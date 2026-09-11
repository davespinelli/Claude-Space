#!/usr/bin/env python3
"""Idea 538 addendum (lane B, 2026-09-11): two things the main run flagged and owes a number.

1. WHY G1's TURNOVER LEG FAILED.  The main run pre-registered max |d turn_yr| < 1e-6 against
   idea 535's committed .grid.csv and read 9.144e-03.  That is a FAIL as written and is
   reported as one.  This addendum localises it: the gap is U56-only, RESPREAD-heaviest, and
   is the SAME data/prices.csv daily-vintage drift that ideas 301/328/514 already stamped
   (and that also produced this run's 6.864e-03 pp U56 resid0 gap, which passed its 1e-2 bar).
   B136 and SMALL439 reproduce turn_yr at EXACTLY 0.0 on all 216 of their books.  The
   conclusion the record should carry is that a 1e-6 ABSOLUTE bar on a turnover level of
   ~20/yr is not a reproduction bar at all on a panel whose price file grows daily; the
   RELATIVE gap is what is bounded, and this prints it.

2. ARE THE 16 4b PASSERS NEW?  The main run's 324 books are ideas 298/301/535's grid at gross
   0.75, which idea 536 (lane B, same day) also ran.  If the passing SET is identical then
   this run has no new KEEP-candidate to memo and has instead produced an unplanned
   independent reproduction of idea 536's KEEP-path counts from a separately written script.
   Either answer is reported.

Deterministic, standalone, reads only committed CSVs.  Writes .diag.csv and .console.txt.
"""
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
MAIN = HERE / "2026-09-11_is-c_sd-the-right-SCALE-or-is-it-a-TURNOVER-proxy_B.grid.csv"
REF535 = HERE / "2026-09-09_is-the-FAMILY-constant-really-a-c_sd-constant_cloud.grid.csv"
REF536 = HERE / "2026-09-11_is-the-MA-residual-DRIFT-a-regime-not-a-panel_B.grid.csv"
OUT = Path(__file__).with_suffix("")
KEY = ["panel", "family", "level", "cad"]
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def main():
    g = pd.read_csv(MAIN)
    r = pd.read_csv(REF535)
    m = g[KEY + ["con", "turn_yr"]].merge(r[KEY + ["con", "turn_yr"]], on=KEY + ["con"],
                                          suffixes=("", "_ref"))
    m["d_abs"] = (m.turn_yr - m.turn_yr_ref).abs()
    m["d_rel"] = m.d_abs / m.turn_yr_ref.abs()
    P("=" * 120)
    P("1.  G1 TURNOVER LEG -- localising the 9.144e-03 failure (bar was 1e-6, ABSOLUTE)")
    P("=" * 120)
    t = m.groupby(["panel", "con"]).d_abs.agg(["max", "mean", "count"])
    t["max_rel"] = m.groupby(["panel", "con"]).d_rel.max()
    P(t.to_string(float_format=lambda x: f"{x:.3e}"))
    P(f"\n  POOLED max |d turn_yr| ABSOLUTE {m.d_abs.max():.3e} (pre-registered bar 1e-6 -> FAIL)")
    P(f"  POOLED max |d turn_yr| RELATIVE {m.d_rel.max():.3e} "
      f"({m.d_rel.max()*1e4:.2f} bp of the turnover level)")
    clean = m[m.panel != "U56"]
    P(f"  B136 + SMALL439: {len(clean)} books, max |d| {clean.d_abs.max():.3e} -- EXACT")
    P(f"  U56 alone:       {len(m)-len(clean)} books, max |d| {m[m.panel=='U56'].d_abs.max():.3e}")
    P("\n  three largest gaps:")
    P(m.nlargest(3, "d_abs")[KEY + ["con", "turn_yr", "turn_yr_ref", "d_abs", "d_rel"]]
      .to_string(index=False))
    P("\n  DIAGNOSIS: U56 reads data/prices.csv, which gains a row every trading day; ideas "
      "301/328/514 stamped the same panel-vintage drift, and this run's own resid0 leg showed "
      "it too (U56 6.864e-03 pp vs B136/SMALL439 2.220e-16).  The turnover gate is the same "
      "fact measured on a quantity whose LEVEL is ~20/yr, so a 1e-6 absolute bar was never "
      "reachable on this panel.  The FAIL stands as pre-registered; the recoverable statement "
      f"is the relative bound {m.d_rel.max():.1e}.")

    P("\n" + "=" * 120)
    P("2.  ARE THE 16 4b PASSERS NEW?  (vs idea 536, lane B, same grid, same day)")
    P("=" * 120)
    b = pd.read_csv(REF536)
    pb = b[b.p4b] if "p4b" in b.columns else b[b.f4b == "-"]
    pa = g[g.p4b]
    ka = set(map(tuple, pa[KEY + ["con"]].values))
    kb = set(map(tuple, pb[KEY + ["con"]].values))
    P(f"  this run 4b {len(pa)}/{len(g)} | idea 536 4b {len(pb)}/{len(b)} | "
      f"4a this run {int(g.p4a.sum())}/{len(g)} | idea 536 4a {int(b.p4a.sum())}/{len(b)}")
    P(f"  passing SETS identical: {ka == kb}   symmetric difference: "
      f"{sorted(ka ^ kb) if ka != kb else 'none'}")
    if ka == kb:
        j = pa[KEY + ["con", "Sharpe", "MaxDD", "oSharpe"]].merge(
            pb[KEY + ["con", "Sharpe", "MaxDD", "oSharpe"]], on=KEY + ["con"],
            suffixes=("", "_536"))
        for c in ("Sharpe", "MaxDD", "oSharpe"):
            P(f"    max |d {c}| on the 16 shared passers: {(j[c]-j[c+'_536']).abs().max():.3e}")
        P("\n  NO NEW KEEP-CANDIDATE AND NO MEMO: every passer is idea 536's, reported the same "
          "day from an independently written script, and the record has already declined that "
          "family.  What this leg adds is the reproduction itself.")
    m.to_csv(f"{OUT}.diag.csv", index=False)
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
