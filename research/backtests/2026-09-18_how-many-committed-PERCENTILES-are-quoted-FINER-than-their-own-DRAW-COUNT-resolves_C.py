#!/usr/bin/env python3
"""
Idea 1200 (lane C, 2026-09-18) — how many committed PERCENTILES are quoted FINER than their
own DRAW COUNT resolves, and how many of the extra digits are LOAD-BEARING?

THE PREMISE, READ FROM THE RECORD.  Idea 1197 found 22 of 103 C_STRICT claims write more
decimal places than 100/(K+1) pp, and 49 of 85 adjudicated ones state no K at all, so their
resolution is unknowable from the text.  1197 stopped at COUNTING the over-quoted figures.
The queue's question is the next one and it is harder: an extra digit is only a defect if it
is LOAD-BEARING — if dropping it would change the claim the unit makes.  This run answers it
twice, once over the committed text and once in money.

WHAT IS BEING MEASURED, STATED BEFORE ANY NUMBER IS READ.

  ARM A (CENSUS).  For every committed percentile figure with an inferable draw count K:
      step(K)   = the resolvable percentile step under the RESOLUTION RULE dial
      d_res     = -floor(log10(step))          decimals the draw count actually resolves
      EXTRA(u)  = max(0, d_quoted - d_res)     decimal places quoted beyond that
      LOAD-BEARING: the unit also states a BAR the figure is compared against, and rounding
      the figure to d_res decimals moves it ACROSS that bar.  A unit with no bar is
      NOT-ADJUDICABLE and is counted separately, never as a pass.

  ARM C (CAPITAL).  The same question asked of a real percentile-keyed DECISION.  Over a grid
  of K real books, PCT(q) picks the cell at the q-th percentile of the in-sample joint 4b
  margin.  The naive reading of 1197's rule says quoting q finer than 100/(K+1) pp cannot
  move the pick.  That reading is TESTED, not assumed: the q axis is walked at 0.001 pp, every
  pick boundary is located, and for each decimal place d the share of d-decimal quote bins
  that STRADDLE a boundary is reported.  A straddled bin is a q whose last quoted digit
  chooses a different book.

  ARM D (THE PRICE OF A DIGIT).  A digit that changes the book is only load-bearing IN MONEY
  if the two books differ.  At every boundary, the OOS Sharpe / CAGR / MaxDD difference and
  the 4b VERDICT difference between the book below and the book above are published.

  PRE-DECLARED OUTCOMES, neither selected on.
    (A) DIGITS ARE DECORATIVE — the post-resolution straddle share is ~0 in ARM C, or the
        boundary crossings carry no 4b verdict change and a negligible OOS Sharpe spread.
    (B) DIGITS ARE LOAD-BEARING — straddle share stays materially above zero past d_res AND
        boundaries carry 4b verdict changes or a material OOS Sharpe spread.
    (C) MIXED — load-bearing syntactically (bins straddle) but not economically (no verdict
        moves), which is the honest report if the two readings disagree.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  CLAIM SET       {C_STRICT, C_WIDE}     C_STRICT: the unit contains percentile/quantile/pctile
                                         AND a decimal figure adjacent to it.  C_WIDE adds
                                         named-percentile tokens (p95 / q05 / P_90 style).
  RESOLUTION RULE {R_ORDER, R_BINOM}     R_ORDER: step = 100/(K+1) pp, 1197's own rule (the
                                         gap between adjacent order statistics).
                                         R_BINOM: step = 196*sqrt(q(1-q)/K) pp, the 95% width
                                         of the percentile's own sampling distribution.

  4 census cells, ALL published.  ARM C's q axis, the digit ladder d, the panel and the grid
  are NOT dials: every value is reported.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); N {5,10,15,20,25,30};
GROSS {0.30..0.80 step 0.05}; d {0,1,2,3,4}; both KEEP paths at all 198 cells.

Frozen at the incumbent's construction (2026-09-04 KEEP 4b, top-N equal weight, no vol
scaler): 3-leg composite (21/252, 0/126, 0/63), above-200d + vol20 < 0.60 eligibility,
H = 126 min-hold, weekly cadence, decide-at-t / apply-at-t+1 (rule 2), 10 bps, 260-row
warm-up.  The rule-8 chooser is idea 1294's, INHERITED not re-tuned.

PROTOCOL: rule 2 execution; rule 8 walk-forward — every percentile is read on
warm-up..2016-12-31 ONLY and 2017-2026 is read ONCE; BOTH KEEP paths (4a vs live RULES v2,
4b vs SPY) at every cell; rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py,
bot.py and baseline.py are NOT modified by this script.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-18_how-many-committed-PERCENTILES-are-quoted-FINER-than-their-own-DRAW-COUNT-resolves_C.py
"""
from __future__ import annotations

import math
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

DATE = "2026-09-18"
SLUG = "how-many-committed-PERCENTILES-are-quoted-FINER-than-their-own-DRAW-COUNT-resolves"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP, MAXVOL = 260, 0.60
COST = 10.0
H_HOLD, FREQ = 126, "W"
NS = [5, 10, 15, 20, 25, 30]
GROSSES = [round(0.30 + 0.05 * i, 2) for i in range(11)]        # 0.30 .. 0.80
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]
DIGITS = [0, 1, 2, 3, 4]
QSTEP = 0.001                                                   # pp; the fine q ladder
LIVE_MAXDD_COMMITTED = -0.1205
# Committed anchors replayed by the gates (idea 1215 / 1293 / 1294, all on this construction).
ANCHOR_1294 = dict(panel="U56", N=15, g=0.60, CAGR=0.1366, Sharpe=1.1706, MaxDD=-0.1638)
ANCHOR_1293 = dict(panel="U56", N=20, g=0.65, CAGR=0.1366, Sharpe=1.1526, MaxDD=-0.1673)

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=value, target=target, pass_=bool(ok)))
    return bool(ok)


# ============================================================ panels / runner (the record's)
def mech(q):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = (q > q.rolling(200).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    sc = (comp * (0.5 + 0.5 * above.astype(float))).values
    return sc, above, np.nan_to_num(vol20, nan=1e9)


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        m = rebalance_mask(px.index, FREQ).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        self.idx = px.index
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.i_oos = int(np.searchsorted(px.index.values,
                                         np.datetime64(pd.Timestamp(OOS_START))))


def build1(pan, N, H):
    """The incumbent's min-hold selection frame at GROSS = 1.0; row t is the APPLICATION-time
    weight (rule 2: decided at t-1, applied at t)."""
    reb = pan.reb
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    for i, t in enumerate(reb):
        ts = max(t - 1, 0)
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


def nrun(pan, Wt):
    """Gross daily returns and one-way turnover.  Costs applied afterwards as an exact affine
    shift, r(c) = gross - turnover * c / 1e4 (gate G1)."""
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    reb = np.asarray(pan.reb, dtype=np.int64)
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
        w0 = Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return (held * rets).sum(axis=1), turn


def at_cost(gr, tu, c=COST):
    return gr - tu * c / 1e4


def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min()) if len(e) else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    e = np.cumprod(1 + r)
    return float(e[-1] ** (252 / len(r)) - 1)


def triple(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def pack(r):
    h1, h2 = halves(r)
    m = triple(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def jmargin(m, bm):
    """The record's joint 4b margin in pp: min(DD cushion, CAGR cushion)."""
    dd = (m["MaxDD"] - DD_CAP * bm["MaxDD"]) * 100.0
    cg = (m["CAGR"] - CAGR_FLOOR * bm["CAGR"]) * 100.0
    return float(min(dd, cg)), float(dd), float(cg)


# ==================================================================== ARM A/B: the census
KEY_STRICT = re.compile(r"percentile|pctile|quantile", re.I)
NAMED_PCT = re.compile(r"\b[pPqQ]_?(\d{1,2}(?:\.\d+)?)\b")
NUM = re.compile(r"(?<![\w.])(\d{1,3}(?:\.\d+)?)\s*(?:pp|%)?")
DRAW = re.compile(
    r"(?:\b[KBN]\s*=\s*(\d[\d,]*)\b)"
    r"|(\d[\d,]*)\s*(?:draws?|replications?|resamples?|seeds?|bootstraps?|permutations?|"
    r"samples?|iterations?|cells?|books?|corpora|folds?)",
    re.I)
BAR = re.compile(
    r"(?:>=|<=|>|<|≥|≤|above|below|under|over|at least|at most|bar(?: of)?|cap(?: of)?|"
    r"floor(?: of)?|threshold(?: of)?|against)\s*(?:a\s+)?(?:bar\s+of\s+)?"
    r"(\d{1,3}(?:\.\d+)?)\s*(?:pp|%)?", re.I)


def units():
    """Every committed text unit under research/: LEADERBOARD rows, CHANGELOG paragraphs and
    every paragraph of every committed .md.  Mechanical; nothing is hand-picked."""
    out = []
    lb = (ROOT / "research" / "LEADERBOARD.md")
    for i, ln in enumerate(lb.read_text(errors="ignore").split("\n")):
        if ln.strip().startswith("|"):
            out.append(("LEADERBOARD.md", i, ln))
    for f in sorted((ROOT / "research").rglob("*.md")):
        if f.name == "LEADERBOARD.md":
            continue
        txt = f.read_text(errors="ignore")
        for i, para in enumerate(re.split(r"\n\s*\n", txt)):
            if para.strip():
                out.append((str(f.relative_to(ROOT)), i, para))
    return out


def decimals(tok: str) -> int:
    return len(tok.split(".")[1]) if "." in tok else 0


def nearest_number(unit, kpos):
    """The decimal figure closest to the percentile keyword — the quoted percentile."""
    best = None
    for m in NUM.finditer(unit):
        tok = m.group(1)
        try:
            v = float(tok)
        except ValueError:
            continue
        if not (0.0 <= v <= 100.0):
            continue
        d = abs(m.start() - kpos)
        if best is None or d < best[0]:
            best = (d, tok, v)
    return (best[1], best[2]) if best else (None, None)


def draw_count(unit):
    vals = []
    for m in DRAW.finditer(unit):
        tok = m.group(1) or m.group(2)
        try:
            k = int(tok.replace(",", ""))
        except ValueError:
            continue
        if 2 <= k <= 10_000_000:
            vals.append(k)
    return max(vals) if vals else None


def step_pp(rule, K, q):
    if rule == "R_ORDER":
        return 100.0 / (K + 1)
    p = min(max(q / 100.0, 1e-6), 1 - 1e-6)
    return 196.0 * math.sqrt(p * (1 - p) / K)


def census():
    rows = []
    for src, i, u in units():
        ks = KEY_STRICT.search(u)
        nm = NAMED_PCT.search(u) if ks is None else None
        if ks is None and nm is None:
            continue
        cset = "C_STRICT" if ks is not None else "C_WIDE_ONLY"
        kpos = (ks or nm).start()
        tok, q = nearest_number(u, kpos)
        if tok is None:
            continue
        K = draw_count(u)
        bars = [float(m.group(1)) for m in BAR.finditer(u)]
        bars = [b for b in bars if 0.0 <= b <= 100.0 and abs(b - q) > 0]
        rows.append(dict(src=src, unit=i, cset=cset, token=tok, q=q,
                         d_quoted=decimals(tok), K=K if K else np.nan,
                         n_bars=len(bars), bar=bars[0] if bars else np.nan))
    return pd.DataFrame(rows)


def adjudicate(df, cset, rule):
    """One census cell.  Returns (per-row frame, summary dict)."""
    sub = df if cset == "C_WIDE" else df[df.cset == "C_STRICT"]
    sub = sub.copy()
    has_k = sub.K.notna()
    st = np.array([step_pp(rule, int(k), q) if np.isfinite(k) else np.nan
                   for k, q in zip(sub.K.values, sub.q.values)])
    sub["step_pp"] = st
    dres = np.where(np.isfinite(st), -np.floor(np.log10(np.where(st > 0, st, 1e-9))), np.nan)
    sub["d_res"] = dres
    sub["extra"] = np.where(np.isfinite(dres),
                            np.maximum(0.0, sub.d_quoted.values - dres), np.nan)
    # LOAD-BEARING: round the figure to the resolvable precision; does it cross the bar?
    lb = []
    for q, d, b in zip(sub.q.values, sub.d_res.values, sub.bar.values):
        if not np.isfinite(d) or not np.isfinite(b):
            lb.append(np.nan); continue
        dd = int(max(0, min(6, d)))
        qr = round(q, dd)
        lb.append(float((q >= b) != (qr >= b)))
    sub["load_bearing"] = lb
    n = len(sub)
    nk = int(has_k.sum())
    over = sub.extra.fillna(0) > 0
    adj = sub.load_bearing.notna()
    return sub, dict(cset=cset, rule=rule, n_units=n, n_with_K=nk,
                     n_no_K=n - nk, n_over=int(over.sum()),
                     share_over=float(over.sum() / nk) if nk else np.nan,
                     n_adjudicable=int(adj.sum()),
                     n_load_bearing=int(sub.load_bearing.fillna(0).sum()),
                     share_load_bearing=float(sub.load_bearing[adj].mean()) if adj.any() else np.nan,
                     median_extra=float(sub.extra[has_k].median()) if nk else np.nan,
                     max_extra=float(sub.extra[has_k].max()) if nk else np.nan)


# ==================================================================== ARM C: the q ladder
def pct_pick(order, q):
    """Nearest-rank percentile on an ASCENDING order of cells: index ceil(q/100*K), clipped.
    Frozen convention, stated before use; ties already broken inside `order`."""
    K = len(order)
    i = int(math.ceil(q / 100.0 * K))
    return order[min(max(i, 1), K) - 1]


def main():
    t0 = time.time()
    say(f"# Idea 1200 (lane C, {DATE}) — committed PERCENTILES vs their own DRAW COUNT")
    say("")

    # ---------------------------------------------------------------- world
    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and mv[c] < 1.0]
    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names; B136 {len(pxB.columns)-1}; "
        f"SMALL {len(inv)} investable of {len(pxS.columns)-1}.")
    say(f"  TAPE: U56 {pxU.index[0].date()}..{pxU.index[-1].date()}; "
        f"B136 ..{pxB.index[-1].date()}; SMALL ..{pxS.index[-1].date()}.")
    say(f"  IS = warm-up..{IS_END}; OOS = {OOS_START}.. (READ ONCE).")
    say("")

    # ---------------------------------------------------------------- 198 real books
    grid = []
    curves = {}
    bench = {}
    for pan in panels:
        n_is = int(np.searchsorted(pan.idx.values, np.datetime64(pd.Timestamp(IS_END)))) + 1
        live = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        spy_f, live_f = pan.spy[WARMUP:], live[WARMUP:]
        bm = dict(full=pack(spy_f), oos=pack(pan.spy[pan.i_oos:]),
                  is_=pack(pan.spy[WARMUP:n_is]))
        lv = dict(full=pack(live_f), oos=pack(live[pan.i_oos:]))
        bench[pan.name] = (bm, lv)
        for N in NS:
            W1 = build1(pan, N, H_HOLD)
            for g in GROSSES:
                gr, tu = nrun(pan, g * W1)
                r = at_cost(gr, tu)
                mf, mo, mi = pack(r[WARMUP:]), pack(r[pan.i_oos:]), pack(r[WARMUP:n_is])
                J, dd_m, cg_m = jmargin(mi, bm["is_"])
                k4a = bool(mf["H1"] > lv["full"]["H1"] and mf["H2"] > lv["full"]["H2"]
                           and mf["MaxDD"] >= lv["full"]["MaxDD"])
                k4b = bool(mf["H1"] > bm["full"]["H1"] and mf["H2"] > bm["full"]["H2"]
                           and mo["Sharpe"] > bm["oos"]["Sharpe"]
                           and mf["MaxDD"] >= DD_CAP * bm["full"]["MaxDD"]
                           and mf["CAGR"] >= CAGR_FLOOR * bm["full"]["CAGR"])
                curves[(pan.name, N, g)] = r
                grid.append(dict(panel=pan.name, N=N, gross=g,
                                 CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"],
                                 H1=mf["H1"], H2=mf["H2"],
                                 OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                 OOS_MaxDD=mo["MaxDD"],
                                 IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"],
                                 IS_MaxDD=mi["MaxDD"],
                                 J_IS=J, ddm_IS=dd_m, cgm_IS=cg_m,
                                 ann_turnover=float(tu[WARMUP:].sum() * 252 / len(tu[WARMUP:])),
                                 keep4a=k4a, keep4b=k4b))
        say(f"  built {len(NS)*len(GROSSES)} books on {pan.name}  ({time.time()-t0:.0f}s)")
    G = pd.DataFrame(grid)
    G.to_csv(f"{OUT}.grid.csv", index=False)

    say("")
    say("## ARM B — THE 198-BOOK GRID (the capital arm's world), both KEEP paths at every cell")
    for p in ["U56", "B136", "SMALL"]:
        s = G[G.panel == p]
        bm, lv = bench[p]
        say(f"  {p:6s}  4a {int(s.keep4a.sum()):3d}/{len(s)}   4b {int(s.keep4b.sum()):3d}/{len(s)}"
            f"   Sharpe {s.Sharpe.min():.4f}..{s.Sharpe.max():.4f}"
            f"   J_IS {s.J_IS.min():+.2f}..{s.J_IS.max():+.2f} pp")
        say(f"          SPY  {bm['full']['CAGR']:.2%} / {bm['full']['Sharpe']:.4f} / "
            f"{bm['full']['MaxDD']:.2%}   (OOS {bm['oos']['CAGR']:.2%} / {bm['oos']['Sharpe']:.4f})"
            f"   RULES v2 {lv['full']['CAGR']:.2%} / {lv['full']['Sharpe']:.4f} / {lv['full']['MaxDD']:.2%}")
    say(f"  TOTAL: 4a {int(G.keep4a.sum())} of {len(G)};  4b {int(G.keep4b.sum())} of {len(G)}.")

    # ---------------------------------------------------------------- gates on the anchors
    for tag, A in (("G2 1294 anchor U56 N=15 g=0.60", ANCHOR_1294),
                   ("G3 1293 anchor U56 N=20 g=0.65", ANCHOR_1293)):
        r = G[(G.panel == A["panel"]) & (G.N == A["N"]) & (G.gross == A["g"])].iloc[0]
        d = max(abs(r.CAGR - A["CAGR"]), abs(r.Sharpe - A["Sharpe"]), abs(r.MaxDD - A["MaxDD"]))
        gate(tag, float(d), "<= 5e-3", d <= 5e-3)
        say(f"  {tag}: {r.CAGR:.2%} / {r.Sharpe:.4f} / {r.MaxDD:.2%}  "
            f"(committed {A['CAGR']:.2%} / {A['Sharpe']:.4f} / {A['MaxDD']:.2%}; max abs-d {d:.2e})")
    lvU = bench["U56"][1]["full"]["MaxDD"]
    gate("G4 live RULES v2 U56 MaxDD == committed -12.05%", float(lvU),
         LIVE_MAXDD_COMMITTED, abs(lvU - LIVE_MAXDD_COMMITTED) <= 2e-3)
    # G1: the cost shift is exactly affine (so nothing below is a re-computation artefact).
    pan = panels[0]
    W1 = build1(pan, 20, H_HOLD)
    gr, tu = nrun(pan, 0.65 * W1)
    g1 = float(np.max(np.abs(at_cost(gr, tu, 0.0) - gr)))
    gate("G1 cost 0 bps is the gross series exactly", g1, "0.0", g1 == 0.0)

    # ---------------------------------------------------------------- ARM A: the census
    say("")
    say("## ARM A — THE CENSUS OF COMMITTED PERCENTILES (all 4 dial cells published)")
    df = census()
    df.to_csv(f"{OUT}.census.csv", index=False)
    say(f"  harvested {len(df)} committed percentile figures over "
        f"{df.src.nunique()} committed files "
        f"(C_STRICT {int((df.cset=='C_STRICT').sum())}, named-token only "
        f"{int((df.cset=='C_WIDE_ONLY').sum())}).")
    summ = []
    for cset in ["C_STRICT", "C_WIDE"]:
        for rule in ["R_ORDER", "R_BINOM"]:
            sub, s = adjudicate(df, cset, rule)
            summ.append(s)
            sub.to_csv(f"{OUT}.census_{cset}_{rule}.csv", index=False)
            say(f"  {cset:9s} x {rule:8s}: n={s['n_units']:5d}  with K {s['n_with_K']:5d}  "
                f"no K {s['n_no_K']:5d} ({s['n_no_K']/max(s['n_units'],1):.4f})  "
                f"OVER-QUOTED {s['n_over']:5d} ({s['share_over']:.4f} of those with K)  "
                f"median extra digits {s['median_extra']:.1f} (max {s['max_extra']:.0f})")
            say(f"  {'':9s}   {'':8s}  adjudicable (a bar is stated) {s['n_adjudicable']:5d}  "
                f"LOAD-BEARING {s['n_load_bearing']:5d}  "
                f"share {s['share_load_bearing']:.4f}")
    S = pd.DataFrame(summ)
    S.to_csv(f"{OUT}.census_summary.csv", index=False)

    # ---------------------------------------------------------------- ARM C: the q ladder
    say("")
    say("## ARM C — THE SAME QUESTION ON A REAL DECISION: PCT(q) over K = 66 books/panel")
    say(f"  PCT(q) = nearest-rank q-th percentile of IS joint 4b margin J_IS, ties to lower")
    say(f"  gross then lower N.  q walked 0..100 at {QSTEP} pp.  R_ORDER step = 100/(K+1) = "
        f"{100/(len(NS)*len(GROSSES)+1):.4f} pp, d_res = "
        f"{int(-math.floor(math.log10(100/(len(NS)*len(GROSSES)+1))))}.")
    qs = np.round(np.arange(0.0, 100.0 + QSTEP / 2, QSTEP), 3)
    lad_rows, bnd_rows = [], []
    picks_by_panel = {}
    for p in ["U56", "B136", "SMALL"]:
        s = G[G.panel == p].copy()
        s = s.sort_values(["J_IS", "gross", "N"], ascending=[True, True, True],
                          kind="mergesort")
        order = list(zip(s.N.values, s.gross.values))
        K = len(order)
        picks = [pct_pick(order, q) for q in qs]
        picks_by_panel[p] = (qs, picks, order)
        chg = [i for i in range(1, len(picks)) if picks[i] != picks[i - 1]]
        say(f"  {p:6s}  K={K}  distinct picks over the whole q axis: "
            f"{len(set(picks))}   boundaries: {len(chg)}   "
            f"min gap {min(np.diff([qs[i] for i in chg])) if len(chg) > 1 else float('nan'):.3f} pp")
        for d in DIGITS:
            u = 10.0 ** (-d)
            bins = set()
            for i in chg:
                bins.add(round(math.floor(qs[i] / u), 6))
            nbins = int(round(100.0 / u)) + 1
            lad_rows.append(dict(panel=p, d=d, quote_unit_pp=u, n_bins=nbins,
                                 n_straddled=len(bins),
                                 straddle_share=len(bins) / nbins))
        # ARM D: what the last digit buys, at every boundary
        for i in chg:
            lo, hi = picks[i - 1], picks[i]
            a = G[(G.panel == p) & (G.N == lo[0]) & (G.gross == lo[1])].iloc[0]
            b = G[(G.panel == p) & (G.N == hi[0]) & (G.gross == hi[1])].iloc[0]
            bnd_rows.append(dict(panel=p, q_boundary=qs[i],
                                 below=f"N={lo[0]}/g={lo[1]}", above=f"N={hi[0]}/g={hi[1]}",
                                 d_OOS_Sharpe=b.OOS_Sharpe - a.OOS_Sharpe,
                                 d_OOS_CAGR=b.OOS_CAGR - a.OOS_CAGR,
                                 d_OOS_MaxDD=b.OOS_MaxDD - a.OOS_MaxDD,
                                 keep4b_below=bool(a.keep4b), keep4b_above=bool(b.keep4b),
                                 verdict_flip=bool(a.keep4b) != bool(b.keep4b)))
    LAD = pd.DataFrame(lad_rows)
    BND = pd.DataFrame(bnd_rows)
    LAD.to_csv(f"{OUT}.qladder.csv", index=False)
    BND.to_csv(f"{OUT}.boundaries.csv", index=False)

    say("")
    say("  STRADDLE SHARE — the share of d-decimal quote bins whose LAST DIGIT chooses a")
    say("  different book (a straddled bin is a load-bearing digit, syntactically):")
    say("    panel     d=0      d=1      d=2      d=3      d=4")
    for p in ["U56", "B136", "SMALL"]:
        s = LAD[LAD.panel == p].set_index("d")
        say(f"    {p:6s} " + "  ".join(f"{s.loc[d,'straddle_share']:.5f}" for d in DIGITS))
    dres_cap = int(-math.floor(math.log10(100 / (len(NS) * len(GROSSES) + 1))))
    say(f"  d_res = {dres_cap} for K=66 under R_ORDER; every digit at d > {dres_cap} is an EXTRA digit.")

    say("")
    say("## ARM D — WHAT A LOAD-BEARING DIGIT IS WORTH IN MONEY (every boundary published)")
    for p in ["U56", "B136", "SMALL"]:
        b = BND[BND.panel == p]
        say(f"  {p:6s}  {len(b)} boundaries;  |d OOS Sharpe| mean {b.d_OOS_Sharpe.abs().mean():.4f}  "
            f"median {b.d_OOS_Sharpe.abs().median():.4f}  max {b.d_OOS_Sharpe.abs().max():.4f}")
        say(f"          |d OOS CAGR| mean {b.d_OOS_CAGR.abs().mean():.2%}  "
            f"max {b.d_OOS_CAGR.abs().max():.2%};  4b VERDICT FLIPS "
            f"{int(b.verdict_flip.sum())} of {len(b)} ({b.verdict_flip.mean():.4f})")

    # ---------------------------------------------------------------- rule 8
    say("")
    say(f"## RULE 8 — every percentile read on warm-up..{IS_END} ONLY; {OOS_START}-2026 READ ONCE")
    r8 = []
    for p in ["U56", "B136", "SMALL"]:
        qs_, picks, order = picks_by_panel[p]
        bm, lv = bench[p]
        for q in [50.0, 75.0, 90.0, 95.0, 97.5, 99.0, 100.0]:
            N, g = pct_pick(order, q)
            row = G[(G.panel == p) & (G.N == N) & (G.gross == g)].iloc[0]
            r = curves[(p, N, g)]
            mo = pack(r[panels[[x.name for x in panels].index(p)].i_oos:])
            k4b_oos = bool(row.H1 > bm["full"]["H1"] and row.H2 > bm["full"]["H2"]
                           and mo["Sharpe"] > bm["oos"]["Sharpe"]
                           and row.MaxDD >= DD_CAP * bm["full"]["MaxDD"]
                           and row.CAGR >= CAGR_FLOOR * bm["full"]["CAGR"])
            k4a = bool(row.keep4a)
            r8.append(dict(panel=p, q=q, N=N, gross=g, J_IS=row.J_IS,
                           FULL_CAGR=row.CAGR, FULL_Sharpe=row.Sharpe, FULL_MaxDD=row.MaxDD,
                           H1=row.H1, H2=row.H2,
                           OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                           SPY_OOS_Sharpe=bm["oos"]["Sharpe"], SPY_OOS_CAGR=bm["oos"]["CAGR"],
                           keep4a=k4a, keep4b=k4b_oos))
    R8 = pd.DataFrame(r8)
    R8.to_csv(f"{OUT}.rule8.csv", index=False)
    for p in ["U56", "B136", "SMALL"]:
        bm, lv = bench[p]
        say(f"  {p} — SPY OOS {bm['oos']['CAGR']:.2%} / {bm['oos']['Sharpe']:.4f} / "
            f"{bm['oos']['MaxDD']:.2%};  RULES v2 OOS {lv['oos']['CAGR']:.2%} / "
            f"{lv['oos']['Sharpe']:.4f} / {lv['oos']['MaxDD']:.2%}")
        for _, r in R8[R8.panel == p].iterrows():
            say(f"    q={r.q:5.1f}  N={int(r.N):2d} g={r.gross:.2f}  J_IS {r.J_IS:+6.2f} pp  "
                f"FULL {r.FULL_CAGR:6.2%} / {r.FULL_Sharpe:.4f} / {r.FULL_MaxDD:7.2%}  "
                f"halves {r.H1:.4f}/{r.H2:.4f}  OOS {r.OOS_CAGR:6.2%} / {r.OOS_Sharpe:.4f} / "
                f"{r.OOS_MaxDD:7.2%}  4a {'P' if r.keep4a else '.'}  4b {'PASS' if r.keep4b else 'FAIL'}")
    say(f"  RULE-8 4b: {int(R8.keep4b.sum())} of {len(R8)} (q, panel) points;  "
        f"4a {int(R8.keep4a.sum())} of {len(R8)}.")
    # does the extra digit ever change the rule-8 answer?
    u = 10.0 ** (-(dres_cap + 1))
    flips = 0
    tot = 0
    for p in ["U56", "B136", "SMALL"]:
        qs_, picks, order = picks_by_panel[p]
        for q in np.round(np.arange(0.0, 100.0 + 1e-9, 10 ** (-dres_cap)), 6):
            a = pct_pick(order, q)
            b = pct_pick(order, min(100.0, q + u))
            tot += 1
            flips += int(a != b)
    say(f"  ONE EXTRA DIGIT (q -> q + {u} pp) moves the rule-8 pick at {flips} of {tot} "
        f"quote points ({flips/tot:.4f}).")

    # ---------------------------------------------------------------- gates + verdict
    G5 = bool(len(df) > 0)
    gate("G5 census harvested at least one committed percentile", len(df), "> 0", G5)
    G6 = bool(len(BND) > 0)
    gate("G6 the q axis has at least one pick boundary", len(BND), "> 0", G6)
    G7 = bool(abs(LAD[LAD.d == 0].straddle_share.mean()
                  - 10 * LAD[LAD.d == 1].straddle_share.mean()) < 0.25)
    gate("G7 straddle share falls ~10x per decimal (the mechanical prediction)",
         float(LAD[LAD.d == 0].straddle_share.mean() / max(LAD[LAD.d == 1].straddle_share.mean(), 1e-12)),
         "~10", G7)
    say("")
    say("## GATES")
    for g in GATES:
        say(f"  {'PASS' if g['pass_'] else 'FAIL'}  {g['gate']}: {g['value']} (target {g['target']})")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)

    say("")
    say("## SURVIVORSHIP (rule 9): U56 and B136 are CURRENT constituents of a committed list;")
    say("   SMALL is the current sub-$2B screen.  Every level here is survivorship-inflated;")
    say("   the census and the straddle shares are DIFFERENCES and comparisons within one tape.")
    say(f"\n  wall {time.time()-t0:.0f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG))
    return G, S, LAD, BND, R8


if __name__ == "__main__":
    main()
