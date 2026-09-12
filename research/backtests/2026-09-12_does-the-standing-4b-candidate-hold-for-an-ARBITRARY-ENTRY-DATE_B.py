#!/usr/bin/env python3
"""Idea 827 (lane B, 2026-09-12) — does the record's standing 4b candidate hold for an
ARBITRARY ENTRY DATE?

DIAGNOSIS THIS RUN IS GROUNDED IN.  The record's one surviving zero-tuned-parameter 4b
candidate is idea 794's control: the LIVE band book with gross moved 0.75 -> 1.00
(`baseline.rules_v2_weights(px, band=0.03, gross=1.00)`, U56, weekly, 10 bps).  Its memo
(`2026-09-11_u56-band003-gross100_4b_B_MEMO.md`) reports full 11.52%/1.1996/-15.91% and OOS
12.66%/1.2740/-15.91%, all five 4b legs passing full AND OOS.  But every number the record
holds on it -- and every 4b verdict in the record generally -- is computed on ONE fixed
window (2009-01-13 .. today) with ONE half split.  Real capital does not enter on
2009-01-13.  It enters on one date and holds for a finite horizon, and it is the realised
Sharpe / drawdown / CAGR of THAT window, against SPY over THAT SAME window, that decides
whether the commitment was right.

THE QUESTION.  Over every entry date in the sample, for holding horizons of 3/4/5/7.5
years, how often would an entrant have seen the candidate clear PROTOCOL 4b against SPY
*measured on their own window*?  And is the gross-1.00 candidate better than the live
gross-0.75 book for such an entrant, or only on the record's one fixed window?

TUNED PARAMETERS: exactly 2 -- (H = holding horizon, s = entry spacing).  All 4 x 2 = 8
grid points reported.  The BOOK itself has zero tuned parameters (band = live 0.03, gross =
the PROTOCOL no-leverage bound 1.00), which is the whole point of the candidate.

CONVENTIONS, DECLARED BEFORE ANY NUMBER:
  C1  Each book's daily return series is run ONCE over the full sample (engine.backtest,
      weights decided at close t applied at t+1, cost_bps=10, freq='W') and windows are
      slices of it.  So the entrant JOINS a running strategy already holding its weights.
      Sensitivity S1 charges a full cold-start turnover (gross x 10 bps) on the entry day.
  C2  A window's 4b legs are read WINDOW-LOCALLY against SPY over the same window: Sharpe
      (full window), Sharpe in both window-local halves, MaxDD >= 0.6 x SPY's MaxDD,
      CAGR >= 0.7 x SPY's CAGR.  PASS_4b requires all four.
  C3  The CAGR floor is applied LITERALLY, including when SPY's window CAGR is negative
      (floor = 0.7 x a negative number is ABOVE it, i.e. strictly harder).  The count of
      such windows is reported, with sensitivity S2 = floor becomes SPY's own CAGR there.
  C4  Warm-up: entry dates start at px.index[260], as baseline.compare does.
  C5  A window must lie wholly inside the sample; the last entry is len(px) - H.

PRE-REGISTERED HYPOTHESES (written before the grid was run; all reported either way):
  H_ENTRY   joint 4b pass share >= 0.80 at the headline cell (H = 1260d, s = 21d).
  H_SHARPE  the full-window Sharpe leg alone holds in >= 0.90 of windows at the headline.
  H_WORST   the DD leg holds in EVERY window at the headline (share = 1.0000), i.e. the
            candidate's drawdown advantage over SPY is not a fixed-window artefact.
  H_GROSS   the gross-1.00 candidate's joint pass share EXCEEDS the live gross-0.75 book's
            at all 8 grid points (raising gross helps an arbitrary entrant, not just the
            record's one window).
  H_WF      (rule 8) the horizon chosen on IS entries alone transports: |OOS share - IS
            share| <= 0.10 at the IS-chosen H.

Run: python3 research/backtests/2026-09-12_does-the-standing-4b-candidate-hold-for-an-ARBITRARY-ENTRY-DATE_B.py
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import (load_universe, rules_v1_weights, rules_v2_weights,  # noqa: E402
                      compare, backtest, metrics)

OUT = Path(__file__).with_suffix("")
COST, FREQ = 10, "W"
BAND = 0.03                      # LIVE band, frozen, not tuned
HORIZONS = [756, 1008, 1260, 1890]      # 3y, 4y, 5y, 7.5y in trading days
SPACINGS = [21, 63]                     # monthly, quarterly entry grids
HEAD_H, HEAD_S = 1260, 21               # headline cell, named before the run
OOS_START = pd.Timestamp("2017-01-01")  # rule 8
IS_END = pd.Timestamp("2016-12-31")
pd.set_option("display.width", 200)


def hdr(s):
    print("\n" + "=" * 100 + f"\n{s}\n" + "=" * 100)


# ---------------------------------------------------------------- books, run once (C1)
def build_books(px):
    books = {}
    for name, wf in [("CAND g=1.00", lambda p: rules_v2_weights(p, band=BAND, gross=1.00)),
                     ("LIVE g=0.75", lambda p: rules_v2_weights(p, band=BAND, gross=0.75)),
                     ("RULES v1", rules_v1_weights)]:
        books[name] = backtest(px, wf(px), cost_bps=COST, freq=FREQ)["returns"]
    books["SPY"] = px["SPY"].pct_change().fillna(0.0)
    return books


def m3(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def halves_sharpe(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


# ---------------------------------------------------------------- gates
def gates(books, start):
    hdr("GATES — reproduction of the committed candidate, printed BEFORE any new number")
    pub = {  # memo 2026-09-11_u56-band003-gross100_4b_B_MEMO.md + PROTOCOL comparands
        ("CAND g=1.00", "full"): (0.1152, 1.1996, -0.1591),
        ("CAND g=1.00", "oos"):  (0.1266, 1.2740, -0.1591),
        ("SPY", "full"):         (0.1516, 0.8860, -0.3372),
    }
    rows = []
    for (bk, win), (c, s, d) in pub.items():
        r = books[bk].loc[start:] if win == "full" else books[bk].loc[OOS_START:]
        gc, gs, gd = m3(r)
        ok = abs(gc - c) <= 0.010 and abs(gs - s) <= 0.060 and abs(gd - d) <= 0.020
        rows.append(dict(gate=f"{bk}/{win}", pub_CAGR=c, got_CAGR=gc, pub_Sharpe=s,
                         got_Sharpe=gs, pub_MaxDD=d, got_MaxDD=gd,
                         verdict="PASS" if ok else "FAIL"))
    g = pd.DataFrame(rows)
    print(g.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    print("Tolerance declared: |dCAGR|<=1.00pp, |dSharpe|<=0.060, |dMaxDD|<=2.00pp "
          "(data/prices.csv was re-cached 2026-09-12; the memo ran on the 2026-09-10 vintage).")
    print(f"GATES: {(g.verdict == 'PASS').sum()} of {len(g)} PASS")
    g.to_csv(f"{OUT}.gates.csv", index=False)
    return g


# ---------------------------------------------------------------- the entry-date census
def census(books, start):
    """One row per (book, H, s, entry date): window-local metrics and the four 4b legs."""
    idx = books["SPY"].index
    i0 = idx.get_loc(start)
    rows = []
    for H in HORIZONS:
        for s in SPACINGS:
            entries = range(i0, len(idx) - H + 1, s)
            for i in entries:
                sl = slice(i, i + H)
                sc, ss_ = m3(books["SPY"].iloc[sl]), None
                spy = books["SPY"].iloc[sl]
                s_c, s_s, s_d = m3(spy)
                s_h1, s_h2 = halves_sharpe(spy)
                for bk in ("CAND g=1.00", "LIVE g=0.75", "RULES v1"):
                    r = books[bk].iloc[sl]
                    c, sh, dd = m3(r)
                    h1, h2 = halves_sharpe(r)
                    L_sh = sh > s_s
                    L_hv = (h1 > s_h1) and (h2 > s_h2)
                    L_dd = dd >= 0.6 * s_d                  # both negative: >= is shallower
                    L_cg = c >= 0.7 * s_c                   # C3, literal
                    L_cg2 = c >= (s_c if s_c <= 0 else 0.7 * s_c)   # S2 sensitivity
                    rows.append(dict(book=bk, H=H, s=s, entry=idx[i], end=idx[i + H - 1],
                                     CAGR=c, Sharpe=sh, MaxDD=dd, h1=h1, h2=h2,
                                     spy_CAGR=s_c, spy_Sharpe=s_s, spy_MaxDD=s_d,
                                     L_sharpe=L_sh, L_halves=L_hv, L_dd=L_dd, L_cagr=L_cg,
                                     L_cagr_S2=L_cg2,
                                     PASS=bool(L_sh and L_hv and L_dd and L_cg),
                                     PASS_S2=bool(L_sh and L_hv and L_dd and L_cg2),
                                     spy_neg=bool(s_c <= 0)))
    return pd.DataFrame(rows)


def grid_table(cen):
    g = (cen.groupby(["book", "H", "s"])
            .agg(n=("PASS", "size"), pass_4b=("PASS", "mean"), pass_S2=("PASS_S2", "mean"),
                 leg_sharpe=("L_sharpe", "mean"), leg_halves=("L_halves", "mean"),
                 leg_dd=("L_dd", "mean"), leg_cagr=("L_cagr", "mean"),
                 med_CAGR=("CAGR", "median"), med_Sharpe=("Sharpe", "median"),
                 worst_MaxDD=("MaxDD", "min"), spy_neg=("spy_neg", "sum"))
            .reset_index())
    return g


# ---------------------------------------------------------------- rule 8
def rule8_entry(cen):
    hdr("RULE 8 (a) — on THIS RUN'S OWN TUNED PARAMETER: H picked on IS entries only")
    c = cen[(cen.book == "CAND g=1.00") & (cen.s == HEAD_S)].copy()
    is_ = c[c.end <= IS_END]
    oos = c[c.entry >= OOS_START]
    tab = []
    for H in HORIZONS:
        i, o = is_[is_.H == H], oos[oos.H == H]
        tab.append(dict(H=H, n_IS=len(i), IS_pass=i.PASS.mean() if len(i) else np.nan,
                        n_OOS=len(o), OOS_pass=o.PASS.mean() if len(o) else np.nan))
    t = pd.DataFrame(tab)
    print(t.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    valid = t.dropna(subset=["IS_pass"])
    if len(valid) == 0 or valid.n_IS.max() == 0:
        print("No IS window of any horizon closes by 2016-12-31 -> H is NOT selectable on IS; "
              "reported as such, nothing is chosen.")
        return t, None
    pick = int(valid.sort_values(["IS_pass", "n_IS"], ascending=[False, False]).iloc[0].H)
    row = t[t.H == pick].iloc[0]
    print(f"IS-chosen H = {pick} (IS pass {row.IS_pass:.4f} on {int(row.n_IS)} windows) -> "
          f"OOS pass {row.OOS_pass:.4f} on {int(row.n_OOS)} windows, read ONCE.")
    print(f"H_WF: |OOS - IS| = {abs(row.OOS_pass - row.IS_pass):.4f} vs bar 0.10 -> "
          f"{'PASS' if abs(row.OOS_pass - row.IS_pass) <= 0.10 else 'FAIL'}")
    return t, pick


def rule8_books(books, start):
    hdr("RULE 8 (b) — MANDATED BOOK LEG: OOS 2017-2026 CAGR/Sharpe/MaxDD vs baseline and SPY")
    rows = []
    for bk in ("CAND g=1.00", "LIVE g=0.75", "RULES v1", "SPY"):
        f = books[bk].loc[start:]
        o = books[bk].loc[OOS_START:]
        fc, fs, fd = m3(f); oc, os_, od = m3(o)
        fh1, fh2 = halves_sharpe(f); oh1, oh2 = halves_sharpe(o)
        rows.append(dict(book=bk, full_CAGR=fc, full_Sharpe=fs, full_MaxDD=fd,
                         full_H1=fh1, full_H2=fh2,
                         OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od, OOS_H1=oh1, OOS_H2=oh2))
    t = pd.DataFrame(rows).set_index("book")
    print(t.to_string(float_format=lambda x: f"{x:+.4f}"))
    spy = t.loc["SPY"]
    print("\n4b legs on the FIXED window (the record's convention), for reference:")
    for bk in ("CAND g=1.00", "LIVE g=0.75", "RULES v1"):
        r = t.loc[bk]
        legs = {
            "Sharpe>SPY both halves (full)": r.full_H1 > spy.full_H1 and r.full_H2 > spy.full_H2,
            "Sharpe>SPY both halves (OOS)": r.OOS_H1 > spy.OOS_H1 and r.OOS_H2 > spy.OOS_H2,
            "OOS Sharpe>SPY": r.OOS_Sharpe > spy.OOS_Sharpe,
            "MaxDD<=60% SPY (full)": r.full_MaxDD >= 0.6 * spy.full_MaxDD,
            "CAGR>=70% SPY (full)": r.full_CAGR >= 0.7 * spy.full_CAGR,
            "MaxDD<=60% SPY (OOS)": r.OOS_MaxDD >= 0.6 * spy.OOS_MaxDD,
            "CAGR>=70% SPY (OOS)": r.OOS_CAGR >= 0.7 * spy.OOS_CAGR,
        }
        print(f"  {bk:14s} 4b {'PASS' if all(legs.values()) else 'FAIL'}  "
              + "  ".join(f"{k}={'Y' if v else 'N'}" for k, v in legs.items()))
    t.to_csv(f"{OUT}.books.csv")
    return t


# ---------------------------------------------------------------- sensitivity S1
def cold_start(books, cen, start):
    hdr("SENSITIVITY S1 — charge a COLD-START turnover (gross x 10 bps) on the entry day")
    idx = books["SPY"].index
    out = []
    for bk, gross in (("CAND g=1.00", 1.00), ("LIVE g=0.75", 0.75)):
        r = books[bk].copy()
        sub = cen[(cen.book == bk) & (cen.H == HEAD_H) & (cen.s == HEAD_S)]
        hits = 0
        for _, row in sub.iterrows():
            i = idx.get_loc(row.entry)
            w = r.iloc[i:i + HEAD_H].copy()
            w.iloc[0] -= gross * COST / 1e4
            spy = books["SPY"].iloc[i:i + HEAD_H]
            c, sh, dd = m3(w); s_c, s_s, s_d = m3(spy)
            h1, h2 = halves_sharpe(w); sh1, sh2 = halves_sharpe(spy)
            hits += bool(sh > s_s and h1 > sh1 and h2 > sh2 and dd >= 0.6 * s_d
                         and c >= 0.7 * s_c)
        out.append(dict(book=bk, n=len(sub), pass_warm=sub.PASS.mean(),
                        pass_cold=hits / len(sub)))
    t = pd.DataFrame(out)
    print(t.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    return t


# ---------------------------------------------------------------- main
def main():
    px = load_universe()
    start = px.index[260]
    print(f"Panel U56: {px.shape[1]} columns, {px.index[0].date()} .. {px.index[-1].date()}; "
          f"scored from {start.date()} (C4).  cost {COST} bps, freq {FREQ}, band {BAND}.")
    books = build_books(px)
    gates(books, start)

    hdr("KEEP PATHS on the fixed window (PROTOCOL rule 4, via baseline.compare)")
    res_cand = compare("CAND band0.03 g=1.00 (U56 W)",
                       lambda p: rules_v2_weights(p, band=BAND, gross=1.00), px,
                       freq=FREQ, cost_bps=COST)
    print()
    res_live = compare("LIVE band0.03 g=0.75 (U56 W)",
                       lambda p: rules_v2_weights(p, band=BAND, gross=0.75), px,
                       freq=FREQ, cost_bps=COST)

    bt = rule8_books(books, start)

    hdr("THE ENTRY-DATE CENSUS — ALL 8 GRID POINTS (H x s), every point reported")
    cen = census(books, start)
    cen.to_csv(f"{OUT}.census.csv.gz", index=False, compression="gzip")
    g = grid_table(cen)
    g.to_csv(f"{OUT}.grid.csv", index=False)
    for bk in ("CAND g=1.00", "LIVE g=0.75", "RULES v1"):
        print(f"\n--- {bk} ---")
        print(g[g.book == bk].drop(columns=["book"]).to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))

    hdr("PRE-REGISTERED HYPOTHESES")
    hc = g[(g.book == "CAND g=1.00") & (g.H == HEAD_H) & (g.s == HEAD_S)].iloc[0]
    hl = g[(g.book == "LIVE g=0.75") & (g.H == HEAD_H) & (g.s == HEAD_S)].iloc[0]
    verd = {}
    verd["H_ENTRY"] = (hc.pass_4b >= 0.80, f"joint 4b pass {hc.pass_4b:.4f} vs bar 0.80 "
                                           f"(n={int(hc.n)} windows, H={HEAD_H}d s={HEAD_S}d)")
    verd["H_SHARPE"] = (hc.leg_sharpe >= 0.90, f"Sharpe leg {hc.leg_sharpe:.4f} vs bar 0.90")
    verd["H_WORST"] = (hc.leg_dd >= 1.0, f"DD leg {hc.leg_dd:.4f} vs bar 1.0000")
    cmp_ = g.pivot_table(index=["H", "s"], columns="book", values="pass_4b")
    wins = (cmp_["CAND g=1.00"] > cmp_["LIVE g=0.75"]).sum()
    verd["H_GROSS"] = (wins == len(cmp_), f"CAND > LIVE at {wins} of {len(cmp_)} grid points")
    for k, (ok, why) in verd.items():
        print(f"  {k:9s} {'PASS' if ok else 'FAIL'}  — {why}")
    print("\nCAND vs LIVE joint 4b pass share at every grid point:")
    print(cmp_.to_string(float_format=lambda x: f"{x:.4f}"))

    wf, pick = rule8_entry(cen)
    wf.to_csv(f"{OUT}.wf.csv", index=False)

    s1 = cold_start(books, cen, start)

    hdr("C3 — windows where SPY's CAGR is negative (the literal floor is HARDER there)")
    neg = cen[(cen.book == "CAND g=1.00")].groupby(["H", "s"]).agg(
        n=("spy_neg", "size"), n_spy_neg=("spy_neg", "sum"),
        pass_literal=("PASS", "mean"), pass_S2=("PASS_S2", "mean")).reset_index()
    print(neg.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    hdr("WHICH LEG BINDS, and WHEN — headline cell, failing windows only")
    f = cen[(cen.book == "CAND g=1.00") & (cen.H == HEAD_H) & (cen.s == HEAD_S) & (~cen.PASS)]
    if len(f):
        binding = pd.DataFrame({
            "leg": ["sharpe", "halves", "dd", "cagr"],
            "fails": [(~f.L_sharpe).sum(), (~f.L_halves).sum(), (~f.L_dd).sum(),
                      (~f.L_cagr).sum()]})
        print(binding.to_string(index=False))
        print(f"\n{len(f)} failing windows of {int(hc.n)}; entry dates "
              f"{f.entry.min().date()} .. {f.entry.max().date()}")
        print(f.groupby(f.entry.dt.year).size().to_string())
        print("\nworst 8 failing windows by dSharpe:")
        f2 = f.assign(dSharpe=f.Sharpe - f.spy_Sharpe).nsmallest(8, "dSharpe")
        print(f2[["entry", "end", "CAGR", "Sharpe", "MaxDD", "spy_CAGR", "spy_Sharpe",
                  "spy_MaxDD", "L_sharpe", "L_halves", "L_dd", "L_cagr"]].to_string(
            index=False, float_format=lambda x: f"{x:+.4f}"))
    else:
        print("No failing windows at the headline cell.")

    hdr("VERDICT INPUTS")
    print(f"4a (vs RULES v2): CAND {res_cand['verdict']} / LIVE {res_live['verdict']}")
    print(f"4b on the fixed window: see RULE 8 (b) block above.")
    print(f"Entry-date joint 4b pass share, headline: CAND {hc.pass_4b:.4f}, "
          f"LIVE {hl.pass_4b:.4f}")
    print("LEADERBOARD rows were emitted by compare() above; the entry-census rows are in "
          f"{Path(OUT).name}.grid.csv")


if __name__ == "__main__":
    main()
