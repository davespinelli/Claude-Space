#!/usr/bin/env python3
"""Idea 1193 — is the GROSS DIAL a PURE DD/CAGR SLIDE on a NON-ZERO CASH RATE?

1189 found the gross ladder's Sharpe rung spread is median 0.561% of its mean: the cash
sleeve returns exactly 0%, so for a book that is g invested and (1-g) in cash, mean and vol
both scale by g and Sharpe cancels.  Real cash has paid 0-5.4% over this tape.

This script re-walks the SAME 8-rung gross ladder on the 2026-09-04 KEEP 4b book
(composite, NO vol scaler / above-200d / N=20 / equal weight / weekly) with the cash sleeve
earning a rate, and asks whether the degeneracy survives.

Two tuned parameters ONLY: gross rung (8) x cash rate (5).  All 40 grid points reported.
Rule 8: rung chosen on the first half, second half read once.

Key reporting decision (stated, not tuned): Sharpe is reported BOTH ways.
  - SH0   = the record's convention, metrics(rf=0) on TOTAL returns.
  - SH_ex = excess-return Sharpe, (r - c) vs its own vol, the standard risk-adjusted number.
The distinction is the whole answer; see the .result.md.

Costs 10 bps, next-day execution (engine), weekly rebalance.  Deterministic.
"""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v2_weights, rules_v1_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics  # noqa

OUT = Path(__file__).with_suffix("")
COST_BPS, FREQ = 10, "W"
GROSS_RUNGS = [0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]   # tuned param 1 (8 rungs)
N_BOOK = 20                                                       # frozen, from the 2026-09-04 memo


# ---------------------------------------------------------------- the frozen book
def book_weights(px, n=N_BOOK, gross=0.75):
    """2026-09-04 KEEP 4b book: composite WITHOUT the vol scaler, above-200d eligible,
    top-n equal weight at gross/n each.  Fewer than n eligible -> de-gross to cash
    (never re-spread), matching the live RULES v2 cash convention."""
    s, above, _vol20 = score(px, vol_scale=False)
    rank = s.where(above).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (gross / n)


# ---------------------------------------------------------------- cash sleeve
def cash_rate_series(px, kind):
    """Daily cash return series for the sleeve.  'SHY' is the tape's own short-rate proxy
    (1-3y Treasury ETF total return, ~1.9y duration -- NOT a pure bill, stated as a caveat);
    the flat rungs are constant annualised rates applied 252 d/yr."""
    if kind == "SHY":
        return px["SHY"].pct_change().fillna(0.0)
    return pd.Series(float(kind) / 252.0, index=px.index)

CASH_KINDS = ["0.00", "0.02", "0.04", "0.054", "SHY"]             # tuned param 2 (5 rungs)


def credited(res, px, kind):
    """Total return of the book once the uninvested sleeve earns the cash rate."""
    cash_w = (1.0 - res["weights"].sum(axis=1)).clip(lower=0.0)
    return res["returns"] + cash_w * cash_rate_series(px, kind)


def ann_cash(px, kind, idx):
    c = cash_rate_series(px, kind).reindex(idx).fillna(0.0)
    return (1 + c).prod() ** (252 / len(c)) - 1


# ---------------------------------------------------------------- metrics
def stats(r, c_daily):
    """SH0 = record convention (rf=0).  SH_ex = excess-return Sharpe against the same cash."""
    m = metrics(r)
    ex = r - c_daily.reindex(r.index).fillna(0.0)
    vol = ex.std() * np.sqrt(252)
    return dict(CAGR=m["CAGR"], SH0=m["Sharpe"], MaxDD=m["MaxDD"],
                SH_ex=(ex.mean() * 252) / vol if vol else np.nan, Vol=m["Vol"])


def halves(r):
    h = len(r) // 2
    return r.iloc[:h], r.iloc[h:]


def keep_paths(r, base_r, spy_r, c_daily, oos_sh=None, oos_spy_sh=None):
    """4a vs the live baseline; 4b vs SPY.  Sharpe legs use the record's SH0 convention
    (that is how every committed verdict was scored); SH_ex is reported alongside."""
    a1, a2 = halves(r); b1, b2 = halves(base_r); s1, s2 = halves(spy_r)
    S = lambda x: metrics(x)["Sharpe"]
    m, mb, ms = metrics(r), metrics(base_r), metrics(spy_r)
    p4a = (S(a1) > S(b1)) and (S(a2) > S(b2)) and (m["MaxDD"] >= mb["MaxDD"])
    legs4b = dict(
        H1=S(a1) > S(s1), H2=S(a2) > S(s2),
        DD=m["MaxDD"] >= 0.60 * ms["MaxDD"],              # both negative: >= is "shallower"
        CAGR=m["CAGR"] >= 0.70 * ms["CAGR"],
        OOS=(oos_sh > oos_spy_sh) if oos_sh is not None else None)
    p4b = all(v for v in legs4b.values() if v is not None)
    return p4a, p4b, legs4b


# ---------------------------------------------------------------- run one panel
def run_panel(px, tag):
    spy = px["SPY"].pct_change().fillna(0.0)
    start = px.index[260]                                          # skip 200d warm-up
    print(f"\n{'='*100}\nPANEL {tag}: {px.shape[1]} cols, {px.index[0].date()} -> {px.index[-1].date()}, "
          f"scored from {start.date()}\n{'='*100}")

    # one engine run per gross rung; cash credit applied afterwards (does not touch weights)
    runs = {g: backtest(px, book_weights(px, gross=g), cost_bps=COST_BPS, freq=FREQ) for g in GROSS_RUNGS}
    base = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq=FREQ)
    v1   = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq=FREQ)

    rows, wf_rows = [], []
    for kind in CASH_KINDS:
        c_daily = cash_rate_series(px, kind).loc[start:]
        spy_r = spy.loc[start:]
        base_r = credited(base, px, kind).loc[start:]
        v1_r   = credited(v1, px, kind).loc[start:]
        ms, mb = stats(spy_r, c_daily), stats(base_r, c_daily)

        for g in GROSS_RUNGS:
            r = credited(runs[g], px, kind).loc[start:]
            st = stats(r, c_daily)
            h1, h2 = halves(r)
            sh1, sh2 = metrics(h1)["Sharpe"], metrics(h2)["Sharpe"]
            ex = (r - c_daily)
            e1, e2 = halves(ex)
            exs = lambda e: (e.mean() * 252) / (e.std() * np.sqrt(252))
            rows.append(dict(panel=tag, cash=kind, gross=g, **st, H1_SH0=sh1, H2_SH0=sh2,
                             H1_ex=exs(e1), H2_ex=exs(e2),
                             turnover=runs[g]["turnover"].loc[start:].sum() / (len(r) / 252)))
        # --- rule 8 walk-forward: rung chosen on H1 by SH0, H2 read once ---
        for crit in ("SH0", "SH_ex"):
            sub = [x for x in rows if x["panel"] == tag and x["cash"] == kind]
            pick = max(sub, key=lambda x: x["H1_SH0"] if crit == "SH0" else x["H1_ex"])["gross"]
            r = credited(runs[pick], px, kind).loc[start:]
            _, oos = halves(r)
            c_oos = c_daily.loc[oos.index]
            _, oos_b = halves(base_r); _, oos_s = halves(spy_r)
            so, sb, ss = stats(oos, c_oos), stats(oos_b, c_oos), stats(oos_s, c_oos)
            p4a, p4b, legs = keep_paths(r, base_r, spy_r, c_daily, so["SH0"], ss["SH0"])
            wf_rows.append(dict(panel=tag, cash=kind, crit=crit, pick=pick,
                                oos_CAGR=so["CAGR"], oos_SH0=so["SH0"], oos_SHex=so["SH_ex"], oos_DD=so["MaxDD"],
                                base_CAGR=sb["CAGR"], base_SH0=sb["SH0"], base_DD=sb["MaxDD"],
                                spy_CAGR=ss["CAGR"], spy_SH0=ss["SH0"], spy_SHex=ss["SH_ex"], spy_DD=ss["MaxDD"],
                                KEEP4a=p4a, KEEP4b=p4b, legs=json.dumps({k: (None if v is None else bool(v))
                                                                        for k, v in legs.items()})))
        # console: the full ladder at this cash rate
        d = pd.DataFrame([x for x in rows if x["panel"] == tag and x["cash"] == kind])
        sp0 = d["SH0"].max() - d["SH0"].min(); spx = d["SH_ex"].max() - d["SH_ex"].min()
        print(f"\n--- {tag} cash={kind} (realised {ann_cash(px, kind, spy_r.index):.2%}/yr) | "
              f"SPY CAGR {ms['CAGR']:.2%} SH0 {ms['SH0']:.3f} SHex {ms['SH_ex']:.3f} DD {ms['MaxDD']:.2%} | "
              f"base CAGR {mb['CAGR']:.2%} SH0 {mb['SH0']:.3f} DD {mb['MaxDD']:.2%}")
        print(d[["gross", "CAGR", "SH0", "SH_ex", "MaxDD", "Vol", "H1_SH0", "H2_SH0", "turnover"]]
              .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        print(f"    rung spread SH0 {sp0:.4f} ({sp0/d['SH0'].mean()*100:.2f}% of mean) | "
              f"SH_ex {spx:.4f} ({spx/abs(d['SH_ex'].mean())*100:.2f}% of mean)")

    # full-sample KEEP table at every grid point
    keep_rows = []
    for kind in CASH_KINDS:
        c_daily = cash_rate_series(px, kind).loc[start:]
        base_r = credited(base, px, kind).loc[start:]; spy_r = spy.loc[start:]
        for g in GROSS_RUNGS:
            r = credited(runs[g], px, kind).loc[start:]
            _, oos = halves(r); _, oos_s = halves(spy_r)
            p4a, p4b, legs = keep_paths(r, base_r, spy_r, c_daily,
                                        metrics(oos)["Sharpe"], metrics(oos_s)["Sharpe"])
            keep_rows.append(dict(panel=tag, cash=kind, gross=g, KEEP4a=p4a, KEEP4b=p4b,
                                  **{f"leg_{k}": (None if v is None else bool(v)) for k, v in legs.items()}))
    kd = pd.DataFrame(keep_rows)
    print(f"\n--- {tag} KEEP grid (full sample, OOS leg = 2nd half vs SPY 2nd half)")
    print(kd.pivot_table(index="gross", columns="cash", values="KEEP4b", aggfunc="first").to_string())
    print(f"    4a passes {int(kd['KEEP4a'].sum())}/{len(kd)} | 4b passes {int(kd['KEEP4b'].sum())}/{len(kd)}")
    return pd.DataFrame(rows), pd.DataFrame(wf_rows), kd


def main():
    all_l, all_w, all_k = [], [], []
    for tag, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        l, w, k = run_panel(px, tag)
        all_l.append(l); all_w.append(w); all_k.append(k)
    L = pd.concat(all_l); W = pd.concat(all_w); K = pd.concat(all_k)
    L.to_csv(f"{OUT}.ladder.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    K.to_csv(f"{OUT}.keepgrid.csv", index=False)

    print(f"\n{'='*100}\nRULE 8 WALK-FORWARD (rung chosen on H1 only, H2 read once)\n{'='*100}")
    print(W[["panel", "cash", "crit", "pick", "oos_CAGR", "oos_SH0", "oos_SHex", "oos_DD",
             "base_SH0", "base_DD", "spy_CAGR", "spy_SH0", "spy_SHex", "spy_DD", "KEEP4a", "KEEP4b"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print(f"\n{'='*100}\nDEGENERACY: rung spread as % of mean, per panel x cash rate\n{'='*100}")
    dg = L.groupby(["panel", "cash"]).apply(
        lambda d: pd.Series({"SH0_spread": d["SH0"].max() - d["SH0"].min(),
                             "SH0_pct_of_mean": (d["SH0"].max() - d["SH0"].min()) / d["SH0"].mean() * 100,
                             "SH0_argmax_gross": d.loc[d["SH0"].idxmax(), "gross"],
                             "SHex_spread": d["SH_ex"].max() - d["SH_ex"].min(),
                             "SHex_pct_of_mean": (d["SH_ex"].max() - d["SH_ex"].min()) / abs(d["SH_ex"].mean()) * 100,
                             "SHex_argmax_gross": d.loc[d["SH_ex"].idxmax(), "gross"],
                             "CAGR_spread_pp": (d["CAGR"].max() - d["CAGR"].min()) * 100,
                             "DD_spread_pp": (d["MaxDD"].max() - d["MaxDD"].min()) * 100}),
        include_groups=False)
    print(dg.to_string(float_format=lambda x: f"{x:.4f}"))
    dg.to_csv(f"{OUT}.degeneracy.csv")
    print("\nwrote:", OUT.name + ".{ladder,walkforward,keepgrid,degeneracy}.csv")


if __name__ == "__main__":
    main()
