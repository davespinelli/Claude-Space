#!/usr/bin/env python3
"""Idea 2094 (lane C, 2026-09-22) — IS THE 2083 4b PASS THE 200d-MA GATE RATHER THAN THE MADIST
RANKING?

WHERE THIS COMES FROM.  Idea 2083 (lane C, 2026-09-22) left a KEEP-4b CANDIDATE: the U56 panel,
MADIST top-40 equal-weight (rank by close/200dMA - 1), gross 1.00, MONTHLY trade, fills t+1,
10 bps.  OOS 16.24% / 1.3099 / -17.67%, i.e. a +2.56 pp margin over the 4b OOS drawdown cap of
-20.23%.  Its own memo flagged the weakness: "top-40-of-56 is a plain book, so its 4b pass may be
mostly the 200d-MA gate."  If in most months fewer than 40 U56 names pass the gate, then the
"top 40" is simply EVERY gated name and the ranking cannot be doing any work at all.

THE QUESTION.  Hold the gate, the width and every other dial FIXED and replace ONLY the ranking
statistic with orderings that carry no return information: (a) ALPHABETICAL by ticker, (b) a
SEEDED RANDOM order (both a per-rebalance redraw and a static permutation, 5 seeds each), and
(c) REVERSE MADIST (weakest trend first).  How much of the +2.56 pp drawdown margin and of the
1.3099 OOS Sharpe does the MADIST ranking actually earn?

THE TWO TUNED DIALS (and no more).
  DIAL 1 — RANKING: MADIST (incumbent) / ALPHA / REVMADIST / RAND (per-rebalance redraw) /
    RANDSTATIC (one permutation held for the whole sample).  RAND and RANDSTATIC are run at
    seeds 0..4 and EVERY seed is published; their mean is what the verdicts read.
  DIAL 2 — WIDTH k in {20, 30, 40, 50, ALL}.  k = 40 is 2083's incumbent; ALL holds every gated
    name, and is the mechanical limit at which all five rankings must coincide EXACTLY.

REPORTED, NOT TUNED: gross 1.00 (2083's rung), monthly cadence, the gate (close > 200d MA and
20d annualised vol < 0.60), the U56 panel, the GATE CENSUS (how many names actually pass each
month), the MADIST-vs-alternative holding OVERLAP, the cost {0,10,25,50} bps x signal-lag
{0,+1 day} ladder at k = 40, and a paired circular-block bootstrap of the OOS Sharpe and MaxDD
differences MADIST minus RAND-mean.  Every grid point is published in .grid.csv.

PRE-STATED VERDICT RULES (fixed before the run, not adjusted after):
  V1  THE IDEA'S OWN QUESTION — IS THE PASS THE GATE?  At k = 40, ALL THREE information-free
      rankings (ALPHA, RAND-mean, RANDSTATIC-mean) also clear 4b FULL *and* OOS.  Triggered ->
      the 2083 pass is the GATE and the width, not the MADIST ranking; the ranking is decorative.
  V2  DOES THE RANKING EARN THE DRAWDOWN MARGIN?  MADIST's OOS drawdown margin over the cap
      exceeds the ALPHA/RAND-mean margin by more than the run's own paired bootstrap SE of that
      difference.  Triggered -> the ranking buys drawdown; not triggered -> it does not.
  V3  IS THE DIRECTION EVEN RIGHT?  REVMADIST (the deliberately wrong direction) FAILS 4b at
      k = 40 while MADIST passes.  Not triggered -> the sign of the ranking does not matter
      either, which is a stronger statement than V1.
  V4  WIDTH, NOT RANKING.  The 4b pass/fail pattern across k at FIXED ranking varies MORE than
      across rankings at FIXED k (compare the count of clearing points by row vs by column).

PROTOCOL: rule 2 (10 bps, next-day fills, no shorting/leverage); rule 3 (live RULES v2 AND SPY);
rule 4 (both KEEP paths at every grid point, <= 2 tuned dials); rule 5 (one idea, deterministic,
standalone); rule 8 (walk-forward: parameters chosen on 2009-2016 ONLY, 2017-2026 read once);
rule 9 (survivorship stated).  RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py are NOT
modified.

SURVIVORSHIP (rule 9).  U56 is a CURRENT-constituent 56-name list, so every CAGR and MaxDD LEVEL
below is optimistic and both 4b bars are easier than on a point-in-time panel.  The comparison
that this idea turns on — MADIST against information-free orderings of the SAME gated names on
the SAME tape with the SAME width and cost — is same-panel and first-order immune to that bias;
the absolute 4b pass counts are not.

Run:  python research/backtests/2026-09-22_gate-vs-ranking_C.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, score               # noqa: E402
from engine import backtest as engine_backtest, metrics                   # noqa: E402

DATE, SLUG = "2026-09-22", "gate-vs-ranking"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

RANKINGS = ["MADIST", "ALPHA", "REVMADIST", "RAND", "RANDSTATIC"]     # tuned dial 1
SEEDS = [0, 1, 2, 3, 4]                                               # published, not tuned
WIDTHS = [20, 30, 40, 50, "ALL"]                                      # tuned dial 2
GROSS = 1.00                                                          # 2083's rung, fixed
COST, MAX_VOL, WARMUP = 10.0, 0.60, 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST_LADDER = [0.0, 10.0, 25.0, 50.0]
LAGS = [0, 1]
NBOOT, BLOCK = 2000, 21

_log: list[str] = []
_gates: list[dict] = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _log.append(s)


def gate(name, value, target, ok):
    _gates.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    log(f"  GATE {'PASS' if ok else 'FAIL'}  {name}: {value}   (target {target})")
    return bool(ok)


def month_end(idx):
    s = pd.Series(idx.to_period("M"), index=idx)
    return idx[(s != s.shift(-1)).values]


def maxdd(r):
    e = (1 + r).cumprod()
    return float((e / e.cummax() - 1).min())


# ---------------------------------------------------------------- the books
def build_signals(px, cols):
    """2083's gate verbatim, plus the ranking statistics that sit inside it."""
    p = px[cols]
    _, above, vol20 = score(p, vol_scale=False)
    elig = above & (vol20 < MAX_VOL) & p.notna()
    madist = p / p.rolling(200).mean() - 1.0
    return elig & madist.notna(), madist


def rank_frame(kind, madist, cols, index, seed=0):
    """A DataFrame of ranking scores (higher = preferred), same shape as madist."""
    if kind == "MADIST":
        return madist
    if kind == "REVMADIST":
        return -madist
    if kind == "ALPHA":
        # alphabetical by ticker: first alphabetically = highest score.  Constant in time.
        order = {c: -i for i, c in enumerate(sorted(cols))}
        return pd.DataFrame({c: float(order[c]) for c in cols}, index=index)
    if kind == "RANDSTATIC":
        rng = np.random.default_rng(1000 + seed)
        perm = rng.permutation(len(cols)).astype(float)
        return pd.DataFrame({c: perm[i] for i, c in enumerate(cols)}, index=index)
    if kind == "RAND":
        rng = np.random.default_rng(2000 + seed)
        return pd.DataFrame(rng.random((len(index), len(cols))), index=index, columns=cols)
    raise ValueError(kind)


def book_weights(rk, elig, rebal, k, gross, index, cols, lag=0):
    """Monthly top-k of the gated names at gross/k each; gated-out NAV stays in CASH.
    lag = extra trading days of SIGNAL STALENESS (the engine always fills at t+1)."""
    if lag:
        rk, elig = rk.shift(lag), elig.shift(lag).fillna(False)
    e = rk.where(elig)
    if k == "ALL":
        n = elig.sum(axis=1).replace(0, np.nan)
        W = elig.astype(float).div(n, axis=0).fillna(0.0) * gross
        return W.reindex(rebal).reindex(index).ffill().fillna(0.0)
    W = pd.DataFrame(0.0, index=rebal, columns=cols)
    er = e.reindex(rebal)
    for d in rebal:
        row = er.loc[d].dropna()
        if len(row):
            W.loc[d, row.sort_values(ascending=False).index[:k]] = gross / k
    return W.reindex(index).ffill().fillna(0.0)


def holdings_at(rk, elig, rebal, k, cols):
    """The held name-set at each rebalance date (for the overlap census)."""
    e = rk.where(elig).reindex(rebal)
    out = {}
    for d in rebal:
        row = e.loc[d].dropna()
        out[d] = set(row.index) if k == "ALL" else set(row.sort_values(ascending=False).index[:k])
    return out


# ---------------------------------------------------------------- bootstrap
def block_boot_diff(ra, rb, nboot=NBOOT, block=BLOCK, seed=7):
    """Paired circular-block bootstrap of (Sharpe_a - Sharpe_b) and (MaxDD_a - MaxDD_b).
    The SAME resampled day-blocks are applied to both series, so the market path is shared."""
    a, b = ra.align(rb, join="inner")
    a, b = a.values, b.values
    n = len(a)
    nb = int(np.ceil(n / block))
    rng = np.random.default_rng(seed)
    ds, dd = np.empty(nboot), np.empty(nboot)
    idx_base = (np.arange(block)[None, :])
    for i in range(nboot):
        starts = rng.integers(0, n, nb)
        idx = ((starts[:, None] + idx_base) % n).ravel()[:n]
        xa, xb = a[idx], b[idx]
        sa = xa.mean() / xa.std() * np.sqrt(252) if xa.std() > 0 else np.nan
        sb = xb.mean() / xb.std() * np.sqrt(252) if xb.std() > 0 else np.nan
        ds[i] = sa - sb
        dd[i] = maxdd(pd.Series(xa)) - maxdd(pd.Series(xb))
    return ds, dd


# ---------------------------------------------------------------- run
def main():
    log(f"# Idea 2094 (lane C, {DATE}) — is the 2083 4b pass the 200d-MA GATE rather than the "
        f"MADIST RANKING?")
    log(f"# tuned dials (2): RANKING {RANKINGS} x WIDTH k {WIDTHS}.  fixed at 2083's values: "
        f"U56 panel, gross {GROSS:.2f}, MONTHLY, fills t+1, {COST:.0f} bps, gate close>200dMA & "
        f"vol20<{MAX_VOL}.  seeds {SEEDS} for the two random rankings, all published.")

    px = load_universe().dropna(how="all").ffill()
    cols = list(px.columns)
    st = px.index[WARMUP]
    spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
    rebal = month_end(px.index)
    log(f"\n## U56: {len(cols)} names, {len(px)} rows ({len(px)/252:.1f}y), book from {st.date()}")

    elig, madist = build_signals(px, cols)

    # ---- SPY and live-rules reference legs -------------------------------------------------
    h = len(spy) // 2
    s_full, s_oos = metrics(spy), metrics(spy.loc[OOS_START:])
    s_h1, s_h2 = metrics(spy.iloc[:h])["Sharpe"], metrics(spy.iloc[h:])["Sharpe"]
    log(f"   SPY FULL {s_full['CAGR']:.2%}/{s_full['Sharpe']:.4f}/{s_full['MaxDD']:.2%} "
        f"(H1 {s_h1:.4f} H2 {s_h2:.4f});  SPY OOS {s_oos['CAGR']:.2%}/{s_oos['Sharpe']:.4f}/"
        f"{s_oos['MaxDD']:.2%}")
    log(f"   4b bars — FULL: DD >= {DD_CAP*s_full['MaxDD']:.2%}, CAGR >= "
        f"{CAGR_FLOOR*s_full['CAGR']:.2%};  OOS: DD >= {DD_CAP*s_oos['MaxDD']:.2%}, CAGR >= "
        f"{CAGR_FLOOR*s_oos['CAGR']:.2%}")

    lw = rules_v2_weights(px[cols], 0.03, 0.75).reindex(columns=px.columns).fillna(0.0)
    lr = engine_backtest(px, lw, cost_bps=COST, freq="W")["returns"].loc[st:]
    lh = len(lr) // 2
    live = dict(S=metrics(lr)["Sharpe"], H1=metrics(lr.iloc[:lh])["Sharpe"],
                H2=metrics(lr.iloc[lh:])["Sharpe"], DD=metrics(lr)["MaxDD"],
                oosS=metrics(lr.loc[OOS_START:])["Sharpe"])
    log(f"   live RULES v2 FULL S={live['S']:.4f} (H1 {live['H1']:.4f} H2 {live['H2']:.4f}) "
        f"DD {live['DD']:.2%}, OOS S={live['oosS']:.4f}")

    # ---- GATE CENSUS: the whole point ------------------------------------------------------
    n_elig = elig.reindex(rebal).sum(axis=1).loc[st:]
    cen = n_elig.describe()
    frac_lt40 = float((n_elig < 40).mean())
    log(f"\n## GATE CENSUS at the {len(n_elig)} month-end decision closes:  gated names "
        f"mean {cen['mean']:.1f}, median {cen['50%']:.0f}, min {cen['min']:.0f}, "
        f"max {cen['max']:.0f} of {len(cols)}")
    for kk in (20, 30, 40, 50):
        log(f"   months with FEWER than {kk} gated names: {float((n_elig<kk).mean()):.1%}   "
            f"(-> top-{kk} degenerates to 'hold every gated name')")
    n_elig.rename("n_gated").to_frame().to_csv(f"{OUT}.gatecensus.csv")

    # ---- price the grid --------------------------------------------------------------------
    def eval_returns(r):
        m, mo = metrics(r), metrics(r.loc[OOS_START:])
        hh = len(r) // 2
        h1, h2 = metrics(r.iloc[:hh])["Sharpe"], metrics(r.iloc[hh:])["Sharpe"]
        k4b_full = bool(h1 > s_h1 and h2 > s_h2 and m["MaxDD"] >= DD_CAP * s_full["MaxDD"]
                        and m["CAGR"] >= CAGR_FLOOR * s_full["CAGR"])
        k4b_oos = bool(mo["Sharpe"] > s_oos["Sharpe"] and mo["MaxDD"] >= DD_CAP * s_oos["MaxDD"]
                       and mo["CAGR"] >= CAGR_FLOOR * s_oos["CAGR"])
        k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["DD"])
        r_is = r.loc[:IS_END]
        return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                    is_CAGR=metrics(r_is)["CAGR"], is_Sharpe=metrics(r_is)["Sharpe"],
                    is_MaxDD=metrics(r_is)["MaxDD"],
                    oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                    dd_margin_pp_full=100.0 * (m["MaxDD"] - DD_CAP * s_full["MaxDD"]),
                    dd_margin_pp_oos=100.0 * (mo["MaxDD"] - DD_CAP * s_oos["MaxDD"]),
                    keep4b_full=k4b_full, keep4b_oos=k4b_oos,
                    keep4b=(k4b_full and k4b_oos), keep4a=k4a)

    rows, rets, overlap_rows = [], {}, []
    mad_hold = {k: holdings_at(madist, elig, rebal, k, cols) for k in WIDTHS}
    for kind in RANKINGS:
        seeds = SEEDS if kind in ("RAND", "RANDSTATIC") else [0]
        for sd in seeds:
            rk = rank_frame(kind, madist, cols, px.index, sd)
            for k in WIDTHS:
                W = book_weights(rk, elig, rebal, k, GROSS, px.index, cols)
                W = W.reindex(columns=px.columns).fillna(0.0)
                res = engine_backtest(px, W, cost_bps=COST, freq="M")
                r = res["returns"].loc[st:]
                rets[(kind, sd, k)] = r
                d = eval_returns(r)
                d.update(ranking=kind, seed=sd, k=str(k), gross=GROSS,
                         turnover_yr=float(res["turnover"].loc[st:].sum() / (len(r) / 252)),
                         gross_max=float(res["weights"].sum(axis=1).max()))
                rows.append(d)
                # overlap with the MADIST book of the same width
                hh = holdings_at(rk, elig, rebal, k, cols)
                jac = [len(hh[d0] & mad_hold[k][d0]) / max(1, len(hh[d0] | mad_hold[k][d0]))
                       for d0 in rebal if d0 >= st]
                overlap_rows.append(dict(ranking=kind, seed=sd, k=str(k),
                                         mean_jaccard_vs_MADIST=float(np.mean(jac))))
    grid = pd.DataFrame(rows)
    grid.to_csv(f"{OUT}.grid.csv", index=False)
    pd.DataFrame(overlap_rows).to_csv(f"{OUT}.overlap.csv", index=False)

    log(f"\n## FULL GRID ({len(grid)} points, all published to {OUT.name}.grid.csv) — "
        f"gross {GROSS:.2f}, monthly, {COST:.0f} bps")
    log("   ranking      seed  k     FULL CAGR/Sharpe/MaxDD     H1/H2        "
        "OOS CAGR/Sharpe/MaxDD      ddOOSmargin  4a  4bFULL 4bOOS")
    for _, x in grid.iterrows():
        log(f"   {x['ranking']:<11} {x['seed']:>4}  {x['k']:<4} "
            f"{x['CAGR']:>7.2%}/{x['Sharpe']:.4f}/{x['MaxDD']:>7.2%}  "
            f"{x['H1']:.4f}/{x['H2']:.4f}  "
            f"{x['oos_CAGR']:>7.2%}/{x['oos_Sharpe']:.4f}/{x['oos_MaxDD']:>7.2%}  "
            f"{x['dd_margin_pp_oos']:>+7.2f} pp   "
            f"{'Y' if x['keep4a'] else '.'}   {'Y' if x['keep4b_full'] else '.'}      "
            f"{'Y' if x['keep4b_oos'] else '.'}")

    ov = pd.DataFrame(overlap_rows)
    log(f"\n## HOLDING OVERLAP with the MADIST book of the same width (mean Jaccard over "
        f"{len([d for d in rebal if d>=st])} month-ends)")
    for k in WIDTHS:
        line = "   k=" + str(k).ljust(4)
        for kind in RANKINGS:
            v = ov[(ov["ranking"] == kind) & (ov["k"] == str(k))]["mean_jaccard_vs_MADIST"].mean()
            line += f"  {kind} {v:.3f}"
        log(line)

    # ---- the headline contrast at k=40 -----------------------------------------------------
    def agg(kind, k):
        s = grid[(grid["ranking"] == kind) & (grid["k"] == str(k))]
        return s.mean(numeric_only=True), s

    log(f"\n## THE CONTRAST AT 2083's WIDTH (k = 40), information-free rankings vs MADIST")
    inf_free = ["ALPHA", "RAND", "RANDSTATIC"]
    v1_parts = []
    for kind in RANKINGS:
        m, s = agg(kind, 40)
        n_pass = int((s["keep4b"]).sum())
        log(f"   {kind:<11} OOS {m['oos_CAGR']:.2%}/{m['oos_Sharpe']:.4f}/{m['oos_MaxDD']:.2%}  "
            f"ddOOSmargin {m['dd_margin_pp_oos']:+.2f} pp   4b FULL+OOS on {n_pass}/{len(s)} "
            f"seed(s)   turnover {m['turnover_yr']:.2f}x/yr")
        if kind in inf_free:
            v1_parts.append((kind, n_pass == len(s), m))
    mad40, _ = agg("MADIST", 40)
    rev40, rev40s = agg("REVMADIST", 40)

    # replication check against 2083's published numbers
    r_m40 = rets[("MADIST", 0, 40)]
    m_m40 = metrics(r_m40.loc[OOS_START:])
    gate("G1 replicates 2083's published MADIST-40 OOS Sharpe 1.3099 to 2dp",
         f"{m_m40['Sharpe']:.4f}", "|d| < 0.005", abs(m_m40["Sharpe"] - 1.3099) < 0.005)
    gate("G2 replicates 2083's published MADIST-40 OOS MaxDD -17.67%",
         f"{m_m40['MaxDD']:.2%}", "|d| < 0.2 pp", abs(m_m40["MaxDD"] + 0.1767) < 0.002)
    gate("G3 no leverage anywhere in the grid", f"max gross {grid['gross_max'].max():.4f}",
         "<= 1.0001", grid["gross_max"].max() <= 1.0001)
    gate("G4 k=ALL collapses every ranking to ONE book (mechanical identity)",
         f"{grid[grid['k']=='ALL']['oos_Sharpe'].std():.2e} sd of OOS Sharpe",
         "< 1e-12", float(grid[grid["k"] == "ALL"]["oos_Sharpe"].std()) < 1e-12)

    # ---- paired bootstrap: MADIST-40 vs the RAND-40 seeds ----------------------------------
    log(f"\n## PAIRED CIRCULAR-BLOCK BOOTSTRAP ({NBOOT} draws, {BLOCK}-day blocks, shared "
        f"day-blocks) — OOS window only")
    boot_rows = []
    for kind in ["ALPHA", "RAND", "RANDSTATIC", "REVMADIST"]:
        seeds = SEEDS if kind in ("RAND", "RANDSTATIC") else [0]
        for sd in seeds:
            ds, dd = block_boot_diff(r_m40.loc[OOS_START:], rets[(kind, sd, 40)].loc[OOS_START:])
            boot_rows.append(dict(vs=kind, seed=sd, dSharpe=float(np.mean(ds)),
                                  dSharpe_se=float(np.std(ds)),
                                  dSharpe_lo=float(np.percentile(ds, 2.5)),
                                  dSharpe_hi=float(np.percentile(ds, 97.5)),
                                  dMaxDD_pp=100.0 * float(np.mean(dd)),
                                  dMaxDD_se_pp=100.0 * float(np.std(dd)),
                                  dMaxDD_lo_pp=100.0 * float(np.percentile(dd, 2.5)),
                                  dMaxDD_hi_pp=100.0 * float(np.percentile(dd, 97.5))))
    boot = pd.DataFrame(boot_rows)
    boot.to_csv(f"{OUT}.bootstrap.csv", index=False)
    for _, x in boot.iterrows():
        log(f"   MADIST-40 minus {x['vs']:<11} seed {int(x['seed'])}:  dSharpe "
            f"{x['dSharpe']:+.4f} (SE {x['dSharpe_se']:.4f}, 95% [{x['dSharpe_lo']:+.4f}, "
            f"{x['dSharpe_hi']:+.4f}])   dMaxDD {x['dMaxDD_pp']:+.2f} pp (SE "
            f"{x['dMaxDD_se_pp']:.2f}, 95% [{x['dMaxDD_lo_pp']:+.2f}, {x['dMaxDD_hi_pp']:+.2f}])")

    # ---- rule 8 walk-forward ---------------------------------------------------------------
    log(f"\n## RULE 8 WALK-FORWARD — the (ranking, k) pair chosen on 2009-{IS_END[:4]} ONLY by "
        f"IS SHARPE, then {OOS_START[:4]}-2026 read ONCE")
    wf_rows = []
    # the chooser sees only IS statistics; random rankings enter as the MEAN over their seeds,
    # which is what a deployment that must fix a seed in advance can honestly expect.
    for kind in RANKINGS:
        seeds = SEEDS if kind in ("RAND", "RANDSTATIC") else [0]
        for k in WIDTHS:
            sub = grid[(grid["ranking"] == kind) & (grid["k"] == str(k))]
            wf_rows.append(dict(ranking=kind, k=str(k), n_seeds=len(seeds),
                                is_Sharpe=float(sub["is_Sharpe"].mean()),
                                is_CAGR=float(sub["is_CAGR"].mean()),
                                is_MaxDD=float(sub["is_MaxDD"].mean()),
                                oos_Sharpe=float(sub["oos_Sharpe"].mean()),
                                oos_CAGR=float(sub["oos_CAGR"].mean()),
                                oos_MaxDD=float(sub["oos_MaxDD"].mean()),
                                oos_dd_margin_pp=float(sub["dd_margin_pp_oos"].mean()),
                                keep4b_oos=bool(sub["keep4b_oos"].all()),
                                keep4b=bool(sub["keep4b"].all())))
    wf = pd.DataFrame(wf_rows).sort_values("is_Sharpe", ascending=False)
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    log("   IS-Sharpe-ranked ladder (IS = 2009-2016, OOS = 2017-2026 read once):")
    for _, x in wf.iterrows():
        log(f"   {x['ranking']:<11} k={x['k']:<4} IS {x['is_CAGR']:>7.2%}/{x['is_Sharpe']:.4f}/"
            f"{x['is_MaxDD']:>7.2%}   ->   OOS {x['oos_CAGR']:>7.2%}/{x['oos_Sharpe']:.4f}/"
            f"{x['oos_MaxDD']:>7.2%}  ddmargin {x['oos_dd_margin_pp']:>+6.2f} pp  "
            f"4bOOS {'Y' if x['keep4b_oos'] else '.'}")
    pick = wf.iloc[0]
    log(f"   IS-ONLY PICK = {pick['ranking']} k={pick['k']}  ->  OOS {pick['oos_CAGR']:.2%}/"
        f"{pick['oos_Sharpe']:.4f}/{pick['oos_MaxDD']:.2%}, ddmargin "
        f"{pick['oos_dd_margin_pp']:+.2f} pp, 4b OOS "
        f"{'PASS' if pick['keep4b_oos'] else 'FAIL'}")
    log(f"   (SPY OOS {s_oos['CAGR']:.2%}/{s_oos['Sharpe']:.4f}/{s_oos['MaxDD']:.2%};  live "
        f"RULES v2 OOS Sharpe {live['oosS']:.4f})")
    log(f"   MADIST k=40 sits at IS-Sharpe rank "
        f"{1 + int(np.flatnonzero((wf['ranking']=='MADIST') & (wf['k']=='40'))[0])} of {len(wf)}")

    # ---- cost x lag ladder at k=40 ---------------------------------------------------------
    log(f"\n## COST x SIGNAL-LAG LADDER at k = 40 (every ranking; random rankings at seed 0)")
    lad = []
    for kind in RANKINGS:
        rk = rank_frame(kind, madist, cols, px.index, 0)
        for lg in LAGS:
            W = book_weights(rk, elig, rebal, 40, GROSS, px.index, cols, lag=lg)
            W = W.reindex(columns=px.columns).fillna(0.0)
            for cb in COST_LADDER:
                r = engine_backtest(px, W, cost_bps=cb, freq="M")["returns"].loc[st:]
                d = eval_returns(r)
                d.update(ranking=kind, lag=lg, cost_bps=cb)
                lad.append(d)
    ladder = pd.DataFrame(lad)
    ladder.to_csv(f"{OUT}.ladder.csv", index=False)
    for kind in RANKINGS:
        s = ladder[ladder["ranking"] == kind]
        log(f"   {kind:<11} 4b FULL+OOS at {int(s['keep4b'].sum())}/{len(s)} cost x lag cells;  "
            f"OOS Sharpe {s['oos_Sharpe'].min():.4f}..{s['oos_Sharpe'].max():.4f};  OOS ddmargin "
            f"{s['dd_margin_pp_oos'].min():+.2f}..{s['dd_margin_pp_oos'].max():+.2f} pp")

    # ---- verdicts --------------------------------------------------------------------------
    log("\n## PRE-STATED VERDICTS")
    v1 = all(p[1] for p in v1_parts)
    log(f"   V1 (the pass is the GATE): ALPHA/RAND/RANDSTATIC all clear 4b FULL+OOS at k=40 at "
        f"EVERY seed?  " + ", ".join(f"{p[0]} {'Y' if p[1] else 'N'}" for p in v1_parts) +
        f"  ->  {'TRIGGERED' if v1 else 'not triggered'}")
    rand_marg = grid[(grid["ranking"].isin(["ALPHA", "RAND", "RANDSTATIC"])) &
                     (grid["k"] == "40")]["dd_margin_pp_oos"].mean()
    dd_se = boot[boot["vs"].isin(["ALPHA", "RAND", "RANDSTATIC"])]["dMaxDD_se_pp"].mean()
    dd_diff = mad40["dd_margin_pp_oos"] - rand_marg
    v2 = bool(dd_diff > dd_se)
    log(f"   V2 (the RANKING earns the DD margin): MADIST ddmargin "
        f"{mad40['dd_margin_pp_oos']:+.2f} pp vs info-free mean {rand_marg:+.2f} pp -> diff "
        f"{dd_diff:+.2f} pp against a bootstrap SE of {dd_se:.2f} pp  ->  "
        f"{'TRIGGERED' if v2 else 'not triggered'}")
    v3 = bool(not rev40s["keep4b"].all() and grid[(grid['ranking']=='MADIST') &
                                                  (grid['k']=='40')]["keep4b"].all())
    log(f"   V3 (the DIRECTION matters): REVMADIST k=40 4b FULL+OOS "
        f"{'FAIL' if not rev40s['keep4b'].all() else 'PASS'} while MADIST k=40 "
        f"{'PASS' if grid[(grid['ranking']=='MADIST') & (grid['k']=='40')]['keep4b'].all() else 'FAIL'}"
        f"  ->  {'TRIGGERED' if v3 else 'not triggered'}")
    by_k = grid.groupby("k")["keep4b"].mean()
    by_rank = grid.groupby("ranking")["keep4b"].mean()
    v4 = bool(by_k.std() > by_rank.std())
    log(f"   V4 (WIDTH moves the verdict more than RANKING): 4b-pass rate sd across k "
        f"{by_k.std():.4f} vs across ranking {by_rank.std():.4f}  ->  "
        f"{'TRIGGERED' if v4 else 'not triggered'}")
    log(f"       pass rate by k:       " + "  ".join(f"{i}={v:.2f}" for i, v in by_k.items()))
    log(f"       pass rate by ranking: " + "  ".join(f"{i}={v:.2f}" for i, v in by_rank.items()))

    verdict = ("ANSWERED / THE PASS IS THE GATE" if v1 and not v2 else
               "ANSWERED / THE RANKING EARNS IT" if v2 and v3 else
               "ANSWERED / MIXED")
    log(f"\n## VERDICT: {verdict}")

    pd.DataFrame(_gates).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")
    log(f"\nwrote {OUT.name}.grid.csv / .walkforward.csv / .ladder.csv / .bootstrap.csv / "
        f".overlap.csv / .gatecensus.csv / .gates.csv / .log.txt")
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")


if __name__ == "__main__":
    main()
