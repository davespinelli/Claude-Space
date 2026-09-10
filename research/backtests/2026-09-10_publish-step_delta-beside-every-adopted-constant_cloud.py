#!/usr/bin/env python3
"""Idea 408 -- publish step_delta beside every adopted constant.

Idea 401 showed that a 4b margin quoted without a scale is uninterpretable: the record's
adopted constants clear their binding bar by <0.5 GRID STEPS in 4 of 19 passing cells and by
>2 in only 6.  The queue asks for `binding bar / margin / one-step motion` as three required
LEADERBOARD columns, back-filled over the committed KEEP rows.

This file does that, and reports a correction to the proposal itself.  Idea 409 found that a
window width measured in POINTS is not comparable across grid densities (width/point is stable
to ~0.02 while the width in points doubles when you halve the spacing).  `steps = margin /
one-step motion` has exactly the same defect by construction -- the one-step motion is
proportional to the spacing, so `steps` is proportional to 1/spacing and a publisher can make
any constant look safe by publishing a finer grid.  So this run measures BOTH the proposed
unit and a spacing-free one (the dial distance to the flip, margin / |dm/dc|, in the dial's own
units) on the same points, and recommends whichever survives a change of density.

    PART A  CENSUS.  How many of the record's committed KEEP / 4b-pass rows publish a binding
            bar, a margin, or any step motion at all.
    PART B  BACK-FILL.  The six adopted constants of RULES v1/v2 (band, gross, K, n, f, vol),
            each swept on its own host book, on three panels, at three grid densities.  For
            every cell: the binding 4b bar, the signed margin, the one-step motion, `steps`,
            and the spacing-free dial distance to the flip.
    PART C  DENSITY TEST.  Is `steps` invariant to the published spacing?  Is the dial distance?
    PART D  RULE 8 (PROTOCOL 8) + BOTH KEEP PATHS on every grid point.

TWO TUNED PARAMETERS, and no more (PROTOCOL 4):
    PANEL      in {U56, B136, SMALL439}
    STEP_SCALE in {x1, x2, x4}   (the published spacing, halved, quartered)
The six dials, their host books and their adopted values are READ FROM RULES.md and
baseline.py, not chosen here; the dial grids are centred on the adopted value at the record's
own published spacing.  Every grid point is written to .grid.csv.

PROTOCOL-fixed: weights decided at close t, applied at t+1; 10 bps per unit turnover; long
only, no leverage; warm-up 260 rows dropped; halves at len(r)//2; rule 8 split 2016-12-31.
SURVIVORSHIP: B136 and SMALL439 are CURRENT constituent lists (PROTOCOL 9); SMALL439 drops the
44 names with data/small_meta.csv max_1d_move >= 1.0 (idea 623's terminal-dated screen, priced
by idea 627), because the published rows this file back-fills all carry that convention.

Run:  python3 research/backtests/2026-09-10_publish-step_delta-beside-every-adopted-constant_cloud.py
"""
import re, sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, rebalance_mask, metrics  # noqa

pd.set_option("display.width", 250)
OUT = Path(__file__).with_suffix("")
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COST_BPS, WARMUP, FREQ = 10.0, 260, "W"
SCALES = {"x1": 1, "x2": 2, "x4": 4}


# ---------------------------------------------------------------- vectorised engine (gated)
def fast_backtest(prices, weights, freq=FREQ):
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy(); m[0] = True
    T, Ncol = rets.shape
    C = np.cumprod(1.0 + rets, axis=0); Cp = np.vstack([np.ones((1, Ncol)), C[:-1]])
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]; W0 = wt[s0]
    h = W0 * (Cp / Cp[s0]); V = h.sum(axis=1) + (1.0 - W0.sum(axis=1)); held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]; W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p]); Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1)); heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T); turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return pd.Series((held * rets).sum(axis=1), index=idx), pd.Series(turn, index=idx)


# =============================================== the six adopted constants and their host books
# name        adopted   published spacing   host   (source)
DIALS = {
    "band":  dict(c0=0.03, step=0.01,  lo=0.00,  hi=0.12,  host="V2", src="RULES.md cl.2"),
    "gross": dict(c0=0.75, step=0.05,  lo=0.30,  hi=1.20,  host="V2", src="RULES.md cl.4"),
    "K":     dict(c0=200,  step=25,    lo=50,    hi=350,   host="V2", src="RULES.md cl.2 (ma200)"),
    "n":     dict(c0=5,    step=4,     lo=1,     hi=29,    host="V1", src="baseline.rules_v1_weights"),
    "f":     dict(c0=0.5,  step=0.1,   lo=0.0,   hi=1.0,   host="V1", src="baseline.score"),
    "vol":   dict(c0=0.60, step=0.05,  lo=0.30,  hi=0.90,  host="V1", src="baseline.rules_v1_weights"),
}


class Panel:
    """Memoises the pieces of baseline.score / band_state that the dials do not move."""

    def __init__(self, px):
        self.px = px
        q = px.drop(columns=["SPY"])
        self.q = q
        mom = q.shift(21) / q.shift(252) - 1
        r6 = q / q.shift(126) - 1
        r3 = q / q.shift(63) - 1
        self.comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True)
                     + r3.rank(axis=1, pct=True)) / 3
        self.vol20 = q.pct_change().rolling(20).std() * np.sqrt(252)
        self.notna = q.notna()
        self._ma, self._above, self._band = {}, {}, {}

    def ma(self, K):
        if K not in self._ma: self._ma[K] = self.q.rolling(int(K)).mean()
        return self._ma[K]

    def above(self, K):
        if K not in self._above: self._above[K] = self.q > self.ma(K)
        return self._above[K]

    def band_state(self, K, band):
        key = (K, round(float(band), 6))
        if key not in self._band:
            ma = self.ma(K)
            raw = pd.DataFrame(np.nan, index=self.q.index, columns=self.q.columns)
            raw = raw.mask(self.q > ma * (1 + band), 1.0).mask(self.q < ma * (1 - band), 0.0)
            self._band[key] = raw.ffill().fillna(0.0) > 0.5
        return self._band[key]

    # ---- host book V2: RULES v2 with (band, gross, K) open
    def w_v2(self, band, gross, K):
        e = self.notna.astype(float)
        ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        return ew.where(self.band_state(K, band), 0.0)

    # ---- host book V1: RULES v1 with (n, f, vol, K) open.  Sizing w=0.15 as adopted.
    def w_v1(self, n, f, vol, K, w=0.15):
        s = self.comp * ((1.0 - f) + f * self.above(K).astype(float))
        s = s / self.vol20.clip(lower=0.08) ** 0.5
        elig = s.where(self.above(K) & (self.vol20 < vol))
        rank = elig.rank(axis=1, ascending=False)
        return (rank <= n).astype(float) * w

    def book(self, dial, c):
        d = DIALS[dial]
        if d["host"] == "V2":
            band = c if dial == "band" else DIALS["band"]["c0"]
            gross = c if dial == "gross" else DIALS["gross"]["c0"]
            K = c if dial == "K" else DIALS["K"]["c0"]
            return self.w_v2(band, gross, int(K))
        n = c if dial == "n" else DIALS["n"]["c0"]
        f = c if dial == "f" else DIALS["f"]["c0"]
        vol = c if dial == "vol" else DIALS["vol"]["c0"]
        K = c if dial == "K" else DIALS["K"]["c0"]
        return self.w_v1(int(n), f, vol, int(K))


# ------------------------------------------------------------------------- metric readings
def legs(r):
    r = r.iloc[WARMUP:]
    h = len(r) // 2
    f, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    ins, oos = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    return dict(CAGR=f["CAGR"], Sharpe=f["Sharpe"], MaxDD=f["MaxDD"], H1=m1["Sharpe"],
                H2=m2["Sharpe"], IS=ins["Sharpe"], OOS=oos["Sharpe"],
                OOS_CAGR=oos["CAGR"], OOS_DD=oos["MaxDD"])


def margins_4b(L, S):
    """The five 4b bars as SIGNED margins in the bar's own units (>=0 passes)."""
    return dict(H1=L["H1"] - S["H1"], H2=L["H2"] - S["H2"], OOS=L["OOS"] - S["OOS"],
                DD=L["MaxDD"] - 0.60 * S["MaxDD"], CAGR=L["CAGR"] - 0.70 * S["CAGR"])


def v4a(L, B):
    return int(L["H1"] > B["H1"] and L["H2"] > B["H2"] and L["MaxDD"] >= B["MaxDD"])


def grid_for(dial, scale):
    d = DIALS[dial]; h = d["step"] / scale
    if dial in ("K", "n"):
        h = max(1, int(round(h)))
        g = list(range(int(d["c0"]), int(d["lo"]) - 1, -h))[::-1] + \
            list(range(int(d["c0"]) + h, int(d["hi"]) + 1, h))
        return sorted(set(g)), h
    lo, hi, c0 = d["lo"], d["hi"], d["c0"]
    nlo, nhi = int(round((c0 - lo) / h)), int(round((hi - c0) / h))
    g = [round(c0 + i * h, 8) for i in range(-nlo, nhi + 1)]
    return g, h


# ------------------------------------------------------------------------------- the panels
def load_panels():
    P = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    P["SMALL439"] = sm.drop(columns=[c for c in sm.columns if c in bad])
    return P


# ==================================================================================== GATES
def gate_g1(P):
    """G1  fast_backtest reproduces engine.backtest on returns AND turnover."""
    w = P.w_v2(0.03, 0.75, 200)
    fr, ft = fast_backtest(P.q, w)
    eng = backtest(P.q, w, cost_bps=0.0, freq=FREQ)
    st = P.q.index[WARMUP]
    dr = float((fr.loc[st:] - eng["returns"].loc[st:]).abs().max())
    dt_ = float((ft.loc[st:] - eng["turnover"].loc[st:]).abs().max())
    print(f"G1  fast_backtest vs engine.backtest: max|dret| {dr:.3e}  max|dturn| {dt_:.3e}")
    assert dr < 1e-10 and dt_ < 1e-10, "G1 FAILED"


def gate_g2(P):
    """G2  the memoised host books reproduce baseline's own functions at the adopted values,
    so the dials really are sweeping the ADOPTED constants and not a look-alike."""
    a = P.w_v2(0.03, 0.75, 200)
    b = rules_v2_weights(P.q, band=0.03, gross=0.75)
    d2 = float((a - b).abs().max().max())
    c = P.w_v1(5, 0.5, 0.60, 200)
    e = rules_v1_weights(P.q, n=5, w=0.15, max_vol=0.60, vol_scale=True)
    d1 = float((c - e).abs().max().max())
    print(f"G2  host V2 vs baseline.rules_v2_weights {d2:.3e};  host V1 vs rules_v1_weights {d1:.3e}")
    assert d2 < 1e-12 and d1 < 1e-12, "G2 FAILED"


def gate_g3(P):
    """G3  every dial's grid CONTAINS its adopted value at all three densities, and the
    adopted point gives the identical book at every density (no off-grid interpolation)."""
    worst = 0.0
    for dl in DIALS:
        ref = None
        for sc in SCALES.values():
            g, h = grid_for(dl, sc)
            assert DIALS[dl]["c0"] in g, f"G3 FAILED: {dl} x{sc} grid misses its adopted value"
            w = P.book(dl, DIALS[dl]["c0"])
            if ref is None: ref = w
            else: worst = max(worst, float((w - ref).abs().max().max()))
    print(f"G3  adopted value on-grid at all 3 densities for all 6 dials; "
          f"max|dweight| across densities {worst:.3e}")
    assert worst == 0.0, "G3 FAILED"


# ================================================================== PART A: the census
KEEPROW = re.compile(r"\bKEEP\b", re.I)
BINDPAT = re.compile(r"\b(binding bar|binds?\b|bar that (?:cuts|binds)|failing leg|sole (?:bar|cut))", re.I)
MARGPAT = re.compile(r"\b(margin|m_min|m4b|clears? (?:it|the bar) by|misses? .{0,20}by)\b", re.I)
STEPPAT = re.compile(r"\b(step_delta|one-step|grid step|per (?:grid )?step|spacing|steps? of the dial)\b", re.I)


def census():
    print("\n=== PART A  CENSUS of the record's committed rows ===")
    lb = (ROOT / "research" / "LEADERBOARD.md").read_text().split("\n")
    rows = [l for l in lb if l.startswith("|") and l.count("|") >= 8][2:]
    keep = [l for l in rows if KEEPROW.search(l.split("|")[-3] if len(l.split("|")) > 3 else "")]
    def sh(pat, sub): return sum(1 for l in sub if pat.search(l))
    print(f"  LEADERBOARD rows parsed: {len(rows)}   rows whose VERDICT column says KEEP: {len(keep)}")
    for nm, pat in (("binding bar", BINDPAT), ("a margin", MARGPAT), ("a step / spacing", STEPPAT)):
        print(f"    KEEP rows naming {nm:18s}: {sh(pat,keep):4d}/{len(keep)}"
              f"      all rows: {sh(pat,rows):4d}/{len(rows)}")
    ch = (ROOT / "research" / "CHANGELOG.md").read_text()
    blocks = [b for b in ch.split("\n- 20") if b.strip()]
    print(f"  CHANGELOG entries: {len(blocks)}   naming a step/spacing: "
          f"{sum(1 for b in blocks if STEPPAT.search(b))}   naming a margin: "
          f"{sum(1 for b in blocks if MARGPAT.search(b))}")
    return len(rows), len(keep)


# ==================================================================================== main
def main():
    n_rows, n_keep = census()

    panels = {k: Panel(v) for k, v in load_panels().items()}
    print("\nPANELS")
    for pn, P in panels.items():
        print(f"  {pn:9s} {P.q.shape[1]:4d} names  {P.q.index[0].date()} .. {P.q.index[-1].date()}")
    gate_g1(panels["U56"]); gate_g2(panels["U56"]); gate_g3(panels["U56"])

    print("\n=== PART B  BACK-FILL: every dial x panel x density ===")
    rows = []
    for pn, P in panels.items():
        spy = P.px["SPY"].pct_change().fillna(0.0)
        S = legs(spy)
        Bl = legs(fast_backtest(P.q, P.w_v2(0.03, 0.75, 200))[0]
                  - fast_backtest(P.q, P.w_v2(0.03, 0.75, 200))[1] * COST_BPS / 1e4)
        for dl in DIALS:
            for sn, sc in SCALES.items():
                g, h = grid_for(dl, sc)
                for c in g:
                    r, t = fast_backtest(P.q, P.book(dl, c))
                    L = legs(r - t * COST_BPS / 1e4)
                    mg = margins_4b(L, S)
                    bind = min(mg, key=mg.get)
                    rows.append(dict(panel=pn, dial=dl, scale=sn, h=h, c=c,
                                     adopted=int(c == DIALS[dl]["c0"]), bind=bind,
                                     m4b=mg[bind], v4b=int(mg[bind] >= 0), v4a=v4a(L, Bl),
                                     **{f"m_{k}": v for k, v in mg.items()}, **L))
        print(f"  {pn}: done ({len(rows)} rows so far)")
    G = pd.DataFrame(rows)
    G.to_csv(OUT.with_suffix(".grid.csv"), index=False)
    print(f"  grid points: {len(G)} -> {OUT.with_suffix('.grid.csv').name}")

    # ---------- the three proposed columns, back-filled at the adopted value
    bf = []
    for (pn, dl, sn), sub in G.groupby(["panel", "dial", "scale"]):
        sub = sub.sort_values("c").reset_index(drop=True)
        i = int(sub.index[sub.adopted == 1][0])
        c0, h = sub.c[i], sub.h[i]
        bind, m = sub.bind[i], sub.m4b[i]
        # the one-step motion of THE SAME bar the adopted point binds on
        col = "m_" + bind
        up = sub[col][i + 1] - sub[col][i] if i + 1 < len(sub) else np.nan
        dn = sub[col][i - 1] - sub[col][i] if i - 1 >= 0 else np.nan
        step_delta = np.nanmean([abs(up), abs(dn)])
        slope = (sub[col][i + 1] - sub[col][i - 1]) / (2 * h) if 0 < i < len(sub) - 1 else np.nan
        bf.append(dict(panel=pn, dial=dl, scale=sn, c0=c0, h=h, bind=bind, margin=m,
                       step_delta=step_delta,
                       steps=abs(m) / step_delta if step_delta > 0 else np.inf,
                       slope=slope,
                       dial_dist=abs(m) / abs(slope) if slope and abs(slope) > 0 else np.inf,
                       pass4b=int(m >= 0), pass4a=int(sub.v4a[i])))
    BF = pd.DataFrame(bf)
    BF.to_csv(OUT.with_suffix(".backfill.csv"), index=False)

    print("\n--- B1  the three PROPOSED columns at the record's own published spacing (x1) ---")
    x1 = BF[BF.scale == "x1"].set_index(["panel", "dial"])[
        ["c0", "h", "bind", "margin", "step_delta", "steps", "slope", "dial_dist", "pass4b", "pass4a"]]
    print(x1.to_string(float_format=lambda x: f"{x:.4g}"))
    print(f"\n  adopted constants clearing their binding bar (margin >= 0): "
          f"{int(x1.pass4b.sum())}/{len(x1)};  4a: {int(x1.pass4a.sum())}/{len(x1)}")
    p = x1[x1.pass4b == 1]
    if len(p):
        print(f"  of the {len(p)} passing cells: steps < 0.5 in {(p.steps < 0.5).sum()}, "
              f"steps > 2 in {(p.steps > 2).sum()}  (idea 401 reported 4/19 and 6/19)")
    print("\n--- B2  binding bar, over all grid points and at the adopted values ---")
    print("  all points:", G.bind.value_counts().to_dict())
    print("  adopted:   ", G[G.adopted == 1].bind.value_counts().to_dict())

    print("\n=== PART C  DENSITY TEST: does the unit survive a change of published spacing? ===")
    piv = BF.pivot_table(index=["panel", "dial"], columns="scale",
                         values=["steps", "dial_dist", "step_delta"])
    print(piv.to_string(float_format=lambda x: f"{x:.4g}"))
    fin = BF[np.isfinite(BF.steps) & np.isfinite(BF.dial_dist)]
    rat = fin.pivot_table(index=["panel", "dial"], columns="scale", values=["steps", "dial_dist"])
    out = []
    for u in ("steps", "dial_dist"):
        a, b = rat[(u, "x1")], rat[(u, "x4")]
        ok = a.notna() & b.notna() & (a > 0)
        out.append(dict(unit=u, n=int(ok.sum()), median_x4_over_x1=float((b[ok] / a[ok]).median()),
                        iqr=float((b[ok] / a[ok]).quantile(0.75) - (b[ok] / a[ok]).quantile(0.25)),
                        share_within_2x=float((((b[ok] / a[ok]) < 2) & ((b[ok] / a[ok]) > 0.5)).mean())))
    C = pd.DataFrame(out).set_index("unit")
    print("\n--- C1  ratio of the unit at x4 spacing to the unit at x1 (1.0 = density-free) ---")
    print(C.to_string(float_format=lambda x: f"{x:.4g}"))
    print("  A unit whose median ratio is ~4 is measuring the GRID, not the constant; a unit\n"
          "  whose median ratio is ~1 is a property of the dial.")

    print("\n--- C2  step_delta itself vs spacing (should be exactly proportional) ---")
    sd = BF.pivot_table(index=["panel", "dial"], columns="scale", values="step_delta")
    print((sd["x1"] / sd["x4"]).describe().to_string(float_format=lambda x: f"{x:.4g}"))

    # ================================================ PART D: rule 8 and both KEEP paths
    print("\n=== PART D  RULE 8 (PROTOCOL 8) and BOTH KEEP PATHS ===")
    print(f"  4a {int(G.v4a.sum())}/{len(G)}   4b {int(G.v4b.sum())}/{len(G)}")
    print("\n--- D1  4b pass rate by dial x panel (all densities pooled) ---")
    print(G.pivot_table(index="dial", columns="panel", values="v4b", aggfunc="mean")
          .to_string(float_format=lambda x: f"{x:.3f}"))
    print("\n--- D2  rule 8: dial value chosen on IS (2010-2016) Sharpe ALONE at each density, "
          "OOS (2017-2026) read once ---")
    r8 = []
    for (pn, dl, sn), sub in G.groupby(["panel", "dial", "scale"]):
        P = panels[pn]
        spy = legs(P.px["SPY"].pct_change().fillna(0.0))
        r, t = fast_backtest(P.q, P.w_v2(0.03, 0.75, 200))
        bl = legs(r - t * COST_BPS / 1e4)
        pick = sub.loc[sub.IS.idxmax()]
        adp = sub[sub.adopted == 1].iloc[0]
        r8.append(dict(panel=pn, dial=dl, scale=sn, pick=pick.c, adopted=adp.c,
                       moved=int(pick.c != adp.c), IS=pick.IS,
                       OOS_CAGR=pick.OOS_CAGR, OOS=pick.OOS, OOS_DD=pick.OOS_DD,
                       adp_OOS=adp.OOS, v2_OOS=bl["OOS"], v2_OOS_CAGR=bl["OOS_CAGR"],
                       v2_OOS_DD=bl["OOS_DD"], spy_OOS=spy["OOS"], spy_OOS_CAGR=spy["OOS_CAGR"],
                       spy_OOS_DD=spy["OOS_DD"], pick4b=int(pick.v4b), pick4a=int(pick.v4a)))
    R8 = pd.DataFrame(r8)
    R8.to_csv(OUT.with_suffix(".rule8.csv"), index=False)
    print(R8.set_index(["panel", "dial", "scale"]).to_string(float_format=lambda x: f"{x:.4f}"))
    print(f"\n  rule 8 MOVES the constant in {int(R8.moved.sum())}/{len(R8)} cells; "
          f"its pick beats the adopted value OOS in {int((R8.OOS > R8.adp_OOS).sum())}/{len(R8)}; "
          f"mean OOS Sharpe premium of the pick over the adopted value "
          f"{float((R8.OOS - R8.adp_OOS).mean()):+.4f}")
    print(f"  pick beats RULES v2 OOS Sharpe in {int((R8.OOS > R8.v2_OOS).sum())}/{len(R8)}; "
          f"beats SPY OOS Sharpe in {int((R8.OOS > R8.spy_OOS).sum())}/{len(R8)}; "
          f"pick is a 4b passer in {int(R8.pick4b.sum())}/{len(R8)}, a 4a passer in "
          f"{int(R8.pick4a.sum())}/{len(R8)}")

    # ============================== PART E: the 4b passers, under PROTOCOL 2's no-leverage rule
    print("\n=== PART E  THE 4b PASSERS, re-read under PROTOCOL 2 (no leverage) ===")
    P4 = G[G.v4b == 1]
    print(f"  4b passes: {len(P4)}, all on the '{'/'.join(sorted(P4.dial.unique()))}' dial, "
          f"c in [{P4.c.min()}, {P4.c.max()}]")
    lev = P4[P4.c > 1.0]
    print(f"  of these, {len(lev)} ({len(lev)/len(P4):.1%}) sit at gross > 1.00, i.e. the book "
          f"BORROWS.  PROTOCOL 2 forbids leverage unless the idea says so, and idea 402 charges "
          f"300 bps to borrow, which this file does not.  Those {len(lev)} are NOT 4b passes.")
    hon = P4[P4.c <= 1.0]
    print(f"  HONEST 4b passes (gross <= 1.00): {len(hon)}/{len(G)}")
    print(hon[["panel", "dial", "scale", "c", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS",
               "OOS", "OOS_CAGR", "OOS_DD", "m4b", "bind"]]
          .sort_values(["panel", "scale", "c"]).to_string(index=False,
                                                          float_format=lambda x: f"{x:.4f}"))
    print("\n--- E1  RULE 8 on the gross dial with the no-leverage constraint imposed "
          "(grid c <= 1.00), IS Sharpe alone chooses, OOS read once ---")
    e1 = []
    for (pn, sn), sub in G[(G.dial == "gross") & (G.c <= 1.0)].groupby(["panel", "scale"]):
        P = panels[pn]
        spy = legs(P.px["SPY"].pct_change().fillna(0.0))
        r, t = fast_backtest(P.q, P.w_v2(0.03, 0.75, 200))
        bl = legs(r - t * COST_BPS / 1e4)
        pk = sub.loc[sub.IS.idxmax()]
        e1.append(dict(panel=pn, scale=sn, pick=pk.c, IS=pk.IS, CAGR=pk.CAGR, Sharpe=pk.Sharpe,
                       MaxDD=pk.MaxDD, H1=pk.H1, H2=pk.H2, OOS=pk.OOS, OOS_CAGR=pk.OOS_CAGR,
                       OOS_DD=pk.OOS_DD, v4b=int(pk.v4b), v4a=int(pk.v4a), m4b=pk.m4b,
                       v2_OOS=bl["OOS"], v2_OOS_CAGR=bl["OOS_CAGR"], v2_OOS_DD=bl["OOS_DD"],
                       spy_OOS=spy["OOS"], spy_OOS_CAGR=spy["OOS_CAGR"], spy_OOS_DD=spy["OOS_DD"],
                       spy_H1=spy["H1"], spy_H2=spy["H2"]))
    E1 = pd.DataFrame(e1).set_index(["panel", "scale"])
    E1.to_csv(OUT.with_suffix(".noleverage.csv"))
    print(E1.to_string(float_format=lambda x: f"{x:.4f}"))
    print(f"\n  rule 8's no-leverage pick is a 4b passer in {int(E1.v4b.sum())}/{len(E1)} cells, "
          f"a 4a passer in {int(E1.v4a.sum())}/{len(E1)}")
    print("  CAUTION, stated with the result: Sharpe is FLAT in gross on this book (U56 x1 range "
          f"{G[(G.panel=='U56')&(G.dial=='gross')&(G.scale=='x1')].Sharpe.min():.4f}"
          f"-{G[(G.panel=='U56')&(G.dial=='gross')&(G.scale=='x1')].Sharpe.max():.4f}) while CAGR "
          "and MaxDD are both linear in it, so a 4b verdict decided on the CAGR floor is decided "
          "by the book's CASH WEIGHT.  That is idea 311's g-band loophole and idea 585's open "
          "question, not a new signal.")

    print("\n=== VERDICT ===")
    print(f"  4a {int(G.v4a.sum())}/{len(G)}   4b {int(G.v4b.sum())}/{len(G)} "
          f"({len(hon)} of them honest under PROTOCOL 2's no-leverage rule)")


if __name__ == "__main__":
    main()
