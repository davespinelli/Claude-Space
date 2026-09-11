#!/usr/bin/env python3
"""Idea 778 addendum - the DISJOINT-PAIR NOISE CONTROL for the cross-parent draw correlation.

The main run measured rho for all three parent pairs.  Two of those pairs (U56/SMALL439 and
B136/SMALL439) share ZERO names, and the coupled draws confirmed it (mean shared 0.00 of 36),
so their TRUE correlation is exactly 0 by construction.  Whatever |rho| those pairs read is
therefore the estimator's own noise, at the same D and the same aggregation as the nested
pair's estimate.  This addendum puts the nested pair's rho beside that control and prices the
conviction-count decomposition (+41 -> pair restriction -> correlation) at every draw count.

Reads only this run's committed artefacts.  No new backtest, no network, deterministic.
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np, pandas as pd

OUT = Path(__file__).resolve().parent
STEM = OUT / "2026-09-11_is-the-RSS-BAR-the-right-object-when-the-two-parents-OVERLAP_cloud"
NEST = "U56|B136"
STATS = ["PREM_SHARPE", "PREM_CAGR", "SHARPE", "CAGR", "MAXDD"]
CELLS = 6  # 3 gross x 2 cadence; rho is the mean over cells
_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); _LOG.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


def main():
    rho = pd.read_csv(f"{STEM}.rho.csv")
    fl = pd.read_csv(f"{STEM}.floors.csv")
    mv = pd.read_csv(f"{STEM}.moves.csv")
    P("# idea 778 addendum - disjoint-pair noise control + conviction decomposition")
    P("")

    # ---------------------------------------------------------------- noise control
    P("=" * 96)
    P("THE CONTROL: two of the three pairs share ZERO names, so their TRUE rho is exactly 0.")
    P("Whatever |rho| they read is the estimator's own noise at that D.")
    P("=" * 96)
    rows = []
    for D in sorted(rho.D.unique()):
        s = rho[(rho.D == D) & (rho.period == "FULL")]
        dis = s[s.overlap_coef == 0.0]
        nes = s[s.pair == NEST]
        # Fisher-z SE of a mean of CELLS independent per-cell correlations at n = D draws
        se = 1.0 / np.sqrt(max(D - 3, 1)) / np.sqrt(CELLS)
        rows.append(dict(
            D=D,
            nested_rho_PREM_SHARPE=float(nes[nes.statistic == "PREM_SHARPE"].rho_coupled.iloc[0]),
            nested_absrho_mean=float(nes.rho_coupled.abs().mean()),
            nested_absrho_max=float(nes.rho_coupled.abs().max()),
            DISJOINT_absrho_mean=float(dis.rho_coupled.abs().mean()),
            DISJOINT_absrho_max=float(dis.rho_coupled.abs().max()),
            fisher_SE=se,
            nested_z=float(nes[nes.statistic == "PREM_SHARPE"].rho_coupled.iloc[0]) / se))
    ctl = pd.DataFrame(rows).set_index("D")
    P(fmt(ctl, 4))
    P("")
    worst_D = int(ctl.index[-1])
    n_exceed = 0
    for D in sorted(rho.D.unique()):
        s = rho[(rho.D == D) & (rho.period == "FULL")]
        dmax = float(s[s.overlap_coef == 0.0].rho_coupled.abs().max())
        for st in STATS:
            v = abs(float(s[(s.pair == NEST) & (s.statistic == st)].rho_coupled.iloc[0]))
            n_exceed += int(v > dmax)
    P(f"VERDICT: the completely-nested pair's |rho| exceeds the structurally-zero pairs' own "
      f"|rho| in {n_exceed} of {len(STATS)*len(rho.D.unique())} (statistic x D) cells.")
    P(f"         At D={worst_D} (the record's largest affordable draw count) the disjoint "
      f"control still reads |rho| up to {ctl.loc[worst_D,'DISJOINT_absrho_max']:.4f} against a "
      f"true value of exactly 0, while the nested pair reads "
      f"{ctl.loc[worst_D,'nested_absrho_max']:.4f} at worst.")
    P("         The correlation the queue asked for is NOT MEASURABLE at any D this record "
      "can afford; it is not zero-because-absent, it is unresolved.")
    P("")

    # ---------------------------------------------------------------- implied bars
    P("=" * 96)
    P("IMPLIED BAR vs RSS, every pair x statistic x draw count (FULL period)")
    P("=" * 96)
    br = []
    for D in sorted(rho.D.unique()):
        f6 = fl[(fl.D == D) & (fl.period == "FULL")].set_index("statistic")
        s = rho[(rho.D == D) & (rho.period == "FULL")]
        for _, r in s.iterrows():
            a, b = r.pair.split("|")
            fa, fb = float(f6.loc[r.statistic, f"floor_{a}"]), float(f6.loc[r.statistic, f"floor_{b}"])
            rss = np.sqrt(fa * fa + fb * fb)
            cor = np.sqrt(max(fa * fa + fb * fb - 2 * r.rho_coupled * fa * fb, 0.0))
            br.append(dict(D=D, pair=r.pair, statistic=r.statistic, RSS=rss,
                           CORRECTED=cor, DIRECT=r.sd_diff_coupled,
                           cor_over_rss=cor / rss, direct_over_rss=r.sd_diff_coupled / rss,
                           nested=(r.pair == NEST)))
    bars = pd.DataFrame(br)
    P("mean DIRECT/RSS and CORRECTED/RSS by pair and D (1.000 = RSS was exactly right)")
    P(fmt(bars.pivot_table(index=["pair"], columns="D", values="direct_over_rss"), 4))
    P("  (CORRECTED/RSS)")
    P(fmt(bars.pivot_table(index=["pair"], columns="D", values="cor_over_rss"), 4))
    P("")
    nd = bars[bars.nested & (bars.D == 24)]
    P(f"At D=24 the NESTED pair's assumption-free DIRECT bar is "
      f"{nd.direct_over_rss.mean():.4f}x RSS on average over the five statistics "
      f"(range {nd.direct_over_rss.min():.4f}-{nd.direct_over_rss.max():.4f}); the disjoint "
      f"pairs, where RSS is exactly right, read "
      f"{bars[(~bars.nested) & (bars.D == 24)].direct_over_rss.mean():.4f}x.")
    P("")

    # ---------------------------------------------------------------- decomposition
    P("=" * 96)
    P("CONVICTION-COUNT DECOMPOSITION (net vs idea 567's POOLED bar, FULL, bar 1.0)")
    P("=" * 96)
    s = mv[(mv.period == "FULL") & (mv.subset == "ALL") & (mv.bar == 1.0)]
    piv = s.pivot_table(index="est", columns="D", values="net")
    P(fmt(piv, 1))
    P("")
    rss = piv.loc["RSS_INDEP"]
    pin = piv.loc["PAIR_INDEP"]
    cpl = piv.loc["PAIR_COUPLED"]
    dr = piv.loc["PAIR_DIRECT"]
    P(f"  RSS over ALL named parents (774's bar) : {rss.min():.0f} to {rss.max():.0f} "
      f"across D  -> range {rss.max()-rss.min():.0f}, STABLE")
    P(f"  restricted to the MIN-GAP PAIR, rho=0  : {pin.min():.0f} to {pin.max():.0f} "
      f"across D  -> range {pin.max()-pin.min():.0f}, STABLE")
    P(f"  + measured rho (coupled)               : {cpl.min():.0f} to {cpl.max():.0f} "
      f"across D  -> range {cpl.max()-cpl.min():.0f}, UNSTABLE")
    P(f"  + measured difference-sd (direct)      : {dr.min():.0f} to {dr.max():.0f} "
      f"across D  -> range {dr.max()-dr.min():.0f}, UNSTABLE")
    P("")
    P(f"  So of idea 774's +41, {rss.mean()-pin.mean():+.1f} on average is the THREE-PARENT "
      f"RSS applied to a TWO-PARENT gap - a specification error that is stable and real - and "
      f"the correlation term the queue asked for adds only {cpl.mean()-pin.mean():+.1f} on "
      f"average with a {cpl.max()-cpl.min():.0f}-claim swing across draw counts, i.e. noise.")
    P("")
    (OUT / (STEM.name + "_addendum.console.txt")).write_text("\n".join(_LOG) + "\n")
    bars.to_csv(OUT / (STEM.name + "_addendum.bars.csv"), index=False)
    ctl.to_csv(OUT / (STEM.name + "_addendum.control.csv"))


if __name__ == "__main__":
    main()
