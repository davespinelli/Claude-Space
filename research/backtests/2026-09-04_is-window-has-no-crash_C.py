#!/usr/bin/env python3
"""QUEUE idea 89 — is-window-has-no-crash (lane C, 2026-09-04).

Question
--------
Idea 87 found that on the incumbent rule-8 split the in-sample window's SPY MaxDD is
-22.1% while the out-of-sample window's is -33.7%.  If that asymmetry is what makes the
4b drawdown cap the *loose* constraint in-sample, then every rule-8 selection on a risk
parameter has been fitted on a sample containing no COVID-scale crash, and the published
selections may be an artefact of where the split was drawn.

    Does moving the rule-8 split change the published selections, and does a split whose
    IS window CONTAINS a crash select better?

Design (PROTOCOL rules 1-8)
---------------------------
Universes : universe.json (56) and universe_broad.json (136).  SURVIVORSHIP: current
            constituents; absolute CAGRs optimistic.  This run compares *split dates on a
            common grid*, so the bias hits every arm and every split alike.
Grids     : the six published 1-parameter grids re-run verbatim from idea 87's harness, so
            the incumbent-split column reproduces the published selections:
              GROSS/top20   g    in {0.50,0.60,0.70,0.75,0.80,0.90,1.00}   (ideas 66, 2)
              GROSS/EWall   g    same grid                                  (idea 66)
              BAND/ew-all   band in {0,0.02,0.03,0.05,0.08}                 (idea 57)
              N/ranked      n    in {5,10,15,20,30,40}                      (idea 2)
              CRYPTO/CAND20 cap  in {0,0.05,0.10,0.15}                      (idea 15)
              CRYPTO/EWall  cap  same grid                                  (idea 15)
Params    : exactly 2 -- the grid parameter and the SPLIT DATE (the thing under test):
              S13  IS 2009-2013 / OOS 2014-2026   (IS holds 2011's -19% but no crash)
              S16  IS 2009-2016 / OOS 2017-2026   (INCUMBENT rule 8)
              S21  IS 2009-2021 / OOS 2022-2026   (IS holds the 2020 COVID crash)
            Every grid point is printed with full-sample, per-split IS and per-split OOS
            statistics.  Nothing is tuned to make a result appear.
Selection : rule 8 as written -- argmax IS Sharpe, fitted on the IS window ONLY, evaluated
            untouched on that split's OOS window.
Outcomes  : pre-registered before any number was read --
            (a) how many of the 12 universe x grid selections CHANGE when the split moves;
            (b) SPY IS vs OOS MaxDD per split, and whether the IS 4b DD cap binds (is it
                loose because the IS window lacks a crash, per idea 87's premise?);
            (c) selection quality per split: pick's OOS Sharpe rank within its grid and
                regret vs the grid's OOS-best, plus Spearman(IS Sharpe, OOS Sharpe);
            (d) apples-to-apples: every split's pick re-scored on the COMMON window
                2022-2026, which is out-of-sample for all three splits.
KEEP paths: both are evaluated per arm -- 4a (Sharpe > RULES v1 in BOTH halves and MaxDD
            no worse) and 4b (Sharpe > SPY in both halves AND OOS, MaxDD <= 60% of SPY's,
            CAGR >= 70% of SPY's), full sample; 4b is also evaluated on each OOS window.
Execution : weekly, weights at close t applied t+1, 10 bps per unit turnover.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

COST, FREQ, MAX_VOL = 10, "W", 0.60
GROSS = 0.75
CRYPTO = ["BTC-USD", "ETH-USD"]
STEM = "2026-09-04_is-window-has-no-crash_C"

# (label, IS end, OOS start).  S16 is the incumbent rule 8.
SPLITS = [("S13", "2013-12-31", "2014-01-01"),
          ("S16", "2016-12-31", "2017-01-01"),
          ("S21", "2021-12-31", "2022-01-01")]
INCUMBENT = "S16"
COMMON = "2022-01-01"          # out-of-sample for every split above


# ---------------------------------------------------------------- construction
def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def trend(px, band=0.0):
    ma = px.rolling(200).mean()
    if band <= 0:
        return (px > ma).fillna(False)
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    raw = raw.mask(px > ma * (1 + band), 1.0).mask(px < ma * (1 - band), 0.0)
    return raw.ffill().fillna(0.0) > 0.5


def eligible(px, band=0.0):
    return (vol20(px) < MAX_VOL) & trend(px, band)


def w_ranked(n=20, g=GROSS, band=0.0):
    def f(px):
        rank = composite(px).where(eligible(px, band)).rank(axis=1, ascending=False)
        return (rank <= n).astype(float) * (g / n)
    return f


def w_ewall(g=GROSS, band=0.0):
    def f(px):
        e = eligible(px, band).astype(float)
        return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * g
    return f


def w_crypto(base_fn, cap):
    """idea 15's `matched`/`same` sleeve: cap per crypto name, funded by scaling the equity
    leg down so realised gross is unchanged; crypto uses v1's own 200d+vol20 gate."""
    def f(px):
        eq_cols = [c for c in px.columns if c not in CRYPTO]
        w_eq = base_fn(px[eq_cols])
        w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
        w[w_eq.columns] = w_eq.values
        if cap <= 0:
            return w
        pxc = px[CRYPTO]
        gate = ((pxc > pxc.rolling(200).mean()) & (vol20(pxc) < MAX_VOL)).fillna(False)
        wc = gate.astype(float) * cap
        gsum = w_eq.sum(axis=1)
        keep = wc.sum(axis=1).clip(upper=gsum)
        scale = np.divide(keep, wc.sum(axis=1).replace(0, np.nan)).fillna(0.0)
        wc = wc.mul(scale, axis=0)
        eq_scale = np.divide(gsum - keep, gsum.replace(0, np.nan)).fillna(0.0)
        w[w_eq.columns] = w_eq.mul(eq_scale, axis=0).values
        w[CRYPTO] = wc[CRYPTO].values
        return w
    return f


# ---------------------------------------------------------------- metrics
def m3(r):
    d = metrics(r)
    return d["CAGR"], d["Sharpe"], d["MaxDD"]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def fail4b_window(r, spy):
    """4b's three absolute bars measured on one window."""
    c, s, dd = m3(r); sc, ss, sdd = m3(spy)
    bad = []
    if s <= ss: bad.append("Sh")
    if dd < 0.60 * sdd: bad.append("DD")
    if c < 0.70 * sc: bad.append("CAGR")
    return bad


def fail4b_full(r, spy, oos_start):
    """Full-sample 4b: both halves + the split's OOS window + DD cap + CAGR floor."""
    c, s, dd = m3(r); h1, h2 = halves(r)
    sc, ss, sdd = m3(spy); s1, s2 = halves(spy)
    o, so = metrics(r.loc[oos_start:])["Sharpe"], metrics(spy.loc[oos_start:])["Sharpe"]
    bad = []
    if h1 <= s1: bad.append("H1")
    if h2 <= s2: bad.append("H2")
    if o <= so: bad.append("OOS")
    if dd < 0.60 * sdd: bad.append("DD")
    if c < 0.70 * sc: bad.append("CAGR")
    return bad


def fail4a(r, base):
    """4a: Sharpe > RULES v1 in BOTH halves and MaxDD no worse than v1's."""
    _, _, dd = m3(r); h1, h2 = halves(r)
    _, _, bdd = m3(base); b1, b2 = halves(base)
    bad = []
    if h1 <= b1: bad.append("H1")
    if h2 <= b2: bad.append("H2")
    if dd < bdd: bad.append("DD")
    return bad


# ---------------------------------------------------------------- grids
def grids(px_c):
    G = [
        ("GROSS/top20", 0.75, {g: w_ranked(20, g) for g in [0.50, 0.60, 0.70, 0.75, 0.80, 0.90, 1.00]}, "eq"),
        ("GROSS/EWall", 0.75, {g: w_ewall(g) for g in [0.50, 0.60, 0.70, 0.75, 0.80, 0.90, 1.00]}, "eq"),
        ("BAND/ew-all", 0.00, {b: w_ewall(GROSS, b) for b in [0.00, 0.02, 0.03, 0.05, 0.08]}, "eq"),
        ("N/ranked", 20, {n: w_ranked(n) for n in [5, 10, 15, 20, 30, 40]}, "eq"),
    ]
    if px_c is not None:
        G += [
            ("CRYPTO/CAND20", 0.00, {c: w_crypto(w_ranked(20), c) for c in [0.00, 0.05, 0.10, 0.15]}, "cry"),
            ("CRYPTO/EWall", 0.00, {c: w_crypto(w_ewall(), c) for c in [0.00, 0.05, 0.10, 0.15]}, "cry"),
        ]
    return G


# ---------------------------------------------------------------- one universe
def sweep(px, px_c, tag):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    base = backtest(px, rules_v1_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]

    print("\n" + "=" * 150)
    print(f"{tag}: {px.shape[1]} tickers, eval {start.date()} -> {px.index[-1].date()}")
    sc, ss, sdd = m3(spy); s1, s2 = halves(spy)
    bc, bs, bdd = m3(base)
    print(f"  SPY   full {sc:.1%}/{ss:.3f}/{sdd:.1%}  halves {s1:.3f}/{s2:.3f}")
    print(f"  v1    full {bc:.1%}/{bs:.3f}/{bdd:.1%}  (4a reference)")
    print("\n  CRASH CONTENT OF EACH WINDOW (idea 89's premise):")
    print(f"  {'split':<6}{'IS window':<24}{'IS SPY CAGR':>12}{'IS Sh':>8}{'IS MaxDD':>10}"
          f"{'| OOS window':<26}{'OOS CAGR':>10}{'OOS Sh':>8}{'OOS MaxDD':>11}"
          f"{'  IS 4b DD bar':>15}")
    for lab, is_end, oos_start in SPLITS:
        sis, soos = spy.loc[:is_end], spy.loc[oos_start:]
        ic, isr, idd = m3(sis); oc, osr, odd = m3(soos)
        print(f"  {lab:<6}{str(spy.index[0].date()) + '..' + is_end:<24}{ic:12.1%}{isr:8.3f}{idd:10.1%}"
              f"{'| ' + oos_start + '..' + str(spy.index[-1].date()):<26}{oc:10.1%}{osr:8.3f}{odd:11.1%}"
              f"{0.60 * idd:15.1%}")
    print("=" * 150)

    rows = []
    for gname, default, arms, panel in grids(px_c):
        P = px if panel == "eq" else px_c
        sp = P["SPY"].pct_change().fillna(0).loc[start:]
        bs_ = base if panel == "eq" else backtest(
            P, rules_v1_weights(P), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
        print(f"\n[{tag}] grid {gname}   (default arm = {default})")
        hdr = (f"  {'param':>7}{'CAGR':>8}{'Sharpe':>8}{'MaxDD':>8}{'H1':>7}{'H2':>7}{'turn':>6}  "
               f"{'4a':<10}{'4b(S16)':<14}")
        for lab, _, _ in SPLITS:
            hdr += f"{lab + '_ISsh':>9}{lab + '_ISdd':>9}{lab + '_OOSsh':>10}{lab + '_OOS4b':>12}"
        print(hdr)
        for v, fn in arms.items():
            res = backtest(P, fn(P), cost_bps=COST, freq=FREQ)
            r = res["returns"].loc[start:]
            tn = res["turnover"].loc[start:].sum() / (len(r) / 252)
            c, s, dd = m3(r); h1, h2 = halves(r)
            f4a = fail4a(r, bs_)
            f4b = fail4b_full(r, sp, "2017-01-01")
            rec = dict(universe=tag, grid=gname, param=v, is_default=(v == default),
                       CAGR=c, Sharpe=s, MaxDD=dd, H1=h1, H2=h2, turn=tn,
                       pass4a=not f4a, fail4a=",".join(f4a),
                       pass4b_full=not f4b, fail4b_full=",".join(f4b))
            line = (f"  {v:>7}{c:8.1%}{s:8.3f}{dd:8.1%}{h1:7.3f}{h2:7.3f}{tn:6.1f}  "
                    f"{(','.join(f4a) or 'PASS'):<10}{(','.join(f4b) or 'PASS'):<14}")
            for lab, is_end, oos_start in SPLITS:
                r_is, r_oos = r.loc[:is_end], r.loc[oos_start:]
                ic_, is_s, idd_ = m3(r_is)
                oc_, os_s, odd_ = m3(r_oos)
                fo = fail4b_window(r_oos, sp.loc[oos_start:])
                rec.update({f"{lab}_IS_Sh": is_s, f"{lab}_IS_DD": idd_, f"{lab}_IS_CAGR": ic_,
                            f"{lab}_OOS_Sh": os_s, f"{lab}_OOS_DD": odd_, f"{lab}_OOS_CAGR": oc_,
                            f"{lab}_OOS_4b": not fo, f"{lab}_OOS_fail": ",".join(fo)})
                line += f"{is_s:9.3f}{idd_:9.1%}{os_s:10.3f}{(','.join(fo) or 'PASS'):>12}"
            # common-window score (2022+), identical for every split
            cc, cs, cdd = m3(r.loc[COMMON:])
            rec.update(C_CAGR=cc, C_Sh=cs, C_DD=cdd)
            print(line)
            rows.append(rec)
        d = pd.DataFrame([x for x in rows if x["grid"] == gname and x["universe"] == tag])
        pr = d["param"].rank()
        msg = f"  selectability: Spearman(param, IS Sharpe)"
        for lab, _, _ in SPLITS:
            spread = d[f"{lab}_IS_Sh"].max() - d[f"{lab}_IS_Sh"].min()
            ddspread = d[f"{lab}_IS_DD"].max() - d[f"{lab}_IS_DD"].min()
            msg += (f"  {lab} {pr.corr(d[f'{lab}_IS_Sh'].rank()):+.2f}"
                    f" (Sh spread {spread:.4f}, DD spread {ddspread*100:.1f}pp)")
        print(msg)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- rule 8 under each split
def rule8(df):
    print("\n" + "=" * 150)
    print("RULE 8 UNDER EACH SPLIT — argmax IS Sharpe on the IS window, evaluated untouched on that split's OOS window")
    print("=" * 150)
    out = []
    for (u, g), d in df.groupby(["universe", "grid"], sort=False):
        dflt = d[d.is_default].iloc[0]
        print(f"\n[{u}] {g}   default arm {dflt.param}   full-sample 4b passes: "
              f"{sorted(d[d.pass4b_full].param.tolist()) or 'none'}   4a passes: "
              f"{sorted(d[d.pass4a].param.tolist()) or 'none'}")
        print(f"  {'split':<6}{'pick':>8}{'IS Sh':>8}{'OOS Sh':>9}{'OOS rank':>10}{'grid best':>11}"
              f"{'regret':>9}{'vs default':>11}{'rho(IS,OOS)':>13}   {'pick OOS 4b':<14}"
              f"{'pick 2022+ Sh':>14}")
        for lab, is_end, oos_start in SPLITS:
            pick = d.loc[d[f"{lab}_IS_Sh"].idxmax()]
            oos = d[f"{lab}_OOS_Sh"]
            best = d.loc[oos.idxmax()]
            rank = int(oos.rank(ascending=False)[pick.name])
            rho = d[f"{lab}_IS_Sh"].rank().corr(oos.rank())
            dflt_oos = dflt[f"{lab}_OOS_Sh"]
            print(f"  {lab:<6}{pick.param:>8}{pick[f'{lab}_IS_Sh']:8.3f}{pick[f'{lab}_OOS_Sh']:9.3f}"
                  f"{str(rank) + '/' + str(len(d)):>10}{best.param:>11}"
                  f"{pick[f'{lab}_OOS_Sh'] - best[f'{lab}_OOS_Sh']:9.3f}"
                  f"{pick[f'{lab}_OOS_Sh'] - dflt_oos:+11.3f}{rho:13.3f}   "
                  f"{(pick[f'{lab}_OOS_fail'] or 'PASS'):<14}{pick.C_Sh:14.3f}")
            out.append(dict(universe=u, grid=g, split=lab, pick=pick.param,
                            IS_Sh=pick[f"{lab}_IS_Sh"], OOS_Sh=pick[f"{lab}_OOS_Sh"],
                            oos_rank=rank, n_arms=len(d),
                            regret=pick[f"{lab}_OOS_Sh"] - best[f"{lab}_OOS_Sh"],
                            vs_default=pick[f"{lab}_OOS_Sh"] - dflt_oos,
                            rho_is_oos=rho, pick_oos_4b=bool(pick[f"{lab}_OOS_4b"]),
                            pick_4b_full=bool(pick.pass4b_full), pick_4a=bool(pick.pass4a),
                            C_Sh=pick.C_Sh, C_CAGR=pick.C_CAGR, C_DD=pick.C_DD))
    sel = pd.DataFrame(out)
    sel.to_csv(ROOT / "research" / "backtests" / f"{STEM}.selections.csv", index=False)
    return sel


def stability(sel, df):
    print("\n" + "=" * 150)
    print("(a) DO THE PUBLISHED SELECTIONS CHANGE?  incumbent = S16 (rule 8 as written)")
    print("=" * 150)
    piv = sel.pivot_table(index=["universe", "grid"], columns="split", values="pick", aggfunc="first")
    piv = piv[[s for s, _, _ in SPLITS]]
    print(piv.to_string())
    for lab, _, _ in SPLITS:
        if lab == INCUMBENT:
            continue
        chg = (piv[lab] != piv[INCUMBENT])
        cells = [f"{u.split('.')[0]}/{g}: {piv[INCUMBENT][(u, g)]}->{piv[lab][(u, g)]}"
                 for (u, g) in piv.index[chg]]
        print(f"\n  {lab} vs {INCUMBENT}: {int(chg.sum())}/{len(piv)} selections change"
              + ("   " + " | ".join(cells) if cells else ""))
    allsame = (piv.nunique(axis=1) == 1).sum()
    print(f"\n  identical pick under all three splits: {allsame}/{len(piv)} cells")


def quality(sel):
    print("\n" + "=" * 150)
    print("(c) SELECTION QUALITY PER SPLIT (own OOS window; lower regret / lower rank number is better)")
    print("=" * 150)
    print(f"  {'split':<6}{'mean regret':>13}{'mean rank':>11}{'picks grid-best':>17}"
          f"{'beats default':>15}{'mean rho(IS,OOS)':>18}{'picks pass OOS-4b':>19}")
    for lab, _, _ in SPLITS:
        d = sel[sel.split == lab]
        print(f"  {lab:<6}{d.regret.mean():13.3f}{d.oos_rank.mean():11.2f}"
              f"{str(int((d.oos_rank == 1).sum())) + '/' + str(len(d)):>17}"
              f"{str(int((d.vs_default > 1e-9).sum())) + '/' + str(len(d)):>15}"
              f"{d.rho_is_oos.mean():18.3f}"
              f"{str(int(d.pick_oos_4b.sum())) + '/' + str(len(d)):>19}")
    print("\n" + "=" * 150)
    print(f"(d) APPLES-TO-APPLES — every split's pick re-scored on the COMMON window {COMMON}..  "
          "(out-of-sample for all three splits)")
    print("=" * 150)
    print(f"  {'split':<6}{'mean 2022+ Sharpe':>19}{'mean 2022+ CAGR':>17}{'mean 2022+ MaxDD':>18}")
    for lab, _, _ in SPLITS:
        d = sel[sel.split == lab]
        print(f"  {lab:<6}{d.C_Sh.mean():19.3f}{d.C_CAGR.mean():17.1%}{d.C_DD.mean():18.1%}")


def consequence(sel, df):
    """(e) Does a changed pick MATTER?  Every number here is already printed above; this
    block only pairs each changed cell with the common-window (2022+) score of the two
    picks, and flags cells whose grid has no selectable IS content (idea 87's 8a)."""
    print("\n" + "=" * 150)
    print("(e) MATERIAL CONSEQUENCE OF EACH CHANGED SELECTION (common window 2022+; "
          "IS Sh spread = selectability of the grid on that IS window)")
    print("=" * 150)
    inc = sel[sel.split == INCUMBENT].set_index(["universe", "grid"])
    print(f"  {'universe':<20}{'grid':<15}{'split':<6}{'S16 pick':>9}{'alt pick':>9}"
          f"{'IS Sh spread':>14}{'S16 2022+ Sh':>14}{'alt 2022+ Sh':>14}{'d 2022+ Sh':>12}   note")
    for lab, _, _ in SPLITS:
        if lab == INCUMBENT:
            continue
        for _, r in sel[sel.split == lab].iterrows():
            base = inc.loc[(r.universe, r.grid)]
            if r.pick == base.pick:
                continue
            d = df[(df.universe == r.universe) & (df.grid == r.grid)]
            spread = d[f"{lab}_IS_Sh"].max() - d[f"{lab}_IS_Sh"].min()
            note = "grid unselectable on this IS window (spread < 0.01)" if spread < 0.01 else ""
            if r.grid.startswith("CRYPTO") and lab == "S13":
                note = "IS window ends before BTC history starts -> all arms identical IS"
            print(f"  {r.universe:<20}{r.grid:<15}{lab:<6}{base.pick:9.2f}{r.pick:9.2f}"
                  f"{spread:14.4f}{base.C_Sh:14.3f}{r.C_Sh:14.3f}{r.C_Sh - base.C_Sh:+12.3f}   {note}")
    print("\n  Cells whose grid IS Sharpe spread exceeds 0.01 (i.e. rule 8 has something to "
          "select on) and whose pick still changes:")
    for lab, _, _ in SPLITS:
        if lab == INCUMBENT:
            continue
        n_chg = n_mat = 0
        for _, r in sel[sel.split == lab].iterrows():
            base = inc.loc[(r.universe, r.grid)]
            if r.pick == base.pick:
                continue
            n_chg += 1
            d = df[(df.universe == r.universe) & (df.grid == r.grid)]
            if d[f"{lab}_IS_Sh"].max() - d[f"{lab}_IS_Sh"].min() >= 0.01:
                n_mat += 1
        print(f"    {lab}: {n_mat} of {n_chg} changed cells are on a selectable grid")


def main():
    frames = []
    for tag, kw in (("universe.json", {}), ("universe_broad.json", {"broad": True})):
        px = load_universe(**kw)
        yrs = px.index.to_series().groupby(px.index.year).count()
        if yrs.loc[2015:2024].max() > 300:
            sys.exit("!! CALENDAR-DAY INDEX DETECTED (idea 38) -- aborting.")
        raw = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)
        px_c = None
        if all(c in raw.columns for c in CRYPTO):
            px_c = pd.concat([px, raw[CRYPTO].reindex(px.index).ffill()], axis=1)
        frames.append(sweep(px, px_c, tag))
    df = pd.concat(frames, ignore_index=True)
    df.to_csv(ROOT / "research" / "backtests" / f"{STEM}.grid.csv", index=False)

    sel = rule8(df)
    stability(sel, df)
    quality(sel)
    consequence(sel, df)

    print("\n" + "=" * 150)
    print("(b) PREMISE CHECK — is the IS 4b drawdown cap loose because the IS window has no crash?")
    print("=" * 150)
    print(f"  {'universe':<20}{'split':<6}{'SPY IS MaxDD':>14}{'SPY OOS MaxDD':>15}"
          f"{'IS DD bar':>11}{'arms clearing IS DD bar':>26}{'arms clearing IS CAGR floor':>29}")
    for tag, kw in (("universe.json", {}), ("universe_broad.json", {"broad": True})):
        px = load_universe(**kw)
        spy = px["SPY"].pct_change().fillna(0).loc[px.index[260]:]
        d = df[df.universe == tag]
        for lab, is_end, oos_start in SPLITS:
            _, _, idd = m3(spy.loc[:is_end])
            oc, _, odd = m3(spy.loc[oos_start:])
            ic = m3(spy.loc[:is_end])[0]
            nd = int((d[f"{lab}_IS_DD"] >= 0.60 * idd).sum())
            nc = int((d[f"{lab}_IS_CAGR"] >= 0.70 * ic).sum())
            print(f"  {tag:<20}{lab:<6}{idd:14.1%}{odd:15.1%}{0.60*idd:11.1%}"
                  f"{str(nd) + '/' + str(len(d)):>26}{str(nc) + '/' + str(len(d)):>29}")

    print("\n" + "=" * 150)
    print("SUMMARY")
    print("=" * 150)
    print(f"  grid points: {len(df)}   selections: {len(sel)} ({len(SPLITS)} splits x "
          f"{len(sel) // len(SPLITS)} universe-grid cells)   ALL reported above.")
    print(f"  full-sample 4b passes: {int(df.pass4b_full.sum())}/{len(df)} arms   "
          f"4a passes: {int(df.pass4a.sum())}/{len(df)} arms")


if __name__ == "__main__":
    main()
