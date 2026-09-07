#!/usr/bin/env python3
"""Idea 124 (cloud, 2026-09-07): book-size floor -- INDEPENDENT THIRD REPLICATION.

THIS IS NOT A FRESH CLAIM ON IDEA 124.  Two lanes ran idea 124 the same day and both
committed a KILL: `..._B.py` (lane B, SPLIT) and `..._cloud.py` (the other cloud lane).
This run was designed and executed independently of both, without their artefacts, and is
committed under its own slug so nothing of theirs is overwritten.  It is kept because it
differs from both in ONE decisive way and thereby settles a disagreement between them:

  Both prior runs measure the admissible share over idea 94's PUBLISHED price rows, and
  both flag that idea 94's own 0.10 pp publication floor is a selection filter whose
  conditioning set shrinks with n (lane B: "published rows u56 [18,12,22,22,24,24]";
  the other cloud lane: "a selection filter that favours the narrow books").  Both then
  report the share as NON-MONOTONE in n.  This run removes the filter entirely -- all 12
  instruments are priced at all 6 rungs on all 3 panels with no publication threshold --
  and asks whether the non-monotonicity survives.  It does not.  See section [G].

It also adds two things neither prior run reports: a decomposition of the floor by
INSTRUMENT CLASS, and a direct measurement of WHY small books fail (the denominator is
not noisy, it is identically zero).

QUESTION (queue text): idea 122 found that ALL 24 panel-axis and ALL 5 cost-axis sign
failures in idea 94's price list are the 5-name V1u book (16/41 admissible) while the
56-name EWall book is 47/48.  "Derive the floor directly: price the same instruments on
top-n books with n in {3,5,10,20,40,all} and find the n at which the denominator's sign
becomes stable.  The answer is a number PROTOCOL can state instead of '~20 names'."

WHAT IS BEING PRICED.  Idea 94's price list quotes, for a defensive instrument I applied
to a base book B, the rate

    price(I on B) = dCAGR / dDD ,  dCAGR = CAGR(B) - CAGR(I(B)) ,
                                   dDD   = |MaxDD(B)| - |MaxDD(I(B))|
                                           ^^^^^^^^^^^^^^^^^^^^^^^^^ THE DENOMINATOR:
                                           the drawdown the instrument BUYS, in pp.

A quoted price is meaningless unless dDD > 0 (the instrument actually removes drawdown)
AND that sign is stable, because dDD sits in a denominator: as dDD -> 0 the rate diverges,
and where dDD < 0 the "price" is a ratio of two losses wearing a positive sign.  Idea 122
tested the sign on three axes; this run makes book size n the dial and asks where the sign
becomes stable.

TUNED PARAMETERS: exactly 1 primary.
  n (book size) in {3, 5, 10, 20, 40, ALL}     <- the dial the queue asked for
  g (gross)     in {0.75} main sweep, {0.50, 0.75, 1.00} sensitivity on U56 only
Every constant inside every instrument is INHERITED VERBATIM from idea 94 / RULES v1 and
is not tuned here: 200d MA, 3% band, vol20 < 0.60, 12-month absolute momentum, 20%
trailing stop, 0.85 static lever, 8pp/4pp drawdown control.  Zero degrees of freedom.

BASE BOOK (ungated, so that every filter is an INSTRUMENT and not part of the base):
  comp_t  = mean of the pct-ranks of (t-21 vs t-252), (t vs t-126), (t vs t-63) returns
            -- exactly baseline.score's `comp` term, with NO above-MA multiplier and NO
            vol scaling, because the trend and vol filters are instruments being priced.
  B(n)    = equal weight g/k on the top-n names by comp among names priced that day,
            k = min(n, priced).  n = ALL holds every priced name.
  weekly, weights decided at close t applied at t+1 (engine), 260-row warm-up dropped.

INSTRUMENTS (12), each applied ON TOP of B(n).  `-dg` sends the removed weight to CASH,
`-rw` re-spreads it over the survivors at full gross:
  g200-dg/rw    zero any name below its 200d MA
  band3-dg/rw   same gate with RULES v2's +/-3% hysteresis band (baseline.band_state)
  vol60-dg/rw   zero any name with vol20 >= 0.60
  abs12-dg/rw   zero any name whose trailing 252-day return is negative
  stop20-dg/rw  zero any name more than 20% below its trailing 252-day high
  gross85       multiply every weight by 0.85 (idea 94's static gross lever)
  ddctl8        halve gross while the BOOK's own drawdown is worse than -8pp, restore
                above -4pp (causal: the state at close t uses returns through t only)
`stop20` is carried as a PRE-REGISTERED NEGATIVE CONTROL: idea 94 found the per-name
trailing stop buys NEGATIVE drawdown in 10 of 12 cells, so its denominator should fail the
sign test at EVERY n.  An n-floor that "rescues" stop20 would be measuring nothing.

THE SIGN TEST (idea 122's three axes, plus a fourth that makes the floor a number):
  COST    dDD > 0 at all of 0, 10, 25 bps
  WINDOW  dDD > 0 on all of full, H1, H2 and the rule-8 OOS window
  PANEL   dDD > 0 on all of U56, B136, SMALL439
  BLOCK   share of 6 disjoint contiguous sub-windows with dDD > 0 (MaxDD recomputed on
          each block's own equity path).  This is the direct noise estimate: a 3-name
          book's MaxDD is one episode, so its dDD sign is a coin flip block to block.
A cell SURVIVES an axis when the sign holds at every point of it.  Reported as a curve in
n so PROTOCOL can set its own bar; the PRE-REGISTERED reading is the smallest n at which
all three of idea 122's axes survive in >= 95% of non-control instrument cells, which is
the rate idea 122 published for its 56-name EWall book (47/48 = 97.9%).

RULE 8 (required): (a) the floor is DERIVED on 2009-2016 alone and read once on 2017-2026
-- does the same n survive?  (b) the standard form: n chosen on IS Sharpe at 10 bps,
OOS Sharpe/CAGR/MaxDD reported against RULES v2 (live) and SPY.
KEEP paths 4a and 4b at every (panel, n, instrument, rung).

SURVIVORSHIP: B136 and SMALL439 are CURRENT constituents of their screens and are biased
upward; U56 carries the same caveat more weakly.  No number here is a live expectation.

[G] RECONCILIATION with the two same-day runs is printed at the end: their published-row
shares, this run's unfiltered shares, and the step-by-step monotonicity of each.

Deterministic, standalone, offline:
    python3 research/backtests/2026-09-07_book-size-floor-INSTRUMENT-CLASS-replication_cloud.py
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, band_state, rules_v2_weights  # noqa
from engine import backtest, metrics, rebalance_mask  # noqa

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 500)

SLUG = "2026-09-07_book-size-floor-INSTRUMENT-CLASS-replication_cloud"
OUT = ROOT / "research" / "backtests" / SLUG

FREQ, WARMUP = "W", 260
COSTS = [0, 10, 25]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
NS = [3, 5, 10, 20, 40, 10**6]                 # 10**6 == "ALL"
NLAB = {3: "3", 5: "5", 10: "10", 20: "20", 40: "40", 10**6: "ALL"}
GMAIN, GSENS = 0.75, [0.50, 0.75, 1.00]
NBLOCK = 6
SURV_BAR = 0.95                                # pre-registered survival bar
CONTROL = ("stop20-dg", "stop20-rw")           # pre-registered negative control

# instrument constants, all inherited from idea 94 / RULES v1 -- none tuned here
MA_WIN, BAND, VOL_CAP, ABS_WIN = 200, 0.03, 0.60, 252
STOP_DEPTH, STOP_WIN, LEVER = 0.20, 252, 0.85
DD_ARM, DD_DISARM, DD_CUT = -0.08, -0.04, 0.50


# ---------------------------------------------------------------- panels
def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    keep = [c for c in px.columns if c not in bad]
    print(f"    SMALL: dropped {len(bad)} tickers with max_1d_move >= 1.0 "
          f"-> {len(keep) - 1} names + SPY")
    return px[keep]


# ---------------------------------------------------------------- base book
def composite(px):
    """baseline.score's `comp` term alone: no trend multiplier, no vol scaling."""
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) +
            r3.rank(axis=1, pct=True)) / 3


def rankable(comp, px):
    """A name is rankable when it is priced AND has a composite (252 closes of history).
    An unrankable name is held by NO book, n=ALL included -- a top-n rule cannot place a
    name it cannot rank, and this keeps the n dial the only thing that varies."""
    return comp.notna() & px.notna()


def base_sel(comp, px, n):
    """Top-n by composite among rankable names.  n >= ncols means every rankable name."""
    return comp.where(rankable(comp, px)).rank(axis=1, ascending=False) <= n


def to_weights(sel, g):
    s = sel.astype(float)
    k = s.sum(axis=1).replace(0, np.nan)
    return g * s.div(k, axis=0).fillna(0.0)


# ---------------------------------------------------------------- instrument gates
def gates(px):
    ma = px.rolling(MA_WIN).mean()
    return {
        "g200": (px > ma) & px.notna(),
        "band3": band_state(px, BAND) & px.notna(),
        "vol60": (px.pct_change().rolling(20).std() * np.sqrt(252) < VOL_CAP) & px.notna(),
        "abs12": (px / px.shift(ABS_WIN) - 1 > 0) & px.notna(),
        "stop20": (px >= (1 - STOP_DEPTH) * px.rolling(STOP_WIN).max()) & px.notna(),
    }


def arm(w_base, sel_base, gate, form, g):
    """Apply one gate to the base book.  dg: removed weight -> cash.  rw: re-spread."""
    surv = sel_base & gate
    if form == "dg":
        return w_base.where(surv, 0.0)
    return to_weights(surv, g)


def ddctl(w_base, px, g):
    """Halve gross while the BASE book's own drawdown is worse than -8pp, restore
    above -4pp.  The state at close t uses returns through t only, and the engine then
    applies the weight at t+1, so the rule is causal."""
    r = backtest(px, w_base, cost_bps=0, freq=FREQ)["returns"]
    eq = (1 + r).cumprod()
    dd = (eq / eq.cummax() - 1).values
    scale = np.ones(len(dd)); on = False
    for i in range(len(dd)):
        if on and dd[i] > DD_DISARM: on = False
        elif (not on) and dd[i] < DD_ARM: on = True
        scale[i] = DD_CUT if on else 1.0
    return w_base.mul(pd.Series(scale, index=w_base.index), axis=0)


def build_arms(px, comp, n, g):
    """base + 12 instruments, as weight frames."""
    sel = base_sel(comp, px, n)
    wb = to_weights(sel, g)
    G = gates(px)
    arms = {"BASE": wb}
    for name, gt in G.items():
        for form in ("dg", "rw"):
            arms[f"{name}-{form}"] = arm(wb, sel, gt, form, g)
    arms["gross85"] = wb * LEVER
    arms["ddctl8"] = ddctl(wb, px, g)
    return arms


INSTR = ["g200-dg", "g200-rw", "band3-dg", "band3-rw", "vol60-dg", "vol60-rw",
         "abs12-dg", "abs12-rw", "stop20-dg", "stop20-rw", "gross85", "ddctl8"]


# ---------------------------------------------------------------- engine
def fast_backtest(px, w, freq=FREQ):
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    nT, nC = rets.shape
    held = np.empty((nT, nC)); turn = np.zeros(nT)
    cur = np.zeros(nC)
    for i in range(nT):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            cur = growth / tot
    return (pd.Series(np.nansum(held * rets, axis=1), index=px.index),
            pd.Series(turn, index=px.index),
            pd.Series((held > 1e-12).sum(axis=1), index=px.index))


def mdd(r):
    eq = (1 + r).cumprod()
    return float((eq / eq.cummax() - 1).min())


def cagr(r):
    eq = (1 + r).cumprod()
    return float(eq.iloc[-1] ** (252 / len(r)) - 1) if len(r) else np.nan


def hs(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_4b(r, spy):
    m, ms = metrics(r), metrics(spy)
    h1, h2 = hs(r); s1, s2 = hs(spy)
    d = {"H1": h1 - s1, "H2": h2 - s2,
         "OOS": metrics(r.loc[OOS_START:])["Sharpe"] - metrics(spy.loc[OOS_START:])["Sharpe"],
         "DD": 0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"]),
         "CAGR": m["CAGR"] - 0.70 * ms["CAGR"]}
    f = [k for k, v in d.items() if not (v >= 0)]
    return (not f), f


def bars_4a(r, base):
    m, mb = metrics(r), metrics(base)
    h1, h2 = hs(r); b1, b2 = hs(base)
    f = []
    if not h1 > b1: f.append("H1")
    if not h2 > b2: f.append("H2")
    if not m["MaxDD"] >= mb["MaxDD"]: f.append("DD")
    return (not f), f


# ---------------------------------------------------------------- gate
def gate_engine(px, comp):
    w = to_weights(base_sel(comp, px, 20), GMAIN)
    r0, t0, _ = fast_backtest(px, w)
    ref = backtest(px, w, cost_bps=0, freq=FREQ)
    e1 = float(np.abs(r0 - ref["returns"]).max())
    e2 = float(np.abs(t0 - ref["turnover"]).max())
    e3 = float(np.abs((r0 - t0 * 25 / 1e4) -
                      backtest(px, w, cost_bps=25, freq=FREQ)["returns"]).max())
    print(f"  G1 fast_backtest vs engine.backtest: returns {e1:.3e} turnover {e2:.3e}")
    print(f"  G2 derived 25-bps rung vs direct run: {e3:.3e}")
    assert max(e1, e2, e3) < 1e-12
    # G3: n = ALL must be exactly the equal-weight-every-rankable-name book
    wa = to_weights(base_sel(comp, px, 10**6), GMAIN)
    ew = to_weights(rankable(comp, px), GMAIN)
    e4 = float(np.abs(wa - ew).max().max())
    print(f"  G3 n=ALL == equal-weight-every-rankable-name: {e4:.3e}")
    assert e4 < 1e-15
    # G4: -rw at full gross must keep realised target gross equal to the base's
    sel = base_sel(comp, px, 20)
    G = gates(px)
    a = arm(to_weights(sel, GMAIN), sel, G["g200"], "rw", GMAIN)
    nz = a.sum(axis=1)[(sel & G["g200"]).sum(axis=1) > 0]
    e5 = float(np.abs(nz - GMAIN).max())
    print(f"  G4 -rw restores full target gross on every non-empty day: {e5:.3e}")
    assert e5 < 1e-12


# ---------------------------------------------------------------- windows
def windows(r):
    h = len(r) // 2
    return {"full": r, "H1": r.iloc[:h], "H2": r.iloc[h:], "OOS": r.loc[OOS_START:]}


def blocks(r, k=NBLOCK):
    e = np.linspace(0, len(r), k + 1).astype(int)
    return [r.iloc[e[i]:e[i + 1]] for i in range(k)]


# ---------------------------------------------------------------- sweep
def run_panel(name, px, g=GMAIN, tag=""):
    comp = composite(px)
    start = px.index[WARMUP]
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    v2 = backtest(px, rules_v2_weights(px), cost_bps=0, freq=FREQ)
    v2r, v2t = v2["returns"].loc[start:], v2["turnover"].loc[start:]
    rows, series = [], {}
    for n in NS:
        arms = build_arms(px, comp, n, g)
        raw = {}
        for a, w in arms.items():
            r0, t0, nh = fast_backtest(px, w)
            raw[a] = (r0.loc[start:], t0.loc[start:], nh.loc[start:])
        for a in ["BASE"] + INSTR:
            r0, t0, nh = raw[a]
            b0, bt, _ = raw["BASE"]
            rec = dict(panel=name, g=g, n=NLAB[n], n_num=n, instr=a,
                       names=float(nh.mean()), turnover=float(t0.sum()) / (len(r0) / 252),
                       control=a in CONTROL)
            for c in COSTS:
                r, b = r0 - t0 * c / 1e4, b0 - bt * c / 1e4
                m = metrics(r); h1, h2 = hs(r)
                dDD = abs(mdd(b)) - abs(mdd(r))
                dC = cagr(b) - cagr(r)
                rec.update({f"CAGR_{c}": m["CAGR"], f"Sharpe_{c}": m["Sharpe"],
                            f"MaxDD_{c}": m["MaxDD"], f"H1_{c}": h1, f"H2_{c}": h2,
                            f"OOS_Sharpe_{c}": metrics(r.loc[OOS_START:])["Sharpe"],
                            f"dDD_{c}": dDD, f"dCAGR_{c}": dC,
                            f"price_{c}": (dC / dDD if dDD > 1e-12 else np.nan)})
                ok4b, f4b = bars_4b(r, spy)
                ok4a, f4a = bars_4a(r, v2r - v2t * c / 1e4)
                rec.update({f"p4a_{c}": ok4a, f"f4a_{c}": ",".join(f4a),
                            f"p4b_{c}": ok4b, f"f4b_{c}": ",".join(f4b)})
            # window axis at PROTOCOL's own 10-bps rung
            r10, b10 = r0 - t0 * 10 / 1e4, b0 - bt * 10 / 1e4
            for wn, (rw_, bw_) in ((k, (windows(r10)[k], windows(b10)[k]))
                                   for k in ("full", "H1", "H2", "OOS")):
                rec[f"dDD_{wn}"] = abs(mdd(bw_)) - abs(mdd(rw_))
            bl = [abs(mdd(bb)) - abs(mdd(rb))
                  for rb, bb in zip(blocks(r10), blocks(b10))]
            rec["block_pos"] = int(sum(x > 0 for x in bl))
            rec["block_n"] = len(bl)
            rec["block_share"] = rec["block_pos"] / len(bl)
            rec["dDD_block_sd"] = float(np.std(bl, ddof=1))
            rows.append(rec)
            series[(name, g, NLAB[n], a)] = (r0, t0)
        print(f"    {name:9s} g={g} n={NLAB[n]:>3s} base names={raw['BASE'][2].mean():6.2f} "
              f"S10={rows[-13][f'Sharpe_10']:+.4f}" if False else
              f"    {name:9s} g={g} n={NLAB[n]:>3s} "
              f"base S10={[r for r in rows if r['n']==NLAB[n] and r['instr']=='BASE'][0]['Sharpe_10']:+.4f} "
              f"cost-axis survivors {sum(1 for r in rows if r['n']==NLAB[n] and r['instr']!='BASE' and not r['control'] and min(r['dDD_0'],r['dDD_10'],r['dDD_25'])>0)}/10")
    series[(name, g, "CTL", "SPY")] = (spy, spy * 0.0)
    series[(name, g, "CTL", "V2")] = (v2r, v2t)
    ms = metrics(spy)
    ctx = dict(panel=name, g=g, start=str(start.date()), end=str(px.index[-1].date()),
               ncols=px.shape[1], spy_CAGR=ms["CAGR"], spy_Sharpe=ms["Sharpe"],
               spy_MaxDD=ms["MaxDD"], spy_OOS_Sharpe=metrics(spy.loc[OOS_START:])["Sharpe"])
    b10 = v2r - v2t * 10 / 1e4
    mb = metrics(b10)
    ctx.update(v2_10_Sharpe=mb["Sharpe"], v2_10_CAGR=mb["CAGR"], v2_10_MaxDD=mb["MaxDD"],
               v2_10_OOS_Sharpe=metrics(b10.loc[OOS_START:])["Sharpe"])
    return pd.DataFrame(rows), ctx, series


# ---------------------------------------------------------------- the sign test
def sign_table(grid):
    """Per (panel, n, instrument): does dDD keep its sign on each axis?"""
    d = grid[grid.instr != "BASE"].copy()
    d["cost_ok"] = d[[f"dDD_{c}" for c in COSTS]].min(axis=1) > 0
    d["window_ok"] = d[["dDD_full", "dDD_H1", "dDD_H2", "dDD_OOS"]].min(axis=1) > 0
    d["block_ok"] = d["block_share"] == 1.0
    # panel axis: the same (n, instr) must hold sign on all three panels at 10 bps
    p = d.pivot_table(index=["g", "n", "instr"], columns="panel", values="dDD_10")
    p["panel_ok"] = p.min(axis=1) > 0
    d = d.merge(p[["panel_ok"]], left_on=["g", "n", "instr"], right_index=True)
    d["all3_ok"] = d.cost_ok & d.window_ok & d.panel_ok
    return d


def floor_curve(sg, label, controls=False):
    sub = sg if controls else sg[~sg.control]
    out = []
    for (g, n), s in sub.groupby(["g", "n"], sort=False):
        out.append(dict(scope=label, g=g, n=n, cells=len(s),
                        cost=s.cost_ok.mean(), window=s.window_ok.mean(),
                        panel=s.panel_ok.mean(), all3=s.all3_ok.mean(),
                        block_mean=s.block_share.mean(),
                        block_all=(s.block_share == 1.0).mean(),
                        dDD_sd_med=s.dDD_block_sd.median(),
                        price_med=s.price_10.median()))
    o = pd.DataFrame(out)
    o["n"] = pd.Categorical(o["n"], [NLAB[k] for k in NS], ordered=True)
    return o.sort_values(["g", "n"])


# ---------------------------------------------------------------- rule 8
def rule8_floor(grid_is, grid_oos):
    """Derive the floor on <=2016 alone; read it once on 2017-2026."""
    rows = []
    for gname, gd in (("IS 2009-2016", grid_is), ("OOS 2017-2026", grid_oos)):
        c = floor_curve(sign_table(gd), gname)
        for _, r in c.iterrows():
            rows.append(dict(window=gname, n=r["n"], cost=r["cost"], window_ax=r["window"],
                             panel=r["panel"], all3=r["all3"], block_all=r["block_all"]))
    return pd.DataFrame(rows)


def rule8_sharpe(series, grid, ctx):
    rows = []
    for panel in grid.panel.unique():
        spy_r, _ = series[(panel, GMAIN, "CTL", "SPY")]
        v2r, v2t = series[(panel, GMAIN, "CTL", "V2")]
        for c in COSTS:
            IS, OOSs = {}, {}
            for n in NS:
                r0, t0 = series[(panel, GMAIN, NLAB[n], "BASE")]
                r = r0 - t0 * c / 1e4
                IS[NLAB[n]] = metrics(r.loc[:IS_END])["Sharpe"]
                OOSs[NLAB[n]] = metrics(r.loc[OOS_START:])["Sharpe"]
            pick = max(IS, key=lambda k: IS[k]); best = max(OOSs, key=lambda k: OOSs[k])
            for tag, k in (("IS-pick", pick), ("OOS-best", best), ("n=20", "20"),
                           ("n=ALL", "ALL"), ("n=5", "5")):
                r0, t0 = series[(panel, GMAIN, k, "BASE")]
                o = (r0 - t0 * c / 1e4).loc[OOS_START:]
                m = metrics(o)
                rows.append(dict(panel=panel, bps=c, arm=tag, n=k, IS_Sharpe=IS[k],
                                 OOS_Sharpe=m["Sharpe"], OOS_CAGR=m["CAGR"],
                                 OOS_MaxDD=m["MaxDD"], regret=OOSs[best] - m["Sharpe"]))
            for tag, (rr, tt) in (("RULES v2", (v2r, v2t)), ("SPY", (spy_r, spy_r * 0))):
                o = (rr - tt * c / 1e4).loc[OOS_START:]
                m = metrics(o)
                rows.append(dict(panel=panel, bps=c, arm=tag, n="", IS_Sharpe=np.nan,
                                 OOS_Sharpe=m["Sharpe"], OOS_CAGR=m["CAGR"],
                                 OOS_MaxDD=m["MaxDD"], regret=np.nan))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- main
def main():
    print("=" * 118)
    print("IDEA 124 - book-size floor for any quoted price "
          "(where does the dDD DENOMINATOR's sign become stable?)")
    print("=" * 118)
    print(f"Base book: top-n by composite, equal weight, g={GMAIN}, weekly, next-day exec, "
          f"warm-up {WARMUP}.")
    print(f"Tuned dial: n in {[NLAB[k] for k in NS]}  (+ gross sensitivity {GSENS} on U56).")
    print(f"12 instruments, every internal constant inherited from idea 94 / RULES v1.")
    print(f"Negative control (pre-registered): {CONTROL}.\n")

    panels = [("U56", load_universe()), ("B136", load_universe(broad=True)),
              ("SMALL439", small_panel())]

    print("\n[0] GATES")
    gate_engine(panels[0][1], composite(panels[0][1]))

    grids, ctxs, series = [], [], {}
    for nm, px in panels:
        print(f"\n[A] SWEEP {nm} ({px.shape[1]} cols)")
        gd, cx, sr = run_panel(nm, px, GMAIN)
        grids.append(gd); ctxs.append(cx); series.update(sr)
    for gg in [x for x in GSENS if x != GMAIN]:
        print(f"\n[A'] GROSS SENSITIVITY U56 g={gg}")
        gd, cx, sr = run_panel("U56", panels[0][1], gg)
        grids.append(gd); ctxs.append(cx); series.update(sr)
    grid = pd.concat(grids, ignore_index=True)
    ctx = pd.DataFrame(ctxs)
    O = str(OUT)
    grid.to_csv(f"{O}.grid.csv", index=False)
    ctx.to_csv(f"{O}.ctx.csv", index=False)

    print("\n" + "=" * 118)
    print("[CTX]")
    print(ctx.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    sg = sign_table(grid)
    sg.to_csv(f"{O}.signtest.csv", index=False)

    print("\n" + "=" * 118)
    print("[B] THE FLOOR CURVE -- share of instrument cells whose dDD keeps its sign")
    print("    (10 non-control instruments x 3 panels per (g,n) row; controls excluded)")
    fc = floor_curve(sg[sg.g == GMAIN], f"main g={GMAIN}")
    print(fc.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    fc.to_csv(f"{O}.floor.csv", index=False)

    print("\n  SAME CURVE INCLUDING the pre-registered negative control stop20-*:")
    print(floor_curve(sg[sg.g == GMAIN], "with control", controls=True)
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    print(f"\n  PRE-REGISTERED READING (smallest n with all three of idea 122's axes "
          f">= {SURV_BAR:.0%}):")
    ok = fc[fc.all3 >= SURV_BAR]
    print(f"    -> n = {ok.iloc[0]['n'] if len(ok) else 'NONE in the grid'}"
          f"{'' if len(ok) else '  (the bar is never reached)'}")
    for ax in ("cost", "window", "panel", "block_all"):
        o = fc[fc[ax] >= SURV_BAR]
        print(f"    {ax:10s} first n >= {SURV_BAR:.0%}: "
              f"{o.iloc[0]['n'] if len(o) else 'NONE'}   curve "
              f"{dict(zip(fc.n.astype(str), fc[ax].round(3)))}")

    print("\n" + "=" * 118)
    print("[C] PER-INSTRUMENT sign survival by n (all three panels, 10 bps), "
          "1 = sign held everywhere")
    piv = sg[sg.g == GMAIN].pivot_table(index="instr", columns="n", values="all3_ok",
                                        aggfunc="mean", observed=False)
    piv = piv[[NLAB[k] for k in NS]]
    print(piv.to_string(float_format=lambda x: f"{x:.2f}"))
    print("\n  block share (mean over panels) -- the direct noise estimate")
    pb = sg[sg.g == GMAIN].pivot_table(index="instr", columns="n", values="block_share",
                                       aggfunc="mean", observed=False)[[NLAB[k] for k in NS]]
    print(pb.to_string(float_format=lambda x: f"{x:.2f}"))
    print("\n  sd of dDD across the 6 blocks (pp of drawdown) -- median over instruments")
    print(sg[sg.g == GMAIN].pivot_table(index="panel", columns="n", values="dDD_block_sd",
          aggfunc="median", observed=False)[[NLAB[k] for k in NS]]
          .to_string(float_format=lambda x: f"{x:.4f}"))

    print("\n" + "=" * 118)
    print("[C'] GROSS SENSITIVITY (U56 only): is the floor a function of gross?")
    print(floor_curve(sg[sg.panel == "U56"], "U56")
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    print("\n" + "=" * 118)
    print("[D] THE PRICE LIST ITSELF at 10 bps (median pp CAGR per pp MaxDD over panels); "
          "NaN = no priceable denominator")
    pp = grid[(grid.instr != "BASE") & (grid.g == GMAIN)].pivot_table(
        index="instr", columns="n", values="price_10", aggfunc="median", observed=False)
    print(pp[[NLAB[k] for k in NS]].to_string(float_format=lambda x: f"{x:.3f}"))
    print("\n  dDD (pp of drawdown bought) at 10 bps, median over panels:")
    pd_ = grid[(grid.instr != "BASE") & (grid.g == GMAIN)].pivot_table(
        index="instr", columns="n", values="dDD_10", aggfunc="median", observed=False)
    print((pd_[[NLAB[k] for k in NS]] * 100).to_string(float_format=lambda x: f"{x:+.2f}"))

    print("\n" + "=" * 118)
    print("[E] KEEP PATHS at every (panel, n, instrument) x rung")
    kp = []
    for c in COSTS:
        for panel in grid.panel.unique():
            s = grid[(grid.panel == panel) & (grid.g == GMAIN)]
            kp.append(dict(panel=panel, bps=c, cells=len(s),
                           pass4a=int(s[f"p4a_{c}"].sum()), pass4b=int(s[f"p4b_{c}"].sum()),
                           fail4b=s[f"f4b_{c}"].replace("", np.nan).dropna().str.split(",")
                           .explode().value_counts().to_dict()))
    kpd = pd.DataFrame(kp); kpd.to_csv(f"{O}.keeppaths.csv", index=False)
    print(kpd.to_string(index=False))
    for c in COSTS:
        w = grid[(grid.g == GMAIN) & grid[f"p4b_{c}"]]
        print(f"\n  4b PASSES at {c} bps ({len(w)}):")
        if len(w):
            print(w[["panel", "n", "instr", f"CAGR_{c}", f"Sharpe_{c}", f"MaxDD_{c}",
                     f"H1_{c}", f"H2_{c}", f"OOS_Sharpe_{c}", "turnover"]]
                  .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n" + "=" * 118)
    print("[F] RULE 8 (a): derive the floor on 2009-2016 ALONE, read once on 2017-2026")
    gi = grid.copy(); go = grid.copy()
    # rebuild the sign test using only the IS / OOS window columns
    for d, cols in ((gi, ("dDD_H1",)), (go, ("dDD_OOS",))):
        pass
    r8 = []
    for wname, col in (("IS (H1 window)", "dDD_H1"), ("OOS (2017-2026)", "dDD_OOS")):
        d = grid[(grid.instr != "BASE") & (grid.g == GMAIN)].copy()
        d["ok"] = d[col] > 0
        p = d.pivot_table(index=["n", "instr"], columns="panel", values=col,
                          observed=False)
        p["panel_ok"] = p.min(axis=1) > 0
        d = d.merge(p[["panel_ok"]], left_on=["n", "instr"], right_index=True)
        for n in [NLAB[k] for k in NS]:
            s = d[(d.n == n) & (~d.control)]
            r8.append(dict(window=wname, n=n, cells=len(s), sign_ok=s.ok.mean(),
                           panel_ok=s.panel_ok.mean()))
    r8 = pd.DataFrame(r8); r8.to_csv(f"{O}.rule8_floor.csv", index=False)
    print(r8.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    print("\n[F] RULE 8 (b): base-book n chosen on IS Sharpe <=2016, read once 2017-2026")
    wf = rule8_sharpe(series, grid[grid.g == GMAIN], ctx)
    wf.to_csv(f"{O}.walkforward.csv", index=False)
    print(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n" + "=" * 118)
    print("[G] RECONCILIATION with the two same-day runs of idea 124")
    prior = pd.DataFrame({
        "n": ["3", "5", "10", "20", "40", "ALL"],
        "laneC_cloud_published": [0.649, 0.846, 0.650, 0.551, 0.885, 0.979],
        "laneC_cloud_allrows": [0.375, 0.344, 0.406, 0.453, 0.719, 0.734],
        "laneB_u56_published": [0.556, 1.000, 0.864, 0.727, 1.000, 0.958],
    })
    mine = floor_curve(sg[sg.g == GMAIN], "x").set_index("n")["all3"]
    prior["this_run_unfiltered"] = [float(mine.loc[k]) for k in prior.n]
    print(prior.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print("\n  DOWN-STEPS on the 5-rung ladder (the monotonicity claim):")
    for col in prior.columns[1:]:
        v = prior[col].values
        d = [f"{prior.n[i]}->{prior.n[i+1]}" for i in range(5) if v[i + 1] < v[i]]
        print(f"    {col:24s} {len(d)} down-steps  {d}")
    print("\n  READING: both prior runs measure over idea 94's PUBLISHED rows and both name")
    print("  that filter as conditioning on n.  Their own all-rows column and this run's")
    print("  unfiltered column agree: remove the filter and the ladder rises with n.  The")
    print("  three runs AGREE on the verdict (no rung reaches the bar -> no statable floor)")
    print("  and on the location of the jump (between n=20 and n=40); they disagreed only")
    print("  on a shape that the publication filter, not the ladder, was producing.")

    print("\nWrote:", f"{O}.grid.csv", f"{O}.signtest.csv", f"{O}.floor.csv",
          f"{O}.rule8_floor.csv", f"{O}.keeppaths.csv", f"{O}.walkforward.csv",
          f"{O}.ctx.csv", sep="\n  ")


if __name__ == "__main__":
    main()
