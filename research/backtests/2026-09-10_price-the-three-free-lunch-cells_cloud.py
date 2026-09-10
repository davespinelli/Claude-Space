#!/usr/bin/env python3
"""Idea 495 — price the three "free lunch" cells.

idea 270 ran a 12-cell (panel x dial) selector menu and found that in 3 cells — (B136, n),
(BSTK100, n), (S5_M120, n) — choosing the dial value by IS **CAGR** beat choosing it by IS
**Sharpe** on BOTH out-of-sample metrics at once, and all three picked a SHALLOW book (FWD5 or
FWD10).  That is the opposite of the record's "selection loses" result, and it is concentrated on
one dial.  Three cells out of twelve is also exactly what a coin flip on 12 cells would give.

THE QUESTION: is the free lunch a stable property of shallow n, or three draws out of twelve?

DESIGN — the queue's literal ask, "re-run those three cells over 40 seeded resamples of their own
panels".  For each of the three parent panels, 40 sub-panels are drawn WITHOUT replacement from
that panel's own tradable set at a fixed 75% coverage (no coverage tuning), seeds 2000..2039.
On each sub-panel the whole n-dial menu is rebuilt and both selectors are re-run:

    menu       EWall, FWD5, FWD10, FWD20, FWD30, FWD40, FWD60   (idea 270's lane-B n dial,
               reproduced verbatim: eligible = above 200d MA and vol20 < 0.60, rank on the
               NON-vol-scaled composite, equal weight, gross 0.75, weekly, t+1, 10 bps)
    S_SHARPE   argmax IS Sharpe on 2009-01-01..2016-12-31
    S_CAGR     argmax IS CAGR   on the same window
    DONOTHING  EWall, the menu's no-choice arm
    FREE LUNCH  S_CAGR beats S_SHARPE on OOS Sharpe AND on OOS CAGR, 2017-01-01..2026 read once.

THE ONLY TWO TUNED PARAMETERS (PROTOCOL rule 4):
    seeds   40 per panel (the queue's number)
    nfloor  the shallowest book the menu is allowed to contain, in {5, 10, 20} — this is the
            dial the hypothesis is about, since idea 270's three picks were FWD5/FWD10.
ALL 3 panels x 40 seeds x 3 nfloors = 360 selector cells are reported, plus the 3 parent cells.

RULE 8 (PROTOCOL 8) is intrinsic: every selector chooses on 2009-2016 ONLY and 2017-2026 is read
once.  Both KEEP paths are additionally evaluated on every selected book against the live RULES v2
baseline and against SPY, full sample and both halves.

Deterministic (fixed seeds); no network; never calls yfinance.
SURVIVORSHIP: B136/BSTK100 are current constituents of a current screen and SMALL439 (the parent
of S5_M120) is a current sub-$2B screen, so every LEVEL is biased up.  The free-lunch RATE is a
within-panel comparison of two selectors on the same books and is not.
"""
from __future__ import annotations
import json, sys, time, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))
from baseline import load_universe, score, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask         # noqa: E402

STEM = Path(__file__).name[:-3]
OUT = REPO / "research" / "backtests"
GROSS, MAX_VOL = 0.75, 0.60
COST, FREQ = 10.0, "W"
IS_START, IS_END, OOS_START = "2009-01-01", "2016-12-31", "2017-01-01"
NS = (5, 10, 20, 30, 40, 60)          # idea 270's lane-B n menu
NFLOORS = (5, 10, 20)                 # tuned param 2
N_SEEDS = 40                          # tuned param 1 (the queue's number)
COVERAGE = 0.75                       # fixed by pre-registration, not swept
SEED0 = 2000

_log: list[str] = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); _log.append(s)


# ------------------------------------------------------------------ engine clone (idea 317)
def fast_bt(px, W, cost_bps=COST, freq=FREQ):
    idx = px.index
    rets = px.pct_change().fillna(0.0).to_numpy(float)
    wt = W.reindex(idx).fillna(0.0).shift(1).fillna(0.0).to_numpy(float)
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).to_numpy(bool).copy()
    mask[0] = True
    T, N = rets.shape
    Cs = np.empty((T, N)); Cs[0] = 1.0
    np.cumprod(1.0 + rets[:-1], axis=0, out=Cs[1:])
    starts = np.flatnonzero(mask)
    seg = np.searchsorted(starts, np.arange(T), side="right") - 1
    s_of_t = starts[seg]
    new = wt[s_of_t]
    num = new * (Cs / Cs[s_of_t])
    D = num.sum(axis=1) + (1.0 - new.sum(axis=1))
    held = num / D[:, None]
    turn = np.zeros(T); turn[0] = np.abs(wt[0]).sum()
    later = starts[1:]
    if len(later):
        sp = starts[seg[later] - 1]
        prev_new = wt[sp]
        np_ = prev_new * (Cs[later] / Cs[sp])
        Dp = np_.sum(axis=1) + (1.0 - prev_new.sum(axis=1))
        turn[later] = np.abs(wt[later] - np_ / Dp[:, None]).sum(axis=1)
    return pd.Series((held * rets).sum(axis=1) - turn * cost_bps / 1e4, index=idx)


def mrow(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def binom_p_two_sided(k, n, p=0.5):
    """Exact two-sided binomial p, no scipy."""
    from math import comb
    pmf = [comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(n + 1)]
    return float(sum(v for i, v in enumerate(pmf) if v <= pmf[k] * (1 + 1e-12)))


# ------------------------------------------------------------------ panels (idea 270 verbatim)
def build_parents():
    U = json.loads((REPO / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    etf36 = [t for t in U["broad"] + U["sectors"] + U["bonds_fx_commod"] if t not in crypto]
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])          # ALWAYS dropped first
    b_stk = [t for t in px136.columns if t not in set(etf36) and t != "SPY"]
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    P(f"  SMALL panel: dropped {len([c for c in pxs.columns if c != 'SPY']) - len(s_stk)} names "
      f"with max_1d_move >= 1.0 -> {len(s_stk)} tradable.")

    def sub(px, cols, tradable=None):
        cols = [c for c in cols if c in px.columns]
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
        return px[keep].dropna(how="all").ffill(), set(tradable if tradable is not None else cols)

    rng5 = np.random.default_rng(1000 + 5)                          # idea 270's seed-5 draw
    s5 = sorted(rng5.choice(np.array(sorted(s_stk)), size=120, replace=False).tolist())
    return {"B136": sub(px136, list(px136.columns)),
            "BSTK100": sub(px136, b_stk, tradable=b_stk),
            "S5_M120": sub(pxs, s5, tradable=s5)}, px136, pxs


# ------------------------------------------------------------------ the n-dial menu
def eligible(px, tradable):
    _, above, vol20 = score(px)
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop: m[drop] = False
    return m


def menu_weights(px, tradable):
    """EWall + FWD{n}: idea 270's lane-B n dial, reproduced verbatim."""
    elig = eligible(px, tradable)
    key = score(px, vol_scale=False)[0]
    rank = key.where(elig).rank(axis=1, ascending=False)
    out = {}
    sel = elig.astype(float)
    out["EWall"] = sel.div(sel.sum(axis=1).replace(0, np.nan), axis=0).mul(GROSS).fillna(0.0)
    for n in NS:
        s = (rank <= n).astype(float)
        out[f"FWD{n}"] = s.div(s.sum(axis=1).replace(0, np.nan), axis=0).mul(GROSS).fillna(0.0)
    return out


def price_menu(px, tradable):
    """Every arm of the menu, with IS/OOS/full metrics.  Returns a DataFrame indexed by arm."""
    start = px.index[260]
    rows = {}
    for arm, W in menu_weights(px, tradable).items():
        r = fast_bt(px, W).loc[start:]
        m, mi, mo = mrow(r), mrow(r.loc[IS_START:IS_END]), mrow(r.loc[OOS_START:])
        rows[arm] = dict(IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"],
                         OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                         CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                         H1=m["H1"], H2=m["H2"])
    return pd.DataFrame(rows).T


def bench(px):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    b2 = fast_bt(px, rules_v2_weights(px)).loc[start:]
    return (mrow(spy), mrow(spy.loc[OOS_START:]), mrow(b2), mrow(b2.loc[OOS_START:]))


def keep_paths(m, mo, S, So, B):
    p4a = bool(m["H1"] > B["H1"] and m["H2"] > B["H2"] and m["MaxDD"] >= B["MaxDD"])
    legs = dict(H1=m["H1"] > S["H1"], H2=m["H2"] > S["H2"], OOS=mo["Sharpe"] > So["Sharpe"],
                DD=m["MaxDD"] >= 0.60 * S["MaxDD"], CAGR=m["CAGR"] >= 0.70 * S["CAGR"])
    return p4a, bool(all(legs.values())), ";".join(k for k, v in legs.items() if not v)


def selectors(tab, nfloor, S, So, B):
    """Both selectors on a menu restricted to n >= nfloor, plus the do-nothing arm."""
    arms = ["EWall"] + [f"FWD{n}" for n in NS if n >= nfloor]
    t = tab.loc[arms]
    ss, sc, dn = t.IS_Sharpe.idxmax(), t.IS_CAGR.idxmax(), "EWall"
    out = dict(n_arms=len(arms), pick_SHARPE=ss, pick_CAGR=sc, disagree=bool(ss != sc),
               S_OOS_Sharpe=t.at[ss, "OOS_Sharpe"], S_OOS_CAGR=t.at[ss, "OOS_CAGR"],
               C_OOS_Sharpe=t.at[sc, "OOS_Sharpe"], C_OOS_CAGR=t.at[sc, "OOS_CAGR"],
               DN_OOS_Sharpe=t.at[dn, "OOS_Sharpe"], DN_OOS_CAGR=t.at[dn, "OOS_CAGR"],
               dOOS_Sharpe=t.at[sc, "OOS_Sharpe"] - t.at[ss, "OOS_Sharpe"],
               dOOS_CAGR_pp=(t.at[sc, "OOS_CAGR"] - t.at[ss, "OOS_CAGR"]) * 100.0)
    out["freelunch"] = bool(out["dOOS_Sharpe"] > 0 and out["dOOS_CAGR_pp"] > 0)
    out["freelunch_reverse"] = bool(out["dOOS_Sharpe"] < 0 and out["dOOS_CAGR_pp"] < 0)
    for tag, arm in (("S", ss), ("C", sc)):
        r = t.loc[arm]
        a, b, fl = keep_paths(dict(r), dict(Sharpe=r.OOS_Sharpe), S, So, B)
        out[f"{tag}_pass4a"], out[f"{tag}_pass4b"], out[f"{tag}_fail4b"] = a, b, fl
    return out


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    P(f"=== {STEM} ===")
    P(__doc__.strip())

    P("\nPANELS")
    parents, px136, pxs = build_parents()
    for nm, (px, tr) in parents.items():
        P(f"  {nm:8s} {len(px.columns):4d} cols, {len(tr):4d} tradable, "
          f"{px.index[0].date()}..{px.index[-1].date()} ({len(px)} rows)")

    P("\nGATES (pre-registered, printed before any hypothesis number)")
    ok = True
    pxB, trB = parents["B136"]
    W = menu_weights(pxB, trB)["FWD20"]
    ref = backtest(pxB, W, cost_bps=COST, freq=FREQ)["returns"]
    r = fast_bt(pxB, W)
    nanrows = ref.index[ref.isna()]
    late = [t for t in nanrows if t >= pxB.index[260]]
    d = float(np.nanmax(np.abs(ref.to_numpy() - r.to_numpy())))
    P(f"  G1 fast_bt vs engine.backtest on B136/FWD20 = {d:.3e} over {len(ref)-len(nanrows)} "
      f"finite rows ({len(nanrows)} engine-NaN warm-up rows, {len(late)} inside the scored "
      f"window)   {'PASS' if d < 1e-12 and not late else 'FAIL'}")
    ok &= d < 1e-12 and not late
    # G2: a resample must be a strict subset of its parent's tradable set, at the stated coverage
    rng = np.random.default_rng(SEED0)
    pool = np.array(sorted(trB))
    k = int(round(COVERAGE * len(pool)))
    pick = set(rng.choice(pool, size=k, replace=False).tolist())
    g2 = pick <= trB and len(pick) == k
    P(f"  G2 resample is a strict subset at the stated coverage: {len(pick)}/{len(trB)} = "
      f"{len(pick)/len(trB):.3f}   {'PASS' if g2 else 'FAIL'}")
    ok &= g2
    # G3: the n menu must be nested — FWD5's holdings are a subset of FWD10's, every day
    M = menu_weights(pxB, trB)
    g3 = float(((M["FWD5"] > 0) & ~(M["FWD10"] > 0)).to_numpy().sum())
    P(f"  G3 the n menu is nested (FWD5 holdings inside FWD10): {int(g3)} violations   "
      f"{'PASS' if g3 == 0 else 'FAIL'}")
    ok &= g3 == 0
    P(f"  GATES: {'ALL PASS' if ok else 'SOME FAILED — read the numbers with that caveat'}")

    # ---------------------------------------------------------------- parents
    P("\n" + "=" * 100)
    P("PART A — THE THREE PARENT CELLS as idea 270 ran them (nfloor = 5), every arm reported")
    arm_rows, cell_rows = [], []
    benches = {}
    for nm, (px, tr) in parents.items():
        S, So, B, Bo = bench(px); benches[nm] = (S, So, B, Bo)
        tab = price_menu(px, tr)
        P(f"\n  {nm}   SPY {S['CAGR']:6.2%}/{S['Sharpe']:.3f}/{S['MaxDD']:7.2%} "
          f"(halves {S['H1']:.3f}/{S['H2']:.3f}, OOS Sharpe {So['Sharpe']:.3f})   "
          f"RULES v2 {B['CAGR']:6.2%}/{B['Sharpe']:.3f}/{B['MaxDD']:7.2%} (OOS {Bo['Sharpe']:.3f})")
        P(f"    arm      IS_Shrp  IS_CAGR | OOS_Shrp OOS_CAGR OOS_MaxDD | full CAGR Sharpe  MaxDD  H1/H2")
        for arm, r in tab.iterrows():
            P(f"    {arm:8s} {r.IS_Sharpe:7.3f} {r.IS_CAGR:8.2%} | {r.OOS_Sharpe:8.3f} "
              f"{r.OOS_CAGR:8.2%} {r.OOS_MaxDD:9.2%} | {r.CAGR:9.2%} {r.Sharpe:6.3f} "
              f"{r.MaxDD:7.2%} {r.H1:.3f}/{r.H2:.3f}")
            arm_rows.append(dict(panel=nm, kind="parent", seed=-1, arm=arm, **r.to_dict()))
        for nf in NFLOORS:
            s = selectors(tab, nf, S, So, B)
            cell_rows.append(dict(panel=nm, kind="parent", seed=-1, nfloor=nf, **s))
            P(f"    nfloor {nf:2d}: S_SHARPE -> {s['pick_SHARPE']:6s}  S_CAGR -> {s['pick_CAGR']:6s}"
              f"  dOOS_Sharpe {s['dOOS_Sharpe']:+.4f}  dOOS_CAGR {s['dOOS_CAGR_pp']:+.2f} pp"
              f"  {'FREE LUNCH' if s['freelunch'] else ('reverse' if s['freelunch_reverse'] else 'mixed/tie')}")

    # ---------------------------------------------------------------- resamples
    P("\n" + "=" * 100)
    P(f"PART B — {N_SEEDS} SEEDED RESAMPLES PER PANEL at {COVERAGE:.0%} coverage "
      f"(seeds {SEED0}..{SEED0+N_SEEDS-1}), the whole menu rebuilt on each")
    for nm, (px, tr) in parents.items():
        S, So, B, Bo = benches[nm]
        pool = np.array(sorted(tr)); k = int(round(COVERAGE * len(pool)))
        t1 = time.time()
        for s_i in range(N_SEEDS):
            rng = np.random.default_rng(SEED0 + s_i)
            pick = sorted(rng.choice(pool, size=k, replace=False).tolist())
            keep = list(dict.fromkeys(pick + (["SPY"] if "SPY" in px.columns else [])))
            sp = px[keep].dropna(how="all").ffill()
            tab = price_menu(sp, set(pick))
            for arm, r in tab.iterrows():
                arm_rows.append(dict(panel=nm, kind="resample", seed=SEED0 + s_i, arm=arm,
                                     **r.to_dict()))
            for nf in NFLOORS:
                cell_rows.append(dict(panel=nm, kind="resample", seed=SEED0 + s_i, nfloor=nf,
                                      **selectors(tab, nf, S, So, B)))
        P(f"  {nm:8s} {k}/{len(pool)} names x {N_SEEDS} seeds  [{time.time()-t1:.1f}s]")

    arms = pd.DataFrame(arm_rows); cells = pd.DataFrame(cell_rows)
    arms.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    cells.to_csv(OUT / f"{STEM}.cells.csv", index=False)

    # ---------------------------------------------------------------- THE ANSWER
    P("\n" + "=" * 100)
    P("PART C — IS THE FREE LUNCH STABLE?  (all 360 resample cells, nothing dropped)")
    rs = cells[cells.kind == "resample"]
    P(f"\n  {'panel':9s} {'nfloor':>6s} {'disagree':>9s} {'FREE LUNCH':>11s} {'reverse':>8s} "
      f"{'p(FL=.5|disagree)':>18s}  mean dOOS_Sharpe  mean dOOS_CAGR_pp")
    for nm in parents:
        for nf in NFLOORS:
            g = rs[(rs.panel == nm) & (rs.nfloor == nf)]
            dis = g[g.disagree]
            fl, rev = int(g.freelunch.sum()), int(g.freelunch_reverse.sum())
            p = binom_p_two_sided(fl, len(dis)) if len(dis) else float("nan")
            P(f"  {nm:9s} {nf:6d} {len(dis):4d}/{len(g):<4d} {fl:6d}/{len(g):<4d} {rev:8d} "
              f"{p:18.4f}  {g.dOOS_Sharpe.mean():+16.4f}  {g.dOOS_CAGR_pp.mean():+17.2f}")
    P(f"\n  POOLED over the 3 panels:")
    for nf in NFLOORS:
        g = rs[rs.nfloor == nf]; dis = g[g.disagree]
        fl, rev = int(g.freelunch.sum()), int(g.freelunch_reverse.sum())
        P(f"    nfloor {nf:2d}: disagree {len(dis)}/{len(g)} ({len(dis)/len(g):.1%}), "
          f"FREE LUNCH {fl}/{len(g)} ({fl/len(g):.1%}), reverse {rev}/{len(g)} ({rev/len(g):.1%}), "
          f"p(FL | disagree, coin) {binom_p_two_sided(fl, len(dis)) if len(dis) else float('nan'):.4f}, "
          f"mean dOOS_Sharpe {g.dOOS_Sharpe.mean():+.4f}, mean dOOS_CAGR {g.dOOS_CAGR_pp.mean():+.2f} pp")

    P("\n  WHICH ARM EACH SELECTOR PICKS (resamples, nfloor = 5) — is the pick SHALLOW?")
    g5 = rs[rs.nfloor == 5]
    for nm in parents:
        gg = g5[g5.panel == nm]
        for lab, col in (("S_SHARPE", "pick_SHARPE"), ("S_CAGR", "pick_CAGR")):
            vc = gg[col].value_counts()
            P(f"    {nm:9s} {lab:9s} " + "  ".join(f"{a}:{c}" for a, c in vc.items()))
        sh = gg[gg.pick_CAGR.isin(["FWD5", "FWD10"])]
        P(f"    {nm:9s} S_CAGR picks FWD5/FWD10 in {len(sh)}/{len(gg)} seeds; "
          f"free lunch among those {int(sh.freelunch.sum())}/{len(sh)}, "
          f"among the rest {int(gg[~gg.index.isin(sh.index)].freelunch.sum())}/{len(gg)-len(sh)}")

    P("\n  DOES EITHER SELECTOR BEAT DO-NOTHING (EWall) OOS?  (resamples, nfloor = 5)")
    for nm in parents:
        gg = g5[g5.panel == nm]
        P(f"    {nm:9s} S_SHARPE > EWall on OOS Sharpe {int((gg.S_OOS_Sharpe>gg.DN_OOS_Sharpe).sum())}"
          f"/{len(gg)}; S_CAGR > EWall {int((gg.C_OOS_Sharpe>gg.DN_OOS_Sharpe).sum())}/{len(gg)}"
          f"  |  mean OOS Sharpe  S_SHARPE {gg.S_OOS_Sharpe.mean():.4f}  "
          f"S_CAGR {gg.C_OOS_Sharpe.mean():.4f}  EWall {gg.DN_OOS_Sharpe.mean():.4f}")

    P("\n  BOTH KEEP PATHS on every selected book (resamples + parents, all nfloors)")
    for tag, lab in (("S", "S_SHARPE"), ("C", "S_CAGR")):
        P(f"    {lab:9s} 4a {int(cells[f'{tag}_pass4a'].sum())}/{len(cells)}   "
          f"4b {int(cells[f'{tag}_pass4b'].sum())}/{len(cells)}")
    fails = pd.concat([cells.S_fail4b, cells.C_fail4b]).replace("", np.nan).dropna()
    P(f"    4b fail-bar census (both selectors, {len(fails)} failing books): "
      + ", ".join(f"{k} {v}" for k, v in fails.value_counts().head(6).items()))

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_log) + "\n")
    P(f"\nwrote {STEM}.arms.csv ({len(arms)}), .cells.csv ({len(cells)}), .console.txt "
      f"[total {time.time()-t0:.1f}s]")


if __name__ == "__main__":
    main()
