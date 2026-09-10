#!/usr/bin/env python3
"""QUEUE idea 395 ADDENDUM — the regime test the main run cannot do  (lane B, 2026-09-10).

The main run (`..._B.py`) finds the macro sleeve is NOT merely an exposure dial: at matched
mean gross and at matched MaxDD it beats its own de-grossed equity control by a median +0.05
Sharpe / +0.09 OOS, and one arm (u56 / EQ_band / weekly / 10 bps / S3 / f=0.25) passes 4a
against cost-matched RULES v2 and is the rule-8 IS pick.

That result has ONE dominant risk and it is not sample size: the sleeve is 3-4 ETFs whose
biggest leg is TLT, over a window that is one secular bond bull (2008-2020) followed by one
bond bear (2022-). Idea 139 risk (a). If the whole edge is the bond bull, the 4a pass is a
regime artefact and the honest verdict is PARK, not KEEP.  This addendum asks that question
three ways, all pre-registered before the numbers were read:

  A1 SUB-PERIOD. Split the OOS decade at the bond turn: 2017-2021 (TLT up) vs 2022-2026
     (TLT down, -), and read the arm and every control in BOTH.  A sleeve that only works
     while bonds rally shows a sign flip here.
  A2 LEG-DROP. Re-run the sleeve with TLT REMOVED (S3-TLT = GLD/UUP, S4-TLT = GLD/DBC/UUP)
     and with each single leg alone.  If the edge survives TLT's removal it is not the bond
     bull; if it is TLT-only it is.
  A3 CALENDAR YEARS. The arm's and RULES v2's yearly returns side by side, so the drawdown
     years the 4a pass rests on are visible rather than summarised.

Fixed at the PROTOCOL rung throughout — u56, EQ_band base, weekly, 10 bps — and at the main
run's rule-8 pick (S3, f=0.25), plus f=0.40 as the neighbouring IS argmax.  NO new tuned
parameter is introduced: the sleeve asset set is the main run's own tuned axis, read at four
extra settings, and every setting is reported.

Deterministic, standalone.  Modifies nothing.  Writes .console.txt, .subperiod.csv,
.legdrop.csv, .years.csv next to itself.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-10_does-the-sleeve-earn-anything-over-its-own-de-grossed-control_B2"
OUT = ROOT / "research" / "backtests"
GROSS, BAND, COST, FREQ = 0.75, 0.03, 10.0, "W"
SETS = {"S3": ["TLT", "GLD", "UUP"], "S4": ["TLT", "GLD", "DBC", "UUP"],
        "S3-TLT": ["GLD", "UUP"], "S4-TLT": ["GLD", "DBC", "UUP"],
        "TLTonly": ["TLT"], "GLDonly": ["GLD"], "DBConly": ["DBC"], "UUPonly": ["UUP"]}
FS = [0.25, 0.40]
SUBS = {"OOS_a 2017-2021": ("2017-01-01", "2021-12-31"),
        "OOS_b 2022-2026": ("2022-01-01", "2026-12-31")}
LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def _ew(px, gate=None):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    W = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return W if gate is None else W.where(gate, 0.0)


def _sleeve(px, assets):
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


def run(px, W, freq=FREQ, c=COST):
    rets = px.pct_change().fillna(0.0).values
    tgt = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n, m = rets.shape
    cur = np.zeros(m)
    held = np.zeros((n, m))
    turn = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            turn[i] = np.abs(tgt[i] - cur).sum()
            cur = tgt[i]
        held[i] = cur
        g = cur * (1 + rets[i])
        t = g.sum() + (1 - cur.sum())
        cur = g / t if t > 0 else cur
    idx = px.index
    return (pd.Series((held * rets).sum(axis=1), index=idx) -
            pd.Series(turn, index=idx) * c / 1e4,
            pd.Series(held.sum(axis=1), index=idx))


px = load_universe()
T0 = px.index[260]
gate = band_state(px, BAND)
Wb = _ew(px, gate)
say(f"# idea 395 ADDENDUM — regime test at the PROTOCOL rung   [{STEM}]")
say(f"panel u56 {px.shape[0]}x{px.shape[1]}  eval {T0.date()} -> {px.index[-1].date()}  "
    f"base EQ_band (== RULES v2 at gross {GROSS}, band {BAND}), {FREQ}, {COST:.0f} bps")
r_base, g_base = run(px, Wb)
r_v2, _ = run(px, rules_v2_weights(px))
d = float((r_base - r_v2).abs().max())
say(f"G5 EQ_band base is bit-identical to baseline.rules_v2_weights: max|d| {d:.3e} "
    f"-> {'PASS' if d < 1e-14 else 'FAIL'}   (so 4a-vs-v2 and 'beats its own base' coincide)")
spy = px["SPY"].pct_change().fillna(0.0)
say("")

# ------------------------------------------------------------------ A1 + A2 ---
say("## A1/A2 — every sleeve asset set x f, full sample and BOTH OOS halves")
rows = []
for sk, av in SETS.items():
    sl = _sleeve(px, av)
    for f in FS:
        r, g = run(px, (1 - f) * Wb + f * sl)
        d = dict(sleeve=sk, f=f, mean_gross=float(g.loc[T0:].mean()))
        for lbl, sli in [("full", (T0, px.index[-1]))] + list(SUBS.items()):
            rr = r.loc[sli[0]:sli[1]]
            bb = r_base.loc[sli[0]:sli[1]]
            m, mb = metrics(rr), metrics(bb)
            d[f"{lbl}|S"] = m["Sharpe"]
            d[f"{lbl}|dS_base"] = m["Sharpe"] - mb["Sharpe"]
            d[f"{lbl}|CAGR"] = m["CAGR"]
            d[f"{lbl}|MaxDD"] = m["MaxDD"]
        rows.append(d)
A = pd.DataFrame(rows)
for lbl in ["full"] + list(SUBS):
    bb = r_base.loc[SUBS[lbl][0]:SUBS[lbl][1]] if lbl != "full" else r_base.loc[T0:]
    ss = spy.loc[SUBS[lbl][0]:SUBS[lbl][1]] if lbl != "full" else spy.loc[T0:]
    mb, ms = metrics(bb), metrics(ss)
    say(f"### {lbl}   base/RULES v2 Sharpe {mb['Sharpe']:.4f} CAGR {mb['CAGR']:.2%} "
        f"MaxDD {mb['MaxDD']:.2%}   |   SPY Sharpe {ms['Sharpe']:.4f} CAGR {ms['CAGR']:.2%} "
        f"MaxDD {ms['MaxDD']:.2%}")
    cols = ["sleeve", "f", "mean_gross", f"{lbl}|S", f"{lbl}|dS_base", f"{lbl}|CAGR",
            f"{lbl}|MaxDD"]
    say(A[cols].to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    say("")
say("A1 verdict — sign of dS_base by sub-period, per set x f:")
sgn = A.assign(a=np.sign(A["OOS_a 2017-2021|dS_base"]), b=np.sign(A["OOS_b 2022-2026|dS_base"]))
say(sgn[["sleeve", "f", "OOS_a 2017-2021|dS_base", "OOS_b 2022-2026|dS_base", "a", "b"]]
    .to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
say(f"    both sub-periods positive: {int(((sgn.a > 0) & (sgn.b > 0)).sum())} of {len(sgn)}; "
    f"sign FLIPS between them: {int((sgn.a * sgn.b < 0).sum())} of {len(sgn)}")
tl = A[A.sleeve.isin(["S3", "S3-TLT", "S4", "S4-TLT"])]
say("A2 verdict — TLT leg-drop, dS_base full / OOS_a / OOS_b:")
say(tl[["sleeve", "f", "full|dS_base", "OOS_a 2017-2021|dS_base", "OOS_b 2022-2026|dS_base"]]
    .to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
say("")

# ----------------------------------------------------------------------- A3 ---
say("## A3 — calendar-year net returns, the rule-8 pick (S3, f=0.25) vs RULES v2 vs SPY")
r_pick, _ = run(px, 0.75 * Wb + 0.25 * _sleeve(px, SETS["S3"]))
Y = pd.DataFrame({"pick_S3_f025": r_pick.loc[T0:], "RULES_v2": r_base.loc[T0:],
                  "SPY": spy.loc[T0:]})
YR = Y.groupby(Y.index.year).apply(lambda x: (1 + x).prod() - 1)
YR["pick_minus_v2"] = YR.pick_S3_f025 - YR.RULES_v2
say(YR.to_string(float_format=lambda x: f"{x:+.2%}"))
say(f"pick beats RULES v2 in {int((YR.pick_minus_v2 > 0).sum())} of {len(YR)} calendar years; "
    f"worst year pick {YR.pick_S3_f025.min():+.2%} vs v2 {YR.RULES_v2.min():+.2%} vs SPY "
    f"{YR.SPY.min():+.2%}")

A.to_csv(OUT / f"{STEM}.subperiod.csv", index=False)
tl.to_csv(OUT / f"{STEM}.legdrop.csv", index=False)
YR.to_csv(OUT / f"{STEM}.years.csv")
(OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
say(f"\nwrote {STEM}.{{subperiod,legdrop,years}}.csv + .console.txt")
(OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
