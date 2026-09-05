#!/usr/bin/env python3
"""
IDEA 193 - is-PRICE/NEG-the-only-arm-that-is-both-large-and-helpful   (lane B, 2026-09-05)

QUESTION (from the queue)
------------------------
Idea 192 found 17 positive clearers among 288 arms and 12 of them are PRICE/NEG -- the same family
that carries idea 181's only selector win and idea 192's S1/S4 nominal gains; every one fails 4b on
drawdown (-21%..-28%) and every one lives on a current-constituent panel.  Pair this with idea
185's split/survivorship decomposition: re-run the 17 positive clearers with price replaced by
frozen-at-entry rank, dollar volume and market cap, and report whether ANY of them is still both
large and helpful.

WHAT THIS RUN IS
----------------
The 17 positive clearers live on exactly two panels: `broad` (9 arms) and `small` (8 arms); none is
on u56.  This run rebuilds idea 181's corpus-T machinery on those two panels (same base book, same
tilt form, same 20 matched null keys from the parent's own seed) and substitutes the PRICE key with
the three replacements the queue names, plus the two diagnostic decompositions that the substitution
turns out to require:

  published anchors (reproduction)   PRICE, MOM, R3                 -- carry all 17 clearers
  substitution 1 (queue)             FROZEN   price rank frozen at each name's own entry date
  substitution 2 (queue)             DVOL     20d mean dollar volume rank   [SMALL PANEL ONLY]
  substitution 3 (queue)             MCAP     ** PARK: needs local/Actions data **
  causal size/level proxy added      REBASED  px / entry price, i.e. total return since entry
  look-ahead decomposition (diag)    PXTERM   terminal adjusted price, held constant
                                     FWDRET   total return from t to the last bar

WHY THE TWO DIAGNOSTIC KEYS ARE HERE.  The panels are ADJUSTED closes (auto_adjust=True), so the
price series IS a total-return index.  That makes an exact identity true of every column:

        px[t]  ==  px[T] / TR(t -> T)             TR(t->T) = cumulative total return t..T

i.e. the published PRICE key is, to machine precision, `terminal price MINUS realised future total
return' in logs.  Neither term is knowable at t.  PXTERM and FWDRET are those two terms run as
their own arms so the published key's dSharpe can be attributed between them.  They are LOOK-AHEAD
BY CONSTRUCTION, are labelled `oracle` in every output, and are excluded from every selector in the
rule-8 walk-forward.  The identity itself is asserted numerically in the reproduction block.

TUNED PARAMETERS: exactly two, both inherited from idea 181 and reported in full -- the tilt
strength m in {0.20, 0.50, 1.00} and the direction in {POS, NEG}.  The KEY is a reported axis and
is never selected on outside the pre-registered rule-8 selectors.  Every grid point is written to
<stem>.arms.csv.

PRE-REGISTERED PREDICTIONS (written before any new number was read; all reported hit or miss)
  P1  The adjusted-price identity holds to <1e-10: PRICE is exactly terminal-price-minus-future-
      total-return, so a `price level' key is not implementable on this data at all.
  P2  FROZEN/NEG is LARGE and CLEARS on both panels -- freezing the rank at entry does not remove
      the look-ahead, it maximises it (the entry bar carries the whole sample's adjustment).
  P3  FWDRET/POS reproduces most of PRICE/NEG's dSharpe; PXTERM/NEG reproduces little of it.
      (The effect is the future-return term, not the terminal-level term.)
  P4  DVOL/NEG -- the one causal size/liquidity substitute available -- is NOT both clearing and
      positive at m=0.2 on the small panel.
  P5  REBASED/NEG (causal) is far smaller than PRICE/NEG on both panels.
  P6  ZERO causal arms are both clearing-and-positive AND 4b-passing (idea 192 found 0 of 288).
  P7  Rule 8: the causal-only selector S2 does not beat do-nothing S0 (ninth consecutive
      do-nothing win in this project).

CAVEATS
  * SURVIVORSHIP.  Both panels are CURRENT constituents (idea 54); the small panel additionally
    drops the 44 tickers with max_1d_move >= 1.0 (idea 186's screen), which is itself a
    survivorship-flavoured filter.  Every number below inherits that bias in one direction.
  * MCAP is PARKED, not run: no shares-outstanding series is cached in data/ and this sandbox has
    no internet.  The market-cap leg of the queue item is therefore unanswered here and is
    re-queued as its own idea.
  * DVOL exists only for the small panel (data/volume_small.csv.gz).  SPY carries no volume and is
    given the neutral rank 0.5 in the DVOL key only; the control book's SPY holding share is
    reported so the reader can see the size of that concession.
  * All rows are t+1 execution at 10 or 25 bps, derived from ONE 0 bps run via the engine's own
    cost identity (asserted exact).

Deterministic, standalone, no network.  Writes .arms.csv, .reproduction.csv, .decomp.csv,
.walkforward.csv, .console.txt, .result.md.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, load_volume, rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-05_is-PRICE-NEG-the-only-arm-that-is-both-large-and-helpful_B"
OUT = ROOT / "research" / "backtests"
T_STEM = "2026-09-05_does-a-null-column-change-any-published-verdict_cloud"          # idea 181
M_STEM = "2026-09-05_does-a-harmful-instrument-clear-more-often-than-a-helpful-one_B"  # idea 192

# --- inherited verbatim from idea 181 so the null bands reproduce -------------------------------
SEED, B_NULL = 181, 20
N, GROSS, FREQ, MAXVOL = 20, 0.75, "W", 0.60
MS = [0.20, 0.50, 1.00]
DIRS = {"POS": 1.0, "NEG": -1.0}
COSTS = [10.0, 25.0]
IS_END = pd.Timestamp("2016-12-31")
OOS_LO = IS_END + pd.Timedelta(days=1)
PANEL_IX = {"u56": 0, "broad": 1, "small": 2}     # parent's panel order -> its per-panel seed

ANCHORS = ["PRICE", "MOM", "R3"]                  # published keys that carry all 17 clearers
CAUSAL = ["MOM", "R3", "REBASED", "DVOL", "VOLSH"]   # implementable without future information
LEAKCTL = ["DVOLT"]                               # liquidity control that removes the R1 factor
# Return-based keys are the only ones the R1 factor cancels out of: px[t]/px[t-k] on adjusted
# closes IS the raw total return over [t-k, t], knowable at t.  Every LEVEL-like key (PRICE,
# FROZEN, DVOL, VOLSH) keeps a factor that is only known at T.
LEAKFREE = ["MOM", "R3", "REBASED"]
ORACLE = ["PXTERM", "FWDRET"]                     # look-ahead by construction; diagnostics only
PRICELEVEL = ["PRICE", "FROZEN"]                  # adjusted-price LEVEL keys (see R1 identity)

_console: list[str] = []


def say(*a):
    line = " ".join(str(x) for x in a)
    print(line)
    _console.append(line)


def rankpct(df):
    return df.rank(axis=1, pct=True)


def spearman(a, b):
    ra, rb = pd.Series(a).rank(), pd.Series(b).rank()
    if ra.std(ddof=0) == 0 or rb.std(ddof=0) == 0:
        return np.nan
    return float(np.corrcoef(ra.values, rb.values)[0, 1])


# ------------------------------------------------------------------ vectorised engine equivalent
def fast_backtest(prices, weights, cost_bps=0.0, freq=FREQ):
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
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=idx), "turnover": pd.Series(turn, index=idx),
            "held": pd.DataFrame(held, index=idx, columns=prices.columns)}


# ------------------------------------------------------------------------------ panels and keys
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    say(f"small panel: dropped {len(bad)} tickers with max_1d_move >= 1.0; "
        f"{len(keep) - 1} names + SPY benchmark remain")
    return px[keep]


def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (rankpct(mom) + rankpct(r6) + rankpct(r3)) / 3


def first_valid_row(px):
    """Per column, the first non-NaN value, broadcast over every date the column is live."""
    fv = px.apply(lambda s: s.loc[s.first_valid_index()] if s.first_valid_index() is not None
                  else np.nan)
    out = pd.DataFrame(np.tile(fv.values, (len(px), 1)), index=px.index, columns=px.columns)
    return out.where(px.notna())


def last_valid_row(px):
    lv = px.apply(lambda s: s.loc[s.last_valid_index()] if s.last_valid_index() is not None
                  else np.nan)
    out = pd.DataFrame(np.tile(lv.values, (len(px), 1)), index=px.index, columns=px.columns)
    return out.where(px.notna())


def build_keys(px, panel, rng):
    """Idea 181's 5 real keys are not all needed; the 3 anchors that carry the 17 clearers are,
    plus the queue's substitutions, plus the two decomposition diagnostics, plus the parent's own
    20 matched null keys drawn in the parent's exact order so the bands reproduce."""
    entry = first_valid_row(px)
    term = last_valid_row(px)
    keys = {
        "PRICE":   rankpct(px),                                   # published
        "MOM":     rankpct(px.shift(21) / px.shift(252) - 1),     # published
        "R3":      rankpct(px / px.shift(63) - 1),                # published
        "FROZEN":  rankpct(entry),                                # queue substitution 1
        "REBASED": rankpct(px / entry),                           # causal level proxy
        "PXTERM":  rankpct(term),                                 # oracle diagnostic
        "FWDRET":  rankpct(term / px - 1),                         # oracle diagnostic
    }
    if panel == "small":
        vol = load_volume(small=True).reindex(index=px.index, columns=px.columns)
        # DVOL   = adjusted close x split-adjusted share volume (the natural construction)
        # DVOLT  = TERMINAL price x share volume: kills the time-varying TR(t->T) factor that the
        #          R1 identity puts inside every adjusted close, so it cannot carry that leak
        # VOLSH  = share volume alone: no price term at all
        for nm, raw in (("DVOL", px * vol), ("DVOLT", term * vol), ("VOLSH", vol)):
            k = rankpct(raw.rolling(20).mean())
            if "SPY" in k.columns:
                k["SPY"] = 0.5                   # SPY carries no volume; neutral, see caveats
            keys[nm] = k
    # --- parent's null keys, same draw order, same per-panel seed
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
    o = win(r, lo=OOS_LO)
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


# ============================================================================================ run
def main():
    t0 = time.time()
    say("=" * 100)
    say("IDEA 193  is-PRICE/NEG-the-only-arm-that-is-both-large-and-helpful   (lane B, 2026-09-05)")
    say("=" * 100)

    panels = {"broad": load_universe(broad=True), "small": small_panel()}
    repro, arms, decomp = [], [], []

    # ---------------------------------------------------------------- R0: published RULES v1 anchor
    pu = load_universe()
    ru = backtest(pu, rules_v1_weights(pu), cost_bps=10.0, freq="W")["returns"].loc[pu.index[260]:]
    mu = metrics(ru)
    say(f"\nR0  RULES v1 on u56 @10bps: {mu['CAGR']:.5%} / {mu['Sharpe']:.5f} / {mu['MaxDD']:.5%}"
        f"   (published 6.45305% / 0.66418 / -13.82780%)")
    repro.append(dict(check="R0_rules_v1_u56", value=mu["Sharpe"], target=0.66418,
                      err=abs(mu["Sharpe"] - 0.66418)))

    for pn, px in panels.items():
        start = px.index[260]
        pseed = SEED + 1000 * (1 + PANEL_IX[pn])
        keys = build_keys(px, pn, np.random.default_rng(pseed))
        comp = composite(px)
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        elig = (px > px.rolling(200).mean()) & (vol20 < MAXVOL)
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        srow = full_row(spy)
        say(f"\npanel {pn}: {px.shape[1]} cols, sample {start.date()}..{px.index[-1].date()}, "
            f"SPY {srow['CAGR_F']:.2%}/{srow['Sharpe_F']:.3f}/{srow['MaxDD_F']:.2%} "
            f"(H1 {srow['Sharpe_H1']:.3f} / H2 {srow['Sharpe_H2']:.3f} / OOS {srow['Sharpe_OOS']:.3f})")

        # ------------------------------------------------- R1: the adjusted-price identity (P1)
        tr = px.iloc[-1] / px                      # claimed == cumulative total return t -> T
        cum = (1 + px.pct_change().fillna(0.0)).cumprod()
        tr2 = cum.iloc[-1] / cum
        ident = float(np.nanmax(np.abs((tr - tr2).values)))
        say(f"R1  adjusted-price identity  px[T]/px[t] == cumulative total return t->T : "
            f"max abs err {ident:.3e}")
        repro.append(dict(check=f"R1_identity_{pn}", value=ident, target=0.0, err=ident))

        def run(score):
            rk = score.where(elig).rank(axis=1, ascending=False)
            w = (rk <= N).astype(float) * (GROSS / N)
            res = fast_backtest(px, w, cost_bps=0.0)
            return res["returns"].loc[start:], res["turnover"].loc[start:], res["held"]

        # ------------------------------------------------- R2: fast == engine, and cost identity
        c0, ct, cheld = run(comp)
        eng = backtest(px, (comp.where(elig).rank(axis=1, ascending=False) <= N).astype(float)
                       * (GROSS / N), cost_bps=0.0, freq=FREQ)
        e2 = float((eng["returns"].loc[start:] - c0).abs().max())
        say(f"R2  fast_backtest == engine.backtest on the control book : max abs err {e2:.3e}")
        repro.append(dict(check=f"R2_engine_{pn}", value=e2, target=0.0, err=e2))
        eng10 = backtest(px, (comp.where(elig).rank(axis=1, ascending=False) <= N).astype(float)
                         * (GROSS / N), cost_bps=10.0, freq=FREQ)["returns"].loc[start:]
        e3 = float((eng10 - (c0 - ct * 10.0 / 1e4)).abs().max())
        say(f"R3  cost identity  r_c == r_0 - turnover*c/1e4 : max abs err {e3:.3e}")
        repro.append(dict(check=f"R3_cost_{pn}", value=e3, target=0.0, err=e3))
        if pn == "small":
            spy_share = float(cheld.loc[start:, "SPY"].mean() / cheld.loc[start:].sum(axis=1).mean())
            say(f"    control book's mean SPY weight share on the small panel: {spy_share:.4%}")

        base = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq="W")
        b0, bt = base["returns"].loc[start:], base["turnover"].loc[start:]
        base_rows = {c: full_row(b0 - bt * c / 1e4) for c in COSTS}
        ctrl_rows = {c: full_row(c0 - ct * c / 1e4) for c in COSTS}
        for c in COSTS:
            r = dict(panel=pn, key="CONTROL", klass="control", published=False,
                     dir="-", m=0.0, cost=c, turnover_yr=float(ct.sum() / (len(ct) / 252)),
                     dSharpe_F=0.0, dSharpe_IS=0.0, dSharpe_OOS=0.0)
            r.update(ctrl_rows[c])
            r["pass4a"] = pass4a(r, base_rows[c])
            r["pass4b"] = pass4b(r, srow)
            arms.append(r)

        # ------------------------------------------------------------------------ the whole grid
        for kn, kv in keys.items():
            klass = ("nullkey" if kn.startswith("NULL") else
                     "oracle" if kn in ORACLE else
                     "leakctl" if kn in LEAKCTL else
                     "pricelevel" if kn in PRICELEVEL else "causal")
            for dn, dv in DIRS.items():
                for m in MS:
                    r0, trn, _ = run(comp + dv * m * kv)
                    for c in COSTS:
                        rr = dict(panel=pn, key=kn, klass=klass, published=kn in ANCHORS,
                                  dir=dn, m=m, cost=c,
                                  turnover_yr=float(trn.sum() / (len(trn) / 252)))
                        rr.update(full_row(r0 - trn * c / 1e4))
                        for tag in ("F", "IS", "OOS"):
                            rr[f"dSharpe_{tag}"] = rr[f"Sharpe_{tag}"] - ctrl_rows[c][f"Sharpe_{tag}"]
                        rr["pass4a"] = pass4a(rr, base_rows[c])
                        rr["pass4b"] = pass4b(rr, srow)
                        arms.append(rr)

        # ----------------------------------------------- leak measurement: how much of PRICE is FWDRET
        dates = px.index[260::63]

        def rho_of(x, y):
            vals = []
            for d in dates:
                a, b = keys[x].loc[d], keys[y].loc[d]
                ok = a.notna() & b.notna()
                if ok.sum() > 10:
                    vals.append(spearman(a[ok].values, b[ok].values))
            return float(np.nanmean(vals)), len(vals)

        pairs = [("PRICE", o) for o in ("FWDRET", "PXTERM", "FROZEN", "REBASED", "DVOL")]
        # how much future information does each LIQUIDITY key carry?  (the R1 leak channel)
        pairs += [(k, "FWDRET") for k in ("DVOL", "DVOLT", "VOLSH")]
        pairs += [("DVOL", "DVOLT"), ("DVOL", "VOLSH")]
        for x, y in pairs:
            if x not in keys or y not in keys:
                continue
            r, n = rho_of(x, y)
            decomp.append(dict(panel=pn, pair=f"{x}~{y}", rho=r, n_dates=n))

    A = pd.DataFrame(arms)
    A["absd"] = A["dSharpe_F"].abs()
    # ------------------------------------------------ the clause: |d| > max |d| over 20 null keys
    A["band"] = np.nan
    A["clears"] = False
    A["IS_band"] = np.nan
    A["IS_clears"] = False
    for (pn, dn, m, c), sub in A[A.klass != "control"].groupby(["panel", "dir", "m", "cost"],
                                                              sort=False):
        nb = sub[sub.klass == "nullkey"]
        thF = float(nb["dSharpe_F"].abs().max())
        thI = float(nb["dSharpe_IS"].abs().max())
        ix = sub.index
        A.loc[ix, "band"] = thF
        A.loc[ix, "IS_band"] = thI
        A.loc[ix, "clears"] = A.loc[ix, "dSharpe_F"].abs() > thF
        A.loc[ix, "IS_clears"] = A.loc[ix, "dSharpe_IS"].abs() > thI
    A["clears"] = A["clears"].astype(bool)
    A["IS_clears"] = A["IS_clears"].astype(bool)
    A.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    say(f"\ngrid: {len(A)} rows ({time.time() - t0:.0f}s) -> {STEM}.arms.csv")

    # ============================================================ R4/R5 reproduction vs idea 181
    say("\n" + "=" * 100)
    say("REPRODUCTION of idea 181's published grid (broad + small, PRICE/MOM/R3, all dirs, all m)")
    say("=" * 100)
    gT = pd.read_csv(OUT / f"{T_STEM}.grid.csv")
    cT = pd.read_csv(OUT / f"{T_STEM}.clause.csv")
    pub = gT[(gT.kind == "real") & (gT.panel.isin(["broad", "small"])) & (gT.key.isin(ANCHORS))]
    mine = A[A["published"] & (A.panel.isin(["broad", "small"]))]
    j = pub.merge(mine, left_on=["panel", "key", "dir", "m", "cost"],
                  right_on=["panel", "key", "dir", "m", "cost"], suffixes=("_pub", "_new"))
    e4 = float((j["dSharpe_F_pub"] - j["dSharpe_F_new"]).abs().max())
    say(f"R4  {len(j)} published (panel,key,dir,m,cost) cells rebuilt from scratch: "
        f"max |dSharpe - published| = {e4:.3e}")
    repro.append(dict(check="R4_grid_dSharpe", value=e4, target=0.0, err=e4))

    cF = cT[(cT.window == "F") & (cT.panel.isin(["broad", "small"]))]
    band_pub = cF.groupby(["panel", "dir", "m", "cost"])["null_max"].first().rename("null_max_pub")
    band_new = A[A.klass != "control"].groupby(["panel", "dir", "m", "cost"])["band"].first()
    bj = pd.concat([band_pub, band_new.rename("null_max_new")], axis=1).dropna()
    e5 = float((bj["null_max_pub"] - bj["null_max_new"]).abs().max())
    say(f"R5  {len(bj)} matched-null bands rebuilt from the parent's own seed: "
        f"max |band - published| = {e5:.3e}")
    repro.append(dict(check="R5_null_band", value=e5, target=0.0, err=e5))

    cj = cF.merge(mine, on=["panel", "dir", "m", "cost", "key"], suffixes=("_pub", ""))
    mism = int((cj["clears_pub"].astype(int) != cj["clears"].astype(int)).sum()) \
        if "clears_pub" in cj.columns else int((cj["clears_x"].astype(int) != cj["clears_y"].astype(int)).sum())
    say(f"R6  clause verdict mismatches on those {len(cj)} published cells: {mism}")
    repro.append(dict(check="R6_clause_mismatch", value=float(mism), target=0.0, err=float(mism)))

    R = pd.DataFrame(repro)
    R.to_csv(OUT / f"{STEM}.reproduction.csv", index=False)
    say("\n" + R.to_string(index=False, float_format=lambda x: f"{x:.3e}"))
    ok = bool((R["err"].iloc[1:] < 1e-8).all() and R["err"].iloc[0] < 5e-5)
    say(f"\nreproduction {'PASSES' if ok else 'FAILS'} -- "
        f"{'proceeding to new numbers' if ok else 'STOP'}")

    # ============================================================ Q1: is anything large AND helpful
    say("\n" + "=" * 100)
    say("Q1  the queue's question: with price replaced, is ANY arm still both LARGE and HELPFUL?")
    say("    LARGE  = clears the matched-null clause (|dSharpe| > max over 20 null keys)")
    say("    HELPFUL= dSharpe > 0 vs the untilted control at the same cost rung")
    say("=" * 100)
    real = A[~A.klass.isin(["nullkey", "control"])].copy()
    real["LH"] = real["clears"].astype(bool) & (real["dSharpe_F"] > 0)
    tab = (real.groupby(["klass", "key", "panel"])["LH"]
           .agg(lambda s: f"{int(s.sum())}/{len(s)}").unstack("panel"))
    say("\n  clearing-AND-positive count per key (out of 12 = 2 dirs x 3 m x 2 cost rungs):")
    say(tab.to_string())
    say("\n  mean dSharpe_F by key and direction (full sample, both rungs, all m):")
    say(real.pivot_table(index=["panel", "key"], columns="dir", values="dSharpe_F")
        .to_string(float_format=lambda x: f"{x:+.4f}"))

    lh = real[real.LH].sort_values("dSharpe_F", ascending=False)
    say(f"\n  ALL {len(lh)} clearing-and-positive arms in this run:")
    say(lh[["panel", "key", "klass", "dir", "m", "cost", "dSharpe_F", "band", "Sharpe_F",
            "CAGR_F", "MaxDD_F", "Sharpe_OOS", "pass4a", "pass4b"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\n  of those, CAUSAL (implementable) arms: {int((lh.klass == 'causal').sum())}")
    say(f"  of those, passing 4b:                  {int(lh['pass4b'].sum())}")
    say(f"  of those, CAUSAL and passing 4b:       "
        f"{int(lh[lh.klass == 'causal']['pass4b'].sum())}")

    # ---------------------------------------------------- Q2: attribution of PRICE/NEG's dSharpe
    say("\n" + "=" * 100)
    say("Q2  where does PRICE/NEG's dSharpe come from?  (log identity: PRICE = PXTERM - FWDRET)")
    say("=" * 100)
    D = pd.DataFrame(decomp)
    say("\n  mean cross-sectional Spearman between the published key and its parts "
        "(quarterly samples):")
    say(D.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    att = []
    for pn in panels:
        for m in MS:
            for c in COSTS:
                def g(k, d):
                    s = real[(real.panel == pn) & (real.key == k) & (real.dir == d)
                             & (real.m == m) & (real.cost == c)]["dSharpe_F"]
                    return float(s.iloc[0]) if len(s) else np.nan
                p = g("PRICE", "NEG")
                att.append(dict(panel=pn, m=m, cost=c, PRICE_NEG=p,
                                FWDRET_POS=g("FWDRET", "POS"), PXTERM_NEG=g("PXTERM", "NEG"),
                                FROZEN_NEG=g("FROZEN", "NEG"), REBASED_NEG=g("REBASED", "NEG"),
                                DVOL_NEG=g("DVOL", "NEG"), DVOLT_NEG=g("DVOLT", "NEG"),
                                VOLSH_NEG=g("VOLSH", "NEG"),
                                share_fwd=g("FWDRET", "POS") / p if p else np.nan,
                                share_term=g("PXTERM", "NEG") / p if p else np.nan))
    AT = pd.DataFrame(att)
    AT.to_csv(OUT / f"{STEM}.decomp.csv", index=False)
    say("\n  dSharpe_F of the published arm and of each replacement, every grid point:")
    say(AT.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    say("\n  means over the 12 grid points:")
    say(AT[["PRICE_NEG", "FWDRET_POS", "PXTERM_NEG", "FROZEN_NEG", "REBASED_NEG", "DVOL_NEG",
            "DVOLT_NEG", "VOLSH_NEG", "share_fwd", "share_term"]]
        .mean().to_string(float_format=lambda x: f"{x:+.4f}"))

    # ------------------------------- Q2b: is the liquidity tilt itself an adjusted-price artefact?
    say("\n" + "=" * 100)
    say("Q2b LIQUIDITY LEAK CONTROL.  DVOL uses the ADJUSTED close, which by R1 carries the")
    say("    TR(t->T) factor.  DVOLT swaps in each name's TERMINAL price (kills that factor);")
    say("    VOLSH drops price entirely.  If the tilt is a leak, it dies in both.")
    say("=" * 100)
    liq = real[(real.panel == "small") & real.key.isin(["DVOL", "DVOLT", "VOLSH"])]
    say(liq[["key", "klass", "dir", "m", "cost", "dSharpe_F", "band", "clears", "Sharpe_F",
             "CAGR_F", "MaxDD_F", "Sharpe_OOS", "turnover_yr", "pass4a", "pass4b"]]
        .sort_values(["key", "dir", "m", "cost"])
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n  clearing-and-positive count, liquidity family (out of 12 each):")
    say(liq.groupby("key")["LH"].agg(lambda s: f"{int(s.sum())}/{len(s)}").to_string())

    # ============================================================ Q3: rule 8 walk-forward
    say("\n" + "=" * 100)
    say("Q3  RULE 8 WALK-FORWARD.  Key chosen on data <= 2016-12-31 only; 2017-2026 read once.")
    say("    12 cells = 2 panels x 3 m x 2 cost rungs.  Oracle keys are excluded from every")
    say("    selector (they are not implementable); ORACLE-OOS is the ceiling, not a candidate.")
    say("=" * 100)
    pool_all = ANCHORS + ["FROZEN", "REBASED", "DVOL", "VOLSH"]
    wf = []
    for pn in panels:
        sub_all = real[real.panel == pn]
        ctrl = A[(A.panel == pn) & (A.klass == "control")]
        for m in MS:
            for c in COSTS:
                cand = sub_all[(sub_all.m == m) & (sub_all.cost == c)
                               & (sub_all.key.isin(pool_all))]
                cz = ctrl[ctrl.cost == c].iloc[0]
                base_oos = float(cz["Sharpe_OOS"])
                if not len(cand):
                    continue

                def pick(df, tag):
                    if not len(df):
                        return dict(selector=tag, pick="ABSTAIN", OOS_Sharpe=base_oos,
                                    OOS_CAGR=float(cz["CAGR_OOS"]), OOS_MaxDD=float(cz["MaxDD_OOS"]))
                    r = df.loc[df["dSharpe_IS"].idxmax()]
                    return dict(selector=tag, pick=f"{r['key']}/{r['dir']}",
                                OOS_Sharpe=float(r["Sharpe_OOS"]), OOS_CAGR=float(r["CAGR_OOS"]),
                                OOS_MaxDD=float(r["MaxDD_OOS"]))

                rows = [dict(selector="S0 do-nothing", pick="-", OOS_Sharpe=base_oos,
                             OOS_CAGR=float(cz["CAGR_OOS"]), OOS_MaxDD=float(cz["MaxDD_OOS"])),
                        pick(cand, "S1 IS-argmax (all)"),
                        pick(cand[cand.klass == "causal"], "S2 IS-argmax (causal only)"),
                        pick(cand[cand.key.isin(LEAKFREE)], "S2LF IS-argmax (leak-free) [post-hoc]"),
                        pick(cand[cand.IS_clears.astype(bool) & (cand.dSharpe_IS > 0)],
                             "S3 clause+positive"),
                        ]
                for kk, dd, tag in (("PRICE", "NEG", "C-PRICE/NEG"), ("DVOL", "NEG", "C-DVOL/NEG"),
                                    ("VOLSH", "NEG", "C-VOLSH/NEG"),
                                    ("REBASED", "NEG", "C-REBASED/NEG")):
                    s = sub_all[(sub_all.m == m) & (sub_all.cost == c)
                                & (sub_all.key == kk) & (sub_all.dir == dd)]
                    if len(s):
                        r = s.iloc[0]
                        rows.append(dict(selector=tag, pick=f"{kk}/{dd}",
                                         OOS_Sharpe=float(r["Sharpe_OOS"]),
                                         OOS_CAGR=float(r["CAGR_OOS"]),
                                         OOS_MaxDD=float(r["MaxDD_OOS"])))
                orc = cand.loc[cand["Sharpe_OOS"].idxmax()]
                rows.append(dict(selector="ORACLE-OOS", pick=f"{orc['key']}/{orc['dir']}",
                                 OOS_Sharpe=float(orc["Sharpe_OOS"]),
                                 OOS_CAGR=float(orc["CAGR_OOS"]),
                                 OOS_MaxDD=float(orc["MaxDD_OOS"])))
                for r in rows:
                    r.update(panel=pn, m=m, cost=c, dOOS=r["OOS_Sharpe"] - base_oos)
                    wf.append(r)
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say("\n  every walk-forward cell:")
    say(W[["panel", "m", "cost", "selector", "pick", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "dOOS"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n  mean over the 12 cells, and paired t vs S0:")
    piv = W.pivot_table(index=["panel", "m", "cost"], columns="selector", values="OOS_Sharpe")
    out = []
    for s in piv.columns:
        d = (piv[s] - piv["S0 do-nothing"]).dropna()
        t = float(d.mean() / (d.std(ddof=1) / np.sqrt(len(d)))) if len(d) > 1 and d.std(ddof=1) > 0 else np.nan
        out.append(dict(selector=s, mean_OOS_Sharpe=float(piv[s].mean()), dOOS=float(d.mean()),
                        t=t, wins=int((d > 0).sum()), losses=int((d < 0).sum()), n=int(len(d))))
    SW = pd.DataFrame(out).sort_values("mean_OOS_Sharpe", ascending=False)
    say(SW.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    say("  NOTE: n=6 rows are SMALL-PANEL-ONLY selectors (DVOL/VOLSH do not exist on broad);")
    say("        their mean is not comparable to the n=12 rows.  Small-panel-only means:")
    ps = piv.loc["small"]
    say(ps.mean().sort_values(ascending=False).to_string(float_format=lambda x: f"{x:+.4f}"))

    # benchmarks over the same OOS window
    say("\n  benchmarks over the same OOS window (2017-01-01 ->):")
    for pn, px in panels.items():
        start = px.index[260]
        b = backtest(px, rules_v1_weights(px), cost_bps=10.0, freq="W")["returns"].loc[start:]
        mb, ms = metrics(win(b, lo=OOS_LO)), metrics(win(px["SPY"].pct_change().fillna(0).loc[start:], lo=OOS_LO))
        say(f"    {pn:6s} RULES v1 @10bps OOS {mb['CAGR']:.2%}/{mb['Sharpe']:.4f}/{mb['MaxDD']:.2%}"
            f"   SPY OOS {ms['CAGR']:.2%}/{ms['Sharpe']:.4f}/{ms['MaxDD']:.2%}")

    # ============================================================ KEEP paths over the whole grid
    say("\n" + "=" * 100)
    say("BOTH KEEP PATHS over every real arm in the run")
    say("=" * 100)
    say(real.pivot_table(index=["panel", "klass"], values=["pass4a", "pass4b"],
                         aggfunc=lambda s: f"{int(s.sum())}/{len(s)}").to_string())
    kb = real[real.pass4b]
    say(f"\n  4b passes: {len(kb)} of {len(real)} real arms")
    if len(kb):
        say(kb[["panel", "key", "klass", "dir", "m", "cost", "CAGR_F", "Sharpe_F", "MaxDD_F",
                "Sharpe_H1", "Sharpe_H2", "Sharpe_OOS", "clears", "dSharpe_F"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------------ predictions scorecard
    say("\n" + "=" * 100)
    say("PRE-REGISTERED PREDICTIONS")
    say("=" * 100)
    idm = max(r["err"] for r in repro if r["check"].startswith("R1"))
    fz = real[(real.key == "FROZEN") & (real.dir == "NEG")]
    p2 = bool(fz["clears"].all() and (fz["dSharpe_F"] > 0).all())
    sf = AT["share_fwd"].mean()
    st = AT["share_term"].mean()
    p3 = bool(sf > 0.5 and abs(st) < 0.5)
    dv = real[(real.key == "DVOL") & (real.dir == "NEG") & (real.m == 0.20)]
    p4 = bool(not (dv["clears"] & (dv["dSharpe_F"] > 0)).any())
    rb = real[(real.key == "REBASED") & (real.dir == "NEG")]["dSharpe_F"].abs().mean()
    pr = real[(real.key == "PRICE") & (real.dir == "NEG")]["dSharpe_F"].abs().mean()
    p5 = bool(rb < 0.5 * pr)
    caus_lh = lh[lh.klass == "causal"]
    p6 = bool(len(caus_lh[caus_lh.pass4b]) == 0)
    s2 = SW[SW.selector == "S2 IS-argmax (causal only)"]
    p7 = bool(len(s2) and float(s2["dOOS"].iloc[0]) <= 0)
    preds = [
        ("P1 adjusted-price identity holds < 1e-10", idm < 1e-10, f"max err {idm:.2e}"),
        ("P2 FROZEN/NEG is large and clears on both panels", p2,
         f"{int(fz['clears'].sum())}/{len(fz)} clear, mean d {fz['dSharpe_F'].mean():+.4f}"),
        ("P3 FWDRET/POS carries most of PRICE/NEG, PXTERM/NEG little", p3,
         f"share_fwd {sf:+.3f}, share_term {st:+.3f}"),
        ("P4 DVOL/NEG at m=0.2 is NOT clearing-and-positive", p4,
         f"{int((dv['clears'] & (dv['dSharpe_F'] > 0)).sum())} of {len(dv)}"),
        ("P5 REBASED/NEG much smaller than PRICE/NEG", p5, f"{rb:.4f} vs {pr:.4f}"),
        ("P6 zero CAUSAL clearing-and-positive arms pass 4b", p6, f"{len(caus_lh[caus_lh.pass4b])}"),
        ("P7 causal selector S2 does not beat do-nothing", p7,
         f"dOOS {float(s2['dOOS'].iloc[0]):+.4f}" if len(s2) else "n/a"),
    ]
    for nm, hit, note in preds:
        say(f"  {'HIT ' if hit else 'MISS'}  {nm:52s} [{note}]")
    say(f"\n  {sum(1 for _, h, _ in preds if h)} of {len(preds)} predictions HIT")
    say("\n  POST-HOC (declared as such): the DVOLT / VOLSH liquidity-leak controls of Q2b were")
    say("  added AFTER P4's miss was read.  They are a control on a new result, not a")
    say("  pre-registered prediction, and are labelled so everywhere they appear.")
    say(f"\ntotal runtime {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_console))


if __name__ == "__main__":
    main()
