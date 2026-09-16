#!/usr/bin/env python3
"""
Idea 996 (cloud lane, 2026-09-16)
CENSUS THE RECORD'S SCREENED STATISTICS FOR A NAMED FALLBACK

  Idea 993 showed that a screened median quoted over SURVIVING PICKS ALONE overstates its
  gain over an unscreened control by 25.4% (median) and 52.7% (mean), and that the SIGN of
  the refusal itself flips with the fallback (mean dSharpe on emptied slots -0.4703 under
  FB_CASH, +0.4066 under FB_SPY, +0.0899 under FB_LIVE).  A screened statistic is therefore
  not a number until the fallback is named: "what does the capital do when the screen
  refuses" is part of the estimator, not a footnote.

  The queue asks two things and this run does both:
    (A) CENSUS -- harvest every committed screen / eligibility / decline claim in
        LEADERBOARD.md and CHANGELOG.md, count how many NAME A FALLBACK and how many are
        SURVIVING-PICKS-ONLY, and count how many are LOCATABLE (name a script or csv that
        still exists on disk, i.e. can be re-scored at all).
    (B) PRICE -- re-score the locatable construction with refusals PAID: rebuild the
        record's own 5-book x 3-panel x 2-gross x 4-cadence ladder from scratch, run three
        IS-only screens over it, and publish the screened-minus-control gain under FOUR
        fallbacks, one of which (FB_DROP) is the incumbent free-refusal convention.

THE UNIT.  A SLOT is a (panel, cadence, gross) cell -- 3 x 4 x 2 = 24 slots.  Inside a slot
the five books are the CANDIDATES.  The CONTROL chooser ranks all five on an IS-only
statistic and takes the best.  The SCREENED chooser first ADMITS candidates through a
screen and takes the best ADMITTED one; if the screen admits nothing the slot is REFUSED,
and what happens then is exactly the question.

TUNED AXES -- exactly two, as the queue line allows, every level reported, none selected:
  (1) claim set : STRICT (claims that quote a NUMERIC screened statistic) and WIDE (any
                  claim carrying screen / eligibility / decline vocabulary).  Leg (A).
  (2) fallback  : FB_DROP (incumbent -- the refused slot leaves the denominator), FB_CASH,
                  FB_SPY, FB_LIVE.  Leg (B).
Everything else -- panel, cadence, gross, book, screen, chooser, cost rung -- is a REPORTED
ladder.  Every point of every ladder is published; nothing is chosen on any of them.

PRE-REGISTERED HYPOTHESES (bars fixed before any number was read):
  H_NAMED  : >= 0.50 of the record's STRICT screened statistics NAME A FALLBACK.
             FAIL means the defect 993 found on one claim is the record's default.
  H_SURV   : >= 0.50 of the STRICT screened statistics are SURVIVING-PICKS-ONLY (quote a
             screened statistic and name no fallback).  PASS means the same.
  H_LOC    : >= 0.25 of the STRICT screened statistics are LOCATABLE on disk.
  H_DROP   : the incumbent FB_DROP convention OVERSTATES the mean OOS-Sharpe gain by
             >= 0.10 Sharpe units against FB_CASH in the headline cell.  This is 993's
             finding restated as a bar.
  H_SIGN   : the SIGN of the mean gain flips across the four fallbacks in >= 1 (screen,
             cost) cell.  PASS means the fallback is load-bearing, not cosmetic.
  H_PAID   : the headline screen's gain is >= 0 under ALL THREE PAID fallbacks.
             FAIL means screening is not free once the refusal is paid.
  H_4B     : the screen buys >= 1 OOS 4b pass the control does not have.
  H_4A     : >= 1 OOS 4a anywhere in this run.

GATES (printed before any hypothesis number):
  G0  offset-0 mask == engine.rebalance_mask on D/W/M/Q
  G1  the fast Ctx runner == engine.backtest on returns AND turnover, post warm-up
  G2  BAND03 @ 0.75 == baseline.rules_v2_weights elementwise
  G3  CROSS-RUN: idea 993's committed 13,500-row ladder, phase-0 rows (600 of them),
      reproduced column by column on today's tree
  G4a FB_CASH is exactly a zero return series
  G4b FB_SPY is exactly the panel's SPY return series
  G4c FB_LIVE is exactly this run's own (panel, BAND03, CORE, W) ladder row
  G5  determinism: one ladder cell rebuilt from scratch
  G6  SMALL panel hygiene: the max_1d_move >= 1.0 drop count from data/small_meta.csv
  G7  census determinism: the parse re-run gives identical counts

PROTOCOL: 10 bps primary (0/5/10/25/50 all built), decided at close t / applied t+1
(LAG 1), warm-up 260 days, IS 2009-2016 / OOS 2017-2026 read ONCE, no shorting, no leverage
beyond the published gross.  Rule 8 walk-forward is the design, not an appendix: every
chooser and every screen reads the IS window only and the OOS window is read once, and both
KEEP paths (4a against RULES v2, 4b against SPY) are evaluated at EVERY grid point -- every
ladder row, every control pick, every screened pick and every fallback.  Nothing in
RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py is modified.

SURVIVORSHIP (rule 9): U56, B136 and SMALL are CURRENT-CONSTITUENT lists (SMALL additionally
drops every ticker with max_1d_move >= 1.0 per data/small_meta.csv).  Every CAGR and drawdown
LEVEL is optimistic and every 4b count is an UPPER bound, most severely on SMALL.  The
measured object here is a DIFFERENCE between a screened and an unscreened chooser on the SAME
names and the SAME tape, so the bias is shared by both arms and very largely cancels; the
LEVELS quoted for the headline book do NOT cancel and are stated as upper bounds.

  SMOKE=1 trims the cost ladder for wiring checks only; headline numbers are the full run.
"""
from __future__ import annotations

import os
import re
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

SMOKE = os.environ.get("SMOKE") == "1"

# ---- reported constants (never tuned) ---------------------------------------------------
WARM = 260
LAG = 1
BAND0 = 0.03
VOLCAP = 0.60
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
HEAD_COST = 10.0
RUNGS = [0.0, 5.0, 10.0, 25.0, 50.0] if not SMOKE else [10.0]
GROSSES = {"CORE": 0.75, "EXT": 1.00}
CADORDER = ["D", "W", "M", "Q"]
PANELS = ["U56", "B136", "SMALL"]

LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
LEGNAME = {"H1": "L1_H1", "H2": "L2_H2", "OOS": "L3_OOS", "DD": "L4_DD", "CAGR": "L5_CAGR"}

SCREENS = ["S_IS4B", "S_ISSHARPE", "S_ISDD"]
HEAD_SCREEN = "S_IS4B"
CHOOSERS = ["C_SHARPE", "C_CAGR", "C_ISLEGS"]
HEAD_CHOOSER = "C_SHARPE"
FALLBACKS = ["FB_DROP", "FB_CASH", "FB_SPY", "FB_LIVE"]
PAID_FB = ["FB_CASH", "FB_SPY", "FB_LIVE"]
CLAIMSETS = ["STRICT", "WIDE"]

# pre-registered bars
BAR_NAMED = 0.50
BAR_SURV = 0.50
BAR_LOC = 0.25
BAR_DROP = 0.10

# idea 993's committed ladder (G3)
PARENT_LADDER = OUT / "2026-09-16_is-REFUSAL-COST-a-CADENCE-object_cloud.ladder.csv"
G3_COLS = ["turn_per_yr", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_CAGR", "IS_Sharpe",
           "IS_MaxDD", "IS_H1", "IS_H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]
G3_TOL = 1e-9

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# =========================================================================================
# (1) THE CENSUS VOCABULARY -- fixed before the corpus was read, published verbatim
# =========================================================================================
SCREEN_VOCAB = ["screen", "screened", "screening", "eligib", "ineligib", "decline",
                "declin", "refus", "admit", "admiss", "gated", "filter"]
FALLBACK_VOCAB = ["fallback", "fb_cash", "fb_spy", "fb_live", "fb_none", "fb_drop",
                  "to cash", "in cash", "de-gross", "degross", "re-spread", "respread",
                  "emptied slot", "refused slot", "declined slot", "goes to cash",
                  "held in cash", "empties", "emptied"]
SURV_VOCAB = ["surviving pick", "over surviving", "picks alone", "over the picks",
              "per-pick", "among survivors", "of the surviving", "survivors only",
              "surviving-picks"]
STAT_VOCAB = ["median", "mean ", "share", "rate", "gain", "dsharpe", "pp", "percent", "%"]
NUM_RE = re.compile(r"[-+]?\d+\.\d+")
FILE_RE = re.compile(r"[\w\-\.]+\.(?:py|csv)")


def claims_from(path: Path, kind: str):
    """A CLAIM is one LEADERBOARD table row, or one CHANGELOG paragraph."""
    txt = path.read_text(errors="replace")
    out = []
    if kind == "table":
        for i, ln in enumerate(txt.split("\n")):
            s = ln.strip()
            if s.startswith("|") and s.count("|") >= 4 and not set(s) <= set("|- "):
                out.append((f"{path.name}:{i+1}", s))
    else:
        buf, start = [], 0
        for i, ln in enumerate(txt.split("\n")):
            if ln.strip():
                if not buf:
                    start = i + 1
                buf.append(ln)
            elif buf:
                out.append((f"{path.name}:{start}", " ".join(buf)))
                buf = []
        if buf:
            out.append((f"{path.name}:{start}", " ".join(buf)))
    return out


def classify(loc, text):
    low = text.lower()
    has_screen = any(v in low for v in SCREEN_VOCAB)
    has_stat = bool(NUM_RE.search(text)) and any(v in low for v in STAT_VOCAB)
    named_fb = any(v in low for v in FALLBACK_VOCAB)
    surv_exp = any(v in low for v in SURV_VOCAB)
    files = [f for f in FILE_RE.findall(text)]
    locatable = any((OUT / f).exists() or (ROOT / "research" / f).exists() for f in files)
    return dict(claim_loc=loc, screen=has_screen, stat=has_stat, named_fb=named_fb,
                surv_explicit=surv_exp, locatable=locatable, n_files=len(files),
                chars=len(text))


def run_census():
    rows = []
    for path, kind in [(ROOT / "research" / "LEADERBOARD.md", "table"),
                       (ROOT / "research" / "CHANGELOG.md", "para")]:
        for loc, text in claims_from(path, kind):
            rows.append(classify(loc, text))
    C = pd.DataFrame(rows)
    C["src"] = C.claim_loc.str.split(":").str[0]
    C["WIDE"] = C.screen
    C["STRICT"] = C.screen & C.stat
    return C


# =========================================================================================
# (2) engine machinery -- the record's form, verbatim
# =========================================================================================
def offset_mask(idx, per, d=0):
    if per == "D":
        return pd.Series(True, index=idx)
    key = pd.Series(idx.to_period({"W": "W", "M": "M", "Q": "Q"}[per]), index=idx)
    last = np.flatnonzero((key != key.shift(-1)).values)
    first = np.concatenate([[0], last[:-1] + 1])
    pick = np.maximum(last - d, first)
    out = pd.Series(False, index=idx)
    out.iloc[np.unique(pick)] = True
    return out


class Ctx:
    def __init__(self, px, mask):
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        m = np.asarray(mask.values, bool)
        m = np.concatenate([[False], m[:-1]]).copy()
        m[0] = True
        self.T, self.N = self.rets.shape
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.N)), C[:-1]])
        self.reb = np.flatnonzero(m)
        seg = np.searchsorted(self.reb, np.arange(self.T), side="right") - 1
        self.s0 = self.reb[seg]
        self.s0p = self.reb[np.maximum(seg - 1, 0)]
        self.ratio = self.Cp / self.Cp[self.s0]
        self.ratiop = self.Cp / self.Cp[self.s0p]

    def run(self, wt):
        W0 = wt[self.s0]
        h = W0 * self.ratio
        V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
        held = h / V[:, None]
        W0p = wt[self.s0p]
        hp = W0p * self.ratiop
        Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
        heldp = hp / Vp[:, None]
        heldp[self.reb[0]] = 0.0
        turn = np.zeros(self.T)
        turn[self.reb] = np.abs(wt[self.reb] - heldp[self.reb]).sum(axis=1)
        return (held * self.rets).sum(axis=1), turn


def shift1(W, idx):
    return W.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values


def sharpe(r):
    """Sharpe of a ZERO-VARIANCE series is 0.0 by convention, not NaN.  This is the record's
    own convention (993's committed fallbacks.csv publishes FB_CASH at Sharpe 0.0) and it is
    load-bearing here: under NaN, FB_CASH would silently drop out of every nanmean and the
    paid statistic would collapse onto the FB_DROP convention this run is testing."""
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else 0.0


def maxdd(r):
    eq = np.cumprod(1.0 + r)
    return float((eq / np.maximum.accumulate(eq) - 1).min())


def mets(r):
    if len(r) == 0:
        return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan, H1=np.nan, H2=np.nan)
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    h = len(r) // 2
    return dict(CAGR=float(eq[-1] ** (1 / yrs) - 1) if yrs > 0 else np.nan,
                Sharpe=sharpe(r), MaxDD=maxdd(r), H1=sharpe(r[:h]), H2=sharpe(r[h:]))


# ---- the book set, verbatim from 942/962/964/976/980/981/984/986/993 --------------------
def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band, g):
    return ew_gross(px, g).where(band_state(px, band) & px.notna(), 0.0)


def ew_elig(px, g):
    _, above, vol20 = score(px, vol_scale=False)
    e = (above & (vol20 < VOLCAP)).astype(float).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def ranked_book(px, g, k):
    sc, above, vol20 = score(px, vol_scale=False)
    rank = sc.where(above & (vol20 < VOLCAP)).rank(axis=1, ascending=False)
    return (rank <= k).astype(float) * (g / k)


BOOKS = {
    "TOP05":  lambda p, g: ranked_book(p, g, 5),
    "TOP10":  lambda p, g: ranked_book(p, g, 10),
    "TOP20":  lambda p, g: ranked_book(p, g, 20),
    "EWELIG": lambda p, g: ew_elig(p, g),
    "BAND03": lambda p, g: band_book(p, BAND0, g),
}
BOOKORDER = list(BOOKS)


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    return px[[c for c in px.columns if c == "SPY" or c not in bad]], len(bad)


def _argmax(v, tiebreak=None):
    v = np.asarray(v, float)
    if not np.isfinite(v).any():
        return None
    best = np.nanmax(v)
    cand = np.flatnonzero(v == best)
    if len(cand) > 1 and tiebreak is not None:
        t = np.asarray(tiebreak, float)[cand]
        cand = cand[np.flatnonzero(t == np.nanmax(t))]
    return int(cand[0])


def choose(name, sub):
    isc, iss = sub.IS_CAGR.values, sub.IS_Sharpe.values
    if name == "C_SHARPE":
        return _argmax(iss, isc)
    if name == "C_CAGR":
        return _argmax(isc, iss)
    if name == "C_ISLEGS":
        return _argmax(sub.IS_legs_passed.values, iss)
    raise KeyError(name)


# =========================================================================================
# (3) main
# =========================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 996 (cloud lane, 2026-09-16) -- CENSUS THE RECORD'S SCREENED STATISTICS FOR A "
      "NAMED FALLBACK")
    P("=" * 100)
    P(f"  SMOKE={SMOKE}  headline cost {HEAD_COST:.0f} bps  LAG={LAG}  WARM={WARM}")
    P(f"  tuned axes: claim set {CLAIMSETS}  x  fallback {FALLBACKS} -- ALL reported")
    P(f"  reported ladders (not tuned): panel {PANELS} x book {BOOKORDER} x gross "
      f"{list(GROSSES)} x cadence {CADORDER} x cost {RUNGS}")
    P(f"  screens {SCREENS} (headline {HEAD_SCREEN}); choosers {CHOOSERS} "
      f"(headline {HEAD_CHOOSER})")

    # ================================================================== (A) THE CENSUS
    P()
    P("=" * 100)
    P("(A) THE CENSUS -- committed screen / eligibility / decline claims")
    P("=" * 100)
    P(f"  screen vocabulary   : {SCREEN_VOCAB}")
    P(f"  fallback vocabulary : {FALLBACK_VOCAB}")
    P(f"  surviving vocabulary: {SURV_VOCAB}")
    C = run_census()
    C2 = run_census()
    census_det = int((C.drop(columns=["src"]).values != C2.drop(columns=["src"]).values).sum())
    P(f"  corpus: {len(C):,} claim units "
      f"({int((C.src == 'LEADERBOARD.md').sum()):,} LEADERBOARD rows + "
      f"{int((C.src == 'CHANGELOG.md').sum()):,} CHANGELOG paragraphs)")

    crows = []
    for cs in CLAIMSETS:
        sel = C[C[cs]]
        n = len(sel)
        nf = int(sel.named_fb.sum())
        se = int(sel.surv_explicit.sum())
        si = int((~sel.named_fb).sum())          # surviving-picks-only by construction
        lo = int(sel.locatable.sum())
        crows.append(dict(claim_set=cs, n_claims=n, n_named_fallback=nf,
                          share_named=nf / n if n else np.nan,
                          n_surv_explicit=se, n_surv_implicit=si,
                          share_surv_implicit=si / n if n else np.nan,
                          n_locatable=lo, share_locatable=lo / n if n else np.nan))
        P(f"  {cs:6s}: {n:5,} claims | name a fallback {nf:5,} ({nf/max(n,1):.4f}) | "
          f"surviving-picks-only {si:5,} ({si/max(n,1):.4f}) | explicit surv vocab {se:4,} | "
          f"locatable {lo:5,} ({lo/max(n,1):.4f})")
    CEN = pd.DataFrame(crows)
    # per-source breakdown
    srows = []
    for cs in CLAIMSETS:
        for src in ["LEADERBOARD.md", "CHANGELOG.md"]:
            sel = C[C[cs] & (C.src == src)]
            n = len(sel)
            srows.append(dict(claim_set=cs, src=src, n_claims=n,
                              n_named_fallback=int(sel.named_fb.sum()),
                              n_surv_implicit=int((~sel.named_fb).sum()),
                              n_locatable=int(sel.locatable.sum())))
    dump(C, "census_claims.csv")
    dump(CEN, "census.csv")
    dump(pd.DataFrame(srows), "census_by_source.csv")

    # ================================================================== panels
    P()
    P("=" * 100)
    P("(B) THE LADDER -- rebuilt from scratch")
    P("=" * 100)
    PX = {}
    PX["U56"] = load_universe()
    PX["B136"] = load_universe(broad=True)
    PX["SMALL"], n_dropped = load_small()
    for k, v in PX.items():
        P(f"  {k:6s} {v.shape[1]:4d} cols  {v.index[0].date()} .. {v.index[-1].date()}  "
          f"({len(v):,} rows)")
    P(f"  SMALL dropped {n_dropped} tickers with max_1d_move >= 1.0 (data/small_meta.csv)")

    # ---------------------------------------------------------------- gates
    P()
    P("-" * 100)
    P("GATES -- printed before any hypothesis number")
    P("-" * 100)
    gates = []
    u56 = PX["U56"]
    bad = sum(int((offset_mask(u56.index, per).values != rebalance_mask(u56.index, per).values
                   ).sum()) for per in CADORDER)
    gates.append(dict(gate="G0", what="offset-0 mask == engine.rebalance_mask on D/W/M/Q",
                      value=float(bad), bar=0.0, ok=bad == 0))
    P(f"  G0  masks vs engine.rebalance_mask         : {bad} disagreeing rows")

    Wb = BOOKS["BAND03"](u56, 0.75)
    ref = backtest(u56, Wb, cost_bps=HEAD_COST, freq="W")
    ctx = Ctx(u56, offset_mask(u56.index, "W"))
    r0, t0v = ctx.run(shift1(Wb, u56.index))
    n0 = r0 - t0v * HEAD_COST / 1e4
    g1 = max(float(np.abs(n0[WARM:] - ref["returns"].values[WARM:]).max()),
             float(np.abs(t0v[WARM:] - ref["turnover"].values[WARM:]).max()))
    gates.append(dict(gate="G1", what="fast Ctx == engine.backtest (returns and turnover)",
                      value=g1, bar=1e-10, ok=g1 < 1e-10))
    P(f"  G1  Ctx vs engine.backtest                 : max|d| {g1:.3e}")

    g2 = float(np.abs(Wb.values - rules_v2_weights(u56).values).max())
    gates.append(dict(gate="G2", what="BAND03@0.75 == baseline.rules_v2_weights",
                      value=g2, bar=1e-12, ok=g2 < 1e-12))
    P(f"  G2  BAND03@0.75 vs rules_v2_weights        : max|d| {g2:.3e}")

    gates.append(dict(gate="G6", what="SMALL max_1d_move>=1.0 tickers dropped",
                      value=float(n_dropped), bar=1.0, ok=n_dropped >= 1))
    P(f"  G6  SMALL hygiene drop count               : {n_dropped}")
    gates.append(dict(gate="G7", what="census parse determinism (cells differing on re-parse)",
                      value=float(census_det), bar=0.0, ok=census_det == 0))
    P(f"  G7  census re-parse                        : {census_det} differing cells")

    # ---------------------------------------------------------------- build the ladder
    rows = []
    NET = {}
    for pname in PANELS:
        px = PX[pname]
        idx = px.index
        rspy = px["SPY"].pct_change().fillna(0.0).values
        isw = np.asarray(idx <= pd.Timestamp(IS_END))[WARM:]
        osw = np.asarray(idx >= pd.Timestamp(OOS_START))
        spy_f, spy_is, spy_o = mets(rspy[WARM:]), mets(rspy[WARM:][isw]), mets(rspy[osw])
        v2n = backtest(px, rules_v2_weights(px), cost_bps=HEAD_COST, freq="W")["returns"].values
        v2 = mets(v2n[WARM:])
        tw = {(b, gn): shift1(BOOKS[b](px, gv), idx)
              for b in BOOKORDER for gn, gv in GROSSES.items()}
        for cad in CADORDER:
            cx = Ctx(px, offset_mask(idx, cad))
            for b in BOOKORDER:
                for gn in GROSSES:
                    r, tu = cx.run(tw[(b, gn)])
                    for cb in RUNGS:
                        net = r - tu * cb / 1e4
                        mf = mets(net[WARM:])
                        mi = mets(net[WARM:][isw])
                        mo = mets(net[osw])
                        lg = dict(H1=mf["H1"] > spy_f["H1"], H2=mf["H2"] > spy_f["H2"],
                                  OOS=mo["Sharpe"] > spy_o["Sharpe"],
                                  DD=abs(mo["MaxDD"]) <= DD_CAP * abs(spy_f["MaxDD"]),
                                  CAGR=mo["CAGR"] >= CAGR_FLOOR * spy_f["CAGR"])
                        ilg = dict(H1=mi["H1"] > spy_is["H1"], H2=mi["H2"] > spy_is["H2"],
                                   OOS=mi["Sharpe"] > spy_is["Sharpe"],
                                   DD=abs(mi["MaxDD"]) <= DD_CAP * abs(spy_is["MaxDD"]),
                                   CAGR=mi["CAGR"] >= CAGR_FLOOR * spy_is["CAGR"])
                        rows.append(dict(
                            panel=pname, book=b, gross=gn, cadence=cad, phase=0, cost_bps=cb,
                            turn_per_yr=float(tu[WARM:].sum() / (len(tu[WARM:]) / 252.0)),
                            CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"],
                            H1=mf["H1"], H2=mf["H2"],
                            IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                            IS_H1=mi["H1"], IS_H2=mi["H2"],
                            OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                            spy_CAGR=spy_f["CAGR"], spy_Sharpe=spy_f["Sharpe"],
                            spy_MaxDD=spy_f["MaxDD"], spy_H1=spy_f["H1"], spy_H2=spy_f["H2"],
                            spy_OOS_CAGR=spy_o["CAGR"], spy_OOS_Sharpe=spy_o["Sharpe"],
                            spy_OOS_MaxDD=spy_o["MaxDD"],
                            v2_Sharpe=v2["Sharpe"], v2_MaxDD=v2["MaxDD"],
                            v2_H1=v2["H1"], v2_H2=v2["H2"],
                            IS_legs_passed=int(sum(ilg.values())),
                            IS_pass4b=bool(all(ilg.values())),
                            IS_leg_SHARPE=bool(ilg["OOS"]), IS_leg_DD=bool(ilg["DD"]),
                            pass4b=bool(all(lg.values())),
                            pass4a=bool(mf["H1"] > v2["H1"] and mf["H2"] > v2["H2"]
                                        and mf["MaxDD"] >= v2["MaxDD"]),
                            fail_legs=",".join(LEGNAME[k] for k in LEGS if not lg[k]) or "-"))
                        if cb == HEAD_COST:
                            NET[(pname, b, gn, cad)] = net
        P(f"  {pname:6s} built {len(BOOKORDER)*len(GROSSES)*len(CADORDER)*len(RUNGS):,} rows "
          f"({time.time()-t0:.0f}s)")
    L = pd.DataFrame(rows)
    dump(L, "ladder.csv")

    # ---------------------------------------------------------------- G3 cross-run
    g3, g3n = np.inf, "parent ladder not found"
    if PARENT_LADDER.exists():
        PL = pd.read_csv(PARENT_LADDER)
        PL = PL[PL.phase == 0]
        key = ["panel", "book", "gross", "cadence", "cost_bps"]
        m = L.merge(PL, on=key, suffixes=("", "_p"))
        d = [float(np.abs(m[c].values - m[c + "_p"].values).max()) for c in G3_COLS
             if c + "_p" in m.columns]
        g3 = max(d) if d else np.inf
        g3n = f"{len(m)} rows x {len(d)} cols"
    gates.append(dict(gate="G3", what=f"CROSS-RUN idea 993 ladder phase-0 ({g3n})",
                      value=g3, bar=G3_TOL, ok=g3 < G3_TOL))
    P(f"  G3  cross-run vs 993's committed ladder    : max|d| {g3:.3e}  [{g3n}]")

    # ---------------------------------------------------------------- G4/G5
    fbser = {}
    for pname in PANELS:
        px = PX[pname]
        fbser[(pname, "FB_CASH")] = np.zeros(len(px))
        fbser[(pname, "FB_SPY")] = px["SPY"].pct_change().fillna(0.0).values
        fbser[(pname, "FB_LIVE")] = backtest(px, rules_v2_weights(px), cost_bps=HEAD_COST,
                                             freq="W")["returns"].values
    g4a = max(float(np.abs(fbser[(p, "FB_CASH")]).max()) for p in PANELS)
    g4b = max(float(np.abs(fbser[(p, "FB_SPY")] - PX[p]["SPY"].pct_change().fillna(0.0).values
                           ).max()) for p in PANELS)
    # engine.backtest emits NaN on the first rows of B136/SMALL (all-NaN prices at the panel
    # start, rows 0 and 3, both far inside the warm-up); G1's post-warm-up convention is used.
    g4c = max(float(np.abs(fbser[(p, "FB_LIVE")][WARM:]
                           - NET[(p, "BAND03", "CORE", "W")][WARM:]).max()) for p in PANELS)
    for tag, v, what in [("G4a", g4a, "FB_CASH is exactly a zero return series"),
                         ("G4b", g4b, "FB_SPY is exactly the panel's SPY series"),
                         ("G4c", g4c, "FB_LIVE == this run's (BAND03,CORE,W) row, post warm-up")]:
        gates.append(dict(gate=tag, what=what, value=v, bar=1e-12, ok=v < 1e-12))
        P(f"  {tag} {what:42s}: max|d| {v:.3e}")

    cx = Ctx(u56, offset_mask(u56.index, "M"))
    rr, tt = cx.run(shift1(BOOKS["TOP20"](u56, 0.75), u56.index))
    g5 = float(np.abs((rr - tt * HEAD_COST / 1e4) - NET[("U56", "TOP20", "CORE", "M")]).max())
    gates.append(dict(gate="G5", what="determinism: one ladder cell rebuilt", value=g5,
                      bar=0.0, ok=g5 == 0.0))
    P(f"  G5  determinism (U56/TOP20/CORE/M)         : max|d| {g5:.3e}")
    G = pd.DataFrame(gates)
    dump(G, "gates.csv")
    P(f"  GATES: {int(G.ok.sum())} of {len(G)} PASS")

    # ================================================================== (C) the screens
    P()
    P("=" * 100)
    P("(C) SCREENED vs CONTROL -- 24 slots, 3 screens, 3 choosers, 4 fallbacks, 5 cost rungs")
    P("=" * 100)

    def admitted(sub, scr):
        if scr == "S_IS4B":
            return sub.IS_pass4b.values
        if scr == "S_ISSHARPE":
            return sub.IS_leg_SHARPE.values
        if scr == "S_ISDD":
            return sub.IS_leg_DD.values
        raise KeyError(scr)

    prows = []
    for cb in RUNGS:
        Lc = L[L.cost_bps == cb]
        for pname in PANELS:
            for cad in CADORDER:
                for gn in GROSSES:
                    sub = Lc[(Lc.panel == pname) & (Lc.cadence == cad)
                             & (Lc.gross == gn)].reset_index(drop=True)
                    for ch in CHOOSERS:
                        ic = choose(ch, sub)
                        ctl = sub.iloc[ic]
                        for scr in SCREENS:
                            adm = admitted(sub, scr)
                            if adm.any():
                                s2 = sub[adm].reset_index(drop=True)
                                isx = choose(ch, s2)
                                pick = s2.iloc[isx]
                                ref_flag = False
                            else:
                                pick, ref_flag = None, True
                            prows.append(dict(
                                cost_bps=cb, panel=pname, cadence=cad, gross=gn,
                                chooser=ch, screen=scr, n_admitted=int(adm.sum()),
                                refused=ref_flag,
                                ctl_book=ctl.book, ctl_OOS_Sharpe=ctl.OOS_Sharpe,
                                ctl_OOS_CAGR=ctl.OOS_CAGR, ctl_OOS_MaxDD=ctl.OOS_MaxDD,
                                ctl_4b=bool(ctl.pass4b), ctl_4a=bool(ctl.pass4a),
                                scr_book=(pick.book if pick is not None else "-"),
                                scr_OOS_Sharpe=(pick.OOS_Sharpe if pick is not None else np.nan),
                                scr_OOS_CAGR=(pick.OOS_CAGR if pick is not None else np.nan),
                                scr_OOS_MaxDD=(pick.OOS_MaxDD if pick is not None else np.nan),
                                scr_4b=(bool(pick.pass4b) if pick is not None else False),
                                scr_4a=(bool(pick.pass4a) if pick is not None else False),
                                spy_OOS_Sharpe=ctl.spy_OOS_Sharpe,
                                spy_OOS_CAGR=ctl.spy_OOS_CAGR,
                                spy_MaxDD=ctl.spy_MaxDD, spy_CAGR=ctl.spy_CAGR))
    PK = pd.DataFrame(prows)
    dump(PK, "picks.csv")
    P(f"  refusal rate by screen (10 bps, {HEAD_CHOOSER}):")
    h = PK[(PK.cost_bps == HEAD_COST) & (PK.chooser == HEAD_CHOOSER)]
    for scr in SCREENS:
        s = h[h.screen == scr]
        P(f"    {scr:11s} refused {int(s.refused.sum()):2d} of {len(s):2d} slots  "
          f"(median admitted {s.n_admitted.median():.1f} of 5)")

    # ---- the fallback-paid statistics ----------------------------------------------------
    FBSTAT = {}
    for pname in PANELS:
        px = PX[pname]
        osw = np.asarray(px.index >= pd.Timestamp(OOS_START))
        spy_f = mets(px["SPY"].pct_change().fillna(0.0).values[WARM:])
        for fb in PAID_FB:
            mo = mets(fbser[(pname, fb)][osw])
            FBSTAT[(pname, fb)] = dict(OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"],
                                       OOS_MaxDD=mo["MaxDD"])

    arows = []
    for cb in RUNGS:
        for ch in CHOOSERS:
            for scr in SCREENS:
                base = PK[(PK.cost_bps == cb) & (PK.chooser == ch) & (PK.screen == scr)]
                for fb in FALLBACKS:
                    d = base.copy()
                    if fb == "FB_DROP":
                        d = d[~d.refused]
                    else:
                        for i in d.index[d.refused]:
                            st = FBSTAT[(d.at[i, "panel"], fb)]
                            d.at[i, "scr_OOS_Sharpe"] = st["OOS_Sharpe"]
                            d.at[i, "scr_OOS_CAGR"] = st["OOS_CAGR"]
                            d.at[i, "scr_OOS_MaxDD"] = st["OOS_MaxDD"]
                            d.at[i, "scr_4b"] = False
                            d.at[i, "scr_4a"] = False
                    ds = d.scr_OOS_Sharpe.values - d.ctl_OOS_Sharpe.values
                    dc = d.scr_OOS_CAGR.values - d.ctl_OOS_CAGR.values
                    dd = np.abs(d.scr_OOS_MaxDD.values) - np.abs(d.ctl_OOS_MaxDD.values)
                    arows.append(dict(
                        cost_bps=cb, chooser=ch, screen=scr, fallback=fb,
                        n_slots=len(d), n_refused=int(base.refused.sum()),
                        mean_dSharpe=float(np.nanmean(ds)) if len(ds) else np.nan,
                        med_dSharpe=float(np.nanmedian(ds)) if len(ds) else np.nan,
                        win_Sharpe=float(np.nanmean(ds > 0)) if len(ds) else np.nan,
                        mean_dCAGR=float(np.nanmean(dc)) if len(dc) else np.nan,
                        mean_dMaxDD=float(np.nanmean(dd)) if len(dd) else np.nan,
                        scr_4b=int(d.scr_4b.sum()), ctl_4b=int(d.ctl_4b.sum()),
                        scr_4a=int(d.scr_4a.sum()), ctl_4a=int(d.ctl_4a.sum())))
    A = pd.DataFrame(arows)
    dump(A, "paid.csv")

    P()
    P(f"  HEADLINE CELL: screen {HEAD_SCREEN}, chooser {HEAD_CHOOSER}, {HEAD_COST:.0f} bps")
    hh = A[(A.cost_bps == HEAD_COST) & (A.chooser == HEAD_CHOOSER) & (A.screen == HEAD_SCREEN)]
    P("   " + hh[["fallback", "n_slots", "n_refused", "mean_dSharpe", "med_dSharpe",
                  "win_Sharpe", "mean_dCAGR", "mean_dMaxDD", "scr_4b", "ctl_4b"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P()
    P("  mean dSharpe by (screen x fallback), all choosers pooled, 10 bps:")
    pv = A[A.cost_bps == HEAD_COST].pivot_table(index=["screen", "chooser"],
                                                columns="fallback", values="mean_dSharpe")
    pv = pv.reindex(columns=FALLBACKS)
    P("   " + pv.to_string(float_format=lambda x: f"{x:+.4f}").replace("\n", "\n   "))

    # ================================================================== (D) hypotheses
    P()
    P("=" * 100)
    P("(D) PRE-REGISTERED HYPOTHESES")
    P("=" * 100)
    hyp = []

    def H(tag, what, val, bar, ok, note=""):
        hyp.append(dict(H=tag, what=what, value=val, bar=bar, passed=bool(ok), note=note))
        P(f"  {tag:9s} {'PASS' if ok else 'FAIL'} at {val:.4f}  (bar {bar})  {what}")
        if note:
            P(f"            {note}")

    st = CEN[CEN.claim_set == "STRICT"].iloc[0]
    wd = CEN[CEN.claim_set == "WIDE"].iloc[0]
    H("H_NAMED", ">= 0.50 of STRICT screened statistics name a fallback",
      float(st.share_named), BAR_NAMED, st.share_named >= BAR_NAMED,
      f"STRICT {int(st.n_named_fallback)} of {int(st.n_claims)}; "
      f"WIDE {int(wd.n_named_fallback)} of {int(wd.n_claims)} ({wd.share_named:.4f})")
    H("H_SURV", ">= 0.50 of STRICT screened statistics are surviving-picks-only",
      float(st.share_surv_implicit), BAR_SURV, st.share_surv_implicit >= BAR_SURV,
      f"explicit surviving-picks vocabulary appears in only "
      f"{int(st.n_surv_explicit)} of {int(st.n_claims)}")
    H("H_LOC", ">= 0.25 of STRICT screened statistics are locatable on disk",
      float(st.share_locatable), BAR_LOC, st.share_locatable >= BAR_LOC,
      f"{int(st.n_locatable)} of {int(st.n_claims)} name an existing .py/.csv")

    drop = float(hh[hh.fallback == "FB_DROP"].mean_dSharpe.iloc[0])
    cash = float(hh[hh.fallback == "FB_CASH"].mean_dSharpe.iloc[0])
    spyv = float(hh[hh.fallback == "FB_SPY"].mean_dSharpe.iloc[0])
    live = float(hh[hh.fallback == "FB_LIVE"].mean_dSharpe.iloc[0])
    H("H_DROP", "FB_DROP overstates mean dSharpe vs FB_CASH by >= 0.10",
      drop - cash, BAR_DROP, (drop - cash) >= BAR_DROP,
      f"FB_DROP {drop:+.4f} / FB_CASH {cash:+.4f} / FB_SPY {spyv:+.4f} / FB_LIVE {live:+.4f}")

    flips = 0
    flipcells = []
    for cb in RUNGS:
        for scr in SCREENS:
            for ch in CHOOSERS:
                v = A[(A.cost_bps == cb) & (A.screen == scr)
                      & (A.chooser == ch)].set_index("fallback").mean_dSharpe
                v = v.reindex(FALLBACKS).values
                if np.nanmin(v) < 0 < np.nanmax(v):
                    flips += 1
                    flipcells.append(f"{scr}/{ch}/{cb:.0f}bps")
    H("H_SIGN", ">= 1 (screen, chooser, cost) cell where the sign flips with the fallback",
      float(flips), 1.0, flips >= 1,
      f"{flips} of {len(RUNGS)*len(SCREENS)*len(CHOOSERS)} cells; e.g. {flipcells[:4]}")

    paidmin = min(cash, spyv, live)
    H("H_PAID", "headline screen's gain >= 0 under ALL THREE paid fallbacks",
      paidmin, 0.0, paidmin >= 0.0,
      f"worst paid fallback is "
      f"{['FB_CASH','FB_SPY','FB_LIVE'][int(np.argmin([cash,spyv,live]))]}")

    best4b = int(hh.scr_4b.max())
    ctl4b = int(hh.ctl_4b.max())
    H("H_4B", "the screen buys >= 1 OOS 4b pass the control does not have",
      float(best4b - ctl4b), 1.0, (best4b - ctl4b) >= 1,
      f"screened best {best4b}, control {ctl4b} of 24 slots")
    n4a = int(L.pass4a.sum()) + int(PK.scr_4a.sum()) + int(PK.ctl_4a.sum())
    H("H_4A", ">= 1 OOS 4a anywhere in this run", float(n4a), 1.0, n4a >= 1,
      f"{int(L.pass4a.sum())} of {len(L):,} ladder rows")
    HY = pd.DataFrame(hyp)
    dump(HY, "hypotheses.csv")
    P(f"  HYPOTHESES: {int(HY.passed.sum())} of {len(HY)} PASS")

    # ================================================================== (E) rule 8
    P()
    P("=" * 100)
    P("(E) RULE 8 -- every pick is IS-only, the OOS window is read ONCE")
    P("=" * 100)
    w = PK[(PK.cost_bps == HEAD_COST)]
    for scr in SCREENS:
        s = w[w.screen == scr]
        P(f"  {scr:11s}: OOS 4b screened {int(s.scr_4b.sum()):2d} of {len(s):2d} picks | "
          f"control {int(s.ctl_4b.sum()):2d} | OOS 4a screened {int(s.scr_4a.sum())} "
          f"control {int(s.ctl_4a.sum())}")
    P(f"  ladder-wide: OOS 4b {int(L[L.cost_bps==HEAD_COST].pass4b.sum())} of "
      f"{len(L[L.cost_bps==HEAD_COST]):,} rows | OOS 4a "
      f"{int(L[L.cost_bps==HEAD_COST].pass4a.sum())}")

    P()
    P("  BEST SCREENED PICK by OOS Sharpe (10 bps, headline screen+chooser), with SPY and "
      "RULES v2 beside it:")
    hp = PK[(PK.cost_bps == HEAD_COST) & (PK.chooser == HEAD_CHOOSER)
            & (PK.screen == HEAD_SCREEN) & (~PK.refused)]
    if len(hp):
        b = hp.sort_values("scr_OOS_Sharpe", ascending=False).iloc[0]
        lr = L[(L.cost_bps == HEAD_COST) & (L.panel == b.panel) & (L.book == b.scr_book)
               & (L.gross == b.gross) & (L.cadence == b.cadence)].iloc[0]
        P(f"    {b.panel}/{b.scr_book}/{b.gross}/{b.cadence}: full {lr.CAGR:.2%} / "
          f"{lr.Sharpe:.4f} / {lr.MaxDD:.2%}  halves {lr.H1:.4f}/{lr.H2:.4f}  "
          f"OOS {lr.OOS_CAGR:.2%} / {lr.OOS_Sharpe:.4f} / {lr.OOS_MaxDD:.2%}  "
          f"4b {lr.pass4b}  4a {lr.pass4a}  fail_legs {lr.fail_legs}")
        P(f"    SPY : full {lr.spy_CAGR:.2%} / {lr.spy_Sharpe:.4f} / {lr.spy_MaxDD:.2%}  "
          f"halves {lr.spy_H1:.4f}/{lr.spy_H2:.4f}  OOS {lr.spy_OOS_CAGR:.2%} / "
          f"{lr.spy_OOS_Sharpe:.4f} / {lr.spy_OOS_MaxDD:.2%}")
        P(f"    RULES v2 (live): Sharpe {lr.v2_Sharpe:.4f}  MaxDD {lr.v2_MaxDD:.2%}  "
          f"halves {lr.v2_H1:.4f}/{lr.v2_H2:.4f}")

    P()
    P("  COST ROBUSTNESS of the headline gap (mean dSharpe, headline screen+chooser):")
    cr = A[(A.chooser == HEAD_CHOOSER) & (A.screen == HEAD_SCREEN)].pivot_table(
        index="cost_bps", columns="fallback", values="mean_dSharpe").reindex(columns=FALLBACKS)
    P("   " + cr.to_string(float_format=lambda x: f"{x:+.4f}").replace("\n", "\n   "))

    P()
    P(f"  SURVIVORSHIP (rule 9): U56/B136/SMALL are current-constituent lists; SMALL drops "
      f"{n_dropped} names with max_1d_move >= 1.0. Every LEVEL is optimistic and every 4b "
      f"count is an UPPER bound. The measured object is a DIFFERENCE between two choosers on "
      f"the same names and tape, so the bias very largely cancels.")
    P(f"  elapsed {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
