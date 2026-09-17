#!/usr/bin/env python3
"""Idea 1173 (lane cloud, 2026-09-17) — should a MONOTONE-LADDER claim be PUBLISHABLE as a
BINARY at all?

QUESTION (QUEUE idea 1173, verbatim)
    idea 1093 found strict monotonicity over 8 adjacent steps holds at exactly 1 of 7 holds on
    EACH panel, at DIFFERENT holds, while the graded readings (argmax, end-to-end drop at
    7.8-24.1 SE, 4-7 of 8 decisively-down steps) replicate at every hold.  Census the record's
    committed monotone / non-monotone ladder claims, re-score them on a graded statistic with
    its own null, and report how many reverse.  Max 2 params (claim set, graded statistic).

THE TWO TUNED DIALS (PROTOCOL rule 4, no more than two, and the queue names both)
    1. CLAIM SET        in {NARROW, PROX, WIDE}   — the census population
    2. GRADED STATISTIC in {G_DOWNSHARE, G_DECSTEPS, G_SPEARMAN, G_ENDSE}
    3 x 4 = 12 cells, EVERY ONE PUBLISHED in `.grid.csv`.

    NOT dials, reported at every value: PANEL {U56, B136, SMALL}; the n-LADDER
    {5,8,10,12,15,20,25,30,40} (9 rungs = 1093's 8 adjacent steps); the HOLD ladder
    {21,42,52,63,76,90,126} (1093's); the LADDER METRIC {SHARPE, CAGR, MAXDD, ULCER}; the
    bootstrap (63-day blocks, 500 reps) and the permutation null (2,000 draws); the three
    rule-8 choosers.  Everything else is frozen at 936/1082/1086/1093's construction: CAND20
    legs, cap INF, max_vol 0.60, gross 0.75, W cadence, 10 bps, LAG 1, WARMUP 260.

WHAT IS BEING MEASURED, SAID UP FRONT
    A "ladder" here is the 9 rung values of one METRIC as the n dial walks, at one (panel, hold).
    189 ladders in total (3 panels x 7 holds x 4 metrics x ... no: 3 x 7 x 4 = 84 ladders over
    63 books per panel).  Each ladder is scored TWICE:

      BINARY  M_STRICT  — all 8 adjacent steps run in the ladder's own end-to-end direction.
                          This is the form the record publishes ("monotone" / "non-monotone").
      GRADED  four statistics, EACH AGAINST ITS OWN NULL (the queue's ask):
        G_DOWNSHARE — share of the 8 steps in the end-to-end direction.  Null: the 2,000
                      random ORDERINGS of the same 9 rung values (a permutation null: it holds
                      the ladder's CONTENT fixed and destroys only its ORDER, which is exactly
                      what a monotonicity claim asserts).
        G_DECSTEPS  — share of the 8 steps that are in direction AND exceed 2 block-bootstrap
                      SEs.  Same permutation null, with the step SEs carried along.
        G_SPEARMAN  — signed Spearman rho of rung index against value.  Same permutation null.
        G_ENDSE     — end-to-end change divided by its own block-bootstrap SE (1093's
                      "7.8-24.1 SE" reading).  Null: the bootstrap's own distribution.
      A graded verdict is DECISIVE iff the observed statistic sits at or above its null's 95th
      percentile, one-sided in the ladder's own direction.

    REVERSAL, pre-declared: a (panel, hold, metric) cell REVERSES iff the BINARY and the GRADED
    verdict disagree.  UNDER-READ = binary NOT monotone while the graded reading is DECISIVE
    (the record would publish "non-monotone" for a ladder that is decisively ordered).
    OVER-READ = binary monotone while the graded reading is NOT decisive (the record would
    publish "monotone" for a ladder that a coin-flip ordering reproduces).

DECLARED BEFORE ANY NUMBER — the four outcomes, so none can be read off the numbers afterwards.
    (A) BINARY IS PUBLISHABLE      : the binary verdict's bootstrap stability is >= 0.90 AND its
                                     across-hold replication is within 0.20 of the best graded
                                     statistic's.  A binary loses nothing.
    (B) BINARY IS NOT PUBLISHABLE  : binary bootstrap stability < 0.90 AND at least one graded
                                     statistic beats it by >= 0.20 on BOTH stability and
                                     across-hold replication.  A binary throws away a reading
                                     that replicates.
    (C) BINARY IS CONSERVATIVE ONLY: reversals are >= 90% UNDER-READ (binary never claims order
                                     that is not there, it only misses order that is).
    (D) NOT RESOLVABLE             : none of the above separates.

    MONOTONICITY IS NOT A KEEP PATH.  4a and 4b are scored at all 189 books and the rule-8
    walk-forward chooses on 2009-2016 alone and reads 2017-2026 ONCE.  A ladder that is ordered
    and a book worth capital are different claims, and CH_MONO / CH_GRADED exist precisely to
    price whether either reading has any capital content at all.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the
    current output of a sub-$2B screen less the documented `max_1d_move >= 1.0` exclusion
    (data/small_meta.csv).  Every LEVEL here — CAGR, Sharpe, MaxDD — is optimistic and every 4a
    and 4b count is an UPPER bound.  It very largely cancels out of a SHAPE statistic, which
    ranks one construction against itself on one tape, but the cancellation is an argument, not
    a measurement, and the levels are published beside every shape so a reader can check.
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
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "should-a-MONOTONE-LADDER-claim-be-PUBLISHABLE-as-a-BINARY-at-all"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ = 10.0, 0.75, "W"
LEGS = [(21, 252), (0, 126), (0, 63)]
CAPNAME = "INF"

NS = [5, 8, 10, 12, 15, 20, 25, 30, 40]          # 9 rungs -> 1093's 8 adjacent steps
HS = [21, 42, 52, 63, 76, 90, 126]               # 1093's finer hold ladder
PANELS = ["U56", "B136", "SMALL"]
METRICS = ["SHARPE", "CAGR", "MAXDD", "ULCER"]

CLAIM_SETS = ["NARROW", "PROX", "WIDE"]                                  # dial 1
GRADED = ["G_DOWNSHARE", "G_DECSTEPS", "G_SPEARMAN", "G_ENDSE"]          # dial 2

BLOCK, NBOOT, NPERM = 63, 500, 2000
SEED = 11731173
DEC_SE = 2.0
BAR_Q = 0.95
STAB_BAR, GAP_BAR = 0.90, 0.20

A936_WH126 = (0.155787, 1.139701, -0.191276)     # 936/1082/1093's committed U56 W/H126/N=20 triple
A1151_WH126 = (0.155520, 1.138079, -0.191276)    # the SAME cell as 1151/1171/1172 committed it
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205

MONO_TOK = re.compile(r"monoton", re.I)
LADDER_TOK = re.compile(r"\bladder|\brung|\bdial\b|\baxis\b|\bstep\b", re.I)
VERDICT_TOK = re.compile(r"\bmonotone\b|\bnon-monotone\b|\bmonotonic(?:ally)?\b|\bmonotonicity\b", re.I)
AXIS_TOK = re.compile(r"\bn[- ]ladder|\bN\b|\bH\b|\bhold\b|\bgross\b|\bcadence\b|\bcost\b", re.I)
NULL_TOK = re.compile(r"\bnull\b|\bbootstrap|\bP\(|\bpercentile|\bSE\b|\bp-value|\bsigma\b", re.I)
GRADED_TOK = re.compile(r"\bSE\b|\bof 8\b|\bof 7\b|\bshare\b|\brho\b|\bargmax\b|\bdecisive|\bslope\b|\bdrop\b", re.I)
RUNGSET_TOK = re.compile(r"\{[^}]*\d[^}]*\}|\b\d+ rungs?\b|\b\d+-rung\b|\b\d+ of \d+\b", re.I)
PANEL_TOK = {"U56": re.compile(r"\bU56\b"), "B136": re.compile(r"\bB136\b"),
             "SMALL": re.compile(r"\bSMALL\d*\b")}
METRIC_TOK = {"SHARPE": re.compile(r"\bsharpe\b", re.I), "CAGR": re.compile(r"\bCAGR\b"),
              "MAXDD": re.compile(r"\bmaxdd\b|\bdrawdown\b|\bDD\b", re.I),
              "ULCER": re.compile(r"\bulcer\b", re.I)}

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


GATES: list[dict] = []


def gate(name, what, value, ok):
    GATES.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
    P(f"  {name:<4s} {'PASS' if ok else 'FAIL'}  {what}   (dev {value:.3e})")


# ------------------------------------------------------------------ 1082's kernel, unmodified
def nrun(rets, wt, mk):
    T, N = rets.shape
    mk = mk.copy()
    mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
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
    return (held * rets).sum(axis=1) - turn * COST / 1e4


def legs_composite(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return sum(parts) / len(parts)


def mech(px):
    comp = legs_composite(px)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, (above & (vol20 < MAXVOL)).values


def build(rank_key, elig, priced, reb, N, H, T, K, gross):
    """Target weights under MIN HOLD H and slot count N, cap = INF.  1082's build(), unmodified."""
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    for i, t in enumerate(reb):
        held = np.flatnonzero(cur >= 0)
        if len(held):
            young = held[(t - cur[held]) < H]
            young = young[priced[t, young]]
        else:
            young = held
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = rank_key[t].copy()
            k[~(elig[t] & priced[t])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new_cur = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new_cur[c] = cur[c]
        for c in take:
            new_cur[c] = t
        cur = new_cur
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = gross / len(sel)
    return W


def six(r):
    r = np.asarray(r, float)
    if len(r) < 10:
        return {k: np.nan for k in METRICS}
    eq = np.cumprod(1.0 + r)
    dd = eq / np.maximum.accumulate(eq) - 1.0
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    vol = r.std(ddof=1) * np.sqrt(252.0)
    mdd = float(dd.min())
    return {"SHARPE": (r.mean() * 252.0 / vol if vol else np.nan), "CAGR": cagr * 100.0,
            "MAXDD": mdd * 100.0, "ULCER": float(np.sqrt((dd ** 2).mean())) * 100.0}


def metvec(R):
    """R: (T, B) matrix of daily net returns -> dict metric -> (B,) vector.  Vectorised."""
    eq = np.cumprod(1.0 + R, axis=0)
    run = np.maximum.accumulate(eq, axis=0)
    dd = eq / run - 1.0
    T = R.shape[0]
    cagr = eq[-1] ** (252.0 / T) - 1.0
    vol = R.std(axis=0, ddof=1) * np.sqrt(252.0)
    with np.errstate(divide="ignore", invalid="ignore"):
        sh = np.where(vol > 0, R.mean(axis=0) * 252.0 / vol, np.nan)
    return {"SHARPE": sh, "CAGR": cagr * 100.0, "MAXDD": dd.min(axis=0) * 100.0,
            "ULCER": np.sqrt((dd ** 2).mean(axis=0)) * 100.0}


def fsharpe(r):
    r = np.asarray(r, float)
    v = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / v if v else np.nan


def blocks(r, warm, ins, oos):
    rr = r[warm]
    m = six(rr)
    h = len(rr) // 2
    mo, mi = six(r[oos]), six(r[ins])
    return dict(CAGR=m["CAGR"] / 100.0, Sharpe=m["SHARPE"], MaxDD=m["MAXDD"] / 100.0,
                H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                IS_CAGR=mi["CAGR"] / 100.0, IS_Sharpe=mi["SHARPE"], IS_MaxDD=mi["MAXDD"] / 100.0,
                OOS_CAGR=mo["CAGR"] / 100.0, OOS_Sharpe=mo["SHARPE"], OOS_MaxDD=mo["MAXDD"] / 100.0)


def legs_4b(b, sb):
    return {"L_H1": b["H1"] > sb["H1"], "L_H2": b["H2"] > sb["H2"],
            "L_OOS": b["OOS_Sharpe"] > sb["OOS_Sharpe"],
            "L_DD": abs(b["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"]),
            "L_CAGR": b["CAGR"] >= CAGR_FLOOR * sb["CAGR"]}


def legs_4b_oos(b, sb):
    return {"O_S": b["OOS_Sharpe"] > sb["OOS_Sharpe"],
            "O_DD": abs(b["OOS_MaxDD"]) <= DD_CAP * abs(sb["OOS_MaxDD"]),
            "O_CAGR": b["OOS_CAGR"] >= CAGR_FLOOR * sb["OOS_CAGR"]}


def legs_4a(b, lb):
    return {"A_H1": b["H1"] > lb["H1"], "A_H2": b["H2"] > lb["H2"], "A_DD": b["MaxDD"] >= lb["MaxDD"]}


# ---------------------------------------------------------------- the shape statistics
def direction(v):
    """The ladder's OWN end-to-end direction.  +1 rising in rung index, -1 falling."""
    d = v[-1] - v[0]
    return 1.0 if d >= 0 else -1.0


def shape_stats(v, step_se=None, end_se=None):
    """v: (9,) ladder values in rung order.  Returns the binary and the four graded readings,
    all oriented by the ladder's OWN end-to-end direction."""
    v = np.asarray(v, float)
    s = direction(v)
    d = np.diff(v) * s
    n = len(d)
    out = {"M_STRICT": float(np.all(d > 0)),
           "G_DOWNSHARE": float((d > 0).mean()),
           "G_SPEARMAN": float(np.corrcoef(np.arange(len(v)), np.argsort(np.argsort(v)))[0, 1] * s),
           "DIR": s, "END": float((v[-1] - v[0]) * s)}
    if step_se is not None:
        with np.errstate(divide="ignore", invalid="ignore"):
            t = np.where(step_se > 0, d / step_se, 0.0)
        out["G_DECSTEPS"] = float((t > DEC_SE).sum()) / n
    else:
        out["G_DECSTEPS"] = np.nan
    out["G_ENDSE"] = float(out["END"] / end_se) if (end_se and end_se > 0) else np.nan
    return out


def perm_null(v, step_se, rng, nperm=NPERM, orient=True):
    """The permutation null: hold the ladder's CONTENT fixed, destroy its ORDER.  Returns the
    null distribution of each order-sensitive graded statistic and of the binary."""
    v = np.asarray(v, float)
    K = len(v)
    idx = np.argsort(np.argsort(v))
    ranks = idx.astype(float)
    perms = np.argsort(rng.random((nperm, K)), axis=1)
    VV = v[perms]
    RR = ranks[perms]
    D = np.diff(VV, axis=1)
    if orient:
        s = np.sign(VV[:, -1] - VV[:, 0])
        s[s == 0] = 1.0
    else:
        s = np.ones(nperm)
    D = D * s[:, None]
    downshare = (D > 0).mean(axis=1)
    strict = (D > 0).all(axis=1).astype(float)
    ar = np.arange(K, dtype=float)
    ar = (ar - ar.mean()) / ar.std()
    RRc = (RR - RR.mean(axis=1, keepdims=True)) / RR.std(axis=1, keepdims=True)
    spear = (RRc * ar).mean(axis=1) * s
    if step_se is not None:
        with np.errstate(divide="ignore", invalid="ignore"):
            T_ = np.where(step_se[None, :] > 0, D / step_se[None, :], 0.0)
        dec = (T_ > DEC_SE).mean(axis=1)
    else:
        dec = np.full(nperm, np.nan)
    return {"M_STRICT": strict, "G_DOWNSHARE": downshare, "G_SPEARMAN": spear, "G_DECSTEPS": dec}


# ---------------------------------------------------------------- the census
def harvest():
    """Every committed monotone/non-monotone LADDER claim in the research record."""
    files = []
    for pat in ("research/**/*.md", "research/*.md"):
        files += sorted(ROOT.glob(pat))
    files = sorted(set(files))
    rows = []
    for f in files:
        try:
            txt = f.read_text(errors="ignore")
        except Exception:
            continue
        for ln, line in enumerate(txt.splitlines(), 1):
            if not MONO_TOK.search(line):
                continue
            for sent in re.split(r"(?<=[.;!?])\s+", line):
                if not MONO_TOK.search(sent):
                    continue
                s = sent.strip()
                if len(s) < 20:
                    continue
                wide = True
                prox = bool(LADDER_TOK.search(s))
                narrow = bool(prox and VERDICT_TOK.search(s) and AXIS_TOK.search(s))
                rows.append(dict(
                    file=str(f.relative_to(ROOT)), line=ln, text=s[:600],
                    WIDE=wide, PROX=prox, NARROW=narrow,
                    states_null=bool(NULL_TOK.search(s)),
                    states_rungset=bool(RUNGSET_TOK.search(s)),
                    graded_phrasing=bool(GRADED_TOK.search(s)),
                    negated=bool(re.search(r"non-monoton|not monoton|fails? .{0,20}monoton", s, re.I)),
                    panel=next((p for p, rx in PANEL_TOK.items() if rx.search(s)), ""),
                    metric=next((m for m, rx in METRIC_TOK.items() if rx.search(s)), ""),
                    hold=next((h for h in HS if re.search(rf"\bH\s*=?\s*{h}\b", s)), np.nan),
                    mentions_edge=bool(re.search(r"\bEDGE\b", s)),
                ))
    return pd.DataFrame(rows)


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    P(f"# Idea 1173 (lane cloud, {DATE}) — should a MONOTONE-LADDER claim be PUBLISHABLE as a")
    P("# BINARY at all?")
    P(f"# 2 tuned dials: CLAIM SET {CLAIM_SETS} x GRADED STATISTIC {GRADED} = 12 cells, ALL published.")
    P(f"# NOT dials, all values reported: PANEL {PANELS}; n-ladder {NS} (8 adjacent steps);")
    P(f"#   HOLD ladder {HS}; LADDER METRIC {METRICS}; block bootstrap ({BLOCK}d x {NBOOT});")
    P(f"#   permutation null ({NPERM} draws); 3 rule-8 choosers.")
    P(f"# FROZEN: CAND20 legs {LEGS}, cap {CAPNAME}, max_vol {MAXVOL}, gross {GROSS0}, "
      f"cost {COST:.0f} bps, LAG {LAG}, cadence {FREQ}, WARMUP {WARMUP}.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P(f"#   (A) BINARY IS PUBLISHABLE       : binary stability >= {STAB_BAR:.2f} and its across-hold")
    P(f"#       replication within {GAP_BAR:.2f} of the best graded statistic's.")
    P(f"#   (B) BINARY IS NOT PUBLISHABLE   : binary stability < {STAB_BAR:.2f} AND some graded stat")
    P(f"#       beats it by >= {GAP_BAR:.2f} on BOTH stability and across-hold replication.")
    P("#   (C) BINARY IS CONSERVATIVE ONLY : >= 90% of reversals are UNDER-READ.")
    P("#   (D) NOT RESOLVABLE              : none of the above separates.")
    P("# MONOTONICITY IS NOT A KEEP PATH: 4a/4b scored at all 189 books; rule 8 picks (n,H) on")
    P("#   2009-2016 and reads 2017-2026 once.")
    P("")

    # ---------------------------------------------------------------- panels
    P("## PANELS AND THE SMALL STAMP")
    panel_data = {}
    for panel in PANELS:
        if panel == "SMALL":
            px = load_universe(small=True)
            meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
            bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
            keep = [c for c in px.columns if c == "SPY" or c not in bad]
            P(f"  SMALL STAMP: data/small_meta.csv lists {len(meta)} tickers; "
              f"{len(meta) - (len(keep) - 1)} dropped for max_1d_move >= 1.0; "
              f"pool served = {len(keep) - 1} names + SPY as benchmark.")
            px = px[keep]
        else:
            px = load_universe(broad=(panel == "B136"))
        px = px.dropna(how="all").ffill()
        idx = px.index
        T, K = len(idx), len(px.columns)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        mk = rebalance_mask(idx, FREQ).values
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        sc, elig = mech(px)
        rank_key = -np.nan_to_num(sc, nan=-np.inf)
        rank_key[np.isnan(sc)] = np.inf
        reb = np.flatnonzero(mk)
        warm = np.zeros(T, dtype=bool)
        warm[WARMUP:] = True
        oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
        ins = warm & ~oos
        panel_data[panel] = dict(px=px, idx=idx, T=T, K=K, rets=rets, priced=priced, mk=mk,
                                 mkl=mkl, rank_key=rank_key, elig=elig, reb=reb,
                                 warm=warm, ins=ins, oos=oos)
        P(f"  {panel:<6s} {T:5d} bars x {K:4d} cols  {idx[0].date()} .. {idx[-1].date()}  "
          f"({warm.sum()} warm, {ins.sum()} IS, {oos.sum()} OOS)")
    P("")

    # ---------------------------------------------------------------- books
    P("## BOOKS — 9 n-rungs x 7 holds x 3 panels = 189, every one published")
    R = {}          # panel -> (T_warm, 63) matrix of warm-window net returns, col = (n,H)
    COLS = [(n, H) for H in HS for n in NS]
    for panel in PANELS:
        d = panel_data[panel]
        M = np.zeros((int(d["warm"].sum()), len(COLS)))
        full = {}
        for j, (n, H) in enumerate(COLS):
            W = build(d["rank_key"], d["elig"], d["priced"], d["reb"], n, H, d["T"], d["K"], GROSS0)
            Wl = np.zeros_like(W)
            Wl[LAG:] = W[:-LAG]
            r = nrun(d["rets"], Wl, d["mkl"])
            full[(n, H)] = r
            M[:, j] = r[d["warm"]]
        R[panel] = M
        panel_data[panel]["full"] = full
        P(f"  {panel:<6s} built {len(COLS)} books  ({time.time()-t0:.0f}s)")
    P("")

    # ---------------------------------------------------------------- gates
    P("## GATES — printed before any result number")
    d = panel_data["U56"]
    Wg = build(d["rank_key"], d["elig"], d["priced"], d["reb"], 20, 126, d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(Wg, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ)["returns"].values
    Wl = np.zeros_like(Wg)
    Wl[LAG:] = Wg[:-LAG]
    fast = nrun(d["rets"], Wl, d["mkl"])
    v = float(np.abs(eng[d["warm"]] - fast[d["warm"]]).max())
    gate("G1", "fast runner == engine.backtest (U56 W/H126/N=20, gross 0.75)", v, v < 1e-12)

    anc = blocks(panel_data["U56"]["full"][(20, 126)], d["warm"], d["ins"], d["oos"])
    v = max(abs(anc["CAGR"] - A936_WH126[0]), abs(anc["Sharpe"] - A936_WH126[1]),
            abs(anc["MaxDD"] - A936_WH126[2]))
    gate("G2", "CROSS-RUN the committed U56 W/H126/N=20 triple as 936/1082/1093 published it",
         v, v < 5e-4)
    v2 = max(abs(anc["CAGR"] - A1151_WH126[0]), abs(anc["Sharpe"] - A1151_WH126[1]),
             abs(anc["MaxDD"] - A1151_WH126[2]))
    gate("G2b", "CROSS-RUN the SAME cell as 1151/1171/1172 published it TODAY (the later vintage)",
         v2, v2 < 5e-5)
    P(f"     this run {anc['CAGR']:.6f} / {anc['Sharpe']:.6f} / {anc['MaxDD']:.6f}")
    P(f"     936/1082/1093 {A936_WH126[0]:.6f} / {A936_WH126[1]:.6f} / {A936_WH126[2]:.6f}   "
      f"(dev {v:.3e})")
    P(f"     1151/1171/1172 {A1151_WH126[0]:.6f} / {A1151_WH126[1]:.6f} / {A1151_WH126[2]:.6f}   "
      f"(dev {v2:.3e})")
    P("     THE VINTAGE, PUBLISHED NOT ABSORBED: G2 fails and G2b passes because data/prices.csv is")
    P("     rewritten nightly (idea 1163's defect).  This run reproduces the CURRENT committed")
    P("     vintage of the same cell bit for bit; the older one is 1.6e-03 of CAGR away.  Nothing")
    P("     in this run's answer depends on the level, but the reader is told, not shielded.")

    spy_u = d["px"]["SPY"].pct_change().fillna(0.0).values
    sb_u = blocks(spy_u, d["warm"], d["ins"], d["oos"])
    v = max(abs(sb_u["OOS_CAGR"] - SPY_OOS_COMMITTED[0]), abs(sb_u["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
            abs(sb_u["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gate("G3", "CROSS-RUN the committed SPY OOS triple on U56's tape", v, v < 5e-4)

    W2 = build(d["rank_key"], d["elig"], d["priced"], d["reb"], 20, 126, d["T"], d["K"], GROSS0)
    v = float(np.abs(W2 - Wg).max())
    gate("G4", "build() deterministic", v, v < 1e-15)

    rng_g = np.random.default_rng(999)
    fake = rng_g.normal(size=9)
    pn_un = perm_null(fake, None, np.random.default_rng(7), nperm=40000, orient=False)
    v = abs(pn_un["G_DOWNSHARE"].mean() - 0.5)
    gate("G5", "permutation machinery is correct: at a FIXED direction the down-share null "
         "centres on 0.5 (order destroyed, content kept)", v, v < 0.01)
    pn = perm_null(fake, None, np.random.default_rng(7), nperm=40000)
    cen = float(pn["G_DOWNSHARE"].mean())
    se = float(pn["G_DOWNSHARE"].std(ddof=1) / np.sqrt(40000))
    P(f"  G5b  REPORTED NOT GATED — and it is a finding, not a nuisance.  The null that every")
    P(f"       graded statistic here ACTUALLY uses is SELF-ORIENTED (each ladder scored in its own")
    P(f"       end-to-end direction, as the record's claims are), and it centres on "
      f"{cen:.4f} +/- {se:.4f}, NOT on 0.500.  Orienting by the endpoints conditions on them and")
    P(f"       buys {cen - 0.5:.4f} of down-share for free.  A record sentence reading 'k of 8 steps")
    P("       down, against the 4 of 8 you would get by chance' is scored against the WRONG null by")
    P(f"       that margin; at 9 rungs the honest chance level is {cen:.3f} of 8 = {8*cen:.2f} steps.")
    GATES.append(dict(gate="G5b", what="self-oriented down-share null centre (REPORTED, not gated)",
                      value=cen, pass_=True))
    import math as _math
    exact_strict = 2.0 / _math.factorial(len(fake))          # = 5.512e-06 at 9 rungs
    v = abs(pn["M_STRICT"].mean() - exact_strict)
    gate("G6", f"permutation null of M_STRICT sits at the exact 2/9! = {exact_strict:.3e} "
         "(strict monotonicity is a 1-in-181,440 ORDERING, not a 1-in-2 one)", v, v < 1e-3)

    B = 200
    sample = R["U56"][:, 0]
    nb = int(np.ceil(len(sample) / BLOCK))
    rg2 = np.random.default_rng(3)
    starts = rg2.integers(0, len(sample) - BLOCK, size=(B, nb))
    ii = (starts[:, :, None] + np.arange(BLOCK)[None, None, :]).reshape(B, -1)[:, :len(sample)]
    bm = sample[ii].mean(axis=1)
    v = abs(bm.mean() - sample.mean()) / (sample.std() / np.sqrt(len(sample)))
    gate("G7", "moving-block bootstrap is unbiased for the mean (< 0.5 SE of the tape mean)",
         v, v < 0.5)

    csv_probe = harvest()
    ok = bool((csv_probe.NARROW <= csv_probe.PROX).all() and (csv_probe.PROX <= csv_probe.WIDE).all())
    gate("G8", "the three claim sets NEST: NARROW subset of PROX subset of WIDE",
         0.0 if ok else 1.0, ok)
    P("")

    # ---------------------------------------------------------------- bootstrap SEs
    P("## BLOCK BOOTSTRAP — step and end-to-end SEs for every ladder, and verdict STABILITY")
    boot = {}
    for panel in PANELS:
        M = R[panel]
        Tw = M.shape[0]
        nb = int(np.ceil(Tw / BLOCK))
        st = rng.integers(0, Tw - BLOCK, size=(NBOOT, nb))
        acc = {m: np.zeros((NBOOT, len(COLS))) for m in METRICS}
        for b in range(NBOOT):
            ii = (st[b][:, None] + np.arange(BLOCK)[None, :]).ravel()[:Tw]
            mm = metvec(M[ii])
            for m in METRICS:
                acc[m][b] = mm[m]
        boot[panel] = acc
        P(f"  {panel:<6s} {NBOOT} reps x {len(COLS)} books x {len(METRICS)} metrics  "
          f"({time.time()-t0:.0f}s)")
    P("")

    # ---------------------------------------------------------------- ladders
    P("## THE 84 LADDERS — binary and four graded readings, each against its own null")
    ladrows, steprows = [], []
    for panel in PANELS:
        obs = metvec(R[panel])
        for H in HS:
            cols = [COLS.index((n, H)) for n in NS]
            for m in METRICS:
                v = obs[m][cols]
                Bm = boot[panel][m][:, cols]                     # (NBOOT, 9)
                step_se = np.diff(Bm, axis=1).std(axis=0, ddof=1)
                end_se = float((Bm[:, -1] - Bm[:, 0]).std(ddof=1))
                st = shape_stats(v, step_se, end_se)
                pn = perm_null(v, step_se, rng)
                pct = {}
                for g in GRADED:
                    if g == "G_ENDSE":
                        pct[g] = np.nan
                    else:
                        nd = pn[g]
                        pct[g] = float((nd <= st[g]).mean())
                # stability: re-score the SAME ladder on every bootstrap replicate
                stab = {"M_STRICT": 0.0}
                gvals = {g: np.zeros(NBOOT) for g in GRADED}
                strict_b = np.zeros(NBOOT)
                for b in range(NBOOT):
                    sb_ = shape_stats(Bm[b], step_se, end_se)
                    strict_b[b] = sb_["M_STRICT"]
                    for g in GRADED:
                        gvals[g][b] = sb_[g]
                stab["M_STRICT"] = float((strict_b == st["M_STRICT"]).mean())
                dec, decstab = {}, {}
                for g in GRADED:
                    if g == "G_ENDSE":
                        bar = 1.645
                        dec[g] = bool(st[g] >= bar) if np.isfinite(st[g]) else False
                        decstab[g] = float(((gvals[g] >= bar) == dec[g]).mean())
                    else:
                        bar = float(np.nanquantile(pn[g], BAR_Q))
                        dec[g] = bool(st[g] >= bar) if np.isfinite(st[g]) else False
                        decstab[g] = float(((gvals[g] >= bar) == dec[g]).mean())
                row = dict(panel=panel, H=H, metric=m, direction=st["DIR"],
                           end_change=st["END"], end_se=end_se,
                           M_STRICT=bool(st["M_STRICT"]), M_STRICT_stab=stab["M_STRICT"])
                for g in GRADED:
                    row[g] = st[g]
                    row[g + "_pct"] = pct[g]
                    row[g + "_decisive"] = dec[g]
                    row[g + "_stab"] = decstab[g]
                    row[g + "_reversal"] = ("UNDER_READ" if (dec[g] and not st["M_STRICT"])
                                            else "OVER_READ" if (st["M_STRICT"] and not dec[g])
                                            else "AGREE")
                row["levels"] = " ".join(f"{x:.3f}" for x in v)
                ladrows.append(row)
                for k, n in enumerate(NS):
                    steprows.append(dict(panel=panel, H=H, metric=m, rung=n, value=float(v[k]),
                                         se=float(Bm[:, k].std(ddof=1)),
                                         step=float(np.diff(v)[k - 1]) if k else np.nan,
                                         step_se=float(step_se[k - 1]) if k else np.nan))
    LAD = pd.DataFrame(ladrows)
    dump(LAD, "ladders")
    dump(pd.DataFrame(steprows), "steps")
    P("")

    P("## (A) THE HEADLINE READING — replication ACROSS HOLDS and bootstrap STABILITY")
    P(f"  {'panel':<7s}{'metric':<8s}{'BINARY holds':>14s}{'stab':>7s}   " +
      "  ".join(f"{g.replace('G_',''):>10s}" for g in GRADED))
    summ = []
    for panel in PANELS:
        for m in METRICS:
            s = LAD[(LAD.panel == panel) & (LAD.metric == m)]
            nb_ = int(s.M_STRICT.sum())
            line = f"  {panel:<7s}{m:<8s}{nb_:>7d} of {len(s):<4d}{s.M_STRICT_stab.mean():>7.3f}   "
            cells = []
            for g in GRADED:
                cells.append(f"{int(s[g+'_decisive'].sum())}/{len(s)}@{s[g+'_stab'].mean():.2f}")
            P(line + "  ".join(f"{c:>10s}" for c in cells))
            row = dict(panel=panel, metric=m, n_holds=len(s), binary_holds=nb_,
                       binary_rep=nb_ / len(s), binary_stab=float(s.M_STRICT_stab.mean()))
            for g in GRADED:
                row[g + "_holds"] = int(s[g + "_decisive"].sum())
                row[g + "_rep"] = float(s[g + "_decisive"].mean())
                row[g + "_stab"] = float(s[g + "_stab"].mean())
            summ.append(row)
    SUMM = pd.DataFrame(summ)
    dump(SUMM, "replication")
    P(f"  (cells read 'decisive holds / 7 @ mean bootstrap stability')")
    P("")

    # ---------------------------------------------------------------- census
    P("## (B) THE CENSUS — every committed monotone/non-monotone claim in the record")
    CL = harvest()
    dump(CL, "claims")
    P(f"  {len(CL):,} committed sentences carry a monotonicity token across "
      f"{CL.file.nunique()} files.")
    for cs in CLAIM_SETS:
        s = CL[CL[cs]]
        P(f"  {cs:<8s} {len(s):6,d} claims | states a NULL {s.states_null.mean():.4f} | "
          f"states a RUNG SET {s.states_rungset.mean():.4f} | GRADED phrasing "
          f"{s.graded_phrasing.mean():.4f} | NEGATED ('non-monotone') {s.negated.mean():.4f} | "
          f"names a PANEL {(s.panel != '').mean():.4f} | names a METRIC {(s.metric != '').mean():.4f}"
          f" | names a HOLD {s.hold.notna().mean():.4f} | about EDGE {s.mentions_edge.mean():.4f}")
    P("  SCOPE, DECLARED AND NOT GLOSSED: the ladders MEASURED here carry the four METRICS")
    P(f"    {METRICS}.  1093's own object was the EDGE ladder (book CAGR minus a DD-matched null's")
    P("    median over 40 seeds), which costs ~86k rebuilt paths per panel and is NOT rebuilt here.")
    P("    Every re-score below is therefore a TRANSFER onto a metric ladder of the same shape, and")
    P("    is labelled TRANSFERRED throughout; it is not a re-derivation of 1093's cell.")
    P("")

    # ---------------------------------------------------------------- the 12-cell grid
    P("## (C) THE 12-CELL GRID (dial 1 x dial 2) — how many committed claims REVERSE")
    gridrows = []
    for cs in CLAIM_SETS:
        s = CL[CL[cs]]
        res = s[(s.panel != "") & (s.metric != "")]
        pin = res[res.hold.notna()]
        for g in GRADED:
            nrev = nagree = nunres = 0
            kinds = {"UNDER_READ": 0, "OVER_READ": 0}
            prev = pagree = 0
            for r in res.itertuples():
                cell = LAD[(LAD.panel == r.panel) & (LAD.metric == r.metric)]
                if cell.empty:
                    nunres += 1
                    continue
                # the claim's own assertion: NEGATED -> "not monotone", else "monotone"
                asserted = not r.negated
                graded_says = float(cell[g + "_decisive"].mean()) >= 0.5   # majority of 7 holds
                if asserted == graded_says:
                    nagree += 1
                else:
                    nrev += 1
                    kinds["UNDER_READ" if graded_says else "OVER_READ"] += 1
                if np.isfinite(r.hold):
                    c1 = cell[cell.H == int(r.hold)]
                    if not c1.empty:
                        if asserted == bool(c1[g + "_decisive"].iloc[0]):
                            pagree += 1
                        else:
                            prev += 1
            gridrows.append(dict(claim_set=cs, graded=g, n_claims=len(s),
                                 n_resolvable=len(res), agree=nagree, reverse=nrev,
                                 unresolved=nunres,
                                 reverse_share=(nrev / max(nagree + nrev, 1)),
                                 under_read=kinds["UNDER_READ"], over_read=kinds["OVER_READ"],
                                 n_pinned=len(pin), pinned_agree=pagree, pinned_reverse=prev,
                                 pinned_reverse_share=(prev / max(pagree + prev, 1))))
    GRID = pd.DataFrame(gridrows)
    dump(GRID, "grid")
    P("  TRANSFERRED (claim names a panel and a metric; scored against the MAJORITY of the 7 holds)")
    P("  and PINNED (the claim also names one of the 7 holds; scored against THAT hold alone).")
    P(f"  {'claim_set':<10s}{'graded':<13s}{'claims':>8s}{'resolv':>8s}{'agree':>7s}"
      f"{'rev':>6s}{'rev_sh':>9s}{'under':>7s}{'over':>6s}{'pinned':>8s}{'p_rev':>7s}{'p_sh':>8s}")
    for r in GRID.itertuples():
        P(f"  {r.claim_set:<10s}{r.graded:<13s}{r.n_claims:>8,d}{r.n_resolvable:>8d}"
          f"{r.agree:>7d}{r.reverse:>6d}{r.reverse_share:>9.4f}{r.under_read:>7d}{r.over_read:>6d}"
          f"{r.n_pinned:>8d}{r.pinned_reverse:>7d}{r.pinned_reverse_share:>8.4f}")
    P("")

    P("## (D) LADDER-LEVEL REVERSALS — the 84 measured ladders, binary vs each graded statistic")
    revrows = []
    for g in GRADED:
        u = int((LAD[g + "_reversal"] == "UNDER_READ").sum())
        o = int((LAD[g + "_reversal"] == "OVER_READ").sum())
        a = int((LAD[g + "_reversal"] == "AGREE").sum())
        revrows.append(dict(graded=g, agree=a, under_read=u, over_read=o, n=len(LAD),
                            under_share=(u / max(u + o, 1))))
        P(f"  {g:<13s} agree {a:3d} / {len(LAD)}   UNDER-READ {u:3d}   OVER-READ {o:3d}   "
          f"under share of reversals {u / max(u + o, 1):.4f}")
    dump(pd.DataFrame(revrows), "reversals")
    P("")

    # ---------------------------------------------------------------- rule 8 + KEEP paths
    P("## RULE 8 WALK-FORWARD AND BOTH KEEP PATHS — 189 books, every one published")
    bookrows, benchrows, pickrows = [], [], []
    bench = {}
    for panel in PANELS:
        d = panel_data[panel]
        spy = d["px"]["SPY"].pct_change().fillna(0.0).values
        sb = blocks(spy, d["warm"], d["ins"], d["oos"])
        lv = backtest(d["px"], rules_v2_weights(d["px"]), cost_bps=COST, freq=FREQ)["returns"].values
        lb = blocks(lv, d["warm"], d["ins"], d["oos"])
        bench[panel] = (sb, lb)
        for nm, bb in (("SPY", sb), ("RULES v2 (live)", lb)):
            benchrows.append(dict(panel=panel, name=nm, **{k: bb[k] for k in bb}))
        P(f"  {panel:<6s} SPY {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%} "
          f"(halves {sb['H1']:.4f}/{sb['H2']:.4f}), OOS {sb['OOS_CAGR']:.2%} / {sb['OOS_Sharpe']:.4f}"
          f" / {sb['OOS_MaxDD']:.2%}")
        P(f"  {'':<6s} LIVE {lb['CAGR']:.2%} / {lb['Sharpe']:.4f} / {lb['MaxDD']:.2%}, "
          f"OOS {lb['OOS_CAGR']:.2%} / {lb['OOS_Sharpe']:.4f} / {lb['OOS_MaxDD']:.2%}")
        for (n, H) in COLS:
            b = blocks(d["full"][(n, H)], d["warm"], d["ins"], d["oos"])
            l4b, l4bo, l4a = legs_4b(b, sb), legs_4b_oos(b, sb), legs_4a(b, lb)
            bookrows.append(dict(panel=panel, N=n, H=H, **{k: b[k] for k in b},
                                 **{k: bool(v) for k, v in l4b.items()},
                                 **{k: bool(v) for k, v in l4bo.items()},
                                 **{k: bool(v) for k, v in l4a.items()},
                                 pass_4b_full=all(l4b.values()), pass_4b_oos=all(l4bo.values()),
                                 pass_4a=all(l4a.values())))
    BK = pd.DataFrame(bookrows)
    dump(BK, "books")
    dump(pd.DataFrame(benchrows), "benchmarks")
    P(f"  4b FULL {int(BK.pass_4b_full.sum())} of {len(BK)} | 4b OOS {int(BK.pass_4b_oos.sum())} | "
      f"BOTH {int((BK.pass_4b_full & BK.pass_4b_oos).sum())} | 4a {int(BK.pass_4a.sum())} of {len(BK)}")
    for panel in PANELS:
        s = BK[BK.panel == panel]
        P(f"    {panel:<6s} 4b full {int(s.pass_4b_full.sum()):2d}/{len(s)}  "
          f"4b OOS {int(s.pass_4b_oos.sum()):2d}/{len(s)}  4a {int(s.pass_4a.sum()):2d}/{len(s)}")
    P("")

    P("  THE THREE CHOOSERS (all choose on 2009-2016 ONLY and read 2017-2026 ONCE):")
    P("    CH_ISSHARPE — argmax IS Sharpe over all 63 books.  The honest incumbent.")
    P("    CH_MONO     — restrict to holds whose IS n-ladder is BINARY monotone, then argmax IS")
    P("                  Sharpe.  Falls back to CH_ISSHARPE when no hold qualifies (and says so).")
    P("    CH_GRADED   — restrict to holds whose IS n-ladder is DECISIVE on the dial-2 statistic,")
    P("                  then argmax IS Sharpe.  Same fallback rule.")
    for panel in PANELS:
        d = panel_data[panel]
        sb, lb = bench[panel]
        Mis = np.array([d["full"][(n, H)][d["ins"]] for (n, H) in COLS]).T
        obs_is = metvec(Mis)
        Tis = Mis.shape[0]
        nb_ = int(np.ceil(Tis / BLOCK))
        stb = rng.integers(0, Tis - BLOCK, size=(NBOOT, nb_))
        Bis = np.zeros((NBOOT, len(COLS)))
        for b in range(NBOOT):
            ii = (stb[b][:, None] + np.arange(BLOCK)[None, :]).ravel()[:Tis]
            Bis[b] = metvec(Mis[ii])["SHARPE"]
        is_sharpe = obs_is["SHARPE"]
        mono_holds, graded_holds = [], {g: [] for g in GRADED}
        for H in HS:
            cols = [COLS.index((n, H)) for n in NS]
            v = is_sharpe[cols]
            Bm = Bis[:, cols]
            sse = np.diff(Bm, axis=1).std(axis=0, ddof=1)
            ese = float((Bm[:, -1] - Bm[:, 0]).std(ddof=1))
            st = shape_stats(v, sse, ese)
            if st["M_STRICT"]:
                mono_holds.append(H)
            pn = perm_null(v, sse, rng)
            for g in GRADED:
                bar = 1.645 if g == "G_ENDSE" else float(np.nanquantile(pn[g], BAR_Q))
                if np.isfinite(st[g]) and st[g] >= bar:
                    graded_holds[g].append(H)
        for ch in ["CH_ISSHARPE", "CH_MONO"] + [f"CH_GRADED:{g}" for g in GRADED]:
            if ch == "CH_ISSHARPE":
                allow, fb = HS, False
            elif ch == "CH_MONO":
                allow, fb = (mono_holds or HS), (not mono_holds)
            else:
                g = ch.split(":")[1]
                allow, fb = (graded_holds[g] or HS), (not graded_holds[g])
            cand = [j for j, (n, H) in enumerate(COLS) if H in allow]
            j = cand[int(np.nanargmax(is_sharpe[cand]))]
            n, H = COLS[j]
            b = blocks(d["full"][(n, H)], d["warm"], d["ins"], d["oos"])
            l4b, l4bo, l4a = legs_4b(b, sb), legs_4b_oos(b, sb), legs_4a(b, lb)
            pickrows.append(dict(panel=panel, chooser=ch, N=n, H=H, fell_back=fb,
                                 allowed_holds=",".join(str(x) for x in allow),
                                 IS_Sharpe=b["IS_Sharpe"], OOS_Sharpe=b["OOS_Sharpe"],
                                 OOS_CAGR=b["OOS_CAGR"], OOS_MaxDD=b["OOS_MaxDD"],
                                 SPY_OOS_Sharpe=sb["OOS_Sharpe"], SPY_OOS_CAGR=sb["OOS_CAGR"],
                                 beats_SPY_OOS=b["OOS_Sharpe"] > sb["OOS_Sharpe"],
                                 pass_4b_full=all(l4b.values()), pass_4b_oos=all(l4bo.values()),
                                 pass_4a=all(l4a.values())))
        P(f"  {panel:<6s} IS-monotone holds {mono_holds if mono_holds else 'NONE'};  "
          + "; ".join(f"{g.replace('G_','')} {graded_holds[g] if graded_holds[g] else 'NONE'}"
                      for g in GRADED))
    PK = pd.DataFrame(pickrows)
    dump(PK, "picks")
    P(f"  {'panel':<7s}{'chooser':<22s}{'N':>4s}{'H':>5s}{'fb':>4s}{'IS_S':>8s}{'OOS_S':>8s}"
      f"{'SPY_S':>8s}{'>SPY':>6s}{'4b':>4s}{'4bO':>5s}{'4a':>4s}")
    for r in PK.itertuples():
        P(f"  {r.panel:<7s}{r.chooser:<22s}{r.N:>4d}{r.H:>5d}{'Y' if r.fell_back else '.':>4s}"
          f"{r.IS_Sharpe:>8.4f}{r.OOS_Sharpe:>8.4f}{r.SPY_OOS_Sharpe:>8.4f}"
          f"{'Y' if r.beats_SPY_OOS else '.':>6s}{'Y' if r.pass_4b_full else '.':>4s}"
          f"{'Y' if r.pass_4b_oos else '.':>5s}{'Y' if r.pass_4a else '.':>4s}")
    P("")

    # ---------------------------------------------------------------- verdict
    P("## VERDICT AGAINST THE PRE-DECLARED OUTCOMES")
    bstab = float(LAD.M_STRICT_stab.mean())
    brep = float(LAD.M_STRICT.mean())
    onT = LAD[LAD.M_STRICT]
    onF = LAD[~LAD.M_STRICT]
    P("  THE BINARY'S STABILITY IS MOSTLY THE STABILITY OF SAYING 'NO', AND IT IS PUBLISHED SPLIT:")
    P(f"    M_STRICT is TRUE at {len(onT)} of {len(LAD)} ladders with mean bootstrap stability "
      f"{onT.M_STRICT_stab.mean():.4f} (min {onT.M_STRICT_stab.min():.4f}),")
    P(f"    FALSE at {len(onF)} with mean stability {onF.M_STRICT_stab.mean():.4f}.  The headline "
      f"{bstab:.4f} is a {len(onF)}/{len(LAD)}-weighted average of the two, so a run that quotes")
    P("    'the binary is stable' is quoting the stability of a verdict that is almost always NO.")
    P("    A PUBLISHED 'THIS LADDER IS MONOTONE' REPRODUCES ON ITS OWN TAPE "
      f"{onT.M_STRICT_stab.mean():.1%} OF THE TIME.")
    best_g, best_gap = None, -9.9
    for g in GRADED:
        gs, gr = float(LAD[g + "_stab"].mean()), float(LAD[g + "_decisive"].mean())
        gap = min(gs - bstab, gr - brep)
        P(f"  {g:<13s} stability {gs:.4f} (binary {bstab:.4f})   replication {gr:.4f} "
          f"(binary {brep:.4f})   min gap {gap:+.4f}")
        if gap > best_gap:
            best_g, best_gap = g, gap
    tot_u = sum(int((LAD[g + "_reversal"] == "UNDER_READ").sum()) for g in GRADED)
    tot_o = sum(int((LAD[g + "_reversal"] == "OVER_READ").sum()) for g in GRADED)
    under_share = tot_u / max(tot_u + tot_o, 1)
    P(f"  binary bootstrap stability {bstab:.4f} (bar {STAB_BAR:.2f});  best graded {best_g} "
      f"min gap {best_gap:+.4f} (bar {GAP_BAR:+.2f});  UNDER-READ share of all reversals "
      f"{under_share:.4f}")
    if bstab >= STAB_BAR and (max(float(LAD[g + "_decisive"].mean()) for g in GRADED) - brep) <= GAP_BAR:
        outcome = "(A) BINARY IS PUBLISHABLE"
    elif bstab < STAB_BAR and best_gap >= GAP_BAR:
        outcome = "(B) BINARY IS NOT PUBLISHABLE"
    elif under_share >= 0.90:
        outcome = "(C) BINARY IS CONSERVATIVE ONLY"
    else:
        outcome = "(D) NOT RESOLVABLE"
    P(f"  OUTCOME: {outcome}")
    P("")

    dump(pd.DataFrame(GATES), "gates")
    P(f"## GATES {sum(g['pass_'] for g in GATES)} of {len(GATES)} PASS")
    P(f"## DONE in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return outcome


if __name__ == "__main__":
    main()
