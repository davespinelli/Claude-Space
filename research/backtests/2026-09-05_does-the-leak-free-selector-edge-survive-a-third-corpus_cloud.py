#!/usr/bin/env python3
"""IDEA 196  does-the-leak-free-selector-edge-survive-a-third-corpus   (cloud, 2026-09-05)

THE QUESTION
------------
Idea 193's rule-8 walk-forward found S2LF -- the in-sample argmax restricted to the three
LEAK-FREE keys (MOM, R3, REBASED) -- beating the do-nothing control by +0.1370 mean OOS
Sharpe (t +2.19 on 6 cost-collapsed cells, 11 wins / 1 loss).  That was the first non-zero
do-nothing loss in nine consecutive project runs (ideas 110/132/151/166/171/174/175/186 all
found an IS-fitted selector losing to doing nothing).

But it rested on TWO panels (broad136, small483) and a 3-key pool, i.e. 12 raw cells that
collapse to 6.  Six paired observations cannot distinguish a real selector edge from a
two-panel accident.  This run re-prices the IDENTICAL three keys, the identical tilt
construction and the identical selector protocol on a THIRD corpus: idea 175's 115 books,
which contains NO broad136 at all and reaches the small panel only through sub-draws.

  replicates  = S2LF's paired dOOS is positive and significant on the 115-book corpus
  accident    = it is zero or negative, or it is carried by one family

THE CORPUS (rebuilt byte-identically from idea 175's own seeds)
---------------------------------------------------------------
  3 fixed books : SMALL439 (the 483-name sub-$2B panel less the 44 max_1d_move >= 1.0
                  tickers), U56 (universe.json single names), ETF36 (universe.json ETFs)
  112 sub-panel draws : SMALL k in {20,40,80} x 16, U56 k in {20,40} x 16,
                        ETF k in {12,24} x 16, seeds 175_500 / 175_600 / 175_700
  -> 115 books, the pairing unit.  Disjoint from idea 193's (broad136, small483) pair.

THE ARMS (inherited verbatim from idea 193, which inherited them from idea 181)
--------------------------------------------------------------------------------
  base book   : idea 2's candidate -- composite (MOM/R6/R3 rank mean, NO vol scaler),
                200d & vol20<0.60 eligibility, top n=20 equal weight, gross 0.75,
                WEEKLY, t+1 execution
  tilted book : rank on  comp + dir * m * rankpct(key)
  keys        : MOM = px[t-21]/px[t-252]-1        (published)
                R3  = px[t]/px[t-63]-1            (published)
                REBASED = px[t]/px[entry]         (total return since the name's first bar)
                All three are RATIO keys: by idea 193's R1 identity the auto-adjustment
                factor cancels, so none reads the level of an adjusted price and none is
                contaminated with future information.  PRICE, FROZEN, DVOL, VOLSH and the
                two oracles are deliberately ABSENT -- this run tests only what survived.
  dirs        : POS, NEG                          TUNED PARAMETER 1 (2 values, all reported)
  m           : 0.20, 0.50, 1.00                  TUNED PARAMETER 2 (3 values, all reported)
  costs       : 10 and 25 bps, both derived EXACTLY from one 0 bps run via the engine's own
                turnover series (a reported axis, not a tuned one)

  115 books x (1 control + 3 keys x 2 dirs x 3 m) = 115 x 19 = 2185 backtests -> 4370 rows.

RULE 8 (PROTOCOL clause 8, required)
------------------------------------
  Key/dir chosen on data <= 2016-12-31 ONLY (argmax of IS dSharpe vs the same book's
  untilted control), 2017-01-01 -> read ONCE.  690 cells = 115 books x 3 m x 2 cost rungs.
  Selectors: S0 do-nothing (the untilted control), S2LF (the arm under test), RANDOM (a
  seeded uniform pick from the same 6-arm pool -- the control idea 173 showed is mandatory),
  the six per-arm CONSTANTS, and ORACLE-OOS as the unreachable ceiling.
  Paired against S0 book-by-book; reported per-cell (690), cost-collapsed (345, idea 193's
  own convention) and per family.

BOTH KEEP PATHS are evaluated on every one of the 4370 arm rows:
  4a  Sharpe > RULES v1 in BOTH halves and MaxDD no worse            (per-book baseline)
  4b  Sharpe > SPY in BOTH halves AND OOS, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's

PRE-REGISTERED PREDICTIONS (written before any number below was read)
---------------------------------------------------------------------
  P1  S2LF's paired dOOS on 115 books is POSITIVE but SMALLER than +0.1370.
  P2  S2LF does NOT beat RANDOM drawn from the same pool by a significant margin.
  P3  The best single CONSTANT beats S2LF, as in ideas 175 and 189's premise.
  P4  The SMALL family carries whatever edge exists; U56 is ~zero (idea 175's pattern).
  P5  4b passes are concentrated in the U56 family and SMALL is ~0 of its rows
      (twelfth reproduction of idea 136).

CAVEATS carried, not buried
---------------------------
  * SURVIVORSHIP: SMALL439 is CURRENT constituents of a sub-$2B screen and contains no
    delistings (idea 54); U56/ETF36 are current lists too.  Every arm and the control
    inherit the bias identically, so the PAIRED selector reading is unaffected; every
    LEVEL (CAGR, Sharpe, 4b pass count) on the small family is not, and is biased upward.
  * Idea 38: data/prices.csv is calendar-day indexed after 2014-09-17 (BTC-USD in the
    download), so weekly bars on U56/ETF36 are calendar weeks; W is unaffected in kind.
  * Idea 126: t+1 execution only.
  * REBASED's entry price is the first bar of the PANEL SAMPLE, not a listing date; on a
    sub-draw the entry date is common to all names, which makes REBASED a since-2008
    total-return rank rather than a since-listing one.  Stated, not corrected: idea 193
    used the same construction and this run's job is to re-price it, not improve it.
  * Books inside a family are overlapping draws from one pool, so a pooled t OVERSTATES
    significance (idea 175 levelled this at idea 171 and it applies here too).  Per-family
    numbers are reported alongside the pooled one for exactly that reason.

Deterministic, standalone.  Writes .console.txt, .arms.csv, .walkforward.csv, .keep.csv.
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-05_does-the-leak-free-selector-edge-survive-a-third-corpus_cloud"
OUT = ROOT / "research" / "backtests"

# ---- inherited verbatim from ideas 175 (corpus) and 193/181 (arms) -----------------------------
N, GROSS, FREQ, MAX_VOL = 20, 0.75, "W", 0.60
MS = [0.20, 0.50, 1.00]
DIRS = {"POS": 1.0, "NEG": -1.0}
COSTS = [10.0, 25.0]
IS_END = pd.Timestamp("2016-12-31")
OOS_LO = IS_END + pd.Timedelta(days=1)
LEAKFREE = ["MOM", "R3", "REBASED"]
PHI, DELTA = 0.70, 0.60                      # 4b CAGR floor and drawdown cap multipliers

FAMILIES = ["SMALL", "U56", "ETF"]
DRAWS = {"SMALL": (175_500, [20, 40, 80]), "U56": (175_600, [20, 40]), "ETF": (175_700, [12, 24])}
N_DRAWS = 16
RANDOM_SEED = 196

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 4000)

_lines: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


def rankpct(df):
    return df.rank(axis=1, pct=True)


# ------------------------------------------------------------------ vectorised engine equivalent
def fast_backtest(prices, weights, cost_bps=0.0, freq=FREQ):
    """Idea 193's fast_backtest verbatim.  Asserted == engine.backtest in R2."""
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
    return {"returns": pd.Series(port, index=idx), "turnover": pd.Series(turn, index=idx)}


# ------------------------------------------------------------------------- book / corpus (id 175)
def comp_score(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (rankpct(mom) + rankpct(r6) + rankpct(r3)) / 3


def first_valid_row(px):
    fv = px.apply(lambda s: s.loc[s.first_valid_index()] if s.first_valid_index() is not None
                  else np.nan)
    out = pd.DataFrame(np.tile(fv.values, (len(px), 1)), index=px.index, columns=px.columns)
    return out.where(px.notna())


class Book:
    def __init__(self, name, px, tradable, family):
        self.name, self.px, self.family = name, px, family
        self.tradable = [c for c in px.columns if c in tradable]
        self.comp = comp_score(px)
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        m = ((px > px.rolling(200).mean()) & (vol20 < MAX_VOL)).copy()
        drop = [c for c in px.columns if c not in set(self.tradable)]
        if drop:
            m[drop] = False
        self.elig = m
        entry = first_valid_row(px)
        self.keys = {
            "MOM":     rankpct(px.shift(21) / px.shift(252) - 1),
            "R3":      rankpct(px / px.shift(63) - 1),
            "REBASED": rankpct(px / entry),
        }

    def run(self, score, cost_bps=0.0):
        rank = score.where(self.elig).rank(axis=1, ascending=False)
        w = (rank <= N).astype(float) * (GROSS / N)
        return fast_backtest(self.px, w, cost_bps=cost_bps)


def build_corpus():
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    etf36 = [t for t in U["broad"] + U["sectors"] + U["bonds_fx_commod"] if t not in crypto]

    px56 = load_universe()
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    P(f"  small panel: {len([c for c in pxs.columns if c != 'SPY'])} names, dropped "
      f"{len([c for c in pxs.columns if c in bad])} with max_1d_move >= 1.0 -> {len(s_stk)} tradable"
      " (SURVIVORSHIP: current constituents only, no delistings -- see data/SMALL_PANEL_README.md)")
    pxs = pxs[s_stk + ["SPY"]]

    u_stk = [c for c in px56.columns if c != "SPY"]
    e_stk = [t for t in etf36 if t in px56.columns and t != "SPY"]

    def keep(px, cols):
        cols = [c for c in cols if c in px.columns]
        return px[list(dict.fromkeys(cols + ["SPY"]))].dropna(how="all").ffill()

    books = [Book("SMALL439", keep(pxs, s_stk), set(s_stk), "SMALL"),
             Book("U56", keep(px56, u_stk), set(u_stk), "U56"),
             Book("ETF36", keep(px56, e_stk), set(e_stk), "ETF")]
    pools = {"SMALL": (pxs, s_stk), "U56": (px56, u_stk), "ETF": (px56, e_stk)}
    for fam in FAMILIES:
        seed, ks = DRAWS[fam]
        pxp, pool = pools[fam]
        for k in ks:
            rng = np.random.default_rng(seed + k)
            for d in range(N_DRAWS):
                sub = sorted(rng.choice(pool, size=k, replace=False).tolist())
                books.append(Book(f"{fam}k{k}d{d:02d}", keep(pxp, sub), set(sub), fam))
    return books


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
    return bool(row["Sharpe_H1"] > base["Sharpe_H1"] and row["Sharpe_H2"] > base["Sharpe_H2"]
                and row["MaxDD_F"] >= base["MaxDD_F"])


def pass4b(row, spy):
    return bool(row["Sharpe_H1"] > spy["Sharpe_H1"] and row["Sharpe_H2"] > spy["Sharpe_H2"]
                and row["Sharpe_OOS"] > spy["Sharpe_OOS"]
                and row["MaxDD_F"] >= DELTA * spy["MaxDD_F"]
                and row["CAGR_F"] >= PHI * spy["CAGR_F"])


def tstat(x):
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    if len(x) < 2 or x.std(ddof=1) == 0:
        return np.nan
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x))))


# ============================================================================================ run
def main():
    t0 = time.time()
    P("=" * 104)
    P("IDEA 196  does-the-leak-free-selector-edge-survive-a-third-corpus   (cloud, 2026-09-05)")
    P("=" * 104)

    P("\nbuilding idea 175's corpus from its own seeds ...")
    books = build_corpus()
    P(f"  corpus: {len(books)} books  " +
      "  ".join(f"{f}={sum(b.family == f for b in books)}" for f in FAMILIES))

    # ---------------------------------------------------------------- reproduction, before numbers
    repro = []
    pu = load_universe()
    ru = backtest(pu, rules_v1_weights(pu), cost_bps=10.0, freq="W")["returns"].loc[pu.index[260]:]
    mu = metrics(ru)
    P(f"\nR0  RULES v1 on u56 @10bps: {mu['CAGR']:.5%} / {mu['Sharpe']:.5f} / {mu['MaxDD']:.5%}"
      f"   (published 6.45305% / 0.66418 / -13.82780%)")
    repro.append(dict(check="R0_rules_v1_u56", value=mu["Sharpe"], target=0.66418,
                      err=abs(mu["Sharpe"] - 0.66418)))

    bk = {b.name: b for b in books}
    tb = bk["U56"]
    w = (tb.comp.where(tb.elig).rank(axis=1, ascending=False) <= N).astype(float) * (GROSS / N)
    f0 = fast_backtest(tb.px, w, cost_bps=0.0)
    e0 = backtest(tb.px, w, cost_bps=0.0, freq=FREQ)
    e2 = float((e0["returns"] - f0["returns"]).abs().max())
    P(f"R1  fast_backtest == engine.backtest on U56's control book : max abs err {e2:.3e}")
    repro.append(dict(check="R1_engine", value=e2, target=0.0, err=e2))
    e10 = backtest(tb.px, w, cost_bps=10.0, freq=FREQ)["returns"]
    e3 = float((e10 - (f0["returns"] - f0["turnover"] * 10.0 / 1e4)).abs().max())
    P(f"R2  cost identity  r_c == r_0 - turnover*c/1e4 : max abs err {e3:.3e}")
    repro.append(dict(check="R2_cost", value=e3, target=0.0, err=e3))

    st = tb.px.index[260]
    m175 = metrics(f0["returns"].loc[st:] - f0["turnover"].loc[st:] * 10.0 / 1e4)
    P(f"R3  idea 175's published U56 @ W ladder point (12.86% / 1.1075 / -18.21%): "
      f"{m175['CAGR']:.4%} / {m175['Sharpe']:.4f} / {m175['MaxDD']:.4%}")
    repro.append(dict(check="R3_id175_U56_W", value=m175["Sharpe"], target=1.1075,
                      err=abs(m175["Sharpe"] - 1.1075)))

    nb = len(books)
    repro.append(dict(check="R4_corpus_115_books", value=float(nb), target=115.0,
                      err=abs(nb - 115)))
    P(f"R4  corpus size == idea 175's 115 books : {nb}")

    R = pd.DataFrame(repro)
    P("\n" + R.to_string(index=False, float_format=lambda x: f"{x:.3e}"))
    ok = bool(R["err"].iloc[1:3].max() < 1e-8 and R["err"].iloc[0] < 5e-5
              and R["err"].iloc[3] < 5e-4 and R["err"].iloc[4] == 0)
    P(f"\nreproduction {'PASSES' if ok else 'FAILS'} -- "
      f"{'proceeding to new numbers' if ok else 'STOP'}")
    if not ok:
        return

    # ------------------------------------------------------------------------------- the grid
    P("\n" + "=" * 104)
    P("GRID  115 books x (1 control + 3 leak-free keys x 2 dirs x 3 m) x 2 cost rungs")
    P("=" * 104)
    arms = []
    for i, b in enumerate(books):
        start = b.px.index[260]
        spy = b.px["SPY"].pct_change().fillna(0).loc[start:]
        srow = full_row(spy)
        base = backtest(b.px, rules_v1_weights(b.px), cost_bps=0.0, freq="W")
        b0, bt = base["returns"].loc[start:], base["turnover"].loc[start:]
        base_rows = {c: full_row(b0 - bt * c / 1e4) for c in COSTS}

        cres = b.run(b.comp)
        c0, ct = cres["returns"].loc[start:], cres["turnover"].loc[start:]
        ctrl_rows = {c: full_row(c0 - ct * c / 1e4) for c in COSTS}
        for c in COSTS:
            r = dict(book=b.name, family=b.family, ncol=len(b.tradable), key="CONTROL",
                     dir="-", m=0.0, cost=c,
                     turnover_yr=float(ct.sum() / (len(ct) / 252)),
                     dSharpe_F=0.0, dSharpe_IS=0.0, dSharpe_OOS=0.0,
                     spy_S_F=srow["Sharpe_F"], spy_S_OOS=srow["Sharpe_OOS"],
                     spy_CAGR_F=srow["CAGR_F"], spy_MaxDD_F=srow["MaxDD_F"])
            r.update(ctrl_rows[c])
            r["pass4a"] = pass4a(r, base_rows[c])
            r["pass4b"] = pass4b(r, srow)
            arms.append(r)

        for kn in LEAKFREE:
            kv = b.keys[kn]
            for dn, dv in DIRS.items():
                for m in MS:
                    res = b.run(b.comp + dv * m * kv)
                    r0, trn = res["returns"].loc[start:], res["turnover"].loc[start:]
                    for c in COSTS:
                        rr = dict(book=b.name, family=b.family, ncol=len(b.tradable), key=kn,
                                  dir=dn, m=m, cost=c,
                                  turnover_yr=float(trn.sum() / (len(trn) / 252)),
                                  spy_S_F=srow["Sharpe_F"], spy_S_OOS=srow["Sharpe_OOS"],
                                  spy_CAGR_F=srow["CAGR_F"], spy_MaxDD_F=srow["MaxDD_F"])
                        rr.update(full_row(r0 - trn * c / 1e4))
                        for tag in ("F", "IS", "OOS"):
                            rr[f"dSharpe_{tag}"] = rr[f"Sharpe_{tag}"] - ctrl_rows[c][f"Sharpe_{tag}"]
                        rr["pass4a"] = pass4a(rr, base_rows[c])
                        rr["pass4b"] = pass4b(rr, srow)
                        arms.append(rr)
        if (i + 1) % 20 == 0:
            P(f"  ... {i + 1}/{len(books)} books ({time.time() - t0:.0f}s)")

    A = pd.DataFrame(arms)
    A.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    P(f"\ngrid: {len(A)} rows, {len(A[A.key != 'CONTROL'])} real arms "
      f"({time.time() - t0:.0f}s) -> {STEM}.arms.csv")

    real = A[A.key != "CONTROL"].copy()
    P("\n  mean dSharpe (full sample) by key x direction, ALL grid points, pooled:")
    P(real.pivot_table(index="key", columns="dir", values="dSharpe_F")
      .to_string(float_format=lambda x: f"{x:+.4f}"))
    P("\n  same, by family (this is the number idea 193 could not compute):")
    P(real.pivot_table(index=["family", "key"], columns="dir", values="dSharpe_F")
      .to_string(float_format=lambda x: f"{x:+.4f}"))
    P("\n  mean dSharpe by tilt strength m and cost rung:")
    P(real.pivot_table(index="m", columns="cost", values="dSharpe_F")
      .to_string(float_format=lambda x: f"{x:+.4f}"))
    P("\n  mean turnover (x/yr): control "
      f"{A[A.key == 'CONTROL']['turnover_yr'].mean():.2f}, tilted {real['turnover_yr'].mean():.2f}")

    # -------------------------------------------------------------------- rule 8 walk-forward
    P("\n" + "=" * 104)
    P("RULE 8 WALK-FORWARD.  key/dir chosen on data <= 2016-12-31 only; 2017-2026 read ONCE.")
    P("  690 cells = 115 books x 3 m x 2 cost rungs.  Pool = 6 arms (3 leak-free keys x 2 dirs).")
    P("=" * 104)
    rng = np.random.default_rng(RANDOM_SEED)
    ctrl = A[A.key == "CONTROL"]
    wf = []
    for b in books:
        cb = ctrl[ctrl.book == b.name]
        sb = real[real.book == b.name]
        for m in MS:
            for c in COSTS:
                cz = cb[cb.cost == c].iloc[0]
                base_oos = float(cz["Sharpe_OOS"])
                cand = sb[(sb.m == m) & (sb.cost == c)]
                if not len(cand):
                    continue
                rows = [dict(selector="S0 do-nothing", pick="-", OOS_Sharpe=base_oos,
                             OOS_CAGR=float(cz["CAGR_OOS"]), OOS_MaxDD=float(cz["MaxDD_OOS"]))]
                r = cand.loc[cand["dSharpe_IS"].idxmax()]
                rows.append(dict(selector="S2LF IS-argmax (leak-free)",
                                 pick=f"{r['key']}/{r['dir']}", OOS_Sharpe=float(r["Sharpe_OOS"]),
                                 OOS_CAGR=float(r["CAGR_OOS"]), OOS_MaxDD=float(r["MaxDD_OOS"])))
                rr = cand.iloc[int(rng.integers(len(cand)))]
                rows.append(dict(selector="RANDOM (same pool)", pick=f"{rr['key']}/{rr['dir']}",
                                 OOS_Sharpe=float(rr["Sharpe_OOS"]), OOS_CAGR=float(rr["CAGR_OOS"]),
                                 OOS_MaxDD=float(rr["MaxDD_OOS"])))
                for kn in LEAKFREE:
                    for dn in DIRS:
                        s = cand[(cand.key == kn) & (cand.dir == dn)]
                        if len(s):
                            q = s.iloc[0]
                            rows.append(dict(selector=f"C-{kn}/{dn}", pick=f"{kn}/{dn}",
                                             OOS_Sharpe=float(q["Sharpe_OOS"]),
                                             OOS_CAGR=float(q["CAGR_OOS"]),
                                             OOS_MaxDD=float(q["MaxDD_OOS"])))
                o = cand.loc[cand["Sharpe_OOS"].idxmax()]
                rows.append(dict(selector="ORACLE-OOS", pick=f"{o['key']}/{o['dir']}",
                                 OOS_Sharpe=float(o["Sharpe_OOS"]), OOS_CAGR=float(o["CAGR_OOS"]),
                                 OOS_MaxDD=float(o["MaxDD_OOS"])))
                for r_ in rows:
                    r_.update(book=b.name, family=b.family, m=m, cost=c,
                              dOOS=r_["OOS_Sharpe"] - base_oos)
                    wf.append(r_)
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(f"\nwalk-forward: {len(W)} rows over {W[['book', 'm', 'cost']].drop_duplicates().shape[0]} "
      f"cells -> {STEM}.walkforward.csv")

    piv = W.pivot_table(index=["book", "m", "cost"], columns="selector", values="OOS_Sharpe")
    out = []
    for s in piv.columns:
        d = (piv[s] - piv["S0 do-nothing"]).dropna()
        out.append(dict(selector=s, mean_OOS_Sharpe=float(piv[s].mean()), dOOS=float(d.mean()),
                        t=tstat(d), wins=int((d > 0).sum()), losses=int((d < 0).sum()),
                        n=int(len(d))))
    SW = pd.DataFrame(out).sort_values("mean_OOS_Sharpe", ascending=False)
    P("\n  ALL 690 CELLS, paired against S0 do-nothing:")
    P(SW.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    # idea 193's own convention: collapse the two cost rungs before pairing
    pc = W.pivot_table(index=["book", "m"], columns="selector", values="OOS_Sharpe")
    out = []
    for s in pc.columns:
        d = (pc[s] - pc["S0 do-nothing"]).dropna()
        out.append(dict(selector=s, mean_OOS_Sharpe=float(pc[s].mean()), dOOS=float(d.mean()),
                        t=tstat(d), wins=int((d > 0).sum()), losses=int((d < 0).sum()),
                        n=int(len(d))))
    SC = pd.DataFrame(out).sort_values("mean_OOS_Sharpe", ascending=False)
    P("\n  COST-COLLAPSED (345 cells) -- idea 193's own convention, the number to compare with")
    P("  its +0.1370 / t +2.19 / 11W-1L:")
    P(SC.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    P("\n  PER FAMILY (the decomposition idea 193's 2-panel corpus could not do):")
    fam_rows = []
    for fam in FAMILIES:
        sub = W[W.family == fam]
        pf = sub.pivot_table(index=["book", "m", "cost"], columns="selector", values="OOS_Sharpe")
        for s in ("S2LF IS-argmax (leak-free)", "RANDOM (same pool)", "ORACLE-OOS",
                  "C-MOM/NEG", "C-MOM/POS", "C-R3/NEG", "C-R3/POS",
                  "C-REBASED/NEG", "C-REBASED/POS"):
            if s not in pf.columns:
                continue
            d = (pf[s] - pf["S0 do-nothing"]).dropna()
            fam_rows.append(dict(family=fam, selector=s, n_books=sub.book.nunique(),
                                 S0=float(pf["S0 do-nothing"].mean()),
                                 mean_OOS=float(pf[s].mean()), dOOS=float(d.mean()), t=tstat(d),
                                 wins=int((d > 0).sum()), losses=int((d < 0).sum())))
    FAM = pd.DataFrame(fam_rows)
    P(FAM.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    P("\n  S2LF vs RANDOM, paired directly (does the FIT beat a coin flip from the same pool?):")
    for lbl, pp in (("all 690 cells", piv), ("cost-collapsed 345", pc)):
        d = (pp["S2LF IS-argmax (leak-free)"] - pp["RANDOM (same pool)"]).dropna()
        P(f"    {lbl:20s}  d {d.mean():+.4f}  t {tstat(d):+.2f}  "
          f"{int((d > 0).sum())}W/{int((d < 0).sum())}L")

    P("\n  what S2LF actually picks (share of the 690 cells):")
    sel = W[W.selector == "S2LF IS-argmax (leak-free)"]
    P((sel["pick"].value_counts(normalize=True) * 100).to_string(float_format=lambda x: f"{x:.1f}%"))
    orc = W[W.selector == "ORACLE-OOS"]
    P("\n  what the OOS oracle would have picked:")
    P((orc["pick"].value_counts(normalize=True) * 100).to_string(float_format=lambda x: f"{x:.1f}%"))
    agree = (sel.set_index(["book", "m", "cost"])["pick"]
             == orc.set_index(["book", "m", "cost"])["pick"]).mean()
    P(f"\n  S2LF agrees with the oracle in {agree:.1%} of cells (1/6 = 16.7% by chance)")
    orc_gap = piv["ORACLE-OOS"] - piv["S0 do-nothing"]
    s2_gap = piv["S2LF IS-argmax (leak-free)"] - piv["S0 do-nothing"]
    P(f"  capture of the oracle: {s2_gap.mean() / orc_gap.mean():.1%} "
      f"(S2LF {s2_gap.mean():+.4f} of the oracle's {orc_gap.mean():+.4f})")

    # ------------------------------------------------------------------------------ benchmarks
    P("\n  BENCHMARKS over the same OOS window (2017-01-01 ->), for the three fixed books:")
    for nm in ("U56", "SMALL439", "ETF36"):
        b = bk[nm]
        start = b.px.index[260]
        bb = backtest(b.px, rules_v1_weights(b.px), cost_bps=10.0, freq="W")["returns"].loc[start:]
        sp = b.px["SPY"].pct_change().fillna(0).loc[start:]
        for tag, rr in (("full", (bb, sp)),):
            pass
        mb, ms_ = metrics(win(bb, lo=OOS_LO)), metrics(win(sp, lo=OOS_LO))
        mbf, msf = metrics(bb), metrics(sp)
        P(f"    {nm:9s} RULES v1 full {mbf['CAGR']:7.2%}/{mbf['Sharpe']:.4f}/{mbf['MaxDD']:8.2%}"
          f"   OOS {mb['CAGR']:7.2%}/{mb['Sharpe']:.4f}/{mb['MaxDD']:8.2%}"
          f" | SPY full {msf['CAGR']:7.2%}/{msf['Sharpe']:.4f}/{msf['MaxDD']:8.2%}"
          f"   OOS {ms_['CAGR']:7.2%}/{ms_['Sharpe']:.4f}/{ms_['MaxDD']:8.2%}")

    # --------------------------------------------------------------------------- both KEEP paths
    P("\n" + "=" * 104)
    P("BOTH KEEP PATHS, every row of the grid")
    P("=" * 104)
    K = A.copy()
    P(f"\n  real arms: 4a {int(real.pass4a.sum())}/{len(real)}, "
      f"4b {int(real.pass4b.sum())}/{len(real)}")
    ctl = A[A.key == "CONTROL"]
    P(f"  controls : 4a {int(ctl.pass4a.sum())}/{len(ctl)}, 4b {int(ctl.pass4b.sum())}/{len(ctl)}")
    P("\n  4b passes by family (real arms):")
    P(real.groupby("family")["pass4b"].agg(["sum", "count"]).to_string())
    P("\n  4a passes by family (real arms):")
    P(real.groupby("family")["pass4a"].agg(["sum", "count"]).to_string())
    P("\n  4b passes by key/dir (real arms):")
    P(real.pivot_table(index="key", columns="dir", values="pass4b", aggfunc="sum")
      .to_string())

    fx = K[K.pass4b & K.book.isin(["SMALL439", "U56", "ETF36"])]
    P(f"\n  4b passes on the three FIXED books ({len(fx)} rows) -- the only ones that are not"
      " an unpriced sub-draw:")
    if len(fx):
        P(fx[["book", "key", "dir", "m", "cost", "CAGR_F", "Sharpe_F", "MaxDD_F",
              "Sharpe_H1", "Sharpe_H2", "Sharpe_OOS", "CAGR_OOS", "turnover_yr",
              "pass4a"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    else:
        P("    none")

    # most-violated 4b bar among failing real rows
    fail = real[~real.pass4b]
    bars = dict(
        CAGR=int((fail["CAGR_F"] < PHI * fail["spy_CAGR_F"]).sum()),
        DD=int((fail["MaxDD_F"] < DELTA * fail["spy_MaxDD_F"]).sum()),
        OOS=int((fail["Sharpe_OOS"] <= fail["spy_S_OOS"]).sum()),
    )
    P(f"\n  among {len(fail)} failing real rows, bar violation counts (CAGR/DD/OOS-Sharpe): {bars}")
    K.to_csv(OUT / f"{STEM}.keep.csv", index=False)

    # ------------------------------------------------------------------------------ predictions
    P("\n" + "=" * 104)
    P("PRE-REGISTERED PREDICTIONS")
    P("=" * 104)
    s2_all = float(SW.loc[SW.selector == "S2LF IS-argmax (leak-free)", "dOOS"].iloc[0])
    s2_cc = float(SC.loc[SC.selector == "S2LF IS-argmax (leak-free)", "dOOS"].iloc[0])
    rnd_cc = float(SC.loc[SC.selector == "RANDOM (same pool)", "dOOS"].iloc[0])
    consts = SW[SW.selector.str.startswith("C-")]
    best_const = float(consts["dOOS"].max())
    d_sr = (pc["S2LF IS-argmax (leak-free)"] - pc["RANDOM (same pool)"]).dropna()
    fam_s2 = FAM[FAM.selector == "S2LF IS-argmax (leak-free)"].set_index("family")["dOOS"]
    small4b = int(real[real.family == "SMALL"]["pass4b"].sum())
    u4b = int(real[real.family == "U56"]["pass4b"].sum())
    preds = [
        ("P1 S2LF dOOS positive but < +0.1370", (s2_cc > 0) and (s2_cc < 0.1370),
         f"cost-collapsed {s2_cc:+.4f} (all-cell {s2_all:+.4f}) vs idea 193's +0.1370"),
        ("P2 S2LF does not significantly beat RANDOM", abs(tstat(d_sr)) < 2.0,
         f"S2LF-RANDOM {d_sr.mean():+.4f}, t {tstat(d_sr):+.2f}"),
        ("P3 best CONSTANT beats S2LF", best_const > s2_all,
         f"best constant {best_const:+.4f} vs S2LF {s2_all:+.4f}"),
        ("P4 SMALL carries the edge, U56 ~zero",
         bool(fam_s2.get("SMALL", 0) > fam_s2.get("U56", 0)),
         "  ".join(f"{k} {v:+.4f}" for k, v in fam_s2.items())),
        ("P5 4b concentrated in U56, SMALL ~0", (small4b == 0) and (u4b > 0),
         f"SMALL {small4b}, U56 {u4b}, ETF {int(real[real.family == 'ETF']['pass4b'].sum())}"),
    ]
    for nm, hit, ev in preds:
        P(f"  {'HIT ' if hit else 'MISS'}  {nm:45s}  {ev}")
    P(f"\n  {sum(h for _, h, _ in preds)} of {len(preds)} predictions hit.")

    P(f"\ndone in {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
