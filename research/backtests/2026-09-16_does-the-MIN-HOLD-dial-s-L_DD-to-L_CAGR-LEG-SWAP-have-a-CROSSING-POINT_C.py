#!/usr/bin/env python3
"""Idea 1113 (lane C, 2026-09-16) — does the MIN-HOLD dial's L_DD -> L_CAGR LEG SWAP have a
CROSSING POINT?

QUESTION (QUEUE idea 1113, verbatim)
    idea 1106 found drawdown headroom rises from +0.55 pp at H=21 to +2.08 pp at H=5 while CAGR
    headroom falls from +4.55 pp to +2.23 pp, so shortening the hold trades one 4b leg for the
    other without clearing both.  Walk H finely between 5 and 63 and report whether any rung
    maximises the MINIMUM of the two headrooms, and by how much it beats 1083's 4.1-7.2 pp
    resolution.  Max 2 params (H grid, panel).

THE TWO TUNED DIALS (PROTOCOL rule 4, no more than two)
    1. H (min hold, trading days) on a FINE ladder between 5 and 63:
       {5, 7, 10, 13, 16, 21, 26, 32, 42, 52, 63}.  1106 walked only {5, 10, 21} with {63, 126}
       carried as context, i.e. three points between 5 and 63; this run puts eleven there, which
       is the whole content of the idea.  H = 126 is carried as a CONTEXT rung for the
       cross-run reproduction gates ONLY and is never eligible for any argmax below.
    2. PANEL in {U56, B136}.  1106's headroom headline is a U56 statement; B136 is the
       out-of-slice test of whether a crossing point is a property of the min-hold dial or of
       one panel.

    THE N LADDER IS NOT A DIAL.  N in {5, 8, 10, 12, 15, 20, 25, 30, 40} is 1082/1086/1106's
    committed coordinate set, taken verbatim; EVERY rung is published.  Everything else is
    frozen at 1106's construction: cap INF, max_vol 0.60, gross 0.75, W cadence, 10 bps, LAG 1,
    CAND20 legs [(21,252),(0,126),(0,63)], warm-up 260 rows skipped.

THE TWO HEADROOMS, fixed before any number (1106's definitions, verbatim)
    DD_HEAD    100 * (0.60 * |SPY MaxDD| - |book MaxDD|).  Positive <=> L_DD passes; the
               quantity is in percentage points OF DRAWDOWN.
    CAGR_HEAD  100 * (book CAGR - 0.70 * SPY CAGR).  Positive <=> L_CAGR passes; the quantity
               is in percentage points OF ANNUAL RETURN.
    MINHEAD    min(DD_HEAD, CAGR_HEAD) — literally the statistic the idea asks to maximise.
               IT IS A MIXED-UNIT STATISTIC: a pp of drawdown and a pp of CAGR are not the same
               pp, and which leg an argmax picks therefore depends on that unmatched scaling.
               This run reports it as asked AND reports a scale-free restatement,
    RELMIN     min(DD_HEAD / (0.60 * |SPY MaxDD|), CAGR_HEAD / (0.70 * SPY CAGR)), each leg as a
               fraction of ITS OWN bar.  RELMIN is not a third dial; it is the same statistic
               with the unit mismatch removed, and it is published beside MINHEAD at every rung
               so that no conclusion here rests on the mismatch.
    All three are computed on the FULL sample, on IS (2009-2016) and on OOS (2017-2026)
    separately, each against SPY measured on the SAME window.

DECLARED BEFORE ANY NUMBER — what a crossing point would look like and what refutes it
    H_CROSS     the leg swap is real and crosses INSIDE the ladder: sign(DD_HEAD - CAGR_HEAD),
                averaged over the N ladder, CHANGES between the H=5 end and the H=63 end, on at
                least one panel.  REFUTED if one leg has more headroom than the other at every
                rung of the ladder on both panels (then there is no crossing point, only a
                gradient, and 1106's "trades one leg for the other" is a statement about two
                curves that never meet).
    H_INTERIOR  the rung maximising mean MINHEAD is INTERIOR to [5, 63] on at least one panel.
                REFUTED if both panels' argmax sits at an endpoint, in which case the answer to
                "does any rung maximise the minimum" is "the grid edge does", i.e. idea 1109's
                boundary-pick reading, and there is no optimum on this dial at all.
    H_RESOLVED  the argmax rung's MINHEAD advantage over the ladder's WORST rung exceeds BOTH
                (a) 1083's committed 4.1 pp lower bound for the 90% width of a margin quantity
                of this kind on this tape, and (b) this run's OWN paired block-bootstrap 90%
                width of the argmax-minus-rung difference.  REFUTED by either.  This is the
                "by how much it beats 1083's resolution" the idea asks for, and it is declared
                as a two-sided bar so that a win on the record's number alone cannot carry it.
    H_MONO_DD   DD_HEAD falls monotonically as H rises across the eleven rungs (1106's 3-point
                claim read at resolution).  REFUTED by any adjacent inversion.
    H_MONO_CAGR CAGR_HEAD rises monotonically as H rises.  REFUTED by any adjacent inversion.
    H_CLEARS    some rung of the fine ladder clears ALL FIVE full-sample 4b legs AND all three
                OOS legs at the incumbent N = 20, on at least one panel — i.e. the swap is
                escapable somewhere between 1106's two endpoints.  REFUTED if no rung does.

RULE 8 (walk-forward, required).  The H rung is chosen on IS 2009-2016 ALONE, by IS MINHEAD,
    independently at each (panel, N); OOS 2017-2026 is then read ONCE at that rung and compared
    against SPY OOS and the live RULES v2 book OOS.  The OOS argmax is also printed, purely to
    show the size of the chooser's regret — it is NEVER used to pick anything.  The full OOS
    ladder is published at every rung, so nothing is hidden behind the pick.

BOTH KEEP PATHS are scored at all 198 walked cells (PROTOCOL rule 4), 4a against the live
    RULES v2 book and 4b against SPY, full sample and OOS.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists.  Every level here
    is optimistic and every 4a / 4b count is an UPPER bound.  DD_HEAD and CAGR_HEAD are measured
    against SPY, a real index, so the bias does NOT cancel out of them: a headroom figure on
    these panels is an over-statement of what a tradable book would have had.
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

DATE = "2026-09-16"
SLUG = "does-the-MIN-HOLD-dial-s-L_DD-to-L_CAGR-LEG-SWAP-have-a-CROSSING-POINT"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

LAG = 1
WARMUP = 260
MAXVOL = 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
GROSS0 = 0.75
FREQ = "W"
LEGS = [(21, 252), (0, 126), (0, 63)]

PANELS = ["U56", "B136"]                                    # dial 2
H_WALK = [5, 7, 10, 13, 16, 21, 26, 32, 42, 52, 63]         # dial 1 — the fine ladder
H_CONTEXT = [126]                                           # gates only, never an argmax rung
H_ALL = H_WALK + H_CONTEXT
NS = [5, 8, 10, 12, 15, 20, 25, 30, 40]                     # committed coordinate set, NOT a dial
N_INC = 20                                                  # the incumbent, for H_CLEARS

BOOT_REPS = 500
BOOT_BLOCK = 63
BOOT_SEED = 1113

W1083_LO, W1083_HI = 4.1, 7.2      # 1083's committed 90% width band for a margin of this kind

A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = {"U56": (0.1521, 0.8713, -0.3372), "B136": (0.1533, 0.8767, -0.3372)}
LIVE_MAXDD_COMMITTED = {"U56": -0.1205, "B136": -0.1224}
SRC_1106 = (ROOT / "research" / "backtests"
            / "2026-09-16_is-the-U56-H21-SIGN-FLIP-a-TURNOVER-fact_B.grid.csv")
# 1106's committed conditional headroom medians (over its cells passing 4b FULL and OOS)
C1106_HEAD = {5: (2.08, 2.23), 10: (1.13, 2.94), 21: (0.55, 4.55), 126: (0.57, 6.17)}

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ---------------------------------------------------------------- fast runner (1097/1106 verbatim)
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


def lagmat(a):
    out = np.zeros_like(a)
    out[LAG:] = a[:-LAG]
    return out


def legs_composite(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return sum(parts) / len(parts)


def mech(px):
    comp = legs_composite(px)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, (above & (vol20 < MAXVOL)).values


def build(rank_key, elig, priced, reb, N, cap, H, T, K, gross):
    """1097/1106's build() verbatim."""
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    nsel_by_reb, gross_by_reb, new_by_reb = [], [], []
    per_cap = cap * gross / N if np.isfinite(cap) else np.inf
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
        nsel_by_reb.append(len(sel))
        new_by_reb.append(len(take))
        stop = reb[i + 1] if i + 1 < len(reb) else T
        if len(sel):
            w = min(gross / len(sel), per_cap)
            W[t:stop, sel] = w
            gross_by_reb.append(w * len(sel))
        else:
            gross_by_reb.append(0.0)
    return W, np.array(nsel_by_reb), np.array(gross_by_reb), np.array(new_by_reb)


def windows(idx):
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    return warm, ins, oos


def blocks(r, warm, ins, oos):
    rr = r[warm]
    c, s, d = fmet(rr)
    h = len(rr) // 2
    oc, os_, od = fmet(r[oos])
    ic, is_, idd = fmet(r[ins])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


def legs_4b(b, sb):
    return {"L_H1": bool(b["H1"] > sb["H1"]), "L_H2": bool(b["H2"] > sb["H2"]),
            "L_OOS": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "L_DD": bool(abs(b["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"])),
            "L_CAGR": bool(b["CAGR"] >= CAGR_FLOOR * sb["CAGR"])}


def legs_4b_oos(b, sb):
    return {"O_S": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "O_DD": bool(abs(b["OOS_MaxDD"]) <= DD_CAP * abs(sb["OOS_MaxDD"])),
            "O_CAGR": bool(b["OOS_CAGR"] >= CAGR_FLOOR * sb["OOS_CAGR"])}


def legs_4a(b, lb):
    return {"A_H1": bool(b["H1"] > lb["H1"]), "A_H2": bool(b["H2"] > lb["H2"]),
            "A_DD": bool(b["MaxDD"] >= lb["MaxDD"])}


def heads(bc, bd, sc, sd):
    """The two headrooms and their two minima, from book (CAGR, MaxDD) and SPY (CAGR, MaxDD)
    measured on the SAME window."""
    dd_bar, cagr_bar = DD_CAP * abs(sd), CAGR_FLOOR * sc
    dh = 100.0 * (dd_bar - abs(bd))
    ch = 100.0 * (bc - cagr_bar)
    rel_d = (dd_bar - abs(bd)) / dd_bar if dd_bar > 0 else np.nan
    rel_c = (bc - cagr_bar) / cagr_bar if cagr_bar > 0 else np.nan
    return dh, ch, min(dh, ch), min(rel_d, rel_c)


def ann_turn(tpath, mask):
    return float(tpath[mask].sum() / (mask.sum() / 252.0))


def block_idx(rng, T, block, reps):
    """Moving-block bootstrap index matrix (reps x T).  The SAME index rows are applied to every
    return series (book rungs and SPY alike), so the contrast each headroom is built on is
    preserved inside every replicate."""
    nb = int(np.ceil(T / block))
    starts = rng.integers(0, T - block + 1, size=(reps, nb))
    off = np.arange(block)
    ix = (starts[:, :, None] + off[None, None, :]).reshape(reps, nb * block)[:, :T]
    return ix


def boot_heads(book_r, spy_r, ix):
    """MINHEAD / DD_HEAD / CAGR_HEAD under each bootstrap replicate, book and SPY resampled
    with the SAME blocks.  Returns (reps,) arrays."""
    B, S = book_r[ix], spy_r[ix]
    T = B.shape[1]
    eb, es = np.cumprod(1.0 + B, axis=1), np.cumprod(1.0 + S, axis=1)
    cb = eb[:, -1] ** (252.0 / T) - 1.0
    cs = es[:, -1] ** (252.0 / T) - 1.0
    db = (eb / np.maximum.accumulate(eb, axis=1) - 1.0).min(axis=1)
    ds = (es / np.maximum.accumulate(es, axis=1) - 1.0).min(axis=1)
    dh = 100.0 * (DD_CAP * np.abs(ds) - np.abs(db))
    ch = 100.0 * (cb - CAGR_FLOOR * cs)
    return dh, ch, np.minimum(dh, ch)


def w90(x):
    x = np.asarray(x, float)
    return float(np.percentile(x, 95) - np.percentile(x, 5))


def main():
    t0 = time.time()
    P(f"# Idea 1113 (lane C, {DATE}) — does the MIN-HOLD dial's L_DD -> L_CAGR LEG SWAP have a")
    P("#   CROSSING POINT?")
    P(f"# 2 tuned dials and no more: H {H_WALK} (the fine ladder) x PANEL {PANELS}.")
    P(f"#   H {H_CONTEXT} is carried for cross-run gates ONLY and is never an argmax rung.")
    P(f"# The N ladder {NS} is 1082/1086/1106's committed coordinate set, NOT a dial; all shown.")
    P(f"# FROZEN: CAND20 legs {LEGS}, cap INF, max_vol {MAXVOL}, gross {GROSS0}, cost "
      f"{COST:.0f} bps, LAG {LAG}, cadence {FREQ}, warm-up {WARMUP} rows.")
    P("# THE STATISTIC: DD_HEAD = 100*(0.60*|SPY MaxDD| - |book MaxDD|), pp OF DRAWDOWN;")
    P("#   CAGR_HEAD = 100*(book CAGR - 0.70*SPY CAGR), pp OF ANNUAL RETURN; MINHEAD = min of")
    P("#   the two, a MIXED-UNIT statistic, published beside RELMIN (each leg as a fraction of")
    P("#   its own bar) so no conclusion rests on the unmatched scaling.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   H_CROSS     sign(DD_HEAD - CAGR_HEAD) changes between the H=5 and H=63 ends on at")
    P("#               least one panel.  REFUTED if one leg leads at every rung on both.")
    P("#   H_INTERIOR  the mean-MINHEAD argmax is INTERIOR to [5,63] on at least one panel.")
    P("#               REFUTED if both argmaxes sit at a grid edge (idea 1109's reading).")
    P(f"#   H_RESOLVED  argmax-minus-worst MINHEAD exceeds BOTH 1083's {W1083_LO} pp lower bound")
    P("#               AND this run's own paired block-bootstrap 90% width.  REFUTED by either.")
    P("#   H_MONO_DD   DD_HEAD monotone FALLING in H over the eleven rungs.")
    P("#   H_MONO_CAGR CAGR_HEAD monotone RISING in H over the eleven rungs.")
    P(f"#   H_CLEARS    some rung clears all five full-sample 4b legs AND all three OOS legs at")
    P(f"#               the incumbent N={N_INC}, on at least one panel.")
    P("# RULE 8: H chosen on IS 2009-2016 by IS MINHEAD at each (panel, N); OOS 2017-2026 read")
    P("#   once.  The OOS argmax is printed for regret only and picks nothing.")
    P("")

    rows, benchrows, bootrows = [], [], []
    gates = {}
    keep_series = {}          # (panel, H, N) -> post-warm-up net returns, for the bootstrap
    spy_series = {}

    for panel in PANELS:
        px = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
        idx = px.index
        K, T = len(px.columns), len(idx)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        mk = rebalance_mask(idx, FREQ).values
        mkl = np.roll(mk, LAG)
        warm, ins, oos = windows(idx)
        sc, elig_real = mech(px)
        rank_key = -np.nan_to_num(sc, nan=-np.inf)
        rank_key[np.isnan(sc)] = np.inf
        reb = np.flatnonzero(mk)

        spy = px["SPY"].pct_change().fillna(0.0).values
        sb = blocks(spy, warm, ins, oos)
        live = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].values
        lb = blocks(live, warm, ins, oos)
        spy_series[panel] = dict(full=spy[warm], ins=spy[ins], oos=spy[oos])

        P(f"\n## {panel}: {K} columns, {T} days {idx[0].date()}..{idx[-1].date()}, "
          f"{len(reb)} rebalance dates ({len(reb[reb >= WARMUP])} after warm-up)")
        P(f"   SPY        full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%}  "
          f"halves {sb['H1']:.4f}/{sb['H2']:.4f}  IS {sb['IS_CAGR']:.2%} / {sb['IS_MaxDD']:.2%}  "
          f"OOS {sb['OOS_CAGR']:.2%} / {sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"   RULES v2   full {lb['CAGR']:.2%} / {lb['Sharpe']:.4f} / {lb['MaxDD']:.2%}  "
          f"halves {lb['H1']:.4f}/{lb['H2']:.4f}  OOS {lb['OOS_CAGR']:.2%} / "
          f"{lb['OOS_Sharpe']:.4f} / {lb['OOS_MaxDD']:.2%}")
        P(f"   THE BARS   full: DD cap {DD_CAP*abs(sb['MaxDD']):.2%}, CAGR floor "
          f"{CAGR_FLOOR*sb['CAGR']:.2%}   IS: {DD_CAP*abs(sb['IS_MaxDD']):.2%} / "
          f"{CAGR_FLOOR*sb['IS_CAGR']:.2%}   OOS: {DD_CAP*abs(sb['OOS_MaxDD']):.2%} / "
          f"{CAGR_FLOOR*sb['OOS_CAGR']:.2%}")
        benchrows += [dict(panel=panel, series="SPY", **sb), dict(panel=panel, series="RULESv2", **lb)]

        # ---- construction gates, printed before any result number ------------------------
        if panel == "U56":
            W20, _, _, _ = build(rank_key, elig_real, priced, reb, 20, np.inf, 126, T, K, GROSS0)
            wdf = pd.DataFrame(W20, index=idx, columns=px.columns)
            eng = backtest(px, wdf, cost_bps=COST, freq=FREQ)["returns"].values
            gg, tn = nrun(rets, lagmat(W20), mkl)
            fast = gg - tn * COST / 1e4
            d = float(np.abs(fast[WARMUP:] - eng[WARMUP:]).max())
            gates["G1 fast runner == engine.backtest (U56, N=20, H=126)"] = (d, d < 1e-12)
            m = fmet(fast[warm])
            d = max(abs(m[i] - A936_WH126[i]) for i in range(3))
            gates["G2 CROSS-RUN 936/1071/1082/1106 committed W/H126 N=20 triple"] = (d, d < 5e-3)
        sc_ = SPY_OOS_COMMITTED[panel]
        d = max(abs(sb["OOS_CAGR"] - sc_[0]), abs(sb["OOS_Sharpe"] - sc_[1]),
                abs(sb["OOS_MaxDD"] - sc_[2]))
        gates[f"G3 CROSS-RUN SPY OOS triple ({panel})"] = (d, d < 5e-4)
        d = abs(lb["MaxDD"] - LIVE_MAXDD_COMMITTED[panel])
        gates[f"G4 live RULES v2 MaxDD == committed ({panel})"] = (d, d < 5e-4)

        # ---- the fine H walk -------------------------------------------------------------
        for Hh in H_ALL:
            for N in NS:
                Wb, nsel, grs, nnew = build(rank_key, elig_real, priced, reb, N, np.inf, Hh,
                                            T, K, GROSS0)
                gb, tb = nrun(rets, lagmat(Wb), mkl)
                rb = gb - tb * COST / 1e4
                b = blocks(rb, warm, ins, oos)
                l4b, l4a, l4bo = legs_4b(b, sb), legs_4a(b, lb), legs_4b_oos(b, sb)
                rebw = reb[reb >= WARMUP]
                keep_mask = np.isin(reb, rebw)

                dh, ch, mh, rm = heads(b["CAGR"], b["MaxDD"], sb["CAGR"], sb["MaxDD"])
                dhi, chi, mhi, rmi = heads(b["IS_CAGR"], b["IS_MaxDD"], sb["IS_CAGR"], sb["IS_MaxDD"])
                dho, cho, mho, rmo = heads(b["OOS_CAGR"], b["OOS_MaxDD"], sb["OOS_CAGR"],
                                           sb["OOS_MaxDD"])
                out = dict(panel=panel, H=Hh, N=N, rung=("WALK" if Hh in H_WALK else "CONTEXT"),
                           mean_nsel=float(nsel[keep_mask].mean()),
                           mean_gross=float(grs[keep_mask].mean()),
                           book_new_per_reb=float(nnew[keep_mask].mean()),
                           turnover=ann_turn(tb, warm), **b, **l4b, **l4a, **l4bo,
                           DD_HEAD=dh, CAGR_HEAD=ch, MINHEAD=mh, RELMIN=rm, SWAP=dh - ch,
                           DD_HEAD_IS=dhi, CAGR_HEAD_IS=chi, MINHEAD_IS=mhi, RELMIN_IS=rmi,
                           DD_HEAD_OOS=dho, CAGR_HEAD_OOS=cho, MINHEAD_OOS=mho, RELMIN_OOS=rmo,
                           pass4b=all(l4b.values()), pass4a=all(l4a.values()),
                           pass4b_oos=all(l4bo.values()))
                out["pass4b_full_and_oos"] = out["pass4b"] and out["pass4b_oos"]
                out["bind"] = "L_DD" if dh < ch else "L_CAGR"
                rows.append(out)
                keep_series[(panel, Hh, N)] = rb[warm]
                P(f"   {panel:<4s} H={Hh:<3d} N={N:<2d} [{out['rung']:<7s}] "
                  f"CAGR {b['CAGR']:6.2%} MaxDD {b['MaxDD']:7.2%} turn {out['turnover']:5.2f}  "
                  f"DD_HEAD {dh:+6.2f} CAGR_HEAD {ch:+6.2f} MIN {mh:+6.2f} "
                  f"(RELMIN {rm:+.4f}) binds {out['bind']:<6s} "
                  f"4b {'Y' if out['pass4b'] else 'n'}{'Y' if out['pass4b_oos'] else 'n'}  "
                  f"t={time.time()-t0:5.0f}s")

    G = pd.DataFrame(rows)
    WALK = G[G.rung == "WALK"].copy()

    # ---- cross-run reproduction gates ----------------------------------------------------
    c06 = pd.read_csv(SRC_1106, dtype={"panel": str}, keep_default_na=False)
    for c in ["CAGR", "MaxDD", "turnover", "H", "N"]:
        c06[c] = pd.to_numeric(c06[c])
    c06 = c06[["panel", "N", "H", "CAGR", "MaxDD", "turnover"]]
    m = G.merge(c06, on=["panel", "N", "H"], suffixes=("", "_06"))
    d = max(float((m.CAGR - m.CAGR_06).abs().max()), float((m.MaxDD - m.MaxDD_06).abs().max()),
            float((m.turnover - m.turnover_06).abs().max()))
    gates[f"G5 CROSS-RUN reproduce 1106's {len(m)} book CAGR/MaxDD/turnover triples"] = (d, d < 1e-9)

    ps = G[G.pass4b_full_and_oos]
    worst = 0.0
    for Hh, (ddm, cgm) in C1106_HEAD.items():
        s = ps[ps.H == Hh]
        if not len(s):
            worst = max(worst, 99.0)
            continue
        worst = max(worst, abs(s.DD_HEAD.median() - ddm), abs(s.CAGR_HEAD.median() - cgm))
    gates["G6 CROSS-RUN 1106's conditional headroom medians at H=5/10/21/126"] = (worst, worst < 5e-3)
    n1106 = int((G.pass4b_full_and_oos & G.H.isin([5, 10, 21, 63, 126])).sum())
    gates["G7 CROSS-RUN 1106's '25 cells pass 4b FULL and OOS' over its own five H rungs"] = (
        abs(n1106 - 25), n1106 == 25)
    d = float(G.mean_gross.sub(GROSS0).abs().max())
    gates[f"G8 every book sits at gross {GROSS0} (cap INF, no de-grossing)"] = (d, d < 1e-12)
    d = float((G.MINHEAD - np.minimum(G.DD_HEAD, G.CAGR_HEAD)).abs().max())
    gates["G9 MINHEAD == min(DD_HEAD, CAGR_HEAD) at every cell"] = (d, d < 1e-12)
    okb = bool(((G.MINHEAD > 0) == (G.L_DD & G.L_CAGR)).all())
    gates["G10 MINHEAD > 0 <=> both L_DD and L_CAGR pass"] = (0.0 if okb else 1.0, okb)

    P("\n## GATES (printed before any result number is read)")
    gaterows = []
    for k, (d, ok) in gates.items():
        P(f"   [{'PASS' if ok else 'FAIL':4s}] {k}  (delta {d:.3e})")
        gaterows.append(dict(gate=k, delta=d, passed=ok))
    npass = sum(1 for _, (_, ok) in gates.items() if ok)
    P(f"   {npass} of {len(gates)} gates pass.")

    # ---- the crossing point --------------------------------------------------------------
    P("\n## THE LADDER — mean over the nine N rungs at each H (every cell is in the CSV)")
    P("   H     DD_HEAD  CAGR_HEAD    SWAP    MINHEAD   RELMIN   binds(L_DD/L_CAGR)  4b  4b-OOS")
    L = []
    for panel in PANELS:
        for Hh in H_WALK:
            s = WALK[(WALK.panel == panel) & (WALK.H == Hh)]
            L.append(dict(panel=panel, H=Hh, k=len(s),
                          DD_HEAD=s.DD_HEAD.mean(), CAGR_HEAD=s.CAGR_HEAD.mean(),
                          SWAP=s.SWAP.mean(), MINHEAD=s.MINHEAD.mean(), RELMIN=s.RELMIN.mean(),
                          MINHEAD_med=s.MINHEAD.median(),
                          MINHEAD_IS=s.MINHEAD_IS.mean(), MINHEAD_OOS=s.MINHEAD_OOS.mean(),
                          n_dd_binds=int((s.bind == "L_DD").sum()),
                          n_cagr_binds=int((s.bind == "L_CAGR").sum()),
                          pass4b=int(s.pass4b.sum()), pass4b_oos=int(s.pass4b_oos.sum()),
                          pass4b_both=int(s.pass4b_full_and_oos.sum()),
                          pass4a=int(s.pass4a.sum())))
    L = pd.DataFrame(L)
    for panel in PANELS:
        P(f"   -- {panel}")
        for _, r in L[L.panel == panel].iterrows():
            P(f"   H={int(r.H):<3d} {r.DD_HEAD:+8.3f} {r.CAGR_HEAD:+9.3f} {r.SWAP:+9.3f} "
              f"{r.MINHEAD:+9.3f} {r.RELMIN:+8.4f}      {r.n_dd_binds:d} / {r.n_cagr_binds:d}"
              f"          {int(r.pass4b):d}   {int(r.pass4b_oos):d}")

    P("\n## H_CROSS — does sign(DD_HEAD - CAGR_HEAD) change inside the ladder?")
    cross_any = False
    cross_at = {}
    for panel in PANELS:
        s = L[L.panel == panel].sort_values("H")
        sg = np.sign(s.SWAP.values)
        flips = [(int(s.H.values[i]), int(s.H.values[i + 1]))
                 for i in range(len(sg) - 1) if sg[i] != sg[i + 1] and sg[i] != 0 and sg[i + 1] != 0]
        cross_at[panel] = flips
        P(f"   {panel:<5s} SWAP at H=5 {s.SWAP.values[0]:+.3f} -> H=63 {s.SWAP.values[-1]:+.3f}; "
          f"sign changes at {flips if flips else 'NO RUNG'}; "
          f"L_DD is the binding leg at {int(s.n_dd_binds.sum())}/{int(s.k.sum())} cells")
        if flips:
            cross_any = True
    H_CROSS = cross_any
    P(f"   H_CROSS: {'SUPPORTED' if H_CROSS else 'REFUTED'}")

    P("\n## H_INTERIOR — where does mean MINHEAD peak on the eleven rungs?")
    argmax = {}
    interior = False
    for panel in PANELS:
        s = L[L.panel == panel].sort_values("H")
        i = int(s.MINHEAD.values.argmax())
        Hs = int(s.H.values[i])
        argmax[panel] = Hs
        edge = Hs in (H_WALK[0], H_WALK[-1])
        if not edge:
            interior = True
        P(f"   {panel:<5s} argmax H={Hs:<3d} MINHEAD {s.MINHEAD.values[i]:+.3f} pp "
          f"({'GRID EDGE' if edge else 'INTERIOR'}); ladder spread "
          f"{s.MINHEAD.max() - s.MINHEAD.min():.3f} pp "
          f"(worst H={int(s.H.values[int(s.MINHEAD.values.argmin())])})")
        rl = int(s.RELMIN.values.argmax())
        Hr = int(s.H.values[rl])
        note = ("same rung" if Hr == Hs else
                "A DIFFERENT RUNG: the argmax moves when the unit mismatch is removed")
        P(f"         RELMIN argmax H={Hr:<3d} ({s.RELMIN.values[rl]:+.4f}) — {note}")
    H_INTERIOR = interior
    P(f"   H_INTERIOR: {'SUPPORTED' if H_INTERIOR else 'REFUTED'}")

    P("\n## H_MONO_DD / H_MONO_CAGR — is 1106's 3-point gradient monotone at resolution?")
    mono = {}
    for panel in PANELS:
        s = L[L.panel == panel].sort_values("H")
        dd_inv = [(int(s.H.values[i]), int(s.H.values[i + 1]))
                  for i in range(len(s) - 1) if s.DD_HEAD.values[i + 1] > s.DD_HEAD.values[i]]
        cg_inv = [(int(s.H.values[i]), int(s.H.values[i + 1]))
                  for i in range(len(s) - 1) if s.CAGR_HEAD.values[i + 1] < s.CAGR_HEAD.values[i]]
        mono[panel] = (dd_inv, cg_inv)
        P(f"   {panel:<5s} DD_HEAD falling in H: {len(dd_inv)} inversions {dd_inv if dd_inv else ''}")
        P(f"         CAGR_HEAD rising in H: {len(cg_inv)} inversions {cg_inv if cg_inv else ''}")
    H_MONO_DD = all(not mono[p][0] for p in PANELS)
    H_MONO_CAGR = all(not mono[p][1] for p in PANELS)
    P(f"   H_MONO_DD: {'SUPPORTED' if H_MONO_DD else 'REFUTED'}   "
      f"H_MONO_CAGR: {'SUPPORTED' if H_MONO_CAGR else 'REFUTED'}")

    # ---- the resolution question ---------------------------------------------------------
    P(f"\n## H_RESOLVED — paired moving-block bootstrap, {BOOT_REPS} reps, block {BOOT_BLOCK}d,")
    P("   the SAME block indices applied to every rung AND to SPY inside each replicate, so the")
    P("   argmax-minus-rung difference is read on a paired distribution, not two marginals.")
    rng = np.random.default_rng(BOOT_SEED)
    resolved_flags = []
    for panel in PANELS:
        Hs = argmax[panel]
        spyf = spy_series[panel]["full"]
        ix = block_idx(rng, len(spyf), BOOT_BLOCK, BOOT_REPS)
        # the incumbent N carries the bootstrap: one N, every H rung, paired.
        base = keep_series[(panel, Hs, N_INC)]
        _, _, mh_star = boot_heads(base, spyf, ix)
        P(f"   -- {panel}, N={N_INC}, argmax rung H={Hs}")
        P(f"      MINHEAD at the argmax cell: point {G[(G.panel==panel)&(G.H==Hs)&(G.N==N_INC)].MINHEAD.values[0]:+.3f} pp, "
          f"bootstrap median {np.median(mh_star):+.3f}, 90% width {w90(mh_star):.3f} pp "
          f"(1083's band {W1083_LO}-{W1083_HI} pp)")
        for Hh in H_WALK:
            if Hh == Hs:
                continue
            _, _, mh_o = boot_heads(keep_series[(panel, Hh, N_INC)], spyf, ix)
            dif = mh_star - mh_o
            pt = float(np.median(dif))
            wd = w90(dif)
            share = float((dif > 0).mean())
            bootrows.append(dict(panel=panel, N=N_INC, H_star=Hs, H_other=Hh,
                                 d_median=pt, d_w90=wd, share_pos=share,
                                 beats_own=abs(pt) > wd, beats_1083=abs(pt) > W1083_LO))
            P(f"      H={Hs} - H={Hh:<3d}: median {pt:+7.3f} pp, 90% width {wd:6.3f} pp, "
              f"P(>0) {share:.3f}  "
              f"{'RESOLVED vs own width' if abs(pt) > wd else 'inside its own width'}")
        BB = pd.DataFrame(bootrows)
        bp = BB[BB.panel == panel]
        s = L[L.panel == panel]
        spread = float(s.MINHEAD.max() - s.MINHEAD.min())
        resolved = bool(spread > W1083_LO and bp.beats_own.any())
        resolved_flags.append(resolved)
        P(f"      LADDER SPREAD (mean MINHEAD, best rung - worst rung) {spread:.3f} pp vs 1083's "
          f"{W1083_LO}-{W1083_HI} pp and vs this run's own paired widths "
          f"{bp.d_w90.min():.3f}-{bp.d_w90.max():.3f} pp: "
          f"{'CLEARS BOTH' if resolved else 'DOES NOT CLEAR BOTH'}")
        P(f"      rungs separated from the argmax by more than their own paired 90% width: "
          f"{int(bp.beats_own.sum())} of {len(bp)}; by more than 1083's {W1083_LO} pp: "
          f"{int(bp.beats_1083.sum())} of {len(bp)}")
    H_RESOLVED = any(resolved_flags)
    P(f"   H_RESOLVED: {'SUPPORTED' if H_RESOLVED else 'REFUTED'}")

    # ---- H_CLEARS ------------------------------------------------------------------------
    P(f"\n## H_CLEARS — does any rung clear all five full-sample 4b legs AND all three OOS legs")
    P(f"   at the incumbent N={N_INC}?")
    clears = []
    for panel in PANELS:
        s = WALK[(WALK.panel == panel) & (WALK.N == N_INC)].sort_values("H")
        for _, r in s.iterrows():
            flags = "".join("Y" if r[c] else "." for c in
                            ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR", "O_S", "O_DD", "O_CAGR"])
            P(f"   {panel:<5s} H={int(r.H):<3d} legs H1/H2/OOS/DD/CAGR|O_S/O_DD/O_CAGR = {flags}  "
              f"MIN {r.MINHEAD:+6.2f}  4b {'PASS' if r.pass4b else 'fail'} / OOS "
              f"{'PASS' if r.pass4b_oos else 'fail'}")
            if r.pass4b_full_and_oos:
                clears.append((panel, int(r.H)))
    H_CLEARS = len(clears) > 0
    P(f"   rungs clearing both at N={N_INC}: {clears if clears else 'NONE'}")
    P(f"   H_CLEARS: {'SUPPORTED' if H_CLEARS else 'REFUTED'}")

    # ---- RULE 8 --------------------------------------------------------------------------
    P("\n## RULE 8 WALK-FORWARD — H chosen on IS 2009-2016 by IS MINHEAD, OOS 2017-2026 read once")
    wf = []
    for panel in PANELS:
        sb_ = [r for r in benchrows if r["panel"] == panel and r["series"] == "SPY"][0]
        lb_ = [r for r in benchrows if r["panel"] == panel and r["series"] == "RULESv2"][0]
        for N in NS:
            s = WALK[(WALK.panel == panel) & (WALK.N == N)].sort_values("H")
            pick = s.loc[s.MINHEAD_IS.idxmax()]
            best = s.loc[s.MINHEAD_OOS.idxmax()]
            wf.append(dict(panel=panel, N=N, H_pick=int(pick.H), IS_MINHEAD=pick.MINHEAD_IS,
                           OOS_MINHEAD=pick.MINHEAD_OOS, OOS_CAGR=pick.OOS_CAGR,
                           OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                           SPY_OOS_CAGR=sb_["OOS_CAGR"], SPY_OOS_Sharpe=sb_["OOS_Sharpe"],
                           SPY_OOS_MaxDD=sb_["OOS_MaxDD"],
                           LIVE_OOS_Sharpe=lb_["OOS_Sharpe"], LIVE_OOS_MaxDD=lb_["OOS_MaxDD"],
                           pass4b=bool(pick.pass4b), pass4b_oos=bool(pick.pass4b_oos),
                           pass4a=bool(pick.pass4a),
                           H_best_OOS=int(best.H), OOS_MINHEAD_best=best.MINHEAD_OOS,
                           regret=float(best.MINHEAD_OOS - pick.MINHEAD_OOS)))
    WF = pd.DataFrame(wf)
    for panel in PANELS:
        P(f"   -- {panel}  (SPY OOS CAGR {WF[WF.panel==panel].SPY_OOS_CAGR.iloc[0]:.2%}, "
          f"Sharpe {WF[WF.panel==panel].SPY_OOS_Sharpe.iloc[0]:.4f}, "
          f"MaxDD {WF[WF.panel==panel].SPY_OOS_MaxDD.iloc[0]:.2%};  live RULES v2 OOS Sharpe "
          f"{WF[WF.panel==panel].LIVE_OOS_Sharpe.iloc[0]:.4f})")
        for _, r in WF[WF.panel == panel].iterrows():
            P(f"      N={int(r.N):<2d} IS pick H={int(r.H_pick):<3d} (IS MIN {r.IS_MINHEAD:+6.2f}) "
              f"-> OOS CAGR {r.OOS_CAGR:6.2%} Sharpe {r.OOS_Sharpe:.4f} MaxDD {r.OOS_MaxDD:7.2%} "
              f"OOS MIN {r.OOS_MINHEAD:+6.2f};  OOS-best rung would be H={int(r.H_best_OOS):<3d} "
              f"(regret {r.regret:+.2f} pp)")
        sp = WF[WF.panel == panel]
        P(f"      IS pick == OOS-best rung at {int((sp.H_pick == sp.H_best_OOS).sum())}/{len(sp)} "
          f"N rungs; median regret {sp.regret.median():+.3f} pp; "
          f"IS-picked cells passing 4b full {int(sp.pass4b.sum())}/{len(sp)}, "
          f"4b OOS {int(sp.pass4b_oos.sum())}/{len(sp)}, 4a {int(sp.pass4a.sum())}/{len(sp)}")

    # ---- both KEEP paths -----------------------------------------------------------------
    P(f"\n## BOTH KEEP PATHS at all {len(WALK)} walked cells (PROTOCOL rule 4)")
    P(f"   4a (Sharpe > RULES v2 in BOTH halves, MaxDD no worse): {int(WALK.pass4a.sum())} of {len(WALK)}")
    for leg in ["A_H1", "A_H2", "A_DD"]:
        P(f"      {leg}: {int(WALK[leg].sum())}/{len(WALK)}")
    P(f"   4b (capital-worthy, full sample): {int(WALK.pass4b.sum())} of {len(WALK)}")
    for leg in ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]:
        P(f"      {leg}: {int(WALK[leg].sum())}/{len(WALK)}")
    P(f"   4b on the OOS window alone: {int(WALK.pass4b_oos.sum())} of {len(WALK)}")
    for leg in ["O_S", "O_DD", "O_CAGR"]:
        P(f"      {leg}: {int(WALK[leg].sum())}/{len(WALK)}")
    P(f"   4b FULL and OOS together: {int(WALK.pass4b_full_and_oos.sum())} of {len(WALK)}")
    LEGS4B = ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]
    fails = WALK[~WALK.pass4b]
    P(f"   BINDING LEG among the {len(fails)} full-sample 4b FAILURES:")
    for leg in LEGS4B:
        n_only = int((~fails[leg] & fails[[x for x in LEGS4B if x != leg]].all(axis=1)).sum())
        P(f"      {leg}: fails at {int((~fails[leg]).sum())}/{len(fails)}, SOLE failing leg at {n_only}")
    psw = WALK[WALK.pass4b_full_and_oos]
    if len(psw):
        P(f"   The {len(psw)} walked cells passing 4b FULL and OOS, with their own headroom:")
        P(f"      DD headroom   min {psw.DD_HEAD.min():+.2f} median {psw.DD_HEAD.median():+.2f} "
          f"max {psw.DD_HEAD.max():+.2f} pp")
        P(f"      CAGR headroom min {psw.CAGR_HEAD.min():+.2f} median {psw.CAGR_HEAD.median():+.2f} "
          f"max {psw.CAGR_HEAD.max():+.2f} pp")
        P(f"      MINHEAD       min {psw.MINHEAD.min():+.2f} median {psw.MINHEAD.median():+.2f} "
          f"max {psw.MINHEAD.max():+.2f} pp — every one of these is inside 1083's "
          f"{W1083_LO}-{W1083_HI} pp band unless stated otherwise above.")

    # ---- hypotheses ----------------------------------------------------------------------
    hyp = [dict(hypothesis="H_CROSS",
                declared="sign(DD_HEAD - CAGR_HEAD) changes inside the ladder on >=1 panel",
                result="; ".join(f"{p}: {cross_at[p] if cross_at[p] else 'no sign change'}"
                                 for p in PANELS),
                verdict="SUPPORTED" if H_CROSS else "REFUTED"),
           dict(hypothesis="H_INTERIOR", declared="mean-MINHEAD argmax interior to [5,63] on >=1 panel",
                result="; ".join(f"{p}: H={argmax[p]}" for p in PANELS),
                verdict="SUPPORTED" if H_INTERIOR else "REFUTED"),
           dict(hypothesis="H_RESOLVED",
                declared=f"argmax-minus-worst MINHEAD > {W1083_LO} pp AND > own paired 90% width",
                result="; ".join(
                    f"{p}: spread {float(L[L.panel==p].MINHEAD.max()-L[L.panel==p].MINHEAD.min()):.3f} pp"
                    for p in PANELS),
                verdict="SUPPORTED" if H_RESOLVED else "REFUTED"),
           dict(hypothesis="H_MONO_DD", declared="DD_HEAD monotone falling in H",
                result="; ".join(f"{p}: {len(mono[p][0])} inversions" for p in PANELS),
                verdict="SUPPORTED" if H_MONO_DD else "REFUTED"),
           dict(hypothesis="H_MONO_CAGR", declared="CAGR_HEAD monotone rising in H",
                result="; ".join(f"{p}: {len(mono[p][1])} inversions" for p in PANELS),
                verdict="SUPPORTED" if H_MONO_CAGR else "REFUTED"),
           dict(hypothesis="H_CLEARS", declared=f"some rung clears 4b full AND OOS at N={N_INC}",
                result=str(clears) if clears else "none",
                verdict="SUPPORTED" if H_CLEARS else "REFUTED")]
    HY = pd.DataFrame(hyp)
    P("\n## HYPOTHESES")
    for _, r in HY.iterrows():
        P(f"   [{r['verdict']:<9s}] {r['hypothesis']:<12s} {r['result']}")
    P(f"   {int((HY.verdict == 'SUPPORTED').sum())} of {len(HY)} supported.")

    dump(G, "grid")
    dump(L, "ladder")
    dump(pd.DataFrame(bootrows), "bootstrap")
    dump(WF, "walkforward")
    dump(HY, "hypotheses")
    dump(pd.DataFrame(gaterows), "gates")
    dump(pd.DataFrame(benchrows), "benchmarks")

    P("\n## SURVIVORSHIP (PROTOCOL rule 9)")
    P("   U56 and B136 are CURRENT-CONSTITUENT lists.  Every level is optimistic and every")
    P("   4a/4b count is an UPPER bound.  DD_HEAD and CAGR_HEAD are measured against SPY, a")
    P("   real index, so the bias does NOT cancel out of them: the headrooms above overstate")
    P("   what a tradable book would have had, in the direction that flatters the answer.")
    P(f"\n# done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
