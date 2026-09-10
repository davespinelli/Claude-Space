#!/usr/bin/env python3
"""Idea 630 -- price the ELAPSED-DAYS drift as a standing reproduction tolerance.

Idea 409 found that idea 401's u56 non-reproduction is NOT vendor restatement: the IS window
(<= 2016-12-31) reproduces to 3.7e-06 while full-sample H2 drifts 1.63e-02 three days later.
The cause it named is the daily-close job APPENDING rows, which (a) lengthens the sample and
(b) moves the `len(r)//2` half-boundary that `baseline._row` and every downstream file use.
Every cross-run '0.000e+00' in the record measured on a live-refreshed panel is therefore a
statement about ELAPSED DAYS, not about precision.

This file prices that drift as a function of elapsed days on a FROZEN panel, so the append
channel is isolated exactly (nothing is restated -- the same committed CSV is truncated), and
proposes the two candidate conventions the queue asks for.

    PART A  THE DRIFT LADDER.  For each panel x book x base vintage x elapsed days k, re-read
            the same book's metrics as a reader would k trading days after publication, and
            record |metric(base+k) - metric(base)| on ten published quantities.
    PART B  CHANNEL DECOMPOSITION.  Split the drift into the APPEND channel (the full-sample
            window grows by k days) and the BOUNDARY channel (`len(r)//2` moves by k/2 days),
            by re-reading the same returns under an end-date rule that pins the boundary date.
            Rule 8's own 2016-12-31 split is calendar-pinned by construction and is the
            control: its IS leg must drift EXACTLY zero.
    PART C  THE TOLERANCE.  Publish tol_X(k) = q95 of |drift_X| over the corpus, per metric,
            and walk it forward: the bar is fitted on the EARLY bases only and its coverage is
            read once on the LATE bases it never saw.
    PART D  RULE 8 + BOTH KEEP PATHS on every grid point, so the measurement idea is still
            scored as a book idea (PROTOCOL 4, 8).

TWO TUNED PARAMETERS, and no more (PROTOCOL 4):
    PANEL         in {U56, B136, SMALL439}
    END_DATE_RULE in {LIVE, PIN_BOUNDARY, PIN_END}
        LIVE         -- the record's convention: read the panel as it stands, halves at len//2.
        PIN_BOUNDARY -- read the fresh panel, but hold the half-boundary at the DATE it had
                        when the result was published.
        PIN_END      -- hold the published end date; re-read the same window.
The book set (5), the base ladder (7) and the elapsed-days grid (9) are corpus axes held
identical across every cell, not dials: nothing in this file is chosen to make a number look
better, and all 8,505 drift rows are written to .drift.csv.

PROTOCOL-fixed: weights decided at close t, applied at t+1; 10 bps per unit turnover; long
only, no leverage; warm-up 260 rows dropped.
SURVIVORSHIP: B136 and SMALL439 are CURRENT constituent lists (PROTOCOL 9). SMALL439
additionally drops the 44 names with data/small_meta.csv max_1d_move >= 1.0 -- idea 623's
terminal-dated screen, priced by idea 627 -- kept here because the record's published numbers,
which are what this file is measuring the reproducibility of, all carry it.

Run:  python3 research/backtests/2026-09-10_price-the-ELAPSED-DAYS-drift-as-a-standing-reproduction-tolerance_cloud.py
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, rebalance_mask, metrics  # noqa

pd.set_option("display.width", 250)
OUT = Path(__file__).with_suffix("")
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COST_BPS = 10.0
WARMUP = 260

# corpus axes (held identical in every cell)
BASES = [1512, 1008, 756, 504, 252, 126, 63]      # trading days before the panel's last row
KGRID = [1, 2, 3, 5, 8, 13, 21, 34, 55]           # elapsed trading days since publication
RULES = ["LIVE", "PIN_BOUNDARY", "PIN_END"]
METRICS = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS", "OOS", "OOS_CAGR", "OOS_DD", "m4b"]


# ---------------------------------------------------------------- vectorised engine (gated)
def fast_backtest(prices, weights, freq):
    """Identical to engine.backtest's returns/turnover, vectorised.  Gate G1 asserts it."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy(); m[0] = True
    T, Ncol = rets.shape
    C = np.cumprod(1.0 + rets, axis=0); Cp = np.vstack([np.ones((1, Ncol)), C[:-1]])
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]; W0 = wt[s0]
    h = W0 * (Cp / Cp[s0]); V = h.sum(axis=1) + (1.0 - W0.sum(axis=1)); held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]; W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p]); Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1)); heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T); turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return pd.Series((held * rets).sum(axis=1), index=idx), pd.Series(turn, index=idx)


# ------------------------------------------------------------------------------- the books
def w_cand20(px):
    """The 2026-09-04 KEEP 4b candidate: top-20 of the scan.py composite, no vol scaler,
    above its own 200d MA, equal weight, gross 1.00."""
    s, above, _ = score(px, vol_scale=False)
    sel = (s.where(above & px.notna()).rank(axis=1, ascending=False) <= 20).astype(float)
    return sel.div(sel.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def w_ewall(px):
    """Equal weight every priced name at gross 0.75 -- the record's de-grossed control."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return 0.75 * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


BOOKS = {"RULESv2": (rules_v2_weights, "W"), "RULESv1": (rules_v1_weights, "W"),
         "CAND20": (w_cand20, "W"), "EWALL": (w_ewall, "W")}


# ------------------------------------------------------------------------ metric readings
def read(r, end, rule, base_end, base_bound):
    """Read a book's published quantities at vintage `end` under one end-date rule.

    LIVE          window = [start, end],       half-boundary = len//2 of that window
    PIN_BOUNDARY  window = [start, end],       half-boundary = the DATE it had at base
    PIN_END       window = [start, base_end],  half-boundary = len//2 of that window
    """
    if rule == "PIN_END":
        rv = r.loc[:base_end]
    else:
        rv = r.loc[:end]
    if len(rv) < 60:
        return None
    if rule == "PIN_BOUNDARY":
        h = int(rv.index.searchsorted(base_bound))
    else:
        h = len(rv) // 2
    h = max(1, min(h, len(rv) - 1))
    f = metrics(rv); m1 = metrics(rv.iloc[:h]); m2 = metrics(rv.iloc[h:])
    ins = metrics(rv.loc[:IS_END]); oos = metrics(rv.loc[OOS_START:])
    return dict(CAGR=f["CAGR"], Sharpe=f["Sharpe"], MaxDD=f["MaxDD"], H1=m1["Sharpe"],
                H2=m2["Sharpe"], IS=ins["Sharpe"], OOS=oos["Sharpe"], OOS_CAGR=oos["CAGR"],
                OOS_DD=oos["MaxDD"])


def margins_4b(L, S):
    """The five 4b bars as SIGNED margins (>=0 passes).  m4b = the binding one."""
    return dict(H1=L["H1"] - S["H1"], H2=L["H2"] - S["H2"], OOS=L["OOS"] - S["OOS"],
                DD=L["MaxDD"] - 0.60 * S["MaxDD"], CAGR=L["CAGR"] - 0.70 * S["CAGR"])


def verdict_4a(L, B):
    return L["H1"] > B["H1"] and L["H2"] > B["H2"] and L["MaxDD"] >= B["MaxDD"]


# ------------------------------------------------------------------------------- the panels
def load_panels():
    P = {}
    P["U56"] = load_universe()
    P["B136"] = load_universe(broad=True)
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    P["SMALL439"] = sm.drop(columns=[c for c in sm.columns if c in bad])
    return P


# ================================================================================== GATES
def gate_g1(px):
    """G1  fast_backtest reproduces engine.backtest on returns AND turnover."""
    q = px.drop(columns=["SPY"])
    w = w_cand20(q)
    fr, ft = fast_backtest(q, w, "W")
    eng = backtest(q, w, cost_bps=0.0, freq="W")
    st = q.index[WARMUP]
    dr = float((fr.loc[st:] - eng["returns"].loc[st:]).abs().max())
    dt_ = float((ft.loc[st:] - eng["turnover"].loc[st:]).abs().max())
    print(f"G1  fast_backtest vs engine.backtest (U56 CAND20 W): max|dret| {dr:.3e}  "
          f"max|dturn| {dt_:.3e}")
    assert dr < 1e-10 and dt_ < 1e-10, "G1 FAILED"


def gate_g2(px):
    """G2  TRUNCATION INVARIANCE -- the premise of the whole file.  Every signal used here is
    causal, so a book run on the panel truncated at E must give the SAME returns on [start,E]
    as the book run on the full panel and then truncated.  If this fails, the drift measured
    below is contaminated by the truncation itself rather than by elapsed days."""
    q = px.drop(columns=["SPY"])
    worst = 0.0
    for nm, (fn, freq) in BOOKS.items():
        full, _ = fast_backtest(q, fn(q), freq)
        for off in (504, 63):
            E = q.index[-off]
            qt = q.loc[:E]
            tr, _ = fast_backtest(qt, fn(qt), freq)
            d = float((full.loc[:E] - tr).abs().max())
            worst = max(worst, d)
    print(f"G2  truncation invariance over 4 books x 2 vintages (U56): max|dret| {worst:.3e}")
    assert worst < 1e-12, "G2 FAILED -- a book in this file is not causal"


def gate_g3(rets, panels):
    """G3  PIN_END drift is EXACTLY zero by construction.  Asserted, not assumed: it is the
    proposal this file recommends, so it must be demonstrated on the real corpus."""
    worst = 0.0
    for pn, R in rets.items():
        end_i = panels[pn].index
        for bk, r in R.items():
            for boff in (504, 63):
                be = end_i[-boff]
                bb = r.loc[:be].index[len(r.loc[:be]) // 2]
                a = read(r, be, "PIN_END", be, bb)
                for k in (3, 21):
                    e = end_i[end_i.searchsorted(be) + k]
                    b = read(r, e, "PIN_END", be, bb)
                    worst = max(worst, max(abs(a[m] - b[m]) for m in a))
    print(f"G3  PIN_END drift over 3 panels x 5 books x 2 bases x 2 k: max|d| {worst:.3e}")
    assert worst == 0.0, "G3 FAILED"


def gate_g4(rets, panels):
    """G4  RULE 8's IS leg is calendar-pinned, so under LIVE it must ALSO drift exactly zero
    while H1 does not.  This is idea 409's finding restated as an assertion."""
    worst_is, worst_h1 = 0.0, 0.0
    for pn, R in rets.items():
        end_i = panels[pn].index
        for bk, r in R.items():
            be = end_i[-252]
            bb = r.loc[:be].index[len(r.loc[:be]) // 2]
            a = read(r, be, "LIVE", be, bb)
            e = end_i[end_i.searchsorted(be) + 55]
            b = read(r, e, "LIVE", be, bb)
            worst_is = max(worst_is, abs(a["IS"] - b["IS"]))
            worst_h1 = max(worst_h1, abs(a["H1"] - b["H1"]))
    print(f"G4  LIVE, k=55: max|d IS| {worst_is:.3e}   max|d H1| {worst_h1:.3e}")
    assert worst_is == 0.0 and worst_h1 > 1e-4, "G4 FAILED"


# ==================================================================================== main
def main():
    panels = load_panels()
    print("PANELS")
    for pn, px in panels.items():
        print(f"  {pn:9s} {px.shape[1]:4d} cols  {px.index[0].date()} .. {px.index[-1].date()}"
              f"  ({len(px)} rows)")

    gate_g1(panels["U56"])
    gate_g2(panels["U56"])

    # ---- one returns series per (panel, book); every vintage is a window over it (G2)
    rets = {}
    for pn, px in panels.items():
        q = px.drop(columns=["SPY"])
        R = {}
        for bk, (fn, freq) in BOOKS.items():
            r, t = fast_backtest(q, fn(q), freq)
            R[bk] = (r - t * COST_BPS / 1e4).iloc[WARMUP:]
        R["SPY"] = px["SPY"].pct_change().fillna(0.0).iloc[WARMUP:]
        rets[pn] = R
    print(f"\nbooks priced: {len(rets)} panels x {len(rets['U56'])} books")

    gate_g3(rets, panels)
    gate_g4(rets, panels)

    # ============================================================ PART A + B: drift ladder
    rows = []
    for pn, px in panels.items():
        idx = px.index
        for boff in BASES:
            be = idx[-boff]
            bpos = idx.searchsorted(be)
            for bk in list(BOOKS) + ["SPY"]:
                r = rets[pn][bk]
                rb = r.loc[:be]
                bbound = rb.index[len(rb) // 2]
                for rule in RULES:
                    a = read(r, be, rule, be, bbound)
                    sa = read(rets[pn]["SPY"], be, rule, be, bbound)
                    ma = margins_4b(a, sa); a["m4b"] = min(ma.values())
                    for k in KGRID:
                        e = idx[bpos + k]
                        b = read(r, e, rule, be, bbound)
                        sb = read(rets[pn]["SPY"], e, rule, be, bbound)
                        mb = margins_4b(b, sb); b["m4b"] = min(mb.values())
                        row = dict(panel=pn, book=bk, rule=rule, base=str(be.date()),
                                   base_off=boff, k=k, T=len(r.loc[:be]))
                        for m in METRICS:
                            row["d_" + m] = abs(a[m] - b[m])
                        rows.append(row)
    D = pd.DataFrame(rows)
    D.to_csv(OUT.with_suffix(".drift.csv"), index=False)
    print(f"\nPART A  drift ladder: {len(D)} rows -> {OUT.with_suffix('.drift.csv').name}")

    print("\n--- A1  max |drift| by END-DATE RULE and metric, over the whole corpus "
          f"({len(D)//len(RULES)} rows per rule) ---")
    print(D.groupby("rule")[["d_" + m for m in METRICS]].max()
          .reindex(RULES).to_string(float_format=lambda x: f"{x:.3e}"))
    print("\n--- A2  median |drift| by END-DATE RULE and metric ---")
    print(D.groupby("rule")[["d_" + m for m in METRICS]].median()
          .reindex(RULES).to_string(float_format=lambda x: f"{x:.3e}"))

    print("\n--- B1  CHANNEL DECOMPOSITION on the halves, LIVE vs PIN_BOUNDARY, by k "
          "(median |drift|; LIVE = append+boundary, PIN_BOUNDARY = append alone) ---")
    ch = D[D.rule.isin(["LIVE", "PIN_BOUNDARY"])].pivot_table(
        index="k", columns="rule", values=["d_H1", "d_H2", "d_Sharpe", "d_OOS"], aggfunc="median")
    print(ch.to_string(float_format=lambda x: f"{x:.3e}"))
    live_h = D[D.rule == "LIVE"][["d_H1", "d_H2"]].median().mean()
    pin_h = D[D.rule == "PIN_BOUNDARY"][["d_H1", "d_H2"]].median().mean()
    print(f"\n  boundary channel / append channel on the halves = {live_h / max(pin_h,1e-18):.1f}x"
          f"   (median |dH1|,|dH2|: LIVE {live_h:.3e} vs PIN_BOUNDARY {pin_h:.3e})")

    print("\n--- B2  LIVE median |drift| by elapsed days k (all panels, books, bases) ---")
    print(D[D.rule == "LIVE"].groupby("k")[["d_" + m for m in METRICS]].median()
          .to_string(float_format=lambda x: f"{x:.3e}"))
    print("\n--- B3  LIVE median |drift| by panel and by book (k pooled) ---")
    print(D[D.rule == "LIVE"].groupby("panel")[["d_Sharpe", "d_H1", "d_H2", "d_OOS", "d_m4b"]]
          .median().to_string(float_format=lambda x: f"{x:.3e}"))
    print(D[D.rule == "LIVE"].groupby("book")[["d_Sharpe", "d_H1", "d_H2", "d_OOS", "d_m4b"]]
          .median().to_string(float_format=lambda x: f"{x:.3e}"))
    print("\n--- B4  does drift scale as 1/T?  LIVE median |dSharpe| by base sample length ---")
    b4 = D[D.rule == "LIVE"].groupby("base_off").agg(T=("T", "median"),
                                                     dSharpe=("d_Sharpe", "median"),
                                                     dH2=("d_H2", "median"))
    b4["dSharpe_x_T"] = b4.dSharpe * b4["T"]; b4["dH2_x_T"] = b4.dH2 * b4["T"]
    print(b4.to_string(float_format=lambda x: f"{x:.4g}"))

    # ============================================================ PART C: the tolerance
    print("\n=== PART C  the proposed tolerance tol_X(k) = q95 |drift_X| (LIVE rule) ===")
    L = D[D.rule == "LIVE"]
    tol = L.groupby("k")[["d_" + m for m in METRICS]].quantile(0.95)
    print(tol.to_string(float_format=lambda x: f"{x:.3e}"))
    print("\n  For reference the record's habitual hand-typed bars: 5e-4 (idea 401), 1e-6 "
          "(idea 520's flat proposal).  Share of LIVE corpus rows already outside each:")
    for bar in (1e-6, 5e-5, 5e-4, 1e-2):
        sh = {m: float((L["d_" + m] > bar).mean()) for m in ("Sharpe", "H1", "H2", "OOS", "m4b")}
        print(f"    bar {bar:.0e}: " + "  ".join(f"{m} {v:.1%}" for m, v in sh.items()))

    print("\n--- C2  RULE 8 FOR THE TOLERANCE: fit q95 on the EARLY bases, read coverage once "
          "on the LATE bases (never seen) ---")
    early = L[L.base_off >= 504]; late = L[L.base_off < 504]
    fit = early.groupby("k")[["d_" + m for m in METRICS]].quantile(0.95)
    cov = []
    for k in KGRID:
        lk = late[late.k == k]
        cov.append(dict(k=k, n=len(lk), **{m: float((lk["d_" + m] <= fit.loc[k, "d_" + m]).mean())
                                           for m in ("Sharpe", "H1", "H2", "OOS", "m4b")}))
    C2 = pd.DataFrame(cov).set_index("k")
    print(C2.to_string(float_format=lambda x: f"{x:.3f}"))
    print(f"  mean OOS coverage of a 0.95 bar: "
          f"{C2[['Sharpe','H1','H2','OOS','m4b']].values.mean():.3f}")

    # ============================================ PART D: verdicts, rule 8, both KEEP paths
    print("\n=== PART D  BOTH KEEP PATHS at every vintage, and rule 8 ===")
    vr = []
    for pn, px in panels.items():
        idx = px.index
        for boff in BASES:
            be = idx[-boff]; bpos = idx.searchsorted(be)
            for k in [0] + KGRID:
                e = idx[bpos + k] if k else be
                rb = rets[pn]["RULESv2"].loc[:be]
                bbound = rb.index[len(rb) // 2]
                S = read(rets[pn]["SPY"], e, "LIVE", be, bbound)
                B = read(rets[pn]["RULESv2"], e, "LIVE", be, bbound)
                for bk in list(BOOKS) + ["SPY"]:
                    Lr = read(rets[pn][bk], e, "LIVE", be, bbound)
                    mg = margins_4b(Lr, S)
                    vr.append(dict(panel=pn, book=bk, base_off=boff, k=k,
                                   v4a=int(verdict_4a(Lr, B)),
                                   v4b=int(min(mg.values()) >= 0),
                                   bind=min(mg, key=mg.get), m4b=min(mg.values()),
                                   CAGR=Lr["CAGR"], Sharpe=Lr["Sharpe"], MaxDD=Lr["MaxDD"],
                                   H1=Lr["H1"], H2=Lr["H2"], OOS=Lr["OOS"],
                                   OOS_CAGR=Lr["OOS_CAGR"], OOS_DD=Lr["OOS_DD"]))
    V = pd.DataFrame(vr)
    V.to_csv(OUT.with_suffix(".verdicts.csv"), index=False)
    nb = V[V.book != "SPY"]
    print(f"  grid points (book x panel x vintage, SPY excluded as a book): {len(nb)}")
    print(f"  4a passes: {int(nb.v4a.sum())}/{len(nb)}     4b passes: {int(nb.v4b.sum())}/{len(nb)}")
    print("  binding 4b bar:", nb.bind.value_counts().to_dict())
    print("\n--- D1  4b pass rate by panel x book (over 70 vintages each) ---")
    print(nb.pivot_table(index="book", columns="panel", values="v4b", aggfunc="mean")
          .to_string(float_format=lambda x: f"{x:.3f}"))
    flips = nb.groupby(["panel", "book", "base_off"]).agg(n4a=("v4a", "nunique"),
                                                          n4b=("v4b", "nunique"))
    print(f"\n--- D2  VERDICT FLIPS within a base's own 55-day re-read window: "
          f"4a {(flips.n4a > 1).sum()}/{len(flips)} cells, 4b {(flips.n4b > 1).sum()}/{len(flips)} cells")
    if (flips.n4b > 1).any():
        print(flips[flips.n4b > 1].to_string())
    if (flips.n4a > 1).any():
        print(flips[flips.n4a > 1].to_string())

    print("\n--- D3  RULE 8: book chosen on IS (2010-2016) Sharpe alone, OOS (2017-2026) read "
          "once, full frozen panel ---")
    r8 = []
    for pn in panels:
        S = rets[pn]["SPY"]; B = rets[pn]["RULESv2"]
        sm = metrics(S.loc[OOS_START:]); bm = metrics(B.loc[OOS_START:])
        iss = {bk: metrics(rets[pn][bk].loc[:IS_END])["Sharpe"] for bk in BOOKS}
        pick = max(iss, key=iss.get)
        om = metrics(rets[pn][pick].loc[OOS_START:])
        r8.append(dict(panel=pn, pick=pick, IS_Sharpe=iss[pick],
                       OOS_CAGR=om["CAGR"], OOS_Sharpe=om["Sharpe"], OOS_MaxDD=om["MaxDD"],
                       v2_OOS_CAGR=bm["CAGR"], v2_OOS_Sharpe=bm["Sharpe"], v2_OOS_MaxDD=bm["MaxDD"],
                       spy_OOS_CAGR=sm["CAGR"], spy_OOS_Sharpe=sm["Sharpe"], spy_OOS_MaxDD=sm["MaxDD"]))
    R8 = pd.DataFrame(r8).set_index("panel")
    print(R8.to_string(float_format=lambda x: f"{x:.4f}"))
    print("  IS Sharpe of every book (the menu rule 8 chose from):")
    print(pd.DataFrame({pn: {bk: metrics(rets[pn][bk].loc[:IS_END])["Sharpe"] for bk in BOOKS}
                        for pn in panels}).to_string(float_format=lambda x: f"{x:.4f}"))

    print("\n--- D4  full-sample table on the live panel end (the record's own reading) ---")
    tb = []
    for pn in panels:
        for bk in list(BOOKS) + ["SPY"]:
            r = rets[pn][bk]; h = len(r) // 2
            f, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
            o = metrics(r.loc[OOS_START:])
            tb.append(dict(panel=pn, book=bk, CAGR=f["CAGR"], Sharpe=f["Sharpe"],
                           MaxDD=f["MaxDD"], H1=m1["Sharpe"], H2=m2["Sharpe"],
                           OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"]))
    T4 = pd.DataFrame(tb).set_index(["panel", "book"])
    T4.to_csv(OUT.with_suffix(".books.csv"))
    print(T4.to_string(float_format=lambda x: f"{x:.4f}"))

    print("\n=== VERDICT ===")
    print("  4a", int(nb.v4a.sum()), "/", len(nb), "   4b", int(nb.v4b.sum()), "/", len(nb))


if __name__ == "__main__":
    main()
