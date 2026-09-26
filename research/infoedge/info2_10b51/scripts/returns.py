"""INFO-2 event study (PREREG D4, D5): abnormal returns over trading days +1..+60 after the filing date.

Benchmark: equal-weighted size-quintile x Fama-French-12 cell of all 10-Q/10-K filers with Yahoo prices,
formed each month-end (event firm excluded); IWM/SPY as robustness.
Writes data/event_returns_terminations.csv, data/event_returns_adoptions.csv and results.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sec
from events import shares_outstanding

DATA = sec.ROOT / "data"
PX = sec.CACHE / "yahoo" / "px"
H = 60
COST = 0.002
LAST = pd.Timestamp("2026-09-25")


# --------------------------------------------------------------------------- industry
def ff12(sic) -> int:
    try:
        s = int(sic)
    except (TypeError, ValueError):
        return 12
    r = lambda a, b: a <= s <= b
    if r(100, 999) or r(2000, 2399) or r(2700, 2749) or r(2770, 2799) or r(3100, 3199) or r(3940, 3989):
        return 1
    if r(2500, 2519) or r(2590, 2599) or r(3630, 3659) or r(3710, 3711) or s in (3714, 3716) or r(3750, 3751) \
            or s == 3792 or r(3900, 3939) or r(3990, 3999):
        return 2
    if r(2520, 2589) or r(2600, 2699) or r(2750, 2769) or r(3000, 3099) or r(3200, 3569) or r(3580, 3629) \
            or r(3700, 3709) or r(3712, 3713) or s == 3715 or r(3717, 3749) or r(3752, 3791) or r(3793, 3799) \
            or r(3830, 3839) or r(3860, 3899):
        return 3
    if r(1200, 1399) or r(2900, 2999):
        return 4
    if r(2800, 2829) or r(2840, 2899):
        return 5
    if r(3570, 3579) or r(3660, 3692) or r(3694, 3699) or r(3810, 3829) or r(7370, 7379):
        return 6
    if r(4800, 4899):
        return 7
    if r(4900, 4949):
        return 8
    if r(5000, 5999) or r(7200, 7299) or r(7600, 7699):
        return 9
    if r(2830, 2839) or s == 3693 or r(3840, 3859) or r(8000, 8099):
        return 10
    if r(6000, 6999):
        return 11
    return 12


# --------------------------------------------------------------------------- panels
def load_panels():
    files = list(PX.glob("*.parquet"))
    close, split = {}, {}
    for p in files:
        d = pd.read_parquet(p)
        d = d[~d.index.duplicated()]
        close[p.stem] = d["close"]
        split[p.stem] = d["split"] if "split" in d else pd.Series(0.0, index=d.index)
    P = pd.DataFrame(close).sort_index()
    S = pd.DataFrame(split).reindex(P.index).fillna(0.0)
    cal = P["SPY"].dropna().index
    cal = cal[cal <= LAST]
    P = P.reindex(cal)
    S = S.reindex(cal).fillna(0.0)
    # returns only inside each stock's own trading span; gaps inside the span earn 0
    first = P.apply(lambda s: s.first_valid_index())
    lastv = P.apply(lambda s: s.last_valid_index())
    Pf = P.ffill()
    R = Pf.pct_change(fill_method=None)
    idx = P.index.values
    for c in P.columns:
        if first[c] is None:
            continue
        R.loc[(idx <= np.datetime64(first[c])) | (idx > np.datetime64(lastv[c])), c] = np.nan
    # split factor after each date: raw price = adjusted price x product of split ratios after the date
    Sr = S.replace(0.0, 1.0)
    after = Sr[::-1].cumprod()[::-1].shift(-1).fillna(1.0)
    return P, R, after, first, lastv


def cik_ticker(P):
    tk = pd.read_csv(DATA / "tickers.csv")
    m = {}
    for r in tk.itertuples():
        for s in (r.yahoo, r.yahoo_alt):
            if isinstance(s, str) and s in P.columns:
                m[r.cik] = s
                break
    return m


def shares_panel():
    """(cik, filed) -> cover-page shares outstanding."""
    so = shares_outstanding()
    f = pd.read_csv(DATA / "filings.csv.gz", usecols=["adsh", "cik", "filed", "sic"], low_memory=False,
                    parse_dates=["filed"])
    f = f.merge(so, left_on="adsh", right_index=True, how="inner").sort_values("filed")
    return f


def build_benchmark(P, R, after, c2t):
    """Month-end cell assignment (size quintile x FF12) and daily cell sums / counts."""
    f = shares_panel()
    sic = pd.read_csv(DATA / "filings.csv.gz", usecols=["cik", "sic"], low_memory=False).dropna().drop_duplicates(
        "cik", keep="last").set_index("cik").sic
    t2c = {}
    for c, t in c2t.items():
        t2c.setdefault(t, c)
    tick = [t for t in P.columns if t in t2c]
    ciks = [t2c[t] for t in tick]
    ind = pd.Series([ff12(sic.get(c)) for c in ciks], index=tick)
    # shares outstanding as of each date: latest cover-page value filed on/before the date (else the first one)
    sh = pd.DataFrame(index=P.index, columns=tick, dtype=float)
    fg = f.groupby("cik")
    for t, c in zip(tick, ciks):
        if c not in fg.groups:
            continue
        g = fg.get_group(c)
        s = pd.Series(g.shares_out.values, index=g.filed.values)
        s = s[~s.index.duplicated(keep="last")]
        s = s.reindex(P.index.union(s.index)).ffill().bfill().reindex(P.index)
        sh[t] = s.values
    raw = P[tick] * after[tick]
    mcap = raw * sh
    months = P.index.to_series().groupby(P.index.to_period("M")).max()
    Rc = R[tick].where((R[tick] <= 1.0) & (R[tick] >= -0.75))
    cells, sums, cnts, sizeq, bps = {}, {}, {}, {}, {}
    for i, (per, me) in enumerate(months.items()):
        mc = mcap.loc[me]
        px = P.loc[me, tick]
        ok = mc.notna() & (px >= 1.0) & (mc > 0)
        if ok.sum() < 100:
            continue
        q = pd.qcut(mc[ok], 5, labels=False) + 1
        bps[per] = np.quantile(mc[ok].values, [0.2, 0.4, 0.6, 0.8])
        cell = (q * 100 + ind[ok.index[ok]]).astype(int)
        cells[per] = cell
        sizeq[per] = q
        nxt = per + 1
        days = P.index[P.index.to_period("M") == nxt]
        if len(days) == 0:
            continue
        sub = Rc.loc[days, cell.index]
        for cid in np.unique(cell.values):
            cols = cell.index[cell.values == cid]
            sums[(nxt, cid)] = sub[cols].sum(axis=1, min_count=1)
            cnts[(nxt, cid)] = sub[cols].notna().sum(axis=1)
        for qq in range(1, 6):
            cols = q.index[q.values == qq]
            sums[(nxt, -qq)] = sub[cols].sum(axis=1, min_count=1)
            cnts[(nxt, -qq)] = sub[cols].notna().sum(axis=1)
    return {"cells": cells, "sums": sums, "cnts": cnts, "bps": bps, "mcap": mcap, "ind": ind, "sizeq": sizeq}


# --------------------------------------------------------------------------- one event
def event_ar(ev, P, R, B, c2t, bench_etf):
    cal = P.index
    tkr = c2t.get(ev.cik)
    out = {"ticker": tkr, "ar": np.nan, "ar_etf": np.nan, "ar_2_60": np.nan, "mcap0": np.nan, "status": ""}
    pos0 = cal.searchsorted(ev.filed, side="right") - 1
    if pos0 < 0 or pos0 + H >= len(cal):
        out["status"] = "window_incomplete"
        return out
    if tkr is None:
        out["status"] = "no_price"
        return out
    d0 = cal[pos0]
    if pd.isna(P[tkr].iloc[:pos0 + 1].last_valid_index()) or P[tkr].iloc[:pos0 + 1].last_valid_index() < d0 - pd.Timedelta(days=10) \
            or P[tkr].iloc[pos0 + 1:pos0 + 3].notna().sum() == 0:
        out["status"] = "no_price_at_event"
        return out
    days = cal[pos0 + 1:pos0 + 1 + H]
    r = R[tkr].reindex(days)
    # cell of the event firm: its month-end cell if in the universe, else by its own market cap on day 0
    mc0 = B["mcap"][tkr].loc[d0] if tkr in B["mcap"].columns else np.nan
    out["mcap0"] = mc0
    per_form = d0.to_period("M") - 1
    cell = B["cells"].get(per_form)
    if cell is not None and tkr in cell.index:
        cid = int(cell[tkr])
        inuniv = True
    else:
        bp = B["bps"].get(per_form)
        if bp is None or pd.isna(mc0):
            cid = None
        else:
            qq = int(np.searchsorted(bp, mc0) + 1)
            cid = qq * 100 + int(B["ind"].get(tkr, 12))
        inuniv = False
    b = []
    for d in days:
        per = d.to_period("M")
        key = (per, cid)
        s = B["sums"].get(key)
        n = B["cnts"].get(key)
        use_cell = s is not None and n is not None and n.get(d, 0) - (1 if inuniv else 0) >= 10
        if not use_cell and cid is not None:
            key = (per, -(cid // 100))
            s, n = B["sums"].get(key), B["cnts"].get(key)
        if s is None or cid is None:
            b.append(np.nan)
            continue
        own = r.get(d)
        cprev = B["cells"].get(per - 1)
        own_cell = int(cprev[tkr]) if cprev is not None and tkr in cprev.index else None
        same = own_cell is not None and (own_cell == key[1] if key[1] > 0 else own_cell // 100 == -key[1])
        own_in = same and pd.notna(own) and -0.75 <= own <= 1.0
        ss, nn = s.get(d, np.nan), n.get(d, 0)
        if own_in:
            ss, nn = ss - own, nn - 1
        b.append(ss / nn if nn > 0 else np.nan)
    b = pd.Series(b, index=days)
    etf = bench_etf(mc0)
    re = R[etf].reindex(days)
    # after delisting (no stock return) the position earns the benchmark
    r_b = r.fillna(b)
    r_e = r.fillna(re)
    if b.isna().all():
        b = re  # no size-industry cell (no market cap): the common-rule fallback, IWM / SPY
        out["bench"] = "etf_fallback"
    else:
        out["bench"] = "size_industry"
    if True:
        b = b.fillna(re)
        out["ar"] = float(np.prod(1 + r_b.fillna(b)) - np.prod(1 + b))
        out["ar_2_60"] = float(np.prod(1 + r_b.fillna(b).iloc[1:]) - np.prod(1 + b.iloc[1:]))
        out["status"] = "ok"
    out["ar_etf"] = float(np.prod(1 + r_e) - np.prod(1 + re))
    out["delisted_in_window"] = bool(r.iloc[-5:].isna().all())
    out["in_universe"] = inuniv
    return out


# --------------------------------------------------------------------------- stats
def clustered(x: pd.Series, g: pd.Series, sign=1, cost=COST):
    x = x.astype(float)
    m = x.mean()
    n = len(x)
    if n < 3:
        return {"n": n, "mean": m, "t": np.nan, "net": np.nan, "t_net": np.nan, "clusters": g.nunique()}
    e = x - m
    s = e.groupby(g.values).sum()
    G = len(s)
    var = G / (G - 1) * (s ** 2).sum() / n ** 2
    se = np.sqrt(var)
    net = sign * m - cost
    return {"n": int(n), "mean": float(m), "se": float(se), "t": float(m / se), "net_in_trade_direction": float(net),
            "t_net": float(net / se), "median": float(x.median()), "share_positive": float((x > 0).mean()),
            "clusters": int(G), "sd": float(x.std())}


def summarize(df, col="ar", sign=1):
    d = df[df[col].notna()].sort_values("filed")
    res = clustered(d[col], d.fm, sign)
    med = d.filed.iloc[len(d) // 2] if len(d) else None
    h1, h2 = d[d.filed < med], d[d.filed >= med]
    res["half1"] = clustered(h1[col], h1.fm, sign) | {"from": str(h1.filed.min())[:10], "to": str(h1.filed.max())[:10]}
    res["half2"] = clustered(h2[col], h2.fm, sign) | {"from": str(h2.filed.min())[:10], "to": str(h2.filed.max())[:10]}
    res["verdict_yes"] = bool(res.get("t_net", 0) >= 2.5 and sign * res["half1"]["mean"] > 0
                              and sign * res["half2"]["mean"] > 0)
    return res


def bounds(df, sign=1):
    """-30% / +15% for events whose company has no Yahoo price."""
    out = {}
    miss = df.status.isin(["no_price", "no_price_at_event"])
    base = df[(df.status == "ok") | miss].copy()
    for lab, v in (("minus30", -0.30), ("plus15", 0.15)):
        x = base.ar.where(~base.status.isin(["no_price", "no_price_at_event"]), v)
        out[lab] = clustered(x, base.fm, sign)
    out["n_missing"] = int(miss.sum())
    return out


K_PLACEBO = 5
SEED = 20260926


def placebo(events, P, R, B, c2t, etf, avoid, sign=1):
    """Coordinator-requested diagnostic (after INFO-5): the same companies on random non-event dates in the
    same calendar year. For each priced event, K dates are drawn (seeded) from trading days of the event's
    calendar year with a complete +60 window, inside the stock's priced life, at least 60 trading days from
    any of the company's own disclosures in `avoid` (cik -> list of filing dates). Same benchmark code.
    Returns per-event columns placebo (size-industry) and placebo_etf, and the event-minus-placebo stats."""
    rng = np.random.default_rng(SEED)
    cal = P.index
    last_ok = len(cal) - 1 - H
    pl, pl_e, pl_b, pl_a = [], [], [], []
    for ev in events.itertuples():
        tkr = c2t.get(ev.cik)
        yr = ev.filed.year
        lo = cal.searchsorted(pd.Timestamp(yr, 1, 1))
        hi = min(cal.searchsorted(pd.Timestamp(yr, 12, 31), side="right") - 1, last_ok)
        fv = P[tkr].first_valid_index()
        lv = P[tkr].last_valid_index()
        own = [cal.searchsorted(d) for d in avoid.get(ev.cik, [])]
        cand = [i for i in range(lo, hi + 1) if fv <= cal[i] and cal[min(i + H, len(cal) - 1)] <= lv
                and all(abs(i - o) >= H for o in own)]
        if not cand:
            pl.append(np.nan); pl_e.append(np.nan); pl_b.append(np.nan); pl_a.append(np.nan)
            continue
        pick = rng.choice(cand, size=min(K_PLACEBO, len(cand)), replace=False)
        a, e, bef, aft = [], [], [], []
        for i in pick:
            fake = pd.Series({"cik": ev.cik, "filed": cal[i]})
            o = event_ar(fake, P, R, B, c2t, etf)
            if o["status"] == "ok":
                a.append(o["ar"]); e.append(o["ar_etf"])
                (bef if cal[i] < ev.filed else aft).append(o["ar"])
        pl.append(np.mean(a) if a else np.nan)
        pl_e.append(np.mean(e) if e else np.nan)
        pl_b.append(np.mean(bef) if bef else np.nan)
        pl_a.append(np.mean(aft) if aft else np.nan)
    ev2 = events.copy()
    ev2["placebo"] = pl
    ev2["placebo_etf"] = pl_e
    ev2["placebo_before"] = pl_b
    ev2["placebo_after"] = pl_a
    ev2["ev_minus_pl_after"] = ev2.ar - ev2.placebo_after
    ev2["ev_minus_pl"] = ev2.ar - ev2.placebo
    ev2["ev_minus_pl_etf"] = ev2.ar_etf - ev2.placebo_etf
    out = {"placebo_mean": summarize(ev2[ev2.placebo.notna()], "placebo", sign),
           "event_minus_placebo": summarize(ev2[ev2.ev_minus_pl.notna()], "ev_minus_pl", sign),
           "placebo_mean_iwm_spy": summarize(ev2[ev2.placebo_etf.notna()], "placebo_etf", sign),
           "event_minus_placebo_iwm_spy": summarize(ev2[ev2.ev_minus_pl_etf.notna()], "ev_minus_pl_etf", sign),
           "placebo_dates_before_event_mean": summarize(ev2[ev2.placebo_before.notna()], "placebo_before", sign),
           "placebo_dates_after_event_mean": summarize(ev2[ev2.placebo_after.notna()], "placebo_after", sign),
           "event_minus_placebo_after_only": summarize(ev2[ev2.ev_minus_pl_after.notna()], "ev_minus_pl_after", sign),
           "n_with_placebo": int(ev2.placebo.notna().sum()), "K": K_PLACEBO, "seed": SEED}
    return ev2, out


def run():
    P, R, after, first, lastv = load_panels()
    c2t = cik_ticker(P)
    B = build_benchmark(P, R, after, c2t)
    etf = lambda mc: "IWM" if (pd.isna(mc) or mc < 2e9) else "SPY"

    t = pd.read_csv(DATA / "terminations.csv", parse_dates=["filed", "term_date"], low_memory=False)
    t = t[(t.filed >= "2023-07-01")]
    ad = pd.read_csv(DATA / "adoptions.csv.gz", parse_dates=["filed"], low_memory=False)
    ad = ad[(ad.filed >= "2023-07-01")]

    def attach(df):
        rows = [event_ar(r, P, R, B, c2t, etf) for r in df.itertuples()]
        return pd.concat([df.reset_index(drop=True), pd.DataFrame(rows)], axis=1)

    te = attach(t[t.primary | t.early_or_repl | (t.trm_class == "early")])
    te.to_csv(DATA / "event_returns_terminations.csv", index=False)
    miss = te[te.status.isin(["no_price", "no_price_at_event"])]
    miss[["company", "cik", "ticker", "filed", "name", "title", "trm_class", "primary", "source", "status"]].to_csv(
        DATA / "missing_prices_terminations.csv", index=False)
    # adoption secondary: cutoff over all usable adoption ratios with a complete window
    cal = P.index
    ad["complete"] = [cal.searchsorted(f, side="right") - 1 + H < len(cal) for f in ad.filed]
    usable = ad[ad.pct_out.notna() & (ad.pct_out > 0) & ~ad.ratio_error.fillna(False) & ad.complete]
    cut = float(usable.pct_out.quantile(0.8))
    top = usable[usable.pct_out >= cut].copy()
    # per-quarter cutoff (robustness)
    usable = usable.assign(q=usable.filed.dt.to_period("Q"))
    qcut = usable.groupby("q").pct_out.transform(lambda s: s.quantile(0.8))
    top_q = usable[usable.pct_out >= qcut]
    ae = attach(pd.concat([top.assign(top_full=True), top_q[~top_q.index.isin(top.index)].assign(top_full=False)]))
    ae["top_q"] = ae.adsh.astype(str) + ae.person.astype(str)
    tq = set((top_q.adsh.astype(str) + top_q.person.astype(str)))
    ae["top_q"] = ae.top_q.isin(tq)
    ae.to_csv(DATA / "event_returns_adoptions.csv", index=False)

    res = {"cutoff_date_last_complete_filing": str(cal[len(cal) - 1 - H].date()), "adoption_cutoff_pct_out": cut}
    prim = te[te.primary.astype(bool)]
    ok = prim[prim.status == "ok"]
    res["counts"] = {
        "terminations_all": int(len(t)), "by_class": t.trm_class.value_counts().to_dict(),
        "primary_all_dates": int(t.primary.sum()),
        "primary_by_source": t[t.primary].source.value_counts().to_dict(),
        "primary_window_complete": int((prim.status != "window_incomplete").sum()),
        "primary_status": prim.status.value_counts().to_dict(),
        "primary_ok": int(len(ok)), "primary_filings_ok": int(ok.adsh.nunique()),
        "primary_ceo": int(ok.is_ceo.fillna(False).astype(bool).sum()), "primary_cfo": int(ok.is_cfo.fillna(False).astype(bool).sum()),
        "primary_dir": int(ok.is_dir.fillna(False).astype(bool).sum()),
        "adoptions_all": int(len(ad)), "adoptions_usable_ratio": int(len(usable)), "adoptions_top20": int(len(top)),
    }
    res["missing_price_companies"] = sorted(set(prim[prim.status.isin(["no_price", "no_price_at_event"])].company.astype(str)))
    res["primary"] = summarize(ok)
    res["primary_bounds"] = bounds(prim[prim.status != "window_incomplete"])
    # robustness
    rb = {}
    rb["tagged_only"] = summarize(ok[ok.source == "xbrl"])
    rb["text_only"] = summarize(ok[ok.source == "text"])
    eor = te[te.early_or_repl.astype(bool) & (te.status == "ok")]
    rb["early_plus_replacement"] = summarize(eor)
    rb["replacement_only"] = summarize(eor[eor.trm_class == "replacement"])
    rb["days_2_60"] = summarize(ok, "ar_2_60")
    rb["iwm_spy_benchmark"] = summarize(prim[prim.ar_etf.notna() & (prim.status == "ok")], "ar_etf")
    w = ok.copy()
    lo, hi = w.ar.quantile([0.01, 0.99])
    w["arw"] = w.ar.clip(lo, hi)
    rb["winsorized_1_99"] = summarize(w, "arw")
    rb["one_per_filing"] = summarize(ok.sort_values("filed").drop_duplicates("adsh"))
    rb["ceo_cfo_only"] = summarize(ok[ok.is_ceo.fillna(False).astype(bool) | ok.is_cfo.fillna(False).astype(bool)])
    rb["all_early_any_officer"] = summarize(te[(te.trm_class == "early") & ~te.dup.astype(bool) & ~te.trm_stale.astype(bool)
                                               & (te.status == "ok")])
    res["robustness"] = rb
    # coordinator-requested lines next to the headline: placebo dates and IWM/SPY
    avoid = t.groupby("cik").filed.apply(list).to_dict()
    ok_pl, res["primary_placebo"] = placebo(ok, P, R, B, c2t, etf, avoid)
    ok_pl.to_csv(DATA / "event_returns_primary_with_placebo.csv", index=False)
    res["primary_iwm_spy"] = rb["iwm_spy_benchmark"]
    _, res["under_2b_placebo"] = placebo(ok[ok.mcap0 < 2e9], P, R, B, c2t, etf, avoid)
    # secondaries
    res["secondary_under_2b"] = summarize(ok[ok.mcap0 < 2e9])
    res["secondary_2b_plus"] = summarize(ok[ok.mcap0 >= 2e9])
    aok = ae[(ae.status == "ok") & ae.top_full.astype(bool)]
    res["secondary_adoptions_top20"] = summarize(aok, sign=-1)
    res["secondary_adoptions_top20_bounds"] = bounds(ae[ae.top_full.astype(bool) & (ae.status != "window_incomplete")], sign=-1)
    res["secondary_adoptions_top20_perquarter_cutoff"] = summarize(ae[(ae.status == "ok") & ae.top_q], sign=-1)
    res["secondary_adoptions_top20_iwm_spy"] = summarize(ae[(ae.status == "ok") & ae.top_full.astype(bool)], "ar_etf", sign=-1)
    res["adoption_status"] = ae[ae.top_full.astype(bool)].status.value_counts().to_dict()
    avoid_a = top.groupby("cik").filed.apply(list).to_dict()
    aok_pl, res["adoptions_top20_placebo"] = placebo(aok, P, R, B, c2t, etf, avoid_a, sign=-1)
    aok_pl.to_csv(DATA / "event_returns_adoptions_top20_with_placebo.csv", index=False)
    res["benchmark"] = {"universe_tickers": int(len(B["ind"])),
                        "median_month_universe": float(np.median([len(c) for c in B["cells"].values()]))}
    (sec.ROOT / "results.json").write_text(json.dumps(res, indent=1, default=str))
    return res


if __name__ == "__main__":
    r = run()
    print(json.dumps({k: r[k] for k in ("counts", "primary")}, indent=1, default=str))
