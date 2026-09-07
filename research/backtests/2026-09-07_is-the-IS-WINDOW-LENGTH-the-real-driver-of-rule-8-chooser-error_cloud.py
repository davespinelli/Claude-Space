#!/usr/bin/env python3
"""Idea 354: is the IS WINDOW LENGTH the real driver of rule-8 chooser error?

Idea 39 found the rule-8 chooser flipped its pick on 2/2 panels from a START truncation alone
(IS 2007 -> 318 trading rows, regret -0.094 / -0.171) while a 577-row arm over the same span
flipped on only 1/2.  That confounds *what the tape is* with *how long the IS window is*.  This
script sweeps the IS window length directly, on the corrected (trading-day) tape, holding the
OOS window fixed, and asks whether PROTOCOL rule 8 needs a stated MINIMUM IS LENGTH rather than
its current fixed 2016 cut.

Two tuned parameters only:
    1. IS start        in {2008, 2010, 2012, 2014, 2016}-01-01   (IS end pinned at 2016-12-31)
    2. menu width m    in {3, 5, 9} arms drawn from ONE pre-registered n-ladder

Everything else is pre-registered and held fixed:
    book form  = top-n eligible names by the v1 composite with the /sqrt(vol20) scaler OFF,
                 equal weight at a constant 75% gross, RULES v1 eligibility (above 200d MA,
                 vol20 < 0.60), weekly, next-day execution, 10 bps  -- the record's KEEP 4b form.
    ladder     = n in {3, 5, 10, 15, 20, 30, 40, 60, ALL}
    m=3 menu   = {5, 20, ALL};  m=5 menu = {5, 10, 20, 40, ALL};  m=9 menu = the whole ladder
    OOS        = 2017-01-01 -> end, read once per cell, never used to choose.

Panels (structural, not tuned; all three reported in full):
    U56      research/universe.json            (ETF/mega-cap panel)
    B136     research/universe_broad.json      (136 large caps)
    SMALL439 data/prices_small.csv sub-$2B panel, after dropping the 44 tickers with
             max_1d_move >= 1.0 in data/small_meta.csv (483 -> 439).

Grid = 3 panels x 5 IS starts x 3 menu widths = 45 cells, ALL reported.  Each cell reports the
chooser's pick, its OOS Sharpe, the in-menu OOS oracle, the regret, and the paired deltas against
two anchors that need no choosing at all: ANCHOR20 (the record's incumbent n=20 book) and EWALL
(the do-nothing, no-selection control, n=ALL).

Rule 8 is the object of study here, so it is run in full: the pick is made on the IS window only
and the OOS window is read once.  Both KEEP paths are evaluated for every chosen book on the full
sample (4a vs the live RULES v2 baseline, 4b vs SPY).

SURVIVORSHIP: all three panels are current-constituent lists (the small panel especially -- see
data/SMALL_PANEL_README.md), which flatters every CAGR below.  The chooser REGRET numbers, which
are differences between arms on the same tape, are far less exposed to it.

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v1_weights, rules_v2_weights   # noqa
from engine import backtest, metrics                                            # noqa

SLUG = "2026-09-07_is-the-IS-WINDOW-LENGTH-the-real-driver-of-rule-8-chooser-error_cloud"
OUT = ROOT / "research" / "backtests"
GROSS, MAX_VOL, FREQ, COST = 0.75, 0.60, "W", 10
LADDER = [3, 5, 10, 15, 20, 30, 40, 60, "ALL"]
MENUS = {3: [5, 20, "ALL"], 5: [5, 10, 20, 40, "ALL"], 9: LADDER}
IS_STARTS = ["2008-01-01", "2010-01-01", "2012-01-01", "2014-01-01", "2016-01-01"]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
ANCHOR, DONOTHING = 20, "ALL"


# ---------------------------------------------------------------- the pre-registered book form
def topn_weights(px, n):
    """top-n eligible by the v1 composite (scaler OFF), equal weight at a constant 75% gross.
    n == 'ALL' equal-weights every eligible name (the record's EWALL do-nothing control)."""
    s = score(px, vol_scale=False)[0]
    _, above, vol20 = score(px)
    elig = (above & (vol20 < MAX_VOL) & s.notna())
    if n == "ALL":
        sel = elig.astype(float)
        k = sel.sum(axis=1).replace(0, np.nan)
        return (sel.div(k, axis=0) * GROSS).fillna(0.0)
    rank = s.where(elig).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (GROSS / n)


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    print(f"    SMALL: dropped {px.shape[1]-len(keep)} tickers with max_1d_move >= 1.0")
    return px[keep]


def hs(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars4b(r, spy):
    """PROTOCOL 4b: Sharpe > SPY in both halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70%."""
    m, ms = metrics(r), metrics(spy)
    h1, h2 = hs(r); s1, s2 = hs(spy)
    o = metrics(r.loc[OOS_START:])["Sharpe"] - metrics(spy.loc[OOS_START:])["Sharpe"]
    d = {"H1": h1 - s1, "H2": h2 - s2, "OOS": o,
         "DD": 0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"]),
         "CAGR": m["CAGR"] - 0.70 * ms["CAGR"]}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


def bars4a(r, base):
    """PROTOCOL 4a: Sharpe > the live book in BOTH halves and MaxDD no worse."""
    h1, h2 = hs(r); b1, b2 = hs(base)
    ok = h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"]
    return ok, {"H1": h1 - b1, "H2": h2 - b2,
                "DD": metrics(r)["MaxDD"] - metrics(base)["MaxDD"]}


def main():
    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": load_small()}
    recs, arms_rows = [], []

    for pname, px in panels.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        base = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
        ms = metrics(spy); s1, s2 = hs(spy); so = metrics(spy.loc[OOS_START:])
        print(f"\n{'='*100}\n=== {pname}: {px.shape[1]-1} names + SPY, "
              f"{px.index[0].date()} -> {px.index[-1].date()}  (scored from {start.date()})")
        print(f"    SPY   CAGR {ms['CAGR']:7.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:8.2%} "
              f"H1/H2 {s1:.3f}/{s2:.3f} | OOS Sharpe {so['Sharpe']:.3f} CAGR {so['CAGR']:.2%}")
        mb = metrics(base); b1, b2 = hs(base)
        print(f"    RULESv2 CAGR {mb['CAGR']:6.2%} Sharpe {mb['Sharpe']:.3f} MaxDD {mb['MaxDD']:8.2%} "
              f"H1/H2 {b1:.3f}/{b2:.3f} | OOS Sharpe {metrics(base.loc[OOS_START:])['Sharpe']:.3f}")
        print(f"    4b bars: MaxDD cap {-0.60*abs(ms['MaxDD']):.2%}, CAGR floor {0.70*ms['CAGR']:.2%}")

        # ---- every arm on the ladder, once
        arms = {}
        for n in LADDER:
            r = backtest(px, topn_weights(px, n), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
            arms[n] = r
        print(f"\n    --- the {len(LADDER)}-arm ladder, full sample @ {COST} bps (ALL points reported)")
        print(f"    {'n':>4} | {'CAGR':>7} {'Sharpe':>7} {'MaxDD':>8} | {'H1':>6} {'H2':>6} | "
              f"{'OOSShrp':>7} {'OOSCAGR':>8} | 4a 4b")
        for n in LADDER:
            r = arms[n]; m = metrics(r); h1, h2 = hs(r); o = metrics(r.loc[OOS_START:])
            p4b, d4b, f4b = bars4b(r, spy); p4a, d4a = bars4a(r, base)
            print(f"    {str(n):>4} | {m['CAGR']:7.2%} {m['Sharpe']:7.3f} {m['MaxDD']:8.2%} | "
                  f"{h1:6.3f} {h2:6.3f} | {o['Sharpe']:7.3f} {o['CAGR']:8.2%} | "
                  f"{'Y' if p4a else 'n'}  {'Y' if p4b else 'n'}"
                  + ("" if p4b else f"  fail:{','.join(f4b)}"))
            arms_rows.append(dict(panel=pname, n=str(n), CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                                  MaxDD=m["MaxDD"], H1=h1, H2=h2, OOS_Sharpe=o["Sharpe"],
                                  OOS_CAGR=o["CAGR"], pass4a=p4a, pass4b=p4b,
                                  fail4b=",".join(f4b)))

        oos_s = {n: metrics(arms[n].loc[OOS_START:])["Sharpe"] for n in LADDER}
        anchor_oos, donothing_oos = oos_s[ANCHOR], oos_s[DONOTHING]

        # ---- the chooser sweep
        print(f"\n    --- rule-8 chooser: pick argmax IS Sharpe on [IS start .. {IS_END}], "
              f"read OOS {OOS_START}.. once")
        print(f"    ANCHOR20 OOS Sharpe {anchor_oos:.4f} | EWALL(do-nothing) OOS Sharpe {donothing_oos:.4f}")
        print(f"    {'IS start':>10} {'rows':>5} {'yrs':>5} {'m':>2} | {'pick':>4} {'ISshrp':>7} | "
              f"{'OOSshrp':>7} {'oracle':>6} {'regret':>7} | {'vsANCH':>7} {'vsEWALL':>7} | 4a 4b")
        for iss in IS_STARTS:
            n_rows = len(arms[ANCHOR].loc[iss:IS_END])
            for m_width, menu in MENUS.items():
                is_sh = {n: metrics(arms[n].loc[iss:IS_END])["Sharpe"] for n in menu}
                pick = max(menu, key=lambda n: is_sh[n])
                oracle = max(menu, key=lambda n: oos_s[n])
                r = arms[pick]
                p4b, d4b, f4b = bars4b(r, spy); p4a, _ = bars4a(r, base)
                print(f"    {iss[:7]:>10} {n_rows:5d} {n_rows/252:5.1f} {m_width:2d} | "
                      f"{str(pick):>4} {is_sh[pick]:7.3f} | {oos_s[pick]:7.4f} {str(oracle):>6} "
                      f"{oos_s[pick]-oos_s[oracle]:+7.4f} | {oos_s[pick]-anchor_oos:+7.4f} "
                      f"{oos_s[pick]-donothing_oos:+7.4f} | {'Y' if p4a else 'n'}  {'Y' if p4b else 'n'}")
                recs.append(dict(panel=pname, is_start=iss, is_rows=n_rows, is_years=n_rows / 252,
                                 menu_width=m_width, pick=str(pick), is_sharpe=is_sh[pick],
                                 oos_sharpe=oos_s[pick], oracle=str(oracle),
                                 oracle_oos=oos_s[oracle], regret=oos_s[pick] - oos_s[oracle],
                                 vs_anchor=oos_s[pick] - anchor_oos,
                                 vs_donothing=oos_s[pick] - donothing_oos,
                                 pass4a=p4a, pass4b=p4b, fail4b=",".join(f4b)))

    df = pd.DataFrame(recs)
    ad = pd.DataFrame(arms_rows)
    df.to_csv(OUT / f"{SLUG}_grid.csv", index=False)
    ad.to_csv(OUT / f"{SLUG}_arms.csv", index=False)

    # ---------------------------------------------------------------- readings
    print(f"\n{'='*100}\n=== READING 1: is regret monotone in IS length? (mean over menu widths)")
    piv = df.pivot_table(index="is_start", columns="panel", values="regret", aggfunc="mean")
    print(piv.to_string(float_format=lambda x: f"{x:+.4f}"))
    print("\n    pooled mean regret by IS start:")
    g = df.groupby("is_start").agg(rows=("is_rows", "mean"), regret=("regret", "mean"),
                                   worst=("regret", "min"), zero=("regret", lambda s: (s >= -1e-9).mean()))
    print(g.to_string(float_format=lambda x: f"{x:.4f}"))
    r_all = df[["is_years", "regret"]].corr().iloc[0, 1]
    print(f"    Spearman(IS years, regret) = {df[['is_years','regret']].corr(method='spearman').iloc[0,1]:+.4f} "
          f"| Pearson {r_all:+.4f}   (positive = longer IS, less negative regret = better)")
    starts = list(g.index)
    mono = all(g.loc[starts[i], "regret"] >= g.loc[starts[i + 1], "regret"] - 1e-12
               for i in range(len(starts) - 1))
    print(f"    monotone (longer IS never worse, pooled): {mono}")

    print(f"\n=== READING 2: does the chooser beat NOT choosing? (paired, per cell)")
    for col, lab in (("vs_anchor", "ANCHOR20"), ("vs_donothing", "EWALL do-nothing")):
        w = (df[col] > 0).sum()
        print(f"    vs {lab:18s}: chooser wins {w:2d}/{len(df)} cells, mean {df[col].mean():+.4f}, "
              f"median {df[col].median():+.4f}, worst {df[col].min():+.4f}")
        sub = df.groupby("is_start")[col].mean()
        print("        by IS start: " + "  ".join(f"{k[:4]} {v:+.4f}" for k, v in sub.items()))

    print(f"\n=== READING 3: pick STABILITY -- how often does the pick change with the IS start?")
    for (p, m_w), sub in df.groupby(["panel", "menu_width"]):
        picks = list(sub.sort_values("is_start").pick)
        flips = sum(picks[i] != picks[i + 1] for i in range(len(picks) - 1))
        print(f"    {p:9s} m={m_w}: {' -> '.join(picks):28s}  flips {flips}/{len(picks)-1}, "
              f"distinct {len(set(picks))}")

    print(f"\n=== READING 4: menu width -- does a wider menu cost the chooser?")
    print(df.groupby("menu_width").agg(regret=("regret", "mean"), vs_anchor=("vs_anchor", "mean"),
                                       vs_dn=("vs_donothing", "mean"),
                                       zero_regret=("regret", lambda s: (s >= -1e-9).mean())
                                       ).to_string(float_format=lambda x: f"{x:+.4f}"))

    print(f"\n=== READING 5: KEEP paths over the 45 chosen books")
    print(f"    4a passes: {int(df.pass4a.sum())}/{len(df)}   4b passes: {int(df.pass4b.sum())}/{len(df)}")
    if df.pass4b.any():
        print(df[df.pass4b][["panel", "is_start", "menu_width", "pick", "oos_sharpe"]].to_string(index=False))
    print(f"    4b failing bars over all {len(ad)} ladder arms: "
          + ", ".join(f"{k}:{v}" for k, v in
                      pd.Series([b for s in ad.fail4b for b in (s.split(",") if s else [])]
                                ).value_counts().items()))

    print(f"\n=== READING 6: what MINIMUM IS length, if any, does the evidence support?")
    for thr in (1.0, 2.0, 3.0, 5.0, 7.0):
        sub = df[df.is_years >= thr]
        if len(sub) == 0: continue
        print(f"    IS >= {thr:4.1f} yr ({len(sub):2d} cells): mean regret {sub.regret.mean():+.4f}, "
              f"worst {sub.regret.min():+.4f}, zero-regret {100*(sub.regret>=-1e-9).mean():5.1f}%, "
              f"beats EWALL {100*(sub.vs_donothing>0).mean():5.1f}%")
    print(f"\n    wrote {SLUG}_grid.csv ({len(df)} cells) and {SLUG}_arms.csv ({len(ad)} arms)")


if __name__ == "__main__":
    main()
