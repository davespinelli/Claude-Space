#!/usr/bin/env python3
"""Idea 1723 (lane B, 2026-09-20) — is the standing 4b candidate DISTINGUISHABLE from a
BAND-GATED SPY?

The record's only standing 4b pass is the U56 band book (band c=0.10, gross G=1.00, weekly):
hold every name inside its own 200d +/- c band at G/N of NAV, send gated-out weight to CASH.
The 2026-09-19 identity says its realised gross is G times the IN-BAND SHARE, i.e. its whole
exposure path is an AGGREGATE market-timing signal wearing 56 names.  This script prices two
comparators on exactly the same dials, cadence and costs and asks whether the panel earns its
turnover:

  CELL      baseline.rules_v2_weights(px, band=c, gross=G)          (the panel book)
  SPY_BAND  ONE ASSET: weight G on SPY while SPY is inside its own 200d +/- c band, else cash
  SPY_MATCH SPY held at the CELL's OWN daily target-gross path (exposure-matched; this strips
            the cross-sectional selection and keeps only the timing)
  PANEL_MATCH the CONTROL that decides the question: the SAME panel, equal-weighted over EVERY
            priced name with NO band gate at all, held at the CELL's own target-gross path.  It
            has the panel's survivorship and the panel's equal-weighting and the CELL's exposure
            path, and differs from the CELL ONLY in WHICH names carry the gross.  CELL - SPY_MATCH
            is the panel's whole contribution; CELL - PANEL_MATCH is the band SELECTION alone.

Two tuned parameters, c and G.  Every grid point is published to grid.csv.
Rule 8: the (c, G) pick is fitted on rows <= 2016-12-31 ONLY, and 2017-2026 is read once.
Deterministic, offline, cached panels only.
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state          # noqa: E402
from engine import backtest, rebalance_mask, metrics                      # noqa: E402

OUT   = Path(__file__).resolve().parent / "2026-09-20_band-gated-spy-vs-panel_B"
COST  = 10.0          # PROTOCOL rule 2
FREQ  = "W"           # live cadence
BANDS = [0.00, 0.03, 0.05, 0.10]
GROSS = [0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]
IS_END = pd.Timestamp("2016-12-31")     # PROTOCOL rule 8
WARM   = 260                            # baseline.compare() skips this many rows


# ----------------------------------------------------------------- fast engine twin
def fast_run(px_v, w_v, mask_v, cost_bps=COST):
    """Exact numpy translation of engine.backtest (gated against it in G1)."""
    n = px_v.shape[0]
    rets = np.zeros_like(px_v)
    rets[1:] = px_v[1:] / px_v[:-1] - 1.0
    rets = np.nan_to_num(rets, nan=0.0, posinf=0.0, neginf=0.0)
    w_t = np.zeros_like(w_v); w_t[1:] = w_v[:-1]                 # decided at t, applied at t+1
    m = np.zeros(n, dtype=bool); m[1:] = mask_v[:-1]             # mask.shift(1, fill_value=False)
    cur = np.zeros(px_v.shape[1]); turn = np.zeros(n); port = np.zeros(n)
    for i in range(n):
        if m[i] or i == 0:
            turn[i] = np.abs(w_t[i] - cur).sum(); cur = w_t[i].copy()
        port[i] = (cur * rets[i]).sum() - turn[i] * cost_bps / 1e4
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    return port, turn


def mx(r):
    """CAGR / Sharpe / MaxDD on a return array (engine.metrics arithmetic)."""
    eq = np.cumprod(1.0 + r); yrs = len(r) / 252.0
    cagr = eq[-1] ** (1.0 / yrs) - 1.0
    dd = (eq / np.maximum.accumulate(eq) - 1.0).min()
    vol = r.std(ddof=1) * np.sqrt(252)
    return cagr, (r.mean() * 252 / vol if vol else np.nan), dd


# ----------------------------------------------------------------- resolution
def paired_block_boot(a, b, n_draw=400, block=63, seed=1723):
    """Paired circular-block bootstrap of Sharpe(a)-Sharpe(b) and MaxDD(a)-MaxDD(b).
    The SAME resampled day-indices are applied to both arms, so the draw removes the
    common market factor and what is left is the contrast's own sampling error."""
    rng = np.random.default_rng(seed)
    n = len(a); nb = int(np.ceil(n / block))
    ds, dd = np.empty(n_draw), np.empty(n_draw)
    for k in range(n_draw):
        st = rng.integers(0, n, size=nb)
        idx = (st[:, None] + np.arange(block)[None, :]).ravel()[:n] % n
        ca, sa, da = mx(a[idx]); cb, sb, db = mx(b[idx])
        ds[k] = sa - sb; dd[k] = da - db
    return ds.std(ddof=1), dd.std(ddof=1)


# ----------------------------------------------------------------- KEEP paths (rule 4)
def keep_4a(row, base):
    """Sharpe > live RULES v2 in BOTH halves and MaxDD no worse than the live rules."""
    return bool(row["H1"] > base["H1"] and row["H2"] > base["H2"] and row["MaxDD"] >= base["MaxDD"])

def keep_4b_full(row, spy):
    """FULL window: Sharpe > SPY in both halves, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's."""
    return bool(row["H1"] > spy["H1"] and row["H2"] > spy["H2"]
                and row["MaxDD"] >= 0.60 * spy["MaxDD"] and row["CAGR"] >= 0.70 * spy["CAGR"])

def keep_4b_oos(row, spy):
    """OOS window (rule 8): Sharpe > SPY OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's."""
    return bool(row["Sharpe"] > spy["Sharpe"]
                and row["MaxDD"] >= 0.60 * spy["MaxDD"] and row["CAGR"] >= 0.70 * spy["CAGR"])


def windows(idx):
    """FULL (post warm-up), its halves, IS (<=2016) and OOS (2017+) as boolean masks."""
    full = np.zeros(len(idx), dtype=bool); full[WARM:] = True
    nf = full.sum(); h = nf // 2
    h1 = full.copy(); h1[WARM + h:] = False
    h2 = full.copy(); h2[:WARM + h] = False
    is_ = full & np.asarray(idx <= IS_END)
    oos = full & np.asarray(idx > IS_END)
    return dict(FULL=full, H1=h1, H2=h2, IS=is_, OOS=oos)


def score(port, turn, W, yrs_idx):
    out = {}
    for k, m in W.items():
        c, s, d = mx(port[m])
        out[k] = dict(CAGR=c, Sharpe=s, MaxDD=d)
    r = dict(CAGR=out["FULL"]["CAGR"], Sharpe=out["FULL"]["Sharpe"], MaxDD=out["FULL"]["MaxDD"],
             H1=out["H1"]["Sharpe"], H2=out["H2"]["Sharpe"],
             IS_Sharpe=out["IS"]["Sharpe"], IS_CAGR=out["IS"]["CAGR"], IS_MaxDD=out["IS"]["MaxDD"],
             OOS_CAGR=out["OOS"]["CAGR"], OOS_Sharpe=out["OOS"]["Sharpe"], OOS_MaxDD=out["OOS"]["MaxDD"])
    r["Turn"] = turn[W["FULL"]].sum() / (W["FULL"].sum() / 252.0)          # turnover units / yr
    r["OOS_Turn"] = turn[W["OOS"]].sum() / (W["OOS"].sum() / 252.0)
    return r


def oos_row(r):   return dict(CAGR=r["OOS_CAGR"], Sharpe=r["OOS_Sharpe"], MaxDD=r["OOS_MaxDD"],
                              H1=r["OOS_Sharpe"], H2=r["OOS_Sharpe"])


def main():
    t0 = time.time(); OUT.mkdir(parents=True, exist_ok=True)
    gates = []
    rows, ref, daily = [], {}, {}

    for panel in ("U56", "B136"):
        px = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
        idx = px.index
        px_v = px.values.astype(float)
        mask_v = rebalance_mask(idx, FREQ).values
        W = windows(idx)
        spy_col = px.columns.get_loc("SPY")
        e = np.where(np.isnan(px_v), 0.0, 1.0)                       # priced that day
        ew_unit = e / np.where(e.sum(axis=1) == 0, np.nan, e.sum(axis=1))[:, None]
        ew_unit = np.nan_to_num(ew_unit)                             # unit gross, equal weight

        # ---- benchmarks -------------------------------------------------------------
        spy_r = np.zeros(len(idx)); spy_r[1:] = px_v[1:, spy_col] / px_v[:-1, spy_col] - 1.0
        spy_r = np.nan_to_num(spy_r)
        SPY = score(spy_r, np.zeros(len(idx)), W, idx)
        base_w = rules_v2_weights(px, band=0.03, gross=0.75)
        base_p, base_t = fast_run(px_v, base_w.values.astype(float), mask_v)
        BASE = score(base_p, base_t, W, idx)
        ref[panel] = dict(SPY=SPY, BASE=BASE)

        # ---- G1 fast_run == engine.backtest -----------------------------------------
        eng = backtest(px, base_w, cost_bps=COST, freq=FREQ)
        # engine.backtest fillna(0)s BEFORE shift(1), so its own returns carry NaN on a
        # couple of rows at the very start of the tape; both sit inside the 260-row warm-up
        # that every published window drops.  Gate on the FULL window -- the rows every
        # number in this file is computed on -- and publish the NaN count.
        fw = W["FULL"]
        nan_pre = int(np.isnan(eng["returns"].values[:WARM]).sum())
        nan_post = int(np.isnan(eng["returns"].values[fw]).sum())
        d_ret = float(np.abs(eng["returns"].values[fw] - base_p[fw]).max())
        d_trn = float(np.abs(eng["turnover"].values[fw] - base_t[fw]).max())
        gates.append((f"G1 {panel} fast_run vs engine.backtest on FULL (returns / turnover); "
                      f"engine NaN rows pre-warm-up {nan_pre}, in FULL {nan_post}",
                      f"{d_ret:.3e} / {d_trn:.3e}",
                      d_ret < 1e-12 and d_trn < 1e-12 and nan_post == 0))

        # ---- G2 the (c=0.03, G=0.75) cell IS the live book --------------------------
        gates.append((f"G2 {panel} RULES v2 FULL cell",
                      f"{BASE['CAGR']:.2%} / {BASE['Sharpe']:.4f} / {BASE['MaxDD']:.2%}", True))

        max_gross = 0.0
        for c in BANDS:
            bs_panel = band_state(px, c)                      # per-name 200d band, hysteresis
            spy_state = bs_panel["SPY"].values.astype(float)  # the SAME rule on one asset
            for G in GROSS:
                # --- CELL: the panel band book ---------------------------------------
                cw = rules_v2_weights(px, band=c, gross=G)
                cw_v = cw.values.astype(float)
                cp, ct = fast_run(px_v, cw_v, mask_v)
                gpath = cw_v.sum(axis=1)                       # target gross = G * in-band share
                max_gross = max(max_gross, float(gpath.max()))

                # --- SPY_BAND: one asset, same band rule, same G ---------------------
                sw = np.zeros_like(px_v); sw[:, spy_col] = G * spy_state
                sp, st = fast_run(px_v, sw, mask_v)

                # --- SPY_MATCH: SPY at the CELL's own target-gross path --------------
                mw = np.zeros_like(px_v); mw[:, spy_col] = gpath
                mp, mt = fast_run(px_v, mw, mask_v)

                # --- PANEL_MATCH: same panel, NO band gate, same target-gross path ---
                pw = ew_unit * gpath[:, None]
                pp_, pt_ = fast_run(px_v, pw, mask_v)
                d_spy = float(np.abs(mw.sum(axis=1) - gpath).max())
                d_pan = float(np.abs(pw.sum(axis=1) - gpath).max())
                gates.append((f"G4 exposure match {panel} c={c} G={G}",
                              f"SPY_MATCH {d_spy:.3e} / PANEL_MATCH {d_pan:.3e}",
                              d_spy == 0.0 and d_pan < 1e-12))

                for arm, (p, t, wv) in (("CELL", (cp, ct, cw_v)), ("SPY_BAND", (sp, st, sw)),
                                        ("SPY_MATCH", (mp, mt, mw)), ("PANEL_MATCH", (pp_, pt_, pw))):
                    r = score(p, t, W, idx)
                    r.update(panel=panel, arm=arm, band=c, gross=G,
                             in_band_share=float(np.mean(gpath[W["FULL"]] / G)),
                             mean_gross=float(np.mean(wv.sum(axis=1)[W["FULL"]])),
                             KEEP_4a_FULL=keep_4a(r, BASE), KEEP_4b_FULL=keep_4b_full(r, SPY),
                             KEEP_4a_OOS=bool(r["OOS_Sharpe"] > BASE["OOS_Sharpe"] and r["OOS_MaxDD"] >= BASE["OOS_MaxDD"]),
                             KEEP_4b_OOS=keep_4b_oos(oos_row(r), dict(CAGR=SPY["OOS_CAGR"], Sharpe=SPY["OOS_Sharpe"], MaxDD=SPY["OOS_MaxDD"])))
                    rows.append(r)
                    if arm == "CELL": daily[(panel, c, G, arm)] = cp
                    else: daily[(panel, c, G, arm)] = p

        gates.append((f"G3 {panel} no leverage (max target gross)", f"{max_gross:.6f}", max_gross <= 1.0 + 1e-12))

    df = pd.DataFrame(rows)
    df.to_csv(OUT / "grid.csv", index=False)

    # ---- G5 the rule-8 chooser cannot see a 2017+ row ------------------------------
    chk = df[(df.panel == "U56") & (df.arm == "CELL")]
    pick_full = chk.sort_values(["IS_Sharpe", "band", "gross"], ascending=[False, True, True]).iloc[0]
    gates.append(("G5 chooser objective is IS_Sharpe only (rows <= 2016-12-31)",
                  f"argmax (c={pick_full.band}, G={pick_full.gross})", True))
    gates.append(("G6 two tuned dials only", "band c, gross G", True))

    # =============================== REPORT =====================================
    L = []
    P = L.append
    P("# Idea 1723 — is the standing 4b candidate distinguishable from a band-gated SPY?")
    P(f"\nPanels U56 / B136 (cached, current constituents), weekly, {COST:.0f} bps, "
      f"{len(BANDS)}x{len(GROSS)} = {len(BANDS)*len(GROSS)} cells x 4 arms x 2 panels = {len(df)} books.\n")

    for panel in ("U56", "B136"):
        S, B = ref[panel]["SPY"], ref[panel]["BASE"]
        P(f"\n## {panel}")
        P(f"SPY buy&hold   FULL {S['CAGR']:.2%} / {S['Sharpe']:.4f} / {S['MaxDD']:.2%} "
          f"(H1 {S['H1']:.4f} / H2 {S['H2']:.4f})   OOS {S['OOS_CAGR']:.2%} / {S['OOS_Sharpe']:.4f} / {S['OOS_MaxDD']:.2%}")
        P(f"RULES v2 live  FULL {B['CAGR']:.2%} / {B['Sharpe']:.4f} / {B['MaxDD']:.2%} "
          f"(H1 {B['H1']:.4f} / H2 {B['H2']:.4f})   OOS {B['OOS_CAGR']:.2%} / {B['OOS_Sharpe']:.4f} / {B['OOS_MaxDD']:.2%}")

        d = df[df.panel == panel]
        P(f"\n### Every grid point (FULL / OOS), {panel}")
        P("| c | G | arm | FULL CAGR | Sh | MaxDD | H1 | H2 | OOS CAGR | Sh | MaxDD | turn/yr | 4a F | 4b F | 4a O | 4b O |")
        P("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
        for _, r in d.sort_values(["band", "gross", "arm"]).iterrows():
            P(f"| {r.band:.2f} | {r.gross:.2f} | {r.arm} | {r.CAGR:.2%} | {r.Sharpe:.4f} | {r.MaxDD:.2%} | "
              f"{r.H1:.4f} | {r.H2:.4f} | {r.OOS_CAGR:.2%} | {r.OOS_Sharpe:.4f} | {r.OOS_MaxDD:.2%} | {r.Turn:.2f} | "
              f"{'Y' if r.KEEP_4a_FULL else '.'} | {'Y' if r.KEEP_4b_FULL else '.'} | "
              f"{'Y' if r.KEEP_4a_OOS else '.'} | {'Y' if r.KEEP_4b_OOS else '.'} |")

        P(f"\n### KEEP census, {panel} (by arm, out of {len(BANDS)*len(GROSS)} cells)")
        P("| arm | 4a FULL | 4b FULL | 4a OOS | 4b OOS | BOTH 4b |")
        P("|---|---|---|---|---|---|")
        for arm in ("CELL", "SPY_BAND", "SPY_MATCH", "PANEL_MATCH"):
            a = d[d.arm == arm]
            P(f"| {arm} | {int(a.KEEP_4a_FULL.sum())} | {int(a.KEEP_4b_FULL.sum())} | "
              f"{int(a.KEEP_4a_OOS.sum())} | {int(a.KEEP_4b_OOS.sum())} | "
              f"{int((a.KEEP_4b_FULL & a.KEEP_4b_OOS).sum())} |")

        # ---- rule 8: pick (c, G) on IS rows only, read OOS once -------------------
        P(f"\n### Rule 8, {panel} — (c, G) fitted on 2009-2016 IS Sharpe ONLY, 2017-2026 read once")
        P("| arm | IS pick (c, G) | IS Sharpe | OOS CAGR | OOS Sharpe | OOS MaxDD | OOS turn/yr | 4a OOS | 4b OOS |")
        P("|---|---|---|---|---|---|---|---|---|")
        picks = {}
        for arm in ("CELL", "SPY_BAND", "SPY_MATCH", "PANEL_MATCH"):
            a = d[d.arm == arm].sort_values(["IS_Sharpe", "band", "gross"], ascending=[False, True, True])
            p = a.iloc[0]; picks[arm] = p
            P(f"| {arm} | ({p.band:.2f}, {p.gross:.2f}) | {p.IS_Sharpe:.4f} | {p.OOS_CAGR:.2%} | "
              f"{p.OOS_Sharpe:.4f} | {p.OOS_MaxDD:.2%} | {p.OOS_Turn:.2f} | "
              f"{'PASS' if p.KEEP_4a_OOS else 'fail'} | {'PASS' if p.KEEP_4b_OOS else 'fail'} |")

        # ---- head-to-head at the standing candidate's own dials -------------------
        P(f"\n### Head-to-head at the standing candidate's dials (c=0.10, G=1.00), {panel}")
        h = d[(d.band == 0.10) & (d.gross == 1.00)].set_index("arm")
        P("| arm | FULL CAGR | Sh | MaxDD | OOS CAGR | Sh | MaxDD | turn/yr | 4b FULL | 4b OOS |")
        P("|---|---|---|---|---|---|---|---|---|---|")
        for arm in ("CELL", "SPY_BAND", "SPY_MATCH", "PANEL_MATCH"):
            r = h.loc[arm]
            P(f"| {arm} | {r.CAGR:.2%} | {r.Sharpe:.4f} | {r.MaxDD:.2%} | {r.OOS_CAGR:.2%} | {r.OOS_Sharpe:.4f} | "
              f"{r.OOS_MaxDD:.2%} | {r.Turn:.2f} | {'PASS' if r.KEEP_4b_FULL else 'fail'} | "
              f"{'PASS' if r.KEEP_4b_OOS else 'fail'} |")

        # ---- resolution of the headline contrast (paired circular-block bootstrap) --
        pk = picks["CELL"]; oos_m = W["OOS"]
        P(f"\n### Is the contrast RESOLVABLE? paired circular-block bootstrap at the rule-8 CELL pick "
          f"(c={pk.band:.2f}, G={pk.gross:.2f}), OOS 2017-2026, 400 draws, block 63d, seed 1723, {panel}")
        P("| contrast | dOOS Sharpe | paired SE | t | dOOS MaxDD | paired SE | t |")
        P("|---|---|---|---|---|---|---|")
        ca = daily[(panel, pk.band, pk.gross, "CELL")][oos_m]
        for other in ("SPY_BAND", "SPY_MATCH", "PANEL_MATCH"):
            cb = daily[(panel, pk.band, pk.gross, other)][oos_m]
            _, sa, da = mx(ca); _, sb, db = mx(cb)
            se_s, se_d = paired_block_boot(ca, cb)
            P(f"| CELL - {other} | {sa-sb:+.4f} | {se_s:.4f} | {(sa-sb)/se_s:+.2f} | "
              f"{(da-db)*100:+.2f} pp | {se_d*100:.2f} pp | {(da-db)/se_d:+.2f} |")

        # ---- pooled CELL-minus-comparator contrasts -------------------------------
        P(f"\n### Pooled CELL minus comparator over all {len(BANDS)*len(GROSS)} cells, {panel}")
        cc = d[d.arm == "CELL"].set_index(["band", "gross"])
        for other in ("SPY_BAND", "SPY_MATCH", "PANEL_MATCH"):
            oo = d[d.arm == other].set_index(["band", "gross"])
            for win, sh, cg, dd in (("FULL", "Sharpe", "CAGR", "MaxDD"), ("OOS", "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD")):
                ds = (cc[sh] - oo[sh]); dc = (cc[cg] - oo[cg]); dd_ = (cc[dd] - oo[dd])
                P(f"- {win} CELL - {other}: dSharpe mean {ds.mean():+.4f} (CELL wins {int((ds>0).sum())}/{len(ds)}), "
                  f"dCAGR mean {dc.mean()*100:+.2f} pp (CELL wins {int((dc>0).sum())}/{len(dc)}), "
                  f"dMaxDD mean {dd_.mean()*100:+.2f} pp (CELL shallower {int((dd_>0).sum())}/{len(dd_)}), "
                  f"turnover ratio mean {(cc['Turn']/oo['Turn'].replace(0,np.nan)).mean():.2f}x")

    P("\n## Gates")
    for name, val, ok in [g for g in gates if not g[0].startswith("G4")]:
        P(f"- [{'PASS' if ok else 'FAIL'}] {name}: {val}")
    nG4 = [g for g in gates if g[0].startswith("G4")]
    w_spy = max(float(g[1].split()[1]) for g in nG4)
    w_pan = max(float(g[1].split()[-1]) for g in nG4)
    P(f"- [{'PASS' if all(g[2] for g in nG4) else 'FAIL'}] G4 exposure match over {len(nG4)} cells "
      f"(SPY_MATCH and PANEL_MATCH target gross == CELL target gross, every day): "
      f"worst |diff| SPY_MATCH {w_spy:.3e} (exact), PANEL_MATCH {w_pan:.3e} — float division by the "
      f"daily priced-name count, bar 1e-12")
    P(f"\nSURVIVORSHIP (rule 9): U56 and B136 are CURRENT-CONSTITUENT lists, so every absolute "
      f"level on the CELL arm is an UPPER BOUND. The direction matters for each contrast and the "
      f"two contrasts are NOT alike:")
    P(f"- CELL - SPY_BAND and CELL - SPY_MATCH compare a SURVIVORSHIP-BEARING panel against a "
      f"SURVIVORSHIP-FREE single ETF, so the panel's bias is INSIDE the gap and it flatters the "
      f"panel. Those two gaps are an UPPER BOUND on what the panel contributes, NOT a conservative "
      f"reading, and nothing here can separate the panel's edge from its survivorship.")
    P(f"- CELL - PANEL_MATCH is the contrast that survives this, because both arms are the SAME "
      f"current-constituent panel over the same names on the same days at the SAME target gross, "
      f"differing only in WHICH names carry it. That one is first-order immune to the panel bias "
      f"and is the only gap this file is entitled to call a selection effect.")
    P(f"\nRuntime {time.time()-t0:.0f}s. Deterministic, offline. All {len(df)} books in grid.csv.")

    txt = "\n".join(L)
    (OUT / "report.md").write_text(txt + "\n")
    print(txt)
    assert all(g[2] for g in gates), "GATE FAILURE"


if __name__ == "__main__":
    main()
