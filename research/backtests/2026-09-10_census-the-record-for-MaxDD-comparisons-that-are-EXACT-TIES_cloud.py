#!/usr/bin/env python3
"""Idea 594 - "census-the-record-for-MaxDD-comparisons-that-are-EXACT-TIES" (cloud lane).

The finding this run exists to price
------------------------------------
Idea 592 found that the record's flip flag `sign(A-U) != sign(A-M)` counts an EXACT TIE as a
sign change, because np.sign(0) == 0.  On idea 584's block-shuffle population 342 of 785 MaxDD
"flips" (43.6%) are ties, and 166 of those labels move under a 3.7e-4 price restatement.  It
also reported the other side: on the 216 REAL published de-gross cells the tie count is ZERO.

So the queue's question is a counting question about the RECORD, not about a shuffle:

    Q1 (CENSUS)     Across every published MaxDD/Calmar comparison the record has committed,
                    how many are TIES (|delta| < bar) rather than differences?
    Q2 (EXPOSURE)   Where a tie occurs, what does the published convention DO with it?  A tie
                    is a PASS under `>=` (PROTOCOL 4a's MaxDD leg), a PASS under `<=` (4b's DD
                    cap), a FAIL under `>`, and a FLIP under np.sign.  Count the comparison
                    SITES by operator, from the source, so the exposure is measured not assumed.
    Q3 (MECHANISM)  Are ties an artefact of synthetic populations only?  Build a fresh
                    record-shaped population of de-gross clauses vs their own ungated controls
                    and measure the tie rate directly, its structural predicate, and its
                    stability under a price restatement.

Q1 and Q3 are different questions and this file keeps them apart: Q1 counts what is committed,
Q3 measures what the record's own construction produces.  Neither is evidence for the other.

Readings (tuned parameter 1 = metric set; every value reported)
    METRICSET   {MAXDD} and {MAXDD, CALMAR}
Tie bar (tuned parameter 2; every value reported, the queue's 1e-12 is the headline)
    TIEBAR      1e-12, 1e-9, 1e-6, 1e-4, 1e-3

Census readings over the committed record (research/backtests/*.csv[.gz], *.py)
    A  DELTA columns   a column that IS a published difference (dMaxDD, d_OOS_MaxDD, OOS_dMaxDD,
                       dMaxDD@25, dCalmar ...).  Every finite cell is one published delta.
    B  PAIR columns    two LEVEL columns in the same row that differ only by a BOOK-ROLE token
                       (ctl_/ctrl_/base_/spy_/v2_/gate_/static_/nogate_/EWall_/arm_/...), i.e.
                       arm-vs-control as published.  Window tokens (IS/OOS/H1/H2/full) are NOT
                       roles, so `IS_MaxDD` vs `OOS_MaxDD` is never counted as a comparison.
    C  SOURCE sites    an AST walk over all committed backtest scripts for Compare nodes and
                       np.sign calls whose operands name MaxDD/Calmar: the operator inventory
                       that decides what a tie MEANS in each published verdict.
    Readings A and B are UPPER BOUNDS on "published comparisons" in ideas 276/286/523's sense:
    a column pair is a NAME, not proof a human quoted it.  Whole-column-identical pairs (a
    duplicated column, or a reference row compared with itself) are counted and reported
    SEPARATELY rather than silently inflating the tie share.

Generative population (Q3), PROTOCOL-compliant, both KEEP paths, rule 8
    Book        EWALL(G): equal weight every name above its own 200d MA with vol20 < 0.60,
                at G/E_t, weekly, 10 bps, next-day execution (the record's standard base book).
    Clauses     BREADTH(B) panel breadth < B; SPYTR(s) SPY/MA200-1 < s; VOL(v) panel median
                vol20 > v.  Each carries the book at (1-depth) when ON.  3 forms x 3 levels x
                3 depths x 2 cadences x 2 gross x 3 cost rungs x 3 panels = 972 arm-vs-control
                MaxDD comparisons, each against its OWN ungated parent at the same gross/rung.
    Predicate   BIND = max de-gross depth applied inside the CONTROL's binding drawdown episode
                (peak -> trough).  Structural tie <=> BIND == 0 and no switch cost inside the
                episode: the arm/control equity RATIO is then constant across the episode.
    Restatement prices rounded to 2 decimals (a real restatement of the same asset, median
                relative move reported); every label recomputed and the movers counted.

Verdicts, evaluated at EVERY grid point (PROTOCOL rule 4)
    4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2's.
    4b  Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's.
Rule 8 walk-forward: (level, depth) chosen on 2009-2016 IS Sharpe alone, 2017-2026 read once.

Data: committed caches only, no network.  SURVIVORSHIP: all three panels are current-constituent
lists (the small panel additionally drops the 46 names with max_1d_move >= 1.0 per data/
small_meta.csv), so CAGR/drawdown LEVELS are optimistic; the arm-vs-control CONTRASTS and the
tie counts are the durable part.  Deterministic, standalone; modifies nothing.
"""
import ast
import gzip
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v1_weights, rules_v2_weights
from engine import backtest, metrics, rebalance_mask

SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"

FREQ = "W"
MAX_VOL = 0.60
GROSSES = [0.75, 1.00]
G_HEAD = 0.75
DEPTHS = [0.25, 0.50, 1.00]
RUNGS = [0, 10, 25]
RUNG_HEAD = 10
CADENCES = ["D", "W"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
BARS = [1e-12, 1e-9, 1e-6, 1e-4, 1e-3]
BAR_HEAD = 1e-12
METRICSETS = {"MAXDD": ("maxdd",), "MAXDD+CALMAR": ("maxdd", "calmar")}

FAMS = {"BREADTH": [0.30, 0.40, 0.50],
        "SPYTR": [-0.05, 0.00, 0.03],
        "VOL": [0.20, 0.25, 0.30]}

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)

LINES = []


def log(s=""):
    print(s)
    LINES.append(str(s))


# ============================================================ census machinery
DD_RE = re.compile(r"(maxdd|max_dd)", re.I)
CAL_RE = re.compile(r"calmar", re.I)
DELTA_RE = re.compile(r"(^|_)(d|delta|gap)_?(oos_|is_|full_)?(maxdd|max_dd|calmar)", re.I)
BOOL_RE = re.compile(r"(flip|sign|pass|fail|better|worse|wins?|tie)", re.I)
ROLES = {"spy", "spytr", "v1", "v2", "base", "ctl", "ctrl", "control", "ewall", "ew",
         "nogate", "static", "gate", "arm", "parent", "pick", "best", "clause", "ungated",
         "matched", "sleeve", "ref", "live", "oracle", "dn", "lad", "a", "u", "m",
         "old", "new", "alt", "twin", "bench", "benchmark", "rules", "book", "child"}


def _metric_family(col):
    if CAL_RE.search(col):
        return "calmar"
    if DD_RE.search(col):
        return "maxdd"
    return None


def _strip_role(col):
    """Drop one leading and/or one trailing BOOK-ROLE token.  Window tokens are not roles."""
    parts = [p for p in col.split("_") if p != ""]
    if not parts:
        return col, False
    hit = False
    if len(parts) > 1 and parts[0].lower() in ROLES:
        parts = parts[1:]
        hit = True
    if len(parts) > 1 and parts[-1].lower() in ROLES:
        parts = parts[:-1]
        hit = True
    return "_".join(parts), hit


def classify_columns(cols):
    """-> (delta_cols, pairs) for one artefact header."""
    deltas, levels = [], []
    for c in cols:
        fam = _metric_family(c)
        if fam is None or BOOL_RE.search(c):
            continue
        (deltas if DELTA_RE.search(c) else levels).append((c, fam))
    pairs = []
    for i in range(len(levels)):
        for j in range(i + 1, len(levels)):
            c1, f1 = levels[i]
            c2, f2 = levels[j]
            if f1 != f2:
                continue
            n1, h1 = _strip_role(c1)
            n2, h2 = _strip_role(c2)
            if n1.lower() == n2.lower() and (h1 or h2):
                pairs.append((c1, c2, f1))
    return deltas, pairs


def _open(path):
    return gzip.open(path, "rt") if str(path).endswith(".gz") else open(path, "r")


def census_artefacts(files):
    """Readings A and B over every committed csv artefact.  One row per published comparison
    GROUP (file x column-or-pair), carrying the tie counts at every bar."""
    rows, bad = [], 0
    for f in files:
        try:
            with _open(f) as fh:
                header = fh.readline().rstrip("\n")
            cols = [c.strip().strip('"') for c in header.split(",")]
            deltas, pairs = classify_columns(cols)
            if not deltas and not pairs:
                continue
            need = sorted({c for c, _ in deltas} | {c for a, b, _ in pairs for c in (a, b)})
            df = pd.read_csv(f, usecols=lambda c: c.strip().strip('"') in need,
                             low_memory=False)
            df.columns = [c.strip().strip('"') for c in df.columns]
        except Exception:
            bad += 1
            continue
        for c, fam in deltas:
            if c not in df.columns:
                continue
            v = pd.to_numeric(df[c], errors="coerce").dropna()
            if v.empty:
                continue
            rows.append(dict(file=Path(f).name, reading="A_delta", metric=fam, col=c, other="",
                             n=len(v), whole_identical=False,
                             **{f"tie_{b:g}": int((v.abs() < b).sum()) for b in BARS}))
        for c1, c2, fam in pairs:
            if c1 not in df.columns or c2 not in df.columns:
                continue
            a = pd.to_numeric(df[c1], errors="coerce")
            b = pd.to_numeric(df[c2], errors="coerce")
            ok = a.notna() & b.notna()
            if not ok.any():
                continue
            d = (a[ok] - b[ok]).abs()
            rows.append(dict(file=Path(f).name, reading="B_pair", metric=fam, col=c1, other=c2,
                             n=int(ok.sum()), whole_identical=bool((d < 1e-15).all()),
                             **{f"tie_{bb:g}": int((d < bb).sum()) for bb in BARS}))
    return pd.DataFrame(rows), bad


def census_sources(pyfiles):
    """Reading C: every Compare / np.sign site in committed source whose operands name
    MaxDD or Calmar, with the operator that decides what a TIE means there."""
    rows = []
    opname = {ast.Gt: ">", ast.GtE: ">=", ast.Lt: "<", ast.LtE: "<=", ast.Eq: "==",
              ast.NotEq: "!=", ast.Is: "is", ast.IsNot: "is not", ast.In: "in",
              ast.NotIn: "not in"}
    tie_effect = {">": "FAIL", ">=": "PASS", "<": "FAIL", "<=": "PASS", "==": "PASS",
                  "!=": "FAIL", "sign": "FLIP"}
    for f in pyfiles:
        try:
            src = f.read_text()
            tree = ast.parse(src)
        except Exception:
            continue
        srclines = src.splitlines(keepends=True)

        def seg_of(node):
            """Own source slice (ast.get_source_segment re-splits the file on every call)."""
            a, b = getattr(node, "lineno", None), getattr(node, "end_lineno", None)
            if a is None or b is None:
                return ""
            if a == b:
                return srclines[a - 1][node.col_offset:node.end_col_offset]
            out = [srclines[a - 1][node.col_offset:]] + srclines[a:b - 1]
            out.append(srclines[b - 1][:node.end_col_offset])
            return "".join(out)

        for node in ast.walk(tree):
            if isinstance(node, ast.Compare):
                seg = seg_of(node)
                if not (DD_RE.search(seg) or CAL_RE.search(seg)):
                    continue
                fam = "calmar" if CAL_RE.search(seg) else "maxdd"
                for op in node.ops:
                    o = opname.get(type(op), type(op).__name__)
                    rows.append(dict(file=f.name, kind="compare", op=o, metric=fam,
                                     tie=tie_effect.get(o, "?"), line=node.lineno,
                                     src=" ".join(seg.split())[:160]))
            elif isinstance(node, ast.Call):
                fn = seg_of(node.func)
                if not fn.endswith("sign"):
                    continue
                seg = seg_of(node)
                if not (DD_RE.search(seg) or CAL_RE.search(seg)):
                    continue
                rows.append(dict(file=f.name, kind="sign", op="sign",
                                 metric="calmar" if CAL_RE.search(seg) else "maxdd",
                                 tie="FLIP", line=node.lineno,
                                 src=" ".join(seg.split())[:160]))
    return pd.DataFrame(rows)


# ============================================================ book machinery
def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def ewall_weights(px, gross):
    e = eligible_mask(px).astype(float)
    n = e.sum(axis=1).replace(0, np.nan)
    return e.div(n, axis=0).mul(gross).fillna(0.0)


def breadth(px):
    above = px > px.rolling(200).mean()
    return above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)


def spytr(px):
    spy = px["SPY"]
    return spy / spy.rolling(200).mean() - 1.0


def medvol(px):
    return (px.pct_change().rolling(20).std() * np.sqrt(252)).median(axis=1)


def signal(px, fam):
    return {"BREADTH": breadth, "SPYTR": spytr, "VOL": medvol}[fam](px)


def gate_on(sig, fam, level):
    """ON == de-grossed.  BREADTH/SPYTR fire LOW, VOL fires HIGH (pre-registered directions)."""
    return (sig > level) if fam == "VOL" else (sig < level)


def gate_mult(px, sig, fam, level, depth, cadence):
    on = gate_on(sig, fam, level)
    m = pd.Series(1.0, index=px.index).where(~on, 1.0 - depth)
    m = m.where(sig.notna(), 1.0)
    if cadence == "W":
        mask = rebalance_mask(px.index, FREQ)
        m = m.where(mask).ffill().fillna(1.0)
    return m


def apply_gate(r_base, mult, gross, cost_bps):
    m_eff = mult.reindex(r_base.index).shift(1).fillna(1.0)
    switch = m_eff.diff().abs().fillna(0.0)
    return m_eff * r_base - switch * gross * cost_bps / 1e4, m_eff


def maxdd(r):
    eq = (1 + r).cumprod()
    return float((eq / eq.cummax() - 1).min())


def binding_episode(r):
    """(peak_date, trough_date) of the control's MaxDD episode."""
    eq = (1 + r).cumprod()
    dd = eq / eq.cummax() - 1
    trough = dd.idxmin()
    peak = eq.loc[:trough].idxmax()
    return peak, trough


def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def tests_4b(r, spy):
    h1, h2 = half_sharpes(r)
    s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    return {"H1": h1 > s1, "H2": h2 > s2,
            "OOS": metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"],
            "DD": abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]),
            "CAGR": m["CAGR"] >= 0.70 * ms["CAGR"]}


def verdict_4a(r, base):
    h1, h2 = half_sharpes(r)
    b1, b2 = half_sharpes(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def small_panel():
    """The sub-$2B panel with the 1d-move outliers dropped, per the standing instruction."""
    px = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad)


# ============================================================ population run
def run_panel(panel, px, tag=""):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    sigs = {f: signal(px, f) for f in FAMS}

    base0, v2_0, v1_0 = {}, None, None
    for g in GROSSES:
        res = backtest(px, ewall_weights(px, g), cost_bps=0, freq=FREQ)
        base0[g] = (res["returns"].loc[start:], res["turnover"].loc[start:])
    rv2 = backtest(px, rules_v2_weights(px), cost_bps=0, freq=FREQ)
    rv1 = backtest(px, rules_v1_weights(px), cost_bps=0, freq=FREQ)

    def rung(pair, c):
        r, t = pair
        return r - t * c / 1e4

    refs = {c: dict(v2=rung((rv2["returns"].loc[start:], rv2["turnover"].loc[start:]), c),
                    v1=rung((rv1["returns"].loc[start:], rv1["turnover"].loc[start:]), c))
            for c in RUNGS}

    mults = {}
    for fam, levels in FAMS.items():
        for lv in levels:
            for d in DEPTHS:
                for cad in CADENCES:
                    mults[(fam, lv, d, cad)] = gate_mult(px, sigs[fam], fam, lv, d, cad).loc[start:]

    rows = []
    for c in RUNGS:
        v2 = refs[c]["v2"]
        for g in GROSSES:
            rb = rung(base0[g], c)
            ctrl_dd = maxdd(rb)
            peak, trough = binding_episode(rb)
            mc = metrics(rb)
            tc = tests_4b(rb, spy)
            rows.append(dict(
                panel=panel, restate=tag, rung=c, gross=g, family="NOGATE", level=np.nan,
                depth=0.0, cadence="-", on_share=0.0, mean_mult=1.0,
                arm_MaxDD=ctrl_dd, ctrl_MaxDD=ctrl_dd, dMaxDD=0.0,
                arm_Calmar=mc["Calmar"], ctrl_Calmar=mc["Calmar"], dCalmar=0.0,
                BIND=0.0, switch_in_episode=0.0, struct=True,
                CAGR=mc["CAGR"], Sharpe=mc["Sharpe"], H1=half_sharpes(rb)[0],
                H2=half_sharpes(rb)[1], IS_Sharpe=metrics(rb.loc[:IS_END])["Sharpe"],
                OOS_CAGR=metrics(rb.loc[OOS_START:])["CAGR"],
                OOS_Sharpe=metrics(rb.loc[OOS_START:])["Sharpe"],
                OOS_MaxDD=metrics(rb.loc[OOS_START:])["MaxDD"],
                ctrl_Sharpe=mc["Sharpe"], ctrl_CAGR=mc["CAGR"],
                ctrl_OOS_Sharpe=metrics(rb.loc[OOS_START:])["Sharpe"],
                p4a=verdict_4a(rb, v2), p4b=all(tc.values()),
                fail4b=",".join([k for k, v in tc.items() if not v]) or "-"))
            for fam, levels in FAMS.items():
                for lv in levels:
                    for d in DEPTHS:
                        for cad in CADENCES:
                            m = mults[(fam, lv, d, cad)]
                            rg, me = apply_gate(rb, m, g, c)
                            win = (me.index >= peak) & (me.index <= trough)
                            bind = float(1.0 - me[win].min())
                            sw = float(me.diff().abs().fillna(0.0)[win].sum())
                            mg = metrics(rg)
                            t4b = tests_4b(rg, spy)
                            rows.append(dict(
                                panel=panel, restate=tag, rung=c, gross=g, family=fam, level=lv,
                                depth=d, cadence=cad,
                                on_share=float((me < 1.0).mean()), mean_mult=float(me.mean()),
                                arm_MaxDD=mg["MaxDD"], ctrl_MaxDD=ctrl_dd,
                                dMaxDD=mg["MaxDD"] - ctrl_dd,
                                arm_Calmar=mg["Calmar"], ctrl_Calmar=mc["Calmar"],
                                dCalmar=mg["Calmar"] - mc["Calmar"],
                                BIND=bind, switch_in_episode=sw,
                                struct=bool(bind <= 0.0 and sw <= 0.0),
                                CAGR=mg["CAGR"], Sharpe=mg["Sharpe"],
                                H1=half_sharpes(rg)[0], H2=half_sharpes(rg)[1],
                                IS_Sharpe=metrics(rg.loc[:IS_END])["Sharpe"],
                                OOS_CAGR=metrics(rg.loc[OOS_START:])["CAGR"],
                                OOS_Sharpe=metrics(rg.loc[OOS_START:])["Sharpe"],
                                OOS_MaxDD=metrics(rg.loc[OOS_START:])["MaxDD"],
                                ctrl_Sharpe=mc["Sharpe"], ctrl_CAGR=mc["CAGR"],
                                ctrl_OOS_Sharpe=metrics(rb.loc[OOS_START:])["Sharpe"],
                                p4a=verdict_4a(rg, v2), p4b=all(t4b.values()),
                                fail4b=",".join([k for k, v in t4b.items() if not v]) or "-"))

    # ---- rule 8 walk-forward: (level, depth) chosen on IS Sharpe alone, at G_HEAD
    wf = []
    for c in RUNGS:
        rb = rung(base0[G_HEAD], c)
        for fam, levels in FAMS.items():
            for cad in CADENCES:
                cells = {}
                for lv in levels:
                    for d in DEPTHS:
                        rg, _ = apply_gate(rb, mults[(fam, lv, d, cad)], G_HEAD, c)
                        cells[(lv, d)] = rg
                is_s = {k: metrics(v.loc[:IS_END])["Sharpe"] for k, v in cells.items()}
                oos = {k: metrics(v.loc[OOS_START:]) for k, v in cells.items()}
                pick = min(is_s, key=lambda k: (-is_s[k], k[0], k[1]))
                best = max(oos, key=lambda k: oos[k]["Sharpe"])
                nog = metrics(rb.loc[OOS_START:])
                wf.append(dict(panel=panel, restate=tag, family=fam, rung=c, cadence=cad,
                               pick_level=pick[0], pick_depth=pick[1], IS_Sharpe=is_s[pick],
                               OOS_CAGR=oos[pick]["CAGR"], OOS_Sharpe=oos[pick]["Sharpe"],
                               OOS_MaxDD=oos[pick]["MaxDD"],
                               nogate_OOS_Sharpe=nog["Sharpe"], nogate_OOS_CAGR=nog["CAGR"],
                               nogate_OOS_MaxDD=nog["MaxDD"],
                               grid_mean_OOS=float(np.mean([oos[k]["Sharpe"] for k in oos])),
                               best_OOS=oos[best]["Sharpe"],
                               regret=oos[pick]["Sharpe"] - oos[best]["Sharpe"],
                               vs_nogate=oos[pick]["Sharpe"] - nog["Sharpe"],
                               spy_OOS=metrics(spy.loc[OOS_START:])["Sharpe"],
                               v2_OOS=metrics(refs[c]["v2"].loc[OOS_START:])["Sharpe"]))
    return pd.DataFrame(rows), pd.DataFrame(wf), spy


# ============================================================ main
def main():
    log("=" * 150)
    log(f"Idea 594 census-the-record-for-MaxDD-comparisons-that-are-EXACT-TIES (cloud) | {SCRIPT}")
    log("=" * 150)
    log("Q1 how many published MaxDD/Calmar comparisons are TIES; Q2 what the published operator")
    log("   DOES with a tie; Q3 does the record's own construction produce ties at all.")
    log(f"Tuned (2): metric set {list(METRICSETS)} x tie bar {BARS} - every value reported.")

    # ---------------- [0] reproduction gates
    log("\n" + "=" * 150)
    log("[0] REPRODUCTION GATES")
    px0 = load_universe()
    r0 = backtest(px0, ewall_weights(px0, 0.75), cost_bps=0, freq=FREQ)
    r25 = backtest(px0, ewall_weights(px0, 0.75), cost_bps=25, freq=FREQ)
    g1 = float((r0["returns"] - r0["turnover"] * 25 / 1e4 - r25["returns"]).abs().max())
    log(f"  G1 derived cost rung r(c)=r(0)-turnover*c/1e4 vs engine.backtest(25): {g1:.3e} "
        f"-> {'PASS' if g1 < 1e-12 else 'FAIL'}")
    assert g1 < 1e-12

    s = px0.index[260]
    r85 = backtest(px0, ewall_weights(px0, 0.85), cost_bps=10, freq=FREQ)["returns"].loc[s:]
    m85 = metrics(r85)
    h1, h2 = half_sharpes(r85)
    ok2 = (abs(m85["CAGR"] - 0.118) < 1e-3 and abs(m85["Sharpe"] - 1.05) < 6e-3
           and abs(m85["MaxDD"] + 0.179) < 1e-3)
    log(f"  G2 idea 84's ungated EWALL U56 g=0.85 @10bps (committed 11.8% / 1.05 / -17.9% / "
        f"H 1.07 / 1.04): {m85['CAGR']:.3%} / {m85['Sharpe']:.3f} / {m85['MaxDD']:.3%} / "
        f"H {h1:.2f} / {h2:.2f} -> {'PASS' if ok2 else 'FAIL (reported, not silenced)'}")

    g3 = float(abs(maxdd(r85) - m85["MaxDD"]))
    log(f"  G3 local maxdd() vs engine.metrics()['MaxDD']: {g3:.3e} "
        f"-> {'PASS' if g3 == 0.0 else 'FAIL'}")
    assert g3 == 0.0

    # G4: census machinery on a planted file with a KNOWN answer
    tmp = OUT / f"{STEM}.gatecheck.csv"
    plant = pd.DataFrame({"ctl_OOS_MaxDD": [-0.10, -0.20, -0.30, np.nan],
                          "OOS_MaxDD": [-0.10, -0.25, -0.30 + 1e-10, -0.4],
                          "dMaxDD": [0.0, 0.05, 1e-13, np.nan],
                          "IS_MaxDD": [-0.11, -0.21, -0.31, -0.41],
                          "flip_MaxDD": [True, False, True, False]})
    plant.to_csv(tmp, index=False)
    cg, _ = census_artefacts([tmp])
    tmp.unlink()
    pair = cg[cg.reading == "B_pair"]
    dl = cg[cg.reading == "A_delta"]
    ok4 = (len(pair) == 1 and pair.iloc[0]["other"] in ("OOS_MaxDD", "ctl_OOS_MaxDD")
           and int(pair.iloc[0]["n"]) == 3 and int(pair.iloc[0]["tie_1e-12"]) == 1
           and int(pair.iloc[0]["tie_1e-09"]) == 2
           and len(dl) == 1 and int(dl.iloc[0]["n"]) == 3
           and int(dl.iloc[0]["tie_1e-12"]) == 2)
    log(f"  G4 census machinery on a planted artefact (1 pair found, IS/OOS not paired, "
        f"flip_ column excluded, ties 1 @1e-12 / 2 @1e-9, delta ties 2): "
        f"-> {'PASS' if ok4 else 'FAIL'}")
    assert ok4, cg.to_string()

    # ---------------- [1] census A/B over the committed artefacts
    log("\n" + "=" * 150)
    log("[1] CENSUS, readings A (published DELTA columns) and B (published arm-vs-control PAIRS)")
    files = sorted(OUT.glob("*.csv")) + sorted(OUT.glob("*.csv.gz"))
    files = [f for f in files if not f.name.startswith(STEM)]
    log(f"  committed csv artefacts scanned: {len(files)}")
    cen, bad = census_artefacts(files)
    log(f"  unreadable/skipped: {bad}   comparison groups found: {len(cen)}")
    cen.to_csv(OUT / f"{STEM}.census.csv", index=False)

    for msname, fams in METRICSETS.items():
        sub = cen[cen.metric.isin(fams)]
        log(f"\n  --- METRICSET = {msname} ---")
        for reading in ("A_delta", "B_pair"):
            r = sub[sub.reading == reading]
            if r.empty:
                log(f"    {reading}: none")
                continue
            n = int(r["n"].sum())
            wi = r[r.whole_identical]
            log(f"    {reading}: {len(r)} groups in {r.file.nunique()} files, "
                f"{n:,} published comparisons "
                f"({len(wi)} groups whole-column-identical, {int(wi['n'].sum()):,} of those cells)")
            for b in BARS:
                t = int(r[f"tie_{b:g}"].sum())
                tn = int(r.loc[~r.whole_identical, f"tie_{b:g}"].sum())
                nn = int(r.loc[~r.whole_identical, "n"].sum())
                log(f"       bar {b:>7g}: ties {t:6,} / {n:,} = {t/max(n,1):7.4%}   "
                    f"excluding whole-identical groups: {tn:6,} / {nn:,} = {tn/max(nn,1):7.4%}")

    # cell-weighted vs FILE-weighted: a handful of very large draw artefacts can carry the
    # whole cell-weighted share, so both weightings are published side by side.
    per_file = (cen.groupby("file").agg(cells=("n", "sum"), ties=(f"tie_{BAR_HEAD:g}", "sum")))
    per_file["share"] = per_file.ties / per_file.cells
    log(f"\n  WEIGHTING: {len(per_file)} artefacts carry a comparison. "
        f"cell-weighted tie share {per_file.ties.sum()/max(per_file.cells.sum(),1):.4%}; "
        f"file-weighted (mean of per-file shares) {per_file.share.mean():.4%}; "
        f"median per-file share {per_file.share.median():.4%}; "
        f"files with ZERO ties {int((per_file.ties == 0).sum())} of {len(per_file)} "
        f"({(per_file.ties == 0).mean():.1%})")
    top = per_file.sort_values("ties", ascending=False).head(10)
    log(f"  the 10 tie-heaviest artefacts carry {int(top.ties.sum()):,} of "
        f"{int(per_file.ties.sum()):,} ties ({top.ties.sum()/max(per_file.ties.sum(),1):.1%}) "
        f"on {int(top.cells.sum()):,} of {int(per_file.cells.sum()):,} cells:")
    log(top.to_string(float_format=lambda x: f"{x:.4f}", max_colwidth=78))

    head = cen[cen[f"tie_{BAR_HEAD:g}"] > 0].copy()
    head["tie_share"] = head[f"tie_{BAR_HEAD:g}"] / head["n"]
    head = head.sort_values(f"tie_{BAR_HEAD:g}", ascending=False)
    log(f"\n  groups carrying at least one EXACT tie (|d| < {BAR_HEAD:g}): {len(head)}")
    if len(head):
        log(head.head(25)[["file", "reading", "metric", "col", "other", "n",
                           f"tie_{BAR_HEAD:g}", "tie_share", "whole_identical"]]
            .to_string(index=False, max_colwidth=62))
    log("\n  pair inventory (normalised comparison shapes, top 20 by cells):")
    inv = (cen[cen.reading == "B_pair"].assign(shape=lambda d: d.col + " vs " + d.other)
           .groupby("shape").agg(files=("file", "nunique"), cells=("n", "sum"),
                                 ties=(f"tie_{BAR_HEAD:g}", "sum"))
           .sort_values("cells", ascending=False))
    log(inv.head(20).to_string())

    # ---------------- [2] census C: what the published operator does with a tie
    log("\n" + "=" * 150)
    log("[2] CENSUS, reading C (SOURCE): the operator inventory that decides what a TIE means")
    pys = sorted(OUT.glob("*.py")) + [REPO / "research" / "baseline.py"]
    pys = [p for p in pys if p.name != SCRIPT]
    src = census_sources(pys)
    src.to_csv(OUT / f"{STEM}.sites.csv", index=False)
    log(f"  committed scripts parsed: {len(pys)}   MaxDD/Calmar comparison sites: {len(src)}")
    for msname, fams in METRICSETS.items():
        s2 = src[src.metric.isin(fams)]
        piv = (s2.groupby(["op", "tie"]).size().rename("sites").reset_index()
               .sort_values("sites", ascending=False))
        log(f"\n  --- METRICSET = {msname} : {len(s2)} sites in {s2.file.nunique()} files ---")
        log(piv.to_string(index=False))
        eff = s2.groupby("tie").size()
        tot = max(len(s2), 1)
        log("   tie effect: " + ", ".join(f"{k} {v} ({v/tot:.1%})" for k, v in eff.items()))
    sg = src[src.kind == "sign"]
    log(f"\n  np.sign sites on a MaxDD/Calmar operand (the flip channel idea 592 named): "
        f"{len(sg)} in {sg.file.nunique() if len(sg) else 0} files")
    if len(sg):
        log(sg[["file", "line", "src"]].head(15).to_string(index=False, max_colwidth=110))

    # ---------------- [3] the record's own construction: does it produce ties?
    log("\n" + "=" * 150)
    log("[3] GENERATIVE POPULATION - fresh record-shaped arm-vs-control comparisons")
    panels = []
    px_u = load_universe()
    panels.append(("U56", px_u))
    px_b = load_universe(broad=True)
    panels.append(("B136", px_b))
    px_s, ndrop = small_panel()
    log(f"  small panel: {px_s.shape[1]-1} names after dropping {ndrop} with max_1d_move >= 1.0")
    panels.append((f"SMALL{px_s.shape[1]-1}", px_s))

    grids, wfs, spys = [], [], {}
    for name, px in panels:
        yrs = px.index.to_series().groupby(px.index.year).count()
        if yrs.loc[2015:2024].max() > 300:
            log(f"!! {name}: CALENDAR-DAY INDEX DETECTED - aborting.")
            sys.exit(1)
        g, w, spy = run_panel(name, px)
        grids.append(g)
        wfs.append(w)
        spys[name] = spy
        log(f"  {name}: {px.shape[1]} cols, {px.index[0].date()} -> {px.index[-1].date()}, "
            f"{len(g)} arm-vs-control comparisons")
    allrows = pd.concat(grids, ignore_index=True)
    ctrl = allrows[allrows.family == "NOGATE"].copy()
    grid = allrows[allrows.family != "NOGATE"].copy()

    # ---- restatement: prices rounded to 2 decimals, same books re-run
    log("\n  RESTATEMENT: prices rounded to 2 decimals, every label recomputed")
    rgrids = []
    for name, px in panels:
        pxr = px.round(2)
        rel = float(((pxr - px).abs() / px.abs().replace(0, np.nan)).stack().median())
        log(f"    {name}: median relative price move {rel:.3e}")
        g, _, _ = run_panel(name, pxr, tag="round2")
        rgrids.append(g[g.family != "NOGATE"])
    rgrid = pd.concat(rgrids, ignore_index=True)
    allrows.to_csv(OUT / f"{STEM}.population.csv", index=False)
    rgrid.to_csv(OUT / f"{STEM}.population_restated.csv", index=False)

    key = ["panel", "rung", "gross", "family", "level", "depth", "cadence"]
    j = grid.set_index(key).join(rgrid.set_index(key), rsuffix="_r")

    log(f"\n  population: {len(grid)} comparisons "
        f"({grid.panel.nunique()} panels x {len(FAMS)} clause forms x 3 levels x {len(DEPTHS)} "
        f"depths x {len(CADENCES)} cadences x {len(GROSSES)} gross x {len(RUNGS)} rungs)")
    for msname, fams in METRICSETS.items():
        cols = ["dMaxDD"] + (["dCalmar"] if "calmar" in fams else [])
        log(f"    METRICSET {msname}: tie counts over {len(grid)*len(cols)} deltas")
        for b in BARS:
            t = int(sum((grid[c].abs() < b).sum() for c in cols))
            log(f"      bar {b:>7g}: {t:5d} ties = {t/(len(grid)*len(cols)):7.4%}")

    ties = grid["dMaxDD"].abs() < BAR_HEAD
    log(f"\n  MaxDD ties at {BAR_HEAD:g}: {int(ties.sum())} of {len(grid)} = {ties.mean():.4%}")
    log(f"  structural predicate BIND==0 and no switch cost inside the control's binding "
        f"episode: {int(grid.struct.sum())} of {len(grid)} arms")
    if int(grid.struct.sum()):
        log(f"    P(tie | struct)   = {grid.loc[grid.struct, 'dMaxDD'].abs().lt(BAR_HEAD).mean():.4f}")
    if int(ties.sum()):
        log(f"    P(struct | tie)   = {grid.loc[ties, 'struct'].mean():.4f}")
        log(f"    P(tie | ~struct)  = {grid.loc[~grid.struct, 'dMaxDD'].abs().lt(BAR_HEAD).mean():.4f}")
    log(f"  by ON-share: arms never ON (dead clause) {int((grid.on_share == 0).sum())}, "
        f"ON < 1% {int(((grid.on_share > 0) & (grid.on_share < 0.01)).sum())}")
    tab = (grid.assign(tie=ties).groupby(["panel", "family"])
           .agg(n=("dMaxDD", "size"), ties=("tie", "sum"), struct=("struct", "sum"),
                med_abs_dMaxDD=("dMaxDD", lambda x: float(x.abs().median())))
           )
    log("\n  ties and structural arms by panel x clause form:")
    log(tab.to_string(float_format=lambda x: f"{x:.5f}"))

    moved = int((j["dMaxDD"].abs().lt(BAR_HEAD) != j["dMaxDD_r"].abs().lt(BAR_HEAD)).sum())
    sflip = int((np.sign(j["dMaxDD"]) != np.sign(j["dMaxDD_r"])).sum())
    log(f"\n  under the restatement: tie labels that MOVE {moved} of {len(j)}; "
        f"sign(dMaxDD) changes {sflip} of {len(j)} "
        f"(median |dMaxDD| shift {float((j['dMaxDD']-j['dMaxDD_r']).abs().median()):.3e})")

    # ---------------- [4] KEEP paths + rule 8
    log("\n" + "=" * 150)
    log("[4] BOTH KEEP PATHS (every grid point) AND RULE 8")
    log(f"  4a passes: {int(grid.p4a.sum())} of {len(grid)};  "
        f"4b passes: {int(grid.p4b.sum())} of {len(grid)};  "
        f"BOTH: {int((grid.p4a & grid.p4b).sum())}")
    log("  4b failure reasons (first-listed set, all rows):")
    log(grid.fail4b.value_counts().head(12).to_string())
    log("\n  the UNGATED PARENTS at the same gross/rung (a gated arm inheriting a passing parent "
        "is NOT an edge):")
    log(ctrl[["panel", "rung", "gross", "CAGR", "Sharpe", "arm_MaxDD", "H1", "H2", "OOS_Sharpe",
              "p4a", "p4b"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    par = ctrl.set_index(["panel", "rung", "gross"])["p4b"]
    inh = grid.join(par.rename("parent_4b"), on=["panel", "rung", "gross"])
    log(f"  of the {int(grid.p4b.sum())} 4b passes, "
        f"{int((inh.p4b & inh.parent_4b).sum())} sit on a parent that already passes 4b; "
        f"{int((inh.p4b & ~inh.parent_4b).sum())} do not.")
    show = ["panel", "rung", "gross", "family", "level", "depth", "cadence", "on_share",
            "CAGR", "Sharpe", "arm_MaxDD", "H1", "H2", "OOS_Sharpe"]
    if int(grid.p4b.sum()):
        log("\n  4b passers NOT inherited from a passing parent:")
        nx = inh[inh.p4b & ~inh.parent_4b]
        log(nx[show + ["p4a"]].to_string(index=False, float_format=lambda x: f"{x:.3f}")
            if len(nx) else "    (none)")
    if int(grid.p4a.sum()):
        log("\n  4a passers:")
        log(grid[grid.p4a][show + ["p4b"]].to_string(index=False,
                                                     float_format=lambda x: f"{x:.3f}"))

    wf = pd.concat(wfs, ignore_index=True)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    log("\n  rule 8 walk-forward (IS 2009-2016 Sharpe chooses level+depth; OOS 2017-2026 read once):")
    log(wf[["panel", "family", "rung", "cadence", "pick_level", "pick_depth", "IS_Sharpe",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "nogate_OOS_Sharpe", "vs_nogate",
            "grid_mean_OOS", "best_OOS", "regret", "spy_OOS", "v2_OOS"]]
        .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    log(f"\n  IS-chosen cell beats DOING NOTHING (its own ungated parent) on OOS Sharpe in "
        f"{int((wf.vs_nogate > 0).sum())} of {len(wf)} cells; beats SPY OOS in "
        f"{int((wf.OOS_Sharpe > wf.spy_OOS).sum())}; beats RULES v2 OOS in "
        f"{int((wf.OOS_Sharpe > wf.v2_OOS).sum())}; mean regret {wf.regret.mean():.3f}")

    # ---------------- verdict
    log("\n" + "=" * 150)
    log("[5] VERDICT")
    n_all = int(cen["n"].sum())
    n_tie = int(cen[f"tie_{BAR_HEAD:g}"].sum())
    n_tie_x = int(cen.loc[~cen.whole_identical, f"tie_{BAR_HEAD:g}"].sum())
    n_all_x = int(cen.loc[~cen.whole_identical, "n"].sum())
    log(f"  CENSUS DELIVERED: {n_all:,} published MaxDD/Calmar comparisons across "
        f"{cen.file.nunique()} artefacts; {n_tie:,} ({n_tie/max(n_all,1):.4%}) are EXACT ties at "
        f"|d| < {BAR_HEAD:g}, {n_tie_x:,} ({n_tie_x/max(n_all_x,1):.4%}) once whole-column-identical "
        f"groups are excluded.")
    log(f"  EXPOSURE: {len(src)} source comparison sites; tie -> "
        + ", ".join(f"{k} {v}" for k, v in src.groupby('tie').size().items()))
    log(f"  GENERATIVE: {int(ties.sum())} ties in {len(grid)} record-shaped comparisons "
        f"({ties.mean():.4%}).")
    verdict = "KILL" if int(grid.p4a.sum()) == 0 and int(grid.p4b.sum()) == 0 else "SPLIT"
    log(f"  No book promoted from this run's grid: 4a {int(grid.p4a.sum())}, "
        f"4b {int(grid.p4b.sum())} of {len(grid)}.")

    row = (f"| 2026-09-10 | idea 594 census-MaxDD-EXACT-TIES (cloud) | census {n_all:,} published "
           f"MaxDD/Calmar comparisons, {n_tie:,} exact ties ({n_tie/max(n_all,1):.3%}); "
           f"generative {int(ties.sum())}/{len(grid)} ties; 4a {int(grid.p4a.sum())} / "
           f"4b {int(grid.p4b.sum())} of {len(grid)} | - | - | - | - | {verdict} | {SCRIPT} |")
    log("\nLEADERBOARD row:\n" + row)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    print("\nwrote:", STEM + ".{console.txt,census.csv,sites.csv,population.csv,"
          "population_restated.csv,walkforward.csv}")


if __name__ == "__main__":
    main()
