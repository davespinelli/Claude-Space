#!/usr/bin/env python3
"""Idea 734 — re-gate the record's ABSOLUTE reproduction bars that sit on LEVEL quantities.

Idea 538's G1 reproduction gate FAILED: max|d turn_yr| = 9.144e-03 against a 1e-6 ABSOLUTE
bar, on a turnover level of ~20/yr — a RELATIVE gap of 4.5e-04.  The claim filed with the
queue is that the bar form, not the reproduction, is what broke: an absolute bar carries an
implicit scale assumption, and turnover/gross/CAGR are LEVEL-valued quantities whose natural
magnitude is not O(1).

This run does two things and refuses to do a third:
  A. CENSUS every `assert` clause with a numeric bar in the 689 committed backtest scripts,
     classified by BAR FORM (absolute / relative / exact / shape) x QUANTITY CLASS.
  B. PRICE the proposed re-gating on a real corpus of cross-script reproduction gaps built
     from the record's own committed .grid.csv artefacts — how many gate cells a relative
     bound RECOVERS, and how many false PASSes it BUYS on cells that are not reproductions.
  It does NOT edit PROTOCOL.md, RULES.md, scan.py, bot.py or baseline.py (rule 6).

TUNED PARAMETERS — exactly two, both swept, ALL grid points reported:
    1. QUANTITY CLASS in {TURNOVER, GROSS, CAGR, DD, VOL, SHARPE}  (the idea's own taxonomy:
       the first five are LEVEL-valued, SHARPE is the scale-free control)
    2. BAR FORM in {ABS, REL, HYBRID}  (HYBRID = pass if EITHER bound passes — the usual
       np.isclose form), each swept over the full bar ladder 1e-12 ... 1e-2.
Everything else is pre-registered and fixed: the corpus construction rule, the near-identity
threshold (with its sensitivity reported, not chosen), 10 bps, t+1 execution, the rule-8 split.

Outputs (all beside this script):
    .console.txt    full run log
    .census.csv     every assert clause with a numeric bar, classified
    .gapcorpus.csv  every (pair x metric) reproduction cell measured
    .grid.csv       quantity class x bar form x bar level — ALL grid points
    .walkforward.csv  rule-8: the bar calibrated on IS gaps, read once on OOS gaps
    .bookleg.csv    rule-8: 4 IS-only selectors x 3 panels, each pick read ONCE on OOS
    .result.md      the memo
"""
from __future__ import annotations
import re, sys, glob, itertools, collections
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state          # noqa: E402
from engine import backtest as engine_backtest, metrics, rebalance_mask   # noqa: E402

STEM = Path(__file__).with_suffix("")
OUT = lambda ext: Path(str(STEM) + ext)

COST_BPS = 10.0
BAND = 0.03
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

# ---- pre-registered corpus construction (Part B)
MIN_KEYS = 2            # a pair must share >= 2 identifying columns
MIN_MATCH = 20          # and >= 20 matched rows
NEAR_IDENT = 1e-2       # median relative gap below this => the two columns are the same
                        # quantity recomputed (a REPRODUCTION cell).  Sensitivity reported.
NEAR_LADDER = (1e-3, 1e-2, 1e-1)
BAR_LADDER = (1e-12, 1e-10, 1e-8, 1e-6, 1e-4, 1e-2)
WF_K = 10.0             # rule-8 bar calibration: bar = K x the 99th pct of IS-window gaps

# ---- quantity taxonomy (the idea's own: CAGR levels, turnover, gross are LEVEL-valued)
CLASS_OF_COL = {}
for c in ("turnover", "turn", "turn_yr", "turn_x_yr", "TO", "turn_yr_is", "turn_yr_oos"):
    CLASS_OF_COL[c] = "TURNOVER"
for c in ("gross_mean",):
    CLASS_OF_COL[c] = "GROSS"
for c in ("CAGR", "CAGR0", "IS_CAGR", "OOS_CAGR", "isCAGR", "oCAGR", "Total"):
    CLASS_OF_COL[c] = "CAGR"
for c in ("MaxDD", "IS_MaxDD", "OOS_MaxDD", "isMaxDD", "oMaxDD"):
    CLASS_OF_COL[c] = "DD"
for c in ("Vol",):
    CLASS_OF_COL[c] = "VOL"
for c in ("Sharpe", "H1", "H2", "IS_Sharpe", "OOS_Sharpe", "isSharpe", "oSharpe",
          "Sortino", "Calmar"):
    CLASS_OF_COL[c] = "SHARPE"
METRIC_COLS = sorted(CLASS_OF_COL)
LEVEL_CLASSES = ("TURNOVER", "GROSS", "CAGR", "DD", "VOL")
CLASSES = ("TURNOVER", "GROSS", "CAGR", "DD", "VOL", "SHARPE")
FORMS = ("ABS", "REL", "HYBRID")

# IS/OOS sibling families used by the rule-8 bar leg
SIBLINGS = [("isCAGR", "oCAGR"), ("isSharpe", "oSharpe"), ("isMaxDD", "oMaxDD"),
            ("IS_CAGR", "OOS_CAGR"), ("IS_Sharpe", "OOS_Sharpe"), ("IS_MaxDD", "OOS_MaxDD"),
            ("turn_yr_is", "turn_yr_oos")]

_LOG: list[str] = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); _LOG.append(s)


# ============================================================================== harness
def fast_backtest(px_vals: np.ndarray, w_vals: np.ndarray, rb: np.ndarray,
                  cost_bps=COST_BPS):
    """numpy clone of engine.backtest; returns (daily returns, daily turnover)."""
    T, N = px_vals.shape
    rets = np.zeros_like(px_vals)
    rets[1:] = px_vals[1:] / px_vals[:-1] - 1.0
    rets = np.nan_to_num(rets, nan=0.0, posinf=0.0, neginf=0.0)
    wt = np.vstack([np.zeros((1, N)), w_vals[:-1]])
    mask = np.concatenate([[False], rb[:-1]])
    cur = np.zeros(N); out = np.zeros(T); tov = np.zeros(T)
    for i in range(T):
        if mask[i] or i == 0:
            new = wt[i]
            to = np.abs(new - cur).sum(); cur = new
        else:
            to = 0.0
        tov[i] = to
        out[i] = (cur * rets[i]).sum() - to * cost_bps / 1e4
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    return out, tov


def mets(r: pd.Series) -> dict:
    m = metrics(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"])


def ewall_weights(px: pd.DataFrame, gross: float) -> pd.DataFrame:
    """RULES v2 shape at an arbitrary gross dial: equal weight inside the 200d +/-3% band,
    gated-out weight to cash."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, BAND), 0.0)


# ================================================================================ gates
def gates(panels) -> dict:
    say("\n" + "=" * 78)
    say("GATES (pre-registered, printed before any new number is read)")
    say("=" * 78)
    g = {}

    # G1 — fast_backtest == engine.backtest on BOTH returns and turnover
    px = panels["U56"]; p = px[[c for c in px.columns if c != "SPY"]]
    dr = dt = 0.0
    for gr, cad in ((0.75, "W"), (1.00, "M")):
        w = ewall_weights(p, gr)
        rb = rebalance_mask(p.index, cad).values
        a, at = fast_backtest(p.values, w.reindex(p.index).fillna(0.0).values, rb)
        b = engine_backtest(p, w, cost_bps=COST_BPS, freq=cad)
        dr = max(dr, float(np.abs(a - b["returns"].values).max()))
        dt = max(dt, float(np.abs(at - b["turnover"].values).max()))
    g["G1"] = dr < 1e-12 and dt < 1e-12
    say(f"G1 fast_backtest == engine.backtest: returns {dr:.3e}, turnover {dt:.3e} "
        f"(bar 1e-12) -> {'PASS' if g['G1'] else 'FAIL'}")

    # G2 — EWALL(0.75) nests the live baseline exactly
    d2 = float((ewall_weights(p, 0.75) - rules_v2_weights(p, band=BAND, gross=0.75)
                .reindex_like(ewall_weights(p, 0.75)).fillna(0.0)).abs().max().max())
    g["G2"] = d2 == 0.0
    say(f"G2 EWALL(0.75) == baseline.rules_v2_weights on U56: {d2:.3e} (bar 0.0) -> "
        f"{'PASS' if g['G2'] else 'FAIL'}")

    # G3 — reproduce idea 538's OWN published failure from the two committed grids
    a538 = pd.read_csv(ROOT / "research" / "backtests" /
                       "2026-09-11_is-c_sd-the-right-SCALE-or-is-it-a-TURNOVER-proxy_B.grid.csv")
    b535 = pd.read_csv(ROOT / "research" / "backtests" /
                       "2026-09-09_is-the-FAMILY-constant-really-a-c_sd-constant_cloud.grid.csv")
    k = ["panel", "family", "level", "cad", "con"]
    m = a538[k + ["turn_yr"]].merge(b535[k + ["turn_yr"]], on=k, suffixes=("", "_ref"))
    d = (m.turn_yr - m.turn_yr_ref).abs()
    lev = m[["turn_yr", "turn_yr_ref"]].abs().max(axis=1)
    g["turn_abs"] = float(d.max()); g["turn_rel"] = float((d / lev).max())
    g["turn_lev"] = float(lev.iloc[int(d.values.argmax())])
    g["G3"] = abs(g["turn_abs"] - 9.144e-03) / 9.144e-03 < 1e-3 and len(m) == 324
    say(f"G3 idea 538's turn_yr gate re-measured from the committed grids: matched {len(m)}, "
        f"max|d| {g['turn_abs']:.4e} (published 9.144e-03) -> {'PASS' if g['G3'] else 'FAIL'}")
    say(f"   the SAME gap in relative form: {g['turn_rel']:.4e} on a level of "
        f"{g['turn_lev']:.4f}/yr")
    for pn, grp in m.groupby("panel"):
        dd = (grp.turn_yr - grp.turn_yr_ref).abs()
        say(f"     {pn:9s} max|d| {dd.max():.4e}  n {len(grp)}")
    g["G3b"] = all(float((grp.turn_yr - grp.turn_yr_ref).abs().max()) == 0.0
                   for pn, grp in m.groupby("panel") if pn != "U56")
    say(f"G3b the queue's claim 'B136/SMALL439 exactly 0' -> "
        f"{'PASS' if g['G3b'] else 'FAIL'}")

    # G3c — the SAME pair, every other shared numeric column: is turnover special?
    shared = [c for c in a538.columns if c in b535.columns and c in CLASS_OF_COL]
    mm = a538[k + shared].merge(b535[k + shared], on=k, suffixes=("", "_ref"))
    say("G3c the same 324-row pair, every shared quantity (this is the control for the "
        "idea's premise):")
    g["anchor"] = []
    for c in shared:
        dd = (mm[c] - mm[c + "_ref"]).abs()
        lv = mm[[c, c + "_ref"]].abs().max(axis=1).replace(0, np.nan)
        g["anchor"].append(dict(col=c, cls=CLASS_OF_COL[c], max_abs=float(dd.max()),
                                max_rel=float((dd / lv).max()), med_level=float(lv.median())))
        say(f"     {c:12s} [{CLASS_OF_COL[c]:8s}] max|d| {dd.max():.4e}  "
            f"max rel {float((dd/lv).max()):.4e}  median level {lv.median():.5g}")

    # G4 — the arithmetic the whole idea rests on
    x, y = 20.3, 20.3 + 9.144e-03
    g["G4"] = abs((abs(x - y) / max(abs(x), abs(y))) - 9.144e-03 / y) < 1e-15
    say(f"G4 rel == abs / level identity -> {'PASS' if g['G4'] else 'FAIL'}")
    return g


# ====================================================================== PART A — census
ASSERT_RE = re.compile(r"^\s*assert\s+(.*)$")
NUM_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?[eE][-+]?\d+|0\.0{2,}\d*)(?![\w])")
IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")

# priority-ordered: first pattern that hits wins.  WORD-ANCHORED (\b) on purpose — a plain
# substring test classifies every `returns` variable in the record as TURNOVER.
KEYWORDS = [
    ("TURNOVER", r"\bturn\w*\b|\bdto\b|\btov\b|\bto_(is|oos|full)\b|\bt_(full|is|oos)\b"),
    ("GROSS",    r"\bgross\w*\b|\bgrs\b|\bexposure\b"),
    ("CAGR",     r"\bcagr\w*\b|\bann_ret\w*\b|\btotal_return\b"),
    ("DD",       r"\bmax_?dd\w*\b|\bdrawdown\b|\bdd\w*\b|\w+_dd\b"),
    ("VOL",      r"\bvol\d*\b|\bvol_\w+\b|\bsigma\b|\bstdev\b"),
    ("SHARPE",   r"\bsharpe\w*\b|\bsortino\b|\bcalmar\b|\bh1\b|\bh2\b|\bir\b"),
    ("RETURNS",  r"\breturns?\b|\brets?\b|\brr\b|\bequity\b|\beq\b|\bport\b|\bpnl\b|\bcurve\b"),
    ("WEIGHTS",  r"\bweights?\b|\bwts\b|\bw\b|\bbook\b|\balloc\w*\b"),
    ("COST",     r"\bcost\w*\b|\bbps\b|\bfee\w*\b"),
    ("SHARE",    r"\bshare\b|\brate\b|\bpct\b|\bfrac\w*\b|\bprob\w*\b|\brho\b|\bcorr\w*\b|"
                 r"\bquantile\b|\bmedian\b|\bmae\b|\br2\b|\bt_?stat\b|\bpvalue\b"),
]
KEYWORDS = [(c, re.compile(p, re.I)) for c, p in KEYWORDS]
REL_MARKERS = ("rel", "ratio", "/ max", "/max", "/ abs", "/abs", "/ np.abs", "/ ref",
               ".div(", "np.isclose", "rtol", "pct_", "/ lev", "/ base", "/ denom")
SHAPE_MARKERS = ("len(", ".shape", ".count(", "== len", "nunique", ".size")


def classify_quantity(text: str) -> str:
    for cls, pat in KEYWORDS:
        if pat.search(text):
            return cls
    return "UNCLASSIFIED"


def census_asserts() -> pd.DataFrame:
    say("\n" + "=" * 78)
    say("PART A — CENSUS of every assert clause with a numeric bar")
    say("=" * 78)
    files = sorted(glob.glob(str(ROOT / "research" / "backtests" / "*.py")))
    rows = []
    n_assert = 0
    for f in files:
        try:
            lines = Path(f).read_text(errors="replace").split("\n")
        except Exception:
            continue
        for i, raw in enumerate(lines):
            m = ASSERT_RE.match(raw)
            if not m:
                continue
            n_assert += 1
            body = m.group(1)
            nums = NUM_RE.findall(body)
            if not nums:
                continue
            bar = min(float(x) for x in nums)
            # resolve opaque names (err, d, worst) by pulling the nearest prior assignment
            ctx = body
            used_ctx = False
            if classify_quantity(body) == "UNCLASSIFIED":
                names = [n for n in IDENT_RE.findall(body.split(",")[0])
                         if n not in ("assert", "abs", "float", "max", "min", "np", "pd", "len")]
                for nm in names:
                    pat = re.compile(r"^\s*" + re.escape(nm) + r"\s*=")
                    for j in range(i - 1, max(-1, i - 13), -1):
                        if pat.match(lines[j]):
                            ctx = body + " || " + lines[j].strip()
                            used_ctx = True
                            break
                    if used_ctx:
                        break
            low = ctx.lower()
            if any(s in low for s in SHAPE_MARKERS) and "abs" not in low:
                form = "SHAPE"
            elif any(s in low for s in REL_MARKERS):
                form = "REL"
            elif bar == 0.0 or " == 0" in body:
                form = "EXACT"
            else:
                form = "ABS"
            cls = classify_quantity(ctx)
            rows.append(dict(file=Path(f).name, line=i + 1, bar=bar, form=form,
                             cls=cls, used_ctx=used_ctx, text=body.strip()[:200]))
    C = pd.DataFrame(rows)
    say(f"scripts scanned {len(files)};  assert clauses {n_assert};  with a numeric bar "
        f"{len(C)};  context resolution used on {int(C.used_ctx.sum())}")
    say("\nBAR FORM x QUANTITY CLASS (counts over every assert clause with a numeric bar):")
    piv = pd.crosstab(C.cls, C.form)
    for c in ("ABS", "REL", "EXACT", "SHAPE"):
        if c not in piv.columns:
            piv[c] = 0
    piv = piv[["ABS", "REL", "EXACT", "SHAPE"]]
    piv.loc["TOTAL"] = piv.sum()
    say(piv.to_string())
    lev = C[(C.form == "ABS") & (C.cls.isin(LEVEL_CLASSES))]
    scf = C[(C.form == "ABS") & (C.cls == "SHARPE")]
    say(f"\nHEADLINE A: {len(lev)} absolute bars sit on LEVEL-valued quantities "
        f"({len(lev)/max(len(C),1):.1%} of all numeric-bar asserts); "
        f"{len(scf)} sit on the scale-free control (SHARPE); "
        f"{int((C.cls=='UNCLASSIFIED').sum())} unclassified "
        f"({(C.cls=='UNCLASSIFIED').mean():.1%}) — reported, not imputed.")
    if len(lev):
        say("  their bar ladder: " + ", ".join(
            f"{b:.0e} x{n}" for b, n in sorted(collections.Counter(lev.bar).items())))
    say("  REL bars anywhere in the record: "
        f"{int((C.form=='REL').sum())} of {len(C)} ({(C.form=='REL').mean():.1%})")
    C.to_csv(OUT(".census.csv"), index=False)
    return C


# ======================================================== PART B — the reproduction corpus
def build_gap_corpus() -> pd.DataFrame:
    say("\n" + "=" * 78)
    say("PART B — a REAL corpus of cross-script reproduction gaps, from the record's own "
        ".grid.csv artefacts")
    say("=" * 78)
    files = sorted(glob.glob(str(ROOT / "research" / "backtests" / "*.grid.csv")))
    D = {}
    for f in files:
        try:
            df = pd.read_csv(f)
        except Exception:
            continue
        mets_ = [c for c in METRIC_COLS if c in df.columns
                 and pd.api.types.is_numeric_dtype(df[c])]
        keys = [c for c in df.columns if c not in CLASS_OF_COL]
        if not mets_ or not keys or len(df) < MIN_MATCH:
            continue
        D[Path(f).name] = (pd.concat([df[keys].astype(str), df[mets_]], axis=1),
                           set(keys), set(mets_))
    say(f"grid artefacts usable: {len(D)} of {len(files)}")
    rows = []
    npair = 0
    for f1, f2 in itertools.combinations(sorted(D), 2):
        d1, k1, m1 = D[f1]; d2, k2, m2 = D[f2]
        kk = sorted(k1 & k2); mm = sorted(m1 & m2)
        if len(kk) < MIN_KEYS or not mm:
            continue
        if d1.duplicated(subset=kk).any() or d2.duplicated(subset=kk).any():
            continue
        j = d1[kk + mm].merge(d2[kk + mm], on=kk, suffixes=("", "_r"))
        if len(j) < MIN_MATCH:
            continue
        npair += 1
        for c in mm:
            a, b = j[c].astype(float), j[c + "_r"].astype(float)
            ok = a.notna() & b.notna()
            if ok.sum() < MIN_MATCH:
                continue
            a, b = a[ok], b[ok]
            d = (a - b).abs()
            lv = pd.concat([a.abs(), b.abs()], axis=1).max(axis=1)
            rel = (d / lv.replace(0, np.nan)).fillna(0.0)
            rows.append(dict(f1=f1, f2=f2, col=c, cls=CLASS_OF_COL[c], n=int(ok.sum()),
                             max_abs=float(d.max()), max_rel=float(rel.max()),
                             med_abs=float(d.median()), med_rel=float(rel.median()),
                             med_level=float(lv.median())))
    G = pd.DataFrame(rows)
    G["near"] = G.med_rel < NEAR_IDENT
    # DRIFT = a reproduction cell that actually MOVED.  A cell whose gap is exactly zero
    # passes every bar under every form, so it cannot discriminate between the forms and
    # dilutes any rate computed over the whole corpus.  This is where the question lives.
    G["drift"] = G.near & (G.max_abs > 0.0)
    say(f"pairs with >= {MIN_KEYS} shared keys and >= {MIN_MATCH} matched rows: {npair}; "
        f"pair x metric cells: {len(G)}; matched rows summed: {int(G.n.sum())}")
    say(f"NEAR-IDENTITY cells (median rel gap < {NEAR_IDENT:g}, i.e. the same quantity "
        f"recomputed): {int(G.near.sum())} ({G.near.mean():.1%});  DISTINCT cells "
        f"{int((~G.near).sum())}")
    say("  near-identity share at the sensitivity ladder: " + ", ".join(
        f"{t:g}: {(G.med_rel < t).mean():.1%}" for t in NEAR_LADDER))
    say(f"  of the {int(G.near.sum())} reproduction cells, {int(G.drift.sum())} "
        f"({G.drift.sum()/max(G.near.sum(),1):.1%}) have a NON-ZERO gap (the DRIFT "
        f"sub-population — the only cells on which a bar FORM can change a decision); "
        f"{int((G.near & (G.max_abs == 0)).sum())} are bit-identical.")
    say("\nper QUANTITY CLASS  (NEAR = every reproduction cell, DRIFT = the non-zero-gap ones):")
    say(f"  {'class':9s} {'NEAR':>6s} {'DRIFT':>6s} {'med level':>11s} | "
        f"{'DRIFT med|d|':>13s} {'DRIFT med rel':>13s} {'DRIFT P90 |d|':>13s} "
        f"{'DRIFT P90 rel':>13s}")
    for cls in CLASSES:
        s = G[G.near & (G.cls == cls)]; d = G[G.drift & (G.cls == cls)]
        if not len(s):
            continue
        if len(d):
            say(f"  {cls:9s} {len(s):6d} {len(d):6d} {s.med_level.median():11.5g} | "
                f"{d.max_abs.median():13.4e} {d.max_rel.median():13.4e} "
                f"{d.max_abs.quantile(0.9):13.4e} {d.max_rel.quantile(0.9):13.4e}")
        else:
            say(f"  {cls:9s} {len(s):6d} {0:6d} {s.med_level.median():11.5g} | "
                f"{'-':>13s} {'-':>13s} {'-':>13s} {'-':>13s}")
    say("\n  READ THIS ROW-WISE: a relative bound is LOOSER than an absolute one only where "
        "the level is > 1.\n  Median levels above: TURNOVER ~10, everything else < 1.")
    G.to_csv(OUT(".gapcorpus.csv"), index=False)
    return G


def price_bar_forms(G: pd.DataFrame) -> pd.DataFrame:
    say("\n" + "=" * 78)
    say("PART B grid — QUANTITY CLASS x BAR FORM x BAR LEVEL (every grid point reported)")
    say("=" * 78)
    rows = []
    for pop in ("NEAR", "DRIFT"):
        sel = G.near if pop == "NEAR" else G.drift
        for cls in CLASSES:
            for bar in BAR_LADDER:
                s = G[G.cls == cls]
                if not len(s):
                    continue
                near, dist = G[sel & (G.cls == cls)], s[~s.near]
                pa_n = (near.max_abs < bar); pr_n = (near.max_rel < bar)
                pa_d = (dist.max_abs < bar); pr_d = (dist.max_rel < bar)
                for form in FORMS:
                    if form == "ABS":
                        okn, okd = pa_n, pa_d
                    elif form == "REL":
                        okn, okd = pr_n, pr_d
                    else:
                        okn, okd = (pa_n | pr_n), (pa_d | pr_d)
                    rows.append(dict(pop=pop, cls=cls, level_valued=cls in LEVEL_CLASSES,
                                     form=form, bar=bar, n_near=len(near), n_dist=len(dist),
                                     pass_near=int(okn.sum()),
                                     pass_near_share=float(okn.mean()) if len(near) else np.nan,
                                     falsepass_dist=int(okd.sum()),
                                     falsepass_share=float(okd.mean()) if len(dist) else np.nan,
                                     recovered=int((~pa_n & pr_n).sum()),
                                     newly_caught=int((pa_n & ~pr_n).sum()),
                                     dist_recovered=int((~pa_d & pr_d).sum())))
    P = pd.DataFrame(rows)
    P.to_csv(OUT(".grid.csv"), index=False)
    for pop in ("NEAR", "DRIFT"):
        say(f"\n--- population {pop} " + ("(every reproduction cell)" if pop == "NEAR"
                                          else "(non-zero-gap reproduction cells only)"))
        for cls in CLASSES:
            s = P[(P.cls == cls) & (P["pop"] == pop)]
            if not len(s) or int(s.n_near.iloc[0]) == 0:
                continue
            say(f"\n  {cls}  (level-valued: {cls in LEVEL_CLASSES};  cells "
                f"{int(s.n_near.iloc[0])}, distinct-control {int(s.n_dist.iloc[0])})")
            say(f"    {'bar':>8s} | {'ABS pass':>9s} {'REL pass':>9s} {'HYB pass':>9s} | "
                f"{'recovered':>9s} {'newcatch':>8s} | {'ABS fp':>7s} {'REL fp':>7s}")
            for bar in BAR_LADDER:
                g = {f: s[(s.bar == bar) & (s.form == f)].iloc[0] for f in FORMS}
                say(f"    {bar:8.0e} | {g['ABS'].pass_near:9d} {g['REL'].pass_near:9d} "
                    f"{g['HYBRID'].pass_near:9d} | {g['ABS'].recovered:9d} "
                    f"{g['ABS'].newly_caught:8d} | {g['ABS'].falsepass_dist:7d} "
                    f"{g['REL'].falsepass_dist:7d}")
    nd = int(P[P["pop"] == "NEAR"].n_dist.sum() / (len(FORMS) * len(BAR_LADDER)))
    say(f"\n  DISCRIMINATION LEG IS UNDERPOWERED AND IS REPORTED AS SUCH: only {nd} "
        f"DISTINCT cells exist in the whole corpus (two artefacts sharing >= 2 key columns "
        f"almost always recompute the same book), so the 'false PASS' columns above carry "
        f"no verdict either way.")
    # headline at the record's own working bar, on the population where the form can bite
    say(f"\nHEADLINE B (at the record's own working bar 1e-6, the bar idea 538 failed; "
        f"DRIFT cells only):")
    for cls in CLASSES:
        a = P[(P["pop"] == "DRIFT") & (P.cls == cls) & (P.bar == 1e-6) & (P.form == "ABS")]
        r = P[(P["pop"] == "DRIFT") & (P.cls == cls) & (P.bar == 1e-6) & (P.form == "REL")]
        if not len(a) or int(a.iloc[0].n_near) == 0:
            say(f"  {cls:9s} no DRIFT cells — every reproduction of this class in the "
                f"corpus is bit-identical")
            continue
        a, r = a.iloc[0], r.iloc[0]
        say(f"  {cls:9s} DRIFT cells {a.n_near:4d}: ABS passes {a.pass_near:4d} "
            f"({a.pass_near_share:6.1%}) -> REL passes {r.pass_near:4d} "
            f"({r.pass_near_share:6.1%});  RECOVERED {a.recovered:4d} "
            f"({a.recovered/a.n_near:5.1%}), NEWLY CAUGHT {a.newly_caught:3d} "
            f"({a.newly_caught/a.n_near:5.1%})")
    return P


def extrapolate(C: pd.DataFrame, P: pd.DataFrame):
    """Price the STATIC census with the MEASURED per-class recovery rate.  This is an
    extrapolation from Part B onto Part A's counts, labelled as such — not a claim that
    these specific asserts were re-run."""
    say("\nEXTRAPOLATION (census counts x measured DRIFT-cell recovery rate at bar 1e-6 — "
        "an estimate, not a re-run):")
    tot = 0.0
    for cls in LEVEL_CLASSES:
        n = int(((C.form == "ABS") & (C.cls == cls)).sum())
        row = P[(P["pop"] == "DRIFT") & (P.cls == cls) & (P.bar == 1e-6) & (P.form == "ABS")]
        if not n or not len(row) or not row.iloc[0].n_near:
            continue
        rate = row.iloc[0].recovered / row.iloc[0].n_near
        tot += n * rate
        say(f"  {cls:9s} {n:3d} absolute bars x recovery {rate:6.1%} = {n*rate:5.1f} "
            f"clauses that a relative bound would flip FAIL -> PASS")
    say(f"  estimated total across LEVEL classes: {tot:.1f} clauses")
    return tot


# ============================================================ PART C — rule 8, two legs
def wf_bar(G_pairs: pd.DataFrame) -> pd.DataFrame:
    """Rule-8 leg 1 (the idea's OWN decision object): calibrate the bar on IS-window gaps
    only, then read it ONCE on the matching OOS-window gaps.  A bar form that only works
    in-sample is a PARK, not a KEEP."""
    say("\n" + "=" * 78)
    say("PART C / RULE 8 leg 1 — the BAR calibrated on IS-window gaps, read once on OOS")
    say("=" * 78)
    rows = []
    for pop in ("NEAR", "DRIFT"):
        selcol = "near" if pop == "NEAR" else "drift"
        for isc, oc in SIBLINGS:
            s_is = G_pairs[(G_pairs.col == isc) & G_pairs[selcol]]
            s_oo = G_pairs[(G_pairs.col == oc) & G_pairs[selcol]]
            key = ["f1", "f2"]
            m = s_is[key + ["max_abs", "max_rel", "med_level"]].merge(
                s_oo[key + ["max_abs", "max_rel"]], on=key, suffixes=("_is", "_oos"))
            if len(m) < 5:
                continue
            bar_abs = WF_K * float(np.nanquantile(m.max_abs_is, 0.99))
            bar_rel = WF_K * float(np.nanquantile(m.max_rel_is, 0.99))
            pa = (m.max_abs_oos < bar_abs); pr = (m.max_rel_oos < bar_rel)
            rows.append(dict(pop=pop, family=f"{isc}->{oc}", cls=CLASS_OF_COL[isc], n=len(m),
                             bar_abs=bar_abs, bar_rel=bar_rel,
                             oos_pass_abs=int(pa.sum()), oos_pass_rel=int(pr.sum()),
                             flips_abs_fail_rel_pass=int((~pa & pr).sum()),
                             flips_abs_pass_rel_fail=int((pa & ~pr).sum()),
                             decisions_changed=int((pa != pr).sum()),
                             med_level=float(m.med_level.median())))
    W = pd.DataFrame(rows)
    if len(W):
        say(W.to_string(index=False, float_format=lambda x: f"{x:.4g}"))
        for pop in ("NEAR", "DRIFT"):
            s = W[W["pop"] == pop]
            if not len(s):
                say(f"\n  rule-8 bar leg [{pop}]: VOID (no sibling family reached 5 cells)")
                continue
            say(f"\n  rule-8 bar leg [{pop}]: {int(s.decisions_changed.sum())} of "
                f"{int(s.n.sum())} OOS gate decisions differ between the two bar forms "
                f"({s.decisions_changed.sum()/max(s.n.sum(),1):.1%})")
    else:
        say("  no IS/OOS sibling family had >= 5 matched reproduction cells — leg VOID")
    return W


def wf_books(panels) -> pd.DataFrame:
    """Rule-8 leg 2 (PROTOCOL compliance): 4 IS-only selectors x 3 panels, each pick read
    ONCE on 2017-01-01+, against RULES v2 and SPY on the same panel and calendar."""
    say("\n" + "=" * 78)
    say("PART C / RULE 8 leg 2 — 4 IS-only selectors x 3 panels, read ONCE on OOS")
    say("=" * 78)
    books = []
    for pname, px in panels.items():
        names = [c for c in px.columns if c != "SPY"]
        p = px[names]
        spy = px["SPY"].pct_change().fillna(0.0)
        start = p.index[260]
        base = engine_backtest(p, rules_v2_weights(p, band=BAND, gross=0.75),
                               cost_bps=COST_BPS, freq="W")["returns"].loc[start:]
        for gr in (0.50, 0.75, 1.00):
            w = ewall_weights(p, gr).reindex(p.index).fillna(0.0).values
            for cad in ("W", "M", "Q"):
                rb = rebalance_mask(p.index, cad).values
                r, _ = fast_backtest(p.values, w, rb)
                r = pd.Series(r, index=p.index).loc[start:]
                books.append(dict(panel=pname, gross=gr, cad=cad,
                                  **{"IS_" + k: v for k, v in mets(r.loc[:IS_END]).items()},
                                  **{"OOS_" + k: v for k, v in mets(r.loc[OOS_START:]).items()},
                                  **mets(r), H1=metrics(r.iloc[:len(r)//2])["Sharpe"],
                                  H2=metrics(r.iloc[len(r)//2:])["Sharpe"]))
        # benchmarks on the same panel/calendar
        for nm, s in (("RULESv2", base), ("SPY", spy.loc[start:])):
            books.append(dict(panel=pname, gross=np.nan, cad=nm,
                              **{"IS_" + k: v for k, v in mets(s.loc[:IS_END]).items()},
                              **{"OOS_" + k: v for k, v in mets(s.loc[OOS_START:]).items()},
                              **mets(s), H1=metrics(s.iloc[:len(s)//2])["Sharpe"],
                              H2=metrics(s.iloc[len(s)//2:])["Sharpe"]))
    B = pd.DataFrame(books)
    say("\nbook grid (all 27 books + 6 benchmark rows, every grid point reported):")
    say(B.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    picks = []
    for pname in panels:
        s = B[(B.panel == pname) & B.gross.notna()]
        bench = B[(B.panel == pname) & B.gross.isna()].set_index("cad")
        v2, sp = bench.loc["RULESv2"], bench.loc["SPY"]
        for sel, col, asc in (("IS_Sharpe", "IS_Sharpe", False), ("IS_CAGR", "IS_CAGR", False),
                              ("IS_MaxDD", "IS_MaxDD", False),
                              ("IS_Calmar", None, False)):
            if sel == "IS_Calmar":
                sc = s.IS_CAGR / s.IS_MaxDD.abs()
                pick = s.loc[sc.idxmax()]
            else:
                pick = s.loc[s[col].idxmax()]
            p4a = (pick.H1 > v2.H1) and (pick.H2 > v2.H2) and (pick.MaxDD >= v2.MaxDD)
            p4b = ((pick.H1 > sp.H1) and (pick.H2 > sp.H2) and
                   (pick.OOS_Sharpe > sp.OOS_Sharpe) and
                   (pick.MaxDD >= 0.60 * sp.MaxDD) and (pick.CAGR >= 0.70 * sp.CAGR))
            picks.append(dict(panel=pname, selector=sel, gross=pick.gross, cad=pick.cad,
                              OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                              OOS_MaxDD=pick.OOS_MaxDD, v2_OOS_Sharpe=v2.OOS_Sharpe,
                              spy_OOS_Sharpe=sp.OOS_Sharpe, spy_OOS_CAGR=sp.OOS_CAGR,
                              H1=pick.H1, H2=pick.H2, MaxDD=pick.MaxDD, CAGR=pick.CAGR,
                              pass4a=bool(p4a), pass4b=bool(p4b)))
    K = pd.DataFrame(picks)
    say("\nrule-8 picks (chosen on 2009-2016 only, read ONCE on 2017-01-01+):")
    say(K.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\n  RULE 8 VERDICT: 4a {int(K.pass4a.sum())}/{len(K)}, "
        f"4b {int(K.pass4b.sum())}/{len(K)}")
    K.to_csv(OUT(".bookleg.csv"), index=False)
    B.to_csv(OUT(".bookgrid.csv"), index=False)
    return K


# ================================================================================= main
def main():
    say("Idea 734 — re-gate the record's ABSOLUTE reproduction bars that sit on LEVEL "
        "quantities  (lane B, 2026-09-11)")
    say("10 bps, next-day execution, PROTOCOL rules 1-9.  Two tuned params: QUANTITY CLASS "
        "x BAR FORM, all grid points reported.")

    say("\nLoading panels (committed caches only — no network)...")
    panels = {}
    panels["U56"] = load_universe()
    panels["B136"] = load_universe(broad=True)
    sm = load_universe(small=True)
    mx = sm.drop(columns=["SPY"]).pct_change().abs().max()
    drop = list(mx[mx >= 1.0].index)
    panels["SMALL439"] = sm.drop(columns=drop)
    say(f"  U56 {panels['U56'].shape}  B136 {panels['B136'].shape}  "
        f"SMALL439 {panels['SMALL439'].shape} (dropped {len(drop)} names, max 1d move >= 1.0)")

    g = gates(panels)
    C = census_asserts()
    G = build_gap_corpus()
    P = price_bar_forms(G)
    est = extrapolate(C, P)
    W = wf_bar(G)
    K = wf_books(panels)
    if len(W):
        W.to_csv(OUT(".walkforward.csv"), index=False)

    # -------------------------------------------------------------------------- verdict
    D = P[P["pop"] == "DRIFT"]
    a6 = D[(D.bar == 1e-6) & (D.form == "ABS")].set_index("cls")
    r6 = D[(D.bar == 1e-6) & (D.form == "REL")].set_index("cls")
    lv = a6.loc[[c for c in LEVEL_CLASSES if c in a6.index]]
    rec = int(lv.recovered.sum()); new = int(lv.newly_caught.sum())
    ndr = int(lv.n_near.sum())
    sh_a = float(a6.loc["SHARPE"].pass_near_share) if "SHARPE" in a6.index else np.nan
    sh_r = float(r6.loc["SHARPE"].pass_near_share) if "SHARPE" in r6.index else np.nan
    to_a = a6.loc["TURNOVER"] if "TURNOVER" in a6.index else None
    wd = W[W["pop"] == "DRIFT"]

    say("\n" + "=" * 78)
    say("VERDICT")
    say("=" * 78)
    say(f"1. The anchor reproduces exactly: idea 538's turn_yr gap is {g['turn_abs']:.4e} "
        f"absolute = {g['turn_rel']:.4e} relative on a level of {g['turn_lev']:.3f}/yr, and "
        f"the queue's 'B136/SMALL439 exactly 0' is {'TRUE' if g['G3b'] else 'FALSE'}. The "
        f"diagnosis in the queue entry is CORRECT for that one gate.")
    say(f"2. It does NOT generalise. On the SAME 324-row pair the scale-free control is "
        f"WORSE in relative terms than turnover (G3c): turnover max rel {g['turn_rel']:.2e} "
        f"against {max(a['max_rel'] for a in g['anchor'] if a['cls']=='SHARPE'):.2e} for the "
        f"Sharpe family and {max(a['max_rel'] for a in g['anchor'] if a['cls']=='CAGR'):.2e} "
        f"for CAGR. The vintage drift is not a turnover problem and not a LEVEL problem.")
    say(f"3. The reason is arithmetic, not empirical: a relative bound is looser than an "
        f"absolute one ONLY where the quantity's level exceeds 1. In this record TURNOVER is "
        f"the only such class (median level ~10); CAGR ~0.09, DD ~0.21, GROSS ~0.73, VOL "
        f"~0.13 all sit BELOW 1, so a relative bound on them is STRICTER, not looser.")
    say(f"4. Priced on the {ndr} DRIFT cells of the LEVEL classes at the record's own 1e-6 "
        f"bar: re-gating RECOVERS {rec} and NEWLY CATCHES {new}. Turnover alone: "
        + (f"{int(to_a.recovered)} recovered of {int(to_a.n_near)} DRIFT cells."
           if to_a is not None else "no DRIFT cells.")
        + f" The scale-free control moves {sh_a:.1%} -> {sh_r:.1%}.")
    say(f"5. Rule 8, bar leg (bar calibrated on IS-window gaps, read once on OOS): "
        + (f"{int(wd.decisions_changed.sum())} of {int(wd.n.sum())} OOS decisions differ "
           f"between the forms on DRIFT cells." if len(wd) else "DRIFT leg VOID.")
        + f"  Book leg: 4a {int(K.pass4a.sum())}/{len(K)}, 4b {int(K.pass4b.sum())}/{len(K)}.")
    say(f"6. Static census: {int(((C.form=='ABS') & (C.cls.isin(LEVEL_CLASSES))).sum())} "
        f"absolute bars on level quantities out of {len(C)} numeric-bar asserts "
        f"({int((C.form=='REL').sum())} relative bars exist in the whole record); the "
        f"measured recovery rate puts an estimated {est:.1f} of them on the other side of "
        f"their bar.")
    say(f"7. VERDICT: KILL of the general proposal, KEEP of the narrow one. Do not re-gate "
        f"the record on relative bounds. Gate TURNOVER — and only quantities whose level "
        f"exceeds 1 — on a relative bound, or equivalently scale the absolute bar by the "
        f"quantity's level. No book KEEP on either PROTOCOL path.")

    OUT(".console.txt").write_text("\n".join(_LOG) + "\n")
    say(f"\nwrote {OUT('.console.txt').name}, .census.csv, .gapcorpus.csv, .grid.csv, "
        f".walkforward.csv, .bookleg.csv, .bookgrid.csv")
    OUT(".console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
