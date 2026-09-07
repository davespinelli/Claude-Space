#!/usr/bin/env python3
"""Idea 318 - "does-WIDENING-into-narrow-markets-beat-the-broad-leg" (lane cloud).

The question
------------
Idea 316 (2026-09-07) killed the narrow-day CONCENTRATION clause.  Its sign test was the
strongest part of the kill: DILUTE - the same causal breadth flag doing the OPPOSITE thing,
widening the book to min(2*n0, E_t) names at the same 75% gross - beat CONC on 3/3 panels and
beat the clause-free NF20 on U56 (1.073 / -18.0% vs 1.070 / -18.3%, 4b PASS).  That was ONE
unswept point (q = 0.20, multiple = 2) run as a control, never as a candidate.  This run
sweeps the widening multiple and q properly on all three panels and asks whether the U56 edge
is a grid artefact.

The book under test
-------------------
    k_broad,t = min(n0, E_t)                                     n0 = 20, the record's count
    DILUTE(q, m):  narrow if E_t <= Quantile_q(E_{<=t-1})  ->  k_t = min(round(m * n0), E_t)
                   broad  otherwise                         ->  k_t = k_broad,t
    equal weight GROSS / k_t either way, so realised gross is 0.75 in BOTH regimes.

Gross is matched by construction, so d = r(DILUTE) - r(NF20) is WIDTH and nothing else - the
same accounting idea 316 used for concentration, with the sign reversed.

Tuned parameters (PROTOCOL rule 4: at most two) - q and m.  ALL 4 x 4 = 16 points are reported
on EACH of U56 / B136 / SMALL439 = 48 points.  Everything else is fixed in advance and not
searched: n0 = 20, GROSS = 0.75, scorer without /sqrt(vol20) (idea 2's), 200d + vol20 < 0.60
eligibility, weekly rebalance, 10 bps, t+1 execution, 252-observation minimum for the causal
quantile, IS = start..2016, OOS = 2017.. (rule 8).

Controls (NOT tuned, none selected on its own result)
-----------------------------------------------------
    NF20        the broad leg with the clause deleted                      (parent 1)
    DIL-ALW m   k = min(round(m*n0), E_t) on EVERY day, one arm per m      (parent 2)
    EWALL       k = E_t always: the limit of widening, at the same gross
    CONC q0.20 c0.35   idea 316's killed clause, for sign continuity
    RULES v2 (live), RULES v1, SPY

The decisive test is idea 317's bar, not 4a/4b: a CONDITIONAL clause is only real if it beats
BOTH the unconditional rules it interpolates.  DILUTE(q, m) interpolates NF20 (never widen)
and DIL-ALW(m) (always widen).  If DIL-ALW is as good, the breadth flag is doing nothing and
the finding is just "hold more names".

Honesty notes
-------------
* The hypothesis was generated from a U56 control point inside the OOS window, so full-sample
  U56 numbers are DESCRIPTION.  The evidence is (i) the sign census over 48 points, (ii) the
  parents test, (iii) the rule-8 walk-forward, (iv) ex-2022.
* Survivorship: universe.json (56) and universe_broad.json (136) are current-constituent
  lists; SMALL439 is the current constituents of a sub-$2B screen with the README's
  max_1d_move >= 1.0 names dropped.  Absolute CAGRs are optimistic on all three panels;
  the DILUTE-vs-NF20 contrast is the durable part.
* SPY is a tradable constituent of U56 and B136 (the record's convention) and a BENCHMARK
  only on SMALL439.

Deterministic, standalone.  Reads baseline.py; modifies nothing.
"""
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v1_weights, rules_v2_weights
from engine import backtest, metrics, rebalance_mask

COST_BPS = 10
FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
VOL_SCALE = False
N0 = 20
MIN_OBS = 252
QS = [0.10, 0.20, 0.30, 0.40]
MS = [1.5, 2.0, 3.0, 5.0]          # k_narrow = min(round(m*20), E_t) -> 30, 40, 60, 100 names
Q_PRE, M_PRE = 0.20, 2.0           # idea 316's control point
C_PRE = 0.35                       # idea 316's concentration arm, for continuity
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
MIN_EPISODE = 5
SCRIPT = Path(__file__).name
OUT = Path(__file__).with_suffix("")

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ------------------------------------------------------------------ primitives
def eligible_mask(px, cols):
    _, above, vol20 = score(px)
    return (above & (vol20 < MAX_VOL))[cols]


def eligible_count(px, cols):
    e = eligible_mask(px, cols).sum(axis=1).astype(float)
    ma_ok = px[cols].rolling(200).mean().notna().any(axis=1)
    return e.where(ma_ok)


def ranked(px, cols):
    s = score(px, vol_scale=VOL_SCALE)[0][cols].where(eligible_mask(px, cols))
    return s.rank(axis=1, ascending=False)


def narrow_flag(e, q):
    thr = e.expanding(min_periods=MIN_OBS).quantile(q).shift(1)
    return (e <= thr).where(thr.notna() & e.notna(), False)


def weights_from_k(rank, k, gross=GROSS):
    k = k.clip(lower=1.0)
    return rank.le(k, axis=0).astype(float).mul(gross / k, axis=0)


def build(kind, rank, e, nar=None, m=None, c=None):
    """kind in {NF, DILUTE, DIL_ALW, EWALL, CONC}."""
    k_broad = np.minimum(float(N0), e)
    if kind == "NF":
        return weights_from_k(rank, k_broad), k_broad
    if kind == "EWALL":
        k = e.clip(lower=1.0)
        return weights_from_k(rank, k), k
    if kind == "DIL_ALW":
        k = np.minimum(float(round(m * N0)), e)
        return weights_from_k(rank, k), k
    if kind == "DILUTE":
        k = k_broad.where(~nar, np.minimum(float(round(m * N0)), e))
        return weights_from_k(rank, k), k
    if kind == "CONC":
        k = k_broad.where(~nar, np.maximum(1.0, np.round(c * k_broad)))
        return weights_from_k(rank, k), k
    raise ValueError(kind)


# ------------------------------------------------------------------ metrics helpers
def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def keep_4a(r, base):
    a1, a2 = halves(r)
    b1, b2 = halves(base)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def tests_4b(r, spy, r_oos, spy_oos):
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    return {"H1": a1 > s1, "H2": a2 > s2,
            "OOS": metrics(r_oos)["Sharpe"] > metrics(spy_oos)["Sharpe"],
            "DD": abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]),
            "CAGR": m["CAGR"] >= 0.70 * ms["CAGR"]}


def keep_4b(r, spy, r_oos, spy_oos):
    return all(tests_4b(r, spy, r_oos, spy_oos).values())


def fail_4b(r, spy, r_oos, spy_oos):
    f = [k for k, v in tests_4b(r, spy, r_oos, spy_oos).items() if not v]
    return ",".join(f) if f else "-"


def summarise(panel, variant, q, m_, r, to, held, spy, base_v2):
    mm = metrics(r)
    h1, h2 = halves(r)
    r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
    spy_oos = spy.loc[OOS_START:]
    m_is, m_oos = metrics(r_is), metrics(r_oos)
    return dict(panel=panel, variant=variant, q=q, m=m_,
                CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                IS_Sharpe=m_is["Sharpe"], IS_CAGR=m_is["CAGR"], IS_MaxDD=m_is["MaxDD"],
                OOS_CAGR=m_oos["CAGR"], OOS_Sharpe=m_oos["Sharpe"], OOS_MaxDD=m_oos["MaxDD"],
                names=float((held > 0).sum(axis=1).mean()), gross=float(held.sum(axis=1).mean()),
                turn=float(to.sum() / mm["Years"]),
                p4a=keep_4a(r, base_v2), p4b=keep_4b(r, spy, r_oos, spy_oos),
                fail4b=fail_4b(r, spy, r_oos, spy_oos))


def episodes(flag):
    f = flag.astype(bool)
    grp = (f != f.shift(1)).cumsum()
    out = []
    for _, idx in f[f].groupby(grp[f]):
        if len(idx) >= MIN_EPISODE:
            out.append((idx.index[0], idx.index[-1]))
    return out


# ------------------------------------------------------------------ panels
def build_panels():
    px56 = load_universe().dropna(how="all").ffill()
    px136 = load_universe(broad=True).dropna(how="all").ffill()
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_all = [c for c in pxs.columns if c != "SPY"]
    s_stk = [c for c in s_all if c not in bad]
    P(f"  SMALL: {len(s_all)} names in panel, dropped {len(s_all) - len(s_stk)} with "
      f"max_1d_move >= 1.0 (README) -> {len(s_stk)} tradable")
    return [("U56", px56, list(px56.columns)),
            ("B136", px136, list(px136.columns)),
            (f"SMALL{len(s_stk)}", pxs[s_stk + ["SPY"]].dropna(how="all").ffill(), s_stk)]


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    P("=" * 160)
    P(f"Idea 318 does-WIDENING-into-narrow-markets-beat-the-broad-leg (cloud) | {SCRIPT}")
    P("=" * 160)
    P(f"Fixed, not searched: n0={N0}, gross={GROSS:.0%} in BOTH regimes, vol-scaler OFF, weekly, "
      f"{COST_BPS} bps, t+1, quantile min_obs={MIN_OBS}, IS <= {IS_END}, OOS {OOS_START}..")
    P(f"Tuned (2): q in {QS} x m in {MS} = {len(QS)*len(MS)} points, ALL reported on EACH panel.")
    P("Decisive test (idea 317's bar): DILUTE(q,m) must beat BOTH NF20 (never widen) and "
      "DIL-ALW(m) (always widen).")
    P("")
    panels = build_panels()

    rows, effects, parent_rows, yearly_rows, episode_rows = [], [], [], [], []

    for panel, px, cols in panels:
        yrs = px.index.to_series().groupby(px.index.year).count()
        if yrs.loc[2015:2024].max() > 300:
            P("!! CALENDAR-DAY INDEX DETECTED - aborting.")
            sys.exit(1)
        start = px.index[260]
        P("=" * 160)
        P(f"PANEL {panel}: {len(cols)} tradable of {px.shape[1]} columns | "
          f"{px.index[0].date()} -> {px.index[-1].date()} | eval from {start.date()} "
          f"| index sanity 2018={yrs.get(2018)}, 2024={yrs.get(2024)}")

        rank = ranked(px, cols)
        e_nan = eligible_count(px, cols)
        e_full = e_nan.fillna(0.0)
        e = e_full.loc[start:]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        base_v2 = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        base_v1 = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]

        P(f"  E_t: mean {e.mean():.1f}, median {e.median():.0f}, min {e.min():.0f}, max {e.max():.0f}"
          f"  | widening targets round(m*n0) = {[round(m*N0) for m in MS]} names, capped at E_t")
        flags = {q: narrow_flag(e_nan, q).astype(bool).loc[start:] for q in QS}
        prem = []
        for q in QS:
            fl = flags[q]
            prem.append(dict(q=q, narrow_share=fl.mean(), n_days=int(fl.sum()),
                             episodes=len(episodes(fl)),
                             share_of_narrow_days_in_2022=fl.loc["2022"].sum() / max(fl.sum(), 1),
                             mean_E_on_narrow=float(e[fl].mean()),
                             mean_E_off_narrow=float(e[~fl].mean()),
                             years_with_any=int(fl.groupby(fl.index.year).any().sum())))
        P("  Narrow-regime footprint (causal expanding quantile) - how much room is there to widen:")
        P(pd.DataFrame(prem).to_string(index=False, float_format=lambda x: f"{x:.3f}"))

        # ---------------- books
        books = {}

        def run(name, kind, q=None, m_=None, c=None):
            nar = (flags[q].reindex(px.index).fillna(False).astype(bool) if q is not None else None)
            w, k = build(kind, rank, e_full, nar=nar, m=m_, c=c)
            res = backtest(px, w.reindex(columns=px.columns).fillna(0.0), cost_bps=COST_BPS, freq=FREQ)
            r, to, held = res["returns"].loc[start:], res["turnover"].loc[start:], res["weights"].loc[start:]
            books[name] = (r, to, held, k.loc[start:])
            rows.append(summarise(panel, name, q, m_, r, to, held, spy, base_v2))
            return r

        run("NF20", "NF")
        run("EWALL", "EWALL")
        run(f"CONC q{Q_PRE:.2f} c{C_PRE:.2f}", "CONC", q=Q_PRE, c=C_PRE)
        for m_ in MS:
            run(f"DIL-ALW m{m_:.1f}", "DIL_ALW", m_=m_)
        for q in QS:
            for m_ in MS:
                run(f"DILUTE q{q:.2f} m{m_:.1f}", "DILUTE", q=q, m_=m_)

        for nm, ser in (("RULES v2 (live)", base_v2), ("RULES v1", base_v1), ("SPY", spy)):
            mm = metrics(ser)
            h1, h2 = halves(ser)
            m_o = metrics(ser.loc[OOS_START:])
            rows.append(dict(panel=panel, variant=nm, q=np.nan, m=np.nan, CAGR=mm["CAGR"],
                             Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                             IS_Sharpe=metrics(ser.loc[:IS_END])["Sharpe"],
                             IS_CAGR=metrics(ser.loc[:IS_END])["CAGR"],
                             IS_MaxDD=metrics(ser.loc[:IS_END])["MaxDD"],
                             OOS_CAGR=m_o["CAGR"], OOS_Sharpe=m_o["Sharpe"], OOS_MaxDD=m_o["MaxDD"],
                             names=np.nan, gross=np.nan, turn=np.nan, p4a=False,
                             p4b=keep_4b(ser, spy, ser.loc[OOS_START:], spy.loc[OOS_START:]),
                             fail4b=fail_4b(ser, spy, ser.loc[OOS_START:], spy.loc[OOS_START:])))

        # ---------------- the widening effect, narrow-state days only
        reb = rebalance_mask(px.index, FREQ)
        r_nf = books["NF20"][0]
        P("")
        P(f"  WIDENING EFFECT on {panel}: d_t = r(DILUTE) - r(NF20).  Gross is 0.75 in both books, "
          f"so d is WIDTH only.  State = flag as of the last rebalance, lagged one day.")
        eff_tbl = []
        for q in QS:
            nar_full = flags[q].reindex(px.index).fillna(False).astype(bool)
            state = nar_full.where(reb).ffill().shift(1).fillna(False).astype(bool).loc[r_nf.index]
            eps = episodes(state)
            for m_ in MS:
                nm = f"DILUTE q{q:.2f} m{m_:.1f}"
                r_x, _, held_x, k_x = books[nm]
                d = r_x - r_nf
                dn, db = d[state], d[~state]
                d_ex22 = d[state & (d.index.year != 2022)]
                pos_years = sum(1 for y, g in dn.groupby(dn.index.year) if g.sum() > 0)
                n_years = dn.index.year.nunique()
                ep_sums = [d.loc[a:b].sum() for a, b in eps]
                ep_ex22 = [d.loc[a:b].sum() for a, b in eps if a.year != 2022 and b.year != 2022]
                eff_tbl.append(dict(
                    q=q, m=m_, narrow_days=int(state.sum()),
                    k_narrow=float(k_x[state].mean()), k_broad=float(k_x[~state].mean()),
                    ann_eff_on_narrow_pp=252 * dn.mean() * 100 if len(dn) else np.nan,
                    ann_eff_narrow_ex22_pp=252 * d_ex22.mean() * 100 if len(d_ex22) else np.nan,
                    off_state_pp_yr=252 * db.mean() * 100 if len(db) else np.nan,
                    book_pp_yr=d.sum() / (len(d) / 252) * 100,
                    book_pp_yr_ex22=(d[d.index.year != 2022].sum()
                                     / (len(d[d.index.year != 2022]) / 252) * 100),
                    pos_years=f"{pos_years}/{n_years}",
                    pos_episodes=f"{sum(1 for s in ep_sums if s > 0)}/{len(ep_sums)}",
                    pos_episodes_ex22=f"{sum(1 for s in ep_ex22 if s > 0)}/{len(ep_ex22)}",
                    dSharpe=metrics(r_x)["Sharpe"] - metrics(r_nf)["Sharpe"],
                    dMaxDD_pp=(metrics(r_x)["MaxDD"] - metrics(r_nf)["MaxDD"]) * 100,
                    dOOS_Sharpe=(metrics(r_x.loc[OOS_START:])["Sharpe"]
                                 - metrics(r_nf.loc[OOS_START:])["Sharpe"])))
                effects.append(dict(panel=panel, **eff_tbl[-1]))
                if q == Q_PRE and m_ == M_PRE:
                    for a, b in eps:
                        episode_rows.append(dict(panel=panel, q=q, m=m_, start=a.date(), end=b.date(),
                                                 days=len(d.loc[a:b]), d_pct=d.loc[a:b].sum() * 100,
                                                 nf_pct=r_nf.loc[a:b].sum() * 100,
                                                 spy_pct=spy.loc[a:b].sum() * 100))
                    yr = pd.DataFrame({"d_pct": d.groupby(d.index.year).sum() * 100,
                                       "narrow_days": state.groupby(state.index.year).sum()})
                    for y, rr in yr.iterrows():
                        yearly_rows.append(dict(panel=panel, year=int(y), d_pct=rr["d_pct"],
                                                narrow_days=int(rr["narrow_days"])))
        eff = pd.DataFrame(eff_tbl)
        P(eff.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

        # ---------------- PARENTS TEST (idea 317's bar), every (q, m)
        P("")
        P(f"  PARENTS TEST on {panel}: does the CONDITIONAL clause beat BOTH parents? "
          f"parent1 = NF20 (never widen), parent2 = DIL-ALW m (always widen).")
        pt = []
        for q in QS:
            for m_ in MS:
                r_x = books[f"DILUTE q{q:.2f} m{m_:.1f}"][0]
                r_a = books[f"DIL-ALW m{m_:.1f}"][0]
                s_x, s_n, s_a = (metrics(r_x)["Sharpe"], metrics(r_nf)["Sharpe"], metrics(r_a)["Sharpe"])
                o_x, o_n, o_a = (metrics(r_x.loc[OOS_START:])["Sharpe"],
                                 metrics(r_nf.loc[OOS_START:])["Sharpe"],
                                 metrics(r_a.loc[OOS_START:])["Sharpe"])
                pt.append(dict(q=q, m=m_, Sharpe=s_x, dS_vs_NF20=s_x - s_n, dS_vs_ALW=s_x - s_a,
                               beats_both=bool(s_x > s_n and s_x > s_a),
                               OOS_dS_vs_NF20=o_x - o_n, OOS_dS_vs_ALW=o_x - o_a,
                               OOS_beats_both=bool(o_x > o_n and o_x > o_a)))
                parent_rows.append(dict(panel=panel, **pt[-1]))
        PT = pd.DataFrame(pt)
        P(PT.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        P(f"  -> beats BOTH parents in {int(PT.beats_both.sum())}/16 full-sample, "
          f"{int(PT.OOS_beats_both.sum())}/16 out of sample.")

        # ---------------- rule 8 walk-forward
        P("")
        P(f"  RULE 8 WALK-FORWARD on {panel}: (q,m) chosen on <= {IS_END}, {OOS_START}.. read once.")
        grid = pd.DataFrame([r for r in rows if r["panel"] == panel
                             and r["variant"].startswith("DILUTE q")])
        s1 = grid.loc[grid.IS_Sharpe.idxmax()]
        is_spy_dd = abs(metrics(spy.loc[:IS_END])["MaxDD"])
        cand = [g for _, g in grid.iterrows() if abs(g["IS_MaxDD"]) <= 0.60 * is_spy_dd]
        s2 = (pd.DataFrame(cand).sort_values("IS_Sharpe").iloc[-1] if cand else s1)
        wf = []
        for label, g in (("S1 IS-Sharpe", s1), ("S2 4b-aware", s2)):
            wf.append(dict(rule=label, pick=g["variant"], OOS_CAGR=g["OOS_CAGR"],
                           OOS_Sharpe=g["OOS_Sharpe"], OOS_MaxDD=g["OOS_MaxDD"],
                           p4a=g["p4a"], p4b=g["p4b"], fail4b=g["fail4b"]))
        for nm in ["NF20", "EWALL"] + [f"DIL-ALW m{m_:.1f}" for m_ in MS]:
            g = next(r for r in rows if r["panel"] == panel and r["variant"] == nm)
            wf.append(dict(rule="control", pick=nm, OOS_CAGR=g["OOS_CAGR"], OOS_Sharpe=g["OOS_Sharpe"],
                           OOS_MaxDD=g["OOS_MaxDD"], p4a=g["p4a"], p4b=g["p4b"], fail4b=g["fail4b"]))
        for nm, ser in (("RULES v2 (live)", base_v2), ("SPY", spy)):
            m_o = metrics(ser.loc[OOS_START:])
            wf.append(dict(rule="benchmark", pick=nm, OOS_CAGR=m_o["CAGR"], OOS_Sharpe=m_o["Sharpe"],
                           OOS_MaxDD=m_o["MaxDD"], p4a=False, p4b="", fail4b=""))
        P(pd.DataFrame(wf).to_string(index=False, float_format=lambda x: f"{x:.3f}"))
        P(f"  4b thresholds on {panel}: MaxDD cap {0.60*metrics(spy)['MaxDD']:.1%}, "
          f"CAGR floor {0.70*metrics(spy)['CAGR']:.1%}  (SPY {metrics(spy)['CAGR']:.1%}/"
          f"{metrics(spy)['Sharpe']:.3f}/{metrics(spy)['MaxDD']:.1%})")
        P(f"  [{time.time()-t0:.0f}s]")

    # ---------------------------------------------------------------- global
    R = pd.DataFrame(rows)
    E = pd.DataFrame(effects)
    PTA = pd.DataFrame(parent_rows)
    R.to_csv(f"{OUT}.grid.csv", index=False)
    E.to_csv(f"{OUT}.effects.csv", index=False)
    PTA.to_csv(f"{OUT}.parents.csv", index=False)
    pd.DataFrame(episode_rows).to_csv(f"{OUT}.episodes.csv", index=False)
    pd.DataFrame(yearly_rows).to_csv(f"{OUT}.yearly.csv", index=False)

    P("")
    P("=" * 160)
    P("FULL GRID - every point, every panel (4a judged vs RULES v2 on the same panel)")
    P("=" * 160)
    P(R.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    P("")
    P("=" * 160)
    P("VERDICT TABLE - is the U56 widening edge a grid artefact?")
    P("=" * 160)
    for panel in E.panel.unique():
        g = E[E.panel == panel]
        P(f"{panel}: 16 points | narrow-day effect > 0 in {int((g.ann_eff_on_narrow_pp>0).sum())}/16 "
          f"(mean {g.ann_eff_on_narrow_pp.mean():+.2f} pp/yr) | ex-2022 > 0 in "
          f"{int((g.ann_eff_narrow_ex22_pp>0).sum())}/16 (mean {g.ann_eff_narrow_ex22_pp.mean():+.2f} pp/yr) | "
          f"book dSharpe > 0 in {int((g.dSharpe>0).sum())}/16 (mean {g.dSharpe.mean():+.4f}) | "
          f"drawdown better in {int((g.dMaxDD_pp>0).sum())}/16 (mean {g.dMaxDD_pp.mean():+.2f} pp) | "
          f"OOS dSharpe > 0 in {int((g.dOOS_Sharpe>0).sum())}/16 (mean {g.dOOS_Sharpe.mean():+.4f})")
    P("")
    P("Pooled over 48 points: "
      f"narrow-day effect > 0 in {int((E.ann_eff_on_narrow_pp>0).sum())}/48, "
      f"ex-2022 > 0 in {int((E.ann_eff_narrow_ex22_pp>0).sum())}/48, "
      f"book dSharpe > 0 in {int((E.dSharpe>0).sum())}/48, "
      f"drawdown improved in {int((E.dMaxDD_pp>0).sum())}/48, "
      f"OOS dSharpe > 0 in {int((E.dOOS_Sharpe>0).sum())}/48")
    P(f"Parents test pooled: beats BOTH parents in {int(PTA.beats_both.sum())}/48 full-sample, "
      f"{int(PTA.OOS_beats_both.sum())}/48 OOS "
      f"(vs NF20 alone {int((PTA.dS_vs_NF20>0).sum())}/48, vs DIL-ALW alone "
      f"{int((PTA.dS_vs_ALW>0).sum())}/48)")
    dil = R[R.variant.str.startswith("DILUTE q")]
    P(f"4a passes: {int(R.p4a.sum())}/{len(R)} rows | 4b passes among DILUTE grid points: "
      f"{int(dil.p4b.sum())}/{len(dil)}")
    if int(dil.p4b.sum()):
        P("  4b-passing DILUTE points, next to their own NF20 parent on the same panel:")
        for _, g in dil[dil.p4b].iterrows():
            nf = next(r for r in rows if r["panel"] == g["panel"] and r["variant"] == "NF20")
            P(f"   {g['panel']:>9} {g['variant']:<20} {g['CAGR']:.2%}/{g['Sharpe']:.3f}/{g['MaxDD']:.1%} "
              f"OOS {g['OOS_Sharpe']:.3f}  vs NF20 {nf['CAGR']:.2%}/{nf['Sharpe']:.3f}/{nf['MaxDD']:.1%} "
              f"OOS {nf['OOS_Sharpe']:.3f} (NF20 4b={nf['p4b']})")

    P("")
    P("REPLICATION of idea 316's single control point (q=0.20, m=2.0), per panel:")
    rep = R[(R.variant == f"DILUTE q{Q_PRE:.2f} m{M_PRE:.1f}") | (R.variant == "NF20")
            | (R.variant == f"CONC q{Q_PRE:.2f} c{C_PRE:.2f}") | (R.variant == "SPY")]
    P(rep[["panel", "variant", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
           "names", "turn", "p4b", "fail4b"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    P("")
    P("PER-EPISODE detail at (q=0.20, m=2.0):")
    P(pd.DataFrame(episode_rows).to_string(index=False, float_format=lambda x: f"{x:.2f}"))
    P("")
    P("PER-YEAR d (DILUTE - NF20) at (q=0.20, m=2.0), pct of NAV:")
    Y = pd.DataFrame(yearly_rows).pivot(index="year", columns="panel", values="d_pct")
    P(Y.to_string(float_format=lambda x: f"{x:+.2f}"))
    P(f"\ntotal {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
