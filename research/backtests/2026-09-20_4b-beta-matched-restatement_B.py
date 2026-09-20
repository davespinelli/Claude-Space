#!/usr/bin/env python3
"""Idea 1719 (lane B, 2026-09-20) — is the 4b CAGR floor that binds at 61-78 of 80 cells
JUST THE 4b BETA LEG?

Idea 1705 found the binding 4b leg is the CAGR floor (>= 70% of SPY's CAGR), not the DD cap,
and that it binds FROM BELOW on gross — which is why every 4b pass in the record sits at the
top gross rung.  PROTOCOL rule 4b judges every book against SPY held at 100%.  A long-only
book at gross G < 1 carries beta ~G to SPY, so the DD cap is handed to it for free and the
CAGR floor is the only leg that can bite.  That is a BETA test, not an ALPHA test.

This script restates every published 4b pass against its OWN realised-beta-matched SPY blend:

    blend_t  =  b * spy_t          (the remaining 1 - b sits in CASH at 0%)

with b the book's realised beta to SPY over the SAME window the verdict is read on.  Three
things follow arithmetically and are GATED, not assumed:
  * Sharpe(blend) == Sharpe(SPY) exactly (scaling a return series leaves Sharpe fixed when
    cash earns 0), so the 4b SHARPE leg is BETA-INVARIANT;
  * MaxDD(blend) ~ b * MaxDD(SPY), so the DD cap TIGHTENS by ~b;
  * CAGR(blend) < CAGR(SPY) for b < 1, so the CAGR floor LOOSENS by ~b.
So the whole beta content of rule 4b lives in two legs that move in OPPOSITE directions, and
"how many 4b passes survive as alpha" is a real, decidable question.

Two arms:
  ARM A (census).  96 books = 3 panels x {BAND c x G, MAXVOL m x G, VOLTGT t, RULES v1}.
    For each, the PUBLISHED 4b verdict (vs SPY) and the RESTATED 4b verdict (vs its own
    beta-matched blend), on FULL and on OOS, plus the strict ALPHA test
    (CAGR_book > CAGR_blend AND Sharpe_book > Sharpe_blend on both halves / OOS).
  ARM B (capital, rule 8).  An IS-ONLY chooser (rows <= 2016-12-31) picks a book two ways —
    C_SPY  = argmax IS Sharpe among IS 4b-vs-SPY passers;
    C_ALPHA = argmax IS beta-matched alpha CAGR among IS restated-4b passers (beta fitted on
              IS rows only) — and 2017-2026 is read exactly ONCE for each pick, against
    RULES v2 (live baseline) and SPY, with both KEEP paths.

TWO tuned parameters, as the idea specifies: BETA WINDOW (full-window OLS vs mean of rolling
252d OLS) and CLAIM SET (FULL-window passes vs OOS-window passes).  ALL grid points are
published to grid.csv; no third dial is tuned anywhere in this file.

Costs 10 bps (PROTOCOL rule 2), weekly cadence, next-day execution.  Deterministic, offline,
committed caches only.  Does not modify RULES.md / scan.py / bot.py / baseline.py.
"""
import sys, os, time, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, band_state   # noqa: E402
from engine import backtest, rebalance_mask                                          # noqa: E402

OUT    = Path(__file__).resolve().parent / "2026-09-20_4b-beta-matched-restatement_B"
COST   = 10.0                            # PROTOCOL rule 2
COSTS  = [0.0, 10.0, 25.0, 50.0]         # derived exactly off the 0 bps run (gated, G2)
FREQ   = "W"
IS_END = pd.Timestamp("2016-12-31")      # PROTOCOL rule 8
WARM   = 260                             # baseline.compare() skips this many rows
BANDS  = [0.00, 0.03, 0.05, 0.10]
GROSS  = [0.30, 0.50, 0.75, 1.00]
MAXVOL = [0.40, 0.60, 0.80]
VOLTGT = [0.08, 0.12, 0.16]
RB     = 252                             # rolling-beta window (the SECOND value of param 1)


# ----------------------------------------------------------------- fast engine twin
def fast_run(px_v, w_v, mask_v, cost_bps=0.0):
    """Exact numpy translation of engine.backtest (gated against it in G1).  Run at 0 bps;
    every other cost rung is derived as r(c) = r(0) - turnover * c / 1e4, which is EXACT
    because the drift state `cur` never sees the cost (gated in G2)."""
    n = px_v.shape[0]
    rets = np.zeros_like(px_v)
    rets[1:] = px_v[1:] / px_v[:-1] - 1.0
    rets = np.nan_to_num(rets, nan=0.0, posinf=0.0, neginf=0.0)
    w_t = np.zeros_like(w_v); w_t[1:] = w_v[:-1]                 # decided at t, applied at t+1
    m = np.zeros(n, dtype=bool); m[1:] = mask_v[:-1]
    cur = np.zeros(px_v.shape[1]); turn = np.zeros(n); port = np.zeros(n); gross = np.zeros(n)
    for i in range(n):
        if m[i] or i == 0:
            turn[i] = np.abs(w_t[i] - cur).sum(); cur = w_t[i].copy()
        gross[i] = cur.sum()
        port[i] = (cur * rets[i]).sum() - turn[i] * cost_bps / 1e4
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    return port, turn, gross


def mx(r):
    """CAGR / Sharpe / MaxDD on a return array (engine.metrics arithmetic)."""
    eq = np.cumprod(1.0 + r); yrs = len(r) / 252.0
    cagr = eq[-1] ** (1.0 / yrs) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252)
    return float(cagr), float(r.mean() * 252 / vol) if vol else np.nan, dd


def windows(idx):
    full = np.zeros(len(idx), dtype=bool); full[WARM:] = True
    nf = full.sum(); h = nf // 2
    h1 = full.copy(); h1[WARM + h:] = False
    h2 = full.copy(); h2[:WARM + h] = False
    return dict(FULL=full, H1=h1, H2=h2,
                IS=full & np.asarray(idx <= IS_END), OOS=full & np.asarray(idx > IS_END))


# ----------------------------------------------------------------- beta (param 1)
def beta_full(r, s, m):
    """Full-window OLS beta of book on SPY over mask m."""
    a, b = r[m], s[m]
    v = b.var(ddof=1)
    return float(np.cov(a, b, ddof=1)[0, 1] / v) if v > 0 else np.nan


def beta_roll(r, s, m):
    """Mean of the 252d rolling OLS betas over mask m (only rows with a full window)."""
    R, S = pd.Series(r), pd.Series(s)
    cov = R.rolling(RB).cov(S); var = S.rolling(RB).var()
    b = (cov / var.replace(0.0, np.nan))
    return float(b[m].mean())


BETA_FNS = {"full": beta_full, "roll252": beta_roll}


# ----------------------------------------------------------------- 4b / 4a legs
def legs_full(row, bench):
    """PROTOCOL 4b on the FULL window against ANY benchmark dict: Sharpe in BOTH halves,
    MaxDD <= 60% of the benchmark's, CAGR >= 70% of the benchmark's."""
    return dict(S1=bool(row["H1"] > bench["H1"]), S2=bool(row["H2"] > bench["H2"]),
                DD=bool(row["MaxDD"] >= 0.60 * bench["MaxDD"]),
                CG=bool(row["CAGR"] >= 0.70 * bench["CAGR"]))


def legs_oos(row, bench):
    return dict(S1=bool(row["Sharpe"] > bench["Sharpe"]), S2=True,
                DD=bool(row["MaxDD"] >= 0.60 * bench["MaxDD"]),
                CG=bool(row["CAGR"] >= 0.70 * bench["CAGR"]))


def passed(lg): return bool(lg["S1"] and lg["S2"] and lg["DD"] and lg["CG"])


# ----------------------------------------------------------------- books
def build_books(px, panel):
    """Every book this run prices, as {name: weights DataFrame}.  SMALL carries SPY as a
    BENCHMARK column only (baseline docstring), so it is never given weight there."""
    cols = list(px.columns)
    tradable = [c for c in cols if not (panel == "SMALL" and c == "SPY")]
    sub = px[tradable]
    priced = sub.notna()
    n_priced = priced.sum(axis=1).replace(0, np.nan)
    ew_unit = priced.astype(float).div(n_priced, axis=0).fillna(0.0)      # unit gross, equal wt
    ma200 = sub.rolling(200).mean()
    above = sub > ma200
    vol20 = sub.pct_change().rolling(20).std() * np.sqrt(252)

    def widen(w):
        return w.reindex(columns=cols).fillna(0.0)

    books = {}
    for c in BANDS:
        st = band_state(sub, band=c)
        for g in GROSS:
            books[f"BAND c={c:.2f} G={g:.2f}"] = widen((g * ew_unit).where(st, 0.0))
    for m in MAXVOL:
        elig = above & (vol20 < m)
        for g in GROSS:
            books[f"MAXVOL m={m:.2f} G={g:.2f}"] = widen((g * ew_unit).where(elig, 0.0))
    ew_ret = (ew_unit.shift(1) * sub.pct_change().fillna(0.0)).sum(axis=1)   # unlevered EW panel
    pvol = ew_ret.rolling(20).std() * np.sqrt(252)
    for t in VOLTGT:
        g_t = (t / pvol.replace(0.0, np.nan)).clip(0.0, 1.0).fillna(0.0)
        books[f"VOLTGT t={t:.2f}"] = widen(ew_unit.mul(g_t, axis=0))
    books["RULESv1 n=5 w=0.15"] = widen(rules_v1_weights(sub))
    return books


# ----------------------------------------------------------------- main
def main():
    t0 = time.time(); OUT.mkdir(parents=True, exist_ok=True)
    gates, rows, picks, refs = [], [], [], []

    for panel in tuple(os.environ.get("PANELS", "U56,B136,SMALL").split(",")):
        px = load_universe(broad=(panel == "B136"), small=(panel == "SMALL")).dropna(how="all").ffill()
        idx = px.index; px_v = px.values.astype(float)
        mask_v = rebalance_mask(idx, FREQ).values
        W = windows(idx)
        spy_col = px.columns.get_loc("SPY")
        spy_r = np.zeros(len(idx)); spy_r[1:] = px_v[1:, spy_col] / px_v[:-1, spy_col] - 1.0
        spy_r = np.nan_to_num(spy_r)
        gates.append((f"G0 {panel} sample years FULL / IS / OOS", len(idx),
                      f"{W['FULL'].sum()/252:.2f}y / {W['IS'].sum()/252:.2f}y / {W['OOS'].sum()/252:.2f}y",
                      "PASS" if W["FULL"].sum() / 252 >= 10 else "FAIL"))

        def sc(r, mask_set=W):
            o = {k: mx(r[m]) for k, m in mask_set.items()}
            return dict(CAGR=o["FULL"][0], Sharpe=o["FULL"][1], MaxDD=o["FULL"][2],
                        H1=o["H1"][1], H2=o["H2"][1],
                        IS_CAGR=o["IS"][0], IS_Sharpe=o["IS"][1], IS_MaxDD=o["IS"][2],
                        OOS_CAGR=o["OOS"][0], OOS_Sharpe=o["OOS"][1], OOS_MaxDD=o["OOS"][2])

        SPY = sc(spy_r)

        # ---- G1 / G3: fast_run == engine.backtest, and the live cell IS the live book ------
        base_w = rules_v2_weights(px, band=0.03, gross=0.75)
        bp0, bt, bg = fast_run(px_v, base_w.values.astype(float), mask_v)
        eng = backtest(px, base_w, cost_bps=COST, freq=FREQ)
        fw = W["FULL"]
        d_ret = float(np.abs(eng["returns"].values[fw] - (bp0 - bt * COST / 1e4)[fw]).max())
        d_trn = float(np.abs(eng["turnover"].values[fw] - bt[fw]).max())
        gates.append((f"G1 {panel} fast_run vs engine.backtest on FULL (returns / turnover)",
                      int(fw.sum()), f"{d_ret:.3e} / {d_trn:.3e}",
                      "PASS" if max(d_ret, d_trn) < 1e-12 else "FAIL"))
        # ---- G2 cost axis exact -------------------------------------------------------
        bp10, _, _ = fast_run(px_v, base_w.values.astype(float), mask_v, cost_bps=COST)
        d_cost = float(np.abs(bp10 - (bp0 - bt * COST / 1e4)).max())
        gates.append((f"G2 {panel} derived 10 bps vs fresh 10 bps fast_run", len(idx),
                      f"{d_cost:.3e}", "PASS" if d_cost < 1e-15 else "FAIL"))
        BASE = sc(bp0 - bt * COST / 1e4)

        books = build_books(px, panel)
        if panel == "U56":
            d_live = float(np.abs(books["BAND c=0.03 G=0.75"].values - base_w.values).max())
            gates.append(("G3 U56 BAND c=0.03 G=0.75 replays baseline.rules_v2_weights",
                          int(base_w.size), f"{d_live:.3e}", "PASS" if d_live < 1e-15 else "FAIL"))

        # ---- G4 blend arithmetic ------------------------------------------------------
        b1 = mx((1.0 * spy_r)[W["FULL"]]); s0 = mx(spy_r[W["FULL"]])
        d_b1 = max(abs(b1[0] - s0[0]), abs(b1[1] - s0[1]), abs(b1[2] - s0[2]))
        sh_dev = max(abs(mx((b * spy_r)[W["FULL"]])[1] - s0[1]) for b in (0.2, 0.5, 0.8, 1.3))
        gates.append((f"G4 {panel} blend(b=1)==SPY / Sharpe(blend)==Sharpe(SPY) over b in .2-1.3",
                      4, f"{d_b1:.3e} / {sh_dev:.3e}", "PASS" if max(d_b1, sh_dev) < 1e-12 else "FAIL"))

        max_gross = 0.0
        for name, w in books.items():
            p0, tn, gr = fast_run(px_v, w.values.astype(float), mask_v)
            max_gross = max(max_gross, float(gr[fw].max()))
            for c in COSTS:
                r = p0 - tn * c / 1e4
                row = sc(r)
                rec = dict(panel=panel, book=name, cost_bps=c, **row,
                           Turn=float(tn[fw].sum() / (fw.sum() / 252.0)),
                           OOS_Turn=float(tn[W["OOS"]].sum() / (W["OOS"].sum() / 252.0)))
                # ---- published 4b (vs SPY at 100%) --------------------------------
                lf, lo = legs_full(row, SPY), legs_oos(dict(Sharpe=row["OOS_Sharpe"],
                                                            CAGR=row["OOS_CAGR"], MaxDD=row["OOS_MaxDD"]),
                                                       dict(Sharpe=SPY["OOS_Sharpe"], CAGR=SPY["OOS_CAGR"],
                                                            MaxDD=SPY["OOS_MaxDD"]))
                rec.update({f"SPY4b_FULL_{k}": v for k, v in lf.items()})
                rec.update({f"SPY4b_OOS_{k}": v for k, v in lo.items()})
                rec["SPY4b_FULL"] = passed(lf); rec["SPY4b_OOS"] = passed(lo)
                rec["keep4a"] = bool(row["H1"] > BASE["H1"] and row["H2"] > BASE["H2"]
                                     and row["MaxDD"] >= BASE["MaxDD"])
                # ---- restated against the book's own beta-matched blend ------------
                for bw, fn in BETA_FNS.items():
                    bF = fn(r, spy_r, W["FULL"]); bO = fn(r, spy_r, W["OOS"]); bI = fn(r, spy_r, W["IS"])
                    blF = sc(bF * spy_r); blO = sc(bO * spy_r)
                    lfb = legs_full(row, blF)
                    lob = legs_oos(dict(Sharpe=row["OOS_Sharpe"], CAGR=row["OOS_CAGR"], MaxDD=row["OOS_MaxDD"]),
                                   dict(Sharpe=blO["OOS_Sharpe"], CAGR=blO["OOS_CAGR"], MaxDD=blO["OOS_MaxDD"]))
                    rec[f"beta_{bw}_FULL"] = bF; rec[f"beta_{bw}_OOS"] = bO; rec[f"beta_{bw}_IS"] = bI
                    rec[f"blendCAGR_{bw}_FULL"] = blF["CAGR"]; rec[f"blendCAGR_{bw}_OOS"] = blO["OOS_CAGR"]
                    rec[f"blendDD_{bw}_FULL"] = blF["MaxDD"]; rec[f"blendDD_{bw}_OOS"] = blO["OOS_MaxDD"]
                    rec[f"alphaCAGR_{bw}_FULL"] = row["CAGR"] - blF["CAGR"]
                    rec[f"alphaCAGR_{bw}_OOS"] = row["OOS_CAGR"] - blO["OOS_CAGR"]
                    rec[f"alphaCAGR_{bw}_IS"] = (row["IS_CAGR"] - sc(bI * spy_r)["IS_CAGR"])
                    rec.update({f"B4b_{bw}_FULL_{k}": v for k, v in lfb.items()})
                    rec.update({f"B4b_{bw}_OOS_{k}": v for k, v in lob.items()})
                    rec[f"B4b_{bw}_FULL"] = passed(lfb); rec[f"B4b_{bw}_OOS"] = passed(lob)
                    # strict ALPHA test: beats its own blend on CAGR and on Sharpe
                    rec[f"ALPHA_{bw}_FULL"] = bool(lfb["S1"] and lfb["S2"] and rec[f"alphaCAGR_{bw}_FULL"] > 0)
                    rec[f"ALPHA_{bw}_OOS"] = bool(lob["S1"] and rec[f"alphaCAGR_{bw}_OOS"] > 0)
                rows.append(rec)
        gates.append((f"G8 {panel} max realised gross on FULL (no leverage, no shorting)",
                      len(books), f"{max_gross:.6f}", "PASS" if max_gross <= 1.0 + 1e-12 else "FAIL"))

        # ---- ARM B: rule-8 IS-only choosers -------------------------------------------
        at10 = [r for r in rows if r["panel"] == panel and r["cost_bps"] == COST]

        def is_pass_spy(r):
            return bool(r["IS_Sharpe"] > SPY["IS_Sharpe"] and r["IS_MaxDD"] >= 0.60 * SPY["IS_MaxDD"]
                        and r["IS_CAGR"] >= 0.70 * SPY["IS_CAGR"])

        def chooser(kind, bw="full"):
            if kind == "C_SPY":
                cand = [r for r in at10 if is_pass_spy(r)]
                key = lambda r: r["IS_Sharpe"]
            else:
                cand = [r for r in at10 if is_pass_spy(r) and r[f"alphaCAGR_{bw}_IS"] > 0]
                key = lambda r: r[f"alphaCAGR_{bw}_IS"]
            if not cand: return None
            return max(sorted(cand, key=lambda r: r["book"]), key=key)

        for kind in ("C_SPY", "C_ALPHA"):
            pick = chooser(kind)
            picks.append(dict(panel=panel, chooser=kind,
                              book=pick["book"] if pick else "(no IS candidate)",
                              **({k: pick[k] for k in ("IS_Sharpe", "IS_CAGR", "IS_MaxDD",
                                                       "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
                                                       "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                                       "SPY4b_FULL", "SPY4b_OOS", "keep4a",
                                                       "B4b_full_FULL", "B4b_full_OOS",
                                                       "ALPHA_full_FULL", "ALPHA_full_OOS",
                                                       "alphaCAGR_full_OOS", "beta_full_OOS",
                                                       "OOS_Turn")} if pick else {})))
        # ---- G6: no chooser reads a 2017+ row -----------------------------------------
        cut = int(np.searchsorted(idx.values, np.datetime64(IS_END)) + 1)
        keys_is = ("IS_Sharpe", "IS_CAGR", "IS_MaxDD", "alphaCAGR_full_IS", "alphaCAGR_roll252_IS")
        trunc_ok = True
        for r in at10[:6]:                       # recompute IS stats on a HARD-TRUNCATED tape
            w = books[r["book"]].values.astype(float)[:cut]
            p0, tn, _ = fast_run(px_v[:cut], w, mask_v[:cut])
            rr = p0 - tn * COST / 1e4
            m = W["IS"][:cut]
            c_, s_, d_ = mx(rr[m])
            bI = beta_full(rr, spy_r[:cut], m)
            a_ = c_ - mx((bI * spy_r[:cut])[m])[0]
            trunc_ok &= (abs(s_ - r["IS_Sharpe"]) < 1e-12 and abs(c_ - r["IS_CAGR"]) < 1e-12
                         and abs(d_ - r["IS_MaxDD"]) < 1e-12 and abs(a_ - r["alphaCAGR_full_IS"]) < 1e-12)
        gates.append((f"G6 {panel} IS stats + IS alpha identical on a hard-truncated tape "
                      f"(chooser cannot see 2017+)", 6 * len(keys_is),
                      "identical" if trunc_ok else "DIFFER", "PASS" if trunc_ok else "FAIL"))

        refs.append(dict(panel=panel, book="SPY (buy & hold)", cost_bps=0.0, **SPY))
        refs.append(dict(panel=panel, book="RULES v2 baseline (live)", cost_bps=COST, **BASE))

    grid = pd.DataFrame(rows)
    ref = pd.DataFrame(refs)
    grid.to_csv(OUT / "grid.csv", index=False)
    ref.to_csv(OUT / "reference.csv", index=False)
    pk = pd.DataFrame(picks); pk.to_csv(OUT / "picks.csv", index=False)
    gates.append(("G5 tuned parameters in this file (beta window, claim set)", 2,
                  "beta_window in {full, roll252}; claim_set in {FULL, OOS}",
                  "PASS"))
    gates.append(("G7 grid cells published", len(grid), f"{len(grid)} of {len(grid)}", "PASS"))

    # =================================================================== ARM A report
    print("=" * 104)
    print("ARM A — CENSUS: does a published 4b pass survive its own realised-beta-matched SPY blend?")
    print("=" * 104)
    g10 = grid[grid["cost_bps"] == COST]
    lines = []
    for claim in ("FULL", "OOS"):
        for bw in ("full", "roll252"):
            sel = g10[g10[f"SPY4b_{claim}"]]
            n = len(sel)
            sur = int(sel[f"B4b_{bw}_{claim}"].sum()); alp = int(sel[f"ALPHA_{bw}_{claim}"].sum())
            pos = int((sel[f"alphaCAGR_{bw}_{claim}"] > 0).sum())
            mb = sel[f"beta_{bw}_{claim}"].mean() if n else np.nan
            ma = sel[f"alphaCAGR_{bw}_{claim}"].mean() if n else np.nan
            lines.append(dict(claim_set=claim, beta_window=bw, published_4b_passes=n,
                              restated_4b_pass=sur, strict_ALPHA_pass=alp, alphaCAGR_gt0=pos,
                              mean_beta=mb, mean_alphaCAGR=ma))
            # leg autopsy on the restated verdict
            for leg, lab in (("S1", "Sharpe H1/OOS"), ("S2", "Sharpe H2"), ("DD", "MaxDD cap"), ("CG", "CAGR floor")):
                lines[-1][f"restated_fail_{leg}"] = int((~sel[f"B4b_{bw}_{claim}_{leg}"]).sum()) if n else 0
    census = pd.DataFrame(lines); census.to_csv(OUT / "census.csv", index=False)
    print(census.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\nPublished 4b passes by panel (cost 10 bps):")
    for claim in ("FULL", "OOS"):
        t = g10[g10[f"SPY4b_{claim}"]].groupby("panel").size()
        print(f"  claim_set={claim}: " + (", ".join(f"{k}={v}" for k, v in t.items()) if len(t) else "none"))

    print("\nWHICH LEG BINDS in the PUBLISHED (vs-SPY) 4b test, all %d cells at 10 bps:" % len(g10))
    for claim in ("FULL", "OOS"):
        f = {leg: int((~g10[f"SPY4b_{claim}_{leg}"]).sum()) for leg in ("S1", "S2", "DD", "CG")}
        print(f"  {claim}: fails Sharpe1 {f['S1']}, Sharpe2 {f['S2']}, DDcap {f['DD']}, CAGRfloor {f['CG']}"
              f"  (of {len(g10)})")

    print("\nThe standing 4b candidates, restated (10 bps, beta window = full):")
    watch = g10[g10["book"].isin(["BAND c=0.10 G=1.00", "VOLTGT t=0.16", "VOLTGT t=0.12",
                                  "BAND c=0.03 G=0.75"])]
    cols = ["panel", "book", "CAGR", "Sharpe", "MaxDD", "SPY4b_FULL", "SPY4b_OOS",
            "beta_full_FULL", "blendCAGR_full_FULL", "alphaCAGR_full_FULL", "B4b_full_FULL",
            "beta_full_OOS", "alphaCAGR_full_OOS", "B4b_full_OOS", "ALPHA_full_OOS"]
    print(watch[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\nCost robustness — published vs restated 4b pass counts at every cost rung:")
    cr = []
    for c in COSTS:
        gc = grid[grid["cost_bps"] == c]
        cr.append(dict(cost_bps=c, SPY4b_FULL=int(gc["SPY4b_FULL"].sum()),
                       B4b_FULL=int(gc[gc["SPY4b_FULL"]]["B4b_full_FULL"].sum()),
                       ALPHA_FULL=int(gc[gc["SPY4b_FULL"]]["ALPHA_full_FULL"].sum()),
                       SPY4b_OOS=int(gc["SPY4b_OOS"].sum()),
                       B4b_OOS=int(gc[gc["SPY4b_OOS"]]["B4b_full_OOS"].sum()),
                       ALPHA_OOS=int(gc[gc["SPY4b_OOS"]]["ALPHA_full_OOS"].sum())))
    print(pd.DataFrame(cr).to_string(index=False))

    # =================================================================== ARM B report
    print("\n" + "=" * 104)
    print("ARM B — CAPITAL, rule 8: IS-only chooser (2009-2016), 2017-2026 read ONCE")
    print("=" * 104)
    show = ["panel", "chooser", "book", "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
            "beta_full_OOS", "alphaCAGR_full_OOS", "SPY4b_OOS", "B4b_full_OOS", "ALPHA_full_OOS",
            "keep4a", "OOS_Turn"]
    print(pk[show].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\nReference rows (OOS 2017-2026):")
    print(ref[["panel", "book", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
               "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]].to_string(index=False,
                                                                 float_format=lambda x: f"{x:.4f}"))

    gdf = pd.DataFrame(gates, columns=["gate", "n", "value", "status"])
    gdf.to_csv(OUT / "gates.csv", index=False)
    print("\nGATES\n" + gdf.to_string(index=False))
    print(f"\nrows={len(grid)+len(ref)}  grid_cells={len(grid)}  elapsed={time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
