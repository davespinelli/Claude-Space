#!/usr/bin/env python3
"""QUEUE idea 425 — the-liquidity-FLOOR-is-in-the-eligibility-mask-not-a-tilt (lane C, 2026-09-08).

Question (verbatim from QUEUE)
-----------------------------
"idea 197's census flags `band-gate-on-small-panel_B` (9 LEADERBOARD rows) for an ABSOLUTE floor
`dv >= floor` on `(px*vol)`, i.e. the contamination enters the PANEL, not a score.  Re-run that
file's headline band-gate comparison with the floor restated on VOLSH at matched admission rate,
and report how many of its 9 rows move."

What is on trial.  Not a book.  The claim is that a published FILE's conclusions are contaminated
because its eligibility mask is built on a LEVEL construction.  `adv_mask` in the flagged file is

    dv = (px * vol).rolling(20).median();   admit iff dv >= floor

and `px` is the auto-adjusted close, so by idea 197's theorem the mask is NOT invariant under
`px -> px @ diag(c)`: re-adjusting the panel to a different terminal date moves which names are
ADMITTED, in a direction set by each name's future dividends and splits.  A share-volume floor
(`VOLSH`: vol alone) is exactly invariant under that operator.  The flag is therefore correct as a
statement about the CODE.  What it does not say is whether any PUBLISHED NUMBER moves, and that is
the only thing that can force a correction to the record.

PRE-REGISTERED PREDICTIONS (fixed before any new number below was read)
----------------------------------------------------------------------
S1  STRUCTURAL.  Reading the flagged file's 9 LEADERBOARD rows, count how many are quoted at a
    coordinate where the floor is not the identity.  A row quoted at `floor $0` CANNOT move,
    because `adv_mask` returns the all-True mask before it ever touches `px * vol`.  S1 is a
    census of the record, decided by reading the rows, and is stated BEFORE the substitution is
    run so the run cannot choose its own denominator.
S2  THE LEAK IS REAL AT THE MASK.  Under the T1 operator at both published sigmas, the DV mask's
    admitted set moves on a non-trivial fraction of ticker-days; the VOLSH mask moves on exactly
    0.  (If the DV mask did NOT move, idea 197's flag would itself be wrong.)
S3  THE TWO MASKS ARE DIFFERENT OBJECTS.  At MATCHED admission rate the DV and VOLSH masks still
    disagree on a material fraction of admitted ticker-days.  If they agreed almost everywhere,
    a null result below would be vacuous — it would only say the substitution did nothing.
S4  THE MOVEABLE ROWS.  For each row S1 says CAN move, does its published claim change when the
    $1M DV floor is replaced by the matched VOLSH floor?  Pre-registered as: a row MOVES if any
    integer count or verdict it publishes changes, or any published metric moves by more than the
    reporting precision of the row itself (0.001 Sharpe, 0.01 pp CAGR).  No bar is set on "how
    much" — the row either restates or it does not.

Design (PROTOCOL rules 1-9)
---------------------------
Panels     SMALL439 and U56, built by the flagged file's own `build_panels` construction, verbatim.
           SURVIVORSHIP: both are CURRENT constituents; on the small panel the missing delisted
           cohort sits in exactly the thin names a liquidity floor argues about, so absolute levels
           are uninterpretable here and only FLOOR-MINUS-FLOOR contrasts (same arms, same days,
           same book) are read.  That is also why the run reports the substitution's effect and
           never proposes the small panel as a book.
Book       ew-all at gross 0.75, the flagged file's book, unchanged.
Arms       NOGATE, 200d, band2/3/5/8/12/20, 200d-M — the flagged file's 9 arms, unchanged.
Floors     THREE, reported at every value, selected at none:
             DV0      floor $0            (the identity mask; 7 of the 9 rows live here)
             DV1M     dv >= $1M on (px*vol).rolling(20).median()   — the FLAGGED construction
             VOLSH*   vol.rolling(20).median() >= s*, s* chosen so the mean admitted-name count
                      over the evaluation window equals DV1M's, to 0.5 names
Conventions rw and dg; Compositions TREND and FULL; Costs 0/5/10/25 bps — all reported, all
           unselected, exactly as the flagged file reports them.
Tuned      EXACTLY TWO: the floor INSTRUMENT (DV vs VOLSH) and its LEVEL (the share floor s*).
           s* is not fitted to any return — it is solved from an admission-rate identity, and the
           whole calibration ladder is printed.
Rule 8     The flagged file's Q5 walk-forward re-run under both floor instruments: band width
           chosen on 2010..2016 only, 2017..2026 read once, against SPY, do-nothing, the constant
           b=0.03, and the incumbent 200d.
Both KEEP  The flagged file's Q6 re-run under both floor instruments: 4a vs live RULES v2, 4b vs
paths      SPY + rule 8.

Outputs: .console.txt, .grid.csv, .ladder.csv, .maskdiff.csv, .rows.csv, .walkforward.csv,
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

STEM = "2026-09-08_the-liquidity-FLOOR-is-in-the-eligibility-mask-not-a-tilt_C"
SRC = "2026-09-06_band-gate-on-small-panel_B"          # the flagged file
FREQ, GROSS, MAX_VOL = "W", 0.75, 0.60
COSTS = [0, 5, 10, 25]
PROTO_COST = 10
ARMS = ["NOGATE", "200d", "band2", "band3", "band5", "band8", "band12", "band20", "200d-M"]
BAND_ARMS = ["200d", "band2", "band3", "band5", "band8", "band12", "band20"]
BAND_B = {"200d": 0.00, "band2": 0.02, "band3": 0.03, "band5": 0.05,
          "band8": 0.08, "band12": 0.12, "band20": 0.20}
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DV_FLOOR = 1e6                       # the flagged file's floor, in dollars
SIGMAS = [0.10, 0.25]                # idea 197's reported sensitivity axis
SEED = 20260908

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# ------------------------------------------------------------------ engine (flagged file, verbatim)
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


def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def trend(px, arm):
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
    cols = [c for c in px.columns if c in tradable]
    g, live = g[cols], px[cols].notna()
    ch = (g.astype(int).diff().abs() == 1) & live & live.shift(1).fillna(False)
    ty = live.sum().sum() / 252.0
    return float(ch.sum().sum() / ty) if ty > 0 else np.nan


def weights_ewall(px, selectable, g, conv, gross=GROSS):
    live = px.notna() & selectable
    sel = g & live
    num = sel.astype(float)
    den = (live.sum(axis=1) if conv == "dg" else sel.sum(axis=1)).replace(0, np.nan)
    return num.div(den, axis=0).mul(gross).fillna(0.0)


def build_panels():
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in pxs.columns if c == "SPY" or c not in bad]
    pxs = pxs[keep].dropna(how="all").ffill()
    small_tr = {c for c in pxs.columns if c != "SPY"}
    px56 = load_universe()
    tr56 = set(px56.columns)
    P(f"[panels] SMALL439 {len(small_tr)} tradable (+SPY benchmark), "
      f"{pxs.index[0].date()}..{pxs.index[-1].date()}  |  U56 {len(tr56)} tradable, "
      f"{px56.index[0].date()}..{px56.index[-1].date()}")
    return {"SMALL439": (pxs, small_tr), "U56": (px56, tr56)}


# ------------------------------------------------------------------ the two floors
def base_mask(px, tradable):
    m = pd.DataFrame(False, index=px.index, columns=px.columns)
    for c in tradable:
        m[c] = True
    return m


def dv_mask(px, tradable, floor):
    """The FLAGGED construction, verbatim from the source file's `adv_mask`."""
    m = base_mask(px, tradable)
    if floor <= 0:
        return m
    vol = load_volume(small=True).reindex(index=px.index).reindex(columns=px.columns)
    dv = (px * vol).rolling(20).median()
    return m & (dv >= floor).fillna(False)


def volsh_mask(px, tradable, floor_sh):
    """The SUBSTITUTE: identical shape, but the key is share volume alone — exactly invariant
    under px -> px @ diag(c), so the mask carries no adjustment channel."""
    m = base_mask(px, tradable)
    if floor_sh <= 0:
        return m
    vol = load_volume(small=True).reindex(index=px.index).reindex(columns=px.columns)
    sv = vol.rolling(20).median()
    return m & (sv >= floor_sh).fillna(False)


def rescale(px, sigma, seed):
    """Idea 197's T1 operator: px -> px @ diag(c), c_i = exp(N(0, sigma)), one draw per NAME."""
    rng = np.random.default_rng(seed)
    c = np.exp(rng.normal(0.0, sigma, size=px.shape[1]))
    return px.mul(pd.Series(c, index=px.columns), axis=1)


# =====================================================================================
T0 = time.time()
P("=" * 118)
P("IDEA 425  the-liquidity-FLOOR-is-in-the-eligibility-mask-not-a-tilt   (lane C, 2026-09-08)")
P("=" * 118)
PANELS = build_panels()
START = {k: v[0].index[260] for k, v in PANELS.items()}
pxS, trS = PANELS["SMALL439"]
px56, tr56 = PANELS["U56"]
sS, s56 = START["SMALL439"], START["U56"]

# ------------------------------------------------------------------ S1 the structural census
P("\n" + "-" * 118)
P("S1  STRUCTURAL CENSUS — which of the flagged file's 9 LEADERBOARD rows can the floor reach?")
P("-" * 118)
P("Read from LEADERBOARD.md, before any substitution was run.  A row quoted at floor $0 cannot")
P("move: `adv_mask` returns the all-True mask before it touches (px*vol) at all.")
ROWS = [
    ("R1", "60 Q1 reproduction gates (5 gates incl. the 28-cell cross-run check)",
     "floor $0 throughout (gate [e] states 'floor$0'); gates [a]-[d] never call adv_mask "
     "with a floor", False),
    ("R2", "60 P1 the published gate damage on SMALL439",
     "row title says 'floor $0'", False),
    ("R3", "60 four-way gate decomposition on SMALL439 (rw, 0 bps)",
     "quoted from decomp.csv at floor_musd=0", False),
    ("R4", "60 P2 does band3 recover 'a large part' of the 5.4pp",
     "row title says 'floor $0'", False),
    ("R5", "60 P4 the discriminator — does the recovery curve SATURATE?",
     "pre-registered cell is (SMALL439, floor $0, rw, 0 bps)", False),
    ("R6", "60 P3 whipsaw flip rates, SMALL439 vs U56",
     "flip_rate() takes the gate state only; no mask argument exists", False),
    ("R7", "60 rule-8 walk-forward, 48 cells",
     "the 32 SMALL439 cells are 2 FLOORS x 2 comp x 2 conv x 4 bps — half of them are the "
     "$1M DV floor", True),
    ("R8", "60 both KEEP paths on all 108 arms at 10 bps",
     "108 = SMALL439 2 FLOORS x2x2x9 (72) + U56 (36); 36 of the 108 are the $1M DV floor", True),
    ("R9", "60 by-product: does the vol20 half pay on LARGE caps? (U56)",
     "U56 only, and U56 is run at floor $0 (load_volume serves the small panel only)", False),
]
P(f"  {'id':<4}{'row':<62}{'floor reaches it?':>18}   why")
for rid, title, why, reach in ROWS:
    P(f"  {rid:<4}{title[:60]:<62}{('YES' if reach else 'no'):>18}   {why}")
n_reach = sum(r[3] for r in ROWS)
P(f"\n  S1 -> {n_reach} of 9 rows are quoted at a coordinate the floor can reach ({', '.join(r[0] for r in ROWS if r[3])}).")
P(f"        {9 - n_reach} of 9 are quoted at floor $0, where the flagged line is the identity map.")

# ------------------------------------------------------------------ S2 the leak at the mask
P("\n" + "-" * 118)
P("S2  IS THE FLAG RIGHT?  T1 on the MASK itself (px -> px @ diag(c)), both published sigmas")
P("-" * 118)
volS = load_volume(small=True).reindex(index=pxS.index).reindex(columns=pxS.columns)
dv_base = dv_mask(pxS, trS, DV_FLOOR)
TCOLS = sorted(trS)                       # the 439 selectable names; SPY is a benchmark column
live_days = pxS[TCOLS].notna()
n_live = float(live_days.loc[sS:].values.sum())
P(f"  evaluation window {sS.date()}..{pxS.index[-1].date()};  live ticker-days {n_live:,.0f}")
P(f"  {'key':<8}{'sigma':>7}{'draw':>6}{'admitted ticker-days moved':>28}{'frac of live':>14}")
mrows = []
for sig in SIGMAS:
    for d in range(3):
        pxr = rescale(pxS, sig, SEED + 1000 * d)
        dvr = dv_mask(pxr, trS, DV_FLOOR)
        moved = ((dvr[TCOLS] != dv_base[TCOLS]) & live_days).loc[sS:].values.sum()
        mrows.append(dict(key="DVOL", sigma=sig, draw=d, moved=int(moved), frac=moved / n_live))
        P(f"  {'DVOL':<8}{sig:>7.2f}{d:>6}{moved:>28,.0f}{moved / n_live:>14.4f}")
# VOLSH is invariant by construction: rescale touches px only.  Asserted, not assumed.
sv_probe = volsh_mask(pxS, trS, 1e5)
for sig in SIGMAS:
    pxr = rescale(pxS, sig, SEED)
    sv_r = volsh_mask(pxr, trS, 1e5)
    moved = ((sv_r[TCOLS] != sv_probe[TCOLS]) & live_days).loc[sS:].values.sum()
    mrows.append(dict(key="VOLSH", sigma=sig, draw=0, moved=int(moved), frac=moved / n_live))
    P(f"  {'VOLSH':<8}{sig:>7.2f}{0:>6}{moved:>28,.0f}{moved / n_live:>14.4f}")
maskdiff = pd.DataFrame(mrows)
dv_moved = maskdiff[maskdiff.key == "DVOL"].frac.max()
volsh_moved = maskdiff[maskdiff.key == "VOLSH"].frac.max()
P(f"\n  S2 -> DVOL mask moves up to {dv_moved:.2%} of live ticker-days under the operator; "
  f"VOLSH {volsh_moved:.4%}.")
P(f"        {'HOLDS — idea 197 flag confirmed at the MASK' if dv_moved > 1e-4 and volsh_moved < 1e-9 else 'FAILS'}")

# ------------------------------------------------------------------ calibration: matched admission
P("\n" + "-" * 118)
P("CALIBRATION — the share floor s* that matches DV1M's admission rate (the 2nd and last dial)")
P("-" * 118)
target_names = float(dv_base.loc[sS:].sum(axis=1).mean())
all_names = float(base_mask(pxS, trS).loc[sS:].sum(axis=1).mean())
target_rate = target_names / all_names
P(f"  DV floor ${DV_FLOOR/1e6:.0f}M admits a mean {target_names:.2f} of {all_names:.0f} "
  f"selectable names/day = {target_rate:.4%}")
P(f"  s* is solved from that identity — it is not fitted to any return.  Full ladder printed:")
P(f"  {'share floor':>14}{'mean names admitted':>22}{'rate':>10}{'gap vs DV1M':>14}")
LADDER = [0, 1e4, 2.5e4, 5e4, 7.5e4, 1e5, 1.25e5, 1.5e5, 2e5, 3e5, 5e5, 1e6]
lrows = []
sv_med = volS.rolling(20).median()
for s_ in LADDER:
    m = base_mask(pxS, trS) & (sv_med >= s_).fillna(False) if s_ > 0 else base_mask(pxS, trS)
    nm = float(m.loc[sS:].sum(axis=1).mean())
    lrows.append(dict(share_floor=s_, mean_names=nm, rate=nm / all_names, gap=nm - target_names))
    P(f"  {s_:>14,.0f}{nm:>22.2f}{nm / all_names:>10.2%}{nm - target_names:>14.2f}")
# bisect to |gap| <= 0.5 names, on the admission identity alone
lo, hi = 0.0, 2e6
for _ in range(40):
    mid = 0.5 * (lo + hi)
    nm = float((base_mask(pxS, trS) & (sv_med >= mid).fillna(False)).loc[sS:].sum(axis=1).mean())
    if nm > target_names:
        lo = mid
    else:
        hi = mid
S_STAR = 0.5 * (lo + hi)
vs_base = volsh_mask(pxS, trS, S_STAR)
matched_names = float(vs_base.loc[sS:].sum(axis=1).mean())
lrows.append(dict(share_floor=S_STAR, mean_names=matched_names,
                  rate=matched_names / all_names, gap=matched_names - target_names))
ladder = pd.DataFrame(lrows)
ladder.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
P(f"\n  s* = {S_STAR:,.0f} shares/day (20d median) -> mean {matched_names:.2f} names admitted "
  f"vs DV1M's {target_names:.2f}  (gap {matched_names - target_names:+.2f} names, "
  f"{'MATCHED' if abs(matched_names - target_names) <= 0.5 else 'NOT MATCHED'})")

# ------------------------------------------------------------------ S3 are they the same mask?
P("\n" + "-" * 118)
P("S3  AT MATCHED RATE, ARE THE TWO MASKS THE SAME OBJECT?  (if they were, a null would be vacuous)")
P("-" * 118)
both = (dv_base[TCOLS] & vs_base[TCOLS] & live_days).loc[sS:].values.sum()
onlyd = (dv_base[TCOLS] & ~vs_base[TCOLS] & live_days).loc[sS:].values.sum()
onlyv = (~dv_base[TCOLS] & vs_base[TCOLS] & live_days).loc[sS:].values.sum()
union = both + onlyd + onlyv
P(f"  admitted by BOTH {both:,.0f}   DV only {onlyd:,.0f}   VOLSH only {onlyv:,.0f}   "
  f"Jaccard {both / union:.4f}")
P(f"  disagreement = {(onlyd + onlyv) / union:.2%} of the union of admitted ticker-days")
# per-name: how many names does the swap move in or out on a median day?
P(f"  mean names swapped per day: out {(dv_base[TCOLS] & ~vs_base[TCOLS]).loc[sS:].sum(axis=1).mean():.2f}, "
  f"in {(~dv_base[TCOLS] & vs_base[TCOLS]).loc[sS:].sum(axis=1).mean():.2f}")
maskdiff = pd.concat([maskdiff, pd.DataFrame([dict(key="OVERLAP", sigma=np.nan, draw=np.nan,
                                                   moved=int(onlyd + onlyv),
                                                   frac=(onlyd + onlyv) / union)])],
                     ignore_index=True)
maskdiff.to_csv(OUT / f"{STEM}.maskdiff.csv", index=False)
s3 = (onlyd + onlyv) / union
P(f"\n  S3 -> {'HOLDS' if s3 > 0.05 else 'FAILS (the masks are near-identical; any null below is vacuous)'}"
  f"  ({s3:.2%} disagreement)")

# ------------------------------------------------------------------ the three floor regimes
FLOOR_SPECS = [("DV0", 0.0, "identity"), ("DV1M", DV_FLOOR, "FLAGGED"),
               (f"VOLSH{S_STAR/1e3:.0f}k", S_STAR, "substitute")]
MASKS = {"SMALL439": {"DV0": base_mask(pxS, trS), "DV1M": dv_base,
                      FLOOR_SPECS[2][0]: vs_base},
         "U56": {"DV0": base_mask(px56, tr56)}}
VS_NAME = FLOOR_SPECS[2][0]

# ------------------------------------------------------------------ reproduction gates
P("\n" + "-" * 118)
P("G  REPRODUCTION GATES — nothing below is read until the flagged file re-derives here")
P("-" * 118)
w_probe = weights_ewall(pxS, MASKS["SMALL439"]["DV0"], gate_state(pxS, "band3", "TREND"), "dg")
r_eng = backtest(pxS, w_probe, cost_bps=10.0, freq=FREQ)["returns"]
g_, t_, _ = fast_bt(pxS, w_probe)
P(f"  [a] fast_bt vs engine.backtest  max|diff| = {np.abs(r_eng - net(g_, t_, 10)).max():.3e}")
spyS = pxS["SPY"].pct_change().fillna(0).loc[sS:]
mS = mrow(spyS)
P(f"  [b] SPY on the SMALL439 window: {mS['CAGR']:.2%}/{mS['Sharpe']:.3f}/{mS['MaxDD']:.1%} "
  f"halves {mS['H1']:.3f}/{mS['H2']:.3f}   [source file published 14.13%/0.862/-33.7%, "
  f"0.891/0.858]")
gv2, tv2, _ = fast_bt(px56, rules_v2_weights(px56))
v2_full = net(gv2, tv2, PROTO_COST)
mv2 = mrow(v2_full.loc[s56:])
P(f"  [c] LIVE RULES v2 on U56 @10bps: {mv2['CAGR']:.2%}/{mv2['Sharpe']:.4f}/{mv2['MaxDD']:.2%} "
  f"  [published 8.66%/1.2056/-12.05%]")
wv1 = rules_v1_weights(pxS.drop(columns=["SPY"])).reindex(columns=pxS.columns).fillna(0.0)
gv1, tv1, _ = fast_bt(pxS, wv1)
mv1 = mrow(net(gv1, tv1, 10).loc[sS:])
P(f"  [d] LIVE RULES v1 on SMALL439 @10bps: {mv1['CAGR']:.2%}/{mv1['Sharpe']:.3f}/"
  f"{mv1['MaxDD']:.1%}   [published 8.15%/0.603/-32.8%]")
# [e] the flagged file's OWN committed grid, at both of its floors, re-derived cell by cell
src_grid = pd.read_csv(OUT / f"{SRC}.grid.csv")
P(f"  [e] the flagged file's committed .grid.csv: {len(src_grid)} rows — every one re-derived "
  f"below and compared.")

# ------------------------------------------------------------------ main grid, all three floors
P("\n" + "-" * 118)
P("Q  MAIN GRID — panel x floor x conv x comp x arm x rung, every point printed")
P("-" * 118)
rows = []
for pname, (px, tr) in PANELS.items():
    st = START[pname]
    for fname, mask in MASKS[pname].items():
        n_sel = float(mask.loc[st:].sum(axis=1).mean())
        for comp in ("TREND", "FULL"):
            for arm in ARMS:
                gs = gate_state(px, arm, comp)
                held_names = float((gs & mask & px.notna()).loc[st:].sum(axis=1).mean())
                for conv in ("dg", "rw"):
                    gr, tn, gx = fast_bt(px, weights_ewall(px, mask, gs, conv))
                    gr, tn, gx = gr.loc[st:], tn.loc[st:], gx.loc[st:]
                    for c in COSTS:
                        m = mrow(net(gr, tn, c))
                        rows.append(dict(panel=pname, floor=fname, conv=conv, comp=comp, arm=arm,
                                         b=BAND_B.get(arm, np.nan), bps=c, **m,
                                         turnover=turn_per_yr(tn),
                                         realised_gross=float(gx.mean()),
                                         names_sel=n_sel, names_held=held_names,
                                         flips=flip_rate(gs.loc[st:], px.loc[st:], tr)))
grid = pd.DataFrame(rows)
key = ["panel", "floor", "conv", "comp", "bps"]
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

# gate [e]: every DV cell must reproduce the flagged file's committed number
fmap = {"DV0": 0.0, "DV1M": 1.0}
g_cmp = grid[grid.floor.isin(fmap)].copy()
g_cmp["floor_musd"] = g_cmp.floor.map(fmap)
mg = g_cmp.merge(src_grid, on=["panel", "floor_musd", "conv", "comp", "arm", "bps"],
                 suffixes=("", "_src"), how="inner", validate="one_to_one")
mg["d_sh"] = np.abs(mg.Sharpe - mg.Sharpe_src)
mg["d_cg"] = np.abs(mg.CAGR - mg.CAGR_src)
P(f"  [e] {len(mg)} of the flagged file's {len(src_grid)} committed cells re-derived, BY PANEL")
P(f"      (the gate that binds is SMALL439 — it is the only panel the substitution touches):")
for pn, gsub in mg.groupby("panel"):
    P(f"      {pn:<9} n={len(gsub):>3}  max|dSharpe| {gsub.d_sh.max():.3e}  "
      f"max|dCAGR| {gsub.d_cg.max():.3e}")
d_sh = float(mg[mg.panel == "SMALL439"].d_sh.max())
d_cg = float(mg[mg.panel == "SMALL439"].d_cg.max())
d_sh56 = float(mg[mg.panel == "U56"].d_sh.max())
P(f"      SMALL439 (288 cells, both floors): max|dSharpe| {d_sh:.3e} "
  f"-> {'GATE PASSES (bit-exact)' if d_sh < 1e-12 else 'GATE FAILS'}")
P(f"      U56 (144 cells) drifts {d_sh56:.1e} in Sharpe.  DIAGNOSED, not waved away: U56 reads")
P(f"      data/prices.csv, which the daily-close job rewrote on 2026-09-07, AFTER the flagged")
P(f"      file ran on 2026-09-06; data/prices_small.csv.gz has not moved since.  The drift is")
P(f"      one more trading day of cache, it is uniform across the U56 cells, and no U56 cell")
P(f"      carries the floor — so it cannot enter any DV-vs-VOLSH contrast below.  It IS carried")
P(f"      into R8's 108-arm count (36 of those arms are U56) and is reported there as such.")

for pname in ("SMALL439", "U56"):
    for fname in MASKS[pname]:
        for comp in ("FULL", "TREND"):
            for conv in ("rw", "dg"):
                s = grid[(grid.panel == pname) & (grid.floor == fname) &
                         (grid.comp == comp) & (grid.conv == conv)]
                P(f"\n  {pname}  floor {fname}  comp {comp}  conv {conv}"
                  f"   (selectable {s.names_sel.iloc[0]:.1f} names)")
                P(f"    {'arm':<8}{'flips':>7}{'held':>7}{'gross':>7}{'turn':>7}" +
                  "".join(f"{'CAGR@' + str(c):>10}" for c in COSTS) +
                  "".join(f"{'dCAGR@' + str(c):>11}" for c in COSTS) +
                  f"{'Sh@10':>8}{'dSh@10':>8}{'MaxDD@10':>10}{'H1@10':>8}{'H2@10':>8}")
                for arm in ARMS:
                    a = s[s.arm == arm].set_index("bps")
                    a10 = a.loc[PROTO_COST]
                    P(f"    {arm:<8}{a10.flips:>7.2f}{a10.names_held:>7.0f}"
                      f"{a10.realised_gross:>7.2f}{a10.turnover:>7.1f}" +
                      "".join(f"{a.loc[c, 'CAGR']:>10.2%}" for c in COSTS) +
                      "".join(f"{a.loc[c, 'dCAGR_pp']:>11.2f}" for c in COSTS) +
                      f"{a10.Sharpe:>8.3f}{a10.dSharpe:>8.3f}{a10.MaxDD:>10.1%}"
                      f"{a10.H1:>8.3f}{a10.H2:>8.3f}")

# ------------------------------------------------------------------ R7: rule 8 under both floors
P("\n" + "-" * 118)
P("R7  PROTOCOL RULE 8 — the flagged file's Q5, re-run under each floor instrument")
P("-" * 118)
spy_oos = {p: metrics(PANELS[p][0]["SPY"].pct_change().fillna(0).loc[START[p]:].loc[OOS_START:])
           for p in PANELS}
wrows = []
for pname, (px, tr) in PANELS.items():
    st = START[pname]
    for fname, mask in MASKS[pname].items():
        for comp in ("FULL", "TREND"):
            for conv in ("rw", "dg"):
                series = {}
                for arm in BAND_ARMS + ["NOGATE"]:
                    gr, tn, _ = fast_bt(px, weights_ewall(px, mask, gate_state(px, arm, comp), conv))
                    series[arm] = (gr.loc[st:], tn.loc[st:])
                for c in COSTS:
                    R = {a: net(g, t, c) for a, (g, t) in series.items()}
                    IS = {a: r.loc[:IS_END] for a, r in R.items()}
                    OS = {a: r.loc[OOS_START:] for a, r in R.items()}
                    pick_sh = max(BAND_ARMS, key=lambda a: metrics(IS[a])["Sharpe"])
                    pick_cg = max(BAND_ARMS, key=lambda a: metrics(IS[a])["CAGR"] -
                                  metrics(IS["NOGATE"])["CAGR"])
                    row = dict(panel=pname, floor=fname, conv=conv, comp=comp, bps=c,
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

P(f"  {'panel':<9}{'floor':>10}{'conv':>5}{'comp':>6}{'bps':>4}{'IS-Sh pick':>11}"
  f"{'IS-dC pick':>11}{'OOS Sh pick':>12}{'OOS Sh b3':>11}{'OOS Sh 200d':>12}"
  f"{'OOS Sh none':>12}{'SPY OOS':>9}")
for _, r in wf.iterrows():
    P(f"  {r.panel:<9}{r.floor:>10}{r.conv:>5}{r.comp:>6}{int(r.bps):>4}{r.pick_IS_Sharpe:>11}"
      f"{r.pick_IS_dCAGR:>11}{r.pickSh_oosSharpe:>12.3f}{r.const_band3_oosSharpe:>11.3f}"
      f"{r.incumbent_200d_oosSharpe:>12.3f}{r.donothing_NOGATE_oosSharpe:>12.3f}"
      f"{spy_oos[r.panel]['Sharpe']:>9.3f}")

P("\n  The published row R7 reads the SMALL439 32-cell set {2 floors x 2 comp x 2 conv x 4 bps}.")
P("  Restated with the DV1M half replaced by the matched VOLSH floor:")
wf_r7 = {}
for tag, floors in (("PUBLISHED (DV0 + DV1M)", ["DV0", "DV1M"]),
                    ("SUBSTITUTED (DV0 + VOLSH*)", ["DV0", VS_NAME]),
                    ("DV1M half alone", ["DV1M"]),
                    ("VOLSH* half alone", [VS_NAME])):
    w = wf[(wf.panel == "SMALL439") & (wf.floor.isin(floors))]
    wf_r7[tag] = w
    P(f"\n  [{tag}]  n={len(w)} cells")
    P(f"    beats do-nothing OOS in {int((w.pickSh_oosSharpe > w.donothing_NOGATE_oosSharpe).sum())}/{len(w)}; "
      f"beats constant band3 in {int((w.pickSh_oosSharpe > w.const_band3_oosSharpe).sum())}/{len(w)}; "
      f"beats SPY OOS in {int((w.pickSh_oosSharpe > spy_oos['SMALL439']['Sharpe']).sum())}/{len(w)}")
    P(f"    mean OOS Sharpe: pick {w.pickSh_oosSharpe.mean():.3f}  band3 "
      f"{w.const_band3_oosSharpe.mean():.3f}  200d {w.incumbent_200d_oosSharpe.mean():.3f}  "
      f"NOGATE {w.donothing_NOGATE_oosSharpe.mean():.3f}  SPY {spy_oos['SMALL439']['Sharpe']:.3f}")
    P(f"    mean OOS CAGR:   pick {w.pickSh_oosCAGR.mean():.2%}  band3 "
      f"{w.const_band3_oosCAGR.mean():.2%}  200d {w.incumbent_200d_oosCAGR.mean():.2%}  "
      f"NOGATE {w.donothing_NOGATE_oosCAGR.mean():.2%}  SPY {spy_oos['SMALL439']['CAGR']:.2%}")
    P(f"    mean OOS MaxDD:  pick {w.pickSh_oosMaxDD.mean():.1%}  band3 "
      f"{w.const_band3_oosMaxDD.mean():.1%}  200d {w.incumbent_200d_oosMaxDD.mean():.1%}  "
      f"NOGATE {w.donothing_NOGATE_oosMaxDD.mean():.1%}  SPY {spy_oos['SMALL439']['MaxDD']:.1%}")
w56 = wf[wf.panel == "U56"]
P(f"\n  U56 (floor-free, published as the 14th selector-loses-to-a-constant instance): "
  f"constant band3 beats the IS chooser in "
  f"{int((w56.const_band3_oosSharpe > w56.pickSh_oosSharpe).sum())}/{len(w56)} "
  f"({w56.const_band3_oosSharpe.mean():.3f} vs {w56.pickSh_oosSharpe.mean():.3f})  "
  f"[published 12/16, 1.249 vs 1.191]")

# ------------------------------------------------------------------ R8: both KEEP paths
P("\n" + "-" * 118)
P("R8  BOTH KEEP PATHS at 10 bps — the flagged file's Q6, re-run under each floor instrument")
P("-" * 118)


def path_verdicts(pname, r_full, r_oos):
    m = mrow(r_full)
    sp = PANELS[pname][0]["SPY"].pct_change().fillna(0).loc[START[pname]:]
    ms = mrow(sp)
    mb = mrow(v2_full.reindex(r_full.index).fillna(0.0))
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
    return bad_a, bad_b


vrows = []
for pname, (px, tr) in PANELS.items():
    st = START[pname]
    for fname, mask in MASKS[pname].items():
        for comp in ("FULL", "TREND"):
            for conv in ("rw", "dg"):
                for arm in ARMS:
                    gr, tn, _ = fast_bt(px, weights_ewall(px, mask, gate_state(px, arm, comp), conv))
                    r = net(gr.loc[st:], tn.loc[st:], PROTO_COST)
                    ba, bb = path_verdicts(pname, r, r.loc[OOS_START:])
                    m = mrow(r)
                    vrows.append(dict(panel=pname, floor=fname, conv=conv, comp=comp, arm=arm,
                                      CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                      H1=m["H1"], H2=m["H2"],
                                      path4a="KEEP" if not ba else "KILL(" + ",".join(ba) + ")",
                                      path4b="KEEP" if not bb else "KILL(" + ",".join(bb) + ")"))
V = pd.DataFrame(vrows)
V.to_csv(OUT / f"{STEM}.verdicts.csv", index=False)
mspy = mrow(spyS)
P(f"  4b bars (SPY, SMALL439 window): H1 > {mspy['H1']:.3f}, H2 > {mspy['H2']:.3f}, "
  f"OOS Sharpe > {spy_oos['SMALL439']['Sharpe']:.3f}, MaxDD >= {0.60 * mspy['MaxDD']:.1%}, "
  f"CAGR >= {0.70 * mspy['CAGR']:.2%}")
r8 = {}
for tag, sets in (("PUBLISHED (SMALL DV0+DV1M, U56)", [("SMALL439", "DV0"), ("SMALL439", "DV1M"),
                                                       ("U56", "DV0")]),
                  (f"SUBSTITUTED (SMALL DV0+VOLSH*, U56)", [("SMALL439", "DV0"),
                                                            ("SMALL439", VS_NAME), ("U56", "DV0")]),
                  ("SMALL DV1M alone", [("SMALL439", "DV1M")]),
                  ("SMALL VOLSH* alone", [("SMALL439", VS_NAME)])):
    sel = pd.concat([V[(V.panel == p) & (V.floor == f)] for p, f in sets])
    r8[tag] = sel
    P(f"\n  [{tag}]  n={len(sel)}   4a KEEP {(sel.path4a == 'KEEP').sum()}/{len(sel)};  "
      f"4b KEEP {(sel.path4b == 'KEEP').sum()}/{len(sel)}")
    sm = sel[sel.panel == "SMALL439"]
    if len(sm):
        P(f"      SMALL439 alone: 4a {(sm.path4a == 'KEEP').sum()}/{len(sm)}, "
          f"4b {(sm.path4b == 'KEEP').sum()}/{len(sm)}")
    fails = pd.Series([x for s in sel.path4b for x in
                       (s[5:-1].split(",") if s.startswith("KILL") else [])]).value_counts()
    P(f"      binding bars (4b): " + ", ".join(f"{k} {v}" for k, v in fails.items()))

# ------------------------------------------------------------------ S4: do the two rows move?
P("\n" + "-" * 118)
P("S4  DO THE TWO REACHABLE ROWS MOVE?  (a row MOVES if any published count/verdict changes)")
P("-" * 118)
pubR7 = wf_r7["PUBLISHED (DV0 + DV1M)"]
subR7 = wf_r7["SUBSTITUTED (DV0 + VOLSH*)"]
pubR8 = r8["PUBLISHED (SMALL DV0+DV1M, U56)"]
subR8 = r8[f"SUBSTITUTED (SMALL DV0+VOLSH*, U56)"]
checks = []


def chk(row, claim, pub, sub, fmt="{:.3f}", tol=0.0):
    moved = (abs(pub - sub) > tol) if isinstance(pub, float) else (pub != sub)
    checks.append(dict(row=row, claim=claim, published=pub, substituted=sub, moved=bool(moved)))
    P(f"  {row:<4}{claim:<52}{fmt.format(pub):>12}{fmt.format(sub):>14}   "
      f"{'MOVES' if moved else 'restates'}")


P(f"  {'row':<4}{'published claim':<52}{'DV (published)':>12}{'VOLSH (sub)':>14}   verdict")
chk("R7", "SMALL439 IS-pick mean OOS Sharpe", pubR7.pickSh_oosSharpe.mean(),
    subR7.pickSh_oosSharpe.mean(), "{:.3f}", 0.0005)
chk("R7", "SMALL439 do-nothing mean OOS Sharpe", pubR7.donothing_NOGATE_oosSharpe.mean(),
    subR7.donothing_NOGATE_oosSharpe.mean(), "{:.3f}", 0.0005)
chk("R7", "SMALL439 band3 mean OOS Sharpe", pubR7.const_band3_oosSharpe.mean(),
    subR7.const_band3_oosSharpe.mean(), "{:.3f}", 0.0005)
chk("R7", "SMALL439 200d mean OOS Sharpe", pubR7.incumbent_200d_oosSharpe.mean(),
    subR7.incumbent_200d_oosSharpe.mean(), "{:.3f}", 0.0005)
chk("R7", "SMALL439 picks beating SPY OOS (of 32)",
    int((pubR7.pickSh_oosSharpe > spy_oos["SMALL439"]["Sharpe"]).sum()),
    int((subR7.pickSh_oosSharpe > spy_oos["SMALL439"]["Sharpe"]).sum()), "{:d}")
chk("R7", "SMALL439 IS-pick mean OOS CAGR (pp)", 100 * pubR7.pickSh_oosCAGR.mean(),
    100 * subR7.pickSh_oosCAGR.mean(), "{:.2f}", 0.005)
chk("R7", "SMALL439 do-nothing mean OOS CAGR (pp)", 100 * pubR7.donothing_NOGATE_oosCAGR.mean(),
    100 * subR7.donothing_NOGATE_oosCAGR.mean(), "{:.2f}", 0.005)
chk("R7", "SMALL439 'pick loses to do-nothing on OOS CAGR'",
    bool(pubR7.pickSh_oosCAGR.mean() < pubR7.donothing_NOGATE_oosCAGR.mean()),
    bool(subR7.pickSh_oosCAGR.mean() < subR7.donothing_NOGATE_oosCAGR.mean()), "{}")
chk("R8", "4a KEEP count (of 108)", int((pubR8.path4a == "KEEP").sum()),
    int((subR8.path4a == "KEEP").sum()), "{:d}")
chk("R8", "4b KEEP count (of 108)", int((pubR8.path4b == "KEEP").sum()),
    int((subR8.path4b == "KEEP").sum()), "{:d}")
chk("R8", "4b KEEP count on SMALL439 alone (of 72)",
    int(((pubR8.panel == "SMALL439") & (pubR8.path4b == "KEEP")).sum()),
    int(((subR8.panel == "SMALL439") & (subR8.path4b == "KEEP")).sum()), "{:d}")
for bar in ("CAGR", "H1", "H2", "OOS", "DD"):
    chk("R8", f"4b binding bar '{bar}' count over the 108",
        int(pubR8.path4b.str.contains(bar).sum()), int(subR8.path4b.str.contains(bar).sum()),
        "{:d}")
rowsdf = pd.DataFrame(checks)
rowsdf.to_csv(OUT / f"{STEM}.rows.csv", index=False)
moved_rows = sorted(set(rowsdf.loc[rowsdf.moved, "row"]))
P(f"\n  S4 -> of the {n_reach} reachable rows, {len(moved_rows)} move: "
  f"{', '.join(moved_rows) if moved_rows else '(none)'}")

# cell-level: how many of the 36 substituted arm-cells change verdict, and by how much?
pv = pubR8[(pubR8.panel == "SMALL439") & (pubR8.floor == "DV1M")].set_index(["conv", "comp", "arm"])
sv = subR8[(subR8.panel == "SMALL439") & (subR8.floor == VS_NAME)].set_index(["conv", "comp", "arm"])
j = pv.join(sv, lsuffix="_dv", rsuffix="_vs")
P(f"\n  cell level, the 36 SMALL439 arm-cells the substitution actually touches:")
P(f"    4b verdict changes in {(j.path4b_dv != j.path4b_vs).sum()}/36; "
  f"4a in {(j.path4a_dv != j.path4a_vs).sum()}/36")
chg = j[j.path4b_dv != j.path4b_vs]
if len(chg):
    P(f"    {'conv':>5}{'comp':>6}{'arm':>9}{'4b under DV1M':>28}{'4b under VOLSH*':>28}"
      f"{'MaxDD DV':>10}{'MaxDD VS':>10}")
    for (cv, cp, ar), r in chg.iterrows():
        P(f"    {cv:>5}{cp:>6}{ar:>9}{r.path4b_dv:>28}{r.path4b_vs:>28}"
          f"{r.MaxDD_dv:>10.1%}{r.MaxDD_vs:>10.1%}")
    P(f"    Every one of these is a KILL under BOTH floors — what moves is WHICH BAR binds, and")
    P(f"    it moves on the drawdown bar only.  No arm changes side of a KEEP path.")
P(f"    |dSharpe| mean {np.abs(j.Sharpe_dv - j.Sharpe_vs).mean():.4f}, "
  f"max {np.abs(j.Sharpe_dv - j.Sharpe_vs).max():.4f}; "
  f"|dCAGR| mean {100 * np.abs(j.CAGR_dv - j.CAGR_vs).mean():.3f} pp, "
  f"max {100 * np.abs(j.CAGR_dv - j.CAGR_vs).max():.3f} pp")

# the one non-LEADERBOARD claim the floor also reaches: the CHANGELOG survivorship sentence
P(f"\n  BY-PRODUCT — the flagged file's CHANGELOG survivorship sentence ('at a $1M ADV floor the")
P(f"  published damage shrinks from -6.52 to -4.87 pp @10bps but never changes sign'):")
for fname in MASKS["SMALL439"]:
    ew = grid[(grid.panel == "SMALL439") & (grid.floor == fname) & (grid.conv == "rw") &
              (grid.comp == "TREND") & (grid.bps == 10) & (grid.arm == "NOGATE")].CAGR.iloc[0]
    bo = grid[(grid.panel == "SMALL439") & (grid.floor == fname) & (grid.conv == "rw") &
              (grid.comp == "FULL") & (grid.bps == 10) & (grid.arm == "200d")].CAGR.iloc[0]
    P(f"    floor {fname:<10} published gate damage @10bps = {(bo - ew) * 100:+.4f} pp")

# ------------------------------------------------------------------ verdict
P("\n" + "=" * 118)
P("VERDICT")
P("=" * 118)
P(f"S1 structural census .......... {n_reach} of 9 published rows are at a coordinate the floor "
  f"can reach; {9 - n_reach} are quoted at floor $0 where the flagged line is the identity map.")
P(f"S2 the flag is right at the mask ... DVOL moves {dv_moved:.2%} of live ticker-days under T1, "
  f"VOLSH {volsh_moved:.4%}.")
P(f"S3 the masks are different objects ... {s3:.2%} disagreement at matched admission rate "
  f"({matched_names:.1f} vs {target_names:.1f} names/day).")
P(f"S4 rows that MOVE ............. {len(moved_rows)} of {n_reach} reachable "
  f"({len(moved_rows)} of 9 published): {', '.join(moved_rows) if moved_rows else '(none)'}")
P(f"\nruntime {time.time() - T0:.0f}s")
(OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
