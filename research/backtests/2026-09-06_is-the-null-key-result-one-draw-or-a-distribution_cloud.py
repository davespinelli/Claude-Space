#!/usr/bin/env python3
"""QUEUE idea 180 - is-the-null-key-result-one-draw-or-a-distribution   (cloud, 2026-09-06).

QUESTION (pre-registered, verbatim from QUEUE.md idea 180)
    "idea 158's decisive control is ONE seeded random key: it beat the live `/sqrt(vol20)` scaler
     in 27 of 28 large-cap cells, took 11 of 54 4b passes and 4 of 19 cross-universe combinations,
     and was what rule 8 picked on broad@10bps.  All of that is a property of that draw.  Re-run
     the identical grid over 100 independent null keys and report the DISTRIBUTION of |dSharpe|,
     of the 4b pass count and of the rule-8 OOS Sharpe, so the project can quote a null band
     rather than a null point.  Max 2 params."

WHAT IS AT STAKE
    Idea 158's null key is now load-bearing: it is the instrument behind "a key with zero
    information clears the 4b bar as often as a real one", the eighth delete-the-scaler finding,
    and the sixth "the selector is picking noise" result.  Every one of those sentences is a
    statement about seed 158.  A null CONTROL that is quoted as a point estimate is not a control
    - it is a single draw of a random variable being compared to five fixed ones.  This run turns
    the point into a band.  It proposes no book and changes no rule.

THE GRID - idea 158's, unchanged
    3 panels (u56 / broad / small) x 7 book shares x {NONE control, 5 real keys x 2 directions}
    plus, per DRAW, RAND x 2 directions.  Weekly, t+1, 0.75 gross, 200d gate, vol20 < 0.60.
    Each book is run ONCE at 0 bps and the 10 / 25 bps rungs are derived by the engine's own cost
    identity r_c = r_0 - turnover * c / 1e4 (control [D]), so every leg of every comparison is the
    SAME book bar for bar.

TUNED PARAMETERS - exactly two, both idea 158's, both swept exhaustively:
    1. book share m in {0.05, 0.10, 0.20, 0.35, 0.53, 0.75, 1.00}, realised as
       n = max(2, round(m x mean weekly eligible count)).
    2. tilt direction in {NEG, NONE, POS}.
    The 100 DRAWS are not a parameter: nothing is ever selected on the draw index.  Panels, cost
    rungs and the OOS window are reported axes, never selected on.

THE 100 NULL KEYS
    Draw d builds RW6_d exactly as idea 158 built its single key - a synthetic geometric random
    walk per name at the panel's own median daily vol, differenced over 126 bars, ranked, clipped
    to [0.05, 1] and raised to 0.5 - with rng = default_rng(SEED_OF(d)), fresh per panel.
    SEED_OF(0) = 158, so DRAW 0 IS IDEA 158'S PUBLISHED KEY, and control [C] requires it to
    reproduce the committed grid.csv exactly.  Draws 1..99 use 180001..180099.

CONTROLS, asserted before any new number is read
    [A] the vectorised simulator == products/backtester/engine.backtest on returns and turnover,
        on all three panels at freq="W".
    [D] the cost identity against a fresh 10 bps engine run.
    [C] THE DECISIVE ONE: every real-key row AND every draw-0 RAND row must reproduce idea 158's
        committed `2026-09-05_does-share-price-any-key-or-only-vol_B.grid.csv` (literal-book rows)
        on CAGR/Sharpe/MaxDD/H1/H2/OOS_*/IS_*/TO to <1e-9.  Failure means this is not idea 158's
        grid and the run stops being a re-run of it.

WHAT IS REPORTED (the three distributions the idea asks for, plus the two derived claims)
    R1  mean |dSharpe| of the null key per (panel, cost), full grid and m <= 0.53, as a
        distribution over 100 draws, against the five real keys' fixed values.
    R2  the null key's 4b pass count (out of its own 84 cells) as a distribution, and its share of
        the grid's total 4b passes.
    R3  rule 8: S3 (IS-Sharpe argmax over the null key's arms only) mean OOS Sharpe as a
        distribution, against S1 (all arms), S2 (do-nothing at m=0.53), S4 (NONE arms only),
        RULES v1 and SPY over the same OOS window.  Also: how often S1 PICKS a null-key arm.
    R4  "beats the live /sqrt(vol20) scaler in k of 28 large-cap cells", as a distribution.
    R5  cross-universe 4b combinations ((m, key, dir) passing on >1 panel) held by the null key.
    Both KEEP paths (4a and 4b) are evaluated on every book.

CAVEATS carried, not buried
    * SURVIVORSHIP: all three panels are current-constituent lists (idea 54); the small panel
      additionally drops every ticker with max_1d_move >= 1.0 per the standing rule.
    * Ideas 39/49: the eligibility gate is INVERTED on the small panel, so its numbers are about a
      gate that does not work there.  Reported, never traded.
    * Idea 126: t+1 only, no spread or impact model.
    * 100 draws bound the SEED, not the model: every null key here is a geometric random walk with
      R6's functional form.  A different null FAMILY is a different question.

Deterministic, standalone, no network.  Writes .console.txt, .grid.csv, .draws.csv, .walkforward.csv.
"""
import importlib.util
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-06_is-the-null-key-result-one-draw-or-a-distribution_cloud"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I129 = OUT / "2026-09-05_cagr-floor-calibration_B.py"
PARENT = "2026-09-05_does-share-price-any-key-or-only-vol_B"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")
C = _load(I129, "i129")

FREQ = "W"
COSTS = [10.0, 25.0]
PANELS = ["u56", "broad", "small"]
OOS_START = H.OOS_START
PHI0, DELTA0 = 0.70, 0.60
GROSS, MAX_VOL = 0.75, 0.60
SHARES = [0.05, 0.10, 0.20, 0.35, 0.53, 0.75, 1.00]
REAL_KEYS = ["VOL", "VOLR", "MOM", "R6", "R3"]
N_DRAWS = int(os.environ.get("N_DRAWS", "100"))   # committed run is 100; the env var is a smoke-test hook

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


def seed_of(d):
    """Draw 0 IS idea 158's published key."""
    return 158 if d == 0 else 180000 + d


# ---------------------------------------------------------------- the book (idea 158 verbatim)
def rk(x):
    return x.rank(axis=1, pct=True).clip(lower=0.05, upper=1.0) ** 0.5


def real_parts(px):
    """comp, 200d gate, vol20 and the FIVE real tilt multipliers - idea 158's `parts`, minus RAND."""
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True)
            + r3.rank(axis=1, pct=True)) / 3
    above = px > px.rolling(200).mean()
    v = px.pct_change().rolling(20).std() * np.sqrt(252)
    G = {"VOL": v.clip(lower=0.08) ** 0.5, "VOLR": rk(v), "MOM": rk(mom), "R6": rk(r6), "R3": rk(r3)}
    return comp, above, v, G


def null_key(px, seed):
    """idea 158's RAND, verbatim, with the seed exposed.  rng is fresh per panel, as it was there."""
    rng = np.random.default_rng(seed)
    sd = float(np.nanmedian(px.pct_change().std().values))
    steps = rng.normal(0.0, sd, size=px.shape)
    rw = pd.DataFrame(np.exp(np.cumsum(steps, axis=0)), index=px.index, columns=px.columns)
    return rk(rw / rw.shift(126) - 1)


def ranks_of(comp, elig, g, d):
    s = comp if d == "NONE" else (comp / g if d == "NEG" else comp * g)
    return s.where(elig).rank(axis=1, ascending=False)


# ---------------------------------------------------------------- vectorised simulator
class Sim:
    """engine.backtest, precomputed per panel: only the weights change between calls."""

    def __init__(self, px, freq=FREQ, lag=1):
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        mask = rebalance_mask(self.idx, freq).shift(lag, fill_value=False).values.copy()
        mask[0] = True
        T, N = self.rets.shape
        Cc = np.cumprod(1.0 + self.rets, axis=0)
        Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
        reb = np.flatnonzero(mask)
        seg = np.searchsorted(reb, np.arange(T), side="right") - 1
        self.s0 = reb[seg]
        self.s0p = reb[np.maximum(seg - 1, 0)]
        self.R = Cp / Cp[self.s0]
        self.Rp = Cp / Cp[self.s0p]
        self.reb = reb
        self.lag = lag
        self.T = T

    def run(self, W):
        wt = W.reindex(self.idx).fillna(0.0).shift(self.lag).fillna(0.0).values
        W0 = wt[self.s0]
        h = W0 * self.R
        V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
        held = h / V[:, None]
        W0p = wt[self.s0p]
        hp = W0p * self.Rp
        Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
        heldp = hp / Vp[:, None]
        heldp[self.reb[0]] = 0.0
        turn = np.zeros(self.T)
        turn[self.reb] = np.abs(wt[self.reb] - heldp[self.reb]).sum(axis=1)
        return (pd.Series((held * self.rets).sum(axis=1), index=self.idx),
                pd.Series(turn, index=self.idx))


# ---------------------------------------------------------------- one book -> one grid row
def row_of(r0, to, ctx, cost, **tags):
    r = r0 - to * cost / 1e4
    mm = metrics(r)
    mo, mi = metrics(H.window(r, "OOS")), metrics(H.window(r, "IS"))
    h1, h2 = H.halves(r)
    ih1, ih2 = H.halves(H.window(r, "IS"))
    mg = C.margins_at(r, ctx["bfull"], PHI0, DELTA0, "full")
    mgo = C.margins_at(r, ctx["bOOS"], PHI0, DELTA0, "OOS")
    d = dict(cost=cost, CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
             OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
             IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"], IS_H1=ih1, IS_H2=ih2,
             TO=to.sum() / mm["Years"],
             pass4a=H.pass4a(r, ctx["v1"][cost]),
             pass4b=(len(C.fails(mg)) == 0), fail4b=",".join(C.fails(mg)) or "-",
             pass4b_oos=all(mgo[k] > 0 for k in ("H1", "H2", "DD", "CAGR")))
    d.update(tags)
    return d


# ---------------------------------------------------------------- main
def main():
    say("=" * 190)
    say(f"IDEA 180 - is-the-null-key-result-one-draw-or-a-distribution   ({STEM})")
    say("Idea 158's null control is one seeded key.  Re-run its grid on 100 independent null keys "
        "and quote a band instead of a point.")
    say("=" * 190)

    ok = {}
    ctxs, real_rows, draw_rows = {}, [], []

    for pk in PANELS:
        px, spy_full, desc = C.panel(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        bfull, bIS, bOOS = (C.bars_win(spy, w) for w in ("full", "IS", "OOS"))
        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        comp, above, vol20, G = real_parts(px)
        elig = above & (vol20 < MAX_VOL)
        n_elig = float(elig.loc[start:].sum(axis=1).mean())
        nmap = {m: max(2, int(round(m * n_elig))) for m in SHARES}
        S = Sim(px)
        ctx = dict(px=px, start=start, spy=metrics(spy), spy_oos=metrics(spy.loc[OOS_START:]),
                   bfull=bfull, bIS=bIS, bOOS=bOOS, v1=v1, n_elig=n_elig, nmap=nmap,
                   comp=comp, elig=elig, G=G, S=S, desc=desc)
        ctxs[pk] = ctx

        say(f"\n[panel] {pk} = {desc}: {px.shape[1]} cols, eval from {start.date()}, mean weekly "
            f"eligible {n_elig:.2f}")
        say("    share -> n:  " + ", ".join(f"m={m:.2f}->n={nmap[m]}" for m in SHARES))
        pub_e = {"u56": 37.50, "broad": 91.46, "small": 141.23}[pk]
        ok[f"a:{pk}"] = abs(n_elig - pub_e) < 0.02
        say(f"    [a] idea 153/158 published mean eligible {pub_e:.2f} -> "
            f"{'MATCH' if ok[f'a:{pk}'] else 'MISMATCH'}")

        # ---- [A] the vectorised simulator against the engine, on this panel
        Wc = (ranks_of(comp, elig, None, "NONE") <= nmap[0.53]).astype(float) * (GROSS / nmap[0.53])
        e0 = backtest(px, Wc, cost_bps=0.0, freq=FREQ)
        r0, t0 = S.run(Wc)
        d1 = float((e0["returns"] - r0).abs().max())
        d2 = float((e0["turnover"] - t0).abs().max())
        e10 = backtest(px, Wc, cost_bps=10.0, freq=FREQ)["returns"]
        d3 = float((e10 - (r0 - t0 * 10.0 / 1e4)).abs().max())
        ok[f"A:{pk}"] = d1 < 1e-12 and d2 < 1e-10
        ok[f"D:{pk}"] = d3 < 1e-12
        say(f"    [A] Sim.run == engine.backtest: max|dret| {d1:.2e}, max|dturn| {d2:.2e} -> "
            f"{'PASS' if ok[f'A:{pk}'] else 'FAIL'}")
        say(f"    [D] cost identity vs a fresh 10 bps engine run: max|d| {d3:.2e} -> "
            f"{'PASS' if ok[f'D:{pk}'] else 'FAIL'}")

        # ---- the fixed part of the grid: NONE + the five real keys
        arms = [("NONE", "NONE")] + [(k, d) for k in REAL_KEYS for d in ("NEG", "POS")]
        for (key, dr) in arms:
            rnk = ranks_of(comp, elig, None if key == "NONE" else G[key], dr)
            for m in SHARES:
                n = nmap[m]
                W = (rnk <= n).astype(float) * (GROSS / n)
                r0, to = S.run(W)
                r0, to = r0.loc[start:], to.loc[start:]
                for c in COSTS:
                    real_rows.append(row_of(r0, to, ctx, c, panel=pk, m=m, n=n, key=key, dir=dr))

    RG = pd.DataFrame(real_rows)

    # ---- [C] the decisive control, on the real-key half of the grid
    say("")
    say(f"[C] reproduction of {PARENT}.grid.csv (literal books)")
    ref = pd.read_csv(OUT / f"{PARENT}.grid.csv")
    ref = ref[ref.constr == "lit"]
    cmpcols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
               "IS_Sharpe", "IS_CAGR", "IS_MaxDD", "IS_H1", "IS_H2", "TO"]
    kidx = ["panel", "m", "key", "dir", "cost"]
    a = RG.set_index(kidx)[cmpcols].sort_index()
    b = ref.set_index(kidx)[cmpcols].sort_index()
    common = a.index.intersection(b.index)
    worst = float((a.loc[common] - b.loc[common]).abs().to_numpy().max())
    ok["C_real"] = worst < 1e-9 and len(common) == len(a)
    say(f"    real keys + NONE: {len(common)} of {len(a)} rows matched, max|d| = {worst:.3e} -> "
        f"{'PASS' if ok['C_real'] else 'FAIL'}")

    # ---------------------------------------------------------------- the 100 draws
    say("")
    say(f"THE {N_DRAWS} NULL KEYS  (draw 0 = idea 158's seed 158; draws 1..{N_DRAWS-1} = "
        f"180001..{180000+N_DRAWS-1})")
    for d in range(N_DRAWS):
        for pk in PANELS:
            ctx = ctxs[pk]
            g = null_key(ctx["px"], seed_of(d))
            for dr in ("NEG", "POS"):
                rnk = ranks_of(ctx["comp"], ctx["elig"], g, dr)
                for m in SHARES:
                    n = ctx["nmap"][m]
                    W = (rnk <= n).astype(float) * (GROSS / n)
                    r0, to = ctx["S"].run(W)
                    r0, to = r0.loc[ctx["start"]:], to.loc[ctx["start"]:]
                    for c in COSTS:
                        draw_rows.append(row_of(r0, to, ctx, c, panel=pk, m=m, n=n,
                                               key="RAND", dir=dr, draw=d, seed=seed_of(d)))
        if (d + 1) % 10 == 0:
            say(f"    ... {d+1}/{N_DRAWS} draws done")
    DG = pd.DataFrame(draw_rows)
    RG.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    DG.to_csv(OUT / f"{STEM}.draws.csv", index=False)

    # ---- [C] continued: draw 0 must BE idea 158's published RAND rows
    a0 = DG[DG.draw == 0].set_index(kidx)[cmpcols].sort_index()
    b0 = ref[ref.key == "RAND"].set_index(kidx)[cmpcols].sort_index()
    common0 = a0.index.intersection(b0.index)
    w0 = float((a0.loc[common0] - b0.loc[common0]).abs().to_numpy().max())
    ok["C_draw0"] = w0 < 1e-9 and len(common0) == len(a0)
    say(f"    draw 0 vs idea 158's published RAND rows: {len(common0)} of {len(a0)} matched, "
        f"max|d| = {w0:.3e} -> {'PASS' if ok['C_draw0'] else 'FAIL'}")
    if not all(ok.values()):
        say("[WARNING] a control did not hold; read everything below with that in mind.")

    def band(x, lab, fmt="{:.4f}"):
        x = np.asarray(x, float)
        q = np.percentile(x, [0, 5, 25, 50, 75, 95, 100])
        say(f"    {lab:44s} mean {fmt.format(x.mean())}  sd {fmt.format(x.std(ddof=1))}  "
            f"[min {fmt.format(q[0])} | p5 {fmt.format(q[1])} | p50 {fmt.format(q[3])} | "
            f"p95 {fmt.format(q[5])} | max {fmt.format(q[6])}]")

    def pctile_of(x, v):
        x = np.asarray(x, float)
        return float((x < v).mean())

    # =============================================================== R1  |dSharpe|
    say("\n" + "=" * 190)
    say("R1  DISTRIBUTION OF |dSharpe| = |Sharpe(tilt) - Sharpe(NONE)| at matched (panel, m, cost)")
    say("=" * 190)
    none_sh = RG[RG.key == "NONE"].set_index(["panel", "m", "cost"]).Sharpe
    for df in (RG, DG):
        df["dSharpe"] = df.Sharpe.values - none_sh.reindex(
            pd.MultiIndex.from_arrays([df.panel, df.m, df.cost])).values
        df["absdS"] = df.dSharpe.abs()
    for restrict, lab in ((False, "FULL grid"), (True, "m <= 0.53 only")):
        Dm = DG[DG.m <= 0.53] if restrict else DG
        Rm = RG[RG.m <= 0.53] if restrict else RG
        say(f"\n  -- {lab} --")
        for pk in PANELS:
            per_draw = Dm[Dm.panel == pk].groupby("draw").absdS.mean()
            band(per_draw.values, f"{pk}: null-key mean |dSharpe| over {N_DRAWS} draws")
            reals = Rm[(Rm.panel == pk) & (Rm.key != "NONE")].groupby("key").absdS.mean()
            say("      real keys: " + "  ".join(f"{k} {v:.4f}" for k, v in reals.items())
                + f"   | mean of the 5 real keys {reals.mean():.4f} sits at the null band's "
                  f"{pctile_of(per_draw.values, reals.mean()):.0%} percentile")
            say(f"      draw 0 (idea 158's key) = {per_draw.loc[0]:.4f}, at the "
                f"{pctile_of(per_draw.values, per_draw.loc[0]):.0%} percentile of its own family")

    # =============================================================== R4  beats the live scaler
    say("\n" + "=" * 190)
    say("R4  \"a random key BEATS THE LIVE /sqrt(vol20) SCALER in k of 28 large-cap cells\"")
    say("    (28 cells = 2 large-cap panels x 7 shares x 2 cost rungs; idea 158 published 27 NEG "
        "and 23 POS on its single draw)")
    say("=" * 190)
    # the LIVE scaler is VOL/NEG; idea 158 compares BOTH null arms against it.
    vol = RG[(RG.key == "VOL") & (RG.dir == "NEG")].set_index(["panel", "m", "cost"]).Sharpe
    LC = ["u56", "broad"]
    for dr in ("NEG", "POS"):
        wins = []
        for d in range(N_DRAWS):
            s = DG[(DG.draw == d) & (DG.dir == dr) & (DG.panel.isin(LC))]
            v = vol.reindex(pd.MultiIndex.from_arrays([s.panel, s.m, s.cost])).values
            wins.append(int((s.Sharpe.values > v).sum()))
        band(wins, f"cells won by the null key, tilt {dr} (of 28)", "{:.2f}")
        say(f"      idea 158's published count: {27 if dr == 'NEG' else 23} of 28, at the "
            f"{pctile_of(wins, 27 if dr == 'NEG' else 23):.0%} percentile of the null band; "
            f"draws winning >= half the cells: {int((np.array(wins) >= 14).sum())}/{N_DRAWS}")
        sd_ = DG[(DG.dir == dr) & (DG.panel.isin(LC))].groupby("draw").dSharpe.mean().values
        band(sd_, f"mean SIGNED dSharpe over the 28 cells, tilt {dr}")
        say(f"      the live scaler VOL/NEG scores "
            f"{RG[(RG.key=='VOL') & (RG.dir=='NEG') & (RG.panel.isin(LC))].dSharpe.mean():+.4f} "
            f"on the same 28 cells (idea 158 published -0.1931); null draws WORSE than it: "
            f"{int((sd_ < RG[(RG.key=='VOL') & (RG.dir=='NEG') & (RG.panel.isin(LC))].dSharpe.mean()).sum())}"
            f"/{N_DRAWS}")

    # =============================================================== R2  4b pass count
    say("\n" + "=" * 190)
    say("R2  DISTRIBUTION OF THE NULL KEY'S 4b PASS COUNT")
    say(f"    each draw contributes 84 RAND cells (3 panels x 7 shares x 2 dirs x 2 costs); the "
        f"fixed part of the grid contributes {int(RG.pass4b.sum())} passes from "
        f"{len(RG)} NONE+real-key cells")
    say("=" * 190)
    p4b = DG.groupby("draw").pass4b.sum().values
    p4a = DG.groupby("draw").pass4a.sum().values
    p4bo = DG.groupby("draw").pass4b_oos.sum().values
    band(p4b, "null-key 4b passes (of 84)", "{:.2f}")
    band(p4a, "null-key 4a passes (of 84)", "{:.2f}")
    band(p4bo, "null-key 4b-on-the-OOS-window passes (of 84)", "{:.2f}")
    say(f"    idea 158's draw scored {int(p4b[0])} 4b passes, at the {pctile_of(p4b, p4b[0]):.0%} "
        f"percentile; draws with ZERO 4b passes: {int((p4b == 0).sum())}/{N_DRAWS}")
    tot = RG.pass4b.sum() + p4b
    say(f"    null-key SHARE of the whole grid's 4b passes: mean {np.mean(p4b/tot):.1%} "
        f"[min {np.min(p4b/tot):.1%}, max {np.max(p4b/tot):.1%}]   "
        f"(idea 158 published 11 of 54 = 20.4%)")
    say("    by panel (mean null-key 4b passes per draw, of 28 cells each):")
    for pk in PANELS:
        v = DG[DG.panel == pk].groupby("draw").pass4b.sum().values
        band(v, f"      {pk}", "{:.2f}")

    # =============================================================== R5  cross-universe
    say("\n" + "=" * 190)
    say("R5  CROSS-UNIVERSE 4b: (m, key, dir) combinations passing on more than one panel")
    say("=" * 190)
    xu_real = RG[RG.pass4b].groupby(["m", "key", "dir"]).panel.nunique()
    xu_real = int((xu_real > 1).sum())
    xu = []
    for d in range(N_DRAWS):
        s = DG[(DG.draw == d) & DG.pass4b]
        g = s.groupby(["m", "dir"]).panel.nunique()
        xu.append(int((g > 1).sum()))
    band(xu, "null-key cross-universe combinations", "{:.2f}")
    say(f"    fixed part of the grid (NONE + 5 real keys): {xu_real} cross-universe combinations; "
        f"idea 158 published 19 total of which 4 were its RAND draw")
    say(f"    draws with at least one cross-universe null pass: {int((np.array(xu) > 0).sum())}"
        f"/{N_DRAWS}")

    # =============================================================== R3  rule 8
    say("\n" + "=" * 190)
    say("R3  PROTOCOL RULE 8 - (m, key, dir) chosen on the IS window (<= 2016-12-31) only, "
        "read ONCE on 2017-01-01..")
    say("=" * 190)
    wrows = []
    for d in range(N_DRAWS):
        for pk in PANELS:
            for c in COSTS:
                fixed = RG[(RG.panel == pk) & (RG.cost == c)]
                rnd = DG[(DG.draw == d) & (DG.panel == pk) & (DG.cost == c)]
                allarms = pd.concat([fixed, rnd], ignore_index=True)
                ctl = fixed[(fixed.key == "NONE") & (fixed.m == 0.53)].iloc[0]
                nones = fixed[fixed.key == "NONE"]
                picks = {"S1_all": allarms.loc[allarms.IS_Sharpe.idxmax()],
                         "S2_donothing": ctl,
                         "S3_RANDonly": rnd.loc[rnd.IS_Sharpe.idxmax()],
                         "S4_NONEonly": nones.loc[nones.IS_Sharpe.idxmax()]}
                for nm, r_ in picks.items():
                    wrows.append(dict(draw=d, panel=pk, cost=c, sel=nm, key=r_.key, dir=r_["dir"],
                                      m=r_.m, IS_Sharpe=r_.IS_Sharpe, OOS_CAGR=r_.OOS_CAGR,
                                      OOS_Sharpe=r_.OOS_Sharpe, OOS_MaxDD=r_.OOS_MaxDD,
                                      pass4b_oos=r_.pass4b_oos))
    WF = pd.DataFrame(wrows)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    v1o = np.mean([metrics(ctxs[pk]["v1"][c].loc[OOS_START:])["Sharpe"]
                   for pk in PANELS for c in COSTS])
    spyo = np.mean([ctxs[pk]["spy_oos"]["Sharpe"] for pk in PANELS for c in COSTS])
    v1oc = np.mean([metrics(ctxs[pk]["v1"][c].loc[OOS_START:])["CAGR"]
                    for pk in PANELS for c in COSTS])
    spyoc = np.mean([ctxs[pk]["spy_oos"]["CAGR"] for pk in PANELS for c in COSTS])
    say("  mean OOS Sharpe over the 6 (panel, cost) cells, as a distribution over draws:")
    for nm in ("S1_all", "S2_donothing", "S3_RANDonly", "S4_NONEonly"):
        v = WF[WF.sel == nm].groupby("draw").OOS_Sharpe.mean().values
        band(v, nm)
        if nm == "S3_RANDonly":
            say(f"      idea 158 published S3 = 0.7240; this run's draw 0 = {v[0]:.4f}, at the "
                f"{pctile_of(v, v[0]):.0%} percentile")
    say(f"    {'RULES v1 (fixed)':44s} {v1o:.4f}   (OOS CAGR {v1oc:.2%})")
    say(f"    {'SPY (fixed)':44s} {spyo:.4f}   (OOS CAGR {spyoc:.2%})")
    s2m = WF[WF.sel == "S2_donothing"].groupby("draw").OOS_Sharpe.mean().values[0]
    for nm in ("S1_all", "S3_RANDonly", "S4_NONEonly"):
        v = WF[WF.sel == nm].groupby("draw").OOS_Sharpe.mean().values
        say(f"    {nm} beats the do-nothing control ({s2m:.4f}) in "
            f"{int((v > s2m).sum())}/{N_DRAWS} draws; beats SPY ({spyo:.4f}) in "
            f"{int((v > spyo).sum())}/{N_DRAWS}")
    s1 = WF[WF.sel == "S1_all"]
    picked = s1.groupby("draw").apply(lambda g: int((g.key == "RAND").sum()), include_groups=False)
    band(picked.values, "cells (of 6) where S1 PICKS the null key", "{:.2f}")
    say(f"    draws where S1 picks the null key at least once: "
        f"{int((picked.values > 0).sum())}/{N_DRAWS}   "
        f"(idea 158: yes, on broad@10bps)")
    bc = s1[(s1.panel == "broad") & (s1.cost == 10.0)]
    say(f"    broad@10bps specifically: S1 picks the null key in "
        f"{int((bc.key == 'RAND').sum())}/{N_DRAWS} draws")

    say("\n" + "=" * 190)
    say("CONTROLS - outcome")
    for k_, v_ in ok.items():
        say(f"    {k_}: {'PASS' if v_ else 'FAIL'}")
    say("=" * 190)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
