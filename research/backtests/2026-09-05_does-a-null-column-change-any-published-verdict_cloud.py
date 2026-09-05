#!/usr/bin/env python3
"""QUEUE idea 181 — does-a-null-column-change-any-published-verdict  (cloud, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 181)
    "idea 158 showed the size of a tilt's Sharpe effect, its 4b pass count and rule 8's own pick
     are all reachable by a key with zero information, and proposed a null-key column as a
     PROTOCOL reporting clause.  Before PROTOCOL takes it, price it: sweep the leaderboard for
     entries whose conclusion rests on a tilt's realised magnitude, re-run each against a matched
     null key, and report how many verdicts move.  If it is near zero the clause is bookkeeping;
     if it is not, name the entries."

WHAT "THE CLAUSE" IS, WRITTEN DOWN BEFORE IT IS PRICED
    The proposed PROTOCOL clause: a claim that rests on the REALISED MAGNITUDE of a keyed tilt
    (a "the tilt moved Sharpe by X, so the key does something" claim) may only be reported if
    that magnitude exceeds what a MATCHED ZERO-INFORMATION key achieves in the same cell.
    Operationally, with B null draws per cell, the clause is
        |dSharpe(real key)|  >  max over the B null draws of |dSharpe(null key)|
    which is the one-sided 1/(B+1) threshold — 1/21 = 4.8% with the B = 20 used here.
    Pricing the clause means answering three separate questions, and this run reports all three
    because they can disagree:
        Q1  MAGNITUDE   how often does a real key's tilt magnitude clear its own null band?
        Q2  VERDICT     how often does swapping the real key for a null key change the KEEP/KILL
                        verdict (4a, 4b full sample, 4b on the OOS window)?
        Q3  SELECTION   does rule 8's pick change, and does the OOS result change, when the
                        selector is required to respect the clause?
    Q1 is what idea 158 measured.  Q2 is what idea 181 actually asks and what decides whether
    the clause is bookkeeping.  A clause can be right on Q1 and still worthless on Q2.

CORPUS — 453 books, every one reported
    3 panels     u56 (research/universe.json), broad (universe_broad.json, 136 large caps),
                 small (sub-$2B panel; tickers with max_1d_move >= 1.0 in data/small_meta.csv
                 DROPPED first)
    5 real keys  VOL   20-day annualised vol        (the live /sqrt(vol20) scaler's key)
                 MOM   12-1 momentum
                 R6    6-month return
                 R3    3-month return
                 PRICE share price level            (idea 158's "does share price any key")
    20 null keys NULL00..NULL19 — the 126-day change of a per-ticker seeded random walk, i.e.
                 R6's exact functional form applied to noise, calibrated to each panel's median
                 daily vol.  Zero information by construction; the realised rank IC of each draw
                 is measured and printed, not assumed.
    2 directions POS (tilt toward a high key) / NEG (tilt away from it)
    3 tilt strengths m in {0.20, 0.50, 1.00}
    2 cost rungs 10 bps (PROTOCOL) and 25 bps, derived EXACTLY from the 0 bps run and the
                 engine's own turnover series (port_c = port_0 - turnover * c / 1e4).
    plus 1 untilted CONTROL per panel (m = 0), which is the reference every dSharpe is taken
    against.  3 x (25 keys x 2 dir x 3 m + 1) = 453 engine runs -> 906 rows with the cost axis.

TUNED PARAMETERS — exactly two: the tilt strength m and the direction.  Keys, panels, cost
    rungs and the OOS window are reported axes and are never selected on.  Every grid point is
    written to .grid.csv.

BOOK — one convention, matching idea 173's anchor and the 2026-09-04 4b KEEP's construction
    s = comp + dir * m * key,  both terms cross-sectional pct-ranks in [0,1]
    comp = RULES v1's composite (mean pct-rank of 12-1 mom, 6m, 3m)
    eligible = (close > 200d MA) & (vol20 < 0.60);  hold top 20 by s, equal weight,
    w = 0.75/20 each, weekly, cash for unfilled slots, t+1 execution (PROTOCOL 2).

WALK-FORWARD (PROTOCOL rule 8)
    IS = sample start..2016-12-31, OOS = 2017-01-01..end, read ONCE.  Three selectors, all
    reading IS only, all evaluated on the identical OOS window:
        S0  do-nothing — hold the untilted control (the honest baseline every previous
            selector study, ideas 110/132/151/166/171/174, found hard to beat)
        S1  IS-Sharpe argmax over all 150 tilted arms (the incumbent, no null column)
        S2  IS-Sharpe argmax over arms that CLEAR THE CLAUSE on the IS window (the real key's
            IS |dSharpe| exceeds all 20 matched null draws'); falls back to the control if none
    Both KEEP paths are evaluated on every arm and every pick, on the full sample and again on
    the OOS window alone:
        4a  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1
        4b  Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's

LEADERBOARD CENSUS — the "sweep the leaderboard" half of the idea
    Every LEADERBOARD row is classified by whether its verdict text rests on the realised
    magnitude of a keyed tilt (a quoted dSharpe / "moves Sharpe by" / scaler / tilt / key claim
    with a number attached).  Counts are reported, the matching rows are written to .census.csv
    with their verdicts, and the ones whose cell is inside this run's grid are named.  The
    census classifies text; it does not re-run rows whose construction is not reconstructible
    from this grid, and says so.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  Q1: fewer than half the real-key arms clear their own null band.  Idea 158 found a null
        key moving Sharpe as much as a real one on u56, so most magnitudes should be indistinct.
    P2  Q2: the clause moves FEWER verdicts than magnitudes — under 15% of arms change 4b status
        when the real key is swapped for the median null draw — because the 4b bars are
        dominated by the base book and the panel, not by the tilt.
    P3  VOL/NEG (the live scaler's own direction) does NOT clear the clause at any m on either
        large-cap panel — the ninth independent delete-the-scaler reading.
    P4  Q3: S2 does not beat S0.  A seventh instance of "no selector beats doing nothing".
    P5  At least one null draw clears 4b somewhere, i.e. the 4b pass count is partly a property
        of the bar rather than of the key (idea 158 found RAND holding 11 of 54 passes).

CAVEATS carried, not buried
    * SURVIVORSHIP.  All three panels are CURRENT constituents (idea 54); the small panel is
      today's sub-$2B screen with delisted and acquired names absent entirely.  Every CAGR here
      is optimistic and no level in this file is an achievable return.
    * B = 20 null draws gives a 1/21 one-sided threshold and a coarse band.  Idea 180 is the
      one asking for 100 draws and a full distribution; this run prices the CLAUSE, and a
      coarser band makes the clause EASIER to clear, which works against P1 and P3.
    * WINDOW COMPOSITION (idea 111): the IS window is the calmer regime, and the small panel's
      IS window is only 2011-2016.
    * The null keys are noise with R6's functional form; they are not a model of a plausible
      alternative signal, and "a real key beats noise" is a weaker claim than "a real key beats
      a rival real key".
    * Every row is t+1 execution at 10 or 25 bps.
    * The `kind` column labels the null arms "nullkey", not "null", because pandas reads the
      bare string "null" back as NaN and would silently empty every null-arm filter.

Deterministic (seed 181), standalone, no network.
Writes .grid.csv (906), .clause.csv, .verdicts.csv, .walkforward.csv, .census.csv,
.result.md and .console.txt.
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_does-a-null-column-change-any-published-verdict_cloud"
OUT = ROOT / "research" / "backtests"
SEED = 181
B_NULL = 20
IS_END = pd.Timestamp("2016-12-31")
N, GROSS, FREQ, MAXVOL = 20, 0.75, "W", 0.60
MS = [0.20, 0.50, 1.00]
DIRS = {"POS": 1.0, "NEG": -1.0}
REAL_KEYS = ["VOL", "MOM", "R6", "R3", "PRICE"]

_console: list[str] = []


def say(*a):
    line = " ".join(str(x) for x in a)
    print(line)
    _console.append(line)


def spearman(a, b):
    ra, rb = pd.Series(a).rank(), pd.Series(b).rank()
    if ra.std(ddof=0) == 0 or rb.std(ddof=0) == 0:
        return np.nan
    return float(np.corrcoef(ra.values, rb.values)[0, 1])


# ----------------------------------------------------------------------------- panels
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    say(f"small panel: dropped {len(bad)} tickers with max_1d_move >= 1.0; "
        f"{len(keep) - 1} names + SPY benchmark remain")
    return px[keep]


# ----------------------------------------------------------------------------- keys
def rankpct(df):
    return df.rank(axis=1, pct=True)


def build_keys(px, rng):
    """5 real keys + B_NULL matched null keys, all as cross-sectional pct ranks."""
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    keys = {
        "VOL": rankpct(vol20),
        "MOM": rankpct(px.shift(21) / px.shift(252) - 1),
        "R6": rankpct(px / px.shift(126) - 1),
        "R3": rankpct(px / px.shift(63) - 1),
        "PRICE": rankpct(px),
    }
    sd = float(np.nanmedian(px.pct_change().std().values))
    for j in range(B_NULL):
        steps = rng.normal(0.0, sd, size=px.shape)
        walk = pd.DataFrame(np.cumsum(steps, axis=0), index=px.index, columns=px.columns) + 10.0
        keys[f"NULL{j:02d}"] = rankpct(walk / walk.shift(126) - 1)   # R6's functional form
    return keys, vol20


def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (rankpct(mom) + rankpct(r6) + rankpct(r3)) / 3


def rank_ic(key, px, horizon=21):
    """Realised cross-sectional rank IC of a key against forward returns (sampled monthly)."""
    fwd = px.shift(-horizon) / px - 1
    idx = px.index[260::horizon]
    vals = []
    for d in idx:
        a, b = key.loc[d], fwd.loc[d]
        ok = a.notna() & b.notna()
        if ok.sum() > 10:
            vals.append(spearman(a[ok].values, b[ok].values))
    v = np.array([x for x in vals if np.isfinite(x)])
    if len(v) < 2:
        return np.nan, np.nan
    return float(v.mean()), float(v.mean() / (v.std(ddof=1) / np.sqrt(len(v))))


# ----------------------------------------------------------------------------- metrics
def win(r, lo=None, hi=None):
    if lo is not None:
        r = r.loc[lo:]
    if hi is not None:
        r = r.loc[:hi]
    return r


def full_row(r):
    h = len(r) // 2
    out = {}
    for tag, x in (("F", r), ("H1", r.iloc[:h]), ("H2", r.iloc[h:]),
                   ("IS", win(r, hi=IS_END)), ("OOS", win(r, lo=IS_END + pd.Timedelta(days=1)))):
        m = metrics(x)
        out[f"CAGR_{tag}"], out[f"Sharpe_{tag}"], out[f"MaxDD_{tag}"] = m["CAGR"], m["Sharpe"], m["MaxDD"]
    o = win(r, lo=IS_END + pd.Timedelta(days=1))
    ho = len(o) // 2
    out["oosH1"] = metrics(o.iloc[:ho])["Sharpe"]
    out["oosH2"] = metrics(o.iloc[ho:])["Sharpe"]
    return out


def pass4a(row, base):
    return bool(row["Sharpe_H1"] > base["Sharpe_H1"] and row["Sharpe_H2"] > base["Sharpe_H2"]
                and row["MaxDD_F"] >= base["MaxDD_F"])


def pass4b(row, spy):
    return bool(row["Sharpe_H1"] > spy["Sharpe_H1"] and row["Sharpe_H2"] > spy["Sharpe_H2"]
                and row["Sharpe_OOS"] > spy["Sharpe_OOS"]
                and row["MaxDD_F"] >= 0.60 * spy["MaxDD_F"]
                and row["CAGR_F"] >= 0.70 * spy["CAGR_F"])


def pass4b_oos(row, spy):
    return bool(row["oosH1"] > spy["oosH1"] and row["oosH2"] > spy["oosH2"]
                and row["Sharpe_OOS"] > spy["Sharpe_OOS"]
                and row["MaxDD_OOS"] >= 0.60 * spy["MaxDD_OOS"]
                and row["CAGR_OOS"] >= 0.70 * spy["CAGR_OOS"])


# ----------------------------------------------------------------------------- run
def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    panels = {"u56": load_universe(), "broad": load_universe(broad=True), "small": small_panel()}
    COSTS = [10.0, 25.0]

    rows, ics = [], []
    ref = {}
    for pn, px in panels.items():
        start = px.index[260]
        pseed = SEED + 1000 * (1 + list(panels).index(pn))   # fixed, not hash()-dependent
        keys, vol20 = build_keys(px, np.random.default_rng(pseed))
        comp = composite(px)
        above = px > px.rolling(200).mean()
        elig_mask = above & (vol20 < MAXVOL)
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        srow = full_row(spy)
        b0 = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq="W")
        ref[pn] = dict(start=start, spy=srow, b_ret=b0["returns"].loc[start:],
                       b_trn=b0["turnover"].loc[start:])
        say(f"panel {pn}: {px.shape[1]} cols, sample {start.date()}..{px.index[-1].date()}, "
            f"SPY {srow['CAGR_F']:.2%}/{srow['Sharpe_F']:.3f}/{srow['MaxDD_F']:.2%} "
            f"(H1 {srow['Sharpe_H1']:.3f} / H2 {srow['Sharpe_H2']:.3f} / OOS {srow['Sharpe_OOS']:.3f})")

        for kn in REAL_KEYS + [f"NULL{j:02d}" for j in range(B_NULL)]:
            ic, t = rank_ic(keys[kn], px)
            ics.append(dict(panel=pn, key=kn, rank_IC=ic, t=t,
                            kind="real" if kn in REAL_KEYS else "nullkey"))

        def run(score, tag):
            r = score.where(elig_mask)
            rk = r.rank(axis=1, ascending=False)
            w = (rk <= N).astype(float) * (GROSS / N)
            res = backtest(px, w, cost_bps=0.0, freq=FREQ)
            return res["returns"].loc[start:], res["turnover"].loc[start:]

        ctrl0, ctrlt = run(comp, "CTRL")
        ctrl_rows = {c: full_row(ctrl0 - ctrlt * c / 1e4) for c in COSTS}
        for c in COSTS:
            rr = dict(panel=pn, key="CONTROL", kind="control", dir="-", m=0.0, cost=c,
                      turnover_yr=float(ctrlt.sum() / (len(ctrlt) / 252)))
            rr.update(ctrl_rows[c])
            rr["dSharpe_F"] = 0.0
            rr["dSharpe_IS"] = 0.0
            rr["dSharpe_OOS"] = 0.0
            rows.append(rr)

        for kn, kv in keys.items():
            for dn, dv in DIRS.items():
                for m in MS:
                    r0, trn = run(comp + dv * m * kv, f"{kn}/{dn}/{m}")
                    for c in COSTS:
                        rr = dict(panel=pn, key=kn,
                                  kind="real" if kn in REAL_KEYS else "nullkey",
                                  dir=dn, m=m, cost=c,
                                  turnover_yr=float(trn.sum() / (len(trn) / 252)))
                        rr.update(full_row(r0 - trn * c / 1e4))
                        for tag in ("F", "IS", "OOS"):
                            rr[f"dSharpe_{tag}"] = rr[f"Sharpe_{tag}"] - ctrl_rows[c][f"Sharpe_{tag}"]
                        rows.append(rr)

    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    IC = pd.DataFrame(ics)
    say(f"\ngrid: {len(G)} rows ({time.time() - t0:.0f}s) -> {STEM}.grid.csv")

    say("\n=== the null keys really are null (realised monthly rank IC vs 21d forward return) ===")
    for pn, sub in IC.groupby("panel", sort=False):
        rl = sub[sub["kind"] == "real"]
        nl = sub[sub["kind"] == "nullkey"]
        say(f"  {pn:5s} real: " + "  ".join(f"{r.key} {r.rank_IC:+.4f} (t {r.t:+.2f})"
                                            for r in rl.itertuples()))
        say(f"  {pn:5s} null: mean {nl['rank_IC'].mean():+.4f}, sd {nl['rank_IC'].std():.4f}, "
            f"|t| max {nl['t'].abs().max():.2f}, |t|>2 in {int((nl['t'].abs() > 2).sum())}/{len(nl)}")
    IC.to_csv(OUT / f"{STEM}.keyic.csv", index=False)

    # ---------------------------------------------------------------- Q1 the clause
    say("\n=== Q1  MAGNITUDE: does the real key's |dSharpe| clear its own null band? ===")
    say("    clause = |dSharpe(real)| > max over 20 matched null draws (one-sided 1/21 = 4.8%)")
    clause = []
    for (pn, dn, m, c), sub in G[G["kind"] != "control"].groupby(["panel", "dir", "m", "cost"],
                                                                sort=False):
        nulls = sub[sub["kind"] == "nullkey"]
        for tag in ("F", "IS"):
            nb = nulls[f"dSharpe_{tag}"].abs()
            thr = float(nb.max())
            for r in sub[sub["kind"] == "real"].itertuples():
                clause.append(dict(panel=pn, dir=dn, m=m, cost=c, window=tag, key=r.key,
                                   d=getattr(r, f"dSharpe_{tag}"),
                                   absd=abs(getattr(r, f"dSharpe_{tag}")),
                                   null_max=thr, null_mean=float(nb.mean()),
                                   clears=int(abs(getattr(r, f"dSharpe_{tag}")) > thr),
                                   pctile=float((nb < abs(getattr(r, f"dSharpe_{tag}"))).mean())))
    CL = pd.DataFrame(clause)
    CL.to_csv(OUT / f"{STEM}.clause.csv", index=False)
    F = CL[CL["window"] == "F"]
    say(f"  full-sample arms: {len(F)} real-key rows, clause cleared by "
        f"{int(F['clears'].sum())} ({F['clears'].mean():.1%})")
    say("\n  by key (full sample, 18 panel x dir x m x cost cells each):")
    say(f"  {'key':6s} {'clears':>7s} {'mean |d|':>9s} {'mean null max':>14s} {'mean pctile':>12s}")
    for k, sub in F.groupby("key", sort=False):
        say(f"  {k:6s} {int(sub['clears'].sum()):3d}/{len(sub):<3d} {sub['absd'].mean():9.4f} "
            f"{sub['null_max'].mean():14.4f} {sub['pctile'].mean():12.3f}")
    say("\n  by direction and panel (share of real-key rows clearing the clause, full sample):")
    say(pd.crosstab([F["panel"], F["dir"]], F["key"], values=F["clears"],
                    aggfunc="mean").to_string(float_format=lambda x: f"{x:.2f}"))
    say("\n  VOL/NEG — the LIVE /sqrt(vol20) scaler's own key and direction:")
    vn = F[(F["key"] == "VOL") & (F["dir"] == "NEG")]
    say(vn[["panel", "m", "cost", "d", "null_max", "clears"]].to_string(
        index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- Q2 verdicts
    say("\n=== Q2  VERDICT: does swapping the real key for a null key change KEEP/KILL? ===")
    ver = []
    for pn in panels:
        srow = ref[pn]["spy"]
        for c in COSTS:
            b = ref[pn]["b_ret"] - ref[pn]["b_trn"] * c / 1e4
            brow = full_row(b)
            sub = G[(G["panel"] == pn) & (G["cost"] == c)]
            for r in sub.to_dict("records"):
                ver.append(dict(panel=pn, key=r["key"], kind=r["kind"], dir=r["dir"], m=r["m"],
                                cost=c, CAGR_F=r["CAGR_F"], Sharpe_F=r["Sharpe_F"],
                                MaxDD_F=r["MaxDD_F"], Sharpe_H1=r["Sharpe_H1"],
                                Sharpe_H2=r["Sharpe_H2"], CAGR_OOS=r["CAGR_OOS"],
                                Sharpe_OOS=r["Sharpe_OOS"], MaxDD_OOS=r["MaxDD_OOS"],
                                dSharpe_F=r["dSharpe_F"], dSharpe_IS=r["dSharpe_IS"],
                                p4a=int(pass4a(r, brow)), p4b=int(pass4b(r, srow)),
                                p4bo=int(pass4b_oos(r, srow))))
    V = pd.DataFrame(ver)
    V.to_csv(OUT / f"{STEM}.verdicts.csv", index=False)
    real = V[V["kind"] == "real"]
    null = V[V["kind"] == "nullkey"]
    ctrl = V[V["kind"] == "control"]
    say(f"  pass counts over {len(real)} real-key arms: 4a {int(real['p4a'].sum())}, "
        f"4b(full) {int(real['p4b'].sum())}, 4b(OOS window) {int(real['p4bo'].sum())}")
    say(f"  pass counts over {len(null)} NULL-key arms: 4a {int(null['p4a'].sum())} "
        f"({null['p4a'].mean():.1%}), 4b(full) {int(null['p4b'].sum())} ({null['p4b'].mean():.1%}), "
        f"4b(OOS) {int(null['p4bo'].sum())} ({null['p4bo'].mean():.1%})")
    say(f"  pass rate over {len(real)} REAL arms:  4a {real['p4a'].mean():.1%}, "
        f"4b {real['p4b'].mean():.1%}, 4b(OOS) {real['p4bo'].mean():.1%}")
    say(f"  untilted CONTROL (6 rows): 4a {int(ctrl['p4a'].sum())}/6, 4b {int(ctrl['p4b'].sum())}/6, "
        f"4b(OOS) {int(ctrl['p4bo'].sum())}/6")

    say("\n  --- the direct swap: real key vs each of its 20 matched null draws, same cell ---")
    say(f"  {'bar':10s} {'real=null verdict':>18s} {'real pass, null pass':>21s} "
        f"{'real pass, null FAIL':>21s} {'real FAIL, null pass':>21s}")
    swap = []
    for bar in ("p4a", "p4b", "p4bo"):
        same = tot = rp_np = rp_nf = rf_np = 0
        for (pn, dn, m, c), sub in V[V["kind"] != "control"].groupby(
                ["panel", "dir", "m", "cost"], sort=False):
            nl = sub[sub["kind"] == "nullkey"][bar].values
            for r in sub[sub["kind"] == "real"].itertuples():
                rv = getattr(r, bar)
                tot += len(nl)
                same += int((nl == rv).sum())
                rp_np += int(((nl == 1) & (rv == 1)).sum())
                rp_nf += int(((nl == 0) & (rv == 1)).sum())
                rf_np += int(((nl == 1) & (rv == 0)).sum())
                swap.append(dict(bar=bar, panel=pn, dir=dn, m=m, cost=c, key=r.key,
                                 real=rv, null_pass_share=float(nl.mean())))
        say(f"  {bar:10s} {same / tot:18.3f} {rp_np / tot:21.3f} {rp_nf / tot:21.3f} "
            f"{rf_np / tot:21.3f}   (n={tot})")
    SW = pd.DataFrame(swap)
    SW.to_csv(OUT / f"{STEM}.swap.csv", index=False)

    say("\n  --- would the CLAUSE re-label any published verdict? ---")
    key_of = CL[CL["window"] == "F"].set_index(["panel", "dir", "m", "cost", "key"])["clears"]
    real2 = real.set_index(["panel", "dir", "m", "cost", "key"])
    real2 = real2.join(key_of.rename("clears"))
    for bar, lbl in (("p4a", "4a"), ("p4b", "4b full"), ("p4bo", "4b OOS")):
        p = real2[real2[bar] == 1]
        say(f"    {lbl:8s}: {len(p)} real-key passes, of which "
            f"{int(p['clears'].sum())} also clear the clause "
            f"({p['clears'].mean() if len(p) else float('nan'):.1%}) -> the clause would strip "
            f"the magnitude claim from {len(p) - int(p['clears'].sum())} of them, "
            f"WITHOUT changing the pass itself")
    say("    (the clause governs what may be SAID about a tilt's size; a 4a/4b pass is decided "
        "by the bars, so the clause re-labels claims, it does not move verdicts)")

    # ---------------------------------------------------------------- Q3 rule 8
    say("\n=== Q3  PROTOCOL rule 8: selectors read IS only, evaluated ONCE on 2017-2026 ===")
    wf = []
    for pn in panels:
        srow = ref[pn]["spy"]
        for c in COSTS:
            b = ref[pn]["b_ret"] - ref[pn]["b_trn"] * c / 1e4
            brow = full_row(b)
            sub = G[(G["panel"] == pn) & (G["cost"] == c)]
            ctl = sub[sub["kind"] == "control"].iloc[0]
            arms = sub[sub["kind"] != "control"]
            reals = arms[arms["kind"] == "real"]
            s1 = arms.loc[arms["Sharpe_IS"].idxmax()]
            adm = CL[(CL["window"] == "IS") & (CL["panel"] == pn) & (CL["cost"] == c)
                     & (CL["clears"] == 1)]
            if len(adm):
                mask = reals.set_index(["dir", "m", "key"]).index.isin(
                    list(zip(adm["dir"], adm["m"], adm["key"])))
                cand = reals[mask]
                s2 = cand.loc[cand["Sharpe_IS"].idxmax()]
                s2src = f"{s2['key']}/{s2['dir']}/{s2['m']}"
            else:
                s2, s2src = ctl, "CONTROL (nothing cleared)"
            for nm, pick, src in (("S0 do-nothing", ctl, "CONTROL"),
                                  ("S1 IS-argmax", s1, f"{s1['key']}/{s1['dir']}/{s1['m']}"),
                                  ("S2 clause-gated", s2, s2src)):
                wf.append(dict(panel=pn, cost=c, selector=nm, pick=src,
                               OOS_CAGR=pick["CAGR_OOS"], OOS_Sharpe=pick["Sharpe_OOS"],
                               OOS_MaxDD=pick["MaxDD_OOS"],
                               base_OOS_Sharpe=brow["Sharpe_OOS"], base_OOS_CAGR=brow["CAGR_OOS"],
                               base_OOS_MaxDD=brow["MaxDD_OOS"],
                               spy_OOS_Sharpe=srow["Sharpe_OOS"], spy_OOS_CAGR=srow["CAGR_OOS"],
                               spy_OOS_MaxDD=srow["MaxDD_OOS"],
                               p4a=int(pass4a(pick, brow)), p4b=int(pass4b(pick, srow)),
                               p4bo=int(pass4b_oos(pick, srow)),
                               n_admissible=len(adm)))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(W[["panel", "cost", "selector", "pick", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
           "p4a", "p4b", "p4bo", "n_admissible"]].to_string(
        index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n  mean OOS over the 6 (panel, cost) cells:")
    for nm, sub in W.groupby("selector", sort=False):
        say(f"    {nm:16s} CAGR {sub['OOS_CAGR'].mean():7.2%}  Sharpe {sub['OOS_Sharpe'].mean():.4f}"
            f"  MaxDD {sub['OOS_MaxDD'].mean():7.2%}  4b(OOS) {int(sub['p4bo'].sum())}/6")
    say(f"    {'RULES v1':16s} CAGR {W['base_OOS_CAGR'].mean():7.2%}  "
        f"Sharpe {W['base_OOS_Sharpe'].mean():.4f}  MaxDD {W['base_OOS_MaxDD'].mean():7.2%}")
    say(f"    {'SPY':16s} CAGR {W['spy_OOS_CAGR'].mean():7.2%}  "
        f"Sharpe {W['spy_OOS_Sharpe'].mean():.4f}  MaxDD {W['spy_OOS_MaxDD'].mean():7.2%}")
    piv = W.pivot_table(index=["panel", "cost"], columns="selector", values="OOS_Sharpe")
    say("\n  paired (S1 - S0) mean " + f"{(piv['S1 IS-argmax'] - piv['S0 do-nothing']).mean():+.4f}"
        f", wins {int((piv['S1 IS-argmax'] > piv['S0 do-nothing']).sum())}/6;  "
        f"(S2 - S0) mean {(piv['S2 clause-gated'] - piv['S0 do-nothing']).mean():+.4f}, "
        f"wins {int((piv['S2 clause-gated'] > piv['S0 do-nothing']).sum())}/6;  "
        f"S2 picks differ from S1 in "
        f"{int((W[W['selector'] == 'S1 IS-argmax']['pick'].values != W[W['selector'] == 'S2 clause-gated']['pick'].values).sum())}/6")

    # ---------------------------------------------------------------- census
    say("\n=== LEADERBOARD CENSUS: entries resting on a tilt's realised magnitude ===")
    lb = (ROOT / "research" / "LEADERBOARD.md").read_text().split("\n")
    MAGN = re.compile(r"dsharpe|moves? sharpe|sharpe by|tilt|scaler|\bkey\b|/sqrt\(vol", re.I)
    NUMB = re.compile(r"[-+]?\d*\.\d+")
    cen = []
    for ln in lb:
        if not ln.startswith("| 20"):
            continue
        cells = ln.split(" | ")
        idea = cells[1] if len(cells) > 1 else ""
        verdict = cells[7] if len(cells) > 8 else ln
        rests = bool(MAGN.search(verdict) and NUMB.search(verdict))
        cen.append(dict(idea=idea[:120], magnitude_claim=int(rests),
                        verdict=re.sub(r"\s+", " ", verdict)[:240]))
    C = pd.DataFrame(cen)
    C.to_csv(OUT / f"{STEM}.census.csv", index=False)
    say(f"  {len(C)} LEADERBOARD rows; {int(C['magnitude_claim'].sum())} rest on the realised "
        f"magnitude of a keyed tilt ({C['magnitude_claim'].mean():.1%})")
    named = C[C["magnitude_claim"] == 1]["idea"].tolist()
    say("  the entries the clause would touch (first 12 named):")
    for s in named[:12]:
        say(f"    - {s}")
    say(f"  ... and {max(0, len(named) - 12)} more, all in .census.csv")
    say("  NOTE: this classifies TEXT.  Of these, the ones whose construction is inside this "
        "run's grid (tilt of the RULES v1 composite by VOL/MOM/R6/R3/PRICE on u56/broad/small "
        "at 10 or 25 bps) are priced above; rows built on sleeves, gates, entry budgets or "
        "book-share ladders are NOT re-run here and are not claimed to be.")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_console) + "\n")
    say(f"\ndone in {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_console) + "\n")


if __name__ == "__main__":
    main()
