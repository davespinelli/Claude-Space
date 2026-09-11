#!/usr/bin/env python3
"""Idea 503 ADDENDUM (lane B, 2026-09-11) - no new backtests.

Reads ONLY the main run's committed artefacts (.percell.csv, .gross.csv, .grid_summary.csv)
and prices the two claims the main tables make visually:

  (1) the NOM form's non-monotonicity is the GROSS confound - rank-correlate the cell's 4b pass
      share against its realised gross, and against min(n, n_elig);
  (2) at fixed gross the share is monotone in min(n, n_elig), NOT in n - the k=20 cell saturates
      at n >= n_elig while the k=80 cell is still climbing at n=40.

Deterministic, seconds to run.  Writes .addendum.console.txt.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "research" / "backtests"
MAIN = "2026-09-11_is-the-4b-PASS-SHARE-a-monotone-function-of-n_B"
NS = [5, 10, 15, 20, 30, 40]
KS = [20, 40, 80]

_lines = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); _lines.append(s)

def spearman(a, b):
    a = pd.Series(a).rank(); b = pd.Series(b).rank()
    if a.std() == 0 or b.std() == 0: return np.nan
    return float(np.corrcoef(a, b)[0, 1])


def main():
    CE = pd.read_csv(OUT / f"{MAIN}.percell.csv")
    GR = pd.read_csv(OUT / f"{MAIN}.gross.csv")
    P("=" * 140)
    P("IDEA 503 ADDENDUM - the two mechanisms, as numbers (source: the main run's committed CSVs)")
    P("=" * 140)

    # long form: one row per (panel, k, n, form)
    rows = []
    for _, c in CE.iterrows():
        g = GR[(GR.panel == c.panel) & (GR.k == c.k)].iloc[0]
        for n in NS:
            for form in ("NOM", "MATCH"):
                rows.append(dict(panel=c.panel, k=int(c.k), n=n, form=form,
                                 n_elig=c.n_elig, share=c[f"{form}{n}"],
                                 gross=(g[f"n{n}"] if form == "NOM" else 0.75),
                                 nmin=min(n, c.n_elig)))
    L = pd.DataFrame(rows)
    L.to_csv(OUT / f"{MAIN}.addendum_long.csv", index=False)

    P("\n(1) WHAT THE PASS SHARE TRACKS - Spearman over the 18 (k, n) cell-points of a panel/form")
    P("    (SMALL484 is 0.000 in every cell, so its correlations are undefined and reported NaN.)")
    tab = []
    for pan in L.panel.unique():
        for form in ("NOM", "MATCH"):
            s = L[(L.panel == pan) & (L.form == form)]
            tab.append(dict(panel=pan, form=form, cells=len(s),
                            rho_vs_n=spearman(s.n, s.share),
                            rho_vs_nmin=spearman(s.nmin, s.share),
                            rho_vs_gross=spearman(s.gross, s.share)))
    T = pd.DataFrame(tab).set_index(["panel", "form"])
    P(T.to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n    NOM's gross column varies (0.114 - 0.740); MATCH's is 0.75 by construction, so")
    P("    rho_vs_gross is undefined there.  Read rho_vs_n against rho_vs_nmin.")

    P("\n(2) IS THE SHARE MONOTONE? - per k cell, strictly increasing in n over {5,10,15,20,30,40}")
    mono = []
    for pan in L.panel.unique():
        for form in ("NOM", "MATCH"):
            for k in KS:
                s = L[(L.panel == pan) & (L.form == form) & (L.k == k)].sort_values("n")
                v = s.share.values; ne = float(s.n_elig.iloc[0])
                sat = [n for n in NS if n >= ne]
                mono.append(dict(panel=pan, form=form, k=k, n_elig=ne,
                                 strict=bool(np.all(np.diff(v) > 0)),
                                 weak=bool(np.all(np.diff(v) >= -1e-12)),
                                 argmax_n=int(s.n.values[int(np.argmax(v))]),
                                 share_at_argmax=float(v.max()), share_at_n40=float(v[-1]),
                                 first_n_ge_nelig=(sat[0] if sat else None),
                                 spread_above_nelig=(float(np.ptp([x for n, x in zip(NS, v) if n >= ne]))
                                                     if sat else np.nan)))
    M = pd.DataFrame(mono)
    P(M.set_index(["panel", "form", "k"]).to_string(float_format=lambda x: f"{x:.4f}"))
    M.to_csv(OUT / f"{MAIN}.addendum_mono.csv", index=False)

    P("\n    'spread_above_nelig' = max-min of the pass share over the n rungs at or above the")
    P("    cell's mean n_elig.  Small = the dial has stopped moving, i.e. n is no longer a dial.")

    P("\n(3) THE 4a COUNT, SPLIT BY BOOK FORM (from .grid_summary.csv)")
    A = pd.read_csv(OUT / f"{MAIN}.grid_summary.csv")
    P(A.groupby("form")[["pass4a_v2", "pass4b", "both", "N"]].sum().to_string())
    P("\n    Every 4a pass in this run's 72,000 book-rows is in the DE-GROSSING (NOM) form.")
    P("    Holding gross at 0.75 removes all of them.")
    (OUT / f"{MAIN}.addendum.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
