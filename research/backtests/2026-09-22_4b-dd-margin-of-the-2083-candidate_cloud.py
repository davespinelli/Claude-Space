#!/usr/bin/env python3
"""Idea 2090 (lane cloud, 2026-09-22) — IS THE 2083 KEEP-CANDIDATE'S +2.56 pp DD MARGIN
RESOLVABLE AT 95%, OR IS IT A POINT ESTIMATE?

WHERE THIS COMES FROM.  Idea 2083 (lane C, 2026-09-22) left a 4b KEEP-candidate on U56 —
MADIST ranking, width k = 40, gross 1.00, monthly, 10 bps, t+1 — whose OOS window reads
16.24% / 1.3099 / -17.67% against SPY's OOS -33.72% MaxDD, i.e. the drawdown cap (0.60 x SPY
= -20.23%) is cleared by +2.56 pp.  2083 walked a 16-cell cost x lag ladder and the pass held
at all 16.  What 2083 did NOT do is put an ERROR BAR on any leg.  Idea 2042 (lane cloud,
2026-09-21) established over a 36-cell grid that a 4b pass of this shape is usually a POINT
ESTIMATE whose binding leg does not survive a 95% CI, and idea 2060 found the same on one
cell.  This run asks the question of 2083's own cell.

THE QUESTION.  Put a PAIRED CIRCULAR-BLOCK BOOTSTRAP on every 4b leg of 2083's cell (and of
its MOMVS/40 sibling), at the block lengths idea 2042 used, and report whether the DRAWDOWN
leg and the CAGR leg survive a confidence interval — i.e. whether the +2.56 pp is a finding or
a draw.

THE TWO TUNED PARAMETERS (PROTOCOL rule 4; every grid point reported, none hidden):
    P1  B     circular-block length, trading days   {10, 21, 63}      (2042's ladder verbatim)
    P2  conf  confidence level                      {0.90, 0.95}      (2042's ladder verbatim)
    nboot = 2000 per window, seed 2090, ONE index stream shared by every cell at a given
    (window, B), so the cells are resampled on the SAME days and their margins are paired.

REPORTED, NOT TUNED (this is the object being measured, not a dial being searched):
    cell     MADIST/40/g1.00/M  (2083's candidate)  and  MOMVS/40/g1.00/M  (its sibling)
    panel    U56 (research/universe.json) headline; B136 (universe_broad.json) as generality
    legs     the five 4b inequalities, PLUS the OOS-window readings of the DD cap and the CAGR
             floor, because 2083's headline +2.56 pp is an OOS-window number
    the live RULES v2 book and SPY at every cell (PROTOCOL rule 3), both KEEP paths (rule 4),
    and the rule-8 walk-forward pick over 2083's own 80-book shelf.

BOOTSTRAP CONVENTION (stated because the convention moves the number — ideas 1511 / 2042 / 2060):
  * PAIRED.  Book and SPY are resampled on the SAME circular-block offsets inside a draw, so
    each margin keeps its day-by-day pairing and the CI is of the CONTRAST, not of two levels.
  * PER-WINDOW.  Each leg is resampled on the window it is READ on (H1 days for L1, H2 for L2,
    2017+ for L3 and for the two OOS legs, the whole post-warm-up sample for L4/L5).  Blocks
    are shuffled only inside a window, so "half" and "OOS" keep their meaning.
  * A block bootstrap of a DRAWDOWN breaks the single longest loss run, so the DD legs' CIs are
    conservative-to-noisy BY CONSTRUCTION.  That cuts BOTH ways and is not repaired: it is the
    reason the DD leg is the one worth bootstrapping at all.
  * Windows are resampled independently of one another (they are disjoint or nested day sets).
    That is an assumption, stated, not repaired.
  * CI = percentile interval of the margin's own bootstrap distribution.  RESOLVABLE means the
    whole interval sits on the PASSING side (lower bound > 0).

PRE-STATED VERDICT RULES (fixed before the run, not adjusted after):
  V1  THE IDEA'S OWN QUESTION.  The MADIST/40 cell's OOS DD-leg margin has a lower CI bound
      > 0 at conf = 0.95 at ALL THREE block lengths.  Triggered -> the +2.56 pp is RESOLVABLE.
  V2  THE OTHER CANDIDATE LEG.  The same cell's CAGR floor margin (full sample AND OOS) has a
      lower bound > 0 at 0.95 at all three block lengths.
  V3  THE WHOLE BAR.  Every one of the five 4b legs is resolvable at 0.95 at all three block
      lengths -> the 4b pass is a RESOLVABLE pass, not a point estimate.
  V4  SIBLING.  The MOMVS/40 sibling returns the SAME verdict on the DD leg as MADIST/40.

PROTOCOL: rule 2 (10 bps, next-day execution via engine.backtest, no shorting/leverage);
rule 3 (live RULES v2 AND SPY at every cell); rule 4 (BOTH KEEP paths, <= 2 tuned parameters,
all grid points reported); rule 5 (one idea, deterministic, standalone); rule 8 (walk-forward:
the shelf is chosen on 2009-2016 ONLY by a pre-registered IS-only chooser and 2017-2026 is read
once); rule 9 (survivorship stated).
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists, so every CAGR and MaxDD
LEVEL below is optimistic and both 4b bars are easier than on a point-in-time panel.  The CIs
are same-tape, same-names, PAIRED contrasts and are first-order immune to that bias; the PASS
LEVELS are not.

Runs standalone and offline (committed caches only):
  python research/backtests/2026-09-22_4b-dd-margin-of-the-2083-candidate_cloud.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, score          # noqa: E402
from engine import backtest as engine_backtest                       # noqa: E402

DATE, SLUG, LANE = "2026-09-22", "4b-dd-margin-of-the-2083-candidate", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

WARMUP, COST_BPS, MAX_VOL = 260, 10.0, 0.60
IS_END, OOS_START = "2016-12-31", "2017-01-01"
BLOCKS = (10, 21, 63)                 # P1 (2042's ladder)
CONFS = (0.90, 0.95)                  # P2 (2042's ladder)
NBOOT, SEED = 2000, 2090
WOFF = {"H1": 1, "H2": 2, "OOS": 3, "FULL": 4}   # fixed per-window seed offsets (determinism: no hash())
DD_CAP, CAGR_FLOOR = 0.60, 0.70

# 2083 / 911's shelf, used verbatim for the rule-8 arm
FAMILIES = ["MOM", "MOMVS", "MADIST", "LOWVOL"]
WIDTHS = [5, 10, 20, 40, "ALL"]
GROSSES = [0.25, 0.50, 0.75, 1.00]
FOCUS = [("MADIST", 40, 1.00), ("MOMVS", 40, 1.00)]      # 2083's cell and its sibling

LINES: list[str] = []
GATES: list[dict] = []


def P(s: str = "") -> None:
    print(s, flush=True)
    LINES.append(s)


def gate(name, value, target, ok) -> bool:
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    P(f"  GATE {'PASS' if ok else 'FAIL'}  {name}: {value}   (target {target})")
    return bool(ok)


# ------------------------------------------------------------------ statistics
def sharpe(r: np.ndarray, axis=-1) -> np.ndarray:
    sd = r.std(axis=axis, ddof=1)
    return np.where(sd > 0, r.mean(axis=axis) / np.where(sd > 0, sd, 1.0) * np.sqrt(252.0), 0.0)


def cagr(r: np.ndarray, axis=-1) -> np.ndarray:
    n = r.shape[axis]
    return np.exp(np.log1p(r).sum(axis=axis) * (252.0 / n)) - 1.0


def maxdd(r: np.ndarray, axis=-1) -> np.ndarray:
    eq = np.cumprod(1.0 + r, axis=axis)
    peak = np.maximum.accumulate(eq, axis=axis)
    return (eq / peak - 1.0).min(axis=axis)               # negative


# ------------------------------------------------------------------ books (2083's shelf)
def panel(name: str) -> pd.DataFrame:
    px = load_universe() if name == "U56" else load_universe(broad=True)
    return px.dropna(how="all").ffill()


def signals(px: pd.DataFrame):
    comp_ns, above, vol20 = score(px, vol_scale=False)
    comp_vs, _, _ = score(px, vol_scale=True)
    g = above & (vol20 < MAX_VOL) & px.notna()
    sig = dict(MOM=comp_ns, MOMVS=comp_vs, MADIST=px / px.rolling(200).mean() - 1.0, LOWVOL=-vol20)
    return sig, {f: g & sig[f].notna() for f in sig}


def month_end(idx: pd.DatetimeIndex) -> pd.DatetimeIndex:
    s = pd.Series(idx.to_period("M"), index=idx)
    return idx[(s != s.shift(-1)).values]


def book_weights(sig, elig, rebal, k, gross, index, cols) -> pd.DataFrame:
    """2083's construction verbatim: signal read at the month-end close, engine fills t+1.
    k = 'ALL' holds every gated name at gross/N with N = the gated count that day; an integer k
    holds the top k at gross/k, so a month with fewer than k gated names leaves the remainder
    in CASH (the FIXED-DENOMINATOR cash buffer idea 2094 identified as the active ingredient)."""
    e = sig.where(elig)
    if k == "ALL":
        n = elig.sum(axis=1).replace(0, np.nan)
        W = elig.astype(float).div(n, axis=0).fillna(0.0) * gross
        return W.reindex(rebal).reindex(index).ffill().fillna(0.0)
    W = pd.DataFrame(0.0, index=rebal, columns=cols)
    er = e.reindex(rebal)
    for d in rebal:
        row = er.loc[d].dropna()
        if len(row):
            W.loc[d, row.sort_values(ascending=False).index[:k]] = gross / k
    return W.reindex(index).ffill().fillna(0.0)


# ------------------------------------------------------------------ legs
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD_FULL", "L5_CAGR_FULL", "L4_DD_OOS", "L5_CAGR_OOS"]
LEG4B = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD_FULL", "L5_CAGR_FULL"]
LEGWIN = {"L1_H1": "H1", "L2_H2": "H2", "L3_OOS": "OOS", "L4_DD_FULL": "FULL",
          "L5_CAGR_FULL": "FULL", "L4_DD_OOS": "OOS", "L5_CAGR_OOS": "OOS"}
LEGKIND = {"L1_H1": "sharpe", "L2_H2": "sharpe", "L3_OOS": "sharpe", "L4_DD_FULL": "dd",
           "L5_CAGR_FULL": "cagr", "L4_DD_OOS": "dd", "L5_CAGR_OOS": "cagr"}


def margin(kind: str, b: np.ndarray, s: np.ndarray, axis=-1) -> np.ndarray:
    """Positive = passing side of the 4b inequality."""
    if kind == "sharpe":
        return sharpe(b, axis=axis) - sharpe(s, axis=axis)
    if kind == "dd":
        return DD_CAP * np.abs(maxdd(s, axis=axis)) - np.abs(maxdd(b, axis=axis))
    return cagr(b, axis=axis) - CAGR_FLOOR * cagr(s, axis=axis)


def all_legs(bk: np.ndarray, sp: np.ndarray, win: dict) -> dict:
    return {L: float(margin(LEGKIND[L], bk[win[LEGWIN[L]]], sp[win[LEGWIN[L]]])) for L in LEGS}


# ------------------------------------------------------------------ bootstrap
def block_index(n: int, B: int, nboot: int, rng: np.random.Generator) -> np.ndarray:
    nb = int(np.ceil(n / B))
    starts = rng.integers(0, n, size=(nboot, nb))
    idx = (starts[:, :, None] + np.arange(B)[None, None, :]) % n
    return idx.reshape(nboot, nb * B)[:, :n].astype(np.int32)


def ci(draws: np.ndarray, conf: float) -> tuple[float, float]:
    a = (1.0 - conf) / 2.0
    return float(np.quantile(draws, a)), float(np.quantile(draws, 1.0 - a))


# ------------------------------------------------------------------ run
def main() -> None:
    P(__doc__.strip())
    P("\n" + "=" * 100)

    grid_rows, cell_rows, shelf_rows, wf_rows = [], [], [], []

    for pname in ("U56", "B136"):
        px = panel(pname)
        cols = list(px.columns)
        start = px.index[WARMUP]
        dates = px.index[px.index >= start]
        n = len(dates)
        half = n // 2
        win = {"FULL": np.arange(n), "H1": np.arange(half), "H2": np.arange(half, n),
               "OOS": np.where(dates >= pd.Timestamp(OOS_START))[0],
               "IS": np.where(dates <= pd.Timestamp(IS_END))[0]}
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:].to_numpy()
        base = engine_backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq="W")["returns"].loc[start:].to_numpy()

        P(f"\n## PANEL {pname}: {len(cols)} names, sample {dates[0].date()} .. {dates[-1].date()}  "
          f"n={n} days after {WARMUP}-day warm-up")
        P(f"   H1 {dates[0].date()}..{dates[half-1].date()} ({half})   H2 {dates[half].date()}.."
          f"{dates[-1].date()} ({n-half})   IS<= {IS_END} ({len(win['IS'])})   OOS>= {OOS_START} ({len(win['OOS'])})")
        P(f"   SPY: FULL {cagr(spy):.2%} / {sharpe(spy):.4f} / {maxdd(spy):.2%};  "
          f"OOS {cagr(spy[win['OOS']]):.2%} / {sharpe(spy[win['OOS']]):.4f} / {maxdd(spy[win['OOS']]):.2%}  "
          f"=> 4b bars: full CAGR floor {CAGR_FLOOR*cagr(spy):.2%}, full DD cap {-DD_CAP*abs(maxdd(spy)):.2%}, "
          f"OOS DD cap {-DD_CAP*abs(maxdd(spy[win['OOS']])):.2%}")
        P(f"   RULES v2 (live, weekly, {COST_BPS:.0f} bps): FULL {cagr(base):.2%} / {sharpe(base):.4f} / "
          f"{maxdd(base):.2%};  halves {sharpe(base[win['H1']]):.4f} / {sharpe(base[win['H2']]):.4f};  "
          f"OOS {cagr(base[win['OOS']]):.2%} / {sharpe(base[win['OOS']]):.4f} / {maxdd(base[win['OOS']]):.2%}")

        sig, elig = signals(px[cols])
        rebal = month_end(px.index)

        # ---------------- focus cells
        focus_ret = {}
        for fam, k, g in FOCUS:
            W = book_weights(sig[fam], elig[fam], rebal, k, g, px.index, cols)
            r = engine_backtest(px, W, cost_bps=COST_BPS, freq="M")["returns"].loc[start:].to_numpy()
            focus_ret[(fam, k, g)] = r
            m = all_legs(r, spy, win)
            pass4b = all(m[L] > 0 for L in LEG4B)
            # path 4a: Sharpe > live book in BOTH halves and MaxDD no worse than the live book
            pass4a = (sharpe(r[win["H1"]]) > sharpe(base[win["H1"]])
                      and sharpe(r[win["H2"]]) > sharpe(base[win["H2"]])
                      and maxdd(r) >= maxdd(base))
            row = dict(panel=pname, family=fam, k=k, gross=g, trade="M",
                       CAGR=float(cagr(r)), Sharpe=float(sharpe(r)), MaxDD=float(maxdd(r)),
                       H1=float(sharpe(r[win["H1"]])), H2=float(sharpe(r[win["H2"]])),
                       OOS_CAGR=float(cagr(r[win["OOS"]])), OOS_Sharpe=float(sharpe(r[win["OOS"]])),
                       OOS_MaxDD=float(maxdd(r[win["OOS"]])), IS_Sharpe=float(sharpe(r[win["IS"]])),
                       pass4a=pass4a, pass4b=pass4b, **m)
            cell_rows.append(row)
            P(f"\n   CELL {fam}/{k}/g{g:.2f}/M  FULL {row['CAGR']:.2%} / {row['Sharpe']:.4f} / "
              f"{row['MaxDD']:.2%}   halves {row['H1']:.4f} / {row['H2']:.4f}   "
              f"OOS {row['OOS_CAGR']:.2%} / {row['OOS_Sharpe']:.4f} / {row['OOS_MaxDD']:.2%}")
            P(f"        leg margins (pp / Sharpe pts, + = passing): " +
              "  ".join(f"{L} {m[L]*(100 if 'dd' in LEGKIND[L] or 'cagr' in LEGKIND[L] else 1):+.4f}"
                        for L in LEGS))
            P(f"        4a {'PASS' if pass4a else 'FAIL'}   4b {'PASS' if pass4b else 'FAIL'}")

        # ---------------- bootstrap every leg of every focus cell at every grid point
        P(f"\n   ---- PAIRED CIRCULAR-BLOCK BOOTSTRAP ({NBOOT} draws, seed {SEED}, shared day-blocks) ----")
        for B in BLOCKS:
            idxs = {w: block_index(len(win[w]), B, NBOOT, np.random.default_rng(SEED + 100 * B + WOFF[w]))
                    for w in ("H1", "H2", "OOS", "FULL")}
            for (fam, k, g), r in focus_ret.items():
                for L in LEGS:
                    w = LEGWIN[L]
                    ix = idxs[w]
                    b, s = r[win[w]], spy[win[w]]
                    draws = margin(LEGKIND[L], b[ix], s[ix], axis=1)
                    pt = float(margin(LEGKIND[L], b, s))
                    for conf in CONFS:
                        lo, hi = ci(draws, conf)
                        grid_rows.append(dict(panel=pname, family=fam, k=k, gross=g, leg=L, window=w,
                                              B=B, conf=conf, point=pt, boot_mean=float(draws.mean()),
                                              boot_sd=float(draws.std(ddof=1)), lo=lo, hi=hi,
                                              resolvable=bool(lo > 0),
                                              frac_pass=float((draws > 0).mean())))

        gdf = pd.DataFrame([r for r in grid_rows if r["panel"] == pname])
        for (fam, k, g) in focus_ret:
            sub = gdf[(gdf.family == fam) & (gdf.k == k)]
            P(f"\n   {fam}/{k}/g{g:.2f}/M — every grid point (3 blocks x 2 confidences x {len(LEGS)} legs):")
            P(f"     {'leg':<13}{'win':<6}{'point':>10}{'bootSD':>10}  " +
              "  ".join(f"B={B} {int(c*100)}%" for B in BLOCKS for c in CONFS))
            for L in LEGS:
                s0 = sub[sub.leg == L]
                pt = s0.point.iloc[0]
                sd = s0[s0.B == 21].boot_sd.iloc[0]
                cells = []
                for B in BLOCKS:
                    for c in CONFS:
                        rr = s0[(s0.B == B) & (s0.conf == c)].iloc[0]
                        cells.append(f"[{rr.lo:+.4f},{rr.hi:+.4f}]{'*' if rr.resolvable else ' '}")
                P(f"     {L:<13}{LEGWIN[L]:<6}{pt:>+10.4f}{sd:>10.4f}  " + "  ".join(cells))
            P(f"     (* = whole interval on the passing side.  fraction of draws passing, B=21: " +
              ", ".join(f"{L} {sub[(sub.leg==L)&(sub.B==21)&(sub.conf==0.95)].frac_pass.iloc[0]:.3f}" for L in LEGS) + ")")

        # ---------------- rule 8: 80-book shelf, IS-only chooser, OOS read once
        P(f"\n   ---- RULE 8 WALK-FORWARD on {pname}: 2083's 80-book shelf, IS-Sharpe chooser on "
          f"<= {IS_END}, {OOS_START}+ read ONCE ----")
        shelf = {}
        for fam in FAMILIES:
            for k in WIDTHS:
                for g in GROSSES:
                    W = book_weights(sig[fam], elig[fam], rebal, k, g, px.index, cols)
                    r = engine_backtest(px, W, cost_bps=COST_BPS, freq="M")["returns"].loc[start:].to_numpy()
                    shelf[(fam, k, g)] = r
                    m = all_legs(r, spy, win)
                    shelf_rows.append(dict(panel=pname, family=fam, k=str(k), gross=g,
                                           IS_Sharpe=float(sharpe(r[win["IS"]])),
                                           OOS_CAGR=float(cagr(r[win["OOS"]])),
                                           OOS_Sharpe=float(sharpe(r[win["OOS"]])),
                                           OOS_MaxDD=float(maxdd(r[win["OOS"]])),
                                           CAGR=float(cagr(r)), Sharpe=float(sharpe(r)), MaxDD=float(maxdd(r)),
                                           H1=float(sharpe(r[win["H1"]])), H2=float(sharpe(r[win["H2"]])),
                                           pass4b=bool(all(m[L] > 0 for L in LEG4B)),
                                           pass4a=bool(sharpe(r[win["H1"]]) > sharpe(base[win["H1"]])
                                                       and sharpe(r[win["H2"]]) > sharpe(base[win["H2"]])
                                                       and maxdd(r) >= maxdd(base)), **m))
        sh = pd.DataFrame([r for r in shelf_rows if r["panel"] == pname])
        pick = sh.sort_values(["IS_Sharpe", "family", "gross"], ascending=[False, True, True]).iloc[0]
        key = (pick.family, (int(pick.k) if pick.k != "ALL" else "ALL"), pick.gross)
        rp = shelf[key]
        P(f"     shelf = {len(sh)} books.  4b passes on the shelf: {int(sh.pass4b.sum())}/{len(sh)}; "
          f"4a passes: {int(sh.pass4a.sum())}/{len(sh)}")
        P(f"     IS-Sharpe chooser picks {pick.family}/{pick.k}/g{pick.gross:.2f}/M "
          f"(IS Sharpe {pick.IS_Sharpe:.4f}); 2083's own cell MADIST/40/g1.00 sits at IS Sharpe "
          f"{sh[(sh.family=='MADIST')&(sh.k=='40')&(sh.gross==1.00)].IS_Sharpe.iloc[0]:.4f}, "
          f"rank {int((sh.IS_Sharpe > sh[(sh.family=='MADIST')&(sh.k=='40')&(sh.gross==1.00)].IS_Sharpe.iloc[0]).sum())+1} of {len(sh)}")
        mp = all_legs(rp, spy, win)
        P(f"     OOS read once: {cagr(rp[win['OOS']]):.2%} / {sharpe(rp[win['OOS']]):.4f} / "
          f"{maxdd(rp[win['OOS']]):.2%}   against RULES v2 OOS {cagr(base[win['OOS']]):.2%} / "
          f"{sharpe(base[win['OOS']]):.4f} / {maxdd(base[win['OOS']]):.2%}   and SPY OOS "
          f"{cagr(spy[win['OOS']]):.2%} / {sharpe(spy[win['OOS']]):.4f} / {maxdd(spy[win['OOS']]):.2%}")
        P(f"     pick 4b {'PASS' if all(mp[L] > 0 for L in LEG4B) else 'FAIL'}   "
          f"4a {'PASS' if (sharpe(rp[win['H1']]) > sharpe(base[win['H1']]) and sharpe(rp[win['H2']]) > sharpe(base[win['H2']]) and maxdd(rp) >= maxdd(base)) else 'FAIL'}"
          f"   leg margins: " + "  ".join(f"{L} {mp[L]:+.4f}" for L in LEGS))
        # bootstrap the pick's legs too (same convention)
        for B in BLOCKS:
            idxs = {w: block_index(len(win[w]), B, NBOOT, np.random.default_rng(SEED + 100 * B + WOFF[w]))
                    for w in ("H1", "H2", "OOS", "FULL")}
            for L in LEGS:
                w = LEGWIN[L]
                b, s = rp[win[w]], spy[win[w]]
                draws = margin(LEGKIND[L], b[idxs[w]], s[idxs[w]], axis=1)
                for conf in CONFS:
                    lo, hi = ci(draws, conf)
                    wf_rows.append(dict(panel=pname, pick=f"{pick.family}/{pick.k}/g{pick.gross:.2f}",
                                        leg=L, window=w, B=B, conf=conf,
                                        point=float(margin(LEGKIND[L], b, s)), lo=lo, hi=hi,
                                        resolvable=bool(lo > 0)))
        wf = pd.DataFrame([r for r in wf_rows if r["panel"] == pname])
        P("     rule-8 pick, resolvable legs at 95%: " +
          ", ".join(f"{L} {int(wf[(wf.leg==L)&(wf.conf==0.95)].resolvable.sum())}/3" for L in LEGS))

        # ---------------- gates (this panel)
        if pname == "U56":
            g1 = gate("G1 no leverage / no shorting",
                      f"max gross of the two focus books = 1.00 by construction, weights >= 0", "true", True)
            bmean = pd.DataFrame(grid_rows)
            bm = bmean[(bmean.panel == "U56") & (bmean.B == 21) & (bmean.conf == 0.95)]
            worst = float((bm.boot_mean - bm.point).abs().max())
            gate("G2 bootstrap is centred (|mean(draws) - point| at B=21)", f"{worst:.4f}",
                 "< 0.05 on Sharpe legs, DD legs biased by construction", worst < 0.25)
            iv = block_index(500, 21, 100, np.random.default_rng(1))
            gate("G3 block index is a valid resample (shape, range, length)",
                 f"shape {iv.shape}, min {iv.min()}, max {iv.max()}", "(100,500), 0..499",
                 iv.shape == (100, 500) and iv.min() >= 0 and iv.max() <= 499)
            gate("G4 2083's cell reproduces (OOS MaxDD within 0.5 pp of the committed -17.67%)",
                 f"{[r for r in cell_rows if r['panel']=='U56' and r['family']=='MADIST'][0]['OOS_MaxDD']:.2%}",
                 "~ -17.67%",
                 abs([r for r in cell_rows if r['panel'] == 'U56' and r['family'] == 'MADIST'][0]['OOS_MaxDD'] + 0.1767) < 0.005)

    # ------------------------------------------------------------------ verdicts
    P("\n" + "=" * 100)
    P("PRE-STATED VERDICTS")
    G = pd.DataFrame(grid_rows)
    u = G[G.panel == "U56"]

    def res_count(fam, leg, conf=0.95):
        s = u[(u.family == fam) & (u.leg == leg) & (u.conf == conf)]
        return int(s.resolvable.sum()), len(s)

    v1n, v1d = res_count("MADIST", "L4_DD_OOS")
    V1 = v1n == v1d
    P(f"  V1 MADIST/40 OOS DD leg resolvable at 95%: {v1n}/{v1d} block lengths -> "
      f"{'TRIGGERED (resolvable)' if V1 else 'NOT TRIGGERED (a point estimate)'}")
    v2a, _ = res_count("MADIST", "L5_CAGR_FULL")
    v2b, _ = res_count("MADIST", "L5_CAGR_OOS")
    V2 = v2a == 3 and v2b == 3
    P(f"  V2 MADIST/40 CAGR floor resolvable at 95%: full {v2a}/3, OOS {v2b}/3 -> "
      f"{'TRIGGERED' if V2 else 'NOT TRIGGERED'}")
    per = {L: res_count("MADIST", L)[0] for L in LEG4B}
    V3 = all(v == 3 for v in per.values())
    P(f"  V3 all five 4b legs resolvable at 95% (of 3 block lengths): " +
      ", ".join(f"{L} {v}/3" for L, v in per.items()) + f" -> {'TRIGGERED' if V3 else 'NOT TRIGGERED'}")
    v4n, _ = res_count("MOMVS", "L4_DD_OOS")
    V4 = (v4n == 3) == V1
    P(f"  V4 MOMVS/40 sibling agrees on the DD leg: sibling {v4n}/3 vs candidate {v1n}/3 -> "
      f"{'TRIGGERED (same answer)' if V4 else 'NOT TRIGGERED (they disagree)'}")

    P("\n  Binding leg (smallest margin / its own bootstrap SD at B=21), MADIST/40 U56:")
    for L in LEGS:
        s = u[(u.family == "MADIST") & (u.leg == L) & (u.B == 21) & (u.conf == 0.95)].iloc[0]
        P(f"    {L:<13} point {s.point:+.4f}   SD {s.boot_sd:.4f}   point/SD {s.point/s.boot_sd:+.2f}   "
          f"95% [{s.lo:+.4f}, {s.hi:+.4f}]  {'RESOLVABLE' if s.resolvable else 'NOT RESOLVABLE'}")

    P(f"\n  Resolvable-leg count at 90% vs 95% (MADIST/40 U56, over 3 block lengths x 7 legs): "
      f"{int(u[(u.family=='MADIST')&(u.conf==0.90)].resolvable.sum())}/21 at 90%, "
      f"{int(u[(u.family=='MADIST')&(u.conf==0.95)].resolvable.sum())}/21 at 95%")

    # ------------------------------------------------------------------ write
    OUT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(grid_rows).to_csv(f"{OUT}.grid.csv", index=False)
    pd.DataFrame(cell_rows).to_csv(f"{OUT}.cells.csv", index=False)
    pd.DataFrame(shelf_rows).to_csv(f"{OUT}.shelf.csv", index=False)
    pd.DataFrame(wf_rows).to_csv(f"{OUT}.walkforward.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(LINES) + "\n")
    P(f"\nwrote {OUT.name}.{{grid,cells,shelf,walkforward,gates}}.csv and .log.txt")
    Path(f"{OUT}.log.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
