#!/usr/bin/env python3
"""Idea 322 - does the CLAUSE FAMILY ever beat BOTH parents?

Idea 317 asked whether the record's conditional clauses beat their own unconditional
parents and found they almost never do; ideas 316 (concentration) and 318 (widening) each
failed it on the two nominated panels, on opposite signs of the same flag.  This run makes
the test a CENSUS over the five conditional clauses the record has actually PARKed or KEPT
rather than over an abstract 'conditional form':

    BREADTHCASH  hold cash while panel breadth (share above 200d MA) sits below a level
    HIVOL        halve gross while SPY 20d realised vol sits above a quantile  (hivol80 arming)
    DDCTL        halve gross while the book's own drawdown is deeper than x    (ddctl)
    BAND         hold only names inside their own 200d +/- b band              (RULES v2's band)
    VOLSCALE     select on the vol-scaled composite while panel vol is high    (the vol scaler)

Every clause is run as 'do A while state S is ON, do B while OFF', and BOTH unconditional
parents (always-A, always-B) are run at the same gross, cadence, cost and panel.  A clause
passes the PARENTS TEST only if the conditional book beats BOTH parents on Sharpe.  Two
of the five families (BREADTHCASH, BAND) have a DEGENERATE always-A parent - cash, whose
Sharpe is 0 by construction - and that is reported rather than hidden: for those two the
test collapses to 'beat the ungated book', which is the weaker bar, so any pass there is
the easiest possible pass.

Base book B0 on every panel: CAND-20 (top 20 by the composite score, NO vol scaler, equal
weight, gross 1.0), the 2026-09-04 KEEP 4b family.  Weekly cadence, 10 bps per unit
turnover, weights decided at close t and applied t+1.

Two tuned parameters: (clause family, threshold).  All 45 grid points reported.
SMALL panel: tickers with max_1d_move >= 1.0 dropped; SURVIVORSHIP - current constituents
of the sub-$2B screen only (data/SMALL_PANEL_README.md).
"""
import sys, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score, band_state  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, metrics, rebalance_mask  # noqa

COST_BPS = 10.0
FREQ = "W"
IS_END = pd.Timestamp("2016-12-31")
OOS_START = pd.Timestamp("2017-01-01")
pd.set_option("display.width", 240, "display.max_columns", 80, "display.max_rows", 400)


# ----------------------------------------------------------------------------- machinery
def fast_backtest(px, w, cost_bps=COST_BPS, freq=FREQ):
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    cur = np.zeros(px.shape[1]); held = np.empty_like(wt); turn = np.zeros(len(px))
    for i in range(len(px)):
        if mask[i] or i == 0:
            new = wt[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return pd.Series(port, index=px.index)


def M(r):
    """CAGR / Sharpe / MaxDD, with an all-cash book scored as Sharpe 0 rather than NaN."""
    m = metrics(r)
    s = m["Sharpe"]
    if not np.isfinite(s): s = 0.0
    return m["CAGR"], s, m["MaxDD"]


def halves(r):
    h = len(r) // 2
    a, b = metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]
    return (0.0 if not np.isfinite(a) else a), (0.0 if not np.isfinite(b) else b)


def cand_weights(px, n=20, vol_scale=False, gross=1.0):
    s, above, vol20 = score(px, vol_scale=vol_scale)
    s = s.drop(columns=["SPY"], errors="ignore").reindex(columns=px.columns).where(px.notna())
    sel = (s.rank(axis=1, ascending=False) <= n).astype(float)
    cnt = sel.sum(axis=1).replace(0, np.nan)
    return (sel.div(cnt, axis=0) * gross).fillna(0.0)


# ------------------------------------------------------------------------ clause states
def states(px, base_ret):
    """(family, threshold) -> boolean state S (True = clause ARMED / action A taken).
    Every state is knowable at close t; the engine applies the weight at t+1."""
    out = {}
    core = px.drop(columns=["SPY"], errors="ignore")
    spy = px["SPY"] if "SPY" in px.columns else px.mean(axis=1)
    br = (core > core.rolling(200).mean()).sum(axis=1) / core.rolling(200).mean().notna().sum(axis=1).replace(0, np.nan)
    for q in (0.30, 0.40, 0.50):
        out[("BREADTHCASH", q)] = (br < q).fillna(True)          # ARMED = go to cash
    rv = spy.pct_change().rolling(20).std() * np.sqrt(252)
    for q in (0.70, 0.80, 0.90):
        out[("HIVOL", q)] = (rv >= rv.expanding(252).quantile(q)).fillna(False)
    eq = (1 + base_ret).cumprod()
    dd = eq / eq.cummax() - 1.0
    for x in (0.05, 0.10, 0.15):
        out[("DDCTL", x)] = (dd <= -x).fillna(False)
    for q in (0.50, 0.70, 0.85):
        out[("VOLSCALE", q)] = (rv >= rv.expanding(252).quantile(q)).fillna(False)
    return out


def clause_books(px, fam, thr, S, base_w):
    """Return (conditional, parentA = always-armed, parentB = always-off) WEIGHT frames."""
    if fam == "BREADTHCASH":
        A = base_w * 0.0                                          # cash (degenerate parent)
        B = base_w
    elif fam in ("HIVOL", "DDCTL"):
        A = base_w * 0.5                                          # half gross
        B = base_w
    elif fam == "VOLSCALE":
        A = cand_weights(px, 20, vol_scale=True)
        B = base_w
    elif fam == "BAND":
        # A PER-NAME state: name i is held while it sits inside its own 200d +/- b band and
        # de-grossed to cash otherwise.  Its two unconditional parents are therefore 'hold
        # every selected name always' (= base_w) and 'hold none of them' (= cash), the same
        # degenerate pair BREADTHCASH has; there is no non-degenerate always-armed book for a
        # per-name gate.  Flagged as degenerate in the output.
        bs = band_state(px, band=thr).reindex(columns=base_w.columns).fillna(False)
        C = base_w.where(bs, 0.0)
        return C, base_w * 0.0, base_w
    else:
        raise ValueError(fam)
    s = S.reindex(px.index).fillna(False)
    C = A.where(s, B)
    return C, A, B


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    print(f"  SMALL: dropped {len(px.columns) - len(keep)} names with max_1d_move >= 1.0")
    return px[keep]


# ----------------------------------------------------------------------------- GATES
def gates(px):
    print("\n" + "=" * 110)
    print("GATES (pre-registered, printed before any hypothesis is read)")
    print("=" * 110)
    w = cand_weights(px, 20)
    r = fast_backtest(px, w)
    eng = engine_backtest(px, w, cost_bps=COST_BPS, freq=FREQ)
    d = float(np.abs(r - eng["returns"]).max())
    g1 = d < 1e-12
    print(f"G1 fast_backtest vs engine.backtest on U56/CAND-20: max|dret| {d:.3e} -> {'PASS' if g1 else 'FAIL'}")

    rv1 = fast_backtest(px, rules_v1_weights(px)).loc[px.index[260]:]
    c, s, m = M(rv1)
    g2 = abs(c - 0.064194) < 5e-4 and abs(s - 0.66110) < 5e-3 and abs(m + 0.138278) < 5e-3
    print(f"G2 U56/RULES v1 rebuild {c:.4%} / {s:.5f} / {m:.4%} vs published 6.4194% / 0.66110 / -13.8278% -> {'PASS' if g2 else 'FAIL'}")

    # G3 - a clause whose state is ALWAYS ON must equal its own parent A exactly, and a
    # clause whose state is NEVER on must equal parent B exactly.  This is what makes the
    # parents test a test of the CLAUSE and not of two unrelated books.
    base_w = cand_weights(px, 20)
    S_on = pd.Series(True, index=px.index); S_off = pd.Series(False, index=px.index)
    Con, A, B = clause_books(px, "HIVOL", 0.80, S_on, base_w)
    Coff, _, _ = clause_books(px, "HIVOL", 0.80, S_off, base_w)
    d_on = float(np.abs(fast_backtest(px, Con) - fast_backtest(px, A)).max())
    d_off = float(np.abs(fast_backtest(px, Coff) - fast_backtest(px, B)).max())
    g3 = d_on < 1e-15 and d_off < 1e-15
    print(f"G3 clause identity: always-ON vs parent A {d_on:.3e}; never-ON vs parent B {d_off:.3e} -> {'PASS' if g3 else 'FAIL'}")
    print(f"GATES: {'ALL PASS' if (g1 and g2 and g3) else 'FAILURE - read nothing below'}")
    return g1 and g2 and g3


# ------------------------------------------------------------------------- the census
def run_panel(pname, px, rows):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0.0)
    base_v2 = fast_backtest(px, rules_v2_weights(px))
    base_w = cand_weights(px, 20)
    r0 = fast_backtest(px, base_w)
    St = states(px, r0)
    grid = list(St.items()) + [(("BAND", b), None) for b in (0.00, 0.03, 0.06)]
    for (fam, thr), S in grid:
        if S is None:
            S = pd.Series(True, index=px.index)
        C, A, B = clause_books(px, fam, thr, S, base_w)
        rC, rA, rB = (fast_backtest(px, x) for x in (C, A, B))
        if fam == "BAND":     # share of the base book's gross that the per-name band leaves on
            armed = float((C.loc[start:].sum(axis=1) / B.loc[start:].sum(axis=1).replace(0, np.nan)).mean())
        else:
            armed = float(S.loc[start:].mean())
        for seg, sl in (("FULL", slice(start, None)), ("OOS", slice(OOS_START, None)),
                        ("H1", None), ("H2", None)):
            if seg in ("H1", "H2"):
                rr = rC.loc[start:]; n = len(rr) // 2
                sub = (slice(rr.index[0], rr.index[n - 1]) if seg == "H1" else slice(rr.index[n], None))
            else:
                sub = sl
            cC, sC, mC = M(rC.loc[sub]); cA, sA, mA = M(rA.loc[sub]); cB, sB, mB = M(rB.loc[sub])
            cS, sS, mS = M(spy.loc[sub]); cL, sL, mL = M(base_v2.loc[sub])
            h1, h2 = halves(rC.loc[sl]) if seg in ("FULL", "OOS") else (np.nan, np.nan)
            p4a = (h1 > halves(base_v2.loc[sl])[0] and h2 > halves(base_v2.loc[sl])[1]
                   and mC >= mL) if seg in ("FULL", "OOS") else False
            p4b = (h1 > halves(spy.loc[sl])[0] and h2 > halves(spy.loc[sl])[1]
                   and mC >= 0.60 * mS and cC >= 0.70 * cS) if seg in ("FULL", "OOS") else False
            rows.append(dict(panel=pname, family=fam, thr=thr, seg=seg, armed_share=armed,
                             CAGR=cC, Sharpe=sC, MaxDD=mC, H1=h1, H2=h2,
                             pA_Sharpe=sA, pB_Sharpe=sB, pA_CAGR=cA, pB_CAGR=cB,
                             beats_both=(sC > sA and sC > sB),
                             beats_both_cagr=(cC > cA and cC > cB),
                             degenerate_parentA=fam in ("BREADTHCASH", "BAND"),
                             spy_Sharpe=sS, live_Sharpe=sL, p4a=p4a, p4b=p4b))
    return base_v2, spy, r0


def main():
    print("Idea 322 - does the clause family EVER beat both parents?")
    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL": small_panel()}
    for k, v in panels.items():
        print(f"  {k}: {v.shape[0]} rows x {v.shape[1]} cols  {v.index[0].date()} .. {v.index[-1].date()}")
    if not gates(panels["U56"]):
        print("GATE FAILURE - stopping."); return

    print("\n" + "=" * 110)
    print("THE CENSUS - 5 clause families x 3 thresholds x 3 panels = 45 conditional books,")
    print("each against BOTH unconditional parents at matched gross/cadence/cost. ALL reported.")
    print("=" * 110)
    rows, ctx = [], {}
    for pname, px in panels.items():
        ctx[pname] = run_panel(pname, px, rows)
    df = pd.DataFrame(rows)

    show = df[df.seg.isin(["FULL", "OOS"])].copy()
    print(show[["panel", "family", "thr", "seg", "armed_share", "CAGR", "Sharpe", "MaxDD",
                "pA_Sharpe", "pB_Sharpe", "beats_both", "p4a", "p4b"]]
          .to_string(index=False, float_format=lambda v: f"{v:.3f}"))

    print("\n--- THE PARENTS TEST ---")
    for seg in ("FULL", "OOS"):
        s = df[df.seg == seg]
        nd = s[~s.degenerate_parentA]
        print(f"{seg}: beats BOTH parents on Sharpe {int(s.beats_both.sum())}/{len(s)}  "
              f"(non-degenerate families only: {int(nd.beats_both.sum())}/{len(nd)});  "
              f"on CAGR {int(s.beats_both_cagr.sum())}/{len(s)}")
    fam_tbl = df[df.seg == "OOS"].groupby("family").agg(
        n=("beats_both", "size"), beats_both=("beats_both", "sum"),
        med_Sharpe=("Sharpe", "median"), med_pA=("pA_Sharpe", "median"), med_pB=("pB_Sharpe", "median"),
        p4a=("p4a", "sum"), p4b=("p4b", "sum"))
    print("\nOOS by family (all panels pooled):")
    print(fam_tbl.to_string(float_format=lambda v: f"{v:.3f}"))

    print("\n" + "=" * 110)
    print("RULE 8 - threshold chosen per (panel, family) on IS <= 2016-12-31 Sharpe, OOS read ONCE")
    print("=" * 110)
    wf = []
    for pname, px in panels.items():
        base_v2, spy, r0 = ctx[pname]
        start = px.index[260]
        base_w = cand_weights(px, 20)
        St = states(px, r0)
        grid = list(St.items()) + [(("BAND", b), None) for b in (0.00, 0.03, 0.06)]
        by_fam = {}
        for (fam, thr), S in grid:
            if S is None: S = pd.Series(True, index=px.index)
            C, A, B = clause_books(px, fam, thr, S, base_w)
            rC, rA, rB = (fast_backtest(px, x) for x in (C, A, B))
            s_is = M(rC.loc[start:IS_END])[1]
            by_fam.setdefault(fam, []).append((thr, s_is, rC, rA, rB))
        for fam, lst in by_fam.items():
            lst.sort(key=lambda z: -z[1])
            thr, s_is, rC, rA, rB = lst[0]
            cC, sC, mC = M(rC.loc[OOS_START:]); cA, sA, mA = M(rA.loc[OOS_START:]); cB, sB, mB = M(rB.loc[OOS_START:])
            cS, sS, mS = M(spy.loc[OOS_START:]); cL, sL, mL = M(base_v2.loc[OOS_START:])
            h1, h2 = halves(rC.loc[OOS_START:]); l1, l2 = halves(base_v2.loc[OOS_START:]); y1, y2 = halves(spy.loc[OOS_START:])
            p4a = h1 > l1 and h2 > l2 and mC >= mL
            p4b = h1 > y1 and h2 > y2 and mC >= 0.60 * mS and cC >= 0.70 * cS
            print(f"{pname:6s} {fam:12s} IS pick thr={thr} (IS Sharpe {s_is:.3f}) | OOS book {cC:7.2%} / {sC:6.3f} / {mC:7.2%}"
                  f" | parents A {sA:6.3f}  B {sB:6.3f} | beats both {str(sC > sA and sC > sB):5s}"
                  f" | live {sL:.3f}  SPY {sS:.3f} | 4a {'PASS' if p4a else 'fail'} 4b {'PASS' if p4b else 'fail'}"
                  f" | all IS: " + " ".join(f"{t}={s:.3f}" for t, s, *_ in lst))
            wf.append(dict(panel=pname, family=fam, thr=thr, is_Sharpe=s_is, oos_CAGR=cC, oos_Sharpe=sC,
                           oos_MaxDD=mC, pA=sA, pB=sB, beats_both=(sC > sA and sC > sB),
                           live=sL, spy=sS, p4a=p4a, p4b=p4b))
        print(f"{pname:6s} reference OOS: base CAND-20 {M(r0.loc[OOS_START:])[0]:.2%} / {M(r0.loc[OOS_START:])[1]:.3f} / {M(r0.loc[OOS_START:])[2]:.2%}"
              f" | RULES v2 (live) {cL:.2%} / {sL:.3f} / {mL:.2%} | SPY {cS:.2%} / {sS:.3f} / {mS:.2%}")
    wfd = pd.DataFrame(wf)

    stem = "2026-09-09_does-the-clause-family-EVER-beat-both-parents_cloud"
    df.to_csv(ROOT / "research" / "backtests" / f"{stem}.cells.csv", index=False)
    wfd.to_csv(ROOT / "research" / "backtests" / f"{stem}.wf.csv", index=False)

    print("\n" + "=" * 110)
    print("SUMMARY")
    print("=" * 110)
    oos = df[df.seg == "OOS"]
    nd = oos[~oos.degenerate_parentA]
    print(f"census: {int(oos.beats_both.sum())}/{len(oos)} conditional books beat BOTH parents on OOS Sharpe "
          f"({int(nd.beats_both.sum())}/{len(nd)} among the three families with a non-degenerate always-armed parent)")
    print(f"rule 8: {int(wfd.beats_both.sum())}/{len(wfd)} IS-chosen clauses beat both parents OOS; "
          f"4a {int(wfd.p4a.sum())}/{len(wfd)}, 4b {int(wfd.p4b.sum())}/{len(wfd)}")
    print(f"wrote {stem}.cells.csv ({len(df)} rows) and {stem}.wf.csv ({len(wfd)} rows)")


if __name__ == "__main__":
    main()
