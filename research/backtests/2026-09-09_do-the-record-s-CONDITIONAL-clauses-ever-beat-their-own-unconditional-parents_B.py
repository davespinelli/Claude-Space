#!/usr/bin/env python3
"""IDEA 317 — do the record's CONDITIONAL clauses ever beat their own unconditional parents?
   (lane B, 2026-09-09)

QUESTION (QUEUE idea 317, verbatim)
    Idea 48's decisive test was not 4a/4b but 'does the conditional rule beat BOTH the rules it
    interpolates' (answer 4/16 full-sample, 0/16 on drawdown).  Audit every committed
    conditional/regime-switching book on the LEADERBOARD against that bar with its own two
    parents run at matched gross.  If conditional clauses systematically fail it, the bar
    belongs in PROTOCOL rule 4 as a precondition for KEEP, ahead of the half-sample tests.

WHAT THE BAR IS, STATED PRECISELY
    A conditional book is  C_t = A_t if the state is RISK-ON at close t, else B_t,  where A and
    B are two UNCONDITIONAL books (its parents).  The PARENTS TEST asks whether C beats BOTH
    A and B on the metric in question.  The test is only meaningful at MATCHED GROSS, because
    a conditional book that spends part of the sample in the lower-gross parent has lower
    average exposure than A and higher than B, and an unmatched Sharpe/MaxDD comparison then
    prices exposure, not conditioning.  Every book here — C, A and B — is rescaled so that its
    MEAN TARGET GROSS on rebalance days equals C's.  Scaling is applied to the WEIGHTS and the
    book is RE-RUN (not to the return series), so costs scale with it and the engine's own
    drift/normalisation semantics hold exactly.  No scaled book exceeds gross 1.0 (asserted).

    Idea 48 answered this on 16 cells of one clause family.  This is the record-wide census:
    6 clause families x 4 state families x 4 firing rates x 3 panels = 288 conditional books,
    each against its own two parents at matched gross.  ALL 288 are reported.

THE 6 CLAUSE FAMILIES (parent pairs), all drawn from the record's own book forms
    TREND    A=EWall (every priced name)          B=MA-DG  (only names above their 200d MA,
                                                            gated weight to CASH)
    VOLCAP   A=EWall                              B=VOLCAP-DG (drop vol20 >= 0.60, to CASH)
    WIDEN    A=TOP20 (composite score)            B=EWall     — idea 318's NF20 vs DIL-ALW pair
    CONC     A=TOP20                              B=TOP10     — idea 316's concentration pair
    GROSS    A=EWall @ gross 1.00                 B=EWall @ gross 0.375  — the de-gross switch
    DEFEND   A=TOP20 (momentum composite)         B=LOWVOL20 (20 lowest vol20 names)
    A is the RISK-ON leg, B the RISK-OFF leg, so C = "run A normally, switch to B in the bad
    state" — the shape of every regime clause in the record (breadth gate, dd de-gross,
    narrow-day widening, defensive rotation).

THE 4 STATE FAMILIES (all causal; risk-off when the signal is in its own bad tail)
    BREADTH  fraction of priced names above their own 200d MA        risk-off = LOW
    SPYTR    SPY / SPY.rolling(200).mean() - 1                       risk-off = LOW
    XVOL     cross-sectional mean of 20d realised vol                risk-off = HIGH
    DD       the RISK-ON parent's own drawdown from its running peak risk-off = DEEP
    Threshold = a TRAILING 5-YEAR (1260d, min 504) rolling quantile q of the signal, not an
    expanding one: idea 399 showed the expanding estimator under-fires its nominal q by 3-4x.
    Realised firing rates are reported for every (panel, state, q) so the reader can check.

TUNED PARAMETERS: 2 — (state family, q).  16 grid points, ALL reported for every one of the
    18 (panel x family) cells.  Everything else is PINNED and not tuned: base gross 0.75
    (1.00/0.375 inside GROSS by construction), weekly cadence, t+1, 10 bps, MA 200d, vol
    window 20d, vol cap 0.60, n = 10/20, quantile window 1260d.

GATES
    G1  the vectorised runner must reproduce `engine.backtest` to < 1e-12 on returns and
        turnover, checked on 4 books spanning all three panels.
    G2  matched-gross: |mean target gross of C, A_scaled, B_scaled| must agree to < 1e-12,
        and max scaled gross must be <= 1.0.
    G3  the DEGENERATE-PAIR check: report, per family, whether the two parents COLLAPSE TO THE
        SAME BOOK once gross is matched (max |A_Sharpe - B_Sharpe| over the family's cells).
        A pair that collapses makes the parents test a one-parent test and its pass rate is
        not comparable with the rest.

PLACEBO (the control that decides whether the bar has any power)
    Every cell is re-run with a PLACEBO state: the same risk-off mask circularly shifted by
    +504 and +1260 trading days.  A circular shift preserves the firing RATE exactly and the
    run-length clustering almost exactly, and destroys the alignment with the market state.
    Deterministic, no seed.  If placebo conditional books clear the parents test at the same
    rate as real ones, the bar separates nothing and does not belong in PROTOCOL rule 4.

RULE 8 (required, run for every cell)
    IS 2009-2016 (in-sample choice window), OOS 2017-01-01..end read ONCE.
    W1  per (panel, family): pick (state, q) by best IS Sharpe of C; read that cell's OOS
        CAGR/Sharpe/MaxDD once, against its two matched-gross parents, SPY and RULES v2.
    W2  the parents test itself re-read out of sample: OOS pass rate over all 288 cells.
    KEEP paths 4a and 4b evaluated for every conditional book AND for every parent.

PANELS / SURVIVORSHIP
    U56   research/universe.json  (56 cols incl. SPY; whole panel tradable, as the record's
          EWall uses it)
    B136  research/universe_broad.json (136 cols) — CURRENT constituents, survivorship
          overstates every LEVEL.
    SMALL research/../data/prices_small.csv.gz, the sub-$2B screen, less names with
          max_1d_move >= 1.0 in data/small_meta.csv -> 439 names.  SPY is a joined BENCHMARK,
          not a constituent, and is excluded from the tradable set on this panel.
    Every claim below is a book-vs-its-own-parents DIFFERENCE on a fixed panel.

Outputs (committed): .console.txt .cells.csv .rates.csv .placebo.csv .walkforward.csv .result.md
Deterministic; no network (load_universe reads committed caches).
"""
from __future__ import annotations
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa

STAMP = "2026-09-09_do-the-record-s-CONDITIONAL-clauses-ever-beat-their-own-unconditional-parents_B"
OUT = Path(__file__).resolve().parent
COST, FREQ = 10.0, "W"
G, MA_WIN, VOL_WIN, VOL_CAP = 0.75, 200, 20, 0.60
QWIN, QMIN = 1260, 504
IS_START, IS_END, OOS_START = "2009-01-01", "2016-12-31", "2017-01-01"
QS = (0.10, 0.20, 0.35, 0.50)
SHIFTS = (504, 1260)            # placebo: circular shift of the risk-off mask, in trading days
STATES = ("BREADTH", "SPYTR", "XVOL", "DD")
FAMS = ("TREND", "VOLCAP", "WIDEN", "CONC", "GROSS", "DEFEND")

_LOG: list[str] = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); _LOG.append(s)


# =============================================================== vectorised engine clone
def fast_bt(px: pd.DataFrame, W: pd.DataFrame, cost_bps=COST, freq=FREQ):
    """Closed-form equivalent of engine.backtest: same t+1 application, same weekly schedule,
    same intra-period drift with cash held flat, same turnover-based cost.

    Within a rebalance period starting at row s with target `new`, the engine's normalisation
    recursion has the closed form  held[t] = new * C[t]/C[s] / D[t],  where C[t] is the
    cumulative gross growth up to (not including) t and D[t] = sum_j new_j C_j[t]/C_j[s]
    + (1 - sum_j new_j).  Proven by induction; gate G1 checks it numerically.
    """
    idx = px.index
    rets = px.pct_change().fillna(0.0).to_numpy(float)
    wt = W.reindex(idx).fillna(0.0).shift(1).fillna(0.0).to_numpy(float)
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).to_numpy(bool).copy()
    mask[0] = True
    T, N = rets.shape
    Cs = np.empty((T, N))                       # Cs[t] = prod_{u<t}(1+ret_u)
    Cs[0] = 1.0
    np.cumprod(1.0 + rets[:-1], axis=0, out=Cs[1:])
    starts = np.flatnonzero(mask)
    seg = np.searchsorted(starts, np.arange(T), side="right") - 1
    s_of_t = starts[seg]
    new = wt[s_of_t]
    Gm = Cs / Cs[s_of_t]
    num = new * Gm
    D = num.sum(axis=1) + (1.0 - new.sum(axis=1))
    held = num / D[:, None]

    turn = np.zeros(T)
    turn[0] = np.abs(wt[0]).sum()
    later = starts[1:]
    if len(later):
        sp = starts[seg[later] - 1]             # previous period's start row
        prev_new = wt[sp]
        Gp = Cs[later] / Cs[sp]
        np_ = prev_new * Gp
        Dp = np_.sum(axis=1) + (1.0 - prev_new.sum(axis=1))
        cur_prev = np_ / Dp[:, None]
        turn[later] = np.abs(wt[later] - cur_prev).sum(axis=1)
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return pd.Series(port, index=idx), pd.Series(turn, index=idx)


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def mrow(r):
    m = metrics(r); h1, h2 = halves(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"], h1, h2


# =============================================================== book forms
def _ew(mask: pd.DataFrame, g: float) -> pd.DataFrame:
    n = mask.sum(axis=1).replace(0, np.nan)
    return g * mask.astype(float).div(n, axis=0).fillna(0.0)


def _topn(sc: pd.DataFrame, elig: pd.DataFrame, n: int, g: float) -> pd.DataFrame:
    s = sc.where(elig)
    rk = s.rank(axis=1, ascending=False)
    return _ew((rk <= n) & elig, g)


def build_books(px, tradable):
    """Every unconditional book form used as a parent, on one panel."""
    elig = px.notna() & pd.DataFrame(np.tile(tradable, (len(px), 1)), index=px.index,
                                     columns=px.columns)
    ma = (px > px.rolling(MA_WIN).mean()) & elig
    vol20 = px.pct_change().rolling(VOL_WIN).std() * np.sqrt(252)
    capok = (vol20 < VOL_CAP).fillna(False) & elig
    sc, _, _ = score(px, vol_scale=True)
    lowvol = (-vol20).where(elig)               # rank high = low vol
    B = {
        "EWall":     _ew(elig, G),
        "MA-DG":     _ew(ma, G).where(ma, 0.0),
        "VOLCAP-DG": _ew(elig, G).where(capok, 0.0),
        "TOP20":     _topn(sc, elig, 20, G),
        "TOP10":     _topn(sc, elig, 10, G),
        "EW-100":    _ew(elig, 1.00),
        "EW-0375":   _ew(elig, 0.375),
        "LOWVOL20":  _topn(lowvol, elig, 20, G),
    }
    return B, elig, ma, vol20


PAIRS = {                       # family -> (risk-ON parent A, risk-OFF parent B)
    "TREND":  ("EWall", "MA-DG"),
    "VOLCAP": ("EWall", "VOLCAP-DG"),
    "WIDEN":  ("TOP20", "EWall"),
    "CONC":   ("TOP20", "TOP10"),
    "GROSS":  ("EW-100", "EW-0375"),
    "DEFEND": ("TOP20", "LOWVOL20"),
}


# =============================================================== states
def build_states(px, elig, ma, vol20, riskon_ret: pd.Series):
    """Signals where LOW = risk-off, uniformly, so one tail and one knob q serve all four."""
    n = elig.sum(axis=1).replace(0, np.nan)
    breadth = (ma.sum(axis=1) / n).ffill()
    spyma = px["SPY"] / px["SPY"].rolling(MA_WIN).mean() - 1.0
    xvol = -(vol20.where(elig).mean(axis=1))                       # negate: LOW = risk-off
    eq = (1 + riskon_ret).cumprod()
    dd = eq / eq.cummax() - 1.0                                    # <= 0; LOW = deep = risk-off
    return {"BREADTH": breadth, "SPYTR": spyma, "XVOL": xvol, "DD": dd}


def risk_off_mask(sig: pd.Series, q: float) -> pd.Series:
    thr = sig.rolling(QWIN, min_periods=QMIN).quantile(q)
    return (sig < thr).fillna(False)


# =============================================================== per-panel run
def mean_gross(W, idx, freq=FREQ):
    m = rebalance_mask(idx, freq)
    return float(W.reindex(idx).fillna(0.0).sum(axis=1)[m].mean())


def build_C(WA, WB, off):
    return pd.DataFrame(np.where(off.to_numpy()[:, None], WB.to_numpy(), WA.to_numpy()),
                        index=WA.index, columns=WA.columns)


def parents_cell(px, WA, WB, gA, gB, off, start):
    """One conditional book plus its two matched-gross parents.  Returns (rC, rA, rB, gC)."""
    WC = build_C(WA, WB, off)
    gC = mean_gross(WC, px.index)
    kA, kB = (gC / gA if gA else 0.0), (gC / gB if gB else 0.0)
    assert max(gA * kA, gB * kB) <= 1.0 + 1e-9, "matched-gross would lever above 1.0"
    gg = (gC, mean_gross(WA * kA, px.index), mean_gross(WB * kB, px.index))
    assert max(gg) - min(gg) < 1e-12, gg                                    # G2
    return (fast_bt(px, WC)[0].loc[start:], fast_bt(px, WA * kA)[0].loc[start:],
            fast_bt(px, WB * kB)[0].loc[start:], gC)


def run_panel(pname, px, tradable, rows, rates, wf_rows, plc_rows):
    P("\n" + "=" * 112)
    P(f"PANEL {pname}: {len(px.columns)} cols, {int(tradable.sum())} tradable, "
      f"{px.index[0].date()}..{px.index[-1].date()} ({len(px)} rows)")
    books, elig, ma, vol20 = build_books(px, tradable)
    start = px.index[max(260, MA_WIN + 20)]
    idx = px.index

    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    b2, _ = fast_bt(px, rules_v2_weights(px))
    b2 = b2.loc[start:]
    P(f"  references  SPY      CAGR {metrics(spy)['CAGR']:7.2%} Sharpe {metrics(spy)['Sharpe']:6.3f} "
      f"MaxDD {metrics(spy)['MaxDD']:7.2%}  H1/H2 {halves(spy)[0]:.3f}/{halves(spy)[1]:.3f}")
    P(f"              RULESv2  CAGR {metrics(b2)['CAGR']:7.2%} Sharpe {metrics(b2)['Sharpe']:6.3f} "
      f"MaxDD {metrics(b2)['MaxDD']:7.2%}  H1/H2 {halves(b2)[0]:.3f}/{halves(b2)[1]:.3f}")
    spy_oos, b2_oos = spy.loc[OOS_START:], b2.loc[OOS_START:]
    ms, mo = metrics(spy), metrics(spy_oos)
    P(f"              SPY OOS  CAGR {mo['CAGR']:7.2%} Sharpe {mo['Sharpe']:6.3f} MaxDD {mo['MaxDD']:7.2%}")

    # risk-on parent returns feed the DD state
    ron_ret = {}
    for fam, (a, _b) in PAIRS.items():
        if a not in ron_ret:
            ron_ret[a] = fast_bt(px, books[a])[0]

    for fam in FAMS:
        an, bn = PAIRS[fam]
        WA, WB = books[an], books[bn]
        gA, gB = mean_gross(WA, idx), mean_gross(WB, idx)
        states = build_states(px, elig, ma, vol20, ron_ret[an])
        P(f"\n  --- family {fam}: A={an} (mean gross {gA:.4f})  B={bn} (mean gross {gB:.4f})")
        if gB == 0 or gA == 0:
            P("      DEGENERATE PARENT (all-cash): parents test ill-posed on MaxDD.")
        for st in STATES:
            sig = states[st]
            for q in QS:
                off = risk_off_mask(sig, q)
                rate = float(off.loc[start:].mean())
                rC, rA, rB, gC = parents_cell(px, WA, WB, gA, gB, off, start)
                rates.append(dict(panel=pname, family=fam, state=st, q=q, off_rate=rate,
                                  gA=gA, gB=gB, gC=gC))
                # ---- placebo: same mask, circularly shifted; same rate, no state alignment
                for sh in SHIFTS:
                    offp = pd.Series(np.roll(off.to_numpy(), sh), index=off.index)
                    pC, pA, pB, pgC = parents_cell(px, WA, WB, gA, gB, offp, start)
                    plc_rows.append(dict(
                        panel=pname, family=fam, state=st, q=q, shift=sh,
                        off_rate=float(offp.loc[start:].mean()), matched_gross=pgC,
                        C_Sharpe=metrics(pC)["Sharpe"], A_Sharpe=metrics(pA)["Sharpe"],
                        B_Sharpe=metrics(pB)["Sharpe"], C_MaxDD=metrics(pC)["MaxDD"],
                        A_MaxDD=metrics(pA)["MaxDD"], B_MaxDD=metrics(pB)["MaxDD"],
                        C_H1=halves(pC)[0], C_H2=halves(pC)[1],
                        A_H1=halves(pA)[0], A_H2=halves(pA)[1],
                        B_H1=halves(pB)[0], B_H2=halves(pB)[1],
                        C_oSharpe=metrics(pC.loc[OOS_START:])["Sharpe"],
                        A_oSharpe=metrics(pA.loc[OOS_START:])["Sharpe"],
                        B_oSharpe=metrics(pB.loc[OOS_START:])["Sharpe"]))
                rec = dict(panel=pname, family=fam, A=an, B=bn, state=st, q=q,
                           off_rate=rate, matched_gross=gC)
                for tag, r in (("C", rC), ("A", rA), ("B", rB)):
                    c, s, d, h1, h2 = mrow(r)
                    ro = r.loc[OOS_START:]
                    mo_ = metrics(ro)
                    rec.update({f"{tag}_CAGR": c, f"{tag}_Sharpe": s, f"{tag}_MaxDD": d,
                                f"{tag}_H1": h1, f"{tag}_H2": h2,
                                f"{tag}_oCAGR": mo_["CAGR"], f"{tag}_oSharpe": mo_["Sharpe"],
                                f"{tag}_oMaxDD": mo_["MaxDD"]})
                    ris = r.loc[IS_START:IS_END]
                    rec[f"{tag}_isSharpe"] = metrics(ris)["Sharpe"]
                # the parents test
                rec["pt_sharpe"] = bool(rec["C_Sharpe"] > rec["A_Sharpe"] and rec["C_Sharpe"] > rec["B_Sharpe"])
                rec["pt_dd"] = bool(rec["C_MaxDD"] > rec["A_MaxDD"] and rec["C_MaxDD"] > rec["B_MaxDD"])
                rec["pt_cagr"] = bool(rec["C_CAGR"] > rec["A_CAGR"] and rec["C_CAGR"] > rec["B_CAGR"])
                rec["pt_sharpe_h1"] = bool(rec["C_H1"] > rec["A_H1"] and rec["C_H1"] > rec["B_H1"])
                rec["pt_sharpe_h2"] = bool(rec["C_H2"] > rec["A_H2"] and rec["C_H2"] > rec["B_H2"])
                rec["pt_sharpe_oos"] = bool(rec["C_oSharpe"] > rec["A_oSharpe"] and rec["C_oSharpe"] > rec["B_oSharpe"])
                rec["pt_both_halves"] = bool(rec["pt_sharpe_h1"] and rec["pt_sharpe_h2"])
                # KEEP paths, for C and for both parents
                mb2, mspy = metrics(b2), metrics(spy)
                h1b, h2b = halves(b2); h1s, h2s = halves(spy)
                spyO = metrics(spy_oos)
                for tag in ("C", "A", "B"):
                    rec[f"{tag}_4a"] = bool(rec[f"{tag}_H1"] > h1b and rec[f"{tag}_H2"] > h2b
                                            and rec[f"{tag}_MaxDD"] >= mb2["MaxDD"])
                    rec[f"{tag}_4b"] = bool(rec[f"{tag}_H1"] > h1s and rec[f"{tag}_H2"] > h2s
                                            and rec[f"{tag}_oSharpe"] > spyO["Sharpe"]
                                            and abs(rec[f"{tag}_MaxDD"]) <= 0.60 * abs(mspy["MaxDD"])
                                            and rec[f"{tag}_CAGR"] >= 0.70 * mspy["CAGR"])
                rows.append(rec)
            P(f"      {st:8s} off-rate by q "
              + "  ".join(f"q={q:.2f}:{rates[-len(QS)+i]['off_rate']:.3f}" for i, q in enumerate(QS)))

    # ---- rule 8: per (panel, family) choose (state,q) on IS Sharpe, read OOS once
    df = pd.DataFrame([r for r in rows if r["panel"] == pname])
    for fam in FAMS:
        sub = df[df.family == fam]
        pick = sub.loc[sub.C_isSharpe.idxmax()]
        wf_rows.append(dict(panel=pname, family=fam, state=pick.state, q=pick.q,
                            IS_Sharpe=pick.C_isSharpe,
                            OOS_CAGR=pick.C_oCAGR, OOS_Sharpe=pick.C_oSharpe, OOS_MaxDD=pick.C_oMaxDD,
                            A_OOS_Sharpe=pick.A_oSharpe, B_OOS_Sharpe=pick.B_oSharpe,
                            A_OOS_CAGR=pick.A_oCAGR, B_OOS_CAGR=pick.B_oCAGR,
                            A_OOS_MaxDD=pick.A_oMaxDD, B_OOS_MaxDD=pick.B_oMaxDD,
                            SPY_OOS_CAGR=spyO["CAGR"], SPY_OOS_Sharpe=spyO["Sharpe"],
                            SPY_OOS_MaxDD=spyO["MaxDD"],
                            V2_OOS_CAGR=metrics(b2_oos)["CAGR"], V2_OOS_Sharpe=metrics(b2_oos)["Sharpe"],
                            V2_OOS_MaxDD=metrics(b2_oos)["MaxDD"],
                            pt_oos=bool(pick.pt_sharpe_oos), pt_full=bool(pick.pt_sharpe),
                            C_4a=bool(pick.C_4a), C_4b=bool(pick.C_4b)))
    return df


# =============================================================== gate G1
def gate_g1(px, W, label):
    r1, t1 = fast_bt(px, W)
    ref = backtest(px, W, cost_bps=COST, freq=FREQ)
    dr = float((r1 - ref["returns"]).abs().max())
    dt = float((t1 - ref["turnover"]).abs().max())
    P(f"  G1 {label:28s} max|dReturn| {dr:.3e}   max|dTurnover| {dt:.3e}")
    assert dr < 1e-12 and dt < 1e-12, (label, dr, dt)


def main():
    t0 = time.time()
    P("=" * 112)
    P("IDEA 317 — do the record's CONDITIONAL clauses ever beat their own unconditional parents?"
      "   (lane B, 2026-09-09)")
    P(f"  pinned: gross {G} (GROSS family 1.00/0.375), cadence {FREQ}, t+1, cost {COST:.0f} bps, "
      f"MA {MA_WIN}d, vol {VOL_WIN}d, cap {VOL_CAP}, n=10/20, quantile window {QWIN}d/min {QMIN}")
    P(f"  2 tuned parameters: state in {STATES} x q in {QS} -> 16 grid points, ALL reported")
    P(f"  {len(FAMS)} clause families x {len(STATES)*len(QS)} grid points x 3 panels = "
      f"{len(FAMS)*len(STATES)*len(QS)*3} conditional books, each vs its own 2 parents at matched gross")
    P("=" * 112)

    # panels
    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS_all = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    scols = [c for c in pxS_all.columns if c != "SPY" and c not in bad]
    pxS = pxS_all[scols + ["SPY"]].dropna(how="all").ffill()
    panels = [("U56", pxU, np.ones(len(pxU.columns), bool)),
              ("B136", pxB, np.ones(len(pxB.columns), bool)),
              ("SMALL439", pxS, np.array([c != "SPY" for c in pxS.columns]))]
    P(f"\nSMALL panel: {len([c for c in pxS_all.columns if c != 'SPY'])} names, dropped "
      f"{len([c for c in pxS_all.columns if c != 'SPY']) - len(scols)} with max_1d_move >= 1.0 "
      f"-> {len(scols)} tradable.  SPY joined as BENCHMARK only, excluded from the tradable set.")
    P("SURVIVORSHIP: B136 and SMALL439 are CURRENT constituents; every LEVEL is biased up. "
      "All claims are book-vs-its-own-parents differences on a fixed panel.")

    P("\nGATE G1 — vectorised runner vs engine.backtest")
    for nm, px, tr in panels:
        bks, *_ = build_books(px, tr)
        gate_g1(px, bks["EWall"], f"{nm}/EWall")
    gate_g1(pxU, build_books(pxU, panels[0][2])[0]["MA-DG"], "U56/MA-DG")
    gate_g1(pxU, rules_v2_weights(pxU), "U56/RULES v2")

    rows, rates, wf_rows, plc_rows = [], [], [], []
    for nm, px, tr in panels:
        run_panel(nm, px, tr, rows, rates, wf_rows, plc_rows)

    df = pd.DataFrame(rows)
    rt = pd.DataFrame(rates)
    wf = pd.DataFrame(wf_rows)
    plc = pd.DataFrame(plc_rows)
    plc["pt_sharpe"] = (plc.C_Sharpe > plc.A_Sharpe) & (plc.C_Sharpe > plc.B_Sharpe)
    plc["pt_both_halves"] = ((plc.C_H1 > plc.A_H1) & (plc.C_H1 > plc.B_H1)
                             & (plc.C_H2 > plc.A_H2) & (plc.C_H2 > plc.B_H2))
    plc["pt_sharpe_oos"] = (plc.C_oSharpe > plc.A_oSharpe) & (plc.C_oSharpe > plc.B_oSharpe)
    plc["pt_dd"] = (plc.C_MaxDD > plc.A_MaxDD) & (plc.C_MaxDD > plc.B_MaxDD)
    df.to_csv(OUT / f"{STAMP}.cells.csv", index=False)
    rt.to_csv(OUT / f"{STAMP}.rates.csv", index=False)
    wf.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    plc.to_csv(OUT / f"{STAMP}.placebo.csv", index=False)

    # =========================================================== the census
    P("\n" + "=" * 112)
    P("THE PARENTS TEST, RECORD-WIDE  (C must beat BOTH parents at matched gross)")
    P("=" * 112)
    n = len(df)
    # ---- G3: which parent pairs COLLAPSE once gross is matched?
    P("\n  GATE G3 — do the two parents collapse to the same book at matched gross?")
    degen = {}
    for fam in FAMS:
        s = df[df.family == fam]
        d = float((s.A_Sharpe - s.B_Sharpe).abs().max())
        degen[fam] = d < 1e-9
        P(f"    {fam:8s} max|A_Sharpe - B_Sharpe| = {d:.3e}"
          + ("   <-- DEGENERATE: matched gross collapses the pair to ONE book; its parents"
             " test is a one-parent test and is NOT comparable with the others." if degen[fam] else ""))
    df["degenerate_pair"] = df.family.map(degen)
    ndg = df[~df.degenerate_pair]
    P(f"    non-degenerate cells: {len(ndg)}/{n}")

    def pct(c): return f"{int(df[c].sum()):3d}/{n}  ({df[c].mean():6.1%})"
    P(f"  full-sample Sharpe          {pct('pt_sharpe')}")
    P(f"  H1 Sharpe alone             {pct('pt_sharpe_h1')}")
    P(f"  H2 Sharpe alone             {pct('pt_sharpe_h2')}")
    P(f"  BOTH halves Sharpe          {pct('pt_both_halves')}")
    P(f"  out-of-sample Sharpe        {pct('pt_sharpe_oos')}")
    P(f"  full-sample CAGR            {pct('pt_cagr')}")
    P(f"  full-sample MaxDD           {pct('pt_dd')}")
    P(f"  Sharpe AND MaxDD            {int((df.pt_sharpe & df.pt_dd).sum()):3d}/{n}  "
      f"({(df.pt_sharpe & df.pt_dd).mean():6.1%})")
    P(f"  Sharpe full AND both halves AND OOS   "
      f"{int((df.pt_sharpe & df.pt_both_halves & df.pt_sharpe_oos).sum()):3d}/{n}")

    P("\n  by clause family (full-sample Sharpe / both halves / OOS / MaxDD):")
    for fam in FAMS:
        s = df[df.family == fam]
        P(f"    {fam:8s} {s.pt_sharpe.sum():3d}/{len(s)}  {s.pt_both_halves.sum():3d}/{len(s)}"
          f"  {s.pt_sharpe_oos.sum():3d}/{len(s)}  {s.pt_dd.sum():3d}/{len(s)}")
    P("\n  by panel:")
    for pn in df.panel.unique():
        s = df[df.panel == pn]
        P(f"    {pn:9s} {s.pt_sharpe.sum():3d}/{len(s)}  {s.pt_both_halves.sum():3d}/{len(s)}"
          f"  {s.pt_sharpe_oos.sum():3d}/{len(s)}  {s.pt_dd.sum():3d}/{len(s)}")
    P("\n  by state family:")
    for st in STATES:
        s = df[df.state == st]
        P(f"    {st:8s} {s.pt_sharpe.sum():3d}/{len(s)}  {s.pt_both_halves.sum():3d}/{len(s)}"
          f"  {s.pt_sharpe_oos.sum():3d}/{len(s)}  {s.pt_dd.sum():3d}/{len(s)}")
    P("\n  by q (firing rate knob):")
    for q in QS:
        s = df[df.q == q]
        P(f"    q={q:.2f}   {s.pt_sharpe.sum():3d}/{len(s)}  {s.pt_both_halves.sum():3d}/{len(s)}"
          f"  {s.pt_sharpe_oos.sum():3d}/{len(s)}  {s.pt_dd.sum():3d}/{len(s)}"
          f"   mean off-rate {s.off_rate.mean():.3f}")

    # =========================================================== PLACEBO
    P("\n" + "=" * 112)
    P("PLACEBO — the SAME risk-off masks circularly shifted +504 / +1260 trading days")
    P("  (identical firing rate and clustering, no alignment with the market state)")
    P("=" * 112)
    P(f"  {'arm':22s} {'cells':>6s} {'fullSharpe':>12s} {'bothHalves':>12s} {'OOS':>10s} {'MaxDD':>10s}")
    def line(lbl, d):
        P(f"  {lbl:22s} {len(d):6d} {d.pt_sharpe.mean():11.1%} {d.pt_both_halves.mean():11.1%}"
          f" {d.pt_sharpe_oos.mean():9.1%} {d.pt_dd.mean():9.1%}")
    line("REAL states", df)
    for sh in SHIFTS:
        line(f"PLACEBO shift +{sh}d", plc[plc["shift"] == sh])
    line("PLACEBO pooled", plc)
    P("\n  ex-degenerate (GROSS dropped), the same four columns:")
    line("REAL ex-degenerate", ndg)
    plc["marg_S"] = plc.C_Sharpe - plc[["A_Sharpe", "B_Sharpe"]].max(axis=1)
    pl_nd = plc[~plc.family.map(degen)]
    line("PLACEBO ex-degenerate", pl_nd)
    P("\n  by clause family, REAL vs PLACEBO-pooled full-sample-Sharpe pass rate:")
    P(f"    {'family':8s} {'REAL':>8s} {'PLACEBO':>8s} {'diff':>8s} | {'REAL bothH':>11s} {'PLC bothH':>10s}")
    for fam in FAMS:
        a, b = df[df.family == fam], plc[plc.family == fam]
        P(f"    {fam:8s} {a.pt_sharpe.mean():8.1%} {b.pt_sharpe.mean():8.1%} "
          f"{a.pt_sharpe.mean() - b.pt_sharpe.mean():+8.1%} | {a.pt_both_halves.mean():11.1%}"
          f" {b.pt_both_halves.mean():10.1%}")
    P("\n  median Sharpe margin over the better parent, REAL vs PLACEBO:")
    dmarg = df.C_Sharpe - df[["A_Sharpe", "B_Sharpe"]].max(axis=1)
    P(f"    REAL    median {dmarg.median():+.4f}   mean {dmarg.mean():+.4f}")
    P(f"    PLACEBO median {plc.marg_S.median():+.4f}   mean {plc.marg_S.mean():+.4f}")
    P(f"    REAL ex-degenerate    median {(ndg.C_Sharpe - ndg[['A_Sharpe','B_Sharpe']].max(axis=1)).median():+.4f}")
    P(f"    PLACEBO ex-degenerate median {pl_nd.marg_S.median():+.4f}")

    P("\n  MEDIAN margin of C over the BETTER parent (Sharpe), by family x panel:")
    df["best_par_S"] = df[["A_Sharpe", "B_Sharpe"]].max(axis=1)
    df["marg_S"] = df.C_Sharpe - df.best_par_S
    df["best_par_D"] = df[["A_MaxDD", "B_MaxDD"]].max(axis=1)
    df["marg_D"] = df.C_MaxDD - df.best_par_D
    piv = df.pivot_table(index="family", columns="panel", values="marg_S", aggfunc="median")
    P(piv.to_string(float_format=lambda x: f"{x:+.4f}"))
    P("\n  MEDIAN margin of C over the SHALLOWER-drawdown parent (pp, + = C is shallower):")
    pivd = df.pivot_table(index="family", columns="panel", values="marg_D", aggfunc="median") * 100
    P(pivd.to_string(float_format=lambda x: f"{x:+.3f}"))

    P("\n  BEST cell per (panel, family) by full-sample Sharpe margin over the better parent:")
    P(f"    {'panel':10s} {'family':8s} {'state':8s} {'q':>5s} {'C_Sh':>7s} {'A_Sh':>7s} {'B_Sh':>7s}"
      f" {'marg':>7s} {'C_DD':>8s} {'best_DD':>8s} {'ptS':>4s} {'ptDD':>5s}")
    for pn in df.panel.unique():
        for fam in FAMS:
            s = df[(df.panel == pn) & (df.family == fam)]
            r = s.loc[s.marg_S.idxmax()]
            P(f"    {pn:10s} {fam:8s} {r.state:8s} {r.q:5.2f} {r.C_Sharpe:7.3f} {r.A_Sharpe:7.3f}"
              f" {r.B_Sharpe:7.3f} {r.marg_S:+7.3f} {r.C_MaxDD:8.2%} {r.best_par_D:8.2%}"
              f" {str(bool(r.pt_sharpe)):>4s} {str(bool(r.pt_dd)):>5s}")

    # =========================================================== ALL grid points
    P("\n" + "=" * 112)
    P("ALL 288 GRID POINTS (matched gross; C vs A vs B; * marks a parents-test pass on Sharpe)")
    P("=" * 112)
    P(f"{'panel':9s} {'fam':7s} {'state':8s} {'q':>5s} {'off':>5s} {'g':>5s} | "
      f"{'C_CAGR':>7s} {'C_Sh':>6s} {'C_DD':>7s} {'C_H1':>6s} {'C_H2':>6s} {'C_oSh':>6s} | "
      f"{'A_Sh':>6s} {'B_Sh':>6s} {'A_DD':>7s} {'B_DD':>7s} | {'ptS':>3s} {'ptH':>3s} {'ptO':>3s} "
      f"{'ptD':>3s} {'4a':>2s} {'4b':>2s}")
    for _, r in df.iterrows():
        P(f"{r.panel:9s} {r.family:7s} {r.state:8s} {r.q:5.2f} {r.off_rate:5.3f} {r.matched_gross:5.3f} | "
          f"{r.C_CAGR:7.2%} {r.C_Sharpe:6.3f} {r.C_MaxDD:7.2%} {r.C_H1:6.3f} {r.C_H2:6.3f} {r.C_oSharpe:6.3f} | "
          f"{r.A_Sharpe:6.3f} {r.B_Sharpe:6.3f} {r.A_MaxDD:7.2%} {r.B_MaxDD:7.2%} | "
          f"{'*' if r.pt_sharpe else '.':>3s} {'*' if r.pt_both_halves else '.':>3s} "
          f"{'*' if r.pt_sharpe_oos else '.':>3s} {'*' if r.pt_dd else '.':>3s} "
          f"{'Y' if r.C_4a else '.':>2s} {'Y' if r.C_4b else '.':>2s}")

    # =========================================================== rule 8
    P("\n" + "=" * 112)
    P("RULE 8 WALK-FORWARD — (state,q) chosen on IS 2009-2016 Sharpe, OOS 2017-2026 read once")
    P("=" * 112)
    P(f"  {'panel':10s} {'family':8s} {'pick':16s} {'IS_Sh':>6s} | {'OOS CAGR':>9s} {'Sh':>6s} "
      f"{'MaxDD':>8s} | {'A oSh':>6s} {'B oSh':>6s} {'ptOOS':>6s} | {'SPY oSh':>7s} {'v2 oSh':>7s}")
    for _, r in wf.iterrows():
        P(f"  {r.panel:10s} {r.family:8s} {r.state + '/' + format(r.q, '.2f'):16s} {r.IS_Sharpe:6.3f} | "
          f"{r.OOS_CAGR:9.2%} {r.OOS_Sharpe:6.3f} {r.OOS_MaxDD:8.2%} | {r.A_OOS_Sharpe:6.3f} "
          f"{r.B_OOS_Sharpe:6.3f} {str(bool(r.pt_oos)):>6s} | {r.SPY_OOS_Sharpe:7.3f} {r.V2_OOS_Sharpe:7.3f}")
    P(f"\n  rule-8 picks that beat BOTH parents OOS: {int(wf.pt_oos.sum())}/{len(wf)}")
    P(f"  rule-8 picks that beat SPY OOS on Sharpe: "
      f"{int((wf.OOS_Sharpe > wf.SPY_OOS_Sharpe).sum())}/{len(wf)}")
    P(f"  rule-8 picks whose OOS CAGR >= 70% of SPY: "
      f"{int((wf.OOS_CAGR >= 0.70 * wf.SPY_OOS_CAGR).sum())}/{len(wf)}")
    P(f"  IS->OOS parents-test agreement over all {n} cells: "
      f"{int((df.pt_sharpe == df.pt_sharpe_oos).sum())}/{n}")

    # =========================================================== KEEP paths
    P("\n" + "=" * 112)
    P("KEEP PATHS 4a / 4b — evaluated for every conditional book AND every matched-gross parent")
    P("=" * 112)
    P(f"  conditional books C:  4a {int(df.C_4a.sum()):3d}/{n}   4b {int(df.C_4b.sum()):3d}/{n}")
    P(f"  risk-on parents  A:   4a {int(df.A_4a.sum()):3d}/{n}   4b {int(df.A_4b.sum()):3d}/{n}")
    P(f"  risk-off parents B:   4a {int(df.B_4a.sum()):3d}/{n}   4b {int(df.B_4b.sum()):3d}/{n}")
    keep = df[df.C_4b]
    P(f"\n  4b passes among conditional books: {len(keep)}")
    if len(keep):
        P(f"    of those, how many ALSO clear the parents test on Sharpe: {int(keep.pt_sharpe.sum())}")
        P(f"    of those, how many ALSO clear it OOS:                    {int(keep.pt_sharpe_oos.sum())}")
        for _, r in keep.iterrows():
            P(f"      {r.panel:9s} {r.family:7s} {r.state:8s} q={r.q:.2f}  C_Sh {r.C_Sharpe:.3f} "
              f"vs A {r.A_Sharpe:.3f} / B {r.B_Sharpe:.3f}   ptS={bool(r.pt_sharpe)} "
              f"ptOOS={bool(r.pt_sharpe_oos)}")
    P("\n  THE PROTOCOL QUESTION — would the parents bar, placed AHEAD of 4a/4b, change any verdict?")
    for lbl, colk in (("4a", "C_4a"), ("4b", "C_4b")):
        k = df[df[colk]]
        if len(k) == 0:
            P(f"    {lbl}: 0 passes, nothing to screen."); continue
        P(f"    {lbl}: {len(k)} passes; parents bar would REJECT {int((~k.pt_sharpe).sum())} of them "
          f"({(~k.pt_sharpe).mean():.1%}) on full-sample Sharpe, "
          f"{int((~k.pt_both_halves).sum())} ({(~k.pt_both_halves).mean():.1%}) on BOTH halves, "
          f"and {int((~(k.pt_sharpe & k.pt_dd)).sum())} on Sharpe+MaxDD.")
        kn = k[~k.degenerate_pair]
        P(f"        ex-degenerate ({len(kn)} passes): reject {int((~kn.pt_sharpe).sum())} full-sample, "
          f"{int((~kn.pt_both_halves).sum())} on both halves.")
    P("\n    Does the bar SEPARATE real conditioning from a shifted mask?  A screen is only worth")
    P("    a PROTOCOL clause if it rejects placebo books more often than real ones:")
    P(f"      full-sample Sharpe   REAL {df.pt_sharpe.mean():.1%}  vs  PLACEBO {plc.pt_sharpe.mean():.1%}"
      f"   -> lift {df.pt_sharpe.mean() - plc.pt_sharpe.mean():+.1%}")
    P(f"      BOTH halves          REAL {df.pt_both_halves.mean():.1%}  vs  PLACEBO "
      f"{plc.pt_both_halves.mean():.1%}   -> lift {df.pt_both_halves.mean() - plc.pt_both_halves.mean():+.1%}")

    P(f"\nelapsed {time.time() - t0:.1f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
