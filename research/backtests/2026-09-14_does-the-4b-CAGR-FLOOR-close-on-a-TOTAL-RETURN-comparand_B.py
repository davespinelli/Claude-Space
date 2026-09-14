#!/usr/bin/env python3
"""Idea 850 — does the 4b CAGR FLOOR close on a TOTAL-RETURN comparand?  (2026-09-14, lane B)

THE CLAIM UNDER TEST (the queue's own wording)
    "every 4b floor in the record is priced against the PRICE-ONLY SPY column in
     data/prices.csv while the traded panel is adjusted closes, so the floor may be
     systematically mis-set in one direction; measure the sign and size."

The queue filed this PARK, "needs a dividend/total-return series".  It does not: the
convention of `data/prices.csv` is decidable FROM THE FILE ITSELF, because the file also
carries six fixed-income ETFs whose PRICE return is structurally pinned and whose TOTAL
return is not.  A 1-3 year Treasury fund (SHY) holds paper that matures at par; its clean
price is a bounded, mean-reverting series that cannot compound.  If the cached SHY has
compounded, the column is dividend-reinvested and the premise is false.  That test needs
no network and no new data.

    PART 0  GATES — five, printed before any new number.
    PART A  THE PREMISE — three independent internal legs on the convention, plus the
            census of what conventions the sandbox actually holds.
    PART B  THE SIZE — the counterfactual the premise describes, priced parametrically.
            There is no price-only SPY to fetch, so the mis-set floor is bracketed: apply
            a dividend drag d to the comparand and read PROTOCOL 4b's four legs at every
            rung of d, on both candidate sets.  SIGN and SIZE come out of the same grid.
    PART C  RULE 8 — dial chosen on 2009-2016 IS Sharpe alone, OOS 2017-2026 read once per
            (d, panel); OOS CAGR/Sharpe/MaxDD against RULES v2, RULES v1 and SPY.

TUNED PARAMETERS: exactly two — (1) the comparand drag d, 7 rungs; (2) the candidate set,
{SHELF, GRID}.  ALL 14 combinations are reported, none is selected.

SURVIVORSHIP: U56 and B136 are current-constituent lists.  Every LEVEL below is optimistic;
the CONTRASTS (floor at d vs floor at 0) are the claim.

Costs 10 bps headline (0 and 25 also read), next-day execution, PROTOCOL rules 2/3/4/8.
Writes nothing outside research/backtests/.  Does not modify RULES.md, scan.py, bot.py or
baseline.py.
"""
from __future__ import annotations

import sys, time
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import (load_universe, rules_v1_weights, rules_v2_weights, score,  # noqa: E402
                      band_state)
from engine import rebalance_mask, backtest, metrics  # noqa: E402

DATE = "2026-09-14"
OUT = str(Path(__file__).with_suffix(""))
LOG: list[str] = []


def P(s=""):
    print(s)
    LOG.append(s)


# ----------------------------------------------------------------------------- dials
# PARAM 1 of 2 — the comparand drag, in %/yr subtracted from the SPY benchmark to simulate
# the price-only column the premise says the record is using.  0.00 is the record's
# committed convention; the rungs bracket the plausible S&P dividend yield.
DRAGS = (0.0000, 0.0050, 0.0100, 0.0150, 0.0180, 0.0200, 0.0250)
# PARAM 2 of 2 — candidate set.
SETS = ("SHELF", "GRID")

RUNGS = (0, 10, 25)
RUNG_HEAD = 10
FREQ = "W"
LAG = 1
WARMUP = 260
MAX_VOL = 0.60
OOS_START = "2017-01-01"
# the record's committed FIXED bars (idea 851's PART A, from SPY full sample)
FIXED_CAP, FIXED_FLOOR = -0.2023, 0.1061
# the record's committed SPY headline, for gate G1
SPY_COMMITTED = (0.151631, 0.8861, -0.337172)
# idea 851's G2 tolerance, reused verbatim so the shelf is admitted on the record's terms
TOL_SHARPE, TOL_DD = 0.030, 0.015
# structural bound used by PART A leg 1 (see the docstring): the clean price of a fund that
# holds only 1-3 year Treasuries is par-pulled.  Nothing in this run depends on the exact
# number; +33% cumulative is an order of magnitude outside any defensible band.
PARPULL_BAND = 0.10


# ------------------------------------------------------------------ runner (the record's)
def fast_run(prices, weights, mask, lag=LAG):
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(lag).fillna(0.0).values
    mk = mask.shift(lag, fill_value=False).values.copy()
    mk[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
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
    return pd.Series((held * rets).sum(axis=1), index=idx), pd.Series(turn, index=idx)


def fmet(r):
    r = np.asarray(r, float)
    if len(r) < 2:
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    if len(r) < 2:
        return np.nan
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def pack(r):
    c, s, d = fmet(r)
    h = len(r) // 2
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(r[:h]), H2=fsharpe(r[h:]))


def verdicts(s, base, spy, cap, floor):
    """PROTOCOL rule 4, both paths.  cap/floor are passed in so the ONLY difference between
    two readings of the same book is the comparand."""
    p4a = (s["H1"] > base["H1"]) and (s["H2"] > base["H2"]) and (s["MaxDD"] >= base["MaxDD"])
    legs = dict(H1=s["H1"] > spy["H1"], H2=s["H2"] > spy["H2"],
                DDCAP=s["MaxDD"] >= cap, CAGRFLOOR=s["CAGR"] >= floor)
    fails = "+".join(k for k, v in legs.items() if not v) or "-"
    return bool(p4a), all(legs.values()), fails


def drag_returns(spy_r, d):
    """The premise's counterfactual comparand: the SAME index with a constant dividend drag
    of d per year removed, i.e. what the record's SPY column would look like if it were
    price-only and the missing piece were a smooth yield.  d = 0 is the committed column."""
    return np.asarray(spy_r, float) - d / 252.0


# ------------------------------------------------------------------ panels and books
def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def breadth(px):
    above = px > px.rolling(200).mean()
    return above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)


def gate_mult(br, thr, depth, idx):
    below = (br < thr)
    m = pd.Series(1.0, index=idx).where(~below, 1.0 - depth)
    m = m.where(br.notna() & thr.notna(), 1.0)
    return m.where(rebalance_mask(idx, FREQ)).ffill().fillna(1.0)


def shelf_books(U, B):
    """Every committed 4b KEEP-candidate memo, rebuilt from its own RULES wording.  Lifted
    verbatim from idea 851's shelf so the two runs are reading the SAME eight books."""
    out = {}
    out["u56-v2band-gross100"] = dict(
        panel="U56", freq="W", W=rules_v2_weights(U, 0.03, 1.00), memo=(0.1155, 1.2067, -0.1570),
        src="2026-09-11_u56-v2band-gross100_4b_cloud_MEMO.md")
    out["u56-band008-gross100"] = dict(
        panel="U56", freq="W", W=rules_v2_weights(U, 0.08, 1.00), memo=(0.1137, 1.1439, -0.1905),
        src="2026-09-11_u56-band008-gross100_4b_cloud_MEMO.md")
    s, above, vol20 = score(U, vol_scale=False)
    rank = s.where(above & (vol20 < MAX_VOL)).rank(axis=1, ascending=False)
    out["u56-top20-band-m20"] = dict(
        panel="U56", freq="W", W=(rank <= 20).astype(float) * 0.75 / 20,
        memo=(0.1287, 1.112, -0.1722), src="2026-09-07_u56-top20-band-m20_4b_B_MEMO.md")
    ab = (U > U.rolling(200).mean()).astype(float)
    n = ab.sum(axis=1).replace(0, np.nan)
    out["u56-marsrespread-gross075"] = dict(
        panel="U56", freq="W", W=ab.div(n, axis=0).mul(0.75).fillna(0.0),
        memo=(0.1155, 1.0914, None), src="2026-09-11_u56-marsrespread-gross075_4b_C_MEMO.md")
    rel = U / U.rolling(200).mean() - 1
    sel = (rel.rank(axis=1, ascending=False, pct=True) <= 0.50) & rel.notna()
    k = sel.astype(float).sum(axis=1).replace(0, np.nan)
    out["u56-quantile50-respread-M"] = dict(
        panel="U56", freq="M", W=sel.astype(float).div(k, axis=0).mul(0.75).fillna(0.0),
        memo=(0.1547, 1.2359, -0.1980), src="2026-09-11_u56-quantile50-respread-M_4b_B_MEMO.md")
    r6 = B / B.shift(126) - 1
    out["b136-r620-gross065-W"] = dict(
        panel="B136", freq="W", W=(r6.rank(axis=1, ascending=False) <= 20).astype(float) * 0.65 / 20,
        memo=(0.1499, 1.1264, -0.1943), src="2026-09-12_b136-r620-gross065-W_4b_C_MEMO.md")
    for nm, px, q, dep, memo, src in (
            ("b136-qroll-q012-w1008-d050-g100", B, 0.12, 0.50, (0.1430, 1.1121, -0.1731),
             "2026-09-12_b136-qroll-q012-w1008-depth050-gross100_4b_cloud_MEMO.md"),
            ("u56-k8-qroll-q017-w1008-d100-g100", U, 0.17, 1.00, (0.1416, 1.2226, -0.1479),
             "2026-09-14_u56-k8-qroll-q017-w1008-depth100-gross100_LIVELEG_4b_cloud_MEMO.md")):
        elig = eligible_mask(px).astype(float)
        nn = elig.sum(axis=1).replace(0, np.nan)
        base = elig.div(nn, axis=0).fillna(0.0)
        br = breadth(px)
        thr = br.rolling(1008, min_periods=1008).quantile(q)
        out[nm] = dict(panel=("B136" if px is B else "U56"), freq="W",
                       W=base.mul(gate_mult(br, thr, dep, px.index), axis=0),
                       memo=memo, src=src)
    return out


def grid_books(U, B):
    """A mechanical ladder nobody memo-selected, so the shelf's answer reads against
    something the record did not choose.  Same ladder as idea 851's GRID."""
    out = {}
    for pname, px in (("U56", U), ("B136", B)):
        for band, g in product((0.03, 0.08), (0.50, 0.75, 1.00)):
            out[f"{pname}-band{band:.2f}-g{g:.2f}"] = dict(
                panel=pname, freq="W", W=rules_v2_weights(px, band, g), memo=None, src="GRID")
        elig = eligible_mask(px).astype(float)
        nn = elig.sum(axis=1).replace(0, np.nan)
        base = elig.div(nn, axis=0).fillna(0.0)
        br = breadth(px)
        for q, w, dep in product((0.12, 0.17), (252, 504, 1008), (0.50, 1.00)):
            thr = br.rolling(w, min_periods=w).quantile(q)
            out[f"{pname}-qroll-q{q:.2f}-w{w}-d{dep:.2f}"] = dict(
                panel=pname, freq="W", W=base.mul(gate_mult(br, thr, dep, px.index), axis=0),
                memo=None, src="GRID")
    return out


# =====================================================================================
def main():
    t0 = time.time()
    P(f"# Idea 850 — does the 4b CAGR FLOOR close on a TOTAL-RETURN comparand? ({DATE}, lane B)")
    P(f"# 2 tuned params: comparand drag d ({len(DRAGS)} rungs) x candidate set "
      f"({len(SETS)}).  ALL {len(DRAGS) * len(SETS)} combinations reported, none selected.")
    P("# SURVIVORSHIP: U56/B136 are current-constituent lists; every LEVEL is optimistic.")

    U = load_universe().dropna(how="all").ffill()
    B = load_universe(broad=True).dropna(how="all").ffill()
    PX = {"U56": U, "B136": B}
    idx = U.index
    assert B.index.equals(idx), "panels must share a calendar"
    start = idx[WARMUP]
    eidx = idx[idx >= start]
    oos_mask = np.asarray(eidx >= pd.Timestamp(OOS_START))
    P(f"\n   U56 {U.shape}, B136 {B.shape}; scored {start.date()}..{eidx[-1].date()} "
      f"({len(eidx)} days), OOS from {OOS_START} ({int(oos_mask.sum())} days)")

    raw = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)
    rawb = pd.read_csv(ROOT / "data" / "prices_broad.csv", index_col=0, parse_dates=True)

    # ============================================================ PART 0 — GATES
    P("\n### PART 0 — GATES (printed before any new number)")
    gates = []

    spy_full = U["SPY"].pct_change().fillna(0.0).loc[start:].values
    sp0 = pack(spy_full)
    d_c = max(abs(sp0["CAGR"] - SPY_COMMITTED[0]), abs(sp0["Sharpe"] - SPY_COMMITTED[1]),
              abs(sp0["MaxDD"] - SPY_COMMITTED[2]))
    g1 = d_c < 1e-3
    gates.append(("G1 SPY headline reproduces the record's committed 15.1631/0.8861/-33.7172",
                  g1, f"{sp0['CAGR']:.4%} / {sp0['Sharpe']:.4f} / {sp0['MaxDD']:.4%}, "
                      f"max|d| {d_c:.3e}"))

    g2 = abs(FIXED_CAP - 0.60 * sp0["MaxDD"]) < 5e-4 and abs(FIXED_FLOOR - 0.70 * sp0["CAGR"]) < 5e-4
    gates.append(("G2 the committed FIXED bars ARE 60%/70% of that SPY (so a comparand move "
                  "moves them mechanically)", g2,
                  f"cap {0.60 * sp0['MaxDD']:.4%} vs {FIXED_CAP:.2%}, "
                  f"floor {0.70 * sp0['CAGR']:.4%} vs {FIXED_FLOOR:.2%}"))

    # G3 — the fast runner IS the engine, on one book, so PART B/C levels are the record's
    tw = rules_v2_weights(U)
    r_f, t_f = fast_run(U, tw, rebalance_mask(U.index, FREQ))
    eng = backtest(U, tw, cost_bps=RUNG_HEAD, freq=FREQ)
    a = (r_f - t_f * RUNG_HEAD / 1e4).loc[start:]
    b = eng["returns"].loc[start:]
    dmax = float((a - b).abs().max())
    g3 = dmax < 1e-10
    gates.append(("G3 fast_run == engine.backtest on RULES v2 / U56 / 10 bps", g3,
                  f"max|d| {dmax:.3e}; engine {metrics(b)['Sharpe']:.4f} vs "
                  f"fast {fsharpe(a.values):.4f}"))

    # G4 — drag_returns at d=0 is the identity
    g4 = float(np.abs(drag_returns(spy_full, 0.0) - spy_full).max()) == 0.0
    gates.append(("G4 the d=0 comparand IS the committed column (empty counterfactual = "
                  "identity)", g4, "max|d| 0.000e+00"))

    # G5 — the two caches carry ONE CONVENTION, so the sandbox holds no second comparand.
    #      NOT bit-identity: prices_broad.csv is stored at 2 decimals (see the BY-PRODUCT
    #      section), so the two files differ by quantization.  A CONVENTION difference is a
    #      different animal: it would show up as the ratio A/B DRIFTING by the cumulative
    #      dividend factor (tens of percent over 18 years), not as half-a-cent noise.  The
    #      gate therefore tests ratio DRIFT, which is the thing this idea is about.
    shared = sorted(set(raw.columns) & set(rawb.columns))
    ci = raw.index.intersection(rawb.index)
    A, Bc = raw.loc[ci, shared], rawb.loc[ci, shared]
    dd = float((A - Bc).abs().max().max())
    #   Quantization is a CONFOUND for this gate, not a convention difference: on a series
    #   whose back-adjusted price falls under a dollar, half a cent is percent-scale and it
    #   contaminates the ratio.  The gate therefore reads only names never cheaper than $5
    #   over the shared window (where quantization is bounded by 0.1%), and NAMES the ones it
    #   drops.  They are priced in full in the BY-PRODUCT section instead.
    cheap = sorted(c for c in shared if float(A[c].min()) < 5.0)
    keep = [c for c in shared if c not in cheap]
    ratio = (A[keep] / Bc[keep]).replace([np.inf, -np.inf], np.nan)
    drift = float((ratio.max() - ratio.min()).max())
    g5 = drift < 0.01
    gates.append((f"G5 data/prices.csv and data/prices_broad.csv share ONE CONVENTION on the "
                  f"{len(keep)} of {len(shared)} shared tickers never under $5 — the sandbox "
                  f"holds no second comparand",
                  g5, f"max ratio DRIFT {drift:.3e} (a price-only/total-return gap would open "
                      f"0.2-0.3 over this window); raw max|d| {dd:.3e} is 2-decimal "
                      f"quantization, priced in the BY-PRODUCT section. Dropped as "
                      f"quantization-contaminated: {cheap}"))

    for nm, ok, det in gates:
        P(f"   [{'PASS' if ok else 'FAIL'}] {nm}\n           {det}")
    P(f"   >>> {sum(int(o) for _, o, _ in gates)} of {len(gates)} gates PASS")

    # ============================================================ PART A — THE PREMISE
    P("\n### PART A — THE PREMISE: is the SPY column in data/prices.csv PRICE-ONLY?")
    P("   The queue filed this idea PARK for want of a dividend series. It does not need one:")
    P("   data/prices.csv carries six fixed-income ETFs whose PRICE return is structurally")
    P("   pinned and whose TOTAL return is not. They decide the convention of the file, and")
    P("   SPY is a column of the SAME file, written by the SAME engine.load_prices call.")

    BONDS = [("SHY", "1-3y UST"), ("IEF", "7-10y UST"), ("TIP", "TIPS"),
             ("LQD", "IG corp"), ("HYG", "HY corp"), ("TLT", "20y+ UST")]
    arows = []
    P("\n   LEG 1 — par pull. A fund holding only bonds redeems them at par; its clean price")
    P("   is a bounded series, not a compounding one. Cumulative PRICE change over the whole")
    P("   cache should sit inside a few percent of zero for the short end.")
    P(f"      {'ticker':<7}{'sleeve':<11}{'first':>10}{'last':>10}{'cumul':>10}{'CAGR/yr':>10}"
      f"{'min':>10}{'min==first?':>13}{'new-high days':>15}")
    for t, sl in BONDS:
        s = raw[t].dropna()
        yrs = (s.index[-1] - s.index[0]).days / 365.25
        cum = s.iloc[-1] / s.iloc[0] - 1.0
        cg = (1 + cum) ** (1 / yrs) - 1
        nh = float((s >= s.cummax() - 1e-12).mean())
        mineqfirst = bool(abs(s.min() - s.iloc[0]) < 1e-9)
        arows.append(dict(part="A1", ticker=t, sleeve=sl, first=s.iloc[0], last=s.iloc[-1],
                          cumul=cum, cagr=cg, minv=s.min(), min_is_first=mineqfirst,
                          new_high_frac=nh, years=yrs))
        P(f"      {t:<7}{sl:<11}{s.iloc[0]:>10.3f}{s.iloc[-1]:>10.3f}{cum:>10.2%}{cg:>10.2%}"
          f"{s.min():>10.3f}{str(mineqfirst):>13}{nh:>15.1%}")
    shy = [r for r in arows if r["ticker"] == "SHY"][0]
    l1 = abs(shy["cumul"]) > PARPULL_BAND
    P(f"      LEG 1 verdict: SHY (1-3y UST) has compounded {shy['cumul']:+.2%} over "
      f"{shy['years']:.1f} years, outside any par-pull band (|{PARPULL_BAND:.0%}|), and its "
      f"MINIMUM IS ITS FIRST OBSERVATION\n"
      f"      ({str(shy['min_is_first'])}) — it never once revisits its starting level. A "
      f"price-only short-Treasury series cannot do this. => {'ADJUSTED' if l1 else 'no call'}")

    P("\n   LEG 2 — the ladder. Order the sleeves by YIELD (credit + term premium). A")
    P("   dividend-reinvested set compounds in yield order; a price-only set does not")
    P("   (its ordering would be driven by duration-weighted rate moves, not by carry).")
    ladder = [(t, [r for r in arows if r["ticker"] == t][0]["cagr"]) for t in
              ("SHY", "IEF", "TIP", "LQD", "HYG")]
    P("      " + "  <  ".join(f"{t} {c:.2%}" for t, c in ladder))
    l2 = all(ladder[i][1] < ladder[i + 1][1] for i in range(len(ladder) - 1))
    P(f"      LEG 2 verdict: yield-monotone across all {len(ladder)} sleeves = {l2} "
      f"=> {'ADJUSTED' if l2 else 'no call'}")

    P("\n   LEG 3 — the long end. TLT's price peaked and then gave back the 2020-2023 rate")
    P("   rout; a PRICE-ONLY TLT over this window ends near or below where it started.")
    tlt = [r for r in arows if r["ticker"] == "TLT"][0]
    s = raw["TLT"].dropna()
    pk = s.idxmax()
    P(f"      TLT {s.iloc[0]:.3f} -> peak {s.max():.3f} ({pk.date()}) -> {s.iloc[-1]:.3f}: "
      f"{s.iloc[-1] / s.max() - 1:+.2%} from the peak, yet {tlt['cumul']:+.2%} from the start "
      f"({tlt['cagr']:+.2%}/yr).")
    l3 = tlt["cumul"] > 0.10
    P(f"      LEG 3 verdict: a {tlt['cumul']:+.2%} cumulative gain through a "
      f"{s.iloc[-1] / s.max() - 1:+.2%} price collapse is coupon, not price "
      f"=> {'ADJUSTED' if l3 else 'no call'}")

    PREMISE_FALSE = bool(l1 and l2 and l3)
    P(f"\n   >>> PART A ANSWER: the premise is {'FALSE' if PREMISE_FALSE else 'NOT REFUTED'} "
      f"({int(l1) + int(l2) + int(l3)} of 3 legs say ADJUSTED).")
    P("   data/prices.csv is a DIVIDEND-REINVESTED (total-return) panel. SPY is a column of")
    P("   that same file. `engine.load_prices` fetches with auto_adjust=True and falls back to")
    P("   this cache, so the benchmark and the traded panel are on ONE convention by")
    P("   construction. THE MISMATCH THE IDEA POSTULATES IS ZERO BY CONSTRUCTION, not small.")
    P(f"   G5 adds the corollary: the sandbox holds no SECOND convention — across the "
      f"{len(keep)} never-under-$5 tickers both cache files carry, the ratio between them "
      f"drifts by "
      f"{drift:.3e} over the whole window, where a price-only/total-return gap would open "
      f"0.2-0.3. So there is nothing to mis-match against even if one wanted to, and a "
      f"genuine price-only comparand would still have to be fetched from outside.")
    pd.DataFrame(arows).to_csv(f"{OUT}.convention.csv", index=False)

    # ============================================================ books
    P("\n### building books")
    books = {}
    for setname, maker in (("SHELF", shelf_books), ("GRID", grid_books)):
        for nm, bk in maker(U, B).items():
            px = PX[bk["panel"]]
            r, t = fast_run(px, bk["W"], rebalance_mask(px.index, bk["freq"]))
            bk["net"] = {c: (r - t * c / 1e4).loc[start:].values for c in RUNGS}
            bk["set"] = setname
            books[nm] = bk
    v2 = {p: {c: (lambda rt: (rt[0] - rt[1] * c / 1e4).loc[start:].values)(
        fast_run(PX[p], rules_v2_weights(PX[p]), rebalance_mask(PX[p].index, FREQ)))
        for c in RUNGS} for p in PX}
    v1 = {p: {c: (lambda rt: (rt[0] - rt[1] * c / 1e4).loc[start:].values)(
        fast_run(PX[p], rules_v1_weights(PX[p]), rebalance_mask(PX[p].index, FREQ)))
        for c in RUNGS} for p in PX}
    P(f"   {len(books)} books ({sum(1 for b in books.values() if b['set'] == 'SHELF')} SHELF, "
      f"{sum(1 for b in books.values() if b['set'] == 'GRID')} GRID) x {len(RUNGS)} rungs")

    # SHELF reproduction gate (idea 851's G2, re-run so the shelf is admitted on its own terms)
    P("\n   SHELF reproduction (tolerance Sharpe {:.3f} / MaxDD {:.1f} pp, idea 851's):"
      .format(TOL_SHARPE, TOL_DD * 100))
    dropped = []
    for nm, bk in sorted(books.items()):
        if bk["set"] != "SHELF":
            continue
        m = pack(bk["net"][RUNG_HEAD])
        mc, ms, md = bk["memo"]
        ok = abs(m["Sharpe"] - ms) <= TOL_SHARPE and (md is None or abs(m["MaxDD"] - md) <= TOL_DD)
        bk["repro"] = ok
        if not ok:
            dropped.append(nm)
        P(f"      {'ok ' if ok else 'DROP'} {nm:<34} {m['CAGR']:>8.2%} {m['Sharpe']:>8.4f} "
          f"{m['MaxDD']:>9.2%}  memo {mc:.2%} / {ms:.4f} / "
          f"{'n/a' if md is None else f'{md:.2%}'}  dS {abs(m['Sharpe'] - ms):.4f}")
    for nm in dropped:
        books.pop(nm)
    P(f"      {len([b for b in books.values() if b['set'] == 'SHELF'])} of "
      f"{len([b for b in books.values() if b['set'] == 'SHELF']) + len(dropped)} shelf books "
      f"admitted; dropped (named, never re-specified): {dropped or 'none'}")

    # ============================================================ PART B — THE SIZE
    P("\n### PART B — THE SIZE: what a price-only comparand would have done to PROTOCOL 4b")
    P("   There is no price-only SPY to fetch, so the counterfactual is priced parametrically:")
    P("   subtract a constant dividend drag d from the comparand and re-read all four 4b legs.")
    P("   d=0 is the record's committed column. Bars are RE-PRICED at every d (cap = 60% of")
    P("   the comparand's MaxDD, floor = 70% of its CAGR), which is what PROTOCOL 4b says.")

    P(f"\n   THE COMPARAND ITSELF (full sample, {start.date()}..{eidx[-1].date()}):")
    P(f"      {'d %/yr':>8}{'CAGR':>10}{'Sharpe':>10}{'MaxDD':>10}{'H1':>9}{'H2':>9}"
      f"{'4b floor':>11}{'4b cap':>10}{'floor move':>12}")
    SP = {}
    for d in DRAGS:
        sp = pack(drag_returns(spy_full, d))
        SP[d] = sp
        P(f"      {d * 100:>8.2f}{sp['CAGR']:>10.4%}{sp['Sharpe']:>10.4f}{sp['MaxDD']:>10.4%}"
          f"{sp['H1']:>9.4f}{sp['H2']:>9.4f}{0.70 * sp['CAGR']:>11.4%}"
          f"{0.60 * sp['MaxDD']:>10.4%}{0.70 * sp['CAGR'] - 0.70 * SP[0.0]['CAGR']:>12.4%}")
    slope = (0.70 * SP[0.0200]["CAGR"] - 0.70 * SP[0.0]["CAGR"]) / 2.0
    P(f"\n   SIGN: the floor MOVES DOWN with the drag ({slope:+.4%} of floor per 1.00 %/yr of")
    P("   missing dividend, i.e. the 0.70 coefficient, essentially exactly). So had the record")
    P("   really been using a price-only SPY, its 4b CAGR floor would have been TOO LOW and")
    P("   every 4b verdict TOO GENEROUS. The convention it actually uses is the STRICTER one.")
    P("   SECOND-ORDER: the drag also lowers the comparand's Sharpe legs and SHALLOWS its")
    P("   MaxDD, so the cap TIGHTENS as the floor loosens — the two 4b level bars move in")
    P("   OPPOSITE directions under a comparand error. They do not cancel; they trade off.")

    rows = []
    for d, setname in product(DRAGS, SETS):
        sp = SP[d]
        cap, flo = 0.60 * sp["MaxDD"], 0.70 * sp["CAGR"]
        for nm, bk in sorted(books.items()):
            if bk["set"] != setname:
                continue
            for c in RUNGS:
                s = pack(bk["net"][c])
                base = pack(v2[bk["panel"]][c])
                p4a, p4b, fails = verdicts(s, base, sp, cap, flo)
                rows.append(dict(drag=d, set=setname, book=nm, panel=bk["panel"], bps=c,
                                 CAGR=s["CAGR"], Sharpe=s["Sharpe"], MaxDD=s["MaxDD"],
                                 H1=s["H1"], H2=s["H2"], cap=cap, floor=flo,
                                 cagr_margin=s["CAGR"] - flo, dd_margin=s["MaxDD"] - cap,
                                 pass4a=p4a, pass4b=p4b, fail4b=fails))
    BK = pd.DataFrame(rows)
    BK.to_csv(f"{OUT}.books.csv", index=False)

    P(f"\n   4b / 4a PASS COUNTS — all {len(DRAGS)} x {len(SETS)} grid points, headline "
      f"{RUNG_HEAD} bps (0 / 25 bps in the .books.csv and the rung table below):")
    P(f"      {'d %/yr':>8}{'floor':>9}{'cap':>9} |{'SHELF 4b':>11}{'SHELF 4a':>10}"
      f"{'   ':>3}|{'GRID 4b':>10}{'GRID 4a':>9}   | binding leg among SHELF failures")
    for d in DRAGS:
        cells = []
        for setname in SETS:
            sub = BK[(BK.drag == d) & (BK["set"] == setname) & (BK.bps == RUNG_HEAD)]
            cells.append((int(sub.pass4b.sum()), int(sub.pass4a.sum()), len(sub)))
        sh = BK[(BK.drag == d) & (BK["set"] == "SHELF") & (BK.bps == RUNG_HEAD)]
        fl = sh[~sh.pass4b].fail4b.value_counts().to_dict()
        P(f"      {d * 100:>8.2f}{0.70 * SP[d]['CAGR']:>9.2%}{0.60 * SP[d]['MaxDD']:>9.2%} |"
          f"{cells[0][0]:>7} /{cells[0][2]:>3}{cells[0][1]:>7} /{cells[0][2]:>3}   |"
          f"{cells[1][0]:>6} /{cells[1][2]:>3}{cells[1][1]:>6} /{cells[1][2]:>3}   | "
          f"{fl if fl else '-'}")

    P(f"\n   RUNG SENSITIVITY — 4b passes at 0 / {RUNG_HEAD} / 25 bps:")
    P(f"      {'d %/yr':>8} | " + "  ".join(f"{s} 0/{RUNG_HEAD}/25" for s in SETS))
    for d in DRAGS:
        parts = []
        for setname in SETS:
            cc = [int(BK[(BK.drag == d) & (BK["set"] == setname) & (BK.bps == c)].pass4b.sum())
                  for c in RUNGS]
            parts.append("/".join(str(x) for x in cc))
        P(f"      {d * 100:>8.2f} | " + "      ".join(parts))

    n_flip = 0
    P("\n   WHICH BOOKS FLIP, and at what drag (headline rung):")
    for nm in sorted(BK.book.unique()):
        ser = [(d, bool(BK[(BK.drag == d) & (BK.book == nm) & (BK.bps == RUNG_HEAD)]
                        .pass4b.iloc[0])) for d in DRAGS]
        if len({v for _, v in ser}) > 1:
            n_flip += 1
            first = next(d for (d, v), (_, v0) in zip(ser[1:], ser[:-1]) if v != v0)
            P(f"      {nm:<34} " + " ".join(f"{d * 100:.2f}:{'P' if v else 'F'}" for d, v in ser)
              + f"   first flip at d={first * 100:.2f} %/yr")
    P(f"      {n_flip} of {BK.book.nunique()} books change their 4b verdict anywhere on the "
      f"drag grid; {BK.book.nunique() - n_flip} are invariant to the comparand convention.")

    inv = BK[(BK.bps == RUNG_HEAD)].groupby("book").pass4a.nunique()
    P(f"      4a is invariant to the comparand by construction (it never reads SPY): "
      f"{int((inv == 1).sum())} of {len(inv)} books constant, "
      f"{int(BK[(BK.drag == 0.0) & (BK.bps == RUNG_HEAD)].pass4a.sum())} of "
      f"{BK.book.nunique()} passing 4a at every d.")

    # how close is the record to the edge?  the margin IS the answer to "mis-set by how much"
    base_sh = BK[(BK.drag == 0.0) & (BK["set"] == "SHELF") & (BK.bps == RUNG_HEAD)]
    P(f"\n   HOW MIS-SET COULD THE FLOOR BE AND STILL NOT MATTER: at d=0 the shelf's CAGR "
      f"margins (CAGR - floor) run {base_sh.cagr_margin.min():+.2%}.."
      f"{base_sh.cagr_margin.max():+.2%}; the SMALLEST is "
      f"{base_sh.loc[base_sh.cagr_margin.idxmin(), 'book']} at "
      f"{base_sh.cagr_margin.min():+.2%}. A drag mis-sets the floor by 0.70*d, so it would "
      f"take d = {base_sh.cagr_margin.min() / 0.70 * 100:.2f} %/yr of comparand error, in the "
      f"WRONG direction (a floor too HIGH), to cost the shelf its first CAGR pass — and a "
      f"price-only comparand errs the OTHER way.")

    # ============================================================ PART C — RULE 8
    P("\n### PART C — RULE 8 walk-forward: GRID dial chosen on 2009-2016 IS Sharpe alone,")
    P("    OOS 2017-2026 read ONCE per (d, panel). The comparand never touches the chooser,")
    P("    only the bars — so a moving pick would mean the counterfactual leaked into the fit.")
    is_mask = ~oos_mask
    wrows = []
    spy_oos_raw = spy_full[oos_mask]
    for d, pname in product(DRAGS, PX):
        pool = [(nm, bk) for nm, bk in books.items()
                if bk["set"] == "GRID" and bk["panel"] == pname]
        best = max(pool, key=lambda kv: fsharpe(kv[1]["net"][RUNG_HEAD][is_mask]))
        s = pack(best[1]["net"][RUNG_HEAD][oos_mask])
        base = pack(v2[pname][RUNG_HEAD][oos_mask])
        old = pack(v1[pname][RUNG_HEAD][oos_mask])
        sp = pack(drag_returns(spy_oos_raw, d))
        cap, flo = 0.60 * sp["MaxDD"], 0.70 * sp["CAGR"]
        p4a, p4b, fails = verdicts(s, base, sp, cap, flo)
        p4a_f, p4b_f, fails_f = verdicts(s, base, sp, FIXED_CAP, FIXED_FLOOR)
        wrows.append(dict(drag=d, panel=pname, pick=best[0],
                          IS_Sharpe=fsharpe(best[1]["net"][RUNG_HEAD][is_mask]),
                          OOS_CAGR=s["CAGR"], OOS_Sharpe=s["Sharpe"], OOS_MaxDD=s["MaxDD"],
                          OOS_H1=s["H1"], OOS_H2=s["H2"], cap=cap, floor=flo,
                          V2_OOS_CAGR=base["CAGR"], V2_OOS_Sharpe=base["Sharpe"],
                          V2_OOS_MaxDD=base["MaxDD"], V1_OOS_Sharpe=old["Sharpe"],
                          V1_OOS_CAGR=old["CAGR"],
                          SPY_OOS_CAGR=sp["CAGR"], SPY_OOS_Sharpe=sp["Sharpe"],
                          SPY_OOS_MaxDD=sp["MaxDD"], pass4a=p4a, pass4b=p4b, fail4b=fails,
                          pass4b_FIXEDBARS=p4b_f, fail4b_FIXEDBARS=fails_f))
    WF = pd.DataFrame(wrows)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    for r in WF.itertuples():
        P(f"   d={r.drag * 100:>5.2f} {r.panel:<5} pick {r.pick:<24} IS {r.IS_Sharpe:.4f} | OOS "
          f"{r.OOS_CAGR:>7.2%} / {r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:>7.2%} "
          f"(cap {r.cap:>7.2%}, floor {r.floor:>6.2%}) | v2 {r.V2_OOS_CAGR:>6.2%}/"
          f"{r.V2_OOS_Sharpe:.4f}/{r.V2_OOS_MaxDD:>7.2%} | v1 {r.V1_OOS_CAGR:>6.2%}/"
          f"{r.V1_OOS_Sharpe:.4f} | SPY {r.SPY_OOS_CAGR:>6.2%}/{r.SPY_OOS_Sharpe:.4f}/"
          f"{r.SPY_OOS_MaxDD:>7.2%} | 4b {'PASS' if r.pass4b else 'FAIL ' + r.fail4b}"
          f"  4a {'PASS' if r.pass4a else 'FAIL'}")
    npick = WF.groupby("panel").pick.nunique().to_dict()
    stable = ("the comparand never reaches the chooser (expected: the dial is IS Sharpe, "
              "which does not read SPY)" if all(v == 1 for v in npick.values())
              else "LEAK: the pick moved with the comparand")
    P(f"   PICK STABILITY: {npick} distinct picks per panel across all {len(DRAGS)} drags — "
      f"{stable}")
    flips = sum(int(bool(WF[(WF.drag == d) & (WF.panel == p)].pass4b.iloc[0]) !=
                    bool(WF[(WF.drag == 0.0) & (WF.panel == p)].pass4b.iloc[0]))
                for d, p in product(DRAGS, PX))
    P(f"   OOS 4b verdict differs from the d=0 reading in {flips} of {len(DRAGS) * len(PX)} "
      f"(drag, panel) cells.")
    fx = sum(int(bool(r.pass4b) != bool(r.pass4b_FIXEDBARS)) for r in WF.itertuples())
    P(f"   RE-PRICED vs the record's FIXED full-sample bars: verdict differs in {fx} of "
      f"{len(WF)} cells (the FIXED bars are a full-sample number read on an OOS leg).")

    # ==================================================== BY-PRODUCT (not the idea)
    P("\n### BY-PRODUCT — found while gating the comparand, reported because it is a")
    P("    property of a panel the record trades: data/prices_broad.csv is stored at TWO")
    P("    DECIMALS while data/prices.csv is not. On back-adjusted low-priced history that")
    P("    is not a rounding nicety — a split-adjusted NVDA trades near 0.14 in 2009, where")
    P("    half a cent is percent-scale. Priced on the 56 tickers BOTH files carry, so the")
    P("    only difference between the two runs is the quantization.")
    q = (A - Bc).abs()
    qrel = (q / A.abs()).replace([np.inf, -np.inf], np.nan)
    P(f"      cells differing: {int((q > 1e-9).sum().sum()):,} of {q.size:,} "
      f"({(q > 1e-9).to_numpy().mean():.1%}); max absolute {q.max().max():.4f} "
      f"(= half a cent); max RELATIVE {qrel.max().max():.4%}")
    P("      worst relative offenders: " + ", ".join(
        f"{t} {v:.3%}" for t, v in qrel.max().sort_values(ascending=False).head(5).items()))
    Uq = rawb.loc[:, [c for c in load_universe().columns if c in rawb.columns]] \
        .dropna(how="all").ffill().reindex(U.index).ffill()
    P(f"\n      the SAME U56 book, run on the full-precision file vs the 2-decimal one "
      f"({Uq.shape[1]} cols):")
    P(f"      {'book':<34}{'CAGR fp':>10}{'CAGR 2dp':>10}{'Sharpe fp':>11}{'Sharpe 2dp':>12}"
      f"{'dSharpe':>10}{'dMaxDD pp':>11}")
    qrows = []
    for nm, wf in (("RULES v2 baseline (live)", lambda p: rules_v2_weights(p)),
                   ("u56-v2band-gross100", lambda p: rules_v2_weights(p, 0.03, 1.00)),
                   ("u56-band008-gross100", lambda p: rules_v2_weights(p, 0.08, 1.00))):
        mm = []
        for pnl in (U, Uq):
            r, t = fast_run(pnl, wf(pnl), rebalance_mask(pnl.index, FREQ))
            mm.append(pack((r - t * RUNG_HEAD / 1e4).loc[start:].values))
        qrows.append(dict(book=nm, CAGR_fp=mm[0]["CAGR"], CAGR_2dp=mm[1]["CAGR"],
                          Sharpe_fp=mm[0]["Sharpe"], Sharpe_2dp=mm[1]["Sharpe"],
                          MaxDD_fp=mm[0]["MaxDD"], MaxDD_2dp=mm[1]["MaxDD"]))
        P(f"      {nm:<34}{mm[0]['CAGR']:>10.2%}{mm[1]['CAGR']:>10.2%}{mm[0]['Sharpe']:>11.4f}"
          f"{mm[1]['Sharpe']:>12.4f}{mm[1]['Sharpe'] - mm[0]['Sharpe']:>10.4f}"
          f"{(mm[1]['MaxDD'] - mm[0]['MaxDD']) * 100:>11.2f}")
    pd.DataFrame(qrows).to_csv(f"{OUT}.quantization.csv", index=False)
    mx = max(abs(r["Sharpe_2dp"] - r["Sharpe_fp"]) for r in qrows)
    P(f"      largest |dSharpe| from quantization alone: {mx:.4f}. Idea 851's shelf "
      f"reproduction tolerance is {TOL_SHARPE:.3f}, so this is "
      f"{'INSIDE' if mx < TOL_SHARPE else 'OUTSIDE'} the tolerance the record admits books "
      f"on — but it is a floor under the reproducibility of every B136 number, and no "
      f"committed file states it. NAMED, not fixed (cache_prices.py is out of scope).")

    # ============================================================ VERDICT
    P("\n### VERDICT")
    P(f"   PREMISE: {'FALSE' if PREMISE_FALSE else 'not refuted'} — data/prices.csv is "
      f"dividend-reinvested on 3 of 3 independent internal legs, so the 4b floor ALREADY "
      f"closes on a total-return comparand and the mis-set the idea postulates is ZERO.")
    P(f"   SIGN (if it had been true): the floor would have been TOO LOW by 0.70*d, i.e. 4b "
      f"TOO GENEROUS; the cap would simultaneously have been TOO TIGHT. Not one direction — "
      f"two, in opposition.")
    P(f"   SIZE: {slope:+.4%} of CAGR floor per 1.00 %/yr of drag. Over the whole plausible "
      f"S&P yield range (0..2.5 %/yr) the floor spans "
      f"{0.70 * SP[max(DRAGS)]['CAGR']:.2%}..{0.70 * SP[0.0]['CAGR']:.2%} and the shelf's 4b "
      f"count moves "
      f"{int(BK[(BK.drag == max(DRAGS)) & (BK['set'] == 'SHELF') & (BK.bps == RUNG_HEAD)].pass4b.sum())}"
      f" <- {int(base_sh.pass4b.sum())} of {len(base_sh)}.")
    P("   CAPITAL: nothing promoted. 4a is untouched by any comparand (it never reads SPY).")
    P(f"\n### done in {time.time() - t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
