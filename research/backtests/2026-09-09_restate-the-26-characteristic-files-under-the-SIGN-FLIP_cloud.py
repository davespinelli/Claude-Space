#!/usr/bin/env python3
"""Idea 295 — restate the 26 characteristic files under the SIGN FLIP.

Question (QUEUE 295): idea 276 counted 26 files (14 tight) attributing a result to a panel
property across the cap line; idea 284 shows breadth's within-stratum content is zero and
disp/corr/evol reverse sign under the control.  Re-read each of those files' headline and
classify it as (a) zero once controlled, (b) sign-reversed once controlled, or (c) already
within-stratum; report how many published direction claims survive.

The classification is NOT a reading of prose — a prose verdict cannot be checked.  It is a
mechanical join of two things, both committed:

  A. THE CENSUS (no sampling).  The 26 files are re-derived from idea 276's own committed
     census (`cross & prop & cmp`), their headline blocks extracted mechanically, and each
     headline scanned for the four characteristics idea 271/284 named (breadth, disp, corr,
     evol) and for whether the file ALREADY controls cap mix (a stratum/fixed-mix/matched-q
     phrase in its own headline).  Every reading is written to .census.csv so it can be
     re-read rather than believed.

  B. THE SIGN FLIP PRICED.  Idea 276's MIX ladder is rebuilt (k=40 names, a share q drawn from
     the sub-$2B panel and 1-q from the large-cap STOCK pool, 21 q rungs x 8 draws = 168
     panels, one common window), each panel's four characteristics measured with idea 284's
     exact definitions, and each characteristic's slope against each book outcome estimated
     TWICE: pooled across the cap line (the published reading) and WITHIN stratum (both sides
     demeaned inside the q bin).  A characteristic's verdict is then read off the pair.

  C. THE JOIN.  Each file inherits the verdict of the characteristic ITS OWN headline names.
     A file naming none of the four, or resting on a non-price instrument, is NOT RESTATABLE
     on this ladder and is reported as such rather than silently classified.

Two tuned parameters, and only two; every grid point is reported:
    t_bar   in {1.000, 1.645, 1.960, 2.576}   the |t| at which a within-stratum slope is
                                              called non-zero
    strata  in {3, 5, 7, 21}                  stratum resolution = how coarsely the 21 q rungs
                                              are binned before demeaning

Rule 8 (PROTOCOL 8) is run on the CLASSIFICATION ITSELF: every slope is re-estimated on the
first half only (<= 2016-12-31), the verdict fixed there, and the second half (2017 .. end)
read ONCE to report whether the same verdict comes back — plus each book's OOS CAGR / Sharpe /
MaxDD against the live RULES v2 baseline and against SPY, and BOTH KEEP paths on every arm.

Costs 10 bps, weekly, weights decided at t applied at t+1 (engine).  No network.
SURVIVORSHIP: the sub-$2B panel and B136 are CURRENT constituents of their screens, so every
mixed panel inherits that bias on its small-cap side and the LEVEL of every number here is
optimistic.  The object under test is the SIGN and the WITHIN-vs-POOLED contrast of a slope,
which survivorship moves only through the level of the eligible share; no level comparison
across q is claimed as tradable.

Deterministic (seed 20260909), standalone.
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = Path(__file__).with_suffix("")
BT = ROOT / "research" / "backtests"
CENSUS_276 = BT / "2026-09-06_is-breadth-a-small-cap-dummy-everywhere-in-the-record_cloud.census.csv"

COST, FREQ = 10, "W"
K_MIX, N_DRAWS = 40, 8
QS = [round(x / 20, 2) for x in range(21)]
NS = [10, 20]
GROSS = 0.75
WARMUP = 260
IS_END = pd.Timestamp("2016-12-31")
SEED = 20260909
CHARS = ["breadth", "disp", "corr", "evol"]
OUTCOMES = ["Sharpe", "CAGR", "MaxDD"]
T_BARS = [1.000, 1.645, 1.960, 2.576]      # tuned param 1
STRATA = [3, 5, 7, 21]                     # tuned param 2
REUSE = "--reuse" in sys.argv

OUT = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT.append(s)


# ================================================================== A. the census
CHAR_PAT = {
    "breadth": r"\bbreadth\b|\bn_elig\b|eligible share|eligible fraction|on-?share|share of the eligible",
    "disp":    r"\bdispersion\b|\bdisp\b|cross-?sectional sd|cross-?sectional spread",
    "corr":    r"\bcorrelation\b|\bcorr\b|pairwise",
    "evol":    r"eligible-?set vol|eligible vol|\bevol\b|vol20|volatility of the eligible",
}
# The TIGHT reading drops the two loosest alternatives (a bare `vol20`/`corr` mention is not an
# attribution) and looks only at the first 300 characters — the bolded verdict clause itself.
CHAR_PAT_TIGHT = {
    "breadth": r"\bbreadth\b|\bn_elig\b|eligible share|eligible fraction|on-?share|share of the eligible",
    "disp":    r"\bdispersion\b|cross-?sectional sd|cross-?sectional spread",
    "corr":    r"\bcorrelation\b|pairwise",
    "evol":    r"eligible-?set vol|eligible vol|\bevol\b|volatility of the eligible",
}
TIGHT_CHARS = 300
CONTROLLED_PAT = (r"within-?stratum|within stratum|fixed cap mix|at fixed cap|matched cap|"
                  r"cap-?mix controlled|inside the stratum|q rung|per stratum|stratified")
NONPRICE_PAT = r"form 4|insider|edgar|8-?k|spin-?off|option|earnings call"


def headline_block(txt: str) -> str:
    """The file's headline: from its first bold verdict marker, 1500 chars. Ledgers have none."""
    m = re.search(r"\*\*(VERDICT|Verdict|ANSWERED|KILL|KEEP|HEADLINE)", txt)
    if m is None:
        m = re.search(r"\*\*", txt)
    if m is None:
        return txt[:1500]
    return txt[m.start():m.start() + 1500]


t0 = time.time()
say("=" * 104)
say("IDEA 295 — restate the 26 characteristic files under the SIGN FLIP   (cloud, 2026-09-09)")
say("=" * 104)

c276 = pd.read_csv(CENSUS_276)
files = c276[c276.cross & c276["prop"] & c276.cmp]["file"].tolist()
say(f"\n[A] THE CENSUS — {len(files)} files re-derived from idea 276's own committed census "
    f"({CENSUS_276.name}: cross & prop & cmp), no sampling.")

rows = []
for f in files:
    p = BT / f
    if not p.exists():
        p = ROOT / "research" / f
    if not p.exists():
        rows.append(dict(file=f, exists=False))
        continue
    txt = p.read_text(errors="replace")
    hb = headline_block(txt)
    low = hb.lower()
    named = [c for c in CHARS if re.search(CHAR_PAT[c], low)]
    tight = [c for c in CHARS if re.search(CHAR_PAT_TIGHT[c], low[:TIGHT_CHARS])]
    rows.append(dict(file=f, exists=True, chars=len(txt), ledger=f in ("LEADERBOARD.md", "CHANGELOG.md"),
                     n_named=len(named), named=";".join(named) or "-",
                     n_tight=len(tight), tight=";".join(tight) or "-",
                     already_controlled=bool(re.search(CONTROLLED_PAT, low)),
                     nonprice_instrument=bool(re.search(NONPRICE_PAT, low)),
                     headline=re.sub(r"\s+", " ", hb)[:240]))
CEN = pd.DataFrame(rows)
CEN.to_csv(f"{STEM}.census.csv", index=False)
say(CEN[["file", "ledger", "n_named", "named", "n_tight", "tight",
         "already_controlled", "nonprice_instrument"]].to_string(index=False))
say("  ('named' = WIDE reading: the characteristic appears anywhere in the 1500-char headline block. "
    "'tight' = the same word inside the bolded verdict clause (first 300 chars) with the two loosest "
    "alternatives, a bare `vol20` and a bare `corr`, removed. Both readings are carried through the "
    "join below; neither is a tuned parameter.)")
say(f"\n  of {len(CEN)}: {int(CEN.ledger.sum())} are LEDGERS (no headline claim of their own), "
    f"{int((~CEN.ledger & (CEN.n_named > 0)).sum())} name at least one of the four characteristics "
    f"{CHARS} in their headline, "
    f"{int((~CEN.ledger & (CEN.n_named == 0)).sum())} name NONE of them (idea 276's census was "
    f"keyword-level and it said so: a lower bound), "
    f"{int(CEN.already_controlled.sum())} already control cap mix in their own headline, "
    f"{int(CEN.nonprice_instrument.sum())} rest on a non-price instrument.")
say("  per-characteristic file counts: " + ", ".join(
    f"{c}={int(CEN.named.str.contains(c).sum())}" for c in CHARS))

# ================================================================== B. the ladder
say(f"\n[B] THE SIGN FLIP PRICED — idea 276's MIX rebuilt: k={K_MIX}, {len(QS)} q rungs x "
    f"{N_DRAWS} draws = {len(QS)*N_DRAWS} panels, seed {SEED}")

U = json.loads((ROOT / "research" / "universe.json").read_text())
ETFS = set(U["broad"]) | set(U["sectors"]) | set(U["bonds_fx_commod"])
pxb = load_universe(broad=True)
pxs = load_universe(small=True)
meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
BAD = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
S_STK = [c for c in pxs.columns if c != "SPY" and c not in BAD]
B_STK = [c for c in pxb.columns if c != "SPY" and c not in ETFS]
SPY_RAW = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)["SPY"]
COMMON = pxs.index
say(f"  small panel: {len(BAD)} tickers with max_1d_move >= 1.0 dropped first, {len(S_STK)} usable; "
    f"large-cap STOCK pool {len(B_STK)} (ETFs excluded)")
say(f"  common window {COMMON[0].date()} .. {COMMON[-1].date()} ({len(COMMON)} rows); "
    f"books top-n for n in {NS} + EWall control + RULES v2 (the 4a comparand) on every panel")
say(f"  costs {COST} bps, {FREQ}, next-day execution, {WARMUP}-day warm-up skip; "
    f"rule 8 IS <= {IS_END.date()}, OOS {IS_END.date()}+1 .. end")
say("  SURVIVORSHIP: both ends of the q ladder are CURRENT-constituent sets; levels are optimistic, "
    "the WITHIN-vs-POOLED sign contrast is what is claimed.")


def mk(cols_s, cols_l):
    parts = []
    if cols_s:
        parts.append(pxs[cols_s])
    if cols_l:
        parts.append(pxb[cols_l].reindex(COMMON, method="ffill"))
    px = pd.concat(parts, axis=1).reindex(COMMON).dropna(how="all").ffill()
    return px.join(SPY_RAW.reindex(px.index, method="ffill").rename("SPY"))


def panel_chars(px, cols, elig, lo, hi):
    """idea 284's four characteristics, verbatim definitions, over a date window."""
    m = rebalance_mask(px.index, FREQ)
    idx = px.loc[px.index[WARMUP]:].index
    if lo is not None:
        idx = idx[idx >= lo]
    if hi is not None:
        idx = idx[idx <= hi]
    rb = idx[m.reindex(idx).fillna(False).values]
    e = elig.loc[rb, cols]
    k = len(cols)
    nel = e.sum(axis=1)
    r63 = (px[cols] / px[cols].shift(63) - 1).loc[rb]
    vol20 = (px[cols].pct_change().rolling(20).std() * np.sqrt(252)).loc[rb]
    dr = px[cols].pct_change().loc[idx]
    C = dr.corr().to_numpy()
    iu = np.triu_indices(k, 1)
    return dict(breadth=float((nel / k).mean()),
                disp=float(r63.where(e).std(axis=1, ddof=0).mean()),
                evol=float(vol20.where(e).mean(axis=1).mean()),
                corr=float(np.nanmean(C[iu])) if k > 1 else np.nan)


rng = np.random.default_rng(SEED)
panels = []
for q in QS:
    ns_ = int(round(q * K_MIX)); nl_ = K_MIX - ns_
    for d in range(N_DRAWS):
        sc = list(rng.choice(S_STK, size=ns_, replace=False)) if ns_ else []
        lc = list(rng.choice(B_STK, size=nl_, replace=False)) if nl_ else []
        panels.append((q, d, sc, lc))

arm_rows = []
for i, (q, d, sc, lc) in enumerate([] if REUSE else panels):
    px = mk(sc, lc)
    tr = [c for c in px.columns if c != "SPY"]
    start = px.index[WARMUP]
    oos_lo = IS_END + pd.Timedelta(days=1)
    s, above, vol20 = score(px[tr], vol_scale=False)
    el = s.where(above & (vol20 < 0.60))
    elig = el.notna()
    ch_full = panel_chars(px, tr, elig, None, None)
    ch_is = panel_chars(px, tr, elig, None, IS_END)
    ch_oos = panel_chars(px, tr, elig, oos_lo, None)

    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    ms, ms_is, ms_oos = metrics(spy), metrics(spy.loc[:IS_END]), metrics(spy.loc[oos_lo:])
    h = len(spy) // 2
    ms1, ms2 = metrics(spy.iloc[:h]), metrics(spy.iloc[h:])
    base = backtest(px, rules_v2_weights(px[tr]).reindex(columns=px.columns).fillna(0.0),
                    cost_bps=COST, freq=FREQ)["returns"].loc[start:]
    mb, mb1, mb2 = metrics(base), metrics(base.iloc[:h]), metrics(base.iloc[h:])
    mb_oos = metrics(base.loc[oos_lo:])

    rank = el.rank(axis=1, ascending=False)
    e01 = elig.astype(float)
    cnt = e01.sum(axis=1).replace(0, np.nan)
    specs = [("EWall", np.nan, (GROSS * e01.div(cnt, axis=0)).reindex(columns=px.columns).fillna(0.0))]
    for n in NS:
        specs.append((f"top{n}", n, ((rank <= n).astype(float) * (GROSS / n))
                      .reindex(columns=px.columns).fillna(0.0)))
    for arm, n, w in specs:
        r = backtest(px, w, cost_bps=COST, freq=FREQ)["returns"].loc[start:]
        m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
        m_is, m_oos = metrics(r.loc[:IS_END]), metrics(r.loc[oos_lo:])
        arm_rows.append(dict(
            q=q, draw=d, arm=arm, n=n,
            **{f"{c}_full": ch_full[c] for c in CHARS},
            **{f"{c}_IS": ch_is[c] for c in CHARS},
            **{f"{c}_OOS": ch_oos[c] for c in CHARS},
            Sharpe_full=m["Sharpe"], CAGR_full=m["CAGR"], MaxDD_full=m["MaxDD"],
            Sharpe_IS=m_is["Sharpe"], CAGR_IS=m_is["CAGR"], MaxDD_IS=m_is["MaxDD"],
            Sharpe_OOS=m_oos["Sharpe"], CAGR_OOS=m_oos["CAGR"], MaxDD_OOS=m_oos["MaxDD"],
            H1=m1["Sharpe"], H2=m2["Sharpe"],
            pass4a=bool(m1["Sharpe"] > mb1["Sharpe"] and m2["Sharpe"] > mb2["Sharpe"]
                        and m["MaxDD"] >= mb["MaxDD"]),
            pass4b=bool(m1["Sharpe"] > ms1["Sharpe"] and m2["Sharpe"] > ms2["Sharpe"]
                        and m_oos["Sharpe"] > ms_oos["Sharpe"]
                        and m["MaxDD"] >= 0.60 * ms["MaxDD"] and m["CAGR"] >= 0.70 * ms["CAGR"]),
            base_Sharpe=mb["Sharpe"], base_CAGR=mb["CAGR"], base_MaxDD=mb["MaxDD"],
            base_H1=mb1["Sharpe"], base_H2=mb2["Sharpe"],
            base_OOS_Sharpe=mb_oos["Sharpe"], base_OOS_CAGR=mb_oos["CAGR"],
            base_OOS_MaxDD=mb_oos["MaxDD"],
            SPY_Sharpe=ms["Sharpe"], SPY_CAGR=ms["CAGR"], SPY_MaxDD=ms["MaxDD"],
            SPY_H1=ms1["Sharpe"], SPY_H2=ms2["Sharpe"],
            SPY_OOS_Sharpe=ms_oos["Sharpe"], SPY_OOS_CAGR=ms_oos["CAGR"],
            SPY_OOS_MaxDD=ms_oos["MaxDD"]))
    if (i + 1) % 21 == 0:
        say(f"    {i+1}/{len(panels)} panels ({time.time()-t0:6.1f}s)")

if REUSE:
    A = pd.read_csv(f"{STEM}.arms.csv")
    say(f"  --reuse: re-read {len(A)} arm-rows (the panel loop is deterministic; seed {SEED})")
else:
    A = pd.DataFrame(arm_rows)
    A.to_csv(f"{STEM}.arms.csv", index=False)
say(f"  {len(A)} arm-rows over {len(panels)} panels -> {Path(STEM).name}.arms.csv")

# ------------------------------------------------------------------ the slopes
def slope_t(x, y):
    """OLS slope of y on standardized x, its t, and n. Returns nan on a degenerate x."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    n = len(x)
    if n < 5 or np.std(x) == 0:
        return np.nan, np.nan, n
    xs = (x - x.mean()) / x.std(ddof=0)
    b = float(np.cov(xs, y, ddof=1)[0, 1] / np.var(xs, ddof=1))
    resid = y - y.mean() - b * xs
    dof = n - 2
    se = float(np.sqrt((resid @ resid) / dof / (np.sum(xs ** 2))))
    return b, (b / se if se > 0 else np.nan), n


def bin_q(qv, nb):
    """Coarsen the 21 q rungs into nb strata (equal-width in q)."""
    return np.minimum((np.asarray(qv, float) * nb).astype(int), nb - 1)


say("\n[B1] SLOPES — every characteristic against every outcome, POOLED across the cap line vs "
    "WITHIN stratum.")
say("     x standardized; 'within' demeans BOTH sides inside the q stratum. All grid points.")
slopes = []
for win in ["full", "IS", "OOS"]:
    for arm in ["EWall"] + [f"top{n}" for n in NS]:
        sub = A[A.arm == arm]
        for ch in CHARS:
            for oc in OUTCOMES:
                x = sub[f"{ch}_{win}"].to_numpy()
                y = sub[f"{oc}_{win}"].to_numpy()
                bu, tu, nu = slope_t(x, y)
                for nb in STRATA:
                    g = pd.DataFrame(dict(s=bin_q(sub["q"], nb), x=x, y=y))
                    xw = (g.x - g.groupby("s").x.transform("mean")).to_numpy()
                    yw = (g.y - g.groupby("s").y.transform("mean")).to_numpy()
                    bw, tw, nw = slope_t(xw, yw)
                    slopes.append(dict(window=win, arm=arm, char=ch, outcome=oc, strata=nb,
                                       b_pooled=bu, t_pooled=tu, n=nu,
                                       b_within=bw, t_within=tw,
                                       dof_within=nw - nb - 1,
                                       sign_flip=bool(np.isfinite(bu) and np.isfinite(bw)
                                                      and np.sign(bu) != np.sign(bw))))
S = pd.DataFrame(slopes)
S.to_csv(f"{STEM}.slopes.csv", index=False)
say("\n--- full window, all four characteristics x three outcomes x three arms x four stratum "
    "resolutions (144 rows; printed in full) ---")
say(S[S.window == "full"].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

# ------------------------------------------------------------------ verdicts on the grid
say("\n[B2] THE CHARACTERISTIC VERDICT over the (t_bar x strata) grid — ALL 16 POINTS.")
say("     ZERO = |t_within| < t_bar;  REVERSED = |t_within| >= t_bar and the pooled sign flips;")
say("     SURVIVES = |t_within| >= t_bar and the pooled sign holds.")


def verdict(bp, tp, bw, tw, t_bar):
    if not np.isfinite(tw):
        return "NA"
    if abs(tw) < t_bar:
        return "ZERO"
    if np.isfinite(bp) and np.sign(bp) != np.sign(bw):
        return "REVERSED"
    return "SURVIVES"


gridrows = []
for t_bar in T_BARS:
    for nb in STRATA:
        sub = S[(S.window == "full") & (S.strata == nb)].copy()
        sub["v"] = [verdict(r.b_pooled, r.t_pooled, r.b_within, r.t_within, t_bar)
                    for r in sub.itertuples()]
        for ch in CHARS:
            vv = sub[sub.char == ch]["v"]
            gridrows.append(dict(t_bar=t_bar, strata=nb, char=ch, cells=len(vv),
                                 ZERO=int((vv == "ZERO").sum()),
                                 REVERSED=int((vv == "REVERSED").sum()),
                                 SURVIVES=int((vv == "SURVIVES").sum()),
                                 modal=vv.mode().iloc[0] if len(vv) else "NA"))
GR = pd.DataFrame(gridrows)
GR.to_csv(f"{STEM}.grid.csv", index=False)
say(GR.to_string(index=False))
say("\n(modal verdict per characteristic across the 16 grid points:)")
say(GR.pivot_table(index="char", columns=["t_bar"], values="modal", aggfunc=lambda v: v.mode().iloc[0])
    .to_string())

# ================================================================== C. the join
say("\n[C] THE JOIN — each of the 26 files inherits the verdict of the characteristic its own "
    "headline names.")
CENTRAL = dict(t_bar=1.960 if 1.960 in T_BARS else T_BARS[len(T_BARS) // 2],
               strata=5 if 5 in STRATA else STRATA[len(STRATA) // 2])
say(f"    central grid point t_bar={CENTRAL['t_bar']}, strata={CENTRAL['strata']}; "
    f"every other point is in .filegrid.csv")


def char_verdict_at(ch, t_bar, nb, window="full"):
    sub = S[(S.window == window) & (S.strata == nb) & (S["char"] == ch)]
    vs = [verdict(r.b_pooled, r.t_pooled, r.b_within, r.t_within, t_bar) for r in sub.itertuples()]
    return pd.Series(vs).mode().iloc[0] if vs else "NA"


filegrid = []
for reading in ["wide", "tight"]:
    col = "named" if reading == "wide" else "tight"
    for t_bar in T_BARS:
        for nb in STRATA:
            cv = {c: char_verdict_at(c, t_bar, nb) for c in CHARS}
            for r in CEN.itertuples():
                nm = getattr(r, col, "-")
                if getattr(r, "exists", True) is False:
                    cls = "MISSING"
                elif r.ledger:
                    cls = "LEDGER (no headline claim)"
                elif r.nonprice_instrument:
                    cls = "NOT RESTATABLE (non-price instrument)"
                elif r.already_controlled:
                    cls = "(c) ALREADY WITHIN-STRATUM"
                elif nm == "-":
                    cls = "NOT RESTATABLE (headline names no characteristic)"
                else:
                    vs = [cv[c] for c in nm.split(";")]
                    if all(v == "ZERO" for v in vs):
                        cls = "(a) ZERO ONCE CONTROLLED"
                    elif any(v == "REVERSED" for v in vs):
                        cls = "(b) SIGN-REVERSED ONCE CONTROLLED"
                    else:
                        cls = "SURVIVES"
                filegrid.append(dict(reading=reading, t_bar=t_bar, strata=nb, file=r.file,
                                     named=nm, cls=cls))
FG = pd.DataFrame(filegrid)
FG.to_csv(f"{STEM}.filegrid.csv", index=False)
for reading in ["wide", "tight"]:
    say(f"\n--- counts per class over ALL {len(T_BARS)*len(STRATA)} grid points "
        f"({reading.upper()} reading) ---")
    say(FG[FG.reading == reading]
        .pivot_table(index="cls", columns=["t_bar", "strata"], values="file", aggfunc="count")
        .fillna(0).astype(int).to_string())
say(f"\n--- the per-file reading at the central point (t_bar={CENTRAL['t_bar']}, "
    f"strata={CENTRAL['strata']}) ---")
for reading in ["wide", "tight"]:
    CF = FG[(FG.reading == reading) & (FG.t_bar == CENTRAL["t_bar"])
            & (FG.strata == CENTRAL["strata"])]
    say(f"\n  [{reading.upper()}]")
    say(CF[["file", "named", "cls"]].to_string(index=False))
    surv = int((CF.cls == "SURVIVES").sum())
    per = (FG[FG.reading == reading].assign(s=lambda d: d.cls == "SURVIVES")
           .groupby(["t_bar", "strata"])["s"].sum())
    say(f"  PUBLISHED DIRECTION CLAIMS THAT SURVIVE ({reading}): {surv} of {len(CF)} files "
        f"({surv/len(CF):.1%}) at the central point; over all {len(per)} grid points the count "
        f"runs {int(per.min())}..{int(per.max())} (median {per.median():.1f}).")

# ================================================================== D. rule 8
say("\n[D] RULE 8 — the classification fixed on the FIRST HALF, the second half read ONCE.")
wf = []
for t_bar in T_BARS:
    for nb in STRATA:
        for ch in CHARS:
            vis = char_verdict_at(ch, t_bar, nb, "IS")
            voos = char_verdict_at(ch, t_bar, nb, "OOS")
            wf.append(dict(t_bar=t_bar, strata=nb, char=ch, IS_verdict=vis, OOS_verdict=voos,
                           holds=bool(vis == voos)))
WF = pd.DataFrame(wf)
WF.to_csv(f"{STEM}.walkforward.csv", index=False)
say(WF.to_string(index=False))
say(f"\n  the IS verdict comes back OOS in {WF.holds.sum()}/{len(WF)} "
    f"(char x grid) cells = {WF.holds.mean():.1%}")
say("\n  per characteristic:")
say(WF.groupby("char").agg(holds=("holds", "mean"),
                           IS_modal=("IS_verdict", lambda v: v.mode().iloc[0]),
                           OOS_modal=("OOS_verdict", lambda v: v.mode().iloc[0]))
    .to_string(float_format=lambda x: f"{x:.3f}"))

say("\n[D2] THE BOOKS THEMSELVES — OOS CAGR / Sharpe / MaxDD vs the live RULES v2 baseline and SPY, "
    "and BOTH KEEP paths (no selection: every arm-row).")
bk = (A.groupby("arm")
      .agg(rows=("pass4b", "size"),
           CAGR=("CAGR_full", "median"), Sharpe=("Sharpe_full", "median"),
           MaxDD=("MaxDD_full", "median"), H1=("H1", "median"), H2=("H2", "median"),
           OOS_CAGR=("CAGR_OOS", "median"), OOS_Sharpe=("Sharpe_OOS", "median"),
           OOS_MaxDD=("MaxDD_OOS", "median"),
           pass4a=("pass4a", "mean"), pass4b=("pass4b", "mean"))
      .reset_index())
base_row = dict(arm="RULES v2 (live, same panels)", rows=len(A),
                CAGR=A.base_CAGR.median(), Sharpe=A.base_Sharpe.median(), MaxDD=A.base_MaxDD.median(),
                H1=A.base_H1.median(), H2=A.base_H2.median(), OOS_CAGR=A.base_OOS_CAGR.median(),
                OOS_Sharpe=A.base_OOS_Sharpe.median(), OOS_MaxDD=A.base_OOS_MaxDD.median(),
                pass4a=np.nan, pass4b=np.nan)
spy_row = dict(arm="SPY", rows=len(A), CAGR=A.SPY_CAGR.iloc[0], Sharpe=A.SPY_Sharpe.iloc[0],
               MaxDD=A.SPY_MaxDD.iloc[0], H1=A.SPY_H1.iloc[0], H2=A.SPY_H2.iloc[0],
               OOS_CAGR=A.SPY_OOS_CAGR.iloc[0], OOS_Sharpe=A.SPY_OOS_Sharpe.iloc[0],
               OOS_MaxDD=A.SPY_OOS_MaxDD.iloc[0], pass4a=np.nan, pass4b=np.nan)
BK = pd.concat([bk, pd.DataFrame([base_row, spy_row])], ignore_index=True)
BK.to_csv(f"{STEM}.keeppaths.csv", index=False)
say(BK.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
say(f"\n  4a passes {int(A.pass4a.sum())}/{len(A)} ({A.pass4a.mean():.1%}); "
    f"4b passes {int(A.pass4b.sum())}/{len(A)} ({A.pass4b.mean():.1%})")
say("\n  (per q rung, so the ladder is visible rather than averaged away:)")
say(A.pivot_table(index="q", columns="arm", values=["Sharpe_OOS", "pass4b"], aggfunc="median")
    .to_string(float_format=lambda x: f"{x:.3f}"))

say(f"\ndone in {time.time()-t0:.1f}s")
Path(f"{STEM}.console.txt").write_text("\n".join(OUT) + "\n")
