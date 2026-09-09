#!/usr/bin/env python3
"""Idea 499 — is the n-vs-cadence disagreement ordering PANEL-driven or DIAL-driven?
   (cloud, 2026-09-09)

QUEUE ASK
    Idea 270's two independent same-day runs put the S_CAGR/S_SHARPE selector disagreement
    on DIFFERENT dials.  Lane B (`..._B.py`): n 7/12 cells, cadence 1/12.  Cloud
    (`..._cloud.py`): cadence 4/6, n 2/6.  The two runs differ in FOUR ways at once —
    the arm parameterisation of each dial, the panel set, the IS/OOS split convention and
    the cost rungs — so nothing in the record says which of them moved the ordering.
    Run BOTH dial sets on ONE shared panel set and report which factor moves it.

DESIGN
    The two factors the queue names, crossed:
      dialset   in {B, CLOUD}   -- each parent's dial families reproduced VERBATIM from its
                                   own script (arm lists, book forms, and for `n` lane B's
                                   saturation cap and EWall arm).
      panelset  in {B12, CLOUD3}-- CLOUD3 = {U56, B136, SMALL439} is a strict SUBSET of
                                   B12 = those three + BSTK100 + lane B's 8 pre-registered
                                   seeded sub-panels, so the whole grid is computed once on
                                   B12 and simply re-read on the CLOUD3 rows.  That is what
                                   "one shared panel set" means here: the same 12 panels
                                   carry both dial sets, and the 3-panel reading is a subset
                                   of the same numbers, never a separate run.
    Outcome = the ORDERING statistic the queue asks about:
        Delta = disagreement_rate(n dial) - disagreement_rate(cadence dial),
    where a cell (panel, dial) DISAGREES iff argmax IS_Sharpe and argmax IS_CAGR pick a
    different arm -- both parents' own definition, arm identity, no tie band.
    Delta > 0 is lane B's ordering, Delta < 0 is cloud's.

    Two nuisance conventions the parents also differ on are read as extra REPORTING axes,
    not as tuned parameters (the returns are computed once; only the window/rung changes):
      split   CAL (PROTOCOL rule 8: IS 2009-01-01..2016-12-31 chooses, OOS 2017-01-01+
              read once -- lane B's convention and the protocol's) vs MID (sample midpoint
              -- the cloud parent's).  CAL is the headline everywhere.
      cost    10 bps headline; 25 bps computed for the CLOUD dial set on CLOUD3 only, so
              the cloud parent's own 36-cell denominator can be reproduced exactly.

    REPRODUCTION GATES, computed before anything new is read:
      G1  CLOUD dial set + CLOUD3 + MID split + both rungs must return the cloud parent's
          published counts (11/36 disagreements; cadence 4/6, volcap 3/6, band 2/6, n 2/6,
          gross 0/6, quantile 0/6).
      G2  B dial set + B12 + CAL split + 10 bps must return lane B's published counts
          (12/60; n 7/12, trim 2/12, cadence 1/12, gross 1/12, volgate 1/12).

TUNED PARAMETERS (PROTOCOL rule 4: max 2)
    1. the dial value inside a cell -- chosen by each selector on IS only, never on OOS.
    2. none.  dialset / panelset / split / cost are ENUMERATED axes; every grid point is
       written to .arms.csv and every cell to .cells.csv.

CONVENTIONS
    10 bps per unit turnover (25 bps rung where stated), weights decided at close t and
    applied at t+1 (engine), long only, no leverage, weekly base cadence except on the
    cadence dial, which is the treatment.  4a is judged against the LIVE RULES v2 book on
    the same panel, 4b against SPY per PROTOCOL rule 4b, for EVERY arm.
    SURVIVORSHIP: B136 / BSTK100 are current constituents of a current screen and SMALL439
    is the 483-name sub-$2B panel with the 44 tickers whose `max_1d_move >= 1.0` dropped
    first (data/small_meta.csv, data/SMALL_PANEL_README.md).  The 8 seeded sub-panels
    inherit that bias.  No network is used.

Outputs: .arms.csv .cells.csv .factorial.csv .walkforward.csv .console.txt .result.md
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
from baseline import load_universe, score, band_state, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask                                       # noqa: E402

STEM = Path(__file__).name[:-3]
OUT = REPO / "research" / "backtests"

GROSS, BAND, MAX_VOL, W_FIXED = 0.75, 0.03, 0.60, 0.15
IS_START, IS_END, OOS_START = "2009-01-01", "2016-12-31", "2017-01-01"
SAT_CAP = 0.25
N_PERM = 20000
SEED = 499

_log: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _log.append(s)


# ============================================================== panels (lane B's, verbatim)
def build_panels():
    U = json.loads((REPO / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    etf36 = [t for t in U["broad"] + U["sectors"] + U["bonds_fx_commod"] if t not in crypto]
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])          # ALWAYS dropped first
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
    for seed in range(8):                                           # lane B's 8 seeded panels
        rng = np.random.default_rng(1000 + seed)
        pool, k, src = (b_stk, 60, px136) if seed < 4 else (s_stk, 120, pxs)
        pick = sorted(rng.choice(np.array(sorted(pool)), size=k, replace=False).tolist())
        panels[f"S{seed}_{'B' if seed < 4 else 'M'}{k}"] = sub(src, pick, tradable=pick)
    return panels


CLOUD3 = ["U56", "B136", "SMALL439"]


# ============================================================== book forms
def _ew(px, mask, gross, tradable):
    e = mask.astype(float).where(px.notna(), 0.0)
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        e[drop] = 0.0
    return gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


# ---- lane B's forms (from ..._B.py: make_weights / eligible_mask / dial_arms) -------------
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


# ---- the cloud parent's forms (from ..._cloud.py: w_topn / w_band / ... ) ------------------
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
    """(IS returns, OOS returns) under the named split convention."""
    if split == "CAL":
        return r.loc[IS_START:IS_END], r.loc[OOS_START:]
    return halves(r)


def sh(r):
    return metrics(r)["Sharpe"]


def keep_paths(r, base, spy, split):
    """PROTOCOL 4a and 4b for one arm, both KEEP paths, under one split convention."""
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
        costs = [10, 25] if pname in CLOUD3 else [10]
        wcache: dict = {}
        base_r, v1_r = {}, {}
        for cost in costs:
            base_r[cost] = backtest(px, b_weights(px, tr, dict(kind="v2", band=BAND, gross=GROSS)),
                                    cost_bps=cost, freq="W")["returns"].loc[start:]
            v1_r[cost] = backtest(px, b_weights(px, tr, dict(kind="v1")),
                                  cost_bps=cost, freq="W")["returns"].loc[start:]

        def emit(dialset, dial, arm, w, freq, cost, dval, sat):
            r = backtest(px, w, cost_bps=cost, freq=freq)["returns"].loc[start:]
            m = metrics(r)
            rec = dict(panel=pname, dialset=dialset, dial=dial, arm=arm, dval=dval,
                       cost=cost, sat_share=sat,
                       FULL_CAGR=m["CAGR"], FULL_Sharpe=m["Sharpe"], FULL_MaxDD=m["MaxDD"],
                       gross=float(w.loc[start:].sum(axis=1).mean()))
            for split in ("CAL", "MID"):
                ri, ro = win(r, split)
                mi, mo = metrics(ri), metrics(ro)
                rec[f"{split}_IS_Sharpe"] = mi["Sharpe"]
                rec[f"{split}_IS_CAGR"] = mi["CAGR"]
                rec[f"{split}_OOS_Sharpe"] = mo["Sharpe"]
                rec[f"{split}_OOS_CAGR"] = mo["CAGR"]
                rec[f"{split}_OOS_MaxDD"] = mo["MaxDD"]
                p4a, f4b = keep_paths(r, base_r[cost], spy, split)
                rec[f"{split}_pass4a"] = p4a
                rec[f"{split}_fail4b"] = f4b
                rec[f"{split}_pass4b"] = (f4b == "-")
            rows.append(rec)

        for cost in costs:
            # ---- lane B's dial set
            for dial, arms in B.items():
                for aname, spec in arms:
                    key = ("B", spec["kind"], spec["n"], spec["gross"], spec["max_vol"], spec["band"])
                    if key not in wcache:
                        wcache[key] = b_weights(px, tr, spec)
                    dv = {"n": spec["n"], "cadence": {"D": 1, "W": 5, "M": 21, "Q": 63}[spec["freq"]],
                          "gross": spec["gross"], "volgate": spec["max_vol"], "trim": spec["band"]}[dial]
                    sat = float((nel <= spec["n"]).mean()) if spec["n"] else 0.0
                    emit("B", dial, aname, wcache[key], spec["freq"], cost, dv, sat)
            # ---- the cloud parent's dial set
            for dial, arms in C.items():
                for aname, spec in arms:
                    key = ("C", spec["form"], spec["v"])
                    if key not in wcache:
                        wcache[key] = c_weights(px, tr, spec)
                    dv = {"D": 1, "W": 5, "M": 21, "Q": 63}[spec["freq"]] if dial == "cadence" else spec["v"]
                    emit("C", dial, aname, wcache[key], spec["freq"], cost, dv, np.nan)
            # ---- comparands
            for nm, r in (("RULES_v2", base_r[cost]), ("RULES_v1", v1_r[cost]), ("SPY", spy)):
                m = metrics(r)
                rec = dict(panel=pname, dialset="-", dial="baseline", arm=nm, dval=np.nan,
                           cost=cost, sat_share=np.nan, FULL_CAGR=m["CAGR"],
                           FULL_Sharpe=m["Sharpe"], FULL_MaxDD=m["MaxDD"], gross=np.nan)
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
        P(f"  {pname:<10} {px.shape[0]}x{px.shape[1]} tradable {len(tr):>3}  "
          f"rungs {costs}  {time.time() - t0:6.1f}s")
    return pd.DataFrame(rows)


# ============================================================== selectors / cells
DONOTHING = {("B", "n"): "EWall", ("B", "cadence"): "FREQ_W", ("B", "gross"): "G0.70",
             ("B", "volgate"): "V0.60", ("B", "trim"): "B0.03",
             ("C", "n"): "N20", ("C", "cadence"): "FREQ_W", ("C", "gross"): "G0.75",
             ("C", "volcap"): "V0.60", ("C", "quantile"): "Q1.00", ("C", "band"): "B0.03"}


def cells(grid, split):
    """One row per (panel, dialset, dial, cost): the two selectors' picks and OOS deltas."""
    out = []
    g = grid[grid.dial != "baseline"]
    for (pn, ds, dial, cost), pool in g.groupby(["panel", "dialset", "dial", "cost"]):
        pool = pool.copy()
        if ds == "B" and dial == "n":              # lane B's saturation cap, verbatim
            pool = pool[(pool.arm == "EWall") | (pool.sat_share <= SAT_CAP)]
        if pool.empty:
            continue
        ss = pool.loc[pool[f"{split}_IS_Sharpe"].idxmax()]
        sc = pool.loc[pool[f"{split}_IS_CAGR"].idxmax()]
        dn = pool[pool.arm == DONOTHING[(ds, dial)]]
        dn = dn.iloc[0] if len(dn) else pool.iloc[0]
        dS = sc[f"{split}_OOS_Sharpe"] - ss[f"{split}_OOS_Sharpe"]
        dC = (sc[f"{split}_OOS_CAGR"] - ss[f"{split}_OOS_CAGR"]) * 100.0
        same = bool(sc.arm == ss.arm)
        out.append(dict(panel=pn, dialset=ds, dial=dial, cost=cost, split=split,
                        n_arms=len(pool), pick_S=ss.arm, pick_C=sc.arm,
                        disagree=(not same),
                        dOOS_Sharpe=dS, dOOS_CAGR_pp=dC,
                        xr=(np.nan if (same or dS >= 0) else dC / (-dS)),
                        freelunch=bool((not same) and dS > 0 and dC > 0),
                        both_worse=bool((not same) and dS < 0 and dC < 0),
                        S_OOS_Sharpe=ss[f"{split}_OOS_Sharpe"], C_OOS_Sharpe=sc[f"{split}_OOS_Sharpe"],
                        DN_OOS_Sharpe=dn[f"{split}_OOS_Sharpe"],
                        S_OOS_CAGR=ss[f"{split}_OOS_CAGR"], C_OOS_CAGR=sc[f"{split}_OOS_CAGR"],
                        DN_OOS_CAGR=dn[f"{split}_OOS_CAGR"],
                        S_OOS_MaxDD=ss[f"{split}_OOS_MaxDD"], C_OOS_MaxDD=sc[f"{split}_OOS_MaxDD"],
                        S_pass4b=bool(ss[f"{split}_pass4b"]), C_pass4b=bool(sc[f"{split}_pass4b"]),
                        S_pass4a=bool(ss[f"{split}_pass4a"]), C_pass4a=bool(sc[f"{split}_pass4a"])))
    return pd.DataFrame(out)


def rate_table(cl):
    t = cl.groupby(["dialset", "dial"]).disagree.agg(["sum", "count"])
    t["rate"] = t["sum"] / t["count"]
    return t.sort_values(["dialset", "rate"], ascending=[True, False])


def delta(cl, ds):
    """Delta = rate(n) - rate(cadence) inside one dial set."""
    s = cl[cl.dialset == ds]
    a = s[s.dial == "n"].disagree
    b = s[s.dial == "cadence"].disagree
    if not len(a) or not len(b):
        return np.nan, (0, 0), (0, 0)
    return float(a.mean() - b.mean()), (int(a.sum()), len(a)), (int(b.sum()), len(b))


def mcnemar(cl, dial):
    """Paired across panels: same panel, same dial NAME, the two parameterisations.
    Returns (b, c, exact two-sided binomial p) for the discordant pairs."""
    s = cl[(cl.dial == dial)].set_index(["panel", "dialset"]).disagree
    pans = sorted({p for p, _ in s.index})
    b = c = 0
    for p in pans:
        try:
            xb, xc = bool(s.loc[(p, "B")]), bool(s.loc[(p, "C")])
        except KeyError:
            continue
        if xb and not xc:
            b += 1
        elif xc and not xb:
            c += 1
    n = b + c
    if n == 0:
        return b, c, 1.0
    from math import comb
    k = min(b, c)
    p = min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)
    return b, c, p


def perm_delta(cl, seed=SEED, n=N_PERM):
    """Permutation test of 'the dial-set label does not move Delta'.  Within each
    (panel, dial) pair the two dial-set labels are exchangeable under the null; the
    statistic is |Delta_B - Delta_C|."""
    d = cl[cl.dial.isin(["n", "cadence"])][["panel", "dial", "dialset", "disagree"]].copy()
    piv = d.pivot_table(index=["panel", "dial"], columns="dialset", values="disagree")
    piv = piv.dropna()
    if piv.empty:
        return np.nan, np.nan

    def stat(mat):
        f = pd.DataFrame(mat, index=piv.index, columns=["B", "C"]).reset_index()
        out = {}
        for ds in ("B", "C"):
            g = f.groupby("dial")[ds].mean()
            out[ds] = g.get("n", np.nan) - g.get("cadence", np.nan)
        return abs(out["B"] - out["C"])

    obs = stat(piv.values.astype(float))
    rng = np.random.default_rng(seed)
    v = piv.values.astype(float)
    hits = 0
    for _ in range(n):
        flip = rng.random(len(v)) < 0.5
        m = v.copy()
        m[flip] = m[flip][:, ::-1]
        if stat(m) >= obs - 1e-12:
            hits += 1
    return obs, (hits + 1) / (n + 1)


# ============================================================== main
def main():
    t0 = time.time()
    P(f"# {STEM}")
    P("Idea 499 — run BOTH idea-270 dial sets on ONE shared panel set.\n")
    panels = build_panels()
    P(f"Panels ({len(panels)}): " + ", ".join(panels))
    P(f"CLOUD3 subset: {CLOUD3}\n")
    P("## Grid")
    grid = run_grid(panels)
    grid.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    P(f"\narms.csv rows {len(grid)} (all grid points), {time.time() - t0:.0f}s\n")

    cl = pd.concat([cells(grid, "CAL"), cells(grid, "MID")], ignore_index=True)
    cl.to_csv(OUT / f"{STEM}.cells.csv", index=False)

    # ---------------------------------------------------------- reproduction gates
    P("## Reproduction gates")
    g1 = cl[(cl.split == "MID") & (cl.dialset == "C") & (cl.panel.isin(CLOUD3))]
    r1 = g1.groupby("dial").disagree.agg(["sum", "count"])
    P("G1  cloud parent (CLOUD dials, CLOUD3, MID split, 10+25 bps): "
      f"{int(g1.disagree.sum())}/{len(g1)} disagreements   published 11/36")
    P(fmt(r1) + "   published: cadence 4/6, volcap 3/6, band 2/6, n 2/6, gross 0/6, quantile 0/6")
    g2 = cl[(cl.split == "CAL") & (cl.dialset == "B") & (cl.cost == 10)]
    r2 = g2.groupby("dial").disagree.agg(["sum", "count"])
    P("\nG2  lane B (B dials, B12, CAL split, 10 bps): "
      f"{int(g2.disagree.sum())}/{len(g2)} disagreements   published 12/60")
    P(fmt(r2) + "   published: n 7/12, trim 2/12, cadence 1/12, gross 1/12, volgate 1/12")

    # ---------------------------------------------------------- the 2x2 the queue asks for
    P("\n## The queue's 2x2 — Delta = rate(n) - rate(cadence), 10 bps")
    fac = []
    for split in ("CAL", "MID"):
        for ps, plist in (("B12", list(panels)), ("CLOUD3", CLOUD3)):
            for ds in ("B", "C"):
                sub = cl[(cl.split == split) & (cl.cost == 10) & (cl.dialset == ds)
                         & (cl.panel.isin(plist))]
                d, nn, cc = delta(sub, ds)
                fac.append(dict(split=split, panelset=ps, dialset=ds, Delta=d,
                                n_dis=nn[0], n_cells=nn[1], cad_dis=cc[0], cad_cells=cc[1],
                                ordering=("B-like (n>cadence)" if d > 0 else
                                          "cloud-like (cadence>n)" if d < 0 else "tied"),
                                pooled_dis=int(sub.disagree.sum()), pooled_cells=len(sub)))
    fac = pd.DataFrame(fac)
    fac.to_csv(OUT / f"{STEM}.factorial.csv", index=False)
    P(fmt(fac))

    P("\n### Per-dial disagreement rates, 10 bps, CAL split, all 12 shared panels")
    P(fmt(rate_table(cl[(cl.split == "CAL") & (cl.cost == 10)])))
    P("\n### Same, MID split")
    P(fmt(rate_table(cl[(cl.split == "MID") & (cl.cost == 10)])))

    # ---------------------------------------------------------- attribution tests
    P("\n## Which factor moves the ordering?")
    base = cl[(cl.split == "CAL") & (cl.cost == 10)]
    for dial in ("n", "cadence"):
        b, c, p = mcnemar(base, dial)
        P(f"  McNemar over the 12 shared panels, dial `{dial}`: B-only {b}, CLOUD-only {c}, "
          f"exact two-sided p {p:.4f}")
    obs, p = perm_delta(base)
    P(f"  Permutation (dial-set labels exchangeable within panel x dial): "
      f"|Delta_B - Delta_C| = {obs:.4f}, p {p:.4f}  [{N_PERM} draws, seed {SEED}]")

    # panel-set effect, dial set held fixed
    P("\n  Panel-set effect with the dial set HELD FIXED (10 bps, CAL):")
    for ds in ("B", "C"):
        d12, n12, c12 = delta(base[base.dialset == ds], ds)
        d3, n3, c3 = delta(base[(base.dialset == ds) & (base.panel.isin(CLOUD3))], ds)
        P(f"    dialset {ds}: Delta(B12) {d12:+.4f} [n {n12[0]}/{n12[1]}, cad {c12[0]}/{c12[1]}]"
          f"   Delta(CLOUD3) {d3:+.4f} [n {n3[0]}/{n3[1]}, cad {c3[0]}/{c3[1]}]")
    P("\n  Dial-set effect with the panel set HELD FIXED (10 bps, CAL):")
    for ps, plist in (("B12", list(panels)), ("CLOUD3", CLOUD3)):
        s = base[base.panel.isin(plist)]
        db, nb, cb = delta(s, "B")
        dc, nc, cc = delta(s, "C")
        P(f"    panelset {ps:<7}: Delta(B dials) {db:+.4f} [n {nb[0]}/{nb[1]}, cad {cb[0]}/{cb[1]}]"
          f"   Delta(CLOUD dials) {dc:+.4f} [n {nc[0]}/{nc[1]}, cad {cc[0]}/{cc[1]}]")
    P("\n  Split-convention effect, dials and panels HELD FIXED (10 bps, 12 panels):")
    for ds in ("B", "C"):
        for split in ("CAL", "MID"):
            s = cl[(cl.split == split) & (cl.cost == 10) & (cl.dialset == ds)]
            d, nn, cc = delta(s, ds)
            P(f"    dialset {ds} split {split}: Delta {d:+.4f} [n {nn[0]}/{nn[1]}, "
              f"cad {cc[0]}/{cc[1]}]")
    P("\n  Cost-rung effect, dials/panels/split HELD FIXED (CLOUD3 only, CAL):")
    for ds in ("B", "C"):
        for cost in (10, 25):
            s = cl[(cl.split == "CAL") & (cl.cost == cost) & (cl.dialset == ds)
                   & (cl.panel.isin(CLOUD3))]
            d, nn, cc = delta(s, ds)
            P(f"    dialset {ds} cost {cost:>2} bps: Delta {d:+.4f} [n {nn[0]}/{nn[1]}, "
              f"cad {cc[0]}/{cc[1]}]")

    # ---------------------------------------------------------- rule 8 / KEEP paths
    P("\n## PROTOCOL rule 8 walk-forward (CAL: chosen on 2009-2016, read once on 2017+)")
    wf = []
    for (ds, dial), g in base.groupby(["dialset", "dial"]):
        for sel, cS, cC in (("S_SHARPE", "S_OOS_Sharpe", "S_OOS_CAGR"),
                            ("S_CAGR", "C_OOS_Sharpe", "C_OOS_CAGR"),
                            ("DONOTHING", "DN_OOS_Sharpe", "DN_OOS_CAGR")):
            wf.append(dict(dialset=ds, dial=dial, selector=sel, cells=len(g),
                           OOS_Sharpe=g[cS].mean(), OOS_CAGR=g[cC].mean()))
    wf = pd.DataFrame(wf)
    bl = grid[(grid.dial == "baseline") & (grid.cost == 10)]
    for nm in ("RULES_v2", "RULES_v1", "SPY"):
        b = bl[bl.arm == nm]
        wf = pd.concat([wf, pd.DataFrame([dict(dialset="-", dial="comparand", selector=nm,
                                               cells=len(b), OOS_Sharpe=b.CAL_OOS_Sharpe.mean(),
                                               OOS_CAGR=b.CAL_OOS_CAGR.mean())])],
                       ignore_index=True)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(fmt(wf))

    P("\n  Mean over ALL 10-bps CAL cells (both dial sets, 12 panels):")
    P(f"    S_SHARPE  OOS Sharpe {base.S_OOS_Sharpe.mean():.4f}  OOS CAGR {base.S_OOS_CAGR.mean():.2%}")
    P(f"    S_CAGR    OOS Sharpe {base.C_OOS_Sharpe.mean():.4f}  OOS CAGR {base.C_OOS_CAGR.mean():.2%}")
    P(f"    DONOTHING OOS Sharpe {base.DN_OOS_Sharpe.mean():.4f}  OOS CAGR {base.DN_OOS_CAGR.mean():.2%}")
    P(f"    S_SHARPE beats DONOTHING in {int((base.S_OOS_Sharpe > base.DN_OOS_Sharpe).sum())}"
      f"/{len(base)} cells; S_CAGR in "
      f"{int((base.C_OOS_Sharpe > base.DN_OOS_Sharpe).sum())}/{len(base)}")

    P("\n## KEEP paths over every arm (both paths, both splits, all rungs)")
    a = grid[grid.dial != "baseline"]
    for split in ("CAL", "MID"):
        P(f"  {split}: 4a {int(a[f'{split}_pass4a'].sum())}/{len(a)}   "
          f"4b {int(a[f'{split}_pass4b'].sum())}/{len(a)}")
    k4b = a[a.CAL_pass4b & (a.cost == 10)]
    P(f"\n  CAL 4b passers at 10 bps ({len(k4b)}), by (dialset, dial):")
    if len(k4b):
        P(fmt(k4b.groupby(["dialset", "dial"]).size().rename("n").to_frame()))
        P(fmt(k4b.groupby(["panel"]).size().rename("n").to_frame()))
    k4a = a[a.CAL_pass4a]
    P(f"\n  CAL 4a passers ({len(k4a)}):")
    if len(k4a):
        P(fmt(k4a[["panel", "dialset", "dial", "arm", "cost", "FULL_CAGR", "FULL_Sharpe",
                   "FULL_MaxDD", "CAL_IS_Sharpe", "CAL_OOS_Sharpe"]]))

    P(f"\nDone in {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_log) + "\n")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


if __name__ == "__main__":
    main()
