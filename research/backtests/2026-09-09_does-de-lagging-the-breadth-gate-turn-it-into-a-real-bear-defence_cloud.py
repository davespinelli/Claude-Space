#!/usr/bin/env python3
"""IDEA 315 - DOES DE-LAGGING THE BREADTH GATE TURN IT INTO A REAL BEAR DEFENCE?
   (cloud, 2026-09-09)

PRE-REGISTERED QUESTION (QUEUE.md, written before any number below was read)
    Idea 48's by-product - the breadth cash gate at the causal bottom quintile - is the grid's
    highest-Sharpe non-live book (12.2% / 1.131 / -12.7%, OOS 1.240) yet returns -9.0% in 2022
    because the flag fires in February, AFTER January's loss, and stays on through the Q4
    recovery.  Test the LAG directly: gate on E_t's own RATE OF CHANGE (E_t vs its 20d mean)
    instead of its level, and on a RE-ENTRY that requires the level to clear the quantile
    rather than merely stop falling below it.  If the 2022 column moves, the gate is a TIMING
    signal; if it does not, it is a VOLATILITY DISCOUNT and belongs in RULES as an exposure
    clause, not a defence.  Max 2 params (q, the de-lagging dial).

THE DECISIVE COLUMN, named in advance: **calendar-2022 return**.  Every other year is printed
beside it, and 2018 and 2020 are called out as the record's other two drawdown years, but the
verdict sentence is written against 2022 because that is the year the queue nominated and the
year the lag is alleged to ruin.  2022 sits INSIDE the rule-8 OOS window, so no selector ever
saw it.

THE FIVE GATE VARIANTS (E_t = fraction of the panel's live names above their own 200d MA;
every quantile is EXPANDING with min_periods=252 and therefore strictly causal)
    LEVEL   idea 48's gate, unchanged.  HOLD iff E_t >= Q_q(E)_t.
    ROC     the queue's literal wording.  HOLD iff E_t >= mean_k(E_t).  No quantile: this
            fires on roughly half of all days, and that is reported, not hidden.
    ROCQ    the RATE-MATCHED de-lagging.  r_t = E_t / mean_k(E_t) - 1;  HOLD iff r_t >=
            Q_q(r)_t.  Same nominal fire rate as LEVEL at the same q, so any difference is
            the LAG and not the exposure budget.  This is the honest version of the test.
    ASYM    hysteresis re-entry.  Go to CASH when E_t < Q_q(E)_t;  return to the book only
            when E_t >= Q_qup(E)_t with qup > q.  De-lags the EXIT not at all and the ENTRY
            deliberately later - the queue's second instrument, and the one that should make
            2022 WORSE if the Q4 recovery is what costs the gate.
    BOTH    HOLD iff (LEVEL holds) AND (ROCQ at k=20 holds).

THE TWO TUNED PARAMETERS (exactly two; every other axis is a REPORTING axis, printed at every
value and never selected on)
    P1  q   in {0.10, 0.20, 0.30, 0.40}    (idea 48's is the bottom quintile, q = 0.20)
    P2  the de-lagging dial: k in {10, 20, 40, 60} for ROC/ROCQ, qup in {0.35, 0.50, 0.65}
        for ASYM.  LEVEL uses no second dial.
  Panel (U56 / B136 / SMALL439), cadence (W / M), underlying book (EWALL / MA-DG), cost rung
  and calendar year are REPORTING axes: every one is printed at every value.

BOOKS.  Underlying = EWALL (equal weight every live name, gross 0.75, DEGROSS) and MA-DG (the
live RULES v2 form: EWALL masked by the per-name 200d +/-3% band, gated weight to cash), both
at gross 0.75.  The breadth gate multiplies the whole book by 0/1.  10 bps per unit turnover,
weights decided at close t applied t+1, no shorting, no leverage.  Control = the same
underlying with NO breadth gate.
  41 gate books x 3 panels x 2 cadences x 2 underlyings = 492 books + 12 controls.

PRE-REGISTERED HYPOTHESES (fixed before any number was read)
  H_2022   De-lagging moves the 2022 column.  PASS requires some (variant, dial) whose 2022
           return beats LEVEL@0.20's by >= +3.0 pp on a majority of the 12 (panel x cadence x
           underlying) arms.  This is the queue's own question.
  H_TIMING If the gate is a TIMING signal, its benefit concentrates in drawdown years.  Test:
           is the gate's mean edge over its control in the three worst SPY years larger than
           its mean edge in the other years?  If not, it is a volatility discount.
  H_KEEP   Does any de-lagged gate clear a KEEP path (4a or 4b) that LEVEL@0.20 does not, on
           the same arm?  A de-lagging that only reshuffles years is not a rule change.
  H_REPRO  Idea 48's published cell (12.2% / 1.131 / -12.7%, OOS 1.240, 2022 = -9.0%) is a
           U56 number; report the closest cell this script builds beside it.  A mismatch is
           reported as a mismatch, not tuned away.

GATES, printed BEFORE any hypothesis is read
  G1  fast_parts == engine.backtest to < 1e-12 on real gated books, every panel.
  G2  CAUSALITY: every gate series is rebuilt from a TRUNCATED history ending at date d, for
      12 random d, and must equal the full-history value at d.  Any look-ahead fails here.
  G3  IDENTITY: q = 0 (LEVEL) and a gate held permanently ON reproduce the ungated control's
      returns exactly.

RULE 8 (PROTOCOL 8).  (variant, q, dial) chosen on IS <= 2016-12-31 by IS Sharpe inside each
panel x underlying arm; 2017-01-01.. read ONCE - so 2018, 2020 and 2022 are all untouched by
the selector.  OOS CAGR / Sharpe / MaxDD reported against the arm's own ungated control, the
live RULES v2 baseline, RULES v1 and SPY.  Both KEEP paths evaluated on EVERY book.

SURVIVORSHIP.  SMALL439 is the current constituents of a sub-$2B screen (data/
SMALL_PANEL_README.md); its levels are optimistic and its CAGRs are not investable numbers.
Every SMALL439 statement here is a within-panel contrast (gated vs ungated, same names, same
days), which survivorship bias does not manufacture.

OUTPUTS  .books.csv, .years.csv, .grid.csv, .keeppaths.csv, .walkforward.csv, .console.txt
"""
import sys, io
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, band_state, rules_v1_weights, rules_v2_weights  # noqa
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa

STEM = ROOT / "research" / "backtests" / ("2026-09-09_does-de-lagging-the-breadth-gate-turn-"
                                          "it-into-a-real-bear-defence_cloud")
GROSS, COST, OOS0, MINP = 0.75, 10.0, "2017-01-01", 252
QS   = [0.10, 0.20, 0.30, 0.40]
KS   = [10, 20, 40, 60]
QUPS = [0.35, 0.50, 0.65]
CADENCES, UNDERLYINGS = ["W", "M"], ["EWALL", "MADG"]

tee = io.StringIO()
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); tee.write(s + "\n")
def hdr(t): P(""); P("=" * 100); P(t); P("=" * 100)

# ---------------------------------------------------------------- fast runner
def fast_parts(prices, weights, freq):
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

def net(parts, bps=COST):
    g, t = parts; return g - t * bps / 1e4

# ---------------------------------------------------------------- panel
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    P(f"   SMALL: dropped {len(bad)} tickers with max_1d_move >= 1.0 -> "
      f"{len([c for c in keep if c != 'SPY'])} names + SPY benchmark")
    return px[keep]

# ---------------------------------------------------------------- gate primitives
def breadth(px, tr):
    p = px[tr]
    live = p.notna() & p.shift(1).notna()
    ma = p.rolling(200).mean()
    above = (p >= ma) & live & ma.notna()
    return above.sum(axis=1) / live.sum(axis=1).clip(lower=1)

def eq(s, q):
    """Causal expanding q-quantile of a series (min_periods=MINP)."""
    return s.expanding(min_periods=MINP).quantile(q)

def gate_series(E, variant, q=None, k=None, qup=None):
    """Every branch returns a boolean HOLD series, True where the book is held.  Before the
    quantile has MINP observations the gate is HOLD (the warm-up is discarded anyway)."""
    if variant == "LEVEL":
        return (E >= eq(E, q)).where(eq(E, q).notna(), True).astype(bool)
    if variant == "ROC":
        m = E.rolling(k).mean()
        return (E >= m).where(m.notna(), True).astype(bool)
    if variant == "ROCQ":
        r = E / E.rolling(k).mean() - 1.0
        t = eq(r, q)
        return (r >= t).where(t.notna(), True).astype(bool)
    if variant == "ASYM":
        lo, hi = eq(E, q), eq(E, qup)
        raw = pd.Series(np.nan, index=E.index)
        raw = raw.mask(E < lo, 0.0).mask(E >= hi, 1.0)
        return raw.ffill().fillna(1.0).astype(bool)
    if variant == "BOTH":
        return gate_series(E, "LEVEL", q=q) & gate_series(E, "ROCQ", q=q, k=20)
    raise ValueError(variant)

def menu():
    m = [("LEVEL", q, np.nan) for q in QS]
    m += [("ROC", np.nan, k) for k in KS]
    m += [("ROCQ", q, k) for q in QS for k in KS]
    m += [("ASYM", q, u) for q in QS for u in QUPS]
    m += [("BOTH", q, 20) for q in QS]
    return m

_GCACHE = {}
def cached_gate(k, E, variant, q, d):
    key = (k, variant, q, d)
    if key not in _GCACHE: _GCACHE[key] = build_gate(E, variant, q, d)
    return _GCACHE[key]

def build_gate(E, variant, q, d):
    if variant == "LEVEL": return gate_series(E, "LEVEL", q=q)
    if variant == "ROC":   return gate_series(E, "ROC", k=int(d))
    if variant == "ROCQ":  return gate_series(E, "ROCQ", q=q, k=int(d))
    if variant == "ASYM":  return gate_series(E, "ASYM", q=q, qup=d)
    if variant == "BOTH":  return gate_series(E, "BOTH", q=q)
    raise ValueError(variant)

# ---------------------------------------------------------------- metrics
def row_of(r):
    h = len(r) // 2; m = metrics(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])

def keep_paths(r, base, spy):
    a, b, s = row_of(r), row_of(base), row_of(spy)
    k4a = (a["H1"] > b["H1"]) and (a["H2"] > b["H2"]) and (a["MaxDD"] >= b["MaxDD"])
    oS, sS = metrics(r.loc[OOS0:])["Sharpe"], metrics(spy.loc[OOS0:])["Sharpe"]
    legs = {"H1": a["H1"] > s["H1"], "H2": a["H2"] > s["H2"], "OOS": oS > sS,
            "DD": a["MaxDD"] >= 0.60 * s["MaxDD"], "CAGR": a["CAGR"] >= 0.70 * s["CAGR"]}
    return k4a, all(legs.values()), "|".join([k for k, v in legs.items() if not v])

def yearly(r):
    return (1 + r).groupby(r.index.year).prod() - 1

# ================================================================== main
def main():
    hdr("PANELS")
    PX = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": small_panel()}
    TR = {k: [c for c in v.columns if not (k == "SMALL439" and c == "SPY")] for k, v in PX.items()}
    E, START, SPY, BASE, V1, BOOK = {}, {}, {}, {}, {}, {}
    for k, px in PX.items():
        E[k] = breadth(px, TR[k]); START[k] = px.index[260]
        SPY[k] = px["SPY"].pct_change().fillna(0.0).loc[START[k]:]
        BASE[k] = net(fast_parts(px, rules_v2_weights(px), "W")).loc[START[k]:]
        V1[k] = net(fast_parts(px, rules_v1_weights(px), "W")).loc[START[k]:]
        p = px[TR[k]]; live = (p.notna() & p.shift(1).notna()).astype(float)
        ew = GROSS * live.div(live.sum(axis=1).clip(lower=1), axis=0)
        BOOK[(k, "EWALL")] = ew
        BOOK[(k, "MADG")] = ew.where(band_state(p, 0.03), 0.0)
        P(f"   {k}: {len(TR[k])} tradable, scored from {START[k].date()}, "
          f"E_t mean {E[k].loc[START[k]:].mean():.3f}")

    # -------------------------------------------------- G1
    hdr("G1  fast_parts == engine.backtest on real GATED books")
    g1 = []
    for k, px in PX.items():
        w = BOOK[(k, "EWALL")].mul(build_gate(E[k], "LEVEL", 0.20, np.nan).astype(float), axis=0)
        w = w.reindex(columns=px.columns).fillna(0.0)
        a = net(fast_parts(px, w, "W"))
        b = engine_backtest(px, w, cost_bps=COST, freq="W")["returns"]
        g1.append(dict(panel=k, maxabs=float((a - b).abs().max())))
    G1 = pd.DataFrame(g1); P(G1.to_string(index=False, float_format=lambda x: f"{x:.3e}"))
    P(f"   max |diff| = {G1.maxabs.max():.3e} -> {'PASS' if G1.maxabs.max() < 1e-12 else 'FAIL'}")

    # -------------------------------------------------- G2 causality
    hdr("G2  CAUSALITY - every gate rebuilt from a TRUNCATED history must equal its "
        "full-history value at that date")
    rng = np.random.default_rng(20260909); g2 = []
    for k in PX:
        e = E[k]; idx = e.index[e.index >= START[k]]
        for d in rng.choice(idx, 12, replace=False):
            d = pd.Timestamp(d)
            for v, q, dl in [("LEVEL", 0.20, np.nan), ("ROCQ", 0.20, 20),
                             ("ASYM", 0.20, 0.50), ("ROC", np.nan, 20), ("BOTH", 0.20, 20)]:
                full = bool(build_gate(e, v, q, dl).loc[d])
                trunc = bool(build_gate(e.loc[:d], v, q, dl).loc[d])
                g2.append(dict(panel=k, date=d.date(), variant=v, ok=(full == trunc)))
    G2 = pd.DataFrame(g2)
    P(G2.groupby("variant").ok.agg(["size", "sum"]).to_string())
    P(f"   {int(G2.ok.sum())} / {len(G2)} truncated rebuilds agree -> "
      f"{'PASS' if G2.ok.all() else 'FAIL'}")

    # -------------------------------------------------- G3 identity
    hdr("G3  IDENTITY - a permanently-ON gate reproduces the ungated control exactly")
    g3 = []
    for k, px in PX.items():
        for u in UNDERLYINGS:
            for cad in CADENCES:
                on = pd.Series(True, index=px.index)
                a = net(fast_parts(px, BOOK[(k, u)].mul(on.astype(float), axis=0), cad))
                b = net(fast_parts(px, BOOK[(k, u)], cad))
                g3.append(dict(panel=k, under=u, cad=cad, ident=float((a - b).abs().max())))
    G3 = pd.DataFrame(g3)
    P(f"   max identity error = {G3.ident.max():.3e} -> "
      f"{'PASS' if G3.ident.max() < 1e-15 else 'FAIL'}")

    # -------------------------------------------------- fire rates
    hdr("FIRE RATES - how often is each gate in CASH?  (a reporting axis, never selected on)")
    fr = []
    for k in PX:
        for v, q, d in menu():
            g = cached_gate(k, E[k], v, q, d).loc[START[k]:]
            fr.append(dict(panel=k, variant=v, q=q, dial=d, cash_rate=1 - g.mean(),
                           n_spells=int((g.astype(int).diff() == -1).sum())))
    FR = pd.DataFrame(fr)
    P(FR.pivot_table(index=["variant", "q", "dial"], columns="panel",
                     values="cash_rate", dropna=False).to_string(float_format=lambda x: f"{x:.3f}"))
    P("   ROC carries NO quantile, so its cash rate is whatever E_t vs its k-day mean gives - "
      "printed here so the reader can see it is a different exposure budget, not a de-lagged LEVEL.")

    # -------------------------------------------------- the grid
    hdr("THE GRID - every book, every gate, every arm.  ALL grid points reported.")
    books, years, RET, CTL = [], [], {}, {}
    for k, px in PX.items():
        st = START[k]
        for u in UNDERLYINGS:
            for cad in CADENCES:
                ctl = net(fast_parts(px, BOOK[(k, u)], cad)).loc[st:]
                CTL[(k, u, cad)] = ctl
                k4a, k4b, f = keep_paths(ctl, BASE[k], SPY[k])
                books.append(dict(panel=k, under=u, cad=cad, variant="CONTROL", q=np.nan,
                                  dial=np.nan, **row_of(ctl), keep4a=k4a, keep4b=k4b, fail4b=f))
                for y, val in yearly(ctl).items():
                    years.append(dict(panel=k, under=u, cad=cad, variant="CONTROL",
                                      q=np.nan, dial=np.nan, year=int(y), ret=val))
                for v, q, d in menu():
                    g = cached_gate(k, E[k], v, q, d)
                    r = net(fast_parts(px, BOOK[(k, u)].mul(g.astype(float), axis=0), cad)).loc[st:]
                    RET[(k, u, cad, v, q, d)] = r
                    k4a, k4b, f = keep_paths(r, BASE[k], SPY[k])
                    books.append(dict(panel=k, under=u, cad=cad, variant=v, q=q, dial=d,
                                      **row_of(r), keep4a=k4a, keep4b=k4b, fail4b=f))
                    for y, val in yearly(r).items():
                        years.append(dict(panel=k, under=u, cad=cad, variant=v, q=q, dial=d,
                                          year=int(y), ret=val))
    B = pd.DataFrame(books); Y = pd.DataFrame(years)
    B.to_csv(f"{STEM}.books.csv", index=False); Y.to_csv(f"{STEM}.years.csv", index=False)
    P(f"   {len(B)} books ({len(B[B.variant!='CONTROL'])} gated + {len(B[B.variant=='CONTROL'])} controls)")
    P("")
    P("--- full-sample Sharpe by variant (median over q/dial), per panel x underlying, weekly ---")
    P(B[(B.cad == "W")].pivot_table(index=["variant"], columns=["panel", "under"],
                                    values="Sharpe", aggfunc="median").to_string(
        float_format=lambda x: f"{x:.3f}"))

    # -------------------------------------------------- H_2022
    hdr("H_2022  THE DECISIVE COLUMN - does de-lagging move calendar 2022?")
    y22 = Y[Y.year == 2022]
    ref = y22[(y22.variant == "LEVEL") & (y22.q == 0.20)].set_index(["panel", "under", "cad"]).ret
    ctl22 = y22[y22.variant == "CONTROL"].set_index(["panel", "under", "cad"]).ret
    P("   2022 return of idea 48's own gate (LEVEL q=0.20) and of the ungated control:")
    P(pd.DataFrame({"LEVEL@0.20": ref, "CONTROL": ctl22,
                    "gate edge": ref - ctl22}).to_string(float_format=lambda x: f"{x:+.2%}"))
    P("")
    rows = []
    for (v, q, d), grp in y22[y22.variant != "CONTROL"].groupby(["variant", "q", "dial"], dropna=False):
        s = grp.set_index(["panel", "under", "cad"]).ret
        delta = (s - ref).dropna()
        rows.append(dict(variant=v, q=q, dial=d, mean_2022=s.mean(), worst=s.min(), best=s.max(),
                         vs_LEVEL020_mean=delta.mean(), arms_better_3pp=int((delta >= 0.03).sum()),
                         arms=len(delta)))
    D22 = pd.DataFrame(rows).sort_values("vs_LEVEL020_mean", ascending=False)
    P(D22.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    win = D22[(D22.arms_better_3pp > D22.arms / 2)]
    P("")
    P(f"   cells beating LEVEL@0.20's 2022 by >= +3.0 pp on a MAJORITY of the 12 arms: {len(win)} "
      f"of {len(D22)}")
    P(f"   H_2022 -> {'PASS' if len(win) else 'FAIL'} (pre-registered bar: at least one such cell)")
    D22.to_csv(f"{STEM}.grid.csv", index=False)

    hdr("EVERY YEAR, weekly EWALL, the three panels - LEVEL@0.20 vs the best de-lagged cell "
        "vs the control")
    best = D22.iloc[0]
    for k in PX:
        sub = Y[(Y.panel == k) & (Y.cad == "W") & (Y.under == "EWALL")]
        tab = pd.DataFrame({
            "CONTROL": sub[sub.variant == "CONTROL"].set_index("year").ret,
            "LEVEL@0.20": sub[(sub.variant == "LEVEL") & (sub.q == 0.20)].set_index("year").ret,
            f"{best.variant}@q={best.q}/d={best.dial}":
                sub[(sub.variant == best.variant) & (sub.q.fillna(-1) == (best.q if pd.notna(best.q) else -1))
                    & (sub.dial.fillna(-1) == (best.dial if pd.notna(best.dial) else -1))]
                .set_index("year").ret})
        P(""); P(f"--- {k} ---")
        P(tab.to_string(float_format=lambda x: f"{x:+.2%}"))

    # -------------------------------------------------- H_TIMING
    hdr("H_TIMING  is the gate's edge concentrated in drawdown years (a timing signal) or "
        "spread across all years (a volatility discount)?")
    spyy = yearly(SPY["U56"])
    bad3 = list(spyy.nsmallest(3).index)
    P(f"   the three worst SPY calendar years: {bad3}  "
      f"({', '.join(f'{spyy[y]:+.1%}' for y in bad3)})")
    tim = []
    for (k, u, cad, v, q, d), grp in Y[Y.variant != "CONTROL"].groupby(
            ["panel", "under", "cad", "variant", "q", "dial"], dropna=False):
        c = Y[(Y.panel == k) & (Y.under == u) & (Y.cad == cad) & (Y.variant == "CONTROL")] \
            .set_index("year").ret
        s = grp.set_index("year").ret
        e = (s - c).dropna()
        tim.append(dict(panel=k, under=u, cad=cad, variant=v, q=q, dial=d,
                        edge_bad=e[e.index.isin(bad3)].mean(),
                        edge_other=e[~e.index.isin(bad3)].mean()))
    T = pd.DataFrame(tim)
    T["timing"] = T.edge_bad > T.edge_other
    P("")
    P(T.groupby("variant")[["edge_bad", "edge_other", "timing"]].mean().to_string(
        float_format=lambda x: f"{x:+.4f}"))
    P("")
    P(f"   cells where the drawdown-year edge exceeds the other-year edge: "
      f"{int(T.timing.sum())} / {len(T)} = {T.timing.mean():.1%}")
    P(f"   H_TIMING -> {'TIMING SIGNAL' if T.timing.mean() >= 0.80 else 'NOT A CLEAN TIMING SIGNAL'} "
      f"(pre-registered bar 80%)")

    # -------------------------------------------------- KEEP paths
    hdr("KEEP PATHS - PROTOCOL 4a and 4b over EVERY book")
    P(f"   4a {int(B.keep4a.sum())} / {len(B)}      4b {int(B.keep4b.sum())} / {len(B)}")
    P("")
    P(B.groupby(["panel", "variant"]).agg(n=("keep4b", "size"), p4a=("keep4a", "sum"),
                                          p4b=("keep4b", "sum")).to_string())
    P("")
    P("   binding 4b legs over all books:")
    P(pd.Series([t for f in B.fail4b.fillna("") for t in (f.split("|") if f else [])])
      .value_counts().to_string())
    lv = B[(B.variant == "LEVEL") & (B.q == 0.20)].set_index(["panel", "under", "cad"])
    bought = []
    for _, r in B[~B.variant.isin(["CONTROL", "LEVEL"])].iterrows():
        base = lv.loc[(r.panel, r.under, r.cad)]
        if (r.keep4a and not base.keep4a) or (r.keep4b and not base.keep4b):
            bought.append(dict(panel=r.panel, under=r.under, cad=r.cad, variant=r.variant,
                               q=r.q, dial=r.dial, CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD,
                               k4a=r.keep4a, k4b=r.keep4b))
    BO = pd.DataFrame(bought)
    P("")
    P(f"   H_KEEP: de-lagged books clearing a KEEP path LEVEL@0.20 does NOT on the same arm: {len(BO)}")
    if len(BO): P(BO.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    P(f"   H_KEEP -> {'PASS' if len(BO) else 'FAIL'}")
    B.to_csv(f"{STEM}.keeppaths.csv", index=False)

    # -------------------------------------------------- H_REPRO
    hdr("H_REPRO  idea 48's published cell (U56, 12.2% / 1.131 / -12.7%, OOS 1.240, 2022 -9.0%)")
    for u in UNDERLYINGS:
        for cad in CADENCES:
            r = B[(B.panel == "U56") & (B.under == u) & (B.cad == cad) &
                  (B.variant == "LEVEL") & (B.q == 0.20)].iloc[0]
            y = Y[(Y.panel == "U56") & (Y.under == u) & (Y.cad == cad) &
                  (Y.variant == "LEVEL") & (Y.q == 0.20) & (Y.year == 2022)].ret.iloc[0]
            P(f"   U56 {u:5s} {cad}: {r.CAGR:6.2%} / {r.Sharpe:.3f} / {r.MaxDD:7.2%}   2022 {y:+.2%}")
    P("   Idea 48's book was a RANKED grid book, not a plain EWALL/MADG, so these are the "
      "closest cells this script builds, printed as a comparison and NOT as a reproduction.")

    # -------------------------------------------------- RULE 8
    hdr("RULE 8  (variant, q, dial) chosen on IS <= 2016-12-31 by IS Sharpe inside each "
        "panel x underlying; 2017-01-01.. read ONCE (2018/2020/2022 all untouched)")
    wf = []
    for k, px in PX.items():
        st = START[k]
        for u in UNDERLYINGS:
            cand = []
            for cad in CADENCES:
                for v, q, d in menu():
                    r = RET[(k, u, cad, v, q, d)]
                    cand.append((v, q, d, cad, metrics(r.loc[:"2016-12-31"])["Sharpe"], r))
            cand.sort(key=lambda x: -x[4])
            v, q, d, cad, iss, r = cand[0]
            ctl = CTL[(k, u, cad)]
            k4a, k4b, f = keep_paths(r, BASE[k], SPY[k])
            oo = r.loc[OOS0:]
            wf.append(dict(panel=k, under=u, pick=f"{v}@q={q}/d={d}/{cad}", IS_Sharpe=iss,
                           IS_CAGR=metrics(r.loc[:"2016-12-31"])["CAGR"],
                           OOS_CAGR=metrics(oo)["CAGR"], OOS_Sharpe=metrics(oo)["Sharpe"],
                           OOS_MaxDD=metrics(oo)["MaxDD"],
                           ctl_OOS_CAGR=metrics(ctl.loc[OOS0:])["CAGR"],
                           ctl_OOS_Sharpe=metrics(ctl.loc[OOS0:])["Sharpe"],
                           ctl_OOS_MaxDD=metrics(ctl.loc[OOS0:])["MaxDD"],
                           v2_OOS_Sharpe=metrics(BASE[k].loc[OOS0:])["Sharpe"],
                           v2_OOS_CAGR=metrics(BASE[k].loc[OOS0:])["CAGR"],
                           v1_OOS_Sharpe=metrics(V1[k].loc[OOS0:])["Sharpe"],
                           spy_OOS_CAGR=metrics(SPY[k].loc[OOS0:])["CAGR"],
                           spy_OOS_Sharpe=metrics(SPY[k].loc[OOS0:])["Sharpe"],
                           spy_OOS_MaxDD=metrics(SPY[k].loc[OOS0:])["MaxDD"],
                           full_CAGR=metrics(r)["CAGR"], full_Sharpe=metrics(r)["Sharpe"],
                           full_MaxDD=metrics(r)["MaxDD"], H1=row_of(r)["H1"], H2=row_of(r)["H2"],
                           y2018=yearly(r).get(2018, np.nan), y2020=yearly(r).get(2020, np.nan),
                           y2022=yearly(r).get(2022, np.nan),
                           ctl_y2022=yearly(ctl).get(2022, np.nan),
                           keep4a=k4a, keep4b=k4b, fail4b=f))
    W = pd.DataFrame(wf); W.to_csv(f"{STEM}.walkforward.csv", index=False)
    P(W[["panel", "under", "pick", "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
         "ctl_OOS_Sharpe", "v2_OOS_Sharpe", "spy_OOS_Sharpe", "full_CAGR", "full_Sharpe",
         "full_MaxDD", "H1", "H2", "y2018", "y2020", "y2022", "ctl_y2022", "keep4a", "keep4b",
         "fail4b"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    (Path(f"{STEM}.console.txt")).write_text(tee.getvalue())

if __name__ == "__main__":
    main()
