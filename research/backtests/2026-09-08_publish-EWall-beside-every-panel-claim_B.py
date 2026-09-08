#!/usr/bin/env python3
"""Idea 239 — publish-EWall-beside-every-panel-claim (lane B, 2026-09-08).

PRE-REGISTERED QUESTION (QUEUE 239): idea 77 found that the un-ranked `EWall` Sharpe of a
panel predicts that panel's RANKED book's OOS Sharpe BETTER than the ranked book's own IS
Sharpe (+0.857 p 0.024 vs +0.821 p 0.034).  Back-fill that one column over every published
panel/universe claim in the record and report HOW MANY CLAIMS HAVE ZERO EXCESS OVER THEIR
OWN UN-RANKED CONTROL.

TWO TUNED PARAMETERS ONLY:
    p1 = n, the ranked book's width          {5, 10, 20, 40}      (all points reported)
    p2 = CTRL, the un-ranked control's form  {EW_ALL, EW_GATED}   (both points reported)
Everything else is FIXED and pre-registered before any number was read:
    gross G = 0.75 on EVERY arm (ranked and control alike) so no reading is a gross dial
      (QUEUE 244);  cadence = weekly (the record's default);  gate = plain 200d MA, no
      hysteresis;  vol cap = 0.60 (RULES v1's);  de-gross convention `dg` (gated-out weight
      to CASH at 0, never re-spread);  cost rungs {0, 10, 25} bps derived EXACTLY from one
      0-bps run per arm (net(c) = gross - turn*c/1e4);  10 bps is the verdict rung
      (PROTOCOL 2).  Panels are a pre-registered LIST, not a dial.

DEFINITIONS
    EW_ALL   : every name priced that day, weight G/N_priced.  No gate, no ranking.
    EW_GATED : every name priced AND above its 200d MA, weight G/N_priced (the gated-out
               weight goes to cash — the denominator is N_priced, not N_above).
    RANKED(n): the record's composite (12-1 + 6m + 3m rank-average, no vol scaling), gated
               by the same 200d MA and vol20 < 0.60, top n by composite, weight G/n.
    EXCESS   := Sharpe(RANKED(n)) - Sharpe(CTRL) on the SAME panel, SAME rung, SAME cadence,
               SAME gross.  "Zero excess" := EXCESS <= 0.

PANELS (pre-registered, 23):  U56, B136, SMALL439 (small panel filtered to
max_1d_move < 1.0, per data/SMALL_PANEL_README.md), plus 10 random k=80 sub-panels of B136
and 10 random k=200 sub-panels of SMALL439 (seeds 0-9, drawn before any Sharpe was read).
The 20 sub-panels exist ONLY to give idea 77's cross-panel correlation more than 7 points;
they are not separate claims.
SURVIVORSHIP: SMALL439 and its sub-panels are current constituents of the sub-$2B screen
(data/SMALL_PANEL_README.md); B136 is current constituents of universe_broad.json
(PROTOCOL 9).  Every panel-level reading below is RELATIVE, never achievable.

PARTS
 A  ARCHIVE CENSUS (fixed, single detection rule, not tuned): every committed backtest
    script/memo that makes a multi-panel claim — does it publish an un-ranked control?
 B  LIVE EXCESS: 23 panels x 4 widths x 2 controls x 3 rungs.  Excess full / H1 / H2 / OOS,
    with both KEEP paths (4a vs RULES v2 on the same panel, 4b vs SPY) on EVERY grid point.
 C  IDEA 77's PREDICTOR: across panels, does CTRL's IS Sharpe beat the ranked book's own IS
    Sharpe at predicting the ranked book's OOS Sharpe?  Pearson + Spearman on all 23 panels,
    plus the 7-panel subsample distribution (idea 77's own n) to say whether +0.857 vs
    +0.821 is separable at that sample size.
 D  RULE 8 WALK-FORWARD: (n, CTRL) chosen on 2009-2016 IS Sharpe only, 2017-2026 read once,
    against the do-nothing control, RULES v2 and SPY.

Outputs (all committed):
    .census.csv       Part A: one row per detected multi-panel file
    .grid.csv         Part B: every (panel, n, ctrl, rung) point with 4a/4b bars
    .excess.csv       Part B: the zero-excess tally by (rung, ctrl, window)
    .predictor.csv    Part C: correlations, full-corpus and 7-panel subsamples
    .walkforward.csv  Part D: IS pick per (panel, rung), OOS read once
"""
import re
import sys
import time
import warnings
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics                                          # noqa: E402

OUT = Path(__file__).with_suffix("")
BT = ROOT / "research" / "backtests"
SELF = Path(__file__).name

RUNGS = [0, 10, 25]
VERDICT_RUNG = 10
NS = [5, 10, 20, 40]                 # p1
CTRLS = ["EW_ALL", "EW_GATED"]       # p2
GROSS = 0.75
MAX_VOL = 0.60
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SEEDS = list(range(10))


# ------------------------------------------------------------------ machinery (idea 231's)
def week_mask(idx):
    per = idx.to_period("W")
    s = pd.Series(per, index=idx)
    return (s != s.shift(-1)).values


def simulate(px, W, mask):
    """Weights decided at t, applied at t+1; drift between rebalances (engine.backtest)."""
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(px.index).fillna(0.0).shift(1).values
    m = np.concatenate([[False], mask[:-1]])
    cur = np.zeros(px.shape[1])
    held = np.empty_like(rets)
    turn = np.zeros(len(px))
    for i in range(len(px)):
        if m[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            cur = growth / tot
    return (pd.Series((held * rets).sum(axis=1), index=px.index),
            pd.Series(turn, index=px.index),
            pd.Series(held.sum(axis=1), index=px.index))


def net(gross, turn, bps):
    return gross - turn * bps / 1e4


def stats(r):
    m = metrics(r)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def bars_4a(s, b):
    f = []
    if not s["H1"] > b["H1"]: f.append("H1")
    if not s["H2"] > b["H2"]: f.append("H2")
    if not s["MaxDD"] >= b["MaxDD"]: f.append("DD")
    return ",".join(f)


def bars_4b(s, spy, oos_s, oos_spy):
    f = []
    if not s["H1"] > spy["H1"]: f.append("H1")
    if not s["H2"] > spy["H2"]: f.append("H2")
    if not oos_s > oos_spy: f.append("OOS")
    if not s["MaxDD"] >= 0.60 * spy["MaxDD"]: f.append("DD")
    if not s["CAGR"] >= 0.70 * spy["CAGR"]: f.append("CAGR")
    return ",".join(f)


# ------------------------------------------------------------------ the three book forms
def ranked_weights(px, comp, above, vol20, n):
    elig = comp.where(above & (vol20 < MAX_VOL))
    return (elig.rank(axis=1, ascending=False) <= n).astype(float) * (GROSS / n)


def ew_weights(px, above, gated):
    """Equal weight over names PRICED that day at GROSS/N_priced; if gated, hold only the
    names above their 200d MA and let the rest of the weight sit in cash (dg convention)."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(above, 0.0) if gated else ew


# ------------------------------------------------------------------ Part A: archive census
PANEL_TOKENS = {
    "U56": (r"\bu56\b", r"\bU56\b", r"universe\.json"),
    "B136": (r"\bb136\b", r"\bB136\b", r"broad136", r"broad=True", r"universe_broad"),
    "SMALL": (r"SMALL4\d\d", r"small=True", r"prices_small"),
}
CTRL_TOKENS = (r"\bEW[_ -]?ALL\b", r"\bEWall\b", r"\bEWALL\b", r"ew-all", r"ew_all",
               r"un-?ranked", r"unranked", r"equal[- ]weight all", r"\bEWA\b")
CLAIM_WORDS = (r"panel", r"universe")


def census():
    rows = []
    files = sorted(list(BT.glob("*.py")) + list(BT.glob("*.md")))
    for f in files:
        if f.name == SELF:
            continue
        try:
            txt = f.read_text(errors="ignore")
        except Exception:
            continue
        hits = {k: any(re.search(p, txt) for p in pats) for k, pats in PANEL_TOKENS.items()}
        n_panels = sum(hits.values())
        if n_panels < 2:
            continue                       # single-panel files make no cross-panel claim
        if not any(re.search(w, txt, re.I) for w in CLAIM_WORDS):
            continue
        has_ctrl = any(re.search(p, txt) for p in CTRL_TOKENS)
        rows.append(dict(file=f.name, kind=f.suffix, n_panel_tokens=n_panels,
                         u56=hits["U56"], b136=hits["B136"], small=hits["SMALL"],
                         has_unranked_control=has_ctrl))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ Parts B-D
def build_panels():
    """Pre-registered panel list.  SPY is a benchmark column, never a constituent."""
    out = []
    u56 = load_universe()
    b136 = load_universe(broad=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv", index_col=0)
    sm = load_universe(small=True)
    keep = [c for c in sm.columns if c == "SPY" or meta.max_1d_move.get(c, 0) < 1.0]
    small = sm[keep]
    out.append(("U56", u56, "named"))
    out.append(("B136", b136, "named"))
    out.append(("SMALL439", small, "named"))
    for s in SEEDS:
        cols = [c for c in b136.columns if c != "SPY"]
        pick = list(pd.Series(cols).sample(80, random_state=s))
        out.append((f"B80_s{s}", b136[pick + ["SPY"]], "sub"))
    for s in SEEDS:
        cols = [c for c in small.columns if c != "SPY"]
        pick = list(pd.Series(cols).sample(200, random_state=s))
        out.append((f"SM200_s{s}", small[pick + ["SPY"]], "sub"))
    return out


def run():
    t0 = time.time()
    grid, wf, pred_rows, ident = [], [], [], []
    for pname, px, kind in build_panels():
        s_ns, above, vol20 = score(px, vol_scale=False)
        comp = s_ns / (0.5 + 0.5 * above.astype(float))
        mask = week_mask(px.index)
        start = px.index[260]
        spy_r = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_s = stats(spy_r)
        spy_oos = metrics(spy_r.loc[OOS_START:])

        # baselines on this panel (RULES v2 live book, RULES v1 previous)
        v2g, v2t, _ = simulate(px, rules_v2_weights(px), mask)
        v1g, v1t, _ = simulate(px, rules_v1_weights(px), mask)
        base = {c: stats(net(v2g, v2t, c).loc[start:]) for c in RUNGS}
        base_oos = {c: metrics(net(v2g, v2t, c).loc[OOS_START:]) for c in RUNGS}
        v1_row = {c: stats(net(v1g, v1t, c).loc[start:]) for c in RUNGS}

        # GATE: the fast path must reproduce engine.backtest exactly on this panel
        if kind == "named":
            eng = backtest(px, rules_v1_weights(px), cost_bps=10, freq="W")["returns"].loc[start:]
            ident.append(dict(panel=pname,
                              max_abs_diff=float(np.abs(eng - net(v1g, v1t, 10).loc[start:]).max())))

        arms = {}
        for ctrl in CTRLS:
            W = ew_weights(px, above, gated=(ctrl == "EW_GATED"))
            g, t, h = simulate(px, W, mask)
            arms[("CTRL", ctrl)] = (g.loc[start:], t.loc[start:], h.loc[start:])
        for n in NS:
            if n > px.shape[1] - 1:
                continue
            W = ranked_weights(px, comp, above, vol20, n)
            g, t, h = simulate(px, W, mask)
            arms[("RANKED", n)] = (g.loc[start:], t.loc[start:], h.loc[start:])

        def read(key, c):
            g, t, h = arms[key]
            r = net(g, t, c)
            st = stats(r)
            return r, st, metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:]), float(h.mean()), \
                float(t.sum() / (len(g) / 252))

        for c in RUNGS:
            ctrl_read = {ct: read(("CTRL", ct), c) for ct in CTRLS}
            for ct, (r0, st0, is0, oo0, gr0, tu0) in ctrl_read.items():
                grid.append(dict(panel=pname, panel_kind=kind, arm="CTRL", ctrl=ct, n=np.nan,
                                 bps=c, mean_gross=gr0, turn_yr=tu0, **st0,
                                 IS_Sharpe=is0["Sharpe"], OOS_Sharpe=oo0["Sharpe"],
                                 OOS_CAGR=oo0["CAGR"], OOS_MaxDD=oo0["MaxDD"],
                                 excess=0.0, excess_H1=0.0, excess_H2=0.0, excess_OOS=0.0,
                                 fail4a=bars_4a(st0, base[c]),
                                 fail4b=bars_4b(st0, spy_s, oo0["Sharpe"], spy_oos["Sharpe"])))
            for n in NS:
                if ("RANKED", n) not in arms:
                    continue
                r, st, iss, oo, gr, tu = read(("RANKED", n), c)
                for ct in CTRLS:
                    _, st0, is0, oo0, _, _ = ctrl_read[ct]
                    grid.append(dict(panel=pname, panel_kind=kind, arm="RANKED", ctrl=ct, n=n,
                                     bps=c, mean_gross=gr, turn_yr=tu, **st,
                                     IS_Sharpe=iss["Sharpe"], OOS_Sharpe=oo["Sharpe"],
                                     OOS_CAGR=oo["CAGR"], OOS_MaxDD=oo["MaxDD"],
                                     ctrl_Sharpe=st0["Sharpe"], ctrl_IS_Sharpe=is0["Sharpe"],
                                     ctrl_OOS_Sharpe=oo0["Sharpe"],
                                     excess=st["Sharpe"] - st0["Sharpe"],
                                     excess_H1=st["H1"] - st0["H1"],
                                     excess_H2=st["H2"] - st0["H2"],
                                     excess_OOS=oo["Sharpe"] - oo0["Sharpe"],
                                     fail4a=bars_4a(st, base[c]),
                                     fail4b=bars_4b(st, spy_s, oo["Sharpe"], spy_oos["Sharpe"])))

            # ---- Part C rows: one per (panel, rung, n) with both predictors on the same line
            for n in NS:
                if ("RANKED", n) not in arms:
                    continue
                r, st, iss, oo, gr, tu = read(("RANKED", n), c)
                row = dict(panel=pname, panel_kind=kind, bps=c, n=n,
                           book_IS_Sharpe=iss["Sharpe"], book_OOS_Sharpe=oo["Sharpe"])
                for ct in CTRLS:
                    _, st0, is0, oo0, _, _ = ctrl_read[ct]
                    row[f"{ct}_IS_Sharpe"] = is0["Sharpe"]
                    row[f"{ct}_OOS_Sharpe"] = oo0["Sharpe"]
                pred_rows.append(row)

            # ---- Part D: rule 8.  (n, ctrl) chosen on IS Sharpe only, OOS read once.
            cand = {}
            for n in NS:
                if ("RANKED", n) in arms:
                    cand[("RANKED", n, "-")] = read(("RANKED", n), c)
            for ct in CTRLS:
                cand[("CTRL", np.nan, ct)] = read(("CTRL", ct), c)
            pick = max(cand, key=lambda k: cand[k][2]["Sharpe"])
            pick_r, pick_st, pick_is, pick_oo, pick_gr, pick_tu = cand[pick]
            dn = cand[("CTRL", np.nan, "EW_ALL")]
            full_arg = max(cand, key=lambda k: cand[k][1]["Sharpe"])
            wf.append(dict(panel=pname, panel_kind=kind, bps=c,
                           pick_arm=pick[0], pick_n=pick[1], pick_ctrl=pick[2],
                           full_argmax=f"{full_arg[0]}{full_arg[1]}{full_arg[2]}",
                           IS_Sharpe=pick_is["Sharpe"],
                           OOS_Sharpe=pick_oo["Sharpe"], OOS_CAGR=pick_oo["CAGR"],
                           OOS_MaxDD=pick_oo["MaxDD"],
                           dn_OOS_Sharpe=dn[3]["Sharpe"], dn_OOS_CAGR=dn[3]["CAGR"],
                           dn_OOS_MaxDD=dn[3]["MaxDD"],
                           v2_OOS_Sharpe=base_oos[c]["Sharpe"], v2_OOS_CAGR=base_oos[c]["CAGR"],
                           v2_OOS_MaxDD=base_oos[c]["MaxDD"],
                           spy_OOS_Sharpe=spy_oos["Sharpe"], spy_OOS_CAGR=spy_oos["CAGR"],
                           spy_OOS_MaxDD=spy_oos["MaxDD"],
                           v1_Sharpe=v1_row[c]["Sharpe"],
                           fail4a=bars_4a(pick_st, base[c]),
                           fail4b=bars_4b(pick_st, spy_s, pick_oo["Sharpe"], spy_oos["Sharpe"])))
        print(f"  {pname:10s} {px.shape[1]-1:4d} names  {time.time()-t0:6.1f}s", flush=True)
    return (pd.DataFrame(grid), pd.DataFrame(wf), pd.DataFrame(pred_rows),
            pd.DataFrame(ident))


# ------------------------------------------------------------------ Part C statistics
# scipy is not installed in the sandbox, so the two-sided Student-t p-value is computed
# EXACTLY from the regularised incomplete beta (Lentz continued fraction), not approximated.
def _betacf(a, b, x, itmax=300, eps=3e-16, fpmin=1e-300):
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < fpmin: d = fpmin
    d = 1.0 / d
    h = d
    for m in range(1, itmax + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin: d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin: c = fpmin
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin: d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin: c = fpmin
        d = 1.0 / d
        de = d * c
        h *= de
        if abs(de - 1.0) < eps:
            break
    return h


def _betai(a, b, x):
    import math
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    lb = (math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
          + a * math.log(x) + b * math.log1p(-x))
    bt = math.exp(lb)
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def _t_sf2(t, df):
    """Two-sided survival function of Student's t."""
    return float(_betai(0.5 * df, 0.5, df / (df + t * t)))


def _pearson(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    n = len(x)
    if n < 3 or x.std() == 0 or y.std() == 0:
        return np.nan, np.nan, n
    r = float(np.corrcoef(x, y)[0, 1])
    if abs(r) >= 1:
        return r, 0.0, n
    t = r * np.sqrt((n - 2) / (1 - r * r))
    return r, _t_sf2(t, n - 2), n


def _spearman(x, y):
    xs = pd.Series(x).rank()
    ys = pd.Series(y).rank()
    return _pearson(xs, ys)


def predictor_table(pred):
    rows = []
    for c in RUNGS:
        for n in NS:
            sub = pred[(pred.bps == c) & (pred.n == n)]
            if len(sub) < 5:
                continue
            for ct in CTRLS:
                r_c, p_c, nn = _pearson(sub[f"{ct}_IS_Sharpe"], sub.book_OOS_Sharpe)
                r_b, p_b, _ = _pearson(sub.book_IS_Sharpe, sub.book_OOS_Sharpe)
                sr_c, sp_c, _ = _spearman(sub[f"{ct}_IS_Sharpe"], sub.book_OOS_Sharpe)
                sr_b, sp_b, _ = _spearman(sub.book_IS_Sharpe, sub.book_OOS_Sharpe)
                # idea 77's own sample size: how often does the control win on 7 panels?
                wins = tot = 0
                idx = list(sub.index)
                if len(idx) >= 7:
                    combos = list(combinations(range(len(idx)), 7))
                    rng = np.random.default_rng(0)
                    if len(combos) > 2000:
                        sel = rng.choice(len(combos), 2000, replace=False)
                        combos = [combos[i] for i in sel]
                    for cb in combos:
                        s7 = sub.iloc[list(cb)]
                        a, _, _ = _pearson(s7[f"{ct}_IS_Sharpe"], s7.book_OOS_Sharpe)
                        b, _, _ = _pearson(s7.book_IS_Sharpe, s7.book_OOS_Sharpe)
                        if np.isfinite(a) and np.isfinite(b):
                            tot += 1
                            wins += int(a > b)
                rows.append(dict(bps=c, n=n, ctrl=ct, n_panels=nn,
                                 r_ctrl=r_c, p_ctrl=p_c, r_book=r_b, p_book=p_b,
                                 d_r=r_c - r_b, rho_ctrl=sr_c, rho_book=sr_b,
                                 d_rho=sr_c - sr_b,
                                 sub7_n=tot, sub7_ctrl_wins=wins,
                                 sub7_win_rate=(wins / tot if tot else np.nan)))
    return pd.DataFrame(rows)


def excess_table(grid):
    rk = grid[grid.arm == "RANKED"]
    rows = []
    for c in RUNGS:
        for ct in CTRLS:
            for win, col in (("full", "excess"), ("H1", "excess_H1"),
                             ("H2", "excess_H2"), ("OOS", "excess_OOS")):
                sub = rk[(rk.bps == c) & (rk.ctrl == ct)]
                v = sub[col].dropna()
                rows.append(dict(bps=c, ctrl=ct, window=win, n_cells=len(v),
                                 zero_or_neg=int((v <= 0).sum()),
                                 share_zero=float((v <= 0).mean()) if len(v) else np.nan,
                                 mean=float(v.mean()), median=float(v.median()),
                                 q10=float(v.quantile(0.10)), q90=float(v.quantile(0.90))))
    return pd.DataFrame(rows)


def main():
    print("=" * 100)
    print("Idea 239 — publish-EWall-beside-every-panel-claim (lane B)")
    print("=" * 100)

    cen = census()
    cen.to_csv(f"{OUT}.census.csv", index=False)
    print(f"\nPART A — archive census: {len(cen)} committed files make a multi-panel claim; "
          f"{int(cen.has_unranked_control.sum())} name an un-ranked control "
          f"({cen.has_unranked_control.mean():.1%}).")
    print(cen.groupby("kind").has_unranked_control.agg(["size", "sum", "mean"]).to_string())
    print("  by panel-token count:")
    print(cen.groupby("n_panel_tokens").has_unranked_control.agg(["size", "sum", "mean"]).to_string())

    print("\nPART B — running 23 panels x (4 widths + 2 controls) x 3 rungs ...")
    grid, wf, pred, ident = run()
    grid.to_csv(f"{OUT}.grid.csv", index=False)
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)

    print("\nGATE — fast path vs engine.backtest (RULES v1, 10 bps, weekly):")
    print(ident.to_string(index=False, float_format=lambda x: f"{x:.3e}"))

    exc = excess_table(grid)
    exc.to_csv(f"{OUT}.excess.csv", index=False)
    print("\nZERO-EXCESS TALLY (ranked book minus its own un-ranked control, same panel/rung):")
    print(exc.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print(f"\nVERDICT RUNG ({VERDICT_RUNG} bps), named panels only:")
    v = grid[(grid.bps == VERDICT_RUNG) & (grid.panel_kind == "named") & (grid.arm == "RANKED")]
    print(v[["panel", "n", "ctrl", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
             "excess", "excess_OOS", "mean_gross", "fail4a", "fail4b"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print("\nControls on the named panels:")
    cv = grid[(grid.bps == VERDICT_RUNG) & (grid.panel_kind == "named") & (grid.arm == "CTRL")]
    print(cv[["panel", "ctrl", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
              "mean_gross", "turn_yr", "fail4a", "fail4b"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    pr = predictor_table(pred)
    pr.to_csv(f"{OUT}.predictor.csv", index=False)
    print("\nPART C — idea 77's predictor across 23 panels (r = Pearson vs book OOS Sharpe):")
    print(pr.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"\n  control beats own-IS on Pearson in {int((pr.d_r > 0).sum())}/{len(pr)} cells; "
          f"on Spearman in {int((pr.d_rho > 0).sum())}/{len(pr)}.")
    print(f"  7-panel subsample win rate for the control: "
          f"{pr.sub7_win_rate.min():.3f}-{pr.sub7_win_rate.max():.3f} "
          f"(mean {pr.sub7_win_rate.mean():.3f}).")

    print("\nPART D — rule 8 walk-forward (IS 2009-2016 -> OOS 2017-2026, read once):")
    print(wf[wf.panel_kind == "named"]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    w = wf
    print(f"\n  chooser beats do-nothing OOS in {int((w.OOS_Sharpe > w.dn_OOS_Sharpe).sum())}/{len(w)} cells; "
          f"beats RULES v2 OOS in {int((w.OOS_Sharpe > w.v2_OOS_Sharpe).sum())}/{len(w)}; "
          f"beats SPY OOS in {int((w.OOS_Sharpe > w.spy_OOS_Sharpe).sum())}/{len(w)}.")
    print(f"  IS pick is an un-ranked CONTROL in {int((w.pick_arm == 'CTRL').sum())}/{len(w)} cells.")

    n4a = int((grid.fail4a == "").sum())
    n4b = int((grid.fail4b == "").sum())
    print(f"\nKEEP PATHS over all {len(grid)} grid points: 4a {n4a}/{len(grid)}, 4b {n4b}/{len(grid)}.")
    if n4b:
        print(grid[grid.fail4b == ""][["panel", "arm", "ctrl", "n", "bps", "CAGR", "Sharpe",
                                       "MaxDD", "H1", "H2", "OOS_Sharpe"]]
              .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print("\nWrote:", ", ".join(Path(p).name for p in
                                [f"{OUT}.census.csv", f"{OUT}.grid.csv", f"{OUT}.excess.csv",
                                 f"{OUT}.predictor.csv", f"{OUT}.walkforward.csv"]))


if __name__ == "__main__":
    main()
