#!/usr/bin/env python3
"""QUEUE idea 395 — does-the-sleeve-earn-anything-over-its-own-de-grossed-control  (lane B, 2026-09-10).

QUESTION.  Idea 135's only 4a candidates against the live RULES v2 are 23 broad-panel SLEEVE
rows, and `SLV50/control` (no overlay, the equity book de-grossed to 0.53) is one of them: the
OVERLAY earns nothing over its own exposure.  Idea 395 asks the next question up — price the
SLEEVE ITSELF the same way.  Is the macro sleeve an INSTRUMENT (it earns something a pure
exposure dial on the same equity book cannot) or is it just ANOTHER EXPOSURE DIAL, in which
case ideas 105/106 must not write it into RULES.

PRE-REGISTERED HYPOTHESIS (H395).  For every cell, the sleeve arm SLV_f beats BOTH of its own
equity-only controls — the same equity book de-grossed to SLV_f's realised MEAN GROSS, and the
same equity book de-grossed to SLV_f's realised MAX DRAWDOWN — on Sharpe, in both halves and
out of sample.  Falsified if the matched controls win, or if the win is confined to one cost
rung / one panel.

CONSTRUCTION (idea 133's `_base`/`book_targets` semantics, re-derived here, not re-typed from
a chain of five importers, so the file is standalone and readable):
    EQ_ung   equal weight over every priced name, gross 0.75, NO gate   (record `control`)
    EQ_band  the same book gated by RULES v2's 200d +/-3% band, de-gross convention
             (gated-out weight -> CASH, never re-spread) — the LIVE book's shape
    SLV_f    (1 - f) * EQ_base  +  f * sleeve,  sleeve normalised to gross 0.75 and NOT gated
             (idea 133 states the sleeve leg is ungated; kept verbatim so the arm is the
             record's arm, which is the whole point of the comparison)
    sleeve   idea 18 variant B / ideas 100/102/104: trend-vote over {12-1m, 6m, 3m} x 60d
             inverse-vol risk parity over the sleeve assets
    CTL_mg(f)  lambda * EQ_ctl  with lambda solved so mean realised gross matches SLV_f
    CTL_dd(f)  lambda * EQ_ctl  with lambda solved so MaxDD matches SLV_f
The control's own base EQ_ctl is a REPORTED AXIS with two settings, because they answer two
different questions and idea 135 only ran the first:
    ctl_base = EQ_ung   "hold less of the fully-invested equity book" — idea 135's `control`,
                        the ladder the record actually de-grossed to 0.53.  lambda <= 1 here,
                        so this control never uses leverage.
    ctl_base = same     the arm's OWN base, gate included — isolates the SLEEVE from the GATE.
                        On the gated base this needs lambda > 1 (the ungated sleeve leg lifts
                        realised gross above the gated book's), i.e. LEVERAGE, which PROTOCOL
                        rule 2 forbids in a proposed book; it is used here only as an analytic
                        control and every lambda > 1 row is flagged, never promoted.
Both controls are REAL PATHS, not linear rescalings: the simulator drifts holdings between
rebalances against a zero-yielding cash residual, so lambda * W does not give lambda * r
(idea 135 note (c)).  Verified numerically below (G2).

TUNED PARAMETERS (2, the protocol maximum; every grid point reported, none selected on):
    1. f       sleeve fraction  in {0.10, 0.25, 0.40, 0.50, 0.60, 0.75}
    2. sleeve  asset set        in {S3 = TLT/GLD/UUP, S4 = TLT/GLD/DBC/UUP}
REPORTED AXES, never selected on:
    panel {u56, broad136} x base book {EQ_ung, EQ_band} x cost {0, 10, 25} bps x cadence {W, M}
    x control base {EQ_ung, same}
    => 6 x 2 x 2 x 2 x 3 x 2 = 288 sleeve arms, each with 4 matched controls, all reported.
The verdict is quoted at the PROTOCOL rung: cost 10 bps, weekly, panel u56, base EQ_band
(the live book's shape).  Every other rung is printed beside it.

BARS.  Rule 4a against COST-MATCHED RULES v2 (the live book) and, for continuity with the
pre-2026-09-06 record, RULES v1.  Rule 4b against SPY: Sharpe > SPY in both halves AND out of
sample, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's.  Rule 8 walk-forward: (f, sleeve) chosen
on 2009-2016 by IS Sharpe alone, evaluated untouched on 2017-2026.

GATES (all asserted, failures printed not swallowed):
    G1  the cost identity  r(c) = r(0) - turnover * c/1e4  vs `engine.backtest` at 10 bps
    G2  lambda * W is NOT lambda * r (the ladder is a real path, idea 135 note (c))
    G3  the sleeve construction reproduces idea 102's committed S4 asset list and the
        sleeve leg's own gross
    G4  monotonicity of MaxDD and mean gross in lambda, which is what makes the two matches
        well-posed; non-monotone cells are reported, not silently interpolated

KNOWN LIMITS.  The sleeve is 3-4 ETFs over ONE macro regime (2008-2026: one secular bond bull
into one bond bear) — idea 139 risk (a) applies in full and no amount of cross-panel work
fixes it, because the sleeve leg is the SAME four tickers on both panels.  Both panels are
current constituents (PROTOCOL rule 9 survivorship).  u56's price cache is rewritten by
daily-close commits, so cross-run reproduction on u56 holds only to ~1e-5 (idea 401 defect).

Deterministic, standalone.  Modifies nothing.  Writes .console.txt, .grid.csv, .match.csv,
.ladder.csv, .keeppaths.csv, .walkforward.csv next to itself.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-10_does-the-sleeve-earn-anything-over-its-own-de-grossed-control_B"
OUT = ROOT / "research" / "backtests"

GROSS = 0.75
BAND = 0.03
IS_END, OOS_START = "2016-12-31", "2017-01-01"
FS = [0.10, 0.25, 0.40, 0.50, 0.60, 0.75]                 # tuned parameter 1
SLEEVES = {"S3": ["TLT", "GLD", "UUP"], "S4": ["TLT", "GLD", "DBC", "UUP"]}   # tuned parameter 2
COSTS = [0.0, 10.0, 25.0]
FREQS = ["W", "M"]
BASES = ["EQ_ung", "EQ_band"]
PANELS = ["u56", "broad"]
C_PROTO, FREQ_PROTO, BASE_PROTO, PANEL_PROTO = 10.0, "W", "EQ_band", "u56"
PHI, DELTA = 0.70, 0.60                                   # 4b CAGR floor / DD cap vs SPY
LAM = np.round(np.arange(0.02, 1.3005, 0.005), 4)         # de-gross ladder for the controls

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 3000)
LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# --------------------------------------------------------------------- books --
def _ew(px, gate=None):
    """Equal weight over priced names at gross GROSS; gated-out weight -> CASH (de-gross)."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    W = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return W if gate is None else W.where(gate, 0.0)


def _sleeve(px, assets):
    """Ideas 18B/100/102/104: trend-vote x 60d inverse-vol risk parity, normalised to GROSS."""
    sub = px[assets]
    sig = [sub.shift(21) / sub.shift(252) - 1, sub / sub.shift(126) - 1, sub / sub.shift(63) - 1]
    vote = sum((s > 0).astype(float).where(s.notna()) for s in sig) / len(sig)
    inv = 1.0 / sub.pct_change().rolling(60).std().replace(0.0, np.nan)
    rp = inv.div(inv.sum(axis=1), axis=0)
    raw = (vote * rp).fillna(0.0)
    tot = raw.sum(axis=1)
    raw = GROSS * raw.div(tot.where(tot > 1e-12), axis=0).fillna(0.0)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[assets] = raw
    return out


def sleeve_book(eq_W, sl_W, f):
    return (1 - f) * eq_W + f * sl_W


# ---------------------------------------------------------------- simulator ---
def run(px, W, freq):
    """engine.backtest's loop in numpy: drifting holdings, zero-yield cash residual.
    Returns GROSS-of-cost returns, per-day turnover and realised (drifted) gross, so every
    cost rung is priced exactly as r(0) - turnover * c/1e4 (gate G1)."""
    rets = px.pct_change().fillna(0.0).values
    tgt = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n, m = rets.shape
    cur = np.zeros(m)
    held = np.zeros((n, m))
    turn = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = tgt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    idx = px.index
    return (pd.Series((held * rets).sum(axis=1), index=idx),
            pd.Series(turn, index=idx),
            pd.Series(held.sum(axis=1), index=idx))


def priced(r0, turn, c):
    return r0 - turn * c / 1e4


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def stats(r):
    m, mo = metrics(r), metrics(r.loc[OOS_START:])
    h1, h2 = halves(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], Calmar=m["Calmar"],
                H1=h1, H2=h2, IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])


# ================================================================== load ======
say(f"# idea 395 — does the sleeve earn anything over its own de-grossed control   [{STEM}]")
say("")
PX = {}
for pk in PANELS:
    px = load_universe(broad=(pk == "broad"))
    PX[pk] = px
    say(f"panel {pk:6s} {px.shape[0]} rows x {px.shape[1]} cols  "
        f"{px.index[0].date()} -> {px.index[-1].date()}")
START = {pk: PX[pk].index[260] for pk in PANELS}          # protocol warm-up skip
say(f"eval start (index 260): " + ", ".join(f"{pk} {START[pk].date()}" for pk in PANELS))
say(f"IS <= {IS_END}   OOS >= {OOS_START}")
say("")

# ================================================================== gates =====
say("## GATES")
_px = PX["u56"]
_W = _ew(_px, band_state(_px, BAND))
_r0, _to, _gr = run(_px, _W, "W")
_eng = backtest(_px, _W, cost_bps=10.0, freq="W")["returns"]
_d = float((priced(_r0, _to, 10.0) - _eng).abs().max())
say(f"G1 cost identity vs engine.backtest @10bps: max|d| = {_d:.3e}  "
    f"-> {'PASS' if _d < 1e-12 else 'FAIL'}")
_r0h, _toh, _ = run(_px, 0.5 * _W, "W")
_lin = float((_r0h - 0.5 * _r0).abs().max())
say(f"G2 ladder non-linearity: max|r(0.5W) - 0.5 r(W)| = {_lin:.3e}  "
    f"-> {'PASS (real path)' if _lin > 1e-8 else 'FAIL (would be a rescaling)'}")
_sl = _sleeve(_px, SLEEVES["S4"])
_nz = sorted(_sl.columns[_sl.abs().sum() > 0])
_slg = _sl.sum(axis=1).loc[START["u56"]:]
say(f"G3 sleeve legs = {_nz}  (idea 102 S4 = {SLEEVES['S4']})  "
    f"-> {'PASS' if _nz == sorted(SLEEVES['S4']) else 'FAIL'};  "
    f"sleeve gross mean {_slg.mean():.4f} max {_slg.max():.4f} (target {GROSS})")
say("")

# ================================================ de-gross ladders (controls) =
say("## LADDERS — the equity-only book scaled by lambda, one real path per rung")
LAD = {}            # (panel, base, freq, c) -> DataFrame indexed by lambda
LADROWS = []
for pk in PANELS:
    px = PX[pk]
    gate = band_state(px, BAND)
    for bk in BASES:
        Wb = _ew(px, None if bk == "EQ_ung" else gate)
        for fq in FREQS:
            rs, ts, gs = {}, {}, {}
            for lam in LAM:
                r0, to, gr = run(px, lam * Wb, fq)
                rs[lam], ts[lam], gs[lam] = r0, to, gr
            for c in COSTS:
                rows = []
                for lam in LAM:
                    r = priced(rs[lam], ts[lam], c).loc[START[pk]:]
                    m = metrics(r)
                    rows.append(dict(lam=lam, mg=float(gs[lam].loc[START[pk]:].mean()),
                                     Sharpe=m["Sharpe"], CAGR=m["CAGR"], MaxDD=m["MaxDD"],
                                     Calmar=m["Calmar"]))
                L = pd.DataFrame(rows).set_index("lam")
                LAD[(pk, bk, fq, c)] = L
                mono_dd = bool((L.MaxDD.diff().dropna() <= 1e-12).all())   # MaxDD falls with lam
                mono_mg = bool((L.mg.diff().dropna() >= -1e-12).all())
                LADROWS.append(dict(panel=pk, base=bk, freq=fq, cost=c,
                                    mg_lo=L.mg.iloc[0], mg_hi=L.mg.iloc[-1],
                                    dd_lo=L.MaxDD.iloc[0], dd_hi=L.MaxDD.iloc[-1],
                                    sharpe_at_lam1=float(L.Sharpe.reindex([1.0]).iloc[0]),
                                    sharpe_spread=float(L.Sharpe.max() - L.Sharpe.min()),
                                    mono_MaxDD=mono_dd, mono_meangross=mono_mg))
LADF = pd.DataFrame(LADROWS)
say(LADF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
say(f"G4 monotone in lambda: MaxDD {int(LADF.mono_MaxDD.sum())}/{len(LADF)}, "
    f"mean gross {int(LADF.mono_meangross.sum())}/{len(LADF)} cells")
say(f"    the ladder's OWN Sharpe spread across lambda in [0.02, 1.30] is "
    f"{LADF.sharpe_spread.min():.4f}-{LADF.sharpe_spread.max():.4f} — de-grossing is nearly "
    f"Sharpe-neutral, so a matched-gross control is close to a matched-SHARPE control and the "
    f"sleeve has to earn its keep on Sharpe, not on exposure.")
say("")


def invert(L, col, target):
    """Monotone interpolation of the LADDER for a starting lambda with L[col](lambda)=target."""
    x = L[col].values.astype(float)
    lams = L.index.values.astype(float)
    if x[-1] < x[0]:                                       # decreasing (MaxDD)
        x, lams = x[::-1], lams[::-1]
    return float(np.clip(np.interp(target, x, lams), LAM[0], LAM[-1]))


def match(px, Wc, L, col, target, fq, c, t0, tol=1e-6, iters=4):
    """Solve lambda so the SIMULATED control matches `target` on `col`, starting from the
    ladder's interpolation and refining by secant on real simulations.  Returns the accepted
    lambda, its simulated paths, the realised value and the residual — the residual is always
    published, so a match that failed is visible rather than assumed."""
    def ev(lam):
        r0, to, gr = run(px, lam * Wc, fq)
        r = priced(r0, to, c).loc[t0:]
        v = float(gr.loc[t0:].mean()) if col == "mg" else float(metrics(r)["MaxDD"])
        return v, (r0, to, gr)
    la = invert(L, col, target)
    va, pa = ev(la)
    best = (abs(va - target), la, va, pa)
    lb = float(np.clip(la * (1.02 if abs(va - target) > tol else 1.0), LAM[0], LAM[-1]))
    if lb == la:
        return best[1], best[3], best[2], best[0]
    vb, pb = ev(lb)
    for _ in range(iters):
        if abs(vb - target) < best[0]:
            best = (abs(vb - target), lb, vb, pb)
        if best[0] < tol or abs(vb - va) < 1e-15:
            break
        ln = lb - (vb - target) * (lb - la) / (vb - va)
        ln = float(np.clip(ln, LAM[0], LAM[-1]))
        if abs(ln - lb) < 1e-9:
            break
        la, va, lb = lb, vb, ln
        vb, pb = ev(lb)
    if abs(vb - target) < best[0]:
        best = (abs(vb - target), lb, vb, pb)
    return best[1], best[3], best[2], best[0]


# ================================================================== grid ======
say("## GRID — every sleeve arm and its two matched equity-only controls")
BENCH, ROWS, MROWS = {}, [], []
for pk in PANELS:
    px = PX[pk]
    gate = band_state(px, BAND)
    spy = px["SPY"].pct_change().fillna(0.0)
    for fq in FREQS:
        for c in COSTS:
            v2 = priced(*run(px, rules_v2_weights(px), fq)[:2], c).loc[START[pk]:]
            v1 = priced(*run(px, rules_v1_weights(px), fq)[:2], c).loc[START[pk]:]
            BENCH[(pk, fq, c)] = dict(v2=stats(v2), v1=stats(v1), spy=stats(spy.loc[START[pk]:]))
    SL = {sk: _sleeve(px, av) for sk, av in SLEEVES.items()}
    WBASE = {"EQ_ung": _ew(px, None), "EQ_band": _ew(px, gate)}
    for bk in BASES:
        Wb = WBASE[bk]
        for fq in FREQS:
            sims = {}
            for sk in SLEEVES:
                for f in FS:
                    sims[(sk, f)] = run(px, sleeve_book(Wb, SL[sk], f), fq)
            base_sim = run(px, Wb, fq)
            for c in COSTS:
                b_r = priced(base_sim[0], base_sim[1], c).loc[START[pk]:]
                b_st = stats(b_r)
                b_st.update(panel=pk, base=bk, freq=fq, cost=c, arm="BASE", sleeve="-", f=0.0,
                            ctl_base="-",
                            mean_gross=float(base_sim[2].loc[START[pk]:].mean()),
                            turn_yr=float(base_sim[1].loc[START[pk]:].sum() /
                                          metrics(b_r)["Years"]), lam=1.0)
                ROWS.append(b_st)
                for sk in SLEEVES:
                    for f in FS:
                        r0, to, gr = sims[(sk, f)]
                        r = priced(r0, to, c).loc[START[pk]:]
                        st = stats(r)
                        mg = float(gr.loc[START[pk]:].mean())
                        st.update(panel=pk, base=bk, freq=fq, cost=c, arm="SLV", sleeve=sk, f=f,
                                  ctl_base="-", mean_gross=mg,
                                  turn_yr=float(to.loc[START[pk]:].sum() / metrics(r)["Years"]),
                                  lam=np.nan)
                        ROWS.append(st)
                        for cb in ("EQ_ung", "same"):
                            cbk = bk if cb == "same" else "EQ_ung"
                            L = LAD[(pk, cbk, fq, c)]
                            Wc = WBASE[cbk]
                            for kind, col, tgt in (("CTL_mg", "mg", mg),
                                                   ("CTL_dd", "MaxDD", st["MaxDD"])):
                                lam, paths, got, res = match(px, Wc, L, col, tgt, fq, c,
                                                             START[pk])
                                rc0, tc, gc = paths
                                rc = priced(rc0, tc, c).loc[START[pk]:]
                                cst = stats(rc)
                                cst.update(panel=pk, base=bk, freq=fq, cost=c, arm=kind,
                                           sleeve=sk, f=f, ctl_base=cb,
                                           mean_gross=float(gc.loc[START[pk]:].mean()),
                                           turn_yr=float(tc.loc[START[pk]:].sum() /
                                                         metrics(rc)["Years"]), lam=lam)
                                ROWS.append(cst)
                                MROWS.append(dict(
                                    panel=pk, base=bk, freq=fq, cost=c, sleeve=sk, f=f,
                                    ctl_base=cb, kind=kind, lam=lam, levered=bool(lam > 1.0),
                                    target=tgt, realised=got, resid=res,
                                    d_Sharpe=st["Sharpe"] - cst["Sharpe"],
                                    d_H1=st["H1"] - cst["H1"], d_H2=st["H2"] - cst["H2"],
                                    d_OOS=st["OOS_Sharpe"] - cst["OOS_Sharpe"],
                                    d_CAGR=st["CAGR"] - cst["CAGR"],
                                    d_MaxDD=st["MaxDD"] - cst["MaxDD"],
                                    d_Calmar=st["Calmar"] - cst["Calmar"]))
G = pd.DataFrame(ROWS)
M = pd.DataFrame(MROWS)
say(f"grid rows: {len(G)} ({int((G.arm == 'SLV').sum())} sleeve arms, "
    f"{int((G.arm == 'CTL_mg').sum())} matched-gross controls, "
    f"{int((G.arm == 'CTL_dd').sum())} matched-DD controls, "
    f"{int((G.arm == 'BASE').sum())} un-scaled bases)")
say(f"match quality: |resid| mean {M.resid.mean():.3e} max {M.resid.max():.3e} "
    f"(CTL_mg {M[M.kind=='CTL_mg'].resid.max():.3e}, CTL_dd {M[M.kind=='CTL_dd'].resid.max():.3e}); "
    f"lambda range {M.lam.min():.3f}-{M.lam.max():.3f}, "
    f"clipped at a ladder end in {int(((M.lam <= LAM[0]+1e-9) | (M.lam >= LAM[-1]-1e-9)).sum())} "
    f"of {len(M)}; lambda>1 (LEVERED control, analytic only) in "
    f"{int(M.levered.sum())} of {len(M)} — "
    f"{int(M[M.ctl_base=='EQ_ung'].levered.sum())} on ctl_base=EQ_ung, "
    f"{int(M[M.ctl_base=='same'].levered.sum())} on ctl_base=same")
say("")

# ================================================== the question, at the rung =
say("## Q1 — THE PROTOCOL RUNG   panel u56, base EQ_band (the live shape), 10 bps, weekly")
q = G[(G.panel == PANEL_PROTO) & (G.base == BASE_PROTO) & (G.cost == C_PROTO) &
      (G.freq == FREQ_PROTO)]
say(q[["arm", "ctl_base", "sleeve", "f", "lam", "mean_gross", "turn_yr", "CAGR", "Sharpe",
       "MaxDD", "Calmar", "H1", "H2", "OOS_Sharpe"]]
    .sort_values(["sleeve", "f", "arm", "ctl_base"])
    .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
say("")
say("## Q2 — SLEEVE minus its OWN matched control (d>0 = the sleeve earns something)")
for kind in ("CTL_mg", "CTL_dd"):
  for cb in ("EQ_ung", "same"):
    sub = M[(M.kind == kind) & (M.ctl_base == cb)]
    say(f"### {kind} @ ctl_base={cb}   "
        f"({'matched mean gross' if kind == 'CTL_mg' else 'matched MaxDD'})   n = {len(sub)}")
    for col in ("d_Sharpe", "d_H1", "d_H2", "d_OOS", "d_Calmar"):
        say(f"  {col:9s} median {sub[col].median():+.4f}  mean {sub[col].mean():+.4f}  "
            f"win {int((sub[col] > 0).sum())}/{len(sub)} = {(sub[col] > 0).mean():.3f}  "
            f"[{sub[col].min():+.4f}, {sub[col].max():+.4f}]")
    both = ((sub.d_H1 > 0) & (sub.d_H2 > 0) & (sub.d_OOS > 0))
    say(f"  H395 (both halves AND OOS): {int(both.sum())}/{len(sub)} = {both.mean():.3f}")
    say("  by cost rung:")
    say("    " + sub.groupby("cost")[["d_Sharpe", "d_Calmar", "d_OOS"]].median()
        .to_string(float_format=lambda x: f"{x:+.4f}").replace("\n", "\n    "))
    say("  by panel x base:")
    say("    " + sub.groupby(["panel", "base"])[["d_Sharpe", "d_Calmar", "d_OOS"]].median()
        .to_string(float_format=lambda x: f"{x:+.4f}").replace("\n", "\n    "))
    say("  by f:")
    say("    " + sub.groupby("f")[["d_Sharpe", "d_Calmar", "d_OOS"]].median()
        .to_string(float_format=lambda x: f"{x:+.4f}").replace("\n", "\n    "))
    say("")
_pr = M[(M.panel == PANEL_PROTO) & (M.base == BASE_PROTO) & (M.cost == C_PROTO) &
        (M.freq == FREQ_PROTO)]
say("at the protocol rung only:")
say(_pr[["sleeve", "f", "kind", "ctl_base", "lam", "resid", "d_Sharpe", "d_H1", "d_H2", "d_OOS",
         "d_CAGR", "d_MaxDD", "d_Calmar"]].sort_values(["kind", "ctl_base", "sleeve", "f"])
    .to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
say("")

# ================================================================ keep paths ==
say("## KEEP PATHS — 4a vs cost-matched RULES v2 (and v1), 4b vs SPY")
KROWS = []
for _, r in G[G.arm == "SLV"].iterrows():
    B = BENCH[(r.panel, r.freq, r.cost)]
    v2, v1, sp = B["v2"], B["v1"], B["spy"]
    k4a_v2 = bool(r.H1 > v2["H1"] and r.H2 > v2["H2"] and r.MaxDD >= v2["MaxDD"])
    k4a_v1 = bool(r.H1 > v1["H1"] and r.H2 > v1["H2"] and r.MaxDD >= v1["MaxDD"])
    k4b = bool(r.H1 > sp["H1"] and r.H2 > sp["H2"] and r.OOS_Sharpe > sp["OOS_Sharpe"]
               and r.MaxDD >= DELTA * sp["MaxDD"] and r.CAGR >= PHI * sp["CAGR"])
    mg = M[(M.panel == r.panel) & (M.base == r.base) & (M.freq == r.freq) &
           (M.cost == r.cost) & (M.sleeve == r.sleeve) & (M.f == r.f)]
    d = {f"beats_{k}_{cb}": bool((mg[(mg.kind == f"CTL_{k}") &
                                     (mg.ctl_base == cb)].d_Sharpe > 0).all())
         for k in ("mg", "dd") for cb in ("EQ_ung", "same")}
    KROWS.append(dict(panel=r.panel, base=r.base, freq=r.freq, cost=r.cost, sleeve=r.sleeve,
                      f=r.f, Sharpe=r.Sharpe, H1=r.H1, H2=r.H2, OOS=r.OOS_Sharpe, CAGR=r.CAGR,
                      MaxDD=r.MaxDD, k4a_v2=k4a_v2, k4a_v1=k4a_v1, k4b=k4b, **d))
K = pd.DataFrame(KROWS)
BEATCOLS = [c for c in K.columns if c.startswith("beats_")]
say(f"4a vs RULES v2: {int(K.k4a_v2.sum())}/{len(K)}   4a vs RULES v1: {int(K.k4a_v1.sum())}/"
    f"{len(K)}   4b vs SPY: {int(K.k4b.sum())}/{len(K)}")
say("by cost rung:")
say(K.groupby("cost")[["k4a_v2", "k4a_v1", "k4b"] + BEATCOLS].sum().to_string())
say("passes that ALSO beat all four of their own matched controls on Sharpe:")
ok = K[(K.k4a_v2 | K.k4b) & K[BEATCOLS].all(axis=1)]
say(f"  {len(ok)} of {len(K)}")
if len(ok):
    say(ok.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
say("")
say("SPY / RULES v2 / RULES v1 bars, per (panel, freq, cost):")
brows = []
for (pk, fq, c), B in BENCH.items():
    for nm in ("v2", "v1", "spy"):
        brows.append(dict(panel=pk, freq=fq, cost=c, bar=nm, **{k: v for k, v in B[nm].items()}))
BR = pd.DataFrame(brows)
say(BR[["panel", "freq", "cost", "bar", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe"]]
    .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
say("")

# ============================================================= walk-forward ===
say("## RULE 8 WALK-FORWARD — (f, sleeve) chosen on 2009-2016 by IS Sharpe, OOS untouched")
WROWS = []
for pk in PANELS:
    for bk in BASES:
        for fq in FREQS:
            for c in COSTS:
                sub = G[(G.panel == pk) & (G.base == bk) & (G.freq == fq) & (G.cost == c) &
                        (G.arm == "SLV")]
                pick = sub.loc[sub.IS_Sharpe.idxmax()]
                B = BENCH[(pk, fq, c)]
                mg = M[(M.panel == pk) & (M.base == bk) & (M.freq == fq) & (M.cost == c) &
                       (M.sleeve == pick.sleeve) & (M.f == pick.f)]
                base = G[(G.panel == pk) & (G.base == bk) & (G.freq == fq) & (G.cost == c) &
                         (G.arm == "BASE")].iloc[0]
                WROWS.append(dict(
                    panel=pk, base=bk, freq=fq, cost=c, pick=f"{pick.sleeve}/f{pick.f:.2f}",
                    IS_Sharpe=pick.IS_Sharpe, OOS_CAGR=pick.OOS_CAGR,
                    OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                    OOS_S_base=base.OOS_Sharpe, OOS_S_v2=B["v2"]["OOS_Sharpe"],
                    OOS_S_spy=B["spy"]["OOS_Sharpe"],
                    OOS_CAGR_base=base.OOS_CAGR, OOS_CAGR_v2=B["v2"]["OOS_CAGR"],
                    OOS_CAGR_spy=B["spy"]["OOS_CAGR"],
                    OOS_DD_v2=B["v2"]["OOS_MaxDD"], OOS_DD_spy=B["spy"]["OOS_MaxDD"],
                    d_OOS_mg_ung=float(mg[(mg.kind == "CTL_mg") &
                                          (mg.ctl_base == "EQ_ung")].d_OOS.iloc[0]),
                    d_OOS_dd_ung=float(mg[(mg.kind == "CTL_dd") &
                                          (mg.ctl_base == "EQ_ung")].d_OOS.iloc[0]),
                    d_OOS_mg_same=float(mg[(mg.kind == "CTL_mg") &
                                           (mg.ctl_base == "same")].d_OOS.iloc[0]),
                    d_OOS_dd_same=float(mg[(mg.kind == "CTL_dd") &
                                           (mg.ctl_base == "same")].d_OOS.iloc[0]),
                    beats_base=bool(pick.OOS_Sharpe > base.OOS_Sharpe),
                    beats_v2=bool(pick.OOS_Sharpe > B["v2"]["OOS_Sharpe"]),
                    beats_spy=bool(pick.OOS_Sharpe > B["spy"]["OOS_Sharpe"])))
W = pd.DataFrame(WROWS)
say(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
say("")
say(f"rule-8 picks: beat their own un-scaled base OOS {int(W.beats_base.sum())}/{len(W)}; "
    f"beat RULES v2 OOS {int(W.beats_v2.sum())}/{len(W)}; beat SPY OOS "
    f"{int(W.beats_spy.sum())}/{len(W)}")
for cc in ("d_OOS_mg_ung", "d_OOS_dd_ung", "d_OOS_mg_same", "d_OOS_dd_same"):
    say(f"rule-8 picks vs their OWN matched control OOS  {cc:14s} "
        f"{int((W[cc] > 0).sum())}/{len(W)}  median {W[cc].median():+.4f}")
say(f"IS-argmax f distribution: " +
    ", ".join(f"{k} x{v}" for k, v in W['pick'].value_counts().items()))
wp = W[(W.panel == PANEL_PROTO) & (W.base == BASE_PROTO) & (W.freq == FREQ_PROTO) &
       (W.cost == C_PROTO)].iloc[0]
say(f"PROTOCOL RUNG rule-8 pick {wp['pick']}: OOS CAGR {wp.OOS_CAGR:.2%} / Sharpe "
    f"{wp.OOS_Sharpe:.3f} / MaxDD {wp.OOS_MaxDD:.2%}  vs base {wp.OOS_CAGR_base:.2%} / "
    f"{wp.OOS_S_base:.3f}  vs RULES v2 {wp.OOS_CAGR_v2:.2%} / {wp.OOS_S_v2:.3f} / "
    f"{wp.OOS_DD_v2:.2%}  vs SPY {wp.OOS_CAGR_spy:.2%} / {wp.OOS_S_spy:.3f} / "
    f"{wp.OOS_DD_spy:.2%}")
say("")

# =================================================================== verdict ==
say("## VERDICT")
KEY = ["panel", "base", "freq", "cost", "sleeve", "f"]
piv = M.assign(pass_all=(M.d_H1 > 0) & (M.d_H2 > 0) & (M.d_OOS > 0)) \
       .groupby(KEY)["pass_all"].all()
say(f"H395 as pre-registered (sleeve > ALL FOUR matched controls in both halves AND OOS): "
    f"{int(piv.sum())} of {len(piv)} arms")
for kind in ("CTL_mg", "CTL_dd"):
    for cb in ("EQ_ung", "same"):
        s = M[(M.kind == kind) & (M.ctl_base == cb)]
        say(f"{kind} @ {cb:7s}: sleeve wins Sharpe {(s.d_Sharpe > 0).mean():.3f} "
            f"(median {s.d_Sharpe.median():+.4f}), Calmar {(s.d_Calmar > 0).mean():.3f} "
            f"(median {s.d_Calmar.median():+.4f}), OOS {(s.d_OOS > 0).mean():.3f} "
            f"(median {s.d_OOS.median():+.4f})")
say(f"4a vs live RULES v2 at 10/25 bps: "
    f"{int(K[(K.cost > 0)].k4a_v2.sum())} of {len(K[K.cost > 0])}; "
    f"4b vs SPY at 10/25 bps: {int(K[(K.cost > 0)].k4b.sum())} of {len(K[K.cost > 0])}")

G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
M.to_csv(OUT / f"{STEM}.match.csv", index=False)
LADF.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
K.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
(OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
say(f"\nwrote {STEM}.{{grid,match,ladder,keeppaths,walkforward}}.csv + .console.txt")
(OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
