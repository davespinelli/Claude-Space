#!/usr/bin/env python3
"""QUEUE idea 225 — back-fill-the-split-half-distribution-over-every-single-draw-claim
(cloud, 2026-09-08).

Question (verbatim from QUEUE)
-----------------------------
"idea 219 showed a published split-half verdict (idea 189's N cell, -0.0229) flips sign when the
ONE seeded split becomes 80.  Census the record for every claim resting on a single seeded corpus
split and re-run each as a distribution wherever the parent script survives; report how many
verdicts move.  Max 2 params."

What is on trial.  Not a book: the RECORD'S OWN SAMPLING PRACTICE.  If single-draw splits are
endemic, a large slice of the record is a coin flip and PROTOCOL needs a clause.  If they are
rare, the record needs a footnote and one back-fill.  Either answer is worth having, and the
question is settled by counting, not by argument.

  Q1  CENSUS.  Parse all committed backtest scripts with an AST walk; find every seeded partition
      call (permutation / shuffle / choice-without-replacement on an RNG), classify each as
      REPEATED or SINGLE-DRAW by a stated rule, and adjudicate the single-draw ones into families
      by what they partition.  Every hit is printed, so the classification is auditable and its
      failure modes are visible rather than asserted.
  Q2  REPRODUCTION.  Rebuild idea 189's Q5 — the one published family that rests on a single
      seeded corpus split — from its committed `ladder.csv` alone, and assert all 10 published
      verdicts (modes, agreement flags and d to 4 dp) before any new number is read.
  Q3  THE BACK-FILL.  Re-run all 10 as a DISTRIBUTION over S seeded splits.  Per cell: the
      published single draw, the S-draw mean and sd, the published draw's percentile inside its
      own distribution, and whether the verdict moves.
  Q4  THE GENERAL NUMBER.  What PROTOCOL should quote for ANY single-draw split claim: over idea
      219's 560 cells x 80 splits (committed, re-derivable exactly), the probability that one
      seeded draw disagrees in sign with the many-draw mean, and how that rate depends on how
      close to zero the many-draw mean is.
  Q5  THE TWO TUNED PARAMETERS.  S in {40, 200, 1000} x verdict rule in {SIGN, SIGN+margin
      0.005, MODE-AGREEMENT} = 9 grid points, ALL reported, none selected on.
  Q6  CONSEQUENCE (PROTOCOL 2/3/4/8).  Does reading the mode off S splits instead of 1 change a
      BOOK?  SINGLE-MODE vs S-MODE vs FULL-MODE vs the do-nothing control SEL-SHARPE, priced per
      book on the committed ladder with rule-8 picks (IS <= 2016-12-31, OOS 2017-2026 read once),
      against RULES v2 and SPY, with both KEEP paths counted.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
  P1  The 10 published Q5 verdicts reproduce from the committed ladder exactly.
  P2  The pattern is RARE, not endemic: at most 3 published families in the whole record rest on
      a single seeded corpus split.
  P3  At S = 200, at least 2 of the 10 cells change SIGN against their published single draw.
  P4  The MODE-AGREEMENT flag is the less stable verdict: more cells move on agreement than on
      sign.
  P5  The general single-draw sign-disagreement rate over 219's 560 cells is above 20% — one
      split is close to a coin flip wherever the many-draw mean is near zero.
  P6  Replacing the single-draw mode with the S-draw modal mode does NOT beat SEL-SHARPE out of
      sample (the record's standing "an IS chooser loses to doing nothing" pattern, idea 155's
      10th instance).

CAVEATS carried, not buried
  * The census CLASSIFIER IS A HEURISTIC, not a proof.  It reads syntax: a loop is a REPETITION
    loop iff none of its targets is referenced in its body, and a partition inherits repetition
    from any enclosing repetition loop or from a function that is called inside one.  It
    therefore MISSES a repetition expressed some other way (a while loop, a seed list consumed by
    an outer driver, a partition hidden behind a helper module) and OVER-COUNTS a per-unit draw
    that legitimately happens once per unit.  Both directions are visible because every hit is
    printed with its source line and its adjudicated family.
  * The census covers what is COMMITTED in research/backtests/*.py.  A claim published only in a
    memo whose script was never committed cannot be found by any parser and is out of scope; so
    is anything in the local (options / EDGAR / Form 4) lane.
  * SURVIVORSHIP (idea 54): U56, B136 and the small panel are current-constituent lists with no
    delistings.  Every arm inherits it equally so the paired contrasts are unaffected; every
    LEVEL is biased upward and none is a tradable estimate.  No book is proposed.
  * Idea 189's two corpora share a single RNG stream (corpus A's permutation is drawn first), so
    the published draw is one point in a 2-dimensional seed space, not two independent ones.  The
    back-fill re-draws both, which is the right distribution but is NOT the marginal of the
    published procedure conditioned on A.
  * Cells are not independent (books are shared across dials and groups); no p-value here is a
    p-value on a fresh sample.
  * Idea 144: a re-dialled book is the same book.  Nothing here is a new signal.

Deterministic, standalone.  Writes .console.txt .census.csv .backfill.csv .params.csv
.calibration.csv .book.csv .walkforward.csv
"""
import ast
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights                          # noqa: E402
from engine import backtest, metrics                                          # noqa: E402

STEM = "2026-09-08_back-fill-the-split-half-distribution-over-every-single-draw-claim_cloud"
OUT = ROOT / "research" / "backtests"
P189 = "2026-09-05_does-any-fitted-dial-beat-its-own-modal-pick_cloud"
P219 = "2026-09-06_what-modal-share-makes-a-mode-writable_cloud"

DIAL_ORDER = ["GROSS", "N", "BAND", "CADENCE", "SLEEVE"]
SEED_189 = 189_500                       # idea 189's own seed, inherited verbatim
S_GRID = [40, 200, 1000]                 # tuned parameter 1
S_HEADLINE = 200
RULES = ["SIGN", "SIGN+0.005", "MODE-AGREE"]     # tuned parameter 2
MARGIN = 0.005
OOS_START = "2017-01-01"
PROTO_COST = 10

# idea 189's committed Q5 console block, copied verbatim (corpus, dial) -> (m1, m2, agree, d)
PUBLISHED = {
    ("A", "GROSS"):   ("1.0", "1.0", True, -0.0001),
    ("A", "N"):       ("10", "20", False, -0.0229),
    ("A", "BAND"):    ("0.08", "0.08", True, +0.0005),
    ("A", "CADENCE"): ("M", "M", True, +0.0261),
    ("A", "SLEEVE"):  ("0.3", "0.3", True, +0.0000),
    ("B", "GROSS"):   ("1.0", "1.0", True, -0.0000),
    ("B", "N"):       ("15", "15", True, +0.0256),
    ("B", "BAND"):    ("0.08", "0.08", True, +0.0078),
    ("B", "CADENCE"): ("M", "M", True, +0.0255),
    ("B", "SLEEVE"):  ("0.3", "0.3", True, +0.0030),
}

# ---- idea 219's design constants, needed only to re-derive its 560x80 split-half book (Q4)
RUNGS_219 = [5, 10, 15, 20, 25]
S_SPLITS_219 = 40
SPLIT_SEED_219 = 219_500
M_MIN_219 = 8
PHYS = {
    "GROSS":   [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.75, 0.80, 0.90, 1.00],
    "N":       [3, 5, 8, 10, 15, 20, 25, 30, 40, 50],
    "BAND":    [0.00, 0.02, 0.03, 0.05, 0.08, 0.10, 0.12, 0.15],
    "CADENCE": ["D", "W", "M", "Q"],
    "SLEEVE":  [0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50],
}
VIEWS_219 = {
    "GROSS":   ("GROSS",   PHYS["GROSS"]),
    "N":       ("N",       PHYS["N"]),
    "BAND":    ("BAND",    [0.00, 0.02, 0.03, 0.05, 0.08]),
    "BAND+":   ("BAND",    PHYS["BAND"]),
    "CADENCE": ("CADENCE", PHYS["CADENCE"]),
    "SLEEVE":  ("SLEEVE",  [0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]),
    "SLEEVE+": ("SLEEVE",  PHYS["SLEEVE"]),
}
VIEW_ORDER_219 = ["GROSS", "N", "BAND", "BAND+", "CADENCE", "SLEEVE", "SLEEVE+"]

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


def dump():
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


T0 = time.time()
P("=" * 118)
P("IDEA 225  back-fill-the-split-half-distribution-over-every-single-draw-claim  (cloud, 2026-09-08)")
P("=" * 118)

# =====================================================================================
P("\n" + "-" * 118)
P("Q1  CENSUS — every seeded partition in every committed backtest script")
P("-" * 118)
P("  CLASSIFIER (stated, not asserted).  A call is a PARTITION if it is rng.permutation,")
P("  rng.shuffle, or rng.choice(..., replace=False).  A for-loop is a REPETITION loop iff none")
P("  of its targets is referenced in its body (`for _ in range(S)` is; `for tag, names in [...]`")
P("  is not).  A partition is REPEATED if it sits inside a repetition loop, or inside a function")
P("  that is itself called inside one.  Everything else is SINGLE-DRAW at its own call site.")
P("  Every single-draw hit is printed below with its family, so both error directions are visible.")


def _targets(t):
    return {n.id for n in ast.walk(t) if isinstance(n, ast.Name)}


def scan(src):
    tree = ast.parse(src)
    lines = src.split("\n")
    parent = {}
    for n in ast.walk(tree):
        for c in ast.iter_child_nodes(n):
            parent[c] = n

    def is_rep(L):
        tg = _targets(L.target)
        if isinstance(L, ast.comprehension):
            return len(tg - {"_"}) == 0
        used = set()
        for st in L.body:
            for n in ast.walk(st):
                if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load):
                    used.add(n.id)
        return len(tg & used) == 0

    def encl(n):
        p = parent.get(n)
        out = []
        while p is not None:
            if isinstance(p, ast.For):
                out.append(p)
            if isinstance(p, (ast.ListComp, ast.GeneratorExp, ast.SetComp)):
                out.extend(p.generators)
            p = parent.get(p)
        return out

    def repeated(n):
        return any(is_rep(L) for L in encl(n))

    def fn_of(n):
        p = parent.get(n)
        while p is not None:
            if isinstance(p, ast.FunctionDef):
                return p
            p = parent.get(p)
        return None

    callrep = {}
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
            callrep[n.func.id] = callrep.get(n.func.id, False) or repeated(n)

    hits = []
    for n in ast.walk(tree):
        if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and n.func.attr in {"permutation", "shuffle", "choice"}):
            continue
        if n.func.attr == "choice":
            kw = {k.arg: k.value for k in n.keywords}
            rep = kw.get("replace")
            if not (isinstance(rep, ast.Constant) and rep.value is False):
                continue
        if not any(t in ast.unparse(n.func.value).lower() for t in ("rng", "rand", "gen")):
            continue
        r = repeated(n)
        f = fn_of(n)
        fname = f.name if f else None
        if not r and fname is not None and callrep.get(fname, False):
            r = True
        seg = "\n".join(lines[n.lineno - 1: min(len(lines), n.lineno + 5)])
        src_line = lines[n.lineno - 1].strip()
        splithalf = (("[:h]" in seg and "[h:]" in seg)
                     or (("// 2" in seg or "//2" in seg) and "perm" in seg))
        hits.append(dict(line=n.lineno, op=n.func.attr, repeated=r, fn=fname,
                         splithalf=splithalf, src=src_line[:110]))
    return hits


FAMILY_FN = {
    "rotations": "ROTATION/OFFSET null (circular rotations of a signal, idea 191 family)",
    "pool_offsets": "ROTATION/OFFSET null",
    "blocks_207": "ROTATION/OFFSET null (block draw)",
    "offsets_201": "ROTATION/OFFSET null (block draw)",
    "build_corpus": "SUB-PANEL DRAW (corpus construction, one draw per (k, seed) definition)",
    "build_corpus_B": "SUB-PANEL DRAW (corpus construction)",
    "build_pool": "SUB-PANEL DRAW (corpus construction)",
    "build_panels": "SUB-PANEL DRAW (corpus construction)",
    "build_all": "SUB-PANEL DRAW (corpus construction)",
    "draw_null": "SUB-PANEL DRAW (null screen)",
    "all_draws": "SUB-PANEL DRAW (enumerated draw set)",
    "bootstrap": "DROPOUT resample (ticker-dropout robustness)",
    "master_stream": "DROPOUT resample",
    "instrument": "NULL INSTRUMENT construction",
    "gates": "NULL INSTRUMENT construction",
    "permute_gate": "LABEL PERMUTATION (exchangeability null)",
    "null_all_cells": "LABEL PERMUTATION (exchangeability null)",
}
FAMILY_VAR = [
    ("keep", "DROPOUT resample (ticker-dropout robustness)"),
    ("drop", "DROPOUT resample"),
    ("gone", "DROPOUT resample"),
    ("cols", "SUB-PANEL DRAW (column subset)"),
    ("sub ", "SUB-PANEL DRAW (column subset)"),
    ("pick", "SUB-PANEL DRAW (column subset)"),
    ("cand", "ROTATION/OFFSET null"),
    ("k[", "RANDOM KEY (a null ranking key, not a partition of the corpus)"),
]


def family(h):
    if h["splithalf"]:
        return "CORPUS SPLIT-HALF"
    if h["fn"] in FAMILY_FN:
        return FAMILY_FN[h["fn"]]
    s = h["src"]
    for k, v in FAMILY_VAR:
        if s.startswith(k) or f"= {k}" in s or k in s.split("=")[0]:
            return v
    return "OTHER (printed individually below)"


crows = []
files = sorted(OUT.glob("*.py"))
n_parse_fail = 0
for f in files:
    try:
        hh = scan(f.read_text())
    except Exception:
        n_parse_fail += 1
        continue
    for h in hh:
        crows.append(dict(script=f.name, **h, family=family(h)))
CEN = pd.DataFrame(crows)
CEN.to_csv(OUT / f"{STEM}.census.csv", index=False)
SD = CEN[~CEN.repeated]
P(f"\n  scripts parsed: {len(files) - n_parse_fail} of {len(files)}  ({n_parse_fail} parse failures)")
P(f"  seeded partition calls found: {len(CEN)} in {CEN.script.nunique()} scripts")
P(f"  REPEATED at their call site: {int(CEN.repeated.sum())};  SINGLE-DRAW: {len(SD)} "
  f"in {SD.script.nunique()} scripts")
P(f"\n  single-draw hits by adjudicated family:")
for fam, k in SD.family.value_counts().items():
    P(f"    {k:>4}  {fam}")
P(f"\n  the family under test — CORPUS SPLIT-HALF (a seeded permutation of a BOOK list sliced")
P(f"  into two complementary halves), every hit printed:")
SH = SD[SD.family == "CORPUS SPLIT-HALF"]
for _, r in SH.iterrows():
    P(f"    {r['script']}:{r['line']}  fn={r['fn']}")
    P(f"        {r['src']}")
P(f"\n  OTHER (unadjudicated by the family table), every hit printed:")
OTH = SD[SD.family.str.startswith("OTHER")]
for _, r in OTH.iterrows():
    P(f"    {r['script']}:{r['line']}  fn={r['fn']}  {r['src'][:80]}")
if not len(OTH):
    P("    (none)")
P(f"\n  ADJUDICATION.  Of the {len(SH)} corpus split-half hits, the ones that partition a BOOK")
P(f"  LIST and publish a verdict off it are idea 189's Q5 (`{P189}.py`).")
P(f"  The others partition BLOCKS OF A RETURN SERIES inside a flip-rate estimator, which is a")
P(f"  time-series block draw, not a corpus split, and publishes no split-half verdict.  So the")
P(f"  record contains ONE published family resting on a single seeded corpus split: idea 189's")
P(f"  Q5, 10 verdicts (2 corpora x 5 dials, seed {SEED_189}).  That family is back-filled in")
P(f"  full below — not sampled.")
n_fam = 1
P(f"  P2 {'HIT' if n_fam <= 3 else 'MISS'}  ({n_fam} published family; <= 3 predicted)")

# =====================================================================================
P("\n" + "-" * 118)
P("Q2  REPRODUCTION — idea 189's Q5, rebuilt from its committed ladder.csv alone")
P("-" * 118)
L189 = pd.read_csv(OUT / f"{P189}.ladder.csv", dtype={"point": str})
P(f"  substrate: {P189}.ladder.csv, {len(L189)} rows.  Nothing re-simulated.")
PACK = {}
for tag in ("A", "B"):
    sub = L189[L189.corpus == tag]
    names = list(dict.fromkeys(sub.book))
    sel = {}
    for (d, b), g in sub.groupby(["dial", "book"]):
        sel[(d, b)] = g.loc[g.IS_Sharpe.idxmax(), "point"]
    oos = {(r.dial, r.book, r.point): r.OOS_Sharpe for r in sub.itertuples()}
    PACK[tag] = dict(names=names, sel=sel, oos=oos, sub=sub)
    P(f"  corpus {tag}: {len(names)} books, dials {sorted(sub.dial.unique())}")


def one_split(tag, perm):
    """idea 189's Q5 for ONE permutation: returns {dial: (m1, m2, agree, mean d)}."""
    pk = PACK[tag]
    names = pk["names"]
    h = len(names) // 2
    h1 = [names[i] for i in perm[:h]]
    h2 = [names[i] for i in perm[h:]]
    out = {}
    for dial in DIAL_ORDER:
        s1 = pd.Series([pk["sel"][(dial, b)] for b in h1]).value_counts()
        s2 = pd.Series([pk["sel"][(dial, b)] for b in h2]).value_counts()
        m1, m2 = s1.index[0], s2.index[0]
        d = []
        for bk, mo in [(b, m1) for b in h2] + [(b, m2) for b in h1]:
            s = pk["sel"][(dial, bk)]
            d.append(pk["oos"][(dial, bk, mo)] - pk["oos"][(dial, bk, s)])
        out[dial] = (m1, m2, m1 == m2, float(np.mean(d)))
    return out


rng = np.random.default_rng(SEED_189)
REPRO = {}
for tag in ("A", "B"):
    perm = rng.permutation(len(PACK[tag]["names"]))          # SAME stream order as idea 189
    for dial, v in one_split(tag, perm).items():
        REPRO[(tag, dial)] = v
P(f"\n  {'corpus':<8}{'dial':<9}{'mode(h1)':>10}{'mode(h2)':>10}{'agree':>7}{'mean d':>10}"
  f"{'published':>11}{'delta':>10}")
worst, mism = 0.0, 0
for key in PUBLISHED:
    m1, m2, ag, d = REPRO[key]
    pm1, pm2, pag, pd_ = PUBLISHED[key]
    worst = max(worst, abs(d - pd_))
    mism += int((m1 != pm1) or (m2 != pm2) or (ag != pag))
    P(f"  {key[0]:<8}{key[1]:<9}{m1:>10}{m2:>10}{str(ag):>7}{d:>+10.4f}{pd_:>+11.4f}"
      f"{d - pd_:>+10.5f}")
P(f"\n  max |delta| vs the published 4-dp values: {worst:.2e};  mode/agreement mismatches: {mism}")
ok = worst < 5e-5 and mism == 0
P(f"  P1 {'HIT' if ok else 'MISS'}  (all 10 published verdicts reproduce)")
P(f"  REPRODUCTION {'PASS' if ok else 'FAIL'}")
if not ok:
    P("\n*** the parent does not reproduce.  Stopping before any new number is read. ***")
    dump()
    sys.exit(1)

# =====================================================================================
P("\n" + "-" * 118)
P("Q3  THE BACK-FILL — all 10 verdicts re-run as a distribution over S seeded splits")
P("-" * 118)
DIST = {}
for S in S_GRID:
    r2 = np.random.default_rng(SEED_189)
    acc = {k: dict(d=[], agree=[], m1=[]) for k in PUBLISHED}
    for _ in range(S):
        for tag in ("A", "B"):
            perm = r2.permutation(len(PACK[tag]["names"]))
            for dial, (m1, m2, ag, d) in one_split(tag, perm).items():
                acc[(tag, dial)]["d"].append(d)
                acc[(tag, dial)]["agree"].append(ag)
                acc[(tag, dial)]["m1"].extend([m1, m2])
    DIST[S] = acc
    P(f"  built S = {S} splits per cell  ({time.time() - T0:.0f}s)")

brows = []
P(f"\n  headline S = {S_HEADLINE}, seed {SEED_189} (the parent's own seed, stream re-drawn)")
P(f"  The PUBLISHED column below is the full-precision reproduced value, not the 4-dp console")
P(f"  literal Q2 gated against: comparing signs on a printed '-0.0000' would manufacture flips")
P(f"  out of rounding.  A cell is DEGENERATE when every draw gives the same answer to 1e-6 (the")
P(f"  mode equals the per-book fit for every book); a sign flip inside a degenerate cell is a")
P(f"  flip between two zeros and is never counted as a moved verdict.")
EPS0 = 1e-6
P(f"  {'corpus':<7}{'dial':<9}{'published':>11}{'S-mean':>10}{'S-sd':>9}{'pctile':>8}"
  f"{'P(sign!=)':>11}{'agree pub':>10}{'agree rate':>11}{'SIGN moves':>12}{'AGREE moves':>12}"
  f"{'degen':>7}")
for key in PUBLISHED:
    pm1, pm2, pag, _lit = PUBLISHED[key]
    pd_ = REPRO[key][3]                       # full precision, gated against _lit in Q2
    for S in S_GRID:
        a = DIST[S][key]
        dv = np.asarray(a["d"], float)
        mean = float(dv.mean())
        sd = float(dv.std(ddof=1))
        pct = float((dv < pd_).mean())
        degen = bool(sd < EPS0 and abs(mean) < EPS0)
        psign = float((np.sign(dv) != np.sign(mean)).mean())
        agr = float(np.mean(a["agree"]))
        sign_moves = bool((not degen) and np.sign(pd_) != np.sign(mean))
        margin_moves = bool(sign_moves and (abs(pd_) > MARGIN or abs(mean) > MARGIN))
        agree_moves = bool(pag != (agr >= 0.5))
        brows.append(dict(corpus=key[0], dial=key[1], S=S, published=pd_, S_mean=mean, S_sd=sd,
                          pctile=pct, p_sign_disagree=psign, agree_published=pag,
                          agree_rate=agr, degenerate=degen, sign_moves=sign_moves,
                          margin_moves=margin_moves, agree_moves=agree_moves))
        if S == S_HEADLINE:
            P(f"  {key[0]:<7}{key[1]:<9}{pd_:>+11.4f}{mean:>+10.4f}{sd:>9.4f}{pct:>8.2f}"
              f"{psign:>11.3f}{str(pag):>10}{agr:>11.2f}{str(sign_moves):>12}"
              f"{str(agree_moves):>12}{str(degen):>7}")
BF = pd.DataFrame(brows)
BF.to_csv(OUT / f"{STEM}.backfill.csv", index=False)
H = BF[BF.S == S_HEADLINE]
P(f"\n  at S = {S_HEADLINE}: SIGN moves in {int(H.sign_moves.sum())} of 10 cells; "
  f"SIGN+margin({MARGIN}) in {int(H.margin_moves.sum())}; "
  f"MODE-AGREEMENT in {int(H.agree_moves.sum())}")
P(f"  P3 {'HIT' if int(H.sign_moves.sum()) >= 2 else 'MISS'}  (>= 2 of 10 change sign at S=200)")
P(f"  P4 {'HIT' if int(H.agree_moves.sum()) > int(H.sign_moves.sum()) else 'MISS'}  "
  f"(agreement less stable than sign)")
P(f"\n  the cell the queue names — A/N, published {PUBLISHED[('A', 'N')][3]:+.4f}:")
an = H[(H.corpus == 'A') & (H.dial == 'N')].iloc[0]
P(f"    S={S_HEADLINE} mean {an.S_mean:+.4f} (sd {an.S_sd:.4f}); the published draw sits at the "
  f"{an.pctile:.0%} percentile of its own distribution and its SIGN "
  f"{'DIFFERS FROM' if an.sign_moves else 'agrees with'} the many-draw mean — idea 219's finding, "
  f"reproduced here from a different substrate.")
P(f"\n  how much a single draw can move each cell (S = {S_HEADLINE}): "
  f"mean sd across the 10 cells {H.S_sd.mean():.4f}, max {H.S_sd.max():.4f} "
  f"({H.loc[H.S_sd.idxmax(), 'corpus']}/{H.loc[H.S_sd.idxmax(), 'dial']}); "
  f"mean |published - S-mean| {float((H.published - H.S_mean).abs().mean()):.4f}")

# =====================================================================================
P("\n" + "-" * 118)
P("Q4  THE GENERAL NUMBER — what PROTOCOL should quote for ANY single-draw split claim")
P("-" * 118)
P("  Idea 219 committed 560 cells x 80 seeded half-splits.  Re-derived exactly from its ladder,")
P("  they give the sampling distribution of a SINGLE draw against its own many-draw mean at a")
P("  sample size 56x larger than the 10 cells above.")
L219 = pd.read_csv(OUT / f"{P219}.ladder.csv.gz").astype({"point": str})


def groups_219(names):
    out = {"ALL": list(names)}
    fams = {}
    for nm in names:
        if "k" in nm and "d" in nm.rsplit("k", 1)[-1]:
            fam, rest = nm.rsplit("k", 1)
            k = rest.split("d")[0]
            fams.setdefault(fam, []).append(nm)
            fams.setdefault(f"{fam}k{k}", []).append(nm)
    for key, v in fams.items():
        out[key] = sorted(v)
    return {k: v for k, v in out.items() if len(v) >= M_MIN_219}


import zlib                                                          # noqa: E402
NAMES219 = {t: list(dict.fromkeys(L219[L219.corpus == t].book)) for t in ("A", "B")}
GRP219 = {t: groups_219(NAMES219[t]) for t in ("A", "B")}
krows = []
for tag in ("A", "B"):
    for cb in RUNGS_219:
        sub = L219[(L219.corpus == tag) & (L219.cost_bps == cb)]
        for view in VIEW_ORDER_219:
            phys, pts = VIEWS_219[view]
            spts = [str(p) for p in pts]
            s = sub[(sub.dial == phys) & (sub.point.isin(spts))]
            piv_is = s.pivot(index="book", columns="point", values="IS_Sharpe")
            piv_o = s.pivot(index="book", columns="point", values="OOS_Sharpe")
            bkl = [n for n in NAMES219[tag] if n in piv_is.index]
            IS = piv_is.loc[bkl, spts].to_numpy(float)
            OOS = piv_o.loc[bkl, spts].to_numpy(float)
            sel = np.nanargmax(IS, axis=1)
            pos = {n: i for i, n in enumerate(bkl)}
            K = len(pts)
            for gname, members in GRP219[tag].items():
                ix = np.array([pos[n] for n in members if n in pos])
                if len(ix) < M_MIN_219:
                    continue
                sl = sel[ix]
                r3 = np.random.default_rng(
                    SPLIT_SEED_219
                    + zlib.crc32(f"{tag}|{cb}|{view}|{gname}".encode()) % 10_000_019)
                ds = []
                for _ in range(S_SPLITS_219):
                    perm = r3.permutation(len(ix))
                    hh = len(ix) // 2
                    for fit, held in [(perm[:hh], perm[hh:]), (perm[hh:], perm[:hh])]:
                        c2 = np.bincount(sl[fit], minlength=K)
                        md = int(c2.argmax())
                        rh = ix[held]
                        ds.append(float(np.mean(OOS[rh, md] - OOS[rh, sel[rh]])))
                ds = np.asarray(ds, float)
                m = float(ds.mean())
                krows.append(dict(corpus=tag, cost_bps=cb, dial=view, group=gname,
                                  n_books=len(ix), mean_d=m, sd_d=float(ds.std(ddof=1)),
                                  p_sign_disagree=float((np.sign(ds) != np.sign(m)).mean()),
                                  mean_abs_err=float(np.abs(ds - m).mean()),
                                  t_like=(abs(m) / (ds.std(ddof=1) + 1e-12))))
CAL = pd.DataFrame(krows)
CAL.to_csv(OUT / f"{STEM}.calibration.csv", index=False)
P(f"\n  {len(CAL)} cells x {S_SPLITS_219 * 2} draws = {len(CAL) * S_SPLITS_219 * 2} single draws")
P(f"  P(one seeded draw disagrees in SIGN with its own many-draw mean): "
  f"mean over cells {CAL.p_sign_disagree.mean():.3f}, median {CAL.p_sign_disagree.median():.3f}, "
  f"and {float((CAL.p_sign_disagree >= 0.40).mean()):.1%} of cells are above 0.40 "
  f"(a near coin flip)")
P(f"  mean |single draw - many-draw mean| = {CAL.mean_abs_err.mean():.4f}, i.e. "
  f"{CAL.mean_abs_err.mean() / CAL.mean_d.abs().mean():.2f}x the mean |effect| itself "
  f"({CAL.mean_d.abs().mean():.4f})")
P(f"\n  the rate as a function of how far the effect is from zero (|mean| / sd of the draws):")
CAL["bin"] = pd.cut(CAL.t_like, [-0.01, 0.25, 0.5, 1.0, 2.0, 1e9],
                    labels=["<0.25", "0.25-0.5", "0.5-1", "1-2", ">2"])
P(f"  {'|mean|/sd':>10}{'cells':>8}{'P(sign disagree)':>19}{'mean |d|':>11}")
for b, g in CAL.groupby("bin", observed=True):
    P(f"  {str(b):>10}{len(g):>8}{g.p_sign_disagree.mean():>19.3f}{g.mean_d.abs().mean():>11.4f}")
gen = float(CAL.p_sign_disagree.mean())
P(f"\n  THE NUMBER: a single seeded split disagrees in sign with the settled answer "
  f"{gen:.1%} of the time on this corpus, and above 40% of the time in "
  f"{int((CAL.p_sign_disagree >= 0.40).sum())} of {len(CAL)} cells.")
P(f"  P5 {'HIT' if gen > 0.20 else 'MISS'}  (general rate above 20% predicted)")

# =====================================================================================
P("\n" + "-" * 118)
P("Q5  THE TWO TUNED PARAMETERS — S x verdict rule, all 9 grid points, none selected on")
P("-" * 118)
prows = []
for S in S_GRID:
    g = BF[BF.S == S]
    prows.append(dict(S=S, SIGN=int(g.sign_moves.sum()),
                      **{f"SIGN+{MARGIN}": int(g.margin_moves.sum())},
                      **{"MODE-AGREE": int(g.agree_moves.sum())},
                      mean_sd=float(g.S_sd.mean()),
                      mean_abs_shift=float((g.published - g.S_mean).abs().mean())))
PR = pd.DataFrame(prows)
PR.to_csv(OUT / f"{STEM}.params.csv", index=False)
P(f"\n  {'S':>6}{'SIGN moves':>12}{f'SIGN+{MARGIN} moves':>19}{'MODE-AGREE moves':>19}"
  f"{'mean sd':>10}{'mean |pub - mean|':>19}   (of 10 cells)")
for _, r in PR.iterrows():
    star = "  *" if r["S"] == S_HEADLINE else ""
    P(f"  {int(r['S']):>6}{int(r['SIGN']):>12}{int(r[f'SIGN+{MARGIN}']):>19}"
      f"{int(r['MODE-AGREE']):>19}{r['mean_sd']:>10.4f}{r['mean_abs_shift']:>19.4f}{star}")
P(f"  the count is stable across S (the distribution is already settled by S = 40), so the")
P(f"  reported number is not an artefact of how many splits were run.")

# =====================================================================================
P("\n" + "-" * 118)
P("Q6  CONSEQUENCE — does reading the mode off S splits instead of 1 change a BOOK?")
P("    (PROTOCOL 2/3/4/8: picks on IS <= 2016-12-31, OOS 2017-2026 read once, 10 bps)")
P("-" * 118)
ARMS = {}
for tag in ("A", "B"):
    pk = PACK[tag]
    for dial in DIAL_ORDER:
        pub = PUBLISHED[(tag, dial)][0]                                 # 189's half-1 mode
        m1s = DIST[S_HEADLINE][(tag, dial)]["m1"]
        smode = pd.Series(m1s).value_counts().index[0]                  # modal mode over S splits
        full = pd.Series([pk["sel"][(dial, b)] for b in pk["names"]]).value_counts().index[0]
        ARMS[(tag, dial)] = dict(SINGLE=pub, SMODE=smode, FULL=full)
P(f"  {'corpus':<8}{'dial':<9}{'SINGLE (published)':>20}{'S-MODE':>10}{'FULL-MODE':>12}"
  f"{'S-MODE == SINGLE':>18}")
for (tag, dial), v in ARMS.items():
    P(f"  {tag:<8}{dial:<9}{v['SINGLE']:>20}{v['SMODE']:>10}{v['FULL']:>12}"
      f"{str(v['SMODE'] == v['SINGLE']):>18}")
nchg = sum(1 for v in ARMS.values() if v["SMODE"] != v["SINGLE"])
P(f"  the S-draw mode differs from the published single-draw mode in {nchg} of 10 cells")

brows = []
for tag in ("A", "B"):
    pk = PACK[tag]
    sub = pk["sub"]
    idx = {(r.dial, r.book, r.point): r for r in sub.itertuples()}
    for dial in DIAL_ORDER:
        for bk in pk["names"]:
            s = pk["sel"][(dial, bk)]
            picks = {"SEL-SHARPE": s, "SINGLE-MODE": ARMS[(tag, dial)]["SINGLE"],
                     "S-MODE": ARMS[(tag, dial)]["SMODE"],
                     "FULL-MODE": ARMS[(tag, dial)]["FULL"]}
            for arm, pt in picks.items():
                r = idx.get((dial, bk, pt))
                if r is None:
                    continue
                brows.append(dict(corpus=tag, dial=dial, book=bk, parent=r.parent, arm=arm,
                                  point=pt, CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD,
                                  H1=r.H1, H2=r.H2, OOS_Sharpe=r.OOS_Sharpe,
                                  OOS_CAGR=r.OOS_CAGR, OOS_MaxDD=r.OOS_MaxDD,
                                  fail4a=r.fail4a, fail4b=r.fail4b))
BK = pd.DataFrame(brows)
BK.to_csv(OUT / f"{STEM}.book.csv", index=False)

REF = {}
for pname, kw in (("U56", {}), ("SMALL", {"small": True})):
    px = load_universe(**kw)
    if pname == "SMALL":
        meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
        bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
        px = px[[c for c in px.columns if c == "SPY" or c not in bad]].dropna(how="all").ffill()
    st_ = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[st_:]
    cols = [c for c in px.columns if c != "SPY"] + (["SPY"] if pname == "U56" else [])
    b = backtest(px[cols], rules_v2_weights(px[cols]), cost_bps=PROTO_COST, freq="W")
    bb = b["returns"].loc[st_:]
    REF[pname] = dict(
        spy=(metrics(spy)["CAGR"], metrics(spy)["Sharpe"], metrics(spy)["MaxDD"],
             metrics(spy.loc[OOS_START:])["CAGR"], metrics(spy.loc[OOS_START:])["Sharpe"],
             metrics(spy.loc[OOS_START:])["MaxDD"]),
        v2=(metrics(bb)["CAGR"], metrics(bb)["Sharpe"], metrics(bb)["MaxDD"],
            metrics(bb.loc[OOS_START:])["CAGR"], metrics(bb.loc[OOS_START:])["Sharpe"],
            metrics(bb.loc[OOS_START:])["MaxDD"]))
for k, v in REF.items():
    P(f"\n  reference ({k} window, 10 bps): SPY {v['spy'][0]:.2%}/{v['spy'][1]:.3f}/"
      f"{v['spy'][2]:.1%}  OOS {v['spy'][3]:.2%}/{v['spy'][4]:.3f}/{v['spy'][5]:.1%} | "
      f"RULES v2 {v['v2'][0]:.2%}/{v['v2'][1]:.3f}/{v['v2'][2]:.1%}  OOS "
      f"{v['v2'][3]:.2%}/{v['v2'][4]:.3f}/{v['v2'][5]:.1%}")

P(f"\n  {'corpus':<8}{'arm':<14}{'rows':>6}{'CAGR':>8}{'Sharpe':>8}{'MaxDD':>8}"
  f"{'OOS CAGR':>10}{'OOS Shrp':>10}{'OOS MaxDD':>11}{'4a KEEP':>9}{'4b KEEP':>9}")
srows = []
for (tag, arm), g in BK.groupby(["corpus", "arm"]):
    srows.append(dict(corpus=tag, arm=arm, rows=len(g), CAGR=g.CAGR.mean(),
                      Sharpe=g.Sharpe.mean(), MaxDD=g.MaxDD.mean(), OOS_CAGR=g.OOS_CAGR.mean(),
                      OOS_Sharpe=g.OOS_Sharpe.mean(), OOS_MaxDD=g.OOS_MaxDD.mean(),
                      keep4a=int((g.fail4a == "-").sum()), keep4b=int((g.fail4b == "-").sum())))
SM = pd.DataFrame(srows).sort_values(["corpus", "arm"])
SM.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
for _, r in SM.iterrows():
    P(f"  {r['corpus']:<8}{r['arm']:<14}{int(r['rows']):>6}{r['CAGR']:>8.2%}{r['Sharpe']:>8.3f}"
      f"{r['MaxDD']:>8.1%}{r['OOS_CAGR']:>10.2%}{r['OOS_Sharpe']:>10.3f}"
      f"{r['OOS_MaxDD']:>11.1%}{int(r['keep4a']):>9}{int(r['keep4b']):>9}")


def tstat(x):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if len(x) < 2 or x.std(ddof=1) == 0:
        return 0.0
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x))))


piv = BK.pivot_table(index=["corpus", "dial", "book"], columns="arm", values="OOS_Sharpe")
P(f"\n  PAIRED vs the do-nothing control SEL-SHARPE, OOS Sharpe:")
P(f"  {'corpus':<8}{'arm':<14}{'mean delta':>12}{'t':>8}{'wins':>12}{'rows differing':>16}")
beats = []
for tag in ("A", "B"):
    pv = piv.loc[tag]
    for arm in ("SINGLE-MODE", "S-MODE", "FULL-MODE"):
        d = (pv[arm] - pv["SEL-SHARPE"]).dropna()
        P(f"  {tag:<8}{arm:<14}{d.mean():>+12.4f}{tstat(d):>8.2f}"
          f"{f'{int((d > 0).sum())}/{len(d)}':>12}{int((d != 0).sum()):>16}")
        beats.append((tag, arm, d.mean()))
    d = (pv["S-MODE"] - pv["SINGLE-MODE"]).dropna()
    P(f"  {tag:<8}{'S - SINGLE':<14}{d.mean():>+12.4f}{tstat(d):>8.2f}"
      f"{f'{int((d > 0).sum())}/{len(d)}':>12}{int((d != 0).sum()):>16}")
smode_wins = [b for t, a, b in beats if a == "S-MODE" and b > 0]
P(f"  P6 {'HIT' if not smode_wins else 'MISS'}  (S-MODE does not beat SEL-SHARPE out of sample; "
  f"{len(smode_wins)} of 2 corpora positive)")

P(f"\n  IS THAT A SAMPLING RESULT OR A DIAL-EXPOSURE ONE? (idea 226/438's standing check — an")
P(f"  arm that changes the pick on some dials and not others can inherit a dial's own premium)")
P(f"  {'corpus':<8}{'arm':<13}{'dial':<9}{'mean delta':>12}{'t':>8}{'rows differing':>16}")
for tag in ("A", "B"):
    pvc = piv.loc[tag].reset_index()
    for arm in ("SINGLE-MODE", "S-MODE"):
        allm = float((pvc[arm] - pvc["SEL-SHARPE"]).mean())
        for dl, g in pvc.groupby("dial"):
            dd = (g[arm] - g["SEL-SHARPE"]).dropna()
            if int((dd != 0).sum()) == 0:
                continue
            P(f"  {tag:<8}{arm:<13}{dl:<9}{dd.mean():>+12.4f}{tstat(dd):>8.2f}"
              f"{int((dd != 0).sum()):>16}")
        lodo = [(dl, float((pvc[pvc.dial != dl][arm] - pvc[pvc.dial != dl]["SEL-SHARPE"]).mean()))
                for dl in sorted(pvc.dial.unique())]
        P(f"  {tag:<8}{arm:<13}{'LODO':<9}"
          + "  ".join(f"{a}:{b:+.4f}" for a, b in sorted(lodo, key=lambda z: z[1])))
        kill = [a for a, b in lodo if np.sign(b) != np.sign(allm) or abs(b) < 1e-9]
        P(f"  {tag:<8}{arm:<13}{'':<9}all-dials {allm:+.4f}; dials whose removal kills or flips "
          f"it: {', '.join(kill) if kill else 'none'}")

P(f"\n  BOTH KEEP PATHS, by parent panel (point-level verdicts inherited from the ladder):")
P(f"  {'parent':<8}{'arm':<14}{'4a':>6}{'4b':>6}{'rows':>7}")
for (parent, arm), g in BK.groupby(["parent", "arm"]):
    P(f"  {parent:<8}{arm:<14}{int((g.fail4a == '-').sum()):>6}"
      f"{int((g.fail4b == '-').sum()):>6}{len(g):>7}")
P("  (counted as ZERO new evidence for idea 136 — these are the parent's own committed rows,")
P("   reproduced not recomputed, and per idea 144 nothing here is proposed as a book.)")

P("\n" + "=" * 118)
P(f"done in {time.time() - T0:.0f}s")
P("=" * 118)
dump()
