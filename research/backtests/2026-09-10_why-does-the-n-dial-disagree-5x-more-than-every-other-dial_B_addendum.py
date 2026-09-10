#!/usr/bin/env python3
"""Idea 494 addendum — the LEVEL term's SIGN, and the queue's own premise, tested directly.

Reads only the committed artefacts of the parent run
(`2026-09-10_why-does-the-n-dial-disagree-5x-more-than-every-other-dial_B.cells.csv`).
No backtest is re-run; every number here is a re-read of that file.

WHY
    The parent found disagreement tracks the LEVEL gap (Spearman +0.937 across dials,
    logistic b +1.395) far better than the CURVATURE gap (+0.518, b +0.510), which is the
    OPPOSITE of the queue's hypothesis.  Two follow-ups are one line of arithmetic each:
      A. Is the level effect really a SIGN DISAGREEMENT — the two surfaces tilting toward
         OPPOSITE ends of the dial — rather than a magnitude difference?
      B. The queue's stated mechanism ("n moves realised gross AND concentration together
         while the other dials move one thing") is a claim about two measured covariates the
         parent already recorded per cell: `gross_range` and `nheld_ratio`.  Put them in the
         same logistic and see whether they explain anything the geometry does not.

Outputs: .signflip.csv .console.txt
"""
from __future__ import annotations
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
OUT = REPO / "research" / "backtests"
PARENT = "2026-09-10_why-does-the-n-dial-disagree-5x-more-than-every-other-dial_B"
STEM = Path(__file__).name[:-3]
SEED, N_PERM = 494, 20000

_log: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _log.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


def pbis(y, x):
    y, x = np.asarray(y, float), np.asarray(x, float)
    ok = np.isfinite(x)
    y, x = y[ok], x[ok]
    if len(y) < 3 or y.std() == 0 or x.std() == 0:
        return np.nan
    return float(np.corrcoef(y, x)[0, 1])


def perm_pbis(y, x, groups, seed=SEED, n=N_PERM):
    y, x, g = np.asarray(y, float), np.asarray(x, float), np.asarray(groups)
    ok = np.isfinite(x)
    y, x, g = y[ok], x[ok], g[ok]
    obs = pbis(y, x)
    if not np.isfinite(obs):
        return obs, np.nan
    rng = np.random.default_rng(seed)
    idx = {u: np.where(g == u)[0] for u in np.unique(g)}
    cnt = 0
    for _ in range(n):
        yp = y.copy()
        for u, ii in idx.items():
            yp[ii] = rng.permutation(y[ii])
        if abs(pbis(yp, x)) >= abs(obs) - 1e-12:
            cnt += 1
    return obs, (cnt + 1) / (n + 1)


def spearman(a, b):
    a, b = pd.Series(a).rank(), pd.Series(b).rank()
    if a.std() == 0 or b.std() == 0:
        return np.nan
    return float(np.corrcoef(a, b)[0, 1])


def logit(X, y, iters=200):
    X = np.column_stack([np.ones(len(y)), np.asarray(X, float)])
    y = np.asarray(y, float)
    b = np.zeros(X.shape[1])
    for _ in range(iters):
        p = 1.0 / (1.0 + np.exp(-X @ b))
        W = p * (1 - p) + 1e-9
        H = X.T @ (X * W[:, None]) + 1e-6 * np.eye(X.shape[1])
        step = np.linalg.solve(H, X.T @ (y - p))
        b = b + step
        if np.max(np.abs(step)) < 1e-9:
            break
    return b


def loglik(X, y, b):
    X = np.column_stack([np.ones(len(y)), np.asarray(X, float)])
    p = np.clip(1.0 / (1.0 + np.exp(-X @ b)), 1e-12, 1 - 1e-12)
    y = np.asarray(y, float)
    return float((y * np.log(p) + (1 - y) * np.log(1 - p)).sum())


def z(s):
    s = pd.Series(s, dtype=float)
    return ((s - s.mean()) / s.std()).values


def main():
    cl = pd.read_csv(OUT / f"{PARENT}.cells.csv")
    P(f"# {STEM}")
    P(f"# re-read of {PARENT}.cells.csv ({len(cl)} cells); no backtest re-run.\n")

    for split in ("CAL", "MID"):
        d = cl[cl.split == split].copy()
        d["SIGNFLIP"] = (np.sign(d.ORD_b1_S) != np.sign(d.ORD_b1_C)).astype(float)
        d["CURVFLIP"] = (np.sign(d.ORD_b2_S) != np.sign(d.ORD_b2_C)).astype(float)
        y = d.disagree.astype(float).values

        P(f"## {split} split — A. does the LEVEL term flip SIGN? ({len(d)} cells)")
        t = d.groupby(["dialset", "dial"]).agg(
            rate=("disagree", "mean"), SIGNFLIP=("SIGNFLIP", "mean"),
            CURVFLIP=("CURVFLIP", "mean"),
            LEVELGAP=("ORD_LEVELGAP", "mean"), CURVGAP=("ORD_CURVGAP", "mean"),
            b1_S=("ORD_b1_S", "mean"), b1_C=("ORD_b1_C", "mean"),
            gross_range=("gross_range", "mean"), nheld_ratio=("nheld_ratio", "mean"),
        ).sort_values("rate", ascending=False)
        P(fmt(t))
        P(f"  Spearman across the {len(t)} dials: rate vs SIGNFLIP {spearman(t.rate, t.SIGNFLIP):+.4f}"
          f"   rate vs CURVFLIP {spearman(t.rate, t.CURVFLIP):+.4f}"
          f"   rate vs nheld_ratio {spearman(t.rate, t.nheld_ratio):+.4f}"
          f"   rate vs gross_range {spearman(t.rate, t.gross_range):+.4f}")
        for nm in ("SIGNFLIP", "CURVFLIP", "nheld_ratio", "gross_range"):
            r, p = perm_pbis(y, d[nm].values, d.panel.values)
            P(f"  cell-level rate~{nm:<12} r {r:+.4f}  panel-clustered perm p {p:.4f}")
        P(f"  cells where the level term flips sign: {int(d.SIGNFLIP.sum())}/{len(d)}; "
          f"of those, {int(d.loc[d.SIGNFLIP == 1, 'disagree'].sum())} disagree "
          f"({d.loc[d.SIGNFLIP == 1, 'disagree'].mean():.1%}) vs "
          f"{d.loc[d.SIGNFLIP == 0, 'disagree'].mean():.1%} where it does not.")

        P(f"\n## {split} split — B. the queue's premise as covariates, against the geometry")
        specs = {
            "premise only  (nheld_ratio, gross_range)": ["nheld_ratio", "gross_range"],
            "geometry only (CURVGAP, LEVELGAP)":        ["ORD_CURVGAP", "ORD_LEVELGAP"],
            "curvature only(CURVGAP)":                  ["ORD_CURVGAP"],
            "level only    (LEVELGAP)":                 ["ORD_LEVELGAP"],
            "signflip only (SIGNFLIP)":                 ["SIGNFLIP"],
            "all four":                                 ["ORD_CURVGAP", "ORD_LEVELGAP",
                                                         "nheld_ratio", "gross_range"],
        }
        ll0 = loglik(np.zeros((len(y), 0)), y, logit(np.zeros((len(y), 0)), y))
        rows = []
        for nm, cols in specs.items():
            X = np.column_stack([z(d[c]) for c in cols])
            b = logit(X, y)
            ll = loglik(X, y, b)
            rows.append(dict(model=nm, k=len(cols), loglik=ll,
                             pseudoR2=1 - ll / ll0,
                             coefs=" ".join(f"{c.replace('ORD_','')}{v:+.3f}" for c, v in zip(cols, b[1:]))))
        P(fmt(pd.DataFrame(rows).set_index("model")))

        if split == "CAL":
            d.to_csv(OUT / f"{STEM}.signflip.csv", index=False)
            P(f"\n  -> {STEM}.signflip.csv")
        P("")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_log) + "\n")


if __name__ == "__main__":
    main()
