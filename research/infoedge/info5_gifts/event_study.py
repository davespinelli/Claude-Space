#!/usr/bin/env python3
"""INFO-5. Insider gifts: event construction and the pre-registered event study.

Spec and every definition: research/infoedge/info5_gifts/PREREG.md (written before any return
was computed). Inputs are built by fetch_form345.py, build_gifts.py, map_tickers.py,
yahoo_daily_info5.py and fetch_meta.py (all cached under cache/, gitignored).

    python event_study.py events    # stage 1: build events (prices used only for gift value,
                                    #          ticker validation and market cap; no returns)
    python event_study.py returns   # stage 2: event study, secondaries, results.json
    python event_study.py all

Writes data/events.csv.gz, data/missing_events.csv.gz, data/excluded_issuers.csv, results.json.
RESULTS.md is written by write_results.py from results.json.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "cache"
DATA = HERE / "data"
DATA.mkdir(exist_ok=True)

MIN_VALUE = 1_000_000.0
MIN_PCT = 0.01
WINDOW = 60
COST = 0.002
RULE_DATE = pd.Timestamp("2023-02-27")
VAL_BAND = (0.8, 1.25)
VAL_MIN_DAYS = 3
MIN_CELL = 10
TWO_B = 2e9
MAX_MCAP = 6e12
CEO_CFO = re.compile(r"\bCEO\b|\bCFO\b|CHIEF\s+EXECUTIVE|CHIEF\s+FINANCIAL|PRINCIPAL\s+EXECUTIVE"
                     r"|PRINCIPAL\s+FINANCIAL", re.I)


# =============================================================================================
# price panel
# =============================================================================================
class Panel:
    """Wide daily matrices on the SPY trading calendar."""

    def __init__(self):
        px = pd.concat([pd.read_parquet(p) for p in sorted((CACHE / "prices").glob("chunk_*.parquet"))],
                       ignore_index=True)
        px["date"] = pd.to_datetime(px["date"]).dt.normalize()
        px = px.drop_duplicates(["ticker", "date"], keep="last")
        ref = "SPY" if (px.ticker == "SPY").any() else px.ticker.value_counts().index[0]
        cal = pd.DatetimeIndex(sorted(px.loc[px.ticker == ref, "date"].unique()))
        self.cal = cal
        self.tickers = sorted(px.ticker.unique())
        self.col = {t: j for j, t in enumerate(self.tickers)}
        px = px[px.date.isin(cal)]
        ii = cal.get_indexer(px.date)
        jj = px.ticker.map(self.col).to_numpy()
        T, N = len(cal), len(self.tickers)

        def mat(v, fill=np.nan):
            m = np.full((T, N), fill, dtype=np.float64)
            m[ii, jj] = v
            return m

        close = mat(px.close.to_numpy())
        adj = mat(px.adj.to_numpy())
        split = mat(px.split.to_numpy(), 0.0)
        close[~(close > 0)] = np.nan
        adj[~(adj > 0)] = np.nan
        # life of each series: first..last valid adjusted close
        valid = np.isfinite(adj)
        self.first = np.where(valid.any(0), valid.argmax(0), T)
        self.last = np.where(valid.any(0), T - 1 - valid[::-1].argmax(0), -1)
        # forward fill inside the life
        adj_ff = pd.DataFrame(adj).ffill().to_numpy(copy=True)
        close_ff = pd.DataFrame(close).ffill().to_numpy(copy=True)
        idx = np.arange(T)[:, None]
        alive = (idx >= self.first[None, :]) & (idx <= self.last[None, :])
        adj_ff[~alive] = np.nan
        close_ff[~alive] = np.nan
        # split factor F(d) = product of split ratios strictly after d (today's basis -> nominal)
        s = np.where(split > 0, split, 1.0)
        cum_after = np.flip(np.cumprod(np.flip(s, 0), 0), 0)       # product over days >= d
        F = cum_after / s                                             # product over days > d
        self.F = F
        self.close = close_ff                                         # split-adjusted close
        self.nominal = close_ff * F                                   # as traded that day
        # daily total returns + bad-print rule (research/oplev clean_returns, applied daily)
        r = adj_ff[1:] / adj_ff[:-1] - 1.0
        r = np.vstack([np.full((1, N), np.nan), r])
        n_v = 0
        a, b = r[:-1], r[1:]
        v = np.isfinite(a) & np.isfinite(b) & (((a <= -0.9) & (b >= 9)) | ((a >= 9) & (b <= -0.9)))
        rows, cols = np.nonzero(v)
        for i, j in zip(rows, cols):
            r[i, j] = np.nan
            r[i + 1, j] = np.nan
            n_v += 1
        big = np.isfinite(r) & (r > 10)
        self.bad_prints = {"round_trips_removed": int(n_v), "daily_returns_above_1000pct_removed": int(big.sum())}
        r[big] = np.nan
        self.r = r
        del close, adj, split, s, cum_after, adj_ff, valid, alive
        print(f"panel: {T} days x {N} tickers; bad prints {self.bad_prints}", flush=True)

    def day0(self, d):
        """index of the last trading day on or before d"""
        return int(self.cal.searchsorted(pd.Timestamp(d), side="right") - 1)


# =============================================================================================
# helpers
# =============================================================================================
def ff12(sic):
    if sic is None or not np.isfinite(sic):
        return None
    s = int(sic)
    R = {
        1: [(100, 999), (2000, 2399), (2700, 2749), (2770, 2799), (3100, 3199), (3940, 3989)],
        2: [(2500, 2519), (2590, 2599), (3630, 3659), (3710, 3711), (3714, 3714), (3716, 3716),
            (3750, 3751), (3792, 3792), (3900, 3939), (3990, 3999)],
        3: [(2520, 2589), (2600, 2699), (2750, 2769), (3000, 3099), (3200, 3569), (3580, 3629),
            (3700, 3709), (3712, 3713), (3715, 3715), (3717, 3749), (3752, 3791), (3793, 3799),
            (3830, 3839), (3860, 3899)],
        4: [(1200, 1399), (2900, 2999)],
        5: [(2800, 2829), (2840, 2899)],
        6: [(3570, 3579), (3660, 3692), (3694, 3699), (3810, 3829), (7370, 7379)],
        7: [(4800, 4899)],
        8: [(4900, 4949)],
        9: [(5000, 5999), (7200, 7299), (7600, 7699)],
        10: [(2830, 2839), (3693, 3693), (3840, 3859), (8000, 8099)],
        11: [(6000, 6999)],
    }
    for k, rr in R.items():
        if any(lo <= s <= hi for lo, hi in rr):
            return k
    return 12


def _clean_shares(v: np.ndarray) -> np.ndarray:
    """XBRL share-count errors (fixed before any return was computed; PREREG deviation 6):
    values under 10,000 shares are dropped; an interior value more than 5x above or below BOTH
    neighbours is a one-off scale error (e.g. Whirlpool 76,398,669,000,000) and is dropped; an end
    value more than 50x from its only neighbour is dropped. Real splits persist, so they survive."""
    keep = v >= 1e4
    v2 = v[keep]
    idx = np.nonzero(keep)[0]
    bad = np.zeros(len(v2), dtype=bool)
    for i in range(len(v2)):
        if 0 < i < len(v2) - 1:
            a, b = v2[i] / v2[i - 1], v2[i] / v2[i + 1]
            bad[i] = (a > 5 and b > 5) or (a < 0.2 and b < 0.2)
        elif len(v2) > 1:
            n = v2[1] if i == 0 else v2[i - 1]
            bad[i] = v2[i] / n > 50 or v2[i] / n < 0.02
    out = np.zeros(len(v), dtype=bool)
    out[idx[~bad]] = True
    return out


def shares_lookup():
    sh = pd.read_parquet(CACHE / "shares.parquet")
    sh = sh.sort_values(["cik", "concept", "end"]).drop_duplicates(["cik", "concept", "end"], keep="last")
    out = {}
    for k, g in sh.groupby("cik"):
        # prefer cover-page shares; balance-sheet shares only where no clean cover-page value exists
        for concept in ("EntityCommonStockSharesOutstanding", "CommonStockSharesOutstanding"):
            x = g[g.concept == concept]
            if x.empty:
                continue
            v = x.val.to_numpy(dtype=float)
            ok = _clean_shares(v)
            if ok.any():
                out[k] = (x.end.to_numpy()[ok], v[ok])
                break
    return out


def mcap_at(P: Panel, SH, cik, j, i):
    """market cap on trading-day index i for ticker column j (today's split basis)."""
    if cik not in SH or j is None or i < 0:
        return np.nan
    ends, vals = SH[cik]
    d = P.cal[i].to_datetime64()
    k = np.searchsorted(ends, d, side="right") - 1
    k = max(k, 0)                                     # before first XBRL value: carry it back
    fi = P.day0(pd.Timestamp(ends[k]))
    fi = min(max(fi, 0), len(P.cal) - 1)
    f_split = P.F[fi, j]                              # splits after the share-count date
    c = P.close[i, j]
    m = float(c * vals[k] * f_split) if np.isfinite(c) else np.nan
    return m if m <= MAX_MCAP else np.nan              # above any real company: a data error


def clustered(x: np.ndarray, groups: np.ndarray):
    """mean, CR1 cluster-robust SE, t (clusters = groups)."""
    x = np.asarray(x, float)
    m = np.isfinite(x)
    x, groups = x[m], np.asarray(groups)[m]
    n = len(x)
    if n < 2:
        return {"n": int(n), "mean": float(x.mean()) if n else None, "se": None, "t": None,
                "clusters": int(len(set(groups)))}
    mu = x.mean()
    e = pd.Series(x - mu).groupby(groups).sum().to_numpy()
    G = len(e)
    var = (G / (G - 1)) * (e ** 2).sum() / n ** 2 if G > 1 else np.nan
    se = float(np.sqrt(var))
    return {"n": int(n), "mean": float(mu), "se": se, "t": float(mu / se) if se > 0 else None,
            "clusters": int(G), "median": float(np.median(x)), "share_negative": float((x < 0).mean())}


# =============================================================================================
# stage 1: events
# =============================================================================================
def build_events(P: Panel):
    g = pd.read_parquet(CACHE / "gift_lines.parquet")
    o = pd.read_parquet(CACHE / "owners.parquet")
    tm = pd.read_csv(CACHE / "ticker_map.csv", dtype=str, keep_default_na=False)
    sic = pd.read_csv(CACHE / "sic.csv", dtype={"cik": str})
    sic["cik"] = sic.cik.str.zfill(10)
    SIC = dict(zip(sic.cik, sic.sic))
    SH = shares_lookup()
    log = {}

    o["rel"] = o.RPTOWNER_RELATIONSHIP.fillna("")
    o["od"] = o.rel.str.contains("Director|Officer")
    o["ceo_cfo"] = o.RPTOWNER_TITLE.fillna("").str.contains(CEO_CFO) & o.rel.str.contains("Officer")
    acc_od = o.groupby("ACCESSION_NUMBER").od.any()
    acc_cc = o.groupby("ACCESSION_NUMBER").ceo_cfo.any()
    acc_owner = o.groupby("ACCESSION_NUMBER").RPTOWNERNAME.agg(lambda s: " / ".join(dict.fromkeys(s.fillna(""))))
    acc_title = o.groupby("ACCESSION_NUMBER").RPTOWNER_TITLE.agg(lambda s: " / ".join(dict.fromkeys(s.fillna(""))))

    log["gift_lines_all_forms"] = int(len(g))
    log["gift_lines_by_form"] = g.DOCUMENT_TYPE.value_counts().to_dict()
    x = g[g.DOCUMENT_TYPE.isin(["4", "4/A"]) & (g.TRANS_CODE == "G")]
    log["form4_gift_lines"] = int(len(x))
    x = x[x.TRANS_ACQUIRED_DISP_CD == "D"]
    log["form4_gift_disposal_lines"] = int(len(x))
    x = x[x.ACCESSION_NUMBER.map(acc_od).fillna(False).astype(bool)]
    log["officer_director_lines"] = int(len(x))
    lag = (x.FILING_DATE - x.TRANS_DATE).dt.days
    bad = ~(x.TRANS_SHARES > 0) | x.TRANS_DATE.isna() | (lag < 0) | (lag > 730)
    log["dropped_bad_lines"] = {"zero_or_missing_shares": int((~(x.TRANS_SHARES > 0)).sum()),
                                "gift_after_filing": int((lag < 0).sum()),
                                "gift_over_2y_before_filing": int((lag > 730).sum())}
    x = x[~bad].copy()
    x["acct"] = (x.SECURITY_TITLE.fillna("").str.upper().str.strip() + "|"
                 + x.DIRECT_INDIRECT_OWNERSHIP.fillna("") + "|"
                 + x.NATURE_OF_OWNERSHIP.fillna("").str.upper().str.strip())
    n0 = len(x)
    x = x.drop_duplicates(["ACCESSION_NUMBER", "TRANS_DATE", "TRANS_SHARES", "acct", "SHRS_OWND_FOLWNG_TRANS"])
    log["dedup_within_filing_removed"] = int(n0 - len(x))
    x = x.sort_values(["FILING_DATE", "ACCESSION_NUMBER"])
    first_acc = x.groupby(["ISSUERCIK", "TRANS_DATE", "TRANS_SHARES"]).ACCESSION_NUMBER.transform("first")
    n0 = len(x)
    x = x[x.ACCESSION_NUMBER == first_acc]
    log["dedup_across_filings_removed"] = int(n0 - len(x))
    log["lines_after_dedup"] = int(len(x))

    # holdings
    bal = pd.read_parquet(CACHE / "acct_balances.parquet")
    tot_after = bal.groupby("ACCESSION_NUMBER").SHRS_OWND_FOLWNG_TRANS.sum(min_count=1)
    tot_gift = x.groupby("ACCESSION_NUMBER").TRANS_SHARES.sum()
    gifts = (x.groupby(["ACCESSION_NUMBER", "TRANS_DATE"])
              .agg(ISSUERCIK=("ISSUERCIK", "first"), FILING_DATE=("FILING_DATE", "first"),
                   DOCUMENT_TYPE=("DOCUMENT_TYPE", "first"), ISSUERNAME=("ISSUERNAME", "first"),
                   symbol=("ISSUERTRADINGSYMBOL", "first"), shares=("TRANS_SHARES", "sum"),
                   own_price=("TRANS_PRICEPERSHARE", "max"), n_lines=("TRANS_SHARES", "size"))
              .reset_index())
    before = gifts.ACCESSION_NUMBER.map(tot_after) + gifts.ACCESSION_NUMBER.map(tot_gift)
    gifts["pct"] = np.where(before > 0, gifts.shares / before, np.nan)
    gifts["ceo_cfo"] = gifts.ACCESSION_NUMBER.map(acc_cc).fillna(False).astype(bool)
    gifts["owner"] = gifts.ACCESSION_NUMBER.map(acc_owner)
    gifts["title"] = gifts.ACCESSION_NUMBER.map(acc_title)
    log["gifts"] = int(len(gifts))

    # ticker per issuer
    tmi = tm.set_index("cik")
    gifts["ticker"] = gifts.ISSUERCIK.map(tmi.ticker).fillna("")
    gifts["map_source"] = gifts.ISSUERCIK.map(tmi.source).fillna("none")
    gifts["j"] = gifts.ticker.map(P.col)

    # insiders' own open-market prices (validation + proxy)
    osp = pd.read_parquet(CACHE / "os_prices.parquet")
    osp = osp[osp.ISSUERCIK.isin(set(gifts.ISSUERCIK)) & osp.date.notna()]
    osp_by = {k: (v.date.to_numpy(), v.price.to_numpy()) for k, v in osp.groupby("ISSUERCIK")}

    ig = np.array([P.day0(d) for d in gifts.TRANS_DATE])
    gifts["ig"] = ig
    val_ratio, val_n, yprice, proxy = [], [], [], []
    for r_, i_g in zip(gifts.itertuples(index=False), ig):
        j = r_.j
        yp = np.nan
        if pd.notna(j) and i_g >= 0:
            j = int(j)
            if P.first[j] <= i_g <= P.last[j] and (r_.TRANS_DATE - P.cal[i_g]).days <= 7:
                yp = P.nominal[i_g, j]
        yprice.append(yp)
        # proxy: insiders' open-market price within 30 days of the gift
        pr = np.nan
        vr, vn = np.nan, 0
        if r_.ISSUERCIK in osp_by:
            dts, prs = osp_by[r_.ISSUERCIK]
            dd = (dts - np.datetime64(r_.TRANS_DATE)) / np.timedelta64(1, "D")
            near = np.abs(dd) <= 30
            if near.any():
                pr = float(np.median(prs[near]))
            if pd.notna(j):
                w = np.abs(dd) <= 365
                if w.any():
                    ii = P.cal.searchsorted(pd.DatetimeIndex(dts[w]), side="right") - 1
                    ok = ii >= 0
                    ii = ii[ok]
                    exact = P.cal[ii].to_numpy() == dts[w][ok]
                    ii = ii[exact]
                    if len(ii):
                        yc = P.nominal[ii, int(j)]
                        rr = prs[w][ok][exact] / yc
                        rr = rr[np.isfinite(rr)]
                        vn = len(rr)
                        if vn:
                            vr = float(np.median(rr))
        own = r_.own_price if (pd.notna(r_.own_price) and r_.own_price > 0) else np.nan
        proxy.append(own if np.isfinite(own) else pr)
        val_ratio.append(vr)
        val_n.append(vn)
    gifts["yahoo_px"] = yprice
    gifts["proxy_px"] = proxy
    gifts["val_ratio"] = val_ratio
    gifts["val_n"] = val_n

    # validation status per gift
    has_val = gifts.val_n >= VAL_MIN_DAYS
    in_band = gifts.val_ratio.between(*VAL_BAND)
    gifts["val_fail"] = has_val & ~in_band
    gifts["usable"] = (gifts.j.notna() & gifts.yahoo_px.notna() & ~gifts.val_fail
                       & ((gifts.map_source == "sec_current") | (has_val & in_band)))
    gifts["price_for_value"] = np.where(gifts.usable, gifts.yahoo_px, gifts.proxy_px)
    gifts["value"] = gifts.shares * gifts.price_for_value
    gifts["qual"] = (gifts.value >= MIN_VALUE) | (gifts.pct >= MIN_PCT)
    log["qualifying_gifts"] = int(gifts.qual.sum())
    log["qualifying_by_test"] = {
        "value_only": int(((gifts.value >= MIN_VALUE) & ~(gifts.pct >= MIN_PCT)).sum()),
        "pct_only": int((~(gifts.value >= MIN_VALUE) & (gifts.pct >= MIN_PCT)).sum()),
        "both": int(((gifts.value >= MIN_VALUE) & (gifts.pct >= MIN_PCT)).sum())}
    q = gifts[gifts.qual].copy()

    # events: issuer x filing date
    q = q.sort_values(["ISSUERCIK", "FILING_DATE", "TRANS_DATE"])
    ev = (q.groupby(["ISSUERCIK", "FILING_DATE"])
           .agg(gift_date=("TRANS_DATE", "min"), last_gift_date=("TRANS_DATE", "max"),
                n_gifts=("shares", "size"), shares=("shares", "sum"), value=("value", lambda s: s.sum(min_count=1)),
                max_pct=("pct", "max"), ceo_cfo=("ceo_cfo", "any"), ticker=("ticker", "first"),
                map_source=("map_source", "first"), j=("j", "first"), usable=("usable", "all"),
                any_val_fail=("val_fail", "any"), val_ratio=("val_ratio", "median"),
                val_n=("val_n", "max"), name=("ISSUERNAME", "first"), owner=("owner", "first"),
                title=("title", "first"), form=("DOCUMENT_TYPE", "first"),
                accession=("ACCESSION_NUMBER", "first"))
           .reset_index())
    ev["december"] = ev.gift_date.dt.month == 12
    ev["post_rule"] = ev.gift_date >= RULE_DATE
    ev["lag_days"] = (ev.FILING_DATE - ev.gift_date).dt.days
    ev["i0"] = [P.day0(d) for d in ev.FILING_DATE]
    ev["ig"] = [P.day0(d) for d in ev.gift_date]
    ev["complete"] = ev.i0 + WINDOW <= len(P.cal) - 1
    log["events_all"] = int(len(ev))
    log["events_window_incomplete_dropped"] = int((~ev.complete).sum())
    ev = ev[ev.complete].copy()

    # priced vs missing
    def reason(r_):
        if r_.map_source == "none":
            return "no_symbol_in_filings"
        if r_.map_source == "reused":
            return "ticker_reused_by_another_company"
        if pd.isna(r_.j):
            return "no_yahoo_data_for_ticker"
        j = int(r_.j)
        if r_.any_val_fail:
            return "yahoo_price_disagrees_with_form4_prices"
        if r_.map_source == "symbol" and not r_.usable:
            return "old_symbol_not_validated"
        if not (P.first[j] <= r_.i0 and P.last[j] >= r_.i0 + 1):
            return "yahoo_series_does_not_cover_filing_date"
        if not r_.usable:
            return "no_yahoo_price_on_gift_date"
        return ""
    ev["missing_reason"] = [reason(r_) for r_ in ev.itertuples(index=False)]
    ev["priced"] = ev.missing_reason == ""

    # industry, market cap at day 0
    ev["sic"] = ev.ISSUERCIK.map(SIC)
    ev["ff12"] = [ff12(s) if pd.notna(s) else None for s in ev.sic]
    ev["mcap"] = [mcap_at(P, SH, c, int(j) if pd.notna(j) else None, i) if p else np.nan
                  for c, j, i, p in zip(ev.ISSUERCIK, ev.j, ev.i0, ev.priced)]
    log["events_priced"] = int(ev.priced.sum())
    log["events_missing"] = int((~ev.priced).sum())
    log["missing_by_reason"] = ev.loc[~ev.priced, "missing_reason"].value_counts().to_dict()
    log["missing_by_year"] = ev.loc[~ev.priced].groupby(ev.FILING_DATE.dt.year).size().to_dict()
    log["priced_by_year"] = ev.loc[ev.priced].groupby(ev.FILING_DATE.dt.year).size().to_dict()
    log["events_no_mcap"] = int((ev.priced & ev.mcap.isna()).sum())
    log["events_no_sic"] = int((ev.priced & ev.ff12.isna()).sum())

    cols = ["ISSUERCIK", "name", "ticker", "map_source", "FILING_DATE", "gift_date", "last_gift_date",
            "lag_days", "n_gifts", "shares", "value", "max_pct", "ceo_cfo", "december", "post_rule",
            "owner", "title", "form", "accession", "sic", "ff12", "mcap", "val_ratio", "val_n",
            "priced", "missing_reason", "j", "i0", "ig"]
    ev = ev[cols].rename(columns={"ISSUERCIK": "cik", "FILING_DATE": "filing_date"})
    ev.to_parquet(CACHE / "events_stage1.parquet", index=False)
    ev[~ev.priced].drop(columns=["j", "i0", "ig"]).to_csv(DATA / "missing_events.csv.gz", index=False)
    exc = (ev[~ev.priced].groupby(["cik", "name", "ticker", "missing_reason"]).size()
           .rename("events").reset_index().sort_values("events", ascending=False))
    exc.to_csv(DATA / "excluded_issuers.csv", index=False)
    log["excluded_issuers"] = int(exc.cik.nunique())
    (CACHE / "stage1_log.json").write_text(json.dumps(log, indent=1, default=str))
    print(json.dumps(log, indent=1, default=str))
    return ev, log


# =============================================================================================
# stage 2: returns
# =============================================================================================
def benchmark_cells(P: Panel):
    """cell id (ff12*10 + size quintile) per ticker per trading day, re-formed each 30 June."""
    tm = pd.read_csv(CACHE / "ticker_map.csv", dtype=str, keep_default_na=False)
    tm = tm[tm.source.isin(["sec_current", "symbol"])]
    sic = pd.read_csv(CACHE / "sic.csv", dtype={"cik": str})
    sic["cik"] = sic.cik.str.zfill(10)
    SIC = dict(zip(sic.cik, sic.sic))
    SH = shares_lookup()
    # one CIK per ticker (current-list mapping wins); benchmark members: current-list tickers
    t2c = {}
    for r_ in tm.sort_values("source").itertuples(index=False):   # sec_current sorts first
        t2c.setdefault(r_.ticker, (r_.cik, r_.source))
    T, N = P.r.shape
    cell = np.full((T, N), -1, dtype=np.int16)
    # every mapped ticker gets a cell (so delisted event firms found under an old symbol are
    # benchmarked too), but only current-list tickers are MEMBERS whose returns form the cells
    member = np.zeros(N, dtype=bool)
    years = range(P.cal[0].year, P.cal[-1].year + 1)
    info = {}
    for y in years:
        i_j = P.day0(pd.Timestamp(f"{y}-06-30"))
        if i_j < 0:
            i_j = 0
        mc, ind = np.full(N, np.nan), np.full(N, -1)
        for t, j in P.col.items():
            if t not in t2c or t in ("SPY", "IWM"):
                continue
            cik, src = t2c[t]
            member[j] = src == "sec_current"
            s = SIC.get(cik)
            f = ff12(s) if s is not None and np.isfinite(s) else None
            if f is None:
                continue
            if not (P.first[j] <= i_j <= P.last[j]):
                continue
            mc[j] = mcap_at(P, SH, cik, j, i_j)
            ind[j] = f
        ok = np.isfinite(mc) & (ind > 0)
        if (ok & member).sum() < 50:
            continue
        qs = np.quantile(mc[ok & member], [0.2, 0.4, 0.6, 0.8])
        qn = np.searchsorted(qs, mc, side="right") + 1
        c = np.where(ok, ind * 10 + qn, -1)
        lo = P.day0(pd.Timestamp(f"{y}-06-30")) + 1
        hi = P.day0(pd.Timestamp(f"{y + 1}-06-30")) + 1
        lo, hi = max(lo, 0), min(hi, T)
        # before the first formation, use the first formation's cells
        if y == P.cal[0].year:
            lo = 0
        cell[lo:hi, :] = c[None, :]
        info[y] = {"member_stocks": int((ok & member).sum()),
                   "size_breaks_$bn": [round(v / 1e9, 3) for v in qs]}
    return cell, member, info


def run_returns(P: Panel):
    ev = pd.read_parquet(CACHE / "events_stage1.parquet")
    cell, member, cell_info = benchmark_cells(P)
    T, N = P.r.shape
    R = np.nan_to_num(P.r, nan=0.0)
    V = np.isfinite(P.r) & (cell >= 0) & member[None, :]
    # cell sums / counts per day
    ncell = int(cell.max()) + 1
    csum = np.zeros((T, ncell))
    ccnt = np.zeros((T, ncell))
    for t in range(T):
        c = cell[t][V[t]]
        np.add.at(csum[t], c, R[t][V[t]])
        np.add.at(ccnt[t], c, 1)
    iwm, spy = P.col["IWM"], P.col["SPY"]
    r_iwm, r_spy = np.nan_to_num(P.r[:, iwm]), np.nan_to_num(P.r[:, spy])

    def bench_series(j, lo, hi, mcap, ff):
        """daily benchmark returns for days lo..hi (inclusive) for stock j; plus type."""
        days = np.arange(lo, hi + 1)
        etf = r_iwm if (not np.isfinite(mcap) or mcap < TWO_B) else r_spy
        if ff is None or not np.isfinite(mcap):
            return etf[days], "etf"
        c = cell[days, j].astype(int)
        has = c >= 0
        cc = np.where(has, c, 0)
        s = csum[days, cc] - np.where(V[days, j], R[days, j], 0.0)
        n = ccnt[days, cc] - V[days, j]
        use = has & (n >= MIN_CELL)
        out = np.where(use, s / np.where(n > 0, n, 1), etf[days])
        used_etf = int((~use).sum())
        return out, ("cell" if used_etf == 0 else ("etf" if used_etf == len(days) else "mixed"))

    def bhar(j, lo, hi, mcap, ff, etf_only=False):
        if hi < lo:
            return np.nan, np.nan, np.nan, ""
        hi_eff = min(hi, P.last[j])
        if hi_eff < lo:
            return np.nan, np.nan, np.nan, ""
        days = np.arange(lo, hi_eff + 1)
        rs = R[days, j]
        if etf_only:
            b = (r_iwm if (not np.isfinite(mcap) or mcap < TWO_B) else r_spy)[days]
            kind = "etf"
        else:
            b, kind = bench_series(j, lo, hi_eff, mcap, ff)
        s = np.prod(1 + rs) - 1
        bb = np.prod(1 + b) - 1
        return s - bb, s, bb, kind

    out = []
    pr = ev[ev.priced].copy()
    for r_ in pr.itertuples(index=False):
        j, i0, ig = int(r_.j), int(r_.i0), int(r_.ig)
        ff = None if pd.isna(r_.ff12) else int(r_.ff12)
        mc = r_.mcap if pd.notna(r_.mcap) else np.nan
        a, s, b, kind = bhar(j, i0 + 1, i0 + WINDOW, mc, ff)
        a_etf, _, _, _ = bhar(j, i0 + 1, i0 + WINDOW, mc, ff, etf_only=True)
        a_pre, _, _, _ = bhar(j, ig + 1, i0, mc, ff) if i0 > ig else (np.nan, 0, 0, "")
        a_gd = np.nan
        if ig + WINDOW <= T - 1 and ig >= P.first[j]:
            a_gd, _, _, _ = bhar(j, ig + 1, ig + WINDOW, mc, ff)
        # short windows for information
        a20, _, _, _ = bhar(j, i0 + 1, i0 + 20, mc, ff)
        a5, _, _, _ = bhar(j, i0 + 1, i0 + 5, mc, ff)
        out.append((a, s, b, kind, a_etf, a_pre, a_gd, a20, a5,
                    int(min(i0 + WINDOW, P.last[j]) - i0)))
    cols = ["bhar", "ret_stock", "ret_bench", "bench_kind", "bhar_etf", "bhar_prefiling",
            "bhar_giftdate", "bhar_1_20", "bhar_1_5", "days_in_window"]
    pr[cols] = pd.DataFrame(out, index=pr.index)
    pr["filing_month"] = pr.filing_date.dt.to_period("M").astype(str)
    pr = pr.sort_values("filing_date").reset_index(drop=True)
    med = pr.filing_date.iloc[len(pr) // 2]
    pr["half"] = np.where(pr.filing_date < med, 1, 2)

    res = {"cell_formations": cell_info, "bad_prints": P.bad_prints,
           "median_filing_date_split": str(med.date()),
           "bench_kind_counts": pr.bench_kind.value_counts().to_dict(),
           "short_window_events": int((pr.days_in_window < WINDOW).sum())}

    def stat(df, col="bhar", cl="filing_month"):
        d = clustered(df[col].to_numpy(), df[cl].to_numpy())
        if d.get("se"):
            d["mean_after_cost"] = d["mean"] + COST
            d["t_after_cost"] = d["mean_after_cost"] / d["se"]
        return d

    P_ = {}
    P_["primary"] = stat(pr)
    P_["half1"] = stat(pr[pr.half == 1])
    P_["half2"] = stat(pr[pr.half == 2])
    P_["half1_range"] = [str(pr[pr.half == 1].filing_date.min().date()), str(pr[pr.half == 1].filing_date.max().date())]
    P_["half2_range"] = [str(pr[pr.half == 2].filing_date.min().date()), str(pr[pr.half == 2].filing_date.max().date())]
    p = P_["primary"]
    P_["verdict"] = ("Yes" if (p["t"] is not None and p["t"] <= -2.5 and P_["half1"]["mean"] < 0
                              and P_["half2"]["mean"] < 0) else "No")
    res["primary"] = P_

    # bounds for missing companies
    miss = ev[~ev.priced].copy()
    miss["filing_month"] = miss.filing_date.dt.to_period("M").astype(str)
    b = {}
    for lab, v in (("minus30", -0.30), ("plus15", 0.15)):
        allx = pd.concat([pr[["bhar", "filing_month"]],
                          miss[["filing_month"]].assign(bhar=v)], ignore_index=True)
        b[lab] = stat(allx)
    b["n_missing"] = int(len(miss))
    b["missing_share"] = float(len(miss) / (len(miss) + len(pr)))
    res["bounds"] = b

    # regimes (the 2023 rule change), by gift date
    res["pre_rule"] = stat(pr[~pr.post_rule])
    res["post_rule"] = stat(pr[pr.post_rule])
    res["pre_rule_lag"] = pr[~pr.post_rule].lag_days.describe().to_dict()
    res["post_rule_lag"] = pr[pr.post_rule].lag_days.describe().to_dict()

    # secondaries
    sec = {}
    sec["december"] = stat(pr[pr.december])
    sec["not_december"] = stat(pr[~pr.december])
    sec["ceo_cfo"] = stat(pr[pr.ceo_cfo])
    sec["not_ceo_cfo"] = stat(pr[~pr.ceo_cfo])
    sec["under_2b"] = stat(pr[pr.mcap < TWO_B])
    sec["over_2b"] = stat(pr[pr.mcap >= TWO_B])
    sec["mcap_unknown"] = stat(pr[pr.mcap.isna()])
    sec["prefiling_window"] = stat(pr[pr.bhar_prefiling.notna()], "bhar_prefiling")
    sec["prefiling_window_pre_rule"] = stat(pr[pr.bhar_prefiling.notna() & ~pr.post_rule], "bhar_prefiling")
    sec["prefiling_window_post_rule"] = stat(pr[pr.bhar_prefiling.notna() & pr.post_rule], "bhar_prefiling")
    sec["gift_date_1_60"] = stat(pr[pr.bhar_giftdate.notna()], "bhar_giftdate")
    for k in ("december", "ceo_cfo", "under_2b"):
        m = {"december": pr.december, "ceo_cfo": pr.ceo_cfo, "under_2b": pr.mcap < TWO_B}[k]
        sec[k + "_half1"] = stat(pr[m & (pr.half == 1)])
        sec[k + "_half2"] = stat(pr[m & (pr.half == 2)])
        sec[k + "_pre_rule"] = stat(pr[m & ~pr.post_rule])
        sec[k + "_post_rule"] = stat(pr[m & pr.post_rule])
    res["secondary"] = sec

    # information-only checks
    info = {}
    lo, hi = pr.bhar.quantile([0.01, 0.99])
    info["winsorised_1_99"] = stat(pr.assign(bw=pr.bhar.clip(lo, hi)), "bw")
    info["etf_benchmark"] = stat(pr, "bhar_etf")
    info["raw_stock_return"] = stat(pr, "ret_stock")
    info["cluster_by_issuer"] = stat(pr, cl="cik")
    # first event per issuer in any 60-trading-day span
    keep, last_i = [], {}
    for r_ in pr.sort_values("i0").itertuples():
        li = last_i.get(r_.cik)
        if li is None or r_.i0 > li + WINDOW:
            keep.append(r_.Index)
            last_i[r_.cik] = r_.i0
    info["non_overlapping"] = stat(pr.loc[keep])
    info["days_1_20"] = stat(pr, "bhar_1_20")
    info["days_1_5"] = stat(pr, "bhar_1_5")
    info["value_ge_1m"] = stat(pr[pr.value >= MIN_VALUE])
    info["pct_ge_1_only"] = stat(pr[~(pr.value >= MIN_VALUE)])
    info["value_ge_10m"] = stat(pr[pr.value >= 10 * MIN_VALUE])
    info["by_year"] = {int(y): stat(d) for y, d in pr.groupby(pr.filing_date.dt.year)}
    res["info"] = info

    res["counts"] = {"priced_events": int(len(pr)), "issuers": int(pr.cik.nunique()),
                     "filing_months": int(pr.filing_month.nunique()),
                     "pre_rule": int((~pr.post_rule).sum()), "post_rule": int(pr.post_rule.sum()),
                     "december": int(pr.december.sum()), "ceo_cfo": int(pr.ceo_cfo.sum()),
                     "under_2b": int((pr.mcap < TWO_B).sum()), "over_2b": int((pr.mcap >= TWO_B).sum()),
                     "mcap_unknown": int(pr.mcap.isna().sum()),
                     "value_ge_1m": int((pr.value >= MIN_VALUE).sum()),
                     "median_value": float(pr.value.median()), "median_max_pct": float(pr.max_pct.median())}
    keepc = ["cik", "name", "ticker", "map_source", "filing_date", "gift_date", "lag_days", "n_gifts",
             "shares", "value", "max_pct", "ceo_cfo", "december", "post_rule", "owner", "title",
             "form", "accession", "sic", "ff12", "mcap", "bench_kind", "bhar", "ret_stock",
             "ret_bench", "bhar_etf", "bhar_prefiling", "bhar_giftdate", "bhar_1_20", "bhar_1_5",
             "days_in_window", "half"]
    out_ev = pr[keepc].copy()
    for c in ("bhar", "ret_stock", "ret_bench", "bhar_etf", "bhar_prefiling", "bhar_giftdate",
              "bhar_1_20", "bhar_1_5", "max_pct"):
        out_ev[c] = out_ev[c].round(5)
    out_ev["value"] = out_ev.value.round(0)
    out_ev["mcap"] = out_ev.mcap.round(-3)
    out_ev.to_csv(DATA / "events.csv.gz", index=False)
    return res


def main():
    stage = sys.argv[1] if len(sys.argv) > 1 else "all"
    P = Panel()
    res = {}
    if stage in ("events", "all"):
        _, log = build_events(P)
    if stage in ("returns", "all"):
        log = json.loads((CACHE / "stage1_log.json").read_text())
        res = run_returns(P)
        res["stage1"] = log
        (HERE / "results.json").write_text(json.dumps(res, indent=1, default=str))
        p = res["primary"]
        print(json.dumps(p, indent=1, default=str))


if __name__ == "__main__":
    main()
