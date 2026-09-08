#!/usr/bin/env python3
"""Idea 404 — does ANY book pass BOTH KEEP paths (PROTOCOL 4a and 4b)?

Two parts.

  PART A (census of the record): parse research/LEADERBOARD.md and count how many
  committed rows claim a 4a pass, a 4b pass, and both together.

  PART B (constructive test, the part that can actually answer the question): the
  record's own claim (ideas 402/405/311) is that 4a's "MaxDD no worse than the live
  book" and 4b's "CAGR >= 70% of SPY" pull the SAME dial (gross) in OPPOSITE
  directions, so the two paths are exclusive by construction.  That is a testable
  statement about an interval, not a counting fact: for each book-form x panel,
  Sharpe is ~invariant in gross while CAGR and MaxDD scale with it, so
      4a gives an UPPER bound on gross (DD must stay <= the live book's DD)
      4b gives a LOWER bound on gross (CAGR must reach 70% of SPY's)
  and the paths are exclusive iff that interval is empty for every book.  We solve
  the interval by brute force on a 7-point gross grid over 6 book-forms x 3 panels
  and report EVERY grid point.

TUNED DIALS (max 2, per PROTOCOL 4): gross g and top-n n.  Panel, book-form and the
sample split are reported dimensions, not tuned: every cell is printed.

Costs 10 bps, weekly cadence, weights at t, applied t+1 (PROTOCOL 2).  Rule-8
walk-forward: dials chosen on the first half only, second half read once.

SURVIVORSHIP: the small panel is current constituents of a sub-$2B screen (see
data/SMALL_PANEL_README.md); broad136 is current large-cap constituents.  Both
overstate the level of every book on them, including the controls.
"""
import re, sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score, band_state  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, rebalance_mask, metrics  # noqa

COST = 10.0
FREQ = "W"
GROSS = [0.25, 0.375, 0.50, 0.625, 0.75, 0.875, 1.00]
NS = [10, 20, 30]

# ---------------------------------------------------------------- fast runner
def run(px, W, cost_bps=COST, freq=FREQ):
    """Vectorised clone of engine.backtest (gated below at 0.0)."""
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n, k = rets.shape
    cur = np.zeros(k); port = np.zeros(n); turn = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum(); cur = new.copy()
        port[i] = cur @ rets[i] - turn[i] * cost_bps / 1e4
        growth = cur * (1 + rets[i]); tot = growth.sum() + (1 - cur.sum())
        if tot > 0: cur = growth / tot
    return pd.Series(port, index=px.index)

def stats(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])

# ---------------------------------------------------------------- book forms
def ewall(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)

def band(px, g):
    return rules_v2_weights(px, band=0.03, gross=g)

def ma200(px, g):
    above = (px > px.rolling(200).mean()).astype(float).where(px.notna(), 0.0)
    n = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0).sum(axis=1)
    return g * above.div(n.replace(0, np.nan), axis=0).fillna(0.0)   # de-gross, never re-spread

def topn(px, g, n):
    s, above, vol20 = score(px, vol_scale=False)
    elig = s.where(above & (vol20 < 0.60))
    rank = elig.rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    return g * sel / n                                                # de-gross when < n eligible

BOOKS = ([("EWALL", lambda px, g: ewall(px, g), None),
          ("BAND(v2 form)", lambda px, g: band(px, g), None),
          ("MA200-EW", lambda px, g: ma200(px, g), None)] +
         [(f"TOP{n}", (lambda n: lambda px, g: topn(px, g, n))(n), n) for n in NS])

# ---------------------------------------------------------------- panels
def panels():
    out = {}
    out["u56"] = load_universe()
    out["broad136"] = load_universe(broad=True)
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in sm.columns if c == "SPY" or c not in bad]
    out[f"small{len(keep)-1}"] = sm[keep]
    return out

# ---------------------------------------------------------------- PART A
def census():
    txt = (ROOT / "research" / "LEADERBOARD.md").read_text().split("\n")
    rows = [l for l in txt if l.startswith("|") and not l.startswith("|---") and "| Date |" not in l]
    pat4a = re.compile(r"\b4a\b", re.I); pat4b = re.compile(r"\b4b\b", re.I)
    keep = [l for l in rows if re.search(r"\bKEEP\b", l)]
    k4a = [l for l in keep if pat4a.search(l)]
    k4b = [l for l in keep if pat4b.search(l)]
    both_txt = [l for l in rows if re.search(r"both\s*(paths|4a)", l, re.I)]
    # explicit machine-counted both-path claims published by earlier ideas
    both_counts = [l for l in rows if re.search(r"BOTH\s*\d+\s*/\s*\d+", l)]
    print(f"[A] LEADERBOARD rows parsed              : {len(rows)}")
    print(f"[A] rows whose verdict contains KEEP     : {len(keep)}")
    print(f"[A]   ...naming path 4a                  : {len(k4a)}")
    print(f"[A]   ...naming path 4b                  : {len(k4b)}")
    print(f"[A]   ...naming BOTH paths in one row    : {len([l for l in keep if pat4a.search(l) and pat4b.search(l)])}")
    print(f"[A] rows carrying a machine 'BOTH x/y'   : {len(both_counts)}")
    for l in both_counts[-6:]:
        m = re.search(r"BOTH\s*\d+\s*/\s*\d+", l)
        print(f"[A]     {m.group(0)}  <- {l[:70]}")
    return dict(rows=len(rows), keep=len(keep), k4a=len(k4a), k4b=len(k4b),
                both=len([l for l in keep if pat4a.search(l) and pat4b.search(l)]))

# ---------------------------------------------------------------- PART B
def bars(r, base, spy, oos_r=None, oos_base=None, oos_spy=None):
    """4a vs the live book on the same panel; 4b vs SPY. Returns flags + margins."""
    a = stats(r); b = stats(base); s = stats(spy)
    p4a = (a["H1"] > b["H1"]) and (a["H2"] > b["H2"]) and (a["MaxDD"] >= b["MaxDD"])
    p4b_h = (a["H1"] > s["H1"]) and (a["H2"] > s["H2"])
    p4b_dd = a["MaxDD"] >= 0.60 * s["MaxDD"]          # MaxDD negative: <= 60% of SPY's depth
    p4b_cg = a["CAGR"] >= 0.70 * s["CAGR"]
    d = dict(**{k: a[k] for k in a},
             a_h1=a["H1"] - b["H1"], a_h2=a["H2"] - b["H2"], a_dd=a["MaxDD"] - b["MaxDD"],
             b_h1=a["H1"] - s["H1"], b_h2=a["H2"] - s["H2"],
             b_dd=a["MaxDD"] - 0.60 * s["MaxDD"], b_cg=a["CAGR"] - 0.70 * s["CAGR"],
             pass4a=p4a, pass4b_full=p4b_h and p4b_dd and p4b_cg)
    if oos_r is not None:
        o, os_ = stats(oos_r), stats(oos_spy)
        d["oos_sharpe"] = o["Sharpe"]; d["oos_cagr"] = o["CAGR"]; d["oos_maxdd"] = o["MaxDD"]
        d["b_oos"] = o["Sharpe"] - os_["Sharpe"]
    return d

def main():
    print("=" * 100); print("PART A — census of the committed record"); print("=" * 100)
    cen = census()

    print(); print("=" * 100); print("PART B — solve the 4a/4b gross interval, all grid points"); print("=" * 100)
    P = panels()
    recs = []
    gate_done = False
    for pname, px in P.items():
        spy_full = px["SPY"].pct_change().fillna(0.0)
        start = px.index[260]
        basew = rules_v2_weights(px, band=0.03, gross=0.75)
        base_r = run(px, basew).loc[start:]
        if not gate_done:                                   # GATE: fast runner vs engine
            eng = backtest(px, basew, cost_bps=COST, freq=FREQ)["returns"].loc[start:]
            print(f"[GATE] max|run - engine.backtest| on {pname} v2 book = {np.abs(base_r - eng).max():.3e}")
            gate_done = True
        spy = spy_full.loc[start:]
        h = len(spy) // 2
        for bname, fn, nval in BOOKS:
            for g in GROSS:
                r = run(px, fn(px, g)).loc[start:]
                d = bars(r, base_r, spy,
                         oos_r=r.iloc[h:], oos_base=base_r.iloc[h:], oos_spy=spy.iloc[h:])
                d.update(panel=pname, book=bname, n=nval, gross=g)
                recs.append(d)
        b, s = stats(base_r), stats(spy)
        print(f"\n[{pname}]  live v2 book: CAGR {b['CAGR']:.2%} Sharpe {b['Sharpe']:.3f} "
              f"MaxDD {b['MaxDD']:.2%} H1/H2 {b['H1']:.3f}/{b['H2']:.3f}")
        print(f"[{pname}]  SPY         : CAGR {s['CAGR']:.2%} Sharpe {s['Sharpe']:.3f} "
              f"MaxDD {s['MaxDD']:.2%} H1/H2 {s['H1']:.3f}/{s['H2']:.3f}")
        print(f"[{pname}]  4a DD bar {b['MaxDD']:.2%} (upper bound on gross) | "
              f"4b DD cap {0.60*s['MaxDD']:.2%}, 4b CAGR floor {0.70*s['CAGR']:.2%} (lower bound on gross)")

    df = pd.DataFrame(recs)
    df.to_csv(ROOT / "research" / "backtests" / "2026-09-08_both-paths_grid.csv", index=False)

    print("\n" + "=" * 100); print("ALL GRID POINTS (126 arms)"); print("=" * 100)
    cols = ["panel", "book", "gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
            "a_h1", "a_h2", "a_dd", "b_cg", "b_dd", "b_oos", "pass4a", "pass4b_full"]
    with pd.option_context("display.width", 250, "display.max_rows", 300):
        print(df[cols].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    print("\n" + "=" * 100); print("COUNTS"); print("=" * 100)
    df["both"] = df.pass4a & df.pass4b_full
    print(f"arms                     : {len(df)}")
    print(f"pass 4a                  : {df.pass4a.sum()}")
    print(f"pass 4b (full sample)    : {df.pass4b_full.sum()}")
    print(f"pass BOTH                : {df.both.sum()}")
    print("\nby panel:")
    print(df.groupby("panel")[["pass4a", "pass4b_full", "both"]].sum().to_string())
    print("\nby book-form:")
    print(df.groupby("book")[["pass4a", "pass4b_full", "both"]].sum().to_string())

    print("\n" + "=" * 100); print("THE INTERVAL (the queue's mechanism, priced)"); print("=" * 100)
    print("For each panel x book: the largest gross still passing 4a's DD bar (g_a_max) and the")
    print("smallest gross still passing 4b's CAGR floor (g_b_min). Exclusive iff g_b_min > g_a_max.")
    rowsI = []
    for (pn, bk), sub in df.groupby(["panel", "book"]):
        ga = sub.loc[sub.a_dd >= 0, "gross"]
        gb = sub.loc[sub.b_cg >= 0, "gross"]
        rowsI.append(dict(panel=pn, book=bk,
                          g_a_max=ga.max() if len(ga) else np.nan,
                          g_b_min=gb.min() if len(gb) else np.nan,
                          a_sharpe_ok=bool((sub.a_h1 > 0).any() and (sub.a_h2 > 0).any()),
                          b_sharpe_ok=bool((sub.b_h1 > 0).any() and (sub.b_h2 > 0).any()),
                          overlap=bool(len(ga) and len(gb) and gb.min() <= ga.max())))
    I = pd.DataFrame(rowsI)
    print(I.to_string(index=False))
    print(f"\nbook x panel cells with a non-empty DD/CAGR gross overlap: "
          f"{int(I.overlap.sum())} / {len(I)}")

    print("\n" + "=" * 100); print("RULE 8 — walk-forward (dials chosen on H1 only, H2 read once)")
    print("=" * 100)
    for pname, px in P.items():
        spy = px["SPY"].pct_change().fillna(0.0).loc[px.index[260]:]
        h = len(spy) // 2
        sub = df[df.panel == pname].copy()
        # IS = first half; choose the arm with the best H1 Sharpe among 4a-DD-eligible arms
        pick_all = sub.loc[sub.H1.idxmax()]
        print(f"\n[{pname}] IS-Sharpe chooser picks {pick_all.book} g={pick_all.gross} "
              f"(H1 {pick_all.H1:.3f}) -> OOS Sharpe {pick_all.oos_sharpe:.3f} "
              f"CAGR {pick_all.oos_cagr:.2%} MaxDD {pick_all.oos_maxdd:.2%}")
        pxi = P[pname]
        base_oos = run(pxi, rules_v2_weights(pxi, gross=0.75)).loc[pxi.index[260]:].iloc[h:]
        bo, so = stats(base_oos), stats(spy.iloc[h:])
        print(f"[{pname}]   OOS live v2: Sharpe {bo['Sharpe']:.3f} CAGR {bo['CAGR']:.2%} MaxDD {bo['MaxDD']:.2%}")
        print(f"[{pname}]   OOS SPY    : Sharpe {so['Sharpe']:.3f} CAGR {so['CAGR']:.2%} MaxDD {so['MaxDD']:.2%}")
        print(f"[{pname}]   OOS 4a pass: {pick_all.oos_sharpe > bo['Sharpe'] and pick_all.oos_maxdd >= bo['MaxDD']}"
              f" | OOS 4b pass: {pick_all.oos_sharpe > so['Sharpe'] and pick_all.oos_maxdd >= 0.60*so['MaxDD'] and pick_all.oos_cagr >= 0.70*so['CAGR']}")

    # ------------------------------------------------------------ PART C
    # Idea 142 (committed the same day, independently) reports the record's FIRST
    # both-paths rows: a ranked top-20 book blended 50/50 with a TLT/GLD/UUP sleeve,
    # band-gated in the RE-WEIGHT convention.  That is a direct counterexample to
    # "exclusive by construction" IF the exclusion is a law rather than a statement
    # about books that differ only by gross.  Test it: add the sleeve dial f and ask
    # whether the DD/CAGR gross interval opens.  Dials for this part: (f, g).
    print("\n" + "=" * 100)
    print("PART C — does a DIVERSIFYING SLEEVE open the interval? (dials: sleeve f, gross g)")
    print("=" * 100)
    SLEEVE = ["TLT", "GLD", "UUP"]
    FS = [0.0, 0.25, 0.50, 0.75]
    recs2 = []
    for pname in ("u56", "broad136"):
        px = P[pname]
        sl = [t for t in SLEEVE if t in px.columns]
        start = px.index[260]
        base_r = run(px, rules_v2_weights(px, gross=0.75)).loc[start:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        h = len(spy) // 2
        s, above, vol20 = score(px, vol_scale=False)
        eq_cols = [c for c in px.columns if c not in sl and c != "SPY"]
        elig = s[eq_cols].where(above[eq_cols] & (vol20[eq_cols] < 0.60))
        sel = (elig.rank(axis=1, ascending=False) <= 20).astype(float)
        bs = band_state(px, 0.03)
        for f in FS:
            eqw = sel.where(bs[eq_cols], 0.0)                      # band gate
            eqw = eqw.div(eqw.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)  # RE-WEIGHT
            slw = pd.DataFrame(0.0, index=px.index, columns=px.columns)
            if sl:
                a = (px[sl].notna()).astype(float).where(bs[sl], 0.0)
                a = a.div(a.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
                slw[sl] = a
            W0 = pd.DataFrame(0.0, index=px.index, columns=px.columns)
            W0[eq_cols] = eqw * (1 - f)
            W0 = W0 + slw * f
            for g in GROSS:
                r = run(px, g * W0).loc[start:]
                d = bars(r, base_r, spy, oos_r=r.iloc[h:], oos_base=base_r.iloc[h:], oos_spy=spy.iloc[h:])
                d.update(panel=pname, book=f"TOP20+SLV f={f:.2f} (reweight)", f=f, gross=g)
                recs2.append(d)
    C = pd.DataFrame(recs2)
    C["both"] = C.pass4a & C.pass4b_full
    C.to_csv(ROOT / "research" / "backtests" / "2026-09-08_both-paths_sleeve.csv", index=False)
    cols2 = ["panel", "f", "gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
             "a_h1", "a_h2", "a_dd", "b_cg", "b_dd", "b_oos", "pass4a", "pass4b_full", "both"]
    with pd.option_context("display.width", 250, "display.max_rows", 200):
        print(C[cols2].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print(f"\nPART C arms {len(C)} | pass4a {C.pass4a.sum()} | pass4b {C.pass4b_full.sum()} | BOTH {C.both.sum()}")
    for (pn, f), sub in C.groupby(["panel", "f"]):
        ga = sub.loc[sub.a_dd >= 0, "gross"]; gb = sub.loc[sub.b_cg >= 0, "gross"]
        ov = bool(len(ga) and len(gb) and gb.min() <= ga.max())
        print(f"  {pn:9s} f={f:.2f}  g_a_max={ga.max() if len(ga) else np.nan}  "
              f"g_b_min={gb.min() if len(gb) else np.nan}  overlap={ov}")
    return df, cen, C

if __name__ == "__main__":
    main()
