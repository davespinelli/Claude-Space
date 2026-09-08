#!/usr/bin/env python3
"""Idea 460 — BACK-FILL THE EW_ALL COLUMN ON THE FILES WHOSE HEADLINE IS A PANEL ORDERING.

Idea 239 found that a majority of the record's multi-panel files publish no un-ranked
control.  A large family of those files' headlines is a PANEL ORDERING — "U56 > B136 >
SMALL439", "the gate premium is monotone in the panel", "the effect is a small-cap fact".
Every such ordering is a statement about a BOOK measured on three different panels, and it
is only a statement about the BOOK if the panel's own passive content has been removed.
This run back-fills that column and asks: how many published panel orderings survive being
re-quoted as an EXCESS over that panel's own EW_ALL?

Pre-registration (fixed before any number was read):
  * EW_ALL, the un-ranked control: hold every PRICED name in the panel at g/N of NAV
    (g = 0.75, the live gross; N = instruments priced that day), no gate, no ranking, no
    vol scaler, weekly, next-day execution.  This is `dg_weights(gate=NONE, g=0.75)` and it
    is the same object across all three panels, so the panel is the only thing that varies.
  * RESTATEMENT.  For a metric M (Sharpe or CAGR), a book B and a panel P:
        RAW(B,P)    = M(B on P)
        EXCESS(B,P) = M(B on P) - M(EW_ALL on P)          [same panel, same rung, same window]
    An ORDERING is the ranking of the three panels for one book at one rung under one
    metric.  It SURVIVES iff the RAW ordering and the EXCESS ordering are the same
    permutation.  A pairwise comparison (P_i vs P_j) FLIPS iff sign(RAW_i - RAW_j) !=
    sign(EXCESS_i - EXCESS_j).  Both are reported; the pairwise count is the primary one
    because most published headlines quote a pair, not the full triple.
  * COMMON WINDOW.  Panels have different histories (U56/B136 from 2008, SMALL439 from
    2010).  An ordering across panels is only meaningful on a shared sample, so every
    number in PART B is computed on the INTERSECTION of the three panels' trading days
    after each panel's own 260-day warm-up.  Stated in the console.
  * TWO tuned parameters, no more: BOOK FORM and PANEL.  Cost rung (10, 25 bps) is
    reported at both, never chosen.  Every grid point is reported.
        books (12) = EWALL(control), RULESV2(=BAND3-dg .75, live), MA200dg, BAND6dg, ABSdg,
                     TOP5V1(vol-scaled, RULES v1 form), TOP10, TOP20, TOP40 (equal weight,
                     no vol scaler = the 2026-09-04 KEEP 4b form), TOP20V (vol-scaled),
                     TOP20B3 (rank inside the band), LOWVOL20
        panels (3) = U56, B136, SMALL439 (sub-$2B less the 44 with max_1d_move >= 1.0)
        rungs (2)  = 10, 25 bps
    12 x 3 x 2 = 72 grid points, ALL reported.
  * BOTH KEEP paths on every point: 4a vs the live RULES v2 book on the same panel and
    window; 4b vs SPY.  Plus the counterfactual 4b' = 4b AND "beats its own EW_ALL on
    Sharpe" — the clause this idea is testing the cost of.
  * Rule 8 (PROTOCOL 8): the book form is chosen on IS <= 2016-12-31 ONLY, under two
    selectors (IS raw Sharpe; IS excess-over-EW_ALL Sharpe), and 2017-01-01.. is read once.
    Reported: OOS CAGR/Sharpe/MaxDD of each pick against the same-window RULES v2 book and
    SPY, and whether the IS panel ordering holds OOS.
  * PART A is a CENSUS of this repository's own committed scripts (regex over their source),
    not a backtest.  It carries no verdict; it sizes the population the queue names.

SURVIVORSHIP (idea 54, carried): B136 and SMALL439 are CURRENT-constituent lists — names
that died were never in them — so every LEVEL on those two panels is biased upward, and the
bias is not equal across panels.  That is precisely why a panel ordering quoted in raw
levels is suspect and why only the paired book-minus-EW_ALL contrast inside one panel is
load-bearing here.  U56 is a fixed ETF/mega-cap list and is the least-biased panel.

Costs 10/25 bps per unit turnover; weights decided at close t applied at t+1 (PROTOCOL 2).
Deterministic, no network.  Writes .census.csv, .grid.csv, .orderings.csv,
.walkforward.csv, .console.txt.
"""
import re
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, band_state, rules_v2_weights, score  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa

STAMP = "2026-09-08_back-fill-the-EWall-column-on-panel-ordering-files_cloud"
OUT = ROOT / "research" / "backtests"
FREQ = "W"
GROSS = 0.75
RUNGS = [10, 25]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

_console = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); _console.append(s)


# ---------------------------------------------------------------- engine twin
def fast_backtest(px, weights, freq=FREQ):
    """Vectorised twin of engine.backtest at ZERO cost, also returning drifted gross."""
    rets = px.pct_change().fillna(0.0).values
    W = weights.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    n = len(px)
    A = np.cumprod(1.0 + rets, axis=0)
    A = np.vstack([np.ones((1, rets.shape[1])), A[:-1]])
    port = np.zeros(n); turn = np.zeros(n); gross = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    starts = np.flatnonzero(mask)
    for i0, i1 in zip(starts, list(starts[1:]) + [n]):
        w = W[i0]
        turn[i0] = np.abs(w - cur).sum()
        u = w[None, :] * (A[i0:i1] / A[i0][None, :])
        cash = 1.0 - w.sum()
        T = u.sum(axis=1) + cash
        port[i0:i1] = (u * rets[i0:i1]).sum(axis=1) / T
        gross[i0:i1] = u.sum(axis=1) / T
        cur = (u[-1] * (1.0 + rets[i1 - 1])) / (T[-1] * (1.0 + port[i1 - 1]))
    return {"returns0": pd.Series(port, index=px.index),
            "turnover": pd.Series(turn, index=px.index),
            "gross": pd.Series(gross, index=px.index)}


def net(res, bps):
    return res["returns0"] - res["turnover"] * bps / 1e4


def mstats(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


# ---------------------------------------------------------------- books
def dg_weights(px, gate, g=GROSS, cols=None):
    """De-grossed: g/N on every admitted priced name, gated weight -> CASH, never re-spread."""
    p = px if cols is None else px[cols]
    e = pd.DataFrame(1.0, index=p.index, columns=p.columns).where(p.notna(), 0.0)
    ew = g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    w = ew.where(gate.reindex_like(ew).fillna(False), 0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


def topn_weights(px, n, cols, vol_scale=False, gate=None, g=GROSS):
    """Rank by the project's composite score; hold the top n at g/n; gated names dropped."""
    p = px[cols]
    s, above, vol20 = score(p, vol_scale=vol_scale)
    elig = s.where(above)
    if gate is not None:
        elig = elig.where(gate.reindex_like(elig).fillna(False))
    rank = elig.rank(axis=1, ascending=False)
    w = (rank <= n).astype(float) * (g / n)
    return w.reindex(columns=px.columns).fillna(0.0)


def lowvol_weights(px, n, cols, g=GROSS):
    p = px[cols]
    vol20 = p.pct_change().rolling(20).std() * np.sqrt(252)
    rank = vol20.rank(axis=1, ascending=True)
    w = (rank <= n).astype(float) * (g / n)
    return w.reindex(columns=px.columns).fillna(0.0)


def build_books(px, cols):
    """The 12 pre-registered book forms on one panel.  SPY is a benchmark, never held."""
    p = px[cols]
    ma = p.rolling(200).mean()
    vol20 = p.pct_change().rolling(20).std() * np.sqrt(252)
    NONE = pd.DataFrame(True, index=p.index, columns=p.columns)
    B = {}
    B["EWALL"] = dg_weights(px, NONE, cols=cols)
    B["RULESV2"] = dg_weights(px, band_state(p, 0.03), cols=cols)
    B["MA200dg"] = dg_weights(px, (p > ma).fillna(False), cols=cols)
    B["BAND6dg"] = dg_weights(px, band_state(p, 0.06), cols=cols)
    B["ABSdg"] = dg_weights(px, (p > p.shift(252)).fillna(False), cols=cols)
    v1 = topn_weights(px, 5, cols, vol_scale=True)
    # RULES v1 also carries the vol20 < 0.60 cap; apply it to the v1 form only
    ok = (vol20 < 0.60).fillna(False).reindex(columns=px.columns).fillna(False)
    B["TOP5V1"] = (v1.where(ok, 0.0)) * (0.15 * 5 / GROSS)   # v1 is 5 x 15% = 75% gross
    B["TOP10"] = topn_weights(px, 10, cols)
    B["TOP20"] = topn_weights(px, 20, cols)
    B["TOP40"] = topn_weights(px, 40, cols)
    B["TOP20V"] = topn_weights(px, 20, cols, vol_scale=True)
    B["TOP20B3"] = topn_weights(px, 20, cols, gate=band_state(p, 0.03))
    B["LOWVOL20"] = lowvol_weights(px, 20, cols)
    return B


BOOKS = ["EWALL", "RULESV2", "MA200dg", "BAND6dg", "ABSdg", "TOP5V1",
         "TOP10", "TOP20", "TOP40", "TOP20V", "TOP20B3", "LOWVOL20"]
PANELS = ["U56", "B136", "SMALL439"]


def panels():
    out = {}
    u = load_universe(); out["U56"] = (u, [c for c in u.columns])
    b = load_universe(broad=True); out["B136"] = (b, [c for c in b.columns])
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    sm = sm[[c for c in sm.columns if c == "SPY" or c not in bad]]
    out["SMALL439"] = (sm, [c for c in sm.columns if c != "SPY"])   # SPY benchmark only
    return out


# ---------------------------------------------------------------- PART A: census
PANEL_PAT = {
    "u56": re.compile(r"\bu56\b|\bU56\b|universe\.json|load_universe\(\)", re.I),
    "broad": re.compile(r"broad\s*=\s*True|\bB136\b|broad136|universe_broad", re.I),
    "small": re.compile(r"small\s*=\s*True|SMALL439|small439|prices_small", re.I),
}
# "publishes an un-ranked control": an EW_ALL-shaped arm label, in the source OR in an
# emitted artefact (csv row/column label, console table, memo).
EWALL_PAT = re.compile(r"EW_?ALL\b|EWall|ew_?all\b|un-?ranked control|NOGATE|no_?gate|"
                       r"n\s*=\s*[\"']?ALL\b|equal[- ]weight[- ]all", re.I)
# an ORDERING-shaped headline: two or three panel names joined by a comparison, or the
# record's own phrases for it.
ORDER_PAT = re.compile(
    r"(u56|b136|broad136|broad|small439|small)\s*(>|>=|/)\s*(u56|b136|broad136|broad|small439|small)"
    r"|panel[- ]order|ordering (is|of|across)|monotone (in|across|U56|the panel)"
    r"|(u56|broad|small439)[^\n]{0,30}\b(beats|above|below|higher than|lower than)\b[^\n]{0,30}(u56|broad|small439|b136)"
    r"|is (a|an) (small[- ]cap|large[- ]cap|ETF|panel) (fact|effect|story)"
    r"|panel property|panel premium|gate premium", re.I)
CSV_HEAD_BYTES = 200_000


def census():
    bt = ROOT / "research" / "backtests"
    rows = []
    for f in sorted(bt.glob("*.py")):
        stem = f.name[:-3]
        src = f.read_text(errors="ignore")
        arte = src
        for ext in (".result.md", ".console.txt", ".md"):
            p = bt / (stem + ext)
            if p.exists():
                arte += "\n" + p.read_text(errors="ignore")
        csv_txt = ""
        for c in bt.glob(stem + "*.csv"):
            with open(c, "rb") as fh:
                csv_txt += fh.read(CSV_HEAD_BYTES).decode("utf-8", "ignore") + "\n"
        hit = {k: bool(v.search(src)) for k, v in PANEL_PAT.items()}
        rows.append(dict(file=f.name, n_panels=sum(hit.values()),
                         u56=hit["u56"], broad=hit["broad"], small=hit["small"],
                         has_ewall_src=bool(EWALL_PAT.search(src)),
                         has_ewall_published=bool(EWALL_PAT.search(arte) or EWALL_PAT.search(csv_txt)),
                         ordering_claim=bool(ORDER_PAT.search(arte)),
                         n_artefacts=len(list(bt.glob(stem + ".*")))))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- main
def main():
    PX = panels()

    # ---------------- GATES
    say("=== GATES ===")
    upx, ucols = PX["U56"]
    st = upx.index[260]
    w2 = rules_v2_weights(upx)
    e_res = engine_backtest(upx, w2, cost_bps=10, freq=FREQ)
    f_res = fast_backtest(upx, w2)
    # engine.backtest carries NaN on day 0 (its w_target is weights.shift(1), so row 0 is
    # NaN) until the first rebalance; every metric in this file starts at index 260, so the
    # twin is asserted on the post-warm-up slice and the pre-warm-up rows are reported.
    g1r = float(np.abs((net(f_res, 10) - e_res["returns"]).loc[st:].values).max())
    g1t = float(np.abs((f_res["turnover"] - e_res["turnover"]).loc[st:].values).max())
    nan0 = int(e_res["returns"].isna().sum())
    say(f"G1 fast_backtest vs engine.backtest (from {st.date()})   max|d returns| = {g1r:.3e}"
        f"   max|d turnover| = {g1t:.3e}   (engine NaN rows before warm-up: {nan0})")
    assert g1r < 1e-12 and g1t < 1e-12, "G1 FAILED"
    B3 = band_state(upx[ucols], 0.03)
    g2 = float(np.abs(dg_weights(upx, B3, cols=ucols).values - w2.values).max())
    say(f"G2 dg_weights(BAND3,0.75) vs baseline.rules_v2_weights   max|diff| = {g2:.3e}")
    assert g2 == 0.0, "G2 FAILED"
    NONEu = pd.DataFrame(True, index=upx.index, columns=ucols)
    ew = dg_weights(upx, NONEu, cols=ucols)
    g3 = float(np.abs(ew.sum(axis=1).iloc[260:] - GROSS).max())
    say(f"G3 EW_ALL nominal gross is exactly {GROSS} on every post-warm-up day   max|dev| = {g3:.3e}")
    assert g3 < 1e-12, "G3 FAILED"

    # ---------------- PART A: census of this repository
    say("\n=== PART A: CENSUS of committed research/backtests/*.py ===")
    C = census()
    C.to_csv(OUT / f"{STAMP}.census.csv", index=False)
    multi = C[C.n_panels >= 2]
    say(f"scripts scanned                                    {len(C)}")
    say(f"multi-panel (>=2 of U56/B136/SMALL439)             {len(multi)}  ({len(multi)/len(C):.1%})")
    say(f"all-three-panel scripts                            {int((C.n_panels == 3).sum())}")
    say(f"  multi-panel with NO EW_ALL token in SOURCE       {int((~multi.has_ewall_src).sum())}"
        f"  ({(~multi.has_ewall_src).mean():.1%})")
    say(f"  multi-panel with NO EW_ALL in ANY published      {int((~multi.has_ewall_published).sum())}"
        f"  ({(~multi.has_ewall_published).mean():.1%})")
    say(f"    artefact (source, memo, console, csv heads)")
    say(f"  multi-panel with an ORDERING-shaped headline     {int(multi.ordering_claim.sum())}"
        f"  ({multi.ordering_claim.mean():.1%})")
    both = multi[multi.ordering_claim & ~multi.has_ewall_published]
    say(f"  ORDERING headline AND no EW_ALL anywhere         {len(both)}"
        f"   <- the population this idea names")
    say("(regex over each script's own source plus its committed .result.md/.console.txt and the"
        f" first {CSV_HEAD_BYTES//1000} KB of each of its .csv artefacts.  A token match is not proof"
        " the file USES the control as a comparand, so read has_ewall_published as an UPPER bound on"
        " coverage and the gap as a LOWER bound.)")

    # ---------------- PART B: common window, all 72 points
    say("\n=== PART B: 12 books x 3 panels x 2 rungs on a COMMON window ===")
    idx = None
    for k in PANELS:
        px, cols = PX[k]
        own = px.index[260:]
        idx = own if idx is None else idx.intersection(own)
    say(f"common window {idx[0].date()} -> {idx[-1].date()}  ({len(idx)} trading days, "
        f"{len(idx)/252:.1f} years)")
    is_idx = idx[idx <= IS_END]; oos_idx = idx[idx >= OOS_START]
    say(f"  IS  {is_idx[0].date()} -> {is_idx[-1].date()}  ({len(is_idx)} days)")
    say(f"  OOS {oos_idx[0].date()} -> {oos_idx[-1].date()}  ({len(oos_idx)} days)")

    RET = {}      # (panel, book, rung) -> net return series on the common window
    GROSSR = {}
    for k in PANELS:
        px, cols = PX[k]
        Bk = build_books(px, cols)
        for b in BOOKS:
            r0 = fast_backtest(px, Bk[b])
            for bps in RUNGS:
                RET[(k, b, bps)] = net(r0, bps).reindex(idx)
            GROSSR[(k, b)] = float(r0["gross"].reindex(idx).mean())
        say(f"  {k}: {len(cols) if k!='SMALL439' else len(cols)} held names, {len(Bk)} books simulated")

    # ONE benchmark for all three panels: SPY out of data/prices.csv (the U56 cache).
    # data/prices_broad.csv carries SPY rounded to a different number of decimals, so the
    # two caches disagree by up to half a cent on some days; the gap is reported, not hidden,
    # and the canonical series is used everywhere so the 4b bar is identical across panels.
    SPY = {k: PX[k][0]["SPY"].pct_change().fillna(0.0).reindex(idx) for k in PANELS}
    spy_ref = SPY["U56"]
    for k in PANELS:
        d = float(np.abs((SPY[k] - spy_ref).fillna(0)).max())
        if d:
            say(f"  NOTE: {k}'s cached SPY differs from data/prices.csv by max {d:.3e} of daily "
                f"return; the prices.csv series is used as the single 4b benchmark.")
    sm_spy = mstats(spy_ref)
    say(f"SPY on the common window: CAGR {sm_spy['CAGR']:.2%}  Sharpe {sm_spy['Sharpe']:.4f}  "
        f"MaxDD {sm_spy['MaxDD']:.2%}  halves {sm_spy['H1']:.3f}/{sm_spy['H2']:.3f}")

    rows = []
    for k in PANELS:
        for b in BOOKS:
            for bps in RUNGS:
                r = RET[(k, b, bps)]
                m = mstats(r)
                mc = mstats(RET[(k, "EWALL", bps)])
                mv2 = mstats(RET[(k, "RULESV2", bps)])
                p4a = (m["H1"] > mv2["H1"] and m["H2"] > mv2["H2"] and m["MaxDD"] >= mv2["MaxDD"])
                p4b = (m["H1"] > sm_spy["H1"] and m["H2"] > sm_spy["H2"]
                       and m["MaxDD"] >= 0.60 * sm_spy["MaxDD"]
                       and m["CAGR"] >= 0.70 * sm_spy["CAGR"])
                rows.append(dict(panel=k, book=b, bps=bps, **{kk: m[kk] for kk in
                                 ("CAGR", "Sharpe", "MaxDD", "H1", "H2")},
                                 gross=GROSSR[(k, b)],
                                 dSharpe_vs_EWALL=m["Sharpe"] - mc["Sharpe"],
                                 dCAGR_vs_EWALL=m["CAGR"] - mc["CAGR"],
                                 pass4a=p4a, pass4b=p4b,
                                 pass4b_plus_beats_EWALL=bool(p4b and m["Sharpe"] > mc["Sharpe"])))
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    say("\nfull grid (all 72 points reported):")
    say(G.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\n4a passes {int(G.pass4a.sum())}/{len(G)}   4b passes {int(G.pass4b.sum())}/{len(G)}"
        f"   4b AND beats own EW_ALL {int(G.pass4b_plus_beats_EWALL.sum())}/{len(G)}")
    lost = G[G.pass4b & ~G.pass4b_plus_beats_EWALL]
    if len(lost):
        say("4b passes DELETED by the 'must beat its own EW_ALL' clause:")
        say(lost[["panel", "book", "bps", "Sharpe", "dSharpe_vs_EWALL"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))

    # every 4b-clearing point read once out of sample (rule 8), whether or not the IS
    # chooser selects it
    say("\n4b-clearing points, read once out of sample (2017-01-01..):")
    mspy_o = mstats(spy_ref.reindex(oos_idx))
    say(f"  SPY OOS: CAGR {mspy_o['CAGR']:.2%}  Sharpe {mspy_o['Sharpe']:.4f}  MaxDD {mspy_o['MaxDD']:.2%}")
    krows = []
    for _, rr in G[G.pass4b].iterrows():
        mo = mstats(RET[(rr.panel, rr.book, rr.bps)].reindex(oos_idx))
        me = mstats(RET[(rr.panel, "EWALL", rr.bps)].reindex(oos_idx))
        mv = mstats(RET[(rr.panel, "RULESV2", rr.bps)].reindex(oos_idx))
        krows.append(dict(panel=rr.panel, book=rr.book, bps=rr.bps,
                          full_Sharpe=rr.Sharpe, H1=rr.H1, H2=rr.H2, MaxDD=rr.MaxDD,
                          OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                          OOS_EWALL_Sharpe=me["Sharpe"], OOS_RULESV2_Sharpe=mv["Sharpe"],
                          OOS_beats_SPY=mo["Sharpe"] > mspy_o["Sharpe"],
                          OOS_beats_EWALL=mo["Sharpe"] > me["Sharpe"],
                          OOS_4b=(mo["Sharpe"] > mspy_o["Sharpe"]
                                  and mo["MaxDD"] >= 0.60 * mspy_o["MaxDD"]
                                  and mo["CAGR"] >= 0.70 * mspy_o["CAGR"])))
    K = pd.DataFrame(krows)
    K.to_csv(OUT / f"{STAMP}.keep.csv", index=False)
    say(K.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------- ORDERINGS
    say("\n=== ORDERINGS: raw vs excess-over-EW_ALL ===")
    orows = []
    for b in BOOKS:
        if b == "EWALL":
            continue
        for bps in RUNGS:
            for met in ("Sharpe", "CAGR"):
                raw = {k: float(G[(G.panel == k) & (G.book == b) & (G.bps == bps)][met].iloc[0])
                       for k in PANELS}
                exc = {k: raw[k] - float(G[(G.panel == k) & (G.book == "EWALL") &
                                           (G.bps == bps)][met].iloc[0]) for k in PANELS}
                ordr = ">".join(sorted(PANELS, key=lambda k: -raw[k]))
                orde = ">".join(sorted(PANELS, key=lambda k: -exc[k]))
                flips = 0; pairs = []
                for i in range(3):
                    for j in range(i + 1, 3):
                        a, c = PANELS[i], PANELS[j]
                        f = np.sign(raw[a] - raw[c]) != np.sign(exc[a] - exc[c])
                        flips += int(f); pairs.append(f"{a}|{c}:{'FLIP' if f else 'same'}")
                orows.append(dict(book=b, bps=bps, metric=met, raw_order=ordr,
                                  excess_order=orde, order_survives=(ordr == orde),
                                  pair_flips=flips, pairs=" ".join(pairs),
                                  **{f"raw_{k}": raw[k] for k in PANELS},
                                  **{f"exc_{k}": exc[k] for k in PANELS}))
    O = pd.DataFrame(orows)
    O.to_csv(OUT / f"{STAMP}.orderings.csv", index=False)
    say(O[["book", "bps", "metric", "raw_order", "excess_order", "order_survives",
           "pair_flips"]].to_string(index=False))
    npair = 3 * len(O)
    say(f"\nfull orderings surviving the restatement: {int(O.order_survives.sum())}/{len(O)}"
        f"  ({O.order_survives.mean():.1%})")
    say(f"pairwise comparisons flipping sign:       {int(O.pair_flips.sum())}/{npair}"
        f"  ({O.pair_flips.sum()/npair:.1%})")
    for met in ("Sharpe", "CAGR"):
        sub = O[O.metric == met]
        say(f"  {met}: orders survive {int(sub.order_survives.sum())}/{len(sub)}, "
            f"pairs flip {int(sub.pair_flips.sum())}/{3*len(sub)}")
    for bps in RUNGS:
        sub = O[O.bps == bps]
        say(f"  {bps} bps: orders survive {int(sub.order_survives.sum())}/{len(sub)}, "
            f"pairs flip {int(sub.pair_flips.sum())}/{3*len(sub)}")
    # the single most-published ordering
    say("\nhow often is the RAW ordering the record's canonical U56>B136>SMALL439?")
    canon = "U56>B136>SMALL439"
    say(f"  raw    {int((O.raw_order == canon).sum())}/{len(O)}"
        f"   excess {int((O.excess_order == canon).sum())}/{len(O)}")

    # ---------------- RULE 8 walk-forward
    say("\n=== RULE 8 WALK-FORWARD (book chosen on IS <= 2016-12-31, OOS read once) ===")
    wrows = []
    for k in PANELS:
        for bps in RUNGS:
            cand = [b for b in BOOKS if b != "EWALL"]
            is_raw = {b: metrics(RET[(k, b, bps)].reindex(is_idx))["Sharpe"] for b in cand}
            is_ew = metrics(RET[(k, "EWALL", bps)].reindex(is_idx))["Sharpe"]
            is_exc = {b: is_raw[b] - is_ew for b in cand}
            for sel, d in (("IS_raw_Sharpe", is_raw), ("IS_excess_over_EWALL", is_exc)):
                pick = max(d, key=d.get)
                ro = RET[(k, pick, bps)].reindex(oos_idx)
                mo = mstats(ro)
                mew = mstats(RET[(k, "EWALL", bps)].reindex(oos_idx))
                mv2 = mstats(RET[(k, "RULESV2", bps)].reindex(oos_idx))
                mspy = mstats(spy_ref.reindex(oos_idx))
                wrows.append(dict(panel=k, bps=bps, selector=sel, pick=pick,
                                  IS_score=d[pick],
                                  OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                  OOS_MaxDD=mo["MaxDD"],
                                  OOS_EWALL_Sharpe=mew["Sharpe"], OOS_EWALL_CAGR=mew["CAGR"],
                                  OOS_RULESV2_Sharpe=mv2["Sharpe"], OOS_SPY_Sharpe=mspy["Sharpe"],
                                  OOS_SPY_CAGR=mspy["CAGR"], OOS_SPY_MaxDD=mspy["MaxDD"],
                                  beats_EWALL_OOS=mo["Sharpe"] > mew["Sharpe"],
                                  beats_SPY_OOS=mo["Sharpe"] > mspy["Sharpe"],
                                  beats_RULESV2_OOS=mo["Sharpe"] > mv2["Sharpe"]))
    W = pd.DataFrame(wrows)
    W.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    say(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\nIS selector disagreement (raw vs excess pick a different book): "
        f"{sum(1 for k in PANELS for bps in RUNGS if W[(W.panel==k)&(W.bps==bps)].pick.nunique()>1)}"
        f"/{len(PANELS)*len(RUNGS)} cells")
    say(f"picks beating their own EW_ALL out of sample: {int(W.beats_EWALL_OOS.sum())}/{len(W)}")
    say(f"picks beating SPY out of sample:              {int(W.beats_SPY_OOS.sum())}/{len(W)}")
    say(f"picks beating live RULES v2 out of sample:    {int(W.beats_RULESV2_OOS.sum())}/{len(W)}")

    # does the IS panel ordering hold OOS, raw and in excess?
    say("\nIS panel ordering vs OOS panel ordering (per book, Sharpe, 10 bps):")
    hold_raw = hold_exc = 0; tot = 0
    for b in BOOKS:
        if b == "EWALL":
            continue
        ir = {k: metrics(RET[(k, b, 10)].reindex(is_idx))["Sharpe"] for k in PANELS}
        orr = {k: metrics(RET[(k, b, 10)].reindex(oos_idx))["Sharpe"] for k in PANELS}
        ie = {k: ir[k] - metrics(RET[(k, "EWALL", 10)].reindex(is_idx))["Sharpe"] for k in PANELS}
        oe = {k: orr[k] - metrics(RET[(k, "EWALL", 10)].reindex(oos_idx))["Sharpe"] for k in PANELS}
        f = lambda d: ">".join(sorted(PANELS, key=lambda k: -d[k]))
        hr = f(ir) == f(orr); he = f(ie) == f(oe)
        hold_raw += hr; hold_exc += he; tot += 1
        say(f"  {b:9s} raw IS {f(ir):24s} OOS {f(orr):24s} {'HOLDS' if hr else 'breaks'}"
            f" | excess IS {f(ie):24s} OOS {f(oe):24s} {'HOLDS' if he else 'breaks'}")
    say(f"  orderings stable IS->OOS: raw {hold_raw}/{tot}, excess {hold_exc}/{tot}")

    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_console) + "\n")
    say(f"\nwrote {STAMP}.census.csv .grid.csv .orderings.csv .walkforward.csv .console.txt")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_console) + "\n")


if __name__ == "__main__":
    main()
