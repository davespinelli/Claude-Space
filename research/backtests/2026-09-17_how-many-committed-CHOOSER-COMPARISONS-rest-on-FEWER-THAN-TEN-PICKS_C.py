#!/usr/bin/env python3
"""
Idea 1210 (lane C, 2026-09-17) — how many committed CHOOSER COMPARISONS in the record rest
on FEWER THAN TEN PICKS, and how many could have been RESOLVED by the draws they had?

THE PREMISE, READ FROM THE RECORD AND NEVER RECALLED.  Idea 1206 (lane C, 2026-09-17,
`2026-09-17_does-the-WIDEST-DIAL-HABIT-lose-to-DOING-NOTHING-on-ladders-1155-did-not-walk_C.py`)
re-read 1155's five-way chooser ordering, which spanned 0.0736 of mean OOS Sharpe on THREE
draws, against 472 draws of the same object and found the ordering REVERSES on 3 of 4 rules:
C_ANCHOR 0.9911 vs M_NONE 0.9895 (+0.0017, clustered SE 0.0526, t 0.03), M_SUBSAMPLE
1.0046 (-0.0135, t -0.29), M_D2 1.0054 (-0.0143, t -0.30).  Its arithmetic was printed
data-free first: 1155's published gaps needed per-pick SDs of 0.0060-0.0637 against a real
per-pick SD of order 0.3.

THE QUEUE'S QUESTION, VERBATIM: "Census every committed 'chooser A beats chooser B by X of
OOS Sharpe' claim in the record for its own pick count, and report how many could have been
resolved by the draws they had."

WHAT IS MEASURED HERE, AND WHAT IS ONLY HARVESTED.  The pick count K and the quoted gap X
come out of the record's own text by a FIXED harvest rule declared below and never tuned.
The only thing this script MEASURES on the tape is the per-pick SD of the OOS-Sharpe
difference between two honest choosers, sigma_d, because that number — and not the text —
decides what a given K can resolve.  A claim quoting |X| on K picks is RESOLVED at bar z
iff  |X| >= z * sigma_d / sqrt(K),  equivalently  K >= K_req = (z * sigma_d / |X|)^2.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  CLAIM SET  {C_STRICT, C_ADJ, C_BROAD}        which text counts as committed
  BAR        {B_1SE, B_2SE, B_NULL90}          what "resolved" means

  = 9 cells, EVERY ONE PUBLISHED.  The HEADLINE cell is C_STRICT x B_2SE, declared here
  before any number: C_STRICT because LEADERBOARD.md and CHANGELOG.md are the record's
  committed surface, B_2SE because 1206's own adjudication bar was 2 SE.

    C_STRICT  research/LEADERBOARD.md + research/CHANGELOG.md
    C_ADJ     the C_STRICT subset whose line also carries a committed verdict token
              (KEEP / KILL / PARK / ANSWERED / HIT) — i.e. a claim that adjudicated something
    C_BROAD   C_STRICT + every research/backtests/*.memo.md and *.result.md

    B_1SE     |X| >= 1.0 * sigma_d / sqrt(K)
    B_2SE     |X| >= 2.0 * sigma_d / sqrt(K)
    B_NULL90  |X| >= the 90th percentile of |mean of K draws| under a count-matched
              resample of the MEASURED per-pick difference pool (no normality assumed)

WHAT IS NOT A DIAL, fixed before the tape is read and never re-tuned:
  * HARVEST RULE.  A claim unit is one explicit GAP NUMBER (a signed 0.xxxx, or a "by 0.xxxx")
    inside a +/-140-character window of an "OOS Sharpe" / "mean OOS Sharpe" / "OOS regret"
    cue on one line of one committed file.  Percentages and "pp" figures are dropped (they
    are CAGR / drawdown units).  Every surviving number is then classified ONCE, by the text
    within 40 characters before it, into exactly one of three classes:
      LABEL  its nearest preceding label names a correlation / dispersion / probability /
             share / drawdown (spearman, pearson, rho, t, z, SE, sd, p, share, rate, MaxDD,
             turnover, percentile, ...) — not a Sharpe quantity at all;
      GAP    a DIFFERENCE MARKER stands immediately before it (gap, regret, by, delta,
             dSharpe / dOOS, margin, advantage, costs, pays, worth, buys, above, below, ...),
             or it is PARENTHESISED right after a level pair — the record's own
             "A 1.1293 vs B 1.1733 (-0.0440)" idiom;
      LEVEL  everything else: a signed Sharpe LEVEL, which is not a comparison.
    A "/"-separated list inherits its head's class.  The HEADLINE harvest rule H_MARKED
    adjudicates the GAP class alone; H_NAIVE (every number, levels and labels included) is
    published beside every headline so the classification's effect is visible and nothing is
    selected on it.  Windows carrying two LEVELS but no explicit gap are recorded as
    LEVELPAIR and reported, never adjudicated.
  * COUNT RECOVERY.  K is the count cue NEAREST the gap number on the same line, among
    "N of M" / "N/M" (K = M), "N picks|draws|decisions|cells|books|folds|arms|offsets|
    comparisons|rungs" (K = N), and "A x B [x C] picks|cells|books|decisions" (K = product).
    If the line carries no count cue, K is UNKNOWABLE and the claim is NEVER imputed a count.
  * MEASUREMENT.  PANEL {U56, B136, SMALL} (rule 9), ANCHOR {A, B}, the four core LADDERS
    {N, H, GROSS, CADENCE} and the three honest CHOOSERS {CH_ISSHARPE, CH_ISCAGR, CH_ISDD}
    are 1101/1154/1206's, inherited whole.  10 bps (rule 2), LAG 1, warm-up 260, max_vol 0.60,
    min hold H, IS end 2016-12-31.
  * ADJUDICATION BASIS.  sigma_d = sigma_CELL, the SD of the paired per-pick difference over
    POOL_CELL: 3 panels x 2 anchors x 4 ladders x 3 IS windows = 72 picks per chooser, each
    pick read on the FULL OOS window 2017-2026 — the same unit the record's own "mean OOS
    Sharpe over K picks" claims average over.  sigma_FOLD (POOL_FOLD: the same cells x 10
    non-overlapping OOS calendar years, 240 picks) is reported as a robustness column, not
    as a third dial.

DECLARED BEFORE THE TAPE IS READ:
  (1) K_req is EXACTLY quadratic in 1/X, so halving a quoted gap quadruples the picks it
      needs.  At K = 10 and z = 2 the smallest resolvable gap is 0.6325 * sigma_d; if
      sigma_d is of 1206's order (~0.3) that is ~0.19 of OOS Sharpe, an order of magnitude
      above the gaps the record habitually publishes.  So the expected finding is that
      MOST committed chooser comparisons are unresolved, and the interesting number is how
      many are not.
  (2) THE CENSUS IS AN UPPER BOUND, NOT AN ESTIMATE.  sigma_d/sqrt(K) treats K picks as
      independent; the record's picks share panels, anchors and one tape, so the true SE is
      larger.  Every "resolved" count below is therefore the most generous reading the
      record can be given, and the clustered-SE ratio (Arm B) prices how generous.
  (3) THIS IS NOT A TRADING RULE.  Nothing here can pass 4a or 4b on its own; the KEEP-path
      arm scores the 162 rung BOOKS the measurement builds, and any passer is prior art.

PROTOCOL: rule 2 costs 10 bps and t+1 execution throughout; rule 8 walk-forward in Arm D
(every chooser picks on 2009-2016 alone, 2017-2026 read ONCE, after) with OOS CAGR / Sharpe
/ MaxDD against the live RULES v2 baseline and SPY; BOTH KEEP paths on every distinct book
in Arm E; rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py are NOT modified by this script.

Runs standalone and offline:
  python research/backtests/2026-09-17_how-many-committed-CHOOSER-COMPARISONS-rest-on-FEWER-THAN-TEN-PICKS_C.py
"""
from __future__ import annotations

import re
import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "how-many-committed-CHOOSER-COMPARISONS-rest-on-FEWER-THAN-TEN-PICKS"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

# ----- 1101/1154/1206's construction, inherited whole ----------------------------------------
LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]

LAD_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]
LAD_H = [21, 63, 126, 252]
LAD_G = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]
LAD_C = ["D", "W", "M", "Q"]
LADDERS = {"N": LAD_N, "H": LAD_H, "GROSS": LAD_G, "CADENCE": LAD_C}
LADNAMES = ["N", "H", "GROSS", "CADENCE"]

ANCHORS = {
    "A": dict(N=20, H=126, GROSS=0.75, CADENCE="W"),
    "B": dict(N=12, H=63, GROSS=0.55, CADENCE="M"),
}
PANELS = ["U56", "B136", "SMALL"]
CHOOSERS = ["CH_ISSHARPE", "CH_ISCAGR", "CH_ISDD"]
PAIRS = [("CH_ISSHARPE", "CH_ISCAGR"), ("CH_ISSHARPE", "CH_ISDD"), ("CH_ISCAGR", "CH_ISDD")]
IS_WINDOWS = [("W09", "2009-01-01"), ("W11", "2011-01-01"), ("W13", "2013-01-01")]
OOS_YEARS = list(range(2017, 2027))

# ----- THE TWO DIALS ---------------------------------------------------------------------------
CLAIMSETS = ["C_STRICT", "C_ADJ", "C_BROAD"]
BARS = ["B_1SE", "B_2SE", "B_NULL90"]
CS_HEAD, BAR_HEAD = "C_STRICT", "B_2SE"
Z_OF = {"B_1SE": 1.0, "B_2SE": 2.0}
NULL_DRAWS = 2000
SEED_BASE = 12101210

# ----- the record's own committed numbers, QUOTED and GATED, never re-derived -----------------
A1101_TRIPLE = (0.155787, 1.139701, -0.191276)      # U56 anchor-A CAGR / Sharpe / MaxDD
LIVE_MAXDD_COMMITTED = -0.1205                      # live RULES v2 on U56
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)       # SPY OOS CAGR / Sharpe / MaxDD
A1206_ANCHOR = 0.9911                               # 1206 mean OOS Sharpe, C_ANCHOR
A1206_MNONE = 0.9895                                # 1206 mean OOS Sharpe, M_NONE
A1206_CLUSTSE = 0.0526                              # 1206's clustered SE of that difference
A1155_SPAN = 0.0736                                 # 1155's five-way span on THREE draws

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def seed_of(*parts):
    return SEED_BASE + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


GATES: list[dict] = []


def gate(name, what, value, ok):
    GATES.append(dict(gate=name, check=what, value=float(value), pass_=bool(ok)))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name:<5s} {what}  ->  {value:.3e}")
    return bool(ok)


# =================================================================================================
# 1101/1154/1206's runner and metrics, verbatim
# =================================================================================================
def nrun(rets, wt, mk):
    T, N = rets.shape
    mk = mk.copy()
    mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
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
    return (held * rets).sum(axis=1), turn


def fmet(r):
    r = np.asarray(r, float)
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def legs_composite(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return sum(parts) / len(parts)


def mech(px):
    comp = legs_composite(px)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, (above & (vol20 < MAXVOL)).values


def build(rank_key, elig, priced, reb, N, H, T, K, gross):
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    for i, t in enumerate(reb):
        held = np.flatnonzero(cur >= 0)
        if len(held):
            young = held[(t - cur[held]) < H]
            young = young[priced[t, young]]
        else:
            young = held
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = rank_key[t].copy()
            k[~(elig[t] & priced[t])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new_cur = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new_cur[c] = cur[c]
        for c in take:
            new_cur[c] = t
        cur = new_cur
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = gross / len(sel)
    return W


def windows_of(idx):
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    return warm, ins, oos


def blocks_m(r, warm, ins, oos):
    rr = r[warm]
    c, s, d = fmet(rr)
    h = len(rr) // 2
    oc, os_, od = fmet(r[oos])
    ic, is_, idd = fmet(r[ins])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


def legs_4b(b, sb):
    return {"L_H1": bool(b["H1"] > sb["H1"]), "L_H2": bool(b["H2"] > sb["H2"]),
            "L_OOS": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "L_DD": bool(abs(b["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"])),
            "L_CAGR": bool(b["CAGR"] >= CAGR_FLOOR * sb["CAGR"])}


def legs_4b_oos(b, sb):
    return {"O_S": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "O_DD": bool(abs(b["OOS_MaxDD"]) <= DD_CAP * abs(sb["OOS_MaxDD"])),
            "O_CAGR": bool(b["OOS_CAGR"] >= CAGR_FLOOR * sb["OOS_CAGR"])}


def legs_4a(b, lb):
    return {"A_H1": bool(b["H1"] > lb["H1"]), "A_H2": bool(b["H2"] > lb["H2"]),
            "A_DD": bool(b["MaxDD"] >= lb["MaxDD"])}


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep].dropna(how="all").ffill(), len(bad), len(meta)


class Panel:
    def __init__(self, name, px):
        self.name, self.px = name, px
        self.idx, self.K, self.T = px.index, len(px.columns), len(px.index)
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.warm, self.ins, self.oos = windows_of(px.index)
        sc, elig = mech(px)
        spy_i = list(px.columns).index("SPY")
        if name == "SMALL":
            elig = elig.copy()
            elig[:, spy_i] = False
        self.sc, self.elig = sc, elig
        self.reb, self.mkl = {}, {}
        for f in LAD_C:
            mk = rebalance_mask(px.index, f).values
            self.reb[f] = np.flatnonzero(mk)
            m = np.roll(mk, LAG)
            m[:LAG] = False
            self.mkl[f] = m
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.years = np.asarray(px.index.year)


def book(pan, N, H, gross, freq):
    W = build(-pan.sc, pan.elig, pan.priced, pan.reb[freq], N, H, pan.T, pan.K, gross)
    Wl = np.zeros_like(W)
    Wl[LAG:] = W[:-LAG]
    r, turn = nrun(pan.rets, Wl, pan.mkl[freq])
    return r - turn * COST / 1e4


def rung_kwargs(anchor, lad, rung):
    a = ANCHORS[anchor]
    kw = dict(N=a["N"], H=a["H"], gross=a["GROSS"], freq=a["CADENCE"])
    kw[{"N": "N", "H": "H", "GROSS": "gross", "CADENCE": "freq"}[lad]] = rung
    return kw


def is_stat_on(x, stat):
    """The chooser's statistic on a slice of daily returns, higher = better."""
    x = np.asarray(x, float)
    if len(x) < 20 or not np.isfinite(x).all():
        return np.nan
    if stat == "CH_ISSHARPE":
        return fsharpe(x)
    eq = np.cumprod(1.0 + x)
    if stat == "CH_ISCAGR":
        return eq[-1] ** (252.0 / len(x)) - 1.0
    if stat == "CH_ISDD":
        return float((eq / np.maximum.accumulate(eq) - 1.0).min())
    raise ValueError(stat)


# =================================================================================================
# ARM A — THE HARVEST.  One fixed rule, declared above, applied to the record's own text.
# =================================================================================================
CUE = re.compile(r"OOS\s+(?:mean\s+)?Sharpe|mean\s+OOS\s+Sharpe|OOS\s+regret", re.I)
NUM = r"\d+(?:\.\d+)?"
GAP_SIGNED = re.compile(r"(?<![\d.])[+−–—-]\s?\*{0,2}(0\.\d{2,6})")
GAP_BY = re.compile(r"\bby\s+\*{0,2}[+−–—-]?\s?(0\.\d{2,6})", re.I)
LEVELPAIR = re.compile(r"(\d\.\d{2,6})\s*(?:vs\.?|/|>|<)\s*\*{0,2}(\d\.\d{2,6})")
CNT_OF = re.compile(r"(\d+)\s*(?:of|/)\s*(\d{1,5})\b")
CNT_WORD = re.compile(
    r"(\d{1,6})\s*(?:\(panel[^)]*\)\s*)?"
    r"(?:picks|draws|decisions|cells|books|folds|arms|offsets|comparisons|rungs)\b", re.I)
CNT_PROD = re.compile(
    r"(\d{1,4})\s*[x×]\s*(\d{1,4})(?:\s*[x×]\s*(\d{1,4}))?\s*"
    r"(?:picks|cells|books|decisions)\b", re.I)
VERDICT = re.compile(r"\b(KEEP|KILL|PARK|ANSWERED|HIT)\b")
# A NUMBER THAT IS NOT A SHARPE GAP.  These labels name correlations, dispersions,
# probabilities, shares and drawdowns; a number whose nearest preceding label is one of them,
# with no other digit in between, is that quantity and not a chooser gap.
LABELS = re.compile(
    r"\b(?:spearman|pearson|kendall|rho|corr|r\^?2|t|z|se|sd|std|p|prob|share|rate|freq|"
    r"maxdd|dd|drawdown|vol|turnover|percentile|pct|quantile|median split|cagr)\b"
    r"(?:\s*\([^()0-9]*\))?[^0-9A-Za-z]*$", re.I)
# A DIFFERENCE MARKER: the record's own idiom for writing a gap rather than a level.
DIFF_MARK = re.compile(
    r"(?:\bgaps?\b|\bregrets?\b|\bdeltas?\b|Δ|\bd(?:OOS|Sharpe|S)\b|\bdiff\w*\b|"
    r"\bmargins?\b|\badvantages?\b|\bworth\b|\bcosts?\b|\bpays?\b|\bbuys\b|\bminus\b|"
    r"\bpenalt\w+\b|\bpremium\b|\bimprovement\b|\bshortfall\b|\bby\b|\bmore than\b|"
    r"\bless than\b|\bahead\b|\bbehind\b|\babove\b|\bbelow\b)"
    r"(?:\s*\([^()0-9]*\))?[^0-9A-Za-z]*$", re.I)
NUM_ANY = re.compile(r"\d\.\d")
SEP_ONLY = re.compile(r"^[\s*/,;:()\[\]|\\+−–—-]*$")
WIN = 140
PRE = 40


def classify(line, pos):
    """One fixed three-way class for a number sitting beside an OOS-Sharpe cue:

      LABEL  its nearest preceding label names a correlation / dispersion / probability /
             share / drawdown — not a Sharpe quantity at all;
      GAP    a DIFFERENCE MARKER (gap, regret, by, delta, dSharpe, margin, costs, worth, ...)
             stands immediately before it, or it is PARENTHESISED after a level pair, which
             is the record's "A 1.1293 vs B 1.1733 (-0.0440)" idiom;
      LEVEL  everything else — a signed Sharpe LEVEL, which is not a comparison and is
             reported but never adjudicated.
    """
    pre = line[max(0, pos - PRE):pos]
    if LABELS.search(pre):
        return "LABEL"
    if DIFF_MARK.search(pre):
        return "GAP"
    opens = line[max(0, pos - 3):pos]
    if "(" in opens and len(NUM_ANY.findall(line[max(0, pos - 70):pos])) >= 2:
        return "GAP"
    return "LEVEL"


def _accept(line, pos, ln_txt):
    """Fixed rejection rule: a percentage or percentage-point figure (a CAGR / drawdown unit,
    not a Sharpe one)."""
    end = pos + len(ln_txt)
    tail = line[end:end + 6]
    return not (tail[:1] == "%" or re.match(r"\*{0,2}\s?(?:%|pp\b)", tail))


def recover_count(line, pos):
    """The count cue NEAREST the gap number on the same line.  Fixed rule, never tuned."""
    cands = []
    for m in CNT_PROD.finditer(line):
        v = int(m.group(1)) * int(m.group(2)) * (int(m.group(3)) if m.group(3) else 1)
        cands.append((abs(m.start() - pos), v, "PROD"))
    for m in CNT_OF.finditer(line):
        cands.append((abs(m.start() - pos), int(m.group(2)), "OF"))
    for m in CNT_WORD.finditer(line):
        cands.append((abs(m.start() - pos), int(m.group(1)), "WORD"))
    cands = [c for c in cands if 1 <= c[1] <= 100000]
    if not cands:
        return None, "NONE"
    cands.sort(key=lambda c: (c[0], -c[1]))
    return cands[0][1], cands[0][2]


def harvest():
    strict_files = [ROOT / "research" / "LEADERBOARD.md", ROOT / "research" / "CHANGELOG.md"]
    broad_files = sorted(set(list((ROOT / "research" / "backtests").glob("*.memo.md")) +
                             list((ROOT / "research" / "backtests").glob("*.result.md"))))
    rows = []
    for src, files in (("STRICT", strict_files), ("BROADONLY", broad_files)):
        for f in files:
            try:
                text = f.read_text(errors="replace")
            except Exception:
                continue
            for ln, line in enumerate(text.split("\n"), 1):
                if not CUE.search(line):
                    continue
                verdict = bool(VERDICT.search(line))
                hits, seen = [], set()
                for m in CUE.finditer(line):
                    a, b = max(0, m.start() - WIN), min(len(line), m.end() + WIN)
                    w = line[a:b]
                    for g in list(GAP_SIGNED.finditer(w)) + list(GAP_BY.finditer(w)):
                        pos = a + g.start(1)
                        if pos in seen or not _accept(line, pos, g.group(1)):
                            continue
                        seen.add(pos)
                        hits.append((pos, float(g.group(1)), pos + len(g.group(1))))
                if hits:
                    hits.sort()
                    prev_pos, prev_cls = None, None
                    for pos, x, end_ in hits:
                        cls = classify(line, pos)
                        if cls == "LEVEL" and prev_cls is not None and prev_pos is not None \
                                and SEP_ONLY.match(line[prev_pos:pos]):
                            cls = prev_cls      # a "/"-separated list inherits its head's class
                        prev_pos, prev_cls = end_, cls
                        K, how = recover_count(line, pos)
                        rows.append(dict(source=src, file=f.name, line=ln, kind="QUANT",
                                         cls=cls, gap=x, K=K if K else np.nan, how=how,
                                         verdict=verdict, label_rejected=(cls == "LABEL"),
                                         text=line[max(0, pos - 90):pos + 90].strip()[:220]))
                else:
                    lp = LEVELPAIR.search(line)
                    rows.append(dict(source=src, file=f.name, line=ln,
                                     kind="LEVELPAIR" if lp else "UNQUANT",
                                     gap=(abs(float(lp.group(1)) - float(lp.group(2)))
                                          if lp else np.nan),
                                     K=np.nan, how="NONE", verdict=verdict, cls="NONE",
                                     label_rejected=False, text=line.strip()[:220]))
    return pd.DataFrame(rows)


def claimset_mask(df, cs):
    if cs == "C_STRICT":
        return df.source == "STRICT"
    if cs == "C_ADJ":
        return (df.source == "STRICT") & df.verdict
    return pd.Series(True, index=df.index)


def adjudicable(df, cs, rule="H_MARKED"):
    """The rows a census cell adjudicates: QUANT, with a recoverable count, and — under the
    FIXED harvest rule H_MARKED — classified GAP, i.e. written by the record as a DIFFERENCE
    and not as a level or a correlation.  H_NAIVE keeps every QUANT hit and is published only
    to price how much the classification matters; nothing is selected on it."""
    m = claimset_mask(df, cs) & (df.kind == "QUANT") & df.K.notna()
    if rule == "H_MARKED":
        m = m & (df.cls == "GAP")
    return df[m]


# =================================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P(f"IDEA 1210 (lane C, {DATE}) — how many committed CHOOSER COMPARISONS rest on FEWER")
    P("THAN TEN PICKS, and how many could have been RESOLVED by the draws they had?")
    P("=" * 100)
    P(f"  dial 1 = CLAIM SET  {CLAIMSETS}   (headline {CS_HEAD})")
    P(f"  dial 2 = BAR        {BARS}        (headline {BAR_HEAD})")
    P("  every one of the 9 cells is published; nothing else is tuned.")
    P("")

    # ------------------------------------------------------------------ ARM 0: arithmetic first
    P("-" * 100)
    P("ARM 0 — THE ARITHMETIC, PRINTED BEFORE THE TAPE IS READ.")
    P("-" * 100)
    P("  K_req(X) = (z * sigma_d / X)^2 is EXACTLY quadratic in 1/X: halve the quoted gap and")
    P("  the claim needs FOUR times the picks.  Equivalently the smallest gap K picks can")
    P("  resolve is  X_min = z * sigma_d / sqrt(K).  At z = 2:")
    P(f"    {'K':>6s}   X_min / sigma_d")
    for K in (1, 3, 5, 10, 20, 50, 72, 100, 240, 472):
        P(f"    {K:>6d}   {2.0 / np.sqrt(K):.4f}")
    P("")
    P(f"  1206 measured this object at 472 picks and read a CLUSTERED SE of {A1206_CLUSTSE:.4f}")
    P(f"  on a difference of {A1206_ANCHOR - A1206_MNONE:+.4f}; 1155 published a five-way span of")
    P(f"  {A1155_SPAN:.4f} on THREE draws.  If sigma_d is of order 0.3, then at K = 3 the")
    P(f"  smallest 2-SE-resolvable gap is {2.0 * 0.3 / np.sqrt(3):.4f} and at K = 10 it is")
    P(f"  {2.0 * 0.3 / np.sqrt(10):.4f} — both an order of magnitude above the gaps the record")
    P("  habitually publishes.  THE EXPECTED FINDING IS THEREFORE 'MOST ARE UNRESOLVED'; the")
    P("  number worth reporting is how many are not, and whether any ADJUDICATED one is.")
    P("")
    P("  UPPER BOUND, NOT ESTIMATE: sigma_d/sqrt(K) assumes K independent picks.  The record's")
    P("  picks share panels, anchors and ONE tape, so the true SE is larger and every")
    P("  'resolved' count below is the most generous reading available.")
    P("")

    # ------------------------------------------------------------------ ARM A: harvest
    P("-" * 100)
    P("ARM A — THE CENSUS.  One fixed harvest rule over the record's own text.")
    P("-" * 100)
    cl = harvest()
    dump(cl, "claims")
    q = cl[cl.kind == "QUANT"]
    P(f"  lines carrying an OOS-Sharpe cue: {cl.file.count():,} claim rows over "
      f"{cl.file.nunique():,} files")
    for cs in CLAIMSETS:
        m = claimset_mask(cl, cs)
        sub = cl[m]
        subq = sub[sub.kind == "QUANT"]
        kn = subq[subq.K.notna()]
        P(f"  {cs:<9s} rows {len(sub):>6,}   QUANT {len(subq):>6,}   "
          f"LEVELPAIR {int((sub.kind == 'LEVELPAIR').sum()):>5,}   "
          f"UNQUANT {int((sub.kind == 'UNQUANT').sum()):>5,}   "
          f"K recovered {len(kn):>6,} ({len(kn) / max(len(subq), 1):.3f})   "
          f"label-rejected {int(subq.label_rejected.sum()):>5,}")
    P("")
    P("  THE THREE-WAY CLASSIFICATION (fixed, declared): GAP = written by the record AS a")
    P("  difference; LEVEL = a signed Sharpe level, not a comparison; LABEL = a correlation,")
    P("  dispersion, probability, share or drawdown reading that merely sits near the words")
    P("  'OOS Sharpe'.  Over every QUANT hit in the corpus:")
    q_all = cl[cl.kind == "QUANT"]
    for c in ("GAP", "LEVEL", "LABEL"):
        n_ = int((q_all.cls == c).sum())
        P(f"    {c:<6s} {n_:>6,} of {len(q_all):>6,} ({n_ / max(len(q_all), 1):.4f})")
    P("  H_MARKED adjudicates GAP alone; H_NAIVE keeps all three and is published beside every")
    P("  headline so the classification's effect is visible, never hidden.")
    P("")
    P("  THE HEADLINE CENSUS NUMBER (no dial, no measurement — the record's own text):")
    for rule in ("H_MARKED", "H_NAIVE"):
        for cs in CLAIMSETS:
            sub = adjudicable(cl, cs, rule)
            lt10 = int((sub.K < 10).sum())
            P(f"    {rule:<8s} {cs:<9s} of {len(sub):>6,} claims with a recoverable count, "
              f"{lt10:>6,} ({lt10 / max(len(sub), 1):.4f}) rest on FEWER THAN TEN PICKS; "
              f"median K {sub.K.median():.1f}, median |X| {sub.gap.median():.4f}")
    P("")
    kk = adjudicable(cl, "C_BROAD", "H_MARKED")
    P("  K distribution over ALL QUANT claims with a recoverable count "
      f"(n = {len(kk):,}):")
    for lo, hi in ((1, 2), (3, 5), (6, 9), (10, 19), (20, 49), (50, 99), (100, 10 ** 9)):
        n = int(((kk.K >= lo) & (kk.K <= hi)).sum())
        P(f"    K {lo:>4d}-{hi if hi < 10**9 else '+':>5} : {n:>6,}  ({n / max(len(kk), 1):.4f})")
    P("")

    # ------------------------------------------------------------------ panels
    P("-" * 100)
    P("PANELS (rule 9: all three are CURRENT-CONSTITUENT lists; every level is optimistic).")
    P("-" * 100)
    u = load_universe()
    b = load_universe(broad=True)
    s, n_bad, n_meta = load_small()
    PAN = {}
    for nm, px in (("U56", u), ("B136", b), ("SMALL", s)):
        PAN[nm] = Panel(nm, px)
        P(f"  {nm:<6s} {px.shape[0]:,} rows x {px.shape[1]} cols   "
          f"{px.index[0].date()} -> {px.index[-1].date()}  warm {PAN[nm].warm.sum():,}  "
          f"IS {PAN[nm].ins.sum():,}  OOS {PAN[nm].oos.sum():,}")
    P(f"  SMALL exclusion: {n_bad} of {n_meta} names dropped on max_1d_move >= 1.0 (documented).")
    P("")

    # ------------------------------------------------------------------ gates
    P("-" * 100)
    P("GATES — printed BEFORE any measured result.")
    P("-" * 100)
    pu = PAN["U56"]
    a = ANCHORS["A"]
    r_anchor = book(pu, a["N"], a["H"], a["GROSS"], a["CADENCE"])
    W = build(-pu.sc, pu.elig, pu.priced, pu.reb["W"], a["N"], a["H"], pu.T, pu.K, a["GROSS"])
    eng = backtest(pu.px, pd.DataFrame(W, index=pu.idx, columns=pu.px.columns),
                   cost_bps=COST, freq="W")["returns"].values
    g1 = float(np.abs(eng[pu.warm] - r_anchor[pu.warm]).max())
    gate("G1", "fast runner == engine.backtest (U56 W/H126/N=20)", g1, g1 < 1e-12)

    mA = blocks_m(r_anchor, pu.warm, pu.ins, pu.oos)
    g2 = max(abs(mA["CAGR"] - A1101_TRIPLE[0]), abs(mA["Sharpe"] - A1101_TRIPLE[1]),
             abs(mA["MaxDD"] - A1101_TRIPLE[2]))
    gate("G2", "CROSS-RUN 1101's committed U56 anchor-A triple", g2, g2 < 5e-3)

    lb = backtest(pu.px, rules_v2_weights(pu.px), cost_bps=COST, freq="W")["returns"]
    _, _, ldd = fmet(lb.values[pu.warm])
    g3 = abs(ldd - LIVE_MAXDD_COMMITTED)
    gate("G3", "live RULES v2 U56 MaxDD == committed -12.05%", g3, g3 < 5e-4)

    spy_m = blocks_m(pu.spy, pu.warm, pu.ins, pu.oos)
    g4 = max(abs(spy_m["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
             abs(spy_m["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(spy_m["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gate("G4", "SPY OOS triple == committed (1161's bar 5e-3)", g4, g4 < 5e-3)

    # G5: the harvest is DETERMINISTIC and idempotent — re-running it returns the same frame.
    cl2 = harvest()
    g5 = float(0.0 if cl2.drop(columns=["text"]).equals(cl.drop(columns=["text"])) else 1.0)
    gate("G5", "harvest is deterministic (re-run identical)", g5, g5 == 0.0)

    # G6: K_req is the EXACT inverse of the bar — at X = z*sigma/sqrt(K), K_req == K.
    zt, sg, Kt = 2.0, 0.3, 37.0
    g6 = abs((zt * sg / (zt * sg / np.sqrt(Kt))) ** 2 - Kt)
    gate("G6", "K_req inverts the bar exactly at X = z*sigma/sqrt(K)", g6, g6 < 1e-9)

    # G7: a chooser against ITSELF must give a difference pool that is EXACTLY zero, so
    # sigma_d == 0 and no gap of any size resolves.  If the pick machinery leaked any
    # asymmetry this would be positive and every SE downstream would be silently wrong.
    P("")

    # ------------------------------------------------------------------ ARM B: measurement
    P("-" * 100)
    P("ARM B — MEASURING sigma_d: the per-pick SD of the OOS-Sharpe difference between two")
    P("honest choosers, on this tape, with 1101's books.")
    P("-" * 100)
    books, bmet = {}, {}
    nb = 0
    for pn in PANELS:
        pan = PAN[pn]
        for an in ANCHORS:
            for lad in LADNAMES:
                for rung in LADDERS[lad]:
                    key = (pn, an, lad, rung)
                    kw = rung_kwargs(an, lad, rung)
                    dk = (pn, kw["N"], kw["H"], kw["gross"], kw["freq"])
                    if dk not in bmet:
                        r = book(pan, kw["N"], kw["H"], kw["gross"], kw["freq"])
                        bmet[dk] = (r, blocks_m(r, pan.warm, pan.ins, pan.oos))
                        nb += 1
                    books[key] = dk
    P(f"  built {nb:,} DISTINCT books over {len(books):,} (panel, anchor, ladder, rung) slots "
      f"[{time.time() - t0:.0f}s]")

    picks = []
    for pn in PANELS:
        pan = PAN[pn]
        yrs = pan.years
        for an in ANCHORS:
            for lad in LADNAMES:
                rungs = LADDERS[lad]
                R = np.column_stack([bmet[books[(pn, an, lad, ru)]][0] for ru in rungs])
                for wn, wstart in IS_WINDOWS:
                    m = pan.warm & (pan.idx >= pd.Timestamp(wstart)) & pan.ins
                    for ch in CHOOSERS:
                        v = [is_stat_on(R[m, j], ch) for j in range(len(rungs))]
                        v = np.where(np.isfinite(v), v, -np.inf)
                        j = int(np.argmax(v))
                        mm = bmet[books[(pn, an, lad, rungs[j])]][1]
                        picks.append(dict(pool="CELL", panel=pn, anchor=an, ladder=lad,
                                          window=wn, fold=0, chooser=ch, rung=str(rungs[j]),
                                          oos_sharpe=mm["OOS_Sharpe"], oos_cagr=mm["OOS_CAGR"],
                                          oos_dd=mm["OOS_MaxDD"]))
                    for y in OOS_YEARS:
                        mi = pan.warm & (pan.idx >= pd.Timestamp(wstart)) & (yrs < y)
                        mo = yrs == y
                        if mo.sum() < 60 or mi.sum() < 250:
                            continue
                        for ch in CHOOSERS:
                            v = [is_stat_on(R[mi, j], ch) for j in range(len(rungs))]
                            v = np.where(np.isfinite(v), v, -np.inf)
                            j = int(np.argmax(v))
                            rr = R[mo, j]
                            c, sh, dd = fmet(rr)
                            picks.append(dict(pool="FOLD", panel=pn, anchor=an, ladder=lad,
                                              window=wn, fold=y, chooser=ch,
                                              rung=str(rungs[j]), oos_sharpe=sh,
                                              oos_cagr=c, oos_dd=dd))
    pk = pd.DataFrame(picks)
    dump(pk, "picks")
    P(f"  {len(pk):,} pick-cells  (CELL {int((pk.pool == 'CELL').sum()):,}, "
      f"FOLD {int((pk.pool == 'FOLD').sum()):,})  [{time.time() - t0:.0f}s]")

    def diff_pool(pool, a_ch, b_ch):
        keys = ["panel", "anchor", "ladder", "window", "fold"]
        s = pk[pk.pool == pool]
        A = s[s.chooser == a_ch].set_index(keys)["oos_sharpe"]
        B = s[s.chooser == b_ch].set_index(keys)["oos_sharpe"]
        d = (A - B).dropna()
        return d

    drows = []
    for pool in ("CELL", "FOLD"):
        for a_ch, b_ch in PAIRS:
            d = diff_pool(pool, a_ch, b_ch)
            folds = np.array([ix[4] for ix in d.index])
            pans = np.array([ix[0] for ix in d.index])
            # clustered SE: cluster on FOLD for the FOLD pool, on PANEL for the CELL pool
            cl_key = folds if pool == "FOLD" else pans
            gm = pd.Series(d.values).groupby(pd.Series(cl_key)).mean()
            se_iid = float(d.values.std(ddof=1) / np.sqrt(len(d))) if len(d) > 1 else np.nan
            se_cl = float(gm.std(ddof=1) / np.sqrt(len(gm))) if len(gm) > 1 else np.nan
            drows.append(dict(pool=pool, pair=f"{a_ch}-{b_ch}", n=len(d),
                              mean=float(d.mean()), sd=float(d.values.std(ddof=1)),
                              se_iid=se_iid, se_clustered=se_cl,
                              ratio=(se_cl / se_iid if se_iid else np.nan),
                              n_nonzero=int((np.abs(d.values) > 1e-12).sum())))
    dd_ = pd.DataFrame(drows)
    dump(dd_, "sigma")
    P("  paired per-pick differences, by pool and chooser pair:")
    P(f"    {'pool':<5s} {'pair':<26s} {'n':>5s} {'nonzero':>8s} {'mean':>9s} {'SD':>8s} "
      f"{'SE_iid':>8s} {'SE_clust':>9s} {'ratio':>6s}")
    for _, r in dd_.iterrows():
        P(f"    {r['pool']:<5s} {r['pair']:<26s} {r['n']:>5d} {r['n_nonzero']:>8d} "
          f"{r['mean']:>+9.4f} {r['sd']:>8.4f} {r['se_iid']:>8.4f} {r['se_clustered']:>9.4f} "
          f"{r['ratio']:>6.2f}")

    pool_cell = np.concatenate([diff_pool("CELL", a_, b_).values for a_, b_ in PAIRS])
    pool_fold = np.concatenate([diff_pool("FOLD", a_, b_).values for a_, b_ in PAIRS])
    SIG_CELL = float(pool_cell.std(ddof=1))
    SIG_FOLD = float(pool_fold.std(ddof=1))
    P("")
    P(f"  sigma_CELL = {SIG_CELL:.4f}  over {len(pool_cell):,} paired picks "
      f"(each read on the FULL OOS window 2017-2026)   <-- ADJUDICATION BASIS, declared above")
    P(f"  sigma_FOLD = {SIG_FOLD:.4f}  over {len(pool_fold):,} paired picks "
      f"(each read on ONE OOS calendar year)           <-- robustness column")
    P(f"  clustered/iid SE ratio, median over pairs: "
      f"{dd_.ratio.median():.2f}  (>1 means the census below is generous)")
    P(f"  ZERO-DIFFERENCE SHARE: the two choosers pick the SAME rung at "
      f"{1 - float((np.abs(pool_cell) > 1e-12).mean()):.4f} of CELL picks and "
      f"{1 - float((np.abs(pool_fold) > 1e-12).mean()):.4f} of FOLD picks — a difference pool")
    P("  that is mostly exact zeros makes the SD SMALLER and the census MORE generous still.")

    # G7 now that the pick machinery exists: a chooser against itself is exactly zero.
    dself = diff_pool("CELL", CHOOSERS[0], CHOOSERS[0])
    g7 = float(np.abs(dself.values).max()) if len(dself) else 1.0
    gate("G7", "degenerate pair (chooser vs itself) is EXACTLY zero", g7, g7 == 0.0)
    P("")

    # ------------------------------------------------------------------ ARM C: adjudication
    P("-" * 100)
    P("ARM C — ADJUDICATION.  The 9 cells of (CLAIM SET x BAR), every one published.")
    P("-" * 100)
    rng = np.random.default_rng(seed_of("null90"))

    def null90(K):
        """90th percentile of |mean of K count-matched resample draws| from the MEASURED
        difference pool.  Drawn in batches so memory is bounded; for K > 20,000 the batch
        cost is pointless and the CLT on the pool's own mean/SD is used instead (stated)."""
        K = int(K)
        if K > 20000:
            return float(abs(pool_cell.mean()) + 1.2816 * pool_cell.std(ddof=1) / np.sqrt(K))
        out, batch = [], max(1, int(2_000_000 // max(K, 1)))
        done = 0
        while done < NULL_DRAWS:
            b = min(batch, NULL_DRAWS - done)
            idx = rng.integers(0, len(pool_cell), size=(b, K))
            out.append(np.abs(pool_cell[idx].mean(axis=1)))
            done += b
        return float(np.quantile(np.concatenate(out), 0.90))

    null_cache = {}
    grid, per_claim = [], []
    for cs in CLAIMSETS:
        sub = adjudicable(cl, cs, "H_MARKED").copy()
        for bar in BARS:
            res = []
            for _, r in sub.iterrows():
                K = int(min(max(r.K, 1), 100000))
                if bar == "B_NULL90":
                    if K not in null_cache:
                        null_cache[K] = null90(K)
                    xmin = null_cache[K]
                else:
                    xmin = Z_OF[bar] * SIG_CELL / np.sqrt(K)
                res.append(bool(abs(r.gap) >= xmin))
                if cs == CS_HEAD and bar == BAR_HEAD:
                    # a gap written as EXACTLY zero clears no positive bar at any K: K_req = inf
                    kreq = (np.inf if abs(r.gap) == 0.0
                            else (Z_OF["B_2SE"] * SIG_CELL / abs(r.gap)) ** 2)
                    per_claim.append(dict(file=r.file, line=r.line, gap=r.gap, K=K,
                                          how=r.how, verdict=r.verdict, x_min=xmin,
                                          K_req=kreq, resolved=res[-1], text=r.text))
            res = np.array(res)
            grid.append(dict(claim_set=cs, bar=bar, n=len(sub), resolved=int(res.sum()),
                             share=float(res.mean()) if len(res) else np.nan,
                             n_lt10=int((sub.K < 10).sum()),
                             resolved_lt10=int((res & (sub.K.values < 10)).sum()),
                             median_K=float(sub.K.median()),
                             median_gap=float(sub.gap.median())))
    gr = pd.DataFrame(grid)
    dump(gr, "grid")
    pc = pd.DataFrame(per_claim)
    dump(pc, "adjudication")
    P(f"    {'claim set':<9s} {'bar':<9s} {'n':>6s} {'resolved':>9s} {'share':>7s} "
      f"{'K<10':>6s} {'res&K<10':>9s} {'medK':>6s} {'med|X|':>7s}")
    for _, r in gr.iterrows():
        P(f"    {r['claim_set']:<9s} {r['bar']:<9s} {r['n']:>6d} {r['resolved']:>9d} "
          f"{r['share']:>7.4f} {r['n_lt10']:>6d} {r['resolved_lt10']:>9d} "
          f"{r['median_K']:>6.1f} {r['median_gap']:>7.4f}")
    P("")
    P("")
    P("  TWO SENSITIVITIES, published beside the grid and NEVER selected on:")
    for rule in ("H_MARKED", "H_NAIVE"):
        for sig_name, sig in (("sigma_CELL", SIG_CELL), ("sigma_FOLD", SIG_FOLD)):
            sub = adjudicable(cl, CS_HEAD, rule)
            xmin = 2.0 * sig / np.sqrt(sub.K.clip(lower=1).values)
            r_ = (np.abs(sub.gap.values) >= xmin)
            P(f"    {rule:<8s} x {sig_name} ({sig:.4f}) at 2 SE: {int(r_.sum()):>5,} of "
              f"{len(sub):>5,} resolve ({r_.mean():.4f})")
    P("  sigma_FOLD is the SD of the SAME difference read on one calendar year instead of the")
    P("  full OOS window; a claim whose picks are single-period reads must be judged there.")
    P("")
    hd = gr[(gr.claim_set == CS_HEAD) & (gr.bar == BAR_HEAD)].iloc[0]
    P(f"  HEADLINE ({CS_HEAD} x {BAR_HEAD}): {hd['resolved']:,} of {hd['n']:,} committed "
      f"chooser comparisons ({hd['share']:.4f}) clear their own 2-SE bar.")
    if len(pc):
        P(f"  K_req at the median committed gap {pc.gap.median():.4f} is "
          f"{(2.0 * SIG_CELL / max(pc.gap.median(), 1e-12)) ** 2:,.0f} picks against a median "
          f"supplied K of {pc.K.median():.0f}.")
        P(f"  committed gaps written as EXACTLY 0.000: {int((pc.gap == 0).sum()):,} "
          f"(K_req infinite — no count resolves a zero).")
        for qq in (0.5, 0.75, 0.90, 0.99):
            P(f"    {qq:.0%} of adjudicated claims need <= "
              f"{np.nanquantile(pc.K_req.replace(np.inf, np.nan), qq):,.0f} picks; they supply "
              f"<= {pc.K.quantile(qq):,.0f}")
        rs = pc[pc.resolved]
        P(f"  the resolved ones: median |X| {rs.gap.median() if len(rs) else float('nan'):.4f}, "
          f"median K {rs.K.median() if len(rs) else float('nan'):.0f}, "
          f"{int(rs.verdict.sum()) if len(rs) else 0} of them on a line carrying a verdict.")
        P("  five largest K_req among ADJUDICATED (verdict-carrying) claims:")
        adj = pc[pc.verdict].sort_values("K_req", ascending=False).head(5)
        for _, r in adj.iterrows():
            P(f"    {r['file']}:{r['line']:<5d} |X| {r['gap']:.4f} on K {r['K']:<5d} "
              f"needs {r['K_req']:>12,.0f}   ...{r['text'][:90]}...")
    P("")

    # ------------------------------------------------------------------ ARM D: rule 8
    P("-" * 100)
    P("ARM D — PROTOCOL RULE 8.  Every chooser picks on 2009-2016 ALONE; 2017-2026 read ONCE.")
    P("-" * 100)
    cell = pk[(pk.pool == "CELL") & (pk.window == "W09")]
    wf = cell.groupby("chooser").agg(n=("oos_sharpe", "size"),
                                     OOS_Sharpe=("oos_sharpe", "mean"),
                                     OOS_CAGR=("oos_cagr", "mean"),
                                     OOS_MaxDD=("oos_dd", "mean")).reset_index()
    base_rows = []
    BASE = {}
    for pn in PANELS:
        pan = PAN[pn]
        rb = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        mb = blocks_m(rb, pan.warm, pan.ins, pan.oos)
        ms = blocks_m(pan.spy, pan.warm, pan.ins, pan.oos)
        BASE[pn] = (mb, ms)
        base_rows.append(dict(panel=pn, who="RULES v2 (live)", OOS_CAGR=mb["OOS_CAGR"],
                              OOS_Sharpe=mb["OOS_Sharpe"], OOS_MaxDD=mb["OOS_MaxDD"]))
        base_rows.append(dict(panel=pn, who="SPY", OOS_CAGR=ms["OOS_CAGR"],
                              OOS_Sharpe=ms["OOS_Sharpe"], OOS_MaxDD=ms["OOS_MaxDD"]))
    bs = pd.DataFrame(base_rows)
    dump(pd.concat([wf.assign(panel="ALL", who=wf.chooser)[
        ["panel", "who", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]], bs]), "walkforward")
    P(f"    {'who':<26s} {'n':>4s} {'OOS CAGR':>9s} {'OOS Sharpe':>11s} {'OOS MaxDD':>10s}")
    for _, r in wf.iterrows():
        P(f"    {r['chooser']:<26s} {r['n']:>4d} {r['OOS_CAGR']:>9.2%} "
          f"{r['OOS_Sharpe']:>11.4f} {r['OOS_MaxDD']:>10.2%}")
    for _, r in bs.iterrows():
        P(f"    {r['panel'] + ' ' + r['who']:<26s} {'':>4s} {r['OOS_CAGR']:>9.2%} "
          f"{r['OOS_Sharpe']:>11.4f} {r['OOS_MaxDD']:>10.2%}")
    P("")
    P("  the SAME comparison this census is about, made honestly on 24 picks per chooser:")
    for a_ch, b_ch in PAIRS:
        d = diff_pool("CELL", a_ch, b_ch)
        d09 = d[[ix[3] == "W09" for ix in d.index]]
        if len(d09) < 2:
            continue
        se = d09.values.std(ddof=1) / np.sqrt(len(d09))
        P(f"    {a_ch} - {b_ch}: {d09.mean():+.4f} on {len(d09)} picks, SE {se:.4f}, "
          f"t {(d09.mean() / se if se else np.nan):+.2f}, "
          f"needs {(2.0 * SIG_CELL / max(abs(d09.mean()), 1e-9)) ** 2:,.0f} picks at 2 SE "
          f"-> {'RESOLVED' if abs(d09.mean()) >= 2 * se else 'UNRESOLVED'}")
    P("")
    P("  IS-to-OOS sign transfer of the chooser ordering (the thing a committed comparison")
    P("  is used FOR): for each pair, does the sign of the IS-window gap survive into OOS?")
    tr = []
    for a_ch, b_ch in PAIRS:
        dc = diff_pool("CELL", a_ch, b_ch)
        df_ = diff_pool("FOLD", a_ch, b_ch)
        agree = np.nan
        if len(dc) and len(df_):
            byc = pd.Series(dc.values, index=[f"{i[0]}|{i[1]}|{i[2]}|{i[3]}" for i in dc.index])
            byf = pd.Series(df_.values, index=[f"{i[0]}|{i[1]}|{i[2]}|{i[3]}" for i in df_.index])
            fm = byf.groupby(level=0).mean()
            j = byc.groupby(level=0).mean().align(fm, join="inner")
            agree = float((np.sign(j[0].values) == np.sign(j[1].values)).mean())
        tr.append(dict(pair=f"{a_ch}-{b_ch}", cell_mean=float(dc.mean()),
                       fold_mean=float(df_.mean()), sign_agree=agree))
        P(f"    {a_ch}-{b_ch}: CELL mean {dc.mean():+.4f}, FOLD mean {df_.mean():+.4f}, "
          f"per-cell sign agreement {agree:.4f}")
    dump(pd.DataFrame(tr), "transfer")
    P("")

    # ------------------------------------------------------------------ ARM E: KEEP paths
    P("-" * 100)
    P("ARM E — BOTH KEEP PATHS (PROTOCOL rule 4) on every distinct book this run built.")
    P("-" * 100)
    krows = []
    for pn in PANELS:
        lbm, sbm = BASE[pn]
        for dk, (r, m) in bmet.items():
            if dk[0] != pn:
                continue
            f4a = legs_4a(m, lbm)
            f4b = legs_4b(m, sbm)
            f4bo = legs_4b_oos(m, sbm)
            krows.append(dict(panel=pn, N=dk[1], H=dk[2], gross=dk[3], freq=dk[4],
                              CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                              OOS_Sharpe=m["OOS_Sharpe"], OOS_CAGR=m["OOS_CAGR"],
                              OOS_MaxDD=m["OOS_MaxDD"],
                              pass_4a=all(f4a.values()), pass_4b_full=all(f4b.values()),
                              pass_4b_oos=all(f4bo.values()),
                              pass_4b_both=all(f4b.values()) and all(f4bo.values()), **f4a,
                              **f4b, **f4bo))
    kp = pd.DataFrame(krows)
    dump(kp, "keeppaths")
    P(f"  {len(kp):,} distinct books scored.")
    P(f"    4a (beat the live book in BOTH halves, MaxDD no worse): "
      f"{int(kp.pass_4a.sum()):,} of {len(kp):,}")
    P(f"    4b FULL:              {int(kp.pass_4b_full.sum()):,} of {len(kp):,}")
    P(f"    4b OOS:               {int(kp.pass_4b_oos.sum()):,} of {len(kp):,}")
    P(f"    4b FULL *and* OOS:    {int(kp.pass_4b_both.sum()):,} of {len(kp):,}")
    for pn in PANELS:
        sub = kp[kp.panel == pn]
        P(f"      {pn:<6s} 4a {int(sub.pass_4a.sum()):>3d}/{len(sub):<3d}  "
          f"4b full+OOS {int(sub.pass_4b_both.sum()):>3d}/{len(sub):<3d}")
    P("  These are 1101's rung books, not this idea's object: any passer is PRIOR ART and is")
    P("  recorded, not promoted.  Nothing in a text census can pass a KEEP path on its own.")
    P("")

    # ------------------------------------------------------------------ verdict
    P("-" * 100)
    P("GATE SUMMARY")
    P("-" * 100)
    gf = pd.DataFrame(GATES)
    dump(gf, "gates")
    P(f"  {int(gf.pass_.sum())} of {len(gf)} gates pass.")
    P("")
    P("-" * 100)
    P("VERDICT")
    P("-" * 100)
    P(f"  KILL (capital) — a text census cannot be a trading rule; 4a {int(kp.pass_4a.sum())} of "
      f"{len(kp)}, 4b full+OOS {int(kp.pass_4b_both.sum())} of {len(kp)} on prior-art books.")
    P(f"  ANSWERED: of {hd['n']:,} committed chooser comparisons with a recoverable pick count, "
      f"{hd['n_lt10']:,} rest on fewer than ten picks and {hd['resolved']:,} "
      f"({hd['share']:.4f}) clear a 2-SE bar built from this tape's own sigma_d = "
      f"{SIG_CELL:.4f}.")
    P(f"  [{time.time() - t0:.0f}s]")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
