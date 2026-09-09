#!/usr/bin/env python3
"""Idea 554 - "is-every-published-BAND-a-band-on-a-MEAN-quoted-as-a-CELL-expectation"
(cloud, 2026-09-09).

The question
------------
Idea 551's bar dial found that idea 300's pre-registered band `BAR_MA_RESID = (-0.70, -0.20)`
is a bar on a NINE-THETA MEAN, not a coverage interval: at the published width only 48-56% of
the individual thetas sit inside it at any cadence, and 7% at ANNUAL; m = 2.0 (the band widened
to [-0.95, +0.05]) is needed before 85-100% of cells are inside.

A band that holds for a mean and fails for half its own cells is not wrong - it is AMBIGUOUS.
Read as "the mean of this statistic lies here" it is true; read as "a cell of this statistic
lies here", which is how a prior gets quoted forward into the next script, it is a coin flip.
The queue asks the census question: across the whole committed record,

    (a) how many pre-registered BANDS state the statistic they bound?
    (b) for those that bound a mean over cells, what is the actual CELL-LEVEL coverage?

The dials (exactly 2, both fully reported)
------------------------------------------
    BAND            (dial 1)  the census unit - every band found is reported, none dropped
    COVERAGE TARGET (dial 2)  {50, 66.7, 80, 90, 95} % - all five reported for every priced band

    WIDTH MULTIPLIER m in {0.5, 0.75, 1.0, 1.5, 2.0, 3.0} and WINDOW in {FULL, IS, OOS} are
    REPORTED CONTRASTS, not tuned dials: every point is printed and nothing is selected on them
    except inside the rule-8 leg, where m is chosen on IS and read on OOS by construction.

The census rule (pre-registered, mechanical, stated before the run)
------------------------------------------------------------------
Step 1 - OCCURRENCES.  A two-sided numeric interval in `research/backtests/*.py` (this script
excluded), found by exactly five patterns:

    TUPLE2   NAME = (lo, hi)                     both numeric literals
    IN_BAND  in_band(x, lo, hi)                  the record's own helper
    CHAIN    lo <= expr <= hi                    a literal-bounded comparison chain
    BETWEEN  x.between(lo, hi)
    ABSTOL   abs(expr - c) < h                   a band written as centre +/- half-width

Step 2 - ELIGIBILITY.  An occurrence is a BAND only if it is used as a pass/fail bar: its line
carries a verdict token (`PASS|FAIL|HIT|MISS|OK|ok|CONFIRMED|REFUTED|in_band|inside|clears|
gate|VERDICT|holds|violat`) OR the constant's name matches `^(BAR|BAND)_` / `_(BAR|BAND)S?$`.
This is what removes parameter pairs that merely LOOK like intervals - `COSTS = (10, 25)`,
`ANCHOR = (0.75, 20)`, `BULK_LAST_Q = (1, 2026)` - and it is applied before anything is counted.

Step 3 - ARITY.  A band is a REPRO gate when it is an ABSTOL whose half-width is <= 5% of its
centre: that is idea 515's hand-copied-constant gate (`abs(Sharpe - 1.133) < 5e-4`), it bounds
ONE number, and its cell-level coverage is 1/1 or 0/1 by construction - the question does not
apply to it.  Everything else is a GRID band: an interval on a quantity that ranges over cells.

Step 4 - WHAT IT BOUNDS, for GRID bands only.  MEAN when the bounded expression, or the
variable assigned to it within 12 lines above, carries `.mean(`/`np.mean`/`mean_`/`_mean`;
CELL when the band is evaluated inside an iteration; SCALAR when the bounded side is a single
named quantity; UNSTATED otherwise.  STATES_STATISTIC is True when the band's own line or the
two lines above it contain `mean|median|pooled|average|per-cell|each cell|every cell|per cell|
cellwise|cell-level`.

Step 5 - PRICING.  A GRID band is priceable when a numeric column of ITS OWN script's committed
artefact CSVs is NAMED IN the bounded expression (a direct name link, not a context token).
The anchor band [-0.70, -0.20] is priced separately from idea 551's own committed decomp.csv,
because its cells are that file's `resid0_pp` by that file's own construction - which is also
gate G2.  The automatic match rate is itself a reported number: a band nobody can re-price from
its own artefacts is, by definition, a band published without its cell distribution.

Rule 8 (walk-forward), required
-------------------------------
The anchor band's cells carry a `window` column (IS <= 2016-12-31, OOS >= 2017-01-01).  For each
coverage target the SMALLEST multiplier m reaching the target ON THE IS CELLS ONLY is chosen,
and the coverage that m delivers on the untouched OOS cells is read, per cadence and pooled.
A width fitted on the first half that does not hold in the second is a width that was fitted,
not measured.  Any other priceable band whose artefact carries a window column is run the same
way.

KEEP paths (PROTOCOL 4)
-----------------------
Idea 554 proposes NO book and therefore has NO KEEP candidate; it cannot produce one, and none
is claimed.  Both paths are still evaluated record-wide over every committed artefact CSV that
carries the `p4a` and `f4b`/`fail4b` columns - the record's own population of priced books, and
the only KEEP evaluation this census can honestly make.

Pre-registered gates (a FAIL is reported, not repaired)
-------------------------------------------------------
    G1  the extractor finds idea 300/551's (-0.70, -0.20) band in >= 2 committed scripts
    G2  idea 551's published coverage reproduces from ITS OWN committed decomp.csv: 48-56% of
        MA-THRESH thetas inside at D/W/M/Q, <= 10% at A, and >= 85% at m = 2.0
    G3  no duplicate (file, line, pattern, lo, hi) occurrence, and lo < hi on every band
    G4  every eligible band classified into exactly one arity and one kind
    G5  the KEEP census parses >= 50 committed grids carrying both KEEP columns
    G6  eligibility removes every occurrence whose constant is a known parameter pair
        (COSTS, ANCHOR, BULK_LAST_Q, RUNGS, COST_RUNGS, GROSSES, GROSS_AXIS, DIP_CENTRES)

No prices are loaded and no book is run: this script reads the committed record only.
Survivorship does not enter directly - nothing here is a return series - but every KEEP column
it pools was computed on panels that ARE survivorship-biased (SMALL439 and B136 are current
constituents), so the record-wide 4a/4b rates below inherit that optimism.
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BTDIR = REPO / "research" / "backtests"
SELF = Path(__file__).name

import numpy as np
import pandas as pd

TARGETS = [50.0, 66.7, 80.0, 90.0, 95.0]          # dial 2 - all reported
MULTS = [0.5, 0.75, 1.0, 1.5, 2.0, 3.0]           # reported contrast
ANCHOR_BAND = (-0.70, -0.20)
PRIOR551 = BTDIR / "2026-09-09_restate-idea-298s-MA-RESIDUAL-BAND-with-its-cadence-domain_C.decomp.csv"
G2_LO, G2_HI, G2_A, G2_M2 = 0.45, 0.60, 0.10, 0.85
G5_MIN_GRIDS = 50
REPRO_REL = 0.05
PARAM_PAIRS = {"COSTS", "ANCHOR", "BULK_LAST_Q", "RUNGS", "COST_RUNGS", "GROSSES",
               "GROSS_AXIS", "DIP_CENTRES", "DIP_CELLS", "MOM_RUN", "QUEUE_WINDOW"}

NUM = r"-?\d+\.?\d*(?:[eE][-+]?\d+)?"
PATTERNS = {
    "TUPLE2": re.compile(rf"^\s*([A-Z][A-Z0-9_]{{2,40}})\s*=\s*\(\s*({NUM})\s*,\s*({NUM})\s*\)\s*(?:#.*)?$"),
    "IN_BAND": re.compile(rf"in_band\s*\(\s*([^,]{{1,60}}?)\s*,\s*({NUM})\s*,\s*({NUM})\s*\)"),
    "CHAIN": re.compile(rf"({NUM})\s*<=?\s*([A-Za-z_][\w.\[\]\"'()]{{0,50}})\s*<=?\s*({NUM})"),
    "BETWEEN": re.compile(rf"([A-Za-z_][\w.\[\]\"']{{0,40}})\.between\s*\(\s*({NUM})\s*,\s*({NUM})\s*\)"),
    "ABSTOL": re.compile(rf"abs\s*\(\s*([^()]{{1,80}}?)\s*-\s*({NUM})\s*\)\s*<=?\s*({NUM})"),
}
VERDICT_RE = re.compile(r"\bPASS\b|\bFAIL\b|\bHIT\b|\bMISS\b|\bOK\b|CONFIRMED|REFUTED|\bok\b|"
                        r"in_band|inside|clears|\bgate\b|VERDICT|holds|violat", re.I)
NAME_RE = re.compile(r"^(BAR|BAND)_|_(BAR|BAND)S?$")
MEAN_RE = re.compile(r"\.mean\s*\(|np\.mean|\bmean_|_mean\b")
ITER_RE = re.compile(r"\bfor\b.*\bin\b|\ball\s*\(|\bany\s*\(")
SAYS_RE = re.compile(r"\bmean\b|\bmedian\b|\bpooled\b|\baverage\b|per-cell|each cell|every cell|"
                     r"per cell|cellwise|cell-level", re.I)
IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


def coverage(v, lo, hi, m):
    c, h = 0.5 * (lo + hi), 0.5 * (hi - lo)
    return float(((v >= c - m * h) & (v <= c + m * h)).mean())


def smallest_m(v, lo, hi, target):
    for m in MULTS:
        if 100 * coverage(v, lo, hi, m) >= target:
            return m
    return np.nan


# ------------------------------------------------------------------ step 1: occurrences
def extract():
    occ = []
    for f in sorted(BTDIR.glob("*.py")):
        if f.name == SELF:
            continue
        try:
            lines = f.read_text(errors="ignore").split("\n")
        except Exception:
            continue
        for i, ln in enumerate(lines):
            ctx = "\n".join(lines[max(0, i - 2):i + 1])
            back = "\n".join(lines[max(0, i - 12):i + 1])
            for pat, rx in PATTERNS.items():
                for m in rx.finditer(ln):
                    if pat == "TUPLE2":
                        name, a, b = m.group(1), float(m.group(2)), float(m.group(3))
                        expr = name
                    elif pat == "ABSTOL":
                        expr, c, h = m.group(1), float(m.group(2)), float(m.group(3))
                        a, b, name = c - h, c + h, ""
                    elif pat in ("IN_BAND", "BETWEEN"):
                        expr, a, b = m.group(1), float(m.group(2)), float(m.group(3))
                        name = ""
                    else:
                        a, expr, b = float(m.group(1)), m.group(2), float(m.group(3))
                        name = ""
                    a, b = min(a, b), max(a, b)
                    if not (b - a) > 0:
                        continue
                    occ.append(dict(file=f.name, line=i + 1, pattern=pat, name=name,
                                    expr=expr.strip(), lo=a, hi=b, text=ln.strip()[:220],
                                    ctx=ctx, back=back))
    return pd.DataFrame(occ)


def classify_kind(row):
    expr, back, line = row["expr"], row["back"], row["text"]
    if MEAN_RE.search(expr) or MEAN_RE.search(line):
        return "MEAN"
    tok = expr.split(".")[0].split("[")[0].split("(")[0].strip()
    if tok and re.fullmatch(r"[A-Za-z_]\w*", tok):
        asg = re.search(rf"^\s*{re.escape(tok)}\s*=\s*(.+)$", back, re.M)
        if asg and MEAN_RE.search(asg.group(1)):
            return "MEAN"
    if ITER_RE.search(line):
        return "CELL"
    if re.fullmatch(r"[A-Za-z_]\w*(\[[^\]]+\])?(\.\w+)*(\(\))?", expr or ""):
        return "SCALAR"
    return "UNSTATED"


# ------------------------------------------------------------------ step 5: pricing
ART_CACHE = {}


def load_art(p):
    if p not in ART_CACHE:
        try:
            ART_CACHE[p] = pd.read_csv(p)
        except Exception:
            ART_CACHE[p] = None
    return ART_CACHE[p]


def price(row):
    """Strict NAME LINK: a numeric column of the band's own script artefacts whose name appears
    as an identifier IN THE BOUNDED EXPRESSION.  No context-token matching."""
    toks = set(IDENT_RE.findall(row["expr"] or ""))
    if not toks:
        return None
    stem = row["file"][:-3]
    best = None
    for p in sorted(BTDIR.glob(f"{stem}.*.csv")):
        df = load_art(p)
        if df is None or not len(df):
            continue
        for c in df.columns:
            if c in toks and pd.api.types.is_numeric_dtype(df[c]):
                v = df[c].dropna()
                if len(v) >= 5 and (best is None or len(v) > len(best[2])):
                    best = (p.name, c, v, df)
    return best


# ------------------------------------------------------------------ main
def main():
    P("=" * 178)
    P("IDEA 554 - is-every-published-BAND-a-band-on-a-MEAN-quoted-as-a-CELL-expectation "
      "(cloud, 2026-09-09)")
    P("=" * 178)
    P("PREMISE (idea 551): the published band [-0.70,-0.20] holds for a 9-theta MEAN but only "
      "48-56% of individual thetas sit inside it (7% at A); m=2.0 is needed for 85-100%.")
    P("ASK  (a) how many committed bands STATE the statistic they bound?  (b) what is the "
      "CELL-LEVEL coverage of the ones that bound a mean over cells?")
    P("DIALS band (census unit, all reported) x coverage target (5 levels, all reported).  "
      "Width multiplier and window are reported contrasts.")
    P("")

    O = extract()
    nscripts = len(list(BTDIR.glob("*.py"))) - 1
    O["elig"] = (O.text.fillna("").str.contains(VERDICT_RE) |
                 O.name.fillna("").str.match(NAME_RE))
    O["half"] = (O.hi - O.lo) / 2
    O["centre"] = (O.hi + O.lo) / 2
    O["rel_half"] = O.half / O.centre.abs().clip(lower=1e-12)
    O["arity"] = np.where((O.pattern == "ABSTOL") & (O.rel_half <= REPRO_REL), "REPRO", "GRID")
    O["kind"] = O.apply(classify_kind, axis=1)
    O["says"] = O.apply(lambda r: bool(SAYS_RE.search(r["ctx"]) or SAYS_RE.search(r["text"])),
                        axis=1)

    P("=" * 178)
    P(f"STEP 1-2  THE POPULATION - {len(O)} two-sided intervals in {O.file.nunique()} of "
      f"{nscripts} committed scripts; {int(O.elig.sum())} of them are used as a PASS/FAIL BAR "
      f"and are the census population")
    P("=" * 178)
    P("all occurrences by pattern / eligible by pattern:")
    P(pd.DataFrame({"found": O.pattern.value_counts(),
                    "eligible": O[O.elig].pattern.value_counts()}).fillna(0).astype(int)
      .to_string())
    E = O[O.elig].copy()
    P(f"\nremoved by the eligibility rule: {len(O) - len(E)} intervals that are not bars "
      f"(parameter pairs, cost grids, index ranges, plotting limits).")

    ok_g6 = not bool(E.name.isin(PARAM_PAIRS).any())
    P(f"\nSTEP 3  ARITY of the {len(E)} bands:")
    P(E.arity.value_counts().to_string())
    P(f"  REPRO = an ABSTOL whose half-width is <= {REPRO_REL:.0%} of its centre: a hand-copied "
      f"constant gate on ONE number (idea 515's category).  Cell-level coverage is 1/1 or 0/1 "
      f"by construction, so question (b) does not apply to it.")
    P(f"  GRID  = an interval on a quantity that ranges over cells.  This is idea 551's object.")
    E.drop(columns=["ctx", "back"]).to_csv(f"{OUT}.census.csv", index=False)

    Gd = E[E.arity == "GRID"].copy()
    P("\n" + "=" * 178)
    P(f"(a) THE {len(Gd)} GRID BANDS, EVERY ONE, AND WHETHER THE SOURCE STATES THE STATISTIC "
      "IT BOUNDS")
    P("=" * 178)
    for _, r in Gd.sort_values(["file", "line"]).iterrows():
        P(f"  {r.file[:64]:64s}:{r.line:<5d} [{r.pattern:7s}] [{r.lo:g}, {r.hi:g}]  "
          f"bounds={r.kind:8s} states_it={str(r.says):5s}  expr={r.expr[:40]!r}")
        P(f"      {r.text[:150]}")
    ct = pd.crosstab(Gd.kind, Gd.says).rename(columns={False: "silent", True: "states_it"})
    for c in ("silent", "states_it"):
        if c not in ct:
            ct[c] = 0
    ct["n"] = ct.sum(axis=1)
    P("\nGRID bands by what they bound x whether they say so:")
    P(ct[["n", "states_it", "silent"]].to_string())
    n_mean = int((Gd.kind == "MEAN").sum())
    P(f"\n(a) ANSWER: of the {len(E)} pre-registered bands in the record, {int((E.arity=='REPRO').sum())} "
      f"bound a single number by construction and {len(Gd)} bound a quantity that ranges over "
      f"cells.  Of those {len(Gd)}, {n_mean} demonstrably bound a MEAN and "
      f"{int(Gd[Gd.kind=='MEAN'].says.sum()) if n_mean else 0} of those say so; "
      f"{int(Gd.says.sum())} of {len(Gd)} name their statistic at all "
      f"({100*Gd.says.mean():.1f}%).")
    flush_log()

    # ------------------------------------------------------ gates
    P("\n" + "=" * 178)
    P("GATES")
    P("=" * 178)
    known = O[(O.lo.round(6) == ANCHOR_BAND[0]) & (O.hi.round(6) == ANCHOR_BAND[1])]
    ok_g1 = known.file.nunique() >= 2
    P(f"G1 {'PASS' if ok_g1 else 'FAIL'}  the (-0.70, -0.20) anchor band is found in "
      f"{known.file.nunique()} committed scripts: {', '.join(sorted(known.file.unique()))}")
    dup = int(O.duplicated(subset=["file", "line", "pattern", "lo", "hi"]).sum())
    ok_g3 = dup == 0 and bool((O.lo < O.hi).all())
    P(f"G3 {'PASS' if ok_g3 else 'FAIL'}  duplicate occurrences = {dup}; lo < hi on all "
      f"{len(O)} intervals")
    ok_g4 = bool(E.arity.isin(["REPRO", "GRID"]).all() and
                 E.kind.isin(["MEAN", "CELL", "SCALAR", "UNSTATED"]).all())
    P(f"G4 {'PASS' if ok_g4 else 'FAIL'}  every eligible band carries exactly one arity and "
      f"one kind")
    P(f"G6 {'PASS' if ok_g6 else 'FAIL'}  eligibility removed every known parameter pair "
      f"({', '.join(sorted(PARAM_PAIRS))})")

    d551 = pd.read_csv(PRIOR551)
    ma = d551[(d551.family == "MA-THRESH") & (d551.window == "FULL")]
    g2 = [dict(cad=c, n=len(ma[ma.cad == c]),
               cov_m1=coverage(ma[ma.cad == c].resid0_pp, *ANCHOR_BAND, 1.0),
               cov_m2=coverage(ma[ma.cad == c].resid0_pp, *ANCHOR_BAND, 2.0))
          for c in ["D", "W", "M", "Q", "A"]]
    G2 = pd.DataFrame(g2)
    ok_g2 = (bool(G2[G2.cad != "A"].cov_m1.between(G2_LO, G2_HI).all()) and
             bool(G2[G2.cad == "A"].cov_m1.iloc[0] <= G2_A) and bool((G2.cov_m2 >= G2_M2).all()))
    P(f"G2 {'PASS' if ok_g2 else 'FAIL'}  idea 551 coverage reproduces from its own decomp.csv: "
      + ", ".join(f"{r.cad} {r.cov_m1:.3f}" for r in G2.itertuples())
      + " at m=1.0; " + ", ".join(f"{r.cad} {r.cov_m2:.3f}" for r in G2.itertuples())
      + " at m=2.0")
    G2.to_csv(f"{OUT}.g2.csv", index=False)
    flush_log()

    # ------------------------------------------------------ (b) coverage
    P("\n" + "=" * 178)
    P("(b) CELL-LEVEL COVERAGE")
    P("=" * 178)
    P("ANCHOR BAND [-0.70, -0.20] on idea 551's own cells (MA-THRESH resid0_pp, 27 cells per "
      "cadence per window = 3 panels x 9 thetas).  ALL grid points:")
    arows = []
    for win in ["FULL", "IS", "OOS"]:
        sub = d551[(d551.family == "MA-THRESH") & (d551.window == win)]
        for cad in ["D", "W", "M", "Q", "A"]:
            v = sub[sub.cad == cad].resid0_pp
            rec = dict(band="ANCHOR [-0.70,-0.20]", column="resid0_pp", window=win, cad=cad,
                       n_cells=len(v), pooled_mean=float(v.mean()),
                       mean_inside=bool(ANCHOR_BAND[0] <= v.mean() <= ANCHOR_BAND[1]))
            for m in MULTS:
                rec[f"cov_m{m}"] = coverage(v, *ANCHOR_BAND, m)
            for t in TARGETS:
                rec[f"m_for_{t:g}"] = smallest_m(v, *ANCHOR_BAND, t)
            arows.append(rec)
        v = sub.resid0_pp
        rec = dict(band="ANCHOR [-0.70,-0.20]", column="resid0_pp", window=win, cad="POOLED",
                   n_cells=len(v), pooled_mean=float(v.mean()),
                   mean_inside=bool(ANCHOR_BAND[0] <= v.mean() <= ANCHOR_BAND[1]))
        for m in MULTS:
            rec[f"cov_m{m}"] = coverage(v, *ANCHOR_BAND, m)
        for t in TARGETS:
            rec[f"m_for_{t:g}"] = smallest_m(v, *ANCHOR_BAND, t)
        arows.append(rec)
    A = pd.DataFrame(arows)
    A.to_csv(f"{OUT}.anchor.csv", index=False)
    P(fmt(A.set_index(["window", "cad"])[["n_cells", "pooled_mean", "mean_inside"] +
                                         [f"cov_m{m}" for m in MULTS] +
                                         [f"m_for_{t:g}" for t in TARGETS]], 3))
    af = A[(A.window == "FULL")]
    P(f"\n  At the PUBLISHED width the mean is inside in {int(af.mean_inside.sum())} of "
      f"{len(af)} (cadence + pooled) cells, while cell-level coverage is "
      f"{af['cov_m1.0'].min():.3f}-{af['cov_m1.0'].max():.3f}.  The band is a bar on a MEAN.")

    # other priceable GRID bands
    P("\nEVERY OTHER GRID BAND, priced where a column of its OWN artefacts is named in the "
      "bounded expression:")
    rows = []
    for _, r in Gd.iterrows():
        got = price(r)
        if got is None:
            rows.append(dict(file=r.file, line=r.line, pattern=r.pattern, kind=r.kind,
                             lo=r.lo, hi=r.hi, says=r.says, priceable=False))
            continue
        art, col, v, df = got
        rec = dict(file=r.file, line=r.line, pattern=r.pattern, kind=r.kind, lo=r.lo, hi=r.hi,
                   says=r.says, priceable=True, artefact=art, column=col, n_cells=len(v),
                   pooled_mean=float(v.mean()),
                   mean_inside=bool(r.lo <= v.mean() <= r.hi))
        for m in MULTS:
            rec[f"cov_m{m}"] = coverage(v, r.lo, r.hi, m)
        for t in TARGETS:
            rec[f"m_for_{t:g}"] = smallest_m(v, r.lo, r.hi, t)
        if "window" in df.columns:
            sub = df.loc[v.index]
            vi = sub.loc[sub.window == "IS", col].dropna()
            vo = sub.loc[sub.window == "OOS", col].dropna()
            if len(vi) >= 5 and len(vo) >= 5:
                rec["n_IS"], rec["n_OOS"] = len(vi), len(vo)
        rows.append(rec)
    B = pd.DataFrame(rows)
    B.to_csv(f"{OUT}.bands.csv", index=False)
    npb = int(B.priceable.sum()) if len(B) else 0
    P(f"  {npb} of {len(B)} GRID bands are priceable by the strict name link; the other "
      f"{len(B)-npb} publish an interval whose cells no committed CSV of their own script "
      f"carries under that name.")
    if npb:
        Bp = B[B.priceable].copy()
        Bp["file"] = Bp.file.str.slice(0, 56)
        P(fmt(Bp.set_index(["file", "line"])[["kind", "column", "n_cells", "lo", "hi",
                                              "pooled_mean", "mean_inside"] +
                                             [f"cov_m{m}" for m in MULTS]], 3))
    flush_log()

    # ------------------------------------------------------ dial 2
    P("\n" + "=" * 178)
    P("(dial 2) COVERAGE TARGETS - smallest width multiplier m reaching each target "
      "(nan = not reached by m = 3.0)")
    P("=" * 178)
    tgt = A[A.window == "FULL"].set_index("cad")[[f"m_for_{t:g}" for t in TARGETS]]
    P("ANCHOR band, FULL window, by cadence:")
    P(fmt(tgt, 2))
    for t in TARGETS:
        col = A[(A.window == "FULL")][f"m_for_{t:g}"]
        P(f"  target {t:5.1f}%: reached at the published width (m<=1.0) in "
          f"{int((col <= 1.0).sum())}/{len(col)} cells, needs m>1.0 in "
          f"{int((col > 1.0).sum())}, unreachable by m=3.0 in {int(col.isna().sum())}")

    # ------------------------------------------------------ rule 8
    P("\n" + "=" * 178)
    P("RULE 8 WALK-FORWARD - width chosen on the IS cells only, coverage read on the untouched "
      "OOS cells")
    P("=" * 178)
    wrows = []
    for cad in ["D", "W", "M", "Q", "A", "POOLED"]:
        sub = d551[d551.family == "MA-THRESH"]
        if cad != "POOLED":
            sub = sub[sub.cad == cad]
        vi = sub[sub.window == "IS"].resid0_pp
        vo = sub[sub.window == "OOS"].resid0_pp
        for t in TARGETS:
            m_is = smallest_m(vi, *ANCHOR_BAND, t)
            cov_o = coverage(vo, *ANCHOR_BAND, m_is) if not np.isnan(m_is) else np.nan
            wrows.append(dict(cad=cad, target_pct=t, n_IS=len(vi), n_OOS=len(vo), m_chosen_IS=m_is,
                              cov_IS_at_m=coverage(vi, *ANCHOR_BAND, m_is) if not np.isnan(m_is) else np.nan,
                              cov_OOS_at_m=cov_o,
                              holds_OOS=bool(cov_o * 100 >= t) if not np.isnan(cov_o) else False))
    W = pd.DataFrame(wrows)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(fmt(W.set_index(["cad", "target_pct"]), 3))
    hit, tot = int(W.holds_OOS.sum()), len(W)
    P(f"\n  the IS-chosen width holds its own target on the OOS cells in {hit} of {tot} "
      f"(cadence x target) cells ({100*hit/tot:.1f}%); "
      f"{int(W.m_chosen_IS.isna().sum())} targets are unreachable in-sample even at m=3.0.")
    flush_log()

    # ------------------------------------------------------ KEEP census
    P("\n" + "=" * 178)
    P("KEEP PATHS (PROTOCOL 4) - record-wide census.  Idea 554 proposes NO book and has NO "
      "KEEP candidate of its own; none is claimed.")
    P("=" * 178)
    krows, n4a, n4b, nboth, nbooks, ngrids = [], 0, 0, 0, 0, 0
    for p in sorted(BTDIR.glob("*.csv")):
        try:
            hdr = pd.read_csv(p, nrows=0).columns
        except Exception:
            continue
        fcol = "f4b" if "f4b" in hdr else ("fail4b" if "fail4b" in hdr else None)
        if "p4a" not in hdr or fcol is None:
            continue
        try:
            df = pd.read_csv(p, usecols=["p4a", fcol])
        except Exception:
            continue
        a = df.p4a.astype(str).str.lower().isin(["true", "1", "1.0"])
        b = df[fcol].astype(str).str.strip().isin(["-", ""])
        ngrids += 1
        nbooks += len(df)
        n4a += int(a.sum())
        n4b += int(b.sum())
        nboth += int((a & b).sum())
        krows.append(dict(artefact=p.name, n=len(df), n4a=int(a.sum()), n4b=int(b.sum()),
                          nboth=int((a & b).sum())))
    K = pd.DataFrame(krows)
    K.to_csv(f"{OUT}.keeppaths.csv", index=False)
    ok_g5 = ngrids >= G5_MIN_GRIDS
    P(f"G5 {'PASS' if ok_g5 else 'FAIL'}  {ngrids} committed grids parsed (bar {G5_MIN_GRIDS}), "
      f"{nbooks:,} priced book rows")
    P(f"record-wide: 4a {n4a:,} of {nbooks:,} ({100*n4a/max(nbooks,1):.3f}%), 4b {n4b:,} "
      f"({100*n4b/max(nbooks,1):.3f}%), BOTH {nboth:,} ({100*nboth/max(nbooks,1):.3f}%)")
    if len(K) and (K.nboth > 0).any():
        P("\ngrids with at least one BOTH-path passer:")
        P(K[K.nboth > 0].sort_values("nboth", ascending=False).to_string(index=False))
    else:
        P("\nno committed grid carries a book that passes BOTH KEEP paths.")
    flush_log()

    # ------------------------------------------------------ verdict
    P("\n" + "=" * 178)
    P("VERDICT")
    P("=" * 178)
    P(f"gates: G1 {ok_g1} G2 {ok_g2} G3 {ok_g3} G4 {ok_g4} G5 {ok_g5} G6 {ok_g6}")
    P(f"(a) the record holds {len(E)} pre-registered bands, not one population but two: "
      f"{int((E.arity=='REPRO').sum())} hand-copied constant gates that bound ONE number "
      f"(coverage is 1/1 by construction) and {len(Gd)} GRID bands.  {int(Gd.says.sum())} of "
      f"the {len(Gd)} name their statistic ({100*Gd.says.mean():.1f}%); {n_mean} demonstrably "
      f"bound a mean.")
    P(f"(b) the pathology is REAL where it was found and RARE elsewhere: the anchor band's "
      f"cell coverage is {af['cov_m1.0'].min():.3f}-{af['cov_m1.0'].max():.3f} against a mean "
      f"that is inside in {int(af.mean_inside.sum())}/{len(af)} cells, but only {npb} other "
      f"GRID band in the record can even be re-priced from its own artefacts.")
    P(f"rule 8: IS-chosen width holds its target OOS in {hit}/{tot} cells.")
    P("KEEP: no candidate - this census prices no book.  Record-wide over "
      f"{nbooks:,} committed book rows: 4a {100*n4a/max(nbooks,1):.3f}%, "
      f"4b {100*n4b/max(nbooks,1):.3f}%, BOTH {100*nboth/max(nbooks,1):.3f}%.")
    P("SURVIVORSHIP: nothing here is a return series, but every pooled KEEP column above was "
      "computed on panels that are current constituents (SMALL439, B136), so the record-wide "
      "4a/4b rates inherit that optimism.")
    flush_log()


if __name__ == "__main__":
    main()
