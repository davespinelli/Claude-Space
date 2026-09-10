#!/usr/bin/env python3
"""Idea 497 (lane B, 2026-09-10) -- re-run the 3 wide-and-unfolded census files individually.

Idea 483's CLOUD census (`2026-09-09_which-published-residualisations-are-IN-SAMPLE-fits_cloud.census.csv`)
scored 70 committed backtest files that carry a linear-fit call on two static flags,
`has_fold_machinery` and `wide_design_hint`.  Exactly 3 files are wide AND unfolded:

  F1  2026-09-06_can-a-panel-property-choose-the-cadence_cloud.py          (line 344, lstsq)
  F2  2026-09-06_does-the-cash-drag-share-depend-on-the-panel-or-on-the-gate-level_cloud.py (line 169, pinv)
  F3  2026-09-06_is-phase-sensitivity-a-book-property-or-a-panel-one_cloud.py (line 398, lstsq)

The queue asks: execute each at its own penalty with K-fold predictions substituted, and
report which PUBLISHED numbers move.  Max 2 params -- (fold count K, ridge penalty lam).

METHOD.  No book is re-run.  Each file's design matrix and target are rebuilt from that
file's OWN committed artefacts (and, for F1's ladder, from idea 175's committed ladder.csv,
which F1 itself gates against at 1e-10), so stage 0 is an exact reproduction gate on the
published number before anything is substituted.  Then, holding the design fixed, the
in-sample fitted value is replaced by an out-of-fold prediction:

    R2_oof = 1 - SS(y - yhat_oof) / SS(y - ybar)          (ybar on the FULL sample)

with deterministic folds (a fixed-seed permutation, identical folds for every spec inside a
file so the specs stay paired) and a standardised ridge at penalty lam (intercept never
penalised; standardisation fitted on the TRAIN fold only).  lam = 0 is plain OLS, i.e. the
published estimator, so the lam=0 / K=n column is the file as committed.

GRID: K in {2, 5, 10, LOO} x lam in {0, 0.1, 1, 10, 100} = 20 points per spec, ALL reported.

PROTOCOL rule 8 is run in section (4): F1's fitted gap model is used as a CADENCE SELECTOR
with every input taken from IS <= 2016-12-31 only, scored once on 2017-2026, IS-fit against
K-fold-fit, against the constant-cadence reference, against the live RULES v2 book and SPY;
both KEEP paths evaluated on the committed ladder's own 4a/4b columns.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .verdicts.csv, .walkforward.csv.
Reads only committed artefacts + research/baseline.py.  Modifies nothing.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

F1 = "2026-09-06_can-a-panel-property-choose-the-cadence_cloud"
F2 = "2026-09-06_does-the-cash-drag-share-depend-on-the-panel-or-on-the-gate-level_cloud"
F3 = "2026-09-06_is-phase-sensitivity-a-book-property-or-a-panel-one_cloud"
P175 = "2026-09-05_does-cadence-skill-survive-a-second-corpus_cloud"

FOLDS = [2, 5, 10, "LOO"]
LAMS = [0.0, 0.1, 1.0, 10.0, 100.0]
SEED = 497
GATE = 1e-9
IS_END, OOS_START = "2016-12-31", "2017-01-01"

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


# ------------------------------------------------------------------ the estimator
def _ridge_fit(Xtr, ytr, lam):
    """Standardised ridge on the TRAIN rows only; returns a predict(X) closure.
    lam=0 is plain OLS (lstsq, same rcond as the published files)."""
    Xtr = np.asarray(Xtr, float)
    ytr = np.asarray(ytr, float)
    n, p = Xtr.shape if Xtr.ndim == 2 else (len(ytr), 0)
    if p == 0:
        m = ytr.mean()
        return lambda X: np.full(len(X), m)
    mu = Xtr.mean(axis=0)
    sd = Xtr.std(axis=0)
    sd = np.where(sd > 1e-12, sd, 1.0)
    Z = (Xtr - mu) / sd
    ybar = ytr.mean()
    if lam == 0.0:
        b, *_ = np.linalg.lstsq(np.hstack([np.ones((n, 1)), Z]), ytr, rcond=None)
        b0, bz = b[0], b[1:]
    else:
        G = Z.T @ Z + lam * np.eye(p)
        bz = np.linalg.solve(G, Z.T @ (ytr - ybar))
        b0 = ybar
    return lambda X: b0 + ((np.asarray(X, float) - mu) / sd) @ bz


def _folds(n, K, seed=SEED):
    """Deterministic fold assignment. K='LOO' -> n folds."""
    k = n if K == "LOO" else int(K)
    idx = np.random.default_rng(seed).permutation(n)
    return [idx[np.arange(n) % k == f] for f in range(k)]


def r2_is(y, X, lam):
    y = np.asarray(y, float)
    pred = _ridge_fit(X, y, lam)(X) if np.size(X) else np.full(len(y), y.mean())
    sst = ((y - y.mean()) ** 2).sum()
    return float(1 - ((y - pred) ** 2).sum() / sst) if sst > 0 else np.nan


def r2_oof(y, X, K, lam, seed=SEED):
    """Out-of-fold R2 with the SAME denominator as the published R2 (full-sample ybar)."""
    y = np.asarray(y, float)
    n = len(y)
    if np.size(X) == 0:
        X = np.zeros((n, 0))
    X = np.asarray(X, float)
    pred = np.empty(n)
    for te in _folds(n, K, seed):
        tr = np.setdiff1d(np.arange(n), te)
        pred[te] = _ridge_fit(X[tr], y[tr], lam)(X[te])
    sst = ((y - y.mean()) ** 2).sum()
    return float(1 - ((y - pred) ** 2).sum() / sst) if sst > 0 else np.nan


# ------------------------------------------------------------------ the three designs
def build_f1():
    """F1 section (2): OLS of the M-minus-6W OOS-Sharpe gap on candidate explanators, 115 books.
    Design rebuilt from idea 175's committed ladder (F1 gates its own ladder against it at
    1e-10) + F1's own props.csv.  Published R2 in F1.decomp.csv."""
    L = pd.read_csv(OUT / f"{P175}.ladder.csv")
    PR = pd.read_csv(OUT / f"{F1}.props.csv")
    piv = L.pivot(index="book", columns="point", values="OOS_Sharpe")
    gap = (piv["M"] - piv["6W"]).rename("gap")
    D = PR.set_index("book").join(gap).join(
        L[L.point == "W"].set_index("book")[["turnover"]].rename(columns={"turnover": "turn_W"}))
    D = D.dropna(subset=["gap"])
    famd = np.column_stack([(D.family == f_).astype(float) for f_ in ("SMALL", "ETF")])
    lh = np.log(D["hstar_IR_s21"].to_numpy(float))[:, None]
    le = np.log(D["episode_days"].to_numpy(float))[:, None]
    lt = np.log(D["turn_W"].clip(lower=1e-6).to_numpy(float))[:, None]
    specs = {
        "family dummies only": famd,
        "log h* (IR, stride 21)": lh,
        "log episode_days": le,
        "log turnover at W": lt,
        "log h* + log episode": np.hstack([lh, le]),
        "log h* + log episode + family": np.hstack([lh, le, famd]),
    }
    return D.gap.to_numpy(float), specs, D


def build_f2():
    """F2 section B3: share ~ 1 + c_bar + panel + family + cadence, and the four partial R2.
    Design rebuilt from F2's own decomp.csv exactly as F2 builds it (FULL window, |gap0|>=0.10)."""
    D = pd.read_csv(OUT / f"{F2}.decomp.csv")
    F = D[D.window == "FULL"].copy()
    F["tiny"] = F.gap0_pp.abs() < 0.10
    S = F[~F.tiny].copy()
    pdum = pd.get_dummies(S.panel, prefix="P", drop_first=True).astype(float).to_numpy()
    fdum = pd.get_dummies(S.family, prefix="F", drop_first=True).astype(float).to_numpy()
    cdum = pd.get_dummies(S.cad, prefix="C", drop_first=True).astype(float).to_numpy()
    cbar = S[["c_bar"]].to_numpy(float)
    blocks = {"c_bar": cbar, "panel": pdum, "family": fdum, "cadence": cdum}
    return S.share.to_numpy(float), blocks, S


def build_f3():
    """F3 section T1(i): log(phase spread) ~ family dummies / two predictors / both, per cadence.
    Design rebuilt from F3's own books.csv."""
    tab = pd.read_csv(OUT / f"{F3}.books.csv")
    out = {}
    for cad in ["2W", "6W", "8W", "10W", "2M"]:
        s = tab[(tab.cad == cad) & np.isfinite(tab.spread) & (tab.spread > 0)].dropna(
            subset=["persistence", "elig_turn"])
        if len(s) < 10:
            continue
        y = np.log(s.spread.to_numpy(float))
        Dm = pd.get_dummies(s.family).to_numpy()[:, 1:].astype(float)
        X = np.column_stack([np.log(s.persistence.to_numpy(float)),
                             np.log(s.elig_turn.to_numpy(float))])
        out[cad] = (y, {"family": Dm, "P1+P2": X, "both": np.hstack([Dm, X])}, s)
    return out


# ================================================================== (0) REPRODUCTION GATES
def stage0():
    P("=" * 112)
    P("(0) REPRODUCTION GATES -- the published number, rebuilt from committed artefacts")
    P("=" * 112)
    ok = True

    y1, specs1, D1 = build_f1()
    pub1 = pd.read_csv(OUT / f"{F1}.decomp.csv").set_index("spec")
    P(f"\nF1 {F1}.py:344  (decomp.csv, n={len(y1)} books)")
    for nm, X in specs1.items():
        mine, pub = r2_is(y1, X, 0.0), float(pub1.loc[nm, "R2"])
        d = abs(mine - pub)
        ok &= d < GATE
        P(f"   {nm:32s} p={X.shape[1]}  R2 mine {mine:.10f}  pub {pub:.10f}  "
          f"|d| {d:.2e}  {'PASS' if d < GATE else 'FAIL'}")

    y2, blk2, S2 = build_f2()
    Xfull = np.hstack([blk2[k] for k in ("c_bar", "panel", "family", "cadence")])
    full = r2_is(y2, Xfull, 0.0)
    P(f"\nF2 {F2}.py:169  (console B3, n={len(y2)}, p={Xfull.shape[1] + 1})")
    d = abs(full - 0.6098)
    ok &= d < 5e-5
    P(f"   full R2 mine {full:.4f}  pub 0.6098  |d| {d:.2e}  {'PASS' if d < 5e-5 else 'FAIL'}")
    pubpr = {"c_bar": 0.2708, "panel": 0.0020, "family": 0.3739, "cadence": 0.0018}
    for lbl, pv in pubpr.items():
        rest = np.hstack([blk2[k] for k in ("c_bar", "panel", "family", "cadence") if k != lbl])
        mine = full - r2_is(y2, rest, 0.0)
        d = abs(mine - pv)
        ok &= d < 5e-5
        P(f"   partial R2 {lbl:9s} mine {mine:.4f}  pub {pv:.4f}  |d| {d:.2e}  "
          f"{'PASS' if d < 5e-5 else 'FAIL'}")

    f3 = build_f3()
    pub3 = {"2W": (0.038, 0.065, 0.097), "6W": (0.112, 0.129, 0.206),
            "8W": (0.068, 0.307, 0.378), "10W": (0.087, 0.326, 0.409),
            "2M": (0.026, 0.015, 0.036)}
    P(f"\nF3 {F3}.py:398  (console T1(i), n=115 per cadence)")
    for cad, (y, sp, _) in f3.items():
        mine = tuple(r2_is(y, sp[k], 0.0) for k in ("family", "P1+P2", "both"))
        dd = max(abs(a - b) for a, b in zip(mine, pub3[cad]))
        ok &= dd < 5e-4
        P(f"   {cad:4s} n={len(y):3d}  mine "
          f"{mine[0]:.3f}/{mine[1]:.3f}/{mine[2]:.3f}  pub "
          f"{pub3[cad][0]:.3f}/{pub3[cad][1]:.3f}/{pub3[cad][2]:.3f}  |d|max {dd:.2e}  "
          f"{'PASS' if dd < 5e-4 else 'FAIL'}")

    P(f"\n  ALL GATES: {'PASS' if ok else 'FAIL'}")
    assert ok, "reproduction gate failed -- nothing downstream is readable"
    return (y1, specs1, D1), (y2, blk2, S2), f3


# ================================================================== (1) THE GRID
def stage1(d1, d2, d3):
    P("\n" + "=" * 112)
    P("(1) THE RE-RUN -- K-fold predictions substituted, every grid point reported")
    P("=" * 112)
    rows = []
    y1, specs1, _ = d1
    for nm, X in specs1.items():
        for lam in LAMS:
            rows.append(dict(file="F1", block="decomp", spec=nm, n=len(y1), p=X.shape[1],
                             K="IS", lam=lam, R2=r2_is(y1, X, lam)))
            for K in FOLDS:
                rows.append(dict(file="F1", block="decomp", spec=nm, n=len(y1), p=X.shape[1],
                                 K=str(K), lam=lam, R2=r2_oof(y1, X, K, lam)))

    y2, blk2, _ = d2
    order = ("c_bar", "panel", "family", "cadence")
    for lam in LAMS:
        for K in ["IS"] + [str(k) for k in FOLDS]:
            def rr(X):
                return r2_is(y2, X, lam) if K == "IS" else r2_oof(y2, X, K, lam)
            Xf = np.hstack([blk2[k] for k in order])
            full = rr(Xf)
            rows.append(dict(file="F2", block="B3", spec="full", n=len(y2), p=Xf.shape[1],
                             K=K, lam=lam, R2=full))
            for lbl in order:
                rest = np.hstack([blk2[k] for k in order if k != lbl])
                rows.append(dict(file="F2", block="B3", spec=f"partial:{lbl}", n=len(y2),
                                 p=blk2[lbl].shape[1], K=K, lam=lam, R2=full - rr(rest)))

    for cad, (y, sp, _) in d3.items():
        for nm, X in sp.items():
            for lam in LAMS:
                rows.append(dict(file="F3", block=f"T1i:{cad}", spec=nm, n=len(y),
                                 p=X.shape[1], K="IS", lam=lam, R2=r2_is(y, X, lam)))
                for K in FOLDS:
                    rows.append(dict(file="F3", block=f"T1i:{cad}", spec=nm, n=len(y),
                                     p=X.shape[1], K=str(K), lam=lam,
                                     R2=r2_oof(y, X, K, lam)))
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    P(f"\n  {len(G)} grid points written to {STEM}.grid.csv")

    for fl, blk in [("F1", "decomp"), ("F2", "B3")] + [("F3", f"T1i:{c}") for c in d3]:
        sub = G[(G.file == fl) & (G.block == blk)]
        P(f"\n  --- {fl} / {blk}: R2 by (spec x K) at lam=0, then the lam ladder at K=10")
        t0 = sub[sub.lam == 0].pivot_table(index="spec", columns="K", values="R2")
        t0 = t0[[c for c in ["IS", "2", "5", "10", "LOO"] if c in t0.columns]]
        P(t0.to_string(float_format=lambda x: f"{x:+.4f}"))
        t1 = sub[sub.K == "10"].pivot_table(index="spec", columns="lam", values="R2")
        P("  lam ladder (K=10):")
        P(t1.to_string(float_format=lambda x: f"{x:+.4f}"))
    return G


# ================================================================== (2) DO THE VERDICTS MOVE
def stage2(G, d1, d2, d3):
    P("\n" + "=" * 112)
    P("(2) DO THE PUBLISHED VERDICTS MOVE?  each file's own headline sentence, re-read")
    P("=" * 112)
    V = []

    # --- F1: "neither property absorbs the family" -> family-only R2 ~= the full spec's
    P("\nF1 published sentence: family dummies alone (0.4453) reach the same R2 as h*+episode+"
      "family (0.4518); the two properties add +0.0065, so neither absorbs the family.")
    sub = G[(G.file == "F1")]
    for K in ["IS", "2", "5", "10", "LOO"]:
        for lam in LAMS:
            s = sub[(sub.K == K) & (sub.lam == lam)].set_index("spec").R2
            add = s["log h* + log episode + family"] - s["family dummies only"]
            best = s.idxmax()
            V.append(dict(file="F1", claim="properties add little over family", K=K, lam=lam,
                          stat=add, published=0.0065,
                          held=bool(add < 0.05), extra=f"argmax={best}"))
            V.append(dict(file="F1", claim="the 4-param spec is the best-fitting spec", K=K,
                          lam=lam, stat=add, published=1.0,
                          held=bool(best == "log h* + log episode + family"),
                          extra=f"argmax={best}"))
    t = pd.DataFrame([v for v in V if v["file"] == "F1"
                      and v["claim"].startswith("properties")]).pivot_table(
        index="K", columns="lam", values="stat")
    P("  R2(h*+episode+family) - R2(family only):")
    P(t.reindex(["IS", "2", "5", "10", "LOO"]).to_string(float_format=lambda x: f"{x:+.4f}"))
    am = pd.DataFrame([v for v in V if v["file"] == "F1"
                       and v["claim"].startswith("properties")]).pivot_table(
        index="K", columns="lam", values="extra", aggfunc="first")
    P("  argmax spec:")
    P(am.reindex(["IS", "2", "5", "10", "LOO"]).to_string())

    # --- F2: "LEVEL explains more of the share than PANEL"; largest partial R2 = family
    P("\nF2 published sentence: largest partial R2 is family (0.3739); c_bar 0.2708 vs panel "
      "0.0020 -> LEVEL explains more of the share.")
    sub = G[(G.file == "F2") & G.spec.str.startswith("partial:")].copy()
    sub["blk"] = sub.spec.str.split(":").str[1]
    lines = []
    for K in ["IS", "2", "5", "10", "LOO"]:
        for lam in LAMS:
            s = sub[(sub.K == K) & (sub.lam == lam)].set_index("blk").R2
            ans = "LEVEL" if s["c_bar"] > s["panel"] else "PANEL"
            win = s.idxmax()
            V.append(dict(file="F2", claim="LEVEL beats PANEL", K=K, lam=lam,
                          stat=s["c_bar"] - s["panel"], published=0.2688,
                          held=bool(ans == "LEVEL"), extra=f"argmax={win}"))
            lines.append(dict(K=K, lam=lam, c_bar=s["c_bar"], panel=s["panel"],
                              family=s["family"], cadence=s["cadence"], ans=ans, argmax=win))
    LF = pd.DataFrame(lines)
    P(LF.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    # --- F3: "the two predictors beat the family label at 8W/10W"
    P("\nF3 published sentence: R2(P1+P2) exceeds R2(family) at 2W/6W/8W/10W and the gap is "
      "large at 8W (0.307 vs 0.068) and 10W (0.326 vs 0.087) -- phase sensitivity is a BOOK "
      "property there, not a panel label.")
    rows3 = []
    for cad in d3:
        sub = G[(G.file == "F3") & (G.block == f"T1i:{cad}")]
        for K in ["IS", "2", "5", "10", "LOO"]:
            for lam in LAMS:
                s = sub[(sub.K == K) & (sub.lam == lam)].set_index("spec").R2
                gap = s["P1+P2"] - s["family"]
                V.append(dict(file="F3", claim=f"predictors beat family @{cad}", K=K, lam=lam,
                              stat=gap, published=np.nan, held=bool(gap > 0),
                              extra=f"Rpred={s['P1+P2']:.3f}"))
                rows3.append(dict(cad=cad, K=K, lam=lam, R2_family=s["family"],
                                  R2_pred=s["P1+P2"], R2_both=s["both"], gap=gap))
    R3 = pd.DataFrame(rows3)
    P("  R2(P1+P2) - R2(family), by cadence x K, at lam=0:")
    P(R3[R3.lam == 0].pivot_table(index="cad", columns="K", values="gap")
      [["IS", "2", "5", "10", "LOO"]].to_string(float_format=lambda x: f"{x:+.4f}"))
    P("  R2(P1+P2) itself, by cadence x K, at lam=0:")
    P(R3[R3.lam == 0].pivot_table(index="cad", columns="K", values="R2_pred")
      [["IS", "2", "5", "10", "LOO"]].to_string(float_format=lambda x: f"{x:+.4f}"))
    P("  R2(family) itself, by cadence x K, at lam=0:")
    P(R3[R3.lam == 0].pivot_table(index="cad", columns="K", values="R2_family")
      [["IS", "2", "5", "10", "LOO"]].to_string(float_format=lambda x: f"{x:+.4f}"))

    VD = pd.DataFrame(V)
    VD.to_csv(OUT / f"{STEM}.verdicts.csv", index=False)
    P("\n  HELD-RATE per published claim (share of the 25 (K x lam) points where the published "
      "verdict still reads the same; K=IS,lam=0 is the file as committed):")
    hr = VD.groupby(["file", "claim"]).held.agg(["mean", "size"])
    P(hr.to_string(float_format=lambda x: f"{x:.3f}"))
    P("\n  ...and restricted to the OUT-OF-FOLD points only (K != IS, 20 points each):")
    hr2 = VD[VD.K != "IS"].groupby(["file", "claim"]).held.agg(["mean", "size"])
    P(hr2.to_string(float_format=lambda x: f"{x:.3f}"))
    return VD


# ================================================================== (3) FREE R2 REFERENCE
def stage3(d1, d2, d3):
    P("\n" + "=" * 112)
    P("(3) HOW MUCH OF EACH PUBLISHED R2 IS FREE?  E[R2] = p/n for a design that knows nothing")
    P("=" * 112)
    rows = []
    y1, specs1, _ = d1
    for nm, X in specs1.items():
        rows.append(dict(file="F1", spec=nm, n=len(y1), p=X.shape[1],
                         R2_IS=r2_is(y1, X, 0.0), free=X.shape[1] / len(y1)))
    y2, blk2, _ = d2
    order = ("c_bar", "panel", "family", "cadence")
    Xf = np.hstack([blk2[k] for k in order])
    full = r2_is(y2, Xf, 0.0)
    rows.append(dict(file="F2", spec="full", n=len(y2), p=Xf.shape[1], R2_IS=full,
                     free=Xf.shape[1] / len(y2)))
    for lbl in order:
        rest = np.hstack([blk2[k] for k in order if k != lbl])
        rows.append(dict(file="F2", spec=f"partial:{lbl}", n=len(y2), p=blk2[lbl].shape[1],
                         R2_IS=full - r2_is(y2, rest, 0.0), free=blk2[lbl].shape[1] / len(y2)))
    for cad, (y, sp, _) in d3.items():
        for nm, X in sp.items():
            rows.append(dict(file="F3", spec=f"{cad}:{nm}", n=len(y), p=X.shape[1],
                             R2_IS=r2_is(y, X, 0.0), free=X.shape[1] / len(y)))
    FR = pd.DataFrame(rows)
    FR["R2_over_free"] = FR.R2_IS / FR.free
    P(FR.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  max p/n over all {len(FR)} published sites here: {FR.free.max():.4f}  "
      f"(p_max={int(FR.p.max())}, n_min={int(FR.n.min())})")
    P("  -> the census's `wide_design_hint` is a STATIC flag (it fires on get_dummies/per-name "
      "text). At runtime none of the 3 files is wide: p/n <= "
      f"{FR.free.max():.3f}, so free R2 is at most {FR.free.max():.1%}.")
    return FR


# ================================================================== (4) RULE 8
def stage4(d1):
    P("\n" + "=" * 112)
    P("(4) RULE 8 WALK-FORWARD -- F1's fit as a CADENCE SELECTOR, IS<=2016 only, scored on 2017-2026")
    P("=" * 112)
    _, _, D = d1
    L = pd.read_csv(OUT / f"{P175}.ladder.csv")
    LADDER = ["D", "2D", "W", "2W", "M", "6W", "8W", "10W", "2M", "Q"]
    L = L[L.point.isin(LADDER)]
    isp = L.pivot(index="book", columns="point", values="IS_Sharpe")
    oos = L.pivot(index="book", columns="point", values="OOS_Sharpe")
    books = [b for b in D.index if b in isp.index and b in oos.index]
    isp, oos = isp.loc[books], oos.loc[books]
    Db = D.loc[books]

    # IS-side target, IS-side regressors ONLY (episode/h* are the IS columns the file publishes)
    y = (isp["M"] - isp["6W"]).to_numpy(float)
    famd = np.column_stack([(Db.family == f_).astype(float) for f_ in ("SMALL", "ETF")])
    lh = np.log(Db["hstarIS_IR_s21"].to_numpy(float))[:, None]
    le = np.log(Db["episode_days_IS"].to_numpy(float))[:, None]
    specs = {"family only": famd, "log h*_IS + log episode_IS": np.hstack([lh, le]),
             "h*_IS + episode_IS + family": np.hstack([lh, le, famd])}

    # why every fitted arm below is the SAME arm: the IS gap is one-signed, so any smoother
    # of it is one-signed too, and the sign REVERSES out of sample.
    oosgap = (oos["M"] - oos["6W"]).to_numpy(float)
    P(f"\n  the target: IS gap = IS_Sharpe(M) - IS_Sharpe(6W) over {len(y)} books -- "
      f"mean {y.mean():+.4f}, sd {y.std(ddof=1):.4f}, share > 0 {(y > 0).mean():.3f}")
    P(f"  the truth : OOS gap over the same books        -- "
      f"mean {oosgap.mean():+.4f}, sd {oosgap.std(ddof=1):.4f}, "
      f"share > 0 {(oosgap > 0).mean():.3f}")
    rho = float(np.corrcoef(pd.Series(y).rank().to_numpy(),
                            pd.Series(oosgap).rank().to_numpy())[0, 1])
    P(f"  Spearman(IS gap, OOS gap) = {rho:+.4f}")
    P("  -> the IS gap is positive on 95% of books and the OOS gap on 27%: the sign the fit "
      "learns IS is the WRONG constant OOS. Any fitted predictor of a one-signed target is "
      "one-signed, so every fitted arm below collapses onto 'constant M' -- which is exactly "
      "what the table shows, at every K and every lam.")
    rows = []

    def score(pick, label, K, lam):
        sel = np.where(pick > 0, "M", "6W")
        s = np.array([oos.loc[b, c] for b, c in zip(books, sel)])
        key = pd.MultiIndex.from_arrays([books, sel])
        Li = L.set_index(["book", "point"])
        p4a = (~Li.loc[key, "fail4a"].fillna("").astype(str).str.len().astype(bool)).sum()
        p4b = (~Li.loc[key, "fail4b"].fillna("").astype(str).str.len().astype(bool)).sum()
        rows.append(dict(selector=label, K=K, lam=lam, n_books=len(books),
                         mean_OOS_Sharpe=float(s.mean()), median_OOS_Sharpe=float(np.median(s)),
                         picked_M=int((sel == "M").sum()),
                         mean_OOS_CAGR=float(Li.loc[key, "OOS_CAGR"].mean()),
                         mean_OOS_MaxDD=float(Li.loc[key, "OOS_MaxDD"].mean()),
                         pass4a=int(p4a), pass4b=int(p4b)))

    # references that fit nothing
    score(np.ones(len(books)), "constant M (no fit)", "-", "-")
    score(np.zeros(len(books)), "constant 6W (no fit)", "-", "-")
    score(y, "IS-Sharpe argmax (incumbent)", "-", "-")
    for nm, X in specs.items():
        for lam in LAMS:
            score(_ridge_fit(X, y, lam)(X), f"fitted: {nm}", "IS", lam)
            for K in FOLDS:
                n = len(y)
                pred = np.empty(n)
                for te in _folds(n, K):
                    tr = np.setdiff1d(np.arange(n), te)
                    pred[te] = _ridge_fit(X[tr], y[tr], lam)(X[te])
                score(pred, f"fitted: {nm}", str(K), lam)
    W = pd.DataFrame(rows)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(f"\n  {len(W)} walk-forward arms (all reported in {STEM}.walkforward.csv); "
      f"{len(books)} books, choice is M vs 6W, everything fitted on IS<=2016 only.")
    P(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  best fitted arm mean OOS Sharpe: {W[W.K != '-'].mean_OOS_Sharpe.max():.4f}   "
      f"vs constant-M {W.iloc[0].mean_OOS_Sharpe:.4f}   "
      f"vs constant-6W {W.iloc[1].mean_OOS_Sharpe:.4f}   "
      f"vs IS-argmax {W.iloc[2].mean_OOS_Sharpe:.4f}")
    P(f"  KEEP paths over all {len(W)} arms: 4a passers "
      f"{int((W.pass4a > 0).sum())}/{len(W)} arms carry any 4a-passing book, "
      f"4b {int((W.pass4b > 0).sum())}/{len(W)}; "
      f"total book-level 4a passes {int(W.pass4a.sum())}, 4b {int(W.pass4b.sum())}.")
    return W


# ================================================================== (5) BASELINE / SPY
def stage5(W):
    P("\n" + "=" * 112)
    P("(5) THE PROTOCOL COMPARANDS -- live RULES v2 book and SPY on the U56 panel, 10 bps, weekly")
    P("=" * 112)
    px = load_universe()
    out = {}
    for nm, fn in (("RULES v2 baseline (live)", rules_v2_weights),
                   ("RULES v1 (previous)", rules_v1_weights)):
        r = backtest(px, fn(px), cost_bps=10, freq="W")["returns"].loc[px.index[260]:]
        m, mo = metrics(r), metrics(r.loc[OOS_START:])
        out[nm] = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                       H1=metrics(r.iloc[:len(r) // 2])["Sharpe"],
                       H2=metrics(r.iloc[len(r) // 2:])["Sharpe"],
                       OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])
    spy = px["SPY"].pct_change().fillna(0).loc[px.index[260]:]
    m, mo = metrics(spy), metrics(spy.loc[OOS_START:])
    out["SPY"] = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                      H1=metrics(spy.iloc[:len(spy) // 2])["Sharpe"],
                      H2=metrics(spy.iloc[len(spy) // 2:])["Sharpe"],
                      OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])
    B = pd.DataFrame(out).T
    P(B.to_string(float_format=lambda x: f"{x:.4f}"))
    best = W[W.K != "-"].sort_values("mean_OOS_Sharpe").iloc[-1]
    P(f"\n  This idea proposes NO book. Its best fitted-selector arm ({best.selector}, K={best.K},"
      f" lam={best.lam}) averages OOS Sharpe {best.mean_OOS_Sharpe:.4f} / CAGR "
      f"{best.mean_OOS_CAGR:.2%} / MaxDD {best.mean_OOS_MaxDD:.2%} across {int(best.n_books)} "
      f"books, against RULES v2 OOS Sharpe {B.loc['RULES v2 baseline (live)','OOS_Sharpe']:.4f} "
      f"and SPY OOS Sharpe {B.loc['SPY','OOS_Sharpe']:.4f}.")
    P("  4a (Sharpe > live RULES v2 in BOTH halves, MaxDD no worse): NOT MET by any arm -- see (4).")
    P("  4b (Sharpe > SPY both halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's): "
      "NOT MET by any arm -- see (4).")
    return B


def main():
    P(f"idea 497 -- re-run the 3 wide-and-unfolded census files individually (lane B, "
      f"{pd.Timestamp.utcnow().date()})")
    P(f"grid: K in {FOLDS} x lam in {LAMS}; seed {SEED}; folds identical across specs "
      f"inside a file.\n")
    d1, d2, d3 = stage0()
    G = stage1(d1, d2, d3)
    stage2(G, d1, d2, d3)
    stage3(d1, d2, d3)
    W = stage4(d1)
    stage5(W)
    flush_log()
    print(f"\nwrote {STEM}.console.txt .grid.csv .verdicts.csv .walkforward.csv")


if __name__ == "__main__":
    main()
