#!/usr/bin/env python3
"""
Idea 1257 (lane C, 2026-09-17) — is the 2026-09-04 KEEP 4b BOOK a THREE-LEG COMPOSITE or
ONE LEG WEARING THREE?

THE PREMISE.  The standing candidate ranks names on the MEAN OF THREE PERCENTILE RANKS —
12-1 momentum (skip 21, look 252), 6m (0,126) and 3m (0,63).  All three are computed on the
SAME price path over NESTED windows, so they are not three pieces of evidence; they are three
readings of one series.  The record has walked N, GROSS, cadence, phase, H, the panel and the
years on this book.  IT HAS NEVER WALKED THE SIGNAL ITSELF.  That matters for capital two ways:
if the legs are near-collinear the RULES wording claims a blend it does not have (and carries
three unstated lookbacks instead of one), and if a SINGLE leg matches the blend out of sample
then the simpler rule is the one to write, because it has fewer dials to overfit.

WHAT IS MEASURED, STATED BEFORE ANY NUMBER IS READ.  The frozen 2026-09-04 book is rebuilt
from scratch with its composite replaced by each of the 7 NON-EMPTY SUBSETS of the three legs,
under 2 combination rules.  Nothing else moves: eligibility (above own 200d MA AND vol20 <
0.60), N = 20, H = 126, GROSS = 0.75, weekly cadence (decide Friday / trade Monday), gated-out
weight to CASH, 10 bps, t+1 execution, 260-row warm-up.  The (M12_1, M6, M3) / MEAN cell IS the
committed anchor and is used as a reproduction gate.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
    LEG SUBSET  all 7 non-empty subsets of {M12_1 = (skip 21, look 252),
                M6 = (0, 126), M3 = (0, 63)}
    COMB RULE   {MEAN, MIN} — MEAN is the record's (average of the legs' cross-sectional
                percentile ranks); MIN is a CONSENSUS rule (a name ranks at its WEAKEST leg),
                which is the natural alternative when legs are meant to be separate evidence.
                On singletons the two rules are the SAME object by construction — gate G2.
Every (subset, rule) cell published.  NOT DIALS, reported at every value: PANEL {U56, B136,
SMALL663} (rule 9); the 4a and 4b legs individually; full / halves / IS / OOS; the rule-8
chooser and its do-nothing control.

PRE-DECLARED OUTCOMES, written before the tape is read:
  (A) DEGENERATE — the legs are near-collinear (mean cross-sectional Spearman >= 0.70 for every
      pair) AND OOS Sharpe spread over all 14 cells on U56 < 0.10.  Then the composite is one
      leg wearing three and the RULES line overstates its own evidence.
  (B) BLEND-CARRIED — at least one subset LOSES the 4b pass while the 3-leg MEAN keeps it, and
      the 3-leg MEAN is within 0.02 of the best OOS Sharpe.  Then the blend is doing work.
  (C) A SINGLE LEG BEATS THE BLEND out of sample AND rule 8 REACHES it (the IS argmax names
      that cell).  Then this is a genuine SIMPLIFICATION candidate and a memo is owed.
  (D) THE CHOOSER LOSES TO DOING NOTHING — the rule-8 IS argmax lands on a cell with worse OOS
      Sharpe than always taking the record's 3-leg MEAN.  Then the signal axis is another dial
      the record cannot resolve, and the answer is KILL with the incumbent left standing.

RULE 8 (walk-forward).  The (subset, rule) cell is chosen by IS SHARPE on warm-up..2016-12-31
ONLY; 2017-2026 is read ONCE.  Reported beside the do-nothing anchor (always the record's 3-leg
MEAN) on every panel, because this record has repeatedly found choosers that lose to doing
nothing and a chooser that cannot beat the incumbent is not a finding, it is a cost.

PROTOCOL: rule 2 costs (10 bps) and t+1 execution; rule 3 baseline = RULES v2 live AND SPY;
rule 4 both KEEP paths at every cell, 2 dials; rule 5 one idea, deterministic, standalone;
rule 8 as above; rule 9 survivorship stated below.  RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py are NOT modified.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists; SMALL663 is a current
sub-$2B screen (52 of 715 dropped for max_1d_move >= 1.0).  Every level below is optimistic and
every 4b pass is an upper bound.  The headline here is a DIFFERENCE between signal variants
scored on the SAME panel with the same eligibility and the same N, so it is first-order immune
to a level bias that moves all 14 cells together; 1255 prices the panel bias itself.

Book machinery (Panel / build / run) is adapted unchanged from idea 1255's committed script so
that the anchor cell reproduces the committed number rather than a near-miss.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-17_is-the-2026-09-04-KEEP-4b-BOOK-a-THREE-LEG-COMPOSITE-or-ONE-LEG-WEARING-THREE_C.py
"""
from __future__ import annotations

import itertools
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "is-the-2026-09-04-KEEP-4b-BOOK-a-THREE-LEG-COMPOSITE-or-ONE-LEG-WEARING-THREE"
OUT = ROOT / "research" / "backtests"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
A_N, A_H, A_G = 20, 126, 0.75

LEGDEF = {"M12_1": (21, 252), "M6": (0, 126), "M3": (0, 63)}
LEGNAMES = ["M12_1", "M6", "M3"]
SUBSETS = [tuple(s) for k in (1, 2, 3)
           for s in itertools.combinations(LEGNAMES, k)]          # DIAL 1: 7 subsets
COMBS = ["MEAN", "MIN"]                                           # DIAL 2
ANCHOR_CELL = (("M12_1", "M6", "M3"), "MEAN")
# committed 2026-09-04 U56 triple (CHANGELOG 2026-09-17 idea 1254/1255 replay)
COMMITTED = dict(CAGR=0.1571, Sharpe=1.1480, MaxDD=-0.1913)

GATES: list[dict] = []


def say(*a):
    print(" ".join(str(x) for x in a), flush=True)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    say(f"   GATE {name:12s} {'PASS' if ok else 'FAIL'}  value={value}  target={target}")
    return bool(ok)


def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    r = np.asarray(r, float)
    e = float(np.prod(1.0 + r))
    return e ** (252.0 / len(r)) - 1.0


def mdd(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1.0).min())


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def windows(idx, r):
    n = len(r)
    h = n // 2
    o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]), oos=stats(r[o:]), is_=stats(r[:o]))


def flat(w):
    return {f"{k}_{m}": x for k, v in w.items() for m, x in v.items()}


def leg_ranks(q):
    """Cross-sectional percentile rank of each leg, as a dict name -> DataFrame."""
    out = {}
    for nm, (skip, look) in LEGDEF.items():
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        out[nm] = x.rank(axis=1, pct=True)
    return out


def mech(q, ranks, subset, comb):
    """Score for a given leg subset + combination rule. Eligibility never moves."""
    parts = [ranks[nm] for nm in subset]
    if comb == "MEAN":
        comp = sum(parts) / len(parts)
    elif comb == "MIN":
        comp = parts[0]
        for p in parts[1:]:
            comp = np.minimum(comp, p)
    else:
        raise ValueError(comb)
    above = (q > q.rolling(200).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    sc = (np.asarray(comp) * (0.5 + 0.5 * above.astype(float)))
    return sc, above, np.nan_to_num(vol20, nan=1e9)


class Panel:
    """Frozen book machinery (adapted from idea 1255), parameterised by the signal only."""

    def __init__(self, name, px, invest, ranks, subset, comb):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        sc, above, vol20 = mech(px[invest], ranks, subset, comb)
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)


def build(pan, N=A_N, H=A_H, lag=1):
    reb = pan.reb
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    for i, t in enumerate(reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.rank_key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def run(pan, Wt, gross=A_G):
    rets = pan.rets
    T, M = rets.shape
    reb = pan.reb
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
        w0 = gross * Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    r = (held * rets).sum(axis=1) - turn * COST / 1e4
    ann_turn = turn.sum() / (T / 252.0)
    return r, ann_turn


def legs_4a(book, live):
    return dict(H1=book["h1"]["Sharpe"] > live["h1"]["Sharpe"],
                H2=book["h2"]["Sharpe"] > live["h2"]["Sharpe"],
                DD=book["full"]["MaxDD"] >= live["full"]["MaxDD"])


def legs_4b(book, spy):
    return dict(H1=book["h1"]["Sharpe"] > spy["h1"]["Sharpe"],
                H2=book["h2"]["Sharpe"] > spy["h2"]["Sharpe"],
                OOS=book["oos"]["Sharpe"] > spy["oos"]["Sharpe"],
                DD=book["full"]["MaxDD"] >= DD_CAP * spy["full"]["MaxDD"],
                CAGR=book["full"]["CAGR"] >= CAGR_FLOOR * spy["full"]["CAGR"])


def mean_xs_spearman(ra, rb, step=21):
    """Mean cross-sectional Spearman between two percentile-rank frames (sampled every `step`)."""
    A, B = ra.values, rb.values
    out = []
    for i in range(0, len(A), step):
        a, b = A[i], B[i]
        m = np.isfinite(a) & np.isfinite(b)
        if m.sum() < 5:
            continue
        x, y = pd.Series(a[m]).rank().values, pd.Series(b[m]).rank().values
        sx, sy = x.std(ddof=0), y.std(ddof=0)
        if sx == 0 or sy == 0:
            continue
        out.append(((x - x.mean()) * (y - y.mean())).mean() / (sx * sy))
    return float(np.mean(out)) if out else float("nan")


def main():
    t0 = time.time()
    say(f"# {DATE} idea 1257 lane C — {SLUG}")
    say(f"# frozen book: eligibility above-200d & vol20<{MAXVOL}, N={A_N}, H={A_H}, GROSS={A_G},")
    say(f"# weekly (decide Fri / trade Mon), {COST:.0f} bps, t+1, {WARMUP}-row warm-up. ONLY the")
    say(f"# ranking signal moves: {len(SUBSETS)} leg subsets x {len(COMBS)} combination rules = "
        f"{len(SUBSETS)*len(COMBS)} cells per panel, ALL published.")

    px_u = load_universe()
    px_b = load_universe(broad=True)
    px_s = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_inv = [c for c in px_s.columns if c != "SPY" and c not in bad]
    panels = [("U56", px_u, [c for c in px_u.columns if c != "SPY"]),
              ("B136", px_b, [c for c in px_b.columns if c != "SPY"]),
              (f"SMALL{len(s_inv)}", px_s, s_inv)]
    say(f"# SMALL: {px_s.shape[1]-1} names, {len(bad & set(px_s.columns))} dropped for max_1d_move >= 1.0")

    rows, corr_rows, r8_rows = [], [], []
    for name, px, inv in panels:
        ranks = leg_ranks(px[inv])
        # --- collinearity of the three legs, in the space the book actually uses (ranks) ---
        say(f"\n## {name}  {len(inv)} investable")
        say("   mean cross-sectional Spearman between leg percentile ranks (sampled monthly):")
        for a, b in itertools.combinations(LEGNAMES, 2):
            rho = mean_xs_spearman(ranks[a], ranks[b])
            corr_rows.append(dict(panel=name, leg_a=a, leg_b=b, mean_xs_spearman=rho))
            say(f"     {a:6s} vs {b:6s}  rho = {rho:+.4f}")

        pan_a = Panel(name, px, inv, ranks, *ANCHOR_CELL)
        idx = pan_a.idx[WARMUP:]
        spy = windows(idx, pan_a.spy[WARMUP:])
        live = windows(idx, backtest(px, rules_v2_weights(px), cost_bps=COST, freq="W")["returns"].values[WARMUP:])
        say(f"   window {idx[0].date()}..{idx[-1].date()}")
        say(f"   SPY     full {spy['full']['CAGR']:7.2%} / {spy['full']['Sharpe']:.4f} / {spy['full']['MaxDD']:7.2%}"
            f"  halves {spy['h1']['Sharpe']:.4f}/{spy['h2']['Sharpe']:.4f}"
            f"  OOS {spy['oos']['CAGR']:7.2%} / {spy['oos']['Sharpe']:.4f} / {spy['oos']['MaxDD']:7.2%}")
        say(f"   LIVE v2 full {live['full']['CAGR']:7.2%} / {live['full']['Sharpe']:.4f} / {live['full']['MaxDD']:7.2%}"
            f"  halves {live['h1']['Sharpe']:.4f}/{live['h2']['Sharpe']:.4f}"
            f"  OOS {live['oos']['CAGR']:7.2%} / {live['oos']['Sharpe']:.4f} / {live['oos']['MaxDD']:7.2%}")
        say(f"   4b bars here: MaxDD >= {DD_CAP*spy['full']['MaxDD']:7.2%}, CAGR >= {CAGR_FLOOR*spy['full']['CAGR']:7.2%},"
            f" Sharpe > {spy['h1']['Sharpe']:.4f}/{spy['h2']['Sharpe']:.4f} (halves), {spy['oos']['Sharpe']:.4f} (OOS)")
        say("")

        cells = {}
        for subset in SUBSETS:
            for comb in COMBS:
                pan = Panel(name, px, inv, ranks, subset, comb)
                r, ann_turn = run(pan, build(pan))
                w = windows(idx, r[WARMUP:])
                a, b = legs_4a(w, live), legs_4b(w, spy)
                key = (subset, comb)
                cells[key] = dict(w=w, r=r[WARMUP:])
                rows.append(dict(panel=name, subset="+".join(subset), nlegs=len(subset), comb=comb,
                                 ann_turnover=ann_turn, **flat(w),
                                 **{f"a_{x}": v for x, v in a.items()},
                                 **{f"b_{x}": v for x, v in b.items()},
                                 pass4a=all(a.values()), pass4b=all(b.values())))
                say(f"   {'+'.join(subset):16s} {comb:4s}  IS {w['is_']['Sharpe']:.4f}  "
                    f"full {w['full']['CAGR']:7.2%} / {w['full']['Sharpe']:.4f} / {w['full']['MaxDD']:7.2%}  "
                    f"halves {w['h1']['Sharpe']:.4f}/{w['h2']['Sharpe']:.4f}  "
                    f"OOS {w['oos']['CAGR']:7.2%} / {w['oos']['Sharpe']:.4f} / {w['oos']['MaxDD']:7.2%}  "
                    f"turn {ann_turn:4.2f}  4a={all(a.values())} 4b={all(b.values())}"
                    + ("  failing 4b: " + ",".join(x for x, v in b.items() if not v) if not all(b.values()) else ""))

        # ---- gates ----
        if name == "U56":
            aw = cells[ANCHOR_CELL]["w"]["full"]
            dev = max(abs(aw["CAGR"] - COMMITTED["CAGR"]), abs(aw["Sharpe"] - COMMITTED["Sharpe"]),
                      abs(aw["MaxDD"] - COMMITTED["MaxDD"]))
            gate("G1_ANCHOR", f"{dev:.2e}", "< 5e-3 vs committed 15.71%/1.1480/-19.13%", dev < 5e-3)
        sing = max(abs(cells[((nm,), "MEAN")]["w"]["full"]["Sharpe"] - cells[((nm,), "MIN")]["w"]["full"]["Sharpe"])
                   for nm in LEGNAMES)
        gate(f"G2_SINGLETON_{name}", f"{sing:.2e}", "== 0 (MEAN and MIN coincide on 1 leg)", sing == 0.0)

        # ---- rule 8: choose the cell on IS Sharpe only, read OOS once ----
        pick = max(cells, key=lambda k: (cells[k]["w"]["is_"]["Sharpe"], str(k)))
        anch = cells[ANCHOR_CELL]
        sel = cells[pick]
        r8_rows.append(dict(panel=name, chooser="CH_IS_SHARPE",
                            pick_subset="+".join(pick[0]), pick_comb=pick[1],
                            pick_is=sel["w"]["is_"]["Sharpe"], pick_oos=sel["w"]["oos"]["Sharpe"],
                            pick_oos_cagr=sel["w"]["oos"]["CAGR"], pick_oos_dd=sel["w"]["oos"]["MaxDD"],
                            anchor_oos=anch["w"]["oos"]["Sharpe"],
                            anchor_oos_cagr=anch["w"]["oos"]["CAGR"], anchor_oos_dd=anch["w"]["oos"]["MaxDD"],
                            spy_oos=spy["oos"]["Sharpe"], live_oos=live["oos"]["Sharpe"],
                            delta_vs_anchor=sel["w"]["oos"]["Sharpe"] - anch["w"]["oos"]["Sharpe"],
                            reached_anchor=(pick == ANCHOR_CELL)))
        best_oos = max(cells, key=lambda k: cells[k]["w"]["oos"]["Sharpe"])
        r8_rows.append(dict(panel=name, chooser="ORACLE_OOS(reference,not a rule)",
                            pick_subset="+".join(best_oos[0]), pick_comb=best_oos[1],
                            pick_is=cells[best_oos]["w"]["is_"]["Sharpe"],
                            pick_oos=cells[best_oos]["w"]["oos"]["Sharpe"],
                            pick_oos_cagr=cells[best_oos]["w"]["oos"]["CAGR"],
                            pick_oos_dd=cells[best_oos]["w"]["oos"]["MaxDD"],
                            anchor_oos=anch["w"]["oos"]["Sharpe"],
                            anchor_oos_cagr=anch["w"]["oos"]["CAGR"], anchor_oos_dd=anch["w"]["oos"]["MaxDD"],
                            spy_oos=spy["oos"]["Sharpe"], live_oos=live["oos"]["Sharpe"],
                            delta_vs_anchor=cells[best_oos]["w"]["oos"]["Sharpe"] - anch["w"]["oos"]["Sharpe"],
                            reached_anchor=(best_oos == ANCHOR_CELL)))
        oos_sp = [cells[k]["w"]["oos"]["Sharpe"] for k in cells]
        say(f"\n   RULE 8 on {name}: IS argmax = {'+'.join(pick[0])}/{pick[1]} (IS {sel['w']['is_']['Sharpe']:.4f})"
            f" -> OOS {sel['w']['oos']['Sharpe']:.4f}; DO-NOTHING anchor OOS {anch['w']['oos']['Sharpe']:.4f}"
            f"; delta {sel['w']['oos']['Sharpe']-anch['w']['oos']['Sharpe']:+.4f}")
        say(f"   OOS Sharpe spread over all {len(cells)} cells on {name}: "
            f"{max(oos_sp)-min(oos_sp):.4f}  (min {min(oos_sp):.4f}, max {max(oos_sp):.4f})")

    df = pd.DataFrame(rows)
    dfc = pd.DataFrame(corr_rows)
    df8 = pd.DataFrame(r8_rows)
    stem = OUT / f"{DATE}_{SLUG}_C"
    df.to_csv(f"{stem}.grid.csv", index=False)
    dfc.to_csv(f"{stem}.legcorr.csv", index=False)
    df8.to_csv(f"{stem}.walkforward.csv", index=False)

    say("\n# ============================ VERDICT ============================")
    say(f"# grid points published: {len(df)} ({len(SUBSETS)} subsets x {len(COMBS)} rules x {len(panels)} panels)")
    say(f"# 4a passes: {int(df.pass4a.sum())} of {len(df)}")
    say(f"# 4b passes: {int(df.pass4b.sum())} of {len(df)}")
    for p in df.panel.unique():
        d = df[df.panel == p]
        say(f"#   {p:9s} 4a {int(d.pass4a.sum()):2d}/{len(d)}  4b {int(d.pass4b.sum()):2d}/{len(d)}"
            f"  OOS Sharpe [{d.oos_Sharpe.min():.4f}, {d.oos_Sharpe.max():.4f}]"
            f"  spread {d.oos_Sharpe.max()-d.oos_Sharpe.min():.4f}")
    say("# rule-8 (IS argmax, OOS read once):")
    for _, r in df8[df8.chooser == "CH_IS_SHARPE"].iterrows():
        say(f"#   {r.panel:9s} picks {r.pick_subset}/{r.pick_comb}  OOS {r.pick_oos:.4f}"
            f"  vs do-nothing {r.anchor_oos:.4f} ({r.delta_vs_anchor:+.4f})"
            f"  vs SPY {r.spy_oos:.4f}  vs LIVE {r.live_oos:.4f}  reached_anchor={r.reached_anchor}")

    # pre-declared outcome scoring, scored as they fall
    u = df[df.panel == "U56"]
    rho_min = dfc.mean_xs_spearman.min()
    A = (rho_min >= 0.70) and ((u.oos_Sharpe.max() - u.oos_Sharpe.min()) < 0.10)
    anchor_pass4b = bool(u[(u.subset == "M12_1+M6+M3") & (u.comb == "MEAN")].pass4b.iloc[0])
    some_subset_fails = bool((~u.pass4b).any())
    anchor_oos_u = float(u[(u.subset == "M12_1+M6+M3") & (u.comb == "MEAN")].oos_Sharpe.iloc[0])
    B = anchor_pass4b and some_subset_fails and (u.oos_Sharpe.max() - anchor_oos_u) <= 0.02
    ch = df8[(df8.chooser == "CH_IS_SHARPE")]
    C = bool(((ch.pick_subset.str.count(r"\+") == 0) & (ch.delta_vs_anchor > 0)).any())
    D = bool((ch.delta_vs_anchor < 0).any())
    say(f"# PRE-DECLARED OUTCOMES (scored as they fell): (A) DEGENERATE={A}  (B) BLEND-CARRIED={B}"
        f"  (C) SINGLE-LEG-SIMPLIFICATION={C}  (D) CHOOSER-LOSES-TO-DOING-NOTHING={D}")
    say(f"# min pairwise leg rank-corr over all panels: {rho_min:+.4f}")

    pd.DataFrame(GATES).to_csv(f"{stem}.gates.csv", index=False)
    say(f"# gates: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass")
    say(f"# artefacts: {stem.name}.grid.csv / .legcorr.csv / .walkforward.csv / .gates.csv")
    say(f"# elapsed {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
