#!/usr/bin/env python3
"""QUEUE idea 85 — exit-schedule-vs-entry-schedule (cloud, 2026-09-04).

Question
--------
Idea 83 killed the per-rebalance turnover budget and explained the kill with a mechanism:
book turnover is mostly the 200d gate's EXITS, so a budget that truncates the trade list
constrains SELLING and therefore costs drawdown (-2.4pp pro-rata, -5.1pp largest-first).
That claim has never been measured.  This run measures it and then tests the remedy the
queue proposed:

    (a) Decompose Sigma|dw| per rebalance into its ENTRY leg (buys) and EXIT leg (sells),
        and attribute the exit leg to the eligibility GATE, to RANK displacement, or to
        drift TRIMS.  Is the mechanism claim true?
    (b) Budget ONLY the entry leg, honouring every exit in full.  If the mechanism holds,
        an entry-only budget should cut turnover without idea 83's drawdown penalty.

Pre-registered before any number was read
-----------------------------------------
A long-only book that resets to a fixed gross is self-financing at each rebalance, so buys
and sells must be near-equal by construction and neither leg can be "most" of turnover in
any interesting sense; the informative split is the ATTRIBUTION of the exit leg, not its
size.  And honouring every exit while capping the buys RAISES CASH -- so an entry-only
budget is a de-grossing instrument, i.e. idea 66's exact lever wearing a turnover label,
the mirror of idea 83's own finding that a truncated trade list is a disguised gross lever.

    H_mech : the exit leg is majority gate-driven (>50% of exit magnitude).
    H_fix  : entry-only budgeting improves the CAGR-per-pp-of-MaxDD exchange rate against
             the gross lever's ~0.68 pp/pp (ideas 66/83), i.e. it buys drawdown more
             cheaply than simply holding less.  If it does not beat the lever, the remedy
             is a relabelled lever and the queue item is answered NO.
Sharpe is the arbiter: ideas 66/86 established that a pure gross change leaves Sharpe
unmoved (dSharpe 0.000, corr 1.0000), so any real turnover effect must show up as dSharpe
against the unconstrained control, not as a CAGR or MaxDD level.

Design (PROTOCOL rules 1-8)
---------------------------
Universes : universe.json (56) and universe_broad.json (136).  SURVIVORSHIP: current
            constituents, absolute CAGRs optimistic; every arm shares the panel, so the
            control-vs-arm comparisons are far less exposed than the levels.
Books     : CAND20 = idea 2's standing 4b candidate (top 20 eligible by the v1 composite
            WITHOUT /sqrt(vol20), equal weight at 0.75/20, cash when E_t < 20).
            EWall  = idea 10/72's `B136/EWall` (equal-weight every eligible name at 0.75).
            Eligibility = RULES v1's gate (above the 200d MA, vol20 < 0.60), unchanged.
Params    : exactly 2 tuned -- the budget B in {inf, 0.30, 0.20, 0.15, 0.10, 0.05} and the
            MODE in {entry (this idea), total (idea 83's pro-rata control)}.  Books,
            universes and the gross reference ladder are reported in full, not tuned.
Reference : a gross ladder g in {0.50,0.60,0.70,0.75} per book measures the lever's own
            exchange rate on the same days, so the remedy is judged against it rather than
            against an assumed 0.68.
Execution : weights decided at close t, applied t+1; weekly; 10 bps per unit turnover
            (25 bps also reported); long-only, no leverage.
Walk-fwd  : rule 8 -- B chosen on 2009-2016 (IS) alone under two rules fixed in advance
            (R0 = argmax IS Sharpe, R2 = argmax IS Sharpe subject to the IS 4b drawdown cap
            and CAGR floor), evaluated untouched on 2017-2026.  Both KEEP paths (4a, 4b)
            are evaluated for every arm, full sample and on the OOS window.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-04_exit-schedule-vs-entry-schedule_cloud"
COST, FREQ, MAX_VOL, GROSS, NCAND = 10.0, "W", 0.60, 0.75, 20
IS_END, OOS_START = "2016-12-31", "2017-01-01"
BUDGETS = [np.inf, 0.30, 0.20, 0.15, 0.10, 0.05]
GLADDER = [0.50, 0.60, 0.70, 0.75]


# ---------------------------------------------------------------- construction
def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def signals(px):
    vol = px.pct_change().rolling(20).std() * np.sqrt(252)
    elig = ((vol < MAX_VOL) & (px > px.rolling(200).mean())).fillna(False)
    rk = composite(px).where(elig).rank(axis=1, ascending=False).fillna(np.inf)
    return elig.values, rk.values


def target(book, elig_row, rk_row, g):
    if book == "EWall":
        c = int(elig_row.sum())
        return (elig_row.astype(float) * (g / c)) if c else np.zeros(len(elig_row)), elig_row.copy()
    sel = rk_row <= NCAND
    return sel.astype(float) * (g / NCAND), sel


# ---------------------------------------------------------------- simulation
def run(px, elig, rk, book, budget=np.inf, mode="entry", g=GROSS):
    """One arm.  Cost-free returns + turnover + the entry/exit decomposition.

    Execution at a rebalance:
      mode 'entry' -- every SELL is executed in full; the BUY leg is scaled pro-rata so its
                      total is at most `budget`.  Unspent proceeds sit in cash (gross falls).
      mode 'total' -- idea 83's pro-rata mode: the whole delta vector is scaled by
                      budget/|delta|_1, which truncates buys and sells alike.
    Weights decided at t are applied at t+1 (signal row i-1 at loop index i), matching
    engine.backtest.
    """
    rets = px.pct_change().fillna(0.0).values
    mask = rebalance_mask(px.index, FREQ).shift(1, fill_value=False).values
    n, m = rets.shape
    cur = np.zeros(m)
    held = np.zeros((n, m))
    turn = np.zeros(n)
    gross_s = np.zeros(n)
    ent = ex = 0.0                       # wanted-leg magnitudes (pre-budget)
    ex_gate = ex_rank = ex_trim = 0.0    # attribution of the wanted exit leg
    nreb = nbind = 0
    sel_prev = None
    el_prev = None
    for i in range(n):
        if mask[i] and i > 0:
            row = i - 1
            tgt, sel = target(book, elig[row], rk[row], g)
            d = tgt - cur
            e_leg = float(d[d > 0].sum())
            x_leg = float(-d[d < 0].sum())
            ent += e_leg
            ex += x_leg
            if sel_prev is not None:
                for j in np.where(d < 0)[0]:
                    a = -float(d[j])
                    if sel_prev[j] and not elig[row][j]:
                        ex_gate += a                      # lost eligibility
                    elif sel_prev[j] and not sel[j]:
                        ex_rank += a                      # still eligible, displaced
                    else:
                        ex_trim += a                      # still held, weight trimmed
            new = tgt.copy()
            if np.isfinite(budget):
                if mode == "entry":
                    if e_leg > budget + 1e-12:
                        new = cur + np.where(d > 0, d * (budget / e_leg), d)
                        nbind += 1
                else:
                    tot = e_leg + x_leg
                    if tot > budget + 1e-12:
                        new = cur + d * (budget / tot)
                        nbind += 1
            new = np.clip(new, 0.0, None)
            if new.sum() > 1.0:
                new = new / new.sum()
            turn[i] = np.abs(new - cur).sum()
            cur = new
            sel_prev, el_prev = sel, elig[row]
            nreb += 1
        held[i] = cur
        gross_s[i] = cur.sum()
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    tot_ex = ex_gate + ex_rank + ex_trim
    return dict(
        r0=pd.Series((held * rets).sum(axis=1), index=px.index),
        to=pd.Series(turn, index=px.index),
        gross=pd.Series(gross_s, index=px.index),
        entry_share=ent / (ent + ex) if ent + ex else np.nan,
        gate=ex_gate / tot_ex if tot_ex else np.nan,
        rank=ex_rank / tot_ex if tot_ex else np.nan,
        trim=ex_trim / tot_ex if tot_ex else np.nan,
        bind=nbind / nreb if nreb else 0.0)


def net(r0, to, bps=COST):
    return r0 - to * bps / 1e4


# ---------------------------------------------------------------- metrics
def m3(r):
    d = metrics(r)
    return d["CAGR"], d["Sharpe"], d["MaxDD"]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars4b(r, spy):
    c, s, dd = m3(r); sc, ss, sdd = m3(spy)
    bad = []
    if s <= ss: bad.append("Sh")
    if dd < 0.60 * sdd: bad.append("DD")
    if c < 0.70 * sc: bad.append("CAGR")
    return bad


def fail4b_full(r, spy):
    c, s, dd = m3(r); h1, h2 = halves(r)
    sc, ss, sdd = m3(spy); s1, s2 = halves(spy)
    o = metrics(r.loc[OOS_START:])["Sharpe"]; so = metrics(spy.loc[OOS_START:])["Sharpe"]
    bad = []
    if h1 <= s1: bad.append("H1")
    if h2 <= s2: bad.append("H2")
    if o <= so: bad.append("OOS")
    if dd < 0.60 * sdd: bad.append("DD")
    if c < 0.70 * sc: bad.append("CAGR")
    return bad


def fail4a(r, base):
    _, _, dd = m3(r); h1, h2 = halves(r)
    _, _, bdd = m3(base); b1, b2 = halves(base)
    bad = []
    if h1 <= b1: bad.append("H1")
    if h2 <= b2: bad.append("H2")
    if dd < bdd: bad.append("DD")
    return bad


def paired_t(a, b):
    """Daily excess-return t-stat, arm minus control."""
    d = (a - b).dropna()
    return float(d.mean() / (d.std(ddof=1) / np.sqrt(len(d)))) if d.std(ddof=1) else np.nan


# ---------------------------------------------------------------- one universe
def run_universe(px, tag, rows):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    base = backtest(px, rules_v1_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
    spy_is = spy.loc[:IS_END]
    yrs = len(spy) / 252
    elig, rk = signals(px)

    print("\n" + "=" * 158)
    sc, ss, sdd = m3(spy); s1, s2 = halves(spy)
    print(f"{tag}: {px.shape[1]} tickers, eval {start.date()} -> {px.index[-1].date()}")
    print(f"  SPY full {sc:.1%}/{ss:.3f}/{sdd:.1%} halves {s1:.3f}/{s2:.3f} | "
          f"v1 full {m3(base)[0]:.1%}/{m3(base)[1]:.3f}/{m3(base)[2]:.1%} (4a reference) | "
          f"IS 4b bars: Sh>{m3(spy_is)[1]:.3f}, DD>={0.60*m3(spy_is)[2]:.1%}, "
          f"CAGR>={0.70*m3(spy_is)[0]:.1%}")
    print("=" * 158)

    out = []
    for book in ("CAND20", "EWall"):
        ctrl = run(px, elig, rk, book)
        rc = net(ctrl["r0"], ctrl["to"]).loc[start:]
        print(f"\n[{tag}] {book} — TURNOVER DECOMPOSITION (unconstrained control)")
        print(f"  entry leg {ctrl['entry_share']:.1%} of Sigma|dw|, exit leg "
              f"{1 - ctrl['entry_share']:.1%}   (a self-financing book must be ~50/50)")
        print(f"  EXIT LEG ATTRIBUTION: gate {ctrl['gate']:.1%} | rank displacement "
              f"{ctrl['rank']:.1%} | drift trims {ctrl['trim']:.1%}   <- idea 83's claim is "
              f"'mostly the gate'")
        print(f"  control: {m3(rc)[0]:.1%}/{m3(rc)[1]:.3f}/{m3(rc)[2]:.1%}, turnover "
              f"{ctrl['to'].loc[start:].sum()/yrs:.1f}x/yr, mean gross {ctrl['gross'].loc[start:].mean():.3f}")

        print(f"\n[{tag}] {book} — ARMS (all reported; control = B=inf)")
        print(f"  {'mode':<7}{'B':>6}{'bind%':>7}{'gross':>7}{'turn':>6}{'CAGR':>8}{'Sharpe':>8}"
              f"{'MaxDD':>8}{'H1':>7}{'H2':>7}{'25bpSh':>8}{'ISsh':>7}{'OOSsh':>7}{'OOSdd':>8}"
              f"{'dSh':>7}{'t':>6}{'pp/pp':>7}  {'4a':<8}{'4b':<12}{'4bOOS':<8}")
        arms = []
        for mode in ("entry", "total"):
            for B in BUDGETS:
                if not np.isfinite(B) and mode == "total":
                    continue                      # the control is shared, printed once
                a = run(px, elig, rk, book, B, mode)
                r = net(a["r0"], a["to"]).loc[start:]
                r25 = net(a["r0"], a["to"], 25.0).loc[start:]
                c, s, dd = m3(r); h1, h2 = halves(r)
                cc, cs, cdd = m3(rc)
                ddd = dd - cdd
                pp = (c - cc) / ddd if abs(ddd) > 1e-6 else np.nan
                rec = dict(universe=tag, book=book, mode=mode, B=B,
                           bind=a["bind"], gross=a["gross"].loc[start:].mean(),
                           turn=a["to"].loc[start:].sum() / yrs,
                           CAGR=c, Sharpe=s, MaxDD=dd, H1=h1, H2=h2,
                           Sharpe25=m3(r25)[1],
                           IS_Sharpe=m3(r.loc[:IS_END])[1], IS_CAGR=m3(r.loc[:IS_END])[0],
                           IS_MaxDD=m3(r.loc[:IS_END])[2],
                           OOS_CAGR=m3(r.loc[OOS_START:])[0],
                           OOS_Sharpe=m3(r.loc[OOS_START:])[1],
                           OOS_MaxDD=m3(r.loc[OOS_START:])[2],
                           dSharpe=s - cs, t=paired_t(r, rc), pp_per_pp=pp,
                           f4a=",".join(fail4a(r, base)) or "PASS",
                           f4b=",".join(fail4b_full(r, spy)) or "PASS",
                           oos4b=",".join(bars4b(r.loc[OOS_START:], spy.loc[OOS_START:])) or "PASS",
                           entry_share=a["entry_share"], gate=a["gate"])
                arms.append(rec)
                lab = "control" if not np.isfinite(B) else mode
                bs = "inf" if not np.isfinite(B) else f"{B:.2f}"
                print(f"  {lab:<7}{bs:>6}{a['bind']:7.0%}{rec['gross']:7.3f}{rec['turn']:6.1f}"
                      f"{c:8.1%}{s:8.3f}{dd:8.1%}{h1:7.3f}{h2:7.3f}{rec['Sharpe25']:8.3f}"
                      f"{rec['IS_Sharpe']:7.3f}{rec['OOS_Sharpe']:7.3f}{rec['OOS_MaxDD']:8.1%}"
                      f"{rec['dSharpe']:+7.3f}{rec['t']:+6.2f}"
                      f"{(pp if np.isfinite(pp) else np.nan):7.2f}  {rec['f4a']:<8}"
                      f"{rec['f4b']:<12}{rec['oos4b']:<8}")

        # ---- the reference lever, measured on the same days ---------------
        print(f"\n[{tag}] {book} — GROSS LADDER (idea 66's lever, the exchange rate to beat)")
        print(f"  {'g':>6}{'turn':>6}{'CAGR':>8}{'Sharpe':>8}{'MaxDD':>8}{'dSh':>7}{'pp/pp':>7}")
        lev = []
        for g in GLADDER:
            a = run(px, elig, rk, book, np.inf, "entry", g)
            r = net(a["r0"], a["to"]).loc[start:]
            c, s, dd = m3(r); cc, cs, cdd = m3(rc)
            ddd = dd - cdd
            pp = (c - cc) / ddd if abs(ddd) > 1e-6 else np.nan
            lev.append(pp)
            print(f"  {g:6.2f}{a['to'].loc[start:].sum()/yrs:6.1f}{c:8.1%}{s:8.3f}{dd:8.1%}"
                  f"{s - cs:+7.3f}{(pp if np.isfinite(pp) else np.nan):7.2f}")
            rows.append(dict(universe=tag, book=book, mode="gross", B=g, CAGR=c, Sharpe=s,
                             MaxDD=dd, turn=a["to"].loc[start:].sum() / yrs, pp_per_pp=pp))
        lev_rate = np.nanmean([x for x in lev if np.isfinite(x)])
        print(f"  lever exchange rate (mean over the ladder): {lev_rate:.2f} pp CAGR per pp MaxDD")

        # ---- rule 8 -------------------------------------------------------
        d = pd.DataFrame(arms)
        for mode in ("entry", "total"):
            sub = d[(d["mode"] == mode) | (~np.isfinite(d.B))].reset_index(drop=True)
            i0 = int(sub.IS_Sharpe.idxmax())
            feas = sub[(sub.IS_MaxDD >= 0.60 * m3(spy_is)[2]) & (sub.IS_CAGR >= 0.70 * m3(spy_is)[0])]
            i2 = int(feas.IS_Sharpe.idxmax()) if len(feas) else None
            b0 = "inf" if not np.isfinite(sub.B[i0]) else f"{sub.B[i0]:.2f}"
            print(f"  rule 8 [{mode}] R0 picks B={b0}: OOS {sub.OOS_CAGR[i0]:.1%}/"
                  f"{sub.OOS_Sharpe[i0]:.3f}/{sub.OOS_MaxDD[i0]:.1%}"
                  f"  (grid OOS-best {sub.OOS_Sharpe.max():.3f})", end="")
            if i2 is None:
                print("   R2: INFEASIBLE")
            else:
                b2 = "inf" if not np.isfinite(sub.B[i2]) else f"{sub.B[i2]:.2f}"
                print(f"   R2 picks B={b2}: OOS {sub.OOS_CAGR[i2]:.1%}/{sub.OOS_Sharpe[i2]:.3f}"
                      f"/{sub.OOS_MaxDD[i2]:.1%}")
        out += arms
        for rec in arms:
            rec["lever_rate"] = lev_rate
        rows += arms
    return out


# ---------------------------------------------------------------- main
def main():
    pd.set_option("display.width", 220)
    px = load_universe()
    pxb = load_universe(broad=True)

    print("HARNESS SANITY (published rows must reproduce before any new number is read)")
    for p_, tag, book, pub in ((px, "u56", "CAND20", "12.7%/1.093/-18.3% halves 1.088/1.103"),
                               (pxb, "broad", "EWall", "10.7%/1.027/-17.7% halves 1.146/0.917")):
        e, k = signals(p_)
        a = run(p_, e, k, book)
        r = net(a["r0"], a["to"]).loc[p_.index[260]:]
        c, s, dd = m3(r); h1, h2 = halves(r)
        print(f"  {tag} {book}: {c:.1%}/{s:.3f}/{dd:.1%} halves {h1:.3f}/{h2:.3f}   (published {pub})")

    rows = []
    all_arms = run_universe(px, "u56", rows) + run_universe(pxb, "broad", rows)
    A = pd.DataFrame(all_arms)
    pd.DataFrame(rows).to_csv(ROOT / "research" / "backtests" / f"{STEM}.grid.csv", index=False)

    print("\n" + "=" * 158)
    print("SUMMARY")
    print("=" * 158)
    ctl = A[~np.isfinite(A.B)]
    print("(1) MECHANISM — is book turnover 'mostly the gate's exits'?")
    for _, r_ in ctl.iterrows():
        print(f"    {r_.universe:<6}{r_.book:<8} entry leg {r_.entry_share:.1%} | exit leg "
              f"attribution: gate {r_.gate:.1%}")
    print("\n(2) REMEDY — entry-only budget vs idea 83's total budget vs the gross lever")
    con = A[np.isfinite(A.B)].merge(
        ctl[["universe", "book", "MaxDD", "CAGR", "turn"]].rename(
            columns={"MaxDD": "cMaxDD", "CAGR": "cCAGR", "turn": "cturn"}),
        on=["universe", "book"], how="left")
    for mode in ("entry", "total"):
        s_ = con[con["mode"] == mode]
        print(f"    {mode:<6} n={len(s_):<3} mean dSharpe {s_.dSharpe.mean():+.3f} "
              f"(>0 in {int((s_.dSharpe > 0).sum())}/{len(s_)}, |t|>2 in "
              f"{int((s_.t.abs() > 2).sum())}/{len(s_)})   mean dMaxDD "
              f"{(s_.MaxDD - s_.cMaxDD).mean():+.1%}   mean turnover cut "
              f"{(1 - s_.turn / s_.cturn).mean():.0%}"
              f"   mean exchange rate {s_.pp_per_pp.mean():.2f} pp/pp "
              f"(lever {ctl.lever_rate.mean():.2f})")
    print("\n(3) KEEP paths over all arms: 4b PASS "
          f"{int((A.f4b == 'PASS').sum())}/{len(A)}, 4b OOS PASS "
          f"{int((A.oos4b == 'PASS').sum())}/{len(A)}, 4a PASS {int((A.f4a == 'PASS').sum())}/{len(A)}")
    print(f"\nfull grid -> {STEM}.grid.csv")


if __name__ == "__main__":
    main()
