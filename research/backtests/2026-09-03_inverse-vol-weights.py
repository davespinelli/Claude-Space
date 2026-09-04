#!/usr/bin/env python3
"""Idea 7: inverse-vol-weights.

RULES v1 selection is kept EXACTLY (top 5 by baseline.score with the 200d-MA and
vol20 < 0.60 eligibility filters, weekly rebalance). Only the sizing changes: the 5
selected names are weighted proportional to 1/vol20 instead of a flat 15% each.

Three runs (10 bps costs, freq="W"):
  (a) inv-vol @ 75% gross  -- same total exposure as RULES v1 (5 x 15%), directly comparable
  (b) inv-vol @ 100% gross -- fully invested
  (c) equal-weight @ 100% gross -- diagnostic, isolates exposure from weighting

Standalone and deterministic. Run: .venv/bin/python research/backtests/2026-09-03_inverse-vol-weights.py
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np  # noqa: E402
from baseline import load_universe, score, compare  # noqa: E402

SCRIPT = "research/backtests/2026-09-03_inverse-vol-weights.py"
N = 5
MAX_VOL = 0.60


def _selection(px):
    """RULES v1 selection mask + the vol20 panel. Identical to rules_v1_weights."""
    s, above, vol20 = score(px, vol_scale=True)
    elig = s.where(above & (vol20 < MAX_VOL))
    rank = elig.rank(axis=1, ascending=False)
    sel = (rank <= N).astype(float)
    return sel, vol20


def inv_vol_weights(px, gross):
    """Same 5 names as v1, sized proportional to 1/vol20, scaled to `gross` total."""
    sel, vol20 = _selection(px)
    inv = sel * (1.0 / vol20.clip(lower=0.08))
    tot = inv.sum(axis=1)
    w = inv.div(tot.where(tot > 0), axis=0) * gross
    return w.fillna(0.0)


def equal_weights(px, gross):
    """Same 5 names as v1, equal-weighted, scaled to `gross` total."""
    sel, _ = _selection(px)
    tot = sel.sum(axis=1)
    w = sel.div(tot.where(tot > 0), axis=0) * gross
    return w.fillna(0.0)


def main():
    px = load_universe()
    print(f"Universe: {px.shape[1]} tickers, {px.index[0].date()} -> {px.index[-1].date()}, {len(px)} rows\n")

    variants = [
        ("inv-vol 75% gross", lambda p: inv_vol_weights(p, 0.75)),
        ("inv-vol 100% gross", lambda p: inv_vol_weights(p, 1.00)),
        ("equal-weight 100% gross (diagnostic)", lambda p: equal_weights(p, 1.00)),
    ]

    out = []
    for name, fn in variants:
        print("=" * 78)
        print(name)
        print("=" * 78)
        w = fn(px)
        gs = w.sum(axis=1)
        gs = gs[gs > 0]
        print(f"  rows with positions: {len(gs)}  mean gross: {gs.mean():.3f}  "
              f"min/max single weight (when held): "
              f"{w[w > 0].min().min():.3f}/{w.max().max():.3f}")
        res = compare(name, fn, px, freq="W", cost_bps=10)
        out.append((name, res))
        print()

    print("=" * 78)
    print("LEADERBOARD rows (script column fixed to filename)")
    print("=" * 78)
    for name, res in out:
        line = res["row"].rstrip()
        assert line.endswith("|")
        parts = line.split(" | ")
        parts[-1] = SCRIPT + " |"
        print(" | ".join(parts))


if __name__ == "__main__":
    np.random.seed(0)
    main()
