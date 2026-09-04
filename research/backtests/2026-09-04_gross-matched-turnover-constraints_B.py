#!/usr/bin/env python3
"""Idea 86 - "gross-matched-turnover-constraints".

The question (pre-registered, from QUEUE)
-----------------------------------------
Idea 83 closed with an incidental finding that invalidates part of its own headline:
`budget-top` (truncate the trade list at a per-rebalance |dw|_1 cap) is not self-financing.
Leaving sells unexecuted RAISES realised exposure - on u56/CAND20 it realised 0.815 average
gross against the control's 0.717, "which is most of its +2.65pp CAGR and all of its
-4.58pp MaxDD".  That is idea 73's de-grossing artefact seen from the other side: an
instrument sold as a TURNOVER lever was partly measuring EXPOSURE.

The same exposure leak is latent in every other turnover/holding-period instrument the
project owns.  Idea 3's cadence arms change how long the book drifts un-reset between
rebalances, so they realise different average gross.  Idea 79's rank hysteresis (never yet
run) holds stale names, which changes how often the book is topped back up to target.  And
the CAND-n construction itself divides GROSS by the fixed n, so it silently de-grosses
whenever fewer than n names are eligible (idea 73/81).

So the pre-registered question is a single one, asked of every instrument at once:

    Re-run every turnover/hysteresis instrument with realised gross renormalised to a
    COMMON target at each rebalance, and mark which published effects survive.

An effect that survives gross-matching is a turnover effect.  An effect that does not was
an exposure effect wearing a turnover label, and the leaderboard row that reported it needs
a footnote.

The treatment
-------------
    gm=off   the published form.  Execute the instrument; whatever gross falls out, falls
             out.  This reproduces the numbers already on the leaderboard.
    gm=on    identical, then rescale the post-trade weight vector so it sums to exactly
             G* = 0.75 before the turnover is counted.  The renormalisation trades are
             charged at the same cost as every other trade - matching gross is not free,
             and pretending it is would replace one artefact with another.

Everything else is held fixed.  gm is applied at rebalance dates only (a book cannot trade
between rebalances), so intra-period drift in gross is left alone in both arms; the claim
tested is about the RESET, which is the only thing an instrument controls.

Instruments (one tuned knob each; every arm reported, none picked on its own result)
------------------------------------------------------------------------------------
    control     weekly, no constraint.  B = inf, k = 1.0, freq = W.
    budget-top  idea 83's literal spec: cap sum|dw| at B, largest trades first, partial
                fill on the marginal one.  NOT self-financing - the arm the finding is about.
    budget-pro  same cap reached pro-rata (lambda = B/|dw|_1 on every name).  Idea 83's
                gross-preserving implementation control; included because if gm changes
                `top` and not `pro`, the mechanism is truncation, as claimed.
                B in {0.10, 0.20, 0.40}.
    hyst        idea 79, first run here: keep a held name until its rank falls outside the
                top k*n, instead of outside the top n; fill the freed slots from the best
                unheld names.  Turnover instrument that changes no signal.
                k in {1.25, 1.50, 2.00}.  Defined only for the RANKED book.
    cadence     idea 3: rebalance calendar in {D, M, Q}; W is the control.

Books (both are standing 4b passers, so an instrument can only take margin away)
    CAND20   idea 2's standing 4b KEEP: top-20 eligible by the composite WITHOUT the
             /sqrt(vol20) scaler, equal weight, 75% gross, weekly.  Its literal form
             de-grosses when fewer than 20 names are eligible - so gm=on is also idea 81's
             gross-normalisation fix for this book, reported here as a by-product.
    EWall    idea 10's `B136/EWall`: equal-weight ALL eligible names at 75% gross, no
             ranking.  Its target already sums to exactly 0.75, so gm=on can only differ
             through the instrument - which makes it the clean read.
Eligibility in both = RULES v1's gate (above 200d MA, vol20 < 0.60), unchanged.

Tuned parameters (PROTOCOL rule 4: at most two)
    (1) the instrument's own knob - B, or k, or the cadence.  One per family, never crossed.
    (2) gm in {off, on} - the treatment under test, both arms always reported.
    Universes, books and costs are reported in full, not tuned.

Grid = 2 universes x [CAND20: 1 + 6 + 3 + 3 = 13 arms; EWall: 1 + 6 + 3 = 10 arms] x 2 gm
     = 2 x 23 x 2 = 92 arms, each at costs {0, 5, 10, 25} bps -> 368 reported points.

Walk-forward (PROTOCOL rule 8), selection rules fixed before any OOS number was read
    For each (universe, book, family, gm): pick the arm with the highest 2009-2016 Sharpe at
    10 bps; ties -> the slower arm (larger B, larger k, longer cadence); then evaluate
    2017-2026 untouched against the same-gm control, RULES v1 and SPY.  The pre-registered
    question specific to this idea is whether gm CHANGES THE PICK - if the selected arm
    differs between gm=off and gm=on, the published selection was an exposure choice.

Verdicts (both KEEP paths, every point)
    4a  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than v1, v1 at the SAME cost.
    4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.  Five continuous margins reported so gm's effect on 4b can be
        read as a size, not a bit flip.

Survivorship: current constituents of both lists, one-directional.  For a TURNOVER study the
direction is adverse (idea 83's caveat, restated): a survivor panel never rotates out of a
name that delisted, so realised turnover here is an underestimate and every budget is easier
to meet than it would have been live.  2020 and 2022 are the only real stress episodes.

Deterministic, standalone.  Imports research/baseline.py; modifies nothing.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v1_weights
from engine import backtest, rebalance_mask, metrics

MAX_VOL = 0.60
GROSS = 0.75                      # the common gross target G*
N_CAND = 20
BUDGETS = [0.10, 0.20, 0.40]
KS = [1.25, 1.50, 2.00]
CADENCES = ["D", "M", "Q"]        # W is the control
REPORT_COSTS = [0, 5, 10, 25]
PROTOCOL_COST = 10
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
BOOKS = ["CAND20", "EWall"]
SCRIPT = Path(__file__).name

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 800)


# ---------------------------------------------------------------- signals
def signals(px):
    """Eligibility mask and the composite's cross-sectional rank, as numpy arrays.

    The rank uses pandas' default `method='average'`, exactly as `rules_v1_weights` and every
    published CAND-n row do.  That matters: the composite is the mean of three pct-ranks and
    ties at the n-th place are common (414 days on u56), on which `rank <= n` selects 19 names
    rather than 20.  Reproducing that tie behaviour is what makes the harness check exact.
    """
    s, above, vol20 = score(px, vol_scale=False)
    elig_df = above & (vol20 < MAX_VOL)
    sc = s.where(elig_df)
    rk = sc.rank(axis=1, ascending=False).fillna(np.inf)
    return elig_df.values, rk.values


def target_ranked(rk_row, held_sel, k):
    """CAND20 target set with idea 79's rank hysteresis.

    Base selection is `rank <= n` (the published book).  With k > 1 a HELD name is kept while
    its rank stays inside the top k*n; freed slots are refilled from the best-ranked unheld
    names, up to the same count the base selection would have held that day, so hysteresis
    changes only WHICH names are held, never how many.  k = 1.0 reproduces the base exactly.
    """
    base = rk_row <= N_CAND
    n_target = int(base.sum())
    if n_target == 0:
        return base
    if k <= 1.0 or held_sel is None:
        return base
    sel = np.zeros(len(rk_row), dtype=bool)
    kept = np.where(held_sel & (rk_row <= N_CAND * k))[0]
    kept = kept[np.argsort(rk_row[kept], kind="stable")][:n_target]
    sel[kept] = True
    need = n_target - int(sel.sum())
    if need > 0:
        cand = np.where(~sel & np.isfinite(rk_row))[0]
        cand = cand[np.argsort(rk_row[cand], kind="stable")][:need]
        sel[cand] = True
    return sel


# ---------------------------------------------------------------- execution
def _execute(cur, target, budget, mode):
    """Post-trade weights under a per-rebalance |dw|_1 budget (idea 83's two modes)."""
    delta = target - cur
    tot = np.abs(delta).sum()
    if budget is None or not np.isfinite(tot) or tot <= budget:
        return target.copy()
    if mode == "pro":
        return cur + (budget / tot) * delta
    new = cur.copy()
    left = budget
    for j in np.argsort(-np.abs(delta)):
        d = delta[j]
        a = abs(d)
        if a <= 1e-15:
            break
        if a <= left:
            new[j] = target[j]
            left -= a
        else:
            new[j] = cur[j] + np.sign(d) * left
            break
    return np.clip(new, 0.0, None)


def run_arm(px, elig, rk, book, freq="W", budget=None, mode="top", k=1.0, gm=False):
    """Cost-free simulation of one arm.  Returns daily returns, turnover and realised gross.

    gm=True renormalises the post-trade vector to sum(G*) at each rebalance, BEFORE turnover
    is measured, so the matching trades are paid for.  Weights are decided at t and applied
    at t+1 (PROTOCOL 2): at loop index i the signal row used is i-1, matching engine.backtest.
    """
    rets = px.pct_change().fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n, m = rets.shape
    cur = np.zeros(m)
    held = np.zeros((n, m))
    turn = np.zeros(n)
    gross_s = np.zeros(n)
    sel_prev = None
    n_reb = n_bind = 0
    for i in range(n):
        if mask[i] and i > 0:
            row = i - 1
            if book == "EWall":
                sel = elig[row]
                c = int(sel.sum())
                tgt = (sel.astype(float) * (GROSS / c)) if c else np.zeros(m)
            else:
                sel = target_ranked(rk[row], sel_prev, k)
                tgt = sel.astype(float) * (GROSS / N_CAND)   # literal CAND-n: divides by n
                sel_prev = sel
            want = np.abs(tgt - cur).sum()
            new = _execute(cur, tgt, budget, mode)
            n_reb += 1
            if budget is not None and want > budget + 1e-12:
                n_bind += 1
            if gm:
                s = new.sum()
                if s > 1e-12:
                    new = new * (GROSS / s)
            if new.sum() > 1.0:                              # long-only, no leverage
                new = new / new.sum()
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        gross_s[i] = cur.sum()
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    r = pd.Series((held * rets).sum(axis=1), index=px.index)
    return dict(r0=r, to=pd.Series(turn, index=px.index),
                gross=pd.Series(gross_s, index=px.index),
                bind=n_bind / n_reb if n_reb else 0.0)


# ---------------------------------------------------------------- metric helpers
def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def net(r0, to, c):
    return r0 - to * c / 1e4


def margins_4b(r, spy, spy_oos, ms):
    h1, h2 = half_sharpes(r)
    s1, s2 = half_sharpes(spy)
    m = metrics(r)
    return dict(m_H1=h1 - s1, m_H2=h2 - s2,
                m_OOS=metrics(r.loc[OOS_START:])["Sharpe"] - metrics(spy_oos)["Sharpe"],
                m_DD=0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"]),
                m_CAGR=m["CAGR"] - 0.70 * ms["CAGR"])


def fail_4b(mg):
    f = [k[2:] for k, v in mg.items() if not v > 0]
    return ",".join(f) if f else "-"


def pass_4a(r, base):
    h1, h2 = half_sharpes(r)
    b1, b2 = half_sharpes(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def paired_t(a, b):
    """t on the mean daily difference (a - b), same days.  No scipy in the sandbox."""
    d = (a - b).dropna()
    sd = d.std(ddof=1)
    return float(d.mean() / (sd / np.sqrt(len(d)))) if sd > 0 else np.nan


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.3f}")


# ---------------------------------------------------------------- arms
def arm_specs(book):
    specs = [("control", np.nan, dict())]
    for B in BUDGETS:
        for mode in ["top", "pro"]:
            specs.append((f"budget-{mode}", B, dict(budget=B, mode=mode)))
    if book == "CAND20":
        for k in KS:
            specs.append(("hyst", k, dict(k=k)))
    for f in CADENCES:
        specs.append(("cadence", f, dict(freq=f)))
    return specs


def arm_name(book, fam, p, gm):
    tag = "" if fam == "control" else (f"{p}" if isinstance(p, str) else f"{p:g}")
    return f"{book}/{fam}{tag}/gm{'ON' if gm else 'OFF'}"


# ---------------------------------------------------------------- one universe
def run_universe(uname, px):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    spy_oos = spy.loc[OOS_START:]
    ms, mso = metrics(spy), metrics(spy_oos)
    s1, s2 = half_sharpes(spy)
    elig, rk = signals(px)

    print("\n" + "=" * 200)
    print(f"UNIVERSE {uname}: {px.shape[1]} names, {px.index[0].date()} -> {px.index[-1].date()}")
    print("=" * 200)
    print(f"Eval {start.date()} -> {px.index[-1].date()} | IS <= {IS_END} | OOS >= {OOS_START} | G* = {GROSS}")
    print(f"SPY  CAGR {ms['CAGR']:.2%}  Sharpe {ms['Sharpe']:.3f}  MaxDD {ms['MaxDD']:.2%}  "
          f"halves {s1:.3f}/{s2:.3f}  OOS Sharpe {mso['Sharpe']:.3f}")
    print(f"4b bars: Sharpe > {s1:.3f}/{s2:.3f} halves, > {mso['Sharpe']:.3f} OOS, "
          f"MaxDD <= {0.60*abs(ms['MaxDD']):.2%}, CAGR >= {0.70*ms['CAGR']:.2%}")
    n_elig = pd.Series(elig.sum(axis=1), index=px.index).loc[start:]
    print(f"Eligible names/day: mean {n_elig.mean():.1f}, "
          f"days with < {N_CAND} eligible: {(n_elig < N_CAND).mean():.1%}  "
          f"(this is the channel through which the literal CAND{N_CAND} de-grosses)")

    v1_res = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq="W")
    v1_r0, v1_to = v1_res["returns"].loc[start:], v1_res["turnover"].loc[start:]

    # ---- harness check: gm=off control must reproduce engine.backtest bit for bit
    print("\nHARNESS CHECK (gm=off control vs engine.backtest, cost-free)")
    worst = 0.0
    for b in BOOKS:
        if b == "EWall":
            cnt = pd.DataFrame(elig, index=px.index, columns=px.columns).sum(axis=1).replace(0, np.nan)
            w = pd.DataFrame(elig, index=px.index, columns=px.columns).astype(float).div(cnt, axis=0).mul(GROSS).fillna(0.0)
        else:
            s = score(px, vol_scale=False)[0]
            rank = s.where(pd.DataFrame(elig, index=px.index, columns=px.columns)).rank(axis=1, ascending=False)
            w = (rank <= N_CAND).astype(float) * (GROSS / N_CAND)
        a = run_arm(px, elig, rk, b)["r0"].loc[start:]
        e = backtest(px, w, cost_bps=0.0, freq="W")["returns"].loc[start:]
        d = float((a - e).abs().max())
        worst = max(worst, d)
        print(f"  {b:<7} max |harness - engine| = {d:.3e}")
    print(f"  worst = {worst:.3e}  ({'EXACT' if worst < 1e-10 else 'NOT EXACT - results below are unsafe'})")

    # ---- build every arm
    arms = {}
    for b in BOOKS:
        for fam, p, kw in arm_specs(b):
            for gm in (False, True):
                arms[(b, fam, p, gm)] = run_arm(px, elig, rk, b, gm=gm, **kw)

    rows = []
    for (b, fam, p, gm), res in arms.items():
        r0, to = res["r0"].loc[start:], res["to"].loc[start:]
        yrs = metrics(r0)["Years"]
        gr = res["gross"].loc[start:]
        for c in REPORT_COSTS:
            r = net(r0, to, c)
            base = net(v1_r0, v1_to, c)
            m = metrics(r)
            h1, h2 = half_sharpes(r)
            roos = r.loc[OOS_START:]
            mg = margins_4b(r, spy, spy_oos, ms)
            rows.append(dict(universe=uname, book=b, fam=fam, param=p, gm=gm, cost=c,
                             arm=arm_name(b, fam, p, gm),
                             CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                             IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                             OOS_CAGR=metrics(roos)["CAGR"], OOS_Sharpe=metrics(roos)["Sharpe"],
                             OOS_MaxDD=metrics(roos)["MaxDD"],
                             TO=to.sum() / yrs, gross=gr.mean(), gross_reb=gr[to > 0].mean(),
                             bind=res["bind"], p4a=pass_4a(r, base), **mg))
    df = pd.DataFrame(rows)
    df["f4b"] = [fail_4b({k: v for k, v in row.items() if k.startswith("m_")}) for _, row in df.iterrows()]
    df["p4b"] = df["f4b"] == "-"

    print(f"\nFULL GRID {uname} - {len(df)} points, ALL reported ({len(arms)} arms x {len(REPORT_COSTS)} costs)")
    cols = ["arm", "cost", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe",
            "OOS_MaxDD", "TO", "gross", "bind", "m_DD", "m_CAGR", "p4a", "p4b", "f4b"]
    print(fmt(df[cols].sort_values(["arm", "cost"]).reset_index(drop=True)))

    # ---- did gross-matching actually bind?  (the treatment's own diagnostic)
    print("\nREALISED GROSS by arm (mean over all days / mean on rebalance days) - "
          "gm=ON should sit at G* on rebalance days")
    g = df[df.cost == PROTOCOL_COST].pivot_table(index=["book", "fam", "param"], columns="gm",
                                                 values=["gross", "gross_reb", "TO"], dropna=False)
    print(fmt(g))

    # ---- THE TEST: does each instrument's published effect survive gross-matching?
    print(f"\nEFFECT OF EACH INSTRUMENT vs its OWN-gm control, at {PROTOCOL_COST} bps")
    print("  dCAGR/dSharpe/dMaxDD = arm minus the control at the SAME gm.  If an effect is real")
    print("  turnover, the gm=OFF and gm=ON columns agree; if it was exposure, they do not.")
    at = df[df.cost == PROTOCOL_COST]
    eff = []
    for b in BOOKS:
        for gm in (False, True):
            ctl = at[(at.book == b) & (at.fam == "control") & (at.gm == gm)].iloc[0]
            ctl_r = net(arms[(b, "control", np.nan, gm)]["r0"].loc[start:],
                        arms[(b, "control", np.nan, gm)]["to"].loc[start:], PROTOCOL_COST)
            for fam, p, _ in arm_specs(b):
                if fam == "control":
                    continue
                a = at[(at.book == b) & (at.fam == fam) & (at.param.astype(str) == str(p)) & (at.gm == gm)].iloc[0]
                a_r = net(arms[(b, fam, p, gm)]["r0"].loc[start:],
                          arms[(b, fam, p, gm)]["to"].loc[start:], PROTOCOL_COST)
                dDD = (abs(ctl.MaxDD) - abs(a.MaxDD)) * 100
                dC = (a.CAGR - ctl.CAGR) * 100
                eff.append(dict(book=b, instrument=f"{fam}{'' if isinstance(p, float) and np.isnan(p) else (p if isinstance(p, str) else f'{p:g}')}",
                                gm=gm, dCAGR_pp=dC, dSharpe=a.Sharpe - ctl.Sharpe, dMaxDD_pp=dDD,
                                t_dSharpe=paired_t(a_r, ctl_r), dTO=a.TO - ctl.TO,
                                dGross=a.gross - ctl.gross, p4b=a.p4b))
    ef = pd.DataFrame(eff)
    piv = ef.pivot_table(index=["book", "instrument"], columns="gm",
                         values=["dCAGR_pp", "dSharpe", "t_dSharpe", "dMaxDD_pp", "dTO", "dGross"],
                         dropna=False)
    print(fmt(piv))

    print("\nSURVIVAL TEST per instrument: sign and size of the effect, gm=OFF -> gm=ON")
    print("  'survives' = same sign on BOTH dCAGR and dMaxDD and |gm=ON| >= 50% of |gm=OFF| on dCAGR")
    surv = []
    for (b, inst), grp in ef.groupby(["book", "instrument"]):
        o = grp[~grp.gm].iloc[0]
        n_ = grp[grp.gm].iloc[0]
        same = (np.sign(o.dCAGR_pp) == np.sign(n_.dCAGR_pp)) and (np.sign(o.dMaxDD_pp) == np.sign(n_.dMaxDD_pp))
        big = abs(n_.dCAGR_pp) >= 0.5 * abs(o.dCAGR_pp) if abs(o.dCAGR_pp) > 1e-9 else True
        surv.append(dict(book=b, instrument=inst, dCAGR_off=o.dCAGR_pp, dCAGR_on=n_.dCAGR_pp,
                         dMaxDD_off=o.dMaxDD_pp, dMaxDD_on=n_.dMaxDD_pp,
                         dGross_off=o.dGross, dGross_on=n_.dGross,
                         shrink=(n_.dCAGR_pp / o.dCAGR_pp) if abs(o.dCAGR_pp) > 1e-9 else np.nan,
                         survives=bool(same and big)))
    sv = pd.DataFrame(surv).sort_values(["book", "instrument"])
    print(fmt(sv.set_index(["book", "instrument"])))

    # ---- walk-forward (PROTOCOL rule 8)
    print("\nWALK-FORWARD (rule 8): parameter chosen on 2009-2016 Sharpe at 10 bps, OOS untouched")
    print("  Pre-registered question: does gm CHANGE THE PICK?")
    order_key = {"budget-top": lambda p: p, "budget-pro": lambda p: p, "hyst": lambda p: p,
                 "cadence": lambda p: {"D": 0, "W": 1, "M": 2, "Q": 3}[p]}
    wf = []
    at10 = df[df.cost == PROTOCOL_COST]
    for b in BOOKS:
        fams = sorted({f for f, _, _ in arm_specs(b) if f != "control"})
        for gm in (False, True):
            ctl = at10[(at10.book == b) & (at10.fam == "control") & (at10.gm == gm)].iloc[0]
            wf.append(dict(book=b, gm=gm, family="control", picked=ctl.arm, IS_Sharpe=ctl.IS_Sharpe,
                           OOS_CAGR=ctl.OOS_CAGR, OOS_Sharpe=ctl.OOS_Sharpe, OOS_MaxDD=ctl.OOS_MaxDD,
                           OOS_4b=ctl.p4b))
            for fam in fams:
                sub = at10[(at10.book == b) & (at10.fam.isin([fam, "control"])) & (at10.gm == gm)].copy()
                sub["tie"] = [order_key[fam](r.param) if r.fam == fam else -1 for _, r in sub.iterrows()]
                pick = sub.sort_values(["IS_Sharpe", "tie"], ascending=False).iloc[0]
                wf.append(dict(book=b, gm=gm, family=fam, picked=pick.arm, IS_Sharpe=pick.IS_Sharpe,
                               OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                               OOS_MaxDD=pick.OOS_MaxDD, OOS_4b=pick.p4b))
    wfd = pd.DataFrame(wf)
    print(fmt(wfd.set_index(["book", "family", "gm"])))

    v1_10 = net(v1_r0, v1_to, PROTOCOL_COST)
    for nm, r in [("RULES v1 baseline", v1_10), ("SPY", spy)]:
        ro = r.loc[OOS_START:]
        m, mo = metrics(r), metrics(ro)
        print(f"  reference {nm:<18} full {m['CAGR']:.2%}/{m['Sharpe']:.3f}/{m['MaxDD']:.2%}   "
              f"OOS {mo['CAGR']:.2%}/{mo['Sharpe']:.3f}/{mo['MaxDD']:.2%}")

    print("\nDoes gm change the rule-8 pick?")
    for b in BOOKS:
        for fam in sorted({f for f, _, _ in arm_specs(b) if f != "control"}):
            o = wfd[(wfd.book == b) & (wfd.family == fam) & (~wfd.gm)].iloc[0]
            n_ = wfd[(wfd.book == b) & (wfd.family == fam) & (wfd.gm)].iloc[0]
            po = o.picked.split("/")[1]
            pn = n_.picked.split("/")[1]
            print(f"  {b:<7} {fam:<11} gmOFF picks {po:<14} (OOS Sh {o.OOS_Sharpe:.3f})   "
                  f"gmON picks {pn:<14} (OOS Sh {n_.OOS_Sharpe:.3f})   "
                  f"{'SAME' if po == pn else '*** CHANGED ***'}")

    print(f"\n{uname} SUMMARY: 4b passes {int(df.p4b.sum())}/{len(df)} points "
          f"(gmOFF {int(df[~df.gm].p4b.sum())}/{len(df[~df.gm])}, gmON {int(df[df.gm].p4b.sum())}/{len(df[df.gm])}), "
          f"4a passes {int(df.p4a.sum())}/{len(df)}")
    ef["universe"] = uname
    sv["universe"] = uname
    wfd["universe"] = uname
    return df, ef, sv, wfd


def main():
    outs = []
    for uname, px in [("u56", load_universe()), ("broad136", load_universe(broad=True))]:
        outs.append(run_universe(uname, px))
    grid = pd.concat([o[0] for o in outs], ignore_index=True)
    ef = pd.concat([o[1] for o in outs], ignore_index=True)
    sv = pd.concat([o[2] for o in outs], ignore_index=True)
    wfd = pd.concat([o[3] for o in outs], ignore_index=True)
    grid.to_csv(REPO / "research" / "backtests" / SCRIPT.replace(".py", ".grid.csv"), index=False)
    sv.to_csv(REPO / "research" / "backtests" / SCRIPT.replace(".py", ".survival.csv"), index=False)
    ef.to_csv(REPO / "research" / "backtests" / SCRIPT.replace(".py", ".effects.csv"), index=False)

    print("\n" + "=" * 200)
    print("CROSS-UNIVERSE VERDICT")
    print("=" * 200)
    print(f"Total reported points: {len(grid)}   4b passes: {int(grid.p4b.sum())}   4a passes: {int(grid.p4a.sum())}")

    print("\nMean effect by instrument FAMILY, both universes and books, 10 bps")
    ef["family"] = ef.instrument.str.replace(r"[\d.]+$", "", regex=True).str.rstrip("DMQ")
    fam = ef.groupby(["family", "gm"])[["dCAGR_pp", "dSharpe", "t_dSharpe", "dMaxDD_pp", "dTO", "dGross"]].mean()
    print(fmt(fam))

    print("\nSURVIVAL SCOREBOARD (per instrument arm, 4 book x universe cells each)")
    sc = sv.groupby("instrument").agg(cells=("survives", "size"), survived=("survives", "sum"),
                                      mean_dCAGR_off=("dCAGR_off", "mean"),
                                      mean_dCAGR_on=("dCAGR_on", "mean"),
                                      mean_dMaxDD_off=("dMaxDD_off", "mean"),
                                      mean_dMaxDD_on=("dMaxDD_on", "mean"),
                                      mean_dGross_off=("dGross_off", "mean"))
    print(fmt(sc))
    print(f"\nOverall: {int(sv.survives.sum())}/{len(sv)} instrument-cells survive gross-matching.")

    print("\nSIGN FLIPS (effect reverses direction once gross is matched) - the headline")
    fl = sv[(np.sign(sv.dCAGR_off) != np.sign(sv.dCAGR_on)) |
            (np.sign(sv.dMaxDD_off) != np.sign(sv.dMaxDD_on))]
    print("  NONE" if fl.empty else fmt(fl.set_index(["universe", "book", "instrument"])
                                        [["dCAGR_off", "dCAGR_on", "dMaxDD_off", "dMaxDD_on", "dGross_off"]]))

    print("\nRULE-8 PICKS: how often does gross-matching change the selected arm?")
    ch = []
    for (u, b, f), grp in wfd[wfd.family != "control"].groupby(["universe", "book", "family"]):
        o = grp[~grp.gm].iloc[0]
        n_ = grp[grp.gm].iloc[0]
        ch.append(dict(universe=u, book=b, family=f,
                       pick_off=o.picked.split("/")[1], pick_on=n_.picked.split("/")[1],
                       OOS_Sh_off=o.OOS_Sharpe, OOS_Sh_on=n_.OOS_Sharpe,
                       changed=o.picked.split("/")[1] != n_.picked.split("/")[1]))
    chd = pd.DataFrame(ch)
    print(fmt(chd.set_index(["universe", "book", "family"])))
    print(f"\nPicks changed by gross-matching: {int(chd.changed.sum())}/{len(chd)}")

    print("\n4b PASSES at 10 bps, both universes (the capital test)")
    p = grid[(grid.cost == PROTOCOL_COST) & grid.p4b]
    if p.empty:
        print("  NONE")
    else:
        print(fmt(p[["universe", "arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "TO", "gross"]]
                  .sort_values(["universe", "arm"]).reset_index(drop=True)))
        both = (p.groupby(p.arm.str.replace("^(u56|broad136)/", "", regex=True))
                 .universe.nunique())
        arms_both = sorted(set(p[p.universe == "u56"].arm) & set(p[p.universe == "broad136"].arm))
        print(f"\n  Arms passing 4b on BOTH universes at 10 bps: "
              f"{arms_both if arms_both else 'NONE'}")
    print(f"\nScript: {SCRIPT}")


if __name__ == "__main__":
    main()
