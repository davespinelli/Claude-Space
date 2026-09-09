#!/usr/bin/env python3
"""Idea 270 — is-S_CAGR-vs-S_SHARPE-a-general-selector-pair?  (lane B, 2026-09-09)

QUEUE ASK
    Idea 259 found that on the *n dial* the two in-sample selectors (argmax IS Sharpe vs
    argmax IS CAGR) pick a DIFFERENT arm in 3 of 4 panels, and that switching the selection
    metric buys +2.53 pp/yr of OOS CAGR for -0.0254 of OOS Sharpe.  Run the same selector
    pair over the record's OTHER swept dials (cadence, gross, vol gate, eligibility trim)
    wherever the parent committed a grid CSV with IS_CAGR, and report whether the
    +CAGR/-Sharpe exchange rate is a CONSTANT or a DIAL-SPECIFIC one.  Max 2 params.

DESIGN
    GATE   Reproduce idea 259's rule-8 n-dial numbers verbatim (same panels, same arms,
           same saturation cap, same pooling) before anything new is computed.
    LEG A  Fresh controlled grid.  FIVE dials x TWELVE panels = 60 cells, every arm
           reported.  Within each cell exactly ONE parameter is chosen, and it is chosen
           on IS 2009-2016 only; OOS 2017+ is read once.  Dials:
              n        FWD top-n ranked book, n in {5,10,20,30,40,60} + EWall  (259's dial)
              cadence  EWall book at freq in {D,W,M,Q}
              gross    EWall book at gross in {0.25,0.40,0.55,0.70,0.85,1.00}
              volgate  EWall book, eligibility vol cap in {0.30,...,1.00}
              trim     RULES-v2-form band book, band in {0.00,0.01,0.02,0.03,0.05,0.08}
           Exchange rate xr = dOOS_CAGR (pp) / (-dOOS_Sharpe), S_CAGR minus S_SHARPE.
           Constancy is tested by PERMUTATION (labels shuffled across cells), not by an
           F distribution, because the per-cell xr is heavy-tailed by construction.
    LEG B  The queue's literal ask: census every committed CSV in research/backtests/ that
           carries IS_Sharpe, IS_CAGR, OOS_Sharpe and OOS_CAGR, reconstruct each swept
           dial as a menu (group by all other label columns), run the same selector pair,
           and report the exchange rate by dial family across the record.

TUNED PARAMETERS (max 2, per PROTOCOL rule 4)
    1. the dial value inside a cell  -- chosen by the selector on IS only, never on OOS.
    2. none.  The panel and dial axes are ENUMERATED and every point is reported; they are
       reporting axes, not tuned parameters.

CONVENTIONS
    10 bps per unit turnover, weekly cadence (except the cadence dial itself, which is the
    treatment), weights decided at close t and applied at t+1 (engine).  Long only, no
    leverage.  4a is judged against the LIVE RULES v2 book on the same panel (idea 482:
    every pre-2026-09-06 4a count was against the superseded v1); the v1 column is carried
    for continuity.  4b is judged against SPY per PROTOCOL rule 4b.
    SURVIVORSHIP: B136/BSTK100 are current constituents, SMALL439 is a current screen
    (data/SMALL_PANEL_README.md).  Seeded sub-panels inherit that bias.

Outputs: .grid.csv .picks.csv .xr.csv .census.csv .walkforward.csv .console.txt
"""
from __future__ import annotations
import json, sys, warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))
from baseline import load_universe, score, band_state          # noqa: E402
from engine import backtest, metrics, rebalance_mask           # noqa: E402

COST_BPS = 10
FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
W_FIXED = 0.15
BAND = 0.03
NS = [5, 10, 20, 30, 40, 60]
IS_START, IS_END, OOS_START = "2009-01-01", "2016-12-31", "2017-01-01"
SAT_CAP = 0.25
EPS_S, EPS_C = 0.005, 0.0005          # idea 259's tie bands: 0.005 Sharpe, 5 bps CAGR
N_PERM = 20000
RNG_SEED = 270

SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 600)

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


def tstat(x):
    """One-sample t on a vector (no scipy).  Returns (mean, t, n)."""
    x = np.asarray([v for v in x if np.isfinite(v)], dtype=float)
    n = len(x)
    if n < 2:
        return (float(x[0]) if n else np.nan), np.nan, n
    sd = x.std(ddof=1)
    return x.mean(), (x.mean() / (sd / np.sqrt(n)) if sd > 0 else np.nan), n


# ============================================================== panels
def build_panels():
    """4 named panels (idea 259's exact four) + 8 pre-registered seeded sub-panels."""
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
    named = list(panels)
    # 8 seeded sub-panels, pre-registered: seeds 0-3 draw k=60 from BSTK100,
    # seeds 4-7 draw k=120 from SMALL439.  Purely for cell count / power.
    for seed in range(8):
        rng = np.random.default_rng(1000 + seed)
        if seed < 4:
            pool, k, src = b_stk, 60, px136
        else:
            pool, k, src = s_stk, 120, pxs
        pick = sorted(rng.choice(np.array(sorted(pool)), size=k, replace=False).tolist())
        panels[f"S{seed}_{'B' if seed < 4 else 'M'}{k}"] = sub(src, pick, tradable=pick)
    return panels, named


# ============================================================== books
def eligible_mask(px, tradable, max_vol=MAX_VOL):
    _, above, vol20 = score(px)
    m = (above & (vol20 < max_vol)).copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m[drop] = False
    return m


def make_weights(px, tradable, spec):
    """spec = dict(kind, n, gross, max_vol, band).  Cadence lives in the backtest call."""
    kind = spec["kind"]
    if kind == "v1":                                        # RULES v1 (previous book)
        s = score(px, vol_scale=True)[0]
        elig = eligible_mask(px, tradable, MAX_VOL)
        rank = s.where(elig).rank(axis=1, ascending=False)
        return (rank <= 5).astype(float) * W_FIXED
    if kind in ("v2", "BAND"):                              # RULES v2 form: MA band, de-gross
        b = spec.get("band", BAND)
        st = band_state(px, b)
        e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
        drop = [c for c in px.columns if c not in tradable]
        if drop:
            e[drop] = 0.0
        g = spec.get("gross", GROSS)
        ew = g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        return ew.where(st, 0.0)
    elig = eligible_mask(px, tradable, spec.get("max_vol", MAX_VOL))
    if kind == "EW":
        sel = elig.astype(float)
    elif kind == "FWD":
        key = score(px, vol_scale=False)[0]
        rank = key.where(elig).rank(axis=1, ascending=False)
        sel = (rank <= spec["n"]).astype(float)
    else:
        raise ValueError(kind)
    held = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(held, axis=0).mul(spec.get("gross", GROSS)).fillna(0.0)


def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def pass4a(r, base):
    """Sharpe > live book in BOTH halves AND MaxDD no worse."""
    h1, h2 = half_sharpes(r)
    b1, b2 = half_sharpes(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def fail4b(r, spy, r_oos, spy_oos):
    h1, h2 = half_sharpes(r)
    s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(r_oos)["Sharpe"] > metrics(spy_oos)["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


# ============================================================== the five dials
def dial_arms():
    """Every dial is a ONE-dimensional family off the same EWall(G) base book."""
    base = dict(kind="EW", n=None, gross=GROSS, max_vol=MAX_VOL, band=None, freq=FREQ)
    arms = {"n": [], "cadence": [], "gross": [], "volgate": [], "trim": []}
    arms["n"].append(("EWall", dict(base)))
    for n in NS:
        arms["n"].append((f"FWD{n}", dict(base, kind="FWD", n=n)))
    for f in ["D", "W", "M", "Q"]:
        arms["cadence"].append((f"FREQ_{f}", dict(base, freq=f)))
    for g in [0.25, 0.40, 0.55, 0.70, 0.85, 1.00]:
        arms["gross"].append((f"G{g:.2f}", dict(base, gross=g)))
    for v in [0.30, 0.40, 0.50, 0.60, 0.80, 1.00]:
        arms["volgate"].append((f"V{v:.2f}", dict(base, max_vol=v)))
    for b in [0.00, 0.01, 0.02, 0.03, 0.05, 0.08]:
        arms["trim"].append((f"B{b:.2f}", dict(base, kind="BAND", band=b)))
    return arms


def run_grid(panels):
    """Every (panel, dial, arm) point.  Cached by weight-spec so shared arms cost once."""
    arms = dial_arms()
    rows, series = [], {}
    for pname, (px, tr) in panels.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        spy_oos = spy.loc[OOS_START:]
        m = rebalance_mask(px.index, FREQ)
        nel = eligible_mask(px, tr)[m.values].sum(axis=1).loc[start:]
        wcache, rcache = {}, {}

        def run(spec):
            key = (spec["kind"], spec["n"], spec["gross"], spec["max_vol"],
                   spec["band"], spec["freq"])
            if key in rcache:
                return rcache[key]
            wkey = key[:5]
            if wkey not in wcache:
                wcache[wkey] = make_weights(px, tr, spec)
            res = backtest(px, wcache[wkey], cost_bps=COST_BPS, freq=spec["freq"])
            r = res["returns"].loc[start:]
            turn = float(res["turnover"].loc[start:].sum() / (len(r) / 252))
            gr = float(wcache[wkey].loc[start:].sum(axis=1).mean())
            rcache[key] = (r, turn, gr)
            return rcache[key]

        # panel baselines: LIVE RULES v2 (for 4a) and RULES v1 (continuity)
        bl = {}
        for bn, sp in (("v2", dict(kind="v2", n=None, gross=GROSS, max_vol=MAX_VOL,
                                   band=BAND, freq=FREQ)),
                       ("v1", dict(kind="v1", n=None, gross=GROSS, max_vol=MAX_VOL,
                                   band=None, freq=FREQ))):
            r, turn, gr = run(sp)
            bl[bn] = r
            mm, mo = metrics(r), metrics(r.loc[OOS_START:])
            h1, h2 = half_sharpes(r)
            rows.append(dict(panel=pname, dial="baseline", arm=f"RULES_{bn}", dval=np.nan,
                             CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                             Vol=mm["Vol"], H1=h1, H2=h2,
                             IS_Sharpe=metrics(r.loc[IS_START:IS_END])["Sharpe"],
                             IS_CAGR=metrics(r.loc[IS_START:IS_END])["CAGR"],
                             OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"],
                             OOS_MaxDD=mo["MaxDD"], turn=turn, gross=gr, sat_share=np.nan,
                             p4a=np.nan, f4b="", p4b=np.nan))
        sm, smo = metrics(spy), metrics(spy_oos)
        rows.append(dict(panel=pname, dial="baseline", arm="SPY", dval=np.nan,
                         CAGR=sm["CAGR"], Sharpe=sm["Sharpe"], MaxDD=sm["MaxDD"],
                         Vol=sm["Vol"], H1=half_sharpes(spy)[0], H2=half_sharpes(spy)[1],
                         IS_Sharpe=metrics(spy.loc[IS_START:IS_END])["Sharpe"],
                         IS_CAGR=metrics(spy.loc[IS_START:IS_END])["CAGR"],
                         OOS_Sharpe=smo["Sharpe"], OOS_CAGR=smo["CAGR"],
                         OOS_MaxDD=smo["MaxDD"], turn=0.0, gross=1.0, sat_share=np.nan,
                         p4a=np.nan, f4b="", p4b=np.nan))

        for dial, alist in arms.items():
            for aname, spec in alist:
                r, turn, gr = run(spec)
                mm, mo = metrics(r), metrics(r.loc[OOS_START:])
                h1, h2 = half_sharpes(r)
                sat = float((nel <= spec["n"]).mean()) if spec["n"] else 0.0
                dv = {"n": spec["n"], "cadence": {"D": 1, "W": 5, "M": 21, "Q": 63}[spec["freq"]],
                      "gross": spec["gross"], "volgate": spec["max_vol"],
                      "trim": spec["band"]}[dial]
                f4b = fail4b(r, spy, r.loc[OOS_START:], spy_oos)
                rows.append(dict(panel=pname, dial=dial, arm=aname, dval=dv,
                                 CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                                 Vol=mm["Vol"], H1=h1, H2=h2,
                                 IS_Sharpe=metrics(r.loc[IS_START:IS_END])["Sharpe"],
                                 IS_CAGR=metrics(r.loc[IS_START:IS_END])["CAGR"],
                                 OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"],
                                 OOS_MaxDD=mo["MaxDD"], turn=turn, gross=gr, sat_share=sat,
                                 p4a=pass4a(r, bl["v2"]), f4b=f4b, p4b=(f4b == "-"),
                                 p4a_v1=pass4a(r, bl["v1"])))
                series[(pname, dial, aname)] = r
        P(f"  panel {pname:<10} px {px.shape[0]}x{px.shape[1]}  tradable {len(tr):>3}  "
          f"{sum(len(a) for a in arms.values())} arms + 3 baselines done")
    return pd.DataFrame(rows), series


# ============================================================== selector pair
def selectors(grid, sat_cap=SAT_CAP):
    """S_SHARPE = argmax IS_Sharpe, S_CAGR = argmax IS_CAGR, inside each (panel,dial) menu.
    DONOTHING = the dial's own base arm (the EWall/W/0.75/0.60 book, or B0.03 for trim)."""
    base_arm = {"n": "EWall", "cadence": "FREQ_W", "gross": "G0.70",
                "volgate": "V0.60", "trim": "B0.03"}
    out = []
    for (pname, dial), g in grid[grid.dial != "baseline"].groupby(["panel", "dial"]):
        pool = g.copy()
        if dial == "n":                       # idea 259's saturation cap, verbatim
            pool = pool[(pool.arm == "EWall") | (pool.sat_share <= sat_cap)]
        if pool.empty:
            continue
        ss = pool.loc[pool.IS_Sharpe.idxmax()]
        sc = pool.loc[pool.IS_CAGR.idxmax()]
        dn = pool[pool.arm == base_arm[dial]]
        dn = dn.iloc[0] if len(dn) else pool.iloc[0]
        for sname, r in (("S_SHARPE", ss), ("S_CAGR", sc), ("DONOTHING", dn)):
            out.append(dict(panel=pname, dial=dial, selector=sname, pick=r.arm,
                            n_arms=len(pool), IS_Sharpe=r.IS_Sharpe, IS_CAGR=r.IS_CAGR,
                            OOS_Sharpe=r.OOS_Sharpe, OOS_CAGR=r.OOS_CAGR,
                            OOS_MaxDD=r.OOS_MaxDD, Sharpe=r.Sharpe, CAGR=r.CAGR,
                            MaxDD=r.MaxDD, H1=r.H1, H2=r.H2, turn=r.turn,
                            p4a=r.p4a, p4a_v1=r.p4a_v1, p4b=r.p4b, f4b=r.f4b))
    return pd.DataFrame(out)


def exchange_rates(picks):
    """Per cell: S_CAGR minus S_SHARPE, and xr = dCAGR(pp) / (-dSharpe)."""
    rows = []
    for (pname, dial), g in picks.groupby(["panel", "dial"]):
        s = g[g.selector == "S_SHARPE"].iloc[0]
        c = g[g.selector == "S_CAGR"].iloc[0]
        d = g[g.selector == "DONOTHING"].iloc[0]
        dS = c.OOS_Sharpe - s.OOS_Sharpe
        dC = (c.OOS_CAGR - s.OOS_CAGR) * 100.0
        same = bool(c.pick == s.pick)
        xr = np.nan if (same or dS >= 0) else dC / (-dS)
        rows.append(dict(panel=pname, dial=dial, pick_S=s.pick, pick_C=c.pick, same=same,
                         dOOS_Sharpe=dS, dOOS_CAGR_pp=dC, xr=xr,
                         freelunch=bool((not same) and dS > 0 and dC > 0),
                         both_worse=bool((not same) and dS < 0 and dC < 0),
                         S_OOS_Sharpe=s.OOS_Sharpe, C_OOS_Sharpe=c.OOS_Sharpe,
                         DN_OOS_Sharpe=d.OOS_Sharpe,
                         S_OOS_CAGR=s.OOS_CAGR, C_OOS_CAGR=c.OOS_CAGR,
                         DN_OOS_CAGR=d.OOS_CAGR, n_arms=s.n_arms))
    return pd.DataFrame(rows)


def perm_heterogeneity(df, col, label="dial", n=N_PERM, seed=RNG_SEED):
    """Permutation test of 'the per-cell value is exchangeable across dials'.
    Statistic = spread (max-min) of the per-label mean.  Returns (obs, p)."""
    d = df[[label, col]].dropna()
    if d[label].nunique() < 2 or len(d) < 4:
        return np.nan, np.nan
    vals = d[col].to_numpy(float)
    codes, _ = pd.factorize(d[label])
    k = codes.max() + 1
    cnt = np.bincount(codes, minlength=k).astype(float)
    means = np.bincount(codes, weights=vals, minlength=k) / cnt
    obs = float(means.max() - means.min())
    rng = np.random.default_rng(seed)
    hits = 0
    for _ in range(n):
        p = rng.permutation(vals)
        m = np.bincount(codes, weights=p, minlength=k) / cnt
        if (m.max() - m.min()) >= obs:
            hits += 1
    return obs, (hits + 1) / (n + 1)


def perm_blocked(df, col, label="dial", block="panel", n=N_PERM, seed=RNG_SEED):
    """Exact randomisation test for a BALANCED block design: the dial labels are shuffled
    WITHIN each panel, so panel effects cannot leak into the statistic.  This is the right
    null for 'the dial does not matter' on a 12-panel x 5-dial grid."""
    d = df[[block, label, col]].dropna()
    if d[label].nunique() < 2:
        return np.nan, np.nan
    vals = d[col].to_numpy(float)
    codes, _ = pd.factorize(d[label])
    bcodes, _ = pd.factorize(d[block])
    k = codes.max() + 1
    cnt = np.bincount(codes, minlength=k).astype(float)
    obs = float((lambda m: m.max() - m.min())(
        np.bincount(codes, weights=vals, minlength=k) / cnt))
    blocks = [np.where(bcodes == b)[0] for b in range(bcodes.max() + 1)]
    rng = np.random.default_rng(seed)
    hits = 0
    for _ in range(n):
        c = codes.copy()
        for ix in blocks:
            c[ix] = rng.permutation(codes[ix])
        cn = np.bincount(c, minlength=k).astype(float)
        m = np.bincount(c, weights=vals, minlength=k) / cn
        if (m.max() - m.min()) >= obs:
            hits += 1
    return obs, (hits + 1) / (n + 1)


# ============================================================== LEG B: record census
METRIC_KEYS = {"is_sharpe": "IS_Sharpe", "is_cagr": "IS_CAGR",
               "oos_sharpe": "OOS_Sharpe", "oos_cagr": "OOS_CAGR"}
NON_DIAL = {"cagr", "sharpe", "maxdd", "vol", "sortino", "calmar", "h1", "h2", "turn",
            "turnover", "gross", "sat_share", "years", "total", "winrate", "bestday",
            "worstday", "oos_maxdd", "is_maxdd", "is_h1", "is_h2", "equity", "start",
            "end", "date"}


BARRED = {"seed", "draw", "rep", "reps", "rung", "phase", "shift", "fold", "cost_bps",
          "cost", "bps", "panel", "source", "book", "arm", "name", "label", "point",
          "key", "file", "idx", "id", "row", "m", "f", "verdict", "pick", "selector",
          "ticker", "sector", "year", "split", "sample", "variant", "run"}


def barred_dial(c):
    """Idea 241's convention: replication and reporting axes may not BE the dial."""
    cl = c.lower().replace(" ", "")
    return cl in BARRED or cl.startswith(("fail", "pass", "p4", "f4", "unnamed"))


def dial_family(colname):
    c = colname.lower()
    if any(k in c for k in ("cadence", "freq", "sched", "period", "rebal")):
        return "cadence"
    if any(k in c for k in ("gross", "lever", "notional")) or c in ("g", "w"):
        return "gross"
    if "vol" in c:
        return "volgate"
    if any(k in c for k in ("band", "trim", "elig", "thresh", "quant", "cut", "floor",
                            "depth", "breadth")) or c in ("q", "b", "d", "t"):
        return "trim"
    if c in ("n", "k", "topn", "nn", "n_hold", "nhold", "top") or c.startswith("n_"):
        return "n"
    return "other"


MAX_ROWS = 200_000        # census guards, pre-registered so the leg terminates
MAX_LEVELS = 60           # a label column with more levels is an id, not a dial
MAX_DIALS = 12            # dial candidates considered per file
MAX_MENUS = 2000          # menus taken per (file, dial)


def census():
    files = sorted(OUT.glob("*.csv")) + sorted(OUT.glob("*.csv.gz"))
    files = [f for f in files if not f.name.startswith(STEM)]
    menus, nfiles, unread, skipped_big = [], 0, 0, 0
    for f in files:
        try:
            df = pd.read_csv(f)
        except Exception:
            unread += 1
            continue
        if len(df) > MAX_ROWS:
            skipped_big += 1
            continue
        low = {c.lower().replace(" ", ""): c for c in df.columns}
        if not all(k in low for k in METRIC_KEYS):
            continue
        ren = {low[k]: v for k, v in METRIC_KEYS.items()}
        df = df.rename(columns=ren)
        for v in METRIC_KEYS.values():
            df[v] = pd.to_numeric(df[v], errors="coerce")
        df = df.dropna(subset=list(METRIC_KEYS.values()))
        if len(df) < 3:
            continue
        labels = [c for c in df.columns
                  if c not in METRIC_KEYS.values()
                  and c.lower().replace(" ", "") not in NON_DIAL
                  and not c.lower().startswith(("is_", "oos_", "spy_", "v1_", "v2_"))
                  and 1 < df[c].nunique(dropna=False) <= MAX_LEVELS]
        used = False
        cands = [c for c in labels
                 if df[c].nunique(dropna=False) >= 3 and not barred_dial(c)][:MAX_DIALS]
        for d in cands:
            others = [c for c in labels if c != d]
            try:
                grp = df.groupby(others, dropna=False) if others else [((), df)]
                if others and grp.ngroups > MAX_MENUS:
                    continue
            except Exception:
                continue
            for key, g in grp:
                g = g.dropna(subset=[d])
                if g[d].nunique() < 3 or len(g) < 3:
                    continue
                s = g.loc[g.IS_Sharpe.idxmax()]
                c = g.loc[g.IS_CAGR.idxmax()]
                dS = float(c.OOS_Sharpe - s.OOS_Sharpe)
                dC = float(c.OOS_CAGR - s.OOS_CAGR)
                # unit guard: some files publish CAGR in %, some in fractions
                dC_pp = dC * 100.0 if g.OOS_CAGR.abs().max() < 2.0 else dC
                menus.append(dict(file=f.name, dial_col=d, family=dial_family(d),
                                  arms=len(g), same=bool(s.name == c.name),
                                  dOOS_Sharpe=dS, dOOS_CAGR_pp=dC_pp,
                                  xr=(np.nan if (s.name == c.name or dS >= 0)
                                      else dC_pp / (-dS)),
                                  key=str(key)))
                used = True
        nfiles += used
    return pd.DataFrame(menus), len(files), nfiles, unread, skipped_big


# ============================================================== GATE: idea 259 reproduction
def gate_259(grid, named):
    """Idea 259's rule-8 n-dial numbers, its four panels only, pooled equal-weight."""
    g = grid[(grid.dial == "n") & (grid.panel.isin(named))]
    picks = selectors(pd.concat([g, grid[(grid.dial == "baseline")
                                         & (grid.panel.isin(named))]]))
    picks = picks[picks.dial == "n"]
    ew = g[g.arm == "EWall"].set_index("panel")
    f20 = g[g.arm == "FWD20"].set_index("panel")
    pool = picks.groupby("selector")[["OOS_Sharpe", "OOS_CAGR"]].mean()
    pool.loc["EWALL"] = [ew.OOS_Sharpe.mean(), ew.OOS_CAGR.mean()]
    pool.loc["FWD20"] = [f20.OOS_Sharpe.mean(), f20.OOS_CAGR.mean()]
    diff = picks.pivot(index="panel", columns="selector", values="pick")
    ndiff = int((diff["S_CAGR"] != diff["S_SHARPE"]).sum())
    return pool, diff, ndiff, picks


# ============================================================== main
def main():
    P("=" * 200)
    P(f"Idea 270 is-S_CAGR-vs-S_SHARPE-a-general-selector-pair (lane B, 2026-09-09) | {SCRIPT}")
    P(f"{COST_BPS} bps per unit turnover | weekly base cadence (cadence dial is the treatment) "
      f"| next-day execution | IS {IS_START}..{IS_END} chooses, OOS {OOS_START}+ read once")
    P("Tuned parameters: ONE (the dial value inside a cell, chosen on IS only). Panel and dial "
      "are enumerated reporting axes; every grid point is reported.")
    P("=" * 200)

    P("\n[1] PANELS")
    panels, named = build_panels()
    P(f"  {len(panels)} panels: 4 named ({', '.join(named)}) + 8 pre-registered seeded sub-panels")

    P("\n[2] GRID  (5 dials x 12 panels, all arms)")
    grid, series = run_grid(panels)
    grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    P(f"  grid rows: {len(grid)}  ->  {STEM}.grid.csv")

    # ---------------------------------------------------------- gate
    P("\n[3] GATE — idea 259's rule-8 n-dial reproduction (its 4 panels, its arms, its cap)")
    pool, diff, ndiff, p259 = gate_259(grid, named)
    P(fmt(pool[["OOS_Sharpe", "OOS_CAGR"]], 4))
    P(f"  picks by panel:\n{diff.to_string()}")
    P(f"  S_CAGR and S_SHARPE pick a DIFFERENT arm in {ndiff} of {len(diff)} panels "
      f"(idea 259 published 3 of 4)")
    dS259 = pool.loc["S_CAGR", "OOS_Sharpe"] - pool.loc["S_SHARPE", "OOS_Sharpe"]
    dC259 = (pool.loc["S_CAGR", "OOS_CAGR"] - pool.loc["S_SHARPE", "OOS_CAGR"]) * 100
    P(f"  S_CAGR minus S_SHARPE pooled: OOS Sharpe {dS259:+.4f} (published -0.0254), "
      f"OOS CAGR {dC259:+.2f} pp (published +2.53)")
    P(f"  published OOS Sharpe levels: EWALL 0.8577 > FWD20 0.8428 > S_SHARPE 0.7815 > "
      f"S_CAGR 0.7561; here EWALL {pool.loc['EWALL','OOS_Sharpe']:.4f} "
      f"FWD20 {pool.loc['FWD20','OOS_Sharpe']:.4f} "
      f"S_SHARPE {pool.loc['S_SHARPE','OOS_Sharpe']:.4f} "
      f"S_CAGR {pool.loc['S_CAGR','OOS_Sharpe']:.4f}")
    gate_ok = (ndiff == 3 and abs(dS259 - (-0.0254)) < 0.01 and abs(dC259 - 2.53) < 0.5)
    P(f"  GATE {'PASS' if gate_ok else 'REVIEW — differences reported above, not hidden'}")

    # ---------------------------------------------------------- leg A
    P("\n[4] LEG A — the selector pair on all five dials")
    picks = selectors(grid)
    picks.to_csv(OUT / f"{STEM}.picks.csv", index=False)
    xr = exchange_rates(picks)
    xr.to_csv(OUT / f"{STEM}.xr.csv", index=False)
    P(f"  cells: {len(xr)} = {xr.panel.nunique()} panels x {xr.dial.nunique()} dials  "
      f"->  {STEM}.picks.csv / {STEM}.xr.csv")

    P("\n  4.1 DISAGREEMENT — do the two selectors even pick different arms?")
    tab = xr.groupby("dial").agg(cells=("same", "size"), same=("same", "sum"))
    tab["disagree"] = tab.cells - tab.same
    tab["rate"] = tab.disagree / tab.cells
    P(fmt(tab, 3))
    P(f"  pooled disagreement {int(tab.disagree.sum())}/{int(tab.cells.sum())} "
      f"= {tab.disagree.sum()/tab.cells.sum():.1%}")

    P("\n  4.2 THE EXCHANGE RATE, per dial (S_CAGR minus S_SHARPE, OOS, read once)")
    rows = []
    for dial, g in xr.groupby("dial"):
        mS, tS, nS = tstat(g.dOOS_Sharpe)
        mC, tC, nC = tstat(g.dOOS_CAGR_pp)
        gd = g[~g.same]
        mSd, tSd, _ = tstat(gd.dOOS_Sharpe)
        mCd, tCd, _ = tstat(gd.dOOS_CAGR_pp)
        rows.append(dict(dial=dial, cells=nS, disagree=len(gd),
                         dSharpe=mS, t_dSharpe=tS, dCAGR_pp=mC, t_dCAGR=tC,
                         xr_ratio_of_means=(mCd / -mSd if (len(gd) and mSd < 0) else np.nan),
                         xr_median_cell=gd.xr.median(),
                         dSharpe_dis=mSd, dCAGR_dis=mCd,
                         freelunch=int(g.freelunch.sum()), both_worse=int(g.both_worse.sum())))
    per_dial = pd.DataFrame(rows).set_index("dial")
    P(fmt(per_dial, 4))
    mS, tS, nS = tstat(xr.dOOS_Sharpe)
    mC, tC, nC = tstat(xr.dOOS_CAGR_pp)
    P(f"  POOLED over all {nS} cells: dOOS Sharpe {mS:+.4f} (t {tS:+.2f}), "
      f"dOOS CAGR {mC:+.2f} pp (t {tC:+.2f}), "
      f"ratio-of-means exchange rate {(mC/-mS if mS<0 else float('nan')):.2f} pp per Sharpe point")
    P(f"  idea 259's n-dial figure on its 4 panels: {dC259:+.2f} pp for {dS259:+.4f} Sharpe "
      f"= {(dC259/-dS259 if dS259<0 else float('nan')):.1f} pp per Sharpe point")

    P("\n  4.3 IS THE EXCHANGE RATE A CONSTANT?  permutation test, labels shuffled across cells")
    for col, lab in (("dOOS_CAGR_pp", "dOOS CAGR (pp)"), ("dOOS_Sharpe", "dOOS Sharpe"),
                     ("xr", "per-cell xr")):
        obs, p = perm_heterogeneity(xr, col, "dial")
        obs2, p2 = perm_blocked(xr, col, "dial", "panel")
        P(f"    {lab:<18} spread of per-dial means {obs:9.4f}   unrestricted p = "
          f"{p:.4f} | BLOCKED within panel p = {p2:.4f}  ({N_PERM} draws each)")
    P("    (small p = the dial matters, i.e. the exchange rate is DIAL-SPECIFIC; "
      "large p = one constant is consistent with the data)")

    P("\n  4.4 SIGN CONSISTENCY — is it always +CAGR for -Sharpe?")
    gd = xr[~xr.same]
    P(f"    disagreeing cells {len(gd)}: S_CAGR gains CAGR in {int((gd.dOOS_CAGR_pp>0).sum())}, "
      f"loses Sharpe in {int((gd.dOOS_Sharpe<0).sum())}, "
      f"BOTH (the queue's shape) in {int(((gd.dOOS_CAGR_pp>0)&(gd.dOOS_Sharpe<0)).sum())}, "
      f"free lunch (both better) in {int(gd.freelunch.sum())}, "
      f"both worse in {int(gd.both_worse.sum())}")

    P("\n  4.5 vs DO-NOTHING and vs SPY — does either selector earn its keep?")
    lvl = picks.groupby("selector")[["OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD"]].mean()
    spy = grid[(grid.dial == "baseline") & (grid.arm == "SPY")]
    v2 = grid[(grid.dial == "baseline") & (grid.arm == "RULES_v2")]
    lvl.loc["SPY (per panel mean)"] = [spy.OOS_Sharpe.mean(), spy.OOS_CAGR.mean(),
                                       spy.OOS_MaxDD.mean()]
    lvl.loc["RULES v2 (live)"] = [v2.OOS_Sharpe.mean(), v2.OOS_CAGR.mean(), v2.OOS_MaxDD.mean()]
    P(fmt(lvl, 4))
    for s in ("S_SHARPE", "S_CAGR"):
        a = picks[picks.selector == s].set_index(["panel", "dial"]).OOS_Sharpe
        b = picks[picks.selector == "DONOTHING"].set_index(["panel", "dial"]).OOS_Sharpe
        m, t, n = tstat((a - b).values)
        P(f"    {s} minus DONOTHING OOS Sharpe: {m:+.4f} (t {t:+.2f}, n {n}, "
          f"wins {int((a-b>0).sum())}/{n})")

    P("\n  4.6 KEEP PATHS over every grid point (4a vs the LIVE RULES v2 book, 4b vs SPY)")
    ga = grid[grid.dial != "baseline"]
    P(f"    all {len(ga)} arms: 4a(v2) {int(ga.p4a.sum())}, 4a(v1, superseded) "
      f"{int(ga.p4a_v1.sum())}, 4b {int(ga.p4b.sum())}")
    P(fmt(ga.groupby("dial").agg(arms=("p4a", "size"), p4a_v2=("p4a", "sum"),
                                 p4a_v1=("p4a_v1", "sum"), p4b=("p4b", "sum")), 0))
    P(f"    4b failure reasons: {ga.f4b.value_counts().head(8).to_dict()}")
    sel_arms = picks[picks.selector.isin(["S_SHARPE", "S_CAGR"])]
    P(f"    among the {len(sel_arms)} SELECTED arms: 4a(v2) {int(sel_arms.p4a.sum())}, "
      f"4b {int(sel_arms.p4b.sum())}")

    # ---------------------------------------------------------- leg B
    P("\n[5] LEG B — the queue's literal ask: the same selector pair over the RECORD's "
      "committed grid CSVs")
    cen, nfile_all, nfile_used, unread, skipped_big = census()
    cen.to_csv(OUT / f"{STEM}.census.csv", index=False)
    P(f"  {nfile_all} committed CSVs scanned ({unread} unreadable, {skipped_big} over "
      f"{MAX_ROWS} rows), {nfile_used} carry "
      f"IS_Sharpe+IS_CAGR+OOS_Sharpe+OOS_CAGR and a sweepable dial -> {len(cen)} menus")
    if len(cen):
        ct = cen.groupby("family").agg(menus=("same", "size"), files=("file", "nunique"),
                                       same=("same", "sum"),
                                       dSharpe=("dOOS_Sharpe", "mean"),
                                       dCAGR_pp=("dOOS_CAGR_pp", "mean"),
                                       xr_med=("xr", "median"))
        ct["disagree_rate"] = 1 - ct.same / ct.menus
        ct["xr_ratio"] = np.where(ct.dSharpe < 0, ct.dCAGR_pp / -ct.dSharpe, np.nan)
        P(fmt(ct, 4))
        mS, tS, nS = tstat(cen.dOOS_Sharpe)
        mC, tC, nC = tstat(cen.dOOS_CAGR_pp)
        P(f"  MENU-POOLED over {nS} record menus: dOOS Sharpe {mS:+.4f} (t {tS:+.2f}), "
          f"dOOS CAGR {mC:+.2f} pp (t {tC:+.2f}), "
          f"exchange rate {(mC/-mS if mS<0 else float('nan')):.2f} pp per Sharpe point")
        P("  -- menus are nested inside files (one file contributes up to "
          f"{int(cen.groupby('file').size().max())}), so the menu-pooled t is inflated. "
          "FILE-CLUSTERED below is the honest one:")
        fc = cen.groupby("file")[["dOOS_Sharpe", "dOOS_CAGR_pp"]].mean()
        fsame = cen.groupby("file")["same"].mean()
        mSf, tSf, nSf = tstat(fc.dOOS_Sharpe)
        mCf, tCf, _ = tstat(fc.dOOS_CAGR_pp)
        P(f"  FILE-CLUSTERED over {nSf} files: dOOS Sharpe {mSf:+.4f} (t {tSf:+.2f}, "
          f"negative in {int((fc.dOOS_Sharpe<0).sum())}/{nSf}), dOOS CAGR {mCf:+.2f} pp "
          f"(t {tCf:+.2f}, positive in {int((fc.dOOS_CAGR_pp>0).sum())}/{nSf}), "
          f"exchange rate {(mCf/-mSf if mSf<0 else float('nan')):.2f} pp per Sharpe point; "
          f"mean per-file agreement rate {fsame.mean():.3f}")
        fam_file = (cen.groupby(["family", "file"])[["dOOS_Sharpe", "dOOS_CAGR_pp"]]
                    .mean().reset_index())
        P("  per-family, FILE-CLUSTERED (one row per file, then averaged):")
        P(fmt(fam_file.groupby("family").agg(files=("file", "nunique"),
                                             dSharpe=("dOOS_Sharpe", "mean"),
                                             dCAGR_pp=("dOOS_CAGR_pp", "mean")), 4))
        for lab, frame, key in (("menu-pooled", cen, "family"),
                                ("file-clustered", fam_file, "family")):
            obs, p = perm_heterogeneity(frame, "dOOS_CAGR_pp", key)
            P(f"  permutation heterogeneity across families ({lab}, dOOS CAGR): "
              f"spread {obs:.4f}, p = {p:.4f}")
            obs, p = perm_heterogeneity(frame, "dOOS_Sharpe", key)
            P(f"  permutation heterogeneity across families ({lab}, dOOS Sharpe): "
              f"spread {obs:.4f}, p = {p:.4f}")
        oth = cen[cen.family == "other"].dial_col.value_counts().head(12)
        P(f"  the 'other' family is {len(cen[cen.family=='other'])}/{len(cen)} menus — its "
          f"commonest dial columns: {oth.to_dict()}")
        P("  CAVEAT: record menus are heterogeneous in construction, cost rung and sample; "
          "they are a corpus check on Leg A's sign and spread, not a controlled experiment.")

    # ---------------------------------------------------------- walk-forward artefact
    wf = picks.merge(xr[["panel", "dial", "same", "dOOS_Sharpe", "dOOS_CAGR_pp", "xr"]],
                     on=["panel", "dial"], how="left")
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(f"\n[6] walk-forward artefact -> {STEM}.walkforward.csv ({len(wf)} rows)")

    P("\n[7] LEADERBOARD-READY SUMMARY")
    P(f"  disagreement {int(tab.disagree.sum())}/{int(tab.cells.sum())}; pooled "
      f"dOOS_Sharpe {mS if False else tstat(xr.dOOS_Sharpe)[0]:+.4f}, pooled dOOS_CAGR "
      f"{tstat(xr.dOOS_CAGR_pp)[0]:+.2f} pp")
    P("=" * 200)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
