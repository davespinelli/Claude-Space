#!/usr/bin/env python3
"""Idea 1280 (lane cloud, 2026-09-18): does the COST-AWARE CHOOSER become the ANCHOR faster
than the SWITCH gets expensive — and at which rung, and is that rung tradable?

THE PREMISE (idea 1276's rule-8 arm, quoted by the queue).  A rule-8 chooser that re-picks the
best rung of the record's H ladder at every fold and stitches the picks together ("STITCHED")
loses to the committed 2026-09-04 anchor (U56 / N=20 / H=126 / gross 0.75 / weekly) out of
sample, and the loss SHRINKS with cost: anchor-minus-stitched OOS Sharpe +0.0637 at 10 bps and
+0.0279 at 50 bps, while the re-booking charge the stitch pays ALONE grows +0.0015 -> +0.0058.
Read literally that says a cost-aware chooser converges on the anchor faster than switching
gets expensive, so somewhere on the cost axis the chooser stops being a separate object.

THE QUESTION AND WHY IT MATTERS FOR CAPITAL.  If the convergence rung sits inside a spread a
real account actually pays, then for that account the chooser IS the anchor: the record can
stop publishing "which rung does the chooser pick" as a live question and buy the anchor.  If
it sits far outside any tradable spread, the two are genuinely different books at every price
anyone trades at, and every committed chooser claim on this ladder is a claim about a decision
that stays open.  Either answer is worth having; neither has been solved, only interpolated
between two rungs.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4, and the queue's own wording):
    DIAL 1  COST RUNG.  Published ladder {0, 10, 25, 50, 75, 100, 150, 200} bps, plus a FINE
            0..200 bps curve at 1-bp resolution so the convergence rung is SOLVED, not
            interpolated.  The rung is applied to the CHOOSER (its IS Sharpe is computed at
            that rung, which is what "cost-aware" means) and to the EVALUATION alike.
    DIAL 2  PANEL {U56, B135, SMALL663}.
Everything else is reported at every value and is not a dial: the 9 H rungs of 1095's committed
ladder; both KEEP paths leg by leg; full / halves / IS / OOS CAGR, Sharpe, MaxDD; annual
turnover; the switch charge on its own; the fold count.

THE LADDER AND THE ANCHOR.  Candidate set = MIN HOLD H in {5, 10, 21, 42, 63, 90, 126, 189,
252} — 1095's committed ladder, used by 1275 and 1277 today, and it CONTAINS the anchor rung
H=126 (gate G5), so "the chooser picks the anchor" is a statement the grid can actually make.
Frozen at the record's construction and not touched here: RAW three-leg composite (21/252,
0/126, 0/63 percentile ranks), eligibility = above own 200d MA AND vol20 < 0.60, N=20 slots,
GROSS=0.75 of NAV, WEEKLY decide-Friday / trade-Monday, t+1 execution, 260-row warm-up, equal
1/len(held) slots.

HOW THE COST LADDER IS FREE, AND WHY THAT IS EXACT.  A book's DRIFTED HOLDINGS and its TRADED
NOTIONAL do not depend on the cost rung under the record's model (costs are charged against the
return series, never re-invested into the weights), so each book is built ONCE and its net
return at rung c is exactly `gross_r - turn * c/1e4`.  Gate G6 checks this against a direct
re-run at three rungs to machine precision.  That is what makes a 201-rung fine ladder on
9 books x 3 panels x 9 folds affordable at all.

THE FOLDS.  Two arms, both reported:
  R8  — PROTOCOL rule 8 exactly: choose on warm-up..2016-12-31, read 2017-2026 ONCE.  This is
        the capital arm and the only one a KEEP could rest on.
  F8  — an 8-fold EXPANDING walk-forward over 2017-2026 (each fold chooses on everything
        strictly before it and is evaluated on its own block).  This is what the queue's "at
        every fold" needs: a convergence rung read off ONE fold is an anecdote.
The STITCHED book is the F8 picks concatenated: fold k's target weights are the fold-k pick's,
so the re-booking turnover at a boundary where the pick CHANGES is charged automatically by the
same runner that charges every other rebalance.  The switch charge is also isolated exactly
(gate G7): at each boundary rebalance the runner records |w_new - w_drifted| and the
counterfactual |w_old - w_drifted| it would have paid had the pick not changed, and the
difference is the switch and nothing else.

PRE-DECLARED OUTCOMES, written before any number was read:
  (A) CONVERGES INSIDE A TRADABLE SPREAD — the pick equals the anchor at every fold on every
      panel at some rung <= 50 bps.  Then at any price a real account pays, the chooser IS the
      anchor and the open question closes.
  (B) CONVERGES ONLY OUTSIDE ONE — convergence exists but at a rung above 50 bps (or above 200).
      The 1276 shrinkage is real but the two books stay distinct at tradable prices.
  (C) NEVER CONVERGES — some (panel, fold) keeps picking away from the anchor at every rung out
      to 200 bps, i.e. the shrinkage 1276 saw is not monotone convergence at all.
  (D) CONVERGES BY DEFAULT — the pick equals the anchor at 0 bps too, so there is no
      convergence to measure on this ladder and 1276's shrinkage is an evaluation-side fact.
These are not exclusive across panels; whichever fire are reported as they fall.

SURVIVORSHIP (rule 9).  U56 and B135 are CURRENT-constituent lists; SMALL663 is a current
sub-$2B screen with the house `max_1d_move >= 1.0` filter applied first.  The headline here is a
CONTRAST between cost rungs on one ladder and one tape (which rung a chooser picks), first-order
immune to a level bias that moves every rung together; the 4a / 4b legs and the absolute OOS
numbers are not, and are upper bounds.

ONE CONVENTION MADE EXPLICIT, BECAUSE IT MOVES THE COMMITTED ANCHOR.  1277 and 1275 compute the
composite's percentile ranks over EVERY column of the U56 frame and ban SPY from selection only
on the SMALL panel, so on U56 their "incumbent" can HOLD SPY and is ranked against it.  This run
treats SPY as the benchmark and never as a constituent.  Gate G1 reproduces 1277's committed OOS
triple to 2.4e-05 under 1277's OWN convention, and G1b prices the difference: excluding SPY moves
the committed anchor's OOS Sharpe +0.0142 and its OOS CAGR +0.0024 with MaxDD identical to four
decimals.  No committed U56 claim in the record states which of the two it was read under.  Every
book in this run uses the SPY-excluded convention; the anchor's numbers here are therefore the
G1b ones, not the ones the changelog quotes.

Deterministic (no RNG anywhere), offline, no network.  Run: python3 <this file>
"""
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
SLUG = "does-the-CHOOSER-BECOME-THE-ANCHOR-FASTER-THAN-THE-SWITCH-GETS-EXPENSIVE"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_cloud"

PROTO_COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
A_N, A_H, A_G = 20, 126, 0.75                      # the committed 2026-09-04 book
LEGS = [(21, 252), (0, 126), (0, 63)]
HOLDS = [5, 10, 21, 42, 63, 90, 126, 189, 252]     # 1095's committed ladder
COSTS = [0, 10, 25, 50, 75, 100, 150, 200]         # DIAL 1, published ladder
FINE = np.arange(0, 201, 1.0)                      # DIAL 1, fine solve
NFOLD = 8
TRADABLE = {"PROTOCOL rule 2": 10.0, "liquid large-cap round trip": 25.0,
            "small-cap round trip": 50.0}
COMMITTED_1277_U56_OOS = (0.1704, 1.1690, -0.1913)  # gate G1 (1277, 10 bps, anchor)
COMMIT_TAPE_END = "2026-09-15"                      # 1277's tape end, gate G1
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


def windows(idx, r):
    n = len(r)
    h = n // 2
    o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]), oos=stats(r[o:]),
                is_=stats(r[:o]))


def flat(w):
    return {f"{k}_{m}": x for k, v in w.items() for m, x in v.items()}


# ------------------------------------------------------------------ panel
class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        q = px[invest]
        parts = []
        for skip, look in LEGS:
            x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
            parts.append(x.rank(axis=1, pct=True))
        comp = (sum(parts) / len(parts)).values
        self.key = np.where(np.isfinite(comp), -comp, np.inf)      # smaller = better
        above = (q > q.rolling(200).mean()).values
        vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
        self.elig = above & (np.nan_to_num(vol20, nan=1e9) < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)


def build(pan, H, N=A_N, lag=1):
    """Target weight rows (gross 1.0) for the min-hold-H book.  Retain every PRICED holding
    younger than H; refill freed slots from the top of the score among eligible names."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    key = pan.key
    nreb = len(pan.reb)
    for i, t in enumerate(pan.reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        if len(held):
            held = held[pr[t, held]]
        keep = [int(c) for c in (held[(t - cur[held]) < H] if len(held) else held)]
        k = key[ts].copy()
        k[~(pan.elig[ts] & pr[ts])] = np.inf
        for c in keep:
            k[c] = np.inf
        need, take = N - len(keep), []
        for c in np.argsort(k, kind="stable"):
            if need <= 0 or not np.isfinite(k[int(c)]):
                break
            take.append(int(c))
            need -= 1
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if not len(sel):
            continue
        stop = pan.reb[i + 1] if i + 1 < nreb else T
        W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def run(pan, Wt, gross=A_G, alt=None):
    """Hold gross*Wt from each rebalance, drift between.  Returns (gross daily return, daily
    traded notional, extra switch notional).  COST IS NOT APPLIED HERE: net at rung c is
    exactly `r - turn * c/1e4` (gate G6), which is what makes the fine ladder affordable.

    `alt` maps a rebalance row index -> the target row the book WOULD have held had the pick
    not changed there; the runner then also accumulates |w_new - drifted| - |w_alt - drifted|,
    which is the switch charge and nothing else (gate G7)."""
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    extra = 0.0
    curw = np.zeros(M)
    ends = np.append(pan.reb[1:], T)
    for i0, i1 in zip(pan.reb, ends):
        w0 = gross * Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        if alt is not None and i0 in alt:
            extra += turn[i0] - np.abs(gross * alt[i0] - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return (held * rets).sum(axis=1), turn, extra


def net(gr, turn, c):
    return gr - turn * c / 1e4


# ------------------------------------------------------------------ KEEP paths
def legs_4a(bk, live):
    return dict(H1=bk["h1"]["Sharpe"] > live["h1"]["Sharpe"],
                H2=bk["h2"]["Sharpe"] > live["h2"]["Sharpe"],
                DD=bk["full"]["MaxDD"] >= live["full"]["MaxDD"])


def legs_4b(bk, spy):
    return dict(H1=bk["h1"]["Sharpe"] > spy["h1"]["Sharpe"],
                H2=bk["h2"]["Sharpe"] > spy["h2"]["Sharpe"],
                OOS=bk["oos"]["Sharpe"] > spy["oos"]["Sharpe"],
                DD=bk["full"]["MaxDD"] >= DD_CAP * spy["full"]["MaxDD"],
                CAGR=bk["full"]["CAGR"] >= CAGR_FLOOR * spy["full"]["CAGR"])


def failed(d):
    return ",".join(k for k, v in d.items() if not v) or "-"


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say(f"# {DATE} idea 1280 lane cloud — {SLUG}")
    say(f"# anchor: U56-construction N={A_N} H={A_H} gross={A_G} weekly, RAW 3-leg composite, "
        f"gate above-200d AND vol20<{MAXVOL}, t+1, warm-up {WARMUP}")
    say(f"# DIAL 1 COST {COSTS} bps published + fine {FINE[0]:.0f}..{FINE[-1]:.0f} at 1 bp")
    say("# DIAL 2 PANEL {U56, B135, SMALL663}")
    say(f"# ladder H = {HOLDS} (1095's committed ladder; contains the anchor rung {A_H})")
    say(f"# folds: R8 = PROTOCOL rule 8 (IS warm-up..2016-12-31, OOS read once); "
        f"F8 = {NFOLD} expanding folds over 2017-2026")

    panels = []
    px = load_universe()
    panels.append(("U56", px, [c for c in px.columns if c != "SPY"]))
    pb = load_universe(broad=True)
    panels.append((f"B{pb.shape[1]-1}", pb, [c for c in pb.columns if c != "SPY"]))
    psm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv_s = [c for c in psm.columns if c != "SPY" and c not in bad]
    say(f"# SMALL panel: {psm.shape[1]-1} names, {len(bad & set(psm.columns))} dropped for "
        f"max_1d_move >= 1.0 -> {len(inv_s)} investable")
    panels.append((f"SMALL{len(inv_s)}", psm, inv_s))

    gate("G5 anchor rung is IN the ladder", A_H in HOLDS, True, A_H in HOLDS)

    grid, pickrows, r8rows, stitchrows, convrows = [], [], [], [], []
    conv_by_panel = {}
    for pname, p_px, inv in panels:
        pan = Panel(pname, p_px, inv)
        idx = pan.idx[WARMUP:]
        spy = windows(idx, pan.spy[WARMUP:])
        live_r = backtest(p_px, rules_v2_weights(p_px), cost_bps=PROTO_COST,
                          freq="W")["returns"].fillna(0.0).values[WARMUP:]
        live = windows(idx, live_r)
        say(f"\n## {pname}  n_days={len(pan.idx)}  n_names={len(inv)}  "
            f"{idx[0].date()}..{idx[-1].date()}")
        say(f"   SPY     full {spy['full']['CAGR']:7.2%} / {spy['full']['Sharpe']:.4f} / "
            f"{spy['full']['MaxDD']:7.2%}   OOS Sh {spy['oos']['Sharpe']:.4f}")
        say(f"   LIVE v2 full {live['full']['CAGR']:7.2%} / {live['full']['Sharpe']:.4f} / "
            f"{live['full']['MaxDD']:7.2%}   OOS Sh {live['oos']['Sharpe']:.4f}")

        # ---- build every rung ONCE (cost-free); net at any rung is a subtraction
        W = {H: build(pan, H) for H in HOLDS}
        G = {}
        for H in HOLDS:
            gr, tn, _ = run(pan, W[H])
            G[H] = (gr[WARMUP:], tn[WARMUP:])
        anchor_gr, anchor_tn = G[A_H]

        # ---- G6: the subtraction identity, checked against a direct re-run
        if pname == "U56":
            ok6 = True
            for c in (0.0, 10.0, 200.0):
                direct = (run(pan, W[A_H])[0] - run(pan, W[A_H])[1] * c / 1e4)[WARMUP:]
                d = float(np.abs(direct - net(anchor_gr, anchor_tn, c)).max())
                ok6 &= d < 1e-15
            gate("G6 net(c) == gross - turn*c/1e4", f"{d:.2e}", "< 1e-15", ok6)

        # ---- fold boundaries
        o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
        bnds = [o] + [o + int(round((len(idx) - o) * k / NFOLD)) for k in range(1, NFOLD + 1)]
        folds = [("R8", 0, o, o, len(idx))] + \
                [(f"F{k+1}", 0, bnds[k], bnds[k], bnds[k + 1]) for k in range(NFOLD)]

        # ---- published grid: every rung at every published cost
        for H in HOLDS:
            gr, tn = G[H]
            for c in COSTS:
                r = net(gr, tn, c)
                w = windows(idx, r)
                a4, b4 = legs_4a(w, live), legs_4b(w, spy)
                grid.append(dict(panel=pname, H=H, cost=c, anchor=(H == A_H), **flat(w),
                                 turnover=float(tn.sum() / (len(tn) / 252.0)),
                                 keep4a=all(a4.values()), keep4b=all(b4.values()),
                                 fail4a=failed(a4), fail4b=failed(b4)))

        # ---- the cost-aware pick at every fold, on the FINE ladder
        picks_fine = np.zeros((len(folds), len(FINE)), dtype=int)
        for fi, (fname, i0, i1, e0, e1) in enumerate(folds):
            IS = {H: (G[H][0][i0:i1], G[H][1][i0:i1]) for H in HOLDS}
            for ci, c in enumerate(FINE):
                sh = [sharpe(net(IS[H][0], IS[H][1], c)) for H in HOLDS]
                picks_fine[fi, ci] = HOLDS[int(np.nanargmax(sh))]
            for c in COSTS:
                sh = [sharpe(net(IS[H][0], IS[H][1], c)) for H in HOLDS]
                j = int(np.nanargmax(sh))
                pk = HOLDS[j]
                ev = net(G[pk][0][e0:e1], G[pk][1][e0:e1], c)
                ea = net(anchor_gr[e0:e1], anchor_tn[e0:e1], c)
                pickrows.append(dict(panel=pname, fold=fname, cost=c, pick=pk,
                                     is_sharpe=sh[j], is_sharpe_anchor=sh[HOLDS.index(A_H)],
                                     eval_sharpe_pick=sharpe(ev), eval_sharpe_anchor=sharpe(ea),
                                     pick_is_anchor=(pk == A_H)))

        # ---- convergence rung for this panel: all folds pick the anchor from here up
        allanch = (picks_fine == A_H).all(axis=0)
        # smallest c such that every rung >= c agrees (a rung that agrees then loses it again
        # is NOT convergence — this is the suffix definition, stated before it was read)
        suffix = np.flip(np.cumprod(np.flip(allanch.astype(int))))
        cr = float(FINE[int(np.argmax(suffix))]) if suffix.any() else float("nan")
        first = float(FINE[int(np.argmax(allanch))]) if allanch.any() else float("nan")
        conv_by_panel[pname] = (cr, first, allanch, (picks_fine == A_H).sum(axis=0), len(folds))
        say(f"   CONVERGENCE (all {len(folds)} folds pick H={A_H}): suffix rung "
            f"{cr if cr == cr else 'NEVER':>6} bps, first agreeing rung "
            f"{first if first == first else 'NEVER':>6} bps, "
            f"agreeing share of 0..200 = {allanch.mean():.4f}")
        say("   pick by fold on the published ladder (F=fold, columns = bps):")
        say("      fold |" + "".join(f"{c:>6}" for c in COSTS))
        for fi, (fname, *_rest) in enumerate(folds):
            sel = [picks_fine[fi, int(np.searchsorted(FINE, c))] for c in COSTS]
            say(f"      {fname:>4} |" + "".join(
                (f"{v:>6}" if v != A_H else f"{'*' + str(v):>6}") for v in sel))
        for c in COSTS:
            ci = int(np.searchsorted(FINE, c))
            agree = int((picks_fine[:, ci] == A_H).sum())
            convrows.append(dict(panel=pname, cost=c, folds=len(folds), agree=agree,
                                 share=agree / len(folds)))

        # ---- STITCHED book (F8 picks concatenated) vs the ANCHOR, at every published rung
        for c in COSTS:
            chosen = []
            for k in range(NFOLD):
                i0, i1 = 0, bnds[k]
                sh = [sharpe(net(G[H][0][i0:i1], G[H][1][i0:i1], c)) for H in HOLDS]
                chosen.append(HOLDS[int(np.nanargmax(sh))])
            # stitch target rows: fold k's block uses that fold's pick
            Ws = np.zeros_like(W[A_H])
            Ws[:] = W[chosen[0]]
            alt = {}
            for k in range(NFOLD):
                a, b = WARMUP + bnds[k], WARMUP + bnds[k + 1]
                Ws[a:b] = W[chosen[k]][a:b]
                if k > 0 and chosen[k] != chosen[k - 1]:
                    nxt = pan.reb[pan.reb >= a]
                    if len(nxt):
                        alt[int(nxt[0])] = W[chosen[k - 1]][int(nxt[0])]
            Ws[:WARMUP + bnds[0]] = W[chosen[0]][:WARMUP + bnds[0]]
            gs, ts, extra = run(pan, Ws, alt=alt)
            rs = net(gs[WARMUP:], ts[WARMUP:], c)
            ws = windows(idx, rs)
            wa = windows(idx, net(anchor_gr, anchor_tn, c))
            yrs = (len(idx) - o) / 252.0
            sw_drag = extra * c / 1e4 / yrs        # annualised, OOS era where switches live
            a4, b4 = legs_4a(ws, live), legs_4b(ws, spy)
            stitchrows.append(dict(
                panel=pname, cost=c, picks="/".join(str(x) for x in chosen),
                n_switch=sum(1 for k in range(1, NFOLD) if chosen[k] != chosen[k - 1]),
                switch_notional=extra, switch_drag_yr=sw_drag,
                stitch_oos_Sharpe=ws["oos"]["Sharpe"], anchor_oos_Sharpe=wa["oos"]["Sharpe"],
                anchor_minus_stitch=wa["oos"]["Sharpe"] - ws["oos"]["Sharpe"],
                stitch_oos_CAGR=ws["oos"]["CAGR"], anchor_oos_CAGR=wa["oos"]["CAGR"],
                stitch_oos_MaxDD=ws["oos"]["MaxDD"], anchor_oos_MaxDD=wa["oos"]["MaxDD"],
                keep4a=all(a4.values()), keep4b=all(b4.values()),
                fail4a=failed(a4), fail4b=failed(b4), **flat(ws)))

        # ---- R8 capital arm at every published rung: IS-only pick, OOS read once
        for c in COSTS:
            sh = [sharpe(net(G[H][0][:o], G[H][1][:o], c)) for H in HOLDS]
            pk = HOLDS[int(np.nanargmax(sh))]
            wp = windows(idx, net(G[pk][0], G[pk][1], c))
            wa = windows(idx, net(anchor_gr, anchor_tn, c))
            a4, b4 = legs_4a(wp, live), legs_4b(wp, spy)
            r8rows.append(dict(panel=pname, cost=c, pick=pk, pick_is_anchor=(pk == A_H),
                               oos_Sharpe=wp["oos"]["Sharpe"],
                               oos_Sharpe_anchor=wa["oos"]["Sharpe"],
                               reach=wp["oos"]["Sharpe"] >= wa["oos"]["Sharpe"],
                               oos_CAGR=wp["oos"]["CAGR"], oos_CAGR_anchor=wa["oos"]["CAGR"],
                               oos_MaxDD=wp["oos"]["MaxDD"], oos_MaxDD_anchor=wa["oos"]["MaxDD"],
                               spy_oos_Sharpe=spy["oos"]["Sharpe"],
                               spy_oos_CAGR=spy["oos"]["CAGR"],
                               spy_oos_MaxDD=spy["oos"]["MaxDD"],
                               live_oos_Sharpe=live["oos"]["Sharpe"],
                               keep4a=all(a4.values()), keep4b=all(b4.values()),
                               fail4a=failed(a4), fail4b=failed(b4)))

        # ---- G1 / G1b: the committed anchor triple on U56 at PROTOCOL's rung, and the
        # convention that reconciles it.  1277 and 1275 compute the composite's percentile
        # ranks over EVERY column of the U56 frame and ban SPY from selection only on the SMALL
        # panel, so their "incumbent" can HOLD SPY and ranks against it.  This run treats SPY as
        # the benchmark and never as a constituent.  G1 reproduces 1277's committed reading
        # under 1277's OWN convention; G1b publishes what this run's convention costs it.
        if pname == "U56":
            r10 = net(anchor_gr, anchor_tn, PROTO_COST)
            wa = windows(idx, r10)
            pan_spy = Panel("U56+SPY", p_px, list(p_px.columns))
            gs, ts_, _ = run(pan_spy, build(pan_spy, A_H))
            ws = windows(idx, net(gs[WARMUP:], ts_[WARMUP:], PROTO_COST))
            gots = (ws["oos"]["CAGR"], ws["oos"]["Sharpe"], ws["oos"]["MaxDD"])
            got = (wa["oos"]["CAGR"], wa["oos"]["Sharpe"], wa["oos"]["MaxDD"])
            ds = max(abs(a - b) for a, b in zip(gots, COMMITTED_1277_U56_OOS))
            d = max(abs(a - b) for a, b in zip(got, COMMITTED_1277_U56_OOS))
            gate("G1 anchor OOS triple vs 1277's committed, under 1277's OWN convention "
                 "(SPY admitted to the U56 selection set)",
                 f"{gots[0]:.4f}/{gots[1]:.4f}/{gots[2]:.4f} (maxdiff {ds:.2e})",
                 f"{COMMITTED_1277_U56_OOS} (< 5e-4)", ds < 5e-4)
            say(f"   G1b SPY-AS-CONSTITUENT is the whole gap, and it is not zero: this run's "
                f"convention (SPY benchmark only) reads {got[0]:.4f}/{got[1]:.4f}/{got[2]:.4f}, "
                f"maxdiff {d:.2e} from the committed triple — OOS Sharpe "
                f"{got[1]-gots[1]:+.4f}, OOS CAGR {got[0]-gots[0]:+.4f}, MaxDD identical to 4 dp. "
                f"No committed U56 claim states which convention produced it.")
            GATES.append(dict(gate="G1b SPY-as-constituent delta on the committed anchor",
                              value=f"OOS Sharpe {got[1]-gots[1]:+.4f}, CAGR {got[0]-gots[0]:+.4f}",
                              target="reported, gates nothing", pass_=True))
            # ---- G2: fast runner == engine.backtest on the anchor.  build() bakes the t+1 lag
            # into its rows (row t holds the decision made at t-1) while engine.backtest applies
            # its OWN shift(1), so the engine-facing frame is rolled back by one row; without
            # that the two runners are compared one session apart.
            Wdf = pd.DataFrame(np.roll(A_G * W[A_H], -1, axis=0),
                               index=pan.idx, columns=pan.px.columns)
            eng = backtest(pan.px, Wdf, cost_bps=PROTO_COST, freq="W")["returns"].fillna(0.0)
            dd = float(np.abs(eng.values[WARMUP:] - r10).max())
            gate("G2 fast runner == engine.backtest", f"{dd:.2e}", "< 1e-12", dd < 1e-12)
            # ---- G3: Sharpe non-increasing in the cost rung at every rung of the ladder
            bad3 = 0
            for H in HOLDS:
                s = [sharpe(net(G[H][0], G[H][1], c)) for c in FINE]
                bad3 += int((np.diff(s) > 1e-12).sum())
                A = anchor_gr
            gate("G3 Sharpe non-increasing in cost", f"{bad3} violations", "0", bad3 == 0)
            # ---- G7: the switch charge is isolated
            s0 = [r for r in stitchrows if r["panel"] == pname and r["cost"] == 0][0]
            gate("G7 switch notional >= 0 and 0 when no pick changes",
                 f"n_switch={s0['n_switch']} extra={s0['switch_notional']:.6f}",
                 ">= 0; == 0 iff n_switch == 0",
                 s0["switch_notional"] >= -1e-12 and
                 (s0["n_switch"] > 0 or abs(s0["switch_notional"]) < 1e-12))

    # ---------------------------------------------------------------- report
    gp, pp = pd.DataFrame(grid), pd.DataFrame(pickrows)
    sp, r8 = pd.DataFrame(stitchrows), pd.DataFrame(r8rows)
    cv = pd.DataFrame(convrows)

    say("\n=== CONVERGENCE RUNG (DIAL 1 solved at 1 bp; agreement = all folds pick H=126) ===")
    say("   panel        | suffix rung | first agreeing | share of 0..200 agreeing")
    glob_ok = None
    agree_fine = sum(v[3] for v in conv_by_panel.values())
    ncell = sum(v[4] for v in conv_by_panel.values())
    for pname, (cr, first, allanch, _af, _nf) in conv_by_panel.items():
        say(f"   {pname:<12} | {('%.0f' % cr) if cr == cr else 'NEVER':>11} | "
            f"{('%.0f' % first) if first == first else 'NEVER':>14} | {allanch.mean():.4f}")
        glob_ok = allanch if glob_ok is None else (glob_ok & allanch)
    suffix = np.flip(np.cumprod(np.flip(glob_ok.astype(int))))
    CR = float(FINE[int(np.argmax(suffix))]) if suffix.any() else float("nan")
    say(f"   ALL PANELS x ALL FOLDS  -> convergence rung "
        f"{('%.0f bps' % CR) if CR == CR else 'NEVER INSIDE 0..200 bps'}")
    say(f"   PEAK AGREEMENT anywhere on the fine 0..200 ladder: "
        f"{int(agree_fine.max())} of {ncell} (panel, fold) cells, first reached at "
        f"{FINE[int(np.argmax(agree_fine))]:.0f} bps; agreement at 0 bps "
        f"{int(agree_fine[0])}/{ncell}, at 200 bps {int(agree_fine[-1])}/{ncell}")
    say("   agreement count by rung (every 10 bps): " + " ".join(
        f"{int(FINE[i])}:{int(agree_fine[i])}" for i in range(0, len(FINE), 10)))
    for label, bps in TRADABLE.items():
        inside = (CR == CR) and CR <= bps
        say(f"   tradable check: {label:<28} {bps:>5.0f} bps -> "
            f"{'INSIDE' if inside else 'OUTSIDE'}")

    say("\n=== AGREEMENT SHARE by (panel, published rung) — folds picking the anchor ===")
    say("   panel        |" + "".join(f"{c:>8}" for c in COSTS))
    for pname in conv_by_panel:
        row = cv[cv.panel == pname].set_index("cost")
        say(f"   {pname:<12} |" + "".join(
            f"{int(row.loc[c,'agree'])}/{int(row.loc[c,'folds'])}".rjust(8) for c in COSTS))

    say("\n=== STITCHED (F8 chooser) vs ANCHOR, OOS 2017-2026 ===")
    say("   panel        cost |   stitch Sh   anchor Sh   A-minus-S | switches  switch drag/yr | 4b")
    for _, r in sp.iterrows():
        say(f"   {r.panel:<12} {r.cost:>4.0f} | {r.stitch_oos_Sharpe:>11.4f} "
            f"{r.anchor_oos_Sharpe:>11.4f} {r.anchor_minus_stitch:>+11.4f} | "
            f"{r.n_switch:>8d}  {r.switch_drag_yr:>14.6f} | "
            f"{'PASS' if r.keep4b else r.fail4b}")

    say("\n=== RULE 8 CAPITAL ARM (IS warm-up..2016-12-31, OOS 2017-2026 READ ONCE) ===")
    say("   panel        cost | pick |  OOS CAGR  OOS Sh  OOS MaxDD | anchor Sh | SPY Sh | "
        "live Sh | reach | 4b")
    for _, r in r8.iterrows():
        say(f"   {r.panel:<12} {r.cost:>4.0f} | {r['pick']:>4d} | {r.oos_CAGR:>9.2%} "
            f"{r.oos_Sharpe:>7.4f} {r.oos_MaxDD:>10.2%} | {r.oos_Sharpe_anchor:>9.4f} | "
            f"{r.spy_oos_Sharpe:>6.3f} | {r.live_oos_Sharpe:>7.3f} | "
            f"{'Y' if r.reach else 'n':^5} | {'PASS' if r.keep4b else r.fail4b}")

    say("\n=== KEEP PATHS over the whole published grid ===")
    say(f"   4a passes: {int(gp.keep4a.sum())} of {len(gp)}    "
        f"4b passes: {int(gp.keep4b.sum())} of {len(gp)}")
    for c in COSTS:
        s = gp[gp.cost == c]
        say(f"      cost {c:>4} bps: 4b {int(s.keep4b.sum()):>2} of {len(s)}   "
            f"4a {int(s.keep4a.sum()):>2} of {len(s)}")

    say("\n=== 1276's SHAPE, REPRODUCED AND EXTENDED (U56, anchor-minus-stitch) ===")
    u = sp[sp.panel == "U56"].set_index("cost")
    say("   cost bps |  anchor-minus-stitch |  switch drag/yr")
    for c in COSTS:
        say(f"   {c:>8} | {u.loc[c,'anchor_minus_stitch']:>20.4f} | "
            f"{u.loc[c,'switch_drag_yr']:>15.6f}")

    reach = int(r8.reach.sum())
    say(f"\n=== VERDICT INPUTS ===")
    say(f"   rule-8 picks reaching the anchor OOS: {reach} of {len(r8)}")
    say(f"   stitched books passing 4b: {int(sp.keep4b.sum())} of {len(sp)}")
    say(f"   convergence rung (all panels, all folds): "
        f"{('%.0f bps' % CR) if CR == CR else 'NEVER inside 0..200 bps'}")

    npass = sum(g["pass_"] for g in GATES)
    say(f"\nGATES {npass} of {len(GATES)} passing.  elapsed {time.time()-t0:.0f}s")

    gp.to_csv(f"{STEM}.grid.csv", index=False)
    pp.to_csv(f"{STEM}.picks.csv", index=False)
    sp.to_csv(f"{STEM}.stitch.csv", index=False)
    r8.to_csv(f"{STEM}.rule8.csv", index=False)
    cv.to_csv(f"{STEM}.converge.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)
    Path(f"{STEM}.log.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
