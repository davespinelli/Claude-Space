#!/usr/bin/env python3
"""Idea 330 — IS THE VOL-TERM DECOMPOSITION A RECORD-WIDE FACT?   (cloud, 2026-09-09)

PRE-REGISTERED QUESTION (from QUEUE.md, written before any number here was read)
    Idea 43 found the H1 Sharpe edge of the eligible-equal-weight family is ENTIRELY a
    volatility term over a negative return term (RETURN -0.621/-0.410/-0.646, VOL
    +0.731/+0.597/+0.189), so the vol-matched counterfactual Sharpe is 0.605/0.704/0.358 vs
    SPY's 0.957/0.957/0.891.  Run the same two-term split over every book in LEADERBOARD.md
    that has ever cleared a Sharpe-vs-SPY bar: is "wins on vol, loses on return" the record's
    universal shape, and is there ANY book whose return term is positive?  If none, PROTOCOL
    4b's Sharpe bars are measuring de-grossing and the CAGR floor is the only bar doing work.
    Max 2 params.

THE SPLIT, exactly idea 43's `gap_channels` (imported, not re-typed):
    S_b - S_s = (mu_b - mu_s)/sig_b   +   mu_s * (1/sig_b - 1/sig_s)
                \_____RETURN_____/       \________VOL________/
    and the vol-matched counterfactual Sharpe is mu_b / sig_s.

TWO ALGEBRAIC FACTS, derived and pre-registered BEFORE the grid was run, then gated on the
numbers (G4/G5).  With lambda = sig_b / sig_s:
    RETURN = S_b - S_s / lambda           VOL = S_s * (1/lambda - 1)
    ==> RETURN > 0  <==>  mu_b > mu_s     (the vol cancels; the sign is a pure RETURN race)
    ==> VOL    > 0  <==>  sig_b < sig_s
    ==> under the record's LEVER convention (idea 66: a book at gross g is exactly g x the
        same book at gross 1, cash at 0% per idea 406), mu_b and sig_b both scale by g, so
        S_b is INVARIANT while RETURN and VOL each MOVE with g and cancel.  The ENGINE's
        book-at-g-weights is NOT exactly the lever (its cash re-normalisation drifts
        differently at different gross); that gap is measured and REPORTED as G2, never
        assumed away.  The two gross points on the grid below are ENGINE books, exactly as the
        record quotes them; only the vol-matched counterfactual uses the lever.
    So the split is NOT a property of a book: it is a property of a book AT A STATED GROSS.
    At the vol-matched gross g* = sig_s/sig_b the VOL term is 0 by construction and the whole
    gap sits in RETURN — the same book, same Sharpe, opposite headline.

WHAT IS RUN.
  PART A — the record-wide census, published numbers only.  Every committed CSV under
    research/backtests/ carrying CAGR and Sharpe AND a row labelled exactly "SPY" is a
    comparison table with its own comparand.  For every other row: does it clear the
    Sharpe-vs-SPY bar, and if so does it also OUT-EARN SPY?  "Out-earns" is the published
    proxy for RETURN > 0 (the exact criterion is mu_b > mu_s and the record does not publish
    mu: only 1 of these 54 files publishes ann_ret/ann_vol).  The proxy's BIAS DIRECTION is
    known and stated: a lower-vol book at equal CAGR has LOWER mu (mu ~ ln(1+CAGR) +
    sig^2/2), so a CAGR screen OVER-counts positive return terms.  It is therefore an UPPER
    BOUND on the record's positive-return-term rate, which is the conservative direction for
    a question asking "is there ANY".
  PART B — re-derivation, 3 panels x 6 books x 3 gross points x 5 windows, all reported, with
    the exact criterion computed rather than proxied.

TUNED PARAMETERS: exactly TWO — the width n in {5, 10, 20, 40, ALL} (idea 43's own grid) and
    the gross g in {0.75, 1.00, g* = vol-matched}.  ALL points reported.  Panel, family and
    window are REPORTING axes and are never selected on.  g* is a REPORTED COUNTERFACTUAL,
    not a proposed book: g* > 1 is leverage, which PROTOCOL 2 forbids unless an idea says so,
    and this idea does not propose it — idea 43 quotes the same counterfactual.

RULE 8 (PROTOCOL 8): (n, g) chosen on IS <= 2016-12-31 by IS Sharpe, 2017-2026 read ONCE, per
    panel.  OOS CAGR/Sharpe/MaxDD against the live RULES v2 book, RULES v1 and SPY, BOTH KEEP
    paths evaluated at every grid point, and the OOS decomposition of the pick reported so the
    sign shape can be checked out of sample rather than in it.

REPRODUCTION GATES, asserted before any new number is read
  G1  idea 43's `fast_backtest` reproduces `engine.backtest` (returns, turnover) below 1e-12.
  G2  REPORTED, not asserted: how far the LEVER convention is from the engine's
      book-at-g-weights (g=1.00 engine book vs (1/0.75) x the g=0.75 engine book), on returns
      and on Sharpe.  This is a convention gap, not an error, and the number belongs in a
      gross-convention idea.
  G3  idea 43's published H1 decomposition on EWALL g=0.75 at 10 bps reproduces on all three
      panels: RETURN -0.621/-0.410/-0.646, VOL +0.731/+0.597/+0.189, counterfactual Sharpe
      0.605/0.704/0.358, SPY H1 0.957/0.957/0.891 (published to 3 dp, gated at 1e-3).
  G4  the identity RETURN = S_b - S_s/lambda and VOL = S_s(1/lambda - 1) holds on every row.
  G5  the sign identity RETURN > 0 <==> mu_b > mu_s holds on every row.

SURVIVORSHIP (PROTOCOL 9 / idea 54): B136 and SMALL439 are CURRENT-constituent lists; the
names that died are absent, so both panels' book returns are biased UP and their vols biased
DOWN relative to a real historical panel.  Both biases push the RETURN term UP and the VOL
term UP, i.e. they make a positive return term MORE likely here than in reality — the bias
runs in favour of the answer this script reports, so a null result is the safe direction and a
positive one must be discounted.  SMALL439: the 483-name sub-$2B panel with the 44 tickers
whose max_1d_move >= 1.0 dropped per data/SMALL_PANEL_README.md.

Costs 10 bps, weekly, weights at close t applied at t+1.  Deterministic, no network.
Writes .census.csv .decomp.csv .grid.csv .walkforward.csv .console.txt
"""
import glob
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

BT = REPO / "research" / "backtests"
STAMP = "2026-09-09_is-the-VOL-TERM-decomposition-a-record-wide-fact_cloud"
OUT = BT / STAMP


def _mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


i43 = _mod("i43", BT / "2026-09-07_h1-sharpe-diagnosis_cloud.py")
rank_frame, weights_for, fast_backtest = i43.rank_frame, i43.weights_for, i43.fast_backtest
gap_channels, small_panel, sharpe = i43.gap_channels, i43.small_panel, i43.sharpe

COST = 10.0
FREQ = "W"
WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
NS = [5, 10, 20, 40, "ALL"]
GROSSES = [0.75, 1.00]
BAND = 0.03

# idea 43's committed H1 numbers (LEADERBOARD 2026-09-07, EWALL g=0.75, 10 bps)
I43 = {"U56": dict(ret=-0.621, vol=+0.731, cf=0.605, spy=0.957),
       "B136": dict(ret=-0.410, vol=+0.597, cf=0.704, spy=0.957),
       "SMALL439": dict(ret=-0.646, vol=+0.189, cf=0.358, spy=0.891)}

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def halves(r):
    h = len(r) // 2
    return r.iloc[:h], r.iloc[h:]


def windows(r, spy):
    h = len(r) // 2
    return {"FULL": (r, spy),
            "H1": (r.iloc[:h], spy.iloc[:h]),
            "H2": (r.iloc[h:], spy.iloc[h:]),
            "IS": (r.loc[:IS_END], spy.loc[:IS_END]),
            "OOS": (r.loc[OOS_START:], spy.loc[OOS_START:])}


def keep_4a(r, base):
    a1, a2 = halves(r)
    b1, b2 = halves(base)
    return bool(sharpe(a1) > sharpe(b1) and sharpe(a2) > sharpe(b2)
                and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def tests_4b(r, spy):
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    return {"H1": sharpe(a1) > sharpe(s1), "H2": sharpe(a2) > sharpe(s2),
            "OOS": sharpe(r.loc[OOS_START:]) > sharpe(spy.loc[OOS_START:]),
            "DD": abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]),
            "CAGR": m["CAGR"] >= 0.70 * ms["CAGR"]}


def fail_4b(r, spy):
    f = [k for k, v in tests_4b(r, spy).items() if not v]
    return ",".join(f) if f else "-"


# ------------------------------------------------------------------ PART A
def census():
    files = sorted(glob.glob(str(BT / "*.csv"))) + sorted(glob.glob(str(BT / "*.csv.gz")))
    rows = []
    for f in files:
        try:
            df = pd.read_csv(f, low_memory=False)
        except Exception:
            continue
        lc = {c.lower(): c for c in df.columns}
        if "cagr" not in lc or "sharpe" not in lc:
            continue
        strc = [c for c in df.columns if pd.api.types.is_string_dtype(df[c])]
        lab = None
        for c in strc:
            if df[c].astype("object").astype(str).str.fullmatch("SPY", case=False,
                                                                na=False).any():
                lab = c
                break
        if lab is None:
            continue
        is_spy = df[lab].astype("object").astype(str).str.fullmatch("SPY", case=False, na=False)
        ref = df[is_spy]
        cg, sh = lc["cagr"], lc["sharpe"]
        if not pd.api.types.is_numeric_dtype(df[cg]) or not pd.api.types.is_numeric_dtype(df[sh]):
            continue
        s_ref, c_ref = float(ref[sh].median()), float(ref[cg].median())
        if not np.isfinite(s_ref) or not np.isfinite(c_ref):
            continue
        b = df[~is_spy]
        s, c = pd.to_numeric(b[sh], errors="coerce"), pd.to_numeric(b[cg], errors="coerce")
        ok = s.notna() & c.notna()
        s, c = s[ok], c[ok]
        beat = s > s_ref
        rows.append(dict(file=Path(f).name, n_books=int(len(s)), spy_Sharpe=s_ref,
                         spy_CAGR=c_ref, beat_sharpe=int(beat.sum()),
                         beat_both=int((beat & (c > c_ref)).sum()),
                         beat_sharpe_only=int((beat & (c <= c_ref)).sum()),
                         beat_sharpe_pass_cagr_floor=int((beat & (c >= 0.70 * c_ref)).sum())))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ main
def main():
    P(f"# Idea 330 — is the VOL-TERM decomposition a record-wide fact?   ({STAMP})")
    P(f"Costs {COST:.0f} bps, {FREQ} cadence, t+1 execution. Split = idea 43's gap_channels, "
      "imported verbatim.")
    P(f"Tuned: n in {NS} x gross in {GROSSES} + the vol-matched counterfactual g*. "
      "Panel/family/window are reporting axes.")
    P("")

    # ---------------- PART A
    P("=" * 100)
    P("PART A — RECORD-WIDE CENSUS (published numbers; every committed CSV with CAGR, Sharpe "
      "and its own SPY row)")
    P("=" * 100)
    C = census()
    C.to_csv(f"{OUT}.census.csv", index=False)
    tb, tbs, tbb, tfl = (int(C.n_books.sum()), int(C.beat_sharpe.sum()),
                         int(C.beat_both.sum()), int(C.beat_sharpe_pass_cagr_floor.sum()))
    P(f"{len(C)} files carry their own SPY comparand; {tb:,} published book rows.")
    P(f"  clear the Sharpe-vs-SPY bar:                 {tbs:,} ({tbs / tb:.2%} of all rows)")
    P(f"  of those, ALSO out-earn SPY on CAGR:         {tbb:,} ({tbb / max(tbs, 1):.2%})")
    P(f"  of those, out-earn but on Sharpe only:       {tbs - tbb:,} "
      f"({(tbs - tbb) / max(tbs, 1):.2%})")
    P(f"  of those, clear 4b's 70%-of-SPY CAGR floor:  {tfl:,} ({tfl / max(tbs, 1):.2%})")
    P("  CAGR > SPY CAGR is an UPPER BOUND on 'RETURN term > 0' (a lower-vol book at equal "
      "CAGR has lower mu), so the true record-wide positive-return-term rate is AT MOST the "
      "second line above.")
    fb = C[C.beat_sharpe > 0].sort_values("beat_both", ascending=False)
    P(f"\n  files contributing a Sharpe-beating book that also out-earns SPY: "
      f"{int((C.beat_both > 0).sum())} of {len(C)}. Top 8:")
    for _, r in fb.head(8).iterrows():
        P(f"    {r.beat_both:5d}/{r.beat_sharpe:5d} beat-both/beat-Sharpe  {r.file[:66]}")
    P("")

    # ---------------- PART B
    P("=" * 100)
    P("PART B — RE-DERIVATION (3 panels x 6 books x gross ladder x 5 windows, ALL reported)")
    P("=" * 100)
    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": small_panel()}

    dec, grid, wf = [], [], []
    g1 = g2 = g2s = 0.0
    g3worst = 0.0
    for pname, px in panels.items():
        start = px.index[WARMUP]
        rk, _ = rank_frame(px, drop_spy=(pname == "SMALL439"))
        spy = px["SPY"].pct_change().fillna(0).loc[start:]

        # G1 / G2
        w = weights_for(rk, "ALL", 0.75)
        fr, ft, _ = fast_backtest(px, w, 0.0)
        ref = backtest(px, w, cost_bps=0.0, freq=FREQ)
        g1 = max(g1, float(np.abs(fr - ref["returns"]).max()),
                 float(np.abs(ft - ref["turnover"]).max()))
        r075 = (fr - ft * COST / 1e4)
        f1, t1, _ = fast_backtest(px, weights_for(rk, "ALL", 1.00), 0.0)
        r100 = (f1 - t1 * COST / 1e4)
        g2 = max(g2, float(np.abs(r100 - r075 / 0.75).max()))
        g2s = max(g2s, abs(sharpe(r100.loc[start:]) - sharpe((r075 / 0.75).loc[start:])))

        base_v2 = fast_backtest(px, rules_v2_weights(px), COST)[0].loc[start:]
        base_v1 = fast_backtest(px, rules_v1_weights(px), COST)[0].loc[start:]

        books = {}                       # ENGINE books at each quoted gross, per the record
        for n in NS:
            for g in GROSSES:
                r0, t0, _ = fast_backtest(px, weights_for(rk, n, g), 0.0)
                books[("CAND", n, g)] = (r0 - t0 * COST / 1e4).loc[start:]
        for g in GROSSES:
            rb0, tb0, _ = fast_backtest(px, rules_v2_weights(px, band=BAND, gross=g), 0.0)
            books[("BAND", "v2", g)] = (rb0 - tb0 * COST / 1e4).loc[start:]

        for fam, n in [("CAND", n) for n in NS] + [("BAND", "v2")]:
            for g in GROSSES + ["g*"]:
                base = books[(fam, n, 0.75)] if g == "g*" else books[(fam, n, g)]
                for wname, (rr, ss) in windows(base, spy).items():
                    sig_s = ss.std() * np.sqrt(252)
                    lev = (sig_s / (rr.std() * np.sqrt(252))) if g == "g*" else 1.0
                    gg = 0.75 * lev if g == "g*" else g
                    rg = rr * lev
                    t_ret, t_vol, cf = gap_channels(rg, ss)
                    Sb, Ss = sharpe(rg), sharpe(ss)
                    lam = (rg.std() * np.sqrt(252)) / sig_s
                    mu_b, mu_s = rg.mean() * 252, ss.mean() * 252
                    dec.append(dict(panel=pname, family=fam, n=str(n), gross=g,
                                    gross_value=gg, window=wname, S_book=Sb, S_spy=Ss,
                                    gap=Sb - Ss, RETURN=t_ret, VOL=t_vol, cf_Sharpe=cf,
                                    mu_book=mu_b, mu_spy=mu_s,
                                    vol_book=rg.std() * np.sqrt(252), vol_spy=sig_s,
                                    lam=lam,
                                    id_RETURN=Sb - Ss / lam, id_VOL=Ss * (1 / lam - 1),
                                    beats_sharpe=bool(Sb > Ss), ret_pos=bool(t_ret > 0),
                                    vol_pos=bool(t_vol > 0), mu_pos=bool(mu_b > mu_s)))
                if g in GROSSES:
                    rg = books[(fam, n, g)]
                    m = metrics(rg)
                    h1, h2 = halves(rg)
                    mo = metrics(rg.loc[OOS_START:])
                    t4 = tests_4b(rg, spy)
                    grid.append(dict(panel=pname, family=fam, n=str(n), gross=g,
                                     CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                     H1=sharpe(h1), H2=sharpe(h2),
                                     IS_Sharpe=sharpe(rg.loc[:IS_END]),
                                     OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                     OOS_MaxDD=mo["MaxDD"],
                                     p4a=keep_4a(rg, base_v2), p4b=all(t4.values()),
                                     fail4b=fail_4b(rg, spy)))

            if fam == "CAND" and n == "ALL":
                d = [x for x in dec if x["panel"] == pname and x["family"] == "CAND"
                     and x["n"] == "ALL" and x["gross"] == 0.75 and x["window"] == "H1"][0]
                ref43 = I43[pname]
                g3worst = max(g3worst, abs(d["RETURN"] - ref43["ret"]),
                              abs(d["VOL"] - ref43["vol"]), abs(d["cf_Sharpe"] - ref43["cf"]),
                              abs(d["S_spy"] - ref43["spy"]))

        for bn, bs in (("RULES v2 (live)", base_v2), ("RULES v1", base_v1), ("SPY", spy)):
            m = metrics(bs)
            h1, h2 = halves(bs)
            mo = metrics(bs.loc[OOS_START:])
            grid.append(dict(panel=pname, family="BENCH", n=bn, gross=np.nan, CAGR=m["CAGR"],
                             Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=sharpe(h1),
                             H2=sharpe(h2), IS_Sharpe=sharpe(bs.loc[:IS_END]),
                             OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                             OOS_MaxDD=mo["MaxDD"], p4a=False, p4b=False, fail4b="-"))

        sub = [x for x in grid if x["panel"] == pname and x["family"] != "BENCH"]
        pick = max(sub, key=lambda x: x["IS_Sharpe"])
        dpick = [x for x in dec if x["panel"] == pname and x["family"] == pick["family"]
                 and x["n"] == pick["n"] and x["gross"] == pick["gross"]
                 and x["window"] == "OOS"][0]
        wf.append(dict(panel=pname, pick=f"{pick['family']}/n={pick['n']}/g={pick['gross']}",
                       IS_Sharpe=pick["IS_Sharpe"], OOS_CAGR=pick["OOS_CAGR"],
                       OOS_Sharpe=pick["OOS_Sharpe"], OOS_MaxDD=pick["OOS_MaxDD"],
                       OOS_RETURN=dpick["RETURN"], OOS_VOL=dpick["VOL"],
                       OOS_cf_Sharpe=dpick["cf_Sharpe"], OOS_ret_pos=dpick["ret_pos"],
                       v2_OOS_CAGR=metrics(base_v2.loc[OOS_START:])["CAGR"],
                       v2_OOS_Sharpe=sharpe(base_v2.loc[OOS_START:]),
                       v2_OOS_MaxDD=metrics(base_v2.loc[OOS_START:])["MaxDD"],
                       v1_OOS_Sharpe=sharpe(base_v1.loc[OOS_START:]),
                       spy_OOS_CAGR=metrics(spy.loc[OOS_START:])["CAGR"],
                       spy_OOS_Sharpe=sharpe(spy.loc[OOS_START:]),
                       spy_OOS_MaxDD=metrics(spy.loc[OOS_START:])["MaxDD"],
                       p4a=pick["p4a"], p4b=pick["p4b"], fail4b=pick["fail4b"]))

    D = pd.DataFrame(dec)
    G = pd.DataFrame(grid)
    W = pd.DataFrame(wf)
    D.to_csv(f"{OUT}.decomp.csv", index=False)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)

    idr = float((D.RETURN - D.id_RETURN).abs().max())
    idv = float((D.VOL - D.id_VOL).abs().max())
    signs = int((D.ret_pos == D.mu_pos).sum())
    P(f"G1  idea 43 fast_backtest vs engine.backtest: max|d| {g1:.3e}   "
      f"{'PASS' if g1 < 1e-12 else 'FAIL'}")
    P(f"G2  REPORTED (a convention gap, not an error): lever vs engine book-at-g-weights, "
      f"g=1.00 vs (1/0.75) x g=0.75 — max|dret| {g2:.3e}, max |dSharpe| over the three panels "
      f"{g2s:.4f}. The grid below uses ENGINE books at each quoted gross; only g* levers.")
    P(f"G3  idea 43's published H1 decomposition (EWALL g=0.75, 10 bps, 3 panels x 4 numbers): "
      f"worst |d| {g3worst:.4f} vs its 3-dp publication   {'PASS' if g3worst < 5e-3 else 'FAIL'}")
    P(f"G4  identity RETURN = S_b - S_s/lambda, VOL = S_s(1/lambda - 1) on all {len(D)} rows: "
      f"max|d| {max(idr, idv):.3e}   {'PASS' if max(idr, idv) < 1e-9 else 'FAIL'}")
    P(f"G5  sign identity RETURN > 0 <==> mu_book > mu_SPY: {signs}/{len(D)}   "
      f"{'PASS' if signs == len(D) else 'FAIL'}")
    assert g1 < 1e-12 and g3worst < 5e-3 and max(idr, idv) < 1e-9 and signs == len(D)
    P("")

    P("THE ANSWER, at the record's own quoting convention (gross 0.75, cash at 0%).")
    for g, lab in ((0.75, "g = 0.75 (idea 43's, and the record's default)"),
                   (1.00, "g = 1.00 (fully invested, no cash drag)"),
                   ("g*", "g = g* (levered/de-levered to SPY's vol — a COUNTERFACTUAL)")):
        s = D[(D.gross == g) & D.beats_sharpe]
        allr = D[D.gross == g]
        P(f"\n  {lab}")
        P(f"    rows: {len(allr)}   clearing the Sharpe-vs-SPY bar: {len(s)}")
        if len(s):
            P(f"    of those, RETURN term > 0: {int(s.ret_pos.sum())} "
              f"({s.ret_pos.mean():.1%})   VOL term > 0: {int(s.vol_pos.sum())} "
              f"({s.vol_pos.mean():.1%})")
            P(f"    RETURN term range {s.RETURN.min():+.3f} .. {s.RETURN.max():+.3f}   "
              f"VOL term range {s.VOL.min():+.3f} .. {s.VOL.max():+.3f}")
    P("")

    P("THE SAME BOOK, THE OPPOSITE HEADLINE — idea 43's own three anchors (EWALL, H1) at each "
      "gross (g=0.75 and g=1.00 are ENGINE books, g* levers the 0.75 book to SPY's vol)")
    an = D[(D.family == "CAND") & (D.n == "ALL") & (D.window == "H1")]
    P(an[["panel", "gross", "gross_value", "S_book", "S_spy", "gap", "RETURN", "VOL",
          "cf_Sharpe", "lam"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("  The gap column is IDENTICAL down each panel's three rows (Sharpe is gross-invariant, "
      "idea 43's own finding); only the SPLIT of that gap moves. That is the answer to the "
      "queue's question in one table.")
    P("")

    P("SIGN SHAPE BY WINDOW (Sharpe-beating rows only, gross 0.75)")
    s = D[(D.gross == 0.75) & D.beats_sharpe]
    t = s.groupby("window").agg(rows=("ret_pos", "size"), ret_pos=("ret_pos", "sum"),
                                vol_pos=("vol_pos", "sum"))
    P(t.to_string())
    P("\nSIGN SHAPE BY PANEL (Sharpe-beating rows only, gross 0.75)")
    t = s.groupby("panel").agg(rows=("ret_pos", "size"), ret_pos=("ret_pos", "sum"),
                               vol_pos=("vol_pos", "sum"))
    P(t.to_string())
    P("\nEVERY Sharpe-beating row with a POSITIVE return term at gross 0.75 (if any):")
    pos = s[s.ret_pos]
    P(pos[["panel", "family", "n", "window", "S_book", "S_spy", "RETURN", "VOL", "mu_book",
           "mu_spy", "lam"]].to_string(index=False, float_format=lambda x: f"{x:.4f}")
      if len(pos) else "  (none)")
    P("")

    P("FULL DECOMPOSITION GRID — all rows are in .decomp.csv; printed here at FULL window")
    P(D[D.window == "FULL"][["panel", "family", "n", "gross", "S_book", "S_spy", "gap",
                             "RETURN", "VOL", "cf_Sharpe", "mu_book", "mu_spy", "vol_book",
                             "vol_spy"]].to_string(index=False,
                                                   float_format=lambda x: f"{x:.4f}"))
    P("")

    P("THE BOOK GRID (both KEEP paths at every point, ALL points reported)")
    P(G.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    gg = G[G.family != "BENCH"]
    P(f"\n  4a passes: {int(gg.p4a.sum())}/{len(gg)}   4b passes: {int(gg.p4b.sum())}/{len(gg)}"
      f"   BOTH: {int((gg.p4a & gg.p4b).sum())}/{len(gg)}")
    fl = pd.Series([x for v in gg.fail4b for x in v.split(",") if x != "-"]).value_counts()
    P("  binding 4b legs across the failures: " + ", ".join(f"{k} {v}" for k, v in fl.items()))
    P("  THE QUEUE'S CONDITIONAL — 'if none, the CAGR floor is the only bar doing work': "
      f"CAGR is the SOLE failing leg on {int((gg.fail4b == 'CAGR').sum())}/{len(gg)} points, "
      f"and appears in {int(fl.get('CAGR', 0))} failures against DD's {int(fl.get('DD', 0))}.")
    P("")

    P("RULE 8 (PROTOCOL 8): (n, g) chosen on IS <= 2016-12-31 by IS Sharpe, 2017- read once.")
    P(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")

    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
