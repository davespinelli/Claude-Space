#!/usr/bin/env python3
"""Stage 6: dated events.

For every mapped contract action (positive obligation, action date FY2010
onward, company alive at SEC on the action date):
  public date   DoD (awarding agency = Department of Defense): action date + 90
                calendar days; civilian: action date + 5 federal business days;
                then refined with FPDS record dates (see PREREG Deviations);
  day 0         last trading day on or before the public date; day +1 is the
                first trading day after it;
  market cap    Yahoo split-adjusted close on day 0 x SEC share count (latest
                dei cover-page count filed on or before day 0, else us-gaap
                balance-sheet count), put on the same split basis;
  size ratio    obligation / market cap on day 0.
Candidates: ratio >= 2% and market cap < $2B. Several qualifying actions of
one company with the same public date form one event (amounts summed).
8-K check: any 8-K or 8-K/A filed from 5 trading days before to 5 trading
days after any of the event's action dates -> "announced".

Companies without usable prices ("missing"): public float (dei) filed on or
before the action date stands in for market cap in the 2% / $2B screens.

Writes cache/all_*_actions.parquet, data/candidates.parquet, data/events.parquet, data/missing_events.parquet.
"""
from __future__ import annotations

import sys

import numpy as np
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay

from common import CACHE, DATA, log, sec_json

PX = CACHE / "prices"
FIRST_ACTION = pd.Timestamp("2009-10-01")
RATIO_MIN = 0.02
MCAP_MAX = 2e9
WIN = 20
BDAY = CustomBusinessDay(calendar=USFederalHolidayCalendar())
SHARE_MAX_AGE = pd.Timedelta(days=400)
BACKFILL = pd.Timedelta(days=548)


def load_prices():
    px = pd.read_parquet(PX / "daily.parquet")
    px["date"] = pd.to_datetime(px.date).dt.tz_localize(None).dt.normalize()
    px = px.drop_duplicates(["date", "ticker"], keep="last")
    close = px.pivot(index="date", columns="ticker", values="close").sort_index()
    adj = px.pivot(index="date", columns="ticker", values="adj").sort_index()
    split = px.pivot(index="date", columns="ticker", values="split").sort_index().fillna(0.0)
    cal = pd.DatetimeIndex(adj["IWM"].dropna().index).astype("datetime64[ns]")
    close.index = close.index.astype("datetime64[ns]")
    adj.index = adj.index.astype("datetime64[ns]")
    split.index = split.index.astype("datetime64[ns]")
    return close.reindex(cal), adj.reindex(cal), split, cal


def split_after(split: pd.DataFrame, tk: str, when: pd.Timestamp) -> float:
    if tk not in split.columns:
        return 1.0
    s = split[tk]
    s = s[(s.index > when) & (s > 0) & (s != 1.0)]
    return float(np.prod(s.to_numpy())) if len(s) else 1.0


def shares_at(F: pd.DataFrame, when: pd.Timestamp):
    """(shares, as-of end date, source) known on `when`."""
    out = {}
    for tag in ("EntityCommonStockSharesOutstanding", "CommonStockSharesOutstanding"):
        f = F[(F.tag == tag) & (F.filed <= when) & (F.end >= when - SHARE_MAX_AGE)]
        if len(f):
            r = f.sort_values(["end", "filed"]).iloc[-1]
            out[tag] = (float(r.val), r.end)
    fl = F[(F.tag == "EntityPublicFloat") & (F.filed <= when) & (F.end >= when - SHARE_MAX_AGE)]
    pf = float(fl.sort_values(["end", "filed"]).iloc[-1].val) if len(fl) else np.nan
    return out, pf


def public_date_rule(action: pd.Timestamp, dod: bool) -> pd.Timestamp:
    return action + pd.Timedelta(days=90) if dod else action + 5 * BDAY


def fpds_dates() -> pd.DataFrame | None:
    p = DATA / "fpds_dates.parquet"
    return pd.read_parquet(p) if p.exists() else None


def public_date(row, fp: dict) -> tuple[pd.Timestamp, str]:
    """PREREG D1-D3: civilian = FPDS approval + 1 federal business day (the
    actual release: FPDS shows civilian records on approval, USAspending loads
    them overnight); DoD = action + 90 days, or approval + 1 business day if the
    record was entered later than that. No FPDS record -> pre-registered rule."""
    rule = public_date_rule(row.action_date, row.dod)
    f = fp.get(row.contract_transaction_unique_key)
    if f is None or pd.isna(f.get("approved")):
        return rule, "rule_no_fpds"
    appr = max(pd.Timestamp(f["approved"]).normalize(), row.action_date)
    seen = appr + 1 * BDAY
    if row.dod:
        return (rule, "dod_rule") if rule >= seen else (seen, "dod_late_entry")
    return seen, "fpds_approved"


def filings_8k(cik: int) -> pd.Series:
    js = sec_json(f"https://data.sec.gov/submissions/CIK{cik:010d}.json",
                  CACHE / "sec" / "subs_fresh" / f"CIK{cik:010d}.json.gz")
    if not isinstance(js, dict):
        return pd.Series(dtype="datetime64[ns]")
    frames = [js.get("filings", {}).get("recent", {})]
    for fi in js.get("filings", {}).get("files", []) or []:
        j2 = sec_json(f"https://data.sec.gov/submissions/{fi['name']}",
                      CACHE / "sec" / "subs_fresh" / f"{fi['name']}.gz")
        if isinstance(j2, dict):
            frames.append(j2)
    d = []
    for fr in frames:
        for form, fd in zip(fr.get("form", []), fr.get("filingDate", [])):
            if form in ("8-K", "8-K/A"):
                d.append(fd)
    return pd.Series(pd.to_datetime(sorted(set(d))))


def main():
    use_fpds = "--rule-only" not in sys.argv
    close, adj, split, cal = load_prices()
    last_day = cal[-1]
    st = pd.read_csv(PX / "status.csv").drop_duplicates("ticker", keep="last").set_index("ticker").status
    M = pd.read_parquet(CACHE / "mapped.parquet")
    M = M[M.in_universe & M.alive & (M.amount > 0) & (M.action_date >= FIRST_ACTION)].copy()
    M["action_date"] = M.action_date.astype("datetime64[ns]")
    M = M[M.cik.isin(pd.read_csv(DATA / "possible_ciks.csv").cik)]   # stage 5's pre-screen
    M["yf"] = M.ticker.fillna("").str.upper().str.replace(".", "-", regex=False)
    rec = pd.read_csv(DATA / "recycled_symbols_skipped.csv")
    recycled = set(rec.cik)
    S = pd.read_parquet(DATA / "shares_long.parquet")
    # public-float values off by 1,000x occur (e.g. Kratos 2018-19): a float more
    # than 20x away from the company's median float is dropped
    fl = S.tag == "EntityPublicFloat"
    med = S[fl].groupby("cik").val.transform("median")
    bad_fl = pd.Series(False, index=S.index)
    bad_fl[fl] = (S.loc[fl, "val"] > 20 * med) | (S.loc[fl, "val"] < med / 20) | (S.loc[fl, "val"] <= 0)
    log(f"public-float facts dropped as scale errors: {int(bad_fl.sum())}")
    S = S[~bad_fl]
    Sg = {c: g for c, g in S.groupby("cik")}
    fp = {}
    if use_fpds:
        FD = fpds_dates()
        if FD is not None:
            fp = FD.set_index("contract_transaction_unique_key")[["approved", "created"]].to_dict("index")
    log(f"{len(M)} mapped positive actions; FPDS dates for {len(fp)}")

    # public dates: pre-registered rule, vectorised; FPDS refinement where looked up
    import warnings
    warnings.simplefilter("ignore", pd.errors.PerformanceWarning)
    ad = pd.DatetimeIndex(M.action_date)
    civ_rule = pd.Series(ad + 5 * BDAY, index=M.index) if len(M) else pd.Series(dtype="datetime64[ns]")
    M["public_date"] = np.where(M.dod, M.action_date + pd.Timedelta(days=90), civ_rule)
    M["public_date"] = pd.to_datetime(M.public_date)
    M["date_src"] = "rule"
    if use_fpds and fp:
        hit = M.contract_transaction_unique_key.isin(fp.keys())
        res = [public_date(r, fp) for r in M[hit].itertuples()]
        M.loc[hit, "public_date"] = [x[0] for x in res]
        M.loc[hit, "date_src"] = [x[1] for x in res]
        M.loc[~hit, "date_src"] = "rule_no_fpds"
    M["i0"] = cal.searchsorted(M.public_date, side="right") - 1
    M = M[M.i0 >= 0].copy()
    M["day0"] = cal[M.i0.to_numpy()]

    def asof(F, tag, q):
        """value (on today's split basis), as-of end date, for each query date in q (Series of dates)."""
        f = F[F.tag == tag].sort_values("filed")
        out = pd.DataFrame({"q": pd.to_datetime(q).astype("datetime64[ns]").to_numpy()}, index=q.index)
        if not len(f):
            out["v"], out["end"], out["backfill"] = np.nan, pd.NaT, False
            return out
        f = f[["filed", "end", "val"]].rename(columns={"filed": "fd"})
        f["fd"] = f.fd.astype("datetime64[ns]")
        f["end"] = f.end.astype("datetime64[ns]")
        o = pd.merge_asof(out.reset_index().sort_values("q"), f, left_on="q", right_on="fd", direction="backward")
        o = o.set_index("index").reindex(out.index)
        o.loc[o.end < o.q - SHARE_MAX_AGE, "val"] = np.nan
        out["v"], out["end"], out["backfill"] = o.val, o.end, False
        # XBRL cover data start in 2009-2011: before a company's first XBRL filing
        # the first count filed within the next 18 months is used (flagged)
        miss = out.v.isna()
        if miss.any():
            o2 = pd.merge_asof(out.loc[miss, ["q"]].reset_index().sort_values("q"), f, left_on="q", right_on="fd",
                               direction="forward", tolerance=BACKFILL)
            o2 = o2.set_index("index")
            ok = o2.val.notna()
            out.loc[o2.index[ok], "v"] = o2.val[ok]
            out.loc[o2.index[ok], "end"] = o2.end[ok]
            out.loc[o2.index[ok], "backfill"] = True
        return out

    rows, miss_rows = [], []
    for cik, g in M.groupby("cik"):
        tk = g.yf.iloc[0]
        F = Sg.get(cik, pd.DataFrame(columns=S.columns))
        priced = bool(tk) and tk in close.columns and st.get(tk) == "ok" and cik not in recycled
        base = pd.DataFrame(dict(cik=cik, ticker=tk, company=g.company, sic=g.sic, key=g.contract_transaction_unique_key,
                                 award=g.contract_award_unique_key, piid=g.award_id_piid, mod=g.modification_number,
                                 ref_idv=g.parent_award_id_piid, action_date=g.action_date, amount=g.amount, dod=g.dod,
                                 agency=g.awarding_agency_name, subagency=g.awarding_sub_agency_name,
                                 recipient=g.recipient_name, parent=g.pname, match=g.match,
                                 public_date=g.public_date, date_src=g.date_src, day0=g.day0, i0=g.i0,
                                 desc=g.transaction_description.astype(str).str[:200]))
        if priced:
            cs = close[tk].dropna()
            first_px = cs.index[0]
            q = base.day0
            lk = pd.merge_asof(pd.DataFrame({"q": pd.to_datetime(q).astype("datetime64[ns]").to_numpy(),
                                             "k": q.index}).sort_values("q"),
                               pd.DataFrame({"pd": pd.DatetimeIndex(cs.index).astype("datetime64[ns]"),
                                             "px": cs.to_numpy()}), left_on="q", right_on="pd",
                               direction="backward", tolerance=pd.Timedelta(days=7)).set_index("k").reindex(q.index)
            base["px0"] = lk.px
            pre = base.day0 < first_px                       # not yet listed: not an event
            base = base[~pre]
            has_px = base.px0.notna()
            P, Xm = base[has_px].copy(), base[~has_px].copy()
            if len(P):
                d_ = asof(F, "EntityCommonStockSharesOutstanding", P.day0)
                g_ = asof(F, "CommonStockSharesOutstanding", P.day0)
                w_ = asof(F, "WeightedAverageNumberOfSharesOutstandingBasic", P.day0)
                # no balance-sheet count: weighted-average basic shares (multi-class companies)
                nog = g_.v.isna() & w_.v.notna()
                g_.loc[nog, ["v", "end", "backfill"]] = w_.loc[nog, ["v", "end", "backfill"]]
                pf = asof(F, "EntityPublicFloat", P.day0)
                sf_d = [split_after(split, tk, e) if pd.notna(e) else np.nan for e in d_.end]
                sf_g = [split_after(split, tk, e) if pd.notna(e) else np.nan for e in g_.end]
                mc_d = d_.v.to_numpy(float) * np.array(sf_d, float) * P.px0.to_numpy(float)
                mc_g = g_.v.to_numpy(float) * np.array(sf_g, float) * P.px0.to_numpy(float)
                pfv = pf.v.to_numpy(float)
                mc = np.where(np.isfinite(mc_d), mc_d, mc_g)
                src = np.where(np.isfinite(mc_d), "dei", np.where(np.isfinite(mc_g), "gaap", None))
                both = np.isfinite(mc_d) & np.isfinite(mc_g) & np.isfinite(pfv)
                with np.errstate(divide="ignore", invalid="ignore"):
                    dis = both & (np.maximum(mc_d, mc_g) / np.minimum(mc_d, mc_g) > 3)
                    okd = (mc_d / pfv >= 0.8) & (mc_d / pfv <= 20)
                    okg = (mc_g / pfv >= 0.8) & (mc_g / pfv <= 20)
                use_g = dis & okg & ~okd
                mc = np.where(use_g, mc_g, mc)
                src = np.where(use_g, "gaap_vs_float", src)
                # share-count errors: a zero cap, or a cap below 30% of the company's own
                # latest public float (float cannot exceed market value), is not used
                bad_mc = (mc <= 0) | (np.isfinite(pfv) & (mc < 0.3 * pfv))
                mc = np.where(bad_mc, np.nan, mc)
                src = np.where(bad_mc, "rejected_vs_float", src)
                P["mcap"], P["mcap_src"], P["pfloat"] = mc, src, pfv
                P["shares_backfilled"] = np.where(src == "dei", d_.backfill.to_numpy(bool), g_.backfill.to_numpy(bool))
                P["ratio"] = P.amount / P.mcap
                if g.listing.iloc[0] == "former":
                    # an old symbol that still has Yahoo data must agree with the
                    # company's own public float (research/oplev's check)
                    fr = P.pfloat / P.mcap
                    bad = ~fr.between(0.2, 5.0)
                    if bad.any():
                        B = P[bad].drop(columns=["px0", "mcap", "mcap_src", "ratio", "shares_backfilled"])
                        B["missing_reason"] = "hist_symbol_failed_float_check"
                        miss_rows.append(B)
                        P = P[~bad]
                rows.append(P)
            if len(Xm):                                      # series ended before day 0
                pf = asof(F, "EntityPublicFloat", Xm.action_date)
                Xm["pfloat"] = pf.v.to_numpy(float)
                Xm["missing_reason"] = "no_price_on_day0"
                miss_rows.append(Xm.drop(columns=["px0"]))
        else:
            pf = asof(F, "EntityPublicFloat", base.action_date)
            base["pfloat"] = pf.v.to_numpy(float)
            base["missing_reason"] = ("no_ticker" if not tk else "recycled_symbol" if cik in recycled else "no_yahoo_data")
            miss_rows.append(base)
    C = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
    X = pd.concat(miss_rows, ignore_index=True) if miss_rows else pd.DataFrame()
    if len(X):
        X["ratio_float"] = X.amount / X.pfloat.where(X.pfloat > 0)
    log(f"dated: {len(C)} priced actions ({int(C.mcap.isna().sum())} without a share count), "
        f"{len(X)} actions of unpriced companies")
    C.to_parquet(CACHE / "all_priced_actions.parquet", index=False)
    X.to_parquet(CACHE / "all_missing_actions.parquet", index=False)
    C = C[(C.ratio >= RATIO_MIN) & (C.mcap < MCAP_MAX)].copy()
    X = X[(X.ratio_float >= RATIO_MIN) & (X.pfloat < MCAP_MAX)].copy()
    log(f"candidates: {len(C)} priced actions >= 2% of cap (cap < $2B), {C.cik.nunique()} companies; "
        f"missing-company actions >= 2% of float: {len(X)}, {X.cik.nunique()} companies")
    C.to_parquet(DATA / "candidates.parquet", index=False)
    X.to_parquet(DATA / "missing_candidates.parquet", index=False)

    # 8-K check
    ciks = sorted(set(C.cik) | set(X.cik))
    k8 = {c: filings_8k(int(c)) for c in ciks}
    calpos = pd.Series(np.arange(len(cal)), index=cal)

    def announced(r):
        f = k8.get(r.cik)
        if f is None or not len(f):
            return False
        j = cal.searchsorted(r.action_date, side="left")          # action date or next trading day
        lo = cal[max(j - 5, 0)]
        hi = cal[min(j + 5, len(cal) - 1)] if cal[min(j, len(cal) - 1)] == r.action_date else cal[min(j + 4, len(cal) - 1)]
        return bool(((f >= lo) & (f <= hi)).any())

    for D in (C, X):
        if len(D):
            D["announced"] = D.apply(announced, axis=1)

    def to_events(D, ratio_col):
        g = D.groupby(["cik", "public_date"])
        E = g.agg(ticker=("ticker", "first"), company=("company", "first"), sic=("sic", "first"),
                  day0=("day0", "first"), n_actions=("key", "size"), amount=("amount", "sum"),
                  max_ratio=(ratio_col, "max"), dod=("dod", "max"), dod_all=("dod", "min"),
                  announced=("announced", "max"), first_action=("action_date", "min"),
                  last_action=("action_date", "max"), date_src=("date_src", "first"),
                  keys=("key", lambda s: "|".join(s)), agency=("agency", "first"),
                  parent=("parent", "first"), recipient=("recipient", "first")).reset_index()
        return E

    E = to_events(C, "ratio")
    per = C.groupby(["cik", "public_date"]).agg(mcap=("mcap", "first"), i0=("i0", "first"),
                                                 ratio_sum=("ratio", "sum")).reset_index()
    E = E.merge(per, on=["cik", "public_date"])
    E["complete_window"] = E.i0 + WIN <= len(cal) - 1
    E.to_parquet(DATA / "events.parquet", index=False)
    XE = to_events(X, "ratio_float") if len(X) else pd.DataFrame()
    if len(XE):
        XE = XE.merge(X.groupby(["cik", "public_date"]).agg(missing_reason=("missing_reason", "first"),
                                                            pfloat=("pfloat", "first")).reset_index(),
                      on=["cik", "public_date"])
        XE["complete_window"] = XE.day0.map(lambda d: cal.searchsorted(d) + WIN <= len(cal) - 1)
    XE.to_parquet(DATA / "missing_events.parquet", index=False)
    log(f"events: {len(E)} (DoD {int(E.dod.sum())}, civilian {int((~E.dod).sum())}; "
        f"announced {int(E.announced.sum())}); complete windows {int(E.complete_window.sum())}; "
        f"missing-company events {len(XE)}")


if __name__ == "__main__":
    main()
