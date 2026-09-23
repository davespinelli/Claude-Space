#!/usr/bin/env python3
"""Cal-Maine (CALM) quarterly nowcast: public egg price -> revenue -> operating income -> EPS.

Every estimate for quarter t uses only (a) CALM numbers reported for quarters <= t-1 and (b) public
prices covering quarter t (complete at quarter end, about 30 days before CALM reports).

Revenue
  M_t        = USDA (ERS) Grade A large "Combined regional" wholesale price, $/dozen, averaged over the
               fiscal quarter's exact dates shifted back 7 days (best-fitting lag, see fit_prices()).
  conv price = a + b*M_t (OLS on all quarters before t) + rho * (last quarter's fit error)
  spec price = last quarter's specialty price + beta_s * (M_t - M_{t-1})     (beta_s: OLS on prior quarters)
  dozens     = same quarter a year ago x last reported quarter's year-on-year growth (week-adjusted)
               + disclosed acquisitions (live quarter only: Eggland's Best Northeast territory)
  other rev  = egg products + prepared foods + other = last quarter's level
Costs (the operating-leverage step)
  shell COGS per dozen sold c_t = c_anchor + k*(M_t - M_anchor) + phi*(feed_t - feed_anchor) + drift
      k   = how much Cal-Maine's cost per dozen moves with the market price (eggs it buys from others),
      phi = pass-through of modelled feed cost per dozen (corn + soybean meal, 6-month window lagged 30 days),
      both fitted on prior quarters; anchor = last quarter (default) or the same quarter a year ago.
  other-revenue COGS = (1 - 20%) x other revenue (assumed 20% gross margin)
  SG&A      = same quarter a year ago x trailing-4-quarter SG&A growth (keeps the Q4 year-end bump in Q4)
  other income = year-ago other income + last quarter's year-on-year change
  tax       = trailing-4-quarter effective rate (clipped 15-35%); minority interest = last quarter's
  EPS       = net income attributable / last quarter's diluted shares (live: latest share count)
"""
import json, sys
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import load_quarters, load_prices, daily, qavg, DATA  # noqa: E402

G_NS = 0.20          # assumed gross margin on non-shell-egg revenue (egg products, prepared foods, other)
FEED = dict(a=0.0921, corn=0.0610, sbm100=0.0336)   # refit in fit_feed(); defaults for reference
PRICE_COL, PRICE_LAG = "ers_combined", 7


# ---------------------------------------------------------------- inputs
def build_inputs(Q, P, price_col=PRICE_COL, lag=PRICE_LAG):
    d = daily(P[price_col])
    dc, ds = daily(P.corn), daily(P.sbm.ffill())
    Q = Q.copy()
    Q["M"] = [qavg(d, r.period_start, r.period_end, lag) for r in Q.itertuples()]
    Q["corn6"] = [qavg(dc, r.period_start - pd.Timedelta(days=90), r.period_end, 30) for r in Q.itertuples()]
    Q["sbm6"] = [qavg(ds, r.period_start - pd.Timedelta(days=90), r.period_end, 30) for r in Q.itertuples()]
    Q["rel_cogs"] = Q.rel_cogs.fillna(Q.rel_net_sales - Q.rel_gross_profit)
    Q["c"] = (Q.rel_cogs - Q.nonshell_sales * (1 - G_NS)) / Q.total_doz
    Q["nci"] = Q.rel_pretax - Q.rel_tax - Q.rel_ni_attr
    return Q


def fit_feed(Q, upto):
    """feed cost per dozen produced ~ corn + soybean meal (prior quarters only)."""
    h = Q.iloc[:upto].dropna(subset=["feed_per_doz", "corn6", "sbm6"])
    X = np.c_[np.ones(len(h)), h.corn6, h.sbm6 / 100]
    b, *_ = np.linalg.lstsq(X, h.feed_per_doz, rcond=None)
    return b


def feed_hat(b, row):
    return b[0] + b[1] * row.corn6 + b[2] * row.sbm6 / 100


def ols(x, y):
    X = np.c_[np.ones(len(x)), x]
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    return b


# ---------------------------------------------------------------- one estimate
def estimate(Q, t, anchor="last", rho=0.5, trend="last", win=12, live=None):
    """Estimate quarter index t from rows < t. `live` may override inputs for the live quarter."""
    live = live or {}
    H = Q.iloc[:t]
    r = Q.iloc[t]
    bf = fit_feed(Q, t)
    fh = np.array([feed_hat(bf, x) for x in Q.itertuples()])
    # --- conventional price
    h = H.dropna(subset=["M", "conv_price"])
    if win:
        h = h.tail(win)   # rolling window: Cal-Maine's contract mix (market vs grain-based) changes over time
    a, b = ols(h.M.values, h.conv_price.values)
    resid_last = H.conv_price.iloc[-1] - (a + b * H.M.iloc[-1])
    conv_price = a + b * r.M + rho * resid_last
    # --- specialty price
    dS = H.spec_price.diff().values[1:]
    dM = H.M.diff().values[1:]
    ok = ~np.isnan(dS) & ~np.isnan(dM)
    beta_s = float(np.dot(dM[ok], dS[ok]) / np.dot(dM[ok], dM[ok]))
    spec_price = H.spec_price.iloc[-1] + beta_s * (r.M - H.M.iloc[-1])
    # --- volumes: year-ago x last quarter's YoY growth, per week
    wk = Q.weeks.values

    def vol(col):
        if trend == "last":   # last reported quarter's year-on-year growth, per week
            g = (H[col].iloc[-1] / wk[t - 1]) / (H[col].iloc[-5] / wk[t - 5])
        else:                 # trailing four quarters vs the four before, per week
            g = (H[col].iloc[-4:].sum() / wk[t - 4:t].sum()) / (H[col].iloc[-8:-4].sum() / wk[t - 8:t - 4].sum())
        return H[col].iloc[-4] / wk[t - 4] * g * wk[t]
    conv_doz = vol("conv_doz") * live.get("conv_doz_adj", 1.0)
    spec_doz = vol("spec_doz_all") * live.get("spec_doz_adj", 1.0)
    total_doz = conv_doz + spec_doz
    nonshell = live.get("nonshell", H.nonshell_sales.iloc[-1])
    revenue = conv_doz * conv_price + spec_doz * spec_price + nonshell
    # --- cost per dozen
    lagk = 1 if anchor == "last" else 4
    c = H.c.values
    Mv, fv = H.M.values, fh[:t]
    dc = c[lagk:] - c[:-lagk]
    dMk = Mv[lagk:] - Mv[:-lagk]
    dfk = fv[lagk:] - fv[:-lagk]
    ok = ~np.isnan(dc) & ~np.isnan(dMk) & ~np.isnan(dfk)
    X = np.c_[np.ones(ok.sum()), dMk[ok], dfk[ok]]
    cb, *_ = np.linalg.lstsq(X, dc[ok], rcond=None)
    drift, k, phi = cb
    ai = t - lagk
    c_t = Q.c.iloc[ai] + drift + k * (r.M - Q.M.iloc[ai]) + phi * (fh[t] - fh[ai])
    cogs = c_t * total_doz + (1 - G_NS) * nonshell
    if trend == "last":
        sga_growth = H.rel_sga.iloc[-1] / H.rel_sga.iloc[-5]
    else:
        sga_growth = H.rel_sga.iloc[-4:].sum() / H.rel_sga.iloc[-8:-4].sum()
    sga = H.rel_sga.iloc[-4] * sga_growth
    op_income = revenue - cogs - sga
    other = H.rel_other_income.iloc[-4] + (H.rel_other_income.iloc[-1] - H.rel_other_income.iloc[-5])
    other = live.get("other_income", other)
    pretax = op_income + other
    tr = H.rel_tax.iloc[-4:].sum() / H.rel_pretax.iloc[-4:].sum()
    tr = float(np.clip(tr, 0.15, 0.35))
    nci = H.nci.iloc[-1] if pd.notna(H.nci.iloc[-1]) else 0.0
    ni = pretax * (1 - tr) - nci
    shares = live.get("shares", H.rel_shares_dil.iloc[-1])
    eps = ni / shares
    return dict(label=r.label, conv_price=conv_price, spec_price=spec_price, conv_doz=conv_doz, spec_doz=spec_doz,
                nonshell=nonshell, revenue=revenue, c=c_t, cogs=cogs, gross_profit=revenue - cogs, sga=sga,
                op_income=op_income, other_income=other, pretax=pretax, tax_rate=tr, nci=nci, ni=ni,
                shares=shares, eps=eps, M=r.M, a=a, b=b, resid_last=resid_last, rho=rho, beta_s=beta_s,
                k=k, phi=phi, drift=drift, feed_hat=fh[t], anchor=anchor, sga_growth=sga_growth)


# ---------------------------------------------------------------- backtest
def backtest(Q, start_label="FY18 Q1", **kw):
    t0 = int(Q.index[Q.label == start_label][0])
    rows = []
    for t in range(t0, len(Q)):
        e = estimate(Q, t, **kw)
        r = Q.iloc[t]
        e.update(act_revenue=r.rel_net_sales, act_eps=r.rel_eps_dil, act_op_income=r.rel_op_income,
                 act_conv_price=r.conv_price, act_spec_price=r.spec_price, act_conv_doz=r.conv_doz,
                 act_spec_doz=r.spec_doz_all, act_c=r.c, act_sga=r.rel_sga, rel_date=r.rel_date)
        e["rev_err_pct"] = e["revenue"] / r.rel_net_sales - 1
        e["eps_err"] = e["eps"] - r.rel_eps_dil
        e["oi_err_pct_rev"] = (e["op_income"] - r.rel_op_income) / r.rel_net_sales
        e["conv_price_err"] = e["conv_price"] - r.conv_price
        rows.append(e)
    return pd.DataFrame(rows)


def summarize(B, last_n=None):
    b = B if last_n is None else B.tail(last_n)
    return dict(n=len(b),
                rev_mape=float(b.rev_err_pct.abs().mean()), rev_bias=float(b.rev_err_pct.mean()),
                rev_median_ape=float(b.rev_err_pct.abs().median()),
                eps_mae=float(b.eps_err.abs().mean()), eps_median_ae=float(b.eps_err.abs().median()),
                eps_bias=float(b.eps_err.mean()),
                oi_mae_pct_rev=float(b.oi_err_pct_rev.abs().mean()),
                conv_price_mae=float(b.conv_price_err.abs().mean()))


# ---------------------------------------------------------------- live quarter: fiscal 2027 Q1
LIVE = dict(fy=2027, q=1, period_start="2026-05-31", period_end="2026-08-29",
            # Eggland's Best Northeast territory bought 2026-07-10 (10-K subsequent event); management: about +5%
            # a year to specialty volume -> owned 7.3 of the 13 weeks
            spec_doz_adj=1 + 0.05 * (51 / 7) / 13,
            # 46,917,080 shares outstanding on 2026-07-22 (10-K cover); basic weighted Q4 FY26 was 47.000M;
            # a loss makes diluted = basic. Assume ~46.85M (a little more buyback in July-August).
            shares=46850.0)


def live_frame(P, **kw):
    Q0 = load_quarters()
    row = {c: np.nan for c in Q0.columns}
    row.update(fy=LIVE["fy"], q=LIVE["q"], period_start=pd.Timestamp(LIVE["period_start"]),
               period_end=pd.Timestamp(LIVE["period_end"]), weeks=13.0, label="FY27 Q1")
    Q1 = pd.concat([Q0, pd.DataFrame([row])], ignore_index=True)
    return build_inputs(Q1, P, **kw)


def live_estimate(P, M_override=None, conv_price_shift=0.0, **kw):
    price_kw = {k: kw.pop(k) for k in ["price_col", "lag"] if k in kw}
    QL = live_frame(P, **price_kw)
    t = len(QL) - 1
    if M_override is not None:
        QL.loc[t, "M"] = M_override
    e = estimate(QL, t, live=dict(spec_doz_adj=LIVE["spec_doz_adj"], shares=LIVE["shares"]), **kw)
    if conv_price_shift:
        e = dict(e)
        d_rev = conv_price_shift * e["conv_doz"]
        for k_ in ["revenue", "gross_profit", "op_income", "pretax"]:
            e[k_] += d_rev
        e["ni"] += d_rev * (1 - e["tax_rate"])
        e["eps"] = e["ni"] / e["shares"]
        e["conv_price"] += conv_price_shift
    return e


def fit_prices(P, Q):
    """Which free series tracks Cal-Maine's conventional net price best, and at what lag (all quarters)."""
    rows = []
    for col in ["ers_combined", "ers_ny", "ppi_fresh", "ppi_large", "ppi_eggs", "retail_large"]:
        d = daily(P[col])
        for lag in [0, 7, 14, 21, 30, 45]:
            m = np.array([qavg(d, r.period_start, r.period_end, lag) for r in Q.itertuples()])
            y = Q.conv_price.values
            ok = ~np.isnan(m) & ~np.isnan(y)
            a, b = ols(m[ok], y[ok])
            e = y[ok] - (a + b * m[ok])
            rows.append(dict(series=col, lag_days=lag, n=int(ok.sum()), intercept=a, slope=b,
                             r2=1 - e.var() / y[ok].var(), rmse=float(np.sqrt((e ** 2).mean())),
                             mae=float(np.abs(e).mean())))
    return pd.DataFrame(rows)


def main():
    P = load_prices()
    Q = build_inputs(load_quarters(), P)
    pd.set_option("display.width", 250)
    # 1. price fit
    F = fit_prices(P, Q)
    F.to_csv(DATA / "price_fit.csv", index=False, float_format="%.4f")
    print(F.sort_values("rmse").head(8).round(3).to_string())
    # 2. variants (reported so the choice is visible)
    res = []
    for anchor in ["last", "yearago"]:
        for rho in [0.0, 0.5, 1.0]:
            for trend in ["last", "trailing4"]:
                for win in [None, 12]:
                    B = backtest(Q, anchor=anchor, rho=rho, trend=trend, win=win)
                    s_ = summarize(B)
                    res.append(dict(anchor=anchor, rho=rho, trend=trend, price_window=win or "all", **s_))
    V = pd.DataFrame(res)
    V.to_csv(DATA / "backtest_variants.csv", index=False, float_format="%.4f")
    # 3. chosen spec: anchor=last, rho=0.5, trend=last, win=12
    B = backtest(Q)
    B.to_csv(DATA / "backtest.csv", index=False, float_format="%.4f")
    S, S12 = summarize(B), summarize(B, 12)
    print("chosen spec, all:", {k: round(v, 3) for k, v in S.items()})
    print("chosen spec, last 12:", {k: round(v, 3) for k, v in S12.items()})
    # 4. live quarter
    e = live_estimate(P)
    q = lambda x, p_: float(np.nanpercentile(x, p_))
    rev_lo = e["revenue"] / (1 + q(B.rev_err_pct, 90))
    rev_hi = e["revenue"] / (1 + q(B.rev_err_pct, 10))
    per_rev = e["revenue"] * (1 - e["tax_rate"]) / e["shares"]
    eps_lo = e["eps"] - q(B.oi_err_pct_rev, 90) * per_rev
    eps_hi = e["eps"] - q(B.oi_err_pct_rev, 10) * per_rev
    # sensitivities: +10c realized conventional price; +10c USDA market price (flows through price AND costs)
    e_c = live_estimate(P, conv_price_shift=0.10)
    e_m = live_estimate(P, M_override=e["M"] + 0.10)
    out = dict(estimate={k: (float(v) if isinstance(v, (int, float, np.floating)) else v) for k, v in e.items()},
               revenue_range_p10_p90=[rev_lo, rev_hi], eps_range_p10_p90=[eps_lo, eps_hi],
               eps_per_10c_conv_price=e_c["eps"] - e["eps"], eps_per_10c_usda_price=e_m["eps"] - e["eps"],
               rev_per_10c_usda_price=e_m["revenue"] - e["revenue"],
               backtest_all=S, backtest_last12=S12,
               backtest_err_quantiles=dict(rev_p10=q(B.rev_err_pct, 10), rev_p90=q(B.rev_err_pct, 90),
                                           oi_pct_rev_p10=q(B.oi_err_pct_rev, 10),
                                           oi_pct_rev_p90=q(B.oi_err_pct_rev, 90),
                                           eps_p10=q(B.eps_err, 10), eps_p90=q(B.eps_err, 90)))
    json.dump(out, open(DATA / "live_estimate.json", "w"), indent=1, default=float)
    print(json.dumps({k: v for k, v in out.items() if k != "estimate"}, indent=1, default=float))
    print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in e.items()})


if __name__ == "__main__":
    main()
