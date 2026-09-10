#!/usr/bin/env python3
"""Idea 649 — is EVERY published CHOOSER WIN in the record a PHASE WIN?   (lane C, 2026-09-10)

QUEUE 649: "idea 624 found that `phase` (rebalance weekday), a dial whose target weights are
IDENTICAL at every rung (JAC=WGT=EXP=0, gated), still hands its rule-8 chooser +0.108 OOS Sharpe on
u56 and +0.188 on small439 against its own default.  Take the record's committed chooser-vs-control
wins and price each one against a NULL DIAL of this kind — a ladder that cannot change the book at
all — to get a per-panel noise floor for 'the pick beat the control'.  Max 2 params (null dial,
panel)."

WHAT IS RUN
  A rule-8 chooser picks the rung with the best IS Sharpe (2009-2016) and is then read OUT OF SAMPLE
  (2017-2026) against its ladder's own default rung.  The published statistic everywhere in this
  record is d = OOS_Sharpe(pick) - OOS_Sharpe(control).  The question is what d looks like when the
  ladder CANNOT CARRY INFORMATION, because that is the bar every committed d must clear.

  A NULL DIAL here is a ladder whose rungs are EXCHANGEABLE BY CONSTRUCTION: nothing about a rung's
  construction makes it a priori better than another, so any d it produces is selection noise.  Three
  families are built (P1), each null in a different way, all three reported:

    PHASE  rebalance weekday {W, MON, TUE, WED, THU, FRI}.  The record's own dial, and idea 624's
           warning case.  TARGET weights are byte-identical at every rung — only the day the same
           target is applied moves.  Null by construction, gated (G5).  NOTE the rung 'W' is the
           engine's own calendar mask (LAST TRADING DAY of each week, so a Thursday in a holiday
           week and never a skipped week) and is therefore NOT exactly exchangeable with the five
           weekday rungs; FRI is added here so the family contains a clean 5-way exchangeable set,
           and the asymmetry of 'W' is reported rather than assumed away.
    JIT    the record's real composite plus informationless uniform tie-break jitter, seed = rung,
           32 rungs.  The BOOK is real (a momentum book with the record's turnover); the LADDER is
           null: every rung including the control carries the same jitter magnitude, only the seed
           differs.  This is "a null ladder on a real book".
    PERM   the record's composite with its NAME LABELS permuted, seed = rung, 32 rungs.  Score
           dynamics, cross-sectional dispersion and therefore turnover character are preserved
           exactly; the name->score link is destroyed.  Every rung is a distinct non-identity
           permutation, so the control is exchangeable with the alternatives too.  This is "a null
           ladder on a null book".  The IDENTITY permutation — the record's real book — is never a
           rung, so no rung of this family carries any name->score information at all.

  LADDER LENGTH is not a tuned parameter but a REPORTED axis: the floor is a function of how many
  rungs the chooser gets to pick from, and the record's ladders run 3-8 rungs.  For each length L the
  default rung plus L-1 alternatives are drawn from the family's rungs and d is recomputed, so the
  floor is quoted at the length of the claim it is pricing.

AXES (PROTOCOL 4: no more than 2 tuned parameters — the queue names them)
  P1 NULL DIAL   {PHASE, JIT, PERM}.  All three reported; none selected on.
  P2 PANEL       {u56, broad136, small439}.  All three reported; none selected on.
  Cost rungs {0,10,25,50} bps and ladder length L in {3,4,5,6,8} are reported axes, never selected
  on.  The only selection anywhere in this file is PROTOCOL rule 8 itself, which is the object of
  study.

PARTS
  A  CENSUS of the record's committed chooser-vs-control pairs: every research/backtests/*.csv that
     publishes a chooser's OOS Sharpe beside a same-file control's OOS Sharpe.  Every extracted d is
     reported; the panel label is taken from the file's own panel/universe column where it has one.
  B  The null ladders themselves: the full grid (every rung, every cost rung, both KEEP paths), the
     rule-8 chooser on every (panel, family, cost) cell, and the floor as a function of L.
  B2 WHY a null ladder pays at all: the IS->OOS rank persistence of the null rungs, split-half.
  C  PRICING: each committed d from PART A against its own panel's floor at matched L.

GATES (run before any new number is read)
  G1 the vectorised segment runner vs `engine.backtest` on returns AND turnover, all panels.
  G2 the cost-rung identity r(c) = r(0) - turnover*c/1e4 vs a live engine.backtest(cost_bps=25).
  G3 the DEFAULT rung is IN the ladder of every family (a control the grid cannot express is not one).
  G4 the IS and OOS windows are disjoint and jointly exhaust the evaluated sample.
  G5 NULLITY, by construction not assertion:
       PHASE  target distance from the default is EXACTLY 0 on all three legs (JAC=WGT=EXP=0).
       JIT    every rung carries the same jitter magnitude (the ladder is exchangeable); the
              realised membership distance from the control is REPORTED, not asserted to be 0.
       PERM   no rung uses the identity permutation, and the permuted composite's per-day
              cross-sectional distribution is identical to the real one (sorted values match).
  G6 REPLICATION: idea 624's phase numbers (+0.108 u56, +0.188 small439, DEFAULT control, 10 bps) are
     re-derived here from this file's own grid, not restated from 624's prose.

CAVEATS CARRIED
  * SURVIVORSHIP (idea 54): all three panels are CURRENT constituents.  SMALL439 additionally drops
    every ticker with max_1d_move >= 1.0 in data/small_meta.csv; its levels are not investable
    history and only WITHIN-panel arm-minus-arm contrasts are read from it.
  * Warm-up is px.index[300] (idea 624's bar, not the record's [260]) so every arm in this file and
    in 624 starts on the same day and G6 is a like-for-like replication.
  * Idea 534: PART A classifies by a FILE's published columns, not by a claim's prose.  A file may
    publish many d's, and rows are the unit — the file count is reported beside the row count.
  * PART A reads what the record COMMITTED.  Those d's were produced at each file's own warm-up,
    cost rung, window split and panel definition; they are not re-run here.  The floor is therefore
    an approximate bar, and the comparison is reported as such.
  * Idea 321: MaxDD is one number off one path.  Idea 126: t+1 execution, 10 bps default rung.
  * Idea 412: cadence has a phase; here phase is the dial, not a nuisance held fixed.
  * Ideas 527/531: 4b is in practice a DD-cap test on ungated momentum books; both KEEP paths are
    priced on every arm anyway, as PROTOCOL requires.
  * PERM books have no momentum tilt by construction.  Their LEVELS are not a proposal; only the
    chooser-minus-control contrast inside the family is read.

Deterministic, standalone.  Modifies nothing outside its own output files.
Writes .console.txt, .census.csv.gz, .grid.csv, .wf.csv, .floor.csv, .priced.csv.
The census is written GZIPPED on purpose: it carries 38,150 rows with a `d` column, and a plain
.csv in this directory would be picked up (and double-counted) by the next run of any census that
scans research/backtests/*.csv — including this one.
"""
from __future__ import annotations

import itertools
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
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-10_is-EVERY-published-CHOOSER-WIN-in-the-record-a-PHASE-WIN_C"
OUT = ROOT / "research" / "backtests"

IS_END, OOS_START = "2016-12-31", "2017-01-01"
PHI, DELTA = 0.70, 0.60            # 4b CAGR floor and MaxDD cap, as fractions of SPY's
PCOST = 10.0                       # PROTOCOL's own rung
RUNGS = [0.0, 10.0, 25.0, 50.0]    # reported cost ladder
CELL_RUNGS = [10.0, 25.0]          # the two rungs the headline cells are cut on (idea 621's pair)
WARM = 300                         # common warm-up bar, idea 624's

NBOOK, GROSS = 20, 0.75            # the book every family holds: top-20 EW at gross 0.75
KNULL = 32                         # rungs in the seeded null families
JIT_SIGMA = 0.02                   # jitter as a fraction of the composite's [0,1] rank range
LLADDER = [3, 4, 5, 6, 8]          # reported ladder lengths
NDRAW = 400                        # rung subsets sampled per (panel, family, cost, L)
DRAW_SEED = 6490

PANELS = ["u56", "broad136", "small439"]
FAMILIES = ["PHASE", "JIT", "PERM"]
LADDERS: dict[str, list] = {
    "PHASE": ["W", "MON", "TUE", "WED", "THU", "FRI"],
    "JIT": list(range(KNULL)),
    "PERM": list(range(KNULL)),
}
DEFAULTS = {"PHASE": "W", "JIT": 0, "PERM": 0}

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 4000)
LOG: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# =====================================================================================
# runner (idea 613/621/624's segment form; gated against engine.backtest below)
# =====================================================================================
def mask_of(idx, phase):
    """Rebalance mask, shifted the way engine.backtest shifts it.  'D'/'W'/'M'/'Q' are the record's
    calendar conventions; MON..THU rebalance on that weekday (the PHASE dial)."""
    if phase in ("D", "W", "M", "Q"):
        return rebalance_mask(idx, phase).shift(1, fill_value=False).values
    wd = {"MON": 0, "TUE": 1, "WED": 2, "THU": 3, "FRI": 4}[phase]
    return pd.Series(idx.weekday == wd, index=idx).shift(1, fill_value=False).values


def fast_bt(rets, w_t, mask):
    """engine.backtest's drift algebra, one pass per rebalance SEGMENT."""
    n = len(rets)
    reb = np.unique(np.concatenate(([0], np.flatnonzero(mask))))
    port = np.zeros(n)
    turn = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    for si, i0 in enumerate(reb):
        i1 = reb[si + 1] if si + 1 < len(reb) else n
        if i1 <= i0:
            continue
        new = w_t[i0]
        turn[i0] = np.abs(new - cur).sum()
        A = new[None, :] * np.cumprod(1.0 + rets[i0:i1], axis=0)
        S = A.sum(axis=1) + (1.0 - new.sum())
        port[i0:i1] = S / np.concatenate(([1.0], S[:-1])) - 1.0
        cur = A[-1] / S[-1]
    return port, turn


def run(px, W, phase):
    rets = px.pct_change().fillna(0.0).values
    w_t = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    p, t = fast_bt(rets, w_t, mask_of(px.index, phase))
    return pd.Series(p, index=px.index), pd.Series(t, index=px.index)


# =====================================================================================
# panels and the book
# =====================================================================================
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad & set(px.columns))


def comp_rec(sub):
    """The record's own composite (scan.py / baseline.score, no vol scaler)."""
    mom = sub.shift(21) / sub.shift(252) - 1
    r6, r3 = sub / sub.shift(126) - 1, sub / sub.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


class Panel:
    def __init__(self, key):
        if key == "u56":
            px, self.ndrop = load_universe(), 0
        elif key == "broad136":
            px, self.ndrop = load_universe(broad=True), 0
        else:
            px, self.ndrop = small_panel()
        self.key = key
        self.px = px.dropna(how="all").ffill()
        self.sub = self.px.drop(columns=["SPY"], errors="ignore")
        self.v20 = self.sub.pct_change().rolling(20).std() * np.sqrt(252)
        self.start = self.px.index[WARM]
        self.comp = comp_rec(self.sub)


def _book_from_score(c, v20):
    """Top-NBOOK of a score, equal weighted at GROSS.  vol cap 0.60 (the record's default)."""
    c = c.where(v20 < 0.60)
    sel = c.rank(axis=1, ascending=False) <= NBOOK
    raw = sel.astype(float)
    tot = raw.sum(axis=1).replace(0, np.nan)
    return (GROSS * raw.div(tot, axis=0)).fillna(0.0)


def score_of(panel: Panel, family: str, value):
    """The composite a rung ranks on.  PHASE never touches it."""
    if family == "PHASE":
        return panel.comp
    if family == "JIT":
        rng = np.random.default_rng(1000 + int(value))
        eps = rng.uniform(-JIT_SIGMA, JIT_SIGMA, size=panel.comp.shape)
        return panel.comp + eps
    rng = np.random.default_rng(2000 + int(value))
    cols = list(panel.comp.columns)
    perm = list(rng.permutation(len(cols)))
    while all(perm[i] == i for i in range(len(cols))):        # never the identity
        perm = list(rng.permutation(len(cols)))
    out = panel.comp.copy()
    out.columns = [cols[i] for i in perm]                     # relabel: name i wears name perm(i)'s score
    return out.reindex(columns=cols)


def arm(panel: Panel, family: str, value):
    """(target weights, rebalance phase) for one rung."""
    if family == "PHASE":
        return _book_from_score(panel.comp, panel.v20), str(value)
    return _book_from_score(score_of(panel, family, value), panel.v20), "W"


# =====================================================================================
# metrics helpers
# =====================================================================================
def sh(r):
    return metrics(r)["Sharpe"]


def halves(r):
    h = len(r) // 2
    return sh(r.iloc[:h]), sh(r.iloc[h:])


def bars_of(spy):
    h1, h2 = halves(spy)
    m = metrics(spy)
    return dict(s1=h1, s2=h2, sdd=m["MaxDD"], scagr=m["CAGR"], soos=sh(spy.loc[OOS_START:]),
                spy_oos=spy.loc[OOS_START:])


def pass4b(r, b, window="full"):
    if window == "full":
        h1, h2 = halves(r)
        m = metrics(r)
        return bool(h1 > b["s1"] and h2 > b["s2"] and sh(r.loc[OOS_START:]) > b["soos"]
                    and abs(m["MaxDD"]) <= DELTA * abs(b["sdd"]) and m["CAGR"] >= PHI * b["scagr"])
    x = r.loc[OOS_START:]
    h1, h2 = halves(x)
    m = metrics(x)
    sp = b["spy_oos"]
    o1, o2 = halves(sp)
    mo = metrics(sp)
    return bool(h1 > o1 and h2 > o2 and abs(m["MaxDD"]) <= DELTA * abs(mo["MaxDD"])
                and m["CAGR"] >= PHI * mo["CAGR"])


def pass4a(r, base, window="full"):
    x, y = (r, base) if window == "full" else (r.loc[OOS_START:], base.loc[OOS_START:])
    h1, h2 = halves(x)
    b1, b2 = halves(y)
    return bool(h1 > b1 and h2 > b2 and metrics(x)["MaxDD"] >= metrics(y)["MaxDD"])


def spearman(x, y):
    x, y = pd.Series(list(x)), pd.Series(list(y))
    m = x.notna() & y.notna()
    if m.sum() < 3:
        return float("nan")
    return float(x[m].rank().corr(y[m].rank()))


def sign_p(k, n):
    """Two-sided exact binomial p at 0.5."""
    from math import comb
    if n == 0:
        return float("nan")
    tail = [comb(n, i) for i in range(n + 1)]
    tot = float(sum(tail))
    obs = tail[k]
    return float(sum(t for t in tail if t <= obs * (1 + 1e-12)) / tot)


# =====================================================================================
# PART A — census of the record's committed chooser-vs-control pairs
# =====================================================================================
PICK_COLS = ["OOS_Sharpe", "oos_sh_pick", "OOS_Sh", "OOS_Sharpe_ISpick", "oos_OOS_Sharpe",
             "S1_OOS_Sharpe", "pick_OOS_Sharpe", "oos_sharpe_pick"]
CTL_COLS = ["ctl_OOS_Sharpe", "anchor_OOS_Sharpe", "OOS_Sharpe_anchor", "anch_OOS_Sharpe",
            "CTL_OOS_Sharpe", "oos_sh_ctl", "ctl_Sharpe", "anchor_OOS", "ctl_OOS",
            "default_OOS_Sharpe", "anchor_oos_sharpe", "OOS_ctl", "oos_ctl", "ctl_OOS_Sh"]
DELTA_COLS = ["d_sharpe", "dOOS_vs_anchor", "d_vs_ctl", "dOOS", "d_ctl"]
PANEL_COLS = ["panel", "universe", "uni", "book_panel"]


def _panel_label(v):
    s = str(v).strip().lower()
    if not s or s in ("nan", "none"):
        return "UNLABELLED"
    if "small" in s:
        return "small439"
    if "broad" in s or "b136" in s or s.startswith("b1"):
        return "broad136"
    if "u56" in s or s in ("u", "core", "universe", "rules", "main") or "56" in s:
        return "u56"
    return "OTHER:" + s[:16]


def census():
    """Every research/backtests/*.csv that publishes a chooser's OOS Sharpe beside a same-file
    control's OOS Sharpe (or a published delta directly).  Rows are the unit; the file count is
    reported beside it.  Reported as an UPPER BOUND on the record's committed chooser wins: a file
    whose control column is named something this reader does not know is missed, not faked."""
    rows = []
    files = sorted(p for p in OUT.iterdir() if p.suffix == ".csv")
    seen_files = 0
    for p in files:
        if p.name.startswith(STEM):
            continue
        try:
            head = p.open(errors="ignore").readline().strip().split(",")
        except Exception:
            continue
        pick = next((c for c in PICK_COLS if c in head), None)
        ctl = next((c for c in CTL_COLS if c in head), None)
        dcol = next((c for c in DELTA_COLS if c in head), None)
        if not ((pick and ctl) or dcol):
            continue
        if p.stat().st_size > 40_000_000:
            continue
        try:
            df = pd.read_csv(p, low_memory=False)
        except Exception:
            continue
        pcol = next((c for c in PANEL_COLS if c in df.columns), None)
        if dcol and dcol in df.columns:
            d = pd.to_numeric(df[dcol], errors="coerce")
            src, strict = f"delta:{dcol}", ("OOS" in dcol.upper())
            u = set(pd.unique(d.dropna()))
            if u and u <= {0.0, 1.0}:            # a boolean 'did it win' column, not a delta
                continue
        else:
            d = pd.to_numeric(df[pick], errors="coerce") - pd.to_numeric(df[ctl], errors="coerce")
            src = f"{pick}-{ctl}"
            strict = ("OOS" in pick.upper()) and ("OOS" in ctl.upper())
        d = d.replace([np.inf, -np.inf], np.nan)
        lab = df[pcol].map(_panel_label) if pcol else pd.Series(["UNLABELLED"] * len(df))
        ok = d.notna()
        if not ok.any():
            continue
        seen_files += 1
        for i in np.flatnonzero(ok.values):
            rows.append(dict(file=p.name, source=src, strict=bool(strict),
                             panel=lab.iloc[i], d=float(d.iloc[i])))
    C = pd.DataFrame(rows)
    return C, seen_files


# =====================================================================================
# PART B — the null grid
# =====================================================================================
def grid_rows(panel: Panel, family: str, b, baser):
    px, start = panel.px, panel.start
    out, rets = [], {}
    for v in LADDERS[family]:
        W, phase = arm(panel, family, v)
        r0, to = run(px, W.reindex(columns=px.columns).fillna(0.0), phase)
        r0, to = r0.loc[start:], to.loc[start:]
        rec = dict(panel=panel.key, family=family, value=str(v),
                   is_default=(v == DEFAULTS[family]),
                   turnover=float(to.sum() / (len(to) / 252.0)))
        for c in RUNGS:
            r = r0 - to * c / 1e4
            m, mo = metrics(r), metrics(r.loc[OOS_START:])
            h1, h2 = halves(r)
            rec[f"sh_full_{c:g}"] = m["Sharpe"]
            rec[f"cagr_full_{c:g}"] = m["CAGR"]
            rec[f"dd_full_{c:g}"] = m["MaxDD"]
            rec[f"h1_{c:g}"], rec[f"h2_{c:g}"] = h1, h2
            rec[f"sh_is_{c:g}"] = sh(r.loc[:IS_END])
            rec[f"sh_isa_{c:g}"] = sh(r.loc[:"2012-12-31"])           # IS first half (part B2)
            rec[f"sh_isb_{c:g}"] = sh(r.loc["2013-01-01":IS_END])     # IS second half (part B2)
            rec[f"sh_oos_{c:g}"] = mo["Sharpe"]
            rec[f"cagr_oos_{c:g}"] = mo["CAGR"]
            rec[f"dd_oos_{c:g}"] = mo["MaxDD"]
            if c == PCOST:
                rec["p4a_full"] = pass4a(r, baser)
                rec["p4b_full"] = pass4b(r, b, "full")
                rec["p4a_oos"] = pass4a(r, baser, "oos")
                rec["p4b_oos"] = pass4b(r, b, "oos")
        out.append(rec)
        rets[str(v)] = (r0, to)
    return out, rets


def wf_cells(G):
    """PROTOCOL 8 on the FULL ladder of every (panel, family, cost) cell: pick = best IS Sharpe,
    read OOS against the ladder's own default rung."""
    rows = []
    for pk in PANELS:
        for fam in FAMILIES:
            g0 = G[(G.panel == pk) & (G.family == fam)]
            if g0.empty:
                continue
            for c in CELL_RUNGS:
                g = g0.set_index("value").loc[[str(v) for v in LADDERS[fam]]]
                pick = g[f"sh_is_{c:g}"].idxmax()
                oracle = g[f"sh_oos_{c:g}"].idxmax()
                ctl = str(DEFAULTS[fam])
                rows.append(dict(
                    panel=pk, family=fam, cost=c, L=len(LADDERS[fam]), pick=pick, control=ctl,
                    oracle=oracle,
                    is_sh_pick=g.loc[pick, f"sh_is_{c:g}"], is_sh_ctl=g.loc[ctl, f"sh_is_{c:g}"],
                    oos_sh_pick=g.loc[pick, f"sh_oos_{c:g}"], oos_sh_ctl=g.loc[ctl, f"sh_oos_{c:g}"],
                    oos_cagr_pick=g.loc[pick, f"cagr_oos_{c:g}"],
                    oos_cagr_ctl=g.loc[ctl, f"cagr_oos_{c:g}"],
                    oos_dd_pick=g.loc[pick, f"dd_oos_{c:g}"], oos_dd_ctl=g.loc[ctl, f"dd_oos_{c:g}"],
                    d_sharpe=g.loc[pick, f"sh_oos_{c:g}"] - g.loc[ctl, f"sh_oos_{c:g}"],
                    d_cagr=g.loc[pick, f"cagr_oos_{c:g}"] - g.loc[ctl, f"cagr_oos_{c:g}"],
                    regret=g.loc[oracle, f"sh_oos_{c:g}"] - g.loc[pick, f"sh_oos_{c:g}"],
                    pick_is_control=(pick == ctl),
                    p4b_pick=bool(g.loc[pick, "p4b_full"]), p4b_ctl=bool(g.loc[ctl, "p4b_full"]),
                    p4a_pick=bool(g.loc[pick, "p4a_full"]), p4a_ctl=bool(g.loc[ctl, "p4a_full"]),
                ))
    return pd.DataFrame(rows)


def floor_rows(G):
    """The noise floor as a function of LADDER LENGTH, in TWO control conventions.

      DEF  the control is the ladder's own DEFAULT rung, which is how the record publishes every
           chooser-vs-control number.  Draws are subsets of L rungs that CONTAIN the default.
      SYM  the control is drawn UNIFORMLY from the same L rungs.  This is the control-luck-free
           floor: under a null with no IS->OOS rung persistence its mean is 0 and its win rate 0.5
           by symmetry, so any departure is the chooser's, not the default rung's.

    The two differ by exactly one thing — whether the named default happened to be a lucky rung —
    and the gap between them is reported, because it is the part of a published chooser win that
    belongs to the CONTROL rather than to the pick.
    """
    rows, dists = [], {}
    rng = np.random.default_rng(DRAW_SEED)
    for pk in PANELS:
        for fam in FAMILIES:
            g0 = G[(G.panel == pk) & (G.family == fam)]
            if g0.empty:
                continue
            vals = [str(v) for v in LADDERS[fam]]
            ctl0 = str(DEFAULTS[fam])
            alts = [v for v in vals if v != ctl0]
            for c in CELL_RUNGS:
                g = g0.set_index("value")
                is_s = g[f"sh_is_{c:g}"]
                oo_s = g[f"sh_oos_{c:g}"]
                for L in LLADDER:
                    if L > len(vals):
                        continue
                    combos = list(itertools.combinations(alts, L - 1))
                    exact = len(combos) <= NDRAW
                    if not exact:
                        idx = rng.choice(len(alts), size=(NDRAW, L - 1))
                        combos = [tuple(alts[j] for j in set(row)) for row in idx]
                        combos = [t for t in combos if len(t) == L - 1]
                    subs = [(ctl0,) + t for t in combos]
                    ds = [float(oo_s[max(s, key=lambda v: is_s[v])] - oo_s[ctl0]) for s in subs]
                    # SYM: same subsets, every rung in turn as the control (exhaustive over controls)
                    ds_sym = []
                    for s in subs:
                        pick = max(s, key=lambda v: is_s[v])
                        ds_sym.extend(float(oo_s[pick] - oo_s[cv]) for cv in s)
                    for conv, a in (("DEF", np.array(ds)), ("SYM", np.array(ds_sym))):
                        dists[(pk, fam, c, L, conv)] = a
                        rows.append(dict(panel=pk, family=fam, cost=c, L=L, control_conv=conv,
                                         ndraw=len(a), exhaustive=exact,
                                         win_rate=float((a > 0).mean()),
                                         tie_rate=float((a == 0).mean()),
                                         mean=float(a.mean()), median=float(np.median(a)),
                                         sd=float(a.std(ddof=1)) if len(a) > 1 else np.nan,
                                         p90=float(np.percentile(a, 90)),
                                         p95=float(np.percentile(a, 95)),
                                         p99=float(np.percentile(a, 99)),
                                         mx=float(a.max())))
    return pd.DataFrame(rows), dists


# =====================================================================================
def main():
    t0 = time.time()
    say("=" * 110)
    say("IDEA 649 — is EVERY published CHOOSER WIN in the record a PHASE WIN?   (lane C 2026-09-10)")
    say("=" * 110)
    say("NULL DIAL FAMILIES (fixed before any run):")
    say(f"   PHASE  {LADDERS['PHASE']}   default {DEFAULTS['PHASE']}   "
        "(the record's own dial; TARGET identical at every rung)")
    say(f"   JIT    {KNULL} seeded rungs, jitter U(+/-{JIT_SIGMA}) on the record's composite, "
        "default seed 0   (null ladder, REAL book)")
    say(f"   PERM   {KNULL} seeded name-label permutations of the composite, default seed 0   "
        "(null ladder, NULL book)")
    say(f"   book at every rung: top-{NBOOK} EW at gross {GROSS}, vol cap 0.60, weekly, "
        f"warm-up index[{WARM}], IS<={IS_END} / OOS>={OOS_START}")

    # ---------------- PART A ----------------
    say("\nPART A — CENSUS of the record's committed chooser-vs-control pairs")
    C, nfile = census()
    if C.empty:
        say("  NO committed chooser-vs-control pairs found — PART C is not attempted (reported).")
    else:
        C.to_csv(OUT / f"{STEM}.census.csv.gz", index=False, compression="gzip")
        say(f"  files publishing a chooser AND a same-file control : {nfile}")
        say(f"  committed d rows (all)    : {len(C)}   from {C.file.nunique()} files")
        say(f"  STRICT rows (both columns name the OOS window explicitly) : "
            f"{int(C.strict.sum())} from {C[C.strict].file.nunique()} files")
        say("  the STRICT subset is the headline population; the loose rows are carried in the CSV.")
        for tag, g in (("ALL", C), ("STRICT", C[C.strict])):
            if g.empty:
                continue
            say(f"    [{tag}] wins (d>0) {int((g.d > 0).sum())}  ties {int((g.d == 0).sum())}  "
                f"losses {int((g.d < 0).sum())}   win rate {float((g.d > 0).mean()):.3f}")
            say(f"    [{tag}] d: mean {g.d.mean():+.4f}  median {g.d.median():+.4f}  "
                f"p90 {g.d.quantile(0.90):+.4f}  p95 {g.d.quantile(0.95):+.4f}  max {g.d.max():+.4f}")
        say("  STRICT rows by panel label (the file's own column, where it has one):")
        for lab, g in C[C.strict].groupby("panel"):
            if len(g) < 5:
                continue
            say(f"     {lab:<14} n={len(g):>6}  win {float((g.d > 0).mean()):.3f}  "
                f"mean {g.d.mean():+.4f}  median {g.d.median():+.4f}  p95 {g.d.quantile(.95):+.4f}")
        C = C[C.strict].reset_index(drop=True)

    # ---------------- gates 3, 4 ----------------
    say("\nGATES")
    for fam in FAMILIES:
        assert DEFAULTS[fam] in LADDERS[fam], fam
    say(f"  G3 default rung present in every ladder: PASS (all {len(FAMILIES)} families)")
    assert pd.Timestamp(IS_END) < pd.Timestamp(OOS_START)
    say(f"  G4 IS <= {IS_END} and OOS >= {OOS_START} are disjoint and jointly exhaust the sample: PASS")

    panels: dict[str, Panel] = {}
    for pk in PANELS:
        panels[pk] = Panel(pk)
        p = panels[pk]
        say(f"  panel {pk:<9} {p.sub.shape[1]:>4} names  {p.px.index[0].date()}..{p.px.index[-1].date()}"
            f"  eval from {p.start.date()}" + (f"  (dropped {p.ndrop} on max_1d_move)" if p.ndrop else ""))

    # ---------------- G1/G2 ----------------
    say("  G1 fast_bt vs engine.backtest (returns, turnover), 10 bps, one arm per panel:")
    for pk in PANELS:
        p = panels[pk]
        W, ph = arm(p, "JIT", 0)
        W = W.reindex(columns=p.px.columns).fillna(0.0)
        r0, to = run(p.px, W, ph)
        eng = backtest(p.px, W, cost_bps=PCOST, freq="W")
        mine = (r0 - to * PCOST / 1e4).loc[p.start:]
        ref = eng["returns"].loc[p.start:]
        dr = float(np.abs(mine.values - ref.values).max())
        dt = float(np.abs(to.loc[p.start:].values - eng["turnover"].loc[p.start:].values).max())
        say(f"     {pk:<9} max|dret| {dr:.3e}   max|dturn| {dt:.3e}   "
            f"{'PASS' if dr < 1e-10 and dt < 1e-10 else 'FAIL'}")
        assert dr < 1e-10 and dt < 1e-10
    say("  G2 cost-rung identity r(c)=r(0)-turnover*c/1e4 vs a live engine.backtest(25 bps):")
    for pk in PANELS:
        p = panels[pk]
        W, ph = arm(p, "JIT", 0)
        W = W.reindex(columns=p.px.columns).fillna(0.0)
        r0, to = run(p.px, W, ph)
        eng = backtest(p.px, W, cost_bps=25.0, freq="W")
        d = float(np.abs((r0 - to * 25.0 / 1e4).loc[p.start:].values
                         - eng["returns"].loc[p.start:].values).max())
        say(f"     {pk:<9} max|d| {d:.3e}   {'PASS' if d < 1e-10 else 'FAIL'}")
        assert d < 1e-10

    # ---------------- G5 nullity ----------------
    say("  G5 NULLITY of each family, measured from TARGET WEIGHTS (never asserted):")
    nullrows = []
    for pk in PANELS:
        p = panels[pk]
        idx = p.px.index
        days = idx[np.flatnonzero(mask_of(idx, "W"))]
        days = days[days >= p.start]
        for fam in FAMILIES:
            Wd, _ = arm(p, fam, DEFAULTS[fam])
            Wd = Wd.reindex(idx).fillna(0.0).loc[days]
            A = Wd.values > 1e-12
            jacs, wgts, exps = [], [], []
            probe = [v for v in LADDERS[fam] if v != DEFAULTS[fam]]
            probe = probe if fam == "PHASE" else probe[:4]   # 4-rung probe on the 32-rung families
            for v in probe:
                Wv, _ = arm(p, fam, v)
                Wv = Wv.reindex(idx).fillna(0.0).loc[days]
                B = Wv.values > 1e-12
                inter = (A & B).sum(axis=1).astype(float)
                union = (A | B).sum(axis=1).astype(float)
                jacs.append(np.nanmean(np.where(union > 0, 1.0 - inter / np.maximum(union, 1e-12), 0.0)))
                ga, gb = Wd.values.sum(axis=1), Wv.values.sum(axis=1)
                ca = np.divide(Wd.values, np.maximum(ga, 1e-12)[:, None])
                cb = np.divide(Wv.values, np.maximum(gb, 1e-12)[:, None])
                wgts.append(float((np.abs(ca - cb) * (A & B)).sum(axis=1).mean() / 2.0))
                exps.append(float(np.abs(ga - gb).mean()))
            nullrows.append(dict(panel=pk, family=fam, nprobe=len(probe),
                                 JAC=float(np.mean(jacs)),
                                 WGT=float(np.mean(wgts)), EXP=float(np.mean(exps))))
    N = pd.DataFrame(nullrows)
    say(N.to_string(index=False, float_format=lambda x: f"{x:.6f}"))
    ph = N[N.family == "PHASE"]
    ok = bool((ph[["JAC", "WGT", "EXP"]].abs().values < 1e-12).all())
    say(f"     PHASE target distance EXACTLY 0 on all three legs, all panels: {'PASS' if ok else 'FAIL'}"
        f"  (max {float(ph[['JAC','WGT','EXP']].abs().values.max()):.3e})")
    assert ok
    say("     JIT/PERM: the ladder is null (equal jitter magnitude / non-identity permutations at")
    say("     every rung, control included); their JAC above is REPORTED, not claimed to be 0.")
    p0 = panels["u56"]
    s_real = np.sort(p0.comp.loc[p0.start:].values, axis=1)
    s_perm = np.sort(score_of(p0, "PERM", 3).loc[p0.start:].values, axis=1)
    dmax = float(np.nanmax(np.abs(s_real - s_perm)))
    say(f"     PERM preserves each day's cross-sectional score distribution exactly: "
        f"max|sorted diff| {dmax:.3e}  {'PASS' if dmax < 1e-12 else 'FAIL'}")
    assert dmax < 1e-12

    # ---------------- the grid ----------------
    say(f"\nPART B — the null grid ({len(PANELS)} panels x {sum(len(LADDERS[f]) for f in FAMILIES)} "
        f"rungs = {len(PANELS)*sum(len(LADDERS[f]) for f in FAMILIES)} arms), every rung reported")
    grid, bars, basers = [], {}, {}
    for pk in PANELS:
        p = panels[pk]
        spy = p.px["SPY"].pct_change().fillna(0.0).loc[p.start:]
        b = bars_of(spy)
        base = backtest(p.px, rules_v2_weights(p.px), cost_bps=PCOST, freq="W")["returns"].loc[p.start:]
        bars[pk], basers[pk] = b, base
        for fam in FAMILIES:
            rows, _ = grid_rows(p, fam, b, base)
            grid.extend(rows)
        say(f"  {pk} done  [{time.time()-t0:.0f}s]")
    G = pd.DataFrame(grid)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    say(f"\n  ALL {len(G)} GRID POINTS at {PCOST:g} bps (PROTOCOL 5: every point reported)")
    show = G[["panel", "family", "value", "is_default", "turnover", "sh_full_10", "cagr_full_10",
              "dd_full_10", "h1_10", "h2_10", "sh_is_10", "sh_oos_10", "p4a_full", "p4b_full"]]
    say(show.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    say(f"\n  PROTOCOL 4 over the whole grid at {PCOST:g} bps:")
    say(f"     4a passes {int(G.p4a_full.sum())}/{len(G)}      4b passes {int(G.p4b_full.sum())}/{len(G)}")
    for fam in FAMILIES:
        g = G[G.family == fam]
        say(f"       {fam:<6} 4a {int(g.p4a_full.sum()):>3}/{len(g):<3}  4b {int(g.p4b_full.sum()):>3}/{len(g)}")

    # ---------------- rule 8 on the full ladders ----------------
    say("\n  PROTOCOL 8 — rule-8 chooser on the FULL ladder of each cell, vs the ladder's own default")
    WF = wf_cells(G)
    WF.to_csv(OUT / f"{STEM}.wf.csv", index=False)
    say(WF[["panel", "family", "cost", "L", "pick", "control", "is_sh_pick", "is_sh_ctl",
            "oos_sh_pick", "oos_sh_ctl", "d_sharpe", "oos_cagr_pick", "oos_cagr_ctl",
            "oos_dd_pick", "oos_dd_ctl", "regret", "pick_is_control"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n  vs the record's own comparands, OOS (2017-2026), 10 bps:")
    for pk in PANELS:
        b, base = bars[pk], basers[pk]
        mo = metrics(base.loc[OOS_START:])
        ms = metrics(b["spy_oos"])
        say(f"     {pk:<9} RULES v2  OOS CAGR {mo['CAGR']:+.2%}  Sharpe {mo['Sharpe']:.4f}  "
            f"MaxDD {mo['MaxDD']:.2%}   |   SPY  OOS CAGR {ms['CAGR']:+.2%}  "
            f"Sharpe {ms['Sharpe']:.4f}  MaxDD {ms['MaxDD']:.2%}")
        for fam in FAMILIES:
            w = WF[(WF.panel == pk) & (WF.family == fam) & (WF.cost == PCOST)]
            if w.empty:
                continue
            r = w.iloc[0]
            say(f"       {fam:<6} pick OOS CAGR {r.oos_cagr_pick:+.2%}  Sharpe {r.oos_sh_pick:.4f}  "
                f"MaxDD {r.oos_dd_pick:.2%}   beats v2 {r.oos_sh_pick > mo['Sharpe']}  "
                f"beats SPY {r.oos_sh_pick > ms['Sharpe']}")

    say(f"\n  G6 REPLICATION of idea 624's PHASE numbers (DEFAULT control, {PCOST:g} bps):")
    for pk in ("u56", "small439"):
        w = WF[(WF.panel == pk) & (WF.family == "PHASE") & (WF.cost == PCOST)]
        say(f"     {pk:<9} d_sharpe {float(w.d_sharpe.iloc[0]):+.4f}   "
            f"(624 published +0.108 u56 / +0.188 small439 on its own book)")
    say("     624's book is top-20 of the same composite at the same gross but its FULL leg carries")
    say("     the record's default wscheme/lambda; the sign and order of magnitude are the claim here.")

    # ---------------- PART B2 ----------------
    say("\nPART B2 — WHY a null ladder pays: split-half persistence of the null rung ordering")
    say("  If the rungs were exchangeable AND independent across sub-windows, a rung that led in")
    say("  IS-first-half would not lead in IS-second-half, and rho would sit at 0.  A positive rho is")
    say("  the mechanism by which an informationless ladder still hands its chooser a repeatable pick.")
    b2 = []
    for pk in PANELS:
        for fam in FAMILIES:
            g = G[(G.panel == pk) & (G.family == fam)]
            b2.append(dict(panel=pk, family=fam, n=len(g),
                           rho_isa_isb=spearman(g["sh_isa_10"], g["sh_isb_10"]),
                           rho_is_oos=spearman(g["sh_is_10"], g["sh_oos_10"]),
                           sd_is=float(g["sh_is_10"].std(ddof=1)),
                           sd_oos=float(g["sh_oos_10"].std(ddof=1))))
    B2 = pd.DataFrame(b2)
    say(B2.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    k = int((B2.rho_is_oos > 0).sum())
    say(f"  rho(IS Sharpe, OOS Sharpe) > 0 in {k} of {len(B2)} (panel,family) cells; "
        f"exact sign p = {sign_p(k, len(B2)):.4f}")

    # ---------------- the floor ----------------
    say("\nPART B3 — THE NOISE FLOOR: d as a function of LADDER LENGTH on an informationless ladder")
    F, dists = floor_rows(G)
    F.to_csv(OUT / f"{STEM}.floor.csv", index=False)
    say(F.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n  pooled over families and cost rungs, per panel and control convention:")
    for pk in PANELS:
        for conv in ("DEF", "SYM"):
            for L in LLADDER:
                ks = [k for k in dists if k[0] == pk and k[3] == L and k[4] == conv]
                if not ks:
                    continue
                a = np.concatenate([dists[k] for k in ks])
                say(f"     {pk:<9} {conv} L={L}  n={a.size:>6}  win {float((a>0).mean()):.3f}  "
                    f"mean {a.mean():+.4f}  median {np.median(a):+.4f}  "
                    f"p90 {np.percentile(a,90):+.4f}  p95 {np.percentile(a,95):+.4f}")
    say("\n  CONTROL LUCK — the DEF floor minus the SYM floor, pooled per panel (this is the part of")
    say("  a published chooser win that belongs to WHICH RUNG WAS NAMED DEFAULT, not to the pick):")
    for pk in PANELS:
        ad = np.concatenate([dists[k] for k in dists if k[0] == pk and k[4] == "DEF"])
        asym = np.concatenate([dists[k] for k in dists if k[0] == pk and k[4] == "SYM"])
        say(f"     {pk:<9} win {float((ad>0).mean()):.3f} (DEF) vs {float((asym>0).mean()):.3f} (SYM)"
            f"   mean {ad.mean():+.4f} vs {asym.mean():+.4f}"
            f"   p95 {np.percentile(ad,95):+.4f} vs {np.percentile(asym,95):+.4f}")

    # ---------------- PART C ----------------
    say("\nPART C — PRICING the record's committed chooser wins against the floor")
    priced = pd.DataFrame()
    if not C.empty:
        pooled = {}
        for conv in ("DEF", "SYM"):
            for pk in list(PANELS) + ["POOL"]:
                keys = [k for k in dists if k[4] == conv and (pk == "POOL" or k[0] == pk)]
                pooled[(pk, conv)] = np.concatenate([dists[k] for k in keys])
        say("  floors (pooled over the three null families, all lengths, both cost rungs):")
        for (pk, conv), a in pooled.items():
            say(f"     {pk:<9} {conv}  n={a.size:>7}  null win rate {float((a>0).mean()):.3f}  "
                f"p90 {np.percentile(a,90):+.4f}  p95 {np.percentile(a,95):+.4f}  "
                f"p99 {np.percentile(a,99):+.4f}")
        rows = []
        for lab, g in C.groupby("panel"):
            if len(g) < 25:                      # tiny per-file labels are carried in the CSV only
                continue
            used = lab if (lab, "DEF") in pooled else "POOL"
            wins = g[g.d > 0]
            rec = dict(panel=lab, floor_used=used, n_rows=len(g), n_wins=len(wins),
                       obs_win_rate=float((g.d > 0).mean()),
                       median_win=float(wins.d.median()) if len(wins) else np.nan)
            for conv in ("DEF", "SYM"):
                a = pooled[(used, conv)]
                p95, p99 = np.percentile(a, 95), np.percentile(a, 99)
                rec[f"null_win_{conv}"] = float((a > 0).mean())
                rec[f"excess_win_{conv}"] = float((g.d > 0).mean()) - float((a > 0).mean())
                rec[f"p95_{conv}"] = float(p95)
                rec[f"over_p95_{conv}"] = int((g.d > p95).sum())
                rec[f"share_wins_over_p95_{conv}"] = float((g.d > p95).sum() / max(len(wins), 1))
                rec[f"over_p99_{conv}"] = int((g.d > p99).sum())
            rows.append(rec)
        priced = pd.DataFrame(rows).sort_values("n_rows", ascending=False)
        priced.to_csv(OUT / f"{STEM}.priced.csv", index=False)
        say(priced.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        for conv in ("DEF", "SYM"):
            allf = pooled[("POOL", conv)]
            p95a, p99a = np.percentile(allf, 95), np.percentile(allf, 99)
            say(f"\n  RECORD-WIDE against the pooled {conv} floor "
                f"(p95 {p95a:+.4f}, p99 {p99a:+.4f}):")
            say(f"     committed d rows                     : {len(C)}")
            say(f"     committed WINS (d>0)                 : {int((C.d>0).sum())}  "
                f"({float((C.d>0).mean()):.1%})")
            say(f"     null win rate on an EMPTY ladder     : {float((allf>0).mean()):.1%}")
            say(f"     committed d ABOVE the null p95       : {int((C.d>p95a).sum())}  "
                f"({float((C.d>p95a).mean()):.1%} of all rows, "
                f"{float((C.d>p95a).sum()/max(int((C.d>0).sum()),1)):.1%} of wins)")
            say(f"     committed d ABOVE the null p99       : {int((C.d>p99a).sum())}  "
                f"({float((C.d>p99a).mean()):.1%} of all rows)")
            say(f"     median committed win {float(C[C.d>0].d.median()):+.4f} vs median null win "
                f"{float(np.median(allf[allf>0])):+.4f}  "
                f"({float(C[C.d>0].d.median()/np.median(allf[allf>0])):.2f}x)")
            nz, nzf = C[C.d != 0].d, allf[allf != 0]
            say(f"     TIES EXCLUDED (the chooser actually moved off the control):")
            say(f"        record {int((nz>0).sum())}/{len(nz)} = {float((nz>0).mean()):.1%} wins "
                f"({int((C.d==0).sum())} of {len(C)} committed rows are exact ties, "
                f"{float((C.d==0).mean()):.1%})")
            say(f"        null   {int((nzf>0).sum())}/{len(nzf)} = {float((nzf>0).mean()):.1%} wins "
                f"({int((allf==0).sum())} of {len(allf)} null draws are exact ties, "
                f"{float((allf==0).mean()):.1%})")
            say(f"        excess win rate, ties excluded : "
                f"{float((nz>0).mean()) - float((nzf>0).mean()):+.1%}")

    # ---------------- verdict ----------------
    say("\n" + "=" * 110)
    say("VERDICT")
    say("=" * 110)
    keep = G[G.p4b_full | G.p4a_full]
    say(f"  4a {int(G.p4a_full.sum())}/{len(G)}   4b {int(G.p4b_full.sum())}/{len(G)} at {PCOST:g} bps; "
        f"{'no arm clears either path' if keep.empty else str(len(keep)) + ' arms clear a path'}.")
    say("  No RULES change proposed: every arm in this file is an informationless ladder by")
    say("  construction and none of them is a book anyone should hold.")
    say(f"\n[{time.time()-t0:.0f}s]")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
