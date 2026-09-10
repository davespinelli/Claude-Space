#!/usr/bin/env python3
"""QUEUE idea 647 — price-the-CAPACITY-CRITERION-s-own-two-constants  (lane B, 2026-09-10).

Question (verbatim from QUEUE)
-----------------------------
"idea 427 re-derived idea 121's floor from a criterion with two unswept numbers in it: a
$10M ticket and a 10% participation bar, both stated once and never varied.  Sweep both on
the same 8-rung x 2-instrument ladder and report the floor each (ticket, bar) pair selects,
so PROTOCOL adopts a clause whose sensitivity to its own constants is published."

What is on trial.  Not a book — the CRITERION idea 427 recommended PROTOCOL adopt in place
of a fixed $1M default:

    the smallest floor at which one rebalance of a TICKET of capital moves <= BAR of the
    p25 held-name 20d median dollar volume of the run's own narrowest book.

427 solved it once, at (TICKET, BAR) = ($10M, 10%), and got $0.50M on an 8-rung ladder
where idea 121's 4-rung ladder had got $1M.  Both constants were typed in and never moved.
A clause whose answer is a free function of two unpublished numbers is not a clause, so
this run sweeps them and publishes the whole surface — 8 tickets x 8 bars x 2 instruments
x the same 8-rung ladder, every point reported.

PRE-REGISTERED PREDICTIONS (fixed before any number below was read)
------------------------------------------------------------------
P1  THE TWO CONSTANTS ARE ONE.  427's `participation` is linear in the ticket and the bar
    enters only as a threshold on it, so the selected floor should depend on (ticket, bar)
    ONLY through the ratio R = ticket / bar.  Falsified if any two pairs with the same R
    select different floors, on either instrument.  (Predicted, not assumed: the criterion
    is re-solved numerically at every one of the 64 pairs and the collapse is TESTED.)
P2  THE SURFACE IS WIDE.  Across the 64 pairs at least 4 of the 8 ladder rungs are selected
    by some pair on the DV ladder — i.e. more than half the ladder is reachable by moving
    constants nobody swept.  Falsified if <= 2 distinct rungs are ever selected.
P3  THE PUBLISHED DEFAULT IS NOT ROBUST.  idea 121's $1M is selected by fewer than a quarter
    of the 64 pairs on the coarse ladder, and by none of them on a refined ladder.
P4  THE INSTRUMENTS AGREE.  DV and admission-matched VOLSH select the same rung on >= 75%
    of the 64 pairs (427 found they agree at the one pair it ran).
P5  RULE 8 DOES NOT PAY.  A ratio R chosen on 2010-2016 by IS Sharpe does not beat the
    NO-FLOOR control out of sample in more than half the cells, and no floor clears 4b.

Design (PROTOCOL rules 1-9)
---------------------------
Panel      SMALL439, idea 427's `build_panel` verbatim (the ONLY panel with volume cached;
           `load_volume` raises for U56/broad136 — that is queue idea 429 and needs network).
           SURVIVORSHIP: current constituents of a sub-$2B screen.  Every capacity number
           below is a dollar-volume statistic on names that are still listed today, so the
           thin cohort a floor argues about is the cohort that is missing.  Only
           FLOOR-MINUS-FLOOR and PAIR-MINUS-PAIR contrasts on the same days are read.
Ladder     8 rungs, idea 427's: {$0, $0.25M, $0.5M, $1M, $2M, $5M, $10M, $20M}, plus a
           33-rung log-refined ladder used ONLY to price the coarse ladder's resolution.
Instruments 2: DV `(px*vol).rolling(20).median() >= F` and VOLSH `vol.rolling(20).median()
           >= s*(F)` with s*(F) solved from an admission identity (no return input), exactly
           as idea 427 calibrated it.
Books      idea 121's three at gross 0.75: EWALL, EWGATE, RANK20.  The criterion is defined
           on the narrowest book, RANK20, so that is what solves it; all three are priced.
TUNED      EXACTLY 2: `ticket` and `bar`.  The ladder, the books, the panel, the cadence,
           the gross and the p25 quantile are idea 121's/427's and are held fixed; where a
           third dial is varied at all (p50 instead of p25) it is a DIAGNOSTIC that selects
           nothing and is labelled as such.
Costs      0/5/10/25 bps reported, 10 bps decides (PROTOCOL 2).  Weekly, next-day (engine).
Rule 8     IS 2010-2016 / OOS 2017-2026, run twice: (a) on the CRITERION itself — solve the
           floor on the IS window alone and read the OOS book — and (b) on the RATIO — pick
           R by IS Sharpe and read the OOS book, against no-floor, against the published
           $1M, against live RULES v2 and against SPY.

Outputs: .console.txt .capacity.csv .surface.csv .refined.csv .grid.csv .walkforward.csv
Run:     python research/backtests/2026-09-10_price-the-CAPACITY-CRITERION-s-own-two-constants_B.py
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "research" / "backtests"
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, load_volume, rules_v2_weights, score  # noqa: E402
from engine import metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-10_price-the-CAPACITY-CRITERION-s-own-two-constants_B"
FREQ, GROSS, MAX_VOL = "W", 0.75, 0.60
COSTS = [0, 5, 10, 25]
PROTO_COST = 10
IS_END, OOS_START = "2016-12-31", "2017-01-01"
LEVELS = [0.0, 0.25e6, 0.5e6, 1e6, 2e6, 5e6, 10e6, 20e6]     # idea 427's 8-rung ladder
CLAUSE_F = 1e6                                               # idea 121's published default
BOOKS = ["EWALL", "EWGATE", "RANK20"]
CRIT_BOOK = "RANK20"                                         # the narrowest book: it solves

# --- THE TWO TUNED PARAMETERS -------------------------------------------------------------
TICKETS = [1e6, 2.5e6, 5e6, 10e6, 25e6, 50e6, 100e6, 250e6]  # 427/121 used 10e6
BARS = [0.02, 0.05, 0.075, 0.10, 0.15, 0.20, 0.25, 1.0 / 3]  # 427/121 used 0.10
REF_TICKET, REF_BAR = 10e6, 0.10                             # the published pair
# refined ladder, used only to price the COARSE ladder's resolution (idea 646's defect)
REFINED = [0.0] + list(np.exp(np.linspace(np.log(2.5e4), np.log(20e6), 32)))

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# ------------------------------------------------------------------ engine (idea 427's fast_bt)
def fast_bt(px, w, freq=FREQ):
    """Exact vectorised equivalent of engine.backtest, gross returns and turnover separately so
    the cost rung is a post-hoc sweep.  Gated against engine.backtest at G1 below."""
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
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def build_panel():
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in pxs.columns if c == "SPY" or c not in bad]
    pxs = pxs[keep].dropna(how="all").ffill()
    return pxs, sorted({c for c in pxs.columns if c != "SPY"})


T0 = time.time()
P("=" * 118)
P("IDEA 647  price-the-CAPACITY-CRITERION-s-own-two-constants   (lane B, 2026-09-10)")
P("=" * 118)
px, TR = build_panel()
START = px.index[260]
P(f"[panel] SMALL439 {len(TR)} tradable (+SPY benchmark), {px.index[0].date()}..{px.index[-1].date()},"
  f" evaluation from {START.date()}")
P("[coverage] SMALL439 is the only panel with volume cached (load_volume raises for U56/broad136;")
P("           that is queue idea 429 and needs network).  SURVIVORSHIP: current constituents.")

VOL = load_volume(small=True).reindex(index=px.index).reindex(columns=px.columns)
TCOLS = [c for c in px.columns if c in set(TR)]
LIVE = px[TCOLS].notna()
DV = (px[TCOLS] * VOL[TCOLS]).rolling(20).median()
SV = VOL[TCOLS].rolling(20).median()
DVv, SVv, LIVEv = DV.values, SV.values, LIVE.values
ev = px.index >= START
ALL_NAMES = float(LIVE.loc[START:].sum(axis=1).mean())
P(f"[panel] mean live tradable names/day over the evaluation window: {ALL_NAMES:.2f}")


def mean_names_dv(f):
    m = LIVEv[ev] & np.nan_to_num(DVv[ev] >= f, nan=False) if f > 0 else LIVEv[ev]
    return float(m.sum(axis=1).mean())


def mean_names_sv(s):
    m = LIVEv[ev] & np.nan_to_num(SVv[ev] >= s, nan=False) if s > 0 else LIVEv[ev]
    return float(m.sum(axis=1).mean())


def s_star(f):
    """Share floor matching the dollar floor f's mean admitted names/day (admission identity)."""
    if f <= 0:
        return 0.0
    nd = mean_names_dv(f)
    lo, hi = 0.0, 5e7
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        if mean_names_sv(mid) > nd:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def mask_of(instr, f):
    if f <= 0:
        return LIVE.copy()
    if instr == "DV":
        return LIVE & (DV >= f).fillna(False)
    return LIVE & (SV >= s_star(f)).fillna(False)


comp_score, above200, v20 = score(px[TCOLS], vol_scale=True)


def weights(book, adm):
    """idea 121's book conventions verbatim, `adm` standing in for its `dv20 >= floor` clause."""
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


def cap_terms(hold, turn, lo=None, hi=None):
    """idea 121's `capacity()` split into the parts that DO and DO NOT depend on the ticket.

    participation = per_trade_frac * capital / p25, so `kappa = per_trade_frac / p25` is the
    participation per DOLLAR of ticket and carries everything the panel contributes."""
    lo = START if lo is None else lo
    h = hold.loc[lo:hi] if hi is not None else hold.loc[lo:]
    d = DV.loc[lo:hi] if hi is not None else DV.loc[lo:]
    flat = d.where(h).stack().dropna()
    if not len(flat):
        return dict(adv_p25=np.nan, adv_p50=np.nan, kappa=np.nan, kappa50=np.nan,
                    turnover=np.nan, mean_names=np.nan, nreb=np.nan)
    p25, p50 = float(flat.quantile(0.25)), float(flat.quantile(0.50))
    t = turn.loc[lo:hi] if hi is not None else turn.loc[lo:]
    yrs = len(t) / 252
    turnover = float(t.sum() / yrs)
    nreb = float((t > 0).sum()) / yrs
    nheld = float(h.sum(axis=1).replace(0, np.nan).mean())
    ptf = (turnover / nreb) / nheld
    return dict(adv_p25=p25, adv_p50=p50, kappa=ptf / p25, kappa50=ptf / p50,
                turnover=turnover, mean_names=nheld, nreb=nreb)


# ------------------------------------------------------------------ gates
P("\n" + "-" * 118)
P("GATES — nothing below is read until these pass")
P("-" * 118)
from engine import backtest as _engine_backtest  # noqa: E402
_w, _ = weights("EWALL", mask_of("DV", 0.0))
_e = _engine_backtest(px, _w, cost_bps=0, freq=FREQ)
_g, _t = fast_bt(px, _w)
_dg, _dt = float((_g - _e["returns"]).abs().max()), float((_t - _e["turnover"]).abs().max())
P(f"  G1 engine equivalence (EWall, floor $0): max|dgross| {_dg:.2e}  max|dturnover| {_dt:.2e}"
  f"  -> {'PASS' if max(_dg, _dt) < 1e-12 else 'FAIL'}")
assert max(_dg, _dt) < 1e-12

_rep = []
for f in (0.0, 1e6, 5e6, 20e6):
    _w, _ = weights("EWALL", mask_of("DV", f))
    _g, _t = fast_bt(px, _w)
    _rep.append(metrics(net(_g.loc[START:], _t.loc[START:], PROTO_COST))["CAGR"])
_d2 = max(abs(a - b) for a, b in zip(_rep, [0.1018, 0.0592, 0.0164, -0.0492]))
P(f"  G2 idea 121's published EWall g=0.75 CAGR ladder (none/$1M/$5M/$20M) 10.18/5.92/1.64/-4.92%;"
  f" here {' / '.join(f'{x:.2%}' for x in _rep)}  -> {'PASS' if _d2 < 5e-4 else 'FAIL'}"
  f" (max |diff| {_d2*100:.3f} pp)")
assert _d2 < 5e-4

# ------------------------------------------------------------------ Q1 the panel's kappa table
P("\n" + "-" * 118)
P("Q1  THE TICKET-FREE PART OF THE CRITERION")
P("    participation(F; ticket) = per_trade_frac(F) * ticket / p25(F) = kappa(F) * ticket")
P("    kappa is a pure panel+book statistic: it contains no ticket and no bar.")
P("-" * 118)
CAPROWS = []
HOLDTURN = {}
for instr in ("DV", "VOLSH"):
    for f in LEVELS:
        adm = mask_of(instr, f)
        w, hold = weights(CRIT_BOOK, adm)
        _gr, tn = fast_bt(px, w)
        HOLDTURN[(instr, f)] = (hold, tn)
        c = cap_terms(hold, tn)
        nd = mean_names_dv(f) if instr == "DV" else mean_names_sv(s_star(f))
        CAPROWS.append(dict(instr=instr, floor=f, share_floor=s_star(f) if instr == "VOLSH" else np.nan,
                            names=nd, rate=nd / ALL_NAMES, **c,
                            partic_ref=c["kappa"] * REF_TICKET))
CAP = pd.DataFrame(CAPROWS)
CAP.to_csv(OUT / f"{STEM}.capacity.csv", index=False)
P(f"  {'instr':>6}{'floor':>12}{'names/day':>11}{'held':>7}{'turn/yr':>9}{'p25 ADV':>11}"
  f"{'p50 ADV':>11}{'kappa (1/$)':>14}{'partic @$10M':>14}")
for _, r in CAP.iterrows():
    P(f"  {r.instr:>6}{r.floor:>12,.0f}{r.names:>11.1f}{r.mean_names:>7.1f}{r.turnover:>9.2f}"
      f"{r.adv_p25/1e6:>10.2f}M{r.adv_p50/1e6:>10.2f}M{r.kappa:>14.3e}{r.partic_ref:>14.2%}")
_u = CAP[(CAP.instr == "DV") & (CAP.floor == 0.0)].iloc[0]
P(f"\n  [reproduction] idea 121 publishes the UNSCREENED RANK20 book at 17.6% participation;"
  f" here {_u.partic_ref:.2%} -> {'REPRODUCES' if abs(_u.partic_ref-0.176) < 0.02 else 'DOES NOT'}")

# monotonicity of the criterion in the floor (idea 646's defect needs a monotone criterion)
P("\n  Is participation MONOTONE (non-increasing) in the floor?  A 'smallest passing rung' only")
P("  means 'the solution' if the passing set is an up-set.")
for instr in ("DV", "VOLSH"):
    k = CAP[CAP.instr == instr].sort_values("floor").kappa.values
    dec = bool(np.all(np.diff(k) <= 1e-12))
    ups = int((np.diff(k) > 1e-12).sum())
    P(f"    {instr:<6} kappa non-increasing over the 8 rungs: {dec}"
      f"{'' if dec else f'  ({ups} up-steps -> the passing set is NOT an up-set)'}")
MONO = {i: bool(np.all(np.diff(CAP[CAP.instr == i].sort_values('floor').kappa.values) <= 1e-12))
        for i in ("DV", "VOLSH")}

# ------------------------------------------------------------------ Q2 the 64-pair surface
P("\n" + "-" * 118)
P("Q2  THE SURFACE — every (ticket, bar) pair's selected floor, all 64 x 2 points reported")
P("    selection rule = idea 121's own: the SMALLEST ladder rung whose participation <= bar")
P("-" * 118)
KAP = {(r.instr, r.floor): r.kappa for _, r in CAP.iterrows()}


def solve(instr, ticket, bar, rungs=LEVELS, kap=None):
    """Smallest rung meeting the criterion; also the full passing set, so a non-monotone
    passing set is visible rather than hidden behind the min."""
    kap = KAP if kap is None else kap
    ok = [f for f in rungs if kap[(instr, f)] * ticket <= bar]
    return (min(ok) if ok else np.nan), len(ok)


SROWS = []
for tk in TICKETS:
    for br in BARS:
        for instr in ("DV", "VOLSH"):
            f, npass = solve(instr, tk, br)
            SROWS.append(dict(ticket=tk, bar=br, R=tk / br, instr=instr, floor=f,
                              n_passing=npass, is_ref=(tk == REF_TICKET and br == REF_BAR)))
S = pd.DataFrame(SROWS)
S.to_csv(OUT / f"{STEM}.surface.csv", index=False)

for instr in ("DV", "VOLSH"):
    P(f"\n  selected floor ($M; '--' = no rung on the ladder meets the bar) — instrument {instr}")
    P(f"      {'bar ->':<10}" + "".join(f"{b:>9.1%}" for b in BARS))
    for tk in TICKETS:
        cells = []
        for br in BARS:
            f = S[(S.ticket == tk) & (S.bar == br) & (S.instr == instr)].floor.iloc[0]
            cells.append("--" if not np.isfinite(f) else ("0" if f == 0 else f"{f/1e6:g}M"))
        P(f"      ${tk/1e6:<9.4g}" + "".join(f"{c:>9}" for c in cells))

_ref = S[(S.is_ref) & (S.instr == "DV")].floor.iloc[0]
P(f"\n  [reproduction] at the PUBLISHED pair (${REF_TICKET/1e6:.0f}M, {REF_BAR:.0%}) the DV ladder"
  f" selects ${_ref/1e6:.2f}M  -> {'REPRODUCES idea 427' if abs(_ref-0.5e6) < 1 else 'DOES NOT'}"
  f" (427 published $0.50M)")

P("\n  P1 — do the two constants collapse to the single ratio R = ticket / bar?")
bad = []
for R, g in S.groupby(S.R.round(6)):
    for instr in ("DV", "VOLSH"):
        gg = g[g.instr == instr]
        vals = {("nan" if not np.isfinite(x) else x) for x in gg.floor}
        if len(gg) > 1 and len(vals) > 1:
            bad.append((R, instr, sorted(vals, key=str)))
nR = S.R.round(6).nunique()
multi = int(sum(1 for R, g in S.groupby(S.R.round(6)) if len(g) > 2))
P(f"    {len(S)} (pair, instrument) points span {nR} distinct ratios; {multi} ratios are hit by"
  f" more than one (ticket, bar) pair.")
P(f"    disagreements within a ratio: {len(bad)}  ->  P1 {'HOLDS' if not bad else 'FALSIFIED'}"
  f" (the criterion has ONE constant, not two)")
# independent algebraic check: participation must be exactly linear in the ticket
_lin = []
for instr in ("DV", "VOLSH"):
    for f in LEVELS:
        hold, tn = HOLDTURN[(instr, f)]
        a = cap_terms(hold, tn)["kappa"] * 1e6
        b = cap_terms(hold, tn)["kappa"] * 250e6
        _lin.append(abs(b / 250.0 - a))
P(f"    linearity check |participation($250M)/250 - participation($1M)| max {max(_lin):.3e}"
  f"  -> {'exact' if max(_lin) < 1e-15 else 'NOT exact'}")

P("\n  P2 — how much of the ladder is reachable by moving the two unswept numbers?")
for instr in ("DV", "VOLSH"):
    sel = S[S.instr == instr].floor
    got = sorted({x for x in sel if np.isfinite(x)})
    P(f"    {instr:<6} distinct rungs selected {len(got)} of {len(LEVELS)}: "
      + ", ".join(("$0" if g == 0 else f"${g/1e6:g}M") for g in got)
      + f";  no rung meets the bar in {int((~np.isfinite(sel)).sum())}/{len(sel)} pairs")
DVSEL = sorted({x for x in S[S.instr == 'DV'].floor if np.isfinite(x)})
P(f"    P2 {'HOLDS' if len(DVSEL) >= 4 else 'FALSIFIED'} (>= 4 of 8 rungs reachable on DV)")

P("\n  P3 — how often is idea 121's published $1M the answer?")
n1m = int((S[S.instr == "DV"].floor == CLAUSE_F).sum())
P(f"    $1M selected by {n1m}/{len(TICKETS)*len(BARS)} DV pairs ({n1m/(len(TICKETS)*len(BARS)):.1%})")

P("\n  P4 — do the two instruments select the same rung?")
agr = 0
for tk in TICKETS:
    for br in BARS:
        a = S[(S.ticket == tk) & (S.bar == br) & (S.instr == "DV")].floor.iloc[0]
        b = S[(S.ticket == tk) & (S.bar == br) & (S.instr == "VOLSH")].floor.iloc[0]
        agr += int((a == b) or (not np.isfinite(a) and not np.isfinite(b)))
P(f"    identical selection on {agr}/{len(TICKETS)*len(BARS)} pairs ({agr/64:.1%})"
  f"  -> P4 {'HOLDS' if agr >= 48 else 'FALSIFIED'}")

# the R step function: the criterion's ENTIRE content in one column
P("\n  THE CRITERION AS ONE DIAL.  Largest R at which each rung is still the answer")
P("  (R = ticket/bar in dollars; the published pair is R = $100M):")
Rgrid = np.exp(np.linspace(np.log(1e6), np.log(1e10), 400))
for instr in ("DV", "VOLSH"):
    steps, prev = [], None
    for R in Rgrid:
        f, _ = solve(instr, R, 1.0)
        key = "none" if not np.isfinite(f) else f
        if key != prev:
            steps.append((R, key))
            prev = key
    P(f"    {instr:<6} " + "  ".join(
        f"R>={R/1e6:,.0f}M -> " + ("no rung" if k == "none" else ("$0" if k == 0 else f"${k/1e6:g}M"))
        for R, k in steps))

# ------------------------------------------------------------------ Q3 ladder resolution
P("\n" + "-" * 118)
P("Q3  RESOLUTION — is the selected floor a SOLUTION or the coarsest rung above one?")
P("    (cross-link: queue idea 646.  Same criterion, same book, 33-rung log ladder $25k..$20M)")
P("-" * 118)
KAPR = {}
for instr in ("DV", "VOLSH"):
    for f in REFINED:
        w, hold = weights(CRIT_BOOK, mask_of(instr, f))
        _gr, tn = fast_bt(px, w)
        KAPR[(instr, f)] = cap_terms(hold, tn)["kappa"]
P(f"  [{time.time()-T0:.0f}s] refined ladder solved ({2*len(REFINED)} book solves)")
RROWS = []
for tk in TICKETS:
    for br in BARS:
        for instr in ("DV", "VOLSH"):
            fc, _ = solve(instr, tk, br)
            fr, _ = solve(instr, tk, br, rungs=REFINED, kap=KAPR)
            RROWS.append(dict(ticket=tk, bar=br, R=tk / br, instr=instr,
                              coarse=fc, refined=fr,
                              overshoot=(fc - fr) if (np.isfinite(fc) and np.isfinite(fr)) else np.nan))
RF = pd.DataFrame(RROWS)
RF.to_csv(OUT / f"{STEM}.refined.csv", index=False)
for instr in ("DV", "VOLSH"):
    d = RF[(RF.instr == instr) & RF.overshoot.notna()]
    exact = int((d.overshoot.abs() < 1).sum())
    P(f"    {instr:<6} coarse == refined on {exact}/{len(d)} pairs; median overshoot "
      f"${d.overshoot.median()/1e6:.2f}M, max ${d.overshoot.max()/1e6:.2f}M"
      f"  (mean overshoot ratio {float((d.coarse/d.refined.replace(0,np.nan)).median()):.2f}x)")
_r1 = RF[(RF.ticket == REF_TICKET) & (RF.bar == REF_BAR) & (RF.instr == "DV")].iloc[0]
P(f"    at the published pair: coarse ${_r1.coarse/1e6:.2f}M vs refined ${_r1.refined/1e6:.3f}M")
n1m_ref = int((RF[RF.instr == "DV"].refined == CLAUSE_F).sum())
P(f"    $1M is selected on the refined ladder by {n1m_ref}/64 DV pairs"
  f"  -> P3 {'HOLDS' if (n1m < 16 and n1m_ref == 0) else 'FALSIFIED'}"
  f" (coarse {n1m}/64 < 16 and refined {n1m_ref}/64 == 0)")

# DIAGNOSTIC (selects nothing): the criterion's unnamed THIRD constant, the p25 quantile
P("\n  DIAGNOSTIC, not a tuned dial — the criterion also fixes a QUANTILE (p25) nobody swept.")
P("  Re-solving at p50 (kappa50) moves the answer by:")
for instr in ("DV", "VOLSH"):
    k50 = {(i, f): CAP[(CAP.instr == i) & (CAP.floor == f)].kappa50.iloc[0] for i in ("DV", "VOLSH") for f in LEVELS}
    same = 0
    for tk in TICKETS:
        for br in BARS:
            a, _ = solve(instr, tk, br)
            b, _ = solve(instr, tk, br, kap=k50)
            same += int((a == b) or (not np.isfinite(a) and not np.isfinite(b)))
    P(f"    {instr:<6} p25 and p50 select the same rung on {same}/64 pairs")

# ------------------------------------------------------------------ Q4 decision surface
P("\n" + "-" * 118)
P("Q4  WHAT THE CONSTANTS BUY — the selected floors on the decision surface (both KEEP paths)")
P("-" * 118)
v2 = rules_v2_weights(px)
gr_b, tn_b = fast_bt(px, v2)
spy = px["SPY"].pct_change().fillna(0).loc[START:]
m_spy, m_spy_oos = mrow(spy), metrics(spy.loc[OOS_START:])
m_v2 = mrow(net(gr_b.loc[START:], tn_b.loc[START:], PROTO_COST))
P(f"  live RULES v2 @10bps: CAGR {m_v2['CAGR']:.2%} Sharpe {m_v2['Sharpe']:.3f} MaxDD {m_v2['MaxDD']:.1%}"
  f" H1 {m_v2['H1']:.3f} H2 {m_v2['H2']:.3f}")
P(f"  SPY:                  CAGR {m_spy['CAGR']:.2%} Sharpe {m_spy['Sharpe']:.3f} MaxDD {m_spy['MaxDD']:.1%}"
  f" H1 {m_spy['H1']:.3f} H2 {m_spy['H2']:.3f} | OOS Sharpe {m_spy_oos['Sharpe']:.3f}")

SERIES = {}
for book in BOOKS:
    for instr in ("DV", "VOLSH"):
        for f in LEVELS:
            w, _h = weights(book, mask_of(instr, f))
            gr, tn = fast_bt(px, w)
            SERIES[(book, instr, f)] = (gr.loc[START:], tn.loc[START:])
P(f"  [{time.time()-T0:.0f}s] {len(SERIES)} book x instrument x level series computed")


def path_verdicts(r):
    m = mrow(r)
    ba = [k for k, c in (("H1", m["H1"] <= m_v2["H1"]), ("H2", m["H2"] <= m_v2["H2"]),
                         ("DD", m["MaxDD"] < m_v2["MaxDD"])) if c]
    bb = [k for k, c in (("H1", m["H1"] <= m_spy["H1"]), ("H2", m["H2"] <= m_spy["H2"]),
                         ("OOS", metrics(r.loc[OOS_START:])["Sharpe"] <= m_spy_oos["Sharpe"]),
                         ("DD", m["MaxDD"] < 0.60 * m_spy["MaxDD"]),
                         ("CAGR", m["CAGR"] < 0.70 * m_spy["CAGR"])) if c]
    return ba, bb


grows = []
P(f"\n  {'book':<8}{'instr':>6}{'floor':>10}{'bps':>5}{'CAGR':>9}{'Sharpe':>8}{'MaxDD':>8}{'H1':>7}"
  f"{'H2':>7}{'turn':>7}  {'4a':<12}{'4b'}")
for book in BOOKS:
    for instr in ("DV", "VOLSH"):
        for f in LEVELS:
            gr, tn = SERIES[(book, instr, f)]
            typ = float(tn.sum() / (len(tn) / 252.0))
            for c in COSTS:
                r = net(gr, tn, c)
                m = mrow(r)
                ba, bb = path_verdicts(r)
                row = dict(book=book, instr=instr, floor=f, bps=c, **m, turn_yr=typ,
                           path4a="KEEP" if not ba else "KILL(" + ",".join(ba) + ")",
                           path4b="KEEP" if not bb else "KILL(" + ",".join(bb) + ")",
                           selected_by=int(((S.instr == instr) & (S.floor == f)).sum()))
                grows.append(row)
                if c == PROTO_COST:
                    P(f"  {book:<8}{instr:>6}{f:>10,.0f}{c:>5}{m['CAGR']:>9.2%}{m['Sharpe']:>8.3f}"
                      f"{m['MaxDD']:>8.1%}{m['H1']:>7.3f}{m['H2']:>7.3f}{typ:>7.2f}  "
                      f"{row['path4a']:<12}{row['path4b']}")
G = pd.DataFrame(grows)
G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
n = len(G)
P(f"\n  grid n={n} ({len(BOOKS)} books x 2 instruments x {len(LEVELS)} levels x {len(COSTS)} costs)")
P(f"  4a KEEP {(G.path4a=='KEEP').sum()}/{n};  4b KEEP {(G.path4b=='KEEP').sum()}/{n};  "
  f"BOTH {((G.path4a=='KEEP')&(G.path4b=='KEEP')).sum()}/{n}")
fb = pd.Series([x for s in G.path4b for x in (s[5:-1].split(",") if s.startswith("KILL") else [])]).value_counts()
P(f"  binding bars (4b): " + ", ".join(f"{k} {v}" for k, v in fb.items()))

# the spread the constants are worth, at the protocol rung
P("\n  The performance SPREAD the two unswept constants span (10 bps, over the rungs any pair selects):")
for book in BOOKS:
    for instr in ("DV", "VOLSH"):
        sub = G[(G.book == book) & (G.instr == instr) & (G.bps == PROTO_COST) & (G.selected_by > 0)]
        if len(sub) < 2:
            continue
        P(f"    {book:<8}{instr:>6}  CAGR {sub.CAGR.min():.2%}..{sub.CAGR.max():.2%}"
          f" ({(sub.CAGR.max()-sub.CAGR.min())*100:.2f} pp)   Sharpe {sub.Sharpe.min():.3f}..{sub.Sharpe.max():.3f}"
          f" ({sub.Sharpe.max()-sub.Sharpe.min():.3f})   over {len(sub)} selectable rungs")

# ------------------------------------------------------------------ Q5 rule 8
P("\n" + "-" * 118)
P("Q5  PROTOCOL RULE 8 — IS 2010-2016, OOS 2017-2026 read once")
P("-" * 118)
P("  (a) THE CRITERION ITSELF: solve it on the IS window alone and compare to the full-sample")
P("      solution.  A criterion whose own answer moves between windows is not a standing clause.")
KIS = {}
for instr in ("DV", "VOLSH"):
    for f in LEVELS:
        hold, tn = HOLDTURN[(instr, f)]
        KIS[(instr, f)] = cap_terms(hold, tn, lo=START, hi=IS_END)["kappa"]
same_win = 0
critrows = []
for tk in TICKETS:
    for br in BARS:
        for instr in ("DV", "VOLSH"):
            a, _ = solve(instr, tk, br)
            b, _ = solve(instr, tk, br, kap=KIS)
            ok = (a == b) or (not np.isfinite(a) and not np.isfinite(b))
            same_win += int(ok)
            critrows.append(dict(ticket=tk, bar=br, R=tk / br, instr=instr, full=a, is_only=b, same=ok))
CR = pd.DataFrame(critrows)
P(f"      IS-window solution == full-sample solution on {same_win}/{len(CR)} (pair, instrument) points"
  f" ({same_win/len(CR):.1%})")
_c1 = CR[(CR.ticket == REF_TICKET) & (CR.bar == REF_BAR) & (CR.instr == "DV")].iloc[0]
P(f"      at the published pair (DV): full ${_c1.full/1e6:.2f}M vs IS-only ${_c1.is_only/1e6:.2f}M")

P("\n  (b) THE RATIO AS A TUNED DIAL: pick R on IS Sharpe over the rungs the criterion can reach,")
P("      read OOS once, against no-floor / the published $1M / RULES v2 / SPY.")
wrows = []
for book in BOOKS:
    for instr in ("DV", "VOLSH"):
        for c in COSTS:
            R = {f: net(*SERIES[(book, instr, f)], c) for f in LEVELS}
            IS = {f: r.loc[:IS_END] for f, r in R.items()}
            OS = {f: r.loc[OOS_START:] for f, r in R.items()}
            pick = max(LEVELS, key=lambda f: metrics(IS[f])["Sharpe"])
            # the floor the PUBLISHED constants select, and the one an IS-solved criterion selects
            crit_full, _ = solve(instr, REF_TICKET, REF_BAR)
            crit_is, _ = solve(instr, REF_TICKET, REF_BAR, kap=KIS)
            row = dict(book=book, instr=instr, bps=c, pick_level=pick,
                       crit_level=crit_full, crit_is_level=crit_is)
            for tag, f in (("pick", pick), ("nofloor", 0.0), ("const1M", CLAUSE_F),
                           ("crit", crit_full if np.isfinite(crit_full) else 0.0),
                           ("critis", crit_is if np.isfinite(crit_is) else 0.0)):
                mo = metrics(OS[f])
                row[f"{tag}_oosCAGR"], row[f"{tag}_oosSharpe"], row[f"{tag}_oosMaxDD"] = (
                    mo["CAGR"], mo["Sharpe"], mo["MaxDD"])
            mb = metrics(net(gr_b.loc[START:], tn_b.loc[START:], c).loc[OOS_START:])
            row["v2_oosCAGR"], row["v2_oosSharpe"], row["v2_oosMaxDD"] = mb["CAGR"], mb["Sharpe"], mb["MaxDD"]
            row["spy_oosCAGR"], row["spy_oosSharpe"], row["spy_oosMaxDD"] = (
                m_spy_oos["CAGR"], m_spy_oos["Sharpe"], m_spy_oos["MaxDD"])
            wrows.append(row)
W = pd.DataFrame(wrows)
W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
P(f"  {'book':<8}{'instr':>6}{'bps':>5}{'IS pick':>11}{'OOS CAGR':>10}{'OOS Sh':>9}{'OOS DD':>9}"
  f"{'| nofloor':>11}{'$1M':>8}{'crit':>8}{'v2':>8}{'SPY':>8}")
for _, r in W.iterrows():
    P(f"  {r.book:<8}{r.instr:>6}{int(r.bps):>5}{r.pick_level:>11,.0f}{r.pick_oosCAGR:>10.2%}"
      f"{r.pick_oosSharpe:>9.3f}{r.pick_oosMaxDD:>9.1%}{r.nofloor_oosSharpe:>11.3f}"
      f"{r.const1M_oosSharpe:>8.3f}{r.crit_oosSharpe:>8.3f}{r.v2_oosSharpe:>8.3f}{r.spy_oosSharpe:>8.3f}")
P(f"\n  IS-Sharpe pick beats NO-FLOOR OOS {int((W.pick_oosSharpe > W.nofloor_oosSharpe).sum())}/{len(W)};"
  f" beats $1M {int((W.pick_oosSharpe > W.const1M_oosSharpe).sum())}/{len(W)};"
  f" beats RULES v2 {int((W.pick_oosSharpe > W.v2_oosSharpe).sum())}/{len(W)};"
  f" beats SPY {int((W.pick_oosSharpe > W.spy_oosSharpe).sum())}/{len(W)}")
P(f"  criterion floor beats NO-FLOOR OOS {int((W.crit_oosSharpe > W.nofloor_oosSharpe).sum())}/{len(W)};"
  f" beats SPY {int((W.crit_oosSharpe > W.spy_oosSharpe).sum())}/{len(W)}")
P(f"  mean OOS Sharpe: pick {W.pick_oosSharpe.mean():.3f}  crit {W.crit_oosSharpe.mean():.3f}"
  f"  critIS {W.critis_oosSharpe.mean():.3f}  nofloor {W.nofloor_oosSharpe.mean():.3f}"
  f"  $1M {W.const1M_oosSharpe.mean():.3f}  v2 {W.v2_oosSharpe.mean():.3f}  SPY {m_spy_oos['Sharpe']:.3f}")
P(f"  mean OOS CAGR:   pick {W.pick_oosCAGR.mean():.2%}  crit {W.crit_oosCAGR.mean():.2%}"
  f"  critIS {W.critis_oosCAGR.mean():.2%}  nofloor {W.nofloor_oosCAGR.mean():.2%}"
  f"  $1M {W.const1M_oosCAGR.mean():.2%}  v2 {W.v2_oosCAGR.mean():.2%}  SPY {m_spy_oos['CAGR']:.2%}")
P(f"  mean OOS MaxDD:  pick {W.pick_oosMaxDD.mean():.1%}  crit {W.crit_oosMaxDD.mean():.1%}"
  f"  critIS {W.critis_oosMaxDD.mean():.1%}  nofloor {W.nofloor_oosMaxDD.mean():.1%}"
  f"  $1M {W.const1M_oosMaxDD.mean():.1%}  v2 {W.v2_oosMaxDD.mean():.1%}  SPY {m_spy_oos['MaxDD']:.1%}")
P5_OK = int((W.pick_oosSharpe > W.nofloor_oosSharpe).sum()) <= len(W) / 2 and (G.path4b == "KEEP").sum() == 0
P(f"  P5 {'HOLDS' if P5_OK else 'FALSIFIED'}")

# ------------------------------------------------------------------ Q6 the wording
P("\n" + "-" * 118)
P("Q6  WHAT THE CLAUSE SHOULD SAY  (proposed for Sunday review; PROTOCOL.md is NOT edited here)")
P("-" * 118)
P(f"  (i)   The criterion has ONE free constant, not two: participation is exactly linear in the")
P(f"        ticket, so only R = ticket/bar is identified.  427's ($10M, 10%) is R = $100M, and so")
P(f"        is ($1M, 1%) and ($250M, 250%).  A clause that publishes both numbers publishes one.")
P(f"  (ii)  R is load-bearing: over the swept range it selects {len(DVSEL)} of the {len(LEVELS)} rungs on DV, and")
P(f"        {int((~np.isfinite(S[S.instr=='DV'].floor)).sum())}/64 pairs have NO admissible rung at all.")
P(f"  (iii) The coarse ladder overshoots the solution; $1M is the answer on {n1m}/64 coarse pairs and")
P(f"        {n1m_ref}/64 refined ones.")
P(f"  (iv)  It buys no return: rule 8 pays in {int((W.pick_oosSharpe > W.nofloor_oosSharpe).sum())}/{len(W)} cells and 4b passes {(G.path4b=='KEEP').sum()}/{n}.")
P("")
P("  PROPOSED amendment to idea 427's clause 10 (one sentence, replacing its two constants):")
P("")
P("     ... Choose `s` by solving the capacity criterion on the run's own narrowest book: the")
P("     smallest `s` at which one rebalance moves <= 10% of the p25 held-name 20d median DOLLAR")
P("     volume PER $100M of stated capital.  State that ratio (capital / participation bar), not")
P("     the two numbers separately -- they are not separately identified -- and solve on a ladder")
P("     refined until the next rung down fails, publishing the solving ladder.  A floor selected")
P("     from a coarse ladder is a resolution artefact, not a solution.")

# ------------------------------------------------------------------ verdict
P("\n" + "=" * 118)
P("VERDICT")
P("=" * 118)
P(f"  4a {(G.path4a=='KEEP').sum()}/{n}   4b {(G.path4b=='KEEP').sum()}/{n}   -> "
  f"{'KEEP-candidate present' if ((G.path4a=='KEEP')|(G.path4b=='KEEP')).any() else 'no KEEP'}")
P(f"  P1 {'HOLDS' if not bad else 'FALSIFIED'} | P2 {'HOLDS' if len(DVSEL) >= 4 else 'FALSIFIED'} | "
  f"P3 {'HOLDS' if (n1m < 16 and n1m_ref == 0) else 'FALSIFIED'} | "
  f"P4 {'HOLDS' if agr >= 48 else 'FALSIFIED'} | P5 {'HOLDS' if P5_OK else 'FALSIFIED'}")
P(f"  monotone criterion: DV {MONO['DV']}  VOLSH {MONO['VOLSH']}")
P(f"  runtime {time.time()-T0:.0f}s")

(OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
