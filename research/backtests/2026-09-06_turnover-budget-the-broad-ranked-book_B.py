#!/usr/bin/env python3
"""QUEUE idea 273 — turnover-budget-the-broad-ranked-book (lane B, 2026-09-06).

Question
--------
Idea 70 (`2026-09-06_what-actually-moves-H2_B.py`) split the broad `top20-200d` H2 Sharpe
gap EXACTLY (identity holds to 1.1e-16) into

    selection +0.1145   turnover bill -0.0979 (14.37x/yr @10bps)   underinvestment -0.0395
                                                                   ------------------------
                                                                   dSharpe vs SPY  -0.0231

so the 4b-binding term is the BILL, not the alpha.  The queued test: put an explicit
turnover budget on that exact book and ask whether **-0.098 can be halved for less than
+0.05 of lost selection**.

Instrument
----------
A **no-trade band on the composite rank**, exactly as the queue words it: a name entering
the book must be in the top NPOS(=20), but a name already held is only replaced once its
rank falls past **NPOS + m**.  Second budget dial: at most **j** discretionary replacements
per rebalance (when more than j holdings breach the band, the j WORST-ranked go).

Pre-registered asymmetry, written before any number was read: **the 200d/vol gate is a risk
rule, not a turnover choice**, so a holding that becomes INELIGIBLE (price below its 200d MA,
or vol20 >= 0.60) is always sold, and those forced sells do NOT consume the j budget.  The
band and the cap therefore govern only rank churn among still-eligible names.  This keeps
every arm inside the parent's risk envelope and makes the comparison a pure cost test.

Reproduction gate (asserted BEFORE any new number is read)
----------------------------------------------------------
1. The parent book reproduces idea 66's PUBLISHED broad numbers 13.1% / 0.958 / -20.1%,
   halves 1.125 / 0.814, SPY H2 0.837.
2. The state machine at (m=0, j=inf) is IDENTICAL to the parent's stateless top-20 book —
   the retained set {rank<=20} plus best-ranked fills IS the top-20 set — asserted at
   max|weight diff| == 0 and max|return diff| == 0.
3. Idea 70's H2 split is recomputed on the parent and asserted against its published
   +0.1145 / -0.0979 / -0.0395 / -0.0231.

Design (PROTOCOL rules 1-9)
---------------------------
Universe : research/universe_broad.json via load_universe(broad=True), 136 tickers.
           SURVIVORSHIP: current constituents only, so absolute CAGR/Sharpe are optimistic;
           every comparison here is between arms on the SAME panel and SAME days.
           u56 (research/universe.json, load_universe()) is run as a TRANSFER panel — an
           arm, not a tuned dial: nothing is selected on it.
Book     : idea 66's `top20-200d` at gross 0.75, weekly, verbatim (composite = mean pct-rank
           of 12-1 / 6m / 3m with NO vol scaler; eligibility = vol20 < 0.60 AND price > 200d
           MA; equal weight 0.75/20; cash if fewer than 20 qualify).  Nothing about the
           parent is tuned here.
Params   : exactly 2 tuned — m in {0,2,5,10,15,20,30,50,999} (999 = hold until ineligible)
           and j in {1,2,3,5,999} (999 = uncapped).  ALL 45 grid points reported at BOTH
           cost rungs on BOTH panels.
Costs    : 10 bps is the protocol rung and the verdict rung; 25 bps is a reporting axis
           (a turnover budget must pay MORE as costs rise or it is not a cost instrument).
Rule 8   : (m, j) chosen on 2009-2016 ONLY by full-window Sharpe, 2017-2026 untouched.
           The book is causal, so the IS window is a slice of the same run.  NOTE, and the
           run says so where it reports: 2017-2026 is essentially H2, so the OOS window and
           the 4b H2 bar OVERLAP ~100% — the walk-forward here is weak by construction and
           is reported as such (idea 111's window problem).
Verdict  : both KEEP paths on every grid point; 4a against the LIVE book (RULES v2), with
           the retired v1 verdict carried alongside for continuity.

Outputs: .console.txt, .grid.csv (every point), .split.csv (H2 attribution per cell),
.walkforward.csv.  Deterministic, no randomness, no network.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask                    # noqa: E402

NPOS, GROSS, MAX_VOL, FREQ = 20, 0.75, 0.60, "W"
END = "2026-09-03"                 # idea 66/70's last eval day, so the halves split identically
IS_END, OOS_START = "2016-12-31", "2017-01-01"
MGRID = [0, 2, 5, 10, 15, 20, 30, 50, 999]     # tuned param 1: no-trade band width
JGRID = [1, 2, 3, 5, 999]                      # tuned param 2: replacements per rebalance
RUNGS = [10, 25]                               # reporting axis, not tuned
OUT = Path(__file__).with_suffix("")

_LINES = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _LINES.append(s)


# --------------------------------------------------------------- construction
def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def eligible(px):
    return (vol20(px) < MAX_VOL) & (px > px.rolling(200).mean())


def parent_weights(px):
    """Idea 66's stateless `top20-200d` at gross 0.75."""
    rank = composite(px).where(eligible(px)).rank(axis=1, ascending=False)
    return (rank <= NPOS).astype(float) * (GROSS / NPOS)


def band_weights(px, m, j):
    """No-trade band on the composite rank, with a cap of j discretionary replacements.

    At each rebalance date:
      1. drop every holding that is INELIGIBLE (risk rule, never capped, never banded);
      2. among still-eligible holdings, those with rank > NPOS + m are band breaches; if
         more than j breach, only the j WORST-ranked are sold (the rest stay one more week);
      3. vacancies are filled with the best-ranked non-held eligible names whose rank is
         <= NPOS, until NPOS are held (fewer if the top NPOS is not full — this is what
         makes the band a pure BUFFER: entry bar NPOS, exit bar NPOS+m).  Names TIED at
         the fill cut are all taken, because the parent's `rank <= NPOS` mask does the
         same: on 7 of 975 rebalance dates a 3-way tie at rank 20.0 makes the parent hold
         21 names at gross 0.7875, so the target size on a date is the PARENT'S set size
         |{rank <= NPOS}|, not the constant 20.  Carrying that quirk verbatim is what lets
         m=0 nest the parent EXACTLY (gate 2) instead of approximately.  Realised mean
         gross is reported per cell so no arm hides an exposure difference (idea 274).
    Weight is GROSS/NPOS per held name; the remainder is cash.
    """
    comp = composite(px)
    elig = eligible(px)
    rank_all = comp.where(elig).rank(axis=1, ascending=False)
    dates = px.index[rebalance_mask(px.index, FREQ).values]
    cols = list(px.columns)
    pos = {c: i for i, c in enumerate(cols)}
    W = np.zeros((len(px.index), len(cols)))
    rk = rank_all.values
    didx = {d: i for i, d in enumerate(px.index)}
    held = []                                    # list of tickers, ordered by entry
    row = np.zeros(len(cols))
    prev_i = 0
    for d in dates:
        i = didx[d]
        W[prev_i:i] = row                        # carry last target forward (only rebal rows are read)
        r = rk[i]
        # 1. forced exits: ineligible today (rank is NaN)
        held = [t for t in held if not np.isnan(r[pos[t]])]
        # 2. band breaches, worst first, capped at j
        breach = sorted([t for t in held if r[pos[t]] > NPOS + m], key=lambda t: -r[pos[t]])
        for t in breach[:j]:
            held.remove(t)
        # 3. fill vacancies with best-ranked non-held eligible names
        npos_t = int(np.nansum(r <= NPOS))          # the parent's own set size on this date
        need = npos_t - len(held)
        if need > 0:
            hs = set(held)
            cand = [(r[pos[c]], c) for c in cols
                    if c not in hs and not np.isnan(r[pos[c]]) and r[pos[c]] <= NPOS]
            cand.sort()
            held += [c for _, c in cand[:need]]
        row = np.zeros(len(cols))
        for t in held:
            row[pos[t]] = GROSS / NPOS
        W[i] = row
        prev_i = i + 1
    W[prev_i:] = row
    return pd.DataFrame(W, index=px.index, columns=px.columns)


def m3(r):
    d = metrics(r)
    return d["CAGR"], d["Sharpe"], d["MaxDD"]


# ------------------------------------------------------------------ KEEP paths
def path4a(r, base):
    h = len(r) // 2
    bad = []
    if metrics(r.iloc[:h])["Sharpe"] <= metrics(base.iloc[:h])["Sharpe"]: bad.append("H1")
    if metrics(r.iloc[h:])["Sharpe"] <= metrics(base.iloc[h:])["Sharpe"]: bad.append("H2")
    if metrics(r)["MaxDD"] < metrics(base)["MaxDD"]: bad.append("DD")
    return bad


def path4b(r, spy, oos_s, spy_oos_s):
    h = len(r) // 2
    bad = []
    if metrics(r.iloc[:h])["Sharpe"] <= metrics(spy.iloc[:h])["Sharpe"]: bad.append("H1")
    if metrics(r.iloc[h:])["Sharpe"] <= metrics(spy.iloc[h:])["Sharpe"]: bad.append("H2")
    if oos_s <= spy_oos_s: bad.append("OOS")
    if abs(metrics(r)["MaxDD"]) > 0.60 * abs(metrics(spy)["MaxDD"]): bad.append("DD")
    if metrics(r)["CAGR"] < 0.70 * metrics(spy)["CAGR"]: bad.append("CAGR")
    return bad


def vstr(bad, tag):
    return f"KEEP {tag}" if not bad else f"KILL {tag}(" + ",".join(bad) + ")"


# --------------------------------------------------- idea 70's exact H2 split
def split(res, px, spy, sl):
    """Vol-matched active-return split over slice `sl`.

        a_t = k*sum_i h_i(r_i - r_spy)  +  (k*sum_i h_i - 1)*r_spy  -  k*cost_t
              \_______ SELECTION _______/   \___ UNDERINVESTMENT __/   \_ BILL _/

    with k = sigma_spy/sigma_book on the same slice, and
    252*mean(a)/sigma_spy == Sharpe(book) - Sharpe(SPY) EXACTLY.

    Two SEL/UND boundaries are reported, because idea 70 used the second one:
      * `SEL`/`UND`   — the exact, time-varying split above (gross_t varies day to day);
      * `SEL0`/`UND0` — idea 70's published boundary, which prices underinvestment with the
        STATIC mean gross, UND0 = (k*mean(gross) - 1) * Sharpe(SPY), and puts the remainder
        in selection.  BILL and dS are identical under both, and those are the two numbers
        the queued question is asked in; the boundary only moves 0.0455 between SEL and UND.
    """
    r = res["returns"].iloc[sl]
    h = res["weights"].iloc[sl]
    t = res["turnover"].iloc[sl]
    s = spy.iloc[sl]
    rets = px.pct_change().fillna(0.0).reindex(h.index)
    sig_b, sig_s = r.std() * np.sqrt(252), s.std() * np.sqrt(252)
    k = sig_s / sig_b
    gross = h.sum(axis=1)
    sel = (k * (h * rets.sub(s, axis=0)).sum(axis=1))
    und = (k * gross - 1.0) * s
    bill = -k * t * res["cost_bps"] / 1e4
    f = 252.0 / sig_s
    SEL, UND, BILL = sel.mean() * f, und.mean() * f, bill.mean() * f
    dS = metrics(r)["Sharpe"] - metrics(s)["Sharpe"]
    UND0 = (k * gross.mean() - 1.0) * metrics(s)["Sharpe"]      # idea 70's boundary
    SEL0 = dS - BILL - UND0
    return dict(k=k, SEL=SEL, UND=UND, BILL=BILL, SEL0=SEL0, UND0=UND0, gross=gross.mean(),
                sum=SEL + UND + BILL, dS=dS, resid=abs(SEL + UND + BILL - dS))


def run(px, w, bps):
    res = backtest(px, w, cost_bps=bps, freq=FREQ)
    res["cost_bps"] = bps
    return res


# ==================================================================== main
def main():
    pd.set_option("display.width", 200)
    px = load_universe(broad=True).loc[:END]
    P(f"universe_broad.json: {px.shape[1]} tickers, {px.index[0].date()} -> {px.index[-1].date()}")
    start = px.index[260]
    spy_full = px["SPY"].pct_change().fillna(0.0)
    spy = spy_full.loc[start:]

    pw = parent_weights(px)
    parent = {b: run(px, pw, b) for b in RUNGS}
    pr = {b: parent[b]["returns"].loc[start:] for b in RUNGS}
    n = len(pr[10]); h = n // 2
    yrs = n / 252.0

    # ------------------------------------------------------ reproduction gate 1
    P("\n" + "=" * 100)
    P("REPRODUCTION GATE 1 — idea 66's published broad `top20-200d` g=0.75 core=0 @10bps")
    P("=" * 100)
    got = dict(CAGR=metrics(pr[10])["CAGR"], Sharpe=metrics(pr[10])["Sharpe"], MaxDD=metrics(pr[10])["MaxDD"],
               H1=metrics(pr[10].iloc[:h])["Sharpe"], H2=metrics(pr[10].iloc[h:])["Sharpe"],
               SPY_H2=metrics(spy.iloc[h:])["Sharpe"])
    want = dict(CAGR=0.131, Sharpe=0.958, MaxDD=-0.201, H1=1.125, H2=0.814, SPY_H2=0.837)
    ok = True
    for kk in want:
        hit = abs(got[kk] - want[kk]) <= 5e-4
        ok &= hit
        P(f"  {kk:8s} published {want[kk]:8.3f}   reproduced {got[kk]:8.4f}   {'EXACT' if hit else 'MISMATCH'}")
    P(f"  eval window {pr[10].index[0].date()} -> {pr[10].index[-1].date()}   H2 from {pr[10].index[h].date()}")
    P(f"  GATE 1: {'6/6 EXACT' if ok else 'FAILED'}")
    assert ok, "reproduction gate 1 failed — refusing to read new numbers"

    # ------------------------------------------------------ reproduction gate 2
    P("\n" + "=" * 100)
    P("REPRODUCTION GATE 2 — the state machine at (m=0, j=inf) IS the stateless top-20 book")
    P("=" * 100)
    w0 = band_weights(px, 0, 999)
    mask = rebalance_mask(px.index, FREQ)
    dw = (w0 - pw).abs().loc[mask.values].to_numpy().max()   # only rebalance rows are read
    r0 = run(px, w0, 10)["returns"].loc[start:]
    dr = (r0 - pr[10]).abs().max()
    P(f"  max|weight diff| on rebalance rows : {dw:.3e}")
    P(f"  max|daily return diff|             : {dr:.3e}")
    P(f"  GATE 2: {'EXACT' if dw == 0.0 and dr == 0.0 else 'FAILED'}")
    assert dw == 0.0 and dr == 0.0, "state machine does not nest the parent — refusing to continue"

    # ------------------------------------------------------ reproduction gate 3
    P("\n" + "=" * 100)
    P("REPRODUCTION GATE 3 — idea 70's H2 split of the parent (vol-matched, @10bps)")
    P("=" * 100)
    sp = split(parent[10], px, spy_full, slice(px.index.get_loc(start) + h, None))
    pub = dict(SEL0=0.1145, BILL=-0.0979, UND0=-0.0395, dS=-0.0231)
    ok3 = True
    for kk in ("SEL0", "BILL", "UND0", "dS"):
        hit = abs(sp[kk] - pub[kk]) <= 1e-3
        ok3 &= hit
        P(f"  {kk:5s} published {pub[kk]:+8.4f}   reproduced {sp[kk]:+8.4f}   {'MATCH' if hit else 'MISMATCH'}")
    P(f"  exact time-varying boundary: SEL {sp['SEL']:+.4f}  UND {sp['UND']:+.4f}  "
      f"(same BILL and dS; the boundary moves {abs(sp['SEL']-sp['SEL0']):.4f} between the two terms)")
    P(f"  identity residual |SEL+UND+BILL-dS| = {sp['resid']:.2e}   vol-match k = {sp['k']:.4f}   "
      f"mean gross {sp['gross']:.4f}")
    P(f"  parent turnover = {parent[10]['turnover'].loc[start:].sum()/yrs:.2f}x/yr")
    P(f"  GATE 3: {'4/4 MATCH' if ok3 else 'MISMATCH (idea 70 numbers not reproduced)'}")
    assert ok3, "reproduction gate 3 failed — refusing to read new numbers"

    # ------------------------------------------------------------- baselines
    base_v2 = {b: backtest(px, rules_v2_weights(px), cost_bps=b, freq=FREQ)["returns"].loc[start:] for b in RUNGS}
    base_v1 = {b: backtest(px, rules_v1_weights(px), cost_bps=b, freq=FREQ)["returns"].loc[start:] for b in RUNGS}
    oos = pr[10].loc[OOS_START:].index
    ins = pr[10].loc[:IS_END].index
    spy_oos_s = metrics(spy.loc[oos])["Sharpe"]
    P("\n" + "=" * 100)
    P("REFERENCE ROWS (broad panel, weekly, eval window above)")
    P("=" * 100)
    P(f"{'row':34s} {'bps':>4s} {'CAGR':>7s} {'Sharpe':>7s} {'MaxDD':>8s} {'H1':>7s} {'H2':>7s} "
      f"{'OOS CAGR':>9s} {'OOSShrp':>8s} {'OOS DD':>8s} {'turn/yr':>8s}")
    def refrow(name, r, turn=np.nan, bps=10):
        c, s, dd = m3(r)
        oc, os_, odd = m3(r.loc[oos])
        P(f"{name:34s} {bps:4d} {c:7.2%} {s:7.3f} {dd:8.2%} {metrics(r.iloc[:h])['Sharpe']:7.3f} "
          f"{metrics(r.iloc[h:])['Sharpe']:7.3f} {oc:9.2%} {os_:8.3f} {odd:8.2%} {turn:8.2f}")
    for b in RUNGS:
        refrow("parent top20-200d (m=0,j=inf)", pr[b], parent[b]["turnover"].loc[start:].sum() / yrs, b)
    for b in RUNGS:
        refrow("RULES v2 baseline (live)", base_v2[b], np.nan, b)
    for b in RUNGS:
        refrow("RULES v1 (previous)", base_v1[b], np.nan, b)
    refrow("SPY buy-and-hold", spy)

    # ------------------------------------------------------------- the grid
    P("\n" + "=" * 100)
    P("GRID — no-trade band m x replacement cap j, broad panel, ALL 45 points x 2 cost rungs")
    P("  m = keep a holding until its composite rank passes NPOS+m (999 = until ineligible)")
    P("  j = at most j discretionary replacements per weekly rebalance (999 = uncapped)")
    P("  4a vs the LIVE book (RULES v2 at the same rung); [v1] carried for continuity")
    P("=" * 100)
    rows, splits = [], []
    W = {}
    for m in MGRID:
        W[m] = {}
        for j in JGRID:
            W[m][j] = band_weights(px, m, j)
    P(f"{'m':>4s} {'j':>4s} {'bps':>4s} {'CAGR':>7s} {'Sharpe':>7s} {'MaxDD':>8s} {'H1':>7s} {'H2':>7s} "
      f"{'turn/yr':>8s} {'IS Shrp':>8s} {'OOSShrp':>8s} {'OOS DD':>8s}  verdicts")
    for m in MGRID:
        for j in JGRID:
            for b in RUNGS:
                res = run(px, W[m][j], b)
                r = res["returns"].loc[start:]
                turn = res["turnover"].loc[start:].sum() / yrs
                gr = res["weights"].loc[start:].sum(axis=1).mean()
                c, s, dd = m3(r)
                is_s = metrics(r.loc[ins])["Sharpe"]
                oc, os_, odd = m3(r.loc[oos])
                a = path4a(r, base_v2[b]); a1 = path4a(r, base_v1[b])
                bb = path4b(r, spy, os_, spy_oos_s)
                P(f"{m:4d} {j:4d} {b:4d} {c:7.2%} {s:7.3f} {dd:8.2%} {metrics(r.iloc[:h])['Sharpe']:7.3f} "
                  f"{metrics(r.iloc[h:])['Sharpe']:7.3f} {turn:8.2f} {is_s:8.3f} {os_:8.3f} {odd:8.2%}  "
                  f"{vstr(a,'4a')} / {vstr(bb,'4b')}  [v1:{vstr(a1,'4a')}]")
                rows.append(dict(panel="broad", m=m, j=j, bps=b, gross=gr, CAGR=c, Sharpe=s, MaxDD=dd,
                                 H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                                 turn_per_yr=turn, IS_Sharpe=is_s, OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=odd,
                                 keep4a=not a, keep4b=not bb, keep4a_v1=not a1,
                                 fail4a=",".join(a), fail4b=",".join(bb)))
                if b == 10:
                    sp2 = split(res, px, spy_full, slice(px.index.get_loc(start) + h, None))
                    spf = split(res, px, spy_full, slice(px.index.get_loc(start), None))
                    splits.append(dict(m=m, j=j, H2_SEL=sp2["SEL0"], H2_UND=sp2["UND0"], H2_BILL=sp2["BILL"],
                                       H2_dS=sp2["dS"], H2_resid=sp2["resid"],
                                       H2_SEL_exact=sp2["SEL"], H2_UND_exact=sp2["UND"],
                                       FULL_SEL=spf["SEL0"], FULL_UND=spf["UND0"], FULL_BILL=spf["BILL"],
                                       FULL_dS=spf["dS"], turn_per_yr=turn, gross=gr))
    grid = pd.DataFrame(rows)
    grid.to_csv(f"{OUT}.grid.csv", index=False)
    sdf = pd.DataFrame(splits)
    sdf.to_csv(f"{OUT}.split.csv", index=False)

    # ------------------------------------------- the queued test, stated exactly
    P("\n" + "=" * 100)
    P("THE QUEUED TEST — can the -0.0979 H2 bill be HALVED for less than +0.05 of lost selection?")
    P("  bar: H2_BILL >= -0.04895  AND  (parent H2_SEL - H2_SEL) <= 0.05     (@10bps, broad)")
    P("  SEL/UND are on idea 70's published boundary, the one the question is worded in.")
    P("=" * 100)
    p_sel, p_bill = sp["SEL0"], sp["BILL"]
    sdf["bill_halved"] = sdf["H2_BILL"] >= p_bill / 2.0
    sdf["sel_lost"] = p_sel - sdf["H2_SEL"]
    sdf["sel_ok"] = sdf["sel_lost"] <= 0.05
    sdf["passes"] = sdf["bill_halved"] & sdf["sel_ok"]
    P(f"{'m':>4s} {'j':>4s} {'turn/yr':>8s} {'H2 SEL':>8s} {'H2 UND':>8s} {'H2 BILL':>8s} {'H2 dS':>8s} "
      f"{'selLost':>8s} {'billHlv':>8s} {'PASS':>6s}   {'FULL SEL':>9s} {'FULL BILL':>9s} {'FULL dS':>8s}")
    for _, x in sdf.iterrows():
        P(f"{int(x['m']):4d} {int(x['j']):4d} {x['turn_per_yr']:8.2f} {x['H2_SEL']:+8.4f} {x['H2_UND']:+8.4f} "
          f"{x['H2_BILL']:+8.4f} {x['H2_dS']:+8.4f} {x['sel_lost']:+8.4f} {str(bool(x['bill_halved'])):>8s} "
          f"{str(bool(x['passes'])):>6s}   {x['FULL_SEL']:+9.4f} {x['FULL_BILL']:+9.4f} {x['FULL_dS']:+8.4f}")
    npass = int(sdf["passes"].sum())
    nhalf = int(sdf["bill_halved"].sum())
    P(f"\n  bill halved in {nhalf}/{len(sdf)} cells; of those, selection loss <= 0.05 in {npass}/{len(sdf)}")
    P(f"  max identity residual across all cells: {sdf['H2_resid'].max():.2e}")
    pos = sdf[sdf["H2_dS"] > 0]
    P(f"  cells whose H2 dSharpe vs SPY turns POSITIVE: {len(pos)}/{len(sdf)}"
      + (f"  best {pos['H2_dS'].max():+.4f} at m={int(pos.loc[pos['H2_dS'].idxmax(),'m'])}, "
         f"j={int(pos.loc[pos['H2_dS'].idxmax(),'j'])}" if len(pos) else ""))
    # trade-off curve: how much selection is bought back per unit of bill saved
    b_ = sdf[sdf["turn_per_yr"] < sdf["turn_per_yr"].max()]
    if len(b_):
        dbill = b_["H2_BILL"] - p_bill
        dsel = b_["H2_SEL"] - p_sel
        ratio = (dsel / dbill).replace([np.inf, -np.inf], np.nan)
        P(f"  slope d(SEL)/d(BILL saved) across {len(b_)} budgeted cells: median {ratio.median():+.3f}, "
          f"mean {ratio.mean():+.3f}  (< 1 means the budget is worth taking)")

    # ------------------------------------------------------------ Sharpe vs turnover
    P("\n" + "=" * 100)
    P("SHARPE AGAINST TURNOVER (broad, @10bps) — the queued deliverable")
    P("=" * 100)
    g10 = grid[(grid.panel == "broad") & (grid.bps == 10)].sort_values("turn_per_yr")
    P(f"{'turn/yr':>8s} {'m':>4s} {'j':>4s} {'gross':>6s} {'Sharpe':>7s} {'CAGR':>7s} {'MaxDD':>8s} {'H2':>7s} {'OOSShrp':>8s}")
    for _, x in g10.iterrows():
        P(f"{x['turn_per_yr']:8.2f} {int(x['m']):4d} {int(x['j']):4d} {x['gross']:6.4f} {x['Sharpe']:7.3f} {x['CAGR']:7.2%} "
          f"{x['MaxDD']:8.2%} {x['H2']:7.3f} {x['OOS_Sharpe']:8.3f}")
    P(f"\n  realised mean gross across the 45 cells: {g10['gross'].min():.4f} - {g10['gross'].max():.4f} "
      f"(parent {g10[(g10.m==0)&(g10.j==999)]['gross'].iloc[0]:.4f}) — span "
      f"{g10['gross'].max()-g10['gross'].min():.4f}, so this is NOT a gross comparison")
    for b in RUNGS:
        gg = grid[(grid.panel == "broad") & (grid.bps == b)]
        c1 = np.corrcoef(gg["turn_per_yr"], gg["Sharpe"])[0, 1]
        best = gg.loc[gg["Sharpe"].idxmax()]
        P(f"\n  @{b:2d}bps: corr(turnover, full Sharpe) = {c1:+.3f}; best cell m={int(best['m'])} j={int(best['j'])} "
          f"Sharpe {best['Sharpe']:.3f} at {best['turn_per_yr']:.2f}x/yr vs parent "
          f"{grid[(grid.m==0)&(grid.j==999)&(grid.bps==b)]['Sharpe'].iloc[0]:.3f} at "
          f"{grid[(grid.m==0)&(grid.j==999)&(grid.bps==b)]['turn_per_yr'].iloc[0]:.2f}x/yr")

    # ------------------------------------------------------------- rule 8
    P("\n" + "=" * 100)
    P("RULE 8 WALK-FORWARD — (m,j) chosen on 2009-2016 Sharpe ONLY, 2017-2026 untouched")
    P("  CAVEAT, pre-registered: 2017-2026 is ~the same window as H2, so the OOS bar and the")
    P("  4b H2 bar overlap almost completely (idea 111).  This weakens, not strengthens, any KEEP.")
    P("=" * 100)
    wf = []
    for b in RUNGS:
        gg = grid[(grid.panel == "broad") & (grid.bps == b)].copy()
        pick = gg.loc[gg["IS_Sharpe"].idxmax()]
        par = gg[(gg.m == 0) & (gg.j == 999)].iloc[0]
        bv2 = base_v2[b]
        P(f"\n  @{b}bps IS pick: m={int(pick['m'])}, j={int(pick['j'])}  (IS Sharpe {pick['IS_Sharpe']:.4f} "
          f"vs parent's {par['IS_Sharpe']:.4f})")
        P(f"    {'series':30s} {'OOS CAGR':>9s} {'OOSShrp':>8s} {'OOS DD':>8s}")
        for nm, r_ in (("IS-picked band book", None), ("parent top20-200d", None),
                       ("RULES v2 baseline (live)", bv2), ("RULES v1 (previous)", base_v1[b]), ("SPY", spy)):
            if nm == "IS-picked band book":
                oc, os_, odd = pick["OOS_CAGR"], pick["OOS_Sharpe"], pick["OOS_MaxDD"]
            elif nm == "parent top20-200d":
                oc, os_, odd = par["OOS_CAGR"], par["OOS_Sharpe"], par["OOS_MaxDD"]
            else:
                oc, os_, odd = m3(r_.loc[oos])
            P(f"    {nm:30s} {oc:9.2%} {os_:8.3f} {odd:8.2%}")
            wf.append(dict(bps=b, series=nm, m=int(pick["m"]), j=int(pick["j"]),
                           OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=odd))
        P(f"    dOOS Sharpe (IS pick - parent) = {pick['OOS_Sharpe']-par['OOS_Sharpe']:+.4f}; "
          f"vs v2 = {pick['OOS_Sharpe']-metrics(bv2.loc[oos])['Sharpe']:+.4f}; "
          f"vs SPY = {pick['OOS_Sharpe']-spy_oos_s:+.4f}")
        # is the IS ranking of (m,j) informative about the OOS ranking at all?
        rho = gg[["IS_Sharpe", "OOS_Sharpe"]].corr(method="spearman").iloc[0, 1]
        P(f"    Spearman(IS Sharpe, OOS Sharpe) across the 45 cells = {rho:+.3f}  "
          f"(IS-best is OOS-best: {bool(gg['OOS_Sharpe'].idxmax()==gg['IS_Sharpe'].idxmax())})")
    pd.DataFrame(wf).to_csv(f"{OUT}.walkforward.csv", index=False)

    # ------------------------------------------------------------- transfer panel
    P("\n" + "=" * 100)
    P("TRANSFER — the identical grid on u56 (research/universe.json). An ARM, nothing selected here.")
    P("=" * 100)
    px2 = load_universe().loc[:END]
    start2 = px2.index[260]
    spy2_full = px2["SPY"].pct_change().fillna(0.0)
    spy2 = spy2_full.loc[start2:]
    n2 = len(spy2); h2 = n2 // 2; yrs2 = n2 / 252.0
    oos2 = spy2.loc[OOS_START:].index
    spy2_oos_s = metrics(spy2.loc[oos2])["Sharpe"]
    b2v2 = backtest(px2, rules_v2_weights(px2), cost_bps=10, freq=FREQ)["returns"].loc[start2:]
    trows = []
    P(f"{'m':>4s} {'j':>4s} {'CAGR':>7s} {'Sharpe':>7s} {'MaxDD':>8s} {'H1':>7s} {'H2':>7s} {'turn/yr':>8s} "
      f"{'OOSShrp':>8s}  verdicts (@10bps)")
    for m in MGRID:
        for j in JGRID:
            res = run(px2, band_weights(px2, m, j), 10)
            r = res["returns"].loc[start2:]
            turn = res["turnover"].loc[start2:].sum() / yrs2
            c, s, dd = m3(r)
            oc, os_, odd = m3(r.loc[oos2])
            a = path4a(r, b2v2); bb = path4b(r, spy2, os_, spy2_oos_s)
            P(f"{m:4d} {j:4d} {c:7.2%} {s:7.3f} {dd:8.2%} {metrics(r.iloc[:h2])['Sharpe']:7.3f} "
              f"{metrics(r.iloc[h2:])['Sharpe']:7.3f} {turn:8.2f} {os_:8.3f}  {vstr(a,'4a')} / {vstr(bb,'4b')}")
            trows.append(dict(panel="u56", m=m, j=j, bps=10,
                              gross=res["weights"].loc[start2:].sum(axis=1).mean(),
                              CAGR=c, Sharpe=s, MaxDD=dd,
                              H1=metrics(r.iloc[:h2])["Sharpe"], H2=metrics(r.iloc[h2:])["Sharpe"],
                              turn_per_yr=turn, IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                              OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=odd,
                              keep4a=not a, keep4b=not bb, keep4a_v1=np.nan,
                              fail4a=",".join(a), fail4b=",".join(bb)))
    t56 = pd.DataFrame(trows)
    pd.concat([grid, t56], ignore_index=True).to_csv(f"{OUT}.grid.csv", index=False)
    # rule 8 on the transfer panel too — 45 cells clear 4b there, so they need a selector
    pick56 = t56.loc[t56["IS_Sharpe"].idxmax()]
    par56 = t56[(t56.m == 0) & (t56.j == 999)].iloc[0]
    P(f"\n  RULE 8 on u56 @10bps — IS pick m={int(pick56['m'])}, j={int(pick56['j'])} "
      f"(IS Sharpe {pick56['IS_Sharpe']:.4f} vs parent's {par56['IS_Sharpe']:.4f})")
    P(f"    {'series':30s} {'OOS CAGR':>9s} {'OOSShrp':>8s} {'OOS DD':>8s}")
    P(f"    {'IS-picked band book':30s} {pick56['OOS_CAGR']:9.2%} {pick56['OOS_Sharpe']:8.3f} {pick56['OOS_MaxDD']:8.2%}")
    P(f"    {'parent top20-200d (u56)':30s} {par56['OOS_CAGR']:9.2%} {par56['OOS_Sharpe']:8.3f} {par56['OOS_MaxDD']:8.2%}")
    for nm, r_ in (("RULES v2 baseline (live)", b2v2), ("SPY", spy2)):
        oc, os_, odd = m3(r_.loc[oos2])
        P(f"    {nm:30s} {oc:9.2%} {os_:8.3f} {odd:8.2%}")
    P(f"    dOOS Sharpe (IS pick - parent) = {pick56['OOS_Sharpe']-par56['OOS_Sharpe']:+.4f}; "
      f"vs v2 = {pick56['OOS_Sharpe']-metrics(b2v2.loc[oos2])['Sharpe']:+.4f}; "
      f"vs SPY = {pick56['OOS_Sharpe']-spy2_oos_s:+.4f}")
    P(f"    Spearman(IS, OOS) across the 45 u56 cells = "
      f"{t56[['IS_Sharpe','OOS_Sharpe']].corr(method='spearman').iloc[0,1]:+.3f}; "
      f"IS pick clears 4b: {bool(pick56['keep4b'])}, 4a: {bool(pick56['keep4a'])}")
    c56 = np.corrcoef(t56["turn_per_yr"], t56["Sharpe"])[0, 1]
    P(f"\n  u56: corr(turnover, Sharpe) = {c56:+.3f} vs broad's "
      f"{np.corrcoef(grid[(grid.bps==10)]['turn_per_yr'], grid[(grid.bps==10)]['Sharpe'])[0,1]:+.3f}  "
      f"(same sign = the budget's effect transfers)")

    # ------------------------------------------------------------- verdict
    P("\n" + "=" * 100)
    P("VERDICT COUNTS")
    P("=" * 100)
    allg = pd.concat([grid, t56], ignore_index=True)
    P(f"  broad 4a (vs live RULES v2): {int(grid['keep4a'].sum())}/{len(grid)}   "
      f"4b: {int(grid['keep4b'].sum())}/{len(grid)}   [v1 4a: {int(grid['keep4a_v1'].sum())}/{len(grid)}]")
    P(f"  u56   4a: {int(t56['keep4a'].sum())}/{len(t56)}   4b: {int(t56['keep4b'].sum())}/{len(t56)}")
    P(f"  ALL   4a: {int(allg['keep4a'].sum())}/{len(allg)}   4b: {int(allg['keep4b'].sum())}/{len(allg)}")
    for _, x in allg[allg["keep4b"]].iterrows():
        P(f"    4b KEEP: {x['panel']} m={int(x['m'])} j={int(x['j'])} @{int(x['bps'])}bps  "
          f"{x['CAGR']:.2%}/{x['Sharpe']:.3f}/{x['MaxDD']:.2%} halves {x['H1']:.3f}/{x['H2']:.3f} "
          f"OOS {x['OOS_Sharpe']:.3f} turn {x['turn_per_yr']:.2f}x")
    for _, x in allg[allg["keep4a"]].iterrows():
        P(f"    4a KEEP: {x['panel']} m={int(x['m'])} j={int(x['j'])} @{int(x['bps'])}bps  "
          f"{x['CAGR']:.2%}/{x['Sharpe']:.3f}/{x['MaxDD']:.2%} halves {x['H1']:.3f}/{x['H2']:.3f} "
          f"OOS {x['OOS_Sharpe']:.3f} turn {x['turn_per_yr']:.2f}x")
    # --------------------------------------------- how isolated is any 4b passer?
    P("\n" + "=" * 100)
    P("4b NEIGHBOURHOOD — is a passing cell an island?  margins on each bar, and how many of")
    P("  its (m,j)-adjacent cells (same panel/rung) also pass.  A KEEP needs a plateau, not a point.")
    P("=" * 100)
    P(f"{'panel':6s} {'m':>4s} {'j':>4s} {'H1 marg':>8s} {'H2 marg':>8s} {'OOS marg':>9s} {'DD marg pp':>11s} "
      f"{'CAGR marg':>10s} {'nbrs pass':>10s}")
    for pan, gg, sp_, so_ in (("broad", grid[(grid.bps == 10)], spy, spy_oos_s), ("u56", t56, spy2, spy2_oos_s)):
        h_ = len(sp_) // 2
        s_h1, s_h2 = metrics(sp_.iloc[:h_])["Sharpe"], metrics(sp_.iloc[h_:])["Sharpe"]
        s_dd, s_cagr = abs(metrics(sp_)["MaxDD"]), metrics(sp_)["CAGR"]
        gg = gg.set_index(["m", "j"])
        for (mm, jj), x in gg[gg["keep4b"]].iterrows():
            mi, ji = MGRID.index(mm), JGRID.index(jj)
            nb = [(MGRID[a], JGRID[b_]) for a in (mi - 1, mi, mi + 1) for b_ in (ji - 1, ji, ji + 1)
                  if 0 <= a < len(MGRID) and 0 <= b_ < len(JGRID) and (a, b_) != (mi, ji)]
            npass_ = sum(int(gg.loc[k_, "keep4b"]) for k_ in nb)
            P(f"{pan:6s} {mm:4d} {jj:4d} {x['H1']-s_h1:+8.3f} {x['H2']-s_h2:+8.3f} "
              f"{x['OOS_Sharpe']-so_:+9.3f} {100*(0.60*s_dd-abs(x['MaxDD'])):+11.2f} "
              f"{100*(x['CAGR']-0.70*s_cagr):+10.2f} {npass_:>5d}/{len(nb):<4d}")
    P(f"  most common 4b failure modes: "
      + ", ".join(f"{kk}={vv}" for kk, vv in allg['fail4b'].value_counts().head(6).items()))
    Path(f"{OUT}.console.txt").write_text("\n".join(_LINES) + "\n")


if __name__ == "__main__":
    main()
