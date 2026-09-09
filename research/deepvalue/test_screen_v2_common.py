#!/usr/bin/env python3
"""
Offline checks on the common-vs-total-equity fix in screen_v2.common_metrics().

No network: the frames are hand-built from filed figures, so this runs anywhere.
NEWT is the worked example (10-Q 2026-08-10 and 8-K 2026-08-06 Ex-99.1). Run with
`python3 research/deepvalue/test_screen_v2_common.py`.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import screen_v2 as V  # noqa: E402

FAILURES: list[str] = []


def close(label: str, got: float, want: float, tol: float) -> None:
    ok = np.isfinite(got) and abs(got - want) <= tol
    print(f"  {'PASS' if ok else 'FAIL'}  {label}: got {got:.4f}, want {want:.4f} (+/-{tol})")
    if not ok:
        FAILURES.append(label)


def newt_row() -> pd.DataFrame:
    """NewtekOne at 30 Jun 2026, $ thousands, priced at the 2026-09-09 screen close."""
    return pd.DataFrame([dict(
        equity=413_373.0,          # total shareholders' equity
        equity_py=312_180.0,       # 30 Jun 2025, includes $19,738 Series A
        preferred=48_181.0,        # Series B
        preferred_py=19_738.0,     # Series A
        preferred_liq=np.nan,
        net_income=65_454.0,       # TTM Q3-25..Q2-26
        ni_prior=50_853.0,
        disc_ops=np.nan,
        pref_div=3_989.0,          # TTM preferred dividends
        ni_avail_common=np.nan,    # force the pref_div fallback path
        dividends=28_044.0,        # PaymentsOfDividends: common AND preferred
        div_common=np.nan,         # filer did not tag the common-only concept
        div_pref_paid=6_044.0,
        goodwill=14_085.0,
        intangibles=441.0,
        assets=3_184_881.0,
        shares=28_899.0,
        shares_py=26_317.0,
        mktcap=28_899.0 * 12.33,
        da=np.nan, da_prior=np.nan,
        impair_total=np.nan, impair_total_prior=np.nan,
    )], index=pd.Index([1587987], name="cik"))


def test_newt() -> None:
    print("NEWT (financial lane), 30 Jun 2026:")
    r = V.financial_metrics(newt_row()).iloc[0]
    # Tangible common book $350,666k / 28,899 sh = $12.13; $12.33 / $12.13 = 1.016x.
    close("p_tbv on tangible COMMON book", r.p_tbv, 1.016, 0.01)
    close("tangible common book", r.tbv_common, 350_666.0, 1.0)
    # $61,465k to common / 28,899 sh = $2.13 TTM EPS; $12.33 / $2.13 = 5.80x.
    close("pe on income available to COMMON", r.pe, 5.80, 0.05)
    close("rote on common", r.rote, 0.1753, 0.002)
    # Common dividends only: $28,044 - $6,044 = $22,000 / mktcap $356.3M = 6.2%.
    close("div_yield excludes preferred", r.div_yield, 0.0618, 0.001)
    # Common BVPS $365,192/28,899 = $12.64 vs $292,442/26,317 = $11.11 -> +13.8%.
    close("bvps_growth on common equity", r.bvps_growth, 0.1377, 0.003)
    # Solvency gate stays on total equity; the common figure is reported beside it.
    close("equity_assets stays on TOTAL equity", r.equity_assets, 0.1298, 0.001)
    close("common_equity_assets", r.common_equity_assets, 0.1147, 0.001)


def test_regression_vs_old() -> None:
    """The old math is what shipped in FINANCIALS.md; show the fix actually moves it."""
    print("\nOld (buggy) versus new, same inputs:")
    f = newt_row()
    old_tbv = f.equity[1587987] - f.goodwill[1587987] - f.intangibles[1587987]
    old_p_tbv = f.mktcap[1587987] / old_tbv
    old_pe = f.mktcap[1587987] / f.net_income[1587987]
    old_yld = f.dividends[1587987] / f.mktcap[1587987]
    new = V.financial_metrics(f).iloc[0]
    for label, o, n in [("P/TBV", old_p_tbv, new.p_tbv),
                        ("P/E", old_pe, new.pe),
                        ("dividend yield", old_yld, new.div_yield)]:
        print(f"  {label}: {o:.4f} -> {n:.4f}")
    if not (old_p_tbv < new.p_tbv and old_pe < new.pe and old_yld > new.div_yield):
        FAILURES.append("fix did not move P/TBV up, P/E up and yield down")


def test_no_preferred_unchanged() -> None:
    """A filer with no preferred must come out exactly where it did before."""
    print("\nNo preferred outstanding (must be unchanged):")
    f = newt_row()
    for c in ["preferred", "preferred_py", "preferred_liq", "pref_div", "div_pref_paid"]:
        f[c] = np.nan
    r = V.financial_metrics(f).iloc[0]
    close("p_tbv equals total-equity result", r.p_tbv,
          f.mktcap[1587987] / (413_373.0 - 14_085.0 - 441.0), 0.001)
    close("pe equals total-income result", r.pe, f.mktcap[1587987] / 65_454.0, 0.001)
    close("div_yield equals total-dividend result", r.div_yield, 28_044.0 / f.mktcap[1587987], 0.001)


def test_par_only_tagging() -> None:
    """Par-value-only tagging falls back to the liquidation preference."""
    print("\nPar-only preferred tagging ($1k par, $50M liquidation preference):")
    f = newt_row()
    f["preferred"] = 1.0
    f["preferred_liq"] = 50_000.0
    r = V.financial_metrics(f).iloc[0]
    close("preferred picked up from liquidation preference", r.preferred, 50_000.0, 1.0)


def test_reit_lane() -> None:
    """REIT lane: FFO is after preferred, yield is common-only."""
    print("\nREIT lane with preferred:")
    f = pd.DataFrame([dict(
        equity=500_000.0, equity_py=480_000.0, preferred=100_000.0, preferred_py=100_000.0,
        preferred_liq=np.nan, net_income=40_000.0, ni_prior=36_000.0, disc_ops=np.nan,
        pref_div=8_000.0, pref_div_prior=8_000.0, ni_avail_common=np.nan,
        dividends=30_000.0, div_common=np.nan, div_pref_paid=8_000.0,
        goodwill=np.nan, intangibles=np.nan, assets=1_000_000.0,
        shares=20_000.0, shares_py=20_000.0, mktcap=300_000.0,
        da=50_000.0, da_prior=48_000.0, impair_total=np.nan, impair_total_prior=np.nan,
    )], index=pd.Index([9999], name="cik"))
    r = V.reit_metrics(f).iloc[0]
    close("ffo after preferred dividends", r.ffo, 82_000.0, 1.0)      # 40,000-8,000+50,000
    close("p_ffo", r.p_ffo, 300_000.0 / 82_000.0, 0.01)
    close("div_yield excludes preferred", r.div_yield, 22_000.0 / 300_000.0, 0.001)
    close("debt_assets unchanged by preferred", r.debt_assets, 0.5, 0.001)


if __name__ == "__main__":
    test_newt()
    test_regression_vs_old()
    test_no_preferred_unchanged()
    test_par_only_tagging()
    test_reit_lane()
    print()
    if FAILURES:
        print(f"{len(FAILURES)} FAILED: " + "; ".join(FAILURES))
        sys.exit(1)
    print("all checks passed")
