#!/usr/bin/env python3
"""Idea 1628 (lane cloud, 2026-09-20): does the MAXVOL 0.60 PARK survive a BAND CROSS and a
CAGR-FLOOR-CHARGED SPY?

1617 left a PARK: a book that holds every priced name whose 20-day realised vol is below 0.60,
with NO band and NO ranking, clears 4b on FULL and OOS on U56 and B136 at 0/10/25/50 bps and
fixes the exact 4b leg live RULES v2 fails (the CAGR floor).  But (a) no IS-only chooser reaches
it and (b) its Sharpe edge over its own no-ceiling twin is +0.0089 at 10 bps and NEGATIVE at 25.

Two questions, one grid:

  Q1 ADDITIVITY.  Live RULES v2 clause 2 is a 200d MA band; the RETIRED v1 vol gate is a MAXVOL
     ceiling.  Are they ADDITIVE (each buys something the other does not) or SUBSTITUTES (the
     second buys nothing once the first is on)?  Cross them: MAXVOL m x BAND c, every rung
     published, and read the interaction directly as
         INTERACTION = [S(m,c) - S(inf,c)] - [S(m,NOBAND) - S(inf,NOBAND)]
     i.e. how much the MAXVOL ceiling's Sharpe gain CHANGES once the band is already on.
     Substitutes => the gain collapses toward 0 with the band on (INTERACTION negative).

  Q2 THE BAR ITSELF.  Idea 1490's caveat: every 4b floor and cap in the record is set by a
     COSTLESS SPY buy-and-hold while every candidate pays 10 bps.  Re-read EVERY 4b verdict here
     against a SPY charged the candidate's OWN realised turnover (1490's convention), beside the
     record's costless SPY, and report how many passes are bar artefacts.

Dials -- exactly TWO tuned parameters, as the idea specifies:
    m   MAXVOL ceiling in {0.45, 0.60, 0.80, 1.00, 1.50, inf}   (inf = no ceiling, the twin)
    c   BAND width in {NOBAND, 0.00, 0.03, 0.10}                (0.03 = live clause 2)
ALL 6 x 4 = 24 grid points are reported on each of 3 panels (72 books).

The COST axis is NOT a third tuned parameter: 1586 established r(c) = r_gross - turnover*c/1e4
is EXACT off the cached gross path, so 0/10/25/50 bps are restatements of the same book, not
refits.  10 bps is the PROTOCOL rung and every verdict is quoted there; the others are published
as robustness (and gate G3 checks the identity against the engine).

Construction (the record's conventions): equal weight over the priced constituents that pass the
gate(s), scaled to the live gross 0.75, weekly cadence, 10 bps, weights decided at t applied at
t+1.  DE-GROSS TO CASH: the denominator is the number of instruments PRICED that day, so
gated-out weight goes to cash and is never re-spread.

Rule 8: (m, c) chosen on 2009-2016 IS rows ONLY -- by TWO independent IS-only choosers (argmax IS
Sharpe, and argmax IS Calmar) -- then 2017-2026 read ONCE and the chosen books scored on BOTH
KEEP paths against live RULES v2 and SPY (costless AND turnover-charged).

Panels: U56, B136 and SMALL (the 483-name sub-$2B panel, with the tickers whose
`max_1d_move >= 1.0` in data/small_meta.csv dropped first).  SURVIVORSHIP: all three panels are
CURRENT constituents of their screens, so every absolute level here is optimistic; SMALL is the
worst affected (sub-$2B names that delisted are simply absent).  On SMALL the joined SPY column
is a BENCHMARK only and is never held.
Price-only.  No EDGAR / Form 4 / 8-K / options / spin-offs / live data.

Deterministic, offline, standalone:
    python3 research/backtests/2026-09-20_maxvol-x-band-cross_cloud.py
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa
from engine import backtest, rebalance_mask  # noqa

T0 = time.time()
COST = 10.0                 # PROTOCOL rule 2
COST_LADDER = (0.0, 10.0, 25.0, 50.0)
FREQ = "W"                  # live cadence
GROSS = 0.75                # live RULES v2 gross
WARM = 260
IS_END = pd.Timestamp("2016-12-31")
M_GRID = (0.45, 0.60, 0.80, 1.00, 1.50, np.inf)
C_GRID = (("NOBAND", None), ("0.00", 0.00), ("0.03", 0.03), ("0.10", 0.10))
OUT = Path(__file__).with_suffix("")

# ------------------------------------------------------------------ engine (gated G1 vs engine)
def fast_run(px_v, w_v, mask_v, cost_bps=0.0):
    """Returns GROSS-of-cost port when cost_bps=0; turnover is returned so any cost is exact."""
    n, k = px_v.shape
    rets = np.zeros_like(px_v); rets[1:] = px_v[1:] / px_v[:-1] - 1.0
    rets = np.nan_to_num(rets, nan=0.0, posinf=0.0, neginf=0.0)
    w_t = np.zeros_like(w_v); w_t[1:] = w_v[:-1]
    m = np.zeros(n, dtype=bool); m[1:] = mask_v[:-1]
    cur = np.zeros(k); turn = np.zeros(n); port = np.zeros(n); heldg = np.zeros(n)
    for i in range(n):
        if m[i] or i == 0:
            turn[i] = np.abs(w_t[i] - cur).sum(); cur = w_t[i].copy()
        heldg[i] = cur.sum()
        port[i] = (cur * rets[i]).sum() - turn[i] * cost_bps / 1e4
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    return port, turn, heldg

def net(gross_p, turn, c):            # 1586's exact cost restatement
    return gross_p - turn * c / 1e4

def sh(r):
    v = r.std(ddof=1) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan
def mdd(r):
    eq = np.cumprod(1.0 + r)
    return float((eq / np.maximum.accumulate(eq) - 1.0).min())
def cagr(r):
    eq = np.cumprod(1.0 + r); y = len(r) / 252.0
    return float(eq[-1] ** (1.0 / y) - 1.0) if y > 0 else np.nan
def calmar(r):
    d = mdd(r)
    return float(cagr(r) / abs(d)) if d < 0 else np.nan

def keep_4a(r, b, win):               # both halves + DD, PROTOCOL 4a
    rw, bw = r[win], b[win]; h = len(rw) // 2
    return bool(sh(rw[:h]) > sh(bw[:h]) and sh(rw[h:]) > sh(bw[h:]) and mdd(rw) >= mdd(bw))
def keep_4a_1w(r, b, win):            # single-window (OOS) form
    return bool(sh(r[win]) > sh(b[win]) and mdd(r[win]) >= mdd(b[win]))
def keep_4b(r, s, win):
    rw, sw = r[win], s[win]; h = len(rw) // 2
    return bool(sh(rw[:h]) > sh(sw[:h]) and sh(rw[h:]) > sh(sw[h:])
                and mdd(rw) >= 0.60 * mdd(sw) and cagr(rw) >= 0.70 * cagr(sw))
def keep_4b_1w(r, s, win):
    rw, sw = r[win], s[win]
    return bool(sh(rw) > sh(sw) and mdd(rw) >= 0.60 * mdd(sw) and cagr(rw) >= 0.70 * cagr(sw))
def legs_4b(r, s, win):               # which leg binds, for the bar-artefact read
    rw, sw = r[win], s[win]
    return dict(L_SH=sh(rw) > sh(sw), L_DD=mdd(rw) >= 0.60 * mdd(sw), L_CAGR=cagr(rw) >= 0.70 * cagr(sw))

# ------------------------------------------------------------------------------- the books
def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)

def build(px, cols, m, band_c, gscale=1.0):
    """Equal weight over priced constituents passing (vol20 < m) and the band, gross 0.75,
    de-gross to CASH (denominator = names PRICED that day, gated weight never re-spread)."""
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = GROSS * gscale * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    gate = pd.DataFrame(True, index=sub.index, columns=sub.columns)
    if np.isfinite(m): gate &= (vol20(sub) < m).fillna(False)
    if band_c is not None: gate &= band_state(sub, band_c)
    w = ew.where(gate, 0.0)
    return w.reindex(columns=px.columns).fillna(0.0)

def panels():
    px56 = load_universe().dropna(how="all").ffill()
    px136 = load_universe(broad=True).dropna(how="all").ffill()
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    small_cols = [c for c in pxs.columns if c != "SPY" and c not in bad]
    return [("U56", px56, list(px56.columns)),                 # live convention: SPY is held
            ("B136", px136, list(px136.columns)),
            ("SMALL", pxs, small_cols)]                        # SPY is benchmark only

def mlab(m): return "inf" if not np.isfinite(m) else f"{m:.2f}"

# ------------------------------------------------------------------------------------ main
def main():
    gates, rows, pick_rows, inter_rows, dg_rows = [], [], [], [], []
    lines = []
    P = lambda s="": (print(s), lines.append(s))

    for pname, px, cols in panels():
        idx = px.index; px_v = px.values.astype(float)
        mask_v = rebalance_mask(idx, FREQ).values
        full = np.zeros(len(idx), dtype=bool); full[WARM:] = True
        IS = full & np.asarray(idx <= IS_END)
        OOS = full & np.asarray(idx > IS_END)

        sc = px.columns.get_loc("SPY")
        spy_r = np.zeros(len(idx)); spy_r[1:] = px_v[1:, sc] / px_v[:-1, sc] - 1.0
        spy_r = np.nan_to_num(spy_r)

        live_w = rules_v2_weights(px[cols], band=0.03, gross=GROSS).reindex(columns=px.columns).fillna(0.0)
        live_g, live_to, _ = fast_run(px_v, live_w.values.astype(float), mask_v)
        live_p = net(live_g, live_to, COST)

        if pname == "U56":
            eng = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].values
            d = float(np.abs(eng[full] - live_p[full]).max())
            gates.append(("G1 U56 fast_run+net == engine.backtest (RULES v2, FULL)", f"{d:.3e}", d < 1e-12))
            eng25 = backtest(px, rules_v2_weights(px), cost_bps=25.0, freq=FREQ)["returns"].values
            d2 = float(np.abs(eng25[full] - net(live_g, live_to, 25.0)[full]).max())
            gates.append(("G3 cost restatement r(c)=r_gross-turn*c/1e4 EXACT at c=25 vs engine", f"{d2:.3e}", d2 < 1e-12))
            gates.append(("G2 U56 RULES v2 OOS cell (10bps)",
                          f"{cagr(live_p[OOS]):.2%} / {sh(live_p[OOS]):.4f} / {mdd(live_p[OOS]):.2%}", True))

        store, store_full = {}, {}
        for m in M_GRID:
            for cname, bc in C_GRID:
                w = build(px, cols, m, bc)
                gp, to, hg = fast_run(px_v, w.values.astype(float), mask_v)
                store[(m, cname)] = (gp, to); store_full[(m, cname)] = (gp, to, hg)
                p = net(gp, to, COST)
                # 1490's turnover-charged SPY: SPY pays THIS book's own realised turnover
                spy_ch = spy_r - to * COST / 1e4
                row = dict(panel=pname, m=mlab(m), c=cname,
                           mean_gross=float(hg[full].mean()),
                           turn_yr=float(to[full].sum() / (full.sum() / 252.0)),
                           IS_Sharpe=sh(p[IS]), IS_Calmar=calmar(p[IS]),
                           FULL_CAGR=cagr(p[full]), FULL_Sharpe=sh(p[full]), FULL_MaxDD=mdd(p[full]),
                           OOS_CAGR=cagr(p[OOS]), OOS_Sharpe=sh(p[OOS]), OOS_MaxDD=mdd(p[OOS]),
                           keep4a_FULL=keep_4a(p, live_p, full), keep4a_OOS=keep_4a_1w(p, live_p, OOS),
                           keep4b_FULL=keep_4b(p, spy_r, full), keep4b_OOS=keep_4b_1w(p, spy_r, OOS),
                           keep4b_FULL_chg=keep_4b(p, spy_ch, full), keep4b_OOS_chg=keep_4b_1w(p, spy_ch, OOS))
                row.update({f"S_{int(c)}bps": sh(net(gp, to, c)) for c in COST_LADDER})
                row.update({f"k4bF_{int(c)}bps": keep_4b(net(gp, to, c), spy_r, full) for c in COST_LADDER})
                lg = legs_4b(p, spy_r, full); row.update({f"F_{k}": v for k, v in lg.items()})
                lgc = legs_4b(p, spy_ch, full); row.update({f"Fchg_{k}": v for k, v in lgc.items()})
                rows.append(row)

        # ---- Q1 interaction: does the MAXVOL gain survive the band being on?
        for m in M_GRID:
            if not np.isfinite(m): continue
            for cname, _ in C_GRID:
                gm, tm = store[(m, cname)]; gi, ti = store[(np.inf, cname)]
                d_here = sh(net(gm, tm, COST)) - sh(net(gi, ti, COST))
                gm0, tm0 = store[(m, "NOBAND")]; gi0, ti0 = store[(np.inf, "NOBAND")]
                d_base = sh(net(gm0, tm0, COST)) - sh(net(gi0, ti0, COST))
                inter_rows.append(dict(panel=pname, m=mlab(m), c=cname,
                                       dSharpe_MAXVOL=d_here, dSharpe_MAXVOL_NOBAND=d_base,
                                       INTERACTION=d_here - d_base,
                                       dSharpe_MAXVOL_25bps=sh(net(gm, tm, 25.0)) - sh(net(gi, ti, 25.0))))

        # ---- MATCHED-EXPOSURE CONTROL.  Eight 2026-09-19 runs found every drawdown-buying
        # device beaten at MATCHED realised exposure by a plain de-gross.  For each MAXVOL cell,
        # build its no-ceiling twin re-scaled so realised mean gross MATCHES, and re-read dSharpe.
        gm_of = {k: float(np.asarray(v[2])[full].mean()) for k, v in store_full.items()}
        for m in M_GRID:
            if not np.isfinite(m): continue
            for cname, bc in C_GRID:
                tgt = gm_of[(m, cname)]; base = gm_of[(np.inf, cname)]
                k1 = tgt / base if base > 0 else 1.0
                w = build(px, cols, np.inf, bc, gscale=k1)
                gp, to, hg = fast_run(px_v, w.values.astype(float), mask_v)
                got = float(hg[full].mean())
                gm, tm = store[(m, cname)]
                dg_rows.append(dict(panel=pname, m=mlab(m), c=cname,
                                    gross_device=tgt, gross_degross=got,
                                    gross_gap=got - tgt,
                                    Sharpe_device=sh(net(gm, tm, COST)),
                                    Sharpe_degross=sh(net(gp, to, COST)),
                                    dSharpe_vs_DEGROSS=sh(net(gm, tm, COST)) - sh(net(gp, to, COST)),
                                    MaxDD_device=mdd(net(gm, tm, COST)[full]),
                                    MaxDD_degross=mdd(net(gp, to, COST)[full]),
                                    dMaxDD_pp=(mdd(net(gm, tm, COST)[full]) - mdd(net(gp, to, COST)[full])) * 100,
                                    CAGR_device=cagr(net(gm, tm, COST)[full]),
                                    CAGR_degross=cagr(net(gp, to, COST)[full]),
                                    turn_device=float(tm[full].sum() / (full.sum() / 252.0)),
                                    turn_degross=float(to[full].sum() / (full.sum() / 252.0)),
                                    k4b_device=keep_4b(net(gm, tm, COST), spy_r, full),
                                    k4b_degross=keep_4b(net(gp, to, COST), spy_r, full)))

        # ---- rule 8: two IS-only choosers over the joint (m, c) grid; OOS read ONCE
        d = pd.DataFrame([r for r in rows if r["panel"] == pname]).reset_index(drop=True)
        for cname_ch, col in (("IS_Sharpe", "IS_Sharpe"), ("IS_Calmar", "IS_Calmar")):
            j = int(d[col].idxmax()); pk = d.loc[j]
            key = (float("inf") if pk.m == "inf" else float(pk.m), pk.c)
            gp, to = store[key]; p = net(gp, to, COST); spy_ch = spy_r - to * COST / 1e4
            pick_rows.append(dict(panel=pname, chooser=cname_ch, pick_m=pk.m, pick_c=pk.c,
                                  IS_rank_of_PARK_m060_NOBAND=int(
                                      (d[col] > float(d[(d.m == "0.60") & (d.c == "NOBAND")][col].iloc[0])).sum() + 1),
                                  n_cells=len(d),
                                  OOS_CAGR=cagr(p[OOS]), OOS_Sharpe=sh(p[OOS]), OOS_MaxDD=mdd(p[OOS]),
                                  live_OOS_Sharpe=sh(live_p[OOS]), live_OOS_MaxDD=mdd(live_p[OOS]),
                                  spy_OOS_CAGR=cagr(spy_r[OOS]), spy_OOS_Sharpe=sh(spy_r[OOS]),
                                  spy_OOS_MaxDD=mdd(spy_r[OOS]),
                                  keep4a_OOS=keep_4a_1w(p, live_p, OOS),
                                  keep4b_OOS=keep_4b_1w(p, spy_r, OOS),
                                  keep4b_OOS_chg=keep_4b_1w(p, spy_ch, OOS)))
        P(f"[{pname}] done  t={time.time()-T0:.0f}s")

    G = pd.DataFrame(rows); I = pd.DataFrame(inter_rows); K = pd.DataFrame(pick_rows)
    D = pd.DataFrame(dg_rows); D.to_csv(f"{OUT}_degross.csv", index=False)
    G.to_csv(f"{OUT}_grid.csv", index=False); I.to_csv(f"{OUT}_interaction.csv", index=False)
    K.to_csv(f"{OUT}_rule8.csv", index=False)

    pd.set_option("display.width", 250, "display.max_columns", 60, "display.max_rows", 300)
    f3 = lambda x: f"{x:.4f}" if isinstance(x, float) else str(x)

    P("\n" + "=" * 110); P("FULL GRID (10 bps) -- ALL 72 cells, every rung published"); P("=" * 110)
    P(G[["panel","m","c","mean_gross","turn_yr","FULL_CAGR","FULL_Sharpe","FULL_MaxDD",
         "OOS_CAGR","OOS_Sharpe","OOS_MaxDD","keep4a_FULL","keep4a_OOS","keep4b_FULL","keep4b_OOS",
         "keep4b_FULL_chg","keep4b_OOS_chg"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n" + "=" * 110); P("COST LADDER -- Sharpe at 0/10/25/50 bps, and 4b FULL at each rung"); P("=" * 110)
    P(G[["panel","m","c"] + [f"S_{int(c)}bps" for c in COST_LADDER]
        + [f"k4bF_{int(c)}bps" for c in COST_LADDER]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n" + "=" * 110); P("Q1 ADDITIVITY -- MAXVOL's Sharpe gain over its OWN no-ceiling twin, by band"); P("=" * 110)
    P(I.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    P("\nPooled over panels and m, mean dSharpe(MAXVOL) by band (10 bps):")
    P(I.groupby("c").dSharpe_MAXVOL.agg(["mean", "min", "max", "count"]).to_string(float_format=lambda x: f"{x:+.4f}"))
    P("\nPooled INTERACTION (gain with band ON minus gain with band OFF); negative = SUBSTITUTES:")
    P(I[I.c != "NOBAND"].groupby(["panel", "c"]).INTERACTION.agg(["mean", "min", "max"]).to_string(float_format=lambda x: f"{x:+.4f}"))
    nneg = int((I[I.c != "NOBAND"].INTERACTION < 0).sum()); ntot = int((I.c != "NOBAND").sum())
    P(f"\nINTERACTION negative in {nneg} of {ntot} band-on cells ({nneg/ntot:.1%}).")
    P(f"mean INTERACTION over all band-on cells: {I[I.c!='NOBAND'].INTERACTION.mean():+.4f}")

    P("\n" + "=" * 110); P("Q2 THE 4b BAR ITSELF -- costless SPY (record) vs turnover-charged SPY (idea 1490)"); P("=" * 110)
    for w in ("FULL", "OOS"):
        a = int(G[f"keep4b_{w}"].sum()); b = int(G[f"keep4b_{w}_chg"].sum())
        flip = int((~G[f"keep4b_{w}"] & G[f"keep4b_{w}_chg"]).sum())
        lost = int((G[f"keep4b_{w}"] & ~G[f"keep4b_{w}_chg"]).sum())
        P(f"  {w:4s}: 4b passes costless SPY = {a:2d}/72 ; charged SPY = {b:2d}/72 ; gained {flip}, lost {lost}")
    P("\nBinding leg on FULL (costless SPY), over all 72 cells:")
    P(G[["F_L_SH", "F_L_DD", "F_L_CAGR"]].sum().to_string())
    P("Binding leg on FULL (turnover-charged SPY):")
    P(G[["Fchg_L_SH", "Fchg_L_DD", "Fchg_L_CAGR"]].sum().to_string())
    P("\nThe PARK cell 1617 left (m=0.60, NOBAND), all three panels:")
    P(G[(G.m == "0.60") & (G.c == "NOBAND")].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\nIts own no-ceiling twin (m=inf, NOBAND):")
    P(G[(G.m == "inf") & (G.c == "NOBAND")].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n" + "=" * 110)
    P("MATCHED-EXPOSURE CONTROL -- every MAXVOL cell against a plain DE-GROSS twin at the SAME")
    P("realised mean gross (no ceiling, band unchanged, gross re-scaled).  10 bps.")
    P("=" * 110)
    P(D.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    nb = D[D.c == "NOBAND"]
    P(f"\nNOBAND cells (the PARK family): device beats matched de-gross on Sharpe in "
      f"{int((nb.dSharpe_vs_DEGROSS > 0).sum())} of {len(nb)}; mean dSharpe {nb.dSharpe_vs_DEGROSS.mean():+.4f}, "
      f"mean dMaxDD {nb.dMaxDD_pp.mean():+.2f} pp")
    P(f"ALL cells: device wins on Sharpe {int((D.dSharpe_vs_DEGROSS > 0).sum())} of {len(D)}; "
      f"mean dSharpe {D.dSharpe_vs_DEGROSS.mean():+.4f}, mean dMaxDD {D.dMaxDD_pp.mean():+.2f} pp")
    P(f"4b FULL: device passes {int(D.k4b_device.sum())} of {len(D)}; matched de-gross twin passes "
      f"{int(D.k4b_degross.sum())} of {len(D)}")
    P("Max |realised gross gap| between device and its matched twin: "
      f"{D.gross_gap.abs().max():.4f} (match quality)")

    P("\n" + "=" * 110); P("RULE 8 -- (m, c) chosen on 2009-2016 ONLY; 2017-2026 read ONCE"); P("=" * 110)
    P(K.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\nIS-only choosers reaching the PARK cell (m=0.60, NOBAND): "
      f"{int(((K.pick_m=='0.60') & (K.pick_c=='NOBAND')).sum())} of {len(K)}")
    P(f"Chooser picks clearing 4a OOS: {int(K.keep4a_OOS.sum())}/{len(K)}; "
      f"4b OOS (costless SPY): {int(K.keep4b_OOS.sum())}/{len(K)}; "
      f"4b OOS (charged SPY): {int(K.keep4b_OOS_chg.sum())}/{len(K)}")

    P("\n" + "=" * 110); P("GATES"); P("=" * 110)
    for n, v, ok in gates: P(f"  [{'PASS' if ok else 'FAIL':4s}] {n}: {v}")
    P(f"\nGates {sum(1 for _,_,o in gates if o)}/{len(gates)}.  elapsed {time.time()-T0:.0f}s")
    P("SURVIVORSHIP: U56/B136/SMALL are CURRENT constituents; absolute levels are optimistic, "
      "SMALL worst (delisted sub-$2B names absent).")
    Path(f"{OUT}_out.txt").write_text("\n".join(lines))

if __name__ == "__main__":
    main()
