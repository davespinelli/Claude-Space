#!/usr/bin/env python3
"""
IDEA 691 -- is-the-CAGR-FLOOR-the-only-4b-bar-that-ever-binds-ALONE                (cloud lane)
===============================================================================================

THE QUEUE'S QUESTION (verbatim intent)
--------------------------------------
  idea 523 found the 0.70*SPY CAGR floor is the SOLE failing bar for 14 of 30 arms on a fresh
  60-arm family, and that the single 4b pass (U56/topn30) flips to a fail at 25 bps through the
  floor alone while every other bar is untouched.  Pool the record's committed arm corpora and
  measure, per bar, how often it is the UNIQUE cut and how often a cost rung moves it, then
  price whether 4b is a one-bar rule.  Bears on ideas 530/531.  Max 2 params (bar set, rung).

WHY IT MATTERS (and this is a PROTOCOL question, not a book question)
---------------------------------------------------------------------
  PROTOCOL 4b is a five-way conjunction.  If one of its five bars is the unique cut on nearly
  every arm the record has ever run, then 4b is that bar wearing four decorations, the other
  four legs are free, and "passes 4b" means far less than the conjunction advertises.  The
  answer changes how every future KEEP is read.  Nothing here promotes a book.

WHAT IS TUNED AND WHAT IS NOT (PROTOCOL 4, "no more than 2 tuned parameters")
-----------------------------------------------------------------------------
  TUNED (2)  : BARSET (which subset of the five 4b bars is the conjunction) and RUNG (cost bps).
               Every point of both grids is reported -- 5 barsets x 5 rungs, no exceptions.
  NOT TUNED  : the ARM CORPUS.  Every arm below is a book family the record has already
               committed, restated verbatim from
               `research/backtests/2026-09-11_is-the-GROSS-dial-s-4b-FOOTPRINT-the-CAGR-FLOOR-
               alone_C.py` (idea 670's ten arms) crossed with the record's own committed gross
               ladder rungs {0.50, 0.75, 1.00} on the record's three live panels.  No arm was
               chosen by looking at an outcome.  Cadence W (RULES v2) except BAND03_M whose
               cadence IS its definition; band 0.03/0.08; n in {5,10,20}; vol cap 0.60/OFF;
               warm-up 260 rows; IS/OOS split 2016-12-31 / 2017-01-01 (PROTOCOL 8).

THE ARM CORPUS (3 panels x 10 families x 3 gross = 90 arms, each run at 5 cost rungs)
--------------------------------------------------------------------------------------
    BAND03        RULES v2 live band book, band 0.03, W        baseline.rules_v2_weights
    BAND08        band 0.08, W                                 idea 664's committed IS pick
    BAND03_M      band 0.03, MONTHLY                           idea 668's CADENCE companion
    CAND20_VS     top-20 composite rank, vol scaler ON         idea 668's N dial
    CAND20        top-20, NO vol scaler, cap 0.60              the 2026-09-04 KEEP 4b book
    CAND10        top-10, no vol scaler, cap 0.60              width companion
    CAND05        top-5,  no vol scaler, cap 0.60              RULES v1's width
    CAND20_NOCAP  top-20, no vol scaler, cap OFF               idea 668's VOLCAP dial
    EWELIG        equal-weight EVERY eligible name             2026-09-03 memo Finding 2
    SPYBH         gross x SPY, weekly                          ZERO-SIGNAL exposure control

  SPYBH is load-bearing: it carries no signal, so any bar it can fail is a bar about exposure
  and cost, not about edge.

THE FIVE 4b BARS (PROTOCOL 4b, decomposed)
-------------------------------------------
    L1 H1 Sharpe > SPY H1        L2 H2 Sharpe > SPY H2        L3 OOS Sharpe > SPY OOS
    L4 |MaxDD| <= 0.60 |MaxDD_SPY|                            L5 CAGR >= 0.70 CAGR_SPY

  THE STATISTIC THE QUEUE ASKS FOR, stated precisely:
    UNIQUE-CUT RATE of bar X  =  #{arms whose fail set is exactly {X}} / #{arms with >=1 fail}
    SOLE-BLOCKER RATE of X    =  #{arms that fail 4b but pass every bar except X} -- identical
                                 to the above by construction, reported as a gate (G6).
    RUNG SENSITIVITY of X     =  #{arms whose X status differs between adjacent rungs} / 90
    DROP-X RECOVERY           =  pass rate of (4b minus X) - pass rate of 4b.  If dropping one
                                 bar recovers essentially the whole failure mass, 4b IS that bar.

PANELS (PROTOCOL 9 survivorship -- stated, not waved at)
---------------------------------------------------------
  U56      research/universe.json        (ETF + mega-cap panel, today's constituents)
  B136     research/universe_broad.json  (136 large caps, TODAY'S constituents)
  SMALL439 data/prices_small.csv.gz, 483 sub-$2B names since 2010 MINUS the 44 with
           data/small_meta.csv:max_1d_move >= 1.0 (the record's committed filter, idea 627).
  ALL THREE ARE CURRENT-CONSTITUENT PANELS.  Every LEVEL below is biased upward -- the small
  panel worst, since it is a screen run today and carries no name that died before today.  The
  claim this run makes is about WHICH BAR CUTS inside a panel, a within-panel ordering that
  survivorship biases far less than it biases a level, but NO level here is tradeable.

PRE-REGISTERED GATES (run and printed BEFORE any new number is read)
---------------------------------------------------------------------
  G1  fast_backtest == engine.backtest on returns, @10 bps, U56 BAND03      bar 1e-12
  G1b engine.backtest NaN rows all fall inside the discarded 260-row warm-up
  G2  band_book(0.03, 0.75) == baseline.rules_v2_weights                    bar 0.0 (exact)
  G3  SMALL panel is exactly 483-44 = 439 names + SPY benchmark column
  G4  cost rung 0 reproduces the gross return exactly (turnover term vanishes)  bar 1e-15
  G5  SPYBH at gross 1.00 tracks SPY buy-and-hold Sharpe                    bar 0.01
  G6  UNIQUE-CUT and SOLE-BLOCKER counts agree for every bar                bar 0 (exact)

VERDICT DISCIPLINE
------------------
  Both KEEP paths are evaluated at EVERY grid point and all points are reported.  PROTOCOL 8
  is run with two pre-registered choosers, both reading the IS half ONLY.  Nothing is promoted
  on a bar-decomposition result.  A documented KILL / ANSWERED is the expected outcome.
"""
import sys
import warnings
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score   # noqa: E402
from engine import backtest, rebalance_mask                               # noqa: E402

# ---- reported constants (never tuned) --------------------------------------------------------
FREQ0 = "W"
BAND0, BAND1 = 0.03, 0.08
MAXVOL = 0.60
WARM = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"

RUNGS = [0.0, 10.0, 25.0, 50.0, 100.0]        # PARAM 2 -- 10 bps is PROTOCOL 2's binding rung
GROSSES = [0.50, 0.75, 1.00]                  # the record's committed gross rungs
BARS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DDcap", "L5_CAGRfloor"]
BARSETS = {                                    # PARAM 1 -- all five reported
    "FIVE": BARS,                                            # PROTOCOL 4b as written today
    "NO_OOS": ["L1_H1", "L2_H2", "L4_DDcap", "L5_CAGRfloor"],  # 4b before rule 8 was folded in
    "NO_CAGR": ["L1_H1", "L2_H2", "L3_OOS", "L4_DDcap"],      # the floor removed
    "SHARPE3": ["L1_H1", "L2_H2", "L3_OOS"],                  # risk-free reading of 4b
    "RISK2": ["L4_DDcap", "L5_CAGRfloor"],                    # Sharpe-free reading of 4b
}

LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ==============================================================================================
# 1.  ENGINE  (vectorised equivalent of engine.backtest; G1 asserts equality)
# ==============================================================================================
def fast_parts(prices, weights, freq=FREQ0):
    """Return (gross_return, turnover) so every cost rung is one subtraction, not a re-run."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy()
    m[0] = True
    T, Ncol = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, Ncol)), C[:-1]])
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return pd.Series((held * rets).sum(axis=1), index=idx), pd.Series(turn, index=idx)


def at_cost(gross_r, turn, cost):
    return gross_r - turn * cost / 1e4


def M0(r):
    vol = r.std() * np.sqrt(252)
    return (r.mean() * 252) / vol if vol else np.nan


def M(r):
    eq = (1 + r).cumprod()
    yrs = len(r) / 252
    vol = r.std() * np.sqrt(252)
    dd = (eq / eq.cummax() - 1).min()
    h = len(r) // 2
    return dict(CAGR=eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan,
                Sharpe=(r.mean() * 252) / vol if vol else np.nan, MaxDD=dd,
                H1=M0(r.iloc[:h]), H2=M0(r.iloc[h:]))


# ==============================================================================================
# 2.  THE TEN COMMITTED ARM FAMILIES
# ==============================================================================================
def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band, gross):
    return ew_gross(px, gross).where(band_state(px, band) & px.notna(), 0.0)


def ranked_book(px, sc, above, vol20, n, gross, max_vol):
    elig = sc.where(above & (vol20 < max_vol))
    rank = elig.rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.mul(gross / k, axis=0).fillna(0.0)


def elig_ew_book(px, above, vol20, gross, max_vol):
    sel = (above & (vol20 < max_vol) & px.notna()).astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.mul(gross / k, axis=0).fillna(0.0)


def spy_book(px, gross):
    w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    w["SPY"] = float(gross)
    return w.where(px.notna(), 0.0)


FAMILIES = ["BAND03", "BAND08", "BAND03_M", "CAND20_VS", "CAND20", "CAND10", "CAND05",
            "CAND20_NOCAP", "EWELIG", "SPYBH"]
FAM_FREQ = {f: ("M" if f == "BAND03_M" else FREQ0) for f in FAMILIES}


def fam_weights(px, pre, fam, g):
    sc_v, sc_n, above, vol20 = pre
    if fam in ("BAND03", "BAND03_M"):
        return band_book(px, BAND0, g)
    if fam == "BAND08":
        return band_book(px, BAND1, g)
    if fam == "CAND20_VS":
        return ranked_book(px, sc_v, above, vol20, 20, g, MAXVOL)
    if fam == "CAND20":
        return ranked_book(px, sc_n, above, vol20, 20, g, MAXVOL)
    if fam == "CAND10":
        return ranked_book(px, sc_n, above, vol20, 10, g, MAXVOL)
    if fam == "CAND05":
        return ranked_book(px, sc_n, above, vol20, 5, g, MAXVOL)
    if fam == "CAND20_NOCAP":
        return ranked_book(px, sc_n, above, vol20, 20, g, 9.99)
    if fam == "EWELIG":
        return elig_ew_book(px, above, vol20, g, MAXVOL)
    if fam == "SPYBH":
        return spy_book(px, g)
    raise KeyError(fam)


def prep(px):
    sc_v, above, vol20 = score(px, vol_scale=True)
    sc_n, _, _ = score(px, vol_scale=False)
    return sc_v, sc_n, above, vol20


# ==============================================================================================
# 3.  THE FIVE BARS
# ==============================================================================================
def bars_of(r, spy):
    m, ms = M(r), M(spy)
    oos_s, oos_b = M0(r.loc[OOS_START:]), M0(spy.loc[OOS_START:])
    return (dict(L1_H1=bool(m["H1"] > ms["H1"]), L2_H2=bool(m["H2"] > ms["H2"]),
                 L3_OOS=bool(oos_s > oos_b),
                 L4_DDcap=bool(abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"])),
                 L5_CAGRfloor=bool(m["CAGR"] >= 0.70 * ms["CAGR"])), m, ms, oos_s)


def pass4a(m, mb):
    return bool(m["H1"] > mb["H1"] and m["H2"] > mb["H2"] and m["MaxDD"] >= mb["MaxDD"])


# ==============================================================================================
# 4.  PANELS
# ==============================================================================================
def panels():
    out = {}
    out["U56"] = load_universe()
    out["B136"] = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in pxs.columns if c == "SPY" or c not in bad]
    out["SMALL439"] = pxs[keep]
    return out


def main():
    P("=" * 96)
    P(f"IDEA 691  is-the-CAGR-FLOOR-the-only-4b-bar-that-ever-binds-ALONE   (cloud)  {pd.Timestamp.today().date()}")
    P("=" * 96)
    PX = panels()
    for k, v in PX.items():
        P(f"  panel {k:9s} {v.shape[0]} rows x {v.shape[1]} cols   {v.index[0].date()} .. {v.index[-1].date()}")

    # ---------------- GATES ------------------------------------------------------------------
    P("\n" + "-" * 96)
    P("PRE-REGISTERED GATES")
    P("-" * 96)
    gates = []
    px = PX["U56"]
    w = band_book(px, BAND0, 0.75)
    gr, tn = fast_parts(px, w, "W")
    eng = backtest(px, w, cost_bps=10.0, freq="W")["returns"]
    fin = np.isfinite(eng.values)                 # engine emits NaN on its 2 warm-up rows
    d1 = float(np.abs(at_cost(gr, tn, 10.0).values[fin] - eng.values[fin]).max())
    nan_pos = int(np.flatnonzero(~fin).max()) if (~fin).any() else -1
    gates.append(("G1 fast_backtest == engine.backtest (U56 BAND03 @10bps)", d1, 1e-12, d1 < 1e-12))
    # engine.backtest emits NaN on a few early rows (last at row 3); every reported number starts
    # at row WARM=260, so the gate is that no NaN can reach a reported row.
    gates.append(("G1b engine NaNs all inside the discarded warm-up (row < 260)", nan_pos, WARM, nan_pos < WARM))
    d2 = float(np.abs(w.values - rules_v2_weights(px).values).max())
    gates.append(("G2 band_book(0.03,0.75) == rules_v2_weights", d2, 0.0, d2 == 0.0))
    nsmall = len([c for c in PX["SMALL439"].columns if c != "SPY"])
    gates.append(("G3 SMALL panel = 483-44 = 439 names (+SPY bench)", nsmall, 439, nsmall == 439))
    d4 = float(np.abs(at_cost(gr, tn, 0.0).values - gr.values).max())
    gates.append(("G4 cost rung 0 == gross return", d4, 1e-15, d4 <= 1e-15))
    grs, tns = fast_parts(px, spy_book(px, 1.00), "W")
    spy_r = px["SPY"].pct_change().fillna(0.0)
    d5 = abs(M0(at_cost(grs, tns, 10.0).iloc[WARM:]) - M0(spy_r.iloc[WARM:]))
    gates.append(("G5 SPYBH(g=1.00) tracks SPY buy-and-hold Sharpe", d5, 0.01, d5 < 0.01))
    for nm, got, bar, ok in gates:
        P(f"  [{'PASS' if ok else 'FAIL'}] {nm:62s} got {got:.6g}  bar {bar:g}")
    if not all(g[3] for g in gates):
        P("\n  *** A GATE FAILED -- results below are NOT to be read. ***")

    # ---------------- BUILD THE CORPUS -------------------------------------------------------
    P("\n" + "-" * 96)
    P("ARM CORPUS: 3 panels x 10 committed families x 3 gross rungs = 90 arms, each at 5 cost rungs")
    P("-" * 96)
    rows = []
    for pname, px in PX.items():
        pre = prep(px)
        spy_full = px["SPY"].pct_change().fillna(0.0)
        start = px.index[WARM]
        spy = spy_full.loc[start:]
        # RULES v2 baseline per panel, per rung (4a comparand)
        bgr, btn = fast_parts(px, rules_v2_weights(px), "W")
        for fam, g in product(FAMILIES, GROSSES):
            wts = fam_weights(px, pre, fam, g)
            agr, atn = fast_parts(px, wts, FAM_FREQ[fam])
            for rung in RUNGS:
                r = at_cost(agr, atn, rung).loc[start:]
                b = at_cost(bgr, btn, rung).loc[start:]
                L, m, ms, oos_s = bars_of(r, spy)
                mb = M(b)
                fails = [k for k in BARS if not L[k]]
                rows.append(dict(panel=pname, family=fam, gross=g, rung=rung,
                                 CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                 H1=m["H1"], H2=m["H2"], OOS_Sharpe=oos_s,
                                 spy_CAGR=ms["CAGR"], spy_MaxDD=ms["MaxDD"],
                                 spy_H1=ms["H1"], spy_H2=ms["H2"],
                                 base_Sharpe=mb["Sharpe"], base_H1=mb["H1"], base_H2=mb["H2"],
                                 base_MaxDD=mb["MaxDD"],
                                 **{k: L[k] for k in BARS},
                                 n_fail=len(fails), fail_set="+".join(fails) if fails else "NONE",
                                 pass4b=len(fails) == 0, pass4a=pass4a(m, mb)))
        P(f"  {pname}: done ({len(FAMILIES)*len(GROSSES)} arms x {len(RUNGS)} rungs)")
    G = pd.DataFrame(rows)
    dump(G, "grid")

    # ---------------- RESULT 1: unique-cut rate, per bar, per rung ---------------------------
    P("\n" + "=" * 96)
    P("RESULT 1 -- UNIQUE-CUT RATE: how often is each bar the ONLY failing bar?")
    P("            (denominator = arms with >=1 failing bar, at that rung)")
    P("=" * 96)
    uc = []
    for rung in RUNGS:
        sub = G[G.rung == rung]
        failing = sub[sub.n_fail > 0]
        d = dict(rung=rung, n_arms=len(sub), n_fail_any=len(failing), n_pass4b=int(sub.pass4b.sum()))
        for b in BARS:
            d[f"uniq_{b}"] = int((failing.fail_set == b).sum())
            d[f"uniqrate_{b}"] = (failing.fail_set == b).mean() if len(failing) else np.nan
            d[f"failrate_{b}"] = float((~sub[b]).mean())
        uc.append(d)
    UC = pd.DataFrame(uc)
    dump(UC, "uniquecut")
    hdr = f"  {'rung':>5s} {'arms':>5s} {'fail>=1':>8s} {'pass4b':>7s} | " + " ".join(f"{b.split('_')[0]:>18s}" for b in BARS)
    P(hdr)
    P("  " + "-" * (len(hdr) - 2))
    for _, r in UC.iterrows():
        cells = " ".join(f"{int(r[f'uniq_{b}']):5d} ({r[f'uniqrate_{b}']*100 if r[f'uniqrate_{b}']==r[f'uniqrate_{b}'] else float('nan'):5.1f}%)"
                         for b in BARS)
        P(f"  {r['rung']:5.0f} {int(r['n_arms']):5d} {int(r['n_fail_any']):8d} {int(r['n_pass4b']):7d} | {cells}")
    P("\n  FAIL RATE of each bar on its own (not unique -- just 'this bar fails'):")
    P(f"  {'rung':>5s} | " + " ".join(f"{b:>14s}" for b in BARS))
    for _, r in UC.iterrows():
        P(f"  {r['rung']:5.0f} | " + " ".join(f"{r[f'failrate_{b}']*100:13.1f}%" for b in BARS))

    # G6: sole-blocker cross-check
    ok6 = True
    for rung in RUNGS:
        sub = G[G.rung == rung]
        for b in BARS:
            others = [x for x in BARS if x != b]
            sole = int(((~sub[b]) & sub[others].all(axis=1)).sum())
            uniq = int((sub[sub.n_fail > 0].fail_set == b).sum())
            ok6 &= (sole == uniq)
    P(f"\n  [{'PASS' if ok6 else 'FAIL'}] G6 unique-cut == sole-blocker for every (bar, rung)   bar 0 (exact)")

    # ---------------- RESULT 2: DROP-X recovery, x BARSET (param 1) ---------------------------
    P("\n" + "=" * 96)
    P("RESULT 2 -- BARSET x RUNG: pass rate of every reported conjunction (both PARAMS, all 25 points)")
    P("=" * 96)
    bs = []
    for name, keep in BARSETS.items():
        for rung in RUNGS:
            sub = G[G.rung == rung]
            p = sub[keep].all(axis=1)
            bs.append(dict(barset=name, bars="+".join(x.split('_')[0] for x in keep), rung=rung,
                           n=len(sub), n_pass=int(p.sum()), pass_rate=float(p.mean())))
    BS = pd.DataFrame(bs)
    dump(BS, "barsets")
    P(f"  {'barset':>9s} {'bars':>26s} | " + " ".join(f"{int(r):>10d}bps" for r in RUNGS))
    for name in BARSETS:
        sub = BS[BS.barset == name]
        P(f"  {name:>9s} {sub.bars.iloc[0]:>26s} | " +
          " ".join(f"{int(sub[sub.rung==r].n_pass.iloc[0]):4d}/{int(sub[sub.rung==r].n.iloc[0]):3d}({sub[sub.rung==r].pass_rate.iloc[0]*100:4.1f}%)" for r in RUNGS))
    P("\n  DROP-ONE RECOVERY at the PROTOCOL rung (10 bps): extra arms that pass when one bar is removed")
    sub10 = G[G.rung == 10.0]
    base_pass = int(sub10[BARS].all(axis=1).sum())
    for b in BARS:
        keep = [x for x in BARS if x != b]
        n = int(sub10[keep].all(axis=1).sum())
        P(f"    drop {b:14s} -> {n:3d}/{len(sub10)} pass ({n-base_pass:+3d} vs 4b's {base_pass})")

    # ---------------- RESULT 3: rung sensitivity, per bar -------------------------------------
    P("\n" + "=" * 96)
    P("RESULT 3 -- RUNG SENSITIVITY: how many of the 90 arms does a cost rung MOVE, per bar?")
    P("=" * 96)
    key = ["panel", "family", "gross"]
    piv = {b: G.pivot_table(index=key, columns="rung", values=b, aggfunc="first") for b in BARS}
    rs = []
    for i in range(len(RUNGS) - 1):
        a, c = RUNGS[i], RUNGS[i + 1]
        d = dict(step=f"{a:.0f}->{c:.0f}")
        for b in BARS:
            d[b] = int((piv[b][a] != piv[b][c]).sum())
        pa = G[G.rung == a].set_index(key)[BARS].all(axis=1)
        pc = G[G.rung == c].set_index(key)[BARS].all(axis=1)
        d["pass4b_flips"] = int((pa != pc).sum())
        rs.append(d)
    RS = pd.DataFrame(rs)
    dump(RS, "rungsens")
    P(f"  {'step':>10s} | " + " ".join(f"{b:>14s}" for b in BARS) + f" {'4b verdict':>12s}")
    for _, r in RS.iterrows():
        P(f"  {r['step']:>10s} | " + " ".join(f"{int(r[b]):14d}" for b in BARS) + f" {int(r['pass4b_flips']):12d}")
    P(f"\n  (n = 90 arms per step.  A bar that no rung moves is a bar cost cannot reach.)")

    # ---------------- RESULT 4: PROTOCOL 8 walk-forward ---------------------------------------
    P("\n" + "=" * 96)
    P("RESULT 4 -- PROTOCOL 8 WALK-FORWARD: choose on 2008-2016 ONLY, evaluate 2017-2026 untouched")
    P("=" * 96)
    wf = []
    for pname, px in PX.items():
        pre = prep(px)
        start = px.index[WARM]
        spy_all = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_is, spy_oos = spy_all.loc[:IS_END], spy_all.loc[OOS_START:]
        bgr, btn = fast_parts(px, rules_v2_weights(px), "W")
        cand = []
        for fam, g in product(FAMILIES, GROSSES):
            if fam == "SPYBH":
                continue                      # the control is never a candidate book
            agr, atn = fast_parts(px, fam_weights(px, pre, fam, g), FAM_FREQ[fam])
            r = at_cost(agr, atn, 10.0).loc[start:]
            ris, roos = r.loc[:IS_END], r.loc[OOS_START:]
            mi, msi = M(ris), M(spy_is)
            is_bars = dict(L1_H1=mi["H1"] > msi["H1"], L2_H2=mi["H2"] > msi["H2"],
                           L3_OOS=mi["Sharpe"] > msi["Sharpe"],      # IS stand-in; no peeking
                           L4_DDcap=abs(mi["MaxDD"]) <= 0.60 * abs(msi["MaxDD"]),
                           L5_CAGRfloor=mi["CAGR"] >= 0.70 * msi["CAGR"])
            cand.append(dict(family=fam, gross=g, is_Sharpe=mi["Sharpe"], is_CAGR=mi["CAGR"],
                             is_MaxDD=mi["MaxDD"], is_nbar=int(sum(is_bars.values())),
                             is_pass4b=all(is_bars.values()), roos=roos))
        C = pd.DataFrame(cand)
        mbo = M(at_cost(bgr, btn, 10.0).loc[OOS_START:])
        mso = M(spy_oos)
        for chooser in ("IS_SHARPE_ARGMAX", "IS_4b_THEN_SHARPE"):
            pool = C[C.is_pass4b] if (chooser == "IS_4b_THEN_SHARPE" and C.is_pass4b.any()) else C
            pick = pool.loc[pool.is_Sharpe.idxmax()]
            mo = M(pick["roos"])
            oos_bars = dict(L1_H1=mo["H1"] > mso["H1"], L2_H2=mo["H2"] > mso["H2"],
                            L3_OOS=mo["Sharpe"] > mso["Sharpe"],
                            L4_DDcap=abs(mo["MaxDD"]) <= 0.60 * abs(mso["MaxDD"]),
                            L5_CAGRfloor=mo["CAGR"] >= 0.70 * mso["CAGR"])
            f = [k for k, v in oos_bars.items() if not v]
            wf.append(dict(panel=pname, chooser=chooser, pick=f"{pick['family']}@g{pick['gross']:.2f}",
                           is_pool=len(pool), is_Sharpe=pick["is_Sharpe"],
                           oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                           base_oos_CAGR=mbo["CAGR"], base_oos_Sharpe=mbo["Sharpe"], base_oos_MaxDD=mbo["MaxDD"],
                           spy_oos_CAGR=mso["CAGR"], spy_oos_Sharpe=mso["Sharpe"], spy_oos_MaxDD=mso["MaxDD"],
                           oos_fail_set="+".join(f) if f else "NONE", oos_pass4b=not f,
                           oos_pass4a=pass4a(mo, M(at_cost(bgr, btn, 10.0).loc[OOS_START:]))))
    WF = pd.DataFrame(wf)
    dump(WF, "walkforward")
    for _, r in WF.iterrows():
        P(f"\n  {r['panel']} / {r['chooser']}   pick = {r['pick']}  (IS pool {r['is_pool']}, IS Sharpe {r['is_Sharpe']:.3f})")
        P(f"    {'':22s} {'CAGR':>9s} {'Sharpe':>9s} {'MaxDD':>9s}")
        P(f"    {'PICK (OOS 2017-26)':22s} {r['oos_CAGR']:8.2%} {r['oos_Sharpe']:9.3f} {r['oos_MaxDD']:8.2%}")
        P(f"    {'RULES v2 baseline':22s} {r['base_oos_CAGR']:8.2%} {r['base_oos_Sharpe']:9.3f} {r['base_oos_MaxDD']:8.2%}")
        P(f"    {'SPY':22s} {r['spy_oos_CAGR']:8.2%} {r['spy_oos_Sharpe']:9.3f} {r['spy_oos_MaxDD']:8.2%}")
        P(f"    OOS 4b: {'PASS' if r['oos_pass4b'] else 'FAIL on ' + r['oos_fail_set']}    OOS 4a: {'PASS' if r['oos_pass4a'] else 'FAIL'}")

    # ---------------- RESULT 5: the answer ----------------------------------------------------
    P("\n" + "=" * 96)
    P("RESULT 5 -- IS 4b A ONE-BAR RULE?")
    P("=" * 96)
    sub = G[G.rung == 10.0]
    failing = sub[sub.n_fail > 0]
    P(f"  At PROTOCOL's 10 bps: {len(sub)} arms, {int(sub.pass4b.sum())} pass 4b, {len(failing)} fail.")
    P(f"  Fail-set composition (top 12 of {failing.fail_set.nunique()} distinct sets):")
    for s, c in failing.fail_set.value_counts().head(12).items():
        P(f"    {c:4d}  {s}")
    P(f"\n  Arms with exactly one failing bar: {int((failing.n_fail==1).sum())} of {len(failing)} "
      f"({(failing.n_fail==1).mean()*100:.1f}%)")
    P(f"  Mean number of failing bars per failing arm: {failing.n_fail.mean():.2f}")
    P(f"  4a passes at 10 bps: {int(sub.pass4a.sum())} of {len(sub)}")
    P("")
    P(f"  {'bar':>14s} {'uniq-cut':>9s} {'fail rate':>10s} {'drop-1 recovery':>16s} {'rungs that move it':>19s}")
    for b in BARS:
        uq = int((failing.fail_set == b).sum())
        fr = float((~sub[b]).mean())
        keep = [x for x in BARS if x != b]
        rec = int(sub[keep].all(axis=1).sum()) - int(sub[BARS].all(axis=1).sum())
        mv = int(RS[b].sum())
        P(f"  {b:>14s} {uq:9d} {fr*100:9.1f}% {rec:+16d} {mv:19d}")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    P(f"\n  wrote {STEM}.console.txt")


if __name__ == "__main__":
    main()
