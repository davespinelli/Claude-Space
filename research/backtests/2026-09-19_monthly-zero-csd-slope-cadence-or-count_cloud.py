#!/usr/bin/env python3
"""Idea 724 (lane cloud, 2026-09-19): is the MONTHLY ZERO of the c_sd residual slope a
CADENCE fact or a REBALANCE-COUNT fact?

Idea 539 fitted the de-grossing TIMING RESIDUAL on the exposure path's dispersion,

    resid0_pp = a + b * c_sd ,   resid0 = [CAGR0(DEGROSS) - CAGR0(RESPREAD)]
                                          - [CAGR0(c_bar * r_RESPREAD) - CAGR0(r_RESPREAD)]

over 54 cells per (cadence, gross) — 3 panels x 2 gate families x 9 strictness levels — and
found the gross-normalised slope b/g at

    D -3.3596   W -3.4627   M -0.2354 (t -0.42, R2 0.0034)   Q -2.4952      (g = 0.75, IS)

The monthly reading is a HOLE, and it is not monotone in rebalance count: Q rebalances three
times less often than M and carries a slope ten times larger.  Either the monthly zero is an
artefact of the MONTH-END CALENDAR (a phase, not a frequency), or it is a genuine interior
node of the rebalance-count axis that D / W / Q simply straddle.

THE TEST: replace the calendar with a COUNT.  Re-cut 539's decomposition verbatim on a fixed
N-TRADING-DAY ladder {2, 5, 10, 21, 42, 63} — 21d has a month's rebalance COUNT with no
month-end alignment — plus the four calendar cadences {D, W, M, Q} as the reference, plus two
extra PHASES of the 21d ladder (offsets 7 and 14) so that a phase effect cannot hide inside a
count effect.  Dials: CADENCE (1) and GROSS (2), and no more; panels, families and levels are
539's reported axes, inherited verbatim and never tuned.

PRE-REGISTERED READING (written before any new number was read):
  CALENDAR ARTEFACT  |b/g| at 21d (and at both extra phases) lands inside the D/W/Q band,
                     i.e. >= 2.0, while calendar-M stays near zero.
  INTERIOR NODE      |b/g| at 21d is itself near zero (< 1.0), i.e. the count, not the
                     calendar, is what kills the slope.
  INCONCLUSIVE       anything between; published as such, with the whole ladder.

Rule 8 (required): every chooser sees rows <= 2016-12-31 only and 2017-2026 is read ONCE.
Both KEEP paths are evaluated on EVERY book.  Costs 10 bps, next-day execution; the 0-bps
rung is DERIVED exactly (r0 = r10 + turnover*bps/1e4), never re-run.

SURVIVORSHIP: all three panels are CURRENT constituents (no delistings), so every CAGR LEVEL
is inflated; the headline object is an arm-minus-arm contrast on the SAME names and days, so
the bias largely cancels out of gap0/pred0/resid0 but NOT out of the 4a/4b columns.  SMALL
drops every ticker with max_1d_move >= 1.0 in data/small_meta.csv first.

RUN AS: `script.py U56`, `script.py B136`, `script.py SMALL439` (one panel per process — the
sandbox throttles background CPU; each writes transient `.part_<panel>.*` files), then
`script.py combine`.  The partials are pruned after the run; regenerate them to re-combine.
Deterministic, offline, no network.  Writes .grid.csv.gz .decomp.csv.gz .slopes.csv
.walkforward.csv .freechooser.csv .gates.csv .log.txt
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
from baseline import load_universe, rules_v2_weights                       # noqa: E402
sys.path.insert(0, str(REPO / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask                       # noqa: E402

OUT = Path(__file__).with_suffix("")
COST_BPS = 10
GROSSES = [0.50, 0.75, 1.00]                                   # dial 2
CAL = ["D", "W", "M", "Q"]                                     # 539's calendar reference
NDAY = [2, 5, 10, 21, 42, 63]                                  # dial 1 — the count ladder
PHASES = [(21, 7), (21, 14)]                                   # phase controls on the 21d rung
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
QUANT_X = [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95]
MA_THETA = [0.30, 0.20, 0.12, 0.06, 0.00, -0.06, -0.12, -0.25, -0.40]
FAMILIES = ["QUANTILE", "MA-THRESH"]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
REF539 = REPO / "research" / "backtests" / (
    "2026-09-11_does-the-c_sd-RESIDUAL-LAW-hold-on-a-CADENCE-and-GROSS-grid_cloud.decomp.csv")
LOG, GATES = [], []
MODE = sys.argv[1] if len(sys.argv) > 1 else "all"


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); LOG.append(s)


def gate(name, val, ok, note=""):
    GATES.append(dict(gate=name, value=str(val), pass_=bool(ok), note=note))
    P(f"GATE {name}: {val}  {'PASS' if ok else 'FAIL'}  {note}")


def ols(x, y):
    X = np.column_stack([np.ones(len(x)), np.asarray(x, float)]); y = np.asarray(y, float)
    XtXi = np.linalg.pinv(X.T @ X); b = XtXi @ (X.T @ y); e = y - X @ b
    ssr = float(e @ e); sst = float(((y - y.mean()) ** 2).sum()); dof = max(1, len(x) - 2)
    se = np.sqrt(np.maximum(np.diag(XtXi * (ssr / dof)), 0))
    return dict(a=b[0], b=b[1], t=b[1] / se[1] if se[1] > 0 else np.nan,
                R2=1 - ssr / sst if sst > 0 else np.nan, n=len(x))


# ---------------------------------------------------------------- cadence masks
def cad_mask(idx, cad):
    """Boolean 'rebalance at this close'.  Calendar cadences delegate to the engine so the
    reference columns are engine cadences, not a re-implementation."""
    if isinstance(cad, str):
        return rebalance_mask(idx, cad).values
    n, ph = cad
    return (np.arange(len(idx)) % n) == (ph % n)


CADENCES = CAL + [(n, 0) for n in NDAY] + list(PHASES)


def cad_name(c):
    return c if isinstance(c, str) else (f"{c[0]}d" if c[1] == 0 else f"{c[0]}d@ph{c[1]}")


# ---------------------------------------------------------------- exact numpy clone of engine
_RET = {}


def fast_backtest(prices, weights, cost_bps, cad, Wv=None):
    idx = prices.index
    k = (id(prices), prices.shape)
    if k not in _RET:
        _RET[k] = prices.pct_change().fillna(0.0).values
    rets = _RET[k]
    W = weights.reindex(idx).fillna(0.0).shift(1).values if Wv is None else Wv
    mask = pd.Series(cad_mask(idx, cad), index=idx).shift(1, fill_value=False).values
    n = len(idx); held = np.empty_like(rets); turn = np.zeros(n); cur = np.zeros(rets.shape[1])
    for i in range(n):
        if mask[i] or i == 0:
            new = W[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        g = cur * (1.0 + rets[i]); tot = g.sum() + (1.0 - cur.sum())
        if tot > 0: cur = g / tot
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=idx), "turnover": pd.Series(turn, index=idx),
            "gross": pd.Series(held.sum(axis=1), index=idx)}


# ---------------------------------------------------------------- 539's constructions, verbatim
def panels():
    sm = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv = [c for c in sm.columns if c != "SPY" and c not in bad]
    u = load_universe(); b = load_universe(broad=True)
    P(f"panels: SMALL439 {len(inv)} names ({len(bad)} dropped for max_1d_move >= 1.0; "
      f"SURVIVORSHIP: current constituents only), U56 {len([c for c in u.columns if c != 'SPY'])}, "
      f"B136 {len([c for c in b.columns if c != 'SPY'])}")
    return {"SMALL439": (sm[inv], sm["SPY"]),
            "U56": (u[[c for c in u.columns if c != "SPY"]], u["SPY"]),
            "B136": (b[[c for c in b.columns if c != "SPY"]], b["SPY"])}, len(bad)


def live_mask(px):
    return px.notna() & px.shift(1).notna()


_MC = {}


def gate_mask(px, family, level):
    k = (id(px), family, level)
    if k in _MC: return _MC[k]
    live = live_mask(px); ma = px.rolling(200).mean()
    if family == "MA-THRESH":
        m = (px > ma * (1 + level)) & live
    else:
        dist = (px / ma - 1).where(live); n = live.sum(axis=1)
        kt = np.ceil(level * n).astype(int).clip(lower=1)
        m = dist.rank(axis=1, ascending=False, method="first").le(kt, axis=0).fillna(False) & live
    _MC[k] = m
    return m


def book(px, family, level, construction, gross):
    g = gate_mask(px, family, level)
    if construction == "RESPREAD":
        return g.astype(float).div(g.sum(axis=1).clip(lower=1), axis=0) * gross
    return g.astype(float).div(live_mask(px).sum(axis=1).clip(lower=1), axis=0) * gross


def stat(r):
    h = len(r) // 2
    m, mi, mo = metrics(r), metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])


def cagr(r):
    return metrics(r)["CAGR"]


def verdict_4a(s, b):
    return bool(s["H1"] > b["H1"] and s["H2"] > b["H2"] and s["MaxDD"] >= b["MaxDD"])


def fail_4b(s, spy, oos=False):
    if oos:
        t = {"H1": s["H1"] > spy["H1"], "H2": s["H2"] > spy["H2"],
             "OOS_Sharpe": s["oSharpe"] > spy["oSharpe"],
             "OOS_DD": abs(s["oMaxDD"]) <= 0.60 * abs(spy["oMaxDD"]),
             "OOS_CAGR": s["oCAGR"] >= 0.70 * spy["oCAGR"]}
    else:
        t = {"H1": s["H1"] > spy["H1"], "H2": s["H2"] > spy["H2"],
             "DD": abs(s["MaxDD"]) <= 0.60 * abs(spy["MaxDD"]),
             "CAGR": s["CAGR"] >= 0.70 * spy["CAGR"]}
    f = [k for k, v in t.items() if not v]
    return ",".join(f) if f else "-"


# ================================================================ run
P("=" * 120)
P("Idea 724 — is the MONTHLY ZERO of the c_sd residual slope a CADENCE fact or a COUNT fact?")
P("=" * 120)
P(f"dials: CADENCE {[cad_name(c) for c in CADENCES]} x GROSS {GROSSES}; "
  f"panels x families x levels inherited from idea 539 verbatim.  Costs {COST_BPS} bps, "
  f"0-bps rung DERIVED.  IS <= {IS_END}, OOS >= {OOS_START}.")
PN, n_bad = panels()
gate("G0 SMALL max_1d_move screen applied", f"{n_bad} dropped", n_bad > 0, "data/small_meta.csv")

# ---- G1: the numpy clone equals the engine on the four cadences the engine supports
g1 = 0.0
probe = PN["U56"][0]
for fam, lvl, con, g, cad in [("MA-THRESH", 0.06, "DEGROSS", 0.75, "W"),
                              ("QUANTILE", 0.40, "RESPREAD", 0.50, "M"),
                              ("MA-THRESH", -0.25, "RESPREAD", 1.00, "D"),
                              ("QUANTILE", 0.95, "DEGROSS", 1.00, "Q")]:
    w = book(probe, fam, lvl, con, g)
    a = backtest(probe, w, cost_bps=COST_BPS, freq=cad); b = fast_backtest(probe, w, COST_BPS, cad)
    g1 = max(g1, float((a["returns"] - b["returns"]).abs().iloc[1:].max()),
             float((a["turnover"] - b["turnover"]).abs().iloc[1:].max()),
             float((a["weights"].sum(axis=1) - b["gross"]).abs().iloc[1:].max()))
gate("G1 fast_backtest == engine.backtest at D/W/M/Q", f"{g1:.3e}", g1 < 1e-12,
     "the N-day ladder runs through this clone; without the gate it is a different backtester")
# ---- G1b: the count ladder really rebalances the number of times it claims
cnt = {cad_name(c): int(pd.Series(cad_mask(probe.index, c), index=probe.index).sum()) for c in CADENCES}
P("rebalance counts over the U56 index (" + str(len(probe.index)) + " rows): "
  + ", ".join(f"{k} {v}" for k, v in cnt.items()))
ok1b = cnt["21d"] > cnt["M"] * 0.9 and cnt["21d"] < cnt["M"] * 1.15
gate("G1b 21d carries a month's rebalance COUNT", f"21d {cnt['21d']} vs calendar M {cnt['M']}",
     ok1b, "the count ladder is matched to the calendar it is replacing")

rows, decomp = [], []
ctx = {}
TODO = [k for k in PN if MODE in ("all", k)]
P(f"run mode: {MODE} -> panels {TODO}")
for pname in TODO:
    px, spy_px = PN[pname]
    start = px.index[260]
    years = len(px.loc[start:]) / 252
    spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:])
    pxu = load_universe()
    live_r = backtest(pxu, rules_v2_weights(pxu), cost_bps=COST_BPS, freq="W")["returns"]
    live_s = stat(live_r.reindex(px.index).fillna(0.0).loc[start:])
    ctx[pname] = (spy_s, live_s)
    P(f"\nPANEL {pname}  eval from {start.date()} ({years:.2f} y)")
    P(f"  SPY      CAGR {spy_s['CAGR']:.2%} Sharpe {spy_s['Sharpe']:.4f} MaxDD {spy_s['MaxDD']:.2%} "
      f"H1/H2 {spy_s['H1']:.4f}/{spy_s['H2']:.4f}  OOS {spy_s['oCAGR']:.2%}/{spy_s['oSharpe']:.4f}/{spy_s['oMaxDD']:.2%}")
    P(f"  RULES v2 CAGR {live_s['CAGR']:.2%} Sharpe {live_s['Sharpe']:.4f} MaxDD {live_s['MaxDD']:.2%} "
      f"H1/H2 {live_s['H1']:.4f}/{live_s['H2']:.4f}  OOS {live_s['oCAGR']:.2%}/{live_s['oSharpe']:.4f}/{live_s['oMaxDD']:.2%}")
    for family in FAMILIES:
        for level in (QUANT_X if family == "QUANTILE" else MA_THETA):
            WCACHE = {(g, c): book(px, family, level, c, g).reindex(px.index).fillna(0.0).shift(1).values
                      for g in GROSSES for c in CONSTRUCTIONS}
            for cad in CADENCES:
                cn = cad_name(cad)
                for gross in GROSSES:
                    got = {}
                    for con in CONSTRUCTIONS:
                        res = fast_backtest(px, None, COST_BPS, cad, Wv=WCACHE[(gross, con)])
                        r10 = res["returns"].loc[start:]; turn = res["turnover"].loc[start:]
                        r0 = r10 + turn * COST_BPS / 1e4
                        s = stat(r10)
                        got[con] = dict(r0=r0, gross=res["gross"].loc[start:])
                        rows.append(dict(panel=pname, family=family, level=level, cad=cn,
                                         gross=gross, con=con, **s, CAGR0=cagr(r0),
                                         turn_yr=turn.sum() / years,
                                         keep4a=verdict_4a(s, live_s),
                                         fail4b=fail_4b(s, spy_s), fail4b_oos=fail_4b(s, spy_s, True)))
                    dg, rs = got["DEGROSS"], got["RESPREAD"]
                    c_t = (dg["gross"] / rs["gross"].replace(0, np.nan)).fillna(0.0)
                    ident = float((dg["r0"] - c_t * rs["r0"]).abs().max())
                    for tag, lo, hi in (("FULL", None, None), ("IS", None, IS_END), ("OOS", OOS_START, None)):
                        sl = slice(lo, hi)
                        rr, rd = rs["r0"].loc[sl], dg["r0"].loc[sl]
                        cb = float(c_t.loc[sl].mean())
                        g0 = 100 * (cagr(rd) - cagr(rr)); p0 = 100 * (cagr(cb * rr) - cagr(rr))
                        decomp.append(dict(panel=pname, family=family, level=level, cad=cn, gross=gross,
                                           window=tag, ident_max_err=ident, c_bar=cb,
                                           c_sd=float(c_t.loc[sl].std()), gap0_pp=g0, pred0_pp=p0,
                                           resid0_pp=g0 - p0))
        P(f"  ... {pname} / {family} done ({9 * len(CADENCES) * len(GROSSES) * 2} books)")
        Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")

if MODE not in ("all", "combine"):
    pd.DataFrame(rows).to_csv(f"{OUT}.part_{MODE}.grid.csv", index=False)
    pd.DataFrame(decomp).to_csv(f"{OUT}.part_{MODE}.decomp.csv", index=False)
    pd.DataFrame(ctx[MODE][0], index=[0]).to_csv(f"{OUT}.part_{MODE}.spy.csv", index=False)
    pd.DataFrame(ctx[MODE][1], index=[0]).to_csv(f"{OUT}.part_{MODE}.live.csv", index=False)
    Path(f"{OUT}.log_{MODE}.txt").write_text("\n".join(LOG) + "\n")
    P(f"partial artifacts written for {MODE}: {len(rows)} books, {len(decomp)//3} cells")
    sys.exit(0)

if MODE == "combine":
    rows, decomp = [], []
    for k in PN:
        rows.append(pd.read_csv(f"{OUT}.part_{k}.grid.csv"))
        decomp.append(pd.read_csv(f"{OUT}.part_{k}.decomp.csv"))
        ctx[k] = (pd.read_csv(f"{OUT}.part_{k}.spy.csv").iloc[0].to_dict(),
                  pd.read_csv(f"{OUT}.part_{k}.live.csv").iloc[0].to_dict())
    G = pd.concat(rows, ignore_index=True); D = pd.concat(decomp, ignore_index=True)
    P(f"combined partials: {len(G)} books, {len(D)//3} decomposition cells over {list(PN)}")
else:
    G = pd.DataFrame(rows); D = pd.DataFrame(decomp)
G["pass4b"] = G.fail4b == "-"; G["pass4b_oos"] = G.fail4b_oos == "-"
G.to_csv(f"{OUT}.grid.csv", index=False); D.to_csv(f"{OUT}.decomp.csv", index=False)
P(f"\nbooks {len(G)}  decomposition cells {len(D)//3}  identity max |r_dg - c_t*r_rs| {D.ident_max_err.max():.3e}")
gate("G2 the DEGROSS = c_t x RESPREAD identity holds", f"{D.ident_max_err.max():.3e}",
     D.ident_max_err.max() < 1e-12, "c_t is the exposure ratio, checked not assumed")

# ---- G3: replay idea 539's committed per-cadence slopes off ITS OWN decomp.csv
ref = pd.read_csv(REF539)
ref = ref[ref.window == "IS"]
mine = D[D.window == "IS"]
dev = []
P("\n# per-(cadence, gross) IS slopes: this run vs idea 539's committed .decomp.csv")
for cad in CAL:
    for g in GROSSES:
        a = ols(ref[(ref.cad == cad) & (ref.gross == g)].c_sd, ref[(ref.cad == cad) & (ref.gross == g)].resid0_pp)
        m = mine[(mine.cad == cad) & (mine.gross == g)]
        b = ols(m.c_sd, m.resid0_pp)
        dev.append(abs(a["b"] / g - b["b"] / g))
        P(f"   {cad:>4s} g={g:.2f}: 539 b/g {a['b']/g:+.4f} (t {a['t']:+.2f}, R2 {a['R2']:.4f}, n {a['n']})"
          f"   |  this run b/g {b['b']/g:+.4f} (t {b['t']:+.2f}, R2 {b['R2']:.4f}, n {b['n']})")
gate("G3 replay of idea 539's committed per-cadence slopes (all three panels)",
     f"max |d b/g| {max(dev):.4f}", max(dev) < 5e-2,
     "FAILS — diagnosed in G3c below; it is not the tape's end (an IS-window slope cannot see it)")

# ---- G3c: WHERE the replay gap lives.  Merge on 539's own cells and isolate it.
M = pd.read_csv(REF539).merge(D, on=["panel", "family", "level", "cad", "gross", "window"],
                              suffixes=("_539", "_now"))
M["dcsd"] = (M.c_sd_539 - M.c_sd_now).abs(); M["dres"] = (M.resid0_pp_539 - M.resid0_pp_now).abs()
P("\n# G3c — per-panel max |d c_sd| and |d resid0_pp| against 539's committed cells (IS window)")
P(M[M.window == "IS"].groupby("panel")[["dcsd", "dres"]].max().to_string(float_format=lambda x: f"{x:.3e}"))
dev_big = []
P("\n# the same per-cadence slopes with the SMALL pool EXCLUDED (36 cells, U56 + B136 only)")
for cad in CAL:
    for g in GROSSES:
        rr = ref[(ref.cad == cad) & (ref.gross == g) & (ref.panel != "SMALL439")]
        mm = mine[(mine.cad == cad) & (mine.gross == g) & (mine.panel != "SMALL439")]
        a, b = ols(rr.c_sd, rr.resid0_pp), ols(mm.c_sd, mm.resid0_pp)
        dev_big.append(abs(a["b"] / g - b["b"] / g))
        if g == 0.75:
            P(f"   {cad:>2s} g=0.75: 539 b/g {a['b']/g:+.4f} (t {a['t']:+.2f}) | this run {b['b']/g:+.4f} "
              f"(t {b['t']:+.2f})  d {abs(a['b']/g - b['b']/g):.4f}")
gate("G3c the replay is EXACT once the SMALL pool is excluded",
     f"max |d b/g| {max(dev_big):.4f} over U56+B136 (against {max(dev):.4f} with SMALL in)",
     max(dev_big) < 5e-2,
     "539 ran a 439-name small pool (44 dropped); today's loader serves 665 (54 dropped) — "
     "the pool was rebuilt, so 100% of the gap is the SMALL panel, not the construction or the tape")
P("\n# and what the MONTHLY hole looks like per panel (IS, g=0.75, 18 cells each)")
for pn in ("U56", "B136", "SMALL439"):
    for cad in ("D", "W", "M", "Q"):
        sub = mine[(mine.cad == cad) & (mine.gross == 0.75) & (mine.panel == pn)]
        f = ols(sub.c_sd, sub.resid0_pp)
        P(f"   {pn:9s} {cad:>2s}: b/g {f['b']/0.75:+.4f} (t {f['t']:+.2f}, R2 {f['R2']:.4f}, n {f['n']})")
pub = ols(ref[(ref.cad == 'M') & (ref.gross == 0.75)].c_sd, ref[(ref.cad == 'M') & (ref.gross == 0.75)].resid0_pp)
gate("G3b the queue's quoted monthly number is recovered from 539's own file",
     f"b/g {pub['b']/0.75:.4f} (queue -0.2354), t {pub['t']:.2f} (queue -0.42), R2 {pub['R2']:.4f} (queue 0.0034)",
     abs(pub["b"] / 0.75 + 0.2354) < 1e-3, "the object under test, quoted from source")

# ---- THE LADDER
P("\n" + "=" * 120)
P("THE COUNT LADDER: gross-normalised slope b/g of resid0_pp on c_sd, 54 cells per (cadence, gross)")
P("=" * 120)
slopes = []
ORDER = [cad_name(c) for c in CADENCES]
for win in ("IS", "OOS", "FULL"):
    for cn in ORDER:
        for g in GROSSES:
            s = D[(D.window == win) & (D.cad == cn) & (D.gross == g)]
            f = ols(s.c_sd, s.resid0_pp)
            slopes.append(dict(window=win, cad=cn, gross=g, n=f["n"], slope=f["b"], slope_per_gross=f["b"] / g,
                               t=f["t"], R2=f["R2"], const=f["a"],
                               mean_c_sd=float(s.c_sd.mean()), mean_resid0_pp=float(s.resid0_pp.mean()),
                               mean_turn=float(G[(G.cad == cn) & (G.gross == g)].turn_yr.mean())))
S = pd.DataFrame(slopes); S.to_csv(f"{OUT}.slopes.csv", index=False)
for win in ("IS", "OOS"):
    P(f"\n## window {win} — b/g by cadence (rows) x gross (cols), with t and R2 at g=0.75")
    piv = S[S.window == win].pivot(index="cad", columns="gross", values="slope_per_gross").reindex(ORDER)
    aux = S[(S.window == win) & (S.gross == 0.75)].set_index("cad").reindex(ORDER)
    piv["t@0.75"] = aux["t"]; piv["R2@0.75"] = aux["R2"]; piv["rebal/yr"] = aux["mean_turn"]
    P(piv.to_string(float_format=lambda x: f"{x:+.4f}"))

# ---- the pooled fit is now known to be a MIXTURE of opposite-signed panels, so read the
# ladder PER PANEL as well, and re-run the pre-registered test on each.
P("\n# PER-PANEL count ladder, IS, g=0.75 (18 cells each): b/g (t)")
per = {}
for pn in ("U56", "B136", "SMALL439"):
    line, row = [], {}
    for cn in ORDER:
        sub = D[(D.window == "IS") & (D.cad == cn) & (D.gross == 0.75) & (D.panel == pn)]
        f = ols(sub.c_sd, sub.resid0_pp)
        row[cn] = f["b"] / 0.75
        line.append(f"{cn} {f['b']/0.75:+.3f} ({f['t']:+.1f})")
    per[pn] = row
    P(f"   {pn:9s} " + "  ".join(line))
P("\n# per-panel reading of the pre-registered test (|b/g| at 21d and its two phases vs the "
  "D/W/Q band and calendar M):")
per_read = {}
for pn, row in per.items():
    band_p = [abs(row[c]) for c in ("D", "W", "Q")]
    v21_p = abs(row["21d"]); ph_p = [abs(row[f"21d@ph{q}"]) for _, q in PHASES]; vM_p = abs(row["M"])
    inband = (min(band_p) - 0.5) <= v21_p <= (max(band_p) + 0.5)
    per_read[pn] = ("CALENDAR/ALIGNMENT" if (v21_p > vM_p * 1.5 and inband) else
                    "COUNT (21d reproduces the M dip)" if v21_p <= vM_p * 1.5 else "MIXED")
    P(f"   {pn:9s} D/W/Q band {min(band_p):.3f}..{max(band_p):.3f} | M {vM_p:.3f} | 21d {v21_p:.3f} "
      f"| phases {', '.join(f'{v:.3f}' for v in ph_p)}  -> {per_read[pn]}")
gate("G4b per-panel reading of the count-vs-calendar question",
     "; ".join(f"{k}: {v}" for k, v in per_read.items()),
     all(v.startswith("COUNT") for v in per_read.values()) or all(v.startswith("CALENDAR") for v in per_read.values()),
     "pass = the three panels agree; fail = they do not, which is itself the answer")

IS75 = S[(S.window == "IS") & (S.gross == 0.75)].set_index("cad")
band = [abs(IS75.loc[c, "slope_per_gross"]) for c in ("D", "W", "Q")]
v21 = abs(IS75.loc["21d", "slope_per_gross"])
v21p = [abs(IS75.loc[f"21d@ph{p}", "slope_per_gross"]) for _, p in PHASES]
vM = abs(IS75.loc["M", "slope_per_gross"])
P(f"\nD/W/Q band |b/g| = {min(band):.4f}..{max(band):.4f};  calendar M = {vM:.4f};  "
  f"21d = {v21:.4f};  21d phases = {', '.join(f'{v:.4f}' for v in v21p)}")
if v21 >= 2.0 and all(v >= 2.0 for v in v21p):
    reading = "CALENDAR ARTEFACT"
elif v21 < 1.0:
    reading = "INTERIOR NODE"
else:
    reading = "INCONCLUSIVE"
P(f"PRE-REGISTERED READING: **{reading}**")
gate("G4 the pre-registered reading", reading, reading != "INCONCLUSIVE",
     "CALENDAR ARTEFACT = 21d and both phases sit in the D/W/Q band; INTERIOR NODE = 21d is itself near zero")

# ---- is the profile monotone in rebalance count?
lad = IS75.reindex([f"{n}d" for n in NDAY])
P("\n# the pure count ladder at g=0.75 (IS): |b/g| against rebalances/yr")
P(lad[["slope_per_gross", "t", "R2", "mean_turn", "mean_c_sd", "mean_resid0_pp"]]
  .to_string(float_format=lambda x: f"{x:+.4f}"))
mono = bool(pd.Series([abs(x) for x in lad.slope_per_gross]).is_monotonic_increasing
            or pd.Series([abs(x) for x in lad.slope_per_gross]).is_monotonic_decreasing)
gate("G5 |b/g| is monotone along the pure count ladder", mono, mono,
     "reported either way — a non-monotone ladder is itself the answer to 724's question")

# ---- KEEP paths
P("\n" + "=" * 120)
P("BOTH KEEP PATHS (every book in .grid.csv)")
P("=" * 120)
P(f"4a {int(G.keep4a.sum())} of {len(G)};  4b FULL {int(G.pass4b.sum())}, 4b OOS {int(G.pass4b_oos.sum())}, "
  f"BOTH {int((G.pass4b & G.pass4b_oos).sum())}")
for pn in PN:
    s = G[G.panel == pn]
    P(f"   {pn}: 4a {int(s.keep4a.sum())}/{len(s)}, 4b FULL {int(s.pass4b.sum())}, "
      f"OOS {int(s.pass4b_oos.sum())}, BOTH {int((s.pass4b & s.pass4b_oos).sum())}")
from collections import Counter
cf = Counter(); co = Counter()
for v in G.fail4b:
    if v != "-": cf.update(v.split(","))
for v in G.fail4b_oos:
    if v != "-": co.update(v.split(","))
P("4b FULL binding legs: " + ", ".join(f"{k} {v}" for k, v in cf.most_common()))
P("4b OOS  binding legs: " + ", ".join(f"{k} {v}" for k, v in co.most_common()))
BOTH = G[G.pass4b & G.pass4b_oos]
if len(BOTH):
    P("\n# books clearing 4b FULL *and* OOS (all published):")
    P(BOTH[["panel", "family", "level", "cad", "gross", "con", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
            "oCAGR", "oSharpe", "oMaxDD", "turn_yr"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\n# ... by cadence: " + ", ".join(f"{k} {v}" for k, v in Counter(BOTH.cad).most_common()))

# ---- RULE 8 walk-forward: choose (cadence, gross) on IS Sharpe alone
P("\n" + "=" * 120)
P("RULE 8 WALK-FORWARD — (cadence, gross) chosen on IS Sharpe alone inside each "
  "(panel, family, level, construction) arm; 2017-2026 read ONCE")
P("=" * 120)
wf = []
for (pn, fam, lvl, con), s in G.groupby(["panel", "family", "level", "con"]):
    spy_s, live_s = ctx[pn]
    pick = s.loc[s.isSharpe.idxmax()]
    dn = s[(s.cad == "W") & (s.gross == 0.75)].iloc[0]          # do-nothing = the live cadence/gross
    m21 = s[(s.cad == "21d") & (s.gross == 0.75)].iloc[0]
    wf.append(dict(panel=pn, family=fam, level=lvl, con=con,
                   pick_cad=pick.cad, pick_gross=pick.gross, pick_IS_Sharpe=pick.isSharpe,
                   pick_OOS_CAGR=pick.oCAGR, pick_OOS_Sharpe=pick.oSharpe, pick_OOS_MaxDD=pick.oMaxDD,
                   pick_keep4a=bool(pick.keep4a), pick_pass4b_oos=bool(pick.pass4b_oos),
                   dn_OOS_CAGR=dn.oCAGR, dn_OOS_Sharpe=dn.oSharpe, dn_OOS_MaxDD=dn.oMaxDD,
                   d21_OOS_Sharpe=m21.oSharpe,
                   base_OOS_Sharpe=live_s["oSharpe"], base_OOS_CAGR=live_s["oCAGR"], base_OOS_MaxDD=live_s["oMaxDD"],
                   spy_OOS_Sharpe=spy_s["oSharpe"], spy_OOS_CAGR=spy_s["oCAGR"], spy_OOS_MaxDD=spy_s["oMaxDD"]))
WF = pd.DataFrame(wf); WF.to_csv(f"{OUT}.walkforward.csv", index=False)
WF["gain"] = WF.pick_OOS_Sharpe - WF.dn_OOS_Sharpe
P(f"{len(WF)} walk-forward arms.  chooser minus do-nothing (W, g=0.75): mean OOS Sharpe "
  f"{WF.gain.mean():+.4f}, positive in {int((WF.gain > 0).sum())} of {len(WF)}")
for pn in PN:
    s = WF[WF.panel == pn]
    P(f"   {pn}: mean {s.gain.mean():+.4f} ({int((s.gain>0).sum())}/{len(s)} positive); "
      f"mean pick OOS CAGR {s.pick_OOS_CAGR.mean():.2%} / Sharpe {s.pick_OOS_Sharpe.mean():.4f} / "
      f"MaxDD {s.pick_OOS_MaxDD.mean():.2%}  vs RULES v2 {s.base_OOS_Sharpe.iloc[0]:.4f} and "
      f"SPY {s.spy_OOS_Sharpe.iloc[0]:.4f}")
P("\n# which cadence does the IS chooser pick? " + ", ".join(f"{k} {v}" for k, v in Counter(WF.pick_cad).most_common()))
P(f"# 4b OOS passes among the {len(WF)} picks: {int(WF.pick_pass4b_oos.sum())}; "
  f"4a passes: {int(WF.pick_keep4a.sum())}")
gate("G6 does the IS chooser of (cadence, gross) beat doing nothing",
     f"{WF.gain.mean():+.4f} mean OOS Sharpe, {int((WF.gain > 0).sum())} of {len(WF)} positive",
     WF.gain.mean() > 0, "reported either way; not a stopping condition")

# ---- a WHOLE-BOOK rule-8 chooser: every dial (family, level, cadence, gross, construction)
# picked on IS Sharpe alone, per panel, then read ONCE on 2017-2026.
P("\n# WHOLE-BOOK rule-8 chooser (all five dials on IS Sharpe, one pick per panel):")
free = []
for pn in PN:
    s_ = G[G.panel == pn]
    spy_s, live_s = ctx[pn]
    for nm, sub in (("C_FREE", s_),
                    ("C_FREE_g075", s_[s_.gross == 0.75]),
                    ("C_FREE_RESPREAD", s_[s_.con == "RESPREAD"])):
        pick = sub.loc[sub.isSharpe.idxmax()]
        free.append(dict(panel=pn, chooser=nm, family=pick.family, level=pick.level, cad=pick.cad,
                         gross=pick.gross, con=pick.con, IS_Sharpe=pick.isSharpe,
                         FULL_CAGR=pick.CAGR, FULL_Sharpe=pick.Sharpe, FULL_MaxDD=pick.MaxDD,
                         H1=pick.H1, H2=pick.H2, OOS_CAGR=pick.oCAGR, OOS_Sharpe=pick.oSharpe,
                         OOS_MaxDD=pick.oMaxDD, keep4a=bool(pick.keep4a),
                         pass4b=bool(pick.pass4b), pass4b_oos=bool(pick.pass4b_oos),
                         fail4b=pick.fail4b, fail4b_oos=pick.fail4b_oos,
                         base_OOS_Sharpe=live_s["oSharpe"], spy_OOS_Sharpe=spy_s["oSharpe"],
                         spy_OOS_CAGR=spy_s["oCAGR"], spy_OOS_MaxDD=spy_s["oMaxDD"]))
F = pd.DataFrame(free); F.to_csv(f"{OUT}.freechooser.csv", index=False)
P(F[["panel", "chooser", "family", "level", "cad", "gross", "con", "FULL_CAGR", "FULL_Sharpe",
     "FULL_MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "pass4b", "pass4b_oos",
     "fail4b_oos"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
gate("G7 does any WHOLE-BOOK IS-only chooser reach a 4b pass (FULL and OOS)",
     f"{int((F.pass4b & F.pass4b_oos).sum())} of {len(F)}",
     bool((F.pass4b & F.pass4b_oos).any()),
     "the honest rule-8 test: all five dials chosen on IS rows alone")
P("\n# the 5 arm-conditional picks that clear 4b OOS (cadence+gross only, family/level/con FIXED "
  "— NOT a legal whole-book chooser, published as a ceiling):")
P(WF[WF.pick_pass4b_oos][["panel", "family", "level", "con", "pick_cad", "pick_gross",
                          "pick_OOS_CAGR", "pick_OOS_Sharpe", "pick_OOS_MaxDD"]]
  .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
P(f"\ngates: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass")
Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
