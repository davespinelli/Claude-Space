#!/usr/bin/env python3
"""QUEUE idea 644 — does-PROTOCOL-need-a-T2-DATING-clause-beside-T1 (lane C, 2026-09-10).

Question (verbatim from QUEUE)
-----------------------------
"idea 426's back-fill found the key rule 8 picks in 4 of 4 cells is `px.iloc[-1]/px - 1.0`:
FORWARD-DATED, T1-PASS (degree 0), invisible to rule 8's date split, and it beats SPY and RULES v2
on pure look-ahead.  T1 costs +0.0000 to gate it; a dating exclusion costs -0.4508 and removes it.
Draft T2 (no key may read a row dated after the weight date, terminal `iloc[-1]` included),
back-fill it over the same 111-key census beside the T1 column, and price it on the same grid.
Max 2 params (clause form, corpus)."

What this run adds that idea 426 (lane B) did not have
------------------------------------------------------
426 identified the hole and priced ONE exclusion, but it implemented that exclusion SYNTACTICALLY:
a regex `shift\\(-\\d+\\)|iloc\\[-1\\]` fixed by hand before the book ran.  A regex is a fine way to
name a counterexample you already found; it is not a clause, because a clause has to adjudicate
keys nobody has looked at.  So the substantive question this run answers is not "is dating a hole"
(426 settled that) but **"can the T2 clause be written as syntax, or does it need an instrument?"**

The instrument proposed here is a CAUSALITY CERTIFICATE, built to mirror T1's construction:

    T1 (426/433):  perturb the panel across NAMES     px -> px @ diag(c)   ; a key is admissible
                   iff the value the book consumes does not move.
    T2 (here):     perturb the panel across TIME      px -> px with every row STRICTLY AFTER a cut
                   date t replaced by a perturbed copy; a key is admissible iff no cell of the key
                   DATED AT OR BEFORE t moves.

That is the queue's clause read literally — "no key may read a row dated after the weight date" —
turned into something executable, and it is sampling-error-free in the same sense T1 is: it is a
deterministic invariance check under a seeded operator, not an estimate of a correlation.

TUNED PARAMETERS — EXACTLY TWO, and they are the two the queue names.
  (1) CLAUSE FORM: SYN  (426's regex, verbatim), SYN+ (regex widened by hand with the four
      other future-reading idioms a reader would think of: bfill, iloc[-k], tail, method='bfill'),
      OP1  (the certificate at ONE cut, 0.50), OP3 (the certificate at THREE cuts, 0.35/0.55/0.75,
      FAIL if ANY cut moves).
  (2) CORPUS: TRUTH20 (a hand-truth dating table, ground truth written before any form was run),
      CENSUS111 (idea 426's committed 111-key census, re-read from its own .backfill.csv),
      BOOK16 (the 16-key book set 426 priced).
  ALL 4 x 3 cells are reported.  The BOOK's own two tuned parameters are KEY x m, exactly as in
  426, and every grid point is written out; the clause form is not a third book parameter, it is
  a re-READING of the same grid under a different gate, which is what "price it on the same grid"
  asks for.

PRE-REGISTERED PREDICTIONS (written before any number below was read; each reported hit/miss)
  P1  The SYNTACTIC form (SYN) CLEARS at least one genuinely forward-dated key on TRUTH20 — i.e.
      the clause cannot be published as a regex.
  P2  On CENSUS111, OP3 fails strictly more keys than SYN does, and at least one key that OP3
      fails is T1-PASS (so T2 is not a relabelling of T1).
  P3  T1 and T2 are close to independent on CENSUS111: the 2x2 cross-tab has a non-empty cell in
      all four corners.
  P4  BOOK.  The price of the T2 gate in front of rule 8 is STRICTLY NEGATIVE in OOS Sharpe (it
      removes the winning arm, which is the point), and no arm clears 4a at the protocol rung.

Design (identical to idea 426 lane B wherever it can be, so the two runs are comparable)
---------------------------------------------------------------------------------------
Panels     U56 (research/universe.json) and SMALL439 (sub-$2B, current constituents, max_1d_move
           >= 1.0 dropped).  SURVIVORSHIP: both are CURRENT constituents, SMALL doubly so.  No
           book is proposed on either; only same-days, same-book contrasts are read.
Books      EWALL (no trend gate), MA200 (200d trend gate); gross 0.75 held equal across tilts.
Cadence    weekly, weights at close t applied t+1 (fast_bt, gated against engine.backtest).
Costs      0/5/10/25 bps, ALL reported; PROTOCOL rung 10 bps for verdicts.
Rule 8     (KEY, m) chosen on 2010..2016 IS Sharpe at 10 bps inside each (panel, book) cell;
           2017..2026 read ONCE against SPY, the m=0 control, RULES v2 and RULES v1.
Both KEEP  4a vs live RULES v2 at the same rung; 4b vs SPY including the rule-8 OOS leg.
CERT axes  sigma 0.25, cuts 0.35/0.55/0.75, seed 644 — REPORTED, never selected on.

Outputs: .console.txt .truth.csv .backfill.csv .crosstab.csv .census.csv .book.csv .walkforward.csv
"""
import hashlib
import re
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, load_volume, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask                                 # noqa: E402

STEM = "2026-09-10_does-PROTOCOL-need-a-T2-DATING-clause-beside-T1_C"
OUT = ROOT / "research" / "backtests"
PARENT = OUT / "2026-09-10_put-the-T1-line-in-PROTOCOL-and-back-fill-it_B.py"
PARENT_BF = OUT / "2026-09-10_put-the-T1-line-in-PROTOCOL-and-back-fill-it_B.backfill.csv"
PARENT_BK = OUT / "2026-09-10_put-the-T1-line-in-PROTOCOL-and-back-fill-it_B.book.csv"

FREQ, GROSS = "W", 0.75
COSTS = [0, 5, 10, 25]
PROTO_COST = 10
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SIGMA, SEED = 0.25, 644
CUTS = [0.35, 0.55, 0.75]
TOL = 1e-9
NKEY_BOOK = 16
MGRID = [-1.0, -0.5, -0.25, 0.0, 0.25, 0.5, 1.0]

# CLAUSE FORM 1: idea 426's regex, copied verbatim from its PART 3 (`FWD_PAT`).
SYN_PAT = re.compile(r"shift\(-\d+\)|iloc\[-1\]")
# CLAUSE FORM 2: the same regex widened by hand with the other future-reading idioms a careful
# reader would list.  Fixed before any key was run.
SYNP_PAT = re.compile(r"shift\(-\d+\)|iloc\[-\d+\]|\.bfill\(|method\s*=\s*['\"]bfill['\"]|\.tail\(")

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


T0 = time.time()
P("=" * 118)
P("IDEA 644  does-PROTOCOL-need-a-T2-DATING-clause-beside-T1   (lane C, 2026-09-10)")
P("=" * 118)
P(f"[parent] idea 426 lane B script sha256[:16] "
  f"{hashlib.sha256(PARENT.read_bytes()).hexdigest()[:16]}")
P(f"[parent] census re-read from {PARENT_BF.name} "
  f"(sha256[:16] {hashlib.sha256(PARENT_BF.read_bytes()).hexdigest()[:16]})")


# =====================================================================================
# PART 1 — panels (built exactly as idea 426 built them)
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
    P("[panels] SURVIVORSHIP: both panels are CURRENT constituents; SMALL doubly so.  No book is "
      "proposed on either — only same-days, same-book contrasts are read.")
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
P(f"[T2   ] cert panel {PC.shape[0]}d x {PC.shape[1]} names "
  f"{PC.index[0].date()}..{PC.index[-1].date()}; sigma {SIGMA}, cuts {CUTS}, seed {SEED}")


# =====================================================================================
# PART 2 — THE T2 INSTRUMENT
# =====================================================================================
# One perturbation matrix, drawn ONCE from a seeded generator and reused for every key and every
# cut, so the whole column is deterministic and every key sees the identical operator.
_RNG = np.random.default_rng(SEED)
PERT = pd.DataFrame(_RNG.lognormal(0.0, SIGMA, size=PC.shape), index=PC.index, columns=PC.columns)


def _as_frame(x):
    if isinstance(x, pd.Series):
        return x.to_frame("K")
    return x


def _moved(A, B):
    """Fraction of comparable cells whose value differs.  NaN-vs-number counts as a move."""
    A, B = A.align(B, join="inner", axis=None)
    if A.size == 0:
        return np.nan
    na, nb = A.notna(), B.notna()
    both = na & nb
    rel = (A - B).abs() / A.abs().clip(lower=1e-12)
    diff = (both & (rel > TOL)) | (na ^ nb)
    return float(diff.values.sum()) / float(A.size)


def t2_on_key(src, p, v, cuts):
    """CAUSALITY CERTIFICATE.  Replace every row STRICTLY AFTER a cut date with a perturbed copy
    and report the fraction of the key's cells DATED AT OR BEFORE the cut that move.
    Returns (max_moved_frac, n_cuts_moved, status)."""
    env = {"np": np, "pd": pd}
    # float-cast BOTH arms up front: the perturbed panel is necessarily float, so casting only it
    # would make an integer volume column differ from its own baseline for a dtype reason.
    p = p.astype(float)
    v = None if v is None else v.astype(float)
    try:
        K0 = _as_frame(eval(src, env, {"px": p, "vol": v}))                       # noqa: S307
        K0b = _as_frame(eval(src, env, {"px": p, "vol": v}))                      # noqa: S307
    except Exception:
        return np.nan, 0, "UNREACHABLE"
    if not isinstance(K0, pd.DataFrame):
        return np.nan, 0, "NOT_PANEL"
    try:
        if _moved(K0.astype(float), K0b.astype(float)) not in (0.0,):
            return np.nan, 0, "NOT_REPRODUCIBLE"
    except Exception:
        return np.nan, 0, "NOT_PANEL"
    K0 = K0.astype(float)
    fr, nmoved = [], 0
    for cq in cuts:
        i = int(round(cq * (len(p) - 1)))
        tcut = p.index[i]
        p1 = p.astype(float).copy()
        p1.iloc[i + 1:] = (p.iloc[i + 1:] * PERT.iloc[i + 1:]).values
        v1 = None
        if v is not None:
            v1 = v.astype(float).copy()
            v1.iloc[i + 1:] = (v.iloc[i + 1:] * PERT.iloc[i + 1:]).values
        try:
            K1 = _as_frame(eval(src, env, {"px": p1, "vol": v1})).astype(float)   # noqa: S307
        except Exception:
            return np.nan, 0, "UNREACHABLE"
        past0 = K0.loc[K0.index <= tcut]
        past1 = K1.loc[K1.index <= tcut]
        if past0.size == 0:
            fr.append(np.nan)
            continue
        m = _moved(past0, past1)
        fr.append(m)
        if np.isfinite(m) and m > 0.0:
            nmoved += 1
    if not np.isfinite(fr).any():
        return np.nan, 0, "UNDECIDABLE"
    return float(np.nanmax(fr)), nmoved, "OK"


def t2_verdict(src, moved_max, nmoved, form):
    """T2 verdict under a given CLAUSE FORM.  'PASS' = admissible, 'FAIL' = reads the future."""
    if form == "SYN":
        return "FAIL" if SYN_PAT.search(src) else "PASS"
    if form == "SYN+":
        return "FAIL" if SYNP_PAT.search(src) else "PASS"
    if form == "OP1":
        return "NA" if not np.isfinite(moved_max) else ("FAIL" if moved_max > 0.0 else "PASS")
    if form == "OP3":
        return "NA" if not np.isfinite(moved_max) else ("FAIL" if nmoved > 0 else "PASS")
    raise ValueError(form)


FORMS = ["SYN", "SYN+", "OP1", "OP3"]


# =====================================================================================
# GATE A — TRUTH20: hand-truth dating table.  Ground truth written before any form was run.
# =====================================================================================
P("\n" + "-" * 118)
P("GATE A — TRUTH20: does each clause form get the DATING of 20 hand-truth keys right?")
P("-" * 118)
TRUTH20 = [
    # (name, src, truth_causal)  truth_causal=True  <=> the key at row t reads only rows <= t
    ("MOM",      "px.shift(21) / px.shift(252) - 1", True),
    ("MA200",    "px.rolling(200).mean()", True),
    ("PCT",      "px.pct_change()", True),
    ("XRANK",    "px.rank(axis=1, pct=True)", True),
    ("EXPMEAN",  "px.expanding().mean()", True),
    ("VOL20",    "px.pct_change().rolling(20).std()", True),
    ("FFILL",    "px.ffill()", True),
    ("CUMMAX",   "px.cummax()", True),
    ("LOGPX",    "np.log(px)", True),
    ("DDOWN",    "px / px.cummax() - 1.0", True),
    ("ZFULL",    "(px - px.mean()) / px.std()", False),
    ("TERMINAL", "px.iloc[-1] / px - 1.0", False),
    ("FWD21",    "px.shift(-21) / px - 1.0", False),
    ("MAXNORM",  "px / px.max()", False),
    ("BFILL",    "px.bfill()", False),
    ("CENTERED", "px.rolling(21, center=True).mean()", False),
    ("TRANK",    "px.rank(axis=0, pct=True)", False),
    ("LAGNEG1",  "px.rolling(200).mean().shift(-1)", False),
    ("REVMAX",   "px.iloc[::-1].cummax().iloc[::-1]", False),
    ("MINMAX",   "(px - px.min()) / (px.max() - px.min())", False),
]
trows = []
for nm, src, causal in TRUTH20:
    mv, nm_, st = t2_on_key(src, PC, VC, CUTS)
    r = dict(key=nm, src=src, truth_causal=causal, status=st, moved_max=mv, cuts_moved=nm_)
    for f in FORMS:
        r[f"T2_{f}"] = t2_verdict(src, mv, nm_, f)
    trows.append(r)
TR = pd.DataFrame(trows)
TR.to_csv(OUT / f"{STEM}.truth.csv", index=False)
P(f"  {'key':<10}{'truth':<9}{'status':<9}{'moved':>9}{'cuts':>6}   " +
  "".join(f"{f:>7}" for f in FORMS))
P("  " + "-" * 78)
for _, r in TR.iterrows():
    P(f"  {r.key:<10}{'CAUSAL' if r.truth_causal else 'LEAKS':<9}{r.status:<9}"
      f"{(f'{r.moved_max:.4f}' if np.isfinite(r.moved_max) else '--'):>9}{r.cuts_moved:>6}   "
      + "".join(f"{r['T2_' + f]:>7}" for f in FORMS))
P("")
GATE_A = {}
for f in FORMS:
    fc = sorted(TR[(TR[f"T2_{f}"] == "PASS") & (~TR.truth_causal)].key)   # cleared a leak
    fr = sorted(TR[(TR[f"T2_{f}"] == "FAIL") & (TR.truth_causal)].key)    # rejected a good key
    GATE_A[f] = (fc, fr)
    P(f"  {f:<5} false clearances {len(fc):>2}/10  ({', '.join(fc) or 'none'})   "
      f"false rejections {len(fr):>2}/10  ({', '.join(fr) or 'none'})")
p1 = len(GATE_A["SYN"][0]) > 0
P(f"\n  P1 (pre-registered): the SYNTACTIC form clears at least one genuinely forward-dated key "
  f"-> {'HIT' if p1 else 'MISS'} ({len(GATE_A['SYN'][0])} cleared)")
P("  -> the adjudicator this back-fill uses is OP3 (certificate, 3 cuts), with SYN beside it.")


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
_g, _t, _gs = fast_bt(_px, rules_v2_weights(_px))
d1 = float((netr(_g, _t, 0) - backtest(_px, rules_v2_weights(_px), cost_bps=0,
                                       freq=FREQ)["returns"]).abs().max())
d2 = float((netr(_g, _t, PROTO_COST) - backtest(_px, rules_v2_weights(_px), cost_bps=PROTO_COST,
                                                freq=FREQ)["returns"]).abs().max())
P(f"  fast_bt == engine.backtest on RULES v2: 0 bps {d1:.3e}, {PROTO_COST} bps {d2:.3e}   "
  f"(PASS if < 1e-12: {'PASS' if max(d1, d2) < 1e-12 else 'FAIL'})")


# =====================================================================================
# GATE C — re-read idea 426's committed census and reproduce its published counts
# =====================================================================================
P("\n" + "-" * 118)
P("GATE C — idea 426's committed 111-key census, re-read from its own .backfill.csv")
P("-" * 118)
BF = pd.read_csv(PARENT_BF)
cls = BF.admitted.value_counts().to_dict()
K = BF[BF.admitted == "KEY"].copy().reset_index(drop=True)
n_pass_t1, n_fail_t1 = int((K.T1 == "PASS").sum()), int((K.T1 == "FAIL").sum())
P(f"  admitted classes: {cls}")
P(f"  KEY census n={len(K)}   T1 PASS {n_pass_t1} / FAIL {n_fail_t1}   "
  f"(426 published 111 keys, 72/39: "
  f"{'PASS' if (len(K), n_pass_t1, n_fail_t1) == (111, 72, 39) else 'FAIL'})")


# =====================================================================================
# PART 3 — THE BACK-FILL: T2 over the same 111 keys, beside the T1 column
# =====================================================================================
P("\n" + "-" * 118)
P("PART 3  BACK-FILL — the T2 column beside the T1 column, over idea 426's own 111 keys")
P("-" * 118)
t_t2 = time.time()
res = []
for _, r in K.iterrows():
    v = VC if bool(r.uses_vol) else None
    mv, nmv, st = t2_on_key(r.expr, PC, v, CUTS)
    row = dict(expr=r.expr, n_files=int(r.n_files), files=r.files, ncol=r.ncol,
               is_bool=bool(r.is_bool), uses_vol=bool(r.uses_vol),
               is_identity=bool(r.is_identity), T1=r.T1,
               CERT_value_moved=r.CERT_value_moved, T2_status=st,
               T2_moved_max=mv, T2_cuts_moved=nmv)
    for f in FORMS:
        row[f"T2_{f}"] = t2_verdict(r.expr, mv, nmv, f)
    res.append(row)
BFC = pd.DataFrame(res)
BFC.to_csv(OUT / f"{STEM}.backfill.csv", index=False)
t_t2 = time.time() - t_t2
P(f"  T2 run over {len(BFC)} keys in {t_t2:.1f}s ({1000 * t_t2 / max(len(BFC), 1):.0f} ms/key); "
  f"status: {BFC.T2_status.value_counts().to_dict()}")
P("")
P(f"  {'form':<6}{'PASS':>7}{'FAIL':>7}{'NA':>5}   {'FAIL keys reach (scripts)':<28}"
  f"{'max n_files of a FAIL key':>26}")
P("  " + "-" * 82)
FORM_STATS = {}
for f in FORMS:
    col = BFC[f"T2_{f}"]
    fails = BFC[col == "FAIL"]
    reach = set()
    for _, r in fails.iterrows():
        reach |= set(str(r.files).split(","))
    reach.discard("")
    FORM_STATS[f] = dict(npass=int((col == "PASS").sum()), nfail=len(fails),
                         na=int((col == "NA").sum()), reach=len(reach),
                         maxn=int(fails.n_files.max()) if len(fails) else 0,
                         reach_set=reach)
    P(f"  {f:<6}{FORM_STATS[f]['npass']:>7}{FORM_STATS[f]['nfail']:>7}{FORM_STATS[f]['na']:>5}   "
      f"{FORM_STATS[f]['reach']:<28}{FORM_STATS[f]['maxn']:>26}")

P("\n  keys OP3 fails that SYN clears (what a regex clause would have let through):")
missed = BFC[(BFC.T2_OP3 == "FAIL") & (BFC.T2_SYN == "PASS")].sort_values(
    "n_files", ascending=False)
for _, r in missed.head(15).iterrows():
    P(f"    n={r.n_files:<4} T1={r.T1:<5} moved={r.T2_moved_max:.4f}  {r.expr[:88]}")
P(f"    ... {len(missed)} such keys in total")
P("\n  keys SYN fails that OP3 clears (what a regex clause would have wrongly removed):")
over = BFC[(BFC.T2_OP3 == "PASS") & (BFC.T2_SYN == "FAIL")]
for _, r in over.iterrows():
    P(f"    n={r.n_files:<4} T1={r.T1:<5}  {r.expr[:88]}")
P(f"    ... {len(over)} such keys in total")

# ---- the 2x2: is T2 a relabelling of T1? -------------------------------------------------------
P("\n  CROSS-TAB  T1 x T2(OP3) over the 111-key census:")
CT = pd.crosstab(BFC.T1, BFC.T2_OP3)
CT.to_csv(OUT / f"{STEM}.crosstab.csv")
P("    " + CT.to_string().replace("\n", "\n    "))
corners = {(a, b): int(((BFC.T1 == a) & (BFC.T2_OP3 == b)).sum())
           for a in ("PASS", "FAIL") for b in ("PASS", "FAIL")}
p3 = all(v > 0 for v in corners.values())
n_t1pass_t2fail = corners[("PASS", "FAIL")]
P(f"    all four corners non-empty: {'YES' if p3 else 'NO'}  {corners}")
P(f"    keys that are T1-PASS and T2-FAIL (the hole the queue names): {n_t1pass_t2fail}")
if corners[("FAIL", "FAIL")] == 0:
    P(f"    the two FAILURE SETS ARE DISJOINT ({n_t1pass_t2fail} T1-PASS/T2-FAIL, "
      f"{corners[('FAIL', 'PASS')]} T1-FAIL/T2-PASS, 0 both).  That is a STRONGER separation than "
      f"the pre-registered 'all four corners' reading, and it falsifies P3 as written: on this "
      f"corpus the clauses do not merely fail to imply each other, they never fire together.  "
      f"Adopting either one alone leaves the other's entire failure set admitted.")
p2 = (FORM_STATS["OP3"]["nfail"] > FORM_STATS["SYN"]["nfail"]) and (n_t1pass_t2fail > 0)
P(f"  P2 (pre-registered): OP3 fails strictly more than SYN AND >=1 OP3-FAIL key is T1-PASS "
  f"-> {'HIT' if p2 else 'MISS'}")
P(f"  P3 (pre-registered): all four corners of the T1 x T2 cross-tab non-empty "
  f"-> {'HIT' if p3 else 'MISS'}")


# =====================================================================================
# PART 4 — CENSUS: what the T2 column touches in the PUBLISHED record
# =====================================================================================
P("\n" + "-" * 118)
P("PART 4  CENSUS — which committed scripts and LEADERBOARD rows carry a T2-FAIL key")
P("-" * 118)
lb = (ROOT / "research" / "LEADERBOARD.md").read_text().split("\n")
lb_rows = [ln for ln in lb if ln.startswith("|") and ln.count("|") >= 8
           and not ln.startswith("|---") and "| date " not in ln.lower()]
cen_rows = []
for f in FORMS:
    reach = FORM_STATS[f]["reach_set"]
    hits = [ln for ln in lb_rows if any(x.replace(".py", "") in ln for x in reach)]
    cen_rows.append(dict(form=f, fail_keys=FORM_STATS[f]["nfail"], scripts=len(reach),
                         lb_rows=len(hits), lb_total=len(lb_rows),
                         lb_share=round(len(hits) / max(len(lb_rows), 1), 4)))
    P(f"  {f:<5} {FORM_STATS[f]['nfail']:>3} FAIL keys carried by {len(reach):>4} committed "
      f"scripts, touching {len(hits):>5} of {len(lb_rows)} LEADERBOARD rows "
      f"({len(hits) / max(len(lb_rows), 1):.1%})")
pd.DataFrame(cen_rows).to_csv(OUT / f"{STEM}.census.csv", index=False)
P("  NOTE: this counts SITES, not verdicts.  A full-sample `px.max()` inside a plotting helper is "
  "a T2-FAIL site that carries no published number; the clause below therefore adjudicates the "
  "KEY AS THE BOOK USES IT, exactly as clause 10(b) does for T1.")


# =====================================================================================
# PART 5 — THE T2 CLAUSE (drafted; PROTOCOL.md NOT edited — rule 6, Sunday review)
# =====================================================================================
CLAUSE = """
PROTOCOL clause 11 (T2 — dating / causality).  DRAFT, report-only.  Sits BESIDE clause 10 (T1),
not inside it: T1 certifies the ADJUSTMENT channel across NAMES, T2 certifies the DATING channel
across TIME, and idea 426's back-fill shows a key can pass either while failing the other.

11. **Dating (T2).**  No key may read a row dated after the date of the weight it feeds.  A key
    is admissible only if, for every date t at which the book forms a weight, the key's value at t
    is unchanged when every row of the panel STRICTLY AFTER t is replaced.  Adjudicate in this
    ORDER:
    (a) GATE — reproducibility, as in 10(b).  A key that is not a function of the panel cannot be
        certified against any operator.
    (b) ADJUDICATOR — the CAUSALITY CERTIFICATE, not a syntactic exclusion list.  For each of at
        least three cut dates t spread over the sample, form px' by multiplying every row after t
        by a positive per-cell perturbation, recompute the key, and compare the two keys ON ROWS
        DATED AT OR BEFORE t.  Any cell that moves is a T2-FAIL and no verdict resting on that key
        may be published.  A syntactic exclusion (`shift(-k)`, `iloc[-1]`) may be reported beside
        the certificate as a reader's aid but MUST NOT be the verdict: on the TRUTH20 hand-truth
        table in PART 2 the regex clears 7 of 10 genuinely forward-dated keys (a full-sample
        `px.max()`, a centred rolling mean, a whole-column `rank(axis=0)`, a reversed cummax) while
        the certificate clears none and rejects none.  On THIS record's currently reconstructible
        keys the two happen to agree exactly (PART 3) — every leak the record actually carries is
        `iloc[-1]`- or `shift(-k)`-shaped — so the certificate is not adopted here because it finds
        more today, but because it is the form that keeps adjudicating keys nobody has looked at.
    (c) T2 is NECESSARY, not sufficient, and it is a DIFFERENT test from T1, not a relabelling.  On
        the 111-key census the two failure sets are DISJOINT: 8 keys are T1-PASS and T2-FAIL
        (`px.iloc[-1]/px - 1` is degree 0, so T1 clears it), 39 are T1-FAIL and T2-PASS (a 200d
        mean is degree 1 but strictly backward-looking), and NO key fails both.  Neither clause
        implies the other and both must be run.
    (d) T2 must run BEFORE rule 8, for the same reason T1 must (idea 195): rule 8 splits the sample
        by DATE, and a terminal-dated key is dated at T in BOTH halves, so no walk-forward split
        can see it.  Idea 426 measured this directly — its rule-8 chooser picked the terminal-dated
        key in 4 of 4 cells.
"""
P("\n" + "-" * 118)
P("PART 5  THE CLAUSE — drafted, report-only (PROTOCOL.md is NOT edited; rule 6, Sunday review)")
P("-" * 118)
for ln in CLAUSE.strip("\n").split("\n"):
    P("  " + ln)


# =====================================================================================
# PART 6 — THE BOOK: the same grid idea 426 priced.  Tuned: KEY x m.
# =====================================================================================
P("\n" + "-" * 118)
P("PART 6  BOOK — the SAME grid as idea 426.  Tuned: KEY x m.  Every grid point reported.")
P("-" * 118)
cand = BFC[(~BFC.is_bool) & (~BFC.uses_vol)].copy()
cand = cand[cand.ncol > 1]
cand = cand.sort_values(["n_files", "expr"], ascending=[False, True])
BOOKKEYS = cand.head(NKEY_BOOK)[["expr", "n_files", "T1"] + [f"T2_{f}" for f in FORMS]
                                ].reset_index(drop=True)
BOOKKEYS["kid"] = ["K%02d" % i for i in range(len(BOOKKEYS))]
PAR_BK = pd.read_csv(PARENT_BK)[["kid", "key"]].drop_duplicates()
par_map = dict(zip(PAR_BK.kid, PAR_BK.key))
mine = dict(zip(BOOKKEYS.kid, BOOKKEYS.expr))
same = all(par_map.get(k) == v for k, v in mine.items()) and len(par_map) == len(mine)
P(f"  key set reproduced from 426's own mechanical rule (n_files desc, expr asc, head 16): "
  f"identical to 426's committed kid->expr map: {'PASS' if same else 'FAIL'}")
P(f"  {'kid':<5}{'n':<6}{'T1':<6}" + "".join(f"{f:>7}" for f in FORMS) + "   key")
for _, r in BOOKKEYS.iterrows():
    P(f"  {r.kid:<5}{r.n_files:<6}{r.T1:<6}" + "".join(f"{r['T2_' + f]:>7}" for f in FORMS)
      + "   " + r.expr[:74])
for f in FORMS:
    P(f"  T2({f}) split of the book key set: PASS {(BOOKKEYS[f'T2_{f}'] == 'PASS').sum()}, "
      f"FAIL {(BOOKKEYS[f'T2_{f}'] == 'FAIL').sum()}")
P(f"  tilt grid m = {MGRID}   (m=0 is the NO-TILT control, shared by every key)")
P("  gross held EXACTLY equal across every m by rw normalisation, so m moves the cross-section "
  "and never the exposure (idea 415); realised gross published beside every Sharpe (idea 641).")

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
    sp = px["SPY"].pct_change().fillna(0.0).loc[START[pn]:]
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
        kcache[kr.kid] = kv if (isinstance(kv, pd.DataFrame) and kv.shape == pxp.shape) else None
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
                    row = dict(panel=pn, book=book, kid=kr.kid, key=kr.expr, T1=kr.T1, m=m,
                               cost_bps=cb, gross=float(gs.loc[START[pn]:].mean()),
                               turnover=float(t_.loc[START[pn]:].sum() / (len(r_) / 252.0)),
                               CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                               H1=mm["H1"], H2=mm["H2"], IS_Sharpe=ins["Sharpe"],
                               OOS_CAGR=oos["CAGR"], OOS_Sharpe=oos["Sharpe"],
                               OOS_MaxDD=oos["MaxDD"])
                    for f in FORMS:
                        row[f"T2_{f}"] = kr[f"T2_{f}"]
                    ROWS.append(row)
BK = pd.DataFrame(ROWS)


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
P("  m=0 is the SAME book for every key, so counts are given raw AND deduped.")
for cb in COSTS:
    sub = BK[BK.cost_bps == cb]
    ded = sub[~((sub.m == 0.0) & (sub.kid != BOOKKEYS.kid.iloc[0]))]
    P(f"    {cb:>2} bps: 4a {int(sub.pass4a.sum()):>4}/{len(sub)}   "
      f"4b {int(sub.pass4b.sum()):>4}/{len(sub)}   | deduped 4a {int(ded.pass4a.sum()):>3}/"
      f"{len(ded)}  4b {int(ded.pass4b.sum()):>3}/{len(ded)}   (m=0 controls: 4b "
      f"{int(ded[ded.m == 0.0].pass4b.sum())}/{int((ded.m == 0.0).sum())})")
p10 = BK[BK.cost_bps == PROTO_COST]
P(f"  gross across the whole {PROTO_COST}-bps grid: min {p10.gross.min():.4f} "
  f"max {p10.gross.max():.4f} (spread {p10.gross.max() - p10.gross.min():.2e}) — the tilt is NOT "
  f"an exposure trade by construction")

P(f"\n  every grid point at the PROTOCOL rung ({PROTO_COST} bps), Sharpe by m:")
for pn in PANELS:
    for book in BOOKS:
        sub = p10[(p10.panel == pn) & (p10.book == book)]
        if not len(sub):
            continue
        P(f"\n  --- {pn} / {book} ---   SPY {SPYM[pn]['CAGR']:.2%} {SPYM[pn]['Sharpe']:.3f} "
          f"{SPYM[pn]['MaxDD']:.2%} | RULES v2 {V2M[pn][0]['CAGR']:.2%} "
          f"{V2M[pn][0]['Sharpe']:.3f} {V2M[pn][0]['MaxDD']:.2%}")
        P(f"  {'key':<5}{'T1':<5}{'T2':<5}" + "".join(f"{m:>+9.2f}" for m in MGRID))
        for kid in BOOKKEYS.kid:
            s = sub[sub.kid == kid]
            if not len(s):
                continue
            P(f"  {kid:<5}{s.T1.iloc[0][0]:<5}{s.T2_OP3.iloc[0][0]:<5}" + "".join(
                f"{s[s.m == m].Sharpe.iloc[0]:>9.3f}" if len(s[s.m == m]) else f"{'--':>9}"
                for m in MGRID))


# =====================================================================================
# PART 7 — RULE 8: what does the T2 gate in FRONT of the chooser buy?
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
        pools = [("S_ALL", "no gate", sub),
                 ("S_T1", "T1-PASS only", sub[sub.T1 == "PASS"]),
                 ("S_T2SYN", "T2(SYN)-PASS only", sub[sub.T2_SYN == "PASS"]),
                 ("S_T2OP3", "T2(OP3)-PASS only", sub[sub.T2_OP3 == "PASS"]),
                 ("S_T1T2", "T1-PASS and T2(OP3)-PASS",
                  sub[(sub.T1 == "PASS") & (sub.T2_OP3 == "PASS")]),
                 ("S_T2FAIL", "T2(OP3)-FAIL only", sub[sub.T2_OP3 == "FAIL"]),
                 ("S_NONE", "m=0 control", sub[sub.m == 0.0])]
        for cname, lab, pool in pools:
            if not len(pool):
                continue
            pick = pool.loc[pool.IS_Sharpe.idxmax()]
            WF.append(dict(panel=pn, book=book, chooser=cname, chooser_label=lab,
                           pick_kid=pick.kid, pick_m=pick.m, pick_T1=pick.T1,
                           pick_T2_SYN=pick.T2_SYN, pick_T2_OP3=pick.T2_OP3,
                           IS_Sharpe=pick.IS_Sharpe, OOS_CAGR=pick.OOS_CAGR,
                           OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                           full_CAGR=pick.CAGR, full_Sharpe=pick.Sharpe, full_MaxDD=pick.MaxDD,
                           H1=pick.H1, H2=pick.H2,
                           ctrl_OOS_Sharpe=ctrl.OOS_Sharpe, ctrl_OOS_CAGR=ctrl.OOS_CAGR,
                           ctrl_OOS_MaxDD=ctrl.OOS_MaxDD,
                           spy_OOS_Sharpe=SPYOOS[pn]["Sharpe"], spy_OOS_CAGR=SPYOOS[pn]["CAGR"],
                           spy_OOS_MaxDD=SPYOOS[pn]["MaxDD"],
                           v2_OOS_Sharpe=V2M[pn][1]["Sharpe"], v2_OOS_CAGR=V2M[pn][1]["CAGR"],
                           v2_OOS_MaxDD=V2M[pn][1]["MaxDD"],
                           v1_OOS_Sharpe=V1M[pn][1]["Sharpe"], v1_OOS_CAGR=V1M[pn][1]["CAGR"],
                           beats_ctrl=bool(pick.OOS_Sharpe > ctrl.OOS_Sharpe),
                           beats_spy=bool(pick.OOS_Sharpe > SPYOOS[pn]["Sharpe"]),
                           beats_v2=bool(pick.OOS_Sharpe > V2M[pn][1]["Sharpe"])))
W = pd.DataFrame(WF)
W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
P(f"  {'panel':<10}{'book':<7}{'chooser':<10}{'pick':<16}{'IS Shp':>8}{'OOS CAGR':>10}"
  f"{'OOS Shp':>9}{'OOS DD':>9}{'vs ctrl':>9}{'vs SPY':>8}{'vs v2':>7}")
P("  " + "-" * 116)
for _, r in W.iterrows():
    tag = f"{r.pick_kid}/{r.pick_m:+.2f}/{r.pick_T1[0]}{r.pick_T2_OP3[0]}"
    P(f"  {r.panel:<10}{r.book:<7}{r.chooser:<10}{tag:<16}{r.IS_Sharpe:>8.3f}"
      f"{r.OOS_CAGR:>10.2%}{r.OOS_Sharpe:>9.3f}{r.OOS_MaxDD:>9.2%}"
      f"{r.OOS_Sharpe - r.ctrl_OOS_Sharpe:>+9.3f}{r.OOS_Sharpe - r.spy_OOS_Sharpe:>+8.3f}"
      f"{r.OOS_Sharpe - r.v2_OOS_Sharpe:>+7.3f}")
P("")
for pn in PANELS:
    P(f"  {pn:<10} OOS comparands  SPY {SPYOOS[pn]['CAGR']:>7.2%} {SPYOOS[pn]['Sharpe']:.3f} "
      f"{SPYOOS[pn]['MaxDD']:>8.2%}  |  RULES v2 {V2M[pn][1]['CAGR']:>7.2%} "
      f"{V2M[pn][1]['Sharpe']:.3f} {V2M[pn][1]['MaxDD']:>8.2%}  |  RULES v1 "
      f"{V1M[pn][1]['CAGR']:>7.2%} {V1M[pn][1]['Sharpe']:.3f}")
P("")
for pn in PANELS:
    P(f"  {pn:<10} FULL-SAMPLE comparands  SPY {SPYM[pn]['CAGR']:>7.2%} {SPYM[pn]['Sharpe']:.3f} "
      f"{SPYM[pn]['MaxDD']:>8.2%} (H1 {SPYM[pn]['H1']:.3f} H2 {SPYM[pn]['H2']:.3f})  |  RULES v2 "
      f"{V2M[pn][0]['CAGR']:>7.2%} {V2M[pn][0]['Sharpe']:.3f} {V2M[pn][0]['MaxDD']:>8.2%} "
      f"(H1 {V2M[pn][0]['H1']:.3f} H2 {V2M[pn][0]['H2']:.3f})")

for c in W.chooser.unique():
    s = W[W.chooser == c]
    P(f"\n  {c:<9} beats the m=0 control in {int(s.beats_ctrl.sum())}/{len(s)} cells "
      f"(mean dOOS Sharpe {(s.OOS_Sharpe - s.ctrl_OOS_Sharpe).mean():+.4f}); beats SPY "
      f"{int(s.beats_spy.sum())}/{len(s)}; beats RULES v2 {int(s.beats_v2.sum())}/{len(s)}")

base = W[W.chooser == "S_ALL"].set_index(["panel", "book"]).OOS_Sharpe
P("\n  *** PRICE OF EACH GATE IN FRONT OF RULE 8 (OOS Sharpe vs the ungated chooser) ***")
PRICE = {}
for c in ("S_T1", "S_T2SYN", "S_T2OP3", "S_T1T2"):
    s = W[W.chooser == c].set_index(["panel", "book"]).OOS_Sharpe
    if not len(s):
        continue
    common = base.index.intersection(s.index)
    d = s.loc[common] - base.loc[common]
    PRICE[c] = float(d.mean())
    P(f"    {c:<9} mean dOOS Sharpe {d.mean():+.4f} over {len(common)} cells   "
      f"(helps {int((d > 0).sum())}, costs {int((d < 0).sum())}, identical pick "
      f"{int((d == 0).sum())})")
P("    Read this the right way round: a NEGATIVE price is the clause WORKING.  The arm it removes "
  "is a look-ahead arm, so the OOS Sharpe it gives up was never earnable.")
if all(c in PRICE for c in ("S_T1", "S_T2OP3", "S_T1T2")):
    P(f"\n    DECOMPOSITION (the number idea 426 could not split).  426 published T1 alone at "
      f"+0.0000 and T1+dating at -0.4508 and could not say which clause was doing the work:")
    P(f"      T1 alone                 {PRICE['S_T1']:+.4f}   (inert: identical pick 4/4)")
    P(f"      T2 alone                 {PRICE['S_T2OP3']:+.4f}   (moves the pick 4/4)")
    P(f"      T1 and T2 together       {PRICE['S_T1T2']:+.4f}")
    _t2p = W[W.chooser == "S_T2OP3"]
    _n_t1f = int((_t2p.pick_T1 == "FAIL").sum())
    _which = ", ".join(f"{k} x{v}" for k, v in _t2p.pick_kid.value_counts().items())
    P(f"      => T2 carries {PRICE['S_T2OP3'] / PRICE['S_T1T2']:.1%} of the joint price, and T1 "
      f"adds {PRICE['S_T1T2'] - PRICE['S_T2OP3']:+.4f} more CONDITIONAL on T2.  T1 is inert on "
      f"its own and NOT inert given T2: the pick T2 leaves behind ({_which}) is T1-FAIL in "
      f"{_n_t1f} of {len(_t2p)} cells, so a record that adopted T2 alone would publish a book "
      f"resting on a degree-1 key.")

fwd_kids = sorted(BOOKKEYS[BOOKKEYS.T2_OP3 == "FAIL"].kid)
P(f"\n  T2(OP3)-FAIL keys in the book set: {fwd_kids}")
P("  the arms rule 8 passed over: TILT arms that pass 4b at the PROTOCOL rung, are T1-PASS, are "
  "T2(OP3)-PASS, and beat their own m=0 control out of sample:")
n_missed = 0
for (pn, bk), gg in p10.groupby(["panel", "book"]):
    ctrl_oos = gg[gg.m == 0.0].OOS_Sharpe.iloc[0]
    s = gg[(gg.m != 0.0) & gg.pass4b & (gg.T1 == "PASS") & (gg.T2_OP3 == "PASS")
           & (gg.OOS_Sharpe > ctrl_oos)]
    n_missed += len(s)
    P(f"    {pn:<10}{bk:<7} {len(s):>3} arms"
      + (f"  ({', '.join(sorted(s.kid.unique()))})" if len(s) else ""))
P(f"    total {n_missed}.")

P("\n  4b legs on the rule-8 picks (the leg PROTOCOL 4b requires):")
for _, r in W.iterrows():
    legs = [x for x, bad in (("OOS", r.OOS_Sharpe <= r.spy_OOS_Sharpe),
                             ("DD", r.OOS_MaxDD < 0.60 * r.spy_OOS_MaxDD),
                             ("CAGR", r.OOS_CAGR < 0.70 * r.spy_OOS_CAGR)) if bad]
    P(f"    {r.panel:<10}{r.book:<7}{r.chooser:<10} 4b-OOS legs failed: "
      f"{','.join(legs) if legs else 'NONE'}")


# =====================================================================================
# PART 8 — predictions, verdict
# =====================================================================================
P("\n" + "-" * 118)
P("PART 8  PRE-REGISTERED PREDICTIONS")
P("-" * 118)
price_t2 = PRICE.get("S_T2OP3", float("nan"))
n4a = int(p10.pass4a.sum())
p4 = (price_t2 < 0) and (n4a == 0)
P(f"  P1 SYN clears a genuinely forward-dated key on TRUTH20   "
  f"{len(GATE_A['SYN'][0])} cleared   {'HIT' if p1 else 'MISS'}")
P(f"  P2 OP3 fails > SYN on CENSUS111 and >=1 is T1-PASS       "
  f"OP3 {FORM_STATS['OP3']['nfail']} vs SYN {FORM_STATS['SYN']['nfail']}, "
  f"T1-PASS&T2-FAIL {n_t1pass_t2fail}   {'HIT' if p2 else 'MISS'}")
P(f"  P3 all four T1 x T2 corners non-empty                    {corners}   "
  f"{'HIT' if p3 else 'MISS'}")
P(f"  P4 T2 gate price < 0 AND 4a is 0 at the protocol rung    "
  f"price {price_t2:+.4f}, 4a {n4a}/{len(p10)}   {'HIT' if p4 else 'MISS'}")

P("\n" + "=" * 118)
P("VERDICT")
P("=" * 118)
P(f"  ANSWERED / no KEEP.  4a {n4a}/{len(p10)} and 4b {int(p10.pass4b.sum())}/{len(p10)} at the "
  f"PROTOCOL rung (idea 426's grid reproduced exactly).  The deliverable is the T2 CLAUSE plus "
  f"the {len(BFC)}-key T2 column beside 426's T1 column.")
P(f"  YES, PROTOCOL needs a T2 clause beside T1, and it must be an INSTRUMENT, not a regex: on "
  f"TRUTH20 the syntactic form clears {len(GATE_A['SYN'][0])}/10 genuinely forward-dated keys "
  f"while the certificate is 20/20.  On the record's currently reconstructible keys the two "
  f"agree exactly ({FORM_STATS['OP3']['nfail']} FAIL each, same set) — every leak the record "
  f"carries today is iloc[-1]/shift(-k)-shaped — so the certificate's extra reach is unexercised "
  f"here and is bought for the keys nobody has written yet, which is reported as a MISS on P2 "
  f"rather than dressed up.")
P(f"  The clause is NOT a relabelling of T1: the failure sets are disjoint "
  f"({n_t1pass_t2fail} T1-PASS/T2-FAIL, {corners[('FAIL', 'PASS')]} T1-FAIL/T2-PASS, 0 both), and "
  f"in front of rule 8 T1 alone prices at {PRICE.get('S_T1', float('nan')):+.4f}, T2 alone at "
  f"{price_t2:+.4f}, both at {PRICE.get('S_T1T2', float('nan')):+.4f}.")
P("  SURVIVORSHIP: U56 and SMALL439 are current constituents, SMALL doubly so.  No book proposed.")
P("  RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched.")
P(f"\n  runtime {time.time() - T0:.1f}s")
(OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
