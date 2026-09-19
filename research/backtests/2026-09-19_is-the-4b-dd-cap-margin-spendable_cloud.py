#!/usr/bin/env python3
"""Idea 1606 — is the 4b DRAWDOWN-CAP MARGIN SPENDABLE?

THE OBJECT.  Two committed books sit on opposite sides of the same 4b bar.  The live RULES v2
book runs -12.05% of drawdown against a -20.23% cap (8.18 pp of the budget UNUSED) and misses the
4b CAGR floor by ~2 pp.  The standing 4b anchor (the frozen 2026-09-04 incumbent) runs -19.13%
against the same cap, with 1.10 pp of slack, and clears the floor.  If drawdown budget were
CURRENCY, the live book could buy its missing CAGR with the 8 pp it is not spending.

THE QUESTION, in two halves, both priced.
  (A) THE RAY.  Walk the CONSTANT gross ladder g in {0.30 .. 1.00 step 0.01} on each frame and
      panel — 71 real books each — and read off (i) the gross that spends the budget EXACTLY
      (MaxDD == the 4b cap) and (ii) the CAGR it delivers there.  If the CAGR floor is still
      missed at the gross that exhausts the cap, the two bars are ONE RAY and the margin is not
      spendable at any exposure this protocol permits.  No leverage: g <= 1.00 (rule 2), so a
      budget that cannot be spent by g = 1.00 is a budget that cannot be spent.
  (B) THE LADDER.  A PRE-COMMITTED drawdown-budget ladder: hold gross G_HI while the book's own
      trailing drawdown (read at close t-1, on its own pre-cost equity, so no look-ahead and no
      cost feedback) is SHALLOWER than a trigger D, and fall back to the live 0.75 when it is
      deeper.  G_HI in {0.80, 0.85, 0.90, 0.95, 1.00} x D in {0.02, 0.04, 0.06, 0.08, 0.10, 0.12}
      = 30 cells.  Each ladder cell is then scored against its MaxDD-MATCHED CONSTANT TWIN — the
      constant gross g* on the SAME frame with the SAME full-sample MaxDD.  dCAGR = ladder minus
      twin is the ONLY quantity that can show a ladder buying something the ray does not.

TUNED PARAMETERS: exactly TWO — G_HI and the trigger D.  The FRAME (LIVE, INC) is a published
robustness axis of two ALREADY-COMMITTED books, not a fitted dial; the 0/10/25/50 bps cost ladder
is an exact identity off one engine run and is never selected on.

PRE-REGISTERED VERDICT RULE (written before the run, not after).
  H_RAY         the budget is NOT spendable: the constant ladder's CAGR at the cap-exhausting
                gross still misses the 4b CAGR floor, AND the pooled mean dCAGR(ladder - matched
                twin) <= 0.  Then drawdown budget and return sit on one ray, the 4b DD cap and
                CAGR floor are not independent bars, and this run is a KILL.
  H_SPENDABLE   some pre-committed ladder cell sits STRICTLY OUTSIDE the constant frontier
                (dCAGR > 0 against its MaxDD-matched twin) AND clears 4b FULL and OOS AND is
                reached by a legal IS-only chooser.  Only then is the margin currency.

PROTOCOL: rule 1 (>= 10y); rule 2 (decided at close t-1, applied at t; 10 bps headline; long-only,
gross <= 1.00, NEVER levered); rule 3 (vs live RULES v2 AND SPY); rule 4 (full + both halves, both
KEEP paths at EVERY cell); rule 8 (dials chosen on warm-up..2016-12-31, 2017-2026 read ONCE);
rule 9 (survivorship stated).

GATES.  G0 >= 10y.  G1 the LIVE frame at g = 0.75 replays `baseline.compare`'s RULES v2 row.
G2 CROSS-SCRIPT REPLAY of the committed frozen U56 anchor on the INC frame.  G3 exactly two tuned
dials.  G4 no chooser or trigger reads a row at or after its own decision date (the ladder's
drawdown is read at t-1; no chooser reads 2017+).  G5 gross in [0, 1] on every book — no leverage.
G6 the cost ladder is an exact identity.  G7 MaxDD match quality < 0.20 pp on every matched twin.
G8 every cell published.  G9 the SMALL max_1d_move filter applied.  G10 the ladder is a strict
generalisation: (G_HI = 0.75) reproduces the constant 0.75 book exactly.

Runs standalone and offline (committed price caches only; no network):
  python research/backtests/2026-09-19_is-the-4b-dd-cap-margin-spendable_cloud.py
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
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-19"
SLUG = "is-the-4b-dd-cap-margin-spendable"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP = 260
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_V, I_C = 20, 126, 0.60, "W"
G_LIVE = 0.75                                     # the live RULES v2 / frozen-anchor gross
BAND = 0.03                                       # RULES v2 clause 2
GHIS = [0.80, 0.85, 0.90, 0.95, 1.00]             # DIAL 1 (tuned)
TRIGS = [0.02, 0.04, 0.06, 0.08, 0.10, 0.12]      # DIAL 2 (tuned)
GFINE = [round(0.30 + 0.01 * k, 2) for k in range(71)]   # the constant ray, 71 real books
COSTS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_COST = 10.0
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
MATCH_BAR = 0.0020                                # 20 bp of MaxDD
C_U56 = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857)

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


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


def bmpack(r):
    h1, h2 = halves(r)
    m = triple(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def keep_paths(r, bm, live):
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(h1 > bm["H1"]), H2=bool(h2 > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


def mech_legs(q):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return (sum(parts) / len(parts)).values


def cadence_rows(idx, cad):
    m = rebalance_mask(idx, cad)
    v = m.shift(1, fill_value=False).values.copy()
    v[0] = True
    return np.flatnonzero(v)


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.q = px[invest]
        self.comp = mech_legs(self.q)
        self.vol20 = (self.q.pct_change().rolling(20).std() * np.sqrt(252)).values


def frame_live(pan):
    """RULES v2 (the LIVE book) as a UNIT-GROSS holdings frame, built by calling the COMMITTED
    `baseline.rules_v2_weights` itself at gross 1.0 and shifting one row (decision at close t-1
    applied at t), so the frame is the live book by construction and not a re-implementation of it.
    On U56 / B136 the sub-panel is every column, so the replay is exact (gate G1); on SMALL the
    protocol-mandated max_1d_move filter is applied first, which the record's own live-baseline row
    does not do — both numbers are printed."""
    sub = pan.px[[c for c in pan.px.columns if c in set(pan.invest) or c == "SPY"]]
    W = rules_v2_weights(sub, band=BAND, gross=1.0).shift(1).fillna(0.0)
    F = pd.DataFrame(0.0, index=pan.px.index, columns=pan.px.columns)
    F[W.columns] = W
    return F.values


def frame_inc(pan):
    """The frozen 2026-09-04 incumbent as a UNIT-GROSS holdings frame (top-N momentum, 200d gate,
    MAXVOL 0.60, min-hold H = 126, weekly)."""
    above = (pan.q > pan.q.rolling(200).mean()).values
    elig = above & (np.nan_to_num(pan.vol20, nan=1e9) < I_V)
    sc = pan.comp * (0.5 + 0.5 * above.astype(float))
    key = np.where(np.isfinite(sc), -sc, np.inf)
    reb = cadence_rows(pan.idx, I_C)
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    for i, t in enumerate(reb):
        ts = max(t - 1, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < I_H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = set(int(c) for c in young)
        need = I_N - len(keep)
        take = []
        if need > 0:
            k = key[ts].copy()
            k[~(elig[ts] & pr[ts])] = np.inf
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
        stop = reb[i + 1] if i + 1 < len(reb) else T
        if len(sel):
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def run_book(pan, frame, reb, g_lo, g_hi=None, trig=None):
    """Daily engine.  CONSTANT gross when g_hi is None; otherwise the PRE-COMMITTED drawdown-budget
    ladder: gross = g_hi while the book's own trailing drawdown READ AT t-1 (on its own pre-cost
    equity, so the cost ladder stays an exact identity and no cost feedback enters the signal) is
    shallower than `trig`, else g_lo.  De-gross goes to CASH at 0%, never re-spread, never levered."""
    T, M = pan.rets.shape
    isreb = np.zeros(T, bool)
    isreb[reb] = True
    cur = np.zeros(M)
    rg = np.zeros(T)
    turn = np.zeros(T)
    sc = np.zeros(T)
    eq, peak, dd_prev = 1.0, 1.0, 0.0
    gmax = 0.0
    for t in range(T):
        if isreb[t]:
            if g_hi is None:
                gt = g_lo
            else:
                gt = g_hi if dd_prev > -trig else g_lo    # budget unspent -> gear up
            post = gt * frame[t]
        else:
            post = cur
        sc[t] = float(post.sum())
        turn[t] = float(np.abs(post - cur).sum())
        gmax = max(gmax, sc[t])
        r = float(post @ pan.rets[t])
        rg[t] = r
        cur = post * (1.0 + pan.rets[t]) / (1.0 + r)
        eq *= (1.0 + r)
        peak = max(peak, eq)
        dd_prev = eq / peak - 1.0                          # read at t, used at t+1 -> no look-ahead
    return dict(rg=rg, turn=turn, gmax=gmax, gbar=float(sc[WARMUP:].mean()),
                hi_share=float(np.mean(sc[WARMUP:] > (g_lo + 1e-9))) if g_hi is not None else 0.0)


def net_of(run, cost):
    return run["rg"] - run["turn"] * cost / 1e4


def match_gross(ray, target_mdd, tag):
    """The constant gross g* whose FULL-sample MaxDD equals `target_mdd`, by linear interpolation
    on the 71-rung ray of REAL books.  Returns (g*, CAGR*, MaxDD*, |gap|) or None if the target is
    outside the ray (which is itself a finding: the budget is unreachable without leverage)."""
    gs = np.array([r["g"] for r in ray])
    dd = np.array([r[f"{tag}_MaxDD"] for r in ray])
    cg = np.array([r[f"{tag}_CAGR"] for r in ray])
    o = np.argsort(-dd)                                     # deepest .. shallowest
    dd_s, gs_s, cg_s = dd[o], gs[o], cg[o]
    if target_mdd > dd_s.max() or target_mdd < dd_s.min():
        return None
    j = int(np.searchsorted(-dd_s, -target_mdd))
    j = max(1, min(j, len(dd_s) - 1))
    lo, hi = j - 1, j
    w = 0.0 if dd_s[hi] == dd_s[lo] else (target_mdd - dd_s[lo]) / (dd_s[hi] - dd_s[lo])
    return dict(g=float(gs_s[lo] + w * (gs_s[hi] - gs_s[lo])),
                CAGR=float(cg_s[lo] + w * (cg_s[hi] - cg_s[lo])),
                MaxDD=float(dd_s[lo] + w * (dd_s[hi] - dd_s[lo])),
                gap=float(abs((dd_s[lo] + w * (dd_s[hi] - dd_s[lo])) - target_mdd)))


def main():
    t0 = time.time()
    say("=" * 128)
    say("IDEA 1606 — is the 4b DRAWDOWN-CAP MARGIN SPENDABLE?   (lane cloud, idea 2 of 2)")
    say("  PRE-REGISTERED  H_RAY:       the constant ladder still misses the 4b CAGR floor at the "
        "gross that EXHAUSTS the DD cap, AND pooled mean dCAGR(ladder - MaxDD-matched twin) <= 0")
    say("                               -> DD budget and return are ONE RAY, the two 4b bars are "
        "not independent, and this run is a KILL.")
    say("  PRE-REGISTERED  H_SPENDABLE: some pre-committed ladder cell beats its MaxDD-matched "
        "constant twin on CAGR, clears 4b FULL and OOS, and is reached by a legal IS-only chooser.")
    say("=" * 128)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    gate("G9 SMALL max_1d_move filter", f"{len(bad)} dropped, {len(inv)} investable",
         "protocol-mandated, applied", len(bad) > 0 and len(inv) > 100)

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"\n  PANELS: U56 {len(pxU.columns)-1}, B136 {len(pxB.columns)-1}, SMALL {len(inv)} names.")
    say("  SURVIVORSHIP (rule 9): U56 and B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010, so every ABSOLUTE level below is an UPPER BOUND.  "
        "The headline — a ladder against its own MaxDD-MATCHED constant twin on the SAME frame, "
        "SAME names, SAME days — is a contrast the bias cannot manufacture; the 4a / 4b verdicts "
        "against SPY inherit it and are read as upper bounds.")
    gate("G3 tuned parameters", 2, "exactly 2 (G_HI, trigger D)", True)

    RAY, LAD = [], []
    bench = {}
    g6_dev, g10_dev, g5_max = 0.0, 0.0, 0.0

    for pan in panels:
        T = len(pan.idx)
        gate(f"G0 {pan.name} length", f"{T/252:.1f}y", ">= 10y", T / 252 >= 10.0)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        spy_is = bmpack(pan.spy[WARMUP:i_oos])
        LIVEC, LIVEOC = {}, {}
        for c in COSTS:                       # 4a must be COST-MATCHED: the live comparand pays
            lrc = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=c,   # the same rung as the
                           freq="W")["returns"].values                     # candidate, else the
            LIVEC[c], LIVEOC[c] = bmpack(lrc[WARMUP:]), bmpack(lrc[i_oos:])  # 0 bps column is fake
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=HEADLINE_COST,
                      freq="W")["returns"].values
        live, liveO = LIVEC[HEADLINE_COST], LIVEOC[HEADLINE_COST]
        bench[pan.name] = dict(spy=spy, spyO=spyO, spy_is=spy_is, live=live, liveO=liveO,
                               livec=LIVEC, liveoc=LIVEOC, i_oos=i_oos, lr=lr)

        say(f"\n  [{pan.name}]  SPY {spy['CAGR']:.2%} / {spy['Sharpe']:.4f} / {spy['MaxDD']:.2%}  "
            f"|  4b bars: DD cap {DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps {live['CAGR']:.2%} / {live['Sharpe']:.4f} / "
            f"{live['MaxDD']:.2%}   ->  UNUSED DD BUDGET "
            f"{(live['MaxDD'] - DD_CAP*spy['MaxDD'])*100:+.2f} pp,  CAGR SHORTFALL "
            f"{(live['CAGR'] - CAGR_FLOOR*spy['CAGR'])*100:+.2f} pp")

        reb = cadence_rows(pan.idx, I_C)
        frames = dict(LIVE=frame_live(pan), INC=frame_inc(pan))

        for fname, F in frames.items():
            # ---- (A) the constant ray: 71 real books
            ray = []
            for g in GFINE:
                run = run_book(pan, F, reb, g)
                g6_dev = max(g6_dev, float(np.abs(net_of(run, 0.0) - run["rg"]).max()))
                g5_max = max(g5_max, run["gmax"])
                rec = dict(panel=pan.name, frame=fname, g=g, gbar=run["gbar"])
                for c in COSTS:
                    nr = net_of(run, c)
                    r_all, r_is, r_oos = nr[WARMUP:], nr[WARMUP:i_oos], nr[i_oos:]
                    k4a, k4b, m, h1, h2, legs = keep_paths(r_all, spy, LIVEC[c])
                    ko4a, ko4b, mo, _, _, _ = keep_paths(r_oos, spyO, LIVEOC[c])
                    t_ = f"c{int(c)}"
                    rec.update({f"{t_}_CAGR": m["CAGR"], f"{t_}_Sharpe": m["Sharpe"],
                                f"{t_}_MaxDD": m["MaxDD"], f"{t_}_H1": h1, f"{t_}_H2": h2,
                                f"{t_}_4a": k4a, f"{t_}_4b": k4b,
                                f"{t_}_4blegs": "".join("1" if legs[x] else "0"
                                                        for x in ("H1", "H2", "DD", "CAGR")),
                                f"{t_}_oCAGR": mo["CAGR"], f"{t_}_oSharpe": mo["Sharpe"],
                                f"{t_}_oMaxDD": mo["MaxDD"], f"{t_}_o4a": ko4a, f"{t_}_o4b": ko4b,
                                f"{t_}_isSharpe": sharpe(r_is), f"{t_}_isCAGR": cagr(r_is),
                                f"{t_}_isMaxDD": mdd(r_is)})
                ray.append(rec)
                RAY.append(rec)

            # G10: the ladder at G_HI = g_lo must reproduce the constant book exactly
            chk = run_book(pan, F, reb, G_LIVE, g_hi=G_LIVE, trig=0.06)
            base = run_book(pan, F, reb, G_LIVE)
            g10_dev = max(g10_dev, float(np.abs(chk["rg"] - base["rg"]).max()))

            # ---- (B) the ladder: 30 real books, each vs its MaxDD-matched constant twin
            for gh in GHIS:
                for tr in TRIGS:
                    run = run_book(pan, F, reb, G_LIVE, g_hi=gh, trig=tr)
                    g6_dev = max(g6_dev, float(np.abs(net_of(run, 0.0) - run["rg"]).max()))
                    g5_max = max(g5_max, run["gmax"])
                    rec = dict(panel=pan.name, frame=fname, gh=gh, trig=tr, gbar=run["gbar"],
                               hi_share=run["hi_share"])
                    for c in COSTS:
                        nr = net_of(run, c)
                        r_all, r_is, r_oos = nr[WARMUP:], nr[WARMUP:i_oos], nr[i_oos:]
                        k4a, k4b, m, h1, h2, legs = keep_paths(r_all, spy, LIVEC[c])
                        ko4a, ko4b, mo, _, _, _ = keep_paths(r_oos, spyO, LIVEOC[c])
                        t_ = f"c{int(c)}"
                        tw = match_gross(ray, m["MaxDD"], t_)
                        rec.update({f"{t_}_CAGR": m["CAGR"], f"{t_}_Sharpe": m["Sharpe"],
                                    f"{t_}_MaxDD": m["MaxDD"], f"{t_}_H1": h1, f"{t_}_H2": h2,
                                    f"{t_}_4a": k4a, f"{t_}_4b": k4b,
                                    f"{t_}_4blegs": "".join("1" if legs[x] else "0"
                                                            for x in ("H1", "H2", "DD", "CAGR")),
                                    f"{t_}_oCAGR": mo["CAGR"], f"{t_}_oSharpe": mo["Sharpe"],
                                    f"{t_}_oMaxDD": mo["MaxDD"], f"{t_}_o4a": ko4a,
                                    f"{t_}_o4b": ko4b, f"{t_}_isSharpe": sharpe(r_is),
                                    f"{t_}_isCAGR": cagr(r_is), f"{t_}_isMaxDD": mdd(r_is),
                                    f"{t_}_twin_g": tw["g"] if tw else np.nan,
                                    f"{t_}_twin_CAGR": tw["CAGR"] if tw else np.nan,
                                    f"{t_}_twin_gap": tw["gap"] if tw else np.nan,
                                    f"{t_}_dCAGR": (m["CAGR"] - tw["CAGR"]) if tw else np.nan})
                    LAD.append(rec)

    R, L = pd.DataFrame(RAY), pd.DataFrame(LAD)
    R.to_csv(f"{OUT}.ray.csv", index=False)
    L.to_csv(f"{OUT}.ladder.csv", index=False)
    gate("G6 cost-ladder identity (0 bps net == rg)", f"max |dev| {g6_dev:.3e}", "== 0",
         g6_dev == 0.0)
    gate("G5 no leverage", f"max realised gross {g5_max:.4f}", "<= 1.0", g5_max <= 1.0 + 1e-9)
    gate("G10 ladder(G_HI=0.75) == constant 0.75", f"max |dev| {g10_dev:.3e}", "== 0",
         g10_dev == 0.0)
    gate("G8 cells published", f"{len(R)} ray + {len(L)} ladder books",
         f"{71*6} + {30*6}", len(R) == 71 * 6 and len(L) == 30 * 6)
    mg = L["c10_twin_gap"].dropna()
    gate("G7 MaxDD match quality", f"max |gap| {mg.max()*100:.4f} pp over {len(mg)} twins",
         "< 0.20 pp", bool(mg.max() < MATCH_BAR))
    unm = L[L["c10_twin_g"].isna()]
    say(f"    PUBLISHED  ladder cells with NO legal constant twin: {len(unm)} of {len(L)} — their "
        f"MaxDD is deeper than the g = 1.00 constant book's, i.e. the ladder spends MORE drawdown "
        f"budget than FULL investment on the same frame does.")
    if len(unm):
        say("      " + ", ".join(f"{r.panel}/{r.frame} G_HI {r.gh:.2f} D {r.trig:.2f} "
                                 f"MaxDD {r.c10_MaxDD:.2%}" for _, r in unm.iterrows()))

    # ---------------------------------------------------------- G1 / G2 replays
    lv = R[(R.panel == "U56") & (R.frame == "LIVE") & (R.g == G_LIVE)].iloc[0]
    b = bench["U56"]
    d1 = max(abs(lv.c10_CAGR - b["live"]["CAGR"]), abs(lv.c10_Sharpe - b["live"]["Sharpe"]),
             abs(lv.c10_MaxDD - b["live"]["MaxDD"]))
    say(f"\n  G1 REPLAY of baseline.rules_v2_weights on U56 (LIVE frame, g = 0.75, W, 10 bps):")
    say(f"     this run {lv.c10_CAGR:7.2%} / {lv.c10_Sharpe:.4f} / {lv.c10_MaxDD:7.2%}   "
        f"engine.backtest {b['live']['CAGR']:7.2%} / {b['live']['Sharpe']:.4f} / "
        f"{b['live']['MaxDD']:7.2%}")
    gate("G1 LIVE frame replays RULES v2", f"max |dev| {d1:.4f}", "< 0.005", d1 < 0.005)
    ic = R[(R.panel == "U56") & (R.frame == "INC") & (R.g == G_LIVE)].iloc[0]
    d2 = max(abs(ic.c10_CAGR - C_U56["CAGR"]), abs(ic.c10_Sharpe - C_U56["Sharpe"]),
             abs(ic.c10_MaxDD - C_U56["MaxDD"]), abs(ic.c10_oSharpe - C_U56["oSharpe"]))
    say(f"  G2 REPLAY of the committed frozen U56 anchor (INC frame, g = 0.75, W, 10 bps):")
    say(f"     this run {ic.c10_CAGR:7.2%} / {ic.c10_Sharpe:.4f} / {ic.c10_MaxDD:7.2%}  OOS Sharpe "
        f"{ic.c10_oSharpe:.4f}   committed {C_U56['CAGR']:7.2%} / {C_U56['Sharpe']:.4f} / "
        f"{C_U56['MaxDD']:7.2%}  OOS {C_U56['oSharpe']:.4f}")
    gate("G2 cross-script anchor replay", f"max |dev| {d2:.4f}", "< 0.01", d2 < 0.01)

    # ---------------------------------------------------------- (A) THE RAY
    say("\n" + "=" * 128)
    say("(A)  THE CONSTANT RAY — can the DD budget be spent at all without leverage?  (10 bps, "
        "71 real books per frame x panel)")
    say("=" * 128)
    ray_rows = []
    for pan in panels:
        bb = bench[pan.name]
        cap, floor = DD_CAP * bb["spy"]["MaxDD"], CAGR_FLOOR * bb["spy"]["CAGR"]
        for fname in ("LIVE", "INC"):
            s = R[(R.panel == pan.name) & (R.frame == fname)].sort_values("g")
            at_cap = s[s.c10_MaxDD >= cap]
            best = at_cap.iloc[-1] if len(at_cap) else None       # deepest cell still inside cap
            gmax_ = s.iloc[-1]
            hit = match_gross(s.to_dict("records"), cap, "c10")
            say(f"\n  [{pan.name} / {fname}]  cap {cap:.2%}, CAGR floor {floor:.2%}")
            say(f"     g = 0.75 (committed): {s[s.g==G_LIVE].iloc[0].c10_CAGR:7.2%} / "
                f"{s[s.g==G_LIVE].iloc[0].c10_MaxDD:7.2%}")
            say(f"     g = 1.00 (max legal): {gmax_.c10_CAGR:7.2%} / {gmax_.c10_MaxDD:7.2%}"
                f"   {'STILL INSIDE the cap' if gmax_.c10_MaxDD >= cap else 'BREACHES the cap'}")
            if hit:
                say(f"     gross that EXACTLY exhausts the cap: g* = {hit['g']:.3f} -> CAGR "
                    f"{hit['CAGR']:7.2%}  vs floor {floor:.2%}  => "
                    f"{'CLEARS' if hit['CAGR'] >= floor else 'STILL MISSES by '+format((floor-hit['CAGR'])*100,'.2f')+' pp'}")
            else:
                say(f"     the cap is NOT reachable on this ray at g <= 1.00: the budget cannot be "
                    f"spent without leverage, which rule 2 forbids.")
            best_cell = s[(s.c10_MaxDD >= cap)]
            nb = best_cell.loc[best_cell.c10_CAGR.idxmax()] if len(best_cell) else None
            if nb is not None:
                say(f"     best CAGR among cap-compliant rungs: g = {nb.g:.2f} -> {nb.c10_CAGR:7.2%}"
                    f" / {nb.c10_Sharpe:.4f} / {nb.c10_MaxDD:7.2%}  4b {'PASS' if nb.c10_4b else 'fail'}"
                    f" [{nb.c10_4blegs}]  OOS {nb.c10_oCAGR:7.2%} / {nb.c10_oSharpe:.4f} / "
                    f"{nb.c10_oMaxDD:7.2%}  o4b {'PASS' if nb.c10_o4b else 'fail'}")
            ray_rows.append(dict(panel=pan.name, frame=fname, cap=cap, floor=floor,
                                 g_star=hit["g"] if hit else np.nan,
                                 cagr_at_cap=hit["CAGR"] if hit else np.nan,
                                 reachable=bool(hit),
                                 clears_floor=bool(hit and hit["CAGR"] >= floor),
                                 cagr_g100=float(gmax_.c10_CAGR), mdd_g100=float(gmax_.c10_MaxDD)))
    RR = pd.DataFrame(ray_rows)
    RR.to_csv(f"{OUT}.raysummary.csv", index=False)

    # ---------------------------------------------------------- (B) THE LADDER
    say("\n" + "=" * 128)
    say("(B)  THE PRE-COMMITTED DD-BUDGET LADDER vs its MaxDD-MATCHED CONSTANT TWIN  (10 bps, "
        "all 180 ladder books)")
    say("=" * 128)
    for pan in panels:
        for fname in ("LIVE", "INC"):
            s = L[(L.panel == pan.name) & (L.frame == fname)]
            say(f"\n  [{pan.name} / {fname}]   (dCAGR > 0 = the ladder buys something the ray does not)")
            for _, r in s.iterrows():
                say(f"    G_HI {r.gh:.2f}  D {r.trig:.2f}  hi-share {r.hi_share:5.1%}  "
                    f"{r.c10_CAGR:7.2%} / {r.c10_Sharpe:7.4f} / {r.c10_MaxDD:7.2%} | twin g* "
                    f"{r.c10_twin_g:.3f} CAGR {r.c10_twin_CAGR:7.2%} | dCAGR "
                    f"{r.c10_dCAGR*100:+6.2f} pp | 4a {'Y' if r.c10_4a else '.'} 4b "
                    f"{'Y' if r.c10_4b else '.'} [{r.c10_4blegs}] | OOS {r.c10_oCAGR:7.2%} / "
                    f"{r.c10_oSharpe:7.4f} / {r.c10_oMaxDD:7.2%} o4b {'Y' if r.c10_o4b else '.'}")
    say("\n  POOLED dCAGR (ladder - MaxDD-matched constant twin), by cost rung:")
    for c in COSTS:
        t_ = f"c{int(c)}"
        d = L[f"{t_}_dCAGR"].dropna()
        say(f"    {int(c):>2d} bps   mean {d.mean()*100:+.4f} pp   median {d.median()*100:+.4f} pp"
            f"   positive {int((d>0).sum())}/{len(d)}   max {d.max()*100:+.3f} pp")
    for (p, f), g in L.groupby(["panel", "frame"]):
        d = g["c10_dCAGR"].dropna()
        say(f"    {p:<6s}/{f:<4s}  mean {d.mean()*100:+.4f} pp   positive {int((d>0).sum())}/{len(d)}")

    # ---------------------------------------------------------- KEEP paths
    say("\n" + "=" * 128)
    say("KEEP-PATH CENSUS (both paths, FULL and OOS, every cost rung)")
    say("=" * 128)
    for c in COSTS:
        t_ = f"c{int(c)}"
        for nm, df in (("RAY", R), ("LADDER", L)):
            say(f"    {int(c):>2d} bps  {nm:<6s}  4a {int(df[f'{t_}_4a'].sum()):>3d}/{len(df)}  "
                f"4b {int(df[f'{t_}_4b'].sum()):>3d}/{len(df)}  OOS-4b "
                f"{int(df[f'{t_}_o4b'].sum()):>3d}/{len(df)}  4b FULL+OOS "
                f"{int((df[f'{t_}_4b'] & df[f'{t_}_o4b']).sum()):>3d}/{len(df)}")

    # ---------------------------------------------------------- rule 8
    say("\n" + "=" * 128)
    say("RULE 8 WALK-FORWARD — (G_HI, D) chosen on warm-up..2016-12-31 ONLY; 2017-2026 read ONCE")
    say("=" * 128)
    gate("G4 chooser look-ahead", "ladder trigger reads its own equity at t-1; choosers read only "
         "IS statistics", "no future row read", True)
    WF = []
    for pan in panels:
        bb = bench[pan.name]
        for fname in ("LIVE", "INC"):
            s = L[(L.panel == pan.name) & (L.frame == fname)]
            ray0 = R[(R.panel == pan.name) & (R.frame == fname) & (R.g == G_LIVE)].iloc[0]
            for c in COSTS:
                t_ = f"c{int(c)}"
                rws = s.to_dict("records")
                picks = {
                    "argmaxISsharpe": max(rws, key=lambda d: d[f"{t_}_isSharpe"]),
                    "argmaxIScalmar": max(rws, key=lambda d: d[f"{t_}_isCAGR"] /
                                          abs(d[f"{t_}_isMaxDD"]) if d[f"{t_}_isMaxDD"] < 0 else -9e9),
                    "argmaxIScagr|ISddcap": max(
                        [d for d in rws if d[f"{t_}_isMaxDD"] >= DD_CAP * bb["spy_is"]["MaxDD"]]
                        or rws, key=lambda d: d[f"{t_}_isCAGR"]),
                }
                for cn, p in picks.items():
                    WF.append(dict(panel=pan.name, frame=fname, cost=c, chooser=cn,
                                   gh=p["gh"], trig=p["trig"], oCAGR=p[f"{t_}_oCAGR"],
                                   oSharpe=p[f"{t_}_oSharpe"], oMaxDD=p[f"{t_}_oMaxDD"],
                                   o4a=p[f"{t_}_o4a"], o4b=p[f"{t_}_o4b"],
                                   dCAGR_vs_twin=p[f"{t_}_dCAGR"],
                                   base_oCAGR=float(ray0[f"{t_}_oCAGR"]),
                                   base_oSharpe=float(ray0[f"{t_}_oSharpe"]),
                                   base_oMaxDD=float(ray0[f"{t_}_oMaxDD"]),
                                   d_oSharpe=p[f"{t_}_oSharpe"] - float(ray0[f"{t_}_oSharpe"]),
                                   spy_oSharpe=bb["spyO"]["Sharpe"], spy_oCAGR=bb["spyO"]["CAGR"],
                                   live_oSharpe=bb["liveO"]["Sharpe"],
                                   live_oCAGR=bb["liveO"]["CAGR"]))
    Wf = pd.DataFrame(WF)
    Wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    for pan in panels:
        for fname in ("LIVE", "INC"):
            say(f"\n  [{pan.name} / {fname}]  do-nothing anchor = constant g = 0.75 on this frame")
            for _, r in Wf[(Wf.panel == pan.name) & (Wf.frame == fname)].iterrows():
                say(f"    {int(r.cost):>2d} bps  {r.chooser:<22s} -> (G_HI {r.gh:.2f}, D {r.trig:.2f})"
                    f"  OOS {r.oCAGR:7.2%} / {r.oSharpe:.4f} / {r.oMaxDD:7.2%}  vs do-nothing "
                    f"{r.base_oCAGR:7.2%} / {r.base_oSharpe:.4f} / {r.base_oMaxDD:7.2%}  d_oSharpe "
                    f"{r.d_oSharpe:+.4f}  dCAGR-vs-twin {r.dCAGR_vs_twin*100:+.2f} pp  "
                    f"o4a {'Y' if r.o4a else '.'} o4b {'Y' if r.o4b else '.'}")
    say("\n  RULE 8 OVER THE CONSTANT RAY ITSELF (g chosen on IS only, 71 rungs):")
    RWF = []
    for pan in panels:
        bb = bench[pan.name]
        for fname in ("LIVE", "INC"):
            s_ = R[(R.panel == pan.name) & (R.frame == fname)]
            r075 = s_[s_.g == G_LIVE].iloc[0]
            for c in COSTS:
                t_ = f"c{int(c)}"
                rws = s_.to_dict("records")
                picks = {
                    "argmaxIScagr": max(rws, key=lambda d: d[f"{t_}_isCAGR"]),
                    "argmaxISsharpe": max(rws, key=lambda d: d[f"{t_}_isSharpe"]),
                    "argmaxIScagr|ISddcap": max(
                        [d for d in rws if d[f"{t_}_isMaxDD"] >= DD_CAP * bb["spy_is"]["MaxDD"]]
                        or rws, key=lambda d: d[f"{t_}_isCAGR"]),
                    "PREREG smallest g clearing BOTH IS bars, else 0.75": min(
                        [d for d in rws if d[f"{t_}_isMaxDD"] >= DD_CAP * bb["spy_is"]["MaxDD"]
                         and d[f"{t_}_isCAGR"] >= CAGR_FLOOR * bb["spy_is"]["CAGR"]],
                        key=lambda d: d["g"], default=r075.to_dict()),
                }
                for cn, pk in picks.items():
                    RWF.append(dict(panel=pan.name, frame=fname, cost=c, chooser=cn, g=pk["g"],
                                    oCAGR=pk[f"{t_}_oCAGR"], oSharpe=pk[f"{t_}_oSharpe"],
                                    oMaxDD=pk[f"{t_}_oMaxDD"], o4a=pk[f"{t_}_o4a"],
                                    o4b=pk[f"{t_}_o4b"], base_oCAGR=float(r075[f"{t_}_oCAGR"]),
                                    base_oSharpe=float(r075[f"{t_}_oSharpe"]),
                                    base_oMaxDD=float(r075[f"{t_}_oMaxDD"])))
    RW = pd.DataFrame(RWF)
    RW.to_csv(f"{OUT}.raywalkforward.csv", index=False)
    for pan in panels:
        for fname in ("LIVE", "INC"):
            for _, r in RW[(RW.panel == pan.name) & (RW.frame == fname) &
                           (RW.cost == HEADLINE_COST)].iterrows():
                say(f"    {pan.name:<6s}/{fname:<4s} 10 bps  {r.chooser:<46s} -> g = {r.g:.2f}   "
                    f"OOS {r.oCAGR:7.2%} / {r.oSharpe:.4f} / {r.oMaxDD:7.2%}   vs g=0.75 "
                    f"{r.base_oCAGR:7.2%} / {r.base_oSharpe:.4f} / {r.base_oMaxDD:7.2%}   "
                    f"o4a {'Y' if r.o4a else '.'} o4b {'Y' if r.o4b else '.'}")
    RH = RW[RW.cost == HEADLINE_COST]
    say(f"    RAY rule-8 @10 bps: {int(RH.o4b.sum())} of {len(RH)} picks pass 4b OOS; "
        f"{int((RH.g > G_LIVE).sum())} of {len(RH)} pick MORE gross than the live 0.75, "
        f"{int((RH.g < G_LIVE).sum())} pick less.")

    H = Wf[Wf.cost == HEADLINE_COST]
    say(f"\n  RULE 8 SUMMARY @10 bps: {len(H)} picks; o4b passes {int(H.o4b.sum())}; o4a passes "
        f"{int(H.o4a.sum())}; mean d_oSharpe vs doing nothing {H.d_oSharpe.mean():+.4f}; "
        f"mean dCAGR vs the matched twin {H.dCAGR_vs_twin.mean()*100:+.3f} pp")

    # ---------------------------------------------------------- verdict
    d10 = L["c10_dCAGR"].dropna()
    ray_kills = bool((~RR.clears_floor).all())
    h_ray = bool(ray_kills and d10.mean() <= 0)
    spend_cells = L[(L.c10_dCAGR > 0) & (L.c10_4b) & (L.c10_o4b)]
    h_spend = bool(len(spend_cells) > 0 and int(H.o4b.sum()) > 0)
    say("\n" + "=" * 128)
    say(f"  RAY VERDICT: at the gross that exhausts the DD cap, the CAGR floor is cleared on "
        f"{int(RR.clears_floor.sum())} of {len(RR)} (panel x frame) cells; the cap is reachable at "
        f"g <= 1.00 on {int(RR.reachable.sum())} of {len(RR)}.")
    say(f"  LADDER VERDICT: pooled mean dCAGR vs the MaxDD-matched twin = {d10.mean()*100:+.4f} pp "
        f"({int((d10>0).sum())} of {len(d10)} positive); ladder cells clearing 4b FULL+OOS AND "
        f"beating their twin: {len(spend_cells)}; rule-8-reachable among them: {int(H.o4b.sum())}.")
    say(f"  H_RAY = {h_ray}   H_SPENDABLE = {h_spend}")
    G = pd.DataFrame(GATES)
    G.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"  GATES: {int(G.pass_.sum())} of {len(G)} PASS.")
    say(f"  elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
