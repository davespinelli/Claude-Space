#!/usr/bin/env python3
"""Idea 316 - "is-CONCENTRATION-in-narrow-markets-a-general-clause-or-one-2022" (lane C).

The question
------------
Idea 48 (lane B, 2026-09-07) KILLED the conditional fraction clause, but isolated one live
mechanism inside it: on narrow-breadth days the hybrid holds FEWER names than its broad leg,
and that concentration was worth ~+0.6 pp/yr of book return on the 13.3% of days the flag was
on, bought with 3.2 pp of extra drawdown.  Its own caveat is the reason this idea exists:
2022 is the only year in U56's sample where the narrow flag is on almost continuously, so
that number rests on effectively ONE episode.

This run asks whether the narrow-day concentration effect is a GENERAL clause.  It re-runs it
on two panels with more (and differently timed) narrow episodes - B136 (universe_broad.json)
and the SMALL439 sub-$2B panel - alongside U56 as the replication reference, and reports the
sign of the effect year by year and EPISODE by EPISODE, with 2022 removed.  Per the queue: if
the sign does not survive outside 2022, no fraction clause of any form belongs in RULES.

What is measured, and why this form
-----------------------------------
Idea 48's clause held `ceil(f * E_t)` names in the narrow regime.  On U56 (E_t ~ 37) that is
a concentration.  On SMALL439 (E_t in the hundreds) `ceil(0.35 * E_t)` is ~100 names, i.e.
the same wording would DILUTE a 20-name book - it would not test the mechanism at all.  So the
clause is written multiplicatively, as concentration relative to the book's own broad leg:

    k_broad,t = min(n0, E_t)                       (the broad leg, n0 = 20, the record's count)
    CONC(q, c):  narrow if E_t <= Quantile_q(E_{<=t-1})  ->  k_t = max(1, round(c * k_broad,t))
                 broad  otherwise                        ->  k_t = k_broad,t
    equal weight GROSS / k_t either way, so realised gross is 0.75 in BOTH regimes.

Holding gross constant is the point: exposure is matched by construction, so any difference
between CONC and its broad leg NF20 is concentration and nothing else.  Idea 48's own
decomposition already showed the exposure treatments (CASH, HALF) behave differently.

Tuned parameters (PROTOCOL rule 4: at most two) - q and c.  ALL 4x4 = 16 points are reported
on EACH of the three panels (48 points).  Everything else is fixed in advance and not
searched: n0 = 20, GROSS = 0.75, scorer without /sqrt(vol20) (idea 2's), 200d + vol20 < 0.60
eligibility, weekly rebalance, 10 bps, t+1 execution, 252-observation minimum for the causal
quantile, IS = start..2016, OOS = 2017..

Structural controls (NOT tuned, none selected on its own result), all at the pre-registered
q = 0.20 and c = 0.35:
    NF20       the broad leg with the clause deleted            (parent 1)
    CONC-ALW   k = round(0.35 * k_broad) on EVERY day           (parent 2 - concentration always)
    DILUTE     narrow -> k = min(2*n0, E_t): the OPPOSITE sign. If concentration is the
               mechanism, this must lose where CONC wins.  It is the sign test.
    FRAC       idea 48's literal `ceil(0.35 * E_t)` narrow leg, run on all three panels with
               its realised narrow-day name count printed, to show what that wording does
               off U56.
    N20        idea 2's book (fixed w = GROSS/n0, de-grosses when E_t < n0), for continuity.

Honesty notes
-------------
* 2022 sits inside rule 8's OOS window and the hypothesis under test was generated from 2022.
  Full-sample and per-year numbers are therefore DESCRIPTION.  The evidence is (i) the
  walk-forward, (ii) the ex-2022 and per-episode signs, (iii) whether the conditional clause
  beats BOTH its unconditional parents.
* Survivorship: universe.json (56) and universe_broad.json (136) are current-constituent
  lists; SMALL439 is the current constituents of a sub-$2B screen (data/SMALL_PANEL_README.md)
  with the README's `max_1d_move >= 1.0` names dropped.  Absolute CAGRs are optimistic on all
  three; the CONC-vs-NF20 contrast is the durable part.
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
MAX_VOL = 0.60           # v1 eligibility, unchanged
GROSS = 0.75             # live gross, FIXED and identical in both regimes
VOL_SCALE = False        # idea 2's scorer: no /sqrt(vol20)
N0 = 20                  # the record's count, FIXED (not tuned here)
MIN_OBS = 252            # observations before the causal breadth quantile exists
QS = [0.10, 0.20, 0.30, 0.40]
CS = [0.25, 0.35, 0.50, 0.75]      # k_narrow = round(c * k_broad) -> 5, 7, 10, 15 names
Q_PRE, C_PRE = 0.20, 0.35          # pre-registered point for the control arms
F_PRE = 0.35                       # idea 48's fraction, for the FRAC control only
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
MIN_EPISODE = 5                    # trading days; shorter narrow runs are not "episodes"
SCRIPT = Path(__file__).name
OUT = Path(__file__).with_suffix("")

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 300)

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ------------------------------------------------------------------ primitives
def eligible_mask(px, cols):
    _, above, vol20 = score(px)
    m = above & (vol20 < MAX_VOL)
    return m[cols]


def eligible_count(px, cols):
    """E_t, with pre-warm-up rows (no 200d MA yet) NaN so they cannot enter the quantile."""
    e = eligible_mask(px, cols).sum(axis=1).astype(float)
    ma_ok = px[cols].rolling(200).mean().notna().any(axis=1)
    return e.where(ma_ok)


def ranked(px, cols):
    s = score(px, vol_scale=VOL_SCALE)[0][cols].where(eligible_mask(px, cols))
    return s.rank(axis=1, ascending=False)


def narrow_flag(e, q):
    """Causal bottom-q regime test: E_t <= expanding q-quantile of E over history to t-1."""
    thr = e.expanding(min_periods=MIN_OBS).quantile(q).shift(1)
    return (e <= thr).where(thr.notna() & e.notna(), False)


def weights_from_k(rank, k, gross=GROSS):
    k = k.clip(lower=1.0)
    sel = rank.le(k, axis=0)
    return sel.astype(float).mul(gross / k, axis=0)


def build(kind, rank, e, nar=None, c=None, f=None):
    """kind in {NF, N, CONC, CONC_ALW, DILUTE, FRAC}."""
    k_broad = np.minimum(float(N0), e)
    if kind == "NF":
        return weights_from_k(rank, k_broad), k_broad
    if kind == "N":                                   # idea 2's fixed-w book (de-grosses)
        k = pd.Series(float(N0), index=rank.index)
        return weights_from_k(rank, k), k_broad
    if kind == "CONC_ALW":
        k = np.maximum(1.0, np.round(c * k_broad))
        return weights_from_k(rank, k), k
    if kind == "CONC":
        k = k_broad.where(~nar, np.maximum(1.0, np.round(c * k_broad)))
        return weights_from_k(rank, k), k
    if kind == "DILUTE":
        k = k_broad.where(~nar, np.minimum(2.0 * N0, e))
        return weights_from_k(rank, k), k
    if kind == "FRAC":                                # idea 48's literal wording
        k = k_broad.where(~nar, np.ceil(f * e))
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


def summarise(panel, variant, q, c, r, to, held, spy, base_v2):
    m = metrics(r)
    h1, h2 = halves(r)
    r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
    spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
    m_is, m_oos = metrics(r_is), metrics(r_oos)
    return dict(panel=panel, variant=variant, q=q, c=c,
                CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                IS_Sharpe=m_is["Sharpe"], IS_CAGR=m_is["CAGR"],
                OOS_CAGR=m_oos["CAGR"], OOS_Sharpe=m_oos["Sharpe"], OOS_MaxDD=m_oos["MaxDD"],
                names=float((held > 0).sum(axis=1).mean()), gross=float(held.sum(axis=1).mean()),
                turn=float(to.sum() / m["Years"]),
                p4a=keep_4a(r, base_v2), p4b=keep_4b(r, spy, r_oos, spy_oos),
                fail4b=fail_4b(r, spy, r_oos, spy_oos))


def episodes(flag):
    """Contiguous runs of True of at least MIN_EPISODE trading days -> list of (start, end)."""
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
    return [("U56", px56, [c for c in px56.columns]),
            ("B136", px136, [c for c in px136.columns]),
            (f"SMALL{len(s_stk)}", pxs[s_stk + ["SPY"]].dropna(how="all").ffill(), s_stk)]


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    P("=" * 150)
    P(f"Idea 316 is-CONCENTRATION-in-narrow-markets-a-general-clause-or-one-2022 (lane C) | {SCRIPT}")
    P("=" * 150)
    P(f"Fixed, not searched: n0={N0}, gross={GROSS:.0%} in BOTH regimes, scorer OFF, weekly, "
      f"{COST_BPS} bps, t+1, quantile min_obs={MIN_OBS}.")
    P(f"Tuned (2): q in {QS} x c in {CS} = {len(QS)*len(CS)} points, ALL reported on EACH panel.")
    P("")
    panels = build_panels()

    rows, effects, yearly_rows, episode_rows = [], [], [], []

    for panel, px, cols in panels:
        yrs = px.index.to_series().groupby(px.index.year).count()
        if yrs.loc[2015:2024].max() > 300:
            P("!! CALENDAR-DAY INDEX DETECTED - aborting.")
            sys.exit(1)
        start = px.index[260]
        P("=" * 150)
        P(f"PANEL {panel}: {len(cols)} tradable of {px.shape[1]} columns | "
          f"{px.index[0].date()} -> {px.index[-1].date()} | eval from {start.date()} "
          f"| index sanity 2018={yrs.get(2018)}, 2024={yrs.get(2024)}")

        rank = ranked(px, cols)
        e_nan = eligible_count(px, cols)        # NaN before the 200d MA exists - the quantile
        e_full = e_nan.fillna(0.0)              # must not see those rows (idea 48's convention)
        e = e_full.loc[start:]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        base_v2 = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        base_v1 = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]

        # ---------------- premise: how many narrow episodes does this panel actually have?
        P(f"  E_t: mean {e.mean():.1f}, median {e.median():.0f}, min {e.min():.0f}, max {e.max():.0f}")
        flags = {q: narrow_flag(e_nan, q).astype(bool).loc[start:] for q in QS}
        prem = []
        for q in QS:
            fl = flags[q]
            eps = episodes(fl)
            in22 = fl.loc["2022"].mean() if len(fl.loc["2022"]) else np.nan
            share22 = fl.loc["2022"].sum() / max(fl.sum(), 1)
            prem.append(dict(q=q, narrow_share=fl.mean(), n_days=int(fl.sum()),
                             episodes=len(eps), share_of_narrow_days_in_2022=share22,
                             narrow_share_2022=in22,
                             years_with_any=int(fl.groupby(fl.index.year).any().sum())))
        prem = pd.DataFrame(prem)
        P("  PREMISE - narrow-regime footprint (causal expanding quantile):")
        P(prem.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

        fl_pre = flags[Q_PRE]
        byyear = pd.DataFrame({"narrow_share": fl_pre.groupby(fl_pre.index.year).mean(),
                               "E_t": e.groupby(e.index.year).mean()})
        P(f"  narrow share by year at the pre-registered q={Q_PRE}:")
        P("   " + "  ".join(f"{y}:{v:.2f}" for y, v in byyear["narrow_share"].items()))

        # ---------------- books
        books = {}          # name -> (returns, turnover, held, k_series, q, c)

        def run(name, kind, q=None, c=None, f=None):
            nar = (flags[q].reindex(px.index).fillna(False).astype(bool)
                   if q is not None else None)
            w, k = build(kind, rank, e_full, nar=nar, c=c, f=f)
            res = backtest(px, w.reindex(columns=px.columns).fillna(0.0), cost_bps=COST_BPS, freq=FREQ)
            r, to, held = res["returns"].loc[start:], res["turnover"].loc[start:], res["weights"].loc[start:]
            books[name] = (r, to, held, k.loc[start:], q, c)
            rows.append(summarise(panel, name, q, c, r, to, held, spy, base_v2))
            return r

        run("NF20", "NF")
        run("N20", "N")
        run(f"CONC-ALW c{C_PRE}", "CONC_ALW", c=C_PRE)
        run(f"DILUTE q{Q_PRE}", "DILUTE", q=Q_PRE)
        run(f"FRAC q{Q_PRE} f{F_PRE}", "FRAC", q=Q_PRE, f=F_PRE)
        for q in QS:
            for c in CS:
                run(f"CONC q{q:.2f} c{c:.2f}", "CONC", q=q, c=c)

        for nm, ser in (("RULES v2 (live)", base_v2), ("RULES v1", base_v1), ("SPY", spy)):
            m = metrics(ser)
            h1, h2 = halves(ser)
            m_o = metrics(ser.loc[OOS_START:])
            rows.append(dict(panel=panel, variant=nm, q=np.nan, c=np.nan, CAGR=m["CAGR"],
                             Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                             IS_Sharpe=metrics(ser.loc[:IS_END])["Sharpe"],
                             IS_CAGR=metrics(ser.loc[:IS_END])["CAGR"],
                             OOS_CAGR=m_o["CAGR"], OOS_Sharpe=m_o["Sharpe"], OOS_MaxDD=m_o["MaxDD"],
                             names=np.nan, gross=np.nan, turn=np.nan, p4a=False,
                             p4b=keep_4b(ser, spy, ser.loc[OOS_START:], spy.loc[OOS_START:]),
                             fail4b=fail_4b(ser, spy, ser.loc[OOS_START:], spy.loc[OOS_START:])))

        # ---------------- the concentration effect, narrow-state days only
        # state governing the CURRENTLY HELD weights: the flag as of the last rebalance,
        # shifted by the engine's one-day execution lag.
        reb = rebalance_mask(px.index, FREQ)
        r_nf = books["NF20"][0]
        P("")
        P(f"  CONCENTRATION EFFECT on {panel}: d_t = r(CONC) - r(NF20), decomposed by state, "
          f"by year and by episode.  Gross is 0.75 in both books, so d is concentration only.")
        eff_tbl = []
        for q in QS:
            nar_full = flags[q].reindex(px.index).fillna(False).astype(bool)
            state = nar_full.where(reb).ffill().shift(1).fillna(False).astype(bool).loc[r_nf.index]
            eps = episodes(state)
            for c in CS:
                r_c = books[f"CONC q{q:.2f} c{c:.2f}"][0]
                d = r_c - r_nf
                dn, db = d[state], d[~state]
                d_ex22 = d[state & (d.index.year != 2022)]
                yrs_state = state.groupby(state.index.year).sum() / 252.0
                pos_years = sum(1 for y, g in d[state].groupby(d[state].index.year) if g.sum() > 0)
                n_years = d[state].index.year.nunique()
                ep_sums = [d.loc[a:b].sum() for a, b in eps]
                ep_sums_ex22 = [d.loc[a:b].sum() for a, b in eps if a.year != 2022 and b.year != 2022]
                eff_tbl.append(dict(
                    q=q, c=c, narrow_days=int(state.sum()),
                    ann_eff_on_narrow_pp=252 * dn.mean() * 100 if len(dn) else np.nan,
                    book_pp_yr=d.sum() / (len(d) / 252) * 100,
                    book_pp_yr_ex22=(d[d.index.year != 2022].sum()
                                     / (len(d[d.index.year != 2022]) / 252) * 100),
                    ann_eff_narrow_ex22_pp=(252 * d_ex22.mean() * 100) if len(d_ex22) else np.nan,
                    off_state_pp_yr=252 * db.mean() * 100 if len(db) else np.nan,
                    pos_years=f"{pos_years}/{n_years}",
                    episodes=len(eps),
                    pos_episodes=f"{sum(1 for s in ep_sums if s > 0)}/{len(ep_sums)}",
                    pos_episodes_ex22=f"{sum(1 for s in ep_sums_ex22 if s > 0)}/{len(ep_sums_ex22)}",
                    dSharpe=metrics(r_c)["Sharpe"] - metrics(r_nf)["Sharpe"],
                    dMaxDD_pp=(metrics(r_c)["MaxDD"] - metrics(r_nf)["MaxDD"]) * 100,
                    dOOS_Sharpe=metrics(r_c.loc[OOS_START:])["Sharpe"] - metrics(r_nf.loc[OOS_START:])["Sharpe"]))
                effects.append(dict(panel=panel, **eff_tbl[-1]))
                if q == Q_PRE and c == C_PRE:
                    for a, b in eps:
                        episode_rows.append(dict(panel=panel, q=q, c=c, start=a.date(), end=b.date(),
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

        # control arms, same decomposition at the pre-registered point
        P(f"  CONTROL ARMS at q={Q_PRE} (sign test + parents), vs NF20:")
        nar_full = flags[Q_PRE].reindex(px.index).fillna(False).astype(bool)
        state = nar_full.where(reb).ffill().shift(1).fillna(False).astype(bool).loc[r_nf.index]
        ctl = []
        for nm in (f"CONC q{Q_PRE:.2f} c{C_PRE:.2f}", f"DILUTE q{Q_PRE}", f"CONC-ALW c{C_PRE}",
                   f"FRAC q{Q_PRE} f{F_PRE}", "N20"):
            r_x, _, held_x, k_x, _, _ = books[nm]
            d = r_x - r_nf
            ctl.append(dict(book=nm,
                            k_narrow=float(k_x[state.reindex(k_x.index).fillna(False)].mean()),
                            k_broad=float(k_x[~state.reindex(k_x.index).fillna(False)].mean()),
                            names=float((held_x > 0).sum(axis=1).mean()),
                            gross=float(held_x.sum(axis=1).mean()),
                            ann_eff_on_narrow_pp=252 * d[state].mean() * 100,
                            ann_eff_narrow_ex22_pp=252 * d[state & (d.index.year != 2022)].mean() * 100,
                            book_pp_yr=d.sum() / (len(d) / 252) * 100,
                            dSharpe=metrics(r_x)["Sharpe"] - metrics(r_nf)["Sharpe"],
                            dMaxDD_pp=(metrics(r_x)["MaxDD"] - metrics(r_nf)["MaxDD"]) * 100))
        P(pd.DataFrame(ctl).to_string(index=False, float_format=lambda x: f"{x:.3f}"))

        # ---------------- rule 8 walk-forward on this panel
        P("")
        P(f"  RULE 8 WALK-FORWARD on {panel}: (q,c) chosen on <= {IS_END}, {OOS_START}.. read once.")
        grid = pd.DataFrame([r for r in rows if r["panel"] == panel
                             and r["variant"].startswith("CONC q")])
        s1 = grid.loc[grid.IS_Sharpe.idxmax()]
        # S2: 4b-aware in-sample chooser - best IS Sharpe among points whose IS MaxDD clears
        # 60% of SPY's IS MaxDD; falls back to S1 if none qualifies.
        is_spy_dd = abs(metrics(spy.loc[:IS_END])["MaxDD"])
        cand = []
        for _, g in grid.iterrows():
            r_x = books[g["variant"]][0]
            if abs(metrics(r_x.loc[:IS_END])["MaxDD"]) <= 0.60 * is_spy_dd:
                cand.append(g)
        s2 = (pd.DataFrame(cand).sort_values("IS_Sharpe").iloc[-1] if cand else s1)
        wf = []
        for label, g in (("S1 IS-Sharpe", s1), ("S2 4b-aware", s2)):
            wf.append(dict(rule=label, pick=g["variant"], OOS_CAGR=g["OOS_CAGR"],
                           OOS_Sharpe=g["OOS_Sharpe"], OOS_MaxDD=g["OOS_MaxDD"],
                           p4a=g["p4a"], p4b=g["p4b"], fail4b=g["fail4b"]))
        for nm in ("NF20", "N20"):
            g = next(r for r in rows if r["panel"] == panel and r["variant"] == nm)
            wf.append(dict(rule="control", pick=nm, OOS_CAGR=g["OOS_CAGR"], OOS_Sharpe=g["OOS_Sharpe"],
                           OOS_MaxDD=g["OOS_MaxDD"], p4a=g["p4a"], p4b=g["p4b"], fail4b=g["fail4b"]))
        for nm, ser in (("RULES v2 (live)", base_v2), ("SPY", spy)):
            m_o = metrics(ser.loc[OOS_START:])
            wf.append(dict(rule="benchmark", pick=nm, OOS_CAGR=m_o["CAGR"], OOS_Sharpe=m_o["Sharpe"],
                           OOS_MaxDD=m_o["MaxDD"], p4a=False, p4b="", fail4b=""))
        P(pd.DataFrame(wf).to_string(index=False, float_format=lambda x: f"{x:.3f}"))
        P(f"  4b thresholds on {panel}: MaxDD cap {0.60*metrics(spy)['MaxDD']:.1%}, "
          f"CAGR floor {0.70*metrics(spy)['CAGR']:.1%}")
        P(f"  [{time.time()-t0:.0f}s]")

    # ---------------------------------------------------------------- global tables
    R = pd.DataFrame(rows)
    E = pd.DataFrame(effects)
    R.to_csv(f"{OUT}.grid.csv", index=False)
    E.to_csv(f"{OUT}.effects.csv", index=False)
    pd.DataFrame(episode_rows).to_csv(f"{OUT}.episodes.csv", index=False)
    pd.DataFrame(yearly_rows).to_csv(f"{OUT}.yearly.csv", index=False)

    P("")
    P("=" * 150)
    P("FULL GRID - every point, every panel (4a judged vs RULES v2 on the same panel)")
    P("=" * 150)
    P(R.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    P("")
    P("=" * 150)
    P("VERDICT TABLE - does the narrow-day concentration effect have a general sign?")
    P("=" * 150)
    for panel in E.panel.unique():
        g = E[E.panel == panel]
        P(f"{panel}: 16 points | ann effect on narrow days > 0 in {int((g.ann_eff_on_narrow_pp>0).sum())}/16 "
          f"(mean {g.ann_eff_on_narrow_pp.mean():+.2f} pp/yr) | ex-2022 > 0 in "
          f"{int((g.ann_eff_narrow_ex22_pp>0).sum())}/16 (mean {g.ann_eff_narrow_ex22_pp.mean():+.2f} pp/yr) | "
          f"book dSharpe > 0 in {int((g.dSharpe>0).sum())}/16 (mean {g.dSharpe.mean():+.4f}) | "
          f"dMaxDD better in {int((g.dMaxDD_pp>0).sum())}/16 (mean {g.dMaxDD_pp.mean():+.2f} pp) | "
          f"dOOS Sharpe > 0 in {int((g.dOOS_Sharpe>0).sum())}/16 (mean {g.dOOS_Sharpe.mean():+.4f})")
    P("")
    P("Pooled over 48 points: "
      f"narrow-day effect > 0 in {int((E.ann_eff_on_narrow_pp>0).sum())}/48, "
      f"ex-2022 > 0 in {int((E.ann_eff_narrow_ex22_pp>0).sum())}/48, "
      f"book dSharpe > 0 in {int((E.dSharpe>0).sum())}/48, "
      f"drawdown improved in {int((E.dMaxDD_pp>0).sum())}/48, "
      f"OOS dSharpe > 0 in {int((E.dOOS_Sharpe>0).sum())}/48")
    P(f"4a passes: {int(R.p4a.sum())}/{len(R)} rows | 4b passes among CONC grid points: "
      f"{int(R[R.variant.str.startswith('CONC q')].p4b.sum())}/{len(R[R.variant.str.startswith('CONC q')])}")
    P("")
    P("PER-EPISODE detail at the pre-registered (q=0.20, c=0.35):")
    P(pd.DataFrame(episode_rows).to_string(index=False, float_format=lambda x: f"{x:.2f}"))
    P("")
    P("PER-YEAR d (CONC - NF20) at the pre-registered point, pct of NAV:")
    Y = pd.DataFrame(yearly_rows).pivot(index="year", columns="panel", values="d_pct")
    P(Y.to_string(float_format=lambda x: f"{x:+.2f}"))
    P(f"\ntotal {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
