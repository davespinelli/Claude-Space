#!/usr/bin/env python3
"""Idea 1666 (lane B, 2026-09-19): does the BAND's TIMING survive an IN-BAND-SHARE-MATCHED
PLACEBO GATE?

Parent: 1674 found the live 200d +/-3% band beats a static equity/SHY mix on U56, and 1670
found the Sharpe half of that is a U56 fact while the drawdown half holds 60/60 on all three
panels.  Either way the credit has only ever been shown against a book that is out of the
market a DIFFERENT amount of the time.  This run holds HOW OFTEN fixed and destroys WHEN.

CELL   = the live book, RULES v2 verbatim: every priced tradable name inside the 200d +/-3%
         band (hysteresis) at gross/N of NAV, gross = 0.75, gated weight to CASH, weekly.
NULLS  (all three match each name's IN-BAND SHARE over its OWN priced days, exactly or to tol):
  ROT-COM  one common circular shift k, applied to every name WITHIN its own priced sub-index.
           Preserves each name's share AND run-length structure AND the cross-name synchrony
           of the gate; destroys only the alignment to the calendar/price path.  *PRIMARY*.
  ROT-IND  an independent circular shift per name.  Preserves share + runs, destroys synchrony.
  IID      Bernoulli(p_i) per priced day, rejection-sampled until |share - p_i| <= tol.
           Preserves share only; destroys runs and synchrony.

TWO TUNED PARAMETERS, and only two: seed count S in {10, 25, 50} and share-match tolerance
tol in {0.005, 0.02, 0.05}.  Band width is PINNED at the live 0.03 and gross at the live 0.75 --
neither is tuned here.  All 9 grid points are published for every panel, null kind and cost rung.

PRE-REGISTERED BAR (written before any number was read).  The band's TIMING is established only
if, on the PRIMARY null ROT-COM at the live 10 bps rung with S = 50:
  (i)   empirical p(Sharpe) = share of draws with placebo Sharpe >= cell Sharpe is <= 0.05
        on >= 2 of 3 panels, FULL;
  (ii)  the same holds OOS (2017-2026, read once);
  (iii) empirical p(MaxDD) = share of draws at least as shallow as the cell is <= 0.05
        on >= 2 of 3 panels, FULL.
Fewer than all three -> the "WHEN" claim is NOT established by this test and the band's credit
is a HOW-OFTEN (exposure) claim, already known to be reproduced by a constant de-gross.

Protocol: 10 bps live rung (0/25/50 also published), weights at close t applied t+1 (engine),
long-only, no leverage, both KEEP paths, rule 8 walk-forward with 2017-2026 read ONCE.
Survivorship (rule 9): U56/B136 are CURRENT constituent lists and SMALL is a current sub-$2B
screen carried back to 2010, so every absolute level is an UPPER BOUND; the cell-vs-placebo
contrast is between two gatings of the SAME names on the SAME days and is not something the
bias can manufacture.
"""
import sys, zlib
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, band_state, rules_v2_weights   # noqa
from engine import backtest, metrics                               # noqa

BAND, GROSS, FREQ = 0.03, 0.75, "W"
RUNGS = [0, 10, 25, 50]
SEEDS_MAX, S_GRID, TOL_GRID = 50, [10, 25, 50], [0.005, 0.02, 0.05]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
OUT = Path(__file__).resolve().parent / "out"
LOG = []


def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def gate_line(name, val, ok, note=""):
    say(f"GATE {name}: {val}  {'PASS' if ok else 'FAIL'}  {note}")
    return dict(gate=name, value=str(val), pass_=bool(ok), note=note)


# ------------------------------------------------------------------ panels
def build_panels():
    P = {}
    u = load_universe();  P["U56"] = (u, list(u.columns))
    b = load_universe(broad=True); P["B136"] = (b, list(b.columns))
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in sm.columns if c not in bad and c != "SPY"]
    P["SMALL"] = (sm[keep + ["SPY"]], keep)
    say(f"panels: " + ", ".join(f"{k} {v[0].shape[0]}d x {len(v[1])} tradable" for k, v in P.items())
        + f"   (SMALL dropped {len(bad)} names with max_1d_move >= 1.0)")
    return P


# ------------------------------------------------------------------ gates
def priced_mask(px, cols, start):
    """Eligible rows for the share match and the permutation: priced AND inside the SCORED
    window.  Restricting to the scored window matters: `band_state` is structurally OUT for a
    name's first 200 closes, which sit in the warm-up the cell is never charged for, and a
    permutation over the whole history would drag those rows INTO the window and hand the null
    a LOWER exposure than the cell."""
    return (px[cols].notna().values & np.asarray(px.index >= start).reshape(-1, 1))


def rotate_within_priced(G, M, shifts):
    """G, M boolean (T x N) gate / priced masks.  Circularly shift each column's gate WITHIN
    its own priced rows by shifts[j].  Exactly preserves every column's in-band priced-day
    count, and its run-length structure inside the priced span."""
    out = np.zeros_like(G)
    for j in range(G.shape[1]):
        rows = np.flatnonzero(M[:, j])
        if rows.size == 0: continue
        out[rows, j] = np.roll(G[rows, j], int(shifts[j]) % rows.size)
    return out


def iid_gate(G, M, rng, tol):
    """Bernoulli(p_j) on each column's priced days, rejection-sampled to |share - p_j| <= tol
    (<= 40 tries, then forced to exactly round(p_j * n_j) random priced days)."""
    out = np.zeros_like(G); forced = 0
    for j in range(G.shape[1]):
        rows = np.flatnonzero(M[:, j]); n = rows.size
        if n == 0: continue
        p = G[rows, j].mean()
        for _ in range(40):
            d = rng.random(n) < p
            if abs(d.mean() - p) <= tol: break
        else:
            k = int(round(p * n)); d = np.zeros(n, bool)
            d[rng.choice(n, size=k, replace=False)] = True; forced += 1
        out[rows, j] = d
    return out, forced


def weights_from_gate(px, cols, gate_bool, scale=1.0):
    """RULES v2 construction with an arbitrary gate: gross/N over priced tradables, gated
    weight to CASH (never re-spread).  `scale` is a CONSTANT (time-invariant) multiplier used
    only to exposure-match a null to the cell; a constant cannot create or destroy timing."""
    e = px[cols].notna().astype(float)
    ew = GROSS * scale * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    w = ew.where(pd.DataFrame(gate_bool, index=px.index, columns=cols), 0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


# ------------------------------------------------------------------ scoring
def run_arm(px, w):
    """One cost-0 backtest; every rung is then EXACT (idea 1586: r(c) = r_gross - turn*c/1e4)."""
    res = backtest(px, w, cost_bps=0.0, freq=FREQ)
    return res["returns"], res["turnover"], w.sum(axis=1)


def windows(idx):
    start = idx[260]
    full = (idx >= start)
    f = idx[full]; h = len(f) // 2
    return dict(FULL=(f[0], f[-1]), H1=(f[0], f[h - 1]), H2=(f[h], f[-1]),
                IS=(f[0], pd.Timestamp(IS_END)), OOS=(pd.Timestamp(OOS_START), f[-1]))


def score(r_gross, turn, c, wins):
    r = r_gross - turn * c / 1e4
    out = {}
    for k, (a, b) in wins.items():
        seg = r.loc[a:b]
        m = metrics(seg)
        out[k] = (m["CAGR"], m["Sharpe"], m["MaxDD"])
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    P = build_panels(); gates = []; rows = []; cellrows = []; SPYM = {}; pathrows = []

    # engine identity check: the exact two-rung reconstruction used everywhere below
    u, ucols = P["U56"]
    wcell_u = weights_from_gate(u, ucols, band_state(u[ucols], BAND).values)
    r0, t0, _ = run_arm(u, wcell_u)
    direct = backtest(u, wcell_u, cost_bps=10.0, freq=FREQ)["returns"]
    err = float((r0 - t0 * 10 / 1e4 - direct).abs().max())
    gates.append(gate_line("cost_reconstruction_exact", f"{err:.3e}", err < 1e-12,
                           "r(c) = r_gross - turnover*c/1e4 reproduces the engine exactly"))
    # the cell IS the live book on U56
    liveerr = float((wcell_u - rules_v2_weights(u, BAND, GROSS).reindex(columns=u.columns).fillna(0.0)).abs().max().max())
    gates.append(gate_line("cell_is_live_RULES_v2_on_U56", f"{liveerr:.3e}", liveerr < 1e-12,
                           "cell weights identical to baseline.rules_v2_weights on U56"))

    for pan, (px, cols) in P.items():
        wins = windows(px.index)
        G = band_state(px[cols], BAND).values
        M = priced_mask(px, cols, wins['FULL'][0])
        shares = np.array([G[M[:, j], j].mean() if M[:, j].any() else np.nan for j in range(len(cols))])
        say(f"\n=== {pan} === in-band share per name: mean {np.nanmean(shares):.4f} "
            f"[{np.nanmin(shares):.3f}, {np.nanmax(shares):.3f}], {len(cols)} names, "
            f"{wins['FULL'][0].date()}..{wins['FULL'][1].date()}")

        wcell = weights_from_gate(px, cols, G)
        rc, tc, gc = run_arm(px, wcell)
        spy = px["SPY"].pct_change().fillna(0.0)
        cell_turn_yr = float(tc.loc[wins["FULL"][0]:].sum() / (len(tc.loc[wins["FULL"][0]:]) / 252))

        # ---- the cell as a capital book: both KEEP paths at every rung
        for c in RUNGS:
            s = score(rc, tc, c, wins)
            sp = {k: (lambda m: (m["CAGR"], m["Sharpe"], m["MaxDD"]))(metrics(spy.loc[a:bb]))
                  for k, (a, bb) in wins.items()}
            SPYM[pan] = sp
            keep4a = "TIE (the cell IS RULES v2 on this panel; 4a is adjudicated below for the NULLS vs the cell)"
            keep4b = (s["H1"][1] > sp["H1"][1] and s["H2"][1] > sp["H2"][1] and s["OOS"][1] > sp["OOS"][1]
                      and s["FULL"][2] >= 0.60 * sp["FULL"][2] and s["OOS"][2] >= 0.60 * sp["OOS"][2]
                      and s["FULL"][0] >= 0.70 * sp["FULL"][0] and s["OOS"][0] >= 0.70 * sp["OOS"][0])
            cellrows.append(dict(panel=pan, cost=c, turnover_yr=cell_turn_yr,
                                 **{f"cell_{k}_{m}": s[k][i] for k in wins for i, m in enumerate("CAGR Sharpe MaxDD".split())},
                                 **{f"spy_{k}_{m}": sp[k][i] for k in wins for i, m in enumerate("CAGR Sharpe MaxDD".split())},
                                 keep4a=keep4a, keep4b=keep4b))
            say(f"  CELL {pan} @{c:>2}bps  FULL {s['FULL'][0]:.2%} / {s['FULL'][1]:.4f} / {s['FULL'][2]:.2%}"
                f"  halves {s['H1'][1]:.4f}/{s['H2'][1]:.4f}  OOS {s['OOS'][0]:.2%} / {s['OOS'][1]:.4f} / {s['OOS'][2]:.2%}"
                f"   SPY FULL {sp['FULL'][1]:.4f} OOS {sp['OOS'][1]:.4f}   4a {keep4a}  4b {keep4b}")

        # ---- placebo draws
        draws = {}   # (kind, tol) -> list over seeds of dict(rung -> window -> tuple)
        forced_tot = {}
        specs = [("ROT-COM", None), ("ROT-IND", None)] + [("IID", t) for t in TOL_GRID]
        for kind, tol in specs:
            key = (kind, tol); draws[key] = []; forced_tot[key] = 0
            expo, scales = [], []
            for i in range(SEEDS_MAX):
                rng = np.random.default_rng([zlib.crc32(pan.encode()), zlib.crc32(kind.encode()),
                                             int((tol or 0) * 1e4), i])   # deterministic
                if kind == "ROT-COM":
                    k = rng.integers(0, 10**6); gp = rotate_within_priced(G, M, np.full(len(cols), k))
                elif kind == "ROT-IND":
                    gp = rotate_within_priced(G, M, rng.integers(0, 10**6, len(cols)))
                else:
                    gp, f = iid_gate(G, M, rng, tol); forced_tot[key] += f
                w = weights_from_gate(px, cols, gp)
                rg, tg, gg = run_arm(px, w)
                g_cell = float(gc.loc[wins["FULL"][0]:].mean())
                sc = g_cell / float(gg.loc[wins["FULL"][0]:].mean())
                if abs(sc - 1.0) > 1e-9:            # exposure-match with ONE constant
                    w = weights_from_gate(px, cols, gp, sc)
                    rg, tg, gg = run_arm(px, w)
                scales.append(sc)
                expo.append(float(gg.loc[wins["FULL"][0]:].mean()))
                draws[key].append({c: score(rg, tg, c, wins) for c in RUNGS})
            de = abs(np.mean(expo) - float(gc.loc[wins["FULL"][0]:].mean()))
            say(f"  {pan} {kind}{'' if tol is None else f' tol={tol}'}: {SEEDS_MAX} draws, "
                f"mean gross {np.mean(expo):.4f} vs cell {float(gc.loc[wins['FULL'][0]:].mean()):.4f} "
                f"(|d| {de:.5f}), forced {forced_tot[key]}, exposure-match scalar mean "
                f"{np.mean(scales):.4f} [{min(scales):.4f}, {max(scales):.4f}], max per-day "
                f"gross {GROSS * max(scales):.3f} (no leverage)")
            gates.append(gate_line(f"exposure_matched_{pan}_{kind}_{tol}", f"{de:.5f}", de < 0.002,
                                   "mean daily gross of the null matches the cell"))

        # ---- grid: all (S, tol) x kind x rung x window
        for kind, tol in specs:
            key = (kind, tol)
            for S in S_GRID:
                for c in RUNGS:
                    for wname in ("FULL", "H1", "H2", "IS", "OOS"):
                        cellv = score(rc, tc, c, wins)[wname]
                        pv = np.array([d[c][wname] for d in draws[key][:S]])  # S x 3
                        pS, pDD, pC = pv[:, 1], pv[:, 2], pv[:, 0]
                        rows.append(dict(
                            panel=pan, kind=kind, tol=(tol if tol is not None else 'n/a'), S=S, cost=c, window=wname,
                            cell_CAGR=cellv[0], cell_Sharpe=cellv[1], cell_MaxDD=cellv[2],
                            null_Sharpe_mean=pS.mean(), null_Sharpe_p05=np.percentile(pS, 5),
                            null_Sharpe_p50=np.percentile(pS, 50), null_Sharpe_p95=np.percentile(pS, 95),
                            null_MaxDD_mean=pDD.mean(), null_CAGR_mean=pC.mean(),
                            dSharpe=cellv[1] - pS.mean(), dMaxDD=cellv[2] - pDD.mean(),
                            p_Sharpe=float((pS >= cellv[1]).mean()),   # share of nulls >= cell
                            p_MaxDD=float((pDD >= cellv[2]).mean())))  # share at least as shallow
                    # per-draw KEEP verdicts: 4a against the CELL, 4b against SPY
                    cs = score(rc, tc, c, wins); sp = SPYM[pan]
                    n4a = n4b = 0
                    for d in draws[key][:S]:
                        a_ok = (d[c]["H1"][1] > cs["H1"][1] and d[c]["H2"][1] > cs["H2"][1]
                                and d[c]["FULL"][2] >= cs["FULL"][2])
                        b_ok = (d[c]["H1"][1] > sp["H1"][1] and d[c]["H2"][1] > sp["H2"][1]
                                and d[c]["OOS"][1] > sp["OOS"][1]
                                and d[c]["FULL"][2] >= 0.60 * sp["FULL"][2] and d[c]["OOS"][2] >= 0.60 * sp["OOS"][2]
                                and d[c]["FULL"][0] >= 0.70 * sp["FULL"][0] and d[c]["OOS"][0] >= 0.70 * sp["OOS"][0])
                        n4a += a_ok; n4b += b_ok
                    pathrows.append(dict(panel=pan, kind=kind, tol=(tol if tol is not None else 'n/a'), S=S, cost=c,
                                         null_4a_share=n4a / S, null_4b_share=n4b / S))

    grid = pd.DataFrame(rows); cells = pd.DataFrame(cellrows)
    paths = pd.DataFrame(pathrows).drop_duplicates(subset=["panel", "kind", "tol", "S", "cost"])
    paths.to_csv(OUT / "2026-09-19_in-band-share-matched-placebo-gate_B_keeppaths.csv", index=False)
    grid.to_csv(OUT / "2026-09-19_in-band-share-matched-placebo-gate_B_grid.csv", index=False)
    cells.to_csv(OUT / "2026-09-19_in-band-share-matched-placebo-gate_B_cell.csv", index=False)
    say(f"\nALL GRID POINTS: {len(grid)} rows written "
        f"({grid.panel.nunique()} panels x {grid.kind.nunique()} null kinds x {len(S_GRID)} S "
        f"x {len(RUNGS)} rungs x 5 windows; tol grid {TOL_GRID} on IID)")

    # ---------------- printed grid: every (kind, tol, S) at every rung, FULL and OOS
    for pan in P:
        say(f"\n---- {pan}: p = share of {'S'} draws whose Sharpe >= the cell's (low = the band's timing matters)")
        sub = grid[(grid.panel == pan) & (grid.window.isin(["FULL", "OOS"]))]
        piv = sub.pivot_table(index=["kind", "tol", "S"], columns=["window", "cost"],
                              values="p_Sharpe", dropna=False)
        say(piv.to_string(float_format=lambda x: f"{x:.2f}", na_rep="-"))
        say(f"---- {pan}: dSharpe = cell - null mean")
        piv2 = sub.pivot_table(index=["kind", "tol", "S"], columns=["window", "cost"],
                               values="dSharpe", dropna=False)
        say(piv2.to_string(float_format=lambda x: f"{x:+.4f}", na_rep="-"))
        say(f"---- {pan}: p_MaxDD = share of draws at least as shallow as the cell")
        piv3 = sub.pivot_table(index=["kind", "tol", "S"], columns=["window", "cost"],
                               values="p_MaxDD", dropna=False)
        say(piv3.to_string(float_format=lambda x: f"{x:.2f}", na_rep="-"))

    # ---------------- RULE 8: choose (S, tol) on IS ONLY, read OOS once
    say("\n==== RULE 8 WALK-FORWARD: (S, tol) chosen on rows <= 2016-12-31 ONLY, 2017-2026 read once ====")
    is_tbl = grid[(grid.window == "IS") & (grid.cost == 10) & (grid.kind == "IID")]
    pick = is_tbl.loc[is_tbl.groupby("panel").null_Sharpe_mean.idxmax(), ["panel", "S", "tol", "null_Sharpe_mean"]]
    say("IS-only chooser = argmax over the 9 (S, tol) cells of the NULL's mean IS Sharpe "
        "(the calibration most adverse to the cell); ROT-COM / ROT-IND are tol-invariant by "
        "construction so their grid is over S alone.")
    say(pick.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    wf = []
    for _, r in pick.iterrows():
        for kind in ("ROT-COM", "ROT-IND", "IID"):
            sel = grid[(grid.panel == r.panel) & (grid.kind == kind) & (grid.S == r.S) &
                       (grid.window == "OOS") & (grid.cost == 10) &
                       ((grid.tol == r.tol) if kind == "IID" else (grid.tol == 'n/a'))]
            if len(sel) != 1: continue
            s = sel.iloc[0]
            wf.append(dict(panel=r.panel, kind=kind, S=int(r.S), tol=r.tol,
                           cell_OOS_Sharpe=s.cell_Sharpe, null_OOS_Sharpe=s.null_Sharpe_mean,
                           dSharpe=s.dSharpe, p_Sharpe=s.p_Sharpe,
                           cell_OOS_CAGR=s.cell_CAGR, null_OOS_CAGR=s.null_CAGR_mean,
                           cell_OOS_MaxDD=s.cell_MaxDD, null_OOS_MaxDD=s.null_MaxDD_mean,
                           p_MaxDD=s.p_MaxDD))
    wfd = pd.DataFrame(wf)
    say(wfd.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    wfd.to_csv(OUT / "2026-09-19_in-band-share-matched-placebo-gate_B_rule8.csv", index=False)

    # ---------------- the pre-registered bar
    say("\n==== PRE-REGISTERED BAR (ROT-COM, 10 bps, S = 50) ====")
    prim = grid[(grid.kind == "ROT-COM") & (grid.S == 50) & (grid.cost == 10)]
    i_full = prim[prim.window == "FULL"]; i_oos = prim[prim.window == "OOS"]
    n1 = int((i_full.p_Sharpe <= 0.05).sum()); n2 = int((i_oos.p_Sharpe <= 0.05).sum())
    n3 = int((i_full.p_MaxDD <= 0.05).sum())
    for nm, tb, col in (("FULL Sharpe", i_full, "p_Sharpe"), ("OOS Sharpe", i_oos, "p_Sharpe"),
                        ("FULL MaxDD", i_full, "p_MaxDD")):
        say(f"  {nm}: " + "  ".join(f"{r.panel} p={getattr(r, col):.2f}" for r in tb.itertuples()))
    g1 = gate_line("bar_i_FULL_Sharpe_p<=0.05_on>=2of3", f"{n1}/3", n1 >= 2)
    g2 = gate_line("bar_ii_OOS_Sharpe_p<=0.05_on>=2of3", f"{n2}/3", n2 >= 2)
    g3 = gate_line("bar_iii_FULL_MaxDD_p<=0.05_on>=2of3", f"{n3}/3", n3 >= 2)
    gates += [g1, g2, g3]
    verdict = "TIMING ESTABLISHED" if (g1["pass_"] and g2["pass_"] and g3["pass_"]) else "KILL"
    say(f"\nVERDICT: {verdict}  (bar (i) {n1}/3, (ii) {n2}/3, (iii) {n3}/3; all three required)")
    say("\n==== BOTH KEEP PATHS FOR THE NULLS (share of draws clearing each path) ====")
    say(paths.pivot_table(index=["kind", "tol", "S"], columns=["panel", "cost"],
                          values="null_4a_share").to_string(float_format=lambda x: f"{x:.2f}", na_rep="-"))
    say("  (4b share)")
    say(paths.pivot_table(index=["kind", "tol", "S"], columns=["panel", "cost"],
                          values="null_4b_share").to_string(float_format=lambda x: f"{x:.2f}", na_rep="-"))
    say("KEEP paths for the CELL book itself: " +
        ", ".join(f"{r.panel}@{r.cost}bps 4a={r.keep4a} 4b={r.keep4b}" for r in cells.itertuples()))

    pd.DataFrame(gates).to_csv(OUT / "2026-09-19_in-band-share-matched-placebo-gate_B_gates.csv", index=False)
    (OUT / "2026-09-19_in-band-share-matched-placebo-gate_B_log.txt").write_text("\n".join(LOG))
    return verdict


if __name__ == "__main__":
    main()
