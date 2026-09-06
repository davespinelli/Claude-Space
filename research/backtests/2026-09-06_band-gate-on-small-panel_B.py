#!/usr/bin/env python3
"""QUEUE idea 60 — band-gate-on-small-panel (lane B, 2026-09-06).

Question (verbatim from QUEUE)
-----------------------------
"ideas 49/39/38 found the 200d gate is *inverted* on the 439-name small-cap panel, costing
5.4pp/yr at zero cost, and idea 52 hypothesised whipsaw as the mechanism. Idea 57 has now
demonstrated whipsaw on large caps and measured its price (7.55 vs 1.77 flips/ticker/yr).
Re-run the ew-all book with the 3% band on the small panel: if whipsaw is the mechanism, the
band should recover a large part of the 5.4pp. Answers idea 52 directly."

What is on trial.  Not a book — no small-panel book has ever passed anything (idea 121: 0 of
192).  The claim under test is a MECHANISM: that the sub-$2B panel's inverted trend gate is a
*trading* artefact (the gate flips too often and sells the bottom) rather than a *signal*
artefact (trend simply does not predict on these names).  The two hypotheses make different
predictions about the shape of the band-width curve, and that shape is the answer:

    WHIPSAW  : damage is caused by crossings that are noise.  A band wide enough to swallow
               the noise removes most of the damage and then STOPS helping — the recovery
               curve SATURATES at a modest width.
    NO-SIGNAL: the gate destroys value on every crossing, noisy or not.  Then the only way to
               stop losing is to stop gating, so the recovery curve is MONOTONE all the way to
               the widest band (b -> large is the un-gated book) and does NOT saturate.

So the discriminator is pre-registered as *saturation*, not as level.

PRE-REGISTERED PREDICTIONS (fixed before any new number below was read)
----------------------------------------------------------------------
P1  REPRODUCTION.  The published zero-cost gate damage reproduces.  Two published anchors:
    idea 49's -5.4 pp/yr, and idea 121's exact re-measurement of the same contrast at 10 bps,
    floor $0, g=0.75, gross-matched: dCAGR -6.515 pp, dSharpe -0.3420, dMaxDD -3.814 pp,
    mean names 347.91 (all) / 141.26 (gated).  P1 holds if the 10 bps cell matches idea 121
    to <0.05 pp / <0.005 Sharpe.
P2  THE QUEUE'S HYPOTHESIS.  band3 recovers "a large part" of the zero-cost damage.  Read as
    >= 50% of the damage closed, at floor $0, g=0.75, gross-matched, 0 bps, and judged on the
    MOST GENEROUS of three readings (Q4): the published EWall-vs-full-gate gap, the trend
    half's own gap inside the full gate, and the trend half's gap with no vol filter at all.
P3  MECHANISM PRESENT.  The small panel's bare-200d flip rate exceeds the large-cap panel's
    (idea 4/57 published 7.55 on U56; idea 61 re-derived 7.44).  If the small panel does not
    flip more, whipsaw cannot be the differentiating mechanism at all.
P4  THE DISCRIMINATOR (saturation).  Under WHIPSAW, recovery saturates: the b=0.03 -> b=0.20
    increment is < 25% of the b=0.00 -> b=0.03 increment, on every reading.  Under NO-SIGNAL
    it does not.
P5  NO BOOK PASSES.  Consistent with idea 121 (0/192) and idea 61 (4b 41/408, none a rule-8
    pick), no arm on this panel clears 4b, and rule-8 picks lose to SPY out of sample.

CORRECTION MADE DURING THE RUN (disclosed because it touches a pre-registered number).  The
first execution measured P2's "damage" as NOGATE-minus-200d *inside* comp=FULL, which leaves
the vol20 half in both legs and so is NOT the -5.4 pp the queue quotes.  Q4 was rewritten to
report all three readings and to judge P2 on the LARGEST of them.  The correction is strictly
favourable to the hypothesis — it can only make P2 easier to pass — so it cannot manufacture a
KILL.  P1's published-damage comparand was fixed in the same edit; nothing else moved, and the
28-cell cross-run gate against idea 61 is unchanged at 5.6e-17.

DISCLOSURE.  Before writing these predictions I read idea 61's committed
`.grid.csv` rows for (SMALL439, ew-all, BAND) at 10 and 25 bps, which already contain the
trend-only, floor-$0 slice of this run.  Those rows are therefore used as a REPRODUCTION GATE
(Q1[e]) and not as a discovery; P2/P4 are stated on the 0 bps FULL-gate cell that idea 61
does not contain, and P4's saturation reading is new.

Design (PROTOCOL rules 1-9)
---------------------------
Panels    SMALL439 — data/prices_small.csv.gz minus the 44 names with `max_1d_move >= 1.0`
                     in data/small_meta.csv (idea 121/61's mandatory screen), = 439 tradable
                     names + SPY as a BENCHMARK COLUMN that is never selectable.
          U56      — research/universe.json via load_universe(), the large-cap mirror idea 57
                     measured on, so the flip-rate contrast is like-for-like.
          SURVIVORSHIP: both panels are CURRENT constituents.  On the small panel the missing
          cohort (delisted / bankrupt 2010-2025) is concentrated in exactly the thin, noisy
          names this run's gate arms disagree about, so absolute levels are uninterpretable
          and only the ARM-MINUS-ARM contrasts (same names, same days) are read.
Book      `ew-all` at gross 0.75 — the idea's own book, and the control idea 49 measured the
          inversion on.  No ranking, no position count.
Convention Reported at BOTH, selected at neither:
          `rw`  gated-out weight re-spread over survivors, gross pinned at 0.75.  This is the
                convention idea 49's -5.4 pp and idea 121's -6.515 pp were measured under.
          `dg`  gated-out weight to CASH, gross floats down with the gate.  This is live
                RULES v2's own convention.
Composition Reported at BOTH:  `TREND` = trend arm only;  `FULL` = trend arm AND vol20 < 0.60
          (RULES v1's eligibility filter, the object of idea 49's claim).
Arms      NOGATE, 200d, band2, band3, band5, band8, band12, band20, and 200d-M (the 200d gate
          re-evaluated on month-ends and held constant in between — idea 57's other cheap
          instrument).  Band = hysteresis: IN above ma200*(1+b), OUT below ma200*(1-b),
          previous state in between, OUT before 200 closes exist.
Floors    ADV floor on the small panel: $0 and $1M, where $1M is idea 121's proposed PROTOCOL
          clause.  L_t = 20-day rolling MEDIAN of close x share volume, point-in-time.
          Reported at both, selected at neither.
Costs     0 / 5 / 10 / 25 bps per unit turnover.  0 bps is where the queue's claim lives;
          10 bps is PROTOCOL rule 2 and is where the 4a/4b verdicts are read.  Costs are
          applied analytically (net = gross - turnover * bps/1e4), which is an identity for
          engine.backtest because `held` and `turnover` do not depend on cost_bps; Q1[a]
          asserts it.
Execution Weekly, weights decided at close t applied at t+1, long only, no leverage.
Tuned     EXACTLY TWO: instrument family (BAND vs STALE) and its dial (band width b / the
          month-end stale flag).  Panel, floor, convention, composition and cost rung are
          reported at every value with no selection over them.
Rule 8    Band width chosen on 2010..2016 ONLY, by two selection rules fixed in advance
          (IS Sharpe argmax; IS dCAGR-vs-NOGATE argmax), evaluated untouched on 2017..2026
          against SPY, against the live RULES v2 book, and against DO-NOTHING (NOGATE) and
          the pre-registered constant b=0.03.

Outputs: .console.txt, .grid.csv, .decomp.csv, .curve.csv, .flips.csv, .walkforward.csv,
         .verdicts.csv, .result.md
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "research" / "backtests"
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, load_volume, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-06_band-gate-on-small-panel_B"
FREQ, GROSS, MAX_VOL = "W", 0.75, 0.60
COSTS = [0, 5, 10, 25]
PROTO_COST = 10
FLOORS = [0.0, 1e6]
ARMS = ["NOGATE", "200d", "band2", "band3", "band5", "band8", "band12", "band20", "200d-M"]
BAND_ARMS = ["200d", "band2", "band3", "band5", "band8", "band12", "band20"]
BAND_B = {"200d": 0.00, "band2": 0.02, "band3": 0.03, "band5": 0.05,
          "band8": 0.08, "band12": 0.12, "band20": 0.20}
IS_END, OOS_START = "2016-12-31", "2017-01-01"

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# ------------------------------------------------------------------ engine
def fast_bt(px, w, freq=FREQ):
    """Vectorised engine.backtest.  Returns gross returns, turnover and realised gross.
    Asserted identical to engine.backtest in Q1[a]."""
    idx = px.index
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mask)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return (pd.Series((held * rets).sum(axis=1), index=idx),
            pd.Series(turn, index=idx),
            pd.Series(held.sum(axis=1), index=idx))


def net(gr, tn, bps):
    return gr - tn * bps / 1e4


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def mrow(r):
    m = metrics(r)
    h1, h2 = halves(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def turn_per_yr(t):
    return float(t.sum() / (len(t) / 252.0))


# ------------------------------------------------------------------ gates
def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def trend(px, arm):
    """Trend state per ticker-day.  Idea 57/61's vocabulary, reproduced verbatim."""
    if arm == "NOGATE":
        return pd.DataFrame(True, index=px.index, columns=px.columns)
    ma = px.rolling(200).mean()
    if arm == "200d":
        return (px > ma).fillna(False)
    if arm == "200d-M":
        g = (px > ma).astype(float)
        me = rebalance_mask(px.index, "M")
        keep = pd.DataFrame(np.repeat(me.values[:, None], px.shape[1], axis=1),
                            index=px.index, columns=px.columns)
        return g.where(keep, other=np.nan).ffill().fillna(0.0) > 0.5
    if arm.startswith("band"):
        b = int(arm[4:]) / 100.0
        raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
        raw = raw.mask(px > ma * (1 + b), 1.0).mask(px < ma * (1 - b), 0.0)
        return raw.ffill().fillna(0.0) > 0.5
    raise ValueError(arm)


def gate_state(px, arm, comp):
    t = trend(px, arm)
    return (t & (vol20(px) < MAX_VOL)) if comp == "FULL" else t


def flip_rate(g, px, tradable):
    """Gate-state changes per TICKER-YEAR on priced days (idea 4/61's unit)."""
    cols = [c for c in px.columns if c in tradable]
    g, live = g[cols], px[cols].notna()
    ch = (g.astype(int).diff().abs() == 1) & live & live.shift(1).fillna(False)
    ty = live.sum().sum() / 252.0
    return float(ch.sum().sum() / ty) if ty > 0 else np.nan


def weights_ewall(px, selectable, g, conv, gross=GROSS):
    """dg: denominator is the full selectable priced universe (gross floats with the gate).
    rw: denominator is the surviving set (gross pinned at `gross`)."""
    live = px.notna() & selectable
    sel = g & live
    num = sel.astype(float)
    den = (live.sum(axis=1) if conv == "dg" else sel.sum(axis=1)).replace(0, np.nan)
    return num.div(den, axis=0).mul(gross).fillna(0.0)


# ------------------------------------------------------------------ panels
def build_panels():
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in pxs.columns if c == "SPY" or c not in bad]
    pxs = pxs[keep].dropna(how="all").ffill()
    small_tr = {c for c in pxs.columns if c != "SPY"}
    px56 = load_universe()
    tr56 = set(px56.columns)                       # SPY is a real constituent of universe.json
    P(f"[panels] SMALL439 {len(small_tr)} tradable (+SPY benchmark; dropped "
      f"{len(bad & set(load_universe(small=True).columns))} with max_1d_move>=1.0), "
      f"{pxs.index[0].date()}..{pxs.index[-1].date()}  |  U56 {len(tr56)} tradable, "
      f"{px56.index[0].date()}..{px56.index[-1].date()}")
    return {"SMALL439": (pxs, small_tr), "U56": (px56, tr56)}


def adv_mask(px, tradable, floor):
    """Point-in-time selectability: 20d rolling MEDIAN dollar volume >= floor (idea 120/121)."""
    m = pd.DataFrame(False, index=px.index, columns=px.columns)
    for c in tradable:
        m[c] = True
    if floor <= 0:
        return m
    vol = load_volume(small=True).reindex(index=px.index).reindex(columns=px.columns)
    dv = (px * vol).rolling(20).median()
    return m & (dv >= floor).fillna(False)


# =====================================================================================
T0 = time.time()
P("=" * 112)
P("IDEA 60  band-gate-on-small-panel   (lane B, 2026-09-06)")
P("=" * 112)
PANELS = build_panels()
START = {k: v[0].index[260] for k, v in PANELS.items()}
pxS, trS = PANELS["SMALL439"]
px56, tr56 = PANELS["U56"]

# ------------------------------------------------------------------ Q1 reproduction gates
P("\n" + "-" * 112)
P("Q1  REPRODUCTION GATES (all printed whatever they say; nothing below is read until these pass)")
P("-" * 112)

w_probe = weights_ewall(pxS, adv_mask(pxS, trS, 0.0), gate_state(pxS, "band3", "TREND"), "dg")
r_eng = backtest(pxS, w_probe, cost_bps=10.0, freq=FREQ)["returns"]
g_, t_, _ = fast_bt(pxS, w_probe)
P(f"[a] fast_bt vs engine.backtest (SMALL439, ew-all, band3, dg, 10bps)  max|diff| = "
  f"{np.abs(r_eng - net(g_, t_, 10)).max():.3e}")

sS = START["SMALL439"]
spyS = pxS["SPY"].pct_change().fillna(0).loc[sS:]
mS = mrow(spyS)
P(f"[b] SPY over the SMALL439 window {sS.date()}..{pxS.index[-1].date()}: "
  f"{mS['CAGR']:.2%}/{mS['Sharpe']:.3f}/{mS['MaxDD']:.1%} halves {mS['H1']:.3f}/{mS['H2']:.3f}"
  f"   [idea 121 published 14.13%/0.862/-33.7%, halves 0.891/0.858]")

wv1 = rules_v1_weights(pxS.drop(columns=["SPY"])).reindex(columns=pxS.columns).fillna(0.0)
gv1, tv1, _ = fast_bt(pxS, wv1)
mv1 = mrow(net(gv1, tv1, 10).loc[sS:])
P(f"[c] LIVE RULES v1 on SMALL439 @10bps: {mv1['CAGR']:.2%}/{mv1['Sharpe']:.3f}/{mv1['MaxDD']:.1%}"
  f"   [idea 121 published 8.15%/0.603/-32.8%]")
P("    (v1's cross-sectional ranks are computed on the 439 SELECTABLE names only — SPY is a "
  "benchmark\n     column, not a constituent; ranking it in costs 0.74 pp of CAGR and is the "
  "one convention\n     that has to be matched for this gate to bind.)")

s56 = START["U56"]
gv2, tv2, _ = fast_bt(px56, rules_v2_weights(px56))
mv2 = mrow(net(gv2, tv2, 10).loc[s56:])
P(f"[d] LIVE RULES v2 on U56 @10bps: {mv2['CAGR']:.2%}/{mv2['Sharpe']:.4f}/{mv2['MaxDD']:.2%} "
  f"halves {mv2['H1']:.4f}/{mv2['H2']:.4f}   [idea 61 published 8.66%/1.2056/-12.05%, "
  f"1.2259/1.1908]")

P("[e] idea 61's committed SMALL439 x ew-all x BAND x TREND x floor$0 rows, re-derived here:")
try:
    g61 = pd.read_csv(OUT / "2026-09-06_gate-instrument-speed-curve_cloud.grid.csv")
    g61 = g61[(g61.panel == "SMALL439") & (g61.book == "ew-all") & (g61.family == "BAND")]
except Exception as e:                                                    # pragma: no cover
    g61 = pd.DataFrame()
    P(f"    !! could not read idea 61's grid ({e}); gate skipped")
P(f"    {'arm':<8}{'conv':>5}{'bps':>5}{'Sharpe':>10}{'ref':>10}{'d':>10}"
  f"{'CAGR':>9}{'ref':>9}{'d':>9}")
gate_e = []
for arm in BAND_ARMS:
    gs = gate_state(pxS, arm, "TREND")
    for conv in ("dg", "rw"):
        gr, tn, _ = fast_bt(pxS, weights_ewall(pxS, adv_mask(pxS, trS, 0.0), gs, conv))
        for c in (10, 25):
            mm = mrow(net(gr, tn, c).loc[sS:])
            ref = g61[(g61.conv == conv) & (g61.cost == c) &
                      (np.isclose(g61.dial, BAND_B[arm]))] if len(g61) else pd.DataFrame()
            if len(ref):
                rs, rc = float(ref.Sharpe.iloc[0]), float(ref.CAGR.iloc[0])
                gate_e.append(abs(mm["Sharpe"] - rs))
                P(f"    {arm:<8}{conv:>5}{c:>5}{mm['Sharpe']:>10.4f}{rs:>10.4f}"
                  f"{mm['Sharpe'] - rs:>10.1e}{mm['CAGR']:>9.4f}{rc:>9.4f}{mm['CAGR'] - rc:>9.1e}")
P(f"    -> max|Sharpe diff| vs idea 61 over {len(gate_e)} cells = "
  f"{max(gate_e) if gate_e else float('nan'):.3e}")

# ------------------------------------------------------------------ Q2 flip rates (P3)
P("\n" + "-" * 112)
P("Q2  WHIPSAW — gate flips per ticker-year, both panels (P3)")
P("-" * 112)
frows = []
P(f"  {'arm':<9}{'SMALL439 TREND':>16}{'U56 TREND':>12}{'ratio':>8}   "
  f"{'SMALL439 FULL':>15}{'U56 FULL':>11}")
for arm in ARMS:
    row = dict(arm=arm, b=BAND_B.get(arm, np.nan))
    for comp in ("TREND", "FULL"):
        row[f"small_{comp}"] = flip_rate(gate_state(pxS, arm, comp).loc[sS:], pxS.loc[sS:], trS)
        row[f"u56_{comp}"] = flip_rate(gate_state(px56, arm, comp).loc[s56:], px56.loc[s56:], tr56)
    # idea 61's convention: the WHOLE index, every column, so its published number is gateable
    row["u56_TREND_i61"] = flip_rate(gate_state(px56, arm, "TREND"), px56, set(px56.columns))
    row["small_TREND_i61"] = flip_rate(gate_state(pxS, arm, "TREND"), pxS, set(pxS.columns))
    row["ratio_TREND"] = row["small_TREND"] / row["u56_TREND"] if row["u56_TREND"] else np.nan
    frows.append(row)
    P(f"  {arm:<9}{row['small_TREND']:>16.2f}{row['u56_TREND']:>12.2f}"
      f"{row['ratio_TREND']:>8.2f}   {row['small_FULL']:>15.2f}{row['u56_FULL']:>11.2f}")
flips = pd.DataFrame(frows)
flips.to_csv(OUT / f"{STEM}.flips.csv", index=False)
f200 = flips.loc[flips.arm == "200d", "u56_TREND"].iloc[0]
fb3 = flips.loc[flips.arm == "band3", "u56_TREND"].iloc[0]
P(f"  Rates above are measured on the EVALUATION window (from index[260]) and on tradable "
  f"columns only.\n  Idea 4/57/61 measure on the WHOLE index over every column; under that "
  f"convention U56 reads\n  200d {flips.loc[flips.arm == '200d', 'u56_TREND_i61'].iloc[0]:.3f} "
  f"and band3 {flips.loc[flips.arm == 'band3', 'u56_TREND_i61'].iloc[0]:.3f} "
  f"[idea 61 published 7.44 / 1.75; idea 4/57 7.55 / 1.77] -> GATE.\n  Both panels are "
  f"measured identically here, so the SMALL/U56 ratio is convention-free.")
s200 = flips.loc[flips.arm == "200d", "small_TREND"].iloc[0]
P(f"  P3 (small panel flips MORE than large caps on the bare 200d gate): "
  f"{s200:.2f} vs {f200:.2f} -> {'HOLDS' if s200 > f200 else 'FAILS'}")

# ------------------------------------------------------------------ Q3 the main grid
P("\n" + "-" * 112)
P("Q3  MAIN GRID — every panel x floor x convention x composition x arm x cost rung, all reported")
P("-" * 112)
rows = []
for pname, (px, tr) in PANELS.items():
    st = START[pname]
    floors = FLOORS if pname == "SMALL439" else [0.0]
    for floor in floors:
        sel = adv_mask(px, tr, floor)
        n_sel = sel.loc[st:].sum(axis=1).mean()
        for comp in ("TREND", "FULL"):
            for arm in ARMS:
                gs = gate_state(px, arm, comp)
                held_names = (gs & sel & px.notna()).loc[st:].sum(axis=1).mean()
                for conv in ("dg", "rw"):
                    gr, tn, gx = fast_bt(px, weights_ewall(px, sel, gs, conv))
                    gr, tn, gx = gr.loc[st:], tn.loc[st:], gx.loc[st:]
                    for c in COSTS:
                        m = mrow(net(gr, tn, c))
                        rows.append(dict(panel=pname, floor_musd=floor / 1e6, conv=conv,
                                         comp=comp, arm=arm, b=BAND_B.get(arm, np.nan), bps=c,
                                         **m, turnover=turn_per_yr(tn),
                                         realised_gross=float(gx.mean()),
                                         names_sel=float(n_sel), names_held=float(held_names),
                                         flips=flip_rate(gs.loc[st:], px.loc[st:], tr)))
grid = pd.DataFrame(rows)

# delta vs the NOGATE control in the same (panel, floor, conv, comp, bps) cell.
# NOTE: an explicit merge, not an index-aligned subtraction — the key repeats once per arm, so
# aligning on a duplicated index silently mis-pairs the rows.
key = ["panel", "floor_musd", "conv", "comp", "bps"]
base = (grid[grid.arm == "NOGATE"][key + ["CAGR", "Sharpe", "MaxDD"]]
        .rename(columns={"CAGR": "b_CAGR", "Sharpe": "b_Sharpe", "MaxDD": "b_MaxDD"}))
grid = grid.merge(base, on=key, how="left", validate="many_to_one")
grid["dCAGR_pp"] = (grid["CAGR"] - grid["b_CAGR"]) * 100
grid["dSharpe"] = grid["Sharpe"] - grid["b_Sharpe"]
grid["dMaxDD_pp"] = (grid["MaxDD"] - grid["b_MaxDD"]) * 100
assert np.allclose(grid.loc[grid.arm == "NOGATE", "dCAGR_pp"], 0.0), "delta join mis-paired"
grid = grid.drop(columns=["b_CAGR", "b_Sharpe", "b_MaxDD"])
grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)
P(f"  {len(grid)} grid points written to {STEM}.grid.csv")

for pname in ("SMALL439", "U56"):
    for floor in (FLOORS if pname == "SMALL439" else [0.0]):
        for comp in ("FULL", "TREND"):
            for conv in ("rw", "dg"):
                s = grid[(grid.panel == pname) & (grid.floor_musd == floor / 1e6) &
                         (grid.comp == comp) & (grid.conv == conv)]
                P(f"\n  {pname}  floor ${floor/1e6:.0f}M  comp {comp}  conv {conv}"
                  f"   (selectable {s.names_sel.iloc[0]:.0f} names)")
                P(f"    {'arm':<8}{'flips':>7}{'held':>7}{'gross':>7}{'turn':>7}" +
                  "".join(f"{'CAGR@'+str(c):>11}" for c in COSTS) +
                  "".join(f"{'dCAGR@'+str(c):>12}" for c in COSTS) +
                  f"{'Sh@10':>8}{'dSh@10':>8}{'MaxDD@10':>10}{'H1/H2@10':>16}")
                for arm in ARMS:
                    a = s[s.arm == arm].set_index("bps")
                    a10 = a.loc[PROTO_COST]
                    P(f"    {arm:<8}{a10.flips:>7.2f}{a10.names_held:>7.0f}"
                      f"{a10.realised_gross:>7.2f}{a10.turnover:>7.1f}" +
                      "".join(f"{a.loc[c, 'CAGR']:>11.2%}" for c in COSTS) +
                      "".join(f"{a.loc[c, 'dCAGR_pp']:>12.2f}" for c in COSTS) +
                      f"{a10.Sharpe:>8.3f}{a10.dSharpe:>8.3f}{a10.MaxDD:>10.1%}"
                      f"{a10.H1:>8.3f}{a10.H2:>8.3f}")

# ------------------------------------------------------------------ Q4 P1, P2, P4
P("\n" + "-" * 112)
P("Q4  THE QUEUE'S THREE NUMBERS — P1 reproduction, P2 recovery, P4 saturation")
P("-" * 112)


def cell(panel, floor, conv, comp, bps, arm):
    s = grid[(grid.panel == panel) & (grid.floor_musd == floor) & (grid.conv == conv) &
             (grid.comp == comp) & (grid.bps == bps) & (grid.arm == arm)]
    return s.iloc[0]


P("The published claim is EWall (NO gate at all) vs EWgate (px>200d AND vol20<0.60), so the")
P("comparand for it is comp=TREND/arm=NOGATE against comp=FULL/arm=200d.  Reading the damage")
P("inside comp=FULL would leave the vol20 half in BOTH legs and understate it, so both")
P("decompositions are printed and the pre-registered numbers are read on the published one.")

P("\n[4-WAY GATE DECOMPOSITION — idea 38/56's construction, CAGR by half of the filter]")
P(f"  {'panel':<9}{'flr':>4}{'conv':>5}{'bps':>5}{'EWall':>9}{'200d only':>11}{'vol20 only':>12}"
  f"{'both':>9}{'both-EWall pp':>15}{'band3+vol20':>13}{'band3 only':>12}")
drows = []
for pname in ("SMALL439", "U56"):
    for floor in (FLOORS if pname == "SMALL439" else [0.0]):
        f = floor / 1e6
        for conv in ("rw", "dg"):
            for c in COSTS:
                ewall = cell(pname, f, conv, "TREND", c, "NOGATE").CAGR
                t_only = cell(pname, f, conv, "TREND", c, "200d").CAGR
                v_only = cell(pname, f, conv, "FULL", c, "NOGATE").CAGR
                both = cell(pname, f, conv, "FULL", c, "200d").CAGR
                b3f = cell(pname, f, conv, "FULL", c, "band3").CAGR
                b3t = cell(pname, f, conv, "TREND", c, "band3").CAGR
                drows.append(dict(panel=pname, floor_musd=f, conv=conv, bps=c, EWall=ewall,
                                  trend_only=t_only, vol_only=v_only, both=both,
                                  published_dCAGR_pp=(both - ewall) * 100,
                                  band3_FULL=b3f, band3_TREND=b3t))
                P(f"  {pname:<9}{f:>4.0f}{conv:>5}{c:>5}{ewall:>9.2%}{t_only:>11.2%}"
                  f"{v_only:>12.2%}{both:>9.2%}{(both - ewall) * 100:>15.2f}{b3f:>13.2%}"
                  f"{b3t:>12.2%}")
dec = pd.DataFrame(drows)
dec.to_csv(OUT / f"{STEM}.decomp.csv", index=False)

c10 = dec[(dec.panel == "SMALL439") & (dec.floor_musd == 0.0) & (dec.conv == "rw") &
          (dec.bps == 10)].iloc[0]
c00 = dec[(dec.panel == "SMALL439") & (dec.floor_musd == 0.0) & (dec.conv == "rw") &
          (dec.bps == 0)].iloc[0]
g10 = cell("SMALL439", 0.0, "rw", "FULL", 10, "200d")
g10n = cell("SMALL439", 0.0, "rw", "TREND", 10, "NOGATE")
P(f"\nP1  idea 121's cell (SMALL439, floor $0, g=0.75, rw, FULL gate, 10 bps), gate minus no-gate:")
P(f"    dCAGR {c10.published_dCAGR_pp:+.4f} pp  [published -6.5155]   "
  f"dSharpe {g10.Sharpe - g10n.Sharpe:+.4f}  [-0.3420]   "
  f"dMaxDD {(g10.MaxDD - g10n.MaxDD) * 100:+.4f} pp  [-3.8143]")
P(f"    names: all {g10n.names_held:.2f} [347.91]   gated {g10.names_held:.2f} [141.26]")
P(f"    and at ZERO cost, where idea 49's headline lives: "
  f"dCAGR {c00.published_dCAGR_pp:+.4f} pp  [published -5.4]")
ok1 = (abs(c10.published_dCAGR_pp - (-6.5155)) < 0.05 and
       abs((g10.Sharpe - g10n.Sharpe) - (-0.3420)) < 0.005 and
       abs(c00.published_dCAGR_pp - (-5.4)) < 0.20)
P(f"    P1 -> {'HOLDS' if ok1 else 'FAILS'}")

P("\nP2/P4  the recovery curve, on two readings, both printed for every cell:")
P("   PUB   recovery of the PUBLISHED damage: (arm-in-FULL - 200d-in-FULL) / (EWall - 200d-in-FULL).")
P("         100% would mean the band alone repairs everything the whole eligibility gate destroyed.")
P("   TRND  recovery of the TREND HALF's own damage: (arm - 200d) / (NOGATE - 200d) inside the")
P("         same composition.  This is the most generous reading available to the hypothesis.")
crows = []
for pname in ("SMALL439", "U56"):
    for floor in (FLOORS if pname == "SMALL439" else [0.0]):
        f = floor / 1e6
        for conv in ("rw", "dg"):
            for c in COSTS:
                pub_gap = (cell(pname, f, conv, "TREND", c, "NOGATE").CAGR -
                           cell(pname, f, conv, "FULL", c, "200d").CAGR)
                b200 = cell(pname, f, conv, "FULL", c, "200d").CAGR
                r = dict(panel=pname, floor_musd=f, conv=conv, bps=c, pub_gap_pp=pub_gap * 100)
                for arm in BAND_ARMS + ["200d-M"]:
                    r[f"pub_{arm}"] = ((cell(pname, f, conv, "FULL", c, arm).CAGR - b200)
                                      / pub_gap if pub_gap else np.nan)
                for comp in ("FULL", "TREND"):
                    gp = (cell(pname, f, conv, comp, c, "NOGATE").CAGR -
                          cell(pname, f, conv, comp, c, "200d").CAGR)
                    r[f"trnd_gap_{comp}_pp"] = gp * 100
                    for arm in BAND_ARMS + ["200d-M"]:
                        r[f"trnd{comp}_{arm}"] = ((cell(pname, f, conv, comp, c, arm).CAGR -
                                                   cell(pname, f, conv, comp, c, "200d").CAGR)
                                                  / gp if gp else np.nan)
                crows.append(r)
curve = pd.DataFrame(crows)
curve.to_csv(OUT / f"{STEM}.curve.csv", index=False)

for lbl, pre_, gapc in (("PUB", "pub_", "pub_gap_pp"),
                        ("TRND(FULL)", "trndFULL_", "trnd_gap_FULL_pp"),
                        ("TRND(TREND)", "trndTREND_", "trnd_gap_TREND_pp")):
    P(f"\n  [{lbl}]  {'panel':<9}{'flr':>4}{'conv':>5}{'bps':>5}{'gap pp':>9}" +
      "".join(f"{a:>9}" for a in BAND_ARMS[1:] + ["200d-M"]))
    for _, r in curve.iterrows():
        P(f"  {'':<6}  {r.panel:<9}{r.floor_musd:>4.0f}{r.conv:>5}{int(r.bps):>5}"
          f"{r[gapc]:>9.2f}" +
          "".join(f"{r[pre_ + a]:>9.1%}" for a in BAND_ARMS[1:] + ["200d-M"]))

pre = curve[(curve.panel == "SMALL439") & (curve.floor_musd == 0.0) & (curve.conv == "rw") &
            (curve.bps == 0)].iloc[0]
P(f"\n  PRE-REGISTERED CELL (SMALL439, floor $0, rw, 0 bps):")
P(f"    published damage {pre.pub_gap_pp:.2f} pp/yr;  band3 recovers {pre.pub_band3:.1%} of it")
P(f"    trend-half damage inside FULL {pre.trnd_gap_FULL_pp:.2f} pp/yr; band3 recovers "
  f"{pre.trndFULL_band3:.1%}")
P(f"    trend-half damage with no vol filter {pre.trnd_gap_TREND_pp:.2f} pp/yr; band3 recovers "
  f"{pre.trndTREND_band3:.1%}")
best = max(pre.pub_band3, pre.trndFULL_band3, pre.trndTREND_band3)
P(f"  P2 (band3 recovers >= 50% of the damage) -> "
  f"{'HOLDS' if best >= 0.50 else 'FAILS'}   (best of the three readings: {best:.1%})")

P("\n  P4 saturation.  Under WHIPSAW the band buys back the noise crossings and then stops "
  "helping,\n  so the 0.03->0.20 increment should be small next to the 0.00->0.03 one.  Under "
  "NO-SIGNAL the\n  only cure is to stop gating, so recovery keeps climbing to the widest band.")
P(f"  {'reading':<14}{'0.00->0.03':>12}{'0.03->0.20':>12}{'ratio':>8}{'band20 total':>14}")
sat = {}
for lbl, pre_ in (("PUB", "pub_"), ("TRND(FULL)", "trndFULL_"), ("TRND(TREND)", "trndTREND_")):
    i3 = pre[pre_ + "band3"]
    i20 = pre[pre_ + "band20"] - pre[pre_ + "band3"]
    sat[lbl] = (i20 / i3) if i3 else np.nan
    P(f"  {lbl:<14}{i3:>12.1%}{i20:>12.1%}{sat[lbl]:>8.2f}{pre[pre_ + 'band20']:>14.1%}")
ok4 = all(v < 0.25 for v in sat.values())
P(f"  P4 (WHIPSAW: every reading's 0.03->0.20 increment is < 25% of its 0.00->0.03 increment)")
P(f"  -> {'HOLDS (whipsaw shape)' if ok4 else 'FAILS (no-signal shape: recovery does not saturate)'}")
P("  Monotonicity check (is recovery still rising at the widest band?): " +
  ", ".join(f"{lbl} {'RISING' if pre[pre_ + 'band20'] > pre[pre_ + 'band12'] else 'flat/falling'}"
            for lbl, pre_ in (("PUB", "pub_"), ("TRND(FULL)", "trndFULL_"),
                              ("TRND(TREND)", "trndTREND_"))))


# ------------------------------------------------------------------ Q5 rule 8
P("\n" + "-" * 112)
P("Q5  PROTOCOL RULE 8 — dial chosen on 2010..2016 only, evaluated untouched on 2017..2026")
P("-" * 112)
spy_oos = {}
for pname, (px, tr) in PANELS.items():
    sp = px["SPY"].pct_change().fillna(0).loc[START[pname]:]
    spy_oos[pname] = (metrics(sp.loc[OOS_START:]), metrics(sp))

# live RULES v2 (the book capital is actually in) on its own universe, aligned to each window
v2_full = net(gv2, tv2, PROTO_COST)
wrows = []
for pname, (px, tr) in PANELS.items():
    st = START[pname]
    floors = FLOORS if pname == "SMALL439" else [0.0]
    for floor in floors:
        sel = adv_mask(px, tr, floor)
        for comp in ("FULL", "TREND"):
            for conv in ("rw", "dg"):
                series = {}
                for arm in BAND_ARMS:
                    gr, tn, _ = fast_bt(px, weights_ewall(px, sel, gate_state(px, arm, comp), conv))
                    series[arm] = (gr.loc[st:], tn.loc[st:])
                gr0, tn0 = fast_bt(px, weights_ewall(px, sel, gate_state(px, "NOGATE", comp),
                                                     conv))[:2]
                series["NOGATE"] = (gr0.loc[st:], tn0.loc[st:])
                for c in COSTS:
                    R = {a: net(g, t, c) for a, (g, t) in series.items()}
                    IS = {a: r.loc[:IS_END] for a, r in R.items()}
                    OS = {a: r.loc[OOS_START:] for a, r in R.items()}
                    pick_sh = max(BAND_ARMS, key=lambda a: metrics(IS[a])["Sharpe"])
                    pick_cg = max(BAND_ARMS,
                                  key=lambda a: metrics(IS[a])["CAGR"] - metrics(IS["NOGATE"])["CAGR"])
                    row = dict(panel=pname, floor_musd=floor / 1e6, conv=conv, comp=comp, bps=c,
                               pick_IS_Sharpe=pick_sh, pick_IS_dCAGR=pick_cg)
                    for tag, a in (("pickSh", pick_sh), ("pickCG", pick_cg),
                                   ("const_band3", "band3"), ("incumbent_200d", "200d"),
                                   ("donothing_NOGATE", "NOGATE")):
                        mo = metrics(OS[a])
                        row[f"{tag}_arm"] = a
                        row[f"{tag}_oosCAGR"] = mo["CAGR"]
                        row[f"{tag}_oosSharpe"] = mo["Sharpe"]
                        row[f"{tag}_oosMaxDD"] = mo["MaxDD"]
                    wrows.append(row)
wf = pd.DataFrame(wrows)
wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

P(f"  {'panel':<9}{'flr':>4}{'conv':>5}{'comp':>6}{'bps':>4}{'IS-Sh pick':>11}{'IS-dC pick':>11}"
  f"{'OOS Sh pick':>12}{'OOS Sh b3':>11}{'OOS Sh 200d':>12}{'OOS Sh none':>12}{'SPY OOS':>9}")
for _, r in wf.iterrows():
    P(f"  {r.panel:<9}{r.floor_musd:>4.0f}{r.conv:>5}{r.comp:>6}{int(r.bps):>4}"
      f"{r.pick_IS_Sharpe:>11}{r.pick_IS_dCAGR:>11}{r.pickSh_oosSharpe:>12.3f}"
      f"{r.const_band3_oosSharpe:>11.3f}{r.incumbent_200d_oosSharpe:>12.3f}"
      f"{r.donothing_NOGATE_oosSharpe:>12.3f}{spy_oos[r.panel][0]['Sharpe']:>9.3f}")

for pname in ("SMALL439", "U56"):
    w = wf[wf.panel == pname]
    P(f"\n  {pname}: IS-Sharpe pick beats DO-NOTHING out of sample in "
      f"{int((w.pickSh_oosSharpe > w.donothing_NOGATE_oosSharpe).sum())}/{len(w)} cells; "
      f"beats the pre-registered constant band3 in "
      f"{int((w.pickSh_oosSharpe > w.const_band3_oosSharpe).sum())}/{len(w)}; "
      f"beats SPY OOS in {int((w.pickSh_oosSharpe > spy_oos[pname][0]['Sharpe']).sum())}/{len(w)}.")
    P(f"    mean OOS Sharpe: pick {w.pickSh_oosSharpe.mean():.3f}  band3 "
      f"{w.const_band3_oosSharpe.mean():.3f}  200d {w.incumbent_200d_oosSharpe.mean():.3f}  "
      f"NOGATE {w.donothing_NOGATE_oosSharpe.mean():.3f}  SPY {spy_oos[pname][0]['Sharpe']:.3f}")
    P(f"    mean OOS CAGR:   pick {w.pickSh_oosCAGR.mean():.2%}  band3 "
      f"{w.const_band3_oosCAGR.mean():.2%}  200d {w.incumbent_200d_oosCAGR.mean():.2%}  "
      f"NOGATE {w.donothing_NOGATE_oosCAGR.mean():.2%}  SPY {spy_oos[pname][0]['CAGR']:.2%}")
    P(f"    mean OOS MaxDD:  pick {w.pickSh_oosMaxDD.mean():.1%}  band3 "
      f"{w.const_band3_oosMaxDD.mean():.1%}  200d {w.incumbent_200d_oosMaxDD.mean():.1%}  "
      f"NOGATE {w.donothing_NOGATE_oosMaxDD.mean():.1%}  SPY {spy_oos[pname][0]['MaxDD']:.1%}")

# ------------------------------------------------------------------ Q6 both KEEP paths
P("\n" + "-" * 112)
P("Q6  BOTH KEEP PATHS at PROTOCOL's 10 bps (4a vs the LIVE RULES v2 book; 4b vs SPY + rule 8)")
P("-" * 112)


def path_verdicts(pname, r_full, r_oos):
    """4a against live RULES v2 (run on its OWN universe, aligned to this window); 4b vs SPY."""
    m = mrow(r_full)
    sp = PANELS[pname][0]["SPY"].pct_change().fillna(0).loc[START[pname]:]
    ms = mrow(sp)
    b = v2_full.reindex(r_full.index).fillna(0.0)
    mb = mrow(b)
    bad_a = []
    if m["H1"] <= mb["H1"]: bad_a.append("H1")
    if m["H2"] <= mb["H2"]: bad_a.append("H2")
    if m["MaxDD"] < mb["MaxDD"]: bad_a.append("DD")
    bad_b = []
    if m["H1"] <= ms["H1"]: bad_b.append("H1")
    if m["H2"] <= ms["H2"]: bad_b.append("H2")
    if metrics(r_oos)["Sharpe"] <= metrics(sp.loc[OOS_START:])["Sharpe"]: bad_b.append("OOS")
    if m["MaxDD"] < 0.60 * ms["MaxDD"]: bad_b.append("DD")
    if m["CAGR"] < 0.70 * ms["CAGR"]: bad_b.append("CAGR")
    return bad_a, bad_b, mb, ms


keep4a = keep4b = 0
vrows = []
for pname, (px, tr) in PANELS.items():
    st = START[pname]
    floors = FLOORS if pname == "SMALL439" else [0.0]
    for floor in floors:
        sel = adv_mask(px, tr, floor)
        for comp in ("FULL", "TREND"):
            for conv in ("rw", "dg"):
                for arm in ARMS:
                    gr, tn, _ = fast_bt(px, weights_ewall(px, sel, gate_state(px, arm, comp), conv))
                    r = net(gr.loc[st:], tn.loc[st:], PROTO_COST)
                    ba, bb, mb, ms = path_verdicts(pname, r, r.loc[OOS_START:])
                    keep4a += not ba
                    keep4b += not bb
                    vrows.append(dict(panel=pname, floor_musd=floor / 1e6, conv=conv, comp=comp,
                                      arm=arm, path4a="KEEP" if not ba else "KILL(" + ",".join(ba) + ")",
                                      path4b="KEEP" if not bb else "KILL(" + ",".join(bb) + ")"))
V = pd.DataFrame(vrows)
P(f"  4a bars (live RULES v2 on U56, aligned): H1 > {mrow(v2_full.loc[START['SMALL439']:])['H1']:.3f}"
  f" / H2 > {mrow(v2_full.loc[START['SMALL439']:])['H2']:.3f} on the SMALL439 window")
P(f"  4b bars (SPY, SMALL439 window): H1 > {mrow(spyS)['H1']:.3f}, H2 > {mrow(spyS)['H2']:.3f}, "
  f"OOS Sharpe > {metrics(spyS.loc[OOS_START:])['Sharpe']:.3f}, MaxDD >= "
  f"{0.60 * mrow(spyS)['MaxDD']:.1%}, CAGR >= {0.70 * mrow(spyS)['CAGR']:.2%}")
P(f"  4a KEEP {keep4a}/{len(V)};  4b KEEP {keep4b}/{len(V)}")
P("  failing bars by frequency (4b): " +
  ", ".join(f"{k} {v}" for k, v in
            pd.Series([x for s in V.path4b for x in
                       (s[5:-1].split(",") if s.startswith("KILL") else [])]).value_counts().items()))
sm = V[(V.panel == "SMALL439")]
P(f"  SMALL439 alone: 4a KEEP {(sm.path4a == 'KEEP').sum()}/{len(sm)}, "
  f"4b KEEP {(sm.path4b == 'KEEP').sum()}/{len(sm)}")
V.to_csv(OUT / f"{STEM}.verdicts.csv", index=False)

# ------------------------------------------------------------------ verdict
P("\n" + "=" * 112)
P("VERDICT")
P("=" * 112)
P(f"P1 reproduction ...... {'HOLDS' if ok1 else 'FAILS'}")
P(f"P2 band3 recovers >=50% of the zero-cost damage ...... "
  f"{'HOLDS' if best >= 0.50 else 'FAILS'}  (best of three readings {best:.1%}; published "
  f"damage {pre.pub_gap_pp:.2f} pp/yr, band3 repairs {pre.pub_band3:.1%} of it)")
P(f"P3 small panel flips more than large caps ...... {'HOLDS' if s200 > f200 else 'FAILS'} "
  f"({s200:.2f} vs {f200:.2f} flips/tkr/yr on the bare 200d gate)")
P(f"P4 recovery SATURATES (whipsaw shape) ...... {'HOLDS' if ok4 else 'FAILS'} "
  f"(0.03->0.20 increments are " +
  ", ".join(f"{lbl} {v:.0%}" for lbl, v in sat.items()) + " of 0.00->0.03)")
P(f"P5 nothing on this panel passes 4b ...... "
  f"{'HOLDS' if (sm.path4b == 'KEEP').sum() == 0 else 'FAILS'}")
P(f"\nruntime {time.time() - T0:.0f}s")
(OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
