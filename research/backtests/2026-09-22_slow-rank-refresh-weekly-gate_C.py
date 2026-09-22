#!/usr/bin/env python3
"""QUEUE idea 2250 (lane C, 2026-09-22) — does-a-SLOWER-RANK-REFRESH-at-an-UNCHANGED-WEEKLY-
BAND-GATE-keep-the-BOTH-PATHS-PASS.

THE QUESTION, VERBATIM FROM THE QUEUE
    "idea 1767 found the VOLTGT candidate's monthly blowout was SIGNAL STALENESS, not rebalance
     count, and 1625 already separates 'the gate must be read at least weekly' from 'the
     equal-weight re-spread may run on any cadence'.  Split the both-paths cell's TWO schedules —
     refresh the top-20 ranking monthly or quarterly while the band3 gate and the de-risking stay
     weekly — and ask whether the 4a+4b pass survives the cost ladder it currently dies on at
     25 bps."

WHY IT MATTERS
    The 2026-09-20 Sunday review re-verified the record's ONLY 4a+4b book (`u56 / S3-50 +
    band3-rw @10 bps`, 11.26% / 1.2632 / -11.63%, OOS Sharpe 1.2881) and REFUSED to promote it
    for exactly one reason: it trades 8.18x/yr against the live book's 1.77x, so 6 of its 24
    cost x latency cells clear the bar and all six are at 5 or 10 bps.  Turnover is the whole
    disqualification.  This run attacks it at the source the queue names: the top-20 composite
    ranking is re-read every week, and a ranking that churns is the cheapest thing to slow down,
    because slowing a SELECTION adds no signal and removes trades directly.

CONSTRUCTION (nothing re-implemented; both parent scripts are IMPORTED)
    Book = idea 133's `S3-50` under idea 94's `band3` gate in the RE-WEIGHT convention, weekly
    trading, gross 0.75 — the committed cell, frozen at n = 20, f = 0.50, band 3%, gross 0.75.
    The ONE thing this run changes is WHEN the composite rank picks the 20 names:

        on a REFRESH date  : take the top-20 composite among the names the band gate allows TODAY
        between refreshes  : hold that name set; the band gate is still read EVERY WEEK, so a held
                             name that leaves the band is dropped at the weekly step and the book
                             re-spreads to gross 0.75 over the survivors (the `rw` convention)
        the TLT/GLD/UUP sleeve re-solves WEEKLY throughout, exactly as committed.

TUNED PARAMETERS — exactly two, every grid point published
    R         rank-refresh cadence in {W, 2W, M, Q}      (W = the committed cell, bit-for-bit)
    BACKFILL  in {False, True} — whether a slot vacated by the gate between refreshes is refilled
              from TODAY's composite rank (True) or simply left empty until the next refresh
              (False).  The two bracket the honest readings of "slower refresh": slower SELECTION
              versus slower REPLACEMENT.  BACKFILL is a no-op at R = W by construction (gate G3).
    REPORTED AXES, never selected on: panel {u56, broad}, cost {5, 10, 25, 50} bps, both KEEP
    paths, turnover, and the rule-8 walk-forward.  Execution is t+1 throughout (the committed
    convention); latency was already shown non-binding for this cell by the Sunday review.

KEEP PATHS (PROTOCOL 4, scored exactly as the Sunday review scored the same cell)
    4a  Sharpe > the LIVE book (RULES v2) in BOTH halves and MaxDD no worse, at the SAME cost.
    4b  Sharpe > SPY in both halves AND out of sample, MaxDD <= 60% of SPY's, CAGR >= 70% of
        SPY's.  The Sunday PROMOTION bar additionally requires beating the live book OOS.

RULE 8 (walk-forward, required)
    (R, BACKFILL) chosen on 2009-2016 ONLY by three pre-declared choosers, then read ONCE on
    2017-2026 against RULES v2 OOS and SPY OOS:
        S0    argmax IS Sharpe over all 8 books.
        S1    argmax IS Sharpe among books whose IS WINDOW alone clears 4b's halves bars, its DD
              cap (0.60) and its CAGR floor (0.70) against SPY's IS window.
        S2    argmax IS Sharpe among books whose IS turnover is <= 4.0x/yr — the cost-aware
              chooser this idea exists to test.
        DEF   the zero-parameter control: ship the committed cell (R = W).  Not a chooser.

GATES (printed before any hypothesis is read)
    G1  H.run == engine.backtest on the live book (the committed simulator identity).
    G2  the (R = W, BACKFILL = False) frame == D.book_weights(px,'S3-50','band3','rw'), 0.0.
    G3  BACKFILL is a no-op at R = W: frame diff 0.0.
    G4  every one of the 2 x 4 x 4 x 2 = 64 cells is published, pass or fail.

CAVEATS carried, not buried
    * SURVIVORSHIP (PROTOCOL rule 9 / idea 54): u56 and broad are CURRENT-constituent lists, so
      every CAGR level is optimistic and both 4b bars are easier than on a point-in-time panel.
      The cadence CONTRAST is within-tape (same names, same dates, only the refresh schedule
      moves) and is first-order immune; the PASS COUNTS are not.
    * The cost model is a flat bps-on-turnover bill; a slower book that trades the same notional
      at worse prices would be invisible here.  That is the record's own cost convention.
    * A 4b pass on this panel is not a capital decision by itself; the Sunday review's bar is.

Deterministic, standalone.  Writes .grid.csv, .walkforward.csv and .console.txt next to itself.
Modifies nothing.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-22_slow-rank-refresh-weekly-gate_C"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I133 = OUT / "2026-09-05_is-the-defensive-class-one-book_cloud.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")
D = _load(I133, "i133")

FREQ, GROSS, OOS_START, IS_END = H.FREQ, H.GROSS, H.OOS_START, H.IS_END
PANELS = ["u56", "broad"]
COSTS = [5.0, 10.0, 25.0, 50.0]
REFRESH = ["W", "2W", "M", "Q"]
BACKFILL = [False, True]
NTOP, FBLEND, S3 = 20, 0.50, ["TLT", "GLD", "UUP"]
PHI0, DELTA0 = 0.70, 0.60          # 4b CAGR floor and MaxDD cap multipliers
TO_BAR = 4.0                       # S2's IS turnover ceiling, x/yr, declared before any read

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)
_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


# ------------------------------------------------------------------ the device ----
def refresh_dates(idx, R):
    """Boolean over idx: True on a rank-refresh date.  W/M/Q are the engine's own period-end
    masks; 2W is every SECOND weekly date, anchored on the first."""
    if R in ("W", "M", "Q"):
        return rebalance_mask(idx, R).values.astype(bool)
    if R == "2W":
        w = rebalance_mask(idx, "W").values.astype(bool)
        out = np.zeros(len(idx), dtype=bool)
        out[np.where(w)[0][::2]] = True
        return out
    raise ValueError(R)


def ranked_slow(px, gm, R, backfill, n=NTOP):
    """Top-n composite among gate-allowed names, re-SELECTED only on refresh dates and held in
    between, with the gate still read every row.  R='W' reproduces idea 133's `ranked(px, n,
    'band3', 'rw')` exactly, because the harness only reads the frame on weekly dates."""
    s = H.composite(px).where(gm)                       # rw convention: rank among allowed names
    rk = s.rank(axis=1, ascending=False)
    fresh = (rk <= n).values                            # today's top-n among allowed names
    rd = refresh_dates(px.index, R)
    sel = np.where(rd[:, None], fresh.astype(float), np.nan)
    sel = pd.DataFrame(sel, index=px.index, columns=px.columns).ffill().fillna(0.0).values > 0.5
    gmv = gm.values
    eff = sel & gmv                                     # the weekly gate still bites
    if backfill:
        # Refill ONLY the slots the gate vacated since the last refresh, back up to the size of
        # the set that refresh selected (never up to n).  Capping at the held-set size rather
        # than at n is what makes backfill exactly inert at R = W (gate G3): there the held set
        # is today's selection and the gate has vacated nothing.
        rkv = rk.values.astype(float)
        big = (np.nanmax(rkv[np.isfinite(rkv)]) + 1.0) if np.isfinite(rkv).any() else 1.0
        pri = np.where(np.isfinite(rkv), rkv, np.inf)   # gated-out names are never eligible
        pri = np.where(eff, pri - 2.0 * big, pri)       # already-held names keep their slots
        ord_ = pd.DataFrame(pri, index=px.index, columns=px.columns).rank(axis=1, method="first")
        k = sel.sum(axis=1)[:, None]                    # the last refresh's book size
        eff = (ord_.values <= k) & np.isfinite(pri)
    return pd.DataFrame(np.where(eff, GROSS / n, 0.0), index=px.index, columns=px.columns)


def cand_weights(px, R, backfill):
    """The committed both-paths cell with ONE thing changed: the rank-refresh schedule."""
    gm = H.gate_mask(px, "band3")
    w = (1 - FBLEND) * ranked_slow(px, gm, R, backfill) \
        + FBLEND * D.sleeve_weights(px, S3).where(gm, 0.0)
    return w.mul((GROSS / w.sum(axis=1).replace(0, np.nan)).fillna(0.0), axis=0).fillna(0.0)


# ------------------------------------------------------------------ scoring ----
def bars_win(spy, which):
    s = spy if which == "full" else spy.loc[:IS_END]
    s1, s2 = H.halves(s)
    m = metrics(s)
    return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=metrics(spy.loc[OOS_START:])["Sharpe"])


def legs4b(r, bars, oos=True):
    h1, h2 = H.halves(r)
    m = metrics(r)
    f = []
    if not h1 > bars["s1"]:
        f.append("H1")
    if not h2 > bars["s2"]:
        f.append("H2")
    if oos and not metrics(r.loc[OOS_START:])["Sharpe"] > bars["soos"]:
        f.append("OOS")
    if not abs(m["MaxDD"]) <= DELTA0 * abs(bars["sdd"]):
        f.append("DD")
    if not m["CAGR"] >= PHI0 * bars["scagr"]:
        f.append("CAGR")
    return f


def main():
    say(f"IDEA 2250 — {STEM}")
    say("slower RANK REFRESH at an unchanged WEEKLY band gate, on the record's only 4a+4b cell\n")
    rows, wf = [], []

    for pk in PANELS:
        px, spy_full = D.panel_px(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        bars, bIS = bars_win(spy, "full"), bars_win(spy, "IS")
        ms, mso = metrics(spy), metrics(spy.loc[OOS_START:])
        say(f"[panel] {pk}: {px.shape[1]} cols, {px.index[0].date()}..{px.index[-1].date()}, "
            f"eval from {start.date()}")
        say(f"    SPY  {ms['CAGR']:.2%} / {ms['Sharpe']:.4f} / {ms['MaxDD']:.2%}  halves "
            f"{bars['s1']:.4f}/{bars['s2']:.4f}  OOS {mso['CAGR']:.2%} / {mso['Sharpe']:.4f} / "
            f"{mso['MaxDD']:.2%}")
        say(f"    4b bars: CAGR >= {PHI0 * bars['scagr']:.2%}, MaxDD <= "
            f"{-DELTA0 * abs(bars['sdd']):.2%}, halves {bars['s1']:.4f}/{bars['s2']:.4f}, "
            f"OOS Sharpe {bars['soos']:.4f}")

        Wv2 = rules_v2_weights(px)
        g1 = float((H.run(px, Wv2, bps=10.0)["r"].loc[start:]
                    - backtest(px, Wv2, cost_bps=10.0, freq=FREQ)["returns"].loc[start:])
                   .abs().max())
        say(f"[G1] harness vs engine.backtest on RULES v2 @10bps: max|diff| {g1:.3e} "
            f"({'EXACT' if g1 < 1e-12 else 'NOT EXACT — unsafe'})")
        Wref = D.book_weights(px, "S3-50", "band3", "rw")
        Ww0, Ww1 = cand_weights(px, "W", False), cand_weights(px, "W", True)
        read = pd.Series(rebalance_mask(px.index, FREQ).values, index=px.index)   # rows H.run reads
        g2f = float((Ww0[read.values] - Wref[read.values]).abs().max().max())
        g2r = float((H.run(px, Ww0, bps=10.0)["r"] - H.run(px, Wref, bps=10.0)["r"]).abs().max())
        g3f = float((Ww1[read.values] - Ww0[read.values]).abs().max().max())
        say(f"[G2] (R=W, backfill=False) vs the committed cell — frame on the rows the simulator "
            f"reads: max|diff| {g2f:.3e}; NET RETURNS: max|diff| {g2r:.3e} "
            f"({'EXACT' if max(g2f, g2r) < 1e-12 else 'NOT EXACT — unsafe'})")
        say("     (off-schedule rows differ by construction: the slowed frame is held between "
            "refresh dates and the committed frame is re-read daily; the simulator never reads them)")
        say(f"[G3] backfill is a no-op at R=W on the read rows: max|diff| {g3f:.3e}")

        base_r = {c: H.run(px, Wv2, bps=c)["r"].loc[start:] for c in COSTS}
        for R in REFRESH:
            for bf in BACKFILL:
                W = cand_weights(px, R, bf)
                for c in COSTS:
                    res = H.run(px, W, bps=c)
                    r = res["r"].loc[start:]
                    b = base_r[c]
                    m, mo = metrics(r), metrics(r.loc[OOS_START:])
                    mb, mbo = metrics(b), metrics(b.loc[OOS_START:])
                    h1, h2 = H.halves(r)
                    b1, b2 = H.halves(b)
                    rIS = r.loc[:IS_END]
                    mIS = metrics(rIS)
                    toIS = res["to"].loc[start:IS_END].sum() / mIS["Years"]
                    f4b = legs4b(r, bars)
                    rows.append(dict(
                        panel=pk, refresh=R, backfill=bf, cost=c,
                        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                        TO=res["to"].loc[start:].sum() / m["Years"],
                        IS_Sharpe=mIS["Sharpe"], IS_CAGR=mIS["CAGR"], IS_MaxDD=mIS["MaxDD"],
                        IS_TO=toIS, IS_fail4b=",".join(legs4b(rIS, bIS, oos=False)) or "-",
                        v2_CAGR=mb["CAGR"], v2_Sharpe=mb["Sharpe"], v2_MaxDD=mb["MaxDD"],
                        v2_H1=b1, v2_H2=b2, v2_OOS_CAGR=mbo["CAGR"],
                        v2_OOS_Sharpe=mbo["Sharpe"], v2_OOS_MaxDD=mbo["MaxDD"],
                        pass4a=bool(h1 > b1 and h2 > b2 and m["MaxDD"] >= mb["MaxDD"]),
                        beats_v2_oos=bool(mo["Sharpe"] > mbo["Sharpe"]),
                        pass4b=(len(f4b) == 0), fail4b=",".join(f4b) or "-",
                        spy_CAGR=ms["CAGR"], spy_Sharpe=ms["Sharpe"], spy_MaxDD=ms["MaxDD"],
                        spy_OOS_CAGR=mso["CAGR"], spy_OOS_Sharpe=mso["Sharpe"],
                        spy_OOS_MaxDD=mso["MaxDD"]))
        say("")

    df = pd.DataFrame(rows)
    df.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"[G4] cells published: {len(df)} of {len(PANELS) * len(REFRESH) * len(BACKFILL) * len(COSTS)}\n")

    cols = ["panel", "refresh", "backfill", "cost", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
            "OOS_Sharpe", "TO", "v2_Sharpe", "v2_OOS_Sharpe", "pass4a", "beats_v2_oos",
            "pass4b", "fail4b"]
    say("ALL 64 CELLS  (promotion bar = pass4a AND beats_v2_oos AND pass4b)")
    say(df[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n--- TURNOVER, the whole reason this idea exists (x/yr, full sample) ---")
    piv = df[df.cost == 10.0].pivot_table(index=["panel", "backfill"], columns="refresh",
                                          values="TO")[REFRESH]
    say(piv.to_string(float_format=lambda x: f"{x:.2f}"))
    say(f"  live book RULES v2 turnover for reference: "
        f"{', '.join(f'{p} n/a' for p in [])}1.77x/yr (2026-09-20 Sunday review)")

    say("\n--- KEEP PATHS by refresh rung and cost rung ---")
    for pk in PANELS:
        for c in COSTS:
            sub = df[(df.panel == pk) & (df.cost == c)]
            say(f"  {pk} @{c:.0f}bps : 4a {int(sub.pass4a.sum())}/8, beats-v2-OOS "
                f"{int(sub.beats_v2_oos.sum())}/8, 4b {int(sub.pass4b.sum())}/8, promotion bar "
                f"{int((sub.pass4a & sub.beats_v2_oos & sub.pass4b).sum())}/8")
    promo = df[df.pass4a & df.beats_v2_oos & df.pass4b]
    say(f"\n[PROMOTION BAR] {len(promo)} of {len(df)} cells clear it")
    if len(promo):
        say(promo[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"  by refresh rung: {dict(promo.refresh.value_counts()) if len(promo) else {}}")
    say(f"  by cost rung:    {dict(promo.cost.value_counts()) if len(promo) else {}}")
    say(f"  the committed cell (R=W) at 25/50 bps: "
        f"{int(df[(df.refresh == 'W') & (df.cost >= 25)].pass4b.sum())}/8 on 4b, "
        f"{int((df[(df.refresh == 'W') & (df.cost >= 25)].pass4a & df[(df.refresh == 'W') & (df.cost >= 25)].beats_v2_oos & df[(df.refresh == 'W') & (df.cost >= 25)].pass4b).sum())}/8 on the bar")
    say(f"  any SLOWED rung (R != W) at 25/50 bps: "
        f"{int(df[(df.refresh != 'W') & (df.cost >= 25)].pass4b.sum())}/24 on 4b, "
        f"{int((df[(df.refresh != 'W') & (df.cost >= 25)].pass4a & df[(df.refresh != 'W') & (df.cost >= 25)].beats_v2_oos & df[(df.refresh != 'W') & (df.cost >= 25)].pass4b).sum())}/24 on the bar")

    # ------------------------------------------------------------ rule 8 ----
    say("\n--- RULE 8 WALK-FORWARD: (R, backfill) chosen on 2009-2016 only, read ONCE on 2017-2026 ---")
    for pk in PANELS:
        for c in COSTS:
            sub = df[(df.panel == pk) & (df.cost == c)].copy()
            picks = {}
            picks["S0"] = sub.loc[sub.IS_Sharpe.idxmax()]
            s1 = sub[sub.IS_fail4b == "-"]
            picks["S1"] = s1.loc[s1.IS_Sharpe.idxmax()] if len(s1) else None
            s2 = sub[sub.IS_TO <= TO_BAR]
            picks["S2"] = s2.loc[s2.IS_Sharpe.idxmax()] if len(s2) else None
            picks["DEF"] = sub[(sub.refresh == "W") & (~sub.backfill)].iloc[0]
            for nm, p in picks.items():
                if p is None:
                    say(f"  {pk} @{c:.0f}bps {nm:4s}: ABSTAINS (no IS-legal book)")
                    wf.append(dict(panel=pk, cost=c, chooser=nm, pick="ABSTAIN"))
                    continue
                say(f"  {pk} @{c:.0f}bps {nm:4s}: pick R={p.refresh}/bf={p.backfill}  "
                    f"OOS {p.OOS_CAGR:.2%} / {p.OOS_Sharpe:.4f} / {p.OOS_MaxDD:.2%}  "
                    f"| v2 OOS {p.v2_OOS_CAGR:.2%} / {p.v2_OOS_Sharpe:.4f} / {p.v2_OOS_MaxDD:.2%}  "
                    f"| SPY OOS {p.spy_OOS_CAGR:.2%} / {p.spy_OOS_Sharpe:.4f} / {p.spy_OOS_MaxDD:.2%}"
                    f"  | TO {p.TO:.2f}x  4b {'PASS' if p.pass4b else 'FAIL(' + p.fail4b + ')'}"
                    f"  bar {'PASS' if (p.pass4a and p.beats_v2_oos and p.pass4b) else 'FAIL'}")
                wf.append(dict(panel=pk, cost=c, chooser=nm,
                               pick=f"R={p.refresh}/bf={p.backfill}", refresh=p.refresh,
                               backfill=bool(p.backfill), OOS_CAGR=p.OOS_CAGR,
                               OOS_Sharpe=p.OOS_Sharpe, OOS_MaxDD=p.OOS_MaxDD, TO=p.TO,
                               v2_OOS_CAGR=p.v2_OOS_CAGR, v2_OOS_Sharpe=p.v2_OOS_Sharpe,
                               v2_OOS_MaxDD=p.v2_OOS_MaxDD, spy_OOS_CAGR=p.spy_OOS_CAGR,
                               spy_OOS_Sharpe=p.spy_OOS_Sharpe, spy_OOS_MaxDD=p.spy_OOS_MaxDD,
                               pass4a=bool(p.pass4a), beats_v2_oos=bool(p.beats_v2_oos),
                               pass4b=bool(p.pass4b),
                               bar=bool(p.pass4a and p.beats_v2_oos and p.pass4b)))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    real = W[W.pick != "ABSTAIN"]
    say(f"\n  choosers that DEVIATE from the shipped R=W default: "
        f"{int((real.refresh != 'W').sum())} of {len(real[real.chooser != 'DEF'])} non-DEF picks")
    for nm in ("S0", "S1", "S2"):
        a = real[real.chooser == nm]
        d = real[real.chooser == "DEF"].set_index(["panel", "cost"])
        if not len(a):
            continue
        j = a.set_index(["panel", "cost"]).join(d[["OOS_Sharpe"]], rsuffix="_def")
        say(f"  {nm}: mean OOS Sharpe {a.OOS_Sharpe.mean():.4f} vs DEF {d.OOS_Sharpe.mean():.4f} "
            f"(delta {j.OOS_Sharpe.mean() - j.OOS_Sharpe_def.mean():+.4f}); beats DEF in "
            f"{int((j.OOS_Sharpe > j.OOS_Sharpe_def).sum())} of {len(j)} cells; "
            f"promotion bar {int(a.bar.sum())}/{len(a)}")
    say(f"  DEF promotion bar {int(real[real.chooser == 'DEF'].bar.sum())}/"
        f"{len(real[real.chooser == 'DEF'])}")

    say("\nCAVEAT (PROTOCOL rule 9 / idea 54): u56 and broad are CURRENT-constituent panels, so "
        "every CAGR level is optimistic and both 4b bars are easier than on a point-in-time "
        "panel.  The cadence contrast is within-tape; the pass counts are not.")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
