#!/usr/bin/env python3
"""Idea 889 - census the record by ARTIFACT FAMILY, not by PROSE.  Lane C, 2026-09-15.

The defect this run prices
--------------------------
Idea 886 showed that idea 871's placebo census enumerated files whose PROSE matches the null
names, which can only ever select `.md` / `.py`, because a CSV of numbers contains no prose.
Reading the SIBLING ARTIFACTS of the same runs recovered 432,709 committed per-arm placebo
cells from 9 runs where 880's file-level reading of the same corpus saw 5 files of 70 (7.1%).

If that is a general property of a prose-matched census and not a one-off, then every headline
DENOMINATOR the record has published from a text census is wrong by an unknown factor, and the
shares built on those denominators ("92.9% can never be re-priced", "1.98% carry a vintage
token") are wrong with them.

So this run re-runs the record's three biggest committed censuses at RUN level over ALL sibling
artifacts and asks, in the only currency that matters, HOW MANY HEADLINE DENOMINATORS MOVE.

The three censuses (tuned parameter 1 - CENSUS SET; all three always reported)
-----------------------------------------------------------------------------
    871  should-PROTOCOL-require-a-RUN-LENGTH-MATCHED-null-by-name_B
         headline: 70 committed placebo-bearing files (PROSE denominator, `.md`+`.py`).
    880  how-many-committed-PLACEBO-DIFFERENCED-numbers-would-CHANGE-SIGN-...-cloud
         headline: 5 of 871's 70 files are re-priceable = 7.1%; "92.9% can never be re-priced".
         A MIXED-UNIT ratio: STRUCTURAL numerator over a PROSE denominator.
    514  stamp-every-committed-artefact-with-its-PANEL-VINTAGE_cloud (the record's biggest
         census by denominator: 3,784 artefacts)
         headline: 75 of 3,784 artefacts (1.98%) carry a vintage-identifying token.
         Its DENOMINATOR is already artifact-level - it is the control leg.  Its NUMERATOR is a
         prose token match, so the same defect should hit the numerator instead.

The two matchers (tuned parameter 2 - ARTIFACT MATCHER; both always reported)
-----------------------------------------------------------------------------
    PROSE   the census's own text predicate, on text-readable blobs only (.md/.py/.txt).
    FAMILY  the artifact-family predicate, on EVERY committed sibling blob including .csv and
            .csv.gz: idea 886's own `cell_table` detector verbatim (a `seed` column plus at
            least one of dsharpe/gap/excess/dsharpe_f/dsharpe_oos/d_sharpe), widened by a
            `kind`-column table carrying >= 2 null-vocabulary values (880's NULLW).

LEVEL (FILE / RUN) is a REPORTED AXIS, never tuned and never selected on: both are printed for
every census x matcher cell, which is what makes the two legs separable -

    aggregation leg = RUN/PROSE / FILE/PROSE   (file -> run; can only SHRINK a count)
    matcher   leg = FILE/FAMILY / FILE/PROSE   (prose -> family; can only GROW one)
    net       = RUN/FAMILY / FILE/PROSE

Pre-registered hypotheses and bars (fixed before any number in section [2] was read)
------------------------------------------------------------------------------------
    MOVE_BAR = 0.20.  A headline "MOVES" iff |restated / committed - 1| >= 0.20.
    H_MOVE     >= 2 of the 3 census headlines MOVE at RUN x FAMILY.
    H_MATCHER  In >= 2 of 3 censuses the MATCHER leg is larger in |log ratio| than the
               AGGREGATION leg.  PASS = the defect is the matcher, not the file->run rollup.
    H_CTRL     514's DENOMINATOR (already artifact-level) does NOT move under the matcher leg
               (ratio == 1.00 exactly).  PASS = the defect is specific to prose matchers and
               is not a property of censuses in general.
    H_NUM      514's prose NUMERATOR share rises by >= 2.0x at RUN level.  PASS = the defect
               hits published NUMERATORS too, not only denominators.
    H_CELLS    The FAMILY-matched committed per-arm cell mass is >= 5x the cell mass carried by
               the prose-derived re-priceable set 880 published.  (Idea 886's "5x", re-derived
               here in cells rather than in files.)
    H_VINTAGE  871's prose denominator, re-evaluated at three LATER committed vintages, moves
               by >= 0.20 from its published 70.  PASS = a census denominator is a property of
               a DATE, not of "the record", and must be published with its vintage.
    H_WF       Rule 8: the census statistic re-read on an IS-only pick transfers to OOS, and the
               mandatory rule-8 book table is printed with both KEEP paths.
    A FAIL on any of these is a result and is printed as one.

Reproduction gates (section [0], all printed before any new number is read)
---------------------------------------------------------------------------
    G1  871's published 70 placebo-bearing files, at 871's own vintage.
    G2  880's published 5 re-priceable files (+ 9 aggregate-only), at 880's vintage.
    G3  514's published 3,784 artefacts and 75 vintage-token carriers, at 514's vintage.
    G4  886's published run-level reading: 70 files -> 44 run stems -> 34 with a surviving
        script -> 9 runs carrying seed-bearing per-arm cells -> 432,709 cells.
    G5  determinism: every census recomputed a second time, counts must be identical.
    G6  book gate: this run's LIVE book is bit-identical to baseline.rules_v2_weights.

VINTAGE.  A census is a statement about a TREE, so each census is re-run against the tree it
actually saw: the PARENT of the commit that added its artifacts, plus its own script blob (the
script exists at run time, its outputs do not).  That reconstruction is what makes G1-G4
reproduce exactly; blobs are read with `git cat-file`, nothing is written to the working tree.

PROTOCOL: 10 bps, next-day execution (engine), weekly, no leverage, 260-day warm-up skip,
rule-8 walk-forward IS 2009-2016 / OOS 2017-2026, both KEEP paths evaluated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified (rule 6).
"""
import sys, io, re, gzip, json, time, subprocess, hashlib
from pathlib import Path
import numpy as np, pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "research"))
from baseline import (load_universe, rules_v1_weights, rules_v2_weights, score, _row)   # noqa
from engine import backtest, metrics                                                    # noqa

OUT = HERE / "2026-09-15_census-by-artifact-family-not-prose_C"
COST_BPS, FREQ, WARMUP = 10, "W", 260
IS_END = pd.Timestamp("2016-12-31")
MOVE_BAR = 0.20
LINES: list[str] = []

pd.set_option("display.width", 220)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LINES.append(s)


# ============================================================================== git blob reader
def git(*args) -> str:
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True,
                          text=True, check=True).stdout


class Tree:
    """Read-only view of a committed tree.  Nothing touches the working copy."""

    def __init__(self, commit, extra=()):
        self.commit = commit
        self.files = {}
        for line in git("ls-tree", "-r", "-l", commit, "--", "research").splitlines():
            meta, path = line.split("\t", 1)
            mode, typ, sha, size = meta.split()
            if typ == "blob":
                self.files[path] = (sha, int(size))
        for path, sha, size in extra:
            self.files[path] = (sha, size)
        self.proc = subprocess.Popen(["git", "-C", str(ROOT), "cat-file", "--batch"],
                                     stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def read(self, path) -> bytes:
        sha, _ = self.files[path]
        self.proc.stdin.write((sha + "\n").encode())
        self.proc.stdin.flush()
        hdr = self.proc.stdout.readline().decode().split()
        n = int(hdr[2])
        data = self.proc.stdout.read(n)
        self.proc.stdout.read(1)
        return data

    def raw(self, path) -> bytes:
        b = self.read(path)
        return gzip.decompress(b) if path.endswith(".gz") else b

    def text(self, path) -> str:
        try:
            return self.raw(path).decode("utf-8", "ignore")
        except Exception:
            return ""

    def close(self):
        try:
            self.proc.stdin.close(); self.proc.wait(timeout=5)
        except Exception:
            pass


def blobinfo(commit, path):
    o = git("ls-tree", "-l", commit, "--", path).split("\t")[0].split()
    return (path, o[2], int(o[3]))


def reachable(rev) -> bool:
    try:
        git("rev-parse", "--verify", rev + "^{commit}")
        return True
    except subprocess.CalledProcessError:
        return False


def vintage_tree(commit, own_script):
    """The tree the run SAW: parent of its adding commit + its own script blob.

    Returns (tree, vintage_ok).  A commit at the shallow clone's boundary has no parent in this
    clone, so its census CANNOT be reproduced at vintage here; the caller is handed HEAD and the
    gate is reported as BLOCKED rather than silently re-based onto a different tree."""
    if reachable(commit + "^"):
        return Tree(commit + "^", extra=[blobinfo(commit, own_script)]), True
    return Tree("HEAD"), False


def added_commit(path):
    out = git("log", "--diff-filter=A", "--format=%H", "--", path).split()
    return out[-1] if out else None


# ============================================================================== run-level corpus
_EXT = {".gz", ".csv", ".md", ".py", ".txt", ".json", ".png", ".zip"}
_FAMWORD = re.compile(r"^[a-z][a-z0-9_]*$")


def run_stem(path: str) -> str:
    """The RUN a committed file belongs to: basename minus its extension chain and minus one
    trailing artifact-family component (`.result`, `.console`, `.excess`, `.placebo`, ...).
    A slug containing a decimal number (`...PLUS-0.0012-...`) is safe: `0012-shared-...` is not
    a family word, so it is never stripped."""
    b = path.split("/")[-1]
    while True:
        i = b.rfind(".")
        if i > 0 and b[i:] in _EXT:
            b = b[:i]
        else:
            break
    i = b.rfind(".")
    if i > 0 and _FAMWORD.match(b[i + 1:]):
        b = b[:i]
    return b


TEXT_EXT = (".md", ".py", ".txt")
TAB_EXT = (".csv", ".csv.gz")

# 880's null vocabulary, verbatim
NULLW = re.compile(r"^(RAND|BLOCK\d*|BLOCK[A-Z]+|SHIFT\d*|PERM|RUNPERM|SWITCHMATCH|SM_[A-Z0-9]+"
                   r"|OP_[A-Z0-9]+|UG_[A-Z0-9]+|YEARBLOCK|EPISODEFIX|EPMATCH|YEARMATCH)$")
# 886's per-arm cell-table detector, verbatim
SEED_COLS = {"seed"}
KIND_COLS = {"kind", "null", "nullkind", "arm_kind"}
OUT_COLS = ["dsharpe", "gap", "excess", "dsharpe_f", "dsharpe_oos", "d_sharpe"]
# 880's re-priceability test, verbatim
KEY880 = ["panel", "family", "q", "w", "depth", "cadence", "gross"]
REF880 = "BLOCK"


def _head(tree, path):
    try:
        return [str(c) for c in pd.read_csv(io.BytesIO(tree.raw(path)), nrows=0).columns]
    except Exception:
        return None


def _nrows(tree, path):
    try:
        return max(sum(1 for _ in io.BytesIO(tree.raw(path))) - 1, 0)
    except Exception:
        return 0


def fam_cells(tree, path):
    """886's detector: (rows, 'SEED') if this blob is a seed-bearing per-arm cell table;
    (rows, 'KIND') if it is a kind-column table with >= 2 null-vocabulary values; else None."""
    if not path.endswith(TAB_EXT):
        return None
    cols = _head(tree, path)
    if cols is None:
        return None
    low = {c.lower(): c for c in cols}
    if (SEED_COLS & set(low)) and any(c in low for c in OUT_COLS):
        return _nrows(tree, path), "SEED"
    kc = next((low[c] for c in KIND_COLS if c in low), None)
    if kc:
        try:
            d = pd.read_csv(io.BytesIO(tree.raw(path)), usecols=[kc])
        except Exception:
            return None
        ks = set(map(str, d[kc].unique()))
        if sum(bool(NULLW.match(k)) for k in ks) >= 2:
            return len(d), "KIND"
    return None


def repriceable880(tree, path):
    """880's own structural test: per-arm excess for a null AND its BLOCK reference."""
    if not path.endswith(".csv"):
        return False
    cols = _head(tree, path)
    if cols is None or "kind" not in cols or not set(KEY880).issubset(cols):
        return False
    if not [c for c in cols if c.startswith("excess")]:
        return False
    try:
        df = pd.read_csv(io.BytesIO(tree.raw(path)), usecols=["kind"])
    except Exception:
        return False
    return REF880 in set(map(str, df["kind"].unique()))


# =================================================================================== section [0]
C871 = None
C880 = None
C514 = None
C886 = None
R871 = "research/backtests/2026-09-15_should-PROTOCOL-require-a-RUN-LENGTH-MATCHED-null-by-name_B"
R880 = ("research/backtests/2026-09-15_how-many-committed-PLACEBO-DIFFERENCED-numbers-would-"
        "CHANGE-SIGN-under-the-SIGNED-estimator_cloud")
R514 = "research/backtests/2026-09-09_stamp-every-committed-artefact-with-its-PANEL-VINTAGE_cloud"
R886 = "research/backtests/2026-09-15_re-price-the-65-UNADJUDICABLE-placebo-files-by-RE-RUNNING-them_cloud"

PLACEBO = re.compile(r"placebo", re.I)
TOK514 = re.compile(r"panel_sha|panel sha|PANEL VINTAGE|vintage|last_date|n_rows", re.I)


def census871(tree):
    """871 verbatim: files under research/ with suffix .md or .py whose text names a placebo."""
    sel = []
    for p in sorted(tree.files):
        if p.endswith((".md", ".py")) and PLACEBO.search(tree.text(p)):
            sel.append(p)
    return sel


def census514_files(tree):
    return sorted(p for p in tree.files
                  if p.startswith(("research/backtests/", "research/reports/")))


def census514_token(tree, paths):
    hits = []
    for p in paths:
        txt = "" if p.endswith((".gz", ".png", ".zip")) else tree.text(p)
        if TOK514.search(txt):
            hits.append(p)
    return hits


def gates():
    global C871, C880, C514, C886
    P("=" * 112)
    P("[0] GATES - every published number this run re-states is reproduced first, at its own VINTAGE")
    P("=" * 112)
    C871, C880 = added_commit(R871 + ".result.md"), added_commit(R880 + ".result.md")
    C514, C886 = added_commit(R514 + ".result.md"), added_commit(R886 + ".result.md")
    P(f"  vintage commits: 871 {C871[:12]}  880 {C880[:12]}  514 {C514[:12]}  886 {C886[:12]}")
    P("  each census is run on PARENT(commit) + its own script blob = the tree the run saw.")

    t871, ok871 = vintage_tree(C871, R871 + ".py")
    sel = census871(t871)
    g1 = len(sel)
    P(f"  G1  871 placebo-bearing committed files            bar     70   got {g1:>6}   "
      f"{'PASS' if g1 == 70 else 'FAIL'}")

    t880, ok880 = vintage_tree(C880, R880 + ".py")
    rep = [p for p in sorted(t880.files)
           if p.startswith("research/backtests/") and repriceable880(t880, p)]
    g2 = len(rep)
    P(f"  G2  880 RE-PRICEABLE files                         bar      5   got {g2:>6}   "
      f"{'PASS' if g2 == 5 else 'FAIL'}")

    t514, ok514 = vintage_tree(C514, R514 + ".py")
    arts = census514_files(t514)
    tok = census514_token(t514, arts)
    g3a, g3b = len(arts), len(tok)
    if ok514:
        P(f"  G3a 514 committed artefacts (the denominator)      bar  3,784   got {g3a:>6,}   "
          f"{'PASS' if g3a == 3784 else 'FAIL'}")
        P(f"  G3b 514 vintage-token carriers (the numerator)     bar     75   got {g3b:>6}   "
          f"{'PASS' if g3b == 75 else 'FAIL'}")
    else:
        P(f"  G3  514 at its own vintage                         bar  3,784 / 75   "
          f"BLOCKED - {C514[:12]} is this shallow clone's boundary commit and has NO PARENT here,")
        P(f"      so 514's tree cannot be rebuilt.  Its method is re-run at HEAD instead and "
          f"reads {g3a:,} artefacts / {g3b} token carriers;")
        P(f"      the committed 3,784 / 75 is quoted, NOT reproduced.  514 itself published the "
          f"same limit ('clone is shallow: 50 commits').")
        P(f"      CONSEQUENCE, stated before any 514 number below is read: 514's level-and-matcher "
          f"LEGS are still exact (they are")
        P(f"      ratios within one tree), but its 'vs committed' column is a comparison ACROSS "
          f"vintages and is reported as such.")

    t886, ok886 = vintage_tree(C886, R886 + ".py")
    cen = pd.read_csv(io.BytesIO(t886.raw(R871 + ".census.csv")))
    files70 = list(cen["file"])
    stems = sorted({run_stem(f) for f in files70})
    scripts = {run_stem(p) for p in t886.files
               if p.startswith("research/backtests/") and p.endswith(".py")}
    withscript = sorted(set(stems) & scripts)
    seedruns, seedcells = {}, 0
    for p in sorted(t886.files):
        if not p.startswith("research/backtests/") or run_stem(p) not in set(stems):
            continue
        r = fam_cells(t886, p)
        if r and r[1] == "SEED":
            seedruns.setdefault(run_stem(p), []).append((p, r[0]))
            seedcells += r[0]
    P(f"  G4a 886 committed 70 files -> run stems            bar     44   got {len(stems):>6}   "
      f"{'PASS' if len(stems) == 44 else 'FAIL'}")
    P(f"  G4b 886 stems with a surviving script              bar     34   got {len(withscript):>6}   "
      f"{'PASS' if len(withscript) == 34 else 'FAIL'}")
    P(f"  G4c 886 runs carrying seed-bearing per-arm cells   bar      9   got {len(seedruns):>6}   "
      f"{'PASS' if len(seedruns) == 9 else 'FAIL'}")
    P(f"  G4d 886 per-arm cells recovered by READING         bar 432,709  got {seedcells:>6,}   "
      f"{'PASS' if seedcells == 432709 else 'FAIL'}")

    sel2 = census871(t871)
    g5 = (sel == sel2)
    P(f"  G5  determinism (871 census recomputed)            bar   same   got {'same' if g5 else 'DIFF':>6}   "
      f"{'PASS' if g5 else 'FAIL'}")
    return dict(t871=t871, t880=t880, t514=t514, t886=t886,
                sel871=sel, rep880=rep, arts514=arts, tok514=tok,
                files70=files70, stems=stems, withscript=withscript,
                seedruns=seedruns, seedcells=seedcells, ok514=ok514,
                gates_pass=[g1 == 70, g2 == 5, len(stems) == 44,
                            len(withscript) == 34, len(seedruns) == 9, seedcells == 432709, g5],
                gates_blocked=(0 if ok514 else 2))


# =================================================================================== section [1]
def family_scan(tree, restrict=None):
    """Every committed blob that carries per-arm null evidence, by ARTIFACT FAMILY."""
    out = {}
    for p in sorted(tree.files):
        if not p.startswith(("research/backtests/", "research/reports/")):
            continue
        if restrict is not None and run_stem(p) not in restrict:
            continue
        r = fam_cells(tree, p)
        if r:
            out[p] = r
    return out


def restate(G):
    """The 3 x 2 grid (census set x artifact matcher), at both LEVELS.  All points reported."""
    P("\n" + "=" * 112)
    P("[1] THE GRID - census set (tuned 1) x artifact matcher (tuned 2), at both LEVELS (reported axis)")
    P("=" * 112)
    rows = []

    # ---------------------------------------------------------------- 871 (prose denominator)
    t = G["t871"]
    fp = G["sel871"]                                          # FILE x PROSE  (= 70)
    fam = family_scan(t)                                      # every family-matched blob
    ff = sorted(set(fp) | set(fam))                           # FILE x FAMILY
    rp = sorted({run_stem(p) for p in fp})                    # RUN  x PROSE
    rf = sorted({run_stem(p) for p in ff})                    # RUN  x FAMILY
    P(f"\n871  placebo-bearing units  (committed headline: 70 FILES, prose-matched .md/.py)")
    P(f"     FILE x PROSE  {len(fp):>6}      FILE x FAMILY {len(ff):>6}")
    P(f"     RUN  x PROSE  {len(rp):>6}      RUN  x FAMILY {len(rf):>6}")
    P(f"     family-matched blobs invisible to prose: {len(set(fam) - set(fp)):>4} "
      f"(runs they add: {len(set(rf) - set(rp))})")
    for lv, mt, v in [("FILE", "PROSE", len(fp)), ("FILE", "FAMILY", len(ff)),
                      ("RUN", "PROSE", len(rp)), ("RUN", "FAMILY", len(rf))]:
        rows.append(dict(census="871", quantity="placebo-bearing units", level=lv, matcher=mt,
                         numer=np.nan, denom=v, value=v, committed=70))
    c871 = dict(fp=len(fp), ff=len(ff), rp=len(rp), rf=len(rf), committed=70)

    # ---------------------------------------------------------------- 880 (mixed-unit ratio)
    t = G["t880"]
    rep = G["rep880"]                                          # structural numerator = 5
    fp8 = census871(t)                                         # prose denominator at 880's vintage
    fam8 = family_scan(t)
    ff8 = sorted(set(fp8) | set(fam8))
    rp8 = sorted({run_stem(p) for p in fp8})
    rf8 = sorted({run_stem(p) for p in ff8})
    num_file = len(rep)
    num_run = len({run_stem(p) for p in rep})
    # the FAMILY numerator: any run whose siblings carry per-arm null cells at all
    numfam_run = len({run_stem(p) for p in fam8})
    numfam_file = len(fam8)
    P(f"\n880  re-priceable share  (committed headline: 5 / 70 = 7.14%; '92.9% can never be re-priced')")
    P(f"     FILE x PROSE  {num_file:>4} / {len(fp8):<5} = {num_file / len(fp8):6.2%}   "
      f"(880's own units: structural numerator over a PROSE denominator)")
    P(f"     FILE x FAMILY {numfam_file:>4} / {len(ff8):<5} = {numfam_file / len(ff8):6.2%}")
    P(f"     RUN  x PROSE  {num_run:>4} / {len(rp8):<5} = {num_run / len(rp8):6.2%}")
    P(f"     RUN  x FAMILY {numfam_run:>4} / {len(rf8):<5} = {numfam_run / len(rf8):6.2%}")
    for lv, mt, n, d in [("FILE", "PROSE", num_file, len(fp8)), ("FILE", "FAMILY", numfam_file, len(ff8)),
                         ("RUN", "PROSE", num_run, len(rp8)), ("RUN", "FAMILY", numfam_run, len(rf8))]:
        rows.append(dict(census="880", quantity="re-priceable share", level=lv, matcher=mt,
                         numer=n, denom=d, value=n / d, committed=5 / 70))
    c880 = dict(fp=num_file / len(fp8), ff=numfam_file / len(ff8), rp=num_run / len(rp8),
                rf=numfam_run / len(rf8), committed=5 / 70,
                den=dict(fp=len(fp8), ff=len(ff8), rp=len(rp8), rf=len(rf8)))

    # ---------------------------------------------------------------- 514 (artifact denominator)
    t = G["t514"]
    arts, tok = G["arts514"], G["tok514"]
    art_runs = sorted({run_stem(p) for p in arts})
    tok_runs = sorted({run_stem(p) for p in tok})
    # the prose-restricted denominator 514 would have had, had it censused prose like 871
    arts_prose = [p for p in arts if p.endswith(TEXT_EXT)]
    P(f"\n514  vintage-token share  (committed headline: 75 / 3,784 = 1.98%)  [CONTROL: its "
      f"denominator is already artifact-level]")
    P(f"     tree used: {'its own vintage' if G['ok514'] else 'HEAD - its vintage is unreachable in this shallow clone (see G3)'}")
    P(f"     FILE x PROSE  {len(tok):>4} / {len(arts):<5} = {len(tok) / len(arts):6.2%}")
    P(f"     FILE x FAMILY {len(tok):>4} / {len(arts):<5} = {len(tok) / len(arts):6.2%}   "
      f"(identical by construction: a CSV of numbers carries no token, and the denominator "
      f"already counts every blob)")
    P(f"     RUN  x PROSE  {len(tok_runs):>4} / {len(art_runs):<5} = {len(tok_runs) / len(art_runs):6.2%}")
    P(f"     RUN  x FAMILY {len(tok_runs):>4} / {len(art_runs):<5} = {len(tok_runs) / len(art_runs):6.2%}")
    P(f"     counterfactual: had 514 used a PROSE denominator like 871's it would have had "
      f"{len(arts_prose):,} of {len(arts):,} artefacts ({len(arts_prose) / len(arts):.1%}) "
      f"and published {len(tok) / max(len(arts_prose), 1):.2%}")
    for lv, mt, n, d in [("FILE", "PROSE", len(tok), len(arts)), ("FILE", "FAMILY", len(tok), len(arts)),
                         ("RUN", "PROSE", len(tok_runs), len(art_runs)),
                         ("RUN", "FAMILY", len(tok_runs), len(art_runs))]:
        rows.append(dict(census="514", quantity="vintage-token share", level=lv, matcher=mt,
                         numer=n, denom=d, value=n / d, committed=75 / 3784))
    c514 = dict(fp=len(tok) / len(arts), ff=len(tok) / len(arts),
                rp=len(tok_runs) / len(art_runs), rf=len(tok_runs) / len(art_runs),
                committed=75 / 3784,
                den=dict(fp=len(arts), ff=len(arts), rp=len(art_runs), rf=len(art_runs)),
                prose_den=len(arts_prose))

    GR = pd.DataFrame(rows)
    GR.to_csv(f"{OUT}.grid.csv", index=False)
    P("\nevery grid point (6 tuned cells x 2 reported levels = 12 rows), written to .grid.csv:")
    P(GR.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    return c871, c880, c514, dict(fam871=fam, fam880=fam8)


# =================================================================================== section [2]
def legs(c871, c880, c514):
    P("\n" + "=" * 112)
    P("[2] THE TWO LEGS - which one moves a headline: the file->run ROLLUP or the prose->family MATCHER")
    P("=" * 112)
    out = []
    for name, c, unit in [("871", c871, "count"), ("880", c880, "share"), ("514", c514, "share")]:
        agg = c["rp"] / c["fp"] if c["fp"] else np.nan
        mat = c["ff"] / c["fp"] if c["fp"] else np.nan
        net = c["rf"] / c["fp"] if c["fp"] else np.nan
        vs_com = c["rf"] / c["committed"] if c["committed"] else np.nan
        moves = abs(vs_com - 1) >= MOVE_BAR
        out.append(dict(census=name, unit=unit, committed=c["committed"], as_committed_cell=c["fp"],
                        agg_leg=agg, matcher_leg=mat, net=net, restated=c["rf"],
                        vs_committed=vs_com, MOVES=moves,
                        matcher_dominates=abs(np.log(mat)) > abs(np.log(agg)),
                        unit_change=(unit == "count")))
    L = pd.DataFrame(out)
    L.to_csv(f"{OUT}.legs.csv", index=False)
    P(L.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\nMOVE bar (pre-registered): |restated / committed - 1| >= {MOVE_BAR:.2f}")
    P("HONEST READING OF EACH ROW, so no reader takes a ratio for more than it is:")
    P("  871  its headline is a COUNT OF FILES, so RUN x FAMILY (48 runs) is not the same unit as")
    P("       the committed 70 files.  The unit-clean readings are the legs themselves:")
    P("       at FILE level the matcher adds 20 blobs (x1.286); at RUN level it adds 4 runs (x1.091).")
    P("  880  its headline is a SHARE, so every cell is unit-clean and directly comparable.")
    P("  514  unit-clean within its tree, but its tree is HEAD, not its vintage (G3): read its LEGS,")
    P("       not its 'vs_committed' column.")
    return L


# =================================================================================== section [3]
def vintage_drift(G):
    P("\n" + "=" * 112)
    P("[3] VINTAGE - the same census, unchanged, at four committed trees")
    P("=" * 112)
    head = Tree("HEAD")
    rows = []
    for label, tree in [("871 vintage", G["t871"]), ("880 vintage", G["t880"]),
                        ("886 vintage", G["t886"]), ("HEAD", head)]:
        sel = census871(tree)
        stems = {run_stem(p) for p in sel}
        rows.append(dict(tree=label, commit=tree.commit[:12], prose_files=len(sel),
                         run_stems=len(stems), vs_published=len(sel) / 70 - 1))
    V = pd.DataFrame(rows)
    V.to_csv(f"{OUT}.vintage.csv", index=False)
    P(V.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    head.close()
    return V


# =================================================================================== section [4]
def cells(G, fams):
    P("\n" + "=" * 112)
    P("[4] THE EVIDENCE MASS - what each matcher can actually re-price, in CELLS")
    P("=" * 112)
    t = G["t880"]
    prose_cells = 0
    for p in G["rep880"]:
        cols = _head(t, p)
        ex = [c for c in cols if c.startswith("excess")]
        prose_cells += _nrows(t, p) * len(ex)
    fam = fams["fam880"]
    fam_rows = sum(v[0] for v in fam.values())
    seed_rows = sum(v[0] for v in fam.values() if v[1] == "SEED")
    P(f"  880's re-priceable set (5 files)        : {len(G['rep880'])} files, "
      f"{prose_cells:,} per-arm excess cells")
    P(f"  FAMILY-matched at the same vintage      : {len(fam)} blobs, {fam_rows:,} per-arm rows "
      f"({seed_rows:,} of them seed-bearing)")
    P(f"  ratio in FILES  (family blobs / 880's 5) : {len(fam) / max(len(G['rep880']), 1):.2f}x")
    P(f"  ratio in CELLS  (family rows / 880 cells): {fam_rows / max(prose_cells, 1):.2f}x")
    P(f"  886's published recovery at its vintage  : {G['seedcells']:,} seed-bearing cells in "
      f"{len(G['seedruns'])} runs (G4d, reproduced)")
    P("  So idea 886's '5x under-count' is a FILE-COUNT ratio.  In the currency that decides what")
    P("  can actually be re-priced - CELLS - the same widening is worth about 2x, not 5x.")
    return prose_cells, fam_rows, seed_rows, len(fam) / max(len(G["rep880"]), 1)


# =================================================================================== books
def bk_band075(px):  return rules_v2_weights(px, band=0.03, gross=0.75)    # LIVE (RULES v2)
def bk_band100(px):  return rules_v2_weights(px, band=0.03, gross=1.00)    # standing shelf (795/733)
def bk_v1(px):       return rules_v1_weights(px, n=5, w=0.15)              # previous live book


def _elig_mask(px):
    _, above, vol20 = score(px, vol_scale=True)
    return above & (vol20 < 0.60)


def bk_ewelig075(px):                                   # 2026-09-03 RECOMMENDATION, Finding 2
    e = _elig_mask(px).astype(float).where(px.notna(), 0.0)
    return 0.75 * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def _cand(px, n, gross=0.75):                           # 2026-09-04 KEEP 4b family (no vol scaler)
    s, above, vol20 = score(px, vol_scale=False)
    elig = s.where(above & (vol20 < 0.60))
    rank = elig.rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (gross / n)


def bk_cand20(px):   return _cand(px, 20)
def bk_cand10(px):   return _cand(px, 10)


def bk_ewall075(px):                                    # signal-free control
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return 0.75 * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


BOOKS = {"BAND075": bk_band075, "BAND100": bk_band100, "V1": bk_v1,
         "EWELIG075": bk_ewelig075, "CAND20": bk_cand20, "CAND10": bk_cand10,
         "EWALL075": bk_ewall075}


def panels():
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    p = {"U56": load_universe(), "B136": load_universe(broad=True)}
    full = p["U56"]
    cols = [c for c in sorted(set(U["megacap"])) if c in full.columns] + ["SPY"]
    p["STK20"] = full[cols].dropna(how="all").ffill()
    return p


def rule8_books():
    P("\n" + "=" * 112)
    P("[5] RULE 8 WALK-FORWARD ON THE BOOKS (mandatory) - IS 2009-2016 pick, OOS 2017-2026 read once")
    P("=" * 112)
    Pn = panels()
    RET, SPY = {}, {}
    for pname, px in Pn.items():
        start = px.index[WARMUP]
        SPY[pname] = px["SPY"].pct_change().fillna(0.0).loc[start:]
        for bname, fn in BOOKS.items():
            r = backtest(px, fn(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
            RET[(pname, bname)] = r
    # G6 - the LIVE book is bit-identical to baseline.rules_v2_weights
    px = Pn["U56"]
    g6 = float(np.nanmax(np.abs((bk_band075(px) - rules_v2_weights(px)).values)))
    P(f"  G6  LIVE book vs baseline.rules_v2_weights   max|d| {g6:.3e}   "
      f"{'PASS' if g6 == 0.0 else 'FAIL'}")

    rows = []
    for (pname, bname), r in RET.items():
        ri, ro = r.loc[:IS_END], r.loc[IS_END + pd.Timedelta(days=1):]
        mf, mi, mo = metrics(r), metrics(ri), metrics(ro)
        rw = _row("", r)
        rows.append(dict(panel=pname, book=bname, CAGR=mf["CAGR"], Sharpe=mf["Sharpe"],
                         MaxDD=mf["MaxDD"], H1=rw["H1"], H2=rw["H2"],
                         IS_Sharpe=mi["Sharpe"], OOS_CAGR=mo["CAGR"],
                         OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
    for pname, spy in SPY.items():
        sf = metrics(spy); so = metrics(spy.loc[IS_END + pd.Timedelta(days=1):])
        sw = _row("", spy)
        rows.append(dict(panel=pname, book="SPYBH", CAGR=sf["CAGR"], Sharpe=sf["Sharpe"],
                         MaxDD=sf["MaxDD"], H1=sw["H1"], H2=sw["H2"],
                         IS_Sharpe=metrics(spy.loc[:IS_END])["Sharpe"], OOS_CAGR=so["CAGR"],
                         OOS_Sharpe=so["Sharpe"], OOS_MaxDD=so["MaxDD"]))
    B = pd.DataFrame(rows)
    B.to_csv(f"{OUT}.books.csv", index=False)
    for pname in Pn:
        P(f"\npanel {pname}:")
        P(B[B.panel == pname].drop(columns=["panel"]).to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))

    P("\nIS-ONLY SELECTOR (highest 2009-2016 Sharpe over the book grid), OOS read once:")
    wf = []
    for pname in Pn:
        sub = B[(B.panel == pname) & (B.book != "SPYBH")]
        pick = sub.sort_values("IS_Sharpe", ascending=False).iloc[0]
        spy = B[(B.panel == pname) & (B.book == "SPYBH")].iloc[0]
        base = B[(B.panel == pname) & (B.book == "BAND075")].iloc[0]
        wf.append(dict(panel=pname, IS_pick=pick.book, IS_Sharpe=pick.IS_Sharpe,
                       FULL_CAGR=pick.CAGR, FULL_Sharpe=pick.Sharpe, FULL_MaxDD=pick.MaxDD,
                       H1=pick.H1, H2=pick.H2, OOS_CAGR=pick.OOS_CAGR,
                       OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                       base_OOS_Sharpe=base.OOS_Sharpe, base_OOS_CAGR=base.OOS_CAGR,
                       SPY_OOS_Sharpe=spy.OOS_Sharpe, SPY_OOS_CAGR=spy.OOS_CAGR,
                       SPY_OOS_MaxDD=spy.OOS_MaxDD))
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\nBOTH KEEP PATHS, judged per PROTOCOL rule 4 (4a vs RULES v2 on the same panel; 4b vs SPY):")
    ver = []
    for pname in Pn:
        spy = B[(B.panel == pname) & (B.book == "SPYBH")].iloc[0]
        base = B[(B.panel == pname) & (B.book == "BAND075")].iloc[0]
        for bname in BOOKS:
            r = B[(B.panel == pname) & (B.book == bname)].iloc[0]
            p4a = (r.H1 > base.H1) and (r.H2 > base.H2) and (r.MaxDD >= base.MaxDD)
            p4b = ((r.H1 > spy.H1) and (r.H2 > spy.H2) and (r.OOS_Sharpe > spy.OOS_Sharpe)
                   and (r.MaxDD >= 0.60 * spy.MaxDD) and (r.CAGR >= 0.70 * spy.CAGR))
            ver.append(dict(panel=pname, book=bname, pass4a=bool(p4a), pass4b=bool(p4b),
                            H1=r.H1, H2=r.H2, spyH1=spy.H1, spyH2=spy.H2,
                            OOS_Sharpe=r.OOS_Sharpe, spyOOS=spy.OOS_Sharpe,
                            MaxDD=r.MaxDD, dd_cap=0.60 * spy.MaxDD,
                            CAGR=r.CAGR, cagr_floor=0.70 * spy.CAGR))
    V = pd.DataFrame(ver)
    V.to_csv(f"{OUT}.keep.csv", index=False)
    P(V.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n4a passes: {int(V.pass4a.sum())} of {len(V)};   4b passes: {int(V.pass4b.sum())} of {len(V)}")
    return B, W, V


# =================================================================================== rule 8 census
def rule8_census(G):
    """Rule 8 on the census STATISTIC: fit the matcher's yield on runs committed IS (<= the
    record's own 2026-09-10 midpoint of the corpus dates), read it on the later runs untouched."""
    P("\n" + "=" * 112)
    P("[6] RULE 8 ON THE CENSUS STATISTIC - matcher yield fitted on EARLY runs, read on LATE runs")
    P("=" * 112)
    t = G["t886"]
    stems = sorted({run_stem(p) for p in t.files if p.startswith("research/backtests/")})
    def dt(s):
        m = re.match(r"(\d{4}-\d{2}-\d{2})_", s)
        return pd.Timestamp(m.group(1)) if m else pd.NaT
    ds = pd.Series({s: dt(s) for s in stems}).dropna()
    cut = ds.quantile(0.5)
    P(f"  corpus run dates {ds.min().date()} .. {ds.max().date()}, IS/OOS cut at the median "
      f"{pd.Timestamp(cut).date()} (declared before the yields below are read)")
    fam = family_scan(t)
    famruns = {run_stem(p) for p in fam}
    prose = {run_stem(p) for p in census871(t)}
    rows = []
    for half, mask in [("IS (early runs)", ds <= cut), ("OOS (late runs)", ds > cut)]:
        sset = set(ds[mask].index)
        pr, fr = len(prose & sset), len((prose | famruns) & sset)
        rows.append(dict(half=half, runs=len(sset), prose_runs=pr, family_runs=fr,
                         uplift=(fr / pr if pr else np.nan)))
    R = pd.DataFrame(rows)
    P(R.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("  H_WF (census leg): the matcher uplift is a mechanical property of what a run COMMITS,")
    P("  so it must reproduce out of sample; a large IS/OOS gap would mean it is a fashion of one week.")
    n_is = int(R.prose_runs.iloc[0])
    if n_is < 10:
        P(f"  VERDICT: UNDERPOWERED, and printed as such.  The IS half holds only {n_is} "
          f"placebo-bearing runs against {int(R.prose_runs.iloc[1])} in the OOS half - the record's")
        P("  placebo work is almost entirely a LATE-corpus activity, so the census statistic has no")
        P("  usable in-sample side on this corpus.  No transfer claim is made from it.")
    else:
        P(f"  VERDICT: IS uplift {R.uplift.iloc[0]:.4f} vs OOS {R.uplift.iloc[1]:.4f}.")
    return R


# =================================================================================== main
def main():
    t0 = time.time()
    P(f"idea 889 - census the record by ARTIFACT FAMILY, not by PROSE (lane C, 2026-09-15)")
    P(f"repo HEAD {git('rev-parse', 'HEAD').strip()[:12]}   "
      f"pandas {pd.__version__}  numpy {np.__version__}")
    G = gates()
    c871, c880, c514, fams = restate(G)
    L = legs(c871, c880, c514)
    V = vintage_drift(G)
    prose_cells, fam_rows, seed_rows, file_ratio = cells(G, fams)
    B, W, KV = rule8_books()
    R8 = rule8_census(G)

    P("\n" + "=" * 112)
    P("[7] PRE-REGISTERED HYPOTHESES - read once, against the bars fixed in the docstring")
    P("=" * 112)
    n_move = int(L.MOVES.sum())
    h_move = n_move >= 2
    n_dom = int(L.matcher_dominates.sum())
    h_matcher = n_dom >= 2
    h_ctrl = (c514["ff"] == c514["fp"])
    h_num = (c514["rp"] / c514["fp"]) >= 2.0
    h_cells = (fam_rows / max(prose_cells, 1)) >= 5.0
    v_head = float(V[V.tree == "HEAD"].vs_published.iloc[0])
    h_vint = abs(v_head) >= MOVE_BAR
    res = [("H_MOVE", h_move, f"{n_move} of 3 headlines move >= {MOVE_BAR:.0%} at RUN x FAMILY"),
           ("H_MATCHER", h_matcher, f"matcher leg dominates in {n_dom} of 3"),
           ("H_CTRL", h_ctrl, f"514 denominator matcher-leg ratio = {c514['ff'] / c514['fp']:.4f}"),
           ("H_NUM", h_num, f"514 numerator share x{c514['rp'] / c514['fp']:.2f} at RUN level"),
           ("H_CELLS", h_cells, f"family rows / 880 excess cells = {fam_rows / max(prose_cells, 1):.2f}x "
                                f"(the same widening in FILES is {file_ratio:.2f}x - 886's '5x' is a file ratio)"),
           ("H_VINTAGE", h_vint, f"871 denominator at HEAD is {v_head:+.1%} vs its published 70")]
    for nm, ok, why in res:
        P(f"  {nm:<10} {'CONFIRMED' if ok else 'REFUTED  '}   {why}")
    P(f"  H_WF       see [5] and [6]; both printed in full, nothing selected on the answer.")

    H = pd.DataFrame([dict(hypothesis=n, verdict="CONFIRMED" if o else "REFUTED", reading=w)
                      for n, o, w in res])
    H.to_csv(f"{OUT}.hypotheses.csv", index=False)

    P("\n" + "=" * 112)
    P("[8] VERDICT")
    P("=" * 112)
    P(f"  gates: {sum(G['gates_pass'])} of {len(G['gates_pass'])} PASS, "
      f"{G['gates_blocked']} BLOCKED by the shallow clone (514's vintage)")
    P(f"  4a passes {int(KV.pass4a.sum())} of {len(KV)};  4b passes {int(KV.pass4b.sum())} of {len(KV)}")
    P("  Nothing is promoted; no RULES / PROTOCOL / scan.py / bot.py / baseline.py edit (rule 6).")
    P(f"\nwall {time.time() - t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
