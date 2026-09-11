#!/usr/bin/env python3
"""Idea 735 — do the ARM-LEVEL turnover slopes that die OOS die on EVERY residual family?

Idea 538 found two arm-level turnover predictors of the de-grossing TIMING RESIDUAL that
carry a genuine in-sample slope yet score WORSE out of sample than the FAMILY constant they
were meant to replace:

    RESPREAD turnover (TOrs)  IS t -4.11, R2 0.0953  ->  OOS MAE 0.2408  vs FAMILY 0.1937
    de-grossing DELTA (DTO)   IS t +4.38, R2 0.1070  ->  OOS MAE 0.2391  vs FAMILY 0.1937

while c_sd's slope walks forward intact (OOS MAE 0.1771).  The queue asks whether that
IS-significant / OOS-dead pattern is SPECIFIC TO TURNOVER, or whether it is simply what every
non-c_sd predictor in the record does.  If it is the norm, then "turnover dies out of sample"
is not a fact about turnover; it is a fact about fitting 162 cells.

METHOD
  Population: idea 538's EXACT 162 cells / 324 books, rebuilt from source and gated against
  538's committed `.cells.csv` and `.grid.csv`.  A cell is (panel, family, level, cadence) at
  gross 0.75; its two books are the RESPREAD and DEGROSS constructions of the same gate mask.
      gap0  = 100*(CAGR(DEGROSS,0bps) - CAGR(RESPREAD,0bps))   pp/yr
      pred0 = 100*(CAGR(c_bar*RESPREAD) - CAGR(RESPREAD))      constant-leverage drag
      resid0 = gap0 - pred0                                    the TIMING of c_t
      c_t = held gross(DEGROSS) / held gross(RESPREAD)
  Panels U56 / B136 / SMALL439; families QUANTILE (9 levels) and MA-THRESH (9 thetas);
  cadences W/M/Q; 10 bps; next-day execution; the 0-bps rung DERIVED as r0 = r10 + turn*bps/1e4.

  TUNED PARAMETERS (exactly 2, every grid point reported, none selected outside rule 8):
    P1 PREDICTOR FORM, 23 values — 3 constants (ZERO, GLOBAL, FAMILY), the incumbent CSD,
       and 19 NON-c_sd single-term predictors spanning five residual families:
         TURNOVER  TO TORS DTO LOGTO TORATIO           (idea 538's arm)
         EXPOSURE  CBAR ABSCBAR CT_AC1 CT_RANGE GSHARE (the c_t path, other than its sd)
         BOOK      ISSH_DG ISSH_RS DSH                 (the arm's own in-sample quality)
         DECOMP    GAP_IS PRED_IS RESID_IS             (the decomposition's own IS terms)
         DESIGN    LEVEL CADRANK NNAMES                (the cell's coordinates)
    P2 SPLIT, 2 values — IS ends 2016-12-31 (idea 538's) or 2018-12-31.

  Every honest form is fitted on IS-window cell values ONLY (y = resid0_IS, x = x_IS) and
  scored ONCE against the OOS-window truth (resid0_OOS).  The 2x2 the idea asks for:
      IS-LIVE   |t| >= 2 on the IS fit
      OOS-LIVE  OOS MAE <= OOS MAE of the FAMILY constant
  "IS-significant / OOS-dead" is the (IS-LIVE, not OOS-LIVE) cell.

  RULE 8 (required): WF-A picks each arm's (level, cadence) on IS Sharpe alone and reads
  2017+ ONCE against RULES v2 and SPY; WF-C lets each IS-fitted predictor CHOOSE the
  construction per cell and reads OOS Sharpe once against always-RESPREAD, always-DEGROSS
  and the OOS oracle.  Both KEEP paths are evaluated on all 324 books.

SURVIVORSHIP: all three panels are CURRENT constituent lists (idea 54) — no delistings — so
every CAGR LEVEL is inflated and the 4a/4b columns inherit that in full.  The headline object
is an arm-minus-arm contrast on the SAME names, days and gross (both constructions share one
gate mask), so the bias very largely cancels out of gap0/pred0/resid0; it does NOT cancel out
of the KEEP columns.  SMALL439 drops every ticker with max_1d_move >= 1.0 first.

Deterministic, standalone, no network.  Modifies nothing outside its own outputs.
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights        # noqa
from engine import backtest as engine_backtest, metrics, rebalance_mask  # noqa

OUT = Path(__file__).with_suffix("")
COST_BPS, GROSS = 10, 0.75
CADENCES = ["W", "M", "Q"]
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
QUANT_X = [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95]
MA_THETA = [0.30, 0.20, 0.12, 0.06, 0.00, -0.06, -0.12, -0.25, -0.40]
FAMILIES = ["QUANTILE", "MA-THRESH"]
SPLITS = {"S2016": ("2016-12-31", "2017-01-01"), "S2018": ("2018-12-31", "2019-01-01")}
REF538 = REPO / "research" / "backtests" / "2026-09-11_is-c_sd-the-right-SCALE-or-is-it-a-TURNOVER-proxy_B"
REF_MAE_CSD, REF_MAE_FAM = 0.177128, 0.193564          # idea 535's committed ladder numbers

GROUPS = {
    "CONSTANT": ["ZERO", "GLOBAL", "FAMILY"],
    "INCUMBENT": ["CSD"],
    "TURNOVER": ["TO", "TORS", "DTO", "LOGTO", "TORATIO"],
    "EXPOSURE": ["CBAR", "ABSCBAR", "CT_AC1", "CT_RANGE", "GSHARE"],
    "BOOK": ["ISSH_DG", "ISSH_RS", "DSH"],
    "DECOMP": ["GAP_IS", "PRED_IS", "RESID_IS"],
    "DESIGN": ["LEVEL", "CADRANK", "NNAMES"],
}
FORMS = [f for g in GROUPS.values() for f in g]
GROUP_OF = {f: g for g, fs in GROUPS.items() for f in fs}
LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)

# ------------------------------------------------------------------ machinery
def fast_backtest(prices, weights, cost_bps=COST_BPS, freq="W"):
    """numpy re-implementation of engine.backtest; returns (returns, turnover, held gross)."""
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(prices.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(prices.index, freq).shift(1, fill_value=False).values
    n = len(prices.index)
    cur = np.zeros(prices.shape[1]); grs = np.empty(n); turn = np.zeros(n); pr = np.empty(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        grs[i] = cur.sum(); pr[i] = float(cur @ rets[i])
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    idx = prices.index
    return (pd.Series(pr - turn * cost_bps / 1e4, index=idx),
            pd.Series(turn, index=idx), pd.Series(grs, index=idx))

def cagr(r):
    eq = (1 + r).cumprod(); return eq.iloc[-1] ** (252 / len(r)) - 1

def stat(r, is_end, oos_start):
    h = len(r) // 2
    m, mi, mo = metrics(r), metrics(r.loc[:is_end]), metrics(r.loc[oos_start:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])

def live_mask(px): return px.notna() & px.shift(1).notna()

def gate_mask(px, family, level):
    live = live_mask(px); ma = px.rolling(200).mean()
    if family == "MA-THRESH":
        return (px > ma * (1 + level)) & live
    dist = (px / ma - 1).where(live)
    kt = np.ceil(level * live.sum(axis=1)).astype(int).clip(lower=1)
    return dist.rank(axis=1, ascending=False, method="first").le(kt, axis=0).fillna(False) & live

def unit_book(px, g, construction):
    if construction == "RESPREAD":
        return g.astype(float).div(g.sum(axis=1).clip(lower=1), axis=0)
    return g.astype(float).div(live_mask(px).sum(axis=1).clip(lower=1), axis=0)

def ols(X, y):
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ b; n, k = X.shape
    s2 = r @ r / max(n - k, 1)
    se = np.sqrt(np.diag(s2 * np.linalg.pinv(X.T @ X)))
    tss = ((y - y.mean()) ** 2).sum()
    return b, se, np.where(se > 0, b / se, np.nan), 1 - (r @ r) / tss if tss > 0 else np.nan

def panels():
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv = [c for c in pxs.columns if c != "SPY" and c not in bad]
    px56, px136 = load_universe(), load_universe(broad=True)
    P(f"panels: SMALL439 {len(inv)} names ({len(bad)} dropped for max_1d_move >= 1.0), "
      f"U56 {px56.shape[1]-1}, B136 {px136.shape[1]-1}")
    return {"SMALL439": (pxs[inv], pxs["SPY"]),
            "U56": (px56[[c for c in px56.columns if c != "SPY"]], px56["SPY"]),
            "B136": (px136[[c for c in px136.columns if c != "SPY"]], px136["SPY"])}

# ================================================================== BUILD
t0 = time.time()
P("=" * 100)
P("IDEA 735 — do the arm-level turnover slopes that die OOS die on EVERY residual family?")
P(f"10 bps, next-day execution, gross {GROSS}; 0-bps rung DERIVED (r0 = r10 + turn*bps/1e4).")
P(f"{len(FORMS)} predictor forms x {len(SPLITS)} splits; population = idea 538's 162 cells / 324 books.")
P("=" * 100)

rows, cells, wfa = [], [], []
PX = panels()
ie0, os0 = SPLITS["S2016"]
# Idea 538 computes the 4a comparand ONCE on the U56 panel (`px_u = load_universe()`, its
# line 376) and reindexes that one series onto all three panels.  PROTOCOL rule 3 and
# baseline.compare() instead run RULES v2 on the IDEA'S OWN panel.  Both readings are
# carried here and both are published; neither is silently adopted.
_pu = load_universe()
_r538, _, _ = fast_backtest(_pu, rules_v2_weights(_pu), COST_BPS, "W")
LIVE538 = _r538
for pname, (px, spy_px) in PX.items():
    start = px.index[260]
    live_full, _, _ = fast_backtest(px.join(spy_px.rename("SPY")),
                                    rules_v2_weights(px.join(spy_px.rename("SPY"))), COST_BPS, "W")
    spy_r = spy_px.pct_change().fillna(0.0).loc[start:]
    spy_s = stat(spy_r, ie0, os0); live_s = stat(live_full.loc[start:], ie0, os0)
    live538_s = stat(LIVE538.reindex(px.index).fillna(0.0).loc[start:], ie0, os0)
    if pname != "U56":
        P(f"  4a COMPARAND SPLIT on {pname}: same-panel RULES v2 Sharpe {live_s['Sharpe']:.4f} / "
          f"MaxDD {live_s['MaxDD']:.4f}  vs idea 538's U56-reindexed comparand Sharpe "
          f"{live538_s['Sharpe']:.4f} / MaxDD {live538_s['MaxDD']:.4f}")
    P(f"\nPANEL {pname}  eval from {start.date()}  SPY CAGR {spy_s['CAGR']:.4f} Sharpe "
      f"{spy_s['Sharpe']:.4f} MaxDD {spy_s['MaxDD']:.4f} | OOS {spy_s['oCAGR']:.4f}/"
      f"{spy_s['oSharpe']:.4f}/{spy_s['oMaxDD']:.4f}")
    P(f"  RULES v2 (live) CAGR {live_s['CAGR']:.4f} Sharpe {live_s['Sharpe']:.4f} MaxDD "
      f"{live_s['MaxDD']:.4f} | OOS {live_s['oCAGR']:.4f}/{live_s['oSharpe']:.4f}/{live_s['oMaxDD']:.4f}")
    for family in FAMILIES:
        for li, level in enumerate(QUANT_X if family == "QUANTILE" else MA_THETA):
            gm = gate_mask(px, family, level)
            gshare_full = (gm.sum(axis=1) / live_mask(px).sum(axis=1).clip(lower=1)).loc[start:]
            ub = {c: unit_book(px, gm, c) for c in CONSTRUCTIONS}
            for cad in CADENCES:
                got = {}
                for con in CONSTRUCTIONS:
                    r10, turn, grs = fast_backtest(px, ub[con] * GROSS, COST_BPS, cad)
                    r10, turn, grs = r10.loc[start:], turn.loc[start:], grs.loc[start:]
                    got[con] = dict(r0=r10 + turn * COST_BPS / 1e4, turn=turn, gross=grs, r10=r10)
                    s = stat(r10, ie0, os0)
                    rows.append(dict(panel=pname, family=family, level=level, cad=cad, con=con,
                                     **s, turn_yr=turn.sum() / (len(turn) / 252),
                                     p4a=bool(s["H1"] > live_s["H1"] and s["H2"] > live_s["H2"]
                                              and s["MaxDD"] >= live_s["MaxDD"]),
                                     p4a_538conv=bool(s["H1"] > live538_s["H1"]
                                                      and s["H2"] > live538_s["H2"]
                                                      and s["MaxDD"] >= live538_s["MaxDD"]),
                                     p4b=bool(s["H1"] > spy_s["H1"] and s["H2"] > spy_s["H2"]
                                              and s["oSharpe"] > spy_s["oSharpe"]
                                              and abs(s["MaxDD"]) <= 0.60 * abs(spy_s["MaxDD"])
                                              and s["CAGR"] >= 0.70 * spy_s["CAGR"])))
                dg, rs = got["DEGROSS"], got["RESPREAD"]
                c_t = (dg["gross"] / rs["gross"].replace(0, np.nan)).fillna(0.0)
                for sp, (ie, os_) in SPLITS.items():
                    rec = dict(panel=pname, family=family, level=level, cad=cad, split=sp,
                               li=li, cadrank=CADENCES.index(cad) + 1, nnames=px.shape[1])
                    for tag, sl in (("is", slice(None, ie)), ("oos", slice(os_, None))):
                        rr, rd, ct = rs["r0"].loc[sl], dg["r0"].loc[sl], c_t.loc[sl]
                        cb = float(ct.mean())
                        g0 = 100 * (cagr(rd) - cagr(rr)); p0 = 100 * (cagr(cb * rr) - cagr(rr))
                        yrs = len(rr) / 252
                        rec[f"resid_{tag}"] = g0 - p0; rec[f"gap_{tag}"] = g0
                        rec[f"pred_{tag}"] = p0; rec[f"c_bar_{tag}"] = cb
                        rec[f"c_sd_{tag}"] = float(ct.std())
                        rec[f"ct_ac1_{tag}"] = float(ct.autocorr(1)) if ct.std() > 0 else 0.0
                        rec[f"ct_range_{tag}"] = float(ct.max() - ct.min())
                        rec[f"to_{tag}"] = dg["turn"].loc[sl].sum() / yrs
                        rec[f"tors_{tag}"] = rs["turn"].loc[sl].sum() / yrs
                        rec[f"gshare_{tag}"] = float(gshare_full.loc[sl].mean())
                        rec[f"isSharpe_dg_{tag}"] = metrics(dg["r10"].loc[sl])["Sharpe"]
                        rec[f"isSharpe_rs_{tag}"] = metrics(rs["r10"].loc[sl])["Sharpe"]
                    rec["oSharpe_dg"] = metrics(dg["r10"].loc[SPLITS[sp][1]:])["Sharpe"]
                    rec["oSharpe_rs"] = metrics(rs["r10"].loc[SPLITS[sp][1]:])["Sharpe"]
                    cells.append(rec)
    P(f"  ... {pname} done ({time.time()-t0:.0f}s)")

G = pd.DataFrame(rows); C0 = pd.DataFrame(cells)
C0["dto_is"] = C0.to_is - C0.tors_is; C0["dto_oos"] = C0.to_oos - C0.tors_oos
G.to_csv(f"{OUT}.grid.csv", index=False); C0.to_csv(f"{OUT}.cells.csv", index=False)

# ================================================================== G1 REPRODUCTION GATE
P("\n" + "=" * 100); P("G1 REPRODUCTION GATE vs idea 538's committed tables (printed before any new fit)")
ref = pd.read_csv(f"{REF538}.cells.csv")
key = ["panel", "family", "level", "cad"]
mine = C0[C0.split == "S2016"].set_index(key).sort_index()
ref = ref.set_index(key).sort_index()
assert list(mine.index) == list(ref.index), "cell alignment vs idea 538"
gate = {}
for col, mycol in [("c_sd_is", "c_sd_is"), ("c_bar_is", "c_bar_is"), ("resid_is", "resid_is"),
                   ("resid_oos", "resid_oos"), ("to_is", "to_is"), ("tors_is", "tors_is"),
                   ("isSharpe_dg", "isSharpe_dg_is"), ("oSharpe_dg", "oSharpe_dg")]:
    d = float(np.abs(mine[mycol].values - ref[col].values).max()); gate[col] = d
    P(f"  max |d {col:12s}| = {d:.3e}")
P(f"  n cells {len(mine)} (538: {len(ref)});  n books {len(G)}")
assert gate["c_sd_is"] < 1e-6 and gate["resid_is"] < 1e-2 and gate["resid_oos"] < 1e-2, "G1 fail"
refg = pd.read_csv(f"{REF538}.grid.csv")
gk = ["panel", "family", "level", "cad", "con"]
mg = G.set_index(gk).sort_index(); rg = refg.set_index(gk).sort_index()
assert list(mg.index) == list(rg.index), "book alignment vs idea 538"
for col in ["CAGR", "Sharpe", "MaxDD", "oSharpe", "turn_yr"]:
    P(f"  max |d {col:12s}| = {float(np.abs(mg[col].values - rg[col].values).max()):.3e}  (book level)")
n538 = int((mg.p4a_538conv.values == rg.p4a.values).sum())
P(f"  4a column under IDEA 538'S OWN convention: agrees on {n538}/{len(mg)} books "
  f"(mine {int(mg.p4a_538conv.sum())} vs 538 {int(rg.p4a.sum())})")
P(f"  4b column: agrees on {int((mg.p4b.values == rg.p4b.values).sum())}/{len(mg)} books "
  f"(mine {int(mg.p4b.sum())} vs 538 {int(rg.p4b.sum())})")
assert n538 == len(mg) and (mg.p4b.values == rg.p4b.values).all(), "G1 KEEP-column reproduction"
P("  G1 PASS (resid bars at idea 301's stated 1e-2 pp allowance for the prices.csv daily vintage)")
P(f"  *** CONVENTION SPLIT, REPORTED NOT RESOLVED: under the SAME-PANEL comparand that "
  f"PROTOCOL rule 3 / baseline.compare() use, 4a is {int(G.p4a.sum())}/{len(G)}; under idea "
  f"538's U56-reindexed comparand it is {int(G.p4a_538conv.sum())}/{len(G)}. ***")

# ================================================================== predictor ladder
def xcol(form, d):
    m = {"CSD": d.c_sd_is, "TO": d.to_is, "TORS": d.tors_is, "DTO": d.dto_is,
         "LOGTO": np.log(d.to_is.clip(lower=1e-6)), "TORATIO": d.to_is / d.tors_is.clip(lower=1e-9),
         "CBAR": d.c_bar_is, "ABSCBAR": (1 - d.c_bar_is).abs(), "CT_AC1": d.ct_ac1_is,
         "CT_RANGE": d.ct_range_is, "GSHARE": d.gshare_is,
         "ISSH_DG": d.isSharpe_dg_is, "ISSH_RS": d.isSharpe_rs_is,
         "DSH": d.isSharpe_dg_is - d.isSharpe_rs_is,
         "GAP_IS": d.gap_is, "PRED_IS": d.pred_is, "RESID_IS": d.resid_is,
         "LEVEL": d.li.astype(float), "CADRANK": d.cadrank.astype(float),
         "NNAMES": np.log(d.nnames.astype(float))}
    return m[form].values.astype(float)

lad, fits = [], []
for sp in SPLITS:
    d = C0[C0.split == sp].reset_index(drop=True)
    y_is, y_oos = d.resid_is.values, d.resid_oos.values
    famdum = (d.family == "MA-THRESH").values.astype(float)
    base = {}
    base["ZERO"] = np.zeros(len(d))
    base["GLOBAL"] = np.full(len(d), y_is.mean())
    fm = {f: y_is[famdum == v].mean() for f, v in (("MA-THRESH", 1.0), ("QUANTILE", 0.0))}
    base["FAMILY"] = np.where(famdum == 1.0, fm["MA-THRESH"], fm["QUANTILE"])
    for form in FORMS:
        if form in base:
            pred, t, r2, coef = base[form], np.nan, np.nan, np.nan
        else:
            x = xcol(form, d); X = np.column_stack([np.ones(len(d)), x])
            b, se, ts, r2 = ols(X, y_is)
            pred = X @ b; t, coef = ts[1], b[1]
        mae = float(np.abs(pred - y_oos).mean())
        mae_is = float(np.abs(pred - y_is).mean())
        lad.append(dict(split=sp, group=GROUP_OF[form], form=form, n=len(d), coef=coef,
                        tstat=t, IS_R2=r2, IS_MAE=mae_is, OOS_MAE=mae))
        fits.append(dict(split=sp, form=form, pred=pred))
L = pd.DataFrame(lad)
for sp in SPLITS:
    fam = float(L[(L.split == sp) & (L.form == "FAMILY")].OOS_MAE.iloc[0])
    L.loc[L.split == sp, "FAMILY_OOS_MAE"] = fam
L["ratio_vs_FAMILY"] = L.OOS_MAE / L.FAMILY_OOS_MAE
L["IS_LIVE"] = L.tstat.abs() >= 2.0
L["OOS_LIVE"] = L.OOS_MAE <= L.FAMILY_OOS_MAE
L["cellclass"] = np.where(L.form.isin(GROUPS["CONSTANT"]), "constant",
                 np.where(L.IS_LIVE & L.OOS_LIVE, "IS-live / OOS-live",
                 np.where(L.IS_LIVE & ~L.OOS_LIVE, "IS-SIGNIFICANT / OOS-DEAD",
                 np.where(~L.IS_LIVE & L.OOS_LIVE, "IS-dead / OOS-live", "dead / dead"))))
L.to_csv(f"{OUT}.ladder.csv", index=False)

P("\n" + "=" * 100); P("ALL GRID POINTS — predictor ladder (IS-only fits, scored once on OOS truth)")
P("=" * 100)
for sp in SPLITS:
    s = L[L.split == sp]
    P(f"\n--- split {sp} (IS <= {SPLITS[sp][0]}, OOS >= {SPLITS[sp][1]}), n = {int(s.n.iloc[0])} cells ---")
    P(s[["group", "form", "coef", "tstat", "IS_R2", "IS_MAE", "OOS_MAE", "ratio_vs_FAMILY",
         "IS_LIVE", "OOS_LIVE", "cellclass"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

P("\n" + "=" * 100); P("THE 2x2 — is 'IS-significant / OOS-dead' specific to TURNOVER?")
P("=" * 100)
nc = L[~L.form.isin(GROUPS["CONSTANT"])]
for sp in SPLITS:
    s = nc[nc.split == sp]
    ct = pd.crosstab(s.IS_LIVE, s.OOS_LIVE)
    P(f"\nsplit {sp}: {len(s)} non-constant forms")
    P(ct.to_string())
    isd = s[s.IS_LIVE & ~s.OOS_LIVE]
    P(f"  IS-significant (|t|>=2): {int(s.IS_LIVE.sum())}/{len(s)}   "
      f"of those, OOS-DEAD: {len(isd)}/{int(s.IS_LIVE.sum())}"
      + (f" ({len(isd)/max(int(s.IS_LIVE.sum()),1):.0%})"))
    P(f"  IS-significant AND OOS-live: {int((s.IS_LIVE & s.OOS_LIVE).sum())} -> "
      f"{sorted(s[s.IS_LIVE & s.OOS_LIVE].form)}")
    P(f"  OOS-live at all (any t): {int(s.OOS_LIVE.sum())} -> {sorted(s[s.OOS_LIVE].form)}")
P("\nBY GROUP (both splits pooled) — share of forms that are IS-significant, and of those, OOS-dead:")
gb = nc.groupby("group").agg(forms=("form", "count"), IS_live=("IS_LIVE", "sum"),
                             OOS_live=("OOS_LIVE", "sum"),
                             ISlive_OOSdead=("cellclass", lambda c: (c == "IS-SIGNIFICANT / OOS-DEAD").sum()),
                             median_ratio=("ratio_vs_FAMILY", "median"))
P(gb.to_string(float_format=lambda x: f"{x:.4f}"))

# ================================================================== RULE 8
P("\n" + "=" * 100); P("RULE 8 — WF-A: each arm's (level, cadence) chosen on IS Sharpe ALONE, 2017+ read ONCE")
P("=" * 100)
ie0, os0 = SPLITS["S2016"]
for pname, (px, spy_px) in PX.items():
    start = px.index[260]
    lf, _, _ = fast_backtest(px.join(spy_px.rename("SPY")),
                             rules_v2_weights(px.join(spy_px.rename("SPY"))), COST_BPS, "W")
    live_s = stat(lf.loc[start:], ie0, os0)
    spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:], ie0, os0)
    for family in FAMILIES:
        for con in CONSTRUCTIONS:
            arm = G[(G.panel == pname) & (G.family == family) & (G.con == con)]
            pick = arm.loc[arm.isSharpe.idxmax()]
            wfa.append(dict(panel=pname, family=family, con=con,
                            pick=f"level={pick.level} cad={pick.cad}", IS_Sharpe=pick.isSharpe,
                            OOS_CAGR=pick.oCAGR, OOS_Sharpe=pick.oSharpe, OOS_MaxDD=pick.oMaxDD,
                            v2_OOS_CAGR=live_s["oCAGR"], v2_OOS_Sharpe=live_s["oSharpe"],
                            v2_OOS_MaxDD=live_s["oMaxDD"], SPY_OOS_CAGR=spy_s["oCAGR"],
                            SPY_OOS_Sharpe=spy_s["oSharpe"], SPY_OOS_MaxDD=spy_s["oMaxDD"],
                            beats_v2=pick.oSharpe > live_s["oSharpe"],
                            beats_SPY=pick.oSharpe > spy_s["oSharpe"],
                            p4a=bool(pick.p4a), p4b=bool(pick.p4b)))
W = pd.DataFrame(wfa); W.to_csv(f"{OUT}.walkforward.csv", index=False)
P(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
P(f"\nWF-A: beats RULES v2 OOS Sharpe {int(W.beats_v2.sum())}/{len(W)}; beats SPY OOS Sharpe "
  f"{int(W.beats_SPY.sum())}/{len(W)}; 4a {int(W.p4a.sum())}/{len(W)}; 4b {int(W.p4b.sum())}/{len(W)}")

P("\n" + "=" * 100); P("RULE 8 — WF-C: does an IS-fitted predictor CHOOSE the construction better?")
P("=" * 100)
wfc = []
for sp in SPLITS:
    d = C0[C0.split == sp].reset_index(drop=True)
    always_rs, always_dg = d.oSharpe_rs.mean(), d.oSharpe_dg.mean()
    oracle = np.maximum(d.oSharpe_rs.values, d.oSharpe_dg.values).mean()
    truth_dg = (d.oSharpe_dg > d.oSharpe_rs).values
    for f in fits:
        if f["split"] != sp: continue
        pick_dg = (d.pred_is.values + f["pred"]) > 0          # predicted gap0 > 0 -> DEGROSS
        picked = np.where(pick_dg, d.oSharpe_dg.values, d.oSharpe_rs.values).mean()
        wfc.append(dict(split=sp, form=f["form"], n_DEGROSS=int(pick_dg.sum()),
                        hit_rate=float((pick_dg == truth_dg).mean()),
                        OOS_Sharpe_pick=picked, vs_RESPREAD=picked - always_rs,
                        vs_DEGROSS=picked - always_dg, oracle=oracle))
WC = pd.DataFrame(wfc); WC.to_csv(f"{OUT}.wfc.csv", index=False)
for sp in SPLITS:
    s = WC[WC.split == sp]
    P(f"\n--- split {sp}: always-RESPREAD {s.OOS_Sharpe_pick.iloc[0] - s.vs_RESPREAD.iloc[0]:.4f} | "
      f"always-DEGROSS {s.OOS_Sharpe_pick.iloc[0] - s.vs_DEGROSS.iloc[0]:.4f} | oracle {s.oracle.iloc[0]:.4f} ---")
    P(s[["form", "n_DEGROSS", "hit_rate", "OOS_Sharpe_pick", "vs_RESPREAD", "vs_DEGROSS"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
P(f"\nWF-C: forms beating always-DEGROSS: "
  f"{int((WC.vs_DEGROSS > 0).sum())}/{len(WC)}; beating always-RESPREAD: {int((WC.vs_RESPREAD > 0).sum())}/{len(WC)}")

P("\n" + "=" * 100); P("BOTH KEEP PATHS on all 324 books")
P("=" * 100)
P(f"  4a SAME-PANEL comparand (PROTOCOL rule 3 / baseline.compare): {int(G.p4a.sum())}/{len(G)}")
P(f"  4a IDEA 538 convention (U56 comparand reindexed onto every panel): {int(G.p4a_538conv.sum())}/{len(G)}")
P(f"  4b (vs SPY, both halves + OOS + DD cap + CAGR floor): {int(G.p4b.sum())}/{len(G)}")
P(G.groupby(["panel", "con"]).agg(n=("p4a", "size"), p4a_samepanel=("p4a", "sum"),
                                  p4a_538conv=("p4a_538conv", "sum"), p4b=("p4b", "sum")).to_string())
P(f"\nwrote {OUT.name}.grid.csv .cells.csv .ladder.csv .walkforward.csv .wfc.csv  ({time.time()-t0:.0f}s)")
Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
