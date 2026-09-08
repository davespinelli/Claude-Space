#!/usr/bin/env python3
"""Idea 227 - "is-the-top-decile-trim-a-drop-the-worst-rule": idea 155's only surviving
edge is a q = 0.90-0.95 trim of the eligible set (+0.0316 U56 / +0.0171 B136 Sharpe at
10 bps over q = 1.00).  Is that the COMPOSITE RANKING at all, or is any trim of that
depth worth the same?

The question
------------
Idea 155 read the CANDq ladder's argmax at q = 0.90 (U56) / 0.95 (B136) and called it a
third derivation of "drop the ranking".  But an argmax at q = 0.90 is a statement about
one operation - delete the bottom 10% of the eligible set - and idea 155 never varied the
key that decides WHICH 10%.  Three things could produce the same number:

    (i)  the composite genuinely ranks, and the bottom decile is genuinely worse;
    (ii) ONE leg of the composite ranks and the other two are ballast;
    (iii) nothing ranks - a book of 0.9 * n_elig names simply beats a book of n_elig
          names at these costs, for reasons of concentration/turnover that have no
          content about which names are dropped.

This run separates them by holding the trim DEPTH fixed and swapping the KEY.

Design - one ladder, 26 arms, one shared control
------------------------------------------------
The construction is idea 155's CANDq verbatim: each rebalance week take the eligible set
(200d MA and vol20 < 0.60 gate, tradable names only, composite defined), rank it, hold
the top n_t = clip(round(q * n_elig), 1, n_elig) equally weighted at 75% gross.  Deployed
gross is 75% at EVERY q and for EVERY key, so idea 157's cash channel cannot contaminate
the comparison; the eligible set is fixed ONCE (by the composite's own notna mask) and
every key is masked to it, so q = 1.00 is byte-identical across all 26 arms and the
ladder carries its own control.  Only WHICH names are dropped changes.

    KEYS (higher = kept)
        COMP     RULES v1's composite without the /sqrt(vol20) tilt  <- idea 155's key
        MOM      leg 1 alone: 12-1 momentum   px.shift(21)/px.shift(252) - 1
        R6       leg 2 alone: 6-month return  px/px.shift(126) - 1
        R3       leg 3 alone: 3-month return  px/px.shift(63) - 1
        LOWVOL   -vol20: a pure vol screen, no return information at all
    DIRECTIONS
        KEEPTOP  drop the bottom (1-q) - the "drop the worst" reading
        KEEPBOT  drop the TOP (1-q)    - the sign control.  If a trim pays the same when
                 it deletes the BEST names, the key carries no direction and (iii) is the
                 answer.
    NULLS (KEY DESTROYED, 8 seeds each, fixed in advance)
        SHUFW    a fresh uniform permutation of the eligible set EVERY rebalance week -
                 the queue's "shuffled within week".  Destroys information AND persistence.
        SHUFF    one uniform draw per NAME, held constant for all time.  Destroys the
                 information but keeps the persistence, so the churn cost of a random
                 trim is separated from its (absent) content.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. q in {0.50, 0.70, 0.80, 0.85, 0.90, 0.95}   trim depth (q = 1.00 is the control)
    2. c in {0, 5, 10, 15, 20, 25, 30} bps          idea 82's cost ladder
The KEY, the DIRECTION, the SEED and the PANEL are the treatment axes of the idea itself,
not dials: every one of them is REPORTED at every grid point, none is chosen.

Grid = 3 panels x 6 q x 26 arms x 7 rungs = 3,276 points, plus 3 controls; all written to
the .grid.csv beside this script.  The cost ladder is exact, not re-simulated:
net(c) = gross - turnover * c / 1e4 is an identity of the engine (pre-check [c]).

Pre-checks run BEFORE any new number is read
    [a] harness: idea 2's U56/CAND20 published row and the live RULES v1 row.
    [b] premise: idea 155's OWN headline premia - COMP/KEEPTOP q=0.90 on U56 (+0.0316)
        and q=0.95 on B136 (+0.0171) at 10 bps.  If they do not reproduce, idea 227 has
        no premise and the run aborts.
    [c] the cost identity.
    [d] the shared control: q = 1.00 must give max|d| = 0 returns across all 26 arms.

Walk-forward (PROTOCOL rule 8) - selectors fixed before any OOS number was read
    S0  do-nothing control: q = 1.00 (EWall over the eligible set).
    S1  IS-argmax over the WHOLE arm x q grid at 10 bps (the chooser that sees all keys).
    S2  IS-argmax restricted to COMP/KEEPTOP - what a reader of idea 155 would have run.
    S3  random (arm, q), seed fixed in advance - the size-matched null.
    Parameters chosen on 2009-2016 only; 2017-2026 read once, untouched.

Verdicts (both KEEP paths, every one of the 3,276 points)
    4a  Sharpe > RULES v2 (the LIVE book since 2026-09-06) in BOTH halves AND MaxDD no
        worse than RULES v2.  The RULES v1 verdict is carried alongside for continuity
        with idea 155's own table.
    4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

Survivorship: universe_broad.json and the small panel are CURRENT constituents,
one-directional; the ladder inherits that in full and nothing here corrects it.

Deterministic, standalone.  Reads baseline.py and engine.py; modifies nothing.
"""
import sys, json, time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import warnings
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore", category=RuntimeWarning)
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score
from engine import backtest, metrics, rebalance_mask

FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
QS = [0.50, 0.70, 0.80, 0.85, 0.90, 0.95]
Q_CTRL = 1.00
RUNGS = [0, 5, 10, 15, 20, 25, 30]
COST_MAIN = 10
WARMUP = 260
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
N_SEEDS = 8
DEEP_SEEDS = 60                                      # deep SHUFF null at the trim band
DEEP_QS = [0.85, 0.90, 0.95]
DEEP_PANELS = ["U56", "B136"]
SEED_BASE = 227_000
SEED_DEEP = 227_300
SEED_S3 = 227_999
SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 800)

_lines = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)

def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")

def fam(k):
    """Key family: the 8 seeded nulls collapse, the 5 real keys do NOT (R3 != R6)."""
    return "SHUFW" if k.startswith("SHUFW") else ("SHUFF" if k.startswith("SHUFF") else k)

def spearman(a, b):
    a, b = pd.Series(np.asarray(a, dtype=float)), pd.Series(np.asarray(b, dtype=float))
    ok = a.notna() & b.notna()
    if ok.sum() < 3: return np.nan
    return float(np.corrcoef(a[ok].rank(), b[ok].rank())[0, 1])

def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]

def fail_4a(m, h1, h2, bm, bh1, bh2):
    f = []
    if not h1 > bh1: f.append("H1")
    if not h2 > bh2: f.append("H2")
    if not m["MaxDD"] >= bm["MaxDD"]: f.append("DD")
    return ",".join(f) if f else "-"

def fail_4b(m, h1, h2, sh_oos, sm, s1, s2, sm_oos):
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not sh_oos > sm_oos: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(sm["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * sm["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


# ---------------------------------------------------------------- panels (idea 155's)
def build_panels():
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)

    def sub(px, cols, tradable=None):
        cols = [c for c in cols if c in px.columns]
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
        p = px[keep].dropna(how="all").ffill()
        return p, set(tradable if tradable is not None else cols)

    s_stk = [c for c in pxs.columns if c != "SPY"]
    return {
        "U56":      sub(px56, list(px56.columns)),
        "B136":     sub(px136, list(px136.columns)),
        "SMALL484": sub(pxs, s_stk, tradable=s_stk),
    }


def eligible_and_keys(px, tradable):
    """The eligible set (fixed ONCE by the composite's notna mask, exactly as idea 155
    defines it) plus every ranking key masked to that SAME set, so q=1.00 is the identical
    book for every arm.  Each key is oriented so that HIGHER = preferred."""
    _, above, vol20 = score(px)
    elig = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        elig[drop] = False
    comp = score(px, vol_scale=False)[0].where(elig)     # composite, no vol tilt
    elig = elig & comp.notna()                            # idea 155's rankable set
    keys = {
        "COMP":   comp.where(elig),
        "MOM":    (px.shift(21) / px.shift(252) - 1).where(elig),
        "R6":     (px / px.shift(126) - 1).where(elig),
        "R3":     (px / px.shift(63) - 1).where(elig),
        "LOWVOL": (-vol20).where(elig),
    }
    return elig, keys


def shuffled_key(px, elig, seed, walk):
    rng = np.random.default_rng(seed)
    if walk:
        v = rng.random(px.shape)                          # fresh draw every day
    else:
        v = np.tile(rng.random(px.shape[1]), (px.shape[0], 1))   # one draw per NAME
    return pd.DataFrame(v, index=px.index, columns=px.columns).where(elig)


def weights_q(px, elig, key, q, keeptop=True):
    """Idea 155's CANDq with an arbitrary key.  keeptop=False keeps the BOTTOM q."""
    # rank 1 must be the PREFERRED name: descending for KEEPTOP, ascending for KEEPBOT
    rank = key.rank(axis=1, ascending=not keeptop)
    n_elig = elig.sum(axis=1)
    n_t = np.clip(np.round(q * n_elig.values), 1, np.maximum(n_elig.values, 1))
    n_t = pd.Series(n_t, index=px.index)
    sel = rank.le(n_t, axis=0) & elig
    cnt = sel.sum(axis=1).replace(0, np.nan)
    return sel.astype(float).div(cnt, axis=0).mul(GROSS).fillna(0.0)


def weights_fixed_n_raw(px, elig, key, n):
    """idea 78/155's raw gross/n CAND-n, used only by pre-check [a]."""
    sel = (key.rank(axis=1, ascending=False) <= n) & elig
    return sel.astype(float) * (GROSS / n)


def run_book(px, w, start):
    res = backtest(px, w, cost_bps=0.0, freq=FREQ)
    return res["returns"].loc[start:], res["turnover"].loc[start:]

def net(r0, tno, c):
    return r0 - tno * c / 1e4


def main():
    t0 = time.time()
    P("=" * 200)
    P(f"Idea 227 is-the-top-decile-trim-a-drop-the-worst-rule (lane B) | {SCRIPT} | weekly, t+1 execution, {GROSS:.0%} gross")
    P("=" * 200)

    panels = build_panels()
    px56, tr56 = panels["U56"]
    px136, tr136 = panels["B136"]

    yrs = px56.index.to_series().groupby(px56.index.year).count()
    P(f"Index sanity (must be ~252 rows/yr): 2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, 2024 {yrs.get(2024)}")
    if yrs.loc[2015:2024].max() > 300:
        P("!! CALENDAR-DAY INDEX DETECTED - aborting."); sys.exit(1)

    # ------------------------------------------------ pre-check [a]
    P("\n--- pre-check [a] harness on universe.json's own window (must match published rows) ---")
    start56 = px56.index[WARMUP]
    elig56, keys56 = eligible_and_keys(px56, tr56)
    for lbl, w, want in [("U56/CAND20", weights_fixed_n_raw(px56, elig56, keys56["COMP"], 20),
                          "idea 2 KEEP: 12.7% / 1.093 / -18.3%"),
                         ("U56/v1", rules_v1_weights(px56), "live v1: 6.5% / 0.666 / -13.8%")]:
        r = backtest(px56, w, cost_bps=COST_MAIN, freq=FREQ)["returns"].loc[start56:]
        m = metrics(r); h1, h2 = half_sharpes(r)
        P(f"  {lbl:<11} {m['CAGR']:.1%} / {m['Sharpe']:.3f} / {m['MaxDD']:.1%}  halves {h1:.3f}/{h2:.3f}   [{want}]")

    # ------------------------------------------------ pre-check [b] idea 155's premise
    P("\n--- pre-check [b] idea 155's OWN headline premia at 10 bps (U56 q=0.90 +0.0316, B136 q=0.95 +0.0171) ---")
    start136 = px136.index[WARMUP]
    elig136, keys136 = eligible_and_keys(px136, tr136)
    prem_pub = {}
    for pk, px, elig, keys, start, qq, want in [
            ("U56", px56, elig56, keys56, start56, 0.90, 0.0316),
            ("B136", px136, elig136, keys136, start136, 0.95, 0.0171)]:
        r1, t1 = run_book(px, weights_q(px, elig, keys["COMP"], Q_CTRL), start)
        rq, tq = run_book(px, weights_q(px, elig, keys["COMP"], qq), start)
        s1 = metrics(net(r1, t1, COST_MAIN))["Sharpe"]; sq = metrics(net(rq, tq, COST_MAIN))["Sharpe"]
        prem_pub[pk] = sq - s1
        P(f"  {pk:<5} q={qq:.2f} {sq:.4f} - q=1.00 {s1:.4f} = {sq-s1:+.4f}   published {want:+.4f}   |d| {abs((sq-s1)-want):.4f}")
    if max(abs(prem_pub["U56"] - 0.0316), abs(prem_pub["B136"] - 0.0171)) > 0.005:
        P("!! idea 155's premise does not reproduce - aborting."); sys.exit(1)

    # ------------------------------------------------ pre-check [c] cost identity
    P("\n--- pre-check [c] cost identity  net(c) = gross - turnover*c/1e4  (must be < 1e-12) ---")
    wt = weights_q(px136, elig136, keys136["COMP"], 0.85)
    r0, tno = run_book(px136, wt, start136)
    direct = backtest(px136, wt, cost_bps=COST_MAIN, freq=FREQ)["returns"].loc[start136:]
    dmax = float((net(r0, tno, COST_MAIN) - direct).abs().max())
    P(f"  B136 q=0.85 at 10 bps: max|identity - direct| = {dmax:.3e}")
    if not dmax < 1e-12:
        P("!! cost identity broken - aborting."); sys.exit(1)

    # ------------------------------------------------ pre-check [d] shared control
    P("\n--- pre-check [d] q=1.00 must be the IDENTICAL book for every arm (max|d| returns) ---")
    base_r, base_t = run_book(px136, weights_q(px136, elig136, keys136["COMP"], Q_CTRL), start136)
    worst = 0.0
    for kname, k in keys136.items():
        for kt in (True, False):
            rr, _ = run_book(px136, weights_q(px136, elig136, k, Q_CTRL, kt), start136)
            worst = max(worst, float((rr - base_r).abs().max()))
    for s in range(N_SEEDS):
        rr, _ = run_book(px136, weights_q(px136, elig136, shuffled_key(px136, elig136, SEED_BASE + s, True), Q_CTRL), start136)
        worst = max(worst, float((rr - base_r).abs().max()))
    P(f"  B136 over 10 keyed arms + {N_SEEDS} shuffles: max|d| = {worst:.3e}")
    if not worst < 1e-15:
        P("!! q=1.00 is not a shared control - aborting."); sys.exit(1)

    # ------------------------------------------------ the ladder
    P("\n" + "=" * 200)
    n_arms = 5 * 2 + 2 * N_SEEDS
    P(f"THE LADDER - {len(panels)} panels x {len(QS)} q x {n_arms} arms x {len(RUNGS)} rungs "
      f"= {len(panels)*len(QS)*n_arms*len(RUNGS)} points, all written to {STEM}.grid.csv")
    P("=" * 200)

    rows, oos_books = [], {}
    for pk, (px, tr) in panels.items():
        start = px.index[WARMUP]
        elig, keys = eligible_and_keys(px, tr)
        arms = {(kn, "KEEPTOP" if kt else "KEEPBOT"): (k, kt)
                for kn, k in keys.items() for kt in (True, False)}
        for s in range(N_SEEDS):
            arms[(f"SHUFW{s}", "KEEPTOP")] = (shuffled_key(px, elig, SEED_BASE + s, True), True)
            arms[(f"SHUFF{s}", "KEEPTOP")] = (shuffled_key(px, elig, SEED_BASE + 500 + s, False), True)

        mask = rebalance_mask(px.index, FREQ)
        n_elig_reb = elig.loc[px.index[mask.values]].sum(axis=1).loc[start:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        v2 = backtest(px, rules_v2_weights(px), cost_bps=COST_MAIN, freq=FREQ)["returns"].loc[start:]
        v1 = backtest(px, rules_v1_weights(px), cost_bps=COST_MAIN, freq=FREQ)["returns"].loc[start:]
        oos = spy.index >= OOS_START
        sm, sh1, sh2 = metrics(spy), *half_sharpes(spy)
        sm_oos = metrics(spy[oos])["Sharpe"]
        m_v2, v2h1, v2h2 = metrics(v2), *half_sharpes(v2)
        m_v1, v1h1, v1h2 = metrics(v1), *half_sharpes(v1)
        P(f"\n[{pk}] {len(tr)} tradables, {start.date()} -> {px.index[-1].date()}, "
          f"mean n_elig on rebalance weeks {n_elig_reb.mean():.1f} (min {int(n_elig_reb.min())}, max {int(n_elig_reb.max())})")
        P(f"       SPY {sm['CAGR']:.1%}/{sm['Sharpe']:.3f}/{sm['MaxDD']:.1%} halves {sh1:.3f}/{sh2:.3f} OOS {sm_oos:.3f} | "
          f"RULES v2 {m_v2['CAGR']:.1%}/{m_v2['Sharpe']:.3f}/{m_v2['MaxDD']:.1%} halves {v2h1:.3f}/{v2h2:.3f} | "
          f"RULES v1 {m_v1['CAGR']:.1%}/{m_v1['Sharpe']:.3f}/{m_v1['MaxDD']:.1%}")

        ctl = {}
        for q in [Q_CTRL] + QS:
            for (kn, dr), (k, kt) in ([(("COMP", "KEEPTOP"), (keys["COMP"], True))] if q == Q_CTRL else arms.items()):
                w = weights_q(px, elig, k, q, kt)
                r0, tno = run_book(px, w, start)
                nheld = float((w.loc[px.index[mask.values]].loc[start:] > 0).sum(axis=1).mean())
                for c in RUNGS:
                    r = net(r0, tno, c)
                    m = metrics(r); h1, h2 = half_sharpes(r)
                    sh_oos = metrics(r[oos])["Sharpe"]
                    if q == Q_CTRL:
                        ctl[c] = dict(Sharpe=m["Sharpe"], CAGR=m["CAGR"], MaxDD=m["MaxDD"],
                                      oos=sh_oos, tno=float(tno.sum()), H1=h1, H2=h2,
                                      oos_cagr=metrics(r[oos])["CAGR"], oos_dd=metrics(r[oos])["MaxDD"])
                        oos_books[(pk, "CTRL", "-", Q_CTRL, c)] = r
                    rows.append(dict(
                        panel=pk, key=kn, dir=dr, q=q, rung=c,
                        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                        OOS_Sharpe=sh_oos, OOS_CAGR=metrics(r[oos])["CAGR"], OOS_MaxDD=metrics(r[oos])["MaxDD"],
                        IS_Sharpe=metrics(r[~oos])["Sharpe"],
                        turnover=float(tno.sum()), n_held=nheld,
                        fail4a=fail_4a(m, h1, h2, m_v2, v2h1, v2h2),
                        fail4a_v1=fail_4a(m, h1, h2, m_v1, v1h1, v1h2),
                        fail4b=fail_4b(m, h1, h2, sh_oos, sm, sh1, sh2, sm_oos)))
                    if q != Q_CTRL:
                        oos_books[(pk, kn, dr, q, c)] = r
            if q == Q_CTRL:
                for c in RUNGS:
                    P(f"       CONTROL q=1.00 @{c:>2} bps: {ctl[c]['CAGR']:.2%} / {ctl[c]['Sharpe']:.4f} / "
                      f"{ctl[c]['MaxDD']:.2%}  halves {ctl[c]['H1']:.3f}/{ctl[c]['H2']:.3f}  OOS {ctl[c]['oos']:.4f}  "
                      f"sum-turnover {ctl[c]['tno']:.1f}")
        P(f"       [{pk} done  t={time.time()-t0:.0f}s]")

    G = pd.DataFrame(rows)
    ref = G[G.q == Q_CTRL].set_index(["panel", "rung"])[["Sharpe", "OOS_Sharpe", "turnover"]]
    idx = pd.MultiIndex.from_arrays([G.panel, G.rung])
    G["prem"] = G["Sharpe"].values - ref["Sharpe"].reindex(idx).values
    G["prem_oos"] = G["OOS_Sharpe"].values - ref["OOS_Sharpe"].reindex(idx).values
    G["tno_ratio"] = G["turnover"].values / ref["turnover"].reindex(idx).values
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    L = G[G.q != Q_CTRL].copy()

    # ---------------------------------------------------------------- Q1: the swap
    P("\n" + "=" * 200)
    P("Q1  DOES THE TRIM SURVIVE THE KEY SWAP?  net Sharpe premium over q=1.00 at 10 bps, by key x direction x q")
    P("=" * 200)
    for pk in panels:
        sub = L[(L.panel == pk) & (L.rung == COST_MAIN)]
        keyed = sub[~sub.key.str.startswith("SHUF")]
        t = keyed.pivot_table(index=["key", "dir"], columns="q", values="prem")
        P(f"\n[{pk}] keyed arms (rows: the key that decides WHICH names are dropped)")
        P(fmt(t))
        for tag, lab in [("SHUFW", "SHUFW  fresh permutation every week"),
                         ("SHUFF", "SHUFF  one random draw per name, held forever")]:
            n = sub[sub.key.str.startswith(tag)]
            agg = n.groupby("q")["prem"].agg(["mean", "std", "min", "max"]).T
            P(f"\n[{pk}] NULL {lab}  ({N_SEEDS} seeds)")
            P(fmt(agg))
            comp = keyed[(keyed.key == "COMP") & (keyed.dir == "KEEPTOP")].set_index("q")["prem"]
            z = ((comp - agg.loc["mean"]) / agg.loc["std"].replace(0, np.nan)).dropna()
            P("      z(COMP/KEEPTOP vs this null): " + "  ".join(f"q={q:.2f} {v:+.2f}" for q, v in z.items()))

    # ------------------------------------------------------- Q1b: the DEEP null
    P("\n" + "=" * 200)
    P(f"Q1b  THE DECISIVE NULL - SHUFF (persistent random key, {DEEP_SEEDS} seeds) at the trim band {DEEP_QS}")
    P("      SHUFW is the WRONG null: a fresh weekly permutation triples turnover (412 vs 187 on U56), so beating it")
    P("      only says the composite is persistent.  SHUFF holds the trim depth, the held count AND the turnover profile")
    P("      fixed and destroys ONLY the information, so it is the null that idea 227's question actually needs.")
    P("=" * 200)
    deep_rows = []
    for pk in DEEP_PANELS:
        px, tr = panels[pk]
        start = px.index[WARMUP]
        elig, keys = eligible_and_keys(px, tr)
        ctl_s = {c: G[(G.panel == pk) & (G.q == Q_CTRL) & (G.rung == c)]["Sharpe"].iloc[0] for c in RUNGS}
        for q in DEEP_QS:
            r0c, tc = run_book(px, weights_q(px, elig, keys["COMP"], q, True), start)
            comp_prem = metrics(net(r0c, tc, COST_MAIN))["Sharpe"] - ctl_s[COST_MAIN]
            draws, tnos = [], []
            for s in range(DEEP_SEEDS):
                k = shuffled_key(px, elig, SEED_DEEP + 1000 * DEEP_QS.index(q) + s, False)
                r0, tn = run_book(px, weights_q(px, elig, k, q, True), start)
                draws.append(metrics(net(r0, tn, COST_MAIN))["Sharpe"] - ctl_s[COST_MAIN])
                tnos.append(float(tn.sum()))
            d = np.array(draws)
            beat = int((d >= comp_prem).sum())
            pct = 100.0 * (d < comp_prem).mean()
            z = (comp_prem - d.mean()) / d.std(ddof=1)
            deep_rows.append(dict(panel=pk, q=q, comp_prem=comp_prem, null_mean=d.mean(), null_sd=d.std(ddof=1),
                                  null_min=d.min(), null_max=d.max(), pctile=pct, z=z,
                                  p_one_sided=(beat + 1) / (DEEP_SEEDS + 1),
                                  comp_turnover=float(tc.sum()), null_turnover=float(np.mean(tnos))))
    D = pd.DataFrame(deep_rows)
    D.to_csv(OUT / f"{STEM}.deepnull.csv", index=False)
    P(fmt(D.set_index(["panel", "q"])))
    P(f"\n  Read: p_one_sided is the exact permutation p-value (rank of COMP among {DEEP_SEEDS} random keys + itself).")
    P(f"  COMP beats the persistent-random null at the 5% level in "
      f"{int((D.p_one_sided <= 0.05).sum())} of {len(D)} (panel x q) cells at the trim band.")
    P(f"  Turnover check (must be close, or the null is not matched): "
      + ", ".join(f"{r.panel} q={r.q:.2f} COMP {r.comp_turnover:.1f} vs null {r.null_turnover:.1f}" for r in D.itertuples()))

    # ---------------------------------------------------------------- Q2: direction
    P("\n" + "=" * 200)
    P("Q2  IS THE TRIM DIRECTIONAL?  premium(KEEPTOP) - premium(KEEPBOT) at the same key and q (10 bps)")
    P("     A key that ranks must pay MORE for dropping the worst than for dropping the best.")
    P("=" * 200)
    d = L[(L.rung == COST_MAIN) & (~L.key.str.startswith("SHUF"))]
    piv = d.pivot_table(index=["panel", "key"], columns=["dir", "q"], values="prem")
    dirgap = (piv["KEEPTOP"] - piv["KEEPBOT"])
    P(fmt(dirgap))
    P(f"\n  KEEPTOP > KEEPBOT in {int((dirgap > 0).sum().sum())} of {int(dirgap.notna().sum().sum())} (panel x key x q) cells; "
      f"mean gap {dirgap.stack().mean():+.4f}, sd {dirgap.stack().std():.4f}")
    for pk in panels:
        sl = dirgap.loc[pk]
        P(f"    [{pk}] {int((sl > 0).sum().sum())}/{int(sl.notna().sum().sum())} positive, mean {sl.stack().mean():+.4f}")

    # ---------------------------------------------------------------- Q3: mechanism
    P("\n" + "=" * 200)
    P("Q3  MECHANISM - is the premium a TURNOVER story?  (10 bps, all 26 arms x 6 q per panel)")
    P("=" * 200)
    for pk in panels:
        sub = L[(L.panel == pk) & (L.rung == COST_MAIN)]
        ctl_t = G[(G.panel == pk) & (G.q == Q_CTRL) & (G.rung == COST_MAIN)]["turnover"].iloc[0]
        P(f"\n[{pk}] control sum-turnover {ctl_t:.1f}   "
          f"Spearman(prem, turnover) {spearman(sub.prem, sub.turnover):+.3f}   "
          f"Spearman(prem, n_held) {spearman(sub.prem, sub.n_held):+.3f}")
        tt = sub.groupby([sub.key.map(fam), "dir"]).agg(
            prem=("prem", "mean"), turnover=("turnover", "mean"), n_held=("n_held", "mean"))
        P(fmt(tt.sort_values("prem", ascending=False)))
    P("\n  GROSS (0 bps) premium, mean over q, by key-family and panel - is there any edge BEFORE costs?")
    g0 = L[L.rung == 0].groupby(["panel", L[L.rung == 0].key.map(fam), "dir"])["prem"].mean().unstack([1, 2])
    P(fmt(g0))

    # ---------------------------------------------------------------- Q4: cost ladder
    P("\n" + "=" * 200)
    P("Q4  THE COST LADDER - mean premium by rung (does the trim pay MORE as costs rise, as a turnover story requires?)")
    P("=" * 200)
    lad = L.groupby(["panel", L.key.map(fam), "rung"])["prem"].mean().unstack("rung")
    P(fmt(lad))

    # ---------------------------------------------------------------- rule 8
    P("\n" + "=" * 200)
    P("RULE 8  WALK-FORWARD - selectors fixed before any OOS number was read; params on 2009-2016, 2017-2026 read once")
    P("=" * 200)
    rng = np.random.default_rng(SEED_S3)
    wf = []
    for pk, (px, tr) in panels.items():
        sub = L[(L.panel == pk) & (L.rung == COST_MAIN)].copy()
        ctl_row = G[(G.panel == pk) & (G.q == Q_CTRL) & (G.rung == COST_MAIN)].iloc[0]
        spy = px["SPY"].pct_change().fillna(0.0).loc[px.index[WARMUP]:]
        spy_oos = spy[spy.index >= OOS_START]
        v2o = backtest(px, rules_v2_weights(px), cost_bps=COST_MAIN, freq=FREQ)["returns"].loc[px.index[WARMUP]:]
        v2o = v2o[v2o.index >= OOS_START]
        sels = {
            "S0 do-nothing q=1.00": ("CTRL", "-", Q_CTRL),
            "S1 IS-argmax (all keys)": tuple(sub.loc[sub.IS_Sharpe.idxmax(), ["key", "dir", "q"]]),
            "S2 IS-argmax (COMP/KEEPTOP only)": tuple(
                sub[(sub.key == "COMP") & (sub.dir == "KEEPTOP")].loc[
                    sub[(sub.key == "COMP") & (sub.dir == "KEEPTOP")].IS_Sharpe.idxmax(), ["key", "dir", "q"]]),
        }
        pick = sub.iloc[int(rng.integers(len(sub)))]
        sels["S3 random arm (seed fixed)"] = (pick.key, pick.dir, pick.q)
        for name, (kn, dr, q) in sels.items():
            r = oos_books[(pk, kn, dr, q, COST_MAIN)]
            ro = r[r.index >= OOS_START]
            m = metrics(ro)
            wf.append(dict(panel=pk, selector=name, arm=f"{kn}/{dr}/q={q}",
                           OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"]))
        wf.append(dict(panel=pk, selector="-- SPY", arm="buy&hold",
                       OOS_CAGR=metrics(spy_oos)["CAGR"], OOS_Sharpe=metrics(spy_oos)["Sharpe"], OOS_MaxDD=metrics(spy_oos)["MaxDD"]))
        wf.append(dict(panel=pk, selector="-- RULES v2 (live)", arm="baseline",
                       OOS_CAGR=metrics(v2o)["CAGR"], OOS_Sharpe=metrics(v2o)["Sharpe"], OOS_MaxDD=metrics(v2o)["MaxDD"]))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(fmt(W.set_index(["panel", "selector"])))
    P("\n  selection premium (OOS Sharpe of the chooser MINUS the do-nothing control on the same panel):")
    for pk in panels:
        s0 = W[(W.panel == pk) & (W.selector.str.startswith("S0"))].OOS_Sharpe.iloc[0]
        for s in ("S1", "S2", "S3"):
            v = W[(W.panel == pk) & (W.selector.str.startswith(s))]
            P(f"    [{pk}] {s} {v.arm.iloc[0]:<26} OOS {v.OOS_Sharpe.iloc[0]:.4f} - do-nothing {s0:.4f} = {v.OOS_Sharpe.iloc[0]-s0:+.4f}")

    # ---------------------------------------------------------------- KEEP paths
    P("\n" + "=" * 200)
    P("KEEP PATHS - both, every grid point")
    P("=" * 200)
    for lab, col in [("4a (vs RULES v2, live)", "fail4a"), ("4a (vs RULES v1, continuity)", "fail4a_v1"), ("4b (vs SPY)", "fail4b")]:
        n = int((G[col] == "-").sum())
        P(f"\n{lab}: {n} of {len(G)} grid points pass")
        if n:
            P(fmt(G[G[col] == "-"][["panel", "key", "dir", "q", "rung", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe"]].head(40)))
        top = G[col].value_counts().head(6)
        P("  most common failure sets: " + ", ".join(f"{k} x{v}" for k, v in top.items()))

    P(f"\n[done in {time.time()-t0:.0f}s]")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
