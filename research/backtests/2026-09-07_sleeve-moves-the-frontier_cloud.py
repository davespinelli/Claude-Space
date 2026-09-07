#!/usr/bin/env python3
"""QUEUE idea 139 — sleeve-moves-the-frontier  (cloud, 2026-09-07)

QUESTION (pre-registered, from QUEUE.md idea 139, verbatim)
    "idea 134's ladder control found that on broad@10bps NO gross level puts the ranked book
     inside 4b (floor at m=0.60, DD cap at m=0.80-1.40, Sharpe flat 0.973-0.978) while a sleeve
     at f>=0.10 does.  That makes the sleeve the first instrument the project has that is not a
     point on the gross ladder.  Price it on idea 74's single axis (pp of CAGR surrendered per
     pp of MaxDD bought) against the 200d gate, the 3% band and de-grossing, at matched starting
     book and cost."

IDEA 74's AXIS (the one number this run is about), as idea 94 implements it
        rate = (CAGR_control - CAGR_arm) / (|MaxDD_control| - |MaxDD_arm|)   pp CAGR per pp MaxDD
    measured on the SAME base book, the SAME days, the SAME cost.  Lower = cheaper insurance.
    The reference price is the static gross lever (hold m x the book, no rule at all), which
    idea 66 showed is an exact, parameter-free, path-independent dial with no Sharpe content.
    Two derived tests, both reported for every arm:
        lever        = rate / the base book's own ladder slope   (<1 = cheaper than de-grossing)
        vs_matchedDD = arm CAGR - the ladder's CAGR interpolated to the ARM's OWN MaxDD
                       (>0 = at this drawdown the arm beats simply holding less; this is the
                        decisive "is it a point on the ladder" test, and it is the one the
                        queue's claim is really about)

TWO FALSIFIABLE HYPOTHESES, written down before any number of this run was read
    H_offladder (the queue's claim) — the sleeve is NOT a point on the gross ladder: it prices
        BELOW the ladder slope (lever < 1) and beats its own matched-drawdown ladder point
        (vs_matchedDD > 0) in the majority of cells, where idea 94 found every other instrument
        prices ABOVE the ladder.  Prediction: sleeve dominated-rate << gate/band dominated-rate,
        and it survives rule 8 (the IS-cheapest instrument is a sleeve and it stays cheap OOS).
    H_ladder — the sleeve is another exposure dial wearing a different asset: once priced on the
        same axis at matched starting book it is dominated by the ladder like everything else,
        and idea 134's "no gross level clears 4b but a sleeve does" is a statement about 4b's
        BAR GEOMETRY (a CAGR floor and a DD cap that the one-dimensional ladder cannot straddle),
        not about the price of insurance.
    They make opposite predictions on the same table, so the run cannot be steered.

TUNED PARAMETERS — exactly two, both swept and fully reported at every grid point
    f  sleeve fraction         in {0.05, 0.10, 0.15, 0.20, 0.25, 0.50}   (idea 134's sweep)
    m  static gross multiplier in 0.10 .. 1.00 step 0.05                 (idea 94's LADDER)
    Everything else is inherited and never selected on: the sleeve's own construction (ideas
    100/104's momentum-vote x risk-parity, imported verbatim from idea 134), the 200d gate, the
    3% band, both gate conventions (-dg / -rw), the base books, cadence (weekly), execution lag
    (t+1), cost rungs (10 and 25 bps) and 4b's coefficients (phi=0.70, delta=0.60).
    The two sleeve asset sets are two INSTRUMENTS, not a dial, in idea 94's sense (as stop15 and
    stop25 are two menu entries): S3 = TLT/GLD/UUP, S4 = TLT/GLD/DBC/UUP.

CORPUS
    panels      u56 (universe.json, 56) and broad (universe_broad.json, 136).  Both carry
                TLT/GLD/DBC/UUP — asserted below, not assumed.  The small panel has none of
                them, so a sleeve book cannot exist there (idea 134's own exclusion).
    base books  V1u, TOP20, EWall — idea 94's three, all at 0.75 gross, ungated, so every
                instrument is priced as an overlay on the SAME starting book ("matched starting
                book").  idea 134 priced the sleeve on TOP20 (its `R20`) alone; carrying three
                base books is what tests whether the sleeve's price is a property of the sleeve
                or of the book it is blended into.
    arms/cell   control + 19 DEGROSS ladder points + 12 sleeve arms (2 asset sets x 6 f)
                + g200-dg + g200-rw + band3-dg + band3-rw  =  36
    cells       2 panels x 3 books x 2 cost rungs = 12   =>  432 arm rows, all committed.

WALK-FORWARD (PROTOCOL rule 8; selectors fixed in writing before any OOS number was read)
    Parameters (f, m, and the instrument family) are chosen on 2009-2016 alone; 2017-2026 is
    read once.  The IS ladder slope and the IS matched-DD control are recomputed on the IS
    window, so nothing in the choice touches the OOS half.
      S_price   argmin IS rate over every treated arm buying >= 0.10 pp of IS drawdown
                (the cheapest insurance in-sample)
      S_family  the same, within each family {SLV3, SLV4, g200, band3, DEGROSS} — this is the
                one that answers the queue: does the sleeve's cheapness survive OOS?
      S_sharpe  argmax IS Sharpe over every arm (idea 151's do-nothing control)
    Every pick is evaluated untouched on 2017-2026 against SPY, the LIVE book (RULES v2),
    RULES v1, and its own OOS ladder slope / OOS matched-DD control.

BOTH KEEP PATHS on all 432 rows
    4a  Sharpe > the LIVE book (RULES v2) in BOTH halves and MaxDD no worse (RULES v1 reported
        beside it for continuity with the pre-2026-09-06 record).
    4b  the five bars vs SPY (H1, H2, OOS, MaxDD cap 0.60x, CAGR floor 0.70x).

REPRODUCTION GATE (nothing new is read until it passes)
    - `H.run` with every instrument off reproduces `engine.backtest` on the evaluated slice.
    - idea 134's COMMITTED ladder.csv is rebuilt from source on its broad/R20 rows and on the
      S3-10 / S3-25 / S4-10 / S4-25 rows the queue's claim rests on.
    - the queue's premise is audited in its own words: is it true that NO gross level puts the
      ranked book inside 4b on broad@10bps, and that a sleeve at f>=0.10 does?

CAVEATS carried, not buried
    - Survivorship (idea 54): current-constituent panels.  Both the sleeve assets and the
      equity book are survivors; the sleeve's ETFs are index products, so survivorship inflates
      the EQUITY side of the blend more than the sleeve side — i.e. it works AGAINST the
      sleeve's measured price, which is the direction that runs against this run's finding.
    - Idea 128: the IS window cannot express deep drawdowns, so every IS-window price (the one
      rule 8 chooses on) is measured on a short ruler.
    - MaxDD is one number off one path and the price's DENOMINATOR is a difference of two of
      them; arms buying < 0.10 pp of drawdown get no price at all (NaN), as in idea 94.
    - The sleeve changes the ASSET MIX, so its price is not a pure timing statement: TLT/GLD/UUP
      carry their own returns over 2009-2026 (a falling-rate era for TLT).  This is stated as a
      limit on the finding's transportability, and is measured in section (5).
    - SPY sits in both panels and is therefore inside the EWall base book; it is the benchmark
      as well.  Inherited from ideas 94/133, and it applies identically to an arm and to its own
      control, so it cancels in every price this run quotes.
    - Idea 38: u56/broad carry the calendar-day index; identical for arm and control.

RUN
    python research/backtests/2026-09-07_sleeve-moves-the-frontier_cloud.py
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-07_sleeve-moves-the-frontier_cloud"
OUT = ROOT / "research" / "backtests"
I134_LADDER = OUT / "2026-09-05_sleeve-f-that-clears-the-floor_cloud.ladder.csv"
I134_GRID = OUT / "2026-09-05_sleeve-f-that-clears-the-floor_cloud.grid.csv"
I94_PRICES = OUT / "2026-09-04_drawdown-insurance-price-list_B.pricelist.csv"


def _imp(name, fn):
    spec = importlib.util.spec_from_file_location(name, OUT / fn)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


H = _imp("i94", "2026-09-04_drawdown-insurance-price-list_B.py")        # idea 74's axis
I134 = _imp("i134", "2026-09-05_sleeve-f-that-clears-the-floor_cloud.py")  # the sleeve, verbatim

FREQ, GROSS = H.FREQ, H.GROSS
IS_END, OOS_START = H.IS_END, H.OOS_START
COSTS = H.COSTS                       # [10, 25]
LADDER = H.LADDER                     # 0.10 .. 1.00 step 0.05  (tuned parameter m)
FS = I134.FS                          # 0.05 .. 0.50            (tuned parameter f)
S3, S4 = I134.S3, I134.S4
BASE_BOOKS = H.BOOKS                  # V1u, TOP20, EWall
PHI, DELTA = 0.70, 0.60

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 4000)

LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def pct(k, n):
    return f"{k}/{n} = {(k / n if n else np.nan):.1%}"


# ---------------------------------------------------------------- books
_BASE = {}


def base_targets(px, book):
    """idea 94's ungated base book at 0.75 gross (cached per panel: the composite is the same
    frame for every arm in a cell, and re-deriving it 36 times would only cost time)."""
    key = (id(px), book)
    if key not in _BASE:
        _BASE[key] = H.targets(px, book)
    return _BASE[key]


def sleeve_book(px, book, assets, f):
    """(1-f) x the base book + f x ideas 100/104's sleeve, rescaled back to GROSS so the blend
    moves the MIX and never the exposure.  Identical to idea 134's `book_weights` when the base
    book is TOP20 (its `R20`); generalised to the other two base books so the sleeve's price can
    be separated from the book it is blended into."""
    base = (1 - f) * base_targets(px, book) + f * I134.sleeve_weights(px, assets)
    return base.mul((GROSS / base.sum(axis=1).replace(0, np.nan)).fillna(0.0), axis=0).fillna(0.0)


def arm_specs():
    """(arm, family, dial, weights-spec).  Order is the print order; nothing here is selected."""
    out = [("control", "CONTROL", np.nan, ("base", None, None))]
    for m in LADDER:
        out.append((f"degross-{m:.2f}", "DEGROSS", float(m), ("degross", None, float(m))))
    for tag, assets in (("SLV3", S3), ("SLV4", S4)):
        for f in FS:
            out.append((f"{tag}-{int(round(f * 100))}", tag, float(f), ("sleeve", assets, float(f))))
    for gate in ("g200", "band3"):
        for conv in ("dg", "rw"):
            out.append((f"{gate}-{conv}", gate, np.nan, ("gate", gate, conv)))
    return out


# ---------------------------------------------------------------- the price, per window
def ladder_frames(px, book, cost, start):
    """The base book's own static-gross ladder — the REFERENCE price: 19 points, no rule at all.
    Run once and metricised on all three windows, so the IS ladder rule 8 chooses on is the same
    simulation as the full-sample one it is reported beside."""
    frames = {w: [] for w in ("full", "IS", "OOS")}
    for m in LADDER:
        r = H.run(px, base_targets(px, book), m=float(m), bps=cost)["r"].loc[start:]
        for w in frames:
            mm = metrics(H.window(r, w))
            frames[w].append(dict(m=float(m), CAGR=mm["CAGR"], Sharpe=mm["Sharpe"],
                                  MaxDD=mm["MaxDD"]))
    return {w: pd.DataFrame(v) for w, v in frames.items()}


def bars_win(spy, which):
    """SPY's 4b bars on one window.  The IS form is idea 133's: four bars, not five — the OOS
    Sharpe bar cannot be evaluated on 2009-2016 without reading 2017-2026."""
    s = H.window(spy, which)
    h1, h2 = H.halves(s)
    m = metrics(s)
    return dict(s1=h1, s2=h2, sdd=m["MaxDD"], scagr=m["CAGR"])


def margins_win(r, spy, which):
    x = H.window(r, which)
    h1, h2 = H.halves(x)
    m = metrics(x)
    b = bars_win(spy, which)
    return dict(H1=h1 - b["s1"], H2=h2 - b["s2"],
                DD=DELTA * abs(b["sdd"]) - abs(m["MaxDD"]),
                CAGR=m["CAGR"] - PHI * b["scagr"])


def priced(rc, ra, L):
    """idea 94's price plus the two derived tests, on whichever window rc/ra/L were cut to."""
    slope = H.ladder_slope(L)
    p = H.price(rc, ra, slope)
    ma = metrics(ra)
    lad_at_dd = H.matched_dd(L, ma["MaxDD"])
    p["lad_slope"] = slope
    p["lever"] = p["rate"] / slope if np.isfinite(p["rate"]) and slope != 0 else np.nan
    p["lad_CAGR_at_matchedDD"] = lad_at_dd
    p["vs_matchedDD"] = (ma["CAGR"] * 100.0 - lad_at_dd) if np.isfinite(lad_at_dd) else np.nan
    return p


# ---------------------------------------------------------------- one cell
def do_cell(pname, px, spy, book, cost, start, v1_net, v2_net):
    bars = H.bars_of(spy)
    ctl_full = H.run(px, base_targets(px, book), bps=cost)["r"].loc[start:]
    LAD = ladder_frames(px, book, cost, start)
    LF, LI, LO = LAD["full"], LAD["IS"], LAD["OOS"]
    rows, rets = [], {}
    for arm, fam, dial, spec in arm_specs():
        if spec[0] in ("base", "degross"):
            W = base_targets(px, book)
        elif spec[0] == "sleeve":
            W = sleeve_book(px, book, spec[1], spec[2])
        else:
            W = H.targets(px, book, spec[1], spec[2])
        res = H.run(px, W, m=(spec[2] if spec[0] == "degross" else 1.0), bps=cost)
        r = res["r"].loc[start:]
        rets[arm] = r
        mm, mi, mo = metrics(r), metrics(H.window(r, "IS")), metrics(H.window(r, "OOS"))
        h1, h2 = H.halves(r)
        mg = H.margins(r, bars)
        mgi = margins_win(r, spy, "IS")
        fails = [k for k in ("H1", "H2", "OOS", "DD", "CAGR") if mg[k] <= 0]
        pf = priced(ctl_full, r, LF)
        pi = priced(H.window(ctl_full, "IS"), H.window(r, "IS"), LI)
        po = priced(H.window(ctl_full, "OOS"), H.window(r, "OOS"), LO)
        rows.append(dict(
            panel=pname, book=book, cost=cost, arm=arm, family=fam, dial=dial,
            CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
            IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
            OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
            gross=float(res["gross"].loc[start:].mean()),
            TO=float(res["to"].loc[start:].sum() / (len(r) / 252)),
            m_H1=mg["H1"], m_H2=mg["H2"], m_OOS=mg["OOS"], m_DD=mg["DD"], m_CAGR=mg["CAGR"],
            pass4b=(len(fails) == 0), fail4b=",".join(fails) or "-", n_fail=len(fails),
            floor_only=(fails == ["CAGR"]),
            IS_m_H1=mgi["H1"], IS_m_H2=mgi["H2"], IS_m_DD=mgi["DD"], IS_m_CAGR=mgi["CAGR"],
            IS_admit_4b=all(mgi[k] > 0 for k in ("H1", "H2", "DD", "CAGR")),
            IS_floor_only=(all(mgi[k] > 0 for k in ("H1", "H2", "DD")) and mgi["CAGR"] <= 0),
            OOS_m_Sharpe=mo["Sharpe"] - metrics(H.window(spy, "OOS"))["Sharpe"],
            OOS_m_DD=DELTA * abs(metrics(H.window(spy, "OOS"))["MaxDD"]) - abs(mo["MaxDD"]),
            OOS_m_CAGR=mo["CAGR"] - PHI * metrics(H.window(spy, "OOS"))["CAGR"],
            pass4a_v2=H.pass4a(r, v2_net), pass4a_v1=H.pass4a(r, v1_net),
            dCAGR=pf["dCAGR"], dMaxDD=pf["dMaxDD"], rate=pf["rate"], dSharpe=pf["dSharpe"],
            lad_slope=pf["lad_slope"], lever=pf["lever"], dominated=pf["dominated"],
            lad_CAGR_at_matchedDD=pf["lad_CAGR_at_matchedDD"], vs_matchedDD=pf["vs_matchedDD"],
            IS_dMaxDD=pi["dMaxDD"], IS_rate=pi["rate"], IS_lever=pi["lever"],
            IS_vs_matchedDD=pi["vs_matchedDD"], IS_lad_slope=pi["lad_slope"],
            OOS_dMaxDD=po["dMaxDD"], OOS_rate=po["rate"], OOS_lever=po["lever"],
            OOS_vs_matchedDD=po["vs_matchedDD"], OOS_lad_slope=po["lad_slope"],
        ))
    return pd.DataFrame(rows), rets, dict(LF=LF, LI=LI, LO=LO)


# ---------------------------------------------------------------- rule 8
def walk_forward(D, rets, key, spy, v1_net, v2_net):
    ms = metrics(spy.loc[OOS_START:])
    mv2 = metrics(H.window(v2_net, "OOS"))
    mv1 = metrics(H.window(v1_net, "OOS"))
    ctl = D[D.arm == "control"].iloc[0]
    treated = D[D.family != "CONTROL"]
    elig = treated[(treated.IS_dMaxDD > 0.10) & np.isfinite(treated.IS_rate)]
    out = []

    def emit(sel, sub):
        base = dict(sel=sel, panel=key[0], book=key[1], cost=key[2],
                    spy_OOS_Sharpe=ms["Sharpe"], spy_OOS_CAGR=ms["CAGR"],
                    spy_OOS_MaxDD=ms["MaxDD"], v2_OOS_Sharpe=mv2["Sharpe"],
                    v2_OOS_CAGR=mv2["CAGR"], v2_OOS_MaxDD=mv2["MaxDD"],
                    v1_OOS_Sharpe=mv1["Sharpe"],
                    ctl_OOS_Sharpe=ctl["OOS_Sharpe"], ctl_OOS_CAGR=ctl["OOS_CAGR"],
                    ctl_OOS_MaxDD=ctl["OOS_MaxDD"])
        if not len(sub):
            out.append(dict(base, pick="(none)", family="(none)", dial=np.nan, n_admitted=0,
                            IS_rate=np.nan, OOS_rate=np.nan, OOS_lever=np.nan,
                            OOS_vs_matchedDD=np.nan, OOS_CAGR=np.nan, OOS_Sharpe=np.nan,
                            OOS_MaxDD=np.nan, OOS_m_Sharpe=np.nan, OOS_m_DD=np.nan,
                            OOS_m_CAGR=np.nan, OOS_pass4b=np.nan,
                            beat_spy=np.nan, beat_v2=np.nan, beat_ctl=np.nan))
            return
        p = (sub.loc[sub.IS_Sharpe.idxmax()]
             if sel in ("S_sharpe", "S_4bIS", "S_4bIS_sleeve")
             else sub.loc[sub.IS_rate.idxmin()])
        out.append(dict(base, pick=p["arm"], family=p["family"], dial=p["dial"],
                        n_admitted=len(sub), IS_rate=p["IS_rate"], OOS_rate=p["OOS_rate"],
                        OOS_lever=p["OOS_lever"], OOS_vs_matchedDD=p["OOS_vs_matchedDD"],
                        OOS_CAGR=p["OOS_CAGR"], OOS_Sharpe=p["OOS_Sharpe"],
                        OOS_MaxDD=p["OOS_MaxDD"],
                        OOS_m_Sharpe=p["OOS_m_Sharpe"], OOS_m_DD=p["OOS_m_DD"],
                        OOS_m_CAGR=p["OOS_m_CAGR"],
                        OOS_pass4b=bool(p["OOS_m_Sharpe"] > 0 and p["OOS_m_DD"] > 0
                                        and p["OOS_m_CAGR"] > 0),
                        beat_spy=bool(p["OOS_Sharpe"] > ms["Sharpe"]),
                        beat_v2=bool(p["OOS_Sharpe"] > mv2["Sharpe"]),
                        beat_ctl=bool(p["OOS_Sharpe"] > ctl["OOS_Sharpe"])))

    emit("S_price", elig)
    emit("S_sharpe", treated)
    # the KEEP-path selector: among arms that clear 4b's four IS-evaluable bars on 2009-2016
    # alone, take the highest IS Sharpe and read 2017-2026 once.
    emit("S_4bIS", treated[treated.IS_admit_4b])
    emit("S_4bIS_sleeve", treated[treated.IS_admit_4b & treated.family.isin(["SLV3", "SLV4"])])
    # the same admitted set chosen by PRICE instead of by IS Sharpe — the two selectors
    # disagree, and which one the record uses decides whether the KEEP path survives OOS.
    emit("S_4bIS_price", elig[elig.IS_admit_4b])
    for fam in ["SLV3", "SLV4", "g200", "band3", "DEGROSS"]:
        emit(f"S_fam:{fam}", elig[elig.family == fam])
    return pd.DataFrame(out)


# ---------------------------------------------------------------- gates
def gate_engine(px, book, cost, start):
    W = base_targets(px, book)
    a = H.run(px, W, bps=cost)["r"].loc[start:]
    b = backtest(px, W, cost_bps=cost, freq=FREQ)["returns"].loc[start:]
    d = float((a - b).abs().max())
    say(f"    (0a) H.run == engine.backtest on {book}@{int(cost)}bps: max|diff| {d:.3e}")
    assert d < 1e-12, d
    return d


def gate_i134(px_by_panel):
    say("\n    (0b) idea 134's COMMITTED ladder.csv rebuilt from source (the rows the queue's "
        "claim rests on)")
    if not I134_LADDER.exists():
        say("    !! idea 134 ladder.csv missing"); raise SystemExit(2)
    L = pd.read_csv(I134_LADDER)
    checks, worst = 0, 0.0
    for (pn, bk, f, m, c), g in L.groupby(["panel", "book", "f", "m", "cost"]):
        if bk not in ("R20", "S3-10", "S3-25", "S4-10", "S4-25"):
            continue
        px, spy, start = px_by_panel[pn]
        if bk == "R20":
            W = base_targets(px, "TOP20")
        else:
            assets = S3 if bk.startswith("S3") else S4
            W = sleeve_book(px, "TOP20", assets, float(f))
        r = H.run(px, W, m=float(m), bps=float(c))["r"].loc[start:]
        mm = metrics(r)
        ref = g.iloc[0]
        for col, val in (("CAGR", mm["CAGR"]), ("Sharpe", mm["Sharpe"]), ("MaxDD", mm["MaxDD"])):
            worst = max(worst, abs(val - float(ref[col])))
        checks += 1
    say(f"    rebuilt {checks} committed ladder rows (R20 / S3-10 / S3-25 / S4-10 / S4-25, both "
        f"panels, both rungs): max|diff| over CAGR, Sharpe, MaxDD = {worst:.3e}")
    assert worst < 1e-9, worst
    return worst


def gate_i94(G):
    """The strongest gate available: idea 94 published a price list on exactly these three base
    books, both panels, both cost rungs, for the two comparands the queue names.  This run's
    price column must equal it, or its sleeve prices mean nothing."""
    say("\n    (0d) idea 94's COMMITTED pricelist.csv — the 200d gate and the 3% band, priced "
        "on idea 74's axis, are re-derived here from source")
    if not I94_PRICES.exists():
        say("    !! idea 94 pricelist.csv missing"); raise SystemExit(2)
    P = pd.read_csv(I94_PRICES)
    P["panel"] = P.uni.map({"universe.json(56)": "u56", "universe_broad.json": "broad"})
    P = P[P.arm.isin(["g200-dg", "g200-rw", "band3-dg", "band3-rw"])]
    m = P.merge(G, on=["panel", "book", "cost", "arm"], suffixes=("_ref", ""))
    assert len(m) == len(P) == 48, (len(m), len(P))
    worst = {}
    for c in ["dCAGR", "dMaxDD", "rate", "vs_matchedDD", "gross", "dSharpe"]:
        worst[c] = float(np.nanmax((m[c] - m[c + "_ref"]).abs().values))
    say(f"    {len(m)} of {len(P)} committed rows rebuilt: " +
        "  ".join(f"{k} {v:.3e}" for k, v in worst.items()))
    assert max(worst.values()) < 1e-12, worst
    say("    GATE PASS — the axis this run prices the sleeve on is idea 94's, to machine "
        "precision, on every row idea 94 published for these comparands.")
    return worst


def audit_premise(D_broad10):
    say("\n    (0c) PREMISE AUDIT, in the queue's own words — broad @10 bps, base book TOP20")
    d = D_broad10
    lad = d[d.family == "DEGROSS"]
    say(f"    ladder points inside 4b: {int(lad.pass4b.sum())} of {len(lad)} "
        f"(m = {lad.dial.min():.2f}..{lad.dial.max():.2f}); Sharpe range over the ladder "
        f"{lad.Sharpe.min():.3f}-{lad.Sharpe.max():.3f} (queue quotes 0.973-0.978 over its own "
        f"5-point m = 0.60..1.40 ladder)")
    for fam in ("SLV3", "SLV4"):
        s = d[d.family == fam]
        ok = s[s.pass4b]
        say(f"    {fam}: 4b passers at native gross {pct(len(ok), len(s))}" +
            (f" -> f = {sorted(ok.dial.tolist())}" if len(ok) else " -> NONE at m=1.00"))
    say("    NOTE the queue says 'a sleeve at f>=0.10 does'.  idea 134's own committed grid has "
        "the f>=0.10 passes at m=0.80, not at the native m=1.00; at native gross only f=0.25 "
        "passes.  Both readings are reported here and neither is required by this run's answer.")


# ---------------------------------------------------------------- reporting
def report_prices(G):
    say("\n" + "=" * 200)
    say("(1) THE PRICE LIST — pp of CAGR surrendered per pp of MaxDD bought, vs the SAME base "
        "book at the SAME cost (idea 74's axis; lower = cheaper insurance)")
    say("    `lever` = rate / the base book's own ladder slope: <1 means cheaper than simply "
        "holding less.  `vs_matchedDD` (pp/yr) = the arm's CAGR minus the ladder's CAGR at the "
        "ARM's own drawdown: >0 means the arm is NOT reachable by de-grossing.")
    T = G[G.family != "CONTROL"].groupby("family").agg(
        n=("rate", "size"), priced=("rate", lambda s: int(np.isfinite(s).sum())),
        med_rate=("rate", "median"), med_lever=("lever", "median"),
        dominated=("dominated", lambda s: float(np.nanmean(pd.to_numeric(s, errors="coerce")))),
        med_vs_matchedDD=("vs_matchedDD", "median"),
        beats_ladder=("vs_matchedDD", lambda s: float(np.nanmean((s > 0).astype(float)))),
        med_dMaxDD=("dMaxDD", "median"), med_dSharpe=("dSharpe", "median"))
    say(T.to_string(float_format=lambda x: f"{x:.3f}"))
    say("\n    by family x panel (all 12 cells pooled per panel):")
    T2 = G[G.family != "CONTROL"].groupby(["family", "panel"]).agg(
        n=("rate", "size"), med_rate=("rate", "median"), med_lever=("lever", "median"),
        beats_ladder=("vs_matchedDD", lambda s: float(np.nanmean((s > 0).astype(float)))),
        med_vs_matchedDD=("vs_matchedDD", "median"))
    say(T2.to_string(float_format=lambda x: f"{x:.3f}"))
    say("\n    THE SLEEVE, every f, every cell (the queue's instrument, all grid points):")
    S = G[G.family.isin(["SLV3", "SLV4"])]
    say(S[["panel", "book", "cost", "arm", "dial", "CAGR", "Sharpe", "MaxDD", "gross", "dCAGR",
           "dMaxDD", "rate", "lever", "vs_matchedDD", "pass4b", "fail4b", "pass4a_v2"]]
        .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say("\n    THE COMPARANDS the queue names — 200d gate, 3% band, de-grossing (median over "
        "the 12 cells; DEGROSS is shown at the ladder points nearest the sleeve's own gross):")
    K = G[G.family.isin(["g200", "band3"])]
    say(K[["panel", "book", "cost", "arm", "CAGR", "Sharpe", "MaxDD", "gross", "dCAGR", "dMaxDD",
           "rate", "lever", "vs_matchedDD", "pass4b", "fail4b"]]
        .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    return T


def head_to_head(G):
    say("\n" + "=" * 200)
    say("(2) HEAD TO HEAD at matched starting book and cost — the queue's actual question")
    say("    For each of the 12 cells: the cheapest arm of each family by `rate`, and whether "
        "it beats the base book's own ladder at its own drawdown.")
    rows = []
    for (p, b, c), g in G.groupby(["panel", "book", "cost"]):
        for fam in ["SLV3", "SLV4", "g200", "band3", "DEGROSS"]:
            s = g[(g.family == fam) & np.isfinite(g.rate)]
            if not len(s):
                rows.append(dict(panel=p, book=b, cost=c, family=fam, arm="(unpriced)",
                                 rate=np.nan, lever=np.nan, vs_matchedDD=np.nan,
                                 dMaxDD=np.nan, pass4b=False))
                continue
            q = s.loc[s.rate.idxmin()]
            rows.append(dict(panel=p, book=b, cost=c, family=fam, arm=q["arm"], rate=q["rate"],
                             lever=q["lever"], vs_matchedDD=q["vs_matchedDD"],
                             dMaxDD=q["dMaxDD"], pass4b=bool(q["pass4b"])))
    T = pd.DataFrame(rows)
    say(T.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say("\n    CHEAPEST FAMILY per cell (the menu's top entry, 12 cells):")
    win = T.dropna(subset=["rate"]).loc[T.dropna(subset=["rate"]).groupby(
        ["panel", "book", "cost"]).rate.idxmin()]
    say(win[["panel", "book", "cost", "family", "arm", "rate", "lever", "vs_matchedDD"]]
        .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say("    family win counts: " + ", ".join(f"{k} {v}" for k, v in
                                              win.family.value_counts().items()))
    return T


def offladder(G):
    say("\n" + "=" * 200)
    say("(3) IS THE SLEEVE A POINT ON THE GROSS LADDER?  (vs_matchedDD > 0 = it is NOT)")
    for fam in ["SLV3", "SLV4", "g200", "band3"]:
        s = G[G.family == fam]
        d = s.dropna(subset=["vs_matchedDD"])
        say(f"    {fam:6s}: defined {len(d):3d}/{len(s):3d} | beats its own matched-DD ladder "
            f"point in {pct(int((d.vs_matchedDD > 0).sum()), len(d))} | median "
            f"{d.vs_matchedDD.median():+.3f} pp/yr | max {d.vs_matchedDD.max():+.3f} | "
            f"min {d.vs_matchedDD.min():+.3f}")
    say("\n    the sleeve by f (pooled over 12 cells and both asset sets):")
    S = G[G.family.isin(["SLV3", "SLV4"])].dropna(subset=["vs_matchedDD"])
    say(S.groupby("dial").agg(n=("vs_matchedDD", "size"),
                              beats=("vs_matchedDD", lambda x: float((x > 0).mean())),
                              med_vs=("vs_matchedDD", "median"),
                              med_rate=("rate", "median"),
                              med_lever=("lever", "median"))
        .to_string(float_format=lambda x: f"{x:.3f}"))
    say("\n    and by panel x cost (is it a broad-panel fact, as idea 134's claim was?):")
    say(S.groupby(["panel", "cost"]).agg(n=("vs_matchedDD", "size"),
                                         beats=("vs_matchedDD", lambda x: float((x > 0).mean())),
                                         med_vs=("vs_matchedDD", "median"))
        .to_string(float_format=lambda x: f"{x:.3f}"))
    say("\n    and by BASE BOOK (is the price a property of the sleeve or of the book?):")
    say(S.groupby("book").agg(n=("vs_matchedDD", "size"),
                              beats=("vs_matchedDD", lambda x: float((x > 0).mean())),
                              med_vs=("vs_matchedDD", "median"),
                              med_rate=("rate", "median"))
        .to_string(float_format=lambda x: f"{x:.3f}"))


def exposure_check(G):
    say("\n" + "=" * 200)
    say("(4) IS THE SLEEVE AN EXPOSURE DIAL IN DISGUISE?  mean achieved gross, arm vs control")
    for (p, b, c), g in G.groupby(["panel", "book", "cost"]):
        ctl = float(g[g.arm == "control"].gross.iloc[0])
        s = g[g.family.isin(["SLV3", "SLV4"])]
        k = g[g.family.isin(["g200", "band3"])]
        say(f"    {p:5s} {b:5s} {int(c):2d}bps: control gross {ctl:.4f} | sleeve gross "
            f"{s.gross.min():.4f}-{s.gross.max():.4f} (max |diff| {float((s.gross - ctl).abs().max()):.4f}) "
            f"| gate/band gross {k.gross.min():.4f}-{k.gross.max():.4f}")
    say("    A sleeve arm that holds the same gross as its control but a shallower drawdown is "
        "buying drawdown with MIX, not with exposure — which is exactly the claim under test.")


def asset_note(G, px_by_panel):
    say("\n" + "=" * 200)
    say("(5) WHAT THE SLEEVE ASSETS DID OVER THIS SAMPLE (the transportability limit, stated "
        "as a number rather than as a worry)")
    px, spy, start = px_by_panel["u56"]
    for a in S4:
        r = px[a].pct_change().fillna(0.0).loc[start:]
        m, mi, mo = metrics(r), metrics(H.window(r, "IS")), metrics(H.window(r, "OOS"))
        say(f"    {a:4s} buy-and-hold: full {m['CAGR']:.2%}/{m['Sharpe']:.3f}/{m['MaxDD']:.2%} | "
            f"IS {mi['CAGR']:.2%}/{mi['Sharpe']:.3f} | OOS {mo['CAGR']:.2%}/{mo['Sharpe']:.3f}")
    say("    The sleeve is a momentum-vote x risk-parity blend of these, so its price is partly "
        "an asset-class statement about 2009-2026 and does not transport unconditionally.")


def keep_paths(G, spyref, v2ref):
    say("\n" + "=" * 200)
    say("(6) BOTH KEEP PATHS on all %d rows" % len(G))
    say(f"    4a vs the LIVE book (RULES v2): {pct(int(G.pass4a_v2.sum()), len(G))}   "
        f"(vs RULES v1: {pct(int(G.pass4a_v1.sum()), len(G))})")
    say(f"    4b vs SPY: {pct(int(G.pass4b.sum()), len(G))}   "
        f"both paths at once: {int((G.pass4a_v2 & G.pass4b).sum())}")
    for lab, sub in (("4b passers", G[G.pass4b]), ("4a(v2) passers", G[G.pass4a_v2])):
        if not len(sub):
            say(f"    {lab}: none")
            continue
        say(f"    {lab} ({len(sub)}), by family: " +
            ", ".join(f"{k} {v}" for k, v in sub.family.value_counts().items()))
        say(sub.sort_values("Sharpe", ascending=False).head(10)
            [["panel", "book", "cost", "arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
              "OOS_Sharpe", "rate", "lever", "vs_matchedDD", "pass4b", "pass4a_v2"]]
            .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    for p, s in spyref.items():
        say(f"    SPY {p}: CAGR {s['scagr']:.2%} halves {s['s1']:.3f}/{s['s2']:.3f} MaxDD "
            f"{s['sdd']:.2%} | 4b bars CAGR >= {PHI * s['scagr']:.2%}, MaxDD >= "
            f"{-DELTA * abs(s['sdd']):.2%}")
    for k, v in v2ref.items():
        say(f"    LIVE RULES v2 {k}: {v}")


def rule8(W):
    say("\n" + "=" * 200)
    say("(7) RULE 8 WALK-FORWARD — f, m and the family chosen on 2009-2016 alone; 2017-2026 "
        "read once.  12 cells (2 panels x 3 base books x 2 cost rungs).")
    T = W.groupby("sel").agg(
        cells=("pick", lambda s: int((s != "(none)").sum())),
        mean_IS_rate=("IS_rate", "mean"), mean_OOS_rate=("OOS_rate", "mean"),
        mean_OOS_lever=("OOS_lever", "mean"),
        mean_OOS_vs_matchedDD=("OOS_vs_matchedDD", "mean"),
        OOS_CAGR=("OOS_CAGR", "mean"), OOS_Sharpe=("OOS_Sharpe", "mean"),
        OOS_MaxDD=("OOS_MaxDD", "mean"),
        beats_SPY=("beat_spy", lambda s: int(np.nansum(pd.to_numeric(s, errors="coerce")))),
        beats_v2=("beat_v2", lambda s: int(np.nansum(pd.to_numeric(s, errors="coerce")))),
        beats_ctl=("beat_ctl", lambda s: int(np.nansum(pd.to_numeric(s, errors="coerce")))),
        OOS_pass4b=("OOS_pass4b", lambda s: int(np.nansum(pd.to_numeric(s, errors="coerce")))))
    say(T.to_string(float_format=lambda x: f"{x:.3f}"))
    say("\n    THE KEEP PATH UNDER RULE 8 — arms admitted by 4b's four IS-evaluable bars on "
        "2009-2016 alone, highest IS Sharpe taken, 2017-2026 read once and scored against 4b's "
        "bars computed on the OOS window:")
    say(W[W.sel.isin(["S_4bIS", "S_4bIS_sleeve", "S_4bIS_price"])]
        [["sel", "panel", "book", "cost", "pick", "n_admitted", "OOS_CAGR", "OOS_Sharpe",
          "OOS_MaxDD", "OOS_m_Sharpe", "OOS_m_DD", "OOS_m_CAGR", "OOS_pass4b", "beat_v2"]]
        .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say(f"\n    SPY OOS {W.spy_OOS_CAGR.mean():.2%} / {W.spy_OOS_Sharpe.mean():.3f} / "
        f"{W.spy_OOS_MaxDD.mean():.2%};  RULES v2 OOS by panel: " +
        ", ".join(f"{p} {g.v2_OOS_CAGR.mean():.2%}/{g.v2_OOS_Sharpe.mean():.3f}/"
                  f"{g.v2_OOS_MaxDD.mean():.2%}" for p, g in W.groupby("panel")))
    say("\n    IS-cheapest family per cell, and what it cost OOS (S_price):")
    say(W[W.sel == "S_price"][["panel", "book", "cost", "pick", "family", "IS_rate", "OOS_rate",
                               "OOS_lever", "OOS_vs_matchedDD", "OOS_CAGR", "OOS_Sharpe",
                               "OOS_MaxDD", "beat_spy", "beat_v2"]]
        .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say("\n    DOES THE SLEEVE'S CHEAPNESS SURVIVE?  per-family IS pick vs its own OOS price:")
    fam = W[W.sel.str.startswith("S_fam:")].copy()
    fam["fam"] = fam.sel.str.replace("S_fam:", "", regex=False)
    say(fam.groupby("fam").agg(cells=("pick", lambda s: int((s != "(none)").sum())),
                               IS_rate=("IS_rate", "mean"), OOS_rate=("OOS_rate", "mean"),
                               OOS_lever=("OOS_lever", "mean"),
                               OOS_vs=("OOS_vs_matchedDD", "mean"),
                               OOS_Sharpe=("OOS_Sharpe", "mean"),
                               OOS_CAGR=("OOS_CAGR", "mean"), OOS_MaxDD=("OOS_MaxDD", "mean"))
        .to_string(float_format=lambda x: f"{x:.3f}"))
    say("\n    per-cell detail (all selectors):")
    say(W[["sel", "panel", "book", "cost", "pick", "n_admitted", "IS_rate", "OOS_rate",
           "OOS_lever", "OOS_vs_matchedDD", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]]
        .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    return T


def main():
    say("=" * 200)
    say("IDEA 139 — sleeve-moves-the-frontier: price the macro sleeve on idea 74's axis against "
        "the 200d gate, the 3% band and de-grossing, at matched starting book and cost")
    say("corpus: 2 panels x 3 base books (V1u, TOP20, EWall, all 0.75 gross, ungated) x 2 cost "
        "rungs x 36 arms (control + 19 ladder + 12 sleeve + 4 gate/band) = 432 rows, all "
        "committed")
    say(f"IS <= {IS_END}   OOS >= {OOS_START}   weekly, t+1, 4b bars phi={PHI} delta={DELTA}")
    say(f"tuned: f in {FS} (sleeve fraction), m in {LADDER[0]:.2f}..{LADDER[-1]:.2f} step 0.05 "
        f"(static gross).  Both fully swept; all grid points reported.")
    say("H_offladder: the sleeve prices BELOW the ladder (lever<1) and beats its own matched-DD "
        "ladder point in the majority of cells.  H_ladder: it is dominated like every other "
        "instrument and idea 134's claim is about 4b's bar geometry, not about price.")
    say("=" * 200)

    px_by_panel, spyref, v2ref = {}, {}, {}
    GR, WF, LADS = [], [], []
    for pname, kw in (("u56", dict()), ("broad", dict(broad=True))):
        px = load_universe(**kw)
        missing = [a for a in S4 if a not in px.columns]
        assert not missing, f"{pname} lacks sleeve assets {missing}"
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        px_by_panel[pname] = (px, spy, start)
        bars = H.bars_of(spy)
        spyref[pname] = bars
        say(f"\n--- PANEL {pname}: {px.shape[1]} names | eval {start.date()} -> "
            f"{px.index[-1].date()} | sleeve assets present: {S4}")
        say(f"    SPY CAGR {bars['scagr']:.2%} MaxDD {bars['sdd']:.2%} halves "
            f"{bars['s1']:.3f}/{bars['s2']:.3f} OOS Sharpe {bars['soos']:.3f} | 4b bars: "
            f"CAGR >= {PHI * bars['scagr']:.2%}, MaxDD >= {-DELTA * abs(bars['sdd']):.2%}")
        for c in COSTS:
            v1 = backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
            v2 = backtest(px, rules_v2_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
            m2, m1 = metrics(v2), metrics(v1)
            v2ref[f"{pname}@{int(c)}bps"] = (f"{m2['CAGR']:.2%} / {m2['Sharpe']:.3f} / "
                                             f"{m2['MaxDD']:.2%} (v1 {m1['CAGR']:.2%} / "
                                             f"{m1['Sharpe']:.3f} / {m1['MaxDD']:.2%})")
            say(f"    live RULES v2 @{int(c)}bps: {v2ref[f'{pname}@{int(c)}bps']}")
            for book in BASE_BOOKS:
                D, rets, L = do_cell(pname, px, spy, book, c, start, v1, v2)
                GR.append(D)
                WF.append(walk_forward(D, rets, (pname, book, c), spy, v1, v2))
                LADS.append(L["LF"].assign(panel=pname, book=book, cost=c, window="full"))
                LADS.append(L["LI"].assign(panel=pname, book=book, cost=c, window="IS"))
                LADS.append(L["LO"].assign(panel=pname, book=book, cost=c, window="OOS"))
                say(f"      {pname:5s} {book:5s} {int(c):2d}bps: {len(D)} arms | 4b "
                    f"{int(D.pass4b.sum()):2d} | 4a(v2) {int(D.pass4a_v2.sum()):2d} | ladder "
                    f"slope {D.lad_slope.iloc[0]:.3f} | sleeve beats matched-DD ladder "
                    f"{int((D[D.family.isin(['SLV3','SLV4'])].vs_matchedDD > 0).sum())}/12")

    G = pd.concat(GR, ignore_index=True)
    W = pd.concat(WF, ignore_index=True)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    pd.concat(LADS, ignore_index=True).to_csv(OUT / f"{STEM}.ladders.csv", index=False)

    say("\n" + "=" * 200)
    say("(0) GATES — nothing new is read until these pass")
    px, spy, start = px_by_panel["u56"]
    gate_engine(px, "TOP20", 10.0, start)
    gate_engine(px, "EWall", 25.0, start)
    gate_i134(px_by_panel)
    gate_i94(G)
    audit_premise(G[(G.panel == "broad") & (G.cost == 10.0) & (G.book == "TOP20")])

    report_prices(G)
    T2 = head_to_head(G)
    T2.to_csv(OUT / f"{STEM}.cheapest_by_family.csv", index=False)
    offladder(G)
    exposure_check(G)
    asset_note(G, px_by_panel)
    keep_paths(G, spyref, v2ref)
    T = rule8(W)
    T.to_csv(OUT / f"{STEM}.selectors.csv", index=False)

    say("\n" + "=" * 200)
    say("(8) VERDICT")
    S = G[G.family.isin(["SLV3", "SLV4"])].dropna(subset=["vs_matchedDD"])
    K = G[G.family.isin(["g200", "band3"])].dropna(subset=["vs_matchedDD"])
    s_beat = float((S.vs_matchedDD > 0).mean()) if len(S) else np.nan
    k_beat = float((K.vs_matchedDD > 0).mean()) if len(K) else np.nan
    s_lev = float(np.nanmedian(S.lever)) if len(S) else np.nan
    say(f"    sleeve beats its own matched-DD ladder point in {s_beat:.1%} of priced arms "
        f"(median lever {s_lev:.3f}); the 200d gate and the 3% band do in {k_beat:.1%}.")
    if s_beat > 0.5 and s_lev < 1.0:
        say("    H_offladder HOLDS in-sample on this corpus: the sleeve is not reachable by "
            "de-grossing the same book.  The OOS half of the claim is section (7).")
    else:
        say("    H_offladder FAILS: the sleeve prices like the other instruments and idea 134's "
            "reading is about 4b's bar geometry, not about the price of insurance.")
    say("=" * 200)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
