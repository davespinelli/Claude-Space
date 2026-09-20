#!/usr/bin/env python3
"""Idea 1757 (lane C, 2026-09-20): is the 4b CAGR FLOOR just a GROSS BAR in disguise?

Across idea 1741's 1,188 cells the 4b legs fail at H1 417 / H2 606 / DD 370 / **CAGR 1,049**:
the CAGR floor is the binding leg almost everywhere, and every FULL-and-OOS passer in that run
sits at gross 1.00 (idea 1761 found the same: "ALL 52 4b passes sit at gross 1.00, 0 of 168 at
gross 0.75").  If the floor is satisfied by EXPOSURE alone then PROTOCOL rule 4b is selecting
books for holding more beta rather than for any device, and every 4b count in the record is a
gross census.

TEST (as the idea specifies).  Hold the DEVICE fixed and sweep GROSS on a dense ladder at every
panel and cadence; regress the 4b FULL and OOS pass indicator on REALISED MEAN GROSS alone and
publish the share of the verdict variance gross explains, plus the gross rung at which each
panel's floor first clears.  Two device arms are carried so that "device" is a label the
regression can be asked about at MATCHED realised gross: BAND (the live RULES v2 clause-2 device,
c = 0.03, gated weight to CASH) and NOBAND (the same equal-weight book ungated).  Constructive
half: should 4b's CAGR floor be stated PER UNIT OF REALISED GROSS?

TUNED PARAMETERS (max 2, PROTOCOL rule 4): GROSS LADDER and PANEL AXIS.  DEVICE, CADENCE and
COST are reported grid axes; every point is published to <stem>_grid.csv.

Protocol: 10 bps headline costs, next-day execution (engine convention), both KEEP paths at
every grid point, rule-8 walk-forward with dials chosen on 2009-2016 ONLY and 2017-2026 read
ONCE.  Offline, deterministic (no randomness is used; the grid is exhaustive).

SURVIVORSHIP: U56 / B136 are CURRENT constituents; SMALL is a CURRENT sub-$2B screen with the
house filter (data/small_meta.csv max_1d_move >= 1.0 dropped).  The headline is a WITHIN-PANEL
statement about which leg binds and is first-order immune; the 4a/4b pass COUNTS are not.
"""
import sys, itertools
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state          # noqa: E402
from engine import backtest as engine_backtest, rebalance_mask           # noqa: E402

BAND      = 0.03
WARMUP    = 260
IS_END    = "2016-12-31"
OOS_START = "2017-01-01"
COSTS     = [0, 10, 25, 50]
HEAD_COST = 10
GROSSES   = [round(0.05 * k, 2) for k in range(1, 21)]      # tuned parameter 1: 0.05 .. 1.00
CADENCES  = ["D", "W", "M", "Q"]
DEVICES   = ["BAND", "NOBAND"]
OUT = Path(__file__).with_suffix(".txt")
_log = []
def log(*a):
    s = " ".join(str(x) for x in a); print(s); _log.append(s)

# ------------------------------------------------------------------ panels (tuned parameter 2)
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    return px[[c for c in px.columns if c not in bad]]

def panels():
    return {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL": small_panel()}

# ------------------------------------------------------------------ vectorised engine replay
def bt_np(px, w, freq):
    """numpy replay of engine.backtest at cost 0 -> (returns, turnover, gross). Gated at G1."""
    R = np.nan_to_num(px.pct_change().values, nan=0.0)
    W = np.nan_to_num(w.reindex(px.index).values, nan=0.0)
    W = np.vstack([np.zeros((1, W.shape[1])), W[:-1]])                 # decided t, applied t+1
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n = len(R); cur = np.zeros(R.shape[1]); held = np.empty_like(R); turn = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = W[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        growth = cur * (1.0 + R[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    return (pd.Series((held * R).sum(axis=1), index=px.index),
            pd.Series(turn, index=px.index), pd.Series(held.sum(axis=1), index=px.index))

def net(r0, turn, c):   return r0 - turn * c / 1e4

def mets(r):
    eq = (1 + r).cumprod(); yrs = len(r) / 252
    cagr = eq.iloc[-1] ** (1 / yrs) - 1
    vol = r.std() * np.sqrt(252)
    return dict(CAGR=cagr, Sharpe=(r.mean() * 252) / vol if vol else np.nan,
                MaxDD=float((eq / eq.cummax() - 1).min()), Vol=vol)

def halves(r):
    h = len(r) // 2
    return mets(r.iloc[:h])["Sharpe"], mets(r.iloc[h:])["Sharpe"]

# ------------------------------------------------------------------ books
def eq_weights(px, cols, gross):
    e = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    e[cols] = px[cols].notna().astype(float)
    return gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)

def r2(y, X):
    """R^2 of an OLS linear-probability model with intercept. X = (n, k) or None."""
    y = np.asarray(y, float)
    if y.std() == 0: return np.nan
    A = np.ones((len(y), 1)) if X is None else np.column_stack([np.ones(len(y)), np.asarray(X, float)])
    beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    resid = y - A @ beta
    return 1.0 - resid.var() / y.var()

def dummies(series):
    lv = sorted(set(series))[1:]
    return np.column_stack([(np.asarray(series) == v).astype(float) for v in lv]) if lv else None

def stack(*parts):
    ps = [np.asarray(x, float) for x in parts if x is not None]
    return np.column_stack(ps) if ps else None

def main():
    PX = panels()
    log("# Idea 1757 (lane C) — is the 4b CAGR FLOOR just a GROSS BAR in disguise?")
    log(f"# band c={BAND} | warm-up {WARMUP} rows | IS <= {IS_END} | OOS >= {OOS_START} "
        f"| gross ladder {GROSSES[0]}..{GROSSES[-1]} step 0.05 ({len(GROSSES)} rungs)")
    for k, v in PX.items():
        log(f"# panel {k}: {v.shape[1]} columns, {v.index[0].date()} -> {v.index[-1].date()}")

    # ---- G1 / G2 / G3 gates -----------------------------------------------------------
    g1 = g2 = g3 = 0.0
    for name in ("U56", "B136"):
        px = PX[name]; st = px.index[WARMUP]
        w = rules_v2_weights(px, BAND, 0.75)
        a0, at, _ = bt_np(px, w, "W")
        b = engine_backtest(px, w, cost_bps=0.0, freq="W")["returns"]
        g1 = max(g1, float(np.abs(a0.loc[st:].values - b.loc[st:].values).max()))
        # G2: the BAND arm at nominal g over ALL columns IS baseline.rules_v2_weights
        mine = eq_weights(px, list(px.columns), 0.75).where(band_state(px, BAND), 0.0)
        g2 = max(g2, float(np.abs(mine.fillna(0).values - w.fillna(0).values).max()))
        # G3: exact cost reconstruction r(c) = r_gross - turnover*c/1e4
        b25 = engine_backtest(px, w, cost_bps=25.0, freq="W")["returns"]
        g3 = max(g3, float(np.abs(net(a0, at, 25).loc[st:].values - b25.loc[st:].values).max()))
    log(f"G1  bt_np vs engine.backtest            max|d| = {g1:.3e}  -> {'PASS' if g1 < 1e-12 else 'FAIL'}")
    log(f"G2  BAND arm == baseline.rules_v2_weights max|d| = {g2:.3e}  -> {'PASS' if g2 == 0.0 else 'FAIL'}")
    log(f"G3  exact cost reconstruction @25 bps    max|d| = {g3:.3e}  -> {'PASS' if g3 < 1e-12 else 'FAIL'}")

    # ---- baselines (live RULES v2 and SPY) --------------------------------------------
    base = {}
    for name, px in PX.items():
        st = px.index[WARMUP]
        r0, t0, _ = bt_np(px, rules_v2_weights(px, BAND, 0.75), "W")
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        b = dict(px=px, start=st, r0=r0.loc[st:], t0=t0.loc[st:], spy=spy)
        for c in COSTS:
            rc = net(b["r0"], b["t0"], c)
            b[f"live{c}"] = mets(rc); b[f"liveH{c}"] = halves(rc)
            b[f"live{c}_oos"] = mets(rc.loc[OOS_START:])
        b["spym"] = mets(spy); b["spyH"] = halves(spy); b["spym_oos"] = mets(spy.loc[OOS_START:])
        base[name] = b
        log(f"# {name}: RULES v2 live 10bps {b['live10']['CAGR']:.2%}/{b['live10']['Sharpe']:.4f}/"
            f"{b['live10']['MaxDD']:.2%} (OOS {b['live10_oos']['CAGR']:.2%}/{b['live10_oos']['Sharpe']:.4f}/"
            f"{b['live10_oos']['MaxDD']:.2%}) | SPY {b['spym']['CAGR']:.2%}/{b['spym']['Sharpe']:.4f}/"
            f"{b['spym']['MaxDD']:.2%} (OOS {b['spym_oos']['CAGR']:.2%}/{b['spym_oos']['Sharpe']:.4f}/"
            f"{b['spym_oos']['MaxDD']:.2%}) | 4b floors: CAGR {0.70*b['spym']['CAGR']:.2%} "
            f"/ OOS {0.70*b['spym_oos']['CAGR']:.2%}, DD cap {0.60*b['spym']['MaxDD']:.2%} "
            f"/ OOS {0.60*b['spym_oos']['MaxDD']:.2%}")

    # ---- the grid ---------------------------------------------------------------------
    rows = []
    for pname, px in PX.items():
        cols = [c for c in px.columns if not (pname == "SMALL" and c == "SPY")]
        bs = band_state(px, BAND).reindex(columns=px.columns).fillna(False)
        unit = {"NOBAND": eq_weights(px, cols, 1.0)}
        unit["BAND"] = unit["NOBAND"].where(bs, 0.0)
        st = base[pname]["start"]; B = base[pname]
        for dev, freq, gross in itertools.product(DEVICES, CADENCES, GROSSES):
            r0, tt, gs = bt_np(px, unit[dev] * gross, freq)
            r0, tt, gs = r0.loc[st:], tt.loc[st:], gs.loc[st:]
            gr = float(gs.mean()); gr_is = float(gs.loc[:IS_END].mean()); gr_oos = float(gs.loc[OOS_START:].mean())
            for c in COSTS:
                r = net(r0, tt, c)
                m, mo, mi = mets(r), mets(r.loc[OOS_START:]), mets(r.loc[:IS_END])
                h1, h2 = halves(r)
                S, So = B["spym"], B["spym_oos"]
                L, LH, Lo = B[f"live{c}"], B[f"liveH{c}"], B[f"live{c}_oos"]
                f_h1 = h1 > B["spyH"][0]
                f_h2 = h2 > B["spyH"][1]
                f_dd = m["MaxDD"] >= 0.60 * S["MaxDD"]
                f_cg = m["CAGR"] >= 0.70 * S["CAGR"]
                o_sh = mo["Sharpe"] > So["Sharpe"]
                o_dd = mo["MaxDD"] >= 0.60 * So["MaxDD"]
                o_cg = mo["CAGR"] >= 0.70 * So["CAGR"]
                # constructive restatement: the floor PER UNIT OF REALISED GROSS
                pu_cg = (m["CAGR"] / gr) >= 0.70 * S["CAGR"] if gr > 0 else False
                pu_ocg = (mo["CAGR"] / gr_oos) >= 0.70 * So["CAGR"] if gr_oos > 0 else False
                rows.append(dict(
                    panel=pname, device=dev, freq=freq, gross=gross, cost=c,
                    gross_real=gr, gross_real_is=gr_is, gross_real_oos=gr_oos,
                    turn_yr=float(tt.sum() / (len(tt) / 252)),
                    CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                    is_CAGR=mi["CAGR"], is_Sharpe=mi["Sharpe"], is_MaxDD=mi["MaxDD"],
                    oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                    f_H1=f_h1, f_H2=f_h2, f_DD=f_dd, f_CAGR=f_cg,
                    o_SH=o_sh, o_DD=o_dd, o_CAGR=o_cg,
                    keep4a=(h1 > LH[0] and h2 > LH[1] and m["MaxDD"] >= L["MaxDD"]),
                    keep4a_oos=(mo["Sharpe"] > Lo["Sharpe"] and mo["MaxDD"] >= Lo["MaxDD"]),
                    keep4b_full=(f_h1 and f_h2 and f_dd and f_cg),
                    keep4b_oos=(o_sh and o_dd and o_cg),
                    pu_CAGR=pu_cg, pu_oos_CAGR=pu_ocg,
                    keep4b_full_pu=(f_h1 and f_h2 and f_dd and pu_cg),
                    keep4b_oos_pu=(o_sh and o_dd and pu_ocg)))
        log(f"# grid done: {pname} ({len(rows)} rows so far)")

    df = pd.DataFrame(rows)
    df.to_csv(Path(__file__).with_name(Path(__file__).stem + "_grid.csv"), index=False)
    log(f"G4  grid rows = {len(df)}  (3 panels x 2 devices x {len(CADENCES)} cadences x "
        f"{len(GROSSES)} gross x {len(COSTS)} cost)  -> "
        f"{'PASS' if len(df) == 3*2*len(CADENCES)*len(GROSSES)*len(COSTS) else 'FAIL'}")
    nb = df[df.device == "NOBAND"]
    g5 = float((nb.gross_real - nb.gross).abs().max())
    log(f"G5  NOBAND realised gross vs nominal     max|d| = {g5:.3e} (drift only, diagnostic)")

    d10 = df[df.cost == HEAD_COST].copy()

    # ---- G6 / G7: replication of the record's committed anchors ------------------------
    anc = d10[(d10.panel == "U56") & (d10.device == "BAND") & (d10.freq == "W") & (d10.gross == 1.00)].iloc[0]
    liv = d10[(d10.panel == "U56") & (d10.device == "BAND") & (d10.freq == "W") & (d10.gross == 0.75)].iloc[0]
    L10 = base["U56"]["live10"]
    g6 = max(abs(anc.CAGR - 0.1153), abs(anc.Sharpe - 1.2008), abs(anc.MaxDD + 0.1591),
             abs(anc.oos_CAGR - 0.1267), abs(anc.oos_Sharpe - 1.2759))
    g7 = max(abs(liv.CAGR - L10["CAGR"]), abs(liv.Sharpe - L10["Sharpe"]), abs(liv.MaxDD - L10["MaxDD"]))
    log(f"G6  replication of 1694/1741's U56 BAND W g=1.00 anchor: FULL {anc.CAGR:.2%}/{anc.Sharpe:.4f}/"
        f"{anc.MaxDD:.2%}, OOS {anc.oos_CAGR:.2%}/{anc.oos_Sharpe:.4f}/{anc.oos_MaxDD:.2%} "
        f"(published 11.53%/1.2008/-15.91%, OOS 12.67%/1.2759/-15.91%) max|d| = {g6:.3e} -> "
        f"{'PASS' if g6 < 5e-5 else 'FAIL'}")
    log(f"G7  the g=0.75 BAND rung IS the live book: {liv.CAGR:.2%}/{liv.Sharpe:.4f}/{liv.MaxDD:.2%} "
        f"vs RULES v2 {L10['CAGR']:.2%}/{L10['Sharpe']:.4f}/{L10['MaxDD']:.2%}  max|d| = {g7:.3e} -> "
        f"{'PASS' if g7 < 1e-12 else 'FAIL'}")

    # ---- 1. the binding-leg census -----------------------------------------------------
    log("\n## 1. WHICH LEG BINDS (10 bps, %d cells)" % len(d10))
    log(f"  4b FULL failures: H1 {int((~d10.f_H1).sum())} / H2 {int((~d10.f_H2).sum())} / "
        f"DD {int((~d10.f_DD).sum())} / CAGR {int((~d10.f_CAGR).sum())}   "
        f"[1741 published 417 / 606 / 370 / 1049 of 1,188]")
    log(f"  4b OOS  failures: SH {int((~d10.o_SH).sum())} / DD {int((~d10.o_DD).sum())} / "
        f"CAGR {int((~d10.o_CAGR).sum())}")
    only = d10[d10.f_H1 & d10.f_H2 & d10.f_DD]
    log(f"  cells failing ONLY on the CAGR floor (all other FULL legs pass): "
        f"{int((~only.f_CAGR).sum())} of {len(only)}")
    log(f"  4b FULL passes {int(d10.keep4b_full.sum())} | 4b OOS {int(d10.keep4b_oos.sum())} | "
        f"BOTH {int((d10.keep4b_full & d10.keep4b_oos).sum())} | "
        f"4a FULL {int(d10.keep4a.sum())} | 4a OOS {int(d10.keep4a_oos.sum())}")
    for pn, g in d10.groupby("panel"):
        log(f"    {pn:6s} 4b FULL {int(g.keep4b_full.sum()):3d}/{len(g)}  "
            f"4b OOS {int(g.keep4b_oos.sum()):3d}  BOTH {int((g.keep4b_full & g.keep4b_oos).sum()):3d}  "
            f"4a FULL {int(g.keep4a.sum()):3d}  | CAGR-floor failures {int((~g.f_CAGR).sum()):3d}")

    # ---- 2. the headline regression ----------------------------------------------------
    log("\n## 2. DOES REALISED GROSS ALONE EXPLAIN THE 4b VERDICT? (LPM R^2, 10 bps)")
    for tgt in ("keep4b_full", "keep4b_oos", "f_CAGR", "o_CAGR", "f_DD", "f_H1", "f_H2"):
        y = d10[tgt].astype(float).values
        gcol = d10.gross_real.values.reshape(-1, 1)
        r_g = r2(y, gcol)
        r_gd = r2(y, stack(gcol, dummies(d10.device)))
        r_all = r2(y, stack(gcol, dummies(d10.device), dummies(d10.panel), dummies(d10.freq)))
        log(f"  {tgt:12s} base rate {y.mean():.3f} | gross alone R2 {r_g:+.4f} | "
            f"+device {r_gd:+.4f} | +panel+cadence {r_all:+.4f}")
    log("  within panel (gross alone):")
    for pn, g in d10.groupby("panel"):
        log(f"    {pn:6s} 4b FULL R2 {r2(g.keep4b_full.astype(float), g.gross_real.values.reshape(-1,1)):+.4f}"
            f" | 4b OOS {r2(g.keep4b_oos.astype(float), g.gross_real.values.reshape(-1,1)):+.4f}"
            f" | CAGR leg {r2(g.f_CAGR.astype(float), g.gross_real.values.reshape(-1,1)):+.4f}")

    # ---- 2b. CAGR as a straight line in realised gross --------------------------------
    log("\n## 2b. IS CAGR A STRAIGHT LINE IN REALISED GROSS? (10 bps; the floor as a gross bar)")
    for lbl, g in [("POOLED", d10)] + [(f"{pn}/{dv}", gg) for (pn, dv), gg in d10.groupby(["panel", "device"])]:
        x = g.gross_real.values; y = g.CAGR.values
        A = np.column_stack([np.ones(len(x)), x]); b0, b1 = np.linalg.lstsq(A, y, rcond=None)[0]
        rr = 1 - (y - A @ np.array([b0, b1])).var() / y.var()
        pn = g.panel.iloc[0]; fl = 0.70 * base[pn]["spym"]["CAGR"]
        cross = (fl - b0) / b1 if b1 else np.nan
        log(f"  {lbl:12s} CAGR = {b0:+.4f} {b1:+.4f}*gross   R2 {rr:+.4f}   "
            f"floor {fl:.2%} crossed at realised gross {cross:.3f}")

    # ---- 3. at MATCHED realised gross, does the device label still move the verdict? ----
    log("\n## 3. AT MATCHED REALISED GROSS — does the DEVICE label move the verdict?")
    d10 = d10.assign(gbin=(d10.gross_real / 0.025).round().astype(int))
    tab = []
    for (pn, gb), g in d10.groupby(["panel", "gbin"]):
        if g.device.nunique() < 2: continue
        a, b = g[g.device == "BAND"], g[g.device == "NOBAND"]
        tab.append(dict(panel=pn, gbin=gb * 0.025, nB=len(a), nN=len(b),
                        pB=a.keep4b_full.mean(), pN=b.keep4b_full.mean(),
                        cB=a.f_CAGR.mean(), cN=b.f_CAGR.mean(),
                        dB=a.f_DD.mean(), dN=b.f_DD.mean()))
    T = pd.DataFrame(tab)
    if len(T):
        log(f"  {len(T)} overlapping (panel, 0.025-gross-bin) cells carry BOTH devices")
        log(f"  mean 4b FULL pass rate  BAND {T.pB.mean():.3f}  vs  NOBAND {T.pN.mean():.3f}  "
            f"(bins where they differ: {int((T.pB != T.pN).sum())} of {len(T)})")
        log(f"  mean CAGR-leg pass rate BAND {T.cB.mean():.3f}  vs  NOBAND {T.cN.mean():.3f}  "
            f"(differ in {int((T.cB != T.cN).sum())} bins)")
        log(f"  mean DD-cap  pass rate  BAND {T.dB.mean():.3f}  vs  NOBAND {T.dN.mean():.3f}  "
            f"(differ in {int((T.dB != T.dN).sum())} bins)")
        T.to_csv(Path(__file__).with_name(Path(__file__).stem + "_matchedgross.csv"), index=False)

    # ---- 4. the rung at which each panel's floor first clears ---------------------------
    log("\n## 4. THE GROSS RUNG AT WHICH THE CAGR FLOOR FIRST CLEARS (10 bps)")
    frows = []
    for (pn, dev, fq), g in d10.groupby(["panel", "device", "freq"]):
        g = g.sort_values("gross")
        okF, okO = g[g.f_CAGR], g[g.o_CAGR]
        frows.append(dict(panel=pn, device=dev, freq=fq,
                          first_full=okF.gross.min() if len(okF) else np.nan,
                          first_full_real=okF.gross_real.min() if len(okF) else np.nan,
                          first_oos=okO.gross.min() if len(okO) else np.nan,
                          first_oos_real=okO.gross_real.min() if len(okO) else np.nan,
                          dd_ok_at_top=bool(g.iloc[-1].f_DD)))
    F = pd.DataFrame(frows)
    F.to_csv(Path(__file__).with_name(Path(__file__).stem + "_firstclear.csv"), index=False)
    for pn, g in F.groupby("panel"):
        for _, r in g.iterrows():
            log(f"  {pn:6s} {r.device:6s} {r.freq:1s}  FULL floor clears at nominal "
                f"{r.first_full if r.first_full==r.first_full else float('nan'):.2f} "
                f"(realised {r.first_full_real:.3f})   OOS at "
                f"{r.first_oos if r.first_oos==r.first_oos else float('nan'):.2f} "
                f"(realised {r.first_oos_real:.3f})")

    # ---- 5. the constructive half ------------------------------------------------------
    log("\n## 5. CONSTRUCTIVE — STATE THE FLOOR PER UNIT OF REALISED GROSS")
    log(f"  4b FULL passes: as written {int(d10.keep4b_full.sum())} -> per-unit "
        f"{int(d10.keep4b_full_pu.sum())};  4b OOS {int(d10.keep4b_oos.sum())} -> "
        f"{int(d10.keep4b_oos_pu.sum())};  BOTH {int((d10.keep4b_full & d10.keep4b_oos).sum())} -> "
        f"{int((d10.keep4b_full_pu & d10.keep4b_oos_pu).sum())}")
    log(f"  CAGR leg failures: as written {int((~d10.f_CAGR).sum())} -> per-unit "
        f"{int((~d10.pu_CAGR).sum())} of {len(d10)}")
    puonly = d10[d10.f_H1 & d10.f_H2 & d10.f_DD]
    log(f"  cells failing ONLY the per-unit floor: {int((~puonly.pu_CAGR).sum())} of {len(puonly)} "
        f"(as written {int((~puonly.f_CAGR).sum())})")
    log(f"  R2 of the PER-UNIT pass indicator on realised gross alone: "
        f"{r2(d10.pu_CAGR.astype(float), d10.gross_real.values.reshape(-1,1)):+.4f} "
        f"(as written {r2(d10.f_CAGR.astype(float), d10.gross_real.values.reshape(-1,1)):+.4f})")
    log(f"  corr(realised gross, CAGR) {np.corrcoef(d10.gross_real, d10.CAGR)[0,1]:+.4f} ; "
        f"corr(realised gross, CAGR/gross) "
        f"{np.corrcoef(d10.gross_real, d10.CAGR/d10.gross_real)[0,1]:+.4f}")

    # ---- 6. RULE 8: dials on 2009-2016 only, 2017-2026 read ONCE -----------------------
    log("\n## 6. RULE 8 — IS-only choosers over (device, cadence, gross), 2017-2026 READ ONCE")
    picks = []
    for pn, g in d10.groupby("panel"):
        B = base[pn]; is_floor = 0.70 * mets(B["spy"].loc[:IS_END])["CAGR"]
        gg = g.copy()
        gg["is_calmar"] = gg.is_CAGR / gg.is_MaxDD.abs()
        gg["is_slack"] = gg.is_CAGR - is_floor
        gg["is_slack_pu"] = gg.is_CAGR / gg.gross_real_is - is_floor
        for cname, col in (("C_SHARPE", "is_Sharpe"), ("C_CALMAR", "is_calmar"),
                           ("C_FLOOR", "is_slack"), ("C_FLOORPU", "is_slack_pu")):
            r = gg.loc[gg[col].idxmax()]
            picks.append(dict(panel=pn, chooser=cname, device=r.device, freq=r.freq, gross=r.gross,
                              gross_real=r.gross_real, is_Sharpe=r.is_Sharpe,
                              oos_CAGR=r.oos_CAGR, oos_Sharpe=r.oos_Sharpe, oos_MaxDD=r.oos_MaxDD,
                              keep4a_oos=bool(r.keep4a_oos), keep4b_oos=bool(r.keep4b_oos),
                              keep4b_oos_pu=bool(r.keep4b_oos_pu),
                              o_SH=bool(r.o_SH), o_DD=bool(r.o_DD), o_CAGR=bool(r.o_CAGR)))
    P = pd.DataFrame(picks)
    P.to_csv(Path(__file__).with_name(Path(__file__).stem + "_picks.csv"), index=False)
    for _, r in P.iterrows():
        B = base[r.panel]
        log(f"  {r.panel:6s} {r.chooser:9s} -> {r.device:6s} {r.freq} g={r.gross:.2f} "
            f"(realised {r.gross_real:.3f}) | OOS {r.oos_CAGR:.2%}/{r.oos_Sharpe:.4f}/{r.oos_MaxDD:.2%} | "
            f"4a OOS {'PASS' if r.keep4a_oos else 'fail'} | 4b OOS {'PASS' if r.keep4b_oos else 'fail'} "
            f"(SH {'y' if r.o_SH else 'n'} DD {'y' if r.o_DD else 'n'} CAGR {'y' if r.o_CAGR else 'n'})"
            f" | per-unit 4b OOS {'PASS' if r.keep4b_oos_pu else 'fail'}"
            f" | live v2 OOS {B['live10_oos']['CAGR']:.2%}/{B['live10_oos']['Sharpe']:.4f}/"
            f"{B['live10_oos']['MaxDD']:.2%}")
    log(f"  picks clearing 4a OOS: {int(P.keep4a_oos.sum())} of {len(P)} ; "
        f"4b OOS: {int(P.keep4b_oos.sum())} of {len(P)} ; "
        f"per-unit 4b OOS: {int(P.keep4b_oos_pu.sum())} of {len(P)}")

    # ---- 7. cost ladder ----------------------------------------------------------------
    log("\n## 7. COST LADDER (exact reconstruction, G3)")
    for c in COSTS:
        g = df[df.cost == c]
        log(f"  {c:2d} bps: 4b FULL {int(g.keep4b_full.sum()):3d} | 4b OOS {int(g.keep4b_oos.sum()):3d} "
            f"| 4a FULL {int(g.keep4a.sum()):3d} | CAGR-leg failures {int((~g.f_CAGR).sum()):4d} of {len(g)}")

    # ---- 8. the gross of every passer --------------------------------------------------
    log("\n## 8. THE GROSS OF EVERY 4b PASSER (10 bps)")
    pf = d10[d10.keep4b_full]
    if len(pf):
        lo, hi = pf.gross_real.min(), pf.gross_real.max()
        win = d10[(d10.gross_real >= lo) & (d10.gross_real <= hi)]
        log(f"  4b FULL passers ({len(pf)}) occupy REALISED gross [{lo:.3f}, {hi:.3f}] "
            f"(width {hi-lo:.3f}) while their NOMINAL gross spans {pf.gross.min():.2f}..{pf.gross.max():.2f}"
            f" ({len(set(pf.gross))} rungs)")
        log(f"  necessity: {len(pf)} of {len(pf)} passers lie in that window "
            f"(1.000) | sufficiency: {len(win[win.keep4b_full])} of {len(win)} cells IN the window pass "
            f"({len(win[win.keep4b_full])/len(win):.3f}); outside it {int(d10.keep4b_full.sum())-len(win[win.keep4b_full])} "
            f"of {len(d10)-len(win)}")
        po = d10[d10.keep4b_oos]
        log(f"  4b OOS passers ({len(po)}) occupy realised gross [{po.gross_real.min():.3f}, "
            f"{po.gross_real.max():.3f}], nominal {po.gross.min():.2f}..{po.gross.max():.2f}")
    pas = d10[d10.keep4b_full | d10.keep4b_oos]
    if len(pas):
        log(f"  {len(pas)} cells pass 4b on at least one slice; realised gross "
            f"min {pas.gross_real.min():.3f} / median {pas.gross_real.median():.3f} / max {pas.gross_real.max():.3f}"
            f" ; nominal gross values {sorted(set(pas.gross))}")
        log(f"  share of 4b FULL passers at nominal gross 1.00: "
            f"{(d10[d10.keep4b_full].gross == 1.00).mean() if d10.keep4b_full.any() else float('nan'):.3f}"
            f"  [1761 published 52 of 52]")
        log("  by device: " + ", ".join(f"{k} {int(v)}" for k, v in pas.groupby('device').size().items()))
    log(f"\n# log -> {OUT.name}")
    OUT.write_text("\n".join(_log) + "\n")

if __name__ == "__main__":
    main()
