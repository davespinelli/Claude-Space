#!/usr/bin/env python3
"""IDEA 694 (cloud, 2026-09-11): is-the-WIDTH-to-OOS-slope-a-SELECTION-POOL-effect-or-a-SMALL-CAP-effect.

THE QUESTION (queue, verbatim)
------------------------------
"idea 688 measured rho(k, OOS Sharpe) +0.5269 with mean OOS Sharpe monotone 0.2516 -> 0.4849
across 40..400 at q=1.00, and idea 685 measured the wide end LOSING on a mixed-q ladder; the
two differ in cap mix as well as in pool depth.  Separate them by holding n/k (the selection
ratio) fixed while varying k, and report whether the slope survives.  Max 2 params (n/k, k)."

WHAT IS ACTUALLY CONFOUNDED.  Both published ladders hold the BOOK SIZE n fixed (the record's
NS_LAD = {5,10,15,20,30}) and vary the panel width k.  A fixed-n book on a widening panel is
NOT the same book: three things move together with k.

    (1) POOL DEPTH   more names to choose from                      <- the claimed channel
    (2) SELECTIVITY  n/k falls 10x across k=40..400 at fixed n      <- never held fixed
    (3) FILL/GROSS   CAND-n weights every pick at GROSS/n, so when the eligible count
                     n_elig_t = breadth*k is BELOW n the book holds n_elig_t names at
                     GROSS/n and is DE-GROSSED by n_elig/n.  At q=1.00 breadth ~ 0.3, so
                     CAND-30 on k=40 runs at ~0.4x its nominal gross and CAND-30 on k=400
                     runs at 1.0x.  Width BUYS EXPOSURE at fixed n.
and across the two published ladders (4) CAP MIX q moves as well.

This run separates all four.  Holding n/k fixed makes (2) constant by construction and, since
the de-gross factor is min(breadth*k, r*k)/(r*k) = min(breadth/r, 1), makes (3) k-invariant
too - so the fixed-ratio arm isolates (1) POOL DEPTH, and the q supports isolate (4).

THE TWO TUNED PARAMETERS (PROTOCOL rule 4, max 2)
    PARAM 1  selection ratio  r = n/k in {0.05, 0.10, 0.25, 0.50}        (4 rungs)
    PARAM 2  panel width      k in {40, 60, 80, 100, 200, 400}           (6 rungs)
    n = max(2, round(r*k)).  ALL 24 cells are reported at every q support.
REPORTED, NOT TUNED (no verdict is taken by choosing among these):
    - cap mix q in {0.00 (pure BSTK100 large caps, k<=100), 0.50, 1.00 (pure SMALL439)} -
      the axis the queue names as the rival explanation; every level reported.
    - the record's own FIXED-n ladder NS_LAD = {5,10,15,20,30} + EWall, re-run on the same
      panels.  It is the REPRODUCTION arm (gate G4) and the thing being decomposed.
    - 8 draws per cell (idea 688's convention), seeded.
Everything else is inherited from the record, not chosen here: RULES v1 eligibility (above
200d, vol20 < 0.60), the v1 composite with the vol scaler OFF, GROSS = 0.75, weekly cadence,
10 bps, next-day execution, the 260-day warm-up skip, IS = ..2016-12-31, OOS = 2017-01-01.. .

GATES (pre-registered; printed before any new number is read)
    G1  fast_bt vs engine.backtest on a k=400 panel book: returns AND turnover.
    G2  the cached-rank CAND weights vs idea 286's committed `cand_weights(n)` - exact.
    G3  ENVELOPE: every panel has exact width, exact cap mix, no duplicate columns, inside
        its pools; the q=1.00 half is idea 688's committed panel set, replayed.
    G4  REPRODUCTION: the fixed-n arm on the q=1.00 panels vs idea 688's COMMITTED
        .books.csv (288 rows x 9 statistics), and its published headline
        rho(k, OOS Sharpe) = +0.5269 with means 0.2516 -> 0.4849, recomputed here.

RULE 8 (PROTOCOL 8, required).  The dial (r, k) - and, on the reproduction arm, (n, k) - is
chosen on 2009-2016 IS Sharpe ONLY, inside one draw's own choice set, and the pick is read
once on 2017-01-01.. .  Six selectors including K-MAX (idea 688's width-pinner) and a seeded
RANDOM control.  Reported against the do-nothing anchor (mean OOS of the choice set), RULES
v2 on the picked panel, and SPY.  Run separately on the FIXED-n and FIXED-RATIO grids, which
is the queue's question asked at the selector level: does width-pinning still pay once the
selection ratio cannot move?

KEEP PATHS (PROTOCOL rule 4).  4a vs RULES v2 on the same panel and 4b vs SPY are evaluated
on EVERY book row by idea 286's committed `keep_paths`, and reported by arm, k and q.

SURVIVORSHIP.  SMALL439 and BSTK100 are CURRENT constituents of their screens (see
data/SMALL_PANEL_README.md): every CAGR level here is optimistic, and the q axis is exactly
the axis survivorship contaminates most, since the small screen is the one rebuilt from
today's names.  Nothing in this run is a capital candidate - the books are the record's
existing CAND-n/EWall books re-run on re-drawn panels, so a 4a/4b pass is a statement about
the panel, not about a rule.

Outputs: .books.csv .panels.csv .slopes.csv .walkforward.csv .console.txt .result.md
"""
import importlib.util, sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import score, rules_v2_weights            # noqa
from engine import backtest, rebalance_mask, metrics    # noqa

OUT = Path(__file__).with_suffix("")
BT = ROOT / "research" / "backtests"
LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)

COST, FREQ, GROSS = 10, "W", 0.75
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARM = 260

RATIOS  = [0.05, 0.10, 0.25, 0.50]        # PARAM 1
KS      = [40, 60, 80, 100, 200, 400]     # PARAM 2
NS_LAD  = [5, 10, 15, 20, 30]             # the record's committed fixed-n ladder (reported)
QS      = [0.00, 0.50, 1.00]              # cap-mix support (reported, never chosen on)
N_DRAWS = 8
SEED_NEW = 694
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 400)


def _load(p, name):
    spec = importlib.util.spec_from_file_location(name, str(p))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

M276 = _load(BT / "2026-09-06_is-breadth-a-small-cap-dummy-everywhere-in-the-record_cloud.py", "idea276")
M286 = _load(BT / "2026-09-09_price-the-14-breadth-files-on-their-own-books_B.py", "idea286")
M688 = _load(BT / "2026-09-11_is-WIDTH-MAXIMISATION-a-general-rule-8-selector-pathology_C.py", "idea688")
B688 = BT / "2026-09-11_is-WIDTH-MAXIMISATION-a-general-rule-8-selector-pathology_C.books.csv"

cand_weights, ewall_weights = M286.cand_weights, M286.ewall_weights
full_row, keep_paths, spearman = M286.full_row, M286.keep_paths, M286.spearman
partial_spearman = M286.partial_spearman


# ---------------------------------------------------------------- fast engine
def fast_bt(prices, weights, cost_bps=COST, freq=FREQ):
    """numpy re-implementation of engine.backtest; same algorithm, same NaN semantics (G1)."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    w_t = weights.reindex(idx).fillna(0.0).shift(1).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values
    n = len(idx)
    held = np.empty_like(rets); turn = np.zeros(n); cur = np.zeros(rets.shape[1])
    for i in range(n):
        if mask[i] or i == 0:
            new = w_t[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    port = np.nansum(held * rets, axis=1) - turn * cost_bps / 1e4
    return pd.Series(port, index=idx), pd.Series(turn, index=idx)


def panel_cache(px, cols):
    """Everything a CAND-n book on this panel needs, computed once (G2 asserts equality)."""
    s, above, vol20 = score(px[cols], vol_scale=False)
    gate = above & (vol20 < 0.60)
    rank = s.where(gate).rank(axis=1, ascending=False)
    return dict(rank=rank, gate=gate, cols=cols)


def cand_w_fast(px, cache, n):
    w = (cache["rank"] <= n).astype(float) * (GROSS / n)
    return w.reindex(columns=px.columns).fillna(0.0)


def gross_stats(px, w, st):
    """Nominal target gross on rebalance days from st, and the fill rate vs GROSS."""
    mask = rebalance_mask(px.index, FREQ)
    g = w.loc[mask.values].loc[st:].sum(axis=1)
    return float(g.mean()), float(g.mean() / GROSS)


# ---------------------------------------------------------------- panels
def build_panels(s_stk, b_stk, built_688):
    """[(q, k, draw, cols, prov)].  q=1.00 replays idea 688's committed panel set exactly."""
    out, seen = [], set()
    for k, d, cols in built_688:
        out.append((1.00, k, d, list(cols), "idea688"))
        seen.add((tuple(sorted(cols)), ()))
    rng = np.random.default_rng(SEED_NEW)
    for q in [q for q in QS if q < 1.0]:
        for k in KS:
            ns_, nl_ = int(round(q * k)), k - int(round(q * k))
            if ns_ > len(s_stk) or nl_ > len(b_stk):
                continue                                   # outside the feasible envelope
            for d in range(N_DRAWS):
                sc = sorted(rng.choice(s_stk, size=ns_, replace=False)) if ns_ else []
                lc = sorted(rng.choice(b_stk, size=nl_, replace=False)) if nl_ else []
                key = (tuple(sc), tuple(lc))
                if key in seen:
                    P(f"  dedupe: q={q:.2f} k={k} d{d} exact repeat - skipped"); continue
                seen.add(key)
                out.append((q, k, d, list(sc) + list(lc), "new"))
    out.sort(key=lambda t: (t[0], t[1], t[2]))
    return out


# ---------------------------------------------------------------- selectors (rule 8)
def rule8(books, grid, dialcol, label):
    """Pick inside one (q, draw) choice set on IS Sharpe only; read OOS once."""
    SEL = {"IS-SHARPE-MAX": ("IS_Sharpe", True), "K-MAX": ("k", True), "K-MIN": ("k", False),
           f"{dialcol.upper()}-MAX": (dialcol, True), f"{dialcol.upper()}-MIN": (dialcol, False)}
    rng = np.random.default_rng(SEED_NEW + 7)
    rows = []
    b = books[books.grid == grid]
    for (q, d), sub in b.groupby(["q", "draw"]):
        if len(sub) < 2: continue
        anchor = float(sub.OOS_Sharpe.mean())
        picks = {}
        for sel, (col, hi) in SEL.items():
            s2 = sub.sort_values(["IS_Sharpe"], ascending=False)      # ties -> better IS Sharpe
            picks[sel] = s2.loc[s2[col].idxmax() if hi else s2[col].idxmin()]
        picks["RANDOM"] = sub.iloc[int(rng.integers(len(sub)))]
        for sel, pk in picks.items():
            rows.append(dict(grid=grid, dial=label, q=q, draw=int(d), selector=sel,
                             k=pk.k, n=pk.n, ratio=pk.ratio, arm=pk.arm,
                             IS_Sharpe=pk.IS_Sharpe, OOS_CAGR=pk.OOS_CAGR,
                             OOS_Sharpe=pk.OOS_Sharpe, OOS_MaxDD=pk.OOS_MaxDD,
                             anchor_OOS_S=anchor, v2_OOS_S=pk.v2_OOS_S, v2_OOS_CAGR=pk.v2_OOS_CAGR,
                             v2_OOS_DD=pk.v2_OOS_DD, spy_OOS_S=pk.spy_OOS_S,
                             spy_OOS_CAGR=pk.spy_OOS_CAGR, spy_OOS_DD=pk.spy_OOS_DD,
                             beats_anchor=bool(pk.OOS_Sharpe > anchor),
                             beats_v2=bool(pk.OOS_Sharpe > pk.v2_OOS_S),
                             beats_spy=bool(pk.OOS_Sharpe > pk.spy_OOS_S),
                             pass4a=bool(pk.pass4a), pass4b=bool(pk.pass4b)))
    return pd.DataFrame(rows)


def main():
    t0all = time.time()
    P("=" * 104)
    P("IDEA 694 - is-the-WIDTH-to-OOS-slope-a-SELECTION-POOL-effect-or-a-SMALL-CAP-effect (cloud, 2026-09-11)")
    P("=" * 104)
    P("TUNED (2): ratio r=n/k in " + str(RATIOS) + "  x  k in " + str(KS))
    P("REPORTED, NOT TUNED: q in " + str(QS) + " (cap mix), the record's fixed-n ladder "
      + str(NS_LAD) + " + EWall, 8 seeded draws.")
    P("Costs 10 bps, weekly, next-day execution, GROSS 0.75, IS ..2016 / OOS 2017.. .")

    src = M276.build_sources()
    pxs, pxb = src["pxs"], src["pxb"]
    idx = pxs.index.intersection(pxb.index)
    pxs_c, pxb_c = pxs.reindex(idx).ffill(), pxb.reindex(idx).ffill()
    spy = pxb_c["SPY"]
    s_stk, b_stk = src["s_stk"], src["b_stk"]
    P(f"common calendar {idx[0].date()} .. {idx[-1].date()} ({len(idx)} days); "
      f"pools SMALL {len(s_stk)}, BSTK {len(b_stk)}")

    built_688, prov688 = M688.build_ladder(s_stk, b_stk)
    panels = build_panels(s_stk, b_stk, built_688)
    P(f"\n{len(panels)} panels: " + ", ".join(
        f"q={q:.2f} {sum(1 for t in panels if t[0] == q)}" for q in QS))

    # ---------------------------------------------------------------- G3
    P("\n--- GATE 3: envelope ---")
    bad = []
    for q, k, d, cols, prov in panels:
        ns_ = int(round(q * k))
        if len(cols) != k: bad.append((q, k, d, "width"))
        if len(set(cols)) != len(cols): bad.append((q, k, d, "dup"))
        if sum(c in s_stk for c in cols) != ns_: bad.append((q, k, d, "cap mix"))
        if any(c not in s_stk and c not in b_stk for c in cols): bad.append((q, k, d, "pool"))
    assert not bad, f"GATE 3 FAILED: {bad[:5]}"
    P(f"  GATE 3 PASS - {len(panels)} panels: exact width, exact cap mix, no duplicate columns, "
      f"inside pools.  q=1.00 half = idea 688's committed set ({len(built_688)} panels), replayed.")

    # ---------------------------------------------------------------- G1 / G2
    P("\n--- GATES 1 and 2: the fast paths, on a k=400 panel ---")
    q0, k0, d0, cols0, _ = [t for t in panels if t[1] == 400][0]
    px0 = pd.concat([pxs_c[cols0], spy.rename("SPY")], axis=1).dropna(how="all").ffill()[cols0 + ["SPY"]]
    c0 = panel_cache(px0, cols0)
    w_ref = cand_weights(20)(px0)
    w_fast = cand_w_fast(px0, c0, 20)
    dw = float(np.abs(w_ref.values - w_fast.values).max())
    assert dw == 0.0, f"GATE 2 FAILED: {dw}"
    P(f"  GATE 2 PASS - cached-rank CAND-20 vs idea 286's cand_weights(20): max |dw| {dw:.3e}")
    eng = backtest(px0, w_ref, cost_bps=COST, freq=FREQ)
    r_f, t_f = fast_bt(px0, w_ref)
    dr = float(np.abs(eng["returns"] - r_f).max()); dt = float(np.abs(eng["turnover"] - t_f).max())
    assert dr < 1e-12 and dt < 1e-12, f"GATE 1 FAILED: {dr}, {dt}"
    P(f"  GATE 1 PASS - fast_bt vs engine.backtest: returns {dr:.3e}, turnover {dt:.3e}")

    # ---------------------------------------------------------------- run the ladder
    P("\n" + "=" * 104); P("RUNNING THE LADDER"); P("=" * 104)
    brows, prows = [], []
    for i, (q, k, d, cols, prov) in enumerate(panels):
        t0 = time.time()
        parts = []                                          # panels may draw from both frames
        sc = [c for c in cols if c in s_stk]; lc = [c for c in cols if c in b_stk]
        if sc: parts.append(pxs_c[sc])
        if lc: parts.append(pxb_c[lc])
        px = pd.concat(parts + [spy.rename("SPY")], axis=1).dropna(how="all").ffill()[cols + ["SPY"]]
        st = px.index[WARM]
        cache = panel_cache(px, cols)
        n_elig = cache["gate"].sum(axis=1)
        mask = rebalance_mask(px.index, FREQ)
        Ebar = float(n_elig.loc[mask.values].loc[st:].mean())
        tag = f"q={q:.2f} k={k} d{d}"

        spy_r = full_row("SPY", px["SPY"].pct_change().fillna(0).loc[st:])
        wv2 = (rules_v2_weights(px).drop(columns=["SPY"], errors="ignore")
               .reindex(columns=px.columns).fillna(0.0))
        v2_r = full_row("v2", fast_bt(px, wv2)[0].loc[st:])

        arms = [("ratio", r, max(2, int(round(r * k)))) for r in RATIOS] + \
               [("fixn", np.nan, n) for n in NS_LAD]
        for grid, r, n in arms:
            w = cand_w_fast(px, cache, n)
            ret, turn = fast_bt(px, w)
            row = full_row(f"CAND{n}", ret.loc[st:])
            a, b = keep_paths(row, spy_r, v2_r)
            g_nom, fill = gross_stats(px, w, st)
            brows.append(dict(panel=tag, grid=grid, q=q, k=k, draw=d, prov=prov,
                              arm=f"CAND{n}", n=n, ratio=(r if grid == "ratio" else n / k),
                              Ebar=Ebar, breadth=Ebar / k, gross=g_nom, fill=fill,
                              turnover=float(turn.loc[st:].sum() / ((len(ret.loc[st:])) / 252)),
                              **{kk: vv for kk, vv in row.items() if kk != "tag"},
                              spy_S=spy_r["Sharpe"], spy_CAGR=spy_r["CAGR"], spy_DD=spy_r["MaxDD"],
                              spy_H1=spy_r["H1"], spy_H2=spy_r["H2"], spy_OOS_S=spy_r["OOS_Sharpe"],
                              spy_OOS_CAGR=spy_r["OOS_CAGR"], spy_OOS_DD=spy_r["OOS_MaxDD"],
                              v2_S=v2_r["Sharpe"], v2_H1=v2_r["H1"], v2_H2=v2_r["H2"],
                              v2_DD=v2_r["MaxDD"], v2_OOS_S=v2_r["OOS_Sharpe"],
                              v2_OOS_CAGR=v2_r["OOS_CAGR"], v2_OOS_DD=v2_r["OOS_MaxDD"],
                              pass4a=a, pass4b=b))
        # EWall: the no-selection anchor (ratio = breadth by construction)
        wew = ewall_weights(px)
        ret, turn = fast_bt(px, wew)
        row = full_row("EWall", ret.loc[st:])
        a, b = keep_paths(row, spy_r, v2_r)
        g_nom, fill = gross_stats(px, wew, st)
        brows.append(dict(panel=tag, grid="fixn", q=q, k=k, draw=d, prov=prov, arm="EWall",
                          n=np.nan, ratio=Ebar / k, Ebar=Ebar, breadth=Ebar / k, gross=g_nom,
                          fill=fill, turnover=float(turn.loc[st:].sum() / (len(ret.loc[st:]) / 252)),
                          **{kk: vv for kk, vv in row.items() if kk != "tag"},
                          spy_S=spy_r["Sharpe"], spy_CAGR=spy_r["CAGR"], spy_DD=spy_r["MaxDD"],
                          spy_H1=spy_r["H1"], spy_H2=spy_r["H2"], spy_OOS_S=spy_r["OOS_Sharpe"],
                          spy_OOS_CAGR=spy_r["OOS_CAGR"], spy_OOS_DD=spy_r["OOS_MaxDD"],
                          v2_S=v2_r["Sharpe"], v2_H1=v2_r["H1"], v2_H2=v2_r["H2"],
                          v2_DD=v2_r["MaxDD"], v2_OOS_S=v2_r["OOS_Sharpe"],
                          v2_OOS_CAGR=v2_r["OOS_CAGR"], v2_OOS_DD=v2_r["OOS_MaxDD"],
                          pass4a=a, pass4b=b))
        prows.append(dict(panel=tag, q=q, k=k, draw=d, prov=prov, Ebar=Ebar, breadth=Ebar / k,
                          v2_S=v2_r["Sharpe"], v2_OOS_S=v2_r["OOS_Sharpe"],
                          spy_S=spy_r["Sharpe"], spy_OOS_S=spy_r["OOS_Sharpe"]))
        if (i + 1) % 10 == 0 or i == 0:
            P(f"  [{i+1:3d}/{len(panels)}] {tag}  {time.time()-t0:4.1f}s  "
              f"(elapsed {time.time()-t0all:6.1f}s)")

    books = pd.DataFrame(brows); pans = pd.DataFrame(prows)
    books.to_csv(f"{OUT}.books.csv", index=False); pans.to_csv(f"{OUT}.panels.csv", index=False)
    P(f"\n{len(books)} book rows over {len(pans)} panels written.")

    # ---------------------------------------------------------------- G4
    P("\n" + "=" * 104); P("GATE 4 - REPRODUCTION of idea 688's committed corpus"); P("=" * 104)
    ref = pd.read_csv(B688)
    mine = books[(books.q == 1.00) & (books.grid == "fixn")].copy()
    mine["arm"] = mine.arm.astype(str)
    key = ["k", "draw", "arm"]
    m = ref.merge(mine, on=key, suffixes=("_ref", "_new"))
    COLS = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "IS_Sharpe"]
    P(f"  matched {len(m)} of {len(ref)} committed rows on (k, draw, arm)")
    worst = {c: float(np.abs(m[f"{c}_ref"] - m[f"{c}_new"]).max()) for c in COLS}
    for c in COLS: P(f"    {c:12s} max |d| {worst[c]:.3e}")
    assert len(m) == len(ref) and max(worst.values()) < 1e-9, f"GATE 4 FAILED: {worst}"
    rho_ref = spearman(ref.k, ref.OOS_Sharpe)
    rho_new = spearman(mine.k, mine.OOS_Sharpe)
    means = mine.groupby("k").OOS_Sharpe.mean()
    P(f"  GATE 4 PASS - all {len(ref)} rows to < 1e-9 on 9 statistics.")
    P(f"  headline recomputed: rho(k, OOS Sharpe) = {rho_new:+.4f} (published +0.5269; "
      f"from the committed file {rho_ref:+.4f}); mean OOS Sharpe by k "
      + " -> ".join(f"{v:.4f}" for v in means.values))

    # ================================================================ PART A
    P("\n" + "=" * 104); P("PART A - THE GEOMETRY: what else moves with k when n is held fixed"); P("=" * 104)
    a = books[books.q == 1.00]
    P("\n  A1. selection ratio n/k by (arm, k) - the dial the published ladder never held fixed:")
    P(a[a.grid == "fixn"].pivot_table(index="arm", columns="k", values="ratio", aggfunc="mean")
      .to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  A2. realised FILL = mean target gross / 0.75 (1.00 = the book is fully invested;")
    P("      below 1 the panel cannot fill the book and CAND-n runs DE-GROSSED):")
    P(a[a.grid == "fixn"].pivot_table(index="arm", columns="k", values="fill", aggfunc="mean")
      .to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  A3. the same two columns on the FIXED-RATIO grid (both should be k-flat by construction):")
    P(a[a.grid == "ratio"].pivot_table(index="ratio", columns="k", values="fill", aggfunc="mean")
      .to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  A4. breadth (n_elig/k) by q and k - the panel property the fill rate is made of:")
    P(books.pivot_table(index="q", columns="k", values="breadth", aggfunc="mean")
      .to_string(float_format=lambda x: f"{x:.4f}"))

    # ================================================================ PART B
    P("\n" + "=" * 104); P("PART B - THE QUEUE'S TEST: the k slope at fixed n vs at fixed n/k"); P("=" * 104)
    srows = []
    for q in QS:
        for grid, dial, levels in [("fixn", "n", NS_LAD), ("ratio", "ratio", RATIOS)]:
            sub = books[(books.q == q) & (books.grid == grid)]
            if not len(sub): continue
            pooled = spearman(sub.k, sub.OOS_Sharpe)
            per = {}
            for lv in levels:
                s2 = sub[sub[dial] == lv] if dial == "ratio" else sub[sub.n == lv]
                if len(s2) > 3: per[lv] = spearman(s2.k, s2.OOS_Sharpe)
            mm = sub.groupby("k").OOS_Sharpe.mean()
            srows.append(dict(q=q, grid=grid, n_rows=len(sub), rho_k_OOS=pooled,
                              rho_k_OOS_withinlevel=float(np.mean(list(per.values()))) if per else np.nan,
                              n_levels_pos=sum(v > 0 for v in per.values()), n_levels=len(per),
                              rho_k_IS=spearman(sub.k, sub.IS_Sharpe),
                              rho_k_fill=spearman(sub.k, sub.fill),
                              rho_k_CAGR=spearman(sub.k, sub.OOS_CAGR),
                              rho_k_DD=spearman(sub.k, sub.OOS_MaxDD),
                              partial_k_given_fill=partial_spearman(sub.OOS_Sharpe, sub.k, sub.fill),
                              partial_k_given_ratio=partial_spearman(sub.OOS_Sharpe, sub.k, sub.ratio),
                              partial_ratio_given_k=partial_spearman(sub.OOS_Sharpe, sub.ratio, sub.k),
                              OOS_S_kmin=float(mm.iloc[0]), OOS_S_kmax=float(mm.iloc[-1]),
                              span=float(mm.iloc[-1] - mm.iloc[0]),
                              **{f"meanOOS_k{int(kk)}": float(vv) for kk, vv in mm.items()},
                              **{f"rho_at_{dial}{lv}": v for lv, v in per.items()}))
    slopes = pd.DataFrame(srows)
    slopes.to_csv(f"{OUT}.slopes.csv", index=False)
    SHOW = ["q", "grid", "n_rows", "rho_k_OOS", "rho_k_OOS_withinlevel", "n_levels_pos",
            "n_levels", "rho_k_IS", "rho_k_fill", "partial_k_given_fill",
            "partial_k_given_ratio", "partial_ratio_given_k", "OOS_S_kmin", "OOS_S_kmax", "span"]
    P(slopes[SHOW].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\n  per-k mean OOS Sharpe (every rung, both grids, every q):")
    P(books.pivot_table(index=["q", "grid"], columns="k", values="OOS_Sharpe", aggfunc="mean")
      .to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  the FIXED-RATIO surface at q=1.00, mean OOS Sharpe by (ratio, k) - ALL 24 cells:")
    P(books[(books.q == 1.00) & (books.grid == "ratio")]
      .pivot_table(index="ratio", columns="k", values="OOS_Sharpe", aggfunc="mean")
      .to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  the same surface at q=0.50 and q=0.00:")
    for q in [0.50, 0.00]:
        s2 = books[(books.q == q) & (books.grid == "ratio")]
        if len(s2):
            P(f"  q={q:.2f}:"); P(s2.pivot_table(index="ratio", columns="k", values="OOS_Sharpe",
                                                 aggfunc="mean").to_string(float_format=lambda x: f"{x:.4f}"))

    P("\n  B2. IS THE SURVIVING SLOPE MORE THAN NOISE?  Each (level, draw) gives ONE independent")
    P("      k-series of 3-6 rungs (q=0.00 has only 3: BSTK100 caps k at 100 and its k=100")
    P("      draws are one panel); rho is computed inside it and the signs counted.  A binomial")
    P("      sign test on those series is the honest inference here, since the pooled rho above")
    P("      re-uses each draw across levels.")
    b2 = []
    for q in QS:
        for grid, dial, levels in [("fixn", "n", NS_LAD + ["EWall"]), ("ratio", "ratio", RATIOS)]:
            sub = books[(books.q == q) & (books.grid == grid)]
            if not len(sub): continue
            rr = []
            for lv in levels:
                s2 = sub[sub.arm == "EWall"] if lv == "EWall" else (
                    sub[sub[dial] == lv] if dial == "ratio" else sub[sub.n == lv])
                for d, s3 in s2.groupby("draw"):
                    if s3.k.nunique() >= 3: rr.append(spearman(s3.k, s3.OOS_Sharpe))
            rr = np.array([x for x in rr if np.isfinite(x)])
            pos = int((rr > 0).sum())
            b2.append(dict(q=q, grid=grid, series=len(rr), mean_rho=float(rr.mean()),
                           median_rho=float(np.median(rr)), pos=pos, neg=len(rr) - pos,
                           share_pos=pos / len(rr),
                           t=float(rr.mean() / (rr.std(ddof=1) / np.sqrt(len(rr))))))
    b2 = pd.DataFrame(b2)
    P(b2.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\n  B3. EWall alone - the record's OWN fixed-ratio arm (its ratio IS the breadth, k-flat):")
    for q in QS:
        e = books[(books.q == q) & (books.arm == "EWall")]
        mm = e.groupby("k").OOS_Sharpe.mean()
        P(f"    q={q:.2f}  rho(k, OOS Sharpe) {spearman(e.k, e.OOS_Sharpe):+.4f}   means "
          + " -> ".join(f"{v:.4f}" for v in mm.values))

    # ================================================================ PART C
    P("\n" + "=" * 104); P("PART C - THE CAP-MIX AXIS (the rival explanation), at matched k"); P("=" * 104)
    mk = books[books.grid == "ratio"].pivot_table(index="k", columns="q", values="OOS_Sharpe", aggfunc="mean")
    P(mk.to_string(float_format=lambda x: f"{x:.4f}"))
    both = books[(books.grid == "ratio") & (books.k <= 100)]
    P(f"\n  rho(q, OOS Sharpe) over the k<=100 block where all three q levels exist: "
      f"{spearman(both.q, both.OOS_Sharpe):+.4f}   (n={len(both)})")
    P(f"  partial rho(q, OOS Sharpe | k) = {partial_spearman(both.OOS_Sharpe, both.q, both.k):+.4f}; "
      f"partial rho(k, OOS Sharpe | q) = {partial_spearman(both.OOS_Sharpe, both.k, both.q):+.4f}")
    P("\n  mean OOS CAGR / MaxDD by q (fixed-ratio grid, all k):")
    P(books[books.grid == "ratio"].groupby("q")[["OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "CAGR",
                                                 "Sharpe", "MaxDD"]].mean()
      .to_string(float_format=lambda x: f"{x:.4f}"))

    # ================================================================ PART D
    P("\n" + "=" * 104); P("PART D - PROTOCOL 8 WALK-FORWARD and the KEEP paths"); P("=" * 104)
    wf = pd.concat([rule8(books, "fixn", "n", "n (the published ladder)"),
                    rule8(books, "ratio", "ratio", "n/k (this run)")], ignore_index=True)
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    agg = wf.groupby(["grid", "selector"]).agg(
        picks=("OOS_Sharpe", "size"), mean_k=("k", "mean"), mean_OOS_S=("OOS_Sharpe", "mean"),
        mean_OOS_CAGR=("OOS_CAGR", "mean"), mean_OOS_DD=("OOS_MaxDD", "mean"),
        anchor=("anchor_OOS_S", "mean"), beats_anchor=("beats_anchor", "mean"),
        beats_v2=("beats_v2", "mean"), beats_spy=("beats_spy", "mean"),
        p4a=("pass4a", "sum"), p4b=("pass4b", "sum")).reset_index()
    agg["edge_vs_anchor"] = agg.mean_OOS_S - agg.anchor
    P(agg.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\n  the queue's question at the selector level - K-MAX minus IS-SHARPE-MAX, and K-MAX's")
    P("  edge over the do-nothing anchor, on each grid and each q:")
    for grid in ["fixn", "ratio"]:
        for q in QS:
            w = wf[(wf.grid == grid) & (wf.q == q)]
            if not len(w): continue
            km = w[w.selector == "K-MAX"]; kn = w[w.selector == "K-MIN"]
            P(f"    {grid:5s} q={q:.2f}:  K-MAX OOS {km.OOS_Sharpe.mean():+.4f}  "
              f"K-MIN {kn.OOS_Sharpe.mean():+.4f}  gap {km.OOS_Sharpe.mean()-kn.OOS_Sharpe.mean():+.4f}  "
              f"anchor {km.anchor_OOS_S.mean():+.4f}  edge {km.OOS_Sharpe.mean()-km.anchor_OOS_S.mean():+.4f}  "
              f"vs SPY OOS {km.spy_OOS_S.mean():.4f}  vs v2 OOS {km.v2_OOS_S.mean():.4f}")
    P("\n  OOS levels of the picks against the two comparands (means over picks):")
    P(wf.groupby("grid")[["OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "v2_OOS_CAGR", "v2_OOS_S",
                          "v2_OOS_DD", "spy_OOS_CAGR", "spy_OOS_S", "spy_OOS_DD"]].mean()
      .to_string(float_format=lambda x: f"{x:.4f}"))

    P("\n  KEEP paths on every book row (4a vs RULES v2 on the same panel, 4b vs SPY):")
    kp = books.groupby(["q", "grid"]).agg(rows=("pass4a", "size"), pass4a=("pass4a", "sum"),
                                          pass4b=("pass4b", "sum")).reset_index()
    P(kp.to_string(index=False))
    P("  by k (all q pooled):")
    P(books.groupby("k").agg(rows=("pass4a", "size"), pass4a=("pass4a", "sum"),
                             pass4b=("pass4b", "sum")).to_string())
    if books.pass4b.sum():
        P("  the 4b passers:")
        P(books[books.pass4b][["panel", "grid", "arm", "n", "ratio", "k", "q", "CAGR", "Sharpe",
                               "MaxDD", "H1", "H2", "OOS_Sharpe", "gross", "fill"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P(f"\ntotal elapsed {time.time()-t0all:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
