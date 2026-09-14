#!/usr/bin/env python3
"""Idea 852 (lane B, 2026-09-14) — does an EQUITY-DRAWDOWN THROTTLE on the band book
spend the unused 4b drawdown budget?

Diagnosis this is grounded in (research/CHANGELOG.md):
  * ideas 786/787/795 — the binding 4b leg is the CAGR FLOOR, and the live band book's
    MaxDD (-12.05%) sits far inside the 4b cap (60% of SPY's -33.72% = -20.23%), i.e.
    ~8 pp of drawdown budget is never spent.
  * idea 794 — the realised-VOL scaler is the KILLED way of spending it.
  * idea 403 — "no instrument here reads equity", so a book whose gross is a function of
    its OWN trailing drawdown has never been priced in this record. That is the sibling
    tested here.

BOOK.  Base = RULES v2's frozen band clause (band=0.03, `baseline.band_state`) at gross
1.00 (idea 733/795's standing candidate level), equal weight over the names in the band,
gated-out weight to CASH. THROTTLE: at each rebalance date t the book reads its own
equity through t (decided at t, applied at t+1 — no look-ahead), computes
dd_t = eq_t/cummax(eq)_t - 1, and targets gross g_low while dd_t <= -d, gross 1.00
otherwise. It re-arms as soon as dd_t recovers above -d.

TUNED PARAMETERS: exactly two — d (trigger) and g_low (throttled gross). 6 x 4 = 24 grid
points, ALL reported, plus the g_low=1.00 parent (no throttle) as a control.

PROTOCOL: 10 bps per unit turnover, weekly cadence, weights decided at close t applied at
t+1, no shorting, no leverage (g <= 1.00). Both KEEP paths evaluated. Rule 8 walk-forward
is run: (d, g_low) chosen on 2009-2016 IS Sharpe ONLY, read once on 2017-2026.

Panels: U56 (the live panel, `load_universe()`) and B136 (`load_universe(broad=True)`).
SURVIVORSHIP: both universe files are CURRENT constituents, which flatters any long book.

Run: python research/backtests/2026-09-14_equity-drawdown-throttle-on-the-band-book_B.py
Deterministic; no network (reads the committed price caches).
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, band_state, rules_v2_weights, rules_v1_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa

OUT = Path(__file__).with_suffix("")
COST_BPS = 10.0
FREQ = "W"
BAND = 0.03                      # FROZEN: the live clause, not a dial
WARMUP = 260                     # same warm-up skip baseline.compare uses
D_GRID = [0.04, 0.06, 0.08, 0.10, 0.12, 0.15]
G_GRID = [0.00, 0.25, 0.50, 0.75]
IS_END = "2016-12-31"            # rule 8: parameters chosen on 2009-2016 only
OOS_START = "2017-01-01"

# ----------------------------------------------------------------------------- runner
def run_throttle(px, d=None, g_low=1.00, gross=1.00, band=BAND, cost_bps=COST_BPS, freq=FREQ):
    """Path-dependent runner. Replicates engine.backtest exactly (drift between
    rebalances, cash = 1 - sum(w), costs on |new - drifted|) but sets the TARGET gross
    from the book's own realised equity drawdown at the decision date.

    d=None disables the throttle -> must equal engine.backtest on the same static book.
    Decision timing: the target for the bar applied at index i was computed from equity
    through i-1 (the shift-by-one the engine already applies to weights), so no look-ahead.
    """
    rets = px.pct_change().fillna(0.0)
    inband = band_state(px, band)
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    unit = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0).where(inband, 0.0)
    unit_s = unit.shift(1).fillna(0.0)                       # decided t, applied t+1
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False)

    n = len(px.index)
    cur = np.zeros(px.shape[1])
    held = np.zeros((n, px.shape[1]))
    turn = np.zeros(n)
    eq = 1.0
    peak = 1.0
    port = np.zeros(n)
    R = rets.values
    U = unit_s.values
    for i in range(n):
        if mask.iloc[i] or i == 0:
            g = gross
            if d is not None and (eq / peak - 1.0) <= -d:     # equity through i-1
                g = g_low
            new = U[i] * g
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        r_i = float((cur * R[i]).sum() - turn[i] * cost_bps / 1e4)
        port[i] = r_i
        eq *= (1.0 + r_i)
        peak = max(peak, eq)
        growth = cur * (1 + R[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    return pd.Series(port, index=px.index), pd.Series(turn, index=px.index)


def stats(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def keep_paths(s, base, spy):
    """PROTOCOL rule 4. 4a vs the live book (RULES v2); 4b vs SPY, BOTH halves."""
    p4a = (s["H1"] > base["H1"]) and (s["H2"] > base["H2"]) and (s["MaxDD"] >= base["MaxDD"])
    p4b = (s["H1"] > spy["H1"]) and (s["H2"] > spy["H2"]) and \
          (s["MaxDD"] >= 0.60 * spy["MaxDD"]) and (s["CAGR"] >= 0.70 * spy["CAGR"])
    return p4a, p4b


def fail4b(s, spy):
    f = []
    if not s["H1"] > spy["H1"]: f.append("H1")
    if not s["H2"] > spy["H2"]: f.append("H2")
    if not s["MaxDD"] >= 0.60 * spy["MaxDD"]: f.append("DDCAP")
    if not s["CAGR"] >= 0.70 * spy["CAGR"]: f.append("CAGRFLOOR")
    return "+".join(f) if f else "-"


# ------------------------------------------------------------------------------ gates
def gates(px, label):
    """Printed BEFORE any new number. All must pass."""
    print(f"\n### GATES ({label})")
    ok = True
    # G1: throttle OFF == engine.backtest on the identical static weights matrix.
    w = rules_v2_weights(px, band=BAND, gross=1.00)
    eng = backtest(px, w, cost_bps=COST_BPS, freq=FREQ)
    r_off, t_off = run_throttle(px, d=None, gross=1.00)
    fin = eng["returns"].notna().values          # the engine's own NaN warm-up rows
    n_nan = int((~fin).sum())
    g1r = float(np.abs(eng["returns"].values[fin] - r_off.values[fin]).max())
    g1t = float(np.abs(eng["turnover"].values[fin] - t_off.values[fin]).max())
    print(f"G1 throttle-off vs engine.backtest over {int(fin.sum())} finite rows "
          f"({n_nan} engine NaN warm-up rows excluded, both before the {WARMUP}-day skip): "
          f"max|dr| {g1r:.3e}  max|dturnover| {g1t:.3e}  "
          f"{'PASS' if max(g1r, g1t) < 1e-12 else 'FAIL'}")
    assert n_nan <= 2 and eng["returns"].index[~fin].max() < px.index[WARMUP]
    ok &= max(g1r, g1t) < 1e-12
    # G2: an unreachable trigger is the parent exactly (throttle wiring is inert when idle).
    r_hi, _ = run_throttle(px, d=0.99, g_low=0.00, gross=1.00)
    g2 = float(np.abs(r_hi.values - r_off.values).max())
    print(f"G2 d=0.99 (never fires) == parent: max|dr| {g2:.3e}  {'PASS' if g2 < 1e-12 else 'FAIL'}")
    ok &= g2 < 1e-12
    # G3: g_low == gross is the parent for EVERY trigger (throttle is a no-op at g_low=1).
    g3 = max(float(np.abs(run_throttle(px, d=d, g_low=1.00, gross=1.00)[0].values - r_off.values).max())
             for d in D_GRID)
    print(f"G3 g_low=1.00 == parent at all 6 triggers: max|dr| {g3:.3e}  {'PASS' if g3 < 1e-12 else 'FAIL'}")
    ok &= g3 < 1e-12
    # G4: cost-rung identity r(c) = r(0) - turnover*c/1e4 on a LIVE throttled run.
    r0, t0 = run_throttle(px, d=0.08, g_low=0.25, cost_bps=0.0)
    r25, _ = run_throttle(px, d=0.08, g_low=0.25, cost_bps=25.0)
    # not an identity for a path-dependent book (equity feeds the trigger); report it.
    g4 = float(np.abs((r0 - t0 * 25.0 / 1e4).values - r25.values).max())
    print(f"G4 cost-rung identity on a throttled arm: max|d| {g4:.3e} "
          f"(REPORTED, not a pass/fail: the trigger reads equity, so costs can move the path)")
    return ok


# ------------------------------------------------------------------------------- main
def run_panel(px, label):
    assert gates(px, label), f"gates failed on {label}"
    start = px.index[WARMUP]
    spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
    base_r = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    v1_r = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    parent_r, _ = run_throttle(px, d=None, gross=1.00)
    parent_r = parent_r.loc[start:]

    refs = {"SPY": spy_r, "RULES v2 (live)": base_r, "RULES v1": v1_r,
            "BAND g=1.00 (parent, no throttle)": parent_r}
    spy, base = stats(spy_r), stats(base_r)

    rows = []
    for name, r in refs.items():
        s = stats(r); a, b = keep_paths(s, base, spy)
        rows.append(dict(panel=label, arm=name, d=np.nan, g_low=np.nan, **s,
                         keep4a=a, keep4b=b, fail4b=fail4b(s, spy)))
    series = {}
    for d in D_GRID:
        for g in G_GRID:
            r, _ = run_throttle(px, d=d, g_low=g, gross=1.00)
            r = r.loc[start:]
            series[(d, g)] = r
            s = stats(r); a, b = keep_paths(s, base, spy)
            rows.append(dict(panel=label, arm=f"THROTTLE d={d:.2f} g_low={g:.2f}", d=d, g_low=g,
                             **s, keep4a=a, keep4b=b, fail4b=fail4b(s, spy)))
    grid = pd.DataFrame(rows)

    # ---- rule 8 walk-forward: choose (d, g_low) on 2009-2016 IS Sharpe, read OOS once.
    wf_rows = []
    is_sh = {k: metrics(v.loc[:IS_END])["Sharpe"] for k, v in series.items()}
    best = max(is_sh.values())
    tied = [k for k, v in is_sh.items() if abs(v - best) < 1e-12]
    pick = tied[0]                      # convention: first in (d, g_low) grid order
    if len(tied) > 1:
        print(f"\n!! IS TIE ({label}): {len(tied)} arms share the IS-best Sharpe {best:.6f} "
              f"-> {tied}. The throttle NEVER FIRES in-sample at these dials, so the pick is "
              f"decided by the tie convention, not by the data. ALL tied arms are read OOS below.")
    oos = {"THROTTLE pick d=%.2f g_low=%.2f" % pick: series[pick].loc[OOS_START:]}
    for k in tied[1:]:
        oos["THROTTLE IS-tied d=%.2f g_low=%.2f" % k] = series[k].loc[OOS_START:]
    oos.update({"BAND g=1.00 parent": parent_r.loc[OOS_START:],
                "RULES v2 (live)": base_r.loc[OOS_START:], "SPY": spy_r.loc[OOS_START:]})
    spy_o = stats(oos["SPY"]); base_o = stats(oos["RULES v2 (live)"])
    for n, r in oos.items():
        s = stats(r); a, b = keep_paths(s, base_o, spy_o)
        wf_rows.append(dict(panel=label, leg="OOS 2017-2026", arm=n,
                            is_sharpe=best if n.startswith("THROTTLE") else np.nan,
                            **s, keep4a=a, keep4b=b, fail4b=fail4b(s, spy_o)))
    # every grid point's OOS too, so the pick is not the only number published
    for k, v in series.items():
        s = stats(v.loc[OOS_START:]); a, b = keep_paths(s, base_o, spy_o)
        wf_rows.append(dict(panel=label, leg="OOS ALL GRID", arm=f"d={k[0]:.2f} g_low={k[1]:.2f}",
                            is_sharpe=is_sh[k], **s, keep4a=a, keep4b=b, fail4b=fail4b(s, spy_o)))
    wf = pd.DataFrame(wf_rows)
    return grid, wf, pick, is_sh, tied


def main():
    pd.set_option("display.width", 200)
    fmt = lambda x: f"{x:.4f}" if isinstance(x, float) else str(x)
    grids, wfs, picks = [], [], {}
    for label, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        print(f"\n{'='*100}\nPANEL {label}: {px.shape[1]} columns, "
              f"{px.index[0].date()} -> {px.index[-1].date()}")
        g, w, pick, is_sh, tied = run_panel(px, label)
        print(f"\n### FULL SAMPLE + HALVES ({label}) — all 24 grid points + 4 references")
        print(g.to_string(index=False, float_format=fmt))
        print(f"\n### RULE 8 ({label}) — pick d={pick[0]:.2f} g_low={pick[1]:.2f} "
              f"(IS 2009-{IS_END[:4]} Sharpe {is_sh[pick]:.4f}; {len(tied)} arms tied at that IS Sharpe), OOS read once")
        print(w[w.leg == "OOS 2017-2026"].to_string(index=False, float_format=fmt))
        print(f"\n### RULE 8 ({label}) — every grid point's OOS, published")
        print(w[w.leg == "OOS ALL GRID"].to_string(index=False, float_format=fmt))
        grids.append(g); wfs.append(w); picks[label] = pick
    G = pd.concat(grids, ignore_index=True); W = pd.concat(wfs, ignore_index=True)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)

    print(f"\n{'='*100}\n### KEEP-PATH TALLY (throttled arms only, 24 per panel)")
    arms = G[G.d.notna()]
    print(arms.groupby("panel")[["keep4a", "keep4b"]].sum().to_string())
    print("\n4b failing legs, full sample (throttled arms):")
    print(arms.groupby(["panel", "fail4b"]).size().to_string())
    oos_arms = W[W.leg == "OOS ALL GRID"]
    print("\nOOS keep tally (24 per panel):")
    print(oos_arms.groupby("panel")[["keep4a", "keep4b"]].sum().to_string())
    print("\nOOS 4b failing legs:")
    print(oos_arms.groupby(["panel", "fail4b"]).size().to_string())
    # ---- the two decisive readings, computed from the published tables -------------
    print(f"\n{'='*100}\n### A. DOES ANY THROTTLED ARM BEAT ITS OWN PARENT?")
    for panel in ("U56", "B136"):
        par = G[(G.panel == panel) & (G.arm.str.startswith("BAND g=1.00"))].iloc[0]
        a = G[(G.panel == panel) & G.d.notna()]
        inert = a[(np.abs(a.Sharpe - par.Sharpe) < 1e-12) & (np.abs(a.CAGR - par.CAGR) < 1e-12)]
        firing = a.drop(inert.index)
        print(f"{panel} FULL: parent Sharpe {par.Sharpe:.4f} CAGR {par.CAGR:.2%} MaxDD {par.MaxDD:.2%} | "
              f"{len(inert)}/{len(a)} arms BIT-IDENTICAL to the parent (throttle never fires) | "
              f"best FIRING arm Sharpe {firing.Sharpe.max():.4f} CAGR {firing.CAGR.max():.2%} | "
              f"firing arms that beat the parent on Sharpe: "
              f"{int((firing.Sharpe > par.Sharpe + 1e-12).sum())}/{len(firing)}, on CAGR: "
              f"{int((firing.CAGR > par.CAGR + 1e-12).sum())}/{len(firing)}")
        po = W[(W.panel == panel) & (W.arm == "BAND g=1.00 parent")].iloc[0]
        ao = W[(W.leg == "OOS ALL GRID") & (W.panel == panel)]
        io = ao[(np.abs(ao.Sharpe - po.Sharpe) < 1e-12) & (np.abs(ao.CAGR - po.CAGR) < 1e-12)]
        fo = ao.drop(io.index)
        print(f"{panel} OOS : parent Sharpe {po.Sharpe:.4f} CAGR {po.CAGR:.2%} | "
              f"{len(io)}/{len(ao)} inert | firing arms beating parent on Sharpe: "
              f"{int((fo.Sharpe > po.Sharpe + 1e-12).sum())}/{len(fo)}, on CAGR: "
              f"{int((fo.CAGR > po.CAGR + 1e-12).sum())}/{len(fo)}")
    print(f"\n### B. THE g_low=0.00 ABSORBING TRAP (first date the arm's gross reaches 0 and stays)")
    for label, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        for d in D_GRID:
            r, _ = run_throttle(px, d=d, g_low=0.00, gross=1.00)
            r = r.loc[px.index[WARMUP]:]
            nz = r[r != 0.0]
            last = nz.index[-1] if len(nz) else None
            trapped = last is not None and last < r.index[-1]
            print(f"{label} d={d:.2f} g_low=0.00: last non-zero return {last.date() if last is not None else 'n/a'}; "
                  + ("ABSORBED (never re-arms: zero gross -> flat equity -> drawdown never recovers); "
                     f"{(r.index[-1] - last).days / 365.25:.1f} years of the sample held in 100% cash"
                     if trapped else "NEVER FIRES (trigger unreached over the whole sample)"))
    print(f"\nWrote {OUT}.grid.csv and {OUT}.walkforward.csv")


if __name__ == "__main__":
    main()
