#!/usr/bin/env python3
"""Idea 1682 (lane cloud, 2026-09-19): is the BAND's NET SHARPE CREDIT a TURNOVER BUDGET
rather than a PANEL FACT?

Idea 1670 priced the live band book (RULES v2 clause 2 + clause 6 SHY sleeve) against its
EXPOSURE-MATCHED static twin and found the credit POSITIVE on all three panels at 0 bps
(pooled over its five gross rungs: U56 +0.1039, B136 +0.0143, SMALL +0.0100) and NEGATIVE
on two of three at the live 10 bps rung, with candidate turnover 2.84x / 3.06x / 3.48x per
year.  That reads as a BUDGET statement, not a panel statement: the credit should die
wherever turnover x cost exceeds the gross credit, on ANY panel, and should COME BACK on
any panel once the book is slowed to the same turnover.

THE TEST: slow the band instead of changing the panel.
  cadence {D, W, M, Q}  x  band width {0.03, 0.06, 0.10}   (the two tuned dials, and no more)
  x panels {U56, B136, SMALL}  x  cost {0, 10, 25, 50} bps (reported axis, not tuned)
Gross is PINNED at the live 0.75 and the SHY sleeve convention is inherited verbatim from
1670/1674, so the W/0.03/G=0.75 cell is a bit-level replay of a committed number (G5).

PRE-REGISTERED READING (written before the grid was run):
  BUDGET-TRUE  iff, for B136 and SMALL, the cadence whose candidate turnover first falls to
               or below U56-weekly's 2.84x/yr shows a POSITIVE net dSharpe at 10 bps.
  BUDGET-FALSE iff slowing kills the GROSS (0 bps) credit at the same rate it kills
               turnover, i.e. the band's timing value is itself a cadence object.
Both outcomes are published; the break-even cost c* is solved per cell either way.

Rule 8: every chooser sees rows <= 2016-12-31 only; 2017-2026 is read ONCE.
Both KEEP paths evaluated at EVERY cell.  Deterministic, offline, no network.
Writes .grid.csv .paired.csv .walkforward.csv .gates.csv .log.txt
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state            # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics                                        # noqa: E402

OUT = Path(__file__).with_suffix("")
SAFE = "SHY"
GROSS = 0.75                      # live RULES v2 gross, PINNED (not a dial of this run)
CADENCES = ["D", "W", "M", "Q"]   # dial 1
WIDTHS = [0.03, 0.06, 0.10]       # dial 2
COSTS = [0, 10, 25, 50]
IS_END = "2016-12-31"
LADDER = [0.05, 0.20, 0.35, 0.50, 0.65, 0.80, 1.00]
LOG, GATES = [], []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); LOG.append(s)


def gate(name, val, ok, note=""):
    GATES.append(dict(gate=name, value=str(val), pass_=bool(ok), note=note))
    say(f"GATE {name}: {val}  {'PASS' if ok else 'FAIL'}  {note}")


# ---------------------------------------------------------------- panels (1670's build, verbatim)
def build_panels():
    P = {}
    u = load_universe()
    P["U56"] = (u, [c for c in u.columns if c not in (SAFE, "SPY")])
    b = load_universe(broad=True)
    P["B136"] = (b, [c for c in b.columns if c not in (SAFE, "SPY")])
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    shy = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)[SAFE]
    shy = shy.reindex(sm.index, method="ffill").rename(SAFE)
    keep = [c for c in sm.columns if c not in bad and c != "SPY"]
    P["SMALL"] = (pd.concat([sm[keep + ["SPY"]], shy], axis=1), keep)
    return P, len(bad)


# ---------------------------------------------------------------- weights (1670's clause 6 form)
def clause6_weights(px, tradable, band, gross):
    e = px[tradable].notna().astype(float)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    w = ew.where(band_state(px[tradable], band), 0.0).reindex(columns=px.columns).fillna(0.0)
    resid = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SAFE] = w[SAFE] + resid.where(px[SAFE].notna(), 0.0)
    return w


def static_mix_weights(px, tradable, a):
    e = px[tradable].notna().astype(float)
    w = a * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    w = w.reindex(columns=px.columns).fillna(0.0)
    w[SAFE] = (1.0 - a) * px[SAFE].notna().astype(float)
    return w


def run(px, wfn, tradable, freq):
    res = backtest(px, wfn(px), cost_bps=0.0, freq=freq)
    return dict(gross=res["returns"], turnover=res["turnover"],
                eq_exp=res["weights"][tradable].sum(axis=1))


def net(r, c):
    return r["gross"] - r["turnover"] * c / 1e4


def legs(ret, start):
    r = ret.loc[start:]
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    ins = metrics(r.loc[:IS_END]); oos = metrics(r.loc[pd.Timestamp(IS_END) + pd.Timedelta(days=1):])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"], H2=m2["Sharpe"],
                IS_Sharpe=ins["Sharpe"], IS_CAGR=ins["CAGR"], IS_MaxDD=ins["MaxDD"],
                OOS_CAGR=oos["CAGR"], OOS_Sharpe=oos["Sharpe"], OOS_MaxDD=oos["MaxDD"])


def sharpe_at(r, c, start):
    return float(metrics((r["gross"] - r["turnover"] * c / 1e4).loc[start:])["Sharpe"])


def breakeven_cost(cand, twin, start, lo=0.0, hi=400.0):
    """c* where the candidate's net Sharpe crosses its matched twin's.  Bisection on the
    EXACT cost algebra; returns nan if no crossing inside [lo, hi]."""
    f = lambda c: sharpe_at(cand, c, start) - sharpe_at(twin, c, start)
    flo, fhi = f(lo), f(hi)
    if flo == 0: return lo
    if flo * fhi > 0: return float("nan")
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if f(lo) * f(mid) <= 0: hi = mid
        else: lo = mid
    return 0.5 * (lo + hi)


PANELS, n_bad = build_panels()
say("# idea 1682 — is the band's NET SHARPE CREDIT a TURNOVER BUDGET rather than a PANEL FACT?")
say(f"#   gross PINNED at {GROSS} (live); dials = cadence {CADENCES} x band width {WIDTHS}; "
    f"cost axis {COSTS} bps derived EXACTLY off the c=0 run")
for k, (px, tr) in PANELS.items():
    say(f"#   {k}: {px.shape[1]} cols, {len(tr)} tradable equities, {px.index[0].date()} -> {px.index[-1].date()}")
say(f"#   SMALL screen: {n_bad} tickers with max_1d_move >= 1.0 dropped (data/small_meta.csv). "
    f"SURVIVORSHIP: the small panel is a CURRENT-CONSTITUENT screen — no delisted name is in it, "
    f"so every SMALL number here is an upper bound.")
gate("G1 SMALL max_1d_move screen applied", f"{n_bad} dropped, {len(PANELS['SMALL'][1])} tradable",
     n_bad > 0 and "SPY" not in PANELS["SMALL"][1], "data/small_meta.csv max_1d_move >= 1.0")
gate("G2 SHY present and never tradable", ", ".join(f"{k}:{SAFE in px.columns and SAFE not in tr}"
     for k, (px, tr) in PANELS.items()), all(SAFE in px.columns and SAFE not in tr for px, tr in PANELS.values()),
     "clause 6 sleeve reserved on every panel")

# ---------------------------------------------------------------- G5: replay idea 1670 EXACTLY
# 1670/1674 built U56's tradable set as "every column except SHY" — i.e. it held SPY, the
# benchmark, as an ordinary tradable name.  This run excludes SPY from the tradable set on
# every panel.  Both conventions are run on the one committed cell so the difference is a
# measured number rather than an unexplained deviation.
_u, _ = PANELS["U56"]
_START = _u.index[260]
_yrs = (_u.index[-1] - _START).days / 365.25
for _label, _tr in (("1670 convention (SPY tradable)", [c for c in _u.columns if c != SAFE]),
                    ("this run (SPY benchmark only)", [c for c in _u.columns if c not in (SAFE, "SPY")])):
    _c = run(_u, lambda p, t=_tr: clause6_weights(p, t, 0.03, GROSS), _tr, "W")
    _s = float(metrics(_c["gross"].loc[_START:])["Sharpe"])
    _t = float(_c["turnover"].loc[_START:].sum() / _yrs)
    say(f"   replay U56 W/0.03 G=0.75 @0bps under {_label}: Sharpe {_s:.6f}, turnover {_t:.6f}")
    if _label.startswith("1670"):
        gate("G5 replay of idea 1670's committed U56 W band0.03 G=0.75 cell under ITS OWN convention",
             f"Sharpe {_s:.6f} vs 1.303484 (dev {abs(_s-1.303484):.3e}), "
             f"turnover {_t:.6f} vs 2.838279 (dev {abs(_t-2.838279):.3e})",
             abs(_s - 1.303484) < 1e-4 and abs(_t - 2.838279) < 1e-4,
             "1670 held SPY as a tradable name; this run does not — G5b prices that difference")

grid, paired, wf, SPYREF = [], [], [], {}
u56_w_turn = None
for pname, (px, trad) in PANELS.items():
    START = px.index[260]
    yrs = (px.index[-1] - START).days / 365.25
    spy = px["SPY"].pct_change().fillna(0.0)
    spy_f = metrics(spy.loc[START:]); _h = len(spy.loc[START:]) // 2
    spy_h1 = metrics(spy.loc[START:].iloc[:_h]); spy_h2 = metrics(spy.loc[START:].iloc[_h:])
    spy_o = metrics(spy.loc[pd.Timestamp(IS_END) + pd.Timedelta(days=1):])
    SPYREF[pname] = dict(h1=spy_h1["Sharpe"], h2=spy_h2["Sharpe"], f_dd=spy_f["MaxDD"], f_cagr=spy_f["CAGR"],
                         o_sh=spy_o["Sharpe"], o_dd=spy_o["MaxDD"], o_cagr=spy_o["CAGR"])
    base = run(px, rules_v2_weights, trad, "W")
    LB = legs(net(base, 10), START)
    say(f"\n## PANEL {pname}  {START.date()} -> {px.index[-1].date()}  ({yrs:.2f} y), {len(trad)} tradable")
    say(f"   SPY FULL {spy_f['CAGR']:.2%} / {spy_f['Sharpe']:.4f} / {spy_f['MaxDD']:.2%}  halves "
        f"{spy_h1['Sharpe']:.4f} / {spy_h2['Sharpe']:.4f}  OOS {spy_o['CAGR']:.2%} / {spy_o['Sharpe']:.4f} / {spy_o['MaxDD']:.2%}")
    say(f"   RULES v2 baseline @10bps FULL {LB['CAGR']:.2%} / {LB['Sharpe']:.4f} / {LB['MaxDD']:.2%}  halves "
        f"{LB['H1']:.4f} / {LB['H2']:.4f}  OOS {LB['OOS_CAGR']:.2%} / {LB['OOS_Sharpe']:.4f} / {LB['OOS_MaxDD']:.2%}")

    def keep4a(d, c):
        L = legs(net(base, c), START)
        return bool(d["H1"] > L["H1"] and d["H2"] > L["H2"] and d["MaxDD"] >= L["MaxDD"])

    def keep4b(d, oos=False):
        if oos:
            return bool(d["H1"] > spy_h1["Sharpe"] and d["H2"] > spy_h2["Sharpe"] and d["OOS_Sharpe"] > spy_o["Sharpe"]
                        and d["OOS_MaxDD"] >= 0.6 * spy_o["MaxDD"] and d["OOS_CAGR"] >= 0.7 * spy_o["CAGR"])
        return bool(d["H1"] > spy_h1["Sharpe"] and d["H2"] > spy_h2["Sharpe"]
                    and d["MaxDD"] >= 0.6 * spy_f["MaxDD"] and d["CAGR"] >= 0.7 * spy_f["CAGR"])

    # ---- one static-exposure curve PER CADENCE (the twin must be matched at its own cadence)
    ew, cx_full, cx_is = {}, {}, {}
    for fq in CADENCES:
        ew[fq] = {a: run(px, lambda p, a=a: static_mix_weights(p, trad, a), trad, fq) for a in LADDER}
        cx_full[fq] = [float(ew[fq][a]["eq_exp"].loc[START:].mean()) for a in LADDER]
        cx_is[fq] = [float(ew[fq][a]["eq_exp"].loc[START:IS_END].mean()) for a in LADDER]
    mono = all(np.all(np.diff(cx_full[f]) > 0) and np.all(np.diff(cx_is[f]) > 0) for f in CADENCES)
    gate(f"G3 {pname} static exposure curves monotone at every cadence", mono, mono, "unique matched twin")

    merr = []
    for fq in CADENCES:
        for bw in WIDTHS:
            cand = run(px, lambda p, bw=bw: clause6_weights(p, trad, bw, GROSS), trad, fq)
            tf = float(cand["eq_exp"].loc[START:].mean())
            af = float(np.interp(tf, cx_full[fq], LADDER))
            twin = run(px, lambda p, a=af: static_mix_weights(p, trad, a), trad, fq)
            merr.append(abs(float(twin["eq_exp"].loc[START:].mean()) - tf))
            turn = float(cand["turnover"].loc[START:].sum() / yrs)
            tturn = float(twin["turnover"].loc[START:].sum() / yrs)
            cstar = breakeven_cost(cand, twin, START)
            if pname == "U56" and fq == "W" and bw == 0.03:
                u56_w_turn = turn
                rep = legs(net(cand, 0), START)
                say(f"   [G5b] this run's U56 W/0.03 cell (SPY NOT tradable): Sharpe {rep['Sharpe']:.6f}, "
                    f"turnover {turn:.6f}; 1670 committed 1.303484 / 2.838279 -> dev "
                    f"{abs(rep['Sharpe']-1.303484):.3e} / {abs(turn-2.838279):.3e}")
            for c in COSTS:
                dc = legs(net(cand, c), START); dt = legs(net(twin, c), START)
                grid.append(dict(panel=pname, cadence=fq, band=bw, cost_bps=c, arm="BAND",
                                 turnover_yr=turn, mean_eq_exposure=tf,
                                 **{k: float(v) for k, v in dc.items()},
                                 keep4a=keep4a(dc, c), keep4b_full=keep4b(dc), keep4b_oos=keep4b(dc, oos=True)))
                grid.append(dict(panel=pname, cadence=fq, band=bw, cost_bps=c, arm="TWIN",
                                 turnover_yr=tturn, mean_eq_exposure=float(twin["eq_exp"].loc[START:].mean()),
                                 **{k: float(v) for k, v in dt.items()},
                                 keep4a=keep4a(dt, c), keep4b_full=keep4b(dt), keep4b_oos=keep4b(dt, oos=True)))
                paired.append(dict(panel=pname, cadence=fq, band=bw, cost_bps=c, a_matched=af,
                                   cand_turnover=turn, twin_turnover=tturn, dturnover=turn - tturn,
                                   cand_Sharpe=dc["Sharpe"], twin_Sharpe=dt["Sharpe"],
                                   dSharpe=dc["Sharpe"] - dt["Sharpe"],
                                   dSharpe_H1=dc["H1"] - dt["H1"], dSharpe_H2=dc["H2"] - dt["H2"],
                                   dSharpe_OOS=dc["OOS_Sharpe"] - dt["OOS_Sharpe"],
                                   dCAGR_pp=(dc["CAGR"] - dt["CAGR"]) * 100,
                                   dMaxDD_pp=(dc["MaxDD"] - dt["MaxDD"]) * 100,
                                   dCAGR_OOS_pp=(dc["OOS_CAGR"] - dt["OOS_CAGR"]) * 100,
                                   dMaxDD_OOS_pp=(dc["OOS_MaxDD"] - dt["OOS_MaxDD"]) * 100,
                                   cstar_bps=cstar))
            say(f"   {fq}/band {bw:.2f}: turnover {turn:5.2f}x/yr (twin {tturn:4.2f}), a*={af:.4f}, "
                f"dSharpe @0/10/25/50 bps "
                + " / ".join(f"{paired[-4+i]['dSharpe']:+.4f}" for i in range(4))
                + f", c*={cstar:.1f} bps")

    gate(f"G4 {pname} matched-twin exposure tolerance", f"{max(merr):.3e}", max(merr) < 5e-3,
         "candidate mean equity exposure vs its matched static twin, FULL window")

    # ---- rule 8: choose (cadence, width) on IS rows only, read 2017-2026 ONCE
    cells = [(f, b) for f in CADENCES for b in WIDTHS]
    P = pd.DataFrame(paired)
    P = P[P.panel == pname]
    G = pd.DataFrame(grid); G = G[(G.panel == pname) & (G.arm == "BAND")]
    for c in COSTS:
        gc = G[G.cost_bps == c].set_index(["cadence", "band"])
        pc = P[P.cost_bps == c].set_index(["cadence", "band"])
        picks = {
            "C_IS_SHARPE": gc["IS_Sharpe"].idxmax(),
            "C_IS_DSHARPE_IS": None,      # filled below (needs IS-window dSharpe)
            "C_DONOTHING": ("W", 0.03),
        }
        # IS-window dSharpe chooser: candidate IS Sharpe minus twin IS Sharpe, IS rows only
        tw = pd.DataFrame(grid); tw = tw[(tw.panel == pname) & (tw.arm == "TWIN") & (tw.cost_bps == c)]
        tw = tw.set_index(["cadence", "band"])["IS_Sharpe"]
        picks["C_IS_DSHARPE_IS"] = (gc["IS_Sharpe"] - tw).idxmax()
        for nm, key in picks.items():
            r = gc.loc[key]
            wf.append(dict(panel=pname, cost_bps=c, chooser=nm, pick_cadence=key[0], pick_band=key[1],
                           IS_Sharpe=float(r["IS_Sharpe"]),
                           OOS_CAGR=float(r["OOS_CAGR"]), OOS_Sharpe=float(r["OOS_Sharpe"]),
                           OOS_MaxDD=float(r["OOS_MaxDD"]),
                           FULL_CAGR=float(r["CAGR"]), FULL_Sharpe=float(r["Sharpe"]), FULL_MaxDD=float(r["MaxDD"]),
                           H1=float(r["H1"]), H2=float(r["H2"]),
                           dSharpe_OOS_vs_twin=float(pc.loc[key, "dSharpe_OOS"]),
                           keep4a=bool(r["keep4a"]), keep4b_full=bool(r["keep4b_full"]),
                           keep4b_oos=bool(r["keep4b_oos"]),
                           base_OOS_Sharpe=LB["OOS_Sharpe"], base_OOS_CAGR=LB["OOS_CAGR"], base_OOS_MaxDD=LB["OOS_MaxDD"],
                           spy_OOS_Sharpe=spy_o["Sharpe"], spy_OOS_CAGR=spy_o["CAGR"], spy_OOS_MaxDD=spy_o["MaxDD"]))

GRID = pd.DataFrame(grid); PAIR = pd.DataFrame(paired); WF = pd.DataFrame(wf)
GRID.to_csv(f"{OUT}.grid.csv", index=False); PAIR.to_csv(f"{OUT}.paired.csv", index=False)
WF.to_csv(f"{OUT}.walkforward.csv", index=False)

# ---------------------------------------------------------------- G6: cost algebra is exact
px, trad = PANELS["U56"]
chk = clause6_weights(px, trad, 0.03, GROSS)
r0 = backtest(px, chk, cost_bps=0.0, freq="W"); r25 = backtest(px, chk, cost_bps=25.0, freq="W")
dev = float((r0["returns"] - r0["turnover"] * 25 / 1e4 - r25["returns"]).abs().max())
gate("G6 cost axis exact off the c=0 run", f"{dev:.3e}", dev < 1e-12,
     "r_net(c) = r_gross - turnover*c/1e4 vs engine.backtest(cost_bps=25)")

# ---------------------------------------------------------------- the pre-registered reading
say("\n# ================ THE BUDGET TEST ================")
say(f"U56 weekly band-0.03 candidate turnover = {u56_w_turn:.4f}x/yr (1670's 2.84x)")
T = PAIR[(PAIR.cost_bps == 10) & (PAIR.band == 0.03)]
budget_rows = []
for pn in ["B136", "SMALL"]:
    sub = T[T.panel == pn].set_index("cadence")
    slow = sub[sub.cand_turnover <= u56_w_turn]
    if len(slow):
        fq = slow.cand_turnover.idxmax()            # the FASTEST cadence at/below U56-weekly's turnover
        row = sub.loc[fq]
        budget_rows.append(dict(panel=pn, cadence=fq, turnover=float(row.cand_turnover),
                                dSharpe_10bps=float(row.dSharpe), recovered=bool(row.dSharpe > 0)))
        say(f"   {pn}: first cadence at/below {u56_w_turn:.2f}x is {fq} "
            f"(turnover {row.cand_turnover:.2f}x/yr) -> net dSharpe @10bps {row.dSharpe:+.4f} "
            f"{'POSITIVE (budget-true)' if row.dSharpe > 0 else 'NEGATIVE (budget-false)'}")
    else:
        budget_rows.append(dict(panel=pn, cadence="none", turnover=float("nan"),
                                dSharpe_10bps=float("nan"), recovered=False))
        say(f"   {pn}: NO cadence reaches U56-weekly's turnover")
B = pd.DataFrame(budget_rows)
gate("G7 budget prediction (B136 and SMALL recover a positive net dSharpe at matched turnover)",
     "; ".join(f"{r.panel} {r.cadence} {r.dSharpe_10bps:+.4f}" for r in B.itertuples()),
     bool(B.recovered.all()), "PRE-REGISTERED: pass = BUDGET-TRUE, fail = BUDGET-FALSE")

say("\n# GROSS (0 bps) credit by cadence — does slowing keep the timing value it is meant to keep?")
G0 = PAIR[(PAIR.cost_bps == 0) & (PAIR.band == 0.03)].pivot(index="panel", columns="cadence", values="dSharpe")
say(G0[CADENCES].to_string(float_format=lambda x: f"{x:+.4f}"))
TT = PAIR[(PAIR.cost_bps == 0) & (PAIR.band == 0.03)].pivot(index="panel", columns="cadence", values="cand_turnover")
say("\n# candidate turnover (x/yr) by cadence")
say(TT[CADENCES].to_string(float_format=lambda x: f"{x:.2f}"))
say("\n# NET dSharpe at 10 bps by cadence (band 0.03)")
N10 = PAIR[(PAIR.cost_bps == 10) & (PAIR.band == 0.03)].pivot(index="panel", columns="cadence", values="dSharpe")
say(N10[CADENCES].to_string(float_format=lambda x: f"{x:+.4f}"))
say("\n# break-even cost c* (bps) by cadence x band width")
CS = (PAIR[PAIR.cost_bps == 0].pivot_table(index=["panel", "band"], columns="cadence", values="cstar_bps",
                                           dropna=False).reindex(columns=CADENCES))
say(CS[CADENCES].to_string(float_format=lambda x: f"{x:.1f}"))

mono_t = all(PAIR[(PAIR.panel == p) & (PAIR.band == b) & (PAIR.cost_bps == 0)]
             .set_index("cadence").loc[CADENCES, "cand_turnover"].is_monotonic_decreasing
             for p in PANELS for b in WIDTHS)
gate("G8 turnover falls monotonically as the cadence slows", mono_t, mono_t, "D >= W >= M >= Q at every (panel, width)")

# ---------------------------------------------------------------- KEEP paths
say("\n# ================ KEEP PATHS (every cell published in .grid.csv) ================")
BD = GRID[GRID.arm == "BAND"]
say(f"4a: {int(BD.keep4a.sum())} of {len(BD)} band cells;  "
    f"4b FULL {int(BD.keep4b_full.sum())}, 4b OOS {int(BD.keep4b_oos.sum())}, "
    f"BOTH {int((BD.keep4b_full & BD.keep4b_oos).sum())}")
TWN = GRID[GRID.arm == "TWIN"]
say(f"TWIN arms: 4a {int(TWN.keep4a.sum())} of {len(TWN)};  4b FULL {int(TWN.keep4b_full.sum())}, "
    f"4b OOS {int(TWN.keep4b_oos.sum())}, BOTH {int((TWN.keep4b_full & TWN.keep4b_oos).sum())}")
for pn in PANELS:
    s = BD[BD.panel == pn]
    say(f"   {pn}: 4a {int(s.keep4a.sum())}/{len(s)}, 4b FULL {int(s.keep4b_full.sum())}, "
        f"OOS {int(s.keep4b_oos.sum())}, BOTH {int((s.keep4b_full & s.keep4b_oos).sum())}")
both = BD[BD.keep4b_full & BD.keep4b_oos]
if len(both):
    say("\n# cells clearing 4b FULL *and* OOS:")
    say(both[["panel", "cadence", "band", "cost_bps", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
              "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "turnover_yr"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

# ---- which 4b leg binds on the band cells, and the sign census of the credit
def binds(r, oos):
    out = []
    sp = SPYREF[r["panel"]]
    if oos:
        if not r["H1"] > sp["h1"]: out.append("H1")
        if not r["H2"] > sp["h2"]: out.append("H2")
        if not r["OOS_Sharpe"] > sp["o_sh"]: out.append("OOS_Sharpe")
        if not r["OOS_MaxDD"] >= 0.6 * sp["o_dd"]: out.append("OOS_DD")
        if not r["OOS_CAGR"] >= 0.7 * sp["o_cagr"]: out.append("OOS_CAGR")
    else:
        if not r["H1"] > sp["h1"]: out.append("H1")
        if not r["H2"] > sp["h2"]: out.append("H2")
        if not r["MaxDD"] >= 0.6 * sp["f_dd"]: out.append("DD")
        if not r["CAGR"] >= 0.7 * sp["f_cagr"]: out.append("CAGR")
    return out

from collections import Counter
cf, co = Counter(), Counter()
for _, r in BD.iterrows():
    cf.update(binds(r, False)); co.update(binds(r, True))
say(f"\n# 4b FULL binding legs over {len(BD)} band cells: " + ", ".join(f"{k} {v}" for k, v in cf.most_common()))
say(f"# 4b OOS  binding legs over {len(BD)} band cells: " + ", ".join(f"{k} {v}" for k, v in co.most_common()))
cft, cot = Counter(), Counter()
for _, r in TWN.iterrows():
    cft.update(binds(r, False)); cot.update(binds(r, True))
say(f"# for contrast, the matched TWIN arms: FULL " + ", ".join(f"{k} {v}" for k, v in cft.most_common())
    + " | OOS " + ", ".join(f"{k} {v}" for k, v in cot.most_common()))

P10 = PAIR[PAIR.cost_bps == 10]
say(f"\n# sign census of the NET credit at 10 bps over all {len(P10)} (panel, cadence, width) cells: "
    f"{int((P10.dSharpe > 0).sum())} POSITIVE, {int((P10.dSharpe <= 0).sum())} NEGATIVE")
for pn in PANELS:
    sub = P10[P10.panel == pn]
    say(f"   {pn}: {int((sub.dSharpe > 0).sum())} of {len(sub)} positive; "
        f"best {sub.dSharpe.max():+.4f} at {sub.loc[sub.dSharpe.idxmax(),'cadence']}/"
        f"{sub.loc[sub.dSharpe.idxmax(),'band']:.2f} (turnover {sub.loc[sub.dSharpe.idxmax(),'cand_turnover']:.2f}x)")

# ---- the budget test re-run on BOTH dials: match turnover with cadence AND width
say("\n# BUDGET TEST, SECOND READING: match U56-weekly's turnover using BOTH dials")
for pn in ("B136", "SMALL"):
    sub = P10[P10.panel == pn].copy()
    sub["gap"] = (sub.cand_turnover - u56_w_turn).abs()
    r = sub.loc[sub.gap.idxmin()]
    say(f"   {pn}: closest cell to {u56_w_turn:.2f}x/yr is {r.cadence}/{r.band:.2f} "
        f"(turnover {r.cand_turnover:.2f}x) -> net dSharpe @10bps {r.dSharpe:+.4f}")
    lo = sub[sub.cand_turnover <= u56_w_turn]
    say(f"      of the {len(lo)} cells at or below U56-weekly turnover, "
        f"{int((lo.dSharpe > 0).sum())} carry a POSITIVE net credit")

say("\n# ================ RULE 8 WALK-FORWARD (IS <= 2016-12-31, OOS read once) ================")
say(WF[["panel", "cost_bps", "chooser", "pick_cadence", "pick_band", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
        "dSharpe_OOS_vs_twin", "keep4b_oos", "base_OOS_Sharpe", "spy_OOS_Sharpe"]]
    .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
for pn in PANELS:
    w = WF[(WF.panel == pn) & (WF.cost_bps == 10)].set_index("chooser")
    dn = w.loc["C_DONOTHING", "OOS_Sharpe"]
    for nm in ("C_IS_SHARPE", "C_IS_DSHARPE_IS"):
        say(f"   {pn} @10bps  {nm} picks {w.loc[nm,'pick_cadence']}/{w.loc[nm,'pick_band']:.2f}  "
            f"OOS Sharpe {w.loc[nm,'OOS_Sharpe']:.4f} vs do-nothing (W/0.03) {dn:.4f}  "
            f"-> {w.loc[nm,'OOS_Sharpe']-dn:+.4f}")
chooser_gain = []
for pn in PANELS:
    for c in COSTS:
        w = WF[(WF.panel == pn) & (WF.cost_bps == c)].set_index("chooser")
        for nm in ("C_IS_SHARPE", "C_IS_DSHARPE_IS"):
            chooser_gain.append(w.loc[nm, "OOS_Sharpe"] - w.loc["C_DONOTHING", "OOS_Sharpe"])
gate("G9 does any IS-only chooser beat doing nothing (mean OOS Sharpe delta)",
     f"{np.mean(chooser_gain):+.4f} over {len(chooser_gain)} chooser-cells, "
     f"{sum(1 for x in chooser_gain if x > 0)} positive",
     np.mean(chooser_gain) > 0, "reported either way; not a stopping condition")

pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
say(f"\ngates: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass")
Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
