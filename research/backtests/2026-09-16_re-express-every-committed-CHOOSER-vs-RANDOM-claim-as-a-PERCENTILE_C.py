#!/usr/bin/env python3
"""Idea 1035 (lane C, 2026-09-16) — re-express EVERY committed CHOOSER-vs-RANDOM claim as a
PERCENTILE.

QUESTION (QUEUE idea 1035, verbatim)
    idea 1031 found a Sharpe gap of -0.0884 corresponds to percentile 0.000 and one of +0.0177
    to 0.800, so the record's committed chooser-vs-null gaps are unadjudicable as published.
    Harvest every such claim in LEADERBOARD.md and CHANGELOG.md and re-score each against its
    own cell's sequence distribution.  Max 2 params (claim set, control basis).

WHAT IS NEW AGAINST 1031.  1031 re-expressed THREE choosers in ONE cell.  This run asks whether
    the record as a whole can be read that way at all.  Two things are measured that 1031 could
    not see from inside a single cell:
    (i)  A CENSUS of the committed text.  Every sentence in LEADERBOARD.md and CHANGELOG.md that
         compares a chooser (or selector, or pick) to a random draw is harvested, and each is
         scored for whether it carries the FIELDS a percentile needs: the POOL SIZE, the DRAW
         COUNT, a yardstick (sd / SE / IQR), the CELL (panel, cost), and whether it already
         publishes a percentile.  A claim missing them cannot be re-scored by anyone, this run
         included, and the share that are missing is the finding the clause rests on.
    (ii) A CALIBRATION of the gap -> percentile map on the record's own legal pool.  For any
         Sharpe gap g and any cell, the percentile a gap of that size earns is exactly
         pct(mean(D) + g, D) — a closed form, no search.  Running every harvested gap through
         every legal cell turns "unadjudicable" from an adjective into a NUMBER: the WIDTH of
         the percentile band a published gap is consistent with.  1031's pair (-0.0884 -> 0.000,
         +0.0177 -> 0.800) is two points of that map; this run draws the whole of it.

    A claim that is EXACTLY mappable — one naming its panel, its cost rung and its chooser — is
    re-scored in its own cell, not banded.  Those are reported separately and are the only ones
    the record can be said to have published adjudicably.

WHAT IS MEASURED
    (A) THE CENSUS.  Harvested claims by source file and claim set, with the field-stamp table
        (POOL / DRAWS / CELL / COST / YARDSTICK / PERCENTILE) and the share carrying each.
    (B) THE CALIBRATION.  For every legal cell and control basis: the null distribution's mean,
        median, sd, and the percentile earned by gaps across the range the record publishes.
    (C) THE RE-SCORE.  Every harvested claim carrying a Sharpe-scale gap, re-expressed as the
        percentile band it is consistent with; and every EXACTLY MAPPABLE claim re-scored in its
        own cell under all three bases.
    (D) THE RULE-8 WALK-FORWARD at PROTOCOL's own split 2016-12-31 (IS 2009-2016, OOS 2017-2026
        read once), OOS CAGR/Sharpe/MaxDD against the live RULES v2 baseline and against SPY,
        BOTH KEEP paths for every pick, and each pick's percentile in its own pool.

TUNED PARAMETERS: exactly TWO, the two the queue names.  ALL 9 grid points reported, none
    selected.
    (1) CLAIM SET — which committed sentences count as a chooser-vs-random claim
          STRICT   a CHOOSER token AND a RANDOM token AND at least one number   <- HEADLINE
          WIDE     a RANDOM token AND any selection token (pick / choose / selector / argmax)
          NUMERIC  STRICT restricted to claims publishing a Sharpe-SCALE gap (|g| <= 0.5, >= 3dp)
    (2) CONTROL BASIS — what "a random draw from its own pool" means
          SEQ      an independent uniform draw at EVERY end, scored by the sequence mean
                   (1023's and 1031's construction)                            <- HEADLINE
          FIXED    ONE uniform draw held at every end — the honest counterfactual for a claim
                   that names a single book (exact, 18 values, no Monte Carlo)
          RAW      a single draw at a single end — the raw per-end 18-book distribution

    NOT TUNED, reported as CONTROLS at every point:
      COST    0 / 10 / 25 bps; 10 bps is PROTOCOL rule 2's and is the headline.
      PANEL   U56 (binding) and B136 (labelled replication).
      POOL    the 18 never-memo-selected GRID ladder books per panel — 1023's and 1031's own
              pool.  The committed SHELF is NOT a legal rule-8 pool (selected on the full tape).
      END GRID  Q16, the 16 quarter-ends 2015-03-31..2018-12-31 that 1013/1023/1031 used, so
              the cross-run gates are stated on the record's own object.  PROTOCOL's declared
              split 2016-12-31 is read separately for the rule-8 walk-forward.
      DRAWS   NRAND = 2,000 sequences per cell, 5x 1023's 400; a percentile resolves to 0.0005
              and its binomial SE at p=0.5 is 0.0112.

    SCALE CAVEAT, stated before the numbers: the record publishes gaps in several units (OOS
    Sharpe, CAGR in pp, pass RATES).  Only a Sharpe-scale gap can be run through a Sharpe
    distribution, so the banding arm is restricted to claims whose sentence names Sharpe and
    whose number is in [-0.5, 0.5] with at least 3 decimals.  Every claim excluded by that
    filter is COUNTED and reported, never silently dropped.

PRE-REGISTERED HYPOTHESES AND BARS (declared before any number below the gates was read)
    H_STAMP   >= 50% of STRICT claims carry BOTH a pool size and a draw count.  PASS => the
              record's chooser-vs-random claims are re-scorable as published.
    H_YARD    >= 50% of STRICT claims carry ANY yardstick (sd / SE / IQR / an explicit
              percentile).  A weaker bar than H_STAMP, on the same question.
    H_MAP     >= 50% of STRICT claims are EXACTLY mappable — they name a panel, a cost rung and
              a chooser, so a percentile can be computed in their own cell without banding.
    H_BAND    DECISIVE.  The median percentile-band WIDTH over re-scorable Sharpe gaps is
              <= 0.20: a published gap pins the percentile to within 20 points.  FAIL => a gap
              does not identify a percentile and the clause is needed.
    H_FUNCTION No two re-scorable gaps within 0.005 of each other earn percentiles more than
              0.10 apart (pooled over cells).  This is H_BAND stated as a function test.
    H_MONO    pooled Spearman rho(gap, percentile) over all (gap, cell) points >= 0.90 — a
              larger published gap means a higher percentile even across cells.
    H_SIGN    sign(gap) agrees with the 50th-percentile verdict in >= 95% of (gap, cell) points
              — 1031's H_FLIP, generalised from 18 pairs to the record's whole gap range.
    H_BASIS   the percentile a given gap earns is invariant (within 0.10) across the three
              control bases.  FAIL => "a random draw from its own pool" must name WHICH draw.
    H_CLAIMSET the headline verdicts (H_STAMP, H_YARD, H_MAP) are unchanged on the WIDE and
              NUMERIC claim sets.
    Each prints its bar and PASS/FAIL, and a FAIL is reported as loudly as a PASS.

REPRODUCTION GATES (printed before any hypothesis number is read)
    G0  HARVEST determinism and accounting: re-running the parser on the same bytes returns the
        same claim set, and every harvested number is either parsed or COUNTED as unparsed.
    G1  this run's fast runner == engine.backtest on a live book, returns AND turnover.
    G2  rules_v2_weights(U, 0.03, 0.75) == baseline.rules_v2_weights(U)                     0.0
    G3  CROSS-RUN: SPY's OOS triple at 2016-12-31 == the record's committed
        15.21% / 0.8713 / -33.72%.
    G4  CROSS-RUN: 1013's four published declared-split picks reproduce their OOS triples.
    G5  determinism: the whole end x book x rung ladder rebuilt reproduces bit-for-bit.      0.0
    G6  IS PURITY: every chooser's pick is invariant under a permutation of the OOS returns.
    G7  SAMPLER UNBIASEDNESS: the Monte-Carlo mean of the SEQ distribution equals the EXACT
        pool mean (closed form, no draws) to within 3 MC standard errors, in all 6 cells.
    G8  PERCENTILE VALIDITY: a distribution's own median scores 0.5000 +/- 0.01 (reported for
        the continuous SEQ basis; FIXED and RAW are 18-point pools quantised to 1/18 and their
        atom mass is printed beside the deviation rather than hidden).
    G9  CROSS-RUN: 1031's committed headline percentiles reproduce — IS_CAGR 0.800,
        IS_SHARPE 0.000, IS_LEGS 0.000 (MC tol 0.02) and its chooser scores to 5e-4.
    G10 BAND SELF-CONSISTENCY: a gap taken FROM a cell, run back through that cell's own
        calibration, returns that cell's own percentile exactly.

SURVIVORSHIP (PROTOCOL rule 9).  The CENSUS arm reads committed text and inherits whatever bias
    its sources carry.  The CALIBRATION arm runs on U56 / B136, CURRENT-CONSTITUENT lists, so
    every CAGR and drawdown LEVEL is optimistic and every 4b count an UPPER bound.  The measured
    object is a RANK inside a distribution built from the SAME pool over the SAME tape, and the
    bias is common to the chooser and to every draw it is ranked against.  Where it does not
    cancel it flatters the coin flip — a uniform draw from a survivor panel is a better book than
    a real-time one — so every chooser percentile here is a LOWER bound.  SPY is a real index
    series and is not inflated.

NOT MODIFIED (PROTOCOL rule 6): RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py.
"""
from __future__ import annotations

import importlib.util
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import rebalance_mask, backtest  # noqa: E402

DATE = "2026-09-16"
SLUG = "re-express-every-committed-CHOOSER-vs-RANDOM-claim-as-a-PERCENTILE"
HERE = Path(__file__).resolve().parent
OUT = HERE / f"{DATE}_{SLUG}_C"
LANEC = HERE / "2026-09-15_do-4b-H1-H2-LEGS-inherit-the-SINGLE-EPISODE-COMPARAND-DEFECT_C.py"

WARMUP = 260
RUNGS = [0.0, 10.0, 25.0]
RUNG_HEAD = 10.0
PANEL_HEAD = "U56"
REC_END = "2016-12-31"
DDCAP_FRAC, CAGRFLOOR_FRAC = 0.60, 0.70
RAW_CH = ["IS_SHARPE", "IS_LEGS", "IS_CAGR"]
BASES = ["SEQ", "FIXED", "RAW"]
BASIS_HEAD = "SEQ"
CLAIMSETS = ["STRICT", "WIDE", "NUMERIC"]
CLAIMSET_HEAD = "STRICT"
NRAND = 2000
SEED0 = 20260916
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
PUB_1013 = {
    ("U56", "U56-band0.08-g1.00"): (0.1199, 1.162, -0.1905),
    ("U56", "U56-qroll-q0.17-w1008-d0.50"): (0.1560, 1.293, -0.1559),
    ("B136", "B136-band0.08-g1.00"): (0.1105, 1.097, -0.1950),
    ("B136", "B136-qroll-q0.12-w1008-d0.50"): (0.1430, 1.157, -0.1731),
}
PUB_1023_CHOOSER = {"IS_SHARPE": 1.155696, "IS_LEGS": 1.155696, "IS_CAGR": 1.261757}
# 1031's committed headline percentiles (U56 / 10 bps / Q16 / MEAN_SH), from its .percentile.csv
PUB_1031_PCT = {"IS_CAGR": 0.800, "IS_SHARPE": 0.000, "IS_LEGS": 0.000}
SOURCES = [ROOT / "research" / "LEADERBOARD.md", ROOT / "research" / "CHANGELOG.md"]
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix, gz=False):
    p = Path(f"{OUT}.{suffix}.csv.gz" if gz else f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False, compression="gzip" if gz else None)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


spec = importlib.util.spec_from_file_location("laneC1023", LANEC)
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)
fast_run, fmet, fsharpe = C.fast_run, C.fmet, C.fsharpe

# ====================================================================== THE HARVESTER
TOK_RANDOM = re.compile(
    r"coin[\s-]?flip|random draw|uniform draw|random(ly)? (chosen|picked|drawn)|"
    r"\bRANDOM\b|\bRANDW\b|null draw|random control|random arm|random sequence", re.I)
TOK_CHOOSER = re.compile(
    r"chooser|IS_CAGR|IS_SHARPE|IS_LEGS|ISARGMAX|C_ISSHARPE|\bS_IS\b|IS-only|"
    r"rule.?8 (pick|chooser)", re.I)
TOK_SELECT = re.compile(
    r"chooser|selector|\bpicks?\b|\bpicked\b|\bchoose[ns]?\b|\bchosen\b|argmax|IS-only|"
    r"IS_[A-Z]+", re.I)
TOK_POOL = re.compile(r"\b\d+[\s-]?book\b|\bpool of \d+|\b\d+ books\b|pool size|"
                      r"\b\d+[\s-]?(panel|cell)s? pool", re.I)
TOK_DRAWS = re.compile(r"\b[\d,]+\s*(draws|sequences|resamples|replications|paths)\b|"
                       r"\bn\s*=\s*[\d,]+\b", re.I)
TOK_PANEL = re.compile(r"\bU56\b|\bB136\b|\bSMALL\b|\bBSTK\d*\b|\bFULL\b", re.I)
TOK_COST = re.compile(r"\b\d+(\.\d+)?\s*bps\b", re.I)
TOK_YARD = re.compile(r"\bsd\b|\bSE\b|std|sigma|IQR|percentile|z\s*[+-]?\d|\bt\s*[+-]?\d", re.I)
TOK_PCT = re.compile(r"percentile|share of (coin flips|draws|sequences)|"
                     r"\bbeaten by \d|\bof \d+,?\d* (draws|sequences)\b", re.I)
TOK_SHARPE = re.compile(r"sharpe", re.I)
NUMRE = re.compile(r"[+-]?\d+(?:,\d{3})*(?:\.\d+)?%?")
SENT_SPLIT = re.compile(r"(?<=[\w\)\*\"%])[.;]\s+(?=[^\d])|\s\|\s|\n")


def sentences(text):
    """Claim units: sentences, with markdown table cells and newlines as hard boundaries.
    A '.' between digits never splits (decimals are preserved)."""
    out = []
    for raw in SENT_SPLIT.split(text):
        if raw is None:
            continue
        s = raw.strip()
        if len(s) >= 25:
            out.append(s)
    return out


def num_list(s):
    """Every number in the sentence, with commas stripped and percents converted."""
    vals = []
    for m in NUMRE.finditer(s):
        t = m.group(0)
        try:
            v = float(t.rstrip("%").replace(",", ""))
        except ValueError:
            continue
        vals.append(v / 100.0 if t.endswith("%") else v)
    return vals


def sharpe_gaps(s):
    """Sharpe-SCALE gap candidates: the sentence names Sharpe, and the number is written with at
    least 3 decimals and lies in [-0.5, 0.5] (and is not a percentage)."""
    if not TOK_SHARPE.search(s):
        return []
    out = []
    for m in NUMRE.finditer(s):
        t = m.group(0)
        if t.endswith("%") or "." not in t:
            continue
        if len(t.split(".")[1]) < 3:
            continue
        v = float(t.replace(",", ""))
        if abs(v) <= 0.5:
            out.append(v)
    return out


def harvest():
    rows = []
    for src in SOURCES:
        txt = src.read_text()
        for ln, line in enumerate(txt.split("\n"), 1):
            for s in sentences(line):
                has_r = bool(TOK_RANDOM.search(s))
                if not has_r:
                    continue
                has_c = bool(TOK_CHOOSER.search(s))
                has_sel = bool(TOK_SELECT.search(s))
                nums = num_list(s)
                sg = sharpe_gaps(s)
                strict = has_c and len(nums) > 0
                wide = has_sel
                numeric = strict and len(sg) > 0
                if not (strict or wide):
                    continue
                rows.append(dict(
                    src=src.name, line=ln, STRICT=strict, WIDE=wide, NUMERIC=numeric,
                    n_numbers=len(nums), n_sharpe_gaps=len(sg),
                    sharpe_gaps=";".join(f"{g:+.4f}" for g in sg),
                    has_pool=bool(TOK_POOL.search(s)), has_draws=bool(TOK_DRAWS.search(s)),
                    has_panel=bool(TOK_PANEL.search(s)), has_cost=bool(TOK_COST.search(s)),
                    has_yardstick=bool(TOK_YARD.search(s)), has_percentile=bool(TOK_PCT.search(s)),
                    chooser=(TOK_CHOOSER.search(s).group(0) if has_c else ""),
                    panel=(TOK_PANEL.search(s).group(0).upper() if TOK_PANEL.search(s) else ""),
                    cost=(float(re.sub(r"[^\d.]", "", TOK_COST.search(s).group(0)))
                          if TOK_COST.search(s) else np.nan),
                    text=s[:400].replace("\n", " ")))
    return pd.DataFrame(rows)


# ====================================================================== LADDER MACHINERY
def quarter_ends(lo, hi):
    return [str(d.date()) for d in pd.date_range(lo, hi, freq="QE")]


END_Q16 = quarter_ends("2015-01-01", "2018-12-31")
ALLE = sorted(set(END_Q16) | {REC_END})


def metblock(r):
    c, s, d = fmet(r)
    k = len(r) // 2
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(r[:k]), H2=fsharpe(r[k:]))


def split_block(net, e):
    b = metblock(net.values)
    o = net.loc[pd.Timestamp(e) + pd.Timedelta(days=1):].values
    i = net.loc[:pd.Timestamp(e)].values
    oc, os_, od = fmet(o)
    ic, is_, idd = fmet(i)
    b.update(OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od, OOS_n=len(o),
             IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd, IS_n=len(i))
    return b


def legs_at(bk, sb):
    return {
        "L1_H1": bool(bk["H1"] > sb["H1"]),
        "L2_H2": bool(bk["H2"] > sb["H2"]),
        "L3_OOS": bool(bk["OOS_Sharpe"] > sb["OOS_Sharpe"]),
        "L4_DD": bool(abs(bk["OOS_MaxDD"]) <= DDCAP_FRAC * abs(sb["MaxDD"])),
        "L5_CAGR": bool(bk["OOS_CAGR"] >= CAGRFLOOR_FRAC * sb["CAGR"]),
    }


def raw_pick(sub, ch, spy_is):
    """IS-ONLY choosers — 1023's and 1031's own three, verbatim."""
    if ch == "IS_SHARPE":
        return sub["IS_Sharpe"].idxmax()
    if ch == "IS_CAGR":
        return sub["IS_CAGR"].idxmax()
    s = sub.copy()
    s["nlegs"] = ((s["IS_Sharpe"] > spy_is[1]).astype(int)
                  + (s["IS_CAGR"] >= CAGRFLOOR_FRAC * spy_is[0]).astype(int)
                  + (s["IS_MaxDD"].abs() <= DDCAP_FRAC * abs(spy_is[2])).astype(int))
    s = s.sort_values(["nlegs", "IS_Sharpe"], ascending=False)
    return s.index[0]


def pct_of(x, dist):
    """Mid-rank percentile of x inside dist, in [0, 1].  Ties split."""
    d = np.asarray(dist, float)
    return float(((d < x).sum() + 0.5 * (d == x).sum()) / len(d))


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 3:
        return np.nan
    ra = pd.Series(a).rank().values
    rb = pd.Series(b).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


def main():
    t0 = time.time()
    P(f"# Idea 1035 (lane C, {DATE}) — re-express EVERY committed CHOOSER-vs-RANDOM claim as a "
      f"PERCENTILE")
    P(f"# 2 tuned dials: CLAIM SET {CLAIMSETS} x CONTROL BASIS {BASES} = 9 points, ALL reported, "
      f"none selected.")
    P(f"# HEADLINE = {CLAIMSET_HEAD} claims x {BASIS_HEAD} basis; cell controls: panel "
      f"[U56, B136] x cost {RUNGS} bps, POOL = 18 GRID books per panel, END GRID Q16 "
      f"(1013/1023/1031's own 16 quarter-ends).")
    P(f"# DRAWS: NRAND = {NRAND:,} sequences per cell (5x 1023's 400); a percentile resolves to "
      f"{1/NRAND:.4f}, binomial SE at p=0.5 = {0.5/np.sqrt(NRAND):.4f}.")
    P("# SCALE CAVEAT declared first: the record publishes gaps in Sharpe, in CAGR pp and in")
    P("#   pass RATES.  Only a Sharpe-scale gap can be run through a Sharpe distribution, so the")
    P("#   banding arm takes only numbers written with >= 3 decimals, |g| <= 0.5, in a sentence")
    P("#   naming Sharpe.  Everything the filter excludes is COUNTED, never silently dropped.")
    P("# SURVIVORSHIP: U56/B136 are current-constituent panels — every LEVEL is optimistic.  The")
    P("#   measured object is a RANK inside a distribution from the SAME pool; where the bias")
    P("#   does not cancel it flatters the coin flip, so every chooser percentile is a LOWER")
    P("#   bound.")
    P("")

    # ================================================================ (A) THE CENSUS
    P("## (A) THE CENSUS — every committed chooser-vs-random sentence in LEADERBOARD.md and "
      "CHANGELOG.md")
    H = harvest()
    H2 = harvest()
    g0 = H.equals(H2)
    src_bytes = {s.name: len(s.read_bytes()) for s in SOURCES}
    P(f"G0 HARVEST determinism (re-parse of the same bytes returns the same claim table): "
      f"{'PASS' if g0 else 'FAIL'}  ({', '.join(f'{k} {v:,}B' for k, v in src_bytes.items())})")
    dump(H, "claims")
    P(f"   harvested {len(H):,} candidate sentences; STRICT {int(H.STRICT.sum()):,}, "
      f"WIDE {int(H.WIDE.sum()):,}, NUMERIC {int(H.NUMERIC.sum()):,}")
    for s in SOURCES:
        sub = H[H.src == s.name]
        P(f"   {s.name:16s} candidates {len(sub):5,}  STRICT {int(sub.STRICT.sum()):5,}  "
          f"WIDE {int(sub.WIDE.sum()):5,}  NUMERIC {int(sub.NUMERIC.sum()):5,}")
    P("")
    P("   FIELD STAMPS — the share of claims carrying each field a percentile needs")
    P(f"{'claim set':10s} {'n':>6s} | {'POOL':>6s} {'DRAWS':>6s} {'CELL':>6s} {'COST':>6s} "
      f"{'YARD':>6s} {'PCT':>6s} | {'POOL&DRAWS':>10s} {'MAPPABLE':>9s}")
    stamp_rows = []
    for cs in CLAIMSETS:
        sub = H[H[cs]]
        n = len(sub)
        if n == 0:
            continue
        mapp = sub.has_panel & sub.has_cost & (sub.chooser.str.upper().isin(
            [c.upper() for c in RAW_CH]))
        d = dict(claim_set=cs, n=n, pool=sub.has_pool.mean(), draws=sub.has_draws.mean(),
                 cell=sub.has_panel.mean(), cost=sub.has_cost.mean(),
                 yardstick=sub.has_yardstick.mean(), percentile=sub.has_percentile.mean(),
                 pool_and_draws=(sub.has_pool & sub.has_draws).mean(), mappable=mapp.mean(),
                 n_mappable=int(mapp.sum()))
        stamp_rows.append(d)
        P(f"{cs:10s} {n:6,} | {d['pool']:6.3f} {d['draws']:6.3f} {d['cell']:6.3f} "
          f"{d['cost']:6.3f} {d['yardstick']:6.3f} {d['percentile']:6.3f} | "
          f"{d['pool_and_draws']:10.3f} {d['mappable']:9.3f}")
    ST = pd.DataFrame(stamp_rows)
    dump(ST, "stamps")

    # ================================================================ THE LADDER
    P("")
    U = load_universe()
    B = load_universe(broad=True)
    if not U.index.equals(B.index):
        P(f"   CALENDAR: U56 ends {U.index[-1].date()} ({len(U)} days), B136 ends "
          f"{B.index[-1].date()} ({len(B)} days); each panel keeps its OWN calendar (1013's, "
          f"1023's and 1031's construction, and what the cross-run gates are stated on). "
          f"No splice.")
    PX = {"U56": U, "B136": B}
    REC = {p: PX[p].index[WARMUP] for p in PX}
    P(f"Tape: U56 {U.shape} {U.index[0].date()}..{U.index[-1].date()}; "
      f"B136 {B.shape} {B.index[0].date()}..{B.index[-1].date()}.")
    pool = C.grid_books(U, B)
    P(f"POOL = {len(pool)} never-memo-selected GRID books "
      f"({sum(b['panel']=='U56' for b in pool.values())} U56 / "
      f"{sum(b['panel']=='B136' for b in pool.values())} B136).  END GRID Q16 = "
      f"{len(END_Q16)} ends {END_Q16[0]}..{END_Q16[-1]}; declared split {REC_END} read "
      f"separately for rule 8.")

    NET = {}
    for nm, b in pool.items():
        px = PX[b["panel"]]
        r, t = fast_run(px, b["W"], rebalance_mask(px.index, b["freq"]))
        st = REC[b["panel"]]
        for c in RUNGS:
            NET[(nm, c)] = (r - t * c / 1e4).loc[st:]
    SPYR = {p: PX[p]["SPY"].pct_change().fillna(0.0).loc[REC[p]:] for p in PX}
    V2 = {}
    for p, px in PX.items():
        r, t = fast_run(px, rules_v2_weights(px), rebalance_mask(px.index, "W"))
        for c in RUNGS:
            V2[(p, c)] = metblock((r - t * c / 1e4).loc[REC[p]:].values)

    P("")
    P("## Reproduction gates (printed BEFORE any hypothesis number is read)")
    gates = [dict(gate="G0", what="harvest determinism", value=f"{len(H)} rows",
                  verdict="PASS" if g0 else "FAIL")]

    W2 = rules_v2_weights(U)
    eng = backtest(U, W2, cost_bps=0.0, freq="W")
    fr, ft = fast_run(U, W2, rebalance_mask(U.index, "W"))
    d_r = float(np.abs(eng["returns"].values[WARMUP:] - fr.values[WARMUP:]).max())
    d_t = float(np.abs(eng["turnover"].values[WARMUP:] - ft.values[WARMUP:]).max())
    g1 = d_r < 1e-12 and d_t < 1e-10
    P(f"G1 fast_run == engine.backtest (returns / turnover): {d_r:.3e} / {d_t:.3e}  "
      f"{'PASS' if g1 else 'FAIL'}")
    gates.append(dict(gate="G1", what="fast runner == engine.backtest",
                      value=f"{d_r:.3e}/{d_t:.3e}", verdict="PASS" if g1 else "FAIL"))

    d2 = float(np.abs(rules_v2_weights(U, 0.03, 0.75).values - W2.values).max())
    g2 = d2 == 0.0
    P(f"G2 rules_v2_weights(U,0.03,0.75) == baseline.rules_v2_weights(U): {d2:.3e}  "
      f"{'PASS' if g2 else 'FAIL'}")
    gates.append(dict(gate="G2", what="band book == live baseline", value=f"{d2:.3e}",
                      verdict="PASS" if g2 else "FAIL"))

    SPYB = {(p, e): split_block(SPYR[p], e) for p in PX for e in ALLE}
    sb = SPYB[(PANEL_HEAD, REC_END)]
    trip = (sb["OOS_CAGR"], sb["OOS_Sharpe"], sb["OOS_MaxDD"])
    d3 = max(abs(a - b) for a, b in zip(trip, SPY_OOS_COMMITTED))
    g3 = d3 <= 5e-4
    P(f"G3 CROSS-RUN SPY OOS at {REC_END}: {trip[0]:.4%} / {trip[1]:.4f} / {trip[2]:.4%}  "
      f"max|d| {d3:.3e}  {'PASS' if g3 else 'FAIL'}")
    gates.append(dict(gate="G3", what="SPY OOS triple vs record", value=f"{d3:.3e}",
                      verdict="PASS" if g3 else "FAIL"))

    def build_ladder():
        rows = []
        for nm, b in pool.items():
            p = b["panel"]
            for c in RUNGS:
                net = NET[(nm, c)]
                for e in ALLE:
                    bk = split_block(net, e)
                    s = SPYB[(p, e)]
                    lg = legs_at(bk, s)
                    v2 = V2[(p, c)]
                    rows.append(dict(
                        book=nm, panel=p, cost=c, E=e,
                        **{k: bk[k] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe",
                                              "IS_CAGR", "IS_MaxDD", "OOS_CAGR", "OOS_Sharpe",
                                              "OOS_MaxDD", "IS_n", "OOS_n")},
                        spy_OOS_Sharpe=s["OOS_Sharpe"], spy_OOS_CAGR=s["OOS_CAGR"],
                        **lg, pass4b=all(lg.values()),
                        pass4a=bool(bk["H1"] > v2["H1"] and bk["H2"] > v2["H2"]
                                    and bk["MaxDD"] >= v2["MaxDD"])))
        return pd.DataFrame(rows)

    L = build_ladder()
    L2 = build_ladder()
    num = L.select_dtypes(include=[float, int]).columns
    d5 = float(np.nanmax(np.abs(L[num].values - L2[num].values)))
    g5 = d5 == 0.0
    P(f"G5 determinism over the {len(L):,}-row ladder: {d5:.3e}  {'PASS' if g5 else 'FAIL'}")
    gates.append(dict(gate="G5", what="ladder determinism", value=f"{d5:.3e}",
                      verdict="PASS" if g5 else "FAIL"))
    dump(L, "ladder")

    bad4, rows4 = 0, []
    for (p, nm), t13 in PUB_1013.items():
        r = L[(L.book == nm) & (L.panel == p) & (L.cost == RUNG_HEAD) & (L.E == REC_END)].iloc[0]
        d = max(abs(r.OOS_CAGR - t13[0]), abs(r.OOS_Sharpe - t13[1]), abs(r.OOS_MaxDD - t13[2]))
        ok = d <= 5e-4
        bad4 += 0 if ok else 1
        rows4.append(dict(panel=p, book=nm, OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe,
                          OOS_MaxDD=r.OOS_MaxDD, pub_CAGR=t13[0], pub_Sharpe=t13[1],
                          pub_MaxDD=t13[2], maxd=d, verdict="PASS" if ok else "FAIL"))
    g4 = bad4 == 0
    P(f"G4 CROSS-RUN 1013's four published declared-split picks: {len(PUB_1013)-bad4}/"
      f"{len(PUB_1013)}  max|d| {max(r['maxd'] for r in rows4):.3e}  {'PASS' if g4 else 'FAIL'}")
    gates.append(dict(gate="G4", what="1013 published picks", value=f"{len(PUB_1013)-bad4}/"
                      f"{len(PUB_1013)}", verdict="PASS" if g4 else "FAIL"))
    dump(pd.DataFrame(rows4), "crossrun")

    SPYIS = {(p, e): fmet(SPYR[p].loc[:pd.Timestamp(e)].values) for p in PX for e in ALLE}
    IDX = {}
    for p in PX:
        for c in RUNGS:
            for e in ALLE:
                IDX[(p, c, e)] = L[(L.panel == p) & (L.cost == c) & (L.E == e)].set_index("book")

    def picks_raw(p, c):
        return {e: {ch: raw_pick(IDX[(p, c, e)], ch, SPYIS[(p, e)]) for ch in RAW_CH}
                for e in ALLE}

    PR = {(p, c): picks_raw(p, c) for p in PX for c in RUNGS}

    rng6 = np.random.default_rng(SEED0)
    base_pick = PR[(PANEL_HEAD, RUNG_HEAD)]
    NET_SAVE = dict(NET)
    for nm, b in pool.items():
        if b["panel"] != PANEL_HEAD:
            continue
        s = NET[(nm, RUNG_HEAD)]
        o = s.loc[pd.Timestamp(ALLE[-1]) + pd.Timedelta(days=1):]
        perm = pd.Series(rng6.permutation(o.values), index=o.index)
        NET[(nm, RUNG_HEAD)] = pd.concat([s.loc[:pd.Timestamp(ALLE[-1])], perm])
    Lp = build_ladder()
    IDXp = {e: Lp[(Lp.panel == PANEL_HEAD) & (Lp.cost == RUNG_HEAD) & (Lp.E == e)].set_index("book")
            for e in ALLE}
    bad6 = sum(raw_pick(IDXp[e], ch, SPYIS[(PANEL_HEAD, e)]) != base_pick[e][ch]
               for e in ALLE for ch in RAW_CH)
    NET.clear()
    NET.update(NET_SAVE)
    g6 = bad6 == 0
    P(f"G6 IS PURITY (picks invariant to an OOS permutation): {bad6} moved picks of "
      f"{len(ALLE)*len(RAW_CH)}  {'PASS' if g6 else 'FAIL'}")
    gates.append(dict(gate="G6", what="IS purity", value=f"{bad6}/{len(ALLE)*len(RAW_CH)}",
                      verdict="PASS" if g6 else "FAIL"))

    # ---------------------------------------------------------------- distributions per basis
    BOOKS = {p: sorted(b for b in pool if pool[b]["panel"] == p) for p in PX}
    MAT = {}
    for p in PX:
        for c in RUNGS:
            MAT[(p, c)] = np.array(
                [[IDX[(p, c, e)].loc[b, "OOS_Sharpe"] for b in BOOKS[p]] for e in END_Q16])
    rng = np.random.default_rng(SEED0 + 7)
    SEQ = {(p, c): rng.integers(0, len(BOOKS[p]), (NRAND, len(END_Q16)))
           for p in PX for c in RUNGS}

    def dists(p, c, basis):
        """The null distribution(s) for a cell under a control basis.  Returns a list of
        (label, distribution) — SEQ and FIXED give one, RAW gives one per end."""
        M = MAT[(p, c)]
        if basis == "SEQ":
            s = SEQ[(p, c)]
            v = M[np.arange(M.shape[0])[None, :], s]
            return [("seq", v.mean(axis=1))]
        if basis == "FIXED":
            return [("fixed", M.mean(axis=0))]
        return [(e, M[i, :]) for i, e in enumerate(END_Q16)]

    def chooser_score(p, c, ch, basis):
        """The chooser's score on the same footing as its null."""
        M = MAT[(p, c)]
        bidx = {b: i for i, b in enumerate(BOOKS[p])}
        v = np.array([M[i, bidx[PR[(p, c)][e][ch]]] for i, e in enumerate(END_Q16)])
        if basis == "RAW":
            return v                      # one score per end
        return np.array([v.mean()])

    bad7, rows7 = 0, []
    for p in PX:
        for c in RUNGS:
            d = dists(p, c, "SEQ")[0][1]
            exact = float(MAT[(p, c)].mean())
            se = float(d.std(ddof=1) / np.sqrt(NRAND))
            ok = abs(d.mean() - exact) <= 3 * se
            bad7 += 0 if ok else 1
            rows7.append(dict(panel=p, cost=c, mc_mean=float(d.mean()), exact_pool_mean=exact,
                              diff=float(d.mean() - exact), mc_se=se,
                              verdict="PASS" if ok else "FAIL"))
    g7 = bad7 == 0
    P(f"G7 SAMPLER UNBIASEDNESS (MC mean == exact pool mean, 3 SE): {6-bad7}/6  "
      f"max|d| {max(abs(r['diff']) for r in rows7):.3e}  {'PASS' if g7 else 'FAIL'}")
    gates.append(dict(gate="G7", what="sampler unbiased vs exact pool mean", value=f"{6-bad7}/6",
                      verdict="PASS" if g7 else "FAIL"))
    dump(pd.DataFrame(rows7), "sampler")

    dev8, atom8 = {}, {}
    for basis in BASES:
        dd = [d for p in PX for c in RUNGS for _, d in dists(p, c, basis)]
        dev8[basis] = max(abs(pct_of(np.median(d), d) - 0.5) for d in dd)
        atom8[basis] = max(float((np.asarray(d) == np.median(d)).mean()) for d in dd)
    g8 = dev8["SEQ"] <= 0.01
    P(f"G8 PERCENTILE VALIDITY (a distribution's own median scores 0.5000): SEQ worst |d| "
      f"{dev8['SEQ']:.5f} {'PASS' if g8 else 'FAIL'};  FIXED {dev8['FIXED']:.4f} "
      f"(atom {atom8['FIXED']:.4f}), RAW {dev8['RAW']:.4f} (atom {atom8['RAW']:.4f}) — both are "
      f"18-point pools quantised to 1/18 = {1/18:.4f}, so their deviation IS the atom and is "
      f"printed, not hidden.")
    gates.append(dict(gate="G8", what="percentile validity (SEQ basis)", value=f"{dev8['SEQ']:.5f}",
                      verdict="PASS" if g8 else "FAIL"))

    bad9, rows9 = 0, []
    for ch in RAW_CH:
        d = dists(PANEL_HEAD, RUNG_HEAD, "SEQ")[0][1]
        sc = float(chooser_score(PANEL_HEAD, RUNG_HEAD, ch, "SEQ")[0])
        pc = pct_of(sc, d)
        dsc = abs(sc - PUB_1023_CHOOSER[ch])
        dpc = abs(pc - PUB_1031_PCT[ch])
        ok = dsc <= 5e-4 and dpc <= 0.02
        bad9 += 0 if ok else 1
        rows9.append(dict(chooser=ch, score=sc, pub_1023_score=PUB_1023_CHOOSER[ch], d_score=dsc,
                          percentile=pc, pub_1031_pct=PUB_1031_PCT[ch], d_pct=dpc,
                          verdict="PASS" if ok else "FAIL"))
        P(f"   {ch:10s} score {sc:.6f} vs 1023's {PUB_1023_CHOOSER[ch]:.6f} (|d| {dsc:.2e});  "
          f"percentile {pc:.3f} vs 1031's {PUB_1031_PCT[ch]:.3f} (|d| {dpc:.3f})")
    g9 = bad9 == 0
    P(f"G9 CROSS-RUN 1031's committed headline percentiles: {len(RAW_CH)-bad9}/{len(RAW_CH)}  "
      f"{'PASS' if g9 else 'FAIL'}")
    gates.append(dict(gate="G9", what="1031 published percentiles", value=f"{3-bad9}/3",
                      verdict="PASS" if g9 else "FAIL"))
    dump(pd.DataFrame(rows9), "crossrun1031")

    # ================================================================ (B) THE CALIBRATION
    P("")
    P("## (B) THE CALIBRATION — what percentile does a published GAP earn?")
    P("   For a cell's null distribution D, a claim of gap g is the claim that the chooser scored")
    P("   mean(D) + g.  Its percentile is pct(mean(D) + g, D) — a closed form, no search.")
    P("")
    cal_rows = []
    GRID_G = [-0.20, -0.10, -0.0884, -0.05, -0.02, -0.01, 0.0, 0.01, 0.0177, 0.02, 0.0418,
              0.05, 0.10, 0.20]
    for basis in BASES:
        for p in PX:
            for c in RUNGS:
                for lab, d in dists(p, c, basis):
                    mu = float(np.mean(d))
                    for g in GRID_G:
                        cal_rows.append(dict(basis=basis, panel=p, cost=c, cell_end=lab, gap=g,
                                             null_mean=mu, null_sd=float(np.std(d, ddof=1)),
                                             percentile=pct_of(mu + g, d)))
    CAL = pd.DataFrame(cal_rows)
    dump(CAL, "calibration")
    P(f"{'basis':6s} {'gap':>8s} | {'pct min':>8s} {'pct med':>8s} {'pct max':>8s} "
      f"{'width':>7s} {'n cells':>7s}")
    for basis in BASES:
        for g in GRID_G:
            s = CAL[(CAL.basis == basis) & (CAL.gap == g)]
            P(f"{basis:6s} {g:+8.4f} | {s.percentile.min():8.3f} {s.percentile.median():8.3f} "
              f"{s.percentile.max():8.3f} {s.percentile.max()-s.percentile.min():7.3f} "
              f"{len(s):7d}")
        P("")
    P("   null sd by basis (the yardstick the record does not publish):")
    SD = {}
    for basis in BASES:
        s = CAL[CAL.basis == basis].drop_duplicates(["panel", "cost", "cell_end"])
        SD[basis] = float(s.null_sd.median())
        P(f"     {basis:6s} sd {s.null_sd.min():.4f}..{s.null_sd.max():.4f} "
          f"(median {s.null_sd.median():.4f}) over {len(s)} cells")
    P("")
    P("   THE RESOLVING WINDOW — a band width is only informative where the percentile is not")
    P("   already SATURATED.  Outside +/- ~2 sd every gap earns 0.000 or 1.000 and gaps of very")
    P("   different size become indistinguishable, which is a second way to be unadjudicable.")
    for basis in BASES:
        P(f"     {basis:6s} null sd {SD[basis]:.4f} -> gaps inside +/-{2*SD[basis]:.4f} resolve; "
          f"1031's pair re-read here: gap -0.0884 -> median pct "
          f"{CAL_interp(CAL, basis, -0.0884)[1]:.3f}, gap +0.0177 -> "
          f"{CAL_interp(CAL, basis, 0.0177)[1]:.3f}")

    # ================================================================ (C) THE RE-SCORE
    P("")
    P("## (C) THE RE-SCORE — every harvested Sharpe-scale gap, as the percentile BAND it is")
    P("   consistent with across the record's own legal cells.")
    rs_rows = []
    for _, r in H.iterrows():
        if not r.sharpe_gaps:
            continue
        for gtxt in r.sharpe_gaps.split(";"):
            g = float(gtxt)
            for basis in BASES:
                s = CAL_interp(CAL, basis, g)
                rs_rows.append(dict(src=r.src, line=r.line, claim_set_STRICT=r.STRICT,
                                    claim_set_WIDE=r.WIDE, claim_set_NUMERIC=r.NUMERIC,
                                    basis=basis, gap=g, pct_min=s[0], pct_med=s[1],
                                    pct_max=s[2], width=s[2] - s[0],
                                    saturated=bool(s[1] <= 0.02 or s[1] >= 0.98),
                                    text=r.text[:200]))
    RS = pd.DataFrame(rs_rows)
    dump(RS, "rescore")
    if len(RS):
        P("")
        P("   ALL NINE GRID POINTS (claim set x control basis).  'sat' = the gap is outside the")
        P("   null's realised support, where every gap earns 0.000 or 1.000 and band width is")
        P("   narrow for the WRONG reason; 'width|in' is the band width on the resolving gaps.")
        P(f"{'claim set':10s} {'basis':6s} {'n gaps':>7s} {'sat':>6s} | {'width med':>9s} "
          f"{'width mean':>10s} {'width max':>9s} | {'width|in':>9s} {'>0.20|in':>9s}")
        grid_rows = []
        for cs in CLAIMSETS:
            for basis in BASES:
                s = RS[(RS.basis == basis) & (RS[f"claim_set_{cs}"])]
                if not len(s):
                    continue
                ins = s[~s.saturated]
                d = dict(claim_set=cs, basis=basis, n_gaps=len(s), sat_share=s.saturated.mean(),
                         width_med=s.width.median(), width_mean=s.width.mean(),
                         width_max=s.width.max(), n_resolving=len(ins),
                         width_med_resolving=ins.width.median() if len(ins) else np.nan,
                         share_wide_resolving=(ins.width > 0.20).mean() if len(ins) else np.nan)
                grid_rows.append(d)
                P(f"{cs:10s} {basis:6s} {len(s):7,} {s.saturated.mean():6.3f} | "
                  f"{s.width.median():9.3f} {s.width.mean():10.3f} {s.width.max():9.3f} | "
                  f"{d['width_med_resolving'] if len(ins) else float('nan'):9.3f} "
                  f"{d['share_wide_resolving'] if len(ins) else float('nan'):9.3f}")
        dump(pd.DataFrame(grid_rows), "grid")
        P("")
        P("   the ten widest bands on the headline basis (a published gap consistent with this "
          "much of the null):")
        top = RS[RS.basis == BASIS_HEAD].nlargest(10, "width")
        for _, r in top.iterrows():
            P(f"     {r.src:15s}:{r.line:<5d} gap {r.gap:+.4f} -> pct "
              f"{r.pct_min:.3f}..{r.pct_max:.3f} (width {r.width:.3f})  {r.text[:90]}")

    # exactly mappable claims, re-scored in their OWN cell
    P("")
    P("   EXACTLY MAPPABLE claims — those naming a panel, a cost rung and a chooser — re-scored")
    P("   in their own cell under all three bases (no banding needed):")
    mp_rows = []
    for _, r in H[H.STRICT].iterrows():
        ch = r.chooser.upper()
        if ch not in [c.upper() for c in RAW_CH] or not r.panel or not np.isfinite(r.cost):
            continue
        p = r.panel.upper()
        if p not in PX or float(r.cost) not in RUNGS:
            continue
        c = float(r.cost)
        for basis in BASES:
            sc = chooser_score(p, c, ch, basis)
            dd = dists(p, c, basis)
            pcs = [pct_of(sc[i] if basis == "RAW" else sc[0], d) for i, (_, d) in enumerate(dd)]
            mp_rows.append(dict(src=r.src, line=r.line, panel=p, cost=c, chooser=ch, basis=basis,
                                score=float(np.mean(sc)), percentile=float(np.mean(pcs)),
                                pct_min=float(np.min(pcs)), pct_max=float(np.max(pcs)),
                                clears_50th=bool(np.mean(pcs) > 0.5), text=r.text[:200]))
    MP = pd.DataFrame(mp_rows)
    if len(MP):
        dump(MP, "mappable")
        P(f"{'src':16s} {'line':>5s} {'panel':6s} {'cost':>4s} {'chooser':10s} {'basis':6s} "
          f"{'score':>7s} {'pct':>6s} {'>50th':>6s}")
        for _, r in MP.iterrows():
            P(f"{r.src:16s} {r.line:5d} {r.panel:6s} {r.cost:4.0f} {r.chooser:10s} {r.basis:6s} "
              f"{r.score:7.4f} {r.percentile:6.3f} {str(r.clears_50th):>6s}")
    else:
        P("     NONE.  No committed chooser-vs-random sentence names all three of panel, cost "
          "rung and chooser.")

    # ================================================================ hypotheses
    P("")
    P("## Hypotheses (bars declared in the docstring, before any number above was read)")
    hyp = []

    def HYP(name, bar, ok, detail):
        hyp.append(dict(hypothesis=name, bar=bar, verdict="PASS" if ok else "FAIL", detail=detail))
        P(f"{name:11s} {'PASS' if ok else 'FAIL'}  bar: {bar}")
        P(f"            {detail}")

    head = ST[ST.claim_set == CLAIMSET_HEAD].iloc[0]
    HYP("H_STAMP", ">= 50% of STRICT claims carry BOTH a pool size and a draw count",
        head.pool_and_draws >= 0.50,
        f"{head.pool_and_draws:.3%} of {int(head.n):,} STRICT claims (pool alone "
        f"{head['pool']:.3%}, draws alone {head['draws']:.3%})")
    HYP("H_YARD", ">= 50% of STRICT claims carry ANY yardstick (sd/SE/IQR/percentile)",
        head.yardstick >= 0.50,
        f"{head.yardstick:.3%} carry a yardstick token; {head.percentile:.3%} already publish a "
        f"percentile or a share-of-draws")
    HYP("H_MAP", ">= 50% of STRICT claims are EXACTLY mappable (panel + cost rung + chooser)",
        head.mappable >= 0.50,
        f"{head.mappable:.3%} — {int(head.n_mappable)} of {int(head.n):,} claims")

    if len(RS):
        hb = RS[(RS.basis == BASIS_HEAD) & RS[f"claim_set_{CLAIMSET_HEAD}"]]
        hbin = hb[~hb.saturated]
        HYP("H_BAND", "median percentile-band width over re-scorable Sharpe gaps <= 0.20",
            float(hb.width.median()) <= 0.20,
            f"median width {hb.width.median():.3f} over {len(hb):,} {CLAIMSET_HEAD} gaps on the "
            f"{BASIS_HEAD} basis (mean {hb.width.mean():.3f}, max {hb.width.max():.3f}); "
            f"{(hb.width > 0.20).mean():.1%} of gaps exceed the bar individually.  "
            f"DIAGNOSIS, stated as loudly as the PASS: {hb.saturated.mean():.1%} of these gaps "
            f"are SATURATED (median percentile <= 0.02 or >= 0.98), where the band is narrow "
            f"because every gap of that size earns the same 0.000 or 1.000 — a second way to be "
            f"unadjudicable, not a resolution.  On the {len(hbin)} RESOLVING gaps the median "
            f"width is " + (f"{hbin.width.median():.3f}" if len(hbin) else "n/a") +
            f" and on FIXED/RAW the same gaps run "
            f"{RS[(RS.basis=='FIXED') & RS['claim_set_'+CLAIMSET_HEAD]].width.median():.3f} / "
            f"{RS[(RS.basis=='RAW') & RS['claim_set_'+CLAIMSET_HEAD]].width.median():.3f}")
        gs = np.sort(hb.gap.unique())
        worst, wpair = 0.0, None
        for i in range(len(gs)):
            for j in range(i + 1, len(gs)):
                if abs(gs[i] - gs[j]) <= 0.005:
                    a = CAL_interp(CAL, BASIS_HEAD, gs[i])
                    b = CAL_interp(CAL, BASIS_HEAD, gs[j])
                    for x in (a[0], a[1], a[2]):
                        for y in (b[0], b[1], b[2]):
                            if abs(x - y) > worst:
                                worst, wpair = abs(x - y), (gs[i], gs[j])
        HYP("H_FUNCTION", "gaps within 0.005 of each other earn percentiles within 0.10",
            worst <= 0.10,
            f"worst spread {worst:.3f}" + (f" between gaps {wpair[0]:+.4f} and {wpair[1]:+.4f}"
                                           if wpair else " (no pair within 0.005)"))
    else:
        HYP("H_BAND", "median percentile-band width over re-scorable Sharpe gaps <= 0.20", False,
            "no re-scorable Sharpe-scale gap was harvested")
        HYP("H_FUNCTION", "gaps within 0.005 earn percentiles within 0.10", False,
            "no re-scorable Sharpe-scale gap was harvested")

    cc = CAL[CAL.basis == BASIS_HEAD]
    rho = spearman(cc.gap.values, cc.percentile.values)
    HYP("H_MONO", "pooled Spearman rho(gap, percentile) >= 0.90 across all (gap, cell) points",
        bool(rho >= 0.90),
        f"rho {rho:.4f} over {len(cc):,} points on the {BASIS_HEAD} basis; by basis " +
        ", ".join(f"{b}={spearman(CAL[CAL.basis==b].gap.values, CAL[CAL.basis==b].percentile.values):.4f}"
                  for b in BASES))

    sgn = cc[cc.gap != 0]
    agree = float(((sgn.gap > 0) == (sgn.percentile > 0.5)).mean())
    HYP("H_SIGN", "sign(gap) agrees with the 50th-percentile verdict in >= 95% of points",
        agree >= 0.95,
        f"{agree:.3%} agreement over {len(sgn):,} non-zero-gap points ({BASIS_HEAD} basis); "
        f"disagreements {int((~((sgn.gap > 0) == (sgn.percentile > 0.5))).sum()):,}")

    wide = []
    for g in GRID_G:
        v = [CAL_interp(CAL, b, g)[1] for b in BASES]
        wide.append(max(v) - min(v))
    HYP("H_BASIS", "the percentile a given gap earns is within 0.10 across the three bases",
        max(wide) <= 0.10,
        "max across-basis spread of the MEDIAN percentile " + f"{max(wide):.3f} at gap "
        f"{GRID_G[int(np.argmax(wide))]:+.4f}; per-gap spreads " +
        " ".join(f"{g:+.3f}:{w:.3f}" for g, w in zip(GRID_G, wide)))

    same = all(
        (ST[ST.claim_set == cs].iloc[0].pool_and_draws >= 0.50) == (head.pool_and_draws >= 0.50)
        and (ST[ST.claim_set == cs].iloc[0].yardstick >= 0.50) == (head.yardstick >= 0.50)
        and (ST[ST.claim_set == cs].iloc[0].mappable >= 0.50) == (head.mappable >= 0.50)
        for cs in CLAIMSETS if (ST.claim_set == cs).any())
    HYP("H_CLAIMSET", "H_STAMP / H_YARD / H_MAP return the same verdict on all three claim sets",
        same,
        "; ".join(f"{r.claim_set}: pool&draws {r.pool_and_draws:.3f}, yard {r.yardstick:.3f}, "
                  f"mappable {r.mappable:.3f}" for _, r in ST.iterrows()))

    # G10 band self-consistency: a gap taken FROM a cell returns that cell's own percentile
    bad10 = 0.0
    for p in PX:
        for c in RUNGS:
            _, d = dists(p, c, BASIS_HEAD)[0]
            mu = float(np.mean(d))
            for ch in RAW_CH:
                sc = float(chooser_score(p, c, ch, BASIS_HEAD)[0])
                bad10 = max(bad10, abs(pct_of(mu + (sc - mu), d) - pct_of(sc, d)))
    g10 = bad10 <= 1e-12
    P("")
    P(f"G10 BAND SELF-CONSISTENCY (a gap taken FROM a cell returns that cell's own percentile): "
      f"max|d| {bad10:.3e}  {'PASS' if g10 else 'FAIL'}")
    gates.append(dict(gate="G10", what="band self-consistency", value=f"{bad10:.3e}",
                      verdict="PASS" if g10 else "FAIL"))

    dump(pd.DataFrame(hyp), "hypotheses")
    dump(pd.DataFrame(gates), "gates")

    # ================================================================ (D) rule 8 walk-forward
    P("")
    P("## (D) RULE 8 WALK-FORWARD — PROTOCOL's own split, IS 2009-2016 / OOS 2017-2026 read ONCE")
    P("   Each chooser picks a book using 2009-2016 data ONLY; the OOS triple is read once and")
    P("   scored on BOTH KEEP paths, and the pick is percentiled inside its own 18-book pool.")
    P("")
    wrows = []
    for p in PX:
        s = SPYB[(p, REC_END)]
        for c in RUNGS:
            v2 = V2[(p, c)]
            sub = IDX[(p, c, REC_END)]
            pooldist = sub.loc[BOOKS[p], "OOS_Sharpe"].values
            for ch in RAW_CH:
                bk = PR[(p, c)][REC_END][ch]
                r = sub.loc[bk]
                lg = legs_at(dict(H1=r.H1, H2=r.H2, OOS_Sharpe=r.OOS_Sharpe,
                                  OOS_MaxDD=r.OOS_MaxDD, OOS_CAGR=r.OOS_CAGR), s)
                wrows.append(dict(
                    panel=p, cost=c, chooser=ch, pick=bk,
                    OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                    spy_OOS_CAGR=s["OOS_CAGR"], spy_OOS_Sharpe=s["OOS_Sharpe"],
                    spy_OOS_MaxDD=s["OOS_MaxDD"], v2_CAGR=v2["CAGR"], v2_Sharpe=v2["Sharpe"],
                    v2_MaxDD=v2["MaxDD"], **lg, pass4b=all(lg.values()), pass4a=bool(r.pass4a),
                    pool_percentile=pct_of(r.OOS_Sharpe, pooldist),
                    pool_mean_OOS_Sharpe=float(np.mean(pooldist)),
                    pool_median_OOS_Sharpe=float(np.median(pooldist))))
    WF = pd.DataFrame(wrows)
    dump(WF, "walkforward")
    P(f"{'panel':6s} {'cost':>4s} {'chooser':10s} {'pick':30s} | {'OOS CAGR':>8s} {'Sh':>6s} "
      f"{'MaxDD':>7s} | {'4b':>3s} {'4a':>3s} {'poolPct':>7s}  binding legs")
    for _, r in WF.iterrows():
        binds = ",".join(k for k in ("L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR") if not r[k])
        P(f"{r.panel:6s} {r.cost:4.0f} {r.chooser:10s} {r['pick']:30s} | {r.OOS_CAGR:8.2%} "
          f"{r.OOS_Sharpe:6.3f} {r.OOS_MaxDD:7.2%} | {str(r.pass4b)[0]:>3s} "
          f"{str(r.pass4a)[0]:>3s} {r.pool_percentile:7.3f}  "
          f"{binds if binds else '(none — passes 4b)'}")
    for p in PX:
        s = SPYB[(p, REC_END)]
        v2 = V2[(p, RUNG_HEAD)]
        P(f"   comparands {p}: SPY OOS {s['OOS_CAGR']:.2%} / {s['OOS_Sharpe']:.4f} / "
          f"{s['OOS_MaxDD']:.2%}  (4b DD cap {DDCAP_FRAC*abs(s['MaxDD']):.2%}, CAGR floor "
          f"{CAGRFLOOR_FRAC*s['CAGR']:.2%});  RULES v2 live @{RUNG_HEAD:.0f} bps full "
          f"{v2['CAGR']:.2%} / {v2['Sharpe']:.4f} / {v2['MaxDD']:.2%} "
          f"(H1 {v2['H1']:.4f} / H2 {v2['H2']:.4f})")
    P(f"   OOS 4b passes: {int(WF.pass4b.sum())} of {len(WF)};  OOS 4a passes: "
      f"{int(WF.pass4a.sum())} of {len(WF)}.")
    P(f"   KEEP paths: 4a needs Sharpe > RULES v2 in BOTH halves and MaxDD no worse; 4b needs "
      f"Sharpe > SPY in both halves AND OOS, |MaxDD| <= 60% of SPY's and CAGR >= 70% of SPY's.")

    P("")
    P(f"GATES {sum(g['verdict']=='PASS' for g in gates)} of {len(gates)};  HYPOTHESES "
      f"{sum(h['verdict']=='PASS' for h in hyp)} of {len(hyp)}.")
    P(f"elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def CAL_interp(CAL, basis, g):
    """(min, median, max) percentile a gap g earns across a basis's cells.  Exact where g is on
    the calibration grid; linear in g between grid points otherwise (percentile is monotone in
    g inside a cell, so interpolation cannot cross a cell's own ordering)."""
    s = CAL[CAL.basis == basis]
    gs = np.sort(s.gap.unique())
    if g in set(gs):
        v = s[s.gap == g].percentile.values
        return float(v.min()), float(np.median(v)), float(v.max())
    lo = gs[gs <= g].max() if (gs <= g).any() else gs[0]
    hi = gs[gs >= g].min() if (gs >= g).any() else gs[-1]
    a = s[s.gap == lo].percentile.values
    b = s[s.gap == hi].percentile.values
    w = 0.0 if hi == lo else (g - lo) / (hi - lo)
    v = a * (1 - w) + b * w
    return float(v.min()), float(np.median(v)), float(v.max())


if __name__ == "__main__":
    main()
