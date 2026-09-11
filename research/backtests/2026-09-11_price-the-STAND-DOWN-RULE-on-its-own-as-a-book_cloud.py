#!/usr/bin/env python3
"""Idea 776 - "price-the-STAND-DOWN-RULE-on-its-own-as-a-book" (cloud lane, 2026-09-11).

The question
------------
Idea 774's WF-B found that the only decision rules matching the live book's OOS Sharpe
(1.2747) are the two that STAND DOWN in 6 of 6 cells - i.e. that never act on the panel
ordering at all.  The queue asks whether that is a capital rule in its own right:

    hold RULES v2 unless the challenger's margin over it clears the challenger's OWN
    ESTIMATED NOISE FLOOR, measured in-sample.

This run prices the stand-down gate as a BOOK, on the record's other published dial
families (gross dials, cadence dials, band dials, n dials), on three panels, and reports
whether "do nothing unless the margin clears its floor" ever beats the incumbent.

Construction (everything pre-registered before any number below was read)
------------------------------------------------------------------------
INCUMBENT (per panel): RULES v2 = `baseline.rules_v2_weights(px, band=0.03, gross=0.75)`,
weekly, 10 bps, next-day execution - the live book, identically on all three panels.

DIALS (the record's own published dial families; every rung a book, every rung reported):
    GROSS     band book, band 0.03, W, gross in {0.50, 0.75, 1.00}
    CADENCE   band book, band 0.03, gross 0.75, freq in {W, M, Q}
    BAND      band book, gross 0.75, W, band in {0.00, 0.03, 0.06}
    N         top-n book (composite score, NO vol scaler, above-200d and vol20 < 0.60,
              gross 0.75 spread over n names), W, n in {10, 20, 30, 50}
The first three CONTAIN the incumbent as a rung; the N dial does NOT (its rungs are the
2026-09-04 KEEP-4b family), so the N dial is the only one where the IS margin can be
negative.  That asymmetry is a property of the record's dials, not a design choice, and it
is reported rather than patched.

THE DECISION (made once, at IS_END, on IS data ALONE):
    challenger = the dial's IS-Sharpe argmax rung
    margin     = IS_Sharpe(challenger) - IS_Sharpe(incumbent)
    floor      = the SD of that margin under a MOVING-BLOCK BOOTSTRAP of the paired IS
                 daily returns (block 21 trading days, B = 400, seed 776), IS-only
    rule SD(f): adopt the challenger for the whole OOS window iff margin > f * floor,
                otherwise HOLD THE INCUMBENT (the stand-down).
Controls: NEVER (never adopt - the pure incumbent) and ARGMAX (adopt unconditionally, even
at a negative margin).  SD(0) = "adopt iff the margin is positive" = the record's ordinary
rule-8 selector, so the f ladder prices the FLOOR itself, not the selection.

Tuned parameters (PROTOCOL rule 4: at most two).  Both are swept and every grid point is
published; nothing is chosen on OOS data.
    1. f  - the floor multiple, in {0, 0.5, 1.0, 1.5, 2.0}
    2. DIAL FAMILY - in {GROSS, CADENCE, BAND, N}
The panel is not tuned: all three are reported side by side.

Windows: warm-up = px.index[260]; IS <= 2016-12-31; OOS >= 2017-01-01 (PROTOCOL rule 8).
Costs 10 bps per unit turnover, weights decided at t applied at t+1 (PROTOCOL rules 2-3).

KEEP paths (PROTOCOL rule 4, both evaluated for every realised decision book):
    4a  Sharpe > RULES v2 in BOTH halves AND MaxDD no worse than RULES v2
    4b  Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of |SPY MaxDD|, CAGR >= 70% of SPY

Pre-registered gates (printed before any result is read)
--------------------------------------------------------
G1  fast_backtest reproduces engine.backtest on a probe cell (< 1e-12).
G2  band_book(0.03, 0.75) == baseline.rules_v2_weights exactly (0.0).
G3  SMALL: every ticker with max_1d_move >= 1.0 in data/small_meta.csv dropped FIRST.
G4  CAUSALITY: IS statistics recomputed on a frame TRUNCATED at IS_END must reproduce the
    IS statistics read off the full frame (0.0) - the decision uses no future bar.
G5  Every floor is strictly positive and finite in every NON-DEGENERATE cell.  A cell is
    DEGENERATE when the dial's IS-argmax rung is the incumbent book itself: the margin and
    the floor are then both exactly 0 and the decision is a no-op whatever f is.  Degenerate
    cells are counted and reported, never patched.

Pre-registered bars
-------------------
B1  DOES THE STAND-DOWN GATE EVER BEAT THE INCUMBENT?  PASS iff some f > 0 has OOS Sharpe
    >= the incumbent's in a MAJORITY of the 12 (panel x dial) cells AND strictly greater in
    at least one.  (The stand-down rule can only differ from the incumbent by declining to
    act, so this is the whole capital question.)
B2  DOES THE FLOOR CHANGE ANY DECISION?  No bar - the adoption count by f is the answer.
B3  KEEP.  Any realised decision book clearing 4a or 4b is reported with its path.

CAVEATS.  (i) SURVIVORSHIP (idea 54): U56, B136 and SMALL439 are current-constituent panels
with no delistings, so every CAGR level is inflated and both KEEP columns inherit that.
SMALL439 is the sub-$2B screen with the 44 max_1d_move >= 1.0 names dropped per PROTOCOL.
(ii) One decision per cell means 12 decisions in total; the OOS window is read ONCE and the
cell-level result is a single draw, not a distribution.  (iii) The record's convention keeps
SPY inside each panel as an investable column (rules_v2_weights does), and that is kept here
so the incumbent is the live book verbatim.  (iv) Four dials on three panels sharing one
OOS window are not 12 independent pieces of evidence.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state, score          # noqa
from engine import backtest, metrics, rebalance_mask                             # noqa

OUT = Path(__file__).with_suffix("")
STEM = OUT.name
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARM, COST0, FREQ0, GROSS0, BAND0, VOLCAP = 260, 10.0, "W", 0.75, 0.03, 0.60
BLOCK, NBOOT, SEED = 21, 400, 776
FLADDER = [0.0, 0.5, 1.0, 1.5, 2.0]

LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


# ------------------------------------------------------------------ machinery (record's own)
def fast_backtest(prices, weights, freq="W", cost_bps=10.0):
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(prices.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(prices.index, freq).shift(1, fill_value=False).values
    n = len(prices.index)
    cur = np.zeros(prices.shape[1]); turn = np.zeros(n); pr = np.empty(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        pr[i] = float(cur @ rets[i])
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    return pd.Series(pr - turn * cost_bps / 1e4, index=prices.index)


def M0(r):
    v = r.std() * np.sqrt(252)
    return (r.mean() * 252) / v if v else np.nan


def M(r):
    eq = (1 + r).cumprod(); yrs = len(r) / 252
    h = len(r) // 2
    return dict(CAGR=eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan, Sharpe=M0(r),
                MaxDD=(eq / eq.cummax() - 1).min(), H1=M0(r.iloc[:h]), H2=M0(r.iloc[h:]))


def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band, gross):
    return ew_gross(px, gross).where(band_state(px, band) & px.notna(), 0.0)


def cand_book(px, n, gross=GROSS0, volcap=VOLCAP):
    sc, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < volcap)
    r = sc.where(elig).rank(axis=1, ascending=False)
    return (r <= n).astype(float) * (gross / n)


def load_panels():
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in sm.columns if c == "SPY" or c not in bad]
    panels["SMALL439"] = sm[keep]
    return panels, len(sm.columns) - len(keep)


# ------------------------------------------------------------------ dials
def dial_rungs(px):
    """Every dial family's rungs as (label, weights, freq).  Declared, not searched."""
    d = {}
    d["GROSS"] = [(f"g={g:.2f}", band_book(px, BAND0, g), FREQ0) for g in (0.50, 0.75, 1.00)]
    d["CADENCE"] = [(f"cad={c}", band_book(px, BAND0, GROSS0), c) for c in ("W", "M", "Q")]
    d["BAND"] = [(f"band={b:.2f}", band_book(px, b, GROSS0), FREQ0) for b in (0.00, 0.03, 0.06)]
    d["N"] = [(f"n={n}", cand_book(px, n), FREQ0) for n in (10, 20, 30, 50)]
    return d


def boot_floor(d_chal, d_inc, seed=SEED):
    """SD of the IS Sharpe margin under a moving-block bootstrap of the PAIRED daily rows."""
    rng = np.random.default_rng(seed)
    a, b = d_chal.values, d_inc.values
    n = len(a); nb = int(np.ceil(n / BLOCK))
    starts = rng.integers(0, max(n - BLOCK, 1), size=(NBOOT, nb))
    off = np.arange(BLOCK)
    idx = (starts[:, :, None] + off[None, None, :]).reshape(NBOOT, -1)[:, :n] % n
    A, B = a[idx], b[idx]
    def sh(X):
        s = X.std(axis=1, ddof=1)
        return np.where(s > 0, X.mean(axis=1) * 252 / (s * np.sqrt(252)), np.nan)
    return float(np.nanstd(sh(A) - sh(B), ddof=1))


def keeppaths(m, oos_s, mb, ms, spy_oos_s):
    p4a = (m["H1"] > mb["H1"]) and (m["H2"] > mb["H2"]) and (m["MaxDD"] >= mb["MaxDD"])
    p4b = ((m["H1"] > ms["H1"]) and (m["H2"] > ms["H2"]) and (oos_s > spy_oos_s)
           and (abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"])) and (m["CAGR"] >= 0.70 * ms["CAGR"]))
    return bool(p4a), bool(p4b)


def main():
    P("=" * 100); P(f"IDEA 776 -- {STEM}"); P("=" * 100)
    panels, n_dropped = load_panels()

    # ------------------------------------------------------------- gates
    P("\n(A) PRE-REGISTERED GATES -- run before any result is read")
    ok = True
    px = panels["U56"]
    w = band_book(px, BAND0, GROSS0)
    g2 = float(np.abs(w.values - rules_v2_weights(px, BAND0, GROSS0).values).max())
    P(f"  G2 band_book(0.03,0.75) == rules_v2_weights        : {g2:.3e}  {'PASS' if g2 == 0 else 'FAIL'}")
    ok &= g2 == 0.0
    slow = backtest(px, w, cost_bps=COST0, freq=FREQ0)["returns"]
    fast = fast_backtest(px, w, FREQ0, COST0)
    j = px.index[WARM]                       # engine seeds row 0 from a shifted NaN row;
    g1 = float(np.abs(slow.loc[j:].values - fast.loc[j:].values).max())   # compare post warm-up
    P(f"  G1 fast_backtest == engine.backtest                : {g1:.3e}  {'PASS' if g1 < 1e-12 else 'FAIL'}")
    ok &= g1 < 1e-12
    P(f"  G3 SMALL dropped max_1d_move>=1.0 tickers          : {n_dropped} dropped -> "
      f"{panels['SMALL439'].shape[1]} cols  {'PASS' if n_dropped == 44 else 'FAIL'}")
    ok &= n_dropped == 44
    # G4 causality: truncate the frame at IS_END and re-read the IS statistics
    start = px.index[WARM]
    full_is = fast_backtest(px, w, FREQ0, COST0).loc[start:IS_END]
    tpx = px.loc[:IS_END]
    trunc = fast_backtest(tpx, band_book(tpx, BAND0, GROSS0), FREQ0, COST0).loc[start:]
    g4 = float(np.abs(full_is.values - trunc.reindex(full_is.index).values).max())
    P(f"  G4 IS statistics on a TRUNCATED frame              : {g4:.3e}  {'PASS' if g4 == 0 else 'FAIL'}")
    ok &= g4 == 0.0
    P(f"  gates so far: {'ALL PASS' if ok else 'FAILURE'}")

    # ------------------------------------------------------------- the grid
    P("\n(B) THE FULL DIAL GRID -- every rung of every dial on every panel, all reported")
    rows, rets = [], {}
    spy_stat, inc_stat = {}, {}
    for pname, px in panels.items():
        start = px.index[WARM]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        ms = M(spy); spy_stat[pname] = dict(full=ms, oos=M(spy.loc[OOS_START:]), isw=M(spy.loc[:IS_END]))
        inc = fast_backtest(px, band_book(px, BAND0, GROSS0), FREQ0, COST0).loc[start:]
        rets[(pname, "INCUMBENT")] = inc
        mb = M(inc); inc_stat[pname] = dict(full=mb, oos=M(inc.loc[OOS_START:]), isw=M(inc.loc[:IS_END]))
        for dial, rungs in dial_rungs(px).items():
            for lab, wts, fr in rungs:
                r = fast_backtest(px, wts, fr, COST0).loc[start:]
                rets[(pname, dial, lab)] = r
                m, mo, mi = M(r), M(r.loc[OOS_START:]), M(r.loc[:IS_END])
                rows.append(dict(panel=pname, dial=dial, rung=lab, freq=fr,
                                 IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"],
                                 CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                 H1=m["H1"], H2=m["H2"], OOS_CAGR=mo["CAGR"],
                                 OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
        P(f"  {pname}: incumbent IS Sharpe {inc_stat[pname]['isw']['Sharpe']:.4f} | "
          f"OOS Sharpe {inc_stat[pname]['oos']['Sharpe']:.4f} CAGR {inc_stat[pname]['oos']['CAGR']:.2%} "
          f"MaxDD {inc_stat[pname]['oos']['MaxDD']:.2%} || SPY OOS Sharpe "
          f"{spy_stat[pname]['oos']['Sharpe']:.4f} CAGR {spy_stat[pname]['oos']['CAGR']:.2%}")
    grid = pd.DataFrame(rows)
    grid.to_csv(OUT.with_suffix(".grid.csv"), index=False)
    P("\n  " + grid.to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n  "))

    # ------------------------------------------------------------- decisions
    P("\n(C) THE DECISION, MADE ON IS ALONE -- challenger, margin, floor")
    dec = []
    for pname in panels:
        inc = rets[(pname, "INCUMBENT")]
        inc_is = inc.loc[:IS_END]
        for dial in ("GROSS", "CADENCE", "BAND", "N"):
            g = grid[(grid.panel == pname) & (grid.dial == dial)]
            ch = g.loc[g.IS_Sharpe.idxmax()]
            chal = rets[(pname, dial, ch.rung)]
            margin = float(ch.IS_Sharpe - inc_stat[pname]["isw"]["Sharpe"])
            floor = boot_floor(chal.loc[:IS_END], inc_is)
            # DEGENERATE cell: the dial's IS-argmax rung IS the incumbent book, so the
            # challenger-minus-incumbent series is identically zero and both margin and
            # floor are 0.  The decision is then a no-op by construction; reported, not patched.
            degen = bool(np.abs((chal - inc).values).max() == 0.0)
            dec.append(dict(panel=pname, dial=dial, challenger=ch.rung, IS_margin=margin,
                            floor=floor, degenerate=degen,
                            ratio=margin / floor if floor else np.nan))
            P(f"  {pname:9s} {dial:8s} challenger {ch.rung:10s} IS margin {margin:+.4f} "
              f"floor {floor:.4f}  margin/floor "
              f"{(f'{margin/floor:+.3f}' if floor else 'n/a (degenerate: challenger IS the incumbent)')}")
    dec = pd.DataFrame(dec)
    nd = dec[~dec.degenerate]
    g5 = bool((nd.floor > 0).all() and np.isfinite(nd.floor).all())
    P(f"  G5 floor > 0 in every NON-DEGENERATE cell          : min {nd.floor.min():.4f} over "
      f"{len(nd)} cells ({int(dec.degenerate.sum())} degenerate)  {'PASS' if g5 else 'FAIL'}")
    ok &= g5
    P(f"  GATES: {'ALL PASS' if ok else 'FAILURE -- results below are not to be trusted'}")

    # ------------------------------------------------------------- the rules as books
    P("\n(D) THE STAND-DOWN RULE PRICED AS A BOOK -- every (panel, dial, rule) cell")
    rules = [("NEVER", None), ("ARGMAX", None)] + [(f"SD(f={f})", f) for f in FLADDER]
    out = []
    for _, d in dec.iterrows():
        pname, dial = d.panel, d.dial
        px = panels[pname]; start = px.index[WARM]
        inc = rets[(pname, "INCUMBENT")]; chal = rets[(pname, dial, d.challenger)]
        mb, ms = inc_stat[pname]["full"], spy_stat[pname]["full"]
        spy_oos_s = spy_stat[pname]["oos"]["Sharpe"]
        for rname, f in rules:
            if rname == "NEVER": adopt = False
            elif rname == "ARGMAX": adopt = True
            else: adopt = bool(d.IS_margin > f * d.floor)
            arm = chal if adopt else inc
            # realised path: the incumbent through IS, the decided arm from OOS_START
            path = pd.concat([inc.loc[:IS_END], arm.loc[OOS_START:]])
            m, mo = M(path), M(arm.loc[OOS_START:])
            p4a, p4b = keeppaths(m, mo["Sharpe"], mb, ms, spy_oos_s)
            out.append(dict(panel=pname, dial=dial, rule=rname, f=f, adopt=adopt,
                            arm=d.challenger if adopt else "RULES v2",
                            CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                            H1=m["H1"], H2=m["H2"],
                            OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                            d_OOS_Sharpe=mo["Sharpe"] - inc_stat[pname]["oos"]["Sharpe"],
                            d_OOS_CAGR=mo["CAGR"] - inc_stat[pname]["oos"]["CAGR"],
                            pass4a=p4a, pass4b=p4b))
    res = pd.DataFrame(out)
    res.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)
    P("\n  " + res.to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n  "))

    # ------------------------------------------------------------- verdict
    P("\n(E) BARS")
    agg = (res.groupby("rule", sort=False)
              .agg(adopted=("adopt", "sum"), cells=("adopt", "size"),
                   mean_OOS_Sharpe=("OOS_Sharpe", "mean"), med_OOS_Sharpe=("OOS_Sharpe", "median"),
                   mean_OOS_CAGR=("OOS_CAGR", "mean"), mean_OOS_MaxDD=("OOS_MaxDD", "mean"),
                   beats_inc=("d_OOS_Sharpe", lambda s: int((s > 1e-12).sum())),
                   ties_inc=("d_OOS_Sharpe", lambda s: int((s.abs() <= 1e-12).sum())),
                   p4a=("pass4a", "sum"), p4b=("pass4b", "sum")))
    P("\n  " + agg.to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n  "))
    b1_rules = [r for r in agg.index if r.startswith("SD(f=") and float(r.split("=")[1][:-1]) > 0]
    b1 = False; b1_who = []
    for r in b1_rules:
        sub = res[res.rule == r]
        if (sub.d_OOS_Sharpe >= -1e-12).sum() > len(sub) / 2 and (sub.d_OOS_Sharpe > 1e-12).any():
            b1 = True; b1_who.append(r)
    P(f"\n  B1 stand-down ever beats the incumbent OOS        : {'PASS' if b1 else 'FAIL'}"
      f"  {b1_who if b1_who else '(no f>0 rule is >= incumbent in a majority of cells AND > it once)'}")
    ndiff = int((res[res.rule.str.startswith('SD(')].groupby(['panel', 'dial'])['adopt']
                 .nunique() > 1).sum())
    P(f"  B2 cells where the FLOOR changes the decision      : {ndiff} of 12  "
      f"(adoption by f: " + ", ".join(f"{r}={int(agg.loc[r,'adopted'])}" for r in agg.index if r.startswith('SD')) + ")")
    P(f"  B3 KEEP: 4a passes {int(res.pass4a.sum())} of {len(res)}, "
      f"4b passes {int(res.pass4b.sum())} of {len(res)}")
    if res.pass4b.any():
        P("\n  4b passers:\n  " + res[res.pass4b].to_string(index=False).replace("\n", "\n  "))

    P("\n(F) INCUMBENT / SPY REFERENCE ROWS (full sample from px.index[260], halves, OOS)")
    ref = []
    for pname in panels:
        for who, st in (("RULES v2", inc_stat[pname]), ("SPY", spy_stat[pname])):
            ref.append(dict(panel=pname, book=who, CAGR=st["full"]["CAGR"], Sharpe=st["full"]["Sharpe"],
                            MaxDD=st["full"]["MaxDD"], H1=st["full"]["H1"], H2=st["full"]["H2"],
                            OOS_CAGR=st["oos"]["CAGR"], OOS_Sharpe=st["oos"]["Sharpe"],
                            OOS_MaxDD=st["oos"]["MaxDD"]))
    ref = pd.DataFrame(ref); ref.to_csv(OUT.with_suffix(".reference.csv"), index=False)
    P("\n  " + ref.to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n  "))
    dec.to_csv(OUT.with_suffix(".decisions.csv"), index=False)
    OUT.with_suffix(".console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
