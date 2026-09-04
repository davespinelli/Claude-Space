#!/usr/bin/env python3
"""QUEUE idea 39 — small-cap-eligible-equal-weight (lane C, 2026-09-04).

Question: the project's two 4b KEEP-candidates (idea 2's top-20 equal-weight at 75%
gross, and idea 46's f=0.85 fraction rule) were found on universe.json (56 ETFs and
mega caps) and partially confirmed on universe_broad.json (136 large caps).  Both are
current-constituent lists of large, liquid names.  Does the "equal-weight everything
that is above its 200d MA with vol20 < 0.60" book (idea 28's v2 logic, i.e. f=1.00)
survive on a structurally different universe — the 483-name sub-$2B small-cap panel?

Construction (fixed in advance, nothing here is tuned except the two parameters below):
  * Panel: baseline.load_universe(small=True); the 44 names with max_1d_move >= 1.0 in
    data/small_meta.csv (corrupted / relisted series) are dropped -> 439 names.  SPY is
    a benchmark column only, never held.
  * Eligibility: px > 200d MA  AND  vol20 < 0.60 annualised.  (v1's own gates.)
  * Score, where a rank is needed: v1's composite mean(pct-rank of 12-1, 6m, 3m)
    x (0.5 + 0.5*above200d), WITHOUT the /sqrt(vol20) term (ideas 1/2/46 established
    the scaler is harmful; it is not a free parameter here, it is the candidate's own
    scorer).
  * Weekly rebalance, weights decided at close t and applied at t+1 (engine), 10 bps
    per unit turnover.  Long only, no leverage.

Two tuned parameters, all 10 grid points reported:
  1. selection breadth: F f in {0.45, 0.85, 1.00}  (top ceil(f*E_t) names, equal weight)
                        N n in {20, 40}            (top n names, equal weight, cash if E_t<n)
     f=1.00 is idea 39's pre-registered primary arm; the others exist so the comparison
     with the mega-cap KEEPs is like-for-like rather than a single point.
  2. gross exposure: 0.75 and 1.00.

Reports: full sample, halves, rule-8 walk-forward (params picked on 2010-2016 only,
evaluated untouched on 2017-2026), and both PROTOCOL KEEP paths 4a and 4b.

SURVIVORSHIP: the small panel is the *current* constituents of a sub-$2B screen
(data/SMALL_PANEL_README.md).  Names that delisted or were acquired 2010-2026 are
absent, so absolute CAGRs are optimistic in one direction only.  Cross-arm
comparisons (all arms hold the same names) are far less affected.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, score  # noqa: E402
from engine import backtest, metrics  # noqa: E402

COST_BPS = 10
FREQ = "W"
GROSS = [0.75, 1.00]
ARMS = [("F", 0.45), ("F", 0.85), ("F", 1.00), ("N", 20), ("N", 40)]
IS_END = "2016-12-31"   # rule 8: parameters chosen here only
OOS_START = "2017-01-01"


# ---------------------------------------------------------------- panel
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c != "SPY" and c not in bad]
    print(f"panel: {px.shape[1] - 1} names -> {len(keep)} after dropping {len(bad)} corrupted "
          f"(max_1d_move >= 1.0); {px.index[0].date()} .. {px.index[-1].date()}, {len(px)} rows")
    return px[keep + ["SPY"]], keep


# ---------------------------------------------------------------- books
def eligibility(px, cols):
    """Boolean eligible mask and the no-vol-scaler composite, over the held columns only."""
    sub = px[cols]
    s, above, vol20 = score(sub, vol_scale=False)
    elig = above & (vol20 < 0.60)
    return elig.fillna(False), s.where(elig)


def weights_fn(px, cols, arm, param, gross):
    """arm 'F': top ceil(param * E_t).  arm 'N': top param, cash when E_t < param."""
    elig, s = eligibility(px, cols)
    E = elig.sum(axis=1)
    rank = s.rank(axis=1, ascending=False)
    if arm == "F":
        k = np.ceil(param * E).astype(int).clip(lower=0)
    else:
        k = pd.Series(np.minimum(param, E), index=px.index)
    kk = k.replace(0, np.nan)
    held = rank.le(k, axis=0) & elig
    if arm == "N":
        # idea 2's clause: when fewer than n are eligible hold all of them at gross/n
        # (i.e. de-gross into cash) rather than renormalising.
        per = pd.Series(gross / param, index=px.index)
    else:
        per = gross / kk
    w = held.astype(float).mul(per, axis=0).fillna(0.0)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[cols] = w
    return out


# ---------------------------------------------------------------- metrics
def stats(r):
    m = metrics(r)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def verdicts(d, base, spy, oos_sharpe=None):
    """PROTOCOL rule 4.  4a vs the live book, 4b vs SPY (incl. OOS when supplied)."""
    a_ok = d["H1"] > base["H1"] and d["H2"] > base["H2"] and d["MaxDD"] >= base["MaxDD"]
    fails = []
    if d["H1"] <= spy["H1"]: fails.append("H1")
    if d["H2"] <= spy["H2"]: fails.append("H2")
    if oos_sharpe is not None and oos_sharpe[0] <= oos_sharpe[1]: fails.append("OOS")
    if d["MaxDD"] < 0.60 * spy["MaxDD"]: fails.append("DD")       # MaxDD negative
    if d["CAGR"] < 0.70 * spy["CAGR"]: fails.append("CAGR")
    b_txt = "KEEP 4b" if not fails else "KILL 4b (" + ",".join(fails) + ")"
    return ("KEEP 4a" if a_ok else "KILL 4a"), b_txt, fails


def run(px, cols, arm, param, gross, start):
    w = weights_fn(px, cols, arm, param, gross)
    res = backtest(px, w, cost_bps=COST_BPS, freq=FREQ)
    r = res["returns"].loc[start:]
    held = (w.loc[start:] > 0).sum(axis=1)
    yrs = len(r) / 252
    return r, res["turnover"].loc[start:].sum() / yrs, held.mean()


def main():
    px, cols = small_panel()
    start = px.index[260]
    spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
    # v1 baseline on the small panel, SPY excluded from the holdable set (here it is a
    # benchmark column, not a constituent).
    v1w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    v1w[cols] = rules_v1_weights(px[cols])
    base_r = backtest(px, v1w, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]

    spy, base = stats(spy_r), stats(base_r)
    elig, _ = eligibility(px, cols)
    E = elig.loc[start:].sum(axis=1)
    print(f"\nsample {start.date()} .. {px.index[-1].date()}   eligible names/day: "
          f"mean {E.mean():.1f}, min {E.min()}, max {E.max()}, p10 {E.quantile(.1):.0f}")
    print(f"SPY   : CAGR {spy['CAGR']:.1%}  Sharpe {spy['Sharpe']:.3f}  MaxDD {spy['MaxDD']:.1%}  "
          f"halves {spy['H1']:.3f}/{spy['H2']:.3f}")
    print(f"v1    : CAGR {base['CAGR']:.1%}  Sharpe {base['Sharpe']:.3f}  MaxDD {base['MaxDD']:.1%}  "
          f"halves {base['H1']:.3f}/{base['H2']:.3f}")
    print(f"4b bars: Sharpe > {spy['H1']:.3f} (H1) and > {spy['H2']:.3f} (H2), "
          f"MaxDD >= {0.60 * spy['MaxDD']:.1%}, CAGR >= {0.70 * spy['CAGR']:.1%}\n")

    # ---- full sample grid -------------------------------------------------
    rows, series = [], {}
    for arm, param in ARMS:
        for g in GROSS:
            r, turn, nheld = run(px, cols, arm, param, g, start)
            d = stats(r)
            v4a, v4b, _ = verdicts(d, base, spy)
            label = f"{arm} {'f' if arm == 'F' else 'n'}={param} g={g:.2f}"
            rows.append(dict(arm=label, **d, names=nheld, turn=turn, v4a=v4a, v4b=v4b))
            series[label] = r
    grid = pd.DataFrame(rows).set_index("arm")
    print("=== FULL SAMPLE (all 10 grid points, 10 bps, weekly, t+1) ===")
    print(grid.to_string(formatters={"CAGR": "{:.1%}".format, "MaxDD": "{:.1%}".format,
                                     "Sharpe": "{:.3f}".format, "H1": "{:.3f}".format,
                                     "H2": "{:.3f}".format, "names": "{:.1f}".format,
                                     "turn": "{:.1f}x".format}))

    # ---- rule 8 walk-forward ---------------------------------------------
    # Two selection rules fixed BEFORE any OOS number is read.
    is_rows = []
    for lab, r in series.items():
        m = metrics(r.loc[:IS_END])
        is_rows.append(dict(label=lab, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"]))
    isdf = pd.DataFrame(is_rows).set_index("label")
    spy_is = metrics(spy_r.loc[:IS_END])
    print(f"\n=== IN-SAMPLE {start.date()}..{IS_END} (selection only) ===")
    print(f"SPY IS: CAGR {spy_is['CAGR']:.1%} Sharpe {spy_is['Sharpe']:.3f} MaxDD {spy_is['MaxDD']:.1%}")
    print(isdf.to_string(
        formatters={"CAGR": "{:.1%}".format, "MaxDD": "{:.1%}".format, "Sharpe": "{:.3f}".format}))

    picks = {}
    picks["plain-Sharpe"] = isdf["Sharpe"].idxmax()
    ok = isdf[(isdf["MaxDD"] >= 0.60 * spy_is["MaxDD"]) & (isdf["CAGR"] >= 0.70 * spy_is["CAGR"])]
    picks["4b-aware"] = ok["Sharpe"].idxmax() if len(ok) else None

    spy_oos = metrics(spy_r.loc[OOS_START:])
    base_oos = metrics(base_r.loc[OOS_START:])
    print(f"\n=== OUT OF SAMPLE {OOS_START}.. (untouched) ===")
    print(f"SPY   OOS: CAGR {spy_oos['CAGR']:.1%} Sharpe {spy_oos['Sharpe']:.3f} MaxDD {spy_oos['MaxDD']:.1%}")
    print(f"v1    OOS: CAGR {base_oos['CAGR']:.1%} Sharpe {base_oos['Sharpe']:.3f} MaxDD {base_oos['MaxDD']:.1%}")
    for rule, lab in picks.items():
        if lab is None:
            print(f"{rule:12s}: picks NOTHING (no in-sample point met the 4b drawdown/CAGR bars)")
            continue
        m = metrics(series[lab].loc[OOS_START:])
        print(f"{rule:12s}: picks {lab:18s} OOS CAGR {m['CAGR']:.1%} Sharpe {m['Sharpe']:.3f} "
              f"MaxDD {m['MaxDD']:.1%}  (SPY {spy_oos['Sharpe']:.3f})")

    # OOS Sharpe for every point, so the 4b OOS test can be applied to the whole grid
    print("\n=== 4b WITH THE OOS TEST APPLIED TO EVERY POINT ===")
    out = []
    for lab, r in series.items():
        d = stats(r)
        mo = metrics(r.loc[OOS_START:])
        v4a, v4b, _ = verdicts(d, base, spy, oos_sharpe=(mo["Sharpe"], spy_oos["Sharpe"]))
        out.append(dict(arm=lab, CAGR=d["CAGR"], Sharpe=d["Sharpe"], MaxDD=d["MaxDD"],
                        H1=d["H1"], H2=d["H2"], oosCAGR=mo["CAGR"], oosSharpe=mo["Sharpe"],
                        oosMaxDD=mo["MaxDD"], v4a=v4a, v4b=v4b))
    fin = pd.DataFrame(out).set_index("arm")
    print(fin.to_string(formatters={"CAGR": "{:.1%}".format, "MaxDD": "{:.1%}".format,
                                    "Sharpe": "{:.3f}".format, "H1": "{:.3f}".format,
                                    "H2": "{:.3f}".format, "oosCAGR": "{:.1%}".format,
                                    "oosSharpe": "{:.3f}".format, "oosMaxDD": "{:.1%}".format}))

    # ---- control: does the eligibility filter do anything at all? ----------
    print("\n=== CONTROLS ===")
    ew = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    ew[cols] = 0.75 / len(cols)
    r_ew = backtest(px, ew, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    d = stats(r_ew)
    mo = metrics(r_ew.loc[OOS_START:])
    print(f"EW all {len(cols)} names @75% gross (no filter): CAGR {d['CAGR']:.1%} Sharpe {d['Sharpe']:.3f} "
          f"MaxDD {d['MaxDD']:.1%} halves {d['H1']:.3f}/{d['H2']:.3f} OOS {mo['CAGR']:.1%}/{mo['Sharpe']:.3f} "
          f"turn {backtest(px, ew, cost_bps=COST_BPS, freq=FREQ)['turnover'].loc[start:].sum() / (len(r_ew) / 252):.1f}x")

    # Which of the two gates does the damage?  Equal-weight everything passing ONE gate,
    # at the same 75% gross, so only the filter differs.
    sub = px[cols]
    _, above, vol20 = score(sub, vol_scale=False)
    gates = {"200d only": above.fillna(False),
             "vol20<0.60 only": (vol20 < 0.60).fillna(False),
             "both (= f=1.00)": (above & (vol20 < 0.60)).fillna(False)}
    for gname, mask in gates.items():
        k = mask.sum(axis=1).replace(0, np.nan)
        w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
        w[cols] = mask.astype(float).div(k, axis=0).mul(0.75).fillna(0.0)
        res_g = backtest(px, w, cost_bps=COST_BPS, freq=FREQ)
        rg = res_g["returns"].loc[start:]
        dg, mog = stats(rg), metrics(rg.loc[OOS_START:])
        # same book with costs switched off, to separate turnover cost from selection
        r0 = backtest(px, w, cost_bps=0, freq=FREQ)["returns"].loc[start:]
        print(f"EW {gname:16s} @75%: CAGR {dg['CAGR']:.1%} Sharpe {dg['Sharpe']:.3f} MaxDD {dg['MaxDD']:.1%} "
              f"halves {dg['H1']:.3f}/{dg['H2']:.3f} OOS {mog['CAGR']:.1%}/{mog['Sharpe']:.3f} "
              f"| 0 bps: {metrics(r0)['CAGR']:.1%}/{metrics(r0)['Sharpe']:.3f} "
              f"| avg names {mask.loc[start:].sum(axis=1).mean():.0f} "
              f"| turn {res_g['turnover'].loc[start:].sum() / (len(rg) / 252):.1f}x")

    # The sharpest test of the gate's sign: hold the COMPLEMENT (every name the filter
    # rejects) at the same gross.  If that beats the eligible book, the gate is inverted
    # on this panel rather than merely weak.
    comp = (~(above & (vol20 < 0.60)).fillna(False)) & sub.notna()
    kc = comp.sum(axis=1).replace(0, np.nan)
    wc = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    wc[cols] = comp.astype(float).div(kc, axis=0).mul(0.75).fillna(0.0)
    rc = backtest(px, wc, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
    dc, moc = stats(rc), metrics(rc.loc[OOS_START:])
    print(f"EW COMPLEMENT (rejected names) @75%: CAGR {dc['CAGR']:.1%} Sharpe {dc['Sharpe']:.3f} "
          f"MaxDD {dc['MaxDD']:.1%} halves {dc['H1']:.3f}/{dc['H2']:.3f} "
          f"OOS {moc['CAGR']:.1%}/{moc['Sharpe']:.3f} | avg names {comp.loc[start:].sum(axis=1).mean():.0f}")
    print("  ^ NOT a tradeable finding: the complement holds beaten-down small caps, and a "
          "current-constituent panel is exactly where\n    survivorship bias is largest — every "
          "name that crashed and then delisted is missing. Read it only as evidence on the\n"
          "    gate's SIGN, not as a strategy.")
    # Where does the filtered book lose to the unfiltered one?  Calendar years.
    r_f100 = series["F f=1.0 g=0.75"]
    sp = r_f100 - rc
    t = sp.mean() / sp.std() * np.sqrt(len(sp))
    print(f"eligible minus complement: {sp.mean() * 252:+.2%}/yr, t {t:+.2f} "
          f"(negative t = the gate picks the WORSE half)")
    yr = pd.DataFrame({"f=1.00": r_f100, "EWall": r_ew, "v1": base_r, "SPY": spy_r})
    yr = yr.groupby(yr.index.year).apply(lambda x: (1 + x).prod() - 1)
    print("\ncalendar-year returns (%):")
    print((yr * 100).round(1).to_string())

    # Whipsaw check: the filter's worst years vs the unfiltered book.  How invested was
    # the f=1.00 book, and how fast did the eligible set empty and refill?
    elig_all = elig.loc[start:]
    Ea = elig_all.sum(axis=1)
    w100 = weights_fn(px, cols, "F", 1.00, 0.75)
    inv = w100.loc[start:].sum(axis=1)
    print(f"\nf=1.00 invested fraction: mean {inv.mean():.1%} of book; days fully in cash "
          f"(E_t=0): {(Ea == 0).sum()} ({(Ea == 0).mean():.1%})")
    for lo, hi in [("2020-01-01", "2020-12-31"), ("2011-01-01", "2011-12-31")]:
        s_ = Ea.loc[lo:hi]
        i_ = inv.loc[lo:hi]
        print(f"  {lo[:4]}: eligible names min {s_.min()} on {s_.idxmin().date()}, "
              f"max {s_.max()}, mean {s_.mean():.0f}; invested mean {i_.mean():.1%}, "
              f"min {i_.min():.1%}; days <25% invested {(i_ < 0.25).sum()}")

    # ---- leaderboard rows -------------------------------------------------
    print("\n=== LEADERBOARD ROWS ===")
    fname = Path(__file__).name
    for lab, row in fin.iterrows():
        print(f"| 2026-09-04 | 39 {lab} | {row['CAGR']:.1%} | {row['Sharpe']:.2f} | {row['MaxDD']:.1%} | "
              f"{row['H1']:.2f} / {row['H2']:.2f} | {base['Sharpe']:.2f} ({base['H1']:.2f}/{base['H2']:.2f}) | "
              f"{row['v4a']} / {row['v4b']} | {fname} |")
    print(f"| 2026-09-04 | 39 SPY buy & hold - reference | {spy['CAGR']:.1%} | {spy['Sharpe']:.2f} | "
          f"{spy['MaxDD']:.1%} | {spy['H1']:.2f} / {spy['H2']:.2f} | "
          f"{base['Sharpe']:.2f} ({base['H1']:.2f}/{base['H2']:.2f}) | - | {fname} |")
    print(f"| 2026-09-04 | 39 RULES v1 on the small panel - reference | {base['CAGR']:.1%} | "
          f"{base['Sharpe']:.2f} | {base['MaxDD']:.1%} | {base['H1']:.2f} / {base['H2']:.2f} | "
          f"{base['Sharpe']:.2f} ({base['H1']:.2f}/{base['H2']:.2f}) | - | {fname} |")
    d = stats(r_ew)
    print(f"| 2026-09-04 | 39 EW all {len(cols)} names @75% - CONTROL (no eligibility filter) | "
          f"{d['CAGR']:.1%} | {d['Sharpe']:.2f} | {d['MaxDD']:.1%} | {d['H1']:.2f} / {d['H2']:.2f} | "
          f"{base['Sharpe']:.2f} ({base['H1']:.2f}/{base['H2']:.2f}) | - | {fname} |")


if __name__ == "__main__":
    main()
