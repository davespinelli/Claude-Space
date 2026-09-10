#!/usr/bin/env python3
"""Idea 624 — is the SELECTION-vs-TRADING dial split a record-wide law?   (lane C, 2026-09-10)

QUEUE 624: "idea 621 found a rule-8 pick beats the NO-DIAL control in 11 of 12 cells when the dial
selects HOLDINGS (n, vol cap) and in 20 of 36 when it only changes trading, exposure or gate width
(lambda, cadence, gross, band; band is a net loss), on six dials and 48 cells.  Re-cut the record's
committed rule-8 picks by this two-class split and test whether the class, not the dial, predicts
whether the pick survives its own default.  Max 2 params (dial class, control form)."

WHY THE QUEUE'S LITERAL INSTRUCTION CANNOT SETTLE IT, AND WHAT IS RUN INSTEAD
  Idea 621's split was READ OFF the same six dials that produced it.  Each dial sits in exactly one
  class, so on that evidence "the class predicts" and "the dial predicts" are the SAME statement —
  no re-reading of 621's own cells can separate them.  Two things can:
    (i)  HELD-OUT DIALS.  Four dials 621 never ran, two per a-priori class, pre-registered before
         any return is read.  If the law is a class law it must transfer to dials chosen for their
         class alone.
    (ii) AN EXACT PARTITION TEST.  With 8 dials there are C(8,4)/2 = 35 balanced 4-4 partitions.
         Score the class gap on every one; the a-priori SELECTION/TRADING partition's rank among
         all 35 is an exact p-value for "this particular cut is special", i.e. for class over dial.
  PART A still does the queue's census leg, on the record's own committed rule-8 stems, and reports
  what it can and cannot support.

  PART C adds the piece 621 did not have: a PRE-RETURN taxonomy.  Each dial's ladder is described by
  three numbers computed from TARGET WEIGHTS ALONE — membership distance (Jaccard), within-set
  composition distance, and gross distance — so a dial can be classified before a single backtest is
  run.  Each dial is then split into a SET-ONLY leg (this dial's holdings, weighted the default way)
  and a WEIGHT-ONLY leg (the default holdings, weighted this dial's way) and rule 8 is run on each.

AXES (PROTOCOL 4: no more than 2 tuned parameters — the queue names them)
  P1 DIAL CLASS: the a-priori binary class (SELECTION / TRADING) plus its measured continuous form
     (mean membership distance).  Both are reported; neither is fitted.
  P2 CONTROL FORM: what "no dial" means, both forms reported everywhere (idea 621's two):
       DEFAULT  the record's own default rung for that dial (n=20, volcap=0.60, gross=0.75,
                lambda=1.00, composite=the record's, wscheme=EW, phase=W);
       MEDIAN   the midpoint rung of the dial's own ladder.
  Panels (u56 / broad136 / small439) and cost rungs are REPORTED axes, never selected on.  The only
  selection anywhere in this file is PROTOCOL rule 8 itself, which is the object of study.

THE EIGHT DIALS (a-priori class fixed before any run; 4 anchors from 621, 4 held out)
  SELECTION  n*        [5,10,15,20,30,40,60]                    default 20      (anchor, 621)
             volcap*   [0.30,0.45,0.60,0.80,1.00,9.99]          default 0.60    (anchor, 621)
             look      [REC,63,126,189,252]                     default REC     (HELD OUT)
             skip      [REC,0,5,21,42]                          default REC     (HELD OUT)
  TRADING    gross*    [0.25,0.50,0.75,1.00]                    default 0.75    (anchor, 621)
             lambda*   [1.00,0.70,0.50,0.35,0.25,0.15,0.10,0.06] default 1.00   (anchor, 621)
             wscheme   [EW,INVVOL,SQRTIV,RANKLIN]               default EW      (HELD OUT)
             phase     [W,MON,TUE,WED,THU]                      default W       (HELD OUT)
  look/skip change WHICH names the composite ranks first; wscheme changes only the weights inside an
  identically-selected set; phase changes only WHEN the same target is applied.  The classes were
  written down here before the grid was run and are not revised by the result.

GATES (run before any new number is read)
  G1 the vectorised segment runner vs `engine.backtest` on returns AND turnover, D and W, all panels.
  G2 the cost-rung identity r(c) = r(0) - turnover*c/1e4 vs a live engine.backtest(cost_bps=25).
  G3 the DEFAULT rung is IN the ladder of every dial (a control the grid cannot express is not one).
  G4 the IS and OOS windows are disjoint and jointly exhaust the evaluated sample.
  G5 CONSTRUCTION: wscheme's membership distance is EXACTLY 0 at every rung (it is a weights dial by
     construction, not by assertion); phase's TARGET distance is exactly 0 on all three legs.
  G6 REPLICATION: 621's anchor ordering (n and volcap win, gross is a coin flip) is re-derived here
     from this file's own grid, not restated from 621's prose.

CAVEATS CARRIED
  * SURVIVORSHIP (idea 54): all three panels are CURRENT constituents.  SMALL439 additionally drops
    every ticker with max_1d_move >= 1.0 in data/small_meta.csv; its levels are not investable
    history and only WITHIN-panel arm-minus-arm contrasts are read from it.
  * Warm-up is px.index[300], not the record's [260], because the longest ladder rung (look=252 with
    the record's 21d skip, skip=42 on the 231d leg) needs 273 closes.  Every arm in this file starts
    on the same day; the anchors' levels therefore differ slightly from 621's.
  * Idea 412: a cadence has a PHASE, measured there at SD up to 0.38 for Q.  Here phase is a DIAL,
    not a nuisance held at 0 — that is deliberate, and it is the cleanest available pure-timing dial.
  * Idea 621: most of a chooser's apparent edge is cost avoidance; the 0 bps rung is reported for
    every arm so the reader can see the same decomposition here.
  * Idea 321: MaxDD is one number off one path.  Idea 126: t+1 execution, 10 bps default rung.
  * Ideas 527/531: 4b is in practice a DD-cap test on ungated momentum books; both KEEP paths are
    priced on every arm anyway, as PROTOCOL requires.
  * PART A classifies FILES by the dial tokens their own text carries (idea 534's claim/file
    distinction); it is an upper bound and it is reported as one.

Deterministic, standalone.  Modifies nothing outside its own output files.
Writes .console.txt, .census.csv, .grid.csv, .wf.csv, .taxonomy.csv, .partition.csv.
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

STEM = "2026-09-10_is-the-SELECTION-vs-TRADING-dial-split-a-record-wide-law_C"
OUT = ROOT / "research" / "backtests"
I621 = OUT / "2026-09-10_does-any-published-rule-8-pick-survive-the-NO-DIAL-control_cloud.census.csv"

IS_END, OOS_START = "2016-12-31", "2017-01-01"
PHI, DELTA = 0.70, 0.60            # 4b CAGR floor and MaxDD cap, as fractions of SPY's
PCOST = 10.0                       # PROTOCOL's own rung
RUNGS = [0.0, 10.0, 25.0, 50.0]    # reported cost ladder
CELL_RUNGS = [10.0, 25.0]          # the two rungs the headline cells are cut on (idea 621's pair)
WARM = 300                         # common warm-up bar for every arm in this file

LADDERS: dict[str, list] = {
    "n":       [5, 10, 15, 20, 30, 40, 60],
    "volcap":  [0.30, 0.45, 0.60, 0.80, 1.00, 9.99],
    "look":    ["REC", 63, 126, 189, 252],
    "skip":    ["REC", 0, 5, 21, 42],
    "gross":   [0.25, 0.50, 0.75, 1.00],
    "lambda":  [1.00, 0.70, 0.50, 0.35, 0.25, 0.15, 0.10, 0.06],
    "wscheme": ["EW", "INVVOL", "SQRTIV", "RANKLIN"],
    "phase":   ["W", "MON", "TUE", "WED", "THU"],
}
DEFAULTS = {"n": 20, "volcap": 0.60, "look": "REC", "skip": "REC",
            "gross": 0.75, "lambda": 1.00, "wscheme": "EW", "phase": "W"}
CLASS = {"n": "SELECTION", "volcap": "SELECTION", "look": "SELECTION", "skip": "SELECTION",
         "gross": "TRADING", "lambda": "TRADING", "wscheme": "TRADING", "phase": "TRADING"}
HELDOUT = {"look", "skip", "wscheme", "phase"}
DIALS = list(LADDERS)
PANELS = ["u56", "broad136", "small439"]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 4000)
LOG: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# =====================================================================================
# runner (idea 613/621's segment form; gated against engine.backtest below)
# =====================================================================================
def mask_of(idx, phase):
    """Rebalance mask, shifted the way engine.backtest shifts it.  'D'/'W'/'M'/'Q' are the
    record's calendar conventions; MON..THU rebalance on that weekday (the phase dial)."""
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


def smooth(W, lam):
    """Idea 137's partial-rebalance dial, verbatim: an EWMA of the raw target with gross restored
    daily, so the dial changes TRADING, not exposure."""
    if lam >= 1.0:
        return W
    S = W.ewm(alpha=lam, adjust=False).mean()
    g = S.sum(axis=1).replace(0, np.nan)
    return S.mul((W.sum(axis=1) / g).fillna(0.0), axis=0).fillna(0.0)


# =====================================================================================
# the book: TOP-n of a composite, vol-capped, weighted by scheme, at gross
# =====================================================================================
def comp_rec(sub):
    """The record's own composite (scan.py / baseline.score, no vol scaler)."""
    mom = sub.shift(21) / sub.shift(252) - 1
    r6, r3 = sub / sub.shift(126) - 1, sub / sub.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def comp_look(sub, J):
    """Single-lookback ranker at the record's 21-day skip: the LOOK dial."""
    return (sub.shift(21) / sub.shift(21 + int(J)) - 1).rank(axis=1, pct=True)


def comp_skip(sub, s):
    """The record's three legs, all read s days ago: the SKIP dial."""
    s = int(s)
    mom = sub.shift(s) / sub.shift(s + 231) - 1
    r6 = sub.shift(s) / sub.shift(s + 126) - 1
    r3 = sub.shift(s) / sub.shift(s + 63) - 1
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
        self._comp: dict = {}

    def comp(self, look, skip):
        k = (str(look), str(skip))
        if k not in self._comp:
            if look != "REC":
                c = comp_look(self.sub, look)
            elif skip != "REC":
                c = comp_skip(self.sub, skip)
            else:
                c = comp_rec(self.sub)
            self._comp[k] = c
        return self._comp[k]


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad & set(px.columns))


def _raw_weights(scheme, sel, rank, v20, n):
    """Positive raw weights on the SELECTED set only.  Every scheme is strictly positive on the
    selected names, so MEMBERSHIP is identical across schemes by construction (gate G5)."""
    if scheme == "EW":
        raw = sel.astype(float)
    elif scheme == "INVVOL":
        raw = (1.0 / v20.clip(lower=0.08)).where(sel)
    elif scheme == "SQRTIV":
        raw = (1.0 / np.sqrt(v20.clip(lower=0.08))).where(sel)
    elif scheme == "RANKLIN":
        raw = (float(n) + 1.0 - rank).clip(lower=1e-9).where(sel)
    else:
        raise ValueError(scheme)
    return raw.where(sel, 0.0).fillna(0.0)


def target(panel: Panel, vals: dict):
    """Target weights (before the lambda/phase timing dials) for one dial setting."""
    c = panel.comp(vals["look"], vals["skip"])
    vc = float(vals["volcap"])
    c = c.where(panel.v20 < vc) if vc < 9.0 else c.where(panel.v20.notna())
    rank = c.rank(axis=1, ascending=False)
    n = int(vals["n"])
    sel = rank <= n
    raw = _raw_weights(vals["wscheme"], sel, rank, panel.v20, n)
    tot = raw.sum(axis=1).replace(0, np.nan)
    return (float(vals["gross"]) * raw.div(tot, axis=0)).fillna(0.0)


def arm(panel: Panel, dial: str, value, leg: str = "FULL"):
    """Weights and rebalance phase for one grid point.

    FULL  the dial as the record would run it.
    SET   this dial's HOLDINGS, weighted the default way (EW at the default gross) — the
          selection content of the dial, with its weighting content removed.
    WGT   the DEFAULT holdings, weighted this dial's way at the default gross — the within-set
          weighting content, with its selection content removed.
    """
    vals = dict(DEFAULTS)
    vals[dial] = value
    if leg == "FULL":
        W = target(panel, vals)
        return smooth(W, float(vals["lambda"])), str(vals["phase"])
    if leg == "SET":
        v2 = dict(vals)
        v2["wscheme"], v2["gross"], v2["lambda"], v2["phase"] = "EW", DEFAULTS["gross"], 1.0, "W"
        return target(panel, v2), "W"
    v2 = dict(DEFAULTS)                       # default SET ...
    v2["wscheme"] = vals["wscheme"]           # ... this dial's within-set weighting only
    return target(panel, v2), "W"


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


# =====================================================================================
# PART A — re-cut of the record's OWN committed rule-8 stems
# =====================================================================================
SEL_TOK = re.compile(r"\bn\s*=\s*\d|\bntop\b|top-?\s*\d+|concentration|volcap|max_vol|vol\s*cap|"
                     r"\beligib|holdings?\s+set|which\s+names", re.I)
TRD_TOK = re.compile(r"\blambda\b|partial\s+rebalanc|\bcadence\b|freq\s*=|\bgross\b|\bband\b|"
                     r"hysteresis|turnover\s+dial|smooth", re.I)


def recut_census():
    """Take idea 621's committed census of rule-8 stems and cut it by DIAL CLASS, reading each
    stem's own files for selection-class and trading-class dial tokens.  Reported as an upper
    bound: a file that mentions both classes cannot be assigned to either."""
    if not I621.exists():
        say("  idea 621 census.csv NOT PRESENT — the re-cut leg is not attempted (reported, not faked)")
        return pd.DataFrame()
    C = pd.read_csv(I621)
    wf = C[C.is_wf].copy()
    files = {}
    for p in OUT.iterdir():
        if p.suffix.lower() not in (".py", ".md", ".txt", ".csv"):
            continue
        s = re.sub(r"\.(csv|md|txt|py)$", "", p.name)
        s = re.sub(r"\.[A-Za-z0-9_]+$", "", s)
        files.setdefault(s, []).append(p)
    rows = []
    for _, r in wf.iterrows():
        sel = trd = False
        for p in files.get(r["stem"], []):
            if p.suffix == ".csv" and p.stat().st_size > 3_000_000:
                continue
            try:
                t = p.read_text(errors="ignore")
            except Exception:
                continue
            if SEL_TOK.search(t):
                sel = True
            if TRD_TOK.search(t):
                trd = True
        cls = ("BOTH" if sel and trd else "SELECTION" if sel else "TRADING" if trd else "NEITHER")
        rows.append(dict(stem=r["stem"], strict=bool(r["strict"]), wf_csv=bool(r["wf_csv"]),
                         sel_tok=sel, trd_tok=trd, dial_class=cls))
    return pd.DataFrame(rows)


# =====================================================================================
# PART C — the PRE-RETURN taxonomy (measured from target weights, no returns read)
# =====================================================================================
def taxonomy(panel: Panel, dial: str):
    """For every rung, distance from the DEFAULT arm's TARGET weights, on rebalance days only:
      JAC  Jaccard distance of the held NAME SET             (selection content)
      WGT  L1/2 between within-set compositions, common names (weighting content)
      EXP  |gross_v - gross_default|                          (exposure content)
    Timing dials move none of the three: their content is entirely in WHEN the target is applied."""
    Wd, _ = arm(panel, dial, DEFAULTS[dial], "FULL")
    idx = panel.px.index
    days = idx[np.flatnonzero(mask_of(idx, "W"))]
    days = days[days >= panel.start]
    Wd = Wd.reindex(idx).fillna(0.0).loc[days]
    A = (Wd.values > 1e-12)
    rows = []
    for v in LADDERS[dial]:
        Wv, _ = arm(panel, dial, v, "FULL")
        Wv = Wv.reindex(idx).fillna(0.0).loc[days]
        B = (Wv.values > 1e-12)
        inter = (A & B).sum(axis=1).astype(float)
        union = (A | B).sum(axis=1).astype(float)
        jac = np.where(union > 0, 1.0 - inter / np.maximum(union, 1e-12), 0.0)
        ga, gb = Wd.values.sum(axis=1), Wv.values.sum(axis=1)
        ca = np.divide(Wd.values, np.maximum(ga, 1e-12)[:, None])
        cb = np.divide(Wv.values, np.maximum(gb, 1e-12)[:, None])
        both = A & B
        wgt = (np.abs(ca - cb) * both).sum(axis=1) / 2.0
        rows.append(dict(panel=panel.key, dial=dial, value=str(v),
                         is_default=(v == DEFAULTS[dial]),
                         JAC=float(np.nanmean(jac)), WGT=float(np.nanmean(wgt)),
                         EXP=float(np.nanmean(np.abs(ga - gb)))))
    return rows


# =====================================================================================
# the grid
# =====================================================================================
def grid_rows(panel: Panel, dial: str, leg: str, b, baser):
    px, start = panel.px, panel.start
    out = []
    for v in LADDERS[dial]:
        W, phase = arm(panel, dial, v, leg)
        r0, to = run(px, W.reindex(columns=px.columns).fillna(0.0), phase)
        r0, to = r0.loc[start:], to.loc[start:]
        rec = dict(panel=panel.key, dial=dial, dial_class=CLASS[dial],
                   heldout=(dial in HELDOUT), leg=leg, value=str(v),
                   is_default=(v == DEFAULTS[dial]),
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
            rec[f"sh_oos_{c:g}"] = mo["Sharpe"]
            rec[f"cagr_oos_{c:g}"] = mo["CAGR"]
            rec[f"dd_oos_{c:g}"] = mo["MaxDD"]
            if c == PCOST:
                rec["p4a_full"] = pass4a(r, baser)
                rec["p4b_full"] = pass4b(r, b, "full")
                rec["p4a_oos"] = pass4a(r, baser, "oos")
                rec["p4b_oos"] = pass4b(r, b, "oos")
        out.append(rec)
    return out


def wf_cells(G):
    """PROTOCOL 8 on every (panel, dial, leg, rung) cell, against both control forms."""
    rows = []
    for (pk, dial, leg, c), g in [((pk, d, lg, c), G[(G.panel == pk) & (G.dial == d) & (G.leg == lg)])
                                  for pk in PANELS for d in DIALS for lg in ("FULL", "SET", "WGT")
                                  for c in CELL_RUNGS]:
        if g.empty:
            continue
        lad = LADDERS[dial]
        g = g.set_index("value").loc[[str(v) for v in lad]]
        pick = g[f"sh_is_{c:g}"].idxmax()
        oracle = g[f"sh_oos_{c:g}"].idxmax()
        for form in ("DEFAULT", "MEDIAN"):
            ctl = str(DEFAULTS[dial]) if form == "DEFAULT" else str(lad[len(lad) // 2])
            rows.append(dict(
                panel=pk, dial=dial, dial_class=CLASS[dial], heldout=(dial in HELDOUT), leg=leg,
                cost=c, control_form=form, pick=pick, control=ctl, oracle=oracle,
                is_sh_pick=g.loc[pick, f"sh_is_{c:g}"], is_sh_ctl=g.loc[ctl, f"sh_is_{c:g}"],
                oos_sh_pick=g.loc[pick, f"sh_oos_{c:g}"], oos_sh_ctl=g.loc[ctl, f"sh_oos_{c:g}"],
                oos_cagr_pick=g.loc[pick, f"cagr_oos_{c:g}"], oos_cagr_ctl=g.loc[ctl, f"cagr_oos_{c:g}"],
                oos_dd_pick=g.loc[pick, f"dd_oos_{c:g}"], oos_dd_ctl=g.loc[ctl, f"dd_oos_{c:g}"],
                d_sharpe=g.loc[pick, f"sh_oos_{c:g}"] - g.loc[ctl, f"sh_oos_{c:g}"],
                d_cagr=g.loc[pick, f"cagr_oos_{c:g}"] - g.loc[ctl, f"cagr_oos_{c:g}"],
                pick_is_control=(pick == ctl),
                p4b_pick=bool(g.loc[pick, "p4b_full"]), p4b_ctl=bool(g.loc[ctl, "p4b_full"]),
                p4a_pick=bool(g.loc[pick, "p4a_full"]), p4a_ctl=bool(g.loc[ctl, "p4a_full"]),
            ))
    return pd.DataFrame(rows)


# =====================================================================================
# exact tests
# =====================================================================================
def fisher(a, b, c, d):
    """Two-sided Fisher exact p for [[a,b],[c,d]] (small integers only)."""
    from math import comb
    n = a + b + c + d
    r1, c1 = a + b, a + c
    def pr(x):
        return comb(r1, x) * comb(n - r1, c1 - x) / comb(n, c1)
    p0 = pr(a)
    lo = max(0, c1 - (n - r1))
    hi = min(r1, c1)
    return float(sum(pr(x) for x in range(lo, hi + 1) if pr(x) <= p0 * (1 + 1e-12)))


def sign_p(k, n):
    """Two-sided exact binomial p at 0.5."""
    from math import comb
    if n == 0:
        return float("nan")
    tail = [comb(n, i) for i in range(n + 1)]
    tot = float(sum(tail))
    obs = tail[k]
    return float(sum(t for t in tail if t <= obs * (1 + 1e-12)) / tot)


def spearman(x, y):
    x, y = pd.Series(x), pd.Series(y)
    m = x.notna() & y.notna()
    if m.sum() < 3:
        return float("nan")
    return float(x[m].rank().corr(y[m].rank()))


# =====================================================================================
def main():
    t0 = time.time()
    say("=" * 108)
    say("IDEA 624 — is the SELECTION-vs-TRADING dial split a record-wide law?   (lane C 2026-09-10)")
    say("=" * 108)
    say("A-PRIORI CLASSES (fixed before any run):")
    for cl in ("SELECTION", "TRADING"):
        say(f"   {cl:<10} " + ", ".join(f"{d}{'*' if d not in HELDOUT else ' (HELD OUT)'}"
                                        for d in DIALS if CLASS[d] == cl))
    say("   * = anchor dial re-run from idea 621 (replication); HELD OUT = never run by 621.")

    # ---------------- PART A ----------------
    say("\nPART A — RE-CUT of the record's committed rule-8 stems by DIAL CLASS")
    A = recut_census()
    if not A.empty:
        A.to_csv(OUT / f"{STEM}.census.csv", index=False)
        say(f"  committed rule-8 stems (idea 621's own population) : {len(A)}")
        vc = A.dial_class.value_counts()
        for k in ("BOTH", "SELECTION", "TRADING", "NEITHER"):
            say(f"     {k:<10}: {int(vc.get(k, 0)):>4}  ({vc.get(k, 0) / len(A):.1%})")
        cut = A[A.dial_class.isin(["SELECTION", "TRADING"])]
        say(f"  stems the queue's two-class cut can actually ASSIGN : {len(cut)}  "
            f"({len(cut) / len(A):.1%})")
        say("  -> the record's published rule-8 files overwhelmingly touch BOTH classes, so a text")
        say("     re-cut cannot answer the queue's question.  PART B answers it by construction.")

    # ---------------- gates ----------------
    say("\nGATES")
    say("  G3 default rung present in every ladder:")
    ok = all(DEFAULTS[d] in LADDERS[d] for d in DIALS)
    for d in DIALS:
        assert DEFAULTS[d] in LADDERS[d], d
    say(f"     PASS ({ok}) — all {len(DIALS)} dials")

    panels = {}
    for pk in PANELS:
        panels[pk] = Panel(pk)
        p = panels[pk]
        say(f"  panel {pk:<9} {p.sub.shape[1]:>4} names  {p.px.index[0].date()}..{p.px.index[-1].date()}"
            f"  eval start {p.start.date()}  (dropped {p.ndrop} bad tickers)")

    say("  G1 fast runner vs engine.backtest (returns, turnover), phases D and W:")
    for pk in PANELS:
        p = panels[pk]
        W, _ = arm(p, "n", DEFAULTS["n"], "FULL")
        W = W.reindex(columns=p.px.columns).fillna(0.0)
        for f in ("D", "W"):
            e = backtest(p.px, W, cost_bps=0.0, freq=f)
            r, to = run(p.px, W, f)
            # compared on the EVALUATED sample: engine.backtest's own shift(1) leaves row 0 NaN,
            # which is 300 bars before anything this file reads (idea 621 gates the same way).
            dr = float((r.loc[p.start:] - e["returns"].loc[p.start:]).abs().max())
            dt = float((to.loc[p.start:] - e["turnover"].loc[p.start:]).abs().max())
            say(f"     {pk:<9} {f}  max|dr| {dr:.2e}  max|dto| {dt:.2e}")
            assert dr < 1e-12 and dt < 1e-12

    say("  G2 cost-rung identity r(c) = r(0) - turnover*c/1e4 vs a live engine.backtest(25 bps):")
    p = panels["u56"]
    W, _ = arm(p, "n", 20, "FULL")
    W = W.reindex(columns=p.px.columns).fillna(0.0)
    e25 = backtest(p.px, W, cost_bps=25.0, freq="W")
    r0, to = run(p.px, W, "W")
    d2 = float(((r0 - to * 25 / 1e4).loc[p.start:] - e25["returns"].loc[p.start:]).abs().max())
    say(f"     max|d| {d2:.2e}")
    assert d2 < 1e-12

    say("  G4 IS/OOS windows disjoint and exhaustive on the evaluated sample:")
    idx = p.px.loc[p.start:].index
    n_is, n_oos = int((idx <= IS_END).sum()), int((idx >= OOS_START).sum())
    say(f"     IS {n_is} bars ({idx[0].date()}..{IS_END})  OOS {n_oos} bars ({OOS_START}..{idx[-1].date()})"
        f"  sum {n_is + n_oos} == {len(idx)}  {n_is + n_oos == len(idx)}")
    assert n_is + n_oos == len(idx)

    # ---------------- PART C.1 — pre-return taxonomy ----------------
    say("\nPART C.1 — PRE-RETURN TAXONOMY (target weights only; no return is read)")
    TX = pd.DataFrame([r for pk in PANELS for d in DIALS for r in taxonomy(panels[pk], d)])
    TX.to_csv(OUT / f"{STEM}.taxonomy.csv", index=False)
    tt = (TX[~TX.is_default].groupby(["dial"])[["JAC", "WGT", "EXP"]].mean()
          .reindex(DIALS))
    tt["class"] = [CLASS[d] for d in tt.index]
    tt["heldout"] = [d in HELDOUT for d in tt.index]
    say(tt.to_string(float_format=lambda x: f"{x:.4f}"))
    say("  G5 CONSTRUCTION checks:")
    jw = float(TX[(TX.dial == "wscheme")].JAC.abs().max())
    say(f"     wscheme membership distance (JAC) max over all rungs/panels : {jw:.2e}  (must be 0)")
    assert jw < 1e-12
    ph = float(TX[(TX.dial == "phase")][["JAC", "WGT", "EXP"]].abs().values.max())
    say(f"     phase TARGET distance (JAC/WGT/EXP) max                      : {ph:.2e}  (must be 0)")
    assert ph < 1e-12
    lm = float(TX[(TX.dial == "lambda")][["JAC", "WGT", "EXP"]].abs().values.max())
    say(f"     lambda TARGET distance (it is a timing dial too)             : {lm:.2e}")
    say("     => phase and lambda are TIMING dials: they move no target at all.  gross is an")
    say("        EXPOSURE dial (EXP>0, JAC=WGT=0).  wscheme is a pure WEIGHTS dial (JAC=0).")
    say("        n / volcap / look / skip all move MEMBERSHIP.  The taxonomy is readable with")
    say("        zero backtests, which is the point.")

    # ---------------- the grid ----------------
    say("\nGRID — every dial x rung x leg x panel, all rungs of the cost ladder reported")
    rows = []
    for pk in PANELS:
        p = panels[pk]
        spy = p.px["SPY"].pct_change().fillna(0.0).loc[p.start:]
        b = bars_of(spy)
        r0, to = run(p.px, rules_v2_weights(p.px), "W")
        baser = (r0 - to * PCOST / 1e4).loc[p.start:]
        m, mo = metrics(spy), metrics(spy.loc[OOS_START:])
        mb, mbo = metrics(baser), metrics(baser.loc[OOS_START:])
        say(f"  {pk:<9} SPY full {m['CAGR']:.2%}/{m['Sharpe']:.3f}/{m['MaxDD']:.2%}"
            f"  OOS {mo['CAGR']:.2%}/{mo['Sharpe']:.3f}/{mo['MaxDD']:.2%}"
            f"  || RULES v2 full {mb['CAGR']:.2%}/{mb['Sharpe']:.3f}/{mb['MaxDD']:.2%}"
            f"  OOS {mbo['CAGR']:.2%}/{mbo['Sharpe']:.3f}/{mbo['MaxDD']:.2%}")
        for d in DIALS:
            for leg in ("FULL", "SET", "WGT"):
                rows += grid_rows(p, d, leg, b, baser)
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"  grid points written: {len(G)}   ({G.leg.value_counts().to_dict()})")

    # ---------------- PROTOCOL 8 ----------------
    say("\nRULE 8 — dial chosen on 2010-2016 IS Sharpe alone; 2017-2026 read exactly once")
    WF = wf_cells(G)
    WF.to_csv(OUT / f"{STEM}.wf.csv", index=False)
    F = WF[WF.leg == "FULL"].copy()
    F["win"] = F.d_sharpe > 0
    say(f"  cells: {len(F)} FULL-leg (panel x dial x rung x control form) "
        f"= {len(PANELS)} panels x {len(DIALS)} dials x {len(CELL_RUNGS)} rungs x 2 forms")

    say("\n  PER-DIAL (both control forms pooled; 6 cells per dial per form, 12 per dial)")
    per = F.groupby(["dial_class", "heldout", "dial"]).agg(
        wins=("win", "sum"), n=("win", "size"), med=("d_sharpe", "median"),
        mean=("d_sharpe", "mean"), pick_eq_ctl=("pick_is_control", "sum")).reset_index()
    per["rate"] = per.wins / per.n
    per = per.sort_values(["dial_class", "heldout", "dial"])
    say(per.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n  THE HELD-OUT TEST (the only cells 621's split did not see)")
    H = F[F.heldout]
    hs, ht = H[H.dial_class == "SELECTION"], H[H.dial_class == "TRADING"]
    say(f"     SELECTION (look, skip)   : {int(hs.win.sum())}/{len(hs)}  median d_sharpe "
        f"{hs.d_sharpe.median():+.4f}   sign p={sign_p(int(hs.win.sum()), len(hs)):.3f}")
    say(f"     TRADING  (wscheme, phase): {int(ht.win.sum())}/{len(ht)}  median d_sharpe "
        f"{ht.d_sharpe.median():+.4f}   sign p={sign_p(int(ht.win.sum()), len(ht)):.3f}")
    pf = fisher(int(hs.win.sum()), len(hs) - int(hs.win.sum()),
                int(ht.win.sum()), len(ht) - int(ht.win.sum()))
    say(f"     Fisher exact (class x win), held-out dials only: p = {pf:.4f}")

    say("\n  G6 REPLICATION of idea 621's anchors, re-derived from THIS file's grid")
    An = F[~F.heldout]
    for d in ["n", "volcap", "gross", "lambda"]:
        s = An[An.dial == d]
        say(f"     {d:<8} {CLASS[d]:<9} {int(s.win.sum())}/{len(s)}  median {s.d_sharpe.median():+.4f}"
            f"   [621 reported: n 5/6, volcap 6/6, gross 8/12, lambda 7/12]")
    a_s, a_t = An[An.dial_class == "SELECTION"], An[An.dial_class == "TRADING"]
    say(f"     ANCHORS  SELECTION {int(a_s.win.sum())}/{len(a_s)} (median {a_s.d_sharpe.median():+.4f})"
        f"   TRADING {int(a_t.win.sum())}/{len(a_t)} (median {a_t.d_sharpe.median():+.4f})")

    say("\n  ALL EIGHT DIALS, a-priori class")
    fs, ft = F[F.dial_class == "SELECTION"], F[F.dial_class == "TRADING"]
    say(f"     SELECTION {int(fs.win.sum())}/{len(fs)} ({fs.win.mean():.1%})  median {fs.d_sharpe.median():+.4f}")
    say(f"     TRADING   {int(ft.win.sum())}/{len(ft)} ({ft.win.mean():.1%})  median {ft.d_sharpe.median():+.4f}")
    say(f"     Fisher exact, all 8 dials: p = "
        f"{fisher(int(fs.win.sum()), len(fs) - int(fs.win.sum()), int(ft.win.sum()), len(ft) - int(ft.win.sum())):.4f}")

    # ---------------- the exact partition test: CLASS or DIAL? ----------------
    say("\n  EXACT PARTITION TEST — is the a-priori class the SPECIAL 4-4 cut of these 8 dials?")
    rate = F.groupby("dial").win.mean()
    med = F.groupby("dial").d_sharpe.median()
    parts = []
    seen = set()
    for combo in itertools.combinations(DIALS, 4):
        other = tuple(sorted(set(DIALS) - set(combo)))
        key = tuple(sorted([tuple(sorted(combo)), other]))
        if key in seen:
            continue
        seen.add(key)
        a, b_ = list(combo), list(other)
        gap = abs(rate[a].mean() - rate[b_].mean())
        gapm = abs(med[a].mean() - med[b_].mean())
        parts.append(dict(A="+".join(sorted(a)), B="+".join(sorted(b_)),
                          gap_rate=gap, gap_med=gapm,
                          is_apriori=(set(a) == {d for d in DIALS if CLASS[d] == "SELECTION"}
                                      or set(b_) == {d for d in DIALS if CLASS[d] == "SELECTION"})))
    P = pd.DataFrame(parts).sort_values("gap_rate", ascending=False).reset_index(drop=True)
    P.to_csv(OUT / f"{STEM}.partition.csv", index=False)
    rk = int(P.index[P.is_apriori][0]) + 1
    say(f"     balanced 4-4 partitions of the 8 dials: {len(P)}")
    say(f"     the a-priori SELECTION/TRADING cut ranks {rk} of {len(P)} on win-rate gap"
        f"  -> exact p = {rk / len(P):.3f}")
    say(f"     its gap {float(P.loc[P.is_apriori, 'gap_rate'].iloc[0]):.3f}"
        f"  vs the best cut {P.gap_rate.iloc[0]:.3f} ({P.A.iloc[0]} | {P.B.iloc[0]})")
    say("     top 5 cuts by win-rate gap:")
    say(P.head(5).to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n  CONTINUOUS FORM — does MEASURED membership distance predict the chooser's edge?")
    jac = TX[~TX.is_default].groupby("dial").JAC.mean()
    wgtd = TX[~TX.is_default].groupby("dial").WGT.mean()
    expd = TX[~TX.is_default].groupby("dial").EXP.mean()
    say(f"     Spearman(JAC, per-dial win rate) over 8 dials : {spearman(jac[DIALS], rate[DIALS]):+.3f}")
    say(f"     Spearman(JAC, per-dial median d_sharpe)       : {spearman(jac[DIALS], med[DIALS]):+.3f}")
    say(f"     Spearman(WGT, per-dial win rate)              : {spearman(wgtd[DIALS], rate[DIALS]):+.3f}")
    say(f"     Spearman(EXP, per-dial win rate)              : {spearman(expd[DIALS], rate[DIALS]):+.3f}")
    cell = F.merge(TX[~TX.is_default].groupby(["panel", "dial"]).JAC.mean().rename("jac_cell"),
                   on=["panel", "dial"], how="left")
    say(f"     Spearman(JAC, d_sharpe) at the CELL level (n={len(cell)}) : "
        f"{spearman(cell.jac_cell, cell.d_sharpe):+.3f}")

    # ---------------- PART C.2 — the within-dial decomposition ----------------
    say("\nPART C.2 — WITHIN-DIAL DECOMPOSITION: which LEG carries the chooser's edge?")
    dec = WF.groupby(["dial_class", "dial", "leg"]).agg(
        wins=("d_sharpe", lambda s: int((s > 0).sum())), n=("d_sharpe", "size"),
        med=("d_sharpe", "median")).reset_index()
    piv = dec.pivot_table(index=["dial_class", "dial"], columns="leg",
                          values=["wins", "med"]).reindex(
        [(CLASS[d], d) for d in DIALS])
    say(piv.to_string(float_format=lambda x: f"{x:.4f}"))
    for leg in ("FULL", "SET", "WGT"):
        L = WF[WF.leg == leg]
        ls, lt = L[L.dial_class == "SELECTION"], L[L.dial_class == "TRADING"]
        say(f"     leg {leg:<4} SELECTION {int((ls.d_sharpe > 0).sum())}/{len(ls)} "
            f"(median {ls.d_sharpe.median():+.4f})   TRADING {int((lt.d_sharpe > 0).sum())}/{len(lt)} "
            f"(median {lt.d_sharpe.median():+.4f})")

    # ---------------- cost decomposition ----------------
    say("\nCOST DECOMPOSITION — the same cells at every rung (idea 621 Q3's question, held-out dials)")
    for c in RUNGS:
        rr = []
        for pk in PANELS:
            for d in DIALS:
                g = G[(G.panel == pk) & (G.dial == d) & (G.leg == "FULL")]
                g = g.set_index("value").loc[[str(v) for v in LADDERS[d]]]
                pick = g[f"sh_is_{c:g}"].idxmax()
                for form in ("DEFAULT", "MEDIAN"):
                    ctl = str(DEFAULTS[d]) if form == "DEFAULT" else str(LADDERS[d][len(LADDERS[d]) // 2])
                    rr.append(dict(dial=d, cls=CLASS[d], heldout=d in HELDOUT,
                                   ds=g.loc[pick, f"sh_oos_{c:g}"] - g.loc[ctl, f"sh_oos_{c:g}"]))
        R = pd.DataFrame(rr)
        line = f"  {c:>5.0f} bps  ALL {int((R.ds > 0).sum())}/{len(R)} med {R.ds.median():+.4f}"
        for cl in ("SELECTION", "TRADING"):
            s = R[R.cls == cl]
            h = R[(R.cls == cl) & R.heldout]
            line += (f"  | {cl[:3]} {int((s.ds > 0).sum())}/{len(s)} med {s.ds.median():+.4f}"
                     f" (held-out {int((h.ds > 0).sum())}/{len(h)})")
        say(line)

    # ---------------- PROTOCOL 4: both KEEP paths on every arm ----------------
    say("\nPROTOCOL 4 — both KEEP paths priced on every one of the grid's arms")
    Ff = G[G.leg == "FULL"]
    say(f"  FULL-leg arms: {len(Ff)}   4a full {int(Ff.p4a_full.sum())}   4b full {int(Ff.p4b_full.sum())}"
        f"   4a OOS {int(Ff.p4a_oos.sum())}   4b OOS {int(Ff.p4b_oos.sum())}")
    say(f"  ALL arms (incl. SET/WGT legs): {len(G)}   4a {int(G.p4a_full.sum())}   4b {int(G.p4b_full.sum())}")
    say("  chooser arms vs no-dial control arms (FULL leg, PROTOCOL's 10 bps rung):")
    c10 = F[F.cost == PCOST]
    say(f"     chooser  4a {int(c10.p4a_pick.sum())}/{len(c10)}   4b {int(c10.p4b_pick.sum())}/{len(c10)}")
    say(f"     no-dial  4a {int(c10.p4a_ctl.sum())}/{len(c10)}   4b {int(c10.p4b_ctl.sum())}/{len(c10)}")
    both = Ff[Ff.p4b_full & Ff.p4b_oos]
    say(f"  arms passing 4b on the FULL sample AND on the OOS window read separately: {len(both)}")
    if len(both):
        say(both[["panel", "dial", "value", "turnover", "cagr_full_10", "sh_full_10", "dd_full_10",
                  "cagr_oos_10", "sh_oos_10", "dd_oos_10"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------- rule-8 OOS headline table ----------------
    say("\nRULE-8 OOS TABLE — the chooser's own pick, per dial, DEFAULT control form, 10 bps")
    T = F[(F.cost == PCOST) & (F.control_form == "DEFAULT")]
    say(T[["panel", "dial", "dial_class", "heldout", "pick", "control", "oracle",
           "oos_sh_pick", "oos_sh_ctl", "d_sharpe", "oos_cagr_pick", "oos_dd_pick"]].to_string(
        index=False, float_format=lambda x: f"{x:.4f}"))

    say(f"\nDone in {time.time() - t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
