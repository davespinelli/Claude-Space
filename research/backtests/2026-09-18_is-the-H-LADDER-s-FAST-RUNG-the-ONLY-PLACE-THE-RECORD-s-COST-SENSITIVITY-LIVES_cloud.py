#!/usr/bin/env python3
"""Idea 1275 (lane cloud, idea 1 of 2, 2026-09-18): is the H LADDER's FAST RUNG the ONLY PLACE
the RECORD's COST SENSITIVITY LIVES?

THE PREMISE.  Idea 1236 found that the whole cost sensitivity of an anchor substitution is a
TAIL on ONE rung: H=21 turns 6.078 / 7.755 / 10.951 times a year on U56 / B136 / SMALL against
the anchor's 2.872 / 3.247 / 4.149, and pooled over its grid the 0 -> 10 bps move is worth only
+0.0004 of delta.  A min hold of 21 days is the one dial in the record whose verdict a realistic
cost assumption could flip, and nobody has priced it past PROTOCOL rule 2's 10 bps.

THE QUESTION, AND WHY IT MATTERS FOR CAPITAL.  Every committed H-ladder claim in the record is
read at 10 bps.  If the ladder's ORDER and its 4b verdicts are cost-inert up to a rung no real
account would pay, the record's H evidence is safe as written; if the fast rungs invert or lose
their passes somewhere inside a tradable spread, then every committed H claim is a 10-bps claim
and should be quoted with the rung it was read at.  The two readings imply different things for
a funded book: cost headroom, or a cost assumption doing the work.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
    DIAL 1  H (MIN-HOLD, trading days) = [5, 10, 21, 42, 63, 90, 126, 189, 252]
            — 1095's committed ladder; it CONTAINS {21, 63, 126} (gate G5) so this run is
            directly comparable with 1086/1095/1236/1260/1274's readings of the same rungs.
    DIAL 2  COST = [0, 10, 25, 50, 100] bps per unit turnover, the queue's own rungs.
EVERY grid point is published in the .grid.csv (3 panels x 2 anchors x 9 rungs x 5 costs = 270
books) and a FINE cost curve (0..200 bps in 1-bp steps) is published for every rung so the
crossing rungs below are solved rather than interpolated.

NOT DIALS, reported at every value: PANEL {U56, B136, SMALL} (rule 9); ANCHOR {A = N20 / gross
0.75 / weekly (the standing 2026-09-04 book, H_anchor = 126), B = N12 / gross 0.55 / monthly
(1260's second anchor, H_anchor = 63)}; both KEEP paths leg by leg; full / halves / IS / OOS
CAGR, Sharpe and MaxDD; annual turnover; and rule 8 at EVERY cost rung.

FROZEN AT THE RECORD'S CONSTRUCTION, not touched by this run: RAW three-leg composite
(21/252, 0/126, 0/63 percentile ranks), eligibility = above own 200d MA AND vol20 < 0.60,
equal weight gross/len(held), t+1 execution, 260-row warm-up, IS = warm-up..2016-12-31,
OOS = 2017-01-01.. READ ONCE.  The cost rung is charged on traded notional only; it never
enters the book's own decisions, exactly as the record's other cost ladders do.

THE ONE-SIDED COST HANDICAP, STATED BEFORE THE NUMBERS (idea 1063's finding, inherited).  SPY
buy-and-hold pays NO turnover at any rung, so as the cost dial rises the 4b bars stay put while
every book falls.  A 4b failure at 100 bps is therefore a statement about a book paying 100 bps
against a benchmark paying nothing, which is the conservative direction and is what a real
account faces if it trades this book against a held index fund.  The live RULES v2 comparand in
path 4a IS re-run at the matched cost rung, so 4a is charged symmetrically.

PRE-DECLARED OUTCOMES, written before any number was read:
  (A) FAST-RUNG-ONLY — the H=21/5/10 end is the only part of the ladder whose 4b verdict or
      rule-8 pick moves anywhere in 0..100 bps; the slow rungs are inert.  1236's reading holds
      and the record's H evidence is safe outside the fast end.
  (B) LADDER-WIDE — rungs at or above the anchor also lose 4b passes inside 100 bps; then cost
      is not a fast-rung fact and every committed H claim is a 10-bps claim.
  (C) INERT — nothing moves anywhere in 0..100 bps: the H ladder's verdicts do not depend on the
      cost rung at all and 1236's +0.0004 is the whole story.
  (D) EMPTY — H=21 is not reachable by any IS-only chooser even at 0 bps, so "the rung at which
      it stops being reachable" does not exist and the queue's question is answered by
      construction.
  These are not exclusive across panels and anchors; whichever fire are reported as they fall.

RULE 8 (walk-forward, required).  At EVERY cost rung and on every (panel, anchor): H is chosen
on warm-up..2016-12-31 ALONE by three IS-only choosers (C_ISSHARPE, C_ISCAGR, C_ISDD) and
2017-2026 is read ONCE.  Each pick is scored against (i) the anchor's own H, (ii) the ladder
mean, (iii) the ladder best and worst, and (iv) SPY, with the IS/OOS rank correlation over the
nine rungs.  The capital verdict is the SIGN of pick-minus-anchor, never the best cell.

"REACHABLE" IS DEFINED BEFORE IT IS MEASURED.  H=21 is REACHABLE at a cost rung iff at least
one of the three IS-only choosers picks it there (an out-of-sample-legal selection); its IS
Sharpe RANK among the nine rungs is published alongside, so a rung that is never picked is
distinguishable from one that is picked and then lost.

GATES.  G1 the fast runner reproduces engine.backtest on the U56 anchor A book at 10 bps.
G2 CROSS-RUN replay of the committed U56 N=20 / H=126 triple on a tape truncated to the
committed vintage.  G3 CROSS-RUN SPY OOS triple.  G4 live RULES v2 MaxDD == committed -12.05%.
G5 the ladder contains {21, 63, 126}.  G6 within every book Sharpe and CAGR are non-increasing
in the cost rung (an arithmetic identity; a violation means the cost is not being charged).
G7 the 0-bps cell equals the gross return series EXACTLY.  G8 turnover is non-increasing in H.
G9 determinism: the anchor book recomputes bit for bit.

PROTOCOL: rule 2 costs and execution (10 bps is the reported rung and the whole ladder is
published around it); rule 4 both KEEP paths at every grid point; rule 5 one idea, one script,
deterministic, standalone; rule 8 as above; rule 9 survivorship below.  RULES.md, PROTOCOL.md,
scan.py, bot.py and baseline.py are NOT modified by this script.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists and SMALL is a current
sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv are dropped before
anything is computed).  Every absolute level printed here is optimistic and every 4b pass is an
UPPER bound.  The headline is a CONTRAST between cost rungs applied to the same books on the
same tape, which is first-order immune to a level bias that moves all rungs together; the 4a /
4b legs and any reachability statement about a particular rung are not.

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
SLUG = "is-the-H-LADDER-s-FAST-RUNG-the-ONLY-PLACE-THE-RECORD-s-COST-SENSITIVITY-LIVES"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_cloud"

# ---- frozen construction (NOT dials) --------------------------------------------------------
LAG = 1
WARMUP = 260
MAXVOL = 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
IS_END = pd.Timestamp("2016-12-31")
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
CHOOSERS = ["C_ISSHARPE", "C_ISCAGR", "C_ISDD"]
PANELS = ["U56", "B136", "SMALL"]
ANCHORS = {"A": dict(N=20, gross=0.75, cadence="W", H=126),
           "B": dict(N=12, gross=0.55, cadence="M", H=63)}

# ---- the two dials ---------------------------------------------------------------------------
LAD_H = [5, 10, 21, 42, 63, 90, 126, 189, 252]
COSTS = [0.0, 10.0, 25.0, 50.0, 100.0]
FINE = np.arange(0.0, 201.0, 1.0)             # published cost curve, 1-bp resolution
FAST = 21                                     # the rung the queue asks about
COARSE = [21, 63, 126]

# ---- committed cross-run constants ----------------------------------------------------------
A936_WH126 = (0.155787, 1.139701, -0.191276)   # U56 N=20 H=126 @10 bps, committed 936/1082/1174
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
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
    return sc.values, (above & (vol20 < MAXVOL)).values


def build(rank_key, elig, priced, reb, N, H, T, K, gross, banned):
    """1082/1095's build(), unmodified except that `banned` columns can never be held (used to
    keep SPY out of the SMALL panel's investable set, where baseline.py documents it as a
    benchmark join and not a constituent)."""
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


def nrun(rets, wt, mk):
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
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return (held * rets).sum(axis=1), turn


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


def first_fail_cost(gr, tn, i_oos, spy_w, costs):
    """Lowest cost on the FINE ladder at which each 4b leg (and the whole of 4b) first fails.
    Returns a dict leg -> cost or nan when the leg never fails inside the ladder."""
    out = {}
    passes = {}
    for c in costs:
        r = (gr - tn * c / 1e4)[WARMUP:]
        w = windows_of(r, i_oos - WARMUP)
        b4 = legs_4b(w, spy_w)
        for k, v in b4.items():
            passes.setdefault(k, []).append(v)
        passes.setdefault("ALL", []).append(all(b4.values()))
    for k, v in passes.items():
        v = np.array(v, bool)
        if v[0] and (~v).any():
            out[k] = float(costs[int(np.flatnonzero(~v)[0])])
        elif not v[0]:
            out[k] = 0.0                      # already failing at 0 bps
        else:
            out[k] = float("nan")             # never fails inside the ladder
    return out


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say(f"# {DATE} idea 1275 lane cloud (idea 1 of 2) — {SLUG}")
    say(f"# DIAL 1 H = {LAD_H}   DIAL 2 COST = {[int(c) for c in COSTS]} bps "
        f"(+ a FINE 0..{int(FINE[-1])} bps curve at 1-bp resolution, published)")
    say(f"# anchors: A = N20/gross0.75/W (H_anchor 126, the 2026-09-04 book); "
        f"B = N12/gross0.55/M (H_anchor 63, 1260's second anchor)")
    say(f"# frozen: legs {LEGS}, elig above-200d & vol20<{MAXVOL}, equal weight, t+{LAG}, "
        f"warm-up {WARMUP}, IS end {IS_END.date()}, OOS read once")
    say("# SPY pays NO turnover at any rung (idea 1063's one-sided handicap, stated not hidden); "
        "the live RULES v2 4a comparand IS re-run at the matched cost rung")
    say("# PRE-DECLARED: (A) fast-rung-only / (B) ladder-wide / (C) inert / (D) empty")
    gate("G5 the 9-rung ladder CONTAINS {21,63,126}", COARSE, "all in " + str(LAD_H),
         all(h in LAD_H for h in COARSE))

    gridrows, r8rows, reachrows, curverows = [], [], [], []

    for pi, panel in enumerate(PANELS):
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
        sc, elig = mech(px)
        rank_key = -np.nan_to_num(sc, nan=-np.inf)
        rank_key[np.isnan(sc)] = np.inf
        i_oos = int(idx.searchsorted(OOS_START))
        pname = {"U56": "U56", "B136": f"B{K-1}", "SMALL": f"SMALL{K-1}"}[panel]
        yrs = (len(idx) - WARMUP) / 252.0
        # SPY is a benchmark join on the SMALL panel (baseline.py), so it is never investable
        # there; on U56 / B136 it is a listed constituent of the panel and stays investable.
        banned = np.zeros(K, bool)
        if panel == "SMALL":
            banned[list(px.columns).index("SPY")] = True
        spy_r = px["SPY"].pct_change().fillna(0.0).values
        sw = windows_of(spy_r[WARMUP:], i_oos - WARMUP)
        say(f"\n## {pname}  n_days={T}  n_cols={K}  {idx[0].date()}..{idx[-1].date()}  OOS row {i_oos}")
        say(f"   SPY (costless at every rung)  full {sw['full']['CAGR']:7.2%} / "
            f"{sw['full']['Sharpe']:.4f} / {sw['full']['MaxDD']:7.2%}   halves "
            f"{sw['h1']['Sharpe']:.4f}/{sw['h2']['Sharpe']:.4f}   OOS {sw['oos']['CAGR']:7.2%} / "
            f"{sw['oos']['Sharpe']:.4f} / {sw['oos']['MaxDD']:7.2%}")
        say(f"   4b bars: DD cap {DD_CAP*sw['full']['MaxDD']:.4%}   CAGR floor "
            f"{CAGR_FLOOR*sw['full']['CAGR']:.4%}   Sharpe H1 {sw['h1']['Sharpe']:.4f} "
            f"H2 {sw['h2']['Sharpe']:.4f} OOS {sw['oos']['Sharpe']:.4f}")

        live_w = {}
        for c in COSTS:
            lr = backtest(px, rules_v2_weights(px), cost_bps=c, freq="W")["returns"].fillna(0.0).values
            live_w[c] = windows_of(lr[WARMUP:], i_oos - WARMUP)
        say("   RULES v2 (live) by cost rung: " + "  ".join(
            f"{int(c)}bps {live_w[c]['full']['Sharpe']:.4f}/{live_w[c]['full']['MaxDD']:.2%}"
            for c in COSTS))

        masks = {cd: rebalance_mask(idx, cd).values for cd in ("W", "M")}
        cache: dict[tuple, tuple] = {}

        def book(anchor, H):
            a = ANCHORS[anchor]
            key = (anchor, H)
            if key not in cache:
                m = masks[a["cadence"]]
                reb = np.flatnonzero(m)
                Wm = build(rank_key, elig, priced, reb, a["N"], H, T, K, a["gross"], banned)
                gr, tn = nrun(rets, lagmat(Wm), np.roll(m, LAG))
                cache[key] = (gr, tn)
            return cache[key]

        if pi == 0:
            gr, tn = book("A", 126)
            r10 = gr - tn * 10.0 / 1e4
            m = masks["W"]
            Wm = build(rank_key, elig, priced, np.flatnonzero(m), 20, 126, T, K, 0.75, banned)
            eng = backtest(px, pd.DataFrame(Wm, index=idx, columns=px.columns),
                           cost_bps=10.0, freq="W")["returns"].values
            d1 = float(np.nanmax(np.abs(np.asarray(eng[WARMUP:], float) - r10[WARMUP:])))
            gate("G1 fast runner == engine.backtest (U56 anchor A, N=20 H=126, 10 bps)",
                 f"{d1:.3e}", "< 1e-12", d1 < 1e-12)
            itr = int(idx.searchsorted(pd.Timestamp(COMMIT_TAPE_END), side="right"))
            wt = windows_of(r10[WARMUP:itr], i_oos - WARMUP)
            d2 = max(abs((wt["full"]["CAGR"], wt["full"]["Sharpe"], wt["full"]["MaxDD"])[i] - A936_WH126[i])
                     for i in range(3))
            gate(f"G2 CROSS-RUN U56 N=20 H=126 @10bps triple (tape to {COMMIT_TAPE_END})",
                 f"{wt['full']['CAGR']:.6f}/{wt['full']['Sharpe']:.6f}/{wt['full']['MaxDD']:.6f} "
                 f"maxdiff {d2:.2e}", f"{A936_WH126} < 5e-4", d2 < 5e-4)
            swt = windows_of(spy_r[WARMUP:itr], i_oos - WARMUP)
            d3 = max(abs((swt["oos"]["CAGR"], swt["oos"]["Sharpe"], swt["oos"]["MaxDD"])[i] - SPY_OOS_COMMITTED[i])
                     for i in range(3))
            gate(f"G3 CROSS-RUN SPY OOS triple (tape to {COMMIT_TAPE_END})",
                 f"{swt['oos']['CAGR']:.4f}/{swt['oos']['Sharpe']:.4f}/{swt['oos']['MaxDD']:.4f} "
                 f"maxdiff {d3:.2e}", f"{SPY_OOS_COMMITTED} < 5e-4", d3 < 5e-4)
            gate("G4 live RULES v2 MaxDD @10bps == committed -12.05%",
                 f"{live_w[10.0]['full']['MaxDD']:.4f}", f"{LIVE_MAXDD_COMMITTED} < 5e-4",
                 abs(live_w[10.0]["full"]["MaxDD"] - LIVE_MAXDD_COMMITTED) < 5e-4)
            g7 = float(np.abs((gr - tn * 0.0 / 1e4) - gr).max())
            gate("G7 the 0-bps cell IS the gross series", f"{g7:.3e}", "== 0.0", g7 == 0.0)
            gr2, _ = book("A", 126)
            cache.pop(("A", 126))
            gr3, _ = book("A", 126)
            g9 = float(np.abs(gr2 - gr3).max())
            gate("G9 determinism (anchor A book recomputes bit for bit)", f"{g9:.3e}", "== 0.0",
                 g9 == 0.0)

        for anchor, a in ANCHORS.items():
            say(f"\n   --- anchor {anchor}: N={a['N']} gross={a['gross']} cadence={a['cadence']} "
                f"H_anchor={a['H']}")
            grs = {H: book(anchor, H) for H in LAD_H}
            tn_yr = {H: float(grs[H][1][WARMUP:].sum() / yrs) for H in LAD_H}
            d = np.diff([tn_yr[H] for H in LAD_H])
            gate(f"G8 turnover non-increasing in H ({pname} anchor {anchor})",
                 f"max positive step {float(d.max()):+.4f}/yr", "<= 1e-9", bool(d.max() <= 1e-9))
            say("   turnover/yr by H: " + "  ".join(f"{H}:{tn_yr[H]:.2f}" for H in LAD_H))

            # --------- the 5-rung published grid
            Wc: dict[tuple, dict] = {}
            for c in COSTS:
                say(f"\n     cost {int(c):3d} bps |     H |    CAGR   Sharpe    MaxDD |  H1/H2  |"
                    "  OOS Sh | turn | 4a 4b | fail4b")
                for H in LAD_H:
                    gr, tn = grs[H]
                    r = (gr - tn * c / 1e4)[WARMUP:]
                    w = windows_of(r, i_oos - WARMUP)
                    Wc[(c, H)] = w
                    a4, b4 = legs_4a(w, live_w[c]), legs_4b(w, sw)
                    gridrows.append(dict(panel=pname, anchor=anchor, N=a["N"], gross=a["gross"],
                                         cadence=a["cadence"], H=H, cost_bps=c,
                                         turn_yr=tn_yr[H], **flat(w),
                                         keep4a=all(a4.values()), keep4b=all(b4.values()),
                                         fail4a=failed(a4), fail4b=failed(b4), **a4, **b4))
                    say(f"                  | {H:5d} | {w['full']['CAGR']:7.2%} "
                        f"{w['full']['Sharpe']:8.4f} {w['full']['MaxDD']:8.2%} | "
                        f"{w['h1']['Sharpe']:.3f}/{w['h2']['Sharpe']:.3f} | "
                        f"{w['oos']['Sharpe']:7.4f} | {tn_yr[H]:4.2f} | "
                        f"{'Y' if all(a4.values()) else 'n'}  {'Y' if all(b4.values()) else 'n'} | "
                        f"{failed(b4)}")

                # G6 monotone in cost, checked once per (panel, anchor) at the end
            for H in LAD_H:
                s = [Wc[(c, H)]["full"]["Sharpe"] for c in COSTS]
                g = [Wc[(c, H)]["full"]["CAGR"] for c in COSTS]
                ok = all(s[i + 1] <= s[i] + 1e-12 for i in range(len(s) - 1)) and \
                     all(g[i + 1] <= g[i] + 1e-12 for i in range(len(g) - 1))
                if not ok:
                    gate(f"G6 Sharpe/CAGR non-increasing in cost ({pname} {anchor} H={H})",
                         f"S {['%.4f' % x for x in s]}", "monotone down", False)
            gate(f"G6 Sharpe and CAGR non-increasing in cost at all 9 rungs ({pname} {anchor})",
                 "checked", "monotone down",
                 all(all(Wc[(COSTS[i + 1], H)]["full"]["Sharpe"] <= Wc[(COSTS[i], H)]["full"]["Sharpe"] + 1e-12
                         for i in range(len(COSTS) - 1)) for H in LAD_H))

            # --------- rule 8 at every cost rung
            ai = LAD_H.index(a["H"])
            for c in COSTS:
                Wl = [Wc[(c, H)] for H in LAD_H]
                oos_S = np.array([w["oos"]["Sharpe"] for w in Wl])
                is_S = np.array([w["is_"]["Sharpe"] for w in Wl])
                rc = rankcorr(is_S, oos_S)
                picks = {}
                for ch in CHOOSERS:
                    vals = np.array([stat_of(ch, w) for w in Wl])
                    j = int(np.nanargmax(vals))
                    picks[ch] = LAD_H[j]
                    pw = Wl[j]
                    b4, a4 = legs_4b(pw, sw), legs_4a(pw, live_w[c])
                    r8rows.append(dict(panel=pname, anchor=anchor, cost_bps=c, chooser=ch,
                                       pick_H=LAD_H[j], anchor_H=a["H"], reach_anchor=int(j == ai),
                                       pick_is_FAST=int(LAD_H[j] == FAST),
                                       pick_OOS_S=oos_S[j], anchor_OOS_S=oos_S[ai],
                                       delta_vs_anchor=oos_S[j] - oos_S[ai],
                                       ladder_mean_OOS_S=float(np.nanmean(oos_S)),
                                       best_OOS_S=float(np.nanmax(oos_S)),
                                       worst_OOS_S=float(np.nanmin(oos_S)),
                                       spy_OOS_S=sw["oos"]["Sharpe"],
                                       pick_OOS_CAGR=pw["oos"]["CAGR"], pick_OOS_DD=pw["oos"]["MaxDD"],
                                       anchor_OOS_CAGR=Wl[ai]["oos"]["CAGR"],
                                       anchor_OOS_DD=Wl[ai]["oos"]["MaxDD"],
                                       spy_OOS_CAGR=sw["oos"]["CAGR"], spy_OOS_DD=sw["oos"]["MaxDD"],
                                       rank_IS_OOS=rc, keep4b=all(b4.values()), fail4b=failed(b4),
                                       keep4a=all(a4.values()), fail4a=failed(a4)))
                say(f"     rule8 @{int(c):3d} bps: " + "  ".join(
                    f"{ch.replace('C_IS','')}->H{picks[ch]}" for ch in CHOOSERS) +
                    f"   anchor H{a['H']} OOS S {oos_S[ai]:.4f}   IS/OOS rank corr {rc:+.4f}")

            # --------- the fast rung: reachability and the crossing costs
            jf = LAD_H.index(FAST)
            reach_by_cost, rank_by_cost = {}, {}
            for c in COSTS:
                Wl = [Wc[(c, H)] for H in LAD_H]
                picked = [LAD_H[int(np.nanargmax([stat_of(ch, w) for w in Wl]))] for ch in CHOOSERS]
                reach_by_cost[c] = FAST in picked
                is_S = np.nan_to_num(np.array([w["is_"]["Sharpe"] for w in Wl]), nan=-1e9)
                rank_by_cost[c] = int(1 + (is_S > is_S[jf]).sum())   # 1 = best IS Sharpe
            # the queue's own question, solved on the FINE ladder rather than the 5 rungs:
            # the cost at which H=21 stops being picked by ANY IS-only chooser, ever again.
            isl = slice(WARMUP, i_oos)
            fine_reach = []
            for c in FINE:
                vals = []
                for H in LAD_H:
                    gr, tn = grs[H]
                    r = (gr - tn * c / 1e4)[isl]
                    vals.append((sharpe(r), cagr(r), mdd(r)))
                V = np.array(vals, float)
                picked = {LAD_H[int(np.nanargmax(V[:, k]))] for k in range(3)}
                fine_reach.append(FAST in picked)
            fine_reach = np.array(fine_reach, bool)
            reach_last = float(FINE[np.flatnonzero(fine_reach)[-1]]) if fine_reach.any() else float("nan")
            reach_dies = (float(FINE[np.flatnonzero(fine_reach)[-1] + 1])
                          if fine_reach.any() and np.flatnonzero(fine_reach)[-1] + 1 < len(FINE)
                          else float("nan"))
            grF, tnF = grs[FAST]
            grA, tnA = grs[a["H"]]
            # FINE cost curve for both, solved rather than interpolated
            dS, dC = [], []
            for c in FINE:
                sF = sharpe((grF - tnF * c / 1e4)[WARMUP:])
                sA = sharpe((grA - tnA * c / 1e4)[WARMUP:])
                gF = cagr((grF - tnF * c / 1e4)[WARMUP:])
                gA = cagr((grA - tnA * c / 1e4)[WARMUP:])
                dS.append(sF - sA)
                dC.append(gF - gA)
                curverows.append(dict(panel=pname, anchor=anchor, cost_bps=c, H_fast=FAST,
                                      S_fast=sF, S_anchor=sA, CAGR_fast=gF, CAGR_anchor=gA))
            dS, dC = np.array(dS), np.array(dC)

            def crossing(d):
                if d[0] <= 0:
                    return 0.0
                k = np.flatnonzero(d <= 0)
                return float(FINE[k[0]]) if len(k) else float("nan")

            ffF = first_fail_cost(grF, tnF, i_oos, sw, FINE)
            ffA = first_fail_cost(grA, tnA, i_oos, sw, FINE)
            reachrows.append(dict(panel=pname, anchor=anchor, H_fast=FAST, H_anchor=a["H"],
                                  turn_fast=tn_yr[FAST], turn_anchor=tn_yr[a["H"]],
                                  turn_ratio=tn_yr[FAST] / max(tn_yr[a["H"]], 1e-12),
                                  reach_0=reach_by_cost[0.0], reach_10=reach_by_cost[10.0],
                                  reach_25=reach_by_cost[25.0], reach_50=reach_by_cost[50.0],
                                  reach_100=reach_by_cost[100.0],
                                  IS_rank_0=rank_by_cost[0.0], IS_rank_10=rank_by_cost[10.0],
                                  IS_rank_100=rank_by_cost[100.0],
                                  fine_reach_share=float(fine_reach.mean()),
                                  fine_reach_last_cost=reach_last, fine_reach_dies_at=reach_dies,
                                  dSharpe_at_0=float(dS[0]), dSharpe_at_10=float(dS[10]),
                                  dSharpe_at_100=float(dS[100]),
                                  cross_cost_Sharpe=crossing(dS), cross_cost_CAGR=crossing(dC),
                                  fast_4b_first_fail=ffF.get("ALL"),
                                  anchor_4b_first_fail=ffA.get("ALL"),
                                  **{f"fast_fail_{k}": v for k, v in ffF.items() if k != "ALL"},
                                  **{f"anchor_fail_{k}": v for k, v in ffA.items() if k != "ALL"}))
            say(f"     FAST RUNG H={FAST}: turnover {tn_yr[FAST]:.2f}/yr vs anchor "
                f"{tn_yr[a['H']]:.2f}/yr ({tn_yr[FAST]/max(tn_yr[a['H']],1e-12):.2f}x); "
                f"reachable at " + ",".join(f"{int(c)}:{'Y' if reach_by_cost[c] else 'n'}" for c in COSTS) +
                f"; on the FINE ladder picked at {fine_reach.sum()}/{len(FINE)} rungs, last at "
                f"{reach_last} bps, never again from {reach_dies} bps")
            say(f"     FAST minus ANCHOR full Sharpe: {dS[0]:+.4f} @0, {dS[10]:+.4f} @10, "
                f"{dS[50]:+.4f} @50, {dS[100]:+.4f} @100 -> crossing cost "
                f"{crossing(dS) if np.isfinite(crossing(dS)) else float('nan'):.0f} bps "
                f"(CAGR crossing {crossing(dC):.0f} bps)")
            say(f"     4b first-fail cost (FINE ladder): FAST {ffF.get('ALL')} bps, "
                f"ANCHOR {ffA.get('ALL')} bps; per-leg FAST " +
                ", ".join(f"{k}:{v}" for k, v in ffF.items() if k != "ALL"))

    g = pd.DataFrame(gridrows)
    r8 = pd.DataFrame(r8rows)
    rch = pd.DataFrame(reachrows)
    cur = pd.DataFrame(curverows)
    dump(g, "grid")
    dump(r8, "walkforward")
    dump(rch, "reach")
    dump(cur, "costcurve")
    dump(pd.DataFrame(GATES), "gates")

    say("\n" + "=" * 100)
    say("## ANSWER")
    say(f"   grid: {len(g)} books (3 panels x 2 anchors x {len(LAD_H)} rungs x {len(COSTS)} costs)")
    for c in COSTS:
        s = g[g.cost_bps == c]
        say(f"   cost {int(c):3d} bps: 4a {int(s.keep4a.sum())}/{len(s)}   4b {int(s.keep4b.sum())}/{len(s)}"
            f"   mean full Sharpe {s.full_Sharpe.mean():.4f}   mean OOS Sharpe {s.oos_Sharpe.mean():.4f}")
    # which rungs lose a 4b pass as cost rises
    piv = g.pivot_table(index=["panel", "anchor", "H"], columns="cost_bps", values="keep4b")
    lost = piv[(piv[0.0] == 1) & (piv[100.0] == 0)]
    kept = piv[(piv[0.0] == 1) & (piv[100.0] == 1)]
    say(f"   cells passing 4b at 0 bps: {int((piv[0.0] == 1).sum())}; still passing at 100 bps: "
        f"{len(kept)}; lost between: {len(lost)}")
    if len(lost):
        say("   rungs that LOSE 4b inside 100 bps: " +
            ", ".join(f"{p}/{a}/H{h}" for p, a, h in lost.index))
    if len(kept):
        say("   rungs that KEEP 4b at 100 bps:    " +
            ", ".join(f"{p}/{a}/H{h}" for p, a, h in kept.index))
    fastrows = rch
    say(f"   FAST rung H={FAST} reachable: " + ", ".join(
        f"{int(c)}bps {int(fastrows['reach_' + str(int(c))].sum())}/{len(fastrows)}" for c in COSTS))
    say(f"   FAST rung H={FAST} stops being reachable AT ALL (fine ladder) at: " + ", ".join(
        f"{r.panel}/{r.anchor} {r.fine_reach_dies_at}" for r in fastrows.itertuples()))
    say(f"   FAST-minus-ANCHOR Sharpe crossing cost by (panel, anchor): " +
        ", ".join(f"{r.panel}/{r.anchor} {r.cross_cost_Sharpe}" for r in fastrows.itertuples()))
    say(f"   rule 8: {len(r8)} decisions; pick-minus-anchor OOS Sharpe mean "
        f"{r8.delta_vs_anchor.mean():+.4f}, positive {int((r8.delta_vs_anchor > 0).sum())}/{len(r8)}, "
        f"reach (pick == anchor H) {int(r8.reach_anchor.sum())}/{len(r8)}, "
        f"pick == FAST {int(r8.pick_is_FAST.sum())}/{len(r8)}")
    for c in COSTS:
        s = r8[r8.cost_bps == c]
        say(f"      @{int(c):3d} bps: delta mean {s.delta_vs_anchor.mean():+.4f}, positive "
            f"{int((s.delta_vs_anchor > 0).sum())}/{len(s)}, 4b {int(s.keep4b.sum())}/{len(s)}, "
            f"picks {sorted(set(s.pick_H))}")
    say(f"   gates: {sum(x['pass_'] for x in GATES)}/{len(GATES)} PASS "
        f"({', '.join(x['gate'].split()[0] for x in GATES if not x['pass_']) or 'none failed'})")
    say(f"   elapsed {time.time() - t0:.0f}s")
    Path(f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
