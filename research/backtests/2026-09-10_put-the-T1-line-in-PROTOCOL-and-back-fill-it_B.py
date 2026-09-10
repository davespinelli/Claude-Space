#!/usr/bin/env python3
"""QUEUE idea 426 — put-the-T1-line-in-PROTOCOL-and-back-fill-it (lane B, 2026-09-10).

Question (verbatim from QUEUE)
-----------------------------
"idea 197 proposes a one-line, sampling-error-free key certificate
(`ranks(key(px)) == ranks(key(px*diag(c)))`) to replace idea 193's Spearman, which it shows has
false positives AND false negatives.  Draft the PROTOCOL clause, back-fill the certificate over
every key the record can still reconstruct, and report the pass/fail column beside each.
Cheap; max 2 params."

What this run owes the queue, and what it does NOT re-litigate
-------------------------------------------------------------
Idea 433 already priced WHICH instrument the clause should name and answered it: an ORDERED PAIR
(DET, idea 428's degree detector, as the corpus GATE; CERT in its VALUE form at a ONE-RANK-STEP
tolerance as the ADJUDICATOR — 0 false clearances and 0 false rejections on 20 hand-truth keys,
where the RANK certificate idea 426 drafts clears MKTLVL).  That verdict is REPRODUCED here as a
gate, not re-derived.  What 433 did NOT do — and what 426 asks for — is the BACK-FILL: actually
pointing the instrument at the record's own keys and publishing the pass/fail column.  433 could
only bound the coverage from above (55.3% of FILES expose an `fn(px)`-callable), and said so.

So this run delivers three things:
  (A) the CLAUSE, drafted verbatim, report-only (PROTOCOL.md is NOT edited; rule 6, Sunday review);
  (B) the BACK-FILL — every key expression the record can still be made to RUN, certified, with a
      PASS/FAIL column beside each, plus an honest accounting of what could not be reached;
  (C) the PRICE of the clause (PROTOCOL 2/3/4/8): a book whose two tuned parameters are the KEY
      and the tilt, and a rule-8 chooser run WITH and WITHOUT the T1 gate in front of it.  Idea
      195's finding — "rule 8 splits by DATE and cannot see terminal dating; the T1 family must
      run BEFORE rule 8" — is the hypothesis (C) tests directly rather than assumes.

THE HARVEST (this is the new machinery; everything else is reused verbatim)
--------------------------------------------------------------------------
433's coverage bound was low because it looked for functions callable as `fn(px)`.  Most keys in
this record are not functions: they are ASSIGNMENTS inside a run body, referring to locals and to
the enclosing function's parameters.  So the harvester works on the AST at the level of the
assignment, and INLINES:
  * every name assigned EXACTLY ONCE in the enclosing scope (recursively, depth <= 7, cycle-safe);
  * every function parameter that carries a literal default.
A candidate survives iff after inlining its only free names are price-like, volume-like, `np`,
`pd`.  Price-like and volume-like names are then renamed to `px` / `vol`, and the expression is
deduped across the whole corpus by its normalised source.  This lifts the reconstructible set
from 167 raw expressions to 485, of which 112 are keys.

An expression is admitted to the KEY census iff, on a fixed panel slice, it
  (1) evaluates without raising                                  (else UNREACHABLE);
  (2) returns a DataFrame/Series on the panel's own index         (else NOT_PANEL);
  (3) is numeric                                                  (else NOT_NUMERIC);
  (3b) is REPRODUCIBLE — two evaluations on the same px agree bit for bit (else
      NOT_REPRODUCIBLE).  This gate is not decoration: two harvested expressions inline an
      `np.empty_like` allocation filled by a later loop, so they read uninitialised memory and
      answer differently every call.  Without the gate the published PASS/FAIL split moves
      between runs of a seeded certificate (observed: 74/39 -> 72/41);
  (4) is PRICE-BORNE — its value moves under a per-CELL multiplicative perturbation of px
      (else NOT_PRICE_BORNE).  Note the perturbation must be per-cell, NOT a uniform px*k:
      every degree-0 key (i.e. every SAFE key) is invariant to a uniform rescale, so a uniform
      probe silently deletes exactly the keys the census exists to clear.

T1 VERDICT per key = the ordered pair, in 433's order:
    DET (gate)        flags the expression on its degree in the price scale;
    CERT-VALUE (adj.) frac of cells whose value moves under px -> px @ diag(c), c_i > 0 lognormal,
                      compared against ONE RANK STEP (1/n_names) — a derived constant, not a fit;
    CERT-RANK         the same for cross-sectional rankpct, reported beside it because the queue's
                      own draft names the RANK form (433 shows it clears MKTLVL; carried as
                      evidence, not as the verdict).
  PASS iff CERT-VALUE says safe.  DET is reported beside it and every DISAGREEMENT is listed.

WHAT THE CLAUSE DOES NOT CATCH — stated up front, not buried.  T1 is an ADJUSTMENT-CHANNEL test.
It certifies invariance under a per-name positive rescale, which is what truncating an
auto-adjusted panel does.  It is NOT a look-ahead detector: a forward return `px.shift(-21)/px-1`
is homogeneous of degree 0 and PASSES T1 while being pure oracle.  The record contains such a key.
This run reports it rather than letting the clause be quoted as more than it is.

PRE-REGISTERED PREDICTIONS (written before any number below was read; each reported hit/miss)
  P1  The back-fill reaches under 40% of the record's key-bearing assignment sites (the free-
      variable wall, not the instrument, is the binding constraint on a PROTOCOL back-fill).
  P2  At least one T1-FAIL key is carried by >= 5 committed scripts — i.e. the clause is not a
      formality, it has live back-fill consequences in this record.
  P3  At least one key PASSES T1 and is nonetheless look-ahead (the FWD counterexample), so the
      clause must be worded as a NECESSARY, not a sufficient, condition.
  P4  BOOK.  The T1 gate in front of rule 8 does NOT improve OOS Sharpe on the price-free
      comparison (the gate's value is in deleting unimplementable arms, not in earning), and no
      tilt arm clears 4b on either panel.

Design
------
Panels     U56 (research/universe.json, the protocol default) and SMALL439 (sub-$2B, current
           constituents, `max_1d_move >= 1.0` dropped per data/small_meta.csv).
           SURVIVORSHIP: both are CURRENT constituents; SMALL439 doubly so.  No book is proposed
           on either; only same-days, same-book contrasts are read.
Books      EWALL (no trend gate) and MA200 (200d trend gate), gross 0.75 held EXACTLY equal across
           every tilt (rw normalisation) so m moves the cross-section and never the exposure —
           idea 415's warning.  Realised gross is published beside every Sharpe (idea 641).
Cadence    weekly, weights at close t applied t+1 (fast_bt, idea 425's helper verbatim).
Costs      0/5/10/25 bps, ALL reported; PROTOCOL rung 10 bps for verdicts.
Tuned      EXACTLY TWO: the KEY (16, chosen mechanically as the most-used reconstructible
           price-only numeric keys in the record) and the tilt m (7 points incl. the m=0 control).
           Every one of the grid points is written to .book.csv and reported.
Rule 8     (KEY, m) chosen on 2010..2016 by IS Sharpe at 10 bps inside each (panel, book) cell;
           2017..2026 read ONCE against SPY, the m=0 control, RULES v2 and RULES v1.
Both KEEP  4a vs live RULES v2 at the same rung; 4b vs SPY including the rule-8 OOS leg.
CERT axes  sigma = 0.25, B = 6 draws, seed 426 — REPORTED, never selected on.

Outputs: .console.txt .keys.csv .backfill.csv .coverage.csv .census.csv .book.csv .walkforward.csv
"""
import ast
import hashlib
import re
import sys
import tempfile
import time
import warnings
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, load_volume, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask                                 # noqa: E402

STEM = "2026-09-10_put-the-T1-line-in-PROTOCOL-and-back-fill-it_B"
OUT = ROOT / "research" / "backtests"
DET_PARENT = OUT / "2026-09-08_census-the-record-s-other-DOLLAR-floors-and-caps_C.py"
CERT_PARENT = OUT / "2026-09-08_adopt-the-T1-DEGREE-DETECTOR-as-the-PROTOCOL-corpus-gate_cloud.py"

FREQ, GROSS = "W", 0.75
COSTS = [0, 5, 10, 25]
PROTO_COST = 10
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SIGMA, NDRAW, SEED = 0.25, 6, 426
TOL = 1e-9
NKEY_BOOK = 16
MGRID = [-1.0, -0.5, -0.25, 0.0, 0.25, 0.5, 1.0]

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


T0 = time.time()
P("=" * 118)
P("IDEA 426  put-the-T1-line-in-PROTOCOL-and-back-fill-it   (lane B, 2026-09-10)")
P("=" * 118)


# =====================================================================================
# PART 0 — instruments imported VERBATIM from the committed record
# =====================================================================================
def load_det():
    """Extract idea 428's PART 0 detector by its own source markers and exec it, so 428's book
    does not re-run and the object under test is byte-identical to the committed one."""
    src = DET_PARENT.read_text()
    a = src.index("# PART 0 — the absolute-cut detector")
    b = src.index("# engine helpers")
    block = src[a:b]
    block = block[:block.rindex("\n# ")] if "\n# =====" in block[100:] else block   # 433's trim
    ns = {"__name__": "det428", "re": re, "ast": ast, "np": np, "pd": pd, "Path": Path}
    exec(compile(block, str(DET_PARENT), "exec"), ns)
    return ns, hashlib.sha256(block.encode()).hexdigest()[:16], block.count("\n")


DET, DET_SHA, DET_LINES = load_det()
scan_file = DET["scan_file"]
P(f"[DET ] idea 428 PART 0 extracted verbatim from {DET_PARENT.name}: {DET_LINES} lines, "
  f"sha256[:16] {DET_SHA}  (433 published 8dbb98aa47fd80cb)")
P(f"[CERT] idea 433's ground-truth key table re-read from {CERT_PARENT.name} "
  f"(sha256[:16] {hashlib.sha256(CERT_PARENT.read_bytes()).hexdigest()[:16]})")

LEVEL_FORM = """import numpy as np, pandas as pd
FLOOR = 1000000.0


def screen(px, vol):
    key = {src}
    mask = (key >= FLOOR) & px.notna()
    return mask
"""
RANK_FORM = """import numpy as np, pandas as pd
NSEL = 20


def screen(px, vol):
    key = {src}
    sel = key.rank(axis=1, ascending=False) <= NSEL
    return sel
"""


def det_on_key(src, form):
    """Run DET on a synthesised single-key file; return (flagged, bucket, deg)."""
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as fh:
            fh.write(form.format(src=src))
            p = Path(fh.name)
        hits, status = scan_file(p)
        p.unlink()
    except Exception:
        return None, "HARNESS_FAIL", 0
    if status != "OK":
        return None, "PARSE_FAIL", 0
    live = [h for h in (hits or []) if h["bucket"] in ("B1", "B2") and h["deg"] >= 1]
    if not live:
        b = (hits or [{}])[0].get("bucket", "-") if hits else "-"
        d = max([h["deg"] for h in hits] or [0]) if hits else 0
        return False, b, d
    return True, live[0]["bucket"], live[0]["deg"]


def rankpct(df):
    return df.rank(axis=1, pct=True)


def cert_on_key(src, p, v):
    """CERT.  Fraction of cells whose VALUE (resp. cross-sectional rankpct) moves under
    px -> px @ diag(c).  Returns (rank_moved, value_moved) or (nan, nan) if it cannot be run."""
    rng = np.random.default_rng(SEED)
    env = {"np": np, "pd": pd}
    try:
        K0 = eval(src, env, {"px": p, "vol": v})                                  # noqa: S307
    except Exception:
        return np.nan, np.nan
    if isinstance(K0, pd.Series):
        K0 = K0.to_frame("K")
    K0 = K0.astype(float)
    R0, dr, dl = rankpct(K0), [], []
    for _ in range(NDRAW):
        c = pd.Series(rng.lognormal(0.0, SIGMA, size=p.shape[1]), index=p.columns)
        try:
            K1 = eval(src, env, {"px": p.mul(c, axis=1), "vol": v})               # noqa: S307
        except Exception:
            return np.nan, np.nan
        if isinstance(K1, pd.Series):
            K1 = K1.to_frame("K")
        K1 = K1.astype(float)
        if K1.shape != K0.shape:
            return np.nan, np.nan
        ok = K0.notna() & K1.notna()
        n = int(ok.values.sum())
        if n == 0:
            dr.append(np.nan)
            dl.append(np.nan)
            continue
        dr.append(float((((rankpct(K1) - R0).abs() > TOL) & ok).values.sum()) / n)
        rel = (K1 - K0).abs() / K0.abs().clip(lower=1e-12)
        dl.append(float(((rel > TOL) & ok).values.sum()) / n)
    if not np.isfinite(dr).any():
        return np.nan, np.nan
    return float(np.nanmean(dr)), float(np.nanmean(dl))


# =====================================================================================
# PART 1 — panels
# =====================================================================================
def build_panels():
    px56 = load_universe()
    tr56 = sorted(c for c in px56.columns)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in pxs.columns if c == "SPY" or c not in bad]
    pxs = pxs[keep].dropna(how="all").ffill()
    small_tr = sorted(c for c in pxs.columns if c != "SPY")
    vs = load_volume(small=True).reindex(index=pxs.index, columns=pxs.columns)
    P(f"[panels] U56 {len(tr56)} cols {px56.index[0].date()}..{px56.index[-1].date()}  |  "
      f"SMALL{len(small_tr)} tradable (+SPY benchmark) "
      f"{pxs.index[0].date()}..{pxs.index[-1].date()}")
    P("[panels] SURVIVORSHIP: both panels are CURRENT constituents; SMALL doubly so (only names "
      "that still screen today).  No book is proposed on either — only same-days contrasts.")
    return {"U56": (px56, tr56, None), f"SMALL{len(small_tr)}": (pxs, small_tr, vs)}


PANELS = build_panels()
SMALL_NAME = [k for k in PANELS if k.startswith("SMALL")][0]


def cert_panel(ncol=100, nrow=500):
    px, tr, vs = PANELS[SMALL_NAME]
    cols = [c for c in tr][:ncol]
    p = px[cols].iloc[-nrow:].copy()
    v = vs[cols].reindex(p.index).ffill()
    return p, v


PC, VC = cert_panel()
STEP = 1.0 / PC.shape[1]
P(f"[CERT ] panel {PC.shape[0]}d x {PC.shape[1]} names {PC.index[0].date()}..{PC.index[-1].date()}"
  f", volume data/volume_small.csv.gz; sigma {SIGMA}, {NDRAW} draws, seed {SEED}, "
  f"calibration ONE RANK STEP = 1/{PC.shape[1]} = {STEP:.4f} (derived, not fitted)")


# =====================================================================================
# PART 2 — GATE: reproduce idea 433's 20-key adjudication before back-filling anything
# =====================================================================================
P("\n" + "-" * 118)
P("GATE A — reproduce idea 433's published instrument comparison on its own 20-key corpus")
P("-" * 118)
KEYS20 = pd.read_csv(CERT_PARENT.with_suffix("").as_posix().replace(
    "_cloud", "_cloud") + ".keys.csv") if False else pd.read_csv(
    OUT / "2026-09-08_adopt-the-T1-DEGREE-DETECTOR-as-the-PROTOCOL-corpus-gate_cloud.keys.csv")
g = []
for _, r in KEYS20.iterrows():
    fl_L, bk_L, dg_L = det_on_key(r["src"], LEVEL_FORM)
    fl_R, _, _ = det_on_key(r["src"], RANK_FORM)
    rm, lm = cert_on_key(r["src"], PC, VC)
    g.append(dict(key=r["key"], src=r["src"], truth_level_safe=bool(r["truth_level_safe"]),
                  truth_rank_safe=bool(r["truth_rank_safe"]),
                  truth_either_leaks=(not r["truth_level_safe"]) or (not r["truth_rank_safe"]),
                  DET_level_flag=fl_L, DET_rank_flag=fl_R, DET_deg=dg_L,
                  CERT_rank_moved=rm, CERT_value_moved=lm,
                  CERT_value_clears=(lm <= STEP), CERT_rank_clears=(rm <= STEP),
                  DET_clause_clears=(fl_L is False) and (fl_R is False)))
G = pd.DataFrame(g)
G.to_csv(OUT / f"{STEM}.keys.csv", index=False)
det_clear = int(G.DET_clause_clears.sum())
det_false_clear = sorted(G[G.DET_clause_clears & G.truth_either_leaks].key)
det_false_rej = sorted(G[(~G.DET_clause_clears) & (~G.truth_either_leaks)].key)
cv_clear = int(G.CERT_value_clears.sum())
cv_false_clear = sorted(G[G.CERT_value_clears & G.truth_either_leaks].key)
cv_false_rej = sorted(G[(~G.CERT_value_clears) & (~G.truth_either_leaks)].key)
cr_false_clear = sorted(G[G.CERT_rank_clears & G.truth_either_leaks].key)
cr_false_rej = sorted(G[(~G.CERT_rank_clears) & (~G.truth_either_leaks)].key)
P(f"  DET  clause clears {det_clear}/20  false clearances {len(det_false_clear)} "
  f"({', '.join(det_false_clear) or 'none'})  false rejections {len(det_false_rej)} "
  f"({', '.join(det_false_rej) or 'none'})")
P(f"  CERT-VALUE @1 step clears {cv_clear}/20  false clearances {len(cv_false_clear)} "
  f"({', '.join(cv_false_clear) or 'none'})  false rejections {len(cv_false_rej)} "
  f"({', '.join(cv_false_rej) or 'none'})")
P(f"  CERT-RANK  @1 step (the form idea 426 DRAFTS) false clearances {len(cr_false_clear)} "
  f"({', '.join(cr_false_clear) or 'none'})  false rejections {len(cr_false_rej)} "
  f"({', '.join(cr_false_rej) or 'none'})")
rep = (det_clear == 12 and set(det_false_clear) == {"PXDIFF", "LOGPX", "PXRANK", "DVRANK"}
       and det_false_rej == ["REBASED"] and len(cv_false_clear) == 0 and len(cv_false_rej) == 0
       and cr_false_clear == ["MKTLVL"] and len(cr_false_rej) == 0)
P(f"  GATE A: idea 433's published table reproduced EXACTLY on all five counts: "
  f"{'PASS' if rep else 'FAIL'}"
  + ("" if rep else "  <-- deviation from the committed table, read the row dump"))
P("  -> the adjudicator this back-fill uses is CERT-VALUE at one rank step, with DET beside it.")


# =====================================================================================
# GATE B — fast_bt == engine.backtest, and the cost-rung identity
# =====================================================================================
def fast_bt(px, w, freq=FREQ):
    idx = px.index
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    T, N = rets.shape
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mask)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    gross = pd.Series(np.abs(held).sum(axis=1), index=idx)
    return pd.Series((held * rets).sum(axis=1), index=idx), pd.Series(turn, index=idx), gross


def netr(gr, tn, bps):
    return gr - tn * bps / 1e4


P("\n" + "-" * 118)
P("GATE B — engine identity and the cost rung")
P("-" * 118)
_px = PANELS["U56"][0]
_w = rules_v2_weights(_px)
_g, _t, _gs = fast_bt(_px, _w)
_e = backtest(_px, _w, cost_bps=0, freq=FREQ)["returns"]
d1 = float((netr(_g, _t, 0) - _e).abs().max())
_e10 = backtest(_px, _w, cost_bps=PROTO_COST, freq=FREQ)["returns"]
d2 = float((netr(_g, _t, PROTO_COST) - _e10).abs().max())
P(f"  fast_bt == engine.backtest on the RULES v2 control book: 0 bps {d1:.3e}, "
  f"{PROTO_COST} bps {d2:.3e}   (PASS if < 1e-12: "
  f"{'PASS' if max(d1, d2) < 1e-12 else 'FAIL'})")


# =====================================================================================
# PART 3 — THE BACK-FILL: harvest every key the record can still be made to run
# =====================================================================================
P("\n" + "-" * 118)
P("PART 3  THE BACK-FILL — harvest, reconstruct, certify")
P("-" * 118)
PRICE_RE = re.compile(r"^(px|pxp|pxs|px56|pxb|pxsm|pxu|prices|price|closes|close|panel|pan|PX|P)$")
VOL_RE = re.compile(r"^(vol|vols|volume|vsh|dvol|VOL|V)$")
FREE_OK = {"np", "pd"}
SKIP_VALUE = (ast.Name, ast.Constant, ast.Lambda, ast.Dict, ast.List, ast.Tuple,
              ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp)
# constructors that return UNINITIALISED memory: the expression is not a function of px at all,
# so no certificate can be run on it.  Detected at source, because within one process the same
# freed buffer is often handed back and a double evaluation agrees by luck.
UNINIT = re.compile(r"\bnp\.(empty|empty_like)\b|\bnp\.ndarray\(")


class Rename(ast.NodeTransformer):
    def visit_Name(self, n):
        if PRICE_RE.match(n.id):
            return ast.Name(id="px", ctx=n.ctx)
        if VOL_RE.match(n.id):
            return ast.Name(id="vol", ctx=n.ctx)
        return n


def name_set(node):
    return {x.id for x in ast.walk(node) if isinstance(x, ast.Name)}


def _single_assign_defs(body, parent, params):
    """Names assigned EXACTLY ONCE in this body (not descending into nested defs) -> their expr."""
    d = dict(parent)
    cnt = Counter()

    def walk(b, sink):
        for nd in b:
            if isinstance(nd, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                continue
            if isinstance(nd, ast.Assign) and len(nd.targets) == 1 \
                    and isinstance(nd.targets[0], ast.Name):
                sink(nd.targets[0].id, nd.value)
            for fld in ("body", "orelse", "finalbody"):
                if hasattr(nd, fld):
                    walk(getattr(nd, fld), sink)

    walk(body, lambda nm, v: cnt.__setitem__(nm, cnt[nm] + 1))
    walk(body, lambda nm, v: d.__setitem__(nm, v) if cnt[nm] == 1 else None)
    d.update(params)
    return d


def scope_defs(tree):
    """(scope_node, name->expr) for the module and for every function, params-with-defaults bound."""
    mod = _single_assign_defs(tree.body, {}, {})
    out = [(tree, mod)]
    for nd in ast.walk(tree):
        if isinstance(nd, (ast.FunctionDef, ast.AsyncFunctionDef)):
            a = nd.args
            allargs = list(a.posonlyargs) + list(a.args)
            params = {}
            if a.defaults:
                for arg, dv in zip(allargs[len(allargs) - len(a.defaults):], a.defaults):
                    params[arg.arg] = dv
            for arg, dv in zip(a.kwonlyargs, a.kw_defaults):
                if dv is not None:
                    params[arg.arg] = dv
            out.append((nd, _single_assign_defs(nd.body, mod, params)))
    return out


def inline(expr, defs, depth=0):
    """Substitute single-assignment names by their defining expression, recursively."""
    if depth > 7:
        return expr

    class T(ast.NodeTransformer):
        def visit_Name(self, n):
            if PRICE_RE.match(n.id) or VOL_RE.match(n.id) or n.id in FREE_OK:
                return n
            if n.id in defs:
                sub = {k: v for k, v in defs.items() if k != n.id}
                return inline(ast.parse(ast.unparse(defs[n.id])).body[0].value, sub, depth + 1)
            return n

    return T().visit(ast.parse(ast.unparse(expr)).body[0].value)


HC = Counter()
SITES = defaultdict(set)          # normalised expr -> set of files
for f in sorted(ROOT.glob("research/**/*.py")):
    if f.name == Path(__file__).name:
        continue
    try:
        tree = ast.parse(f.read_text())
    except Exception:
        HC["file_parse_fail"] += 1
        continue
    HC["files"] += 1
    for scope, defs in scope_defs(tree):
        for node in ast.walk(scope):
            if not isinstance(node, ast.Assign):
                continue
            v = node.value
            if isinstance(v, SKIP_VALUE):
                continue
            HC["assign_sites"] += 1
            raw = name_set(v)
            try:
                iv = inline(v, defs)
            except Exception:
                HC["inline_fail"] += 1
                continue
            nm = name_set(iv)
            price_borne_syntactically = any(PRICE_RE.match(x) or VOL_RE.match(x) for x in nm)
            if not price_borne_syntactically:
                HC["not_price_bearing"] += 1
                continue
            HC["key_bearing_sites"] += 1
            free = {x for x in nm if not (PRICE_RE.match(x) or VOL_RE.match(x) or x in FREE_OK)}
            if free:
                HC["free_var_wall"] += 1
                continue
            try:
                s = ast.unparse(Rename().visit(iv))
            except Exception:
                HC["unparse_fail"] += 1
                continue
            if len(s) > 400:
                HC["too_long"] += 1
                continue
            HC["reconstructible_sites"] += 1
            SITES[s].add(f.name)
            _ = raw

P(f"  corpus: {HC['files']} committed .py under research/ ({HC['file_parse_fail']} unparseable)")
P(f"  assignment sites visited            {HC['assign_sites']:>8,}")
P(f"  of which KEY-BEARING (touch px/vol) {HC['key_bearing_sites']:>8,}")
P(f"    reconstructible after inlining    {HC['reconstructible_sites']:>8,}"
  f"   ({HC['reconstructible_sites'] / max(HC['key_bearing_sites'], 1):.1%} of key-bearing)")
P(f"    blocked by the FREE-VARIABLE WALL {HC['free_var_wall']:>8,}"
  f"   ({HC['free_var_wall'] / max(HC['key_bearing_sites'], 1):.1%})")
P(f"  distinct normalised expressions     {len(SITES):>8,}")

RNG = np.random.default_rng(SEED)
PERT = PC * (1.0 + pd.DataFrame(RNG.normal(0.0, 0.05, PC.shape),
                                index=PC.index, columns=PC.columns))


def classify(s):
    env = {"np": np, "pd": pd}
    try:
        K = eval(s, env, {"px": PC, "vol": VC})                                   # noqa: S307
    except Exception as e:
        return "UNREACHABLE", type(e).__name__, None
    if isinstance(K, pd.Series):
        K = K.to_frame("K")
    if not isinstance(K, pd.DataFrame) or not K.index.equals(PC.index) or K.shape[1] == 0:
        return "NOT_PANEL", type(K).__name__, None
    try:
        A = np.asarray(K.values, dtype=float)
    except Exception:
        return "NOT_NUMERIC", str(K.dtypes.iloc[0]), None
    # REPRODUCIBLE: the certificate compares key(px) against key(px @ diag(c)), so it presupposes
    # that key(px) is a FUNCTION of px.  Two harvested expressions are not: the inliner
    # substituted an `np.empty_like(...)` allocation whose buffer is filled by a later loop, so
    # they read UNINITIALISED MEMORY and return a different answer every call.  Evaluating twice
    # catches them; without this gate the back-fill column is irreproducible run to run (observed:
    # the PASS/FAIL split moved 74/39 -> 72/41 between two runs of a seeded certificate).
    if UNINIT.search(s):
        return "NOT_REPRODUCIBLE", "reads uninitialised memory (np.empty/empty_like)", None
    _churn = np.random.default_rng(1).normal(size=A.shape)                  # perturb the heap
    try:
        Ka = eval(s, env, {"px": PC, "vol": VC})                                  # noqa: S307
    except Exception as e:
        return "UNREACHABLE", "rerun:" + type(e).__name__, None
    del _churn
    if isinstance(Ka, pd.Series):
        Ka = Ka.to_frame("K")
    Aa = np.asarray(Ka.values, dtype=float)
    if Aa.shape != A.shape or not np.array_equal(np.nan_to_num(A, nan=-9.87e30),
                                                 np.nan_to_num(Aa, nan=-9.87e30)):
        return "NOT_REPRODUCIBLE", "value differs between two calls on the same px", None
    try:
        K2 = eval(s, env, {"px": PERT, "vol": VC})                                # noqa: S307
    except Exception as e:
        return "UNREACHABLE", "pert:" + type(e).__name__, None
    if isinstance(K2, pd.Series):
        K2 = K2.to_frame("K")
    B = np.asarray(K2.values, dtype=float)
    if A.shape != B.shape or np.array_equal(np.nan_to_num(A), np.nan_to_num(B)):
        return "NOT_PRICE_BORNE", "", None
    is_bool = bool(K.dtypes.astype(str).eq("bool").all())
    uses_vol = "vol" in name_set(ast.parse(s).body[0].value)
    # IDENTITY: the expression is a re-expression of the panel itself (a handle: .copy(),
    # .ffill(), .drop(columns=['SPY']), a slice), not a key.  It is arithmetically degree 1 and
    # T1-FAILs correctly, but calling it a "failed key" would overstate the back-fill.  Split it
    # out: same columns as px, and every co-present cell equal to px.
    ident = False
    if A.shape[1] == PC.shape[1] and list(K.columns) == list(PC.columns):
        X = PC.values
        both = np.isfinite(A) & np.isfinite(X)
        ident = bool(both.any() and np.allclose(A[both], X[both], rtol=0, atol=0))
    return "KEY", ("identity" if ident else ("bool" if is_bool else "numeric")), \
        (K.shape[1], is_bool, uses_vol, ident)


rows, cls = [], Counter()
t_cert = 0.0
for s in sorted(SITES):
    kind, detail, extra = classify(s)
    cls[kind] += 1
    r = dict(expr=s, n_files=len(SITES[s]), files=";".join(sorted(SITES[s])[:6]),
             admitted=kind, detail=detail)
    if kind == "KEY":
        t = time.time()
        rm, lm = cert_on_key(s, PC, VC)
        t_cert += time.time() - t
        fl_L, bk_L, dg_L = det_on_key(s, LEVEL_FORM)
        fl_R, _, _ = det_on_key(s, RANK_FORM)
        r.update(ncol=extra[0], is_bool=extra[1], uses_vol=extra[2], is_identity=extra[3],
                 CERT_value_moved=lm, CERT_rank_moved=rm,
                 T1=("PASS" if (np.isfinite(lm) and lm <= STEP)
                     else ("FAIL" if np.isfinite(lm) else "CERT_NA")),
                 DET_flag=(bool(fl_L) if fl_L is not None else None),
                 DET_rank_flag=(bool(fl_R) if fl_R is not None else None),
                 DET_deg=dg_L, DET_clears=((fl_L is False) and (fl_R is False)))
    rows.append(r)
B = pd.DataFrame(rows)
B.to_csv(OUT / f"{STEM}.backfill.csv", index=False)
K = B[B.admitted == "KEY"].copy()
P(f"\n  admission of the {len(B)} distinct expressions: " +
  ", ".join(f"{k} {v}" for k, v in sorted(cls.items(), key=lambda x: -x[1])))
P(f"  CERT ran on all {len(K)} admitted keys in {t_cert:.1f}s "
  f"({t_cert / max(len(K), 1) * 1000:.0f} ms/key)")

npass = int((K.T1 == "PASS").sum())
nfail = int((K.T1 == "FAIL").sum())
KI = K[K.is_identity.astype(bool)]
KR = K[~K.is_identity.astype(bool)]
P(f"\n  *** THE BACK-FILL COLUMN: T1 PASS {npass}/{len(K)}, T1 FAIL {nfail}/{len(K)} ***")
P(f"  of which {len(KI)} are IDENTITY re-expressions of the panel itself (.copy(), .ffill(), "
  f"a slice, drop(SPY)) — arithmetically degree 1, T1-FAIL {int((KI.T1 == 'FAIL').sum())}/"
  f"{len(KI)} correctly, but they are panel HANDLES, not keys.  Split them out and the real "
  f"back-fill is {len(KR)} keys: T1 PASS {int((KR.T1 == 'PASS').sum())}, "
  f"T1 FAIL {int((KR.T1 == 'FAIL').sum())}.")
P(f"\n  {'n':>4} {'T1':<5}{'DET':<6}{'kind':<9}{'CERTval':>9}{'CERTrnk':>9}  expression")
P("  " + "-" * 114)
for _, r in K.sort_values(["T1", "n_files"], ascending=[True, False]).iterrows():
    d = "FLAG" if r.DET_flag else ("pass" if r.DET_flag is False else "n/a")
    P(f"  {r.n_files:>4} {r.T1:<5}{d:<6}{r.detail:<9}"
      f"{r.CERT_value_moved:>9.4f}{r.CERT_rank_moved:>9.4f}  {r.expr[:84]}")

# ---- DET vs CERT disagreements on the record's own keys (the back-fill's own audit) ----------
dis = K[(K.DET_clears) != (K.T1 == "PASS")]
P(f"\n  DET/CERT DISAGREEMENTS on the record's own keys: {len(dis)}/{len(K)}")
for _, r in dis.iterrows():
    P(f"    DET {'clears' if r.DET_clears else 'flags '} / CERT says {r.T1:<4} "
      f"(value moved {r.CERT_value_moved:.4f})  n={r.n_files}  {r.expr[:74]}")

# ---- the FAIL keys and their reach into the record -------------------------------------------
fail_files = set()
for _, r in K[K.T1 == "FAIL"].iterrows():
    fail_files |= SITES[r.expr]
P(f"\n  reach of the T1-FAIL keys: {nfail} expressions carried by {len(fail_files)} committed "
  f"scripts")
worst = K[K.T1 == "FAIL"].sort_values("n_files", ascending=False).head(6)
for _, r in worst.iterrows():
    P(f"    n={r.n_files:<4} {r.expr[:96]}")

# ---- P3: does anything PASS T1 and still leak? ------------------------------------------------
FWD_PAT = re.compile(r"shift\(-\d+\)|iloc\[-1\]")
lookahead_pass = K[(K.T1 == "PASS") & K.expr.str.contains(FWD_PAT)]
P(f"\n  keys that PASS T1 and are nonetheless FORWARD-LOOKING (shift(-k) or iloc[-1]): "
  f"{len(lookahead_pass)}")
for _, r in lookahead_pass.iterrows():
    P(f"    n={r.n_files:<4} PASS  {r.expr[:96]}")
lookahead_fail = K[(K.T1 == "FAIL") & K.expr.str.contains(FWD_PAT)]
for _, r in lookahead_fail.iterrows():
    P(f"    n={r.n_files:<4} FAIL  {r.expr[:96]}")

cov = pd.DataFrame([dict(metric=k, value=v) for k, v in HC.items()]
                   + [dict(metric=f"admitted_{k}", value=v) for k, v in cls.items()]
                   + [dict(metric="T1_PASS", value=npass), dict(metric="T1_FAIL", value=nfail),
                      dict(metric="fail_files", value=len(fail_files)),
                      dict(metric="cert_seconds", value=round(t_cert, 2))])
cov.to_csv(OUT / f"{STEM}.coverage.csv", index=False)


# =====================================================================================
# PART 4 — what the back-fill touches in the PUBLISHED record
# =====================================================================================
P("\n" + "-" * 118)
P("PART 4  CENSUS — which committed scripts and LEADERBOARD rows carry a T1-FAIL key")
P("-" * 118)
lb = (ROOT / "research" / "LEADERBOARD.md").read_text().split("\n")
lb_rows = [ln for ln in lb if ln.startswith("|") and ln.count("|") >= 8
           and not ln.startswith("|---") and "| date " not in ln.lower()]
hit_rows = [ln for ln in lb_rows if any(f.replace(".py", "") in ln for f in fail_files)]
P(f"  LEADERBOARD rows total {len(lb_rows)}; rows whose script carries a T1-FAIL key "
  f"{len(hit_rows)} ({len(hit_rows) / max(len(lb_rows), 1):.1%})")
cen = pd.DataFrame([dict(file=f, n_fail_keys=sum(1 for _, r in K[K.T1 == "FAIL"].iterrows()
                                                 if f in SITES[r.expr]))
                    for f in sorted(fail_files)])
cen.to_csv(OUT / f"{STEM}.census.csv", index=False)
P(f"  scripts carrying >=2 distinct T1-FAIL keys: "
  f"{int((cen.n_fail_keys >= 2).sum()) if len(cen) else 0}")
P("  NOTE: carrying a T1-FAIL key is NOT the same as PUBLISHING a verdict that rests on one — a "
  "200d moving average is a degree-1 object used inside a degree-0 ratio in almost every one of "
  "these files.  The census counts SITES, and the adjudication of a site is the ratio it sits in, "
  "which is why the clause below is worded on the KEY AS USED, not on every sub-expression.")


# =====================================================================================
# PART 5 — THE CLAUSE (drafted; PROTOCOL.md NOT edited — rule 6, Sunday review)
# =====================================================================================
CLAUSE = """
PROTOCOL clause 10 (T1 — adjustment invariance).  DRAFT, report-only.

10. **Adjustment invariance (T1).**  `data/prices*.csv` holds auto-adjusted closes, so truncating
    or re-downloading a panel multiplies each name's WHOLE history by one positive constant
    (px -> px @ diag(c)).  A key is therefore admissible only if the quantity the book actually
    consumes is invariant under that operator.  Adjudicate in this ORDER:
    (a) GATE — run idea 428's degree detector over the script.  Degree >= 1 in the price scale is
        a finding to be answered, never a verdict: the detector is blind to the rank family
        (`rank(key) <= n` is degree 0 whatever the key) and mis-types `diff`, `log` and `var`.
    (b) ADJUDICATOR — the certificate presupposes the key is a FUNCTION of the panel, so first
        evaluate it twice and require agreement: a key that is not reproducible cannot be
        certified.  Then run the VALUE certificate on the key AS THE BOOK USES IT: draw c_i
        lognormal(0, 0.25), recompute, and report the fraction of cells whose value moves by more
        than 1e-9 relative.  Compare that fraction against ONE RANK STEP (1/N names), which is the
        float64 tie-swap floor, not a tuned tolerance.  Above it the key is T1-FAIL and no verdict
        resting on it may be published; at or below it the key is T1-PASS.
    (c) A T1-PASS key is NOT thereby implementable.  T1 certifies the ADJUSTMENT channel only.
        Forward-dated keys (`px.shift(-k)`, `px.iloc[-1]/px`) are homogeneous of degree 0 and
        PASS T1 while being pure look-ahead.  T1 is a NECESSARY condition, never a sufficient one,
        and it must be run BEFORE rule 8, because rule 8 splits by DATE and cannot see terminal
        dating (idea 195).
"""
P("\n" + "-" * 118)
P("PART 5  THE CLAUSE — drafted, report-only (PROTOCOL.md is NOT edited; rule 6, Sunday review)")
P("-" * 118)
for ln in CLAUSE.strip("\n").split("\n"):
    P("  " + ln)


# =====================================================================================
# PART 6 — THE BOOK: two tuned parameters (KEY, m), every grid point reported
# =====================================================================================
P("\n" + "-" * 118)
P("PART 6  BOOK — PROTOCOL 2/3/4/8.  Tuned: KEY x m.  Every grid point below.")
P("-" * 118)
cand = K[(~K.is_bool.astype(bool)) & (~K.uses_vol.astype(bool))].copy()
cand = cand[cand.ncol > 1]
cand = cand.sort_values(["n_files", "expr"], ascending=[False, True])
BOOKKEYS = cand.head(NKEY_BOOK)[["expr", "n_files", "T1", "CERT_value_moved"]].reset_index(drop=True)
BOOKKEYS["kid"] = ["K%02d" % i for i in range(len(BOOKKEYS))]
P(f"  key set = the {len(BOOKKEYS)} most-used reconstructible price-only numeric multi-column "
  f"keys in the record (mechanical rule: sort by n_files desc, expr asc, take the head)")
for _, r in BOOKKEYS.iterrows():
    P(f"    {r.kid}  n={r.n_files:<4} T1={r.T1:<5}  {r.expr[:92]}")
P(f"  T1 split of the book key set: PASS {(BOOKKEYS.T1 == 'PASS').sum()}, "
  f"FAIL {(BOOKKEYS.T1 == 'FAIL').sum()}")
P(f"  tilt grid m = {MGRID}   (m=0 is the NO-TILT control, shared by every key)")
P("  gross is held EXACTLY equal across every m by rw normalisation, so m moves the "
  "cross-section and never the exposure (idea 415); realised gross published beside every "
  "Sharpe (idea 641).")

BOOKS = ["EWALL", "MA200"]


def tilt_weights(px, key, m, book):
    live = px.notna()
    if book == "MA200":
        live = live & (px > px.rolling(200).mean()).fillna(False)
    if m == 0.0:
        num = live.astype(float)
    else:
        r = key.where(live).rank(axis=1, pct=True)
        mult = (1.0 + m * (2.0 * r - 1.0)).clip(lower=0.0)
        num = live.astype(float) * mult.fillna(0.0)
    den = num.sum(axis=1).replace(0.0, np.nan)
    return num.div(den, axis=0).mul(GROSS).fillna(0.0)


def mrow(r):
    m = metrics(r)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


START, SPYM, SPYOOS, V2M, V1M = {}, {}, {}, {}, {}
for pn, (px, tr, vs) in PANELS.items():
    START[pn] = px.index[260]
    sp = px["SPY"].pct_change().fillna(0.0).loc[START[pn]:] if "SPY" in px.columns else None
    SPYM[pn] = mrow(sp)
    SPYOOS[pn] = metrics(sp.loc[OOS_START:])
    cols = [c for c in px.columns if c in set(tr)]
    for nm, fn, sink in (("v2", rules_v2_weights, V2M), ("v1", rules_v1_weights, V1M)):
        g_, t_, _ = fast_bt(px[cols], fn(px[cols]))
        r_ = netr(g_, t_, PROTO_COST).loc[START[pn]:]
        sink[pn] = (mrow(r_), metrics(r_.loc[OOS_START:]))

ROWS = []
for pn, (px, tr, vs) in PANELS.items():
    cols = [c for c in px.columns if c in set(tr)]
    pxp = px[cols]
    kcache = {}
    for _, kr in BOOKKEYS.iterrows():
        try:
            kv = eval(kr.expr, {"np": np, "pd": pd}, {"px": pxp, "vol": None})    # noqa: S307
        except Exception:
            kv = None
        if isinstance(kv, pd.Series):
            kv = kv.to_frame("K")
        kcache[kr.kid] = kv if (isinstance(kv, pd.DataFrame)
                                and kv.shape == pxp.shape) else None
    for book in BOOKS:
        for _, kr in BOOKKEYS.iterrows():
            kv = kcache[kr.kid]
            if kv is None:
                continue
            for m in MGRID:
                w = tilt_weights(pxp, kv, m, book)
                g_, t_, gs = fast_bt(pxp, w)
                for cb in COSTS:
                    r_ = netr(g_, t_, cb).loc[START[pn]:]
                    mm = mrow(r_)
                    oos = metrics(r_.loc[OOS_START:])
                    ins = metrics(r_.loc[:IS_END])
                    ROWS.append(dict(panel=pn, book=book, kid=kr.kid, key=kr.expr, T1=kr.T1, m=m,
                                     cost_bps=cb, gross=float(gs.loc[START[pn]:].mean()),
                                     turnover=float(t_.loc[START[pn]:].sum()
                                                    / ((len(r_)) / 252.0)),
                                     CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                                     H1=mm["H1"], H2=mm["H2"], IS_Sharpe=ins["Sharpe"],
                                     OOS_CAGR=oos["CAGR"], OOS_Sharpe=oos["Sharpe"],
                                     OOS_MaxDD=oos["MaxDD"]))
BK = pd.DataFrame(ROWS)
BK.to_csv(OUT / f"{STEM}.book.csv", index=False)


def keep_paths(row, pn):
    sm, v2 = SPYM[pn], V2M[pn][0]
    a = (row["H1"] > v2["H1"]) and (row["H2"] > v2["H2"]) and (row["MaxDD"] >= v2["MaxDD"])
    b = (row["H1"] > sm["H1"]) and (row["H2"] > sm["H2"]) \
        and (row["OOS_Sharpe"] > SPYOOS[pn]["Sharpe"]) \
        and (row["MaxDD"] >= 0.60 * sm["MaxDD"]) and (row["CAGR"] >= 0.70 * sm["CAGR"])
    return a, b


BK["pass4a"], BK["pass4b"] = zip(*[keep_paths(r, r["panel"]) for _, r in BK.iterrows()])
BK.to_csv(OUT / f"{STEM}.book.csv", index=False)
P(f"\n  grid = {BK.panel.nunique()} panels x {len(BOOKS)} books x {BK.kid.nunique()} keys x "
  f"{len(MGRID)} tilts x {len(COSTS)} rungs = {len(BK)} rows, ALL written to .book.csv")
P("  NOTE 1: m=0 is the SAME book for every key (no tilt), so its row is duplicated "
  f"{BK.kid.nunique()} times per (panel, book).  Counts are given BOTH raw and deduped.")
P("  NOTE 2: the T1-FAIL keys K08/K09/K11/K12 are identity handles of the panel, so tilting on "
  "them IS the price-LEVEL tilt and their rows are identical to each other by construction — a "
  "degeneracy of the mechanical key rule, reported not hidden.")
for cb in COSTS:
    sub = BK[BK.cost_bps == cb]
    ded = sub[~((sub.m == 0.0) & (sub.kid != BOOKKEYS.kid.iloc[0]))]
    P(f"    {cb:>2} bps: 4a {int(sub.pass4a.sum()):>4}/{len(sub)}   "
      f"4b {int(sub.pass4b.sum()):>4}/{len(sub)}   "
      f"| deduped 4a {int(ded.pass4a.sum()):>3}/{len(ded)}  4b {int(ded.pass4b.sum()):>3}/"
      f"{len(ded)}   (of which m=0 controls: 4b "
      f"{int(ded[(ded.m == 0.0)].pass4b.sum())}/{int((ded.m == 0.0).sum())})")
_p10 = BK[(BK.cost_bps == PROTO_COST) & (BK.m == 0.0)]
P(f"  the m=0 CONTROL alone passes 4b in "
  f"{int(_p10.groupby(['panel', 'book']).pass4b.first().sum())} of "
  f"{_p10.groupby(['panel', 'book']).ngroups} (panel, book) cells at {PROTO_COST} bps — so the "
  f"4b passes above are the UNDERLYING BOOK clearing, not the key.")
p10 = BK[BK.cost_bps == PROTO_COST]
P(f"\n  gross across the whole {PROTO_COST}-bps grid: min {p10.gross.min():.4f} "
  f"max {p10.gross.max():.4f} (spread {p10.gross.max() - p10.gross.min():.2e}) — the tilt is "
  f"NOT an exposure trade by construction")

P(f"\n  every grid point at the PROTOCOL rung ({PROTO_COST} bps), by panel/book "
  f"(CAGR / Sharpe / MaxDD / H1 / H2):")
for pn in PANELS:
    for book in BOOKS:
        sub = p10[(p10.panel == pn) & (p10.book == book)]
        if not len(sub):
            continue
        P(f"\n  --- {pn} / {book} ---   SPY {SPYM[pn]['CAGR']:.2%} {SPYM[pn]['Sharpe']:.3f} "
          f"{SPYM[pn]['MaxDD']:.2%} | RULES v2 {V2M[pn][0]['CAGR']:.2%} "
          f"{V2M[pn][0]['Sharpe']:.3f} {V2M[pn][0]['MaxDD']:.2%}")
        P(f"  {'key':<5}{'T1':<6}" + "".join(f"{m:>+9.2f}" for m in MGRID) + "   <- Sharpe by m")
        for kid in BOOKKEYS.kid:
            s = sub[sub.kid == kid]
            if not len(s):
                continue
            t1 = s.T1.iloc[0]
            P(f"  {kid:<5}{t1:<6}" + "".join(
                f"{s[s.m == m].Sharpe.iloc[0]:>9.3f}" if len(s[s.m == m]) else f"{'--':>9}"
                for m in MGRID))


# =====================================================================================
# PART 7 — RULE 8: does the T1 gate in FRONT of the chooser change what rule 8 buys?
# =====================================================================================
P("\n" + "-" * 118)
P("PART 7  RULE 8 WALK-FORWARD — (KEY, m) chosen on 2010..2016 IS Sharpe, 2017..2026 read once")
P("-" * 118)
WF = []
for pn in PANELS:
    for book in BOOKS:
        sub = p10[(p10.panel == pn) & (p10.book == book)]
        if not len(sub):
            continue
        ctrl = sub[sub.m == 0.0].iloc[0]
        # S_T1F is NOT a third tuned parameter: it is the SAME grid read under clause 10 with the
        # dating exclusion 10(c) actually enforced, reported beside the other choosers to price
        # what the clause buys with and without it.  The forward-dated set is syntactic
        # (shift(-k) / iloc[-1]), fixed before the book ran.
        fwd_kids = set(BOOKKEYS[BOOKKEYS.expr.str.contains(FWD_PAT)].kid)
        for cname, pool in (("S_ALL  (no T1 gate)", sub),
                            ("S_T1   (T1-PASS only)", sub[sub.T1 == "PASS"]),
                            ("S_T1F  (T1-PASS + not forward-dated)",
                             sub[(sub.T1 == "PASS") & (~sub.kid.isin(fwd_kids))]),
                            ("S_FAIL (T1-FAIL only)", sub[sub.T1 == "FAIL"]),
                            ("S_NONE (m=0 control)", sub[sub.m == 0.0])):
            if not len(pool):
                continue
            pick = pool.loc[pool.IS_Sharpe.idxmax()]
            WF.append(dict(panel=pn, book=book, chooser=cname.split()[0], chooser_label=cname,
                           pick_kid=pick.kid, pick_m=pick.m, pick_T1=pick.T1,
                           IS_Sharpe=pick.IS_Sharpe, OOS_CAGR=pick.OOS_CAGR,
                           OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                           ctrl_OOS_Sharpe=ctrl.OOS_Sharpe, ctrl_OOS_CAGR=ctrl.OOS_CAGR,
                           ctrl_OOS_MaxDD=ctrl.OOS_MaxDD,
                           spy_OOS_Sharpe=SPYOOS[pn]["Sharpe"], spy_OOS_CAGR=SPYOOS[pn]["CAGR"],
                           spy_OOS_MaxDD=SPYOOS[pn]["MaxDD"],
                           v2_OOS_Sharpe=V2M[pn][1]["Sharpe"], v2_OOS_CAGR=V2M[pn][1]["CAGR"],
                           v2_OOS_MaxDD=V2M[pn][1]["MaxDD"],
                           v1_OOS_Sharpe=V1M[pn][1]["Sharpe"], v1_OOS_CAGR=V1M[pn][1]["CAGR"],
                           v1_OOS_MaxDD=V1M[pn][1]["MaxDD"],
                           beats_ctrl=bool(pick.OOS_Sharpe > ctrl.OOS_Sharpe),
                           beats_spy=bool(pick.OOS_Sharpe > SPYOOS[pn]["Sharpe"]),
                           beats_v2=bool(pick.OOS_Sharpe > V2M[pn][1]["Sharpe"])))
W = pd.DataFrame(WF)
W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
P(f"  {'panel':<10}{'book':<7}{'chooser':<8}{'pick':<14}{'IS Shp':>8}{'OOS CAGR':>10}"
  f"{'OOS Shp':>9}{'OOS DD':>9}{'vs ctrl':>9}{'vs SPY':>8}{'vs v2':>7}")
P("  " + "-" * 114)
for _, r in W.iterrows():
    P(f"  {r.panel:<10}{r.book:<7}{r.chooser:<8}"
      f"{r.pick_kid + '/' + format(r.pick_m, '+.2f') + '/' + r.pick_T1[0]:<14}"
      f"{r.IS_Sharpe:>8.3f}{r.OOS_CAGR:>10.2%}{r.OOS_Sharpe:>9.3f}{r.OOS_MaxDD:>9.2%}"
      f"{r.OOS_Sharpe - r.ctrl_OOS_Sharpe:>+9.3f}"
      f"{r.OOS_Sharpe - r.spy_OOS_Sharpe:>+8.3f}{r.OOS_Sharpe - r.v2_OOS_Sharpe:>+7.3f}")
P("")
for pn in PANELS:
    P(f"  {pn:<10} OOS comparands  SPY {SPYOOS[pn]['CAGR']:>7.2%} {SPYOOS[pn]['Sharpe']:.3f} "
      f"{SPYOOS[pn]['MaxDD']:>8.2%}  |  RULES v2 {V2M[pn][1]['CAGR']:>7.2%} "
      f"{V2M[pn][1]['Sharpe']:.3f} {V2M[pn][1]['MaxDD']:>8.2%}  |  RULES v1 "
      f"{V1M[pn][1]['CAGR']:>7.2%} {V1M[pn][1]['Sharpe']:.3f} {V1M[pn][1]['MaxDD']:>8.2%}")

for c in ("S_ALL", "S_T1", "S_T1F", "S_FAIL"):
    s = W[W.chooser == c]
    if not len(s):
        continue
    P(f"\n  {c:<7} beats the m=0 control in {int(s.beats_ctrl.sum())}/{len(s)} cells "
      f"(mean dOOS Sharpe {(s.OOS_Sharpe - s.ctrl_OOS_Sharpe).mean():+.4f}); "
      f"beats SPY {int(s.beats_spy.sum())}/{len(s)}; beats RULES v2 {int(s.beats_v2.sum())}/"
      f"{len(s)}")
sa = W[W.chooser == "S_ALL"].set_index(["panel", "book"]).OOS_Sharpe
st = W[W.chooser == "S_T1"].set_index(["panel", "book"]).OOS_Sharpe
if len(sa) and len(st):
    common = sa.index.intersection(st.index)
    d = (st.loc[common] - sa.loc[common])
    P(f"\n  *** PRICE OF THE T1 GATE IN FRONT OF RULE 8: mean OOS Sharpe(S_T1) - Sharpe(S_ALL) "
      f"= {d.mean():+.4f} over {len(common)} cells "
      f"(gate helps in {int((d > 0).sum())}, costs in {int((d < 0).sum())}, "
      f"identical pick in {int((d == 0).sum())}) ***")
sf = W[W.chooser == "S_T1F"].set_index(["panel", "book"]).OOS_Sharpe
if len(sf):
    cf = sa.index.intersection(sf.index)
    df_ = sf.loc[cf] - sa.loc[cf]
    P(f"  and with clause 10(c) ENFORCED (T1-PASS + not forward-dated): "
      f"Sharpe(S_T1F) - Sharpe(S_ALL) = {df_.mean():+.4f} over {len(cf)} cells — the dating "
      f"exclusion, not T1, is what moves the rule-8 pick.")

P("\n  the arms rule 8 passed over: TILT arms that pass 4b at the PROTOCOL rung, are T1-PASS, "
  "are NOT forward-dated, and beat their own m=0 control out of sample:")
fwd_k = set(BOOKKEYS[BOOKKEYS.expr.str.contains(FWD_PAT)].kid)
n_missed = 0
for (pn, bk), gg in p10.groupby(["panel", "book"]):
    ctrl_oos = gg[gg.m == 0.0].OOS_Sharpe.iloc[0]
    s = gg[(gg.m != 0.0) & gg.pass4b & (gg.T1 == "PASS") & (~gg.kid.isin(fwd_k))
           & (gg.OOS_Sharpe > ctrl_oos)]
    n_missed += len(s)
    P(f"    {pn:<10}{bk:<7} {len(s):>3} arms" + (f"  ({', '.join(sorted(s.kid.unique()))})"
                                                 if len(s) else ""))
P(f"    total {n_missed}.  Rule 8 picked NONE of them: its IS-Sharpe chooser preferred the "
  f"forward-dated key in every cell.  This is the cost of running T1 (or nothing) AFTER rule 8 "
  f"instead of before it.")

picks = W[W.chooser.isin(["S_ALL", "S_T1"])]
lk = set(BOOKKEYS[BOOKKEYS.expr.str.contains(FWD_PAT)].kid)
n_lk = int(picks.pick_kid.isin(lk).sum())
if n_lk:
    kk = BOOKKEYS[BOOKKEYS.kid.isin(picks.pick_kid[picks.pick_kid.isin(lk)])]
    P(f"\n  *** THE BACK-FILL'S OWN COUNTEREXAMPLE: rule 8's pick is a FORWARD-DATED key in "
      f"{n_lk} of {len(picks)} (S_ALL + S_T1) cells, and that key is T1-**PASS**: "
      f"{kk.expr.iloc[0]} ***")
    P(f"      The T1 gate does not remove it (it is degree 0 in the price scale), rule 8 does not "
      f"remove it (it is dated at T, and rule 8 splits by DATE), and it beats SPY, the m=0 "
      f"control and RULES v2 in every cell it is picked.  This reproduces idea 195's finding "
      f"through the back-fill's OWN harvest rather than by hand, and it is the reason clause "
      f"10(c) must be worded as NECESSARY-not-sufficient.")

P("\n  4b on the rule-8 picks (the leg PROTOCOL 4b requires):")
for _, r in W.iterrows():
    legs = [x for x, bad in (("OOS", r.OOS_Sharpe <= r.spy_OOS_Sharpe),
                             ("DD", r.OOS_MaxDD < 0.60 * r.spy_OOS_MaxDD),
                             ("CAGR", r.OOS_CAGR < 0.70 * r.spy_OOS_CAGR)) if bad]
    P(f"    {r.panel:<10}{r.book:<7}{r.chooser:<8} 4b-OOS legs failed: "
      f"{','.join(legs) if legs else 'NONE'}")


# =====================================================================================
# PART 8 — pre-registered predictions, verdict
# =====================================================================================
P("\n" + "-" * 118)
P("PART 8  PRE-REGISTERED PREDICTIONS")
P("-" * 118)
frac_reach = HC["reconstructible_sites"] / max(HC["key_bearing_sites"], 1)
p1 = frac_reach < 0.40
p2 = bool(len(K[(K.T1 == "FAIL") & (K.n_files >= 5)]))
p3 = bool(len(lookahead_pass))
gate_help = float(d.mean()) if (len(sa) and len(st) and len(common)) else float("nan")
tilt10 = BK[(BK.cost_bps == PROTO_COST) & (BK.m != 0.0)]
n4b_tilt = int(tilt10.pass4b.sum())
n4b_all = int(BK[BK.cost_bps == PROTO_COST].pass4b.sum())
p4 = (not np.isfinite(gate_help) or gate_help <= 0) and n4b_tilt == 0
P(f"  P1 back-fill reaches <40% of key-bearing sites          {frac_reach:.1%}   "
  f"{'HIT' if p1 else 'MISS'}")
P(f"  P2 a T1-FAIL key carried by >=5 committed scripts       "
  f"{int(K[(K.T1 == 'FAIL')].n_files.max()) if nfail else 0} max   "
  f"{'HIT' if p2 else 'MISS'}")
P(f"  P3 a key PASSES T1 and is still look-ahead             {len(lookahead_pass)} found   "
  f"{'HIT' if p3 else 'MISS'}")
P(f"  P4 T1 gate does not improve OOS, no TILT arm clears 4b   gate {gate_help:+.4f}, "
  f"4b(tilt) {n4b_tilt}   {'HIT' if p4 else 'MISS'}")
P(f"     (both readings given: 4b over ALL grid rows incl. the shared m=0 control is {n4b_all}; "
  f"over TILT rows only, which is what P4 says, it is {n4b_tilt}.)")

P("\n" + "=" * 118)
P("VERDICT")
P("=" * 118)
P(f"  ANSWERED / no KEEP.  4a {int(p10.pass4a.sum())}/{len(p10)} and 4b "
  f"{int(p10.pass4b.sum())}/{len(p10)} at the PROTOCOL rung; the deliverable is the CLAUSE and "
  f"the BACK-FILL COLUMN ({npass} PASS / {nfail} FAIL over {len(K)} reconstructible keys), not a "
  f"book.")
P(f"  RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched.")
P(f"\n  runtime {time.time() - T0:.1f}s")
(OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
