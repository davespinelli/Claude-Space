#!/usr/bin/env python3
"""
Idea 1313 (lane cloud, 2026-09-18) — do SELECTION and EXPOSURE STACK at SMALL's DD CAP?

THE PREMISE, READ FROM THE RECORD.  PROTOCOL 4b's drawdown cap (MaxDD <= 0.60 x SPY's) is the
modal reason this family fails 4b (idea 1215: 88 of 148 failing cells bind it).  On SMALL the
cap is -20.23% and the certified incumbent (N=15 / H=126 / GROSS=0.60 / W) runs -32.33%, a
13.12 pp miss.  Two instruments have been priced SEPARATELY against that leg:
  * SELECTION (idea 1301): the shallowest cell of its 24-cell N x H grid, N=30 / H=63, buys
    +4.66 pp of drawdown FOR FREE (+0.70 pp of CAGR too).
  * EXPOSURE  (idea 1297): a vol-target scaler k_t = min(0.60, TARGET / v_t) buys up to
    +9.90 pp (6% / 21d) but pays -2.58 pp of CAGR and still misses the cap by 2.20 pp.
Neither alone closes 13.12 pp and NEITHER RUN TESTED THEM TOGETHER.  This run stacks them:
the vol-target ladder is applied ON TOP OF the selection cell rather than on the incumbent.

THE QUESTION.  Do the two drawdown gains ADD (they act on different parts of the return —
WHICH names vs HOW MUCH of them) or SUBSTITUTE (both are just de-risking the same episode)?
The run publishes, at every cell, the ADDITIVITY RESIDUAL
    resid_pp = dMaxDD(stack) - [ dMaxDD(selection only) + dMaxDD(exposure only) ]
all three measured in pp against the SAME frozen anchor (the certified incumbent on that
panel).  resid ~ 0 means the instruments are additive; resid < 0 means they substitute.

THE GRID (exactly two dials, PROTOCOL rule 4).
    N       (names held)      {15, 20, 30, 40}
    TARGET  (annualised vol)  {6, 8, 10, 12}%
16 stacked cells, EVERY ONE PUBLISHED, on every panel.  FROZEN at the values each prior run
already certified and NOT tuned here: H=63 (1301's shallowest cell), WINDOW=21d (1297's only
OOS winner), CAP=0.60 (the incumbent's gross, PROTOCOL rule 2 — no leverage), cadence W,
10 bps, warm-up 260 rows, decide-at-t / apply-at-t+1.

ALSO PUBLISHED, NOT DIALS: the 4 SELECTION-ONLY (flat gross 0.60) books at each N, the 4
EXPOSURE-ONLY books at each TARGET on the incumbent's own N=15/H=126, and the frozen anchor
itself — the comparands the additivity residual is built from; PANEL {U56, B136, SMALL663}
(rule 9); both KEEP paths at every cell; the IS/OOS windows; the halves.

VOL-TARGET BASIS.  v_t is the annualised sd of the SELECTION BOOK's own FLAT (constant-gross)
returns over the WINDOW rows ENDING AT t-1 — idea 1297's B_CONST basis, which is causal under
PROTOCOL rule 2 and not self-referential.  A B_SELF arm (v from the scaled book's own realised
returns, computed recursively rebalance by rebalance) is published as a robustness read.

PROTOCOL: rule 1 (>= 10 years, gate G0); rule 2 (t+1 execution, 10 bps, no leverage); rule 3
(compare against live RULES v2 AND SPY); rule 4 (both KEEP paths, 2 tuned parameters);
rule 8 (walk-forward: (N, TARGET) chosen by argmax IS Sharpe on warm-up..2016-12-31, 2017-2026
read ONCE); rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py are NOT modified by this script.

SMALL PANEL (house filter): data/small_meta.csv, drop every ticker with max_1d_move >= 1.0
FIRST.  SURVIVORSHIP: the small panel is the CURRENT constituents of a sub-$2B screen carried
back to 2010, so every absolute SMALL number is biased UP; a KILL read on it is therefore
strengthened, not weakened, by the bias.

Runs standalone and offline (committed price caches only; no network).
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-18"
SLUG = "do-SELECTION-and-EXPOSURE-STACK-at-SMALL-s-DD-CAP"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
COST = 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G, I_C = 15, 126, 0.60, "W"       # the certified incumbent / anchor, frozen
S_H = 63                                       # 1301's shallowest cell's H, frozen
WINDOW = 21                                    # 1297's OOS winner's window, frozen
NS = [15, 20, 30, 40]                          # DIAL 1
TARGETS = [0.06, 0.08, 0.10, 0.12]             # DIAL 2
OOS_START, IS_END = "2017-01-01", "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

C_U56 = dict(CAGR=0.1366, Sharpe=1.1706, MaxDD=-0.1638)     # 1215/1297/1301 U56 anchor
C_SMALL_CAP, C_SMALL_FLOOR = -0.2023, 0.0984                # 1297/1301 SMALL 4b legs

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=value, target=target, pass_=bool(ok)))
    say(f"    [{'PASS' if ok else 'FAIL'}] {name}: {value} (target {target})")
    return bool(ok)


# ==================================================================== the record's mechanism
def mech(q):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = (q > q.rolling(200).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    sc = (comp * (0.5 + 0.5 * above.astype(float))).values
    return sc, above, np.nan_to_num(vol20, nan=1e9)


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        m = rebalance_mask(px.index, I_C).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        self.idx = px.index
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.lo = WARMUP
        self.i_oos = int(np.searchsorted(px.index.values, np.datetime64(OOS_START)))
        self.i_ise = int(np.searchsorted(px.index.values, np.datetime64(IS_END), side="right"))


def build1(pan, N, H, lag=1):
    """The record's min-hold selection frame at GROSS = 1.0 (row t = application-time weight)."""
    reb = pan.reb
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    for i, t in enumerate(reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.rank_key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def run_gross(pan, frame, gvec):
    """The record's runner with a PER-REBALANCE gross vector gvec (len = len(pan.reb)).
    Returns (gross daily returns, one-way turnover per row); costs applied afterwards."""
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    turn = np.zeros(T)
    out = np.zeros(T)
    curw = np.zeros(M)
    reb = np.asarray(pan.reb, dtype=np.int64)
    ends = np.append(reb[1:], T)
    for i, (i0, i1) in enumerate(zip(reb, ends)):
        w0 = gvec[i] * frame[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return out, turn


def run_const(pan, frame, g=I_G):
    return run_gross(pan, frame, np.full(len(pan.reb), float(g)))


def kvec_from(series, pan, target, window=WINDOW, cap=I_G):
    """k_t = min(cap, TARGET / v_t), v_t = annualised sd of `series` over the `window` rows
    ENDING AT t-1 (PROTOCOL rule 2: nothing from t is used to size t)."""
    s = pd.Series(series)
    v = (s.rolling(window).std(ddof=0) * np.sqrt(252)).shift(1).values
    k = np.empty(len(pan.reb))
    for i, t in enumerate(pan.reb):
        vt = v[t] if t < len(v) else np.nan
        k[i] = cap if not np.isfinite(vt) or vt <= 0 else min(cap, target / vt)
    return k


def run_self(pan, frame, target, window=WINDOW, cap=I_G):
    """B_SELF robustness arm: v_t from the SCALED book's OWN realised gross returns, built
    forward rebalance by rebalance (still strictly causal: rows ending at t-1)."""
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    turn = np.zeros(T)
    out = np.zeros(T)
    curw = np.zeros(M)
    reb = np.asarray(pan.reb, dtype=np.int64)
    ends = np.append(reb[1:], T)
    ks = np.empty(len(reb))
    for i, (i0, i1) in enumerate(zip(reb, ends)):
        j0 = i0 - window
        if j0 < 1:
            k = cap
        else:
            v = float(np.std(out[j0:i0], ddof=0) * np.sqrt(252))
            k = cap if v <= 0 else min(cap, target / v)
        ks[i] = k
        w0 = k * frame[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return out, turn, ks


def at_cost(gr, tu, c=COST):
    return gr - tu * c / 1e4


def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min()) if len(e) else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    return float(np.cumprod(1 + r)[-1] ** (252 / len(r)) - 1)


def triple(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def annturn(tu):
    return float(np.sum(tu) * 252.0 / len(tu)) if len(tu) else np.nan


def bmpack(r):
    h1, h2 = halves(r)
    m = triple(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def keep_paths(r, bm, live):
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    k4b = bool(h1 > bm["H1"] and h2 > bm["H2"]
               and m["MaxDD"] >= DD_CAP * bm["MaxDD"]
               and m["CAGR"] >= CAGR_FLOOR * bm["CAGR"])
    return k4a, k4b, m, h1, h2


def keep4b_window(r, b):
    m = triple(r)
    return bool(m["Sharpe"] > b["Sharpe"] and m["MaxDD"] >= DD_CAP * b["MaxDD"]
                and m["CAGR"] >= CAGR_FLOOR * b["CAGR"]), m


# ==================================================================== main
def main():
    t0 = time.time()
    say("=" * 104)
    say("IDEA 1313 (lane cloud, 2026-09-18) — do SELECTION and EXPOSURE STACK at SMALL's DD CAP?")
    say("=" * 104)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad]
    say(f"  SMALL house filter: data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0; {len(inv)} investable of {len(pxS.columns)-1} priced")
    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL663", pxS, inv)]
    for p in panels:
        say(f"    {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y), {len(p.reb)} weekly rebalances, {len(p.invest)} names")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)

    # ------------------------------------------------------------ benchmarks (rule 3)
    bm, live, bm_oos, live_oos, bm_is = {}, {}, {}, {}, {}
    for p in panels:
        lo = p.lo
        spy = p.spy[lo:]
        bm[p.name] = bmpack(spy)
        bres = backtest(p.px, rules_v2_weights(p.px), cost_bps=COST, freq="W")
        lr = bres["returns"].fillna(0.0).values[lo:]
        live[p.name] = bmpack(lr)
        o = p.i_oos - lo
        bm_oos[p.name] = bmpack(spy[o:])
        live_oos[p.name] = bmpack(lr[o:])
        bm_is[p.name] = bmpack(spy[: p.i_ise - lo])
        say(f"  {p.name:9s} SPY {bm[p.name]['CAGR']:7.2%} / {bm[p.name]['Sharpe']:.4f} / "
            f"{bm[p.name]['MaxDD']:7.2%} (H1 {bm[p.name]['H1']:.4f} H2 {bm[p.name]['H2']:.4f}) "
            f"| 4b cap {DD_CAP*bm[p.name]['MaxDD']:7.2%} floor {CAGR_FLOOR*bm[p.name]['CAGR']:6.2%}")
        say(f"  {p.name:9s} v2  {live[p.name]['CAGR']:7.2%} / {live[p.name]['Sharpe']:.4f} / "
            f"{live[p.name]['MaxDD']:7.2%} | OOS SPY {bm_oos[p.name]['CAGR']:7.2%} / "
            f"{bm_oos[p.name]['Sharpe']:.4f} / {bm_oos[p.name]['MaxDD']:7.2%} | OOS v2 "
            f"{live_oos[p.name]['CAGR']:7.2%} / {live_oos[p.name]['Sharpe']:.4f} / "
            f"{live_oos[p.name]['MaxDD']:7.2%}")

    rows, series = [], {}

    def record(p, kind, N, H, tgt, r, tu, extra=None):
        lo, o = p.lo, p.i_oos - p.lo
        k4a, k4b, m, h1, h2 = keep_paths(r, bm[p.name], live[p.name])
        k4b_oos, mo = keep4b_window(r[o:], bm_oos[p.name])
        ris = r[: p.i_ise - lo]
        d = dict(panel=p.name, arm=kind, N=N, H=H,
                 target=("" if tgt is None else round(tgt, 4)), window=("" if tgt is None else WINDOW),
                 cap=I_G, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                 turn=annturn(tu[lo:]), IS_CAGR=cagr(ris), IS_Sharpe=sharpe(ris), IS_MaxDD=mdd(ris),
                 OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                 dd_cap=DD_CAP * bm[p.name]["MaxDD"], cagr_floor=CAGR_FLOOR * bm[p.name]["CAGR"],
                 oos_dd_cap=DD_CAP * bm_oos[p.name]["MaxDD"],
                 oos_cagr_floor=CAGR_FLOOR * bm_oos[p.name]["CAGR"],
                 keep4a=k4a, keep4b_full=k4b, keep4b_oos=k4b_oos, keep4b_both=bool(k4b and k4b_oos))
        if extra:
            d.update(extra)
        rows.append(d)
        series[(p.name, kind, N, tgt)] = r
        return d

    say("")
    say("-" * 104)
    say(f"BUILDING: anchor (N={I_N}/H={I_H} flat) + SELECTION-only N {NS} at H={S_H} + "
        f"EXPOSURE-only TARGET {[f'{t:.0%}' for t in TARGETS]} on the anchor + "
        f"{len(NS)*len(TARGETS)} STACKED cells, x {len(panels)} panels, WINDOW={WINDOW}d, "
        f"cap={I_G}, {COST:.0f} bps")
    say("-" * 104)

    for p in panels:
        lo = p.lo
        # anchor: the certified incumbent, flat
        fr_anc = build1(p, I_N, I_H)
        gr_a, tu_a = run_const(p, fr_anc)
        r_anc = at_cost(gr_a, tu_a)[lo:]
        record(p, "ANCHOR", I_N, I_H, None, r_anc, tu_a)
        # exposure-only: 1297's ladder on the anchor
        for tgt in TARGETS:
            k = kvec_from(gr_a, p, tgt)
            g2, t2 = run_gross(p, fr_anc, k)
            record(p, "EXPOSURE", I_N, I_H, tgt, at_cost(g2, t2)[lo:], t2,
                   dict(k_mean=float(k.mean()), k_at_cap=float((k >= I_G - 1e-12).mean())))
        # selection-only and the stack
        for N in NS:
            fr = build1(p, N, S_H)
            gr_f, tu_f = run_const(p, fr)
            record(p, "SELECTION", N, S_H, None, at_cost(gr_f, tu_f)[lo:], tu_f)
            for tgt in TARGETS:
                k = kvec_from(gr_f, p, tgt)
                g2, t2 = run_gross(p, fr, k)
                record(p, "STACK", N, S_H, tgt, at_cost(g2, t2)[lo:], t2,
                       dict(k_mean=float(k.mean()), k_at_cap=float((k >= I_G - 1e-12).mean())))
                gs, ts, ks = run_self(p, fr, tgt)
                record(p, "STACK_SELF", N, S_H, tgt, at_cost(gs, ts)[lo:], ts,
                       dict(k_mean=float(ks.mean()), k_at_cap=float((ks >= I_G - 1e-12).mean())))
        say(f"  {p.name}: {1 + len(TARGETS) + len(NS)*(1 + 2*len(TARGETS))} books built")

    G = pd.DataFrame(rows)

    # ------------------------------------------------------------ additivity vs the anchor
    for p in panels:
        m = G.panel == p.name
        anc = G[m & (G.arm == "ANCHOR")].iloc[0]
        G.loc[m, "dMaxDD_pp"] = (G.loc[m, "MaxDD"] - anc["MaxDD"]) * 100
        G.loc[m, "dCAGR_pp"] = (G.loc[m, "CAGR"] - anc["CAGR"]) * 100
        G.loc[m, "dSharpe"] = G.loc[m, "Sharpe"] - anc["Sharpe"]
    with np.errstate(divide="ignore", invalid="ignore"):
        G["price"] = G["dMaxDD_pp"] / (-G["dCAGR_pp"])
    for i, x in G.iterrows():
        if x.arm not in ("STACK", "STACK_SELF"):
            continue
        sel = G[(G.panel == x.panel) & (G.arm == "SELECTION") & (G.N == x.N)].iloc[0]
        exp = G[(G.panel == x.panel) & (G.arm == "EXPOSURE") & (G.target == x.target)].iloc[0]
        G.loc[i, "dMaxDD_sel_pp"] = sel.dMaxDD_pp
        G.loc[i, "dMaxDD_exp_pp"] = exp.dMaxDD_pp
        G.loc[i, "additivity_resid_pp"] = x.dMaxDD_pp - (sel.dMaxDD_pp + exp.dMaxDD_pp)
        G.loc[i, "dCAGR_sel_pp"] = sel.dCAGR_pp
        G.loc[i, "dCAGR_exp_pp"] = exp.dCAGR_pp
        G.loc[i, "cagr_resid_pp"] = x.dCAGR_pp - (sel.dCAGR_pp + exp.dCAGR_pp)
    G.to_csv(f"{OUT}.grid.csv", index=False)

    # ------------------------------------------------------------ replay gates
    say("")
    say("-" * 104)
    say("REPLAY GATES against committed numbers (nothing is tuned on them)")
    say("-" * 104)
    aU = G[(G.panel == "U56") & (G.arm == "ANCHOR")].iloc[0]
    dU = max(abs(aU.CAGR - C_U56["CAGR"]), abs(aU.Sharpe - C_U56["Sharpe"]),
             abs(aU.MaxDD - C_U56["MaxDD"]))
    gate("G1 U56 anchor replays the record's 13.66% / 1.1706 / -16.38%",
         f"{aU.CAGR:.4%} / {aU.Sharpe:.4f} / {aU.MaxDD:.4%} (max|dev| {dU:.2e})",
         "max|dev| <= 5e-3", dU <= 5e-3)
    capS = DD_CAP * bm["SMALL663"]["MaxDD"]
    flS = CAGR_FLOOR * bm["SMALL663"]["CAGR"]
    gate("G2 SMALL 4b DD cap replays -20.23%", f"{capS:.4%}", "|dev| <= 2e-3",
         abs(capS - C_SMALL_CAP) <= 2e-3)
    gate("G3 SMALL 4b CAGR floor replays 9.84%", f"{flS:.4%}", "|dev| <= 2e-3",
         abs(flS - C_SMALL_FLOOR) <= 2e-3)
    s30 = G[(G.panel == "SMALL663") & (G.arm == "SELECTION") & (G.N == 30)].iloc[0]
    gate("G4 1301's SELECTION claim replays on SMALL (N=30/H=63 buys ~+4.66 pp of MaxDD "
         "and ~+0.70 pp of CAGR, both vs the anchor)",
         f"dMaxDD {s30.dMaxDD_pp:+.2f} pp, dCAGR {s30.dCAGR_pp:+.2f} pp",
         "|dev| <= 0.5 pp on each", abs(s30.dMaxDD_pp - 4.66) <= 0.5 and abs(s30.dCAGR_pp - 0.70) <= 0.5)
    e6 = G[(G.panel == "SMALL663") & (G.arm == "EXPOSURE") & (G.target == 0.06)].iloc[0]
    gate("G5 1297's EXPOSURE claim replays on SMALL (6%/21d reaches ~-22.43% for ~-2.58 pp "
         "of CAGR)", f"MaxDD {e6.MaxDD:.2%}, dCAGR {e6.dCAGR_pp:+.2f} pp",
         "|dev| <= 0.5 pp on each", abs(e6.MaxDD - (-0.2243)) <= 0.005 and abs(e6.dCAGR_pp - (-2.58)) <= 0.5)

    # ------------------------------------------------------------ full grid, every cell
    for p in panels:
        sub = G[G.panel == p.name]
        anc = sub[sub.arm == "ANCHOR"].iloc[0]
        say("")
        say(f"  ===== {p.name} — EVERY CELL (cap {DD_CAP*bm[p.name]['MaxDD']:.2%}, "
            f"floor {CAGR_FLOOR*bm[p.name]['CAGR']:.2%}; anchor {anc.CAGR:.2%} / "
            f"{anc.Sharpe:.4f} / {anc.MaxDD:.2%}) =====")
        say("     arm          N  TGT |    CAGR   Sharpe    MaxDD |     H1     H2 |  turn | k_mean"
            " k@cap |  4a 4bF 4bO | dMaxDD  dCAGR  price | resid")
        for _, x in sub.iterrows():
            tg = f"{x.target:.0%}" if x.target != "" else "  -"
            km = f"{x.k_mean:5.3f}" if "k_mean" in sub.columns and pd.notna(x.get("k_mean")) else "    -"
            kc = f"{x.k_at_cap:5.1%}" if "k_at_cap" in sub.columns and pd.notna(x.get("k_at_cap")) else "    -"
            rs = f"{x.additivity_resid_pp:+6.2f}" if pd.notna(x.get("additivity_resid_pp")) else "     -"
            say(f"    {x.arm:11s} {int(x.N):3d} {tg:>4s} | {x.CAGR:7.2%} {x.Sharpe:8.4f} "
                f"{x.MaxDD:8.2%} | {x.H1:6.3f} {x.H2:6.3f} | {x.turn:5.2f} | {km} {kc} | "
                f"{'Y' if x.keep4a else '.':>3s} {'Y' if x.keep4b_full else '.':>3s} "
                f"{'Y' if x.keep4b_oos else '.':>3s} | {x.dMaxDD_pp:+6.2f} {x.dCAGR_pp:+6.2f} "
                f"{x.price:6.2f} | {rs}")

    # ------------------------------------------------------------ the queue's question
    say("")
    say("=" * 104)
    say("THE QUEUE'S QUESTION 1 — DOES THE STACK CLOSE SMALL's 13.12 pp GAP TO THE -20.23% CAP?")
    say("=" * 104)
    for p in panels:
        cap = DD_CAP * bm[p.name]["MaxDD"]
        fl = CAGR_FLOOR * bm[p.name]["CAGR"]
        st = G[(G.panel == p.name) & (G.arm == "STACK")]
        best = st.loc[st.MaxDD.idxmax()]
        under = st[(st.MaxDD >= cap)]
        both = st[(st.MaxDD >= cap) & (st.CAGR >= fl)]
        say(f"  {p.name:9s} cap {cap:7.2%} floor {fl:6.2%} | shallowest STACK "
            f"N={int(best.N)}/TGT={best.target:.0%}: MaxDD {best.MaxDD:7.2%} "
            f"(miss {100*(cap-best.MaxDD):+.2f} pp), CAGR {best.CAGR:6.2%} | "
            f"cells clearing the CAP {len(under)}/{len(st)}, clearing CAP AND FLOOR "
            f"{len(both)}/{len(st)} | 4b full {int(st.keep4b_full.sum())}/{len(st)}, "
            f"4b OOS {int(st.keep4b_oos.sum())}/{len(st)}")
    say("")
    say("=" * 104)
    say("THE QUEUE'S QUESTION 2 — DO THE TWO INSTRUMENTS ADD OR SUBSTITUTE?")
    say("  resid = dMaxDD(stack) - [dMaxDD(selection) + dMaxDD(exposure)], pp vs the same anchor")
    say("=" * 104)
    for p in panels:
        st = G[(G.panel == p.name) & (G.arm == "STACK")]
        say(f"  {p.name:9s} resid mean {st.additivity_resid_pp.mean():+6.2f} pp, median "
            f"{st.additivity_resid_pp.median():+6.2f}, range [{st.additivity_resid_pp.min():+6.2f}, "
            f"{st.additivity_resid_pp.max():+6.2f}] | additive (|resid| <= 1 pp) "
            f"{int((st.additivity_resid_pp.abs() <= 1).sum())}/{len(st)} | substituting "
            f"(resid < -1 pp) {int((st.additivity_resid_pp < -1).sum())}/{len(st)}")
        say(f"            CAGR resid mean {st.cagr_resid_pp.mean():+6.2f} pp "
            f"[{st.cagr_resid_pp.min():+.2f}, {st.cagr_resid_pp.max():+.2f}]")
    sf = G[G.arm == "STACK_SELF"]
    say(f"  B_SELF robustness arm (all panels): resid mean "
        f"{sf.additivity_resid_pp.mean():+.2f} pp, 4b full {int(sf.keep4b_full.sum())}/{len(sf)}, "
        f"4b OOS {int(sf.keep4b_oos.sum())}/{len(sf)}")

    # ------------------------------------------------------------ RULE 8 walk-forward
    say("")
    say("=" * 104)
    say("RULE 8 WALK-FORWARD — (N, TARGET) chosen by argmax IS Sharpe on warm-up..2016-12-31; "
        "2017-2026 READ ONCE")
    say("=" * 104)
    wf = []
    for p in panels:
        bo, li = bm_oos[p.name], live_oos[p.name]
        for arm, pool in (("STACK", G[(G.panel == p.name) & (G.arm == "STACK")]),
                          ("STACK_SELF", G[(G.panel == p.name) & (G.arm == "STACK_SELF")]),
                          ("SELECTION", G[(G.panel == p.name) & (G.arm == "SELECTION")]),
                          ("EXPOSURE", G[(G.panel == p.name) & (G.arm == "EXPOSURE")])):
            pick = pool.loc[pool.IS_Sharpe.idxmax()]
            k4b_oos, mo = keep4b_window(series[(p.name, arm, pick.N, pick.target if pick.target != "" else None)][p.i_oos - p.lo:], bo)
            anc_oos = G[(G.panel == p.name) & (G.arm == "ANCHOR")].iloc[0]
            wf.append(dict(panel=p.name, arm=arm, pick_N=int(pick.N),
                           pick_target=pick.target, IS_Sharpe=pick.IS_Sharpe,
                           OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                           anchor_OOS_CAGR=anc_oos.OOS_CAGR, anchor_OOS_Sharpe=anc_oos.OOS_Sharpe,
                           anchor_OOS_MaxDD=anc_oos.OOS_MaxDD,
                           spy_OOS_CAGR=bo["CAGR"], spy_OOS_Sharpe=bo["Sharpe"], spy_OOS_MaxDD=bo["MaxDD"],
                           v2_OOS_CAGR=li["CAGR"], v2_OOS_Sharpe=li["Sharpe"], v2_OOS_MaxDD=li["MaxDD"],
                           oos_cap=DD_CAP * bo["MaxDD"], oos_floor=CAGR_FLOOR * bo["CAGR"],
                           keep4b_oos=k4b_oos,
                           dSharpe_vs_anchor=mo["Sharpe"] - anc_oos.OOS_Sharpe,
                           dCAGR_pp_vs_anchor=100 * (mo["CAGR"] - anc_oos.OOS_CAGR),
                           dMaxDD_pp_vs_anchor=100 * (mo["MaxDD"] - anc_oos.OOS_MaxDD)))
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    for p in panels:
        bo = bm_oos[p.name]
        say(f"  {p.name:9s} OOS SPY {bo['CAGR']:7.2%} / {bo['Sharpe']:.4f} / {bo['MaxDD']:7.2%}"
            f"  (cap {DD_CAP*bo['MaxDD']:7.2%}, floor {CAGR_FLOOR*bo['CAGR']:6.2%}) | "
            f"v2 {live_oos[p.name]['CAGR']:7.2%} / {live_oos[p.name]['Sharpe']:.4f} / "
            f"{live_oos[p.name]['MaxDD']:7.2%}")
        for _, x in W[W.panel == p.name].iterrows():
            tg = f"{x.pick_target:.0%}" if x.pick_target != "" else "  -"
            say(f"    {x.arm:11s} pick N={x.pick_N:3d} TGT={tg:>4s} (IS Sharpe {x.IS_Sharpe:.4f}) "
                f"-> OOS {x.OOS_CAGR:7.2%} / {x.OOS_Sharpe:.4f} / {x.OOS_MaxDD:7.2%} | "
                f"4b OOS {'PASS' if x.keep4b_oos else 'FAIL'} | vs anchor "
                f"{x.dCAGR_pp_vs_anchor:+6.2f} pp CAGR, {x.dSharpe_vs_anchor:+.4f} Sharpe, "
                f"{x.dMaxDD_pp_vs_anchor:+6.2f} pp MaxDD")

    # ------------------------------------------------------------ verdict
    say("")
    say("=" * 104)
    stS = G[(G.panel == "SMALL663") & (G.arm == "STACK")]
    capS = DD_CAP * bm["SMALL663"]["MaxDD"]
    flS = CAGR_FLOOR * bm["SMALL663"]["CAGR"]
    closed = int(((stS.MaxDD >= capS) & (stS.CAGR >= flS)).sum())
    n4b = int(G[G.arm == "STACK"].keep4b_full.sum())
    n4bo = int(G[G.arm == "STACK"].keep4b_oos.sum())
    n4a = int(G[G.arm == "STACK"].keep4a.sum())
    say(f"VERDICT INPUTS: SMALL stacked cells clearing BOTH 4b legs the queue named: "
        f"{closed}/{len(stS)}. STACK 4a {n4a}/{len(G[G.arm=='STACK'])}, 4b full "
        f"{n4b}/{len(G[G.arm=='STACK'])}, 4b OOS {n4bo}/{len(G[G.arm=='STACK'])} (all panels).")
    say("=" * 104)

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    say(f"done in {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
