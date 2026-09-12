#!/usr/bin/env python3
"""Idea 607 (cloud lane, 2026-09-12) — put a CROSSING-COST column on every published TWIN claim.

THE FINDING THIS RUN IS GROUNDED IN.  Idea 605 measured the matched-mean-gross static twin win
rate on a 648-arm corpus over a 15-rung cost ladder and found it monotone in cost (pooled
Spearman -1.000) with the families crossing 0.50 at ABS ~10 bps, QEXP ~20 and QROLL ~50 — i.e.
idea 42's ABS family is already a COIN FLIP at PROTOCOL's own 10-bps rung.  Every "a gate that
fires is not merely a gross dial" claim in the record rests on a twin comparison read at ONE cost
rung.  This run asks what that costs the record: census the committed twin / matched-gross claim
sites, price the crossing cost that applies to each, and report how many were published AT OR
ABOVE their own crossing cost — where the claim they state is no better than a coin flip.

TWO TUNED PARAMETERS, exactly as the queue names them:
  P1  CLAIM SET     — SITES (every matching line in a committed .py/.md under research/backtests),
                      FILES (the file as the unit, its strongest stated rung), LEADERBOARD (the
                      committed leaderboard rows only).  3 readings, all reported.
  P2  COST LADDER   — FINE (0,1,2,3,5,7.5,10,15,20,25,30,40,50,75,100 bps, idea 605's own ladder)
                      and COARSE (0,10,25,50), both reported everywhere.
Panels (U56, B136), families (ABS / QEXP / QROLL), gate level, QROLL lookback, depth, gross and
cadence are REPORTED AXES, never tuned or selected on.

CONVENTIONS, DECLARED BEFORE ANY NUMBER:
  C1  BASE BOOK: EWALL — every scored-eligible name (composite eligibility from baseline.score
      with vol_scale=False, above its 200d MA, vol20 < 0.60) equal-weighted to gross g, residual
      in CASH.  Copied from idea 605/602's `ewall_weights` so the corpus is the same construction.
  C2  GATE: breadth = share of the panel's non-SPY names above their own 200d MA.  A gate FIRES on
      day t when breadth is below its family threshold; on a firing day the book's gross is
      multiplied by (1 - depth).  The multiplier is held on the book's own rebalance calendar
      (mask -> ffill), exactly as idea 605's `breadth_gate_weights` does.
        ABS   breadth < B,                       B in {0.30, 0.40, 0.50}
        QEXP  breadth < expanding quantile q,    q in {0.07, 0.12, 0.17}
        QROLL breadth < rolling-w quantile q,    q in {0.07, 0.12, 0.17}, w in {252, 1008}
  C3  TWIN: the MATCHED-MEAN-GROSS STATIC TWIN — ungated EWALL held at the CONSTANT gross
      g_eff = the gated arm's own realised mean daily gross.  An EWALL book's WEIGHTS are exactly
      g * (e/k), so they are linear in g (gate G2a, bar 1e-15), but its RETURNS are NOT: the
      engine renormalises drifted positions by total NAV including the cash residual, which makes
      the drift path gross-dependent (gate G2b measures the error of the scaling shortcut at
      1.775e-02 on a 0.375/0.617/0.900 grid).  So EVERY twin in this run is a LIVE
      engine.backtest of the EWALL book built at its own g_eff — never a scaled series.
  C4  COST: every arm and twin is run ONCE at 0 bps (engine.backtest, weights decided at close t
      applied at t+1) and every rung is the exact identity r_c = r_0 - turnover * c / 1e4
      (gate G1, bar 1e-12).  No approximation, no overlay convention.
  C5  Scoring starts at px.index[260] (baseline.compare's warm-up) and runs to the panel's last
      close; halves are that window's own row-count halves.
  C6  dSharpe(c) = Sharpe(arm at c) - Sharpe(twin at c).  WIN = dSharpe > 0.
  C7  CROSSING COST c*: per ARM, the linear interpolation on the ladder of the first sign change
      of dSharpe(c); per FAMILY, the same interpolation of the first crossing of win rate 0.50.
      Two censoring classes are counted, never silently dropped (idea 612): NEVERCROSS (dSharpe
      > 0 at 100 bps) and LOSES0 (dSharpe <= 0 already at 0 bps).
  C8  A census SITE's rung is the bps token on its own line; failing that, the file's single
      declared rung; failing that UNSTATED.  PROTOCOL's rung (10 bps) is reported separately and
      never imputed onto an unstated site.

PRE-REGISTERED HYPOTHESES (written before the grid ran; all reported either way):
  H_MONO   the fresh corpus reproduces 605's direction: per-family Spearman(cost, win rate)
           <= -0.80 on the FINE ladder for all three families.
  H_ORDER  the family ordering at 0 bps is QROLL > QEXP > ABS (605's ordering is present before
           any cost is charged).
  H_CROSS  ABS's family crossing cost is <= 15 bps and QROLL's is >= 30 bps on the fresh corpus
           (605 committed ~10 and ~50).
  H_ABOVE  at least 25% of census sites that state a rung state one AT OR ABOVE the crossing cost
           that applies to them.
  H_CENSUS at least half of the census sites state no cost rung on their own line.
  H_ARMDD  the arm-level c* is ORDERED by switch tax: Spearman(mean |dm|, c*) < 0 (a gate that
           moves its dial more crosses sooner), on the arms that cross.
  H_WF     (rule 8) the family crossing cost fitted on IS (<=2016-12-31) alone is within 10 bps
           of the OOS (2017+) reading, for all three families.

GATES (printed before any new number):
  G1  C4's cost identity: derived r_c vs a live engine.backtest at 10 and 25 bps on 12 arms.
  G2  C3's two linearity facts: G2a EWALL weights are exactly linear in gross (bar 1e-15), and
      G2b the engine's cash-residual renormalisation makes RETURNS non-linear in gross — measured,
      and the reason every twin is run live.
  G3  idea 605's COMMITTED .ladder.csv reproduces from its COMMITTED .cells.csv.gz (mean of the
      `win` column by family x rung), bar 1e-12 — the committed corpus this run re-reads is the
      one 605 published.
  G4  RULES v2 LIVE on U56 @10bps reproduces RULES.md's committed 8.63% / 1.202 / -12.05%.
  G5  the vectorised window metrics reproduce engine.metrics (bar 1e-10).

Outputs (all under research/backtests/, all committed):
  .txt            full console log
  .arms.csv       one row per (arm, rung): Sharpe, twin Sharpe, dSharpe, win, g_eff, switch tax
  .cstar.csv      one row per arm: c*, censoring class, family, axes
  .family.csv     the family x rung win-rate ladder and each family's c*, fresh and committed
  .census.csv     every twin/matched-gross claim site with its stated rung and its crossing cost
  .wf.csv         rule 8 on the CLAIM (IS-fitted c*) and on the BOOKS (OOS triples, KEEP paths)
  .result.md      the answer
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Run: python3 research/backtests/2026-09-12_put-a-CROSSING-COST-column-on-every-published-TWIN-claim_cloud.py
"""
from __future__ import annotations
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics, rebalance_mask                          # noqa: E402

DATE = "2026-09-12"
SLUG = "put-a-CROSSING-COST-column-on-every-published-TWIN-claim"
BT = Path(__file__).resolve().parent
OUT = BT / f"{DATE}_{SLUG}_cloud"
FINE = [0.0, 1.0, 2.0, 3.0, 5.0, 7.5, 10.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 75.0, 100.0]
COARSE = [0.0, 10.0, 25.0, 50.0]
LADDERS = {"FINE": FINE, "COARSE": COARSE}                      # P2
PROTO_RUNG = 10.0
MAX_VOL, WARMUP = 0.60, 260
SPLIT = pd.Timestamp("2016-12-31")
OOS_START = pd.Timestamp("2017-01-01")
PANELS = ["U56", "B136"]
CADENCES = ["W", "D"]
DEPTHS = [0.50, 1.00]
GROSSES = [0.75, 1.00]
GATES = ([("ABS", b, None) for b in (0.30, 0.40, 0.50)] +
         [("QEXP", q, None) for q in (0.07, 0.12, 0.17)] +
         [("QROLL", q, w) for q in (0.07, 0.12, 0.17) for w in (252, 1008)])
COMMITTED_605 = BT / "2026-09-10_is-the-TWIN-WIN-RATE-a-SWITCHING-COST-statistic_C"
LOG: list[str] = []
pd.set_option("display.width", 250)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def hdr(s):
    P("\n" + "=" * 110 + f"\n{s}\n" + "=" * 110)


# =====================================================================================
# BOOKS — C1/C2, copied from idea 605/602's committed constructors
# =====================================================================================
def ewall_weights(px, gross=1.00):
    s, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < MAX_VOL)
    e = elig.astype(float).where(px.notna(), 0.0)
    k = e.sum(axis=1).replace(0, np.nan)
    return e.div(k, axis=0).mul(gross).fillna(0.0)


def breadth(px):
    core = px.drop(columns=["SPY"], errors="ignore")
    above = core > core.rolling(200).mean()
    return above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)


def gate_multiplier(px, fam, level, w, depth, freq):
    """C2: 1.0 normally, (1-depth) on a firing day, held on the book's rebalance calendar."""
    b = breadth(px)
    if fam == "ABS":
        thr = pd.Series(level, index=px.index)
    elif fam == "QEXP":
        thr = b.expanding(min_periods=252).quantile(level)
    else:
        thr = b.rolling(w, min_periods=w).quantile(level)
    bad = (b < thr) & b.notna() & thr.notna()
    m = pd.Series(1.0, index=px.index).where(~bad, 1.0 - depth)
    mask = rebalance_mask(px.index, freq)
    return m.where(mask).ffill().fillna(1.0)


def w_metrics(r: np.ndarray):
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    sd = r.std(ddof=1)
    sharpe = (r.mean() * 252.0) / (sd * np.sqrt(252.0)) if sd > 0 else np.nan
    mdd = float(np.min(eq / np.maximum.accumulate(eq) - 1.0))
    return float(cagr), float(sharpe), mdd


def sharpe_of(r: np.ndarray):
    sd = r.std(ddof=1)
    return float((r.mean() * 252.0) / (sd * np.sqrt(252.0))) if sd > 0 else np.nan


def cross_zero(xs, ys):
    """C7: first sign change of y over the x ladder, linearly interpolated.  Returns
    (c_star, class) with class in {CROSS, NEVERCROSS, LOSES0}."""
    ys = np.asarray(ys, float)
    xs = np.asarray(xs, float)
    if not np.isfinite(ys).all():
        return np.nan, "NAN"
    if ys[0] <= 0:
        return 0.0, "LOSES0"
    for i in range(1, len(xs)):
        if ys[i] <= 0:
            y0, y1 = ys[i - 1], ys[i]
            return float(xs[i - 1] + (xs[i] - xs[i - 1]) * y0 / (y0 - y1)), "CROSS"
    return np.nan, "NEVERCROSS"


def cross_half(xs, ws):
    """Family crossing: first crossing of win rate 0.50, interpolated; also the first rung
    strictly below 0.50 (the record's own reading) and a class label.
    BELOW0 = already a coin flip at 0 bps (no crossing cost exists);
    CROSS  = crosses inside the ladder;  NEVER = still above 0.50 at the top rung."""
    ws = np.asarray(ws, float)
    xs = np.asarray(xs, float)
    if ws[0] < 0.50:
        return 0.0, 0.0, "BELOW0"
    for i in range(1, len(xs)):
        if ws[i] < 0.50:
            y0, y1 = ws[i - 1] - 0.50, ws[i] - 0.50
            interp = xs[i - 1] + (xs[i] - xs[i - 1]) * y0 / (y0 - y1) if y0 != y1 else xs[i]
            return float(interp), float(xs[i]), "CROSS"
    return np.nan, np.nan, "NEVER"


def spear(a, b):
    v = pd.concat([pd.Series(a).rank(), pd.Series(b).rank()], axis=1).dropna()
    return float(v.iloc[:, 0].corr(v.iloc[:, 1])) if len(v) > 2 else np.nan


# =====================================================================================
def main():
    t_all = time.time()
    hdr("PANELS")
    px_ = {"U56": load_universe(), "B136": load_universe(broad=True)}
    starts = {k: v.index[WARMUP] for k, v in px_.items()}
    for k, px in px_.items():
        P(f"  {k:5s} {px.shape[0]} x {px.shape[1]}  {px.index[0].date()} .. {px.index[-1].date()}"
          f"   scoring starts {starts[k].date()}")

    # ---------------- ungated EWALL at gross 1.00: the twin generator (C3) ----------------
    hdr("BUILD — the ungated EWALL base (one per panel x cadence) and every gated arm")
    base = {}
    for pan, px in px_.items():
        W1 = ewall_weights(px, 1.00)
        for cad in CADENCES:
            t0 = time.time()
            res = backtest(px, W1, cost_bps=0, freq=cad)
            base[(pan, cad)] = dict(r0=res["returns"], to=res["turnover"], W1=W1)
            P(f"  EWALL g=1.00 {pan:5s} {cad}  ({time.time()-t0:.1f}s)")

    arms = {}
    for pan, px in px_.items():
        for cad in CADENCES:
            for fam, level, w in GATES:
                for depth in DEPTHS:
                    m = gate_multiplier(px, fam, level, w, depth, cad)
                    for g in GROSSES:
                        Wg = base[(pan, cad)]["W1"].mul(g).mul(m, axis=0)
                        res = backtest(px, Wg, cost_bps=0, freq=cad)
                        r0 = res["returns"].loc[starts[pan]:]
                        to = res["turnover"].loc[starts[pan]:]
                        gross_path = Wg.sum(axis=1).loc[starts[pan]:]
                        g_eff = float(gross_path.mean())
                        sw = float(m.diff().abs().fillna(0.0).loc[starts[pan]:].mean())
                        key = (pan, cad, fam, level, w, depth, g)
                        arms[key] = dict(r0=r0, to=to, g_eff=g_eff, switch=sw,
                                         on_share=float((m < 1.0).loc[starts[pan]:].mean()))
    P(f"  built {len(arms)} gated arms "
      f"({len(PANELS)} panels x {len(CADENCES)} cadences x {len(GATES)} gates x "
      f"{len(DEPTHS)} depths x {len(GROSSES)} gross)  [{time.time()-t_all:.0f}s]")

    TWIN_CACHE: dict = {}

    def twin_series(pan, cad, g_eff):
        """C3: a LIVE engine.backtest of ungated EWALL at the constant gross g_eff."""
        k = (pan, cad, round(float(g_eff), 8))
        if k not in TWIN_CACHE:
            W = base[(pan, cad)]["W1"].mul(k[2])
            res = backtest(px_[pan], W, cost_bps=0, freq=cad)
            TWIN_CACHE[k] = (res["returns"].loc[starts[pan]:], res["turnover"].loc[starts[pan]:])
        return TWIN_CACHE[k]

    # ================================ GATES ================================
    hdr("GATES — printed BEFORE any new number")
    grows = []
    # G1 cost identity on 12 arms
    g1 = 0.0
    sample = list(arms.keys())[::max(1, len(arms) // 12)][:12]
    for (pan, cad, fam, level, w, depth, g) in sample:
        px = px_[pan]
        m = gate_multiplier(px, fam, level, w, depth, cad)
        Wg = base[(pan, cad)]["W1"].mul(g).mul(m, axis=0)
        a = arms[(pan, cad, fam, level, w, depth, g)]
        for c in (10.0, 25.0):
            live = backtest(px, Wg, cost_bps=c, freq=cad)["returns"].loc[starts[pan]:]
            g1 = max(g1, float((live - (a["r0"] - a["to"] * c / 1e4)).abs().max()))
    P(f"  G1 cost identity on {len(sample)} arms x (10, 25) bps: max |diff| = {g1:.3e}  "
      f"{'PASS' if g1 <= 1e-12 else 'FAIL'}")
    grows.append(dict(gate="G1_cost_identity", value=g1, bar=1e-12, ok=g1 <= 1e-12))

    # G2a weights linear in gross (exact);  G2b returns are NOT (measured, hence live twins)
    g2a, g2b = 0.0, 0.0
    for pan, px in px_.items():
        W1 = base[(pan, "W")]["W1"]
        for cad in CADENCES:
            for ge in (0.375, 0.617, 0.9):
                g2a = max(g2a, float((ewall_weights(px, ge) - W1.mul(ge)).abs().max().max()))
                live = backtest(px, W1.mul(ge), cost_bps=0, freq=cad)["returns"].loc[starts[pan]:]
                scaled = base[(pan, cad)]["r0"].loc[starts[pan]:] * ge
                g2b = max(g2b, float((live - scaled).abs().max()))
    P(f"  G2a EWALL weights exactly linear in gross, {len(PANELS)}x3 cells: max |diff| = "
      f"{g2a:.3e}  {'PASS' if g2a <= 1e-15 else 'FAIL'}")
    P(f"  G2b the engine's cash-residual renormalisation makes RETURNS non-linear in gross: "
      f"max |r(g) - g*r(1)| = {g2b:.3e} — MEASURED, and the reason every twin in this run is a "
      f"LIVE backtest at its own g_eff, never a scaled series")
    grows.append(dict(gate="G2a_weight_linearity", value=g2a, bar=1e-15, ok=g2a <= 1e-15))
    grows.append(dict(gate="G2b_return_nonlinearity_measured", value=g2b, bar=float("nan"),
                      ok=True))

    # G3 idea 605's committed ladder reproduces from its committed cells
    C605 = pd.read_csv(f"{COMMITTED_605}.cells.csv.gz")
    LAD605 = pd.read_csv(f"{COMMITTED_605}.ladder.csv", index_col=0)
    LAD605.columns = [float(c) for c in LAD605.columns]
    gated = C605[C605.family.isin(["ABS", "QEXP", "QROLL"])]
    rep = gated.pivot_table(index="family", columns="rung", values="win", aggfunc="mean")
    pooled = gated.groupby("rung").win.mean()
    g3 = 0.0
    for fam in ("ABS", "QEXP", "QROLL"):
        for c in LAD605.columns:
            g3 = max(g3, abs(float(rep.loc[fam, c]) - float(LAD605.loc[fam, c])))
    for c in LAD605.columns:
        g3 = max(g3, abs(float(pooled.loc[c]) - float(LAD605.loc["POOLED", c])))
    P(f"  G3 idea 605's committed ladder.csv rebuilt from its committed cells.csv.gz "
      f"({len(gated)} gated rows, {gated.arm.nunique()} arms): max |diff| = {g3:.3e}  "
      f"{'PASS' if g3 <= 1e-12 else 'FAIL'}")
    grows.append(dict(gate="G3_605_ladder", value=g3, bar=1e-12, ok=g3 <= 1e-12))

    # G4 RULES v2
    live = backtest(px_["U56"], rules_v2_weights(px_["U56"], 0.03, 0.75), cost_bps=10,
                    freq="W")["returns"].loc[starts["U56"]:]
    lc, ls, ld = w_metrics(live.values)
    g4 = max(abs(lc - 0.0863), abs(ls - 1.202), abs(ld + 0.1205))
    P(f"  G4 RULES v2 LIVE U56 @10bps {lc:.4%} / {ls:.4f} / {ld:.4%} vs committed "
      f"8.63% / 1.202 / -12.05%: max |d| = {g4:.3e}  {'PASS' if g4 <= 6e-3 else 'FAIL'}")
    grows.append(dict(gate="G4_rules_v2", value=g4, bar=6e-3, ok=g4 <= 6e-3))

    # G5 metrics identity
    g5 = 0.0
    for k in list(arms.keys())[:25]:
        r = arms[k]["r0"] - arms[k]["to"] * 10 / 1e4
        m_ = metrics(r)
        v = w_metrics(r.values)
        g5 = max(g5, abs(v[0] - m_["CAGR"]), abs(v[1] - m_["Sharpe"]), abs(v[2] - m_["MaxDD"]))
    P(f"  G5 w_metrics vs engine.metrics on 25 arms: max |diff| = {g5:.3e}  "
      f"{'PASS' if g5 <= 1e-10 else 'FAIL'}")
    grows.append(dict(gate="G5_metrics", value=g5, bar=1e-10, ok=g5 <= 1e-10))
    pd.DataFrame(grows).to_csv(f"{OUT}.gates.csv", index=False)
    P(f"\n  GATES: {sum(1 for g in grows if g['ok'])} of {len(grows)} PASS")

    # ============== SECTION 1: the arm x rung ladder and every arm's c* ==============
    hdr(f"SECTION 1 — {len(arms)} arms x {len(FINE)} rungs = {len(arms)*len(FINE)} priced cells, "
        "every point reported")
    rows = []
    spy = {p: px_[p]["SPY"].pct_change().fillna(0.0).loc[starts[p]:] for p in PANELS}
    for (pan, cad, fam, level, w, depth, g), a in arms.items():
        tr, tt = twin_series(pan, cad, a["g_eff"])
        for c in FINE:
            r = (a["r0"] - a["to"] * c / 1e4).values
            t = (tr - tt * c / 1e4).values
            ac, ash, add = w_metrics(r)
            tc, tsh, tdd = w_metrics(t)
            rows.append(dict(panel=pan, cadence=cad, family=fam, level=level, w=w, depth=depth,
                             gross=g, rung=c, g_eff=a["g_eff"], switch=a["switch"],
                             on_share=a["on_share"], CAGR=ac, Sharpe=ash, MaxDD=add,
                             twin_CAGR=tc, twin_Sharpe=tsh, twin_MaxDD=tdd,
                             dSharpe=ash - tsh, win=bool(ash > tsh)))
    A = pd.DataFrame(rows)
    A.to_csv(f"{OUT}.arms.csv", index=False)

    cst = []
    for key, sub in A.groupby(["panel", "cadence", "family", "level", "w", "depth", "gross"],
                              dropna=False):
        sub = sub.sort_values("rung")
        for lname, lad in LADDERS.items():
            s = sub[sub.rung.isin(lad)]
            c_, cls = cross_zero(s.rung.values, s.dSharpe.values)
            cst.append(dict(panel=key[0], cadence=key[1], family=key[2], level=key[3], w=key[4],
                            depth=key[5], gross=key[6], ladder=lname, c_star=c_, cls=cls,
                            dSharpe_0=float(s.dSharpe.iloc[0]),
                            dSharpe_10=float(sub[sub.rung == 10.0].dSharpe.iloc[0]),
                            g_eff=float(s.g_eff.iloc[0]), switch=float(s.switch.iloc[0]),
                            on_share=float(s.on_share.iloc[0])))
    CS = pd.DataFrame(cst)
    CS.to_csv(f"{OUT}.cstar.csv", index=False)
    for lname in LADDERS:
        s = CS[CS.ladder == lname]
        P(f"\n  ARM-LEVEL c* on the {lname} ladder ({len(s)} arms): "
          f"CROSS {int((s.cls=='CROSS').sum())}, NEVERCROSS {int((s.cls=='NEVERCROSS').sum())}, "
          f"LOSES0 {int((s.cls=='LOSES0').sum())}")
        P(s.groupby("family").c_star.describe()[["count", "mean", "50%", "min", "max"]]
          .to_string(float_format=lambda x: f"{x:.3f}"))

    # ============== SECTION 2: the family ladder and the crossing costs ==============
    hdr("SECTION 2 — the FAMILY win-rate ladder and the CROSSING COST column")
    fam_rows = []
    for lname, lad in LADDERS.items():
        sub = A[A.rung.isin(lad)]
        for fam in ["ABS", "QEXP", "QROLL"]:
            s = sub[sub.family == fam].groupby("rung").win.mean()
            ci, cr, cl = cross_half(s.index.values, s.values)
            fam_rows.append(dict(source="FRESH", ladder=lname, family=fam, cls=cl, n_arms=
                                 int(sub[sub.family == fam].rung.value_counts().iloc[0]),
                                 win_0=float(s.iloc[0]), win_10=float(s.loc[10.0]) if 10.0 in
                                 s.index else np.nan,
                                 win_25=float(s.loc[25.0]) if 25.0 in s.index else np.nan,
                                 c_star_interp=ci, c_star_firstrung=cr,
                                 rho_cost_win=spear(s.index.values, s.values)))
        s = sub.groupby("rung").win.mean()
        ci, cr, cl = cross_half(s.index.values, s.values)
        fam_rows.append(dict(source="FRESH", ladder=lname, family="POOLED", cls=cl,
                             n_arms=int(sub.rung.value_counts().iloc[0]),
                             win_0=float(s.iloc[0]),
                             win_10=float(s.loc[10.0]) if 10.0 in s.index else np.nan,
                             win_25=float(s.loc[25.0]) if 25.0 in s.index else np.nan,
                             c_star_interp=ci, c_star_firstrung=cr,
                             rho_cost_win=spear(s.index.values, s.values)))
    # the committed 605 corpus, same statistic
    for fam in ["ABS", "QEXP", "QROLL", "POOLED"]:
        s = LAD605.loc[fam]
        ci, cr, cl = cross_half(s.index.values.astype(float), s.values)
        fam_rows.append(dict(source="COMMITTED_605", ladder="FINE", family=fam, cls=cl,
                             n_arms=int(gated.arm.nunique() if fam == "POOLED" else
                                        gated[gated.family == fam].arm.nunique()),
                             win_0=float(s.iloc[0]), win_10=float(s.loc[10.0]),
                             win_25=float(s.loc[25.0]), c_star_interp=ci, c_star_firstrung=cr,
                             rho_cost_win=spear(s.index.values.astype(float), s.values)))
    F = pd.DataFrame(fam_rows)
    F.to_csv(f"{OUT}.family.csv", index=False)
    P(F.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    CSTAR_FRESH = {r.family: r.c_star_firstrung for r in
                   F[(F.source == "FRESH") & (F.ladder == "FINE")].itertuples()}
    CSTAR = {r.family: r.c_star_firstrung for r in
             F[F.source == "COMMITTED_605"].itertuples()}      # the RECORD's own published column
    CSTAR_I = {r.family: r.c_star_interp for r in F[F.source == "COMMITTED_605"].itertuples()}
    P("\n  CROSSING-COST COLUMN, the RECORD's own (idea 605's committed 648-arm corpus, first "
      "rung below a 0.50 win rate): " +
      ", ".join(f"{k} {v:.4g} bps" if np.isfinite(v) else f"{k} never" for k, v in CSTAR.items()))
    P("  CROSSING-COST COLUMN, this run's FRESH corpus (U56/B136, depth >= 0.50, w in "
      "{252, 1008}): " +
      ", ".join(f"{k} {v:.4g} bps" if np.isfinite(v) else f"{k} NEVER crosses inside 100 bps"
                for k, v in CSTAR_FRESH.items()))

    # ---- 2b: ATTRIBUTION, from 605's COMMITTED cells alone (no new backtest): is the published
    # crossing cost a property of the STATISTIC or of the POPULATION it was measured on? ----
    P("\n  SECTION 2b — the published c* re-read on the SUBSET of 605's own committed corpus that "
      "matches this run's population (panel in U56/B136, depth >= 0.50, w in {252, 1008}):")
    sub605 = gated.copy()
    pan_map = {"u56": "U56", "b136": "B136"}
    sub605["pan_norm"] = sub605.panel.astype(str).str.lower().map(
        lambda s: pan_map.get(s, s.upper()))
    # NB: 605's cells write w = 0.0 (not NaN) for the w-free families ABS and QEXP.
    keep = sub605[(sub605.pan_norm.isin(["U56", "B136"])) & (sub605.depth >= 0.50) &
                  (sub605.w.isna() | sub605.w.isin([0.0, 252.0, 1008.0]))]
    att_rows = []
    for fam in ["ABS", "QEXP", "QROLL", "POOLED"]:
        for tag, dd in (("605_ALL", gated), ("605_MATCHED", keep)):
            d = dd if fam == "POOLED" else dd[dd.family == fam]
            if not len(d):
                continue
            s = d.groupby("rung").win.mean()
            ci, cr, cl = cross_half(s.index.values.astype(float), s.values)
            att_rows.append(dict(subset=tag, family=fam, n_arms=int(d.arm.nunique()),
                                 win_0=float(s.iloc[0]), win_10=float(s.loc[10.0]),
                                 win_25=float(s.loc[25.0]), c_star_firstrung=cr, cls=cl,
                                 rho_cost_win=spear(s.index.values.astype(float), s.values)))
    AT = pd.DataFrame(att_rows)
    AT.to_csv(f"{OUT}.attribution.csv", index=False)
    P(AT.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ============== SECTION 3: the census ==============
    hdr("SECTION 3 — CENSUS of every committed TWIN / MATCHED-GROSS claim site, with the "
        "crossing cost that applies to it")
    pat_twin = re.compile(r"twin|matched[-\s]?gross|gross[-\s]?matched", re.I)
    pat_bps = re.compile(r"(\d+(?:\.\d+)?)\s*bps|cost_bps\s*=\s*(\d+(?:\.\d+)?)", re.I)
    pat_fam = re.compile(r"\b(ABS|QEXP|QROLL)\b")
    files = sorted([p for p in BT.glob("*.py")] + [p for p in BT.glob("*.md")])
    sites, file_rows = [], []
    for f in files:
        if f.name.startswith(f"{DATE}_{SLUG}"):
            continue                                   # never census this run's own file
        try:
            txt = f.read_text(errors="ignore")
        except Exception:
            continue
        lines = txt.split("\n")
        fbps = sorted({float(m[0] or m[1]) for m in pat_bps.findall(txt)})
        ffam = sorted(set(pat_fam.findall(txt)))
        n_site = 0
        for ln, line in enumerate(lines, 1):
            if not pat_twin.search(line):
                continue
            n_site += 1
            lb = sorted({float(m[0] or m[1]) for m in pat_bps.findall(line)})
            lf = sorted(set(pat_fam.findall(line)))
            fam = (lf[0] if len(lf) == 1 else (ffam[0] if len(ffam) == 1 else "POOLED"))
            if lb:
                rung, src = max(lb), "LINE"
            elif len(fbps) == 1:
                rung, src = fbps[0], "FILE"
            else:
                rung, src = np.nan, "UNSTATED"
            cs = CSTAR.get(fam, CSTAR["POOLED"])
            csf = CSTAR_FRESH.get(fam, CSTAR_FRESH["POOLED"])
            sites.append(dict(file=f.name, line=ln, family=fam, rung=rung, rung_src=src,
                              c_star=cs, c_star_fresh=csf,
                              c_star_interp=CSTAR_I.get(fam, CSTAR_I["POOLED"]),
                              above_fresh=(bool(rung >= csf) if (np.isfinite(rung) and
                                                                 np.isfinite(csf)) else None),
                              at_or_above=(bool(rung >= cs) if (np.isfinite(rung) and
                                                                np.isfinite(cs)) else None),
                              proto_at_or_above=bool(PROTO_RUNG >= cs) if np.isfinite(cs)
                              else None,
                              text=line.strip()[:220]))
        if n_site:
            fam = ffam[0] if len(ffam) == 1 else "POOLED"
            rung = max(fbps) if fbps else np.nan
            cs = CSTAR.get(fam, CSTAR["POOLED"])
            file_rows.append(dict(file=f.name, n_sites=n_site, family=fam, rung=rung,
                                  c_star=cs,
                                  at_or_above=(bool(rung >= cs) if (np.isfinite(rung) and
                                                                    np.isfinite(cs)) else None)))
    S = pd.DataFrame(sites)
    FR = pd.DataFrame(file_rows)
    S.to_csv(f"{OUT}.census.csv", index=False)
    FR.to_csv(f"{OUT}.censusfiles.csv", index=False)
    lb_rows = []
    lbtxt = (ROOT / "research" / "LEADERBOARD.md").read_text(errors="ignore").split("\n")
    for ln, line in enumerate(lbtxt, 1):
        if line.startswith("|") and pat_twin.search(line):
            lb = sorted({float(m[0] or m[1]) for m in pat_bps.findall(line)})
            lf = sorted(set(pat_fam.findall(line)))
            fam = lf[0] if len(lf) == 1 else "POOLED"
            rung = max(lb) if lb else np.nan
            cs = CSTAR.get(fam, CSTAR["POOLED"])
            lb_rows.append(dict(line=ln, family=fam, rung=rung, c_star=cs,
                                at_or_above=(bool(rung >= cs) if (np.isfinite(rung) and
                                                                  np.isfinite(cs)) else None)))
    LBR = pd.DataFrame(lb_rows)
    LBR.to_csv(f"{OUT}.censusleaderboard.csv", index=False)

    for name, D in (("SITES", S), ("FILES", FR), ("LEADERBOARD", LBR)):                  # P1
        n = len(D)
        stated = int(D.rung.notna().sum())
        above = int((D.at_or_above == True).sum())                                # noqa: E712
        P(f"  {name:12s} n = {n:5d}   state a rung {stated:5d} ({stated/max(n,1):.1%})   "
          f"AT OR ABOVE their crossing cost {above:5d} "
          f"({above/max(stated,1):.1%} of the stating ones)")
    if len(S):
        P("\n  SITES by the rung they state (top rungs):")
        P(S.rung.value_counts(dropna=False).head(12).to_string())
        P("\n  SITES by family attribution: " +
          ", ".join(f"{k} {v}" for k, v in S.family.value_counts().items()))
        P(f"\n  At PROTOCOL's own 10-bps rung, the crossing cost is already reached for: " +
          ", ".join(f"{k}" for k, v in CSTAR.items() if np.isfinite(v) and PROTO_RUNG >= v))
        P("  Example sites at or above their crossing cost (first 8):")
        for r in S[S.at_or_above == True].head(8).itertuples():                   # noqa: E712
            P(f"    {r.file}:{r.line}  [{r.family} rung {r.rung:g} >= c* {r.c_star:g}]  "
              f"{r.text[:120]}")

    # ============== SECTION 4: mechanism + rule 8 ==============
    hdr("SECTION 4 — MECHANISM: does the switch tax order the arm-level crossing cost?")
    sub = CS[(CS.ladder == "FINE") & (CS.cls == "CROSS")]
    rho_sw = spear(sub.switch.values, sub.c_star.values)
    rho_on = spear(sub.on_share.values, sub.c_star.values)
    rho_d0 = spear(sub.dSharpe_0.values, sub.c_star.values)
    P(f"  on {len(sub)} crossing arms: rho(mean |dm| switch, c*) = {rho_sw:+.4f}   "
      f"rho(on_share, c*) = {rho_on:+.4f}   rho(dSharpe at 0 bps, c*) = {rho_d0:+.4f}")
    for fam in ["ABS", "QEXP", "QROLL"]:
        s = sub[sub.family == fam]
        if len(s) > 2:
            P(f"    {fam:6s} n={len(s):3d}  rho(switch, c*) = {spear(s.switch, s.c_star):+.4f}"
              f"   median c* {s.c_star.median():.2f} bps   median switch {s.switch.mean():.5f}")

    hdr("SECTION 5 — PROTOCOL rule 8.  (a) on the CLAIM: the crossing cost fitted on IS "
        "(<=2016-12-31) alone and read ONCE on OOS (2017+).  (b) the MANDATED BOOK leg.")
    wf_rows = []
    for (pan, cad, fam, level, w, depth, g), a in arms.items():
        tr, tt = twin_series(pan, cad, a["g_eff"])
        for wname, sl in (("IS", slice(None, SPLIT)), ("OOS", slice(OOS_START, None))):
            r0, to = a["r0"].loc[sl], a["to"].loc[sl]
            t0, tu = tr.loc[sl], tt.loc[sl]
            for c in FINE:
                r = (r0 - to * c / 1e4).values
                t = (t0 - tu * c / 1e4).values
                wf_rows.append(dict(window=wname, panel=pan, cadence=cad, family=fam, level=level,
                                    w=w, depth=depth, gross=g, rung=c,
                                    dSharpe=sharpe_of(r) - sharpe_of(t)))
    WF = pd.DataFrame(wf_rows)
    WF["win"] = WF.dSharpe > 0
    claim = []
    for wname in ("IS", "OOS"):
        for fam in ["ABS", "QEXP", "QROLL", "POOLED"]:
            s = WF[WF.window == wname]
            if fam != "POOLED":
                s = s[s.family == fam]
            s = s.groupby("rung").win.mean()
            ci, cr, cl = cross_half(s.index.values, s.values)
            claim.append(dict(window=wname, family=fam, cls=cl, win_0=float(s.iloc[0]),
                              win_10=float(s.loc[10.0]), win_25=float(s.loc[25.0]),
                              c_star_interp=ci, c_star_firstrung=cr,
                              rho_cost_win=spear(s.index.values, s.values)))
    CL = pd.DataFrame(claim)
    P(CL.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    wf_gap, wf_cls = {}, {}
    for fam in ["ABS", "QEXP", "QROLL"]:
        ri = CL[(CL.window == "IS") & (CL.family == fam)].iloc[0]
        ro = CL[(CL.window == "OOS") & (CL.family == fam)].iloc[0]
        i_, o_ = ri.c_star_firstrung, ro.c_star_firstrung
        gap = abs(i_ - o_) if (np.isfinite(i_) and np.isfinite(o_)) else np.inf
        wf_gap[fam] = gap
        wf_cls[fam] = (ri.cls, ro.cls)
        P(f"    {fam:6s} IS c* {i_:>6.4g} [{ri.cls:6s}]   OOS c* {o_:>6.4g} [{ro.cls:6s}]   "
          f"|gap| {gap:.4g} bps   IS win@0 {ri.win_0:.4f} vs OOS win@0 {ro.win_0:.4f}")

    # (b) the mandated book leg: every arm's OOS triple + both KEEP paths, at 10 bps
    live10 = backtest(px_["U56"], rules_v2_weights(px_["U56"], 0.03, 0.75), cost_bps=10,
                      freq="W")["returns"].loc[starts["U56"]:]
    v1_10 = backtest(px_["U56"], rules_v1_weights(px_["U56"]), cost_bps=10,
                     freq="W")["returns"].loc[starts["U56"]:]
    book = []
    for (pan, cad, fam, level, w, depth, g), a in arms.items():
        r = a["r0"] - a["to"] * PROTO_RUNG / 1e4
        s = spy[pan].reindex(r.index)
        ro, so = r.loc[OOS_START:], s.loc[OOS_START:]
        fc, fs, fd = w_metrics(r.values)
        oc, os_, od = w_metrics(ro.values)
        sc, ss, sd = w_metrics(s.values)
        soc, sos, sod = w_metrics(so.values)
        h = len(r) // 2
        ho = len(ro) // 2
        b_h1, b_h2 = sharpe_of(r.values[:h]), sharpe_of(r.values[h:])
        s_h1, s_h2 = sharpe_of(s.values[:h]), sharpe_of(s.values[h:])
        o_h1, o_h2 = sharpe_of(ro.values[:ho]), sharpe_of(ro.values[ho:])
        so_h1, so_h2 = sharpe_of(so.values[:ho]), sharpe_of(so.values[ho:])
        b4 = (b_h1 > s_h1 and b_h2 > s_h2 and fd >= 0.60 * sd and fc >= 0.70 * sc
              and o_h1 > so_h1 and o_h2 > so_h2 and od >= 0.60 * sod and oc >= 0.70 * soc)
        lr = live10.reindex(r.index).dropna()
        rr = r.reindex(lr.index)
        hh = len(rr) // 2
        a4 = (sharpe_of(rr.values[:hh]) > sharpe_of(lr.values[:hh])
              and sharpe_of(rr.values[hh:]) > sharpe_of(lr.values[hh:])
              and w_metrics(rr.values)[2] >= w_metrics(lr.values)[2])
        book.append(dict(panel=pan, cadence=cad, family=fam, level=level, w=w, depth=depth,
                         gross=g, CAGR=fc, Sharpe=fs, MaxDD=fd, H1=b_h1, H2=b_h2,
                         OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od, OOS_H1=o_h1, OOS_H2=o_h2,
                         keep_4a=bool(a4), keep_4b=bool(b4), g_eff=a["g_eff"]))
    BK = pd.DataFrame(book)
    lc_, ls_, ld_ = w_metrics(live10.loc[OOS_START:].values)
    vc_, vs_, vd_ = w_metrics(v1_10.loc[OOS_START:].values)
    spc, sps, spd = w_metrics(spy["U56"].loc[OOS_START:].values)
    P(f"\n  BOOK LEG at 10 bps ({len(BK)} arms): OOS CAGR {BK.OOS_CAGR.min():.2%}.."
      f"{BK.OOS_CAGR.max():.2%} (median {BK.OOS_CAGR.median():.2%});  OOS Sharpe "
      f"{BK.OOS_Sharpe.min():.4f}..{BK.OOS_Sharpe.max():.4f} (median "
      f"{BK.OOS_Sharpe.median():.4f});  OOS MaxDD {BK.OOS_MaxDD.min():.2%}.."
      f"{BK.OOS_MaxDD.max():.2%}")
    P(f"  comparands OOS: RULES v2 {lc_:.2%} / {ls_:.4f} / {ld_:.2%}   RULES v1 {vc_:.2%} / "
      f"{vs_:.4f} / {vd_:.2%}   SPY {spc:.2%} / {sps:.4f} / {spd:.2%}")
    P(f"  full-sample: arms CAGR {BK.CAGR.min():.2%}..{BK.CAGR.max():.2%} (median "
      f"{BK.CAGR.median():.2%}), Sharpe {BK.Sharpe.min():.4f}..{BK.Sharpe.max():.4f} (median "
      f"{BK.Sharpe.median():.4f}), MaxDD {BK.MaxDD.min():.2%}..{BK.MaxDD.max():.2%}")
    P(f"  KEEP paths on all {len(BK)} arms at 10 bps: 4a {int(BK.keep_4a.sum())}, "
      f"4b (full AND OOS legs) {int(BK.keep_4b.sum())}")
    # rule 8 on the BOOK: the arm chosen on IS Sharpe ALONE, its OOS read exactly once
    def akey(pan, cad, fam, level, w, depth, g):
        return (pan, cad, fam, float(level), (None if (w is None or pd.isna(w)) else float(w)),
                float(depth), float(g))

    is_sh = {}
    for k, a in arms.items():
        r = (a["r0"] - a["to"] * PROTO_RUNG / 1e4).loc[:SPLIT]
        is_sh[akey(*k)] = sharpe_of(r.values)
    BK["IS_Sharpe"] = [is_sh[akey(r.panel, r.cadence, r.family, r.level, r.w, r.depth, r.gross)]
                       for r in BK.itertuples()]
    pick = BK.loc[BK.IS_Sharpe.idxmax()]
    BK.to_csv(f"{OUT}.books.csv", index=False)          # written AFTER IS_Sharpe is attached
    pd.concat([CL.assign(kind="claim"), BK.assign(kind="book")],
              ignore_index=True).to_csv(f"{OUT}.wf.csv", index=False)
    P(f"\n  RULE-8 PICK (highest IS Sharpe <= 2016-12-31 among all {len(BK)} arms, OOS read "
      f"once): {pick.panel}/{pick.cadence}/{pick.family} level {pick.level} w {pick.w} depth "
      f"{pick.depth} gross {pick.gross}")
    P(f"     IS Sharpe {pick.IS_Sharpe:.4f} -> OOS {pick.OOS_CAGR:.2%} / {pick.OOS_Sharpe:.4f} / "
      f"{pick.OOS_MaxDD:.2%}   (OOS-best by Sharpe {BK.OOS_Sharpe.max():.4f}, "
      f"OOS median {BK.OOS_Sharpe.median():.4f})")
    P(f"     vs RULES v2 OOS {lc_:.2%} / {ls_:.4f} / {ld_:.2%};  SPY OOS {spc:.2%} / {sps:.4f} / "
      f"{spd:.2%};  the pick's 4b {bool(pick.keep_4b)} / 4a {bool(pick.keep_4a)}")
    if BK.keep_4b.any():
        P("  4b passers:")
        P(BK[BK.keep_4b].sort_values("OOS_Sharpe", ascending=False)
          [["panel", "cadence", "family", "level", "w", "depth", "gross", "CAGR", "Sharpe",
            "MaxDD", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]]
          .head(15).to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ============== SECTION 6: hypotheses + verdict ==============
    hdr("SECTION 6 — the seven pre-registered hypotheses")
    res = {}
    rho = {r.family: r.rho_cost_win for r in
           F[(F.source == "FRESH") & (F.ladder == "FINE")].itertuples()}
    fresh_cls = {r.family: r.cls for r in
                 F[(F.source == "FRESH") & (F.ladder == "FINE")].itertuples()}
    res["H_MONO"] = (all(rho[f] <= -0.80 for f in ("ABS", "QEXP", "QROLL")),
                     "rho(cost, win) " + ", ".join(f"{f} {rho[f]:+.4f}" for f in
                                                   ("ABS", "QEXP", "QROLL")) + " (bar <= -0.80)")
    w0 = {r.family: r.win_0 for r in F[(F.source == "FRESH") & (F.ladder == "FINE")].itertuples()}
    res["H_ORDER"] = (w0["QROLL"] > w0["QEXP"] > w0["ABS"],
                      f"win rate at 0 bps QROLL {w0['QROLL']:.4f} / QEXP {w0['QEXP']:.4f} / "
                      f"ABS {w0['ABS']:.4f}")
    abs_c, qr_c = CSTAR_FRESH["ABS"], CSTAR_FRESH["QROLL"]
    res["H_CROSS"] = (bool(np.isfinite(abs_c) and abs_c <= 15 and
                           (not np.isfinite(qr_c) or qr_c >= 30)),
                      f"FRESH ABS c* {abs_c:.4g} [{fresh_cls['ABS']}] (bar <= 15), QROLL c* "
                      f"{qr_c:.4g} [{fresh_cls['QROLL']}] (bar >= 30 or never); the RECORD's own "
                      f"committed column is ABS {CSTAR['ABS']:.4g} / QEXP {CSTAR['QEXP']:.4g} / "
                      f"QROLL {CSTAR['QROLL']:.4g}")
    stated = int(S.rung.notna().sum())
    above = int((S.at_or_above == True).sum())                                    # noqa: E712
    res["H_ABOVE"] = (above / max(stated, 1) >= 0.25,
                      f"{above} of {stated} rung-stating SITES are at or above their crossing "
                      f"cost ({above/max(stated,1):.1%}; bar >= 25%)")
    res["H_CENSUS"] = (int((S.rung_src != "LINE").sum()) >= len(S) / 2,
                       f"{int((S.rung_src != 'LINE').sum())} of {len(S)} sites state NO rung on "
                       f"their own line (bar >= half)")
    res["H_ARMDD"] = (bool(np.isfinite(rho_sw) and rho_sw < 0),
                      f"rho(switch tax, c*) = {rho_sw:+.4f} on {len(sub)} crossing arms "
                      f"(bar < 0)")
    res["H_WF"] = (all(v <= 10 for v in wf_gap.values()),
                   "IS vs OOS family c* gaps " +
                   ", ".join(f"{k} {v:.4g} [{wf_cls[k][0]}->{wf_cls[k][1]}]"
                             for k, v in wf_gap.items()) + " bps (bar <= 10)")
    for k, (ok, txt) in res.items():
        P(f"  {k:9s} {'PASS' if ok else 'FAIL'}  — {txt}")
    nph = sum(1 for ok, _ in res.values() if ok)
    P(f"\n  {nph} of {len(res)} hypotheses PASS")

    hdr("SECTION 7 — VERDICT")
    P(f"  The crossing-cost column, the RECORD's own (605's committed corpus): " +
      ", ".join(f"{k} {v:.4g} bps" if np.isfinite(v) else f"{k} never crosses"
                for k, v in CSTAR.items()))
    P(f"  The same column on this run's FRESH corpus: " +
      ", ".join(f"{k} {v:.4g} bps" if np.isfinite(v) else f"{k} NEVER crosses inside 100 bps"
                for k, v in CSTAR_FRESH.items()))
    P(f"  Attribution (605's OWN committed cells, matched subset): " +
      "; ".join(f"{r.family} {r.subset} c* "
                f"{r.c_star_firstrung if np.isfinite(r.c_star_firstrung) else float('nan'):.4g} "
                f"[{r.cls}]" for r in AT.itertuples()))
    P(f"  Census: {len(S)} twin/matched-gross SITES in {S.file.nunique()} committed files; "
      f"{stated} state a rung; {above} are AT OR ABOVE their crossing cost.")
    P(f"  Rule 8 on the CLAIM: family c* IS vs OOS gaps " +
      ", ".join(f"{k} {v:.4g}" for k, v in wf_gap.items()) + " bps.")
    P(f"  Rule 8 on the BOOKS: 4b {int(BK.keep_4b.sum())} of {len(BK)} arms, "
      f"4a {int(BK.keep_4a.sum())} of {len(BK)}, at 10 bps.")

    lines = [f"# Idea 607 — put a CROSSING-COST column on every published TWIN claim "
             f"({DATE}, cloud lane)\n",
             f"**Corpus** {len(arms)} gated arms (U56/B136 x W/D x "
             f"{len(GATES)} gates x depth x gross) each against its own matched-mean-gross static "
             f"twin, on a {len(FINE)}-rung ladder = {len(A)} priced cells; plus idea 605's "
             f"committed 648-arm corpus re-read. **Params** P1 claim set (SITES/FILES/"
             f"LEADERBOARD) x P2 ladder (FINE/COARSE).\n",
             f"**Gates** {sum(1 for g in grows if g['ok'])} of {len(grows)} PASS (G1 cost "
             f"identity {g1:.1e}, G2a weight linearity {g2a:.1e}, G2b return non-linearity in "
             f"gross MEASURED at {g2b:.1e} so every twin is run live, G3 605's committed ladder "
             f"{g3:.1e}, G4 RULES v2 {g4:.1e}, G5 metrics {g5:.1e}).\n",
             "**The crossing-cost column (the record's own, from 605's committed corpus)** " +
             ", ".join(f"{k} **{v:.4g} bps**" if np.isfinite(v) else f"{k} **never crosses**"
                       for k, v in CSTAR.items()) + "; on this run's FRESH corpus " +
             ", ".join(f"{k} {v:.4g} bps" if np.isfinite(v) else f"{k} NEVER inside 100 bps"
                       for k, v in CSTAR_FRESH.items()) + ".\n",
             f"**Census** {len(S)} SITES in {S.file.nunique()} files; {stated} state a rung "
             f"({stated/max(len(S),1):.1%}); **{above} are at or above the record's own crossing "
             f"cost for the family they name** ({above/max(stated,1):.1%} of those stating one); "
             f"{int((S.above_fresh == True).sum())} are at or above the FRESH column.\n",
             f"**Rule 8** claim leg: family c* IS vs OOS " +
             ", ".join(f"{k} {v:.4g} bps" for k, v in wf_gap.items()) +
             f". Book leg at 10 bps: arms OOS Sharpe {BK.OOS_Sharpe.min():.4f}.."
             f"{BK.OOS_Sharpe.max():.4f} (median {BK.OOS_Sharpe.median():.4f}), OOS CAGR "
             f"{BK.OOS_CAGR.min():.2%}..{BK.OOS_CAGR.max():.2%}; RULES v2 {lc_:.2%} / {ls_:.4f} "
             f"/ {ld_:.2%}; RULES v1 {vc_:.2%} / {vs_:.4f}; SPY {spc:.2%} / {sps:.4f} / "
             f"{spd:.2%}.\n",
             f"**KEEP paths** 4a {int(BK.keep_4a.sum())} of {len(BK)}; 4b (full AND OOS) "
             f"{int(BK.keep_4b.sum())} of {len(BK)}.\n",
             f"**Hypotheses** {nph} of {len(res)} PASS: " +
             "; ".join(f"{k} {'PASS' if v[0] else 'FAIL'}" for k, v in res.items()) + "\n",
             "**SURVIVORSHIP** U56 and B136 are current-constituent lists, so CAGR and drawdown "
             "levels are optimistic; the gate-minus-twin contrast and its cost slope are the "
             "durable part.\n"]
    Path(f"{OUT}.result.md").write_text("\n".join(lines))
    P(f"\n  wrote {OUT.name}.{{txt,arms.csv,cstar.csv,family.csv,census*.csv,books.csv,wf.csv,"
      f"gates.csv,result.md}}")
    P(f"  total {time.time()-t_all:.1f}s")
    Path(f"{OUT}.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
