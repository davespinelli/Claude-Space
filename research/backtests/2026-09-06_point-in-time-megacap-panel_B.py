#!/usr/bin/env python3
"""QUEUE idea 71 - point-in-time-megacap-panel   (lane B, 2026-09-06).

THE IDEA AS QUEUED.  Idea 10 found "the whole edge of universe.json lives in its 20
mega-cap single stocks" (STK20 / CAND-n20 passed 4a AND 4b, the run's only 4a pass, and
rule 8 selected it), but idea 10's own control showed the effect shrinks 5.6x on
universe_broad.json's 100 stocks -- so it is *selection*.  The queued fix is
INFRASTRUCTURE: build a point-in-time top-20-by-market-cap panel (names that later fell
out included) and re-run.

WHAT IS AND IS NOT POSSIBLE OFFLINE.  A true PIT market-cap panel needs (a) shares
outstanding per name per date and (b) the tickers that were top-20 in 2009-2015 and have
since fallen out (GE, XOM at its old weight, CSCO, INTC, IBM, PFE, WFC, T, ...) or been
delisted.  data/ has NEITHER: no shares-outstanding series (idea 195 PARKed exactly this),
and prices_broad.csv is 136 CURRENT constituents, so a fallen-out name is not merely
mis-weighted, it is ABSENT.  The infrastructure half of idea 71 is therefore PARKed:
**needs local/Actions data** (shares outstanding + a delisted-name price cache).

WHAT THIS RUN DOES INSTEAD -- and it is the number the idea exists to produce.  Idea 71's
operative claim is not "market cap" but "**STK20's edge is hand-picking**", and the size
of that doubt is measurable offline WITHOUT PIT market cap.  Hold the book fixed and vary
only the PANEL:

  STK20      the 20 names of universe.json['megacap'] -- the hand-picked incumbent panel
  HIND20     top 20 of BSTK100 by FULL-SAMPLE total return -- deliberate look-ahead, the
             CEILING on what hand-picking 20 of 100 names can possibly buy
  PITGROW20  lookahead-free panel: each 31-Dec, rank BSTK100 by cumulative return from
             sample start to THAT date, take the top 20, hold for the next calendar year.
             This is the honest offline stand-in for a PIT megacap rule (megacaps in this
             era became megacaps by rising).  It is NOT market cap -- see CAVEATS.
  RAND20     K=200 seeded uniform 20-name draws from BSTK100 -- the null distribution
  BSTK100    all 100 single stocks, no panel selection at all (the EWall control)

Then read three things: (1) where STK20 sits in the RAND20 distribution, (2) what share of
the HIND20 ceiling STK20 captures -- the SELECTION SHARE -- and (3) whether the
lookahead-free PITGROW20 panel reproduces STK20.  If STK20 sits near the RAND20 median,
"the edge lives in the 20 megacaps" is a claim about 20 names out of 100, not about those
20 names.  If it sits at the ceiling with PITGROW20 far below, the edge is hand-picking.

BOOK (identical across every arm; the panel is the ONLY treatment).  Composite score
(12-1 mom + 6m + 3m, equal-rank-weighted, ranked WITHIN the panel), x (0.5 + 0.5*above200d),
divided by sqrt(vol20) -- byte-identical to research/baseline.score when the panel is the
whole column set (asserted in check_b).  Eligible = in panel AND above 200d AND vol20 < 0.60.
Weekly cadence, t+1 execution, PROTOCOL rule 2.

GRID (exactly 2 tuned parameters, ALL points reported, nothing picked outside rule 8):
    n      book size in {5, 10, 20, ALL-eligible}      (4 points)
    g      gross target in {0.75, 1.00}                (2 points)
Both weight conventions are reported side by side and neither is selected on:
    NORM   w = g / (number actually selected)   -- constant realised gross (idea 240's fix)
    FIXED  w = g / n                            -- de-grosses when < n names are eligible
Cost rungs 10 bps (PROTOCOL) and 0 bps (idea 261's required twin) from one run each.

KEEP PATHS (PROTOCOL rule 4, both evaluated):
    4a  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1.
    4b  Sharpe > SPY in BOTH halves AND on the rule-8 OOS window,
        MaxDD <= 0.60 x |SPY MaxDD|, CAGR >= 0.70 x SPY CAGR.
RULE 8 (required): (n, g, convention) chosen on <= 2016-12-31 IS Sharpe only, per arm;
2017-01-01.. read ONCE.  OOS CAGR/Sharpe/MaxDD reported vs the RULES v1 baseline and SPY.

CAVEATS, stated up front because they are the whole point of the queued idea:
  * PROTOCOL rule 9: universe_broad.json is CURRENT constituents.  Every arm here --
    RAND20 included -- draws from survivors.  This run bounds HAND-PICKING WITHIN a
    survivor set.  It cannot and does not measure survivorship itself.  The RAND20 null is
    therefore a *conservative* null: it is already survivorship-inflated, so STK20 beating
    it is the harder result and STK20 failing to beat it is the safer one.
  * PITGROW20 is a price-growth proxy, not market cap.  No shares-outstanding series is
    cached.  It is lookahead-free (expanding window, annual re-selection) but it will
    over-select names whose share count shrank (buybacks) and under-select issuers.

Deterministic (numpy default_rng(71)).  Runnable standalone, no network.
Writes:  <stem>.grid.csv, <stem>.rand.csv, <stem>.out.md
"""
import sys, json
from math import comb
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, score as baseline_score  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask  # noqa

OUT = ROOT / "research" / "backtests"
STEM = "2026-09-06_point-in-time-megacap-panel_B"
SEED = 71
K_RAND = 200
MAX_VOL = 0.60
CAD = "W"
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
PHI, DELTA = 0.70, 0.60          # 4b CAGR floor and MaxDD cap vs SPY
N_GRID = [5, 10, 20, None]       # None = all eligible
G_GRID = [0.75, 1.00]
CONVS = ["NORM", "FIXED"]
RUNGS = [0, 10]

_LOG = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); _LOG.append(s)


# ---------------------------------------------------------------- engine (vectorised)
def cad_mask(idx, cad):
    """True on the last bar of each cadence block; same rule as engine.rebalance_mask."""
    key = {"W": idx.to_period("W"), "M": idx.to_period("M"), "Q": idx.to_period("Q")}[cad]
    key = np.asarray(pd.PeriodIndex(key).astype("int64"))
    m = np.empty(len(idx), bool); m[:-1] = key[:-1] != key[1:]; m[-1] = True
    return pd.Series(m, index=idx)


def fast_backtest(prices, weights, cad=CAD):
    """Vectorised equivalent of engine.backtest at cost_bps=0; returns gross rets + turnover."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = cad_mask(idx, cad).shift(1, fill_value=False).values.copy(); mask[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mask)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]; W0 = wt[s0]
    h = W0 * (Cp / Cp[s0]); V = h.sum(axis=1) + (1.0 - W0.sum(axis=1)); held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]; W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p]); Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1)); heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T); turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return pd.Series((held * rets).sum(axis=1), index=idx), pd.Series(turn, index=idx)


def net(r0, turn, bps):
    return r0 - turn * bps / 1e4


def mtr(r):
    r = np.asarray(r, float)
    if len(r) < 60: return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    eq = np.cumprod(1.0 + r); yrs = len(r) / 252.0
    v = r.std(ddof=1) * np.sqrt(252)
    dd = eq / np.maximum.accumulate(eq) - 1.0
    return dict(CAGR=eq[-1] ** (1 / yrs) - 1, Sharpe=(r.mean() * 252) / v if v else np.nan,
                MaxDD=dd.min())


# ---------------------------------------------------------------- panels and book
ETF_GROUPS = ("broad", "sectors", "bonds_fx_commod")


def build_panels(px):
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    etfs = {t for g in ETF_GROUPS for t in U[g]}
    stocks = sorted([c for c in px.columns if c not in etfs])
    mega = [t for t in U["megacap"]]
    return stocks, mega


def raw_signals(px):
    """Member-independent pieces of baseline.score, computed once for the whole run."""
    return dict(mom=px.shift(21) / px.shift(252) - 1,
                r6=px / px.shift(126) - 1,
                r3=px / px.shift(63) - 1,
                above=px > px.rolling(200).mean(),
                vol20=px.pct_change().rolling(20).std() * np.sqrt(252))


def panel_score(px, member, R=None):
    """baseline.score, but cross-sectional ranks taken WITHIN `member` only."""
    if R is None: R = raw_signals(px)
    rk = lambda x: x.where(member).rank(axis=1, pct=True)
    comp = (rk(R["mom"]) + rk(R["r6"]) + rk(R["r3"])) / 3
    s = comp * (0.5 + 0.5 * R["above"].astype(float)) / R["vol20"].clip(lower=0.08) ** 0.5
    return s, R["above"], R["vol20"]


def const_score(R, names):
    """panel_score for a CONSTANT panel, computed on that panel's columns only.
    Ranking within `member` is identical to ranking the column subset, so this is the same
    number far more cheaply (asserted against the full-width path in check_c)."""
    rk = lambda k: R[k][names].rank(axis=1, pct=True)
    comp = (rk("mom") + rk("r6") + rk("r3")) / 3
    above, vol20 = R["above"][names], R["vol20"][names]
    return comp * (0.5 + 0.5 * above.astype(float)) / vol20.clip(lower=0.08) ** 0.5, above, vol20


def weights_from(pre, member, n, g, conv):
    s, above, vol20 = pre
    elig = s.where(above & (vol20 < MAX_VOL)) if member is None else \
           s.where(member & above & (vol20 < MAX_VOL))
    if n is None:
        sel = elig.notna()
    else:
        sel = elig.rank(axis=1, ascending=False) <= n
    cnt = sel.sum(axis=1)
    if conv == "NORM" or n is None:
        return sel.astype(float).div(cnt.replace(0, np.nan), axis=0).fillna(0.0) * g
    return sel.astype(float) * (g / n)


def book_weights(px, member, n, g, conv, R=None, pre=None):
    return weights_from(pre if pre is not None else panel_score(px, member, R),
                        member, n, g, conv)


def const_member(px, names):
    m = pd.DataFrame(False, index=px.index, columns=px.columns)
    m.loc[:, names] = True
    return m


def pitgrow_member(px, stocks, k=20):
    """Lookahead-free: each 31-Dec rank stocks by cumulative return from sample start to
    that date (needs >= 252 obs), take top k, hold for the NEXT calendar year."""
    sub = px[stocks]
    first = sub.apply(lambda c: c.first_valid_index())
    m = pd.DataFrame(False, index=px.index, columns=px.columns)
    yrs = sorted(set(px.index.year))
    prev = None
    for y in yrs:
        if prev is None:
            sel = stocks[:k]                      # first year: alphabetical, no information
        else:
            asof = px.index[px.index <= f"{prev}-12-31"][-1]
            grow = {}
            for t in stocks:
                f = first[t]
                if pd.isna(f) or f > asof or (asof - f).days < 400: continue
                p0, p1 = sub[t].loc[f], sub[t].loc[asof]
                if p0 > 0 and np.isfinite(p1) and np.isfinite(p0): grow[t] = p1 / p0
            sel = [t for t, _ in sorted(grow.items(), key=lambda kv: -kv[1])[:k]]
            if len(sel) < k: sel = sel + [t for t in stocks if t not in sel][:k - len(sel)]
        m.loc[m.index.year == y, sel] = True
        prev = y
    return m


# ---------------------------------------------------------------- reproduction controls
def check_a(px, w):
    """engine.backtest leaves NaN on the first 2 bars (it reads the shifted weight row 0
    before any rebalance); compare on the post-warm-up window every metric here uses."""
    e = engine_backtest(px, w, cost_bps=10.0, freq=CAD)
    r0, tn = fast_backtest(px, w)
    sl = px.index[260:]
    d1 = float(np.abs(net(r0, tn, 10).loc[sl].values - e["returns"].loc[sl].values).max())
    d2 = float(np.abs(tn.loc[sl].values - e["turnover"].loc[sl].values).max())
    P(f"  check_a  fast_backtest vs engine.backtest : returns {d1:.2e}  turnover {d2:.2e}")
    assert d1 < 1e-12 and d2 < 1e-12
    return d1, d2


def check_b(px, stocks):
    sub = px[stocks]
    s_ref, _, _ = baseline_score(sub)
    s_new, _, _ = panel_score(sub, pd.DataFrame(True, index=sub.index, columns=sub.columns))
    d = float((s_ref - s_new).abs().max().max())
    P(f"  check_b  panel_score vs baseline.score (all-member) : {d:.2e}")
    assert d < 1e-12
    return d


# ---------------------------------------------------------------- main
def main():
    px = load_universe(broad=True).dropna(how="all").ffill()
    stocks, mega = build_panels(px)
    P("=" * 100)
    P("IDEA 71  point-in-time-megacap-panel  (lane B, 2026-09-06)   PANEL-SELECTION BOUND")
    P("=" * 100)
    P(f"sample {px.index[0].date()} .. {px.index[-1].date()}   B136 cols {px.shape[1]}   "
      f"single stocks BSTK100 {len(stocks)}   megacap STK20 {len(mega)}")
    assert len(stocks) == 100, len(stocks)
    assert set(mega) <= set(stocks), set(mega) - set(stocks)
    P("  PIT market cap: data/ has no shares-outstanding series and prices_broad.csv holds")
    P("  CURRENT constituents only -> fallen-out names are ABSENT, not mis-weighted.")
    P("  Infrastructure half of idea 71 -> PARK (needs local/Actions data).  This run bounds")
    P("  hand-picking WITHIN the survivor set, which is the claim idea 10 actually made.")
    P("")
    P("REPRODUCTION CONTROLS")
    w_chk = book_weights(px, const_member(px, mega), 5, 0.75, "NORM")
    check_a(px, w_chk)
    check_b(px, stocks)

    start = px.index[260]
    idx = px.index[px.index >= start]
    h = len(idx) // 2
    W = dict(FULL=idx, H1=idx[:h], H2=idx[h:],
             IS=idx[idx <= IS_END], OOS=idx[idx >= OOS_START])
    P(f"  windows  FULL {len(idx)}d  H1 {len(W['H1'])}d  H2 {len(W['H2'])}d  "
      f"IS {len(W['IS'])}d (..{W['IS'][-1].date()})  OOS {len(W['OOS'])}d ({W['OOS'][0].date()}..)")

    # references
    ref = {}
    br0, btn = fast_backtest(px, rules_v1_weights(px))
    spy = px["SPY"].pct_change().fillna(0.0)
    for bps in RUNGS:
        b = net(br0, btn, bps)
        ref[("RULESv1", bps)] = {k: mtr(b.loc[v]) for k, v in W.items()}
    ref[("SPY", 0)] = {k: mtr(spy.loc[v]) for k, v in W.items()}
    ref[("SPY", 10)] = ref[("SPY", 0)]
    P("")
    P("REFERENCES (10 bps for the book, SPY is buy-and-hold so cost-free)")
    for nm, bps in [("RULESv1", 10), ("SPY", 0)]:
        d = ref[(nm, bps)]
        P(f"  {nm:8s} FULL CAGR {d['FULL']['CAGR']:7.2%} Sharpe {d['FULL']['Sharpe']:.4f} "
          f"MaxDD {d['FULL']['MaxDD']:7.2%} | H1 {d['H1']['Sharpe']:.4f} H2 {d['H2']['Sharpe']:.4f} "
          f"| OOS CAGR {d['OOS']['CAGR']:7.2%} Sharpe {d['OOS']['Sharpe']:.4f} MaxDD {d['OOS']['MaxDD']:7.2%}")
    S = ref[("SPY", 0)]
    P(f"  4b bars: |MaxDD| <= {DELTA:.2f}x|SPY| -> FULL {DELTA*abs(S['FULL']['MaxDD']):.2%}, "
      f"OOS {DELTA*abs(S['OOS']['MaxDD']):.2%};  CAGR >= {PHI:.2f}x SPY -> FULL "
      f"{PHI*S['FULL']['CAGR']:.2%}, OOS {PHI*S['OOS']['CAGR']:.2%}")

    # arms
    full_ret = px[stocks].loc[idx[-1]] / px[stocks].loc[idx[0]]
    hind = list(full_ret.sort_values(ascending=False).index[:20])
    members = {
        "STK20":     const_member(px, mega),
        "HIND20":    const_member(px, hind),
        "PITGROW20": pitgrow_member(px, stocks),
        "BSTK100":   const_member(px, stocks),
    }
    rng = np.random.default_rng(SEED)
    rand_sets = [sorted(rng.choice(stocks, 20, replace=False).tolist()) for _ in range(K_RAND)]
    P("")
    P(f"  HIND20 (full-sample top-20 by total return) = {','.join(hind)}")
    ov = len(set(mega) & set(hind))
    hyp = sum(comb(20, i) * comb(80, 20 - i) for i in range(ov, 21)) / comb(100, 20)
    P(f"  STK20 n HIND20 = {ov} names: {','.join(sorted(set(mega) & set(hind)))}")
    P(f"  overlap {ov}/20 against {20*20/100:.1f} expected for a random 20-of-100 draw; "
      f"hypergeometric P(overlap >= {ov}) = {hyp:.3e}")
    P("  -> the hand-picked panel is DEMONSTRABLY hindsight-loaded at the membership level,")
    P("     independently of anything the backtest says.")
    pg = members["PITGROW20"]
    lastyr = pg.loc[pg.index.year == idx[-1].year].iloc[0]
    P(f"  PITGROW20 final-year panel = {','.join(sorted(lastyr[lastyr].index))}")
    P(f"  PITGROW20 final n STK20 = {len(set(lastyr[lastyr].index) & set(mega))}/20")

    R = raw_signals(px)

    def run_arm(mem=None, names=None):
        """names -> fast constant-panel path (rank and backtest on that panel's columns);
        mem -> general time-varying-membership path over all 136 columns."""
        rows = []
        if names is not None:
            pre, sub, memb = const_score(R, names), px[names], None
        else:
            pre, sub, memb = panel_score(px, mem, R), px, mem
        for n in N_GRID:
            for g in G_GRID:
                for conv in CONVS:
                    if n is None and conv == "FIXED": continue      # identical to NORM
                    r0, tn = fast_backtest(sub, weights_from(pre, memb, n, g, conv))
                    for bps in RUNGS:
                        r = net(r0, tn, bps)
                        rec = dict(n=("ALL" if n is None else n), g=g, conv=conv, bps=bps,
                                   turn=float(tn.loc[idx].sum()) / (len(idx) / 252.0))
                        for k, v in W.items():
                            m = mtr(r.loc[v])
                            rec[f"{k}_CAGR"], rec[f"{k}_Sharpe"], rec[f"{k}_MaxDD"] = \
                                m["CAGR"], m["Sharpe"], m["MaxDD"]
                        rows.append(rec)
        return pd.DataFrame(rows)

    const_names = {"STK20": mega, "HIND20": hind, "BSTK100": stocks}
    named = {a: (run_arm(names=const_names[a]) if a in const_names
                 else run_arm(mem=members[a])).assign(arm=a) for a in members}

    # check_c: the fast constant-panel path reproduces the general full-width path exactly
    slow = run_arm(mem=members["STK20"])
    fast = named["STK20"]
    cols = [c for c in slow.columns if c.endswith(("_CAGR", "_Sharpe", "_MaxDD")) or c == "turn"]
    dmax = float((slow[cols].values - fast[cols].values).__abs__().max())
    P(f"  check_c  const-panel path vs full-width path on STK20 (all {len(cols)} stats "
      f"x {len(slow)} rows) : {dmax:.2e}")
    assert dmax < 1e-10
    P("")
    P(f"  running {K_RAND} RAND20 draws x {len(named['STK20'])//len(RUNGS)} grid points x {len(RUNGS)} rungs ...")
    rand_rows = []
    for i, s in enumerate(rand_sets):
        d = run_arm(names=s).assign(arm="RAND20", draw=i)
        rand_rows.append(d)
        if (i + 1) % 50 == 0: print(f"    ... {i+1}/{K_RAND} draws", flush=True)
    rand = pd.concat(rand_rows, ignore_index=True)
    grid = pd.concat(list(named.values()), ignore_index=True)
    grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    rand.to_csv(OUT / f"{STEM}.rand.csv", index=False)

    # ---------------------------------------------------------- 1. every grid point
    P("")
    P("-" * 100)
    P("1. EVERY GRID POINT, EVERY ARM (10 bps; the 0-bps twin is the last column, idea 261)")
    P("-" * 100)
    P(f"{'arm':10s} {'n':>4s} {'g':>5s} {'conv':5s} {'turn/yr':>8s} {'CAGR':>8s} {'Sharpe':>7s} "
      f"{'MaxDD':>8s} {'H1':>7s} {'H2':>7s} {'OOSshp':>7s} {'4a':>3s} {'4b':>3s} {'Shp@0':>7s}")
    def pass4a(r, bps):
        b = ref[("RULESv1", bps)]
        return (r["H1_Sharpe"] > b["H1"]["Sharpe"] and r["H2_Sharpe"] > b["H2"]["Sharpe"]
                and r["FULL_MaxDD"] >= b["FULL"]["MaxDD"])
    def pass4b(r):
        return (r["H1_Sharpe"] > S["H1"]["Sharpe"] and r["H2_Sharpe"] > S["H2"]["Sharpe"]
                and r["OOS_Sharpe"] > S["OOS"]["Sharpe"]
                and abs(r["FULL_MaxDD"]) <= DELTA * abs(S["FULL"]["MaxDD"])
                and r["FULL_CAGR"] >= PHI * S["FULL"]["CAGR"])
    for a in ["STK20", "HIND20", "PITGROW20", "BSTK100"]:
        d = named[a]
        for _, r in d[d.bps == 10].iterrows():
            z = d[(d.bps == 0) & (d.n == r.n) & (d.g == r.g) & (d.conv == r.conv)].iloc[0]
            P(f"{a:10s} {str(r['n']):>4s} {r['g']:5.2f} {r['conv']:5s} {r['turn']:8.2f} "
              f"{r['FULL_CAGR']:8.2%} {r['FULL_Sharpe']:7.4f} {r['FULL_MaxDD']:8.2%} "
              f"{r['H1_Sharpe']:7.4f} {r['H2_Sharpe']:7.4f} {r['OOS_Sharpe']:7.4f} "
              f"{'Y' if pass4a(r,10) else '.':>3s} {'Y' if pass4b(r) else '.':>3s} {z['FULL_Sharpe']:7.4f}")

    grid["p4a"] = [pass4a(r, r["bps"]) for _, r in grid.iterrows()]
    grid["p4b"] = [pass4b(r) for _, r in grid.iterrows()]
    rand["p4a"] = [pass4a(r, r["bps"]) for _, r in rand.iterrows()]
    rand["p4b"] = [pass4b(r) for _, r in rand.iterrows()]

    NPTS = len(named["STK20"]) // len(RUNGS)          # distinct (n, g, conv) grid points
    P("")
    P(f"KEEP-path census ({NPTS*len(RUNGS)} points per named arm = {NPTS} grid x {len(RUNGS)} rungs; "
      f"RAND20 = {K_RAND} draws x {NPTS*len(RUNGS)})")
    for a in ["STK20", "HIND20", "PITGROW20", "BSTK100"]:
        d = grid[grid.arm == a]
        P(f"  {a:10s} 4a {int(d.p4a.sum()):3d}/{len(d):4d}   4b {int(d.p4b.sum()):3d}/{len(d):4d}")
    P(f"  {'RAND20':10s} 4a {int(rand.p4a.sum()):3d}/{len(rand):4d} ({rand.p4a.mean():.1%})"
      f"   4b {int(rand.p4b.sum()):3d}/{len(rand):4d} ({rand.p4b.mean():.1%})   <- NOISE FLOOR")
    dr10 = rand[rand.bps == 10]
    P(f"  RAND20 @10bps: 4b base rate {dr10.p4b.mean():.1%}; draws with >=1 of {NPTS} points passing "
      f"4b: {dr10.groupby('draw').p4b.any().mean():.1%}")

    # ---------------------------------------------------------- 2. STK20 vs the null
    P("")
    P("-" * 100)
    P("2. WHERE STK20 SITS IN THE RAND20 NULL, AND HOW MUCH OF THE HINDSIGHT CEILING IT TAKES")
    P("-" * 100)
    P("   selection share = (STK20 - RAND20 median) / (HIND20 - RAND20 median)")
    P("   1.00 = STK20 is as good as knowing the answer; 0.00 = STK20 is a random 20 of 100")
    P(f"{'n':>4s} {'g':>5s} {'conv':5s} {'win':4s} {'STK20':>8s} {'RANDmed':>8s} {'RANDp90':>8s} "
      f"{'HIND20':>8s} {'PITGRW':>8s} {'pctile':>7s} {'share':>7s}")
    shares = {}
    for _, r in named["STK20"][named["STK20"].bps == 10].iterrows():
        key = (r["n"], r["g"], r["conv"])
        for win in ["FULL", "OOS"]:
            col = f"{win}_Sharpe"
            rs = dr10[(dr10.n == r["n"]) & (dr10.g == r["g"]) & (dr10.conv == r["conv"])][col]
            med, p90 = rs.median(), rs.quantile(0.90)
            hv = named["HIND20"][(named["HIND20"].bps == 10) & (named["HIND20"].n == r["n"]) &
                                 (named["HIND20"].g == r["g"]) & (named["HIND20"].conv == r["conv"])][col].iloc[0]
            pv = named["PITGROW20"][(named["PITGROW20"].bps == 10) & (named["PITGROW20"].n == r["n"]) &
                                    (named["PITGROW20"].g == r["g"]) & (named["PITGROW20"].conv == r["conv"])][col].iloc[0]
            pct = float((rs < r[col]).mean())
            sh = (r[col] - med) / (hv - med) if abs(hv - med) > 1e-9 else np.nan
            shares[(key, win)] = (pct, sh, r[col], med, p90, hv, pv)
            P(f"{str(r['n']):>4s} {r['g']:5.2f} {r['conv']:5s} {win:4s} {r[col]:8.4f} {med:8.4f} "
              f"{p90:8.4f} {hv:8.4f} {pv:8.4f} {pct:7.1%} {sh:7.2f}")
    fs = [v[1] for (k, w), v in shares.items() if w == "FULL"]
    os_ = [v[1] for (k, w), v in shares.items() if w == "OOS"]
    fp = [v[0] for (k, w), v in shares.items() if w == "FULL"]
    op = [v[0] for (k, w), v in shares.items() if w == "OOS"]
    P(f"  MEDIAN over the {len(fp)} grid points -- FULL: percentile {np.median(fp):.1%}, selection share "
      f"{np.median(fs):.2f}   OOS: percentile {np.median(op):.1%}, share {np.median(os_):.2f}")
    P(f"  STK20 beats the RAND20 MEDIAN in {sum(p>0.5 for p in fp)}/{len(fp)} FULL and "
      f"{sum(p>0.5 for p in op)}/{len(op)} OOS points;")
    P(f"  clears the RAND20 90th pctile in {sum(p>=0.90 for p in fp)}/{len(fp)} FULL and "
      f"{sum(p>=0.90 for p in op)}/{len(op)} OOS.")

    # ---------------------------------------------------------- 3. rule 8
    P("")
    P("-" * 100)
    P("3. RULE 8 WALK-FORWARD.  (n, g, conv) chosen on IS <= 2016-12-31 Sharpe @10bps only;")
    P("   2017-01-01.. read ONCE.  RAND20's chooser is run per draw and pooled.")
    P("-" * 100)
    P(f"{'arm':10s} {'pick (n,g,conv)':>20s} {'IS shp':>7s} | {'OOS CAGR':>9s} {'OOS shp':>8s} "
      f"{'OOS MaxDD':>10s} {'turn/yr':>8s} {'vs SPY':>7s} {'vs base':>8s}")
    wf = {}
    for a in ["STK20", "HIND20", "PITGROW20", "BSTK100"]:
        d = named[a][named[a].bps == 10]
        b = d.loc[d.IS_Sharpe.idxmax()]
        wf[a] = b
        P(f"{a:10s} {f'{b[chr(110)]},{b.g:.2f},{b.conv}':>20s} {b['IS_Sharpe']:7.4f} | "
          f"{b['OOS_CAGR']:9.2%} {b['OOS_Sharpe']:8.4f} {b['OOS_MaxDD']:10.2%} {b['turn']:8.2f} "
          f"{b['OOS_Sharpe']-S['OOS']['Sharpe']:+7.4f} "
          f"{b['OOS_Sharpe']-ref[('RULESv1',10)]['OOS']['Sharpe']:+8.4f}")
    picks = dr10.loc[dr10.groupby("draw").IS_Sharpe.idxmax()]
    P(f"{'RAND20':10s} {'(per draw)':>20s} {picks.IS_Sharpe.mean():7.4f} | "
      f"{picks.OOS_CAGR.mean():9.2%} {picks.OOS_Sharpe.mean():8.4f} {picks.OOS_MaxDD.mean():10.2%} "
      f"{picks.turn.mean():8.2f} {picks.OOS_Sharpe.mean()-S['OOS']['Sharpe']:+7.4f} "
      f"{picks.OOS_Sharpe.mean()-ref[('RULESv1',10)]['OOS']['Sharpe']:+8.4f}")
    q = picks.OOS_Sharpe
    P(f"  RAND20 rule-8 OOS Sharpe distribution: p10 {q.quantile(.10):.4f}  med {q.median():.4f}  "
      f"p90 {q.quantile(.90):.4f}  max {q.max():.4f}")
    st = wf["STK20"]
    P(f"  STK20's rule-8 OOS Sharpe {st['OOS_Sharpe']:.4f} sits at the "
      f"{float((q < st['OOS_Sharpe']).mean()):.1%} percentile of the 200 random panels.")
    P(f"  4b on the rule-8 pick: STK20 {'PASS' if pass4b(st) else 'FAIL'}, "
      f"HIND20 {'PASS' if pass4b(wf['HIND20']) else 'FAIL'}, "
      f"PITGROW20 {'PASS' if pass4b(wf['PITGROW20']) else 'FAIL'}, "
      f"BSTK100 {'PASS' if pass4b(wf['BSTK100']) else 'FAIL'}, "
      f"RAND20 {float(np.mean([pass4b(r) for _, r in picks.iterrows()])):.1%} of draws.")

    # ---------------------------------------------------------- 4. idea 10's 5.6x
    P("")
    P("-" * 100)
    P("4. IDEA 10's OWN CONTROL, RE-READ:  STK20 vs BSTK100 at matched (n, g, conv)")
    P("-" * 100)
    for bps in RUNGS:
        a = named["STK20"][named["STK20"].bps == bps].set_index(["n", "g", "conv"])
        b = named["BSTK100"][named["BSTK100"].bps == bps].set_index(["n", "g", "conv"])
        j = a.join(b, lsuffix="_s", rsuffix="_b")
        for w in ["FULL", "OOS"]:
            d = j[f"{w}_Sharpe_s"] - j[f"{w}_Sharpe_b"]
            P(f"  @{bps:2d}bps {w:4s} STK20-BSTK100 dSharpe: mean {d.mean():+.4f} "
              f"median {d.median():+.4f} range {d.min():+.4f}..{d.max():+.4f}  wins {int((d>0).sum())}/{len(d)}")
    a = named["STK20"][named["STK20"].bps == 10].set_index(["n", "g", "conv"])
    p = named["PITGROW20"][named["PITGROW20"].bps == 10].set_index(["n", "g", "conv"])
    j = a.join(p, lsuffix="_s", rsuffix="_p")
    for w in ["FULL", "OOS"]:
        d = j[f"{w}_Sharpe_s"] - j[f"{w}_Sharpe_p"]
        P(f"  @10bps {w:4s} STK20-PITGROW20 dSharpe: mean {d.mean():+.4f} "
          f"range {d.min():+.4f}..{d.max():+.4f}  wins {int((d>0).sum())}/{len(d)}")

    (OUT / f"{STEM}.out.md").write_text("```\n" + "\n".join(_LOG) + "\n```\n")
    P("")
    P(f"wrote {STEM}.grid.csv ({len(grid)} rows), {STEM}.rand.csv ({len(rand)} rows), {STEM}.out.md")


if __name__ == "__main__":
    main()
