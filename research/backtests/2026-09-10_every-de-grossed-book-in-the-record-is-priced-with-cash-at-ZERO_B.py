#!/usr/bin/env python3
"""QUEUE idea 406 — every-de-grossed-book-in-the-record-is-priced-with-cash-at-ZERO
(lane B, 2026-09-10).

PRE-REGISTERED QUESTION (verbatim from QUEUE.md idea 406, written before any number here
was read)
    "idea 402 charged 300 bps to borrow while crediting 0 on the 25% cash the live book
     holds, the record's standing convention.  Re-price the committed 4b candidates
     crediting cash at a flat 150 bps (and at 300) and report how many 4b margins change
     sign; the de-grossed books are the ones the convention taxes.  Max 2 params
     (credit rate, book)."

WHY IT MATTERS
    RULES v2 runs at gross 0.75 and de-grosses further whenever the 200d band gates a name
    out, so the live book sits in cash a quarter to a half of the time.  PROTOCOL 4b judges
    it against SPY, which is 100% invested by construction.  If cash earns nothing in the
    simulator but ~150 bps in a real sweep account, then every 4b margin the record has ever
    published on a de-grossed book is understated, and the CAGR floor — the bar the record
    keeps failing by tens of bps — is understated by exactly (1 - gross) x credit.  That is
    an accounting convention deciding KEEP verdicts, not a finding about markets.

WHAT IS TESTED (fixed in advance)
    Q1  EXACT re-pricing.  Re-simulate idea 402's committed family with cash credited inside
        the drift loop (not bolted on afterwards) at 0 / 150 / 300 bps, and count how many of
        the 4b bar margins change SIGN, per bar and per book.
    Q2  The rf CONSISTENCY horn the queue does not state.  engine.metrics computes Sharpe at
        rf = 0.  Crediting cash at c while leaving rf = 0 pays the book a risk-free return and
        then counts it as alpha.  Three treatments are therefore priced, all reported:
            C0  cash 0,  rf 0   — the record's standing convention (idea 402's).
            C1  cash c,  rf 0   — the queue's literal ask.
            C2  cash c,  rf c   — the internally consistent one (excess-return Sharpe for
                                  the arm AND for SPY).  CAGR floor and DD cap are
                                  total-return bars and are identical under C1 and C2.
        C1 can only move margins one way (up).  C2 can move the Sharpe legs DOWN, because a
        low-vol de-grossed book earns more of its rf=0 Sharpe from the risk-free leg than
        SPY does.  Which way the record's verdicts move is the actual question.
    Q3  RECORD-WIDE CENSUS.  Every committed .csv in research/backtests that publishes the
        full 4b margin vector AND a realised `gross` column (18 files, 26,207 rows) is
        re-read under the first-order credit  dCAGR = (1-gross)*c,  dSharpe = (1-gross)*c/Vol,
        and the flip counts are reported.  The first-order form is VALIDATED against Q1's
        exact re-simulation and its error is printed, not assumed.
    Q4  Rule 8.  (f, g) chosen on 2009-2016 only under each treatment, 2017-2026 read once.
        Does the cash convention change the pick, and does the pick's OOS beat RULES v2 and
        SPY?  A convention that only moves in-sample margins is bookkeeping, not capital.
    Q5  Both KEEP paths on every row: 4a against the LIVE book (rules_v2_weights, cost- and
        credit-matched — the live book holds cash too, so 4a is nearly convention-free) and
        4b against SPY.

GRID (two tuned parameters, both swept, ALL points reported)
    param 1  credit c in {0, 150, 300} bps/yr, flat, on positive cash only.
    param 2  book = (f, g) from idea 402's committed family:
             f in {0.00, 0.25, 0.60}  (0.00 no-sleeve control, 0.25 the adopted constant,
                                       0.60 idea 138's Sharpe argmax)
             g in {0.40, 0.50, 0.60, 0.75, 0.85, 0.90, 1.00, 1.10, 1.25, 1.50, 1.75, 2.00}
             plus the two live books, RULES v2 and RULES v1, priced at the same rungs.
    REPORTED AXES, never selected on: panel {u56, broad} x base book {EWall, TOP20} x sleeve
    {S3 = TLT/GLD/UUP, S4 = TLT/GLD/DBC/UUP} x cost rung {10, 25} bps = 16 cells.

CONVENTIONS, stated not buried
    * Credit is paid on max(0, 1 - realised drifted gross), daily, at c/252.  NEGATIVE cash
      (g > 1) is left to idea 402's financing convention and is NOT credited here — this run
      does not re-open the borrow rate, so the levered arms carry fin = 0 and are reported as
      a control, never as a candidate.
    * The credit enters the drift renormalisation, so the reported numbers are exact, not a
      post-hoc addition.  At c = 0 the simulator is asserted equal to idea 402's committed
      .grid.csv on the shared rows.
    * A FLAT credit over 2009-2026 is wrong in both directions: 2009-2015 T-bills paid ~10
      bps, 2023-2026 ~500.  150/300 brackets the realised average, not the path.  No rate
      series is cached and the sandbox has no network.  This is the single largest caveat.
    * PROTOCOL 2 (10 bps, t+1, weekly) unchanged.  Nothing in RULES.md / scan.py / bot.py /
      baseline.py is touched.

PRE-REGISTERED PREDICTIONS (written before the main grid was read)
    P1  At g = 0.75 and c = 150 the CAGR-floor margin gains ~37.5 bps.  Committed m_CAGR
        values in this family sit in the tens of bps, so a MAJORITY of near-miss CAGR-floor
        failures flip to pass under C1.
    P2  The DD margin improves, but by well under the CAGR gain: cash only cushions the
        drawdown by the credit accrued during it (< 10 bps over a one-year episode).
    P3  Under C2 the Sharpe legs move DOWN for every de-grossed book, by roughly
        c*(1/sigma_SPY - g/sigma_book), which at sigma_book ~ 0.09, g = 0.75, sigma_SPY ~ 0.18
        is about -0.042 Sharpe at c = 150.  Some C0 passes therefore FAIL under C2.
    P4  Rule 8's pick is unchanged or nearly so, because the credit is close to a constant
        shift within a cell (gross barely varies across g at fixed g) and a constant shift
        cannot re-order an argmax.  Where it does move it moves toward LOWER g.
    P5  Net: the convention is a real tax on the CAGR floor and a real SUBSIDY on the Sharpe
        legs, and the two do not cancel — so "credit cash" is not a free upgrade to the
        record's verdicts.

DECISION RULE, pre-registered
    KEEP (4b) only if some (f, g) passes 4b in ALL 16 cells under C2 at c = 150 AND the
    rule-8 C2 pick's OOS clears all three OOS-visible bars and beats RULES v2 on OOS Sharpe.
    KEEP (4a) only if a row beats rules_v2_weights in BOTH halves with no worse MaxDD, at
    matched credit.  Anything weaker is PARK or KILL, and a convention finding with no book
    behind it is reported as an ANSWER with no KEEP.

CAVEATS carried, not buried
    * SURVIVORSHIP (idea 54): both panels are current constituents.
    * MaxDD is one number off one path (idea 321); the 4b DD cap turns on exactly it.
    * The census (Q3) is first-order and C1-only (its Sharpe leg needs a per-half vol the
      record does not publish).  C1 is the GENEROUS direction, so census flip counts are an
      UPPER bound on how much the convention buys.
    * Idea 126: t+1 only.  Idea 38: calendar-day index on both panels.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .flips.csv, .census.csv,
.walkforward.csv next to itself.  Modifies nothing.
"""
import glob
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-10_every-de-grossed-book-in-the-record-is-priced-with-cash-at-ZERO_B"
OUT = ROOT / "research" / "backtests"
I402_GRID = OUT / "2026-09-07_does-a-levered-f-060-book-clear-the-CAGR-floor_C.grid.csv"

FREQ = "W"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COSTS = [10.0, 25.0]
CREDITS = [0.0, 150.0, 300.0]            # tuned parameter 1 — all reported
PHI, DELTA = 0.70, 0.60                  # 4b CAGR floor / DD cap fractions of SPY
FS = [0.00, 0.25, 0.60]                  # tuned parameter 2a
GS = [0.40, 0.50, 0.60, 0.75, 0.85, 0.90, 1.00, 1.10, 1.25, 1.50, 1.75, 2.00]   # param 2b
SLEEVES = {"S3": ["TLT", "GLD", "UUP"], "S4": ["TLT", "GLD", "DBC", "UUP"]}
BOOKS = ["EWall", "TOP20"]
PANELS = ["u56", "broad"]
GROSS0, NTOP = 0.75, 20
BARS = ["H1", "H2", "OOS", "DD", "CAGR"]

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
    sub = px[assets]
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[assets] = (_vote_mom(sub) * _risk_parity(sub)).fillna(0.0)
    return out


def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def base_book(px, book):
    """Idea 94's ungated base books, verbatim (EWall and TOP20 at gross 0.75)."""
    if book == "EWall":
        e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
        return GROSS0 * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    rank = composite(px).rank(axis=1, ascending=False)
    return (rank <= NTOP).astype(float) * (GROSS0 / NTOP)


def blend(base_W, sl_W, f, g):
    raw = base_W if f == 0.0 else (1 - f) * base_W + f * sl_W
    return raw.mul((g / raw.sum(axis=1).replace(0, np.nan)).fillna(0.0), axis=0).fillna(0.0)


# ------------------------------------------- simulator with a CREDITED cash leg --
def run_cash(px, W, credit_bps=0.0, freq=FREQ):
    """Idea 402's run_lev with the cash leg paid credit_bps/yr on POSITIVE cash only.

    The credit enters the drift renormalisation, so weights, turnover and NAV are all
    consistent with a book that actually earns on its cash.  credit_bps = 0 reproduces
    engine.backtest / idea 402's run_lev exactly (asserted in main).

    Returns cost-free returns plus turnover, so both cost rungs come off one simulation
    (costs do not feed back into weights in this engine).
    """
    rets = px.pct_change().fillna(0.0).values
    tgt = W.reindex(px.index).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    crd = credit_bps / 1e4 / 252.0
    nrow, ncol = rets.shape
    cur = np.zeros(ncol)
    r = np.zeros(nrow)
    turn = np.zeros(nrow)
    gross_s = np.zeros(nrow)
    cash_s = np.zeros(nrow)
    for i in range(nrow):
        if mask[i] and i > 0:
            new = tgt[i - 1]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        gross_s[i] = cur.sum()
        cash = 1.0 - cur.sum()
        pay = cash * crd if cash > 0.0 else 0.0      # negative cash: idea 402's fin rung, not here
        cash_s[i] = max(cash, 0.0)
        growth = cur * (1 + rets[i])
        r[i] = growth.sum() - cur.sum() + pay
        tot = growth.sum() + cash + pay
        cur = growth / tot if tot > 0 else cur
    idx = px.index
    return dict(r=pd.Series(r, index=idx), to=pd.Series(turn, index=idx),
                gross=pd.Series(gross_s, index=idx), cash=pd.Series(cash_s, index=idx))


def net(sim, bps, start):
    return (sim["r"] - sim["to"] * bps / 1e4).loc[start:]


# ------------------------------------------------------------------ metrics --
def sharpe(r, rf=0.0):
    v = r.std() * np.sqrt(252)
    return (r.mean() * 252 - rf) / v if v else np.nan


def halves(r, rf=0.0):
    h = len(r) // 2
    return sharpe(r.iloc[:h], rf), sharpe(r.iloc[h:], rf)


def bars_win(spy, which, rf=0.0):
    s = spy.loc[:IS_END] if which == "IS" else spy
    h = len(s) // 2
    m = metrics(s)
    return dict(s1=sharpe(s.iloc[:h], rf), s2=sharpe(s.iloc[h:], rf), sdd=m["MaxDD"],
                scagr=m["CAGR"],
                soos=sharpe(spy.loc[OOS_START:], rf) if which == "full" else np.nan)


def margins(r, b, which="full", rf=0.0):
    s = r.loc[:IS_END] if which == "IS" else r
    h = len(s) // 2
    m = metrics(s)
    d = dict(H1=sharpe(s.iloc[:h], rf) - b["s1"], H2=sharpe(s.iloc[h:], rf) - b["s2"],
             DD=DELTA * abs(b["sdd"]) - abs(m["MaxDD"]), CAGR=m["CAGR"] - PHI * b["scagr"])
    if which == "full":
        d["OOS"] = sharpe(r.loc[OOS_START:], rf) - b["soos"]
    return d


def oos_bars(spy, rf=0.0):
    s = spy.loc[OOS_START:]
    m = metrics(s)
    return dict(sharpe=sharpe(s, rf), dd=m["MaxDD"], cagr=m["CAGR"])


def oos_margins(r, ob, rf=0.0):
    s = r.loc[OOS_START:]
    m = metrics(s)
    return dict(S=sharpe(s, rf) - ob["sharpe"], DD=DELTA * abs(ob["dd"]) - abs(m["MaxDD"]),
                CAGR=m["CAGR"] - PHI * ob["cagr"])


def pass4a(r, base, rf=0.0):
    h1, h2 = halves(r, rf)
    b1, b2 = halves(base, rf)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


# ------------------------------------------------------------------ main -----
def main():
    ncell = len(PANELS) * len(BOOKS) * len(SLEEVES) * len(COSTS)
    say(f"IDEA 406 — CASH AT ZERO IS A CONVENTION (lane B).  {len(FS)} f x {len(GS)} g x "
        f"{ncell} cells x {len(CREDITS)} credit rungs x 3 treatments (C0/C1/C2).")
    say(f"credit rungs {CREDITS} bps/yr on POSITIVE cash only; negative cash (g>1) keeps idea "
        f"402's financing convention at fin=0 and is a CONTROL, not a candidate.")
    say(f"Weekly, t+1, costs {COSTS} bps.  4b bars: PHI={PHI} CAGR floor, DELTA={DELTA} DD cap.")
    say("Treatments:  C0 cash 0 / rf 0 (record).  C1 cash c / rf 0 (queue's ask).  "
        "C2 cash c / rf c (consistent).  CAGR and DD bars identical under C1 and C2.")

    rows, keep_r, LIVE = [], {}, {}

    for pk in PANELS:
        px = load_universe(broad=(pk == "broad"))
        for t in SLEEVES["S4"]:
            if t not in px.columns:
                raise RuntimeError(f"{pk} lacks {t}")
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        ms = metrics(spy)
        say(f"\n[panel] {pk}: {px.shape[1]} cols, eval {start.date()}..{px.index[-1].date()}")
        say(f"    SPY CAGR {ms['CAGR']:.2%} vol {ms['Vol']:.3f} Sharpe(rf0) {ms['Sharpe']:.3f} "
            f"MaxDD {ms['MaxDD']:.2%}")

        # ---- the two live books, priced at every credit rung (4a comparand) ----
        live = {}
        for tag, wfn in (("v2", rules_v2_weights), ("v1", rules_v1_weights)):
            W = wfn(px)
            for c in CREDITS:
                sim = run_cash(px, W, c)
                for k in COSTS:
                    live[(tag, c, k)] = net(sim, k, start)
                live[(tag, c, "gross")] = sim["gross"].loc[start:].mean()
                live[(tag, c, "cash")] = sim["cash"].loc[start:].mean()
        for tag in ("v2", "v1"):
            g_ = live[(tag, 0.0, "gross")]
            ln = [f"    RULES {tag} mean gross {g_:.3f} (cash {live[(tag,0.0,'cash')]:.3f})"]
            for c in CREDITS:
                m = metrics(live[(tag, c, 10.0)])
                ln.append(f"c={c:.0f}: {m['CAGR']:.2%}/{m['Sharpe']:.3f}/{m['MaxDD']:.2%}")
            say("  ".join(ln))

        LIVE[pk] = dict(live=live, spy=spy)

        # ---- 4b bars per treatment -------------------------------------------
        bars = {}
        for c in CREDITS:
            for T in ("C0", "C1", "C2"):
                if T == "C0" and c != 0.0:
                    continue
                rf = c / 1e4 if T == "C2" else 0.0
                bars[(c, T)] = dict(full=bars_win(spy, "full", rf), IS=bars_win(spy, "IS", rf),
                                    oos=oos_bars(spy, rf))

        # ---- the family ------------------------------------------------------
        for bk in BOOKS:
            bW = base_book(px, bk)
            for sk, assets in SLEEVES.items():
                sW = sleeve_weights(px, assets)
                for f in FS:
                    for g in GS:
                        W = blend(bW, sW, f, g)
                        sims = {c: run_cash(px, W, c) for c in CREDITS}
                        for k in COSTS:
                            for c in CREDITS:
                                sim = sims[c]
                                r = net(sim, k, start)
                                mg = sim["gross"].loc[start:].mean()
                                mc = sim["cash"].loc[start:].mean()
                                m = metrics(r)
                                treats = ["C0"] if c == 0.0 else ["C1", "C2"]
                                for T in treats:
                                    rf = c / 1e4 if T == "C2" else 0.0
                                    b = bars[(c, T)]
                                    d = margins(r, b["full"], "full", rf)
                                    di = margins(r, b["IS"], "IS", rf)
                                    do = oos_margins(r, b["oos"], rf)
                                    row = dict(panel=pk, book=bk, sleeve=sk, cost=k, credit=c,
                                               treat=T, f=f, g=g, CAGR=m["CAGR"],
                                               Sharpe=sharpe(r, rf), Vol=m["Vol"],
                                               MaxDD=m["MaxDD"], gross=mg, cash=mc,
                                               turnover=sim["to"].loc[start:].sum() /
                                               (len(r) / 252.0),
                                               OOS_Sharpe=sharpe(r.loc[OOS_START:], rf),
                                               OOS_CAGR=metrics(r.loc[OOS_START:])["CAGR"],
                                               OOS_MaxDD=metrics(r.loc[OOS_START:])["MaxDD"])
                                    for kk in BARS:
                                        row["m_" + kk] = d[kk]
                                    row["m_min"] = min(d.values())
                                    row["m_bind"] = min(d, key=d.get)
                                    row["pass4b"] = bool(row["m_min"] > 0)
                                    row["IS_m_min"] = min(di.values())
                                    row["IS_pass4b"] = bool(row["IS_m_min"] > 0)
                                    row["OOS_m_min"] = min(do.values())
                                    row["OOS_pass"] = bool(row["OOS_m_min"] > 0)
                                    row["pass4a_v2"] = pass4a(r, live[("v2", c, k)], rf)
                                    row["pass4a_v1"] = pass4a(r, live[("v1", c, k)], rf)
                                    rows.append(row)
                                    keep_r[(pk, bk, sk, k, c, f, g)] = r
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"\n[grid] {len(G)} arm-rows written.")

    # ---- gate (a): c = 0 reproduces idea 402's committed grid ----------------
    ref = pd.read_csv(I402_GRID)
    ref = ref[(ref.fin == 0.0)].copy()
    key = ["panel", "book", "sleeve", "cost", "f", "g"]
    cols = ["CAGR", "Sharpe", "MaxDD", "m_CAGR", "m_DD"]
    a = G[G.treat == "C0"].set_index(key)[cols]
    b = ref.set_index(key)[cols]
    j = a.join(b, lsuffix="_new", rsuffix="_402", how="inner")
    for pk in PANELS:
        s = j[j.index.get_level_values("panel") == pk]
        e = max(float((s[c + "_new"] - s[c + "_402"]).abs().max()) for c in cols)
        say(f"[gate a] c=0 vs idea 402's committed grid, panel {pk}, {len(s)} shared rows: "
            f"max abs diff {e:.3e}")
    eb = max(float((j[j.index.get_level_values("panel") == "broad"][c + "_new"] -
                    j[j.index.get_level_values("panel") == "broad"][c + "_402"]).abs().max())
             for c in cols)
    assert eb < 1e-9, "broad must reproduce idea 402 exactly (its cache is unchanged)"
    say("[gate a] broad REPRODUCED to 1e-9.  u56 differs because data/prices.csv has gained "
        "trading days since idea 402 ran on 2026-09-07 (the broad cache is written weekly and "
        "has not moved).  Proof, not assertion — u56 truncated to idea 402's last bar:")
    pxu = load_universe()
    q = ref[(ref.panel == "u56") & (ref.book == "EWall") & (ref.sleeve == "S3") &
            (ref.cost == 10.0) & (ref.f == 0.25) & (ref.g == 0.75)].iloc[0]
    best = (np.inf, None)
    for cand in pxu.index[-8:]:
        pxt = pxu.loc[:cand]
        st = pxt.index[260]
        W = blend(base_book(pxt, "EWall"), sleeve_weights(pxt, SLEEVES["S3"]), 0.25, 0.75)
        rr = net(run_cash(pxt, W, 0.0), 10.0, st)
        d = abs(metrics(rr)["CAGR"] - q.CAGR) + abs(sharpe(rr) - q.Sharpe)
        say(f"      truncate u56 at {cand.date()}: |dCAGR|+|dSharpe| = {d:.3e}")
        best = min(best, (d, cand))
    say(f"[gate a] u56 is closest to idea 402 at truncation {best[1].date()} "
        f"(residual {best[0]:.2e}, vs {4.16e-3:.2e} untruncated).  The residual is NOT zero: "
        f"data/prices.csv is re-downloaded daily with AUTO-ADJUSTED closes, so its history is "
        f"restated (dividends) between runs.  u56 rows in this record are reproducible to ~1e-5, "
        f"not bit-exact; broad (weekly cache, unmoved) is bit-exact.  Reported, not corrected.")
    assert best[0] < 1e-4, "u56 must reproduce idea 402 to 1e-4 at the matching truncation"
    # direct simulator identity on today's data
    from engine import backtest as _bt
    _W = blend(base_book(pxu, "EWall"), sleeve_weights(pxu, SLEEVES["S3"]), 0.25, 0.75)
    _st = pxu.index[260]
    _d = float((net(run_cash(pxu, _W, 0.0), 10.0, _st) -
                _bt(pxu, _W, cost_bps=10.0, freq=FREQ)["returns"].loc[_st:]).abs().max())
    say(f"[gate a'] run_cash(c=0) vs engine.backtest on today's u56: max|d| {_d:.3e}")
    assert _d < 1e-12

    # ---- gate (b): the credit is (1-gross)*c to first order ------------------
    base = G[G.treat == "C0"].set_index(key + ["credit"]).droplevel("credit")
    chk = []
    for c in [x for x in CREDITS if x > 0]:
        cc = G[(G.treat == "C1") & (G.credit == c)].set_index(key)
        d = (cc["CAGR"] - base["CAGR"]) * 1e4                       # bps of CAGR actually gained
        pred = base["cash"] * c
        chk.append(pd.DataFrame(dict(credit=c, actual_bps=d, pred_bps=pred,
                                     err_bps=d - pred)).reset_index())
    CHK = pd.concat(chk)
    say("[gate b] exact CAGR gain vs first-order (1-gross)*c, bps:")
    say(CHK.groupby("credit")[["actual_bps", "pred_bps", "err_bps"]]
        .agg(["mean", "min", "max"]).to_string(float_format=lambda x: f"{x:.2f}"))
    say(f"[gate b] first-order error is at most {CHK.err_bps.abs().max():.2f} bps of CAGR; "
        f"the census (Q3) inherits exactly this error.")

    # ================= Q1/Q2 — how many 4b margins change sign ================
    say("\n=== Q1/Q2  SIGN CHANGES IN THE 4b BAR MARGINS ===")
    flips = []
    b0 = G[G.treat == "C0"].set_index(key)
    for c in [x for x in CREDITS if x > 0]:
        for T in ("C1", "C2"):
            cc = G[(G.treat == T) & (G.credit == c)].set_index(key)
            for bar in BARS:
                x, y = b0["m_" + bar], cc["m_" + bar]
                up = int(((x <= 0) & (y > 0)).sum())
                dn = int(((x > 0) & (y <= 0)).sum())
                flips.append(dict(credit=c, treat=T, bar=bar, n=len(x), fail_to_pass=up,
                                  pass_to_fail=dn, mean_shift=float((y - x).mean()),
                                  min_shift=float((y - x).min()), max_shift=float((y - x).max())))
            up = int(((~b0.pass4b) & cc.pass4b).sum())
            dn = int((b0.pass4b & (~cc.pass4b)).sum())
            flips.append(dict(credit=c, treat=T, bar="4b VERDICT", n=len(b0), fail_to_pass=up,
                              pass_to_fail=dn, mean_shift=float((cc.m_min - b0.m_min).mean()),
                              min_shift=float((cc.m_min - b0.m_min).min()),
                              max_shift=float((cc.m_min - b0.m_min).max())))
            up = int(((~b0.pass4a_v2) & cc.pass4a_v2).sum())
            dn = int((b0.pass4a_v2 & (~cc.pass4a_v2)).sum())
            flips.append(dict(credit=c, treat=T, bar="4a VERDICT (v2)", n=len(b0),
                              fail_to_pass=up, pass_to_fail=dn, mean_shift=np.nan,
                              min_shift=np.nan, max_shift=np.nan))
    F = pd.DataFrame(flips)
    F.to_csv(OUT / f"{STEM}.flips.csv", index=False)
    say(F.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    say(f"\n[Q1] C0 4b passes {int(b0.pass4b.sum())}/{len(b0)}; "
        + "; ".join(f"C{t}@{c:.0f} {int(G[(G.treat==t2)&(G.credit==c)].pass4b.sum())}"
                    for c in [x for x in CREDITS if x > 0] for t, t2 in ((1, 'C1'), (2, 'C2'))))

    # de-grossed vs levered split (the queue's claim: de-grossed books are the taxed ones)
    say("\n[Q1] flips by gross regime (de-grossed g<1 vs levered g>=1), 4b verdict:")
    tab = []
    for c in [x for x in CREDITS if x > 0]:
        for T in ("C1", "C2"):
            cc = G[(G.treat == T) & (G.credit == c)].set_index(key)
            for lab, sel in (("g<1", b0.index.get_level_values("g") < 1.0),
                             ("g>=1", b0.index.get_level_values("g") >= 1.0)):
                tab.append(dict(credit=c, treat=T, regime=lab, n=int(sel.sum()),
                                C0_pass=int(b0.pass4b[sel].sum()), pass_=int(cc.pass4b[sel].sum()),
                                mean_dm_min=float((cc.m_min[sel] - b0.m_min[sel]).mean()),
                                mean_cash=float(b0.cash[sel].mean())))
    say(pd.DataFrame(tab).to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    # ================= Q3 — record-wide census ===============================
    say("\n=== Q3  RECORD-WIDE CENSUS OF COMMITTED 4b MARGINS ===")
    need = {"gross", "m_CAGR", "m_DD", "m_H1", "m_H2", "m_min", "pass4b"}
    files = [p for p in sorted(glob.glob(str(OUT / "*.csv")))
             if need <= set(open(p).readline().strip().split(","))]
    cen, per_file = [], []
    for p in files:
        d = pd.read_csv(p)
        if Path(p).name.startswith(STEM):
            continue
        mcols = [c for c in ["m_H1", "m_H2", "m_OOS", "m_DD", "m_CAGR"] if c in d.columns]
        cash = (1.0 - d["gross"]).clip(lower=0.0)
        vol = d["Vol"] if "Vol" in d.columns else pd.Series(np.nan, index=d.index)
        for c in [x for x in CREDITS if x > 0]:
            n = d.copy()
            n["m_CAGR"] = d["m_CAGR"] + cash * c / 1e4
            for s in ("m_H1", "m_H2", "m_OOS"):
                if s in mcols:
                    n[s] = d[s] + (cash * c / 1e4) / vol           # NaN where Vol unpublished
            # m_DD is left unmoved: Q1 measures its true (positive, tiny) shift; see gate (c)
            new_min = n[mcols].min(axis=1)
            old_min = d[mcols].min(axis=1)
            ok = new_min.notna() & old_min.notna()
            per_file.append(dict(file=Path(p).name, credit=c, rows=int(len(d)),
                                 priceable=int(ok.sum()), mean_cash=float(cash.mean()),
                                 C0_pass=int((old_min > 0).sum()),
                                 C1_pass=int((new_min[ok] > 0).sum() + ((~ok) & (old_min > 0)).sum()),
                                 flip_up=int((ok & (old_min <= 0) & (new_min > 0)).sum()),
                                 cagr_flip=int(((d.m_CAGR <= 0) & (n.m_CAGR > 0)).sum())))
            cen.append(pd.DataFrame(dict(file=Path(p).name, credit=c, cash=cash,
                                         old_m_min=old_min, new_m_min=new_min,
                                         old_m_CAGR=d.m_CAGR, new_m_CAGR=n.m_CAGR)))
    PF = pd.DataFrame(per_file)
    PF.to_csv(OUT / f"{STEM}.census.csv", index=False)
    say(PF.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    CEN = pd.concat(cen)
    for c in [x for x in CREDITS if x > 0]:
        s = CEN[CEN.credit == c]
        say(f"[Q3] c={c:.0f} bps over {len(s)} committed rows ({s.file.nunique()} files): "
            f"mean cash {s.cash.mean():.3f}; CAGR-floor margins flipping fail->pass "
            f"{int(((s.old_m_CAGR<=0)&(s.new_m_CAGR>0)).sum())} "
            f"({((s.old_m_CAGR<=0)&(s.new_m_CAGR>0)).mean():.2%}); "
            f"4b verdicts flipping fail->pass "
            f"{int(((s.old_m_min<=0)&(s.new_m_min>0)).sum())} "
            f"({((s.old_m_min<=0)&(s.new_m_min>0)).mean():.2%}); pass->fail 0 by construction "
            f"(C1 margins are weakly increasing).")

    # ================= Q4 — rule 8 walk-forward ==============================
    say("\n=== Q4  RULE 8 WALK-FORWARD: does the cash convention move the pick? ===")
    wf = []
    for pk in PANELS:
        px = load_universe(broad=(pk == "broad"))
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        for bk in BOOKS:
            for sk in SLEEVES:
                for k in COSTS:
                    for c in CREDITS:
                        for T in (["C0"] if c == 0.0 else ["C1", "C2"]):
                            rf = c / 1e4 if T == "C2" else 0.0
                            sub = G[(G.panel == pk) & (G.book == bk) & (G.sleeve == sk) &
                                    (G.cost == k) & (G.credit == c) & (G.treat == T) &
                                    (G.g < 1.0)].copy()          # de-grossed arms only (no fin)
                            if sub.empty:
                                continue
                            pick = sub.sort_values(["IS_m_min", "f", "g"],
                                                   ascending=[False, True, True]).iloc[0]
                            r = keep_r[(pk, bk, sk, k, c, pick.f, pick.g)]
                            ro = r.loc[OOS_START:]
                            v2 = None
                            Wv2 = rules_v2_weights(px)
                            sim2 = run_cash(px, Wv2, c)
                            v2 = net(sim2, k, start)
                            v2o = v2.loc[OOS_START:]
                            so = spy.loc[OOS_START:]
                            wf.append(dict(panel=pk, book=bk, sleeve=sk, cost=k, credit=c,
                                           treat=T, pick_f=pick.f, pick_g=pick.g,
                                           IS_m_min=pick.IS_m_min,
                                           OOS_CAGR=metrics(ro)["CAGR"],
                                           OOS_Sharpe=sharpe(ro, rf),
                                           OOS_MaxDD=metrics(ro)["MaxDD"],
                                           v2_OOS_CAGR=metrics(v2o)["CAGR"],
                                           v2_OOS_Sharpe=sharpe(v2o, rf),
                                           v2_OOS_MaxDD=metrics(v2o)["MaxDD"],
                                           spy_OOS_CAGR=metrics(so)["CAGR"],
                                           spy_OOS_Sharpe=sharpe(so, rf),
                                           spy_OOS_MaxDD=metrics(so)["MaxDD"],
                                           OOS_pass=bool(pick.OOS_pass),
                                           beats_v2=bool(sharpe(ro, rf) > sharpe(v2o, rf)),
                                           beats_spy=bool(sharpe(ro, rf) > sharpe(so, rf))))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n[Q4] pick stability — (f,g) chosen under each treatment, by cell:")
    piv = WF.pivot_table(index=["panel", "book", "sleeve", "cost"],
                         columns=["treat", "credit"], values="pick_g", aggfunc="first")
    say(piv.to_string())
    base_pick = WF[WF.treat == "C0"].set_index(["panel", "book", "sleeve", "cost"])[["pick_f", "pick_g"]]
    for c in [x for x in CREDITS if x > 0]:
        for T in ("C1", "C2"):
            cc = WF[(WF.treat == T) & (WF.credit == c)].set_index(["panel", "book", "sleeve", "cost"])
            same = int(((cc.pick_f == base_pick.pick_f) & (cc.pick_g == base_pick.pick_g)).sum())
            dS = float((cc.OOS_Sharpe - cc.v2_OOS_Sharpe).mean())
            say(f"    {T}@{c:.0f}: pick unchanged in {same}/{len(cc)} cells; mean OOS Sharpe "
                f"vs RULES v2 {dS:+.4f}; OOS beats SPY in {int(cc.beats_spy.sum())}/{len(cc)}; "
                f"OOS 4b-visible bars all clear in {int(cc.OOS_pass.sum())}/{len(cc)}")
    c0 = WF[WF.treat == "C0"]
    say(f"    C0@0  : mean OOS Sharpe vs RULES v2 {(c0.OOS_Sharpe-c0.v2_OOS_Sharpe).mean():+.4f}; "
        f"OOS beats SPY in {int(c0.beats_spy.sum())}/{len(c0)}; OOS bars clear in "
        f"{int(c0.OOS_pass.sum())}/{len(c0)}")

    # ================= Q5 — KEEP paths =======================================
    say("\n=== Q5  KEEP PATHS ===")
    for c in CREDITS:
        for T in (["C0"] if c == 0.0 else ["C1", "C2"]):
            s = G[(G.credit == c) & (G.treat == T)]
            allcell = (s[s.g < 1.0].groupby(["f", "g"]).pass4b.mean() == 1.0)
            say(f"    {T}@{c:.0f}: 4a(v2) {int(s.pass4a_v2.sum())}/{len(s)}; "
                f"4a(v1) {int(s.pass4a_v1.sum())}/{len(s)}; 4b {int(s.pass4b.sum())}/{len(s)}; "
                f"(f,g) pairs passing 4b in ALL 16 cells: {int(allcell.sum())}/{len(allcell)} "
                f"{sorted(allcell[allcell].index.tolist())}")

    # ========= Q6 — the book that actually holds the cash: RULES v2 ==========
    say("\n=== Q6  THE LIVE BOOK ITSELF (RULES v2 holds more cash than any candidate) ===")
    lr = []
    for pk in PANELS:
        spy = LIVE[pk]["spy"]
        live = LIVE[pk]["live"]
        for tag in ("v2", "v1"):
            for k in COSTS:
                for c in CREDITS:
                    for T in (["C0"] if c == 0.0 else ["C1", "C2"]):
                        rf = c / 1e4 if T == "C2" else 0.0
                        r = live[(tag, c, k)]
                        b = dict(full=bars_win(spy, "full", rf))
                        d = margins(r, b["full"], "full", rf)
                        m = metrics(r)
                        lr.append(dict(panel=pk, bookrule=tag, cost=k, credit=c, treat=T,
                                       cash=live[(tag, c, "cash")], CAGR=m["CAGR"],
                                       Sharpe=sharpe(r, rf), MaxDD=m["MaxDD"],
                                       CAGR_floor=PHI * metrics(spy)["CAGR"],
                                       **{"m_" + kk: d[kk] for kk in BARS},
                                       m_min=min(d.values()), m_bind=min(d, key=d.get),
                                       pass4b=bool(min(d.values()) > 0)))
    LR = pd.DataFrame(lr)
    LR.to_csv(OUT / f"{STEM}.livebook.csv", index=False)
    say(LR.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    v2 = LR[(LR.bookrule == "v2") & (LR.cost == 10.0)]
    say(f"[Q6] RULES v2 holds {v2.cash.mean():.1%} cash on average.  4b passes: "
        + "; ".join(f"{t}@{c:.0f} {int(v2[(v2.treat==t)&(v2.credit==c)].pass4b.sum())}/2"
                    for c, t in [(0.0, 'C0'), (150.0, 'C1'), (150.0, 'C2'), (300.0, 'C1'),
                                 (300.0, 'C2')])
        + f".  Binding bar throughout: {v2.m_bind.value_counts().index[0]}. "
          f"CAGR at c=0/150/300 (u56): "
        + "/".join(f"{v2[(v2.panel=='u56')&(v2.credit==c)].CAGR.iloc[0]:.2%}" for c in CREDITS)
        + f" against a floor of {v2[v2.panel=='u56'].CAGR_floor.iloc[0]:.2%}.")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
