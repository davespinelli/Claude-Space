#!/usr/bin/env python3
"""Idea 1261 — is ALWAYS-ACT the DEFAULT the record never declared and cannot afford?

1252 reported that acting on every IS argmax gives mean OOS Sharpe 0.8357 against 0.8268 for
doing nothing and 0.8254 for the incumbent decisiveness bar, yet it destroys 18 of the anchor's
24 4b passes (24 -> 6).  Those two facts were measured over a pool of decisions, not on a book.
This script prices ALWAYS-ACT as a book an account could actually hold, per panel and per ladder,
and asks whether the Sharpe gain and the 4b loss can both be true of ONE book.

Selectors, all three realised as one stitched return stream an account could hold:
  INCUMBENT   the frozen 2026-09-04 KEEP 4b book (N=20, gross 0.75, weekly), never re-picked.
  ANCHOR      the IS-argmax rung at the FIRST fold, then held forever (one book, one decision).
  ALWAYS_ACT  the IS-argmax rung re-picked at EVERY fold (expanding IS window, Sharpe).

The thing 1252's pooled averaging cannot see, and the reason this script exists: a switch costs
money.  When ALWAYS_ACT moves between rungs the account must trade |w_new - w_old| at the same
10 bps every other trade pays.  That charge is levied here on the switch date, from the two books'
actual held (drifted) weights.  SWITCH_FREE is reported beside it so the rebate is visible.

Two tuned parameters ONLY: ladder (4) x panel (3).  All cells reported.
Rule 8: every decision uses a strictly trailing expanding window; the anchor is pinned on
warm-up..2016-12-31 and 2017-2026 is read once.

Costs 10 bps, next-day execution (engine).  Deterministic.
"""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics  # noqa

OUT = Path(__file__).with_suffix("")
COST_BPS = 10
OOS_START = pd.Timestamp("2017-01-01")     # rule 8 boundary, frozen before any result was read
FOLD_YEARS = range(2013, 2026)             # decision at each year-end; first decision 2012-12-31
INCUMBENT = dict(n=20, gross=0.75, freq="W", k=1.0)


# ---------------------------------------------------------------- the book family
def book_weights(px, n=20, gross=0.75, k=1.0):
    """2026-09-04 KEEP 4b book, with the composite's three lookbacks scaled by k.
    Composite WITHOUT the vol scaler; above-200d eligible; top-n at gross/n each; the
    shortfall when fewer than n are eligible goes to cash (never re-spread)."""
    w_mom, w_lag, w6, w3 = int(round(252 * k)), int(round(21 * k)), int(round(126 * k)), int(round(63 * k))
    mom = px.shift(w_lag) / px.shift(w_mom) - 1
    r6 = px / px.shift(w6) - 1
    r3 = px / px.shift(w3) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3
    above = px > px.rolling(200).mean()
    s = comp * (0.5 + 0.5 * above.astype(float))
    rank = s.where(above).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (gross / n)


# ladders: each is a list of (label, book kwargs) around the incumbent, one dial moved
LADDERS = {
    "N":       [(f"N{n}",    dict(INCUMBENT, n=n))       for n in (5, 10, 15, 20, 30, 40)],
    "GROSS":   [(f"G{g:.2f}", dict(INCUMBENT, gross=g))  for g in (0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00)],
    "CADENCE": [(f"C{f}",    dict(INCUMBENT, freq=f))    for f in ("D", "W", "M", "Q")],
    "MOM":     [(f"K{k:g}",  dict(INCUMBENT, k=k))       for k in (0.5, 0.75, 1.0, 1.5, 2.0)],
}


def run_books(px):
    """Every distinct rung across all four ladders, backtested once."""
    specs = {}
    for rungs in LADDERS.values():
        for lab, kw in rungs:
            specs.setdefault(lab, kw)
    out = {}
    for lab, kw in specs.items():
        w = book_weights(px, n=kw["n"], gross=kw["gross"], k=kw["k"])
        out[lab] = backtest(px, w, cost_bps=COST_BPS, freq=kw["freq"])
    return out


# ---------------------------------------------------------------- selectors
def fold_dates(idx):
    """Last trading day of each year in FOLD_YEARS-1 .. i.e. the decision dates."""
    ye = pd.Series(idx.year, index=idx)
    lasts = idx[(ye != ye.shift(-1)).values]
    return [d for d in lasts if (d.year + 1) in FOLD_YEARS or d.year + 1 == max(FOLD_YEARS) + 1]


def is_argmax(runs, labels, start, end):
    """IS Sharpe argmax over [start, end]; ties -> first in ladder order (declared, not tuned)."""
    best, bl = -np.inf, labels[0]
    for lab in labels:
        r = runs[lab]["returns"].loc[start:end]
        s = metrics(r)["Sharpe"]
        if s > best + 1e-12:
            best, bl = s, lab
    return bl, best


def stitch(runs, plan, idx, charge_switch=True):
    """plan = list of (start_date, end_date, label). Realised daily return of the account,
    with the switch trade charged at COST_BPS on the first day of the new segment."""
    r = pd.Series(0.0, index=idx)
    prev = None
    for (a, b, lab) in plan:
        seg = runs[lab]["returns"].loc[a:b]
        r.loc[seg.index] = seg.values
        if prev is not None and prev != lab and charge_switch and len(seg):
            d = seg.index[0]
            w_old = runs[prev]["weights"].loc[d]
            w_new = runs[lab]["weights"].loc[d]
            r.loc[d] -= np.abs(w_new - w_old).sum() * COST_BPS / 1e4
        prev = lab
    return r


def build_plans(runs, labels, idx, warm):
    """Three selectors over the same fold grid. Returns dict label -> (plan, picks)."""
    fds = [d for d in fold_dates(idx) if d.year >= min(FOLD_YEARS) - 1]
    segs = []
    for i, d in enumerate(fds):
        a = idx[idx.get_loc(d) + 1]
        b = fds[i + 1] if i + 1 < len(fds) else idx[-1]
        segs.append((a, b, d))
    plans, picks = {}, {}
    # ALWAYS_ACT: re-pick at every fold on a strictly trailing expanding window
    pa, rec = [], []
    for (a, b, d) in segs:
        lab, s = is_argmax(runs, labels, warm, d)
        pa.append((a, b, lab)); rec.append(dict(selector="ALWAYS_ACT", decided=d.date(), pick=lab, is_sharpe=s))
    plans["ALWAYS_ACT"] = pa
    # ANCHOR: the first fold's argmax, held forever
    lab0, s0 = is_argmax(runs, labels, warm, segs[0][2])
    plans["ANCHOR"] = [(segs[0][0], segs[-1][1], lab0)]
    rec.append(dict(selector="ANCHOR", decided=segs[0][2].date(), pick=lab0, is_sharpe=s0))
    # ANCHOR_R8: pinned on warm-up..2016-12-31, then 2017-2026 read once
    d8 = max([d for (_, _, d) in segs if d < OOS_START])
    lab8, s8 = is_argmax(runs, labels, warm, d8)
    plans["ANCHOR_R8"] = [(segs[0][0], segs[-1][1], lab8)]
    rec.append(dict(selector="ANCHOR_R8", decided=d8.date(), pick=lab8, is_sharpe=s8))
    # INCUMBENT: the frozen book, if it is on this ladder; else the ladder's incumbent-equivalent
    inc = "N20" if "N20" in labels else ("G0.75" if "G0.75" in labels else
          ("CW" if "CW" in labels else ("K1" if "K1" in labels else labels[0])))
    plans["INCUMBENT"] = [(segs[0][0], segs[-1][1], inc)]
    rec.append(dict(selector="INCUMBENT", decided=None, pick=inc, is_sharpe=np.nan))
    picks = rec
    return plans, picks, segs


# ---------------------------------------------------------------- verdicts
def verdicts(r, base_r, spy_r):
    h = len(r) // 2
    S = lambda x: metrics(x)["Sharpe"]
    m, mb, ms = metrics(r), metrics(base_r), metrics(spy_r)
    oos = r.loc[OOS_START:]; oos_s = spy_r.loc[OOS_START:]
    p4a = (S(r.iloc[:h]) > S(base_r.iloc[:h])) and (S(r.iloc[h:]) > S(base_r.iloc[h:])) and (m["MaxDD"] >= mb["MaxDD"])
    legs = dict(H1=S(r.iloc[:h]) > S(spy_r.iloc[:h]), H2=S(r.iloc[h:]) > S(spy_r.iloc[h:]),
                DD=m["MaxDD"] >= 0.60 * ms["MaxDD"], CAGR=m["CAGR"] >= 0.70 * ms["CAGR"],
                OOS=metrics(oos)["Sharpe"] > metrics(oos_s)["Sharpe"])
    return p4a, all(legs.values()), legs


def main():
    panels = [("U56", load_universe()), ("B136", load_universe(broad=True)), ("SMALL", load_small())]
    rows, pickrows = [], []
    for tag, px in panels:
        if px is None:
            continue
        idx = px.index; warm = idx[260]
        spy = px["SPY"].pct_change().fillna(0.0)
        runs = run_books(px)
        base = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq="W")
        print(f"\n{'='*104}\nPANEL {tag}: {px.shape[1]} cols, {idx[0].date()} -> {idx[-1].date()}\n{'='*104}")
        for lname, rungs in LADDERS.items():
            labels = [l for l, _ in rungs]
            plans, picks, segs = build_plans(runs, labels, idx, warm)
            span_a, span_b = segs[0][0], segs[-1][1]
            base_r, spy_r = base["returns"].loc[span_a:span_b], spy.loc[span_a:span_b]
            for p in picks:
                pickrows.append(dict(panel=tag, ladder=lname, **p))
            for sel, plan in plans.items():
                for charged in (True, False):
                    r = stitch(runs, plan, idx, charge_switch=charged).loc[span_a:span_b]
                    m = metrics(r); h = len(r) // 2
                    oos = r.loc[OOS_START:]; mo = metrics(oos)
                    p4a, p4b, legs = verdicts(r, base_r, spy_r)
                    nsw = sum(1 for i in range(1, len(plan)) if plan[i][2] != plan[i - 1][2])
                    rows.append(dict(panel=tag, ladder=lname, selector=sel, costed=charged,
                                     switches=nsw, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                     H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                                     oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                                     KEEP4a=p4a, KEEP4b=p4b, legs=json.dumps({k: bool(v) for k, v in legs.items()})))
            d = pd.DataFrame([x for x in rows if x["panel"] == tag and x["ladder"] == lname and x["costed"]])
            mb, ms = metrics(base_r), metrics(spy_r)
            mob, mos = metrics(base_r.loc[OOS_START:]), metrics(spy_r.loc[OOS_START:])
            print(f"\n--- {tag} / ladder {lname} ({len(labels)} rungs) | base CAGR {mb['CAGR']:.2%} SH {mb['Sharpe']:.3f} "
                  f"DD {mb['MaxDD']:.2%} (OOS {mob['CAGR']:.2%}/{mob['Sharpe']:.3f}/{mob['MaxDD']:.2%}) | "
                  f"SPY {ms['CAGR']:.2%}/{ms['Sharpe']:.3f}/{ms['MaxDD']:.2%} (OOS {mos['CAGR']:.2%}/{mos['Sharpe']:.3f}/{mos['MaxDD']:.2%})")
            print(d[["selector", "switches", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                     "oos_CAGR", "oos_Sharpe", "oos_MaxDD", "KEEP4a", "KEEP4b"]]
                  .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
            free = pd.DataFrame([x for x in rows if x["panel"] == tag and x["ladder"] == lname and not x["costed"]])
            aa_c = d[d.selector == "ALWAYS_ACT"].iloc[0]; aa_f = free[free.selector == "ALWAYS_ACT"].iloc[0]
            print(f"    ALWAYS_ACT switch charge: Sharpe {aa_f['Sharpe']:.4f} free -> {aa_c['Sharpe']:.4f} costed "
                  f"({aa_c['Sharpe']-aa_f['Sharpe']:+.4f}); OOS {aa_f['oos_Sharpe']:.4f} -> {aa_c['oos_Sharpe']:.4f} "
                  f"({aa_c['oos_Sharpe']-aa_f['oos_Sharpe']:+.4f}) over {int(aa_c['switches'])} switches")
    R = pd.DataFrame(rows); P = pd.DataFrame(pickrows)
    R.to_csv(f"{OUT}.cells.csv", index=False); P.to_csv(f"{OUT}.picks.csv", index=False)

    print(f"\n{'='*104}\nSUMMARY — ALWAYS_ACT minus ANCHOR minus INCUMBENT, costed, per cell\n{'='*104}")
    piv = R[R.costed].pivot_table(index=["panel", "ladder"], columns="selector",
                                  values=["Sharpe", "oos_Sharpe", "KEEP4b"], aggfunc="first")
    print(piv.to_string(float_format=lambda x: f"{x:.4f}"))
    d = R[R.costed]
    for col in ("Sharpe", "oos_Sharpe"):
        a = d[d.selector == "ALWAYS_ACT"].set_index(["panel", "ladder"])[col]
        n = d[d.selector == "ANCHOR"].set_index(["panel", "ladder"])[col]
        i = d[d.selector == "INCUMBENT"].set_index(["panel", "ladder"])[col]
        print(f"\n{col}: mean ALWAYS_ACT {a.mean():.4f} | ANCHOR {n.mean():.4f} | INCUMBENT {i.mean():.4f} "
              f"| AA-ANCHOR {(a-n).mean():+.4f} (wins {int((a>n).sum())}/{len(a)}) "
              f"| AA-INCUMBENT {(a-i).mean():+.4f} (wins {int((a>i).sum())}/{len(a)})")
    print("\n4b passes, costed:", d.groupby("selector")["KEEP4b"].sum().to_dict(),
          "of", len(d[d.selector == "ANCHOR"]), "cells each")
    print("4a passes, costed:", d.groupby("selector")["KEEP4a"].sum().to_dict())
    print("\nwrote:", OUT.name + ".{cells,picks}.csv")


def load_small():
    """483-name sub-$2B panel, with the >=100% single-day movers dropped (data/small_meta.csv)."""
    try:
        px = load_universe(small=True)
        meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
        bad = set(meta.loc[meta["max_1d_move"] >= 1.0, meta.columns[0]].astype(str))
        keep = [c for c in px.columns if c not in bad or c == "SPY"]
        print(f"SMALL panel: dropped {px.shape[1]-len(keep)} tickers with max_1d_move >= 1.0")
        return px[keep]
    except Exception as e:
        print("SMALL panel unavailable:", type(e).__name__, e)
        return None


if __name__ == "__main__":
    main()
