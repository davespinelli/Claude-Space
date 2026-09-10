#!/usr/bin/env python3
"""IDEA 647 -- price-the-CAPACITY-CRITERION-s-own-two-constants   (cloud, 2026-09-10)

QUEUE: idea 427 re-derived idea 121's ADV floor from a criterion with two unswept numbers in
it -- a $10M TICKET and a 10% PARTICIPATION BAR, both stated once and never varied.  Sweep
both on the same 8-rung x 2-instrument ladder and report the floor each (ticket, bar) pair
selects, so PROTOCOL adopts a clause whose sensitivity to its own constants is published.

TWO TUNED PARAMETERS, exactly the queue's:
  TICKET in {$1M, 2, 5, 10, 20, 50, 100M}          (7 rungs, idea 121's $10M is one of them)
  BAR    in {2%, 5%, 7.5%, 10%, 15%, 20%, 25%}     (7 rungs, idea 121's 10% is one of them)
=> 49 pairs x 2 instruments (DV dollar floor / VOLSH matched share floor) = 98 selections,
   every one reported.  The floor LADDER (8 rungs), the book (EWALL/EWGATE/RANK20) and the
   cost rung (10/25 bps) are REPORTED axes, not tuned ones.

Construction is idea 427 lane B's, kept VERBATIM where it is load-bearing (panel, `fast_bt`,
the admission ladder and its matched share floors s*(F), `weights`, `capacity`) so the two
runs are directly comparable; G1-G3 gate that.

Report-only.  PROTOCOL.md, RULES.md, scan.py, bot.py and baseline.py are NOT touched.

SURVIVORSHIP (PROTOCOL 9): SMALL439 is a CURRENT-CONSTITUENT screen of sub-$2B names since
2010 with the 44 `max_1d_move >= 1.0` names dropped, and it is the only panel with cached
volume, so every number here is an upper bound on a tradable estimate.  The load-bearing
quantity is the floor-minus-floor contrast inside one panel, not any book's level.
"""
import sys, time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "research" / "backtests"
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, load_volume, rules_v2_weights, score   # noqa: E402
from engine import backtest as engine_backtest, metrics, rebalance_mask     # noqa: E402

STEM = str(Path(__file__).with_suffix(""))
FREQ, GROSS, MAX_VOL = "W", 0.75, 0.60
RUNGS = [10.0, 25.0]
PROTO_COST = 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
LEVELS = [0.0, 0.25e6, 0.5e6, 1e6, 2e6, 5e6, 10e6, 20e6]    # idea 427's ladder, verbatim
CLAUSE_F = 1e6                                              # the level idea 121 proposes
TICKETS = [1e6, 2e6, 5e6, 10e6, 20e6, 50e6, 100e6]          # tuned dial 1
BARS = [0.02, 0.05, 0.075, 0.10, 0.15, 0.20, 0.25]          # tuned dial 2
TICKET0, BAR0 = 10e6, 0.10                                  # idea 121's own pair
BOOKS = ["EWALL", "EWGATE", "RANK20"]
_LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _LOG.append(s)


# ---------------------------------------------------------------- engine (idea 427 lane B, verbatim)
def fast_bt(px, w, freq=FREQ):
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

    def _held(start_idx, rows=None):
        base = Cp[start_idx]
        top = Cp if rows is None else Cp[rows]
        g = np.divide(top, base, out=np.zeros_like(base), where=base != 0)
        raw = wt[start_idx] * g
        nav = raw.sum(axis=1) + (1.0 - wt[start_idx].sum(axis=1))
        nav = np.where(nav > 0, nav, 1.0)
        return raw / nav[:, None]

    held = _held(s0)
    gross = (held * rets).sum(axis=1)
    turn = np.zeros(T)
    turn[0] = np.abs(wt[0]).sum()
    if len(reb) > 1:
        rows = reb[1:]
        heldold = _held(s0[rows - 1], rows)
        turn[rows] = np.abs(wt[rows] - heldold).sum(axis=1)
    return pd.Series(gross, index=idx), pd.Series(turn, index=idx)


def net(gr, tn, bps):
    return gr - tn * bps / 1e4


def mrow(r):
    m = metrics(r)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                IS=metrics(r.loc[:IS_END])["Sharpe"],
                OOS=metrics(r.loc[OOS_START:])["Sharpe"],
                OOS_CAGR=metrics(r.loc[OOS_START:])["CAGR"],
                OOS_DD=metrics(r.loc[OOS_START:])["MaxDD"])


def v4a(L, B):
    return int(L["H1"] > B["H1"] and L["H2"] > B["H2"] and L["MaxDD"] >= B["MaxDD"])


def v4b(L, S):
    return int(L["H1"] > S["H1"] and L["H2"] > S["H2"] and L["OOS"] > S["OOS"]
               and L["MaxDD"] >= 0.60 * S["MaxDD"] and L["CAGR"] >= 0.70 * S["CAGR"])


# ---------------------------------------------------------------- panel (idea 427, verbatim)
T0 = time.time()
P("=" * 112)
P("IDEA 647  price-the-CAPACITY-CRITERION-s-own-two-constants   (cloud, 2026-09-10)")
P("=" * 112)
pxs = load_universe(small=True)
meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
px = pxs[[c for c in pxs.columns if c == "SPY" or c not in bad]].dropna(how="all").ffill()
TR = sorted({c for c in px.columns if c != "SPY"})
START = px.index[260]
P(f"[panel] SMALL439 {len(TR)} tradable (+SPY benchmark), {px.index[0].date()}..{px.index[-1].date()}, "
  f"evaluation from {START.date()}; dropped {len(bad)} names with max_1d_move >= 1.0")

VOL = load_volume(small=True).reindex(index=px.index).reindex(columns=px.columns)
TCOLS = [c for c in px.columns if c in set(TR)]
LIVE = px[TCOLS].notna()
DV = (px[TCOLS] * VOL[TCOLS]).rolling(20).median()          # dollar-volume instrument
SV = VOL[TCOLS].rolling(20).median()                        # share-volume instrument
DVv, SVv, LIVEv = DV.values, SV.values, LIVE.values
ev = px.index >= START
ALL_NAMES = float(LIVE.loc[START:].sum(axis=1).mean())
P(f"[panel] mean live tradable names/day over the evaluation window: {ALL_NAMES:.2f}")


def mask_dv(f):
    return LIVE.copy() if f <= 0 else LIVE & (DV >= f).fillna(False)


def mask_sv(s):
    return LIVE.copy() if s <= 0 else LIVE & (SV >= s).fillna(False)


def mean_names(vals, thr):
    m = LIVEv[ev] & np.nan_to_num(vals[ev] >= thr, nan=False) if thr > 0 else LIVEv[ev]
    return float(m.sum(axis=1).mean())


# ---------------------------------------------------------------- the matched share ladder
P("\n" + "-" * 112)
P("LADDER  the share floor s*(F) that matches each dollar floor's admission rate "
  "(idea 427's calibration, reproduced)")
P("-" * 112)
P(f"  {'DV floor':>12}{'names/day':>12}{'rate':>9}   {'s* (shares/day)':>17}{'names/day':>12}{'rate':>9}{'gap':>8}")
lrows, SSTAR = [], {}
for f in LEVELS:
    nd = mean_names(DVv, f)
    if f <= 0:
        s = 0.0
    else:
        lo, hi = 0.0, 5e7
        for _ in range(50):
            mid = 0.5 * (lo + hi)
            if mean_names(SVv, mid) > nd:
                lo = mid
            else:
                hi = mid
        s = 0.5 * (lo + hi)
    SSTAR[f] = s
    ns = mean_names(SVv, s)
    lrows.append(dict(dv_floor=f, dv_names=nd, dv_rate=nd / ALL_NAMES, s_star=s,
                      sv_names=ns, sv_rate=ns / ALL_NAMES, gap=ns - nd,
                      matched=abs(ns - nd) <= 0.5))
    P(f"  {f:>12,.0f}{nd:>12.2f}{nd/ALL_NAMES:>9.2%}   {s:>17,.0f}{ns:>12.2f}"
      f"{ns/ALL_NAMES:>9.2%}{ns-nd:>+8.2f}")
ladder = pd.DataFrame(lrows)
ladder.to_csv(f"{STEM}.ladder.csv", index=False)
assert bool(ladder["matched"].all()), "admission matching failed on some rung"
MASKS = {}
for f in LEVELS:
    MASKS[("DV", f)] = mask_dv(f)
    MASKS[("VOLSH", f)] = mask_sv(SSTAR[f])

# ---------------------------------------------------------------- books (idea 427, verbatim)
comp_score, above200, v20 = score(px[TCOLS], vol_scale=True)


def weights(book, adm):
    ok = LIVE & adm
    if book == "EWGATE":
        ok = ok & above200 & (v20 < MAX_VOL)
    if book in ("EWALL", "EWGATE"):
        w = ok.astype(float).div(ok.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0).mul(GROSS)
        return w.reindex(columns=px.columns).fillna(0.0), ok
    if book == "RANK20":
        e = comp_score.where(ok & above200 & (v20 < MAX_VOL))
        hold = (e.rank(axis=1, ascending=False) <= 20) & e.notna()
        w = hold.astype(float).div(hold.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0).mul(GROSS)
        return w.reindex(columns=px.columns).fillna(0.0), hold
    raise ValueError(book)


def capacity(hold, turn, start=None, end=None, capital=TICKET0):
    """idea 121's `capacity()`, VERBATIM in construction (idea 427 lane B): p25/p50 of the
    pooled (day, held-name) 20d median DOLLAR volume, and the share of that p25 name's ADV
    moved by one rebalance of `capital`;
    per_trade_frac = (turnover/yr / rebalances/yr) / mean names held.
    `end` is added here so the SAME criterion can be read on the IS window alone (rule 8)."""
    start = START if start is None else start
    h = hold.loc[start:end]
    flat = DV.loc[start:end].where(h).stack().dropna()
    if not len(flat):
        return dict(adv_p25=np.nan, adv_p50=np.nan, participation=np.nan,
                    turnover=np.nan, mean_names=np.nan, per_trade_frac=np.nan)
    p25, p50 = float(flat.quantile(0.25)), float(flat.quantile(0.50))
    t = turn.loc[start:end]
    yrs = len(t) / 252
    turnover = float(t.sum() / yrs)
    nreb = float((t > 0).sum()) / yrs
    nheld = float(h.sum(axis=1).replace(0, np.nan).mean())
    ptf = (turnover / nreb) / nheld
    return dict(adv_p25=p25, adv_p50=p50, turnover=turnover, mean_names=nheld,
                per_trade_frac=ptf, participation=ptf * capital / p25)


# ---------------------------------------------------------------- gates
P("\n" + "-" * 112)
P("GATES -- nothing below is read until these pass")
P("-" * 112)
_w, _ = weights("EWALL", MASKS[("DV", 0.0)])
_e = engine_backtest(px, _w, cost_bps=0, freq=FREQ)
_g, _t = fast_bt(px, _w)
_dg = float((_g - _e["returns"]).abs().max()); _dt = float((_t - _e["turnover"]).abs().max())
P(f"  G1 engine equivalence (EWall, floor $0): max|dgross| {_dg:.2e}  max|dturnover| {_dt:.2e}"
  f"  -> {'PASS' if max(_dg, _dt) < 1e-12 else 'FAIL'}")
assert max(_dg, _dt) < 1e-12
_rep = []
for f in (0.0, 1e6, 5e6, 20e6):
    _w, _ = weights("EWALL", MASKS[("DV", f)])
    _g, _t = fast_bt(px, _w)
    _rep.append(metrics(net(_g.loc[START:], _t.loc[START:], PROTO_COST))["CAGR"])
_tgt = [0.1018, 0.0592, 0.0164, -0.0492]
_mx = max(abs(a - b) for a, b in zip(_rep, _tgt))
P(f"  G2 idea 121's published EWall CAGR ladder (none/$1M/$5M/$20M) 10.18/5.92/1.64/-4.92%; "
  f"here {' / '.join(f'{x:.2%}' for x in _rep)} -> {'PASS' if _mx < 5e-4 else 'FAIL'} "
  f"(max |diff| {_mx*100:.3f} pp)")
assert _mx < 5e-4

# ---------------------------------------------------------------- the participation table
P("\n" + "-" * 112)
P("PART A  the criterion's INPUT, per instrument x floor: per-trade fraction and p25 held-name ADV")
P("        participation(ticket) = per_trade_frac * ticket / p25_ADV   [idea 121's own formula]")
P("-" * 112)
caprows = []
P(f"  {'instr':>6}{'floor':>12}{'names/day':>11}{'held':>7}{'turn/yr':>9}{'ptf':>9}"
  f"{'p25 ADV':>12}{'p50 ADV':>12}{'partic@$10M':>12}{'<=10%?':>8}")
BOOKW = {}
for instr in ("DV", "VOLSH"):
    for f in LEVELS:
        adm = MASKS[(instr, f)]
        w, hold = weights("RANK20", adm)
        gr, tn = fast_bt(px, w)
        BOOKW[(instr, f)] = (w, hold, gr, tn)
        c = capacity(hold, tn)
        cis = capacity(hold, tn, end=IS_END)
        nd = ladder.loc[ladder.dv_floor == f, "dv_names" if instr == "DV" else "sv_names"].iloc[0]
        caprows.append(dict(instr=instr, floor=f, share_floor=SSTAR[f] if instr == "VOLSH" else np.nan,
                            names=nd, held=c["mean_names"], turnover=c["turnover"],
                            ptf=c["per_trade_frac"], p25_dv=c["adv_p25"], p50_dv=c["adv_p50"],
                            participation_10M=c["participation"],
                            ptf_IS=cis["per_trade_frac"], p25_IS=cis["adv_p25"],
                            participation_10M_IS=cis["participation"],
                            passes_121=bool(c["participation"] <= BAR0)))
        P(f"  {instr:>6}{f:>12,.0f}{nd:>11.1f}{c['mean_names']:>7.1f}{c['turnover']:>9.2f}"
          f"{c['per_trade_frac']:>9.4f}{c['adv_p25']/1e6:>11.2f}M{c['adv_p50']/1e6:>11.2f}M"
          f"{c['participation']:>12.2%}{'YES' if c['participation'] <= BAR0 else 'no':>8}")
cap = pd.DataFrame(caprows)
cap.to_csv(f"{STEM}.capacity.csv", index=False)
r0 = cap[(cap.instr == "DV") & (cap.floor == 0.0)].iloc[0]
r1 = cap[(cap.instr == "DV") & (cap.floor == CLAUSE_F)].iloc[0]
P(f"  G3 idea 121 publishes the UNSCREENED RANK20 book at 17.6% participation and picks $1M as "
  f"the smallest passing rung.\n     here: unscreened {r0.participation_10M:.2%}, "
  f"$1M {r1.participation_10M:.2%} -> "
  f"{'REPRODUCES' if abs(r0.participation_10M-0.176) < 0.02 else 'DOES NOT REPRODUCE'} "
  f"(|diff| {abs(r0.participation_10M-0.176)*100:.2f} pp)")
assert abs(r0.participation_10M - 0.176) < 0.02


def select_floor(instr, ticket, bar, iswindow=False):
    """The clause as idea 121 words it: the SMALLEST ladder rung whose participation meets the
    bar.  Returns np.nan when no rung on the ladder clears it."""
    s = cap[cap.instr == instr]
    col = "ptf_IS" if iswindow else "ptf"
    p25c = "p25_IS" if iswindow else "p25_dv"
    ok = s[(s[col] * ticket / s[p25c]) <= bar]
    return float(ok.floor.min()) if len(ok) else np.nan


# ---------------------------------------------------------------- PART B: the 49-point grid
P("\n" + "-" * 112)
P("PART B  THE GRID: the floor each (TICKET, BAR) pair selects -- 7 x 7 x 2 instruments = 98 "
  "selections, all reported")
P("-" * 112)
grows = []
for instr in ("DV", "VOLSH"):
    P(f"\n  instrument {instr}   (selected floor in $M; '--' = no rung on the ladder clears the bar)")
    P("    " + "ticket \\ bar".ljust(14) + "".join(f"{b:>9.1%}" for b in BARS))
    for tk in TICKETS:
        cells = []
        for b in BARS:
            f = select_floor(instr, tk, b)
            fis = select_floor(instr, tk, b, iswindow=True)
            grows.append(dict(instr=instr, ticket=tk, bar=b, floor=f, floor_IS=fis,
                              ratio=tk / b, is121=(tk == TICKET0 and b == BAR0)))
            cells.append("--" if not np.isfinite(f) else f"{f/1e6:g}")
        P(f"    ${tk/1e6:>6,.0f}M      " + "".join(f"{c:>9}" for c in cells))
G = pd.DataFrame(grows)
G.to_csv(f"{STEM}.grid.csv", index=False)

sel = G[np.isfinite(G.floor)]
P(f"\n  {len(G)} selections; {int((~np.isfinite(G.floor)).sum())} pairs are UNSATISFIABLE on this "
  f"ladder (no rung reaches the bar).")
P(f"  DISTINCT floors selected: DV {sorted(set(G[G.instr=='DV'].floor.dropna()/1e6))} $M; "
  f"VOLSH {sorted(set(G[G.instr=='VOLSH'].floor.dropna()/1e6))} $M")
n121 = int((sel[sel.instr == "DV"].floor == CLAUSE_F).sum())
P(f"  idea 121's proposed $1M is selected by {n121} of {len(sel[sel.instr=='DV'])} satisfiable "
  f"DV pairs ({n121/max(len(sel[sel.instr=='DV']),1):.1%}); its own pair "
  f"(${TICKET0/1e6:.0f}M, {BAR0:.0%}) selects "
  f"${select_floor('DV',TICKET0,BAR0)/1e6:g}M (DV) and "
  f"${select_floor('VOLSH',TICKET0,BAR0)/1e6:g}M (VOLSH).")

# --- the structural point: participation is LINEAR in ticket, so the two constants are ONE
P("\n  IS IT REALLY TWO CONSTANTS?  participation = ptf * ticket / p25, so the criterion "
  "\n  `participation <= bar` is `ptf/p25 <= bar/ticket`: it can only depend on the RATIO "
  "ticket/bar.")
byratio = G.groupby(["instr", "ratio"]).floor.nunique()
P(f"    across all 98 cells, floors selected per (instrument, ticket/bar ratio) group: "
  f"max {int(byratio.max())} (1 == the collapse is exact); "
  f"{G.ratio.nunique()} distinct ratios among {len(TICKETS)*len(BARS)} pairs")
assert int(byratio.max()) == 1, "the ratio collapse should be exact by construction"
rat = (G[G.instr == "DV"].groupby("ratio").floor.first().reset_index()
       .sort_values("ratio"))
P("    the clause's ONE effective constant, k = ticket/bar ($M), and the DV floor it selects:")
P("      " + "  ".join(f"k={r.ratio/1e6:g}->{'--' if not np.isfinite(r.floor) else f'{r.floor/1e6:g}M'}"
                       for _, r in rat.iterrows()))
kk = rat[np.isfinite(rat.floor)]
P(f"    the selected floor is a STEP FUNCTION of k with {kk.floor.nunique()} steps over "
  f"{len(rat)} ratios; idea 121's k = ${TICKET0/BAR0/1e6:.0f}M.")

# ---------------------------------------------------------------- PART C: what the floor costs
P("\n" + "-" * 112)
P("PART C  WHAT THE SELECTED FLOOR COSTS: every ladder rung x 3 books x 2 rungs, both KEEP paths")
P("-" * 112)
spy = mrow(px["SPY"].pct_change().fillna(0.0).loc[START:])
gr_v2, tn_v2 = fast_bt(px, rules_v2_weights(px[TCOLS], band=0.03, gross=GROSS)
                       .reindex(columns=px.columns).fillna(0.0))
v2 = {c: mrow(net(gr_v2.loc[START:], tn_v2.loc[START:], c)) for c in RUNGS}
P(f"  comparands: SPY {spy['CAGR']:.2%} / {spy['Sharpe']:.4f} / {spy['MaxDD']:.2%} "
  f"(H1 {spy['H1']:.3f}, H2 {spy['H2']:.3f}, OOS {spy['OOS']:.4f});  RULES v2 @10bps "
  f"{v2[10.0]['CAGR']:.2%} / {v2[10.0]['Sharpe']:.4f} / {v2[10.0]['MaxDD']:.2%}")
brows = []
for book in BOOKS:
    for instr in ("DV", "VOLSH"):
        for f in LEVELS:
            if book == "RANK20":
                w, hold, gr, tn = BOOKW[(instr, f)]
            else:
                w, hold = weights(book, MASKS[(instr, f)])
                gr, tn = fast_bt(px, w)
            for c in RUNGS:
                L = mrow(net(gr.loc[START:], tn.loc[START:], c))
                brows.append(dict(book=book, instr=instr, floor=f, rung=c, **L,
                                  pass4a=v4a(L, v2[c]), pass4b=v4b(L, spy),
                                  v2_Sharpe=v2[c]["Sharpe"], v2_OOS=v2[c]["OOS"],
                                  spy_OOS=spy["OOS"], spy_CAGR=spy["CAGR"], spy_DD=spy["MaxDD"]))
B = pd.DataFrame(brows)
B.to_csv(f"{STEM}.books.csv", index=False)
P(f"  {len(B)} book-rows committed.  4a passes {int(B.pass4a.sum())}/{len(B)}; "
  f"4b passes {int(B.pass4b.sum())}/{len(B)}.")
for book in BOOKS:
    s = B[(B.book == book) & (B.instr == "DV") & (B.rung == PROTO_COST)].sort_values("floor")
    P(f"    {book:7s} DV @10bps  CAGR by floor: "
      + "  ".join(f"${r.floor/1e6:g}M {r.CAGR:+.2%}" for _, r in s.iterrows()))
    P(f"    {book:7s} DV @10bps  Sharpe/OOS   : "
      + "  ".join(f"${r.floor/1e6:g}M {r.Sharpe:.2f}/{r.OOS:.2f}" for _, r in s.iterrows()))

# the cost of the constants: the spread of outcomes over the floors the grid can select
P("\n  THE PRICE OF THE TWO CONSTANTS -- the spread of the SELECTED book across the grid:")
P(f"    {'book':8s}{'instr':>6}{'rung':>6}  {'floors selectable':>22}{'CAGR spread':>14}"
  f"{'Sharpe spread':>15}{'OOS spread':>13}")
prows = []
for book in BOOKS:
    for instr in ("DV", "VOLSH"):
        fl = sorted(set(G[(G.instr == instr) & np.isfinite(G.floor)].floor))
        for c in RUNGS:
            s = B[(B.book == book) & (B.instr == instr) & (B.rung == c) & (B.floor.isin(fl))]
            if not len(s):
                continue
            prows.append(dict(book=book, instr=instr, rung=c, nfloors=len(fl),
                              cagr_lo=s.CAGR.min(), cagr_hi=s.CAGR.max(),
                              sh_lo=s.Sharpe.min(), sh_hi=s.Sharpe.max(),
                              oos_lo=s.OOS.min(), oos_hi=s.OOS.max()))
            P(f"    {book:8s}{instr:>6}{c:>6.0f}  "
              f"{', '.join(f'${x/1e6:g}M' for x in fl):>22}"
              f"{s.CAGR.max()-s.CAGR.min():>13.2%} {s.Sharpe.max()-s.Sharpe.min():>14.3f}"
              f"{s.OOS.max()-s.OOS.min():>13.3f}")
pd.DataFrame(prows).to_csv(f"{STEM}.spread.csv", index=False)

# ---------------------------------------------------------------- PROTOCOL 8
P("\n" + "-" * 112)
P("PROTOCOL 8  WALK-FORWARD: the floor is chosen on 2010-2016 ONLY, then 2017-2026 is read once")
P("            two choosers: (A) the CAPACITY CRITERION read on the IS window, (B) IS Sharpe")
P("-" * 112)
wrows = []
for book in BOOKS:
    for instr in ("DV", "VOLSH"):
        for c in RUNGS:
            s = B[(B.book == book) & (B.instr == instr) & (B.rung == c)].set_index("floor")
            # chooser A: idea 121's clause, its own pair, computed on the IS window alone
            fA = select_floor(instr, TICKET0, BAR0, iswindow=True)
            # chooser B: the return-based control
            fB = float(s.IS.astype(float).idxmax())
            f0 = 0.0                       # no-floor control
            for nm, f in (("A capacity (IS)", fA), ("B IS-Sharpe", fB), ("C no floor", f0)):
                if not np.isfinite(f) or f not in s.index:
                    wrows.append(dict(book=book, instr=instr, rung=c, chooser=nm, floor=np.nan))
                    continue
                r = s.loc[f]
                wrows.append(dict(book=book, instr=instr, rung=c, chooser=nm, floor=f,
                                  IS=r.IS, OOS=r.OOS, OOS_CAGR=r.OOS_CAGR, OOS_DD=r.OOS_DD,
                                  CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD,
                                  pass4a=int(r.pass4a), pass4b=int(r.pass4b),
                                  v2_OOS=r.v2_OOS, spy_OOS=r.spy_OOS))
W = pd.DataFrame(wrows)
W.to_csv(f"{STEM}.wf.csv", index=False)
P(f"    {'book':8s}{'instr':>6}{'rung':>5} {'chooser':17s}{'floor':>8}{'OOS Sh':>9}{'OOS CAGR':>10}"
  f"{'OOS DD':>9}{'4a':>4}{'4b':>4} | {'v2 OOS':>8}{'SPY OOS':>9}")
for _, r in W.dropna(subset=["floor"]).iterrows():
    P(f"    {r.book:8s}{r.instr:>6}{r.rung:>5.0f} {r.chooser:17s}${r.floor/1e6:>6.2f}M"
      f"{r.OOS:>9.4f}{r.OOS_CAGR:>10.2%}{r.OOS_DD:>9.2%}{int(r.pass4a):>4}{int(r.pass4b):>4} | "
      f"{r.v2_OOS:>8.4f}{r.spy_OOS:>9.4f}")
A = W[W.chooser == "A capacity (IS)"].set_index(["book", "instr", "rung"])
Bc = W[W.chooser == "B IS-Sharpe"].set_index(["book", "instr", "rung"]).reindex(A.index)
Cc = W[W.chooser == "C no floor"].set_index(["book", "instr", "rung"]).reindex(A.index)
same = int((A.floor == Bc.floor).sum())
P(f"\n  the capacity chooser and the IS-Sharpe chooser pick the SAME floor in {same} of {len(A)} "
  f"cells; mean OOS Sharpe capacity {A.OOS.mean():.4f} vs IS-Sharpe {Bc.OOS.mean():.4f} "
  f"({A.OOS.mean()-Bc.OOS.mean():+.4f})")
P(f"  the capacity floor vs the NO-FLOOR control: mean OOS Sharpe {A.OOS.mean():.4f} vs "
  f"{Cc.OOS.mean():.4f} ({A.OOS.mean()-Cc.OOS.mean():+.4f}); it wins in "
  f"{int((A.OOS > Cc.OOS).sum())} of {len(A)} cells")
P(f"  IS-window vs FULL-sample selection at idea 121's own pair: "
  + ", ".join(f"{i} IS ${select_floor(i,TICKET0,BAR0,True)/1e6:g}M vs full "
              f"${select_floor(i,TICKET0,BAR0)/1e6:g}M" for i in ("DV", "VOLSH")))
P(f"  KEEP paths over the whole run: 4a {int(B.pass4a.sum())}/{len(B)}, "
  f"4b {int(B.pass4b.sum())}/{len(B)}.")

P(f"\ndone in {time.time()-T0:.0f}s")
Path(f"{STEM}.txt").write_text("\n".join(_LOG) + "\n")
