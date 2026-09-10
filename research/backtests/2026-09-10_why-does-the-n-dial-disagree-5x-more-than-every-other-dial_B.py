#!/usr/bin/env python3
"""Idea 494 — why does the n dial disagree 5x more than every other dial? (lane B, 2026-09-10)

QUEUE ASK
    Idea 270 found S_CAGR/S_SHARPE selector disagreement at 58.3% on the `n` dial against
    8-17% on cadence, gross, volgate and trim, on the same panels and the same base book.
    The queue's candidate mechanism: n moves realised gross AND concentration together while
    the other dials move one thing.  The ask: decompose the IS Sharpe and IS CAGR surfaces of
    each dial into a LEVEL term and a CURVATURE term, and report whether disagreement tracks
    the CURVATURE GAP between the two surfaces.

    Idea 499 already killed the panel explanation ("the ordering is DIAL-driven, the panel set
    is nearly irrelevant") and pointed at ARM-MENU composition.  This run tests the queue's
    surface-geometry explanation on exactly idea 499's grid, so every number here sits beside
    a published one.

DESIGN
    The grid is idea 499's, reproduced verbatim and re-read: 12 panels x 2 dial sets
    (lane B's 5 dials, the cloud parent's 6) x their arms, 10 bps, weekly base cadence except
    on the cadence dial, CAL and MID split conventions both computed.  Nothing about the
    backtests is new; what is new is the SURFACE DECOMPOSITION laid over each cell.

    For one cell (panel, dialset, dial) and one metric m in {IS_Sharpe, IS_CAGR}:
        1. order the arms along the dial (ORD spacing: equally spaced by arm order;
           VAL spacing: by the dial's own value where one exists -- log for n and cadence,
           linear for gross/volgate/trim/band/quantile).  Both spacings are ENUMERATED and
           both are written out; ORD is the headline because `EWall` and `FREQ_*` have no
           common numeric value.
        2. map the ordered positions onto x in [-1, +1].
        3. z-score the metric ACROSS THE ARMS OF THAT CELL (so a surface's units and its
           overall height drop out -- the decomposition is about SHAPE, not level of return).
        4. least-squares fit  z = b0 + b1*x + b2*q(x),  q = x^2 orthogonalised against
           {1, x} on that cell's own x grid.  b1 is the LEVEL term (monotone tilt: which
           end of the dial the surface prefers), b2 the CURVATURE term (interior peak vs
           interior trough).  R2 of the fit is recorded so a badly-described surface is
           visible rather than silently treated as a parabola.
    Then per cell:
        LEVELGAP = |b1_Sharpe - b1_CAGR|,  CURVGAP = |b2_Sharpe - b2_CAGR|,
        SHAPEDIST = euclidean distance between the two z-surfaces (the model-free comparand).
    A cell DISAGREES iff argmax IS_Sharpe and argmax IS_CAGR pick a different arm -- idea
    270's and idea 499's own definition, arm identity, no tie band.

    THE TEST (three readings, all pre-registered, all reported whatever they say)
      T1  Does disagreement track CURVGAP?  Point-biserial correlation and a panel-clustered
          permutation test, pooled over all cells, and the per-dial Spearman between mean
          CURVGAP and the dial's disagreement rate.
      T2  Does it track CURVGAP better than LEVELGAP?  Same statistics for LEVELGAP, plus a
          two-covariate logistic fit (both standardised) so the terms compete directly.
      T3  Does the `n` dial's excess survive the geometry?  Fit disagreement on CURVGAP and
          LEVELGAP only, then compare each dial's OBSERVED rate to the rate the geometry
          model predicts.  If the queue's mechanism is right the n dial's residual is ~0.

    Idea 499's honest caveat -- that "dial set" bundles book form, ranking key, eligibility
    legs and arm list -- applies here too.  The decomposition does not unbundle those; it
    asks only whether the SHAPE statistics of the two IS surfaces suffice to explain where
    the two selectors part company.

RULE 8 / WHY THIS COSTS CAPITAL ANYTHING
    If CURVGAP explains disagreement it is an IS-only quantity, so it can be used as an
    ABSTENTION rule: when the two IS surfaces disagree in curvature by more than tau, refuse
    to tune the dial and hold the cell's DONOTHING arm; otherwise take S_SHARPE's pick.  The
    threshold ladder tau is pre-registered and EVERY grid point is reported.  Books are chosen
    on IS 2009-01-01..2016-12-31 only and read once on OOS 2017-01-01+, against the LIVE
    RULES v2 baseline, RULES v1, SPY and the DONOTHING arm.  Both KEEP paths are evaluated for
    every arm and for every selector book.

TUNED PARAMETERS (PROTOCOL rule 4: max 2)
    1. the dial value inside a cell -- chosen by each selector on IS only, never on OOS.
    2. the abstention threshold tau on CURVGAP -- pre-registered ladder, ALL points reported.
    dialset / panelset / spacing / split are ENUMERATED axes, not tuned: every point is
    written to .arms.csv, .cells.csv and .abstain.csv.

CONVENTIONS
    10 bps per unit turnover, weights decided at close t applied at t+1 (engine), long only,
    no leverage, weekly base cadence except on the cadence dial.  4a judged against the LIVE
    RULES v2 book on the same panel, 4b against SPY, per PROTOCOL rule 4.
    SURVIVORSHIP: B136 / BSTK100 are current constituents of a current screen; SMALL439 is the
    483-name sub-$2B panel with the 44 tickers whose max_1d_move >= 1.0 dropped first
    (data/small_meta.csv, data/SMALL_PANEL_README.md).  The 8 seeded sub-panels inherit it.
    No network is used.

Outputs: .arms.csv .cells.csv .geometry.csv .abstain.csv .walkforward.csv .console.txt
"""
from __future__ import annotations
import json, sys, time, warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))
from baseline import load_universe, score, band_state                     # noqa: E402
from engine import backtest, metrics, rebalance_mask                      # noqa: E402

STEM = Path(__file__).name[:-3]
OUT = REPO / "research" / "backtests"

GROSS, BAND, MAX_VOL, W_FIXED = 0.75, 0.03, 0.60, 0.15
IS_START, IS_END, OOS_START = "2009-01-01", "2016-12-31", "2017-01-01"
SAT_CAP = 0.25
COST = 10
N_PERM = 20000
SEED = 494
TAUS = [0.00, 0.25, 0.50, 0.75, 1.00, 1.50, 2.00, 1e9]   # pre-registered CURVGAP ladder

_log: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _log.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ============================================================== panels (idea 499's, verbatim)
def build_panels():
    U = json.loads((REPO / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    etf36 = [t for t in U["broad"] + U["sectors"] + U["bonds_fx_commod"] if t not in crypto]
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    b_stk = [t for t in px136.columns if t not in set(etf36) and t != "SPY"]
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]

    def sub(px, cols, tradable=None):
        cols = [c for c in cols if c in px.columns]
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
        p = px[keep].dropna(how="all").ffill()
        return p, set(tradable if tradable is not None else cols)

    panels = {
        "U56": sub(px56, list(px56.columns)),
        "B136": sub(px136, list(px136.columns)),
        "BSTK100": sub(px136, b_stk, tradable=b_stk),
        "SMALL439": sub(pxs, s_stk, tradable=s_stk),
    }
    for seed in range(8):
        rng = np.random.default_rng(1000 + seed)
        pool, k, src = (b_stk, 60, px136) if seed < 4 else (s_stk, 120, pxs)
        pick = sorted(rng.choice(np.array(sorted(pool)), size=k, replace=False).tolist())
        panels[f"S{seed}_{'B' if seed < 4 else 'M'}{k}"] = sub(src, pick, tradable=pick)
    return panels


# ============================================================== book forms (idea 499's, verbatim)
def _ew(px, mask, gross, tradable):
    e = mask.astype(float).where(px.notna(), 0.0)
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        e[drop] = 0.0
    return gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def b_eligible(px, tradable, max_vol=MAX_VOL):
    _, above, vol20 = score(px)
    m = (above & (vol20 < max_vol)).copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m[drop] = False
    return m


def b_weights(px, tradable, spec):
    kind = spec["kind"]
    if kind == "v1":
        s = score(px, vol_scale=True)[0]
        rank = s.where(b_eligible(px, tradable)).rank(axis=1, ascending=False)
        return (rank <= 5).astype(float) * W_FIXED
    if kind in ("v2", "BAND"):
        st = band_state(px, spec.get("band", BAND))
        e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
        drop = [c for c in px.columns if c not in tradable]
        if drop:
            e[drop] = 0.0
        g = spec.get("gross", GROSS)
        ew = g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        return ew.where(st, 0.0)
    elig = b_eligible(px, tradable, spec.get("max_vol", MAX_VOL))
    if kind == "EW":
        sel = elig.astype(float)
    elif kind == "FWD":
        key = score(px, vol_scale=False)[0]
        sel = (key.where(elig).rank(axis=1, ascending=False) <= spec["n"]).astype(float)
    else:
        raise ValueError(kind)
    held = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(held, axis=0).mul(spec.get("gross", GROSS)).fillna(0.0)


def b_dials():
    base = dict(kind="EW", n=None, gross=GROSS, max_vol=MAX_VOL, band=None, freq="W")
    a = {"n": [("EWall", dict(base))], "cadence": [], "gross": [], "volgate": [], "trim": []}
    for n in [5, 10, 20, 30, 40, 60]:
        a["n"].append((f"FWD{n}", dict(base, kind="FWD", n=n)))
    for f in ["D", "W", "M", "Q"]:
        a["cadence"].append((f"FREQ_{f}", dict(base, freq=f)))
    for g in [0.25, 0.40, 0.55, 0.70, 0.85, 1.00]:
        a["gross"].append((f"G{g:.2f}", dict(base, gross=g)))
    for v in [0.30, 0.40, 0.50, 0.60, 0.80, 1.00]:
        a["volgate"].append((f"V{v:.2f}", dict(base, max_vol=v)))
    for b in [0.00, 0.01, 0.02, 0.03, 0.05, 0.08]:
        a["trim"].append((f"B{b:.2f}", dict(base, kind="BAND", band=b)))
    return a


def c_topn(px, tr, n, gross=GROSS):
    s, above, _ = score(px)
    return _ew(px, s.where(above).rank(axis=1, ascending=False) <= n, gross, tr)


def c_bandbook(px, tr, band, gross=GROSS):
    st = band_state(px, band)
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    drop = [c for c in px.columns if c not in tr]
    if drop:
        e[drop] = 0.0
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(st, 0.0)


def c_volcap(px, tr, cap, gross=GROSS):
    _, above, vol20 = score(px)
    return _ew(px, above & (vol20 < cap), gross, tr)


def c_quantile(px, tr, x, gross=GROSS):
    s, above, _ = score(px)
    r = s.where(above).rank(axis=1, ascending=False, pct=True)
    return _ew(px, r <= x, gross, tr)


def c_dials():
    return {
        "n":        [(f"N{v}", dict(form="topn", v=v, freq="W")) for v in [5, 10, 20, 30, 50]],
        "band":     [(f"B{v:.2f}", dict(form="band", v=v, freq="W")) for v in [0.00, 0.01, 0.03, 0.05, 0.08, 0.12]],
        "gross":    [(f"G{v:.2f}", dict(form="gross", v=v, freq="W")) for v in [0.25, 0.50, 0.75, 1.00]],
        "volcap":   [(f"V{v:.2f}", dict(form="volcap", v=v, freq="W")) for v in [0.30, 0.45, 0.60, 0.90, 9.99]],
        "quantile": [(f"Q{v:.2f}", dict(form="quant", v=v, freq="W")) for v in [0.10, 0.25, 0.50, 0.75, 1.00]],
        "cadence":  [(f"FREQ_{f}", dict(form="band", v=BAND, freq=f)) for f in ["D", "W", "M", "Q"]],
    }


def c_weights(px, tr, spec):
    f, v = spec["form"], spec["v"]
    if f == "topn":
        return c_topn(px, tr, v)
    if f == "band":
        return c_bandbook(px, tr, v)
    if f == "gross":
        return c_bandbook(px, tr, BAND, gross=v)
    if f == "volcap":
        return c_volcap(px, tr, v)
    if f == "quant":
        return c_quantile(px, tr, v)
    raise ValueError(f)


# ============================================================== metric helpers
def halves(r):
    h = len(r) // 2
    return r.iloc[:h], r.iloc[h:]


def win(r, split):
    if split == "CAL":
        return r.loc[IS_START:IS_END], r.loc[OOS_START:]
    return halves(r)


def sh(r):
    return metrics(r)["Sharpe"]


def keep_paths(r, base, spy, split):
    ri, ro = win(r, split)
    bi, bo = win(base, split)
    si, so = win(spy, split)
    m, mb, ms = metrics(r), metrics(base), metrics(spy)
    p4a = bool(sh(ri) > sh(bi) and sh(ro) > sh(bo) and m["MaxDD"] >= mb["MaxDD"])
    fail = []
    if not sh(ri) > sh(si):
        fail.append("H1")
    if not sh(ro) > sh(so):
        fail.append("H2/OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]):
        fail.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]:
        fail.append("CAGR")
    return p4a, (",".join(fail) if fail else "-")


# ============================================================== the grid
def run_grid(panels):
    B, C = b_dials(), c_dials()
    rows = []
    for pname, (px, tr) in panels.items():
        t0 = time.time()
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        mask = rebalance_mask(px.index, "W")
        nel = b_eligible(px, tr)[mask.values].sum(axis=1).loc[start:]
        wcache: dict = {}
        base_r = backtest(px, b_weights(px, tr, dict(kind="v2", band=BAND, gross=GROSS)),
                          cost_bps=COST, freq="W")["returns"].loc[start:]
        v1_r = backtest(px, b_weights(px, tr, dict(kind="v1")),
                        cost_bps=COST, freq="W")["returns"].loc[start:]

        def emit(dialset, dial, arm, w, freq, dval, sat):
            r = backtest(px, w, cost_bps=COST, freq=freq)["returns"].loc[start:]
            m = metrics(r)
            rec = dict(panel=pname, dialset=dialset, dial=dial, arm=arm, dval=dval,
                       cost=COST, sat_share=sat,
                       FULL_CAGR=m["CAGR"], FULL_Sharpe=m["Sharpe"], FULL_MaxDD=m["MaxDD"],
                       gross=float(w.loc[start:].sum(axis=1).mean()),
                       nheld=float((w.loc[start:] > 0).sum(axis=1).mean()))
            for split in ("CAL", "MID"):
                ri, ro = win(r, split)
                mi, mo = metrics(ri), metrics(ro)
                rec[f"{split}_IS_Sharpe"] = mi["Sharpe"]
                rec[f"{split}_IS_CAGR"] = mi["CAGR"]
                rec[f"{split}_OOS_Sharpe"] = mo["Sharpe"]
                rec[f"{split}_OOS_CAGR"] = mo["CAGR"]
                rec[f"{split}_OOS_MaxDD"] = mo["MaxDD"]
                p4a, f4b = keep_paths(r, base_r, spy, split)
                rec[f"{split}_pass4a"] = p4a
                rec[f"{split}_fail4b"] = f4b
                rec[f"{split}_pass4b"] = (f4b == "-")
            rows.append(rec)

        for dial, arms in B.items():
            for aname, spec in arms:
                key = ("B", spec["kind"], spec["n"], spec["gross"], spec["max_vol"], spec["band"])
                if key not in wcache:
                    wcache[key] = b_weights(px, tr, spec)
                dv = {"n": spec["n"], "cadence": {"D": 1, "W": 5, "M": 21, "Q": 63}[spec["freq"]],
                      "gross": spec["gross"], "volgate": spec["max_vol"], "trim": spec["band"]}[dial]
                sat = float((nel <= spec["n"]).mean()) if spec["n"] else 0.0
                emit("B", dial, aname, wcache[key], spec["freq"], dv, sat)
        for dial, arms in C.items():
            for aname, spec in arms:
                key = ("C", spec["form"], spec["v"])
                if key not in wcache:
                    wcache[key] = c_weights(px, tr, spec)
                dv = {"D": 1, "W": 5, "M": 21, "Q": 63}[spec["freq"]] if dial == "cadence" else spec["v"]
                emit("C", dial, aname, wcache[key], spec["freq"], dv, np.nan)
        for nm, r in (("RULES_v2", base_r), ("RULES_v1", v1_r), ("SPY", spy)):
            m = metrics(r)
            rec = dict(panel=pname, dialset="-", dial="baseline", arm=nm, dval=np.nan,
                       cost=COST, sat_share=np.nan, FULL_CAGR=m["CAGR"],
                       FULL_Sharpe=m["Sharpe"], FULL_MaxDD=m["MaxDD"], gross=np.nan, nheld=np.nan)
            for split in ("CAL", "MID"):
                ri, ro = win(r, split)
                mi, mo = metrics(ri), metrics(ro)
                rec[f"{split}_IS_Sharpe"] = mi["Sharpe"]
                rec[f"{split}_IS_CAGR"] = mi["CAGR"]
                rec[f"{split}_OOS_Sharpe"] = mo["Sharpe"]
                rec[f"{split}_OOS_CAGR"] = mo["CAGR"]
                rec[f"{split}_OOS_MaxDD"] = mo["MaxDD"]
                rec[f"{split}_pass4a"] = False
                rec[f"{split}_fail4b"] = ""
                rec[f"{split}_pass4b"] = False
            rows.append(rec)
        P(f"  {pname:<10} {px.shape[0]}x{px.shape[1]} tradable {len(tr):>3}  {time.time() - t0:6.1f}s")
    return pd.DataFrame(rows)


# ============================================================== selectors / cells
DONOTHING = {("B", "n"): "EWall", ("B", "cadence"): "FREQ_W", ("B", "gross"): "G0.70",
             ("B", "volgate"): "V0.60", ("B", "trim"): "B0.03",
             ("C", "n"): "N20", ("C", "cadence"): "FREQ_W", ("C", "gross"): "G0.75",
             ("C", "volcap"): "V0.60", ("C", "quantile"): "Q1.00", ("C", "band"): "B0.03"}

# arm ORDER along each dial (widest/slowest last).  EWall is the widest n arm.
def arm_order(ds, dial, pool):
    if ds == "B" and dial == "n":
        o = {"FWD5": 0, "FWD10": 1, "FWD20": 2, "FWD30": 3, "FWD40": 4, "FWD60": 5, "EWall": 6}
        return sorted(pool.arm, key=lambda a: o[a])
    if dial == "cadence":
        o = {"FREQ_D": 0, "FREQ_W": 1, "FREQ_M": 2, "FREQ_Q": 3}
        return sorted(pool.arm, key=lambda a: o[a])
    return list(pool.sort_values("dval").arm)


def arm_x(ds, dial, pool, arms, spacing):
    """Positions of `arms` on x in [-1, +1] under ORD or VAL spacing."""
    k = len(arms)
    if spacing == "ORD" or k < 2:
        return np.linspace(-1.0, 1.0, k) if k > 1 else np.zeros(k)
    v = pool.set_index("arm").dval
    if ds == "B" and dial == "n":
        # EWall has no n; place it one log-step beyond the widest FWD arm.
        fw = [a for a in arms if a != "EWall"]
        lv = {a: np.log(float(v[a])) for a in fw}
        if "EWall" in arms:
            step = (max(lv.values()) - min(lv.values())) / max(len(fw) - 1, 1) if len(fw) > 1 else 1.0
            lv["EWall"] = max(lv.values()) + step
        raw = np.array([lv[a] for a in arms], float)
    elif dial in ("cadence",):
        raw = np.log(np.array([float(v[a]) for a in arms], float))
    else:
        raw = np.array([float(v[a]) for a in arms], float)
    lo, hi = raw.min(), raw.max()
    return np.zeros(k) if hi == lo else 2.0 * (raw - lo) / (hi - lo) - 1.0


def decompose(x, y):
    """z-score y across the arms, fit z = b0 + b1*x + b2*q, q = x^2 orthogonalised
    against {1, x}.  Returns (b1 level, b2 curvature, R2, z)."""
    y = np.asarray(y, float)
    sd = y.std(ddof=0)
    z = (y - y.mean()) / sd if sd > 0 else np.zeros_like(y)
    if len(x) < 3 or np.ptp(x) == 0:
        return np.nan, np.nan, np.nan, z
    X1 = np.column_stack([np.ones_like(x), x])
    q = x ** 2
    q = q - X1 @ np.linalg.lstsq(X1, q, rcond=None)[0]     # orthogonalise x^2 against {1, x}
    qsd = q.std(ddof=0)
    if qsd < 1e-12:                                        # x grid too coarse to carry curvature
        X, has_q = X1, False
    else:
        X, has_q = np.column_stack([X1, q]), True
    beta = np.linalg.lstsq(X, z, rcond=None)[0]
    fit = X @ beta
    ss = (z ** 2).sum()
    r2 = 1.0 - ((z - fit) ** 2).sum() / ss if ss > 0 else np.nan
    # report the STANDARDISED coefficients: change in z per 1 sd of the regressor, so the
    # level and curvature terms are on one scale and comparable across cells and dials.
    b1 = beta[1] * x.std(ddof=0)
    b2 = beta[2] * qsd if has_q else 0.0
    return float(b1), float(b2), float(r2), z


def cells(grid, split):
    """One row per (panel, dialset, dial): selectors' picks + the surface decomposition."""
    out, geo = [], []
    g = grid[grid.dial != "baseline"]
    for (pn, ds, dial), pool in g.groupby(["panel", "dialset", "dial"]):
        pool = pool.copy()
        if ds == "B" and dial == "n":
            pool = pool[(pool.arm == "EWall") | (pool.sat_share <= SAT_CAP)]
        if pool.empty:
            continue
        ss = pool.loc[pool[f"{split}_IS_Sharpe"].idxmax()]
        sc = pool.loc[pool[f"{split}_IS_CAGR"].idxmax()]
        dn = pool[pool.arm == DONOTHING[(ds, dial)]]
        dn = dn.iloc[0] if len(dn) else pool.iloc[0]
        same = bool(sc.arm == ss.arm)
        arms = arm_order(ds, dial, pool)
        idx = pool.set_index("arm")
        rec = dict(panel=pn, dialset=ds, dial=dial, split=split, n_arms=len(pool),
                   pick_S=ss.arm, pick_C=sc.arm, disagree=(not same),
                   dOOS_Sharpe=sc[f"{split}_OOS_Sharpe"] - ss[f"{split}_OOS_Sharpe"],
                   dOOS_CAGR_pp=(sc[f"{split}_OOS_CAGR"] - ss[f"{split}_OOS_CAGR"]) * 100.0,
                   S_OOS_Sharpe=ss[f"{split}_OOS_Sharpe"], C_OOS_Sharpe=sc[f"{split}_OOS_Sharpe"],
                   DN_OOS_Sharpe=dn[f"{split}_OOS_Sharpe"],
                   S_OOS_CAGR=ss[f"{split}_OOS_CAGR"], C_OOS_CAGR=sc[f"{split}_OOS_CAGR"],
                   DN_OOS_CAGR=dn[f"{split}_OOS_CAGR"],
                   S_OOS_MaxDD=ss[f"{split}_OOS_MaxDD"], C_OOS_MaxDD=sc[f"{split}_OOS_MaxDD"],
                   DN_OOS_MaxDD=dn[f"{split}_OOS_MaxDD"],
                   S_pass4a=bool(ss[f"{split}_pass4a"]), C_pass4a=bool(sc[f"{split}_pass4a"]),
                   S_pass4b=bool(ss[f"{split}_pass4b"]), C_pass4b=bool(sc[f"{split}_pass4b"]),
                   DN_pass4a=bool(dn[f"{split}_pass4a"]), DN_pass4b=bool(dn[f"{split}_pass4b"]),
                   gross_range=float(idx.gross.max() - idx.gross.min()),
                   nheld_ratio=float(idx.nheld.max() / max(idx.nheld.min(), 1e-9)))
        for spacing in ("ORD", "VAL"):
            x = arm_x(ds, dial, pool, arms, spacing)
            bS1, bS2, rS, zS = decompose(x, idx.loc[arms, f"{split}_IS_Sharpe"].values)
            bC1, bC2, rC, zC = decompose(x, idx.loc[arms, f"{split}_IS_CAGR"].values)
            rec[f"{spacing}_b1_S"] = bS1
            rec[f"{spacing}_b2_S"] = bS2
            rec[f"{spacing}_R2_S"] = rS
            rec[f"{spacing}_b1_C"] = bC1
            rec[f"{spacing}_b2_C"] = bC2
            rec[f"{spacing}_R2_C"] = rC
            rec[f"{spacing}_LEVELGAP"] = abs(bS1 - bC1)
            rec[f"{spacing}_CURVGAP"] = abs(bS2 - bC2)
            rec[f"{spacing}_SHAPEDIST"] = float(np.sqrt(((zS - zC) ** 2).mean()))
            for a, xx, s1, c1 in zip(arms, x, zS, zC):
                geo.append(dict(panel=pn, dialset=ds, dial=dial, split=split, spacing=spacing,
                                arm=a, x=xx, z_IS_Sharpe=s1, z_IS_CAGR=c1))
        out.append(rec)
    return pd.DataFrame(out), pd.DataFrame(geo)


# ============================================================== statistics
def pbis(y, x):
    """Point-biserial correlation between binary y and continuous x."""
    y = np.asarray(y, float)
    x = np.asarray(x, float)
    ok = np.isfinite(x)
    y, x = y[ok], x[ok]
    if len(y) < 3 or y.std() == 0 or x.std() == 0:
        return np.nan
    return float(np.corrcoef(y, x)[0, 1])


def perm_pbis(y, x, groups, seed=SEED, n=N_PERM):
    """Panel-clustered permutation: shuffle the disagreement labels WITHIN each panel,
    so a panel's overall disagreement level is held fixed under the null."""
    y = np.asarray(y, float)
    x = np.asarray(x, float)
    g = np.asarray(groups)
    ok = np.isfinite(x)
    y, x, g = y[ok], x[ok], g[ok]
    obs = pbis(y, x)
    if not np.isfinite(obs):
        return obs, np.nan
    rng = np.random.default_rng(seed)
    idx = {u: np.where(g == u)[0] for u in np.unique(g)}
    cnt = 0
    for _ in range(n):
        yp = y.copy()
        for u, ii in idx.items():
            yp[ii] = rng.permutation(y[ii])
        if abs(pbis(yp, x)) >= abs(obs) - 1e-12:
            cnt += 1
    return obs, (cnt + 1) / (n + 1)


def spearman(a, b):
    a = pd.Series(a).rank()
    b = pd.Series(b).rank()
    if a.std() == 0 or b.std() == 0:
        return np.nan
    return float(np.corrcoef(a, b)[0, 1])


def logit(X, y, iters=200):
    """Plain Newton logistic with a tiny ridge; returns coefficients (intercept first)."""
    X = np.column_stack([np.ones(len(y)), np.asarray(X, float)])
    y = np.asarray(y, float)
    b = np.zeros(X.shape[1])
    for _ in range(iters):
        p = 1.0 / (1.0 + np.exp(-X @ b))
        W = p * (1 - p) + 1e-9
        H = X.T @ (X * W[:, None]) + 1e-6 * np.eye(X.shape[1])
        step = np.linalg.solve(H, X.T @ (y - p))
        b = b + step
        if np.max(np.abs(step)) < 1e-9:
            break
    return b


def predict(b, X):
    X = np.column_stack([np.ones(len(X)), np.asarray(X, float)])
    return 1.0 / (1.0 + np.exp(-X @ b))


# ============================================================== main
def main():
    t0 = time.time()
    P(f"# {STEM}")
    P(f"# idea 494 — decompose each dial's IS Sharpe / IS CAGR surfaces into LEVEL and")
    P(f"#            CURVATURE, and test whether selector disagreement tracks the CURVATURE GAP.")
    P(f"# {COST} bps, weekly base cadence, next-day execution, long only, seed {SEED}.\n")

    P("## Panels")
    panels = build_panels()
    grid = run_grid(panels)
    grid.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    P(f"\n  grid rows (ALL grid points): {len(grid)}  -> {STEM}.arms.csv")

    cl_cal, geo_cal = cells(grid, "CAL")
    cl_mid, geo_mid = cells(grid, "MID")
    cl = pd.concat([cl_cal, cl_mid], ignore_index=True)
    geo = pd.concat([geo_cal, geo_mid], ignore_index=True)
    cl.to_csv(OUT / f"{STEM}.cells.csv", index=False)
    geo.to_csv(OUT / f"{STEM}.geometry.csv", index=False)
    P(f"  cells: {len(cl)} ({len(cl_cal)} CAL + {len(cl_mid)} MID)  -> {STEM}.cells.csv")
    P(f"  per-arm z-surfaces: {len(geo)} rows  -> {STEM}.geometry.csv")

    base = cl_cal   # headline: PROTOCOL rule 8 calendar split, 10 bps, 12 panels

    # ---------------------------------------------------------- reproduction gates
    P("\n## Reproduction gates against idea 499's published table (CAL, 10 bps, 12 panels)")
    pub = {("B", "n"): (7, 12), ("B", "trim"): (2, 12), ("B", "cadence"): (1, 12),
           ("B", "gross"): (1, 12), ("B", "volgate"): (1, 12),
           ("C", "cadence"): (6, 12), ("C", "band"): (5, 12), ("C", "volcap"): (3, 12),
           ("C", "quantile"): (2, 12), ("C", "n"): (1, 12), ("C", "gross"): (0, 12)}
    allok = True
    for (ds, dial), (k, m) in pub.items():
        s = base[(base.dialset == ds) & (base.dial == dial)].disagree
        got = (int(s.sum()), len(s))
        ok = got == (k, m)
        allok &= ok
        P(f"  {ds}/{dial:<9} reproduced {got[0]:>2}/{got[1]:<3} published {k:>2}/{m:<3} "
          f"{'PASS' if ok else 'FAIL'}")
    P(f"  GATE: {'PASS — the grid is idea 499s, to the cell' if allok else 'FAIL'}")
    P(f"  pooled: B {int(base[base.dialset=='B'].disagree.sum())}/{len(base[base.dialset=='B'])}  "
      f"C {int(base[base.dialset=='C'].disagree.sum())}/{len(base[base.dialset=='C'])}")

    # ---------------------------------------------------------- the queue's premise
    P("\n## The premise: does `n` move gross AND concentration while other dials move one thing?")
    prem = base.groupby(["dialset", "dial"]).agg(
        rate=("disagree", "mean"), cells=("disagree", "size"),
        gross_range=("gross_range", "mean"), nheld_ratio=("nheld_ratio", "mean")).sort_values(
        ["dialset", "rate"], ascending=[True, False])
    P(fmt(prem))

    # ---------------------------------------------------------- T1/T2 the decomposition
    for spacing in ("ORD", "VAL"):
        P(f"\n## Surface decomposition, {spacing} spacing (headline = ORD)")
        L, Cc, S = f"{spacing}_LEVELGAP", f"{spacing}_CURVGAP", f"{spacing}_SHAPEDIST"
        tab = base.groupby(["dialset", "dial"]).agg(
            rate=("disagree", "mean"),
            LEVELGAP=(L, "mean"), CURVGAP=(Cc, "mean"), SHAPEDIST=(S, "mean"),
            R2_S=(f"{spacing}_R2_S", "mean"), R2_C=(f"{spacing}_R2_C", "mean"),
            b2_S=(f"{spacing}_b2_S", "mean"), b2_C=(f"{spacing}_b2_C", "mean"),
            b1_S=(f"{spacing}_b1_S", "mean"), b1_C=(f"{spacing}_b1_C", "mean"),
        ).sort_values("rate", ascending=False)
        P(fmt(tab))
        P(f"  Spearman across the {len(tab)} dials: rate vs CURVGAP  {spearman(tab.rate, tab.CURVGAP):+.4f}"
          f"   rate vs LEVELGAP {spearman(tab.rate, tab.LEVELGAP):+.4f}"
          f"   rate vs SHAPEDIST {spearman(tab.rate, tab.SHAPEDIST):+.4f}")
        for nm, col in (("CURVGAP", Cc), ("LEVELGAP", L), ("SHAPEDIST", S)):
            r, p = perm_pbis(base.disagree.values, base[col].values, base.panel.values)
            P(f"  cell-level point-biserial rate~{nm:<9} r {r:+.4f}  panel-clustered perm p {p:.4f}"
              f"  (n={int(np.isfinite(base[col]).sum())})")
        # two-covariate logistic, both standardised
        d = base.dropna(subset=[L, Cc])
        Z = np.column_stack([(d[Cc] - d[Cc].mean()) / d[Cc].std(),
                             (d[L] - d[L].mean()) / d[L].std()])
        b = logit(Z, d.disagree.values.astype(float))
        P(f"  logistic disagree ~ z(CURVGAP) + z(LEVELGAP):  b_CURV {b[1]:+.4f}  b_LEVEL {b[2]:+.4f}"
          f"  (intercept {b[0]:+.4f}, n {len(d)})")

    # ---------------------------------------------------------- T3 does n survive geometry?
    P("\n## T3 — does the `n` dial's excess SURVIVE the geometry? (ORD, CAL, 10 bps)")
    L, Cc = "ORD_LEVELGAP", "ORD_CURVGAP"
    d = base.dropna(subset=[L, Cc]).copy()
    Z = np.column_stack([(d[Cc] - d[Cc].mean()) / d[Cc].std(),
                         (d[L] - d[L].mean()) / d[L].std()])
    b = logit(Z, d.disagree.values.astype(float))
    d["pred"] = predict(b, Z)
    res = d.groupby(["dialset", "dial"]).agg(observed=("disagree", "mean"),
                                             predicted=("pred", "mean"),
                                             cells=("disagree", "size"))
    res["residual"] = res.observed - res.predicted
    P(fmt(res.sort_values("residual", ascending=False)))
    bn = res.loc[("B", "n")]
    P(f"  lane B `n`: observed {bn.observed:.4f}  geometry-predicted {bn.predicted:.4f}  "
      f"residual {bn.residual:+.4f}")
    P(f"  mean |residual| over the {len(res)} dials: {res.residual.abs().mean():.4f};  "
      f"largest {res.residual.abs().max():.4f} at {res.residual.abs().idxmax()}")

    # ---------------------------------------------------------- MID robustness
    P("\n## Same three readings on the MID split (robustness, not the headline)")
    m = cl_mid.dropna(subset=[L, Cc])
    for nm, col in (("CURVGAP", Cc), ("LEVELGAP", L), ("SHAPEDIST", "ORD_SHAPEDIST")):
        r, p = perm_pbis(m.disagree.values, m[col].values, m.panel.values)
        P(f"  MID rate~{nm:<9} r {r:+.4f}  perm p {p:.4f}")

    # ---------------------------------------------------------- rule 8 abstention ladder
    P("\n## PROTOCOL rule 8 — CURVGAP as an ABSTENTION rule (IS 2009-2016 chooses, OOS 2017+ read once)")
    P("   ABSTAIN(tau): if ORD_CURVGAP > tau hold the cell's DONOTHING arm, else take S_SHARPE's pick.")
    ab = []
    for tau in TAUS:
        for scope, sel in (("ALL", base), ("B_only", base[base.dialset == "B"]),
                           ("n_only", base[base.dial == "n"])):
            s = sel.dropna(subset=[Cc]).copy()
            if not len(s):
                continue
            take = s[Cc] <= tau
            ab.append(dict(tau=tau, scope=scope, cells=len(s), took=int(take.sum()),
                           abstained=int((~take).sum()),
                           OOS_Sharpe=float(np.where(take, s.S_OOS_Sharpe, s.DN_OOS_Sharpe).mean()),
                           OOS_CAGR=float(np.where(take, s.S_OOS_CAGR, s.DN_OOS_CAGR).mean()),
                           OOS_MaxDD=float(np.where(take, s.S_OOS_MaxDD, s.DN_OOS_MaxDD).mean()),
                           pass4a=int(np.where(take, s.S_pass4a, s.DN_pass4a).sum()),
                           pass4b=int(np.where(take, s.S_pass4b, s.DN_pass4b).sum())))
    ab = pd.DataFrame(ab)
    ab.to_csv(OUT / f"{STEM}.abstain.csv", index=False)
    P(fmt(ab))

    P("\n  Fixed comparands on the same cells (ALL scope, CAL, 10 bps):")
    wf = []
    for nm, cS, cC, cD, p4a, p4b in (
            ("S_SHARPE", "S_OOS_Sharpe", "S_OOS_CAGR", "S_OOS_MaxDD", "S_pass4a", "S_pass4b"),
            ("S_CAGR", "C_OOS_Sharpe", "C_OOS_CAGR", "C_OOS_MaxDD", "C_pass4a", "C_pass4b"),
            ("DONOTHING", "DN_OOS_Sharpe", "DN_OOS_CAGR", "DN_OOS_MaxDD", "DN_pass4a", "DN_pass4b")):
        wf.append(dict(book=nm, cells=len(base), OOS_Sharpe=base[cS].mean(),
                       OOS_CAGR=base[cC].mean(), OOS_MaxDD=base[cD].mean(),
                       pass4a=int(base[p4a].sum()), pass4b=int(base[p4b].sum())))
    bl = grid[grid.dial == "baseline"]
    for nm in ("RULES_v2", "RULES_v1", "SPY"):
        bb = bl[bl.arm == nm]
        wf.append(dict(book=nm, cells=len(bb), OOS_Sharpe=bb.CAL_OOS_Sharpe.mean(),
                       OOS_CAGR=bb.CAL_OOS_CAGR.mean(), OOS_MaxDD=bb.CAL_OOS_MaxDD.mean(),
                       pass4a=-1, pass4b=-1))
    wf = pd.DataFrame(wf)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(fmt(wf))

    P("\n  Per-panel OOS Sharpe of the best abstention rung vs the comparands:")
    if len(ab):
        bestrow = ab[ab.scope == "ALL"].sort_values("OOS_Sharpe", ascending=False).iloc[0]
        P(f"    best tau on OOS Sharpe (ALL) = {bestrow.tau}  ->  {bestrow.OOS_Sharpe:.4f} "
          f"(took {int(bestrow.took)}/{int(bestrow.cells)}); "
          f"tau=inf (never abstain, = S_SHARPE) = "
          f"{ab[(ab.scope=='ALL') & (ab.tau > 1e8)].OOS_Sharpe.iloc[0]:.4f}; "
          f"tau=0 (always abstain, = DONOTHING) = "
          f"{ab[(ab.scope=='ALL') & (ab.tau == 0.0)].OOS_Sharpe.iloc[0]:.4f}")
        P("    NOTE: picking tau on OOS Sharpe is NOT a rule-8 result; it is the ORACLE"
          " headroom of the ladder and is reported only as an upper bound.")

    # ---------------------------------------------------------- KEEP paths, every arm
    P("\n## KEEP paths over EVERY arm (both paths, both splits)")
    a = grid[grid.dial != "baseline"]
    for split in ("CAL", "MID"):
        P(f"  {split}: 4a {int(a[f'{split}_pass4a'].sum())}/{len(a)}   "
          f"4b {int(a[f'{split}_pass4b'].sum())}/{len(a)}")
    k4b = a[a.CAL_pass4b]
    P(f"\n  CAL 4b passers ({len(k4b)}), by (dialset, dial) and by panel:")
    if len(k4b):
        P(fmt(k4b.groupby(["dialset", "dial"]).size().rename("n").to_frame()))
        P(fmt(k4b.groupby(["panel"]).size().rename("n").to_frame()))
    k4a = a[a.CAL_pass4a]
    P(f"\n  CAL 4a passers ({len(k4a)}):")
    if len(k4a):
        P(fmt(k4a[["panel", "dialset", "dial", "arm", "FULL_CAGR", "FULL_Sharpe",
                   "FULL_MaxDD", "CAL_IS_Sharpe", "CAL_OOS_Sharpe"]]))

    P(f"\nDone in {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_log) + "\n")


if __name__ == "__main__":
    main()
