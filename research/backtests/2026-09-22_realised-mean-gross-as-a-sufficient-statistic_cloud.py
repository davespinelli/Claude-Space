#!/usr/bin/env python3
"""Idea 1494 (lane cloud, 2026-09-22): is REALISED MEAN GROSS a SUFFICIENT STATISTIC for
every DEVICE-vs-DEGROSS loss in the record?

THE DEFECT THIS PRICES.  Eight 2026-09-19 runs each built a different "drawdown-buying
device" (a band, a trailing stop, a vol target, a max-vol gate, an MA-distance gate, a
market filter) over the same book and each found the device BEATEN at matched exposure by
a plain de-gross.  Eight separate findings, eight separate slugs.  If a device's CAGR and
MaxDD are fully explained by the ONE scalar it moves -- its realised mean gross -- then the
record has re-discovered one scalar eight times and every one of those runs is the same
run.  The test is a RESIDUAL, not a tally.

CONSTRUCTION
  BASE (frozen, the record's committed anchor shape): top-N by H-day momentum among names
  above their 200d MA with vol20 < 0.60, equal weight at gross 0.75, weekly, 10 bps, t+1.
  TUNED PARAMETERS: exactly two, (N, H) = (20, 126), FROZEN at the committed anchor and NOT
  searched here.  Every device rung and every gross rung below is PUBLISHED, none selected.

  DEVICE = an overlay that withdraws exposure.  Six families x five rungs x three panels
  = 90 device books, all published.
  TWIN     = the SAME base book multiplied by a CONSTANT chosen so its realised mean gross
             equals the device's (two Newton passes; achieved match published as gate G1).
             This is the exact prediction of the sufficiency model AT the device's own gross.
  LADDER   = the base book at 16 published constant scale factors, giving the pure
             gross->metric curve g |-> (CAGR, MaxDD, Sharpe) independent of any device.

  RESIDUAL (the headline).  For metric M in {CAGR, MaxDD, Sharpe}:
      R_twin(i)   = M(device_i) - M(twin_i)                 # exact, paired, same gross
      R_ladder(i) = M(device_i) - interp_ladder(M; g_dev_i)  # model-based cross-check
  If realised mean gross is sufficient, BOTH are zero for every device, every family, every
  panel.  The residual is reported WITH an SE from a CIRCULAR BLOCK BOOTSTRAP (LB = 65
  trading days, B = 400, the SAME blocks drawn for every book and panel in a replicate so
  cross-book dependence is carried, not assumed away), and as a per-family OLS R^2 of the
  metric on realised gross ALONE.

  CAPITAL ARM.  Every device book, every twin and every ladder rung is a real weights
  function.  Both KEEP paths (4a vs live RULES v2, 4b vs SPY) are evaluated at all of them,
  and PROTOCOL rule 8's walk-forward is run twice: a DEVICE chooser (argmax IS Sharpe over
  the 30 device books) against a GROSS-ONLY chooser (argmax IS Sharpe over the 16 ladder
  rungs), both picked on 2009/2010-2016 alone with 2017-2026 read exactly once.  If gross is
  sufficient the gross-only chooser should not be beaten out of sample.

PROTOCOL: rule 1 (committed caches, >= 10y); rule 2 (10 bps, t+1, long-only, no leverage);
rule 3 (live RULES v2 AND SPY); rule 4 (both KEEP paths at every cell, 2 tuned params, both
frozen); rule 5 (one idea, one deterministic script); rule 7 (honest report); rule 8
(walk-forward, OOS read once); rule 9 (broad panel survivorship stated).

SURVIVORSHIP CAVEAT.  B136 and SMALL are CURRENT constituents of their screens, so both
carry survivorship bias; SMALL additionally drops every ticker with max_1d_move >= 1.0 in
data/small_meta.csv before use.  Levels on those panels are upward-biased; the residual is a
WITHIN-PANEL, WITHIN-BOOK contrast (device minus its own twin on the same names and days),
which is the quantity the bias cancels out of.

Run: python3 research/backtests/2026-09-22_realised-mean-gross-as-a-sufficient-statistic_cloud.py
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state          # noqa
from engine import backtest                                              # noqa

SLUG      = "2026-09-22_realised-mean-gross-as-a-sufficient-statistic_cloud"
OUT       = ROOT / "research" / "backtests"
SEED      = 20260922
N_FROZEN  = 20        # tuned parameter 1 (frozen at the committed anchor)
H_FROZEN  = 126       # tuned parameter 2 (frozen at the committed anchor)
GROSS     = 0.75
MAXVOL    = 0.60
COST_BPS  = 10
FREQ      = "W"
WARMUP    = 260       # rows skipped, same convention as baseline.compare
OOS_START = pd.Timestamp("2017-01-01")
LB        = 65
NBOOT     = 400
STOP_FRAC = 0.50      # trailing-stop re-entry fraction, frozen at the record's value
LADDER_F  = (0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90,
             1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 1.60)

LOG = []
def log(s):
    print(s, flush=True); LOG.append(str(s))

# ------------------------------------------------------------------ book construction
def base_weights(px, cols, maxvol=MAXVOL, madist=0.0, band=None):
    """Top-N momentum, equal weight, gross 0.75, over `cols` only (SPY is a benchmark on
    SMALL, never a constituent).  maxvol / madist / band are the eligibility-side devices;
    at their base rungs this returns the frozen BASE book."""
    p     = px[cols]
    mom   = p / p.shift(H_FROZEN) - 1
    ma200 = p.rolling(200).mean()
    vol20 = p.pct_change().rolling(20).std() * np.sqrt(252)
    above = band_state(p, band) if band is not None else (p > ma200 * (1 + madist))
    elig  = mom.where(above & (vol20 < maxvol))
    rank  = elig.rank(axis=1, ascending=False)
    w     = (rank <= N_FROZEN).astype(float) * (GROSS / N_FROZEN)
    return w.reindex(columns=px.columns).fillna(0.0)

def trailing_stop_mult(eq, depth, frac=STOP_FRAC):
    """Causal 0/1 gross multiplier from the BASE book's OWN equity: out when the base book
    is `depth` below its running peak, back in once it has recovered `frac` of that fall.
    Decided at close t; the engine applies weights at t+1."""
    e = eq.ffill().bfill().values
    m = np.ones(len(e)); peak = e[0]; out = False; trough = np.nan
    for i in range(len(e)):
        if not out:
            peak = max(peak, e[i])
            if e[i] <= peak * (1 - depth):
                out = True; trough = e[i]
        else:
            trough = min(trough, e[i])
            if e[i] >= trough + frac * (peak - trough):
                out = False; peak = max(peak, e[i])
        m[i] = 0.0 if out else 1.0
    return pd.Series(m, index=eq.index)

def device_books(px, cols, base_w, base_r, base_eq):
    """-> {(family, rung_label): weights}.  Six families x five rungs, every rung published."""
    out = {}
    for c in (0.02, 0.04, 0.06, 0.08, 0.10):
        out[("BAND",   f"c={c:.2f}")]  = base_weights(px, cols, band=c)
    for d in (0.05, 0.075, 0.10, 0.15, 0.20):
        out[("STOP",   f"d={d:.3f}")]  = base_w.mul(trailing_stop_mult(base_eq, d), axis=0)
    rv = base_r.rolling(20).std() * np.sqrt(252)
    for v in (0.08, 0.10, 0.12, 0.15, 0.20):
        s = (v / rv.replace(0, np.nan)).clip(upper=1.0).fillna(1.0)
        out[("VOLTGT", f"v={v:.2f}")]  = base_w.mul(s.reindex(base_w.index).fillna(1.0), axis=0)
    for m in (0.25, 0.35, 0.45, 0.60, 0.80):
        out[("MAXVOL", f"m={m:.2f}")]  = base_weights(px, cols, maxvol=m)
    for k in (0.00, 0.03, 0.06, 0.10, 0.15):
        out[("MADIST", f"k={k:.2f}")]  = base_weights(px, cols, madist=k)
    spy = px["SPY"]
    for L in (100, 150, 200, 250, 300):
        ind = (spy > spy.rolling(L).mean()).astype(float)
        out[("SPYFILT", f"L={L}")]     = base_w.mul(ind, axis=0)
    return out

# ------------------------------------------------------------------ metrics
def sharpe(r): s = r.std(); return r.mean() * 252 / (s * np.sqrt(252)) if s > 0 else np.nan
def maxdd(r):  e = (1 + r).cumprod(); return (e / e.cummax() - 1).min()
def cagr(r):   e = (1 + r).cumprod(); return e.iloc[-1] ** (252 / len(r)) - 1

def full_metrics(r):
    h = len(r) // 2
    o = r.loc[OOS_START:]
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r),
                H1=sharpe(r.iloc[:h]), H2=sharpe(r.iloc[h:]),
                OOS_CAGR=cagr(o), OOS_Sharpe=sharpe(o), OOS_MaxDD=maxdd(o))

def keep_paths(m, base_m, spy_m):
    """4a: Sharpe > live RULES v2 in BOTH halves AND MaxDD no worse.
       4b: Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's (i.e. the
           signed MaxDD >= 0.60 * SPY's signed MaxDD), CAGR >= 70% of SPY's."""
    a = (m["H1"] > base_m["H1"]) and (m["H2"] > base_m["H2"]) and (m["MaxDD"] >= base_m["MaxDD"])
    b = (m["H1"] > spy_m["H1"]) and (m["H2"] > spy_m["H2"]) and (m["OOS_Sharpe"] > spy_m["OOS_Sharpe"]) \
        and (m["MaxDD"] >= 0.60 * spy_m["MaxDD"]) and (m["CAGR"] >= 0.70 * spy_m["CAGR"])
    return a, b

def run_book(px, w, start):
    res   = backtest(px, w, cost_bps=COST_BPS, freq=FREQ)
    r     = res["returns"].loc[start:]
    gross = res["weights"].sum(axis=1).loc[start:].mean()
    return r, gross, res["equity"]

# ------------------------------------------------------------------ bootstrap
def block_boot_stats(D, A, rng, nboot=NBOOT, lb=LB):
    """Circular block bootstrap over the SAME day-blocks for every column of D (device) and
    A (twin).  Returns arrays (nboot, k) of resampled d_CAGR, d_MaxDD, d_Sharpe."""
    T, k = D.shape
    nb   = int(np.ceil(T / lb))
    outC = np.empty((nboot, k)); outD = np.empty((nboot, k)); outS = np.empty((nboot, k))
    for b in range(nboot):
        st  = rng.integers(0, T, size=nb)
        idx = (st[:, None] + np.arange(lb)[None, :]).ravel() % T
        idx = idx[:T]
        d, a = D[idx], A[idx]
        for X, col in ((d, 0), (a, 1)):
            e  = np.cumprod(1 + np.nan_to_num(X, nan=0.0), axis=0)
            cg = e[-1] ** (252 / T) - 1
            dd = (e / np.maximum.accumulate(e, axis=0) - 1).min(axis=0)
            sd = np.nanstd(X, axis=0)
            sh = np.where(sd > 0, np.nanmean(X, axis=0) * 252 / (sd * np.sqrt(252)), np.nan)
            if col == 0: cgd, ddd, shd = cg, dd, sh
            else:        cga, dda, sha = cg, dd, sh
        outC[b] = cgd - cga; outD[b] = ddd - dda; outS[b] = shd - sha
    return outC, outD, outS

# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    gates, rows, ladder_rows, series = [], [], [], {}

    panels = {}
    for lbl, kw in (("U56", {}), ("B136", dict(broad=True)), ("SMALL", dict(small=True))):
        px = load_universe(**kw)
        if lbl == "SMALL":
            meta    = pd.read_csv(ROOT / "data" / "small_meta.csv")
            bad     = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"].astype(str))
            mx      = px.drop(columns=["SPY"]).pct_change().abs().max()
            bad    |= {c for c in mx.index if mx[c] >= 1.0}
            cols    = [c for c in px.columns if c != "SPY" and c not in bad]
            gates.append(("G0 SMALL house filter",
                          f"{len(bad & set(px.columns))} tickers dropped (max_1d_move >= 1.0); "
                          f"{len(cols)} names kept + SPY as benchmark only"))
        else:
            cols = [c for c in px.columns]
        start = px.index[WARMUP]
        bw    = base_weights(px, cols)
        br, bg, beq = run_book(px, bw, start)
        spy_r = px["SPY"].pct_change().fillna(0.0).loc[start:]
        v2_r  = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        panels[lbl] = dict(px=px, cols=cols, start=start, base_w=bw, base_r=br, base_g=bg,
                           base_eq=beq, spy_m=full_metrics(spy_r), v2_m=full_metrics(v2_r),
                           spy_r=spy_r, v2_r=v2_r, base_m=full_metrics(br))
        log(f"[{lbl}] {len(cols)} selectable names  {start.date()}..{px.index[-1].date()}  "
            f"base realised gross {bg:.4f}  base Sharpe {sharpe(br):.4f}  ({time.time()-t0:.0f}s)")

    # ---------------------------------------------------------- gross ladder (per panel)
    for lbl, P in panels.items():
        for f in LADDER_F:
            r, g, _ = run_book(P["px"], P["base_w"] * f, P["start"])
            m = full_metrics(r)
            a, b = keep_paths(m, P["v2_m"], P["spy_m"])
            ladder_rows.append(dict(panel=lbl, f=f, gross=g, keep4a=a, keep4b=b, **m))
            series[(lbl, "LADDER", f"f={f:.2f}")] = r
        log(f"[{lbl}] gross ladder done ({time.time()-t0:.0f}s)")
    lad = pd.DataFrame(ladder_rows)

    def ladder_interp(lbl, metric, g):
        sub = lad[lad.panel == lbl].sort_values("gross")
        return float(np.interp(g, sub["gross"].values, sub[metric].values))

    # ---------------------------------------------------------- devices + matched twins
    for lbl, P in panels.items():
        px, cols, start, bw = P["px"], P["cols"], P["start"], P["base_w"]
        books = device_books(px, cols, bw, P["base_r"], P["base_eq"])
        for (fam, rung), w in books.items():
            dr, dg, _ = run_book(px, w, start)
            f = dg / P["base_g"]
            ar, ag, _ = run_book(px, bw * f, start)
            if ag > 0:                                   # one Newton correction pass
                f *= dg / ag
                ar, ag, _ = run_book(px, bw * f, start)
            dm, am = full_metrics(dr), full_metrics(ar)
            a4, b4 = keep_paths(dm, P["v2_m"], P["spy_m"])
            aa, ab = keep_paths(am, P["v2_m"], P["spy_m"])
            rows.append(dict(
                panel=lbl, family=fam, rung=rung, gross_dev=dg, gross_twin=ag,
                gross_err=ag - dg, scale=f,
                R_twin_CAGR=dm["CAGR"] - am["CAGR"], R_twin_MaxDD=dm["MaxDD"] - am["MaxDD"],
                R_twin_Sharpe=dm["Sharpe"] - am["Sharpe"],
                R_lad_CAGR=dm["CAGR"] - ladder_interp(lbl, "CAGR", dg),
                R_lad_MaxDD=dm["MaxDD"] - ladder_interp(lbl, "MaxDD", dg),
                R_lad_Sharpe=dm["Sharpe"] - ladder_interp(lbl, "Sharpe", dg),
                keep4a=a4, keep4b=b4, twin_keep4a=aa, twin_keep4b=ab,
                twin_CAGR=am["CAGR"], twin_MaxDD=am["MaxDD"], twin_Sharpe=am["Sharpe"],
                twin_OOS_Sharpe=am["OOS_Sharpe"], **dm))
            series[(lbl, fam, rung)]        = dr
            series[(lbl, fam + "_TWIN", rung)] = ar
            log(f"  [{lbl}] {fam:8s} {rung:9s} g {dg:.4f}/{ag:.4f}  "
                f"CAGR {dm['CAGR']:+.4f} vs {am['CAGR']:+.4f} (R {dm['CAGR']-am['CAGR']:+.4f})  "
                f"DD {dm['MaxDD']:+.4f} vs {am['MaxDD']:+.4f} (R {dm['MaxDD']-am['MaxDD']:+.4f})  "
                f"({time.time()-t0:.0f}s)")
    dev = pd.DataFrame(rows)

    gates.append(("G1 twin gross match",
                  f"max |realised gross(twin) - realised gross(device)| = "
                  f"{dev.gross_err.abs().max():.2e} over {len(dev)} books; "
                  f"median {dev.gross_err.abs().median():.2e}"))

    # ---------------------------------------------------------- bootstrap SEs
    union = panels["U56"]["px"].index
    union = union[union >= panels["U56"]["start"]]
    keys  = [(r.panel, r.family, r.rung) for r in dev.itertuples()]
    D = np.column_stack([series[(p, f, u)].reindex(union).values for p, f, u in keys])
    A = np.column_stack([series[(p, f + "_TWIN", u)].reindex(union).values for p, f, u in keys])
    bC, bD, bS = block_boot_stats(np.nan_to_num(D), np.nan_to_num(A), rng)
    dev["se_CAGR"]   = bC.std(axis=0)
    dev["se_MaxDD"]  = bD.std(axis=0)
    dev["se_Sharpe"] = bS.std(axis=0)
    dev["t_CAGR"]    = dev.R_twin_CAGR   / dev.se_CAGR.replace(0, np.nan)
    dev["t_MaxDD"]   = dev.R_twin_MaxDD  / dev.se_MaxDD.replace(0, np.nan)
    dev["t_Sharpe"]  = dev.R_twin_Sharpe / dev.se_Sharpe.replace(0, np.nan)
    gates.append(("G2 bootstrap", f"circular block bootstrap LB={LB}d, B={NBOOT}, seed {SEED}; "
                                  f"same blocks for all {len(keys)} books in a replicate"))

    # ---------------------------------------------------------- headline: sufficiency
    log("\n=== A. IS REALISED MEAN GROSS SUFFICIENT?  RESIDUAL OF DEVICE MINUS ITS MATCHED TWIN ===")
    log(f"{'panel':6s} {'family':8s} {'n':>2s} {'R_CAGR':>9s} {'SE':>7s} {'t':>7s} "
        f"{'R_MaxDD':>9s} {'SE':>7s} {'t':>7s} {'R_Sharpe':>9s} {'SE':>7s} {'t':>7s}")
    fam_rows = []
    for (p, f), grp in dev.groupby(["panel", "family"]):
        n = len(grp)
        rec = dict(panel=p, family=f, n=n)
        for lab, col in (("CAGR", "R_twin_CAGR"), ("MaxDD", "R_twin_MaxDD"), ("Sharpe", "R_twin_Sharpe")):
            mean = grp[col].mean()
            se   = {"CAGR": bC, "MaxDD": bD, "Sharpe": bS}[lab][:, grp.index.values].mean(axis=1).std()
            rec[f"mean_{lab}"] = mean; rec[f"se_{lab}"] = se
            rec[f"t_{lab}"] = mean / se if se > 0 else np.nan
        fam_rows.append(rec)
        log(f"{p:6s} {f:8s} {n:2d} "
            f"{rec['mean_CAGR']:+9.4f} {rec['se_CAGR']:7.4f} {rec['t_CAGR']:+7.2f} "
            f"{rec['mean_MaxDD']:+9.4f} {rec['se_MaxDD']:7.4f} {rec['t_MaxDD']:+7.2f} "
            f"{rec['mean_Sharpe']:+9.4f} {rec['se_Sharpe']:7.4f} {rec['t_Sharpe']:+7.2f}")
    fam = pd.DataFrame(fam_rows)

    for lab, arr, col in (("CAGR", bC, "R_twin_CAGR"), ("MaxDD", bD, "R_twin_MaxDD"),
                          ("Sharpe", bS, "R_twin_Sharpe")):
        m  = dev[col].mean(); se = arr.mean(axis=1).std()
        log(f"POOLED (all {len(dev)} books) R_{lab:6s} = {m:+.4f}  SE {se:.4f}  "
            f"t {m/se if se>0 else float('nan'):+.2f}")

    # OLS of each metric on realised mean gross ALONE, within panel x family
    log("\n=== B. OLS OF THE METRIC ON REALISED MEAN GROSS ALONE (device books only) ===")
    log(f"{'panel':6s} {'family':8s} {'R2_CAGR':>8s} {'sd_res':>9s} {'R2_MaxDD':>9s} {'sd_res':>9s}")
    ols_rows = []
    for (p, f), grp in dev.groupby(["panel", "family"]):
        rec = dict(panel=p, family=f)
        for lab in ("CAGR", "MaxDD"):
            x = grp.gross_dev.values; y = grp[lab].values
            if len(x) > 2 and x.std() > 1e-12:
                b1 = np.cov(x, y, bias=True)[0, 1] / x.var()
                b0 = y.mean() - b1 * x.mean()
                res = y - (b0 + b1 * x)
                r2  = 1 - res.var() / y.var() if y.var() > 0 else np.nan
            else:
                r2, res, b1 = np.nan, np.array([np.nan]), np.nan
            rec[f"R2_{lab}"] = r2; rec[f"sdres_{lab}"] = res.std(ddof=0); rec[f"slope_{lab}"] = b1
        ols_rows.append(rec)
        log(f"{p:6s} {f:8s} {rec['R2_CAGR']:8.4f} {rec['sdres_CAGR']:9.4f} "
            f"{rec['R2_MaxDD']:9.4f} {rec['sdres_MaxDD']:9.4f}")
    ols = pd.DataFrame(ols_rows)

    # pooled-within-panel OLS across ALL device books (the "one scalar" model)
    log("")
    for p, grp in dev.groupby("panel"):
        for lab in ("CAGR", "MaxDD"):
            x, y = grp.gross_dev.values, grp[lab].values
            b1 = np.cov(x, y, bias=True)[0, 1] / x.var(); b0 = y.mean() - b1 * x.mean()
            r2 = 1 - (y - (b0 + b1 * x)).var() / y.var()
            log(f"POOLED-WITHIN-PANEL {p:6s} {lab:6s} on gross alone: R2 = {r2:.4f}  "
                f"slope {b1:+.4f}  residual sd {(y-(b0+b1*x)).std():.4f}")

    # ---------------------------------------------------------- C. KEEP paths
    log("\n=== C. KEEP PATHS AT EVERY PUBLISHED CELL ===")
    log(f"devices: 4a {int(dev.keep4a.sum())} of {len(dev)}   4b {int(dev.keep4b.sum())} of {len(dev)}")
    log(f"twins:   4a {int(dev.twin_keep4a.sum())} of {len(dev)}   4b {int(dev.twin_keep4b.sum())} of {len(dev)}")
    log(f"ladder:  4a {int(lad.keep4a.sum())} of {len(lad)}   4b {int(lad.keep4b.sum())} of {len(lad)}")
    for p, grp in dev.groupby("panel"):
        log(f"  {p:6s} devices 4a {int(grp.keep4a.sum()):2d}/{len(grp)}  4b {int(grp.keep4b.sum()):2d}/{len(grp)}"
            f"   twins 4a {int(grp.twin_keep4a.sum()):2d}/{len(grp)}  4b {int(grp.twin_keep4b.sum()):2d}/{len(grp)}")
    for p, grp in lad.groupby("panel"):
        log(f"  {p:6s} ladder  4a {int(grp.keep4a.sum()):2d}/{len(grp)}  4b {int(grp.keep4b.sum()):2d}/{len(grp)}")
        pas = grp[grp.keep4b]
        for r in pas.itertuples():
            log(f"      4b PASS ladder f={r.f:.2f} gross {r.gross:.3f}: CAGR {r.CAGR:.2%} "
                f"Sharpe {r.Sharpe:.4f} MaxDD {r.MaxDD:.2%} OOS Sh {r.OOS_Sharpe:.4f}")

    # ---------------------------------------------------------- D. rule 8 walk-forward
    log("\n=== D. PROTOCOL RULE 8 WALK-FORWARD: DEVICE CHOOSER vs GROSS-ONLY CHOOSER ===")
    log("    dials chosen on the IS window (panel start .. 2016-12-31) ONLY; 2017-2026 read once.")
    wf = []
    for lbl, P in panels.items():
        spy_r, v2_r, base_r = P["spy_r"], P["v2_r"], P["base_r"]
        def _is(r):  return r.loc[:OOS_START - pd.Timedelta(days=1)]
        def _oos(r): return r.loc[OOS_START:]
        cand_dev = {(f, u): series[(lbl, f, u)] for (p, f, u) in
                    [(r.panel, r.family, r.rung) for r in dev.itertuples()] if p == lbl}
        cand_lad = {("LADDER", f"f={f:.2f}"): series[(lbl, "LADDER", f"f={f:.2f}")] for f in LADDER_F}
        picks = {}
        for nm, cands in (("DEVICE", cand_dev), ("GROSS-ONLY", cand_lad)):
            k = max(cands, key=lambda kk: sharpe(_is(cands[kk])))
            picks[nm] = (k, cands[k])
        for nm, (k, r) in picks.items():
            o = _oos(r)
            rec = dict(panel=lbl, chooser=nm, pick=f"{k[0]} {k[1]}",
                       IS_Sharpe=sharpe(_is(r)), OOS_CAGR=cagr(o), OOS_Sharpe=sharpe(o),
                       OOS_MaxDD=maxdd(o))
            wf.append(rec)
            log(f"  [{lbl}] {nm:11s} picks {rec['pick']:18s} IS Sh {rec['IS_Sharpe']:.4f}  ->  "
                f"OOS CAGR {rec['OOS_CAGR']:.2%}  Sharpe {rec['OOS_Sharpe']:.4f}  MaxDD {rec['OOS_MaxDD']:.2%}")
        for nm, r in (("BASE", base_r), ("RULES v2 (live)", v2_r), ("SPY", spy_r)):
            o = _oos(r)
            wf.append(dict(panel=lbl, chooser=nm, pick="-", IS_Sharpe=sharpe(_is(r)),
                           OOS_CAGR=cagr(o), OOS_Sharpe=sharpe(o), OOS_MaxDD=maxdd(o)))
            log(f"  [{lbl}] {nm:11s} {'':24s} IS Sh {sharpe(_is(r)):.4f}  ->  "
                f"OOS CAGR {cagr(o):.2%}  Sharpe {sharpe(o):.4f}  MaxDD {maxdd(o):.2%}")
        d = [w for w in wf if w["panel"] == lbl and w["chooser"] == "DEVICE"][0]
        g = [w for w in wf if w["panel"] == lbl and w["chooser"] == "GROSS-ONLY"][0]
        log(f"  [{lbl}] SUFFICIENCY OOS GAP (device - gross-only): "
            f"Sharpe {d['OOS_Sharpe']-g['OOS_Sharpe']:+.4f}  CAGR {d['OOS_CAGR']-g['OOS_CAGR']:+.2%}  "
            f"MaxDD {d['OOS_MaxDD']-g['OOS_MaxDD']:+.2%}")
    wfd = pd.DataFrame(wf)

    # ---------------------------------------------------------- E. full/half/OOS table
    log("\n=== E. LEVELS: BASE, LIVE RULES v2, SPY (full / halves / OOS) ===")
    for lbl, P in panels.items():
        for nm, m in (("BASE", P["base_m"]), ("RULES v2 (live)", P["v2_m"]), ("SPY", P["spy_m"])):
            log(f"  [{lbl}] {nm:16s} CAGR {m['CAGR']:7.2%}  Sharpe {m['Sharpe']:.4f}  "
                f"MaxDD {m['MaxDD']:7.2%}  H1/H2 {m['H1']:.4f}/{m['H2']:.4f}  "
                f"OOS {m['OOS_CAGR']:7.2%}/{m['OOS_Sharpe']:.4f}/{m['OOS_MaxDD']:7.2%}")

    log("\n=== GATES ===")
    for k, v in gates: log(f"  {k}: {v}")

    dev.to_csv(OUT / f"{SLUG}.devices.csv", index=False)
    lad.to_csv(OUT / f"{SLUG}.ladder.csv", index=False)
    fam.to_csv(OUT / f"{SLUG}.family.csv", index=False)
    ols.to_csv(OUT / f"{SLUG}.ols.csv", index=False)
    wfd.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    pd.DataFrame(gates, columns=["gate", "value"]).to_csv(OUT / f"{SLUG}.gates.csv", index=False)
    (OUT / f"{SLUG}.console.txt").write_text("\n".join(LOG) + "\n")
    log(f"\ndone in {time.time()-t0:.0f}s")
    (OUT / f"{SLUG}.console.txt").write_text("\n".join(LOG) + "\n")

if __name__ == "__main__":
    main()
