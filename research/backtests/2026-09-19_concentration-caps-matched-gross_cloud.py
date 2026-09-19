#!/usr/bin/env python3
"""Idea 1686 (lane cloud, 2026-09-19) — DOES THE KEEP-4b BOOK SURVIVE A PER-NAME AND
PER-GROUP CONCENTRATION CAP AT MATCHED REALISED GROSS?

The standing 4b line is the 200d +/-3% band book.  Real capital cannot hold an uncapped
book, and the record's own nine-run lesson (every device is beaten at matched exposure by a
plain de-gross) says a cap must be priced against a REALISED-GROSS-MATCHED twin, not against
the uncapped book.

DIALS (2, the protocol maximum)
  cap_name   c_N in {0.02, 0.04, 0.06, 0.10, 0.20, inf}   fraction of NAV, per NAME
  cap_group  c_G in {0.20, 0.30, 0.45, inf}               fraction of NAV, per research/universe.json GROUP
                                                          (U56 only: B136 and SMALL have no committed groups)

PUBLISHED, NOT TUNED (every cell printed)
  BOOK   DEGROSS  = the committed recipe: gross/N_priced on every in-band name, gated-out
                    weight to CASH, never re-spread (baseline.rules_v2_weights)
         INBAND   = the same band, gross/N_inband, i.e. full exposure concentrated on the
                    names that are in the band -- the construction a cap is actually FOR
  PANEL  U56 / B136 / SMALL (sub-$2B, max_1d_move < 1.0, survivorship-caveated)
  GROSS  0.75 (live) and 1.00 (the only gross at which the band book clears 4b FULL-and-OOS)

SPILL convention (fixed, stated, not tuned): capped-away weight is re-spread to names that
still have BOTH name and group headroom; whatever cannot be placed goes to CASH.

Every capped book is priced against its OWN realised-mean-gross-matched twin: the same
uncapped book scaled so its realised mean gross equals the capped book's.

Costs 10 bps / unit turnover, weekly, decided at t applied at t+1 (PROTOCOL 2).
Rule 8: caps chosen on IS (<= 2016-12-31) by three legal IS-only choosers, OOS (2017+) read once.
"""
import sys, json, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state          # noqa
from engine import backtest, rebalance_mask, metrics                      # noqa

OUT = ROOT / "research" / "backtests"
STAMP = "2026-09-19_concentration-caps-matched-gross_cloud"
COST = 10.0
FREQ = "W"
BAND = 0.03
IS_END = "2016-12-31"
CAP_N = [0.02, 0.04, 0.06, 0.10, 0.20, np.inf]
CAP_G = [0.20, 0.30, 0.45, np.inf]
GROSSES = [0.75, 1.00]
LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ---------------------------------------------------------------- panels
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    say(f"SMALL: {px.shape[1]-1} names priced, dropped {px.shape[1]-len(keep)} with max_1d_move >= 1.0"
        f" -> {len(keep)-1} names (SURVIVORSHIP: current constituents of the screen only)")
    return px[keep]


# ---------------------------------------------------------------- fast replay of engine.backtest
def fast_bt(px, W, cost_bps=COST, freq=FREQ):
    """Bit-for-bit replay of engine.backtest (gated below), in numpy."""
    P = px.values
    R = np.zeros_like(P, dtype=float)
    R[1:] = P[1:] / P[:-1] - 1.0
    R = np.nan_to_num(R, nan=0.0, posinf=0.0, neginf=0.0)
    Wv = np.nan_to_num(W.reindex(px.index).values.astype(float), nan=0.0)
    Ws = np.zeros_like(Wv); Ws[1:] = Wv[:-1]                       # weights.shift(1)
    m = rebalance_mask(px.index, freq).values
    ms = np.zeros(len(P), dtype=bool); ms[1:] = m[:-1]             # mask.shift(1)
    T, N = P.shape
    cur = np.zeros(N)
    port = np.zeros(T); gross = np.zeros(T); turn = np.zeros(T)
    for i in range(T):
        if ms[i] or i == 0:
            new = Ws[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new.copy()
        gross[i] = cur.sum()
        port[i] = float(cur @ R[i]) - turn[i] * cost_bps / 1e4
        growth = cur * (1.0 + R[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    idx = px.index
    return (pd.Series(port, index=idx), pd.Series(gross, index=idx), pd.Series(turn, index=idx))


# ---------------------------------------------------------------- books
def inband_mask(px, band=BAND):
    return band_state(px, band) & px.notna()


def base_weights(px, gross, book, band=BAND):
    """DEGROSS = committed recipe (gross/N_priced, spill to cash). INBAND = gross/N_inband."""
    priced = px.notna()
    ib = inband_mask(px, band)
    if book == "DEGROSS":
        denom = priced.sum(axis=1).replace(0, np.nan)
    else:
        denom = ib.sum(axis=1).replace(0, np.nan)
    w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    w = w.add(gross / denom, axis=0).where(ib, 0.0).fillna(0.0)
    return w


def apply_caps(w, cap_n, cap_g, gmat, target, iters=60):
    """Waterfall: cap per name and per group, re-spread to names with headroom, remainder to cash.
    w: (T,N) ndarray, gmat: (G,N) 0/1 group membership or None, target: (T,) desired gross."""
    if not np.isfinite(cap_n) and (gmat is None or not np.isfinite(cap_g)):
        return w
    w = w.copy()
    live = w > 0
    for _ in range(iters):
        if np.isfinite(cap_n):
            w = np.minimum(w, cap_n)
        if gmat is not None and np.isfinite(cap_g):
            gt = w @ gmat.T                                   # (T,G) group totals
            sc = np.where(gt > cap_g, cap_g / np.maximum(gt, 1e-15), 1.0)
            w = w * (sc @ gmat)                               # each name scaled by its group's factor
        deficit = target - w.sum(axis=1)
        if np.nanmax(np.abs(deficit)) < 1e-12:
            break
        hn = np.where(live, np.maximum(cap_n - w, 0.0) if np.isfinite(cap_n) else np.inf, 0.0)
        if gmat is not None and np.isfinite(cap_g):
            gt = w @ gmat.T
            hg = np.maximum(cap_g - gt, 0.0) @ gmat           # group headroom broadcast to its names
            h = np.minimum(hn, hg)
        else:
            h = hn
        h = np.where(np.isinf(h), 1.0, h)                     # unconstrained -> equal shares
        hs = h.sum(axis=1)
        add = np.where(hs[:, None] > 0, h * (np.maximum(deficit, 0.0) / np.where(hs == 0, 1, hs))[:, None], 0.0)
        w = w + add
    if np.isfinite(cap_n):
        w = np.minimum(w, cap_n)
    if gmat is not None and np.isfinite(cap_g):
        gt = w @ gmat.T
        sc = np.where(gt > cap_g, cap_g / np.maximum(gt, 1e-15), 1.0)
        w = w * (sc @ gmat)
    return w


def capped_book(px, gross, book, cap_n, cap_g, gmat, rows, band=BAND, w0=None):
    """Weights only on the rebalance rows `rows` (the only rows engine.backtest ever reads)."""
    if w0 is None:
        w0 = base_weights(px, gross, book, band)
    if not np.isfinite(cap_n) and (gmat is None or not np.isfinite(cap_g)):
        return w0
    sub = w0.values[rows]
    W = apply_caps(sub, cap_n, cap_g, gmat, sub.sum(axis=1))
    out = np.zeros_like(w0.values)
    out[rows] = W
    return pd.DataFrame(out, index=px.index, columns=px.columns)


# ---------------------------------------------------------------- metrics / gates
def mets(r):
    m = metrics(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"])


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def leg4b(r, spy):
    """Four 4b legs on the window r/spy span."""
    h1, h2 = halves(r); s1, s2 = halves(spy)
    m, ms = mets(r), mets(spy)
    return dict(L_H1=h1 > s1, L_H2=h2 > s2,
                L_DD=m["MaxDD"] >= 0.60 * ms["MaxDD"],         # less negative than 60% of SPY's
                L_CAGR=m["CAGR"] >= 0.70 * ms["CAGR"],
                H1=h1, H2=h2, **m)


def pass4b(d):
    return bool(d["L_H1"] and d["L_H2"] and d["L_DD"] and d["L_CAGR"])


def pass4a(r, base):
    h1, h2 = halves(r); b1, b2 = halves(base)
    return bool(h1 > b1 and h2 > b2 and mets(r)["MaxDD"] >= mets(base)["MaxDD"])


# ---------------------------------------------------------------- driver
def window(s, lo=None, hi=None):
    return s.loc[lo:hi] if (lo is not None or hi is not None) else s


def run_panel(name, px, gmat_cols):
    t0 = time.time()
    rows = np.where(rebalance_mask(px.index, FREQ).values)[0]
    start = px.index[260]
    spy_all = px["SPY"].pct_change().fillna(0.0)
    gmat = None
    if gmat_cols is not None:
        gmat = np.zeros((len(gmat_cols), px.shape[1]))
        for gi, (gname, tks) in enumerate(gmat_cols.items()):
            for tk in tks:
                if tk in px.columns:
                    gmat[gi, list(px.columns).index(tk)] = 1.0
        say(f"{name}: groups " + ", ".join(f"{g}={int(gmat[i].sum())}" for i, g in enumerate(gmat_cols)))

    # live baseline (RULES v2: band 0.03, gross 0.75, weekly)
    r_base, _, _ = fast_bt(px, rules_v2_weights(px, BAND, 0.75))
    # GATE 1: fast replay == engine.backtest, bit for bit, on the evaluated sample
    eng = backtest(px, rules_v2_weights(px, BAND, 0.75), cost_bps=COST, freq=FREQ)["returns"]
    d = float((eng.loc[start:] - r_base.loc[start:]).abs().max())
    say(f"{name}: GATE fast_bt vs engine.backtest max|d| = {d:.3e}")
    assert d < 1e-15, "replay gate failed"

    # GATE 2: the INBAND ladder's tight limit IS the committed book. Capping the re-spread
    # book at c_N = gross / N_priced reproduces baseline.rules_v2_weights exactly, so the
    # tightest rung of the cap ladder is not a new device but the recipe already shipped.
    for g in GROSSES:
        cN = g / float(px.notna().sum(axis=1).max())
        Wg = capped_book(px, g, "INBAND", cN, np.inf, None, rows)
        Wd = capped_book(px, g, "DEGROSS", np.inf, np.inf, None, rows)
        npriced = px.notna().sum(axis=1).values
        full = rows[npriced[rows] == npriced.max()]          # days on which every name is priced
        dw = float(np.abs(Wg.values[full] - Wd.values[full]).max())
        say(f"{name}: GATE INBAND@c_N={cN:.5f} == DEGROSS@G={g:.2f} on the {len(full)} of {len(rows)} "
            f"rebalance days with all {npriced.max()} names priced: max|dw| {dw:.3e}")
        assert dw < 1e-15, "cap-limit identity gate failed"

    r_base = r_base.loc[start:]
    spy = spy_all.loc[start:]
    sl = dict(FULL=(None, None), IS=(None, IS_END), OOS=("2017-01-01", None))
    ref = {k: dict(spy=leg4b(window(spy, *v), window(spy, *v)), base=window(r_base, *v)) for k, v in sl.items()}
    say(f"{name}: sample {start.date()}..{px.index[-1].date()}  SPY full "
        f"CAGR {mets(spy)['CAGR']:.2%} Sharpe {mets(spy)['Sharpe']:.4f} MaxDD {mets(spy)['MaxDD']:.2%}"
        f" | baseline RULES v2 CAGR {mets(r_base)['CAGR']:.2%} Sharpe {mets(r_base)['Sharpe']:.4f}"
        f" MaxDD {mets(r_base)['MaxDD']:.2%}")

    recs = []
    for book in ("DEGROSS", "INBAND"):
        for gross in GROSSES:
            w0 = base_weights(px, gross, book)
            r_unc, g_unc, _ = fast_bt(px, w0)
            gu = float(g_unc.loc[start:].mean())
            cgs = CAP_G if gmat is not None else [np.inf]
            for cn in CAP_N:
                for cg in cgs:
                    W = capped_book(px, gross, book, cn, cg, gmat, rows, w0=w0)
                    r, g, tn = fast_bt(px, W)
                    r, g = r.loc[start:], g.loc[start:]
                    gm = float(g.mean())
                    # binding statistics on the rebalance rows
                    sub = W.values[rows]
                    maxw = sub.max(axis=1)
                    binds_n = float((maxw > cn * (1 + 1e-9)).mean()) if np.isfinite(cn) else 0.0
                    natural = w0.values[rows]
                    bind_rows = float((natural.max(axis=1) > cn * (1 + 1e-9)).mean()) if np.isfinite(cn) else 0.0
                    if gmat is not None and np.isfinite(cg):
                        gt0 = natural @ gmat.T
                        bind_g = float((gt0 > cg * (1 + 1e-9)).any(axis=1).mean())
                    else:
                        bind_g = 0.0
                    # realised-gross-matched twin: scale the UNCAPPED book to the capped book's mean gross
                    s_hat, r_tw, g_tw = 1.0, r_unc.loc[start:], g_unc.loc[start:]
                    if abs(gm - gu) > 1e-10:
                        for _ in range(3):
                            s_hat *= gm / max(float(g_tw.mean()), 1e-12)
                            r_tw, g_tw, _ = fast_bt(px, w0 * s_hat)
                            r_tw, g_tw = r_tw.loc[start:], g_tw.loc[start:]
                    rec = dict(panel=name, book=book, gross=gross, cap_name=cn, cap_group=cg,
                               mean_gross=gm, mean_gross_unc=gu, twin_scale=s_hat,
                               twin_gross=float(g_tw.mean()), gross_resid=float(g_tw.mean()) - gm,
                               bind_name_share=bind_rows, bind_group_share=bind_g,
                               max_name_w=float(maxw.mean()), turn_yr=float(tn.loc[start:].sum() / (len(r) / 252)))
                    for k, v in sl.items():
                        rw, tw = window(r, *v), window(r_tw, *v)
                        L = leg4b(rw, window(spy, *v)); Lt = leg4b(tw, window(spy, *v))
                        rec.update({f"{k}_CAGR": L["CAGR"], f"{k}_Sharpe": L["Sharpe"], f"{k}_MaxDD": L["MaxDD"],
                                    f"{k}_H1": L["H1"], f"{k}_H2": L["H2"],
                                    f"{k}_4b": pass4b(L), f"{k}_4a": pass4a(rw, window(ref[k]["base"], None, None)),
                                    f"{k}_twin_Sharpe": Lt["Sharpe"], f"{k}_twin_CAGR": Lt["CAGR"],
                                    f"{k}_twin_MaxDD": Lt["MaxDD"], f"{k}_twin_4b": pass4b(Lt),
                                    f"{k}_dSharpe_twin": L["Sharpe"] - Lt["Sharpe"],
                                    f"{k}_dMaxDD_twin": L["MaxDD"] - Lt["MaxDD"]})
                    recs.append(rec)
    df = pd.DataFrame(recs)
    say(f"{name}: {len(df)} cells in {time.time()-t0:.1f}s")
    return df, ref, r_base, spy


def main():
    frames, refs = [], {}
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    panels = [("U56", load_universe(), U), ("B136", load_universe(broad=True), None), ("SMALL", small_panel(), None)]
    for nm, px, grp in panels:
        df, ref, rb, spy = run_panel(nm, px, grp)
        frames.append(df); refs[nm] = (ref, rb, spy)
    G = pd.concat(frames, ignore_index=True)
    G.to_csv(OUT / f"{STAMP}.grid.csv", index=False)

    say("")
    say("=" * 110)
    say("ALL GRID POINTS (FULL sample, 10 bps, weekly, t+1).  dS/dDD = capped MINUS its realised-gross-matched twin")
    say("=" * 110)
    hdr = (f"{'panel':6}{'book':9}{'G':>5} {'capN':>6} {'capG':>6} | {'bindN':>6}{'bindG':>6}{'gross':>7} |"
           f" {'CAGR':>7}{'Sharpe':>8}{'MaxDD':>8} | {'dS_twin':>8}{'dDD_twin':>9} | {'4b_F':>5}{'4b_O':>5}{'4a_F':>5}")
    say(hdr); say("-" * len(hdr))
    for _, r in G.iterrows():
        say(f"{r.panel:6}{r.book:9}{r.gross:5.2f} {r.cap_name:6.2f} {r.cap_group:6.2f} |"
            f" {r.bind_name_share:6.2f}{r.bind_group_share:6.2f}{r.mean_gross:7.3f} |"
            f" {r.FULL_CAGR:7.2%}{r.FULL_Sharpe:8.4f}{r.FULL_MaxDD:8.2%} |"
            f" {r.FULL_dSharpe_twin:+8.4f}{r.FULL_dMaxDD_twin:+9.2%} |"
            f" {str(r.FULL_4b):>5}{str(r.OOS_4b):>5}{str(r.FULL_4a):>5}")

    # ------------------------------------------------ rule 8 walk-forward
    say("")
    say("=" * 110)
    say("RULE 8 WALK-FORWARD — caps chosen on IS (<= 2016-12-31) only, OOS 2017-2026 read once")
    say("=" * 110)
    wf = []
    for (panel, book, gross), sub in G.groupby(["panel", "book", "gross"]):
        ref, rb, spy = refs[panel]
        unc = sub[(sub.cap_name == np.inf) & (sub.cap_group == np.inf)].iloc[0]
        choosers = {
            "C_SHARPE": sub.loc[sub.IS_Sharpe.idxmax()],
            "C_CALMAR": sub.loc[(sub.IS_CAGR / sub.IS_MaxDD.abs()).idxmax()],
            "C_TIGHT4b": (sub[sub.IS_4b].sort_values(["cap_name", "cap_group"]).iloc[0]
                          if sub.IS_4b.any() else None),
        }
        for cname, pick in choosers.items():
            if pick is None:
                wf.append(dict(panel=panel, book=book, gross=gross, chooser=cname, picked="none IS-4b"))
                continue
            wf.append(dict(panel=panel, book=book, gross=gross, chooser=cname,
                           picked=f"capN={pick.cap_name:.2f}/capG={pick.cap_group:.2f}",
                           is_uncapped=bool(np.isinf(pick.cap_name) and np.isinf(pick.cap_group)),
                           OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                           OOS_4b=pick.OOS_4b, OOS_4a=pick.OOS_4a,
                           unc_OOS_CAGR=unc.OOS_CAGR, unc_OOS_Sharpe=unc.OOS_Sharpe, unc_OOS_MaxDD=unc.OOS_MaxDD,
                           dSharpe_vs_uncapped=pick.OOS_Sharpe - unc.OOS_Sharpe,
                           dSharpe_vs_twin=pick.OOS_dSharpe_twin,
                           base_OOS_Sharpe=metrics(rb.loc["2017-01-01":])["Sharpe"],
                           base_OOS_CAGR=metrics(rb.loc["2017-01-01":])["CAGR"],
                           base_OOS_MaxDD=metrics(rb.loc["2017-01-01":])["MaxDD"],
                           spy_OOS_Sharpe=metrics(spy.loc["2017-01-01":])["Sharpe"],
                           spy_OOS_CAGR=metrics(spy.loc["2017-01-01":])["CAGR"],
                           spy_OOS_MaxDD=metrics(spy.loc["2017-01-01":])["MaxDD"]))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    for _, r in W.iterrows():
        if "OOS_Sharpe" not in r or pd.isna(r.get("OOS_Sharpe")):
            say(f"{r.panel:6}{r.book:9}{r.gross:5.2f} {r.chooser:10} -> {r.picked}")
            continue
        say(f"{r.panel:6}{r.book:9}{r.gross:5.2f} {r.chooser:10} -> {r.picked:26}"
            f" OOS CAGR {r.OOS_CAGR:7.2%} Sharpe {r.OOS_Sharpe:7.4f} MaxDD {r.OOS_MaxDD:7.2%}"
            f" | vs uncapped {r.dSharpe_vs_uncapped:+7.4f} vs twin {r.dSharpe_vs_twin:+7.4f}"
            f" | base {r.base_OOS_Sharpe:6.4f} SPY {r.spy_OOS_Sharpe:6.4f} | 4b {str(r.OOS_4b):5} 4a {str(r.OOS_4a):5}")

    # ------------------------------------------------ headline counts
    say("")
    say("=" * 110)
    cap = G[~(np.isinf(G.cap_name) & np.isinf(G.cap_group))]
    binding = cap[(cap.bind_name_share > 0) | (cap.bind_group_share > 0)]
    say(f"CORPUS: {len(G)} cells, {len(cap)} capped, {len(binding)} of them with a cap that ACTUALLY BINDS")
    say(f"4a FULL: {int(G.FULL_4a.sum())} of {len(G)} | 4b FULL: {int(G.FULL_4b.sum())} | 4b OOS: {int(G.OOS_4b.sum())}"
        f" | 4b FULL-and-OOS: {int((G.FULL_4b & G.OOS_4b).sum())}")
    say(f"capped cells beating their own matched-gross twin on FULL Sharpe: "
        f"{int((binding.FULL_dSharpe_twin > 0).sum())} of {len(binding)}"
        f" (mean {binding.FULL_dSharpe_twin.mean():+.4f}, median {binding.FULL_dSharpe_twin.median():+.4f})")
    say(f"   ... on OOS Sharpe: {int((binding.OOS_dSharpe_twin > 0).sum())} of {len(binding)}"
        f" (mean {binding.OOS_dSharpe_twin.mean():+.4f})")
    say(f"   ... on FULL MaxDD (shallower): {int((binding.FULL_dMaxDD_twin > 0).sum())} of {len(binding)}"
        f" (mean {binding.FULL_dMaxDD_twin.mean():+.2%})")
    b4 = binding[binding.FULL_4b & binding.OOS_4b]
    say(f"binding capped cells clearing 4b FULL-and-OOS: {len(b4)}")
    for _, r in b4.iterrows():
        say(f"   -> {r.panel} {r.book} G={r.gross} capN={r.cap_name} capG={r.cap_group} "
            f"FULL S {r.FULL_Sharpe:.4f} OOS S {r.OOS_Sharpe:.4f} dS_twin FULL {r.FULL_dSharpe_twin:+.4f} "
            f"OOS {r.OOS_dSharpe_twin:+.4f}")
    (OUT / f"{STAMP}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
