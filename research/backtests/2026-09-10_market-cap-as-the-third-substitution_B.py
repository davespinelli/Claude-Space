#!/usr/bin/env python3
"""IDEA 195 - market-cap-as-the-third-substitution   (lane B, 2026-09-10)

THE QUEUE ENTRY, AND WHY IT IS CLAIMABLE TODAY
    Idea 193 ran the low-price tilt's substitutions (a) FROZEN and (b) DVOL and left leg (c)
    MCAP unrun for want of a shares-outstanding series; idea 185 re-stated the same gap; a
    2026-09-08 lane-B pass re-affirmed the PARK after searching `data/` and finding
    prices/volume/earnings/form4/spinoffs/small_meta only.  That search was too narrow.
    `research/deepvalue/universe_under2b.csv` - written by the filings job, not the price job -
    carries `shares` (dei:EntityCommonStockSharesOutstanding and friends) and `mktcap` for 716
    tickers, of which **430 of the 439 SMALL panel names** are covered.  Leg (c) is runnable.

    It is runnable in ONE FORM ONLY, and naming that form is half the answer.  The file is a
    SNAPSHOT: one share count, dated today, per name.  There is no shares TIME SERIES anywhere
    in the repo.  So the only market cap this run can build is

        MCAP_t = px_t * s_T        (adjusted close at t) x (share count at T)

    and by idea 193's own identity that is the true market cap times TWO terminal-known
    constants per name: (s_T / s_t), sixteen years of buybacks and dilution, and the panel's
    per-name dividend-adjustment factor.  MCAP is therefore a LEAKING key BY CONSTRUCTION,
    strictly leakier than PRICE, and this run reports it as such.  Idea 565's pinning
    convention is honoured: the snapshot is committed beside the result as `.shares.csv`,
    because `universe_under2b.csv` is rewritten nightly and this run is otherwise
    irreproducible tomorrow.

THE QUESTION, unchanged from idea 193: put MCAP into the substitution table beside PRICE,
    FROZEN, DVOL, VOLSH, DDTR, REBASED and read it against idea 185's leak law
    (Spearman(|IC vs realised forward total return|, mean NEG dSharpe) = +0.881 on small).
    Decompose it, because a snapshot lets the two dimensions be separated exactly:

        MCAP     = rankpct(px * s)          dynamic price x frozen terminal shares  <- leg (c)
        MCAPFRZ  = rankpct(entry * s)       frozen entry price x frozen shares (static size)
        SHARES   = rankpct(s)               the PURE size dimension, price-free, static
        MCAPREB  = rankpct((px / entry) * s) price LEVEL removed, shares kept

    If leg (c) is just PRICE wearing a size label, MCAP tracks PRICE and SHARES carries little.
    If size is its own dimension, SHARES carries a share of MCAP's dSharpe on its own.

PRE-REGISTERED PREDICTIONS (written before the grid ran; scored verbatim at the end)
    P1  Gates: fast_backtest == engine.backtest to 1e-12; the rung identity to 1e-12;
        mktcap == price*shares in the snapshot to 1e-12; idea 185's published small-panel
        rows reproduce to <= 5e-3 (SPY is joined from data/prices.csv, which is rewritten
        daily - idea 137's drift allowance; a tighter bar would fail for the wrong reason).
    P2  MCAP/NEG's mean dSharpe_F on SMALL430 is POSITIVE and clears the null band.
    P3  MCAP LEAKS MORE THAN PRICE: |mean IC vs forward return| is larger for MCAP than for
        PRICE, and under idea 185's law MCAP/NEG's dSharpe is therefore LARGER than PRICE/NEG's.
    P4  SHARES alone carries less than HALF of MCAP's mean NEG dSharpe: the size dimension is
        not the content.
    P5  Idea 185's leak law survives the four new points: Spearman(|IC|, mean NEG dSharpe)
        over the real non-oracle keys stays >= +0.70.
    P6  No leg-(c) arm passes BOTH KEEP paths at 10 bps, and the rule-8 chooser inside the
        MCAP family does not beat RULES v2 out of sample.

PROTOCOL
    2. costs 10 bps (0 and 25 also reported), weights at t applied t+1 (engine convention,
       reproduced by fast_backtest at machine precision - gate G1).
    3. compared against RULES v2 (live baseline) AND RULES v1 AND SPY.
    4. full sample + both halves; both KEEP paths counted on every arm.
    5. one idea, one script, deterministic.
    8. walk-forward: (key, m) chosen on 2010-2016 only, 2017-2026 read once.
    Two tuned parameters: KEY and TILT STRENGTH m.  Every grid point is reported.

SURVIVORSHIP, stated as PROTOCOL 9 requires and worse than usual here: the SMALL panel is
    current constituents of a sub-$2B screen (data/SMALL_PANEL_README.md), and the shares
    snapshot is by construction only available for names that still file today, so the 430-name
    sub-panel is a survivor of a survivor.  Every number below is biased in the tilt's favour.

Writes .console.txt, .arms.csv, .keyic.csv, .walkforward.csv, .reproduction.csv, .shares.csv.
Deterministic, standalone:  python research/backtests/2026-09-10_market-cap-as-the-third-substitution_B.py
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import (load_universe, load_volume, rules_v1_weights,  # noqa: E402
                      rules_v2_weights)
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-10_market-cap-as-the-third-substitution_B"
OUT = ROOT / "research" / "backtests"
PARENT = "2026-09-06_is-the-low-price-tilt-a-split-artefact-or-a-survivorship-one_cloud"
CAPFILE = ROOT / "research" / "deepvalue" / "universe_under2b.csv"

# ---- inherited verbatim from ideas 181/185/193 so the published cells stay comparable
SEED, B_NULL = 181, 20
N, GROSS, FREQ, MAXVOL = 20, 0.75, "W", 0.60
MS = [0.20, 0.50, 1.00]
DIRS = {"POS": 1.0, "NEG": -1.0}
COSTS = [0.0, 10.0, 25.0]
IS_END = pd.Timestamp("2016-12-31")
OOS_LO = IS_END + pd.Timedelta(days=1)
PHI, DELTA = 0.70, 0.60
REPRO_TOL = 5e-3                      # pre-stated, see P1

RECORD = ["PRICE", "FROZEN", "DDTR", "REBASED", "DVOL", "VOLSH"]
LEGC = ["MCAP", "MCAPFRZ", "SHARES", "MCAPREB"]
ORACLE = ["PXTERM", "FWDRET"]
PRICELEVEL = ["PRICE", "FROZEN"]
LEAKFREE = ["DDTR", "REBASED"]

_console = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _console.append(s)


def rankpct(df):
    return df.rank(axis=1, pct=True)


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 5:
        return np.nan
    ra, rb = pd.Series(a[m]).rank().values, pd.Series(b[m]).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


# ------------------------------------------------------------------ vectorised engine equivalent
def fast_backtest(prices, weights, freq=FREQ):
    """Returns (gross returns at 0 bps, turnover).  Costs are applied afterwards through the
    rung identity r(c) = r(0) - turnover * c / 1e4, which gate G4 checks against the engine."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy()
    m[0] = True
    T, Ncol = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, Ncol)), C[:-1]])
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    port = (held * rets).sum(axis=1)
    return pd.Series(port, index=idx), pd.Series(turn, index=idx)


# ------------------------------------------------------------------------------ panel and keys
def small_panel_full():
    """Idea 185's small panel, verbatim: 439 names + SPY, SPY includable."""
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], bad


def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (rankpct(mom) + rankpct(r6) + rankpct(r3)) / 3


def first_valid_row(px):
    fv = px.apply(lambda s: s.loc[s.first_valid_index()] if s.first_valid_index() is not None
                  else np.nan)
    out = pd.DataFrame(np.tile(fv.values, (len(px), 1)), index=px.index, columns=px.columns)
    return out.where(px.notna())


def last_valid_row(px):
    lv = px.apply(lambda s: s.loc[s.last_valid_index()] if s.last_valid_index() is not None
                  else np.nan)
    out = pd.DataFrame(np.tile(lv.values, (len(px), 1)), index=px.index, columns=px.columns)
    return out.where(px.notna())


def build_keys(px, shares, rng, with_legc=True):
    entry, term = first_valid_row(px), last_valid_row(px)
    keys = {
        "PRICE":   rankpct(px),                                     # published - the arm on trial
        "FROZEN":  rankpct(entry),                                  # idea 193 leg (a)
        "DDTR":    rankpct(px / px.rolling(252).max() - 1.0),       # leak-free "beaten down"
        "REBASED": rankpct(px / entry),                             # causal level proxy
        "PXTERM":  rankpct(term),                                   # oracle diagnostic
        "FWDRET":  rankpct(term / px - 1.0),                        # oracle diagnostic
    }
    vol = load_volume(small=True).reindex(index=px.index, columns=px.columns)
    for nm, raw in (("DVOL", px * vol), ("VOLSH", vol)):            # idea 193 leg (b) + companion
        k = rankpct(raw.rolling(20).mean())
        if "SPY" in k.columns:
            k["SPY"] = 0.5                                          # idea 193's convention
        keys[nm] = k
    if with_legc:
        S = pd.DataFrame(np.tile(shares.reindex(px.columns).values, (len(px), 1)),
                         index=px.index, columns=px.columns).where(px.notna())
        keys["MCAP"] = rankpct(px * S)                              # LEG (c)
        keys["MCAPFRZ"] = rankpct(entry * S)
        keys["SHARES"] = rankpct(S)
        keys["MCAPREB"] = rankpct((px / entry) * S)
    sd = float(np.nanmedian(px.pct_change().std().values))
    for j in range(B_NULL):
        steps = rng.normal(0.0, sd, size=px.shape)
        walk = pd.DataFrame(np.cumsum(steps, axis=0), index=px.index, columns=px.columns) + 10.0
        keys[f"NULL{j:02d}"] = rankpct(walk / walk.shift(126) - 1)
    return keys


# --------------------------------------------------------------------------------------- metrics
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
                   ("IS", win(r, hi=IS_END)), ("OOS", win(r, lo=OOS_LO))):
        m = metrics(x)
        out[f"CAGR_{tag}"], out[f"Sharpe_{tag}"], out[f"MaxDD_{tag}"] = \
            m["CAGR"], m["Sharpe"], m["MaxDD"]
    return out


def pass4a(row, base):
    """PROTOCOL 4a against the LIVE rules (RULES v2 since 2026-09-06)."""
    return bool(row["Sharpe_H1"] > base["Sharpe_H1"] and row["Sharpe_H2"] > base["Sharpe_H2"]
                and row["MaxDD_F"] >= base["MaxDD_F"])


def pass4b(row, spy):
    return bool(row["Sharpe_H1"] > spy["Sharpe_H1"] and row["Sharpe_H2"] > spy["Sharpe_H2"]
                and row["Sharpe_OOS"] > spy["Sharpe_OOS"]
                and row["MaxDD_F"] >= DELTA * spy["MaxDD_F"]
                and row["CAGR_F"] >= PHI * spy["CAGR_F"])


# ============================================================================================ run
def main():
    t0 = time.time()
    say("=" * 112)
    say(f"IDEA 195  market-cap-as-the-third-substitution   (lane B, {pd.Timestamp.today().date()})")
    say("=" * 112)
    say("Leg (c) of idea 193's substitution.  PARKED since 2026-09-05 for want of a shares series;")
    say("re-affirmed PARK 2026-09-08 after a search of data/ only.  The series is in the repo:")
    say(f"  {CAPFILE.relative_to(ROOT)}  (filings job, rewritten NIGHTLY - snapshot pinned below)")
    say("It is a SNAPSHOT, not a history, so the only market cap constructible is px_t * s_T,")
    say("which is the true cap times two terminal-known per-name constants (s_T/s_t and the")
    say("dividend-adjustment factor).  Leg (c) is therefore run in a LEAKING form, and that is")
    say("reported as the finding, not hidden as a caveat.")
    say(f"Two tuned params: KEY (all reported) x TILT STRENGTH m in {MS} (all reported).")
    say("")

    repro, arms, ics = [], [], []

    # ------------------------------------------------------------------ G0/G3  the snapshot
    cap = pd.read_csv(CAPFILE).dropna(subset=["ticker"])
    assert cap["ticker"].duplicated().sum() == 0
    rel = float(((cap["mktcap"] - cap["price"] * cap["shares"]).abs()
                 / cap["mktcap"].abs()).max())
    say(f"G3  snapshot self-consistency  mktcap == price * shares : max rel err {rel:.3e} "
        f"-> {'PASS' if rel < 1e-12 else 'FAIL'}")
    repro.append(dict(check="G3_snapshot_identity", value=rel, target=0.0, err=rel))

    pxF, bad = small_panel_full()
    names_full = [c for c in pxF.columns if c != "SPY"]
    shares = cap.set_index("ticker")["shares"]
    covered = [c for c in names_full if c in shares.index]
    say(f"G0  panel coverage: small panel {len(names_full)} names after the max_1d_move>=1.0 drop "
        f"({len(bad)} dropped); shares outstanding present for {len(covered)} "
        f"({len(covered)/len(names_full):.1%}).")
    miss = sorted(set(names_full) - set(covered))
    say(f"    the {len(miss)} uncovered names are dropped from the leg-(c) panel: {', '.join(miss)}")
    fp = cap.set_index("ticker")["price"].reindex(covered)
    lastpx = pxF[covered].ffill().iloc[-1]
    dd = ((fp - lastpx).abs() / lastpx)
    say(f"    snapshot price vs panel last adjusted close: median {dd.median():.4f}, "
        f"q90 {dd.quantile(0.9):.4f}, max {dd.max():.4f}  (staleness + the dividend-adjustment")
    say("    factor - exactly the terminal-known per-name constant that makes MCAP leak)")
    pd.DataFrame({"ticker": covered,
                  "shares": shares.reindex(covered).values,
                  "mktcap_snapshot": cap.set_index("ticker")["mktcap"].reindex(covered).values,
                  "price_snapshot": fp.values,
                  "panel_last_adj_close": lastpx.values,
                  "source": "research/deepvalue/universe_under2b.csv",
                  "pinned_utc": pd.Timestamp.utcnow().isoformat()}).to_csv(
        OUT / f"{STEM}.shares.csv", index=False)
    say(f"    snapshot PINNED to {STEM}.shares.csv (idea 565's convention: the source file is")
    say("    rewritten nightly, so without the pin this run is irreproducible tomorrow)")
    say("")

    # ------------------------------------------------------------- G2  reproduce idea 185's cells
    say("G2  REPRODUCTION of idea 185's published small-panel rows (its exact 439+SPY panel,")
    say("    its keys, its construction).  Establishes that leg (c) is being added to the SAME")
    say(f"    table.  Pre-stated tolerance {REPRO_TOL:.0e} (SPY is joined from the daily-rewritten")
    say("    data/prices.csv - idea 137's drift allowance).")
    startF = pxF.index[260]
    keysF = build_keys(pxF, shares, np.random.default_rng(SEED + 3000), with_legc=False)
    compF = composite(pxF)
    vol20F = pxF.pct_change().rolling(20).std() * np.sqrt(252)
    eligF = (pxF > pxF.rolling(200).mean()) & (vol20F < MAXVOL)

    def runF(sc):
        rk = sc.where(eligF).rank(axis=1, ascending=False)
        w = (rk <= N).astype(float) * (GROSS / N)
        g, t = fast_backtest(pxF, w)
        return g.loc[startF:], t.loc[startF:]

    c0F, ctF = runF(compF)
    engF = backtest(pxF, (compF.where(eligF).rank(axis=1, ascending=False) <= N).astype(float)
                    * (GROSS / N), cost_bps=0.0, freq=FREQ)["returns"].loc[startF:]
    g1 = float((engF - c0F).abs().max())
    say(f"G1  fast_backtest == engine.backtest on the control book : max abs err {g1:.3e} "
        f"-> {'PASS' if g1 < 1e-12 else 'FAIL'}")
    repro.append(dict(check="G1_fast_vs_engine", value=g1, target=0.0, err=g1))
    eng25 = backtest(pxF, (compF.where(eligF).rank(axis=1, ascending=False) <= N).astype(float)
                     * (GROSS / N), cost_bps=25.0, freq=FREQ)["returns"].loc[startF:]
    g4 = float((eng25 - (c0F - ctF * 25.0 / 1e4)).abs().max())
    say(f"G4  rung identity r(c) = r(0) - turnover*c/1e4 vs a live 25 bps engine run : "
        f"{g4:.3e} -> {'PASS' if g4 < 1e-12 else 'FAIL'}")
    repro.append(dict(check="G4_rung_identity", value=g4, target=0.0, err=g4))

    ctrlF = {c: full_row(c0F - ctF * c / 1e4) for c in COSTS}
    old = pd.read_csv(OUT / f"{PARENT}.arms.csv")
    old = old[(old.panel == "small") & (old.key.isin(RECORD))]
    rows = []
    for kn in RECORD:
        for dn, dv in DIRS.items():
            for m in MS:
                r0, trn = runF(compF + dv * m * keysF[kn])
                for c in (10.0, 25.0):
                    rw = full_row(r0 - trn * c / 1e4)
                    rows.append(dict(key=kn, dir=dn, m=m, cost=c, Sharpe_F=rw["Sharpe_F"],
                                     dSharpe_F=rw["Sharpe_F"] - ctrlF[c]["Sharpe_F"]))
    mg = old.merge(pd.DataFrame(rows), on=["key", "dir", "m", "cost"], suffixes=("_o", "_n"))
    d1 = float((mg.Sharpe_F_o - mg.Sharpe_F_n).abs().max())
    d2 = float((mg.dSharpe_F_o - mg.dSharpe_F_n).abs().max())
    say(f"    matched {len(mg)} of the parent's {len(old)} rows; max |dSharpe_F| {d1:.3e}, "
        f"max |ddSharpe_F| {d2:.3e} -> {'PASS' if max(d1, d2) < REPRO_TOL else 'FAIL'}")
    repro.append(dict(check="G2_parent_rows", value=max(d1, d2), target=0.0, err=max(d1, d2)))
    say("")

    # ------------------------------------------------------------------- the leg-(c) panel
    px = pxF[covered]                                  # SPY is a BENCHMARK here, not a constituent
    spy_px = pxF["SPY"]
    start = px.index[260]
    keys = build_keys(px, shares, np.random.default_rng(SEED + 1000 * 3), with_legc=True)
    comp = composite(px)
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    elig = (px > px.rolling(200).mean()) & (vol20 < MAXVOL)
    spy = spy_px.pct_change().fillna(0).loc[start:]
    srow = full_row(spy)
    say("=" * 112)
    say(f"SMALL430 leg-(c) panel: {px.shape[1]} names, SPY benchmark only (not a constituent), "
        f"sample {start.date()}..{px.index[-1].date()}")
    say(f"  SPY  {srow['CAGR_F']:.2%} / {srow['Sharpe_F']:.3f} / {srow['MaxDD_F']:.2%}   "
        f"(H1 {srow['Sharpe_H1']:.3f} / H2 {srow['Sharpe_H2']:.3f} / OOS {srow['Sharpe_OOS']:.3f})")

    def run(sc):
        rk = sc.where(elig).rank(axis=1, ascending=False)
        w = (rk <= N).astype(float) * (GROSS / N)
        g, t = fast_backtest(px, w)
        return g.loc[start:], t.loc[start:]

    c0, ct = run(comp)
    ctrl_rows = {c: full_row(c0 - ct * c / 1e4) for c in COSTS}
    b1 = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq="W")
    b2 = backtest(px, rules_v2_weights(px), cost_bps=0.0, freq="W")
    v1_rows = {c: full_row(b1["returns"].loc[start:] - b1["turnover"].loc[start:] * c / 1e4)
               for c in COSTS}
    v2_rows = {c: full_row(b2["returns"].loc[start:] - b2["turnover"].loc[start:] * c / 1e4)
               for c in COSTS}
    for nm, rr in (("control (untilted composite book)", ctrl_rows), ("RULES v1", v1_rows),
                   ("RULES v2 (live baseline)", v2_rows)):
        r = rr[10.0]
        say(f"  {nm:36s} @10bps {r['CAGR_F']:7.2%} / {r['Sharpe_F']:6.3f} / {r['MaxDD_F']:7.2%}   "
            f"(H1 {r['Sharpe_H1']:.3f} / H2 {r['Sharpe_H2']:.3f} / OOS {r['Sharpe_OOS']:.3f})")
    for c in COSTS:
        r = dict(key="CONTROL", klass="control", dir="-", m=0.0, cost=c,
                 turnover_yr=float(ct.sum() / (len(ct) / 252)),
                 dSharpe_F=0.0, dSharpe_IS=0.0, dSharpe_OOS=0.0)
        r.update(ctrl_rows[c])
        r["pass4a"] = pass4a(r, v2_rows[c])
        r["pass4b"] = pass4b(r, srow)
        arms.append(r)
    say("")

    # --------------------------------------------------------- leak content of every key
    fwd = (px.iloc[-1] / px - 1.0)
    for kn, kv in keys.items():
        if kn.startswith("NULL"):
            continue
        rows_ix = kv.index[(len(kv) // 4)::252]         # a date grid, not a chosen date
        vals = [spearman(kv.loc[d].values, fwd.loc[d].values) for d in rows_ix]
        ics.append(dict(key=kn, mean_IC_fwd=float(np.nanmean(vals)),
                        n_dates=int(np.isfinite(vals).sum())))

    # ------------------------------------------------------------------------------ the grid
    for kn, kv in keys.items():
        klass = ("nullkey" if kn.startswith("NULL") else
                 "oracle" if kn in ORACLE else
                 "legc" if kn in LEGC else
                 "pricelevel" if kn in PRICELEVEL else
                 "leakfree" if kn in LEAKFREE else "levelproduct")
        for dn, dv in DIRS.items():
            for m in MS:
                r0, trn = run(comp + dv * m * kv)
                for c in COSTS:
                    rr = dict(key=kn, klass=klass, dir=dn, m=m, cost=c,
                              turnover_yr=float(trn.sum() / (len(trn) / 252)))
                    rr.update(full_row(r0 - trn * c / 1e4))
                    for tag in ("F", "IS", "OOS"):
                        rr[f"dSharpe_{tag}"] = rr[f"Sharpe_{tag}"] - ctrl_rows[c][f"Sharpe_{tag}"]
                    rr["pass4a"] = pass4a(rr, v2_rows[c])
                    rr["pass4b"] = pass4b(rr, srow)
                    arms.append(rr)
    A = pd.DataFrame(arms)
    A.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    IC = pd.DataFrame(ics).sort_values("mean_IC_fwd")
    IC.to_csv(OUT / f"{STEM}.keyic.csv", index=False)
    pd.DataFrame(repro).to_csv(OUT / f"{STEM}.reproduction.csv", index=False)
    say(f"{len(A)} arm rows over {len([k for k in keys if not k.startswith('NULL')])} real keys "
        f"+ {B_NULL} nulls x 2 directions x {len(MS)} strengths x {len(COSTS)} rungs "
        f"({time.time()-t0:.0f}s).  ALL of them are in {STEM}.arms.csv; nothing below is picked.")
    say("")

    # ------------------------------------------------------------------- Q1 the substitution table
    real = A[(~A.key.str.startswith("NULL")) & (A.key != "CONTROL")]
    nul = A[A.key.str.startswith("NULL")]
    say("=" * 112)
    say("Q1  THE SUBSTITUTION TABLE, SMALL430.  dSharpe_F vs the untilted control at 10 bps.")
    say("    The last column is the null band: the q95 of |dSharpe_F| over the 20 random-walk")
    say("    keys at the same (dir, m).  A key inside its own band is indistinguishable from noise.")
    say("")
    nb = nul[nul.cost == 10.0].groupby(["dir", "m"])["dSharpe_F"].apply(
        lambda s: float(np.nanquantile(s.abs(), 0.95)))
    hdr = " ".join(f"{(d+' m'+str(m)):>13s}" for d in ["NEG", "POS"] for m in MS)
    say(f"  {'key':9s} {'class':13s} {hdr}   {'mean NEG':>9s} {'null q95':>9s}")
    order = ["MCAP", "MCAPFRZ", "SHARES", "MCAPREB", "PRICE", "FROZEN", "DVOL", "VOLSH",
             "DDTR", "REBASED", "PXTERM", "FWDRET"]
    for kn in order:
        g = real[(real.key == kn) & (real.cost == 10.0)]
        cells = []
        for d in ["NEG", "POS"]:
            for m in MS:
                v = g[(g.dir == d) & (g.m == m)]["dSharpe_F"]
                cells.append(f"{v.iloc[0]:+13.4f}" if len(v) else f"{'':>13s}")
        mneg = g[g.dir == "NEG"]["dSharpe_F"].mean()
        band = float(np.nanmean([nb.get(("NEG", m), np.nan) for m in MS]))
        say(f"  {kn:9s} {g.klass.iloc[0]:13s} " + " ".join(cells) +
            f"   {mneg:+9.4f} {band:9.4f}")
    say("")

    # -------------------------------------------------------------------------- Q2 the leak law
    say("=" * 112)
    say("Q2  IDEA 185'S LEAK LAW WITH THE FOUR NEW POINTS ON IT.")
    say("    mean_IC_fwd = Spearman(key rank, realised forward total return to T), on a 252-day")
    say("    date grid.  A key that knows the future has |IC| far from 0.  Idea 185 measured")
    say("    Spearman(|IC|, mean NEG dSharpe) = +0.881 on the small panel over 10-12 keys.")
    say("")
    mn = real[(real.cost == 10.0) & (real.dir == "NEG")].groupby("key")["dSharpe_F"].mean()
    mp = real[(real.cost == 10.0) & (real.dir == "POS")].groupby("key")["dSharpe_F"].mean()
    tab = IC.set_index("key").join(mn.rename("mean_dS_NEG")).join(mp.rename("mean_dS_POS"))
    tab["abs_IC"] = tab.mean_IC_fwd.abs()
    say(f"  {'key':9s} {'class':13s} {'mean IC vs fwd ret':>19s} {'|IC|':>8s} "
        f"{'mean dS NEG':>12s} {'mean dS POS':>12s}")
    for kn in order:
        if kn not in tab.index:
            continue
        r = tab.loc[kn]
        kl = real[real.key == kn].klass.iloc[0]
        say(f"  {kn:9s} {kl:13s} {r.mean_IC_fwd:19.4f} {r.abs_IC:8.4f} "
            f"{r.mean_dS_NEG:12.4f} {r.mean_dS_POS:12.4f}")
    fam = [k for k in order if k not in ORACLE]
    t2 = tab.loc[[k for k in fam if k in tab.index]]
    rho_all = spearman(t2.abs_IC.values, t2.mean_dS_NEG.values)
    t3 = t2.drop(index=[k for k in LEGC if k in t2.index])
    rho_rec = spearman(t3.abs_IC.values, t3.mean_dS_NEG.values)
    say("")
    say(f"  Spearman(|IC|, mean NEG dSharpe), record keys only ({len(t3)} keys): {rho_rec:+.3f}")
    say(f"  Spearman(|IC|, mean NEG dSharpe), with leg (c) added  ({len(t2)} keys): {rho_all:+.3f}")
    say("")

    # ------------------------------------------------------------------------- Q3 decomposition
    say("=" * 112)
    say("Q3  DECOMPOSITION - is leg (c) a SIZE key or a PRICE key wearing a size label?")
    say("    MCAP = PRICE x (a frozen per-name share count).  SHARES is that share count alone.")
    say("")
    for c in COSTS:
        g = real[(real.cost == c) & (real.dir == "NEG")].groupby("key")["dSharpe_F"].mean()
        pieces = " ".join(f"{k} {g.get(k, np.nan):+.4f}" for k in
                          ["MCAP", "SHARES", "MCAPFRZ", "MCAPREB", "PRICE", "FROZEN"])
        say(f"  @{c:5.1f} bps  mean NEG dSharpe:  {pieces}")
    sh_frac = (real[(real.cost == 10.0) & (real.dir == "NEG") & (real.key == "SHARES")]
               .dSharpe_F.mean()
               / real[(real.cost == 10.0) & (real.dir == "NEG") & (real.key == "MCAP")]
               .dSharpe_F.mean())
    say(f"  SHARES / MCAP share of the mean NEG dSharpe at 10 bps: {sh_frac:.3f}")
    # cross-sectional rank agreement between the keys, averaged over the date grid
    grid = px.index[(len(px) // 4)::252]
    say("")
    say("  Cross-sectional Spearman between key ranks (mean over the same 252-day date grid):")
    for a, b in [("MCAP", "PRICE"), ("MCAP", "SHARES"), ("MCAP", "DVOL"), ("SHARES", "PRICE"),
                 ("MCAPFRZ", "FROZEN"), ("MCAPREB", "REBASED")]:
        v = float(np.nanmean([spearman(keys[a].loc[d].values, keys[b].loc[d].values)
                              for d in grid]))
        say(f"    rho({a:8s}, {b:8s}) = {v:+.4f}")
    say("")

    # ------------------------------------------------------------------------ Q4 PROTOCOL counts
    say("=" * 112)
    say("Q4  PROTOCOL 4 - BOTH KEEP PATHS ON EVERY ARM.  4a is judged against RULES v2 (live),")
    say("    4b against SPY on this panel.  Counts are over ALL arms, nulls included.")
    say("")
    say(f"  {'rung':>6s} {'arms':>6s} {'4a':>6s} {'4b':>6s} {'BOTH':>6s}   "
        f"{'4a legc':>8s} {'4b legc':>8s} {'BOTH legc':>10s}")
    for c in COSTS:
        g = A[A.cost == c]
        gl = g[g.klass == "legc"]
        say(f"  {c:6.1f} {len(g):6d} {int(g.pass4a.sum()):6d} {int(g.pass4b.sum()):6d} "
            f"{int((g.pass4a & g.pass4b).sum()):6d}   {int(gl.pass4a.sum()):8d} "
            f"{int(gl.pass4b.sum()):8d} {int((gl.pass4a & gl.pass4b).sum()):10d}")
    p4b = A[(A.cost == 10.0) & A.pass4b]
    if len(p4b):
        say("")
        say("  every 4b passer at 10 bps:")
        for _, r in p4b.iterrows():
            say(f"    {r.key:9s} {r.dir:3s} m={r.m:.2f}  {r.CAGR_F:7.2%} / {r.Sharpe_F:6.3f} / "
                f"{r.MaxDD_F:7.2%}  OOS Sharpe {r.Sharpe_OOS:6.3f}")
    say("")

    # --------------------------------------------------------------------- Q5 rule 8 walk-forward
    say("=" * 112)
    say("Q5  PROTOCOL 8 WALK-FORWARD.  Both tuned parameters - KEY and TILT STRENGTH m - are")
    say("    chosen on 2010-2016 IS Sharpe ALONE, inside a named menu, and 2017-2026 is read")
    say("    once.  Four menus: the leg-(c) family, the record's keys, everything, and NO TILT.")
    say("")
    wf = []
    menus = {"LEGC": LEGC, "RECORD": RECORD,
             "ALL": [k for k in order if k not in ORACLE], "NOTILT": []}
    for c in COSTS:
        base_ctrl = ctrl_rows[c]
        for mname, ks in menus.items():
            if not ks:
                pick, row = ("CONTROL", "-", 0.0), base_ctrl
            else:
                cand = A[(A.cost == c) & (A.key.isin(ks))]
                i = cand.Sharpe_IS.idxmax()
                row = A.loc[i]
                pick = (row.key, row.dir, row.m)
            wf.append(dict(cost=c, menu=mname, pick_key=pick[0], pick_dir=pick[1], pick_m=pick[2],
                           Sharpe_IS=row["Sharpe_IS"], CAGR_OOS=row["CAGR_OOS"],
                           Sharpe_OOS=row["Sharpe_OOS"], MaxDD_OOS=row["MaxDD_OOS"],
                           beats_ctrl_OOS=bool(row["Sharpe_OOS"] > base_ctrl["Sharpe_OOS"]),
                           beats_v2_OOS=bool(row["Sharpe_OOS"] > v2_rows[c]["Sharpe_OOS"]),
                           beats_v1_OOS=bool(row["Sharpe_OOS"] > v1_rows[c]["Sharpe_OOS"]),
                           beats_SPY_OOS=bool(row["Sharpe_OOS"] > srow["Sharpe_OOS"])))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(f"  {'rung':>6s} {'menu':7s} {'IS pick':>22s} {'IS Sh':>7s} | {'OOS CAGR':>9s} "
        f"{'OOS Sh':>7s} {'OOS MaxDD':>10s} | {'>ctrl':>6s} {'>v2':>5s} {'>v1':>5s} {'>SPY':>5s}")
    for _, r in W.iterrows():
        say(f"  {r.cost:6.1f} {r.menu:7s} "
            f"{(r.pick_key + '/' + str(r.pick_dir) + '/m' + f'{r.pick_m:.2f}'):>22s} "
            f"{r.Sharpe_IS:7.3f} | {r.CAGR_OOS:9.2%} {r.Sharpe_OOS:7.3f} {r.MaxDD_OOS:10.2%} | "
            f"{str(r.beats_ctrl_OOS):>6s} {str(r.beats_v2_OOS):>5s} {str(r.beats_v1_OOS):>5s} "
            f"{str(r.beats_SPY_OOS):>5s}")
    say("")
    say("  the OOS comparands, same window, same panel:")
    for nm, rr in (("RULES v2 (live)", v2_rows), ("RULES v1", v1_rows),
                   ("untilted control", ctrl_rows)):
        r = rr[10.0]
        say(f"    {nm:20s} @10bps OOS {r['CAGR_OOS']:7.2%} / {r['Sharpe_OOS']:6.3f} / "
            f"{r['MaxDD_OOS']:7.2%}")
    say(f"    {'SPY':20s}        OOS {srow['CAGR_OOS']:7.2%} / {srow['Sharpe_OOS']:6.3f} / "
        f"{srow['MaxDD_OOS']:7.2%}")
    say("")
    say("  IS -> OOS sign stability of the leg-(c) tilt (does the tilt keep its direction?):")
    for kn in LEGC:
        g = real[(real.cost == 10.0) & (real.key == kn) & (real.dir == "NEG")]
        say(f"    {kn:9s} NEG  mean dSharpe IS {g.dSharpe_IS.mean():+.4f} -> "
            f"OOS {g.dSharpe_OOS.mean():+.4f}   (sign holds "
            f"{int((np.sign(g.dSharpe_IS) == np.sign(g.dSharpe_OOS)).sum())}/{len(g)})")
    say("")

    # ------------------------------------------------------- Q6 the placebo, and the binding leg
    say("=" * 112)
    say("Q6  THE PLACEBO.  MCAP = PRICE composed with diag(s): a per-name constant multiplier,")
    say("    which is EXACTLY idea 197's px -> px*diag(c) operator.  So the question 'does the")
    say("    SIZE information matter' has an exact placebo: permute the share counts across")
    say("    names, destroying the name<->shares link while keeping the multiplier distribution.")
    say(f"    {B_NULL} permutations, NEG direction, all {len(MS)} strengths, 10 bps.")
    say("")
    sv = shares.reindex(px.columns).values
    plac = []
    for j in range(B_NULL):
        rg = np.random.default_rng(90000 + j)
        pv = rg.permutation(sv)
        SP = pd.DataFrame(np.tile(pv, (len(px), 1)), index=px.index,
                          columns=px.columns).where(px.notna())
        kp = rankpct(px * SP)
        for m in MS:
            r0, trn = run(comp - m * kp)
            rw = full_row(r0 - trn * 10.0 / 1e4)
            plac.append(dict(seed=j, m=m, dSharpe_F=rw["Sharpe_F"] - ctrl_rows[10.0]["Sharpe_F"],
                             dSharpe_OOS=rw["Sharpe_OOS"] - ctrl_rows[10.0]["Sharpe_OOS"],
                             Sharpe_F=rw["Sharpe_F"], MaxDD_F=rw["MaxDD_F"]))
    P = pd.DataFrame(plac)
    P.to_csv(OUT / f"{STEM}.placebo.csv", index=False)
    real10 = real[(real.cost == 10.0) & (real.dir == "NEG")]
    say(f"  {'m':>5s} {'REAL MCAP':>10s} | {'placebo mean':>13s} {'sd':>7s} {'q05':>8s} "
        f"{'q95':>8s} {'max':>8s} | {'REAL > placebo max':>19s}")
    for m in MS:
        rv = float(real10[(real10.key == "MCAP") & (real10.m == m)].dSharpe_F.iloc[0])
        g = P[P.m == m].dSharpe_F
        say(f"  {m:5.2f} {rv:+10.4f} | {g.mean():+13.4f} {g.std(ddof=1):7.4f} "
            f"{g.quantile(0.05):+8.4f} {g.quantile(0.95):+8.4f} {g.max():+8.4f} | "
            f"{str(bool(rv > g.max())):>19s}")
    pm, pr_real = float(P.dSharpe_F.mean()), float(real10[real10.key == "MCAP"].dSharpe_F.mean())
    say(f"  pooled: REAL {pr_real:+.4f}, placebo {pm:+.4f}  ->  the placebo reproduces "
        f"{pm/pr_real:.1%} of leg (c)'s tilt; the SIZE information is the remaining "
        f"{1-pm/pr_real:.1%}.")
    say("")
    say("  4b BINDING LEG over all 193 arms at 10 bps (which of the five bars each arm fails):")
    a10 = A[A.cost == 10.0]
    legs = {"Sharpe_H1 <= SPY": a10.Sharpe_H1 <= srow["Sharpe_H1"],
            "Sharpe_H2 <= SPY": a10.Sharpe_H2 <= srow["Sharpe_H2"],
            "Sharpe_OOS <= SPY": a10.Sharpe_OOS <= srow["Sharpe_OOS"],
            f"MaxDD < {DELTA:.2f}x SPY ({DELTA*srow['MaxDD_F']:.2%})":
                a10.MaxDD_F < DELTA * srow["MaxDD_F"],
            f"CAGR < {PHI:.2f}x SPY ({PHI*srow['CAGR_F']:.2%})": a10.CAGR_F < PHI * srow["CAGR_F"]}
    for nm, msk in legs.items():
        say(f"    {nm:38s} fails {int(msk.sum()):4d} / {len(a10)}")
    orc = a10[a10.key == "FWDRET"]
    say(f"    the pure ORACLE key FWDRET (rank of realised forward return) passes 4b on "
        f"{int(orc.pass4b.sum())} of its {len(orc)} arms.")
    say("")

    # ------------------------------------------------------------------------------ predictions
    say("=" * 112)
    say("PRE-REGISTERED PREDICTIONS, SCORED")
    say("")
    mc = float(mn.get("MCAP", np.nan))
    pr = float(mn.get("PRICE", np.nan))
    sh = float(mn.get("SHARES", np.nan))
    band10 = float(np.nanmean([nb.get(("NEG", m), np.nan) for m in MS]))
    ic_mc = float(tab.loc["MCAP", "abs_IC"])
    ic_pr = float(tab.loc["PRICE", "abs_IC"])
    gates = max(g1, g4, rel)
    say(f"  P1 gates                        G1 {g1:.3e} G4 {g4:.3e} G3 {rel:.3e} "
        f"G2 {max(d1,d2):.3e} (tol {REPRO_TOL:.0e})   "
        f"{'PASS' if gates < 1e-12 and max(d1,d2) < REPRO_TOL else 'FAIL'}")
    say(f"  P2 MCAP/NEG positive and clears its null band   {mc:+.4f} vs band {band10:.4f}   "
        f"{'HIT' if mc > band10 else 'MISS'}")
    say(f"  P3 MCAP leaks more than PRICE and pays more     |IC| {ic_mc:.4f} vs {ic_pr:.4f}, "
        f"dS {mc:+.4f} vs {pr:+.4f}   "
        f"{'HIT' if (ic_mc > ic_pr and mc > pr) else 'MISS'}")
    say(f"  P4 SHARES alone carries < half of MCAP          {sh:+.4f} / {mc:+.4f} = "
        f"{sh/mc if mc else float('nan'):.3f}   "
        f"{'HIT' if (mc > 0 and sh < 0.5 * mc) else 'MISS'}")
    say(f"  P5 the leak law survives leg (c)                rho {rho_all:+.3f} (record-only "
        f"{rho_rec:+.3f})   {'HIT' if rho_all >= 0.70 else 'MISS'}")
    both10 = int((A[(A.cost == 10.0) & (A.klass == 'legc')].pass4a
                  & A[(A.cost == 10.0) & (A.klass == 'legc')].pass4b).sum())
    wl = W[(W.cost == 10.0) & (W.menu == "LEGC")].iloc[0]
    say(f"  P6 no leg-(c) BOTH pass at 10 bps and the LEGC rule-8 pick loses to RULES v2 OOS   "
        f"BOTH {both10}, beats v2 {wl.beats_v2_OOS}   "
        f"{'HIT' if (both10 == 0 and not wl.beats_v2_OOS) else 'MISS'}")
    say("")
    say(f"done in {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_console) + "\n")


if __name__ == "__main__":
    main()
