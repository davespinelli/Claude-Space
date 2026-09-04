#!/usr/bin/env python3
"""QUEUE idea 84 — which-4b-bar-binds-decides-the-lever (lane B, 2026-09-04).

Question (pre-registered, from QUEUE)
------------------------------------
Idea 83 closed with a two-branch rule: the correct risk lever is decided by WHICH 4b bar
binds — the gross lever helps a drawdown-bound book and is strictly counterproductive on a
CAGR-bound one (32/32 gross arms failed on CAGR there), while a turnover budget is the
reverse.  The queue asks for the tabulation that rule was never built on: the binding 4b bar
for every STANDING candidate on BOTH large-cap universes, and the lever-selection rule RULES
should carry instead of quoting one instrument.

Standing candidates (constructions taken verbatim from the runs that produced them; NOT tuned)
    C2   idea 2   `CAND20`  : top-20 eligible by the v1 composite WITHOUT /sqrt(vol20),
                              equal weight at g/20, cash when E_t < 20.  (4b KEEP on u56.)
    C46  idea 46  `frac.85` : top ceil(0.85 * E_t) eligible by the same composite, equal
                              weight at g/count.  (4b on BOTH universes; the portability arm.)
    C57  idea 57  `ew-band3`: equal-weight EVERY eligible name, 200d gate replaced by a
                              +/-3% re-entry band.  (First arm to clear 4b on both lists.)
    C72  idea 72  `EWall`   : equal-weight every eligible name, literal 200d gate.  The
                              simplest 4b-passing book the project has.
Eligibility everywhere = RULES v1's gate (above the 200d MA — banded for C57 — and
vol20 < 0.60), unchanged.  Gross 0.75 and weekly rebalance are the published settings.

Tuned parameters (PROTOCOL rule 4: at most two).  Exactly two, and BOTH are levers, not fits:
    g  in {0.55, 0.65, 0.75, 0.85, 1.00}   gross exposure (idea 66's lever; <=1, no leverage)
    B  in {inf, 0.30, 0.20, 0.10}          ENTRY-ONLY per-rebalance buy budget (idea 85's
                                           instrument: every SELL executed in full, the buy
                                           leg scaled pro-rata to at most B).  Idea 83's
                                           total budget is not re-run — it is already KILLed.
The full 5 x 4 cross is run for every (universe, book) cell, so 8 cells x 20 arms = 160 arms,
each priced at 5 / 10 / 25 bps -> 480 reported points.  EVERY point is printed.
Books and universes are reported in full, never selected.

The three pre-registered predictions (written before any number below was read)
------------------------------------------------------------------------------
    P1 (idea 83's branch A)  On a DD-bound cell, lowering g raises the DD margin and can
                             convert the cell to a 4b pass.
    P2 (idea 83's branch B)  On a CAGR-bound cell, lowering g strictly lowers the CAGR
                             margin (never a fix); the correct direction is to RAISE g, and
                             the entry-only budget is the only instrument that can help.
    P3 (the branch idea 83 does not have)  Both levers are near-Sharpe-neutral (idea 66:
                             dSharpe 0.000 for gross).  So on a cell whose binding bar is a
                             SHARPE bar (H1, H2 or OOS), NO lever can help and the two-branch
                             rule is inapplicable.  Falsified if any lever moves a binding
                             Sharpe margin by more than 0.05.
The queue item is answered by which of the three branches the 8 cells actually land in.

Binding-bar convention (a REPORTING convention, fixed in advance, not a result): when a cell
fails 4b, the binding bars are the failing ones and the tightest is the most negative
normalised margin; when it passes, the binding bar is the smallest normalised slack.  The
normalisation is 0.05 Sharpe == 1pp CAGR == 1pp MaxDD.  Raw margins in natural units are
printed alongside so the convention can be discarded without losing the table.

Walk-forward (PROTOCOL rule 8) — selection rules fixed before any OOS number was read
    R0     argmax 2009-2016 Sharpe over the 20-arm lever cross; ties -> larger g, then larger B.
    RBIND  the rule under test: read the binding 4b bar from the IS window ALONE, take the
           lever branch it prescribes (DD-bound -> gross ladder; CAGR-bound -> entry budget
           and g>=0.75; Sharpe-bound -> declare no lever, fall back to the published control),
           then argmax IS Sharpe within that branch subject to the IS 4b bars.
    Both evaluated untouched on 2017-2026 against the RULES v1 baseline and SPY.  The
    head-to-head RBIND vs R0 vs the published control is what says whether the rule has
    content or is a relabelling of "pick the control".

Execution realism (PROTOCOL rule 2): weights decided at close t applied at t+1, weekly,
long-only, no leverage, costs applied to realised turnover (10 bps is the protocol point).

SURVIVORSHIP: universe.json and universe_broad.json are current-constituent lists, so every
absolute CAGR here is optimistic in one direction.  This run compares arms that share the
same panel and the same days, so the lever deltas — which are the result — are far less
exposed than the levels.  The binding-bar TABULATION is exposed: survivorship inflates CAGR
and so makes the CAGR floor easier and the Sharpe bars harder than they would have been live.

Deterministic, standalone.  Imports research/baseline.py; modifies nothing.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-04_which-4b-bar-binds_B"
FREQ, MAX_VOL, GROSS, NCAND, FRAC, BAND = "W", 0.60, 0.75, 20, 0.85, 0.03
IS_END, OOS_START = "2016-12-31", "2017-01-01"
GLADDER = [0.55, 0.65, 0.75, 0.85, 1.00]
BUDGETS = [np.inf, 0.30, 0.20, 0.10]
COSTS = [5, 10, 25]
PCOST = 10.0
BOOKS = ["C2/CAND20", "C46/frac.85", "C57/ew-band3", "C72/EWall"]
# normalisation for the binding-bar convention: 0.05 Sharpe == 1pp CAGR == 1pp MaxDD
NORM = dict(H1=0.05, H2=0.05, OOS=0.05, DD=0.01, CAGR=0.01)

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 700)


# ---------------------------------------------------------------- construction
def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def trend(px, band=0.0):
    ma = px.rolling(200).mean()
    if band <= 0:
        return (px > ma).fillna(False)
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    raw = raw.mask(px > ma * (1 + band), 1.0).mask(px < ma * (1 - band), 0.0)
    return raw.ffill().fillna(0.0) > 0.5


def targets_unit(px, book):
    """Target weight matrix at gross g=1.  Multiplying by g is exact for all four books."""
    vol = px.pct_change().rolling(20).std() * np.sqrt(252)
    band = BAND if book == "C57/ew-band3" else 0.0
    elig = ((vol < MAX_VOL) & trend(px, band)).fillna(False)
    if book in ("C57/ew-band3", "C72/EWall"):
        e = elig.astype(float)
        return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    rank = composite(px).where(elig).rank(axis=1, ascending=False)
    if book == "C2/CAND20":                       # literal: cash when E_t < NCAND
        return (rank <= NCAND).astype(float) / NCAND
    cnt = np.ceil(FRAC * elig.sum(axis=1)).clip(lower=0)   # C46 fraction book
    sel = rank.le(cnt, axis=0) & rank.notna()
    return sel.astype(float).div(cnt.replace(0, np.nan), axis=0).fillna(0.0)


# ---------------------------------------------------------------- simulation
def run(px, W1, g=GROSS, budget=np.inf):
    """One arm.  Cost-free returns + realised turnover + realised gross.

    Entry-only budget: at each rebalance every SELL is executed in full and the BUY leg is
    scaled pro-rata so its total is at most `budget`; unspent proceeds sit in cash.
    budget=inf reproduces engine.backtest exactly (asserted in the equivalence check).
    """
    rets = px.pct_change().fillna(0.0).values
    tgt_all = (W1.reindex(px.index).fillna(0.0) * g).values
    mask = rebalance_mask(px.index, FREQ).shift(1, fill_value=False).values
    n, m = rets.shape
    cur = np.zeros(m)
    held = np.zeros((n, m))
    turn = np.zeros(n)
    gross_s = np.zeros(n)
    nreb = nbind = 0
    for i in range(n):
        if mask[i] and i > 0:
            tgt = tgt_all[i - 1]
            d = tgt - cur
            new = tgt.copy()
            if np.isfinite(budget):
                e_leg = float(d[d > 0].sum())
                if e_leg > budget + 1e-12:
                    new = cur + np.where(d > 0, d * (budget / e_leg), d)
                    nbind += 1
            new = np.clip(new, 0.0, None)
            s = new.sum()
            if s > 1.0:
                new = new / s
            turn[i] = np.abs(new - cur).sum()
            cur = new
            nreb += 1
        held[i] = cur
        gross_s[i] = cur.sum()
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    return dict(r0=pd.Series((held * rets).sum(axis=1), index=px.index),
                to=pd.Series(turn, index=px.index),
                gross=pd.Series(gross_s, index=px.index),
                bind=nbind / nreb if nreb else 0.0)


def net(r0, to, bps):
    return r0 - to * bps / 1e4


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


# ---------------------------------------------------------------- 4b margins
def margins(r, bars):
    """Five 4b margins in natural units.  Positive = that bar is cleared."""
    h1, h2 = halves(r)
    m = metrics(r)
    mo = metrics(r.loc[OOS_START:])
    return dict(H1=h1 - bars["s1"], H2=h2 - bars["s2"], OOS=mo["Sharpe"] - bars["soos"],
                DD=0.60 * abs(bars["sdd"]) - abs(m["MaxDD"]),
                CAGR=m["CAGR"] - 0.70 * bars["scagr"])


def binding(mg):
    """(binding bar, its normalised margin, comma-list of failing bars)."""
    z = {k: v / NORM[k] for k, v in mg.items()}
    fails = [k for k, v in mg.items() if not v > 0]
    key = min(z, key=z.get)
    return key, z[key], (",".join(fails) if fails else "-")


def pass4a(r, base):
    h1, h2 = halves(r)
    b1, b2 = halves(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def bars_of(spy, oos=True):
    """SPY's 4b bars over whatever window `spy` covers.  oos=False for an IS-only window."""
    s1, s2 = halves(spy)
    m = metrics(spy)
    return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=metrics(spy.loc[OOS_START:])["Sharpe"] if oos else np.nan)


# ---------------------------------------------------------------- per universe
def run_universe(uname, px, out, W, arms):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    bars = bars_of(spy)
    ms, mso = metrics(spy), metrics(spy.loc[OOS_START:])
    v1 = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq=FREQ)
    v1_r0, v1_to = v1["returns"].loc[start:], v1["turnover"].loc[start:]

    print("\n" + "=" * 200)
    print(f"UNIVERSE {uname}: {px.shape[1]} names, {px.index[0].date()} -> {px.index[-1].date()}"
          f" | eval {start.date()} -> {px.index[-1].date()} | IS <= {IS_END} | OOS >= {OOS_START}")
    print(f"SPY  CAGR {ms['CAGR']:.2%}  Sharpe {ms['Sharpe']:.3f}  MaxDD {ms['MaxDD']:.2%}  "
          f"halves {bars['s1']:.3f}/{bars['s2']:.3f}  OOS Sharpe {mso['Sharpe']:.3f}")
    print(f"4b bars: Sharpe > {bars['s1']:.3f} (H1) / {bars['s2']:.3f} (H2) / {bars['soos']:.3f} (OOS), "
          f"MaxDD <= {0.60*abs(ms['MaxDD']):.2%}, CAGR >= {0.70*ms['CAGR']:.2%}")
    print("=" * 200)

    # -------- engine equivalence: budget=inf, g=0.75 must reproduce engine.backtest
    worst = 0.0
    for b in BOOKS:
        a = arms[(b, GROSS, np.inf)]["r0"].loc[start:]
        e = backtest(px, W[b] * GROSS, cost_bps=0.0, freq=FREQ)["returns"].loc[start:]
        worst = max(worst, float((a - e).abs().max()))
    print(f"ENGINE-EQUIVALENCE (budget=inf vs engine.backtest, cost-free): max|diff| = {worst:.3e} "
          f"({'EXACT' if worst < 1e-12 else 'NOT EXACT — results below are unsafe'})")

    rows = []
    for (b, g, B), res in arms.items():
        r0, to = res["r0"].loc[start:], res["to"].loc[start:]
        yrs = metrics(r0)["Years"]
        for c in COSTS:
            r = net(r0, to, c)
            m = metrics(r)
            mo = metrics(r.loc[OOS_START:])
            h1, h2 = halves(r)
            mg = margins(r, bars)
            bind, zb, fails = binding(mg)
            mg_oos = dict(H1=np.nan, H2=np.nan,
                          OOS=mo["Sharpe"] - bars["soos"],
                          DD=0.60 * abs(mso["MaxDD"]) - abs(mo["MaxDD"]),
                          CAGR=mo["CAGR"] - 0.70 * mso["CAGR"])
            rows.append(dict(
                uni=uname, book=b, g=g, B=B, cost=c,
                CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                TO=to.sum() / yrs, gross=res["gross"].loc[start:].mean(), bind_rate=res["bind"],
                m_H1=mg["H1"], m_H2=mg["H2"], m_OOS=mg["OOS"], m_DD=mg["DD"], m_CAGR=mg["CAGR"],
                binds=bind, z=zb, f4b=fails, p4b=(fails == "-"),
                p4b_oos=all(v > 0 for k, v in mg_oos.items() if not np.isnan(v)),
                p4a=pass4a(r, net(v1_r0, v1_to, c))))
    df = pd.DataFrame(rows)
    df["arm"] = df.apply(lambda r: f"g{r.g:.2f}/B{'inf' if not np.isfinite(r.B) else f'{r.B:.2f}'}", axis=1)
    out.append(df)

    print(f"\nFULL GRID {uname} — {len(df)} points, ALL reported "
          f"({len(arms)} arms x {len(COSTS)} costs)")
    cols = ["book", "arm", "cost", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR",
            "OOS_Sharpe", "OOS_MaxDD", "TO", "gross", "m_DD", "m_CAGR", "binds", "z",
            "p4a", "p4b", "p4b_oos", "f4b"]
    print(df.sort_values(["book", "cost", "g", "B"])[cols].to_string(
        index=False, float_format=lambda x: f"{x:.3f}"))

    # ---------------- PART A: the tabulation the queue asked for
    print(f"\n--- PART A  {uname}: binding 4b bar for each STANDING candidate as published "
          f"(g=0.75, B=inf, {PCOST:.0f} bps) ---")
    ctl = df[(df.g == GROSS) & (~np.isfinite(df.B)) & (df.cost == PCOST)].set_index("book")
    a = ctl[["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
             "m_H1", "m_H2", "m_OOS", "m_DD", "m_CAGR", "binds", "z", "p4b", "f4b"]]
    print(a.to_string(float_format=lambda x: f"{x:.3f}"))
    return df, ctl, bars, (v1_r0, v1_to), spy


# ---------------------------------------------------------------- lever response
def lever_table(df, uname):
    """dMargin per lever step, measured against the published control in each cell."""
    at = df[df.cost == PCOST]
    out = []
    for b in BOOKS:
        cell = at[at.book == b]
        c0 = cell[(cell.g == GROSS) & (~np.isfinite(cell.B))].iloc[0]
        for _, r in cell.iterrows():
            if r.g == GROSS and not np.isfinite(r.B):
                continue
            lev = ("gross" if not np.isfinite(r.B) else
                   ("budget" if r.g == GROSS else "both"))
            out.append(dict(uni=uname, book=b, lever=lev, arm=r.arm,
                            d_H1=r.m_H1 - c0.m_H1, d_H2=r.m_H2 - c0.m_H2,
                            d_OOS=r.m_OOS - c0.m_OOS, d_DD=r.m_DD - c0.m_DD,
                            d_CAGR=r.m_CAGR - c0.m_CAGR,
                            d_Sharpe=r.Sharpe - c0.Sharpe,
                            d_bindmargin=(r[f"m_{c0.binds}"] - c0[f"m_{c0.binds}"]),
                            ctl_binds=c0.binds, p4b=r.p4b, p4b_oos=r.p4b_oos,
                            fixed=bool(r.p4b and not c0.p4b)))
    return pd.DataFrame(out)


# ---------------------------------------------------------------- walk-forward
def walk_forward(df, uname, bars, v1, spy):
    """Rule 8.  Both selection rules were fixed before any OOS number was read."""
    v1_r0, v1_to = v1
    at = df[df.cost == PCOST].copy()
    is_bars = bars_of(spy.loc[:IS_END], oos=False)
    rows = []
    for b in BOOKS:
        cell = at[at.book == b].copy()
        ctl = cell[(cell.g == GROSS) & (~np.isfinite(cell.B))].iloc[0]
        # --- IS-only view: recompute margins on the IS window alone
        isv = []
        for _, r in cell.iterrows():
            key = (b, r.g, r.B)
            ris = ARM_RETS[(r.uni, key)].loc[:IS_END]
            m = metrics(ris)
            h1, h2 = halves(ris)
            isv.append(dict(arm=r.arm, g=r.g, B=r.B, IS_Sharpe=m["Sharpe"],
                            i_H1=h1 - is_bars["s1"], i_H2=h2 - is_bars["s2"],
                            i_DD=0.60 * abs(is_bars["sdd"]) - abs(m["MaxDD"]),
                            i_CAGR=m["CAGR"] - 0.70 * is_bars["scagr"]))
        I = pd.DataFrame(isv)
        ic = I[(I.g == GROSS) & (~np.isfinite(I.B))].iloc[0]
        zmap = {"H1": ic.i_H1 / NORM["H1"], "H2": ic.i_H2 / NORM["H2"],
                "DD": ic.i_DD / NORM["DD"], "CAGR": ic.i_CAGR / NORM["CAGR"]}
        is_bind = min(zmap, key=zmap.get)
        # R0: argmax IS Sharpe over the whole cross; ties -> larger g, then larger B
        r0 = I.sort_values(["IS_Sharpe", "g", "B"], ascending=[False, False, False]).iloc[0]
        # RBIND: branch prescribed by the IS binding bar
        if is_bind == "DD":
            branch = I[np.isinf(I.B)]                      # gross ladder only
        elif is_bind == "CAGR":
            branch = I[(I.g >= GROSS)]                     # budget instrument, g not cut
        else:
            branch = I[(I.g == GROSS) & (np.isinf(I.B))]   # Sharpe-bound: no lever exists
        ok = branch[(branch.i_DD > 0) & (branch.i_CAGR > 0) & (branch.i_H1 > 0) & (branch.i_H2 > 0)]
        pick = (ok if len(ok) else branch).sort_values(
            ["IS_Sharpe", "g", "B"], ascending=[False, False, False]).iloc[0]
        for lbl, sel in (("CTL", ic), ("R0", r0), ("RBIND", pick)):
            ret = ARM_RETS[(uname, (b, sel.g, sel.B))]
            oos = ret.loc[OOS_START:]
            m = metrics(oos)
            rows.append(dict(uni=uname, book=b, rule=lbl, arm=sel.arm, IS_bind=is_bind,
                             IS_Sharpe=sel.IS_Sharpe, OOS_CAGR=m["CAGR"],
                             OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"],
                             feasible=bool(len(ok)) if lbl == "RBIND" else np.nan))
    W = pd.DataFrame(rows)
    spy_o = metrics(spy.loc[OOS_START:])
    v1_o = metrics(net(v1_r0, v1_to, PCOST).loc[OOS_START:])
    print(f"\n--- WALK-FORWARD (rule 8) {uname}: params chosen on 2009-2016 only, "
          f"2017-2026 untouched, {PCOST:.0f} bps ---")
    print(f"  OOS references: SPY {spy_o['CAGR']:.2%}/{spy_o['Sharpe']:.3f}/{spy_o['MaxDD']:.2%}"
          f"   RULES v1 {v1_o['CAGR']:.2%}/{v1_o['Sharpe']:.3f}/{v1_o['MaxDD']:.2%}")
    print(W.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    return W


# ---------------------------------------------------------------- main
ARM_RETS = {}


def main():
    frames, ctls, wfs, levs = [], {}, [], []
    for uname, kw in (("universe.json(56)", {}), ("universe_broad.json", dict(broad=True))):
        px = load_universe(**kw)
        start = px.index[260]
        W = {b: targets_unit(px, b) for b in BOOKS}
        arms = {}
        for b in BOOKS:
            for g in GLADDER:
                for B in BUDGETS:
                    res = run(px, W[b], g=g, budget=B)
                    arms[(b, g, B)] = res
                    ARM_RETS[(uname, (b, g, B))] = net(res["r0"].loc[start:],
                                                       res["to"].loc[start:], PCOST)
        df, ctl, bars, v1, spy = run_universe(uname, px, frames, W, arms)
        ctls[uname] = ctl
        L = lever_table(df, uname)
        levs.append(L)
        print(f"\n--- PART B  {uname}: lever response vs the published control "
              f"(g=0.75/Binf, {PCOST:.0f} bps).  ALL {len(L)} arms ---")
        print(L.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
        wfs.append(walk_forward(df, uname, bars, v1, spy))

    D = pd.concat(frames, ignore_index=True)
    L = pd.concat(levs, ignore_index=True)
    W = pd.concat(wfs, ignore_index=True)
    D.to_csv(ROOT / "research" / "backtests" / f"{STEM}.grid.csv", index=False)

    print("\n" + "=" * 200)
    print("PART C — THE ANSWER: does the binding bar decide the lever?")
    print("=" * 200)

    print("\nC1. Binding bar of every standing candidate as published (8 cells, 10 bps)")
    tab = pd.concat([c.assign(uni=u)[["uni", "binds", "z", "p4b", "f4b", "Sharpe", "CAGR", "MaxDD"]]
                     for u, c in ctls.items()])
    print(tab.to_string(float_format=lambda x: f"{x:.3f}"))
    cnt = tab.binds.value_counts()
    print("  binding-bar census:", dict(cnt))

    print("\nC2. P1/P2/P3 — the biggest move each lever family makes in the BINDING margin")
    for (u, b), grp in L.groupby(["uni", "book"], sort=False):
        cb = grp.ctl_binds.iloc[0]
        for fam in ("gross", "budget", "both"):
            g = grp[grp.lever == fam]
            if not len(g):
                continue
            best = g.loc[g.d_bindmargin.idxmax()]
            print(f"  {u:22s} {b:14s} binds={cb:5s} {fam:7s} best d(bind margin)="
                  f"{best.d_bindmargin:+.4f} at {best.arm:12s}  dSharpe {best.d_Sharpe:+.3f}"
                  f"  4b {'PASS' if best.p4b else 'fail'}"
                  f"{'  <-- CONVERTS' if best.fixed else ''}")

    print("\nC3. P3 test — can any lever move a binding SHARPE margin by more than 0.05?")
    sb = L[L.ctl_binds.isin(["H1", "H2", "OOS"])]
    if len(sb):
        print(f"  {len(sb)} arms across {sb.groupby(['uni','book']).ngroups} Sharpe-bound cells;"
              f" max |d(bind margin)| = {sb.d_bindmargin.abs().max():.4f}"
              f" (arm {sb.loc[sb.d_bindmargin.abs().idxmax()].arm} on "
              f"{sb.loc[sb.d_bindmargin.abs().idxmax()].book})")
        print(f"  P3 {'HOLDS' if sb.d_bindmargin.abs().max() <= 0.05 else 'FALSIFIED'}"
              f"; arms converting a Sharpe-bound cell to 4b: {int(sb.fixed.sum())}")
    else:
        print("  no Sharpe-bound cell in the 8 — P3 untested this run")

    print("\nC4. P2 test — on CAGR-bound cells, does lowering g ever help?")
    cb = L[(L.ctl_binds == "CAGR") & (L.lever == "gross")]
    if len(cb):
        dn = cb[cb.arm.str.startswith(("g0.55", "g0.65"))]
        print(f"  cut-gross arms on CAGR-bound cells: {len(dn)}, all with d_CAGR<0: "
              f"{bool((dn.d_CAGR < 0).all())}; best d(bind margin) among them "
              f"{dn.d_bindmargin.max():+.4f}")
        up = cb[cb.arm.str.startswith(("g0.85", "g1.00"))]
        print(f"  raise-gross arms: {len(up)}, converting to 4b: {int(up.fixed.sum())}, "
              f"best d(bind margin) {up.d_bindmargin.max():+.4f}")
    else:
        print("  no CAGR-bound cell — P2 untested this run")

    print("\nC5. Cross-universe 4b (the bar that matters): arms passing 4b on BOTH universes")
    p = D[(D.cost == PCOST)].pivot_table(index=["book", "arm"], columns="uni",
                                         values="p4b", aggfunc="first")
    p["both"] = p.all(axis=1)
    print(p.to_string())
    print(f"  arms passing 4b on both universes: {int(p['both'].sum())} of {len(p)}")

    print("\nC6. Cost sensitivity of the census (does the binding bar move with cost?)")
    cc = D[(D.g == GROSS) & (~np.isfinite(D.B))].pivot_table(
        index=["uni", "book"], columns="cost", values="binds", aggfunc="first")
    print(cc.to_string())

    print("\nC7. Walk-forward head-to-head, both universes")
    print(W.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    piv = W.pivot_table(index=["uni", "book"], columns="rule", values="OOS_Sharpe")
    piv["RBIND-CTL"] = piv["RBIND"] - piv["CTL"]
    piv["R0-CTL"] = piv["R0"] - piv["CTL"]
    print(piv.to_string(float_format=lambda x: f"{x:.3f}"))
    print(f"  mean OOS Sharpe: CTL {piv['CTL'].mean():.3f}  R0 {piv['R0'].mean():.3f}  "
          f"RBIND {piv['RBIND'].mean():.3f}")

    print("\n" + "=" * 200)
    print("PART D — the replacement clause, measured: 4b's CAGR floor and DD cap are BOTH on")
    print("the gross axis, so together they define an INTERVAL [g_min, g_max] per cell.  A book")
    print("passes 4b iff that interval is non-empty AND its Sharpe bars pass (which g cannot move).")
    print("Fine ladder g = 0.40..1.00 step 0.05 at B=inf, every point priced at 5/10/25 bps.")
    print("=" * 200)
    fine = np.round(np.arange(0.40, 1.001, 0.05), 2)
    drows = []
    for uname, kw in (("universe.json(56)", {}), ("universe_broad.json", dict(broad=True))):
        px = load_universe(**kw)
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        bars = bars_of(spy)
        for b in BOOKS:
            W1 = targets_unit(px, b)
            for g in fine:
                res = run(px, W1, g=g)
                r0, to = res["r0"].loc[start:], res["to"].loc[start:]
                for c in COSTS:
                    r = net(r0, to, c)
                    mg = margins(r, bars)
                    drows.append(dict(uni=uname, book=b, g=g, cost=c,
                                      CAGR=metrics(r)["CAGR"], MaxDD=metrics(r)["MaxDD"],
                                      Sharpe=metrics(r)["Sharpe"], **{f"m_{k}": v for k, v in mg.items()},
                                      shp_ok=(mg["H1"] > 0 and mg["H2"] > 0 and mg["OOS"] > 0),
                                      p4b=all(v > 0 for v in mg.values())))
    F = pd.DataFrame(drows)
    F.to_csv(ROOT / "research" / "backtests" / f"{STEM}.gladder.csv", index=False)
    print(f"\nFine gross ladder — {len(F)} points, ALL reported")
    print(F.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print("\nD1. The gross interval implied by 4b, per cell and cost")
    for (u, b, c), grp in F.groupby(["uni", "book", "cost"], sort=False):
        ok = grp[grp.m_CAGR > 0]
        lo = ok.g.min() if len(ok) else np.nan
        ok2 = grp[grp.m_DD > 0]
        hi = ok2.g.max() if len(ok2) else np.nan
        s = grp.shp_ok.iloc[0]
        w = "empty" if not (np.isfinite(lo) and np.isfinite(hi) and lo <= hi) else f"[{lo:.2f},{hi:.2f}]"
        print(f"  {u:22s} {b:14s} {c:2.0f}bps  g_min(CAGR floor)={lo if np.isfinite(lo) else float('nan'):.2f}"
              f"  g_max(DD cap)={hi if np.isfinite(hi) else float('nan'):.2f}  interval {w:12s}"
              f"  Sharpe bars {'PASS' if s else 'FAIL (no g helps)'}"
              f"  -> 4b {'reachable' if (w != 'empty' and s) else 'UNREACHABLE by any g'}")
    print("\nLEADERBOARD rows are in the .result.md written by hand from this console.")


if __name__ == "__main__":
    main()
