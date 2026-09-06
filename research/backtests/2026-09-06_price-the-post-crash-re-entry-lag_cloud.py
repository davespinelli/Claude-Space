#!/usr/bin/env python3
"""QUEUE idea 274 — price-the-post-crash-re-entry-lag (cloud, 2026-09-06).

Question (pre-registered, verbatim from QUEUE)
----------------------------------------------
"idea 70 localised the ENTIRE residual H2 gap to one 21-day window, 2020-03-24 -> 2020-04-22
(permutation pctile 1.0%), where the 200d gate had de-risked the book and it re-entered too
slowly; deleting the window flips dSharpe -0.023 -> +0.120.  Test a fast re-entry instrument
that only fires after a >20% SPY drawdown (e.g. re-enter on price > 20d MA rather than 200d,
for 60 days after the trough) on both universes, and report whether it pays for itself
outside 2020.  Max 2 params."

The instrument (pre-registered before any number was read)
---------------------------------------------------------
Base book = the LIVE book, RULES v2: equal-weight every name inside the 200d +/-3% hysteresis
band at 0.75/N of NAV, gated-out weight to CASH, weekly, t+1.  The overlay changes ONE thing:

    A crash episode ARMS when SPY's drawdown from its running high reaches -D (decided on
    closes through t-1 only).  While armed, the running trough is tracked; for the L trading
    days that follow the LATEST trough the book's per-name gate is replaced by the fast gate
    `px > 20d MA`.  Names still de-gross to cash when the fast gate is false, so gross is not
    forced up — the overlay only lets a name back IN sooner.  The episode DISARMS when SPY has
    recovered to within 5% of its high (a new crash can then re-arm), and the fast window
    lapses on its own after L days even if the drawdown persists, at which point the ordinary
    band gate governs again.

Tuned parameters (PROTOCOL rule 4).  TWO and no more: D (crash trigger) and L (fast-window
length).  The fast MA is fixed at 20 days, the disarm level at -5% and the base book at the
live RULES v2 settings; none of them is searched.  ALL 9 grid points (D x L) are reported
beside the un-overlaid control on every panel and both cost rungs — nothing is selected.

Grid: D in {0.15, 0.20, 0.25} x L in {30, 60, 90} trading days, panels {U56, B136, SMALL439},
costs {10, 25} bps = 60 overlay cells + 6 controls.

"Does it pay for itself outside 2020" is answered three ways, all reported
    (a) the full-sample delta vs the control (CAGR / Sharpe / MaxDD / turnover);
    (b) the same delta with calendar 2020 DELETED from the return series of both books;
    (c) an episode census: every armed episode on every panel with its start, trough, fast
        window, and the overlay's cumulative return delta inside that window — so the number
        of independent events behind any headline is visible rather than implied.

Walk-forward (PROTOCOL rule 8), selection fixed before any OOS number was read
    S1  Choose (D, L) by IS (2009-2016) Sharpe of the overlaid book, evaluate 2017-2026
        untouched vs the control, vs live RULES v2 and vs SPY.
    S2  Report the number of armed episodes inside the IS window per D.  If a D never arms in
        2009-2016 the parameter is UNCHOOSABLE in sample and the walk-forward for it is
        vacuous; that is reported as the result, not papered over with a full-sample number.

Both KEEP paths are evaluated at every grid point (4a vs live RULES v2 on the same panel, 4b
vs SPY).

Panels: U56 (research/universe.json, 56 instruments, the live panel — SPY is a constituent and
RULES v2 holds it), B136 (research/universe_broad.json), SMALL439 (data/prices_small.csv minus
the 44 names with max_1d_move >= 1.0 in data/small_meta.csv).
SURVIVORSHIP: all three are current-constituent lists; SMALL439 has no delistings at all, so
its levels are optimistic by an unknown one-directional margin concentrated in beaten-down
names — the very cohort a re-entry rule buys.  Read the SMALL439 deltas as an upper bound.

Execution realism (PROTOCOL rule 2): weights decided at close t applied at t+1, weekly
rebalance (the fast gate therefore acts at the next weekly rebalance, not intra-week — this is
the honest form of the live book, and it is stated because it caps how fast "fast" can be),
long-only, no leverage, 10 bps PROTOCOL rung plus 25 bps.

Deterministic, standalone.  Imports research/baseline.py; modifies nothing.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = ROOT / "research" / "backtests" / "2026-09-06_price-the-post-crash-re-entry-lag_cloud"
FREQ, GROSS, BAND, FASTMA, DISARM = "W", 0.75, 0.03, 20, 0.05
COSTS = [10.0, 25.0]
DS = [0.15, 0.20, 0.25]
LS = [10, 20, 30, 60, 90]   # 30 was the argmax of the pre-registered {30, 60, 90} grid and sat
                            # on its EDGE, so the grid is extended DOWN before anything is
                            # concluded; all 5 rungs are reported and none is dropped.
IS_END, OOS_START = "2016-12-31", "2017-01-01"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 3000)
_LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


def build_panels():
    out = {}
    px = load_universe().dropna(how="all").ffill()
    out["U56"] = (px, list(px.columns))
    pb = load_universe(broad=True)
    out["B136"] = (pb, [c for c in pb.columns if c != "SPY"])
    ps = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    stk = [c for c in ps.columns if c != "SPY" and c not in bad]
    ps = ps[stk + ["SPY"]].dropna(how="all").ffill()
    out["SMALL439"] = (ps, stk)
    for k, (p, t) in out.items():
        P(f"  {k:9s} {p.shape[1]:4d} cols, {len(t):4d} tradable, {p.index[0].date()} -> {p.index[-1].date()}")
    P(f"  SMALL439 dropped {len([c for c in ps.columns if c in bad])} names with max_1d_move >= 1.0")
    return out


# ------------------------------------------------------------------ the overlay state machine
def fast_window(spy, D, L):
    """Boolean series: True on days whose weights are decided under the fast gate.

    Uses only closes through t (weights decided at t are applied at t+1 by the engine, so
    reading spy[t] here is not look-ahead).  Returns the mask plus an episode census.
    """
    s = spy.values
    n = len(s)
    peak = -np.inf
    armed = False
    trough = np.inf
    since = 0
    mask = np.zeros(n, dtype=bool)
    eps, cur = [], None
    for i in range(n):
        p = s[i]
        peak = max(peak, p)
        dd = p / peak - 1.0
        if not armed and dd <= -D:
            armed, trough, since = True, p, 0
            cur = dict(armed_on=spy.index[i], trigger_dd=dd, trough_on=spy.index[i], trough_px=p)
        elif armed:
            if p < trough:
                trough, since = p, 0
                cur["trough_on"], cur["trough_px"] = spy.index[i], p
            else:
                since += 1
            if dd > -DISARM:                       # recovered: episode over, can re-arm later
                armed = False
                cur["disarmed_on"] = spy.index[i]
                eps.append(cur)
                cur = None
                continue
        if armed and since <= L:
            mask[i] = True
    if cur is not None:
        cur["disarmed_on"] = spy.index[-1]
        eps.append(cur)
    return pd.Series(mask, index=spy.index), eps


def weights(px, tradable, spy, D=None, L=None):
    """RULES v2 weights, with the fast 20d gate substituted inside the fast window."""
    e = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    e[tradable] = px[tradable].notna().astype(float)
    ew = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    gate = band_state(px, BAND)
    if D is not None:
        fw, _ = fast_window(spy, D, L)
        fast = (px > px.rolling(FASTMA).mean()).fillna(False)
        fwdf = pd.DataFrame(np.broadcast_to(fw.values[:, None], gate.shape),
                            index=gate.index, columns=gate.columns)
        gate = gate.where(~fwdf, fast)
    return ew.where(gate.reindex(columns=ew.columns, fill_value=False), 0.0)


def mm(r):
    m = metrics(r)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def ex2020(r):
    return r[r.index.year != 2020]


def main():
    P("=" * 120)
    P("idea 274 — does a fast post-crash re-entry pay for itself outside 2020?")
    P("=" * 120)
    panels = build_panels()

    rows, epi_rows, wf_rows = [], [], []
    for pname, (px, trad) in panels.items():
        spy = px["SPY"]
        start = px.index[260]
        sl = slice(start, px.index[-1])
        is_sl = slice(start, pd.Timestamp(IS_END))
        oos_sl = slice(pd.Timestamp(OOS_START), px.index[-1])
        spy_r = spy.pct_change().fillna(0.0)

        # ---- episode census (panel-independent except for the trading calendar)
        for D in DS:
            _, eps = fast_window(spy.loc[start:], D, max(LS))
            for e in eps:
                epi_rows.append(dict(panel=pname, D=D, armed_on=e["armed_on"].date(),
                                     trough_on=e["trough_on"].date(),
                                     disarmed_on=e["disarmed_on"].date(),
                                     trigger_dd=e["trigger_dd"],
                                     in_IS=bool(e["armed_on"] <= pd.Timestamp(IS_END))))
        P(f"\n{'='*120}\nPANEL {pname}   sample {start.date()} -> {px.index[-1].date()}")
        ec = pd.DataFrame([e for e in epi_rows if e["panel"] == pname])
        P("  crash episodes (SPY drawdown reaching -D), by trigger:")
        P(ec.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        for D in DS:
            n_is = int(((ec.D == D) & ec.in_IS).sum())
            P(f"    D={D:.2f}: {int((ec.D==D).sum())} episodes total, {n_is} inside the IS window "
              f"(2009-2016)" + ("  <-- UNCHOOSABLE in sample" if n_is == 0 else ""))

        W0 = weights(px, trad, spy)
        Wg = {(D, L): weights(px, trad, spy, D, L) for D in DS for L in LS}
        for bps in COSTS:
            ctl = backtest(px, W0, cost_bps=bps, freq=FREQ)
            c_r = ctl["returns"]
            cm, cm_x, cm_is, cm_oos = mm(c_r.loc[sl]), mm(ex2020(c_r.loc[sl])), mm(c_r.loc[is_sl]), mm(c_r.loc[oos_sl])
            spm, spm_x = mm(spy_r.loc[sl]), mm(ex2020(spy_r.loc[sl]))
            spm_oos = mm(spy_r.loc[oos_sl])
            yrs = len(c_r.loc[sl]) / 252
            rows.append(dict(panel=pname, bps=bps, D=np.nan, L=np.nan, arm="control(v2)",
                             **{k: v for k, v in cm.items()},
                             turnover=ctl["turnover"].loc[sl].sum() / yrs,
                             CAGR_x20=cm_x["CAGR"], Sharpe_x20=cm_x["Sharpe"], MaxDD_x20=cm_x["MaxDD"],
                             dCAGR=0.0, dSharpe=0.0, dMaxDD=0.0, dCAGR_x20=0.0, dSharpe_x20=0.0,
                             dMaxDD_x20=0.0, IS_Sharpe=cm_is["Sharpe"], OOS_CAGR=cm_oos["CAGR"],
                             OOS_Sharpe=cm_oos["Sharpe"], OOS_MaxDD=cm_oos["MaxDD"],
                             p4a=False, p4b_halves=cm["H1"] > spm["H1"] and cm["H2"] > spm["H2"],
                             p4b_dd=abs(cm["MaxDD"]) <= 0.60 * abs(spm["MaxDD"]),
                             p4b_cagr=cm["CAGR"] >= 0.70 * spm["CAGR"]))
            for D in DS:
                for L in LS:
                    res = backtest(px, Wg[(D, L)], cost_bps=bps, freq=FREQ)
                    r = res["returns"]
                    a, ax, ais, aoos = mm(r.loc[sl]), mm(ex2020(r.loc[sl])), mm(r.loc[is_sl]), mm(r.loc[oos_sl])
                    rows.append(dict(
                        panel=pname, bps=bps, D=D, L=L, arm=f"fast{FASTMA}-D{int(D*100)}-L{L}",
                        **{k: v for k, v in a.items()},
                        turnover=res["turnover"].loc[sl].sum() / yrs,
                        CAGR_x20=ax["CAGR"], Sharpe_x20=ax["Sharpe"], MaxDD_x20=ax["MaxDD"],
                        dCAGR=a["CAGR"] - cm["CAGR"], dSharpe=a["Sharpe"] - cm["Sharpe"],
                        dMaxDD=abs(cm["MaxDD"]) - abs(a["MaxDD"]),
                        dCAGR_x20=ax["CAGR"] - cm_x["CAGR"], dSharpe_x20=ax["Sharpe"] - cm_x["Sharpe"],
                        dMaxDD_x20=abs(cm_x["MaxDD"]) - abs(ax["MaxDD"]),
                        IS_Sharpe=ais["Sharpe"], OOS_CAGR=aoos["CAGR"], OOS_Sharpe=aoos["Sharpe"],
                        OOS_MaxDD=aoos["MaxDD"],
                        p4a=bool(a["H1"] > cm["H1"] and a["H2"] > cm["H2"]
                                 and abs(a["MaxDD"]) <= abs(cm["MaxDD"])),
                        p4b_halves=bool(a["H1"] > spm["H1"] and a["H2"] > spm["H2"]),
                        p4b_dd=bool(abs(a["MaxDD"]) <= 0.60 * abs(spm["MaxDD"])),
                        p4b_cagr=bool(a["CAGR"] >= 0.70 * spm["CAGR"])))
            sub = pd.DataFrame([x for x in rows if x["panel"] == pname and x["bps"] == bps])
            P(f"\n  cost {bps:.0f} bps — full sample and 2020-deleted, vs the un-overlaid v2 control")
            P(sub[["arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "turnover", "dCAGR", "dSharpe",
                   "dMaxDD", "CAGR_x20", "Sharpe_x20", "dCAGR_x20", "dSharpe_x20", "dMaxDD_x20"]]
              .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
            P(f"    SPY on this panel: full {spm['CAGR']:.2%}/{spm['Sharpe']:.4f}/{spm['MaxDD']:.2%}  "
              f"ex-2020 {spm_x['CAGR']:.2%}/{spm_x['Sharpe']:.4f}/{spm_x['MaxDD']:.2%}  "
              f"OOS {spm_oos['CAGR']:.2%}/{spm_oos['Sharpe']:.4f}/{spm_oos['MaxDD']:.2%}")

            # ---- rule 8: (D, L) chosen on IS Sharpe, evaluated untouched OOS
            arms = [x for x in rows if x["panel"] == pname and x["bps"] == bps and x["arm"] != "control(v2)"]
            pick = max(arms, key=lambda x: x["IS_Sharpe"])
            n_is_eps = int(((ec.D == pick["D"]) & ec.in_IS).sum())
            wf_rows.append(dict(panel=pname, bps=bps, pick=pick["arm"], D=pick["D"], L=pick["L"],
                                IS_Sharpe=pick["IS_Sharpe"], ctl_IS_Sharpe=cm_is["Sharpe"],
                                is_episodes_for_D=n_is_eps,
                                OOS_CAGR=pick["OOS_CAGR"], OOS_Sharpe=pick["OOS_Sharpe"],
                                OOS_MaxDD=pick["OOS_MaxDD"],
                                ctl_OOS_CAGR=cm_oos["CAGR"], ctl_OOS_Sharpe=cm_oos["Sharpe"],
                                ctl_OOS_MaxDD=cm_oos["MaxDD"],
                                spy_OOS_CAGR=spm_oos["CAGR"], spy_OOS_Sharpe=spm_oos["Sharpe"],
                                spy_OOS_MaxDD=spm_oos["MaxDD"],
                                dOOS_Sharpe=pick["OOS_Sharpe"] - cm_oos["Sharpe"],
                                dOOS_CAGR=pick["OOS_CAGR"] - cm_oos["CAGR"],
                                dOOS_MaxDD=abs(cm_oos["MaxDD"]) - abs(pick["OOS_MaxDD"])))

    grid = pd.DataFrame(rows)
    epis = pd.DataFrame(epi_rows)
    wf = pd.DataFrame(wf_rows)
    grid.to_csv(f"{STEM}.grid.csv", index=False)
    epis.to_csv(f"{STEM}.episodes.csv", index=False)
    wf.to_csv(f"{STEM}.walkforward.csv", index=False)

    P("\n" + "=" * 120)
    P("SUMMARY 1 — dSharpe vs the un-overlaid RULES v2 control, full sample (positive = the overlay helps)")
    P("=" * 120)
    t = grid[grid.arm != "control(v2)"]
    for bps in COSTS:
        P(f"\n  cost {bps:.0f} bps")
        P(t[t.bps == bps].pivot_table(index=["panel", "D"], columns="L", values="dSharpe")
          .to_string(float_format=lambda x: f"{x:+.4f}"))
    P("\n" + "=" * 120)
    P("SUMMARY 2 — the same dSharpe with calendar 2020 DELETED (this is the QUEUE's question)")
    P("=" * 120)
    for bps in COSTS:
        P(f"\n  cost {bps:.0f} bps")
        P(t[t.bps == bps].pivot_table(index=["panel", "D"], columns="L", values="dSharpe_x20")
          .to_string(float_format=lambda x: f"{x:+.4f}"))
    P("\n" + "=" * 120)
    P("SUMMARY 3 — dCAGR (pp) full sample / ex-2020, and dMaxDD (pp, positive = shallower)")
    P("=" * 120)
    for bps in COSTS:
        for v, lab in (("dCAGR", "dCAGR full"), ("dCAGR_x20", "dCAGR ex-2020"),
                       ("dMaxDD", "dMaxDD full"), ("dMaxDD_x20", "dMaxDD ex-2020")):
            P(f"\n  {lab}, cost {bps:.0f} bps (pp)")
            P((t[t.bps == bps].pivot_table(index=["panel", "D"], columns="L", values=v) * 100)
              .to_string(float_format=lambda x: f"{x:+.2f}"))
    P("\n  sign counts over all 60 overlay cells:")
    P(f"    dSharpe      > 0 in {int((t.dSharpe > 0).sum())} / {len(t)}")
    P(f"    dSharpe_x20  > 0 in {int((t.dSharpe_x20 > 0).sum())} / {len(t)}")
    P(f"    dCAGR        > 0 in {int((t.dCAGR > 0).sum())} / {len(t)}")
    P(f"    dCAGR_x20    > 0 in {int((t.dCAGR_x20 > 0).sum())} / {len(t)}")
    P(f"    dMaxDD       > 0 in {int((t.dMaxDD > 0).sum())} / {len(t)}")

    P("\n" + "=" * 120)
    P("SUMMARY 4 — episode census (the number of independent events behind every number above)")
    P("=" * 120)
    P(epis.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n" + "=" * 120)
    P("SUMMARY 5 — rule 8 walk-forward, (D, L) chosen by IS Sharpe, evaluated untouched on 2017-2026")
    P("=" * 120)
    P(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  OOS dSharpe > 0 in {int((wf.dOOS_Sharpe > 0).sum())} of {len(wf)} panel x cost cells; "
      f"mean {wf.dOOS_Sharpe.mean():+.4f}")
    P(f"  cells whose IS-chosen D never armed in sample: {int((wf.is_episodes_for_D == 0).sum())} of {len(wf)}")

    P("\n" + "=" * 120)
    P("SUMMARY 6 — KEEP paths at every grid point")
    P("=" * 120)
    g2 = grid.copy()
    g2["p4b"] = g2.p4b_halves & g2.p4b_dd & g2.p4b_cagr
    P(f"  4a passes (vs the v2 control on the same panel): {int(g2.p4a.sum())} of {len(g2)}")
    P(f"  4b passes (vs SPY): {int(g2.p4b.sum())} of {len(g2)}")
    for flag in ("p4a", "p4b"):
        if g2[flag].any():
            P(f"\n  {flag} passes:")
            P(g2[g2[flag]][["panel", "bps", "arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "turnover"]]
              .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\n  4b bar failures among overlay cells: "
      f"halves {int((~g2[g2.arm!='control(v2)'].p4b_halves).sum())}, "
      f"dd {int((~g2[g2.arm!='control(v2)'].p4b_dd).sum())}, "
      f"cagr {int((~g2[g2.arm!='control(v2)'].p4b_cagr).sum())} of "
      f"{len(g2[g2.arm!='control(v2)'])}")

    Path(f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")
    P(f"\nwrote {STEM.name}.grid.csv / .episodes.csv / .walkforward.csv / .console.txt")
    Path(f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
