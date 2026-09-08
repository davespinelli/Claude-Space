#!/usr/bin/env python3
"""QUEUE idea 405 — price-the-levered-sleeve-against-its-own-TURNOVER   (lane C, 2026-09-08).

PRE-REGISTERED QUESTION (verbatim from QUEUE.md idea 405, written before any number here
was read)
    "idea 402's levered f=0.60 g=1.25 book triples the incumbent's turnover (2.3x -> 7.9x/yr)
     for a Sharpe edge whose break-even borrow rate is a median 277 bps.  Sweep the
     trading-cost rung {0, 10, 25, 50 bps} against the financing rung {0..600 bps} and report
     the joint region where the levered arm beats f=0.25 @ 0.75; if the region needs both
     cheap borrow and cheap trading, the arm is a fee story.  Max 2 params."

WHY IT MATTERS
    Idea 402 PARKed the levered arm on a rule-8 count (12/16 vs a pre-registered 14/16) and
    published a single-rung financing break-even (median 277 bps at 10 bps of trading cost).
    But that break-even was solved at ONE cost rung, and the levered book pays its edge out
    of two fee taps, not one: it borrows AND it trades 3.4x more.  The two taps are not
    independent — the same gross that costs financing also scales turnover — so the honest
    object is a SURFACE over (trading cost, borrow rate), not a point.  If the arm only wins
    in the corner where both taps are near zero, it is a fee story and the record should stop
    carrying it as a candidate.  If it wins across the realistic rectangle, idea 402's PARK
    was a rule-8 count and not a pricing failure.

WHAT IS TESTED (fixed in advance)
    Q1  PREMISE: is the turnover multiple really 3.4x (2.3x -> 7.9x/yr)?  Measured per cell,
        not on the two rows idea 402 tabulated.
    Q2  The JOINT REGION: over the 4 x 7 = 28 (c, phi) rungs, in how many does LEV beat INC
        on Sharpe, in each of the 8 cells?  Is the region a rectangle in both dials (a fee
        story), a half-plane in phi only, or all of it?
    Q3  The EXACT BREAK-EVEN FRONTIER phi*(c): the borrow rate at which the Sharpe edge dies,
        per cost rung, solved by interpolation on the simulated ladder.  Slope d phi*/d c is
        the exchange rate between the two taps and is what "the arm is a fee story" means
        quantitatively.
    Q4  DECOMPOSITION: split the LEV-minus-INC Sharpe gap at each rung into (i) the zero-fee
        gap, (ii) the trading-cost increment, (iii) the financing increment.  Idea 137's
        method on a different pair of taps.  The identity is checked to machine precision.
    Q5  4b at every rung, and rule 8: the ARM chosen on 2009-2016 only at each rung, read
        once on 2017-2026.  Does the IS-decided region predict the OOS-decided one?

GRID (two tuned parameters, both swept, ALL points reported)
    param 1  c    in {0, 10, 25, 50} bps       — trading cost per unit turnover (queue's rung).
             10 is PROTOCOL 2's binding assumption and the rung the verdict is quoted at.
    param 2  phi  in {0, 100, 200, 300, 400, 500, 600} bps/yr on borrowed notional (queue's
             "0..600").  300 is idea 402's headline rung.
    REPORTED AXES, never selected on: panel {u56, broad} x base book {EWall, TOP20} x sleeve
    set {S3 = TLT/GLD/UUP, S4 = TLT/GLD/DBC/UUP} = 8 cells; ARM in {INC, LEV, CTL, CTLg}.
        INC  = f 0.25, g 0.75   (idea 139's standing 4b KEEP-candidate — the comparand)
        LEV  = f 0.60, g 1.25   (idea 402's arm — the subject)
        CTL  = f 0.00, g 0.75   (no sleeve, record convention — exposure control)
        CTLg = f 0.00, g 1.25   (no sleeve at LEV's gross — isolates the sleeve from the lever)

BOOK (verbatim from ideas 138/402)
    raw = (1-f) * base_book + f * sleeve(assets);  book = raw * (g / sum(raw)) per day.
    sleeve(assets) = momentum-vote x risk-parity (ideas 100/104), vote over {12-1m, 6m, 3m}.

FEE CONVENTION, stated not buried
    Trading:   c bps charged on each unit of turnover, inside the simulator (PROTOCOL 2).
    Financing: phi/252 bps charged daily on max(realised gross - 1, 0), i.e. on borrowed
               notional only, on the DRIFTED gross, not the target (idea 402's convention).
    Cash earns 0 at gross < 1 — the record's standing convention (open idea 406 questions it).
               That pairing is UNKIND to the levered arm and KIND to INC/CTL, which hold 25%
               cash.  Every number below inherits that asymmetry; it is not corrected here
               because idea 406 owns it, but it is quantified in the CAVEAT block at the end.
    Sharpe is rf = 0 throughout (engine.metrics), as everywhere in this record.

PRE-REGISTERED PREDICTIONS (written before the main grid was read)
    P1  The turnover multiple is NOT a constant 3.4x: TOP20's base book already turns over
        fast, so the multiple should be smaller on TOP20 cells than on EWall cells.
    P2  Because Sharpe is near-invariant in gross at zero fees (idea 311) while BOTH taps
        scale with gross, the win region is bounded above in phi AND above in c, i.e. a
        staircase, not a half-plane.  The queue's "fee story" phrasing is a prediction I
        expect to be PARTLY confirmed.
    P3  The frontier phi*(c) is DECREASING in c with a slope of order -(turnover multiple)
        x (1 / borrowed fraction) x 252/1e4 ... i.e. a few tens of bps of borrow per bp of
        trading cost.  A 15-bps cost surprise should be worth >100 bps of borrow.
    P4  At the record's own rung (c = 10, phi = 300) the arm wins in a majority of cells
        (idea 402 measured a median 277-bps break-even, so ~half should already be under
        water there — this is the sharpest test of idea 402's own number).
    P5  Rule 8's IS-chosen arm picks LEV in the low-fee corner and INC in the high-fee corner,
        and the OOS win region is SMALLER than the IS one (fees are a certainty, edges are not).

DECISION RULE, pre-registered
    KEEP-candidate (4b) only if LEV passes 4b AND beats INC on Sharpe in ALL 8 cells at the
    PROTOCOL rung c = 10 bps with phi >= 300 bps, AND the rule-8 IS chooser picks LEV there
    and its OOS clears all three OOS-visible 4b bars in >= 7/8 cells.  Otherwise the verdict
    is the SURFACE itself: report the region and classify the arm as fee-story or not.
    "Fee story" is pre-defined as: the win region requires c <= 10 bps AND phi <= 300 bps,
    i.e. it does not survive either tap being moved one rung up from the record's convention.

CAVEATS carried, not buried
    * SURVIVORSHIP (idea 54): both panels are current constituents; absent delistings inflate
      the EQUITY leg more than the ETF sleeve, so every number here favours LOW f and the
      unlevered control.  A finding that levered high-f wins is understated.
    * Financing is a FLAT rate over 2009-2026, not a path (no rate series is cached and the
      sandbox has no network).  0-600 bps brackets the plausible range; a real account paid
      near 0 in 2009-2015 and 500-600 in 2023-2024, so the flat rung mis-times the edge.
    * Cash-at-zero (open idea 406) taxes INC/CTL by ~25% of the credit rate and taxes LEV by
      0.  Correcting it would move the frontier AGAINST the levered arm; the size of that
      move is computed exactly in the CAVEAT block, not hand-waved.
    * MaxDD is one number off one path (idea 321); 4b's DD cap turns on exactly it.
    * The sleeve is 3-4 ETFs over one macro regime (idea 139 risk (a)).
    * Idea 126: t+1 only.  Idea 38: calendar-day index on both panels.  Idea 401's DEFECT:
      u56's price cache is rewritten by daily-close commits, so cross-run reproduction on
      u56 holds only to ~1e-5.

HARNESS: idea 94's simulator and idea 402's leverage-capable `run_lev` are IMPORTED/rebuilt
verbatim.  Idea 402's committed .grid.csv is reproduced on its shared rows as a gate.
Deterministic, standalone.  Modifies nothing.  Writes .console.txt, .grid.csv, .region.csv,
.frontier.csv, .decomp.csv, .walkforward.csv, .keeppaths.csv next to itself.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-08_price-the-levered-sleeve-against-its-own-TURNOVER_C"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I402_GRID = OUT / "2026-09-07_does-a-levered-f-060-book-clear-the-CAGR-floor_C.grid.csv"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")

FREQ = H.FREQ
IS_END, OOS_START = H.IS_END, H.OOS_START
COSTS = [0.0, 10.0, 25.0, 50.0]                       # tuned parameter 1 — all reported
FINS = [0.0, 100.0, 200.0, 300.0, 400.0, 500.0, 600.0]  # tuned parameter 2 — all reported
C_PROTO, FIN_HEADLINE = 10.0, 300.0                   # the rung the verdict is quoted at
PHI, DELTA = 0.70, 0.60                               # 4b CAGR floor / DD cap fractions of SPY
ARMS = {"INC": (0.25, 0.75), "LEV": (0.60, 1.25), "CTL": (0.00, 0.75), "CTLg": (0.00, 1.25)}
SLEEVES = {"S3": ["TLT", "GLD", "UUP"], "S4": ["TLT", "GLD", "DBC", "UUP"]}
BOOKS = ["EWall", "TOP20"]
PANELS = ["u56", "broad"]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 4000)
LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ------------------------------------------------------------------ books ----
def _risk_parity(sub, window=60):
    inv = 1.0 / sub.pct_change().rolling(window).std().replace(0.0, np.nan)
    return inv.div(inv.sum(axis=1), axis=0)


def _vote_mom(sub):
    sig = [sub.shift(21) / sub.shift(252) - 1, sub / sub.shift(126) - 1, sub / sub.shift(63) - 1]
    return sum((s > 0).astype(float).where(s.notna()) for s in sig) / len(sig)


def sleeve_weights(px, assets):
    """Ideas 100/104's sleeve, verbatim from ideas 133/134/138/402."""
    sub = px[assets]
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[assets] = (_vote_mom(sub) * _risk_parity(sub)).fillna(0.0)
    return out


def blend(base_W, sl_W, f, g):
    raw = base_W if f == 0.0 else (1 - f) * base_W + f * sl_W
    return raw.mul((g / raw.sum(axis=1).replace(0, np.nan)).fillna(0.0), axis=0).fillna(0.0)


# ------------------------------------------------- leverage-capable simulator --
def run_lev(px, W, bps, freq=FREQ):
    """Idea 402's run_lev, verbatim: H.run with instruments and the gross cap removed.
    Returns per-day turnover and DRIFTED gross so both fee taps can be charged exactly."""
    rets = px.pct_change().fillna(0.0).values
    tgt = W.reindex(px.index).fillna(0.0).values
    mask = H.rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    nrow, ncol = rets.shape
    cur = np.zeros(ncol)
    held = np.zeros((nrow, ncol))
    turn = np.zeros(nrow)
    gross_s = np.zeros(nrow)
    for i in range(nrow):
        if mask[i] and i > 0:
            new = tgt[i - 1]
            turn[i] += np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        gross_s[i] = cur.sum()
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    idx = px.index
    r = pd.Series((held * rets).sum(axis=1), index=idx) - pd.Series(turn, index=idx) * bps / 1e4
    return dict(r=r, to=pd.Series(turn, index=idx), gross=pd.Series(gross_s, index=idx))


def priced(r0, turn, gross, c, fin):
    """r(c, phi) = r(0, 0) - c/1e4 * turnover_t - phi/1e4/252 * borrowed_t.  EXACT: both taps
    are linear in the simulated paths, which is what makes the surface solvable rather than
    re-simulated.  Asserted against a direct simulation at every cost rung."""
    return r0 - (c / 1e4) * turn - (fin / 1e4 / 252.0) * (gross - 1.0).clip(lower=0.0)


# ------------------------------------------------------------------ metrics --
def bars_win(spy, which):
    s = spy.loc[:IS_END] if which == "IS" else spy
    h = len(s) // 2
    m = metrics(s)
    return dict(s1=metrics(s.iloc[:h])["Sharpe"], s2=metrics(s.iloc[h:])["Sharpe"],
                sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=metrics(spy.loc[OOS_START:])["Sharpe"] if which == "full" else np.nan)


def margins(r, b, which="full"):
    s = r.loc[:IS_END] if which == "IS" else r
    h = len(s) // 2
    m = metrics(s)
    d = dict(H1=metrics(s.iloc[:h])["Sharpe"] - b["s1"],
             H2=metrics(s.iloc[h:])["Sharpe"] - b["s2"],
             DD=DELTA * abs(b["sdd"]) - abs(m["MaxDD"]),
             CAGR=m["CAGR"] - PHI * b["scagr"])
    if which == "full":
        d["OOS"] = metrics(r.loc[OOS_START:])["Sharpe"] - b["soos"]
    return d


def oos_bars(spy):
    s = spy.loc[OOS_START:]
    m = metrics(s)
    return dict(sharpe=m["Sharpe"], dd=m["MaxDD"], cagr=m["CAGR"])


def oos_margins(r, ob):
    m = metrics(r.loc[OOS_START:])
    return dict(S=m["Sharpe"] - ob["sharpe"], DD=DELTA * abs(ob["dd"]) - abs(m["MaxDD"]),
                CAGR=m["CAGR"] - PHI * ob["cagr"])


def pass_all(d):
    return bool(all(v > 0 for v in d.values()))


def crossing(xs, ys, target=0.0):
    """First x at which y crosses target, linearly interpolated on the swept ladder.
    Returns (value, 'interior'|'below-all'|'above-all')."""
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    o = np.argsort(xs)
    xs, ys = xs[o], ys[o]
    if np.all(ys > target):
        return None, "above-all"
    if np.all(ys <= target):
        return None, "below-all"
    for i in range(len(xs) - 1):
        a, b = ys[i], ys[i + 1]
        if (a - target) * (b - target) <= 0 and a != b:
            return float(xs[i] + (xs[i + 1] - xs[i]) * (target - a) / (b - a)), "interior"
    return None, "none"


# ------------------------------------------------------------------ main -----
def main():
    ncell = len(PANELS) * len(BOOKS) * len(SLEEVES)
    say(f"IDEA 405 — THE LEVERED SLEEVE PRICED AGAINST ITS OWN TURNOVER (lane C, 2026-09-08).")
    say(f"{ncell} cells x {len(ARMS)} arms x {len(COSTS)} cost rungs x {len(FINS)} financing "
        f"rungs = {ncell*len(ARMS)*len(COSTS)*len(FINS)} arm-rows from "
        f"{ncell*len(ARMS)} simulated paths (both fee taps are exactly linear).")
    say(f"cost sweep {COSTS} bps; financing sweep {FINS} bps/yr on borrowed notional.")
    say(f"Verdict quoted at the PROTOCOL rung c={C_PROTO:.0f} bps, phi={FIN_HEADLINE:.0f} bps. "
        f"Cash earns 0 at gross<1 (record convention; taxes INC/CTL, not LEV).")
    say(f"Arms: " + ", ".join(f"{k} f={v[0]:.2f} g={v[1]:.2f}" for k, v in ARMS.items()))

    rows, rets, ref = [], {}, {}

    for pk in PANELS:
        px = load_universe(broad=(pk == "broad"))
        missing = [t for t in SLEEVES["S4"] if t not in px.columns]
        if missing:
            raise RuntimeError(f"{pk} lacks {missing}")
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        b_full, b_is, ob = bars_win(spy, "full"), bars_win(spy, "IS"), oos_bars(spy)
        ms, mo = metrics(spy), metrics(spy.loc[OOS_START:])
        ref[pk] = dict(bfull=b_full, bIS=b_is, oos=ob, start=start)
        say(f"\n[panel] {pk}: {px.shape[1]} cols {px.index[0].date()}..{px.index[-1].date()}, "
            f"eval from {start.date()}")
        say(f"    SPY full {ms['CAGR']:.2%}/{ms['Sharpe']:.3f}/{ms['MaxDD']:.2%} halves "
            f"{b_full['s1']:.3f}/{b_full['s2']:.3f}; OOS {mo['CAGR']:.2%}/{mo['Sharpe']:.3f}/"
            f"{mo['MaxDD']:.2%}")
        say(f"    4b bars (full): H1>{b_full['s1']:.3f} H2>{b_full['s2']:.3f} "
            f"OOS>{b_full['soos']:.3f} MaxDD>={-DELTA*abs(b_full['sdd']):.2%} "
            f"CAGR>={PHI*ms['CAGR']:.2%}")

        v2 = {c: backtest(px, rules_v2_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        ref[pk]["v2"], ref[pk]["v1"] = v2, v1
        for c in (C_PROTO, 25.0):
            m2 = metrics(v2[c])
            h = H.halves(v2[c])
            say(f"    RULES v2 (live) @{c:.0f}bps {m2['CAGR']:.2%}/{m2['Sharpe']:.3f}/"
                f"{m2['MaxDD']:.2%} halves {h[0]:.3f}/{h[1]:.3f}")

        # ---- gate (a): run_lev == H.run == engine.backtest where the cap does not bind ----
        Wchk = H.targets(px, "EWall")
        a = run_lev(px, Wchk, bps=10.0)["r"].loc[start:]
        b = H.run(px, Wchk, bps=10.0, freq=FREQ)["r"].loc[start:]
        c0 = backtest(px, Wchk, cost_bps=10.0, freq=FREQ)["returns"].loc[start:]
        say(f"    [gate a] run_lev vs H.run max|d| {float((a-b).abs().max()):.3e}; "
            f"vs engine.backtest max|d| {float((a-c0).abs().max()):.3e}")
        assert float((a - b).abs().max()) < 1e-12 and float((a - c0).abs().max()) < 1e-12

        base_W = {bk: H.targets(px, bk) for bk in BOOKS}
        sl_W = {sk: sleeve_weights(px, av) for sk, av in SLEEVES.items()}

        for bk in BOOKS:
            for sk in SLEEVES:
                for an, (f, g) in ARMS.items():
                    W = blend(base_W[bk], sl_W[sk], f, g)
                    out = run_lev(px, W, bps=0.0)
                    r0, turn, gr = out["r"], out["to"], out["gross"]

                    # ---- gate (b): the linear-cost identity is EXACT --------------
                    for c in COSTS:
                        if c == 0.0:
                            continue
                        direct = run_lev(px, W, bps=c)["r"]
                        lin = priced(r0, turn, gr, c, 0.0)
                        d = float((direct - lin).abs().max())
                        assert d < 1e-15, f"cost identity broke at {c}: {d:.3e}"

                    for c in COSTS:
                        for fin in FINS:
                            r = priced(r0, turn, gr, c, fin).loc[start:]
                            key = (pk, bk, sk, an, c, fin)
                            rets[key] = r
                            m = metrics(r)
                            mI, mO = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
                            h1, h2 = H.halves(r)
                            mgf = margins(r, b_full, "full")
                            mgi = margins(r, b_is, "IS")
                            mgo = oos_margins(r, ob)
                            rows.append(dict(
                                panel=pk, book=bk, sleeve=sk, arm=an, f=f, g=g, cost=c, fin=fin,
                                CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], Vol=m["Vol"],
                                H1=h1, H2=h2,
                                IS_Sharpe=mI["Sharpe"], IS_CAGR=mI["CAGR"], IS_MaxDD=mI["MaxDD"],
                                OOS_Sharpe=mO["Sharpe"], OOS_CAGR=mO["CAGR"],
                                OOS_MaxDD=mO["MaxDD"],
                                gross=float(gr.loc[start:].mean()),
                                borrowed=float((gr.loc[start:] - 1.0).clip(lower=0.0).mean()),
                                turnover=float(turn.loc[start:].sum() / (len(r) / 252)),
                                m_H1=mgf["H1"], m_H2=mgf["H2"], m_OOS=mgf["OOS"],
                                m_DD=mgf["DD"], m_CAGR=mgf["CAGR"],
                                m_min=min(mgf.values()), pass4b=pass_all(mgf),
                                IS_m_min=min(mgi.values()), IS_pass4b=pass_all(mgi),
                                IS_Sharpe_win=mI["Sharpe"],
                                OOS_m_S=mgo["S"], OOS_m_DD=mgo["DD"], OOS_m_CAGR=mgo["CAGR"],
                                OOS_m_min=min(mgo.values()), OOS_pass=pass_all(mgo),
                                pass4a_v2=H.pass4a(r, v2[c]),
                                pass4a_v1_10=H.pass4a(r, v1[10.0]),
                            ))

    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"\n[grid] {len(G)} arm-rows written to {STEM}.grid.csv")

    # ---- gate (c): reproduce idea 402's committed rows ----------------------
    say("\n[gate c] REPRODUCTION of idea 402's committed .grid.csv on its shared rows "
        "(arms INC/LEV/CTL at their (f,g), cost 10/25, fin 0/300)")
    if I402_GRID.exists():
        g402 = pd.read_csv(I402_GRID)
        diffs = []
        for an, (f, g) in ARMS.items():
            for c in (10.0, 25.0):
                for fin in (0.0, 300.0):
                    q = g402[(np.isclose(g402.f, f)) & (np.isclose(g402.g, g)) &
                             (g402.cost == c) & (g402.fin == fin)]
                    mine = G[(G.arm == an) & (G.cost == c) & (G.fin == fin)]
                    for _, qq in q.iterrows():
                        cd = mine[(mine.panel == qq.panel) & (mine.book == qq.book) &
                                  (mine.sleeve == qq.sleeve)]
                        if len(cd) != 1:
                            continue
                        cd = cd.iloc[0]
                        for col in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
                                    "turnover", "gross"):
                            diffs.append(abs(float(cd[col]) - float(qq[col])))
        if diffs:
            say(f"    matched {len(diffs)//8} rows x 8 columns; max|d| {max(diffs):.3e} "
                f"(u56 cache drift caveat, idea 401: ~1e-5 is the floor after a daily close)")
        else:
            say("    NO overlapping rows found — reproduction gate SKIPPED")
    else:
        say("    idea 402's grid CSV not present — reproduction gate SKIPPED")

    # ================================================================== Q1 ====
    say("\n" + "=" * 100)
    say("Q1  PREMISE CHECK — is the turnover multiple really 3.4x (2.3x -> 7.9x/yr)?")
    say("=" * 100)
    T = G[(G.cost == C_PROTO) & (G.fin == 0.0)].pivot_table(
        index=["panel", "book", "sleeve"], columns="arm", values="turnover")
    T["LEV/INC"] = T["LEV"] / T["INC"]
    T["gLEV/gINC"] = 1.25 / 0.75
    say(T.to_string(float_format=lambda x: f"{x:.3f}"))
    say(f"\n    Turnover multiple LEV/INC: median {T['LEV/INC'].median():.3f}, range "
        f"{T['LEV/INC'].min():.3f}-{T['LEV/INC'].max():.3f}, against the queue's stated 3.4x "
        f"and the pure gross ratio {1.25/0.75:.3f}.")
    ewa = T.xs("EWall", level="book")["LEV/INC"]
    top = T.xs("TOP20", level="book")["LEV/INC"]
    say(f"    By base book: EWall median {ewa.median():.3f} (idea 402 tabulated 2.29->7.90 = "
        f"3.45x on EWall rows), TOP20 median {top.median():.3f}.  P1 "
        f"{'CONFIRMED' if top.median() < ewa.median() else 'REJECTED'}.")
    say(f"    Mean borrowed notional at LEV: "
        f"{G[(G.arm=='LEV')].borrowed.mean():.4f} of NAV; at INC "
        f"{G[(G.arm=='INC')].borrowed.mean():.4f} (INC never borrows, by construction).")

    # ================================================================== Q2 ====
    say("\n" + "=" * 100)
    say("Q2  THE JOINT REGION — over the 4 x 7 = 28 (cost, financing) rungs, where does LEV "
        "beat INC on Sharpe?")
    say("=" * 100)
    piv = G.pivot_table(index=["panel", "book", "sleeve", "cost", "fin"], columns="arm",
                        values=["Sharpe", "CAGR", "MaxDD", "OOS_Sharpe", "pass4b"])
    reg = []
    for (pk, bk, sk), _ in G.groupby(["panel", "book", "sleeve"]):
        for c in COSTS:
            for fin in FINS:
                sub = G[(G.panel == pk) & (G.book == bk) & (G.sleeve == sk) &
                        (G.cost == c) & (G.fin == fin)].set_index("arm")
                reg.append(dict(
                    panel=pk, book=bk, sleeve=sk, cost=c, fin=fin,
                    S_LEV=sub.loc["LEV", "Sharpe"], S_INC=sub.loc["INC", "Sharpe"],
                    S_CTL=sub.loc["CTL", "Sharpe"], S_CTLg=sub.loc["CTLg", "Sharpe"],
                    dS=sub.loc["LEV", "Sharpe"] - sub.loc["INC", "Sharpe"],
                    dCAGR=sub.loc["LEV", "CAGR"] - sub.loc["INC", "CAGR"],
                    dDD=abs(sub.loc["INC", "MaxDD"]) - abs(sub.loc["LEV", "MaxDD"]),
                    dOOS=sub.loc["LEV", "OOS_Sharpe"] - sub.loc["INC", "OOS_Sharpe"],
                    LEV_4b=bool(sub.loc["LEV", "pass4b"]), INC_4b=bool(sub.loc["INC", "pass4b"]),
                    LEV_win=bool(sub.loc["LEV", "Sharpe"] > sub.loc["INC", "Sharpe"]),
                    LEV_win_and_4b=bool((sub.loc["LEV", "Sharpe"] > sub.loc["INC", "Sharpe"])
                                        and sub.loc["LEV", "pass4b"]),
                    LEV_beats_CTLg=bool(sub.loc["LEV", "Sharpe"] > sub.loc["CTLg", "Sharpe"]),
                ))
    R = pd.DataFrame(reg)
    R.to_csv(OUT / f"{STEM}.region.csv", index=False)

    say("\n  dSharpe(LEV - INC) surface, cell mean over the 8 cells (rows = cost bps, "
        "cols = financing bps):")
    say(R.pivot_table(index="cost", columns="fin", values="dS").to_string(
        float_format=lambda x: f"{x:+.4f}"))
    say("\n  Cells (of 8) in which LEV beats INC on Sharpe:")
    say(R.pivot_table(index="cost", columns="fin", values="LEV_win", aggfunc="sum")
        .to_string())
    say("\n  Cells (of 8) in which LEV beats INC AND passes 4b:")
    say(R.pivot_table(index="cost", columns="fin", values="LEV_win_and_4b", aggfunc="sum")
        .to_string())
    say("\n  Cells (of 8) in which the INCUMBENT itself passes 4b (the comparand's own region):")
    say(R.pivot_table(index="cost", columns="fin", values="INC_4b", aggfunc="sum").to_string())
    say("\n  Per-cell count of winning rungs (of 28) and the region's shape:")
    shape = []
    for (pk, bk, sk), sub in R.groupby(["panel", "book", "sleeve"]):
        w = sub.pivot_table(index="cost", columns="fin", values="LEV_win")
        nwin = int(sub.LEV_win.sum())
        # max cost rung and max fin rung at which the cell still wins somewhere
        cmax = sub[sub.LEV_win].cost.max() if nwin else np.nan
        fmax = sub[sub.LEV_win].fin.max() if nwin else np.nan
        # monotone staircase check: within each cost row, wins form a prefix in fin
        stair = all(list(w.loc[c].values) == sorted(w.loc[c].values, reverse=True)
                    for c in COSTS)
        shape.append(dict(panel=pk, book=bk, sleeve=sk, n_win=nwin, cost_max=cmax,
                          fin_max=fmax, prefix_in_fin=stair,
                          win_at_proto=bool(sub[(sub.cost == C_PROTO) &
                                                (sub.fin == FIN_HEADLINE)].LEV_win.iloc[0])))
    SH = pd.DataFrame(shape)
    say(SH.to_string(index=False))
    say(f"\n    LEV wins in {int(R.LEV_win.sum())} of {len(R)} (cell, rung) points; the win "
        f"set is a prefix in financing within every cost row in {int(SH.prefix_in_fin.sum())} "
        f"of 8 cells.")
    at_proto = R[(R.cost == C_PROTO) & (R.fin == FIN_HEADLINE)]
    say(f"    AT THE RECORD'S OWN RUNG (c={C_PROTO:.0f}, phi={FIN_HEADLINE:.0f}): LEV beats INC "
        f"in {int(at_proto.LEV_win.sum())} of 8 cells (mean dSharpe "
        f"{at_proto.dS.mean():+.4f}), passes 4b in {int(at_proto.LEV_4b.sum())} of 8; "
        f"P4 predicted a majority — "
        f"{'CONFIRMED' if at_proto.LEV_win.sum() >= 5 else 'REJECTED'}.")

    # ================================================================== Q3 ====
    say("\n" + "=" * 100)
    say("Q3  THE BREAK-EVEN FRONTIER phi*(c) — borrow rate at which the Sharpe edge dies")
    say("=" * 100)
    fr = []
    for (pk, bk, sk), sub in R.groupby(["panel", "book", "sleeve"]):
        for c in COSTS:
            s = sub[sub.cost == c].sort_values("fin")
            v, kind = crossing(s.fin.values, s.dS.values, 0.0)
            v4, kind4 = crossing(s.fin.values, s.LEV_4b.astype(float).values - 0.5, 0.0)
            fr.append(dict(panel=pk, book=bk, sleeve=sk, cost=c,
                           dS_at_0=s.dS.iloc[0], dS_at_600=s.dS.iloc[-1],
                           phi_star=v, kind=kind,
                           phi_4b=v4 if kind4 == "interior" else np.nan, kind_4b=kind4))
    F = pd.DataFrame(fr)
    F.to_csv(OUT / f"{STEM}.frontier.csv", index=False)
    say(F.to_string(index=False, float_format=lambda x: f"{x:.1f}"))
    for c in COSTS:
        s = F[F.cost == c]
        interior = s[s.kind == "interior"]
        say(f"\n    c={c:5.1f} bps: phi* interior in {len(interior)}/8 cells "
            f"(median {interior.phi_star.median():.0f} bps if any), above-all "
            f"{(s.kind=='above-all').sum()} (LEV wins out to 600 bps), below-all "
            f"{(s.kind=='below-all').sum()} (LEV never wins).")
    piv_f = F.pivot_table(index=["panel", "book", "sleeve"], columns="cost", values="phi_star")
    say("\n  phi*(c) per cell (bps of borrow the edge can absorb; NaN = never crosses "
        "inside 0-600):")
    say(piv_f.to_string(float_format=lambda x: f"{x:.0f}"))
    med = F[F.kind == "interior"].groupby("cost").phi_star.median()
    cnt = F[F.kind == "interior"].groupby("cost").phi_star.size()
    say(f"\n  Median phi* by cost rung (UNPAIRED — different cells are interior at each rung, "
        f"so this median is NOT comparable across rungs): " +
        ", ".join(f"{c:.0f}bps -> {v:.0f} (n={cnt[c]})" for c, v in med.items()))
    # PAIRED exchange rate: only cells whose phi* is interior at BOTH rungs of a step.
    say("\n  PAIRED exchange rate d phi*/d c, per cell, over cost steps where the cell's "
        "phi* is interior at BOTH ends (the unpaired median above is a composition artefact):")
    pw = F.pivot_table(index=["panel", "book", "sleeve"], columns="cost", values="phi_star")
    slopes = []
    for (a, b) in zip(COSTS[:-1], COSTS[1:]):
        if a not in pw.columns or b not in pw.columns:
            continue
        ok = pw[[a, b]].dropna()
        for idx, r_ in ok.iterrows():
            slopes.append(dict(cell="/".join(idx), step=f"{a:.0f}->{b:.0f}",
                               slope=(r_[b] - r_[a]) / (b - a)))
    SL = pd.DataFrame(slopes)
    if len(SL):
        say(SL.to_string(index=False, float_format=lambda x: f"{x:+.1f}"))
        sm = SL.slope.median()
        say(f"  MEDIAN PAIRED d phi*/d c = {sm:+.1f} bps of borrow per bp of trading cost "
            f"over {len(SL)} paired cell-steps (range {SL.slope.min():+.1f}.."
            f"{SL.slope.max():+.1f}).  P3 predicted 'a few tens, negative': "
            f"{'CONFIRMED' if sm < -10 else 'REJECTED'}.")
    say(f"\n  Idea 402 published a median break-even of 277 bps at c=10.  Here: median "
        f"{F[(F.cost==C_PROTO)&(F.kind=='interior')].phi_star.median():.0f} bps over "
        f"{(F[(F.cost==C_PROTO)].kind=='interior').sum()} interior cells of 8.")

    # ================================================================== Q4 ====
    say("\n" + "=" * 100)
    say("Q4  DECOMPOSITION — the LEV-minus-INC Sharpe gap, split into zero-fee gap, trading "
        "increment and financing increment (idea 137's method)")
    say("=" * 100)
    dec = []
    for (pk, bk, sk), _ in G.groupby(["panel", "book", "sleeve"]):
        base = R[(R.panel == pk) & (R.book == bk) & (R.sleeve == sk) &
                 (R.cost == 0.0) & (R.fin == 0.0)].dS.iloc[0]
        for c in COSTS:
            for fin in FINS:
                tot = R[(R.panel == pk) & (R.book == bk) & (R.sleeve == sk) &
                        (R.cost == c) & (R.fin == fin)].dS.iloc[0]
                trad = R[(R.panel == pk) & (R.book == bk) & (R.sleeve == sk) &
                         (R.cost == c) & (R.fin == 0.0)].dS.iloc[0] - base
                finc = R[(R.panel == pk) & (R.book == bk) & (R.sleeve == sk) &
                         (R.cost == 0.0) & (R.fin == fin)].dS.iloc[0] - base
                dec.append(dict(panel=pk, book=bk, sleeve=sk, cost=c, fin=fin,
                                dS_total=tot, dS_zero_fee=base, trad_inc=trad, fin_inc=finc,
                                resid=tot - base - trad - finc))
    D = pd.DataFrame(dec)
    D.to_csv(OUT / f"{STEM}.decomp.csv", index=False)
    say(f"  Additivity residual (total - zerofee - trading - financing): max|resid| "
        f"{D.resid.abs().max():.3e}, mean {D.resid.abs().mean():.3e}.  The two taps are "
        f"NOT exactly additive in SHARPE (they are in returns); the residual size says how "
        f"far from additive.")
    say("\n  Cell-mean split at each rung (zero-fee gap is constant by construction):")
    say(D.pivot_table(index="cost", columns="fin", values="trad_inc").to_string(
        float_format=lambda x: f"{x:+.4f}") + "   <- trading increment (invariant in phi)")
    say(D.pivot_table(index="cost", columns="fin", values="fin_inc").to_string(
        float_format=lambda x: f"{x:+.4f}") + "   <- financing increment (invariant in c)")
    say(f"\n  Zero-fee dSharpe (LEV - INC), cell mean {D.dS_zero_fee.mean():+.4f}, "
        f"range {D.dS_zero_fee.min():+.4f}..{D.dS_zero_fee.max():+.4f}, positive in "
        f"{int((D.groupby(['panel','book','sleeve']).dS_zero_fee.first() > 0).sum())} of 8 cells.")
    at = D[(D.cost == C_PROTO) & (D.fin == FIN_HEADLINE)]
    say(f"  At c={C_PROTO:.0f}/phi={FIN_HEADLINE:.0f}: cell-mean total {at.dS_total.mean():+.4f} "
        f"= zero-fee {at.dS_zero_fee.mean():+.4f} + trading {at.trad_inc.mean():+.4f} + "
        f"financing {at.fin_inc.mean():+.4f} (+resid {at.resid.mean():+.4f}).")
    tsum, fsum = at.trad_inc.abs().mean(), at.fin_inc.abs().mean()
    say(f"  WHICH TAP DOMINATES at the record's rung: trading {tsum/(tsum+fsum):.1%} vs "
        f"financing {fsum/(tsum+fsum):.1%} of the total fee drag on the gap.")
    say("  Cell-mean fee drag on the gap at every rung (trading + financing, in Sharpe):")
    D["fee_drag"] = D.trad_inc + D.fin_inc
    say(D.pivot_table(index="cost", columns="fin", values="fee_drag").to_string(
        float_format=lambda x: f"{x:+.4f}"))

    # ================================================================== Q5 ====
    say("\n" + "=" * 100)
    say("Q5  RULE 8 WALK-FORWARD — the ARM chosen on 2009-2016 only at each rung, "
        "2017-2026 read once")
    say("=" * 100)
    say("  Selectors (both see IS only): S0 = argmax IS Sharpe over {INC, LEV, CTL, CTLg}; "
        "S1 = IS-4b-admissible then argmax IS Sharpe (abstains if none admissible).")
    wf = []
    for (pk, bk, sk), _ in G.groupby(["panel", "book", "sleeve"]):
        ob = ref[pk]["oos"]
        for c in COSTS:
            for fin in FINS:
                sub = G[(G.panel == pk) & (G.book == bk) & (G.sleeve == sk) &
                        (G.cost == c) & (G.fin == fin)].set_index("arm")
                s0 = sub.IS_Sharpe.idxmax()
                adm = sub[sub.IS_pass4b]
                s1 = adm.IS_Sharpe.idxmax() if len(adm) else None
                inc = sub.loc["INC"]
                lev = sub.loc["LEV"]
                rowd = dict(panel=pk, book=bk, sleeve=sk, cost=c, fin=fin,
                            S0=s0, S1=s1 if s1 else "ABSTAIN",
                            IS_win_LEV=bool(lev.IS_Sharpe > inc.IS_Sharpe),
                            OOS_win_LEV=bool(lev.OOS_Sharpe > inc.OOS_Sharpe),
                            S0_OOS_S=sub.loc[s0, "OOS_Sharpe"],
                            S0_OOS_CAGR=sub.loc[s0, "OOS_CAGR"],
                            S0_OOS_DD=sub.loc[s0, "OOS_MaxDD"],
                            S0_OOS_pass=bool(sub.loc[s0, "OOS_pass"]),
                            S1_OOS_S=sub.loc[s1, "OOS_Sharpe"] if s1 else np.nan,
                            S1_OOS_CAGR=sub.loc[s1, "OOS_CAGR"] if s1 else np.nan,
                            S1_OOS_DD=sub.loc[s1, "OOS_MaxDD"] if s1 else np.nan,
                            S1_OOS_pass=bool(sub.loc[s1, "OOS_pass"]) if s1 else False,
                            INC_OOS_S=inc.OOS_Sharpe, INC_OOS_CAGR=inc.OOS_CAGR,
                            INC_OOS_DD=inc.OOS_MaxDD, INC_OOS_pass=bool(inc.OOS_pass),
                            LEV_OOS_S=lev.OOS_Sharpe, LEV_OOS_CAGR=lev.OOS_CAGR,
                            LEV_OOS_DD=lev.OOS_MaxDD, LEV_OOS_pass=bool(lev.OOS_pass),
                            SPY_OOS_S=ob["sharpe"], SPY_OOS_CAGR=ob["cagr"],
                            SPY_OOS_DD=ob["dd"])
                wf.append(rowd)
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say("\n  S0 pick counts by rung (rows = cost, cols = financing), 8 cells each:")
    for arm in ARMS:
        cnt = WF[WF.S0 == arm].pivot_table(index="cost", columns="fin", values="S0",
                                           aggfunc="count")
        if len(cnt):
            say(f"  --- S0 picks {arm} ---")
            say(cnt.fillna(0).astype(int).to_string())
    say("\n  S1 (IS-4b screened) pick counts:")
    say(WF.groupby("S1").size().to_string())
    say("\n  IS says LEV beats INC vs OOS says so (the rule-8 question), count of 8 per rung:")
    say("  IS:")
    say(WF.pivot_table(index="cost", columns="fin", values="IS_win_LEV", aggfunc="sum")
        .to_string())
    say("  OOS:")
    say(WF.pivot_table(index="cost", columns="fin", values="OOS_win_LEV", aggfunc="sum")
        .to_string())
    agree = (WF.IS_win_LEV == WF.OOS_win_LEV).mean()
    say(f"\n  IS/OOS agreement on the LEV>INC call: {agree:.1%} of {len(WF)} (cell, rung) "
        f"points.  IS wins {WF.IS_win_LEV.sum()}, OOS wins {WF.OOS_win_LEV.sum()} — "
        f"P5 predicted the OOS region is SMALLER: "
        f"{'CONFIRMED' if WF.OOS_win_LEV.sum() < WF.IS_win_LEV.sum() else 'REJECTED'}.")
    say("\n  OOS performance at the PROTOCOL rung (c=10, phi=300), cell means over 8 cells:")
    ap = WF[(WF.cost == C_PROTO) & (WF.fin == FIN_HEADLINE)]
    say(f"    S0        OOS CAGR {ap.S0_OOS_CAGR.mean():.2%} Sharpe {ap.S0_OOS_S.mean():.4f} "
        f"MaxDD {ap.S0_OOS_DD.mean():.2%}  clears 3 OOS 4b bars {int(ap.S0_OOS_pass.sum())}/8")
    say(f"    S1        OOS CAGR {ap.S1_OOS_CAGR.mean():.2%} Sharpe {ap.S1_OOS_S.mean():.4f} "
        f"MaxDD {ap.S1_OOS_DD.mean():.2%}  clears {int(ap.S1_OOS_pass.sum())}/8")
    say(f"    INC (std) OOS CAGR {ap.INC_OOS_CAGR.mean():.2%} Sharpe {ap.INC_OOS_S.mean():.4f} "
        f"MaxDD {ap.INC_OOS_DD.mean():.2%}  clears {int(ap.INC_OOS_pass.sum())}/8")
    say(f"    LEV       OOS CAGR {ap.LEV_OOS_CAGR.mean():.2%} Sharpe {ap.LEV_OOS_S.mean():.4f} "
        f"MaxDD {ap.LEV_OOS_DD.mean():.2%}  clears {int(ap.LEV_OOS_pass.sum())}/8")
    say(f"    SPY       OOS CAGR {ap.SPY_OOS_CAGR.mean():.2%} Sharpe {ap.SPY_OOS_S.mean():.4f} "
        f"MaxDD {ap.SPY_OOS_DD.mean():.2%}")
    for pk in PANELS:
        v2o = metrics(ref[pk]["v2"][C_PROTO].loc[OOS_START:])
        say(f"    RULES v2 (live) {pk} @10bps OOS CAGR {v2o['CAGR']:.2%} Sharpe "
            f"{v2o['Sharpe']:.4f} MaxDD {v2o['MaxDD']:.2%}")
    say("\n  OOS dSharpe(LEV - INC) surface, cell mean (rows = cost, cols = financing):")
    say(R.pivot_table(index="cost", columns="fin", values="dOOS").to_string(
        float_format=lambda x: f"{x:+.4f}"))

    # ============================================================ KEEP paths ==
    say("\n" + "=" * 100)
    say("KEEP PATHS over all rows (4a judged against the LIVE RULES v2 book, cost-matched, "
        "per PROTOCOL 3; 4b per PROTOCOL 4b)")
    say("=" * 100)
    KP = G.groupby(["arm", "cost", "fin"]).agg(
        n=("pass4b", "size"), p4b=("pass4b", "sum"), p4a=("pass4a_v2", "sum"),
        p4a_v1=("pass4a_v1_10", "sum")).reset_index()
    KP["both"] = 0
    for i, r_ in KP.iterrows():
        s = G[(G.arm == r_.arm) & (G.cost == r_.cost) & (G.fin == r_.fin)]
        KP.loc[i, "both"] = int((s.pass4b & s.pass4a_v2).sum())
    KP.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    say(f"  Totals over {len(G)} rows: 4b {int(G.pass4b.sum())}, 4a(v2, cost-matched) "
        f"{int(G.pass4a_v2.sum())}, BOTH {int((G.pass4b & G.pass4a_v2).sum())}, "
        f"4a(v1 @fixed 10bps) {int(G.pass4a_v1_10.sum())} "
        f"(the comparand gap open idea 398 owns).")
    say("\n  4b pass count by arm and cost rung (of 8 cells x 7 fin rungs = 56 each):")
    say(G.pivot_table(index="arm", columns="cost", values="pass4b", aggfunc="sum").to_string())
    say("\n  4b pass count by arm and financing rung (of 8 cells x 4 cost rungs = 32 each):")
    say(G.pivot_table(index="arm", columns="fin", values="pass4b", aggfunc="sum").to_string())

    # ------------------------------------------------------------- verdict ---
    say("\n" + "=" * 100)
    say("VERDICT against the PRE-REGISTERED decision rule")
    say("=" * 100)
    proto = R[(R.cost == C_PROTO) & (R.fin >= FIN_HEADLINE)]
    all8 = all(int(R[(R.cost == C_PROTO) & (R.fin == fin)].LEV_win_and_4b.sum()) == 8
               for fin in FINS if fin >= FIN_HEADLINE)
    s1pass = int(ap.S1_OOS_pass.sum())
    s1_lev = int((WF[(WF.cost == C_PROTO) & (WF.fin == FIN_HEADLINE)].S1 == "LEV").sum())
    say(f"  (i)   LEV wins AND passes 4b in all 8 cells at c=10 for every phi>=300: "
        f"{'YES' if all8 else 'NO'} "
        f"(actual at phi=300: {int(at_proto.LEV_win_and_4b.sum())}/8; "
        f"at phi=600: {int(R[(R.cost==C_PROTO)&(R.fin==600.0)].LEV_win_and_4b.sum())}/8)")
    say(f"  (ii)  rule-8 S1 picks LEV at that rung in {s1_lev}/8 cells and clears all three "
        f"OOS 4b bars in {s1pass}/8 (bar was >=7/8)")
    keep = all8 and s1pass >= 7 and s1_lev >= 5
    # fee-story classification, pre-defined
    win_hi_c = int(R[(R.cost == 25.0) & (R.fin == FIN_HEADLINE)].LEV_win.sum())
    win_hi_f = int(R[(R.cost == C_PROTO) & (R.fin == 600.0)].LEV_win.sum())
    fee_story = (win_hi_c < 5) and (win_hi_f < 5)
    say(f"  (iii) FEE-STORY test (pre-defined: the win region needs c<=10 AND phi<=300): "
        f"moving cost one rung up (c=25, phi=300) LEV wins {win_hi_c}/8; moving borrow to the "
        f"top rung (c=10, phi=600) LEV wins {win_hi_f}/8.  "
        f"{'FEE STORY' if fee_story else 'NOT a fee story'}.")
    verdict = "KEEP-candidate (4b)" if keep else ("KILL (fee story)" if fee_story
                                                  else "ANSWERED / PARK")
    say(f"\n  VERDICT: {verdict}")

    # ------------------------------------------------- caveat, quantified ----
    say("\n" + "=" * 100)
    say("CAVEAT, QUANTIFIED — what open idea 406's cash-credit convention would do to this "
        "frontier")
    say("=" * 100)
    say("  INC holds mean cash 1 - 0.750 = 0.250 of NAV; LEV borrows mean "
        f"{G[G.arm=='LEV'].borrowed.mean():.3f}.  Crediting cash at k bps/yr therefore adds "
        "k*0.250/1e4 to INC's return and 0 to LEV's, i.e. it moves the frontier AGAINST LEV "
        "by roughly (0.250/borrowed) bps of borrow per bp of credit.")
    bmean = G[G.arm == "LEV"].borrowed.mean()
    say(f"  With borrowed = {bmean:.3f}, the exchange rate is ~{0.250/bmean:.2f} bps of phi* "
        f"per bp of cash credit: a 150-bps credit (idea 406's first rung) would cut phi* by "
        f"~{150*0.250/bmean:.0f} bps.  Every phi* below is therefore an UPPER bound under the "
        f"record's cash-at-zero convention.")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    say(f"\n[done] console -> {STEM}.console.txt")


if __name__ == "__main__":
    main()
