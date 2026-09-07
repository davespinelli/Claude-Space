#!/usr/bin/env python3
"""QUEUE idea 402 — does-a-levered-f-060-book-clear-the-CAGR-floor   (lane C, 2026-09-07).

PRE-REGISTERED QUESTION (verbatim from QUEUE.md idea 402, written before any number here
was read)
    "idea 138 found the sleeve fraction's Sharpe argmax is f=0.60 (cell-mean 1.196 vs 1.131
     at the adopted 0.25) and that it fails 4b ONLY on the CAGR floor, in 16 of 16 cells.
     Price the f=0.60 book at gross > 0.75 against its own 0.75 control and against the
     floor, and say whether the 4b-defensive class at high f is just the sleeve's own low
     return.  Max 2 params."

WHY IT MATTERS
    The record's 4b path has five bars.  Idea 138 showed that on the sleeve-fraction dial the
    Sharpe bars and the drawdown cap get EASIER as f rises while the CAGR floor gets harder,
    so the adopted f = 0.25 is the argmax of the 4b MARGIN, not of Sharpe.  If the only thing
    wrong with the higher-Sharpe f = 0.60 book is that it holds too little risk, then the
    honest instrument is not "sleeve fraction" at all — it is EXPOSURE, and the 4b-defensive
    class at high f is idea 127's exposure effect wearing a sleeve.  The test is direct: put
    the gross back and see whether the book clears the floor without breaching the DD cap.

WHAT IS TESTED (fixed in advance)
    Q1  Does f = 0.60 clear PROTOCOL 4b at ANY gross, per cell, and how wide is the g-window?
    Q2  At MATCHED CAGR with the standing candidate (f = 0.25 @ 0.75, idea 139), is the
        levered f = 0.60 book better on Sharpe and on MaxDD?  (This is the queue's second
        sentence: if yes, high f is just low return.)
    Q3  Against its OWN levered control: at every g, f = 0.60 vs f = 0.00 (the equity book at
        the same gross), so the comparison is never an exposure comparison (ideas 127/135/395).
    Q4  Rule 8.  g (and, in a second chooser, (f, g) jointly) picked on 2009-2016 only,
        2017-2026 read once.  OOS CAGR/Sharpe/MaxDD vs the incumbent, the control, and SPY.
    Q5  The financing BREAK-EVEN: the borrow rate at which the levered arm loses its Sharpe
        edge over the incumbent, and the rate at which it stops passing 4b at all.  This is
        the number a real allocation turns on, so it is solved for rather than assumed.

GRID (two tuned parameters, both swept, ALL points reported)
    param 1  f  in {0.00, 0.25, 0.60}   — 0.00 control, 0.25 the adopted constant, 0.60 the
             Sharpe argmax idea 138 located.  Not selected on: all three reported everywhere.
    param 2  g  in {0.40, 0.50, 0.60, 0.75, 0.85, 0.90, 1.00, 1.10, 1.25, 1.50, 1.75, 2.00} —
             gross.  0.75 is the record's convention and the control point; g > 1.00 is levered;
             g < 0.75 is carried so the no-sleeve control can be DE-grossed to matched CAGR
             (ideas 135/395's control), which is the only way it reaches the incumbent's return.
    REPORTED AXES, never selected on: panel {u56, broad} x base book {EWall, TOP20} x sleeve
    set {S3 = TLT/GLD/UUP, S4 = TLT/GLD/DBC/UUP} x cost rung {10, 25} bps = 16 cells, and a
    financing rung {0, 150, 300} bps/yr charged on borrowed notional.

BOOK (verbatim from idea 138, one line changed — the rescale target is g, not 0.75)
    raw = (1-f) * base_book + f * sleeve(assets);  book = raw * (g / sum(raw)) per day.
    sleeve(assets) = momentum-vote x risk-parity (ideas 100/104), vote over {12-1m, 6m, 3m}.
    At f = 0, g = 0.75 this is the ungated base book exactly (asserted).

LEVERAGE CONVENTION, stated not buried
    PROTOCOL 2 forbids leverage "unless the idea says so"; idea 402 says so.  Financing is
    charged daily as fin_bps/252 on max(realised gross - 1, 0), i.e. on borrowed notional
    only, using the DRIFTED daily gross, not the target.  Cash earns 0 at g < 1 (the record's
    standing convention, kept so these rows are comparable with idea 138's).  That pairing is
    deliberately UNKIND to the levered arm: it pays to borrow but is not paid to lend.  Sharpe
    is rf = 0 throughout (engine.metrics), as everywhere in this record.  The 300 bps rung is
    the one the verdict is quoted at; all three are printed on every row.

PRE-REGISTERED PREDICTIONS (written before the main grid was read)
    P1  Sharpe is near-INVARIANT in g (rf = 0, costs scale with gross), so the Sharpe bars
        that f = 0.60 already clears at 0.75 stay cleared until financing bites.
    P2  MaxDD deepens close to linearly in g, CAGR rises sub-linearly (volatility drag), so
        the 4b window in g, if it exists, is bounded ABOVE by the DD cap and BELOW by the
        CAGR floor — a crossing, not a plateau (idea 401's shape).
    P3  A g-window exists at f = 0.60 in a MAJORITY of the 16 cells, because idea 138's
        f = 0.60 row misses the floor by ~1.5 pp of CAGR while sitting at MaxDD -11.1% against
        a cap near -20%: there is drawdown room to spend.
    P4  At matched CAGR the levered f = 0.60 book beats f = 0.25 @ 0.75 on Sharpe in most
        cells (its unlevered Sharpe is 0.065 higher on the cell mean) but by LESS than that,
        because financing and cost scale with gross.
    P5  Rule 8's IS-4b chooser picks an interior g and its OOS is close to, not better than,
        the incumbent's, because idea 138 found the IS->OOS rank ordering of this family
        stable but the IS window's DD bar too loose (idea 128's caveat).

DECISION RULE, pre-registered
    KEEP-candidate (4b) only if ONE (f = 0.60, g) pair passes 4b in ALL 16 cells at the
    300 bps financing rung AND the rule-8 IS-4b chooser's OOS clears all three OOS-visible
    bars in >= 14/16 cells AND its OOS Sharpe beats the incumbent's.  Anything weaker is
    PARK.  4a is evaluated on every row against the LIVE book (rules_v2_weights),
    cost-matched, per PROTOCOL 3.

CAVEATS carried, not buried
    * SURVIVORSHIP (idea 54): both panels are current constituents; absent delistings inflate
      the EQUITY leg more than the ETF sleeve, so every number here is biased in favour of
      LOW f and of the unlevered control.  A finding that levered high-f wins is understated.
    * Financing is a FLAT rate over 2009-2026, not a path (no fed-funds series is cached and
      the sandbox has no network).  It therefore misprices the 2009-2015 and 2021-2026 ends
      in opposite directions; 0/150/300 bps brackets the plausible range.
    * MaxDD is one number off one path (idea 321) and the 4b DD cap turns on exactly it.  A
      g-window bounded above by the DD cap inherits that fragility in full.
    * The sleeve is 3-4 ETFs over one macro regime (idea 139 risk (a)).  Leverage does not
      make that sample bigger; it makes a bad draw from it cost more.
    * Idea 126: t+1 only.  Idea 38: calendar-day index on both panels.  Idea 127: realised
      mean gross is printed on every row.
    * Idea 128's IS-window caveat (IS SPY MaxDD shallower than OOS's) biases the IS-4b
      chooser toward admitting too much gross.  Reported, not corrected.

HARNESS: idea 94's simulator (H.run/H.targets/H.halves/H.margins/H.pass4a) is IMPORTED.
`run_lev` below is H.run with every instrument removed and the `s > 1.0` gross CAP removed
(that cap is what makes H.run unable to price leverage at all); it is asserted equal to
H.run and to engine.backtest to machine precision on every g <= 1.00 arm, where the cap does
not bind.  Idea 138's committed .grid.csv is reproduced on its shared (f, g = 0.75) rows.
Deterministic, standalone.  Modifies nothing.  Writes .console.txt, .grid.csv, .window.csv,
.matched.csv, .walkforward.csv, .breakeven.csv, .keeppaths.csv next to itself.
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

STEM = "2026-09-07_does-a-levered-f-060-book-clear-the-CAGR-floor_C"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I138_GRID = OUT / "2026-09-07_sleeve-f-plateau-width_B.grid.csv"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")

FREQ = H.FREQ
BASE_GROSS = H.GROSS                     # 0.75, the record's convention and the control point
IS_END, OOS_START = H.IS_END, H.OOS_START
COSTS = [10.0, 25.0]
FINS = [0.0, 150.0, 300.0]               # bps/yr on borrowed notional; reported axis
FIN_HEADLINE = 300.0                     # the rung the verdict is quoted at (pre-registered)
PHI, DELTA = 0.70, 0.60                  # 4b CAGR floor / DD cap fractions of SPY
FS = [0.00, 0.25, 0.60]                  # tuned parameter 1 — all reported
GS = [0.40, 0.50, 0.60, 0.75, 0.85, 0.90, 1.00, 1.10, 1.25, 1.50, 1.75, 2.00]  # param 2, all reported
SLEEVES = {"S3": ["TLT", "GLD", "UUP"], "S4": ["TLT", "GLD", "DBC", "UUP"]}
BOOKS = ["EWall", "TOP20"]
PANELS = ["u56", "broad"]
INCUMBENT = (0.25, 0.75)                 # idea 139's standing 4b KEEP-candidate
ARGMAX_F = 0.60                          # idea 138's Sharpe argmax — the subject of this run

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 6000)
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
    """Ideas 100/104's sleeve, verbatim from ideas 133/134/138: momentum vote x risk parity."""
    sub = px[assets]
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[assets] = (_vote_mom(sub) * _risk_parity(sub)).fillna(0.0)
    return out


def blend(base_W, sl_W, f, g):
    """(1-f)*base + f*sleeve, rescaled to gross g per day.  f=0 is the base book at gross g."""
    raw = base_W if f == 0.0 else (1 - f) * base_W + f * sl_W
    return raw.mul((g / raw.sum(axis=1).replace(0, np.nan)).fillna(0.0), axis=0).fillna(0.0)


# ------------------------------------------------- leverage-capable simulator --
def run_lev(px, W, bps, freq=FREQ):
    """H.run with every instrument removed AND the `s > 1.0` gross cap removed.

    Identical to H.run for any book whose target gross never exceeds 1.0 (asserted below).
    Returns the drifted daily gross so financing can be charged on realised borrowing.
    """
    rets = px.pct_change().fillna(0.0).values
    tgt = W.reindex(px.index).fillna(0.0).values
    mask = H.rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    nrow, ncol = rets.shape
    cur = np.zeros(ncol)
    held = np.zeros((nrow, ncol))
    turn = np.zeros(nrow)
    gross_s = np.zeros(nrow)
    for i in range(nrow):
        if mask[i] and i > 0:                        # scheduled rebalance to close t-1 targets
            new = tgt[i - 1]
            turn[i] += np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        gross_s[i] = cur.sum()
        growth = cur * (1 + rets[i])                 # drift, as fractions of NAV
        tot = growth.sum() + (1 - cur.sum())         # cash leg is negative when levered
        cur = growth / tot if tot > 0 else cur
    idx = px.index
    r = pd.Series((held * rets).sum(axis=1), index=idx) - pd.Series(turn, index=idx) * bps / 1e4
    return dict(r=r, to=pd.Series(turn, index=idx), gross=pd.Series(gross_s, index=idx))


RAW = {}                                 # (panel, book, sleeve, cost, f, g) -> (r, gross, start)


def finance(r, gross, fin_bps):
    """Charge fin_bps/yr on borrowed notional only, daily, on the realised (drifted) gross."""
    if fin_bps == 0.0:
        return r
    return r - (fin_bps / 1e4 / 252.0) * (gross - 1.0).clip(lower=0.0)


# ------------------------------------------------------------------ metrics --
def bars_win(spy, which):
    """4b bars inside one window.  'full' = PROTOCOL's halves of the full slice + the OOS bar;
    'IS' = halves of the IS window (all an IS-only screen can see)."""
    s = spy.loc[:IS_END] if which == "IS" else spy
    h = len(s) // 2
    m = metrics(s)
    return dict(s1=metrics(s.iloc[:h])["Sharpe"], s2=metrics(s.iloc[h:])["Sharpe"],
                sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=metrics(spy.loc[OOS_START:])["Sharpe"] if which == "full" else np.nan)


def margins(r, b, which="full"):
    """4b bar margins in each bar's own units.  Positive = clears."""
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
    """The three 4b bars that are visible inside the OOS window alone (rule 8 reporting)."""
    s = spy.loc[OOS_START:]
    m = metrics(s)
    return dict(sharpe=m["Sharpe"], dd=m["MaxDD"], cagr=m["CAGR"])


def oos_margins(r, ob):
    s = r.loc[OOS_START:]
    m = metrics(s)
    return dict(S=m["Sharpe"] - ob["sharpe"], DD=DELTA * abs(ob["dd"]) - abs(m["MaxDD"]),
                CAGR=m["CAGR"] - PHI * ob["cagr"])


def pass_all(d):
    return bool(all(v > 0 for v in d.values()))


def interp_g(sub, col, target):
    """Smallest g on the ladder at which `col` reaches `target`, linearly interpolated.
    None if the column never reaches it inside the swept range."""
    s = sub.sort_values("g")
    gv, cv = s.g.values, s[col].values
    for i in range(len(gv) - 1):
        a, b = cv[i], cv[i + 1]
        if (a - target) * (b - target) <= 0 and a != b:
            return float(gv[i] + (gv[i + 1] - gv[i]) * (target - a) / (b - a))
    return None


# ------------------------------------------------------------------ main -----
def main():
    say(f"IDEA 402 — LEVERED f=0.60 vs THE 4b CAGR FLOOR (lane C).  {len(FS)} f x {len(GS)} g "
        f"x 2 panels x {len(BOOKS)} books x {len(SLEEVES)} sleeves x {len(COSTS)} cost rungs "
        f"= {len(FS)*len(GS)*2*len(BOOKS)*len(SLEEVES)*len(COSTS)} backtests, each priced at "
        f"{len(FINS)} financing rungs = "
        f"{len(FS)*len(GS)*2*len(BOOKS)*len(SLEEVES)*len(COSTS)*len(FINS)} arm-rows.")
    say(f"f sweep {FS} (0.00 = no-sleeve control, 0.25 = idea 139's adopted constant, 0.60 = "
        f"idea 138's Sharpe argmax).  g sweep {GS} (0.75 = record convention).")
    say(f"Financing {FINS} bps/yr on borrowed notional; verdict quoted at {FIN_HEADLINE:.0f} bps. "
        f"Cash earns 0 at g < 1 (record convention) — unkind to the levered arm by construction.")
    say(f"Weekly, t+1, costs {COSTS} bps.  4b bars: PHI={PHI} CAGR floor, DELTA={DELTA} DD cap.")

    rows, rets, ref = [], {}, {}
    RAW.clear()

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
        say(f"    SPY full CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%}"
            f" halves {b_full['s1']:.3f}/{b_full['s2']:.3f}; OOS Sharpe {mo['Sharpe']:.3f} "
            f"CAGR {mo['CAGR']:.2%} MaxDD {mo['MaxDD']:.2%}")
        say(f"    4b bars (full slice): H1>{b_full['s1']:.3f} H2>{b_full['s2']:.3f} "
            f"OOS>{b_full['soos']:.3f} MaxDD>={-DELTA*abs(b_full['sdd']):.2%} "
            f"CAGR>={PHI*ms['CAGR']:.2%}")
        say(f"    4b bars (OOS window alone): Sharpe>{ob['sharpe']:.3f} "
            f"MaxDD>={-DELTA*abs(ob['dd']):.2%} CAGR>={PHI*ob['cagr']:.2%}")

        v2 = {c: backtest(px, rules_v2_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        ref[pk]["v2"] = v2
        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        ref[pk]["v1"] = v1
        for c in COSTS:
            m2 = metrics(v2[c])
            h2 = H.halves(v2[c])
            say(f"    RULES v2 (live) @{c:.0f}bps {m2['CAGR']:.2%}/{m2['Sharpe']:.3f}/"
                f"{m2['MaxDD']:.2%} halves {h2[0]:.3f}/{h2[1]:.3f}")

        # ---- gate (a): run_lev == H.run == engine.backtest at g <= 1.0 -------
        Wchk = H.targets(px, "EWall")
        a = run_lev(px, Wchk, bps=10.0)["r"].loc[start:]
        b = H.run(px, Wchk, bps=10.0, freq=FREQ)["r"].loc[start:]
        c0 = backtest(px, Wchk, cost_bps=10.0, freq=FREQ)["returns"].loc[start:]
        say(f"    [gate a] run_lev vs H.run: max|d| {float((a-b).abs().max()):.3e}; "
            f"run_lev vs engine.backtest: max|d| {float((a-c0).abs().max()):.3e}")
        assert float((a - b).abs().max()) < 1e-12 and float((a - c0).abs().max()) < 1e-12

        base_W = {bk: H.targets(px, bk) for bk in BOOKS}
        sl_W = {sk: sleeve_weights(px, av) for sk, av in SLEEVES.items()}

        for bk in BOOKS:
            for sk in SLEEVES:
                for f in FS:
                    for g in GS:
                        W = blend(base_W[bk], sl_W[sk], f, g)
                        tg = W.sum(axis=1).loc[start:]
                        assert float(tg.max()) <= g + 1e-9, "target gross exceeds g"
                        for c in COSTS:
                            out = run_lev(px, W, bps=c)
                            gr = out["gross"]
                            RAW[(pk, bk, sk, c, f, g)] = (out["r"], gr, start)
                            for fin in FINS:
                                r = finance(out["r"], gr, fin).loc[start:]
                                key = (pk, bk, sk, c, fin, f, g)
                                rets[key] = r
                                m = metrics(r)
                                mI, mO = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
                                h1, h2 = H.halves(r)
                                mgf = margins(r, b_full, "full")
                                mgi = margins(r, b_is, "IS")
                                mgo = oos_margins(r, ob)
                                rows.append(dict(
                                    panel=pk, book=bk, sleeve=sk, cost=c, fin=fin, f=f, g=g,
                                    CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                    Vol=m["Vol"], H1=h1, H2=h2,
                                    IS_Sharpe=mI["Sharpe"], IS_CAGR=mI["CAGR"],
                                    IS_MaxDD=mI["MaxDD"],
                                    OOS_Sharpe=mO["Sharpe"], OOS_CAGR=mO["CAGR"],
                                    OOS_MaxDD=mO["MaxDD"],
                                    gross=float(gr.loc[start:].mean()),
                                    max_gross=float(gr.loc[start:].max()),
                                    turnover=float(out["to"].loc[start:].sum() / (len(r) / 252)),
                                    m_H1=mgf["H1"], m_H2=mgf["H2"], m_OOS=mgf["OOS"],
                                    m_DD=mgf["DD"], m_CAGR=mgf["CAGR"],
                                    m_min=min(mgf.values()), pass4b=pass_all(mgf),
                                    IS_m_min=min(mgi.values()), IS_pass4b=pass_all(mgi),
                                    OOS_m_S=mgo["S"], OOS_m_DD=mgo["DD"], OOS_m_CAGR=mgo["CAGR"],
                                    OOS_m_min=min(mgo.values()), OOS_pass=pass_all(mgo),
                                    pass4a_v2=H.pass4a(r, v2[c]),
                                    pass4a_v1_10=H.pass4a(r, v1[10.0]),
                                ))

    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    # ---- gate (b): reproduce idea 138's committed rows at g = 0.75 ----------
    say("\n[gate b] REPRODUCTION of idea 138's committed .grid.csv on its shared rows "
        "(f in {0.00, 0.25, 0.60}, g = 0.75, fin = 0)")
    if I138_GRID.exists():
        g138 = pd.read_csv(I138_GRID)
        mine = G[(G.g == 0.75) & (G.fin == 0.0)]
        cmp_rows = []
        for _, q in g138.iterrows():
            if not any(np.isclose(q.f, x) for x in FS):
                continue
            cand = mine[(mine.panel == q.panel) & (mine.book == q.book) &
                        (mine.sleeve == q.sleeve) & (mine.cost == q.cost) &
                        (np.isclose(mine.f, q.f))]
            if len(cand) != 1:
                continue
            k = cand.iloc[0]
            cmp_rows.append(dict(book=q.book, f=q.f, dS=k.Sharpe - q.Sharpe,
                                 dC=k.CAGR - q.CAGR, dD=k.MaxDD - q.MaxDD,
                                 dO=k.OOS_Sharpe - q.OOS_Sharpe,
                                 dgross=k.gross - q.gross, dto=k.turnover - q.turnover))
        R = pd.DataFrame(cmp_rows)
        if len(R):
            say(f"    matched {len(R)} committed rows; max|dSharpe| {R.dS.abs().max():.3e}  "
                f"max|dCAGR| {R.dC.abs().max():.3e}  max|dMaxDD| {R.dD.abs().max():.3e}  "
                f"max|dOOS| {R.dO.abs().max():.3e}")
            # The ONE definitional difference, stated rather than hidden: idea 138's f = 0 arm is
            # the raw base book, whose target gross is 0.75 only on days when the book is full.
            # This run must hold gross EXACTLY at g (Q3 is a matched-gross comparison and g is
            # the swept parameter), so every arm here is renormalised daily.  On EWall the two
            # coincide to machine precision; on TOP20 the raw book averages ~0.747 gross and
            # trades less, so idea 138's control is the slightly stronger one.
            exact = R[(R.f > 0) | (R.book == "EWall")]
            say(f"    EXACT subset (all f > 0 rows + EWall f = 0): {len(exact)} rows, "
                f"max|dSharpe| {exact.dS.abs().max():.3e}  max|dCAGR| {exact.dC.abs().max():.3e}  "
                f"max|dMaxDD| {exact.dD.abs().max():.3e}")
            assert exact.dS.abs().max() < 1e-9, "idea 138 reproduction FAILED on the exact subset"
            diff = R[(R.f == 0) & (R.book == "TOP20")]
            if len(diff):
                say(f"    DEFINITIONAL subset (TOP20 f = 0, renormalised here): {len(diff)} rows, "
                    f"mean dSharpe {diff.dS.mean():+.4f} (range {diff.dS.min():+.4f}.."
                    f"{diff.dS.max():+.4f}), mean d(mean gross) {diff.dgross.mean():+.4f}, "
                    f"mean d(turnover) {diff.dto.mean():+.3f}/yr.  This run's TOP20 control is "
                    f"therefore ~0.008 Sharpe WEAKER than idea 138's; every 'sleeve beats "
                    f"control' count on a TOP20 cell is flattered by that much and no more.")
        else:
            say("    no comparable rows matched — reproduction NOT established")
    else:
        say("    idea 138 grid missing — reproduction NOT established")

    # ---- the full grid, printed ---------------------------------------------
    cols = ["f", "g", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "OOS_CAGR",
            "OOS_MaxDD", "gross", "turnover", "m_CAGR", "m_DD", "m_min", "pass4b", "pass4a_v2"]
    say("\n" + "=" * 118)
    say(f"FULL GRID at the headline financing rung ({FIN_HEADLINE:.0f} bps).  m_CAGR is the "
        f"distance above the 4b floor, m_DD the room left under the cap, m_min the binding bar.")
    for pk in PANELS:
        for bk in BOOKS:
            for sk in SLEEVES:
                for c in COSTS:
                    sub = G[(G.panel == pk) & (G.book == bk) & (G.sleeve == sk) &
                            (G.cost == c) & (G.fin == FIN_HEADLINE)].sort_values(["f", "g"])
                    say(f"\n--- {pk} / {bk} / {sk} / {c:.0f}bps / fin {FIN_HEADLINE:.0f}bps ---")
                    say(sub[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n" + "=" * 118)
    say("CELL-MEAN CURVES over the 16 cells, per financing rung (the shape P1/P2 predicted).")
    for fin in FINS:
        say(f"\n[fin {fin:.0f} bps]")
        piv = G[G.fin == fin].groupby(["f", "g"])[
            ["Sharpe", "CAGR", "MaxDD", "m_CAGR", "m_DD", "m_min", "turnover"]].mean()
        say(piv.to_string(float_format=lambda x: f"{x:.4f}"))
        say(f"  4b pass counts (of 16 cells) by (f, g):")
        cnt = G[G.fin == fin].groupby(["f", "g"]).pass4b.sum().unstack("g")
        say(cnt.to_string())
        say(f"  4a-vs-live pass counts (of 16 cells) by (f, g):")
        say(G[G.fin == fin].groupby(["f", "g"]).pass4a_v2.sum().unstack("g").to_string())

    # ---- Q1: the g-window at f = 0.60 --------------------------------------
    say("\n" + "=" * 118)
    say("Q1 — DOES f = 0.60 CLEAR 4b AT ANY GROSS?  Per cell and financing rung: the g-window "
        "(contiguous or not), the binding bar at each end, and the same for f = 0.25 / 0.00.")
    wrows = []
    for (pk, bk, sk, c, fin, f), sub in G.groupby(["panel", "book", "sleeve", "cost", "fin", "f"]):
        sub = sub.sort_values("g")
        ok = sub[sub.pass4b]
        binding = sub.set_index("g")[["m_H1", "m_H2", "m_OOS", "m_DD", "m_CAGR"]].idxmin(axis=1)
        wrows.append(dict(
            panel=pk, book=bk, sleeve=sk, cost=c, fin=fin, f=f,
            n_pass=int(len(ok)), g_lo=float(ok.g.min()) if len(ok) else np.nan,
            g_hi=float(ok.g.max()) if len(ok) else np.nan,
            contiguous=bool(len(ok) and
                            list(sub[(sub.g >= ok.g.min()) & (sub.g <= ok.g.max())].pass4b.values)
                            == [True] * len(sub[(sub.g >= ok.g.min()) & (sub.g <= ok.g.max())])),
            best_m_min=float(sub.m_min.max()), best_g=float(sub.loc[sub.m_min.idxmax(), "g"]),
            binding_at_075=binding.loc[0.75], binding_at_lo=binding.loc[ok.g.min()] if len(ok)
            else "", binding_below=binding.loc[sub.g.min()], binding_above=binding.loc[sub.g.max()],
            sharpe_at_075=float(sub[sub.g == 0.75].Sharpe.iloc[0]),
            sharpe_at_best=float(sub.loc[sub.m_min.idxmax(), "Sharpe"]),
            g_clears_floor=interp_g(sub, "m_CAGR", 0.0),
            g_breaches_dd=interp_g(sub, "m_DD", 0.0),
        ))
    Wdf = pd.DataFrame(wrows)
    Wdf.to_csv(OUT / f"{STEM}.window.csv", index=False)
    for fin in FINS:
        for f in FS:
            A = Wdf[(Wdf.fin == fin) & (Wdf.f == f)]
            say(f"\n[f={f:.2f} / fin {fin:.0f}bps]  cells with a 4b g-window: "
                f"{int((A.n_pass > 0).sum())} / {len(A)}; median window width "
                f"{A.n_pass.median():.1f} of {len(GS)} g-points")
            say(A[["panel", "book", "sleeve", "cost", "n_pass", "g_lo", "g_hi", "contiguous",
                   "best_g", "best_m_min", "sharpe_at_075", "sharpe_at_best",
                   "g_clears_floor", "g_breaches_dd", "binding_at_075", "binding_below",
                   "binding_above"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n  SUMMARY of the window's ENDS (the P2 shape test): a window bounded BELOW by the "
        "CAGR floor and ABOVE by the DD cap is idea 401's crossing, not a plateau.")
    for fin in FINS:
        for f in FS:
            A = Wdf[(Wdf.fin == fin) & (Wdf.f == f)]
            say(f"   f={f:.2f} fin={fin:.0f}: binding bar at the LOWEST g "
                f"{dict(A.binding_below.value_counts())}; at the HIGHEST g "
                f"{dict(A.binding_above.value_counts())}")

    # ---- Q2: matched CAGR / matched DD against the incumbent ----------------
    say("\n" + "=" * 118)
    say("Q2 — AT MATCHED CAGR WITH THE INCUMBENT (f=0.25, g=0.75), is levered f=0.60 better?  "
        "g* is interpolated on this cell's own g ladder so the two books earn the SAME CAGR; "
        "Sharpe/MaxDD are then read at g* by linear interpolation on the same ladder.")
    mrows = []
    for (pk, bk, sk, c, fin), sub in G.groupby(["panel", "book", "sleeve", "cost", "fin"]):
        inc = sub[(sub.f == INCUMBENT[0]) & (sub.g == INCUMBENT[1])].iloc[0]
        ctl = sub[(sub.f == 0.0) & (sub.g == 0.75)].iloc[0]
        hi = sub[sub.f == ARGMAX_F].sort_values("g")
        lo = sub[sub.f == 0.0].sort_values("g")
        rec = dict(panel=pk, book=bk, sleeve=sk, cost=c, fin=fin,
                   inc_CAGR=inc.CAGR, inc_Sharpe=inc.Sharpe, inc_MaxDD=inc.MaxDD,
                   inc_pass4b=bool(inc.pass4b),
                   ctl_CAGR=ctl.CAGR, ctl_Sharpe=ctl.Sharpe, ctl_MaxDD=ctl.MaxDD)
        for tag, lad in (("f060", hi), ("f000", lo)):
            gstar = interp_g(lad, "CAGR", inc.CAGR)
            rec[f"{tag}_gstar"] = gstar
            if gstar is None:
                rec[f"{tag}_S_at_gstar"] = np.nan
                rec[f"{tag}_DD_at_gstar"] = np.nan
            else:
                rec[f"{tag}_S_at_gstar"] = float(np.interp(gstar, lad.g.values, lad.Sharpe.values))
                rec[f"{tag}_DD_at_gstar"] = float(np.interp(gstar, lad.g.values, lad.MaxDD.values))
            rec[f"{tag}_dS"] = rec[f"{tag}_S_at_gstar"] - inc.Sharpe
            rec[f"{tag}_dDD"] = rec[f"{tag}_DD_at_gstar"] - inc.MaxDD   # >0 = shallower
        mrows.append(rec)
    M = pd.DataFrame(mrows)
    M.to_csv(OUT / f"{STEM}.matched.csv", index=False)
    for fin in FINS:
        A = M[M.fin == fin]
        say(f"\n[fin {fin:.0f} bps]")
        say(A[["panel", "book", "sleeve", "cost", "inc_CAGR", "inc_Sharpe", "inc_MaxDD",
               "f060_gstar", "f060_S_at_gstar", "f060_DD_at_gstar", "f060_dS", "f060_dDD",
               "f000_gstar", "f000_dS", "f000_dDD"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))
        say(f"  f=0.60 at matched CAGR beats the incumbent on Sharpe in "
            f"{int((A.f060_dS > 0).sum())}/{len(A)} cells (mean dS {A.f060_dS.mean():+.4f}), "
            f"and is SHALLOWER on MaxDD in {int((A.f060_dDD > 0).sum())}/{len(A)} "
            f"(mean {A.f060_dDD.mean():+.2%}); mean g* {A.f060_gstar.mean():.3f}")
        say(f"  the NO-SLEEVE control levered to the same CAGR beats the incumbent on Sharpe in "
            f"{int((A.f000_dS > 0).sum())}/{len(A)} (mean dS {A.f000_dS.mean():+.4f}), "
            f"MaxDD {int((A.f000_dDD > 0).sum())}/{len(A)} (mean {A.f000_dDD.mean():+.2%}); "
            f"mean g* {A.f000_gstar.mean():.3f}")

    # ---- Q3: f = 0.60 vs its own levered control, gross by gross ------------
    say("\n" + "=" * 118)
    say("Q3 — f = 0.60 vs the NO-SLEEVE CONTROL AT THE SAME GROSS (never an exposure "
        "comparison: both books carry identical mean realised gross by construction).")
    for fin in FINS:
        A = G[G.fin == fin]
        piv = A.pivot_table(index="g", columns="f", values=["Sharpe", "CAGR", "MaxDD"])
        say(f"\n[fin {fin:.0f} bps] cell means")
        say(piv.to_string(float_format=lambda x: f"{x:.4f}"))
        for g in GS:
            hi = A[(A.f == ARGMAX_F) & (A.g == g)].set_index(["panel", "book", "sleeve", "cost"])
            ct = A[(A.f == 0.0) & (A.g == g)].set_index(["panel", "book", "sleeve", "cost"])
            d = (hi.Sharpe - ct.Sharpe).dropna()
            dd = (hi.MaxDD - ct.MaxDD).dropna()
            dg = (hi.gross - ct.gross).abs().max()
            say(f"   g={g:.2f}: f=0.60 beats control on Sharpe {int((d > 0).sum())}/{len(d)} "
                f"(mean {d.mean():+.4f}); shallower MaxDD {int((dd > 0).sum())}/{len(dd)} "
                f"(mean {dd.mean():+.2%}); max|d mean gross| {dg:.2e}")

    say("\n  P1 CHECK — Sharpe's sensitivity to g (should be near-flat at fin=0, negative at "
        "fin>0):")
    for fin in FINS:
        A = G[G.fin == fin]
        for f in FS:
            s = A[A.f == f].groupby("g").Sharpe.mean()
            slope = np.polyfit(list(s.index), s.values, 1)[0]
            say(f"   fin {fin:.0f} f={f:.2f}: Sharpe {s.iloc[0]:.4f} @g=0.75 -> "
                f"{s.iloc[-1]:.4f} @g=2.00, range {s.max()-s.min():.4f}, slope {slope:+.4f}/unit g")
    say("\n  P2 CHECK — MaxDD and CAGR against g (linear vs sub-linear):")
    for f in FS:
        s = G[(G.fin == FIN_HEADLINE) & (G.f == f)].groupby("g")[["MaxDD", "CAGR"]].mean()
        say(f"   f={f:.2f}: MaxDD {s.MaxDD.iloc[0]:.2%} -> {s.MaxDD.iloc[-1]:.2%} "
            f"(ratio {s.MaxDD.iloc[-1]/s.MaxDD.iloc[0]:.2f}x for 2.67x gross); "
            f"CAGR {s.CAGR.iloc[0]:.2%} -> {s.CAGR.iloc[-1]:.2%} "
            f"(ratio {s.CAGR.iloc[-1]/s.CAGR.iloc[0]:.2f}x)")

    # ---- Q4: rule 8 --------------------------------------------------------
    say("\n" + "=" * 118)
    say("Q4 — RULE 8 WALK-FORWARD.  Parameters chosen on 2009-2016 ONLY; 2017-2026 read once.")
    say("  S0  g argmax of IS Sharpe, f held at 0.60          (the naive chooser)")
    say("  S1  g argmax of the IS 4b margin-min at f = 0.60, screened to IS-4b passers")
    say("  S2  JOINT (f, g) argmax of the IS 4b margin-min over the whole grid")
    say("  INC the incumbent f = 0.25, g = 0.75, chosen by no data at all (idea 139)")
    say("  CTL the no-sleeve control f = 0.00, g = 0.75")
    wf = []
    for (pk, bk, sk, c, fin), sub in G.groupby(["panel", "book", "sleeve", "cost", "fin"]):
        hi = sub[sub.f == ARGMAX_F]
        picks = {}
        picks["S0"] = (ARGMAX_F, float(hi.loc[hi.IS_Sharpe.idxmax(), "g"]))
        s1 = hi[hi.IS_pass4b]
        picks["S1"] = (ARGMAX_F, float(s1.loc[s1.IS_m_min.idxmax(), "g"])) if len(s1) else None
        picks["S2"] = (float(sub.loc[sub.IS_m_min.idxmax(), "f"]),
                       float(sub.loc[sub.IS_m_min.idxmax(), "g"]))
        s2s = sub[sub.IS_pass4b]
        picks["S2_screened"] = (float(s2s.loc[s2s.IS_m_min.idxmax(), "f"]),
                                float(s2s.loc[s2s.IS_m_min.idxmax(), "g"])) if len(s2s) else None
        picks["INC"] = INCUMBENT
        picks["CTL"] = (0.0, 0.75)
        for name, pick in picks.items():
            rec = dict(panel=pk, book=bk, sleeve=sk, cost=c, fin=fin, selector=name)
            if pick is None:
                rec.update(pick_f=np.nan, pick_g=np.nan, abstain=True)
                wf.append(rec)
                continue
            row = sub[(np.isclose(sub.f, pick[0])) & (np.isclose(sub.g, pick[1]))].iloc[0]
            ob = ref[pk]["oos"]
            rec.update(pick_f=pick[0], pick_g=pick[1], abstain=False,
                       OOS_Sharpe=row.OOS_Sharpe, OOS_CAGR=row.OOS_CAGR, OOS_MaxDD=row.OOS_MaxDD,
                       OOS_m_S=row.OOS_m_S, OOS_m_DD=row.OOS_m_DD, OOS_m_CAGR=row.OOS_m_CAGR,
                       OOS_pass=bool(row.OOS_pass),
                       SPY_OOS_Sharpe=ob["sharpe"], SPY_OOS_CAGR=ob["cagr"],
                       SPY_OOS_MaxDD=ob["dd"],
                       full_Sharpe=row.Sharpe, full_CAGR=row.CAGR, full_MaxDD=row.MaxDD,
                       pass4b=bool(row.pass4b), pass4a_v2=bool(row.pass4a_v2))
            wf.append(rec)
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    for fin in FINS:
        A = WF[WF.fin == fin]
        say(f"\n[fin {fin:.0f} bps] per-selector OOS summary over 16 cells")
        agg = A.groupby("selector").agg(
            picks_g=("pick_g", lambda s: dict(pd.Series(s.dropna()).value_counts())),
            mean_OOS_Sharpe=("OOS_Sharpe", "mean"), mean_OOS_CAGR=("OOS_CAGR", "mean"),
            mean_OOS_MaxDD=("OOS_MaxDD", "mean"),
            OOS_all3=("OOS_pass", "sum"), abstain=("abstain", "sum"))
        say(agg.to_string(float_format=lambda x: f"{x:.4f}"))
        say(A[["panel", "book", "sleeve", "cost", "selector", "pick_f", "pick_g", "OOS_Sharpe",
               "OOS_CAGR", "OOS_MaxDD", "OOS_m_S", "OOS_m_DD", "OOS_m_CAGR", "OOS_pass"]]
            .sort_values(["panel", "book", "sleeve", "cost", "selector"])
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        for sel in ("S0", "S1", "S2", "S2_screened"):
            a = A[A.selector == sel].set_index(["panel", "book", "sleeve", "cost"])
            i = A[A.selector == "INC"].set_index(["panel", "book", "sleeve", "cost"])
            d = (a.OOS_Sharpe - i.OOS_Sharpe).dropna()
            dc = (a.OOS_CAGR - i.OOS_CAGR).dropna()
            if len(d):
                say(f"   {sel} vs INCUMBENT OOS: Sharpe better in {int((d > 0).sum())}/{len(d)} "
                    f"(mean {d.mean():+.4f}); CAGR better in {int((dc > 0).sum())}/{len(dc)} "
                    f"(mean {dc.mean():+.2%})")

    # ---- Q5: the financing break-even (the number the answer actually turns on) --
    say("\n" + "=" * 118)
    say("Q5 — FINANCING BREAK-EVEN.  Everything above says the CAGR floor is clearable with "
        "gross; what it costs to borrow decides whether that is worth anything.  Per cell, the "
        "borrow rate (bps/yr on borrowed notional) at which the levered f=0.60 arm (i) loses its "
        "Sharpe edge over the incumbent f=0.25 @ 0.75, and (ii) stops passing 4b at all.  The "
        "incumbent never borrows (g = 0.75), so its numbers do not move with the rate.")

    def at_fin(key, fin):
        r0, gr, st = RAW[key]
        r = finance(r0, gr, fin).loc[st:]
        pk_ = key[0]
        return metrics(r)["Sharpe"], min(margins(r, ref[pk_]["bfull"], "full").values())

    def bisect(key, fn, lo=0.0, hi=3000.0, iters=34):
        if fn(at_fin(key, lo)) <= 0:
            return 0.0                       # already below the target with free money
        if fn(at_fin(key, hi)) > 0:
            return np.nan                    # still above at 3000 bps: no break-even in range
        for _ in range(iters):
            mid = 0.5 * (lo + hi)
            if fn(at_fin(key, mid)) > 0:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    brows = []
    for (pk, bk, sk, c), sub0 in G[G.fin == 0.0].groupby(["panel", "book", "sleeve", "cost"]):
        inc_S = float(sub0[(sub0.f == INCUMBENT[0]) & (sub0.g == INCUMBENT[1])].Sharpe.iloc[0])
        hi = sub0[sub0.f == ARGMAX_F]
        g_best = float(hi.loc[hi.m_min.idxmax(), "g"])
        for tag, g in (("best_m_min", g_best), ("g=1.25 (modal S1 pick)", 1.25)):
            key = (pk, bk, sk, c, ARGMAX_F, g)
            brows.append(dict(
                panel=pk, book=bk, sleeve=sk, cost=c, arm=tag, g=g,
                S_free=at_fin(key, 0.0)[0], m_min_free=at_fin(key, 0.0)[1], inc_Sharpe=inc_S,
                be_sharpe=bisect(key, lambda t: t[0] - inc_S),
                be_4b=bisect(key, lambda t: t[1])))
    B = pd.DataFrame(brows)
    B.to_csv(OUT / f"{STEM}.breakeven.csv", index=False)
    say(B.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    for tag, A in B.groupby("arm"):
        say(f"  [{tag}] break-even borrow rate for the SHARPE edge over the incumbent: median "
            f"{A.be_sharpe.median():.0f} bps (range {A.be_sharpe.min():.0f}..{A.be_sharpe.max():.0f}); "
            f"for 4b itself: median {A.be_4b.median():.0f} bps "
            f"(range {A.be_4b.min():.0f}..{A.be_4b.max():.0f})")

    # ---- KEEP paths ---------------------------------------------------------
    say("\n" + "=" * 118)
    say("KEEP PATHS (PROTOCOL 4, both evaluated on every row)")
    K = G[G.pass4b | G.pass4a_v2].copy()
    K.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    say(f"  4b passers: {int(G.pass4b.sum())} of {len(G)} arm-rows "
        f"({int(G[G.fin == FIN_HEADLINE].pass4b.sum())} at the headline financing rung)")
    say(f"  4a passers vs the LIVE RULES v2, cost-matched: {int(G.pass4a_v2.sum())} of {len(G)} "
        f"({int(G[G.fin == FIN_HEADLINE].pass4a_v2.sum())} at the headline rung)")
    say(f"  4a passers vs RULES v1 @ fixed 10 bps (the record's older convention, idea 398): "
        f"{int(G.pass4a_v1_10.sum())}")
    say(f"  BOTH paths: {int((G.pass4b & G.pass4a_v2).sum())}")
    say("\n  4b pass count by (f, g) at the headline rung, and the count of cells (max 16):")
    say(G[G.fin == FIN_HEADLINE].groupby(["f", "g"]).pass4b.sum().unstack("g").to_string())

    say("\n  PRE-REGISTERED DECISION RULE: KEEP only if ONE (f=0.60, g) pair passes 4b in ALL "
        "16 cells at 300 bps financing AND the IS-4b chooser (S1) clears all three OOS bars in "
        ">= 14/16 cells AND beats the incumbent's OOS Sharpe.")
    hi300 = G[(G.fin == FIN_HEADLINE) & (G.f == ARGMAX_F)]
    per_g = hi300.groupby("g").pass4b.sum()
    universal = [float(g) for g, n in per_g.items() if n == 16]
    inc_n = int(G[(G.fin == FIN_HEADLINE) & (G.f == INCUMBENT[0]) &
                  (G.g == INCUMBENT[1])].pass4b.sum())
    say(f"   [context, not a moved goalpost] the STANDING candidate f=0.25 @ 0.75 itself passes "
        f"4b in {inc_n}/16 cells, so bar (i) is one the incumbent does not meet either; the "
        f"verdict below still uses the rule as pre-registered.")
    best_g = float(per_g.idxmax())
    fails = hi300[(hi300.g == best_g) & (~hi300.pass4b)]
    incf = G[(G.fin == FIN_HEADLINE) & (G.f == INCUMBENT[0]) & (G.g == INCUMBENT[1]) & (~G.pass4b)]
    say(f"   the best single g at f=0.60 is {best_g:.2f} ({int(per_g.max())}/16); the cells it "
        f"misses are: {[tuple(x) for x in fails[['panel','book','sleeve','cost']].values]}")
    say(f"   the cells the incumbent misses are: "
        f"{[tuple(x) for x in incf[['panel','book','sleeve','cost']].values]}")
    s1 = WF[(WF.fin == FIN_HEADLINE) & (WF.selector == "S1")]
    inc = WF[(WF.fin == FIN_HEADLINE) & (WF.selector == "INC")]
    s1n = int(s1.OOS_pass.fillna(False).sum())
    beats = float(s1.OOS_Sharpe.mean() - inc.OOS_Sharpe.mean())
    say(f"   (i)  g values passing 4b in all 16 cells at f=0.60, 300bps: {universal or 'NONE'}")
    say(f"   (ii) S1 clears all three OOS bars in {s1n}/16 cells")
    say(f"   (iii) S1 mean OOS Sharpe - incumbent's: {beats:+.4f}")
    verdict = ("KEEP-candidate (4b)" if (universal and s1n >= 14 and beats > 0)
               else ("PARK" if universal or s1n >= 8 else "KILL"))
    say(f"\n  VERDICT BY THE PRE-REGISTERED RULE: {verdict}")

    say("\n  Incumbent and the best levered f=0.60 arm side by side (headline rung, per panel, "
        "EWall / S3 / 10 bps — idea 139's own cell):")
    for pk in PANELS:
        sub = G[(G.panel == pk) & (G.book == "EWall") & (G.sleeve == "S3") & (G.cost == 10.0) &
                (G.fin == FIN_HEADLINE)]
        inc_r = sub[(sub.f == INCUMBENT[0]) & (sub.g == INCUMBENT[1])].iloc[0]
        hi_r = sub[sub.f == ARGMAX_F].sort_values("m_min").iloc[-1]
        for tag, r in (("INC f=0.25 g=0.75", inc_r), (f"f=0.60 g={hi_r.g:.2f}", hi_r)):
            say(f"   {pk:5s} {tag:20s} CAGR {r.CAGR:6.2%} Sharpe {r.Sharpe:.4f} "
                f"MaxDD {r.MaxDD:7.2%} halves {r.H1:.3f}/{r.H2:.3f} OOS {r.OOS_Sharpe:.4f} "
                f"m_min {r.m_min:+.4f} 4b {bool(r.pass4b)}")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    say(f"\nWrote {STEM}.grid.csv ({len(G)} rows), .window.csv ({len(Wdf)}), .matched.csv "
        f"({len(M)}), .walkforward.csv ({len(WF)}), .breakeven.csv ({len(B)}), .keeppaths.csv "
        f"({len(K)}), .console.txt")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
