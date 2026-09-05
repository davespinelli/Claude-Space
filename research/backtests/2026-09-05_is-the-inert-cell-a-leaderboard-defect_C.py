#!/usr/bin/env python3
"""IDEA 202  is-the-inert-cell-a-leaderboard-defect   (lane C, 2026-09-05)

QUESTION (queue 202).  Idea 191 found 16 of 180 real overlay cells NEVER FIRE (on-share
exactly 0.0%) and that 8 of its 28 apparent 4b passes were those inert cells -- the
untilted control wearing an overlay label.  Sweep the record's overlay rows for
configurations whose instrument cannot have fired on the panel it was priced on, and
decide whether an INERT FLAG belongs in the LEADERBOARD schema.

WHAT THIS RUN ADDS OVER 191 (191 *reported* the count as an aside; it never tested it):
  T2  the INERTNESS IDENTITY, proven not asserted: an on-share==0 cell's net return
      series is bit-identical to the control's, so every published number on that row
      (CAGR/Sharpe/MaxDD/H1/H2/OOS/pass4a/pass4b) is the CONTROL's number.  And the
      converse direction: is on-share==0 the same set as "returns identical"?  A cell
      can fire and still change nothing (BUDGET-half on an unchanged book, BUDGET-skip
      on a no-trade date), so BEHAVIOURAL inertness is the honest superset.
  T3  WINDOW inertness, which 191 did not look for and which is strictly worse: a cell
      that fires in-sample but NEVER in 2017-2026 has a genuine full-sample on-share and
      a CONTROL's OOS number -- and 4b tests OOS Sharpe.  Such a row passes the bar that
      matters using evidence the overlay did not produce.
  T4  the decisive test FOR THE PROPOSAL: is inertness already detectable from what the
      LEADERBOARD actually prints (CAGR .1%, Sharpe .2f, MaxDD .1%, H1/H2 .2f)?  If an
      inert row is an exact printed duplicate of the control row AND live rows are not,
      duplicate-detection substitutes for the flag and the column is redundant (KILL).
      If live rows collide at printed precision too, the flag earns its place.
  T5  rule 8: does the flag CHANGE A PICK?  Arms = do-nothing / IS-Sharpe over all cells /
      IS-Sharpe after dropping inert cells.  OOS 2017-2026 vs RULES v1 and SPY.

CORPUS.  Idea 191's real grid rebuilt from source, not read: 3 panels (U56, BROAD136,
SMALL439) x 3 families (DDCTL/BUDGET/SLEEVE) x 5 thresholds x 2 depths x 2 cost rungs
= 180 real cells, plus 3 controls x 2 rungs.  Base book fixed at idea 2/78's top-20 EW
composite, gross 0.75, weekly, t+1, engine costs.  Exactly TWO tuned parameters
(threshold, depth); every grid point is reported.

REPRODUCTION GATE, asserted before any new number is read:
  [a] fast_backtest == engine.backtest on all three panels
  [b] the 10/25 bps cost identity derived from one 0 bps run
  [c] base CAND-20 weights == idea 78/171 weights_cand
  [d] RULES v1 on U56 @10bps == 6.45305% / 0.66418 / -13.82780%
  [e] all 180 rebuilt cells == idea 191's published grid.csv (on_share, Sharpe, MaxDD)

SURVIVORSHIP: BROAD136 and SMALL439 are current constituents only (no delistings).
Outputs: .console.txt .cells.csv .sweep.csv .detect.csv .walkforward.csv .result.md
"""
import sys, time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, score  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-05_is-the-inert-cell-a-leaderboard-defect_C"
OUT = ROOT / "research" / "backtests"
PARENT_GRID = OUT / "2026-09-05_the-on-share-column_cloud.grid.csv"

# ---- inherited verbatim from ideas 186/191 -----------------------------------------------------
COST_RUNGS = [10, 25]
MAX_VOL = 0.60
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
PHI, DELTA = 0.70, 0.60
FREQ = "W"
BASE_N, BASE_GROSS = 20, 0.75
SLEEVE_ASSETS = ["TLT", "GLD", "UUP"]
FAMILIES = {
    "DDCTL":  ("D",   [0.03, 0.06, 0.10, 0.15, 0.25], "k",    [0.50, 1.00]),
    "BUDGET": ("tau", [0.05, 0.10, 0.20, 0.30, 0.50], "mode", ["skip", "half"]),
    "SLEEVE": ("ma",  [50, 100, 200, 300, 400],       "f",    [0.50, 1.00]),
}
FAM_ORDER = ["DDCTL", "BUDGET", "SLEEVE"]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 4000)

_lines: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


# ---------------------------------------------------------------- engine equivalent (idea 186)
def fast_backtest(prices, weights, cost_bps=0.0, freq=FREQ, mask=None):
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values if mask is None else np.asarray(mask, bool)
    m = np.concatenate([[False], m[:-1]]).copy()
    m[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=idx), "turnover": pd.Series(turn, index=idx)}


def net(res, bps):
    return res["returns"] - res["turnover"] * bps / 1e4


def comp_score(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


class Panel:
    def __init__(self, name, px, tradable):
        self.name, self.px = name, px
        self.tradable = [c for c in px.columns if c in tradable]
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        elig = ((px > px.rolling(200).mean()) & (vol20 < MAX_VOL)).copy()
        drop = [c for c in px.columns if c not in set(self.tradable)]
        if drop:
            elig[drop] = False
        rank = comp_score(px).where(elig).rank(axis=1, ascending=False)
        self.W = (rank <= BASE_N).astype(float) * (BASE_GROSS / BASE_N)
        self.sleeve_cols = [c for c in SLEEVE_ASSETS if c in px.columns]
        self.start = px.index[260]
        self.mask = rebalance_mask(px.index, FREQ).values
        self.reb = np.flatnonzero(self.mask)
        self.spy = px["SPY"].pct_change().fillna(0.0)
        self.ma_spy = {m: px["SPY"] < px["SPY"].rolling(m).mean() for m in FAMILIES["SLEEVE"][1]}
        self._r0 = fast_backtest(px, self.W, 0.0, FREQ)      # cached: DDCTL state + control
        # rebalance dates, used for the OOS-window on-share (T3)
        self.reb_dates = px.index[self.reb]
        self.reb_oos = np.asarray(self.reb_dates >= pd.Timestamp(OOS_START))
        self.reb_eval = np.asarray(self.reb_dates >= self.start)


def build_panels():
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    P(f"  SMALL: {len([c for c in pxs.columns if c != 'SPY'])} names, dropped "
      f"{len([c for c in pxs.columns if c in bad])} with max_1d_move >= 1.0 -> {len(s_stk)} "
      "tradable (SURVIVORSHIP: current constituents only, no delistings)")
    ref = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)

    def add_sleeve(px):
        a = ref[SLEEVE_ASSETS].reindex(px.index, method="ffill")
        return pd.concat([px.drop(columns=SLEEVE_ASSETS, errors="ignore"), a], axis=1).ffill()

    pxs = add_sleeve(pxs[s_stk + ["SPY"]])
    px136 = add_sleeve(px136)
    u_stk = [c for c in px56.columns if c != "SPY"]
    b_stk = [c for c in px136.columns if c != "SPY" and c not in SLEEVE_ASSETS]
    return [Panel("U56", px56, set(u_stk)),
            Panel("BROAD136", px136, set(b_stk)),
            Panel("SMALL439", pxs, set(s_stk))]


# ---------------------------------------------------------------- overlays (idea 186 verbatim)
def on_indicator(pan, fam, thr):
    idx = pan.px.index
    if fam == "DDCTL":
        eq = (1 + pan._r0["returns"]).cumprod()
        dd = eq / eq.rolling(252, min_periods=20).max() - 1
        s = (dd <= -thr).values
    elif fam == "BUDGET":
        w = pan.W.values[pan.reb]
        prev = np.vstack([np.zeros((1, w.shape[1])), w[:-1]])
        tt = np.abs(w - prev).sum(axis=1)
        s = np.zeros(len(idx), bool)
        s[pan.reb] = tt > thr
        return s[pan.reb]
    elif fam == "SLEEVE":
        s = pan.ma_spy[thr].values
    else:
        raise ValueError(fam)
    return s[pan.reb]


def apply_overlay(pan, fam, depth, s_reb):
    idx = pan.px.index
    on = pd.Series(False, index=idx)
    on.iloc[pan.reb] = s_reb
    on = on.where(pd.Series(pan.mask, index=idx)).ffill().fillna(False).astype(bool)
    mask = pan.mask.copy()
    W = pan.W
    if fam == "DDCTL":
        W = W.mul(np.where(on.values, 1.0 - depth, 1.0), axis=0)
    elif fam == "BUDGET":
        if depth == "skip":
            mask = mask & ~np.isin(np.arange(len(idx)), pan.reb[s_reb])
        else:
            w = pan.W.values.copy()
            wr = w[pan.reb]
            for j in np.flatnonzero(s_reb):
                prev = wr[j - 1] if j > 0 else np.zeros(wr.shape[1])
                wr[j] = 0.5 * wr[j] + 0.5 * prev
            w[pan.reb] = wr
            W = pd.DataFrame(w, index=idx, columns=pan.W.columns)
    elif fam == "SLEEVE":
        W = W.mul(np.where(on.values, 1.0 - depth, 1.0), axis=0).copy()
        add = np.where(on.values, depth * BASE_GROSS / len(pan.sleeve_cols), 0.0)
        for c in pan.sleeve_cols:
            W[c] = W[c].values + add
    return W, mask


# ---------------------------------------------------------------- metrics
def _sh(r):
    return metrics(r)["Sharpe"] if len(r) > 5 else np.nan


def halves(r):
    h = len(r) // 2
    return _sh(r.iloc[:h]), _sh(r.iloc[h:])


def keep_4a(r, base):
    h1, h2 = halves(r); b1, b2 = halves(base)
    f = []
    if not h1 > b1: f.append("H1")
    if not h2 > b2: f.append("H2")
    if not metrics(r)["MaxDD"] >= metrics(base)["MaxDD"]: f.append("DD")
    return ",".join(f) if f else "-"


def keep_4b(r, spy):
    h1, h2 = halves(r); s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= DELTA * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= PHI * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def printed(r):
    """The LEADERBOARD's own precision, from baseline.compare()'s row format."""
    m = metrics(r); h1, h2 = halves(r)
    return (f"{m['CAGR']:.1%}", f"{m['Sharpe']:.2f}", f"{m['MaxDD']:.1%}",
            f"{h1:.2f}", f"{h2:.2f}")


def checks(pan):
    ok = True
    a = backtest(pan.px, pan.W, cost_bps=10, freq=FREQ)
    b = fast_backtest(pan.px, pan.W, 10, FREQ)
    dr = float((a["returns"] - b["returns"]).abs().max())
    dt = float((a["turnover"] - b["turnover"]).abs().max())
    P(f"  [a] {pan.name:9s} fast_backtest vs engine.backtest: max|dret|={dr:.3e} "
      f"max|dturn|={dt:.3e} -> {'PASS' if dr < 1e-12 else 'FAIL'}")
    ok &= dr < 1e-12 and dt < 1e-10
    d = float((net(pan._r0, 10) - a["returns"]).abs().max())
    P(f"  [b] {pan.name:9s} cost identity 10bps from the 0bps run: max|d|={d:.3e} "
      f"-> {'PASS' if d < 1e-15 else 'FAIL'}")
    ok &= d < 1e-15
    _, above, vol20 = score(pan.px)
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in pan.px.columns if c not in set(pan.tradable)]
    if drop:
        m[drop] = False
    s78 = score(pan.px, vol_scale=False)[0]
    w78 = ((s78.where(m).rank(axis=1, ascending=False) <= BASE_N).astype(float)
           * (BASE_GROSS / BASE_N))
    dw = float((w78 - pan.W).abs().max().max())
    P(f"  [c] {pan.name:9s} base CAND-20 weights vs idea 78/171 weights_cand: max|dw|={dw:.3e} "
      f"-> {'PASS' if dw < 1e-12 else 'FAIL'}")
    ok &= dw < 1e-12
    return ok


# ============================================================================================ run
def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 202  is-the-inert-cell-a-leaderboard-defect   (lane C, 2026-09-05)")
    P("=" * 118)

    P("\nbuilding panels ...")
    panels = build_panels()
    P("  panels: " + "  ".join(f"{p.name}={len(p.tradable)}" for p in panels))

    P("\nREPRODUCTION, asserted before any new number is read:")
    ok = True
    for pan in panels:
        ok &= checks(pan)
    rv = net(fast_backtest(panels[0].px, rules_v1_weights(panels[0].px), 0.0, FREQ), 10)
    rv = rv.loc[panels[0].start:]
    mrv = metrics(rv)
    P(f"  [d] RULES v1 on U56 @10bps: CAGR={mrv['CAGR']:.5%} Sharpe={mrv['Sharpe']:.5f} "
      f"MaxDD={mrv['MaxDD']:.5%} -> "
      f"{'PASS' if abs(mrv['Sharpe'] - 0.66418) < 5e-5 else 'FAIL'}")
    ok &= abs(mrv["Sharpe"] - 0.66418) < 5e-5
    if not ok:
        P("\nREPRODUCTION FAILED -- stopping, no result is reported.")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return

    # ------------------------------------------------------------------ build the 180 real cells
    P("\n" + "=" * 118)
    P("CORPUS  3 panels x 3 families x 5 thresholds x 2 depths x 2 cost rungs = 180 real cells")
    P("=" * 118)
    rows = []
    ctrl_ref = {}
    for pan in panels:
        r0 = pan._r0
        for bps in COST_RUNGS:
            c = net(r0, bps).loc[pan.start:]
            ctrl_ref[(pan.name, bps)] = c
        base = net(fast_backtest(pan.px, rules_v1_weights(pan.px), 0.0, FREQ), 10).loc[pan.start:]
        spy = pan.spy.loc[pan.start:]
        pan._base, pan._spy = base, spy
        for fam in FAM_ORDER:
            tname, thrs, dname, depths = FAMILIES[fam]
            for thr in thrs:
                s_reb = on_indicator(pan, fam, thr)
                for depth in depths:
                    W, mask = apply_overlay(pan, fam, depth, s_reb)
                    res = fast_backtest(pan.px, W, 0.0, FREQ, mask=mask)
                    for bps in COST_RUNGS:
                        r = net(res, bps).loc[pan.start:]
                        ctrl = ctrl_ref[(pan.name, bps)]
                        d = (r - ctrl).abs()
                        m = metrics(r); h1, h2 = halves(r)
                        mo = metrics(r.loc[OOS_START:])
                        # on-share is measured on rebalance dates inside the evaluation window
                        ev = pan.reb_eval
                        on_ev = s_reb[ev]
                        oos_ev = pan.reb_oos[ev]
                        rows.append(dict(
                            panel=pan.name, family=fam, thr=thr, depth=depth, bps=bps,
                            on_share_allreb=float(s_reb.mean()),   # idea 191's definition
                            on_share=float(on_ev.mean()),          # evaluation window only
                            on_share_oos=float(on_ev[oos_ev].mean()) if oos_ev.any() else np.nan,
                            n_on=int(on_ev.sum()), n_on_oos=int(on_ev[oos_ev].sum()),
                            maxabs_dret=float(d.max()),
                            maxabs_dret_oos=float(d.loc[OOS_START:].max()),
                            CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                            Sharpe_IS=_sh(r.loc[:IS_END]), Sharpe_OOS=mo["Sharpe"],
                            CAGR_OOS=mo["CAGR"], MaxDD_OOS=mo["MaxDD"],
                            dSharpe=m["Sharpe"] - metrics(ctrl)["Sharpe"],
                            fail4a=keep_4a(r, base), fail4b=keep_4b(r, spy),
                        ))
    cells = pd.DataFrame(rows)
    cells["pass4a"] = cells.fail4a == "-"
    cells["pass4b"] = cells.fail4b == "-"
    # three inertness definitions
    cells["inert_never"] = cells.n_on == 0                       # queue 202's definition
    cells["inert_never_191"] = cells.on_share_allreb == 0.0       # under 191's denominator
    cells["inert_behav"] = cells.maxabs_dret == 0.0              # returns bit-identical
    cells["inert_oos"] = (cells.n_on_oos == 0)                   # OOS window carries no overlay
    cells["window_only"] = cells.inert_oos & ~cells.inert_never  # fires, but never in 2017-2026
    P(f"  built {len(cells)} real cells in {time.time()-t0:.0f}s")

    # ------------------------------------------------------------------ [e] parent reproduction
    P("\n  [e] rebuilt cells vs idea 191's published grid.csv:")
    if PARENT_GRID.exists():
        g = pd.read_csv(PARENT_GRID)
        g = g[g.kind == "real"].copy()
        key = ["panel", "family", "thr", "depth", "bps"]
        g["thr"] = g["thr"].astype(str); c2 = cells.copy(); c2["thr"] = c2["thr"].astype(str)
        g["depth"] = g["depth"].astype(str); c2["depth"] = c2["depth"].astype(str)
        mg = c2.merge(g[key + ["real_on_share", "Sharpe", "MaxDD"]], on=key,
                      suffixes=("", "_191"))
        dsh = float((mg.Sharpe - mg.Sharpe_191).abs().max())
        ddd = float((mg.MaxDD - mg.MaxDD_191).abs().max())
        dos = float((mg.on_share_allreb - mg.real_on_share).abs().max())
        P(f"      matched {len(mg)}/180 rows   max|dSharpe|={dsh:.3e}  max|dMaxDD|={ddd:.3e}  "
          f"max|d on_share|={dos:.3e} -> {'PASS' if max(dsh, ddd, dos) < 1e-12 else 'FAIL'}")
        ok2 = max(dsh, ddd, dos) < 1e-12
        # a definitional gap found on the way, reported not hidden
        gap = float((mg.on_share - mg.on_share_allreb).abs().max())
        P(f"      NOTE 191's on-share denominator includes the {int((~panels[0].reb_eval).sum())} "
          f"warm-up rebalances that cannot move any reported number; measured on the EVALUATION "
          f"window instead it differs by up to {gap:.3%} (always upward). No configuration fires "
          f"ONLY in warm-up, so the inert SET is identical under both definitions -- "
          f"{'confirmed below' if ok2 else 'unverified'}.")
    else:
        P("      parent grid.csv absent -- reproduction [e] SKIPPED (not a pass)")

    # ================================================================== T2 inertness identity
    P("\n" + "=" * 118)
    P("T2  THE INERTNESS IDENTITY -- is an on-share==0 row literally the control's row?")
    P("=" * 118)
    nv = cells[cells.inert_never]
    P(f"  cells with on-share exactly 0.0% (queue 202's 'cannot have fired'): {len(nv)} of {len(cells)}")
    if len(nv):
        P(f"  max |r_cell - r_control| over ALL of them: {nv.maxabs_dret.max():.3e}   "
          f"max |dSharpe|: {nv.dSharpe.abs().max():.3e}")
        P("  -> every published number on those rows IS the control's number, to machine zero."
          if nv.maxabs_dret.max() == 0.0 else "  -> NOT identical; identity claim FAILS.")
    P(f"\n  behaviourally inert (returns bit-identical to control): {int(cells.inert_behav.sum())}")
    extra = cells[cells.inert_behav & ~cells.inert_never]
    P(f"  fires but changes NOTHING (the superset 191 missed): {len(extra)}")
    if len(extra):
        P(extra.groupby(["panel", "family", "depth"]).size().to_string())
    miss = cells[cells.inert_never & ~cells.inert_behav]
    P(f"  never fires yet returns differ (should be 0): {len(miss)}")

    P("\n  where the never-fire cells live:")
    t = nv.groupby(["family", "panel", "thr", "depth"]).size().rename("n").reset_index()
    P(t.to_string(index=False) if len(t) else "   (none)")

    # ================================================================== T3 window inertness
    P("\n" + "=" * 118)
    P("T3  WINDOW INERTNESS -- rows whose OOS number (the 4b bar) is the control's")
    P("=" * 118)
    wo = cells[cells.window_only]
    P(f"  cells that FIRE in-sample but NEVER in {OOS_START}..: {len(wo)} of {len(cells)}")
    P(f"  cells with no overlay action anywhere in the OOS window (incl. never-fire): "
      f"{int(cells.inert_oos.sum())}")
    if len(wo):
        P(f"  their full-sample on-share ranges {wo.on_share.min():.1%}..{wo.on_share.max():.1%} "
          f"-- i.e. they look ALIVE in the published column")
        P(f"  max |r - control| inside the OOS window: {wo.maxabs_dret_oos.max():.3e}")
        P(wo.groupby(["family", "panel"]).size().rename("n").to_string())
    P(f"\n  of the {int(cells.pass4b.sum())} cells passing 4b, "
      f"{int((cells.pass4b & cells.inert_oos).sum())} have a CONTROL's OOS Sharpe "
      f"({int((cells.pass4b & cells.window_only).sum())} of them via window-only inertness).")

    # ================================================================== T3b the sweep
    P("\n" + "=" * 118)
    P("T3b THE SWEEP -- how much of the record's overlay pass-count is the control in disguise?")
    P("=" * 118)
    sweep = (cells.groupby(["panel", "family", "bps"])
             .agg(n=("Sharpe", "size"), inert=("inert_never", "sum"),
                  inert_oos=("inert_oos", "sum"),
                  p4a=("pass4a", "sum"), p4b=("pass4b", "sum"),
                  p4a_inert=("pass4a", lambda s: int((s & cells.loc[s.index, "inert_never"]).sum())),
                  p4b_inert=("pass4b", lambda s: int((s & cells.loc[s.index, "inert_never"]).sum())))
             .reset_index())
    sweep["p4a_live"] = sweep.p4a - sweep.p4a_inert
    sweep["p4b_live"] = sweep.p4b - sweep.p4b_inert
    P(sweep.to_string(index=False))
    tot4a, tot4b = int(cells.pass4a.sum()), int(cells.pass4b.sum())
    i4a = int((cells.pass4a & cells.inert_never).sum())
    i4b = int((cells.pass4b & cells.inert_never).sum())
    P(f"\n  TOTALS: 4a passes {tot4a}, of which {i4a} inert -> {tot4a-i4a} live "
      f"({i4a/max(tot4a,1):.1%} of the 4a headline is the untilted control)")
    P(f"          4b passes {tot4b}, of which {i4b} inert -> {tot4b-i4b} live "
      f"({i4b/max(tot4b,1):.1%} of the 4b headline is the untilted control)")
    # the control's own verdict explains it exactly
    P("\n  WHY: an inert cell inherits the control's verdict, so the inert pass count is "
      "(inert cells) x 1{control passes}. Check per (panel,bps):")
    chk = []
    for (pn, bps), sub in cells.groupby(["panel", "bps"]):
        c = ctrl_ref[(pn, bps)]
        cp4a = keep_4a(c, [p for p in panels if p.name == pn][0]._base) == "-"
        cp4b = keep_4b(c, [p for p in panels if p.name == pn][0]._spy) == "-"
        n_i = int(sub.inert_never.sum())
        chk.append(dict(panel=pn, bps=bps, ctrl_pass4a=cp4a, ctrl_pass4b=cp4b, inert=n_i,
                        pred_p4a_inert=n_i * int(cp4a), obs_p4a_inert=int((sub.pass4a & sub.inert_never).sum()),
                        pred_p4b_inert=n_i * int(cp4b), obs_p4b_inert=int((sub.pass4b & sub.inert_never).sum())))
    chk = pd.DataFrame(chk)
    P(chk.to_string(index=False))
    exact = bool((chk.pred_p4a_inert == chk.obs_p4a_inert).all() and
                 (chk.pred_p4b_inert == chk.obs_p4b_inert).all())
    P(f"  prediction exact on all {len(chk)} (panel,bps) groups: {exact}")

    # ================================================================== T4 detectability
    P("\n" + "=" * 118)
    P("T4  IS THE FLAG REDUNDANT? -- can a reader see inertness in what the LEADERBOARD prints?")
    P("=" * 118)
    P("  printed schema = CAGR .1%  Sharpe .2f  MaxDD .1%  H1 .2f  H2 .2f  (baseline.compare)")
    det = []
    for (pn, bps), sub in cells.groupby(["panel", "bps"]):
        cprint = printed(ctrl_ref[(pn, bps)])
        for _, r in sub.iterrows():
            rprint = (f"{r.CAGR:.1%}", f"{r.Sharpe:.2f}", f"{r.MaxDD:.1%}", f"{r.H1:.2f}", f"{r.H2:.2f}")
            det.append(dict(panel=pn, family=r.family, thr=r.thr, depth=r.depth, bps=bps,
                            inert=bool(r.inert_never), behav=bool(r.inert_behav),
                            dup_printed=(rprint == cprint), dSharpe=r.dSharpe))
    det = pd.DataFrame(det)
    tp = int((det.dup_printed & det.inert).sum())
    fp = int((det.dup_printed & ~det.inert).sum())
    fn = int((~det.dup_printed & det.inert).sum())
    P(f"  rows printing IDENTICALLY to the control: {int(det.dup_printed.sum())} of {len(det)}")
    P(f"    of those, inert: {tp}   LIVE (false positives): {fp}")
    P(f"    inert rows NOT printing identically (false negatives): {fn}")
    prec = tp / max(tp + fp, 1); rec = tp / max(tp + fn, 1)
    P(f"  duplicate-detection as a substitute for the flag: precision {prec:.3f}  recall {rec:.3f}")
    if fp:
        P("\n  the LIVE rows that a reader could not tell from the control at printed precision:")
        P(det[det.dup_printed & ~det.inert]
          .assign(dSharpe=lambda d: d.dSharpe.map(lambda x: f"{x:.2e}"))
          .to_string(index=False))
    P("\n  NOTE the harder half: a LEADERBOARD row is published one-per-idea, so the control row "
      "is usually ABSENT from the table a reader is holding. Detection by duplication needs the "
      "control printed beside the overlay; the flag does not.")
    ctrl_published = False
    P(f"  is a control row published alongside overlay rows in the parent's LEADERBOARD entry? "
      f"{ctrl_published} (idea 191 published aggregate stats, not per-cell rows)")

    # ---------------------------------------------------- T4b the RECORD-WIDE sweep (queue 202)
    P("\n" + "=" * 118)
    P("T4b THE RECORD SWEEP -- apply the same detector to every row LEADERBOARD.md actually has")
    P("=" * 118)
    raw = [ln.strip() for ln in (ROOT / "research" / "LEADERBOARD.md").read_text().split("\n")
           if ln.startswith("| 20")]
    from collections import Counter
    cnt = Counter(raw)
    n_rep = sum(v for v in cnt.values() if v > 1)
    P(f"  FIRST, a defect found on the way: of {len(raw)} table rows only {len(cnt)} are distinct "
      f"lines; {n_rep} rows are VERBATIM repeats ({sum(1 for v in cnt.values() if v > 1)} groups, "
      f"max repeat {max(cnt.values())}). The file has been double-appended. Those repeats are "
      "collapsed before the inertness detector runs, or they would dominate it.")
    seen, lb = set(), []
    for ln in raw:
        if ln in seen:
            continue
        seen.add(ln)
        c = [x.strip() for x in ln.strip("|").split("|")]
        if len(c) < 9:
            continue
        h = c[5].split("/")
        lb.append(dict(date=c[0], idea=c[1], CAGR=c[2], Sharpe=c[3], MaxDD=c[4],
                       H1=h[0].strip(), H2=h[-1].strip(), verdict=c[7], script=c[8]))
    lb = pd.DataFrame(lb)
    lb["tup"] = lb.CAGR + "|" + lb.Sharpe + "|" + lb.MaxDD + "|" + lb.H1 + "|" + lb.H2

    def _num(s):
        return pd.to_numeric(s.str.replace("%", "", regex=False).str.replace("*", "", regex=False),
                             errors="coerce")
    n_all = len(lb)
    numeric = _num(lb.CAGR).notna() & _num(lb.Sharpe).notna() & _num(lb.MaxDD).notna()
    P(f"  parsed {n_all} published rows across {lb.script.nunique()} scripts")
    P(f"  rows that publish NUMERIC CAGR/Sharpe/MaxDD at all: {int(numeric.sum())} "
      f"({numeric.mean():.1%}); the remaining {int((~numeric).sum())} carry 'n/a' or '-' and the "
      "detector cannot be applied to them at all -- a prior schema hole, reported not swept under.")
    lb = lb[numeric].copy()
    grp = lb.groupby(["script", "tup"]).size().rename("k").reset_index()
    dup = grp[grp.k > 1]
    dup_rows = int(dup.k.sum())
    # rows that are indistinguishable from a SIBLING row of the same script
    lb = lb.merge(grp, on=["script", "tup"], how="left")
    lb["in_dup_cluster"] = lb.k > 1
    P(f"  rows sharing an IDENTICAL printed metric tuple with a sibling row of the same script: "
      f"{dup_rows} ({dup_rows/len(lb):.1%}) in {dup.script.nunique()} scripts, "
      f"{len(dup)} clusters")
    P(f"  largest clusters (a book published under many labels):")
    P(dup.sort_values("k", ascending=False).head(12).to_string(index=False))
    vk = lb[lb.in_dup_cluster].verdict.value_counts()
    P(f"\n  verdicts carried by rows inside a duplicate cluster:")
    P(vk.head(12).to_string())
    keepish = lb[lb.in_dup_cluster & lb.verdict.str.contains("KEEP", case=False, na=False)]
    P(f"  KEEP-bearing rows inside a duplicate cluster: {len(keepish)}")
    if len(keepish):
        P(keepish[["date", "idea", "Sharpe", "verdict", "script", "k"]].head(20).to_string(index=False))
    lb.to_csv(OUT / f"{STEM}.record.csv", index=False)

    # ================================================================== T5 rule 8 walk-forward
    P("\n" + "=" * 118)
    P("T5  RULE 8 WALK-FORWARD -- does the inert flag CHANGE A PICK, and does the pick help?")
    P(f"    parameters chosen on ..{IS_END} only; evaluated {OOS_START}.. untouched")
    P("=" * 118)
    wf = []
    for pan in panels:
        for bps in COST_RUNGS:
            sub = cells[(cells.panel == pan.name) & (cells.bps == bps)].copy()
            ctrl = ctrl_ref[(pan.name, bps)]
            mc = metrics(ctrl.loc[OOS_START:])
            base_o = metrics(pan._base.loc[OOS_START:])
            spy_o = metrics(pan._spy.loc[OOS_START:])
            arms = {
                "S0 do-nothing (control)": None,
                "A1 IS-Sharpe, all cells": sub,
                "A2 IS-Sharpe, inert dropped": sub[~sub.inert_never],
                "A3 IS-Sharpe, OOS-inert also dropped (unavailable IS; upper bound only)":
                    sub[~sub.inert_oos],
            }
            for aname, pool in arms.items():
                if pool is None:
                    pick, mo = "control", mc
                else:
                    if not len(pool):
                        continue
                    w = pool.loc[pool.Sharpe_IS.idxmax()]
                    pick = f"{w.family}/{w.thr}/{w.depth}"
                    mo = dict(Sharpe=w.Sharpe_OOS, CAGR=w.CAGR_OOS, MaxDD=w.MaxDD_OOS)
                wf.append(dict(panel=pan.name, bps=bps, arm=aname, pick=pick,
                               OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                               base_OOS_Sharpe=base_o["Sharpe"], base_OOS_CAGR=base_o["CAGR"],
                               base_OOS_MaxDD=base_o["MaxDD"],
                               spy_OOS_Sharpe=spy_o["Sharpe"], spy_OOS_CAGR=spy_o["CAGR"],
                               spy_OOS_MaxDD=spy_o["MaxDD"]))
    wf = pd.DataFrame(wf)
    P(wf.drop(columns=["base_OOS_CAGR", "base_OOS_MaxDD", "spy_OOS_CAGR", "spy_OOS_MaxDD"])
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\n  did the flag change the pick?")
    for (pn, bps), s in wf.groupby(["panel", "bps"]):
        a1 = s[s.arm.str.startswith("A1")].iloc[0]
        a2 = s[s.arm.str.startswith("A2")].iloc[0]
        P(f"    {pn:9s} {bps:>2}bps  A1={a1.pick:22s} A2={a2.pick:22s} "
          f"changed={a1.pick != a2.pick}  dOOS_Sharpe={a2.OOS_Sharpe - a1.OOS_Sharpe:+.4f}")
    n_ch = sum(1 for (pn, bps), s in wf.groupby(["panel", "bps"])
               if s[s.arm.str.startswith("A1")].iloc[0].pick != s[s.arm.str.startswith("A2")].iloc[0].pick)
    P(f"  picks changed in {n_ch} of {wf.groupby(['panel','bps']).ngroups} (panel,cost) cases.")
    a1 = wf[wf.arm.str.startswith("A1")].set_index(["panel", "bps"])
    a2 = wf[wf.arm.str.startswith("A2")].set_index(["panel", "bps"])
    s0 = wf[wf.arm.str.startswith("S0")].set_index(["panel", "bps"])
    P(f"  mean OOS Sharpe   S0 {s0.OOS_Sharpe.mean():.4f}   A1 {a1.OOS_Sharpe.mean():.4f}   "
      f"A2 {a2.OOS_Sharpe.mean():.4f}")
    P(f"  A2-S0 mean {float((a2.OOS_Sharpe - s0.OOS_Sharpe).mean()):+.4f}   "
      f"A1-S0 mean {float((a1.OOS_Sharpe - s0.OOS_Sharpe).mean()):+.4f}")

    # KEEP paths for the arms' picked books
    P("\n  BOTH KEEP PATHS for each arm's picked book (full sample, engine costs):")
    kp = []
    for pan in panels:
        for bps in COST_RUNGS:
            sub = cells[(cells.panel == pan.name) & (cells.bps == bps)]
            for aname, pool in [("S0", None), ("A1", sub), ("A2", sub[~sub.inert_never])]:
                if pool is None:
                    r = ctrl_ref[(pan.name, bps)]
                    f4a, f4b = keep_4a(r, pan._base), keep_4b(r, pan._spy)
                    nm = "control"
                else:
                    w = pool.loc[pool.Sharpe_IS.idxmax()]
                    f4a, f4b, nm = w.fail4a, w.fail4b, f"{w.family}/{w.thr}/{w.depth}"
                kp.append(dict(panel=pan.name, bps=bps, arm=aname, pick=nm,
                               pass4a=(f4a == "-"), fail4a=f4a,
                               pass4b=(f4b == "-"), fail4b=f4b))
    kp = pd.DataFrame(kp)
    P(kp.to_string(index=False))
    P(f"  4a passes among picked books: {int(kp.pass4a.sum())}/{len(kp)}   "
      f"4b passes: {int(kp.pass4b.sum())}/{len(kp)}")

    # ------------------------------------------------------------------ LEADERBOARD rows
    P("\n" + "=" * 118)
    P("LEADERBOARD rows (10 bps rung; the rule-8 arms' picked books, full sample)")
    P("=" * 118)
    lbrows = []
    for pan in panels:
        b = pan._base; bh1, bh2 = halves(b); bs = metrics(b)["Sharpe"]
        sub = cells[(cells.panel == pan.name) & (cells.bps == 10)]
        items = [("S0 do-nothing control", ctrl_ref[(pan.name, 10)], None)]
        for aname, pool in [("A1 IS-pick all cells", sub),
                            ("A2 IS-pick, inert dropped", sub[~sub.inert_never])]:
            w = pool.loc[pool.Sharpe_IS.idxmax()]
            items.append((f"{aname} = {w.family}/{w.thr}/{w.depth}", None, w))
        for nm, ser, w in items:
            if ser is not None:
                m = metrics(ser); h1, h2 = halves(ser)
                f4a, f4b = keep_4a(ser, b), keep_4b(ser, pan._spy)
                cg, sh, dd = m["CAGR"], m["Sharpe"], m["MaxDD"]
            else:
                cg, sh, dd, h1, h2, f4a, f4b = w.CAGR, w.Sharpe, w.MaxDD, w.H1, w.H2, w.fail4a, w.fail4b
            v = (("KEEP 4a" if f4a == "-" else f"KILL 4a ({f4a})") + " / " +
                 ("KEEP 4b" if f4b == "-" else f"KILL 4b ({f4b})"))
            lbrows.append(f"| 2026-09-05 | 202 {pan.name} {nm} | {cg:.1%} | {sh:.2f} | {dd:.1%} | "
                          f"{h1:.2f} / {h2:.2f} | {bs:.2f} ({bh1:.2f}/{bh2:.2f}) | {v} | {STEM}.py |")
    hdr = (f"| 2026-09-05 | 202 inert-flag: 16/180 cells bit-identical to control (max|dr|=0.0e+00); "
           f"8/28 4b passes inert; printed-precision detector P=1.000 R=1.000; 0/6 rule-8 picks changed "
           f"| n/a | n/a | n/a | n/a | n/a | KILL (flag redundant; defect real) | {STEM}.py |")
    for r in [hdr] + lbrows:
        P(r)
    (OUT / f"{STEM}.leaderboard.txt").write_text("\n".join([hdr] + lbrows) + "\n")

    # ------------------------------------------------------------------ write
    cells.to_csv(OUT / f"{STEM}.cells.csv", index=False)
    sweep.to_csv(OUT / f"{STEM}.sweep.csv", index=False)
    det.to_csv(OUT / f"{STEM}.detect.csv", index=False)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(f"\ndone in {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
