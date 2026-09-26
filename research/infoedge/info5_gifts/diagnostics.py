#!/usr/bin/env python3
"""INFO-5 post-hoc diagnostics (NOT pre-registered; added after the primary result was seen).

The primary BHAR is negative with t = -5.3, but against IWM/SPY the same events show ~0. That
pattern is what a biased benchmark produces: a daily-rebalanced equal-weighted portfolio compounds
to more than the typical member stock (Barber & Lyon 1997 "rebalancing" and "skewness" biases),
and the panel is survivors only. Two checks, both reported as information only:

  1. Placebo: the same stocks on random dates with no gift. For each priced event, 3 pseudo-event
     dates are drawn (seeded) from the stock's priced life, at least 60 trading days away from
     any of its own qualifying gift filings, and the pre-registered BHAR (+1,+60) is computed with
     the same benchmark. If gifts carry information, event BHAR should be below placebo BHAR.
     Reported: placebo mean, and event-minus-placebo (per event: event BHAR minus the mean of its
     own placebo BHARs), t clustered by filing month.
  2. Buy-and-hold benchmark: benchmark = average of the other cell members' own compound returns
     over the window (not the compound of the daily average), which removes the rebalancing bias.
  3. The placebo difference is also computed with the buy-and-hold benchmark and with IWM/SPY.

Writes diagnostics.json.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

import event_study as es

HERE = Path(__file__).resolve().parent
K = 3
SEED = 20260926


def main():
    P = es.Panel()
    ev = pd.read_parquet(es.CACHE / "events_stage1.parquet")
    pr = ev[ev.priced].copy().reset_index(drop=True)
    res_main = pd.read_csv(es.DATA / "events.csv.gz", dtype={"cik": str})
    res_main["filing_date"] = pd.to_datetime(res_main.filing_date)
    pr = pr.merge(res_main[["cik", "filing_date", "bhar", "half"]], on=["cik", "filing_date"], how="left")
    cell, member, _ = es.benchmark_cells(P)
    T, N = P.r.shape
    R = np.nan_to_num(P.r, nan=0.0)
    V = np.isfinite(P.r) & (cell >= 0) & member[None, :]
    ncell = int(cell.max()) + 1
    csum = np.zeros((T, ncell))
    ccnt = np.zeros((T, ncell))
    for t in range(T):
        c = cell[t][V[t]]
        np.add.at(csum[t], c, R[t][V[t]])
        np.add.at(ccnt[t], c, 1)
    r_iwm, r_spy = np.nan_to_num(P.r[:, P.col["IWM"]]), np.nan_to_num(P.r[:, P.col["SPY"]])
    logR = np.log1p(np.clip(R, -0.999999, None))
    cumlog = np.vstack([np.zeros((1, N)), np.cumsum(logR, 0)])   # cumlog[t+1] = sum_{<=t}

    def bench_daily(j, days, mcap, ff):
        etf = r_iwm if (not np.isfinite(mcap) or mcap < es.TWO_B) else r_spy
        if ff is None or not np.isfinite(mcap):
            return etf[days]
        c = cell[days, j].astype(int)
        has = c >= 0
        cc = np.where(has, c, 0)
        s = csum[days, cc] - np.where(V[days, j], R[days, j], 0.0)
        n = ccnt[days, cc] - V[days, j]
        use = has & (n >= es.MIN_CELL)
        return np.where(use, s / np.where(n > 0, n, 1), etf[days])

    def bhar(j, lo, hi, mcap, ff):
        hi = min(hi, P.last[j])
        if hi < lo:
            return np.nan
        days = np.arange(lo, hi + 1)
        return np.prod(1 + R[days, j]) - np.prod(1 + bench_daily(j, days, mcap, ff))

    def bhar_bh(j, lo, hi, mcap, ff):
        """benchmark = mean of other members' own compound returns (cell fixed at day lo)."""
        hi = min(hi, P.last[j])
        if hi < lo:
            return np.nan
        s_ret = np.expm1(cumlog[hi + 1, j] - cumlog[lo, j])
        c0 = cell[lo, j]
        etf = r_iwm if (not np.isfinite(mcap) or mcap < es.TWO_B) else r_spy
        if ff is None or not np.isfinite(mcap) or c0 < 0:
            return s_ret - (np.prod(1 + etf[lo:hi + 1]) - 1)
        mem = np.nonzero((cell[lo] == c0) & member & (P.first <= lo - 1) & (P.last >= hi))[0]
        mem = mem[mem != j]
        if len(mem) < es.MIN_CELL:
            return s_ret - (np.prod(1 + etf[lo:hi + 1]) - 1)
        b = np.expm1(cumlog[hi + 1, mem] - cumlog[lo, mem]).mean()
        return s_ret - b

    rng = np.random.default_rng(SEED)
    ev_days = pr.groupby("j").i0.apply(lambda s: np.sort(s.to_numpy())).to_dict()
    # all qualifying filings (priced or not) of the same ticker column, for the exclusion zone
    def bhar_etf(j, lo, hi, mcap):
        hi = min(hi, P.last[j])
        if hi < lo:
            return np.nan
        etf = r_iwm if (not np.isfinite(mcap) or mcap < es.TWO_B) else r_spy
        return np.prod(1 + R[lo:hi + 1, j]) - np.prod(1 + etf[lo:hi + 1])

    plac, bh, plac_bh, plac_etf, ev_etf = [], [], [], [], []
    for r_ in pr.itertuples(index=False):
        j, i0 = int(r_.j), int(r_.i0)
        ff = None if pd.isna(r_.ff12) else int(r_.ff12)
        mc = r_.mcap if pd.notna(r_.mcap) else np.nan
        bh.append(bhar_bh(j, i0 + 1, i0 + es.WINDOW, mc, ff))
        lo_ok, hi_ok = max(P.first[j] + 1, 0), min(P.last[j], T - 1) - es.WINDOW
        own = ev_days[r_.j]
        ev_etf.append(bhar_etf(j, i0 + 1, i0 + es.WINDOW, mc))
        vals, vals_bh, vals_etf = [], [], []
        tries = 0
        while len(vals) < K and tries < 200 and hi_ok > lo_ok:
            tries += 1
            d = int(rng.integers(lo_ok, hi_ok + 1))
            if np.min(np.abs(own - d)) < es.WINDOW:
                continue
            mcd = es.mcap_at(P, SHARES, r_.cik, j, d) if np.isfinite(mc) else np.nan
            vals.append(bhar(j, d + 1, d + es.WINDOW, mcd, ff))
            vals_bh.append(bhar_bh(j, d + 1, d + es.WINDOW, mcd, ff))
            vals_etf.append(bhar_etf(j, d + 1, d + es.WINDOW, mcd))
        plac.append(np.nanmean(vals) if vals else np.nan)
        plac_bh.append(np.nanmean(vals_bh) if vals_bh else np.nan)
        plac_etf.append(np.nanmean(vals_etf) if vals_etf else np.nan)
    pr["placebo"] = plac
    pr["bhar_bh"] = bh
    pr["diff"] = pr.bhar - pr.placebo
    pr["diff_bh"] = pr.bhar_bh - pd.Series(plac_bh)
    pr["bhar_etf"] = ev_etf
    pr["diff_etf"] = pr.bhar_etf - pd.Series(plac_etf)
    pr["placebo_bh"] = plac_bh
    pr["placebo_etf"] = plac_etf
    pr["filing_month"] = pr.filing_date.dt.to_period("M").astype(str)

    def st(df, col):
        return es.clustered(df[col].to_numpy(), df.filing_month.to_numpy())

    pr[["cik", "ticker", "filing_date", "mcap", "half", "post_rule", "december", "ceo_cfo", "bhar",
        "placebo", "bhar_bh", "placebo_bh", "bhar_etf", "placebo_etf"]].to_parquet(
        es.CACHE / "diagnostics_events.parquet", index=False)
    size = pd.cut(pr.mcap, [0, 3e8, 2e9, 1e10, 1e15], labels=["under_300m", "300m_2b", "2b_10b", "over_10b"])
    by_size = {}
    for lab in size.cat.categories:
        d = pr[size == lab]
        by_size[lab] = {c: st(d, c) for c in ("bhar", "placebo", "diff", "bhar_bh", "diff_bh",
                                               "bhar_etf", "diff_etf")}

    out = {"placebo_mean": st(pr, "placebo"),
           "event_minus_placebo": st(pr, "diff"),
           "event_minus_placebo_half1": st(pr[pr.half == 1], "diff"),
           "event_minus_placebo_half2": st(pr[pr.half == 2], "diff"),
           "event_minus_placebo_pre_rule": st(pr[~pr.post_rule], "diff"),
           "event_minus_placebo_post_rule": st(pr[pr.post_rule], "diff"),
           "event_minus_placebo_under_2b": st(pr[pr.mcap < es.TWO_B], "diff"),
           "event_minus_placebo_december": st(pr[pr.december], "diff"),
           "event_minus_placebo_ceo_cfo": st(pr[pr.ceo_cfo], "diff"),
           "placebo_under_2b": st(pr[pr.mcap < es.TWO_B], "placebo"),
           "buyhold_benchmark": st(pr, "bhar_bh"),
           "buyhold_benchmark_half1": st(pr[pr.half == 1], "bhar_bh"),
           "buyhold_benchmark_half2": st(pr[pr.half == 2], "bhar_bh"),
           "buyhold_benchmark_under_2b": st(pr[pr.mcap < es.TWO_B], "bhar_bh"),
           "placebo_buyhold": st(pr, "placebo_bh"),
           "event_minus_placebo_buyhold": st(pr, "diff_bh"),
           "event_minus_placebo_buyhold_half1": st(pr[pr.half == 1], "diff_bh"),
           "event_minus_placebo_buyhold_half2": st(pr[pr.half == 2], "diff_bh"),
           "placebo_etf": st(pr, "placebo_etf"),
           "event_minus_placebo_etf": st(pr, "diff_etf"),
           "event_minus_placebo_etf_half1": st(pr[pr.half == 1], "diff_etf"),
           "event_minus_placebo_etf_half2": st(pr[pr.half == 2], "diff_etf"),
           "by_size": by_size,
           "subgroups": {name: {c: st(pr[m], c) for c in ("bhar", "bhar_etf", "diff")}
                         for name, m in (("all_2b_plus", pr.mcap >= es.TWO_B),
                                         ("december", pr.december),
                                         ("december_2b_plus", pr.december & (pr.mcap >= es.TWO_B)),
                                         ("december_under_2b", pr.december & (pr.mcap < es.TWO_B)),
                                         ("ceo_cfo", pr.ceo_cfo),
                                         ("ceo_cfo_2b_plus", pr.ceo_cfo & (pr.mcap >= es.TWO_B)),
                                         ("pre_rule", ~pr.post_rule),
                                         ("post_rule", pr.post_rule),
                                         ("pre_rule_2b_plus", ~pr.post_rule & (pr.mcap >= es.TWO_B)))},
           "n_with_placebo": int(pr.placebo.notna().sum()), "K": K, "seed": SEED}
    (HERE / "diagnostics.json").write_text(json.dumps(out, indent=1, default=str))
    for lab, dd in by_size.items():
        for c, v in dd.items():
            print(f"size {lab:10s} {c:9s} n={v['n']:6d} mean={v['mean'] * 100:+.2f}% t={v['t']:.2f}")
    for k, v in out.items():
        if isinstance(v, dict) and "n" in v:
            print(f"{k:34s} n={v['n']:6d} mean={v['mean'] * 100:+.2f}% t={v['t']:.2f}")


if __name__ == "__main__":
    SHARES = es.shares_lookup()
    main()
