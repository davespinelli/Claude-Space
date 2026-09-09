#!/usr/bin/env python3
"""Idea 506 (lane C, 2026-09-09): is the 32-EVENT 4a pass a general NO-OP ARTEFACT?

Idea 275's only 4a passer (U56 / RULES v2 / x=0.05 / c=3) clears PROTOCOL 4a at 0, 10 AND
25 bps while firing 32 times in 4,700 days: dTurn +0.000231 x/yr, dCAGR +0.025 pp, dSharpe
+0.0048.  A clause that does almost nothing inherits its control's return stream and can
then "win" on a rounding-scale Sharpe difference.  This run asks whether that is a general
property of PROTOCOL 4a rather than a fact about that clause.

Three legs.

  PART 1 - THE CAUSAL TEST (live prices, the decisive leg).
    Build a family of clauses with ZERO signal content and a tunable activity level: on k
    seeded-random days the book sells one held name in full, sell-only, proceeds to cash
    until the next scheduled rebalance - the exact mechanics of idea 275's daily exit, with
    the trigger replaced by a coin.  If 4a is a sound bar, a content-free clause should pass
    it at a negligible rate at every k.  If the 32-event pass is a no-op artefact, the pass
    rate should be high at small k and decay as the clause starts to cost something.
    k in {1,2,4,8,16,32,64,128,256,512} (tuned param 1) x panel in {U56, BROAD136} (tuned
    param 2) x book in {v1, v2} x 40 seeds x cost rungs {0, 10, 25} bps.  ALL reported.

  PART 2 - THE CENSUS.  Every committed research/backtests/*.csv[.gz] carrying a turnover
    column, a published 4a column and a panel label: how far is each published 4a PASS from
    the comparand it beat, in x/yr of turnover?  Two anchors, both reported:
      (a) BASELINE-anchored (universal): the live book PROTOCOL 4a actually names - RULES v1
          for files dated before 2026-09-06, RULES v2 from 2026-09-06 - with its turnover
          recomputed here on the same panel.
      (b) OWN-CONTROL (clause families): where a file labels a control row inside a cell.
    Coverage and every unanchored file are counted and reported; nothing is imputed.

  PART 3 - RULE 8 (walk-forward).  Activity level k chosen on 2009-2016 IS Sharpe alone,
    evaluated untouched on 2017-2026 against the arm's own control, the live RULES v2 book
    and SPY.  Both the honest (k-only) selector and the overfit (k, seed) selector.

  PART 4 - THE PROPOSED PROTOCOL MINIMUM-ACTIVITY CLAUSE, priced on the grid (tau, delta):
    delete a 4a pass whose turnover differs from its comparand by less than tau x/yr AND
    whose worse-half Sharpe margin is under delta.  Every grid point reported.

KEEP paths 4a and 4b are evaluated for every arm in Part 1.

SURVIVORSHIP: BROAD136 is a current-constituent screen (PROTOCOL 9).  Absolute levels are
optimistic; every number quoted here is an arm-minus-its-own-control difference on the same
names and the same days, which is far less exposed.

Deterministic, offline, no network.  Does not modify RULES.md, scan.py, bot.py or baseline.py.
Run: python research/backtests/2026-09-09_is-the-32-EVENT-4a-PASS-a-general-NO-OP-ARTEFACT_C.py
"""
import sys, glob, gzip, re, warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import (  # noqa: E402
    load_universe, rules_v1_weights, rules_v2_weights, band_state, score, metrics, backtest,
)
from engine import rebalance_mask  # noqa: E402

STEM = Path(__file__).with_suffix("")
OUT = lambda ext: Path(str(STEM) + ext)

K_GRID = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
SEEDS = list(range(40))
COST_RUNGS = [0.0, 10.0, 25.0]
FREQ = "W"
WARMUP = 260
OOS_START = "2017-01-01"
IS_END = "2016-12-31"
TAU_GRID = [0.005, 0.01, 0.02, 0.05, 0.10, 0.25, 0.50, 1.00]
DELTA_GRID = [0.000, 0.005, 0.010, 0.020, 0.050]
V2_LIVE_DATE = pd.Timestamp("2026-09-06")   # RULES v2 became the live 4a comparand


# ------------------------------------------------------------------ backtester (idea 275's)
def backtest_exit(prices, weights, exit_sig, cost_bps=10.0, freq="W"):
    """engine.backtest plus a sell-only daily exit.  exit_sig=None must reproduce it exactly."""
    rets = prices.pct_change().fillna(0.0)
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1)
    mask = rebalance_mask(prices.index, freq).shift(1, fill_value=False)
    if exit_sig is None:
        ex_v = np.zeros(prices.shape, dtype=bool)
    else:
        ex_v = exit_sig.reindex(prices.index).fillna(False).shift(1, fill_value=False).astype(bool).values
    held = np.zeros((len(prices), prices.shape[1]))
    cur = np.zeros(prices.shape[1])
    turnover = np.zeros(len(prices))
    r_v, wt_v, mk = rets.values, w_target.values, mask.values
    n_ev = 0
    for i in range(len(prices)):
        if mk[i] or i == 0:
            new = np.nan_to_num(wt_v[i])
            turnover[i] = np.abs(new - cur).sum()
            cur = new.copy()
        else:
            hit = ex_v[i] & (cur > 0)
            if hit.any():
                n_ev += int(hit.sum())
                turnover[i] += cur[hit].sum()
                cur = cur.copy()
                cur[hit] = 0.0
        held[i] = cur
        growth = cur * (1 + r_v[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    turnover = pd.Series(turnover, index=prices.index)
    H = pd.DataFrame(held, index=prices.index, columns=prices.columns)
    gross_ret = (H * rets).sum(axis=1)
    return {"gross": gross_ret, "turnover": turnover, "events": n_ev, "held": H,
            "applied": pd.Series(mk, index=prices.index)}


def rung(res, cost_bps):
    """Cost-rung identity: r(c) = r(0) - turnover * c / 1e4  (gated below)."""
    return res["gross"] - res["turnover"] * cost_bps / 1e4


def legs(r, start):
    r = r.loc[start:]
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    o = metrics(r.loc[OOS_START:])
    i = metrics(r.loc[:IS_END])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"],
                H2=m2["Sharpe"], IS_Sharpe=i["Sharpe"], IS_CAGR=i["CAGR"],
                OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"])


def pass4a(a, b):
    """PROTOCOL 4a: Sharpe > comparand in BOTH halves and MaxDD no worse."""
    return bool(a["H1"] > b["H1"] and a["H2"] > b["H2"] and a["MaxDD"] >= b["MaxDD"])


def pass4b(a, s):
    """PROTOCOL 4b: Sharpe > SPY in both halves AND OOS, MaxDD <= 60% of SPY, CAGR >= 70%."""
    return bool(a["H1"] > s["H1"] and a["H2"] > s["H2"] and a["OOS_Sharpe"] > s["OOS_Sharpe"]
                and a["MaxDD"] >= 0.60 * s["MaxDD"] and a["CAGR"] >= 0.70 * s["CAGR"])


def ann_turn(res, start, index):
    t = res["turnover"].loc[start:]
    return float(t.sum() / (len(t) / 252.0))


# ------------------------------------------------------------------ panels / books
def panels():
    return {"U56": load_universe(), "BROAD136": load_universe(broad=True)}


BOOKS = {"v1": rules_v1_weights, "v2": rules_v2_weights}


# ------------------------------------------------------------------ the content-free clause
def null_exit(px, ctl, k, seed):
    """k seeded-random sell events, one genuinely-held name each, no signal content at all.

    A signal set at close t is applied at t+1 (backtest_exit shifts it), and the exit branch
    is skipped on a rebalance day, so candidate days are t with holdings at t and no
    rebalance applied at t+1.  Each chosen day therefore fires exactly one event.
    """
    hold = ctl["held"].values > 0
    applied = ctl["applied"].values
    n = len(px)
    cand = np.array([t for t in range(WARMUP, n - 1) if hold[t].any() and not applied[t + 1]])
    rng = np.random.default_rng(1_000_003 * seed + 7919 * k)
    days = rng.choice(cand, size=min(k, len(cand)), replace=False)
    ex = np.zeros(px.shape, dtype=bool)
    for t in days:
        cols = np.where(hold[t])[0]
        ex[t, cols[rng.integers(len(cols))]] = True
    return pd.DataFrame(ex, index=px.index, columns=px.columns)


# ------------------------------------------------------------------ GATES
def gates(P):
    print("\n=== GATES ===")
    px = P["U56"]
    w = rules_v2_weights(px)
    ref = backtest(px, w, cost_bps=10.0, freq=FREQ)
    mine = backtest_exit(px, w, None, freq=FREQ)
    d_r = float((rung(mine, 10.0) - ref["returns"]).abs().max())
    d_t = float((mine["turnover"] - ref["turnover"]).abs().max())
    print(f"[A] backtest_exit(None) vs engine.backtest   returns {d_r:.3e}  turnover {d_t:.3e}")

    r25 = backtest(px, w, cost_bps=25.0, freq=FREQ)["returns"]
    d_c = float((rung(mine, 25.0) - r25).abs().max())
    print(f"[B] cost-rung identity r(c)=r(0)-turn*c/1e4   max abs diff vs live 25 bps {d_c:.3e}")

    # [C] reproduce idea 275's U56 / v2 / x=0.05 / c=3 arm and its control
    ma = px.rolling(200).mean()
    conf = (px < ma * (1 - 0.05)).rolling(3).sum() >= 3      # x = 0.05, c = 3
    arm = backtest_exit(px, w, conf, freq=FREQ)              # the loop applies the held filter
    ctl = mine
    start = px.index[WARMUP]
    la, lc = legs(rung(arm, 10.0), start), legs(rung(ctl, 10.0), start)
    pub = pd.read_csv(ROOT / "research" / "backtests" /
                      "2026-09-09_price-the-removal-of-the-daily-hard-exit_B.csv")
    row = pub[(pub.panel == "U56") & (pub.book == "v2") & (pub.x == 0.05) &
              (pub.c == 3) & (pub.cost == 10.0)].iloc[0]
    diffs = {k: abs(la[k] - row[k]) for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2")}
    ta = ann_turn(arm, start, px.index)
    tc = ann_turn(ctl, start, px.index)
    print(f"[C] idea-275 arm reproduction  max abs diff {max(diffs.values()):.3e}  "
          f"({', '.join(f'{k} {v:.2e}' for k, v in diffs.items())})")
    print(f"    events {arm['events']} (published narrative: 32)   dTurn {ta-tc:+.6f} x/yr "
          f"(published {row['dTurn']:+.6f})   dSharpe {la['Sharpe']-lc['Sharpe']:+.6f} "
          f"(published {row['dSharpe']:+.6f})   4a vs own control {pass4a(la, lc)}")
    return dict(gate_a_ret=d_r, gate_a_turn=d_t, gate_b_cost=d_c,
                gate_c_max=max(diffs.values()), gate_c_events=arm["events"],
                gate_c_dturn=ta - tc, gate_c_pub_dturn=float(row["dTurn"]))


# ------------------------------------------------------------------ PART 1
def part1(P):
    print("\n=== PART 1: content-free clauses at controlled activity ===")
    rows = []
    for pname, px in P.items():
        start = px.index[WARMUP]
        spy = legs(px["SPY"].pct_change().fillna(0.0), start)
        live = backtest_exit(px, rules_v2_weights(px), None, freq=FREQ)
        for bname, fn in BOOKS.items():
            w = fn(px)
            ctl = backtest_exit(px, w, None, freq=FREQ)
            ctl_turn = ann_turn(ctl, start, px.index)
            for cost in COST_RUNGS:
                lc = legs(rung(ctl, cost), start)
                ll = legs(rung(live, cost), start)
                rows.append(dict(panel=pname, book=bname, k=0, seed=-1, cost=cost, kind="control",
                                 events=0, Turn=ctl_turn, dTurn=0.0, **lc,
                                 dSharpe=0.0, dCAGR=0.0, dMaxDD=0.0, dH1=0.0, dH2=0.0,
                                 p4a_ctl=False, p4a_live=pass4a(lc, ll), p4b=pass4b(lc, spy)))
            for k in K_GRID:
                for sd in SEEDS:
                    a = backtest_exit(px, w, null_exit(px, ctl, k, sd), freq=FREQ)
                    at = ann_turn(a, start, px.index)
                    for cost in COST_RUNGS:
                        la = legs(rung(a, cost), start)
                        lc = legs(rung(ctl, cost), start)
                        ll = legs(rung(live, cost), start)
                        rows.append(dict(panel=pname, book=bname, k=k, seed=sd, cost=cost,
                                         kind="noop", events=a["events"], Turn=at,
                                         dTurn=at - ctl_turn, **la,
                                         dSharpe=la["Sharpe"] - lc["Sharpe"],
                                         dCAGR=la["CAGR"] - lc["CAGR"],
                                         dMaxDD=la["MaxDD"] - lc["MaxDD"],
                                         dH1=la["H1"] - lc["H1"], dH2=la["H2"] - lc["H2"],
                                         p4a_ctl=pass4a(la, lc), p4a_live=pass4a(la, ll),
                                         p4b=pass4b(la, spy)))
                print(f"  {pname:9s} {bname} k={k:4d}  done ({len(rows)} rows)")
    df = pd.DataFrame(rows)
    df.to_csv(OUT(".null.csv"), index=False, float_format="%.8f")

    n = df[df.kind == "noop"]
    print("\n  4a pass rate of a CONTENT-FREE clause, vs its OWN control (all grid points):")
    piv = n.pivot_table(index=["panel", "book", "cost"], columns="k", values="p4a_ctl", aggfunc="mean")
    print(piv.to_string(float_format=lambda x: f"{x:.3f}"))
    print("\n  4a pass rate vs the LIVE RULES v2 book:")
    piv2 = n.pivot_table(index=["panel", "book", "cost"], columns="k", values="p4a_live", aggfunc="mean")
    print(piv2.to_string(float_format=lambda x: f"{x:.3f}"))
    print("\n  4b pass rate (vs SPY):")
    piv3 = n.pivot_table(index=["panel", "book", "cost"], columns="k", values="p4b", aggfunc="mean")
    print(piv3.to_string(float_format=lambda x: f"{x:.3f}"))
    print("\n  median |dSharpe| and median dTurn (x/yr) by activity, 10 bps:")
    q = n[n.cost == 10.0].groupby(["panel", "book", "k"]).agg(
        med_absdSharpe=("dSharpe", lambda s: float(np.median(np.abs(s)))),
        med_dTurn=("dTurn", "median"), med_events=("events", "median"),
        rate4a_ctl=("p4a_ctl", "mean"))
    print(q.to_string(float_format=lambda x: f"{x:.6f}"))
    piv.to_csv(OUT(".rate4a_ctl.csv"))
    piv2.to_csv(OUT(".rate4a_live.csv"))
    q.to_csv(OUT(".activity.csv"))

    # [i] the sharper comparison: idea 275's arm cleared 4a at 0, 10 AND 25 bps at once
    w = n.pivot_table(index=["panel", "book", "k", "seed"], columns="cost", values="p4a_ctl")
    w["all3"] = (w[0.0] > 0.5) & (w[10.0] > 0.5) & (w[25.0] > 0.5)
    a3 = w.groupby(level=["panel", "book", "k"])["all3"].mean().unstack("k")
    print("\n  rate at which a CONTENT-FREE clause clears 4a at 0 AND 10 AND 25 bps at once:")
    print(a3.to_string(float_format=lambda x: f"{x:.3f}"))
    a3.to_csv(OUT(".rate4a_all3.csv"))
    print(f"  pooled all-three-rungs rate {w['all3'].mean():.4f} "
          f"({int(w['all3'].sum())} of {len(w)} content-free arms)")
    # activity-MATCHED null: idea 275's arm has |dTurn| = 0.000231 x/yr, so match on dTurn,
    # not on k (its clause front-runs a sale the weekly schedule was going to make anyway).
    dt = n[n.cost == 10.0].set_index(["panel", "book", "k", "seed"])["dTurn"].abs()
    w2 = w.join(dt.rename("adTurn"))
    for tau in (0.02, 0.05, 0.10):
        s = w2[w2.adTurn < tau]
        print(f"  activity-matched (|dTurn| < {tau:4.2f} x/yr): all-three-rungs "
              f"{int(s['all3'].sum())}/{len(s)} ({s['all3'].mean():.4f})   "
              f"single-rung 10 bps {(s[10.0] > 0.5).mean():.4f}")
    print("  the 6 content-free arms that clear 4a at all three rungs:")
    print(w2[w2.all3].to_string(float_format=lambda x: f"{x:.4f}"))
    print("\n  median |dTurn| (x/yr) of a content-free arm by k "
          "(idea 275's 32-event arm: 0.000231):")
    print(n[n.cost == 10.0].pivot_table(index=["panel", "book"], columns="k",
                                        values="dTurn", aggfunc="median")
          .to_string(float_format=lambda x: f"{x:.4f}"))

    # [ii] the census statistic, run inside a controlled experiment
    print("\n  4a-vs-own-control pass rate by |dTurn| bucket (content-free arms, all rungs):")
    b = n.copy()
    b["bucket"] = pd.cut(b.dTurn.abs(), [0, 0.02, 0.05, 0.10, 0.25, 0.50, 1e9],
                         labels=["<0.02", "0.02-0.05", "0.05-0.10", "0.10-0.25", "0.25-0.50", ">0.50"])
    t = b.groupby(["cost", "bucket"], observed=True).agg(
        n=("p4a_ctl", "size"), rate4a=("p4a_ctl", "mean"),
        med_absdSharpe=("dSharpe", lambda s: float(np.median(np.abs(s)))))
    print(t.to_string(float_format=lambda x: f"{x:.4f}"))
    t.to_csv(OUT(".bybucket.csv"))
    return df


# ------------------------------------------------------------------ PART 2: the census
TURN_COLS = ("turn", "turnover", "turn_yr", "turnover_yr", "turn_per_yr", "turn/yr",
             "turn_x_yr", "turn_x", "ann_turnover", "Turn/yr", "Turn_yr", "turnover_x")
DTURN_COLS = ("dturn", "dturnover", "d_turn", "delta_turn")
A4_COLS = ("p4a", "pass4a", "4a", "keep4a", "is4a")
FAIL4A_COLS = ("f4a", "fail4a")
PANEL_COLS = ("panel", "universe", "uni", "book_panel")
COST_COLS = ("cost", "bps", "cost_bps", "cost_rung")
H1_COLS, H2_COLS, DD_COLS = ("H1",), ("H2",), ("MaxDD",)
PANEL_MAP = {
    "u56": "U56", "universe.json": "U56", "universe.json(56)": "U56", "universe.json (56)": "U56",
    "56": "U56", "U56": "U56", "universe": "U56",
    "broad": "BROAD136", "b136": "BROAD136", "broad136": "BROAD136", "universe_broad.json": "BROAD136",
    "universe_broad(136)": "BROAD136", "136": "BROAD136", "bstk100": None,
}
CTRL_VOCAB = re.compile(
    r"^(control|ctrl|base|baseline|none|off|nil|null|do[-_ ]?nothing|donothing|incumbent|"
    r"parent|identity|ewall|ew_all|ew-all|no[-_ ]?clause|no[-_ ]?exit|noclause|nogate|"
    r"ungated|v1|v2|raw|default|-)$", re.I)


def corpus():
    """Every committed backtest csv EXCEPT this script's own outputs (whose columns would
    otherwise be harvested as if they were published results on a re-run)."""
    mine = STEM.name
    fs = sorted(glob.glob(str(ROOT / "research" / "backtests" / "*.csv")) +
                glob.glob(str(ROOT / "research" / "backtests" / "*.csv.gz")))
    return [f for f in fs if not Path(f).name.startswith(mine)]


def is_ctrl(x):
    try:
        return bool(CTRL_VOCAB.match(str(x).strip()))
    except Exception:
        return False


def header(f):
    op = gzip.open if f.endswith(".gz") else open
    with op(f, "rt", errors="replace") as fh:
        return [c.strip().strip('"') for c in fh.readline().strip().split(",")]


def pick(cols, names):
    low = {c.lower(): c for c in cols}
    for n in names:
        if n.lower() in low:
            return low[n.lower()]
    return None


def as_bool(s):
    if s.dtype == bool:
        return s
    return s.astype(str).str.strip().str.lower().isin({"true", "1", "yes", "y", "t"})


def part2(P, base_turn):
    print("\n=== PART 2: census of published 4a passes vs the turnover of what they beat ===")
    files = corpus()
    recs, skipped = [], []
    for f in files:
        name = Path(f).name
        try:
            cols = header(f)
        except Exception:
            skipped.append((name, "unreadable")); continue
        tc = pick(cols, TURN_COLS) or pick(cols, DTURN_COLS)
        ac = pick(cols, A4_COLS)
        fc = pick(cols, FAIL4A_COLS)
        if tc is None or (ac is None and fc is None):
            continue
        pc = pick(cols, PANEL_COLS); cc = pick(cols, COST_COLS)
        h1 = pick(cols, H1_COLS); h2 = pick(cols, H2_COLS); dd = pick(cols, DD_COLS)
        if pc is None:
            skipped.append((name, "no panel column")); continue
        try:
            d = pd.read_csv(f, low_memory=False)
        except Exception:
            skipped.append((name, "parse error")); continue
        if ac is not None:
            p4 = as_bool(d[ac])
        else:                                    # fail-list convention: "-" means it passed
            p4 = d[fc].astype(str).str.strip().isin({"-", "", "nan", "none"})
        pan = d[pc].astype(str).str.strip().str.lower().map(
            lambda v: PANEL_MAP.get(v, PANEL_MAP.get(v.replace(" ", ""), None)))
        m = pd.to_datetime(name[:10], errors="coerce")
        cmp_book = "v2" if (pd.notna(m) and m >= V2_LIVE_DATE) else "v1"
        turn = pd.to_numeric(d[tc], errors="coerce")
        is_delta = tc.lower() in {c.lower() for c in DTURN_COLS}
        sub = pd.DataFrame(dict(
            file=name, panel=pan, p4a=p4.values, turn=turn.values, is_delta=is_delta,
            cmp_book=cmp_book,
            cost=pd.to_numeric(d[cc], errors="coerce").values if cc else np.nan,
            H1=pd.to_numeric(d[h1], errors="coerce").values if h1 else np.nan,
            H2=pd.to_numeric(d[h2], errors="coerce").values if h2 else np.nan,
            MaxDD=pd.to_numeric(d[dd], errors="coerce").values if dd else np.nan))
        sub = sub[sub.panel.notna() & sub.turn.notna()]
        if sub.empty:
            skipped.append((name, "no mapped panel rows")); continue
        recs.append(sub)
    if not recs:
        print("  no census rows"); return pd.DataFrame(), pd.DataFrame()
    C = pd.concat(recs, ignore_index=True)

    # unit sanity: annualised turnover must be plausible; per-file median in [0.05, 200]
    med = C.groupby("file")["turn"].median()
    bad = set(med[(med < 0.02) | (med > 300)].index) - set(C.loc[C.is_delta, "file"])
    C["unit_ok"] = ~C.file.isin(bad)
    C["cmp_turn"] = [base_turn[(p, b)] for p, b in zip(C.panel, C.cmp_book)]
    C["dTurn_cmp"] = np.where(C.is_delta, C.turn.abs(), (C.turn - C.cmp_turn).abs())
    # The full 278k-row census is regenerated by re-running this script; what is COMMITTED is
    # (i) every row inside the region the census makes claims about (dTurn_cmp < 1.0 x/yr) and
    # (ii) a per-file summary of the whole thing.  All headline counts are printed below and
    # in the console log, computed on the full frame.
    C[C.dTurn_cmp < 1.0].to_csv(OUT(".census.csv.gz"), index=False, compression="gzip",
                                float_format="%.6f")
    C.groupby("file").agg(rows=("p4a", "size"), passes=("p4a", "sum"),
                          unit_ok=("unit_ok", "all"),
                          med_dTurn_cmp=("dTurn_cmp", "median"),
                          min_dTurn_cmp=("dTurn_cmp", "min")).to_csv(
        OUT(".censusperfile.csv"), float_format="%.6f")

    ok = C[C.unit_ok]
    P4 = ok[ok.p4a]
    print(f"  files censused {C.file.nunique()}  rows {len(C)}  unit-plausible rows {len(ok)} "
          f"({ok.file.nunique()} files)  published 4a PASSES {len(P4)}")
    print(f"  files skipped: {len(skipped)} (reasons: "
          f"{pd.Series([r for _, r in skipped]).value_counts().to_dict()})")
    q = P4.dTurn_cmp.quantile([0.01, 0.05, 0.10, 0.25, 0.50]).to_dict()
    print("  |turnover - comparand| (x/yr) among published 4a passes, quantiles: " +
          ", ".join(f"q{int(k*100)} {v:.4f}" for k, v in q.items()))
    print("\n  share of published 4a passes within tau x/yr of the book they beat:")
    rows = []
    for tau in TAU_GRID:
        n = int((P4.dTurn_cmp < tau).sum())
        nf = int((ok.loc[~ok.p4a, "dTurn_cmp"] < tau).sum())
        rows.append(dict(tau=tau, passes_within=n, pass_share=n / max(len(P4), 1),
                         fails_within=nf, fail_share=nf / max(int((~ok.p4a).sum()), 1)))
        print(f"    tau {tau:5.3f} x/yr : {n:6d} / {len(P4)} passes ({n/max(len(P4),1):6.2%})   "
              f"| non-passes within tau {nf}/{int((~ok.p4a).sum())} ({nf/max(int((~ok.p4a).sum()),1):6.2%})")
    cen = pd.DataFrame(rows)
    cen.to_csv(OUT(".censusgrid.csv"), index=False)
    return C, cen


def part2b():
    """Tier (b): files that label a control row INSIDE a cell -> exact own-control dTurn."""
    print("\n=== PART 2b: own-control anchor (clause families that publish their control) ===")
    files = corpus()
    recs, anchored = [], []
    for f in files:
        name = Path(f).name
        try:
            cols = header(f)
        except Exception:
            continue
        tc = pick(cols, TURN_COLS)
        ac = pick(cols, A4_COLS)
        if tc is None or ac is None:
            continue
        try:
            d = pd.read_csv(f, low_memory=False)
        except Exception:
            continue
        strc = [c for c in d.columns if str(d[c].dtype) in ("object", "str", "string")]
        lab = None
        for c in strc:                                   # the arm-label column
            v = pd.Series([str(x).strip() for x in d[c].dropna().tolist()], dtype=object)
            if v.map(is_ctrl).any() and v.nunique() > 1:
                lab = c; break
        if lab is None:
            continue
        keys = [c for c in strc if c != lab] + [c for c in (pick(cols, COST_COLS),) if c]
        turn = pd.to_numeric(d[tc], errors="coerce")
        p4 = as_bool(d[ac])
        got = 0
        for _, g in (d.assign(_t=turn, _p=p4).groupby(keys, dropna=False) if keys
                     else [((), d.assign(_t=turn, _p=p4))]):
            isc = pd.Series([is_ctrl(x) for x in g[lab].tolist()], index=g.index)
            if isc.sum() != 1:
                continue
            ct = float(g.loc[isc, "_t"].iloc[0])
            if not np.isfinite(ct):
                continue
            arms = g[~isc]
            for _, r in arms.iterrows():
                if np.isfinite(r["_t"]):
                    recs.append(dict(file=name, label=str(r[lab]), p4a=bool(r["_p"]),
                                     turn=float(r["_t"]), ctl_turn=ct,
                                     dTurn=abs(float(r["_t"]) - ct)))
                    got += 1
        if got:
            anchored.append((name, got))
    if not recs:
        print("  no own-control-anchored rows found"); return pd.DataFrame()
    B = pd.DataFrame(recs)
    B.to_csv(OUT(".owncontrol.csv.gz"), index=False, compression="gzip", float_format="%.6f")
    P4 = B[B.p4a]
    print(f"  files anchored {len(anchored)}   arm rows {len(B)}   published 4a passes {len(P4)}")
    print("  share of own-control-anchored 4a passes within tau x/yr of THEIR OWN control:")
    for tau in TAU_GRID:
        n = int((P4.dTurn < tau).sum())
        nf = int((B.loc[~B.p4a, "dTurn"] < tau).sum())
        print(f"    tau {tau:5.3f} x/yr : {n:5d} / {len(P4)} passes ({n/max(len(P4),1):6.2%})   "
              f"| non-passes {nf}/{int((~B.p4a).sum())} ({nf/max(int((~B.p4a).sum()),1):6.2%})")
    print("  top anchored files by arm count: " +
          ", ".join(f"{n.split('_',1)[1][:38]} ({c})" for n, c in
                    sorted(anchored, key=lambda x: -x[1])[:6]))
    return B


# ------------------------------------------------------------------ PART 3: rule 8
def part3(df, P):
    print("\n=== PART 3: rule 8 walk-forward (activity chosen on 2009-2016 only) ===")
    rows = []
    for (pname, bname), g in df[df.cost == 10.0].groupby(["panel", "book"]):
        px = P[pname]; start = px.index[WARMUP]
        spy = legs(px["SPY"].pct_change().fillna(0.0), start)
        live = legs(rung(backtest_exit(px, rules_v2_weights(px), None, freq=FREQ), 10.0), start)
        ctl = g[g.kind == "control"].iloc[0]
        nul = g[g.kind == "noop"]
        # honest selector: choose k only, on IS Sharpe averaged over seeds
        ks = nul.groupby("k")["IS_Sharpe"].mean()
        k_star = float(ks.idxmax())
        pick_k = nul[nul.k == k_star]
        # overfit selector: choose (k, seed) on IS Sharpe
        best = nul.loc[nul.IS_Sharpe.idxmax()]
        for lbl, arm in (("do-nothing (control)", ctl),
                         (f"noop k*={int(k_star)} (mean of {len(pick_k)} seeds)", pick_k.mean(numeric_only=True)),
                         (f"noop best-IS arm k={int(best.k)} seed={int(best.seed)}", best)):
            rows.append(dict(panel=pname, book=bname, arm=lbl,
                             IS_Sharpe=arm["IS_Sharpe"], OOS_CAGR=arm["OOS_CAGR"],
                             OOS_Sharpe=arm["OOS_Sharpe"], OOS_MaxDD=arm["OOS_MaxDD"]))
        rows.append(dict(panel=pname, book=bname, arm="LIVE RULES v2", IS_Sharpe=live["IS_Sharpe"],
                         OOS_CAGR=live["OOS_CAGR"], OOS_Sharpe=live["OOS_Sharpe"], OOS_MaxDD=live["OOS_MaxDD"]))
        rows.append(dict(panel=pname, book=bname, arm="SPY", IS_Sharpe=spy["IS_Sharpe"],
                         OOS_CAGR=spy["OOS_CAGR"], OOS_Sharpe=spy["OOS_Sharpe"], OOS_MaxDD=spy["OOS_MaxDD"]))
    wf = pd.DataFrame(rows)
    print(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    wf.to_csv(OUT(".walkforward.csv"), index=False)
    return wf


# ------------------------------------------------------------------ PART 4: proposed clause
def part4(C, df, base):
    print("\n=== PART 4: proposed PROTOCOL minimum-activity clause, grid (tau, delta) ===")
    ok = C[C.unit_ok & C.p4a & C.H1.notna() & C.H2.notna()].copy()
    rung_of = ok.cost.where(ok.cost.isin(COST_RUNGS), 10.0).fillna(10.0)
    bH1 = [base[(p, b, c)]["H1"] for p, b, c in zip(ok.panel, ok.cmp_book, rung_of)]
    bH2 = [base[(p, b, c)]["H2"] for p, b, c in zip(ok.panel, ok.cmp_book, rung_of)]
    ok["margin"] = np.minimum(ok.H1.values - np.array(bH1), ok.H2.values - np.array(bH2))
    rows = []
    for tau in TAU_GRID:
        for delta in DELTA_GRID:
            cut = int(((ok.dTurn_cmp < tau) & (ok.margin < delta)).sum())
            rows.append(dict(tau=tau, delta=delta, deleted=cut, of=len(ok),
                             share=cut / max(len(ok), 1)))
    g = pd.DataFrame(rows)
    print(g.pivot(index="tau", columns="delta", values="share").to_string(
        float_format=lambda x: f"{x:.4f}"))
    print(f"  (denominator: {len(ok)} published 4a passes carrying H1/H2 and a plausible turnover unit)")
    # the same clause applied to Part 1's content-free family at 10 bps
    n = df[(df.kind == "noop") & (df.cost == 10.0)]
    p = n[n.p4a_ctl]
    rows2 = []
    marg = np.minimum(p.dH1.values, p.dH2.values)
    for tau in TAU_GRID:
        for delta in DELTA_GRID:
            cut = int(((p.dTurn.abs().values < tau) & (marg < delta)).sum())
            rows2.append(dict(tau=tau, delta=delta, deleted=cut, of=len(p)))
    g2 = pd.DataFrame(rows2)
    print("\n  same clause applied to the content-free family's own 4a passes "
          f"(n={len(p)} at 10 bps): share deleted")
    print(g2.assign(share=g2.deleted / g2["of"].clip(lower=1)).pivot(
        index="tau", columns="delta", values="share").to_string(float_format=lambda x: f"{x:.4f}"))
    g.to_csv(OUT(".clausegrid.csv"), index=False)
    g2.to_csv(OUT(".clausegrid_null.csv"), index=False)
    return g


# ------------------------------------------------------------------ main
def main():
    P = panels()
    for k, v in P.items():
        print(f"panel {k:9s} {v.shape[0]} days x {v.shape[1]} cols  {v.index[0].date()} -> {v.index[-1].date()}")
    G = gates(P)

    print("\n=== baselines (the comparands PROTOCOL 4a names) ===")
    base_turn, base_legs = {}, {}
    for pname, px in P.items():
        start = px.index[WARMUP]
        for bname, fn in BOOKS.items():
            r = backtest_exit(px, fn(px), None, freq=FREQ)
            base_turn[(pname, bname)] = ann_turn(r, start, px.index)
            for c in COST_RUNGS:
                base_legs[(pname, bname, c)] = legs(rung(r, c), start)
            L = base_legs[(pname, bname, 10.0)]
            print(f"  {pname:9s} {bname}  turnover {base_turn[(pname,bname)]:8.4f} x/yr  "
                  f"CAGR {L['CAGR']:7.2%}  Sharpe {L['Sharpe']:.4f}  MaxDD {L['MaxDD']:7.2%}  "
                  f"H1/H2 {L['H1']:.4f}/{L['H2']:.4f}  OOS Sh {L['OOS_Sharpe']:.4f}  (10 bps)")
        spy = legs(px["SPY"].pct_change().fillna(0.0), start)
        print(f"  {pname:9s} SPY  CAGR {spy['CAGR']:7.2%}  Sharpe {spy['Sharpe']:.4f}  "
              f"MaxDD {spy['MaxDD']:7.2%}  H1/H2 {spy['H1']:.4f}/{spy['H2']:.4f}  "
              f"OOS Sh {spy['OOS_Sharpe']:.4f}")

    df = part1(P)
    C, cen = part2(P, base_turn)
    B = part2b()
    wf = part3(df, P)
    if not C.empty:
        part4(C, df, base_legs)

    print("\n=== SUMMARY ===")
    n = df[(df.kind == "noop")]
    for cost in COST_RUNGS:
        s = n[n.cost == cost]
        lo = s[s.k <= 32]; hi = s[s.k >= 256]
        print(f"  {cost:5.1f} bps: content-free 4a-vs-own-control pass rate "
              f"{lo.p4a_ctl.mean():.3f} at k<=32  vs  {hi.p4a_ctl.mean():.3f} at k>=256   "
              f"| 4b {s.p4b.mean():.3f}  | 4a-vs-live {s.p4a_live.mean():.3f}")
    print(f"  gates: A {G['gate_a_ret']:.1e}/{G['gate_a_turn']:.1e}  B {G['gate_b_cost']:.1e}  "
          f"C {G['gate_c_max']:.1e} (events {G['gate_c_events']})")


if __name__ == "__main__":
    main()
