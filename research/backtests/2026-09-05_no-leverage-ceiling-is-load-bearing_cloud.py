#!/usr/bin/env python3
"""QUEUE idea 148 — the-no-leverage-ceiling-is-load-bearing  (research sprint, cloud, 2026-09-05)

QUESTION (pre-registered, from QUEUE.md idea 148)
    Idea 144 adopted the convention that a static rescaling of a book is the SAME book, so a
    book passes 4b iff SOME point of its own gross family clears every bar (FAMILY-4b).  That
    family is not unbounded: PROTOCOL rule 2 says NO LEVERAGE, which under idea 144's
    parameterisation is a ceiling on the static multiplier m.  Idea 144 ran that ceiling as an
    arm at m_max in {1.00, 1.30} and found it binds in 54 of 306 books and moves the CAGR
    floor's UNIQUE exclusions from 51 to 37 — i.e. a construction constraint is silently doing
    part of the adequacy bar's job.

    Idea 148 sweeps the ceiling itself:

      Q0  Reproduce idea 144 exactly (harness, published row, m=1.00 census, and BOTH of the
          two claims this idea is built on) before any new number is read.
      Q1  Sweep the ceiling c over 0.75x .. 1.3333x of the 75% target gross (c = 1.3333 is
          exactly 100% gross = the true no-leverage boundary; nothing above it is legal).
          Report FAMILY-4b and FAMILY-4a pass counts at EVERY c.
      Q2  THE QUESTION: how many 4b verdicts are decided by the CEILING rather than by either
          bar?  Partition all 306 books at each c into
             bar-pass      passes at c and at every legal c            (ceiling irrelevant)
             ceiling-KILL  fails at c, passes at the legal ceiling     (the ceiling decided it)
             bar-KILL      fails at every legal c                      (a bar decided it)
      Q3  For the ceiling-KILLs, WHICH bar is failing at m = c?  (If it is always the CAGR
          floor, the ceiling and the floor are one constraint seen from two sides.)
      Q4  Does the ceiling stay load-bearing across the bar grid?  Cross the ceiling sweep with
          the two tuned bar coefficients and report every grid point.
      Q5  Rule 8 walk-forward: choose on 2009-2016, evaluate 2017-2026 untouched.  Does a
          higher ceiling select better OOS, or does it only let the screen buy gross (idea 146
          found the screen's m-move buys -0.003 Sharpe)?  Report OOS CAGR/Sharpe/MaxDD against
          RULES v1 and SPY at every ceiling, plus the m-pinned and no-screen controls.

    A finding of "the ceiling decides nothing" is a KILL of idea 148's premise and is reported
    as such.  Rule 7: nothing is tuned until it works; every grid point is printed.

TUNED PARAMETERS — exactly two (the bar coefficients, as in ideas 131/144)
    phi    CAGR floor   in {0.00, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00}   (0.70 published)
    delta  MaxDD cap    in {0.40, 0.50, 0.60, 0.70, 0.80, 1.00}         (0.60 published)
    The CEILING c is NOT a tuned parameter: it is the constraint under adjudication and is
    swept exhaustively with every point reported, exactly as idea 144 swept m.

CORPUS (nothing new is invented; idea 144's corpus verbatim)
    3 panels (u56, broad, small) x 3 books (V1u, TOP20, EWall) x 17 arms x 2 cost rungs
    = 306 books.  Weekly, t+1, 75% target gross at m=1.00, 10 and 25 bps.
    IS <= 2016-12-31, OOS >= 2017-01-01.
    GROSS FAMILY: m in {0.10, 0.15, ..., 1.30} + {1.3333} = 26 points.  1.3333 is added by
    this run because it, not 1.30, is where PROTOCOL rule 2 actually bites.
    306 x 26 = 7,956 backtests.

CAVEATS carried, not buried
    - SURVIVORSHIP: all three panels are current-constituent lists (idea 54).  The small panel
      is data/prices_small.csv with the 44 tickers whose max 1-day move >= 1.0 dropped
      (439 names retained of 483), and it excludes every name that delisted or was acquired,
      a one-directional upward bias that falls hardest on beaten-down names.
    - Idea 128: the IS window's SPY MaxDD (-22.1%) is shallower than the OOS window's
      (-33.7%), so every IS drawdown cap admits too much gross.  This biases Q5 uniformly.
    - Idea 38: u56/broad are on a calendar-day index (weekend rows ffilled).
    - The `ebud` arms take an ABSOLUTE turnover budget, so m changes how hard the budget bites;
      they are not pure exposure rescales (idea 144 Q1).  Reported by kind, never averaged away.
    - run() caps realised gross at 1.00 inside the loop, so no arm can lever even if m would.

REUSE
    build_frame() is exposed so a later script can adjudicate the SAME 7,956 rows rather than
    re-deriving them; it caches to <STEM>.family.csv.gz.
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

STEM = "2026-09-05_no-leverage-ceiling-is-load-bearing_cloud"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"

_spec = importlib.util.spec_from_file_location("i94", I94)
H = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(H)

FREQ, GROSS, PCOST = H.FREQ, H.GROSS, H.PCOST
IS_END, OOS_START = H.IS_END, H.OOS_START
COSTS = [10.0, 25.0]
BOOKS = H.BOOKS
PANELS = ["u56", "broad", "small"]

MLEG = 1.3333                                                    # 1.3333 x 0.75 = 1.00 gross
MGRID = [round(x, 4) for x in np.arange(0.10, 1.3001, 0.05)] + [MLEG]
CEILS = [round(x, 4) for x in np.arange(0.75, 1.3001, 0.05)] + [MLEG]

PHIS = [0.00, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]                # tuned param 1
DELTAS = [0.40, 0.50, 0.60, 0.70, 0.80, 1.00]                    # tuned param 2
PHI0, DELTA0 = 0.70, 0.60                                        # published

BARS5 = ("H1", "H2", "OOS", "DD", "CAGR")
BARS_IS = ("H1", "H2", "DD", "CAGR")
NBOOK = 306

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 3000)

LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ------------------------------------------------------------------ panels (idea 144 verbatim)
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


def stats_of(r, which):
    w = H.window(r, which) if which != "full" else r
    m = metrics(w)
    h1, h2 = H.halves(w)
    oos = metrics(r.loc[OOS_START:])["Sharpe"] if which == "full" else m["Sharpe"]
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2, OOS_Sharpe=oos)


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


# ------------------------------------------------------------------ the frame
def build_frame(cache=True, verbose=True):
    """306 books x 26 gross points.  Cached to <STEM>.family.csv.gz."""
    cpath = OUT / f"{STEM}.family.csv.gz"
    bpath = OUT / f"{STEM}.bars.csv"
    if cache and cpath.exists() and bpath.exists():
        F = pd.read_csv(cpath)
        B = pd.read_csv(bpath)
        bars = {r.panel: (dict(s1=r.s1, s2=r.s2, sdd=r.sdd, scagr=r.scagr, soos=r.soos),
                          dict(s1=r.i_s1, s2=r.i_s2, sdd=r.i_sdd, scagr=r.i_scagr, soos=r.i_soos))
                for r in B.itertuples()}
        return F, bars

    FR, bars = [], {}
    for pname in PANELS:
        px, spy, desc = panel(pname)
        start = px.index[260]
        spy = spy.loc[start:]
        bfull, bIS = bars_win(spy, "full"), bars_win(spy, "IS")
        bars[pname] = (bfull, bIS)
        if verbose:
            say(f"\n--- PANEL {pname}: {desc} | {px.index[0].date()} -> {px.index[-1].date()} | "
                f"eval from {start.date()}")
            say(f"    SPY full CAGR {bfull['scagr']:.2%}  Sharpe {metrics(spy)['Sharpe']:.3f}  "
                f"MaxDD {bfull['sdd']:.2%}  halves {bfull['s1']:.3f}/{bfull['s2']:.3f}  "
                f"OOS Sharpe {bfull['soos']:.3f}")
            say(f"    published bars: CAGR floor {PHI0*bfull['scagr']:.2%}/yr   "
                f"DD cap {-DELTA0*abs(bfull['sdd']):.2%}   |   IS SPY CAGR {bIS['scagr']:.2%}  "
                f"MaxDD {bIS['sdd']:.2%}")
        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        for book in BOOKS:
            for arm, kind, kw, (gate, conv) in H.arm_specs():
                W = H.targets(px, book, gate, conv)          # computed once per (book, arm)
                for cost in COSTS:
                    for m_ in MGRID:
                        res = H.run(px, W, m=m_, bps=cost, **kw)
                        r = res["r"].loc[start:]
                        g = res["gross"].loc[start:]
                        sf, si = stats_of(r, "full"), stats_of(r, "IS")
                        so = metrics(H.window(r, "OOS"))
                        FR.append(dict(
                            panel=pname, book=book, cost=cost, arm=arm, kind=kind, m=m_,
                            CAGR=sf["CAGR"], Sharpe=sf["Sharpe"], MaxDD=sf["MaxDD"],
                            H1=sf["H1"], H2=sf["H2"], OOS_Sharpe_full=sf["OOS_Sharpe"],
                            IS_CAGR=si["CAGR"], IS_Sharpe=si["Sharpe"], IS_MaxDD=si["MaxDD"],
                            IS_H1=si["H1"], IS_H2=si["H2"],
                            OOS_CAGR=so["CAGR"], OOS_Sharpe=so["Sharpe"], OOS_MaxDD=so["MaxDD"],
                            gross=float(g.mean()), pass4a=H.pass4a(r, v1[cost]),
                            TO=float(res["to"].loc[start:].sum() / (len(r) / 252))))
            if verbose:
                say(f"    {pname}/{book}: {len(FR)} rows")
    F = pd.DataFrame(FR)
    F["book_id"] = F.panel + "|" + F.book + "|" + F.cost.astype(str) + "|" + F.arm
    for key, idx in (("b_s1", "s1"), ("b_s2", "s2"), ("b_soos", "soos"),
                     ("b_sdd", "sdd"), ("b_scagr", "scagr")):
        F[key] = F.panel.map({p: bars[p][0][idx] for p in bars})
    for key, idx in (("bi_s1", "s1"), ("bi_s2", "s2"), ("bi_sdd", "sdd"), ("bi_scagr", "scagr")):
        F[key] = F.panel.map({p: bars[p][1][idx] for p in bars})
    if cache:
        F.to_csv(cpath, index=False, compression="gzip")
        pd.DataFrame([dict(panel=p, **bars[p][0],
                           **{f"i_{k}": v for k, v in bars[p][1].items()}) for p in PANELS]
                     ).to_csv(bpath, index=False)
    return F, bars


# ------------------------------------------------------------------ verdicts
def bar_ok(D, phi, delta, which="full"):
    if which == "full":
        return pd.DataFrame(dict(
            H1=D.H1 - D.b_s1 > 0, H2=D.H2 - D.b_s2 > 0,
            OOS=D.OOS_Sharpe_full - D.b_soos > 0,
            DD=delta * D.b_sdd.abs() - D.MaxDD.abs() > 0,
            CAGR=D.CAGR - phi * D.b_scagr > 0), index=D.index)
    return pd.DataFrame(dict(
        H1=D.IS_H1 - D.bi_s1 > 0, H2=D.IS_H2 - D.bi_s2 > 0,
        OOS=pd.Series(True, index=D.index),
        DD=delta * D.bi_sdd.abs() - D.IS_MaxDD.abs() > 0,
        CAGR=D.IS_CAGR - phi * D.bi_scagr > 0), index=D.index)


def family_pass(F, phi, delta, ceil_, drop=None, which="full", extra=None):
    """Series indexed by book_id: True iff SOME m <= ceil_ clears every (kept) bar."""
    keys = [k for k in (BARS5 if which == "full" else BARS_IS) if k != drop]
    sub = F[F.m <= ceil_ + 1e-9]
    ok = bar_ok(sub, phi, delta, which)[keys].all(axis=1)
    if extra is not None:
        ok = ok & extra.loc[sub.index]
    return ok.groupby(sub.book_id).any()


def family_ms(F, phi, delta, ceil_, which="full"):
    """Per book: admissible m's under the ceiling (lo, hi, count)."""
    keys = list(BARS5 if which == "full" else BARS_IS)
    sub = F[F.m <= ceil_ + 1e-9]
    ok = bar_ok(sub, phi, delta, which)[keys].all(axis=1)
    d = pd.DataFrame(dict(book_id=sub.book_id.values, m=sub.m.values, ok=ok.values))
    g = d[d.ok].groupby("book_id").m
    ids = sub.book_id.drop_duplicates().values
    return pd.DataFrame(dict(m_lo=g.min(), m_hi=g.max(), n_m=g.count())).reindex(ids)


# ------------------------------------------------------------------ rule 8
def rule8(F, ceil_, mode, phi=PHI0, delta=DELTA0):
    """Per (panel, book, cost) cell: choose ONE (arm, m) on the IS window, evaluate OOS.

    mode 'none'   unscreened IS-Sharpe argmax over m <= ceil_
    mode 'pin'    m forced to 1.00, IS-4b-admissible arms only, IS-Sharpe argmax (idea 146)
    mode 'family' IS-4b-admissible (arm, m) with m <= ceil_, IS-Sharpe argmax
    Empty screens fall back to the unscreened argmax of the same m-set (explicit, per idea 132).
    """
    picks = []
    for (p, b, c), D in F.groupby(["panel", "book", "cost"], sort=False):
        sub = D[D.m <= ceil_ + 1e-9] if mode != "pin" else D[np.isclose(D.m, 1.00)]
        if mode == "none":
            cand = sub
            screened = False
        else:
            ok = bar_ok(sub, phi, delta, "IS")[list(BARS_IS)].all(axis=1)
            cand = sub[ok.values]
            screened = len(cand) > 0
            if not screened:
                cand = sub
        row = cand.loc[cand.IS_Sharpe.idxmax()]
        picks.append(dict(panel=p, book=b, cost=c, mode=mode, ceil=ceil_, screened=screened,
                          n_adm=int(len(cand)) if screened else 0,
                          arm=row.arm, m=row.m, IS_Sharpe=row.IS_Sharpe,
                          OOS_CAGR=row.OOS_CAGR, OOS_Sharpe=row.OOS_Sharpe,
                          OOS_MaxDD=row.OOS_MaxDD, gross=row.gross))
    return pd.DataFrame(picks)


def main():
    say("=" * 200)
    say("IDEA 148 — the-no-leverage-ceiling-is-load-bearing.  Under adjudication: PROTOCOL "
        "rule 2's no-leverage clause as a 4b bar in disguise.")
    say(f"corpus = 3 panels x 3 books x 17 arms x 2 costs = {NBOOK} BOOKS; gross family = "
        f"{len(MGRID)} points m in [{MGRID[0]}, {MGRID[-1]}] -> {NBOOK*len(MGRID)} backtests")
    say(f"ceiling sweep c = {CEILS}   (c x 75% = realised target gross; c={MLEG} is exactly "
        f"100% gross = PROTOCOL rule 2's boundary)")
    say(f"IS <= {IS_END}   OOS >= {OOS_START}   weekly, t+1, costs {COSTS} bps.  "
        f"Published bars: CAGR >= {PHI0} x SPY, MaxDD <= {DELTA0} x |SPY|.")
    say("=" * 200)

    F, bars = build_frame()
    say(f"\nfull frame: {len(F)} rows over {F.book_id.nunique()} books "
        f"({'from cache' if len(LOG) < 8 else 'freshly computed'})")

    # ============================================================ Q0 reproduction
    say("\n" + "=" * 200)
    say("Q0  REPRODUCTION CHECKS — all must pass before any new number is read")
    px56, spy56, _ = panel("u56")
    s56 = px56.index[260]
    ew = H.targets(px56, "EWall")
    a = H.run(px56, ew, bps=PCOST)["r"].loc[s56:]
    b = backtest(px56, ew, cost_bps=PCOST, freq=FREQ)["returns"].loc[s56:]
    d_ab = float((a - b).abs().max())
    say(f"  (a) H.run vs engine.backtest, ungated EWall u56: max|diff| = {d_ab:.3e}  -> "
        f"{'PASS' if d_ab < 1e-12 else 'FAIL'}")

    P = F[np.isclose(F.m, 1.00)].copy()
    pub = P[(P.panel == "u56") & (P.book == "EWall") & (P.arm == "vol60-dg") & (P.cost == 10.0)]
    r0 = pub.iloc[0]
    say(f"  (b) idea 94's published EWall+vol60-dg u56@10bps row: "
        f"{r0.CAGR:.3%} / {r0.Sharpe:.3f} / {r0.MaxDD:.3%}  "
        f"(published 11.587% / 1.133 / -16.884%)  -> "
        f"{'PASS' if abs(r0.CAGR-0.11587)<2e-4 and abs(r0.Sharpe-1.133)<2e-3 else 'CHECK'}")

    ok5 = bar_ok(P, PHI0, DELTA0)[list(BARS5)].all(axis=1)
    ok_nofloor = bar_ok(P, PHI0, DELTA0)[[k for k in BARS5 if k != "CAGR"]].all(axis=1)
    P["front"] = pareto_front(P)
    say(f"  (c) idea 131/129 POINT census at m=1.00: rows {len(P)} (306), "
        f"pass4b {int(ok5.sum())} (29), floor-only KILL {int((ok_nofloor & ~ok5).sum())} (27), "
        f"Pareto {int(P.front.sum())} (82), pass4a {int(P.pass4a.sum())}")

    # the two claims idea 148 is built on
    fm130 = family_ms(F, PHI0, DELTA0, 1.30)
    binds_hi = int((fm130.m_hi >= 1.30 - 1e-9).sum())
    fam130 = family_pass(F, PHI0, DELTA0, 1.30)
    fam100 = family_pass(F, PHI0, DELTA0, 1.00)
    nf130 = family_pass(F, PHI0, DELTA0, 1.30, drop="CAGR")
    nf100 = family_pass(F, PHI0, DELTA0, 1.00, drop="CAGR")
    fo130 = int((nf130 & ~fam130).sum())
    fo100 = int((nf100 & ~fam100).sum())
    say(f"  (d) idea 144's claim 1 — 'the m<=1.30 ceiling binds in 54 of 306 books': "
        f"books whose admissible set reaches the ceiling = {binds_hi}; "
        f"books whose FAMILY verdict differs between c=1.00 and c=1.30 = "
        f"{int((fam130 != fam100).sum())}; "
        f"books whose family-Sharpe argmax sits at m=1.30 = "
        f"{int((F[F.m <= 1.3001].loc[F[F.m <= 1.3001].groupby('book_id').Sharpe.idxmax()].m >= 1.2999).sum())}")
    say(f"  (e) idea 144's claim 2 — floor's UNIQUE exclusions 51 (c=1.00) -> 37 (c=1.30): "
        f"got {fo100} -> {fo130}")

    # ============================================================ Q1 the ceiling sweep
    say("\n" + "=" * 200)
    say("Q1  CEILING SWEEP at the published bars (phi=0.70, delta=0.60).  Every point reported.")
    fam_by_c, ms_by_c = {}, {}
    rows = []
    for c in CEILS:
        fam = family_pass(F, PHI0, DELTA0, c)
        fa = F[F.m <= c + 1e-9].groupby("book_id").pass4a.any()
        nf = family_pass(F, PHI0, DELTA0, c, drop="CAGR")
        nd = family_pass(F, PHI0, DELTA0, c, drop="DD")
        ms = family_ms(F, PHI0, DELTA0, c)
        fam_by_c[c], ms_by_c[c] = fam, ms
        rows.append(dict(ceil=c, target_gross=round(c * GROSS, 4),
                         pass4b=int(fam.sum()), pass4a=int(fa.sum()),
                         pass_both=int((fam & fa).sum()),
                         floor_unique_KILL=int((nf & ~fam).sum()),
                         cap_unique_KILL=int((nd & ~fam).sum()),
                         mean_n_m=float(ms.n_m.mean(skipna=True)),
                         reach_ceiling=int((ms.m_hi >= c - 1e-9).sum())))
    Q1 = pd.DataFrame(rows)
    say(Q1.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ============================================================ Q2 the question
    say("\n" + "=" * 200)
    say("Q2  HOW MANY 4b VERDICTS ARE DECIDED BY THE CEILING RATHER THAN BY EITHER BAR?")
    say("    Reference = the LEGAL ceiling c=1.3333 (100% gross).  A book is")
    say("      bar-pass      : passes at c AND at the legal ceiling            (ceiling irrelevant)")
    say("      ceiling-KILL  : fails at c, passes at the legal ceiling         (the CEILING decided it)")
    say("      bar-KILL      : fails at every legal c                           (a BAR decided it)")
    ref = fam_by_c[MLEG]
    rows = []
    for c in CEILS:
        fam = fam_by_c[c]
        rows.append(dict(ceil=c, target_gross=round(c * GROSS, 4),
                         bar_pass=int((fam & ref).sum()),
                         ceiling_KILL=int((~fam & ref).sum()),
                         bar_KILL=int((~ref).sum()),
                         pct_ceiling_decided=100.0 * float((~fam & ref).sum()) / NBOOK))
    Q2 = pd.DataFrame(rows)
    say(Q2.to_string(index=False, float_format=lambda x: f"{x:.2f}"))
    ever = pd.concat([fam_by_c[c].rename(c) for c in CEILS], axis=1)
    n_flip = int((ever.any(axis=1) & ~ever.all(axis=1)).sum())
    n_always = int(ever.all(axis=1).sum())
    n_never = int((~ever.any(axis=1)).sum())
    say(f"\n  Over the WHOLE legal ceiling range 0.75 -> {MLEG}: "
        f"{n_always} books pass at every ceiling (bar-decided PASS), "
        f"{n_flip} change verdict somewhere (CEILING-DECIDED), "
        f"{n_never} pass at no ceiling (bar-decided KILL).   "
        f"{n_flip}/{NBOOK} = {100*n_flip/NBOOK:.1f}% of all 4b verdicts are ceiling-decided.")
    say(f"  At the PUBLISHED ceiling of idea 144 (c=1.30) against the legal one ({MLEG}): "
        f"{int((~fam_by_c[1.30] & ref).sum())} verdicts differ.")

    # ============================================================ Q3 which bar binds at the ceiling
    say("\n" + "=" * 200)
    say("Q3  FOR THE CEILING-KILLs, WHICH BAR FAILS AT m = c?  (the ceiling can only ever be "
        "binding through a bar that RELAXES as gross rises)")
    rows = []
    for c in CEILS:
        fam = fam_by_c[c]
        vic = fam.index[(~fam & ref).values]
        sub = F[(F.book_id.isin(vic)) & (F.m <= c + 1e-9)]
        if len(sub) == 0:
            rows.append(dict(ceil=c, n=0))
            continue
        top = sub.loc[sub.groupby("book_id").m.idxmax()]        # the ceiling point itself
        B = bar_ok(top, PHI0, DELTA0)
        rows.append(dict(ceil=c, n=len(top),
                         **{f"fail_{k}": int((~B[k]).sum()) for k in BARS5},
                         only_CAGR=int(((~B.CAGR) & B.H1 & B.H2 & B.OOS & B.DD).sum())))
    Q3 = pd.DataFrame(rows).fillna(0)
    say(Q3.to_string(index=False))
    say("  (a bar that TIGHTENS with gross — the DD cap — cannot be relieved by a higher "
        "ceiling; any non-zero count in fail_DD is a book whose admissible window lies BELOW c "
        "and is therefore not ceiling-decided at all.)")

    # ============================================================ Q4 ceiling x bar grid
    say("\n" + "=" * 200)
    say(f"Q4  DOES THE CEILING STAY LOAD-BEARING ACROSS THE BAR GRID?  "
        f"{len(PHIS)} phi x {len(DELTAS)} delta x {len(CEILS)} ceilings = "
        f"{len(PHIS)*len(DELTAS)*len(CEILS)} verdict sets, every one reported.")
    rows = []
    for phi in PHIS:
        for delta in DELTAS:
            refg = family_pass(F, phi, delta, MLEG)
            for c in CEILS:
                fam = family_pass(F, phi, delta, c)
                rows.append(dict(phi=phi, delta=delta, ceil=c, pass4b=int(fam.sum()),
                                 ceiling_KILL=int((~fam & refg).sum())))
    Q4 = pd.DataFrame(rows)
    piv = Q4.pivot_table(index=["phi", "delta"], columns="ceil", values="ceiling_KILL")
    say("\n  ceiling-decided KILL count, by (phi, delta) x ceiling:")
    say(piv.to_string())
    piv2 = Q4.pivot_table(index=["phi", "delta"], columns="ceil", values="pass4b")
    say("\n  FAMILY-4b pass count, by (phi, delta) x ceiling:")
    say(piv2.to_string())
    at_pub = Q4[(Q4.phi == PHI0) & (Q4.delta == DELTA0) & (np.isclose(Q4.ceil, 1.30))]
    say(f"\n  published bars, published ceiling 1.30: pass4b {int(at_pub.pass4b.iloc[0])}, "
        f"ceiling-decided KILLs {int(at_pub.ceiling_KILL.iloc[0])}")
    say(f"  ceiling-decided KILLs at c=1.30 range over the 42-point bar grid: "
        f"{int(Q4[np.isclose(Q4.ceil,1.30)].ceiling_KILL.min())} .. "
        f"{int(Q4[np.isclose(Q4.ceil,1.30)].ceiling_KILL.max())}  "
        f"(median {Q4[np.isclose(Q4.ceil,1.30)].ceiling_KILL.median():.0f})")

    # ============================================================ Q5 rule 8
    say("\n" + "=" * 200)
    say("Q5  RULE 8 WALK-FORWARD — choose on 2009-2016, evaluate 2017-2026 untouched.")
    say("    18 cells (3 panels x 3 books x 2 costs).  Equal-weighted across cells; the PAIRED "
        "reading (same cells for every arm) is the one that counts.")
    WF = []
    WF.append(rule8(F, MLEG, "none"))
    WF.append(rule8(F, 1.00, "pin"))
    for c in CEILS:
        WF.append(rule8(F, c, "family"))
    WF = pd.concat(WF, ignore_index=True)

    # SPY / RULES v1 OOS references, equal-weighted over the same 18 cells
    ref_rows = []
    for pname in PANELS:
        px, spy, _ = panel(pname)
        start = px.index[260]
        spy = spy.loc[start:]
        sm = metrics(H.window(spy, "OOS"))
        for book in BOOKS:
            for c in COSTS:
                v1 = backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
                vm = metrics(H.window(v1, "OOS"))
                ref_rows.append(dict(panel=pname, book=book, cost=c,
                                     SPY_CAGR=sm["CAGR"], SPY_Sharpe=sm["Sharpe"], SPY_MaxDD=sm["MaxDD"],
                                     V1_CAGR=vm["CAGR"], V1_Sharpe=vm["Sharpe"], V1_MaxDD=vm["MaxDD"]))
    R = pd.DataFrame(ref_rows)
    say(f"\n  OOS references, equal-weighted over the 18 cells: "
        f"SPY {R.SPY_CAGR.mean():.2%}/{R.SPY_Sharpe.mean():.3f}/{R.SPY_MaxDD.mean():.2%}   "
        f"RULES v1 {R.V1_CAGR.mean():.2%}/{R.V1_Sharpe.mean():.3f}/{R.V1_MaxDD.mean():.2%}")

    agg = (WF.groupby(["mode", "ceil"])
             .agg(OOS_CAGR=("OOS_CAGR", "mean"), OOS_Sharpe=("OOS_Sharpe", "mean"),
                  OOS_MaxDD=("OOS_MaxDD", "mean"), mean_m=("m", "mean"),
                  mean_gross=("gross", "mean"), cells_screened=("screened", "sum"))
             .reset_index())
    agg["vs_SPY_Sharpe"] = agg.OOS_Sharpe - R.SPY_Sharpe.mean()
    agg["vs_V1_Sharpe"] = agg.OOS_Sharpe - R.V1_Sharpe.mean()
    say("\n  " + "-" * 150)
    say(agg.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    base_none = WF[WF["mode"] == "none"].set_index(["panel", "book", "cost"])
    base_pin = WF[WF["mode"] == "pin"].set_index(["panel", "book", "cost"])
    say("\n  PAIRED against the no-screen control and the m-pinned screen (per cell, 18 cells):")
    prows = []
    for c in CEILS:
        f_ = WF[(WF["mode"] == "family") & (np.isclose(WF.ceil, c))].set_index(["panel", "book", "cost"])
        j = f_.join(base_none[["OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD"]], rsuffix="_none")
        j = j.join(base_pin[["OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD"]], rsuffix="_pin")
        prows.append(dict(ceil=c,
                          d_Sharpe_vs_none=float((j.OOS_Sharpe - j.OOS_Sharpe_none).mean()),
                          n_better_none=int((j.OOS_Sharpe > j.OOS_Sharpe_none).sum()),
                          d_Sharpe_vs_pin=float((j.OOS_Sharpe - j.OOS_Sharpe_pin).mean()),
                          n_better_pin=int((j.OOS_Sharpe > j.OOS_Sharpe_pin).sum()),
                          d_CAGR_vs_pin=float((j.OOS_CAGR - j.OOS_CAGR_pin).mean()),
                          d_MaxDD_vs_pin=float((j.OOS_MaxDD.abs() - j.OOS_MaxDD_pin.abs()).mean()),
                          n_picks_moved=int(((j.arm != base_pin.arm) | (~np.isclose(j.m, base_pin.m))).sum())))
    Q5 = pd.DataFrame(prows)
    say(Q5.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ============================================================ verdict
    say("\n" + "=" * 200)
    say("VERDICT")
    ck130 = int((~fam_by_c[1.30] & ref).sum())
    say(f"  Q2 answer: {n_flip} of {NBOOK} 4b verdicts ({100*n_flip/NBOOK:.1f}%) are decided by "
        f"WHERE the ceiling is put rather than by either bar, over the legal range 0.75-{MLEG}.")
    say(f"  Idea 144's own published ceiling (1.30) is NOT the legal boundary ({MLEG} = 100% "
        f"gross); moving it to the boundary changes {ck130} verdicts.")
    say(f"  Q1: FAMILY-4b passes go {Q1.pass4b.iloc[0]} (c=0.75) -> {Q1.pass4b.iloc[-1]} "
        f"(c={MLEG}); the CAGR floor's unique exclusions go {Q1.floor_unique_KILL.iloc[0]} -> "
        f"{Q1.floor_unique_KILL.iloc[-1]}.")
    best = agg[agg["mode"] == "family"].sort_values("OOS_Sharpe", ascending=False).iloc[0]
    pin = agg[agg["mode"] == "pin"].iloc[0]
    none = agg[agg["mode"] == "none"].iloc[0]
    say(f"  Q5: best family ceiling OOS Sharpe {best.OOS_Sharpe:.3f} (c={best.ceil}) vs pinned "
        f"{pin.OOS_Sharpe:.3f} vs no-screen {none.OOS_Sharpe:.3f} vs SPY {R.SPY_Sharpe.mean():.3f} "
        f"vs RULES v1 {R.V1_Sharpe.mean():.3f}.")
    say("  NO NEW BOOK IS PROPOSED.  This run re-scores an existing corpus under a swept "
        "construction constraint, which is the thing being adjudicated.")

    # ============================================================ outputs
    P.to_csv(OUT / f"{STEM}.corpus.csv", index=False)
    Q1.to_csv(OUT / f"{STEM}.ceiling_sweep.csv", index=False)
    Q2.to_csv(OUT / f"{STEM}.ceiling_decided.csv", index=False)
    Q3.to_csv(OUT / f"{STEM}.binding_bar.csv", index=False)
    Q4.to_csv(OUT / f"{STEM}.bargrid.csv", index=False)
    Q5.to_csv(OUT / f"{STEM}.walkforward_paired.csv", index=False)
    WF.to_csv(OUT / f"{STEM}.picks.csv", index=False)
    agg.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    pd.concat([ms_by_c[c].assign(ceil=c) for c in CEILS]).to_csv(
        OUT / f"{STEM}.admissible_m.csv")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    say("\nwrote: .corpus.csv .ceiling_sweep.csv .ceiling_decided.csv .binding_bar.csv "
        ".bargrid.csv .walkforward.csv .walkforward_paired.csv .picks.csv .admissible_m.csv "
        ".family.csv.gz .console.txt")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
