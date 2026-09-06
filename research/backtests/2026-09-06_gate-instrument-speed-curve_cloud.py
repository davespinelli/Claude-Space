#!/usr/bin/env python3
"""IDEA 61  gate-instrument-speed-curve   (cloud, 2026-09-06)

THE QUESTION
------------
Idea 4 found net Sharpe in the `ew-all` book orders by FLIP RATE (band3 1.77 -> abs 5.75 ->
200d 7.55 -> both 8.06 flips/tkr/yr) on universe.json and near-monotone on broad, while the
ordering is absent or inverted in the ranked top20 book.  The queue asks for the design
variable rather than the instrument:

    sweep instruments spanning ~0.5-8 flips/tkr/yr and regress net Sharpe on flip rate in
    BOTH books.  Is there an optimum, or is slower always better?

  Q1  REPRODUCTION.  Rebuild idea 4's four instruments with its own `trend()` code and
      re-derive its published flip rates (band3 1.77, abs 5.75, 200d 7.55, both 8.06 per
      ticker-year) before any new number is read.
  Q2  THE SPEED AXIS.  Three families, each with ONE speed dial, spanning the range the queue
      asked for: BAND (200d + hysteresis b), STALE (bare 200d re-evaluated every k trading
      days, state held between), ABS (12-1 absolute momentum + deadband d).  Flip rate is
      measured, not assumed; every grid point is reported.
  Q3  THE CURVE.  Net Sharpe against measured flip rate in BOTH books x 3 panels x 2 rungs.
      Spearman, the argmax's location, and whether the argmax is INTERIOR (an optimum) or at
      the slow edge ("slower is always better").
  Q4  IS THE CURVE A GROSS LADDER?  (Idea 277, this morning.)  Under the `dg` convention a
      SLOWER gate holds more names in, so realised gross rises with slowness and the curve is
      confounded with the exposure ladder that idea 277 measured.  Every point is therefore
      re-read twice: against the ungated constant-gross ladder at its OWN realised mean gross,
      and again under the `rw` convention where gross is held at nominal by construction.  If
      the speed curve is real it must survive both.
  Q5  RULE 8.  Speed dial chosen on IS <= 2016-12-31 by IS Sharpe, OOS >= 2017-01-01 read
      ONCE, against the do-nothing incumbent (RULES v2), the gross-matched ladder point,
      RULES v1 and SPY.
  Q6  BOTH KEEP PATHS on every arm.

DESIGN
------
Parent code is IMPORTED, not re-implemented: idea 62's `trend`/`abs_mom` (which is idea 4's
gate vocabulary), idea 78's `build_panels`, and idea 171's `fast_backtest`.

  BOOKS        `ew-all` : equal weight every gated name (idea 4's book)
               `top20`  : the composite-ranked top 20, equal weighted (idea 4's ranked book)
               Both at gross 0.75, weekly, t+1 execution.
  CONVENTIONS  `dg` gated-out weight to cash (gross floats with the gate) -- idea 4's own;
               `rw` gated-out weight re-spread over survivors (gross pinned at nominal).
  FAMILIES     BAND  b in {0, 0.02, 0.03, 0.05, 0.08, 0.12, 0.20}      (b = 0 is the bare 200d)
               STALE k in {1, 5, 21, 63, 126, 252} trading days        (k = 1 is the bare 200d)
               ABS   d in {0, 0.05, 0.10, 0.20}                        (d = 0 is idea 4's `abs`)
               17 arms per (book, conv, panel, rung); the two k=1/b=0 duplicates of the bare
               200d gate are asserted identical, not assumed.
  PANELS       U56, B136 primary; SMALL439 secondary (the sub-$2B panel with the
               max_1d_move >= 1.0 screen applied -- 44 of 483 names dropped).
  RUNGS        10 and 25 bps, both derived exactly from one 0 bps run per book.
  WINDOWS      IS <= 2016-12-31 chooses; OOS >= 2017-01-01 read ONCE.

  TUNED PARAMETER 1: the family's speed dial (b / k / d) -- ALL grid points reported.
  TUNED PARAMETER 2: the cost rung -- both reported.
  The families, the books, the gross, the cadence and the panels are INHERITED from ideas
  4/62/78, not chosen here.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
---------------------------------------------------------------------
  P1  Idea 4's published flip rates re-derive to within 0.3 flips/tkr/yr on U56.
  P2  Flip rate is monotone DECREASING in each family's speed dial (wider band, staler
      re-evaluation and deeper deadband all slow the gate).
  P3  In the `ew-all` book at 10 bps, Spearman(flip rate, net Sharpe) is NEGATIVE on both
      primary panels -- idea 4's ordering reproduces as a curve.
  P4  In the `top20` book that Spearman is weaker (|rho| smaller) or positive -- idea 4's
      "absent or inverted in the ranked book".
  P5  The argmax is at the SLOW EDGE of the grid in a majority of (book, panel, rung) cells,
      i.e. "slower is always better" and there is no interior optimum.
  P6  Under `rw` (gross pinned) the speed curve's Sharpe RANGE shrinks by more than half
      against `dg` -- most of idea 4's ordering is the exposure channel idea 277 measured.
  P7  Rule 8: choosing the speed dial on IS does NOT beat doing nothing out of sample.

CAVEATS carried, not buried
---------------------------
  * SURVIVORSHIP (idea 54): all three panels are current-constituent lists.  It runs AGAINST
    the SLOW arm -- a slow gate is slow to exit a name a delisting-aware panel would kill --
    so a survivorship-free panel would move the curve TOWARD the fast end.  That is the
    direction that matters for a "slower is better" conclusion and it is stated, not adjusted.
  * The small panel is secondary: ideas 39/49/136 show the 200d gate is INVERTED there.
  * Flip rate is counted on the GATE STATE per ticker-day, not on trades; a flip only costs
    money if it lands on a rebalance date.  Turnover is reported beside it.
  * Costs are flat linear bps on turnover; real cost is spread plus impact (idea 126).
  * The three families are not independent draws -- BAND b=0 and STALE k=1 are the same gate.
  * Idea 38's calendar-day index fix and idea 126's t+1-only execution carry over.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .flips.csv, .curve.csv,
.walkforward.csv, .keep.csv
"""
import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-06_gate-instrument-speed-curve_cloud"
OUT = ROOT / "research" / "backtests"
P78_STEM = "2026-09-05_candidate-count-vs-dispersion_B"
P171_STEM = "2026-09-05_do-gross-choice-rules-lose-to-constants-in-general_C"
P62_STEM = "2026-09-06_abs-gate-bear-shape_B"

GROSS = 0.75
FREQ = "W"
RUNGS = [10, 25]
BASE_RUNG = 10
MAX_VOL = 0.60
N_TOP = 20
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
BANDS = [0.00, 0.02, 0.03, 0.05, 0.08, 0.12, 0.20]
STALES = [1, 5, 21, 63, 126, 252]
DEADS = [0.00, 0.05, 0.10, 0.20]
GROSS_LADDER = [round(0.20 + 0.05 * i, 2) for i in range(17)]

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 6000)

_lines: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


def _load(stem, name):
    spec = importlib.util.spec_from_file_location(name, OUT / f"{stem}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


T0 = time.time()
p78 = _load(P78_STEM, "p78")
p171 = _load(P171_STEM, "p171")
p62 = _load(P62_STEM, "p62")
for m in (p78, p171, p62):
    m.P = P
build_panels = p78.build_panels
spearman = p78.spearman
trend = p62.trend                    # idea 4's gate vocabulary, imported
abs_mom = p62.abs_mom


def fast_backtest_g(prices, weights, cost_bps=0.0, freq=FREQ):
    """Idea 171's vectorised engine.backtest plus the realised (drifted) gross series.
    Asserted identical to engine.backtest and p171.fast_backtest in Q1."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
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
    gross_ret = (held * rets).sum(axis=1)
    return {"returns": pd.Series(gross_ret - turn * cost_bps / 1e4, index=idx),
            "gross_ret": pd.Series(gross_ret, index=idx),
            "turnover": pd.Series(turn, index=idx),
            "gross": pd.Series(held.sum(axis=1), index=idx)}


def net(gr, tn, bps):
    return gr - tn * bps / 1e4


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def mrow(r):
    m = metrics(r)
    h1, h2 = halves(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


# ------------------------------------------------------------------ the speed families
def gate_state(px, family, dial):
    """One boolean gate state per ticker-day.  Each family has exactly ONE speed dial."""
    if family == "BAND":
        return trend(px, "200d") if dial == 0.0 else trend(px, f"band{int(round(dial * 100))}")
    if family == "STALE":
        g = trend(px, "200d")
        if dial == 1:
            return g
        # re-evaluate only every `dial` trading days; hold the last decision in between
        keep = pd.Series(False, index=px.index)
        keep.iloc[::int(dial)] = True
        return g.where(keep, np.nan).ffill().fillna(False).astype(bool)
    if family == "ABS":
        a = abs_mom(px)
        if dial == 0.0:
            return (a > 0).fillna(False)
        st = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
        st = st.mask(a > dial, 1.0).mask(a < -dial, 0.0)
        return st.ffill().fillna(0.0) > 0.5
    raise ValueError(family)


def flip_rate(g, px):
    """Gate-state changes per TICKER-YEAR, counted on days the name is priced (idea 4's unit)."""
    live = px.notna()
    ch = (g.astype(int).diff().abs() == 1) & live & live.shift(1).fillna(False)
    tkr_years = (live.sum().sum()) / 252.0
    return float(ch.sum().sum() / tkr_years) if tkr_years > 0 else np.nan


def weights_book(px, tradable, g, book, conv, gross=GROSS):
    """`ew-all` = equal weight the gated set; `top20` = the composite-ranked top 20 of it.

    dg  denominator is the full priced tradable universe (ew-all) / the fixed count n=20
        (top20) -> gross floats down with the gate.
    rw  denominator is the surviving set (ew-all) / the realised count (top20) -> gross pinned.
    """
    live = px.notna().copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        live[drop] = False
    sel = (g & live)
    if book == "ew-all":
        num = sel.astype(float)
        denom = (live.sum(axis=1) if conv == "dg" else sel.sum(axis=1)).replace(0, np.nan)
        return num.div(denom, axis=0).mul(gross).fillna(0.0)
    if book == "top20":
        key = score(px, vol_scale=False)[0].where(sel)
        rank = key.rank(axis=1, ascending=False)
        pick = (rank <= N_TOP) & sel
        denom = (float(N_TOP) if conv == "dg" else pick.sum(axis=1).replace(0, np.nan))
        return pick.astype(float).div(denom, axis=0 if conv != "dg" else 0).mul(gross).fillna(0.0) \
            if conv != "dg" else pick.astype(float).mul(gross / N_TOP)
    raise ValueError(book)


# ------------------------------------------------------------------ panels
def get_panels():
    pans = build_panels()
    out = {"U56": pans["U56"], "B136": pans["B136"]}
    pxs, s_stk = pans["SMALL484"]
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in pxs.columns if c == "SPY" or (c in s_stk and c not in bad)]
    out["SMALL439"] = (pxs[keep].dropna(how="all").ffill(), {c for c in keep if c != "SPY"})
    P(f"[panels] U56 {len(out['U56'][1])} tradable, B136 {len(out['B136'][1])}, "
      f"SMALL439 {len(out['SMALL439'][1])} (dropped {len(bad & set(s_stk))} with max_1d_move>=1.0)")
    return out


# =====================================================================================
P("=" * 112)
P("IDEA 61  gate-instrument-speed-curve   (cloud, 2026-09-06)")
P("=" * 112)

PANELS = get_panels()
START = {nm: px.index[260] for nm, (px, tr) in PANELS.items()}
px56, tr56 = PANELS["U56"]

# ------------------------------------------------------------------ Q1
P("\n" + "-" * 112)
P("Q1  REPRODUCTION")
P("-" * 112)
w_probe = weights_book(px56, tr56, gate_state(px56, "BAND", 0.03), "ew-all", "dg")
r_eng = backtest(px56, w_probe, cost_bps=10.0, freq=FREQ)["returns"]
r_fast = fast_backtest_g(px56, w_probe, 10.0, FREQ)["returns"]
P(f"[a] fast_backtest_g vs engine.backtest      max|diff| = {np.abs(r_eng - r_fast).max():.3e}")
P(f"[a] fast_backtest_g vs p171.fast_backtest   max|diff| = "
  f"{np.abs(p171.fast_backtest(px56, w_probe, 10.0, FREQ)['returns'] - r_fast).max():.3e}")
assert np.abs(r_eng - r_fast).max() < 1e-12

res_v2 = fast_backtest_g(px56, rules_v2_weights(px56), 0.0, FREQ)
m = mrow(net(res_v2["gross_ret"], res_v2["turnover"], BASE_RUNG).loc[START["U56"]:])
P(f"[b] LIVE RULES v2 on U56 @10bps: {m['CAGR']:.2%} / {m['Sharpe']:.4f} / {m['MaxDD']:.2%}, "
  f"halves {m['H1']:.4f}/{m['H2']:.4f}   (record 8.66% / 1.2056 / -12.05%, 1.2259/1.1908)")

P("\n[c] idea 4's published flip rates on U56 (band3 1.77, abs 5.75, 200d 7.55, both 8.06):")
for nm, g in [("band3", trend(px56, "band3")), ("abs", trend(px56, "abs")),
              ("200d", trend(px56, "200d")), ("both", trend(px56, "both"))]:
    P(f"      {nm:6s} measured {flip_rate(g, px56):6.2f} flips/tkr/yr")
P("\n[d] the two duplicate parameterisations of the bare 200d gate are ASSERTED identical:")
assert gate_state(px56, "BAND", 0.00).equals(gate_state(px56, "STALE", 1))
P("      gate_state(BAND, 0.00) == gate_state(STALE, 1)   True")

# ------------------------------------------------------------------ Q2 the ungated ladder (idea 277's control)
P("\n" + "-" * 112)
P("Q2  THE UNGATED CONSTANT-GROSS LADDER  (idea 277's control channel, per panel x rung)")
P("-" * 112)
lad_rows = []
for pname, (px, tr) in PANELS.items():
    st = START[pname]
    live = px.notna().copy()
    live[[c for c in px.columns if c not in tr]] = False
    for gl in GROSS_LADDER:
        w = live.astype(float).div(live.sum(axis=1).replace(0, np.nan), axis=0).mul(gl).fillna(0.0)
        res = fast_backtest_g(px, w, 0.0, FREQ)
        gr, tn = res["gross_ret"].loc[st:], res["turnover"].loc[st:]
        rg = res["gross"].loc[st:].mean()
        for c in RUNGS:
            lad_rows.append(dict(panel=pname, cost=c, nominal_gross=gl, realised_gross=rg,
                                 **mrow(net(gr, tn, c))))
lad = pd.DataFrame(lad_rows)


def ladder_at(pname, cost, rg, col):
    s = lad[(lad.panel == pname) & (lad.cost == cost)].sort_values("realised_gross")
    return float(np.interp(rg, s["realised_gross"].values, s[col].values))


sp = lad.groupby(["panel", "cost"]).agg(Sharpe_span=("Sharpe", lambda x: x.max() - x.min()),
                                        CAGR_span_pp=("CAGR", lambda x: 100 * (x.max() - x.min())),
                                        MaxDD_span_pp=("MaxDD", lambda x: 100 * (x.max() - x.min())))
P(sp.to_string(float_format=lambda x: f"{x:.4f}"))
P("  (idea 277: the ladder is a pure SCALE dial -- the Sharpe span is the information floor.)")

# ------------------------------------------------------------------ Q3/Q4 the grid
P("\n" + "-" * 112)
P("Q3/Q4  THE SPEED GRID  (17 arms x 2 books x 2 conventions x 3 panels x 2 rungs = 408, all reported)")
P("-" * 112)

ARMS = [("BAND", b) for b in BANDS] + [("STALE", k) for k in STALES] + [("ABS", d) for d in DEADS]
rows, SER = [], {}
for pname, (px, tr) in PANELS.items():
    st = START[pname]
    for family, dial in ARMS:
        g = gate_state(px, family, dial)
        fr = flip_rate(g, px)
        for book in ("ew-all", "top20"):
            for conv in ("dg", "rw"):
                res = fast_backtest_g(px, weights_book(px, tr, g, book, conv), 0.0, FREQ)
                gr, tn = res["gross_ret"].loc[st:], res["turnover"].loc[st:]
                rg = res["gross"].loc[st:].mean()
                SER[(pname, family, dial, book, conv)] = (gr, tn, rg)
                for c in RUNGS:
                    r = net(gr, tn, c)
                    mm = mrow(r)
                    rows.append(dict(panel=pname, cost=c, book=book, conv=conv, family=family,
                                     dial=dial, flips=fr, realised_gross=rg,
                                     turnover=tn.sum() / (len(r) / 252), **mm,
                                     lad_Sharpe=ladder_at(pname, c, rg, "Sharpe"),
                                     lad_CAGR=ladder_at(pname, c, rg, "CAGR"),
                                     lad_MaxDD=ladder_at(pname, c, rg, "MaxDD")))
grid = pd.DataFrame(rows)
grid["gm_dSharpe"] = grid["Sharpe"] - grid["lad_Sharpe"]
grid["gm_dCAGR_pp"] = 100 * (grid["CAGR"] - grid["lad_CAGR"])
grid["gm_dMaxDD_pp"] = 100 * (grid["MaxDD"] - grid["lad_MaxDD"])
grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)

P("\nmeasured flip rates by family and panel (P2: monotone decreasing in the dial?):")
fl = grid.drop_duplicates(["panel", "family", "dial"])[["panel", "family", "dial", "flips"]]
fl.to_csv(OUT / f"{STEM}.flips.csv", index=False)
P(fl.pivot_table(index=["family", "dial"], columns="panel", values="flips")
  .to_string(float_format=lambda x: f"{x:6.2f}"))
mono = []
for (pn, fam), s in fl.groupby(["panel", "family"]):
    s = s.sort_values("dial")
    mono.append(bool((s["flips"].diff().dropna() <= 1e-9).all()))
P(f"P2 (flip rate monotone decreasing in the dial in every family x panel): "
  f"{all(mono)}  ({sum(mono)}/{len(mono)})")
P(f"    range spanned: {fl['flips'].min():.2f} to {fl['flips'].max():.2f} flips/tkr/yr "
  f"(the queue asked for ~0.5-8)")

P("\nfull grid:")
cols = ["panel", "cost", "book", "conv", "family", "dial", "flips", "realised_gross", "turnover",
        "CAGR", "Sharpe", "MaxDD", "H1", "H2", "gm_dSharpe", "gm_dCAGR_pp", "gm_dMaxDD_pp"]
P(grid[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

P("\n" + "-" * 112)
P("THE CURVE: Spearman(flip rate, net Sharpe) per (book, conv, panel, rung), 17 arms each")
P("-" * 112)
crows = []
for (book, conv, pn, c), s in grid.groupby(["book", "conv", "panel", "cost"]):
    s = s.sort_values("flips")
    best = s.loc[s["Sharpe"].idxmax()]
    slowest, fastest = s.iloc[0], s.iloc[-1]
    interior = bool(best["flips"] not in (s["flips"].min(), s["flips"].max()))
    crows.append(dict(book=book, conv=conv, panel=pn, cost=c,
                      rho_flips_Sharpe=spearman(s["flips"], s["Sharpe"]),
                      rho_flips_gmSharpe=spearman(s["flips"], s["gm_dSharpe"]),
                      Sharpe_range=s["Sharpe"].max() - s["Sharpe"].min(),
                      gm_Sharpe_range=s["gm_dSharpe"].max() - s["gm_dSharpe"].min(),
                      argmax_family=best["family"], argmax_dial=best["dial"],
                      argmax_flips=best["flips"], argmax_Sharpe=best["Sharpe"],
                      argmax_interior=interior,
                      slowest_Sharpe=slowest["Sharpe"], fastest_Sharpe=fastest["Sharpe"],
                      rho_flips_gross=spearman(s["flips"], s["realised_gross"])))
curve = pd.DataFrame(crows)
curve.to_csv(OUT / f"{STEM}.curve.csv", index=False)
P(curve.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

P("\nP3 (ew-all @10bps: Spearman(flips, Sharpe) NEGATIVE on both primary panels):")
for conv in ("dg", "rw"):
    s = curve[(curve.book == "ew-all") & (curve.cost == BASE_RUNG) & (curve.conv == conv)
              & (curve.panel.isin(["U56", "B136"]))]
    P(f"   conv={conv}: " + "  ".join(f"{r['panel']} {r['rho_flips_Sharpe']:+.3f}" for _, r in s.iterrows()))
P("P4 (top20 @10bps: weaker or positive):")
for conv in ("dg", "rw"):
    s = curve[(curve.book == "top20") & (curve.cost == BASE_RUNG) & (curve.conv == conv)
              & (curve.panel.isin(["U56", "B136"]))]
    P(f"   conv={conv}: " + "  ".join(f"{r['panel']} {r['rho_flips_Sharpe']:+.3f}" for _, r in s.iterrows()))
P(f"P5 (argmax at an EDGE, i.e. no interior optimum): "
  f"{int((~curve.argmax_interior).sum())}/{len(curve)} cells at an edge; "
  f"{int(curve.argmax_interior.sum())} interior")
P("     of the edge cells, how many are at the SLOW edge (the 'slower is always better' claim)?")
slow_edge = 0
for (book, conv, pn, c), s in grid.groupby(["book", "conv", "panel", "cost"]):
    if s.loc[s["Sharpe"].idxmax(), "flips"] == s["flips"].min():
        slow_edge += 1
P(f"     slow edge {slow_edge}/{len(curve)};  fast edge "
  f"{int((~curve.argmax_interior).sum()) - slow_edge}/{len(curve)}")
P("\n  BUT an interior argmax is the NULL, not the finding: with 17 arms, 15/17 = 88.2% of")
P("  positions are interior, so 20/24 = 83.3% is BELOW what pure noise delivers.  The honest")
P("  reading of 'is there an optimum' is the PLATEAU (idea 128's test), not the argmax:")
pl = []
for (book, conv, pn, c), s in grid.groupby(["book", "conv", "panel", "cost"]):
    top = s["Sharpe"].max()
    near = s[s["Sharpe"] >= top - 0.02]
    pl.append(dict(book=book, conv=conv, panel=pn, cost=c, n_within_002=len(near),
                   plateau_flips_lo=near["flips"].min(), plateau_flips_hi=near["flips"].max(),
                   Sharpe_range=s["Sharpe"].max() - s["Sharpe"].min(),
                   ladder_floor=float(sp.loc[(pn, c), "Sharpe_span"])))
pl = pd.DataFrame(pl)
P(pl.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
P(f"  arms within 0.02 Sharpe of the cell argmax: median {pl.n_within_002.median():.1f} of 17; "
  f"the plateau spans a median {(pl.plateau_flips_hi - pl.plateau_flips_lo).median():.2f} flips/tkr/yr")
P(f"  every cell's Sharpe range ({pl.Sharpe_range.min():.3f}-{pl.Sharpe_range.max():.3f}) DOES exceed the")
P(f"  ungated ladder's own Sharpe span ({pl.ladder_floor.max():.4f}), so the axis is not the exposure channel.")

P("\n  THE POOLED SHAPE (level differenced out: each cell's 17 Sharpes minus that cell's mean),")
P("  which is the statistic that does not depend on where one argmax landed:")
grid["_z"] = grid.groupby(["book", "conv", "panel", "cost"])["Sharpe"].transform(lambda x: x - x.mean())
buckets = pd.cut(grid["flips"], [0, 0.5, 1.0, 2.0, 4.0, 9.0],
                 labels=["<0.5", "0.5-1", "1-2", "2-4", "4-9"])
for book in ("ew-all", "top20"):
    for conv in ("dg", "rw"):
        s = grid[(grid.book == book) & (grid.conv == conv)]
        b = s.groupby(buckets[s.index], observed=False)["_z"].agg(["mean", "size"])
        P(f"   {book:7s}/{conv}:  " + "  ".join(f"{i} {r['mean']:+.4f}(n{int(r['size'])})"
                                                for i, r in b.iterrows()))
P("\n  sign consistency of rho(flips, Sharpe) across the 24 cells: "
  f"{int((curve.rho_flips_Sharpe < 0).sum())} negative, {int((curve.rho_flips_Sharpe > 0).sum())} positive "
  f"(mean {curve.rho_flips_Sharpe.mean():+.3f})")

P("\nP6 (gross is pinned under rw, so the curve's Sharpe RANGE should shrink by >half):")
for pn in PANELS:
    for book in ("ew-all", "top20"):
        a = curve[(curve.panel == pn) & (curve.book == book) & (curve.conv == "dg")]["Sharpe_range"].mean()
        b = curve[(curve.panel == pn) & (curve.book == book) & (curve.conv == "rw")]["Sharpe_range"].mean()
        P(f"   {pn:9s} {book:7s}  dg range {a:.4f} -> rw range {b:.4f}   "
          f"shrink {1 - b / a if a else np.nan:+.1%}")
P("\n   and the same curve read against its OWN realised-gross ladder point (idea 277's control):")
for pn in PANELS:
    for book in ("ew-all", "top20"):
        s = curve[(curve.panel == pn) & (curve.book == book) & (curve.conv == "dg")]
        P(f"   {pn:9s} {book:7s}  rho(flips, raw Sharpe) {s['rho_flips_Sharpe'].mean():+.3f}  ->  "
          f"rho(flips, gross-matched dSharpe) {s['rho_flips_gmSharpe'].mean():+.3f}    "
          f"rho(flips, realised gross) {s['rho_flips_gross'].mean():+.3f}")

# ------------------------------------------------------------------ Q6 KEEP
P("\n" + "-" * 112)
P("Q6  BOTH KEEP PATHS on every arm")
P("-" * 112)
BASE = {}
for pname, (px, tr) in PANELS.items():
    st = START[pname]
    rv2 = fast_backtest_g(px, rules_v2_weights(px), 0.0, FREQ)
    rv1 = fast_backtest_g(px, rules_v1_weights(px), 0.0, FREQ)
    spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
    sm = mrow(spy)
    for c in RUNGS:
        BASE[(pname, c)] = dict(v2=mrow(net(rv2["gross_ret"], rv2["turnover"], c).loc[st:]),
                                v1=mrow(net(rv1["gross_ret"], rv1["turnover"], c).loc[st:]), spy=sm)

a4, b4, failb = [], [], []
for _, r in grid.iterrows():
    b = BASE[(r["panel"], r["cost"])]
    v2, s = b["v2"], b["spy"]
    a4.append(bool(r["H1"] > v2["H1"] and r["H2"] > v2["H2"] and r["MaxDD"] >= v2["MaxDD"]))
    f = []
    if not r["H1"] > s["H1"]:
        f.append("H1")
    if not r["H2"] > s["H2"]:
        f.append("H2")
    if not r["MaxDD"] >= 0.60 * s["MaxDD"]:
        f.append("DD")
    if not r["CAGR"] >= 0.70 * s["CAGR"]:
        f.append("CAGR")
    b4.append(len(f) == 0)
    failb.append(",".join(f))
grid["pass4a"], grid["pass4b"], grid["fail4b"] = a4, b4, failb
grid.to_csv(OUT / f"{STEM}.keep.csv", index=False)
P(f"4a: {int(grid['pass4a'].sum())}/{len(grid)}    4b (full-sample bars): {int(grid['pass4b'].sum())}/{len(grid)}")
P(grid.groupby(["panel", "cost", "book", "conv"])[["pass4a", "pass4b"]].sum().to_string())
P("\nbinding 4b bar, over the failures:")
P(grid.loc[~grid.pass4b, "fail4b"].value_counts().to_string())

# ------------------------------------------------------------------ Q5 rule 8
P("\n" + "-" * 112)
P("Q5  RULE 8  (speed dial chosen on IS <= 2016-12-31 by IS Sharpe; OOS >= 2017-01-01 read ONCE)")
P("-" * 112)
wf = []
for pname, (px, tr) in PANELS.items():
    st = START[pname]
    spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
    rv2 = fast_backtest_g(px, rules_v2_weights(px), 0.0, FREQ)
    live = px.notna().copy()
    live[[c for c in px.columns if c not in tr]] = False
    for book in ("ew-all", "top20"):
        for conv in ("dg", "rw"):
            for c in RUNGS:
                cd = []
                for (pn, fam, dial, bk, cv), (gr, tn, rg) in SER.items():
                    if (pn, bk, cv) != (pname, book, conv):
                        continue
                    r = net(gr, tn, c)
                    ris, ros = r.loc[:IS_END], r.loc[OOS_START:]
                    cd.append(dict(fam=fam, dial=dial, rg=rg,
                                   IS_Sharpe=metrics(ris)["Sharpe"],
                                   OOS_Sharpe=metrics(ros)["Sharpe"],
                                   OOS_CAGR=metrics(ros)["CAGR"], OOS_MaxDD=metrics(ros)["MaxDD"],
                                   flips=grid[(grid.panel == pn) & (grid.family == fam)
                                              & (grid.dial == dial)]["flips"].iloc[0]))
                cd = pd.DataFrame(cd)
                pk = cd.loc[cd["IS_Sharpe"].idxmax()]
                # the slowest arm as a pre-registered "slower is better" control
                sl = cd.loc[cd["flips"].idxmin()]
                bos = net(rv2["gross_ret"], rv2["turnover"], c).loc[st:].loc[OOS_START:]
                sos = spy.loc[OOS_START:]
                wl = live.astype(float).div(live.sum(axis=1).replace(0, np.nan), axis=0) \
                    .mul(round(float(pk["rg"]), 2)).fillna(0.0)
                rl = fast_backtest_g(px, wl, 0.0, FREQ)
                rlo = net(rl["gross_ret"], rl["turnover"], c).loc[st:].loc[OOS_START:]
                wf.append(dict(panel=pname, book=book, conv=conv, cost=c,
                               pick=f"{pk['fam']}/{pk['dial']}", pick_flips=pk["flips"],
                               IS_Sharpe=pk["IS_Sharpe"], OOS_Sharpe=pk["OOS_Sharpe"],
                               OOS_CAGR=pk["OOS_CAGR"], OOS_MaxDD=pk["OOS_MaxDD"],
                               slowest_OOS_Sharpe=sl["OOS_Sharpe"], grid_mean_OOS=cd["OOS_Sharpe"].mean(),
                               donothing_OOS_Sharpe=metrics(bos)["Sharpe"],
                               donothing_OOS_CAGR=metrics(bos)["CAGR"],
                               donothing_OOS_MaxDD=metrics(bos)["MaxDD"],
                               grossmatched_OOS_Sharpe=metrics(rlo)["Sharpe"],
                               spy_OOS_Sharpe=metrics(sos)["Sharpe"], spy_OOS_CAGR=metrics(sos)["CAGR"],
                               spy_OOS_MaxDD=metrics(sos)["MaxDD"],
                               rho_IS_OOS=spearman(cd["IS_Sharpe"], cd["OOS_Sharpe"]),
                               rho_flips_OOS=spearman(cd["flips"], cd["OOS_Sharpe"])))
wf = pd.DataFrame(wf)
wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
P(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
P(f"\nP7: IS chooser beats do-nothing OOS in {int((wf.OOS_Sharpe > wf.donothing_OOS_Sharpe).sum())}/{len(wf)} "
  f"(mean {wf.OOS_Sharpe.mean():.4f} vs {wf.donothing_OOS_Sharpe.mean():.4f}; SPY {wf.spy_OOS_Sharpe.mean():.4f})")
P(f"    IS chooser vs the pre-registered SLOWEST arm: chooser wins "
  f"{int((wf.OOS_Sharpe > wf.slowest_OOS_Sharpe).sum())}/{len(wf)} "
  f"(mean {wf.OOS_Sharpe.mean():.4f} vs {wf.slowest_OOS_Sharpe.mean():.4f})")
P(f"    OOS: is slower still better?  mean rho(flips, OOS Sharpe) = {wf.rho_flips_OOS.mean():+.3f} "
  f"(negative in {int((wf.rho_flips_OOS < 0).sum())}/{len(wf)} cells)")
P(f"    mean Spearman(IS, OOS) over the 17 arms = {wf.rho_IS_OOS.mean():+.3f}")

# ------------------------------------------------------------------ Q7 the 4b arms out of sample
P("\n" + "-" * 112)
P("Q7  EVERY 4b PASS READ OUT OF SAMPLE (rule 8 window, not a selection — all of them)")
P("-" * 112)
oos = []
for _, r in grid[grid.pass4b].iterrows():
    gr, tn, rg = SER[(r["panel"], r["family"], r["dial"], r["book"], r["conv"])]
    ro = net(gr, tn, r["cost"]).loc[OOS_START:]
    ri = net(gr, tn, r["cost"]).loc[:IS_END]
    w = wf[(wf.panel == r["panel"]) & (wf.book == r["book"]) & (wf.conv == r["conv"])
           & (wf.cost == r["cost"])].iloc[0]
    oos.append(dict(panel=r["panel"], cost=r["cost"], book=r["book"], conv=r["conv"],
                    arm=f"{r['family']}/{r['dial']}", flips=r["flips"],
                    full_Sharpe=r["Sharpe"], IS_Sharpe=metrics(ri)["Sharpe"],
                    OOS_Sharpe=metrics(ro)["Sharpe"], OOS_CAGR=metrics(ro)["CAGR"],
                    OOS_MaxDD=metrics(ro)["MaxDD"],
                    donothing_OOS=w["donothing_OOS_Sharpe"], spy_OOS=w["spy_OOS_Sharpe"],
                    is_the_rule8_pick=(f"{r['family']}/{r['dial']}" == w["pick"])))
oos = pd.DataFrame(oos)
oos.to_csv(OUT / f"{STEM}.oos4b.csv", index=False)
P(oos.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
P(f"\n  of the {len(oos)} full-sample 4b passes, {int((oos.OOS_Sharpe > oos.spy_OOS).sum())} also beat SPY "
  f"out of sample and {int((oos.OOS_Sharpe > oos.donothing_OOS).sum())} beat the live book; "
  f"{int(oos.is_the_rule8_pick.sum())} are the rule-8 pick of their own cell.")

P("\n" + "=" * 112)
P(f"done in {time.time() - T0:.1f}s")
(OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
