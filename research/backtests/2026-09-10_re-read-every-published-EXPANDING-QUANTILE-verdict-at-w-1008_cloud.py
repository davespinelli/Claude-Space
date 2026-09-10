#!/usr/bin/env python3
"""Idea 601 - "re-read-every-published-EXPANDING-QUANTILE-verdict-at-w-1008" (cloud lane).

What this run exists to settle
------------------------------
Idea 399 measured, on BREADTH only, that a CAUSAL EXPANDING quantile fires at 0.00-0.31 of its
nominal q while a trailing w=1008 window lands 0.85-1.03 on all nine panel x q cells, and that
idea 336's nominal q=0.07 arm is INERT (fires ~0 days) rather than negative.  The queue's
follow-up is a re-read of the RECORD: census every committed result that used a causal expanding
quantile as its instrument, and re-price the ones whose verdict rests on a sub-nominal-firing arm.

Two things idea 399 did NOT establish and this run must:
    (a) whether the deficit is a BREADTH fact or an ESTIMATOR fact - i.e. whether it also holds
        on the record's other quantile-gated series (realised vol, cross-sectional dispersion,
        drawdown speed), and
    (b) whether it holds in the HIGH tail.  Every series above is gated LOW in the record except
        vol/dispersion, which are gated HIGH (`x >= expanding.quantile(0.80)`).  An expanding
        estimator anchored by 2008-2011 is anchored LOW for breadth and HIGH for vol, so the two
        tails are separate claims and the record contains both.

Questions, stated so they can be answered either way
----------------------------------------------------
    Q1 (CENSUS)     How many committed files use a causal expanding quantile as an instrument,
                    which series and which tail, and how many of them are verdict-bearing?
    Q2 (DEFICIT)    Is realised/nominal < 1 an estimator property across all four series and BOTH
                    tails, or only breadth-low?  Reported per panel x series x tail x q.
    Q3 (REPAIR)     Does w=1008 restore level fidelity everywhere idea 399 found it does on
                    breadth, and what does each w cost in armed sample?
    Q4 (RE-READ)    Re-priced at w=1008, does any gated book's verdict MOVE - 4a against the live
                    RULES v2 book, 4b against SPY, and the rule-8 (choose on the first half,
                    evaluate on the untouched second half) pick?  A verdict that does not move is
                    the useful answer here: it means the record's quantile-gated KILLs stand.

Tuned parameters (PROTOCOL rule 4: at most two) - the queue names both
    1. w    trailing window in trading days, in {252, 504, 1008, 2016}
    2. tau  INERTNESS BAR: realised firing rate below which an arm's verdict is called
            "resting on an inert arm", in {0.005, 0.010, 0.020, 0.050}
    16 grid points, ALL reported (section [5]).

Reported axes, never tuned or selected on
    panel    U56 / B136 / SMALL439
    series   BREADTH (low tail) / RVOL (high) / DISP (high) / DDSPD (high)
    q        the record's OWN union of published levels, per tail (section [1] derives it)
    base     EWALL(0.75) and CAND20(1.00), the latter being the 2026-09-04 KEEP 4b family
    depth    0.50 (the record's middle cut; never searched)
    cost     0 / 10 / 25 bps, 10 = PROTOCOL rule 2

Instruments, all on the SAME base book and the SAME days
    QEXP        causal expanding quantile, min_periods=252 - the record's instrument
    QROLL(w)    trailing-w quantile, computed through t only, executed t+1 - idea 399's repair
    Unarmed days (fewer than the window's observations) are gate OFF = fully invested, which is
    what every committed file does; the armed share is reported for every w.

Reproduction gates, printed before any new number is read (section [0])
    G1  derived cost rung r(c) = r(0) - turnover*c/1e4 vs a live engine.backtest(c).
    G2  idea 399's headline: QROLL w=1008 realised/nominal in 0.85-1.03 on all nine
        panel x q breadth cells, QEXP median 0.207, QROLL median 0.884.
    G3  U56/RULES v1 = 6.4194% / 0.66110 / -13.8278% (idea 486's published triple).  Vintage-
        sensitive by idea 328/514; the drift is reported, not hidden.
    G4  rate identity on a stationary tie-free control (the equidistributed sequence
        frac(t*phi), uniform on [0,1)): a trailing-w quantile gate fires at its nominal rate
        (q low tail, 1-q high tail) to within 1/w + 0.02, in BOTH tails.

Data: committed caches only, no network.  SURVIVORSHIP: all three panels are current-constituent
lists, so CAGR/drawdown LEVELS are optimistic; the QEXP-vs-QROLL CONTRAST on one fixed base book
is the durable part.  SMALL439 drops the max_1d_move >= 1.0 names and starts 2010, so w=2016
costs it half its sample in warm-up.

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v1_weights, rules_v2_weights
from engine import backtest, metrics, rebalance_mask

SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"

FREQ = "W"
MAX_VOL = 0.60
DEPTH = 0.50
MINQ = 252
WS = [252, 504, 1008, 2016]                 # tuned param 1
TAUS = [0.005, 0.010, 0.020, 0.050]         # tuned param 2
RUNGS = [0, 10, 25]
RUNG_HEAD = 10
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
NTOP = 20

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 3000)

LINES = []
MULTS = {}
BASES = {}


def log(s=""):
    print(s)
    LINES.append(str(s))


# ------------------------------------------------------------------ [1] census
CENSUS_RE = re.compile(r"expanding\s*\(")


def census():
    """Every committed .py under research/ carrying a causal expanding-quantile site."""
    rows = []
    for f in sorted((REPO / "research").rglob("*.py")):
        txt = f.read_text(errors="replace")
        lines = txt.split("\n")
        sites = []
        for i, ln in enumerate(lines):
            if "expanding(" not in ln:
                continue
            ctx = ln
            if "quantile" not in ctx and i + 1 < len(lines):
                ctx = ln + " " + lines[i + 1]
            if "quantile" not in ctx:
                continue
            sites.append((i + 1, ctx.strip()))
        if not sites:
            continue
        low = txt.lower()
        rows.append(dict(
            file=f.name, sites=len(sites),
            verdict_bearing=any(t in txt for t in ("KEEP", "KILL", "PARK", "4a", "4b")),
            has_4b="4b" in txt or "pass4b" in low,
            ctx="; ".join(c for _, c in sites)))
    return pd.DataFrame(rows)


SERIES_WORDS = {
    "BREADTH": ("br", "breadth", "e_full", "narrow"),
    "RVOL": ("vol", "rv", "v.", "vtest", "t63"),
    "DISP": ("disp",),
    "DDSPD": ("ddsp", "speed", "req"),
}


def classify(ctx):
    c = ctx.lower()
    if "disp" in c:
        return "DISP"
    if "speed" in c or "ddsp" in c or "req" in c:
        return "DDSPD"
    if re.search(r"\b(vol|rv|vtest|t63|v)\b\s*\.\s*expanding", c) or "vol.expanding" in c \
       or "rv.expanding" in c or "v.expanding" in c or "vtest" in c or "t63" in c:
        return "RVOL"
    if "br" in c or "e.expanding" in c or "e_full" in c or "s.expanding" in c:
        return "BREADTH"
    return "OTHER"


# ------------------------------------------------------------------ primitives
def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def ewall_weights(px, gross=0.75):
    e = eligible_mask(px).astype(float)
    n = e.sum(axis=1).replace(0, np.nan)
    return e.div(n, axis=0).mul(gross).fillna(0.0)


def cand20_weights(px, n=NTOP, gross=1.00):
    """The 2026-09-04 KEEP 4b family: top-n on the composite, NO vol scaler, equal weight."""
    s, above, vol20 = score(px, vol_scale=False)
    elig = s.where(above & (vol20 < MAX_VOL))
    rank = elig.rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(k, axis=0).mul(gross).fillna(0.0)


def state_series(px, cols):
    """The record's four quantile-gated state series, on the panel's own constituents.

    BREADTH  share of priced names above their own 200d MA           (gated LOW)
    RVOL     20d realised vol of the equal-weight panel return       (gated HIGH)
    DISP     cross-sectional sd of 20d name returns                  (gated HIGH)
    DDSPD    21d fall in the equal-weight panel's drawdown           (gated HIGH)
    """
    p = px[cols]
    above = p > p.rolling(200).mean()
    br = above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)
    rets = p.pct_change()
    ew = rets.mean(axis=1)
    rvol = ew.rolling(20).std() * np.sqrt(252)
    disp = rets.rolling(20).sum().std(axis=1)
    eq = (1 + ew.fillna(0)).cumprod()
    dd = eq / eq.cummax() - 1
    ddspd = -(dd - dd.shift(21))
    return {"BREADTH": br, "RVOL": rvol, "DISP": disp, "DDSPD": ddspd}


TAIL = {"BREADTH": "LOW", "RVOL": "HIGH", "DISP": "HIGH", "DDSPD": "HIGH"}
QS_LOW = [0.07, 0.10, 0.12, 0.17, 0.20, 0.30, 0.40]      # the record's own low-tail levels
QS_HIGH = [0.60, 0.70, 0.80, 0.90]                        # the record's own high-tail levels


def nominal(q, tail):
    """The rate the instrument CLAIMS to fire at: q in the low tail, 1-q in the high tail."""
    return q if tail == "LOW" else 1.0 - q


def thr_exp(s, q):
    return s.expanding(min_periods=MINQ).quantile(q)


def thr_roll(s, q, w):
    return s.rolling(w, min_periods=w).quantile(q)


def fire(s, thr, tail):
    """Gate armed and firing at t.  Information through t only; execution is t+1 (apply_gate)."""
    ok = s.notna() & thr.notna()
    f = (s < thr) if tail == "LOW" else (s >= thr)
    return (f & ok), ok


def mult_from_fire(f, idx, cadence="W"):
    m = pd.Series(1.0, index=idx).where(~f.reindex(idx).fillna(False), 1.0 - DEPTH)
    mask = rebalance_mask(idx, FREQ)
    return m.where(mask).ffill().fillna(1.0) if cadence == "W" else m


def apply_gate(r_base, t_base, mult, gross, cost_bps):
    m_eff = mult.reindex(r_base.index).shift(1).fillna(1.0)
    switch = m_eff.diff().abs().fillna(0.0)
    return m_eff * (r_base - t_base * cost_bps / 1e4) - switch * gross * cost_bps / 1e4


def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def summarise(r, spy_pack, base_pack):
    m = metrics(r)
    h1, h2 = half_sharpes(r)
    m_oos = metrics(r.loc[OOS_START:])
    s1, s2, s_oos, s_dd, s_cagr = spy_pack
    t = {"H1": h1 > s1, "H2": h2 > s2, "OOS": m_oos["Sharpe"] > s_oos,
         "DD": abs(m["MaxDD"]) <= 0.60 * abs(s_dd), "CAGR": m["CAGR"] >= 0.70 * s_cagr}
    b1, b2, bdd = base_pack
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"], OOS_CAGR=m_oos["CAGR"],
                OOS_Sharpe=m_oos["Sharpe"], OOS_MaxDD=m_oos["MaxDD"],
                p4a=bool(h1 > b1 and h2 > b2 and m["MaxDD"] >= bdd), p4b=all(t.values()),
                fail4b=",".join(k for k, v in t.items() if not v) or "-")


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad)


# ------------------------------------------------------------------ main
def main():
    log("=" * 170)
    log("IDEA 601  re-read-every-published-EXPANDING-QUANTILE-verdict-at-w-1008   (cloud lane)")
    log("=" * 170)

    # ---------------------------------------------------------- [1] census
    log("\n[1] CENSUS - committed .py files using a causal expanding quantile as an instrument")
    cen = census()
    cen["family"] = cen["ctx"].map(classify)
    log(f"  research/**/*.py scanned: {len(list((REPO/'research').rglob('*.py')))}; "
        f"files with >=1 expanding-quantile site: {len(cen)}; total sites: {int(cen['sites'].sum())}")
    log(f"  verdict-bearing (file mentions KEEP/KILL/PARK/4a/4b): {int(cen['verdict_bearing'].sum())}"
        f" of {len(cen)}; carrying a 4b leg: {int(cen['has_4b'].sum())}")
    log(cen[["file", "sites", "family", "verdict_bearing", "has_4b"]].to_string(index=False))
    log("\n  by series family: " + ", ".join(f"{k}={v}" for k, v in cen["family"].value_counts().items()))

    # ---------------------------------------------------------- panels
    u56 = load_universe()
    b136 = load_universe(broad=True)
    small, ndrop = small_panel()
    last = min(u56.index[-1], b136.index[-1], small.index[-1])
    panels = {"U56": u56.loc[:last], "B136": b136.loc[:last], "SMALL439": small.loc[:last]}
    log(f"\n  panels truncated to common last date {last.date()}; SMALL panel dropped {ndrop} "
        f"tickers with max_1d_move >= 1.0 -> {panels['SMALL439'].shape[1]-1} names + SPY")

    # ---------------------------------------------------------- [0] gates
    log("\n[0] REPRODUCTION GATES")
    px = panels["U56"]
    w0 = ewall_weights(px, 0.75)
    r0 = backtest(px, w0, cost_bps=0, freq=FREQ)
    r10 = backtest(px, w0, cost_bps=10, freq=FREQ)
    g1 = float((r0["returns"] - r0["turnover"] * 10 / 1e4 - r10["returns"]).abs().max())
    log(f"  G1 cost-rung identity |derived - engine(10bps)| max = {g1:.3e}  "
        f"{'PASS' if g1 < 1e-12 else 'FAIL'}")

    rv1 = backtest(px, rules_v1_weights(px), cost_bps=10, freq=FREQ)
    st = px.index[260]
    mv1 = metrics(rv1["returns"].loc[st:])
    pub = (0.064194, 0.66110, -0.138278)
    d3 = max(abs(mv1["CAGR"] - pub[0]), abs(mv1["Sharpe"] - pub[1]), abs(mv1["MaxDD"] - pub[2]))
    log(f"  G3 U56/RULES v1 = {mv1['CAGR']:.4%} / {mv1['Sharpe']:.5f} / {mv1['MaxDD']:.4%} vs "
        f"published 6.4194% / 0.66110 / -13.8278%; max|d| = {d3:.3e} "
        f"{'PASS' if d3 < 1e-3 else 'DRIFT (vintage, idea 328/514)'}")

    n = 6000
    # A deterministic, tie-free, stationary control: the equidistributed sequence
    # frac(t * phi) is uniform on [0,1) with no repeated values, so a quantile gate on it
    # has an exactly known firing rate and no tie ambiguity (a discrete sawtooth does not).
    phi = (np.sqrt(5.0) - 1.0) / 2.0
    saw = pd.Series(np.modf(np.arange(1, n + 1) * phi)[0],
                    index=pd.bdate_range("2000-01-03", periods=n))
    g4 = []
    for w in WS:
        for q in (0.10, 0.50, 0.90):
            for tail in ("LOW", "HIGH"):
                th = thr_roll(saw, q, w)
                f, ok = fire(saw, th, tail)
                rate = float(f[ok].mean())
                g4.append(abs(rate - nominal(q, tail)) <= 1.0 / w + 0.02)
    log(f"  G4 sawtooth rate identity |realised - nominal| <= 1/w + 0.02 on {len(g4)} "
        f"(w, q, tail) cells: {'PASS' if all(g4) else 'FAIL'} ({sum(g4)}/{len(g4)})")

    # ---------------------------------------------------------- [2] rates
    log("\n[2] Q2/Q3  REALISED FIRING RATE / NOMINAL q, per panel x series x tail x q x instrument")
    rate_rows = []
    states, evals = {}, {}
    for pname, ppx in panels.items():
        cols = [c for c in ppx.columns if c != "SPY"]
        start = ppx.index[260]
        evals[pname] = start
        ss = state_series(ppx, cols)
        states[pname] = ss
        for sname, s in ss.items():
            tail = TAIL[sname]
            qs = QS_LOW if tail == "LOW" else QS_HIGH
            for q in qs:
                for inst, th in [("QEXP", thr_exp(s, q))] + \
                                [(f"QROLL{w}", thr_roll(s, q, w)) for w in WS]:
                    f, ok = fire(s, th, tail)
                    f, ok = f.loc[start:], ok.loc[start:]
                    armed = float(ok.mean())
                    rate = float(f[ok].mean()) if ok.any() else np.nan
                    rate_rows.append(dict(panel=pname, series=sname, tail=tail, q=q, inst=inst,
                                          nominal=nominal(q, tail), armed=armed, rate=rate,
                                          ratio=rate / nominal(q, tail) if rate == rate
                                          else np.nan))
    rates = pd.DataFrame(rate_rows)
    rates.to_csv(OUT / f"{STEM}.rates.csv", index=False)

    log("\n  ratio = realised/nominal (nominal = q in the LOW tail, 1-q in the HIGH tail), over")
    log("  ARMED eval days only (unarmed days are gate OFF, i.e. fully invested):")
    piv = rates.pivot_table(index=["panel", "series", "q"], columns="inst", values="ratio")
    piv = piv[["QEXP"] + [f"QROLL{w}" for w in WS]]
    log(piv.to_string(float_format=lambda x: f"{x:.3f}"))

    log("\n  median ratio by instrument x series (all panels, all q):")
    log(rates.pivot_table(index="inst", columns="series", values="ratio", aggfunc="median")
        .reindex(["QEXP"] + [f"QROLL{w}" for w in WS])
        .to_string(float_format=lambda x: f"{x:.3f}"))
    log("\n  median ARMED share of eval days by instrument x panel (the cost of a long window):")
    log(rates.pivot_table(index="inst", columns="panel", values="armed", aggfunc="median")
        .reindex(["QEXP"] + [f"QROLL{w}" for w in WS])
        .to_string(float_format=lambda x: f"{x:.3f}"))

    br9 = rates[(rates["series"] == "BREADTH") & (rates["q"].isin([0.07, 0.12, 0.17]))]
    g2a = br9[br9["inst"] == "QROLL1008"]["ratio"]
    g2 = bool(len(g2a) == 9 and g2a.between(0.85, 1.03).all())
    log(f"\n  G2 idea 399 headline re-measured: QROLL1008 breadth 9 cells in [0.85,1.03] -> "
        f"{'PASS' if g2 else 'FAIL'} (min {g2a.min():.3f}, max {g2a.max():.3f}); "
        f"QEXP median {br9[br9['inst']=='QEXP']['ratio'].median():.3f} (published 0.207), "
        f"QROLL median {br9[br9['inst'].str.startswith('QROLL')]['ratio'].median():.3f} "
        f"(published 0.884)")

    # ---------------------------------------------------------- [3] re-price
    log("\n[3] Q4  RE-PRICING every (panel x series x q x instrument) gated book, both base books")
    book_rows = []
    for pname, ppx in panels.items():
        start = evals[pname]
        spy = ppx["SPY"].pct_change().fillna(0).loc[start:]
        ms = metrics(spy)
        s1, s2 = half_sharpes(spy)
        spy_pack = (s1, s2, metrics(spy.loc[OOS_START:])["Sharpe"], ms["MaxDD"], ms["CAGR"])
        log(f"\n  {pname}: SPY {ms['CAGR']:.2%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.2%}; "
            f"halves {s1:.3f}/{s2:.3f}, OOS {spy_pack[2]:.3f}; 4b bars CAGR>={0.70*ms['CAGR']:.2%}, "
            f"MaxDD>={-0.60*abs(ms['MaxDD']):.2%}")

        v2 = backtest(ppx, rules_v2_weights(ppx), cost_bps=0, freq=FREQ)
        v2r, v2t = v2["returns"].loc[start:], v2["turnover"].loc[start:]
        base_packs = {}
        for c in RUNGS:
            rb = v2r - v2t * c / 1e4
            b1, b2 = half_sharpes(rb)
            base_packs[c] = (b1, b2, metrics(rb)["MaxDD"])
        log(f"    RULES v2 (4a comparand) @10bps: {metrics(v2r - v2t*10/1e4)['CAGR']:.2%} / "
            f"{metrics(v2r - v2t*10/1e4)['Sharpe']:.3f} / {base_packs[10][2]:.2%}, "
            f"halves {base_packs[10][0]:.3f}/{base_packs[10][1]:.3f}")

        bases = {}
        MULTS.setdefault(pname, {})
        for bname, wfn, gross in [("EWALL0.75", ewall_weights, 0.75),
                                  ("CAND20", cand20_weights, 1.00)]:
            res = backtest(ppx, wfn(ppx), cost_bps=0, freq=FREQ)
            bases[bname] = (res["returns"].loc[start:], res["turnover"].loc[start:], gross)

        BASES[pname] = {k: (v[0], v[1], v[2]) for k, v in bases.items()}
        for bname, (rb, tb, gross) in bases.items():
            for c in RUNGS:
                d = summarise(rb - tb * c / 1e4, spy_pack, base_packs[c])
                d.update(panel=pname, base=bname, series="-", tail="-", q=np.nan,
                         inst="NOGATE", cost=c, rate=np.nan, ratio=np.nan, mean_mult=1.0)
                book_rows.append(d)
            for sname, s in states[pname].items():
                tail = TAIL[sname]
                for q in (QS_LOW if tail == "LOW" else QS_HIGH):
                    for inst, th in [("QEXP", thr_exp(s, q))] + \
                                    [(f"QROLL{w}", thr_roll(s, q, w)) for w in WS]:
                        f, ok = fire(s, th, tail)
                        m = mult_from_fire(f, rb.index)
                        MULTS[pname][(sname, q, inst)] = m
                        rate = float(f.loc[start:][ok.loc[start:]].mean()) \
                            if ok.loc[start:].any() else np.nan
                        for c in RUNGS:
                            r = apply_gate(rb, tb, m, gross, c)
                            d = summarise(r, spy_pack, base_packs[c])
                            d.update(panel=pname, base=bname, series=sname, tail=tail, q=q,
                                     inst=inst, cost=c, rate=rate, nominal=nominal(q, tail),
                                     ratio=rate / nominal(q, tail) if rate == rate else np.nan,
                                     mean_mult=float(m.mean()))
                            book_rows.append(d)
    books = pd.DataFrame(book_rows)
    books.to_csv(OUT / f"{STEM}.books.csv", index=False)
    log(f"\n  {len(books)} arm-rows written ({len(books[books.inst!='NOGATE'])} gated), "
        f"3 cost rungs, 2 base books, all reported in {STEM}.books.csv")

    head = books[books["cost"] == RUNG_HEAD]
    log("\n  4a / 4b pass counts at 10 bps by instrument (denominator = gated arms):")
    tbl = head[head.inst != "NOGATE"].groupby("inst")[["p4a", "p4b"]].agg(["sum", "count"])
    log(tbl.reindex(["QEXP"] + [f"QROLL{w}" for w in WS]).to_string())
    log("\n  ungated parents at 10 bps (the do-nothing bar):")
    log(head[head.inst == "NOGATE"][["panel", "base", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                     "OOS_Sharpe", "p4a", "p4b", "fail4b"]]
        .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---------------------------------------------------------- [4] verdict moves
    log("\n[4] Q4  DOES ANY VERDICT MOVE?  QEXP -> QROLL1008 on the SAME (panel, base, series, q)")
    key = ["panel", "base", "series", "q", "cost"]
    a = books[books.inst == "QEXP"].set_index(key)
    mv_rows = []
    for w in WS:
        b = books[books.inst == f"QROLL{w}"].set_index(key)
        j = a.join(b, lsuffix="_e", rsuffix="_r", how="inner")
        mv_rows.append(dict(w=w, n=len(j),
                            move4a=int((j.p4a_e != j.p4a_r).sum()),
                            move4b=int((j.p4b_e != j.p4b_r).sum()),
                            gain4a=int(((~j.p4a_e) & j.p4a_r).sum()),
                            gain4b=int(((~j.p4b_e) & j.p4b_r).sum()),
                            lose4a=int((j.p4a_e & (~j.p4a_r)).sum()),
                            lose4b=int((j.p4b_e & (~j.p4b_r)).sum()),
                            med_dSharpe=float((j.Sharpe_r - j.Sharpe_e).median()),
                            med_dOOS=float((j.OOS_Sharpe_r - j.OOS_Sharpe_e).median()),
                            med_dMaxDD=float((j.MaxDD_r - j.MaxDD_e).median())))
    moves = pd.DataFrame(mv_rows)
    log(moves.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------- [5] tuned grid
    log("\n[5] TUNED GRID - w x tau, ALL 16 POINTS.  'inert' = realised rate < tau on 10-bps arms;")
    log("    'inert_verdicts' = gated arm-rows whose 4a or 4b verdict rests on an inert arm.")
    grid = []
    for w in WS:
        sub = head[head.inst == f"QROLL{w}"]
        subq = head[head.inst == "QEXP"]
        for tau in TAUS:
            grid.append(dict(w=w, tau=tau,
                             QEXP_inert=int((subq.rate < tau).sum()), QEXP_n=len(subq),
                             QEXP_inert_share=float((subq.rate < tau).mean()),
                             QROLL_inert=int((sub.rate < tau).sum()), QROLL_n=len(sub),
                             QROLL_inert_share=float((sub.rate < tau).mean()),
                             QEXP_inert_4apass=int(subq[(subq.rate < tau)].p4a.sum()),
                             QEXP_inert_4bpass=int(subq[(subq.rate < tau)].p4b.sum())))
    gdf = pd.DataFrame(grid)
    log(gdf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    gdf.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    # ---------------------------------------------------------- [6] rule 8
    log("\n[6] PROTOCOL RULE 8 WALK-FORWARD - the instrument (QEXP or QROLL w) is CHOSEN on the")
    log("    first half by IS Sharpe alone; every number below is the untouched second half.")
    wf = []
    for (pname, bname, sname, q), g in head.groupby(["panel", "base", "series", "q"]):
        gg = g.set_index("inst")
        pick = gg["IS_Sharpe"].idxmax()
        row = gg.loc[pick]
        wf.append(dict(panel=pname, base=bname, series=sname, q=q, pick=pick,
                       pick_rate=row["rate"], pick_ratio=row["ratio"],
                       OOS_CAGR=row["OOS_CAGR"], OOS_Sharpe=row["OOS_Sharpe"],
                       OOS_MaxDD=row["OOS_MaxDD"], p4a=row["p4a"], p4b=row["p4b"],
                       fail4b=row["fail4b"]))
    wfd = pd.DataFrame(wf)
    wfd.to_csv(OUT / f"{STEM}.wf.csv", index=False)
    log(f"  {len(wfd)} rule-8 cells.  Instrument picked by the IS chooser:")
    log(wfd["pick"].value_counts().to_string())
    log(f"  picks whose realised firing rate < 0.010 (an INERT arm chosen): "
        f"{int((wfd.pick_rate < 0.010).sum())} of {len(wfd)}; < 0.050: "
        f"{int((wfd.pick_rate < 0.050).sum())}")
    log(f"  rule-8 picks passing 4a: {int(wfd.p4a.sum())}/{len(wfd)}; passing 4b: "
        f"{int(wfd.p4b.sum())}/{len(wfd)}")
    log("\n  full rule-8 table:")
    log(wfd.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    log("\n  OOS of the rule-8 picks vs the two comparands, per panel "
        "(median over that panel's cells):")
    for pname, ppx in panels.items():
        start = evals[pname]
        spy = ppx["SPY"].pct_change().fillna(0).loc[start:]
        v2 = backtest(ppx, rules_v2_weights(ppx), cost_bps=10, freq=FREQ)["returns"].loc[start:]
        mo_s, mo_v = metrics(spy.loc[OOS_START:]), metrics(v2.loc[OOS_START:])
        sub = wfd[wfd.panel == pname]
        log(f"    {pname}: picks median OOS CAGR {sub.OOS_CAGR.median():.2%} / Sharpe "
            f"{sub.OOS_Sharpe.median():.3f} / MaxDD {sub.OOS_MaxDD.median():.2%}  ||  "
            f"RULES v2 {mo_v['CAGR']:.2%} / {mo_v['Sharpe']:.3f} / {mo_v['MaxDD']:.2%}  ||  "
            f"SPY {mo_s['CAGR']:.2%} / {mo_s['Sharpe']:.3f} / {mo_s['MaxDD']:.2%}")

    # ---------------------------------------------------------- [8] inherited vs earned
    log("\n[8] IS ANY 4b PASS EARNED BY THE GATE, OR INHERITED FROM ITS UNGATED PARENT?")
    par = head[head.inst == "NOGATE"].set_index(["panel", "base"])[["p4b", "p4a"]]
    gat = head[head.inst != "NOGATE"].copy()
    gat["parent4b"] = [bool(par.loc[(a, b), "p4b"]) for a, b in zip(gat.panel, gat.base)]
    earned = gat[gat.p4b & ~gat.parent4b]
    log(f"  gated arms at 10 bps passing 4b: {int(gat.p4b.sum())} of {len(gat)}; of those, "
        f"{len(earned)} sit on a parent that FAILS 4b (an UNINHERITED pass)")
    if len(earned):
        log(earned[["panel", "base", "series", "q", "inst", "rate", "ratio", "CAGR", "Sharpe",
                    "MaxDD", "H1", "H2", "OOS_Sharpe", "mean_mult"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    wfd2 = wfd.copy()
    wfd2["parent4b"] = [bool(par.loc[(a, b), "p4b"]) for a, b in zip(wfd2.panel, wfd2.base)]
    we = wfd2[wfd2.p4b & ~wfd2.parent4b]
    log(f"  rule-8 picks passing 4b: {int(wfd2.p4b.sum())} of {len(wfd2)}; UNINHERITED "
        f"(parent fails 4b): {len(we)}")
    if len(we):
        log(we.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    log("  4b passes by (panel, base), gated arms, with the parent's own verdict:")
    tb = gat.groupby(["panel", "base"]).agg(n=("p4b", "size"), pass4b=("p4b", "sum"),
                                            parent4b=("parent4b", "first"))
    log(tb.to_string())

    # ---------------------------------------------------------- [6b] full rule-8 chooser
    log("\n[6b] FULL RULE-8 CHOOSER - the WHOLE configuration (series, q, instrument) is chosen")
    log("     on the first half by IS Sharpe, per panel x base; the second half is untouched.")
    log("     Each pick is priced against its own MATCHED-MEAN-GROSS STATIC TWIN (the same")
    log("     average exposure, constant, no timing) - the record's standing 'a gate is only a")
    log("     gross dial' bar, which PROTOCOL does not require but which decides whether the")
    log("     gate earns anything.")
    fc = []
    for (pname, bname), g in head[head.inst != "NOGATE"].groupby(["panel", "base"]):
        pick = g.loc[g["IS_Sharpe"].idxmax()]
        rb, tb, gross = BASES[pname][bname]
        m = MULTS[pname][(pick["series"], pick["q"], pick["inst"])]
        r = apply_gate(rb, tb, m, gross, RUNG_HEAD)
        tw = pd.Series(float(m.mean()), index=m.index)
        rt = apply_gate(rb, tb, tw, gross, RUNG_HEAD)
        par = head[(head.panel == pname) & (head.base == bname) & (head.inst == "NOGATE")].iloc[0]
        mo, mt, mp = metrics(r.loc[OOS_START:]), metrics(rt.loc[OOS_START:]), \
            metrics((rb - tb * RUNG_HEAD / 1e4).loc[OOS_START:])
        fc.append(dict(panel=pname, base=bname, series=pick["series"], q=pick["q"],
                       inst=pick["inst"], rate=pick["rate"], mean_mult=float(m.mean()),
                       OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                       twin_OOS_Sharpe=mt["Sharpe"], twin_OOS_MaxDD=mt["MaxDD"],
                       parent_OOS_Sharpe=mp["Sharpe"], parent_OOS_MaxDD=mp["MaxDD"],
                       beats_twin=bool(mo["Sharpe"] > mt["Sharpe"]),
                       p4a=bool(pick["p4a"]), p4b=bool(pick["p4b"]),
                       fail4b=pick["fail4b"], parent4b=bool(par["p4b"])))
    fcd = pd.DataFrame(fc)
    fcd.to_csv(OUT / f"{STEM}.chooser.csv", index=False)
    log(fcd.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    log(f"  full-chooser picks passing 4a: {int(fcd.p4a.sum())}/{len(fcd)}; 4b: "
        f"{int(fcd.p4b.sum())}/{len(fcd)}; beating their matched-gross twin OOS: "
        f"{int(fcd.beats_twin.sum())}/{len(fcd)}; 4b AND uninherited AND beats twin: "
        f"{int((fcd.p4b & ~fcd.parent4b & fcd.beats_twin).sum())}/{len(fcd)}")

    # ---------------------------------------------------------- [9] episode diagnostic
    log("\n[9] HOW the 4b DD leg is cleared: does the gate COVER the parent's binding decline,")
    log("    or does the binding EPISODE simply move to one the gate never touches?")

    def dd_episode(r):
        eq = (1 + r).cumprod()
        dd = eq / eq.cummax() - 1
        tr = dd.idxmin()
        pk = eq.loc[:tr].idxmax()
        return pk, tr, float(dd.min())

    for pname in panels:
        for bname in ("EWALL0.75", "CAND20"):
            rb, tb, gross = BASES[pname][bname]
            rp = rb - tb * RUNG_HEAD / 1e4
            pk, tr, dmin = dd_episode(rp)
            sub = gat[(gat.panel == pname) & (gat.base == bname) & gat.p4b & ~gat.parent4b]
            if not len(sub):
                continue
            rows = []
            for _, a in sub.iterrows():
                m = MULTS[pname][(a["series"], a["q"], a["inst"])]
                r = apply_gate(rb, tb, m, gross, RUNG_HEAD)
                pk2, tr2, d2 = dd_episode(r)
                cover = float(1.0 - m.loc[pk:tr].mean())        # share of gross cut in the decline
                rows.append(dict(series=a["series"], q=a["q"], inst=a["inst"], cover=cover,
                                 arm_MaxDD=d2, trough=tr2.date(), moved=bool(tr2 != tr)))
            d = pd.DataFrame(rows)
            log(f"  {pname}/{bname}: parent MaxDD {dmin:.4f}, episode {pk.date()} -> {tr.date()}; "
                f"{len(d)} uninherited 4b passes")
            log(f"    cover of the parent's binding decline (1 - mean multiplier over it): "
                f"median {d.cover.median():.4f}, min {d.cover.min():.4f}, max {d.cover.max():.4f}; "
                f"arms with ZERO cover: {int((d.cover <= 1e-12).sum())}")
            log(f"    binding trough MOVED to a different date on {int(d.moved.sum())} of {len(d)} "
                f"arms; distinct arm MaxDD values {d.arm_MaxDD.round(4).nunique()}, modal "
                f"{d.arm_MaxDD.round(4).mode().iloc[0]:.4f} on "
                f"{int((d.arm_MaxDD.round(4) == d.arm_MaxDD.round(4).mode().iloc[0]).sum())} arms")
            log("    " + d.groupby("trough").size().to_string().replace("\n", "\n    "))

    # ---------------------------------------------------------- [7] which published arms
    log("\n[7] WHICH PUBLISHED ARMS ARE RE-PRICED - the census files whose q level this run")
    log("    measures directly, with the deficit at that level (U56, 10 bps, mean over series):")
    for _, r in cen.iterrows():
        qs = sorted({float(m) for m in re.findall(r"quantile\((0\.\d+)\)", r["ctx"])})
        if not qs:
            continue
        for q in qs:
            sel = rates[(rates.panel == "U56") & (rates.q == q)]
            if sel.empty:
                continue
            e = sel[sel.inst == "QEXP"]["ratio"].mean()
            rr = sel[sel.inst == "QROLL1008"]["ratio"].mean()
            log(f"    {r['file'][:72]:74s} q={q:.2f}  QEXP {e:.3f}  QROLL1008 {rr:.3f}")

    (OUT / f"{STEM}.txt").write_text("\n".join(LINES) + "\n")
    log(f"\nWrote {STEM}.txt / .rates.csv / .books.csv / .grid.csv / .wf.csv")


if __name__ == "__main__":
    main()
