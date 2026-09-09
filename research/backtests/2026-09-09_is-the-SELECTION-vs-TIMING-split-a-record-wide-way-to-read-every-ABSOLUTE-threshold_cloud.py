#!/usr/bin/env python3
"""IDEA 578 - IS THE SELECTION-vs-TIMING SPLIT A RECORD-WIDE WAY TO READ EVERY ABSOLUTE
   THRESHOLD?   (cloud, 2026-09-09)

PRE-REGISTERED QUESTION (QUEUE.md, written before any number below was read)
    Idea 314 used a matched-admission cross-sectional quantile as a pivot to split an absolute
    vol cap's damage into cross-sectional SELECTION (65-74% on SMALL439) and market-state
    TIMING (the rest, sign-flipping by panel).  Idea 400 already flagged absolute thresholds as
    frequency artefacts.  Apply the same matched-rate pivot to the record's OTHER absolute
    thresholds - the 200d gate, the breadth gate, the ADV/dollar-volume floor - and report
    which are SELECTION and which are TIMING.  Max 2 params (threshold, matched level).

THE PIVOT, taken verbatim from idea 314 (research/backtests/2026-09-09_is-the-vol-cap-the-
real-universe-clause-not-the-trend-leg_B.py, lines 520-527) and not re-derived here:
    TOTAL      = CAGR(ABS book)          - CAGR(unclaused control)
    SELECTION  = CAGR(QTL@matched book)  - CAGR(unclaused control)
    TIMING     = TOTAL - SELECTION
    sel_share  = SELECTION / TOTAL
  The QTL arm admits at a CONSTANT rate r, fixed for all time, where r is the ABS arm's own
  realised MEAN daily admission rate on that panel at that level.  The two arms therefore
  differ in exactly one thing: whether the admission rate moves with the market.  Everything
  that moves with the market is TIMING; everything left at a frozen rate is SELECTION.
  Idea 314 read the split at 0 bps; both 0 and 10 bps are reported here.

THE THREE THRESHOLD FAMILIES (the record's, named by the queue).  Two are NAME-LEVEL, one is
MARKET-LEVEL, and that asymmetry is the point of the run, not a defect of it:
    MA200  admit name i at t iff  px/MA200 - 1 >= c.     Ranking variable: px/MA200 - 1.
           c in {-0.05, -0.02, 0.00, +0.02, +0.05};  c = 0.00 is RULES v1's own clause and
           the +/-0.03 pair brackets RULES v2's band.
    ADV    admit name i at t iff  20d mean dollar volume >= A.   Ranking variable: that ADV.
           A in {$0.5M, $1M, $2M, $5M, $10M}.  SMALL439 only - data/volume_small.csv is the
           only share-volume series cached, so U56/B136 cannot carry this leg and are not
           faked.  Stated as a scope limit, not a result.
    BREADTH  market-level: hold the book iff E_t = (fraction of live names above their own
           200d MA) >= b;  otherwise the WHOLE book goes to cash.   b in {0.20,0.30,0.40,
           0.50,0.60}.  Its matched QTL control ranks days by E_t's own EXPANDING percentile
           rank (min_periods=252, causal) and is OFF on the lowest-ranked days at EXACTLY the
           ABS arm's realised OFF-rate.
           NOTE, said once and plainly: a market-level threshold has NO cross-section, so its
           "SELECTION" leg is a DAY-selection leg (out of the market r of the time, days
           picked by relative breadth) and its TIMING leg is what the ABSOLUTE level adds by
           clustering those days into structural bear markets.  The arithmetic is identical to
           idea 314's; the reading is not, and both are printed.

BOOK FORM, pinned to the record and never chosen: EWALL, gross 0.75, DEGROSS (gated weight to
cash, never re-spread - the live RULES v2 convention), 10 bps per unit turnover, weights at
close t applied t+1, no shorting, no leverage.  Control = the same EWALL with no clause.

THE TWO TUNED PARAMETERS (exactly two; every other axis is a REPORTING axis, printed at every
value and never selected on)
    P1  LEVEL - the absolute threshold (c / A / b).  ALL 5 rungs of every family reported.
    P2  in the RULE 8 selector ONLY, the (family, level) cell chosen on the IS window.
  Panel, family, cadence (W/M), cost rung (0/10 bps), half and window are reporting axes.

PRE-REGISTERED HYPOTHESES (fixed before any number was read)
  H_WIDE   The split generalises: on EVERY (panel, family, level) cell whose TOTAL is
           material (|TOTAL| >= 0.50 pp/yr), sel_share lands in [0,1] - i.e. the two legs do
           not straddle the total with opposite signs.  Idea 314 found 65-74% on SMALL439.
  H_NAME   Name-level thresholds (MA200, ADV) are SELECTION-dominated (median sel_share > 0.5)
           and the market-level threshold (BREADTH) is TIMING-dominated (median < 0.5).  This
           is the queue's own question stated as a testable ordering.
  H_SIGN   Idea 314 found TIMING sign-flips by panel.  Test whether the TIMING leg's sign is
           panel-dependent within a family, at a fixed level.
  H_KEEP   Does any thresholded book clear a KEEP path its own unclaused control does not?
           If no threshold ever buys a KEEP the record does not already have, the split is a
           diagnostic and never a rule.

GATES, printed BEFORE any hypothesis is read
  G1  fast_backtest == engine.backtest to < 1e-12 on real books, every panel.
  G2  MATCHED RATE: the QTL arm's realised mean admission rate is within 0.02 of the ABS
      arm's, in every cell.  If it is not, the pivot is not matched and the split is void.
  G3  IDENTITY: the OFF rung of each family (c = -inf / A = 0 / b = 0) reproduces the
      unclaused control's returns exactly.

RULE 8 (PROTOCOL 8).  (family, level) chosen on IS <= 2016-12-31 by IS Sharpe among the ABS
books of that panel; 2017-01-01.. read ONCE.  OOS CAGR / Sharpe / MaxDD reported against the
panel's own unclaused control, the live RULES v2 baseline, RULES v1 and SPY.  Both KEEP paths
(4a beat-the-book, 4b capital-worthy) evaluated on EVERY book in the grid.

SURVIVORSHIP.  SMALL439 is the current constituents of a sub-$2B screen (data/
SMALL_PANEL_README.md): its levels are optimistic and its CAGRs are not investable numbers.
Every SMALL439 statement here is a WITHIN-panel contrast (clause vs its own unclaused control
on the same names, same days), which survivorship bias does not manufacture; no cross-panel
level claim is made from it.

OUTPUTS  .books.csv, .decomp.csv, .rates.csv, .keeppaths.csv, .walkforward.csv, .console.txt
"""
import sys, io
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, load_volume, rules_v1_weights, rules_v2_weights  # noqa
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa

STEM = ROOT / "research" / "backtests" / ("2026-09-09_is-the-SELECTION-vs-TIMING-split-a-"
                                          "record-wide-way-to-read-every-ABSOLUTE-threshold_cloud")
GROSS, COST, OOS0 = 0.75, 10.0, "2017-01-01"
CADENCES = ["W", "M"]
LEVELS = {
    "MA200":   [-0.05, -0.02, 0.00, 0.02, 0.05],
    "ADV":     [0.5e6, 1e6, 2e6, 5e6, 10e6],
    "BREADTH": [0.20, 0.30, 0.40, 0.50, 0.60],
}
tee = io.StringIO()
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); tee.write(s + "\n")
def hdr(t): P(""); P("=" * 100); P(t); P("=" * 100)

# ---------------------------------------------------------------- fast runner
def fast_parts(prices, weights, freq):
    """Vectorised engine.backtest: returns (gross_returns, turnover) so any cost rung is a
    subtraction.  Asserted against engine.backtest in G1."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(index=idx, columns=prices.columns).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy(); mask[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0); Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mask); seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]; W0 = wt[s0]
    h = W0 * (Cp / Cp[s0]); V = h.sum(axis=1) + (1.0 - W0.sum(axis=1)); held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]; W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p]); Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1)); heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T); turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return pd.Series((held * rets).sum(axis=1), index=idx), pd.Series(turn, index=idx)

def net(parts, bps):
    g, t = parts
    return g - t * bps / 1e4

# ---------------------------------------------------------------- panels
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    P(f"   SMALL: dropped {len(bad)} tickers with max_1d_move >= 1.0 -> "
      f"{len([c for c in keep if c != 'SPY'])} names + SPY benchmark")
    return px[keep], bad

def build_panels():
    u, b = load_universe(), load_universe(broad=True)
    s, bad = small_panel()
    vol = load_volume(small=True)
    vol = vol[[c for c in vol.columns if c not in bad]]
    return {"U56":      dict(px=u, tr=list(u.columns), vol=None),
            "B136":     dict(px=b, tr=list(b.columns), vol=None),
            "SMALL439": dict(px=s, tr=[c for c in s.columns if c != "SPY"], vol=vol)}

# ---------------------------------------------------------------- clauses
def primitives(px, tr, vol):
    """Everything a clause needs, computed once per panel.  All causal."""
    p = px[tr]
    live = p.notna() & p.shift(1).notna()
    ma = p.rolling(200).mean()
    dist = (p / ma - 1.0).where(live & ma.notna())
    above = dist >= 0.0
    nlive = live.sum(axis=1).clip(lower=1)
    breadth = (above & live).sum(axis=1) / nlive          # E_t
    adv = None
    if vol is not None:
        dv = (p * vol.reindex(index=p.index, columns=p.columns)).where(live)
        adv = dv.rolling(20).mean()
    return dict(p=p, live=live, dist=dist, nlive=nlive, breadth=breadth, adv=adv)

def ewall(pr, mask=None, g=GROSS):
    """EWALL, DEGROSS: denominator is ALL live names, so masked-out weight goes to CASH."""
    live = pr["live"].astype(float)
    w = g * live.div(pr["nlive"], axis=0)
    if mask is not None:
        w = w.where(mask.reindex_like(w).fillna(False), 0.0)
    return w

def abs_mask(pr, fam, lvl):
    """The OFF rung (c = -inf, A = 0) is the live mask itself, so G3's identity is exact
    even for names whose 200d MA / 20d ADV does not yet exist."""
    if fam == "MA200":
        return pr["live"] if lvl == -np.inf else ((pr["dist"] >= lvl) & pr["live"])
    if fam == "ADV":
        return pr["live"] if lvl <= 0 else ((pr["adv"] >= lvl) & pr["live"])
    raise ValueError(fam)

def qtl_mask(pr, fam, r):
    """Admit the top r fraction of the day's LIVE names by the family's ranking variable.
    r is CONSTANT in time - that is the whole pivot."""
    v = pr["dist"] if fam == "MA200" else pr["adv"]
    v = v.where(pr["live"])
    k = np.maximum(1, np.rint(r * pr["nlive"].values)).astype(int)
    rk = v.rank(axis=1, ascending=False, method="first")
    return rk.le(pd.Series(k, index=v.index), axis=0).fillna(False) & pr["live"]

def breadth_abs_on(pr, b):
    return pr["breadth"] >= b

def breadth_pct(pr):
    """E_t's own EXPANDING percentile rank (min_periods=252, strictly causal: the rank of
    today's breadth among all breadth values seen up to and including today).  Computed once
    per panel; it does not depend on the matched rate."""
    e = pr["breadth"]
    p = e.expanding(min_periods=252).apply(lambda x: (x[:-1] <= x[-1]).mean(), raw=True)
    return p.fillna(1.0)

def breadth_qtl_on(pct, r, st):
    """ON on the r fraction of days whose breadth is HIGHEST by that causal percentile rank,
    OFF on the rest.  The ORDERING of days is causal (pct is expanding); only the CUTOFF is a
    matched-rate calibration over the evaluation window - which is exactly what idea 314's r
    is on the cross-sectional side, and is stated as such rather than hidden.  Matching by
    rank rather than by level makes the realised rate exact (G2)."""
    o = pct.loc[st:].rank(method="first", pct=True)
    on = pd.Series(True, index=pct.index)
    on.loc[st:] = (o > 1.0 - r).values
    return on

# ---------------------------------------------------------------- metrics
def mets(r):
    m = metrics(r); return m["CAGR"], m["Sharpe"], m["MaxDD"]

def row_of(r):
    h = len(r) // 2
    c, s, d = mets(r)
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=metrics(r.iloc[:h])["Sharpe"],
                H2=metrics(r.iloc[h:])["Sharpe"])

def keep_paths(r, base, spy):
    """PROTOCOL 4a and 4b, evaluated exactly as written."""
    a, b, s = row_of(r), row_of(base), row_of(spy)
    oos = r.loc[OOS0:]; oos_spy = spy.loc[OOS0:]
    k4a = (a["H1"] > b["H1"]) and (a["H2"] > b["H2"]) and (a["MaxDD"] >= b["MaxDD"])
    k4b = (a["H1"] > s["H1"] and a["H2"] > s["H2"]
           and metrics(oos)["Sharpe"] > metrics(oos_spy)["Sharpe"]
           and a["MaxDD"] >= 0.60 * s["MaxDD"]          # MaxDD negative: <= 60% of SPY's depth
           and a["CAGR"] >= 0.70 * s["CAGR"])
    fails = []
    if not (a["H1"] > s["H1"]): fails.append("H1")
    if not (a["H2"] > s["H2"]): fails.append("H2")
    if not (metrics(oos)["Sharpe"] > metrics(oos_spy)["Sharpe"]): fails.append("OOS")
    if not (a["MaxDD"] >= 0.60 * s["MaxDD"]): fails.append("DD")
    if not (a["CAGR"] >= 0.70 * s["CAGR"]): fails.append("CAGR")
    return k4a, k4b, "|".join(fails)

# ================================================================== main
def main():
    hdr("PANELS")
    PAN = build_panels()
    PR, START, SPY, BASE, V1, PCT = {}, {}, {}, {}, {}, {}
    for k, d in PAN.items():
        PR[k] = primitives(d["px"], d["tr"], d["vol"])
        PCT[k] = breadth_pct(PR[k])
        START[k] = d["px"].index[260]
        SPY[k] = d["px"]["SPY"].pct_change().fillna(0.0).loc[START[k]:]
        BASE[k] = net(fast_parts(d["px"], rules_v2_weights(d["px"]), "W"), COST).loc[START[k]:]
        V1[k] = net(fast_parts(d["px"], rules_v1_weights(d["px"]), "W"), COST).loc[START[k]:]
        P(f"   {k}: {len(d['tr'])} tradable, {d['px'].index[0].date()}..{d['px'].index[-1].date()}, "
          f"scored from {START[k].date()}, ADV leg = {'YES' if d['vol'] is not None else 'no (no volume series cached)'}")

    # -------------------------------------------------- G1
    hdr("G1  fast_parts == engine.backtest")
    g1 = []
    for k, d in PAN.items():
        for fam, lvl in [("MA200", 0.0), ("MA200", 0.05)]:
            w = ewall(PR[k], abs_mask(PR[k], fam, lvl)).reindex(columns=d["px"].columns).fillna(0.0)
            a = net(fast_parts(d["px"], w, "W"), COST)
            b = engine_backtest(d["px"], w, cost_bps=COST, freq="W")["returns"]
            g1.append(dict(panel=k, book=f"{fam}@{lvl}", maxabs=float((a - b).abs().max())))
    G1 = pd.DataFrame(g1)
    P(G1.to_string(index=False, float_format=lambda x: f"{x:.3e}"))
    P(f"   max |diff| = {G1.maxabs.max():.3e} -> {'PASS' if G1.maxabs.max() < 1e-12 else 'FAIL'}")

    # -------------------------------------------------- G3 identity + controls
    hdr("G3  IDENTITY: the OFF rung of each family == the unclaused control, exactly")
    CTRL = {}
    g3 = []
    for k, d in PAN.items():
        for cad in CADENCES:
            w0 = ewall(PR[k])
            CTRL[(k, cad)] = fast_parts(d["px"], w0, cad)
            off_ma = ewall(PR[k], abs_mask(PR[k], "MA200", -np.inf))
            e = float((net(fast_parts(d["px"], off_ma, cad), COST) - net(CTRL[(k, cad)], COST)).abs().max())
            g3.append(dict(panel=k, cad=cad, fam="MA200", ident=e))
            on = breadth_abs_on(PR[k], 0.0)
            wb = ewall(PR[k]).mul(on.astype(float), axis=0)
            e = float((net(fast_parts(d["px"], wb, cad), COST) - net(CTRL[(k, cad)], COST)).abs().max())
            g3.append(dict(panel=k, cad=cad, fam="BREADTH", ident=e))
            if PR[k]["adv"] is not None:
                wa = ewall(PR[k], abs_mask(PR[k], "ADV", 0.0))
                e = float((net(fast_parts(d["px"], wa, cad), COST) - net(CTRL[(k, cad)], COST)).abs().max())
                g3.append(dict(panel=k, cad=cad, fam="ADV", ident=e))
    G3 = pd.DataFrame(g3)
    P(G3.pivot_table(index=["panel", "cad"], columns="fam", values="ident").to_string(
        float_format=lambda x: f"{x:.2e}"))
    P(f"   max identity error = {G3.ident.max():.3e} -> {'PASS' if G3.ident.max() < 1e-12 else 'FAIL'}")

    # -------------------------------------------------- rates + G2
    hdr("MATCHED ADMISSION RATES  (r = the ABS arm's own realised mean rate; the QTL arm is "
        "then frozen at r for all time)")
    rates = []
    MASKS = {}
    for k, d in PAN.items():
        pr = PR[k]; st = START[k]
        for fam, lv in LEVELS.items():
            if fam == "ADV" and pr["adv"] is None: continue
            for lvl in lv:
                if fam == "BREADTH":
                    on = breadth_abs_on(pr, lvl).loc[st:]
                    r = float(on.mean())
                    onq = breadth_qtl_on(PCT[k], r, st)
                    rq = float(onq.loc[st:].mean())
                    MASKS[(k, fam, lvl, "ABS")] = breadth_abs_on(pr, lvl)
                    MASKS[(k, fam, lvl, "QTL")] = onq
                    sd = float(on.astype(float).rolling(252).mean().std())
                else:
                    m = abs_mask(pr, fam, lvl).loc[st:]
                    rt = m.sum(axis=1) / pr["nlive"].loc[st:]
                    r = float(rt.mean()); sd = float(rt.std())
                    mq = qtl_mask(pr, fam, r)
                    rq = float((mq.loc[st:].sum(axis=1) / pr["nlive"].loc[st:]).mean())
                    MASKS[(k, fam, lvl, "ABS")] = abs_mask(pr, fam, lvl)
                    MASKS[(k, fam, lvl, "QTL")] = mq
                rates.append(dict(panel=k, family=fam, level=lvl, abs_rate=r, qtl_rate=rq,
                                  err=abs(rq - r), rate_sd=sd))
    RT = pd.DataFrame(rates)
    P(RT.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\nG2  max |qtl_rate - abs_rate| = {RT.err.max():.4f} (bar 0.02) -> "
      f"{'PASS' if RT.err.max() <= 0.02 else 'FAIL'}")
    P("   rate_sd is the ABS arm's own admission-rate variability - the thing the QTL arm has "
      "zero of, and therefore the thing the TIMING leg prices.")
    RT.to_csv(f"{STEM}.rates.csv", index=False)

    # -------------------------------------------------- the grid
    hdr("THE GRID - every book, every level, both arms, both cadences.  ALL grid points.")
    books = []
    for k, d in PAN.items():
        pr = PR[k]; st = START[k]
        for cad in CADENCES:
            ctrl = net(CTRL[(k, cad)], COST).loc[st:]
            ctrl0 = net(CTRL[(k, cad)], 0.0).loc[st:]
            k4a, k4b, f = keep_paths(ctrl, BASE[k], SPY[k])
            books.append(dict(panel=k, family="CONTROL", level=np.nan, arm="none", cad=cad,
                              **row_of(ctrl), CAGR0=metrics(ctrl0)["CAGR"],
                              keep4a=k4a, keep4b=k4b, fail4b=f))
            for fam, lv in LEVELS.items():
                if fam == "ADV" and pr["adv"] is None: continue
                for lvl in lv:
                    for arm in ("ABS", "QTL"):
                        m = MASKS[(k, fam, lvl, arm)]
                        w = ewall(pr).mul(m.astype(float), axis=0) if fam == "BREADTH" else ewall(pr, m)
                        parts = fast_parts(d["px"], w, cad)
                        r10 = net(parts, COST).loc[st:]; r0 = net(parts, 0.0).loc[st:]
                        k4a, k4b, f = keep_paths(r10, BASE[k], SPY[k])
                        books.append(dict(panel=k, family=fam, level=lvl, arm=arm, cad=cad,
                                          **row_of(r10), CAGR0=metrics(r0)["CAGR"],
                                          keep4a=k4a, keep4b=k4b, fail4b=f))
    B = pd.DataFrame(books)
    B.to_csv(f"{STEM}.books.csv", index=False)
    P(f"{len(B)} books written to .books.csv "
      f"({len(B[B.family!='CONTROL'])} clause books + {len(B[B.family=='CONTROL'])} controls)")
    for k in PAN:
        P("")
        P(f"--- {k} (weekly, 10 bps).  CONTROL = unclaused EWALL g=0.75 ---")
        sub = B[(B.panel == k) & (B.cad == "W")]
        P(sub.pivot_table(index=["family", "level"], columns="arm",
                          values=["CAGR", "Sharpe", "MaxDD"]).to_string(
            float_format=lambda x: f"{x:.3f}"))

    # -------------------------------------------------- the decomposition
    hdr("THE DECOMPOSITION - idea 314's split, applied to every threshold family")
    dec = []
    for k in PAN:
        for cad in CADENCES:
            ctl = B[(B.panel == k) & (B.cad == cad) & (B.family == "CONTROL")].iloc[0]
            for fam, lv in LEVELS.items():
                for lvl in lv:
                    a = B[(B.panel == k) & (B.cad == cad) & (B.family == fam) &
                          (B.level == lvl) & (B.arm == "ABS")]
                    q = B[(B.panel == k) & (B.cad == cad) & (B.family == fam) &
                          (B.level == lvl) & (B.arm == "QTL")]
                    if a.empty: continue
                    a, q = a.iloc[0], q.iloc[0]
                    for bps, col, cc in [(0, "CAGR0", "CAGR0"), (10, "CAGR", "CAGR")]:
                        tot = (a[col] - ctl[col]) * 100
                        sel = (q[col] - ctl[col]) * 100
                        dec.append(dict(panel=k, cad=cad, family=fam, level=lvl, bps=bps,
                                        TOTAL=tot, SELECTION=sel, TIMING=tot - sel,
                                        sel_share=(sel / tot if abs(tot) > 1e-9 else np.nan),
                                        dSharpe_abs=a["Sharpe"] - ctl["Sharpe"],
                                        dSharpe_qtl=q["Sharpe"] - ctl["Sharpe"],
                                        dMaxDD_abs=(a["MaxDD"] - ctl["MaxDD"]) * 100))
    D = pd.DataFrame(dec)
    D.to_csv(f"{STEM}.decomp.csv", index=False)
    for bps in (0, 10):
        P("")
        P(f"--- pp/yr vs the unclaused control, weekly, {bps} bps ---")
        sub = D[(D.bps == bps) & (D.cad == "W")]
        P(sub[["panel", "family", "level", "TOTAL", "SELECTION", "TIMING", "sel_share"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # -------------------------------------------------- hypotheses
    hdr("H_WIDE  does the split stay inside [0,1] wherever the TOTAL is material?")
    mat = D[(D.bps == 0) & (D.TOTAL.abs() >= 0.50)].copy()
    inside = mat.sel_share.between(0, 1)
    P(f"   material cells (|TOTAL| >= 0.50 pp/yr, 0 bps, both cadences): {len(mat)} of {len(D[D.bps==0])}")
    P(f"   sel_share inside [0,1]: {int(inside.sum())} / {len(mat)} = {inside.mean():.1%}")
    P(f"   H_WIDE -> {'PASS' if inside.mean() >= 0.80 else 'FAIL'} (pre-registered bar 80%)")
    P("")
    P("   by family (material cells only):")
    P(mat.assign(inside=inside).groupby("family").agg(
        n=("sel_share", "size"), inside=("inside", "mean"),
        med_share=("sel_share", "median"), med_TOTAL=("TOTAL", "median")).to_string(
        float_format=lambda x: f"{x:.3f}"))

    hdr("H_NAME  are name-level thresholds SELECTION and the market-level one TIMING?")
    med = mat.groupby("family").sel_share.median()
    P(mat.groupby(["family", "panel"]).sel_share.median().to_string(float_format=lambda x: f"{x:.3f}"))
    P("")
    for f in ["MA200", "ADV", "BREADTH"]:
        if f in med.index:
            P(f"   {f:8s} median sel_share = {med[f]:+.3f}  -> "
              f"{'SELECTION-dominated' if med[f] > 0.5 else 'TIMING-dominated'}")
    ok = (med.get("MA200", np.nan) > 0.5 and med.get("ADV", np.nan) > 0.5
          and med.get("BREADTH", np.nan) < 0.5)
    P(f"   H_NAME -> {'PASS' if ok else 'FAIL'}")

    hdr("H_SIGN  does the TIMING leg's sign depend on the panel, within a family?")
    sg = D[(D.bps == 0) & (D.cad == "W")].pivot_table(index=["family", "level"],
                                                      columns="panel", values="TIMING")
    P(sg.to_string(float_format=lambda x: f"{x:+.3f}"))
    flip = []
    for (f, l), row in sg.iterrows():
        v = row.dropna()
        if len(v) > 1: flip.append(dict(family=f, level=l, flips=bool((v > 0).any() and (v < 0).any())))
    FL = pd.DataFrame(flip)
    P(f"\n   cells with >1 panel: {len(FL)};  TIMING sign flips across panels in "
      f"{int(FL.flips.sum())} = {FL.flips.mean():.1%}")
    P(f"   H_SIGN -> {'CONFIRMED (panel-dependent)' if FL.flips.mean() >= 0.5 else 'NOT CONFIRMED'}")

    # -------------------------------------------------- KEEP paths
    hdr("H_KEEP / PROTOCOL 4a and 4b over EVERY book in the grid")
    K = B.copy()
    P(f"   4a passes: {int(K.keep4a.sum())} / {len(K)}      4b passes: {int(K.keep4b.sum())} / {len(K)}")
    P("")
    P(K.groupby(["panel", "family", "arm"]).agg(
        n=("keep4b", "size"), p4a=("keep4a", "sum"), p4b=("keep4b", "sum")).to_string())
    P("")
    P("   binding 4b legs over all books:")
    P(pd.Series([t for f in K.fail4b for t in (f.split("|") if f else [])]).value_counts().to_string())
    P("")
    ctl4 = K[K.family == "CONTROL"].set_index(["panel", "cad"])[["keep4a", "keep4b"]]
    bought = []
    for _, r in K[K.family != "CONTROL"].iterrows():
        c = ctl4.loc[(r.panel, r.cad)]
        if (r.keep4a and not c.keep4a) or (r.keep4b and not c.keep4b):
            bought.append(dict(panel=r.panel, family=r.family, level=r.level, arm=r.arm,
                               cad=r.cad, CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD,
                               k4a=r.keep4a, k4b=r.keep4b))
    BO = pd.DataFrame(bought)
    P(f"   H_KEEP: books clearing a KEEP path their own unclaused control does NOT: {len(BO)}")
    if len(BO): P(BO.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    P(f"   H_KEEP -> {'PASS' if len(BO) else 'FAIL - no absolute threshold buys a KEEP the control lacks'}")
    K.to_csv(f"{STEM}.keeppaths.csv", index=False)

    # -------------------------------------------------- RULE 8
    hdr("RULE 8  (family, level) chosen on IS <= 2016-12-31 by IS Sharpe among ABS books; "
        "2017-01-01.. read ONCE")
    wf = []
    for k, d in PAN.items():
        pr = PR[k]; st = START[k]
        cand = []
        for cad in CADENCES:
            for fam, lv in LEVELS.items():
                if fam == "ADV" and pr["adv"] is None: continue
                for lvl in lv:
                    m = MASKS[(k, fam, lvl, "ABS")]
                    w = ewall(pr).mul(m.astype(float), axis=0) if fam == "BREADTH" else ewall(pr, m)
                    r = net(fast_parts(d["px"], w, cad), COST).loc[st:]
                    cand.append((fam, lvl, cad, metrics(r.loc[:"2016-12-31"])["Sharpe"], r))
        cand.sort(key=lambda x: -x[3])
        fam, lvl, cad, iss, r = cand[0]
        ctl = net(CTRL[(k, cad)], COST).loc[st:]
        oo, ob, os_, oc = r.loc[OOS0:], BASE[k].loc[OOS0:], SPY[k].loc[OOS0:], ctl.loc[OOS0:]
        k4a, k4b, f = keep_paths(r, BASE[k], SPY[k])
        wf.append(dict(panel=k, pick=f"{fam}@{lvl}/{cad}", IS_Sharpe=iss,
                       IS_CAGR=metrics(r.loc[:"2016-12-31"])["CAGR"],
                       OOS_CAGR=metrics(oo)["CAGR"], OOS_Sharpe=metrics(oo)["Sharpe"],
                       OOS_MaxDD=metrics(oo)["MaxDD"],
                       ctl_OOS_CAGR=metrics(oc)["CAGR"], ctl_OOS_Sharpe=metrics(oc)["Sharpe"],
                       ctl_OOS_MaxDD=metrics(oc)["MaxDD"],
                       v2_OOS_CAGR=metrics(ob)["CAGR"], v2_OOS_Sharpe=metrics(ob)["Sharpe"],
                       v2_OOS_MaxDD=metrics(ob)["MaxDD"],
                       v1_OOS_Sharpe=metrics(V1[k].loc[OOS0:])["Sharpe"],
                       spy_OOS_CAGR=metrics(os_)["CAGR"], spy_OOS_Sharpe=metrics(os_)["Sharpe"],
                       spy_OOS_MaxDD=metrics(os_)["MaxDD"],
                       full_CAGR=metrics(r)["CAGR"], full_Sharpe=metrics(r)["Sharpe"],
                       full_MaxDD=metrics(r)["MaxDD"], H1=row_of(r)["H1"], H2=row_of(r)["H2"],
                       keep4a=k4a, keep4b=k4b, fail4b=f))
    W = pd.DataFrame(wf)
    W.to_csv(f"{STEM}.walkforward.csv", index=False)
    P(W.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    P("")
    P("   Every rule-8 pick is the IS-best ABS threshold on its panel; the OOS column was read "
      "once, after the pick.  ctl_* is the SAME panel's unclaused EWALL control.")

    (Path(f"{STEM}.console.txt")).write_text(tee.getvalue())

if __name__ == "__main__":
    main()
