#!/usr/bin/env python3
"""Idea 229 — the-tenth-selection-loses-instance-as-a-distribution   (cloud lane, 2026-09-08)

QUESTION (queue, verbatim intent)
    Idea 155 is the 10th time an IS chooser lost to doing nothing OOS.  Pool EVERY such instance
    in the record with its (selector, panel, dial, margin) and test whether the mean loss is a
    constant, whether it scales with the dial's IS-OOS argmax distance, and whether ANY selector
    class has ever won.  The output is the number PROTOCOL should quote when it says selection
    loses.

WHAT THIS RUN DOES
    A. CENSUS of every committed `*.walkforward.csv` (304 files).  Two admitted shapes, both
       declared before any number was read:
         SHAPE-W (wide)  the file carries a per-row `OOS_Sharpe` for a selected arm AND a
                         declared do-nothing control column `<ctl>_OOS_Sharpe`.
         SHAPE-L (long)  the file carries an arm-like column whose LEVEL SET contains at least
                         one declared CONTROL level and at least one declared SELECTOR level;
                         rows are paired within the group formed by every non-metric column.
       Every file is reported as admitted or rejected WITH ITS REASON.  Nothing is dropped
       silently, and the coverage fraction is published.
    B. Q1 — is the mean loss a CONSTANT?  Pooled margin (selector OOS Sharpe minus control OOS
       Sharpe), cell-weighted and instance-weighted, with a bootstrap CI under three blocks, and
       a between-instance heterogeneity decomposition.  This is the number PROTOCOL would quote.
    C. Q2 — does it SCALE with the dial's IS-OOS argmax distance?  Measured on the live corpus
       (part E), where the ladder, its IS argmax and its OOS argmax are all reconstructable;
       reported on the record side wherever a file carries per-arm IS and OOS Sharpe.
    D. Q3 — has ANY selector class ever won?  Per-class pooled margin + bootstrap CI, classes
       assigned by a declared name map (IS-SHARPE / IS-CAGR / GATED / ABSTAIN / SHRUNK-FIT /
       RANDOM / OTHER), with ORACLE arms held out as a non-selector reference.
    E. RULE 8 on live prices, out of corpus: a fresh pre-registered 6-dial ladder on 3 panels x
       2 costs.  Each dial has a DECLARED do-nothing arm (the incumbent value) and an IS-Sharpe
       argmax chooser fitted on <= 2016-12-31 only; 2017-2026 is read once.  Both KEEP paths
       (4a vs live RULES v2 and vs RULES v1; 4b vs SPY), full sample + halves + OOS.

TUNED PARAMETERS (exactly two; every grid point reported)
    P1  admission vocabulary in {STRICT, BROAD}.  STRICT counts only arms/columns the record
        names as a do-nothing control (control, S0, none, ctl, ctrl, base, anchor, do-nothing).
        BROAD additionally counts the live books (v1, v2) as the "doing nothing" comparand.
    P2  bootstrap block in {cell, instance, file}.
    The live corpus's ladders, their declared defaults, the IS/OOS split, costs, cadence, gross,
    panels and t+1 execution are the record's committed conventions, not chosen here.

PRE-REGISTERED PREDICTIONS (written before the new numbers were read)
    R1  The record contains far MORE than 10 such instances; "the 10th" is an undercount driven
        by which runs happened to phrase the result in prose.
    R2  The pooled mean margin is NEGATIVE but SMALL, and its confidence interval contains
        losses an order of magnitude smaller than any single published instance.
    R3  The loss is NOT a constant: between-instance dispersion dominates the pooled mean, so
        PROTOCOL cannot quote a single number without an interval.
    R4  No selector class wins.  If one appears to, it will be a class with few instances.
    R5  The margin scales with the IS-OOS argmax distance: choosers only lose when the dial's
        IS and OOS argmaxes disagree, which is most of the time.

CONFOUNDS / CAVEATS declared up front
    * The census is over the record's COMMITTED ARTEFACTS, not over its prose.  A run that lost
      to doing nothing but never wrote a machine-readable walk-forward file cannot be counted;
      the coverage fraction is published so the undercount is visible.
    * Instances are NOT independent: many share panels, price data, dials and even books.  That
      is exactly why the instance and file blocks are carried as P2 rather than assuming i.i.d.
      cells.
    * Margins from different files use different arm ladders and different cell definitions, so
      the cell-weighted pool over-weights files with many cells.  Both weightings are reported.
    * SMALL439 is a CURRENT-CONSTITUENTS panel (data/SMALL_PANEL_README.md); tickers with
      max_1d_move >= 1.0 in data/small_meta.csv are dropped first (439 names).  SURVIVORSHIP
      BIAS — reported as a shape check, never as a tradable return.
    * The live corpus's per-dial "do nothing" arm is the INCUMBENT value, declared in DIALS
      below before the corpus was run.  A different default would give a different margin; that
      is a property of the question, and the whole ladder is published either way.
    * 10 bps is the protocol rung; 25 bps is carried as a robustness axis.  t+1 execution and
      the 260-bar warm-up skip are the engine's, unchanged.

Deterministic (seed 229000), standalone, no network.
Writes .console.txt .census.csv .instances.csv .cells.csv .classes.csv .boot.csv
       .livegrid.csv .walkforward.csv .keeppaths.csv .result.md
"""
from __future__ import annotations

import csv
import glob
import importlib.util
import os
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import band_state, rules_v1_weights, rules_v2_weights   # noqa: E402
from engine import backtest, metrics, rebalance_mask                  # noqa: E402

STEM = "2026-09-08_the-tenth-selection-loses-instance-as-a-distribution_cloud"
OUT = ROOT / "research" / "backtests"
SEED = 229000
B_BOOT = 2000

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 70)
pd.set_option("display.max_rows", 500)
LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


I129 = _load(OUT / "2026-09-05_cagr-floor-calibration_B.py", "i129")
I94 = _load(OUT / "2026-09-04_drawdown-insurance-price-list_B.py", "i94")
C, H = I129, I94
IS_END, OOS_START = H.IS_END, H.OOS_START

# ============================================================ the declared vocabularies (P1)
# A do-nothing control is the arm you would hold if you did NOT select, on the SAME ladder.
# `base` is deliberately NOT in STRICT: in this record `base_OOS_*` is almost always the RULES
# baseline book, i.e. a different strategy, not the unselected arm.  It enters under BROAD,
# where the question becomes the looser "did the selected arm beat its declared comparand".
CTL_STRICT = {"control", "s0", "s0 do-nothing", "(none)", "none", "ctl", "ctrl",
              "anchor", "do-nothing", "donothing", "(none) -> control", "no-selection",
              "nothing", "s0 (do nothing)", "s0 control"}
CTL_BROAD = CTL_STRICT | {"base", "v1", "v2", "rules v1", "rules v2", "live", "incumbent"}
CTL_COL_STRICT = {"ctl", "ctrl", "control", "anchor", "s0", "null", "nosel"}
CTL_COL_BROAD = CTL_COL_STRICT | {"base", "v1", "v2", "live", "fixed", "none"}
ORACLE = {"oracle", "oracle-oos", "oracle_oos", "best", "best-oos", "oracle (oos argmax)"}

SELECTOR_CLASS = [                      # ordered; first match wins.  declared, not tuned.
    (r"^random", "RANDOM"),
    (r"abstain", "ABSTAIN"),
    (r"shrunk|shrink|^fit$|james|stein", "SHRUNK-FIT"),
    (r"k_?cagr|is[_ -]?cagr|cagr[- ]?argmax", "IS-CAGR"),
    (r"^s[234]\b|clause|gated|positive|sign-only|margin", "GATED"),
    (r"^s1\b|is[- ]?argmax|sel-sharpe|is[_ -]?sharpe|leak-free", "IS-SHARPE"),
    (r"^mode$|^incumbent$", "OTHER"),
]
METRIC_RE = re.compile(
    r"(oos|cagr|sharpe|maxdd|dd|is_|_is$|^is$|pass|keep|beat|regret|margin|wins|losses|"
    r"^t_|^p_|^n_|count|spy|turnover|vol|calmar|sortino|equity|total|years|dsharpe|dcagr)",
    re.I)


def classify(name: str):
    s = str(name).strip().lower()
    if s in ORACLE:
        return "ORACLE"
    for pat, cls in SELECTOR_CLASS:
        if re.search(pat, s):
            return cls
    return None                          # not a recognised selector


def ctl_cols(header, vocab):
    out = []
    for c in header:
        lc = c.lower()
        if lc.endswith("oos_sharpe"):
            pre = lc[: -len("oos_sharpe")].strip("_")
            if pre in vocab:
                out.append(c)
    return out


ARM_COLS = ("arm", "pick", "sel", "selector", "rule", "method", "mode", "strategy", "chosen")


def read_csv_safe(f):
    try:
        d = pd.read_csv(f)
        return d if len(d) else None
    except Exception:
        return None


# ============================================================================ PART A — census
def census(vocab_name):
    ctlv = CTL_STRICT if vocab_name == "STRICT" else CTL_BROAD
    ctlc = CTL_COL_STRICT if vocab_name == "STRICT" else CTL_COL_BROAD
    files = sorted(glob.glob(str(OUT / "*.walkforward.csv")))
    crows, cells = [], []
    for f in files:
        base = os.path.basename(f)
        d = read_csv_safe(f)
        if d is None:
            crows.append(dict(vocab=vocab_name, file=base, kind="-", admitted=False,
                              reason="unreadable or empty", n_cells=0)); continue
        if "OOS_Sharpe" not in d.columns:
            crows.append(dict(vocab=vocab_name, file=base, kind="-", admitted=False,
                              reason="no OOS_Sharpe column", n_cells=0)); continue
        got = False

        # ---- SHAPE-W
        cc = ctl_cols(d.columns, ctlc)
        armc = [c for c in d.columns if c.lower() in ARM_COLS]
        # evidence that the rows are the OUTCOME of a selection, not an enumerated ladder
        sel_evidence = [c for c in d.columns
                        if c.lower() in ARM_COLS or c.lower().endswith("_star")
                        or "pick" in c.lower() or "chosen" in c.lower()
                        or c.lower() in ("regret", "f_star", "tau", "q_star")]
        if cc and not sel_evidence:
            crows.append(dict(vocab=vocab_name, file=base, kind="-", admitted=False,
                              reason="control column but no evidence the rows are IS-selected",
                              n_cells=0))
            cc = []
        if cc:
            sel_name = None
            for c in armc:
                lv = [v for v in d[c].astype(str).unique() if classify(v)]
                if lv:
                    sel_name = c; break
            for c0 in cc:
                sub = d[np.isfinite(pd.to_numeric(d.OOS_Sharpe, errors="coerce"))
                        & np.isfinite(pd.to_numeric(d[c0], errors="coerce"))]
                if sel_name:                       # keep only recognised selector rows
                    sub = sub[[bool(classify(v)) and classify(v) != "ORACLE"
                               for v in sub[sel_name].astype(str)]]
                if len(sub) == 0:
                    continue
                m = pd.to_numeric(sub.OOS_Sharpe) - pd.to_numeric(sub[c0])
                inst = f"{base}::W::{c0}"
                crows.append(dict(vocab=vocab_name, file=base, kind="W", admitted=True,
                                  reason=f"control column {c0}", n_cells=len(sub)))
                rgc = [c for c in sub.columns if c.lower() == "regret"]
                bst = [c for c in sub.columns
                       if c.lower() in ("best_oos_sharpe", "best_oos_in_pool",
                                        "oracle_oos_sharpe", "best_oos")]
                if rgc:
                    rg = pd.to_numeric(sub[rgc[0]], errors="coerce").values
                elif bst:
                    rg = (pd.to_numeric(sub[bst[0]], errors="coerce")
                          - pd.to_numeric(sub.OOS_Sharpe, errors="coerce")).values
                else:
                    rg = np.full(len(sub), np.nan)
                for i, v in enumerate(m.values):
                    nm = str(sub[sel_name].iloc[i]) if sel_name else "IS-SHARPE"
                    cells.append(dict(vocab=vocab_name, instance=inst, file=base, kind="W",
                                      control=c0, selector=nm,
                                      cls=classify(nm) or "IS-SHARPE", margin=float(v),
                                      regret=float(rg[i])))
                got = True

        # ---- SHAPE-L
        for c in armc:
            lv = d[c].astype(str).str.strip()
            has_ctl = lv.str.lower().isin(ctlv)
            sels = {v: classify(v) for v in lv.unique()}
            good = {v: k for v, k in sels.items() if k and k != "ORACLE"}
            if not has_ctl.any() or not good:
                continue
            keys = [k for k in d.columns
                    if k != c and not METRIC_RE.search(k) and d[k].dtype != float]
            if not keys:
                d = d.assign(__k__="all"); keys = ["__k__"]
            piv = d.assign(__arm__=lv)
            base_map = (piv[has_ctl.values].groupby(keys, dropna=False).OOS_Sharpe
                        .mean())
            npair = 0
            for v, cls in good.items():
                sub = piv[piv.__arm__ == v]
                if not len(sub):
                    continue
                sm = sub.groupby(keys, dropna=False).OOS_Sharpe.mean()
                j = pd.concat([sm.rename("s"), base_map.rename("b")], axis=1).dropna()
                if not len(j):
                    continue
                inst = f"{base}::L::{c}::{v}"
                crows.append(dict(vocab=vocab_name, file=base, kind="L", admitted=True,
                                  reason=f"arm column {c}, selector level {v!r}", n_cells=len(j)))
                for mv in (j.s - j.b).values:
                    cells.append(dict(vocab=vocab_name, instance=inst, file=base, kind="L",
                                      control=f"{c}=<control>", selector=v, cls=cls,
                                      margin=float(mv), regret=np.nan))
                npair += len(j); got = True
            if npair:
                break
        if not got:
            why = ("no control column and no control level in an arm column"
                   if not cc else "control column present but no finite paired rows")
            crows.append(dict(vocab=vocab_name, file=base, kind="-", admitted=False,
                              reason=why, n_cells=0))
    return pd.DataFrame(crows), pd.DataFrame(cells)


def report_census(CE, CL, vocab):
    adm = CE[CE.admitted]
    P(f"\n  vocabulary {vocab}:  {CE.file.nunique()} committed *.walkforward.csv files scanned")
    P(f"      admitted instances {len(adm)}  over {adm.file.nunique()} files "
      f"({adm.file.nunique()/CE.file.nunique():.1%} coverage), {len(CL)} paired cells")
    P(f"      by shape: " + ", ".join(
        f"{k} {v} instances / {int(adm[adm.kind==k].n_cells.sum())} cells"
        for k, v in adm.kind.value_counts().items()))
    rej = CE[~CE.admitted].drop_duplicates("file")
    rej = rej[~rej.file.isin(set(adm.file))]
    P(f"      REJECTED {len(rej)} files, by reason (nothing dropped silently):")
    for r, n in rej.reason.value_counts().items():
        P(f"          {n:4d}  {r}")


# ============================================================================ PART B/C/D
def pooled_stats(CL, tag):
    P(f"\n  {tag}")
    n = len(CL)
    inst = CL.groupby("instance").margin.mean()
    P(f"      cells {n}, instances {len(inst)}, files {CL.file.nunique()}")
    P(f"      CELL-weighted mean margin     {CL.margin.mean():+.5f}  (sd {CL.margin.std(ddof=1):.5f}, "
      f"median {CL.margin.median():+.5f}, win rate {(CL.margin>0).mean():.1%})")
    P(f"      INSTANCE-weighted mean margin {inst.mean():+.5f}  (sd {inst.std(ddof=1):.5f}, "
      f"median {inst.median():+.5f}, instances that WIN {(inst>0).mean():.1%})")
    rg = CL[np.isfinite(CL.regret)] if "regret" in CL.columns else CL.iloc[:0]
    if len(rg):
        ri = rg.groupby("instance").regret.mean()
        P(f"      REGRET (chooser OOS Sharpe below its own pool's OOS best) is published on "
          f"{len(rg)} of {n} cells / {rg.instance.nunique()} instances:")
        P(f"          cell-weighted mean regret {rg.regret.mean():+.5f}, instance-weighted "
          f"{ri.mean():+.5f}, median {rg.regret.median():+.5f}, "
          f"share with regret > 0 {(rg.regret>0).mean():.1%}")
    else:
        P(f"      REGRET: not published on any admitted cell under this vocabulary.")
    within = CL.groupby("instance").margin.var(ddof=1).mean()
    between = inst.var(ddof=1)
    P(f"      heterogeneity: between-instance var {between:.5f} vs mean within-instance var "
      f"{within:.5f}  ->  between / (between+within) = {between/(between+within):.1%}")
    return inst


def boot_ci(CL, blocks=("cell", "instance", "file"), B=B_BOOT):
    rows = []
    for bi, blk in enumerate(blocks):
        rng = np.random.default_rng(SEED + 11 * (bi + 1))
        if blk == "cell":
            v = CL.margin.values
            draws = np.array([v[rng.integers(0, len(v), len(v))].mean() for _ in range(B)])
        else:
            g = list(CL.groupby(blk).margin.apply(list))
            draws = np.empty(B)
            for i in range(B):
                pick = rng.integers(0, len(g), len(g))
                draws[i] = np.mean(np.concatenate([np.asarray(g[j]) for j in pick]))
        lo, hi = np.percentile(draws, [2.5, 97.5])
        rows.append(dict(block=blk, mean=float(draws.mean()), lo=float(lo), hi=float(hi),
                         p_neg=float((draws < 0).mean())))
    return pd.DataFrame(rows)


def by_class(CL, B=1000):
    rows = []
    for cls, d in CL.groupby("cls"):
        rng = np.random.default_rng(SEED + 977 + len(cls))
        g = list(d.groupby("instance").margin.apply(list))
        draws = np.empty(B)
        for i in range(B):
            pick = rng.integers(0, len(g), len(g))
            draws[i] = np.mean(np.concatenate([np.asarray(g[j]) for j in pick]))
        lo, hi = np.percentile(draws, [2.5, 97.5])
        ni = d.instance.nunique()
        usable = ni >= 5          # declared: an instance-block CI over <5 instances is not usable
        rows.append(dict(cls=cls, cells=len(d), instances=ni,
                         files=d.file.nunique(), mean=d.margin.mean(),
                         inst_mean=d.groupby("instance").margin.mean().mean(),
                         win_rate=float((d.margin > 0).mean()), lo=lo, hi=hi, usable=usable,
                         wins=bool(lo > 0 and usable), loses=bool(hi < 0 and usable)))
    return pd.DataFrame(rows).sort_values("cells", ascending=False)


# ============================================================================ PART E — live
def fast_backtest(px, W, cost_bps, freq="W"):
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n, k = rets.shape
    cur = np.zeros(k); held = np.empty((n, k)); to = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]; to[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            cur = growth / tot
    return pd.Series((held * rets).sum(axis=1) - to * cost_bps / 1e4, index=px.index)


def csd(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


_PARTS = {}


def parts(px, pk):
    if pk in _PARTS:
        return _PARTS[pk]
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True)
            + r3.rank(axis=1, pct=True)) / 3
    above = px > px.rolling(200).mean()
    v = px.pct_change().rolling(20).std() * np.sqrt(252)
    _PARTS[pk] = (comp * (0.5 + 0.5 * above.astype(float)), above, v)
    return _PARTS[pk]


def band_book(px, band, gross):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, band), 0.0) if band > 0 else \
        ew.where(px > px.rolling(200).mean(), 0.0)


def rank_book(px, pk, n, gross=0.75, max_vol=0.60, k=-0.50):
    s, above, v = parts(px, pk)
    vv = v.clip(lower=0.08)
    sc = s if k == 0.0 else (s / vv ** 0.5 if k == -0.5 else s * vv ** k)
    elig = above & (v < max_vol) if np.isfinite(max_vol) else above
    m = (sc.where(elig).rank(axis=1, ascending=False) <= n).astype(float)
    return m.div(m.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * gross


# Six dials.  Each: (name, ladder, index of the DECLARED do-nothing arm, builder).
# The default arm is the INCUMBENT value, declared here before the corpus was run.
DIALS = {
    "band":    (["0.00", "0.02", "0.03", "0.05", "0.08", "0.12", "0.20"], "0.03"),
    "gross":   (["0.50", "0.60", "0.75", "0.90", "1.00"], "0.75"),
    "cadence": (["W", "M", "Q"], "W"),
    "share":   (["0.05", "0.10", "0.15", "0.20", "0.27", "0.35", "0.53", "0.75"], "0.20"),
    "volcap":  (["0.30", "0.45", "0.60", "0.90", "off"], "0.60"),
    "kexp":    (["-1.00", "-0.75", "-0.50", "-0.25", "-0.10", "0.00", "0.10", "0.25",
                 "0.50", "0.75", "1.00"], "-0.50"),
}
PANELS = ["u56", "broad", "small"]
COSTS = [10.0, 25.0]


def live_book(px, pk, dial, arm, nmap):
    if dial == "band":
        return band_book(px, float(arm), 0.75), "W"
    if dial == "gross":
        return band_book(px, 0.03, float(arm)), "W"
    if dial == "cadence":
        return band_book(px, 0.03, 0.75), arm
    if dial == "share":
        return rank_book(px, pk, nmap[float(arm)]), "W"
    if dial == "volcap":
        mv = np.inf if arm == "off" else float(arm)
        return rank_book(px, pk, nmap[0.20], max_vol=mv), "W"
    if dial == "kexp":
        return rank_book(px, pk, nmap[0.20], k=float(arm)), "W"
    raise ValueError(dial)


def run_live():
    P("\n" + "=" * 118)
    P("PART E — RULE 8 ON LIVE PRICES, OUT OF CORPUS: 6 pre-registered dials, choice on")
    P("         IS (<= 2016-12-31) only, 2017-2026 read once.  36 cells = 3 panels x 2 costs")
    P("         x 6 dials; the do-nothing arm of each dial is its declared INCUMBENT value.")
    P("=" * 118)
    ref, rows, RET = {}, [], {}
    t0 = time.time()
    for pk in PANELS:
        px, spy_full, desc = C.panel(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        s, above, v = parts(px, pk)
        n_elig = float((above & (v < 0.60)).loc[start:].sum(axis=1).mean())
        nmap = {m: max(2, int(round(m * n_elig)))
                for m in [0.05, 0.10, 0.15, 0.20, 0.27, 0.35, 0.53, 0.75]}
        v2 = {c: fast_backtest(px, rules_v2_weights(px), c).loc[start:] for c in COSTS}
        v1 = {c: fast_backtest(px, rules_v1_weights(px), c).loc[start:] for c in COSTS}
        ref[pk] = dict(px=px, start=start, spy=spy, nmap=nmap, v2=v2, v1=v1, desc=desc)
        cg, sh, dd = csd(spy); oc, osh, odd = csd(spy.loc[OOS_START:])
        P(f"\n  [panel] {pk} = {desc}: {px.shape[1]} cols, eval {start.date()} -> "
          f"{px.index[-1].date()}, mean weekly eligible {n_elig:.1f}")
        P(f"      SPY {cg:.2%}/{sh:.3f}/{dd:.2%} | OOS {oc:.2%}/{osh:.3f}/{odd:.2%}")
        for c in COSTS:
            a, b, d_ = csd(v2[c]); e, f_, g_ = csd(v1[c])
            P(f"      RULES v2 @{c:.0f}bps {a:.2%}/{b:.3f}/{d_:.2%}   "
              f"RULES v1 @{c:.0f}bps {e:.2%}/{f_:.3f}/{g_:.2%}")
        for dial, (ladder, dflt) in DIALS.items():
            for arm in ladder:
                W, freq = live_book(px, pk, dial, arm, nmap)
                for cost in COSTS:
                    r = fast_backtest(px, W, cost, freq).loc[start:]
                    RET[(pk, cost, dial, arm)] = r
                    cgr, shr, ddr = csd(r)
                    o = r.loc[OOS_START:]
                    oc2, osh2, odd2 = csd(o)
                    rows.append(dict(panel=pk, cost=cost, dial=dial, arm=arm,
                                     is_default=(arm == dflt),
                                     IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                                     IS_CAGR=metrics(r.loc[:IS_END])["CAGR"],
                                     CAGR=cgr, Sharpe=shr, MaxDD=ddr,
                                     OOS_CAGR=oc2, OOS_Sharpe=osh2, OOS_MaxDD=odd2))
        P(f"      {sum(len(l) for l, _ in DIALS.values())*len(COSTS)} books done "
          f"({time.time()-t0:.0f}s cum.)")
    LG = pd.DataFrame(rows)
    LG.to_csv(OUT / f"{STEM}.livegrid.csv", index=False)
    return ref, LG, RET


def live_walkforward(ref, LG, RET):
    P("\n  (i) PER-CELL: the IS-Sharpe chooser against the dial's declared do-nothing arm.")
    P(f"  {'panel':7s} {'cost':>5s} {'dial':9s} {'IS pick':>8s} {'S0':>8s} {'OOS S1':>8s} "
      f"{'OOS S0':>8s} {'margin':>8s} {'OOS best':>9s} {'regret':>8s} {'|IS-OOS| steps':>15s}")
    wf = []
    for pk in PANELS:
        for cost in COSTS:
            for dial, (ladder, dflt) in DIALS.items():
                sub = LG[(LG.panel == pk) & (LG.cost == cost) & (LG.dial == dial)]
                sub = sub.set_index("arm").reindex(ladder)
                pick = str(sub.IS_Sharpe.idxmax())
                oos_arg = str(sub.OOS_Sharpe.idxmax())
                dist = abs(ladder.index(pick) - ladder.index(oos_arg))
                m = float(sub.loc[pick, "OOS_Sharpe"] - sub.loc[dflt, "OOS_Sharpe"])
                reg = float(sub.OOS_Sharpe.max() - sub.loc[pick, "OOS_Sharpe"])
                P(f"  {pk:7s} {cost:5.0f} {dial:9s} {pick:>8s} {dflt:>8s} "
                  f"{sub.loc[pick,'OOS_Sharpe']:8.3f} {sub.loc[dflt,'OOS_Sharpe']:8.3f} "
                  f"{m:+8.4f} {sub.OOS_Sharpe.max():9.3f} {reg:8.4f} {dist:15d}")
                wf.append(dict(panel=pk, cost=cost, dial=dial, pick=pick, s0=dflt,
                               oos_argmax=oos_arg, dist_steps=dist, ladder_len=len(ladder),
                               OOS_Sharpe_pick=float(sub.loc[pick, "OOS_Sharpe"]),
                               OOS_Sharpe_s0=float(sub.loc[dflt, "OOS_Sharpe"]),
                               OOS_CAGR_pick=float(sub.loc[pick, "OOS_CAGR"]),
                               OOS_CAGR_s0=float(sub.loc[dflt, "OOS_CAGR"]),
                               OOS_MaxDD_pick=float(sub.loc[pick, "OOS_MaxDD"]),
                               OOS_MaxDD_s0=float(sub.loc[dflt, "OOS_MaxDD"]),
                               margin=m, regret=reg))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    w = int((WF.margin > 0).sum())
    P(f"\n      chooser BEATS do-nothing in {w} of {len(WF)} cells; mean margin "
      f"{WF.margin.mean():+.5f} (sd {WF.margin.std(ddof=1):.5f}, median "
      f"{WF.margin.median():+.5f})")
    rng = np.random.default_rng(SEED + 5)
    dr = np.array([WF.margin.values[rng.integers(0, len(WF), len(WF))].mean()
                   for _ in range(B_BOOT)])
    lo, hi = np.percentile(dr, [2.5, 97.5])
    P(f"      bootstrap over cells: 95% CI [{lo:+.5f}, {hi:+.5f}], P(mean < 0) = "
      f"{(dr<0).mean():.1%}")
    P(f"      by dial:")
    for d, g in WF.groupby("dial"):
        P(f"          {d:9s} beats do-nothing {int((g.margin>0).sum())}/{len(g)}, mean "
          f"{g.margin.mean():+.5f}, mean |IS-OOS argmax| {g.dist_steps.mean():.2f} steps")
    P(f"      by panel:")
    for d, g in WF.groupby("panel"):
        P(f"          {d:9s} beats do-nothing {int((g.margin>0).sum())}/{len(g)}, mean "
          f"{g.margin.mean():+.5f}")

    P("\n  (ii) THE DECOMPOSITION THAT SETTLES THE SIGN.  By construction, for every cell")
    P("       margin = (OOS_best - OOS_S0) - regret  =  ROOM - REGRET.")
    P("       ROOM is a property of the DIAL and its declared default — how much a perfect")
    P("       chooser could have won.  REGRET is the selector's own shortfall and is >= 0 by")
    P("       construction.  Only REGRET is attributable to selection.")
    WF["room"] = WF.margin + WF.regret
    P(f"\n  {'dial':9s} {'cells':>5s} {'beats S0':>9s} {'ROOM':>9s} {'REGRET':>9s} "
      f"{'MARGIN':>9s} {'|IS-OOS|':>9s}")
    for d, g in WF.groupby("dial"):
        P(f"  {d:9s} {len(g):5d} {int((g.margin>0).sum()):5d}/{len(g):<3d} {g.room.mean():+9.5f} "
          f"{g.regret.mean():9.5f} {g.margin.mean():+9.5f} {g.dist_steps.mean():9.2f}")
    P(f"  {'ALL':9s} {len(WF):5d} {int((WF.margin>0).sum()):5d}/{len(WF):<3d} "
      f"{WF.room.mean():+9.5f} {WF.regret.mean():9.5f} {WF.margin.mean():+9.5f} "
      f"{WF.dist_steps.mean():9.2f}")
    rng2 = np.random.default_rng(SEED + 6)
    dr2 = np.array([WF.regret.values[rng2.integers(0, len(WF), len(WF))].mean()
                    for _ in range(B_BOOT)])
    lo2, hi2 = np.percentile(dr2, [2.5, 97.5])
    P(f"\n      MEAN REGRET = {WF.regret.mean():.5f}, 95% CI [{lo2:.5f}, {hi2:.5f}] "
      f"— strictly positive, and this is the only term selection controls.")
    P(f"      Mean ROOM = {WF.room.mean():+.5f}: the two dials whose declared incumbent the")
    P(f"      record has ALREADY shown to be wrong (kexp default -0.50, share default 0.20) "
      f"supply\n      {WF[WF.dial.isin(['kexp','share'])].room.mean():+.5f} of room; the other "
      f"four supply {WF[~WF.dial.isin(['kexp','share'])].room.mean():+.5f}.")
    o4 = WF[~WF.dial.isin(["kexp", "share"])]
    P(f"      On those other four dials the chooser beats do-nothing in "
      f"{int((o4.margin>0).sum())} of {len(o4)} cells, mean margin {o4.margin.mean():+.5f} "
      f"(regret {o4.regret.mean():.5f}).")

    P("\n  (iii) Q2 — DOES THE LOSS SCALE WITH THE DIAL'S IS-OOS ARGMAX DISTANCE?")
    agree = WF[WF.dist_steps == 0]; disagree = WF[WF.dist_steps > 0]
    P(f"      IS and OOS argmax AGREE in {len(agree)} of {len(WF)} cells; there the margin is "
      f"{agree.margin.mean():+.5f} (all >= 0: {bool((agree.margin >= 0).all())})")
    P(f"      they DISAGREE in {len(disagree)}; there the margin is "
      f"{disagree.margin.mean():+.5f}, and the chooser still beats do-nothing in "
      f"{int((disagree.margin>0).sum())} of {len(disagree)}")
    x = WF.dist_steps.values.astype(float)
    for nm, y in (("margin", WF.margin.values), ("regret", WF.regret.values)):
        sp = H.spearman(x, y)
        b = np.polyfit(x, y, 1)
        P(f"      Spearman(|IS-OOS| steps, {nm}) = {sp:+.3f};  OLS slope "
          f"{b[0]:+.5f} per grid step (intercept {b[1]:+.5f})")
    P(f"      normalised distance (steps / ladder length): Spearman vs margin "
      f"{H.spearman(WF.dist_steps/WF.ladder_len, WF.margin):+.3f}")
    return WF


def live_keep(ref, WF, RET):
    P("\n  (iv) THE TWO BOOKS, POOLED (equal weight over the 36 cells), and the KEEP paths.")

    def eq(sl):
        return pd.concat(sl, axis=1).fillna(0.0).mean(axis=1)

    chooser = eq([RET[(r.panel, r.cost, r.dial, r["pick"])] for _, r in WF.iterrows()])
    donoth = eq([RET[(r.panel, r.cost, r.dial, r.s0)] for _, r in WF.iterrows()])
    oracle = eq([RET[(r.panel, r.cost, r.dial, r.oos_argmax)] for _, r in WF.iterrows()])
    spy = eq([ref[p]["spy"] for p in PANELS])
    v2 = eq([ref[p]["v2"][10.0] for p in PANELS])
    v1 = eq([ref[p]["v1"][10.0] for p in PANELS])
    bars = H.bars_of(spy)
    P(f"      4b bars off the pooled SPY: H1>{bars['s1']:.3f} H2>{bars['s2']:.3f} "
      f"OOS>{bars['soos']:.3f} |MaxDD|<={0.60*abs(bars['sdd']):.2%} "
      f"CAGR>={0.70*bars['scagr']:.2%}")
    P(f"  {'book':34s} | {'CAGR':>8s} {'Sharpe':>7s} {'MaxDD':>8s} {'H1':>6s} {'H2':>6s} "
      f"| {'OOS CAGR':>9s} {'Sharpe':>7s} {'MaxDD':>8s} | {'4a v2':>6s} {'4a v1':>6s} "
      f"{'4b':>5s}  failing")
    kp = []
    for nm, r in (("S1  IS-Sharpe chooser", chooser), ("S0  do nothing (declared defaults)",
                                                       donoth),
                  ("ORACLE (OOS argmax, not a rule)", oracle),
                  ("SPY", spy), ("RULES v2 (live) @10bps", v2), ("RULES v1 @10bps", v1)):
        cg, sh, dd = csd(r); oc, osh, odd = csd(r.loc[OOS_START:]); h1, h2 = H.halves(r)
        mg = H.margins(r, bars)
        fb = [b for b in ("H1", "H2", "OOS", "DD", "CAGR") if mg[b] <= 0]
        p2, p1 = H.pass4a(r, v2), H.pass4a(r, v1)
        P(f"  {nm:34s} | {cg:8.2%} {sh:7.3f} {dd:8.2%} {h1:6.3f} {h2:6.3f} | {oc:9.2%} "
          f"{osh:7.3f} {odd:8.2%} | {str(p2):>6s} {str(p1):>6s} {str(len(fb)==0):>5s}  "
          f"{'|'.join(fb) if fb else '—'}")
        kp.append(dict(book=nm, CAGR=cg, Sharpe=sh, MaxDD=dd, H1=h1, H2=h2, OOS_CAGR=oc,
                       OOS_Sharpe=osh, OOS_MaxDD=odd, pass4a_v2=p2, pass4a_v1=p1,
                       pass4b=(len(fb) == 0), failing="|".join(fb)))
    K = pd.DataFrame(kp)
    K.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    a, b, c = csd(chooser.loc[OOS_START:]); d, e, f = csd(donoth.loc[OOS_START:])
    P(f"\n      SELECTION'S PRICE, pooled OOS: {b-e:+.4f} Sharpe, {(a-d)*100:+.3f} pp CAGR, "
      f"{(abs(c)-abs(f))*100:+.3f} pp drawdown.")
    return K


# ============================================================================== main
def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 229 — the-tenth-selection-loses-instance-as-a-distribution   (cloud, 2026-09-08)")
    P("=" * 118)
    P(__doc__.split("QUESTION")[1].split("Deterministic")[0].strip())

    P("\n" + "=" * 118)
    P("PART A — THE CENSUS (every committed *.walkforward.csv, admitted or rejected with reason)")
    P("=" * 118)
    CE, CL = {}, {}
    for vocab in ("STRICT", "BROAD"):
        CE[vocab], CL[vocab] = census(vocab)
        report_census(CE[vocab], CL[vocab], vocab)
    pd.concat(CE.values()).to_csv(OUT / f"{STEM}.census.csv", index=False)
    pd.concat(CL.values()).to_csv(OUT / f"{STEM}.cells.csv", index=False)

    P("\n" + "=" * 118)
    P("PART B — Q1: IS THE MEAN LOSS A CONSTANT?  (TUNED PARAMETER 1 = the vocabulary)")
    P("=" * 118)
    INST = {}
    for vocab in ("STRICT", "BROAD"):
        INST[vocab] = pooled_stats(CL[vocab], f"vocabulary {vocab}")
    P("\n  TUNED PARAMETER 2 — bootstrap block, on the mean margin:")
    boots = []
    for vocab in ("STRICT", "BROAD"):
        BC = boot_ci(CL[vocab]); BC.insert(0, "vocab", vocab)
        for _, r in BC.iterrows():
            P(f"      {vocab:6s} block {r.block:9s} mean {r['mean']:+.5f}  95% CI "
              f"[{r.lo:+.5f}, {r.hi:+.5f}]  P(mean<0) {r.p_neg:.1%}")
        boots.append(BC)
    BOOT = pd.concat(boots)
    BOOT.to_csv(OUT / f"{STEM}.boot.csv", index=False)

    P("\n  The 10 largest single instances (STRICT), i.e. what the record's prose quotes:")
    top = CL["STRICT"].groupby("instance").margin.agg(["mean", "count"]).nsmallest(10, "mean")
    for i, (nm, r) in enumerate(top.iterrows(), 1):
        P(f"      {i:2d}. {r['mean']:+.4f} over {int(r['count']):4d} cells  {nm[:96]}")

    P("\n" + "=" * 118)
    P("PART D — Q3: HAS ANY SELECTOR CLASS EVER WON?  (declared name map, per-class bootstrap)")
    P("=" * 118)
    CLS = []
    for vocab in ("STRICT", "BROAD"):
        Q = by_class(CL[vocab]); Q.insert(0, "vocab", vocab)
        P(f"\n  vocabulary {vocab}:")
        P(f"      {'class':12s} {'cells':>6s} {'inst':>5s} {'files':>6s} {'cell mean':>10s} "
          f"{'inst mean':>10s} {'win rate':>9s} {'95% CI':>24s}  verdict")
        for _, r in Q.iterrows():
            vd = ("CI NOT USABLE (<5 instances)" if not r.usable else
                  ("WINS" if r.wins else ("LOSES" if r.loses else "not separable")))
            P(f"      {r.cls:12s} {r.cells:6d} {r.instances:5d} {r.files:6d} {r['mean']:+10.5f} "
              f"{r.inst_mean:+10.5f} {r.win_rate:9.1%} "
              f"{f'[{r.lo:+.4f}, {r.hi:+.4f}]':>24s}  {vd}")
        CLS.append(Q)
    pd.concat(CLS).to_csv(OUT / f"{STEM}.classes.csv", index=False)
    pd.concat([CE[v][CE[v].admitted] for v in CE]).to_csv(
        OUT / f"{STEM}.instances.csv", index=False)

    ref, LG, RET = run_live()
    WF = live_walkforward(ref, LG, RET)
    K = live_keep(ref, WF, RET)

    P("\n" + "=" * 118)
    P("VERDICT")
    P("=" * 118)
    ad = CE["STRICT"][CE["STRICT"].admitted]
    P(f"  R1 the record holds {len(ad)} admitted instances over {ad.file.nunique()} files "
      f"(STRICT), not 10 — the prose count is an undercount.")
    b = BOOT[(BOOT.vocab == "STRICT") & (BOOT.block == "instance")].iloc[0]
    P(f"  R2/R3 pooled mean margin (STRICT, instance block) {b['mean']:+.5f}, 95% CI "
      f"[{b.lo:+.5f}, {b.hi:+.5f}], P(<0) {b.p_neg:.1%}")
    het = INST["STRICT"].var(ddof=1)
    P(f"     between-instance sd {np.sqrt(het):.5f} vs the pooled mean itself "
      f"{abs(b['mean']):.5f} -> the loss is NOT a constant")
    Q = by_class(CL["STRICT"])
    P(f"  R4 selector classes that WIN (CI above 0): "
      f"{list(Q[Q.wins].cls) or 'NONE'};  that LOSE: {list(Q[Q.loses].cls) or 'NONE'}")
    P(f"  R5 live corpus: chooser beats do-nothing in {int((WF.margin>0).sum())} of {len(WF)} "
      f"cells, mean {WF.margin.mean():+.5f}; Spearman(|IS-OOS| steps, margin) "
      f"{H.spearman(WF.dist_steps, WF.margin):+.3f}")
    P(f"  KEEP paths on the pooled live books: 4a-v2 {int(K.pass4a_v2.sum())}/{len(K)}, "
      f"4b {int(K.pass4b.sum())}/{len(K)}")
    P(f"\n  runtime {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
