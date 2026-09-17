#!/usr/bin/env python3
"""
Idea 1211 (lane B, 2026-09-17) — is the RECORD's COUNT CUE the CLAIM's OWN COUNT?

THE PREMISE, READ FROM THE RECORD AND NEVER RECALLED.  Idea 1210 (lane C, 2026-09-17,
`2026-09-17_how-many-committed-CHOOSER-COMPARISONS-rest-on-FEWER-THAN-TEN-PICKS_C.py`)
adjudicated 165 committed OOS-Sharpe GAP claims against K_req = (2*sigma_d/X)^2 and published
80 of 165 (0.4848) resolved at 2 SE, 44 of 165 (0.2667) resting on fewer than ten picks,
median K 21.  Every one of those K's came out of the TEXT by one rule: the count cue NEAREST
the gap number on the same line.  1210 wrote that limit down itself (its Limits section, item
2): "Where a line quotes several counts, the nearest one may not be the claim's own."

THE QUEUE'S QUESTION, VERBATIM: "Re-recover K from the SCRIPT that produced each row instead
of from the text, and report how many claims the text mis-counts and in which direction."

WHAT IS MEASURED HERE, AND WHAT IS ONLY HARVESTED.  The claim frame is 1210's own committed
adjudication artefact, taken verbatim — the object under study is exactly the 165 claims 1210
counted, not a re-harvest of a corpus that has grown since.  The script behind each claim is
recovered by a fixed mapping rule, and the counts that script can actually supply are read off
the ARTEFACTS it emitted (`<stem>.<suffix>.csv`, one row per unit).  The only thing this script
MEASURES on the tape is sigma_d, re-measured with 1210's construction inherited whole, because
sigma_d is what turns a count into a verdict.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  RECOVERY RULE {R_NOUN, R_NEAREST, R_MAXART}   how K is read off the script
  CLAIM SET     {C_STRICT, C_ADJ, C_BROAD}      which text counts as committed

  = 9 cells, EVERY ONE PUBLISHED.  The HEADLINE cell is R_NOUN x C_STRICT, declared here
  before any number is read.

    R_NOUN     the claim's own count NOUN (picks / books / cells / decisions / folds /
               claims / rungs / arms / offsets / comparisons / draws / rows) is mapped by a
               FIXED vocabulary to an artefact SUFFIX; K_SCRIPT = that artefact's data-row
               count.  No noun, or no matching artefact -> UNMAPPED, never imputed.
               THE HONEST RULE: it identifies the referent before it reads a number.
    R_NEAREST  K_SCRIPT = the supplied count closest to K_TEXT in log distance.  THE MOST
               GENEROUS RULE BY CONSTRUCTION — it hands the text the best artefact available
               after seeing the text's answer.  A mis-count under R_NEAREST is a HARD miss:
               no artefact of that script carries anything near the quoted count.
    R_MAXART   K_SCRIPT = the LARGEST data-row count the script emitted.  An UPPER BOUND on
               what the script could have averaged over: K_TEXT > R_MAXART means the claim
               quotes more units than the script's biggest table has rows.

    C_STRICT   1210's committed adjudication frame, 165 rows, verbatim from
               `...FEWER-THAN-TEN-PICKS_C.adjudication.csv`.  FROZEN — the record has grown
               since 1210 ran and a re-harvest would not be the same object.
    C_ADJ      the C_STRICT subset whose line also carries a committed verdict token
               (1210's own `verdict` column) — a claim that adjudicated something.
    C_BROAD    a FRESH harvest under 1210's rule, verbatim, over LEADERBOARD.md +
               CHANGELOG.md + every research/backtests/*.memo.md and *.result.md.  This one
               moves with the corpus and prices how much the frozen frame leaves out.

WHAT IS NOT A DIAL, fixed before any artefact is read and never re-tuned:
  * HARVEST.  1210's CUE / GAP_SIGNED / GAP_BY / classify / recover_count are copied here
    CHARACTER FOR CHARACTER and gated (G6) to reproduce 1210's own K on all 165 frozen rows.
  * CLAIM RELOCATION.  The record PREPENDS rows, so 1210's stored line numbers are stale (17
    of 165 still match).  Each frozen claim is relocated by EXACT substring match of its
    stored +/-90-character text in the current file; the FIRST match wins.  A claim that does
    not relocate is dropped, never guessed.
  * SCRIPT MAPPING.  LEADERBOARD.md row -> the LAST `*.py` token on that row (the table's own
    Script column).  CHANGELOG.md line -> the nearest `*.py` token at or above it inside the
    same `## ` section.  A *.memo.md / *.result.md line -> its own stem + ".py".  No match, or
    the file is absent from research/backtests/ -> UNMAPPED, never imputed.
  * SUPPLY SET.  For a script `<stem>.py`, the multiset of data-row counts (physical lines
    minus the header) of every `<stem>.<suffix>.csv` beside it.  These are the tables the
    script itself wrote one row per unit into.  A script that emitted none is UNMEASURABLE
    and is reported as such, NOT as a mis-count.
  * MEASUREMENT.  PANEL {U56, B136, SMALL} (rule 9), ANCHOR {A, B}, LADDERS {N, H, GROSS,
    CADENCE}, CHOOSERS {CH_ISSHARPE, CH_ISCAGR, CH_ISDD}, IS windows, 10 bps (rule 2), LAG 1,
    warm-up 260, max_vol 0.60, IS end 2016-12-31 — 1101/1154/1206/1210's, inherited whole.
  * ADJUDICATION.  1210's, verbatim: a claim quoting |X| on K picks resolves at 2 SE iff
    |X| >= 2*sigma_CELL/sqrt(K).

DECLARED BEFORE ANY ARTEFACT IS READ:
  (1) THE TRAP IN THE FLIP COUNT.  Resolution is MONOTONE in K and K enters only as a square
      root, so a mis-count of a factor f moves the bar by sqrt(f) — a claim whose count is
      wrong by 2x moves its bar by 1.41x, and most claims sit nowhere near their bar (1210's
      median claim needs 22 picks and supplies 21; its 90th percentile needs 3,969 and
      supplies 213).  THE FLIP COUNT IS THEREFORE EXPECTED TO BE SMALL WHATEVER THE MIS-COUNT
      RATE, and a small flip count is NOT evidence the counts are right.  The headline of this
      run is the MIS-COUNT RATE AND ITS DIRECTION; the flip count is reported beside it and
      never in its place.
  (2) R_NEAREST IS GENEROUS BY CONSTRUCTION and R_NOUN IS NOT.  Agreement under R_NEAREST is
      an UPPER BOUND on how often the text is right; disagreement under R_NEAREST is a LOWER
      BOUND on how often it is wrong.  Anything in between is the referent problem, which is
      what the queue asked about.
  (3) THIS IS A CENSUS, NOT A TRADING RULE.  Nothing here can pass 4a or 4b on its own; the
      KEEP-path arm scores the rung BOOKS the measurement builds and any passer is prior art.

PROTOCOL: rule 2 costs 10 bps and t+1 execution throughout; rule 8 walk-forward in Arm E
(every chooser picks on 2009-2016 alone, 2017-2026 read ONCE) with OOS CAGR / Sharpe / MaxDD
against the live RULES v2 baseline and SPY; BOTH KEEP paths on every distinct book in Arm F;
rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT
modified by this script.

Runs standalone and offline:
  python research/backtests/2026-09-17_is-the-RECORD-s-COUNT-CUE-the-CLAIM-s-OWN-COUNT_B.py
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
SLUG = "is-the-RECORD-s-COUNT-CUE-the-CLAIM-s-OWN-COUNT"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"
BT = ROOT / "research" / "backtests"

# 1210's committed claim frame — the frozen object under study.
FRAME_1210 = BT / "2026-09-17_how-many-committed-CHOOSER-COMPARISONS-rest-on-FEWER-THAN-TEN-PICKS_C.adjudication.csv"

# ----- 1101/1154/1206/1210's construction, inherited whole -------------------------------------
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
RULES = ["R_NOUN", "R_NEAREST", "R_MAXART"]
CLAIMSETS = ["C_STRICT", "C_ADJ", "C_BROAD"]
RULE_HEAD, CS_HEAD = "R_NOUN", "C_STRICT"
SEED_BASE = 12111211
AUDIT_N, AUDIT_SEED = 20, 1211

# ----- the record's own committed numbers, QUOTED and GATED, never re-derived ------------------
A1101_TRIPLE = (0.155787, 1.139701, -0.191276)      # U56 anchor-A CAGR / Sharpe / MaxDD
LIVE_MAXDD_COMMITTED = -0.1205                      # live RULES v2 on U56
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)       # SPY OOS CAGR / Sharpe / MaxDD
A1210_SIGCELL = 0.1176                              # 1210's committed sigma_CELL
A1210_N = 165                                       # 1210's committed C_STRICT claim count
A1210_LT10 = 44                                     # ... of which rest on fewer than ten picks
A1210_RESOLVED = 80                                 # ... resolved at 2 SE
A1210_MEDK = 21.0

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
# 1101/1154/1206/1210's runner and metrics, verbatim
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
# 1210's HARVEST, copied character for character (gated at G5/G6)
# =================================================================================================
CUE = re.compile(r"OOS\s+(?:mean\s+)?Sharpe|mean\s+OOS\s+Sharpe|OOS\s+regret", re.I)
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
LABELS = re.compile(
    r"\b(?:spearman|pearson|kendall|rho|corr|r\^?2|t|z|se|sd|std|p|prob|share|rate|freq|"
    r"maxdd|dd|drawdown|vol|turnover|percentile|pct|quantile|median split|cagr)\b"
    r"(?:\s*\([^()0-9]*\))?[^0-9A-Za-z]*$", re.I)
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
    end = pos + len(ln_txt)
    tail = line[end:end + 6]
    return not (tail[:1] == "%" or re.match(r"\*{0,2}\s?(?:%|pp\b)", tail))


NOUN_VOCAB = ["picks", "draws", "decisions", "cells", "books", "folds", "arms", "offsets",
              "comparisons", "rungs", "claims", "rows", "pairs", "panels", "ladders"]
NOUN_AFTER = re.compile(r"[^A-Za-z]{0,24}([A-Za-z-]+)")


def _noun_of_word(m):
    """The plural noun the CNT_WORD / CNT_PROD match itself consumed."""
    tail = m.group(0)
    for n in NOUN_VOCAB:
        if tail.lower().rstrip().endswith(n):
            return n
    return None


def _noun_after_of(line, m):
    """For an 'N of M' cue, the first vocabulary noun within 40 characters after the cue."""
    seg = line[m.end():m.end() + 40].lower()
    for w in re.findall(r"[a-z-]+", seg):
        if w in NOUN_VOCAB:
            return w
    return None


def recover_count(line, pos, want_noun=False):
    """1210's rule, verbatim: the count cue NEAREST the gap number on the same line.
    want_noun additionally returns the NOUN that cue names, which is what R_NOUN needs to
    identify the referent.  The (K, how) return is bit-identical to 1210's (gated, G6)."""
    cands = []
    for m in CNT_PROD.finditer(line):
        v = int(m.group(1)) * int(m.group(2)) * (int(m.group(3)) if m.group(3) else 1)
        cands.append((abs(m.start() - pos), v, "PROD", _noun_of_word(m)))
    for m in CNT_OF.finditer(line):
        cands.append((abs(m.start() - pos), int(m.group(2)), "OF", _noun_after_of(line, m)))
    for m in CNT_WORD.finditer(line):
        cands.append((abs(m.start() - pos), int(m.group(1)), "WORD", _noun_of_word(m)))
    cands = [c for c in cands if 1 <= c[1] <= 100000]
    if not cands:
        return (None, "NONE", None) if want_noun else (None, "NONE")
    cands.sort(key=lambda c: (c[0], -c[1]))
    _, v, how, noun = cands[0]
    return (v, how, noun) if want_noun else (v, how)


def gap_pos(line: str, snippet: str, gap: float):
    """Where on the CURRENT line the frozen claim's gap number sits.  1210 stored the claim
    as line[pos-90:pos+90].strip(), so inside that snippet the number sits at index ~90; the
    occurrence nearest that index is the claim's own.  Fixed, no tuning."""
    pos_snip = line.find(snippet)
    if pos_snip < 0:
        return None
    forms = [f"{gap:.4f}", f"{gap:.4f}".rstrip("0"), f"{gap:.3f}", f"{gap:.2f}", f"{gap:g}"]
    for form in forms:
        occ = [i for i in range(len(snippet)) if snippet.startswith(form, i)]
        if occ:
            return pos_snip + min(occ, key=lambda i: abs(i - 90))
    return None


def harvest():
    """1210's harvest, verbatim, plus the source FILE PATH so a claim can be mapped to its
    script.  Nothing else is changed."""
    strict_files = [ROOT / "research" / "LEADERBOARD.md", ROOT / "research" / "CHANGELOG.md"]
    broad_files = sorted(set(list(BT.glob("*.memo.md")) + list(BT.glob("*.result.md"))))
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
                            cls = prev_cls
                        prev_pos, prev_cls = end_, cls
                        K, how, noun = recover_count(line, pos, want_noun=True)
                        rows.append(dict(source=src, file=f.name, path=str(f), line=ln,
                                         kind="QUANT", cls=cls, gap=x,
                                         K=K if K else np.nan, how=how, noun=noun,
                                         verdict=verdict, label_rejected=(cls == "LABEL"),
                                         text=line[max(0, pos - 90):pos + 90].strip()[:220]))
                else:
                    lp = LEVELPAIR.search(line)
                    rows.append(dict(source=src, file=f.name, path=str(f), line=ln,
                                     kind="LEVELPAIR" if lp else "UNQUANT",
                                     gap=(abs(float(lp.group(1)) - float(lp.group(2)))
                                          if lp else np.nan),
                                     K=np.nan, how="NONE", noun=None, verdict=verdict,
                                     cls="NONE", label_rejected=False, text=line.strip()[:220]))
    return pd.DataFrame(rows)


# =================================================================================================
# SCRIPT MAPPING and SUPPLY SETS — the fixed rules declared in the header
# =================================================================================================
PY = re.compile(r"([0-9A-Za-z][-0-9A-Za-z_.]*\.py)")
_FILE_CACHE: dict[str, list[str]] = {}


def lines_of(p: Path) -> list[str]:
    k = str(p)
    if k not in _FILE_CACHE:
        _FILE_CACHE[k] = p.read_text(errors="replace").split("\n")
    return _FILE_CACHE[k]


def script_for(fname: str, lineno: int) -> tuple[str | None, str]:
    """LEADERBOARD row -> the LAST *.py token on the row (its own Script column).
    CHANGELOG line   -> the nearest *.py token at or above it inside the same '## ' section.
    memo/result line -> its own stem + '.py'.  Fixed, declared, never imputed."""
    if fname == "LEADERBOARD.md":
        L = lines_of(ROOT / "research" / "LEADERBOARD.md")
        if not (1 <= lineno <= len(L)):
            return None, "OOR"
        hits = PY.findall(L[lineno - 1])
        return (hits[-1], "ROW") if hits else (None, "NOPY")
    if fname == "CHANGELOG.md":
        L = lines_of(ROOT / "research" / "CHANGELOG.md")
        if not (1 <= lineno <= len(L)):
            return None, "OOR"
        for i in range(lineno - 1, -1, -1):
            hits = PY.findall(L[i])
            if hits:
                return hits[-1], "SECTION"
            if L[i].startswith("## ") and i != lineno - 1:
                return None, "SECTION_NOPY"
        return None, "NOPY"
    for suf in (".memo.md", ".result.md"):
        if fname.endswith(suf):
            return fname[: -len(suf)] + ".py", "SELF"
    return None, "UNKNOWN"


def rowcount(p: Path) -> int:
    n = 0
    with open(p, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            n += b.count(b"\n")
    return max(n - 1, 0)          # physical lines minus the header


_SUPPLY: dict[str, dict[str, int]] = {}


def supply_of(script: str) -> dict[str, int]:
    """{artefact suffix -> data-row count} for every <stem>.<suffix>.csv beside the script."""
    if script in _SUPPLY:
        return _SUPPLY[script]
    out: dict[str, int] = {}
    if script and (BT / script).exists():
        stem = script[:-3]
        for p in sorted(BT.glob(stem + ".*.csv")):
            suf = p.name[len(stem) + 1:-4]
            out[suf] = rowcount(p)
    _SUPPLY[script] = out
    return out


# noun -> ORDERED artefact-suffix vocabulary.  Fixed before any artefact was read.
NOUN_ART = {
    "picks":       ["picks", "pick", "draws", "picked"],
    "draws":       ["draws", "draw", "picks", "null"],
    "decisions":   ["decisions", "decision", "picks"],
    "cells":       ["cells", "cell", "grid"],
    "books":       ["books", "book", "keeppaths", "keep"],
    "folds":       ["folds", "fold", "walkforward"],
    "arms":        ["arms", "arm"],
    "offsets":     ["offsets", "offset"],
    "comparisons": ["comparisons", "pairs", "compare", "adjudication"],
    "rungs":       ["rungs", "rung", "ladder", "ladders"],
    "claims":      ["claims", "claim", "adjudication", "census"],
    "rows":        ["rows"],
    "pairs":       ["pairs", "pair", "comparisons"],
    "panels":      ["panels", "panel"],
    "ladders":     ["ladders", "ladder", "rungs"],
}


def k_script(rule: str, K_TEXT: float, noun, sup: dict[str, int]):
    """K recovered from the SCRIPT under one of the three declared rules.
    Returns (K_SCRIPT or None, which artefact suffix supplied it)."""
    if not sup:
        return None, "NO_ARTEFACT"
    if rule == "R_NOUN":
        if not noun or noun not in NOUN_ART:
            return None, "NO_NOUN"
        for suf in NOUN_ART[noun]:
            for have in sup:
                if have.lower() == suf or have.lower().endswith("_" + suf) \
                        or have.lower().startswith(suf):
                    return sup[have], have
        return None, "NO_MATCHING_ARTEFACT"
    if rule == "R_MAXART":
        s = max(sup, key=lambda k: (sup[k], k))
        return sup[s], s
    # R_NEAREST — the most generous rule: the closest supplied count in log distance.
    kt = max(float(K_TEXT), 1.0)
    best = min(sup, key=lambda k: (abs(np.log(max(sup[k], 1)) - np.log(kt)), k))
    return sup[best], best


# =================================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P(f"IDEA 1211 (lane B, {DATE}) — is the RECORD's COUNT CUE the CLAIM's OWN COUNT?")
    P("Re-recover K from the SCRIPT that produced each row, not from the text.")
    P("=" * 100)
    P(f"  dial 1 = RECOVERY RULE  {RULES}      (headline {RULE_HEAD})")
    P(f"  dial 2 = CLAIM SET      {CLAIMSETS}  (headline {CS_HEAD})")
    P("  every one of the 9 cells is published; nothing else is tuned.")
    P("")

    # ------------------------------------------------------------------ ARM 0: the trap first
    P("-" * 100)
    P("ARM 0 — THE TRAP, PRINTED BEFORE ANY ARTEFACT IS READ.")
    P("-" * 100)
    P("  Resolution is |X| >= 2*sigma/sqrt(K): MONOTONE in K, and K enters as a SQUARE ROOT.")
    P("  A count wrong by a factor f moves the bar by sqrt(f):")
    P(f"    {'f':>8s}  bar moves by")
    for f in (1.5, 2.0, 3.0, 4.0, 10.0, 12.0, 100.0):
        P(f"    {f:>8.1f}  {np.sqrt(f):.4f}x")
    P("  1210's median claim needs 22 picks and supplies 21; its 90th percentile needs 3,969")
    P("  and supplies 213.  Most claims are nowhere near their bar, so THE FLIP COUNT IS")
    P("  EXPECTED TO BE SMALL WHATEVER THE MIS-COUNT RATE.  A small flip count is NOT evidence")
    P("  the counts are right.  The headline here is the MIS-COUNT RATE AND ITS DIRECTION.")
    P("  R_NEAREST is generous BY CONSTRUCTION (it picks the artefact after seeing the text's")
    P("  answer): agreement under it is an UPPER bound, disagreement a LOWER bound.")
    P("")

    # ------------------------------------------------------------------ ARM A: the claim frame
    P("-" * 100)
    P("ARM A — THE CLAIM FRAME.  1210's committed adjudication artefact, taken verbatim.")
    P("-" * 100)
    fr = pd.read_csv(FRAME_1210)
    P(f"  {FRAME_1210.name}: {len(fr):,} rows  "
      f"(LEADERBOARD {int((fr.file == 'LEADERBOARD.md').sum())}, "
      f"CHANGELOG {int((fr.file == 'CHANGELOG.md').sum())})")
    g0 = abs(len(fr) - A1210_N)
    gate("G0", "1210's committed frame is 165 claims", g0, g0 == 0)

    # relocate every frozen claim in the CURRENT file (the record PREPENDS rows)
    rel = []
    for _, r in fr.iterrows():
        L = lines_of(ROOT / "research" / str(r.file))
        t = str(r.text)
        stored_ok = (1 <= int(r.line) <= len(L)) and t in L[int(r.line) - 1]
        idx = [i + 1 for i, l in enumerate(L) if t in l]
        rel.append(dict(file=r.file, line_1210=int(r.line),
                        line_now=(idx[0] if idx else -1), stored_ok=stored_ok,
                        n_matches=len(idx)))
    rl = pd.DataFrame(rel)
    P(f"  1210's stored line still matches: {int(rl.stored_ok.sum())} of {len(rl)} "
      f"(the record PREPENDS rows, so line numbers are stale)")
    P(f"  relocated by exact text match:    {int((rl.line_now > 0).sum())} of {len(rl)}  "
      f"(ambiguous, >1 match: {int((rl.n_matches > 1).sum())})")
    g1 = float(len(rl) - int((rl.line_now > 0).sum()))
    gate("G1", "every frozen claim relocates in the current record", g1, g1 == 0)

    fr["line_now"] = rl.line_now.values
    fr["cid"] = np.arange(len(fr))

    # re-derive K (and the NOUN its cue names) from the text at the relocated line; the K must
    # equal 1210's, which is what makes this run a re-recovery of the SAME claims.
    kchk, nouns, hows = [], [], []
    for _, r in fr.iterrows():
        if r.line_now <= 0:
            kchk.append(np.nan)
            nouns.append(None)
            hows.append("NOLINE")
            continue
        line = lines_of(ROOT / "research" / str(r.file))[int(r.line_now) - 1]
        off = gap_pos(line, str(r.text), float(r.gap))
        K, how, noun = recover_count(line, off if off is not None else 0, want_noun=True)
        kchk.append(K if K else np.nan)
        nouns.append(noun)
        hows.append(how)
    fr["K_recheck"] = kchk
    fr["noun"] = nouns
    fr["how_now"] = hows
    ok = fr.K_recheck.notna() & (fr.K_recheck == fr.K)
    g2 = float(1.0 - ok.mean())
    gate("G2", "1210's K reproduces from the relocated text (share failing)", g2, g2 < 0.05)
    P(f"     {int(ok.sum())} of {len(fr)} rows reproduce 1210's K exactly from the current text.")
    P("  what the count cue NAMES, over the frozen frame:")
    vc = pd.Series([n if n else "(no noun)" for n in nouns]).value_counts()
    for k, v in vc.items():
        P(f"    {str(k):<14s} {v:>4d}  ({v / len(fr):.4f})")
    P("")

    # ------------------------------------------------------------------ ARM B: script mapping
    P("-" * 100)
    P("ARM B — THE SCRIPT BEHIND EACH CLAIM, and what counts that script can SUPPLY.")
    P("-" * 100)
    scr, how_m = [], []
    for _, r in fr.iterrows():
        s, h = script_for(str(r.file), int(r.line_now)) if r.line_now > 0 else (None, "NOLINE")
        scr.append(s)
        how_m.append(h)
    fr["script"] = scr
    fr["map_how"] = how_m
    fr["script_exists"] = [bool(s) and (BT / s).exists() for s in scr]
    P(f"  mapped to a script:            {int(fr.script.notna().sum()):>4d} of {len(fr)}")
    P(f"  ... and the script is on disk: {int(fr.script_exists.sum()):>4d} of {len(fr)}  "
      f"over {fr.loc[fr.script_exists, 'script'].nunique()} distinct scripts")
    for k, v in fr.map_how.value_counts().items():
        P(f"    mapping route {str(k):<14s} {v:>4d}")

    t_sup = time.time()
    sups = [supply_of(s) if ex else {} for s, ex in zip(fr.script, fr.script_exists)]
    fr["n_artefacts"] = [len(s) for s in sups]
    fr["max_supply"] = [max(s.values()) if s else np.nan for s in sups]
    P(f"  artefact scan: {len(_SUPPLY)} scripts, "
      f"{sum(len(v) for v in _SUPPLY.values())} CSVs  [{time.time() - t_sup:.0f}s]")
    P(f"  claims whose script emitted at least one artefact: "
      f"{int((fr.n_artefacts > 0).sum())} of {len(fr)} "
      f"(UNMEASURABLE, not mis-counted: {int((fr.n_artefacts == 0).sum())})")
    P("")

    # the rule-free containment test: is the text's count ANY count the script supplies?
    in_supply = [bool(s) and int(k) in set(s.values()) for s, k in zip(sups, fr.K)]
    fr["in_supply"] = in_supply
    meas = fr[fr.n_artefacts > 0]
    P("  RULE-FREE CONTAINMENT (no recovery rule, no referent assumed): is K_TEXT equal to")
    P("  ANY data-row count the script emitted?")
    P(f"    {int(meas.in_supply.sum())} of {len(meas)} "
      f"({meas.in_supply.mean() if len(meas) else np.nan:.4f}) measurable claims — "
      f"{len(meas) - int(meas.in_supply.sum())} quote a count NO artefact of their own script "
      f"carries.")
    P("")

    # ------------------------------------------------------------------ ARM C: the 9 cells
    P("-" * 100)
    P("ARM C — THE 9 CELLS OF (RECOVERY RULE x CLAIM SET), EVERY ONE PUBLISHED.")
    P("-" * 100)
    P("  building C_BROAD by re-harvesting the current corpus under 1210's rule ...")
    cl = harvest()
    dump(cl, "claims")
    broad = cl[(cl.kind == "QUANT") & (cl.cls == "GAP") & cl.K.notna()].copy()
    P(f"  fresh harvest: {len(cl):,} claim rows over {cl.file.nunique():,} files; "
      f"{len(broad):,} GAP claims with a recoverable count (C_BROAD)")
    strict_now = broad[broad.source == "STRICT"]
    P(f"  drift check: C_STRICT re-harvested TODAY gives {len(strict_now):,} claims against "
      f"1210's committed {A1210_N}; C_BROAD gives {len(broad):,} against its committed 196.")
    P("  The frozen frame is still this run's C_STRICT — the object under study is the claims")
    P("  1210 counted — but on this corpus a re-harvest happens to agree, so nothing in the")
    P("  headline turns on the choice.")
    g3 = float(max(0, A1210_N - len(strict_now)))
    gate("G3", "the record is append-only (today's re-harvest >= 1210's 165)", g3, g3 == 0)

    bscr, bhow = [], []
    for _, r in broad.iterrows():
        s, h = script_for(str(r.file), int(r.line))
        bscr.append(s)
        bhow.append(h)
    broad["script"] = bscr
    broad["map_how"] = bhow
    broad["script_exists"] = [bool(s) and (BT / s).exists() for s in bscr]
    bsups = [supply_of(s) if ex else {} for s, ex in zip(broad.script, broad.script_exists)]
    broad["n_artefacts"] = [len(s) for s in bsups]
    broad["in_supply"] = [bool(s) and int(k) in set(s.values())
                          for s, k in zip(bsups, broad.K)]
    P(f"  C_BROAD mapped to an on-disk script: {int(broad.script_exists.sum()):,} of "
      f"{len(broad):,}; with artefacts {int((broad.n_artefacts > 0).sum()):,}  "
      f"[{time.time() - t0:.0f}s]")
    P("")

    def frame_for(cs):
        if cs == "C_STRICT":
            return fr.copy(), sups
        if cs == "C_ADJ":
            m = fr.verdict.astype(bool).values
            return fr[m].copy(), [s for s, k in zip(sups, m) if k]
        return broad.copy(), bsups

    rows, per_claim = [], []
    for cs in CLAIMSETS:
        sub, ss = frame_for(cs)
        for rule in RULES:
            ks, whichs = [], []
            for (_, r), sp in zip(sub.iterrows(), ss):
                kk, w = k_script(rule, float(r.K), r.get("noun", None), sp)
                ks.append(kk if kk is not None else np.nan)
                whichs.append(w)
            ks = np.array(ks, float)
            kt = sub.K.values.astype(float)
            rec = np.isfinite(ks)
            exact = rec & (ks == kt)
            over = rec & (kt > ks)
            under = rec & (kt < ks)
            ratio = np.where(rec & (ks > 0), kt / np.maximum(ks, 1e-9), np.nan)
            rows.append(dict(
                rule=rule, claim_set=cs, n=len(sub),
                n_mapped=int(sub.script_exists.sum()),
                n_measurable=int((sub.n_artefacts > 0).sum()),
                n_recovered=int(rec.sum()),
                exact=int(exact.sum()), over=int(over.sum()), under=int(under.sum()),
                share_exact=float(exact.sum() / max(rec.sum(), 1)),
                share_over=float(over.sum() / max(rec.sum(), 1)),
                share_under=float(under.sum() / max(rec.sum(), 1)),
                median_ratio=float(np.nanmedian(ratio)) if rec.any() else np.nan,
                p10_ratio=float(np.nanquantile(ratio, 0.10)) if rec.any() else np.nan,
                p90_ratio=float(np.nanquantile(ratio, 0.90)) if rec.any() else np.nan,
                in_supply=int(sub.in_supply.sum()),
                share_in_supply=float(sub.in_supply.mean()) if len(sub) else np.nan))
            if cs == CS_HEAD:
                for (_, r), kk, w in zip(sub.iterrows(), ks, whichs):
                    per_claim.append(dict(rule=rule, cid=int(r.cid), file=r.file,
                                          line=int(r.line_now),
                                          script=r.script, gap=float(r.gap),
                                          K_text=float(r.K), noun=r.get("noun", None),
                                          K_script=kk, artefact=w,
                                          in_supply=bool(r.in_supply),
                                          verdict=bool(r.verdict), text=str(r.text)[:200]))
    gr = pd.DataFrame(rows)
    dump(gr, "grid")
    pc = pd.DataFrame(per_claim)
    dump(pc, "perclaim")
    P(f"    {'rule':<10s} {'claims':<9s} {'n':>5s} {'mapped':>7s} {'meas':>5s} {'recov':>6s} "
      f"{'exact':>6s} {'OVER':>5s} {'UNDER':>6s} {'medK_t/K_s':>11s} {'p10':>7s} {'p90':>8s} "
      f"{'inSupply':>9s}")
    for _, r in gr.iterrows():
        P(f"    {r['rule']:<10s} {r['claim_set']:<9s} {r['n']:>5d} {r['n_mapped']:>7d} "
          f"{r['n_measurable']:>5d} {r['n_recovered']:>6d} {r['exact']:>6d} {r['over']:>5d} "
          f"{r['under']:>6d} {r['median_ratio']:>11.3f} {r['p10_ratio']:>7.3f} "
          f"{r['p90_ratio']:>8.3f} {r['share_in_supply']:>9.4f}")
    P("")
    hd = gr[(gr.rule == RULE_HEAD) & (gr.claim_set == CS_HEAD)].iloc[0]
    P(f"  HEADLINE ({RULE_HEAD} x {CS_HEAD}): of {hd['n_recovered']} claims whose referent the")
    P(f"  noun rule IDENTIFIES, {hd['exact']} agree with the script "
      f"({hd['share_exact']:.4f}), {hd['over']} OVERCOUNT ({hd['share_over']:.4f}) and "
      f"{hd['under']} UNDERCOUNT ({hd['share_under']:.4f}).")
    gen = gr[(gr.rule == "R_NEAREST") & (gr.claim_set == CS_HEAD)].iloc[0]
    P(f"  MOST GENEROUS (R_NEAREST x {CS_HEAD}): {gen['exact']} of {gen['n_recovered']} "
      f"({gen['share_exact']:.4f}) — an UPPER bound on how often the text is right.")
    ub = gr[(gr.rule == "R_MAXART") & (gr.claim_set == CS_HEAD)].iloc[0]
    P(f"  UPPER-BOUND SUPPLY (R_MAXART x {CS_HEAD}): {ub['over']} of {ub['n_recovered']} "
      f"claims quote MORE units than their script's LARGEST table has rows.")
    P("")

    # direction detail on the headline cell
    h = pc[pc.rule == RULE_HEAD].dropna(subset=["K_script"])
    if len(h):
        P("  DIRECTION, headline cell, by the size of the error:")
        rr = h.K_text / h.K_script.clip(lower=1e-9)
        for lo, hi, nm in ((0, 0.1, "under by >10x"), (0.1, 0.5, "under 2-10x"),
                           (0.5, 0.999, "under <2x"), (0.999, 1.001, "EXACT"),
                           (1.001, 2.0, "over <2x"), (2.0, 10.0, "over 2-10x"),
                           (10.0, 1e18, "over by >10x")):
            n_ = int(((rr > lo) & (rr <= hi)).sum())
            P(f"    {nm:<15s} {n_:>4d}  ({n_ / max(len(h), 1):.4f})")
        P(f"  the noun rule's own artefact choice, top 8: "
          f"{dict(h.artefact.value_counts().head(8))}")
    P("")

    # ------------------------------------------------------------------ ARM D: consequence
    P("-" * 100)
    P("ARM D — THE CONSEQUENCE.  Re-adjudicate 1210's frame at its own 2-SE bar with K_SCRIPT")
    P("in place of K_TEXT.  sigma_d is MEASURED on this tape below; the flips are printed after.")
    P("-" * 100)

    u = load_universe()
    b = load_universe(broad=True)
    s_px, n_bad, n_meta = load_small()
    PAN = {}
    for nm, px in (("U56", u), ("B136", b), ("SMALL", s_px)):
        PAN[nm] = Panel(nm, px)
        P(f"  {nm:<6s} {px.shape[0]:,} rows x {px.shape[1]} cols   "
          f"{px.index[0].date()} -> {px.index[-1].date()}  warm {PAN[nm].warm.sum():,}  "
          f"IS {PAN[nm].ins.sum():,}  OOS {PAN[nm].oos.sum():,}")
    P(f"  SMALL exclusion: {n_bad} of {n_meta} names dropped on max_1d_move >= 1.0 (rule 9).")
    P("")

    pu = PAN["U56"]
    a = ANCHORS["A"]
    r_anchor = book(pu, a["N"], a["H"], a["GROSS"], a["CADENCE"])
    W = build(-pu.sc, pu.elig, pu.priced, pu.reb["W"], a["N"], a["H"], pu.T, pu.K, a["GROSS"])
    eng = backtest(pu.px, pd.DataFrame(W, index=pu.idx, columns=pu.px.columns),
                   cost_bps=COST, freq="W")["returns"].values
    g4 = float(np.abs(eng[pu.warm] - r_anchor[pu.warm]).max())
    gate("G4", "fast runner == engine.backtest (U56 W/H126/N=20)", g4, g4 < 1e-12)

    mA = blocks_m(r_anchor, pu.warm, pu.ins, pu.oos)
    g5 = max(abs(mA["CAGR"] - A1101_TRIPLE[0]), abs(mA["Sharpe"] - A1101_TRIPLE[1]),
             abs(mA["MaxDD"] - A1101_TRIPLE[2]))
    gate("G5", "CROSS-RUN 1101's committed U56 anchor-A triple", g5, g5 < 5e-3)

    lb = backtest(pu.px, rules_v2_weights(pu.px), cost_bps=COST, freq="W")["returns"]
    _, _, ldd = fmet(lb.values[pu.warm])
    g6 = abs(ldd - LIVE_MAXDD_COMMITTED)
    gate("G6", "live RULES v2 U56 MaxDD == committed -12.05%", g6, g6 < 5e-4)

    spy_m = blocks_m(pu.spy, pu.warm, pu.ins, pu.oos)
    g7 = max(abs(spy_m["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
             abs(spy_m["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(spy_m["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gate("G7", "SPY OOS triple == committed (1161's bar 5e-3)", g7, g7 < 5e-3)

    cl2 = harvest()
    g8 = float(0.0 if cl2.drop(columns=["text"]).equals(cl.drop(columns=["text"])) else 1.0)
    gate("G8", "harvest is deterministic (re-run identical)", g8, g8 == 0.0)

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
    P(f"  built {nb:,} DISTINCT books over {len(books):,} slots  [{time.time() - t0:.0f}s]")

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
                            rr_ = R[mo, j]
                            c, sh, dd = fmet(rr_)
                            picks.append(dict(pool="FOLD", panel=pn, anchor=an, ladder=lad,
                                              window=wn, fold=y, chooser=ch,
                                              rung=str(rungs[j]), oos_sharpe=sh,
                                              oos_cagr=c, oos_dd=dd))
    pk = pd.DataFrame(picks)
    dump(pk, "picks")

    def diff_pool(pool, a_ch, b_ch):
        keys = ["panel", "anchor", "ladder", "window", "fold"]
        s = pk[pk.pool == pool]
        A = s[s.chooser == a_ch].set_index(keys)["oos_sharpe"]
        B = s[s.chooser == b_ch].set_index(keys)["oos_sharpe"]
        return (A - B).dropna()

    pool_cell = np.concatenate([diff_pool("CELL", a_, b_).values for a_, b_ in PAIRS])
    pool_fold = np.concatenate([diff_pool("FOLD", a_, b_).values for a_, b_ in PAIRS])
    SIG_CELL = float(pool_cell.std(ddof=1))
    SIG_FOLD = float(pool_fold.std(ddof=1))
    P(f"  sigma_CELL = {SIG_CELL:.4f} over {len(pool_cell):,} paired picks   "
      f"sigma_FOLD = {SIG_FOLD:.4f} over {len(pool_fold):,}")
    g9 = abs(SIG_CELL - A1210_SIGCELL)
    gate("G9", "sigma_CELL reproduces 1210's committed 0.1176", g9, g9 < 5e-4)

    dself = diff_pool("CELL", CHOOSERS[0], CHOOSERS[0])
    g10 = float(np.abs(dself.values).max()) if len(dself) else 1.0
    gate("G10", "degenerate pair (chooser vs itself) is EXACTLY zero", g10, g10 == 0.0)

    def resolved(gapv, K, sig):
        K = np.maximum(np.asarray(K, float), 1.0)
        return np.abs(np.asarray(gapv, float)) >= 2.0 * sig / np.sqrt(K)

    P("")
    P("  1210's own headline, reproduced on the frozen frame with THIS run's sigma:")
    r_text = resolved(fr.gap.values, fr.K.values, SIG_CELL)
    P(f"    resolved on K_TEXT: {int(r_text.sum())} of {len(fr)} "
      f"({r_text.mean():.4f}) against 1210's committed {A1210_RESOLVED} of {A1210_N}")
    g11 = abs(int(r_text.sum()) - A1210_RESOLVED)
    gate("G11", "1210's 80-of-165 resolution reproduces", g11, g11 <= 1)
    g12 = float((r_text != fr.resolved.values.astype(bool)).mean())
    gate("G12", "ROW-LEVEL agreement with 1210's own resolved column (share differing)",
         g12, g12 < 0.02)

    flips = []
    for rule in RULES:
        sub = pc[pc.rule == rule].dropna(subset=["K_script"])
        if not len(sub):
            continue
        rt = resolved(sub.gap.values, sub.K_text.values, SIG_CELL)
        rs = resolved(sub.gap.values, sub.K_script.values, SIG_CELL)
        for sig_nm, sig in (("sigma_CELL", SIG_CELL), ("sigma_FOLD", SIG_FOLD)):
            a_ = resolved(sub.gap.values, sub.K_text.values, sig)
            b_ = resolved(sub.gap.values, sub.K_script.values, sig)
            flips.append(dict(rule=rule, sigma=sig_nm, n=len(sub),
                              res_text=int(a_.sum()), res_script=int(b_.sum()),
                              lost=int((a_ & ~b_).sum()), gained=int((~a_ & b_).sum()),
                              flips=int((a_ != b_).sum()),
                              share_flip=float((a_ != b_).mean())))
        P(f"    {rule:<10s} n {len(sub):>4d}  resolved on TEXT {int(rt.sum()):>4d} -> on "
          f"SCRIPT {int(rs.sum()):>4d}   lost {int((rt & ~rs).sum()):>3d}  "
          f"gained {int((~rt & rs).sum()):>3d}")
    fl = pd.DataFrame(flips)
    dump(fl, "flips")
    P("  (sigma_FOLD column in flips.csv: the same test with the one-calendar-year read.)")
    P("")

    # ------------------------------------------------------------------ hand audit
    P("-" * 100)
    P(f"HAND AUDIT — {AUDIT_N} headline-cell rows drawn at random_state={AUDIT_SEED}, printed")
    P("in full so the noun rule's referent can be checked by eye and the precision stated.")
    P("-" * 100)
    aud = pc[(pc.rule == RULE_HEAD)].dropna(subset=["K_script"])
    if len(aud):
        aud = aud.sample(min(AUDIT_N, len(aud)), random_state=AUDIT_SEED).sort_values("file")
        dump(aud, "audit")
        for i, (_, r) in enumerate(aud.iterrows(), 1):
            P(f"  [{i:>2d}] {r['file']}:{int(r['line'])}  noun={str(r['noun']):<12s} "
              f"K_text={int(r['K_text']):<6d} K_script={int(r['K_script']):<6d} "
              f"({r['artefact']})  gap={r['gap']:.4f}")
            P(f"       script: {r['script']}")
            P(f"       ...{r['text'][:170]}...")
    P("")

    # ------------------------------------------------------------------ ARM E: rule 8
    P("-" * 100)
    P("ARM E — PROTOCOL RULE 8.  Every chooser picks on 2009-2016 ALONE; 2017-2026 read ONCE.")
    P("-" * 100)
    cell = pk[(pk.pool == "CELL") & (pk.window == "W09")]
    wf = cell.groupby("chooser").agg(n=("oos_sharpe", "size"),
                                     OOS_Sharpe=("oos_sharpe", "mean"),
                                     OOS_CAGR=("oos_cagr", "mean"),
                                     OOS_MaxDD=("oos_dd", "mean")).reset_index()
    base_rows, BASE = [], {}
    for pn in PANELS:
        pan = PAN[pn]
        rb = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        mb = blocks_m(rb, pan.warm, pan.ins, pan.oos)
        ms = blocks_m(pan.spy, pan.warm, pan.ins, pan.oos)
        BASE[pn] = (mb, ms)
        base_rows.append(dict(panel=pn, who="RULES v2 (live)", OOS_CAGR=mb["OOS_CAGR"],
                              OOS_Sharpe=mb["OOS_Sharpe"], OOS_MaxDD=mb["OOS_MaxDD"],
                              H1=mb["H1"], H2=mb["H2"], CAGR=mb["CAGR"], Sharpe=mb["Sharpe"],
                              MaxDD=mb["MaxDD"]))
        base_rows.append(dict(panel=pn, who="SPY", OOS_CAGR=ms["OOS_CAGR"],
                              OOS_Sharpe=ms["OOS_Sharpe"], OOS_MaxDD=ms["OOS_MaxDD"],
                              H1=ms["H1"], H2=ms["H2"], CAGR=ms["CAGR"], Sharpe=ms["Sharpe"],
                              MaxDD=ms["MaxDD"]))
    bs = pd.DataFrame(base_rows)
    dump(pd.concat([wf.assign(panel="ALL", who=wf.chooser)[
        ["panel", "who", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]], bs], ignore_index=True),
        "walkforward")
    P(f"    {'who':<26s} {'n':>4s} {'OOS CAGR':>9s} {'OOS Sharpe':>11s} {'OOS MaxDD':>10s}")
    for _, r in wf.iterrows():
        P(f"    {r['chooser']:<26s} {r['n']:>4d} {r['OOS_CAGR']:>9.2%} "
          f"{r['OOS_Sharpe']:>11.4f} {r['OOS_MaxDD']:>10.2%}")
    for _, r in bs.iterrows():
        P(f"    {r['panel'] + ' ' + r['who']:<26s} {'':>4s} {r['OOS_CAGR']:>9.2%} "
          f"{r['OOS_Sharpe']:>11.4f} {r['OOS_MaxDD']:>10.2%}")
    P("")
    P("  THIS RUN'S OWN OBJECT UNDER RULE 8.  The count census has no tradable parameter, so")
    P("  the honest walk-forward of the DIAL is: choose the recovery rule on the claims that")
    P("  existed at the IS boundary and read the rest ONCE.  Committed rows carry dates, so")
    P("  the split is by the row's own DATE: claims dated on or before 2026-09-10 choose the")
    P("  rule, claims after it are read once.")
    DATE_RE = re.compile(r"(20\d\d-\d\d-\d\d)")
    dts = []
    for _, r in fr.iterrows():
        L = lines_of(ROOT / "research" / str(r.file))
        line = L[int(r.line_now) - 1] if r.line_now > 0 else ""
        m = DATE_RE.search(line)
        dts.append(m.group(1) if m else None)
    fr["row_date"] = dts
    is_m = fr.row_date.notna() & (fr.row_date <= "2026-09-10")
    oos_m = fr.row_date.notna() & (fr.row_date > "2026-09-10")
    P(f"    dated rows {int(fr.row_date.notna().sum())} of {len(fr)}; "
      f"IS (<= 2026-09-10) {int(is_m.sum())}, OOS (> 2026-09-10) {int(oos_m.sum())}")
    wf_rows = []
    for rule in RULES:
        sub = pc[pc.rule == rule].set_index("cid")
        for nm, msk in (("IS", is_m), ("OOS", oos_m)):
            idx = [int(c) for c in fr.cid[msk]]
            got = sub.reindex(idx).dropna(subset=["K_script"])
            if not len(got):
                wf_rows.append(dict(rule=rule, window=nm, n=0, exact=0, share_exact=np.nan,
                                    over=0, under=0))
                continue
            ex = (got.K_text == got.K_script)
            wf_rows.append(dict(rule=rule, window=nm, n=len(got), exact=int(ex.sum()),
                                share_exact=float(ex.mean()),
                                over=int((got.K_text > got.K_script).sum()),
                                under=int((got.K_text < got.K_script).sum())))
    wfr = pd.DataFrame(wf_rows)
    dump(wfr, "rule8")
    P(f"    {'rule':<10s} {'window':<5s} {'n':>5s} {'exact':>6s} {'share':>7s} {'over':>5s} "
      f"{'under':>6s}")
    for _, r in wfr.iterrows():
        sh = f"{r['share_exact']:.4f}" if np.isfinite(r["share_exact"]) else "   n/a"
        P(f"    {r['rule']:<10s} {r['window']:<5s} {r['n']:>5d} {r['exact']:>6d} {sh:>7s} "
          f"{r['over']:>5d} {r['under']:>6d}")
    isb = wfr[wfr.window == "IS"].dropna(subset=["share_exact"])
    if len(isb):
        pick = isb.sort_values(["share_exact", "rule"], ascending=[False, True]).iloc[0]["rule"]
        oosb = wfr[(wfr.window == "OOS") & (wfr.rule == pick)]
        P(f"    IS-chosen recovery rule (highest agreement on pre-split claims): {pick}")
        if len(oosb) and np.isfinite(oosb.iloc[0]["share_exact"]):
            P(f"    read ONCE on the post-split claims: {int(oosb.iloc[0]['exact'])} of "
              f"{int(oosb.iloc[0]['n'])} exact ({oosb.iloc[0]['share_exact']:.4f}), "
              f"over {int(oosb.iloc[0]['over'])}, under {int(oosb.iloc[0]['under'])}")
        else:
            P("    post-split claims: none recovered — reported, not imputed.")
    P("")

    # ------------------------------------------------------------------ ARM F: KEEP paths
    P("-" * 100)
    P("ARM F — BOTH KEEP PATHS (PROTOCOL rule 4) on every distinct book this run built.")
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
                              H1=m["H1"], H2=m["H2"],
                              OOS_Sharpe=m["OOS_Sharpe"], OOS_CAGR=m["OOS_CAGR"],
                              OOS_MaxDD=m["OOS_MaxDD"],
                              pass_4a=all(f4a.values()), pass_4b_full=all(f4b.values()),
                              pass_4b_oos=all(f4bo.values()),
                              pass_4b_both=all(f4b.values()) and all(f4bo.values()),
                              **f4a, **f4b, **f4bo))
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
    P("  These are 1101's rung books, PRIOR ART: recorded, not promoted.  A count census")
    P("  cannot pass a KEEP path on its own.")
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
    P(f"  KILL (capital) — a count census is not a trading rule; 4a {int(kp.pass_4a.sum())} of "
      f"{len(kp)}, 4b full+OOS {int(kp.pass_4b_both.sum())} of {len(kp)} on prior-art books.")
    P(f"  ANSWERED: under the headline {RULE_HEAD} x {CS_HEAD}, {hd['exact']} of "
      f"{hd['n_recovered']} ({hd['share_exact']:.4f}) committed count cues agree with the "
      f"script that produced the row; {hd['over']} overcount, {hd['under']} undercount.")
    P(f"  Rule-free containment: {int(meas.in_supply.sum())} of {len(meas)} "
      f"({meas.in_supply.mean() if len(meas) else np.nan:.4f}) quoted counts appear among ANY "
      f"of their script's own artefact row counts.")
    P(f"  [{time.time() - t0:.0f}s]")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
