#!/usr/bin/env python3
"""Idea 921 (lane cloud, 2026-09-22) — PUBLISH THE FIVE-LEG COST CLOSING PRICE, NOT THE
WINDOW'S, BESIDE EVERY 4b PASS.

WHERE THIS COMES FROM.  Idea 675 (lane B, second cut) bisected TWO DIFFERENT closing prices on
the SAME book: the DD-cap x CAGR-floor WINDOW closes at 34.9 bps on U56 while the FIVE-LEG 4b
PASS closes at 21.8 bps, and on B136 the five-leg price is 6.1 bps — BELOW PROTOCOL's own 10 bps
rung.  Quoting the window's price overstates the tolerance 1.6x on that one book.  The record
quotes cost tolerance constantly and has never said which of the two it means.

THE QUESTION.  On a FRESHLY PRICED corpus of committed-shaped books (this run harvests no prose):
how far apart are the two closing prices, how often does the window stay open after the 4b pass
has already closed, and WHICH LEG actually closes first?  If the closing leg is usually one of
the three SHARPE legs, the DD x CAGR window is structurally blind to it and every tolerance the
record has quoted from a window is an overstatement of unknown size.

DEFINITIONS (both are cost-axis bisections on one and the same book and tape).
  c_WINDOW  = the largest cost c at which the TWO LEVEL legs both hold:
              L4_DD   MaxDD_full  >= 0.60 x SPY MaxDD_full
              L5_CAGR CAGR_full   >= 0.70 x SPY CAGR_full
  c_5LEG    = the largest cost c at which ALL FIVE 4b legs hold: L1_H1, L2_H2 (Sharpe > SPY in
              both halves), L3_OOS (OOS Sharpe > SPY OOS), L4_DD, L5_CAGR.
  SPY is NOT charged the book's costs (protocol convention), so both prices are the cost the
  BOOK can bear before it stops clearing the bar it is quoted against.
  OVERSTATEMENT = c_WINDOW / c_5LEG.  CLOSING LEG = the leg that fails first as c rises.

WHAT IS PRICED.  72 cells per (panel x cadence), all price-only on the committed caches:
    SHELF  families MOM / MOMVS / MADIST / LOWVOL x width k in {5,10,20,40,ALL}
           x gross in {0.50,0.75,1.00}                                    = 60 cells
    BAND   200d-MA band with hysteresis, band in {0.00,0.03,0.05,0.08} x the same gross rungs
                                                                          = 12 cells
  Panels U56 / B136, cadences W / M, fills t+1 -> 288 books, every one published.

THE TWO TUNED DIALS (and no more).
  DIAL 1 — CLAIM (BOOK) SET: {ALL books, 4b PASSES at 10 bps, WINDOW-OPEN books at 10 bps}.
           Every headline is reported on all three, so no set can be chosen after the fact.
  DIAL 2 — COST GRID: FINE (continuous bisection on [0,200] bps to 0.05 bps) and COARSE (the
           record's own quoted rungs {0,10,25,50,100} bps).  Both conventions are published and
           their discretisation gap is reported.
REPORTED, NOT TUNED: panel, cadence, family, width, gross.

PRE-STATED VERDICT RULES (fixed before the run, not adjusted after).
  V1  OVERSTATEMENT.  Median c_WINDOW / c_5LEG over the books where both prices are finite is
      >= 1.25.  Triggered -> 675's 1.6x is a property of the corpus, not of one book.
  V2  SILENT CLOSURE.  More than 10% of all books have the WINDOW OPEN at 10 bps while the
      FIVE-LEG pass is already CLOSED there.  Triggered -> a window-quoted tolerance can be
      wrong about the protocol rung itself, not merely optimistic above it.
  V3  BLIND WINDOW.  On more than 50% of the books with a finite five-leg price, the CLOSING LEG
      is one of the three SHARPE legs (L1_H1 / L2_H2 / L3_OOS), i.e. a leg the window cannot
      see.  Triggered -> the window is structurally blind, not just looser.
  V4  CAPITAL.  A legal IS-only chooser (rule 8: 2009-2016 only) reaches a book that clears 4b
      FULL+OOS at 10 bps AND whose five-leg price is >= 25 bps — a pass with real headroom.

PROTOCOL: rule 2 (10 bps headline, t+1 fills, no shorting, no leverage — gate G1); rule 3 (live
RULES v2 AND SPY); rule 4 (both KEEP paths, <= 2 tuned dials); rule 5 (one idea, deterministic,
standalone); rule 8 (dials chosen on 2009-2016, 2017-2026 read ONCE); rule 9 (survivorship).
RULES.md / scan.py / bot.py / baseline.py are NOT modified.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists: every CAGR and MaxDD LEVEL
is optimistic, so both closing prices are biased HIGH in absolute terms.  The object this run
reports is the RATIO of two prices on one and the same book and tape, which is first-order
immune; the absolute bps figures and the 4b pass counts are not.

Run:  python research/backtests/2026-09-22_five-leg-vs-window-cost-close_cloud.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state, score      # noqa: E402
from engine import backtest as engine_backtest                               # noqa: E402

DATE, SLUG = "2026-09-22", "five-leg-vs-window-cost-close"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

PANELS = ["U56", "B136"]
CADENCES = ["W", "M"]
FAMILIES = ["MOM", "MOMVS", "MADIST", "LOWVOL"]
WIDTHS = [5, 10, 20, 40, "ALL"]
GROSSES = [0.50, 0.75, 1.00]
BANDS = [0.00, 0.03, 0.05, 0.08]
COARSE = [0, 10, 25, 50, 100]                 # dial 2, the record's own quoted rungs
CMAX, CTOL = 200.0, 0.05                      # dial 2, fine bisection range / tolerance
PROTOCOL_COST = 10.0
WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
MAX_VOL = 0.60
SHARPE_LEGS = ["L1_H1", "L2_H2", "L3_OOS"]
WINDOW_LEGS = ["L4_DD", "L5_CAGR"]
LEGS = SHARPE_LEGS + WINDOW_LEGS

_log: list[str] = []
_gates: list[dict] = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _log.append(s)


def gate(name, value, target, ok):
    _gates.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    log(f"  GATE {'PASS' if ok else 'FAIL'}  {name}: {value}   (target {target})")
    return bool(ok)


def net(r0, t0, c):
    return r0 - t0 * c / 1e4


def mets(r):
    r = r.dropna()
    eq = (1 + r).cumprod()
    yrs = len(r) / 252.0
    vol = r.std() * np.sqrt(252.0)
    return dict(CAGR=eq.iloc[-1] ** (1 / yrs) - 1 if yrs else np.nan,
                Sharpe=(r.mean() * 252.0) / vol if vol else np.nan,
                MaxDD=float((eq / eq.cummax() - 1).min()))


def halves(r):
    h = len(r) // 2
    return mets(r.iloc[:h])["Sharpe"], mets(r.iloc[h:])["Sharpe"]


# --------------------------------------------------------------------------- panel / books
def panel(name):
    px = (load_universe() if name == "U56" else load_universe(broad=True))
    return px.dropna(how="all").ffill()


def signals(px):
    comp_ns, above, vol20 = score(px, vol_scale=False)
    comp_vs, _, _ = score(px, vol_scale=True)
    gate_ = above & (vol20 < MAX_VOL) & px.notna()
    sig = dict(MOM=comp_ns, MOMVS=comp_vs, MADIST=px / px.rolling(200).mean() - 1.0,
               LOWVOL=-vol20)
    return sig, {f: gate_ & sig[f].notna() for f in sig}


def eq_weights(elig, gross):
    n = elig.sum(axis=1).replace(0, np.nan)
    return elig.astype(float).div(n, axis=0).fillna(0.0) * gross


def book_frame(kind, a, b, px, sig, elig):
    """kind='SHELF' -> a=(family,k), b=gross;  kind='BAND' -> a=band, b=gross."""
    if kind == "BAND":
        return eq_weights(band_state(px, a) & px.notna(), b)
    fam, k = a
    e = elig[fam]
    if k == "ALL":
        return eq_weights(e, b)
    # method="first" breaks ties by column order: EXACTLY k names, never k+ties, so a book's
    # target gross can never exceed `b` (protocol rule 2, gate G1).
    rank = sig[fam].where(e).rank(axis=1, ascending=False, method="first")
    return (rank <= k).astype(float) * (b / k)


# --------------------------------------------------------------------------- leg algebra
def legs_at(r0, t0, c, S):
    r = net(r0, t0, c)
    mf, mo = mets(r), mets(r.loc[OOS_START:])
    h1, h2 = halves(r)
    return {"L1_H1": h1 - S["h1"], "L2_H2": h2 - S["h2"],
            "L3_OOS": mo["Sharpe"] - S["oos"]["Sharpe"],
            "L4_DD": mf["MaxDD"] - DD_CAP * S["full"]["MaxDD"],
            "L5_CAGR": mf["CAGR"] - CAGR_FLOOR * S["full"]["CAGR"]}


def open_at(mar, legset):
    return all(mar[k] > 0 for k in legset)


def closing_price(r0, t0, S, legset, cache):
    """Largest c in [0, CMAX] at which every leg in legset holds, by bisection to CTOL bps.
    Returns (price, closing_leg).  price = 0.0 if already closed at c=0 (closing leg reported
    from c=0); price = CMAX if still open at the top of the range (right-censored)."""
    def ok(c):
        if c not in cache:
            cache[c] = legs_at(r0, t0, c, S)
        return cache[c]
    m0 = ok(0.0)
    if not open_at(m0, legset):
        return 0.0, "|".join(k for k in legset if not (m0[k] > 0))
    mtop = ok(CMAX)
    if open_at(mtop, legset):
        return CMAX, "CENSORED"
    lo, hi = 0.0, CMAX
    while hi - lo > CTOL:
        mid = 0.5 * (lo + hi)
        if open_at(ok(mid), legset):
            lo = mid
        else:
            hi = mid
    mhi = ok(hi)
    bad = [k for k in legset if not (mhi[k] > 0)]
    return lo, "|".join(bad)


def coarse_price(r0, t0, S, legset, cache):
    """The record's convention: the largest QUOTED rung at which the leg set still holds."""
    def ok(c):
        if c not in cache:
            cache[c] = legs_at(r0, t0, float(c), S)
        return cache[c]
    best = np.nan
    for c in COARSE:
        if open_at(ok(float(c)), legset):
            best = float(c)
        else:
            break
    return best


# --------------------------------------------------------------------------------------- run
def main():
    log(f"# Idea 921 (lane cloud, {DATE}) — publish the FIVE-LEG cost closing price, not the "
        f"WINDOW's, beside every 4b pass.")
    log(f"# TUNED DIALS (2): CLAIM SET (ALL / 4b-PASS-at-10bps / WINDOW-OPEN-at-10bps) and COST "
        f"GRID (FINE bisection [0,{CMAX:.0f}] bps to {CTOL} bps; COARSE rungs {COARSE}).")
    log(f"# reported, not tuned: PANEL {PANELS} x CADENCE {CADENCES} x family/width/gross.  "
        f"72 books per (panel x cadence) = 288 books, all published.")
    log(f"# COMPARAND (committed, idea 675, NOT recomputed here): window 34.9 bps vs five-leg "
        f"21.8 bps on U56 (1.60x); five-leg 6.1 bps on B136, below the 10 bps protocol rung.")

    rows, g_gross, g_mono, g_bis = [], 0.0, 0, 0.0
    for pname in PANELS:
        px = panel(pname)
        st = px.index[WARMUP]
        sig, elig = signals(px)
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        h1s, h2s = halves(spy)
        S = dict(full=mets(spy), oos=mets(spy.loc[OOS_START:]), is_=mets(spy.loc[:IS_END]),
                 h1=h1s, h2=h2s)
        log(f"\n## {pname}: {px.shape[1]} cols, {len(px)} rows ({len(px)/252:.1f}y), book from "
            f"{st.date()}")
        log(f"   SPY FULL {S['full']['CAGR']:.2%}/{S['full']['Sharpe']:.3f}/"
            f"{S['full']['MaxDD']:.2%} (H1 {h1s:.3f} H2 {h2s:.3f});  SPY OOS "
            f"{S['oos']['CAGR']:.2%}/{S['oos']['Sharpe']:.3f}/{S['oos']['MaxDD']:.2%}"
            f"  ->  4b FULL bars: DD {DD_CAP*S['full']['MaxDD']:.2%}, CAGR "
            f"{CAGR_FLOOR*S['full']['CAGR']:.2%}")

        lb = engine_backtest(px, rules_v2_weights(px, 0.03, 0.75), cost_bps=0.0, freq="W")
        lr0, lt0 = lb["returns"].loc[st:], lb["turnover"].loc[st:]
        lr = net(lr0, lt0, PROTOCOL_COST)
        la1, la2 = halves(lr)
        LV = dict(full=mets(lr), oos=mets(lr.loc[OOS_START:]), h1=la1, h2=la2)
        log(f"   RULES v2 live @10bps FULL {LV['full']['CAGR']:.2%}/{LV['full']['Sharpe']:.3f}/"
            f"{LV['full']['MaxDD']:.2%};  OOS {LV['oos']['CAGR']:.2%}/{LV['oos']['Sharpe']:.3f}"
            f"/{LV['oos']['MaxDD']:.2%}")

        specs = ([("SHELF", (f, k), g) for f in FAMILIES for k in WIDTHS for g in GROSSES]
                 + [("BAND", b, g) for b in BANDS for g in GROSSES])
        for freq in CADENCES:
            for kind, a, b in specs:
                W = book_frame(kind, a, b, px, sig, elig).reindex(
                    columns=px.columns).fillna(0.0)
                res = engine_backtest(px, W, cost_bps=0.0, freq=freq)
                g_gross = max(g_gross, float(res["weights"].sum(axis=1).max()))
                r0, t0 = res["returns"].loc[st:], res["turnover"].loc[st:]
                cache: dict[float, dict] = {}
                c_win, leg_win = closing_price(r0, t0, S, WINDOW_LEGS, cache)
                c_5, leg_5 = closing_price(r0, t0, S, LEGS, cache)
                k_win = coarse_price(r0, t0, S, WINDOW_LEGS, cache)
                k_5 = coarse_price(r0, t0, S, LEGS, cache)
                m10 = legs_at(r0, t0, PROTOCOL_COST, S) if PROTOCOL_COST not in cache \
                    else cache[PROTOCOL_COST]
                r10 = net(r0, t0, PROTOCOL_COST)
                mf, mo, mi = mets(r10), mets(r10.loc[OOS_START:]), mets(r10.loc[:IS_END])
                hh1, hh2 = halves(r10)
                ih1, ih2 = halves(r10.loc[:IS_END])
                k4bf = open_at(m10, LEGS)
                k4bo = (mo["Sharpe"] > S["oos"]["Sharpe"]
                        and mo["MaxDD"] >= DD_CAP * S["oos"]["MaxDD"]
                        and mo["CAGR"] >= CAGR_FLOOR * S["oos"]["CAGR"])
                # G2 monotonicity: the five-leg set must not re-open above its closing price
                for cc in (c_5 + 5.0, c_5 + 20.0):
                    if cc <= CMAX and open_at(legs_at(r0, t0, cc, S), LEGS) and c_5 < CMAX:
                        g_mono += 1
                if 0.0 < c_5 < CMAX:                      # bisection accuracy check
                    g_bis = max(g_bis, 0.0 if open_at(legs_at(r0, t0, c_5, S), LEGS) else 1.0)
                rows.append(dict(
                    panel=pname, cadence=freq, kind=kind,
                    book=(f"{a[0]}/{a[1]}/{b}" if kind == "SHELF" else f"BAND{a}/{b}"),
                    family=(a[0] if kind == "SHELF" else "BAND"),
                    width=(str(a[1]) if kind == "SHELF" else str(a)), gross=b,
                    c_window=c_win, c_5leg=c_5, close_leg_5=leg_5, close_leg_win=leg_win,
                    k_window=k_win, k_5leg=k_5,
                    win_open10=bool(open_at(m10, WINDOW_LEGS)),
                    keep4b_full=bool(k4bf), keep4b_oos=bool(k4bo),
                    keep4b=bool(k4bf and k4bo),
                    keep4a=bool(hh1 > LV["h1"] and hh2 > LV["h2"]
                                and mf["MaxDD"] >= LV["full"]["MaxDD"]),
                    keep4a_oos=bool(mo["Sharpe"] > LV["oos"]["Sharpe"]
                                    and mo["MaxDD"] >= LV["oos"]["MaxDD"]),
                    CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=hh1, H2=hh2,
                    is_Sharpe=mi["Sharpe"], is_CAGR=mi["CAGR"], is_MaxDD=mi["MaxDD"],
                    is_legs=(int(ih1 > halves(spy.loc[:IS_END])[0])
                             + int(ih2 > halves(spy.loc[:IS_END])[1])
                             + int(mi["MaxDD"] >= DD_CAP * S["is_"]["MaxDD"])
                             + int(mi["CAGR"] >= CAGR_FLOOR * S["is_"]["CAGR"])),
                    oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                    spy_oos_S=S["oos"]["Sharpe"], live_oos_S=LV["oos"]["Sharpe"]))
            log(f"   {pname} {freq}: {len(specs)} books priced")

    D = pd.DataFrame(rows)
    D.to_csv(f"{OUT}.books.csv", index=False)
    log(f"\n{len(D)} books written to {Path(OUT).name}.books.csv")

    gate("G1 no leverage (max gross over every book)", f"{g_gross:.4f}", "<= 1.0001",
         g_gross <= 1.0001)
    gate("G2 five-leg set never re-opens above its closing price", f"{g_mono} re-openings",
         "0", g_mono == 0)
    gate("G3 bisected price is itself open (all five legs hold at c_5leg)",
         f"{g_bis:.0f} violations", "0", g_bis == 0)

    both = D[(D.c_5leg > 0) & (D.c_window > 0)].copy()
    both["ratio"] = both.c_window / both.c_5leg
    log(f"\n## THE TWO PRICES.  {len(both)} of {len(D)} books have BOTH prices strictly above "
        f"zero; {(D.c_window<=0).sum()} have the window closed at 0 bps and "
        f"{(D.c_5leg<=0).sum()} have the five-leg pass closed at 0 bps.")
    log(f"   c_WINDOW  median {both.c_window.median():.2f} bps  (p25 "
        f"{both.c_window.quantile(.25):.2f}, p75 {both.c_window.quantile(.75):.2f}, censored at "
        f"{CMAX:.0f}: {(both.c_window>=CMAX).sum()})")
    log(f"   c_5LEG    median {both.c_5leg.median():.2f} bps  (p25 "
        f"{both.c_5leg.quantile(.25):.2f}, p75 {both.c_5leg.quantile(.75):.2f}, censored: "
        f"{(both.c_5leg>=CMAX).sum()})")
    med_ratio = float(both.ratio.median())
    log(f"   RATIO c_WINDOW / c_5LEG: median {med_ratio:.2f}x, mean {both.ratio.mean():.2f}x, "
        f"p90 {both.ratio.quantile(.90):.2f}x, max {both.ratio.max():.2f}x, "
        f"share > 1.0: {(both.ratio>1.0).mean():.1%}")
    log("   by panel x cadence (median ratio, n):")
    for (p, f), s in both.groupby(["panel", "cadence"]):
        log(f"      {p} {f}: {s.ratio.median():.2f}x  (n={len(s)}, median window "
            f"{s.c_window.median():.1f} bps, median five-leg {s.c_5leg.median():.1f} bps)")
    log("   by family (median ratio, n):")
    for fam, s in both.groupby("family"):
        log(f"      {fam:7s} {s.ratio.median():.2f}x  (n={len(s)}, window "
            f"{s.c_window.median():.1f}, five-leg {s.c_5leg.median():.1f})")
    v1 = gate("V1 OVERSTATEMENT: median c_WINDOW / c_5LEG", f"{med_ratio:.2f}x", ">= 1.25",
              med_ratio >= 1.25)

    silent = D[(D.win_open10) & (~D.keep4b_full)]
    share = len(silent) / len(D)
    log(f"\n## SILENT CLOSURE AT THE PROTOCOL RUNG.  {len(silent)} of {len(D)} books "
        f"({share:.1%}) have the DD x CAGR WINDOW OPEN at 10 bps while the FIVE-LEG pass is "
        f"already CLOSED there.  A window-quoted tolerance calls these books cost-tolerant when "
        f"their 4b pass does not exist at the protocol rung at all.")
    log(f"   of the {int(D.win_open10.sum())} window-open books at 10 bps, "
        f"{int(D[D.win_open10].keep4b_full.sum())} actually clear the five legs "
        f"({D[D.win_open10].keep4b_full.mean():.1%}).")
    v2 = gate("V2 SILENT CLOSURE: share of books with window open and five-leg closed at 10 bps",
              f"{share:.3f}", "> 0.10", share > 0.10)

    fin = D[(D.c_5leg > 0) & (D.c_5leg < CMAX)]
    cl = fin.close_leg_5.str.split("|").explode().value_counts()
    sh = float(fin.close_leg_5.apply(
        lambda s: any(x in SHARPE_LEGS for x in s.split("|"))).mean())
    log(f"\n## WHICH LEG CLOSES FIRST ({len(fin)} books with a finite five-leg price):")
    for k, v in cl.items():
        log(f"      {k:8s} {v:4d} ({v/len(fin):.1%} of books)")
    log(f"   share of books whose closing leg includes a SHARPE leg the window cannot see: "
        f"{sh:.1%}")
    v3 = gate("V3 BLIND WINDOW: share closing on a SHARPE leg", f"{sh:.3f}", "> 0.50", sh > 0.50)

    # MECHANISM.  The two prices can only differ when the leg that closes the five-leg set is a
    # leg the window cannot see.  Split the corpus on exactly that and report both sides.
    is_sh = fin.close_leg_5.apply(lambda s: any(x in SHARPE_LEGS for x in s.split("|")))
    A = fin[is_sh & (fin.c_window > 0)].copy()      # closes on a Sharpe leg
    B = fin[~is_sh & (fin.c_window > 0)].copy()     # closes on a window leg
    for nm, sub in (("SHARPE-CLOSING", A), ("WINDOW-CLOSING", B)):
        if len(sub):
            rr = sub.c_window / sub.c_5leg
            log(f"   {nm:15s} n={len(sub):3d}  ratio median {rr.median():.2f}x, mean "
                f"{rr.mean():.2f}x, p90 {rr.quantile(.90):.2f}x, max {rr.max():.2f}x;  "
                f"identical prices: {(rr <= 1.0001).mean():.1%}")
    if len(A):
        rA = A.c_window / A.c_5leg
        log(f"   -> CONDITIONAL OVERSTATEMENT (the only population where 675's 1.6x can exist): "
            f"median {rA.median():.2f}x on {len(A)} of {len(fin)} books "
            f"({len(A)/len(fin):.1%} of the corpus).")
    p4b_fin = D[(D.keep4b) & (D.c_5leg < CMAX)]
    if len(p4b_fin):
        sh4 = p4b_fin.close_leg_5.apply(lambda s: any(x in SHARPE_LEGS for x in s.split("|")))
        r4 = p4b_fin.c_window / p4b_fin.c_5leg
        log(f"   among the {len(p4b_fin)} 4b passes at 10 bps: {int(sh4.sum())} "
            f"({sh4.mean():.1%}) close on a Sharpe leg; their ratio median "
            f"{r4[sh4].median() if sh4.any() else float('nan'):.2f}x vs "
            f"{r4[~sh4].median() if (~sh4).any() else float('nan'):.2f}x for the rest.")

    log(f"\n## COARSE (record-convention) vs FINE prices.  Quoting the largest passing rung in "
        f"{COARSE} instead of bisecting:")
    cm = D[(D.k_5leg.notna()) & (D.c_5leg < CMAX)]
    log(f"   median understatement of the five-leg price by rung-quoting: "
        f"{(cm.c_5leg - cm.k_5leg).median():.2f} bps over {len(cm)} books; "
        f"{(cm.k_5leg == 0).mean():.1%} of them quote 0 bps for a price that is actually "
        f"positive.")

    # ------------------------------------------------------------------ rule 8 walk-forward
    log(f"\n## RULE 8 — WALK-FORWARD.  Dials picked on 2009-2016 rows ONLY (IS Sharpe and IS "
        f"legs); 2017-2026 read ONCE.  Both KEEP paths at the protocol {PROTOCOL_COST:.0f} bps "
        f"rung.")
    pk = []
    for (p, f), s in D.groupby(["panel", "cadence"]):
        s = s.sort_values("book").reset_index(drop=True)
        for ch, key in (("IS_SHARPE", s.is_Sharpe.values),
                        ("IS_LEGS", s.is_legs.values * 1e6 + s.is_Sharpe.values),
                        ("IS_DD", s.is_MaxDD.values)):
            row = s.iloc[int(np.argmax(np.nan_to_num(key, nan=-1e18)))]
            pk.append(dict(panel=p, cadence=f, chooser=ch, book=row.book,
                           c_window=row.c_window, c_5leg=row.c_5leg,
                           close_leg_5=row.close_leg_5,
                           oos_CAGR=row.oos_CAGR, oos_Sharpe=row.oos_Sharpe,
                           oos_MaxDD=row.oos_MaxDD, spy_oos_S=row.spy_oos_S,
                           live_oos_S=row.live_oos_S, CAGR=row.CAGR, Sharpe=row.Sharpe,
                           MaxDD=row.MaxDD, H1=row.H1, H2=row.H2,
                           keep4b_full=row.keep4b_full, keep4b_oos=row.keep4b_oos,
                           keep4b=row.keep4b, keep4a=row.keep4a, keep4a_oos=row.keep4a_oos))
    K = pd.DataFrame(pk)
    K.to_csv(f"{OUT}.picks.csv", index=False)
    log(K.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    log(f"   4b FULL+OOS among the {len(K)} rule-8 picks: {int(K.keep4b.sum())};  "
        f"4a FULL: {int(K.keep4a.sum())};  4a OOS: {int(K.keep4a_oos.sum())}")
    head = K[(K.keep4b) & (K.c_5leg >= 25.0)]
    v4 = gate("V4 CAPITAL: a rule-8 pick clearing 4b FULL+OOS with five-leg price >= 25 bps",
              f"{len(head)}", ">= 1", len(head) >= 1)
    if len(head):
        log(head.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    p4b = D[D.keep4b]
    log(f"\n## THE CLAIM SET THAT MATTERS: the {len(p4b)} books that clear 4b FULL+OOS at 10 "
        f"bps (the corpus's own 'committed 4b passes').")
    if len(p4b):
        log(f"   their five-leg price: median {p4b.c_5leg.median():.1f} bps, min "
            f"{p4b.c_5leg.min():.1f}, p25 {p4b.c_5leg.quantile(.25):.1f}, max "
            f"{p4b.c_5leg.max():.1f};  window price median {p4b.c_window.median():.1f} bps "
            f"(ratio {(p4b.c_window/p4b.c_5leg).median():.2f}x)")
        log(f"   {int((p4b.c_5leg < 25).sum())} of {len(p4b)} die before the record's NEXT "
            f"quoted rung (25 bps); {int((p4b.c_5leg < 50).sum())} before 50 bps.")
        log(p4b[["panel", "cadence", "book", "c_window", "c_5leg", "close_leg_5", "CAGR",
                 "Sharpe", "MaxDD", "oos_Sharpe", "oos_MaxDD"]]
            .sort_values("c_5leg", ascending=False)
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    pd.DataFrame(_gates).to_csv(f"{OUT}.gates.csv", index=False)
    log(f"\n## VERDICT  V1 {'YES' if v1 else 'NO'} (overstatement >= 1.25x) | V2 "
        f"{'YES' if v2 else 'NO'} (silent closure at 10 bps) | V3 {'YES' if v3 else 'NO'} "
        f"(window blind to a Sharpe leg) | V4 {'YES' if v4 else 'NO'} (capital)")
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")


if __name__ == "__main__":
    main()
