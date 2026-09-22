#!/usr/bin/env python3
"""Idea 2085 (lane B, 2026-09-22): does LEVERAGE on the live band book clear the 4b
CAGR floor where DE-GROSS cannot?

CHANGELOG diagnosis this run is grounded in: the standing KEEP-4b candidate's SOLE
binding 4b leg is the CAGR floor (>=70% of SPY's CAGR), and every drawdown-buying
device the record has priced is beaten at matched exposure by a plain DE-GROSS -- i.e.
every device REMOVES exposure. LEVERAGE (gross > 1.0) is the one direction the record
has never priced, and it is the direction that lifts CAGR directly. The tension worth
pricing for real capital: leverage lifts CAGR (helps the sole binding leg) but also
scales MaxDD toward the 4b DD cap (<=60% of SPY's) -- which binds first?

Book: baseline.rules_v2_weights(px, band, gross) -- the LIVE band book, gross allowed
above 1.0 (leverage stated per PROTOCOL rule 2).
Two tuned params and no more: BAND c in {0.03, 0.08}, GROSS in {0.75,1.00,1.25,1.50,1.75,2.00}.
All 12 cells x 2 panels reported. Costs {0,10,25,50} bps reported for the rule-8 pick,
tuned nowhere (headline 10 bps). Rule-8 walk-forward: params chosen on 2009-2016 ONLY,
2017-2026 read once.

LEVERAGE IS NOT FREE. Headline uses fin=0%/yr (comparable to the record's convention that
un-invested NAV earns 0%). A financing sensitivity subtracts fin_rate/252 * borrowed_gross
each day at fin in {0,3,6}%/yr and reports the break-even. This is the honest caveat:
gross>1 assumes a borrow rate, and at ~3-6%/yr on the levered slice the CAGR gain is taxed.

Price-only on committed caches (U56=universe.json, B136=universe_broad.json). No EDGAR /
Form 4 / options / live data. Survivorship: current constituents on both panels.
"""
import sys, itertools
from pathlib import Path
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from baseline import load_universe, rules_v2_weights, rules_v1_weights
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics

BANDS = [0.03, 0.08]
GROSS = [0.75, 1.00, 1.25, 1.50, 1.75, 2.00]
FIN = [0.0, 0.03, 0.06]          # annual financing on borrowed gross (gross_held - 1)+
WARM = 260
IS_END = "2016-12-31"            # rule 8: choose on 2009-2016 only
OOS_START = "2017-01-01"


def _dd(eq):
    return (eq / eq.cummax() - 1).min()


def met(r):
    """Full-sample metrics on a daily return series."""
    m = metrics(r)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def run_book(px, band, gross, cost_bps=10, fin=0.0):
    """Backtest the band book at (band, gross); subtract financing on borrowed gross.
    Returns the net daily return series over the post-warmup window."""
    res = backtest(px, rules_v2_weights(px, band=band, gross=gross), cost_bps=cost_bps, freq="W")
    r = res["returns"]
    if fin > 0:
        borrowed = (res["weights"].sum(axis=1) - 1.0).clip(lower=0.0)
        r = r - borrowed * fin / 252.0
    return r.iloc[WARM:]


def spy_series(px):
    return px["SPY"].pct_change().fillna(0.0).iloc[WARM:]


def verdict_4a(row, base):
    return row["H1"] > base["H1"] and row["H2"] > base["H2"] and row["MaxDD"] >= base["MaxDD"]


def verdict_4b(r, spy):
    """4b on a return window r vs its aligned SPY window."""
    m, ms = met(r), met(spy)
    ok_sharpe = (m["H1"] > ms["H1"]) and (m["H2"] > ms["H2"])
    ok_dd = m["MaxDD"] >= 0.60 * ms["MaxDD"]        # both negative -> shallower
    ok_cagr = m["CAGR"] >= 0.70 * ms["CAGR"]
    return ok_sharpe and ok_dd and ok_cagr, dict(sharpe=ok_sharpe, dd=ok_dd, cagr=ok_cagr)


def panel_grid(name, px):
    print(f"\n{'='*78}\nPANEL {name}\n{'='*78}")
    spy = spy_series(px)
    base_r = run_book_baseline(px)                 # RULES v2 live (band 0.03, gross 0.75)
    base = met(base_r)
    ms = met(spy)
    print(f"comparands FULL:  RULES v2 {base['CAGR']:.2%}/{base['Sharpe']:.3f}/{base['MaxDD']:.2%}"
          f"   SPY {ms['CAGR']:.2%}/{ms['Sharpe']:.3f}/{ms['MaxDD']:.2%}")
    print(f"  4b bars: CAGR>= {0.70*ms['CAGR']:.2%}, MaxDD>= {0.60*ms['MaxDD']:.2%}, "
          f"Sharpe> SPY halves ({ms['H1']:.3f}/{ms['H2']:.3f})")
    rows = []
    for band, gross in itertools.product(BANDS, GROSS):
        r = run_book(px, band, gross, cost_bps=10, fin=0.0)
        m = met(r)
        p4a = verdict_4a(m, base)
        p4b, legs = verdict_4b(r, spy)
        rows.append(dict(panel=name, band=band, gross=gross, **m,
                         v4a=p4a, v4b=p4b, cagr_ok=legs["cagr"], dd_ok=legs["dd"], sh_ok=legs["sharpe"]))
    df = pd.DataFrame(rows)
    show = df.copy()
    for c in ["CAGR", "MaxDD"]:
        show[c] = show[c].map(lambda x: f"{x:.2%}")
    for c in ["Sharpe", "H1", "H2"]:
        show[c] = show[c].map(lambda x: f"{x:.3f}")
    print(show[["band", "gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                "v4a", "v4b", "cagr_ok", "dd_ok", "sh_ok"]].to_string(index=False))
    return df, base, ms


def run_book_baseline(px):
    return backtest(px, rules_v2_weights(px), cost_bps=10, freq="W")["returns"].iloc[WARM:]


def rule8(name, px):
    """Choose (band,gross) on 2009-2016 by the memo's pre-stated 4b screen, read 2017-2026 once."""
    print(f"\n--- RULE 8 walk-forward, PANEL {name} (choose on <= {IS_END}, read {OOS_START}+ once) ---")
    spy = spy_series(px)
    spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
    ms_is = met(spy_is)
    cells = []
    for band, gross in itertools.product(BANDS, GROSS):
        r = run_book(px, band, gross, cost_bps=10, fin=0.0)
        r_is = r.loc[:IS_END]
        m_is = met(r_is)
        # 4b-legal IS screen: Sharpe>SPY both IS halves, IS MaxDD<=60% SPY IS, IS CAGR>=70% SPY IS
        legal = (m_is["H1"] > ms_is["H1"] and m_is["H2"] > ms_is["H2"]
                 and m_is["MaxDD"] >= 0.60 * ms_is["MaxDD"] and m_is["CAGR"] >= 0.70 * ms_is["CAGR"])
        cells.append((band, gross, m_is["Sharpe"], legal, r))
    legal_cells = [c for c in cells if c[3]]
    pool = legal_cells if legal_cells else cells
    band, gross, is_sharpe, legal, r = max(pool, key=lambda c: c[2])
    tag = "4b-legal" if legal_cells else "NONE legal IS -> fell back to max IS Sharpe"
    print(f"IS pick: band={band} gross={gross} (IS Sharpe {is_sharpe:.3f}; chooser={tag})")
    # OOS read once
    r_oos = r.loc[OOS_START:]
    base_oos = run_book_baseline(px).loc[OOS_START:]
    mo, mb, mso = met(r_oos), met(base_oos), met(spy_oos)
    p4b, legs = verdict_4b(r_oos, spy_oos)
    print(f"OOS pick   {mo['CAGR']:.2%}/{mo['Sharpe']:.3f}/{mo['MaxDD']:.2%}  halves {mo['H1']:.3f}/{mo['H2']:.3f}")
    print(f"OOS RULESv2{mb['CAGR']:.2%}/{mb['Sharpe']:.3f}/{mb['MaxDD']:.2%}")
    print(f"OOS SPY    {mso['CAGR']:.2%}/{mso['Sharpe']:.3f}/{mso['MaxDD']:.2%}")
    print(f"OOS 4b: {p4b}  legs {legs}")
    # cost + financing sensitivity on the pick
    print("cost/financing sensitivity on the pick (full sample):")
    for cost in [0, 10, 25, 50]:
        rr = run_book(px, band, gross, cost_bps=cost, fin=0.0)
        print(f"  {cost:>2} bps, fin 0%: {met(rr)['CAGR']:.2%}/{met(rr)['Sharpe']:.3f}/{met(rr)['MaxDD']:.2%}")
    for fin in FIN:
        rr = run_book(px, band, gross, cost_bps=10, fin=fin)
        p, _ = verdict_4b(rr.loc[OOS_START:], spy_oos)
        print(f"  10 bps, fin {fin:.0%}: full {met(rr)['CAGR']:.2%}/{met(rr)['Sharpe']:.3f}/{met(rr)['MaxDD']:.2%}  OOS4b={p}")
    # financing on a LEVERED cell (gross 1.25, same band) where borrowed>0, so the caveat bites
    print(f"financing on a LEVERED cell (band={band}, gross=1.25, borrowed>0):")
    for fin in FIN:
        rr = run_book(px, band, 1.25, cost_bps=10, fin=fin)
        p, legs = verdict_4b(rr.loc[OOS_START:], spy_oos)
        print(f"  1.25x, 10 bps, fin {fin:.0%}: full {met(rr)['CAGR']:.2%}/{met(rr)['Sharpe']:.3f}/{met(rr)['MaxDD']:.2%}  OOS4b={p} {legs}")
    return dict(band=band, gross=gross, oos=mo, oos_base=mb, oos_spy=mso, oos_4b=p4b, legs=legs)


def main():
    out = {}
    for name, kw in [("U56", {}), ("B136", {"broad": True})]:
        px = load_universe(**kw)
        df, base, ms = panel_grid(name, px)
        pick = rule8(name, px)
        out[name] = (df, base, ms, pick)
    # concise summary
    print(f"\n{'='*78}\nSUMMARY\n{'='*78}")
    for name, (df, base, ms, pick) in out.items():
        n4b = int(df["v4b"].sum())
        lev_pass = df[(df.gross > 1.0) & df.v4b]
        deg_pass = df[(df.gross <= 1.0) & df.v4b]
        print(f"{name}: 4b full-sample cells passing = {n4b}/12 "
              f"(leverage rungs {len(lev_pass)}, de-gross/1.0 rungs {len(deg_pass)}); "
              f"rule-8 pick band={pick['band']} gross={pick['gross']} OOS4b={pick['oos_4b']}")
    # write grid csv
    allg = pd.concat([out[n][0] for n in out])
    allg.to_csv(Path(__file__).with_suffix(".grid.csv"), index=False)
    print("wrote", Path(__file__).with_suffix(".grid.csv").name)


if __name__ == "__main__":
    main()
