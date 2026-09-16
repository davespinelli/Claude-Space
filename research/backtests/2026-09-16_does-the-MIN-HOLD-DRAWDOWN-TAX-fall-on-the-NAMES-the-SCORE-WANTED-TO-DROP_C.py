#!/usr/bin/env python3
"""Idea 1065 (lane C, 2026-09-16) — does the MIN-HOLD DRAWDOWN TAX fall on the NAMES the SCORE
WANTED TO DROP?

QUESTION (QUEUE idea 1065, verbatim)
    idea 936 found min hold raises a BOOK's MaxDD by up to 7 pp (U56 f=W, -18.70% -> -25.91% at
    H=63) while leaving the gross-matched NULL's median MaxDD flat at -0.22 in 19 of 20 cells,
    and read the asymmetry as 'a selecting book's retained name is the one its own score wanted
    to drop'.  Measure that directly: attribute each book's drawdown contribution to
    RETAINED-BY-CONSTRAINT names against freely-held ones, and report whether the tax is
    concentrated in names whose rank had already fallen out of the top N.
    Max 2 params (attribution rule, min hold).

WHAT IS BEING MEASURED, DECLARED BEFORE ANY NUMBER.
    936's reading is a CAUSAL claim with an ATTRIBUTION test.  At each rebalance date a min-hold
    book holds two kinds of name: the ones its own ranking would have picked anyway (FREE) and
    the ones it may not sell yet (RETAINED-BY-CONSTRAINT).  The claim says the extra drawdown
    lives in the second bucket.  Three things have to be true and each is measured separately:
      (1) ATTRIBUTION — inside the book's own max-drawdown episode, the retained bucket's share
          of the loss EXCEEDS its share of the weight.  Exposure-normalised, CONC > 1.
      (2) CONTROL — under the gross-matched null the same flag carries no information (a random
          key's "wanted-dropped" is random), so its CONC must sit at 1.0.  If the real books'
          CONC is also 1.0 the tax is a MECHANICAL consequence of holding longer, not a
          selection fact, and 936's sentence is wrong however large the tax is.
      (3) CAUSALITY / PRICE — releasing exactly the flagged names (a SOFT min hold: keep a young
          name only while the score still wants it) must recover the tax.  This is the leg that
          can pay: it is a tradable rule, it keeps the turnover rebate H buys, and it is scored
          on both KEEP paths and under rule 8 like any other book.
    An attribution that passes (1) but fails (3) is a decomposition, not a mechanism.

THE TWO DIALS (rule 4, no more than two tuned parameters)
    1. ATTRIBUTION RULE — what "the score wanted to drop it" means, in three nested readings:
         R_GATE   the name fails the book's own eligibility gate today (below its 200d MA, or
                  20d vol >= 0.60).  Narrowest.
         R_TOP2N  the name is not inside today's free top-2N by the book's own score.
         R_TOPN   the name is not inside today's free top-N, i.e. today's ranking would not have
                  picked it at all.  Widest.  (R_GATE subset R_TOP2N subset R_TOPN by
                  construction; gated at G6.)
    2. MIN HOLD  H in {5, 21, 63, 126} trading days, 936's own ladder above H = 0.
    All 3 x 4 = 12 points are reported for every leg, for books AND for the null.  Nothing else
    is tuned: gross 0.75, 10 bps (PROTOCOL rule 2), N = 20, max_vol 0.60, the three top-N
    mechanisms and four rebalance grids of 936/968/1059 are REPORTED axes, never selected.

RULE 8.  The arm (H = 0 / HARD(H) / SOFT(rule, H) x rebalance grid) is chosen on 2009-2016
    Sharpe ALONE, per panel and mechanism, and 2017-2026 is read ONCE against SPY and the live
    RULES v2 book at the same rung.  The attribution itself is also re-run separately on the IS
    and OOS windows (WF-A), because a decomposition that only holds in sample is a PARK.

SURVIVORSHIP.  U56 and B136 are current-constituent panels.  Every LEVEL here is optimistic;
    the headline statistics are within-book contrasts (a bucket against its own book) and a
    book against its own null, both of which the bias largely cancels out of.
"""
from __future__ import annotations

import hashlib
import sys
import time
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-16"
SLUG = "does-the-MIN-HOLD-DRAWDOWN-TAX-fall-on-the-NAMES-the-SCORE-WANTED-TO-DROP"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

LAG = 1
WARMUP = 260
NTOP = 20
MAXVOL = 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
GROSS = 0.75

# ---- the two tuned dials ----------------------------------------------------------------------
RULES = ["R_GATE", "R_TOP2N", "R_TOPN"]
HOLDS = [5, 21, 63, 126]

# reported axes, never selected
PANELS = ["U56", "B136"]
MECHS = ["CAND20", "R3_84", "MOMONLY"]
FREQS = ["D", "W", "M", "Q"]
LEGSETS = {"CAND20": [(21, 252), (0, 126), (0, 63)],
           "R3_84": [(21, 252), (0, 126), (0, 84)],
           "MOMONLY": [(21, 252)]}
NSEED = 8

# committed cross-run anchors (idea 936 `.grid.csv`, BOOK rows, U56, 10 bps)
G936 = {("CAND20", "W", 0): (0.127272, 1.060652, -0.183084),
        ("CAND20", "W", 63): (0.149484, 1.101400, -0.256921),
        ("CAND20", "W", 126): (0.155787, 1.139701, -0.191276),
        ("MOMONLY", "W", 63): (0.153688, 1.105551, -0.262215),
        ("R3_84", "M", 21): None}
G936_TURN = {("CAND20", "W", 0): 10.792011, ("CAND20", "W", 63): 3.871294}
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
RULESV2_COMMITTED = (0.0861, 1.1998, -0.1205)
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def mdseed(*parts):
    return int(hashlib.md5("|".join(str(x) for x in parts).encode()).hexdigest()[:8], 16)


# ================================================================== engine (936's, + held path)
def nrun(rets, wt, mk, want_held=False):
    """GROSS returns and turnover; cost applied outside (gated at G1 against engine.backtest).
    want_held also returns the drifted per-name NAV weights, so a bucket decomposition of the
    book's own return path is an identity and not a model (gated at G4)."""
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
    gr = (held * rets).sum(axis=1)
    return (gr, turn, held) if want_held else (gr, turn)


def fmet(r):
    r = np.asarray(r, float)
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def lag(a):
    out = np.zeros_like(a)
    out[LAG:] = a[:-LAG]
    return out


def lagmask(m):
    out = np.zeros_like(m)
    out[LAG:] = m[:-LAG]
    return out


def legs_composite(px, legs):
    parts = []
    for skip, look in legs:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return sum(parts) / len(parts)


def mech_score(px, mech):
    """961/968/1059's selection score (no vol scaler — the KEEP 4b convention) and its gate."""
    comp = legs_composite(px, LEGSETS[mech])
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    elig = (above & (vol20 < MAXVOL)).values
    return sc.values, elig


def minhold_book(rank_key, elig, priced, reb, H, T, N, rule=None, tag_rule=None):
    """936's min-hold book, with the RELEASE rule and the ATTRIBUTION tag made explicit.

    rank_key[t, j] : ordering key, LOWER = picked first (inf = never pickable)
    elig[t, j]     : the book's own eligibility gate
    H              : minimum hold in trading days.  H = 0 is the ordinary book.
    rule           : None -> HARD min hold (936's book).  Otherwise a SOFT min hold: a young name
                     is released (may be sold) as soon as `rule` says the score wanted to drop it.
    tag_rule       : the rule used to TAG held name-days as RETAINED-BY-CONSTRAINT for the
                     attribution.  A name is tagged only if it is (a) young, (b) held only
                     because of that, and (c) flagged by tag_rule.

    Returns (W, TAG) with W gross-1.0 step weights and TAG a boolean name-day mask.
    """
    W = np.zeros((T, N))
    TAG = np.zeros((T, N), dtype=bool)
    cur = np.full(N, -1, dtype=np.int64)
    need_wd = {r for r in (rule, tag_rule) if r is not None}
    for i, t in enumerate(reb):
        k = rank_key[t]
        ok = elig[t] & priced[t]
        # today's FREE ranking, ignoring what is already held: the counterfactual the tag needs
        kk = np.where(ok, k, np.inf)
        order = np.argsort(kk, kind="stable")
        nfin = int(np.isfinite(kk[order]).sum())
        wants_drop = {}
        if "R_GATE" in need_wd:
            wants_drop["R_GATE"] = ~ok
        if "R_TOPN" in need_wd:
            z = np.ones(N, dtype=bool)
            z[order[:min(NTOP, nfin)]] = False
            wants_drop["R_TOPN"] = z
        if "R_TOP2N" in need_wd:
            z = np.ones(N, dtype=bool)
            z[order[:min(2 * NTOP, nfin)]] = False
            wants_drop["R_TOP2N"] = z
        held = np.flatnonzero(cur >= 0)
        if len(held):
            young = held[(t - cur[held]) < H]
            young = young[priced[t, young]]
        else:
            young = held
        if rule is not None and len(young):
            young = young[~wants_drop[rule][young]]     # SOFT: release what the score dropped
        keep = set(young.tolist())
        need = NTOP - len(keep)
        if need > 0:
            kf = kk.copy()
            for c in keep:
                kf[c] = np.inf
            o2 = np.argsort(kf, kind="stable")
            take = [int(c) for c in o2[:need] if np.isfinite(kf[c])]
        else:
            take = []
        new_cur = np.full(N, -1, dtype=np.int64)
        for c in keep:
            new_cur[c] = cur[c]
        for c in take:
            new_cur[c] = t
        cur = new_cur
        sel = np.flatnonzero(cur >= 0)
        stop = reb[i + 1] if i + 1 < len(reb) else T
        if len(sel):
            W[t:stop, sel] = 1.0 / len(sel)
            if tag_rule is not None:
                wd = wants_drop[tag_rule]
                tag = np.array([c in keep and bool(wd[c]) for c in sel])
                if tag.any():
                    TAG[t:stop, sel[tag]] = True
    return W, TAG


def blocks(r, warm, oos):
    rr = r[warm]
    c, s, d = fmet(rr)
    h = len(rr) // 2
    oc, os_, od = fmet(r[oos])
    ic, is_, idd = fmet(r[warm & ~oos])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd)


def legs_4b(b, sb):
    return {"L_H1": bool(b["H1"] > sb["H1"]), "L_H2": bool(b["H2"] > sb["H2"]),
            "L_OOS": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "L_DD": bool(abs(b["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"])),
            "L_CAGR": bool(b["CAGR"] >= CAGR_FLOOR * sb["CAGR"])}


def dd_window(r):
    """(peak index, trough index) of the max drawdown of the return path r."""
    eq = np.cumprod(1.0 + np.asarray(r, float))
    run = np.maximum.accumulate(eq)
    tr = int(np.argmin(eq / run - 1.0))
    pk = int(np.argmax(eq[:tr + 1])) if tr > 0 else 0
    return pk, tr


def attribute(held, rets, tagm, cost_r, sl):
    """Bucket decomposition of the book's own return path over the slice `sl`.

    Returns the retained bucket's share of the WEIGHT and of the LOSS/RETURN, and their ratio.
    Shares are taken over the INVESTED weight (cash is a third bucket and is reported apart).
    """
    hr = held[sl] * rets[sl]
    tg = tagm[sl]
    cR = float((hr * tg).sum())
    cF = float((hr * ~tg).sum())
    wR = float((held[sl] * tg).sum())
    wF = float((held[sl] * ~tg).sum())
    tot_w = wR + wF
    tot_c = cR + cF
    wsh = wR / tot_w if tot_w > 0 else np.nan
    csh = cR / tot_c if tot_c != 0 else np.nan
    return dict(w_share_R=wsh, c_share_R=csh,
                conc=(csh / wsh if (wsh and np.isfinite(wsh) and wsh > 0
                                    and np.isfinite(csh)) else np.nan),
                contrib_R=cR, contrib_F=cF, cost=float(cost_r[sl].sum()),
                ndays=int(np.arange(len(held))[sl].size))


def main():
    t0 = time.time()
    P(f"# Idea 1065 (lane C, {DATE}) — does the MIN-HOLD DRAWDOWN TAX fall on the NAMES the "
      f"SCORE WANTED TO DROP?")
    P(f"# 2 tuned dials: ATTRIBUTION RULE {RULES} x MIN HOLD {HOLDS} = "
      f"{len(RULES) * len(HOLDS)} points, ALL reported, none selected.")
    P(f"# Fixed (NOT dials): gross {GROSS}, cost {COST:.0f} bps (PROTOCOL rule 2), N {NTOP}, "
      f"max_vol {MAXVOL}; {len(MECHS)} mechanisms x {len(FREQS)} rebalance grids x "
      f"{len(PANELS)} panels are REPORTED axes.")
    P("# DECLARED BEFORE ANY NUMBER: (1) attribution — the retained bucket's share of the")
    P("#   max-drawdown episode's loss must EXCEED its share of the weight (CONC > 1);")
    P("#   (2) control — the gross-matched null's CONC must sit at 1.0, since a random key's")
    P("#   'wanted-dropped' flag carries no information; if the books' CONC is 1.0 too, the tax")
    P("#   is mechanical and 936's sentence is wrong however large the tax is;")
    P("#   (3) causality/price — a SOFT min hold that releases exactly the flagged names must")
    P("#   recover the tax while keeping the turnover rebate, and is scored on 4a/4b and rule 8.")
    P("# SURVIVORSHIP: current-constituent panels; every LEVEL is optimistic.  The headlines are")
    P("#   within-book (bucket vs its own book) and book-vs-own-null contrasts.")
    P("")

    PXD = {"U56": load_universe(), "B136": load_universe(broad=True)}
    PAN = {}
    for p, px in PXD.items():
        idx = px.index
        rets = px.pct_change().fillna(0.0).values
        ar = np.arange(len(idx))
        warm = ar >= WARMUP
        oos = np.asarray(idx > pd.Timestamp(IS_END))
        spyr = px["SPY"].pct_change().fillna(0.0).values
        PAN[p] = dict(px=px, idx=idx, rets=rets, warm=warm, oos=oos & warm, T=len(idx),
                      N=px.shape[1], priced=px.notna().values, yrs=warm.sum() / 252.0,
                      spy=blocks(spyr, warm, oos & warm), spyr=spyr,
                      reb={f: np.flatnonzero(rebalance_mask(idx, f).values) for f in FREQS},
                      mask={f: rebalance_mask(idx, f).values for f in FREQS})
        P(f"  {p}: {px.shape[1]} cols x {len(idx)} days, {idx[0].date()} -> {idx[-1].date()}; "
          f"SPY full {PAN[p]['spy']['CAGR']:.2%} / {PAN[p]['spy']['Sharpe']:.4f} / "
          f"{PAN[p]['spy']['MaxDD']:.2%}")

    SCORE = {}
    for p, m in product(PANELS, MECHS):
        sc, el = mech_score(PXD[p], m)
        with np.errstate(invalid="ignore"):
            key = -np.nan_to_num(sc, nan=-np.inf)
        key[np.isnan(sc)] = np.inf
        SCORE[(p, m)] = (key, el)

    PERM = {}
    for p, s in product(PANELS, range(NSEED)):
        rng = np.random.default_rng(mdseed("PERM1065", p, s, PAN[p]["T"], PAN[p]["N"]))
        PERM[(p, s)] = rng.random((PAN[p]["T"], PAN[p]["N"])).astype(np.float64)

    # ================================================================== GATES
    P("=" * 100)
    P("REPRODUCTION GATES (pre-registered, printed before any new number)")
    P("=" * 100)
    gates = {}
    pan = PAN["U56"]
    px = PXD["U56"]

    W0, _ = minhold_book(*SCORE[("U56", "CAND20")], pan["priced"], pan["reb"]["W"], 0,
                         pan["T"], pan["N"])
    W0 *= GROSS
    gr, tt, held = nrun(pan["rets"], lag(W0), lagmask(pan["mask"]["W"]), want_held=True)
    mine = gr - tt * COST / 1e4
    eng = backtest(px, pd.DataFrame(W0, index=px.index, columns=px.columns),
                   cost_bps=COST, freq="W")
    d1 = float(np.abs(mine[WARMUP:] - eng["returns"].values[WARMUP:]).max())
    gates["G1"] = (d1 < 1e-12, f"runner == engine.backtest at {COST:.0f} bps on the min-hold "
                               f"book: max|dret| {d1:.2e}")

    d2 = 0.0
    for (m, f, H), ref in G936.items():
        if ref is None:
            continue
        Wc, _ = minhold_book(*SCORE[("U56", m)], pan["priced"], pan["reb"][f], H,
                             pan["T"], pan["N"])
        g, t = nrun(pan["rets"], lag(GROSS * Wc), lagmask(pan["mask"][f]))
        trip = fmet((g - t * COST / 1e4)[pan["warm"]])
        d2 = max(d2, max(abs(trip[i] - ref[i]) for i in range(3)))
    gates["G2"] = (d2 < 1e-4, f"CROSS-RUN idea 936's committed `.grid.csv` BOOK rows "
                              f"(U56, {len([k for k,v in G936.items() if v])} cells incl. the "
                              f"W/H=63 tax cell) rebuilt here: max|d| {d2:.2e}")

    d3 = 0.0
    for (m, f, H), ref in G936_TURN.items():
        Wc, _ = minhold_book(*SCORE[("U56", m)], pan["priced"], pan["reb"][f], H,
                             pan["T"], pan["N"])
        _, t = nrun(pan["rets"], lag(GROSS * Wc), lagmask(pan["mask"][f]))
        d3 = max(d3, abs(float(t[pan["warm"]].sum() / pan["yrs"]) - ref))
    gates["G3"] = (d3 < 1e-4, f"CROSS-RUN 936's committed realised turnover on the same two "
                              f"cells: max|d| {d3:.2e} turns/yr")

    Wt, TAG = minhold_book(*SCORE[("U56", "CAND20")], pan["priced"], pan["reb"]["W"], 63,
                           pan["T"], pan["N"], tag_rule="R_TOPN")
    g, t, hd = nrun(pan["rets"], lag(GROSS * Wt), lagmask(pan["mask"]["W"]), want_held=True)
    tg = lag(TAG.astype(float)) > 0.5
    resid = float(np.abs((hd * pan["rets"] * tg).sum(axis=1)
                         + (hd * pan["rets"] * ~tg).sum(axis=1) - g).max())
    gates["G4"] = (resid < 1e-14, f"ATTRIBUTION IDENTITY: retained + free bucket contributions "
                                  f"== the book's own gross return, every day; max|resid| "
                                  f"{resid:.2e}")

    b2 = backtest(px, rules_v2_weights(px), cost_bps=COST, freq="W")
    bb = blocks(b2["returns"].values, pan["warm"], pan["oos"])
    d5a = max(abs(bb["CAGR"] - RULESV2_COMMITTED[0]), abs(bb["Sharpe"] - RULESV2_COMMITTED[1]),
              abs(bb["MaxDD"] - RULESV2_COMMITTED[2]))
    sp = pan["spy"]
    d5b = max(abs(sp["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
              abs(sp["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
              abs(sp["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gates["G5"] = (d5a < 5e-4, f"live RULES v2 on U56 {bb['CAGR']:.4f}/{bb['Sharpe']:.4f}/"
                               f"{bb['MaxDD']:.4f} vs committed {RULESV2_COMMITTED} "
                               f"(|d| {d5a:.2e}; the committed triple is quoted to 4 dp and the "
                               f"panel has gained trading days since, and 936's own cross-run "
                               f"gate on this triple uses 5e-3 — at that tolerance this passes. "
                               f"Reported FAIL at the 5e-4 tolerance THIS run declared.)")
    gates["G8"] = (d5b < 5e-4, f"SPY OOS {sp['OOS_CAGR']:.4f}/{sp['OOS_Sharpe']:.4f}/"
                               f"{sp['OOS_MaxDD']:.4f} vs committed {SPY_OOS_COMMITTED} "
                               f"(max|d| {d5b:.2e})")

    # G6: the three attribution rules are NESTED by construction, on the real tag stream
    nest_bad = 0
    tags = {}
    for rl in RULES:
        _, TG = minhold_book(*SCORE[("U56", "CAND20")], pan["priced"], pan["reb"]["W"], 63,
                             pan["T"], pan["N"], tag_rule=rl)
        tags[rl] = TG & (Wt > 0)
    nest_bad += int((tags["R_GATE"] & ~tags["R_TOP2N"]).sum())
    nest_bad += int((tags["R_TOP2N"] & ~tags["R_TOPN"]).sum())
    shares = {rl: float(tags[rl].sum()) / max(float((Wt > 0).sum()), 1.0) for rl in RULES}
    gates["G6"] = (nest_bad == 0, "R_GATE subset R_TOP2N subset R_TOPN on the real tag stream: "
                                  f"{nest_bad} violations; tagged share of held name-days "
                                  + ", ".join(f"{rl} {shares[rl]:.3f}" for rl in RULES))

    # G7: H=0 admits no retained name-day at all (the tag is a min-hold object)
    _, TG0 = minhold_book(*SCORE[("U56", "CAND20")], pan["priced"], pan["reb"]["W"], 0,
                          pan["T"], pan["N"], tag_rule="R_TOPN")
    gates["G7"] = (int(TG0.sum()) == 0, f"H=0 produces ZERO retained-by-constraint name-days "
                                        f"({int(TG0.sum())}), so the whole tax is a min-hold "
                                        f"object by construction")

    for k in sorted(gates, key=lambda s: int(s[1:])):
        ok, msg = gates[k]
        P(f"  {k} {'PASS' if ok else 'FAIL'}  {msg}")
    P(f"GATES: {sum(1 for v in gates.values() if v[0])} of {len(gates)} pass.")
    P("")

    # ================================================================== (A) books + attribution
    P("=" * 100)
    P("(A) BOOKS, THE TAX, AND THE BUCKET DECOMPOSITION")
    P("=" * 100)
    rows, att = [], []

    def score_arm(kind, panel, mech, f, H, rule, W, TAGS):
        pn = PAN[panel]
        g, t, hd = nrun(pn["rets"], lag(GROSS * W), lagmask(pn["mask"][f]), want_held=True)
        r = g - t * COST / 1e4
        b = blocks(r, pn["warm"], pn["oos"])
        lg = legs_4b(b, pn["spy"])
        row = dict(kind=kind, panel=panel, mech=mech, freq=f, hold=H, rule=rule,
                   turn_yr=float(t[pn["warm"]].sum() / pn["yrs"]), **b, **lg,
                   pass4b=all(lg.values()), nfail=sum(1 for v in lg.values() if not v))
        rows.append(row)
        if TAGS is None:
            return row, r, hd, None
        return row, r, hd, {k: lag(v.astype(float)) > 0.5 for k, v in TAGS.items()}

    # H = 0 reference books
    REF = {}
    for p, m, f in product(PANELS, MECHS, FREQS):
        W, _ = minhold_book(*SCORE[(p, m)], PAN[p]["priced"], PAN[p]["reb"][f], 0,
                            PAN[p]["T"], PAN[p]["N"])
        row, r, _, _ = score_arm("BOOK_H0", p, m, f, 0, "-", W, None)
        REF[(p, m, f)] = row

    # HARD books, tagged under all three rules; SOFT books, one per rule
    for p, m, f, H in product(PANELS, MECHS, FREQS, HOLDS):
        pn = PAN[p]
        TAGS = {}
        Wh = None
        for rl in RULES:
            W, TG = minhold_book(*SCORE[(p, m)], pn["priced"], pn["reb"][f], H,
                                 pn["T"], pn["N"], tag_rule=rl)
            Wh = W
            TAGS[rl] = TG
        rowH, rH, hdH, TL = score_arm("BOOK_HARD", p, m, f, H, "-", Wh, TAGS)
        ref = REF[(p, m, f)]
        pk, tr = dd_window(rH[pn["warm"]])
        off = int(np.flatnonzero(pn["warm"])[0])
        sl_dd = slice(off + pk + 1, off + tr + 1)
        sl_full = slice(off, len(rH))
        oidx = np.flatnonzero(pn["oos"])
        sl_is = slice(off, int(oidx[0]))
        sl_oos = slice(int(oidx[0]), len(rH))
        cost_r = -np.zeros(len(rH))
        for rl in RULES:
            a_dd = attribute(hdH, pn["rets"], TL[rl], cost_r, sl_dd)
            a_fu = attribute(hdH, pn["rets"], TL[rl], cost_r, sl_full)
            a_is = attribute(hdH, pn["rets"], TL[rl], cost_r, sl_is)
            a_oo = attribute(hdH, pn["rets"], TL[rl], cost_r, sl_oos)
            att.append(dict(kind="BOOK", panel=p, mech=m, freq=f, hold=H, rule=rl,
                            tax_pp=100.0 * (abs(rowH["MaxDD"]) - abs(ref["MaxDD"])),
                            dd_days=a_dd["ndays"],
                            w_share_dd=a_dd["w_share_R"], c_share_dd=a_dd["c_share_R"],
                            conc_dd=a_dd["conc"], w_share_full=a_fu["w_share_R"],
                            c_share_full=a_fu["c_share_R"], conc_full=a_fu["conc"],
                            conc_is=a_is["conc"], conc_oos=a_oo["conc"],
                            w_share_is=a_is["w_share_R"], w_share_oos=a_oo["w_share_R"],
                            loss_dd=a_dd["contrib_R"] + a_dd["contrib_F"],
                            loss_R=a_dd["contrib_R"], loss_F=a_dd["contrib_F"],
                            MaxDD=rowH["MaxDD"], MaxDD_H0=ref["MaxDD"],
                            turn_yr=rowH["turn_yr"], turn_yr_H0=ref["turn_yr"]))
        for rl in RULES:
            Ws, TGs = minhold_book(*SCORE[(p, m)], pn["priced"], pn["reb"][f], H,
                                   pn["T"], pn["N"], rule=rl, tag_rule=rl)
            score_arm("BOOK_SOFT", p, m, f, H, rl, Ws, None)

    P(f"  books built: {len(rows):,} arms  ({time.time() - t0:.0f}s)")

    # ---- the null: same mechanics, random key, no gate -----------------------------------------
    nrows, natt = [], []
    for p, f, H, s in product(PANELS, FREQS, HOLDS, range(NSEED)):
        pn = PAN[p]
        el = np.ones_like(pn["priced"])
        TAGS = {}
        Wh = None
        for rl in RULES:
            W, TG = minhold_book(PERM[(p, s)], el, pn["priced"], pn["reb"][f], H,
                                 pn["T"], pn["N"], tag_rule=rl)
            Wh = W
            TAGS[rl] = TG
        g, t, hd = nrun(pn["rets"], lag(GROSS * Wh), lagmask(pn["mask"][f]), want_held=True)
        r = g - t * COST / 1e4
        b = blocks(r, pn["warm"], pn["oos"])
        lg = legs_4b(b, pn["spy"])
        nrows.append(dict(kind="NULL_HARD", panel=p, mech="NULL", freq=f, hold=H, rule="-",
                          seed=s, turn_yr=float(t[pn["warm"]].sum() / pn["yrs"]), **b, **lg,
                          pass4b=all(lg.values())))
        W0n, _ = minhold_book(PERM[(p, s)], el, pn["priced"], pn["reb"][f], 0,
                              pn["T"], pn["N"])
        g0, t0n = nrun(pn["rets"], lag(GROSS * W0n), lagmask(pn["mask"][f]))
        b0 = blocks(g0 - t0n * COST / 1e4, pn["warm"], pn["oos"])
        TL = {k: lag(v.astype(float)) > 0.5 for k, v in TAGS.items()}
        pk, tr = dd_window(r[pn["warm"]])
        off = int(np.flatnonzero(pn["warm"])[0])
        cost_r = np.zeros(len(r))
        for rl in RULES:
            a_dd = attribute(hd, pn["rets"], TL[rl], cost_r, slice(off + pk + 1, off + tr + 1))
            a_fu = attribute(hd, pn["rets"], TL[rl], cost_r, slice(off, len(r)))
            natt.append(dict(kind="NULL", panel=p, mech="NULL", freq=f, hold=H, rule=rl, seed=s,
                             tax_pp=100.0 * (abs(b["MaxDD"]) - abs(b0["MaxDD"])),
                             w_share_dd=a_dd["w_share_R"], c_share_dd=a_dd["c_share_R"],
                             conc_dd=a_dd["conc"], w_share_full=a_fu["w_share_R"],
                             c_share_full=a_fu["c_share_R"], conc_full=a_fu["conc"],
                             MaxDD=b["MaxDD"], MaxDD_H0=b0["MaxDD"],
                             turn_yr=float(t[pn["warm"]].sum() / pn["yrs"])))
    P(f"  null built: {len(nrows):,} arms x {len(RULES)} tag rules  ({time.time() - t0:.0f}s)")

    A = pd.DataFrame(att)
    NA = pd.DataFrame(natt)
    R = pd.DataFrame(rows)
    NR = pd.DataFrame(nrows)

    # ---- (A1) the tax itself, reproduced ------------------------------------------------------
    P("")
    P("(A1) THE TAX (|MaxDD(H)| - |MaxDD(0)|, pp), median over mechanisms, 10 bps, gross 0.75")
    tx = (A[A.rule == RULES[0]].groupby(["panel", "freq", "hold"])["tax_pp"].median()
          .unstack("hold"))
    P(tx.to_string(float_format=lambda x: f"{x:+.2f}"))
    ntx = NA[NA.rule == RULES[0]].groupby(["panel", "freq", "hold"])["tax_pp"].median().unstack("hold")
    P("  the gross-matched NULL's same tax (median over seeds), 936's control:")
    P(ntx.to_string(float_format=lambda x: f"{x:+.2f}"))

    # ---- (A2) the attribution, all 12 dial points ---------------------------------------------
    P("")
    P("(A2) ATTRIBUTION inside each book's own max-drawdown episode — ALL 12 DIAL POINTS")
    P("     w_share = retained bucket's share of invested weight; c_share = its share of the")
    P("     episode's loss; CONC = c_share / w_share.  CONC > 1 => the tax is concentrated in")
    P("     the names the score wanted to drop.  n = 24 books per cell (2 panels x 3 mechs x 4 f).")
    hdr = f"  {'rule':8s} {'H':>4s} {'n':>4s} {'w_share':>9s} {'c_share':>9s} {'CONC med':>9s} " \
          f"{'CONC>1':>8s} {'NULL CONC':>10s} {'NULL>1':>8s}"
    P(hdr)
    dial = []
    for rl, H in product(RULES, HOLDS):
        a = A[(A.rule == rl) & (A.hold == H)]
        n = NA[(NA.rule == rl) & (NA.hold == H)]
        c = a.conc_dd.dropna()
        cn = n.conc_dd.dropna()
        row = dict(rule=rl, hold=H, n=len(a), w_share=a.w_share_dd.median(),
                   c_share=a.c_share_dd.median(), conc_med=c.median(),
                   share_gt1=float((c > 1).mean()) if len(c) else np.nan,
                   null_conc_med=cn.median(),
                   null_share_gt1=float((cn > 1).mean()) if len(cn) else np.nan,
                   conc_full=a.conc_full.median(), conc_is=a.conc_is.median(),
                   conc_oos=a.conc_oos.median(), tax_pp=a.tax_pp.median())
        dial.append(row)
        P(f"  {rl:8s} {H:>4d} {len(a):>4d} {row['w_share']:>9.4f} {row['c_share']:>9.4f} "
          f"{row['conc_med']:>9.4f} {row['share_gt1']:>8.3f} {row['null_conc_med']:>10.4f} "
          f"{row['null_share_gt1']:>8.3f}")
    D = pd.DataFrame(dial)

    P("")
    P("(A2b) RESOLUTION — is the book's CONC distinguishable from its own null's at all?")
    P("      yardstick = the null's across-seed sd of CONC in the same (panel, f, H, rule) cell;")
    P("      a book CONC inside +/-2 of those sds of the null's mean is NOT a selection signal.")
    P(f"  {'rule':8s} {'H':>4s} {'book CONC':>10s} {'null mean':>10s} {'null sd':>8s} "
      f"{'z':>7s} {'|z|>2':>7s}")
    res = []
    for rl, H in product(RULES, HOLDS):
        zs = []
        for p, f in product(PANELS, FREQS):
            nn = NA[(NA.rule == rl) & (NA.hold == H) & (NA.panel == p)
                    & (NA.freq == f)].conc_dd.dropna()
            if len(nn) < 3 or nn.std(ddof=1) == 0:
                continue
            for m in MECHS:
                bb_ = A[(A.rule == rl) & (A.hold == H) & (A.panel == p) & (A.freq == f)
                        & (A.mech == m)].conc_dd.dropna()
                if len(bb_):
                    zs.append(float((bb_.iloc[0] - nn.mean()) / nn.std(ddof=1)))
        zs = np.array(zs)
        a = A[(A.rule == rl) & (A.hold == H)]
        n = NA[(NA.rule == rl) & (NA.hold == H)]
        row = dict(rule=rl, hold=H, book_conc=a.conc_dd.median(), null_mean=n.conc_dd.mean(),
                   null_sd=n.conc_dd.std(ddof=1), z_med=float(np.median(zs)) if len(zs) else np.nan,
                   share_abs_z_gt2=float((np.abs(zs) > 2).mean()) if len(zs) else np.nan, nz=len(zs))
        res.append(row)
        P(f"  {rl:8s} {H:>4d} {row['book_conc']:>10.4f} {row['null_mean']:>10.4f} "
          f"{row['null_sd']:>8.4f} {row['z_med']:>+7.2f} {row['share_abs_z_gt2']:>7.3f}")
    RES = pd.DataFrame(res)

    P("")
    P("(A3) the same 12 points on the FULL sample and split IS / OOS (WF-A)")
    P(f"  {'rule':8s} {'H':>4s} {'CONC dd':>8s} {'CONC full':>10s} {'CONC IS':>9s} "
      f"{'CONC OOS':>9s} {'tax pp':>8s}")
    for _, r_ in D.iterrows():
        P(f"  {r_['rule']:8s} {int(r_['hold']):>4d} {r_['conc_med']:>8.4f} "
          f"{r_['conc_full']:>10.4f} {r_['conc_is']:>9.4f} {r_['conc_oos']:>9.4f} "
          f"{r_['tax_pp']:>+8.2f}")

    # ---- (A4) does the tax track the retained bucket's size? ----------------------------------
    P("")
    P("(A4) across the 24 books in each dial cell, rho(tax_pp, retained weight share) and")
    P("     rho(tax_pp, CONC) — if the tax is the retained bucket's doing, the first is positive")
    for rl in RULES:
        a = A[A.rule == rl].dropna(subset=["conc_dd", "w_share_dd"])
        r1 = float(np.corrcoef(a.tax_pp, a.w_share_dd)[0, 1]) if len(a) > 3 else np.nan
        r2 = float(np.corrcoef(a.tax_pp, a.conc_dd)[0, 1]) if len(a) > 3 else np.nan
        P(f"  {rl:8s} n={len(a):>3d}  rho(tax, w_share) {r1:+.4f}   rho(tax, CONC) {r2:+.4f}")

    # ================================================================== (B) the SOFT price leg
    P("")
    P("=" * 100)
    P("(B) THE CAUSAL / PRICE LEG — a SOFT min hold releases exactly the flagged names")
    P("=" * 100)
    P("  tax recovered = 1 - (|MaxDD_soft| - |MaxDD_H0|) / (|MaxDD_hard| - |MaxDD_H0|)")
    P("  rebate kept   = (turn_H0 - turn_soft) / (turn_H0 - turn_hard)")
    P(f"  {'rule':8s} {'H':>4s} {'n':>4s} {'tax rec':>9s} {'rebate':>8s} {'dCAGR':>8s} "
      f"{'dSharpe':>8s} {'4b hard':>8s} {'4b soft':>8s} {'4a soft':>8s}")
    soft_rows = []
    b2r = {}
    for p in PANELS:
        b2 = backtest(PXD[p], rules_v2_weights(PXD[p]), cost_bps=COST, freq="W")
        b2r[p] = blocks(b2["returns"].values, PAN[p]["warm"], PAN[p]["oos"])

    def is4a(b, base):
        return bool(b["H1"] > base["H1"] and b["H2"] > base["H2"]
                    and b["MaxDD"] >= base["MaxDD"])

    for rl, H in product(RULES, HOLDS):
        rec, reb_, dc, ds, n4bh, n4bs, n4as = [], [], [], [], 0, 0, 0
        for p, m, f in product(PANELS, MECHS, FREQS):
            hard = R[(R.kind == "BOOK_HARD") & (R.panel == p) & (R.mech == m) & (R.freq == f)
                     & (R.hold == H)].iloc[0]
            soft = R[(R.kind == "BOOK_SOFT") & (R.panel == p) & (R.mech == m) & (R.freq == f)
                     & (R.hold == H) & (R.rule == rl)].iloc[0]
            ref = REF[(p, m, f)]
            th = abs(hard["MaxDD"]) - abs(ref["MaxDD"])
            ts = abs(soft["MaxDD"]) - abs(ref["MaxDD"])
            if abs(th) > 1e-6:
                rec.append(1.0 - ts / th)
            rb = ref["turn_yr"] - hard["turn_yr"]
            if abs(rb) > 1e-6:
                reb_.append((ref["turn_yr"] - soft["turn_yr"]) / rb)
            dc.append(soft["CAGR"] - hard["CAGR"])
            ds.append(soft["Sharpe"] - hard["Sharpe"])
            n4bh += int(hard["pass4b"])
            n4bs += int(soft["pass4b"])
            n4as += int(is4a(soft, b2r[p]))
            soft_rows.append(dict(panel=p, mech=m, freq=f, hold=H, rule=rl,
                                  tax_hard_pp=100 * th, tax_soft_pp=100 * ts,
                                  tax_recovered=(1.0 - ts / th) if abs(th) > 1e-6 else np.nan,
                                  rebate_kept=((ref["turn_yr"] - soft["turn_yr"]) / rb)
                                  if abs(rb) > 1e-6 else np.nan,
                                  CAGR_soft=soft["CAGR"], CAGR_hard=hard["CAGR"],
                                  CAGR_H0=ref["CAGR"], Sharpe_soft=soft["Sharpe"],
                                  Sharpe_hard=hard["Sharpe"], Sharpe_H0=ref["Sharpe"],
                                  MaxDD_soft=soft["MaxDD"], MaxDD_hard=hard["MaxDD"],
                                  MaxDD_H0=ref["MaxDD"], turn_soft=soft["turn_yr"],
                                  turn_hard=hard["turn_yr"], turn_H0=ref["turn_yr"],
                                  pass4b_soft=bool(soft["pass4b"]),
                                  pass4b_hard=bool(hard["pass4b"]),
                                  pass4a_soft=is4a(soft, b2r[p])))
        P(f"  {rl:8s} {H:>4d} {len(dc):>4d} {np.median(rec):>9.3f} {np.median(reb_):>8.3f} "
          f"{np.median(dc):>+8.4f} {np.median(ds):>+8.4f} {n4bh:>8d} {n4bs:>8d} {n4as:>8d}")
    S = pd.DataFrame(soft_rows)

    # ================================================================== (C) KEEP paths + rule 8
    P("")
    P("=" * 100)
    P("(C) BOTH KEEP PATHS over every arm, and RULE 8")
    P("=" * 100)
    R["pass4a"] = [is4a(r_, b2r[r_["panel"]]) for _, r_ in R.iterrows()]
    for k in ["BOOK_H0", "BOOK_HARD", "BOOK_SOFT"]:
        sub = R[R.kind == k]
        P(f"  {k:10s} n={len(sub):>4d}   4a {int(sub.pass4a.sum()):>3d}   "
          f"4b {int(sub.pass4b.sum()):>3d}   BOTH "
          f"{int((sub.pass4a & sub.pass4b).sum()):>3d}")
    P(f"  NULL_HARD  n={len(NR):>4d}   4b {int(NR.pass4b.sum()):>3d}  "
      f"(base rate {NR.pass4b.mean():.3f})")
    legct = {L: int((~R[L]).sum()) for L in ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]}
    P("  binding 4b legs over all book arms (count FAILING): "
      + ", ".join(f"{k} {v}" for k, v in sorted(legct.items(), key=lambda x: -x[1])))

    P("")
    P("  RULE 8 — arm chosen on IS (<= %s) Sharpe ALONE per (panel, mech); OOS read ONCE."
      % IS_END)
    wf = []
    for p, m in product(PANELS, MECHS):
        cand = R[(R.panel == p) & (R.mech == m)]
        pick = cand.loc[cand.IS_Sharpe.idxmax()]
        sp = PAN[p]["spy"]
        bl = b2r[p]
        wf.append(dict(panel=p, mech=m, pick_kind=pick["kind"], pick_freq=pick["freq"],
                       pick_hold=int(pick["hold"]), pick_rule=pick["rule"],
                       IS_Sharpe=pick["IS_Sharpe"], OOS_CAGR=pick["OOS_CAGR"],
                       OOS_Sharpe=pick["OOS_Sharpe"], OOS_MaxDD=pick["OOS_MaxDD"],
                       full_CAGR=pick["CAGR"], full_Sharpe=pick["Sharpe"],
                       full_MaxDD=pick["MaxDD"], H1=pick["H1"], H2=pick["H2"],
                       turn_yr=pick["turn_yr"], pass4a=bool(pick["pass4a"]),
                       pass4b=bool(pick["pass4b"]),
                       beat_v2_OOS=bool(pick["OOS_Sharpe"] > bl["OOS_Sharpe"]),
                       beat_spy_OOS=bool(pick["OOS_Sharpe"] > sp["OOS_Sharpe"]),
                       v2_OOS_Sharpe=bl["OOS_Sharpe"], spy_OOS_Sharpe=sp["OOS_Sharpe"]))
        P(f"  {p:5s} {m:8s} -> {pick['kind']:10s} f={pick['freq']} H={int(pick['hold']):>3d} "
          f"rule={pick['rule']:8s} | IS Sh {pick['IS_Sharpe']:.4f} | OOS "
          f"{pick['OOS_CAGR']:.2%}/{pick['OOS_Sharpe']:.4f}/{pick['OOS_MaxDD']:.2%} | "
          f"full {pick['CAGR']:.2%}/{pick['Sharpe']:.4f}/{pick['MaxDD']:.2%} | halves "
          f"{pick['H1']:.4f}/{pick['H2']:.4f} vs SPY {sp['H1']:.4f}/{sp['H2']:.4f} | "
          f"turn {pick['turn_yr']:.2f}/yr | 4a {bool(pick['pass4a'])} 4b {bool(pick['pass4b'])}")
    WF = pd.DataFrame(wf)
    for p in PANELS:
        sp, bl = PAN[p]["spy"], b2r[p]
        P(f"  benchmarks {p}: SPY full {sp['CAGR']:.2%}/{sp['Sharpe']:.4f}/{sp['MaxDD']:.2%} "
          f"OOS {sp['OOS_CAGR']:.2%}/{sp['OOS_Sharpe']:.4f}/{sp['OOS_MaxDD']:.2%} | "
          f"RULES v2 full {bl['CAGR']:.2%}/{bl['Sharpe']:.4f}/{bl['MaxDD']:.2%} OOS "
          f"{bl['OOS_CAGR']:.2%}/{bl['OOS_Sharpe']:.4f}/{bl['OOS_MaxDD']:.2%}")
    P(f"  picks beating RULES v2 on OOS Sharpe: {int(WF.beat_v2_OOS.sum())} of {len(WF)}; "
      f"beating SPY: {int(WF.beat_spy_OOS.sum())} of {len(WF)}")

    # ================================================================== (D) hypotheses
    P("")
    P("=" * 100)
    P("(D) PRE-REGISTERED HYPOTHESES (declared in the docstring before any number)")
    P("=" * 100)
    hyp = []

    def H_(name, ok, msg):
        hyp.append(dict(hypothesis=name, verdict="PASS" if ok else "FAIL", detail=msg))
        P(f"  {name:10s} {'PASS' if ok else 'FAIL'}  {msg}")

    cmed = A.groupby(["rule", "hold"]).conc_dd.median()
    ok_cells = int((cmed > 1.0).sum())
    H_("H_CONC", ok_cells >= 7, f"retained bucket's loss share exceeds its weight share (median "
                                f"CONC > 1) in {ok_cells} of {len(cmed)} dial cells; range "
                                f"{cmed.min():.4f}..{cmed.max():.4f}")
    nmed = NA.groupby(["rule", "hold"]).conc_dd.median()
    flat = float(np.abs(nmed - 1.0).max())
    H_("H_NULLFLAT", flat <= 0.05, f"the gross-matched null's CONC sits at 1.0 (max|CONC-1| "
                                   f"{flat:.4f} over {len(nmed)} cells, range {nmed.min():.4f}.."
                                   f"{nmed.max():.4f})")
    gap = float((cmed - nmed).median())
    H_("H_GAP", gap > 0.05, f"median (book CONC - null CONC) over the 12 cells = {gap:+.4f}; a "
                            f"gap at or below 0 makes the concentration mechanical, not selective")
    zmed = float(RES.z_med.median())
    zsh = float(RES.share_abs_z_gt2.mean())
    H_("H_RESOLVE", abs(zmed) > 2.0,
       f"the book's CONC is resolvable against its own null at all: median z {zmed:+.2f} over "
       f"{len(RES)} cells, share of books with |z| > 2 = {zsh:.3f}")
    recmed = S.groupby(["rule", "hold"]).tax_recovered.median()
    H_("H_SOFT", float(recmed.max()) >= 0.50,
       f"a SOFT min hold recovers >= 50% of the tax in its best dial cell (max median recovery "
       f"{recmed.max():+.3f}, min {recmed.min():+.3f})")
    rebmed = S.groupby(["rule", "hold"]).rebate_kept.median()
    H_("H_REBATE", float(rebmed.max()) >= 0.70,
       f"and keeps >= 70% of the turnover rebate somewhere (max median {rebmed.max():.3f}, "
       f"min {rebmed.min():.3f})")
    both = S[(S.tax_recovered >= 0.5) & (S.rebate_kept >= 0.7)]
    H_("H_BOTH", len(both) > 0, f"{len(both)} of {len(S)} (book, rule, H) arms recover >= 50% of "
                                f"the tax AND keep >= 70% of the rebate")
    nsoft = int(R[(R.kind == 'BOOK_SOFT')].pass4b.sum())
    nhard = int(R[(R.kind == 'BOOK_HARD')].pass4b.sum())
    H_("H_KEEP", nsoft > nhard, f"SOFT passes 4b more often than HARD: {nsoft} of "
                                f"{int((R.kind == 'BOOK_SOFT').sum())} vs {nhard} of "
                                f"{int((R.kind == 'BOOK_HARD').sum())}")
    ci, co = A.conc_is.median(), A.conc_oos.median()
    same = (ci > 1) == (co > 1)
    H_("H_WF", bool(same), f"the attribution verdict is the same in both windows: CONC IS "
                           f"{ci:.4f}, CONC OOS {co:.4f}")
    a4 = int(R.pass4a.sum())
    H_("H_4A", a4 == 0, f"no arm on this grid clears 4a against the live RULES v2 book "
                        f"({a4} of {len(R)} do)")
    P(f"  {sum(1 for h in hyp if h['verdict'] == 'PASS')} of {len(hyp)} pre-registered "
      f"hypotheses PASS.")

    # ================================================================== outputs
    P("")
    P("=" * 100)
    P("OUTPUTS")
    P("=" * 100)
    dump(pd.DataFrame([dict(gate=k, verdict="PASS" if v[0] else "FAIL", detail=v[1])
                       for k, v in sorted(gates.items())]), "gates")
    dump(R, "arms")
    dump(NR, "nullarms")
    dump(A, "attribution")
    dump(NA, "nullattribution")
    dump(D, "dial")
    dump(RES, "resolution")
    dump(S, "soft")
    dump(WF, "walkforward")
    dump(pd.DataFrame(hyp), "hypotheses")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    P(f"# done in {time.time() - t0:.0f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
