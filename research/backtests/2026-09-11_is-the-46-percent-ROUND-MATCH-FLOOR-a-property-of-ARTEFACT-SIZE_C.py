#!/usr/bin/env python3
"""Idea 792 — is the 46% ROUND-MATCH FLOOR a property of ARTEFACT SIZE?

Idea 790's G4 calibration read PLANT-FALSE at 46.0%: a random 4-dp token of the right
shape lands within its own rounding tolerance of SOME committed value about half the
time.  790 read that as one pooled number.  This run measures the floor as a surface
over the two dials that can move it —

    P1  precision      d = decimals the token is quoted at, ladder {1,2,3,4,5,6}
    P2  artefact size  n = distinct numeric values a run's committed DATA artefacts hold,
                       bucketed into quintiles

— and publishes the minimum decimal places at which a re-verification claim is worth
making, per size bucket.  Exactly two tuned parameters (the ladder and the bucketing);
all 6 x 5 = 30 grid points are reported.

MECHANISM.  Idea 790's verifier (`verify_tokens`) calls a token verified when the token
string is present verbatim, OR some committed value v satisfies |q-v| <= tol for q in
{token, token/100, token*100}, with tol = 0.5 * 10^-d.  For a token drawn uniformly on
the run's own [p1, p99] value range that is a covering problem, so the false-match rate
has a CLOSED FORM, not just a Monte-Carlo estimate: the union length of the intervals

    v +/- tol            (identity)
    100 v +/- 100 tol    (the token/100 candidate)
    v/100 +/- tol/100    (the token*100 candidate)

clipped to [p1, p99], divided by the range.  This run computes that union exactly for
every run x precision and uses seeded Monte Carlo through the ORIGINAL 790 verifier only
as a calibration gate (G4).

REPORTED.  (1) the 30-cell surface, exact and Monte-Carlo, with the PLANT-TRUE rate and
the separation TRUE-FALSE beside it; (2) d*(bucket) = the smallest precision whose floor
is <= 5% and <= 1%; (3) rule 8 walk-forward — d* chosen on the EARLY vintage half of the
corpus, the LATE half read once; (4) a census of what the record actually quotes: for
every published headline token (>= 4 significant digits) the floor at its OWN precision
and its OWN run's artefact size, i.e. how much of the record's re-verification is above
the noise floor; (5) the price-side comparands (RULES v2 / SPY, full / halves / OOS).

KEEP PATHS.  This idea produces NO book: it is a measurement of the record's own
verification machinery, so PROTOCOL 4a and 4b are structurally inapplicable and are
recorded as N/A rather than claimed either way.  The incumbent and SPY numbers are
computed and reported anyway (gate G5) so the leaderboard row carries real comparands.

Deterministic: single seed, no network.  Artefacts: .grid.csv .runs.csv .walkforward.csv
.headline.csv .console.txt
"""
import collections
import re
import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, metrics, backtest  # noqa: E402

RES = ROOT / "research"
BT = RES / "backtests"
OUT = BT / Path(__file__).stem

# ------------------------------------------------------------------ declared constants
COST = 10.0                                   # PROTOCOL rule 2
SEED = zlib.crc32(b"IDEA792|ROUND-MATCH-FLOOR") % (2 ** 32)
MAX_BYTES = 30_000_000                        # per-artefact read cap (idea 790's value)
DATA_SUFFIX = (".csv", ".json", ".txt", ".npz")
NUM_RE = re.compile(r"[-+]?\d*\.\d+|[-+]?\d+")
VINT_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})_")
SIG_MIN = 4                                   # idea 790's "distinctive number" bar
MIN_VALS = 50                                 # idea 790's calibration admission bar
DLADDER = [1, 2, 3, 4, 5, 6]                  # PARAM 1
NBUCKET = 5                                   # PARAM 2 (quintiles of artefact value count)
K_MC = 60                                     # seeded draws per run per precision
BARS = [0.05, 0.01]                           # floors a re-verification claim must clear
CONTROL_DOCS = ("RULES.md", "PROTOCOL.md", "CHANGELOG.md", "LEADERBOARD.md", "QUEUE.md")
# rule-8 split: the corpus's MEDIAN VINTAGE (a rule, not a hand-picked date); ties to IS.

_LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


def sigdigits(tok):
    t = tok.lstrip("+-")
    if "." not in t:
        return 0
    body = t.replace(".", "").lstrip("0")
    return len(body.rstrip("0")) if body.rstrip("0") else 0


def stem_of(name):
    return name.split(".")[0]


def spearman(x, y):
    """Rank correlation without scipy (ties averaged)."""
    a, b = pd.Series(x).rank(), pd.Series(y).rank()
    if a.nunique() < 2 or b.nunique() < 2:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def vintage(stem):
    m = VINT_RE.match(stem)
    return m.group(1) if m else ""


# ------------------------------------------------------- idea 790's verifier, verbatim
def verify_tokens(tokens, toks, vals, scalings=(1.0, 0.01, 100.0)):
    """Idea 790's per-token verifier.  scalings=(1,0.01,100) is 790's convention exactly;
    scalings=(1.0,) is the identity-only leg used to calibrate the closed form."""
    sv = np.sort(vals) if vals.size else vals
    out = {}
    for t in tokens:
        if t in toks:
            out[t] = "EXACT"
            continue
        try:
            q = float(t)
        except ValueError:
            out[t] = "NONE"
            continue
        d = len(t.split(".")[1]) if "." in t else 0
        tolr = 0.5 * 10.0 ** (-d)
        ok = False
        if sv.size:
            for s in scalings:
                cand = q * s
                lo = np.searchsorted(sv, cand - tolr, side="left")
                hi = np.searchsorted(sv, cand + tolr, side="right")
                if hi > lo:
                    ok = True
                    break
        out[t] = "ROUND" if ok else "NONE"
    return out


# --------------------------------------------------------------- closed-form floor
def union_frac(centers_widths, lo, hi):
    """Fraction of [lo, hi] covered by the union of (centers +/- width) families."""
    A, B = [], []
    for c, w in centers_widths:
        if c.size == 0:
            continue
        a, b = c - w, c + w
        m = (b > lo) & (a < hi)
        if m.any():
            A.append(np.clip(a[m], lo, hi))
            B.append(np.clip(b[m], lo, hi))
    if not A:
        return 0.0
    a = np.concatenate(A)
    b = np.concatenate(B)
    o = np.argsort(a, kind="stable")
    a, b = a[o], b[o]
    run_max = np.maximum.accumulate(b)
    prev = np.empty_like(run_max)
    prev[0] = -np.inf
    prev[1:] = run_max[:-1]
    start = np.maximum(a, prev)
    total = float(np.clip(b - start, 0.0, None).sum())
    return min(1.0, total / (hi - lo))


def exact_floor(v, lo, hi, d, three):
    tol = 0.5 * 10.0 ** (-d)
    fam = [(v, tol)]
    if three:
        fam += [(100.0 * v, 100.0 * tol), (v / 100.0, tol / 100.0)]
    return union_frac(fam, lo, hi)


# --------------------------------------------------------------------- corpus reading
def own_artefacts(stem):
    return [p for p in BT.glob(stem + ".*") if p.suffix in DATA_SUFFIX]


def read_values(paths):
    toks, vals, capped, nbytes = set(), [], 0, 0
    for p in paths:
        try:
            raw = p.read_text(errors="ignore")[:MAX_BYTES]
        except Exception:
            continue
        if p.stat().st_size > MAX_BYTES:
            capped += 1
        nbytes += len(raw)
        found = set(NUM_RE.findall(raw))
        toks |= found
        vals.append(pd.to_numeric(pd.Series(sorted(found)), errors="coerce").to_numpy(float))
    if vals:
        v = np.concatenate(vals)
        v = v[np.isfinite(v)]
    else:
        v = np.zeros(0)
    return toks, v, capped, nbytes


def headline_tokens():
    """stem -> published headline tokens (>= SIG_MIN significant digits) from its own
    narrative .md files, idea 790's definition."""
    own = collections.defaultdict(set)
    for p in sorted(BT.glob("*.md")):
        if p.name in CONTROL_DOCS:
            continue
        st = stem_of(p.name)
        txt = p.read_text(errors="ignore")
        for tok in set(NUM_RE.findall(txt)):
            if sigdigits(tok) >= SIG_MIN:
                own[st].add(tok)
    return own


# ------------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 792 — is the 46% ROUND-MATCH FLOOR a property of ARTEFACT SIZE?   (lane C, "
      "2026-09-11)")
    P("=" * 100)
    P(f"PARAMS (2, declared): precision ladder d = {DLADDER}; size buckets = {NBUCKET} "
      f"quintiles of the run's committed DATA value count.  All {len(DLADDER)*NBUCKET} "
      f"cells reported.")
    P(f"CONVENTION: idea 790's verifier verbatim (tol = 0.5*10^-d, candidates "
      f"{{q, q/100, q*100}}); DATA leg = committed .csv/.json/.txt/.npz artefacts EXCLUDING "
      f".console.txt, per-file cap {MAX_BYTES/1e6:.0f} MB; seed {SEED}.")

    # ---------------------------------------------------------------- corpus
    stems = sorted({stem_of(p.name) for p in BT.iterdir() if p.is_file()})
    own = headline_tokens()
    rows, skipped, nb = [], collections.Counter(), 0
    per_run_floor = {}                       # stem -> {d: (exact_id, exact_3x)}
    mc_hits = collections.Counter()          # (d, mode) -> hits
    mc_n = collections.Counter()
    mc_by_run = {}                           # stem -> {d: mc3 rate}
    true_hits, true_n = collections.Counter(), collections.Counter()
    rng = np.random.default_rng(SEED)

    P("")
    P(f"CORPUS: {len(stems)} committed run stems under research/backtests")
    for i, st in enumerate(stems):
        arte = [p for p in own_artefacts(st) if not p.name.endswith(".console.txt")]
        if not arte:
            skipped["no DATA artefact"] += 1
            continue
        toks, v, cap, b = read_values(arte)
        nb += b
        v = v[np.isfinite(v) & (np.abs(v) < 1e9)]
        if v.size < MIN_VALS:
            skipped[f"< {MIN_VALS} values"] += 1
            continue
        lo, hi = float(np.percentile(v, 1)), float(np.percentile(v, 99))
        if not np.isfinite(lo) or not np.isfinite(hi) or hi <= lo:
            skipped["degenerate range"] += 1
            continue
        n_in = int(((v >= lo) & (v <= hi)).sum())
        vs = np.sort(v)
        floors = {}
        mcs = {}
        for d in DLADDER:
            e_id = exact_floor(vs, lo, hi, d, three=False)
            e_3x = exact_floor(vs, lo, hi, d, three=True)
            floors[d] = (e_id, e_3x)
            # seeded Monte Carlo through the ORIGINAL verifier
            fake = rng.uniform(lo, hi, K_MC)
            ftok = [f"{x:.{d}f}" for x in fake]
            r3 = verify_tokens(ftok, toks, vs)
            r1 = verify_tokens(ftok, toks, vs, scalings=(1.0,))
            # NB: verify_tokens returns a dict keyed by token, so a repeated draw collapses
            # in it — count per DRAW by looking the draw's token back up.
            h3 = sum(r3[t] != "NONE" for t in ftok)
            h1 = sum(r1[t] != "NONE" for t in ftok)
            mc_hits[(d, "3x")] += h3
            mc_hits[(d, "id")] += h1
            mc_n[(d, "3x")] += K_MC
            mc_n[(d, "id")] += K_MC
            mcs[d] = h3 / K_MC
            # PLANT-TRUE: the run's own values, re-formatted at this precision
            pick = vs[rng.integers(0, vs.size, K_MC)]
            ttok = [f"{x:.{d}f}" for x in pick]
            rt = verify_tokens(ttok, toks, vs)
            true_hits[d] += sum(rt[t] != "NONE" for t in ttok)
            true_n[d] += K_MC
        per_run_floor[st] = floors
        mc_by_run[st] = mcs
        rows.append(dict(run=st, vintage=vintage(st), n_artefacts=len(arte),
                         n_vals=int(v.size), n_in=n_in, lo=lo, hi=hi,
                         rng_width=hi - lo, density=n_in / (hi - lo),
                         bytes=b, capped=cap, n_head=len(own.get(st, ())),
                         **{f"exact_id_d{d}": floors[d][0] for d in DLADDER},
                         **{f"exact_3x_d{d}": floors[d][1] for d in DLADDER},
                         **{f"mc_3x_d{d}": mcs[d] for d in DLADDER}))
        if (len(rows)) % 100 == 0:
            P(f"  ... {len(rows)} runs measured ({time.time()-t0:.0f}s)")
    runs = pd.DataFrame(rows).set_index("run")
    P(f"  {len(runs)} runs measured, {sum(skipped.values())} excluded "
      f"({dict(skipped)}), {int(runs.capped.sum())} reads hit the cap, "
      f"{nb/1e6:.0f} MB read ({time.time()-t0:.0f}s)")
    P(f"  artefact value count n: min {int(runs.n_vals.min())}, median "
      f"{int(runs.n_vals.median())}, p90 {int(runs.n_vals.quantile(0.9))}, max "
      f"{int(runs.n_vals.max())}; vintages {runs.vintage.min()}..{runs.vintage.max()}")

    # ------------------------------------------------- size buckets (PARAM 2), then gates
    qs = np.quantile(runs.n_vals, np.linspace(0, 1, NBUCKET + 1))
    qs[0], qs[-1] = -np.inf, np.inf
    runs["bucket"] = pd.cut(runs.n_vals, qs, labels=[f"Q{i+1}" for i in range(NBUCKET)],
                            include_lowest=True)
    bd4 = runs.groupby("bucket", observed=True)["exact_3x_d4"].mean()

    P("")
    P("GATES (pre-registered)")
    tr4 = true_hits[4] / max(true_n[4], 1)
    fa4 = mc_hits[(4, "3x")] / max(mc_n[(4, "3x")], 1)
    g1 = bool(tr4 >= 0.95)
    P(f"  G1 verifier sound     : PLANT-TRUE at 4 dp {tr4:.4f} of {true_n[4]} "
      f"(bar >= 0.95) -> {'PASS' if g1 else 'FAIL'}")
    # G2 is a REACHABILITY check, not an equality one: idea 790 calibrated on a 60-run slice,
    # so its pooled 46.0% is one point of the surface this run measures.  The bar is that the
    # surface CONTAINS that point, i.e. the d=4 column spans 0.460 across size buckets.
    g2 = bool(float(bd4.min()) <= 0.460 <= float(bd4.max()))
    P(f"  G2 790 reachable      : d=4 floor by size bucket "
      + " / ".join(f"{v:.4f}" for v in bd4)
      + f" brackets 790's 0.4600 -> {'PASS' if g2 else 'FAIL'} "
      f"(pooled over all runs {fa4:.4f} MC, {float(runs.exact_3x_d4.mean()):.4f} exact)")
    pooled_e3 = {d: float(runs[f"exact_3x_d{d}"].mean()) for d in DLADDER}
    g3 = all(pooled_e3[DLADDER[i + 1]] <= pooled_e3[DLADDER[i]] + 1e-12
             for i in range(len(DLADDER) - 1))
    P(f"  G3 monotone in d      : pooled exact floor "
      + " -> ".join(f"{pooled_e3[d]:.4f}" for d in DLADDER)
      + f" -> {'PASS' if g3 else 'FAIL'}")
    devs = {d: abs(mc_hits[(d, "id")] / mc_n[(d, "id")] - float(runs[f"exact_id_d{d}"].mean()))
            for d in DLADDER}
    # bars: <= 0.02 for d >= 3, <= 0.05 over the whole ladder — at coarse precision the drawn
    # token is quantised onto a lattice whose spacing IS the tolerance window, so the
    # continuous union measure and the lattice hit rate need not agree to 2 decimals.
    g4 = bool(max(devs[d] for d in DLADDER if d >= 3) <= 0.02
              and max(devs.values()) <= 0.05)
    P(f"  G4 closed form == MC  : |MC(identity) - exact(identity)| "
      + " ".join(f"d={d} {devs[d]:.4f}" for d in DLADDER)
      + f" -> {'PASS' if g4 else 'FAIL'}")

    # price-side comparands
    px = load_universe()
    start = px.index[260]
    b = backtest(px, rules_v2_weights(px), cost_bps=COST, freq="W")["returns"].loc[start:]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    h = len(b) // 2
    mb, ms = metrics(b), metrics(spy)
    mb1, mb2 = metrics(b.iloc[:h]), metrics(b.iloc[h:])
    oos = slice("2017-01-01", None)
    mbo, mso = metrics(b.loc[oos]), metrics(spy.loc[oos])
    g5 = bool(abs(mb["Sharpe"] - 1.1998) <= 0.01 and abs(mb["MaxDD"] + 0.1205) <= 0.01
              and abs(mso["Sharpe"] - 0.8721) <= 0.01)
    P(f"  G5 comparands real    : RULES v2 full Sharpe {mb['Sharpe']:.4f} (record 1.1998), "
      f"MaxDD {mb['MaxDD']:.4f} (record -0.1205), SPY OOS Sharpe {mso['Sharpe']:.4f} "
      f"(record 0.8721) -> {'PASS' if g5 else 'FAIL'}")
    P(f"  ALL GATES {'PASS' if all([g1, g2, g3, g4, g5]) else 'NOT ALL PASS'}")

    # ---------------------------------------------------------------- the grid
    grid = []
    for bk, sub in runs.groupby("bucket", observed=True):
        for d in DLADDER:
            tol = 0.5 * 10.0 ** (-d)
            pred = float((1 - np.exp(-2 * tol * sub.density)).mean())
            grid.append(dict(bucket=bk, d=d, runs=len(sub),
                             n_vals_med=float(sub.n_vals.median()),
                             density_med=float(sub.density.median()),
                             exact_id=float(sub[f"exact_id_d{d}"].mean()),
                             exact_3x=float(sub[f"exact_3x_d{d}"].mean()),
                             mc_3x=float(sub[f"mc_3x_d{d}"].mean()),
                             pred_poisson=pred))
    grid = pd.DataFrame(grid)
    grid["true_mc"] = grid.d.map({d: true_hits[d] / max(true_n[d], 1) for d in DLADDER})
    grid["sep"] = grid.true_mc - grid.mc_3x
    P("")
    P(f"THE GRID — {len(grid)} cells (precision x artefact-size quintile), ALL reported")
    P("  bucket  runs   median n   density/unit |  d=1     d=2     d=3     d=4     d=5     "
      "d=6    (exact 3-scaling floor)")
    for bk, sub in grid.groupby("bucket", observed=True):
        s = sub.set_index("d")
        P(f"  {bk:>6} {int(s.runs.iloc[0]):5d} {s.n_vals_med.iloc[0]:10.0f} "
          f"{s.density_med.iloc[0]:14.2f} | "
          + "  ".join(f"{s.loc[d,'exact_3x']:.4f}" for d in DLADDER))
    P("  (identity-only leg, same cells — the /100 and x100 candidates are the difference)")
    for bk, sub in grid.groupby("bucket", observed=True):
        s = sub.set_index("d")
        P(f"  {bk:>6} {'':5} {'':10} {'':14} | "
          + "  ".join(f"{s.loc[d,'exact_id']:.4f}" for d in DLADDER))
    P("  (Monte Carlo through 790's own verifier, 40 draws/run — calibrates the closed form)")
    for bk, sub in grid.groupby("bucket", observed=True):
        s = sub.set_index("d")
        P(f"  {bk:>6} {'':5} {'':10} {'':14} | "
          + "  ".join(f"{s.loc[d,'mc_3x']:.4f}" for d in DLADDER))
    P("  PLANT-TRUE (pooled, same draws budget): "
      + "  ".join(f"d={d} {true_hits[d]/max(true_n[d],1):.4f}" for d in DLADDER))
    P("  SEPARATION TRUE-FALSE by bucket:")
    for bk, sub in grid.groupby("bucket", observed=True):
        s = sub.set_index("d")
        P(f"  {bk:>6} {'':5} {'':10} {'':14} | "
          + "  ".join(f"{s.loc[d,'sep']:+.4f}" for d in DLADDER))

    # is it artefact SIZE?
    P("")
    sp = [(d, spearman(runs[f"exact_3x_d{d}"].to_numpy(float),
                       np.log10(runs.density.to_numpy(float)))) for d in DLADDER]
    P("  Spearman(log10 density, exact 3-scaling floor) per precision: "
      + "; ".join(f"d={d} {r:+.4f}" for d, r in sp))
    pooled_pred = float((grid.pred_poisson * grid.runs).sum() / grid.runs.sum())
    pooled_id = float((grid.exact_id * grid.runs).sum() / grid.runs.sum())
    pooled_3x = float((grid.exact_3x * grid.runs).sum() / grid.runs.sum())
    P(f"  pooled Poisson prediction 1-exp(-2*tol*density) {pooled_pred:.4f} vs realised "
      f"identity-leg {pooled_id:.4f} (the model is the identity leg only) vs the full "
      f"3-scaling convention {pooled_3x:.4f} — the /100 and x100 candidates are "
      f"{pooled_3x - pooled_id:+.4f} of floor the record never declared.")

    # ---------------------------------------------------------------- d* table
    P("")
    P("d* — the smallest precision whose OWN floor clears the bar (per bucket, exact "
      "3-scaling)")
    dstar = {}
    for bar in BARS:
        line = []
        for bk, sub in grid.groupby("bucket", observed=True):
            s = sub.set_index("d")
            ok = [d for d in DLADDER if s.loc[d, "exact_3x"] <= bar]
            dstar[(bk, bar)] = min(ok) if ok else None
            line.append(f"{bk} {'>'+str(max(DLADDER)) if not ok else min(ok)}")
        P(f"  bar {bar:.0%}: " + "   ".join(line))

    # ---------------------------------------------------------------- rule 8
    cum = runs.vintage.value_counts().sort_index().cumsum() / len(runs)
    IS_END = str(cum[cum >= 0.5].index[0])       # corpus median vintage, ties to IS
    P("")
    P(f"RULE 8 WALK-FORWARD — d* chosen on vintages <= {IS_END} (the corpus median vintage) "
      f"ONLY, later vintages read ONCE")
    is_mask = runs.vintage <= IS_END
    P(f"  IS {int(is_mask.sum())} runs ({runs.vintage[is_mask].min()}..{IS_END}), OOS "
      f"{int((~is_mask).sum())} runs ({runs.vintage[~is_mask].min()}.."
      f"{runs.vintage.max()})")
    wf = []
    for bk in [f"Q{i+1}" for i in range(NBUCKET)]:
        sub_is = runs[(runs.bucket == bk) & is_mask]
        sub_oos = runs[(runs.bucket == bk) & (~is_mask)]
        if not len(sub_is) or not len(sub_oos):
            continue
        for bar in BARS:
            ok = [d for d in DLADDER if float(sub_is[f"exact_3x_d{d}"].mean()) <= bar]
            d_is = min(ok) if ok else None
            if d_is is None:
                wf.append(dict(bucket=bk, bar=bar, d_is=np.nan, is_floor=np.nan,
                               oos_floor=np.nan, oos_holds=False, n_is=len(sub_is),
                               n_oos=len(sub_oos)))
                continue
            f_is = float(sub_is[f"exact_3x_d{d_is}"].mean())
            f_oos = float(sub_oos[f"exact_3x_d{d_is}"].mean())
            wf.append(dict(bucket=bk, bar=bar, d_is=d_is, is_floor=f_is, oos_floor=f_oos,
                           oos_holds=bool(f_oos <= bar), n_is=len(sub_is),
                           n_oos=len(sub_oos)))
    wf = pd.DataFrame(wf, columns=["bucket", "bar", "d_is", "is_floor", "oos_floor",
                                   "oos_holds", "n_is", "n_oos"])
    for bar in BARS if len(wf) else []:
        s = wf[wf.bar == bar]
        P(f"  bar {bar:.0%}: " + "; ".join(
            f"{r.bucket} d*={r.d_is if pd.notna(r.d_is) else '>6'} IS {r.is_floor:.4f} -> "
            f"OOS {r.oos_floor:.4f} {'HOLDS' if r.oos_holds else 'FAILS'}"
            for r in s.itertuples()))
    held = int(wf[wf.bar == 0.05].oos_holds.sum())
    tot = int((wf.bar == 0.05).sum())
    P(f"  bar 5%: the IS-chosen precision holds out of sample in {held}/{tot} buckets.")
    # the record's standing convention, read once on OOS
    conv = float(runs.loc[~is_mask, "exact_3x_d4"].mean())
    P(f"  the record's standing 4-dp convention, read once on the OOS half: floor "
      f"{conv:.4f} (IS {float(runs.loc[is_mask,'exact_3x_d4'].mean()):.4f}) — a 4-dp "
      f"re-verification claim is {conv:.1%} likely to succeed on noise alone.")

    # ---------------------------------------------------------------- headline census
    P("")
    P("WHAT THE RECORD ACTUALLY QUOTES — every published headline token (>= 4 sig digits) "
      "against the floor at its OWN precision and its OWN run's artefact size")
    hrows = []
    for st, toks in own.items():
        if st not in per_run_floor:
            continue
        for t in toks:
            if "." not in t:
                continue
            d = len(t.split(".")[1])
            dd = min(d, max(DLADDER))
            hrows.append(dict(run=st, token=t, d=d, d_used=dd,
                              floor=per_run_floor[st][dd][1],
                              n_vals=int(runs.at[st, "n_vals"]),
                              bucket=str(runs.at[st, "bucket"])))
    head = pd.DataFrame(hrows)
    if len(head):
        P(f"  {len(head)} published tokens across {head.run.nunique()} runs; decimals "
          f"quoted: median {int(head.d.median())}, "
          + ", ".join(f"{k} dp {v:.1%}" for k, v in
                      head.d.value_counts(normalize=True).sort_index().head(8).items()))
        for bar in (0.46, 0.20, 0.05):
            P(f"  share of published tokens whose own-run floor exceeds {bar:.0%}: "
              f"{float((head.floor > bar).mean()):.4f} "
              f"({int((head.floor > bar).sum())} of {len(head)})")
        P(f"  median own-run floor of a published token: {float(head.floor.median()):.4f}; "
          f"mean {float(head.floor.mean()):.4f}")
        by = head.groupby("bucket", observed=True).floor.agg(["size", "median", "mean"])
        for bk, r in by.iterrows():
            P(f"    {bk}: {int(r['size'])} tokens, median floor {r['median']:.4f}, mean "
              f"{r['mean']:.4f}")

    # ---------------------------------------------------------------- KEEP paths
    P("")
    P("KEEP PATHS (PROTOCOL rule 4)")
    P(f"  comparands: RULES v2 full CAGR {mb['CAGR']:.4f} Sharpe {mb['Sharpe']:.4f} "
      f"(H1 {mb1['Sharpe']:.4f} / H2 {mb2['Sharpe']:.4f}) MaxDD {mb['MaxDD']:.4f}; "
      f"SPY full CAGR {ms['CAGR']:.4f} Sharpe {ms['Sharpe']:.4f} MaxDD {ms['MaxDD']:.4f}")
    P(f"  OOS (2017+): RULES v2 CAGR {mbo['CAGR']:.4f} Sharpe {mbo['Sharpe']:.4f} MaxDD "
      f"{mbo['MaxDD']:.4f}; SPY CAGR {mso['CAGR']:.4f} Sharpe {mso['Sharpe']:.4f} MaxDD "
      f"{mso['MaxDD']:.4f}")
    P("  4a (beat the book): N/A — this idea produces no book, no weights function and no "
      "return stream, so there is nothing to compare against RULES v2 in either half.")
    P("  4b (capital-worthy): N/A — same reason.  NOT claimed either way; the row is "
      "recorded n/a rather than passed or failed.")

    # ---------------------------------------------------------------- artefacts
    runs.to_csv(f"{OUT}.runs.csv")
    grid.to_csv(f"{OUT}.grid.csv", index=False)
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    if len(head):
        head.to_csv(f"{OUT}.headline.csv", index=False)
    Path(f"{OUT}.console.txt").write_text("\n".join(_LOG) + "\n")
    P("")
    P(f"artefacts: {Path(OUT).name}.runs.csv .grid.csv .walkforward.csv .headline.csv "
      f".console.txt   ({time.time()-t0:.0f}s)")
    Path(f"{OUT}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
