#!/usr/bin/env python3
"""Idea 840 (cloud lane, 2026-09-12) — price an IS-ONLY HEADLINE CONVENTION against the record's
own 4b PASS LIST.

THE DIAGNOSIS THIS RUN IS GROUNDED IN.  Idea 836 found that every committed memo's LEAD number
is a FULL-sample number whose window CONTAINS the 2017+ window the memo then claims to be
validated on: 9 of 12 books move rank on CAGR and 12 of 12 on Sharpe when the headline is
recomputed on <=2016 alone, and rho(FULL MaxDD, POST MaxDD) = +1.0000 EXACTLY at all six splits,
i.e. the third headline number IS the out-of-sample number.  836 killed the READING.  This run
asks the only question that decides whether a PROTOCOL line is worth proposing: if the record had
run an IS-ONLY convention, WHICH of its standing 4b passes would never have been promoted, and
would the surviving list have been BETTER out of sample?

A convention is only worth a PROTOCOL line if it selects books that go on to pass out of window.
So this run scores BOTH conventions against the POST window each of them claims to predict:
  IS-ONLY   promote on [start .. split] alone.  Knows nothing about POST.  Honest but short.
  FULL      promote on [start .. end], the record's published convention.  CONTAINS POST.
and reports the confusion of each against the POST-window 4b verdict at every split and cost.

TWO TUNED PARAMETERS, exactly as the queue allows:
  P1  HEADLINE READING — CAGR / Sharpe / MaxDD (idea 836's three lead numbers) plus FOURB, the
                         PROTOCOL-4b conjunction read as the headline.  4 rungs.
  P2  SPLIT DATE       — 2013-12-31 .. 2018-12-31, 6 rungs.  2016-12-31 is PROTOCOL rule 8's own
                         split and the headline cell.
Cost rung {0, 10, 25} bps is REPORTED at every point, never selected.  No book dial is tuned:
every book runs at the gross, band, n and cadence its own committed memo published.

CONVENTIONS, DECLARED BEFORE ANY NUMBER (C1-C4 copied from ideas 831/832/833/836 so the corpus
and the windows are directly comparable; C5-C8 are this run's own):
  C1  Each book's daily return series is run ONCE at 0 bps (engine.backtest, weights decided at
      close t applied at t+1, the book's own cadence); cost rungs are the exact identity
      r_c = r_0 - turnover * c / 1e4 (gate G3 proves it against a re-run at 10 and 25 bps).
  C2  Warm-up: scoring starts at each panel's px.index[260], as baseline.compare does.
  C3  A book is scored against its own panel's SPY column over the SAME window.
  C4  4b legs are read literally: Sharpe > SPY in BOTH halves of the window, MaxDD >= 0.60 *
      SPY MaxDD (both negative), CAGR >= 0.70 * SPY CAGR (literal, negative SPY CAGR included).
      The rule-8 OOS leg is a FIFTH leg and is only defined for a convention that has a future.
  C5  FULL = [start_260 .. end].  IS = [start_260 .. split].  POST = (split .. end].  IS and
      POST are disjoint and their union is FULL exactly (G4 asserts this row for row).
  C6  "Would never have been promoted" = the book FAILS the 4-leg 4b conjunction on its own IS
      window at that (split, cost), while the record promoted it on the FULL window.
  C7  Rank 1 = best: highest CAGR, highest Sharpe, SHALLOWEST MaxDD; for FOURB, rank on the
      number of 4b legs passed (ties share the average rank, pandas default).
  C8  The 12-book corpus IS the record's standing 4b pass list as idea 836 committed it (MEMO12);
      LIVE (RULES v2 at its live gross 0.75) and V1 are comparands, NOT 4b passes, and are
      excluded from every pass-list count.

PRE-REGISTERED HYPOTHESES (written before the grid ran; all reported either way):
  H_DROP     at the headline cell (split 2016-12-31, 10 bps) at least 4 of the 12 standing 4b
             passes FAIL an IS-only 4b read, i.e. would never have been promoted.
  H_TOP1     the top-1 book by the lead number changes identity between FULL and IS-only at >= 4
             of the 6 splits, on at least one reading (836 found this on CAGR at its own split).
  H_PRED     the IS-only 4b verdict is INFORMATIVE about the POST 4b verdict: P(POST pass |
             IS pass) > P(POST pass | IS fail) at >= 4 of the 6 splits, at 10 bps.
  H_CONTAM   the FULL-sample 4b verdict agrees with the POST verdict MORE often than the IS-only
             verdict does at >= 5 of 6 splits (the contamination signature, since FULL contains
             POST).
  H_STABLE   the IS-only passer SET is not stable across the six splits (at least one book flips).
  H_WF       (rule 8) the book chosen on IS-only Sharpe alone is NOT the OOS-best book by Sharpe
             over 2017+ (836 committed R4 chosen, the worst of the twelve OOS).
  H_COST     the IS-only passer count is monotone non-increasing in cost at every split.

GATES (printed before any new number):
  G1  every book reproduces its own memo's published (CAGR, Sharpe, MaxDD) within
      |dCAGR| <= 1.00pp, |dSharpe| <= 0.060, |dMaxDD| <= 2.00pp (data/prices.csv is re-cached
      daily; ideas 406/574 measured u56 vintage drift at ~3e-3).
  G2  the LIVE book reproduces RULES.md v2's committed 8.63% / 1.202 / -12.05% (bar 6e-3).
  G3  C1's cost identity holds: derived r_c vs a re-run engine.backtest at 10 and 25 bps,
      max |diff| <= 1e-12, on every book.
  G4  C5's split is EXHAUSTIVE and DISJOINT at every split, for every panel.
  G5  the vectorised window metrics reproduce engine.metrics (bar 1e-10) on every book's FULL,
      IS and POST windows at the headline split.

Outputs (all under research/backtests/, all committed):
  .txt            full console log
  .books.csv      one row per (book, split, cost): FULL / IS / POST triples and 4b legs
  .grid.csv       one row per (reading, split, cost): every rank and confusion statistic
  .promote.csv    the promotion table: which of the 12 survives an IS-only read, per cell
  .wf.csv         rule-8 IS/OOS table plus both KEEP paths per book
  .result.md      the answer
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Run: python3 research/backtests/2026-09-12_price-an-IS-ONLY-HEADLINE-CONVENTION-against-the-4b-PASS-LIST_cloud.py
"""
from __future__ import annotations
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import (load_universe, rules_v1_weights, rules_v2_weights, score,  # noqa: E402
                      band_state)                                                # noqa: E402
from engine import backtest, metrics, rebalance_mask                             # noqa: E402

DATE = "2026-09-12"
SLUG = "price-an-IS-ONLY-HEADLINE-CONVENTION-against-the-4b-PASS-LIST"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"
COSTS = [0, 10, 25]
COST = 10                                        # PROTOCOL's rung and the headline
SPLITS = [pd.Timestamp(f"{y}-12-31") for y in (2013, 2014, 2015, 2016, 2017, 2018)]   # P2
HEAD_SPLIT = pd.Timestamp("2016-12-31")
READINGS = ["CAGR", "Sharpe", "MaxDD", "FOURB"]  # P1
MAX_VOL, WARMUP = 0.60, 260
OOS_START = pd.Timestamp("2017-01-01")           # PROTOCOL rule 8
LOG: list[str] = []
pd.set_option("display.width", 250)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def hdr(s):
    P("\n" + "=" * 110 + f"\n{s}\n" + "=" * 110)


# =====================================================================================
# BOOK CONSTRUCTORS — copied verbatim from idea 836's committed script (which copied them from
# 832/831/641/574/804), so the corpus is not silently redefined here.
# =====================================================================================
def comp_rank(px):
    s, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < MAX_VOL)
    return s.where(elig), elig


def topn_weights(px, n=20, gross=0.75, m=0, fixed=False):
    sc, elig = comp_rank(px)
    rank = sc.rank(axis=1, ascending=False)
    if m == 0:
        sel = (rank <= n).fillna(False)
    else:
        R, E = rank.values, elig.values
        held = np.zeros(px.shape[1], bool)
        out = np.zeros(px.shape, bool)
        for i in range(len(px)):
            r_i, e_i = R[i], E[i]
            ok = ~np.isnan(r_i)
            keep = held & e_i & ok & (r_i <= n + m)
            need = n - int(keep.sum())
            if need > 0:
                cand = np.where(e_i & ok & ~keep)[0]
                if len(cand):
                    cand = cand[np.argsort(r_i[cand])][:need]
                    keep[cand] = True
            held = keep
            out[i] = keep
        sel = pd.DataFrame(out, index=px.index, columns=px.columns)
    if fixed:
        return sel.astype(float).mul(gross / n)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.astype(float).div(k, axis=0).mul(gross).fillna(0.0)


def band_ew_respread(px, band, gross):
    e = band_state(px, band).astype(float).where(px.notna(), 0.0)
    k = e.sum(axis=1).replace(0, np.nan)
    return e.div(k, axis=0).mul(gross).fillna(0.0)


def ewall_weights(px, gross=1.00):
    _, elig = comp_rank(px)
    e = elig.astype(float).where(px.notna(), 0.0)
    k = e.sum(axis=1).replace(0, np.nan)
    return e.div(k, axis=0).mul(gross).fillna(0.0)


def shy_residual_weights(px, gross=0.375, sleeve="SHY"):
    W = ewall_weights(px.drop(columns=[sleeve]), gross).reindex(columns=px.columns).fillna(0.0)
    W[sleeve] = (1.0 - W.sum(axis=1)).clip(lower=0.0)
    return W


def breadth_gate_weights(px, gross=1.00, q=0.17, wroll=1008, depth=1.0, freq="W"):
    core = px.drop(columns=["SPY"], errors="ignore")
    above = core > core.rolling(200).mean()
    breadth = above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)
    thr = breadth.rolling(wroll, min_periods=wroll).quantile(q)
    bad = (breadth < thr) & breadth.notna() & thr.notna()
    m = pd.Series(1.0, index=px.index).where(~bad, 1.0 - depth)
    mask = rebalance_mask(px.index, freq)
    m = m.where(mask).ffill().fillna(1.0)
    return ewall_weights(px, gross).mul(m, axis=0)


def ma_respread(px, gross=0.75):
    pm = px.notna()
    ma = (px > px.rolling(200).mean()) & pm
    k = ma.sum(axis=1).replace(0, np.nan)
    return gross * ma.astype(float).div(k, axis=0).fillna(0.0)


def ma_dist_tophalf(px, gross=0.75, q=0.50):
    pm = px.notna()
    dist = (px / px.rolling(200).mean() - 1.0).where(pm)
    rk = dist.rank(axis=1, ascending=False)
    n_priced = dist.notna().sum(axis=1)
    k = np.ceil(q * n_priced).replace(0, np.nan)
    sel = rk.le(k, axis=0).fillna(False) & dist.notna()
    kk = sel.sum(axis=1).replace(0, np.nan)
    return gross * sel.astype(float).div(kk, axis=0).fillna(0.0)


def r6_topn(px, n=20, gross=0.65):
    pm = px.notna()
    r6 = (px / px.shift(126) - 1.0).where(pm)
    rk = r6.rank(axis=1, ascending=False)
    return (rk <= n).astype(float) * (gross / n)


# (key, label, panel, weights_fn, cadence, published (CAGR, Sharpe, MaxDD), memo file)
CORPUS = [
    ("K1", "u56 top20 composite, W, g0.75", "U56",
     lambda px: topn_weights(px, 20, 0.75, 0), "W", (0.1279, 1.064, -0.1831),
     "2026-09-07_u56-top20-g075-4b_C_MEMO.md"),
    ("K2", "u56 top20 + rank buffer m=20, W, g0.75", "U56",
     lambda px: topn_weights(px, 20, 0.75, 20), "W", (None, None, None),
     "2026-09-07_u56-top20-band-m20_4b_B_MEMO.md"),
    ("K3", "u56 top20 DAILY + buffer m=50 (fixed g/n), D, g0.75", "U56",
     lambda px: topn_weights(px, 20, 0.75, 50, fixed=True), "D", (0.1171, 1.1454, -0.1237),
     "2026-09-06_daily-plus-buffer30_PARK_MEMO.md"),
    ("K4", "u56 EW-all 200d-MA gate (band 0), M, g1.00", "U56",
     lambda px: rules_v2_weights(px, 0.0, 1.00), "M", (0.1196, 1.2126, -0.1549),
     "2026-09-08_u56-ewall-magate-fullgross_KEEP_MEMO.md"),
    ("K5", "u56 RULES v2 band 0.03, W, g1.00  [the standing candidate]", "U56",
     lambda px: rules_v2_weights(px, 0.03, 1.00), "W", (0.1159, 1.2055, -0.1591),
     "2026-09-08_u56-band3-fullgross_KEEP_MEMO.md"),
    ("K6", "u56 wide band b=0.12 EW respread, W, g0.75", "U56",
     lambda px: band_ew_respread(px, 0.12, 0.75), "W", (0.1402, 1.2264, -0.1942),
     "2026-09-06_band12-ewall-rw_PARK_MEMO.md"),
    ("K7", "b136 scored-eligible EW, residual in SHY, W, g0.375", "B136",
     lambda px: shy_residual_weights(px, 0.375), "W", (0.0627, 1.1777, -0.1110),
     "2026-09-07_b136-ewall-shy-residual"),
    ("K8", "u56 EW-all, de-gross to ZERO on breadth<q0.17(1008d), W, g1.00", "U56",
     lambda px: breadth_gate_weights(px, 1.00, 0.17), "W", (0.1413, 1.2204, -0.1479),
     "2026-09-10_does-the-BREADTH-gate-4b-pass-live-only-at-gross-1.00_cloud.memo.md"),
    ("R1", "u56 band 0.08, W, g1.00", "U56",
     lambda px: rules_v2_weights(px, 0.08, 1.00), "W", (0.1137, 1.1439, -0.1905),
     "2026-09-11_u56-band008-gross100_4b_cloud_MEMO.md"),
    ("R2", "u56 MA-RESPREAD, W, g0.75", "U56",
     lambda px: ma_respread(px, 0.75), "W", (0.1155, 1.0914, -0.1862),
     "2026-09-11_u56-marsrespread-gross075_4b_C_MEMO.md"),
    ("R3", "u56 MA-DISTANCE top-half, M, g0.75", "U56",
     lambda px: ma_dist_tophalf(px, 0.75, 0.50), "M", (0.1547, 1.2359, -0.1980),
     "2026-09-11_4b-candidate-U56-MA-DISTANCE-TOP-HALF-monthly_memo.md"),
    ("R4", "b136 R6-top20 (de-gross), W, g0.65", "B136",
     lambda px: r6_topn(px, 20, 0.65), "W", (0.1499, 1.1264, -0.1943),
     "2026-09-12_b136-r620-gross065-W_4b_C_MEMO.md"),
    ("LIVE", "RULES v2 LIVE band 0.03, W, g0.75  [comparand, NOT a 4b pass]", "U56",
     lambda px: rules_v2_weights(px, 0.03, 0.75), "W", (0.0863, 1.202, -0.1205), "RULES.md v2"),
    ("V1", "RULES v1 retired, W  [comparand, NOT a 4b pass]", "U56",
     rules_v1_weights, "W", (None, None, None), "RULES.md v1"),
]
PASSLIST = ["K1", "K2", "K3", "K4", "K5", "K6", "K7", "K8", "R1", "R2", "R3", "R4"]   # C8
COMPARANDS = ["LIVE", "V1"]
KEYS = PASSLIST + COMPARANDS


# =====================================================================================
# metrics
# =====================================================================================
def w_metrics(r: np.ndarray):
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    sd = r.std(ddof=1)
    sharpe = (r.mean() * 252.0) / (sd * np.sqrt(252.0)) if sd > 0 else np.nan
    mdd = float(np.min(eq / np.maximum.accumulate(eq) - 1.0))
    return float(cagr), float(sharpe), mdd


def sharpe_of(r: np.ndarray):
    sd = r.std(ddof=1)
    return float((r.mean() * 252.0) / (sd * np.sqrt(252.0))) if sd > 0 else np.nan


def fourb_legs(rb: np.ndarray, rs: np.ndarray):
    """C4: the four window-local 4b legs (halves x2, DD cap, CAGR floor) for book vs SPY."""
    h = len(rb) // 2
    b_h1, b_h2 = sharpe_of(rb[:h]), sharpe_of(rb[h:])
    s_h1, s_h2 = sharpe_of(rs[:h]), sharpe_of(rs[h:])
    bc, bs, bd = w_metrics(rb)
    sc, ss, sd_ = w_metrics(rs)
    return dict(h1=bool(b_h1 > s_h1), h2=bool(b_h2 > s_h2),
                dd=bool(bd >= 0.60 * sd_), cagr=bool(bc >= 0.70 * sc),
                CAGR=bc, Sharpe=bs, MaxDD=bd, spy_CAGR=sc, spy_Sharpe=ss, spy_MaxDD=sd_,
                b_h1=b_h1, b_h2=b_h2, s_h1=s_h1, s_h2=s_h2)


def npass(d):
    return int(d["h1"]) + int(d["h2"]) + int(d["dd"]) + int(d["cagr"])


def allpass(d):
    return d["h1"] and d["h2"] and d["dd"] and d["cagr"]


# =====================================================================================
def main():
    t_all = time.time()
    hdr("PANELS")
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    starts = {}
    for k, px in panels.items():
        starts[k] = px.index[WARMUP]
        P(f"  {k:5s} {px.shape[0]} rows x {px.shape[1]} cols  {px.index[0].date()} .. "
          f"{px.index[-1].date()}   scoring starts {starts[k].date()}")

    # ---------------- build every book ONCE at 0 bps (C1) ----------------
    hdr("BUILD — one engine.backtest per book at 0 bps; cost rungs by the C1 identity")
    raw = {}
    for key, label, pan, wf, freq, pub, memo in CORPUS:
        px = panels[pan]
        t0 = time.time()
        res = backtest(px, wf(px), cost_bps=0, freq=freq)
        raw[key] = dict(r0=res["returns"], to=res["turnover"], panel=pan, freq=freq,
                        label=label, pub=pub, memo=memo)
        P(f"  {key:5s} {label:60s} {pan:5s} {freq}  ({time.time()-t0:.1f}s)")

    def series(key, cost):
        d = raw[key]
        s = d["r0"] - d["to"] * cost / 1e4
        return s.loc[starts[d["panel"]]:]

    def spy(key, cost=None):
        d = raw[key]
        return panels[d["panel"]]["SPY"].pct_change().fillna(0.0).loc[starts[d["panel"]]:]

    # ================================ GATES ================================
    hdr("GATES — printed BEFORE any new number")
    gate_rows = []

    # G3 first: the cost identity every later number rests on.
    g3 = 0.0
    for key, label, pan, wf, freq, pub, memo in CORPUS:
        px = panels[pan]
        W = wf(px)
        for c in (10, 25):
            rr = backtest(px, W, cost_bps=c, freq=freq)["returns"]
            g3 = max(g3, float((rr - (raw[key]["r0"] - raw[key]["to"] * c / 1e4)).abs().max()))
    P(f"  G3 cost identity r_c = r_0 - turnover*c/1e4 over all {len(CORPUS)} books x "
      f"(10, 25) bps: max |diff| = {g3:.3e}   {'PASS' if g3 <= 1e-12 else 'FAIL'}")
    gate_rows.append(dict(gate="G3_cost_identity", value=g3, bar=1e-12, ok=g3 <= 1e-12))

    # G1 / G2
    g1_ok, worst = True, []
    for key, label, pan, wf, freq, pub, memo in CORPUS:
        if pub[0] is None:
            continue
        c, s, d = w_metrics(series(key, COST).values)
        dc, ds, dd = abs(c - pub[0]) * 100, abs(s - pub[1]), abs(d - pub[2]) * 100
        ok = dc <= 1.00 and ds <= 0.060 and dd <= 2.00
        g1_ok &= ok
        worst.append((key, dc, ds, dd, ok))
        P(f"  G1 {key:5s} got {c:7.2%} / {s:7.4f} / {d:8.2%}  pub {pub[0]:7.2%} / {pub[1]:7.4f} / "
          f"{pub[2]:8.2%}   d = {dc:.2f}pp / {ds:.4f} / {dd:.2f}pp  {'ok' if ok else 'FAIL'}")
    gate_rows.append(dict(gate="G1_published_triples", value=max(w[1] for w in worst),
                          bar=1.00, ok=g1_ok))
    P(f"  G1 {'PASS' if g1_ok else 'FAIL'}")
    lc, ls, ld = w_metrics(series("LIVE", COST).values)
    g2 = max(abs(lc - 0.0863), abs(ls - 1.202), abs(ld - (-0.1205)))
    P(f"  G2 LIVE RULES v2 @10bps {lc:.4%} / {ls:.4f} / {ld:.4%} vs committed 8.63% / 1.202 / "
      f"-12.05%  max|d| = {g2:.3e}  {'PASS' if g2 <= 6e-3 else 'FAIL'}")
    gate_rows.append(dict(gate="G2_live_rules_v2", value=g2, bar=6e-3, ok=g2 <= 6e-3))

    # G4 exhaustive / disjoint
    g4_ok = True
    for pan, px in panels.items():
        idx = px.loc[starts[pan]:].index
        for sp in SPLITS:
            a, b = idx[idx <= sp], idx[idx > sp]
            g4_ok = g4_ok and bool(len(a) + len(b) == len(idx)) and bool(a.union(b).equals(idx)) \
                and len(a) > 0 and len(b) > 0
    P(f"  G4 IS/POST exhaustive and disjoint at all {len(SPLITS)} splits x {len(panels)} panels: "
      f"{'PASS' if g4_ok else 'FAIL'}")
    gate_rows.append(dict(gate="G4_window_partition", value=float(g4_ok), bar=1.0, ok=g4_ok))

    # G5 vectorised metrics == engine.metrics
    g5 = 0.0
    for key in KEYS:
        r = series(key, COST)
        for win in ("FULL", "IS", "POST"):
            rr = r if win == "FULL" else (r.loc[:HEAD_SPLIT] if win == "IS"
                                          else r.loc[HEAD_SPLIT + pd.Timedelta(days=1):])
            m = metrics(rr)
            v = w_metrics(rr.values)
            g5 = max(g5, abs(v[0] - m["CAGR"]), abs(v[1] - m["Sharpe"]), abs(v[2] - m["MaxDD"]))
    P(f"  G5 w_metrics vs engine.metrics over {len(KEYS)} books x 3 windows: max |diff| = "
      f"{g5:.3e}  {'PASS' if g5 <= 1e-10 else 'FAIL'}")
    gate_rows.append(dict(gate="G5_metrics_identity", value=g5, bar=1e-10, ok=g5 <= 1e-10))
    pd.DataFrame(gate_rows).to_csv(f"{OUT}.gates.csv", index=False)
    P(f"\n  GATES: {sum(1 for g in gate_rows if g['ok'])} of {len(gate_rows)} PASS")

    # ================== SECTION 1: the book x split x cost table ==================
    hdr("SECTION 1 — every book on every window: FULL / IS / POST triples and 4b legs "
        f"({len(KEYS)} books x {len(SPLITS)} splits x {len(COSTS)} costs, all reported)")
    rows = []
    for cost in COSTS:
        for key in KEYS:
            r = series(key, cost)
            s = spy(key)
            r, s = r.align(s, join="inner")
            full = fourb_legs(r.values, s.values)
            oos_b, oos_s = r.loc[OOS_START:], s.loc[OOS_START:]
            oos = fourb_legs(oos_b.values, oos_s.values)
            for sp in SPLITS:
                is_b, is_s = r.loc[:sp], s.loc[:sp]
                po_b, po_s = r.loc[sp + pd.Timedelta(days=1):], s.loc[sp + pd.Timedelta(days=1):]
                IS = fourb_legs(is_b.values, is_s.values)
                PO = fourb_legs(po_b.values, po_s.values)
                rows.append(dict(
                    book=key, label=raw[key]["label"], panel=raw[key]["panel"],
                    freq=raw[key]["freq"], cost=cost, split=sp.date(),
                    n_full=len(r), n_is=len(is_b), n_post=len(po_b),
                    full_CAGR=full["CAGR"], full_Sharpe=full["Sharpe"], full_MaxDD=full["MaxDD"],
                    is_CAGR=IS["CAGR"], is_Sharpe=IS["Sharpe"], is_MaxDD=IS["MaxDD"],
                    post_CAGR=PO["CAGR"], post_Sharpe=PO["Sharpe"], post_MaxDD=PO["MaxDD"],
                    oos_CAGR=oos["CAGR"], oos_Sharpe=oos["Sharpe"], oos_MaxDD=oos["MaxDD"],
                    spy_full_CAGR=full["spy_CAGR"], spy_full_Sharpe=full["spy_Sharpe"],
                    spy_full_MaxDD=full["spy_MaxDD"],
                    spy_is_CAGR=IS["spy_CAGR"], spy_is_Sharpe=IS["spy_Sharpe"],
                    spy_post_CAGR=PO["spy_CAGR"], spy_post_Sharpe=PO["spy_Sharpe"],
                    full_h1_Sharpe=full["b_h1"], full_h2_Sharpe=full["b_h2"],
                    spy_full_h1_Sharpe=full["s_h1"], spy_full_h2_Sharpe=full["s_h2"],
                    oos_h1_Sharpe=oos["b_h1"], oos_h2_Sharpe=oos["b_h2"],
                    spy_oos_h1_Sharpe=oos["s_h1"], spy_oos_h2_Sharpe=oos["s_h2"],
                    full_4b_legs=npass(full), is_4b_legs=npass(IS), post_4b_legs=npass(PO),
                    full_4b=allpass(full), is_4b=allpass(IS), post_4b=allpass(PO),
                    full_h1=full["h1"], full_h2=full["h2"], full_dd=full["dd"],
                    full_cagr=full["cagr"],
                    is_h1=IS["h1"], is_h2=IS["h2"], is_dd=IS["dd"], is_cagr=IS["cagr"],
                    post_h1=PO["h1"], post_h2=PO["h2"], post_dd=PO["dd"], post_cagr=PO["cagr"],
                    oos_4b=allpass(oos), oos_sharpe_gt_spy=bool(oos["Sharpe"] > oos["spy_Sharpe"]),
                ))
    B = pd.DataFrame(rows)
    B.to_csv(f"{OUT}.books.csv", index=False)
    head = B[(B.cost == COST) & (B.split == HEAD_SPLIT.date())].set_index("book")
    P("\n  HEADLINE CELL (10 bps, split 2016-12-31).  FULL is the record's published convention; "
      "IS knows nothing after the split.")
    show = head[["full_CAGR", "full_Sharpe", "full_MaxDD", "full_4b", "is_CAGR", "is_Sharpe",
                 "is_MaxDD", "is_4b", "is_4b_legs", "post_CAGR", "post_Sharpe", "post_MaxDD",
                 "post_4b"]]
    P(show.to_string(float_format=lambda x: f"{x:.4f}"))
    P(f"\n  SPY over the same windows: FULL {head.spy_full_CAGR.iloc[0]:.2%} / "
      f"{head.spy_full_Sharpe.iloc[0]:.4f} / {head.spy_full_MaxDD.iloc[0]:.2%}")

    # ================== SECTION 2: the promotion table ==================
    hdr("SECTION 2 — WHICH OF THE 12 WOULD NEVER HAVE BEEN PROMOTED (C6), every cell reported")
    prom = []
    for cost in COSTS:
        for sp in SPLITS:
            sub = B[(B.cost == cost) & (B.split == sp.date())].set_index("book")
            pl = sub.loc[PASSLIST]
            never = [k for k in PASSLIST if pl.loc[k, "full_4b"] and not pl.loc[k, "is_4b"]]
            new = [k for k in PASSLIST if pl.loc[k, "is_4b"] and not pl.loc[k, "full_4b"]]
            prom.append(dict(cost=cost, split=sp.date(),
                             full_pass=int(pl.full_4b.sum()), is_pass=int(pl.is_4b.sum()),
                             post_pass=int(pl.post_4b.sum()),
                             never_promoted=";".join(never), n_never=len(never),
                             newly_promoted=";".join(new), n_new=len(new),
                             is_passers=";".join([k for k in PASSLIST if pl.loc[k, "is_4b"]])))
    PR = pd.DataFrame(prom)
    PR.to_csv(f"{OUT}.promote.csv", index=False)
    P(PR.to_string(index=False))
    h = PR[(PR.cost == COST) & (PR.split == HEAD_SPLIT.date())].iloc[0]
    P(f"\n  HEADLINE: at 10 bps / split 2016-12-31 the FULL convention promotes "
      f"{h.full_pass} of 12, the IS-ONLY convention promotes {h.is_pass} of 12.")
    P(f"  WOULD NEVER HAVE BEEN PROMOTED under IS-only: {h.never_promoted or '(none)'} "
      f"({h.n_never} books)")
    P(f"  Promoted by IS-only but NOT by FULL: {h.newly_promoted or '(none)'} ({h.n_new} books)")

    # ================== SECTION 3: does either convention predict POST? ==================
    hdr("SECTION 3 — the only question that licenses a PROTOCOL line: does the convention "
        "PREDICT the POST-window 4b verdict?")
    grid = []
    for cost in COSTS:
        for sp in SPLITS:
            sub = B[(B.cost == cost) & (B.split == sp.date())].set_index("book").loc[PASSLIST]
            post = sub.post_4b.astype(bool)
            for conv, col in (("IS", "is_4b"), ("FULL", "full_4b")):
                v = sub[col].astype(bool)
                agree = float((v == post).mean())
                p_giv_pass = float(post[v].mean()) if v.any() else np.nan
                p_giv_fail = float(post[~v].mean()) if (~v).any() else np.nan
                lift = (p_giv_pass - p_giv_fail) if not (np.isnan(p_giv_pass) or
                                                         np.isnan(p_giv_fail)) else np.nan
                grid.append(dict(kind="confusion", reading="FOURB", conv=conv, cost=cost,
                                 split=sp.date(), agree=agree, p_post_given_pass=p_giv_pass,
                                 p_post_given_fail=p_giv_fail, lift=lift,
                                 n_pass=int(v.sum()), n_post=int(post.sum())))
            # rank / top-1 movement on the three lead numbers, and on the 4b leg count
            for rd in READINGS:
                if rd == "FOURB":
                    f, i_, p_ = sub.full_4b_legs, sub.is_4b_legs, sub.post_4b_legs
                else:
                    f, i_ = sub[f"full_{rd}"], sub[f"is_{rd}"]
                    p_ = sub[f"post_{rd}"]
                rf, ri, rp = (x.rank(ascending=False) for x in (f, i_, p_))
                top_f, top_i, top_p = rf.idxmin(), ri.idxmin(), rp.idxmin()
                grid.append(dict(kind="rank", reading=rd, conv="IS_vs_FULL", cost=cost,
                                 split=sp.date(),
                                 rho_full_is=float(rf.corr(ri)),      # Pearson on ranks == Spearman
                                 rho_full_post=float(rf.corr(rp)),
                                 rho_is_post=float(ri.corr(rp)),
                                 max_rank_move=float((rf - ri).abs().max()),
                                 n_moved=int(((rf - ri).abs() > 0).sum()),
                                 top1_full=top_f, top1_is=top_i, top1_post=top_p,
                                 top1_changed=bool(top_f != top_i),
                                 is_top1_is_post_top1=bool(top_i == top_p)))
    G = pd.DataFrame(grid)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    C = G[G.kind == "confusion"]
    P(C[["conv", "cost", "split", "agree", "p_post_given_pass", "p_post_given_fail", "lift",
         "n_pass", "n_post"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    R = G[G.kind == "rank"]
    P("\n  RANK MOVEMENT (12 books, rank 1 = best):")
    P(R[["reading", "cost", "split", "rho_full_is", "rho_full_post", "rho_is_post",
         "max_rank_move", "n_moved", "top1_full", "top1_is", "top1_post",
         "top1_changed"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ================== SECTION 4: rule 8 (mandatory) ==================
    hdr("SECTION 4 — PROTOCOL rule 8 walk-forward.  Convention chosen on IS (<=2016-12-31) "
        "ALONE; OOS 2017-01-01..2026-09-11 read exactly ONCE.")
    wf = []
    for key in KEYS:
        r = series(key, COST)
        s = spy(key)
        r, s = r.align(s, join="inner")
        i_b, i_s = r.loc[:HEAD_SPLIT], s.loc[:HEAD_SPLIT]
        o_b, o_s = r.loc[OOS_START:], s.loc[OOS_START:]
        IS, OO = fourb_legs(i_b.values, i_s.values), fourb_legs(o_b.values, o_s.values)
        FU = fourb_legs(r.values, s.values)
        # 4a: vs the LIVE book on its own panel, both halves + MaxDD no worse
        lr = series("LIVE", COST)
        lr = lr.reindex(r.index).dropna()
        rr = r.reindex(lr.index)
        hh = len(rr) // 2
        a_h1 = sharpe_of(rr.values[:hh]) > sharpe_of(lr.values[:hh])
        a_h2 = sharpe_of(rr.values[hh:]) > sharpe_of(lr.values[hh:])
        a_dd = w_metrics(rr.values)[2] >= w_metrics(lr.values)[2]
        wf.append(dict(book=key, label=raw[key]["label"], panel=raw[key]["panel"],
                       is_CAGR=IS["CAGR"], is_Sharpe=IS["Sharpe"], is_MaxDD=IS["MaxDD"],
                       oos_CAGR=OO["CAGR"], oos_Sharpe=OO["Sharpe"], oos_MaxDD=OO["MaxDD"],
                       oos_spy_CAGR=OO["spy_CAGR"], oos_spy_Sharpe=OO["spy_Sharpe"],
                       oos_spy_MaxDD=OO["spy_MaxDD"],
                       oos_h1=OO["h1"], oos_h2=OO["h2"], oos_dd=OO["dd"], oos_cagr=OO["cagr"],
                       oos_4b=allpass(OO), is_4b=allpass(IS), full_4b=allpass(FU),
                       keep_4a=bool(a_h1 and a_h2 and a_dd),
                       keep_4b=bool(allpass(FU) and allpass(OO)),
                       a_h1=bool(a_h1), a_h2=bool(a_h2), a_dd=bool(a_dd)))
    W = pd.DataFrame(wf).set_index("book")
    W.to_csv(f"{OUT}.wf.csv")
    P(W[["is_Sharpe", "is_CAGR", "is_MaxDD", "oos_CAGR", "oos_Sharpe", "oos_MaxDD", "oos_4b",
         "is_4b", "full_4b", "keep_4a", "keep_4b"]].to_string(float_format=lambda x: f"{x:.4f}"))
    P(f"\n  SPY OOS: {W.oos_spy_CAGR.iloc[0]:.2%} / {W.oos_spy_Sharpe.iloc[0]:.4f} / "
      f"{W.oos_spy_MaxDD.iloc[0]:.2%}   (U56 panel; B136 SPY column is the same series)")
    P(f"  RULES v2 LIVE OOS: {W.loc['LIVE','oos_CAGR']:.2%} / {W.loc['LIVE','oos_Sharpe']:.4f} / "
      f"{W.loc['LIVE','oos_MaxDD']:.2%}")
    P(f"  RULES v1      OOS: {W.loc['V1','oos_CAGR']:.2%} / {W.loc['V1','oos_Sharpe']:.4f} / "
      f"{W.loc['V1','oos_MaxDD']:.2%}")
    picks = {}
    for rd in READINGS:
        pl = W.loc[PASSLIST]
        col = {"CAGR": "is_CAGR", "Sharpe": "is_Sharpe", "MaxDD": "is_MaxDD",
               "FOURB": "is_4b"}[rd]
        if rd == "FOURB":
            cand = pl[pl.is_4b] if pl.is_4b.any() else pl
            pick = cand.is_Sharpe.idxmax()          # tie-break inside the passer set on IS Sharpe
        else:
            pick = pl[col].idxmax()
        picks[rd] = pick
        P(f"  rule-8 PICK by IS-only {rd:6s} = {pick:4s} -> OOS {W.loc[pick,'oos_CAGR']:7.2%} / "
          f"{W.loc[pick,'oos_Sharpe']:.4f} / {W.loc[pick,'oos_MaxDD']:8.2%}   "
          f"(OOS-best by Sharpe is {W.loc[PASSLIST].oos_Sharpe.idxmax()} at "
          f"{W.loc[PASSLIST].oos_Sharpe.max():.4f})")

    # ================== SECTION 5: hypotheses ==================
    hdr("SECTION 5 — the seven pre-registered hypotheses")
    res = {}
    res["H_DROP"] = (int(h.n_never) >= 4, f"{h.n_never} of 12 fail an IS-only 4b read at the "
                                          f"headline cell (bar >= 4)")
    t1 = R[(R.cost == COST)].groupby("reading").top1_changed.sum()
    res["H_TOP1"] = (bool((t1 >= 4).any()),
                     "top-1 changes identity FULL->IS at " +
                     ", ".join(f"{k} {int(v)}/6" for k, v in t1.items()) + " (bar >=4 on any)")
    cis = C[(C.conv == "IS") & (C.cost == COST)]
    n_lift = int((cis.lift > 0).sum())
    res["H_PRED"] = (n_lift >= 4, f"P(POST|IS pass) > P(POST|IS fail) at {n_lift} of 6 splits "
                                  f"(lifts {', '.join(f'{x:+.3f}' for x in cis.lift)})")
    cf = C[(C.conv == "FULL") & (C.cost == COST)].set_index("split")
    ci = cis.set_index("split")
    n_cont = int((cf.agree > ci.agree).sum())
    res["H_CONTAM"] = (n_cont >= 5, f"FULL agrees with POST more often than IS does at "
                                    f"{n_cont} of 6 splits (FULL "
                                    f"{', '.join(f'{x:.2f}' for x in cf.agree)} vs IS "
                                    f"{', '.join(f'{x:.2f}' for x in ci.agree)})")
    sets = PR[PR.cost == COST].is_passers.tolist()
    res["H_STABLE"] = (len(set(sets)) > 1, f"{len(set(sets))} distinct IS-passer sets over the 6 "
                                           f"splits (bar > 1 = unstable)")
    best = W.loc[PASSLIST].oos_Sharpe.idxmax()
    res["H_WF"] = (picks["Sharpe"] != best, f"IS-Sharpe pick {picks['Sharpe']} vs OOS-best "
                                            f"{best} (H passes if they DIFFER)")
    mono = all(PR[PR.split == sp.date()].sort_values("cost").is_pass.is_monotonic_decreasing
               for sp in SPLITS)
    res["H_COST"] = (mono, "IS passer count monotone non-increasing in cost at every split"
                           if mono else "IS passer count NOT monotone in cost at some split")
    for k, (ok, txt) in res.items():
        P(f"  {k:10s} {'PASS' if ok else 'FAIL'}  — {txt}")
    npass_h = sum(1 for ok, _ in res.values() if ok)
    P(f"\n  {npass_h} of {len(res)} hypotheses PASS")

    # ================== SECTION 6: verdict + the proposed PROTOCOL line ==================
    hdr("SECTION 6 — VERDICT")
    ip = int(h.is_pass)
    fp = int(h.full_pass)
    lift_med = float(np.nanmedian(cis.lift))
    P(f"  FULL convention promotes {fp} of 12 at the headline cell; IS-ONLY promotes {ip}.")
    P(f"  IS-only lift on the POST verdict: median {lift_med:+.4f} over the 6 splits "
      f"({n_lift} of 6 positive).")
    P(f"  Contamination: FULL beats IS on POST agreement at {n_cont} of 6 splits.")
    P(f"  Rule 8: the IS-Sharpe pick is {picks['Sharpe']} (OOS Sharpe "
      f"{W.loc[picks['Sharpe'],'oos_Sharpe']:.4f}); OOS-best is {best} "
      f"({W.loc[best,'oos_Sharpe']:.4f}); SPY OOS {W.oos_spy_Sharpe.iloc[0]:.4f}.")
    P("  NO new KEEP is claimed by this run: every book in the corpus is already committed, no "
      "dial was tuned, and nothing is promoted.")

    lines = []
    lines.append(f"# Idea 840 — price an IS-ONLY HEADLINE CONVENTION against the record's own "
                 f"4b PASS LIST ({DATE}, cloud lane)\n")
    lines.append(f"**Corpus** {len(PASSLIST)} committed 4b passes (MEMO12, idea 836's set) plus "
                 f"LIVE and V1 as comparands. **Params** P1 reading x P2 split; "
                 f"{len(READINGS)}x{len(SPLITS)}x{len(COSTS)} = "
                 f"{len(READINGS)*len(SPLITS)*len(COSTS)} grid points, all reported.\n")
    lines.append(f"**Gates** {sum(1 for g in gate_rows if g['ok'])} of {len(gate_rows)} PASS "
                 f"(G3 cost identity {g3:.1e}, G1 published triples, G2 LIVE {g2:.1e}, "
                 f"G4 partition, G5 metrics {g5:.1e}).\n")
    lines.append(f"**Headline (10 bps, split 2016-12-31)** FULL promotes {fp} of 12, IS-ONLY "
                 f"promotes {ip}. Would never have been promoted: "
                 f"`{h.never_promoted or '(none)'}`. Promoted only by IS-only: "
                 f"`{h.newly_promoted or '(none)'}`.\n")
    lines.append(f"**Does the convention predict?** IS-only lift P(POST|pass)-P(POST|fail): "
                 f"median {lift_med:+.4f}, positive at {n_lift} of 6 splits. FULL out-agrees "
                 f"IS on the POST verdict at {n_cont} of 6 splits — the contamination signature, "
                 f"since FULL contains POST.\n")
    lines.append(f"**Rule 8** IS-Sharpe pick {picks['Sharpe']} OOS "
                 f"{W.loc[picks['Sharpe'],'oos_CAGR']:.2%} / "
                 f"{W.loc[picks['Sharpe'],'oos_Sharpe']:.4f} / "
                 f"{W.loc[picks['Sharpe'],'oos_MaxDD']:.2%}; OOS-best {best} "
                 f"{W.loc[best,'oos_CAGR']:.2%} / {W.loc[best,'oos_Sharpe']:.4f} / "
                 f"{W.loc[best,'oos_MaxDD']:.2%}; RULES v2 "
                 f"{W.loc['LIVE','oos_CAGR']:.2%} / {W.loc['LIVE','oos_Sharpe']:.4f} / "
                 f"{W.loc['LIVE','oos_MaxDD']:.2%}; RULES v1 {W.loc['V1','oos_CAGR']:.2%} / "
                 f"{W.loc['V1','oos_Sharpe']:.4f}; SPY {W.oos_spy_CAGR.iloc[0]:.2%} / "
                 f"{W.oos_spy_Sharpe.iloc[0]:.4f} / {W.oos_spy_MaxDD.iloc[0]:.2%}.\n")
    lines.append(f"**KEEP paths** 4a {int(W.loc[PASSLIST].keep_4a.sum())} of 12; "
                 f"4b (full AND OOS) {int(W.loc[PASSLIST].keep_4b.sum())} of 12.\n")
    lines.append(f"**Hypotheses** {npass_h} of {len(res)} PASS: " +
                 "; ".join(f"{k} {'PASS' if v[0] else 'FAIL'}" for k, v in res.items()) + "\n")
    (Path(f"{OUT}.result.md")).write_text("\n".join(lines))
    Path(f"{OUT}.txt").write_text("\n".join(LOG) + "\n")
    P(f"\n  wrote {OUT.name}.{{txt,books.csv,grid.csv,promote.csv,wf.csv,gates.csv,result.md}}")
    P(f"  total {time.time()-t_all:.1f}s")
    Path(f"{OUT}.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
