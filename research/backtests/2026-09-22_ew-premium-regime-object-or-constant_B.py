#!/usr/bin/env python3
"""Idea 935 (lane B, 2026-09-22): is the RSP-minus-SPY EQUAL-WEIGHT PREMIUM a REGIME
OBJECT, or is the record right to quote it as a CONSTANT?

WHY THIS IDEA.  Idea 924 measured the only SURVIVORSHIP-FREE leg of U56's +0.2006 of
Sharpe -- RSP vs SPY, both TRADED instruments, no name selection -- at +0.0750 in
2009-2013, -0.0863 on FULL and -0.1797 out of sample.  It changes SIGN on the window the
record quotes it in, and every committed citation of it quotes a single number.  Two
readings are consistent with that: (i) the premium is a CONSTANT and the sign flip is
noise about a ~0 mean, or (ii) it is a REGIME OBJECT whose sign is set by an ex-ante
observable, in which case a book that conditions on the regime is worth capital and the
committed constant is a mis-statement.  This run prices both.

THE TWO ARMS.
  ARM A (diagnostic).  Split every session into terciles of an EX-ANTE, CAUSAL regime
  rank and report the annualised premium and its t-stat per tercile, on FULL / IS / OOS.
  If (i) is right the terciles are indistinguishable.
  ARM B (capital).  The book the diagnostic implies: hold RSP when the regime rank >= q,
  else SPY -- a real, fully-specified, tradable switch, scored against the LIVE RULES v2
  baseline AND SPY on BOTH KEEP paths with the mandatory rule-8 walk-forward.

TUNED PARAMETERS -- EXACTLY TWO, EVERY GRID POINT PUBLISHED.
  v in {BREADTH, DISP, RATE}  x  q in {0.00, 0.20, 0.40, 0.50, 0.60, 0.80, 1.01}  = 21 cells.
  q=0.00 is always-RSP and q=1.01 is always-SPY -- the two CONSTANT controls, identical
  across v, kept in the grid so the conditioning is scored against its own null of "do
  not condition at all".
PUBLISHED-NOT-TUNED AXES: panel {U56, B136}; gross {1.00, 0.75}; cost {0, 10, 25, 50} bps
  (headline 10); windows {FULL, IS 2010-2016, OOS 2017-2026}.

DIRECTION IS FIXED A PRIORI, NOT FITTED.  The hypothesis is the standard one -- broad
participation favours EQUAL weight -- so rank >= q always buys RSP and rank < q always
buys SPY, on all three variables, before any number is read.  A premium whose sign runs
the other way is therefore a KILL of this book, not a prompt to flip the inequality.

REGIME VARIABLES (all price-only, all known at the close of t, none tuned):
  BREADTH  fraction of the panel's names above their own 200d MA.
  DISP     cross-sectional stdev of trailing 63d returns across the panel's names.
  RATE     63d change in IEF (a price-only rate-direction proxy; IEF up = rates falling).
  RSP and SPY are EXCLUDED from the breadth/dispersion cross-section so the signal cannot
  read its own traded legs.  Each variable is converted to an EXPANDING percentile rank
  (min 504 sessions of history), which is causal by construction -- no full-sample
  quantile is ever used.

EXECUTION.  Weekly rebalance, weights decided at close t applied at t+1 (engine), 10 bps
per unit turnover, long-only, no leverage.  Price-only on the committed caches
(U56 = research/universe.json, B136 = research/universe_broad.json).  No EDGAR / Form 4 /
options / live data.  SURVIVORSHIP: both panels are CURRENT constituents, so all absolute
levels are optimistic; the RSP-vs-SPY contrast itself is survivorship-free (two traded
ETFs), and only the breadth/dispersion SIGNAL is built on the survivorship-bearing list.
"""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from baseline import load_universe, rules_v2_weights
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics

VARS = ["BREADTH", "DISP", "RATE"]
QS = [0.00, 0.20, 0.40, 0.50, 0.60, 0.80, 1.01]
GROSSES = [1.00, 0.75]
COSTS = [0, 10, 25, 50]
MINHIST = 504                      # sessions of history before an expanding rank is used
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
NULL_DRAWS = 200
NULL_BLOCK = 21
SEED = 20260922


# ----------------------------------------------------------------- regime machinery
def expanding_rank(s: pd.Series, minhist=MINHIST) -> pd.Series:
    """Causal percentile rank: r_t = fraction of s[0..t] that is <= s_t.  NaN until
    minhist observations exist.  No full-sample quantile is ever touched."""
    a = s.to_numpy(dtype=float)
    out = np.full(len(a), np.nan)
    for t in range(len(a)):
        if t + 1 < minhist or not np.isfinite(a[t]):
            continue
        w = a[: t + 1]
        w = w[np.isfinite(w)]
        out[t] = (w <= a[t]).mean()
    return pd.Series(out, index=s.index)


def regimes(px: pd.DataFrame) -> pd.DataFrame:
    """The three ex-ante regime ranks for a panel."""
    names = [c for c in px.columns if c not in ("RSP", "SPY")]
    sub = px[names]
    breadth = (sub > sub.rolling(200).mean()).sum(axis=1) / sub.notna().sum(axis=1)
    disp = (sub / sub.shift(63) - 1).std(axis=1)
    rate = px["IEF"] / px["IEF"].shift(63) - 1
    raw = pd.DataFrame({"BREADTH": breadth, "DISP": disp, "RATE": rate})
    return pd.DataFrame({c: expanding_rank(raw[c]) for c in VARS})


# ----------------------------------------------------------------- books and metrics
def two_leg(px: pd.DataFrame) -> pd.DataFrame:
    """The switch book only ever holds RSP or SPY, so it is backtested on the two-column
    price frame.  engine.backtest is exactly equivalent here -- columns whose weight is
    always 0 contribute nothing to returns, turnover or the cash-drift denominator -- and
    it is ~30x faster, which is what buys the 200-draw matched null."""
    return px[["RSP", "SPY"]]


def switch_weights(px, rank: pd.Series, q: float, gross: float) -> pd.DataFrame:
    """rank >= q  -> RSP at `gross`;  rank < q -> SPY at `gross`.  Before the rank exists
    the book holds SPY (the neutral leg), stated rather than dropped."""
    on = (rank >= q).fillna(False)
    w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    w["RSP"] = np.where(on, gross, 0.0)
    w["SPY"] = np.where(on, 0.0, gross)
    return w


def met(r: pd.Series) -> dict:
    m = metrics(r)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def v4a(m, b):
    """PROTOCOL 4a: Sharpe > live rules in BOTH halves, MaxDD no worse."""
    return (m["H1"] > b["H1"]) and (m["H2"] > b["H2"]) and (m["MaxDD"] >= b["MaxDD"])


def v4b(m, s):
    """PROTOCOL 4b: Sharpe > SPY both halves, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's."""
    legs = dict(H1=m["H1"] > s["H1"], H2=m["H2"] > s["H2"],
                DD=m["MaxDD"] >= 0.60 * s["MaxDD"], CAGR=m["CAGR"] >= 0.70 * s["CAGR"])
    return all(legs.values()), legs


def legstr(legs):
    return "".join(k if v else k.lower() for k, v in
                   [("H", legs["H1"]), ("h", legs["H2"]), ("D", legs["DD"]), ("C", legs["CAGR"])])


# ----------------------------------------------------------------- panel run
def run_panel(pname: str, px: pd.DataFrame, out: list):
    print(f"\n{'='*92}\nPANEL {pname}  ({px.shape[1]} columns, {px.index[0].date()} .. {px.index[-1].date()})\n{'='*92}")
    R = regimes(px)
    start = R.dropna().index[0]
    print(f"first session with all three causal ranks available: {start.date()}  "
          f"(200d MA + {MINHIST}-session expanding rank)")

    win = dict(FULL=(start, px.index[-1]),
               IS=(start, pd.Timestamp(IS_END)),
               OOS=(pd.Timestamp(OOS_START), px.index[-1]))

    def cut(r, w):
        a, b = win[w]
        return r.loc[a:b]

    spy_r = px["SPY"].pct_change().fillna(0.0).loc[start:]
    rsp_r = px["RSP"].pct_change().fillna(0.0).loc[start:]
    base_r = backtest(px, rules_v2_weights(px), cost_bps=10, freq="W")["returns"].loc[start:]

    # ---------- GATE G1: two-column backtest == full-panel backtest ----------
    wf = switch_weights(px, R["BREADTH"], 0.50, 1.00)
    pxl = two_leg(px)
    wl = switch_weights(pxl, R["BREADTH"], 0.50, 1.00)
    d = (backtest(px, wf, cost_bps=10, freq="W")["returns"]
         - backtest(pxl, wl, cost_bps=10, freq="W")["returns"]).abs().max()
    print(f"GATE G1  two-column runner == full-panel runner, max|d| = {d:.3e}")
    assert d < 1e-12

    # ---------- ARM A: is the premium a regime object? ----------
    prem = (rsp_r - spy_r)
    print("\nARM A -- TERCILE DIAGNOSTIC.  Annualised RSP-minus-SPY premium (pp/yr) by "
          "ex-ante regime tercile, with Newey-free t = mean/SE(mean) on daily data.")
    print(f"{'var':<8}{'window':<7}{'lo(pp/yr)':>11}{'t_lo':>7}{'mid':>9}{'t_mid':>7}"
          f"{'hi':>9}{'t_hi':>7}{'hi-lo':>9}{'t_diff':>8}{'n_lo/n_hi':>12}")
    for v in VARS:
        for w in ("FULL", "IS", "OOS"):
            p, rk = cut(prem, w), cut(R[v], w)
            lo, mid, hi = p[rk < 1/3], p[(rk >= 1/3) & (rk < 2/3)], p[rk >= 2/3]
            def st(x):
                if len(x) < 30: return np.nan, np.nan
                return x.mean() * 252 * 100, x.mean() / (x.std() / np.sqrt(len(x)))
            (a1, t1), (a2, t2), (a3, t3) = st(lo), st(mid), st(hi)
            d = hi.mean() - lo.mean()
            sd = np.sqrt(hi.var(ddof=1)/len(hi) + lo.var(ddof=1)/len(lo)) if len(hi) > 30 and len(lo) > 30 else np.nan
            td = d / sd if sd and np.isfinite(sd) else np.nan
            print(f"{v:<8}{w:<7}{a1:>11.2f}{t1:>7.2f}{a2:>9.2f}{t2:>7.2f}{a3:>9.2f}{t3:>7.2f}"
                  f"{d*252*100:>9.2f}{td:>8.2f}{f'{len(lo)}/{len(hi)}':>12}")
            out.append(dict(kind="tercile", panel=pname, var=v, window=w,
                            lo=a1, t_lo=t1, mid=a2, hi=a3, t_hi=t3, diff=d*252*100, t_diff=td))

    # ---------- ARM B: the capital grid ----------
    print("\nARM B -- FULL GRID, every point published.  Book: rank>=q -> RSP, else SPY. "
          "10 bps, weekly, t+1.  4a vs RULES v2 (live), 4b vs SPY.  "
          "Leg string HhDC: upper = leg passes.")
    grid = {}
    for gross in GROSSES:
        refs = {}
        for w in ("FULL", "IS", "OOS"):
            refs[w] = (met(cut(base_r, w)), met(cut(spy_r, w)))
        print(f"\n  gross {gross:.2f}   RULES v2 FULL {refs['FULL'][0]['Sharpe']:.3f} "
              f"(DD {refs['FULL'][0]['MaxDD']:.2%}) | SPY FULL {refs['FULL'][1]['Sharpe']:.3f} "
              f"(CAGR {refs['FULL'][1]['CAGR']:.2%}, DD {refs['FULL'][1]['MaxDD']:.2%})")
        print(f"  {'var':<8}{'q':>6}{'sw/yr':>7}"
              f"{'FULL CAGR':>11}{'Sh':>7}{'MaxDD':>9}{'4a':>4}{'4b':>6}"
              f"{'| OOS CAGR':>12}{'Sh':>7}{'MaxDD':>9}{'4a':>4}{'4b':>6}")
        for v in VARS:
            for q in QS:
                key = (gross, "CONST", q) if q in (0.00, 1.01) else (gross, v, q)
                if key in grid:
                    continue
                pxl = two_leg(px)
                res = backtest(pxl, switch_weights(pxl, R[v], q, gross), cost_bps=10, freq="W")
                r = res["returns"].loc[start:]
                # switches/yr counted on the TARGET regime, not on held weights: below
                # gross 1.00 the held book drifts every session and a held-weight diff
                # would report ~250/yr for a book that never switches at all.
                on_t = (R[v] >= q).fillna(False).loc[start:]
                sw = float((on_t != on_t.shift()).iloc[1:].sum()) / (len(r) / 252)
                row = {}
                for w in ("FULL", "IS", "OOS"):
                    m = met(cut(r, w))
                    b, s = refs[w]
                    ok_b, legs = v4b(m, s)
                    row[w] = dict(m=m, a=v4a(m, b), b=ok_b, legs=legs)
                grid[key] = dict(ret=r, row=row, sw=sw, var=key[1], q=q, gross=gross)
                f, o = row["FULL"], row["OOS"]
                print(f"  {key[1]:<8}{q:>6.2f}{sw:>7.1f}"
                      f"{f['m']['CAGR']:>11.2%}{f['m']['Sharpe']:>7.3f}{f['m']['MaxDD']:>9.2%}"
                      f"{'Y' if f['a'] else '.':>4}{legstr(f['legs']):>6}"
                      f"{o['m']['CAGR']:>12.2%}{o['m']['Sharpe']:>7.3f}{o['m']['MaxDD']:>9.2%}"
                      f"{'Y' if o['a'] else '.':>4}{legstr(o['legs']):>6}")
                out.append(dict(kind="grid", panel=pname, gross=gross, var=key[1], q=q,
                                switches_yr=sw,
                                **{f"{w}_{k}": row[w]["m"][k] for w in ("FULL", "IS", "OOS")
                                   for k in ("CAGR", "Sharpe", "MaxDD")},
                                FULL_4a=row["FULL"]["a"], FULL_4b=row["FULL"]["b"],
                                OOS_4a=row["OOS"]["a"], OOS_4b=row["OOS"]["b"],
                                OOS_legs=legstr(row["OOS"]["legs"])))

    # ---------- RULE 8 ----------
    print(f"\nRULE 8 WALK-FORWARD ({pname}).  Parameters (v, q) chosen on IS "
          f"{start.date()}..{IS_END} by IS Sharpe ONLY; 2017-2026 read once.")
    for gross in GROSSES:
        cells = {k: g for k, g in grid.items() if k[0] == gross}
        pick = max(cells, key=lambda k: cells[k]["row"]["IS"]["m"]["Sharpe"])
        g = cells[pick]
        b_is, s_is = met(cut(base_r, "IS")), met(cut(spy_r, "IS"))
        b_o, s_o = met(cut(base_r, "OOS")), met(cut(spy_r, "OOS"))
        mi, mo = g["row"]["IS"]["m"], g["row"]["OOS"]["m"]
        okb, legs = v4b(mo, s_o)
        print(f"  gross {gross:.2f}  IS pick = ({pick[1]}, q={pick[2]:.2f})  "
              f"IS Sharpe {mi['Sharpe']:.3f} (SPY {s_is['Sharpe']:.3f}, RULES v2 {b_is['Sharpe']:.3f})")
        print(f"      OOS   book {mo['CAGR']:>8.2%} / {mo['Sharpe']:.3f} / {mo['MaxDD']:>8.2%}"
              f"   RULES v2 {b_o['CAGR']:>8.2%} / {b_o['Sharpe']:.3f} / {b_o['MaxDD']:>8.2%}"
              f"   SPY {s_o['CAGR']:>8.2%} / {s_o['Sharpe']:.3f} / {s_o['MaxDD']:>8.2%}")
        print(f"      OOS 4a {'PASS' if g['row']['OOS']['a'] else 'FAIL'}   "
              f"OOS 4b {'PASS' if okb else 'FAIL'} legs {legs}   "
              f"4b caps: DD <= {0.60*s_o['MaxDD']:.2%}, CAGR >= {0.70*s_o['CAGR']:.2%}")
        out.append(dict(kind="rule8", panel=pname, gross=gross, pick_var=pick[1], pick_q=pick[2],
                        IS_Sharpe=mi["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                        OOS_MaxDD=mo["MaxDD"], OOS_4a=g["row"]["OOS"]["a"], OOS_4b=okb,
                        base_OOS_Sharpe=b_o["Sharpe"], spy_OOS_Sharpe=s_o["Sharpe"]))

        # The CONDITIONING-ONLY chooser: the same IS-Sharpe rule restricted to the cells
        # that actually condition (the two CONSTANT controls removed).  This is the fair
        # test of the DEVICE -- what the best regime book, chosen honestly in sample,
        # does out of sample.
        cond = {k: g for k, g in cells.items() if k[1] != "CONST"}
        cpick = max(cond, key=lambda k: cond[k]["row"]["IS"]["m"]["Sharpe"])
        cg = cond[cpick]
        cmi, cmo = cg["row"]["IS"]["m"], cg["row"]["OOS"]["m"]
        cokb, clegs = v4b(cmo, s_o)
        print(f"      CONDITIONING-ONLY pick = ({cpick[1]}, q={cpick[2]:.2f})  IS Sharpe "
              f"{cmi['Sharpe']:.3f} vs always-SPY IS {cells[(gross,'CONST',1.01)]['row']['IS']['m']['Sharpe']:.3f}")
        print(f"      OOS   book {cmo['CAGR']:>8.2%} / {cmo['Sharpe']:.3f} / {cmo['MaxDD']:>8.2%}"
              f"   4a {'PASS' if cg['row']['OOS']['a'] else 'FAIL'}  4b {'PASS' if cokb else 'FAIL'} {legstr(clegs)}")
        out.append(dict(kind="rule8_cond", panel=pname, gross=gross, pick_var=cpick[1],
                        pick_q=cpick[2], IS_Sharpe=cmi["Sharpe"], OOS_CAGR=cmo["CAGR"],
                        OOS_Sharpe=cmo["Sharpe"], OOS_MaxDD=cmo["MaxDD"],
                        OOS_4a=cg["row"]["OOS"]["a"], OOS_4b=cokb))

        # cost sensitivity at the pick, tuned nowhere
        line = []
        for c in COSTS:
            pxl = two_leg(px)
            rr = backtest(pxl, switch_weights(pxl, R[cpick[1]], cpick[2], gross), cost_bps=c, freq="W")["returns"]
            mm = met(cut(rr.loc[start:], "OOS"))
            line.append(f"{c}bps {mm['Sharpe']:.3f}")
        print("      OOS Sharpe of the conditioning-only pick vs cost: " + " | ".join(line))

        # matched null: same on-fraction, block-resampled regime, direction preserved
        if gross == 1.00:
            on = (R[cpick[1]] >= cpick[2]).loc[start:]
            frac = float(on.mean())
            rng = np.random.default_rng(SEED)
            n = len(on)
            nb = int(np.ceil(n / NULL_BLOCK))
            draws = []
            for _ in range(NULL_DRAWS):
                blocks = rng.random(nb) < frac
                fake = np.repeat(blocks, NULL_BLOCK)[:n]
                pxl = two_leg(px)
                s_on = pd.Series(fake, index=on.index).reindex(pxl.index).fillna(False)
                w_df = pd.DataFrame(0.0, index=pxl.index, columns=pxl.columns)
                w_df["RSP"] = np.where(s_on, gross, 0.0)
                w_df["SPY"] = np.where(s_on, 0.0, gross)
                rr = backtest(pxl, w_df, cost_bps=10, freq="W")["returns"].loc[start:]
                draws.append(met(cut(rr, "OOS"))["Sharpe"])
            draws = np.array(draws)
            pct = float((draws <= cmo["Sharpe"]).mean())
            print(f"      MATCHED NULL ({NULL_DRAWS} block-{NULL_BLOCK} draws, on-fraction "
                  f"{frac:.3f} preserved): OOS Sharpe percentile of the real regime = {pct:.3f}  "
                  f"(null median {np.median(draws):.3f}, 5/95 {np.percentile(draws,5):.3f}/"
                  f"{np.percentile(draws,95):.3f})")
            out.append(dict(kind="null", panel=pname, gross=gross, pick_var=cpick[1], pick_q=cpick[2],
                            pctile=pct, null_median=float(np.median(draws)), real=cmo["Sharpe"]))


def main():
    out = []
    run_panel("U56", load_universe(), out)
    run_panel("B136", load_universe(broad=True), out)
    df = pd.DataFrame(out)
    p = ROOT / "backtests" / "out" / "2026-09-22_ew-premium-regime_B.csv"
    p.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(p, index=False)
    print(f"\n{len(df)} rows written to {p.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
