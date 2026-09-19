#!/usr/bin/env python3
"""Idea 1534 (lane C, 2026-09-19): does ANY ruler ever rescue a DEVICE, or is the
device side of the record simply EMPTY?

The record has eleven runs returning 4a = 0 and a standing count of "no device beats a
de-gross".  A COUNT OF FAILURES is not a number.  This run pools every device book it can
build into ONE panel-pooled paired test against each book's OWN matched-exposure de-gross
anchor, and reports the pooled effect WITH ITS SE, so the record can state an EFFECT SIZE
and a confidence interval instead of a tally.

CONSTRUCTION
  BASE (frozen, the record's 2026-09-04 anchor shape): top-N by H-day momentum among names
  above their 200d MA with vol20 < 0.60, equal weight at gross 0.75, weekly, 10 bps, t+1.
  TUNED PARAMETERS: exactly two, (N, H) = (20, 126), FROZEN at the committed anchor; they
  are not searched here.  Every device rung below is PUBLISHED, none is selected.

  DEVICE = any overlay that withdraws exposure (a "ruler" over the book).  Six families x
  five rungs x three panels = 90 device books.
  ANCHOR = the SAME base book de-grossed by a CONSTANT so that its realised mean gross
  equals the device's realised mean gross (one Newton correction pass; the achieved match
  is published as gate G1).  This is the "plain de-gross twin".

  PAIRED STATISTIC  d_i = Sharpe(device_i) - Sharpe(anchor_i), likewise for CAGR and MaxDD.
  POOLED EFFECT     mean_i d_i, with an SE from a CIRCULAR BLOCK BOOTSTRAP over calendar
  blocks (LB = 65 trading days ~ the record's LB = 13 rebalance rows), the SAME blocks drawn
  for every book and every panel in a replicate, so cross-book and cross-panel dependence is
  carried, not assumed away.  B = 500.

Run: python3 research/backtests/2026-09-19_pooled-device-vs-degross_C.py
"""
import sys, json, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state          # noqa
from engine import backtest, metrics                                      # noqa

SEED      = 20260919
N_FROZEN  = 20        # tuned parameter 1 (frozen at the committed anchor)
H_FROZEN  = 126       # tuned parameter 2 (frozen at the committed anchor)
GROSS     = 0.75
MAXVOL    = 0.60
COST_BPS  = 10
FREQ      = "W"
WARMUP    = 260       # rows skipped, same convention as baseline.compare
OOS_START = pd.Timestamp("2017-01-01")
LB        = 65        # bootstrap block length in trading days
NBOOT     = 500
STOP_FRAC = 0.50      # re-entry fraction, frozen (idea 1468's committed value)

# ------------------------------------------------------------------ book construction
def _feat(px):
    mom   = px / px.shift(H_FROZEN) - 1
    ma200 = px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    return mom, ma200, vol20

def base_weights(px, maxvol=MAXVOL, madist=0.0, band=None):
    """Top-N momentum, equal weight, gross 0.75.  maxvol / madist / band are the
    eligibility-side devices; at their base rungs this returns the frozen BASE book."""
    mom, ma200, vol20 = _feat(px)
    above = band_state(px, band) if band is not None else (px > ma200 * (1 + madist))
    elig  = mom.where(above & (vol20 < maxvol))
    rank  = elig.rank(axis=1, ascending=False)
    return (rank <= N_FROZEN).astype(float) * (GROSS / N_FROZEN)

def run(px, w, start):
    res = backtest(px, w, cost_bps=COST_BPS, freq=FREQ)
    r     = res["returns"].loc[start:]
    gross = res["weights"].sum(axis=1).loc[start:].mean()
    return r, gross

def trailing_stop_mult(eq, depth, frac=STOP_FRAC):
    """Causal 0/1 gross multiplier from the BASE book's own equity: out when the base book
    is `depth` below its running peak, back in once it has recovered `frac` of that fall.
    Decided at close t; the engine applies weights at t+1."""
    eq = eq.ffill().bfill()
    e = eq.values; m = np.ones(len(e)); peak = e[0]; out = False; trough = np.nan
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

def device_books(px, base_w, base_res):
    """-> {(family, rung_label, rung_value): weights DataFrame}.  Every rung published."""
    out   = {}
    base_r, base_eq = base_res
    spy   = px["SPY"] if "SPY" in px.columns else None
    for c in (0.02, 0.04, 0.06, 0.08, 0.10):
        out[("BAND", f"c={c:.2f}", c)] = base_weights(px, band=c)
    for d in (0.05, 0.075, 0.10, 0.15, 0.20):
        out[("STOP", f"d={d:.3f}", d)] = base_w.mul(trailing_stop_mult(base_eq, d), axis=0)
    rv = base_r.rolling(20).std() * np.sqrt(252)
    for v in (0.08, 0.10, 0.12, 0.15, 0.20):
        s = (v / rv.replace(0, np.nan)).clip(upper=1.0).fillna(1.0)
        out[("VOLTGT", f"v={v:.2f}", v)] = base_w.mul(s.reindex(base_w.index).fillna(1.0), axis=0)
    for m in (0.25, 0.35, 0.45, 0.60, 0.80):
        out[("MAXVOL", f"m={m:.2f}", m)] = base_weights(px, maxvol=m)
    for k in (0.00, 0.03, 0.06, 0.10, 0.15):
        out[("MADIST", f"k={k:.2f}", k)] = base_weights(px, madist=k)
    for L in (100, 150, 200, 250, 300):
        ind = (spy > spy.rolling(L).mean()).astype(float) if spy is not None else 1.0
        out[("SPYFILT", f"L={L}", L)] = base_w.mul(ind, axis=0)
    return out

# ------------------------------------------------------------------ metric helpers
def sharpe(r):  return r.mean() * 252 / (r.std() * np.sqrt(252)) if r.std() > 0 else np.nan
def _t(e, se):  return e / se if se > 0 else float('nan')
def maxdd(r):   e = (1 + r).cumprod(); return (e / e.cummax() - 1).min()
def cagr(r):    e = (1 + r).cumprod(); return e.iloc[-1] ** (252 / len(r)) - 1

def full_metrics(r):
    h = len(r) // 2
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r),
                H1=sharpe(r.iloc[:h]), H2=sharpe(r.iloc[h:]),
                OOS_CAGR=cagr(r.loc[OOS_START:]), OOS_Sharpe=sharpe(r.loc[OOS_START:]),
                OOS_MaxDD=maxdd(r.loc[OOS_START:]))

def keep_paths(m, base_m, spy_m):
    """4a: Sharpe > live RULES v2 in BOTH halves AND MaxDD no worse.
       4b: Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's."""
    a = (m["H1"] > base_m["H1"]) and (m["H2"] > base_m["H2"]) and (m["MaxDD"] >= base_m["MaxDD"])
    b = (m["H1"] > spy_m["H1"]) and (m["H2"] > spy_m["H2"]) and (m["OOS_Sharpe"] > spy_m["OOS_Sharpe"]) \
        and (m["MaxDD"] >= 0.60 * spy_m["MaxDD"]) and (m["CAGR"] >= 0.70 * spy_m["CAGR"])
    return a, b

# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    panels = {}
    for lbl, kw in (("U56", {}), ("B136", dict(broad=True)), ("SMALL", dict(small=True))):
        px = load_universe(**kw)
        start = px.index[WARMUP]
        bw  = base_weights(px)
        br  = backtest(px, bw, cost_bps=COST_BPS, freq=FREQ)
        beq = br["equity"]
        panels[lbl] = dict(px=px, start=start, base_w=bw,
                           base_r=br["returns"].loc[start:],
                           base_gross=br["weights"].sum(axis=1).loc[start:].mean(),
                           base_eq=beq)
        print(f"[{lbl}] {px.shape[1]} names  {start.date()}..{px.index[-1].date()}  "
              f"base gross {panels[lbl]['base_gross']:.3f}  ({time.time()-t0:.0f}s)")

    rows, series = [], {}          # series: (panel, family, rung) -> (dev_r, anc_r)
    for lbl, P in panels.items():
        px, start, bw = P["px"], P["start"], P["base_w"]
        spy_r  = px["SPY"].pct_change().fillna(0).loc[start:]
        v2_r   = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        spy_m, v2_m = full_metrics(spy_r), full_metrics(v2_r)
        base_m = full_metrics(P["base_r"])
        series[(lbl, "SPY", "-")]  = (spy_r, None)
        series[(lbl, "RULESv2", "-")] = (v2_r, None)
        series[(lbl, "BASE", "-")] = (P["base_r"], None)
        a, b = keep_paths(base_m, v2_m, spy_m)
        rows.append(dict(panel=lbl, family="BASE", rung="frozen", gross_dev=P["base_gross"],
                         gross_anc=P["base_gross"], d_Sharpe=0.0, d_CAGR=0.0, d_MaxDD=0.0,
                         keep4a=a, keep4b=b, **base_m))

        books = device_books(px, bw, (P["base_r"], P["base_eq"]))
        for (fam, rung, val), w in books.items():
            dr, dg = run(px, w, start)
            # matched-exposure de-gross twin: one Newton correction on the scale factor
            f = dg / P["base_gross"]
            ar, ag = run(px, bw * f, start)
            if ag > 0:
                f *= dg / ag
                ar, ag = run(px, bw * f, start)
            dm, am = full_metrics(dr), full_metrics(ar)
            a4, b4 = keep_paths(dm, v2_m, spy_m)
            rows.append(dict(panel=lbl, family=fam, rung=rung, gross_dev=dg, gross_anc=ag,
                             d_Sharpe=dm["Sharpe"] - am["Sharpe"], d_CAGR=dm["CAGR"] - am["CAGR"],
                             d_MaxDD=dm["MaxDD"] - am["MaxDD"], keep4a=a4, keep4b=b4, **dm))
            series[(lbl, fam, rung)] = (dr, ar)
            print(f"  [{lbl}] {fam:8s} {rung:9s} gross {dg:.3f}/{ag:.3f}  "
                  f"Sh {dm['Sharpe']:.4f} vs {am['Sharpe']:.4f}  d={dm['Sharpe']-am['Sharpe']:+.4f}  "
                  f"({time.time()-t0:.0f}s)")
        panels[lbl].update(spy_m=spy_m, v2_m=v2_m, spy_r=spy_r, v2_r=v2_r, base_m=base_m)

    df = pd.DataFrame(rows)
    dev = df[df.family != "BASE"].copy()

    # ---------------------------------------------------------- block bootstrap
    pairs  = [(k, v) for k, v in series.items() if v[1] is not None]
    union  = panels["U56"]["px"].index
    union  = union[union >= panels["U56"]["start"]]
    T      = len(union)
    keys   = [k for k, _ in pairs]
    # align every pair onto the union calendar once; NaN = that panel has no row that day
    D = np.column_stack([v[0].reindex(union).values for _, v in pairs])
    A = np.column_stack([v[1].reindex(union).values for _, v in pairs])
    rng   = np.random.default_rng(SEED)
    nblk  = int(np.ceil(T / LB))
    fam_of  = np.array([k[1] for k in keys]); pan_of = np.array([k[0] for k in keys])
    fams    = ["BAND", "STOP", "VOLTGT", "MAXVOL", "MADIST", "SPYFILT"]
    boot_pooled_S = np.empty(NBOOT); boot_exstop = np.empty(NBOOT)
    boot_D = np.empty((NBOOT, len(keys)))
    boot_panel = {l: np.empty(NBOOT) for l in panels}
    boot_fam   = {f: np.empty(NBOOT) for f in fams}

    def _sh(X):
        """column-wise annualised Sharpe of a T x K array, NaNs ignored per column."""
        m  = np.nanmean(X, axis=0); sd = np.nanstd(X, axis=0, ddof=1)
        return np.where(sd > 0, m * 252 / (sd * np.sqrt(252)), np.nan)

    for b in range(NBOOT):
        starts = rng.integers(0, T, nblk)
        idx = (starts[:, None] + np.arange(LB)[None, :]).ravel()[:T] % T
        d = _sh(D[idx]) - _sh(A[idx])
        boot_D[b] = d
        boot_pooled_S[b] = np.nanmean(d)
        boot_exstop[b]   = np.nanmean(d[fam_of != "STOP"])
        for l in panels: boot_panel[l][b] = np.nanmean(d[pan_of == l])
        for f in fams:   boot_fam[f][b]   = np.nanmean(d[fam_of == f])
        if b % 100 == 0: print(f"  boot {b}/{NBOOT} ({time.time()-t0:.0f}s)")

    se_pooled = float(np.nanstd(boot_pooled_S, ddof=1))
    eff_pooled = float(dev.d_Sharpe.mean())
    se_book = np.nanstd(boot_D, axis=0, ddof=1)
    key_idx = {k: i for i, k in enumerate(keys)}
    dev["se_book"] = [se_book[key_idx[(r.panel, r.family, r.rung)]] for r in dev.itertuples()]
    dev["t_book"]  = dev.d_Sharpe / dev.se_book
    se_exstop  = float(np.nanstd(boot_exstop, ddof=1))
    eff_exstop = float(dev[dev.family != "STOP"].d_Sharpe.mean())

    # ---------------------------------------------------------- rule 8 walk-forward
    wf = []
    for lbl, P in panels.items():
        is_end = OOS_START - pd.Timedelta(days=1)
        cand = [(k, v) for k, v in series.items() if k[0] == lbl and v[1] is not None]
        pick = max(cand, key=lambda kv: sharpe(kv[1][0].loc[:is_end]))
        (_, fam, rung), (dr, ar) = pick
        dm, am = full_metrics(dr), full_metrics(ar)
        bm, sm = P["base_m"], P["spy_m"]
        a4, b4 = keep_paths(dm, P["v2_m"], sm)
        wf.append(dict(panel=lbl, pick=f"{fam} {rung}",
                       OOS_CAGR=dm["OOS_CAGR"], OOS_Sharpe=dm["OOS_Sharpe"], OOS_MaxDD=dm["OOS_MaxDD"],
                       anc_OOS_Sharpe=am["OOS_Sharpe"], anc_OOS_CAGR=am["OOS_CAGR"], anc_OOS_MaxDD=am["OOS_MaxDD"],
                       base_OOS_Sharpe=bm["OOS_Sharpe"], spy_OOS_Sharpe=sm["OOS_Sharpe"],
                       spy_OOS_CAGR=sm["OOS_CAGR"], spy_OOS_MaxDD=sm["OOS_MaxDD"],
                       keep4a=a4, keep4b=b4))
    wfdf = pd.DataFrame(wf)

    # ---------------------------------------------------------- report
    pd.set_option("display.width", 200, "display.max_rows", 400)
    print("\n" + "=" * 100)
    print("ALL GRID POINTS (90 device books + 3 BASE books), device minus its matched-exposure anchor")
    print("=" * 100)
    cols = ["panel","family","rung","gross_dev","gross_anc","CAGR","Sharpe","MaxDD","H1","H2",
            "OOS_Sharpe","d_Sharpe","d_CAGR","d_MaxDD","keep4a","keep4b"]
    print(df[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\nREFERENCE BOOKS")
    for lbl, P in panels.items():
        for nm, m in (("SPY", P["spy_m"]), ("RULES v2 (live)", P["v2_m"]), ("BASE frozen", P["base_m"])):
            print(f"  [{lbl}] {nm:16s} CAGR {m['CAGR']:.2%}  Sharpe {m['Sharpe']:.4f}  MaxDD {m['MaxDD']:.2%}  "
                  f"H1/H2 {m['H1']:.3f}/{m['H2']:.3f}  OOS {m['OOS_CAGR']:.2%}/{m['OOS_Sharpe']:.4f}/{m['OOS_MaxDD']:.2%}")

    print("\n" + "=" * 100)
    print("POOLED PAIRED TEST  (device - matched-exposure de-gross), block bootstrap "
          f"LB={LB}d, B={NBOOT}, common blocks across all books")
    print("=" * 100)
    print(f"  POOLED dSharpe over {len(dev)} books = {eff_pooled:+.4f}  SE {se_pooled:.4f}  "
          f"t {_t(eff_pooled, se_pooled):+.2f}  95% CI [{eff_pooled-1.96*se_pooled:+.4f}, {eff_pooled+1.96*se_pooled:+.4f}]")
    print(f"  POOLED dCAGR  = {dev.d_CAGR.mean():+.4%}     POOLED dMaxDD = {dev.d_MaxDD.mean():+.4%} "
          "(positive dMaxDD = shallower than the de-gross twin)")
    print(f"  POOLED dSharpe EXCLUDING the STOP family ({len(dev[dev.family!='STOP'])} books) = "
          f"{eff_exstop:+.4f}  SE {se_exstop:.4f}  t {_t(eff_exstop, se_exstop):+.2f}  "
          f"95% CI [{eff_exstop-1.96*se_exstop:+.4f}, {eff_exstop+1.96*se_exstop:+.4f}]")
    npos = int((dev.t_book > 1.96).sum()); nneg = int((dev.t_book < -1.96).sum())
    print(f"\n  PER-BOOK SIGNIFICANCE (own block-bootstrap SE, 95%): significantly POSITIVE {npos} of {len(dev)}, "
          f"significantly NEGATIVE {nneg} of {len(dev)}, indeterminate {len(dev)-npos-nneg}")
    if npos:
        print(dev[dev.t_book > 1.96][["panel","family","rung","d_Sharpe","se_book","t_book","keep4a","keep4b"]]
              .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\n  BY PANEL")
    for lbl in panels:
        sub = dev[dev.panel == lbl]; se = float(np.nanstd(boot_panel[lbl], ddof=1)); e = float(sub.d_Sharpe.mean())
        print(f"    {lbl:6s} n={len(sub):3d}  dSharpe {e:+.4f}  SE {se:.4f}  t {_t(e, se):+.2f}   "
              f"dCAGR {sub.d_CAGR.mean():+.3%}  dMaxDD {sub.d_MaxDD.mean():+.3%}  wins {int((sub.d_Sharpe>0).sum())}/{len(sub)}")
    print("\n  BY DEVICE FAMILY (pooled over three panels, five rungs)")
    for fam in ["BAND","STOP","VOLTGT","MAXVOL","MADIST","SPYFILT"]:
        sub = dev[dev.family == fam]; se = float(np.nanstd(boot_fam[fam], ddof=1)); e = float(sub.d_Sharpe.mean())
        print(f"    {fam:8s} n={len(sub):3d}  dSharpe {e:+.4f}  SE {se:.4f}  t {_t(e, se):+.2f}   "
              f"dCAGR {sub.d_CAGR.mean():+.3%}  dMaxDD {sub.d_MaxDD.mean():+.3%}  wins {int((sub.d_Sharpe>0).sum())}/{len(sub)}")

    print("\n  KEEP-PATH CENSUS over all 90 device books + 3 BASE books")
    print(f"    4a passes: {int(df.keep4a.sum())} of {len(df)}      4b passes: {int(df.keep4b.sum())} of {len(df)}")
    if df.keep4b.any():
        print(df[df.keep4b][["panel","family","rung","CAGR","Sharpe","MaxDD","H1","H2","OOS_Sharpe","d_Sharpe"]]
              .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n" + "=" * 100)
    print("RULE 8 WALK-FORWARD — device+rung chosen by argmax Sharpe on warm-up..2016-12-31 only,")
    print("2017-01-01..2026 read ONCE, against its own matched-exposure anchor, the frozen BASE and SPY")
    print("=" * 100)
    print(wfdf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dvs = (wfdf.OOS_Sharpe - wfdf.anc_OOS_Sharpe)
    print(f"\n  chooser OOS Sharpe minus its matched anchor: mean {dvs.mean():+.4f}, beats it {int((dvs>0).sum())} of {len(dvs)}")
    dvb = (wfdf.OOS_Sharpe - wfdf.base_OOS_Sharpe)
    print(f"  chooser OOS Sharpe minus the do-nothing frozen BASE: mean {dvb.mean():+.4f}, beats it {int((dvb>0).sum())} of {len(dvb)}")

    print("\nGATES")
    g1 = float((dev.gross_dev - dev.gross_anc).abs().max())
    print(f"  G1 exposure match: max |gross_device - gross_anchor| = {g1:.2e} (all 90 pairs)")
    deg = dev[((dev.family=='MAXVOL') & (dev.rung=='m=0.60')) | ((dev.family=='MADIST') & (dev.rung=='k=0.00'))]
    print(f"  G2 degenerate rungs (MAXVOL m=0.60, MADIST k=0.00 ARE the BASE): "
          f"max |dSharpe| = {deg.d_Sharpe.abs().max():.2e} over {len(deg)} books")
    print(f"  G3 sample length: " + ", ".join(f"{l} {len(P['base_r'])/252:.1f}y" for l, P in panels.items()))
    print(f"  G4 all {len(df)} books published above; G5 exactly two tuned parameters (N={N_FROZEN}, H={H_FROZEN}), both FROZEN")
    print(f"  G6 OOS starts {OOS_START.date()} on every panel; chooser reads no row at or after it")
    print(f"  G7 costs {COST_BPS} bps/unit turnover, weights t -> t+1, no shorting, no leverage (gross <= {GROSS})")
    print(f"\nSURVIVORSHIP (rule 9): U56 / B136 / SMALL are CURRENT-constituent lists, so every absolute")
    print( "  level is an upper bound. The headline is a DIFFERENCE between two books over the SAME names on")
    print( "  the SAME days, so it is first-order immune; the 4a/4b pass counts are not.")
    print(f"\ndone in {time.time()-t0:.0f}s")

    out = ROOT / "research" / "backtests" / "2026-09-19_pooled-device-vs-degross_C.csv"
    df.merge(dev[["panel","family","rung","se_book","t_book"]], on=["panel","family","rung"], how="left").to_csv(out, index=False)
    print("grid written to", out.name)
    return df, wfdf

if __name__ == "__main__":
    main()
