#!/usr/bin/env python3
"""Idea 1277 (lane cloud, idea 2 of 2, 2026-09-18): does the INCUMBENT 4b BOOK have a COST RUNG
AT WHICH IT FAILS, and WHERE IS IT?

THE PREMISE.  Idea 1236 found the standing 2026-09-04 U56 book still clears every 4b leg at
50 bps (15.91% CAGR / 1.1003 Sharpe / -19.35% MaxDD against a -20.23% cap and a 10.70% floor),
five times PROTOCOL rule 2's rung, on 2.872 turns a year and 0.333 / 0.831 / 1.656 pp/yr of drag
at 10 / 25 / 50 bps.  Earlier today idea 1275 (this lane's first run) carried the proportional
ladder to 100 bps and solved the book's first 4b failure at 118 bps on the L_H1 leg.  What the
record still has no reading on is (i) the rungs ABOVE 100 bps leg by leg and (ii) whether the
answer survives a cost model that is not flat — the one a real account actually pays, where the
charge is wider on volatile names and widens further exactly when the book is losing money.

THE QUESTION, AND WHY IT MATTERS FOR CAPITAL.  Cost headroom is the single number a funded
account needs before it trades this book: it says how much slippage, spread and impact the edge
can absorb before the case for it stops being a case.  A headroom measured only under a FLAT
proportional charge is an assumption about market microstructure, not a measurement — flat cost
cannot express the one thing that matters in a drawdown, which is that spreads widen when
volatility spikes.  If the failing rung is the same under both models, the record's flat-cost
ladder is safe to quote; if the vol-scaled model brings the failure forward materially, every
committed cost headroom in the record is an artefact of the cost model's shape.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
    DIAL 1  COST RUNG = [0, 10, 25, 50, 75, 100, 150, 200] bps (the queue's own extension of the
            record's ladder), PLUS a FINE 0..400 bps curve at 1-bp resolution so every failing
            rung below is SOLVED and not interpolated.
    DIAL 2  COST MODEL:
            M_PROP      — the record's model: `cost_bps` on traded notional, flat across names
                          and time.
            M_VOLSPREAD — the SAME rung redistributed by each name's own volatility: name i's
                          charge at rebalance t is `c * clip(vol20[i,t] / median_j vol20[j,t],
                          0.25, 4.0)` bps of ITS traded notional.  The cross-sectional median is
                          the normaliser, so the rung keeps its meaning ("the cost of trading a
                          median-volatility name") and the model adds SHAPE, not level: it is a
                          half-spread proxy that is wider on volatile names and widens for the
                          whole book when volatility rises — which is when the book trades most.
                          The realised mean effective bps is published at every rung (gate G4)
                          so the level change the shape brings with it is visible and not
                          smuggled in, and setting the multiplier to 1 reproduces M_PROP bit for
                          bit (gate G5).
EVERY grid point is published in the .grid.csv and the fine per-leg solution in .failrung.csv.

THE OBJECT, AND ITS COMPARANDS.  The headline is the INCUMBENT: U56 / N=20 / min hold H=126 /
gross 0.75 / weekly — the standing 2026-09-04 KEEP 4b candidate.  Reported at every rung and
every model, NOT as dials: its own H ladder on U56 anchor A (9 rungs, so the incumbent's
headroom can be read against its neighbours'), U56 anchor B (N=12 / gross 0.55 / monthly) at
H = 63 and H = 252, and the SAME book construction on B136 and SMALL (rule 9).  SPY buy-and-hold
(costless at every rung — idea 1063's one-sided handicap, stated not hidden) and the live
RULES v2 book RE-RUN at the matched rung and model, so path 4a is charged symmetrically.

FROZEN AT THE RECORD'S CONSTRUCTION, not touched by this run: RAW three-leg composite
(21/252, 0/126, 0/63 percentile ranks), eligibility = above own 200d MA AND vol20 < 0.60, equal
weight gross/len(held), t+1 execution, 260-row warm-up, IS = warm-up..2016-12-31, OOS =
2017-01-01.. READ ONCE.  Neither dial ever enters the book's own decisions: the book is
cost-blind at every rung, exactly as the record's other cost ladders are.

PRE-DECLARED OUTCOMES, written before any number was read:
  (A) HEADROOM CONFIRMED AND MODEL-FREE — the incumbent's first failing rung is within a few bps
      under both models, i.e. the flat ladder is a fair summary of a shaped one.
  (B) MODEL-SENSITIVE — M_VOLSPREAD brings the first failure forward materially (> 15 bps),
      so every committed cost headroom in the record is a flat-cost artefact.
  (C) NO FAILURE INSIDE 400 bps — the book's 4b pass is cost-insensitive on any tradable
      assumption and the question is answered by the ladder running out.
  (D) ALREADY FAILING — the book does not clear 4b at 10 bps under one of the models, in which
      case the incumbent's committed pass is model-dependent and that is the headline.

RULE 8 (walk-forward, required).  At EVERY (cost rung, model) the H rung is chosen on
warm-up..2016-12-31 ALONE by three IS-only choosers (C_ISSHARPE, C_ISCAGR, C_ISDD) over U56
anchor A's nine rungs and 2017-2026 is READ ONCE; the pick is scored against the incumbent
H=126, the ladder mean, the ladder best and worst, and SPY.  The incumbent's own OOS CAGR /
Sharpe / MaxDD against the live baseline and SPY is reported at every rung of both models —
this run's step-3 deliverable.

GATES.  G1 the fast runner reproduces engine.backtest on the incumbent at 10 bps under M_PROP.
G2 CROSS-RUN replay of the committed U56 N=20 / H=126 triple on a tape truncated to the
committed vintage.  G3 CROSS-RUN agreement with THIS LANE's idea 1275 run committed earlier
today: the incumbent's M_PROP full triple at 0/10/25/50/100 bps must match its .grid.csv to
1e-9.  G4 M_VOLSPREAD's realised mean effective bps is published at every rung.  G5 M_VOLSPREAD
with the multiplier pinned to 1.0 IS M_PROP, bit for bit.  G6 within every book and model,
Sharpe and CAGR are non-increasing in the cost rung.  G7 the 0-bps cell IS the gross series
under both models.  G8 live RULES v2 MaxDD @10 bps == committed -12.05%.  G9 determinism.
G10 the vol multiplier is inside its declared clip [0.25, 4.0] at every rebalance.

PROTOCOL: rule 2 execution and the 10-bps rung reported with the ladder around it; rule 4 both
KEEP paths at every grid point; rule 5 one idea, one script, deterministic, standalone; rule 8
as above; rule 9 survivorship below.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py
are NOT modified by this script.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists and SMALL is a current
sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped first).  Every
absolute level is optimistic and every 4b pass is an UPPER bound, so a headroom measured here is
an UPPER bound on the live one: the names that would have been delisted are not in the panel to
be traded expensively on the way out.  The headline is a CONTRAST between cost rungs and cost
models on the same book and the same tape, first-order immune to a level bias that moves all
rungs together; the 4a / 4b legs and the failing rungs themselves are not.

Runs standalone and offline (committed price caches only).
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
SLUG = "does-the-INCUMBENT-4b-BOOK-have-a-COST-RUNG-AT-WHICH-IT-FAILS-and-where-is-it"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_cloud"
PRIOR = ROOT / "research" / "backtests" / (
    "2026-09-18_is-the-H-LADDER-s-FAST-RUNG-the-ONLY-PLACE-THE-RECORD-s-COST-SENSITIVITY-LIVES"
    "_cloud.grid.csv")

# ---- frozen construction (NOT dials) --------------------------------------------------------
LAG = 1
WARMUP = 260
MAXVOL = 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
CHOOSERS = ["C_ISSHARPE", "C_ISCAGR", "C_ISDD"]
ANCHORS = {"A": dict(N=20, gross=0.75, cadence="W", H=126),
           "B": dict(N=12, gross=0.55, cadence="M", H=63)}
LAD_H = [5, 10, 21, 42, 63, 90, 126, 189, 252]
INCUMBENT_H = 126

# ---- the two dials ---------------------------------------------------------------------------
RUNGS = [0.0, 10.0, 25.0, 50.0, 75.0, 100.0, 150.0, 200.0]
FINE = np.arange(0.0, 401.0, 1.0)
MODELS = ["M_PROP", "M_VOLSPREAD"]
VCLIP = (0.25, 4.0)

# ---- committed cross-run constants ----------------------------------------------------------
A936_WH126 = (0.155787, 1.139701, -0.191276)
LIVE_MAXDD_COMMITTED = -0.1205
COMMIT_TAPE_END = "2026-09-15"

_LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    say(f"   GATE {name}: {value} vs {target} -> {'PASS' if ok else 'FAIL'}")
    return bool(ok)


def dump(df, suffix):
    p = Path(f"{STEM}.{suffix}.csv")
    df.to_csv(p, index=False)
    say(f"   wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ------------------------------------------------------------------ metrics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    return float(np.prod(1.0 + r) ** (252.0 / len(r)) - 1.0)


def mdd(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1.0).min())


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def windows_of(r, i_oos):
    n = len(r)
    h = n // 2
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]),
                is_=stats(r[:i_oos]), oos=stats(r[i_oos:]))


def flat(w):
    return {f"{k}_{m}": v for k, d in w.items() for m, v in d.items()}


def rankcorr(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return float("nan")
    ra, rb = pd.Series(a[ok]).rank().values, pd.Series(b[ok]).rank().values
    sa, sb = ra.std(ddof=0), rb.std(ddof=0)
    if sa == 0 or sb == 0:
        return float("nan")
    return float(((ra - ra.mean()) * (rb - rb.mean())).mean() / (sa * sb))


# ------------------------------------------------------------------ book machinery (1095's)
def mech(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, (above & (vol20 < MAXVOL)).values, vol20.values


def build(rank_key, elig, priced, reb, N, H, T, K, gross, banned):
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    for i, t in enumerate(reb):
        held = np.flatnonzero(cur >= 0)
        if len(held):
            young = held[(t - cur[held]) < H]
            young = young[priced[t, young]]
        else:
            young = held
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = rank_key[t].copy()
            k[~(elig[t] & priced[t])] = np.inf
            k[banned] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new_cur = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new_cur[c] = cur[c]
        for c in take:
            new_cur[c] = t
        cur = new_cur
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = gross / len(sel)
    return W


def lagmat(a):
    out = np.zeros_like(a)
    out[LAG:] = a[:-LAG]
    return out


def nrun(rets, wt, mk, mult):
    """1095's fast runner, with the per-name traded notional charged through a MULTIPLIER matrix.
    Returns gross returns, the flat turnover series (M_PROP) and the multiplier-weighted one."""
    T, N = rets.shape
    mk = mk.copy()
    mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    traded = np.abs(wt[reb] - heldp[reb])                 # per-name traded notional, NAV units
    turn = np.zeros(T)
    turn_v = np.zeros(T)
    turn[reb] = traded.sum(axis=1)
    turn_v[reb] = (traded * mult[reb]).sum(axis=1)
    return (held * rets).sum(axis=1), turn, turn_v


# ------------------------------------------------------------------ KEEP paths
def legs_4a(bk, live):
    return dict(A_H1=bk["h1"]["Sharpe"] > live["h1"]["Sharpe"],
                A_H2=bk["h2"]["Sharpe"] > live["h2"]["Sharpe"],
                A_DD=bk["full"]["MaxDD"] >= live["full"]["MaxDD"])


def legs_4b(bk, spy):
    return dict(L_H1=bk["h1"]["Sharpe"] > spy["h1"]["Sharpe"],
                L_H2=bk["h2"]["Sharpe"] > spy["h2"]["Sharpe"],
                L_OOS=bk["oos"]["Sharpe"] > spy["oos"]["Sharpe"],
                L_DD=abs(bk["full"]["MaxDD"]) <= DD_CAP * abs(spy["full"]["MaxDD"]),
                L_CAGR=bk["full"]["CAGR"] >= CAGR_FLOOR * spy["full"]["CAGR"])


def failed(d):
    return ",".join(k for k, v in d.items() if not v) or "-"


def stat_of(chooser, w):
    return {"C_ISSHARPE": w["is_"]["Sharpe"], "C_ISCAGR": w["is_"]["CAGR"],
            "C_ISDD": w["is_"]["MaxDD"]}[chooser]


def fail_rungs(gr, tn, i_oos, spy_w, live_by_cost):
    """Lowest FINE rung at which each 4b leg, the whole of 4b, and each 4a leg first fails."""
    seen = {}
    for c in FINE:
        r = (gr - tn * c / 1e4)[WARMUP:]
        w = windows_of(r, i_oos - WARMUP)
        b4 = legs_4b(w, spy_w)
        a4 = legs_4a(w, live_by_cost(c))
        for k, v in list(b4.items()) + list(a4.items()) + [("ALL_4b", all(b4.values())),
                                                           ("ALL_4a", all(a4.values()))]:
            seen.setdefault(k, []).append(v)
    out = {}
    for k, v in seen.items():
        v = np.array(v, bool)
        if not v[0]:
            out[k] = 0.0
        elif (~v).any():
            out[k] = float(FINE[int(np.flatnonzero(~v)[0])])
        else:
            out[k] = float("nan")
    return out


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say(f"# {DATE} idea 1277 lane cloud (idea 2 of 2) — {SLUG}")
    say(f"# DIAL 1 COST RUNG = {[int(c) for c in RUNGS]} bps (+ a FINE 0..{int(FINE[-1])} bps "
        f"curve at 1-bp resolution, published)")
    say(f"# DIAL 2 COST MODEL = {MODELS}; M_VOLSPREAD charges name i at c * clip(vol20_i / "
        f"median_j vol20_j, {VCLIP[0]}, {VCLIP[1]}) bps of ITS traded notional")
    say("# HEADLINE OBJECT: the standing 2026-09-04 book = U56 / N=20 / H=126 / gross 0.75 / weekly")
    say("# reported-not-dials: U56 anchor A's 9-rung H ladder, U56 anchor B (N12/gross0.55/M) at "
        "H=63 and H=252, the same book on B136 and SMALL; SPY (costless); live RULES v2 at the "
        "matched rung AND model")
    say("# PRE-DECLARED: (A) headroom model-free / (B) model-sensitive (>15 bps) / (C) no failure "
        "inside 400 bps / (D) already failing at 10 bps")

    gridrows, failrows, r8rows, modelrows = [], [], [], []
    prior = pd.read_csv(PRIOR) if PRIOR.exists() else None

    PANELS = [("U56", ["A", "B"], LAD_H), ("B136", ["A"], [INCUMBENT_H]),
              ("SMALL", ["A"], [INCUMBENT_H])]

    for pi, (panel, anchors, holds) in enumerate(PANELS):
        if panel == "SMALL":
            px = load_universe(small=True)
            meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
            bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
            drop = [c for c in px.columns if c in bad]
            px = px.drop(columns=drop)
            say(f"\n## SMALL: {len(drop)} tickers dropped for max_1d_move >= 1.0")
        else:
            px = load_universe(broad=(panel == "B136"))
        px = px.dropna(how="all").ffill()
        idx = px.index
        T, K = len(idx), len(px.columns)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        sc, elig, vol20 = mech(px)
        rank_key = -np.nan_to_num(sc, nan=-np.inf)
        rank_key[np.isnan(sc)] = np.inf
        i_oos = int(idx.searchsorted(OOS_START))
        pname = {"U56": "U56", "B136": f"B{K-1}", "SMALL": f"SMALL{K-1}"}[panel]
        yrs = (len(idx) - WARMUP) / 252.0
        banned = np.zeros(K, bool)
        if panel == "SMALL":
            banned[list(px.columns).index("SPY")] = True
        spy_r = px["SPY"].pct_change().fillna(0.0).values
        sw = windows_of(spy_r[WARMUP:], i_oos - WARMUP)

        # ---- the M_VOLSPREAD multiplier: each name's vol20 over the cross-sectional median
        med = np.nanmedian(np.where(np.isfinite(vol20), vol20, np.nan), axis=1)
        with np.errstate(invalid="ignore", divide="ignore"):
            mult = vol20 / med[:, None]
        mult = np.where(np.isfinite(mult), mult, 1.0)
        mult = np.clip(mult, VCLIP[0], VCLIP[1])
        ONES = np.ones_like(mult)

        say(f"\n## {pname}  n_days={T}  n_cols={K}  {idx[0].date()}..{idx[-1].date()}  OOS row {i_oos}")
        say(f"   SPY (costless at every rung)  full {sw['full']['CAGR']:7.2%} / "
            f"{sw['full']['Sharpe']:.4f} / {sw['full']['MaxDD']:7.2%}   halves "
            f"{sw['h1']['Sharpe']:.4f}/{sw['h2']['Sharpe']:.4f}   OOS {sw['oos']['CAGR']:7.2%} / "
            f"{sw['oos']['Sharpe']:.4f} / {sw['oos']['MaxDD']:7.2%}")
        say(f"   4b bars: DD cap {DD_CAP*sw['full']['MaxDD']:.4%}   CAGR floor "
            f"{CAGR_FLOOR*sw['full']['CAGR']:.4%}   Sharpe H1 {sw['h1']['Sharpe']:.4f} "
            f"H2 {sw['h2']['Sharpe']:.4f} OOS {sw['oos']['Sharpe']:.4f}")
        gate(f"G10 vol multiplier inside its declared clip ({pname})",
             f"[{mult.min():.4f}, {mult.max():.4f}], median {np.median(mult):.4f}",
             f"[{VCLIP[0]}, {VCLIP[1]}]", bool(mult.min() >= VCLIP[0] and mult.max() <= VCLIP[1]))

        # live RULES v2 at the matched rung (M_PROP only: the live book is the record's own
        # comparand and its weights function is not this run's object)
        # the live comparand is run ONCE at 0 bps and re-charged arithmetically at every rung:
        # engine.backtest's returns are gross - turnover * cost/1e4 (engine.py:50), so this is an
        # identity, not an approximation (gate G11 checks it against a direct 10-bps run).
        _lb = backtest(px, rules_v2_weights(px), cost_bps=0.0, freq="W")
        LGR = _lb["returns"].fillna(0.0).values
        LTN = _lb["turnover"].fillna(0.0).values
        live_cache: dict[float, dict] = {}

        def live_at(c):
            c = float(c)
            if c not in live_cache:
                live_cache[c] = windows_of((LGR - LTN * c / 1e4)[WARMUP:], i_oos - WARMUP)
            return live_cache[c]

        live_w = {}

        for c in RUNGS:
            live_w[c] = live_at(c)
        say("   RULES v2 (live) by rung: " + "  ".join(
            f"{int(c)}bps {live_w[c]['full']['Sharpe']:.4f}/{live_w[c]['full']['MaxDD']:.2%}"
            for c in RUNGS))
        if pi == 0:
            _direct = backtest(px, rules_v2_weights(px), cost_bps=10.0, freq="W")["returns"].fillna(0.0).values
            d11 = float(np.abs(_direct - (LGR - LTN * 10.0 / 1e4)).max())
            gate("G11 the re-charged live comparand IS a direct 10-bps engine run", f"{d11:.3e}",
                 "< 1e-15", d11 < 1e-15)
            gate("G8 live RULES v2 MaxDD @10bps == committed -12.05%",
                 f"{live_w[10.0]['full']['MaxDD']:.4f}", f"{LIVE_MAXDD_COMMITTED} < 5e-4",
                 abs(live_w[10.0]["full"]["MaxDD"] - LIVE_MAXDD_COMMITTED) < 5e-4)

        masks = {cd: rebalance_mask(idx, cd).values for cd in ("W", "M")}
        cache: dict[tuple, tuple] = {}

        def bookpair(anchor, H):
            a = ANCHORS[anchor]
            key = (anchor, H)
            if key not in cache:
                m = masks[a["cadence"]]
                Wm = build(rank_key, elig, priced, np.flatnonzero(m), a["N"], H, T, K,
                           a["gross"], banned)
                gr, tn, tnv = nrun(rets, lagmat(Wm), np.roll(m, LAG), mult)
                cache[key] = (gr, tn, tnv)
            return cache[key]

        if pi == 0:
            gr, tn, tnv = bookpair("A", INCUMBENT_H)
            m = masks["W"]
            Wm = build(rank_key, elig, priced, np.flatnonzero(m), 20, INCUMBENT_H, T, K, 0.75, banned)
            eng = backtest(px, pd.DataFrame(Wm, index=idx, columns=px.columns),
                           cost_bps=10.0, freq="W")["returns"].values
            r10 = gr - tn * 10.0 / 1e4
            d1 = float(np.nanmax(np.abs(np.asarray(eng[WARMUP:], float) - r10[WARMUP:])))
            gate("G1 fast runner == engine.backtest (incumbent, 10 bps, M_PROP)", f"{d1:.3e}",
                 "< 1e-12", d1 < 1e-12)
            itr = int(idx.searchsorted(pd.Timestamp(COMMIT_TAPE_END), side="right"))
            wt = windows_of(r10[WARMUP:itr], i_oos - WARMUP)
            d2 = max(abs((wt["full"]["CAGR"], wt["full"]["Sharpe"], wt["full"]["MaxDD"])[i] - A936_WH126[i])
                     for i in range(3))
            gate(f"G2 CROSS-RUN incumbent triple (tape to {COMMIT_TAPE_END})",
                 f"{wt['full']['CAGR']:.6f}/{wt['full']['Sharpe']:.6f}/{wt['full']['MaxDD']:.6f} "
                 f"maxdiff {d2:.2e}", f"{A936_WH126} < 5e-4", d2 < 5e-4)
            _, tn_a, tnv_a = nrun(rets, lagmat(Wm), np.roll(m, LAG), ONES)
            d5 = float(np.abs(tn_a - tnv_a).max())
            gate("G5 M_VOLSPREAD with the multiplier pinned to 1.0 IS M_PROP", f"{d5:.3e}",
                 "== 0.0", d5 == 0.0)
            g7 = max(float(np.abs((gr - tn * 0.0) - gr).max()),
                     float(np.abs((gr - tnv * 0.0) - gr).max()))
            gate("G7 the 0-bps cell IS the gross series under both models", f"{g7:.3e}", "== 0.0",
                 g7 == 0.0)
            cache.pop(("A", INCUMBENT_H))
            gr2, _, _ = bookpair("A", INCUMBENT_H)
            gate("G9 determinism (incumbent recomputes bit for bit)",
                 f"{float(np.abs(gr - gr2).max()):.3e}", "== 0.0",
                 float(np.abs(gr - gr2).max()) == 0.0)

        for anchor in anchors:
            a = ANCHORS[anchor]
            hs = holds if anchor == "A" else ([63, 252] if panel == "U56" else [a["H"]])
            for H in hs:
                gr, tn, tnv = bookpair(anchor, H)
                tns = {"M_PROP": tn, "M_VOLSPREAD": tnv}
                eff = float(tnv[WARMUP:].sum() / max(tn[WARMUP:].sum(), 1e-12))
                is_incumbent = (panel == "U56" and anchor == "A" and H == INCUMBENT_H)
                if H == INCUMBENT_H or is_incumbent:
                    modelrows.append(dict(panel=pname, anchor=anchor, H=H, turn_yr=float(tn[WARMUP:].sum() / yrs),
                                          eff_bps_ratio=eff))
                    gate(f"G4 M_VOLSPREAD realised effective/nominal bps published ({pname} {anchor} H={H})",
                         f"{eff:.4f} (a book trading names {eff:.2f}x the panel median vol20, "
                         f"traded-notional weighted)", f"inside the clip {VCLIP}",
                         bool(VCLIP[0] <= eff <= VCLIP[1]))
                for model in MODELS:
                    t_ = tns[model]
                    for c in RUNGS:
                        r = (gr - t_ * c / 1e4)[WARMUP:]
                        w = windows_of(r, i_oos - WARMUP)
                        a4, b4 = legs_4a(w, live_w[c]), legs_4b(w, sw)
                        drag = ((gr[WARMUP:].mean() - r.mean()) * 252) * 100
                        gridrows.append(dict(panel=pname, anchor=anchor, N=a["N"], gross=a["gross"],
                                             cadence=a["cadence"], H=H, model=model, cost_bps=c,
                                             incumbent=is_incumbent,
                                             turn_yr=float(tn[WARMUP:].sum() / yrs),
                                             eff_bps=c * eff if model == "M_VOLSPREAD" else c,
                                             drag_pp_yr=drag, **flat(w),
                                             keep4a=all(a4.values()), keep4b=all(b4.values()),
                                             fail4a=failed(a4), fail4b=failed(b4), **a4, **b4))
                    fr = fail_rungs(gr, t_, i_oos, sw, live_at)
                    failrows.append(dict(panel=pname, anchor=anchor, H=H, model=model,
                                         incumbent=is_incumbent,
                                         turn_yr=float(tn[WARMUP:].sum() / yrs),
                                         eff_bps_ratio=eff if model == "M_VOLSPREAD" else 1.0,
                                         **{f"fail_{k}": v for k, v in fr.items()}))

            # ---- rule 8 over U56 anchor A's ladder, at every (rung, model)
            if panel == "U56" and anchor == "A":
                books = {H: bookpair("A", H) for H in LAD_H}
                ai = LAD_H.index(INCUMBENT_H)
                for model in MODELS:
                    for c in RUNGS:
                        Wl = []
                        for H in LAD_H:
                            gr_, tn_, tnv_ = books[H]
                            t_ = tn_ if model == "M_PROP" else tnv_
                            Wl.append(windows_of((gr_ - t_ * c / 1e4)[WARMUP:], i_oos - WARMUP))
                        oos_S = np.array([w["oos"]["Sharpe"] for w in Wl])
                        is_S = np.array([w["is_"]["Sharpe"] for w in Wl])
                        rc = rankcorr(is_S, oos_S)
                        for ch in CHOOSERS:
                            vals = np.array([stat_of(ch, w) for w in Wl])
                            j = int(np.nanargmax(vals))
                            pw = Wl[j]
                            b4, a4 = legs_4b(pw, sw), legs_4a(pw, live_w[c])
                            r8rows.append(dict(panel=pname, anchor=anchor, model=model, cost_bps=c,
                                               chooser=ch, pick_H=LAD_H[j],
                                               reach_incumbent=int(j == ai),
                                               pick_OOS_S=oos_S[j], incumbent_OOS_S=oos_S[ai],
                                               delta_vs_incumbent=oos_S[j] - oos_S[ai],
                                               ladder_mean_OOS_S=float(np.nanmean(oos_S)),
                                               best_OOS_S=float(np.nanmax(oos_S)),
                                               worst_OOS_S=float(np.nanmin(oos_S)),
                                               spy_OOS_S=sw["oos"]["Sharpe"],
                                               pick_OOS_CAGR=pw["oos"]["CAGR"],
                                               pick_OOS_DD=pw["oos"]["MaxDD"],
                                               rank_IS_OOS=rc, keep4b=all(b4.values()),
                                               fail4b=failed(b4), keep4a=all(a4.values()),
                                               fail4a=failed(a4)))

        # ---- print the headline ladder for this panel's incumbent-construction book
        for anchor in anchors:
            for H in (holds if anchor == "A" else ([63, 252] if panel == "U56" else [ANCHORS[anchor]["H"]])):
                if not (H == INCUMBENT_H or (panel == "U56" and anchor == "B")):
                    continue
                for model in MODELS:
                    rows = [r for r in gridrows if r["panel"] == pname and r["anchor"] == anchor
                            and r["H"] == H and r["model"] == model]
                    say(f"\n   {pname} anchor {anchor} H={H} [{model}]  turnover "
                        f"{rows[0]['turn_yr']:.2f}/yr")
                    say("     cost |  eff bps |    CAGR   Sharpe    MaxDD |  H1/H2  |  OOS CAGR / "
                        "Sharpe / MaxDD | drag pp/yr | 4a 4b | fail4b")
                    for r in rows:
                        say(f"     {int(r['cost_bps']):4d} | {r['eff_bps']:8.1f} | "
                            f"{r['full_CAGR']:7.2%} {r['full_Sharpe']:8.4f} {r['full_MaxDD']:8.2%} | "
                            f"{r['h1_Sharpe']:.3f}/{r['h2_Sharpe']:.3f} | {r['oos_CAGR']:7.2%} / "
                            f"{r['oos_Sharpe']:.4f} / {r['oos_MaxDD']:7.2%} | {r['drag_pp_yr']:10.3f} | "
                            f"{'Y' if r['keep4a'] else 'n'}  {'Y' if r['keep4b'] else 'n'} | "
                            f"{r['fail4b']}")

    g = pd.DataFrame(gridrows)
    fr = pd.DataFrame(failrows)
    r8 = pd.DataFrame(r8rows)

    # G3 cross-run agreement with idea 1275, committed earlier today
    if prior is not None:
        me = g[(g.panel == "U56") & (g.anchor == "A") & (g.H == INCUMBENT_H) &
               (g.model == "M_PROP") & (g.cost_bps.isin([0.0, 10.0, 25.0, 50.0, 100.0]))]
        th = prior[(prior.panel == "U56") & (prior.anchor == "A") & (prior.H == INCUMBENT_H) &
                   (prior.cost_bps.isin([0.0, 10.0, 25.0, 50.0, 100.0]))]
        j = me.merge(th, on="cost_bps", suffixes=("", "_1275"))
        d3 = float(max((j.full_CAGR - j.full_CAGR_1275).abs().max(),
                       (j.full_Sharpe - j.full_Sharpe_1275).abs().max(),
                       (j.full_MaxDD - j.full_MaxDD_1275).abs().max(),
                       (j.oos_Sharpe - j.oos_Sharpe_1275).abs().max()))
        gate("G3 CROSS-RUN agreement with idea 1275's committed grid (5 shared rungs)",
             f"{d3:.3e}", "< 1e-9", d3 < 1e-9)
    else:
        gate("G3 CROSS-RUN agreement with idea 1275's committed grid", "prior grid missing",
             "file present", False)

    # G6 monotone in cost, per (book, model)
    bad = []
    for k, s in g.groupby(["panel", "anchor", "H", "model"]):
        s = s.sort_values("cost_bps")
        if (s.full_Sharpe.diff().dropna() > 1e-12).any() or (s.full_CAGR.diff().dropna() > 1e-12).any():
            bad.append(k)
    gate("G6 Sharpe and CAGR non-increasing in the cost rung (every book x model)",
         f"{len(bad)} violations", "0", len(bad) == 0)

    dump(g, "grid")
    dump(fr, "failrung")
    dump(r8, "walkforward")
    dump(pd.DataFrame(modelrows), "effcost")
    dump(pd.DataFrame(GATES), "gates")

    say("\n" + "=" * 100)
    say("## ANSWER")
    inc = fr[fr.incumbent]
    for r in inc.itertuples():
        say(f"   INCUMBENT [{r.model}] effective/nominal bps {r.eff_bps_ratio:.4f}: whole 4b first "
            f"fails at {r.fail_ALL_4b} bps; legs H1 {r.fail_L_H1}, H2 {r.fail_L_H2}, "
            f"OOS {r.fail_L_OOS}, DD {r.fail_L_DD}, CAGR {r.fail_L_CAGR}; 4a {r.fail_ALL_4a}")
    if len(inc) == 2:
        P = inc[inc.model == "M_PROP"].iloc[0]
        V = inc[inc.model == "M_VOLSPREAD"].iloc[0]
        d = abs(float(P.fail_ALL_4b) - float(V.fail_ALL_4b))
        say(f"   MODEL SENSITIVITY in NOMINAL bps: the two models' first-failure rungs differ by "
            f"{d:.0f} bps -> outcome {'(B) MODEL-SENSITIVE' if d > 15 else '(A) HEADROOM MODEL-FREE'}")
        say("   THE SAME COMPARISON IN EFFECTIVE (ACTUALLY PAID) bps — nominal x the realised "
            f"{V.eff_bps_ratio:.4f} ratio, which separates the model's LEVEL from its SHAPE:")
        for leg in ["ALL_4b", "L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]:
            pv, vv = float(P[f"fail_{leg}"]), float(V[f"fail_{leg}"])
            ve = vv * V.eff_bps_ratio
            say(f"      {leg:7s}: M_PROP {pv:6.1f} bps | M_VOLSPREAD {vv:6.1f} nominal = "
                f"{ve:6.1f} effective | shape effect {ve - pv:+6.1f} bps ({(ve/pv-1)*100:+5.1f}%)")
    gi = g[g.incumbent]
    for model in MODELS:
        s = gi[gi.model == model]
        say(f"   INCUMBENT [{model}] 4b PASS at {int(s.keep4b.sum())}/{len(s)} published rungs, "
            f"4a at {int(s.keep4a.sum())}/{len(s)}; Sharpe "
            + ", ".join(f"{int(r.cost_bps)}:{r.full_Sharpe:.4f}" for r in s.itertuples()))
    say(f"   whole grid: {len(g)} books; 4b {int(g.keep4b.sum())}/{len(g)}, 4a {int(g.keep4a.sum())}/{len(g)}")
    for model in MODELS:
        s = g[g.model == model]
        say(f"      [{model}] 4b by rung: " + ", ".join(
            f"{int(c)}:{int(s[s.cost_bps == c].keep4b.sum())}/{len(s[s.cost_bps == c])}" for c in RUNGS))
    say(f"   fail-rung table: {len(fr)} (book, model) cells; whole-4b failures inside "
        f"{int(FINE[-1])} bps at {int(fr.fail_ALL_4b.notna().sum())}/{len(fr)}")
    say(f"   rule 8: {len(r8)} decisions; pick-minus-incumbent OOS Sharpe mean "
        f"{r8.delta_vs_incumbent.mean():+.4f}, positive {int((r8.delta_vs_incumbent > 0).sum())}/{len(r8)}, "
        f"reach (pick == incumbent) {int(r8.reach_incumbent.sum())}/{len(r8)}, "
        f"4b among picks {int(r8.keep4b.sum())}/{len(r8)}")
    for model in MODELS:
        s = r8[r8.model == model]
        say(f"      [{model}] delta {s.delta_vs_incumbent.mean():+.4f}, positive "
            f"{int((s.delta_vs_incumbent > 0).sum())}/{len(s)}, 4b {int(s.keep4b.sum())}/{len(s)}, "
            f"picks {sorted(set(s.pick_H))}")
    say(f"   gates: {sum(x['pass_'] for x in GATES)}/{len(GATES)} PASS "
        f"({', '.join(x['gate'].split()[0] for x in GATES if not x['pass_']) or 'none failed'})")
    say(f"   elapsed {time.time() - t0:.0f}s")
    Path(f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
