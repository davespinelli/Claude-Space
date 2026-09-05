#!/usr/bin/env python3
"""QUEUE idea 170 — is-0.75-the-argmax-on-every-corpus  (cloud, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 170)
    "idea 166 found the incumbent constant `g = 0.75` is the OUT-OF-SAMPLE argmax of a 10-point
     gross ladder on idea 78's 300 books (OOS-4b pass 0.110 at 0.75, 0.103 at 0.70, 0.027 at
     1.00) with a 0.70-0.75 plateau, and that no IS-fitted chooser beats it.  That is currently
     a one-corpus claim.  Re-run the identical ladder on the u56 and broad ranked/EWall books
     and on the small panel, and report where the OOS argmax sits on each.  If it is 0.70-0.80
     everywhere, PROTOCOL can state the constant as a finding rather than an inheritance.
     Max 2 params."

WHAT IS AT STAKE.
    `g = 0.75` is inherited from RULES v1 (5 names x 15%).  Idea 66 established gross is an
    exact lever with no Sharpe content; idea 166 nonetheless found the OOS-4b PASS RATE of a
    300-book corpus peaks at 0.70-0.75.  If that peak is a property of the 4b bars (and so of
    any corpus), PROTOCOL can quote 0.75 as a measured constant.  If it is a property of idea
    78's B136 sub-panel corpus, it is still an inheritance and must not be promoted.

CORPUS (axes, NOT tuned) — three panels x two book constructions x two book families:
    panels      U56    = baseline.load_universe()              (56 ETF/mega-cap names)
                B136   = baseline.load_universe(broad=True)    (136 large caps)
                SMALL  = baseline.load_universe(small=True) with every ticker whose
                         data/small_meta.csv max_1d_move >= 1.0 dropped (44 dropped, 439 left)
    whole-panel books   RANKED n in {5, 10, 20, 40}  (idea 78's `weights_cand`, no vol scaler)
                        EWALL                        (idea 78's `weights_ewall`)
    sub-panel books     12 fixed draws of k=40 tradable names per panel, RANKED n=20, from
                        np.random.default_rng(170_000 + panel_seed) — idea 78's draw device,
                        re-seeded per panel, so the pooled pass-rate curve is not read off 5
                        books per panel.
    => 3 x 5 = 15 whole-panel books + 3 x 12 = 36 sub-panel books = 51 books, 10 gross points
       each = 510 engine runs.  10 bps, weekly, t+1, no shorting, no leverage (PROTOCOL 2).

TUNED PARAMETERS — exactly two, swept exhaustively, ALL grid points in .ladder.csv:
    1. the LADDER POINT g, 10 values {0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.75, 0.80, 0.90,
       1.00} — imported verbatim from idea 166's script, not retyped.
    2. the RANKED book size n, 4 values {5, 10, 20, 40}.
    The scoring machinery (`rel_margins`, `bars_win`, `win`) is IMPORTED from idea 166's
    committed script, so "identical ladder" is enforced by reuse rather than by transcription.

WALK-FORWARD (PROTOCOL rule 8) — arms fixed BEFORE any OOS number is read:
    Per book: STATIC g=0.75 (the control), ISMARG = IS 4b-relative-margin argmax (ties -> smaller
    g), ISSHARPE = IS Sharpe argmax (ties -> smaller g).  Everything chosen on <= 2016-12-31
    only, read ONCE on 2017-01-01..2026-09-04.  OOS CAGR/Sharpe/MaxDD reported per arm against
    RULES v1 on the same panel and against SPY.  Both KEEP paths (4a and 4b) evaluated at every
    ladder point of every book.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  The three Sharpe bars (H1, H2, OOS) are near gross-invariant in this construction (both
        the return stream and the 10 bps cost drag scale with g), so on any book whose binding
        bar is a Sharpe bar the margin curve is FLAT in g and its argmax is decided by the
        tie-break, not by the data.  Expect a large share of books in that state.
    P2  Where CAGR and DD bind instead, the margin argmax is an interior crossing of a rising
        CAGR margin and a falling DD margin, and its location depends on the book's own vol —
        i.e. it moves with the panel and with n, not with 4b.
    P3  Therefore 0.70-0.80 will NOT be the OOS argmax everywhere; I expect the per-panel
        pooled OOS-pass argmax to differ across the three panels.  If P3 is wrong and every
        panel peaks in 0.70-0.80, idea 170's promotion is earned.
    P4  No arm produces a 4b KEEP that PROTOCOL would accept on the small panel (idea 133/136).
    P5  ISMARG and ISSHARPE do not beat STATIC on OOS mean Sharpe (ideas 110/151/132/166).

CAVEATS carried, not buried
    * SURVIVORSHIP.  All three panels are current-constituent lists (idea 54); the small panel
      is the sub-$2B screen's survivors since 2010 and its numbers are biased upward in a way
      that falls hardest on the beaten-down cohort.  Nothing here corrects it; the ladder
      compares gross points WITHIN a panel, where the bias is common to every point.
    * Idea 144: a re-grossed book is the SAME book.  A verdict flip along the ladder is not a
      new signal.
    * Idea 38 (calendar-day price index on prices.csv/prices_broad.csv) and idea 126 (t+1
      execution only) carry over unchanged.
    * The 4b OOS bar inside `rel_margins("IS")` is, by idea 166's convention, the window's own
      Sharpe vs SPY's — kept identical so the ladders are comparable.
    * SMALL's sample starts 2010-01-04, so its halves and its IS window are shorter than the
      large-cap panels'.  Reported, not adjusted.

Deterministic, standalone.  Writes .console.txt, .ladder.csv, .argmax.csv, .corpus.csv,
.walkforward.csv.
"""
import importlib.util
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_is-075-the-argmax-on-every-corpus_cloud"
OUT = ROOT / "research" / "backtests"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# idea 166's committed script — LADDER, rel_margins, bars_win, win, and (through it) idea 78's
# eligible_mask / weights / half_sharpes / fail_4a / fail_4b.  Imported, not retyped.
I166 = _load(OUT / "2026-09-05_does-the-ceiling-beat-a-chosen-gross_C.py", "i166")
I78 = I166.I78

LADDER = I166.LADDER
COST_BPS = I166.COST_BPS          # 10
FREQ = I166.FREQ                  # "W"
GROSS0 = I166.GROSS0              # 0.75
IS_END, OOS_START = I166.IS_END, I166.OOS_START
CAP = I166.CAP                    # 1.00
NS = [5, 10, 20, 40]              # tuned param 2
K_SUB, N_DRAWS, N_SUB = 40, 12, 20
SEEDS = {"U56": 170_056, "B136": 170_136, "SMALL": 170_439}
ARMS = ["STATIC", "ISMARG", "ISSHARPE"]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 4000)

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


def build_panels():
    """U56, B136 and the max_1d_move-filtered SMALL panel, each as (prices, tradable set)."""
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in pxs.columns if c == "SPY" or c not in bad]
    pxs = pxs[keep]
    return {
        "U56": (px56, set(c for c in px56.columns)),
        "B136": (px136, set(c for c in px136.columns)),
        "SMALL": (pxs, set(c for c in pxs.columns if c != "SPY")),
    }, len(bad), len(meta)


def book_weights(px, tradable, kind, n, g):
    if kind == "EWALL":
        return I78.weights_ewall(px, tradable, gross=g)
    return I78.weights_cand(px, tradable, n, gross=g)


def argmax_g(L, col):
    """Ladder argmax of `col`, ties -> smaller g (idea 166's tie-break)."""
    o = L.sort_values([col, "g"], ascending=[False, True])
    return float(o.iloc[0].g), float(o.iloc[0][col])


def flat_in_g(L, col, tol=1e-3):
    """True when the curve's spread across the whole ladder is below tol (P1's test)."""
    return float(L[col].max() - L[col].min()) < tol


def main():
    t0 = time.time()
    say("=" * 200)
    say(f"IDEA 170 — is-0.75-the-argmax-on-every-corpus   ({STEM})")
    say("Idea 166's identical 10-point gross ladder (imported, not retyped) re-run on U56, B136 "
        "and the filtered SMALL panel, ranked and EWall, whole-panel and sub-panel books.  "
        "Question: where does the OOS argmax sit on each corpus?")
    say("PRE-REGISTERED: 2 tuned params (ladder point g x 10, ranked book size n x 4).  Panel, "
        "construction and draw are corpus axes carried over from ideas 78/166.")
    say("=" * 200)

    panels, n_dropped, n_meta = build_panels()
    say(f"\n  SMALL panel: dropped {n_dropped} of {n_meta} tickers with max_1d_move >= 1.0 "
        f"(data/small_meta.csv); {len(panels['SMALL'][1])} tradable names remain.")
    say("  SURVIVORSHIP: all three panels are current-constituent lists; the small panel is the "
        "sub-$2B screen's SURVIVORS since 2010.  Levels are biased up; the ladder compares "
        "gross points WITHIN a panel, where the bias is common to every point.")

    ctx = {}
    for pname, (px, tr) in panels.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        bw = rules_v1_weights(px)
        drop = [c for c in px.columns if c not in tr]
        if drop:
            bw[drop] = 0.0
        base = backtest(px, bw, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        ctx[pname] = dict(px=px, tr=tr, start=start, spy=spy, base=base,
                          b_IS=I166.bars_win(spy, "IS"), b_OOS=I166.bars_win(spy, "OOS"),
                          b_full=I166.bars_win(spy, "full"))
        ms, mb = metrics(spy), metrics(base)
        mso, mbo = metrics(spy.loc[OOS_START:]), metrics(base.loc[OOS_START:])
        say(f"\n  panel {pname:<6} {px.shape[1]} cols, {len(tr)} tradable, eval "
            f"{start.date()} .. {px.index[-1].date()}   IS <= {IS_END}, OOS {OOS_START} ->")
        say(f"    SPY      full {ms['CAGR']:7.2%}/{ms['Sharpe']:.3f}/{ms['MaxDD']:8.2%}   "
            f"OOS {mso['CAGR']:7.2%}/{mso['Sharpe']:.3f}/{mso['MaxDD']:8.2%}")
        say(f"    RULES v1 full {mb['CAGR']:7.2%}/{mb['Sharpe']:.3f}/{mb['MaxDD']:8.2%}   "
            f"OOS {mbo['CAGR']:7.2%}/{mbo['Sharpe']:.3f}/{mbo['MaxDD']:8.2%}")
        for lbl in ("IS", "OOS", "full"):
            b = ctx[pname][f"b_{lbl}"]
            say(f"    4b bars {lbl:<4}: H1 > {b['s1']:.3f}, H2 > {b['s2']:.3f}, "
                f"Sharpe > {b['soos']:.3f}, |MaxDD| <= {I166.DELTA * abs(b['sdd']):.2%}, "
                f"CAGR >= {I166.PHI * b['scagr']:.2%}")
    say(f"\n  ladder (idea 166's, imported): {LADDER}")

    # ------------------------------------------------------------------ the books
    books = []                                  # (panel, family, label, kind, n, cols)
    for pname, (px, tr) in panels.items():
        for n in NS:
            books.append((pname, "whole", f"RANKED{n}", "RANKED", n, None))
        books.append((pname, "whole", "EWALL", "EWALL", np.nan, None))
        names = sorted(tr)
        rng = np.random.default_rng(SEEDS[pname])
        for d in range(N_DRAWS):
            cols = sorted(rng.choice(names, size=min(K_SUB, len(names)), replace=False))
            books.append((pname, "sub", f"SUB{d:02d}", "RANKED", N_SUB, cols))

    lad_rows, arg_rows, wf_rows = [], [], []
    for bi, (pname, fam, label, kind, n, cols) in enumerate(books):
        c = ctx[pname]
        px, tr, start = c["px"], c["tr"], c["start"]
        if cols is None:
            p, trb = px, tr
        else:
            keep = list(dict.fromkeys(list(cols) + ["SPY"]))
            p, trb = px[keep].dropna(how="all").ffill(), set(cols)
        lad = []
        rets = {}
        for g in LADDER:
            w = book_weights(p, trb, kind, n, g)
            res = backtest(p, w, cost_bps=COST_BPS, freq=FREQ)
            r = res["returns"].loc[start:]
            rets[g] = r
            mi = I166.rel_margins(r, c["b_IS"], "IS")
            mo = I166.rel_margins(r, c["b_OOS"], "OOS")
            mf = I166.rel_margins(r, c["b_full"], "full")
            m_is, m_full, m_oos = (metrics(r.loc[:IS_END]), metrics(r),
                                   metrics(r.loc[OOS_START:]))
            h1, h2 = I78.half_sharpes(r)
            lad.append(dict(
                panel=pname, family=fam, book=label, kind=kind, n=n, g=g,
                CAGR=m_full["CAGR"], Sharpe=m_full["Sharpe"], MaxDD=m_full["MaxDD"],
                H1=h1, H2=h2, vol=m_full["Vol"],
                turnover_yr=res["turnover"].loc[start:].sum() / (len(r) / 252),
                IS_Sharpe=m_is["Sharpe"], IS_CAGR=m_is["CAGR"], IS_MaxDD=m_is["MaxDD"],
                OOS_CAGR=m_oos["CAGR"], OOS_Sharpe=m_oos["Sharpe"], OOS_MaxDD=m_oos["MaxDD"],
                IS_margin=mi["margin"], IS_pass=mi["margin"] > 0, IS_fails=mi["fails"],
                IS_bar_H1=mi["H1"], IS_bar_H2=mi["H2"], IS_bar_OOS=mi["OOS"],
                IS_bar_DD=mi["DD"], IS_bar_CAGR=mi["CAGR"],
                OOS_margin=mo["margin"], OOS_pass=mo["margin"] > 0, OOS_fails=mo["fails"],
                OOS_bar_H1=mo["H1"], OOS_bar_H2=mo["H2"], OOS_bar_OOS=mo["OOS"],
                OOS_bar_DD=mo["DD"], OOS_bar_CAGR=mo["CAGR"],
                full_margin=mf["margin"], full_pass4b=(mf["margin"] > 0),
                f4b=I78.fail_4b(r, c["spy"], r.loc[OOS_START:], c["spy"].loc[OOS_START:]),
                f4a=I78.fail_4a(r, c["base"]),
            ))
        L = pd.DataFrame(lad)
        L["pass4a"] = L.f4a == "-"
        lad_rows.extend(L.to_dict("records"))

        g_is, v_is = argmax_g(L, "IS_margin")
        g_oos, v_oos = argmax_g(L, "OOS_margin")
        g_full, v_full = argmax_g(L, "full_margin")
        g_shr, _ = argmax_g(L, "IS_Sharpe")
        g_oshr, _ = argmax_g(L, "OOS_Sharpe")
        passing = L.loc[L.OOS_pass, "g"]
        arg_rows.append(dict(
            panel=pname, family=fam, book=label, kind=kind, n=n,
            g_IS_margin=g_is, IS_margin_max=v_is, IS_flat=flat_in_g(L, "IS_margin"),
            g_OOS_margin=g_oos, OOS_margin_max=v_oos, OOS_flat=flat_in_g(L, "OOS_margin"),
            g_full_margin=g_full, full_margin_max=v_full,
            g_IS_Sharpe=g_shr, g_OOS_Sharpe=g_oshr,
            OOS_Sharpe_spread=float(L.OOS_Sharpe.max() - L.OOS_Sharpe.min()),
            OOS_binding_bar=L.set_index("g").loc[g_oos, ["OOS_bar_H1", "OOS_bar_H2",
                                                         "OOS_bar_OOS", "OOS_bar_DD",
                                                         "OOS_bar_CAGR"]].idxmin()[8:],
            n_OOS_pass=int(L.OOS_pass.sum()), n_IS_pass=int(L.IS_pass.sum()),
            n_full_pass4b=int(L.full_pass4b.sum()), n_pass4a=int(L.pass4a.sum()),
            OOS_pass_lo=(float(passing.min()) if len(passing) else np.nan),
            OOS_pass_hi=(float(passing.max()) if len(passing) else np.nan),
        ))

        # ------------------------------------------------- rule 8 walk-forward (3 arms)
        chosen = dict(STATIC=GROSS0, ISMARG=g_is, ISSHARPE=g_shr)
        for arm in ARMS:
            g = float(min(chosen[arm], CAP))
            r = rets[g]
            mo_ = metrics(r.loc[OOS_START:])
            mo = I166.rel_margins(r, c["b_OOS"], "OOS")
            bo = metrics(c["base"].loc[OOS_START:])
            so = metrics(c["spy"].loc[OOS_START:])
            wf_rows.append(dict(
                panel=pname, family=fam, book=label, kind=kind, n=n, arm=arm, g=g,
                OOS_CAGR=mo_["CAGR"], OOS_Sharpe=mo_["Sharpe"], OOS_MaxDD=mo_["MaxDD"],
                OOS_margin=mo["margin"], OOS_pass4b=mo["margin"] > 0, OOS_fails=mo["fails"],
                base_OOS_Sharpe=bo["Sharpe"], base_OOS_CAGR=bo["CAGR"],
                base_OOS_MaxDD=bo["MaxDD"], spy_OOS_Sharpe=so["Sharpe"],
                spy_OOS_CAGR=so["CAGR"], spy_OOS_MaxDD=so["MaxDD"],
                d_Sharpe_vs_base=mo_["Sharpe"] - bo["Sharpe"],
                d_Sharpe_vs_spy=mo_["Sharpe"] - so["Sharpe"],
            ))
        if (bi + 1) % 10 == 0 or bi == len(books) - 1:
            say(f"  books {bi + 1}/{len(books)} done  ({time.time() - t0:.0f}s)")

    LAD, ARG, WF = pd.DataFrame(lad_rows), pd.DataFrame(arg_rows), pd.DataFrame(wf_rows)
    LAD.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
    ARG.to_csv(OUT / f"{STEM}.argmax.csv", index=False)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    # =============================================================== 1. whole-panel ladders
    say("\n" + "=" * 200)
    say("1. THE LADDER, EVERY POINT — whole-panel books (OOS-window relative 4b margin; "
        "> 0 means the book passes 4b on 2017-2026)")
    say("=" * 200)
    W = LAD[LAD.family == "whole"]
    for pname in panels:
        say(f"\n  {pname}: OOS_margin by (book, g)")
        say(W[W.panel == pname].pivot_table(index="book", columns="g", values="OOS_margin")
            .to_string(float_format=lambda x: f"{x:+.3f}"))
        say(f"  {pname}: OOS_Sharpe by (book, g)   [P1: flat in g => Sharpe bars are "
            f"gross-invariant]")
        say(W[W.panel == pname].pivot_table(index="book", columns="g", values="OOS_Sharpe")
            .to_string(float_format=lambda x: f"{x:.3f}"))

    # =============================================================== 2. the argmaxes
    say("\n" + "=" * 200)
    say("2. WHERE THE ARGMAX SITS — per book (the idea's actual question)")
    say("=" * 200)
    say("\n  whole-panel books:")
    say(ARG[ARG.family == "whole"][
        ["panel", "book", "n", "g_IS_margin", "g_OOS_margin", "g_full_margin", "g_OOS_Sharpe",
         "OOS_margin_max", "OOS_flat", "OOS_binding_bar", "n_OOS_pass", "OOS_pass_lo",
         "OOS_pass_hi", "n_pass4a"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say("\n  sub-panel books (12 draws x 3 panels, k=40, RANKED n=20):")
    say(ARG[ARG.family == "sub"].groupby("panel").agg(
        books=("book", "size"),
        median_g_OOS=("g_OOS_margin", "median"),
        mean_g_OOS=("g_OOS_margin", "mean"),
        share_g_OOS_in_070_080=("g_OOS_margin", lambda s: float(((s >= 0.70) & (s <= 0.80)).mean())),
        median_g_IS=("g_IS_margin", "median"),
        OOS_flat_share=("OOS_flat", "mean"),
        mean_OOS_Sharpe_spread=("OOS_Sharpe_spread", "mean"),
        any_OOS_pass=("n_OOS_pass", lambda s: int((s > 0).sum())),
    ).to_string(float_format=lambda x: f"{x:.3f}"))

    say("\n  OOS argmax distribution over ALL 51 books, by panel (counts per ladder point):")
    tab = ARG.pivot_table(index="panel", columns="g_OOS_margin", values="book",
                          aggfunc="size").fillna(0).astype(int)
    say(tab.to_string())
    say("\n  pooled over all panels: " + ", ".join(
        f"{g:.2f}:{int((ARG.g_OOS_margin == g).sum())}" for g in LADDER))
    inband = float(((ARG.g_OOS_margin >= 0.70) & (ARG.g_OOS_margin <= 0.80)).mean())
    say(f"  share of books whose OOS argmax lies in idea 170's claimed 0.70-0.80 band: "
        f"{inband:.3f}  ({int(inband * len(ARG))} of {len(ARG)})")

    # =============================================================== 3. corpus pass-rate curve
    say("\n" + "=" * 200)
    say("3. IDEA 166's STATISTIC — OOS-window 4b PASS RATE at each ladder point, per corpus")
    say("=" * 200)
    rows = []
    for pname in list(panels) + ["ALL"]:
        sub = LAD if pname == "ALL" else LAD[LAD.panel == pname]
        for fam in ("whole", "sub", "both"):
            s = sub if fam == "both" else sub[sub.family == fam]
            if not len(s):
                continue
            d = dict(panel=pname, family=fam, books=int(s.book.nunique()))
            for g in LADDER:
                d[f"{g:.2f}"] = float(s.loc[s.g == g, "OOS_pass"].mean())
            gs = [d[f"{g:.2f}"] for g in LADDER]
            best = max(gs)
            d["argmax_g"] = LADDER[gs.index(best)] if best > 0 else np.nan
            d["peak"] = best
            d["at_075"] = d["0.75"]
            rows.append(d)
    CORP = pd.DataFrame(rows)
    CORP.to_csv(OUT / f"{STEM}.corpus.csv", index=False)
    say(CORP.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say("\n  idea 166's B136 sub-panel corpus for reference: 0.75 -> 0.110, 0.70 -> 0.103, "
        "1.00 -> 0.027 (300 books).")

    # =============================================================== 4. which bar binds
    say("\n" + "=" * 200)
    say("4. WHICH BAR BINDS ON THE OOS WINDOW, at each ladder point (share of books)")
    say("=" * 200)
    bars = ["OOS_bar_H1", "OOS_bar_H2", "OOS_bar_OOS", "OOS_bar_DD", "OOS_bar_CAGR"]
    LAD["binding"] = LAD[bars].idxmin(axis=1).str[8:]
    say(pd.crosstab(LAD.g, LAD.binding, normalize="index")
        .to_string(float_format=lambda x: f"{x:.3f}"))
    say("\n  by panel, at g = 0.75:")
    say(pd.crosstab(LAD[LAD.g == GROSS0].panel, LAD[LAD.g == GROSS0].binding)
        .to_string())
    say("\n  P1 check — mean spread of each bar across the whole ladder, by panel "
        "(a Sharpe bar that does not move in g cannot produce an argmax):")
    sp = LAD.groupby(["panel", "book"])[bars].agg(lambda s: s.max() - s.min())
    say(sp.groupby("panel").mean().to_string(float_format=lambda x: f"{x:.4f}"))

    # =============================================================== 5. walk-forward
    say("\n" + "=" * 200)
    say("5. RULE 8 WALK-FORWARD — g chosen on IS (<= 2016-12-31) only, read once on 2017-2026")
    say("=" * 200)
    say(WF.groupby(["panel", "arm"]).agg(
        books=("book", "size"), mean_g=("g", "mean"),
        OOS_CAGR=("OOS_CAGR", "mean"), OOS_Sharpe=("OOS_Sharpe", "mean"),
        OOS_MaxDD=("OOS_MaxDD", "mean"), OOS_4b_passes=("OOS_pass4b", "sum"),
        d_vs_base=("d_Sharpe_vs_base", "mean"), d_vs_spy=("d_Sharpe_vs_spy", "mean"),
    ).to_string(float_format=lambda x: f"{x:.3f}"))
    say("\n  paired (per book) OOS Sharpe differences vs the STATIC 0.75 control:")
    piv = WF.pivot_table(index=["panel", "book"], columns="arm", values="OOS_Sharpe")
    for arm in ("ISMARG", "ISSHARPE"):
        d = (piv[arm] - piv["STATIC"])
        say(f"    {arm:<9} mean {d.mean():+.4f}  median {d.median():+.4f}  "
            f"wins {int((d > 0).sum())}/{len(d)}  |max| {d.abs().max():.4f}")
    say("\n  whole-panel books, per-arm OOS detail vs RULES v1 and SPY:")
    say(WF[WF.family == "whole"][
        ["panel", "book", "arm", "g", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "OOS_pass4b",
         "OOS_fails", "base_OOS_Sharpe", "spy_OOS_Sharpe"]].to_string(
        index=False, float_format=lambda x: f"{x:.3f}"))

    # =============================================================== 6. KEEP paths
    say("\n" + "=" * 200)
    say("6. BOTH KEEP PATHS at every ladder point (full-sample verdicts)")
    say("=" * 200)
    say(f"  4a passes (Sharpe > RULES v1 in BOTH halves and MaxDD no worse): "
        f"{int(LAD.pass4a.sum())} of {len(LAD)} book-gross points")
    say(f"  4b passes (full sample): {int(LAD.full_pass4b.sum())} of {len(LAD)}")
    if LAD.full_pass4b.any():
        say(LAD[LAD.full_pass4b][["panel", "book", "kind", "n", "g", "CAGR", "Sharpe", "MaxDD",
                                  "H1", "H2", "OOS_Sharpe", "turnover_yr", "f4a"]]
            .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    if LAD.pass4a.any():
        say("\n  4a passers:")
        say(LAD[LAD.pass4a][["panel", "book", "kind", "n", "g", "CAGR", "Sharpe", "MaxDD",
                             "H1", "H2", "f4b"]]
            .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # =============================================================== census
    say("\n" + "=" * 200)
    say("CENSUS")
    say("=" * 200)
    say(f"  books {len(books)};  ladder rows {len(LAD)};  walk-forward rows {len(WF)}")
    say(f"  every g <= 1.00 (PROTOCOL rule 2): {bool((LAD.g <= CAP + 1e-12).all())}")
    say(f"  cost {COST_BPS} bps, freq {FREQ}, t+1 execution (engine), no shorting, no leverage")
    say(f"  runtime {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")
    print(f"\nwrote {STEM}.console.txt/.ladder.csv/.argmax.csv/.corpus.csv/.walkforward.csv")


if __name__ == "__main__":
    main()
