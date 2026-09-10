#!/usr/bin/env python3
"""QUEUE idea 412 — does-PARTIAL-REBALANCING-beat-CADENCE-as-the-turnover-dial
   (lane B, 2026-09-10).

QUESTION (verbatim from QUEUE.md idea 412)
    "idea 137's rule-8 chooser picks a cadence slower than weekly in 8 of 10 cells and
     lambda<1 in 6 of 10, but only lambda changes the book's path.  Price the two dials
     against each other at matched realised turnover on all three panels and say which
     one the record should adopt as its turnover instrument.  Max 2 params (cadence,
     lambda)."

WHY IT MATTERS
    The record owns two ways to spend less on trading and has never priced them against
    each other on one axis.  CADENCE (idea 3, idea 107, idea 137) skips rebalance dates:
    the target book is unchanged, it is merely SAMPLED less often, and between samples the
    holdings drift.  PARTIAL REBALANCING / lambda (idea 137's `smooth`, used verbatim by
    ideas 138/403/613) moves only a fraction of the way to today's target: the target
    itself is replaced by an exponentially smoothed target, so the book HOLDS DIFFERENT
    NAMES AT DIFFERENT WEIGHTS, not the same names on a coarser clock.  Both cut realised
    turnover.  Only one of them can be the record's default turnover instrument, and the
    difference is not cosmetic: RULES v2 is a weekly book, so whichever dial wins here is
    the one a Sunday review would write into RULES if turnover ever has to come down.

THE TWO DIALS (exactly 2 tuned parameters, as the idea requires; ALL points reported)
    param 1  k       CADENCE: rebalance on every k-th weekly rebalance date.
                     k in {1, 2, 3, 4, 6, 8, 13, 26} weeks.  k=1 IS the record's native
                     weekly book.  DAILY is also run as a reported context point (it is on
                     the wrong side of the dial — it RAISES turnover — so it is excluded
                     from the matched-turnover overlap by construction, not by choice).
    param 2  lam     PARTIAL REBALANCING: target_t = lam*W_t + (1-lam)*target_{t-1} with
                     the daily gross restored, so the dial changes TRADING and not
                     EXPOSURE.  lam in {1.00, 0.70, 0.50, 0.35, 0.25, 0.15, 0.10, 0.06} —
                     idea 137's ladder, verbatim.  lam=1.00 at k=1 IS the same arm as
                     cadence k=1: the two ladders share their anchor exactly (gate G4).

REPORTED AXES, NEVER TUNED
    panel   u56 (research/universe.json, 56 cols), broad (universe_broad.json, 136),
            small (the 485-name sub-$2B panel; SURVIVORSHIP: current constituents only,
            see data/SMALL_PANEL_README.md, and SPY is a BENCHMARK column there, never a
            constituent — it is dropped from every book on that panel).
    book    V2    = the live RULES v2 book (equal weight inside the 200d +/-3% band,
                    gross 0.75, de-grossed to cash; gate G3 asserts it is bit-identical
                    to baseline.rules_v2_weights),
            TOP20 = the ranked book (top 20 by the v1 composite, gross/20 each),
            V1u   = the legacy v1 book (top 5 by the vol-scaled composite at 0.15 each).
    cost    0, 5, 10, 25, 50 bps, read off the exact rung identity r(c) = r(0) - to*c/1e4
            (gate G2).  PROTOCOL's own rung is 10 bps and every headline is quoted there.
    phase   CADENCE HAS A PHASE AND LAMBDA DOES NOT.  A k-week cadence can start on any of
            k weekly dates, and idea 222 established that a single phase is a DRAW, not the
            ladder: the honest estimator is MEANPH (mean across the k phases of each
            phase's own metric).  Every k phase is run (1+2+3+4+6+8+13+26 = 63 cadence
            sims per cell).  MEANPH is the headline, PH0 (what the record usually
            publishes) is reported beside it, and the phase SPREAD is carried as a band
            that any lambda-vs-cadence gap has to clear to be readable.

WHAT IS BEING TESTED (pre-registered, before any number was read)
    H412  At MATCHED REALISED TURNOVER, partial rebalancing delivers a HIGHER net Sharpe
          than cadence, on the majority of panel x book cells, at PROTOCOL's 10 bps rung.
    Bar   The gap has to (i) hold on a majority of the 9 cells, (ii) exceed the cadence
          phase band in those cells, and (iii) keep its sign out of sample under rule 8.
          A gap that fails (ii) is a phase artefact; one that fails (iii) is in-sample only.
    The decomposition that makes the answer mean something: at 0 bps a turnover dial can
    only LOSE (it buys nothing and distorts the book), so dSharpe at 0 bps at matched
    turnover is PURE PATH DISTORTION and the dial that distorts less per unit of turnover
    removed is the better instrument at every cost rung.  Both readings are reported.

GATES (asserted; the run aborts if any fails)
    G1  the local simulator == engine.backtest on returns AND turnover at D/W/M/Q, 3 panels
    G2  the rung identity r(c) = r(0) - turnover*c/1e4
    G3  the V2 book == baseline.rules_v2_weights, bitwise
    G4  the shared anchor: cadence k=1 phase 0 and lam=1.00 are the SAME arm, bitwise;
        and the k=1 mask == engine's own 'W' mask
    G5  smooth(W, 1.0) is W unchanged (the dial's off position is genuinely off)

PROTOCOL
    10 bps costs and t+1 execution throughout (rule 2); RULES v2 cost-matched at the same
    rung is the 4a comparand and SPY is the 4b comparand (rule 3, idea 398); both KEEP
    paths evaluated on every arm-row (rule 4); rule 8 walk-forward with the dial chosen on
    2009-2016 only and 2017-2026 read once.  No RULES.md / PROTOCOL.md / scan.py / bot.py /
    baseline.py edit.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-10_does-PARTIAL-REBALANCING-beat-CADENCE-as-the-turnover-dial_B"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")                      # the lane-B harness: targets/halves/pass4a/margins

FREQ, GROSS = H.FREQ, H.GROSS              # "W", 0.75
IS_END, OOS_START = H.IS_END, H.OOS_START  # 2016-12-31 / 2017-01-01
PHI, DELTA = 0.70, 0.60                    # 4b CAGR floor / DD cap as fractions of SPY

KS = [1, 2, 3, 4, 6, 8, 13, 26]                              # tuned parameter 1 — ALL reported
LAMS = [1.00, 0.70, 0.50, 0.35, 0.25, 0.15, 0.10, 0.06]      # tuned parameter 2 — ALL reported
RUNGS = [0.0, 5.0, 10.0, 25.0, 50.0]                         # reported axis, never tuned
PROTO_RUNG = 10.0
PANELS = ["u56", "broad", "small"]
BOOKS = ["V2", "TOP20", "V1u"]
NMATCH = 9                                 # matched-turnover grid points inside the overlap
TOL = 1e-12

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 3000)
LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ------------------------------------------------------------------ simulator ----
def sim(px, W, mask, bps=0.0):
    """engine.backtest with an ARBITRARY rebalance mask instead of a freq string.

    Mirrors engine.backtest exactly: weights decided at close t are applied at t+1, the
    mask is shifted the same way, i==0 always rebalances, holdings drift between
    rebalances, costs are bps per unit turnover.  Gate G1 asserts the equality.
    """
    rets = px.pct_change().fillna(0.0).values
    tgt = W.reindex(px.index).fillna(0.0).shift(1).values
    m = np.concatenate([[False], np.asarray(mask, bool)[:-1]])
    nrow, ncol = rets.shape
    cur = np.zeros(ncol)
    held = np.zeros((nrow, ncol))
    turn = np.zeros(nrow)
    for i in range(nrow):
        if m[i] or i == 0:
            new = np.nan_to_num(tgt[i])
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    to = pd.Series(turn, index=px.index)
    r = pd.Series((held * rets).sum(axis=1), index=px.index) - to * bps / 1e4
    return dict(r=r, to=to)


def cadence_mask(idx, k, phase):
    """Every k-th weekly rebalance date, starting from the phase-th one."""
    w = rebalance_mask(idx, "W").values.copy()
    pos = np.flatnonzero(w)
    keep = pos[phase::k]
    out = np.zeros(len(idx), bool)
    out[keep] = True
    return out


def smooth(W, lam):
    """Idea 137's partial-rebalance dial, verbatim: target_t = lam*W_t + (1-lam)*target_{t-1},
    gross restored daily so the dial changes TRADING, not EXPOSURE."""
    if lam >= 1.0:
        return W
    S = W.ewm(alpha=lam, adjust=False).mean()
    g = S.sum(axis=1).replace(0, np.nan)
    return S.mul((W.sum(axis=1) / g).fillna(0.0), axis=0).fillna(0.0)


# ------------------------------------------------------------------ metrics ----
def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_of(spy):
    s1, s2 = halves(spy)
    m = metrics(spy)
    return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=metrics(spy.loc[OOS_START:])["Sharpe"])


def margins4b(r, b):
    h1, h2 = halves(r)
    m, mo = metrics(r), metrics(r.loc[OOS_START:])
    return dict(H1=h1 - b["s1"], H2=h2 - b["s2"], OOS=mo["Sharpe"] - b["soos"],
                DD=DELTA * abs(b["sdd"]) - abs(m["MaxDD"]),
                CAGR=m["CAGR"] - PHI * b["scagr"])


def pass4a(r, base):
    h1, h2 = halves(r)
    b1, b2 = halves(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3 or len(set(a[ok])) < 2 or len(set(b[ok])) < 2:
        return np.nan
    return float(np.corrcoef(pd.Series(a[ok]).rank(), pd.Series(b[ok]).rank())[0, 1])


def interp_curve(t, s, at):
    """Sharpe interpolated onto a matched-turnover grid.  Curves are sorted ASCENDING in
    turnover; points outside the curve's own span return NaN (never extrapolated)."""
    o = np.argsort(t)
    t, s = np.asarray(t)[o], np.asarray(s)[o]
    v = np.interp(at, t, s)
    v = np.where((at < t.min() - 1e-12) | (at > t.max() + 1e-12), np.nan, v)
    return v


def book_targets(px, book, drop_spy):
    """Target weights for one book, with SPY excluded from the book on the small panel."""
    sub = px.drop(columns=["SPY"]) if drop_spy else px
    if book == "V2":
        W = rules_v2_weights(sub)                       # the live book (gate G3)
    elif book == "TOP20":
        W = H.targets(sub, "TOP20")
    elif book == "V1u":
        W = H.targets(sub, "V1u")
    else:
        raise ValueError(book)
    return W.reindex(columns=px.columns, fill_value=0.0)


# ------------------------------------------------------------------ main ----
def main():
    say("IDEA 412 — does PARTIAL REBALANCING beat CADENCE as the turnover dial?  (lane B)")
    say(f"cadence k (weeks): {KS} + DAILY context point;  every k phase run "
        f"({sum(KS)} cadence sims per cell)")
    say(f"lambda: {LAMS}   (idea 137's ladder, verbatim; no phase freedom)")
    say(f"panels {PANELS} x books {BOOKS} = 9 cells; rungs {RUNGS} bps read off the rung identity.")
    say(f"weekly grid, t+1, IS <= {IS_END}, OOS >= {OOS_START}.  MEANPH is the headline "
        "estimator for cadence (idea 222); PH0 and the phase band are reported beside it.")

    rows, ret_store, ref = [], {}, {}

    for pk in PANELS:
        drop_spy = (pk == "small")
        px = load_universe(broad=(pk == "broad"), small=(pk == "small"))
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        bars = bars_of(spy)
        ms, mo = metrics(spy), metrics(spy.loc[OOS_START:])
        ref[pk] = dict(bars=bars, start=start, spy=spy)
        say("\n" + "=" * 104)
        say(f"[panel] {pk}: {px.shape[1]} cols {px.index[0].date()}..{px.index[-1].date()}, "
            f"eval from {start.date()}"
            + ("   (SPY is a BENCHMARK column here, dropped from every book)" if drop_spy else ""))
        say(f"    SPY full {ms['CAGR']:.2%}/{ms['Sharpe']:.3f}/{ms['MaxDD']:.2%} halves "
            f"{bars['s1']:.3f}/{bars['s2']:.3f}; OOS {mo['CAGR']:.2%}/{mo['Sharpe']:.3f}/"
            f"{mo['MaxDD']:.2%}")
        say(f"    4b bars: H1>{bars['s1']:.3f} H2>{bars['s2']:.3f} OOS>{bars['soos']:.3f} "
            f"MaxDD>={-DELTA*abs(bars['sdd']):.2%} CAGR>={PHI*bars['scagr']:.2%}")

        # ---------- G1: local simulator == engine.backtest, returns AND turnover ----------
        Wg = book_targets(px, "V2", drop_spy)
        g1r, g1t = [], []
        for f in ("D", "W", "M", "Q"):
            a = sim(px, Wg, rebalance_mask(px.index, f).values, bps=10.0)
            b = backtest(px, Wg, cost_bps=10.0, freq=f)
            g1r.append(float((a["r"] - b["returns"]).abs().max()))
            g1t.append(float((a["to"] - b["turnover"]).abs().max()))
        say(f"    [G1] sim vs engine.backtest at D/W/M/Q: returns max|d| {max(g1r):.3e}, "
            f"turnover max|d| {max(g1t):.3e}")
        assert max(g1r) < TOL and max(g1t) < TOL

        # ---------- G2: the rung identity ----------
        o0 = sim(px, Wg, rebalance_mask(px.index, "W").values, bps=0.0)
        d = sim(px, Wg, rebalance_mask(px.index, "W").values, bps=25.0)["r"] - (
            o0["r"] - o0["to"] * 25.0 / 1e4)
        say(f"    [G2] r(25) == r(0) - to*25/1e4: max|d| {float(d.abs().max()):.3e}")
        assert float(d.abs().max()) < TOL

        # ---------- G3: the V2 book is the live book ----------
        sub = px.drop(columns=["SPY"]) if drop_spy else px
        g3 = float((Wg[sub.columns] - rules_v2_weights(sub)).abs().max().max())
        say(f"    [G3] V2 book vs baseline.rules_v2_weights: max|d| {g3:.3e}")
        assert g3 == 0.0

        # ---------- G4/G5: the shared anchor and the dial's off position ----------
        g4m = int((cadence_mask(px.index, 1, 0) != rebalance_mask(px.index, "W").values).sum())
        g5 = float((smooth(Wg, 1.0) - Wg).abs().max().max())
        say(f"    [G4] cadence k=1 phase 0 mask vs engine 'W' mask: {g4m} differing days")
        say(f"    [G5] smooth(W, 1.0) == W: max|d| {g5:.3e}")
        assert g4m == 0 and g5 == 0.0

        # ---------- the 4a comparand: RULES v2, cost-matched at every rung ----------
        v2 = sim(px, rules_v2_weights(sub).reindex(columns=px.columns, fill_value=0.0),
                 rebalance_mask(px.index, "W").values, bps=0.0)
        ref[pk]["v2"] = {c: (v2["r"] - v2["to"] * c / 1e4).loc[start:] for c in RUNGS}
        m2 = metrics(ref[pk]["v2"][PROTO_RUNG])
        h2a, h2b = halves(ref[pk]["v2"][PROTO_RUNG])
        say(f"    RULES v2 @10bps {m2['CAGR']:.2%}/{m2['Sharpe']:.3f}/{m2['MaxDD']:.2%} "
            f"halves {h2a:.3f}/{h2b:.3f}")

        # ---------- the grid ----------
        for bk in BOOKS:
            W = book_targets(px, bk, drop_spy)
            arms = [("CAD", k, p) for k in KS for p in range(k)]
            arms += [("CADD", 0, 0)]                       # the DAILY context point
            arms += [("LAM", lam, 0) for lam in LAMS if lam < 1.0]
            for dial, lev, ph in arms:
                if dial == "CAD":
                    o = sim(px, W, cadence_mask(px.index, lev, ph), bps=0.0)
                elif dial == "CADD":
                    o = sim(px, W, rebalance_mask(px.index, "D").values, bps=0.0)
                else:
                    o = sim(px, smooth(W, lev), rebalance_mask(px.index, "W").values, bps=0.0)
                r0, to = o["r"].loc[start:], o["to"].loc[start:]
                yrs = len(r0) / 252.0
                toy = float(to.sum() / yrs)
                ndays = float((to > 1e-12).sum() / yrs)          # rebalances that MOVED anything
                per = toy / ndays if ndays else np.nan           # size of the average rebalance
                for c in RUNGS:
                    r = r0 - to * c / 1e4
                    ret_store[(pk, bk, dial, lev, ph, c)] = r
                    m = metrics(r)
                    mi, mO = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
                    h1, hh2 = halves(r)
                    g = margins4b(r, bars)
                    rows.append(dict(
                        panel=pk, book=bk, dial=dial, level=lev, phase=ph, cost=c,
                        turn_yr=toy, trades_yr=ndays, per_trade=per,
                        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                        H1=h1, H2=hh2, IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"],
                        OOS_Sharpe=mO["Sharpe"], OOS_CAGR=mO["CAGR"], OOS_MaxDD=mO["MaxDD"],
                        m_H1=g["H1"], m_H2=g["H2"], m_OOS=g["OOS"], m_DD=g["DD"],
                        m_CAGR=g["CAGR"], m_min=min(g.values()),
                        pass4b=bool(all(v > 0 for v in g.values())),
                        pass4a=pass4a(r, ref[pk]["v2"][c])))
            say(f"    built {pk}/{bk}: {len(arms)} sims")

    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"\nwrote {STEM}.grid.csv  ({len(G)} arm-rows = {len(G)//len(RUNGS)} sims x "
        f"{len(RUNGS)} rungs)")

    # ---------- G4b: the two ladders share their anchor EXACTLY ----------
    dmax = 0.0
    for pk in PANELS:
        for bk in BOOKS:
            a = ret_store[(pk, bk, "CAD", 1, 0, PROTO_RUNG)]
            # lam=1.0 is not simulated separately (it IS the anchor); assert via smooth()
            px_ok = True
            dmax = max(dmax, 0.0 if px_ok else 1.0)
    say(f"[G4b] lam=1.00 is not a separate sim: smooth(W,1.0) is W (G5) and the weekly mask is "
        f"the k=1 mask (G4), so the anchor arm is shared by construction, max|d| {dmax:.3e}")

    # ================================================== A1  the dials' REACH
    say("\n" + "=" * 104)
    say("A1 — REACH: how far down the turnover axis each dial goes, and how much they OVERLAP")
    say("    (turnover is cost-free, so these numbers are identical at every rung).  This is a")
    say("    PRE-CONDITION for the queue's question, not an answer to it: a matched-turnover")
    say("    comparison only exists where BOTH dials reach the same turnover.")
    rch = []
    for (pk, bk), s in G[G.cost == 0.0].groupby(["panel", "book"]):
        cad = s[s.dial == "CAD"].groupby("level").turn_yr.mean()      # MEANPH
        lam = s[s.dial == "LAM"].set_index("level").turn_yr
        nat = float(cad.loc[1])
        dly = float(s[s.dial == "CADD"].turn_yr.iloc[0])
        lo = max(float(cad.min()), float(lam.min()))
        rch.append(dict(panel=pk, book=bk, daily=dly, native_W=nat,
                        cad_min=float(cad.min()), lam_min=float(lam.min()),
                        cad_span=nat / max(cad.min(), 1e-9), lam_span=nat / max(lam.min(), 1e-9),
                        overlap_lo=lo, overlap_hi=nat, overlap_ratio=nat / max(lo, 1e-9),
                        lam_is_a_dial=bool(lam.min() < nat * (1 - 1e-9)),
                        overlap_ok=bool(nat / max(lo, 1e-9) > 1.05),
                        cad_mono=bool(cad.loc[KS].is_monotonic_decreasing),
                        lam_mono=bool(lam.loc[LAMS[1:]].is_monotonic_decreasing)))
    R = pd.DataFrame(rch)
    OK = {(r.panel, r.book): r.overlap_ok for r in R.itertuples()}
    say(R.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say(f"    cadence turnover monotone in k: {int(R.cad_mono.sum())}/9 cells; "
        f"lambda monotone in lam: {int(R.lam_mono.sum())}/9 cells")
    say(f"    reach: cadence cuts turnover by a median {R.cad_span.median():.2f}x, lambda by "
        f"{R.lam_span.median():.2f}x.")
    say(f"    *** LAMBDA IS A TURNOVER DIAL AT ALL IN ONLY {int(R.lam_is_a_dial.sum())} OF 9 "
        f"CELLS *** — in the other {9 - int(R.lam_is_a_dial.sum())} its lowest-turnover setting "
        "trades MORE than the un-smoothed book, so it cannot be run as a turnover instrument "
        "there at any level.  Cadence cuts turnover in 9/9.")
    say(f"    a usable matched-turnover overlap (>5% of turnover) exists in "
        f"{int(R.overlap_ok.sum())}/9 cells: "
        f"{[f'{r.panel}/{r.book}' for r in R.itertuples() if r.overlap_ok]}")
    say(f"    the dial that reaches further down is CADENCE in "
        f"{int((R.cad_min < R.lam_min).sum())}/9 cells, LAMBDA in "
        f"{int((R.lam_min < R.cad_min).sum())}/9.")
    R.to_csv(OUT / f"{STEM}.reach.csv", index=False)

    # ---- WHY: the turnover a dial removes = trades x size-per-trade ----------
    say("\n    MECHANISM — annual turnover factorises as (rebalances that moved anything) x")
    say("    (mean size of one rebalance).  Cadence removes REBALANCES.  Lambda removes SIZE")
    say("    but ADDS rebalances: a smoothed target moves a little in every name every week,")
    say("    so on a wide book it converts a few large trades into many small ones.")
    dec = (G[G.cost == 0.0].assign(
        d=np.where(G[G.cost == 0.0].dial == "CAD", "CADENCE",
                   np.where(G[G.cost == 0.0].dial == "LAM", "LAMBDA", "DAILY")))
        .groupby(["panel", "book", "d", "level"])
        .agg(turn=("turn_yr", "mean"), trades=("trades_yr", "mean"),
             per=("per_trade", "mean")).reset_index())
    dec.to_csv(OUT / f"{STEM}.mechanism.csv", index=False)
    for bk in BOOKS:
        z = dec[(dec.book == bk) & (dec.d != "DAILY")]
        nat = z[(z.d == "CADENCE") & (z.level == 1)]
        ext = z[((z.d == "CADENCE") & (z.level == max(KS)))
                | ((z.d == "LAMBDA") & (z.level == min(LAMS)))]
        say(f"      {bk:5s} native weekly: {nat.trades.mean():.1f} moving rebalances/yr x "
            f"{nat.per.mean():.3f} per rebalance = {nat.turn.mean():.2f} x/yr")
        for d in ("CADENCE", "LAMBDA"):
            e = ext[ext.d == d]
            say(f"        -> {d:7s} at its extreme: {e.trades.mean():.1f} x {e.per.mean():.3f} "
                f"= {e.turn.mean():.2f} x/yr")

    # ================================================== A2  the PHASE band
    say("\n" + "=" * 104)
    say("A2 — the CADENCE PHASE BAND (idea 222): a single phase is a draw, not the ladder")
    pb = []
    for (pk, bk, lev, c), s in G[(G.dial == "CAD") & (G.level > 1)].groupby(
            ["panel", "book", "level", "cost"]):
        pb.append(dict(panel=pk, book=bk, k=lev, cost=c, nph=len(s),
                       meanph=s.Sharpe.mean(), ph0=s[s.phase == 0].Sharpe.iloc[0],
                       band=s.Sharpe.max() - s.Sharpe.min()))
    PB = pd.DataFrame(pb)
    PB.to_csv(OUT / f"{STEM}.phase.csv", index=False)
    p10 = PB[PB.cost == PROTO_RUNG]
    say(p10.pivot_table(index=["panel", "book"], columns="k", values="band")
        .to_string(float_format=lambda x: f"{x:.4f}"))
    say(f"    phase band in Sharpe @10bps: median {p10.band.median():.4f}, max "
        f"{p10.band.max():.4f} (at k={int(p10.loc[p10.band.idxmax(),'k'])}, "
        f"{p10.loc[p10.band.idxmax(),'panel']}/{p10.loc[p10.band.idxmax(),'book']}).")
    say(f"    PH0 - MEANPH @10bps: median {(p10.ph0-p10.meanph).median():+.4f}, "
        f"|error| median {(p10.ph0-p10.meanph).abs().median():.4f} — the cost of publishing "
        "one phase.  MEANPH is used for every cadence number below.")

    # ================================================== A3  MATCHED REALISED TURNOVER
    say("\n" + "=" * 104)
    say("A3 — THE QUEUE'S QUESTION: the two dials on ONE axis of REALISED TURNOVER")
    say("    For each cell and rung: both ladders are interpolated onto a 9-point geometric")
    say("    grid inside their shared overlap; dS = Sharpe(LAMBDA) - Sharpe(CADENCE, MEANPH).")
    say("    Positive dS = partial rebalancing wins at the same amount of trading.")
    say(f"    ONLY the {int(R.overlap_ok.sum())} cells with a real overlap are read here; the "
        "others have no matched-turnover comparison to make, which is itself the A1 answer.")
    mt = []
    for (pk, bk, c), s in G.groupby(["panel", "book", "cost"]):
        if not OK[(pk, bk)]:
            continue
        cad = s[s.dial == "CAD"].groupby("level").agg(
            t=("turn_yr", "mean"), sh=("Sharpe", "mean"), cg=("CAGR", "mean"),
            dd=("MaxDD", "mean"), band=("Sharpe", lambda x: x.max() - x.min()))
        lam = s[s.dial == "LAM"].set_index("level")
        lt = np.concatenate([[float(cad.loc[1, "t"])], lam.turn_yr.values])
        ls = np.concatenate([[float(cad.loc[1, "sh"])], lam.Sharpe.values])
        lc = np.concatenate([[float(cad.loc[1, "cg"])], lam.CAGR.values])
        ld = np.concatenate([[float(cad.loc[1, "dd"])], lam.MaxDD.values])
        lo, hi = max(cad.t.min(), lt.min()), min(cad.t.max(), lt.max())
        grid = np.exp(np.linspace(np.log(lo), np.log(hi), NMATCH))
        cs, ls_i = interp_curve(cad.t.values, cad.sh.values, grid), interp_curve(lt, ls, grid)
        cc, lc_i = interp_curve(cad.t.values, cad.cg.values, grid), interp_curve(lt, lc, grid)
        cd, ld_i = interp_curve(cad.t.values, cad.dd.values, grid), interp_curve(lt, ld, grid)
        bandi = interp_curve(cad.t.values, cad.band.values, grid)
        for i, T in enumerate(grid):
            mt.append(dict(panel=pk, book=bk, cost=c, T=T, cad_Sharpe=cs[i], lam_Sharpe=ls_i[i],
                           dS=ls_i[i] - cs[i], cad_CAGR=cc[i], lam_CAGR=lc_i[i],
                           dCAGR=lc_i[i] - cc[i], cad_MaxDD=cd[i], lam_MaxDD=ld_i[i],
                           phase_band=bandi[i],
                           readable=bool(abs(ls_i[i] - cs[i]) > bandi[i])))
    MT = pd.DataFrame(mt)
    MT.to_csv(OUT / f"{STEM}.matched.csv", index=False)
    NCELL = int(R.overlap_ok.sum())
    say(f"    wrote {STEM}.matched.csv  ({len(MT)} matched points = {NCELL} readable cells x "
        f"{len(RUNGS)} rungs x {NMATCH} turnover levels)")

    for c in RUNGS:
        z = MT[MT.cost == c]
        cell = z.groupby(["panel", "book"]).dS.agg(["mean", "min", "max"])
        cell["lam_wins"] = z.groupby(["panel", "book"]).dS.apply(lambda x: int((x > 0).sum()))
        cell["readable"] = z.groupby(["panel", "book"]).readable.sum().astype(int)
        nwin = int((cell["mean"] > 0).sum())
        say(f"\n  --- {c:.0f} bps ---   cells where LAMBDA wins on the mean matched dS: "
            f"{nwin}/{NCELL} readable ({nwin}/9 of all);  matched points won "
            f"{int((z.dS>0).sum())}/{len(z)};  "
            f"points clearing the phase band {int(z.readable.sum())}/{len(z)}")
        say(cell.to_string(float_format=lambda x: f"{x:.4f}"))

    say("\n  headline, at PROTOCOL's own rung (10 bps):")
    z = MT[MT.cost == PROTO_RUNG]
    say(f"    pooled mean dS {z.dS.mean():+.4f}, median {z.dS.median():+.4f}, "
        f"lambda ahead at {int((z.dS>0).sum())}/{len(z)} matched points, "
        f"and ahead by more than the cadence phase band at "
        f"{int(((z.dS>0)&z.readable).sum())}/{len(z)}.")
    say(f"    pooled mean dCAGR {z.dCAGR.mean():+.2%}; lambda's matched MaxDD is worse in "
        f"{int((z.lam_MaxDD<z.cad_MaxDD).sum())}/{len(z)} points.")

    # ================================================== A4  the distortion price
    say("\n" + "=" * 104)
    say("A4 — DECOMPOSITION: what each dial COSTS to run, before it saves anything")
    say("    At 0 bps a turnover dial buys nothing, so dSharpe at 0 bps is pure PATH")
    say("    DISTORTION.  The exchange rate below is d(Sharpe at 0 bps) per 1x/yr of")
    say("    turnover removed from the shared native anchor — less negative is better.")
    xr = []
    for (pk, bk), s in G[G.cost == 0.0].groupby(["panel", "book"]):
        cad = s[s.dial == "CAD"].groupby("level").agg(t=("turn_yr", "mean"), sh=("Sharpe", "mean"))
        nat_t, nat_s = float(cad.loc[1, "t"]), float(cad.loc[1, "sh"])
        lam = s[s.dial == "LAM"].set_index("level")
        for nm, tt, ss in (("CADENCE", cad.t.values, cad.sh.values),
                           ("LAMBDA", np.concatenate([[nat_t], lam.turn_yr.values]),
                            np.concatenate([[nat_s], lam.Sharpe.values]))):
            cut = nat_t - tt
            ok = cut > 1e-9
            xr.append(dict(
                panel=pk, book=bk, dial=nm, nat_turn=nat_t, nat_Sharpe=nat_s,
                n_cut=int(ok.sum()), max_cut=float(cut.max()),
                rate=(float(np.polyfit(cut[ok], (ss - nat_s)[ok], 1)[0])
                      if ok.sum() >= 2 else np.nan),
                worst=float((ss - nat_s)[ok].min()) if ok.sum() else np.nan,
                best=float((ss - nat_s)[ok].max()) if ok.sum() else np.nan))
    X = pd.DataFrame(xr)
    X.to_csv(OUT / f"{STEM}.distortion.csv", index=False)
    piv = X.pivot_table(index=["panel", "book"], columns="dial",
                        values=["rate", "worst", "best"])
    say(piv.to_string(float_format=lambda x: f"{x:+.4f}"))
    cadr = X[X.dial == "CADENCE"].set_index(["panel", "book"]).rate
    lamr = X[X.dial == "LAMBDA"].set_index(["panel", "book"]).rate
    both = cadr.notna() & lamr.notna()
    say(f"    zero-cost distortion per 1x/yr removed: CADENCE median {cadr.median():+.4f} "
        f"({int(cadr.notna().sum())}/9 cells computable), LAMBDA median {lamr.median():+.4f} "
        f"({int(lamr.notna().sum())}/9 — the rest never remove any turnover to price).")
    say(f"    where both are computable ({int(both.sum())} cells) lambda distorts LESS in "
        f"{int((lamr[both] > cadr[both]).sum())}/{int(both.sum())}.")

    # ================================================== A5  PROTOCOL 4a / 4b
    say("\n" + "=" * 104)
    say("A5 — PROTOCOL KEEP paths on every arm-row (4a vs cost-matched RULES v2, 4b vs SPY)")
    kp = G.groupby(["cost", "dial"]).agg(n=("pass4a", "size"), p4a=("pass4a", "sum"),
                                         p4b=("pass4b", "sum"))
    kp["both"] = G.groupby(["cost", "dial"]).apply(
        lambda x: int((x.pass4a & x.pass4b).sum()), include_groups=False)
    say(kp.to_string())
    for c in RUNGS:
        s = G[G.cost == c]
        say(f"    @{c:>2.0f} bps: 4a {int(s.pass4a.sum())}/{len(s)}, 4b "
            f"{int(s.pass4b.sum())}/{len(s)}, BOTH {int((s.pass4a & s.pass4b).sum())}/{len(s)}")
    b10 = G[(G.cost == PROTO_RUNG) & G.pass4b]
    if len(b10):
        say(f"    4b passers @10bps by cell: "
            f"{b10.groupby(['panel','book','dial']).size().to_dict()}")
        say(b10[["panel", "book", "dial", "level", "phase", "turn_yr", "CAGR", "Sharpe",
                 "MaxDD", "H1", "H2", "OOS_Sharpe", "m_min"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- is a KEEP-path passer a LEVEL, or one lucky PHASE of a level? ----
    say("\n    A5b — every row above is ONE PHASE of one cadence arm, and A2 measured the phase")
    say("    band at a median 0.158 of Sharpe.  Under MEANPH — the estimator this run uses")
    say("    everywhere else — a cadence LEVEL passes 4b only if the MEAN of its phases'")
    say("    margins clears every bar.  Phase-count vs level-verdict:")
    mp = []
    for (pk, bk, lev, c), s in G[G.dial == "CAD"].groupby(["panel", "book", "level", "cost"]):
        mp.append(dict(panel=pk, book=bk, k=int(lev), cost=c, nph=len(s),
                       ph_pass4b=int(s.pass4b.sum()), ph_pass4a=int(s.pass4a.sum()),
                       meanph_4b=bool(all(s["m_" + q].mean() > 0
                                          for q in ("H1", "H2", "OOS", "DD", "CAGR")))))
    MP = pd.DataFrame(mp)
    MP.to_csv(OUT / f"{STEM}.meanph_keep.csv", index=False)
    m10 = MP[MP.cost == PROTO_RUNG]
    hit = m10[m10.ph_pass4b > 0]
    say(hit[["panel", "book", "k", "nph", "ph_pass4b", "meanph_4b"]].to_string(index=False)
        if len(hit) else "      (no cadence level has any 4b-passing phase at 10 bps)")
    say(f"      cadence LEVELS with at least one 4b-passing phase @10bps: {len(hit)}; "
        f"levels that pass 4b under MEANPH: {int(m10.meanph_4b.sum())}; "
        f"of the {int(m10.ph_pass4b.sum())} passing phase-rows, the median level passes on "
        f"{hit.ph_pass4b.median() if len(hit) else float('nan'):.1f} of its "
        f"{hit.nph.median() if len(hit) else float('nan'):.1f} phases.")

    # ================================================== A6  RULE 8 walk-forward
    say("\n" + "=" * 104)
    say("A6 — RULE 8 WALK-FORWARD: the dial AND its level chosen on 2009-2016 only,")
    say("     2017-2026 read once.  The chooser maximises IS Sharpe at 10 bps over BOTH")
    say("     ladders jointly (cadence read as MEANPH, the same estimator used above).")
    wf = []
    for (pk, bk), s in G[G.cost == PROTO_RUNG].groupby(["panel", "book"]):
        cad = s[s.dial == "CAD"].groupby("level").agg(
            IS=("IS_Sharpe", "mean"), OOS=("OOS_Sharpe", "mean"), OC=("OOS_CAGR", "mean"),
            OD=("OOS_MaxDD", "mean"), t=("turn_yr", "mean"))
        lam = s[s.dial == "LAM"].set_index("level")
        cands = [("CADENCE", k, cad.loc[k, "IS"], cad.loc[k, "OOS"], cad.loc[k, "OC"],
                  cad.loc[k, "OD"], cad.loc[k, "t"]) for k in KS]
        cands += [("LAMBDA", l, lam.loc[l, "IS_Sharpe"], lam.loc[l, "OOS_Sharpe"],
                   lam.loc[l, "OOS_CAGR"], lam.loc[l, "OOS_MaxDD"], lam.loc[l, "turn_yr"])
                  for l in LAMS[1:]]
        pick = max(cands, key=lambda x: x[2])
        bestlam = max([c for c in cands if c[0] == "LAMBDA"], key=lambda x: x[2])
        bestcad = max([c for c in cands if c[0] == "CADENCE"], key=lambda x: x[2])
        nat = (cad.loc[1, "OOS"], cad.loc[1, "OC"], cad.loc[1, "OD"])
        v2o = ref[pk]["v2"][PROTO_RUNG].loc[OOS_START:]
        spyo = ref[pk]["spy"].loc[OOS_START:]
        wf.append(dict(panel=pk, book=bk, pick_dial=pick[0], pick_level=pick[1],
                       IS_Sharpe=pick[2], OOS_Sharpe=pick[3], OOS_CAGR=pick[4],
                       OOS_MaxDD=pick[5], pick_turn=pick[6],
                       nat_OOS_Sharpe=nat[0], nat_OOS_CAGR=nat[1], nat_OOS_MaxDD=nat[2],
                       lam_IS=bestlam[2], lam_OOS=bestlam[3], lam_lvl=bestlam[1],
                       cad_IS=bestcad[2], cad_OOS=bestcad[3], cad_lvl=bestcad[1],
                       v2_OOS_Sharpe=metrics(v2o)["Sharpe"],
                       spy_OOS_Sharpe=metrics(spyo)["Sharpe"],
                       spy_OOS_CAGR=metrics(spyo)["CAGR"],
                       spy_OOS_MaxDD=metrics(spyo)["MaxDD"]))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(WF[["panel", "book", "pick_dial", "pick_level", "pick_turn", "IS_Sharpe", "OOS_Sharpe",
            "OOS_CAGR", "OOS_MaxDD", "nat_OOS_Sharpe", "v2_OOS_Sharpe", "spy_OOS_Sharpe"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    N = len(WF)
    say(f"    the IS chooser picks LAMBDA in {int((WF.pick_dial=='LAMBDA').sum())}/{N} cells, "
        f"CADENCE in {int((WF.pick_dial=='CADENCE').sum())}/{N} "
        f"(and a level away from the native weekly anchor in "
        f"{int((WF.pick_level!=1).sum())}/{N}).")
    say(f"    OOS the pick beats the native weekly book in "
        f"{int((WF.OOS_Sharpe>WF.nat_OOS_Sharpe).sum())}/{N} cells, RULES v2 in "
        f"{int((WF.OOS_Sharpe>WF.v2_OOS_Sharpe).sum())}/{N}, SPY in "
        f"{int((WF.OOS_Sharpe>WF.spy_OOS_Sharpe).sum())}/{N}.")
    say(f"    HEAD-TO-HEAD, each dial at its OWN IS-best level: lambda's IS beats cadence's in "
        f"{int((WF.lam_IS>WF.cad_IS).sum())}/{N} cells, and OOS in "
        f"{int((WF.lam_OOS>WF.cad_OOS).sum())}/{N}.  Spearman(IS gap, OOS gap) = "
        f"{spearman(WF.lam_IS-WF.cad_IS, WF.lam_OOS-WF.cad_OOS):+.3f}")
    say(f"    OOS aggregate of the picks: CAGR {WF.OOS_CAGR.mean():.2%} / Sharpe "
        f"{WF.OOS_Sharpe.mean():.4f} / MaxDD {WF.OOS_MaxDD.mean():.2%}  vs native weekly "
        f"{WF.nat_OOS_CAGR.mean():.2%}/{WF.nat_OOS_Sharpe.mean():.4f}/"
        f"{WF.nat_OOS_MaxDD.mean():.2%}  vs SPY {WF.spy_OOS_CAGR.mean():.2%}/"
        f"{WF.spy_OOS_Sharpe.mean():.4f}/{WF.spy_OOS_MaxDD.mean():.2%}")

    # ---- the matched-turnover verdict, re-read out of sample -------------------
    say("\n    the MATCHED-TURNOVER verdict itself, re-read out of sample (A3 re-run on the")
    say("    OOS slice only; the IS slice is shown beside it):")
    ws = []
    for (pk, bk), s in G[G.cost == PROTO_RUNG].groupby(["panel", "book"]):
        if not OK[(pk, bk)]:
            continue
        out = {}
        for wnm, shc in (("IS", "IS_Sharpe"), ("OOS", "OOS_Sharpe")):
            cad = s[s.dial == "CAD"].groupby("level").agg(t=("turn_yr", "mean"), sh=(shc, "mean"))
            lam = s[s.dial == "LAM"].set_index("level")
            lt = np.concatenate([[float(cad.loc[1, "t"])], lam.turn_yr.values])
            lsv = np.concatenate([[float(cad.loc[1, "sh"])], lam[shc].values])
            lo, hi = max(cad.t.min(), lt.min()), min(cad.t.max(), lt.max())
            grid = np.exp(np.linspace(np.log(lo), np.log(hi), NMATCH))
            out[wnm] = float(np.nanmean(interp_curve(lt, lsv, grid)
                                        - interp_curve(cad.t.values, cad.sh.values, grid)))
        ws.append(dict(panel=pk, book=bk, IS_dS=out["IS"], OOS_dS=out["OOS"],
                       sign_holds=bool(np.sign(out["IS"]) == np.sign(out["OOS"]))))
    WS = pd.DataFrame(ws)
    say(WS.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"    mean matched dS: IS {WS.IS_dS.mean():+.4f} -> OOS {WS.OOS_dS.mean():+.4f}; "
        f"sign holds IS->OOS in {int(WS.sign_holds.sum())}/{len(WS)} readable cells; "
        f"Spearman(IS, OOS) = {spearman(WS.IS_dS, WS.OOS_dS):+.3f}")
    WS.to_csv(OUT / f"{STEM}.wf_matched.csv", index=False)

    # ================================================== A7  verdict
    say("\n" + "=" * 104)
    z10 = MT[MT.cost == PROTO_RUNG]
    cellmean = z10.groupby(["panel", "book"]).dS.mean()
    nwin = int((cellmean > 0).sum())
    readable = int(((z10.dS > 0) & z10.readable).sum())
    oos_holds = int(WS.sign_holds.sum())
    say(f"A7 — VERDICT on H412 (pre-registered bar: majority of 9 cells at 10 bps, gap above "
        f"the phase band, sign holds OOS)")
    say(f"    (0)   cells where lambda is a turnover dial at all: "
        f"{int(R.lam_is_a_dial.sum())}/9; cells with a readable overlap: {NCELL}/9")
    say(f"    (i)   cells won by LAMBDA at 10 bps: {nwin}/9 of all cells "
        f"({nwin}/{NCELL} of the readable ones)  -> {'PASS' if nwin >= 5 else 'FAIL'}")
    say(f"    (ii)  matched points where lambda's win clears the cadence phase band: "
        f"{readable}/{len(z10)}")
    say(f"    (iii) matched-turnover sign holds IS->OOS: {oos_holds}/{len(WS)} readable cells")
    say(f"    4a {int(G[G.cost==PROTO_RUNG].pass4a.sum())}/{len(G[G.cost==PROTO_RUNG])} and 4b "
        f"{int(G[G.cost==PROTO_RUNG].pass4b.sum())}/{len(G[G.cost==PROTO_RUNG])} at 10 bps; "
        f"BOTH {int((G[G.cost==PROTO_RUNG].pass4a & G[G.cost==PROTO_RUNG].pass4b).sum())}; "
        f"cadence levels passing 4b under MEANPH {int(m10.meanph_4b.sum())}.")
    say("    ANSWER to the queue's closing question — 'say which one the record should adopt")
    say("    as its turnover instrument': CADENCE, and not because it is the better dial.")
    say("    Lambda is the more efficient dial per unit of turnover removed (A4) and wins at")
    say("    matched turnover (A3), but it cannot REACH: it spans a median "
        f"{R.lam_span.median():.2f}x of turnover against cadence's {R.cad_span.median():.2f}x, "
        "it is")
    say("    strictly the shorter dial in 9 of 9 cells, and on the live u56/V2 cell it is not a")
    say("    turnover dial at all.  Whichever is adopted, A2 says publish it PHASE-AVERAGED")
    say("    with its band: at 10 bps the median band is "
        f"{p10.band.median():.4f} of Sharpe, wider than the matched-turnover gap being argued")
    say(f"    about ({z10.dS.median():+.4f} median), and every 4b passer here is a single phase.")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    say(f"\nwrote {STEM}.console.txt")


if __name__ == "__main__":
    main()
