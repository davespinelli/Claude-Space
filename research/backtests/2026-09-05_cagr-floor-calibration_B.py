#!/usr/bin/env python3
"""QUEUE idea 129 — absolute-bars-disqualify-the-best-insurance  (research sprint lane B, 2026-09-05)

QUESTION (pre-registered, from QUEUE.md idea 129)
    Idea 95's `theta=0.40/dg` is the best point in its own run on Sharpe (1.190) AND on
    drawdown (-12.6%) AND on price against the static-gross lever (+3.85 pp), and fails
    PROTOCOL rule 4b in 4 of 4 cells on the CAGR floor ALONE.  Ideas 100 and 117 report the
    identical shape.  Two questions, in order:

      Q1 (census)   How often, across the project's arm corpus, is an arm that is
                    PARETO-BEST on (Sharpe, MaxDD) killed by 4b's CAGR floor and by nothing
                    else?  If the answer is "rarely", idea 95 was an accident and 4b needs
                    no attention.  If it is "routinely", 4b's calibration is load-bearing.

      Q2 (calibration)  Is the floor at 0.70 x SPY doing RISK work, or is it a return
                    preference that mechanically excludes defensive books?  The falsifiable
                    form: screen arms on the IS window ALONE, then read the OOS window once.
                    If the arms the floor rejects (and nothing else rejects) turn out OOS to
                    be worse on Sharpe or deeper on drawdown than the arms it admits, the
                    floor is doing risk work and should stay at 0.70.  If they are OOS-equal
                    or OOS-BETTER on Sharpe and SHALLOWER on drawdown, and differ only in
                    CAGR, then the floor is a return preference wearing a risk bar's clothes,
                    and PROTOCOL should say so rather than calling those arms KILLs.

HARNESS
    Idea 94's script (`2026-09-04_drawdown-insurance-price-list_B.py`) is IMPORTED, not
    re-implemented: same simulator, same books, same gates, same instrument set, so every
    number here sits on the machine that produced the rows being audited.  The small panel is
    built with idea 97/118's construction verbatim (SPY held out, `max_1d_move >= 1.0` names
    dropped).  Three reproduction checks run before any new number is read:
      (a) the ungated EWall control vs `engine.backtest` — must be exact;
      (b) idea 94's published `EWall + vol60-dg` u56 @10bps row (11.6% / 1.133 / -16.9%);
      (c) this run's 4b verdict at (phi=0.70, delta=0.60) must equal `H.margins`' verdict on
          every one of the 306 corpus rows — i.e. the re-parameterised bars are the same bars.

CORPUS (nothing new is invented; this is the project's own published arm family)
    3 panels (u56, broad, small) x 3 books (V1u, TOP20, EWall) x 17 arms (control, 5 gates x
    {dg, rw}, 2 stops, 2 DD controls, 2 entry budgets) x 2 costs (10, 25 bps) = 306 arm-rows.
    A 19-point static-gross ladder per (panel, book, cost) is carried as a SEPARATE reference
    family, never mixed into the census: the ladder is pure de-risking, so the floor SHOULD
    kill its low-gross points, and that is the control which tells us the floor is not simply
    broken.

TUNED PARAMETERS — exactly two, both bars of 4b itself
    phi   CAGR floor coefficient   in {0.00, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00}   (0.70 published)
    delta MaxDD cap coefficient    in {0.50, 0.60, 0.70}                            (0.60 published)
    All 21 grid points are reported.  Nothing else is tuned: books, gates, dials, gross,
    cadence, cost rungs and window boundaries are inherited unchanged.

WALK-FORWARD (PROTOCOL rule 8; three selectors fixed in writing before any OOS number is read)
    S0  no screen:      argmax IS Sharpe over all 17 arms in the cell.
    S1  4b screen WITH the floor:    among arms whose IS window alone meets 4b's two halves
                                     bars, its DD cap at delta=0.60 and its CAGR floor at
                                     phi=0.70, argmax IS Sharpe.  (4b's OOS-Sharpe bar cannot
                                     be screened on prospectively and is therefore not used by
                                     any selector — it is read only in the OOS evaluation.)
    S2  4b screen WITHOUT the floor: identical, at phi=0.00 (the floor deleted, DD cap kept).
    Each picks at most one arm per cell; the pick is evaluated untouched on 2017-2026 against
    that cell's own ungated control, RULES v1 and SPY.  If S1 and S2 have equal OOS quality,
    the floor buys nothing in selection.  If S2 is OOS-better, the floor costs.

BOTH KEEP PATHS are evaluated on every corpus row (4a via `H.pass4a` against RULES v1 on the
same panel and cost; 4b via the re-parameterised bars).

CAVEATS carried, not buried
    - Survivorship: all three panels are current-constituent lists (idea 54).  It runs one way
      here: absent delistings inflate every arm's CAGR, and inflate the UNGATED books most,
      so the floor's real-world exclusion of defensive arms is if anything understated.
    - Idea 128: the IS window (SPY MaxDD -22.1%) is shallower than the OOS window (-33.7%), so
      an IS-window drawdown cap is measured on a window that cannot express deep drawdowns.
      This biases the S1/S2 comparison toward admitting too much, not too little; stated.
    - Idea 38: u56/broad still carry the calendar-day index.
    - Idea 126: every ratio below is quoted at t+1 execution only; no lag band is claimed.
    - The LEADERBOARD.md census (section E) is INDICATIVE ONLY — its rows span different
      samples, universes, costs and construction conventions and carry no OOS column, so it
      is reported as a range across two SPY reference sets and never used for a verdict.
"""
import importlib.util
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_cagr-floor-calibration_B"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"

_spec = importlib.util.spec_from_file_location("i94", I94)
H = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(H)

FREQ, GROSS, PCOST = H.FREQ, H.GROSS, H.PCOST
IS_END, OOS_START = H.IS_END, H.OOS_START
COSTS = [10.0, 25.0]
BOOKS = H.BOOKS
LADDER = H.LADDER
PANELS = ["u56", "broad", "small"]

PHIS = [0.00, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]   # tuned parameter 1 (CAGR floor)
DELTAS = [0.50, 0.60, 0.70]                          # tuned parameter 2 (MaxDD cap)
PHI0, DELTA0 = 0.70, 0.60                            # the published bars

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 1000)

LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ------------------------------------------------------------------ panels (idea 97/118 verbatim)
_PCACHE = {}


def panel(name):
    if name in _PCACHE:
        return _PCACHE[name]
    _PCACHE[name] = _panel(name)
    return _PCACHE[name]


def _panel(name):
    if name == "u56":
        px = load_universe()
        return px, px["SPY"].pct_change().fillna(0.0), "universe.json(56)"
    if name == "broad":
        px = load_universe(broad=True)
        return px, px["SPY"].pct_change().fillna(0.0), "universe_broad.json(136)"
    if name == "small":
        px = load_universe(small=True)
        meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
        bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
        inv = [c for c in px.columns if c != "SPY" and c not in bad]
        return px[inv], px["SPY"].pct_change().fillna(0.0), f"prices_small({len(inv)}, SPY held out)"
    raise ValueError(name)


# ------------------------------------------------------------------ re-parameterised 4b bars
def bars_win(spy, which):
    """SPY's 4b reference numbers on a window: 'full' (halves + OOS), 'IS', 'OOS'."""
    if which == "full":
        s1, s2 = H.halves(spy)
        m = metrics(spy)
        return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"],
                    soos=metrics(spy.loc[OOS_START:])["Sharpe"])
    w = H.window(spy, which)
    s1, s2 = H.halves(w)
    m = metrics(w)
    return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"], soos=m["Sharpe"])


def margins_at(r, b, phi, delta, which="full"):
    """4b's five margins with the two coefficients exposed.  which='full' is PROTOCOL's own
    reading (halves + OOS of the whole sample); which='IS'/'OOS' reads a single window and
    splits IT into halves, which is what a prospective screen can actually see."""
    w = H.window(r, which)
    h1, h2 = H.halves(w)
    m = metrics(w)
    soos = metrics(r.loc[OOS_START:])["Sharpe"] if which == "full" else m["Sharpe"]
    return dict(H1=h1 - b["s1"], H2=h2 - b["s2"], OOS=soos - b["soos"],
                DD=delta * abs(b["sdd"]) - abs(m["MaxDD"]),
                CAGR=m["CAGR"] - phi * b["scagr"])


def fails(mg):
    return [k for k in ("H1", "H2", "OOS", "DD", "CAGR") if mg[k] <= 0]


def pareto_front(df, s="Sharpe", d="MaxDD"):
    """Boolean mask: arm is non-dominated on (Sharpe up, MaxDD up i.e. shallower)."""
    S, D = df[s].values, df[d].values
    out = np.ones(len(df), dtype=bool)
    for i in range(len(df)):
        if not np.isfinite(S[i]) or not np.isfinite(D[i]):
            out[i] = False
            continue
        dom = (S >= S[i]) & (D >= D[i]) & ((S > S[i]) | (D > D[i]))
        out[i] = not dom.any()
    return out


# ------------------------------------------------------------------ one (panel, book, cost) cell
def do_cell(pname, px, spy, book, cost, bfull, bIS, v1_net):
    rows, rets = [], {}
    for arm, kind, kw, (gate, conv) in H.arm_specs():
        W = H.targets(px, book, gate, conv)
        res = H.run(px, W, bps=cost, **kw)
        r = res["r"].loc[spy.index[0]:]
        rets[arm] = r
        m, mi, mo = metrics(r), metrics(H.window(r, "IS")), metrics(H.window(r, "OOS"))
        mg = margins_at(r, bfull, PHI0, DELTA0, "full")
        mgi = margins_at(r, bIS, PHI0, DELTA0, "IS")
        f = fails(mg)
        rows.append(dict(
            panel=pname, book=book, cost=cost, arm=arm, kind=kind,
            CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
            H1=H.halves(r)[0], H2=H.halves(r)[1],
            IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
            OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
            m_H1=mg["H1"], m_H2=mg["H2"], m_OOS=mg["OOS"], m_DD=mg["DD"], m_CAGR=mg["CAGR"],
            IS_m_H1=mgi["H1"], IS_m_H2=mgi["H2"], IS_m_OOS=mgi["OOS"],
            IS_m_DD=mgi["DD"], IS_m_CAGR=mgi["CAGR"],
            pass4b=(len(f) == 0), fail4b=",".join(f) or "-", n_fail=len(f),
            floor_only=(f == ["CAGR"]),
            pass4a=H.pass4a(r, v1_net),
            gross=float(res["gross"].loc[spy.index[0]:].mean()),
            TO=float(res["to"].loc[spy.index[0]:].sum() / (len(r) / 252)),
        ))
    D = pd.DataFrame(rows)
    D["pareto"] = pareto_front(D)
    return D, rets


def ladder_cell(pname, px, spy, book, cost, bfull):
    W = H.targets(px, book)
    rows = []
    for m_ in LADDER:
        r = H.run(px, W, m=m_, bps=cost)["r"].loc[spy.index[0]:]
        mm = metrics(r)
        mg = margins_at(r, bfull, PHI0, DELTA0, "full")
        f = fails(mg)
        rows.append(dict(panel=pname, book=book, cost=cost, m=float(m_),
                         CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                         pass4b=(len(f) == 0), fail4b=",".join(f) or "-",
                         floor_only=(f == ["CAGR"])))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ walk-forward (rule 8)
def walk_forward(G, RET, bIS, bfull, spy, v1_net, key):
    """S0 / S1 / S2 on one cell.  Screens read the IS window ONLY."""
    sub = G[(G.panel == key[0]) & (G.book == key[1]) & (G.cost == key[2])]
    picks = {}
    isok = lambda row, phi: all(  # noqa: E731
        row[f"IS_m_{k}"] > 0 for k in ("H1", "H2", "DD")) and (
        row["IS_CAGR"] - phi * bIS["scagr"] > 0)
    cand = {"S0": sub,
            "S1": sub[sub.apply(lambda r: isok(r, PHI0), axis=1)],
            "S2": sub[sub.apply(lambda r: isok(r, 0.00), axis=1)]}
    ctl = RET["control"]
    mc = metrics(H.window(ctl, "OOS"))
    ms = metrics(spy.loc[OOS_START:])
    mv = metrics(H.window(v1_net, "OOS"))
    for s, c in cand.items():
        if len(c) == 0:
            picks[s] = dict(sel=s, panel=key[0], book=key[1], cost=key[2], pick="(none)",
                            n_admitted=0, OOS_CAGR=np.nan, OOS_Sharpe=np.nan, OOS_MaxDD=np.nan,
                            beat_ctl=np.nan, beat_spy=np.nan, beat_v1=np.nan,
                            oos_best=np.nan, oos_rank=np.nan)
            continue
        p = c.loc[c.IS_Sharpe.idxmax()]
        r = H.window(RET[p["arm"]], "OOS")
        m = metrics(r)
        order = sub.OOS_Sharpe.rank(ascending=False)
        picks[s] = dict(sel=s, panel=key[0], book=key[1], cost=key[2], pick=p["arm"],
                        n_admitted=len(c), OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"],
                        OOS_MaxDD=m["MaxDD"],
                        beat_ctl=bool(m["Sharpe"] > mc["Sharpe"]),
                        beat_spy=bool(m["Sharpe"] > ms["Sharpe"]),
                        beat_v1=bool(m["Sharpe"] > mv["Sharpe"]),
                        oos_best=bool(p["arm"] == sub.loc[sub.OOS_Sharpe.idxmax(), "arm"]),
                        oos_rank=float(order.loc[p.name]))
    for s in picks:
        picks[s].update(ctl_OOS_Sharpe=mc["Sharpe"], spy_OOS_Sharpe=ms["Sharpe"],
                        v1_OOS_Sharpe=mv["Sharpe"], ctl_OOS_MaxDD=mc["MaxDD"],
                        spy_OOS_MaxDD=ms["MaxDD"])
    return pd.DataFrame(list(picks.values()))


# ------------------------------------------------------------------ leaderboard census (indicative)
def leaderboard_census():
    txt = (ROOT / "research" / "LEADERBOARD.md").read_text().split("\n")
    pat = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|(.*?)\|\s*(-?[\d.]+)%\s*\|\s*(-?[\d.]+)\s*\|"
                     r"\s*(-?[\d.]+)%\s*\|")
    rows = []
    for ln in txt:
        m = pat.match(ln)
        if m:
            rows.append(dict(date=m.group(1), idea=m.group(2).strip()[:70],
                             CAGR=float(m.group(3)) / 100, Sharpe=float(m.group(4)),
                             MaxDD=float(m.group(5)) / 100))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ main
def main():
    say("=" * 200)
    say(f"IDEA 129 — is 4b's CAGR floor doing risk work?   corpus = 3 panels x 3 books x "
        f"17 arms x 2 costs = {3*3*17*2} arm-rows;  ladder = 3 x 3 x {len(LADDER)} x 2 reference rows")
    say(f"IS <= {IS_END}   OOS >= {OOS_START}   t+1 execution, weekly, {GROSS:.0%} gross, "
        f"costs {COSTS} bps.  Published bars: CAGR >= {PHI0} x SPY, MaxDD <= {DELTA0} x |SPY|.")
    say("=" * 200)

    GR, LD, WF, RET = [], [], [], {}
    SPYREF = {}
    for pname in PANELS:
        px, spy, desc = panel(pname)
        start = px.index[260]
        spy = spy.loc[start:]
        bfull, bIS = bars_win(spy, "full"), bars_win(spy, "IS")
        mo = metrics(spy.loc[OOS_START:])
        SPYREF[pname] = dict(desc=desc, **bfull, oos_cagr=mo["CAGR"], oos_dd=mo["MaxDD"])
        say(f"\n--- PANEL {pname}: {desc} | {px.index[0].date()} -> {px.index[-1].date()} | "
            f"eval from {start.date()}")
        say(f"    SPY full  CAGR {bfull['scagr']:.2%}  Sharpe {metrics(spy)['Sharpe']:.3f}  "
            f"MaxDD {bfull['sdd']:.2%}  halves {bfull['s1']:.3f}/{bfull['s2']:.3f}  "
            f"OOS Sharpe {bfull['soos']:.3f}")
        say(f"    bars: CAGR floor {PHI0*bfull['scagr']:.2%}/yr   DD cap "
            f"{-DELTA0*abs(bfull['sdd']):.2%}   |  IS-window SPY: CAGR {bIS['scagr']:.2%} "
            f"MaxDD {bIS['sdd']:.2%}  (idea 128: the IS window is {abs(bIS['sdd'])/abs(bfull['sdd']):.0%} "
            f"as deep as the full sample)")

        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        for book in BOOKS:
            for c in COSTS:
                D, rets = do_cell(pname, px, spy, book, c, bfull, bIS, v1[c])
                GR.append(D)
                RET[(pname, book, c)] = rets
                LD.append(ladder_cell(pname, px, spy, book, c, bfull))
                WF.append(walk_forward(pd.concat(GR, ignore_index=True), rets, bIS, bfull,
                                       spy, v1[c], (pname, book, c)))
        say(f"    ... {pname} done")

    G = pd.concat(GR, ignore_index=True)
    L = pd.concat(LD, ignore_index=True)
    W = pd.concat(WF, ignore_index=True)

    # ---------------------------------------------------------------- reproduction checks
    say("\n" + "=" * 200)
    say("REPRODUCTION CHECKS (all three must pass before any new number is read)")
    px56, spy56, _ = panel("u56")
    s56 = px56.index[260]
    ew = H.targets(px56, "EWall")
    a = H.run(px56, ew, bps=PCOST)["r"].loc[s56:]
    b = backtest(px56, ew, cost_bps=PCOST, freq=FREQ)["returns"].loc[s56:]
    say(f"  (a) run() vs engine.backtest on ungated EWall u56: max|diff| = {float((a-b).abs().max()):.2e}"
        f"  -> {'PASS' if float((a-b).abs().max()) < 1e-12 else 'FAIL'}")
    pub = G[(G.panel == "u56") & (G.book == "EWall") & (G.cost == 10.0) & (G.arm == "vol60-dg")].iloc[0]
    ok_b = abs(pub.CAGR - 0.116) < 5e-4 and abs(pub.Sharpe - 1.133) < 5e-3 and abs(pub.MaxDD + 0.169) < 5e-4
    say(f"  (b) idea 94's published EWall+vol60-dg u56@10bps 11.6%/1.133/-16.9%: got "
        f"{pub.CAGR:.3%}/{pub.Sharpe:.3f}/{pub.MaxDD:.3%} -> {'PASS' if ok_b else 'FAIL'}")
    mism = 0
    for pname in PANELS:
        _, spy, _ = panel(pname)
        pxp, _, _ = panel(pname)
        spy = spy.loc[pxp.index[260]:]
        bf = bars_win(spy, "full")
        for (bk, c), rets in [((k[1], k[2]), v) for k, v in RET.items() if k[0] == pname]:
            for arm, r in rets.items():
                ref = H.margins(r, bf)
                mine = margins_at(r, bf, PHI0, DELTA0)
                if max(abs(ref[k] - mine[k]) for k in ref) > 1e-12:
                    mism += 1
    say(f"  (c) re-parameterised bars at (phi={PHI0}, delta={DELTA0}) vs H.margins on all "
        f"{len(G)} rows: {mism} mismatches -> {'PASS' if mism == 0 else 'FAIL'}")

    # ---------------------------------------------------------------- Q1 the census
    say("\n" + "=" * 200)
    say("Q1  CENSUS — of the arms that are PARETO-BEST on (Sharpe, MaxDD) in their own cell,")
    say("    how many are killed by 4b and by which bar?   (18 cells x 17 arms, full sample)")
    say("=" * 200)
    P = G[G.pareto]
    say(f"  Pareto-best arm-rows: {len(P)} of {len(G)} ({len(P)/len(G):.1%});  "
        f"{P.groupby(['panel']).size().to_dict()}")
    say(f"  of those {len(P)}:  pass 4b {int(P.pass4b.sum())}   "
        f"fail on the CAGR floor ALONE {int(P.floor_only.sum())}   "
        f"fail on >=1 other bar {int((~P.pass4b & ~P.floor_only).sum())}")
    say(f"  -> the floor alone is the SOLE cause of KILL in {int(P.floor_only.sum())} of "
        f"{int((~P.pass4b).sum())} Pareto-best KILLs "
        f"({P.floor_only.sum()/max(1,(~P.pass4b).sum()):.0%}) and in "
        f"{P.floor_only.sum()/len(P):.0%} of all Pareto-best rows")
    say("\n  same census on the WHOLE corpus (not just the frontier):")
    say(f"    pass 4b {int(G.pass4b.sum())} of {len(G)} ({G.pass4b.mean():.1%});  "
        f"floor-only KILLs {int(G.floor_only.sum())} ({G.floor_only.mean():.1%});  "
        f"other KILLs {int((~G.pass4b & ~G.floor_only).sum())}")
    say("\n  which bar kills, counted over all corpus KILLs (a row can fail several):")
    fc = {k: int(G[~G.pass4b][f"m_{k}"].le(0).sum()) for k in ("H1", "H2", "OOS", "DD", "CAGR")}
    say(f"    {fc}   (n KILLs = {int((~G.pass4b).sum())})")
    say("\n  Pareto-best rows killed by the floor alone — the arms 4b throws away:")
    cols = ["panel", "book", "cost", "arm", "CAGR", "Sharpe", "MaxDD", "OOS_Sharpe", "OOS_MaxDD",
            "gross", "m_CAGR", "pass4a"]
    say(P[P.floor_only][cols].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    say("\n  LADDER CONTROL (pure de-grossing; the floor SHOULD bite here):")
    say(f"    ladder rows {len(L)};  pass 4b {int(L.pass4b.sum())} ({L.pass4b.mean():.1%});  "
        f"floor-only KILLs {int(L.floor_only.sum())} ({L.floor_only.mean():.1%})")
    lm = L[L.floor_only].groupby(["panel"]).m.agg(["min", "max", "count"])
    say(f"    gross multiplier at which the floor bites, by panel:\n{lm.to_string()}")

    # ---------------------------------------------------------------- Q2a calibration grid
    say("\n" + "=" * 200)
    say("Q2a CALIBRATION GRID — all 21 (phi, delta) points, full-sample 4b applied to the 306-row corpus")
    say("=" * 200)
    grid = []
    for pname in PANELS:
        pxp, spy, _ = panel(pname)
        spy = spy.loc[pxp.index[260]:]
        bf = bars_win(spy, "full")
        for (pn, bk, c), rets in RET.items():
            if pn != pname:
                continue
            for arm, r in rets.items():
                mo = metrics(H.window(r, "OOS"))
                for phi in PHIS:
                    for de in DELTAS:
                        f = fails(margins_at(r, bf, phi, de))
                        grid.append(dict(panel=pn, book=bk, cost=c, arm=arm, phi=phi, delta=de,
                                         pass4b=(len(f) == 0), floor_only=(f == ["CAGR"]),
                                         dd_only=(f == ["DD"]),
                                         OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
    GRID = pd.DataFrame(grid)
    piv = GRID.groupby(["phi", "delta"]).agg(
        n_pass=("pass4b", "sum"), pct_pass=("pass4b", "mean"),
        floor_only=("floor_only", "sum"), dd_only=("dd_only", "sum")).reset_index()
    adm = GRID[GRID.pass4b].groupby(["phi", "delta"]).agg(
        adm_OOS_Sharpe=("OOS_Sharpe", "mean"), adm_OOS_MaxDD=("OOS_MaxDD", "mean")).reset_index()
    piv = piv.merge(adm, on=["phi", "delta"], how="left")
    say(piv.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say("\n  read: `n_pass` out of 306.  `adm_OOS_*` = mean OOS outcome of the arms the bars admit.")

    # ---------------------------------------------------------------- Q2b the risk-work test
    say("\n" + "=" * 200)
    say("Q2b THE RISK-WORK TEST — screen on the IS window ALONE, then read OOS once.")
    say("    A = IS-admitted at (phi=0.70, delta=0.60).   B = rejected by the IS CAGR floor ALONE.")
    say("    C = rejected by some other IS bar.   If the floor does risk work, B must be OOS-worse.")
    say("=" * 200)
    grp = []
    for pname in PANELS:
        pxp, spy, _ = panel(pname)
        spy = spy.loc[pxp.index[260]:]
        bI = bars_win(spy, "IS")
        for (pn, bk, c), rets in RET.items():
            if pn != pname:
                continue
            for arm, r in rets.items():
                mgi = margins_at(r, bI, PHI0, DELTA0, "IS")
                mgi_nofloor = dict(mgi, CAGR=metrics(H.window(r, "IS"))["CAGR"] - 0.0)
                f = fails(mgi)
                f0 = fails(mgi_nofloor)
                g = "A" if len(f) == 0 else ("B" if (len(f0) == 0 and f == ["CAGR"]) else "C")
                mo = metrics(H.window(r, "OOS"))
                grp.append(dict(panel=pn, book=bk, cost=c, arm=arm, group=g,
                                IS_CAGR=metrics(H.window(r, "IS"))["CAGR"],
                                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                gross=float(G[(G.panel == pn) & (G.book == bk) & (G.cost == c) &
                                              (G.arm == arm)].gross.iloc[0])))
    Q = pd.DataFrame(grp)
    agg = Q.groupby("group").agg(n=("arm", "size"), OOS_Sharpe=("OOS_Sharpe", "mean"),
                                 OOS_Sharpe_med=("OOS_Sharpe", "median"),
                                 OOS_MaxDD=("OOS_MaxDD", "mean"),
                                 OOS_MaxDD_med=("OOS_MaxDD", "median"),
                                 OOS_CAGR=("OOS_CAGR", "mean"), gross=("gross", "mean"))
    say(agg.to_string(float_format=lambda x: f"{x:.3f}"))
    A, B = Q[Q.group == "A"], Q[Q.group == "B"]
    if len(B) and len(A):
        def welch(x, y):
            nx, ny = len(x), len(y)
            if nx < 2 or ny < 2:
                return np.nan, np.nan
            se = np.sqrt(x.var(ddof=1) / nx + y.var(ddof=1) / ny)
            return float(x.mean() - y.mean()), (float((x.mean() - y.mean()) / se) if se > 0 else np.nan)
        for col in ("OOS_Sharpe", "OOS_MaxDD", "OOS_CAGR"):
            d, t = welch(B[col], A[col])
            say(f"  B - A on {col}: {d:+.3f}   Welch t {t:+.2f}"
                f"   (B = the floor's exclusive victims, n={len(B)}; A = admitted, n={len(A)})")
        say(f"  B beats A's cell-mean OOS Sharpe in "
            f"{int(sum(B.OOS_Sharpe.mean() > A.OOS_Sharpe.mean() for _ in [0]))} of 1 pooled comparison; "
            f"paired by cell:")
        pair = Q.pivot_table(index=["panel", "book", "cost"], columns="group",
                             values="OOS_Sharpe", aggfunc="mean")
        if {"A", "B"} <= set(pair.columns):
            pp = pair.dropna(subset=["A", "B"])
            say(f"    cells with both A and B: {len(pp)};  B > A in {int((pp.B > pp.A).sum())}"
                f"   mean(B-A) {float((pp.B - pp.A).mean()):+.3f}")
        pdd = Q.pivot_table(index=["panel", "book", "cost"], columns="group",
                            values="OOS_MaxDD", aggfunc="mean")
        if {"A", "B"} <= set(pdd.columns):
            pq = pdd.dropna(subset=["A", "B"])
            say(f"    OOS MaxDD paired: B shallower than A in {int((pq.B > pq.A).sum())} of "
                f"{len(pq)} cells;  mean(B-A) {float((pq.B - pq.A).mean()):+.3f} "
                f"(positive = the floor's victims drew down LESS)")

    # ---------------------------------------------------------------- rule 8
    say("\n" + "=" * 200)
    say("RULE 8 WALK-FORWARD — S0 (no screen) / S1 (4b with the floor) / S2 (4b, floor deleted).")
    say("    Screens read 2009-2016 only; 2017-2026 read once.  18 cells.")
    say("=" * 200)
    say(W[["sel", "panel", "book", "cost", "pick", "n_admitted", "OOS_CAGR", "OOS_Sharpe",
           "OOS_MaxDD", "beat_ctl", "beat_spy", "beat_v1", "oos_best", "oos_rank"]]
        .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say("\n  summary by selector (means over the 18 cells; a cell where the selector admits "
        "nothing is excluded from its means and counted in `empty`):")
    ws = W.groupby("sel").agg(
        empty=("pick", lambda s: int((s == "(none)").sum())),
        mean_admitted=("n_admitted", "mean"),
        OOS_CAGR=("OOS_CAGR", "mean"), OOS_Sharpe=("OOS_Sharpe", "mean"),
        OOS_MaxDD=("OOS_MaxDD", "mean"),
        beat_ctl=("beat_ctl", "sum"), beat_spy=("beat_spy", "sum"), beat_v1=("beat_v1", "sum"),
        oos_best=("oos_best", "sum"), mean_oos_rank=("oos_rank", "mean"))
    say(ws.to_string(float_format=lambda x: f"{x:.3f}"))
    say(f"\n  reference OOS Sharpe: SPY {W.spy_OOS_Sharpe.mean():.3f} (panel-mean), "
        f"ungated control {W.ctl_OOS_Sharpe.mean():.3f}, RULES v1 {W.v1_OOS_Sharpe.mean():.3f}; "
        f"SPY OOS MaxDD {W.spy_OOS_MaxDD.mean():.3f}")
    s1, s2 = W[W.sel == "S1"], W[W.sel == "S2"]
    m = s1.merge(s2, on=["panel", "book", "cost"], suffixes=("_1", "_2"))
    both = m.dropna(subset=["OOS_Sharpe_1", "OOS_Sharpe_2"])
    say(f"  S1 vs S2 head-to-head on the {len(both)} cells where both pick: "
        f"S2 (no floor) OOS-better in {int((both.OOS_Sharpe_2 > both.OOS_Sharpe_1).sum())}, "
        f"S1 better in {int((both.OOS_Sharpe_1 > both.OOS_Sharpe_2).sum())}, "
        f"identical pick in {int((both.pick_1 == both.pick_2).sum())};  "
        f"mean OOS Sharpe S1 {both.OOS_Sharpe_1.mean():.3f} vs S2 {both.OOS_Sharpe_2.mean():.3f}"
        f"  (delta {both.OOS_Sharpe_2.mean()-both.OOS_Sharpe_1.mean():+.3f})")
    say(f"  cells where the floor empties the admitted set entirely: S1 {int((s1['pick']=='(none)').sum())} "
        f"of 18 vs S2 {int((s2['pick']=='(none)').sum())} of 18")

    # ---------------------------------------------------------------- 4a
    say("\n" + "=" * 200)
    say("KEEP PATH 4a (beat the live book) on the same corpus")
    say(f"  4a passes {int(G.pass4a.sum())} of {len(G)} ({G.pass4a.mean():.1%});  "
        f"of the {int(P.floor_only.sum())} Pareto-best floor-only KILLs, "
        f"{int(P[P.floor_only].pass4a.sum())} pass 4a")
    say(f"  arms passing BOTH 4a and 4b: {int((G.pass4a & G.pass4b).sum())};  "
        f"4a but not 4b: {int((G.pass4a & ~G.pass4b).sum())};  4b but not 4a: "
        f"{int((~G.pass4a & G.pass4b).sum())}")

    # ---------------------------------------------------------------- E leaderboard census
    say("\n" + "=" * 200)
    say("E  LEADERBOARD.md CENSUS — INDICATIVE ONLY (mixed samples/universes/costs, no OOS column)")
    LB = leaderboard_census()
    say(f"  parseable numeric rows: {len(LB)} of {len((ROOT/'research'/'LEADERBOARD.md').read_text().splitlines())} lines")
    for ref, nm in ((SPYREF["u56"], "u56 SPY"), (SPYREF["broad"], "broad SPY")):
        ok_dd = LB.MaxDD.abs() <= DELTA0 * abs(ref["sdd"])
        ok_c = LB.CAGR >= PHI0 * ref["scagr"]
        LB["_p"] = pareto_front(LB)
        pf = LB[LB._p]
        say(f"  vs {nm} (CAGR {ref['scagr']:.2%}, MaxDD {ref['sdd']:.2%}): "
            f"rows meeting DD cap {int(ok_dd.sum())}, meeting CAGR floor {int(ok_c.sum())}, "
            f"both {int((ok_dd & ok_c).sum())};  killed by the floor alone "
            f"{int((ok_dd & ~ok_c).sum())} ({(ok_dd & ~ok_c).mean():.1%} of all rows)")
        say(f"     among the {len(pf)} Pareto-best published rows: floor-only KILLs "
            f"{int((ok_dd & ~ok_c)[pf.index].sum())}")

    # ---------------------------------------------------------------- outputs
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    L.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
    GRID.to_csv(OUT / f"{STEM}.calibration.csv", index=False)
    Q.to_csv(OUT / f"{STEM}.riskwork.csv", index=False)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"\nwrote {STEM}.{{grid,ladder,calibration,riskwork,walkforward}}.csv and .console.txt")


if __name__ == "__main__":
    main()
