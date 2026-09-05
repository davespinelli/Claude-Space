#!/usr/bin/env python3
"""QUEUE idea 91 — band-width-at-g085   (cloud sprint, 2026-09-05)

PRE-REGISTERED QUESTION (from QUEUE.md idea 91, written before any number below was read)
    Idea 84 fixed the gross dial at g = 0.85 on idea 57's 3% re-entry band but never re-opened
    the band, which had been chosen at g = 0.75.  Sweep band in {0, 2, 3, 5, 8}% at g = 0.85 on
    both large-cap universes at 10 and 25 bps: is 3% still the right width once the exposure
    dial moved, or was the band absorbing a GROSS SHORTFALL?

    The substitution hypothesis, stated so it can fail: a wider re-entry band keeps names in
    the book through shallow dips, so it RAISES mean realised gross.  If that is all the band
    does, then (i) the band-optimal width should fall as g rises, and (ii) a banded book at
    g = 0.75 should be reproducible by an UNBANDED book at whatever g matches its realised
    gross.  If instead the band survives at g = 0.85 and beats the matched-gross unbanded
    control, the band is a genuine instrument and the two dials are not substitutes.

WHAT IS RUN
    Q1  Reproduction of idea 84's published g = 0.85 / band 3% rows before anything new is read.
    Q2  The full band x gross grid, every point printed, at both cost rungs, on both universes
        and on BOTH book shapes (the equal-weight book idea 57/84 used, and the ranked top-20
        book, so the answer is not a property of one construction).
    Q3  The substitution test: mean realised gross as a function of (band, g), and the
        MATCHED-GROSS control — the unbanded book at the g that reproduces the banded book's
        own realised gross.
    Q4  PROTOCOL rule 8 walk-forward: the band is chosen on 2009-2016 alone at each g, and
        2017-2026 is read once, against a band pinned at 3%, the unbanded control, RULES v1
        and SPY.
    Q5  Both KEEP paths on every grid point.

TUNED PARAMETERS — exactly two, both swept exhaustively and reported in full
    1. band width b in {0, 2, 3, 5, 8} %     (idea 57/59's published sweep; 0 = no band, the
                                              literal 200d gate, i.e. idea 72's C72/EWall)
    2. gross g in {0.55, 0.65, 0.75, 0.85, 1.00}   (idea 66/84's ladder; g <= 1, no leverage)
    Everything else is the published construction, unchanged: eligibility = above the 200d MA
    (banded) AND vol20 < 0.60; weekly rebalance; t+1 execution; no shorting.

HARNESS
    Idea 84's script (`2026-09-04_which-4b-bar-binds_B.py`) is IMPORTED, not re-implemented, so
    this run sits on the harness that produced the number being re-opened.  Checks before any
    new number is read:
      (a) the band-parameterised weight builder reproduces idea 84's four fixed books exactly
          (band 3% -> C57/ew-band3, band 0 -> C72/EWall and C2/CAND20), 0 differing cells;
      (b) idea 84's `run` at g = 0.75, budget = inf reproduces engine.backtest to machine
          precision;
      (c) idea 84's published rows: u56 C57/ew-band3 g=0.85 @10bps = 12.8% / 1.14 / -17.1%
          (halves 1.11/1.16) and broad = 12.6% / 1.06 / -18.9% (halves 1.16/0.97).

CAVEATS carried forward, stated not buried
  - SURVIVORSHIP (idea 54 / PROTOCOL rule 9): universe.json and universe_broad.json are
    CURRENT-CONSTITUENT lists.  Delisted and acquired names are absent.  That flatters
    stay-invested settings — wide bands and high gross — i.e. it flatters the side of both
    dials this idea is testing, so a finding AGAINST the wide band is if anything understated.
  - Idea 38: both large-cap panels carry a calendar-day index (BTC-driven weekend rows).
  - Idea 126: t+1 execution only, no lag band.
  - Idea 128: the IS window's worst SPY drawdown is shallower than the OOS window's, so any
    IS-window drawdown cap admits too much; Q4's selector is affected by that and says so.
  - Q3's matched-gross control matches on MEAN realised gross.  A band and a gross dial with
    the same mean differ in the TIMING of their exposure, which is exactly what the control is
    built to isolate; it is not a claim that they are the same path.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

OUT = ROOT / "research" / "backtests"
STEM = "2026-09-05_band-width-at-g085_cloud"

_spec = importlib.util.spec_from_file_location(
    "i84", OUT / "2026-09-04_which-4b-bar-binds_B.py")
J = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(J)

FREQ, MAX_VOL, GROSS = J.FREQ, J.MAX_VOL, J.GROSS
IS_END, OOS_START = J.IS_END, J.OOS_START
NCAND = J.NCAND
BANDS = [0.0, 2.0, 3.0, 5.0, 8.0]                 # tuned parameter 1 (percent)
GLADDER = [0.55, 0.65, 0.75, 0.85, 1.00]          # tuned parameter 2
COSTS = [10.0, 25.0]
PCOST = 10.0
G84, B84 = 0.85, 3.0                              # idea 84's fixed point, the thing re-opened
BOOKS = ["ew-all", "cand20"]

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 3000)
LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ---------------------------------------------------------------- construction (band opened)
def targets_unit_b(px, book, band_pct):
    """Idea 84's `targets_unit` with the band re-opened.  Weights at gross 1; multiplying by g
       is exact for both books.  band_pct = 0 is the literal 200d gate."""
    vol = px.pct_change().rolling(20).std() * np.sqrt(252)
    elig = ((vol < MAX_VOL) & J.trend(px, band_pct / 100.0)).fillna(False)
    if book == "ew-all":
        e = elig.astype(float)
        return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    rank = J.composite(px).where(elig).rank(axis=1, ascending=False)
    return (rank <= NCAND).astype(float) / NCAND      # cash when fewer than NCAND are eligible


def rowstats(r, bars, spy):
    m, mo = metrics(r), metrics(r.loc[OOS_START:])
    mi = metrics(r.loc[:IS_END])
    h1, h2 = J.halves(r)
    i1, i2 = J.halves(r.loc[:IS_END])
    mg = J.margins(r, bars)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                IS_H1=i1, IS_H2=i2,
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                m_H1=mg["H1"], m_H2=mg["H2"], m_OOS=mg["OOS"], m_DD=mg["DD"], m_CAGR=mg["CAGR"],
                pass4b=bool(all(v > 0 for v in mg.values())))


def main():
    say("=" * 200)
    say("IDEA 91 — BAND WIDTH RE-OPENED AT g = 0.85.  Is 3% still right once the exposure dial "
        "moved, or was the band absorbing a gross shortfall?")
    say(f"    grid: band {BANDS}%  x  gross {GLADDER}  x  2 universes  x  2 books  x  "
        f"{len(COSTS)} cost rungs = {len(BANDS)*len(GLADDER)*2*2*len(COSTS)} reported points.")
    say(f"    weekly, t+1, eligibility = 200d MA (banded) AND vol20 < {MAX_VOL}.  "
        f"IS <= {IS_END} chosen on;  OOS >= {OOS_START} read once.")
    say("=" * 200)

    ROWS, REF = [], {}
    for uname, kw in (("u56", {}), ("broad", dict(broad=True))):
        px = load_universe(**kw)
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        bars = J.bars_of(spy)
        bars_is = J.bars_of(spy.loc[:IS_END], oos=False)
        ms, mso = metrics(spy), metrics(spy.loc[OOS_START:])
        v1 = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq=FREQ)
        v1_r0, v1_to = v1["returns"].loc[start:], v1["turnover"].loc[start:]
        say(f"\n{'='*200}\nUNIVERSE {uname}: {px.shape[1]} names | eval {start.date()} -> "
            f"{px.index[-1].date()}")
        say(f"  SPY  {ms['CAGR']:.2%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.2%}  halves "
            f"{bars['s1']:.3f}/{bars['s2']:.3f}  OOS {mso['CAGR']:.2%} / {mso['Sharpe']:.3f} / "
            f"{mso['MaxDD']:.2%}")
        say(f"  4b bars: Sharpe > {bars['s1']:.3f} (H1) / {bars['s2']:.3f} (H2) / "
            f"{bars['soos']:.3f} (OOS);  MaxDD <= {0.60*abs(ms['MaxDD']):.2%};  "
            f"CAGR >= {0.70*ms['CAGR']:.2%}")
        for c in COSTS:
            rv = J.net(v1_r0, v1_to, c)
            mv, mvo = metrics(rv), metrics(rv.loc[OOS_START:])
            say(f"  RULES v1 @{c:.0f}bps  {mv['CAGR']:.2%} / {mv['Sharpe']:.3f} / "
                f"{mv['MaxDD']:.2%}  halves {J.halves(rv)[0]:.3f}/{J.halves(rv)[1]:.3f}   "
                f"OOS {mvo['CAGR']:.2%} / {mvo['Sharpe']:.3f} / {mvo['MaxDD']:.2%}")
        REF[uname] = dict(spy=spy, bars=bars, bars_is=bars_is, ms=ms, mso=mso,
                          v1={c: J.net(v1_r0, v1_to, c) for c in COSTS}, start=start)

        # ---- reproduction (a): the band-parameterised builder vs idea 84's fixed books
        if True:
            chk = [("ew-all", 3.0, "C57/ew-band3"), ("ew-all", 0.0, "C72/EWall"),
                   ("cand20", 0.0, "C2/CAND20")]
            for bk, b_, name84 in chk:
                d = int((targets_unit_b(px, bk, b_) != J.targets_unit(px, name84)).sum().sum())
                say(f"  CHECK (a) {bk}@band{b_:.0f}% vs idea 84 {name84}: {d} differing cells "
                    f"-> {'PASS' if d == 0 else 'FAIL'}")
                assert d == 0

        W = {(bk, b_): targets_unit_b(px, bk, b_) for bk in BOOKS for b_ in BANDS}

        # ---- reproduction (b): engine equivalence at the published g, budget = inf
        a = J.run(px, W[("ew-all", 0.0)], g=GROSS)["r0"].loc[start:]
        e = backtest(px, W[("ew-all", 0.0)] * GROSS, cost_bps=0.0, freq=FREQ)["returns"].loc[start:]
        d = float((a - e).abs().max())
        say(f"  CHECK (b) idea 84 run vs engine.backtest (ew-all, band 0, g={GROSS}): "
            f"max|diff| = {d:.3e} -> {'PASS' if d < 1e-12 else 'FAIL'}")
        assert d < 1e-12

        for bk in BOOKS:
            for b_ in BANDS:
                for g in GLADDER:
                    res = J.run(px, W[(bk, b_)], g=g)
                    r0, to = res["r0"].loc[start:], res["to"].loc[start:]
                    gs = res["gross"].loc[start:]
                    for c in COSTS:
                        r = J.net(r0, to, c)
                        ROWS.append(dict(
                            uni=uname, book=bk, band=b_, g=g, cost=c,
                            gross_mean=float(gs.mean()),
                            gross_mean_IS=float(gs.loc[:IS_END].mean()),
                            invested=float((gs > 1e-9).mean()),
                            TO=float(to.sum() / (len(r0) / 252)),
                            pass4a=J.pass4a(r, REF[uname]["v1"][c]),
                            **rowstats(r, bars, spy)))
        say(f"  ... {uname} done ({len([x for x in ROWS if x['uni']==uname])} rows)")

    D = pd.DataFrame(ROWS)
    D.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    # ---- reproduction (c): idea 84's published g=0.85 band-3 rows
    say("\n" + "=" * 200)
    say("CHECK (c) IDEA 84's PUBLISHED ROWS (nothing new is read until these reproduce)")
    for uname, exp in (("u56", (0.128, 1.14, -0.171, 1.11, 1.16)),
                       ("broad", (0.126, 1.06, -0.189, 1.16, 0.97))):
        r = D[(D.uni == uname) & (D.book == "ew-all") & (D.band == B84) &
              (D.g == G84) & (D.cost == PCOST)].iloc[0]
        got = (r.CAGR, r.Sharpe, r.MaxDD, r.H1, r.H2)
        ok = all(abs(a - b) < 6e-3 for a, b in zip(got, exp))
        say(f"  {uname} ew-band3 g=0.85 @10bps: {r.CAGR:.1%} / {r.Sharpe:.2f} / {r.MaxDD:.1%} "
            f"halves {r.H1:.2f}/{r.H2:.2f}   published {exp[0]:.1%} / {exp[1]:.2f} / "
            f"{exp[2]:.1%} halves {exp[3]:.2f}/{exp[4]:.2f}  -> {'PASS' if ok else 'FAIL'}")
        assert ok

    # ---- Q2: the full grid
    say("\n" + "=" * 200)
    say("Q2 — THE FULL BAND x GROSS GRID.  Every point, both books, both universes, both cost "
        "rungs.  4b = all five bars on the full sample; 4a = beats RULES v1 on both Sharpe "
        "halves with no worse MaxDD.")
    cols = ["uni", "book", "cost", "g", "band", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "gross_mean", "TO", "pass4a", "pass4b"]
    for uname in ("u56", "broad"):
        for bk in BOOKS:
            for c in COSTS:
                S = D[(D.uni == uname) & (D.book == bk) & (D.cost == c)].sort_values(["g", "band"])
                say(f"\n--- {uname} / {bk} / {c:.0f} bps ---")
                say(S[cols[3:]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    say("\n  4b pass counts by (g, band), pooled over the 2 universes x 2 books x 2 cost rungs "
        "(8 cells per pair):")
    say(D.pivot_table(index="g", columns="band", values="pass4b", aggfunc="sum").to_string())
    say("\n  4a pass counts by (g, band), same 8 cells per pair:")
    say(D.pivot_table(index="g", columns="band", values="pass4a", aggfunc="sum").to_string())

    say("\n  FULL-SAMPLE Sharpe by (g, band), mean over the 8 cells:")
    say(D.pivot_table(index="g", columns="band", values="Sharpe", aggfunc="mean"
                      ).to_string(float_format=lambda x: f"{x:.3f}"))
    say("\n  the band's Sharpe RANGE within each (uni, book, cost, g) cell — how much the dial "
        "can move anything at all (idea 128's plateau statistic):")
    rng = D.groupby(["uni", "book", "cost", "g"]).agg(
        sharpe_range=("Sharpe", lambda s: s.max() - s.min()),
        best_band=("Sharpe", lambda s: np.nan),
        ).reset_index()
    bb = D.loc[D.groupby(["uni", "book", "cost", "g"]).Sharpe.idxmax(),
               ["uni", "book", "cost", "g", "band"]].rename(columns={"band": "best_band"})
    rng = rng.drop(columns=["best_band"]).merge(bb, on=["uni", "book", "cost", "g"])
    bb4 = D[D.pass4b].groupby(["uni", "book", "cost", "g"]).band.apply(
        lambda s: ",".join(f"{v:.0f}" for v in sorted(s))).rename("bands_passing_4b")
    rng = rng.merge(bb4, on=["uni", "book", "cost", "g"], how="left").fillna({"bands_passing_4b": "-"})
    say(rng.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n  DOES THE BAND-OPTIMAL WIDTH MOVE WITH g?  (the substitution hypothesis predicts "
        "the best band SHRINKS as g rises)")
    say(rng.pivot_table(index=["uni", "book", "cost"], columns="g", values="best_band"
                        ).to_string())
    sp = []
    for (u_, b_, c_), sg in rng.groupby(["uni", "book", "cost"]):
        sg = sg.sort_values("g")
        sp.append(dict(uni=u_, book=b_, cost=c_,
                       corr=(float(np.corrcoef(sg.g.rank(), sg.best_band.rank())[0, 1])
                             if sg.best_band.nunique() > 1 else np.nan)))
    SP = pd.DataFrame(sp)
    say(SP.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    v = SP["corr"].dropna()
    if len(v):
        say(f"    rank correlation between g and the Sharpe-optimal band, across the "
            f"{len(v)} cells where the best band is not constant: mean {v.mean():+.3f} "
            f"(negative = substitutes, as the hypothesis predicts)")

    # ---- Q3: the substitution test
    say("\n" + "=" * 200)
    say("Q3 — IS THE BAND A GROSS DIAL IN DISGUISE?")
    say("  (i) mean realised gross by (g, band), mean over the 8 cells.  A band that raises "
        "realised gross is, to that extent, a gross dial:")
    say(D.pivot_table(index="g", columns="band", values="gross_mean", aggfunc="mean"
                      ).to_string(float_format=lambda x: f"{x:.4f}"))
    say("\n  (ii) MATCHED-GROSS CONTROL.  For every banded point, the UNBANDED (band 0) book of "
        "the same cell is interpolated along its own g ladder to the banded point's mean "
        "realised gross.  d = banded minus matched control; positive means the band delivers "
        "something the gross dial cannot.")
    MG = []
    for (u_, bk, c_), S in D.groupby(["uni", "book", "cost"]):
        base = S[S.band == 0.0].sort_values("gross_mean")
        for _, r in S[S.band > 0].iterrows():
            if not (base.gross_mean.min() <= r.gross_mean <= base.gross_mean.max()):
                MG.append(dict(uni=u_, book=bk, cost=c_, band=r.band, g=r.g,
                               gross_mean=r.gross_mean, in_range=False))
                continue
            f = {k: float(np.interp(r.gross_mean, base.gross_mean.values, base[k].values))
                 for k in ("CAGR", "Sharpe", "MaxDD", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "TO")}
            MG.append(dict(uni=u_, book=bk, cost=c_, band=r.band, g=r.g, in_range=True,
                           gross_mean=r.gross_mean,
                           dCAGR_pp=100 * (r.CAGR - f["CAGR"]), dSharpe=r.Sharpe - f["Sharpe"],
                           dMaxDD_pp=100 * (abs(f["MaxDD"]) - abs(r.MaxDD)),
                           dOOS_Sharpe=r.OOS_Sharpe - f["OOS_Sharpe"],
                           dOOS_CAGR_pp=100 * (r.OOS_CAGR - f["OOS_CAGR"]),
                           dTO=r.TO - f["TO"]))
    MGD = pd.DataFrame(MG)
    MGD.to_csv(OUT / f"{STEM}.matched_gross.csv", index=False)
    ok = MGD[MGD.in_range]
    say(f"\n  {len(ok)} of {len(MGD)} banded points fall inside the unbanded ladder's realised "
        f"gross range and can be matched at all.")
    if len(ok):
        say(ok.groupby("band").agg(n=("g", "size"), dSharpe=("dSharpe", "mean"),
                                   dCAGR_pp=("dCAGR_pp", "mean"), dMaxDD_pp=("dMaxDD_pp", "mean"),
                                   dOOS_Sharpe=("dOOS_Sharpe", "mean"),
                                   dOOS_CAGR_pp=("dOOS_CAGR_pp", "mean"), dTO=("dTO", "mean"),
                                   Sharpe_wins=("dSharpe", lambda s: int((s > 0).sum()))
                                   ).to_string(float_format=lambda x: f"{x:.4f}"))
        say(f"\n  the band beats its matched-gross control on full-sample Sharpe in "
            f"{int((ok.dSharpe > 0).sum())}/{len(ok)} points and on OOS Sharpe in "
            f"{int((ok.dOOS_Sharpe > 0).sum())}/{len(ok)}.")
        say("\n  the same table at the point idea 91 asks about (g = 0.85):")
        say(ok[ok.g == G84].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- Q4: rule 8 walk-forward
    say("\n" + "=" * 200)
    say("Q4 — PROTOCOL RULE 8 WALK-FORWARD.  The band is chosen on 2009-2016 ALONE at each g; "
        "2017-2026 is read once.")
    say("    SEL-IS   argmax IS Sharpe over the 5 bands (no IS 4b screen)")
    say("    SEL-4b   argmax IS Sharpe over the bands whose IS window clears the IS-readable 4b "
        "bars (both Sharpe halves, DD cap, CAGR floor); abstains if none")
    say("    PIN3     the published 3% band, not chosen        CTL0  the unbanded control")
    WF = []
    for (u_, bk, c_, g), S in D.groupby(["uni", "book", "cost", "g"]):
        bi = REF[u_]["bars_is"]
        S = S.copy()
        cap_is = 0.60 * abs(bi["sdd"])
        flo_is = 0.70 * bi["scagr"]
        adm = S[(S.IS_MaxDD.abs() < cap_is) & (S.IS_CAGR > flo_is) &
                (S.IS_H1 > bi["s1"]) & (S.IS_H2 > bi["s2"])]
        picks = {"SEL-IS": S.loc[S.IS_Sharpe.idxmax()],
                 "SEL-4b": (adm.loc[adm.IS_Sharpe.idxmax()] if len(adm) else None),
                 "PIN3": S[S.band == B84].iloc[0],
                 "CTL0": S[S.band == 0.0].iloc[0]}
        mv = metrics(REF[u_]["v1"][c_].loc[OOS_START:])
        mso = REF[u_]["mso"]
        for sel, r in picks.items():
            base = dict(uni=u_, book=bk, cost=c_, g=g, sel=sel,
                        spy_OOS_Sharpe=mso["Sharpe"], spy_OOS_CAGR=mso["CAGR"],
                        spy_OOS_MaxDD=mso["MaxDD"], v1_OOS_Sharpe=mv["Sharpe"],
                        v1_OOS_CAGR=mv["CAGR"], v1_OOS_MaxDD=mv["MaxDD"])
            if r is None:
                WF.append(dict(base, band=np.nan, OOS_CAGR=np.nan, OOS_Sharpe=np.nan,
                               OOS_MaxDD=np.nan, pass4a=False, pass4b=False))
                continue
            WF.append(dict(base, band=r.band, OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe,
                           OOS_MaxDD=r.OOS_MaxDD, pass4a=bool(r.pass4a), pass4b=bool(r.pass4b)))
    WFD = pd.DataFrame(WF)
    WFD["beat_spy"] = WFD.OOS_Sharpe > WFD.spy_OOS_Sharpe
    WFD["beat_v1"] = WFD.OOS_Sharpe > WFD.v1_OOS_Sharpe
    WFD.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say("\n  bands chosen on the IS window (SEL-IS / SEL-4b), by cell and g:")
    say(WFD[WFD.sel.isin(["SEL-IS", "SEL-4b"])].pivot_table(
        index=["uni", "book", "cost"], columns=["sel", "g"], values="band").to_string())
    say("\n  OOS outcome by selector, mean over all 20 (uni, book, cost, g) cells:")
    say(WFD.groupby("sel").agg(cells=("band", lambda s: int(s.notna().sum())),
                               mean_band=("band", "mean"), OOS_CAGR=("OOS_CAGR", "mean"),
                               OOS_Sharpe=("OOS_Sharpe", "mean"), OOS_MaxDD=("OOS_MaxDD", "mean"),
                               beat_SPY=("beat_spy", "sum"), beat_v1=("beat_v1", "sum"),
                               pass4a=("pass4a", "sum"), pass4b=("pass4b", "sum")
                               ).to_string(float_format=lambda x: f"{x:.3f}"))
    say("\n  the same, restricted to g = 0.85 (idea 91's question) — 4 cells:")
    say(WFD[WFD.g == G84].groupby("sel").agg(
        cells=("band", lambda s: int(s.notna().sum())), mean_band=("band", "mean"),
        OOS_CAGR=("OOS_CAGR", "mean"), OOS_Sharpe=("OOS_Sharpe", "mean"),
        OOS_MaxDD=("OOS_MaxDD", "mean"), beat_SPY=("beat_spy", "sum"),
        beat_v1=("beat_v1", "sum"), pass4b=("pass4b", "sum")
        ).to_string(float_format=lambda x: f"{x:.3f}"))
    say("\n  per-cell OOS at g = 0.85, every selector:")
    say(WFD[WFD.g == G84].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---- Q5
    say("\n" + "=" * 200)
    say("Q5 — BOTH KEEP PATHS OVER THE WHOLE GRID")
    say(D.groupby(["band"]).agg(points=("g", "size"), pass4a=("pass4a", "sum"),
                                pass4b=("pass4b", "sum"), Sharpe=("Sharpe", "mean"),
                                CAGR=("CAGR", "mean"), MaxDD=("MaxDD", "mean"),
                                OOS_Sharpe=("OOS_Sharpe", "mean")
                                ).to_string(float_format=lambda x: f"{x:.3f}"))
    say("\n  at g = 0.85 only:")
    say(D[D.g == G84].groupby(["band"]).agg(
        points=("g", "size"), pass4a=("pass4a", "sum"), pass4b=("pass4b", "sum"),
        Sharpe=("Sharpe", "mean"), CAGR=("CAGR", "mean"), MaxDD=("MaxDD", "mean"),
        OOS_Sharpe=("OOS_Sharpe", "mean")).to_string(float_format=lambda x: f"{x:.3f}"))

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    say(f"\nwrote {STEM}.grid.csv / .matched_gross.csv / .walkforward.csv / .console.txt")


if __name__ == "__main__":
    main()
