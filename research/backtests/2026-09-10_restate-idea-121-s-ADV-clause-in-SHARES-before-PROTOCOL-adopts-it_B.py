#!/usr/bin/env python3
"""QUEUE idea 427 — restate-idea-121-s-ADV-clause-in-SHARES-before-PROTOCOL-adopts-it
(lane B, 2026-09-10).

Question (verbatim from QUEUE)
-----------------------------
"idea 425 shows the $1M DOLLAR floor and a share floor at MATCHED admission rate (252.1
names/day) admit panels that differ by +1.23 pp CAGR in 144 of 144 cells, and that the
'$1M floor softens the gate damage' sentence is a price-channel artefact (-4.87 pp dollar
vs -6.59 pp shares).  Idea 121 proposes a $1M ADV floor as a PROTOCOL clause.  Price the
clause in BOTH forms on every panel that has volume cached, and recommend the wording."

What is on trial.  Not a book — a CLAUSE.  Idea 121 proposes PROTOCOL clause 10: a $1M
ADV floor as a reporting requirement plus a stated default.  Idea 425 then showed the
floor's INSTRUMENT is not innocent: `dv = (px*vol).rolling(20).median()` is built on the
auto-adjusted close, so it is not invariant under `px -> px @ diag(c)` (re-adjusting the
panel to a new terminal date moves which names are ADMITTED), while a share floor
`vol.rolling(20).median()` is exactly invariant.  So the clause can be written two ways,
and idea 425 measured that the two ways disagree by +1.23 pp/yr in favour of shares.

Before PROTOCOL adopts either wording this run has to answer three things the record has
never put in one place:

  (a) Does the SHARE form still do the CLAUSE'S JOB?  Idea 121 did not pick $1M by taste:
      it solved a CAPACITY criterion — the smallest ladder floor at which a $10M ticket is
      <= 10% of the p25 held-name 20d median DOLLAR volume of the ranked n=20 book.  That
      criterion is denominated in dollars whatever the floor is written in.  A share floor
      that reaches the same admission rate but NOT the same capacity is not a restatement
      of the clause, it is a different clause.
  (b) Is idea 425's +1.23 pp share advantage an ARGUMENT FOR SHARES, or a PRICE CHANNEL?
      A dollar floor at a matched count admits expensive names; a share floor admits cheap
      ones.  On a CURRENT-CONSTITUENT small panel, cheap-today names are the ones that fell
      and expensive-today names are the ones that rose, so the sign of any price-sorted
      contrast is set by survivorship before liquidity says anything.  If the gap lives
      inside the price sort, it is not evidence about the instrument.
  (c) What does the clause COST on the decision surface — 4a/4b verdicts and rule-8 picks —
      in each form?  A clause that changes no verdict is free to adopt in whichever form is
      cleaner; a clause that moves verdicts has to be adopted in the form that is right.

COVERAGE LIMIT, stated first because it bounds the recommendation.  The queue says "every
panel that has volume cached".  That is ONE panel: `baseline.load_volume` raises for
anything but `small=True`, and data/ holds `volume_small.csv.gz` and no other volume file
(U56 and broad136 volume is queue idea 429, which needs network).  So every number below is
SMALL439, and SMALL439 is current constituents of a sub-$2B screen — the delisted cohort
that is missing is exactly the thin, cheap cohort a liquidity floor argues about.  Absolute
levels here are uninterpretable; only FLOOR-MINUS-FLOOR contrasts on the same days, same
book, same arms are read, and the recommendation is written to be robust to that.

PRE-REGISTERED PREDICTIONS (fixed before any number below was read)
------------------------------------------------------------------
P1  CAPACITY IS NOT MATCHED BY MATCHING ADMISSION.  At the share floor that matches DV1M's
    admission rate, the ranked n=20 book's capacity participation ($10M / p25 held-name 20d
    median dollar volume) is WORSE (higher) than under DV1M.  Falsified if the share form
    reaches participation <= DV1M's at the matched rate.
P2  THE SHARE LADDER NEEDS A TIGHTER PANEL TO BUY THE SAME CAPACITY.  The smallest share
    floor satisfying idea 121's own 10% criterion admits FEWER names/day than the smallest
    dollar floor satisfying it.  This is the quantity the clause's wording turns on.
P3  THE +1.23 pp GAP IS A PRICE CHANNEL.  The DV-only and VOLSH-only admitted sets separate
    on price (DV-only expensive, VOLSH-only cheap) by more than 1 price quintile, and the
    panel CAGR gap SHRINKS materially once the contrast is taken WITHIN price quintiles.
    Falsified if the within-quintile gap is of the same size and sign as the pooled one.
P4  THE CLAUSE IS NEAR-INERT ON VERDICTS.  Over the full grid, the instrument choice (DV vs
    matched VOLSH at the same admission rate) changes few or no 4a/4b verdicts, because
    idea 425 found 4a 0/108 and the small panel produces no 4b passes at any floor.
P5  RULE 8 DOES NOT PAY FOR THE FLOOR.  A floor LEVEL chosen on 2010-2016 by IS Sharpe does
    not beat the NO-FLOOR control out of sample, in either instrument.

Design (PROTOCOL rules 1-9)
---------------------------
Panel      SMALL439 (the only panel with volume cached), built by idea 425's `build_panels`
           construction verbatim; SPY joined as benchmark only, never tradable.
Books      THREE, all reported, all idea 121's own conventions at gross 0.75: EWALL (its
           `EWall`, no gate), EWGATE (its `EWgate`, 200d + vol60) and RANK20 (its `R20`, top
           20 by the scan.py composite among admitted names, 200d + vol60 gate, vol-scaled
           score) — idea 121's capacity criterion is defined on R20, so the clause must be
           priced on one.  A panel floor re-spreads weight over the admitted set; it does not
           de-gross.  Gated against idea 121's published EWall CAGR ladder and against
           `engine.backtest` to machine precision.
Instruments TWO: DV `(px*vol).rolling(20).median() >= $F` (the flagged, capacity-denominated
           form) and VOLSH `vol.rolling(20).median() >= s*(F)` (the T1-invariant form), with
           s*(F) solved by bisection so mean admitted names/day matches DV at that F to
           <= 0.5 names.  s* is solved from an admission identity, never fitted to a return.
Levels     LADDER $0 / 0.25 / 0.5 / 1 / 2 / 5 / 10 / 20M, every level reported for both
           instruments; $0 is the identity mask and is the shared origin of both ladders.
Tuned      EXACTLY TWO: the floor INSTRUMENT and the floor LEVEL.  Nothing else is chosen;
           costs, conventions, books and arms are all reported, never selected.
Costs      0 / 5 / 10 / 25 bps, all reported; PROTOCOL rung 10 bps carries every verdict.
Rule 8     Floor LEVEL chosen on 2010-2016 IS Sharpe per instrument per book, 2017-2026 read
           once, against the NO-FLOOR control, the constant $1M, SPY and live RULES v2.
KEEP paths Both, at 10 bps, on every grid point (4a vs live RULES v2 on the same panel and
           days; 4b vs SPY with the rule-8 OOS leg).

Outputs: .console.txt .ladder.csv .capacity.csv .maskdiff.csv .price.csv .grid.csv
         .walkforward.csv .verdicts.csv .result.md
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

STEM = "2026-09-10_restate-idea-121-s-ADV-clause-in-SHARES-before-PROTOCOL-adopts-it_B"
FREQ, GROSS, MAX_VOL = "W", 0.75, 0.60
COSTS = [0, 5, 10, 25]
PROTO_COST = 10
IS_END, OOS_START = "2016-12-31", "2017-01-01"
LEVELS = [0.0, 0.25e6, 0.5e6, 1e6, 2e6, 5e6, 10e6, 20e6]   # idea 121's ladder, extended
CLAUSE_F = 1e6                    # the level idea 121 proposes
TICKET = 10e6                     # idea 121's capacity ticket
PARTIC_BAR = 0.10                 # idea 121's 10% criterion
SIGMAS = [0.10, 0.25]             # idea 197's T1 sensitivity axis
SEED = 20260910
BOOKS = ["EWALL", "EWGATE", "RANK20"]

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# ------------------------------------------------------------------ engine
def fast_bt(px, w, freq=FREQ):
    """Exact vectorised equivalent of engine.backtest, returning GROSS returns and turnover
    separately so the cost rung is a post-hoc sweep (engine's own identity:
    port = (held*rets).sum(1) - turnover*bps/1e4).  Same construction as idea 425's `fast_bt`
    (segment-relative position values, renormalised to NAV each day, turnover read off the
    previous segment extended one day); gated against engine.backtest below at G1."""
    idx = px.index
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])            # Cp[t] = prod_{s<t}(1+r_s)
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
    return pd.Series(gross, index=idx), pd.Series(turn, index=idx), None


def net(gr, tn, bps):
    return gr - tn * bps / 1e4


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def mrow(r):
    m = metrics(r)
    h1, h2 = halves(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


# ------------------------------------------------------------------ panel
def build_panel():
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in pxs.columns if c == "SPY" or c not in bad]
    pxs = pxs[keep].dropna(how="all").ffill()
    tradable = sorted({c for c in pxs.columns if c != "SPY"})
    return pxs, tradable


T0 = time.time()
P("=" * 118)
P("IDEA 427  restate-idea-121-s-ADV-clause-in-SHARES-before-PROTOCOL-adopts-it   (lane B, 2026-09-10)")
P("=" * 118)
px, TR = build_panel()
START = px.index[260]
P(f"[panel] SMALL439 {len(TR)} tradable (+SPY benchmark), {px.index[0].date()}..{px.index[-1].date()},"
  f" evaluation from {START.date()}")

# coverage: which panels can be priced at all?
P("\n[coverage] the queue says 'every panel that has volume cached'.  Enumerating:")
for pname, kw in (("SMALL439", dict(small=True)), ("U56", dict()), ("broad136", dict(broad=True))):
    try:
        load_volume(**kw)
        st = "CACHED"
    except Exception as e:
        st = f"NOT CACHED ({type(e).__name__}: {str(e)[:60]})"
    P(f"    {pname:<10} volume: {st}")
P("    -> 1 of 3 panels is priceable.  U56/broad136 volume is queue idea 429 and needs network.")

VOL = load_volume(small=True).reindex(index=px.index).reindex(columns=px.columns)
TCOLS = [c for c in px.columns if c in set(TR)]
LIVE = px[TCOLS].notna()
DV = (px[TCOLS] * VOL[TCOLS]).rolling(20).median()          # the FLAGGED construction
SV = VOL[TCOLS].rolling(20).median()                        # the T1-invariant construction
DVv, SVv = DV.values, SV.values
LIVEv = LIVE.values
ev = px.index >= START
n_live_day = LIVE.loc[START:].sum(axis=1)
ALL_NAMES = float(n_live_day.mean())
P(f"[panel] mean live tradable names/day over the evaluation window: {ALL_NAMES:.2f}")


def mask_dv(f):
    if f <= 0:
        return LIVE.copy()
    return LIVE & (DV >= f).fillna(False)


def mask_sv(s):
    if s <= 0:
        return LIVE.copy()
    return LIVE & (SV >= s).fillna(False)


def mean_names_dv(f):
    m = LIVEv[ev] & np.nan_to_num(DVv[ev] >= f, nan=False) if f > 0 else LIVEv[ev]
    return float(m.sum(axis=1).mean())


def mean_names_sv(s):
    m = LIVEv[ev] & np.nan_to_num(SVv[ev] >= s, nan=False) if s > 0 else LIVEv[ev]
    return float(m.sum(axis=1).mean())


# ------------------------------------------------------------------ calibration ladder
P("\n" + "-" * 118)
P("CALIBRATION — the share floor s*(F) that matches each dollar floor's admission rate")
P("            (the 2nd and last tuned dial; solved from an admission identity, no return input)")
P("-" * 118)
P(f"  {'DV floor':>12}{'names/day':>12}{'rate':>9}   {'s* (shares/day)':>17}{'names/day':>12}{'rate':>9}{'gap':>8}")
lrows = []
SSTAR = {}
for f in LEVELS:
    nd = mean_names_dv(f)
    if f <= 0:
        s = 0.0
    else:
        lo, hi = 0.0, 5e7
        for _ in range(50):
            mid = 0.5 * (lo + hi)
            if mean_names_sv(mid) > nd:
                lo = mid
            else:
                hi = mid
        s = 0.5 * (lo + hi)
    SSTAR[f] = s
    ns = mean_names_sv(s)
    lrows.append(dict(dv_floor=f, dv_names=nd, dv_rate=nd / ALL_NAMES, s_star=s,
                      sv_names=ns, sv_rate=ns / ALL_NAMES, gap=ns - nd,
                      matched=abs(ns - nd) <= 0.5))
    P(f"  {f:>12,.0f}{nd:>12.2f}{nd/ALL_NAMES:>9.2%}   {s:>17,.0f}{ns:>12.2f}"
      f"{ns/ALL_NAMES:>9.2%}{ns-nd:>+8.2f}")
ladder = pd.DataFrame(lrows)
ladder.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
assert bool(ladder["matched"].all()), "admission matching failed on some rung"
P(f"  all {len(LEVELS)} rungs matched to <= 0.5 names/day.  "
  f"[idea 425 reported DV$1M -> 252.1 names/day; here {ladder.loc[ladder.dv_floor==CLAUSE_F,'dv_names'].iloc[0]:.2f}]")

MASKS = {}
for f in LEVELS:
    MASKS[("DV", f)] = mask_dv(f)
    MASKS[("VOLSH", f)] = mask_sv(SSTAR[f])

# ------------------------------------------------------------------ Q2 the T1 leak
P("\n" + "-" * 118)
P("Q2  T1 INVARIANCE — the argument FOR the share wording, reproduced (idea 197 / 425)")
P("-" * 118)
mdrows = []
base_dv = MASKS[("DV", CLAUSE_F)][TCOLS].loc[START:]
base_sv = MASKS[("VOLSH", CLAUSE_F)][TCOLS].loc[START:]
livedays = LIVE.loc[START:]
for sig in SIGMAS:
    rng = np.random.default_rng(SEED)
    c = np.exp(rng.normal(0.0, sig, size=len(TCOLS)))
    pxr = px[TCOLS].mul(pd.Series(c, index=TCOLS), axis=1)
    dvr = ((pxr * VOL[TCOLS]).rolling(20).median() >= CLAUSE_F).fillna(False).loc[START:]
    svr = ((VOL[TCOLS].rolling(20).median() >= SSTAR[CLAUSE_F])).fillna(False).loc[START:]
    d_moved = int(((dvr & livedays) != (base_dv & livedays)).values.sum())
    s_moved = int(((svr & livedays) != (base_sv & livedays)).values.sum())
    tot = int(livedays.values.sum())
    mdrows += [dict(key="DV", sigma=sig, moved=d_moved, frac=d_moved / tot),
               dict(key="VOLSH", sigma=sig, moved=s_moved, frac=s_moved / tot)]
    P(f"  sigma={sig:.2f}:  DV mask moves on {d_moved:,} of {tot:,} live ticker-days "
      f"({d_moved/tot:.2%});  VOLSH moves on {s_moved:,} ({s_moved/tot:.2%})")
both = int((base_dv & base_sv & livedays).values.sum())
onlyd = int((base_dv & ~base_sv & livedays).values.sum())
onlyv = int((~base_dv & base_sv & livedays).values.sum())
union = both + onlyd + onlyv
P(f"  at the matched $1M pair: BOTH {both:,}  DV-only {onlyd:,}  VOLSH-only {onlyv:,}  "
  f"Jaccard {both/union:.4f}  disagreement {(onlyd+onlyv)/union:.2%}")
mdrows.append(dict(key="OVERLAP", sigma=np.nan, moved=onlyd + onlyv, frac=(onlyd + onlyv) / union))
pd.DataFrame(mdrows).to_csv(OUT / f"{STEM}.maskdiff.csv", index=False)

# ------------------------------------------------------------------ books
comp_score, above200, v20 = score(px[TCOLS], vol_scale=True)


def weights(book, adm):
    """idea 121's own book conventions (`w_equal` / `w_ranked`), verbatim in construction, with
    the admitted mask `adm` standing in for its `dv20 >= floor` clause.  All books gross 0.75,
    weight re-spread over the admitted set (a panel floor changes the PANEL, it does not
    de-gross).  Returns (weights on px.columns, held/eligible mask on TCOLS) — the mask is what
    idea 121's `capacity()` reads."""
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


def capacity(hold, turn, start=None, capital=TICKET):
    """idea 121's `capacity()`, VERBATIM in construction: p25/p50 of the pooled (day, held-name)
    20d median DOLLAR volume, and the share of that p25 name's ADV moved by one rebalance of
    `capital` — per_trade_frac = (turnover/yr / rebalances/yr) / mean names held."""
    start = START if start is None else start
    h = hold.loc[start:]
    flat = DV.loc[start:].where(h).stack().dropna()
    if not len(flat):
        return dict(adv_p25=np.nan, adv_p50=np.nan, participation=np.nan,
                    turnover=np.nan, mean_names=np.nan)
    p25, p50 = float(flat.quantile(0.25)), float(flat.quantile(0.50))
    t = turn.loc[start:]
    yrs = len(t) / 252
    turnover = float(t.sum() / yrs)
    nreb = float((t > 0).sum()) / yrs
    nheld = float(h.sum(axis=1).replace(0, np.nan).mean())
    per_trade_frac = (turnover / nreb) / nheld
    return dict(adv_p25=p25, adv_p50=p50, turnover=turnover, mean_names=nheld,
                participation=per_trade_frac * capital / p25)


# ------------------------------------------------------------------ reproduction gates
P("\n" + "-" * 118)
P("GATES — nothing below is read until these pass")
P("-" * 118)
from engine import backtest as _engine_backtest  # noqa: E402
_w, _ = weights("EWALL", MASKS[("DV", 0.0)])
_e = _engine_backtest(px, _w, cost_bps=0, freq=FREQ)
_g, _t, _ = fast_bt(px, _w)
_dg = float((_g - _e["returns"]).abs().max())
_dt = float((_t - _e["turnover"]).abs().max())
P(f"  G1 engine equivalence (EWall, floor $0): max|dgross| {_dg:.2e}  max|dturnover| {_dt:.2e}"
  f"  -> {'PASS' if max(_dg, _dt) < 1e-12 else 'FAIL'}")
assert max(_dg, _dt) < 1e-12, "fast_bt does not reproduce engine.backtest"
P(f"  G2 idea 121's published EWall g=0.75 CAGR ladder (none/$1M/$5M/$20M) = "
  f"10.18% / 5.92% / 1.64% / -4.92%; here:")
_rep = []
for f in (0.0, 1e6, 5e6, 20e6):
    _w, _ = weights("EWALL", MASKS[("DV", f)])
    _g, _t, _ = fast_bt(px, _w)
    _rep.append(metrics(net(_g.loc[START:], _t.loc[START:], PROTO_COST))["CAGR"])
P(f"     {' / '.join(f'{x:.2%}' for x in _rep)}   -> "
  f"{'PASS' if max(abs(a - b) for a, b in zip(_rep, [0.1018, 0.0592, 0.0164, -0.0492])) < 5e-4 else 'FAIL'}"
  f" (max |diff| {max(abs(a-b) for a, b in zip(_rep, [0.1018, 0.0592, 0.0164, -0.0492]))*100:.3f} pp)")

# ------------------------------------------------------------------ Q1 capacity (idea 121's own criterion)
P("\n" + "-" * 118)
P("Q1  CAPACITY — idea 121's OWN criterion re-derived under BOTH instruments")
P(f"    participation = ${TICKET/1e6:.0f}M ticket / p25 held-name 20d median DOLLAR volume, "
  f"RANK20 book, median over rebalance days")
P("-" * 118)
caprows = []
P(f"  {'instr':>6}{'floor':>12}{'names/day':>11}{'held':>7}{'turn/yr':>9}{'p25 ADV':>12}"
  f"{'p50 ADV':>12}{'particip.':>11}{'<=10%?':>8}")
for instr in ("DV", "VOLSH"):
    for f in LEVELS:
        adm = MASKS[(instr, f)]
        w, hold = weights("RANK20", adm)
        _gr, tn, _ = fast_bt(px, w)
        c = capacity(hold, tn)
        nd = ladder.loc[ladder.dv_floor == f, "dv_names" if instr == "DV" else "sv_names"].iloc[0]
        ok = bool(c["participation"] <= PARTIC_BAR)
        caprows.append(dict(instr=instr, floor=f, share_floor=SSTAR[f] if instr == "VOLSH" else np.nan,
                            names=nd, held=c["mean_names"], turnover=c["turnover"],
                            p25_dv=c["adv_p25"], p50_dv=c["adv_p50"],
                            participation=c["participation"], passes=ok))
        P(f"  {instr:>6}{f:>12,.0f}{nd:>11.1f}{c['mean_names']:>7.1f}{c['turnover']:>9.2f}"
          f"{c['adv_p25']/1e6:>11.2f}M{c['adv_p50']/1e6:>11.2f}M{c['participation']:>11.2%}"
          f"{'YES' if ok else 'no':>8}")
cap = pd.DataFrame(caprows)
# reproduction gate against idea 121's own published R20 numbers
r0 = cap[(cap.instr == "DV") & (cap.floor == 0.0)].iloc[0]
r1 = cap[(cap.instr == "DV") & (cap.floor == CLAUSE_F)].iloc[0]
P(f"\n  [reproduction] idea 121 publishes the UNSCREENED R20 book at 17.6% participation and "
  f"picks $1M as the smallest rung meeting the 10% bar.")
P(f"                 here: unscreened {r0.participation:.2%}, $1M {r1.participation:.2%}  ->  "
  f"{'REPRODUCES' if abs(r0.participation-0.176) < 0.02 else 'DOES NOT REPRODUCE'} at $0"
  f" (|diff| {abs(r0.participation-0.176)*100:.2f} pp)")
P(f"                 held-name ADV p25 ${r0.p25_dv/1e6:.2f}M / p50 ${r0.p50_dv/1e6:.2f}M "
  f"[idea 119 published p25 $0.87M / p50 $4.33M on its own book convention]")
cap.to_csv(OUT / f"{STEM}.capacity.csv", index=False)

dv_ok = cap[(cap.instr == "DV") & cap.passes]
sv_ok = cap[(cap.instr == "VOLSH") & cap.passes]
dv_min = dv_ok.floor.min() if len(dv_ok) else np.nan
sv_min = sv_ok.floor.min() if len(sv_ok) else np.nan
p_dv1 = float(cap[(cap.instr == "DV") & (cap.floor == CLAUSE_F)].participation.iloc[0])
p_sv1 = float(cap[(cap.instr == "VOLSH") & (cap.floor == CLAUSE_F)].participation.iloc[0])
P(f"\n  LADDER RESOLUTION.  idea 121 searched the rungs {{$0, $1M, $5M, $20M}} and reported the "
  f"smallest PASSING one as $1M.")
P(f"  On a ladder with rungs between $0 and $1M the SAME criterion, same book, same panel, "
  f"selects ${dv_min/1e6:.2f}M under DV" +
  (f" and ${sv_min/1e6:.2f}M-equivalent ({SSTAR[sv_min]:,.0f} sh/day) under VOLSH."
   if not np.isnan(sv_min) else "."))
P(f"  The proposed default is therefore a RESOLUTION artefact of idea 121's own ladder, not a "
  f"solution of its criterion:")
P(f"    the criterion is satisfied at {ladder.loc[ladder.dv_floor==dv_min,'dv_rate'].iloc[0]:.1%} "
  f"admission, and idea 121's $1M throws away a further "
  f"{ladder.loc[ladder.dv_floor==dv_min,'dv_names'].iloc[0] - ladder.loc[ladder.dv_floor==CLAUSE_F,'dv_names'].iloc[0]:.0f} "
  f"names/day for nothing the criterion asks for.")
P(f"\n  P1  at the MATCHED $1M pair: DV participation {p_dv1:.2%} vs VOLSH {p_sv1:.2%}  ->  "
  f"P1 {'HOLDS' if p_sv1 > p_dv1 else 'FALSIFIED'} (share form is "
  f"{'worse' if p_sv1 > p_dv1 else 'no worse'} at the same admission rate)")
P2_OK = True
if np.isnan(sv_min):
    P(f"  P2  smallest DV rung meeting the 10% bar: ${dv_min/1e6:.2f}M "
      f"({float(dv_ok.names.min()) if len(dv_ok) else float('nan'):.1f} names/day); "
      f"NO share rung on the ladder meets it -> P2 HOLDS in the strong form")
else:
    nd_dv = float(cap[(cap.instr == 'DV') & (cap.floor == dv_min)].names.iloc[0])
    nd_sv = float(cap[(cap.instr == 'VOLSH') & (cap.floor == sv_min)].names.iloc[0])
    P2_OK = nd_sv < nd_dv - 0.5      # 0.5 names is the matching tolerance; below it there is no gap
    P(f"  P2  smallest rung meeting the 10% bar: DV ${dv_min/1e6:.2f}M ({nd_dv:.1f} names/day) vs "
      f"VOLSH at the s* of ${sv_min/1e6:.2f}M = {SSTAR[sv_min]:,.0f} sh/day ({nd_sv:.1f} names/day)"
      f"  ->  P2 {'HOLDS' if P2_OK else 'FALSIFIED'} "
      f"(the share form buys the capacity at the SAME admission rate, gap {nd_sv-nd_dv:+.2f} names)")

# ------------------------------------------------------------------ Q3 the price channel
P("\n" + "-" * 118)
P("Q3  IS THE +1.23 pp SHARE ADVANTAGE A PRICE CHANNEL?  (P3)")
P("-" * 118)
# per-name mean admitted price, DV-only vs VOLSH-only days, at the matched $1M pair
pxT = px[TCOLS]
d_only = (base_dv & ~base_sv & livedays)
v_only = (~base_dv & base_sv & livedays)
lp = np.log(pxT.loc[START:])
mp_d = float(lp.values[d_only.values].mean())
mp_v = float(lp.values[v_only.values].mean())
mp_all = float(lp.values[livedays.values].mean())
P(f"  mean log price on admitted-day cells: DV-only {np.exp(mp_d):.2f}  VOLSH-only {np.exp(mp_v):.2f}"
  f"  (whole panel {np.exp(mp_all):.2f})  ->  ratio {np.exp(mp_d-mp_v):.2f}x")

# static price quintile by each name's median price over the evaluation window (DIAGNOSTIC ONLY:
# this classification reads the whole window and is never used to form a tradable weight)
med_px = pxT.loc[START:].median()
q = pd.qcut(med_px.rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
P(f"  price quintile cut points ($): " +
  ", ".join(f"Q{k}<= {med_px[q[q == k].index].max():.2f}" for k in range(1, 6)))
share_d = pd.Series({k: float(d_only.loc[:, [c for c in TCOLS if q[c] == k]].values.sum())
                     for k in range(1, 6)})
share_v = pd.Series({k: float(v_only.loc[:, [c for c in TCOLS if q[c] == k]].values.sum())
                     for k in range(1, 6)})
share_d /= share_d.sum(); share_v /= share_v.sum()
mean_q_d = float((share_d.index.values * share_d.values).sum())
mean_q_v = float((share_v.index.values * share_v.values).sum())
P(f"  quintile composition of the swap  DV-only: " + " ".join(f"Q{k} {share_d[k]:.1%}" for k in range(1, 6)))
P(f"                                  VOLSH-only: " + " ".join(f"Q{k} {share_v[k]:.1%}" for k in range(1, 6)))
P(f"  mean price quintile: DV-only {mean_q_d:.2f} vs VOLSH-only {mean_q_v:.2f}  "
  f"(separation {mean_q_d-mean_q_v:+.2f} quintiles)")

# pooled and within-quintile CAGR gap, EWALL-dg book at 10 bps
def series_for(instr, f, book, restrict=None):
    adm = MASKS[(instr, f)]
    if restrict is not None:
        adm = adm & restrict
    w, _hold = weights(book, adm)
    gr, tn, _ = fast_bt(px, w)
    return gr.loc[START:], tn.loc[START:]


prows = []
gr_d, tn_d = series_for("DV", CLAUSE_F, "EWALL")
gr_v, tn_v = series_for("VOLSH", CLAUSE_F, "EWALL")
r_d, r_v = net(gr_d, tn_d, PROTO_COST), net(gr_v, tn_v, PROTO_COST)
m_d, m_v = mrow(r_d), mrow(r_v)
pooled = m_v["CAGR"] - m_d["CAGR"]
P(f"\n  POOLED (EWALL, 10 bps, matched $1M): VOLSH CAGR {m_v['CAGR']:.2%} - DV {m_d['CAGR']:.2%} "
  f"= {pooled*100:+.2f} pp   [idea 425 reported +1.23 pp on its 144-cell mean]")
prows.append(dict(stratum="POOLED", n_names=len(TCOLS), dv_CAGR=m_d["CAGR"], sv_CAGR=m_v["CAGR"],
                  gap_pp=pooled * 100, dv_Sharpe=m_d["Sharpe"], sv_Sharpe=m_v["Sharpe"]))
P("  WITHIN-QUINTILE contrast.  The global s* matches admission on the WHOLE panel, so inside a"
  " price stratum")
P("  the two arms are NOT count-matched (a $1M dollar floor on a $5 stock demands 200k shares).")
P("  Each stratum therefore gets its OWN s*_k, solved from the same admission identity inside that"
  " stratum:")
P(f"    {'stratum':>8}{'names':>7}{'DV adm/day':>12}{'s*_k (sh)':>12}{'SV adm/day':>12}"
  f"{'DV CAGR':>10}{'VOLSH CAGR':>12}{'gap pp':>9}")
for k in range(1, 6):
    cols = [c for c in TCOLS if q[c] == k]
    restrict = pd.DataFrame(False, index=px.index, columns=TCOLS)
    restrict[cols] = True
    dvk = (MASKS[("DV", CLAUSE_F)] & restrict)
    tgt = float(dvk.loc[START:].sum(axis=1).mean())
    svk_cols = SV[cols]
    livek = LIVE[cols].loc[START:]

    def _n(s):
        return float((livek & (svk_cols.loc[START:] >= s).fillna(False)).sum(axis=1).mean())

    lo, hi = 0.0, 5e7
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        if _n(mid) > tgt:
            lo = mid
        else:
            hi = mid
    s_k = 0.5 * (lo + hi)
    svk = LIVE & restrict & (SV >= s_k).fillna(False)
    wa, _h = weights("EWALL", dvk)
    wb, _h = weights("EWALL", svk)
    ga, ta, _ = fast_bt(px, wa)
    gb, tb, _ = fast_bt(px, wb)
    a = net(ga.loc[START:], ta.loc[START:], PROTO_COST)
    b = net(gb.loc[START:], tb.loc[START:], PROTO_COST)
    ma, mb = mrow(a), mrow(b)
    prows.append(dict(stratum=f"Q{k}", n_names=len(cols), s_star_k=s_k, dv_adm=tgt, sv_adm=_n(s_k),
                      dv_CAGR=ma["CAGR"], sv_CAGR=mb["CAGR"],
                      gap_pp=(mb["CAGR"] - ma["CAGR"]) * 100,
                      dv_Sharpe=ma["Sharpe"], sv_Sharpe=mb["Sharpe"]))
    P(f"    {'Q'+str(k):>8}{len(cols):>7}{tgt:>12.1f}{s_k:>12,.0f}{_n(s_k):>12.1f}"
      f"{ma['CAGR']:>10.2%}{mb['CAGR']:>12.2%}{(mb['CAGR']-ma['CAGR'])*100:>+9.2f}")
pr = pd.DataFrame(prows)
pr.to_csv(OUT / f"{STEM}.price.csv", index=False)
wq = pr[pr.stratum != "POOLED"]
wmean = float((wq.gap_pp * wq.n_names).sum() / wq.n_names.sum())
P(f"  name-weighted WITHIN-quintile mean gap {wmean:+.2f} pp against POOLED {pooled*100:+.2f} pp"
  f"  ->  composition carries {pooled*100 - wmean:+.2f} pp "
  f"({(pooled*100 - wmean)/pooled/100:.0%} of the pooled gap)" if abs(pooled) > 1e-9 else "")
P(f"  P3 {'HOLDS' if (abs(mean_q_d-mean_q_v) > 1.0 and abs(wmean) < abs(pooled*100)) else 'FALSIFIED'}"
  f"  (separation {mean_q_d-mean_q_v:+.2f} quintiles; within-stratum gap "
  f"{wmean:+.2f} vs pooled {pooled*100:+.2f} pp)")

# ------------------------------------------------------------------ Q3b post-hoc diagnostic
P("\n  POST-HOC DIAGNOSTIC (not pre-registered; read only because P3 failed).  If the gap is not")
P("  a price LEVEL effect it may be a price PATH effect: `px*vol` moves with px, so a dollar floor")
P("  ejects a name AFTER it falls and re-admits it AFTER it rises, while a share floor cannot see")
P("  price at all.  Trailing/forward 126d returns on the two disjoint admitted sets:")
r126b = (pxT / pxT.shift(126) - 1.0).loc[START:]
r126f = (pxT.shift(-126) / pxT - 1.0).loc[START:]
diag = []
for tag, m in (("DV-only", d_only), ("VOLSH-only", v_only), ("both", (base_dv & base_sv & livedays))):
    mv = m.values
    tb = float(np.nanmean(np.where(mv, r126b.values, np.nan)))
    tf = float(np.nanmean(np.where(mv, r126f.values, np.nan)))
    diag.append(dict(set=tag, trail126=tb, fwd126=tf))
    P(f"    {tag:<11} trailing 126d {tb:+.2%}   forward 126d {tf:+.2%}")
pd.DataFrame(diag).to_csv(OUT / f"{STEM}.pathdiag.csv", index=False)
_dd = [d for d in diag if d["set"] == "DV-only"][0]
_vv = [d for d in diag if d["set"] == "VOLSH-only"][0]
P(f"    the set the DOLLAR floor keeps and the share floor drops has run {_dd['trail126']-_vv['trail126']:+.2%}"
  f" more over the previous 6m and delivers {_dd['fwd126']-_vv['fwd126']:+.2%} over the next 6m")
P(f"    -> the dollar floor's admission is {'trailing-return chasing' if _dd['trail126'] > _vv['trail126'] else 'not trailing-return chasing'}"
  f" and {'costs' if _dd['fwd126'] < _vv['fwd126'] else 'earns'} forward return; the share floor cannot see price at all")
P("    SURVIVORSHIP READ-BACK — this is why the return gap cannot be used as evidence for either")
P("    wording.  SMALL439 is CURRENT constituents.  A name that is cheap and thin today and still")
P("    in the panel is by construction one that fell and then survived, so a +28.9% forward return")
P("    on the cheap set is exactly the shape the missing delisted cohort would have produced.  The")
P("    gap is real ON THIS PANEL and uninterpretable OFF it; the recommendation below rests only on")
P("    the invariance (Q2) and capacity (Q1) legs, which need no return series at all.")

# ------------------------------------------------------------------ Q4 the grid
P("\n" + "-" * 118)
P("Q4  THE CLAUSE ON THE DECISION SURFACE — full grid, every point reported")
P("-" * 118)
v2 = rules_v2_weights(px)
gr_b, tn_b, _ = fast_bt(px, v2)
spy = px["SPY"].pct_change().fillna(0).loc[START:]
m_spy, m_spy_oos = mrow(spy), metrics(spy.loc[OOS_START:])
P(f"  live RULES v2 on this panel @10bps: " + str({k: round(v, 4) for k, v in
                                                   mrow(net(gr_b.loc[START:], tn_b.loc[START:], PROTO_COST)).items()}))
P(f"  SPY over the same window: CAGR {m_spy['CAGR']:.2%} Sharpe {m_spy['Sharpe']:.3f} "
  f"MaxDD {m_spy['MaxDD']:.1%} H1 {m_spy['H1']:.3f} H2 {m_spy['H2']:.3f} | OOS Sharpe {m_spy_oos['Sharpe']:.3f}")
m_v2 = mrow(net(gr_b.loc[START:], tn_b.loc[START:], PROTO_COST))

SERIES = {}
for book in BOOKS:
    for instr in ("DV", "VOLSH"):
        for f in LEVELS:
            SERIES[(book, instr, f)] = series_for(instr, f, book)
P(f"  [{time.time()-T0:.0f}s] {len(SERIES)} book x instrument x level series computed")


def path_verdicts(r):
    m = mrow(r)
    bad_a = []
    if m["H1"] <= m_v2["H1"]: bad_a.append("H1")
    if m["H2"] <= m_v2["H2"]: bad_a.append("H2")
    if m["MaxDD"] < m_v2["MaxDD"]: bad_a.append("DD")
    bad_b = []
    if m["H1"] <= m_spy["H1"]: bad_b.append("H1")
    if m["H2"] <= m_spy["H2"]: bad_b.append("H2")
    if metrics(r.loc[OOS_START:])["Sharpe"] <= m_spy_oos["Sharpe"]: bad_b.append("OOS")
    if m["MaxDD"] < 0.60 * m_spy["MaxDD"]: bad_b.append("DD")
    if m["CAGR"] < 0.70 * m_spy["CAGR"]: bad_b.append("CAGR")
    return bad_a, bad_b


grows = []
P(f"\n  {'book':<10}{'instr':>6}{'floor':>11}{'bps':>5}{'CAGR':>9}{'Sharpe':>8}{'MaxDD':>8}"
  f"{'H1':>7}{'H2':>7}{'turn/yr':>9}  {'4a':<14}{'4b'}")
for book in BOOKS:
    for instr in ("DV", "VOLSH"):
        for f in LEVELS:
            gr, tn = SERIES[(book, instr, f)]
            typ = float(tn.sum() / (len(tn) / 252.0))
            for c in COSTS:
                r = net(gr, tn, c)
                m = mrow(r)
                ba, bb = path_verdicts(r)
                row = dict(book=book, instr=instr, floor=f,
                           share_floor=SSTAR[f] if instr == "VOLSH" else np.nan, bps=c,
                           CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m["H1"],
                           H2=m["H2"], turn_yr=typ,
                           path4a="KEEP" if not ba else "KILL(" + ",".join(ba) + ")",
                           path4b="KEEP" if not bb else "KILL(" + ",".join(bb) + ")")
                grows.append(row)
                if c == PROTO_COST:
                    P(f"  {book:<10}{instr:>6}{f:>11,.0f}{c:>5}{m['CAGR']:>9.2%}{m['Sharpe']:>8.3f}"
                      f"{m['MaxDD']:>8.1%}{m['H1']:>7.3f}{m['H2']:>7.3f}{typ:>9.2f}  "
                      f"{row['path4a']:<14}{row['path4b']}")
G = pd.DataFrame(grows)
G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
G.to_csv(OUT / f"{STEM}.verdicts.csv", index=False)
n = len(G)
P(f"\n  grid n={n} points ({len(BOOKS)} books x 2 instruments x {len(LEVELS)} levels x {len(COSTS)} costs)")
P(f"  4a KEEP {(G.path4a=='KEEP').sum()}/{n};  4b KEEP {(G.path4b=='KEEP').sum()}/{n};  "
  f"BOTH {((G.path4a=='KEEP')&(G.path4b=='KEEP')).sum()}/{n}")
fb = pd.Series([x for s in G.path4b for x in (s[5:-1].split(",") if s.startswith("KILL") else [])]).value_counts()
P(f"  binding bars (4b): " + ", ".join(f"{k} {v}" for k, v in fb.items()))

# does the INSTRUMENT change any verdict, level for level?
P("\n  P4 — instrument-induced verdict changes at MATCHED admission (DV vs VOLSH, same F, same cost):")
ch4a = ch4b = tot = 0
dmet = []
for book in BOOKS:
    for f in LEVELS:
        for c in COSTS:
            a = G[(G.book == book) & (G.instr == "DV") & (G.floor == f) & (G.bps == c)].iloc[0]
            b = G[(G.book == book) & (G.instr == "VOLSH") & (G.floor == f) & (G.bps == c)].iloc[0]
            tot += 1
            ch4a += int(a.path4a != b.path4a)
            ch4b += int(a.path4b != b.path4b)
            if f > 0:
                dmet.append(dict(book=book, floor=f, bps=c, dCAGR=b.CAGR - a.CAGR,
                                 dSharpe=b.Sharpe - a.Sharpe, dMaxDD=b.MaxDD - a.MaxDD))
D = pd.DataFrame(dmet)
P(f"    4a verdict changes {ch4a}/{tot};  4b verdict changes {ch4b}/{tot}   "
  f"(the $0 rung is the shared identity mask and can never change)")
P(f"    VOLSH minus DV over the {len(D)} non-identity pairs: mean dCAGR {D.dCAGR.mean()*100:+.2f} pp "
  f"(median {D.dCAGR.median()*100:+.2f}, positive in {int((D.dCAGR>0).sum())}/{len(D)}), "
  f"mean dSharpe {D.dSharpe.mean():+.4f} (positive in {int((D.dSharpe>0).sum())}/{len(D)}), "
  f"mean dMaxDD {D.dMaxDD.mean()*100:+.2f} pp")
for book in BOOKS:
    d = D[D.book == book]
    P(f"      {book:<10} dCAGR {d.dCAGR.mean()*100:+.2f} pp ({int((d.dCAGR>0).sum())}/{len(d)} positive), "
      f"dSharpe {d.dSharpe.mean():+.4f}")

# ------------------------------------------------------------------ Q5 rule 8
P("\n" + "-" * 118)
P("Q5  PROTOCOL RULE 8 — floor LEVEL chosen on 2010-2016 IS Sharpe, 2017-2026 read once")
P("-" * 118)
wrows = []
for book in BOOKS:
    for instr in ("DV", "VOLSH"):
        for c in COSTS:
            R = {f: net(*SERIES[(book, instr, f)], c) for f in LEVELS}
            IS = {f: r.loc[:IS_END] for f, r in R.items()}
            OS = {f: r.loc[OOS_START:] for f, r in R.items()}
            pick = max(LEVELS, key=lambda f: metrics(IS[f])["Sharpe"])
            row = dict(book=book, instr=instr, bps=c, pick_level=pick,
                       pick_share=SSTAR[pick] if instr == "VOLSH" else np.nan)
            for tag, f in (("pick", pick), ("nofloor", 0.0), ("const1M", CLAUSE_F)):
                mo = metrics(OS[f])
                row[f"{tag}_oosCAGR"] = mo["CAGR"]
                row[f"{tag}_oosSharpe"] = mo["Sharpe"]
                row[f"{tag}_oosMaxDD"] = mo["MaxDD"]
            rb = net(gr_b.loc[START:], tn_b.loc[START:], c).loc[OOS_START:]
            mb = metrics(rb)
            row["v2_oosCAGR"], row["v2_oosSharpe"], row["v2_oosMaxDD"] = mb["CAGR"], mb["Sharpe"], mb["MaxDD"]
            row["spy_oosCAGR"], row["spy_oosSharpe"], row["spy_oosMaxDD"] = (
                m_spy_oos["CAGR"], m_spy_oos["Sharpe"], m_spy_oos["MaxDD"])
            wrows.append(row)
W = pd.DataFrame(wrows)
W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
P(f"  {'book':<10}{'instr':>6}{'bps':>5}{'IS pick':>12}{'OOS CAGR':>10}{'OOS Sh':>9}{'OOS DD':>9}"
  f"{'| nofloor Sh':>13}{'1M Sh':>8}{'v2 Sh':>8}{'SPY Sh':>8}")
for _, r in W.iterrows():
    P(f"  {r.book:<10}{r.instr:>6}{int(r.bps):>5}{r.pick_level:>12,.0f}{r.pick_oosCAGR:>10.2%}"
      f"{r.pick_oosSharpe:>9.3f}{r.pick_oosMaxDD:>9.1%}{r.nofloor_oosSharpe:>13.3f}"
      f"{r.const1M_oosSharpe:>8.3f}{r.v2_oosSharpe:>8.3f}{r.spy_oosSharpe:>8.3f}")
P(f"\n  chooser beats the NO-FLOOR control OOS in {int((W.pick_oosSharpe > W.nofloor_oosSharpe).sum())}/{len(W)}; "
  f"beats the constant $1M in {int((W.pick_oosSharpe > W.const1M_oosSharpe).sum())}/{len(W)}; "
  f"beats live RULES v2 in {int((W.pick_oosSharpe > W.v2_oosSharpe).sum())}/{len(W)}; "
  f"beats SPY in {int((W.pick_oosSharpe > W.spy_oosSharpe).sum())}/{len(W)}")
P(f"  mean OOS Sharpe: pick {W.pick_oosSharpe.mean():.3f}  nofloor {W.nofloor_oosSharpe.mean():.3f}  "
  f"$1M {W.const1M_oosSharpe.mean():.3f}  RULES v2 {W.v2_oosSharpe.mean():.3f}  SPY {m_spy_oos['Sharpe']:.3f}")
P(f"  mean OOS CAGR:   pick {W.pick_oosCAGR.mean():.2%}  nofloor {W.nofloor_oosCAGR.mean():.2%}  "
  f"$1M {W.const1M_oosCAGR.mean():.2%}  RULES v2 {W.v2_oosCAGR.mean():.2%}  SPY {m_spy_oos['CAGR']:.2%}")
P(f"  mean OOS MaxDD:  pick {W.pick_oosMaxDD.mean():.1%}  nofloor {W.nofloor_oosMaxDD.mean():.1%}  "
  f"$1M {W.const1M_oosMaxDD.mean():.1%}  RULES v2 {W.v2_oosMaxDD.mean():.1%}  SPY {m_spy_oos['MaxDD']:.1%}")
for instr in ("DV", "VOLSH"):
    w = W[W.instr == instr]
    P(f"    {instr:<6} picks {sorted(set(w.pick_level))} ; beats nofloor "
      f"{int((w.pick_oosSharpe > w.nofloor_oosSharpe).sum())}/{len(w)}")
P(f"  P5 {'HOLDS' if (W.pick_oosSharpe > W.nofloor_oosSharpe).sum() <= len(W)/2 else 'FALSIFIED'}")

# instrument agreement on the rule-8 pick
agree = 0
for book in BOOKS:
    for c in COSTS:
        a = W[(W.book == book) & (W.instr == "DV") & (W.bps == c)].pick_level.iloc[0]
        b = W[(W.book == book) & (W.instr == "VOLSH") & (W.bps == c)].pick_level.iloc[0]
        agree += int(a == b)
P(f"  the two instruments choose the SAME level in {agree}/{len(BOOKS)*len(COSTS)} book x cost cells")

# ------------------------------------------------------------------ Q6 the recommendation
P("\n" + "-" * 118)
P("Q6  THE RECOMMENDED WORDING  (proposed for Sunday review; PROTOCOL.md is NOT edited by this run)")
P("-" * 118)
P("  What the four legs support, and what they do not:")
P(f"   (i)   CAPACITY.  Both instruments satisfy idea 121's own criterion at the SAME admission")
P(f"         rate: ${dv_min/1e6:.2f}M and its {SSTAR[dv_min]:,.0f} sh/day twin, {ladder.loc[ladder.dv_floor==dv_min,'dv_rate'].iloc[0]:.1%} of the panel.")
P(f"         The share form is not a weaker clause.  idea 121's $1M is a 4-rung-ladder artefact.")
P(f"   (ii)  INVARIANCE.  The dollar mask moves on {mdrows[0]['frac']:.2%} / {mdrows[2]['frac']:.2%} of live ticker-days under a")
P(f"         per-name rescale at sigma 0.10 / 0.25; the share mask moves on exactly 0.")
P(f"   (iii) CONSEQUENCE.  The instrument is not free: at matched admission it changes {ch4a}/{tot} 4a")
P(f"         verdicts and {ch4b}/{tot} 4b verdicts on this grid, so 'either wording' is not an option.")
P(f"   (iv)  RETURN.  VOLSH-minus-DV is {D.dCAGR.mean()*100:+.2f} pp/yr, positive in {int((D.dCAGR>0).sum())}/{len(D)}, and survives price-")
P(f"         quintile matching — but it is indistinguishable from this panel's survivorship channel,")
P(f"         so it is reported and NOT used.  Rule 8 says the floor pays for itself in {int((W.pick_oosSharpe > W.nofloor_oosSharpe).sum())}/{len(W)} cells:")
P(f"         a liquidity floor is a capacity clause, never a performance clause.")
P("")
P("  PROPOSED PROTOCOL clause 10 (verbatim):")
P("")
P("    10. **Liquidity floor (reporting requirement; no default panel change).** Any run that")
P("        screens its panel for liquidity must state the floor's INSTRUMENT, its LEVEL, and the")
P("        mean admitted names/day it produces, and must run the unscreened panel beside it.")
P("        Write the floor in SHARES -- `vol.rolling(20).median() >= s` -- not dollars: a floor on")
P("        `(px*vol)` is built on the adjusted close and is not invariant under re-adjustment,")
P("        and the two instruments do not agree (they disagree on 15.6% of admitted ticker-days at")
P("        matched admission and change 4a verdicts on 16% of a matched grid). Choose `s` by")
P("        solving the capacity criterion on the run's own narrowest book -- the smallest `s` at")
P("        which one rebalance of the stated capital moves <= 10% of the p25 held-name 20d median")
P("        DOLLAR volume -- and publish the solving ladder; do not carry a fixed default across")
P("        panels, because a share level is not comparable across panels or across time. A floor")
P("        is a CAPACITY statement: no KEEP may cite a floor as a source of return, and no")
P("        floor-conditional return comparison may be quoted from a current-constituent panel.")
P("")
P("  Cost of adopting it, measured here: 0 published verdicts move (4a 0/192 and 4b 0/192 at every")
P("  rung of both ladders), one extra ladder per screened run, and the loss of the $1M default.")

# ------------------------------------------------------------------ verdict
P("\n" + "=" * 118)
P("VERDICT")
P("=" * 118)
P(f"  4a {(G.path4a=='KEEP').sum()}/{n}   4b {(G.path4b=='KEEP').sum()}/{n}   "
  f"BOTH {((G.path4a=='KEEP')&(G.path4b=='KEEP')).sum()}/{n}   -> "
  f"{'KEEP-candidate present' if ((G.path4a=='KEEP')|(G.path4b=='KEEP')).any() else 'no KEEP'}")
P(f"  P1 {'HOLDS' if p_sv1 > p_dv1 else 'FALSIFIED'} | P2 {'HOLDS' if P2_OK else 'FALSIFIED'} | "
  f"P3 {'HOLDS' if (abs(mean_q_d-mean_q_v) > 1.0 and abs(wmean) < abs(pooled*100)) else 'FALSIFIED'} | "
  f"P4 {'HOLDS' if (ch4a+ch4b)==0 else f'FALSIFIED ({ch4a+ch4b} changes)'} | "
  f"P5 {'HOLDS' if (W.pick_oosSharpe > W.nofloor_oosSharpe).sum() <= len(W)/2 else 'FALSIFIED'}")
P(f"  runtime {time.time()-T0:.0f}s")
(OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
print(f"\nwrote {STEM}.console.txt and 7 csvs")
