#!/usr/bin/env python3
"""Idea 435 — is the untreated BASE BOOK the only thing passing 4b in the overlay corpus?

QUESTION (queue 435, following ideas 186/203)
    Idea 203's nine 4b passes are all U56, all on the non-suppressing arms, and the
    EFFECTIVELY-UNTREATED book already scores Sharpe 1.0913 / OOS 1.1464 on its own.
    Idea 186's P7 said the same thing about a different overlay family.  So the record's
    published "N of M overlay arms clear 4b" counts may be crediting the INSTRUMENT for a
    verdict that belongs to its CARRIER.

    The right decomposition of an overlay arm's 4b pass is:

        pass4b(overlay on carrier C)  =  pass4b(C untreated)          <- the carrier
                                      +  the overlay's own contribution

    and only the second term is an instrument result.  This script measures the
    conditional table

                                    carrier passes 4b   carrier fails 4b
        overlay arm passes 4b            CARRIED            INCREMENTAL
        overlay arm fails 4b            DESTROYED             BOTH-FAIL

    and reports INCREMENTAL / (CARRIED + INCREMENTAL) — the share of overlay 4b passes
    that survive subtracting the untreated base book's own pass.

TWO LEGS
    LEG A (CENSUS, archival)  Every committed CSV in research/backtests/ that carries a 4b
        pass column AND an explicit OFF/none/control level of an overlay-style dial, so the
        untreated carrier row is present in the same file and can be paired mechanically.
        Coverage is reported honestly: files scanned, files qualifying, files dropped by
        reason.  No hand-picking; the OFF vocabulary and the carrier-key allowlist are fixed
        constants below.
    LEG B (FRESH, real backtests)  A purpose-built overlay corpus in which the untreated
        carrier is present BY CONSTRUCTION, so the conditional table has no missing cell.
        3 panels x 4 base books x 2 gross x (1 control + 6 overlay families x 2 levels).
        Every arm is priced at PROTOCOL costs (10 bps), next-day execution, weekly cadence.

PARAMETERS (2, swept, ALL grid points reported)
    p1  level  — each overlay family's own strength dial, 2 pre-registered points per family
    p2  gross  — the carrier's gross exposure in {0.75, 1.00}
    PANEL, BASE BOOK and FAMILY are CORPUS dimensions, reported in full, not tuned.

RULE 8 (required)  Walk-forward on this run's own numbers: within each
    (panel, base book, gross, family) cell the LEVEL is chosen on the IS window
    (<= 2016-12-31) by IS Sharpe and the 2017-2026 window is read once.  Reported against
    (a) the untreated carrier's own OOS (do-nothing on the overlay dial), (b) RULES v2,
    (c) SPY.  An ORACLE-OOS arm (perfect hindsight over the level dial) bounds the headroom.

BOTH KEEP PATHS are evaluated for every arm (PROTOCOL 4a vs live RULES v2, and 4b vs SPY).

SURVIVORSHIP: the SMALL panel is current constituents of a sub-$2B screen only
(data/SMALL_PANEL_README.md); tickers with max_1d_move >= 1.0 in data/small_meta.csv are
dropped first.  The BROAD panel is current constituents of a large-cap list.  Any panel
ordering read off this run inherits that bias.

Outputs (committed): .console.txt .arms.csv .cells.csv .keeppaths.csv .walkforward.csv
                     .census.csv .censusfiles.csv .result.md
Deterministic; no network.
"""
import sys, re, glob, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics  # noqa

STAMP = "2026-09-08_is-the-BASE-BOOK-the-only-thing-passing-4b-in-the-overlay-corpus_cloud"
OUT = Path(__file__).resolve().parent
IS_END = pd.Timestamp("2016-12-31")
COST_BPS = 10.0
FREQ = "W"
WARMUP = 260

_LOG: list[str] = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); _LOG.append(s)


# ======================================================================= panels
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c not in bad]
    return px[keep]

def panels():
    d = {}
    d["u56"] = load_universe()
    d["broad136"] = load_universe(broad=True)
    d["small439"] = small_panel()
    return d


# =============================================================== carrier books
def _eligible(px):
    """1.0 where the name is priced that day."""
    return px.notna().astype(float)

def _norm(e, gross):
    return gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)

def carrier_weights(px, book, gross, spy_is_bench=False):
    """The four untreated base books.  On the SMALL panel SPY is a benchmark column, not a
    constituent, so it is dropped from every book there; on u56/broad SPY is a genuine
    universe member and stays in."""
    cols = [c for c in px.columns if c != "SPY"] if spy_is_bench else list(px.columns)
    q = px[cols]
    if book == "EWALL":
        return _norm(_eligible(q), gross)
    if book == "MA200":
        above = q > q.rolling(200).mean()
        return _norm(_eligible(q), gross).where(above, 0.0)          # de-gross to cash
    if book == "BAND3":
        ma = q.rolling(200).mean()
        raw = pd.DataFrame(np.nan, index=q.index, columns=q.columns)
        raw = raw.mask(q > ma * 1.03, 1.0).mask(q < ma * 0.97, 0.0)
        st = raw.ffill().fillna(0.0) > 0.5
        return _norm(_eligible(q), gross).where(st, 0.0)
    if book == "TOP20":                       # the KEEP-4b candidate form: top-20 EW, no vol scaler
        s, above, vol20 = score(q, vol_scale=False)
        elig = s.where(above)
        rank = elig.rank(axis=1, ascending=False)
        sel = (rank <= 20).astype(float)
        return _norm(sel, gross)
    raise ValueError(book)

BOOKS = ["EWALL", "MA200", "BAND3", "TOP20"]
GROSSES = [0.75, 1.00]


# ==================================================================== overlays
# Each family maps (weights, prices) -> weights, with ONE strength dial.  level index 0/1.
FAMILIES = {
    "GATE":   [0.0, 0.5],     # market 200d-MA gate: multiply the book by f_off when SPY < its MA200
    "DDCTL":  [0.10, 0.20],   # de-gross to 50% while the book's own drawdown is worse than -T
    "BUDGET": [0.25, 0.50],   # rebalance only on the top-share dates by required turnover
    "STOP":   [0.15, 0.25],   # per-name trailing stop off the 63d high, 21-day timeout
    "VOLTGT": [0.10, 0.15],   # scale by clip(target / realised 20d book vol, 0, 1)
    "LAM":    [0.25, 0.50],   # partial rebalance toward the target
}

def _spy_ma_flag(px):
    spy = px["SPY"]
    return (spy > spy.rolling(200).mean()).fillna(False)

def _book_returns_for_overlay(px, W):
    """Cheap causal proxy for the book's own daily return, used by the path-dependent
    overlays (DDCTL, VOLTGT).  Uses the PREVIOUS day's weights, so it is causal."""
    rets = px.pct_change().fillna(0.0)
    return (W.shift(1).fillna(0.0) * rets).sum(axis=1)

def apply_overlay(px, W, fam, lev):
    if fam == "NONE":
        return W
    if fam == "GATE":
        on = _spy_ma_flag(px).shift(1).fillna(False)          # causal
        mult = pd.Series(np.where(on, 1.0, lev), index=W.index)
        return W.mul(mult, axis=0)
    if fam == "DDCTL":
        r = _book_returns_for_overlay(px, W)
        eq = (1 + r).cumprod(); dd = eq / eq.cummax() - 1
        on = (dd.shift(1) < -lev).fillna(False)               # causal: yesterday's drawdown
        return W.mul(pd.Series(np.where(on, 0.5, 1.0), index=W.index), axis=0)
    if fam == "BUDGET":
        req = W.diff().abs().sum(axis=1)                      # required turnover at each date
        thr = req.expanding(min_periods=252).quantile(1 - lev).shift(1)
        fire = (req >= thr).fillna(True).values               # causal expanding threshold
        Wb = W.where(pd.DataFrame(np.repeat(fire[:, None], W.shape[1], axis=1),
                                  index=W.index, columns=W.columns)).ffill().fillna(0.0)
        return Wb
    if fam == "STOP":
        hi = px.rolling(63).max()
        hit = (px < hi * (1 - lev)).astype(float)
        blocked = hit.rolling(21, min_periods=1).max().shift(1).fillna(0.0) > 0.5
        blocked = blocked.reindex(columns=W.columns).fillna(False)
        return W.where(~blocked, 0.0)
    if fam == "VOLTGT":
        r = _book_returns_for_overlay(px, W)
        rv = r.rolling(20).std() * np.sqrt(252)
        mult = (lev / rv.replace(0, np.nan)).clip(upper=1.0).shift(1).fillna(1.0)
        return W.mul(mult, axis=0)
    if fam == "LAM":
        return W.ewm(alpha=lev, adjust=False).mean()          # partial rebalance
    raise ValueError(fam)


# ================================================================== evaluation
def bars(r, spy, v2):
    """PROTOCOL 4a and 4b for one return series, on the common (post-warm-up) sample."""
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    sm, sm1, sm2 = metrics(spy), metrics(spy.iloc[:h]), metrics(spy.iloc[h:])
    vm, vm1, vm2 = metrics(v2), metrics(v2.iloc[:h]), metrics(v2.iloc[h:])
    oos = r.loc[IS_END + pd.Timedelta(days=1):]
    ins = r.loc[:IS_END]
    so = metrics(spy.loc[IS_END + pd.Timedelta(days=1):])
    mo, mi = metrics(oos), metrics(ins)
    d = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"], H2=m2["Sharpe"],
             IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"],
             OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"])
    # 4b margins (positive = clears)
    d["m_H1"] = m1["Sharpe"] - sm1["Sharpe"]
    d["m_H2"] = m2["Sharpe"] - sm2["Sharpe"]
    d["m_OOS"] = mo["Sharpe"] - so["Sharpe"]
    d["m_DD"] = 0.60 * abs(sm["MaxDD"]) - abs(m["MaxDD"])
    d["m_CAGR"] = m["CAGR"] - 0.70 * sm["CAGR"]
    marg = {"H1": d["m_H1"], "H2": d["m_H2"], "OOS": d["m_OOS"], "DD": d["m_DD"], "CAGR": d["m_CAGR"]}
    d["m_min"] = min(marg.values()); d["m_bind"] = min(marg, key=marg.get)
    d["pass4b"] = bool(d["m_min"] > 0)
    d["pass4a"] = bool(m1["Sharpe"] > vm1["Sharpe"] and m2["Sharpe"] > vm2["Sharpe"]
                       and m["MaxDD"] >= vm["MaxDD"])
    d["both"] = bool(d["pass4b"] and d["pass4a"])
    return d


# ======================================================================= LEG B
def leg_b():
    P("=" * 100)
    P("LEG B — FRESH OVERLAY CORPUS (the untreated carrier exists by construction)")
    P("=" * 100)
    rows = []
    t0 = time.time()
    for pname, px in panels().items():
        spy_is_bench = (pname == "small439")      # SPY is a benchmark, not a constituent, on small
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        # RULES v2 comparand: on the small panel SPY is a benchmark, so the live book is run on
        # the SPY-free sub-panel there; on u56/broad SPY is a genuine constituent and stays in.
        pv2 = px.drop(columns=["SPY"]) if spy_is_bench else px
        W2 = rules_v2_weights(pv2).reindex(columns=px.columns).fillna(0.0)
        v2 = backtest(px, W2, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        P(f"\n--- panel {pname}: {px.shape[1]} cols, {px.index[0].date()} -> {px.index[-1].date()}"
          f" | SPY {metrics(spy)['CAGR']:.2%}/{metrics(spy)['Sharpe']:.4f}/{metrics(spy)['MaxDD']:.2%}"
          f" | RULES v2 {metrics(v2)['CAGR']:.2%}/{metrics(v2)['Sharpe']:.4f}/{metrics(v2)['MaxDD']:.2%}")
        for book in BOOKS:
            for g in GROSSES:
                W0 = carrier_weights(px, book, g, spy_is_bench)
                arms = [("NONE", np.nan)] + [(f, lv) for f in FAMILIES for lv in FAMILIES[f]]
                for fam, lev in arms:
                    W = apply_overlay(px, W0, fam, lev).reindex(columns=px.columns).fillna(0.0)
                    res = backtest(px, W, cost_bps=COST_BPS, freq=FREQ)
                    r = res["returns"].loc[start:]
                    d = bars(r, spy, v2)
                    d.update(panel=pname, book=book, gross=g, family=fam, level=lev,
                             is_carrier=(fam == "NONE"),
                             turnover=res["turnover"].loc[start:].sum() / (len(r) / 252),
                             mean_gross=res["weights"].loc[start:].sum(axis=1).mean())
                    rows.append(d)
                P(f"    {book:6s} g={g:.2f}  carrier 4b={rows[-13]['pass4b']}"
                  f"  overlay 4b passes={sum(x['pass4b'] for x in rows[-12:])}/12"
                  f"  ({time.time()-t0:.0f}s)")
    df = pd.DataFrame(rows)
    cols = ["panel", "book", "gross", "family", "level", "is_carrier", "CAGR", "Sharpe", "MaxDD",
            "H1", "H2", "IS_Sharpe", "IS_CAGR", "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD",
            "turnover", "mean_gross", "m_H1", "m_H2", "m_OOS", "m_DD", "m_CAGR", "m_min",
            "m_bind", "pass4b", "pass4a", "both"]
    df = df[cols]
    df.to_csv(OUT / f"{STAMP}.arms.csv", index=False)
    return df


def conditional_table(df):
    """The idea's headline: overlay 4b passes split by whether their own carrier passes."""
    car = df[df.is_carrier].set_index(["panel", "book", "gross"])
    ov = df[~df.is_carrier].copy()
    keys = list(zip(ov.panel, ov.book, ov.gross))
    for src, dst in [("pass4b", "carrier4b"), ("pass4a", "carrier4a"), ("m_bind", "carrier_bind"),
                     ("mean_gross", "carrier_gross"), ("Sharpe", "carrier_Sharpe"),
                     ("OOS_Sharpe", "carrier_OOS_Sharpe"), ("MaxDD", "carrier_MaxDD")]:
        ov[dst] = [car.loc[k, src] for k in keys]
    return ov


# ======================================================================= LEG C
def leg_c(df):
    """MATCHED-GROSS CONTROL.  An overlay that only de-grosses moves the 4b DD bar without
    doing anything an exposure dial could not.  For every overlay arm, scale the UNTREATED
    carrier by k = mean_gross(arm) / mean_gross(carrier) and price that.  An overlay 4b pass
    whose matched-gross carrier ALSO passes 4b is a gross placement, not an instrument."""
    P("\n" + "=" * 100)
    P("LEG C — MATCHED-GROSS CONTROL for every overlay arm (288 extra backtests)")
    P("=" * 100)
    out = []
    for pname, px in panels().items():
        spy_is_bench = (pname == "small439")
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        pv2 = px.drop(columns=["SPY"]) if spy_is_bench else px
        W2 = rules_v2_weights(pv2).reindex(columns=px.columns).fillna(0.0)
        v2 = backtest(px, W2, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        sub = df[df.panel == pname]
        for book in BOOKS:
            for g in GROSSES:
                W0 = carrier_weights(px, book, g, spy_is_bench).reindex(columns=px.columns).fillna(0.0)
                cg = sub[(sub.book == book) & (sub.gross == g) & sub.is_carrier].iloc[0].mean_gross
                arms = sub[(sub.book == book) & (sub.gross == g) & (~sub.is_carrier)]
                for _, a in arms.iterrows():
                    k = a.mean_gross / cg if cg > 0 else 1.0
                    res = backtest(px, W0 * k, cost_bps=COST_BPS, freq=FREQ)
                    r = res["returns"].loc[start:]
                    d = bars(r, spy, v2)
                    d.update(panel=pname, book=book, gross=g, family=a.family, level=a.level,
                             k=k, ctl_mean_gross=res["weights"].loc[start:].sum(axis=1).mean(),
                             arm_pass4b=bool(a.pass4b), arm_Sharpe=a.Sharpe,
                             arm_OOS_Sharpe=a.OOS_Sharpe)
                    out.append(d)
    cc = pd.DataFrame(out)
    cc = cc.rename(columns={c: f"ctl_{c}" for c in
                            ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "IS_CAGR",
                             "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "m_H1", "m_H2", "m_OOS",
                             "m_DD", "m_CAGR", "m_min", "m_bind", "pass4b", "pass4a", "both"]})
    cc.to_csv(OUT / f"{STAMP}.matched.csv", index=False)
    return cc


# ======================================================================= LEG A
PASS4B_PAT = re.compile(r"^(pass_?4b|p4b)$", re.I)
PASS4A_PAT = re.compile(r"^(pass_?4a(_v2)?|p4a)$", re.I)
DIAL_COLS = ["overlay", "family", "fam", "arm", "kind", "instrument", "instr", "mode",
             "clause", "treatment", "variant", "gate", "rule", "form", "type"]
OFF_PAT = re.compile(r"^(none|off|no|nooverlay|no_overlay|base|basebook|base_book|control|ctl|"
                     r"ctrl|untreated|raw|do_?nothing|donothing|anchor|incumbent|plain|"
                     r"unfiltered|nofilter|no_filter|s0|null_?arm)$", re.I)
CARRIER_KEYS = ["panel", "universe", "uni", "book", "base", "basebook", "base_book", "corpus",
                "grid", "cost", "cost_bps", "bps", "cad", "cadence", "freq", "gross", "g",
                "n", "conv", "seed", "depth", "rung"]

def leg_a():
    P("\n" + "=" * 100)
    P("LEG A — CENSUS of every committed CSV that carries a 4b column")
    P("=" * 100)
    files = sorted(glob.glob(str(OUT / "*.csv")))
    fstat, cens = [], []
    for f in files:
        name = Path(f).name
        if name.startswith(STAMP):
            continue
        try:
            df = pd.read_csv(f)
        except Exception as e:
            fstat.append(dict(file=name, status="unreadable", reason=type(e).__name__, rows=0)); continue
        c4b = [c for c in df.columns if PASS4B_PAT.match(str(c))]
        if not c4b:
            fstat.append(dict(file=name, status="drop", reason="no 4b pass column", rows=len(df))); continue
        c4b = c4b[0]
        vals = df[c4b]
        if vals.dtype == object:
            vals = vals.astype(str).str.strip().str.lower().map(
                {"true": True, "false": False, "1": True, "0": False, "yes": True, "no": False})
        try:
            p4b = vals.astype(float) > 0.5
        except Exception:
            fstat.append(dict(file=name, status="drop", reason="4b column not boolean", rows=len(df))); continue
        # find a dial column that carries an explicit OFF level
        dial = None
        for c in df.columns:
            if str(c).lower() not in DIAL_COLS:
                continue
            u = df[c].astype(str).str.strip().fillna("")
            if u.map(lambda x: bool(OFF_PAT.match(str(x)))).any() and u.nunique() > 1:
                dial = c; break
        if dial is None:
            fstat.append(dict(file=name, status="drop", reason="no dial with an explicit OFF level",
                              rows=len(df), n4b=int(p4b.sum()))); continue
        keys = [c for c in df.columns if str(c).lower() in CARRIER_KEYS and c != dial
                and df[c].nunique() <= max(40, len(df) // 2)]
        off = df[dial].astype(str).str.strip().fillna("").map(lambda x: bool(OFF_PAT.match(str(x))))
        # pair each treated row with the OFF row of its own carrier group
        gk = keys if keys else None
        n_car = n_inc = n_dest = n_bf = n_unpaired = 0
        if gk:
            grouped = df.assign(_p4b=p4b, _off=off).groupby(gk, dropna=False)
        else:
            grouped = [((), df.assign(_p4b=p4b, _off=off))]
        for _, gdf in (grouped if gk is None else grouped):
            ctl = gdf[gdf._off]
            trt = gdf[~gdf._off]
            if len(ctl) == 0 or len(trt) == 0:
                n_unpaired += len(trt); continue
            cpass = bool(ctl._p4b.any())          # carrier passes if ANY of its OFF rows passes
            for _, rr in trt.iterrows():
                if rr._p4b and cpass: n_car += 1
                elif rr._p4b and not cpass: n_inc += 1
                elif (not rr._p4b) and cpass: n_dest += 1
                else: n_bf += 1
        tot_pass = n_car + n_inc
        cens.append(dict(file=name, rows=len(df), dial=dial, keys="|".join(map(str, keys)),
                         n_treated=n_car + n_inc + n_dest + n_bf, n_unpaired=n_unpaired,
                         carried=n_car, incremental=n_inc, destroyed=n_dest, both_fail=n_bf,
                         overlay_pass4b=tot_pass,
                         incr_share=(n_inc / tot_pass) if tot_pass else np.nan))
        fstat.append(dict(file=name, status="census", reason="", rows=len(df), n4b=int(p4b.sum())))
    fs = pd.DataFrame(fstat); cs = pd.DataFrame(cens)
    fs.to_csv(OUT / f"{STAMP}.censusfiles.csv", index=False)
    cs.to_csv(OUT / f"{STAMP}.census.csv", index=False)
    P(f"files scanned            : {len(fs)}")
    P(f"  with a 4b pass column  : {int((fs.status != 'drop').sum() + (fs.reason == 'no dial with an explicit OFF level').sum() + (fs.reason == '4b column not boolean').sum()) - int((fs.status=='unreadable').sum())}")
    for reason, k in fs[fs.status == "drop"].reason.value_counts().items():
        P(f"  dropped: {reason:45s} {k}")
    P(f"  QUALIFYING overlay-style files (an explicit OFF level present): {len(cs)}")
    if len(cs):
        tot = cs[["carried", "incremental", "destroyed", "both_fail", "n_unpaired"]].sum()
        tp = int(tot.carried + tot.incremental)
        P(f"  treated rows paired    : {int(tot[['carried','incremental','destroyed','both_fail']].sum())}"
          f"  (unpaired, no OFF row in their carrier group: {int(tot.n_unpaired)})")
        P(f"  CARRIED     (arm 4b, carrier 4b too) : {int(tot.carried)}")
        P(f"  INCREMENTAL (arm 4b, carrier fails)  : {int(tot.incremental)}")
        P(f"  DESTROYED   (carrier 4b, arm fails)  : {int(tot.destroyed)}")
        P(f"  BOTH FAIL                            : {int(tot.both_fail)}")
        P(f"  >>> archival INCREMENTAL share of overlay 4b passes: "
          f"{(tot.incremental/tp if tp else float('nan')):.4f}  ({int(tot.incremental)}/{tp})")
    return fs, cs


# ======================================================================= rule 8
def rule8(df):
    P("\n" + "=" * 100)
    P("RULE 8 WALK-FORWARD — level chosen on IS (<= 2016-12-31) by IS Sharpe, 2017-2026 read once")
    P("=" * 100)
    out = []
    for (pn, bk, g, fam), gdf in df[~df.is_carrier].groupby(["panel", "book", "gross", "family"]):
        car = df[(df.panel == pn) & (df.book == bk) & (df.gross == g) & df.is_carrier].iloc[0]
        pick = gdf.loc[gdf.IS_Sharpe.idxmax()]
        orac = gdf.loc[gdf.OOS_Sharpe.idxmax()]
        out.append(dict(panel=pn, book=bk, gross=g, family=fam,
                        pick_level=pick.level, pick_OOS_Sharpe=pick.OOS_Sharpe,
                        pick_OOS_CAGR=pick.OOS_CAGR, pick_OOS_MaxDD=pick.OOS_MaxDD,
                        carrier_OOS_Sharpe=car.OOS_Sharpe, carrier_OOS_CAGR=car.OOS_CAGR,
                        carrier_OOS_MaxDD=car.OOS_MaxDD,
                        oracle_OOS_Sharpe=orac.OOS_Sharpe,
                        d_vs_carrier=pick.OOS_Sharpe - car.OOS_Sharpe,
                        oracle_headroom=orac.OOS_Sharpe - car.OOS_Sharpe,
                        pick_pass4b=bool(pick.pass4b), carrier_pass4b=bool(car.pass4b),
                        pick_pass4a=bool(pick.pass4a), carrier_pass4a=bool(car.pass4a)))
    wf = pd.DataFrame(out)
    wf.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    n = len(wf); w = int((wf.d_vs_carrier > 0).sum())
    sd = wf.d_vs_carrier.std(ddof=1); mn = wf.d_vs_carrier.mean()
    t = mn / (sd / np.sqrt(n)) if sd else np.nan
    P(f"cells (panel x book x gross x family) : {n}")
    P(f"IS-chooser mean dOOS_Sharpe vs the UNTREATED CARRIER : {mn:+.4f}  (t {t:+.2f}, wins {w}/{n})")
    P(f"ORACLE-OOS mean headroom over the carrier            : {wf.oracle_headroom.mean():+.4f}"
      f"  (positive cells {int((wf.oracle_headroom>0).sum())}/{n})")
    P(f"IS-chosen arm passes 4b in {int(wf.pick_pass4b.sum())}/{n} cells; its carrier passes in "
      f"{int(wf.carrier_pass4b.sum())}/{n}")
    inc = int(((wf.pick_pass4b) & (~wf.carrier_pass4b)).sum())
    P(f"  of the chooser's 4b passes, INCREMENTAL (carrier fails): {inc}/{int(wf.pick_pass4b.sum())}")
    P("\nper family:")
    P(wf.groupby("family").agg(cells=("d_vs_carrier", "size"), mean_dOOS=("d_vs_carrier", "mean"),
                               wins=("d_vs_carrier", lambda s: int((s > 0).sum())),
                               mean_headroom=("oracle_headroom", "mean")).to_string(
        float_format=lambda x: f"{x:+.4f}"))
    P("\nper panel:")
    P(wf.groupby("panel").agg(cells=("d_vs_carrier", "size"), mean_dOOS=("d_vs_carrier", "mean"),
                              wins=("d_vs_carrier", lambda s: int((s > 0).sum())),
                              mean_headroom=("oracle_headroom", "mean")).to_string(
        float_format=lambda x: f"{x:+.4f}"))
    return wf


# ========================================================================= main
def main():
    t0 = time.time()
    df = leg_b()

    P("\n" + "=" * 100)
    P("ALL GRID POINTS — LEG B (312 arms; full table in .arms.csv)")
    P("=" * 100)
    P(df.to_string(index=False, float_format=lambda x: f"{x:.4f}", max_colwidth=12))

    ov = conditional_table(df)
    ov.to_csv(OUT / f"{STAMP}.cells.csv", index=False)

    P("\n" + "=" * 100)
    P("HEADLINE — the conditional 4b table (LEG B, 288 overlay arms on 24 carriers)")
    P("=" * 100)
    car = df[df.is_carrier]
    P(f"carriers passing 4b untreated : {int(car.pass4b.sum())}/{len(car)}")
    P(f"carriers passing 4a untreated : {int(car.pass4a.sum())}/{len(car)}")
    n_car = int(((ov.pass4b) & (ov.carrier4b)).sum())
    n_inc = int(((ov.pass4b) & (~ov.carrier4b)).sum())
    n_des = int(((~ov.pass4b) & (ov.carrier4b)).sum())
    n_bf = int(((~ov.pass4b) & (~ov.carrier4b)).sum())
    tp = n_car + n_inc
    P(f"overlay arms passing 4b       : {tp}/{len(ov)}")
    P(f"  CARRIED     (carrier passes too) : {n_car}")
    P(f"  INCREMENTAL (carrier fails)      : {n_inc}")
    P(f"  DESTROYED   (carrier passes, arm fails) : {n_des}")
    P(f"  BOTH FAIL                        : {n_bf}")
    P(f">>> INCREMENTAL SHARE of overlay 4b passes = {n_inc}/{tp} = "
      f"{(n_inc/tp if tp else float('nan')):.4f}")
    P(f">>> net 4b passes created by the overlay corpus = {n_inc} - {n_des} = {n_inc - n_des}")
    # same for 4a
    a_car = int(((ov.pass4a) & (ov.carrier4a)).sum()); a_inc = int(((ov.pass4a) & (~ov.carrier4a)).sum())
    a_des = int(((~ov.pass4a) & (ov.carrier4a)).sum())
    P(f"4a: carried {a_car}, incremental {a_inc}, destroyed {a_des}"
      f"  -> incremental share {(a_inc/(a_car+a_inc) if (a_car+a_inc) else float('nan')):.4f}")

    P("\nby carrier (panel x book x gross): carrier 4b, then overlay 4b passes out of 12")
    tab = ov.groupby(["panel", "book", "gross"]).agg(
        carrier4b=("carrier4b", "first"), carrier4a=("carrier4a", "first"),
        arms=("pass4b", "size"), arm4b=("pass4b", "sum"), arm4a=("pass4a", "sum"))
    P(tab.to_string())
    tab.to_csv(OUT / f"{STAMP}.keeppaths.csv")

    P("\nby family (pooled over 24 carriers):")
    fam = ov.assign(inc=(ov.pass4b & ~ov.carrier4b), carr=(ov.pass4b & ov.carrier4b),
                    dest=(~ov.pass4b & ov.carrier4b)).groupby("family").agg(
        arms=("pass4b", "size"), pass4b=("pass4b", "sum"), carried=("carr", "sum"),
        incremental=("inc", "sum"), destroyed=("dest", "sum"))
    P(fam.to_string())

    P("\nby panel:")
    pan = ov.assign(inc=(ov.pass4b & ~ov.carrier4b), carr=(ov.pass4b & ov.carrier4b),
                    dest=(~ov.pass4b & ov.carrier4b)).groupby("panel").agg(
        arms=("pass4b", "size"), pass4b=("pass4b", "sum"), carried=("carr", "sum"),
        incremental=("inc", "sum"), destroyed=("dest", "sum"))
    P(pan.to_string())

    P("\nbinding bar for the arms that FAIL 4b:")
    P(ov[~ov.pass4b].m_bind.value_counts().to_string())

    # ---------------------------------------------------------- LEG C: is it just de-grossing?
    cc = leg_c(df)
    key = ["panel", "book", "gross", "family", "level"]
    j = ov.merge(cc[key + ["k", "ctl_mean_gross", "ctl_Sharpe", "ctl_OOS_Sharpe", "ctl_MaxDD",
                           "ctl_m_min", "ctl_m_bind", "ctl_pass4b", "ctl_pass4a"]], on=key, how="left")
    j.to_csv(OUT / f"{STAMP}.cells.csv", index=False)
    P("\n" + "=" * 100)
    P("HEADLINE 2 — do the INCREMENTAL 4b passes survive a MATCHED-GROSS carrier control?")
    P("=" * 100)
    inc = j[j.pass4b & ~j.carrier4b]
    P(f"incremental overlay 4b passes                      : {len(inc)}")
    P(f"  arm mean gross < carrier mean gross              : "
      f"{int((inc.mean_gross < inc.carrier_gross).sum())}/{len(inc)}   (k in "
      f"[{inc.k.min():.3f}, {inc.k.max():.3f}])")
    P(f"  carrier's own binding bar on those cells         : "
      f"{inc.carrier_bind.value_counts().to_dict()}")
    gexp = int(inc.ctl_pass4b.fillna(False).sum())
    P(f"  MATCHED-GROSS carrier control ALSO passes 4b     : {gexp}/{len(inc)}"
      f"   <- these are GROSS PLACEMENTS, not instrument results")
    P(f"  >>> 4b passes attributable to the OVERLAY ITSELF : {len(inc) - gexp}/{len(inc)}")
    P(f"  mean dSharpe(arm - matched-gross control)        : {(inc.Sharpe - inc.ctl_Sharpe).mean():+.4f}")
    P(f"  mean dOOS  (arm - matched-gross control)         : {(inc.OOS_Sharpe - inc.ctl_OOS_Sharpe).mean():+.4f}")
    allov = j
    P(f"\nover ALL 288 overlay arms: arm beats its matched-gross control on Sharpe in "
      f"{int((allov.Sharpe > allov.ctl_Sharpe).sum())}/{len(allov)}; on OOS Sharpe in "
      f"{int((allov.OOS_Sharpe > allov.ctl_OOS_Sharpe).sum())}/{len(allov)}")
    P(f"  mean dSharpe {(allov.Sharpe - allov.ctl_Sharpe).mean():+.4f}, "
      f"mean dOOS {(allov.OOS_Sharpe - allov.ctl_OOS_Sharpe).mean():+.4f}")
    P(f"  matched-gross controls passing 4b: {int(allov.ctl_pass4b.fillna(False).sum())}/{len(allov)}"
      f" vs overlay arms {int(allov.pass4b.sum())}/{len(allov)}")
    P("\nper family, arm vs its own matched-gross control:")
    P(allov.assign(dS=allov.Sharpe - allov.ctl_Sharpe, dO=allov.OOS_Sharpe - allov.ctl_OOS_Sharpe)
      .groupby("family").agg(arms=("dS", "size"), mean_dSharpe=("dS", "mean"),
                             wins=("dS", lambda s: int((s > 0).sum())),
                             mean_dOOS=("dO", "mean"),
                             arm4b=("pass4b", "sum"), ctl4b=("ctl_pass4b", "sum")).to_string(
        float_format=lambda x: f"{x:+.4f}"))

    wf = rule8(df)
    fs, cs = leg_a()

    P(f"\ntotal runtime {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
