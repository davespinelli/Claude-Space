#!/usr/bin/env python3
"""Idea 943 (lane C, 2026-09-15) -- should every published CADENCE or TURNOVER claim carry
its NULL'S GAIN?

THE QUESTION (queue, 2026-09-15)
  Idea 931 found the W->M improvement on the standing candidate is a TURNOVER REBATE every book
  collects: the null's own median gain runs +0.0466 / +0.3334 / +0.7624 / +1.4501 at 0 / 10 / 25 /
  50 bps while the book's runs +0.0994 / +0.1525 / +0.2321 / +0.3645.  The queue asks for the
  RECORD-WIDE form: census the committed cadence and turnover claims for whether any of them
  priced the null's gain, and re-score those that did not.

WHY THE NULL'S GAIN IS THE RIGHT SUBTRAHEND
  Slowing a book down cuts its turnover, and at a fixed cost rung every book -- including a coin
  flip -- is paid for that.  So a published "monthly beats weekly by X of Sharpe" is evidence
  about the RULE only in the part of X that exceeds what a gross-matched random book collects for
  free on the same panel over the same cadence step.  The null-differenced gain
  (book gain minus null median gain) is that part.  A claim that never subtracted it is quoting a
  rebate as a result.

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL 4: max 2 tuned parameters)
  TUNED 1  CLAIM SET, 2 levels, both reported and never merged:
           STRICT = a committed paragraph carrying a cadence-or-turnover AXIS token, a
                    COMPARATIVE token, a METRIC word and >= 2 numerals
           WIDE   = the same AXIS token and >= 1 numeral (no comparative, no metric word)
  TUNED 2  COST RUNG, 4 levels, ALL reported: 0 / 10 / 25 / 50 bps (PROTOCOL's own rung is 10)
  REPORTED AXES (nothing fitted on them; every point published):
           PANEL {U56, B136} -- the 663-name SMALL panel is NOT included here and this run makes
           no claim about it; idea 931 read it and found the same direction, 0.0 percentile;
           CADENCE STEP {D->W, W->M, M->Q, W->Q}; BOOK TEMPLATE
           {TOP20 = idea 670's CAND20 = CORE/TOP20; TOP05 = RULES v1's own width, k = 5};
           WINDOW {FULL, IS, OOS, H1, H2}; 300 draws per (panel, cadence, template) with the
           150-draw half-sample printed beside it.

THE BOOKS (both pre-existing in the record; NOT re-specified here)
  TOP20  each rebalance rank every priced name above its own 200d MA with 20d realised vol < 0.60
         by the v1 composite mean(pct-rank 12-1 mom, pct-rank 6m, pct-rank 3m) x (1 if above 200d
         MA else 0.5) WITHOUT the /sqrt(vol20) term; hold top k = min(20, #eligible) at g/k, g=0.75.
  TOP05  the same screen and the same composite at k = min(5, #eligible) -- RULES v1's own width.
  WHY NOT AN EQUAL-WEIGHT-EVERYTHING TEMPLATE: with k(t) = |P(t)| the gross-matched draw has to
  take the whole pool, so the "null" IS the book and every excess is identically zero.  That is a
  degenerate cell, not a result, and G8 gates against it.

THE NULL (idea 680's construction as used by idea 931, unmodified)
  On each DECISION row the null holds the book's own k(t) names at the book's own per-name weight
  w(t) = g/k(t), drawn uniformly without replacement from the book's own candidate pool P(t).
  Count, per-name weight, gross and cash are copied row by row (G2); only WHICH names differs.
  The null is re-drawn on its OWN cadence, so it carries the same turnover effect the book does --
  which is the entire point of differencing against it.

PRE-REGISTERED BARS (fixed before any number was read; both directions reported)
  H_CENSUS  at least one committed cadence-or-turnover claim in the record prices its null's GAIN
            (a null DELTA distribution on the same axis), under EITHER claim set.
  H_REBATE  the null's median gain is > 0 at 10 bps on EVERY (panel, step, template) cell -- the
            rebate is universal, not a U56/W->M special case.
  H_EXCESS  the book's cadence gain exceeds its own null's median gain on >= 50% of
            (panel, step, template) cells at 10 bps.  Below that, the record's cadence claims are
            mostly rebate.
  H_RUNG    the per-cell verdict (book gain > null median) agrees on >= 90% of cells between the
            0 bps and the 10 bps rung.  A verdict that only exists at one rung is a rung fact.
  H_CLAIM   the census headline (share of claims that priced the null's gain) moves by <= 5
            percentage points between STRICT and WIDE.
  H_WF      (rule 8, REQUIRED) cadence chosen on 2009-2016 ALONE by IS Sharpe, 2017-2026 read
            ONCE, both KEEP paths, against SPY and the live RULES v2 book in the same window.

GATES (all printed before any result number)
  G1  the fast runner == `engine.backtest` on returns and turnover (TOP20, U56, W and M)
  G2  the null's TARGET gross / count / per-name weight == the book's on every cell
  G3  CROSS-RUN: idea 931's published U56 TOP20 book gains and NULL MEDIAN gains, W->M, 4 rungs
  G4  the draw is legal: |P(t)| >= k(t) on every decision row of every panel and cadence
  G5  determinism: the same seed reproduces the same null return series bit-for-bit
  G6  the null is INVESTED on every cadence (median realised gross > 0.50, vol > 0.01)
  G7  the census is deterministic and its corpus is the committed tree (file count + byte count)
  G8  the draw is UNIFORM and NON-DEGENERATE: observed null-vs-book name overlap == the
      hypergeometric expectation E[k/|P|] on every cell, and that expectation is < 0.95.
      RE-SPECIFIED after its first cut (a flat "overlap < 0.50" bar, which failed at 0.5749 for a
      reason that is not degeneracy -- see the comment at the gate).  Stated, not hidden.

PROTOCOL: 10 bps primary, t+1 execution, warm-up 260 days, IS 2009-2016 / OOS 2017-2026.
Nothing in RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py is modified.

SURVIVORSHIP: U56 and B136 are CURRENT-CONSTITUENT lists, so every CAGR and drawdown LEVEL is
optimistic.  The direction for THIS run's headline is specific and works AGAINST the books: a coin
flip drawn from a survivor panel is a BETTER book than one drawn in real time, so every NULL gain
here is an UPPER bound and every book's excess over it is a LOWER bound -- a cell where the book
fails to out-gain its null fails a fortiori.  The 4b bar is SPY, which is not survivorship-
inflated.  Stated, not hidden.
"""
from __future__ import annotations

import json
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
from baseline import load_universe, rules_v2_weights, score  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

# ---- reported constants (never tuned) ---------------------------------------------------------
COST0 = 10.0
LAG = 1
MAXVOL = 0.60
NTOP = 20
NTOP5 = 5
GROSS = 0.75
WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COSTS = [0.0, 10.0, 25.0, 50.0]
NDRAW = 300
HALF = 150
SEED0 = 20260943

PANELS = ["U56", "B136"]
FREQS = ["D", "W", "M", "Q"]
STEPS = [("D", "W"), ("W", "M"), ("M", "Q"), ("W", "Q")]
TEMPLATES = ["TOP20", "TOP05"]

EXCESS_BAR = 0.50     # H_EXCESS
RUNG_BAR = 0.90       # H_RUNG
CLAIM_BAR = 5.0       # H_CLAIM (percentage points)

# idea 931's committed U56 TOP20 W->M numbers at 0 / 10 / 25 / 50 bps
PUB_BOOK_GAIN = [0.0994, 0.1525, 0.2321, 0.3645]
PUB_NULL_GAIN = [0.0466, 0.3334, 0.7624, 1.4501]
TOL_GAIN = 0.060      # the record's own vintage bar for a Sharpe difference, doubled (2 x 0.030)

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ================================================================================================
# PART A -- THE CENSUS
# ================================================================================================
AX_CAD = re.compile(r"(W\s*->\s*M|W→M|caden\w*|rebalance frequenc\w*|freq\s*=|D/W/M/Q)", re.I)
AX_WK = re.compile(r"\bweekly\b", re.I)
AX_MO = re.compile(r"\b(monthly|quarterly|daily)\b", re.I)
AX_TUR = re.compile(r"\bturnover\b", re.I)
CMP = re.compile(r"(improv\w*|\bgains?\b|\bgained\b|\bbetter\b|\blifts?\b|\blifted\b|\bworse\b|->|→"
                 r"|\bvs\b|\brebate\b|\bbeats?\b|advantage|\bdrops?\b|\bfaster\b|\bslow\w*\b)", re.I)
MET = re.compile(r"(Sharpe|CAGR|MaxDD|turnover|\bpp\b|drawdown)", re.I)
NUM = re.compile(r"[-+]?\d+\.\d+|\d+(?:\.\d+)?%")

NULL_TOK = re.compile(r"(\bnull\b|placebo|coin[- ]?flip|random draw|shuffl\w*|bootstrap|permut\w*|RAND\b)", re.I)
DELTA_TOK = re.compile(r"(\bgain\w*|improv\w*|\bdelta\b|dSharpe|d_?sharpe|Δ|difference|excess|percentile of the (gain|improvement))", re.I)


def axis_of(para: str):
    """Which axis (if any) this paragraph is a claim about.  Cadence needs a real CONTRAST token
    or two different cadence words in the same paragraph; a bare 'weekly' is not a cadence claim."""
    cad = bool(AX_CAD.search(para)) or (bool(AX_WK.search(para)) and bool(AX_MO.search(para)))
    tur = bool(AX_TUR.search(para))
    if cad and tur:
        return "BOTH"
    if cad:
        return "CADENCE"
    if tur:
        return "TURNOVER"
    return ""


def own_para_prices_null_gain(para: str) -> bool:
    """The LOWER bound: the claim's OWN paragraph states a null DELTA on this axis.  `classify_run`
    is the UPPER bound -- it credits the whole run family, so a run that priced a null gain on some
    OTHER axis counts.  Publishing both is the point: the true share sits inside the band."""
    if not NULL_TOK.search(para):
        return False
    return bool(DELTA_TOK.search(para))


def classify_run(text: str) -> str:
    """N2 the run prices a NULL DELTA on this axis; N1 a null is present but only as a LEVEL;
    N0 no null construction at all."""
    if not NULL_TOK.search(text):
        return "N0_NO_NULL"
    for m in NULL_TOK.finditer(text):
        win = text[max(0, m.start() - 220): m.end() + 220]
        if DELTA_TOK.search(win) and (AX_CAD.search(win) or AX_TUR.search(win)
                                      or (AX_WK.search(win) and AX_MO.search(win))):
            return "N2_NULL_GAIN_PRICED"
    return "N1_NULL_LEVEL_ONLY"


def run_census():
    P("\n" + "=" * 100)
    P("PART A -- THE CENSUS of committed CADENCE and TURNOVER claims")
    P("=" * 100)
    bt = ROOT / "research" / "backtests"
    md_files = sorted(list(bt.glob("*.result.md")) + list(bt.glob("*.memo.md")))
    corpus_bytes = sum(f.stat().st_size for f in md_files)

    # the run FAMILY text used for the null classification: the memo + its own script
    fam_cache: dict[str, str] = {}

    def family_text(stem: str) -> str:
        if stem not in fam_cache:
            parts = []
            for suf in (".py", ".result.md", ".memo.md"):
                p = bt / f"{stem}{suf}"
                if p.exists():
                    parts.append(p.read_text(errors="ignore"))
            fam_cache[stem] = "\n".join(parts)
        return fam_cache[stem]

    rows = []
    for f in md_files:
        stem = f.name.replace(".result.md", "").replace(".memo.md", "")
        txt = f.read_text(errors="ignore")
        paras = re.split(r"\n\s*\n", txt)
        for pi, para in enumerate(paras):
            ax = axis_of(para)
            if not ax:
                continue
            nums = NUM.findall(para)
            wide = len(nums) >= 1
            strict = bool(CMP.search(para)) and bool(MET.search(para)) and len(nums) >= 2
            if not wide:
                continue
            fam = family_text(stem)
            rows.append(dict(source="MEMO", file=f.name, stem=stem, para=pi, axis=ax,
                             n_numerals=len(nums), in_STRICT=strict, in_WIDE=wide,
                             null_class=classify_run(fam),
                             own_para_null_gain=own_para_prices_null_gain(para),
                             text=re.sub(r"\s+", " ", para)[:400]))

    # CHANGELOG: one claim unit per paragraph, run resolved via the "Scripts/artifacts:" pointer
    cl = (ROOT / "research" / "CHANGELOG.md").read_text(errors="ignore")
    cl_entries = re.split(r"\n(?=- 20\d\d-\d\d-\d\d )", cl)
    for ei, ent in enumerate(cl_entries):
        m = re.search(r"research/backtests/([0-9A-Za-z_\-\.]+?)\.py", ent)
        stem = m.group(1) if m else ""
        fam = family_text(stem) if stem else ent
        for pi, para in enumerate(re.split(r"\n\s*\n", ent)):
            ax = axis_of(para)
            if not ax:
                continue
            nums = NUM.findall(para)
            if len(nums) < 1:
                continue
            strict = bool(CMP.search(para)) and bool(MET.search(para)) and len(nums) >= 2
            rows.append(dict(source="CHANGELOG", file=f"CHANGELOG.md#{ei}", stem=stem, para=pi, axis=ax,
                             n_numerals=len(nums), in_STRICT=strict, in_WIDE=True,
                             null_class=classify_run(fam) if stem else "N0_UNRESOLVED",
                             own_para_null_gain=own_para_prices_null_gain(para),
                             text=re.sub(r"\s+", " ", para)[:400]))

    # LEADERBOARD: one claim unit per row, run resolved via the last column (the script filename)
    lb = (ROOT / "research" / "LEADERBOARD.md").read_text(errors="ignore").split("\n")
    for li, line in enumerate(lb):
        if not line.startswith("|") or line.count("|") < 4:
            continue
        ax = axis_of(line)
        if not ax:
            continue
        nums = NUM.findall(line)
        if len(nums) < 1:
            continue
        last = line.rstrip("|").rsplit("|", 1)[-1].strip().replace(".py", "")
        stem = last if (bt / f"{last}.py").exists() else ""
        fam = family_text(stem) if stem else line
        strict = bool(CMP.search(line)) and bool(MET.search(line)) and len(nums) >= 2
        rows.append(dict(source="LEADERBOARD", file=f"LEADERBOARD.md#{li}", stem=stem, para=0, axis=ax,
                         n_numerals=len(nums), in_STRICT=strict, in_WIDE=True,
                         null_class=classify_run(fam) if stem else "N0_UNRESOLVED",
                         own_para_null_gain=own_para_prices_null_gain(line),
                         text=re.sub(r"\s+", " ", line)[:400]))

    cen = pd.DataFrame(rows)
    P(f"\n  corpus: {len(md_files):,} committed .result.md/.memo.md files ({corpus_bytes:,} bytes)")
    P(f"          + CHANGELOG.md ({len(cl_entries)} entries) + LEADERBOARD.md ({len(lb)} lines)")
    P(f"  claim units found: WIDE {len(cen):,}   STRICT {int(cen.in_STRICT.sum()):,}")

    head = []
    for cs in ("STRICT", "WIDE"):
        sub = cen[cen["in_STRICT"]] if cs == "STRICT" else cen
        for src in ("ALL", "MEMO", "CHANGELOG", "LEADERBOARD"):
            s2 = sub if src == "ALL" else sub[sub.source == src]
            if not len(s2):
                continue
            n2 = int((s2.null_class == "N2_NULL_GAIN_PRICED").sum())
            n1 = int((s2.null_class == "N1_NULL_LEVEL_ONLY").sum())
            n0 = int(len(s2) - n1 - n2)
            head.append(dict(claim_set=cs, source=src, n_claims=len(s2),
                             n_N2_gain_priced=n2, n_N1_level_only=n1, n_N0_no_null=n0,
                             share_gain_priced=n2 / len(s2), share_any_null=(n1 + n2) / len(s2),
                             n_own_para_gain=int(s2.own_para_null_gain.sum()),
                             share_own_para_gain=float(s2.own_para_null_gain.mean())))
    H = pd.DataFrame(head)
    P("\n  CENSUS HEADLINE.  share_gain_priced is the UPPER bound (the whole run family is credited);")
    P("  share_own_para_gain is the LOWER bound (the claim's own paragraph states a null DELTA).")
    P(H.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(cen.drop(columns=["text"]).assign(text=cen.text), "census.csv")
    dump(H, "census_headline.csv")
    return cen, H, len(md_files), corpus_bytes


# ================================================================================================
# PART B -- THE REBUILD (the null's own gain, so the census has a subtrahend to offer)
# ================================================================================================
class Panel:
    def __init__(self, name, px, freq):
        self.name, self.px, self.freq = name, px, freq
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        T, N = self.rets.shape
        self.T, self.N = T, N
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, N)), C[:-1]])
        mk = rebalance_mask(self.idx, freq).shift(LAG, fill_value=False).values.copy()
        mk[0] = True
        self.reb = np.flatnonzero(mk)
        seg = np.searchsorted(self.reb, np.arange(T), side="right") - 1
        self.s0 = self.reb[seg]
        self.s0p = self.reb[np.maximum(seg - 1, 0)]
        self.dec = np.maximum(self.reb - LAG, 0)
        self.R = self.Cp / self.Cp[self.s0]
        self.Rp = self.Cp[self.reb] / self.Cp[self.s0p[self.reb]]
        m_full = np.asarray(self.idx >= self.idx[WARMUP])
        fp = np.flatnonzero(m_full)
        h = len(fp) // 2
        m1 = np.zeros(T, bool); m1[fp[:h]] = True
        m2 = np.zeros(T, bool); m2[fp[h:]] = True
        self.masks = {"FULL": m_full, "H1": m1, "H2": m2,
                      "IS": m_full & np.asarray(self.idx <= pd.Timestamp(IS_END)),
                      "OOS": np.asarray(self.idx >= pd.Timestamp(OOS_START))}
        self.spy = px["SPY"].pct_change().fillna(0.0).values


class Book:
    """gross-1.0 target weights W1 -> (gross return path, turnover path) at any g and cost."""

    def __init__(self, panel: Panel, W1: np.ndarray):
        self.pan = panel
        wt = np.roll(W1, LAG, axis=0).copy()
        wt[:LAG] = 0.0
        self.wt_reb = wt[panel.reb]
        A = wt[panel.s0]
        AR = A * panel.R
        self.S = AR.sum(axis=1)
        self.As = A.sum(axis=1)
        self.ARr = (AR * panel.rets).sum(axis=1)
        Ap = wt[panel.s0p[panel.reb]]
        self.ARp = Ap * panel.Rp
        self.Sp = self.ARp.sum(axis=1)
        self.Asp = Ap.sum(axis=1)

    def paths(self, g=GROSS):
        """Cost-free return path and turnover path; any cost rung is then r = gr - turn*c/1e4."""
        pan = self.pan
        V = 1.0 + g * (self.S - self.As)
        gr = g * self.ARr / V
        Vp = 1.0 + g * (self.Sp - self.Asp)
        heldp = (g * self.ARp) / Vp[:, None]
        heldp[0] = 0.0
        turn = np.zeros(pan.T)
        turn[pan.reb] = np.abs(g * self.wt_reb - heldp).sum(axis=1)
        return gr, turn

    def at(self, g=GROSS, cost=COST0):
        gr, turn = self.paths(g)
        return gr - turn * cost / 1e4, turn

    def realised_gross(self, g=GROSS):
        V = 1.0 + g * (self.S - self.As)
        return g * self.S / V


def fmet(r):
    r = np.asarray(r, float)
    if len(r) < 3 or not np.isfinite(r).all():
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    if len(r) < 3:
        return np.nan
    v = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / v if v else np.nan


def pack(r, pan):
    c, s, d = fmet(np.asarray(r)[pan.masks["FULL"]])
    co, so, do = fmet(np.asarray(r)[pan.masks["OOS"]])
    ci, si, di = fmet(np.asarray(r)[pan.masks["IS"]])
    return dict(CAGR=c, Sharpe=s, MaxDD=d,
                H1=fsharpe(np.asarray(r)[pan.masks["H1"]]),
                H2=fsharpe(np.asarray(r)[pan.masks["H2"]]),
                iCAGR=ci, iSharpe=si, iMaxDD=di,
                oCAGR=co, oSharpe=so, oMaxDD=do)


def legs4b(s, spy):
    L = dict(L1_H1=bool(s["H1"] > spy["H1"]), L2_H2=bool(s["H2"] > spy["H2"]),
             L3_OOS=bool(s["oSharpe"] > spy["oSharpe"]),
             L4_DDcap=bool(s["MaxDD"] >= DD_CAP * spy["MaxDD"]),
             L5_CAGRfloor=bool(s["CAGR"] >= CAGR_FLOOR * spy["CAGR"]))
    L["pass4b"] = bool(all(L.values()))
    return L


def elig_and_score(px):
    sc, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < MAXVOL) & px.notna() & sc.notna()
    return sc.where(elig), elig


def template_w1(px, template):
    """Returns (W1 gross-1 weights, pool boolean, k(t)) for a template."""
    sce, elig = elig_and_score(px)
    n = {"TOP20": NTOP, "TOP05": NTOP5}[template]
    rank = sce.rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    W1 = sel.div(k, axis=0).fillna(0.0).values
    return W1, elig.values, sel.sum(axis=1).values.astype(int)


def null_w1(pool, kcount, dec, rng):
    """Gross-matched coin flip on the DECISION rows (idea 680/931 construction, unmodified)."""
    T, N = pool.shape
    W = np.zeros((T, N))
    for t in dec:
        k = kcount[t]
        if k <= 0:
            continue
        idx = np.flatnonzero(pool[t])
        if len(idx) == 0:
            continue
        k = min(k, len(idx))
        pick = rng.choice(idx, size=k, replace=False)
        W[t, pick] = 1.0 / k
    return W


# ================================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 943 (lane C) -- should every published CADENCE or TURNOVER claim carry its NULL'S GAIN?")
    P("=" * 100)

    cen, CEN_H, n_md, n_bytes = run_census()

    P("\n" + "=" * 100)
    P("PART B -- THE REBUILD: the null's own cadence gain, at every rung")
    P("=" * 100)

    raw = {"U56": load_universe(), "B136": load_universe(broad=True)}
    P("  panels: " + ", ".join(f"{k} {v.shape[1]} cols x {v.shape[0]} rows "
                               f"[{v.index[0].date()}..{v.index[-1].date()}]" for k, v in raw.items()))

    ctx = {}
    for pn, px in raw.items():
        for tm in TEMPLATES:
            W1, pool, kc = template_w1(px, tm)
            for f in FREQS:
                pan = Panel(pn, px, f)
                ctx[(pn, tm, f)] = dict(pan=pan, book=Book(pan, W1), pool=pool, kc=kc, W1=W1, px=px)

    # -------------------------------------------------------------------------------- GATES
    P("\n" + "-" * 100)
    P("GATES (printed before any result number)")
    P("-" * 100)
    gates = []

    d1 = []
    for f in ("W", "M"):
        c = ctx[("U56", "TOP20", f)]
        r_f, t_f = c["book"].at(GROSS, COST0)
        eng = backtest(c["px"], pd.DataFrame(GROSS * c["W1"], index=c["px"].index, columns=c["px"].columns),
                       cost_bps=COST0, freq=f)
        m = c["pan"].masks["FULL"]
        d1.append((f, float(np.abs(r_f[m] - eng["returns"].values[m]).max()),
                   float(np.abs(t_f[m] - eng["turnover"].values[m]).max())))
    ok1 = all(a < 1e-9 and b < 1e-9 for _, a, b in d1)
    gates.append(dict(gate="G1 fast runner == engine.backtest (TOP20, U56, W and M, post-warm-up)",
                      stat=" | ".join(f"{f}: dret {a:.2e} dturn {b:.2e}" for f, a, b in d1),
                      bar="1e-9", passed=ok1))

    # G2 target gross / count / per-name weight match, and G4 draw legality, and G6 investedness
    d2g, d2k, d2w, short, inv_g, inv_v, ovl = [], [], [], 0, [], [], []
    for (pn, tm, f), c in ctx.items():
        pan, pool, kc = c["pan"], c["pool"], c["kc"]
        rng = np.random.default_rng(SEED0 + 7)
        Wn = null_w1(pool, kc, pan.dec, rng)
        bw, nw = c["W1"][pan.dec], Wn[pan.dec]
        live = (bw > 0).sum(axis=1) > 0
        if live.any():
            kk = (bw > 0).sum(axis=1)[live]
            pp = pool[pan.dec].sum(axis=1)[live]
            ovl.append((float(((((bw > 0) & (nw > 0)).sum(axis=1)[live]) / kk).mean()),
                        float((kk / np.maximum(pp, 1)).mean())))   # observed, hypergeometric E
        d2g.append(float(np.abs(bw.sum(axis=1) - nw.sum(axis=1)).max()))
        d2k.append(int(np.abs((bw > 0).sum(axis=1) - (nw > 0).sum(axis=1)).max()))
        d2w.append(float(np.abs(np.where(bw > 0, bw, 0).max(axis=1) - np.where(nw > 0, nw, 0).max(axis=1)).max()))
        short += int(sum(1 for t in pan.dec if kc[t] > 0 and pool[t].sum() < kc[t]))
        nb = Book(pan, Wn)
        rg = nb.realised_gross(GROSS)[pan.masks["FULL"]]
        rr = nb.at(GROSS, COST0)[0][pan.masks["FULL"]]
        inv_g.append(float(np.median(rg))); inv_v.append(float(rr.std(ddof=1) * np.sqrt(252)))
    gates.append(dict(gate="G2 null TARGET gross / count / per-name weight == the book's (all 16 cells)",
                      stat=f"dgross {max(d2g):.3e} | dcount {max(d2k)} | dweight {max(d2w):.3e}",
                      bar="1e-12 / 0 / 1e-12", passed=max(d2g) < 1e-12 and max(d2k) == 0 and max(d2w) < 1e-12))
    gates.append(dict(gate="G4 draw legality |P(t)| >= k(t) on every decision row",
                      stat=f"{short} rows short", bar="0", passed=short == 0))
    gates.append(dict(gate="G6 the null is INVESTED on every cell (median realised gross, ann vol)",
                      stat=f"min median gross {min(inv_g):.4f} | min vol {min(inv_v):.4f}",
                      bar="> 0.50 / > 0.01", passed=min(inv_g) > 0.50 and min(inv_v) > 0.01))

    rngA = np.random.default_rng(SEED0 + 11)
    rngB = np.random.default_rng(SEED0 + 11)
    cA = ctx[("U56", "TOP20", "M")]
    rA = Book(cA["pan"], null_w1(cA["pool"], cA["kc"], cA["pan"].dec, rngA)).at(GROSS, COST0)[0]
    rB = Book(cA["pan"], null_w1(cA["pool"], cA["kc"], cA["pan"].dec, rngB)).at(GROSS, COST0)[0]
    gates.append(dict(gate="G5 determinism: same seed -> same null return series",
                      stat=f"{float(np.abs(rA - rB).max()):.3e}", bar="0", passed=bool(np.abs(rA - rB).max() == 0)))

    g7 = n_md > 700 and n_bytes > 0 and len(cen) > 0
    gates.append(dict(gate="G7 census corpus is the committed tree and non-empty",
                      stat=f"{n_md:,} md files, {n_bytes:,} bytes, {len(cen):,} claim units",
                      bar="> 700 files, > 0 units", passed=bool(g7)))
    # G8 -- RE-SPECIFIED AFTER ITS FIRST CUT, STATED NOT HIDDEN.  The first formulation was a flat
    # "mean null-vs-book name overlap < 0.50" and FAILED at 0.5749, but that is not degeneracy: on
    # U56 the TOP20 book holds 20 of a ~28-name eligible pool, so a UNIFORM draw is *supposed* to
    # overlap ~0.70.  A flat bar would condemn idea 931's own accepted construction.  The object
    # the gate actually needs is (a) UNIFORMITY -- the observed overlap equals the hypergeometric
    # expectation E[k/|P|] -- and (b) NON-DEGENERACY -- that expectation is itself below 1, which
    # is exactly what rules out an equal-weight-everything template where the draw must take the
    # whole pool and the "null" IS the book.
    d_unif = max(abs(o - e) for o, e in ovl)
    e_max = max(e for _, e in ovl)
    gates.append(dict(gate="G8 the draw is UNIFORM and NON-DEGENERATE (overlap vs hypergeometric E[k/|P|])",
                      stat=f"max |observed - E| {d_unif:.4f} over {len(ovl)} cells; max E {e_max:.4f}",
                      bar="|d| < 0.02 / E < 0.95", passed=d_unif < 0.02 and e_max < 0.95))

    # ------------------------------------------------------- the null gain grid (and G3 with it)
    P("\n  building the null gain grid: "
      f"{len(PANELS)} panels x {len(TEMPLATES)} templates x {len(FREQS)} cadences x {NDRAW} draws ...")
    null_rows, book_rows = [], []
    for pn in PANELS:
        for tm in TEMPLATES:
            # book, all cadences, all rungs
            bpaths = {}
            for f in FREQS:
                c = ctx[(pn, tm, f)]
                gr, tu = c["book"].paths(GROSS)
                bpaths[f] = (gr, tu, c["pan"])
                yrs = c["pan"].masks["FULL"].sum() / 252.0
                for cost in COSTS:
                    m = pack(gr - tu * cost / 1e4, c["pan"])
                    book_rows.append(dict(panel=pn, template=tm, freq=f, cost_bps=cost,
                                          ann_turnover=float(tu[c["pan"].masks["FULL"]].sum() / yrs), **m))
            # nulls
            for f in FREQS:
                c = ctx[(pn, tm, f)]
                pan, pool, kc = c["pan"], c["pool"], c["kc"]
                yrs = pan.masks["FULL"].sum() / 252.0
                for d in range(NDRAW):
                    rng = np.random.default_rng(SEED0 + 1009 * FREQS.index(f)
                                                + 7919 * TEMPLATES.index(tm)
                                                + 104729 * PANELS.index(pn) + d)
                    nb = Book(pan, null_w1(pool, kc, pan.dec, rng))
                    gr, tu = nb.paths(GROSS)
                    at = float(tu[pan.masks["FULL"]].sum() / yrs)
                    for cost in COSTS:
                        m = pack(gr - tu * cost / 1e4, pan)
                        null_rows.append(dict(panel=pn, template=tm, freq=f, draw=d, cost_bps=cost,
                                              ann_turnover=at, Sharpe=m["Sharpe"], CAGR=m["CAGR"],
                                              MaxDD=m["MaxDD"], iSharpe=m["iSharpe"],
                                              oSharpe=m["oSharpe"], oCAGR=m["oCAGR"], oMaxDD=m["oMaxDD"]))
                P(f"    {pn}/{tm}/{f}: {NDRAW} draws done  ({time.time()-t0:6.1f}s)")
    BK = pd.DataFrame(book_rows)
    NL = pd.DataFrame(null_rows)

    # ---- the GAIN table: book gain, null median gain, excess, percentile -- per cadence STEP
    gain_rows = []
    for pn in PANELS:
        for tm in TEMPLATES:
            for (f0, f1) in STEPS:
                for cost in COSTS:
                    b0 = BK[(BK.panel == pn) & (BK.template == tm) & (BK.freq == f0) & (BK.cost_bps == cost)].iloc[0]
                    b1 = BK[(BK.panel == pn) & (BK.template == tm) & (BK.freq == f1) & (BK.cost_bps == cost)].iloc[0]
                    n0 = NL[(NL.panel == pn) & (NL.template == tm) & (NL.freq == f0) & (NL.cost_bps == cost)].sort_values("draw")
                    n1 = NL[(NL.panel == pn) & (NL.template == tm) & (NL.freq == f1) & (NL.cost_bps == cost)].sort_values("draw")
                    ng = n1.Sharpe.values - n0.Sharpe.values          # paired by draw index
                    ngo = n1.oSharpe.values - n0.oSharpe.values
                    bg = float(b1.Sharpe - b0.Sharpe)
                    bgo = float(b1.oSharpe - b0.oSharpe)
                    pct = float((ng < bg).mean() * 100.0)
                    pct_h = float((ng[:HALF] < bg).mean() * 100.0)
                    gain_rows.append(dict(
                        panel=pn, template=tm, step=f"{f0}->{f1}", cost_bps=cost,
                        book_gain=bg, null_med_gain=float(np.median(ng)), null_p95=float(np.percentile(ng, 95)),
                        null_sd=float(ng.std(ddof=1)), n_draw=len(ng),
                        excess=bg - float(np.median(ng)), book_pctile=pct, book_pctile_half=pct_h,
                        book_beats_null=bool(bg > float(np.median(ng))),
                        book_gain_OOS=bgo, null_med_gain_OOS=float(np.median(ngo)),
                        excess_OOS=bgo - float(np.median(ngo)),
                        book_turn_drop=float(BK[(BK.panel == pn) & (BK.template == tm) & (BK.freq == f0) & (BK.cost_bps == cost)].ann_turnover.iloc[0]
                                             - BK[(BK.panel == pn) & (BK.template == tm) & (BK.freq == f1) & (BK.cost_bps == cost)].ann_turnover.iloc[0]),
                    ))
    GN = pd.DataFrame(gain_rows)

    # G3 CROSS-RUN against idea 931's published U56 TOP20 W->M numbers
    g3 = GN[(GN.panel == "U56") & (GN.template == "TOP20") & (GN.step == "W->M")].sort_values("cost_bps")
    db = [abs(float(g3[g3.cost_bps == c].book_gain.iloc[0]) - p) for c, p in zip(COSTS, PUB_BOOK_GAIN)]
    dn = [abs(float(g3[g3.cost_bps == c].null_med_gain.iloc[0]) - p) for c, p in zip(COSTS, PUB_NULL_GAIN)]
    gates.append(dict(gate="G3 CROSS-RUN vs idea 931's published U56/TOP20 W->M book and NULL MEDIAN gains",
                      stat="book d " + "/".join(f"{x:.4f}" for x in db) + " | null d " + "/".join(f"{x:.4f}" for x in dn),
                      bar=f"{TOL_GAIN}", passed=max(db + dn) < TOL_GAIN))

    GT = pd.DataFrame(gates)
    P(GT.to_string(index=False))
    P(f"\n  GATES: {int(GT.passed.sum())} of {len(GT)} PASS")
    dump(GT, "gates.csv")
    dump(BK, "books.csv")
    dump(NL, "null.csv")
    dump(GN, "gain.csv")

    P("\n  THE GAIN TABLE at PROTOCOL's own 10 bps (book gain vs the null's median gain):")
    P(GN[GN.cost_bps == COST0][["panel", "template", "step", "book_gain", "null_med_gain", "excess",
                                "book_pctile", "book_turn_drop"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\n  THE SAME TABLE, ALL FOUR RUNGS (every grid point, nothing withheld):")
    P(GN[["panel", "template", "step", "cost_bps", "book_gain", "null_med_gain", "excess", "book_pctile",
          "excess_OOS"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ============================================================================ PART C: RULE 8
    P("\n" + "=" * 100)
    P("PART C -- RULE 8 WALK-FORWARD: cadence chosen on 2009-2016 ALONE, 2017-2026 read ONCE")
    P("=" * 100)
    wf_rows = []
    for pn in PANELS:
        px = raw[pn]
        pan_ref = ctx[(pn, "TOP20", "W")]["pan"]
        spy_pack = pack(pan_ref.spy, pan_ref)
        v2 = backtest(px, rules_v2_weights(px), cost_bps=COST0, freq="W")["returns"].values
        v2_pack = pack(v2, pan_ref)
        for tm in TEMPLATES:
            for cost in COSTS:
                sub = BK[(BK.panel == pn) & (BK.template == tm) & (BK.cost_bps == cost)]
                pick = sub.loc[sub.iSharpe.idxmax()]
                # the same chooser applied to the null, draw by draw
                nsub = NL[(NL.panel == pn) & (NL.template == tm) & (NL.cost_bps == cost)]
                piv_is = nsub.pivot(index="draw", columns="freq", values="iSharpe")[FREQS]
                piv_oo = nsub.pivot(index="draw", columns="freq", values="oSharpe")[FREQS]
                nf = piv_is.values.argmax(axis=1)
                n_oos_pick = piv_oo.values[np.arange(len(nf)), nf]
                n_oos_W = piv_oo["W"].values
                s = dict(CAGR=pick.CAGR, Sharpe=pick.Sharpe, MaxDD=pick.MaxDD, H1=pick.H1, H2=pick.H2,
                         oSharpe=pick.oSharpe)
                L = legs4b(s, spy_pack)
                keep4a = bool(pick.H1 > v2_pack["H1"] and pick.H2 > v2_pack["H2"] and pick.MaxDD >= v2_pack["MaxDD"])
                # the OOS null-differenced gain of the CHOSEN cadence over W (the record's old default)
                b_gain_oos = float(pick.oSharpe - sub[sub.freq == "W"].oSharpe.iloc[0])
                n_gain_oos = float(np.median(n_oos_pick - n_oos_W))
                wf_rows.append(dict(panel=pn, template=tm, cost_bps=cost, IS_pick=pick.freq,
                                    null_pick_mode=FREQS[int(np.bincount(nf, minlength=4).argmax())],
                                    null_pick_share=float(np.bincount(nf, minlength=4).max() / len(nf)),
                                    OOS_CAGR=pick.oCAGR, OOS_Sharpe=pick.oSharpe, OOS_MaxDD=pick.oMaxDD,
                                    SPY_OOS_CAGR=spy_pack["oCAGR"], SPY_OOS_Sharpe=spy_pack["oSharpe"],
                                    SPY_OOS_MaxDD=spy_pack["oMaxDD"],
                                    V2_OOS_CAGR=v2_pack["oCAGR"], V2_OOS_Sharpe=v2_pack["oSharpe"],
                                    V2_OOS_MaxDD=v2_pack["oMaxDD"],
                                    pass4b=L["pass4b"], pass4a=keep4a, **{k: v for k, v in L.items() if k != "pass4b"},
                                    OOS_gain_vs_W=b_gain_oos, OOS_null_med_gain_vs_W=n_gain_oos,
                                    OOS_excess=b_gain_oos - n_gain_oos))
    WF = pd.DataFrame(wf_rows)
    P(WF[["panel", "template", "cost_bps", "IS_pick", "null_pick_mode", "null_pick_share", "OOS_CAGR",
          "OOS_Sharpe", "OOS_MaxDD", "pass4b", "pass4a", "OOS_gain_vs_W", "OOS_null_med_gain_vs_W",
          "OOS_excess"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  OOS 4b {int(WF.pass4b.sum())} of {len(WF)}; 4a {int(WF.pass4a.sum())} of {len(WF)}")
    P(f"  OOS bars: SPY {WF.SPY_OOS_CAGR.iloc[0]:.2%} / {WF.SPY_OOS_Sharpe.iloc[0]:.3f} / {WF.SPY_OOS_MaxDD.iloc[0]:.2%}"
      f"   RULES v2 {WF.V2_OOS_CAGR.iloc[0]:.2%} / {WF.V2_OOS_Sharpe.iloc[0]:.3f} / {WF.V2_OOS_MaxDD.iloc[0]:.2%}")
    P(f"  OOS excess over the null's own cadence gain: positive on {int((WF.OOS_excess > 0).sum())} of {len(WF)} cells")
    dump(WF, "walkforward.csv")

    # ================================================================== PART D: the re-score map
    P("\n" + "=" * 100)
    P("PART D -- RE-SCORE: what the un-priced claims did not subtract")
    P("=" * 100)
    resc = []
    for cs in ("STRICT", "WIDE"):
        sub = cen[cen["in_STRICT"]] if cs == "STRICT" else cen
        unp = sub[sub.null_class != "N2_NULL_GAIN_PRICED"]
        for cost in COSTS:
            g = GN[GN.cost_bps == cost]
            resc.append(dict(claim_set=cs, cost_bps=cost, n_claims=len(sub), n_unpriced=len(unp),
                             share_unpriced=len(unp) / len(sub),
                             null_med_gain_min=float(g.null_med_gain.min()),
                             null_med_gain_median=float(g.null_med_gain.median()),
                             null_med_gain_max=float(g.null_med_gain.max()),
                             cells_null_gain_pos=int((g.null_med_gain > 0).sum()), n_cells=len(g),
                             cells_book_beats_null=int(g.book_beats_null.sum()),
                             share_book_beats_null=float(g.book_beats_null.mean())))
    RS = pd.DataFrame(resc)
    P(RS.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(RS, "rescore.csv")

    # ===================================================================== pre-registered bars
    P("\n" + "=" * 100)
    P("PRE-REGISTERED BARS")
    P("=" * 100)
    n2_tot = int((cen.null_class == "N2_NULL_GAIN_PRICED").sum())
    h_census = n2_tot > 0
    g10 = GN[GN.cost_bps == COST0]
    h_rebate = bool((g10.null_med_gain > 0).all())
    share_exc = float(g10.book_beats_null.mean())
    h_excess = share_exc >= EXCESS_BAR
    a0 = GN[GN.cost_bps == 0.0].set_index(["panel", "template", "step"]).book_beats_null
    a10 = GN[GN.cost_bps == COST0].set_index(["panel", "template", "step"]).book_beats_null
    agree = float((a0 == a10.reindex(a0.index)).mean())
    h_rung = agree >= RUNG_BAR
    sh_s = float(CEN_H[(CEN_H.claim_set == "STRICT") & (CEN_H.source == "ALL")].share_gain_priced.iloc[0]) * 100
    sh_w = float(CEN_H[(CEN_H.claim_set == "WIDE") & (CEN_H.source == "ALL")].share_gain_priced.iloc[0]) * 100
    h_claim = abs(sh_s - sh_w) <= CLAIM_BAR
    h_wf = bool(WF.pass4b.any() or WF.pass4a.any())
    hyp = pd.DataFrame([
        dict(bar="H_CENSUS  >=1 committed claim prices its null's GAIN",
             stat=f"{n2_tot} of {len(cen)} claim units (WIDE); {int(cen[cen.in_STRICT].null_class.eq('N2_NULL_GAIN_PRICED').sum())} of {int(cen.in_STRICT.sum())} STRICT",
             verdict="PASS" if h_census else "FAIL"),
        dict(bar="H_REBATE  null median gain > 0 on EVERY cell at 10 bps",
             stat=f"{int((g10.null_med_gain > 0).sum())} of {len(g10)} cells; min {g10.null_med_gain.min():.4f}",
             verdict="PASS" if h_rebate else "FAIL"),
        dict(bar=f"H_EXCESS  book gain > null median on >= {EXCESS_BAR:.0%} of cells at 10 bps",
             stat=f"{int(g10.book_beats_null.sum())} of {len(g10)} = {share_exc:.4f}",
             verdict="PASS" if h_excess else "FAIL"),
        dict(bar=f"H_RUNG    0 bps and 10 bps verdicts agree on >= {RUNG_BAR:.0%} of cells",
             stat=f"{agree:.4f}", verdict="PASS" if h_rung else "FAIL"),
        dict(bar=f"H_CLAIM   census headline moves <= {CLAIM_BAR:.0f} pp between claim sets",
             stat=f"STRICT {sh_s:.2f}% vs WIDE {sh_w:.2f}% = {abs(sh_s-sh_w):.2f} pp",
             verdict="PASS" if h_claim else "FAIL"),
        dict(bar="H_WF      rule 8: any IS-only cadence pick clears 4a or 4b OOS",
             stat=f"4b {int(WF.pass4b.sum())} of {len(WF)}, 4a {int(WF.pass4a.sum())} of {len(WF)}",
             verdict="PASS" if h_wf else "FAIL"),
    ])
    P(hyp.to_string(index=False))
    dump(hyp, "hypotheses.csv")

    P("\n" + "=" * 100)
    P(f"DONE in {time.time()-t0:.1f}s")
    P("=" * 100)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
