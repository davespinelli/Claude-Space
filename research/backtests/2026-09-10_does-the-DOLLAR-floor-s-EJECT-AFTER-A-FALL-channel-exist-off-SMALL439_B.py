#!/usr/bin/env python3
"""IDEA 645 — does the DOLLAR floor's EJECT-AFTER-A-FALL channel exist off SMALL439?   (lane B, 2026-09-10)

QUEUE 645: idea 427 named the mechanism behind the dollar-vs-share floor gap: `px*vol` moves with
price, so the DV-only admitted set has run +11.01% over the prior 126d and returns +0.29% over the
next 126d while the VOLSH-only set has run +2.53% and returns +28.91%.  On a current-constituent
panel that is indistinguishable from survivorship.  Re-measure the SAME trailing/forward split on a
panel with a delisted cohort (or on U56/broad136 once idea 429 caches volume) and decide whether the
channel is real.  Max 2 params (panel, horizon).

DATA CONSTRAINT, stated up front.  There is no delisted cohort in data/ and U56/broad136 volume is
NOT cached (queue idea 429, needs network).  A naive reading of 645 is therefore PARK.  It is not,
because of an ALGEBRAIC IDENTITY the parent run reported as a "post-hoc mechanism":

    DV := median_20(px*vol),  SV := median_20(vol),  IP := DV/SV   (an implied 20d price)
    DV-only(F,s)   <=>  DV >= F  and  SV <  s  <=>  SV*IP >= F and SV < s  ==>  IP > F/s
    VOLSH-only(F,s)<=>  SV >= s  and  DV <  F  <=>  SV >= s and SV*IP < F  ==>  IP < F/s

so the two swapped sets are separated by an EXACT one-sided cut on IP at the threshold F/s, with no
return input and no free parameter.  If IP is close enough to the traded price px, the channel can be
measured on ANY panel with prices alone -- which is exactly what 645 asks for.  Q1 gates that
substitution on SMALL439 (where volume IS cached); Q3 then carries the price-only restatement to U56
and broad136.  Every leg that needs volume is confined to SMALL439 and labelled.

TUNED PARAMETERS (2, per the queue's "panel, horizon" budget, re-spent as the two dials that are
actually free once panel is reported-across rather than chosen):
    q  price-rank quantile cut   {0.10, 0.20, 0.30, 0.40, 0.50}
    h  horizon / rebalance       {W, M, Q}  (and {63,126,252}d for the descriptive split)
PANEL is reported across all three, never selected.  Every grid point is printed and written to CSV.

Costs 10 bps (PROTOCOL 2), next-day execution (engine), rule-8 walk-forward IS 2010-2016 / OOS
2017-2026, both KEEP paths 4a and 4b evaluated (PROTOCOL 4).
"""
from __future__ import annotations
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, load_volume, rules_v2_weights            # noqa: E402
from engine import backtest, metrics, rebalance_mask                          # noqa: E402

pd.set_option("display.width", 200)
OUT = ROOT / "research" / "backtests"
STEM = "2026-09-10_does-the-DOLLAR-floor-s-EJECT-AFTER-A-FALL-channel-exist-off-SMALL439_B"

# ------------------------------------------------------------------ constants (pre-registered)
CLAUSE_F = 1e6                              # idea 121's dollar floor, the level 427 priced
COSTS = [0, 5, 10, 25]
PROTO_COST = 10
IS_END, OOS_START = "2016-12-31", "2017-01-01"
QGRID = [0.10, 0.20, 0.30, 0.40, 0.50]      # tuned dial 1
HGRID = ["W", "M", "Q"]                     # tuned dial 2 (book cadence)
DAYS = [63, 126, 252]                       # tuned dial 2 (descriptive horizon)
GROSS = 0.75                                # RULES v2's gross, held fixed (not a dial)
PANELS = ["SMALL439", "U56", "broad136"]

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# ------------------------------------------------------------------ engine (vectorised, gated at G2)
def fast_bt(px, w, freq="W"):
    """Exact vectorised equivalent of engine.backtest; returns GROSS returns and turnover separately
    so the cost rung is a post-hoc sweep (engine identity: port = (held*rets).sum(1) - turn*bps/1e4)."""
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


# ------------------------------------------------------------------ panels
def build_small():
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])          # idea 427's filter, kept
    keep = [c for c in pxs.columns if c == "SPY" or c not in bad]
    return pxs[keep].dropna(how="all").ffill()


T0 = time.time()
P("=" * 118)
P("IDEA 645  does-the-DOLLAR-floor-s-EJECT-AFTER-A-FALL-channel-exist-off-SMALL439   (lane B, 2026-09-10)")
P("=" * 118)

PX, TCOLS, START = {}, {}, {}
PX["SMALL439"] = build_small()
PX["U56"] = load_universe()
PX["broad136"] = load_universe(broad=True)
for p in PANELS:
    TCOLS[p] = [c for c in PX[p].columns if c != "SPY"]
    START[p] = PX[p].index[260]
    P(f"[panel] {p:<10} {len(TCOLS[p]):>4} tradable (+SPY benchmark)  "
      f"{PX[p].index[0].date()}..{PX[p].index[-1].date()}  evaluation from {START[p].date()}")

P("\n[coverage] volume cached?  (645 asks for the split off SMALL439; volume is what makes that hard)")
for p, kw in (("SMALL439", dict(small=True)), ("U56", dict()), ("broad136", dict(broad=True))):
    try:
        load_volume(**kw)
        st = "CACHED"
    except Exception as e:
        st = f"NOT CACHED ({type(e).__name__})"
    P(f"    {p:<10} {st}")
P("    -> 1 of 3.  data/ has no delisted cohort either.  The literal 645 is unrunnable; Q1 below")
P("       replaces the volume split with an EXACT algebraic equivalent that needs prices only.")

px = PX["SMALL439"]
tcs = TCOLS["SMALL439"]
S0 = START["SMALL439"]
VOL = load_volume(small=True).reindex(index=px.index).reindex(columns=px.columns)
LIVE = px[tcs].notna()
DV = (px[tcs] * VOL[tcs]).rolling(20).median()
SV = VOL[tcs].rolling(20).median()
ev = px.index >= S0

# ------------------------------------------------------------------ s*: matched-admission share floor
tgt = float((LIVE & (DV >= CLAUSE_F).fillna(False)).loc[S0:].sum(axis=1).mean())


def _n_sv(s):
    return float((LIVE.loc[S0:] & (SV.loc[S0:] >= s).fillna(False)).sum(axis=1).mean())


lo, hi = 0.0, 5e7
for _ in range(60):
    mid = 0.5 * (lo + hi)
    if _n_sv(mid) > tgt:
        lo = mid
    else:
        hi = mid
SSTAR = 0.5 * (lo + hi)
PXSTAR = CLAUSE_F / SSTAR
P(f"\n[calibration] DV floor ${CLAUSE_F/1e6:.2f}M admits {tgt:.2f} names/day; matched share floor"
  f" s* = {SSTAR:,.0f} sh/day admits {_n_sv(SSTAR):.2f}.  Implied price threshold F/s* = ${PXSTAR:.2f}")

base_dv = (LIVE & (DV >= CLAUSE_F).fillna(False)).loc[S0:]
base_sv = (LIVE & (SV >= SSTAR).fillna(False)).loc[S0:]
livedays = LIVE.loc[S0:]
d_only = base_dv & ~base_sv & livedays
v_only = ~base_dv & base_sv & livedays
both = base_dv & base_sv & livedays

# ================================================================== GATES
P("\n" + "-" * 118)
P("GATES — pre-registered reproductions before anything new is read")
P("-" * 118)
gates = []

# G1: engine identity, over the EVALUATION window only.  engine.backtest emits NaN on the first two
# rows of every panel (its `weights.shift(1)` leaves row 0 undefined and the first rebalance reads it);
# those rows are inside the 260-day warm-up that PROTOCOL drops, and fast_bt fills them with 0 instead.
# The gate reports the discrepancy explicitly rather than hiding it.
def _g1(pxp, w, tag):
    st = pxp.index[260]
    e = backtest(pxp, w, cost_bps=PROTO_COST, freq="W")
    g, t = fast_bt(pxp, w, "W")
    a, b = e["returns"].loc[st:].values, net(g, t, PROTO_COST).loc[st:].values
    ta, tb = e["turnover"].loc[st:].values, t.loc[st:].values
    warm = int((~np.isfinite(e["returns"].values)).sum())
    d1 = float(np.abs(a - b).max())
    d2 = float(np.abs(ta - tb).max())
    passed = bool(np.isfinite(a).all() and np.isfinite(b).all() and d1 < 1e-12 and d2 < 1e-12)
    gates.append(dict(gate=f"G1 fast_bt == engine.backtest [{tag}]", warmup_nonfinite=warm,
                      stat=f"max|dret| {d1:.2e} max|dturn| {d2:.2e}", passed=passed))
    P(f"  G1  fast_bt vs engine.backtest [{tag}], evaluation window: max|dret| {d1:.2e},"
      f" max|dturn| {d2:.2e}   -> {'PASS' if passed else 'FAIL'}"
      f"   (engine NaN rows inside the dropped warm-up: {warm})")
    return passed


_lo = pd.DataFrame(0.0, index=px.index, columns=px.columns)
_sel = ((px[tcs].rank(axis=1, pct=True) <= 0.20) & px[tcs].notna())
_lo[tcs] = (0.75 * _sel.astype(float)).div(_sel.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
_g1(px, rules_v2_weights(px), "RULES v2, SMALL439")
_g1(px, _lo, "LOW q=0.20 book, SMALL439")
_g1(PX["U56"], rules_v2_weights(PX["U56"]), "RULES v2, U56")

# G2: idea 427's headline trailing/forward split reproduces
pxT = px[tcs]
r126b = (pxT / pxT.shift(126) - 1.0).loc[S0:]
r126f = (pxT.shift(-126) / pxT - 1.0).loc[S0:]


def tf(mask, b=r126b, f=r126f):
    mv = mask.values
    return (float(np.nanmean(np.where(mv, b.values, np.nan))),
            float(np.nanmean(np.where(mv, f.values, np.nan))))


tb_d, tf_d = tf(d_only)
tb_v, tf_v = tf(v_only)
tb_b, tf_b = tf(both)
pub = dict(dv_b=0.1101, dv_f=0.0029, sv_b=0.0253, sv_f=0.2891)
err = max(abs(tb_d - pub["dv_b"]), abs(tf_d - pub["dv_f"]), abs(tb_v - pub["sv_b"]), abs(tf_v - pub["sv_f"]))
gates.append(dict(gate="G2 idea 427 P3 trailing/forward split", stat=f"max|diff| {err*100:.3f} pp",
                  passed=bool(err < 0.005)))
P(f"  G2  idea 427's published split reproduces:")
P(f"        DV-only     trailing 126d {tb_d:+.2%} (pub +11.01%)   forward 126d {tf_d:+.2%} (pub +0.29%)")
P(f"        VOLSH-only  trailing 126d {tb_v:+.2%} (pub  +2.53%)   forward 126d {tf_v:+.2%} (pub +28.91%)")
P(f"        both        trailing 126d {tb_b:+.2%}                 forward 126d {tf_b:+.2%}")
P(f"        max|diff| vs published {err*100:.3f} pp  -> {'PASS' if err < 0.005 else 'FAIL'}")
PUB_FWD_GAP = tf_v - tf_d
P(f"        published forward gap (VOLSH-only minus DV-only) = {PUB_FWD_GAP:+.2%}  [the object of 645]")

pd.DataFrame(gates).to_csv(OUT / f"{STEM}.gates.csv", index=False)

# ================================================================== Q1  THE IDENTITY
P("\n" + "-" * 118)
P("Q1  IS THE SWAP AN ALGEBRAIC PRICE CUT?  (the leg that makes 645 runnable without volume)")
P("-" * 118)
IP = (DV / SV).loc[S0:]
ipv = IP.values
above = np.nan_to_num(ipv > PXSTAR, nan=False)
below = np.nan_to_num(ipv < PXSTAR, nan=False)
n_d, n_v = int(d_only.values.sum()), int(v_only.values.sum())
sh_d = float((d_only.values & above).sum()) / n_d
sh_v = float((v_only.values & below).sum()) / n_v
P(f"  IP := median20(px*vol)/median20(vol).  Threshold F/s* = ${PXSTAR:.2f}.")
P(f"    DV-only    ticker-days {n_d:>9,}   with IP > F/s*: {sh_d:.6f}")
P(f"    VOLSH-only ticker-days {n_v:>9,}   with IP < F/s*: {sh_v:.6f}")
P(f"    -> the swap is an EXACT one-sided cut on IP.  It is not a 'post-hoc mechanism'; it is the")
P(f"       definition of the two instruments.  No return data enters, no parameter is fitted.")

# does the TRADED price substitute for IP?
lm = livedays.values & np.isfinite(ipv) & np.isfinite(pxT.loc[S0:].values)
a, b = np.log(ipv[lm]), np.log(pxT.loc[S0:].values[lm])
rho = float(np.corrcoef(a, b)[0, 1])
ratio = ipv[lm] / pxT.loc[S0:].values[lm]
agree = float((np.nan_to_num(ipv[lm] > PXSTAR, nan=False) ==
               np.nan_to_num(pxT.loc[S0:].values[lm] > PXSTAR, nan=False)).mean())
P(f"\n  TRANSPORT GATE — can the traded close px stand in for IP (so the split can be run on a panel")
P(f"  with no cached volume)?  Over {int(lm.sum()):,} live ticker-days:")
P(f"    corr(log IP, log px) {rho:.6f};  IP/px median {np.median(ratio):.4f}, p05 {np.percentile(ratio,5):.4f},"
  f" p95 {np.percentile(ratio,95):.4f}")
P(f"    the px cut at ${PXSTAR:.2f} agrees with the IP cut on {agree:.4%} of live ticker-days")
TRANSPORT_OK = agree > 0.95 and rho > 0.99
P(f"    -> transport {'HOLDS' if TRANSPORT_OK else 'FAILS'}; px is {'an adequate' if TRANSPORT_OK else 'NOT an adequate'} stand-in for IP")
pd.DataFrame([dict(threshold=PXSTAR, dv_only_days=n_d, dv_only_share_above=sh_d,
                   volsh_only_days=n_v, volsh_only_share_below=sh_v, rho_log=rho,
                   ip_over_px_median=float(np.median(ratio)), px_cut_agreement=agree)]
             ).to_csv(OUT / f"{STEM}.identity.csv", index=False)

# ================================================================== Q2  LEVEL vs EVENT
P("\n" + "-" * 118)
P("Q2  IS 'EJECT AFTER A FALL' THE RIGHT NAME?   LEVEL cut vs the literal EVENT   (SMALL439 only)")
P("-" * 118)
P("  645 (via 427) names an EVENT mechanism: the dollar floor EJECTS a name AFTER it falls and")
P("  RE-ADMITS after a rise.  Q1 says the split is a LEVEL cut.  Those are different claims, and")
P("  only one of them is about price PATH.  Four splits, same trailing/forward statistic:")
q2 = []
ip_hi = pd.DataFrame(np.nan_to_num(ipv > PXSTAR, nan=False), index=IP.index, columns=IP.columns) & livedays
ip_lo = pd.DataFrame(np.nan_to_num(ipv < PXSTAR, nan=False), index=IP.index, columns=IP.columns) & livedays
px_hi = (pxT.loc[S0:] > PXSTAR) & livedays
px_lo = (pxT.loc[S0:] <= PXSTAR) & livedays
# the literal event: DV crossed the floor DOWN (ejected) / UP (re-admitted) in the last 126 sessions
dvin = (DV >= CLAUSE_F).fillna(False)
ej = (dvin.shift(1) & ~dvin).rolling(126).max().fillna(0).astype(bool).loc[S0:] & livedays
ad = (~dvin.shift(1).fillna(False) & dvin).rolling(126).max().fillna(0).astype(bool).loc[S0:] & livedays
for tag, m in (("DV-only (427)", d_only), ("VOLSH-only (427)", v_only),
               ("IP > F/s*", ip_hi), ("IP < F/s*", ip_lo),
               ("px > F/s*", px_hi), ("px <= F/s*", px_lo),
               ("EJECTED <=126d", ej), ("RE-ADMITTED <=126d", ad)):
    tbx, tfx = tf(m)
    q2.append(dict(split=tag, days=int(m.values.sum()), trail126=tbx, fwd126=tfx))
    P(f"    {tag:<20} days {int(m.values.sum()):>9,}   trailing 126d {tbx:+8.2%}   forward 126d {tfx:+8.2%}")
Q2 = pd.DataFrame(q2).set_index("split")
Q2.to_csv(OUT / f"{STEM}.levelvsevent.csv")
g_vol = Q2.loc["VOLSH-only (427)", "fwd126"] - Q2.loc["DV-only (427)", "fwd126"]
g_ip = Q2.loc["IP < F/s*", "fwd126"] - Q2.loc["IP > F/s*", "fwd126"]
g_px = Q2.loc["px <= F/s*", "fwd126"] - Q2.loc["px > F/s*", "fwd126"]
g_ev = Q2.loc["EJECTED <=126d", "fwd126"] - Q2.loc["RE-ADMITTED <=126d", "fwd126"]
P(f"\n    forward-126d gap, VOLUME split (idea 427)        {g_vol:+.2%}   [the published +28.62%]")
P(f"    forward-126d gap, IP LEVEL cut                  {g_ip:+.2%}   ({g_ip/g_vol:.0%} of it)")
P(f"    forward-126d gap, PRICE LEVEL cut (no volume)   {g_px:+.2%}   ({g_px/g_vol:.0%} of it)")
P(f"    forward-126d gap, LITERAL EJECT-vs-READMIT      {g_ev:+.2%}   ({g_ev/g_vol:.0%} of it)")
P(f"    -> the channel is a {'LEVEL' if abs(g_px) > abs(g_ev) else 'PATH'} effect."
  f"  'Eject after a fall' names the {'WRONG' if abs(g_px) > 2*abs(g_ev) else 'right'} object:"
  f" a price-level cut carries it, the crossing EVENT carries {abs(g_ev/g_vol):.0%}.")

# ================================================================== Q3  OFF-PANEL (the question)
P("\n" + "-" * 118)
P("Q3  DOES THE CHANNEL EXIST OFF SMALL439?   price-only restatement, all 3 panels, all grid points")
P("-" * 118)
P("  Two cut conventions, because the absolute threshold F/s* is a SMALL-CAP number and cannot be")
P("  transplanted to mega caps without re-deciding what 'cheap' means:")
P("    ABS  px <= F/s* = $%.2f (the literal clause)" % PXSTAR)
P("    REL  cross-sectional price rank <= q among that day's live names (panel-relative)")
P("  Reported for horizons h in %s.  Nothing is selected here; every cell is printed." % DAYS)
q3 = []
for p in PANELS:
    pxp = PX[p]
    tc = TCOLS[p]
    st = START[p]
    live = pxp[tc].notna().loc[st:]
    pl = pxp[tc].loc[st:]
    rk = pl.rank(axis=1, pct=True)
    spyf = {}
    for h in DAYS:
        bwd = (pxp[tc] / pxp[tc].shift(h) - 1.0).loc[st:]
        fwd = (pxp[tc].shift(-h) / pxp[tc] - 1.0).loc[st:]
        sp = pxp["SPY"]
        spyf[h] = float(((sp.shift(-h) / sp - 1.0).loc[st:]).mean())
        # ABS
        for cut, tag in ((pl <= PXSTAR, "ABS"),):
            lo_m, hi_m = (cut & live), (~cut & live)
            for side, m in (("LOW", lo_m), ("HIGH", hi_m)):
                tbx, tfx = tf(m, bwd, fwd)
                q3.append(dict(panel=p, conv=tag, q=np.nan, h=h, side=side,
                               daysh=int(m.values.sum()), share=float(m.values.sum() / live.values.sum()),
                               trail=tbx, fwd=tfx, spy_fwd=spyf[h]))
        # REL
        for q in QGRID:
            lo_m, hi_m = ((rk <= q) & live), ((rk > q) & live)
            for side, m in (("LOW", lo_m), ("HIGH", hi_m)):
                tbx, tfx = tf(m, bwd, fwd)
                q3.append(dict(panel=p, conv="REL", q=q, h=h, side=side,
                               daysh=int(m.values.sum()), share=float(m.values.sum() / live.values.sum()),
                               trail=tbx, fwd=tfx, spy_fwd=spyf[h]))
Q3 = pd.DataFrame(q3)
Q3.to_csv(OUT / f"{STEM}.offpanel.csv", index=False)
G3 = (Q3.pivot_table(index=["panel", "conv", "q", "h"], columns="side", values=["trail", "fwd"], dropna=False))
P(f"\n  {'panel':<10}{'conv':>5}{'q':>6}{'h':>5}{'LOW share':>11}{'LOW trail':>11}{'HIGH trail':>11}"
  f"{'LOW fwd':>10}{'HIGH fwd':>10}{'FWD GAP':>10}{'SPY fwd':>10}")
gaps = []
for p in PANELS:
    for conv in ("ABS", "REL"):
        for q in ([np.nan] if conv == "ABS" else QGRID):
            for h in DAYS:
                sel = Q3[(Q3.panel == p) & (Q3.conv == conv) & (Q3.h == h) &
                         (Q3["q"].isna() if conv == "ABS" else Q3["q"] == q)]
                lo = sel[sel.side == "LOW"].iloc[0]
                hi = sel[sel.side == "HIGH"].iloc[0]
                gap = lo.fwd - hi.fwd
                gaps.append(dict(panel=p, conv=conv, q=q, h=h, low_share=lo.share,
                                 low_trail=lo.trail, high_trail=hi.trail, low_fwd=lo.fwd,
                                 high_fwd=hi.fwd, fwd_gap=gap, trail_gap=lo.trail - hi.trail,
                                 spy_fwd=lo.spy_fwd))
                P(f"  {p:<10}{conv:>5}{('' if conv=='ABS' else f'{q:.2f}'):>6}{h:>5}{lo.share:>11.3f}"
                  f"{lo.trail:>11.2%}{hi.trail:>11.2%}{lo.fwd:>10.2%}{hi.fwd:>10.2%}{gap:>+10.2%}{lo.spy_fwd:>10.2%}")
GAP = pd.DataFrame(gaps)
GAP.to_csv(OUT / f"{STEM}.gaps.csv", index=False)
P(f"\n  grid n={len(GAP)} cells (3 panels x (1 ABS + 5 REL q) x 3 horizons), all printed above")
for p in PANELS:
    d = GAP[GAP.panel == p]
    d126 = d[d.h == 126]
    P(f"    {p:<10} forward gap (LOW - HIGH): mean {d.fwd_gap.mean():+.2%}, median {d.fwd_gap.median():+.2%},"
      f" positive {int((d.fwd_gap>0).sum())}/{len(d)};  at h=126 mean {d126.fwd_gap.mean():+.2%}")
sm = GAP[GAP.panel == "SMALL439"].fwd_gap.mean()
off = GAP[GAP.panel != "SMALL439"].fwd_gap.mean()
P(f"\n  ANSWER TO 645 (descriptive leg): SMALL439 mean forward gap {sm:+.2%} vs off-panel {off:+.2%}"
  f"  -> {sm/off if abs(off)>1e-9 else float('inf'):.2f}x")
P(f"  The channel {'DOES' if off > 0.05 else 'DOES NOT'} survive off SMALL439 at anything like its"
  f" published size.")

# ================================================================== Q4  SURVIVORSHIP DIAGNOSTICS
P("\n" + "-" * 118)
P("Q4  IS THE SMALL439 GAP THE SHAPE SURVIVORSHIP MAKES?   three signatures, no new data needed")
P("-" * 118)
P("  data/SMALL_PANEL_README.md: the panel is CURRENT constituents, 'bias grows with lookback',")
P("  'cross-sectional strategies look better ... especially deep-value and LOW-PRICE sorts'.  If the")
P("  gap is survivorship it should be (a) tail-driven, (b) era-decaying, (c) absent on mega caps.")
q4 = []
for p in PANELS:
    pxp, tc, st = PX[p], TCOLS[p], START[p]
    live = pxp[tc].notna().loc[st:]
    pl = pxp[tc].loc[st:]
    rk = pl.rank(axis=1, pct=True)
    fwd = (pxp[tc].shift(-126) / pxp[tc] - 1.0).loc[st:]
    lo_m = ((rk <= 0.20) & live)
    hi_m = ((rk > 0.20) & live)
    for tag, m in (("LOW q=0.20", lo_m), ("HIGH", hi_m)):
        v = fwd.values[m.values]
        v = v[np.isfinite(v)]
        q4.append(dict(panel=p, side=tag, n=len(v), mean=float(v.mean()), median=float(np.median(v)),
                       p90=float(np.percentile(v, 90)), p99=float(np.percentile(v, 99)),
                       share_gt_1=float((v > 1.0).mean())))
Q4 = pd.DataFrame(q4)
Q4.to_csv(OUT / f"{STEM}.tails.csv", index=False)
P(f"\n  (a) TAIL TEST — forward 126d distribution, REL q=0.20:")
P(f"      {'panel':<10}{'side':<12}{'n':>10}{'mean':>9}{'median':>9}{'p90':>9}{'p99':>10}{'P(>+100%)':>11}")
for _, r in Q4.iterrows():
    P(f"      {r.panel:<10}{r.side:<12}{r.n:>10,}{r['mean']:>9.2%}{r['median']:>9.2%}{r.p90:>9.2%}"
      f"{r.p99:>10.2%}{r.share_gt_1:>11.3%}")
for p in PANELS:
    d = Q4[Q4.panel == p].set_index("side")
    gm = d.loc["LOW q=0.20", "mean"] - d.loc["HIGH", "mean"]
    gd = d.loc["LOW q=0.20", "median"] - d.loc["HIGH", "median"]
    P(f"      {p:<10} MEAN gap {gm:+.2%} vs MEDIAN gap {gd:+.2%}  -> "
      f"{'TAIL-DRIVEN' if abs(gd) < 0.4*abs(gm) else 'broad-based'}"
      f" (median carries {gd/gm if abs(gm)>1e-9 else float('nan'):.0%})")

P(f"\n  (b) ERA TEST — the same gap, IS 2010-2016 vs OOS {OOS_START}-2026 (rule 8's own boundary):")
era = []
for p in PANELS:
    pxp, tc, st = PX[p], TCOLS[p], START[p]
    live = pxp[tc].notna().loc[st:]
    rk = pxp[tc].loc[st:].rank(axis=1, pct=True)
    fwd = (pxp[tc].shift(-126) / pxp[tc] - 1.0).loc[st:]
    for ename, sl in (("IS 2010-2016", slice(None, IS_END)), ("OOS 2017-2026", slice(OOS_START, None))):
        f2, l2, r2 = fwd.loc[sl], live.loc[sl], rk.loc[sl]
        a1 = f2.values[((r2 <= 0.20) & l2).values]
        a2 = f2.values[((r2 > 0.20) & l2).values]
        a1, a2 = a1[np.isfinite(a1)], a2[np.isfinite(a2)]
        era.append(dict(panel=p, era=ename, low=float(a1.mean()), high=float(a2.mean()),
                        gap=float(a1.mean() - a2.mean())))
ERA = pd.DataFrame(era)
ERA.to_csv(OUT / f"{STEM}.era.csv", index=False)
P(f"      {'panel':<10}{'era':<16}{'LOW fwd':>10}{'HIGH fwd':>10}{'gap':>10}")
for _, r in ERA.iterrows():
    P(f"      {r.panel:<10}{r.era:<16}{r.low:>10.2%}{r.high:>10.2%}{r.gap:>+10.2%}")
for p in PANELS:
    d = ERA[ERA.panel == p].set_index("era")
    P(f"      {p:<10} gap decays {d.loc['IS 2010-2016','gap']:+.2%} -> {d.loc['OOS 2017-2026','gap']:+.2%}"
      f"  ({d.loc['OOS 2017-2026','gap']/d.loc['IS 2010-2016','gap'] if abs(d.loc['IS 2010-2016','gap'])>1e-9 else float('nan'):.2f}x)")

# ================================================================== Q5  THE BOOK (PROTOCOL 4a/4b)
P("\n" + "-" * 118)
P("Q5  THE BOOK — is the channel worth capital?   3 panels x 5 q x 3 cadences x 2 sides x 4 costs")
P("-" * 118)
P(f"  Book: equal weight the selected side at gross {GROSS:.2f} of NAV, remainder CASH (RULES v2's own")
P("  gross convention).  LOW = the VOLSH-only shape (the side carrying the +28.9% forward return);")
P("  HIGH = the DV-only shape, carried as the mirror control.  Costs swept; PROTOCOL rung is 10 bps.")


def side_weights(pxp, tc, q, side):
    live = pxp[tc].notna()
    rk = pxp[tc].rank(axis=1, pct=True)
    sel = ((rk <= q) if side == "LOW" else (rk > q)) & live
    w = pd.DataFrame(0.0, index=pxp.index, columns=pxp.columns)
    cnt = sel.sum(axis=1).replace(0, np.nan)
    w[tc] = (GROSS * sel.astype(float)).div(cnt, axis=0).fillna(0.0)
    return w


BENCH = {}
for p in PANELS:
    pxp, st = PX[p], START[p]
    gb, tbn = fast_bt(pxp, rules_v2_weights(pxp), "W")
    rb = net(gb.loc[st:], tbn.loc[st:], PROTO_COST)
    spy = pxp["SPY"].pct_change().fillna(0).loc[st:]
    BENCH[p] = dict(v2=mrow(rb), v2_oos=metrics(rb.loc[OOS_START:]), spy=mrow(spy),
                    spy_oos=metrics(spy.loc[OOS_START:]))
    P(f"\n  [{p}] RULES v2 @10bps: CAGR {BENCH[p]['v2']['CAGR']:.2%} Sharpe {BENCH[p]['v2']['Sharpe']:.3f}"
      f" MaxDD {BENCH[p]['v2']['MaxDD']:.1%} H1/H2 {BENCH[p]['v2']['H1']:.3f}/{BENCH[p]['v2']['H2']:.3f}"
      f" | OOS Sharpe {BENCH[p]['v2_oos']['Sharpe']:.3f}")
    P(f"  [{p}] SPY:            CAGR {BENCH[p]['spy']['CAGR']:.2%} Sharpe {BENCH[p]['spy']['Sharpe']:.3f}"
      f" MaxDD {BENCH[p]['spy']['MaxDD']:.1%} H1/H2 {BENCH[p]['spy']['H1']:.3f}/{BENCH[p]['spy']['H2']:.3f}"
      f" | OOS Sharpe {BENCH[p]['spy_oos']['Sharpe']:.3f}")


def verdicts(p, r):
    m = mrow(r)
    B = BENCH[p]
    ba = []
    if m["H1"] <= B["v2"]["H1"]: ba.append("H1")
    if m["H2"] <= B["v2"]["H2"]: ba.append("H2")
    if m["MaxDD"] < B["v2"]["MaxDD"]: ba.append("DD")
    bb = []
    if m["H1"] <= B["spy"]["H1"]: bb.append("H1")
    if m["H2"] <= B["spy"]["H2"]: bb.append("H2")
    if metrics(r.loc[OOS_START:])["Sharpe"] <= B["spy_oos"]["Sharpe"]: bb.append("OOS")
    if m["MaxDD"] < 0.60 * B["spy"]["MaxDD"]: bb.append("DD")
    if m["CAGR"] < 0.70 * B["spy"]["CAGR"]: bb.append("CAGR")
    return m, ba, bb


SER = {}
rows = []
P(f"\n  {'panel':<10}{'side':>5}{'q':>6}{'cad':>5}{'bps':>5}{'CAGR':>9}{'Sharpe':>8}{'MaxDD':>8}"
  f"{'H1':>7}{'H2':>7}{'OOS Sh':>8}{'trn/yr':>8}  {'4a':<16}{'4b'}")
for p in PANELS:
    pxp, tc, st = PX[p], TCOLS[p], START[p]
    for side in ("LOW", "HIGH"):
        for q in QGRID:
            w = side_weights(pxp, tc, q, side)
            for cad in HGRID:
                gr, tn = fast_bt(pxp, w, cad)
                gr, tn = gr.loc[st:], tn.loc[st:]
                SER[(p, side, q, cad)] = (gr, tn)
                typ = float(tn.sum() / (len(tn) / 252.0))
                for c in COSTS:
                    r = net(gr, tn, c)
                    m, ba, bb = verdicts(p, r)
                    oos = metrics(r.loc[OOS_START:])["Sharpe"]
                    row = dict(panel=p, side=side, q=q, cadence=cad, bps=c, CAGR=m["CAGR"],
                               Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m["H1"], H2=m["H2"],
                               OOS_Sharpe=oos, turn_yr=typ,
                               path4a="KEEP" if not ba else "KILL(" + ",".join(ba) + ")",
                               path4b="KEEP" if not bb else "KILL(" + ",".join(bb) + ")")
                    rows.append(row)
                    if c == PROTO_COST:
                        P(f"  {p:<10}{side:>5}{q:>6.2f}{cad:>5}{c:>5}{m['CAGR']:>9.2%}{m['Sharpe']:>8.3f}"
                          f"{m['MaxDD']:>8.1%}{m['H1']:>7.3f}{m['H2']:>7.3f}{oos:>8.3f}{typ:>8.2f}  "
                          f"{row['path4a']:<16}{row['path4b']}")
G = pd.DataFrame(rows)
G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
G.to_csv(OUT / f"{STEM}.verdicts.csv", index=False)
n = len(G)
P(f"\n  grid n={n} points (3 panels x 2 sides x {len(QGRID)} q x {len(HGRID)} cadences x {len(COSTS)} costs), ALL reported")
P(f"  4a KEEP {(G.path4a=='KEEP').sum()}/{n};  4b KEEP {(G.path4b=='KEEP').sum()}/{n};"
  f"  BOTH {((G.path4a=='KEEP')&(G.path4b=='KEEP')).sum()}/{n}")
fb = pd.Series([x for s in G.path4b for x in (s[5:-1].split(",") if s.startswith("KILL") else [])]).value_counts()
P(f"  binding bars (4b): " + ", ".join(f"{k} {v}" for k, v in fb.items()))
fa = pd.Series([x for s in G.path4a for x in (s[5:-1].split(",") if s.startswith("KILL") else [])]).value_counts()
P(f"  binding bars (4a): " + ", ".join(f"{k} {v}" for k, v in fa.items()))
P("\n  LOW minus HIGH at 10 bps, matched (panel, q, cadence) — the channel priced as a book:")
d10 = G[G.bps == PROTO_COST]
for p in PANELS:
    a = d10[(d10.panel == p) & (d10.side == "LOW")].set_index(["q", "cadence"])
    b = d10[(d10.panel == p) & (d10.side == "HIGH")].set_index(["q", "cadence"])
    dc, ds = (a.CAGR - b.CAGR), (a.Sharpe - b.Sharpe)
    P(f"    {p:<10} dCAGR mean {dc.mean()*100:+.2f} pp (positive {int((dc>0).sum())}/{len(dc)}),"
      f" dSharpe mean {ds.mean():+.4f} (positive {int((ds>0).sum())}/{len(ds)})")

# ================================================================== Q6  RULE 8
P("\n" + "-" * 118)
P("Q6  PROTOCOL RULE 8 — (q, cadence) chosen on 2010-2016 IS Sharpe, 2017-2026 read ONCE")
P("-" * 118)
wf = []
for p in PANELS:
    for side in ("LOW", "HIGH"):
        best, bs = None, -np.inf
        for q in QGRID:
            for cad in HGRID:
                gr, tn = SER[(p, side, q, cad)]
                s = metrics(net(gr, tn, PROTO_COST).loc[:IS_END])["Sharpe"]
                if s > bs:
                    bs, best = s, (q, cad)
        q, cad = best
        gr, tn = SER[(p, side, q, cad)]
        r = net(gr, tn, PROTO_COST)
        o = metrics(r.loc[OOS_START:])
        B = BENCH[p]
        # OOS-only 4b bars, against SPY OOS
        oos_bad = []
        if o["Sharpe"] <= B["spy_oos"]["Sharpe"]: oos_bad.append("Sharpe")
        if o["MaxDD"] < 0.60 * B["spy_oos"]["MaxDD"]: oos_bad.append("DD")
        if o["CAGR"] < 0.70 * B["spy_oos"]["CAGR"]: oos_bad.append("CAGR")
        wf.append(dict(panel=p, side=side, pick_q=q, pick_cad=cad, IS_Sharpe=bs,
                       OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"],
                       base_OOS_Sharpe=B["v2_oos"]["Sharpe"], base_OOS_CAGR=B["v2_oos"]["CAGR"],
                       base_OOS_MaxDD=B["v2_oos"]["MaxDD"],
                       spy_OOS_CAGR=B["spy_oos"]["CAGR"], spy_OOS_Sharpe=B["spy_oos"]["Sharpe"],
                       spy_OOS_MaxDD=B["spy_oos"]["MaxDD"],
                       oos4b="PASS" if not oos_bad else "FAIL(" + ",".join(oos_bad) + ")"))
WF = pd.DataFrame(wf)
WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
P(f"  {'panel':<10}{'side':>5}{'pick':>10}{'IS Sh':>8}{'OOS CAGR':>10}{'OOS Sh':>8}{'OOS DD':>9}"
  f"{'base Sh':>9}{'SPY CAGR':>10}{'SPY Sh':>8}{'SPY DD':>9}  4b-OOS")
for _, r in WF.iterrows():
    P(f"  {r.panel:<10}{r.side:>5}{f'q{r.pick_q:.2f}/{r.pick_cad}':>10}{r.IS_Sharpe:>8.3f}"
      f"{r.OOS_CAGR:>10.2%}{r.OOS_Sharpe:>8.3f}{r.OOS_MaxDD:>9.1%}{r.base_OOS_Sharpe:>9.3f}"
      f"{r.spy_OOS_CAGR:>10.2%}{r.spy_OOS_Sharpe:>8.3f}{r.spy_OOS_MaxDD:>9.1%}  {r.oos4b}")
P(f"\n  rule-8 OOS 4b passes: {(WF.oos4b=='PASS').sum()}/{len(WF)}")
P(f"  LOW beats its own HIGH control OOS on Sharpe in "
  f"{int(sum(WF[(WF.side=='LOW')].set_index('panel').OOS_Sharpe > WF[(WF.side=='HIGH')].set_index('panel').OOS_Sharpe))}"
  f"/{len(PANELS)} panels")

# ------------------------------------------------------------------ VERDICT
P("\n" + "=" * 118)
P("VERDICT")
P("=" * 118)
n4a = int((G.path4a == "KEEP").sum())
n4b = int((G.path4b == "KEEP").sum())
P(f"  4a {n4a}/{n}, 4b {n4b}/{n}, rule-8 OOS 4b {(WF.oos4b=='PASS').sum()}/{len(WF)}"
  f"  ->  {'KEEP-candidate' if (n4b and (WF.oos4b=='PASS').any()) else 'KILL (no KEEP on either path)'}")
P(f"  645 asked whether the eject-after-a-fall channel exists off SMALL439.")
P(f"    SMALL439 mean forward gap {sm:+.2%};  U56+broad136 {off:+.2%}.")
P(f"    The split is an EXACT price-level cut (Q1), not a path event (Q2: event carries {abs(g_ev/g_vol):.0%}).")
P(f"  [{time.time()-T0:.0f}s]")

(OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
print(f"\nwrote {STEM}.{{console.txt,gates,identity,levelvsevent,offpanel,gaps,tails,era,grid,verdicts,walkforward}}")
