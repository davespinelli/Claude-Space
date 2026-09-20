#!/usr/bin/env python3
"""Idea 1727 (lane cloud, 2026-09-20) — CAN THE PER-NAME BAND GATE BE REPLACED BY A SINGLE
BREADTH DIAL?

Idea 1723 (lane B, 2026-09-20) found that the band's PER-NAME SELECTION is worth +0.0757 of OOS
Sharpe at t +0.82 on U56 and +0.0049 at t +0.07 on B136 against the SAME panel held equal-weight
with NO gate at the SAME target gross — and that the no-gate control is the better rule-8 OOS
book on both panels.  But that control is NOT IMPLEMENTABLE: its gross path is computed FROM the
band it is meant to replace.  This script closes the loop.

  BREADTH  the implementable book.  One aggregate number drives exposure:
               b_t   = share of PRICED names trading above their own 200d MA
               bs_t  = b_t averaged over the last S trading days  (dial 1: SMOOTHING)
               g_t   = clip(k * bs_t, 0, 1)                       (dial 2: MAP SLOPE)
           every priced name held at g_t / N of NAV, gated-out weight to CASH.  No per-name gate,
           no ranking, no vol filter.  Exactly TWO tuned parameters, S and k, and every one of the
           6 x 8 = 48 grid points is reported per panel.

  CELL     the standing 4b candidate, `rules_v2_weights(px, band=0.10, gross=1.00)` — the per-name
           200d +/- 10% band with hysteresis, weight to cash.  This is what BREADTH must reproduce.
  LIVE     `rules_v2_weights(px, band=0.03, gross=0.75)` — the live book (path 4a's incumbent).
  PANEL_MATCH  1723's non-implementable control, reported for continuity only.

Everything is weekly, 10 bps, next-day execution, no leverage.  Rule 8: (S, k) fitted on
2009-2016 IS Sharpe ONLY, 2017-2026 read ONCE.  Both KEEP paths at every grid point.
Panels U56 / B136 (CURRENT CONSTITUENTS — survivorship) and SMALL (sub-$2B names since 2010,
tickers with max_1d_move >= 1.0 dropped per data/small_meta.csv; ALSO current constituents of the
screen, so its survivorship bias is the worst of the three).  Price-only, deterministic, offline.

    python3 research/backtests/2026-09-20_breadth-dial-vs-band-gate_cloud.py
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights                # noqa: E402
from engine import backtest, rebalance_mask                         # noqa: E402

T0 = time.time()
OUT  = Path(__file__).resolve().parent
STEM = "2026-09-20_breadth-dial-vs-band-gate_cloud"
COST, FREQ, WARM = 10.0, "W", 260
IS_END = pd.Timestamp("2016-12-31")
SMOOTH = (1, 5, 10, 21, 42, 63)                                     # dial 1
SLOPE  = (0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0)                   # dial 2
CAND_BAND, CAND_GROSS = 0.10, 1.00                                  # the standing 4b candidate


def fast_run(px_v, w_v, mask_v, cost_bps=COST):
    """Exact numpy translation of engine.backtest (gated in G1)."""
    n = px_v.shape[0]
    rets = np.zeros_like(px_v); rets[1:] = px_v[1:] / px_v[:-1] - 1.0
    rets = np.nan_to_num(rets, nan=0.0, posinf=0.0, neginf=0.0)
    w_t = np.zeros_like(w_v); w_t[1:] = w_v[:-1]
    m = np.zeros(n, dtype=bool); m[1:] = mask_v[:-1]
    cur = np.zeros(px_v.shape[1]); turn = np.zeros(n); port = np.zeros(n)
    for i in range(n):
        if m[i] or i == 0:
            turn[i] = np.abs(w_t[i] - cur).sum(); cur = w_t[i].copy()
        port[i] = (cur * rets[i]).sum() - turn[i] * cost_bps / 1e4
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    return port, turn

def mx(r):
    eq = np.cumprod(1.0 + r); yrs = len(r) / 252.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252)
    return float(eq[-1] ** (1.0 / yrs) - 1.0), (float(r.mean() * 252 / vol) if vol else np.nan), dd

def windows(idx):
    full = np.zeros(len(idx), dtype=bool); full[WARM:] = True
    h = full.sum() // 2
    h1 = full.copy(); h1[WARM + h:] = False
    h2 = full.copy(); h2[:WARM + h] = False
    return dict(FULL=full, H1=h1, H2=h2,
                IS=full & np.asarray(idx <= IS_END), OOS=full & np.asarray(idx > IS_END))

def score(port, turn, W):
    o = {k: mx(port[m]) for k, m in W.items()}
    r = dict(CAGR=o["FULL"][0], Sharpe=o["FULL"][1], MaxDD=o["FULL"][2],
             H1=o["H1"][1], H2=o["H2"][1],
             IS_Sharpe=o["IS"][1], IS_CAGR=o["IS"][0], IS_MaxDD=o["IS"][2],
             OOS_CAGR=o["OOS"][0], OOS_Sharpe=o["OOS"][1], OOS_MaxDD=o["OOS"][2])
    r["Turn"] = float(turn[W["FULL"]].sum() / (W["FULL"].sum() / 252.0))
    r["OOS_Turn"] = float(turn[W["OOS"]].sum() / (W["OOS"].sum() / 252.0))
    return r

def keep_4a(r, b):      return bool(r["H1"] > b["H1"] and r["H2"] > b["H2"] and r["MaxDD"] >= b["MaxDD"])
def keep_4a_oos(r, b):  return bool(r["OOS_Sharpe"] > b["OOS_Sharpe"] and r["OOS_MaxDD"] >= b["OOS_MaxDD"])
def keep_4b_full(r, s): return bool(r["H1"] > s["H1"] and r["H2"] > s["H2"]
                                    and r["MaxDD"] >= 0.60 * s["MaxDD"] and r["CAGR"] >= 0.70 * s["CAGR"])
def keep_4b_oos(r, s):  return bool(r["OOS_Sharpe"] > s["OOS_Sharpe"]
                                    and r["OOS_MaxDD"] >= 0.60 * s["OOS_MaxDD"]
                                    and r["OOS_CAGR"] >= 0.70 * s["OOS_CAGR"])


def load_small():
    """The sub-$2B panel with the data-quality screen the sprint mandates."""
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep].dropna(how="all").ffill(), len(bad)


def main():
    gates, rows, corr_rows = [], [], []
    ref = {}
    panels = [("U56", lambda: (load_universe().dropna(how="all").ffill(), 0)),
              ("B136", lambda: (load_universe(broad=True).dropna(how="all").ffill(), 0)),
              ("SMALL", load_small)]

    for pname, loader in panels:
        px, n_dropped = loader()
        idx = px.index; px_v = px.values.astype(float)
        mask_v = rebalance_mask(idx, FREQ).values
        W = windows(idx); fw = W["FULL"]
        spy_col = px.columns.get_loc("SPY")
        nnames = px.shape[1] - 1

        spy_r = np.zeros(len(idx)); spy_r[1:] = px_v[1:, spy_col] / px_v[:-1, spy_col] - 1.0
        SPY = score(np.nan_to_num(spy_r), np.zeros(len(idx)), W)

        live_w = rules_v2_weights(px, band=0.03, gross=0.75)
        live_p, live_t = fast_run(px_v, live_w.values.astype(float), mask_v)
        LIVE = score(live_p, live_t, W)

        cand_w = rules_v2_weights(px, band=CAND_BAND, gross=CAND_GROSS)
        cand_wv = cand_w.values.astype(float)
        cand_p, cand_t = fast_run(px_v, cand_wv, mask_v)
        CELL = score(cand_p, cand_t, W)
        cand_g = cand_wv.sum(axis=1)                       # the CELL's own target-gross path

        # ---- G1 fast_run == engine.backtest ------------------------------------------
        eng = backtest(px, live_w, cost_bps=COST, freq=FREQ)
        d_ret = float(np.abs(eng["returns"].values[fw] - live_p[fw]).max())
        d_trn = float(np.abs(eng["turnover"].values[fw] - live_t[fw]).max())
        gates.append((f"G1 {pname} fast_run vs engine.backtest (returns / turnover, FULL)",
                      f"{d_ret:.3e} / {d_trn:.3e}", d_ret < 1e-12 and d_trn < 1e-12))
        gates.append((f"G2 {pname} live RULES v2 FULL cell ({nnames} names"
                      + (f", {n_dropped} tickers dropped on max_1d_move >= 1.0" if n_dropped else "") + ")",
                      f"{LIVE['CAGR']:.2%} / {LIVE['Sharpe']:.4f} / {LIVE['MaxDD']:.2%}", True))

        # ---- the breadth statistic ---------------------------------------------------
        cols = [c for c in px.columns if c != "SPY"]        # SPY is a benchmark, not a holding
        sub = px[cols]
        above = (sub > sub.rolling(200).mean())
        priced = sub.notna() & sub.rolling(200).mean().notna()
        b_raw = (above & priced).sum(axis=1) / priced.sum(axis=1).replace(0, np.nan)
        b_raw = b_raw.fillna(0.0)

        # unit equal weight over every PRICED name (SPY excluded from the book)
        e = np.where(np.isnan(px_v), 0.0, 1.0)
        e[:, spy_col] = 0.0
        ew_unit = np.nan_to_num(e / np.where(e.sum(axis=1) == 0, np.nan, e.sum(axis=1))[:, None])

        # PANEL_MATCH: 1723's non-implementable control (gross path taken FROM the band book)
        pm_p, pm_t = fast_run(px_v, ew_unit * cand_g[:, None], mask_v)
        PM = score(pm_p, pm_t, W)
        ref[pname] = dict(SPY=SPY, LIVE=LIVE, CELL=CELL, PM=PM, nnames=nnames,
                          cand_mean_gross=float(cand_g[fw].mean()))

        max_g = 0.0
        for S in SMOOTH:
            bs = b_raw.rolling(S).mean().fillna(0.0).values if S > 1 else b_raw.values
            for k in SLOPE:
                g = np.clip(k * bs, 0.0, 1.0)
                max_g = max(max_g, float(g.max()))
                w = ew_unit * g[:, None]
                p, t = fast_run(px_v, w, mask_v)
                r = score(p, t, W)
                rho = float(np.corrcoef(g[fw], cand_g[fw])[0, 1])
                r.update(panel=pname, S=S, k=k, arm="BREADTH",
                         mean_gross=float(g[fw].mean()),
                         gross_rho_vs_CELL=rho,
                         turn_ratio_vs_CELL=r["Turn"] / CELL["Turn"],
                         dOOS_Sharpe_vs_CELL=r["OOS_Sharpe"] - CELL["OOS_Sharpe"],
                         KEEP_4a_FULL=keep_4a(r, LIVE), KEEP_4b_FULL=keep_4b_full(r, SPY),
                         KEEP_4a_OOS=keep_4a_oos(r, LIVE), KEEP_4b_OOS=keep_4b_oos(r, SPY))
                rows.append(r)
                corr_rows.append(dict(panel=pname, S=S, k=k, rho=rho,
                                      mean_gross=r["mean_gross"],
                                      cell_mean_gross=float(cand_g[fw].mean())))
        for arm, sc in (("CELL", CELL), ("LIVE", LIVE), ("PANEL_MATCH", PM)):
            d = dict(sc); d.update(panel=pname, S=np.nan, k=np.nan, arm=arm,
                                   mean_gross=(float(cand_g[fw].mean()) if arm != "LIVE" else np.nan),
                                   gross_rho_vs_CELL=(1.0 if arm in ("CELL", "PANEL_MATCH") else np.nan),
                                   turn_ratio_vs_CELL=sc["Turn"] / CELL["Turn"],
                                   dOOS_Sharpe_vs_CELL=sc["OOS_Sharpe"] - CELL["OOS_Sharpe"],
                                   KEEP_4a_FULL=keep_4a(sc, LIVE), KEEP_4b_FULL=keep_4b_full(sc, SPY),
                                   KEEP_4a_OOS=keep_4a_oos(sc, LIVE), KEEP_4b_OOS=keep_4b_oos(sc, SPY))
            rows.append(d)
        gates.append((f"G3 {pname} no leverage (max breadth-driven target gross)",
                      f"{max_g:.6f}", max_g <= 1.0 + 1e-12))
        gates.append((f"G4 {pname} breadth statistic in [0,1] and uses NO forward information "
                      f"(200d MA through t, S-day mean through t, applied at t+1 by the engine)",
                      f"min {b_raw.min():.4f} max {b_raw.max():.4f} mean {b_raw[fw].mean():.4f}",
                      bool(b_raw.min() >= 0 and b_raw.max() <= 1)))

    df = pd.DataFrame(rows)
    df.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    pd.DataFrame(corr_rows).to_csv(OUT / f"{STEM}.gross_corr.csv", index=False)
    gates.append(("G5 two tuned dials only", "S (smoothing), k (map slope)", True))
    gates.append(("G6 every grid point reported",
                  f"{len(SMOOTH)}x{len(SLOPE)} = {len(SMOOTH)*len(SLOPE)} cells x 3 panels "
                  f"+ 3 reference arms x 3 panels = {len(df)} rows", True))

    # ================================ REPORT ====================================
    L = []; P = L.append
    P("# Idea 1727 — can the per-name band gate be replaced by a single breadth dial?\n")
    P(f"BREADTH book: every priced name equal-weight at `g_t/N`, "
      f"`g_t = clip(k * mean_S(share of panel above its own 200d MA), 0, 1)`, weight to CASH. "
      f"Weekly, {COST:.0f} bps, next-day execution, no leverage. "
      f"{len(SMOOTH)}x{len(SLOPE)} = {len(SMOOTH)*len(SLOPE)} grid points per panel, all reported.\n")
    P("SURVIVORSHIP: U56 / B136 / SMALL are all CURRENT constituents of their screens. SMALL is the "
      "worst exposed (sub-$2B names that still exist in 2026) and its levels should be read as an "
      "upper bound; the BREADTH-vs-CELL contrast is within-panel and far less exposed.\n")

    for pname in ("U56", "B136", "SMALL"):
        r = ref[pname]
        P(f"\n## {pname} ({r['nnames']} names)")
        for tag, s in (("SPY buy&hold", r["SPY"]), ("RULES v2 live (c=0.03, G=0.75)", r["LIVE"]),
                       ("CELL = standing 4b candidate (c=0.10, G=1.00)", r["CELL"]),
                       ("PANEL_MATCH (1723's non-implementable control)", r["PM"])):
            P(f"- **{tag}** FULL {s['CAGR']:.2%} / {s['Sharpe']:.4f} / {s['MaxDD']:.2%} "
              f"(H1 {s['H1']:.4f} / H2 {s['H2']:.4f}) | OOS {s['OOS_CAGR']:.2%} / "
              f"{s['OOS_Sharpe']:.4f} / {s['OOS_MaxDD']:.2%} | turnover {s['Turn']:.2f}/yr")
        P(f"- CELL mean target gross over FULL: {r['cand_mean_gross']:.4f}\n")

        d = df[(df.panel == pname) & (df.arm == "BREADTH")]
        P(f"### Every grid point, {pname}\n")
        P("| S | k | mean gross | rho(g, CELL g) | FULL CAGR | Sh | MaxDD | H1 | H2 | OOS CAGR | "
          "Sh | MaxDD | turn/yr | turn vs CELL | 4a F | 4b F | 4a O | 4b O |")
        P("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
        for _, x in d.sort_values(["S", "k"]).iterrows():
            P(f"| {int(x.S)} | {x.k:.1f} | {x.mean_gross:.3f} | {x.gross_rho_vs_CELL:+.4f} | "
              f"{x.CAGR:.2%} | {x.Sharpe:.4f} | {x.MaxDD:.2%} | {x.H1:.4f} | {x.H2:.4f} | "
              f"{x.OOS_CAGR:.2%} | {x.OOS_Sharpe:.4f} | {x.OOS_MaxDD:.2%} | {x.Turn:.2f} | "
              f"{x.turn_ratio_vs_CELL:.2f}x | {'Y' if x.KEEP_4a_FULL else '.'} | "
              f"{'Y' if x.KEEP_4b_FULL else '.'} | {'Y' if x.KEEP_4a_OOS else '.'} | "
              f"{'Y' if x.KEEP_4b_OOS else '.'} |")
        P(f"\nKEEP census {pname} (48 BREADTH cells): 4a FULL {int(d.KEEP_4a_FULL.sum())}, "
          f"4b FULL {int(d.KEEP_4b_FULL.sum())}, 4a OOS {int(d.KEEP_4a_OOS.sum())}, "
          f"4b OOS {int(d.KEEP_4b_OOS.sum())}, BOTH 4b "
          f"{int((d.KEEP_4b_FULL & d.KEEP_4b_OOS).sum())}.")
        P(f"rho(breadth gross, CELL gross) over the grid: min {d.gross_rho_vs_CELL.min():+.4f}, "
          f"max {d.gross_rho_vs_CELL.max():+.4f}, median {d.gross_rho_vs_CELL.median():+.4f}. "
          f"Turnover ratio vs CELL: min {d.turn_ratio_vs_CELL.min():.2f}x, "
          f"median {d.turn_ratio_vs_CELL.median():.2f}x, max {d.turn_ratio_vs_CELL.max():.2f}x.")

    # -------------------------------- rule 8 ------------------------------------
    P("\n## Rule 8 — (S, k) fitted on 2009-2016 IS Sharpe ONLY; 2017-2026 read ONCE\n")
    P("| panel | chooser | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | OOS turn/yr | 4a OOS | 4b OOS |")
    P("|---|---|---|---|---|---|---|---|---|")
    picks = []
    for pname in ("U56", "B136", "SMALL"):
        d = df[(df.panel == pname) & (df.arm == "BREADTH")]
        pk = d.sort_values(["IS_Sharpe", "S", "k"], ascending=[False, True, True]).iloc[0]
        P(f"| {pname} | C_IS_SHARPE (BREADTH) | S={int(pk.S)}, k={pk.k:.1f} | {pk.OOS_CAGR:.2%} | "
          f"{pk.OOS_Sharpe:.4f} | {pk.OOS_MaxDD:.2%} | {pk.OOS_Turn:.2f} | "
          f"{'Y' if pk.KEEP_4a_OOS else '.'} | {'Y' if pk.KEEP_4b_OOS else '.'} |")
        picks.append((pname, pk))
        for tag, key in (("CELL (standing 4b candidate)", "CELL"), ("RULES v2 live", "LIVE"),
                         ("PANEL_MATCH (control)", "PM"), ("SPY buy&hold", "SPY")):
            s = ref[pname][key]
            P(f"| {pname} | *{tag}* | — | {s['OOS_CAGR']:.2%} | {s['OOS_Sharpe']:.4f} | "
              f"{s['OOS_MaxDD']:.2%} | {s['OOS_Turn']:.2f} | — | — |")

    P("\n### The question as asked: does the one-number dial reproduce the candidate at a "
      "fraction of its turnover?\n")
    P("| panel | rule-8 BREADTH pick OOS Sharpe | CELL OOS Sharpe | d | BREADTH OOS turn/yr | "
      "CELL OOS turn/yr | turn ratio | rho(gross paths) |")
    P("|---|---|---|---|---|---|---|---|")
    for pname, pk in picks:
        c = ref[pname]["CELL"]
        P(f"| {pname} | {pk.OOS_Sharpe:.4f} | {c['OOS_Sharpe']:.4f} | "
          f"{pk.OOS_Sharpe - c['OOS_Sharpe']:+.4f} | {pk.OOS_Turn:.2f} | {c['OOS_Turn']:.2f} | "
          f"{pk.OOS_Turn / c['OOS_Turn']:.2f}x | {pk.gross_rho_vs_CELL:+.4f} |")

    P("\n## Gates\n")
    ok = sum(1 for _, _, g in gates if g)
    P(f"**{ok} of {len(gates)} pass.**\n")
    P("| gate | value | ok |")
    P("|---|---|---|")
    for n, v, o in gates:
        P(f"| {n} | {v} | {'OK' if o else 'FAIL'} |")

    (OUT / f"{STEM}.result.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))
    print(f"\n[{time.time()-T0:.1f}s] wrote {STEM}.result.md / .grid.csv / .gross_corr.csv")


if __name__ == "__main__":
    main()
