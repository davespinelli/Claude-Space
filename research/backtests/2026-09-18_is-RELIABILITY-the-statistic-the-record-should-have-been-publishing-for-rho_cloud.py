#!/usr/bin/env python3
"""Idea 1079 (lane cloud, 2026-09-18) — is RELIABILITY the statistic the record should have
been publishing for rho?

Idea 1073 measured one book's OOS Sharpe reliability at 0.0915 on small-cap panels against
0.5126 on large-cap ones.  Every committed rho(dial, OOS Sharpe | cell) is therefore
attenuated by a cell-specific amount that is never quoted.  This run:

  CAPITAL LEG   54 books (3 panels x 9 N x 2 gross), monthly, t+1, read at 10 / 25 / 50 bps
                = 162 cells.  Every grid point reported.  Both KEEP paths at every cell.
  RELIABILITY   Split-half (interleaved 63-day blocks, Spearman-Brown) reliability of the
                OOS Sharpe within each (panel, gross, cost) cell, and the SAME statistic
                computed IS-ONLY so it is available ex ante.
  RHO LEG       rho(N, OOS Sharpe) per cell, observed and disattenuated by sqrt(rel), and
                how many cells change RANK once disattenuated.
  RULE 8        N chosen on 2009-2016 IS Sharpe alone, 2017-2026 read ONCE.  Does the
                IS-reliability of a cell predict whether making the choice pays?
  CENSUS        Mechanical grep of the committed record for rho-on-OOS-Sharpe claims that
                quote a reliability.  Regexes printed.

Two tuned parameters only: N and gross.  Cost is a reported scenario, not a tuned dial.
Deterministic; runnable standalone.
"""
import sys, re
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score          # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa: E402

OUT = Path(__file__).with_suffix("")
FREQ, WARM = "M", 260
NS = [5, 8, 10, 12, 15, 20, 25, 30, 40]
GROSSES = [0.65, 1.00]
COSTS = [10.0, 25.0, 50.0]
IS_END, OOS_START, BLOCK = "2016-12-31", "2017-01-01", 63
pd.set_option("display.width", 220)


def fast_bt_raw(px, w, freq=FREQ):
    """engine.backtest's loop with cost_bps=0, returning (raw returns, turnover).
    Cost enters the engine strictly as `- turnover * bps/1e4` and never feeds back into the
    drift, so returns at any cost rung are EXACTLY raw - turnover*bps/1e4.  Gated below."""
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n, k = rets.shape
    cur = np.zeros(k); port = np.empty(n); to = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]; to[i] = np.abs(new - cur).sum(); cur = new.copy()
        port[i] = cur @ rets[i]
        g = cur * (1 + rets[i]); tot = g.sum() + (1 - cur.sum())
        if tot > 0: cur = g / tot
    return pd.Series(port, index=px.index), pd.Series(to, index=px.index)


def at_cost(raw, to, bps):
    return raw - to * bps / 1e4


def topn_weights(px, n, gross):
    s, above, vol20 = score(px, vol_scale=False)
    elig = s.where(above & (vol20 < 0.60))
    return (elig.rank(axis=1, ascending=False) <= n).astype(float) * (gross / n)


def spearman(a, b):
    """Rank correlation without scipy (the sandbox has none): Pearson on ranks."""
    ra, rb = pd.Series(a).rank(), pd.Series(b).rank()
    return float(ra.corr(rb))


def sh(r):
    return metrics(r)["Sharpe"]


def split_half_rel(sers, lo=None, hi=None):
    """Split-half reliability of the Sharpe statistic ACROSS the books of one cell.
    Interleaved 63-day blocks -> half A / half B; corr of Sharpe_A vs Sharpe_B across books,
    Spearman-Brown corrected.  Returns (rel, raw r)."""
    a_list, b_list = [], []
    for r in sers:
        x = r.loc[lo:hi] if (lo or hi) else r
        blk = np.arange(len(x)) // BLOCK
        A, B = x[blk % 2 == 0], x[blk % 2 == 1]
        a_list.append(sh(A)); b_list.append(sh(B))
    a, b = np.array(a_list), np.array(b_list)
    if np.std(a) == 0 or np.std(b) == 0 or len(a) < 3: return np.nan, np.nan
    r = float(np.corrcoef(a, b)[0, 1])
    rel = 2 * r / (1 + r) if r > -1 else np.nan
    return float(np.clip(rel, 0.0, 1.0)), r


def legs(r, spy, v2):
    h = len(r) // 2
    d = dict(CAGR=metrics(r)["CAGR"], S=sh(r), DD=metrics(r)["MaxDD"],
             H1=sh(r.iloc[:h]), H2=sh(r.iloc[h:]), IS_S=sh(r.loc[:IS_END]),
             OOS_S=sh(r.loc[OOS_START:]), OOS_CAGR=metrics(r.loc[OOS_START:])["CAGR"],
             OOS_DD=metrics(r.loc[OOS_START:])["MaxDD"])
    hs = len(spy) // 2; hv = len(v2) // 2
    d["p4a"] = bool(d["H1"] > sh(v2.iloc[:hv]) and d["H2"] > sh(v2.iloc[hv:])
                    and d["DD"] >= metrics(v2)["MaxDD"])
    d["p4b"] = bool(d["H1"] > sh(spy.iloc[:hs]) and d["H2"] > sh(spy.iloc[hs:])
                    and d["OOS_S"] > sh(spy.loc[OOS_START:])
                    and d["DD"] >= 0.60 * metrics(spy)["MaxDD"]
                    and d["CAGR"] >= 0.70 * metrics(spy)["CAGR"])
    return d


def get_panels():
    out = {"U56": load_universe(), "B136": load_universe(broad=True)}
    ps = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in ps.columns if c == "SPY" or c not in bad]
    print(f"SMALL: dropped {len(ps.columns)-len(keep)} tickers with max_1d_move >= 1.0 "
          f"(data/small_meta.csv); {len(keep)-1} names + SPY benchmark remain")
    out["SMALL"] = ps[keep]
    return out


def main():
    panels = get_panels()

    print("\n=== GATES ===")
    px = panels["U56"]; w = topn_weights(px, 20, 0.65); s0 = px.index[WARM]
    raw, to = fast_bt_raw(px, w)
    for bps in COSTS:
        e = engine_backtest(px, w, cost_bps=bps, freq=FREQ)["returns"].loc[s0:]
        d = float((e - at_cost(raw, to, bps).loc[s0:]).abs().max())
        print(f"  G1 cost-linearity + runner @ {bps:.0f} bps vs engine.backtest: max|d| {d:.3e}")
        assert d < 1e-12
    r10 = at_cost(raw, to, 10.0).loc[s0:]
    print(f"  G2 standing 2026-09-04 candidate (U56 N=20 g=0.65 monthly 10 bps): "
          f"CAGR {metrics(r10)['CAGR']:.4f} Sharpe {sh(r10):.4f} MaxDD {metrics(r10)['MaxDD']:.4f} "
          f"OOS Sharpe {sh(r10.loc[OOS_START:]):.4f}  (committed: 0.1269 / 1.201 / -0.1711 / 1.281)")

    bench = {}
    for pn, p in panels.items():
        s = p.index[WARM]
        vraw, vto = fast_bt_raw(p, rules_v2_weights(p), freq="W")
        v2 = at_cost(vraw, vto, 10.0).loc[s:]
        spy = p["SPY"].pct_change().fillna(0.0).loc[s:]
        bench[pn] = (spy, v2)
        print(f"  {pn}: SPY {metrics(spy)['CAGR']:.2%}/{sh(spy):.4f}/{metrics(spy)['MaxDD']:.2%} "
              f"(OOS {sh(spy.loc[OOS_START:]):.4f}) | RULES v2 {metrics(v2)['CAGR']:.2%}/{sh(v2):.4f}/"
              f"{metrics(v2)['MaxDD']:.2%} (OOS {sh(v2.loc[OOS_START:]):.4f})")

    # ---- CAPITAL LEG: 54 books x 3 cost rungs = 162 cells
    rows, series = [], {}
    for pn, p in panels.items():
        s = p.index[WARM]; spy, v2 = bench[pn]
        for n in NS:
            for g in GROSSES:
                raw, to = fast_bt_raw(p, topn_weights(p, n, g))
                for c in COSTS:
                    r = at_cost(raw, to, c).loc[s:]
                    series[(pn, g, c, n)] = r
                    d = legs(r, spy, v2)
                    d.update(panel=pn, N=n, gross=g, bps=c,
                             turn=float(to.loc[s:].sum() / (len(r) / 252)))
                    rows.append(d)
    grid = pd.DataFrame(rows)[["panel", "gross", "bps", "N", "CAGR", "S", "DD", "H1", "H2",
                               "IS_S", "OOS_S", "OOS_CAGR", "OOS_DD", "turn", "p4a", "p4b"]]
    grid.to_csv(OUT.with_suffix(".grid.csv"), index=False)
    print("\n=== CAPITAL LEG — ALL 162 GRID POINTS (monthly, t+1) ===")
    print(grid.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"\n4a: {int(grid.p4a.sum())} of {len(grid)}   4b: {int(grid.p4b.sum())} of {len(grid)}")
    for c in COSTS:
        sub = grid[grid.bps == c]
        print(f"   @{c:.0f} bps: 4a {int(sub.p4a.sum())}/{len(sub)}, 4b {int(sub.p4b.sum())}/{len(sub)}"
              + "".join(f"   {pn} 4b {int(sub[sub.panel==pn].p4b.sum())}/{len(sub[sub.panel==pn])}"
                        for pn in panels))

    # ---- RELIABILITY + RHO LEG
    crows = []
    for pn in panels:
        spy, _ = bench[pn]
        for g in GROSSES:
            for c in COSTS:
                sers = [series[(pn, g, c, n)] for n in NS]
                rel_o, r_o = split_half_rel(sers, OOS_START, None)
                rel_i, r_i = split_half_rel(sers, None, IS_END)
                oos = np.array([sh(x.loc[OOS_START:]) for x in sers])
                iss = np.array([sh(x.loc[:IS_END]) for x in sers])
                rho = spearman(NS, oos)
                dis = rho / np.sqrt(rel_o) if rel_o and rel_o > 0 else np.nan
                # rule 8: choose N on IS Sharpe alone, read OOS once
                win = int(np.argmax(iss))
                crows.append(dict(cell=f"{pn}|g={g:.2f}|{c:.0f}bps", panel=pn, gross=g, bps=c,
                                  rel_OOS=rel_o, r_OOS=r_o, rel_IS=rel_i,
                                  rho_obs=rho, rho_disatt=dis,
                                  SD_OOS_S=float(oos.std(ddof=1)), pick_N=NS[win],
                                  OOS_pick=float(oos[win]), OOS_anchor=float(oos.mean()),
                                  gain=float(oos[win] - oos.mean()),
                                  OOS_SPY=sh(spy.loc[OOS_START:])))
    cells = pd.DataFrame(crows)
    cells.to_csv(OUT.with_suffix(".cells.csv"), index=False)
    print("\n=== RELIABILITY + RHO LEG — every cell (dial = N, 9 rungs) ===")
    print(cells.drop(columns=["panel", "gross", "bps"]).to_string(index=False,
          float_format=lambda x: f"{x:.4f}"))

    print("\n--- reliability by panel (the 1073 claim, re-measured on 9-rung cells) ---")
    for pn in panels:
        sub = cells[cells.panel == pn]
        print(f"  {pn:6s} mean rel_OOS {sub.rel_OOS.mean():.4f}  mean rel_IS {sub.rel_IS.mean():.4f}"
              f"  mean |rho_obs| {sub.rho_obs.abs().mean():.4f}"
              f"  mean SD(OOS Sharpe) {sub.SD_OOS_S.mean():.4f}")

    ok = cells.dropna(subset=["rho_disatt"])
    ro = cells.rho_obs.abs().rank(ascending=False)
    rd = cells.rho_disatt.abs().rank(ascending=False)
    changed = int((ro != rd).sum())
    print(f"\n  cells: {len(cells)}; rank on |rho| CHANGES for {changed} of {len(cells)} "
          f"once disattenuated; Spearman(rank_obs, rank_disatt) = "
          f"{spearman(ro.values, rd.values):.4f}")
    print(f"  |rho| mean observed {cells.rho_obs.abs().mean():.4f} -> disattenuated "
          f"{ok.rho_disatt.abs().mean():.4f}; cells whose disattenuated |rho| exceeds 1.0 "
          f"(i.e. the attenuation correction is larger than the statistic can carry): "
          f"{int((ok.rho_disatt.abs() > 1).sum())} of {len(ok)}")
    print(f"  rho(rel_IS, rel_OOS) across cells = {cells.rel_IS.corr(cells.rel_OOS):.4f} "
          f"— is reliability itself stable enough to be used ex ante?")

    # ---- is reliability a usable EX ANTE gate? (rule 8, OOS read once)
    print("\n--- RELIABILITY AS AN EX-ANTE GATE (rule 8, N chosen on IS only, OOS read once) ---")
    print(f"  rho(rel_IS, OOS gain of the pick) = {cells.rel_IS.corr(cells.gain):+.4f} "
          f"(n={len(cells)})")
    for thr in (0.0, 0.25, 0.50, 0.75):
        fired = cells.rel_IS >= thr
        g = np.where(fired, cells.OOS_pick, cells.OOS_anchor)
        print(f"  gate rel_IS >= {thr:.2f}: fires {int(fired.sum()):3d}/{len(cells)}, "
              f"mean OOS Sharpe {g.mean():.4f}")
    print(f"  always take the IS-max pick:   mean OOS Sharpe {cells.OOS_pick.mean():.4f}")
    print(f"  do nothing (hold the 9 rungs): mean OOS Sharpe {cells.OOS_anchor.mean():.4f}")
    print(f"  panel SPY OOS, cell-weighted:  {cells.OOS_SPY.mean():.4f}")

    # ---- CENSUS LEG
    print("\n=== CENSUS LEG — committed rho-on-OOS-Sharpe claims that quote a reliability ===")
    RHO = re.compile(r"(rho|ρ)\s*\(|correlat", re.I)
    OOSS = re.compile(r"OOS[^.\n]{0,40}(Sharpe|S\|k|S \| k)", re.I)
    REL = re.compile(r"reliab|disattenuat|attenuat|ICC|split-half|Spearman-Brown", re.I)
    files = [ROOT / "research" / "LEADERBOARD.md"] + sorted((ROOT / "research" / "backtests").glob("*.memo.md"))
    units = claims = withrel = 0
    for f in files:
        for ln in f.read_text(errors="ignore").split("\n"):
            if not ln.strip(): continue
            units += 1
            if RHO.search(ln) and OOSS.search(ln):
                claims += 1
                if REL.search(ln): withrel += 1
    print(f"  files {len(files)}, non-blank lines {units}")
    print(f"  lines carrying a rho/correlation claim ABOUT an OOS Sharpe: {claims}")
    print(f"  of those, lines that also name reliability / attenuation: {withrel}"
          + (f" ({withrel/claims:.1%})" if claims else ""))
    print("  regexes:", RHO.pattern, "|", OOSS.pattern, "|", REL.pattern)
    print("\nWrote:", OUT.with_suffix(".grid.csv").name, OUT.with_suffix(".cells.csv").name)


if __name__ == "__main__":
    main()
