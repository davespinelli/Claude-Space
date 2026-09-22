#!/usr/bin/env python3
"""
Idea 2307 (lane cloud, 2026-09-22) — is the BAND BOOK's IDLE-CASH SHARE a MARKET-LEVEL object
or a CROSS-SECTIONAL one?

THE PREMISE.  RULES v2 clause 2 gates every name on its OWN 200d +/-3% band and clause 4 sends
the gated-out weight to CASH, so the book's realised mean gross is 0.5327 against a nominal
0.75 (idea 2304): ~29% of NAV sits idle because names are individually OUT.  Every device the
record has priced tries to SPEND that cash.  Nobody has asked what the IN-BAND SHARE itself is.

THE DECOMPOSITION.  Let N_t = names priced at t and S_t = (# IN at t) / N_t, the in-band SHARE
-- the book's own gross path in units of nominal gross.  Write the daily gate matrix as

        1{IN_it}  =  S_t            (a MARKET-WIDE level: one number a day)
                  +  (1{IN_it} - S_t)   (a CROSS-SECTIONAL residual, zero mean by row)

and price the two halves as BOOKS:

  NAME(c)   w_it = (g / N_t) * 1{IN_it}                 the live construction (both terms)
  LVL(c, L) w_it = (g / N_t) * mean_L(S)_t   for EVERY priced name (the level term only)

At L = 1, LVL's gross is S_t * g on EVERY row -- bit-identical to NAME's gross (gate G7) -- so
LVL(c,1) is the EXPOSURE-MATCHED, INFORMATION-FREE twin of the live book: same cash share every
day, same nominal gross, but it spreads the invested part over ALL priced names instead of the
IN ones.  r_NAME - r_LVL1 is therefore a PURE cross-sectional-residual return, and

        VAR SHARE OF THE RESIDUAL  =  var(r_NAME - r_LVL1) / var(r_NAME)
        R^2 OF THE LEVEL          =  corr(r_NAME, r_LVL1)^2

answer the queue's question directly.  L > 1 slows the level term to a moving average of the
share, which is the same book with the cash decision made on stale market-level information
only; var(mean_L(S)) / var(S) publishes how much of the share's own variance that window keeps.

THE QUEUE'S OWN FALSIFIER: "if the residual explains nothing, the 56 name gates are one market
gate with extra turnover."  Pre-registered here BEFORE any number was read, at 10 bps:
  (i)  NAME beats its own LVL(c,1) twin on FULL-sample Sharpe at a MAJORITY of the 15
       (panel x c) cells, AND
  (ii) that margin exceeds 2 SE on a PAIRED circular-block bootstrap at >= 1 cell, AND
  (iii) NAME's turnover premium over the twin is PAID FOR: the Sharpe margin survives at the
       25 bps rung as well.
Failing (i) or (ii) is the pre-registered KILL of the name-gate's cross-sectional content.
Clearing them is a MECHANISM finding; a CAPITAL claim additionally needs a KEEP path.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
  c {0.00, 0.02, 0.03, 0.05, 0.08}   DIAL 1 -- band half-width.  0.03 is the live value.
  L {1, 5, 21, 63, 126}              DIAL 2 -- decomposition window (trading days).  L = 1 is
                                     the contemporaneous share, i.e. the exact decomposition.
25 books per panel (5 NAME + 20 LVL), EVERY ONE published in .grid.csv.

FROZEN, NEVER VARIED: gross 0.75; weekly cadence; t+1; warm-up 260 rows; the gate is RULES v2's
own hysteresis band (baseline.band_state) at half-width c.
NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} and COST RUNG {0, 10, 25, 50} bps.
The verdict is quoted at PROTOCOL's 10 bps; the other rungs are published, never selected on.

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, 10 bps, no shorting, no leverage); rule 3 (live RULES v2
AND SPY); rule 4 (both KEEP paths at every cell, exactly 2 tuned parameters); rule 8 (walk
forward: (c, L) chosen on warm-up..2016-12-31 ONLY by two pre-registered IS-only choosers,
2017-2026 read ONCE); rule 9 (SURVIVORSHIP STATED: U56 and B136 are CURRENT-constituent lists
held from 2008 and SMALL is a CURRENT sub-$2B screen from 2010, so absolute levels are biased
UP; the object here is a WITHIN-PANEL contrast -- book vs its own exposure-matched twin on the
same names and the same days -- which is first-order immune, the pass counts are not).  Tickers
with max_1d_move >= 1.0 in data/small_meta.csv are DROPPED before anything is computed.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

GATES.  G0 sample >= 10y on every panel.  G1 NAME(0.03) on U56 reproduces baseline.rules_v2 to
< 1e-12 in daily return.  G2 cost-rung algebra (returns_0 - turnover * bps/1e4) reproduces the
engine's own priced run bit-for-bit.  G3 EXPOSURE CHANNEL SHUT at L = 1: max |gross_NAME -
gross_LVL1| < 1e-12 on every row.  G4 LVL holds EVERY priced name on every row (zero
cross-sectional information).  G5 all 25 books published per panel.  G6 exactly two tuned
parameters.  G7 the rule-8 choosers read no row on or after 2017-01-01.  G8 no leverage: gross
<= 0.75 + 1e-12 on every row of every book.  G9 the c dial BITES (spread of mean in-band share across c >= 0.01; monotonicity is
PUBLISHED, not asserted -- hysteresis makes a wider band delay entry AND exit).  G10 the L dial BITES (var(mean_L(S)) strictly decreasing in L).  G11 the dropped-ticker
rule bit on SMALL (>= 1 name removed).  G12 bit-identical recompute of the U56 headline cell.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-22_band-share-market-vs-cross-sectional_cloud.py
"""
from __future__ import annotations

import sys, time, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state   # noqa: E402
from engine import backtest, metrics                               # noqa: E402

DATE, SLUG = "2026-09-22", "band-share-market-vs-cross-sectional"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

GROSS, CADENCE, WARMUP = 0.75, "W", 260
CS = [0.00, 0.02, 0.03, 0.05, 0.08]
LS = [1, 5, 21, 63, 126]
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG = 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BOOT_REPS, BOOT_BLOCK, SEED = 400, 63, 20260922

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


def bcol(df, name):
    """Leg columns carry NaN on the SPY / BASE_v2 reference rows; read them as booleans."""
    return df[name].fillna(False).astype(bool)


# ---------------------------------------------------------------- books
def name_weights(px, invest, c):
    """RULES v2 clause 2+4 at half-width c, restricted to the investable columns."""
    q = px[invest]
    e = pd.DataFrame(1.0, index=q.index, columns=q.columns).where(q.notna(), 0.0)
    ew = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    w = ew.where(band_state(q, c), 0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


def share_series(px, invest, c):
    """S_t = (# IN) / (# priced), the in-band SHARE."""
    q = px[invest]
    pr = q.notna()
    inb = band_state(q, c) & pr
    return (inb.sum(axis=1) / pr.sum(axis=1).replace(0, np.nan)).fillna(0.0)


def level_weights(px, invest, c, L, S=None):
    """LVL(c, L): every priced name at (g / N_t) * mean_L(S)_t.  Zero cross-sectional info."""
    q = px[invest]
    S = share_series(px, invest, c) if S is None else S
    SL = S.rolling(L, min_periods=1).mean() if L > 1 else S
    e = pd.DataFrame(1.0, index=q.index, columns=q.columns).where(q.notna(), 0.0)
    ew = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    w = ew.mul(SL, axis=0)
    return w.reindex(columns=px.columns).fillna(0.0)


def run(px, w):
    """One zero-cost run; cost rungs are applied afterwards from the turnover series (gate G2)."""
    res = backtest(px, w, cost_bps=0.0, freq=CADENCE)
    return res["returns"], res["turnover"], res["weights"].sum(axis=1)


def priced(r, to, bps):
    return r - to * bps / 1e4


# ---------------------------------------------------------------- metrics / KEEP paths
def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    eq = (1 + r).cumprod()
    return float(eq.iloc[-1] ** (252 / len(r)) - 1)


def maxdd(r):
    eq = (1 + r).cumprod()
    return float((eq / eq.cummax() - 1).min())


def halves(r):
    h = len(r) // 2
    return sharpe(r.iloc[:h]), sharpe(r.iloc[h:])


def legs(r, base, spy, r_oos, spy_oos):
    """PROTOCOL rule 4, both paths, on the window r spans (OOS leg from r_oos)."""
    h1, h2 = halves(r)
    b1, b2 = halves(base)
    p4a = (h1 > b1) and (h2 > b2) and (maxdd(r) >= maxdd(base))
    s1, s2 = halves(spy)
    L_H1, L_H2 = h1 > s1, h2 > s2
    L_OOS = sharpe(r_oos) > sharpe(spy_oos)
    L_DD = maxdd(r) >= DD_CAP * maxdd(spy)          # both negative: |dd| <= 0.60 |spy dd|
    L_CAGR = cagr(r) >= CAGR_FLOOR * cagr(spy)
    return dict(pass4a=bool(p4a), pass4b=bool(L_H1 and L_H2 and L_OOS and L_DD and L_CAGR),
                L_H1=bool(L_H1), L_H2=bool(L_H2), L_OOS=bool(L_OOS), L_DD=bool(L_DD),
                L_CAGR=bool(L_CAGR))


def boot_sharpe_diff(a, b, reps=BOOT_REPS, block=BOOT_BLOCK, seed=SEED):
    """Paired circular block bootstrap on the Sharpe difference (same blocks for both arms)."""
    rng = np.random.default_rng(seed)
    x, y = a.values, b.values
    n = len(x)
    nb = int(np.ceil(n / block))
    obs = sharpe(a) - sharpe(b)
    out = np.empty(reps)
    for i in range(reps):
        st = rng.integers(0, n, nb)
        idx = np.concatenate([(np.arange(s, s + block) % n) for s in st])[:n]
        xs, ys = x[idx], y[idx]
        sx = xs.mean() * 252 / (xs.std() * np.sqrt(252)) if xs.std() > 0 else np.nan
        sy = ys.mean() * 252 / (ys.std() * np.sqrt(252)) if ys.std() > 0 else np.nan
        out[i] = sx - sy
    se = float(np.nanstd(out))
    return float(obs), se, (float(obs / se) if se > 0 else np.nan)


# ---------------------------------------------------------------- panels
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"].astype(str))
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    dropped = len(px.columns) - len(keep)
    return px[keep], dropped


def main():
    t0 = time.time()
    say("=== idea 2307 — is the band book's IDLE-CASH SHARE a MARKET-LEVEL object or a CROSS-SECTIONAL one? ===")
    say(f"    {DATE}  lane cloud   cadence {CADENCE}  gross {GROSS}  t+1  rungs {RUNGS} bps  headline {HEADLINE_RUNG:.0f} bps")
    say(f"    DIAL 1 band c {CS}   DIAL 2 window L {LS}   (exactly two tuned parameters)")

    px_u = load_universe()
    px_b = load_universe(broad=True)
    px_s, dropped = small_panel()
    gate("G11 dropped-ticker rule bit (SMALL)", f"{dropped} names dropped (max_1d_move >= 1.0)", ">= 1", dropped >= 1)
    gate("G6 exactly two tuned parameters", "c (band half-width), L (decomposition window)", "2", True)

    panels = {}
    for nm, px in (("U56", px_u), ("B136", px_b), ("SMALL", px_s)):
        invest = [c for c in px.columns if c != "SPY"] if nm == "SMALL" else list(px.columns)
        panels[nm] = (px, invest)
        say(f"    {nm:5s} {len(invest)} investable names, {px.index[0].date()}..{px.index[-1].date()}, {len(px)} rows")

    # ---- G1/G2: construction identity against the live baseline, and the cost algebra
    w_live = rules_v2_weights(px_u, band=0.03, gross=GROSS)
    r_live0, to_live, g_live = run(px_u, w_live)
    r_mine0, to_mine, g_mine = run(px_u, name_weights(px_u, list(px_u.columns), 0.03))
    gate("G1 NAME(0.03) == baseline.rules_v2 on U56", f"max|d| {float((r_live0 - r_mine0).abs().max()):.3e}", "< 1e-12",
         float((r_live0 - r_mine0).abs().max()) < 1e-12)
    r_eng = backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    d_cost = float((r_eng - priced(r_live0, to_live, HEADLINE_RUNG)).abs().max())
    gate("G2 cost-rung algebra == engine", f"max|d| {d_cost:.3e}", "< 1e-12", d_cost < 1e-12)

    grid, dec_rows, boot_rows = [], [], []
    store: dict = {}

    for pname, (px, invest) in panels.items():
        say(f"\n--- PANEL {pname} ---")
        idx = px.index
        i0 = WARMUP
        win = idx[i0:]
        oos_mask = win >= pd.Timestamp(OOS_START)
        is_mask = win <= pd.Timestamp(IS_END)
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        gate(f"G0 sample >= 10y ({pname})", f"{len(win)/252:.1f} yr", ">= 10", len(win) / 252 >= 10)

        # panel baseline = RULES v2 construction on THAT panel (the live book itself on U56)
        base0, base_to, _ = run(px, rules_v2_weights(px, band=0.03, gross=GROSS))
        base = {c: priced(base0, base_to, c).loc[win] for c in RUNGS}

        shares = {c: share_series(px, invest, c) for c in CS}
        mean_share = {c: float(shares[c].loc[win].mean()) for c in CS}
        spread = max(mean_share.values()) - min(mean_share.values())
        gate(f"G9 c dial bites ({pname})", " ".join(f"{c}:{mean_share[c]:.4f}" for c in CS),
             "spread of mean share across c >= 0.01", spread >= 0.01)
        publish(f"G9b mean share MONOTONE in c ({pname})",
                "YES" if all(mean_share[CS[i]] > mean_share[CS[i + 1]] for i in range(len(CS) - 1))
                else f"NO (hysteresis: a wider band delays BOTH entry and exit); spread {spread:.4f}")

        for c in CS:
            S = shares[c]
            wn = name_weights(px, invest, c)
            rn0, ton, gn = run(px, wn)
            rows_lvl = {}
            for L in LS:
                wl = level_weights(px, invest, c, L, S=S)
                rl0, tol, gl = run(px, wl)
                rows_lvl[L] = (rl0, tol, gl, wl)
            # G3 exposure channel shut at L=1 (target weights, pre-drift)
            dg = float((wn.sum(axis=1) - rows_lvl[1][3].sum(axis=1)).abs().max())
            gate(f"G3 exposure matched at L=1 ({pname} c={c})", f"max|d gross| {dg:.3e}", "< 1e-12", dg < 1e-12)
            # G4 LVL holds every priced name
            nm_held = int((rows_lvl[1][3][invest] > 0).sum(axis=1).iloc[i0:].min())
            npriced = int(px[invest].notna().sum(axis=1).iloc[i0:].min())
            gate(f"G4 LVL holds every priced name ({pname} c={c})", f"min held {nm_held} vs min priced {npriced}",
                 "equal", nm_held == npriced)
            gate(f"G8 no leverage ({pname} c={c})", f"max gross {float(wn.sum(axis=1).max()):.6f}",
                 f"<= {GROSS}+1e-12", float(wn.sum(axis=1).max()) <= GROSS + 1e-12)

            for L in LS:
                SL = S.rolling(L, min_periods=1).mean() if L > 1 else S
                vshare = float(SL.loc[win].var() / S.loc[win].var()) if S.loc[win].var() > 0 else np.nan
                dec_rows.append(dict(panel=pname, c=c, L=L, var_ratio_levelshare=vshare,
                                     mean_share=mean_share[c], mean_share_L=float(SL.loc[win].mean())))

            for rung in RUNGS:
                rn = priced(rn0, ton, rung).loc[win]
                bb = base[rung]
                store[(pname, c, "NAME", rung)] = rn
                rec = dict(panel=pname, c=c, book="NAME", L=np.nan, cost_bps=rung,
                           CAGR=cagr(rn), Sharpe=sharpe(rn), MaxDD=maxdd(rn),
                           H1=halves(rn)[0], H2=halves(rn)[1],
                           OOS_CAGR=cagr(rn[oos_mask]), OOS_Sharpe=sharpe(rn[oos_mask]), OOS_MaxDD=maxdd(rn[oos_mask]),
                           IS_Sharpe=sharpe(rn[is_mask]),
                           turnover_yr=float(ton.loc[win].sum() / (len(win) / 252)),
                           mean_gross=float(gn.loc[win].mean()))
                rec.update({f"FULL_{k}": v for k, v in legs(rn, bb, spy, rn[oos_mask], spy[oos_mask]).items()})
                rec.update({f"OOS_{k}": v for k, v in legs(rn[oos_mask], bb[oos_mask], spy[oos_mask],
                                                          rn[oos_mask], spy[oos_mask]).items()})
                grid.append(rec)
                for L in LS:
                    rl0, tol, gl, _ = rows_lvl[L]
                    rl = priced(rl0, tol, rung).loc[win]
                    store[(pname, c, f"LVL{L}", rung)] = rl
                    rec = dict(panel=pname, c=c, book=f"LVL{L}", L=L, cost_bps=rung,
                               CAGR=cagr(rl), Sharpe=sharpe(rl), MaxDD=maxdd(rl),
                               H1=halves(rl)[0], H2=halves(rl)[1],
                               OOS_CAGR=cagr(rl[oos_mask]), OOS_Sharpe=sharpe(rl[oos_mask]), OOS_MaxDD=maxdd(rl[oos_mask]),
                               IS_Sharpe=sharpe(rl[is_mask]),
                               turnover_yr=float(tol.loc[win].sum() / (len(win) / 252)),
                               mean_gross=float(gl.loc[win].mean()))
                    rec.update({f"FULL_{k}": v for k, v in legs(rl, bb, spy, rl[oos_mask], spy[oos_mask]).items()})
                    rec.update({f"OOS_{k}": v for k, v in legs(rl[oos_mask], bb[oos_mask], spy[oos_mask],
                                                               rl[oos_mask], spy[oos_mask]).items()})
                    grid.append(rec)

            # ---- the decomposition itself, at every rung (residual = NAME - LVL1)
            for rung in RUNGS:
                rn = store[(pname, c, "NAME", rung)]
                rl = store[(pname, c, "LVL1", rung)]
                resid = rn - rl
                rho = float(np.corrcoef(rn.values, rl.values)[0, 1])
                dec_rows.append(dict(panel=pname, c=c, L=0, cost_bps=rung,
                                     rho_name_lvl1=rho, R2_level=rho ** 2,
                                     var_share_resid=float(resid.var() / rn.var()),
                                     resid_ann_ret=float(resid.mean() * 252),
                                     resid_sharpe=sharpe(resid),
                                     d_CAGR=cagr(rn) - cagr(rl), d_Sharpe=sharpe(rn) - sharpe(rl),
                                     d_MaxDD=maxdd(rn) - maxdd(rl)))

        # ---- paired bootstrap on the headline rung, NAME vs its own LVL1 twin
        for c in CS:
            for rung in (HEADLINE_RUNG, 25.0):
                obs, se, t = boot_sharpe_diff(store[(pname, c, "NAME", rung)], store[(pname, c, "LVL1", rung)])
                boot_rows.append(dict(panel=pname, c=c, cost_bps=rung, d_Sharpe=obs, SE=se, t=t))

        # ---- SPY / baseline reference rows
        grid.append(dict(panel=pname, c=np.nan, book="SPY", L=np.nan, cost_bps=0.0,
                         CAGR=cagr(spy), Sharpe=sharpe(spy), MaxDD=maxdd(spy), H1=halves(spy)[0], H2=halves(spy)[1],
                         OOS_CAGR=cagr(spy[oos_mask]), OOS_Sharpe=sharpe(spy[oos_mask]), OOS_MaxDD=maxdd(spy[oos_mask]),
                         IS_Sharpe=sharpe(spy[is_mask]), turnover_yr=0.0, mean_gross=1.0))
        for rung in RUNGS:
            bb = base[rung]
            grid.append(dict(panel=pname, c=np.nan, book="BASE_v2", L=np.nan, cost_bps=rung,
                             CAGR=cagr(bb), Sharpe=sharpe(bb), MaxDD=maxdd(bb), H1=halves(bb)[0], H2=halves(bb)[1],
                             OOS_CAGR=cagr(bb[oos_mask]), OOS_Sharpe=sharpe(bb[oos_mask]), OOS_MaxDD=maxdd(bb[oos_mask]),
                             IS_Sharpe=sharpe(bb[is_mask]), turnover_yr=float(base_to.loc[win].sum() / (len(win) / 252)),
                             mean_gross=np.nan))

    G = pd.DataFrame(grid)
    D = pd.DataFrame(dec_rows)
    B = pd.DataFrame(boot_rows)
    gate("G5 all books published", f"{len(G[(G.book!='SPY')&(G.book!='BASE_v2')])} rows = 3 panels x 5 c x 6 books x 4 rungs",
         "360", len(G[(G.book != 'SPY') & (G.book != 'BASE_v2')]) == 360)

    dl = D[D.L > 0].drop_duplicates(subset=["panel", "c", "L"])
    ok_L = all(
        all(dl[(dl.panel == p) & (dl.c == c)].sort_values("L").var_ratio_levelshare.diff().dropna() < 0)
        for p in dl.panel.unique() for c in CS)
    gate("G10 L dial bites", "var(mean_L(S))/var(S) strictly decreasing in L at every (panel, c)", "True", ok_L)

    # ---------------------------------------------------------------- headline readings
    say("\n=== DECOMPOSITION (10 bps): how much of the live book's return is the MARKET LEVEL? ===")
    d10 = D[(D.L == 0) & (D.cost_bps == HEADLINE_RUNG)]
    say(d10[["panel", "c", "rho_name_lvl1", "R2_level", "var_share_resid", "d_CAGR", "d_Sharpe", "d_MaxDD",
             "resid_ann_ret", "resid_sharpe"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n=== SHARE-LEVEL VARIANCE KEPT BY WINDOW L (var(mean_L(S)) / var(S)) ===")
    piv = dl.pivot_table(index=["panel", "c"], columns="L", values="var_ratio_levelshare")
    say(piv.to_string(float_format=lambda x: f"{x:.4f}"))

    say("\n=== NAME vs its EXPOSURE-MATCHED LVL1 TWIN — paired block bootstrap on Sharpe ===")
    say(B.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    g10 = G[(G.cost_bps == HEADLINE_RUNG) & (G.book.isin(["NAME"] + [f"LVL{L}" for L in LS]))]
    say("\n=== FULL-SAMPLE GRID AT 10 bps (all 90 books) ===")
    say(g10[["panel", "c", "book", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "turnover_yr",
             "mean_gross", "FULL_pass4a", "FULL_pass4b"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # pre-registered bar
    win_cells, tot_cells, boot_hits, win25 = 0, 0, 0, 0
    for p in ["U56", "B136", "SMALL"]:
        for c in CS:
            tot_cells += 1
            a = store[(p, c, "NAME", HEADLINE_RUNG)]
            b = store[(p, c, "LVL1", HEADLINE_RUNG)]
            if sharpe(a) > sharpe(b):
                win_cells += 1
            if sharpe(store[(p, c, "NAME", 25.0)]) > sharpe(store[(p, c, "LVL1", 25.0)]):
                win25 += 1
    boot_hits = int((B[(B.cost_bps == HEADLINE_RUNG)].t.abs() > 2).sum())
    boot_pos = int(((B[(B.cost_bps == HEADLINE_RUNG)].t > 2)).sum())
    bar_i = win_cells > tot_cells / 2
    bar_ii = boot_pos >= 1
    bar_iii = win25 > tot_cells / 2
    say(f"\n=== PRE-REGISTERED BAR (10 bps) ===")
    say(f"    (i)   NAME > LVL1 on Sharpe at {win_cells} of {tot_cells} cells -> {'PASS' if bar_i else 'FAIL'}")
    say(f"    (ii)  paired-bootstrap t > +2 at {boot_pos} of {tot_cells} cells (|t| > 2 at {boot_hits}) -> {'PASS' if bar_ii else 'FAIL'}")
    say(f"    (iii) margin survives 25 bps at {win25} of {tot_cells} cells -> {'PASS' if bar_iii else 'FAIL'}")

    # ---------------------------------------------------------------- rule 8 walk-forward
    say("\n=== RULE 8 WALK-FORWARD — (c, L) chosen on <= 2016-12-31 ONLY, 2017-2026 read ONCE ===")
    wf_rows = []
    base_cache = {}
    for p in ["U56", "B136", "SMALL"]:
        pxp, _inv = panels[p]
        b0, bto, _ = run(pxp, rules_v2_weights(pxp, band=0.03, gross=GROSS))
        base_cache[p] = (b0, bto)
    for p in ["U56", "B136", "SMALL"]:
        px, invest = panels[p]
        win = px.index[WARMUP:]
        oos_mask = win >= pd.Timestamp(OOS_START)
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        for rung in RUNGS:
            cand = {}
            for c in CS:
                cand[(c, "NAME", np.nan)] = store[(p, c, "NAME", rung)]
                for L in LS:
                    cand[(c, f"LVL{L}", L)] = store[(p, c, f"LVL{L}", rung)]
            isw = {k: v[~oos_mask] for k, v in cand.items()}
            gate_ok = all(v.index.max() <= pd.Timestamp(IS_END) for v in isw.values())
            if rung == HEADLINE_RUNG and p == "U56":
                gate("G7 choosers read no OOS row", f"max IS date {max(v.index.max() for v in isw.values()).date()}",
                     f"<= {IS_END}", gate_ok)
            for chooser, key in (("C_ISSHARPE", lambda r: sharpe(r)),
                                 ("C_ISCALMAR", lambda r: (cagr(r) / abs(maxdd(r)) if maxdd(r) < 0 else np.nan))):
                pick = max(isw, key=lambda k: (key(isw[k]) if np.isfinite(key(isw[k])) else -1e9))
                r = cand[pick]
                ro, so = r[oos_mask], spy[oos_mask]
                base0, base_to = base_cache[p]
                bo = priced(base0, base_to, rung).loc[win][oos_mask]
                lg = legs(ro, bo, so, ro, so)
                wf_rows.append(dict(panel=p, cost_bps=rung, chooser=chooser, pick_c=pick[0], pick_book=pick[1],
                                    OOS_CAGR=cagr(ro), OOS_Sharpe=sharpe(ro), OOS_MaxDD=maxdd(ro),
                                    BASE_OOS_CAGR=cagr(bo), BASE_OOS_Sharpe=sharpe(bo), BASE_OOS_MaxDD=maxdd(bo),
                                    SPY_OOS_CAGR=cagr(so), SPY_OOS_Sharpe=sharpe(so), SPY_OOS_MaxDD=maxdd(so),
                                    **{f"OOS_{k}": v for k, v in lg.items()}))
            # zero-parameter reference: the live construction at the live band
            r = store[(p, 0.03, "NAME", rung)]
            ro, so = r[oos_mask], spy[oos_mask]
            base0, base_to = base_cache[p]
            bo = priced(base0, base_to, rung).loc[win][oos_mask]
            lg = legs(ro, bo, so, ro, so)
            wf_rows.append(dict(panel=p, cost_bps=rung, chooser="C_ZEROPARAM(live c=0.03 NAME)", pick_c=0.03,
                                pick_book="NAME", OOS_CAGR=cagr(ro), OOS_Sharpe=sharpe(ro), OOS_MaxDD=maxdd(ro),
                                BASE_OOS_CAGR=cagr(bo), BASE_OOS_Sharpe=sharpe(bo), BASE_OOS_MaxDD=maxdd(bo),
                                SPY_OOS_CAGR=cagr(so), SPY_OOS_Sharpe=sharpe(so), SPY_OOS_MaxDD=maxdd(so),
                                **{f"OOS_{k}": v for k, v in lg.items()}))
    W = pd.DataFrame(wf_rows)
    say(W[W.cost_bps == HEADLINE_RUNG][["panel", "chooser", "pick_c", "pick_book", "OOS_CAGR", "OOS_Sharpe",
                                        "OOS_MaxDD", "BASE_OOS_Sharpe", "SPY_OOS_Sharpe", "OOS_pass4a",
                                        "OOS_pass4b"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- KEEP-path census
    say("\n=== BOTH KEEP PATHS, EVERY CELL ===")
    for rung in RUNGS:
        sub = G[(G.cost_bps == rung) & (~G.book.isin(["SPY", "BASE_v2"]))]
        say(f"    {rung:4.0f} bps: 4a FULL {int(bcol(sub, 'FULL_pass4a').sum())} of {len(sub)}   "
            f"4b FULL {int(bcol(sub, 'FULL_pass4b').sum())} of {len(sub)}   "
            f"4a OOS {int(bcol(sub, 'OOS_pass4a').sum())} of {len(sub)}   "
            f"4b OOS {int(bcol(sub, 'OOS_pass4b').sum())} of {len(sub)}")
    p4b = G[(~G.book.isin(["SPY", "BASE_v2"])) & bcol(G, "FULL_pass4b")]
    if len(p4b):
        say("    4b FULL passers:")
        say(p4b[["panel", "c", "book", "cost_bps", "CAGR", "Sharpe", "MaxDD", "OOS_Sharpe"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))
    fails = G[(G.cost_bps == HEADLINE_RUNG) & (~G.book.isin(["SPY", "BASE_v2"])) & (~bcol(G, "FULL_pass4b"))]
    say(f"    binding legs on the {len(fails)} FULL 4b failures at 10 bps (count of cells the leg FAILS): "
        + json.dumps({k: int((~bcol(fails, k)).sum()) for k in
                      ["FULL_L_H1", "FULL_L_H2", "FULL_L_OOS", "FULL_L_DD", "FULL_L_CAGR"]}))

    # G12 bit-identical recompute of the headline cell
    px, invest = panels["U56"]
    r2, to2, _ = run(px, name_weights(px, invest, 0.03))
    d12 = float((priced(r2, to2, HEADLINE_RUNG).loc[px.index[WARMUP:]] - store[("U56", 0.03, "NAME", HEADLINE_RUNG)]).abs().max())
    gate("G12 headline cell recompute", f"max|d| {d12:.3e}", "< 1e-12", d12 < 1e-12)

    OUT.mkdir(parents=True, exist_ok=True)
    G.to_csv(OUT / "grid.csv", index=False)
    D.to_csv(OUT / "decomposition.csv", index=False)
    B.to_csv(OUT / "bootstrap.csv", index=False)
    W.to_csv(OUT / "walkforward.csv", index=False)
    pd.DataFrame(GATES).to_csv(OUT / "gates.csv", index=False)
    (OUT / "console.txt").write_text("\n".join(LOG) + "\n")
    say(f"\n    wrote {OUT}  ({time.time() - t0:.1f}s)")
    say(f"    GATES: {sum(1 for g in GATES if g['pass_'])} pass / {sum(1 for g in GATES if not g['pass_'])} fail")
    (OUT / "console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
