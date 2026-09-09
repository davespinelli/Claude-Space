#!/usr/bin/env python3
"""
Quality-growth screen (v2) for the Deep Value Desk.

Built after the first 82 deep dives showed that the cheapest names on the value
screen were cheap for a reason, and that the genuinely mispriced ones were hidden
behind GAAP artefacts (impairments, discontinued operations) the screen misread.

What changed versus screen.py
  * Growth is a gate, not a fifth of the score: revenue OR normalised operating
    profit must be growing in the last fiscal year AND not shrinking in the most
    recent quarter (year over year).
  * Profit is normalised: GAAP operating income + reported impairments (non-cash,
    non-recurring), taxed at 25%. The primary valuation metric is
    EV / normalised after-tax operating profit ("EV/NOPAT").
  * Debt is a gate: net debt / normalised EBITDA above 4x is excluded, 3-4x is
    penalised. Net-cash companies pass automatically.
  * Financials are no longer thrown away. Banks, brokers, insurers and holdcos
    get their own lane (P/E, P/TBV, ROTE, tangible book per share growth, every one
    of them on the common slice: see common_metrics());
    REITs and real-estate operators get P/FFO, FFO growth, dividend yield and a
    debt/assets gate. Industrial metrics are never applied to them.
  * Every row keeps an explicit `exclude_reason`, so "not on the list" is always
    explainable.

Outputs (all in research/deepvalue/)
  universe_v2.csv        every priced company in the $50M-$2B band, all lanes
  universe_under2b.csv   same rows in the legacy column layout (+ v2 columns) so
                         fetch_all.py / triage_pack.py keep working; ranked by v2
  QUALITY.md             ranked industrial qualifiers + GAAP-artefact watchlist
  FINANCIALS.md          ranked bank/insurer/broker and REIT qualifiers

Research output only, not investment advice.
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import screen as S  # noqa: E402  (shared fetchers, cache, filters)

HERE = S.HERE
TAX = 0.25                 # normalised tax rate applied to operating profit
EV_NOPAT_MAX = 20.0        # ranking ceiling for EV / normalised after-tax profit
LEV_MAX = 4.0              # net debt / normalised EBITDA: excluded above this
LEV_FLAG = 3.0             # penalised between LEV_FLAG and LEV_MAX
PE_MAX, PTBV_MAX = 12.0, 1.2      # financial lane: cheap on either
PFFO_MAX, REIT_DEBT_MAX = 15.0, 0.80   # REIT lane (liabilities / assets)
TOP_INDUSTRIAL, TOP_FIN, TOP_REIT = 60, 30, 20

# ---- extra XBRL concepts (registered into screen.py's tag tables) ----------
S.DUR_TAGS.update({
    # AssetImpairmentCharges is usually the total; the pieces are a fallback.
    "impair_total": ["AssetImpairmentCharges", "GoodwillAndIntangibleAssetImpairment"],
    "impair_gw": ["GoodwillImpairmentLoss"],
    "impair_intang": ["ImpairmentOfIntangibleAssetsExcludingGoodwill"],
    "impair_lla": ["ImpairmentOfLongLivedAssetsHeldForUse",
                   "ImpairmentOfLongLivedAssetsToBeDisposedOf"],
    "restructuring": ["RestructuringCharges"],
    "disc_ops": ["IncomeLossFromDiscontinuedOperationsNetOfTax"],
    "da": ["DepreciationDepletionAndAmortization", "DepreciationAndAmortization",
           "DepreciationAmortizationAndAccretionNet"],
    "dividends": ["PaymentsOfDividendsCommonStock", "PaymentsOfDividends"],
    # Common- and preferred-only cash dividends, so `dividends` (which falls back to
    # the combined PaymentsOfDividends tag) can be split. See common_metrics().
    "div_common": ["PaymentsOfDividendsCommonStock"],
    "div_pref_paid": ["PaymentsOfDividendsPreferredStockAndPreferenceStock"],
    # Income-statement preferred charge, and the direct "available to common" tag.
    "pref_div": ["PreferredStockDividendsAndOtherAdjustments",
                 "PreferredStockDividendsIncomeStatementImpact",
                 "DividendsPreferredStock"],
    "ni_avail_common": ["NetIncomeLossAvailableToCommonStockholdersBasic"],
    "interest_net": ["InterestIncomeExpenseNet"],
    "nonint_income": ["NoninterestIncome"],
    "premiums": ["PremiumsEarnedNet"],
})
S.INST_TAGS.update({
    "goodwill": ["Goodwill"],
    "intangibles": ["IntangibleAssetsNetExcludingGoodwill", "FiniteLivedIntangibleAssetsNet"],
    # Carrying value of preferred stock. Some filers tag par only and carry the rest
    # in APIC; PREF_LIQ_MIN in common_metrics() catches that case.
    "preferred": ["PreferredStockValue", "PreferredStockIncludingAdditionalPaidInCapital"],
    "preferred_liq": ["PreferredStockLiquidationPreferenceValue"],
})

# Most recent quarter vs the same quarter a year earlier, newest pair first.
QTR_PAIRS = [("CY2026Q2", "CY2025Q2"), ("CY2026Q1", "CY2025Q1"), ("CY2025Q4", "CY2024Q4")]

log = S.log


def quarter_yoy(tags: list[str]) -> tuple[pd.Series, pd.Series, pd.Series]:
    """Latest available quarter YoY: (growth where prior > 0, current value, prior value)."""
    cur_all = pd.Series(dtype="float64")
    prev_all = pd.Series(dtype="float64")
    for cur, prev in QTR_PAIRS:
        c = S.coalesce([S.frame("us-gaap", t, "USD", cur) for t in tags])
        p = S.coalesce([S.frame("us-gaap", t, "USD", prev) for t in tags])
        if c.empty or p.empty:
            continue
        both = c.index.intersection(p.index).difference(cur_all.index)
        if len(both) == 0:
            continue
        cur_all = pd.concat([cur_all, c[both]])
        prev_all = pd.concat([prev_all, p[both]])
    g = pd.Series(np.where(prev_all > 0, cur_all / prev_all - 1, np.nan), index=cur_all.index)
    return g, cur_all, prev_all


def nz(s: pd.Series) -> pd.Series:
    return s.fillna(0.0)


def col(f: pd.DataFrame, name: str) -> pd.Series:
    """A column, or an all-NaN column of the right index when the concept was never tagged."""
    return f[name] if name in f.columns else pd.Series(np.nan, index=f.index, dtype="float64")


def rank_hi(s: pd.Series) -> pd.Series:
    return s.rank(pct=True)


def rank_lo(s: pd.Series) -> pd.Series:
    return 1.0 - s.rank(pct=True)


def lane_of(sic: int, revenue: float) -> str:
    if 6798 == sic or 6500 <= sic <= 6599:
        return "reit"
    if 6000 <= sic <= 6799:
        return "financial"
    return "industrial"


# --------------------------------------------------------------------------- #
# metrics
# --------------------------------------------------------------------------- #
def industrial_metrics(f: pd.DataFrame) -> pd.DataFrame:
    f = f.copy()
    imp_parts = nz(f.impair_gw) + nz(f.impair_intang) + nz(f.impair_lla)
    f["impairment"] = np.maximum(nz(f.impair_total), imp_parts).clip(lower=0)
    imp_parts_p = nz(f.impair_gw_prior) + nz(f.impair_intang_prior) + nz(f.impair_lla_prior)
    f["impairment_prior"] = np.maximum(nz(f.impair_total_prior), imp_parts_p).clip(lower=0)

    f["ebit_norm"] = f.ebit + f.impairment
    f["ebit_norm_prior"] = f.ebit_prior + f.impairment_prior
    f["nopat"] = f.ebit_norm * (1 - TAX)
    f["ev_nopat"] = np.where((f.nopat > 0) & (f.ev > 0), f.ev / f.nopat, np.nan)
    f["ebitda_norm"] = f.ebit_norm + nz(f.da)
    lev = np.where(f.net_debt <= 0, 0.0,
                   np.where(f.ebitda_norm > 0, f.net_debt / f.ebitda_norm, np.inf))
    f["leverage"] = lev
    # No debt concept tagged: total liabilities (assets - equity) minus cash is the
    # upper bound on net debt. It overstates (payables, deferred revenue count), so
    # it is used only to EXCLUDE, never to call a company net cash.
    liab_net = (f.assets - f.equity - nz(f.cash)).clip(lower=0)
    f["leverage_upper"] = np.where(f.ltd_missing,
                                   np.where(f.ebitda_norm > 0, liab_net / f.ebitda_norm, np.inf),
                                   np.nan)
    invcap = f.equity + f.net_debt
    f["roic_norm"] = np.where(invcap > 0, f.nopat / invcap, np.nan)
    f["ebit_growth"] = np.where(f.ebit_norm_prior > 0, f.ebit_norm / f.ebit_norm_prior - 1, np.nan)
    f["ebit_turned_positive"] = (f.ebit_norm_prior <= 0) & (f.ebit_norm > 0) & f.ebit_norm_prior.notna()
    f["fcf_conv"] = np.where(f.nopat > 0, f.fcf / f.nopat, np.nan)

    bought = f.share_chg.notna() & (f.share_chg > S.SHARE_GROWTH_FLAG)
    q_rev_ok = f.rev_q_yoy.isna() | (f.rev_q_yoy > 0)
    q_ebit_ok = (f.ebit_q_yoy.isna() & ~(f.ebit_q_prev.notna() & (f.ebit_q_cur < f.ebit_q_prev))) \
        | (f.ebit_q_yoy > 0) | ((f.ebit_q_prev <= 0) & (f.ebit_q_cur > 0))
    f["growing_rev"] = (f.rev_growth > 0) & q_rev_ok & ~bought
    # Profit growth only counts as sustainable if revenue is not falling hard.
    rev_not_collapsing = (f.rev_growth.isna() | (f.rev_growth > -0.10)) & \
                         (f.rev_q_yoy.isna() | (f.rev_q_yoy > -0.10))
    f["growing_ebit"] = ((f.ebit_growth > 0) | f.ebit_turned_positive) & q_ebit_ok & rev_not_collapsing
    f["growing"] = f.growing_rev | f.growing_ebit

    # GAAP artefact: a loss or a depressed profit manufactured by a non-cash charge
    masked_loss = (f.impairment > 0) & (f.ebit <= 0) & (f.ebit_norm > 0)
    big_charge = (f.impairment > 0) & (f.ebit_norm > 0) & (f.impairment / f.ebit_norm > 0.25)
    disc_hit = f.disc_ops.notna() & (f.disc_ops < 0) & (f.disc_ops.abs() > 0.2 * f.net_income.abs())
    f["artifact_flag"] = masked_loss | big_charge | disc_hit
    note = np.where(masked_loss, "GAAP operating loss becomes a profit once the impairment is added back",
            np.where(big_charge, "impairment > 25% of normalised EBIT",
            np.where(disc_hit, "discontinued-ops loss > 20% of |net income|", "")))
    f["artifact_note"] = note
    f["restructuring_pct"] = np.where(f.ebit_norm > 0, nz(f.restructuring) / f.ebit_norm, np.nan)

    reason = pd.Series("", index=f.index, dtype="object")
    reason[~f.growing] = "not growing (revenue and normalised EBIT both flat/down, or growth bought with shares)"
    m = reason.eq("") & f.ev_nopat.isna()
    reason[m] = "no positive normalised after-tax profit"
    m = reason.eq("") & (f.ev_nopat > EV_NOPAT_MAX)
    reason[m] = f"EV/NOPAT above {EV_NOPAT_MAX:.0f}x"
    m = reason.eq("") & (f.leverage > LEV_MAX)
    reason[m] = f"net debt above {LEV_MAX:.0f}x normalised EBITDA"
    m = reason.eq("") & f.ltd_missing & (f.leverage_upper > LEV_MAX)
    reason[m] = f"no debt concept tagged and total liabilities exceed {LEV_MAX:.0f}x normalised EBITDA"
    f["exclude_reason"] = reason
    f["qualifies"] = reason.eq("")

    q = f[f.qualifies]
    growth_comp = pd.concat([q.rev_growth.clip(-0.5, 0.5),
                             q.ebit_growth.clip(-1.0, 1.0)], axis=1).mean(axis=1)
    score = (0.45 * rank_lo(q.ev_nopat).fillna(0.5)
             + 0.25 * rank_hi(growth_comp).fillna(0.5)
             + 0.15 * rank_hi(q.fcf_yield).fillna(0.5)
             + 0.15 * rank_hi(q.roic_norm).fillna(0.5)
             - 0.10 * ((q.leverage > LEV_FLAG) & (q.leverage <= LEV_MAX)).astype(float)
             + 0.05 * q.artifact_flag.astype(float)
             - 0.05 * q.ltd_missing.astype(float))
    f["score_v2"] = score.reindex(f.index)
    return f


# A preferred balance below this share of total equity is treated as par-only
# tagging, and the liquidation preference is used instead when it is available.
PREF_LIQ_MIN = 0.005


def common_metrics(f: pd.DataFrame) -> pd.DataFrame:
    """
    Split preferred stock out of equity, income and dividends.

    Market cap is a claim on the common only, so every metric that divides by it
    (P/E, P/TBV, dividend yield) or compares against it (ROTE, book per share)
    must use the common-only figure. Before this existed the screen divided market
    cap by *total* equity and *total* net income, which understated P/TBV and P/E
    for any bank, insurer or REIT with preferred outstanding, and counted preferred
    dividends as common yield. NEWT was the worked example: 0.89x tangible book and
    a 7.9% yield reported, 1.02x and 6.2% once $48.2M of Series B came out.

    Known limitation: preferred UNITS of an operating partnership (common in REITs,
    e.g. CSR's Series D and E) sit in noncontrolling interest or mezzanine rather
    than in StockholdersEquity, so PreferredStockValue does not see them and this
    function cannot deduct them. Those rows still need the filing read.
    """
    f = f.copy()
    pref = nz(col(f, "preferred"))
    liq = nz(col(f, "preferred_liq"))
    par_only = (pref < PREF_LIQ_MIN * f.equity.abs()) & (liq > pref)
    f["preferred"] = np.where(par_only, liq, pref)
    f["preferred_py"] = nz(col(f, "preferred_py"))

    f["common_equity"] = f.equity - f.preferred
    f["common_equity_py"] = f.equity_py - f.preferred_py
    f["ni_cont"] = f.net_income - nz(f.disc_ops)
    # Prefer the filer's own "available to common" tag; else back out the preferred charge.
    avail = col(f, "ni_avail_common")
    f["ni_common"] = np.where(avail.notna(),
                              avail - nz(f.disc_ops),
                              f.ni_cont - nz(col(f, "pref_div")))
    # `dividends` falls back to the combined PaymentsOfDividends tag, which includes
    # preferred. Use the common-only tag when the filer provides it.
    dc = col(f, "div_common")
    f["div_common"] = np.where(dc.notna(), dc,
                               nz(f.dividends) - nz(col(f, "div_pref_paid")))
    return f


def financial_metrics(f: pd.DataFrame) -> pd.DataFrame:
    f = common_metrics(f)
    # Total tangible equity is kept for reference; every ratio uses the common slice.
    f["tbv"] = f.equity - nz(f.goodwill) - nz(f.intangibles)
    f["tbv_common"] = f.tbv - f.preferred
    f["p_tbv"] = np.where(f.tbv_common > 0, f.mktcap / f.tbv_common, np.nan)
    f["pe"] = np.where(f.ni_common > 0, f.mktcap / f.ni_common, np.nan)
    f["rote"] = np.where(f.tbv_common > 0, f.ni_common / f.tbv_common, np.nan)
    bvps = f.common_equity / f.shares
    bvps_py = np.where((f.common_equity_py > 0) & (f.shares_py > 0),
                       f.common_equity_py / f.shares_py, np.nan)
    f["bvps_growth"] = np.where(bvps_py > 0, bvps / bvps_py - 1, np.nan)
    f["ni_growth"] = np.where(f.ni_prior > 0, f.ni_cont / f.ni_prior - 1, np.nan)
    f["div_yield"] = f.div_common / f.mktcap
    # The 5% gate is a solvency test, and preferred absorbs losses ahead of
    # depositors, so it stays on total equity. The common figure is reported beside it.
    f["equity_assets"] = np.where(f.assets > 0, f.equity / f.assets, np.nan)
    f["common_equity_assets"] = np.where(f.assets > 0, f.common_equity / f.assets, np.nan)
    f["growing"] = (f.bvps_growth > 0) | (f.ni_growth > 0)
    cheap = ((f.pe > 0) & (f.pe <= PE_MAX)) | ((f.p_tbv > 0) & (f.p_tbv <= PTBV_MAX))
    # A year's profit above 40% of common equity, or a P/E under 4, is almost always
    # a one-off (tax-asset release, gain on sale, reserve release). Flag, don't score.
    f["fin_eq_flag"] = ((f.ni_common > 0.4 * f.common_equity) | ((f.pe > 0) & (f.pe < 4))).map(
        {True: "net income > 40% of common equity or P/E < 4: likely one-off", False: ""})

    reason = pd.Series("", index=f.index, dtype="object")
    reason[~f.growing] = "tangible common book per share and continuing net income both not growing"
    m = reason.eq("") & ~cheap
    reason[m] = f"P/E above {PE_MAX:.0f}x and P/TBV above {PTBV_MAX:.1f}x"
    m = reason.eq("") & (f.equity_assets < 0.05)
    reason[m] = "equity below 5% of assets"
    m = reason.eq("") & f.pe.isna()
    reason[m] = "no positive continuing net income"
    f["exclude_reason"] = reason
    f["qualifies"] = reason.eq("")
    q = f[f.qualifies]
    score = (0.40 * rank_lo(q.pe).fillna(0.5)
             + 0.30 * rank_hi(q.rote).fillna(0.5)
             + 0.30 * rank_hi(q.bvps_growth).fillna(0.5)
             - 0.15 * q.fin_eq_flag.ne("").astype(float))
    f["score_v2"] = score.reindex(f.index)
    return f


def reit_metrics(f: pd.DataFrame) -> pd.DataFrame:
    f = common_metrics(f)
    # FFO to common: preferred dividends rank ahead of the shares market cap prices.
    f["ffo"] = f.ni_common + nz(f.da) + nz(f.impair_total)
    f["ffo_prior"] = f.ni_prior - nz(col(f, "pref_div_prior")) + nz(f.da_prior) + nz(f.impair_total_prior)
    f["p_ffo"] = np.where(f.ffo > 0, f.mktcap / f.ffo, np.nan)
    f["ffo_growth"] = np.where(f.ffo_prior > 0, f.ffo / f.ffo_prior - 1, np.nan)
    f["div_yield"] = f.div_common / f.mktcap
    # Total liabilities over assets: preferred is equity, not debt, so it stays out.
    f["debt_assets"] = np.where(f.assets > 0, (f.assets - f.equity) / f.assets, np.nan)
    f["growing"] = f.ffo_growth > 0

    reason = pd.Series("", index=f.index, dtype="object")
    reason[~f.growing] = "FFO not growing"
    m = reason.eq("") & f.p_ffo.isna()
    reason[m] = "no positive FFO"
    m = reason.eq("") & (f.p_ffo > PFFO_MAX)
    reason[m] = f"P/FFO above {PFFO_MAX:.0f}x"
    m = reason.eq("") & (f.debt_assets > REIT_DEBT_MAX)
    reason[m] = f"liabilities above {REIT_DEBT_MAX:.0%} of assets"
    f["exclude_reason"] = reason
    f["qualifies"] = reason.eq("")
    q = f[f.qualifies]
    score = (0.50 * rank_lo(q.p_ffo).fillna(0.5)
             + 0.30 * rank_hi(q.ffo_growth).fillna(0.5)
             + 0.20 * rank_hi(q.div_yield).fillna(0.5))
    f["score_v2"] = score.reindex(f.index)
    return f


# --------------------------------------------------------------------------- #
# "why" strings
# --------------------------------------------------------------------------- #
pct, num, money = S.pct, S.num, S.money


def why_industrial(r) -> str:
    bits = []
    if np.isfinite(r.rev_growth):
        q = f", last Q {pct(r.rev_q_yoy)}" if np.isfinite(r.rev_q_yoy) else ""
        bits.append(f"revenue {pct(r.rev_growth)} FY{q}")
    if np.isfinite(r.ebit_growth):
        bits.append(f"normalised EBIT {pct(r.ebit_growth)}")
    elif bool(r.ebit_turned_positive):
        bits.append("normalised EBIT turned positive")
    if np.isfinite(r.ev_nopat):
        bits.append(f"{r.ev_nopat:.1f}x EV/after-tax profit")
    if bool(r.ltd_missing):
        lu = f"{r.leverage_upper:.1f}x" if np.isfinite(r.leverage_upper) else "n/a"
        bits.append(f"debt untagged (total liabilities <= {lu} EBITDA)")
    elif r.net_debt <= 0:
        bits.append(f"net cash {money(-r.net_debt)}")
    elif np.isfinite(r.leverage) and r.leverage > 0:
        bits.append(f"{r.leverage:.1f}x net debt/EBITDA")
    if np.isfinite(r.fcf_yield):
        bits.append(f"FCF yield {pct(r.fcf_yield)}")
    if bool(r.artifact_flag):
        bits.append("GAAP ARTEFACT: " + str(r.artifact_note) + f" (impairment {money(r.impairment)})")
    eq = str(getattr(r, "eq_flag", "") or "")
    if eq and eq.lower() not in ("nan", "none"):
        bits.append("EARNINGS QUALITY: " + eq)
    if np.isfinite(r.fcf_conv) and r.fcf_conv < 0.3:
        bits.append(f"weak cash conversion (FCF/NOPAT {r.fcf_conv:.2f})")
    if bool(r.falling_knife):
        bits.append("WARNING 6m return below -40%")
    return "; ".join(bits)


def why_financial(r) -> str:
    bits = []
    if np.isfinite(r.pe):
        bits.append(f"{r.pe:.1f}x P/E")
    if np.isfinite(r.p_tbv):
        bits.append(f"{r.p_tbv:.2f}x tangible common book")
    if np.isfinite(r.rote):
        bits.append(f"ROTCE {pct(r.rote)}")
    if np.isfinite(r.bvps_growth):
        bits.append(f"tangible common BVPS {pct(r.bvps_growth)}")
    if np.isfinite(r.ni_growth):
        bits.append(f"net income {pct(r.ni_growth)}")
    if r.div_yield > 0:
        bits.append(f"dividend {pct(r.div_yield)}")
    if np.isfinite(r.equity_assets):
        bits.append(f"equity/assets {pct(r.equity_assets)}")
    if str(r.fin_eq_flag):
        bits.append("EARNINGS QUALITY: " + str(r.fin_eq_flag))
    eq = str(getattr(r, "eq_flag", "") or "")
    if eq and eq.lower() not in ("nan", "none"):
        bits.append("EARNINGS QUALITY: " + eq)
    return "; ".join(bits)


def why_reit(r) -> str:
    bits = []
    if np.isfinite(r.p_ffo):
        bits.append(f"{r.p_ffo:.1f}x P/FFO")
    if np.isfinite(r.ffo_growth):
        bits.append(f"FFO {pct(r.ffo_growth)}")
    if r.div_yield > 0:
        bits.append(f"dividend {pct(r.div_yield)}")
    if np.isfinite(r.debt_assets):
        bits.append(f"debt/assets {pct(r.debt_assets)}")
    return "; ".join(bits)


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
V2_COLS = ["lane", "rank_v2", "score_v2", "qualifies", "exclude_reason", "growing",
           "impairment", "ebit_norm", "ebit_prior", "ebit_growth", "nopat", "ev_nopat",
           "ebitda_norm", "leverage", "roic_norm", "fcf_conv", "rev_q_yoy", "rev_q_label",
           "ebit_q_yoy", "artifact_flag", "artifact_note", "restructuring", "disc_ops", "da",
           "dividends", "div_common", "goodwill", "intangibles", "preferred", "tbv",
           "tbv_common", "ni_common", "p_tbv", "pe", "rote",
           "bvps_growth", "ni_growth", "div_yield", "equity_assets", "common_equity_assets",
           "ffo", "p_ffo",
           "ffo_growth", "debt_assets", "leverage_upper", "fin_eq_flag", "why_v2"]


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description="Quality-growth screen v2")
    ap.add_argument("--no-legacy", action="store_true",
                    help="do not overwrite universe_under2b.csv")
    args = ap.parse_args(argv)
    t0 = time.time()
    stages: list[tuple[str, int]] = []

    uni = S.load_universe()
    S.prefetch_all()

    log("assembling fundamentals")
    A = S.annual_concept
    rev, rev_per, rev_prior = A("revenue")
    ni, _, ni_prior = A("net_income")
    ebit, ebit_per, ebit_prior = A("op_income")
    cfo, _, _ = A("cfo")
    capex, _, _ = A("capex")
    extra = {}
    for name in ["impair_total", "impair_gw", "impair_intang", "impair_lla", "restructuring",
                 "disc_ops", "da", "dividends", "div_common", "div_pref_paid", "pref_div",
                 "ni_avail_common", "interest_net", "nonint_income", "premiums"]:
        v, _, vp = A(name)
        extra[name] = v
        extra[name + "_prior"] = vp
    equity, equity_per, _ = S.instant_concept("equity", S.INSTANT_PERIODS)
    equity_py, _, _ = S.instant_concept("equity", S.INSTANT_PERIODS_PY)
    pref, _, _ = S.instant_concept("preferred", S.INSTANT_PERIODS)
    pref_liq, _, _ = S.instant_concept("preferred_liq", S.INSTANT_PERIODS)
    pref_py, _, _ = S.instant_concept("preferred", S.INSTANT_PERIODS_PY)
    assets, _, _ = S.instant_concept("assets", S.INSTANT_PERIODS)
    goodwill, _, _ = S.instant_concept("goodwill", S.INSTANT_PERIODS)
    intang, _, _ = S.instant_concept("intangibles", S.INSTANT_PERIODS)
    ltd, ltd_per, ltd_tag = S.instant_concept("ltd", S.INSTANT_PERIODS)
    ltd, ltd_per, ltd_tag, _ = S.fill_ltd_fallbacks(ltd, ltd_per, ltd_tag)
    cash, _, _ = S.instant_concept("cash", S.INSTANT_PERIODS)
    sh, sh_per = S.shares_concept(S.INSTANT_PERIODS)
    sh_py, sh_py_per = S.shares_concept(S.INSTANT_PERIODS_PY)
    alt_sh, alt_sh_per = S.alt_shares_concept(S.INSTANT_PERIODS)
    alt_sh_py, alt_sh_py_per = S.alt_shares_concept(S.INSTANT_PERIODS_PY)
    wanso_chg, wanso_lab = S.wanso_yoy()
    log("quarterly year-over-year")
    rev_q, rev_q_cur, rev_q_prev = quarter_yoy(S.REV_TAGS)
    ebit_q, ebit_q_cur, ebit_q_prev = quarter_yoy(S.DUR_TAGS["op_income"])

    f = pd.DataFrame(dict(
        revenue=rev, revenue_prior=rev_prior, revenue_period=rev_per,
        net_income=ni, ni_prior=ni_prior, ebit=ebit, ebit_period=ebit_per, ebit_prior=ebit_prior,
        cfo=cfo, capex=capex, equity=equity, equity_period=equity_per, equity_py=equity_py,
        preferred=pref, preferred_liq=pref_liq, preferred_py=pref_py,
        assets=assets, goodwill=goodwill, intangibles=intang,
        ltd=ltd, ltd_period=ltd_per, ltd_tag=ltd_tag, cash=cash,
        shares=sh, shares_period=sh_per, shares_py=sh_py, shares_py_period=sh_py_per,
        alt_shares=alt_sh, alt_shares_period=alt_sh_per,
        alt_shares_py=alt_sh_py, alt_shares_py_period=alt_sh_py_per,
        wanso_chg=wanso_chg, wanso_label=wanso_lab,
        rev_q_yoy=rev_q, rev_q_cur=rev_q_cur, rev_q_prev=rev_q_prev,
        ebit_q_yoy=ebit_q, ebit_q_cur=ebit_q_cur, ebit_q_prev=ebit_q_prev,
        **extra))
    f.index.name = "cik"
    f = f.join(uni, how="inner")
    stages.append(("CIKs with USD XBRL frame data + a ticker", len(f)))

    fin_rev = nz(f.interest_net) + nz(f.nonint_income) + nz(f.premiums)
    f = f[f.shares.notna() & (f.shares > 0) & (f.shares < 5e9)
          & ((f.revenue > S.REV_MIN) | (fin_rev > S.REV_MIN))]
    stages.append((f"shares outstanding + revenue (or interest/premium income) > ${S.REV_MIN/1e6:.0f}M", len(f)))

    prices = S.fetch_prices(sorted(f.yf.unique().tolist()))
    f = f.join(prices, on="yf", how="inner")
    stages.append(("priced by yfinance (>=130 trading days)", len(f)))
    f["mktcap"] = f.price * f.shares
    f = f[(f.mktcap >= S.UNIVERSE_MIN) & (f.mktcap <= S.UNIVERSE_MAX)]
    stages.append((f"market cap ${S.UNIVERSE_MIN/1e6:.0f}M - ${S.UNIVERSE_MAX/1e9:.0f}B", len(f)))
    f = f[f.adv20 > S.ADV_MIN]
    stages.append((f"20d avg dollar volume > ${S.ADV_MIN/1e6:.0f}M", len(f)))

    sic = S.fetch_sic(sorted(f.index.unique()))
    f = f.join(sic, how="left")
    f["sic"] = f.sic.fillna(0).astype(int)
    f = f[~(f.sic.isin(S.SIC_BIOTECH) & (f.revenue < S.BIOTECH_REV_MIN))]
    stages.append((f"exclude clinical-stage biotech (drug SIC, revenue < ${S.BIOTECH_REV_MIN/1e6:.0f}M)", len(f)))
    f["lane"] = [lane_of(s, r) for s, r in zip(f.sic, f.revenue)]

    ind = f.lane.eq("industrial")
    ind_ok = ind & (f.revenue > S.REV_MIN) & f.ebit.notna() & (f.ebit > -0.25 * f.revenue) & f.cfo.notna()
    fin_ok = f.lane.eq("financial") & f.net_income.notna() & (f.equity > 0)
    reit_ok = f.lane.eq("reit") & f.net_income.notna() & (f.equity > 0)
    f = f[ind_ok | fin_ok | reit_ok]
    stages.append(("lane data requirements (industrial: op income & CFO; financial/REIT: net income & equity)", len(f)))
    n_lane = f.lane.value_counts().to_dict()
    log(f"lanes: {n_lane}")

    # legacy metrics (net_debt, ev, fcf, roic, share_chg, eq_flag, ...) for every row
    f = S.compute_metrics(f)

    parts = []
    g = f[f.lane.eq("industrial")]
    if len(g):
        parts.append(industrial_metrics(g))
    g = f[f.lane.eq("financial")]
    if len(g):
        parts.append(financial_metrics(g))
    g = f[f.lane.eq("reit")]
    if len(g):
        parts.append(reit_metrics(g))
    f = pd.concat(parts)
    for c in V2_COLS:
        if c not in f.columns:
            f[c] = np.nan
    f["rev_q_label"] = np.where(f.rev_q_yoy.notna(), "latest reported quarter vs same quarter prior year", "")

    def why_row(r) -> str:
        if r.lane == "industrial":
            return why_industrial(r)
        if r.lane == "financial":
            return why_financial(r)
        return why_reit(r)
    f["why_v2"] = [why_row(r) for _, r in f.iterrows()]

    # ranks: qualifiers by score within lane; non-qualifiers after, by legacy score
    f["rank_v2"] = np.nan
    for lane in ["industrial", "financial", "reit"]:
        m = f.lane.eq(lane) & f.qualifies
        f.loc[m, "rank_v2"] = f.loc[m, "score_v2"].rank(ascending=False, method="first")
    f = f.sort_values(["qualifies", "score_v2", "score"], ascending=[False, False, False])
    f.insert(0, "rank", range(1, len(f) + 1))
    stages.append(("qualify on growth + valuation + leverage gates (all lanes)", int(f.qualifies.sum())))

    f.to_csv(HERE / "universe_v2.csv", index=True)
    log(f"wrote {HERE/'universe_v2.csv'}")
    if not args.no_legacy:
        legacy = f.copy()
        for c in S.OUT_COLS:
            if c not in legacy.columns:
                legacy[c] = np.nan
        legacy["why"] = np.where(legacy.why_v2.astype(str) != "", legacy.why_v2, legacy.get("why", ""))
        cols = ["rank"] + [c for c in S.OUT_COLS if c != "rank"] + [c for c in V2_COLS if c not in S.OUT_COLS]
        legacy[cols].to_csv(HERE / "universe_under2b.csv", index=True)
        log(f"wrote {HERE/'universe_under2b.csv'} ({len(legacy)} rows, v2 order)")

    write_markdown(f, stages, t0)


def write_markdown(f: pd.DataFrame, stages, t0) -> None:
    asof = dt.date.today().isoformat()
    ind = f[f.lane.eq("industrial")]
    q = ind[ind.qualifies].sort_values("rank_v2")

    L = [f"# Quality-Growth Screen (v2) -- US small caps $50M-$2B -- {asof}", "",
         "Free data only: SEC XBRL frames for fundamentals, SEC submissions for SIC codes, yfinance for "
         "prices. Generated by `research/deepvalue/screen_v2.py`. **Research output only, not investment "
         "advice.** Every number below is a tagged XBRL figure, not a read of the filing; the deep-dive "
         "note is where the filing gets read.", "",
         "## Gates (a company must pass all three)", "",
         "1. **Growing.** Revenue up in the last fiscal year and not down in the latest quarter year over year "
         "(growth alongside share-count growth above 15% does not count), OR normalised operating profit up in "
         "the last fiscal year and not down in the latest quarter.",
         f"2. **Priced sensibly.** EV / normalised after-tax operating profit between 0 and {EV_NOPAT_MAX:.0f}x, "
         f"where normalised = GAAP operating income + reported impairments, taxed at {TAX:.0%}.",
         f"3. **Not over-levered.** Net debt / normalised EBITDA at or below {LEV_MAX:.0f}x ({LEV_FLAG:.0f}-{LEV_MAX:.0f}x is penalised). "
         "Net cash passes. When no debt concept is tagged, total liabilities minus cash stand in as an upper bound and only ever exclude.", "",
         "Score among qualifiers = 0.45 x rank(cheapness on EV/NOPAT) + 0.25 x rank(growth, mean of revenue and "
         "normalised EBIT growth) + 0.15 x rank(FCF yield) + 0.15 x rank(normalised ROIC), -0.10 if leverage is "
         "in the penalty band, +0.05 if a GAAP artefact hides the profit (that is where the reading is worth most), "
         "-0.05 if no debt concept was tagged.", "",
         "## Filter stages", "", "| # | Stage | Companies |", "|---|---|---|"]
    for i, (label, n) in enumerate(stages, 1):
        L.append(f"| {i} | {label} | {n:,} |")
    L += ["", f"Lanes: industrial {int(f.lane.eq('industrial').sum())}, financial "
          f"{int(f.lane.eq('financial').sum())}, REIT/real estate {int(f.lane.eq('reit').sum())}. "
          f"Industrial qualifiers: {len(q)}. Financial and REIT lanes are in FINANCIALS.md.", ""]

    L += [f"## Ranked industrial qualifiers (top {TOP_INDUSTRIAL})", "",
          "| # | Ticker | Company | Industry | Mkt cap | Price | Rev FY | Rev last Q | Norm EBIT | EV/NOPAT | ND/EBITDA | FCF yld | Why |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in q.head(TOP_INDUSTRIAL).iterrows():
        eg = pct(r.ebit_growth) if np.isfinite(r.ebit_growth) else ("turned +" if r.ebit_turned_positive else "n/a")
        if bool(r.ltd_missing):
            lev = f"untagged (<= {r.leverage_upper:.1f}x)" if np.isfinite(r.leverage_upper) else "untagged"
        else:
            lev = "net cash" if r.net_debt <= 0 else (f"{r.leverage:.1f}x" if np.isfinite(r.leverage) else "n/a")
        L.append(f"| {int(r.rank_v2)} | {r.ticker} | {str(r['name'])[:40]} | {str(r.get('sic_desc',''))[:28]} | "
                 f"{money(r.mktcap)} | ${r.price:.2f} | {pct(r.rev_growth)} | {pct(r.rev_q_yoy)} | {eg} | "
                 f"{r.ev_nopat:.1f}x | {lev} | {pct(r.fcf_yield)} | {r.why_v2} |")

    art = ind[ind.artifact_flag].sort_values("ev_nopat")
    L += ["", "## GAAP-artefact watchlist (all industrial rows with a masking charge, qualifying or not)", "",
          "These are the rows where GAAP operating income and normalised operating income disagree by a "
          "non-cash charge. The value screen read them as losses or as expensive; several of the desk's best "
          "notes (NX, SMP, ROCK, SXC) came from exactly this pattern.", "",
          "| Ticker | Company | Mkt cap | GAAP EBIT | Impairment | Norm EBIT | EV/NOPAT | Growing | Qualifies | Note |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in art.iterrows():
        evn = f"{r.ev_nopat:.1f}x" if np.isfinite(r.ev_nopat) else "n/a"
        qq = "yes" if r.qualifies else f"no: {r.exclude_reason}"
        L.append(f"| {r.ticker} | {str(r['name'])[:40]} | {money(r.mktcap)} | {money(r.ebit)} | "
                 f"{money(r.impairment)} | {money(r.ebit_norm)} | {evn} | {'yes' if r.growing else 'no'} | {qq} | {r.artifact_note} |")

    L += ["", "## Why the rest were excluded", "", "| Reason | Companies |", "|---|---|"]
    for reason, n in ind[~ind.qualifies].exclude_reason.value_counts().items():
        L.append(f"| {reason} | {n} |")
    L += ["", f"_Runtime {time.time()-t0:.0f}s. Columns for every row are in universe_v2.csv._"]
    (HERE / "QUALITY.md").write_text("\n".join(L) + "\n")
    log(f"wrote {HERE/'QUALITY.md'}")

    # ---- financials -------------------------------------------------------
    fin = f[f.lane.eq("financial")]
    qf = fin[fin.qualifies].sort_values("rank_v2")
    re_ = f[f.lane.eq("reit")]
    qr = re_[re_.qualifies].sort_values("rank_v2")
    M = [f"# Financials & REIT Screen (v2) -- {asof}", "",
         "Banks, brokers, insurers and holding companies (SIC 6000-6799 except real estate) are scored on "
         f"P/E, price to tangible book, return on tangible equity and tangible book-per-share growth, all on the "
         "common slice: preferred stock is deducted from equity and preferred dividends from earnings, because "
         "market cap only buys the common. Gates: growing "
         f"(tangible BVPS or continuing net income up), cheap (P/E <= {PE_MAX:.0f}x or P/TBV <= {PTBV_MAX:.1f}x), equity "
         "at least 5% of assets. REITs and real-estate operators (SIC 6798, 6500-6599) are scored on P/FFO "
         f"(FFO = net income + D&A + impairments), FFO growth and dividend yield; gates: FFO growing, P/FFO <= {PFFO_MAX:.0f}x, "
         f"total liabilities <= {REIT_DEBT_MAX:.0%} of assets. Generated by `research/deepvalue/screen_v2.py`. "
         "**Research output only, not investment advice.** XBRL tags for financials are inconsistent; treat every "
         "row as a prompt to read the 10-K, not as a fact.", "",
         f"Financial lane: {len(fin)} companies, {len(qf)} qualify. REIT lane: {len(re_)} companies, {len(qr)} qualify.", "",
         f"## Banks, brokers, insurers, holdcos (top {TOP_FIN})", "",
         "| # | Ticker | Company | Industry | Mkt cap | Price | P/E | P/TBV | ROTE | TBVPS growth | NI growth | Div yld | Equity/assets |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in qf.head(TOP_FIN).iterrows():
        pe = f"{r.pe:.1f}x" if np.isfinite(r.pe) else "n/a"
        pt = f"{r.p_tbv:.2f}x" if np.isfinite(r.p_tbv) else "n/a"
        M.append(f"| {int(r.rank_v2)} | {r.ticker} | {str(r['name'])[:40]} | {str(r.get('sic_desc',''))[:28]} | "
                 f"{money(r.mktcap)} | ${r.price:.2f} | {pe} | {pt} | {pct(r.rote)} | {pct(r.bvps_growth)} | "
                 f"{pct(r.ni_growth)} | {pct(r.div_yield)} | {pct(r.equity_assets)} |")
    M += ["", f"## REITs and real estate (top {TOP_REIT})", "",
          "| # | Ticker | Company | Industry | Mkt cap | Price | P/FFO | FFO growth | Div yld | Liabilities/assets |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in qr.head(TOP_REIT).iterrows():
        pf = f"{r.p_ffo:.1f}x" if np.isfinite(r.p_ffo) else "n/a"
        M.append(f"| {int(r.rank_v2)} | {r.ticker} | {str(r['name'])[:40]} | {str(r.get('sic_desc',''))[:28]} | "
                 f"{money(r.mktcap)} | ${r.price:.2f} | {pf} | {pct(r.ffo_growth)} | {pct(r.div_yield)} | {pct(r.debt_assets)} |")
    M += ["", "## Why the rest were excluded", "", "| Lane | Reason | Companies |", "|---|---|---|"]
    for lane, grp in [("financial", fin), ("reit", re_)]:
        for reason, n in grp[~grp.qualifies].exclude_reason.value_counts().items():
            M.append(f"| {lane} | {reason} | {n} |")
    (HERE / "FINANCIALS.md").write_text("\n".join(M) + "\n")
    log(f"wrote {HERE/'FINANCIALS.md'}")


if __name__ == "__main__":
    main()
