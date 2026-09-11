#!/usr/bin/env python3
"""Idea 786 (lane B, 2026-09-11) — is the U56 CAGR-FLOOR GAP a DELISTING artefact?

Idea 787 killed the record's whole standing 4b shelf against an equal-weight basket of the book's
own panel (0 of 82), and named ONE leg as binding on the tightest-drawdown book: the CAGR FLOOR.
The U56 RULES v2 band book at gross 1.00 runs 11.55% against a floor of 0.70 x 17.69% = 12.38%,
i.e. it misses by **-0.83 pp/yr** (-0.14 pp OOS). Idea 787's own caveat 1 says the bar is the most
survivorship-exposed object in the record — it holds every CURRENT constituent at full weight — so
a delisting-complete panel would lower the bar and could revive the shelf.

This run bounds that. Two tuned parameters, every grid point reported: **(drag model, panel)**.

  DRAG MODEL 1 — FLAT: a constant arithmetic survivorship drag d (pp/yr, applied as d/252 per day)
    charged to the equal-weight BAR, and to the BOOK at a share phi of the same drag. d and phi are
    REPORTING ladders, not tuned: the deliverable is the inversion d*(phi), the drag that closes the
    floor, over the whole ladder. phi matters because the book trades the SAME survivorship-biased
    panel as the bar: a drag charged to both moves the gap by -(1-phi/0.70) x 0.70 x d, so a SHARED
    drag WIDENS the miss and only a bar-heavier drag can close it.

  DRAG MODEL 2 — HAZARD: synthetic delistings injected into the PRICE PANEL itself, then BOTH the
    book and the bar are rebuilt on the augmented panel, so phi is MEASURED instead of assumed. A
    phantom name clones a real donor's path, then declines geometrically to a terminal delisting
    return L over the last W trading days and goes NaN (delisted; the bar respreads, the band book's
    gate may exit first — that gate is the whole reason phi could be < 1). Ladders: annual hazard h,
    decline window W, terminal return L, seed.

  Then the INVERSION: the required bar drag is converted to the (hazard, delisting-return) pairs
  that would produce it, so the answer can be read against delisting-return estimates.

PROTOCOL: 10 bps per unit turnover, next-day execution (engine applies weights at t+1), no
shorting, no leverage (gross <= 1.00) in the headline, 260-row warm-up skip, rule 8 walk-forward
throughout (gross picked on IS <= 2016-12-31 alone, 2017-01-01 -> end read ONCE), both KEEP paths.
SPY is held OUT of every book and bar as a pure benchmark column (idea 787's SPY-free frame).

NO INTERNET in this sandbox: no delisting-return or hazard figure is fetched. Literature anchors
are quoted as UNVERIFIED and are used only as labels on L rungs that are reported in full anyway.
The caches are current-constituent panels, so no internal hazard estimate is possible either; the
deliverable is the required (h, L) curve, not a claim about the true h.

Outputs (all beside this script):
  *.gates.csv        the eight pre-registered gates
  *.grid.csv         DRAG MODEL 1: every (panel, bar form, gross, d, phi) point + 4b legs
  *.inversion.csv    required bar drag d* and the (h, L) pairs that deliver it
  *.hazard.csv       DRAG MODEL 2: every (panel, h, W, L, seed, gross) point, measured phi
  *.walkforward.csv  rule 8: gross picked on IS alone, OOS read once, under BOTH drag models
  *.result.md        the answer
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa: E402

HERE = Path(__file__).resolve().parent
STEM = Path(__file__).stem
COST = 10.0
WARMUP = 260
IS_END = pd.Timestamp("2016-12-31")
OOS_START = pd.Timestamp("2017-01-01")
GROSS_LADDER = [0.50, 0.60, 0.70, 0.75, 0.80, 0.90, 1.00]

# ---- reporting ladders (NOT tuned parameters: every rung is published) ----
D_LADDER = [0.0, 0.25, 0.50, 0.75, 1.00, 1.25, 1.50, 2.00, 3.00, 5.00]     # pp/yr of bar drag
PHI_LADDER = [0.00, 0.20, 0.40, 0.50, 0.60, 0.70, 0.80, 1.00]              # share charged to book
H_LADDER = [0.00, 0.01, 0.02, 0.03, 0.05]                                  # annual delisting hazard
W_LADDER = [21, 63, 126, 252, 504]                                         # decline window (days)
L_LADDER = [(-0.30, "Shumway-1997-style NYSE/AMEX anchor (UNVERIFIED, not fetched)"),
            (-0.55, "Shumway-Warther-1999-style Nasdaq anchor (UNVERIFIED, not fetched)"),
            (-1.00, "total loss (arithmetic worst case, no citation needed)")]
SEEDS = [0, 1, 2]
BASE_W, BASE_L, BASE_SEED = 252, -0.30, 0


# ---------------------------------------------------------------- fast backtester (gated vs engine)
def fast_backtest(px: pd.DataFrame, w: pd.DataFrame, cost_bps=COST, freq="W") -> dict:
    """Numpy transcription of engine.backtest (idea 787's, unchanged). Same drift, t+1, cost model."""
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n = len(px)
    held = np.zeros_like(rets)
    turn = np.zeros(n)
    cur = np.zeros(px.shape[1])
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new.copy()
        held[i] = cur
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=px.index),
            "turnover": pd.Series(turn, index=px.index)}


# ---------------------------------------------------------------- books (idea 787's, unchanged)
def _priced(px):
    return px.notna().astype(float)


def _respread(mask_df: pd.DataFrame, gross: float) -> pd.DataFrame:
    m = mask_df.astype(float)
    return gross * m.div(m.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def b_band_dg(px, g):
    """RULES v2 exactly: band gate, g/N over ALL priced names, gated weight -> CASH."""
    e = _priced(px)
    ew = g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, 0.03), 0.0)


def b_ewbar(px, g=1.00):
    """B_EW — idea 742/787's bar: equal-weight the panel's own tradables, gross 1.00."""
    return _respread(px.notna(), g)


# ---------------------------------------------------------------- drag model 1: FLAT
def flat_drag(r: pd.Series, d_pp: float) -> pd.Series:
    """Charge d_pp percentage points per year as a constant arithmetic daily deduction."""
    return r - (d_pp / 100.0) / 252.0


# ---------------------------------------------------------------- drag model 2: HAZARD
def augment_panel(frame: pd.DataFrame, h: float, W: int, L: float, seed: int) -> pd.DataFrame:
    """Return frame + phantom delisted names, giving an annual delisting hazard of h.

    A current-constituent panel of N survivors over T years implies a delisting-complete start
    count N0 = N / (1-h)^T, so D = N0 - N names died inside the window. Each phantom clones a real
    donor's returns, then decays geometrically to a cumulative return L over its last W trading
    days, then goes NaN (delisted -> the bar respreads out of it, the band book may have exited
    earlier). Death dates are spread deterministically across the window.
    """
    if h <= 0:
        return frame
    idx = frame.index
    T = len(idx) / 252.0
    N = frame.shape[1]
    D = int(round(N / (1.0 - h) ** T - N))
    if D <= 0:
        return frame
    rng = np.random.default_rng(seed)
    donors = rng.permutation(frame.columns.to_numpy())
    lo, hi = WARMUP + W + 21, len(idx) - 21                     # death must follow warm-up, precede end
    deaths = np.linspace(lo, hi, D).round().astype(int)
    deaths = (deaths + rng.integers(-10, 11, D)).clip(lo, hi)
    cols = {}
    for j in range(D):
        donor = donors[j % len(donors)]
        s = frame[donor].astype(float).copy()
        t_d = int(deaths[j])
        path = s.to_numpy(copy=True)
        start = max(0, t_d - W)
        base = path[start]
        if not np.isfinite(base) or base <= 0:                  # donor not priced yet: skip this phantom
            continue
        step = (1.0 + L) ** (1.0 / W)                           # geometric slide to (1+L) x base
        k = np.arange(1, t_d - start + 1)
        path[start + 1:t_d + 1] = base * step ** k
        path[t_d + 1:] = np.nan                                 # delisted
        cols[f"_DL{j:03d}_{donor}"] = pd.Series(path, index=idx)
    if not cols:
        return frame
    return pd.concat([frame, pd.DataFrame(cols, index=idx)], axis=1)


# ---------------------------------------------------------------- metric helpers
def full_row(r):
    h = len(r) // 2
    m = metrics(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def oos_row(r):
    m = metrics(r.loc[OOS_START:])
    return dict(oos_CAGR=m["CAGR"], oos_Sharpe=m["Sharpe"], oos_MaxDD=m["MaxDD"])


def both(r):
    return {**full_row(r), **oos_row(r)}


def is_sharpe(r):
    return metrics(r.loc[:IS_END])["Sharpe"]


def path_4a(cand, base):
    legs = {"H1": cand["H1"] > base["H1"], "H2": cand["H2"] > base["H2"],
            "MaxDD": cand["MaxDD"] >= base["MaxDD"]}
    return all(legs.values()), ",".join(k for k, v in legs.items() if not v)


def path_4b(cand, bar):
    """PROTOCOL 4b: Sharpe > bar in BOTH halves AND OOS, MaxDD <= 60% of bar's, CAGR >= 70%."""
    legs = {"H1": cand["H1"] > bar["H1"], "H2": cand["H2"] > bar["H2"],
            "OOS": cand["oos_Sharpe"] > bar["oos_Sharpe"],
            "DD": cand["MaxDD"] >= 0.60 * bar["MaxDD"],
            "CAGR": cand["CAGR"] >= 0.70 * bar["CAGR"]}
    return all(legs.values()), ",".join(k for k, v in legs.items() if not v)


def cagr_slack(cand, bar, key="CAGR"):
    """pp/yr by which the book clears (+) or misses (-) the 4b CAGR floor."""
    ck, bk = (key, key) if key == "CAGR" else ("oos_CAGR", "oos_CAGR")
    return 100.0 * (cand[ck] - 0.70 * bar[bk])


# ---------------------------------------------------------------- main
def main():
    out = []

    def log(s=""):
        print(s)
        out.append(str(s))

    gates, grid, inv_rows, haz_rows, wf_rows = [], [], [], [], []

    log(f"# {STEM}\n")
    log("DRAG MODEL 1 = FLAT (assumed drag, phi ladder) | DRAG MODEL 2 = HAZARD (injected "
        "delistings, phi MEASURED). Tuned params: (drag model, panel). Everything else is a "
        "published ladder.\n")

    panels = {}
    for broad in (False, True):
        pname = "B136" if broad else "U56"
        px = load_universe(broad=broad)
        frame = px[[c for c in px.columns if c != "SPY"]].copy()
        start = px.index[WARMUP]
        panels[pname] = (px, frame, start)
        log(f"=== {pname}: {frame.shape[1]} tradables, {px.index[0].date()}..{px.index[-1].date()}, "
            f"scored from {start.date()}, {len(px.index)/252:.2f} yrs")

    # ------------------------------------------------------------ GATES
    log("\n## GATES (pre-registered, printed before any answer)\n")
    px, frame, start = panels["U56"]

    # G1 fast vs engine, returns AND turnover
    for nm, w, fq in [("BAND-DG g0.75", b_band_dg(frame, 0.75), "W"),
                      ("EW bar g1.00", b_ewbar(frame, 1.00), "W")]:
        f = fast_backtest(frame, w, COST, fq)
        e = engine_backtest(frame, w, cost_bps=COST, freq=fq)
        v = max(float(np.nanmax(np.abs(f["returns"].values - e["returns"].values))),
                float(np.nanmax(np.abs(f["turnover"].values - e["turnover"].values))))
        gates.append(dict(gate=f"G1 U56 fast vs engine [{nm}] max|dr|,|dturn|", value=v, bar=1e-12,
                          passed=v < 1e-12))

    # G2 b_band_dg(0.75) IS baseline.rules_v2_weights
    g2 = float(np.nanmax(np.abs(b_band_dg(px, 0.75).values - rules_v2_weights(px).values)))
    gates.append(dict(gate="G2 b_band_dg(0.75) == baseline.rules_v2_weights (full frame)",
                      value=g2, bar=0.0, passed=g2 == 0.0))

    # G3 cost-rung identity
    w0 = b_band_dg(frame, 0.75)
    r0, r25 = fast_backtest(frame, w0, 0.0, "W"), fast_backtest(frame, w0, 25.0, "W")
    g3 = float(np.nanmax(np.abs((r0["returns"] - r0["turnover"] * 25 / 1e4 - r25["returns"]).values)))
    gates.append(dict(gate="G3 U56 cost-rung identity r(25)=r(0)-turn*25/1e4", value=g3, bar=1e-12,
                      passed=g3 < 1e-12))

    # the three U56 objects idea 787 published, reproduced
    ewb = b_ewbar(frame, 1.00)
    bars_u56 = {"B_EW742": both(fast_backtest(frame, ewb, 0.0, "D")["returns"].loc[start:]),
                "B_EWW10": both(fast_backtest(frame, ewb, COST, "W")["returns"].loc[start:]),
                "B_SPY": both(px["SPY"].pct_change().fillna(0.0).loc[start:])}
    book_u56_g100 = both(fast_backtest(frame, b_band_dg(frame, 1.00), COST, "W")["returns"].loc[start:])

    def dev(got, want):
        return float(np.nanmax(np.abs(np.array(got) - np.array(want))))

    g4 = dev([bars_u56["B_EWW10"]["CAGR"], bars_u56["B_EWW10"]["Sharpe"], bars_u56["B_EWW10"]["MaxDD"]],
             [0.1769, 1.1237, -0.2909])
    gates.append(dict(gate="G4 U56 B_EWW10 == idea 787 (17.69% / 1.1237 / -29.09%)", value=g4,
                      bar=5e-4, passed=g4 < 5e-4))
    g5 = dev([bars_u56["B_EW742"]["CAGR"], bars_u56["B_EW742"]["Sharpe"], bars_u56["B_EW742"]["MaxDD"],
              bars_u56["B_EW742"]["oos_CAGR"], bars_u56["B_EW742"]["oos_Sharpe"]],
             [0.1794, 1.1357, -0.2887, 0.1864, 1.1448])
    gates.append(dict(gate="G5 U56 B_EW742 == idea 742/787 (17.94/1.1357/-28.87/OOS 18.64/1.1448)",
                      value=g5, bar=5e-4, passed=g5 < 5e-4))
    g6 = dev([book_u56_g100["CAGR"], book_u56_g100["Sharpe"], book_u56_g100["MaxDD"],
              book_u56_g100["H1"], book_u56_g100["H2"]],
             [0.1155, 1.2067, -0.1570, 1.2405, 1.1798])
    gates.append(dict(gate="G6 U56 BAND-DG g1.00 == standing memo line 3 (11.55/1.2067/-15.70/1.2405/1.1798)",
                      value=g6, bar=5e-4, passed=g6 < 5e-4))

    # G7 THE OBJECT UNDER TEST: idea 787's -0.83 pp/yr CAGR-floor miss, and -0.14 pp OOS
    miss_full = cagr_slack(book_u56_g100, bars_u56["B_EWW10"])
    miss_oos = cagr_slack(book_u56_g100, bars_u56["B_EWW10"], key="oos")
    g7 = dev([miss_full, miss_oos], [-0.83, -0.14])
    gates.append(dict(gate="G7 the gap under test: U56 g1.00 CAGR-floor miss vs B_EWW10 "
                          f"(-0.83 pp full / -0.14 pp OOS); got {miss_full:+.3f} / {miss_oos:+.3f}",
                      value=g7, bar=0.05, passed=g7 < 0.05))

    # G8 drag identity: d=0 is a no-op, and realised CAGR is strictly decreasing in d
    base_r = fast_backtest(frame, ewb, COST, "W")["returns"].loc[start:]
    g8a = float(np.nanmax(np.abs((flat_drag(base_r, 0.0) - base_r).values)))
    cg = [metrics(flat_drag(base_r, d))["CAGR"] for d in D_LADDER]
    g8b = float(np.min(np.diff(cg)))
    gates.append(dict(gate="G8a flat_drag(d=0) is a no-op", value=g8a, bar=0.0, passed=g8a == 0.0))
    gates.append(dict(gate="G8b bar CAGR strictly decreasing over the d ladder (max step)",
                      value=g8b, bar=0.0, passed=g8b < 0.0))

    gdf = pd.DataFrame(gates)
    gdf.to_csv(HERE / f"{STEM}.gates.csv", index=False)
    log(gdf.to_string(index=False))
    log(f"\nGATES: {int(gdf.passed.sum())} of {len(gdf)} PASS")
    if not gdf.passed.all():
        log("!! a gate failed — results below are NOT published as reproductions")

    # ------------------------------------------------------------ DRAG MODEL 1: FLAT
    log("\n## DRAG MODEL 1 — FLAT: the inversion d*(phi), every ladder point reported\n")
    for pname, (px_, frame_, start_) in panels.items():
        spy = px_["SPY"].pct_change().fillna(0.0).loc[start_:]
        ewb_ = b_ewbar(frame_, 1.00)
        bar_raw = {"B_EW742": fast_backtest(frame_, ewb_, 0.0, "D")["returns"].loc[start_:],
                   "B_EWW10": fast_backtest(frame_, ewb_, COST, "W")["returns"].loc[start_:]}
        base_live = both(fast_backtest(frame_, b_band_dg(frame_, 0.75), COST, "W")["returns"].loc[start_:])
        books = {g: fast_backtest(frame_, b_band_dg(frame_, g), COST, "W")["returns"].loc[start_:]
                 for g in GROSS_LADDER}
        log(f"--- {pname} | SPY {metrics(spy)['CAGR']:.2%}/{metrics(spy)['Sharpe']:.4f}/"
            f"{metrics(spy)['MaxDD']:.2%} | RULES v2 live g0.75 {base_live['CAGR']:.2%}/"
            f"{base_live['Sharpe']:.4f}/{base_live['MaxDD']:.2%}")
        for bname, br in bar_raw.items():
            for d in D_LADDER:
                bar = both(flat_drag(br, d))
                for phi in PHI_LADDER:
                    for g in GROSS_LADDER:
                        cand = both(flat_drag(books[g], d * phi))
                        ok4b, miss4b = path_4b(cand, bar)
                        ok4a, miss4a = path_4a(cand, base_live)
                        grid.append(dict(
                            model="FLAT", panel=pname, bar=bname, d_pp=d, phi=phi, gross=g,
                            CAGR=cand["CAGR"], Sharpe=cand["Sharpe"], MaxDD=cand["MaxDD"],
                            H1=cand["H1"], H2=cand["H2"], oos_CAGR=cand["oos_CAGR"],
                            oos_Sharpe=cand["oos_Sharpe"], oos_MaxDD=cand["oos_MaxDD"],
                            bar_CAGR=bar["CAGR"], bar_Sharpe=bar["Sharpe"], bar_MaxDD=bar["MaxDD"],
                            bar_oos_CAGR=bar["oos_CAGR"], bar_oos_Sharpe=bar["oos_Sharpe"],
                            cagr_slack_pp=cagr_slack(cand, bar),
                            oos_cagr_slack_pp=cagr_slack(cand, bar, key="oos"),
                            pass4b=ok4b, miss4b=miss4b, pass4a=ok4a, miss4a=miss4a))
        # the inversion, solved on the committed ladder AND analytically
        for bname, br in bar_raw.items():
            bar0 = both(br)
            for g in GROSS_LADDER:
                c0 = both(books[g])
                for key, bk, ck in (("full", "CAGR", "CAGR"), ("oos", "oos_CAGR", "oos_CAGR")):
                    gap = 100.0 * (c0[ck] - 0.70 * bar0[bk])
                    for phi in PHI_LADDER:
                        denom = 0.70 - phi
                        d_star = (-gap / denom) if denom > 1e-12 and gap < 0 else (
                            0.0 if gap >= 0 else np.inf)
                        inv_rows.append(dict(panel=pname, bar=bname, gross=g, window=key,
                                             gap_pp=gap, phi=phi,
                                             d_star_pp=d_star,
                                             feasible=np.isfinite(d_star)))
    gdf1 = pd.DataFrame(grid)
    gdf1.to_csv(HERE / f"{STEM}.grid.csv", index=False)
    idf = pd.DataFrame(inv_rows)
    idf.to_csv(HERE / f"{STEM}.inversion.csv", index=False)
    log(f"FLAT grid: {len(gdf1)} points written; 4b passes {int(gdf1.pass4b.sum())}, "
        f"4a passes {int(gdf1.pass4a.sum())}")

    piv = (gdf1[(gdf1.bar == "B_EWW10") & (gdf1.gross == 1.00)]
           .pivot_table(index="d_pp", columns=["panel", "phi"], values="cagr_slack_pp"))
    log("\nCAGR-floor slack (pp/yr, + = clears) for BAND-DG g1.00 vs B_EWW10, by (panel, phi) x d:")
    log(piv.to_string(float_format=lambda x: f"{x:+.2f}"))

    key_inv = idf[(idf.bar == "B_EWW10") & (idf.gross == 1.00)]
    log("\nRequired BAR drag d* (pp/yr) to close the floor, BAND-DG g1.00 vs B_EWW10:")
    log(key_inv.pivot_table(index="phi", columns=["panel", "window"], values="d_star_pp")
        .to_string(float_format=lambda x: f"{x:.3f}"))

    # the (h, L) decomposition of the required bar drag, at phi = 0 (the generous case)
    log("\n(h, L) pairs delivering the phi=0 required bar drag  [drag ~= h x (m - L), m = bar CAGR]:")
    hl = []
    for pname in panels:
        bar_m = float(idf[(idf.panel == pname) & (idf.bar == "B_EWW10")].iloc[0:1].index.size) * 0  # noop
        bm = gdf1[(gdf1.panel == pname) & (gdf1.bar == "B_EWW10") & (gdf1.d_pp == 0.0)]["bar_CAGR"].iloc[0]
        for window in ("full", "oos"):
            row = key_inv[(key_inv.panel == pname) & (key_inv.phi == 0.00)
                          & (key_inv.window == window)]
            d_star = float(row["d_star_pp"].iloc[0])
            for L, label in L_LADDER:
                h_req = (d_star / 100.0) / (bm - L) if np.isfinite(d_star) else np.inf
                hl.append(dict(panel=pname, window=window, bar_CAGR=bm, d_star_pp=d_star,
                               L=L, h_required=h_req, L_label=label))
    hldf = pd.DataFrame(hl)
    hldf.to_csv(HERE / f"{STEM}.inversion_hl.csv", index=False)
    log(hldf.pivot_table(index=["panel", "window"], columns="L", values="h_required")
        .to_string(float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------ DRAG MODEL 2: HAZARD
    log("\n## DRAG MODEL 2 — HAZARD: delistings injected into the panel, phi MEASURED\n")
    for pname, (px_, frame_, start_) in panels.items():
        base_live = both(fast_backtest(frame_, b_band_dg(frame_, 0.75), COST, "W")["returns"].loc[start_:])
        ref_bar = both(fast_backtest(frame_, b_ewbar(frame_, 1.00), COST, "W")["returns"].loc[start_:])
        ref_books = {g: both(fast_backtest(frame_, b_band_dg(frame_, g), COST, "W")["returns"].loc[start_:])
                     for g in (0.75, 1.00)}
        cells = [(h, W, L, sd) for h in H_LADDER for W in W_LADDER for L, _ in L_LADDER
                 for sd in (SEEDS if (h, W, L) == (0.02, BASE_W, BASE_L) else [BASE_SEED])]
        for (h, W, L, sd) in cells:
            aug = augment_panel(frame_, h, W, L, sd)
            n_add = aug.shape[1] - frame_.shape[1]
            bar_r = fast_backtest(aug, b_ewbar(aug, 1.00), COST, "W")["returns"].loc[start_:]
            bar = both(bar_r)
            for g in (0.75, 1.00):
                cand = both(fast_backtest(aug, b_band_dg(aug, g), COST, "W")["returns"].loc[start_:])
                bar_drag = 100.0 * (ref_bar["CAGR"] - bar["CAGR"])
                book_drag = 100.0 * (ref_books[g]["CAGR"] - cand["CAGR"])
                phi_meas = book_drag / bar_drag if abs(bar_drag) > 1e-9 else np.nan
                ok4b, miss4b = path_4b(cand, bar)
                ok4a, miss4a = path_4a(cand, base_live)
                haz_rows.append(dict(
                    model="HAZARD", panel=pname, h=h, W=W, L=L, seed=sd, n_phantom=n_add, gross=g,
                    CAGR=cand["CAGR"], Sharpe=cand["Sharpe"], MaxDD=cand["MaxDD"], H1=cand["H1"],
                    H2=cand["H2"], oos_CAGR=cand["oos_CAGR"], oos_Sharpe=cand["oos_Sharpe"],
                    oos_MaxDD=cand["oos_MaxDD"], bar_CAGR=bar["CAGR"], bar_Sharpe=bar["Sharpe"],
                    bar_MaxDD=bar["MaxDD"], bar_oos_CAGR=bar["oos_CAGR"],
                    bar_oos_Sharpe=bar["oos_Sharpe"], bar_drag_pp=bar_drag,
                    book_drag_pp=book_drag, phi_measured=phi_meas,
                    cagr_slack_pp=cagr_slack(cand, bar),
                    oos_cagr_slack_pp=cagr_slack(cand, bar, key="oos"),
                    pass4b=ok4b, miss4b=miss4b, pass4a=ok4a, miss4a=miss4a))
            log(f"  {pname} h={h:.2f} W={W:3d} L={L:+.2f} sd={sd} +{n_add:3d} phantoms | "
                f"bar {bar['CAGR']:6.2%} (drag {100*(ref_bar['CAGR']-bar['CAGR']):+.2f} pp) | "
                f"g1.00 {haz_rows[-1]['CAGR']:6.2%} (drag {haz_rows[-1]['book_drag_pp']:+.2f} pp) "
                f"phi {haz_rows[-1]['phi_measured']:+.3f} slack {haz_rows[-1]['cagr_slack_pp']:+.2f} pp "
                f"4b {'PASS' if haz_rows[-1]['pass4b'] else 'fail:' + haz_rows[-1]['miss4b']}")
    hdf = pd.DataFrame(haz_rows)

    # G9 — ADDED AFTER THE FIRST RUN (not pre-registered, stated as such): the FLAT inversion is an
    # exact identity given phi, so DRAG MODEL 1 contributes arithmetic only and the whole empirical
    # content of this run is the MEASURED phi of DRAG MODEL 2.
    #     slack(h) == slack(0) + 0.70 * bar_drag - book_drag
    g0 = hdf[hdf.h == 0].groupby(["panel", "gross"])["cagr_slack_pp"].first()
    pred = np.array([g0.loc[(p, g)] for p, g in zip(hdf.panel, hdf.gross)]) \
        + 0.70 * hdf.bar_drag_pp.values - hdf.book_drag_pp.values
    g9 = float(np.nanmax(np.abs(hdf.cagr_slack_pp.values - pred)))
    gates.append(dict(gate="G9 (ADDED post-hoc) slack == slack(0)+0.70*bar_drag-book_drag over all "
                           f"{len(hdf)} HAZARD cells -> the FLAT inversion is an identity in phi",
                      value=g9, bar=1e-9, passed=g9 < 1e-9))
    pd.DataFrame(gates).to_csv(HERE / f"{STEM}.gates.csv", index=False)
    log(f"\nG9 (added post-hoc) slack identity over {len(hdf)} HAZARD cells: max resid {g9:.3e} "
        f"(bar 1e-9, {'PASS' if g9 < 1e-9 else 'FAIL'}) — the FLAT model is arithmetic; phi is the "
        "only empirical quantity.")

    hdf.to_csv(HERE / f"{STEM}.hazard.csv", index=False)
    log(f"\nHAZARD grid: {len(hdf)} points written; 4b passes {int(hdf.pass4b.sum())}, "
        f"4a passes {int(hdf.pass4a.sum())}")
    liv = hdf[(hdf.h > 0) & (hdf.gross == 1.00)]
    log(f"measured phi over the {len(liv)} live-hazard cells at g1.00: "
        f"min {liv.phi_measured.min():+.3f} / median {liv.phi_measured.median():+.3f} / "
        f"max {liv.phi_measured.max():+.3f}; phi < 0.70 in {int((liv.phi_measured < 0.70).sum())} of {len(liv)}")
    log("\nmeasured phi by (panel, W) at g1.00, L=-0.30, seed 0:")
    log(hdf[(hdf.h > 0) & (hdf.gross == 1.00) & (hdf.L == -0.30) & (hdf.seed == BASE_SEED)]
        .pivot_table(index="W", columns=["panel", "h"], values="phi_measured")
        .to_string(float_format=lambda x: f"{x:+.3f}"))
    log("\nCAGR-floor slack (pp/yr) by (panel, W) at g1.00, L=-0.30, seed 0:")
    log(hdf[(hdf.h > 0) & (hdf.gross == 1.00) & (hdf.L == -0.30) & (hdf.seed == BASE_SEED)]
        .pivot_table(index="W", columns=["panel", "h"], values="cagr_slack_pp")
        .to_string(float_format=lambda x: f"{x:+.2f}"))
    sd_cells = hdf[(hdf.h == 0.02) & (hdf.W == BASE_W) & (hdf.L == BASE_L) & (hdf.gross == 1.00)]
    log("\nSEED control (h=0.02, W=252, L=-0.30): "
        + "; ".join(f"{r.panel} sd{r.seed} phi {r.phi_measured:+.3f} slack {r.cagr_slack_pp:+.2f}"
                    for r in sd_cells.itertuples()))

    # ------------------------------------------------------------ RULE 8
    log("\n## RULE 8 — gross picked on IS <= 2016 alone, 2017-2026 read ONCE\n")
    for pname, (px_, frame_, start_) in panels.items():
        spy_r = px_["SPY"].pct_change().fillna(0.0).loc[start_:]
        spy, base = both(spy_r), both(fast_backtest(frame_, b_band_dg(frame_, 0.75), COST,
                                                    "W")["returns"].loc[start_:])
        variants = [("UNDRAGGED", frame_, 0.0)]
        variants += [(f"HAZARD h={h:.2f} W={BASE_W} L={BASE_L}",
                      augment_panel(frame_, h, BASE_W, BASE_L, BASE_SEED), 0.0)
                     for h in (0.02, 0.05)]
        for vname, fr, _ in variants:
            rs = {g: fast_backtest(fr, b_band_dg(fr, g), COST, "W")["returns"].loc[start_:]
                  for g in GROSS_LADDER}
            pick = max(GROSS_LADDER, key=lambda g: is_sharpe(rs[g]))
            cand = both(rs[pick])
            bar_r = fast_backtest(fr, b_ewbar(fr, 1.00), COST, "W")["returns"].loc[start_:]
            bar = both(bar_r)
            for dname, d_applied, phi in [("no flat drag", 0.0, 0.0)] + \
                    [(f"FLAT d={d} phi={phi}", d, phi) for d in (1.25, 2.00) for phi in (0.0, 0.70)]:
                c = both(flat_drag(rs[pick], d_applied * phi))
                bb = both(flat_drag(bar_r, d_applied))
                ok4b, miss4b = path_4b(c, bb)
                ok4a, miss4a = path_4a(c, base)
                wf_rows.append(dict(panel=pname, variant=vname, drag=dname, is_pick_gross=pick,
                                    oos_CAGR=c["oos_CAGR"], oos_Sharpe=c["oos_Sharpe"],
                                    oos_MaxDD=c["oos_MaxDD"],
                                    base_oos_CAGR=base["oos_CAGR"], base_oos_Sharpe=base["oos_Sharpe"],
                                    base_oos_MaxDD=base["oos_MaxDD"],
                                    spy_oos_CAGR=spy["oos_CAGR"], spy_oos_Sharpe=spy["oos_Sharpe"],
                                    spy_oos_MaxDD=spy["oos_MaxDD"],
                                    bar_oos_CAGR=bb["oos_CAGR"], bar_oos_Sharpe=bb["oos_Sharpe"],
                                    oos_cagr_slack_pp=cagr_slack(c, bb, key="oos"),
                                    pass4b=ok4b, miss4b=miss4b, pass4a=ok4a, miss4a=miss4a,
                                    beats_base_oos=c["oos_Sharpe"] > base["oos_Sharpe"],
                                    beats_spy_oos=c["oos_Sharpe"] > spy["oos_Sharpe"]))
    wdf = pd.DataFrame(wf_rows)
    wdf.to_csv(HERE / f"{STEM}.walkforward.csv", index=False)
    log(wdf[["panel", "variant", "drag", "is_pick_gross", "oos_CAGR", "oos_Sharpe", "oos_MaxDD",
             "bar_oos_CAGR", "oos_cagr_slack_pp", "pass4b", "miss4b", "pass4a",
             "beats_base_oos", "beats_spy_oos"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    log(f"\nrule 8: 4b passes {int(wdf.pass4b.sum())} of {len(wdf)}; 4a {int(wdf.pass4a.sum())}; "
        f"beats RULES v2 OOS {int(wdf.beats_base_oos.sum())}; beats SPY OOS {int(wdf.beats_spy_oos.sum())}")
    log(f"OOS comparands: RULES v2 {wdf.base_oos_CAGR.iloc[0]:.2%}/{wdf.base_oos_Sharpe.iloc[0]:.4f}/"
        f"{wdf.base_oos_MaxDD.iloc[0]:.2%} (U56); SPY {wdf.spy_oos_CAGR.iloc[0]:.2%}/"
        f"{wdf.spy_oos_Sharpe.iloc[0]:.4f}/{wdf.spy_oos_MaxDD.iloc[0]:.2%}")

    (HERE / f"{STEM}.console.txt").write_text("\n".join(out) + "\n")
    print(f"\nwrote {STEM}.{{gates,grid,inversion,inversion_hl,hazard,walkforward}}.csv + console.txt")


if __name__ == "__main__":
    main()
