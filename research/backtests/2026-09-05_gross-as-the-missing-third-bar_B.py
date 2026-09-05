#!/usr/bin/env python3
"""QUEUE idea 131 — gross-as-the-missing-third-bar  (research sprint lane B, 2026-09-05)

QUESTION (pre-registered, from QUEUE.md idea 131)
    Idea 129 established two things about PROTOCOL 4b's CAGR floor (CAGR >= phi x SPY CAGR,
    phi = 0.70):
      (i) it is the SOLE cause of KILL for 48% of arms clearing 4b's other four bars
          (27/56 corpus, 11/23 Pareto-best), and its victims are OOS-BETTER on Sharpe
          (+0.104) and 8.1 pp SHALLOWER on drawdown;
      (ii) it is nevertheless NOT broken, because on the static-gross ladder — pure
          de-risking with zero Sharpe content — it is the sole KILL in 97 of 342 rows and
          bites only at gross multipliers m <= 0.80.

    So the floor is doing ONE useful job (excluding a lever that just turns exposure down)
    with an instrument that also throws away differently-shaped defensive books.  Idea 129's
    closing diagnosis was that "the floor's real content is a gross-level filter".  The
    pre-registered test of that diagnosis:

      Q1  Does replacing the CAGR floor with an explicit MINIMUM MEAN GROSS bar
          (mean gross >= gamma) ADMIT the 11 Pareto-best defensive arm-rows the floor kills?
      Q2  Does the same gross bar STILL EXCLUDE the low-gross ladder points — the control
          that says a replacement bar is not simply "no bar at all"?
      Q3  Are the two bars substitutes at all?  Confusion matrix and rank association between
          mean gross and the CAGR margin, computed SEPARATELY on the arm corpus and on the
          ladder (they are one family only if the association holds in both).
      Q4  Rule 8: as a PROSPECTIVE screen read on 2009-2016 alone, does a gross-bar 4b select
          better out-of-sample than the CAGR-floor 4b, than no screen, and than no bar?

    A result of "the gross bar cannot do both jobs at once" is a KILL of the idea and is
    reported as such.  Rule 7: no bar is tuned until it works; the whole grid is printed.

HARNESS
    Idea 94's script (`2026-09-04_drawdown-insurance-price-list_B.py`) is IMPORTED, and idea
    129's corpus construction is reproduced EXACTLY, so this run's rows are the same rows the
    question is asked about.  Four reproduction checks run before any new number is read:
      (a) ungated EWall u56 via H.run vs engine.backtest — must be exact;
      (b) idea 94's published EWall+vol60-dg u56 @10bps row (11.6% / 1.133 / -16.9%);
      (c) idea 129's published census: 306 rows, 82 Pareto, 29 pass 4b, 27 floor-only,
          11 of 23 on the frontier, 97 of 342 ladder rows floor-only and all at m <= 0.80;
      (d) idea 129's IS-screen groups A=45 / B=9 / C=252.

CORPUS (nothing new is invented)
    3 panels (u56, broad, small) x 3 books (V1u, TOP20, EWall) x 17 arms x 2 costs
    = 306 arm-rows, plus the 19-point static-gross ladder per cell = 342 reference rows.
    Weekly, t+1 execution, 75% target gross, 10 and 25 bps, IS <= 2016-12-31, OOS >= 2017.

TUNED PARAMETERS — exactly two, both the bar coefficients being compared
    gamma  mean-gross floor    in {0.00, 0.30, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75}
    phi    CAGR floor          in {0.00, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00}   (0.70 published)
    delta (MaxDD cap) is HELD at its published 0.60 — not a third tuned dial.
    All 70 grid points are reported.  Books, gates, dials, gross, cadence, cost rungs and
    window boundaries are inherited unchanged from ideas 94/129.

BOTH KEEP PATHS are evaluated on every corpus row (4a via H.pass4a against RULES v1 on the
same panel and cost; 4b under each of the three bar-sets).

CAVEATS carried, not buried
    - Survivorship: all three panels are current-constituent lists (idea 54).  Absent
      delistings inflate every arm's CAGR and inflate the UNGATED (high-gross) books most, so
      a CAGR floor is flattered and a gross floor is not; stated, not corrected.
    - Idea 128: the IS window (SPY MaxDD -22.1%) is shallower than the OOS window (-33.7%),
      so any IS drawdown cap admits too much.  This biases every selector here the same way.
    - Idea 38: u56/broad still carry the calendar-day index.
    - Idea 126: every number is at t+1 execution only; no lag band is claimed.
    - Mean gross is measured on the SAME window the bar is applied to (full sample for the
      adoption question, IS window for the rule-8 screen).  It is directly observable
      prospectively, which is the one structural advantage it has over a CAGR floor.
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

STEM = "2026-09-05_gross-as-the-missing-third-bar_B"
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

GAMMAS = [0.00, 0.30, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]  # tuned param 1
PHIS = [0.00, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]                       # tuned param 2
PHI0, DELTA0, GAMMA0 = 0.70, 0.60, 0.50   # published floor, published cap, QUEUE's own gamma

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 1200)

LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ------------------------------------------------------------------ panels (idea 97/118 verbatim)
_PCACHE = {}


def panel(name):
    if name not in _PCACHE:
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


# ------------------------------------------------------------------ the three bar-sets
def bars_win(spy, which):
    if which == "full":
        s1, s2 = H.halves(spy)
        m = metrics(spy)
        return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"],
                    soos=metrics(spy.loc[OOS_START:])["Sharpe"])
    w = H.window(spy, which)
    s1, s2 = H.halves(w)
    m = metrics(w)
    return dict(s1=s1, s2=s2, sdd=m["MaxDD"], scagr=m["CAGR"], soos=m["Sharpe"])


def margins_at(r, g, b, phi, delta, gamma, which="full"):
    """4b's bars with BOTH candidate floors exposed.  `g` is the mean-gross series over the
    same window.  The three bar-sets are then:
        FLOOR  = H1,H2,OOS,DD,CAGR                 (PROTOCOL as published)
        GROSS  = H1,H2,OOS,DD,GROSS                (the CAGR floor swapped out)
        NEITHER= H1,H2,OOS,DD                      (no return/exposure adequacy bar)
    """
    w = H.window(r, which)
    gw = H.window(g, which) if which != "full" else g
    h1, h2 = H.halves(w)
    m = metrics(w)
    soos = metrics(r.loc[OOS_START:])["Sharpe"] if which == "full" else m["Sharpe"]
    return dict(H1=h1 - b["s1"], H2=h2 - b["s2"], OOS=soos - b["soos"],
                DD=delta * abs(b["sdd"]) - abs(m["MaxDD"]),
                CAGR=m["CAGR"] - phi * b["scagr"],
                GROSS=float(gw.mean()) - gamma)


CORE = ("H1", "H2", "OOS", "DD")


def verdict(mg, bar):
    """bar in {'floor','gross','neither'} -> (passes, list-of-failing-bars)."""
    keys = CORE + (("CAGR",) if bar == "floor" else ("GROSS",) if bar == "gross" else ())
    f = [k for k in keys if mg[k] <= 0]
    return (len(f) == 0), f


def pareto_front(df, s="Sharpe", d="MaxDD"):
    S, D = df[s].values, df[d].values
    out = np.ones(len(df), dtype=bool)
    for i in range(len(df)):
        if not np.isfinite(S[i]) or not np.isfinite(D[i]):
            out[i] = False
            continue
        dom = (S >= S[i]) & (D >= D[i]) & ((S > S[i]) | (D > D[i]))
        out[i] = not dom.any()
    return out


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return np.nan
    ra = pd.Series(a[ok]).rank().values
    rb = pd.Series(b[ok]).rank().values
    return float(np.corrcoef(ra, rb)[0, 1])


def welch(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    x, y = x[np.isfinite(x)], y[np.isfinite(y)]
    if len(x) < 2 or len(y) < 2:
        return np.nan, np.nan
    d = x.mean() - y.mean()
    se = np.sqrt(x.var(ddof=1) / len(x) + y.var(ddof=1) / len(y))
    return d, (d / se if se > 0 else np.nan)


# ------------------------------------------------------------------ one (panel, book, cost) cell
def do_cell(pname, px, spy, book, cost, bfull, bIS, v1_net):
    rows, rets, grs = [], {}, {}
    for arm, kind, kw, (gate, conv) in H.arm_specs():
        W = H.targets(px, book, gate, conv)
        res = H.run(px, W, bps=cost, **kw)
        r = res["r"].loc[spy.index[0]:]
        g = res["gross"].loc[spy.index[0]:]
        rets[arm], grs[arm] = r, g
        m, mi, mo = metrics(r), metrics(H.window(r, "IS")), metrics(H.window(r, "OOS"))
        mg = margins_at(r, g, bfull, PHI0, DELTA0, GAMMA0, "full")
        mgi = margins_at(r, g, bIS, PHI0, DELTA0, GAMMA0, "IS")
        p_fl, f_fl = verdict(mg, "floor")
        p_gr, f_gr = verdict(mg, "gross")
        p_ne, f_ne = verdict(mg, "neither")
        rows.append(dict(
            panel=pname, book=book, cost=cost, arm=arm, kind=kind,
            CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
            H1=H.halves(r)[0], H2=H.halves(r)[1],
            IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
            OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
            m_H1=mg["H1"], m_H2=mg["H2"], m_OOS=mg["OOS"], m_DD=mg["DD"],
            m_CAGR=mg["CAGR"], m_GROSS=mg["GROSS"],
            IS_m_H1=mgi["H1"], IS_m_H2=mgi["H2"], IS_m_DD=mgi["DD"],
            IS_m_CAGR=mgi["CAGR"], IS_m_GROSS=mgi["GROSS"],
            pass4b_floor=p_fl, fail_floor=",".join(f_fl) or "-",
            pass4b_gross=p_gr, fail_gross=",".join(f_gr) or "-",
            pass4b_neither=p_ne,
            floor_only=(f_fl == ["CAGR"]), gross_only=(f_gr == ["GROSS"]),
            pass4a=H.pass4a(r, v1_net),
            gross=float(g.mean()), IS_gross=float(H.window(g, "IS").mean()),
            OOS_gross=float(H.window(g, "OOS").mean()),
            gross_sd=float(g.std()), gross_cv=float(g.std() / g.mean()) if g.mean() > 0 else np.nan,
            TO=float(res["to"].loc[spy.index[0]:].sum() / (len(r) / 252)),
        ))
    D = pd.DataFrame(rows)
    D["pareto"] = pareto_front(D)
    return D, rets, grs


def ladder_cell(pname, px, spy, book, cost, bfull):
    W = H.targets(px, book)
    rows = []
    for m_ in LADDER:
        res = H.run(px, W, m=m_, bps=cost)
        r = res["r"].loc[spy.index[0]:]
        g = res["gross"].loc[spy.index[0]:]
        mm = metrics(r)
        mg = margins_at(r, g, bfull, PHI0, DELTA0, GAMMA0, "full")
        p_fl, f_fl = verdict(mg, "floor")
        p_gr, f_gr = verdict(mg, "gross")
        p_ne, _ = verdict(mg, "neither")
        rows.append(dict(panel=pname, book=book, cost=cost, m=float(m_),
                         CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                         gross=float(g.mean()), gross_sd=float(g.std()),
                         gross_cv=float(g.std() / g.mean()) if g.mean() > 0 else np.nan,
                         m_CAGR=mg["CAGR"], m_GROSS=mg["GROSS"],
                         pass4b_floor=p_fl, fail_floor=",".join(f_fl) or "-",
                         pass4b_gross=p_gr, fail_gross=",".join(f_gr) or "-",
                         pass4b_neither=p_ne,
                         floor_only=(f_fl == ["CAGR"]), gross_only=(f_gr == ["GROSS"])))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ walk-forward (rule 8)
def walk_forward(sub, RET, bIS, spy, v1_net, key, gamma):
    """Selectors read the IS WINDOW ONLY, then the pick is read once on 2017-2026.
       S0  no screen                     argmax IS Sharpe over all 17 arms
       S1  IS-4b with the CAGR floor     (phi=0.70, delta=0.60)
       S2  IS-4b with neither floor      (phi=0.00, delta=0.60)
       S3  IS-4b with the GROSS bar      (gamma, delta=0.60), CAGR floor deleted
    """
    def core(row):
        return all(row[f"IS_m_{k}"] > 0 for k in ("H1", "H2", "DD"))

    cand = {
        "S0": sub,
        "S1": sub[sub.apply(lambda r: core(r) and r["IS_CAGR"] - PHI0 * bIS["scagr"] > 0, axis=1)],
        "S2": sub[sub.apply(core, axis=1)],
        "S3": sub[sub.apply(lambda r: core(r) and r["IS_gross"] - gamma > 0, axis=1)],
    }
    ctl = RET["control"]
    mc = metrics(H.window(ctl, "OOS"))
    ms = metrics(spy.loc[OOS_START:])
    mv = metrics(H.window(v1_net, "OOS"))
    order = sub.OOS_Sharpe.rank(ascending=False)
    best = sub.loc[sub.OOS_Sharpe.idxmax(), "arm"]
    out = []
    for s, c in cand.items():
        base = dict(sel=s, gamma=gamma, panel=key[0], book=key[1], cost=key[2],
                    ctl_OOS_Sharpe=mc["Sharpe"], spy_OOS_Sharpe=ms["Sharpe"],
                    v1_OOS_Sharpe=mv["Sharpe"], ctl_OOS_MaxDD=mc["MaxDD"],
                    spy_OOS_MaxDD=ms["MaxDD"], spy_OOS_CAGR=ms["CAGR"])
        if len(c) == 0:
            out.append(dict(base, pick="(none)", n_admitted=0, OOS_CAGR=np.nan,
                            OOS_Sharpe=np.nan, OOS_MaxDD=np.nan, beat_ctl=np.nan,
                            beat_spy=np.nan, beat_v1=np.nan, oos_best=np.nan, oos_rank=np.nan))
            continue
        p = c.loc[c.IS_Sharpe.idxmax()]
        r = H.window(RET[p["arm"]], "OOS")
        m = metrics(r)
        out.append(dict(base, pick=p["arm"], n_admitted=len(c), OOS_CAGR=m["CAGR"],
                        OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"],
                        beat_ctl=bool(m["Sharpe"] > mc["Sharpe"]),
                        beat_spy=bool(m["Sharpe"] > ms["Sharpe"]),
                        beat_v1=bool(m["Sharpe"] > mv["Sharpe"]),
                        oos_best=bool(p["arm"] == best), oos_rank=float(order.loc[p.name])))
    return pd.DataFrame(out)


# ------------------------------------------------------------------ main
def main():
    say("=" * 200)
    say(f"IDEA 131 — can a MINIMUM MEAN GROSS bar replace 4b's CAGR floor?   corpus = 3 panels "
        f"x 3 books x 17 arms x 2 costs = {3*3*17*2} arm-rows; ladder = {3*3*len(LADDER)*2} reference rows")
    say(f"IS <= {IS_END}   OOS >= {OOS_START}   t+1, weekly, {GROSS:.0%} target gross, costs "
        f"{COSTS} bps.  Published bars: CAGR >= {PHI0} x SPY, MaxDD <= {DELTA0} x |SPY|.  "
        f"Candidate: mean gross >= {GAMMA0:.2f}.")
    say("=" * 200)

    GR, LD, RET, GRS, WF = [], [], {}, {}, []
    V1, SPY = {}, {}
    BARS = {}
    for pname in PANELS:
        px, spy, desc = panel(pname)
        start = px.index[260]
        spy = spy.loc[start:]
        SPY[pname] = spy
        bfull, bIS = bars_win(spy, "full"), bars_win(spy, "IS")
        BARS[pname] = (bfull, bIS)
        say(f"\n--- PANEL {pname}: {desc} | {px.index[0].date()} -> {px.index[-1].date()} | eval from {start.date()}")
        say(f"    SPY full CAGR {bfull['scagr']:.2%}  Sharpe {metrics(spy)['Sharpe']:.3f}  "
            f"MaxDD {bfull['sdd']:.2%}  halves {bfull['s1']:.3f}/{bfull['s2']:.3f}  OOS Sharpe {bfull['soos']:.3f}")
        say(f"    bars: CAGR floor {PHI0*bfull['scagr']:.2%}/yr   DD cap {-DELTA0*abs(bfull['sdd']):.2%}   "
            f"gross floor {GAMMA0:.2f} of a {GROSS:.2f} target book")
        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        V1[pname] = v1
        for book in BOOKS:
            for c in COSTS:
                D, rets, grs = do_cell(pname, px, spy, book, c, bfull, bIS, v1[c])
                GR.append(D)
                RET[(pname, book, c)] = rets
                GRS[(pname, book, c)] = grs
                LD.append(ladder_cell(pname, px, spy, book, c, bfull))
        say(f"    ... {pname} done")

    G = pd.concat(GR, ignore_index=True)
    L = pd.concat(LD, ignore_index=True)

    # ---------------------------------------------------------------- reproduction checks
    say("\n" + "=" * 200)
    say("REPRODUCTION CHECKS (all four must pass before any new number is read)")
    px56, spy56, _ = panel("u56")
    s56 = px56.index[260]
    ew = H.targets(px56, "EWall")
    a = H.run(px56, ew, bps=PCOST)["r"].loc[s56:]
    b = backtest(px56, ew, cost_bps=PCOST, freq=FREQ)["returns"].loc[s56:]
    d_ab = float((a - b).abs().max())
    say(f"  (a) H.run vs engine.backtest, ungated EWall u56: max|diff| = {d_ab:.2e} -> "
        f"{'PASS' if d_ab < 1e-12 else 'FAIL'}")
    pub = G[(G.panel == "u56") & (G.book == "EWall") & (G.cost == 10.0) & (G.arm == "vol60-dg")].iloc[0]
    ok_b = abs(pub.CAGR - 0.116) < 5e-4 and abs(pub.Sharpe - 1.133) < 5e-3 and abs(pub.MaxDD + 0.169) < 5e-4
    say(f"  (b) idea 94 published EWall+vol60-dg u56@10bps 11.6%/1.133/-16.9%: got "
        f"{pub.CAGR:.3%}/{pub.Sharpe:.3f}/{pub.MaxDD:.3%} -> {'PASS' if ok_b else 'FAIL'}")
    P = G[G.pareto]
    c129 = dict(rows=len(G), pareto=int(G.pareto.sum()), pass4b=int(G.pass4b_floor.sum()),
                floor_only=int(G.floor_only.sum()),
                p_floor_only=int(P.floor_only.sum()),
                p_clear4=int((P.floor_only | P.pass4b_floor).sum()),
                lad_rows=len(L), lad_floor_only=int(L.floor_only.sum()),
                lad_max_m=float(L.loc[L.floor_only, "m"].max()) if L.floor_only.any() else np.nan)
    tgt = dict(rows=306, pareto=82, pass4b=29, floor_only=27, p_floor_only=11, p_clear4=23,
               lad_rows=342, lad_floor_only=97, lad_max_m=0.80)
    ok_c = all(abs(c129[k] - tgt[k]) < 1e-9 for k in tgt)
    say(f"  (c) idea 129 census reproduced: {c129}")
    say(f"      target                    : {tgt}  -> {'PASS' if ok_c else 'FAIL'}")
    # (d) idea 129's IS-screen groups A/B/C
    def is_ok(row, phi):
        return all(row[f"IS_m_{k}"] > 0 for k in ("H1", "H2", "DD")) and row["IS_m_CAGR"] > 0 if phi else \
            all(row[f"IS_m_{k}"] > 0 for k in ("H1", "H2", "DD"))
    A = G[G.apply(lambda r: is_ok(r, 1), axis=1)]
    B = G[G.apply(lambda r: is_ok(r, 0) and not is_ok(r, 1), axis=1)]
    C = G[~G.apply(lambda r: is_ok(r, 0), axis=1)]
    ok_d = (len(A), len(B), len(C)) == (45, 9, 252)
    say(f"  (d) idea 129 IS-screen groups A/B/C = {len(A)}/{len(B)}/{len(C)}  (target 45/9/252) "
        f"-> {'PASS' if ok_d else 'FAIL'}")
    say(f"  ALL CHECKS: {'PASS' if (d_ab < 1e-12 and ok_b and ok_c and ok_d) else 'SEE ABOVE'}")

    # ---------------------------------------------------------------- Q1 the swap on the corpus
    say("\n" + "=" * 200)
    say(f"Q1  DOES A GROSS BAR (mean gross >= {GAMMA0:.2f}) ADMIT THE 11 PARETO-BEST DEFENSIVE ARMS?")
    say("=" * 200)
    say(f"  corpus {len(G)} rows;  pass 4b-FLOOR {int(G.pass4b_floor.sum())}   "
        f"pass 4b-GROSS {int(G.pass4b_gross.sum())}   pass 4b-NEITHER {int(G.pass4b_neither.sum())}")
    v = G[G.floor_only]
    say(f"\n  The floor's exclusive victims (fail 4b on CAGR alone): n = {len(v)}, "
        f"of which Pareto-best {int(v.pareto.sum())}")
    say(f"    admitted by the gross bar at gamma={GAMMA0:.2f}: {int(v.pass4b_gross.sum())} of {len(v)}"
        f"   (Pareto-best: {int(v[v.pareto].pass4b_gross.sum())} of {int(v.pareto.sum())})")
    say(f"    their mean gross: {v.gross.mean():.3f}  [min {v.gross.min():.3f}, max {v.gross.max():.3f}]")
    cols = ["panel", "book", "cost", "arm", "CAGR", "Sharpe", "MaxDD", "OOS_Sharpe", "OOS_MaxDD",
            "gross", "m_CAGR", "m_GROSS", "pass4b_gross", "pass4a", "pareto"]
    say("\n  every floor-only victim (the rows 4b calls a KILL and 4a does not):")
    say(v.sort_values(["pareto", "Sharpe"], ascending=False)[cols].to_string(
        index=False, float_format=lambda x: f"{x:.3f}"))

    say(f"\n  Rows the SWAP costs (pass 4b-FLOOR but fail 4b-GROSS at gamma={GAMMA0:.2f}):")
    lost = G[G.pass4b_floor & ~G.pass4b_gross]
    say(f"    n = {len(lost)}" + ("" if len(lost) == 0 else ""))
    if len(lost):
        say(lost[cols].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---------------------------------------------------------------- Q2 the ladder control
    say("\n" + "=" * 200)
    say("Q2  DOES THE GROSS BAR STILL EXCLUDE THE LOW-GROSS LADDER (the pure de-risking control)?")
    say("=" * 200)
    say(f"  ladder {len(L)} rows;  pass 4b-FLOOR {int(L.pass4b_floor.sum())}   "
        f"pass 4b-GROSS {int(L.pass4b_gross.sum())}   pass 4b-NEITHER {int(L.pass4b_neither.sum())}")
    say(f"  sole-KILL by the CAGR floor: {int(L.floor_only.sum())} rows, all at m <= "
        f"{L.loc[L.floor_only,'m'].max():.2f}")
    say(f"  sole-KILL by the GROSS bar : {int(L.gross_only.sum())} rows, all at m <= "
        f"{L.loc[L.gross_only,'m'].max():.2f}" if L.gross_only.any() else
        f"  sole-KILL by the GROSS bar : 0 rows")
    lad_new = L[L.pass4b_gross & ~L.pass4b_floor]
    say(f"\n  LADDER POINTS THE SWAP LETS IN (pass 4b-GROSS, fail 4b-FLOOR): n = {len(lad_new)}")
    if len(lad_new):
        say(lad_new[["panel", "book", "cost", "m", "CAGR", "Sharpe", "MaxDD", "gross",
                     "m_CAGR", "m_GROSS"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say("\n  ladder pass-counts by m (how far down the de-grossing lever each bar reaches):")
    lm = L.groupby("m").agg(n=("m", "size"), pass_floor=("pass4b_floor", "sum"),
                            pass_gross=("pass4b_gross", "sum"),
                            pass_neither=("pass4b_neither", "sum"),
                            mean_gross=("gross", "mean"), mean_CAGR=("CAGR", "mean"),
                            mean_Sharpe=("Sharpe", "mean"))
    say(lm.to_string(float_format=lambda x: f"{x:.3f}"))

    # ---------------------------------------------------------------- Q2b the separation curve
    say("\n" + "=" * 200)
    say("Q2b  IS THERE ANY gamma THAT DOES BOTH JOBS?  (the decisive table for idea 131)")
    say("     admit the floor's victims  AND  exclude every ladder point the core four bars admit")
    say("=" * 200)
    vic = G[G.floor_only]                       # the 27 rows the CAGR floor alone kills
    ladc = L[L.pass4b_neither]                  # ladder points the core four bars admit
    say(f"  floor's exclusive victims: n={len(vic)} (Pareto {int(vic.pareto.sum())}), "
        f"mean gross min {vic.gross.min():.4f} / median {vic.gross.median():.4f} / max {vic.gross.max():.4f}")
    say(f"  core-admissible ladder pts: n={len(ladc)}, mean gross min {ladc.gross.min():.4f} / "
        f"median {ladc.gross.median():.4f} / max {ladc.gross.max():.4f}")
    sep = vic.gross.min() > ladc.gross.max()
    say(f"  SEPARABLE ON GROSS?  min(victim gross) {vic.gross.min():.4f} > max(ladder gross) "
        f"{ladc.gross.max():.4f} ?  -> {'YES' if sep else 'NO — the two families OVERLAP'}")
    ov = ladc[ladc.gross > vic.gross.min()]
    say(f"  overlap region [{vic.gross.min():.4f}, {ladc.gross.max():.4f}] contains "
        f"{int((vic.gross <= ladc.gross.max()).sum())} of {len(vic)} victims and {len(ov)} ladder points")
    say("\n  fine sweep — every gamma from 0.45 to 0.78 in steps of 0.01:")
    fine = []
    for gm in np.round(np.arange(0.45, 0.781, 0.01), 2):
        va = int((vic.gross > gm).sum())
        pa = int((vic[vic.pareto].gross > gm).sum())
        la = int((ladc.gross > gm).sum())
        fine.append(dict(gamma=float(gm), victims_admitted=va, of=len(vic),
                         pareto_victims_admitted=pa, ladder_admitted=la,
                         corpus_pass4b_gross=int(((G.m_H1 > 0) & (G.m_H2 > 0) & (G.m_OOS > 0)
                                                  & (G.m_DD > 0) & (G.gross > gm)).sum())))
    FINE = pd.DataFrame(fine)
    say(FINE.to_string(index=False))
    both = FINE[(FINE.victims_admitted == len(vic)) & (FINE.ladder_admitted == 0)]
    say(f"\n  gammas achieving BOTH (all {len(vic)} victims admitted AND 0 ladder points): "
        f"{len(both)} of {len(FINE)} grid points -> "
        f"{'FOUND' if len(both) else 'NONE EXIST — the swap cannot do both jobs'}")
    bestp = FINE[FINE.ladder_admitted == 0]
    if len(bestp):
        r0 = bestp.iloc[0]
        say(f"  the tightest gamma that empties the ladder is {r0.gamma:.2f}; there it admits "
            f"{int(r0.victims_admitted)} of {len(vic)} victims and {int(r0.pareto_victims_admitted)} "
            f"of {int(vic.pareto.sum())} Pareto-best ones.")
    r1 = FINE[FINE.victims_admitted == len(vic)]
    if len(r1):
        rr = r1.iloc[-1]
        say(f"  the tightest gamma that keeps every victim is {rr.gamma:.2f}; there "
            f"{int(rr.ladder_admitted)} ladder points are still admitted "
            f"(the CAGR floor admits {int(L.pass4b_floor.sum())}).")
    FINE.to_csv(OUT / f"{STEM}.separation.csv", index=False)

    say("\n  DIAGNOSTIC (descriptive only — NOT a tuned third bar): the ladder holds gross CONSTANT")
    say("  by construction while a de-grossing gate makes it TIME-VARYING.  Gross dispersion:")
    say(f"    floor's victims        cv(gross) mean {vic.gross_cv.mean():.4f}  "
        f"[min {vic.gross_cv.min():.4f}, max {vic.gross_cv.max():.4f}]")
    say(f"    core-admissible ladder cv(gross) mean {ladc.gross_cv.mean():.4f}  "
        f"[min {ladc.gross_cv.min():.4f}, max {ladc.gross_cv.max():.4f}]")
    sep2 = vic.gross_cv.min() > ladc.gross_cv.max()
    say(f"    SEPARABLE ON cv(gross)?  min(victim) {vic.gross_cv.min():.4f} > max(ladder) "
        f"{ladc.gross_cv.max():.4f} ?  -> {'YES — complete separation' if sep2 else 'NO'}")
    say("    No threshold is fitted here and no verdict rests on it; it is reported so the "
        "next queue idea can pre-register it.")

    # ---------------------------------------------------------------- Q3 are they substitutes?
    say("\n" + "=" * 200)
    say("Q3  ARE THE TWO BARS SUBSTITUTES?  (association must hold on BOTH families, not one)")
    say("=" * 200)
    for nm, DF in (("arm corpus", G), ("static-gross ladder", L)):
        rho = spearman(DF.gross, DF.CAGR)
        rho_m = spearman(DF.m_GROSS, DF.m_CAGR)
        say(f"  {nm:22s} n={len(DF):4d}   Spearman(mean gross, CAGR) = {rho:+.3f}   "
            f"Spearman(gross margin, CAGR margin) = {rho_m:+.3f}")
    say("")
    ct = pd.crosstab(G.pass4b_floor, G.pass4b_gross)
    say("  corpus confusion (rows: pass 4b-FLOOR, cols: pass 4b-GROSS)\n" + ct.to_string())
    ctl_ = pd.crosstab(L.pass4b_floor, L.pass4b_gross)
    say("\n  ladder confusion (rows: pass 4b-FLOOR, cols: pass 4b-GROSS)\n" + ctl_.to_string())
    agree_c = float((G.pass4b_floor == G.pass4b_gross).mean())
    agree_l = float((L.pass4b_floor == L.pass4b_gross).mean())
    say(f"\n  verdict agreement: corpus {agree_c:.1%}   ladder {agree_l:.1%}")

    say("\n  OOS quality of what each bar-set admits (full-sample bars, read on 2017-2026):")
    qrows = []
    for nm, msk in (("4b-FLOOR (published)", G.pass4b_floor), (f"4b-GROSS g={GAMMA0:.2f}", G.pass4b_gross),
                    ("4b-NEITHER", G.pass4b_neither)):
        s = G[msk]
        qrows.append(dict(bar=nm, n=len(s), OOS_Sharpe=s.OOS_Sharpe.mean(), OOS_MaxDD=s.OOS_MaxDD.mean(),
                          OOS_CAGR=s.OOS_CAGR.mean(), gross=s.gross.mean(), pass4a=int(s.pass4a.sum())))
    say(pd.DataFrame(qrows).to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---------------------------------------------------------------- the 70-point grid
    say("\n" + "=" * 200)
    say("CALIBRATION GRID — all 70 points (delta held at its published 0.60).")
    say("  left block: n admitted by 4b-GROSS at each gamma (the CAGR floor deleted)")
    say("  right block: n admitted by 4b-FLOOR at each phi (gamma irrelevant) — idea 129's column")
    say("=" * 200)
    grid = []
    for gm in GAMMAS:
        for ph in PHIS:
            gcol, ccol = G.gross.values, G.CAGR.values
            core_ok = (G.m_H1 > 0) & (G.m_H2 > 0) & (G.m_OOS > 0) & (G.m_DD > 0)
            scg = np.array([BARS[p][0]["scagr"] for p in G.panel])
            pg = core_ok & (gcol - gm > 0)
            pf = core_ok & (ccol - ph * scg > 0)
            pb = pg & pf
            grid.append(dict(gamma=gm, phi=ph, n_gross=int(pg.sum()), n_floor=int(pf.sum()),
                             n_both=int(pb.sum()),
                             adm_gross_OOS_Sharpe=G.OOS_Sharpe[pg].mean(),
                             adm_gross_OOS_MaxDD=G.OOS_MaxDD[pg].mean(),
                             adm_gross_OOS_CAGR=G.OOS_CAGR[pg].mean(),
                             adm_floor_OOS_Sharpe=G.OOS_Sharpe[pf].mean(),
                             adm_floor_OOS_MaxDD=G.OOS_MaxDD[pf].mean(),
                             adm_floor_OOS_CAGR=G.OOS_CAGR[pf].mean()))
    GRID = pd.DataFrame(grid)
    piv = GRID.pivot_table(index="gamma", columns="phi", values="n_both")
    say("  n admitted with BOTH bars applied (gamma down, phi across):\n" + piv.to_string())
    say("\n  gross bar alone, by gamma (phi deleted):")
    say(GRID[GRID.phi == 0.0][["gamma", "n_gross", "adm_gross_OOS_Sharpe", "adm_gross_OOS_MaxDD",
                               "adm_gross_OOS_CAGR"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say("\n  CAGR floor alone, by phi (gamma deleted) — reproduces idea 129's delta=0.60 column:")
    say(GRID[GRID.gamma == 0.0][["phi", "n_floor", "adm_floor_OOS_Sharpe", "adm_floor_OOS_MaxDD",
                                 "adm_floor_OOS_CAGR"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # the same grid on the ladder — the bar must kill the lever at every point it is adopted
    lgrid = []
    for gm in GAMMAS:
        for ph in PHIS:
            core_ok = (L.pass4b_neither)
            scg = np.array([BARS[p][0]["scagr"] for p in L.panel])
            pg = core_ok & (L.gross.values - gm > 0)
            pf = core_ok & (L.CAGR.values - ph * scg > 0)
            lgrid.append(dict(gamma=gm, phi=ph, lad_gross=int(pg.sum()), lad_floor=int(pf.sum()),
                              lad_gross_max_m=float(L.m[pg].max()) if pg.any() else np.nan,
                              lad_gross_min_m=float(L.m[pg].min()) if pg.any() else np.nan,
                              lad_floor_min_m=float(L.m[pf].min()) if pf.any() else np.nan))
    LGRID = pd.DataFrame(lgrid)
    say("\n  LADDER admissions by bar (the control: a bar that admits low-m points is not doing the job)")
    say(LGRID[LGRID.phi == 0.0][["gamma", "lad_gross", "lad_gross_min_m"]].to_string(
        index=False, float_format=lambda x: f"{x:.3f}"))
    say(LGRID[LGRID.gamma == 0.0][["phi", "lad_floor", "lad_floor_min_m"]].to_string(
        index=False, float_format=lambda x: f"{x:.3f}"))

    # ---------------------------------------------------------------- Q4 rule-8 walk-forward
    say("\n" + "=" * 200)
    say("Q4  RULE 8 WALK-FORWARD — screens read 2009-2016 ONLY, picks read once on 2017-2026.")
    say("    S0 no screen | S1 IS-4b + CAGR floor (phi=0.70) | S2 IS-4b, no adequacy bar | "
        "S3 IS-4b + GROSS bar (gamma)")
    say("=" * 200)
    for key in RET:
        sub = G[(G.panel == key[0]) & (G.book == key[1]) & (G.cost == key[2])]
        for gm in GAMMAS:
            WF.append(walk_forward(sub, RET[key], BARS[key[0]][1], SPY[key[0]],
                                   V1[key[0]][key[2]], key, gm))
    W = pd.concat(WF, ignore_index=True)

    def wf_summary(w):
        rows = []
        for s, g_ in w.groupby(["sel", "gamma"]):
            picked = g_.dropna(subset=["OOS_Sharpe"])
            rows.append(dict(sel=s[0], gamma=s[1], cells=len(g_), picking=len(picked),
                             mean_admitted=g_.n_admitted.mean(),
                             OOS_CAGR=picked.OOS_CAGR.mean(), OOS_Sharpe=picked.OOS_Sharpe.mean(),
                             OOS_MaxDD=picked.OOS_MaxDD.mean(),
                             beat_spy=int(picked.beat_spy.sum()), beat_v1=int(picked.beat_v1.sum()),
                             beat_ctl=int(picked.beat_ctl.sum()),
                             oos_best=int(picked.oos_best.sum()),
                             mean_rank=picked.oos_rank.mean()))
        return pd.DataFrame(rows)

    S = wf_summary(W)
    say("  raw (each selector over its own picking cells — NOT comparable across selectors):")
    say(S[S.sel.isin(["S0", "S1", "S2"]) & (S.gamma == 0.0) | (S.sel == "S3")].to_string(
        index=False, float_format=lambda x: f"{x:.3f}"))

    # paired reading (idea 132's lesson: compare on the SAME cells or not at all)
    say("\n  PAIRED reading — S0/S1/S2/S3 restricted to the cells where S3 at each gamma picks:")
    prow = []
    for gm in GAMMAS:
        w3 = W[(W.sel == "S3") & (W.gamma == gm)]
        cells = set(map(tuple, w3.dropna(subset=["OOS_Sharpe"])[["panel", "book", "cost"]].values))
        if not cells:
            prow.append(dict(gamma=gm, cells=0))
            continue
        d = dict(gamma=gm, cells=len(cells))
        for s in ("S0", "S1", "S2", "S3"):
            ws = W[(W.sel == s) & (W.gamma == gm)]
            ws = ws[[tuple(x) in cells for x in ws[["panel", "book", "cost"]].values]]
            ws = ws.dropna(subset=["OOS_Sharpe"])
            d[f"{s}_n"] = len(ws)
            d[f"{s}_Sh"] = ws.OOS_Sharpe.mean()
            d[f"{s}_DD"] = ws.OOS_MaxDD.mean()
            d[f"{s}_CAGR"] = ws.OOS_CAGR.mean()
        prow.append(d)
    PAIR = pd.DataFrame(prow)
    say(PAIR.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    say("\n  how often does the GROSS bar change the pick relative to no screen (S0)?")
    mv = []
    for gm in GAMMAS:
        w0 = W[(W.sel == "S0") & (W.gamma == gm)].set_index(["panel", "book", "cost"]).pick
        w3 = W[(W.sel == "S3") & (W.gamma == gm)].set_index(["panel", "book", "cost"]).pick
        w1 = W[(W.sel == "S1") & (W.gamma == gm)].set_index(["panel", "book", "cost"]).pick
        both3 = (w3 != "(none)")
        both1 = (w1 != "(none)")
        mv.append(dict(gamma=gm, S3_cells=int(both3.sum()),
                       S3_moved=int(((w3 != w0) & both3).sum()),
                       S1_cells=int(both1.sum()),
                       S1_moved=int(((w1 != w0) & both1).sum())))
    say(pd.DataFrame(mv).to_string(index=False))

    ref = W[(W.sel == "S0") & (W.gamma == 0.0)].iloc[0]
    say(f"\n  reference OOS: SPY Sharpe {ref.spy_OOS_Sharpe:.3f} / MaxDD {ref.spy_OOS_MaxDD:.1%} / "
        f"CAGR {ref.spy_OOS_CAGR:.1%};  RULES v1 Sharpe {ref.v1_OOS_Sharpe:.3f}   "
        "(u56 reference row; per-cell values in the walkforward csv)")

    # ---------------------------------------------------------------- KEEP paths
    say("\n" + "=" * 200)
    say("BOTH KEEP PATHS on every corpus row")
    say("=" * 200)
    say(f"  4a (beat the book, vs RULES v1 same panel & cost): {int(G.pass4a.sum())} of {len(G)}")
    say(f"  4b published (CAGR floor)                        : {int(G.pass4b_floor.sum())} of {len(G)}")
    say(f"  4b with the gross bar at gamma={GAMMA0:.2f}                 : {int(G.pass4b_gross.sum())} of {len(G)}")
    say(f"  both 4a and 4b-floor {int((G.pass4a & G.pass4b_floor).sum())};  "
        f"both 4a and 4b-gross {int((G.pass4a & G.pass4b_gross).sum())}")
    newk = G[G.pass4b_gross & ~G.pass4b_floor]
    say(f"\n  NEW 4b passes created by the swap: {len(newk)} rows "
        f"(of which also 4a: {int(newk.pass4a.sum())})")
    if len(newk):
        say(newk.sort_values("Sharpe", ascending=False)[cols].to_string(
            index=False, float_format=lambda x: f"{x:.3f}"))
    say("\n  NO NEW BOOK IS PROPOSED BY THIS SCRIPT — it re-scores an existing corpus under an "
        "alternative bar.  Any row above is a KEEP-candidate only under the alternative bar, "
        "which is exactly what is being adjudicated.")

    # ---------------------------------------------------------------- outputs
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    L.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
    GRID.to_csv(OUT / f"{STEM}.calibration.csv", index=False)
    LGRID.to_csv(OUT / f"{STEM}.ladder_calibration.csv", index=False)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    PAIR.to_csv(OUT / f"{STEM}.paired.csv", index=False)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    say(f"\nwrote {STEM}.{{grid,ladder,calibration,ladder_calibration,walkforward,paired}}.csv "
        f"and .console.txt")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
