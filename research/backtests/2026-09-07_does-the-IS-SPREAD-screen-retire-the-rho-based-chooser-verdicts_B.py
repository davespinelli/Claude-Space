#!/usr/bin/env python3
"""Idea 373 -- does the IS-SPREAD screen retire the record's rho-based chooser verdicts?

The queue's argument
--------------------
Idea 371 (2026-09-07, lane B) found the gross dial G1 inverting PERFECTLY -- Spearman
rho(IS Sharpe, OOS Sharpe) = -1.00 in 6 of 6 cells -- on an IS Sharpe spread of only
0.001-0.005.  A rank correlation computed over five points that are indistinguishable
in-sample is ranking noise: the sign is reproducible only because the noise itself is
frozen by the tape.  Meanwhile the material damage in that same cell was a 4.8x deeper
OOS drawdown that the Sharpe-ranked verdict never showed.

So the queue proposes a SCREEN, and this script prices it:

    S1  How many rule-8 chooser verdicts in the record rest on an IS Sharpe spread
        below tau (tau = 0.01 as proposed, plus a full reported grid)?
    S2  Of those, how many FLIP when the pick is judged by OOS MaxDD instead of by
        OOS Sharpe?
    S3  Does the spread actually SEPARATE good chooser verdicts from bad ones -- i.e.
        is the screen informative, or does it fire at random with respect to chooser
        quality?  A screen that does not separate cannot retire anything.

Pre-registered definitions (written before any number in this script was read)
-----------------------------------------------------------------------------
A CHOOSER CELL is a pool P of >= n_min books that share every context coordinate
(panel, cost rung, book form, ...) and differ in exactly ONE dial coordinate, each with
an IS (<=2016) Sharpe and an OOS (>=2017) Sharpe and OOS MaxDD.  This is the object
PROTOCOL rule 8 selects over everywhere in the record.
    pick        = argmax IS Sharpe over P                      (the rule-8 chooser)
    IS_spread   = max IS Sharpe - min IS Sharpe over P         (the screen's statistic)
    rank_S      = pick's percentile rank in P by OOS Sharpe    (1.0 = OOS best)
    rank_D      = pick's percentile rank in P by OOS |MaxDD|   (1.0 = shallowest)
    GOOD_S      = rank_S >= 0.5      "the Sharpe-judged verdict says the chooser was OK"
    GOOD_D      = rank_D >= 0.5      "the MaxDD-judged verdict says the chooser was OK"
    FLIP        = GOOD_S xor GOOD_D  "the verdict flips when judged by OOS MaxDD"
    regret_S    = OOS Sharpe(pick) - max OOS Sharpe over P     (<= 0)
    regret_D_pp = |OOS MaxDD(pick)| - min |OOS MaxDD| over P   (>= 0, in pp)
The two reported parameters are tau (the spread threshold) and n_min (the minimum pool
size).  BOTH are swept and every grid point is printed; nothing is tuned to a target.

Three arms
----------
[A] TEXTUAL CENSUS of research/LEADERBOARD.md: how many rows claim a rule-8 / chooser
    result at all, and how many of those quote an IS spread or margin.  This fixes the
    denominator the queue is asking about and is exact, not modelled.

[B] RECORD ARCHAEOLOGY over every committed CSV in research/backtests/ that carries an
    IS Sharpe, an OOS Sharpe and an OOS MaxDD per grid point (256 files).  Chooser cells
    are RECONSTRUCTED by the definition above and the screen is priced on them.  Two
    honesty devices: (i) results are reported pooled AND as a median across source
    files, because a handful of large grids would otherwise carry the census; (ii) a
    VALIDATED subset -- cells whose reconstructed pick's IS Sharpe also appears in the
    file's own committed *.walkforward.csv -- where the reconstruction is confirmed
    against a chooser verdict the record actually published.

[C] LIVE CONTROL CORPUS, computed here from baseline.py, where the pools are exact by
    construction and nothing is reconstructed: idea 371's nine dials (GATE: IS_spread
    and rho asserted equal to its committed ordering.csv) plus three dials it did not
    run (cadence, vol target, breadth gate), x 2 panels x 3 cost rungs.  Both KEEP paths
    are evaluated at EVERY point and the rule-8 walk-forward is reported for every cell
    against RULES v2 (live) and SPY.

Conventions: weekly rebalance unless the dial is cadence, weights decided at close t and
applied at t+1 (engine), long-only, no leverage, 10 bps is the PROTOCOL rung (0 and 25
reported), 260-day warm-up skipped, IS = through 2016-12-31, OOS = 2017-01-01 on.

CAVEATS.  (1) Arm [B] reconstructs pools from committed artefacts by a column-role
heuristic; a slice it admits is a pool rule 8 COULD have chosen over, not proof that a
given script published that exact verdict -- which is why the validated subset is
reported separately and the headline claim is stated on both.  (2) Both panels are
current-constituent lists: survivorship flatters levels, and the OOS window is where it
bites hardest; the IS-vs-OOS ordering statistics studied here are far less affected than
the levels.  (3) Five points per dial gives a Spearman rho roughly 1.5 effective degrees
of freedom -- nothing rests on any single cell's rho.  (4) The archaeology inherits every
bug of the artefacts it reads, including the pre-idea-38 calendar-day tape in files dated
before 2026-09-07; idea 39 established that the tape error was conservative, never
generous, and it is a level effect shared by every point inside a pool, so it cancels in
the within-pool ranks used here.

Deterministic, standalone.  Reads baseline.py, engine and committed CSVs; modifies nothing.
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, band_state  # noqa
from engine import backtest, metrics                                                # noqa

SLUG = "2026-09-07_does-the-IS-SPREAD-screen-retire-the-rho-based-chooser-verdicts_B"
OUT = ROOT / "research" / "backtests"
BT = OUT
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COSTS = [0, 10, 25]
FREQ = "W"
TAUS = [0.0025, 0.005, 0.01, 0.02, 0.05, 0.10]      # reported parameter 1
NMINS = [3, 4, 5]                                    # reported parameter 2
IDEA371 = OUT / "2026-09-07_the-IS-chooser-prefers-SPY-where-OOS-prefers-QQQ_B.ordering.csv"

# ============================================================ shared metric helpers
def hs(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_4b(r, spy):
    """PROTOCOL 4b: Sharpe > SPY in BOTH halves AND OOS, |MaxDD| <= 60% of SPY's, CAGR >= 70%."""
    m, ms = metrics(r), metrics(spy)
    h1, h2 = hs(r); s1, s2 = hs(spy)
    o = metrics(r.loc[OOS_START:])["Sharpe"] - metrics(spy.loc[OOS_START:])["Sharpe"]
    d = {"H1": h1 - s1, "H2": h2 - s2, "OOS": o,
         "DD": 0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"]),
         "CAGR": m["CAGR"] - 0.70 * ms["CAGR"]}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


def bars_4a(r, base):
    """PROTOCOL 4a: Sharpe > the live book in BOTH halves, MaxDD no worse."""
    m, mb = metrics(r), metrics(base)
    h1, h2 = hs(r); b1, b2 = hs(base)
    d = {"H1": h1 - b1, "H2": h2 - b2, "DD": abs(mb["MaxDD"]) - abs(m["MaxDD"])}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 2: return np.nan
    ra, rb = pd.Series(a).rank().values, pd.Series(b).rank().values
    if ra.std() == 0 or rb.std() == 0: return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


def prank(values, i, higher_is_better=True):
    """Percentile rank of element i among `values`, 1.0 = best, 0.0 = worst, ties averaged."""
    s = pd.Series(np.asarray(values, float))
    r = s.rank(ascending=not higher_is_better)      # 1 = best
    n = len(s)
    if n < 2: return np.nan
    return float((n - r.iloc[i]) / (n - 1))


def cell_stats(is_sh, oos_sh, oos_dd):
    """The pre-registered chooser statistics for one pool."""
    is_sh, oos_sh = np.asarray(is_sh, float), np.asarray(oos_sh, float)
    add = np.abs(np.asarray(oos_dd, float))
    i = int(np.argmax(is_sh))
    rs = prank(oos_sh, i, True)
    rd = prank(-add, i, True)
    good_s, good_d = rs >= 0.5, rd >= 0.5
    return dict(n=len(is_sh), IS_spread=float(is_sh.max() - is_sh.min()),
                IS_sd=float(is_sh.std(ddof=1)), pick_ix=i,
                IS_Sharpe_pick=float(is_sh[i]), OOS_Sharpe_pick=float(oos_sh[i]),
                OOS_MaxDD_pick=float(-add[i]),
                OOS_Sharpe_best=float(oos_sh.max()), OOS_MaxDD_best=float(-add.min()),
                OOS_spread=float(oos_sh.max() - oos_sh.min()),
                OOS_DD_spread_pp=float(100 * (add.max() - add.min())),
                regret_S=float(oos_sh[i] - oos_sh.max()),
                regret_D_pp=float(100 * (add[i] - add.min())),
                rank_S=rs, rank_D=rd, good_S=int(good_s), good_D=int(good_d),
                flip=int(good_s != good_d), sharpe_ok_dd_bad=int(good_s and not good_d),
                rho=spearman(is_sh, oos_sh), rho_D=spearman(is_sh, -add),
                pick_is_OOS_best=int(i == int(np.argmax(oos_sh))),
                pick_is_DD_best=int(i == int(np.argmin(add))))


# ============================================================ [A] leaderboard census
RULE8_PAT = re.compile(r"rule[ -]?8|chooser|walk[- ]?forward|OOS[- ]best|regret", re.I)
SPREAD_PAT = re.compile(r"IS[ _-]?(Sharpe[ _-]?)?(spread|margin)|near[- ]?tie|spread[ _-]?below", re.I)


def arm_a(log):
    txt = (ROOT / "research" / "LEADERBOARD.md").read_text().split("\n")
    rows = [l for l in txt if l.startswith("| ") and not l.startswith("|---")]
    rows = [l for l in rows if not l.startswith("| Date |")]
    r8 = [l for l in rows if RULE8_PAT.search(l)]
    sp = [l for l in r8 if SPREAD_PAT.search(l)]
    log("\n" + "=" * 108)
    log("[A] TEXTUAL CENSUS of research/LEADERBOARD.md (exact, not modelled)")
    log(f"    leaderboard rows                                    : {len(rows)}")
    log(f"    rows claiming a rule-8 / chooser / regret result     : {len(r8)} "
        f"({len(r8) / max(len(rows), 1):.1%})")
    log(f"    ... of those, rows quoting an IS spread or margin    : {len(sp)} "
        f"({len(sp) / max(len(r8), 1):.1%} of the chooser rows)")
    log("    => the record's chooser verdicts are, with the listed exceptions, published")
    log("       WITHOUT the statistic the queue proposes to screen them by.")
    for l in sp[:6]:
        log("       quoting: " + l[:150])
    return dict(rows=len(rows), rule8_rows=len(r8), spread_rows=len(sp))


# ============================================================ [B] record archaeology
IS_PATS = [r"IS_Sharpe", r"IS_Sh"]
OS_PATS = [r"OOS_Sharpe", r"OOS_Sh", r"oSharpe"]
DD_PATS = [r"OOS_MaxDD", r"OOS_DD", r"oMaxDD"]
METRIC_EXACT = {
    "cagr", "vol", "sharpe", "maxdd", "h1", "h2", "to", "turn", "turn/yr", "turnover", "gross",
    "gross_reb", "4a", "4b", "4b_oos", "p4a", "p4b", "f4a", "f4b", "oos", "osharpe", "ocagr",
    "omaxdd", "sharpe25", "years", "total", "winrate", "calmar", "sortino", "verdict", "fails",
    "elig", "names", "held", "flips", "z", "t", "bind", "bind_rate", "resid", "binds",
    "lever_rate", "entry_share", "pp_per_pp", "dsharpe", "dcagr", "dmaxdd", "cut_days",
    "episodes", "stops", "y2020", "y2022", "is_null", "rho", "regret", "skill", "keep_4a",
    "keep_4b", "keep_4b_oos", "interior", "oos_rank", "equity", "sortino_oos",
}
METRIC_PREFIX = ("is_", "oos_", "m_", "sh_y_", "f4", "p4", "d_")


def _col(cols, pats):
    for p in pats:
        for c in cols:
            if c == p: return c
    return None


def _is_metric(c):
    lc = str(c).lower()
    return lc in METRIC_EXACT or lc.startswith(METRIC_PREFIX)


def arm_b(log, n_min_report=3):
    files = sorted((BT).glob("*.csv"))
    cells, per_file, skipped = [], [], 0
    for f in files:
        try:
            d = pd.read_csv(f)
        except Exception:
            skipped += 1
            continue
        cols = d.columns.tolist()
        ic, oc, dc = _col(cols, IS_PATS), _col(cols, OS_PATS), _col(cols, DD_PATS)
        if not (ic and oc and dc) or len(d) < 3:
            continue
        # the file's own published chooser picks, for the validation subset
        wf = f.with_name(f.name.rsplit(".", 2)[0] + ".walkforward.csv")
        pub = np.array([])
        if wf.exists() and wf != f:
            try:
                w = pd.read_csv(wf)
                pubcols = [c for c in w.columns if str(c).startswith(("IS_Sharpe", "IS_Sh"))]
                if pubcols:
                    pub = pd.to_numeric(w[pubcols[0]], errors="coerce").dropna().values
            except Exception:
                pub = np.array([])
        keys = [c for c in cols if not _is_metric(c) and 1 <= d[c].nunique(dropna=False) <= 20]
        got = 0
        for ax in keys:
            if not (3 <= d[ax].nunique() <= 15):
                continue
            ctx = [k for k in keys if k != ax]
            groups = d.groupby(ctx, dropna=False, sort=False) if ctx else [((), d)]
            for gk, sub in groups:
                sub = sub.dropna(subset=[ic, oc, dc])
                if len(sub) < 3 or sub[ax].nunique() != len(sub):
                    continue
                st = cell_stats(sub[ic].values, sub[oc].values, sub[dc].values)
                st.update(source=f.name, axis=ax,
                          ctx="|".join(f"{k}={v}" for k, v in
                                       zip(ctx, gk if isinstance(gk, tuple) else (gk,)))[:120],
                          validated=int(pub.size > 0 and
                                        bool(np.any(np.abs(pub - st["IS_Sharpe_pick"]) < 1e-6))))
                cells.append(st)
                got += 1
        if got:
            per_file.append((f.name, got))
    C = pd.DataFrame(cells)
    log("\n" + "=" * 108)
    log("[B] RECORD ARCHAEOLOGY -- chooser cells reconstructed from committed artefacts")
    log(f"    CSV artefacts scanned                : {len(files)} (unreadable: {skipped})")
    log(f"    files with IS + OOS Sharpe + OOS DD  : {len(per_file)}")
    log(f"    reconstructed chooser cells (n>={n_min_report}) : {len(C)}")
    log(f"    ... of which VALIDATED against a published *.walkforward.csv pick: "
        f"{int(C['validated'].sum())} ({C['validated'].mean():.1%})")
    top = sorted(per_file, key=lambda x: -x[1])[:8]
    log("    largest contributing files (cells): " + ", ".join(f"{n.split('_')[0]}..{c}" for n, c in top))
    log(f"    file-level concentration: top 8 files carry {sum(c for _, c in top) / len(C):.1%} of cells "
        f"-> every headline below is reported POOLED and as a MEDIAN ACROSS FILES")
    return C


def screen_table(C, log, label, taus=TAUS, nmins=NMINS):
    """S1/S2/S3 for every (tau, n_min) grid point.  Nothing here is tuned."""
    rows = []
    for nm in nmins:
        S = C[C["n"] >= nm]
        if not len(S): continue
        for tau in taus:
            lo, hi = S[S["IS_spread"] < tau], S[S["IS_spread"] >= tau]
            def agg(x):
                if not len(x): return dict(n=0)
                return dict(n=len(x), flip=x["flip"].mean(), good_S=x["good_S"].mean(),
                            good_D=x["good_D"].mean(), sok_dbad=x["sharpe_ok_dd_bad"].mean(),
                            regS=x["regret_S"].mean(), regD=x["regret_D_pp"].mean(),
                            hit=x["pick_is_OOS_best"].mean())
            a, b = agg(lo), agg(hi)
            rows.append(dict(n_min=nm, tau=tau, n_cells=len(S), n_below=a["n"],
                             share_below=a["n"] / len(S),
                             flip_below=a.get("flip", np.nan), flip_above=b.get("flip", np.nan),
                             dflip=a.get("flip", np.nan) - b.get("flip", np.nan),
                             goodS_below=a.get("good_S", np.nan), goodS_above=b.get("good_S", np.nan),
                             goodD_below=a.get("good_D", np.nan), goodD_above=b.get("good_D", np.nan),
                             sok_dbad_below=a.get("sok_dbad", np.nan),
                             sok_dbad_above=b.get("sok_dbad", np.nan),
                             regS_below=a.get("regS", np.nan), regS_above=b.get("regS", np.nan),
                             regD_below=a.get("regD", np.nan), regD_above=b.get("regD", np.nan),
                             hit_below=a.get("hit", np.nan), hit_above=b.get("hit", np.nan)))
    T = pd.DataFrame(rows)
    log(f"\n--- SCREEN GRID [{label}]  (every (tau, n_min) point reported; none tuned)")
    log(T.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    return T


def separation(C, log, label):
    """S3: does the spread separate good chooser verdicts from bad ones?"""
    S = C.dropna(subset=["rank_S", "IS_spread"])
    out = dict(label=label, n=len(S),
               rho_spread_rankS=spearman(S["IS_spread"], S["rank_S"]),
               rho_spread_regretS=spearman(S["IS_spread"], -S["regret_S"]),
               rho_spread_rankD=spearman(S["IS_spread"], S["rank_D"]),
               rho_spread_regretD=spearman(S["IS_spread"], S["regret_D_pp"]),
               rho_spread_flip=spearman(S["IS_spread"], S["flip"]),
               rho_rankS_rankD=spearman(S["rank_S"], S["rank_D"]),
               flip_rate=S["flip"].mean(), goodS=S["good_S"].mean(), goodD=S["good_D"].mean(),
               hit=S["pick_is_OOS_best"].mean(), mean_regret_S=S["regret_S"].mean(),
               mean_regret_D_pp=S["regret_D_pp"].mean())
    log(f"\n--- SEPARATION [{label}] n={out['n']}")
    log(f"    Spearman rho(IS_spread, rank_S)   = {out['rho_spread_rankS']:+.4f}   "
        f"(> 0 means a WIDER spread buys a BETTER Sharpe-judged chooser)")
    log(f"    Spearman rho(IS_spread, -regret_S)= {out['rho_spread_regretS']:+.4f}")
    log(f"    Spearman rho(IS_spread, rank_D)   = {out['rho_spread_rankD']:+.4f}")
    log(f"    Spearman rho(IS_spread, regret_D) = {out['rho_spread_regretD']:+.4f}   "
        f"(> 0 means a WIDER spread buys a DEEPER OOS drawdown)")
    log(f"    Spearman rho(IS_spread, FLIP)     = {out['rho_spread_flip']:+.4f}")
    log(f"    Spearman rho(rank_S, rank_D)      = {out['rho_rankS_rankD']:+.4f}   "
        f"(the two judgements' agreement)")
    log(f"    unconditional: FLIP {out['flip_rate']:.1%} | GOOD_S {out['goodS']:.1%} | "
        f"GOOD_D {out['goodD']:.1%} | pick = OOS best {out['hit']:.1%} | "
        f"mean regret_S {out['mean_regret_S']:+.4f} | mean regret_DD {out['mean_regret_D_pp']:+.2f}pp")
    return out


# ============================================================ [C] live control corpus
MACRO = ["SPY", "QQQ", "IWM", "EFA", "EEM", "TLT", "GLD", "DBC", "UUP"]
SLEEVE_EQ = ["SPY", "QQQ", "IWM", "EFA", "EEM"]
MOM_LAGS = (252, 126, 63)
VOL_WINDOW, MA_WINDOW = 60, 200
SECTORS = ["XLK", "XLF", "XLV", "XLE", "XLI", "XLY", "XLP", "XLU", "XLB", "XLRE", "XLC"]
TILT = "XLK"


def _risk_parity(sub):
    vol = sub.pct_change().rolling(VOL_WINDOW).std()
    inv = 1.0 / vol.replace(0.0, np.nan)
    return inv.div(inv.sum(axis=1), axis=0)


def _vote_mom(sub):
    sig = [sub.shift(21) / sub.shift(MOM_LAGS[0]) - 1,
           sub / sub.shift(MOM_LAGS[1]) - 1,
           sub / sub.shift(MOM_LAGS[2]) - 1]
    return sum((s > 0).astype(float).where(s.notna()) for s in sig) / len(sig)


def sleeve_b_weights(px):
    sub = px[MACRO]
    w = (_vote_mom(sub) * _risk_parity(sub)).fillna(0.0)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[MACRO] = w
    return out


def sleeve_membership_weights(px, q):
    base = sleeve_b_weights(px)[MACRO]
    tilt = base.copy()
    tilt[SLEEVE_EQ] = tilt[SLEEVE_EQ] * q
    g0, g1 = base.sum(axis=1), tilt.sum(axis=1)
    scaled = tilt.mul((g0 / g1.replace(0.0, np.nan)).fillna(0.0), axis=0)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[MACRO] = scaled.fillna(0.0)
    return out


def core_leg(px, ticker, frac, gate=True):
    p = px[ticker]
    if gate:
        ma = p.rolling(MA_WINDOW).mean()
        on = (p > ma).astype(float).where(ma.notna(), 0.0)
    else:
        on = pd.Series(1.0, index=px.index)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[ticker] = frac * on
    return out


def core_blend(px, q, hi, lo, c=0.60, gate=True):
    return (core_leg(px, hi, c * q, gate) + core_leg(px, lo, c * (1.0 - q), gate)
            + (1.0 - c) * sleeve_b_weights(px))


def book_blend(px, q, gross=0.75):
    return q * rules_v1_weights(px, n=5, w=gross / 5.0) + (1.0 - q) * rules_v2_weights(px, gross=gross)


def sector_tilt(px, q, gross=0.75):
    cols = [c for c in SECTORS if c in px.columns]
    others = [c for c in cols if c != TILT]
    avail = px[cols].notna()
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    t_ok = avail[TILT].astype(float)
    n_o = avail[others].sum(axis=1).replace(0, np.nan)
    out[TILT] = gross * q * t_ok
    share = gross * (1.0 - q * t_ok) / n_o
    for c in others:
        out[c] = (share * avail[c].astype(float)).fillna(0.0)
    return out.fillna(0.0)


def breadth_gate_weights(px, B, band=0.03, gross=0.75):
    """B1 (new here): RULES v2 de-grossed to CASH on days when cross-sectional breadth
    E_t (share of priced names inside the band) is at or below B.  B=0 is the ungated
    control.  E_t is known at close t and the engine applies weights at t+1."""
    w = rules_v2_weights(px, band=band, gross=gross)
    st = band_state(px, band).where(px.notna())
    E = st.sum(axis=1) / px.notna().sum(axis=1).replace(0, np.nan)
    return w.mul((E > B).astype(float), axis=0)


def vol_target_weights(px, tgt, band=0.03, gross=0.75, cost=10, cap=1.5):
    """V1 (new here): RULES v2 scaled by tgt / realised 20d vol of its OWN returns, the
    vol lagged one day so the scalar is causal, capped at `cap` (no leverage beyond it and
    never above 1.0 gross-equivalent when cap*gross <= 1).  Two-pass: pass 1 prices the
    unscaled book to get its return stream."""
    w = rules_v2_weights(px, band=band, gross=gross)
    r0 = backtest(px, w, cost_bps=cost, freq=FREQ)["returns"]
    v = (r0.rolling(20).std() * np.sqrt(252)).shift(1)
    s = (tgt / v.replace(0.0, np.nan)).clip(upper=cap).fillna(1.0)
    return w.mul(s, axis=0)


def build_dials():
    D = []
    for key, lab, hi, lo in (("C1", "core-QQQ-vs-SPY", "QQQ", "SPY"),
                             ("C2", "core-QQQ-vs-IWM", "QQQ", "IWM"),
                             ("C3", "core-SPY-vs-EFA", "SPY", "EFA")):
        D.append((key, "composition", f"{lab} (c=0.60 gated + 0.40 sleeve)",
                  [(q, q, (lambda px, c, q=q, hi=hi, lo=lo: core_blend(px, q, hi, lo)), FREQ)
                   for q in (0.0, 0.25, 0.5, 0.75, 1.0)], 1.0, 1))
    D.append(("C4", "composition", "sleeve-equity-membership (0.60 gated QQQ core + 0.40 sleeve)",
              [(q, q, (lambda px, c, q=q: core_leg(px, "QQQ", 0.60, True)
                       + 0.40 * sleeve_membership_weights(px, q)), FREQ)
               for q in (0.0, 0.25, 0.5, 0.75, 1.0)], 1.0, 1))
    D.append(("C5", "composition", "book-blend RULES v1 vs RULES v2 (gross 0.75 both)",
              [(q, q, (lambda px, c, q=q: book_blend(px, q)), FREQ)
               for q in (0.0, 0.25, 0.5, 0.75, 1.0)], 0.0, 1))
    D.append(("C6", "composition", "sector-tilt XLK vs the other ten (gross 0.75)",
              [(q, i / 4.0, (lambda px, c, q=q: sector_tilt(px, q)), FREQ)
               for i, q in enumerate((0.0, 1.0 / 11.0, 0.25, 0.50, 1.00))], 1.0 / 11.0, 1))
    D.append(("W1", "control-width", "width n (RULES v1, gross 0.75)",
              [(n, i / 4.0, (lambda px, c, n=n: rules_v1_weights(px, n=n, w=0.75 / n)), FREQ)
               for i, n in enumerate((3, 5, 8, 12, 20))], 5, 1))
    D.append(("W2", "control-width", "width band (RULES v2, gross 0.75)",
              [(b, i / 4.0, (lambda px, c, b=b: rules_v2_weights(px, band=b, gross=0.75)), FREQ)
               for i, b in enumerate((0.00, 0.03, 0.06, 0.12, 0.20))], 0.03, 1))
    D.append(("G1", "control-gross", "gross (RULES v2, band 0.03)",
              [(g, i / 4.0, (lambda px, c, g=g: rules_v2_weights(px, band=0.03, gross=g)), FREQ)
               for i, g in enumerate((0.20, 0.40, 0.60, 0.80, 1.00))], 0.75, 1))
    # --- three dials idea 371 did not run (this script's extension of its corpus)
    D.append(("W3", "control-cadence", "rebalance cadence (RULES v2, band 0.03, gross 0.75)",
              [(f, i / 3.0, (lambda px, c, f=f: rules_v2_weights(px, band=0.03, gross=0.75)), f)
               for i, f in enumerate(("D", "W", "M", "Q"))], "W", 0))
    D.append(("V1", "control-voltarget", "vol target on RULES v2 (band 0.03, gross 0.75, cap 1.5x)",
              [(t, i / 4.0, (lambda px, c, t=t: vol_target_weights(px, t, cost=c)), FREQ)
               for i, t in enumerate((0.06, 0.08, 0.10, 0.12, 0.15))], 0.12, 0))
    D.append(("B1", "control-breadth", "breadth cash gate on RULES v2 (band 0.03, gross 0.75)",
              [(B, i / 4.0, (lambda px, c, B=B: breadth_gate_weights(px, B)), FREQ)
               for i, B in enumerate((0.00, 0.20, 0.30, 0.40, 0.50))], 0.00, 0))
    return D


def arm_c(log):
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    dials = build_dials()
    grid, cells = [], []
    for pname, px in panels.items():
        wknd = int((px.index.dayofweek >= 5).sum())
        assert wknd == 0, f"{pname}: expected the corrected trading-day tape, {wknd} weekend rows"
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        ms = metrics(spy); s1, s2 = hs(spy); so = metrics(spy.loc[OOS_START:])
        log("\n" + "#" * 108)
        log(f"### PANEL {pname}: {px.shape[1]} cols {px.index[0].date()} -> {px.index[-1].date()}, "
            f"eval from {start.date()}  |  SPY CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} "
            f"MaxDD {ms['MaxDD']:.2%} H1/H2 {s1:.3f}/{s2:.3f} OOS Sharpe {so['Sharpe']:.3f} "
            f"CAGR {so['CAGR']:.2%} MaxDD {so['MaxDD']:.2%}")
        for cost in COSTS:
            b = backtest(px, rules_v2_weights(px), cost_bps=cost, freq=FREQ)["returns"].loc[start:]
            mb = metrics(b); b1, b2 = hs(b); bo = metrics(b.loc[OOS_START:])
            log("\n" + "=" * 108)
            log(f"[C] LIVE DIAL CORPUS -- {pname} @ {cost} bps.  RULES v2 (live): CAGR {mb['CAGR']:.2%} "
                f"Sharpe {mb['Sharpe']:.3f} MaxDD {mb['MaxDD']:.2%} H1/H2 {b1:.3f}/{b2:.3f} "
                f"| OOS Sharpe {bo['Sharpe']:.3f} CAGR {bo['CAGR']:.2%} MaxDD {bo['MaxDD']:.2%}")
            for key, klass, label, points, anchor, in371 in dials:
                tab = []
                for native, qn, fn, freq in points:
                    res = backtest(px, fn(px, cost), cost_bps=cost, freq=freq)
                    r = res["returns"].loc[start:]
                    t = res["turnover"].loc[start:]
                    m = metrics(r); h1, h2 = hs(r)
                    mi, mo = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
                    ok4b, _, f4b = bars_4b(r, spy)
                    ok4a, _, f4a = bars_4a(r, b)
                    rec = dict(panel=pname, cost=cost, dial=key, dial_class=klass, param=native,
                               q_norm=qn, is_anchor=int(native == anchor), in_idea371=in371,
                               CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], Vol=m["Vol"],
                               H1=h1, H2=h2, IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                               OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                               turnover=t.sum() / (len(r) / 252),
                               pass4a=int(ok4a), fail4a="+".join(f4a) or "-",
                               pass4b=int(ok4b), fail4b="+".join(f4b) or "-")
                    grid.append(rec)
                    tab.append(dict(param=native, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                    H1=h1, H2=h2, IS_Sh=mi["Sharpe"], OOS_Sh=mo["Sharpe"],
                                    OOS_CAGR=mo["CAGR"], OOS_DD=mo["MaxDD"],
                                    turn=t.sum() / (len(r) / 252),
                                    _4a="PASS" if ok4a else "f:" + "+".join(f4a),
                                    _4b="PASS" if ok4b else "f:" + "+".join(f4b),
                                    anchor="<-anchor" if native == anchor else ""))
                sub = [g for g in grid if g["panel"] == pname and g["cost"] == cost and g["dial"] == key]
                st = cell_stats([x["IS_Sharpe"] for x in sub], [x["OOS_Sharpe"] for x in sub],
                                [x["OOS_MaxDD"] for x in sub])
                pick, best = sub[st["pick_ix"]], max(sub, key=lambda x: x["OOS_Sharpe"])
                ddbest = min(sub, key=lambda x: abs(x["OOS_MaxDD"]))
                anch = next((x for x in sub if x["is_anchor"]), None)
                st.update(source="LIVE", axis="dial", ctx=f"panel={pname}|cost={cost}|dial={key}",
                          validated=1, panel=pname, cost=cost, dial=key, dial_class=klass,
                          param_pick=pick["param"], param_OOS_best=best["param"],
                          param_DD_best=ddbest["param"],
                          OOS_CAGR_pick=pick["OOS_CAGR"], OOS_CAGR_best=best["OOS_CAGR"],
                          OOS_SPY_Sharpe=so["Sharpe"], OOS_SPY_CAGR=so["CAGR"],
                          OOS_SPY_MaxDD=so["MaxDD"], OOS_v2_Sharpe=bo["Sharpe"],
                          OOS_v2_CAGR=bo["CAGR"], OOS_v2_MaxDD=bo["MaxDD"],
                          vs_SPY=pick["OOS_Sharpe"] - so["Sharpe"],
                          vs_v2=pick["OOS_Sharpe"] - bo["Sharpe"],
                          vs_anchor=(pick["OOS_Sharpe"] - anch["OOS_Sharpe"]) if anch else np.nan,
                          n4a=sum(x["pass4a"] for x in sub), n4b=sum(x["pass4b"] for x in sub),
                          in_idea371=in371)
                cells.append(st)
                log(f"\n--- {key} [{klass}] {label}")
                log(pd.DataFrame(tab).to_string(index=False, float_format=lambda x: f"{x:.3f}"))
                log(f"    IS spread {st['IS_spread']:.4f}"
                    f"{'  <-- NEAR-TIE (<0.01): rho ranks noise' if st['IS_spread'] < 0.01 else ''}"
                    f" | rho(IS,OOS Sharpe) {st['rho']:+.2f} | rho(IS,-|OOS DD|) {st['rho_D']:+.2f}")
                log(f"    rule 8: pick={pick['param']} -> OOS CAGR {pick['OOS_CAGR']:.2%} "
                    f"Sharpe {pick['OOS_Sharpe']:.3f} MaxDD {pick['OOS_MaxDD']:.2%} "
                    f"| vs SPY {st['vs_SPY']:+.3f} vs RULES v2 {st['vs_v2']:+.3f} "
                    f"| 4a {st['n4a']}/{len(sub)} 4b {st['n4b']}/{len(sub)}")
                log(f"    judged by OOS Sharpe: rank {st['rank_S']:.2f} ({'GOOD' if st['good_S'] else 'BAD'}"
                    f", regret {st['regret_S']:+.3f} vs best={best['param']}) | "
                    f"judged by OOS MaxDD: rank {st['rank_D']:.2f} "
                    f"({'GOOD' if st['good_D'] else 'BAD'}, +{st['regret_D_pp']:.2f}pp vs "
                    f"best={ddbest['param']})"
                    f"{'   <== VERDICT FLIPS' if st['flip'] else ''}")
    return pd.DataFrame(grid), pd.DataFrame(cells)


def gate_371(cells, log):
    """Continuity gate: the nine idea-371 dials must reproduce its committed IS spreads."""
    if not IDEA371.exists():
        log("\n[GATE] idea 371 ordering.csv not found -- gate SKIPPED")
        return
    o = pd.read_csv(IDEA371)
    mine = cells[cells["in_idea371"] == 1]
    j = o.merge(mine, on=["panel", "cost", "dial"], suffixes=("_371", "_now"))
    d_sp = (j["IS_spread_371"] - j["IS_spread_now"]).abs()
    d_rho = (j["rho_IS_OOS"] - j["rho"]).abs()
    log("\n" + "=" * 108)
    log(f"[GATE] idea 371 reproduction on its 9 dials x 2 panels x 3 rungs: {len(j)}/54 cells joined")
    log(f"       max |dIS_spread| = {d_sp.max():.3e}   max |drho| = {d_rho.max():.3e}")
    assert len(j) == 54 and d_sp.max() < 1e-9 and d_rho.max() < 1e-9, "idea 371 not reproduced"
    log("       PASS -- the live corpus reproduces idea 371 exactly.")


# ============================================================ main
def main():
    lines = []

    def log(s=""):
        print(s)
        lines.append(str(s))

    log("#" * 108)
    log("IDEA 373 -- does the IS-SPREAD screen retire the record's rho-based chooser verdicts?")
    log("Pre-registered: pick = argmax IS Sharpe; GOOD_S/GOOD_D = pick in the better half of the")
    log("pool by OOS Sharpe / by OOS |MaxDD|; FLIP = GOOD_S xor GOOD_D.  tau and n_min swept, "
        "all reported.")
    log("#" * 108)

    a = arm_a(log)

    C = arm_b(log)
    C.to_csv(OUT / f"{SLUG}.cells.csv", index=False)
    tb_all = screen_table(C, log, "record archaeology, all reconstructed cells")
    tb_val = screen_table(C[C["validated"] == 1], log,
                          "record archaeology, VALIDATED subset (pick matches a published walkforward)")
    sep_all = separation(C, log, "archaeology, all cells")
    sep_val = separation(C[C["validated"] == 1], log, "archaeology, validated cells")

    # per-file medians, so a few large grids cannot carry the census
    g = C.assign(below=(C["IS_spread"] < 0.01).astype(float)).groupby("source")
    fm = pd.DataFrame(dict(cells=g.size(), flip=g["flip"].mean(), share_below_001=g["below"].mean(),
                           regret_S=g["regret_S"].mean(), regret_D_pp=g["regret_D_pp"].mean(),
                           goodS=g["good_S"].mean(), goodD=g["good_D"].mean()))
    log(f"\n--- PER-FILE MEDIANS across {len(fm)} source files (unweighted by cell count)")
    log(f"    median share of cells with IS spread < 0.01 : {fm['share_below_001'].median():.1%} "
        f"(IQR {fm['share_below_001'].quantile(.25):.1%}-{fm['share_below_001'].quantile(.75):.1%})")
    log(f"    median FLIP rate per file                    : {fm['flip'].median():.1%}")
    log(f"    median mean regret_S / regret_DD per file    : {fm['regret_S'].median():+.4f} / "
        f"{fm['regret_D_pp'].median():+.2f}pp")
    fm.to_csv(OUT / f"{SLUG}.perfile.csv")

    # the queue's headline numbers, at the proposed tau = 0.01, n_min = 3
    S = C[C["n"] >= 3]
    lo = S[S["IS_spread"] < 0.01]
    log("\n" + "*" * 108)
    log("*** THE QUEUE'S TWO QUESTIONS, at the proposed tau = 0.01 (archaeology arm)")
    log(f"***   how many chooser cells rest on IS spread < 0.01 : {len(lo)} of {len(S)} "
        f"({len(lo) / len(S):.1%});  validated subset "
        f"{int((lo['validated'] == 1).sum())} of {int((S['validated'] == 1).sum())}")
    log(f"***   how many of those FLIP when judged by OOS MaxDD  : {int(lo['flip'].sum())} of {len(lo)} "
        f"({lo['flip'].mean():.1%})   [cells with IS spread >= 0.01 flip "
        f"{S[S['IS_spread'] >= 0.01]['flip'].mean():.1%}]")
    log("*" * 108)

    grid, live = arm_c(log)
    grid.to_csv(OUT / f"{SLUG}.grid.csv", index=False)
    live.to_csv(OUT / f"{SLUG}.livecells.csv", index=False)
    gate_371(live, log)

    tb_live = screen_table(live, log, "live control corpus (exact pools)")
    sep_live = separation(live, log, "live control corpus")

    log("\n" + "=" * 108)
    log("[C] RULE-8 WALK-FORWARD on the live corpus -- every chooser cell's pick vs RULES v2 and SPY")
    wf = live[["panel", "cost", "dial", "dial_class", "param_pick", "IS_spread",
               "OOS_CAGR_pick", "OOS_Sharpe_pick", "OOS_MaxDD_pick", "OOS_v2_CAGR",
               "OOS_v2_Sharpe", "OOS_v2_MaxDD", "OOS_SPY_CAGR", "OOS_SPY_Sharpe",
               "OOS_SPY_MaxDD", "vs_v2", "vs_SPY", "regret_S", "regret_D_pp", "flip",
               "n4a", "n4b"]]
    wf.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    log(wf.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    log(f"\n    picks beating SPY OOS Sharpe: {(live['vs_SPY'] > 0).sum()}/{len(live)} | "
        f"beating RULES v2 OOS Sharpe: {(live['vs_v2'] > 0).sum()}/{len(live)}")
    log(f"    KEEP paths over all {len(grid)} live grid points: "
        f"4a {int(grid['pass4a'].sum())}/{len(grid)}, 4b {int(grid['pass4b'].sum())}/{len(grid)}")
    b4 = grid[grid["pass4b"] == 1]
    if len(b4):
        log("    4b passes:")
        log(b4[["panel", "cost", "dial", "param", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                "OOS_Sharpe", "turnover"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---- headline synthesis
    log("\n" + "#" * 108)
    log("SYNTHESIS")
    for name, sep in (("archaeology (all)", sep_all), ("archaeology (validated)", sep_val),
                      ("live corpus", sep_live)):
        log(f"  {name:26s} n={sep['n']:5d}  FLIP {sep['flip_rate']:.1%}  "
            f"rho(spread,rank_S) {sep['rho_spread_rankS']:+.3f}  "
            f"rho(spread,regret_DD) {sep['rho_spread_regretD']:+.3f}  "
            f"rho(rank_S,rank_D) {sep['rho_rankS_rankD']:+.3f}")
    pd.DataFrame([sep_all, sep_val, sep_live]).to_csv(OUT / f"{SLUG}.separation.csv", index=False)
    pd.concat([tb_all.assign(arm="archaeology_all"), tb_val.assign(arm="archaeology_validated"),
               tb_live.assign(arm="live")]).to_csv(OUT / f"{SLUG}.screengrid.csv", index=False)

    (OUT / f"{SLUG}.console.txt").write_text("\n".join(lines) + "\n")
    print(f"\nwrote {SLUG}.[cells|perfile|screengrid|separation|grid|livecells|walkforward].csv "
          f"and .console.txt")


if __name__ == "__main__":
    main()
