#!/usr/bin/env python3
"""Idea 831 (lane B, 2026-09-12) — how many of the record's COMMITTED 4b PASSES survive
their OWN ENTRY-DATE CENSUS?

THE DIAGNOSIS THIS RUN IS GROUNDED IN.  Every 4b verdict in LEADERBOARD.md is computed on
ONE fixed window (2009-01-13 .. today) with ONE half split.  Idea 828 scored five fixed-window
4b passers on every entry date and found each fails for at least 60% of them; idea 829 found
the same for the standing candidate (0.3977 at a 3-year horizon).  Neither run scored the
record's 4b column as a whole.  This run does: it takes the record's committed, reconstructible
4b passes — the MEMO corpus, i.e. every KEEP/4b candidate the record filed a memo for and that
can be rebuilt from committed prices alone — and publishes each claim's entry-date pass share
BESIDE the claim.

TWO TUNED PARAMETERS, exactly as the queue allows:
  P1  CLAIM SET   — MEMO8 (the gate-verified corpus K1..K8 of ideas 641/574, each at its OWN
                    memo gross) or MEMO12 (MEMO8 + the four further reconstructible 4b memos
                    filed 2026-09-11/12: R1..R4).  Both reported in full.
  P2  HORIZON H   — 756d (3y, the queue's ask) or 1260d (5y).  Both reported in full.
Entry spacing s in {21, 63} is REPORTED-NOT-SELECTED at every cell, as is the cost rung.
No book dial is tuned here: every book is run at the gross, band, n and cadence its own
committed memo published.

CONVENTIONS, DECLARED BEFORE ANY NUMBER (C1-C5 copied from idea 829 so the two censuses are
directly comparable; C6 is this run's own):
  C1  Each book's daily return series is run ONCE over the full sample (engine.backtest,
      weights decided at close t applied at t+1, cost_bps=10, the book's own cadence) and
      windows are SLICES of it: the entrant JOINS a running book already holding its weights.
  C2  A window's 4b legs are read WINDOW-LOCALLY against SPY over the SAME window: Sharpe
      (full window) > SPY, Sharpe in BOTH window-local halves > SPY's, MaxDD >= 0.6 x SPY's
      MaxDD, CAGR >= 0.7 x SPY's CAGR.  PASS_4b requires all four.
  C3  The CAGR floor is applied LITERALLY, including where SPY's window CAGR is negative
      (0.7 x a negative number is ABOVE it, i.e. strictly harder).  Counted, with sensitivity
      S2 = floor becomes SPY's own CAGR in those windows.
  C4  Warm-up: entry dates start at each panel's px.index[260], as baseline.compare does.
  C5  A window must lie wholly inside the sample; the last entry is len(px) - H.
  C6  A B136 book is scored against the B136 panel's own SPY column; a U56 book against U56's.
      Both are the same instrument, so the comparand is identical by construction; the
      statement is that no book is scored against another panel's benchmark.

PRE-REGISTERED HYPOTHESES (written before the grid was run; all reported either way):
  H_NONE      at the headline cell (MEMO8, H=756, s=21) NO committed 4b pass reaches an
              entry-date pass share of 0.80.
  H_MAJORITY  at least one committed 4b pass reaches 0.50 at the headline cell.
  H_RANK      the record's published fixed-window number ORDERS the entry-date share:
              Spearman(full-sample Sharpe, entry share) >= +0.70 over the claim set
              (statistic and n published beside it, per idea 564's proposal).
  H_HORIZON   every book's share is HIGHER at H=1260 than at H=756 (idea 828's finding that
              HORIZON, not form, is the binding axis).
  H_WF        (rule 8, on this run's own tuned axis) the claim set's IS-best book stays best
              OOS, and |OOS share - IS share| <= 0.10 at that book.

GATES (printed before any new number):
  G1  every book reproduces its own memo's published (CAGR, Sharpe, MaxDD) within
      |dCAGR| <= 1.00pp, |dSharpe| <= 0.060, |dMaxDD| <= 2.00pp (data/prices.csv is
      re-cached daily; idea 406/574 measured u56 vintage drift at ~3e-3).
  G2  the LIVE book reproduces RULES.md v2's committed 8.63% / 1.202 / -12.05%.
  G3  this run's census machinery reproduces idea 828/829's committed entry-date share for
      the standing candidate (K5 at g=1.00, H=756, s=21): 0.3977, bar |d| <= 0.02.

Outputs (all under research/, all committed):
  .txt            full console log
  .books.csv      one row per book: fixed-window + OOS metrics, both KEEP paths
  .census.csv.gz  one row per (book, H, s, entry date)
  .grid.csv       one row per (book, H, s): pass share and every leg share
  .wf.csv         rule-8 IS/OOS entry-share table
  .result.md      the answer
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Run: python3 research/backtests/2026-09-12_how-many-of-the-record-s-committed-4b-PASSES-survive-their-OWN-ENTRY-DATE-CENSUS_B.py
"""
from __future__ import annotations
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import (load_universe, rules_v1_weights, rules_v2_weights, score,  # noqa: E402
                      band_state, compare)                                        # noqa: E402
from engine import backtest, metrics                                              # noqa: E402

DATE, SLUG = "2026-09-12", "how-many-of-the-record-s-committed-4b-PASSES-survive-their-OWN-ENTRY-DATE-CENSUS"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"
COST = 10
HORIZONS = [756, 1260]          # P2: 3y (the queue's ask) and 5y
SPACINGS = [21, 63]             # reported, not selected
HEAD_H, HEAD_S = 756, 21        # headline cell, named before the run
OOS_START = pd.Timestamp("2017-01-01")
IS_END = pd.Timestamp("2016-12-31")
MAX_VOL, WARMUP = 0.60, 260
BAR_HI, BAR_MID = 0.80, 0.50    # the queue's standing bar, and a majority bar
LOG: list[str] = []
pd.set_option("display.width", 250)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def hdr(s):
    P("\n" + "=" * 110 + f"\n{s}\n" + "=" * 110)


# =====================================================================================
# BOOK CONSTRUCTORS — copied verbatim from the committed scripts that built each corpus
# (idea 641 / 574 for K1..K8; idea 804's committed constructor for R4) so the corpus is
# not silently redefined here.
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
    from engine import rebalance_mask
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
    """R2 — hold every name above its own 200d MA, gross RE-SPREAD over exactly those names."""
    pm = px.notna()
    ma = (px > px.rolling(200).mean()) & pm
    k = ma.sum(axis=1).replace(0, np.nan)
    return gross * ma.astype(float).div(k, axis=0).fillna(0.0)


def ma_dist_tophalf(px, gross=0.75, q=0.50):
    """R3 — rank priced names by px/MA200-1, hold the top ceil(q*N) at gross/K each, rest CASH."""
    pm = px.notna()
    dist = (px / px.rolling(200).mean() - 1.0).where(pm)
    rk = dist.rank(axis=1, ascending=False)
    n_priced = dist.notna().sum(axis=1)
    k = np.ceil(q * n_priced).replace(0, np.nan)
    sel = rk.le(k, axis=0).fillna(False) & dist.notna()
    kk = sel.sum(axis=1).replace(0, np.nan)
    return gross * sel.astype(float).div(kk, axis=0).fillna(0.0)


def r6_topn(px, n=20, gross=0.65):
    """R4 — idea 804's committed constructor: rank priced names by 6m return, top n at g/n (DE-GROSS)."""
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
MEMO8 = ["K1", "K2", "K3", "K4", "K5", "K6", "K7", "K8"]
MEMO12 = MEMO8 + ["R1", "R2", "R3", "R4"]
CLAIM_SETS = {"MEMO8": MEMO8, "MEMO12": MEMO12}
COMPARANDS = ["LIVE", "V1"]


# =====================================================================================
def m3(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def build(panels):
    """Run every book ONCE over its panel's full sample (C1)."""
    books, meta = {}, {}
    for key, label, pan, wf, freq, pub, memo in CORPUS:
        px = panels[pan]
        t0 = time.time()
        r = backtest(px, wf(px), cost_bps=COST, freq=freq)["returns"]
        books[key] = r
        meta[key] = dict(label=label, panel=pan, freq=freq, pub=pub, memo=memo)
        P(f"  built {key:5s} {label:62s} panel {pan:5s} freq {freq}  ({time.time()-t0:.1f}s)")
    return books, meta


def gates(books, meta, panels, starts):
    hdr("GATES — printed BEFORE any new number")
    rows = []
    for key, label, pan, wf, freq, pub, memo in CORPUS:
        if pub[0] is None:
            rows.append(dict(gate=f"G1/{key}", pub_CAGR=np.nan, got_CAGR=np.nan, pub_Sharpe=np.nan,
                             got_Sharpe=np.nan, pub_MaxDD=np.nan, got_MaxDD=np.nan,
                             verdict="NO PUBLISHED TRIPLE"))
            continue
        r = books[key].loc[starts[pan]:]
        gc, gs, gd = m3(r)
        ok = abs(gc - pub[0]) <= 0.010 and abs(gs - pub[1]) <= 0.060 and abs(gd - pub[2]) <= 0.020
        rows.append(dict(gate=f"G1/{key}" if key not in ("LIVE", "V1") else f"G2/{key}",
                         pub_CAGR=pub[0], got_CAGR=gc, pub_Sharpe=pub[1], got_Sharpe=gs,
                         pub_MaxDD=pub[2], got_MaxDD=gd, verdict="PASS" if ok else "FAIL"))
    g = pd.DataFrame(rows)
    P(g.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    scored = g[g.verdict.isin(["PASS", "FAIL"])]
    P(f"Tolerance declared: |dCAGR|<=1.00pp, |dSharpe|<=0.060, |dMaxDD|<=2.00pp "
      f"(daily price re-cache; idea 406/574 measured u56 drift ~3e-3).")
    P(f"G1+G2: {(scored.verdict=='PASS').sum()} of {len(scored)} PASS "
      f"({len(g)-len(scored)} books have no published triple in their memo and are marked so).")
    g.to_csv(f"{OUT}.gates.csv", index=False)
    return g


# ----------------------------------------------------------------- the entry-date census
def census(books, meta, panels, starts):
    rows = []
    spy_cache = {}
    for pan, px in panels.items():
        spy_cache[pan] = px["SPY"].pct_change().fillna(0.0)
    for key in [c[0] for c in CORPUS]:
        pan = meta[key]["panel"]
        idx = panels[pan].index
        i0 = idx.get_loc(starts[pan])
        r_all, spy_all = books[key], spy_cache[pan]
        for H in HORIZONS:
            for s in SPACINGS:
                for i in range(i0, len(idx) - H + 1, s):
                    sl = slice(i, i + H)
                    spy = spy_all.iloc[sl]
                    s_c, s_s, s_d = m3(spy)
                    s_h1, s_h2 = halves(spy)
                    r = r_all.iloc[sl]
                    c, sh, dd = m3(r)
                    h1, h2 = halves(r)
                    L_sh = sh > s_s
                    L_hv = (h1 > s_h1) and (h2 > s_h2)
                    L_dd = dd >= 0.6 * s_d
                    L_cg = c >= 0.7 * s_c                                  # C3, literal
                    L_cg2 = c >= (s_c if s_c <= 0 else 0.7 * s_c)          # S2
                    rows.append(dict(book=key, panel=pan, H=H, s=s, entry=idx[i],
                                     end=idx[i + H - 1], CAGR=c, Sharpe=sh, MaxDD=dd,
                                     h1=h1, h2=h2, spy_CAGR=s_c, spy_Sharpe=s_s, spy_MaxDD=s_d,
                                     L_sharpe=L_sh, L_halves=L_hv, L_dd=L_dd, L_cagr=L_cg,
                                     PASS=bool(L_sh and L_hv and L_dd and L_cg),
                                     PASS_S2=bool(L_sh and L_hv and L_dd and L_cg2),
                                     spy_neg=bool(s_c <= 0)))
    return pd.DataFrame(rows)


def grid_of(cen):
    return (cen.groupby(["book", "H", "s"])
              .agg(n=("PASS", "size"), share=("PASS", "mean"), share_S2=("PASS_S2", "mean"),
                   leg_sharpe=("L_sharpe", "mean"), leg_halves=("L_halves", "mean"),
                   leg_dd=("L_dd", "mean"), leg_cagr=("L_cagr", "mean"),
                   med_CAGR=("CAGR", "median"), med_Sharpe=("Sharpe", "median"),
                   worst_MaxDD=("MaxDD", "min"), spy_neg=("spy_neg", "sum")).reset_index())


# ----------------------------------------------------------------- fixed-window KEEP paths
def fixed_window(books, meta, panels, starts):
    hdr("RULE 8 (b) MANDATED BOOK LEG + BOTH KEEP PATHS on the fixed window (the record's convention)")
    live = books["LIVE"]
    rows = []
    for key in [c[0] for c in CORPUS] + ["SPY_U56", "SPY_B136"]:
        if key.startswith("SPY_"):
            pan = key.split("_")[1]
            r_all = panels[pan]["SPY"].pct_change().fillna(0.0)
            pan_k = pan
        else:
            r_all, pan_k = books[key], meta[key]["panel"]
        f = r_all.loc[starts[pan_k]:]
        o = r_all.loc[OOS_START:]
        fc, fs, fd = m3(f); oc, os_, od = m3(o)
        fh1, fh2 = halves(f); oh1, oh2 = halves(o)
        rows.append(dict(book=key, panel=pan_k, full_CAGR=fc, full_Sharpe=fs, full_MaxDD=fd,
                         full_H1=fh1, full_H2=fh2, OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                         OOS_H1=oh1, OOS_H2=oh2))
    t = pd.DataFrame(rows).set_index("book")
    P(t.to_string(float_format=lambda x: f"{x:+.4f}"))

    P("\nBoth KEEP paths, per book (4a vs the LIVE RULES v2 book; 4b vs SPY, full AND OOS):")
    lv = t.loc["LIVE"]
    out = []
    for key in [c[0] for c in CORPUS if c[0] not in COMPARANDS]:
        r = t.loc[key]
        spy = t.loc[f"SPY_{meta[key]['panel']}"]
        legs4b = {
            "H1>SPY": r.full_H1 > spy.full_H1, "H2>SPY": r.full_H2 > spy.full_H2,
            "OOSsh>SPY": r.OOS_Sharpe > spy.OOS_Sharpe,
            "DD<=60%SPY": r.full_MaxDD >= 0.6 * spy.full_MaxDD,
            "CAGR>=70%SPY": r.full_CAGR >= 0.7 * spy.full_CAGR,
            "OOS_DD": r.OOS_MaxDD >= 0.6 * spy.OOS_MaxDD,
            "OOS_CAGR": r.OOS_CAGR >= 0.7 * spy.OOS_CAGR,
        }
        legs4a = {"H1>LIVE": r.full_H1 > lv.full_H1, "H2>LIVE": r.full_H2 > lv.full_H2,
                  "DD<=LIVE": r.full_MaxDD >= lv.full_MaxDD}
        p4b, p4a = all(legs4b.values()), all(legs4a.values())
        out.append(dict(book=key, keep4b="PASS" if p4b else "FAIL",
                        fail4b="+".join(k for k, v in legs4b.items() if not v),
                        keep4a="PASS" if p4a else "FAIL",
                        fail4a="+".join(k for k, v in legs4a.items() if not v)))
        P(f"  {key:5s} 4b {'PASS' if p4b else 'FAIL'}  4a {'PASS' if p4a else 'FAIL'}   "
          + "  ".join(f"{k}={'Y' if v else 'N'}" for k, v in legs4b.items()))
    kp = pd.DataFrame(out).set_index("book")
    t = t.join(kp)
    t.to_csv(f"{OUT}.books.csv")
    return t, kp


# ----------------------------------------------------------------- rule 8 on the tuned axis
def rule8_entry(cen, meta):
    hdr("RULE 8 (a) — ON THIS RUN'S OWN TUNED AXES: claim set / horizon picked on IS entries only")
    c = cen[(cen.s == HEAD_S) & (~cen.book.isin(COMPARANDS))].copy()
    rows = []
    for key in MEMO12:
        for H in HORIZONS:
            sub = c[(c.book == key) & (c.H == H)]
            is_, oos = sub[sub.end <= IS_END], sub[sub.entry >= OOS_START]
            rows.append(dict(book=key, H=H, n_IS=len(is_),
                             IS_share=is_.PASS.mean() if len(is_) else np.nan,
                             n_OOS=len(oos), OOS_share=oos.PASS.mean() if len(oos) else np.nan))
    t = pd.DataFrame(rows)
    P(t.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    valid = t.dropna(subset=["IS_share"])
    pick = None
    if len(valid) and valid.n_IS.max() > 0:
        best = valid.sort_values(["IS_share", "n_IS"], ascending=[False, False]).iloc[0]
        pick = (best.book, int(best.H))
        gap = abs(best.OOS_share - best.IS_share)
        P(f"\nIS-chosen (book, H) = {pick} on {int(best.n_IS)} IS windows (IS share "
          f"{best.IS_share:.4f}) -> OOS share {best.OOS_share:.4f} on {int(best.n_OOS)} windows, "
          f"read ONCE.  |OOS-IS| = {gap:.4f} vs bar 0.10.")
        oos_best = valid.sort_values("OOS_share", ascending=False).iloc[0]
        P(f"OOS-best cell is ({oos_best.book}, {int(oos_best.H)}) at {oos_best.OOS_share:.4f}; "
          f"IS pick {'IS' if (oos_best.book, int(oos_best.H)) == pick else 'is NOT'} the OOS best.")
    else:
        P("\nNo IS window closes by 2016-12-31 at any horizon -> nothing is selectable IS.")
    t.to_csv(f"{OUT}.wf.csv", index=False)
    return t, pick


# =====================================================================================
def main():
    t0 = time.time()
    P("=" * 110)
    P(f"# {DATE} lane B — IDEA 831: how many of the record's COMMITTED 4b PASSES survive their")
    P("#                 OWN ENTRY-DATE CENSUS?")
    P("=" * 110)
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    starts = {k: v.index[WARMUP] for k, v in panels.items()}
    for k, v in panels.items():
        P(f"panel {k:5s} {v.shape[1]:3d} cols  {v.index[0].date()} .. {v.index[-1].date()}  "
          f"scored from {starts[k].date()} (C4)")
    P(f"cost {COST} bps, next-day execution, no shorting, no leverage.  "
      f"P1 claim set {list(CLAIM_SETS)} | P2 horizon {HORIZONS} | spacing {SPACINGS} reported.")
    P("SURVIVORSHIP: universe.json and universe_broad.json are CURRENT-CONSTITUENT lists, so "
      "every LEVEL below is optimistic; the object here is a within-book contrast.")

    P("\nbuilding books (one full-sample simulation each, C1):")
    books, meta = build(panels)
    gates(books, meta, panels, starts)

    bt, kp = fixed_window(books, meta, panels, starts)

    hdr("THE ENTRY-DATE CENSUS — every (book x H x s) cell reported")
    cen = census(books, meta, panels, starts)
    cen.to_csv(f"{OUT}.census.csv.gz", index=False, compression="gzip")
    g = grid_of(cen)
    g.to_csv(f"{OUT}.grid.csv", index=False)
    P(f"{len(cen):,} (book, H, s, entry) rows over {len(CORPUS)} books.\n")

    g3 = g[(g.book == "K5") & (g.H == 756) & (g.s == 21)].iloc[0]
    d3 = abs(g3.share - 0.3977)
    P(f"GATE G3 — this run's census machinery vs idea 828/829's committed entry-date share for "
      f"the standing candidate (K5 g=1.00, H=756, s=21): got {g3.share:.4f} on {int(g3.n)} "
      f"windows vs committed 0.3977, |d| = {d3:.4f} vs bar 0.0200 -> "
      f"{'PASS' if d3 <= 0.02 else 'FAIL'}\n")
    for H in HORIZONS:
        for s in SPACINGS:
            P(f"--- H={H}d  s={s}d ---")
            sub = g[(g.H == H) & (g.s == s)].drop(columns=["H", "s"]).set_index("book")
            sub = sub.reindex([c[0] for c in CORPUS])
            P(sub.to_string(float_format=lambda x: f"{x:.4f}"))
            P("")

    # ---------------------------------------------------------------- THE DELIVERABLE
    hdr("THE DELIVERABLE — the record's committed 4b claim BESIDE its entry-date pass share")
    head = g[(g.H == HEAD_H) & (g.s == HEAD_S)].set_index("book")
    rowsD = []
    for key, label, pan, wf, freq, pub, memo in CORPUS:
        if key in COMPARANDS:
            continue
        r = bt.loc[key]
        rowsD.append(dict(book=key, panel=pan, label=label[:48],
                          claimed=f"{r.keep4b}/{r.keep4a}",
                          pub_CAGR=pub[0], full_CAGR=r.full_CAGR, full_Sharpe=r.full_Sharpe,
                          full_MaxDD=r.full_MaxDD,
                          share_3y=head.loc[key, "share"], n_3y=int(head.loc[key, "n"]),
                          leg_sharpe=head.loc[key, "leg_sharpe"],
                          leg_halves=head.loc[key, "leg_halves"],
                          leg_dd=head.loc[key, "leg_dd"], leg_cagr=head.loc[key, "leg_cagr"],
                          memo=memo))
    D = pd.DataFrame(rowsD).sort_values("share_3y", ascending=False)
    P(D.drop(columns=["memo", "label"]).to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    D.to_csv(f"{OUT}.deliverable.csv", index=False)
    P("\n(claimed = this run's own re-derivation of the fixed-window 4b/4a verdict; the memo file "
      "for each book is in .deliverable.csv)")

    hdr("P1 x P2 — how many committed 4b passes clear each entry-date bar, at every cell")
    cells = []
    for cs, keys in CLAIM_SETS.items():
        for H in HORIZONS:
            for s in SPACINGS:
                sub = g[(g.H == H) & (g.s == s) & (g.book.isin(keys))].set_index("book")
                sub = sub.reindex(keys)
                cells.append(dict(claim_set=cs, H=H, s=s, n_books=len(keys),
                                  n_ge_080=int((sub.share >= BAR_HI).sum()),
                                  n_ge_050=int((sub.share >= BAR_MID).sum()),
                                  median_share=sub.share.median(), max_share=sub.share.max(),
                                  argmax=sub.share.idxmax(), min_share=sub.share.min(),
                                  argmin=sub.share.idxmin(),
                                  live_share=g[(g.H == H) & (g.s == s) &
                                               (g.book == "LIVE")].share.iloc[0]))
    C = pd.DataFrame(cells)
    P(C.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    C.to_csv(f"{OUT}.cells.csv", index=False)

    # ---------------------------------------------------------------- hypotheses
    hdr("PRE-REGISTERED HYPOTHESES")
    h8 = head.reindex(MEMO8)
    h12 = head.reindex(MEMO12)
    verd = {}
    verd["H_NONE"] = (not (h8.share >= BAR_HI).any(),
                      f"max share over MEMO8 = {h8.share.max():.4f} ({h8.share.idxmax()}) vs bar "
                      f"{BAR_HI}; {(h8.share>=BAR_HI).sum()} of 8 clear it "
                      f"[MEMO12: {(h12.share>=BAR_HI).sum()} of 12]")
    verd["H_MAJORITY"] = ((h8.share >= BAR_MID).any(),
                          f"{(h8.share>=BAR_MID).sum()} of 8 reach {BAR_MID} "
                          f"[MEMO12: {(h12.share>=BAR_MID).sum()} of 12]")
    x = bt.reindex(MEMO12)["full_Sharpe"].astype(float)
    y = h12["share"].astype(float)
    rho = x.rank().corr(y.rank())                     # SPEARMAN, n = 12 (idea 564's convention)
    pear = np.corrcoef(x.values, y.values)[0, 1]
    verd["H_RANK"] = (rho >= 0.70, f"Spearman(full-sample Sharpe, 3y entry share) = {rho:+.4f} "
                                   f"(n=12; Pearson {pear:+.4f}) vs bar +0.70")
    hi = g[(g.s == HEAD_S) & (g.book.isin(MEMO12))].pivot_table(index="book", columns="H",
                                                                values="share")
    up = (hi[1260] > hi[756]).sum()
    verd["H_HORIZON"] = (up == len(hi), f"share(1260) > share(756) at {up} of {len(hi)} books")
    for k, (ok, why) in verd.items():
        P(f"  {k:11s} {'PASS' if ok else 'FAIL'}  — {why}")

    wf, pick = rule8_entry(cen, meta)
    if pick is not None:
        row = wf[(wf.book == pick[0]) & (wf.H == pick[1])].iloc[0]
        gap = abs(row.OOS_share - row.IS_share)
        oos_best = wf.dropna(subset=["IS_share"]).sort_values("OOS_share", ascending=False).iloc[0]
        okwf = gap <= 0.10 and (oos_best.book, int(oos_best.H)) == pick
        P(f"  H_WF        {'PASS' if okwf else 'FAIL'}  — IS pick {pick} -> gap {gap:.4f} vs bar "
          f"0.10; OOS best ({oos_best.book}, {int(oos_best.H)})")
    else:
        P("  H_WF        FAIL  — no IS-selectable cell")

    hdr("C3 — windows where SPY's CAGR is negative (the literal floor is HARDER there)")
    neg = (cen[cen.book == "K5"].groupby(["H", "s"])
              .agg(n=("spy_neg", "size"), n_spy_neg=("spy_neg", "sum"),
                   pass_literal=("PASS", "mean"), pass_S2=("PASS_S2", "mean")).reset_index())
    P(neg.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("(K5 shown; .grid.csv carries share_S2 for every book — the S2 column there is the same "
      "sensitivity applied to all.)")

    hdr("WHICH LEG BINDS — headline cell (H=756, s=21), failing windows only, per book")
    for key in MEMO12:
        f = cen[(cen.book == key) & (cen.H == HEAD_H) & (cen.s == HEAD_S) & (~cen.PASS)]
        tot = int(head.loc[key, "n"])
        if not len(f):
            P(f"  {key:5s} 0 failing windows of {tot}")
            continue
        P(f"  {key:5s} {len(f):4d} failing of {tot:4d}  "
          f"sharpe {int((~f.L_sharpe).sum()):4d}  halves {int((~f.L_halves).sum()):4d}  "
          f"dd {int((~f.L_dd).sum()):4d}  cagr {int((~f.L_cagr).sum()):4d}   "
          f"entries {f.entry.min().date()} .. {f.entry.max().date()}")

    hdr("PROTOCOL rule 3 — baseline.compare on the two books this run would have to defend")
    for key in ["K5", "R3"]:
        wfun = dict((c[0], c[3]) for c in CORPUS)[key]
        fr = dict((c[0], c[4]) for c in CORPUS)[key]
        pan = meta[key]["panel"]
        P(f"\n--- {key}: {meta[key]['label']} ---")
        res = compare(f"831 B {key} {meta[key]['label']}", wfun, panels[pan], freq=fr,
                      cost_bps=COST)
        LOG.append(str(res["table"]))

    P(f"\nTotal runtime {time.time()-t0:.0f}s")
    Path(f"{OUT}.txt").write_text("\n".join(LOG) + "\n")
    return D, C, g, bt, wf, verd


if __name__ == "__main__":
    main()
