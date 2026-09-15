#!/usr/bin/env python3
"""Idea 984 (lane C, 2026-09-15) -- should every committed 4b LEG claim carry the CADENCE it was
MEASURED at?

THE QUESTION (queue, 2026-09-15, filed by idea 981)
  Idea 981 found idea 968's "L_DD binds on 89.2% of quarterly phase-books" and idea 976's
  "L4_DD binds on 36 of 36 rule-8 picks" are reproduced EXACTLY on the M/Q half of the
  D/W/M/Q ladder and collapse to 5 of 18 on the D/W half -- both correct, both LOCAL.  The
  queue asks: census the record's committed leg-binding and "4b is a drawdown test" claims for
  how many state a cadence AT ALL, and re-score those that do not against the D/W half of the
  ladder.

WHY IT MATTERS FOR CAPITAL
  The record's DD-heavy reading of 4b is what tells the next twenty ideas to spend their effort
  on drawdown control rather than return.  If that reading is an artefact of the M/Q grids the
  record happens to run most, and the claims carrying it do not say which cadence they were
  measured at, then a reader cannot tell a universal fact from a local one -- and will aim
  research, and eventually capital, at the wrong leg.  This run does not ask whether the DD
  reading is TRUE (981 answered that: it is a cadence object).  It asks how much of the
  committed record is stated in a form that survives being read at a different cadence, and
  prices the reporting clause 981 proposed.

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL 4: max 2 tuned parameters)
  TUNED 1  CLAIM SET, 3 variants, every one reported and none selected:
           STRICT  a sentence in LEADERBOARD.md / CHANGELOG.md naming an explicit leg token
                   (L1_H1 / L2_H2 / L3_OOS / L4_DD / L5_CAGR and their published aliases) AND a
                   binding verb
           WIDE    STRICT plus prose leg forms ("DD cap", "CAGR floor", "drawdown test") in a
                   sentence whose row/paragraph mentions 4b
           FILES   WIDE plus every committed research/backtests/*.result.md and *.memo.md
  TUNED 2  LADDER, 3 variants, every one reported and none selected:
           FINE2    D / W      (the queue's re-score half)
           COARSE2  M / Q      (the half the record was measured on)
           CORE4    D / W / M / Q
  REPORTED AXES (nothing fitted on them, every point published): cadence-detection context
  (SENTENCE vs ROW), panel U56 / B136 / SMALL, book TOP05 / TOP10 / TOP20 / EWELIG / BAND03,
  gross CORE 0.75 / EXT 1.00, phase within cadence, cost rung 0 / 5 / 10 / 25 / 50 bps,
  statistic type S_RATE / S_ONLY / S_MODAL / S_DDTEST.

PRE-REGISTERED BARS (fixed before any number below was read; both directions reported)
  H_SILENT  the clause is NOT VACUOUS iff >= 0.50 of committed leg-binding claims state no
            cadence at all.
  H_MOVE    the clause is CONSEQUENTIAL iff, among cadence-silent claims this run can map to a
            computable statistic, >= 0.25 do not survive the D/W half (rate types: the
            statistic moves by more than 0.10; modal types: the named leg is not modal on D/W).
  H_GAP     the under-determination is LARGE iff the claim-weighted mean |M/Q value - D/W
            value| of the mapped statistics is >= 0.20.
  H_DD      the silence is concentrated on the DRAWDOWN leg iff >= 0.50 of cadence-silent
            mapped claims name L4_DD.
  H_RULE8   (rule 8, REQUIRED) the halves genuinely disagree OUT OF SAMPLE iff, on this run's
            own walk-forward picks, (DD-bind share on M/Q picks) - (DD-bind share on D/W picks)
            is >= 0.40.
  DECISION RULE, fixed in advance:
      H_SILENT and (H_MOVE or H_GAP) and H_RULE8 -> the cadence clause is CONSEQUENTIAL;
                                                    KEEP it as a PROTOCOL rule 4 reporting
                                                    clause (proposed, not applied -- rule 6)
      H_SILENT and not (H_MOVE or H_GAP)         -> the record is silent but the silence costs
                                                    nothing -> KILL the clause
      not H_SILENT                               -> the record already states its cadence
                                                    -> KILL the clause as redundant

GATES (all printed before any result number)
  G0  `offset_mask(idx, per, 0)` == `engine.rebalance_mask(idx, per)` on D / W / M / Q
  G1  the fast `Ctx` runner == `engine.backtest` on returns AND turnover, post warm-up, D and M
  G2  BAND03 @ 0.75 == `baseline.rules_v2_weights` elementwise
  G3  CROSS-RUN: idea 981's committed 13,500-row `.grid.csv.gz` reproduced by this run's own
      independent rebuild on every shared numeric column, with 0 4b-verdict flips
  G4  CROSS-RUN: idea 981's published pooled `L4_DD` fail rates 0.633 / 0.647 / 0.832 / 0.927
      at D / W / M / Q, 10 bps, recomputed from this run's own grid
  G5  MATCHED GROSS: the target weight matrix is identical across all four cadences
  G6  determinism: one cell rebuilt from scratch, max|d| over returns and turnover
  G7  every rule-8 chooser is IS-ONLY -- picks invariant to permuted OOS columns
  G8  HARVESTER RECALL: the two claims the queue names by hand -- idea 968's "89.2%" quarterly
      claim and idea 976's "36 of 36" rule-8 claim -- are both found by the harvester and both
      classified, and no claim is counted twice (source line + offset is unique)

PROTOCOL: 10 bps primary (all five rungs reported), decided at close t / applied t+1, warm-up
260 days, IS 2009-2016 / OOS 2017-2026 read once, no shorting, no leverage beyond the published
gross.  Nothing in RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py is modified.

SURVIVORSHIP (rule 9): U56, B136 and SMALL are CURRENT-CONSTITUENT lists (SMALL additionally
drops every ticker with `max_1d_move` >= 1.0 per `data/small_meta.csv`), so every CAGR and
drawdown LEVEL below is optimistic and both 4b bars are easier here than on a point-in-time
panel.  A survivor panel understates drawdown, so every `L4_DD` fail rate is a LOWER bound.
The object this run measures is a DIFFERENCE between two halves of the SAME ladder on the SAME
names and the SAME tape -- only the rebalance schedule moves -- so it is very nearly immune to
survivorship.  The rule-8 4b levels are read against SPY, which is not survivorship-inflated.
Stated, not hidden.
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
from baseline import load_universe, rules_v2_weights, band_state, score   # noqa: E402
from engine import backtest, rebalance_mask                               # noqa: E402

BAND0, VOLCAP, WARM = 0.03, 0.60, 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
HEAD_COST = 10.0
GROSSES = {"CORE": 0.75, "EXT": 1.00}
CADENCES = {"D": 1, "W": 5, "M": 21, "Q": 63}
CADORDER = ["D", "W", "M", "Q"]
LADDERS = {"FINE2": ["D", "W"], "COARSE2": ["M", "Q"], "CORE4": ["D", "W", "M", "Q"]}
RUNGS = [0.0, 5.0, 10.0, 25.0, 50.0]
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
LEGNAME = {"H1": "L1_H1", "H2": "L2_H2", "OOS": "L3_OOS", "DD": "L4_DD", "CAGR": "L5_CAGR"}
SILENT_BAR, MOVE_BAR, GAP_BAR, DD_BAR, RULE8_BAR = 0.50, 0.25, 0.20, 0.50, 0.40
MOVE_TOL = 0.10          # a rate-type claim "survives" the other half within this much
REF981 = OUT / ("2026-09-15_is-4b-a-DRAWDOWN-TEST-on-EVERY-panel-and-not-just-the-QUARTERLY-"
                "grid_B.grid.csv.gz")
REF981_PUB = {"D": 0.633, "W": 0.647, "M": 0.832, "Q": 0.927}   # 981's published pooled rates
SMOKE = bool(int(os.environ.get("IDEA984_SMOKE", "0")))
LINES: list[str] = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix, gz=False):
    p = OUT / (f"{STEM}.{suffix}.csv.gz" if gz else f"{STEM}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ==========================================================================================
# (1) cadence / phase machinery -- copied VERBATIM from ideas 938 / 942 / 962 / 964 / 976 / 981
#     so this run NESTS the record and G3 is an EXACT cross-run reproduction.
# ==========================================================================================
def offset_mask(idx, per, d):
    key = pd.Series(idx.to_period(per), index=idx)
    last = np.flatnonzero((key != key.shift(-1)).values)
    first = np.concatenate([[0], last[:-1] + 1])
    pick = np.maximum(last - d, first)
    out = pd.Series(False, index=idx)
    out.iloc[np.unique(pick)] = True
    return out, int((last - d < first).sum())


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
        return (held * self.rets).sum(axis=1), turn, held.sum(axis=1)


def shift1(W, idx):
    return W.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values


def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def maxdd(r):
    eq = np.cumprod(1.0 + r)
    return float((eq / np.maximum.accumulate(eq) - 1).min())


def mets(r):
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    h = len(r) // 2
    return dict(CAGR=float(eq[-1] ** (1 / yrs) - 1) if yrs > 0 else np.nan,
                Sharpe=sharpe(r), MaxDD=maxdd(r), H1=sharpe(r[:h]), H2=sharpe(r[h:]))


def legs_rec(row):
    return dict(H1=row["H1"] > row["spy_H1"], H2=row["H2"] > row["spy_H2"],
                OOS=row["OOS_Sharpe"] > row["spy_OOS_Sharpe"],
                DD=abs(row["OOS_MaxDD"]) <= 0.60 * abs(row["spy_MaxDD"]),
                CAGR=row["OOS_CAGR"] >= 0.70 * row["spy_CAGR"])


def legs_is(row):
    return dict(H1=row["IS_H1"] > row["spy_IS_H1"], H2=row["IS_H2"] > row["spy_IS_H2"],
                OOS=row["IS_Sharpe"] > row["spy_IS_Sharpe"],
                DD=abs(row["IS_MaxDD"]) <= 0.60 * abs(row["spy_IS_MaxDD"]),
                CAGR=row["IS_CAGR"] >= 0.70 * row["spy_IS_CAGR"])


def slacks(row):
    return dict(
        H1=(row["H1"] - row["spy_H1"]) / abs(row["spy_H1"]),
        H2=(row["H2"] - row["spy_H2"]) / abs(row["spy_H2"]),
        OOS=(row["OOS_Sharpe"] - row["spy_OOS_Sharpe"]) / abs(row["spy_OOS_Sharpe"]),
        DD=(0.60 * abs(row["spy_MaxDD"]) - abs(row["OOS_MaxDD"])) / (0.60 * abs(row["spy_MaxDD"])),
        CAGR=(row["OOS_CAGR"] - 0.70 * row["spy_CAGR"]) / abs(0.70 * row["spy_CAGR"]),
    )


def failstr(lg):
    f = [LEGNAME[k] for k in LEGS if not lg[k]]
    return ",".join(f) if f else "-"


# ==========================================================================================
# (2) THE BOOK SET -- 942 / 962 / 964 / 976 / 981's five books verbatim
# ==========================================================================================
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


CHOOSERS = ["C_CAGR", "C_SHARPE", "C_ISLEGS"]


def _argmax(v, tiebreak=None):
    v = np.asarray(v, float)
    if not np.isfinite(v).any():
        return None
    best = np.nanmax(v)
    cand = np.flatnonzero(np.isclose(v, best, rtol=0, atol=0))
    if len(cand) > 1 and tiebreak is not None:
        t = np.asarray(tiebreak, float)[cand]
        cand = cand[np.flatnonzero(t == np.nanmax(t))]
    return int(cand[0])


def choose(name, sub):
    isc, iss = sub.IS_CAGR.values, sub.IS_Sharpe.values
    if name == "C_CAGR":
        return _argmax(isc, iss)
    if name == "C_SHARPE":
        return _argmax(iss, isc)
    if name == "C_ISLEGS":
        return _argmax(sub.IS_legs_passed.values, iss)
    raise KeyError(name)


# ==========================================================================================
# (3) THE HARVESTER -- committed leg-binding claims out of the record's own prose
# ==========================================================================================
LEG_TOK = {           # STRICT: explicit leg tokens as the record writes them
    "DD":   r"L4_DD(?:cap)?|L_DD\b|\bLDD\b",
    "CAGR": r"L5_CAGR(?:floor)?|L_CAGR\b",
    "H1":   r"L1_H1|L_H1\b",
    "H2":   r"L2_H2|L_H2\b",
    "OOS":  r"L3_OOS|L_OOS\b",
}
LEG_PROSE = {         # WIDE: prose leg names, only inside a 4b context
    "DD":   r"\bDD[ -]cap\b|\bDDcap\b|drawdown cap|drawdown leg|\bDD leg\b|drawdown test",
    "CAGR": r"CAGR floor|CAGR leg",
    "H1":   r"\bH1 leg\b", "H2": r"\bH2 leg\b",
    "OOS":  r"OOS Sharpe leg",
}
VERB = (r"\bbinds?\b|\bbinding\b|\bbinder\b|only failed leg|only fail\b|\bmodal\b|fail rate|"
        r"\btops\b|\balone\b|\bsole\b|drawdown test|most-failed|\btightest\b|whole test")
CAD_TOK = (r"\bdaily\b|\bweekly\b|\bmonthly\b|\bquarterly\b|\bD/W/M/Q\b|\bM/Q\b|\bD/W\b|"
           r"\bW/M/Q\b|\bW->M\b|W→M|\bDOM21\b|\bDOW5\b|\bon M\b|\bon Q\b|\bon W\b|\bon D\b|"
           r"freq=\"?[DWMQ]|\bM and Q\b|\bD and W\b|\bcadence [DWMQ]\b")
NUM_PCT = r"(\d{1,3}(?:\.\d+)?)\s?%"
NUM_OFN = r"(\d{1,6})\s+of\s+(\d{1,6})"
NUM_DEC = r"\b0\.(\d{2,4})\b"


def sentences(text):
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9*_`(])", text)
    return [p.strip() for p in parts if len(p.strip()) >= 15]


def blocks_from(path, rel):
    """(rel_path, line_no, block_index, text) for every markdown table cell / paragraph."""
    out = []
    for ln, line in enumerate(open(path, encoding="utf-8"), 1):
        line = line.rstrip("\n")
        chunks = line.split("|") if line.lstrip().startswith("|") else [line]
        for bi, c in enumerate(chunks):
            c = c.strip()
            if len(c) >= 15:
                out.append((rel, ln, bi, c))
    return out


def classify(sent, block):
    """-> (leg, source_kind, stat_type) or None.  source_kind STRICT / WIDE."""
    if not re.search(VERB, sent, re.I):
        return None
    for lg, pat in LEG_TOK.items():
        if re.search(pat, sent):
            return lg, "STRICT", stat_type(sent)
    if re.search(r"\b4b\b", sent, re.I) or re.search(r"\b4b\b", block, re.I):
        for lg, pat in LEG_PROSE.items():
            if re.search(pat, sent, re.I):
                return lg, "WIDE", stat_type(sent)
    return None


def stat_type(sent):
    s = sent.lower()
    if "drawdown test" in s:
        return "S_DDTEST"
    if "only failed leg" in s or "only fail" in s or re.search(r"\balone\b|\bsole\b", s):
        return "S_ONLY"
    if re.search(r"\bmodal\b|most-failed|\btops\b|\btightest\b", s):
        return "S_MODAL"
    if re.search(r"fail rate|\bbinds?\b|\bbinding\b|\bbinder\b", s):
        return "S_RATE"
    return "S_MODAL"


def published_number(sent):
    """The first number the sentence publishes, normalised to a rate in [0,1] when possible."""
    m = re.search(NUM_OFN, sent)
    if m and int(m.group(2)) > 0:
        return float(m.group(1)) / float(m.group(2)), f"{m.group(1)} of {m.group(2)}"
    m = re.search(NUM_PCT, sent)
    if m:
        v = float(m.group(1)) / 100.0
        return (v, m.group(0)) if 0.0 <= v <= 1.0 else (np.nan, m.group(0))
    m = re.search(NUM_DEC, sent)
    if m:
        return float("0." + m.group(1)), m.group(0)
    return np.nan, ""


def eta2(df, factor, y):
    v = df[y].astype(float)
    tot = float(((v - v.mean()) ** 2).sum())
    if tot <= 0:
        return np.nan
    bet = 0.0
    for _, g in df.groupby(factor):
        bet += len(g) * (float(g[y].astype(float).mean()) - float(v.mean())) ** 2
    return float(bet / tot)


# ==========================================================================================
def stat_value(g10, cads, leg, typ):
    """The statistic a claim of this (leg, type) asserts, measured on the given cadences.
    Cadence-balanced: each cadence contributes equally (the ladder has 1/5/21/63 phases)."""
    vals = []
    for cad in cads:
        s = g10[g10.cadence == cad]
        if not len(s):
            continue
        if typ in ("S_RATE", "S_DDTEST"):
            vals.append(float((~s["leg_" + leg]).mean()))
        elif typ == "S_ONLY":
            vals.append(float((s.only_fail == LEGNAME[leg]).mean()))
        elif typ == "S_MODAL":
            rates = {k: float((~s["leg_" + k]).mean()) for k in LEGS}
            vals.append(1.0 if max(rates, key=rates.get) == leg else 0.0)
    return float(np.mean(vals)) if vals else np.nan


def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 984 (lane C) -- should every committed 4b LEG claim carry the CADENCE it was "
      "MEASURED at?")
    P(f"  run {pd.Timestamp.utcnow():%Y-%m-%d %H:%M UTC}   PROTOCOL 10 bps / t+1 / warm-up {WARM}")
    P(f"  ladder {CADORDER} at MATCHED GROSS {GROSSES}; phases per cadence {CADENCES}")
    P("=" * 100)

    panels = {"U56": load_universe()}
    if not SMOKE:
        panels["B136"] = load_universe(broad=True)
        sm, ndrop = load_small()
        panels["SMALL"] = sm
    else:
        ndrop = 0
    for k, v in panels.items():
        P(f"  panel {k:6s} {v.shape[1]:4d} cols  {v.index[0].date()} .. {v.index[-1].date()}  "
          f"{len(v):,} rows")
    P(f"  SMALL drops {ndrop} tickers with max_1d_move >= 1.0; SURVIVORSHIP: all panels are "
      f"CURRENT-CONSTITUENT lists (rule 9).")

    # ------------------------------------------------------------------------------ gates A
    P()
    P("=" * 100)
    P("(A) GATES -- printed before any result number")
    P("=" * 100)
    gk, gdetail = {}, []
    u = panels["U56"]
    idx = u.index

    g0 = sum(int((offset_mask(idx, per, 0)[0].values != rebalance_mask(idx, per).values).sum())
             for per in CADORDER)
    gk["G0"] = g0 == 0
    P(f"  G0 offset_mask(.,per,0) == engine.rebalance_mask on {'/'.join(CADORDER)}: "
      f"{g0} disagreeing rows  {'PASS' if gk['G0'] else 'FAIL'}")
    gdetail.append(dict(gate="G0", stat=float(g0), bar=0.0, passed=gk["G0"],
                        what="offset_mask(d=0) == engine.rebalance_mask on D/W/M/Q"))

    w75 = rules_v2_weights(u, BAND0, 0.75)
    d2 = float(np.nanmax(np.abs(w75.values - band_book(u, BAND0, 0.75).values)))
    gk["G2"] = d2 == 0.0
    P(f"  G2 BAND03@0.75 == baseline.rules_v2_weights: {d2:.3e}  {'PASS' if gk['G2'] else 'FAIL'}")
    gdetail.append(dict(gate="G2", stat=d2, bar=0.0, passed=gk["G2"],
                        what="BAND03@0.75 == baseline.rules_v2_weights elementwise"))

    sw = shift1(w75, idx)
    d1 = 0.0
    for per in ("D", "M"):
        c = Ctx(u, offset_mask(idx, per, 0)[0])
        gr, tn, _ = c.run(sw)
        eng = backtest(u, w75, cost_bps=0.0, freq=per)
        d1 = max(d1, float(np.abs(gr[WARM:] - eng["returns"].values[WARM:]).max()),
                 float(np.abs(tn[WARM:] - eng["turnover"].values[WARM:]).max()))
    gk["G1"] = d1 < 1e-12
    P(f"  G1 Ctx == engine.backtest on D and M (returns AND turnover, post warm-up): "
      f"max|d| {d1:.3e}  {'PASS' if gk['G1'] else 'FAIL'}")
    gdetail.append(dict(gate="G1", stat=d1, bar=1e-12, passed=gk["G1"],
                        what="fast Ctx runner == engine.backtest on D and M"))

    # ------------------------------------------------------------- B: the ladder x phase grid
    P()
    P("=" * 100)
    P("(B) THE LADDER -- rebuilt independently; every (panel, book, gross, cadence, phase) "
      "at 5 rungs")
    P("=" * 100)
    rows, gross_rows, det_store = [], [], {}
    cads = CADORDER if not SMOKE else ["D", "M"]
    for pname, px in panels.items():
        rets_spy = px["SPY"].pct_change().fillna(0.0).values
        isw = np.asarray(px.index <= pd.Timestamp(IS_END))
        osw = np.asarray(px.index >= pd.Timestamp(OOS_START))
        spy_full, spy_is, spy_oos = (mets(rets_spy[WARM:]), mets(rets_spy[WARM:][isw[WARM:]]),
                                     mets(rets_spy[osw]))
        shifted = {(bk, gn): shift1(BOOKS[bk](px, gv), px.index)
                   for bk in BOOKS for gn, gv in GROSSES.items()}
        for cad in cads:
            nph = CADENCES[cad] if not SMOKE else min(CADENCES[cad], 3)
            for ph in range(nph):
                m, clipped = offset_mask(px.index, cad, ph)
                ctx = Ctx(px, m)
                for bk in BOOKORDER:
                    for gn in GROSSES:
                        wt = shifted[(bk, gn)]
                        r, tu, gx = ctx.run(wt)
                        if ph == 0:
                            gross_rows.append(dict(panel=pname, book=bk, gross=gn, cadence=cad,
                                                   target_gross=float(wt[WARM:].sum(axis=1).mean()),
                                                   realised_gross=float(gx[WARM:].mean()),
                                                   turn_per_yr=float(tu[WARM:].sum() /
                                                                     (len(tu[WARM:]) / 252.0))))
                        for cb in RUNGS:
                            net = r - tu * cb / 1e4
                            f, i_, o_ = (mets(net[WARM:]), mets(net[WARM:][isw[WARM:]]),
                                         mets(net[osw]))
                            row = dict(panel=pname, book=bk, gross=gn, cadence=cad, phase=ph,
                                       cost_bps=cb, clipped=clipped,
                                       turn_per_yr=float(tu[WARM:].sum() / (len(tu[WARM:]) / 252.0)))
                            for k, v in f.items():
                                row[k] = v
                            for k, v in i_.items():
                                row["IS_" + k] = v
                            for k, v in o_.items():
                                row["OOS_" + k] = v
                            for k, v in spy_full.items():
                                row["spy_" + k] = v
                            for k, v in spy_is.items():
                                row["spy_IS_" + k] = v
                            for k, v in spy_oos.items():
                                row["spy_OOS_" + k] = v
                            lr, li, sl = legs_rec(row), legs_is(row), slacks(row)
                            for k in LEGS:
                                row["leg_" + k] = bool(lr[k])
                                row["slack_" + k] = float(sl[k])
                            row["n_fail"] = int(sum(not lr[k] for k in LEGS))
                            row["IS_legs_passed"] = int(sum(li.values()))
                            row["pass4b_REC"] = bool(all(lr.values()))
                            row["fail4b_REC"] = failstr(lr)
                            order = sorted(LEGS, key=lambda k: (sl[k], LEGS.index(k)))
                            row["tightest"] = LEGNAME[order[0]]
                            row["only_fail"] = (LEGNAME[[k for k in LEGS if not lr[k]][0]]
                                                if row["n_fail"] == 1 else "")
                            rows.append(row)
                        if ph == 0 and cad == cads[0] and bk == "BAND03" and gn == "CORE":
                            det_store[pname] = (r.copy(), tu.copy())
                del ctx
            P(f"  {pname:6s} {cad}  {nph} phases x 10 book-gross x {len(RUNGS)} rungs done "
              f"[{time.time()-t0:6.0f}s]")
    G = pd.DataFrame(rows)
    GR = pd.DataFrame(gross_rows)
    P(f"  grid {len(G):,} rows over "
      f"{len(G.groupby(['panel','book','gross','cadence','phase'])):,} phase-books")

    for pname, px in panels.items():
        b = backtest(px, rules_v2_weights(px), cost_bps=HEAD_COST, freq="W")["returns"].values
        bm = mets(b[WARM:])
        sel = G.panel == pname
        G.loc[sel, "v2_Sharpe"] = bm["Sharpe"]
        G.loc[sel, "v2_H1"] = bm["H1"]
        G.loc[sel, "v2_H2"] = bm["H2"]
        G.loc[sel, "v2_MaxDD"] = bm["MaxDD"]
    G["pass4a"] = (G.H1 > G.v2_H1) & (G.H2 > G.v2_H2) & (G.MaxDD >= G.v2_MaxDD)

    # ------------------------------------------------------------------------------ gates B
    P()
    piv = GR.pivot_table(index=["panel", "book", "gross"], columns="cadence",
                         values="target_gross")
    g5 = float(np.nanmax(piv.max(axis=1).values - piv.min(axis=1).values))
    gk["G5"] = g5 == 0.0
    P(f"  G5 MATCHED GROSS: target weight matrix identical across all {len(cads)} cadences over "
      f"{len(piv)} (panel,book,gross): max spread {g5:.3e}  {'PASS' if gk['G5'] else 'FAIL'}")
    gdetail.append(dict(gate="G5", stat=g5, bar=0.0, passed=gk["G5"],
                        what="target gross identical across the ladder"))

    g10 = G[G.cost_bps == HEAD_COST].copy()
    if REF981.exists() and not SMOKE:
        ref = pd.read_csv(REF981)
        key = ["panel", "book", "gross", "cadence", "phase", "cost_bps"]
        cmp_cols = [c for c in ref.columns if c in G.columns and
                    ref[c].dtype.kind in "fi" and c not in key]
        j = ref.merge(G, on=key, suffixes=("_ref", "_new"), how="inner")
        dmax, worst = 0.0, ""
        for c in cmp_cols:
            d = float(np.nanmax(np.abs(j[c + "_ref"].values - j[c + "_new"].values)))
            if d > dmax:
                dmax, worst = d, c
        flips = int((j["pass4b_REC_ref"].astype(bool) != j["pass4b_REC_new"].astype(bool)).sum())
        gk["G3"] = (len(j) == len(ref)) and dmax < 1e-10 and flips == 0
        P(f"  G3 CROSS-RUN idea 981's committed grid: {len(j):,} of {len(ref):,} rows matched, "
          f"max|d| {dmax:.3e} (on {worst or 'n/a'}) over {len(cmp_cols)} shared numeric cols, "
          f"{flips} 4b verdict flips  {'PASS' if gk['G3'] else 'FAIL'}")
        gdetail.append(dict(gate="G3", stat=dmax, bar=1e-10, passed=gk["G3"],
                            what=f"981's 13,500-row ladder reproduced ({len(j)} rows, {flips} flips)"))
    else:
        gk["G3"] = False
        P("  G3 SKIPPED/FAIL: idea 981's grid not found (or SMOKE)")
        gdetail.append(dict(gate="G3", stat=np.nan, bar=1e-10, passed=False, what="981 grid missing"))

    # G4 -- 981's PUBLISHED pooled L4_DD fail rates recomputed
    pub_d = 0.0
    pub_rows = []
    for cad in cads:
        s = g10[g10.cadence == cad]
        got = float((~s.leg_DD).mean())
        want = REF981_PUB.get(cad, np.nan)
        pub_rows.append(dict(cadence=cad, published=want, recomputed=got, diff=abs(got - want)))
        pub_d = max(pub_d, abs(got - want))
    gk["G4"] = pub_d <= 0.0005
    want_s = "/".join("%.3f" % REF981_PUB[c] for c in cads if c in REF981_PUB)
    got_s = "/".join("%.3f" % r["recomputed"] for r in pub_rows)
    P(f"  G4 CROSS-RUN idea 981's PUBLISHED pooled L4_DD fail rates {want_s} at "
      f"{'/'.join(cads)}: recomputed {got_s}, max|d| {pub_d:.4f}  "
      f"{'PASS' if gk['G4'] else 'FAIL'}")
    gdetail.append(dict(gate="G4", stat=pub_d, bar=0.0005, passed=gk["G4"],
                        what="981's published D/W/M/Q L4_DD fail rates recomputed"))

    pn = "U56"
    px = panels[pn]
    m, _ = offset_mask(px.index, cads[0], 0)
    c2 = Ctx(px, m)
    r2, t2, _ = c2.run(shift1(band_book(px, BAND0, 0.75), px.index))
    d6 = float(max(np.abs(r2 - det_store[pn][0]).max(), np.abs(t2 - det_store[pn][1]).max()))
    gk["G6"] = d6 == 0.0
    P(f"  G6 determinism (U56/{cads[0]}/BAND03/CORE rebuilt from scratch): {d6:.3e}  "
      f"{'PASS' if gk['G6'] else 'FAIL'}")
    gdetail.append(dict(gate="G6", stat=d6, bar=0.0, passed=gk["G6"], what="rebuild determinism"))

    # =====================================================================================
    # (C) THE CENSUS -- committed leg-binding claims, and whether they name a cadence
    # =====================================================================================
    P()
    P("=" * 100)
    P("(C) THE CENSUS -- every committed leg-binding / '4b is a drawdown test' claim")
    P("=" * 100)
    srcs = [(ROOT / "research" / "LEADERBOARD.md", "LEADERBOARD.md"),
            (ROOT / "research" / "CHANGELOG.md", "CHANGELOG.md")]
    file_srcs = sorted([p for p in (ROOT / "research" / "backtests").glob("*.md")
                        if p.name.endswith(".result.md") or ".memo" in p.name
                        or p.name.endswith("MEMO.md")])
    claims = []
    for path, rel in srcs + [(p, "backtests/" + p.name) for p in file_srcs]:
        in_files = rel.startswith("backtests/")
        for (r_, ln, bi, block) in blocks_from(path, rel):
            for si, sent in enumerate(sentences(block)):
                c = classify(sent, block)
                if c is None:
                    continue
                leg, kind, typ = c
                num, numtxt = published_number(sent)
                cad_sent = bool(re.search(CAD_TOK, sent, re.I))
                cad_row = bool(re.search(CAD_TOK, block, re.I))
                claims.append(dict(source=r_, line=ln, block=bi, sent_i=si,
                                   set_STRICT=(kind == "STRICT") and not in_files,
                                   set_WIDE=not in_files,
                                   set_FILES=True,
                                   kind=kind, leg=leg, stat_type=typ,
                                   cadence_in_sentence=cad_sent, cadence_in_row=cad_row,
                                   published_num=num, published_txt=numtxt,
                                   text=sent[:400]))
    CL = pd.DataFrame(claims).drop_duplicates(subset=["source", "line", "block", "sent_i"])
    P(f"  harvested {len(CL):,} claims  "
      f"(STRICT {int(CL.set_STRICT.sum()):,} / WIDE {int(CL.set_WIDE.sum()):,} / "
      f"FILES {int(CL.set_FILES.sum()):,})")
    P(f"  by leg: " + "  ".join(f"{LEGNAME[k]} {int((CL.leg == k).sum())}" for k in LEGS))
    P(f"  by statistic type: " +
      "  ".join(f"{t} {int((CL.stat_type == t).sum())}" for t in sorted(CL.stat_type.unique())))

    # G8 harvester recall on the two claims the queue names by hand
    hit968 = CL.text.str.contains("89.2", regex=False).any()
    hit976 = CL.text.str.contains("36 of 36", regex=False).any()
    dupes = int(len(claims) - len(CL))
    gk["G8"] = bool(hit968 and hit976 and dupes == 0)
    P(f"  G8 HARVESTER RECALL: 968's '89.2' claim found {hit968}; 976's '36 of 36' claim found "
      f"{hit976}; duplicate (source,line,block,sentence) rows {dupes}  "
      f"{'PASS' if gk['G8'] else 'FAIL'}")
    gdetail.append(dict(gate="G8", stat=float(dupes), bar=0.0, passed=gk["G8"],
                        what="queue's two named claims are both harvested; no double counting"))

    # TUNED 1: claim set x cadence-detection context (context is REPORTED, not tuned)
    P()
    P("  TUNED 1 (claim set) x REPORTED (cadence-detection context) -- share stating NO cadence:")
    cen = []
    for cs in ["STRICT", "WIDE", "FILES"]:
        sub = CL[CL["set_" + cs]]
        for ctx_ in ["SENTENCE", "ROW"]:
            col = "cadence_in_sentence" if ctx_ == "SENTENCE" else "cadence_in_row"
            cen.append(dict(claim_set=cs, context=ctx_, n=len(sub),
                            n_states_cadence=int(sub[col].sum()),
                            share_silent=float(1.0 - sub[col].mean()),
                            share_silent_DD=float(1.0 - sub[sub.leg == "DD"][col].mean())
                            if (sub.leg == "DD").any() else np.nan,
                            DD_share_of_silent=float((sub[~sub[col]].leg == "DD").mean())
                            if (~sub[col]).any() else np.nan))
    CEN = pd.DataFrame(cen)
    for _, r in CEN.iterrows():
        P(f"    {r.claim_set:6s} {r.context:8s} n {r.n:5d}  states cadence {r.n_states_cadence:5d}"
          f"  SILENT {r.share_silent:.3f}  (DD-only claims silent {r.share_silent_DD:.3f}; "
          f"DD share of the silent {r.DD_share_of_silent:.3f})")
    dump(CEN, "census")
    dump(CL, "claims")

    # =====================================================================================
    # (D) THE RE-SCORE -- cadence-silent claims against the D/W half of this run's own ladder
    # =====================================================================================
    P()
    P("=" * 100)
    P("(D) THE RE-SCORE -- each mapped statistic on the M/Q half and on the D/W half")
    P("=" * 100)
    P("  the 20 (leg x statistic type) cells this run can compute, 10 bps, cadence-balanced:")
    stat_tab = []
    for leg in LEGS:
        for typ in ["S_RATE", "S_ONLY", "S_MODAL", "S_DDTEST"]:
            row = dict(leg=LEGNAME[leg], stat_type=typ)
            for lname, lc in LADDERS.items():
                row[lname] = stat_value(g10, lc, leg, typ)
            row["delta_MQ_minus_DW"] = row["COARSE2"] - row["FINE2"]
            stat_tab.append(row)
    ST = pd.DataFrame(stat_tab)
    P("    " + ST.to_string(index=False, float_format=lambda x: f"{x:.3f}").replace("\n", "\n    "))
    dump(ST, "statistics")

    stmap = {(r.leg, r.stat_type): r for _, r in ST.iterrows()}
    rs = []
    for _, c in CL.iterrows():
        s = stmap[(LEGNAME[c.leg], c.stat_type)]
        mq, dw = float(s["COARSE2"]), float(s["FINE2"])
        if c.stat_type in ("S_MODAL", "S_DDTEST"):
            survives = bool(dw >= 1.0) if c.stat_type == "S_MODAL" else bool(dw >= 0.80)
            basis = "named leg still modal on D/W" if c.stat_type == "S_MODAL" \
                else "named leg still fails >= 0.80 on D/W"
        else:
            survives = bool(abs(mq - dw) <= MOVE_TOL)
            basis = f"|M/Q - D/W| <= {MOVE_TOL}"
        num = float(c.published_num)
        located = bool(np.isfinite(num) and abs(num - mq) <= MOVE_TOL)
        pub_surv = bool(np.isfinite(num) and abs(num - dw) <= MOVE_TOL)
        rs.append(dict(source=c.source, line=c.line, leg=LEGNAME[c.leg], stat_type=c.stat_type,
                       claim_set_STRICT=c.set_STRICT, claim_set_WIDE=c.set_WIDE,
                       cadence_in_sentence=c.cadence_in_sentence, cadence_in_row=c.cadence_in_row,
                       published_num=num, published_txt=c.published_txt,
                       value_MQ=mq, value_DW=dw, abs_delta=abs(mq - dw),
                       survives_DW=survives, survival_basis=basis,
                       located_on_MQ=located, published_survives_DW=pub_surv,
                       text=c.text[:200]))
    RS = pd.DataFrame(rs)
    dump(RS, "rescore")

    P()
    P("  RE-SCORE of the CADENCE-SILENT claims (sentence context), by claim set x ladder half:")
    resc = []
    for cs in ["STRICT", "WIDE", "FILES"]:
        col = "claim_set_STRICT" if cs == "STRICT" else (
            "claim_set_WIDE" if cs == "WIDE" else None)
        sub = RS if col is None else RS[RS[col]]
        sil = sub[~sub.cadence_in_sentence]
        loc = sil[sil.located_on_MQ]
        resc.append(dict(claim_set=cs, n_claims=len(sub), n_silent=len(sil),
                         share_silent=float(len(sil) / len(sub)) if len(sub) else np.nan,
                         n_mapped=len(sil),
                         share_not_surviving_DW=float(1.0 - sil.survives_DW.mean())
                         if len(sil) else np.nan,
                         mean_abs_delta=float(sil.abs_delta.mean()) if len(sil) else np.nan,
                         median_abs_delta=float(sil.abs_delta.median()) if len(sil) else np.nan,
                         DD_share=float((sil.leg == "L4_DD").mean()) if len(sil) else np.nan,
                         n_located=len(loc),
                         located_published_survives=float(loc.published_survives_DW.mean())
                         if len(loc) else np.nan))
    RESC = pd.DataFrame(resc)
    for _, r in RESC.iterrows():
        P(f"    {r.claim_set:6s} claims {r.n_claims:5d}  silent {r.n_silent:5d} "
          f"({r.share_silent:.3f})  NOT surviving D/W {r.share_not_surviving_DW:.3f}  "
          f"mean|delta| {r.mean_abs_delta:.3f}  median {r.median_abs_delta:.3f}  "
          f"DD share {r.DD_share:.3f}  located {r.n_located:4d} of which published number "
          f"survives {r.located_published_survives if r.n_located else float('nan'):.3f}")
    dump(RESC, "rescore_summary")

    P()
    P("  the same, split by statistic type (STRICT set, cadence-silent):")
    sil_s = RS[RS.claim_set_STRICT & ~RS.cadence_in_sentence]
    bytype = sil_s.groupby(["stat_type", "leg"]).apply(
        lambda s: pd.Series({"n": len(s), "value_MQ": float(s.value_MQ.iloc[0]),
                             "value_DW": float(s.value_DW.iloc[0]),
                             "abs_delta": float(s.abs_delta.iloc[0]),
                             "survives_DW": bool(s.survives_DW.iloc[0])})).reset_index()
    P("    " + bytype.to_string(index=False, float_format=lambda x: f"{x:.3f}")
      .replace("\n", "\n    "))
    dump(bytype, "bytype")

    # =====================================================================================
    # (E) RULE 8 -- walk-forward, (book, gross) chosen on 2009-2016 alone, per panel x cadence
    # =====================================================================================
    P()
    P("=" * 100)
    P("(E) RULE 8 WALK-FORWARD -- (book, gross) chosen on 2009-2016 alone, OOS 2017-2026 once")
    P("=" * 100)
    canon = g10[g10.phase == 0].reset_index(drop=True)
    picks = []
    for pn_ in panels:
        for cad in cads:
            sub = canon[(canon.panel == pn_) & (canon.cadence == cad)].reset_index(drop=True)
            for ch in CHOOSERS:
                i = choose(ch, sub)
                if i is None:
                    continue
                r = sub.iloc[i]
                lg = legs_rec(r)
                rec = dict(panel=pn_, cadence=cad, half="D/W" if cad in ("D", "W") else "M/Q",
                           chooser=ch, book=r.book, gross=r.gross, turn_per_yr=r.turn_per_yr,
                           OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                           spy_OOS_CAGR=r.spy_OOS_CAGR, spy_OOS_Sharpe=r.spy_OOS_Sharpe,
                           spy_OOS_MaxDD=r.spy_OOS_MaxDD, spy_CAGR=r.spy_CAGR,
                           spy_MaxDD=r.spy_MaxDD, v2_Sharpe=r.v2_Sharpe, v2_MaxDD=r.v2_MaxDD,
                           pass4b=bool(all(lg.values())), fail4b=failstr(lg),
                           pass4a=bool(r.pass4a),
                           DD_binds=bool(not lg["DD"]),
                           only_DD=bool(sum(not v for v in lg.values()) == 1 and not lg["DD"]))
                picks.append(rec)
    WF = pd.DataFrame(picks)
    P(f"  {'panel':6s} {'cad':3s} {'chooser':9s} {'book':7s} {'gr':5s} {'OOS CAGR':>9s} "
      f"{'Sharpe':>7s} {'MaxDD':>8s} {'4b':>4s} {'4a':>4s}  failed legs")
    for _, r in WF.iterrows():
        P(f"  {r.panel:6s} {r.cadence:3s} {r.chooser:9s} {r.book:7s} {r.gross:5s} "
          f"{r.OOS_CAGR:9.2%} {r.OOS_Sharpe:7.3f} {r.OOS_MaxDD:8.2%} "
          f"{'PASS' if r.pass4b else 'fail':>4s} {'PASS' if r.pass4a else 'fail':>4s}  {r.fail4b}")
    sp = canon.iloc[0]
    P()
    P(f"  SPY OOS {sp.spy_OOS_CAGR:.2%} / {sp.spy_OOS_Sharpe:.3f} / {sp.spy_OOS_MaxDD:.2%}   "
      f"(4b bars: OOS Sharpe > {sp.spy_OOS_Sharpe:.3f}, MaxDD >= {0.60*sp.spy_MaxDD:.2%}, "
      f"OOS CAGR >= {0.70*sp.spy_CAGR:.2%})")
    for pn_ in panels:
        v = canon[canon.panel == pn_].iloc[0]
        P(f"  RULES v2 (live, the 4a comparand) on {pn_}: full-sample Sharpe {v.v2_Sharpe:.3f} "
          f"MaxDD {v.v2_MaxDD:.2%}")
    dw = WF[WF.half == "D/W"]
    mq = WF[WF.half == "M/Q"]
    dd_dw = float(dw.DD_binds.mean()) if len(dw) else np.nan
    dd_mq = float(mq.DD_binds.mean()) if len(mq) else np.nan
    P()
    P(f"  OOS 4b {int(WF.pass4b.sum())} of {len(WF)};  OOS 4a {int(WF.pass4a.sum())} of {len(WF)}")
    P(f"  L4_DD among the failed legs: M/Q {int(mq.DD_binds.sum())} of {len(mq)} ({dd_mq:.3f})"
      f"   vs   D/W {int(dw.DD_binds.sum())} of {len(dw)} ({dd_dw:.3f})   gap {dd_mq-dd_dw:+.3f}")
    P(f"  the ONLY failed leg: M/Q {int(mq.only_DD.sum())} of {len(mq)}, "
      f"D/W {int(dw.only_DD.sum())} of {len(dw)}")
    P(f"  full-sample over the {len(g10):,}-row 10 bps grid: 4b {int(g10.pass4b_REC.sum()):,}, "
      f"4a {int(g10.pass4a.sum()):,}")
    if len(WF[WF.pass4b]):
        P("  the OOS 4b passers (both KEEP paths evaluated on every pick):")
        for _, r in WF[WF.pass4b].iterrows():
            P(f"    {r.panel}/{r.cadence}/{r.chooser}: {r.book}@{r.gross} "
              f"{r.OOS_CAGR:.2%} / {r.OOS_Sharpe:.3f} / {r.OOS_MaxDD:.2%}  "
              f"4a {'PASS' if r.pass4a else 'fail'} (v2 Sharpe {r.v2_Sharpe:.3f} "
              f"MaxDD {r.v2_MaxDD:.2%})")
    dump(WF, "walkforward")

    perm = canon.copy()
    rng = np.random.default_rng(7)
    for c in [c for c in perm.columns if c.startswith("OOS_")]:
        perm[c] = rng.permutation(perm[c].values)
    g7bad = 0
    for pn_ in panels:
        for cad in cads:
            a0 = canon[(canon.panel == pn_) & (canon.cadence == cad)].reset_index(drop=True)
            b0 = perm[(perm.panel == pn_) & (perm.cadence == cad)].reset_index(drop=True)
            for ch in CHOOSERS:
                if choose(ch, a0) != choose(ch, b0):
                    g7bad += 1
    gk["G7"] = g7bad == 0
    P(f"  G7 choosers invariant to permuted OOS columns: {g7bad} disagreements  "
      f"{'PASS' if gk['G7'] else 'FAIL'}")
    gdetail.append(dict(gate="G7", stat=float(g7bad), bar=0.0, passed=gk["G7"],
                        what="every rule-8 chooser is IS-only"))

    # =====================================================================================
    # (F) PRE-REGISTERED HYPOTHESES
    # =====================================================================================
    P()
    P("=" * 100)
    P("(F) PRE-REGISTERED HYPOTHESES  (headline = STRICT claim set, SENTENCE context)")
    P("=" * 100)
    head = RESC[RESC.claim_set == "STRICT"].iloc[0]
    hyp = [
        dict(H="H_SILENT", stat=float(head.share_silent), bar=f">= {SILENT_BAR}",
             passed=bool(head.share_silent >= SILENT_BAR),
             what=f"{int(head.n_silent)} of {int(head.n_claims)} committed leg-binding claims "
                  f"state no cadence"),
        dict(H="H_MOVE", stat=float(head.share_not_surviving_DW), bar=f">= {MOVE_BAR}",
             passed=bool(head.share_not_surviving_DW >= MOVE_BAR),
             what="share of cadence-silent claims whose statistic does not survive the D/W half"),
        dict(H="H_GAP", stat=float(head.mean_abs_delta), bar=f">= {GAP_BAR}",
             passed=bool(head.mean_abs_delta >= GAP_BAR),
             what="claim-weighted mean |M/Q value - D/W value| of the mapped statistics"),
        dict(H="H_DD", stat=float(head.DD_share), bar=f">= {DD_BAR}",
             passed=bool(head.DD_share >= DD_BAR),
             what="share of cadence-silent claims that name L4_DD"),
        dict(H="H_RULE8", stat=float(dd_mq - dd_dw), bar=f">= {RULE8_BAR}",
             passed=bool((dd_mq - dd_dw) >= RULE8_BAR),
             what=f"walk-forward DD-bind share M/Q {dd_mq:.3f} minus D/W {dd_dw:.3f}"),
    ]
    HY = pd.DataFrame(hyp)
    for _, r in HY.iterrows():
        P(f"  {r.H:9s} {'PASS' if r.passed else 'FAIL':4s}  stat {r.stat:+.4f}  bar {r.bar:10s}  "
          f"{r.what}")
    dump(HY, "hypotheses")

    hS = bool(HY.set_index("H").loc["H_SILENT", "passed"])
    hM = bool(HY.set_index("H").loc["H_MOVE", "passed"])
    hG = bool(HY.set_index("H").loc["H_GAP", "passed"])
    hR = bool(HY.set_index("H").loc["H_RULE8", "passed"])
    if hS and (hM or hG) and hR:
        answer = ("CONSEQUENTIAL -- KEEP the cadence clause as a PROTOCOL rule 4 reporting "
                  "clause (proposed, not applied; rule 6)")
    elif hS and not (hM or hG):
        answer = "SILENT BUT COSTLESS -- KILL the clause"
    elif not hS:
        answer = "REDUNDANT -- the record already states its cadence; KILL the clause"
    else:
        answer = "MIXED -- report the mixture; no clause proposed"
    P()
    P(f"  DECISION RULE (fixed in advance) -> the cadence clause is: {answer}")

    # sensitivity: the same decision under every claim set and the ROW context (reported)
    P()
    P("  SENSITIVITY (reported, not selected) -- the same four shares under each claim set and "
      "the ROW context:")
    sens = []
    for cs in ["STRICT", "WIDE", "FILES"]:
        col = "claim_set_STRICT" if cs == "STRICT" else (
            "claim_set_WIDE" if cs == "WIDE" else None)
        sub = RS if col is None else RS[RS[col]]
        for ctx_ in ["SENTENCE", "ROW"]:
            ccol = "cadence_in_sentence" if ctx_ == "SENTENCE" else "cadence_in_row"
            sil = sub[~sub[ccol]]
            sens.append(dict(claim_set=cs, context=ctx_, n=len(sub), n_silent=len(sil),
                             H_SILENT=float(len(sil) / len(sub)) if len(sub) else np.nan,
                             H_MOVE=float(1 - sil.survives_DW.mean()) if len(sil) else np.nan,
                             H_GAP=float(sil.abs_delta.mean()) if len(sil) else np.nan,
                             H_DD=float((sil.leg == "L4_DD").mean()) if len(sil) else np.nan))
    SENS = pd.DataFrame(sens)
    P("    " + SENS.to_string(index=False, float_format=lambda x: f"{x:.3f}")
      .replace("\n", "\n    "))
    dump(SENS, "sensitivity")

    # marginal variance shares, for the record (reported)
    P()
    dec = pd.DataFrame([dict(leg=LEGNAME[k],
                             eta2_cadence=eta2(g10, "cadence", "leg_" + k),
                             eta2_panel=eta2(g10, "panel", "leg_" + k),
                             eta2_book=eta2(g10, "book", "leg_" + k),
                             eta2_gross=eta2(g10, "gross", "leg_" + k),
                             eta2_phase=eta2(g10, "phase", "leg_" + k)) for k in LEGS])
    P("  MARGINAL variance shares of each leg's PASS indicator (one-way eta^2, NOT orthogonal):")
    P("    " + dec.to_string(index=False, float_format=lambda x: f"{x:.4f}")
      .replace("\n", "\n    "))
    dump(dec, "decomp")

    GA = pd.DataFrame(gdetail)
    dump(GA, "gates")
    P()
    P(f"  GATES {int(sum(gk.values()))} of {len(gk)} PASS  "
      f"({', '.join(k for k, v in gk.items() if not v) or 'none failed'})")
    P(f"  runtime {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
