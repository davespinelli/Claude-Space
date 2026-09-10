#!/usr/bin/env python3
"""Idea 665 ADDENDUM -- the SCRAMBLE placebo of the main run is contaminated; re-price both
ladders on a warm-up-clean COMMON WINDOW.   (lane C, 2026-09-10)

WHY THIS EXISTS.  The main script's placebo reads the gate state at a large PAST offset O in
[252, 1008].  `state.shift(O)` is False for the first O rows, so at O=1008 the book is ALL CASH
for roughly the first four years of the evaluation window (verified: U56 TREND at O=1008 has its
first non-empty day on 2012-10-15, and mean ON share over 2009-2013 is 0.115 vs 0.676 at O=42).
A long flat stretch cannot draw down, so the main run's placebo MaxDD is FLATTERED and its
"saturated scale" (mean dMaxDD -0.03..-0.09 pp) is an artefact, not a measurement.  The same
contamination touches the L=63 rung of the headline ladder for the first weeks of the window.

WHAT THIS ADDENDUM DOES.  Everything is recomputed on ONE window that is clean for every arm:
    CW = px.index[260 + PLACEBO_HI]  (the latest first-valid day any arm can have)
Both the lag ladder AND the placebo draws are scored on CW, each against an L=0 control scored on
CW too.  Nothing else changes: same families, same lags, same offsets, same seed, same gross 0.75,
same 10 bps, same next-day execution.

WHAT SURVIVES OR NOT IS REPORTED EITHER WAY.  The two claims under test:
  C1  the staleness tax is paid in DRAWDOWN rather than in RETURN (the queue's question)
  C2  intermediate staleness costs MORE drawdown than TOTAL de-alignment (frac_sat > 1) -- the
      main run's striking number, and exactly the one the artefact could have manufactured

The rule-8 walk-forward in the main run is NOT affected: its OOS window opens 2017-01-01, which is
years past the warm-up of any L <= 63 arm.  Its numbers stand as published.

Deterministic, standalone, no network.  Writes .console.txt .cw_tax.csv .cw_placebo.csv.
Modifies nothing.
"""
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe  # noqa: E402
from engine import backtest, metrics  # noqa: E402

MAIN = OUT / "2026-09-10_is-the-STALENESS-TAX-a-DRAWDOWN-tax-on-every-gate-family_C.py"
sys.path.insert(0, str(OUT))
main_mod = __import__(MAIN.stem)
gate_state, book, gate_work = main_mod.gate_state, main_mod.book, main_mod.gate_work
FAMILIES, LAGS = main_mod.FAMILIES, main_mod.LAGS
COST, FREQ, CURRENCY_BAR = main_mod.COST, main_mod.FREQ, main_mod.CURRENCY_BAR
PLACEBO_DRAWS, PLACEBO_LO, PLACEBO_HI, SEED = (main_mod.PLACEBO_DRAWS, main_mod.PLACEBO_LO,
                                               main_mod.PLACEBO_HI, main_mod.SEED)
GROSS = 0.75

LINES = []


def P(s=""):
    print(s)
    LINES.append(str(s))


def stats(px, start, w):
    r = backtest(px, w, cost_bps=COST, freq=FREQ)["returns"].loc[start:]
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"], m["Vol"]


def main():
    t0 = time.time()
    P(f"Idea 665 ADDENDUM -- warm-up-clean common window   (lane C, {pd.Timestamp.today().date()})")
    P(f"PROTOCOL: {COST:.0f} bps, next-day execution, freq {FREQ}, gross {GROSS:.2f} throughout.")
    P(f"Common window CW = index[260 + {PLACEBO_HI}]: every arm (lag and placebo alike) is fully")
    P("warmed up there, so the L=0 control, the lag ladder and the placebo see the SAME days.")
    P()

    panels = {"U56": load_universe(), "B136": load_universe(broad=True),
              "SMALL484": load_universe(small=True)}
    rng = np.random.default_rng(SEED)
    offs = {f: rng.integers(PLACEBO_LO, PLACEBO_HI + 1, PLACEBO_DRAWS) for f in FAMILIES}

    trows, prows = [], []
    for pname, px in panels.items():
        cw = px.index[260 + PLACEBO_HI]
        P(f"  --- {pname} --- CW {cw.date()} -> {px.index[-1].date()}  "
          f"({(px.index[-1] - cw).days / 365.25:.1f} years; the main run used "
          f"{px.index[260].date()} ->)")
        for fam in FAMILIES:
            st = gate_state(px, fam)
            c0, s0, d0, v0 = stats(px, cw, book(px, fam, 0, GROSS, state_cache=st))
            P(f"    {fam:8s} L=0 on CW: CAGR {c0:7.2%}  Sharpe {s0:.3f}  MaxDD {d0:7.2%}")
            lad = []
            for L in LAGS:
                c, s, d, v = stats(px, cw, book(px, fam, L, GROSS, state_cache=st))
                rc = -(c - c0) / abs(c0)
                rd = -(d - d0) / abs(d0)
                cur = ("NONE" if L == 0 else "DD_TAX" if rd > CURRENCY_BAR * rc else
                       "RETURN_TAX" if rc > CURRENCY_BAR * rd else "MIXED")
                lad.append(dict(panel=pname, family=fam, lag=L, CAGR=c, Sharpe=s, MaxDD=d, Vol=v,
                                dCAGR=c - c0, dSharpe=s - s0, dMaxDD_pp=(d - d0) * 100,
                                r_CAGR=rc, r_DD=rd, currency=cur))
            pl = []
            for o in offs[fam]:
                c, s, d, v = stats(px, cw, book(px, fam, 0, GROSS, state_cache=st, offset=int(o)))
                pl.append(dict(panel=pname, family=fam, offset=int(o), CAGR=c, Sharpe=s, MaxDD=d,
                               dCAGR=c - c0, dSharpe=s - s0, dMaxDD_pp=(d - d0) * 100,
                               r_CAGR=-(c - c0) / abs(c0), r_DD=-(d - d0) / abs(d0)))
            PLf = pd.DataFrame(pl)
            sat_dd = float(PLf.dMaxDD_pp.mean())
            sat_sd = float(PLf.dMaxDD_pp.std())
            sat_cg = float(PLf.dCAGR.mean())
            for row in lad:
                row["sat_dMaxDD_pp"] = sat_dd
                row["sat_sd_dMaxDD_pp"] = sat_sd
                row["sat_dCAGR"] = sat_cg
                row["frac_sat_DD"] = row["dMaxDD_pp"] / sat_dd if sat_dd else np.nan
                row["z_vs_sat_DD"] = (row["dMaxDD_pp"] - sat_dd) / sat_sd if sat_sd else np.nan
            trows += lad
            prows += pl
            P(f"      SCRAMBLE ({PLACEBO_DRAWS} draws, offsets {PLACEBO_LO}..{PLACEBO_HI}): "
              f"dCAGR {sat_cg:+7.2%}  dMaxDD {sat_dd:+6.2f} pp (sd {sat_sd:.2f}, "
              f"min {PLf.dMaxDD_pp.min():+6.2f} max {PLf.dMaxDD_pp.max():+6.2f})")
            for row in lad:
                if row["lag"] == 0:
                    continue
                P(f"      L={row['lag']:>3d}  dCAGR {row['dCAGR'] * 100:+6.2f} pp  "
                  f"dSharpe {row['dSharpe']:+.3f}  dMaxDD {row['dMaxDD_pp']:+6.2f} pp  "
                  f"r_CAGR {row['r_CAGR']:+.3f} r_DD {row['r_DD']:+.3f}  {row['currency']:10s} "
                  f"frac of SCRAMBLE DD {row['frac_sat_DD']:+6.2f}  z {row['z_vs_sat_DD']:+6.2f}")
        P()

    T = pd.DataFrame(trows)
    PL = pd.DataFrame(prows)

    P("=" * 100)
    P("(C1) THE CURRENCY, on the clean window")
    P("=" * 100)
    tal = T[T.lag > 0].groupby("currency").size().sort_values(ascending=False)
    n = int(T[T.lag > 0].shape[0])
    for k, v in tal.items():
        P(f"   {k:10s} {v:3d} / {n}  ({v / n:.1%})")
    P()
    P("   by FAMILY (L>0, all three panels pooled):")
    for fam in FAMILIES:
        s = T[(T.lag > 0) & (T.family == fam)]
        P(f"     {fam:8s} DD_TAX {int((s.currency == 'DD_TAX').sum()):2d}  "
          f"RETURN_TAX {int((s.currency == 'RETURN_TAX').sum()):2d}  "
          f"MIXED {int((s.currency == 'MIXED').sum()):2d}   of {len(s)};  "
          f"median r_DD {s.r_DD.median():+.3f}  median r_CAGR {s.r_CAGR.median():+.3f}")
    hit = T[T.lag.isin([42, 63])]
    P(f"\n   at the reported rungs [42, 63]: DD_TAX {int((hit.currency == 'DD_TAX').sum())} / "
      f"{len(hit)}  ({(hit.currency == 'DD_TAX').mean():.1%})   "
      f"(main run, contaminated window: 18/24 = 75.0%)")

    P()
    P("=" * 100)
    P("(C2) IS INTERMEDIATE STALENESS WORSE THAN TOTAL DE-ALIGNMENT?")
    P("=" * 100)
    P("   frac_sat_DD > 1 means the L-day-stale read gives up MORE drawdown than a fully")
    P("   de-aligned read of the same gate.  z is that gap in SCRAMBLE draw sd.")
    s = T[T.lag.isin([21, 42, 63])]
    worse = int((s.z_vs_sat_DD < -1.0).sum())
    P(f"   L in [21,42,63]: {worse} / {len(s)} arms are MORE than 1 draw-sd WORSE in MaxDD than")
    P(f"   their own SCRAMBLE mean;  median frac_sat_DD {s.frac_sat_DD.median():+.2f}, "
      f"median z {s.z_vs_sat_DD.median():+.2f}")
    for _, r in s.sort_values("z_vs_sat_DD").head(8).iterrows():
        P(f"     {r.panel:8s} {r.family:8s} L={int(r.lag):>3d}  dMaxDD {r.dMaxDD_pp:+6.2f} pp vs "
          f"SCRAMBLE {r.sat_dMaxDD_pp:+6.2f} (sd {r.sat_sd_dMaxDD_pp:.2f})  z {r.z_vs_sat_DD:+.2f}")

    P()
    for nm, df in (("cw_tax", T), ("cw_placebo", PL)):
        p = OUT / f"{STEM}.{nm}.csv"
        df.to_csv(p, index=False)
        P(f"  wrote {p.name}  ({len(df)} rows)")
    P(f"\ntotal {time.time() - t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
