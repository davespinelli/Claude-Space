#!/usr/bin/env python3
"""Idea 1177 — does the CASH SLEEVE break the record's GROSS SCALING IDENTITY
anywhere it is LOAD-BEARING?

Background.  Idea 1171's G5b found the committed weight identity W(g) == g*W(1)
does NOT carry to the compounded RETURN path when gross < 1
(max |r(0.75) - 2.5*r(0.30)| = 3.331e-03).  Reason, read off engine.backtest:
between rebalances the held weights drift and are renormalised by
    tot = growth.sum() + (1 - cur.sum())
i.e. the UNINVESTED CASH SLEEVE is carried at 0% and re-shares the book each day.
At gross g with per-period book return r_p the next day's held weight is
    held_g = g * w * (1+r_i) / (1 + g*r_p)
against held_1 = w*(1+r_i)/(1+r_p).  held_g / held_1 = g*(1+r_p)/(1+g*r_p) != g.
So the sleeve makes the gross dial NON-linear in the realised return path, second
order in r_p, vanishing only at g=1 and g=0.

The record leans on the identity in three committed families:
  SHARPE-FLAT : "gross is not an information dial / Sharpe flat to 0.0001 across
                 the ladder" -> Sharpe is scale-invariant under EXACT scaling.
  CAGR-BUYS   : "gross buys CAGR" -> CAGR(g) read as a monotone exposure effect.
  MAXDD-BUYS  : "gross buys drawdown" -> MaxDD(g) read as a monotone exposure effect.

This run prices the sleeve: for every (panel, book, gross rung) it runs the engine
at gross g (ACTUAL) and compares it to the identity's prediction g*r_1 (ASSUMED),
and asks how far each committed family moves once the sleeve is paid for.

Two tuned parameters ONLY, both reported at every grid point:
  P1 CLAIM SET  in {SHARPE-FLAT, CAGR-BUYS, MAXDD-BUYS}
  P2 GROSS RUNG in {0.20, 0.30, 0.40, 0.50, 0.65, 0.75, 0.85, 1.00}

Rule 8 walk-forward: the gross rung is chosen on the FIRST half by IS Sharpe,
twice - once off the ASSUMED (scaled) paths, once off the ACTUAL paths - and the
second half is read once.  If the sleeve is immaterial the two choosers agree.

Panels: MEGA/ETF (56), BROAD (136 large caps), SMALL (sub-$2B, max_1d_move<1.0
dropped).  SMALL is current-constituents only -> SURVIVORSHIP BIAS, stated in the
memo and the leaderboard row.

Costs 10 bps, weekly cadence, next-day execution (engine).  Deterministic.
"""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score, band_state, compare  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics  # noqa

COST_BPS, FREQ = 10.0, "W"
GROSS = [0.20, 0.30, 0.40, 0.50, 0.65, 0.75, 0.85, 1.00]   # P2
CLAIMS = ["SHARPE-FLAT", "CAGR-BUYS", "MAXDD-BUYS"]         # P1
pd.set_option("display.width", 200)


# ---------------------------------------------------------------- panels
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep]


def panels():
    return {"MEGA": load_universe(), "BROAD": load_universe(broad=True), "SMALL": small_panel()}


# ---------------------------------------------------------------- books (gross-dialled)
def book_v2band(px, g):
    """RULES v2, live book: 200d +/-3% band, equal weight, gated weight -> CASH."""
    return rules_v2_weights(px, band=0.03, gross=g)


def book_top20(px, g):
    """The 2026-09-04 KEEP 4b candidate: top-20 composite, equal weight, NO vol scaler."""
    s, above, vol20 = score(px, vol_scale=False)
    cols = [c for c in px.columns if c != "SPY"]
    s = s[cols].where(above[cols])
    rank = s.rank(axis=1, ascending=False)
    w = (rank <= 20).astype(float) * (g / 20.0)
    return w.reindex(columns=px.columns).fillna(0.0)


def book_v1(px, g):
    """RULES v1 (previous live): top-5 vol-scaled composite, per-name weight g/5."""
    return rules_v1_weights(px, n=5, w=g / 5.0)


BOOKS = {"V2BAND": book_v2band, "TOP20EW": book_top20, "V1TOP5": book_v1}


# ---------------------------------------------------------------- helpers
def run(px, fn, g, start):
    r = backtest(px, fn(px, g), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    return r


def m3(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def half(r, which):
    h = len(r) // 2
    return r.iloc[:h] if which == 1 else r.iloc[h:]


def keep_paths(r, base, spy):
    """4a vs the live book, 4b vs SPY. Returns (pass4a, pass4b) booleans."""
    s1, s2 = metrics(half(r, 1))["Sharpe"], metrics(half(r, 2))["Sharpe"]
    b1, b2 = metrics(half(base, 1))["Sharpe"], metrics(half(base, 2))["Sharpe"]
    a = s1 > b1 and s2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"]
    p1, p2 = metrics(half(spy, 1))["Sharpe"], metrics(half(spy, 2))["Sharpe"]
    mS, mR = metrics(spy), metrics(r)
    b = (s1 > p1 and s2 > p2 and mR["MaxDD"] >= 0.60 * mS["MaxDD"]
         and mR["CAGR"] >= 0.70 * mS["CAGR"])
    return a, b


# ---------------------------------------------------------------- census of committed claims
def census():
    """Harvest the record's committed GROSS-dial claims and classify which metric
    family each one hinges on.  Text harvest, reported as counts of CLAIM LINES."""
    txt = {}
    for f in ("LEADERBOARD.md", "CHANGELOG.md"):
        txt[f] = (ROOT / "research" / f).read_text().split("\n")
    pat_g = ("gross", "GROSS", "de-gross", "re-gross")
    fam = {"SHARPE-FLAT": ("sharpe", "information dial", "flat to"),
           "CAGR-BUYS": ("cagr", "return leg"),
           "MAXDD-BUYS": ("maxdd", "drawdown", "dd leg")}
    out, lines = {c: 0 for c in CLAIMS}, 0
    for f, L in txt.items():
        for ln in L:
            if not any(p in ln for p in pat_g):
                continue
            low = ln.lower()
            hit = [c for c, keys in fam.items() if any(k in low for k in keys)]
            if hit:
                lines += 1
                for c in hit:
                    out[c] += 1
    return out, lines


# ---------------------------------------------------------------- main
def main():
    P = panels()
    cen, cen_lines = census()
    print("=" * 108)
    print("CENSUS of committed GROSS-dial claim lines (LEADERBOARD.md + CHANGELOG.md)")
    print(f"  lines mentioning a gross dial AND a metric family: {cen_lines}")
    for c in CLAIMS:
        print(f"  {c:<12} {cen[c]:>5} lines")
    print("=" * 108)

    rows, wf_rows = [], []
    for pname, px in P.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        live = run(px, book_v2band, 0.75, start)          # the live book, gross 0.75
        for bname, fn in BOOKS.items():
            r1 = run(px, fn, 1.00, start)                 # the identity's reference path
            for g in GROSS:
                ra = run(px, fn, g, start)                # ACTUAL
                rs = g * r1                               # ASSUMED  (identity W(g)=g*W(1))
                ca, sa, da = m3(ra)
                cs, ss, ds = m3(rs)
                a_a, b_a = keep_paths(ra, live, spy)
                a_s, b_s = keep_paths(rs, live, spy)
                rows.append(dict(panel=pname, book=bname, gross=g,
                                 maxabs=float((ra - rs).abs().max()),
                                 CAGR_act=ca, CAGR_asm=cs, dCAGR=ca - cs,
                                 Sh_act=sa, Sh_asm=ss, dSharpe=sa - ss,
                                 DD_act=da, DD_asm=ds, dDD=da - ds,
                                 f4a_act=a_a, f4a_asm=a_s, f4b_act=b_a, f4b_asm=b_s,
                                 flip4a=a_a != a_s, flip4b=b_a != b_s))
            # ---- rule 8 walk-forward: choose the gross rung on half 1, read half 2 once
            h = len(r1) // 2
            act = {g: run(px, fn, g, start) for g in GROSS}
            asm = {g: g * r1 for g in GROSS}
            pick_a = max(GROSS, key=lambda g: metrics(act[g].iloc[:h])["Sharpe"])
            pick_s = max(GROSS, key=lambda g: metrics(asm[g].iloc[:h])["Sharpe"])
            for tag, pick, src in (("ACTUAL", pick_a, act), ("ASSUMED", pick_s, asm)):
                oos = src[pick].iloc[h:]
                c, s, d = m3(oos)
                a, b = keep_paths(src[pick], live, spy)
                wf_rows.append(dict(panel=pname, book=bname, chooser=tag, pick=pick,
                                    OOS_CAGR=c, OOS_Sharpe=s, OOS_MaxDD=d,
                                    OOS_base_Sharpe=metrics(live.iloc[h:])["Sharpe"],
                                    OOS_base_CAGR=metrics(live.iloc[h:])["CAGR"],
                                    OOS_base_DD=metrics(live.iloc[h:])["MaxDD"],
                                    OOS_SPY_Sharpe=metrics(spy.iloc[h:])["Sharpe"],
                                    OOS_SPY_CAGR=metrics(spy.iloc[h:])["CAGR"],
                                    OOS_SPY_DD=metrics(spy.iloc[h:])["MaxDD"],
                                    p4a=a, p4b=b))
            print(f"  ran {pname}/{bname}")

    D = pd.DataFrame(rows)
    W = pd.DataFrame(wf_rows)
    out = ROOT / "research" / "backtests" / "reports"
    out.mkdir(parents=True, exist_ok=True)
    D.to_csv(out / "1177_gross_sleeve_grid.csv", index=False)
    W.to_csv(out / "1177_gross_sleeve_wf.csv", index=False)

    print("\n" + "=" * 108)
    print("G1  FULL GRID — ACTUAL (sleeve priced) vs ASSUMED (identity r_g = g*r_1)")
    print("=" * 108)
    show = D[["panel", "book", "gross", "maxabs", "Sh_act", "Sh_asm", "dSharpe",
              "CAGR_act", "CAGR_asm", "dCAGR", "DD_act", "DD_asm", "dDD"]]
    print(show.to_string(index=False, float_format=lambda x: f"{x:.5f}"))

    print("\n" + "=" * 108)
    print("G2  PER-CLAIM-FAMILY worst move across the ladder (P1 x P2 fully reported)")
    print("=" * 108)
    for pname in P:
        for bname in BOOKS:
            d = D[(D.panel == pname) & (D.book == bname)]
            print(f"\n{pname}/{bname}:")
            print(f"  SHARPE-FLAT : identity says Sharpe(g) == Sharpe(1) exactly.  "
                  f"ACTUAL spread across ladder = {d.Sh_act.max()-d.Sh_act.min():.5f}, "
                  f"ASSUMED spread = {d.Sh_asm.max()-d.Sh_asm.min():.5f}, "
                  f"max |act-asm| = {d.dSharpe.abs().max():.5f}")
            print(f"  CAGR-BUYS   : max |act-asm| = {d.dCAGR.abs().max():.5%}  "
                  f"(at gross {d.loc[d.dCAGR.abs().idxmax(),'gross']:.2f}); "
                  f"ACTUAL monotone in g? {bool((d.sort_values('gross').CAGR_act.diff().dropna()>0).all())}  "
                  f"ASSUMED monotone? {bool((d.sort_values('gross').CAGR_asm.diff().dropna()>0).all())}")
            print(f"  MAXDD-BUYS  : max |act-asm| = {d.dDD.abs().max():.5%}  "
                  f"(at gross {d.loc[d.dDD.abs().idxmax(),'gross']:.2f}); "
                  f"ACTUAL monotone in g? {bool((d.sort_values('gross').DD_act.diff().dropna()<0).all())}  "
                  f"ASSUMED monotone? {bool((d.sort_values('gross').DD_asm.diff().dropna()<0).all())}")

    print("\n" + "=" * 108)
    print("G3  DOES THE SLEEVE MOVE A PUBLISHED VERDICT?  (4a / 4b flips, both KEEP paths)")
    print("=" * 108)
    print(f"  grid cells                : {len(D)}")
    print(f"  4a verdict flips act/asm  : {int(D.flip4a.sum())}")
    print(f"  4b verdict flips act/asm  : {int(D.flip4b.sum())}")
    if D.flip4a.any() or D.flip4b.any():
        print(D[D.flip4a | D.flip4b][["panel", "book", "gross", "f4a_act", "f4a_asm",
                                      "f4b_act", "f4b_asm"]].to_string(index=False))
    print(f"\n  cells where |dSharpe| > 1e-4 (the record's published precision): "
          f"{int((D.dSharpe.abs()>1e-4).sum())} of {len(D)}")
    print(f"  cells where |dSharpe| > 1e-3 : {int((D.dSharpe.abs()>1e-3).sum())} of {len(D)}")
    print(f"  cells where |dCAGR|  > 10 bps: {int((D.dCAGR.abs()>1e-3).sum())} of {len(D)}")
    print(f"  cells where |dDD|    > 10 bps: {int((D.dDD.abs()>1e-3).sum())} of {len(D)}")
    print(f"  max |r_g - g*r_1| over grid  : {D.maxabs.max():.3e}")

    print("\n" + "=" * 108)
    print("G4  RULE 8 WALK-FORWARD — gross chosen on half 1, half 2 read once")
    print("=" * 108)
    print(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    agree = W.pivot_table(index=["panel", "book"], columns="chooser", values="pick")
    n_ag = int((agree["ACTUAL"] == agree["ASSUMED"]).sum())
    print(f"\n  chooser agreement (ACTUAL pick == ASSUMED pick): {n_ag} of {len(agree)} panel x book cells")
    print(agree.to_string())

    print("\n" + "=" * 108)
    print("G5  LEADERBOARD compare() for the walk-forward pick on each panel (V2BAND book)")
    print("=" * 108)
    lines = []
    for pname, px in P.items():
        pick = W[(W.panel == pname) & (W.book == "V2BAND") & (W.chooser == "ACTUAL")].pick.iloc[0]
        res = compare(f"1177 sleeve-priced gross {pick:.2f} V2BAND [{pname}]",
                      lambda p, g=pick: book_v2band(p, g), px, freq=FREQ, cost_bps=COST_BPS)
        lines.append(res["row"])
    print("\nROWS:")
    for l in lines:
        print(l)


if __name__ == "__main__":
    main()
