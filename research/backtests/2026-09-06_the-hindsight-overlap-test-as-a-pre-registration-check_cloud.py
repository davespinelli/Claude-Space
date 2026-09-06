#!/usr/bin/env python3
"""Idea 266 - "the-hindsight-overlap-test-as-a-pre-registration-check" (cloud, 2026-09-06).

The queue's ask, verbatim
-------------------------
    266. the-hindsight-overlap-test-as-a-pre-registration-check - idea 71's sharpest number
        needed no backtest at all: STK20 overlaps the ex-post best-20 of its own superset by
        10/20 against 4.0 expected, hypergeometric p 6.5e-4. That test is one line and applies
        to every hand-curated panel in the record. Run it over universe.json's four groups,
        ETF36, BSTK100 itself and SMALL439's screen, each against the ex-post top-k of its
        natural superset, and publish the overlap p-value beside every panel the project
        quotes. Report which panels are hindsight-loaded BEFORE their backtests are believed.
        Max 2 params. (2026-09-06)

Design
------
PART A (the census, no backtest).  For every hand-curated panel in the record, the members
are compared against the ex-post top-k of the widest offline superset that contains them,
k = the panel's own size, and the one-sided hypergeometric tail P(overlap >= observed) is
computed EXACTLY (integer binomials, no normal approximation, no scipy).

    panel                        superset                                    note
    STK20  (universe.json megacap)  BSTK100 (the 100 single stocks of B136)   idea 71's cell
    STK20                           ALLSTK  (BSTK100 + the small panel)       size-confounded
    BROAD8 (universe.json broad)    ETF36                                     index ETFs
    SECT16 (universe.json sectors)  ETF36                                     sector ETFs
    BFC12  (bonds_fx_commod, ex-crypto) ETF36                                 diversifiers
    BSTK100                         ALLSTK                                    size-confounded
    SMALL439 (post max_1d_move screen) SMALL483 (the raw panel)               the SCREEN itself
    ETF36                           - none offline -                          reported untestable

Two tuned parameters (PROTOCOL rule 4), both reported at every level, nothing picked:
    1. the ex-post ranking metric   in {TOTRET, SHARPE}
    2. the ranking window           in {FULL, IS (<= 2016-12-31), OOS (>= 2017-01-01)}
The window axis is the point of the run, not a robustness afterthought: a panel assembled in
2026 could in principle have known the IS window (it is history a curator can read) but could
NOT have known the OOS window.  Overlap with the OOS-window top-k is therefore the part of a
panel's advantage that no pre-registration could have earned.

A seeded empirical null (K=200 uniform draws) is run for the headline cell to confirm the
hypergeometric tail is the right null for a uniform draw; it is a check on the arithmetic,
not a second test.

PART B (the backtests PROTOCOL requires).  Each panel is traded with ONE pre-registered book,
fixed before any number here was read and taken from the record rather than tuned:

    RULES v1's composite key (12-1 + 6m + 3m percentile ranks, /sqrt(vol20)) ranked WITHIN
    the panel, RULES v1's gate (above 200d MA, vol20 < 0.60), n = 10, gross = 0.75,
    NORM convention, weekly, next-day execution.

Rungs 0 / 10 / 25 bps are derived exactly from one 0-bps run (`r(c) = r(0) - turnover*c/1e4`,
an identity of engine.backtest asserted against a live call), per ideas 260/261.  Both KEEP
paths are evaluated for every panel at every rung.

PART C (rule 8).  IS <= 2016-12-31 chooses, OOS >= 2017-01-01 is read once:
    ANCHOR         U56, the project's incumbent panel      (the do-nothing arm)
    IS_SHARPE_PICK the panel with the best IS book Sharpe
    CLEAN_PICK     the panel with the LOWEST IS-window overlap excess - i.e. this idea's
                   proposed pre-registration check used as a selector
    LOADED_PICK    the panel with the HIGHEST IS-window overlap excess - its mirror
against RULES v1 OOS and SPY OOS.  The question CLEAN_PICK answers is the queue's real one:
if the overlap test flags a panel BEFORE its backtest is believed, does acting on the flag
pay?  And the linking regression - each panel's OOS Sharpe against its OOS-WINDOW overlap
excess - prices how much of a panel's out-of-sample record is membership hindsight.

SURVIVORSHIP AND SCOPE CAVEATS.  (i) All panels are CURRENT constituents; a name that was
delisted is in no superset here, so every superset is itself hindsight-screened and the
overlap counts below are LOWER bounds on the true selection.  (ii) ALLSTK pools large caps
with sub-$2B names, so a large-cap panel's overlap against it mixes a size effect with a
hindsight effect - those two rows are reported and flagged, never read as clean.  (iii) The
small panel is today's sub-$2B screen carried back to 2010 (data/SMALL_PANEL_README.md); per
instruction the 44 tickers with `max_1d_move >= 1.0` in data/small_meta.csv are dropped, and
that drop is itself one of the tested objects.  (iv) Panels have different member counts and
different histories; the hypergeometric null assumes a uniform k-of-N draw, which no curator
performs, so a small p-value means "not a uniform draw", and the ex-post ORDERING of the
superset is what makes that finding a HINDSIGHT one.

Deterministic, standalone.  Reads baseline.py; modifies nothing outside its own outputs.
"""
import json
import sys
from math import comb
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v1_weights
from engine import backtest, metrics

RUNGS = [0, 10, 25]
PUB_RUNG = 10
N_BOOK = 10
GROSS = 0.75
MAX_VOL = 0.60
FREQ = "W"
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
METRICS = ["TOTRET", "SHARPE"]
WINDOWS = ["FULL", "IS", "OOS"]
NULL_DRAWS = 200
SEED = 266
COVERAGE = 0.95           # a name must trade on >= 95% of the window's days to be rankable
SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 800)


# ---------------------------------------------------------------- membership objects
def build_sets():
    U = json.loads((REPO / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    g = {k: [t for t in v if t not in crypto] for k, v in U.items()}
    etf36 = g["broad"] + g["sectors"] + g["bonds_fx_commod"]

    px56 = load_universe()
    px136 = load_universe(broad=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    pxs_raw = load_universe(small=True)
    small483 = [c for c in pxs_raw.columns if c != "SPY"]
    small439 = [c for c in small483 if c not in bad]
    bstk100 = [t for t in px136.columns if t not in set(etf36) and t != "SPY"]

    sets = dict(STK20=g["megacap"], BROAD8=g["broad"], SECT16=g["sectors"],
                BFC12=g["bonds_fx_commod"], ETF36=etf36, BSTK100=bstk100,
                SMALL439=small439, SMALL483=small483,
                ALLSTK=sorted(set(bstk100) | set(small483)))
    px = dict(U56=px56, B136=px136, SMALL=pxs_raw)
    return sets, px, sorted(bad)


def price_for(names, px):
    """Assemble one price frame for an arbitrary name set out of the three cached panels."""
    cols, src = {}, {}
    for t in names:
        for pn in ("U56", "B136", "SMALL"):
            if t in px[pn].columns:
                cols[t] = px[pn][t]
                src[t] = pn
                break
    return pd.DataFrame(cols).sort_index(), src


# ---------------------------------------------------------------- part A: overlap
def hyper_sf(obs, N, K, n):
    """Exact one-sided P(X >= obs) for a hypergeometric(N, K, n), integer arithmetic."""
    lo, hi = max(0, n + K - N), min(K, n)
    denom = comb(N, n)
    return float(sum(comb(K, x) * comb(N - K, n - x) for x in range(max(obs, lo), hi + 1)) / denom)


def rank_names(prices, names, metric, lo, hi):
    """Ex-post ranking over [lo, hi].  A name is RANKABLE only if it trades at both ends of the
    window (the cached frames are already ffilled, so that is the binding availability test);
    the unrankable ones are returned separately because the two conventions below count them
    differently."""
    cols = [c for c in names if c in prices.columns]
    p = prices.loc[lo:hi, cols]
    if p.empty:
        return [], cols
    ok = [c for c in p.columns if pd.notna(p[c].iloc[0]) and pd.notna(p[c].iloc[-1])
          and p[c].notna().mean() >= COVERAGE]
    q = p[ok].ffill()
    if metric == "TOTRET":
        v = q.iloc[-1] / q.iloc[0] - 1
    else:
        r = q.pct_change()
        v = r.mean() / r.std()
    return list(v.sort_values(ascending=False).index), [c for c in cols if c not in ok]


def overlap_row(label, panel, superset, prices, metric, win, bounds, conv, note=""):
    """One hypergeometric cell.

    PUB  (idea 71's published convention): N = the whole superset and K = the whole panel,
         even though a name that had not listed by the window's start CANNOT be in the top-K.
    COV  (the conservative convention): unrankable names are removed from BOTH N and K.
    """
    lo, hi = bounds[win]
    order, unrank = rank_names(prices, superset, metric, lo, hi)
    inpanel = [t for t in panel if t in superset]
    if conv == "PUB":
        N, members = len(inpanel) + len([t for t in superset if t not in inpanel]), inpanel
    else:
        N, members = len(order), [t for t in inpanel if t in order]
    K = len(members)
    if N == 0 or K == 0 or K >= N or not order:
        return dict(panel=label, conv=conv, metric=metric, window=win, superset_n=N, k=K,
                    unrankable=len(unrank), obs=np.nan, exp=np.nan, excess=np.nan, p=np.nan,
                    note=note or "degenerate")
    top = set(order[:K])
    obs = len(top & set(members))
    exp = K * K / N
    return dict(panel=label, conv=conv, metric=metric, window=win, superset_n=N, k=K,
                unrankable=len(unrank), obs=obs, exp=exp, excess=obs - exp,
                p=hyper_sf(obs, N, K, K), note=note)


# ---------------------------------------------------------------- part B: the one book
def book_weights(px, tradable):
    s, above, vol20 = score(px, vol_scale=True)
    elig = above & (vol20 < MAX_VOL) & px.notna()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        elig[drop] = False
    rank = s.where(elig).rank(axis=1, ascending=False)
    sel = (rank <= N_BOOK).astype(float)
    held = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(held, axis=0).mul(GROSS).fillna(0.0)


def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def pass4a(r, base):
    h1, h2 = half_sharpes(r)
    b1, b2 = half_sharpes(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def fail4b(r, spy):
    h1, h2 = half_sharpes(r)
    s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    mo, mso = metrics(r.loc[OOS_START:]), metrics(spy.loc[OOS_START:])
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not mo["Sharpe"] > mso["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 3:
        return np.nan
    ra = pd.Series(a[m]).rank().values
    rb = pd.Series(b[m]).rank().values
    return float(np.corrcoef(ra, rb)[0, 1])


def fmt(df, p=3):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


def main():
    sets, PX, dropped = build_sets()
    pool, _ = price_for(sets["ALLSTK"], PX)
    pool = pool.loc[PX["SMALL"].index[0]:]        # the pooled frame starts where the small panel does
    FRAMES = {"U56": PX["U56"], "B136": PX["B136"], "SMALL": PX["SMALL"], "POOL": pool}

    def win_bounds(frame):
        """Windows start at the frame's 260th bar - the same post-warm-up start every book in
        this project is evaluated from, and the start idea 71's published cell used."""
        i = frame.index
        s = i[260]
        return {"FULL": (s, i[-1]), "IS": (s, pd.Timestamp(IS_END)),
                "OOS": (pd.Timestamp(OOS_START), i[-1])}

    print("=" * 200)
    print(f"Idea 266 the-hindsight-overlap-test-as-a-pre-registration-check | {SCRIPT}")
    print(f"sets: " + ", ".join(f"{k}={len(v)}" for k, v in sets.items()))
    for k, f in FRAMES.items():
        print(f"  frame {k:5s} {f.index[0].date()} -> {f.index[-1].date()}, {f.shape[1]} columns")
    print(f"windows per frame: FULL = the frame's own span | IS ..{IS_END} | OOS {OOS_START}.. | "
          f"metrics {METRICS} | conventions PUB (idea 71's) and COV (unrankable names dropped)")
    print(f"small panel: {len(dropped)} tickers dropped by the max_1d_move>=1.0 screen")
    print("=" * 200)

    # ---------------- PART A -------------------------------------------------
    pairs = [("STK20", "STK20", "BSTK100", "B136", ""),
             ("STK20 vs ALLSTK", "STK20", "ALLSTK", "POOL", "size-confounded"),
             ("BROAD8", "BROAD8", "ETF36", "U56", ""),
             ("SECT16", "SECT16", "ETF36", "U56", ""),
             ("BFC12", "BFC12", "ETF36", "U56", ""),
             ("BSTK100 vs ALLSTK", "BSTK100", "ALLSTK", "POOL", "size-confounded"),
             ("SMALL439 screen", "SMALL439", "SMALL483", "SMALL", "the max_1d_move screen itself")]
    rows = []
    for lab, pn, sn, fk, note in pairs:
        b = win_bounds(FRAMES[fk])
        for conv in ("PUB", "COV"):
            for metric in METRICS:
                for win in WINDOWS:
                    rows.append(overlap_row(lab, sets[pn], sets[sn], FRAMES[fk], metric, win, b,
                                            conv, note))
    A = pd.DataFrame(rows)
    A["p_lt_05"] = A["p"] < 0.05
    A.to_csv(OUT / f"{STEM}.overlap.csv", index=False)
    print("\n--- PART A: hindsight-overlap census, panel x convention x metric x window "
          "(exact hypergeometric) " + "-" * 25)
    print(A.set_index(["panel", "conv", "metric", "window"])[["superset_n", "k", "unrankable", "obs",
                                                              "exp", "excess", "p", "p_lt_05", "note"]]
          .to_string(float_format=lambda x: f"{x:.4g}"))
    print("\nsignificant at 0.05, by panel x convention (of 6 metric x window cells each):")
    print(A.groupby(["panel", "conv"]).agg(cells=("p", "size"), sig=("p_lt_05", "sum"),
                                           min_p=("p", "min"), mean_excess=("excess", "mean")
                                           ).to_string(float_format=lambda x: f"{x:.4g}"))
    print("\nwhat the convention costs: the same cell under PUB and COV")
    piv = A.pivot_table(index=["panel", "metric", "window"], columns="conv",
                        values=["k", "superset_n", "obs", "excess", "p"])
    print(piv.to_string(float_format=lambda x: f"{x:.4g}"))
    print("\nETF36: NO offline superset exists (it IS the whole cached ETF list) - UNTESTABLE here, "
          "reported as such rather than scored.")

    print("\nreproduction of idea 71's published cell (STK20 vs BSTK100, TOTRET, FULL, PUB):")
    r71 = A[(A.panel == "STK20") & (A.metric == "TOTRET") & (A.window == "FULL")
            & (A.conv == "PUB")].iloc[0]
    print(f"  overlap {int(r71['obs'])} of {int(r71['k'])} against {r71['exp']:.1f} expected, "
          f"N={int(r71['superset_n'])}, p = {r71['p']:.3g}   (idea 71 published 10/20 vs 4.0, p 6.5e-4)")

    rng = np.random.default_rng(SEED)
    b71 = win_bounds(FRAMES["B136"])
    order, unrank = rank_names(FRAMES["B136"], sets["BSTK100"], "TOTRET", *b71["FULL"])
    K71 = int(r71["k"])
    top = set(order[:K71])
    pool71 = list(order) + list(unrank)                      # PUB draws from the WHOLE superset
    draws = [len(top & set(rng.choice(pool71, size=K71, replace=False))) for _ in range(NULL_DRAWS)]
    emp = float(np.mean(np.asarray(draws) >= r71["obs"]))
    print(f"  empirical null ({NULL_DRAWS} seeded uniform {K71}-of-{len(pool71)} draws): "
          f"mean overlap {np.mean(draws):.2f} (hypergeometric expectation {r71['exp']:.2f}), "
          f"P(overlap >= {int(r71['obs'])}) = {emp:.3g} vs exact {r71['p']:.3g}; "
          f"{len(unrank)} of {len(pool71)} superset names were not listed at the window start and "
          f"therefore CANNOT enter the top-{K71} under PUB")

    # ---------------- PART B -------------------------------------------------
    print("\n--- PART B: the one pre-registered book on every panel (composite/n10/g0.75/NORM/W) "
          + "-" * 35)
    book_panels = {"U56": ("U56", None), "ETF36": ("U56", "ETF36"), "STK20": ("U56", "STK20"),
                   "B136": ("B136", None), "BSTK100": ("B136", "BSTK100"),
                   "SMALL439": ("SMALL", "SMALL439"), "SMALL483": ("SMALL", "SMALL483")}

    # the two counterfactual panels the overlap test implies, on STK20's own superset:
    #   HIND20_IS   top 20 of BSTK100 by IS-window total return - KNOWABLE on 2017-01-01,
    #               so it is a legitimate ex-ante rule and the honest benchmark for STK20
    #   HIND20_OOS  top 20 by OOS-window total return - pure look-ahead, the ceiling
    b71 = win_bounds(FRAMES["B136"])
    ordIS, _ = rank_names(FRAMES["B136"], sets["BSTK100"], "TOTRET", *b71["IS"])
    ordOOS, _ = rank_names(FRAMES["B136"], sets["BSTK100"], "TOTRET", *b71["OOS"])
    sets["HIND20_IS"] = ordIS[:20]
    sets["HIND20_OOS"] = ordOOS[:20]
    book_panels["HIND20_IS"] = ("B136", "HIND20_IS")
    book_panels["HIND20_OOS"] = ("B136", "HIND20_OOS")
    print(f"  HIND20_IS  (top 20 of BSTK100 by 2009-2016 total return) = {','.join(sets['HIND20_IS'])}")
    print(f"  HIND20_OOS (top 20 by 2017-2026 total return, LOOK-AHEAD) = {','.join(sets['HIND20_OOS'])}")
    print(f"  STK20 n HIND20_IS = {len(set(sets['STK20']) & set(sets['HIND20_IS']))}/20   "
          f"STK20 n HIND20_OOS = {len(set(sets['STK20']) & set(sets['HIND20_OOS']))}/20")
    brows, series = [], {}
    checked = False
    for lab, (parent, sub) in book_panels.items():
        px = PX[parent]
        tradable = set(px.columns) - {"SPY"} if sub is None else set(sets[sub])
        cols = list(dict.fromkeys(sorted(tradable & set(px.columns))
                                  + (["SPY"] if "SPY" in px.columns else [])))
        p = px[cols].dropna(how="all").ffill()
        start = p.index[260]
        spy = p["SPY"].pct_change().fillna(0.0).loc[start:]
        base = backtest(p, rules_v1_weights(p), cost_bps=PUB_RUNG, freq=FREQ)["returns"].loc[start:]
        w = book_weights(p, tradable)
        res = backtest(p, w, cost_bps=0.0, freq=FREQ)
        r0, turn = res["returns"], res["turnover"]
        if not checked:
            live = backtest(p, w, cost_bps=float(PUB_RUNG), freq=FREQ)["returns"]
            err = float(np.max(np.abs((r0 - turn * PUB_RUNG / 1e4) - live)))
            print(f"  harness identity |derived - live @{PUB_RUNG}bps| max = {err:.3e}")
            if err > 1e-12:
                print("!! cost identity failed - aborting."); sys.exit(1)
            checked = True
        years = len(r0.loc[start:]) / 252
        to_yr = float(turn.loc[start:].sum() / years)
        for c in RUNGS:
            r = (r0 - turn * c / 1e4).loc[start:]
            m, mo, mi = metrics(r), metrics(r.loc[OOS_START:]), metrics(r.loc[:IS_END])
            h1, h2 = half_sharpes(r)
            f4 = fail4b(r, spy)
            series[(lab, c)] = r
            brows.append(dict(panel=lab, members=len(tradable & set(px.columns)), cost=c,
                              CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                              IS_Sharpe=mi["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                              OOS_MaxDD=mo["MaxDD"], decay=mi["Sharpe"] - mo["Sharpe"], TO=to_yr,
                              p4a=pass4a(r, base), f4b=f4, p4b=(f4 == "-")))
        series[(lab, "__BASE__")] = base
        series[(lab, "__SPY__")] = spy
    B = pd.DataFrame(brows)
    B.to_csv(OUT / f"{STEM}.books.csv", index=False)
    print(fmt(B.set_index(["panel", "cost"])))
    print("\ncontrols (RULES v1 weekly @10 bps and SPY, on each parent price panel):")
    ctl = []
    for lab in book_panels:
        for nm, r in (("RULES v1", series[(lab, "__BASE__")]), ("SPY", series[(lab, "__SPY__")])):
            m, mo = metrics(r), metrics(r.loc[OOS_START:])
            h1, h2 = half_sharpes(r)
            ctl.append(dict(panel=lab, arm=nm, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                            H1=h1, H2=h2, OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                            OOS_MaxDD=mo["MaxDD"]))
    print(fmt(pd.DataFrame(ctl).set_index(["panel", "arm"])))
    print("\nKEEP paths by rung:")
    print(fmt(B.groupby("cost")[["p4a", "p4b"]].sum().join(B.groupby("cost").size().to_frame("n")), 0))
    if B["p4b"].any():
        print("\nevery 4b pass:")
        print(fmt(B[B.p4b].set_index(["panel", "cost"])[["CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                                         "OOS_Sharpe", "OOS_MaxDD", "TO"]]))
    else:
        print("\n4b passes: NONE at any rung.")
    print("\nfailing 4b bars at the published rung:")
    print(B[B.cost == PUB_RUNG]["f4b"].value_counts().to_string())

    # ---------------- the link: overlap vs book -------------------------------
    print("\n--- does the overlap statistic predict the book? (excess overlap vs performance) "
          + "-" * 45)
    link_map = {"STK20": "STK20", "BSTK100": "BSTK100 vs ALLSTK", "SMALL439": "SMALL439 screen"}
    lrows = []
    for blab, olab in link_map.items():
        b = B[(B.panel == blab) & (B.cost == PUB_RUNG)].iloc[0]
        for metric in METRICS:
            sub = A[(A.panel == olab) & (A.metric == metric) & (A.conv == "COV")].set_index("window")
            lrows.append(dict(panel=blab, metric=metric,
                              exc_FULL=sub.loc["FULL", "excess"], p_FULL=sub.loc["FULL", "p"],
                              exc_IS=sub.loc["IS", "excess"], p_IS=sub.loc["IS", "p"],
                              exc_OOS=sub.loc["OOS", "excess"], p_OOS=sub.loc["OOS", "p"],
                              Sharpe=b["Sharpe"], OOS_Sharpe=b["OOS_Sharpe"], decay=b["decay"],
                              f4b=b["f4b"]))
    L = pd.DataFrame(lrows)
    L.to_csv(OUT / f"{STEM}.link.csv", index=False)
    print(L.set_index(["panel", "metric"]).to_string(float_format=lambda x: f"{x:.4g}"))
    for metric in METRICS:
        s = L[L.metric == metric]
        print(f"  [{metric}] Spearman(excess_OOS, OOS_Sharpe) = {spearman(s.exc_OOS, s.OOS_Sharpe):.3f}; "
              f"Spearman(excess_IS, OOS_Sharpe) = {spearman(s.exc_IS, s.OOS_Sharpe):.3f}; "
              f"n = {len(s)} panels (too few to order; reported as a table, not a fit)")

    # ---------------- PART C: rule 8 -----------------------------------------
    print("\n--- PART C: PROTOCOL rule 8 (IS <= 2016-12-31 chooses, OOS >= 2017 read once) " + "-" * 45)
    cand = [c for c in book_panels if c not in ("SMALL483", "HIND20_OOS")]
    isS = {c: B[(B.panel == c) & (B.cost == PUB_RUNG)].iloc[0]["IS_Sharpe"] for c in cand}
    ov_is = {}
    for c in cand:
        olab = {"STK20": "STK20", "BSTK100": "BSTK100 vs ALLSTK", "SMALL439": "SMALL439 screen"}.get(c)
        if olab is None:
            continue
        sub = A[(A.panel == olab) & (A.metric == "TOTRET") & (A.window == "IS") & (A.conv == "COV")]
        v = float(sub.iloc[0]["p"])
        if np.isfinite(v):
            ov_is[c] = v
    sel = {"ANCHOR (U56, do nothing)": "U56",
           "IS_SHARPE_PICK": max(isS, key=isS.get),
           "CLEAN_PICK (weakest IS overlap evidence, highest p)": max(ov_is, key=ov_is.get),
           "LOADED_PICK (strongest IS overlap evidence, lowest p)": min(ov_is, key=ov_is.get),
           "HIND20_IS (a real ex-ante rule on the same superset)": "HIND20_IS",
           "HIND20_OOS (look-ahead ceiling, NOT a rule)": "HIND20_OOS"}
    print(f"  IS book Sharpe @10 bps: " + ", ".join(f"{k} {v:.3f}" for k, v in isS.items()))
    print(f"  IS-window overlap p (TOTRET, COV): " + ", ".join(f"{k} {v:.4g}" for k, v in ov_is.items())
          + "   [only the 3 panels with an offline superset are eligible for the overlap selectors]")
    w8 = []
    for lab, pick in sel.items():
        r = series[(pick, PUB_RUNG)]
        m, mo = metrics(r), metrics(r.loc[OOS_START:])
        w8.append(dict(selector=lab, picked=pick, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                       OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                       p4a=pass4a(r, series[(pick, "__BASE__")]),
                       f4b=fail4b(r, series[(pick, "__SPY__")])))
    for nm, key in (("RULES v1 (U56)", "U56"), ("SPY", "U56")):
        r = series[(key, "__BASE__" if nm.startswith("RULES") else "__SPY__")]
        m, mo = metrics(r), metrics(r.loc[OOS_START:])
        w8.append(dict(selector=nm, picked="-", CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                       OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                       p4a=np.nan, f4b="-"))
    W = pd.DataFrame(w8)
    W.to_csv(OUT / f"{STEM}.rule8.csv", index=False)
    print(fmt(W.set_index("selector")))

    print("\n--- the number the queue actually asked for: the publishable column " + "-" * 80)
    pub = A[(A.metric == "TOTRET") & (A.window == "FULL")].set_index(["panel", "conv"])[
        ["superset_n", "k", "unrankable", "obs", "exp", "excess", "p", "note"]]
    print(pub.to_string(float_format=lambda x: f"{x:.4g}"))
    print("(ETF36: no offline superset - the column cannot be computed and must be printed as such.)")

    print("\n" + "=" * 200)
    print("CAVEATS: (i) every superset is itself made of CURRENT constituents, so delisted names are "
          "absent from both panel and superset and the overlap counts are LOWER bounds on the true "
          "selection; (ii) the two ALLSTK rows pool large caps with sub-$2B names and therefore mix a "
          "SIZE effect into the hindsight reading - flagged, not clean; (iii) the hypergeometric null is "
          "a uniform k-of-N draw, which no curator performs, so a small p means 'not uniform' and it is "
          "the EX-POST ordering of the superset that makes it a hindsight finding; (iv) the small panel "
          "is today's sub-$2B screen carried back to 2010 and its own max_1d_move screen is one of the "
          "objects under test; (v) 3 panels have an offline superset, so the link between overlap and "
          "performance is reported as a table, not fitted.")
    print("=" * 200)


if __name__ == "__main__":
    main()
