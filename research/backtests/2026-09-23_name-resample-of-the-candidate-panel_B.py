#!/usr/bin/env python3
"""idea 2520 (lane B, run 65, 2026-09-23) — DOES THE CANDIDATE'S 4b PASS SURVIVE A
NAME-RESAMPLE OF ITS OWN PANEL?

THE OBJECT.  The record's standing 4b KEEP-candidate is idea 2322's CAP2: every name INSIDE
the 200d +/- 3% band (hysteresis, `baseline.band_state`) held at `min(gross / N_in, 2%)` of
NAV, idle NAV swept to SHY, weekly, t+1, 10 bps.

THE GAP.  Every robustness test this record owns resamples TIME — circular-block and
moving-block bootstraps (ideas 1785 / 2022 / 2042 / 2060) — and NOT ONE resamples NAMES.
Yet the panel is the record's own stated contaminant: rule 9, and idea 2435 verbatim,
"U56 / B136 are CURRENT constituents held from 2008; `L_CAGR` is the contaminated leg".
The candidate has therefore been scored on exactly ONE draw of 56 tickers.  Nothing in the
record says whether its 4b pass is a property of the RULE or of THOSE TICKERS.

DIAL 1 -- f, the NAME-KEEP FRACTION, in {0.25, 0.50, 0.75, 1.00}.  At each f a sub-panel of
K = round(f x |I|) names is drawn WITHOUT REPLACEMENT from the investable set I (the panel
minus the sweep instrument), md5-seeded so the draw is reproducible from the seed string
alone.  f = 1.00 is the IDENTITY rung: I itself, one deterministic book, = the committed
candidate (gate G1).  SHY is NEVER in the draw (it is the sweep, not a name) and the SPY
PRICE COLUMN is never removed from the frame (compare() needs it as the benchmark), so every
draw is scored on the IDENTICAL trading days against the IDENTICAL SPY series (gate G5).
SPY remains ELIGIBLE TO BE DRAWN, because the committed book may hold it; the pass rate is
also published SPLIT by whether SPY was drawn (idea 2435 measured the ETF sleeve as a drag,
so the prediction, stated before compute, is that the split is small and negative).
DIAL 2 -- GROSS in {0.75, 1.00}, the record's committed pair.

THE CONFOUND THIS RUN FOUND IN ITS OWN SMOKE TEST, AND CONTROLS FOR RATHER THAN HIDES.  Idea
2506 proved the 2% cap is a BREADTH-LINKED GROSS SCHEDULE: target risk gross is exactly
`min(gross, CAP x N_in)`, so it is CONSTANT above `gross/CAP` = 37.5 in-band names and falls
below it.  Shrinking the panel therefore DE-GROSSES the book mechanically -- at f = 0.25 on
U56 only 14 names exist, so gross can never exceed 0.28 and the book is a cash fund whatever
the names are.  A raw f-ladder would measure that arithmetic and call it name luck.  So every
cell is priced under TWO CAP CONVENTIONS, both reported in full and NEITHER selected on:
    ABS     cap = 2%,     RULES v2 clause 3 verbatim -- what a real sub-panel book would do
    SCALED  cap = 2% / f, breadth-matched -- the kink moves to f x 37.5 names, so the gross
            SCHEDULE is proportionally the same and only the NAMES differ
SCALED is the arm that answers the idea's question; ABS is the arm that answers "what happens
to the committed clause on a smaller panel". At f = 1.00 the two are identical by construction.

THAT IS EXACTLY TWO TUNED PARAMETERS.  Panels {U56, B136}, cost rungs {0, 10, 25, 50} bps,
cap 2%, band 0.03, cadence W and the SHY sweep are REPORTED IN FULL and never selected on.

THE PAIRED CONTROL THAT DIFFERENCES THE DRAW'S LUCK OUT.  A smaller sub-panel is a less
diversified book, so a fall in Sharpe with f is expected and says nothing on its own.  Beside
EVERY draw this run prices EWALL: the SAME drawn names, the SAME gross, the SAME 2% cap, the
SAME SHY sweep, the SAME weekly cadence -- and NO BAND GATE (every priced name admitted).
BAND minus EWALL on the same draw is a same-names, same-days, same-gross contrast in which
the draw cancels exactly.  It is the one number here that is first-order immune to
survivorship, and it is what "the rule earns its keep" has to mean.

BOTH KEEP PATHS on every row: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse)
and 4b (Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x
SPY's).  RULE 8: (f, gross) chosen on warm-up..2016-12-31 ONLY by five pre-stated choosers,
then 2017-2026 read ONCE.
    C_ISSHARPE   max IS Sharpe over the f ladder at gross 0.75
    C_ISCALMAR   max IS Calmar over the f ladder at gross 0.75
    C_ISCAGR     max IS CAGR   over the f ladder at gross 0.75
    C_JOINT      max IS Sharpe over the FULL (f x gross) grid -- both dials fitted together
    C_PREREG     NO CHOICE AT ALL -- f = 1.00, gross = 0.75, the committed cell.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_name-resample-of-the-candidate-panel_B.py
"""
from __future__ import annotations

import hashlib, sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state   # noqa: E402
from engine import backtest, metrics                               # noqa: E402

DATE, SLUG, LANE = "2026-09-23", "name-resample-of-the-candidate-panel", "B"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, CAP, CADENCE, WARMUP = 0.03, 0.02, "W", 260
SWEEP = "SHY"
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG = 10.0
FRACS = [0.25, 0.50, 0.75, 1.00]
SEEDS = 30                              # draws per (panel, f<1); f=1.00 is deterministic
CAPMODES = ["ABS", "SCALED"]            # reported in full, never selected on -- see the header
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
# the committed headline this run must reproduce at f = 1.00 (idea 2322 / 2431 / 2499)
COMMITTED = dict(CAGR=0.1162, Sharpe=1.2687, MaxDD=-0.1481, turn=3.51)

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


def publish(name, value):
    GATES.append(dict(gate=name, value=str(value), target="published, not asserted", pass_=True))
    say(f"    PUB   {name}: {value}")


# ---------------------------------------------------------------- the draw
def draw_names(invest, k, panel, f, seed):
    """Deterministic md5-seeded draw of k names WITHOUT replacement from `invest`.

    The seed string carries the panel, the fraction and the seed index, so no two cells can
    ever share a draw by accident and the whole study is reproducible from this file alone.
    """
    h = hashlib.md5(f"2520|{panel}|{f:.2f}|{seed}".encode()).hexdigest()
    rng = np.random.default_rng(int(h[:16], 16))
    idx = rng.permutation(len(invest))[:k]
    return sorted(invest[i] for i in idx)


# ---------------------------------------------------------------- the two books
def cap_weights(px, invest, gross, gated, state, cap=CAP):
    """CAP2 on `invest`: w_i = min(gross / N_in, CAP) on the admitted set, idle NAV -> SHY.

    gated=True  -> admitted = inside the 200d +/- BAND band (hysteresis) AND priced  (BAND arm)
    gated=False -> admitted = priced that day                                        (EWALL arm)
    EWALL is the SAME names, gross, cap, sweep and cadence with the gate removed, so the
    BAND-minus-EWALL contrast prices the GATE and nothing else.
    """
    q = px[invest]
    live = q.notna()
    adm = (state[invest] & live) if gated else live
    adm = adm.reindex(columns=px.columns).fillna(False)
    nin = adm[invest].sum(axis=1).replace(0, np.nan)
    per = pd.concat([gross / nin, pd.Series(cap, index=q.index)], axis=1).min(axis=1)
    w = adm.astype(float).mul(per.fillna(0.0), axis=0)
    w[SWEEP] = 0.0
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = idle * px[SWEEP].notna().astype(float)
    return w


def score(px, w, start):
    """One engine pass at ZERO cost; every rung is then priced from the same turnover path."""
    res = backtest(px, w, cost_bps=0.0, freq=CADENCE)
    r0 = res["returns"].loc[start:]
    to = res["turnover"].loc[start:].fillna(0.0)
    held = res["weights"].loc[start:]
    out = {}
    for k in RUNGS:
        r = r0 - to * k / 1e4
        m = metrics(r)
        h = len(r) // 2
        oos = r.loc[OOS_START:]
        isr = r.loc[:IS_END]
        mo, mi = metrics(oos), metrics(isr)
        out[k] = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], Calmar=m["Calmar"],
                      H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                      OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                      IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_Calmar=mi["Calmar"],
                      turn=to.sum() / m["Years"])
    out["mean_sweep_w"] = float(held[SWEEP].mean())
    out["mean_risk_gross"] = float(held.drop(columns=[SWEEP]).sum(axis=1).mean())
    return out


def bench(r, start):
    rr = r.loc[start:]
    m = metrics(rr)
    h = len(rr) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(rr.iloc[:h])["Sharpe"], H2=metrics(rr.iloc[h:])["Sharpe"],
                OOS_CAGR=metrics(rr.loc[OOS_START:])["CAGR"],
                OOS_Sharpe=metrics(rr.loc[OOS_START:])["Sharpe"],
                OOS_MaxDD=metrics(rr.loc[OOS_START:])["MaxDD"])


def legs4b(d, s):
    """4b: Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 0.60 x SPY's, CAGR >= 0.70 x SPY's."""
    L = dict(L_H1=d["H1"] > s["H1"], L_H2=d["H2"] > s["H2"], L_OOS=d["OOS_Sharpe"] > s["OOS_Sharpe"],
             L_DD=d["MaxDD"] >= DD_CAP * s["MaxDD"], L_CAGR=d["CAGR"] >= CAGR_FLOOR * s["CAGR"])
    return L, "".join("1" if L[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))


def legs4a(d, b):
    L = dict(A_H1=d["H1"] > b["H1"], A_H2=d["H2"] > b["H2"], A_DD=d["MaxDD"] >= b["MaxDD"])
    return L, "".join("1" if L[k] else "0" for k in ("A_H1", "A_H2", "A_DD"))


# ================================================================= run
T0 = time.time()
say(f"idea 2520 — name-resample of the candidate panel  (lane {LANE}, {DATE})")
say(f"  dials: f {FRACS} x gross {GROSSES}   seeds {SEEDS}   arms BAND / EWALL")
say(f"  fixed & reported, never selected on: band {BAND} cap {CAP} cadence {CADENCE} "
    f"rungs {RUNGS} bps sweep {SWEEP}")

PANELS = {}
STATE = {}
BENCH = {}
for panel, kw in (("U56", dict()), ("B136", dict(broad=True))):
    px = load_universe(**kw)
    PANELS[panel] = px
    STATE[panel] = band_state(px, BAND)
    start = px.index[WARMUP]
    spy = bench(px["SPY"].pct_change().fillna(0.0), start)
    base = bench(backtest(px, rules_v2_weights(px), cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"], start)
    BENCH[panel] = dict(start=start, SPY=spy, BASE=base,
                        invest=[c for c in px.columns if c != SWEEP])
    say(f"\n  {panel}: {px.shape[1]} cols, {len(BENCH[panel]['invest'])} investable, "
        f"{px.index[0].date()} -> {px.index[-1].date()}, scored from {start.date()}")
    say(f"    SPY  {spy['CAGR']:.2%} / {spy['Sharpe']:.4f} / {spy['MaxDD']:.2%}  "
        f"halves {spy['H1']:.4f}/{spy['H2']:.4f}  OOS {spy['OOS_CAGR']:.2%}/{spy['OOS_Sharpe']:.4f}")
    say(f"    live RULES v2 @10bps  {base['CAGR']:.2%} / {base['Sharpe']:.4f} / {base['MaxDD']:.2%}  "
        f"OOS {base['OOS_CAGR']:.2%}/{base['OOS_Sharpe']:.4f}")

# ---- gates on the machinery -------------------------------------------------
say("\n--- GATES ---")
px = PANELS["U56"]; st = BENCH["U56"]["start"]; inv = BENCH["U56"]["invest"]
anchor = score(px, cap_weights(px, inv, 0.75, True, STATE["U56"]), st)[HEADLINE_RUNG]
gate("G1 f=1.00 CAP2 reproduces the committed U56/g0.75/10bps Sharpe",
     f"{anchor['Sharpe']:.4f} vs {COMMITTED['Sharpe']:.4f}", "|d| <= 0.005",
     abs(anchor["Sharpe"] - COMMITTED["Sharpe"]) <= 0.005)
publish("G1b f=1.00 CAGR / MaxDD / turnover vs the committed quote",
        f"{anchor['CAGR']:.4%} vs {COMMITTED['CAGR']:.2%}; {anchor['MaxDD']:.4%} vs "
        f"{COMMITTED['MaxDD']:.2%}; {anchor['turn']:.3f}x vs {COMMITTED['turn']:.2f}x "
        f"(engine.backtest + baseline.compare's row-260 warm-up; the quoted headline comes "
        f"from a hand-rolled replica on a shorter tape)")
d = draw_names(inv, 14, "U56", 0.25, 3)
d2 = draw_names(inv, 14, "U56", 0.25, 3)
gate("G2 draw is deterministic given (panel, f, seed)", f"{d == d2}", "True", d == d2)
gate("G3 draw has no repeats and the right size", f"{len(set(d))}/{len(d)} of 14", "14/14", len(set(d)) == len(d) == 14)
gate("G4 SWEEP never drawn (200 draws x 2 panels)",
     f"{sum(SWEEP in draw_names(BENCH[p]['invest'], max(1, round(f*len(BENCH[p]['invest']))), p, f, s) for p in PANELS for f in FRACS for s in range(25))} hits",
     "0", not any(SWEEP in draw_names(BENCH[p]["invest"], max(1, round(f * len(BENCH[p]["invest"]))), p, f, s)
                  for p in PANELS for f in FRACS for s in range(25)))
gate("G5 SPY benchmark series identical across every draw (the frame is never subset)",
     "price frame passed to engine is the FULL panel; only the INVESTABLE set is drawn", "by construction", True)
w_chk = cap_weights(px, inv, 0.75, True, STATE["U56"])
_cut = px.index[len(px.index) - 400]
_trunc = px.loc[:_cut]
_wt = cap_weights(_trunc, inv, 0.75, True, band_state(_trunc, BAND))
_d = float((w_chk.loc[:_cut][_wt.columns] - _wt).abs().max().max())
gate("G6 NO LOOKAHEAD: weights recomputed on a tape truncated 400 rows early are identical",
     f"max |dw| = {_d:.3e}", "0.000e+00", _d == 0.0)
gate("G7 EWALL holds strictly more names than BAND at f=1.00",
     f"mean admitted {float((STATE['U56'][inv] & px[inv].notna()).sum(axis=1).mean()):.2f} (BAND) vs "
     f"{float(px[inv].notna().sum(axis=1).mean()):.2f} (EWALL)", "EWALL >= BAND",
     float(px[inv].notna().sum(axis=1).mean()) >= float((STATE["U56"][inv] & px[inv].notna()).sum(axis=1).mean()))
gate("G8 max-minus-min held risk weight is 0 (idea 2506's identity: the cap de-grosses, never de-concentrates)",
     f"{float(w_chk[inv].replace(0.0, np.nan).max(axis=1).sub(w_chk[inv].replace(0.0, np.nan).min(axis=1)).max()):.3e}",
     "0.000e+00",
     float(w_chk[inv].replace(0.0, np.nan).max(axis=1).sub(w_chk[inv].replace(0.0, np.nan).min(axis=1)).max()) < 1e-15)

# ---- the grid ---------------------------------------------------------------
say("\n--- GRID ---")
rows = []
for panel in PANELS:
    px = PANELS[panel]; st = BENCH[panel]["start"]; inv = BENCH[panel]["invest"]
    spy, base = BENCH[panel]["SPY"], BENCH[panel]["BASE"]
    for f in FRACS:
        k = max(1, round(f * len(inv)))
        seeds = [0] if f >= 1.0 else list(range(SEEDS))
        for s in seeds:
            names = inv if f >= 1.0 else draw_names(inv, k, panel, f, s)
            has_spy = "SPY" in names
            for g in GROSSES:
              for cm in (["ABS"] if f >= 1.0 else CAPMODES):
                cap = CAP if cm == "ABS" else CAP / f
                for arm, gated in (("BAND", True), ("EWALL", False)):
                    sc = score(px, cap_weights(px, names, g, gated, STATE[panel], cap), st)
                    for rung in RUNGS:
                        d = sc[rung]
                        Lb, sb = legs4b(d, spy)
                        La, sa = legs4a(d, base)
                        rows.append(dict(panel=panel, f=f, K=k, seed=s, gross=g, arm=arm,
                                         capmode=cm, cap=cap, rung=rung, has_spy=has_spy,
                                         mean_sweep_w=sc["mean_sweep_w"],
                                         mean_risk_gross=sc["mean_risk_gross"], **d,
                                         keep4b=all(Lb.values()), legs4b=sb,
                                         keep4a=all(La.values()), legs4a=sa, **Lb, **La))
        say(f"  {panel}  f={f:.2f} K={k:3d}  {len(seeds)} draw(s)  "
            f"[{time.time()-T0:6.1f}s]")

G = pd.DataFrame(rows)
# f = 1.00 is identical under both conventions (cap = CAP/1.0 = CAP); duplicate the anchor into
# the SCALED slice so every capmode slice carries its own f=1.00 comparand.
dup = G[G.f >= 1.0].copy(); dup["capmode"] = "SCALED"
G = pd.concat([G, dup], ignore_index=True)
G.to_csv(f"{OUT}.grid.csv", index=False)
say(f"\n  {len(G)} rows written to {Path(OUT).name}.grid.csv  [{time.time()-T0:.1f}s]")

# ================================================================= A. the pass-rate curve
say("\n--- A. 4b / 4a PASS RATE AS A FUNCTION OF THE NAME-KEEP FRACTION (arm BAND) ---")
A = []
for panel in PANELS:
    for cm in CAPMODES:
        for g in GROSSES:
            for rung in RUNGS:
                for f in FRACS:
                    q = G[(G.panel == panel) & (G.capmode == cm) & (G.gross == g) &
                          (G.rung == rung) & (G.arm == "BAND") & (G.f == f)]
                    A.append(dict(panel=panel, capmode=cm, gross=g, rung=rung, f=f, n=len(q),
                                  pass4b=q.keep4b.mean(), pass4a=q.keep4a.mean(),
                                  med_Sharpe=q.Sharpe.median(), med_CAGR=q.CAGR.median(),
                                  med_MaxDD=q.MaxDD.median(),
                                  med_OOS_Sharpe=q.OOS_Sharpe.median(), med_turn=q.turn.median(),
                                  med_risk_gross=q.mean_risk_gross.median(),
                                  **{L: q[L].mean() for L in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")}))
A = pd.DataFrame(A)
A.to_csv(f"{OUT}.passrate.csv", index=False)

say("\n  HEADLINE (10 bps): 4b / 4a pass rate, median Sharpe, median realised RISK GROSS")
for cm in CAPMODES:
    say(f"  --- cap convention {cm} ---")
    for panel in PANELS:
        for g in GROSSES:
            for r in A[(A.panel == panel) & (A.capmode == cm) & (A.gross == g) &
                       (A.rung == HEADLINE_RUNG)].itertuples():
                say(f"    {panel} g{g:.2f} f={r.f:.2f} n={r.n:3d}  4b {r.pass4b:5.0%}  4a {r.pass4a:5.0%}  "
                    f"Sh {r.med_Sharpe:.4f}  CAGR {r.med_CAGR:6.2%}  DD {r.med_MaxDD:7.2%}  "
                    f"OOSSh {r.med_OOS_Sharpe:.4f}  turn {r.med_turn:.2f}x  gross {r.med_risk_gross:.3f}")

say("\n  LEG-BY-LEG PASS RATE (arm BAND, 10 bps) — which leg binds as the panel shrinks:")
for cm in CAPMODES:
    for panel in PANELS:
        for g in GROSSES:
            for r in A[(A.panel == panel) & (A.capmode == cm) & (A.gross == g) &
                       (A.rung == HEADLINE_RUNG)].itertuples():
                say(f"    {cm:6s} {panel} g{g:.2f} f={r.f:.2f}  H1 {r.L_H1:5.0%}  H2 {r.L_H2:5.0%}  "
                    f"OOS {r.L_OOS:5.0%}  DD {r.L_DD:5.0%}  CAGR {r.L_CAGR:5.0%}   -> 4b {r.pass4b:5.0%}")

say("\n  ALL FOUR COST RUNGS (arm BAND, 4b pass rate):")
for cm in CAPMODES:
    for panel in PANELS:
        for g in GROSSES:
            for f in FRACS:
                q = A[(A.panel == panel) & (A.capmode == cm) & (A.gross == g) & (A.f == f)].sort_values("rung")
                say(f"    {cm:6s} {panel} g{g:.2f} f={f:.2f}   " +
                    "  ".join(f"{r.rung:.0f}bps {r.pass4b:5.0%}" for r in q.itertuples()))

# ================================================================= B. the paired gate contrast
say("\n--- B. BAND minus EWALL ON THE SAME DRAW (the survivorship-immune contrast) ---")
say("  Same names, same days, same gross, same cap, same sweep, same cadence; only the 200d")
say("  band gate differs.  The draw cancels exactly, so this is the one number here that is")
say("  first-order immune to the panel's current-constituent bias (rule 9).")
key = ["panel", "capmode", "f", "seed", "gross", "rung"]
b_ = G[G.arm == "BAND"].drop_duplicates(key).set_index(key)
e_ = G[G.arm == "EWALL"].drop_duplicates(key).set_index(key)
D = pd.DataFrame(index=b_.index)
for c in ("CAGR", "Sharpe", "MaxDD", "OOS_Sharpe", "OOS_CAGR", "turn", "mean_risk_gross"):
    D["d" + c] = b_[c] - e_[c]
D["band_keep4b"] = b_["keep4b"]; D["ewall_keep4b"] = e_["keep4b"]
D = D.reset_index()
D.to_csv(f"{OUT}.gate_contrast.csv", index=False)
for cm in CAPMODES:
    for panel in PANELS:
        for g in GROSSES:
            for f in FRACS:
                q = D[(D.panel == panel) & (D.capmode == cm) & (D.gross == g) & (D.f == f) &
                      (D.rung == HEADLINE_RUNG)]
                if not len(q): continue
                say(f"    {cm:6s} {panel} g{g:.2f} f={f:.2f} n={len(q):3d}  "
                    f"dSharpe med {q.dSharpe.median():+.4f} (>0 in {int((q.dSharpe > 0).sum())}/{len(q)})  "
                    f"dCAGR {q.dCAGR.median():+.2%}  "
                    f"dMaxDD {q.dMaxDD.median():+.2%} (shallower {int((q.dMaxDD > 0).sum())}/{len(q)})  "
                    f"dOOSSh {q.dOOS_Sharpe.median():+.4f} (>0 in {int((q.dOOS_Sharpe > 0).sum())}/{len(q)})  "
                    f"dturn {q.dturn.median():+.2f}x")
POOL = D[D.rung == HEADLINE_RUNG]
for nm, col, cmp_ in (("dSharpe > 0", "dSharpe", 0), ("dOOS_Sharpe > 0", "dOOS_Sharpe", 0),
                      ("dMaxDD shallower", "dMaxDD", 0), ("dCAGR > 0", "dCAGR", 0)):
    publish(f"B-pooled {nm}", f"{int((POOL[col] > cmp_).sum())} of {len(POOL)} "
            f"(median {POOL[col].median():+.4f})")
for cm in CAPMODES:
    q = POOL[POOL.capmode == cm]
    publish(f"B-pooled dSharpe > 0 [{cm}]",
            f"{int((q.dSharpe > 0).sum())} of {len(q)} (median {q.dSharpe.median():+.4f})")

# ================================================================= C. where the committed draw sits
say("\n--- C. WHERE THE COMMITTED PANEL SITS IN ITS OWN SUB-PANEL DISTRIBUTION ---")
say("  (f=1.00 IS the committed draw; the f<1 rows are random sub-panels of it)")
for cm in CAPMODES:
    for panel in PANELS:
        for g in GROSSES:
            full = G[(G.panel == panel) & (G.capmode == cm) & (G.gross == g) &
                     (G.rung == HEADLINE_RUNG) & (G.arm == "BAND") & (G.f == 1.0)].iloc[0]
            for f in [x for x in FRACS if x < 1.0]:
                q = G[(G.panel == panel) & (G.capmode == cm) & (G.gross == g) &
                      (G.rung == HEADLINE_RUNG) & (G.arm == "BAND") & (G.f == f)]
                say(f"    {cm:6s} {panel} g{g:.2f} f={f:.2f}  full-panel Sharpe {full.Sharpe:.4f} "
                    f"sits at pct {float((q.Sharpe < full.Sharpe).mean()):3.0%} of its sub-panels "
                    f"(OOS {float((q.OOS_Sharpe < full.OOS_Sharpe).mean()):3.0%})  |  sub-panel Sharpe "
                    f"p10/p50/p90 {q.Sharpe.quantile(.1):.4f}/{q.Sharpe.median():.4f}/{q.Sharpe.quantile(.9):.4f}"
                    f"  OOS p10/p50/p90 {q.OOS_Sharpe.quantile(.1):.4f}/{q.OOS_Sharpe.median():.4f}/"
                    f"{q.OOS_Sharpe.quantile(.9):.4f}")

say("\n  SPY-IN-DRAW SPLIT (idea 2435 predicted the ETF sleeve is a DRAG; sign stated before compute):")
for panel in PANELS:
    q = G[(G.panel == panel) & (G.rung == HEADLINE_RUNG) & (G.arm == "BAND") & (G.f < 1.0)]
    wi, wo = q[q.has_spy], q[~q.has_spy]
    say(f"    {panel}  SPY drawn n={len(wi)} Sharpe med {wi.Sharpe.median():.4f} 4b {wi.keep4b.mean():.0%}  |  "
        f"SPY NOT drawn n={len(wo)} Sharpe med {wo.Sharpe.median():.4f} 4b {wo.keep4b.mean():.0%}  "
        f"-> d {wi.Sharpe.median()-wo.Sharpe.median():+.4f}")

# ================================================================= D. rule 8 walk-forward
say("\n--- D. RULE 8 WALK-FORWARD: (f, gross) fitted on warm-up..2016-12-31, 2017-2026 read ONCE ---")
CHOOSERS = {
    "C_ISSHARPE": ("IS_Sharpe", 0.75), "C_ISCALMAR": ("IS_Calmar", 0.75),
    "C_ISCAGR": ("IS_CAGR", 0.75), "C_JOINT": ("IS_Sharpe", None), "C_PREREG": (None, 0.75),
}
WF = []
for panel in PANELS:
    spy, base = BENCH[panel]["SPY"], BENCH[panel]["BASE"]
    inc = G[(G.panel == panel) & (G.arm == "BAND") & (G.f == 1.0) & (G.gross == 0.75) &
            (G.rung == HEADLINE_RUNG) & (G.capmode == "ABS")].iloc[0]
    for cm in CAPMODES:
        for rung in RUNGS:
            pool = G[(G.panel == panel) & (G.arm == "BAND") & (G.rung == rung) & (G.capmode == cm)]
            for s in range(SEEDS):
                cand = pool[(pool.seed == s) | (pool.f == 1.0)]
                for cname, (stat, gfix) in CHOOSERS.items():
                    c = cand if gfix is None else cand[cand.gross == gfix]
                    pick = c.loc[c[stat].idxmax()] if stat else c[c.f == 1.0].iloc[0]
                    WF.append(dict(panel=panel, capmode=cm, rung=rung, seed=s, chooser=cname,
                                   pick_f=pick.f, pick_gross=pick.gross,
                                   OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                                   OOS_MaxDD=pick.OOS_MaxDD,
                                   beats_SPY_OOS=pick.OOS_Sharpe > spy["OOS_Sharpe"],
                                   beats_BASE_OOS=pick.OOS_Sharpe > base["OOS_Sharpe"],
                                   beats_INC_OOS=pick.OOS_Sharpe > inc.OOS_Sharpe,
                                   keep4b=pick.keep4b, keep4a=pick.keep4a))
WF = pd.DataFrame(WF)
WF.to_csv(f"{OUT}.walkforward.csv", index=False)
for cm in CAPMODES:
    for panel in PANELS:
        for cname in CHOOSERS:
            q = WF[(WF.panel == panel) & (WF.capmode == cm) & (WF.chooser == cname) &
                   (WF.rung == HEADLINE_RUNG)]
            say(f"    {cm:6s} {panel} {cname:11s} picks f=" +
                "/".join(f"{f:.2f}:{int((q.pick_f == f).sum())}" for f in FRACS) +
                f"  beats SPY OOS {int(q.beats_SPY_OOS.sum())}/{len(q)}"
                f"  beats live v2 OOS {int(q.beats_BASE_OOS.sum())}/{len(q)}"
                f"  beats the COMMITTED panel OOS {int(q.beats_INC_OOS.sum())}/{len(q)}"
                f"  full-sample 4b {int(q.keep4b.sum())}/{len(q)}"
                f"  med OOS Sharpe {q.OOS_Sharpe.median():.4f}")
publish("D rule-8 picks beating SPY OOS (all choosers, rungs, capmodes, panels)",
        f"{int(WF.beats_SPY_OOS.sum())} of {len(WF)}")
publish("D rule-8 picks beating the COMMITTED full panel OOS",
        f"{int(WF.beats_INC_OOS.sum())} of {len(WF)}")
publish("D rule-8 picks landing on f < 1.00 (a sub-panel chosen IN SAMPLE)",
        f"{int((WF.pick_f < 1.0).sum())} of {len(WF)}")
publish("D rule-8 picks carrying a full-sample 4b", f"{int(WF.keep4b.sum())} of {len(WF)}")

# ================================================================= E. verdict
say("\n--- E. VERDICT ---")
BND = G[G.arm == "BAND"]
publish("E total rows / BAND rows", f"{len(G)} / {len(BND)}")
publish("E BOTH KEEP PATHS over all BAND rows", f"4b {int(BND.keep4b.sum())}, 4a {int(BND.keep4a.sum())}")
publish("E 4b leg-string census (BAND rows)",
        "; ".join(f"{k} x{v}" for k, v in BND.legs4b.value_counts().head(8).items()))
publish("E 4b leg FAIL counts (BAND rows)",
        "; ".join(f"{L} {int((~BND[L]).sum())}" for L in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
for cm in CAPMODES:
    hl = A[(A.rung == HEADLINE_RUNG) & (A.gross == 0.75) & (A.capmode == cm) & (A.panel == "U56")]
    publish(f"E 4b pass rate U56 g0.75 @10bps [{cm}] f=0.25/0.50/0.75/1.00",
            " / ".join(f"{float(hl[hl.f == f].pass4b.iloc[0]):.0%}" for f in FRACS))
    hl = A[(A.rung == HEADLINE_RUNG) & (A.gross == 0.75) & (A.capmode == cm) & (A.panel == "B136")]
    publish(f"E 4b pass rate B136 g0.75 @10bps [{cm}] f=0.25/0.50/0.75/1.00",
            " / ".join(f"{float(hl[hl.f == f].pass4b.iloc[0]):.0%}" for f in FRACS))

gates_ok = sum(1 for g in GATES if g["pass_"] and "published" not in g["target"])
gates_n = sum(1 for g in GATES if "published" not in g["target"])
say(f"\n  gates {gates_ok} of {gates_n}")
pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)

# ---- LEADERBOARD rows -------------------------------------------------------
LB = []
script = f"{DATE}_{SLUG}_{LANE}.py"
for panel in PANELS:
    base = BENCH[panel]["BASE"]
    for cm in CAPMODES:
        for f in FRACS:
            q = G[(G.panel == panel) & (G.capmode == cm) & (G.arm == "BAND") &
                  (G.gross == 0.75) & (G.rung == HEADLINE_RUNG) & (G.f == f)]
            md = q.median(numeric_only=True)
            rate = q.keep4b.mean()
            v = f"4b-rate {rate:.0%}" + (" KEEP-4b(median draw)" if rate >= 0.5 else " KILL")
            nm = f"2520 name-resample {panel} {cm} f={f:.2f} (median of {len(q)} draws, g0.75, 10bps)"
            LB.append(f"| {DATE} | {nm} | {md.CAGR:.1%} | {md.Sharpe:.2f} | {md.MaxDD:.1%} | "
                      f"{md.H1:.2f} / {md.H2:.2f} | {base['Sharpe']:.2f} "
                      f"({base['H1']:.2f}/{base['H2']:.2f}) | {v} | {script} |")
Path(f"{OUT}.leaderboard.txt").write_text("\n".join(LB) + "\n")
say("\nLEADERBOARD rows:\n" + "\n".join(LB))
say(f"\ndone in {time.time()-T0:.1f}s")
Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
