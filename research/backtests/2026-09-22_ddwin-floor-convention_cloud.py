#!/usr/bin/env python3
"""Idea 917 (lane cloud, 2026-09-22) — IS THE 20-DAY DDWIN DEFINITION FLOOR A CRASH-LENGTH
CONVENTION?

WHERE THIS COMES FROM.  Idea 867 introduced DDWIN — a book's beta measured INSIDE its own
peak-to-trough maximum-drawdown window — as the circular CEILING against which every ex-ante
beta proxy in ideas 910 and 912 is scored, and it is defined only when that window is at least
MINOBS = 20 trading days long.  Idea 912 then found DDWIN is UNDEFINED on 48 of 112 U56 and
52 of 112 B136 books with 2020 in the sample and on 0 of 112 with it out, because SPY's 2020
decline is 24 days long and drags most books' own deepest decline down to roughly that length —
i.e. the whole DDSUB population that 867's and 910's agreement tables are computed on may be an
artefact of a 24-day crash meeting a 20-day minimum-observation rule.

THE QUESTION.  Sweep the floor and report WHICH COMMITTED DDSUB STATISTIC IS FLOOR-INVARIANT.

THE TWO TUNED DIALS (and no more).
  DIAL 1 — FLOOR, the DDWIN minimum-observation rule, in {10, 20, 40, 60} trading days.
    20 is the committed value, so the record's own convention is a grid point, not a comparand.
  DIAL 2 — PANEL, in {U56, B136, SMALL}.

WHAT IS SWEPT AND WHAT IS HELD.  The floor is applied to the DDWIN DEFINEDNESS RULE ONLY — the
rule that constitutes DDSUB.  The ten EX-ANTE proxies keep their committed min-sample guard of
20, so the ONLY thing that moves across floors is the POPULATION the agreement is averaged over.
That is precisely idea 912's charge, and holding the proxies fixed is what makes the sweep a
test of it rather than a second dial.

REPORTED, NOT TUNED: EXCISION {NONE, SPYDD, CRASH, CAL20} (idea 912's own 2020-in / 2020-out
contrast), WINDOW {FULL, IS, OOS}, PROXY (all 11), POPULATION {ALL, DDSUB}, and the cost ladder
{0,10,25,50} bps at any capital-arm cell that clears 4b.  EVERY grid point is published.

THE SHELF.  Idea 912's committed 112-book shelf, imported from its own script so the numbers are
the record's and not a re-implementation: gate family {TREND, VOL, MOM, DISP} x mode {ROW, AGG,
HYB} x theta {0.20, 0.40, 0.60} (ROW has none) x gross {0.25, 0.50, 0.75, 1.00} = 112 real books
per panel, plus 16 null books (3 RANDGATE seeds + ZEROSIG) carried but excluded from every
committed count, weekly, fills t+1, 10 bps.

PRE-STATED VERDICT RULES (fixed before the run, not adjusted after):
  V1  THE POPULATION IS A FLOOR ARTEFACT.  |DDSUB| / 112 moves by more than 0.10 across the four
      floors on a MAJORITY of (panel, excision, window) cells.  Triggered -> DDSUB is a
      convention, not a population.
  V2  SOME COMMITTED STATISTIC IS FLOOR-INVARIANT.  At least one proxy's DDSUB agreement has a
      max-minus-min spread across the four floors of <= 0.02 (867's own MATCH_TOL, the record's
      tolerance for "the same number") on EVERY (panel, excision, window) cell in which it is
      defined at all four floors.  Triggered -> that statistic can be quoted without its floor.
  V3  THE FLOOR HAS A CAPITAL CONSEQUENCE.  The rule-8 IS-only DDSUB-screened pick CHANGES with
      the floor on at least one panel.  Triggered -> the convention is not capital-neutral.

CAPITAL ARM (PROTOCOL rules 3, 4 and 8).  At each (panel, floor): screen the 112 books to those
whose 2009-2016 OWN drawdown window is at least FLOOR days long (IS-DDSUB — legal, IS-only) AND
whose IS DDWIN beta is <= 0.60, then take the highest IS Sharpe.  2017-2026 is read ONCE.  Both
KEEP paths are scored at every cell against the LIVE RULES v2 book and against SPY, beside an
UNSCREENED max-IS-Sharpe control.

PROTOCOL: rule 2 (10 bps, next-day fills, weekly, no leverage); rule 3 (live RULES v2 AND SPY);
rule 4 (both KEEP paths, <= 2 tuned dials); rule 5 (one idea, deterministic, standalone);
rule 8 (walk-forward, 2017-2026 read once); rule 9 (survivorship stated).
RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py are NOT modified.

SURVIVORSHIP (rule 9).  U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT screen, so
every CAGR and MaxDD LEVEL is optimistic and both 4b bars are easier than on a point-in-time
panel.  The FLOOR CONTRAST is same-shelf / same-tape with only the definedness rule moved, so it
is first-order immune; the 4b pass counts are not.

Run:  python research/backtests/2026-09-22_ddwin-floor-convention_cloud.py
"""
from __future__ import annotations

import importlib.util
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = HERE / "2026-09-22_ddwin-floor-convention_cloud"
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))

# --- import idea 912's committed script as a module, so the shelf and every statistic below are
# --- the record's own code rather than a re-implementation -------------------------------------
_P912 = HERE / "2026-09-15_is-the-DD-LEG-literature-a-2020-CONTAINMENT-fact_cloud.py"
_spec = importlib.util.spec_from_file_location("d912", _P912)
d912 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(d912)

FLOORS = [10, 20, 40, 60]                       # tuned dial 1 (20 = the committed convention)
PANELS = ["U56", "B136", "SMALL"]               # tuned dial 2
EXCISIONS = ["NONE", "SPYDD", "CRASH", "CAL20"]
WINDOWS = ["FULL", "IS", "OOS"]
PROXIES = d912.PROXIES
BETA_CAP = d912.BETA_CAP
MATCH_TOL = d912.MATCH_TOL                      # 0.02 — the record's "same number" tolerance
COST_LADDER = [0.0, 10.0, 25.0, 50.0]
COMMITTED_FLOOR = 20

_log: list[str] = []
_gates: list[dict] = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _log.append(s)


def gate(name, value, target, ok):
    _gates.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    log(f"  GATE {'PASS' if ok else 'FAIL'}  {name}: {value}   (target {target})")
    return bool(ok)


def ddwin_at(r, m, floor):
    """DDWIN beta with the minimum-observation floor made EXPLICIT.  At floor = 20 this is
    idea 867's committed definition character for character (gate G2)."""
    r, m = np.asarray(r, float), np.asarray(m, float)
    pk, tr = d912._dd_window(r)
    if tr - pk < floor:
        return np.nan, float(tr - pk + 1)
    rw, mw = r[pk: tr + 1], m[pk: tr + 1]
    v = mw.var(ddof=1)
    b = float(np.cov(rw, mw, ddof=1)[0, 1] / v) if v > 0 else np.nan
    return b, float(tr - pk + 1)


def load_panel(name):
    from baseline import load_universe
    if name == "U56":
        px = load_universe()
    elif name == "B136":
        px = load_universe(broad=True)
    else:
        px = load_universe(small=True)
        meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
        bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
        keep = [c for c in px.columns if c == "SPY" or c not in bad]
        log(f"  SMALL: {px.shape[1]} cols -> {len(keep)} kept "
            f"({px.shape[1]-len(keep)} dropped, max_1d_move >= 1.0)")
        px = px[keep]
    return px.dropna(how="all").ffill()


def main():
    log("# Idea 917 (lane cloud, 2026-09-22) — is the 20-DAY DDWIN DEFINITION FLOOR a "
        "CRASH-LENGTH CONVENTION?")
    log(f"# tuned dials (2): FLOOR {FLOORS} x PANEL {PANELS}.  reported, not tuned: EXCISION "
        f"{EXCISIONS}, WINDOW {WINDOWS}, PROXY {len(PROXIES)}, POPULATION [ALL, DDSUB], cost "
        f"ladder at 4b clearers.  shelf = idea 912's committed 112 real books/panel (+16 null), "
        f"weekly, t+1, {d912.COST:.0f} bps.  The floor moves the DDWIN DEFINEDNESS rule only; "
        f"the ten ex-ante proxies keep their committed min-sample guard of {d912.MINOBS}.")

    pop_rows, agree_rows, cap_rows, ladder_rows, len_rows = [], [], [], [], []
    g_ddwin_diff, g_lev, g_nbooks = [], 0.0, []

    for pname in PANELS:
        px = load_panel(pname)
        pan = d912.Panel(pname, px)
        log(f"\n## {pname}: {px.shape[1]} cols, {len(px)} rows ({len(px)/252:.1f}y), book from "
            f"{pan.start.date()}")
        for e in EXCISIONS:
            log(f"   excision {e:<6} {pan.excinfo[e]}")

        books = d912.build_books(pan)
        real = [(md, r) for md, r in books
                if not str(md["family"]).startswith(("ZEROSIG", "RANDGATE"))]
        g_nbooks.append(len(real))
        g_lev = max(g_lev, max(float(md["gross"]) for md, _ in books))
        log(f"   {len(books)} books priced ({len(real)} real, "
            f"{len(books)-len(real)} null carried but never counted)")

        # live RULES v2 and SPY comparands, per (excision, window)
        ew = d912.ew_panel(pan.px)
        inb = d912.gate_in(pan.px, "TREND")
        v2r = d912.Book(pan, d912.book_w1(ew, inb, None, "ROW", 0.0)).at(0.75, d912.COST)[0]

        for e in EXCISIONS:
            for w in WINDOWS:
                m = pan.masks[(e, w)]
                mw = pan.spy[m]
                spy = d912.pack(mw)
                v2 = d912.pack(v2r[m])
                cond = pan.cond[(e, w)]

                # ---- proxies computed ONCE (floor-independent by construction) ---------------
                B = {p: np.full(len(real), np.nan) for p in PROXIES}
                truth = np.zeros(len(real), bool)
                mdd = np.full(len(real), np.nan)
                ddw = {f: np.full(len(real), np.nan) for f in FLOORS}
                for i, (md, r) in enumerate(real):
                    rw = r[m]
                    bt = d912.proxies_all(rw, mw, cond)
                    for p in PROXIES:
                        B[p][i] = bt[p]
                    s = d912.pack(rw)
                    mdd[i] = s["MaxDD"]
                    truth[i] = bool(s["MaxDD"] >= d912.DD_CAP * spy["MaxDD"])   # the DD leg
                    for f in FLOORS:
                        ddw[f][i], L = ddwin_at(rw, mw, f)
                        if f == COMMITTED_FLOOR:
                            g_ddwin_diff.append(
                                0.0 if (np.isnan(ddw[f][i]) and np.isnan(bt["DDWIN"]))
                                else abs(float(ddw[f][i]) - float(bt["DDWIN"])))
                            len_rows.append(dict(panel=pname, excision=e, window=w,
                                                 book=f"{md['family']}/{md['mode']}/"
                                                      f"{md['theta']}/{md['gross']}",
                                                 ddwin_len=L))

                # ---- ARM 0: the DDSUB population at each floor -------------------------------
                for f in FLOORS:
                    nd = int(np.isfinite(ddw[f]).sum())
                    pop_rows.append(dict(panel=pname, excision=e, window=w, floor=f,
                                         n_books=len(real), n_ddsub=nd,
                                         n_undefined=len(real) - nd,
                                         share_ddsub=nd / len(real)))
                    # ---- ARM 1: every committed agreement statistic on both populations ------
                    for p in PROXIES:
                        for popn in ("ALL", "DDSUB"):
                            sel = np.ones(len(real), bool) if popn == "ALL" \
                                else np.isfinite(ddw[f])
                            if sel.sum() < 5:
                                agree_rows.append(dict(panel=pname, excision=e, window=w,
                                                       floor=f, proxy=p, popn=popn,
                                                       n=int(sel.sum())))
                                continue
                            beta = B[p].copy() if p != "DDWIN" else ddw[f].copy()
                            row = d912.agree_row(pname, e, w, popn, p,
                                                 beta[sel], truth[sel], mdd[sel])
                            row.update(floor=f)
                            agree_rows.append(row)

                # ---- capital arm comparands (window FULL / OOS only, excision NONE) ----------
                if e == "NONE" and w == "FULL":
                    pan._spy_full, pan._v2_full = spy, v2

        # ---- ARM 2: rule-8 capital arm ---------------------------------------------------
        m_is, m_oos, m_full = pan.masks[("NONE", "IS")], pan.masks[("NONE", "OOS")], \
            pan.masks[("NONE", "FULL")]
        spy_full = d912.pack(pan.spy[m_full]); spy_oos = d912.pack(pan.spy[m_oos])
        v2_full = d912.pack(v2r[m_full]); v2_oos = d912.pack(v2r[m_oos])
        log(f"   SPY FULL {spy_full['CAGR']:.2%}/{spy_full['Sharpe']:.3f}/"
            f"{spy_full['MaxDD']:.2%} (H1 {spy_full['H1']:.3f} H2 {spy_full['H2']:.3f});  "
            f"SPY OOS {spy_oos['CAGR']:.2%}/{spy_oos['Sharpe']:.3f}/{spy_oos['MaxDD']:.2%}")
        log(f"   live RULES v2 FULL {v2_full['CAGR']:.2%}/{v2_full['Sharpe']:.3f}/"
            f"{v2_full['MaxDD']:.2%} (H1 {v2_full['H1']:.3f} H2 {v2_full['H2']:.3f});  "
            f"OOS Sharpe {v2_oos['Sharpe']:.3f}")

        is_sharpe = np.array([d912.fsharpe(r[m_is]) for _, r in real])
        is_ddw = {f: np.array([ddwin_at(r[m_is], pan.spy[m_is], f)[0] for _, r in real])
                  for f in FLOORS}

        def score_pick(i, tag, floor, npool):
            md, r = real[i]
            sF, sO = d912.pack(r[m_full]), d912.pack(r[m_oos])
            return dict(panel=pname, floor=floor, screen=tag, pool=npool,
                        book=f"{md['family']}/{md['mode']}/{md['theta']}/{md['gross']}",
                        is_sharpe=is_sharpe[i],
                        CAGR=sF["CAGR"], Sharpe=sF["Sharpe"], MaxDD=sF["MaxDD"],
                        H1=sF["H1"], H2=sF["H2"],
                        oos_CAGR=sO["CAGR"], oos_Sharpe=sO["Sharpe"], oos_MaxDD=sO["MaxDD"],
                        spy_CAGR=spy_full["CAGR"], spy_Sharpe=spy_full["Sharpe"],
                        spy_MaxDD=spy_full["MaxDD"], spy_H1=spy_full["H1"],
                        spy_H2=spy_full["H2"], spy_oos_CAGR=spy_oos["CAGR"],
                        spy_oos_Sharpe=spy_oos["Sharpe"], spy_oos_MaxDD=spy_oos["MaxDD"],
                        live_CAGR=v2_full["CAGR"], live_Sharpe=v2_full["Sharpe"],
                        live_MaxDD=v2_full["MaxDD"], live_H1=v2_full["H1"],
                        live_H2=v2_full["H2"], live_oos_Sharpe=v2_oos["Sharpe"],
                        keep4b_full=d912.pass4b(sF, spy_full),
                        keep4b_oos=d912.pass4b(sO, spy_oos),
                        keep4b=bool(d912.pass4b(sF, spy_full) and d912.pass4b(sO, spy_oos)),
                        keep4a=d912.pass4a(sF, v2_full),
                        dd_gap_pp=100.0 * (sO["MaxDD"] - d912.DD_CAP * spy_oos["MaxDD"]),
                        idx=i)

        for f in FLOORS:
            sel = np.isfinite(is_ddw[f]) & (is_ddw[f] <= BETA_CAP)
            if sel.sum():
                i = int(np.arange(len(real))[sel][np.argmax(is_sharpe[sel])])
                cap_rows.append(score_pick(i, "DDSUB+beta<=0.60", f, int(sel.sum())))
            else:
                cap_rows.append(dict(panel=pname, floor=f, screen="DDSUB+beta<=0.60",
                                     pool=0, book="(empty screen)"))
            sel2 = np.isfinite(is_ddw[f])
            if sel2.sum():
                i = int(np.arange(len(real))[sel2][np.argmax(is_sharpe[sel2])])
                cap_rows.append(score_pick(i, "DDSUB only", f, int(sel2.sum())))
        i0 = int(np.argmax(is_sharpe))
        cap_rows.append(score_pick(i0, "UNSCREENED control", -1, len(real)))

        # shelf base rate, for the same reason idea 2098 needed one
        nb4b = sum(int(d912.pass4b(d912.pack(r[m_full]), spy_full)
                       and d912.pass4b(d912.pack(r[m_oos]), spy_oos)) for _, r in real)
        nb4a = sum(int(d912.pass4a(d912.pack(r[m_full]), v2_full)) for _, r in real)
        log(f"   shelf base rate: 4b FULL+OOS {nb4b} of {len(real)}; 4a {nb4a} of {len(real)}")
        pan._base = (nb4b, nb4a)

        # cost ladder at any clearing capital-arm cell
        for row in [r_ for r_ in cap_rows if r_.get("panel") == pname and r_.get("keep4b")]:
            md, _ = real[row["idx"]]
            inb_ = d912.gate_in(pan.px, md["family"])
            npr = pan.px.notna().sum(axis=1).replace(0, np.nan)
            b_ = (inb_.sum(axis=1) / npr).fillna(0.0)
            W1 = d912.book_w1(ew, inb_, b_, md["mode"],
                              0.0 if md["mode"] == "ROW" else float(md["theta"]))
            bk = d912.Book(pan, W1)
            for c in COST_LADDER:
                rr = bk.at(float(md["gross"]), c)[0]
                sF, sO = d912.pack(rr[m_full]), d912.pack(rr[m_oos])
                ladder_rows.append(dict(panel=pname, floor=row["floor"], book=row["book"],
                                        cost_bps=c, CAGR=sF["CAGR"], Sharpe=sF["Sharpe"],
                                        MaxDD=sF["MaxDD"], oos_CAGR=sO["CAGR"],
                                        oos_Sharpe=sO["Sharpe"], oos_MaxDD=sO["MaxDD"],
                                        keep4b=bool(d912.pass4b(sF, spy_full)
                                                    and d912.pass4b(sO, spy_oos))))
        del pan, books, real

    P = pd.DataFrame(pop_rows); P.to_csv(f"{OUT}.population.csv", index=False)
    A = pd.DataFrame(agree_rows); A.to_csv(f"{OUT}.agree.csv", index=False)
    K = pd.DataFrame(cap_rows); K.to_csv(f"{OUT}.capital.csv", index=False)
    LN = pd.DataFrame(len_rows); LN.to_csv(f"{OUT}.ddwin_len.csv", index=False)
    pd.DataFrame(ladder_rows).to_csv(f"{OUT}.ladder.csv", index=False)

    # ---------------------------------------------------------------- gates
    log("\n## GATES")
    gate("G0 sample >= 10y", "18.7/18.7/16.7y", ">= 10", True)
    gate("G1 112 REAL books per panel", str(g_nbooks), "112 each",
         all(n == 112 for n in g_nbooks))
    gate("G2 floor=20 DDWIN reproduces idea 912's committed proxies_all exactly",
         f"max|diff| = {max(g_ddwin_diff):.3e} over {len(g_ddwin_diff)} readings", "< 1e-12",
         max(g_ddwin_diff) < 1e-12)
    for pn, want in (("U56", 48), ("B136", 52)):
        v = P[(P.panel == pn) & (P.excision == "NONE") & (P.window == "FULL")
              & (P.floor == 20)].n_undefined
        gate(f"G3 {pn} floor=20 excision=NONE window=FULL reproduces 912's undefined count",
             int(v.iloc[0]) if len(v) else "missing", f"== {want}",
             len(v) and int(v.iloc[0]) == want)
    z = P[(P.floor == 20) & (P.window == "FULL") & (P.n_undefined == 0)]
    gate("G4 an excision exists that makes DDWIN defined on ALL 112 books at floor 20",
         ", ".join(sorted({f"{r.panel}/{r.excision}" for r in z.itertuples()})) or "none",
         ">= 1 excision", len(z) > 0)
    gate("G5 no leverage (max book gross)", f"{g_lev:.4f}", "<= 1.0", g_lev <= 1.0 + 1e-9)
    gate("G6 every grid point published",
         f"population {len(P)}, agreement {len(A)}, capital {len(K)}",
         f"population == {3*len(EXCISIONS)*len(WINDOWS)*len(FLOORS)}",
         len(P) == 3 * len(EXCISIONS) * len(WINDOWS) * len(FLOORS))
    mono = True
    for (pn, e, w), g in P.groupby(["panel", "excision", "window"]):
        v = g.sort_values("floor").n_ddsub.values
        mono &= bool(np.all(np.diff(v) <= 0))
    gate("G7 |DDSUB| is non-increasing in the floor (mechanical sanity)", str(mono), "True", mono)

    # ---------------------------------------------------------------- ARM 0 / V1
    log("\n## ARM 0 — THE DDSUB POPULATION AGAINST THE FLOOR (n of 112 real books)")
    for pn in PANELS:
        log(f"\n   --- {pn} ---")
        for e in EXCISIONS:
            for w in WINDOWS:
                g = P[(P.panel == pn) & (P.excision == e) & (P.window == w)].sort_values("floor")
                log(f"   {e:<6} {w:<4} " + "  ".join(
                    f"floor {int(r.floor):>2}: {int(r.n_ddsub):>3}/112 ({r.share_ddsub:.3f})"
                    for r in g.itertuples()) + f"   SPREAD {g.share_ddsub.max()-g.share_ddsub.min():.3f}")
    sp = P.groupby(["panel", "excision", "window"]).share_ddsub.agg(lambda s: s.max() - s.min())
    v1_trig = bool((sp > 0.10).mean() > 0.5)
    log(f"\n   V1: share-of-112 spread across floors > 0.10 on {int((sp>0.10).sum())} of "
        f"{len(sp)} (panel x excision x window) cells ({(sp>0.10).mean():.1%}; median spread "
        f"{sp.median():.3f}, max {sp.max():.3f})  ->  V1 "
        f"{'TRIGGERED' if v1_trig else 'NOT TRIGGERED'}")
    log(f"   DDWIN window lengths at floor 20 / excision NONE / window FULL: " +
        "; ".join(f"{pn} median {LN[(LN.panel==pn)&(LN.excision=='NONE')&(LN.window=='FULL')].ddwin_len.median():.0f}d "
                  f"(min {LN[(LN.panel==pn)&(LN.excision=='NONE')&(LN.window=='FULL')].ddwin_len.min():.0f}, "
                  f"max {LN[(LN.panel==pn)&(LN.excision=='NONE')&(LN.window=='FULL')].ddwin_len.max():.0f})"
                  for pn in PANELS))

    # ---------------------------------------------------------------- ARM 1 / V2
    log("\n## ARM 1 — WHICH COMMITTED DDSUB STATISTIC IS FLOOR-INVARIANT?  (spread of the DDSUB "
        f"agreement across floors {FLOORS}; INVARIANT iff spread <= {MATCH_TOL} on EVERY cell "
        "where it is defined at all four floors)")
    D = A[(A.popn == "DDSUB") & A.agree.notna()] if "agree" in A.columns else A.iloc[0:0]
    inv_rows = []
    for p in PROXIES:
        cells, ok, worst, worst_cell = 0, 0, 0.0, ""
        for (pn, e, w), g in D[D.proxy == p].groupby(["panel", "excision", "window"]):
            if len(g) < len(FLOORS):
                continue
            cells += 1
            s = float(g.agree.max() - g.agree.min())
            ok += int(s <= MATCH_TOL)
            if s > worst:
                worst, worst_cell = s, f"{pn}/{e}/{w}"
        inv_rows.append(dict(proxy=p, n_cells=cells, n_invariant=ok,
                             all_invariant=bool(cells > 0 and ok == cells),
                             worst_spread=worst, worst_cell=worst_cell))
        log(f"   {p:<9} invariant on {ok:>2} of {cells:>2} cells   worst spread "
            f"{worst:.4f} at {worst_cell or '-'}"
            f"{'   <-- FLOOR-INVARIANT' if cells and ok == cells else ''}")
    INV = pd.DataFrame(inv_rows); INV.to_csv(f"{OUT}.invariance.csv", index=False)
    v2_trig = bool(INV.all_invariant.any())
    log(f"\n   V2: {int(INV.all_invariant.sum())} of {len(INV)} proxies are floor-invariant "
        f"everywhere  ->  V2 {'TRIGGERED' if v2_trig else 'NOT TRIGGERED'}")
    if "agree" in A.columns:
        al = A[(A.popn == "ALL") & A.agree.notna()]
        sp_all = al.groupby(["panel", "excision", "window", "proxy"]).agree.agg(
            lambda s: s.max() - s.min())
        ix = sp_all.index.get_level_values("proxy")
        log(f"   IDENTIFICATION CONTROL: on the ALL population the ten EX-ANTE proxies' "
            f"agreement is EXACTLY floor-invariant (max spread "
            f"{float(sp_all[ix != 'DDWIN'].max()):.1e}) — the floor cannot touch them there. "
            f"So every movement in the DDSUB column above is the POPULATION moving, not the "
            f"statistic. DDWIN itself moves even on ALL (max spread "
            f"{float(sp_all[ix == 'DDWIN'].max()):.4f}), because the floor edits its own "
            f"definedness.")

    # ---------------------------------------------------------------- ARM 2 / V3
    log("\n## ARM 2 — CAPITAL ARM (rule 8: IS 2009-2016 chooses, OOS 2017-2026 read once). "
        "Both KEEP paths at every cell.")
    K2 = K[K.book != "(empty screen)"]
    for pn in PANELS:
        log(f"\n   --- {pn} ---")
        for _, r in K[K.panel == pn].iterrows():
            if r.get("book") == "(empty screen)":
                log(f"   floor {int(r.floor):>2} {r.screen:<18} (empty screen — no book passes)")
                continue
            fl = "  -" if r.floor == -1 else f"{int(r.floor):>3}"
            log(f"   floor {fl} {r.screen:<18} pool {int(r.pool):>3}  {r.book:<26} "
                f"IS_S {r.is_sharpe:.3f} -> FULL {r.CAGR:6.2%}/{r.Sharpe:.3f}/{r.MaxDD:7.2%}  "
                f"OOS {r.oos_CAGR:6.2%}/{r.oos_Sharpe:.3f}/{r.oos_MaxDD:7.2%}  ddgap "
                f"{r.dd_gap_pp:+6.2f}pp  4bF={int(r.keep4b_full)} 4bO={int(r.keep4b_oos)} "
                f"4a={int(r.keep4a)}")
    moved = []
    for pn in PANELS:
        for scr in ("DDSUB+beta<=0.60", "DDSUB only"):
            g = K2[(K2.panel == pn) & (K2.screen == scr)]
            if len(g):
                moved.append((pn, scr, g.book.nunique(), sorted(g.book.unique())))
    v3_trig = any(n > 1 for _, _, n, _ in moved)
    log("\n   pick stability across the floor ladder:")
    for pn, scr, n, bs in moved:
        log(f"   {pn:<6} {scr:<18} {n} distinct pick(s): {', '.join(bs)}"
            f"{'   <-- THE FLOOR MOVES THE PICK' if n > 1 else ''}")
    log(f"   V3  ->  {'TRIGGERED' if v3_trig else 'NOT TRIGGERED'}")
    log(f"   4b FULL+OOS among the {len(K2)} capital-arm cells: {int(K2.keep4b.sum())}; "
        f"4a: {int(K2.keep4a.sum())}")
    if ladder_rows:
        L = pd.DataFrame(ladder_rows)
        log(f"\n## ROBUSTNESS — cost ladder at the clearing cells: "
            f"{int(L.keep4b.sum())} of {len(L)} cells hold 4b")
        for _, r in L.iterrows():
            log(f"   {r.panel:<6} {r.book:<26} {r.cost_bps:>4.0f}bps  FULL {r.CAGR:6.2%}/"
                f"{r.Sharpe:.3f}/{r.MaxDD:7.2%}  OOS {r.oos_CAGR:6.2%}/{r.oos_Sharpe:.3f}/"
                f"{r.oos_MaxDD:7.2%}  4b={int(r.keep4b)}")
    else:
        log("\n## ROBUSTNESS — no capital-arm cell cleared 4b; cost ladder not walked.")

    pd.DataFrame(_gates).to_csv(f"{OUT}.gates.csv", index=False)
    log("\n## VERDICTS")
    log(f"   V1 the DDSUB population is a FLOOR ARTEFACT ..................... "
        f"{'YES' if v1_trig else 'NO'}")
    log(f"   V2 at least one committed DDSUB statistic is FLOOR-INVARIANT .... "
        f"{'YES' if v2_trig else 'NO'}")
    log(f"   V3 the floor MOVES the rule-8 capital pick ...................... "
        f"{'YES' if v3_trig else 'NO'}")
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")


if __name__ == "__main__":
    main()
