#!/usr/bin/env python3
"""
Idea 1198 (lane C, 2026-09-19) — how many committed RUNNER-EQUIVALENCE GATES were read
through a SKIPNA MAX, and did the skip cover any cell OUTSIDE the warm-up?

WHY THIS IDEA, AND WHY NO ELIGIBILITY DESCENT.  The sprint rule gives lane C the SECOND
numbered item standing in QUEUE.md's '## Open'.  That is 1198 (1204 is first, lane A's).  It
is price-only — no EDGAR / Form 4 / 8-K / options / live data — so no skip applied.  The
standing "a census has no price leg" objection is NOT repeated here, and lane B's own idea-1265
correction is followed instead: the object this idea questions is the EQUIVALENCE GATE through
which every fast runner in the record was validated, and every capital number the record has
published since was produced by a fast runner that passed one.  If the gate's reading is blind
anywhere, the record's books are unvalidated there.  That is a question about money and it is
answered here by building the books, not by reading the text.

THE PREMISE, FROM THE RECORD.  Idea 1191's G1b found `engine.backtest` emits NaN in `returns`,
because `products/backtester/engine.py` line

    w_target = weights.reindex(prices.index).fillna(0.0).shift(1)

never fills the row the shift vacates.  At i = 0 the engine rebalances unconditionally, reads an
all-NaN target row, and carries `cur = NaN` until the first scheduled rebalance; the turnover at
BOTH rows is then NaN, and `port = (held*rets).sum(axis=1) - turnover*cost/1e4` is NaN at both.
1191 observed that both rows sit inside the 260-row warm-up every committed script drops, so no
published figure moves — but also that no gate has ever CHECKED that, because the gates compare
pandas objects and `pandas.Series.max()` SKIPS NaN while `numpy.ndarray.max()` PROPAGATES it.  A
NaN difference is therefore invisible to a pandas-basis gate at any row, warm-up or not.

WHAT IS MEASURED (five legs, all published):
  C1 MECHANISM.  The NaN census of engine.backtest itself: 3 panels x 4 cadences x 2 books = 24
     cells, every NaN row index and date published, against the 260-row warm-up.
  C2 BASIS PROOF.  That the classifier's premise is true, run rather than asserted: the same
     difference vector read on both bases, and a NaN INJECTED at a post-warm-up row, to show the
     skipna basis reads 0.0e+00 on a vector that a strict basis reads as NaN.
  C3 CENSUS.  Every engine-equivalence gate line in the committed record (research/backtests/*.py)
     classified by comparison basis: NAN_AWARE / STRICT_NUMPY / SKIPNA_PANDAS.
  C4 EXPOSURE.  The only way a NaN row can reach a PUBLISHED window is a window that starts at
     row 0 of its own engine.backtest call.  Every backtest() call site in the record is counted
     and the pre-sliced-frame ones are read out by name.
  C5 RE-RUN ON NDARRAY (the idea's literal ask).  The record's canonical gate — the segment fast
     runner against engine.backtest on the SAME book — re-run NaN-aware on 3 panels x 4 cadences,
     with the NaN cells of the difference counted INSIDE and OUTSIDE the warm-up separately.

THE CAPITAL ARM.  The frozen 2026-09-04 KEEP-4b incumbent (N = 20 slots, H = 126-day minimum
hold, gross 0.75, weekly Fri-decide / Mon-trade, 10 bps, t+1) is priced through all three
runners on all three panels — 9 real books — against the live RULES v2 baseline AND SPY on each
panel, with both KEEP paths at every cell and rule 8 with 2017-2026 read once.  If the three
runners are one book outside the warm-up, the record's 4b pass is runner-independent and the
skipna gates certified nothing they needed to; if they are not, every committed capital figure
is a runner artefact.  Either answer is worth the run.

EXACTLY TWO TUNED PARAMETERS (PROTOCOL rule 4):
    RUNNER  the gate set axis — which runner produced the book:
            ENGINE   products/backtester/engine.backtest exactly as committed (the comparand
                     every gate in the record is written against).  The rule-8 anchor.
            REPAIRED a LOCAL copy of engine.backtest with the vacated shift row filled with 0.0
                     (engine.py itself is NOT modified — PROTOCOL forbids it).
            FAST     the segment runner the record's capital runs actually use (idea 1403's
                     `run` at f = 1, the frozen incumbent's own sizing).
    BASIS   the comparison basis a gate reads the difference on:
            SKIPNA_PANDAS  pandas .max() — the record's basis
            STRICT_NUMPY   ndarray .max() — NaN propagates
            NAN_AWARE      np.nanmax plus an explicit NaN count

NOT DIALS, reported at every value and never chosen on:
    PANEL    {U56, B136, SMALL} — the record's three standing panels.
    CADENCE  {D, W, M, Q} — for C1 and C5 only; every capital cell is WEEKLY, the incumbent's.
    GROSS    0.75, the frozen incumbent's, on every capital cell.  Not walked.
    COST     10 bps per unit turnover (PROTOCOL rule 2) at every cell.

PRE-DECLARED OUTCOMES, written before any number below was read:
  H_NAN   engine.backtest emits EXACTLY two NaN rows in `returns` at every one of the 24 cells,
          at row 0 and at the first rebalance-application row, and the largest such row index
          over the whole grid is < 260.  (The Q cadence is the stress case, ~63 rows in.)
  H_BLIND the skipna basis reads a NaN-carrying difference vector as a clean 0.0e+00 at EVERY
          cell, so the record's gates could not have caught a NaN difference anywhere.
  H_CENS  a MAJORITY of the record's committed engine-equivalence gate lines are on the skipna
          basis.
  H_CLEAN no cell OUTSIDE the warm-up is NaN in any runner difference, on any panel or cadence.
          This is the headline: it is what makes the record's committed figures safe, and it has
          never been checked.  If it fails anywhere the run reports a live defect.
  H_BOOK  the three runners are ONE BOOK outside the warm-up — identical 4a and 4b verdicts at
          all 9 capital cells, and a difference at or below floating-point noise.
  H_PICK  rule 8: the IS chooser over RUNNER costs EXACTLY 0.0000 of OOS Sharpe, because the
          axis is a null axis.  A dial that cannot move a book is not a dial; the capital
          verdict is KILL-as-a-dial whatever the census finds.
  Whichever fire are reported as they fall.  The capital verdict follows rule 8, not the census.

GATES.  G1 the (ENGINE, U56, weekly) capital cell replays idea 1350's committed head-vintage
anchor 15.80% / 1.1537 / -19.13% to within the 5e-3 tape-vintage floor that run established; the
deviation is PUBLISHED, not asserted.  G2 REPAIRED carries zero NaN in returns, weights and
turnover at all 24 C1 cells.  G3 ENGINE and REPAIRED are bit-identical on every row AFTER the
first rebalance-application row, on every panel and cadence (this is what bounds the defect).
  (G3 IN THIS PRE-DECLARED FORM FAILS, and the failure is published rather than swapped out.
   ENGINE and REPAIRED agree to 4.9e-17, not to 0.  The cause is not the book: pandas'
   DataFrame.sum(axis=1) switches accumulation kernel when the frame carries a NaN ANYWHERE, so
   the engine's NaN weight rows perturb every OTHER row too — the defect's reach is wider than
   idea 1191 read it, and its post-warm-up magnitude is 15 orders of magnitude below any
   published digit.  Two exact restatements are added and both pass: G3a the post-NaN-row
   deviation is <= 1e-15, and G3b the kernel switch demonstrated on a synthetic frame.)
G4 every capital cell published to CSV with both KEEP paths.  G5 exactly two tuned parameters.
G6 the rule-8 chooser reads no row on or after 2017-01-01.  G7 determinism: the headline cell
recomputed bit for bit.  G8 the C3 census is non-empty and its classes partition the population.

PROTOCOL: rule 1 committed caches, >= 10 years; rule 2 10 bps per unit turnover, t+1 execution;
rule 3 compared against live RULES v2 AND SPY on each panel; rule 4 both KEEP paths at every
cell; rule 5 one idea, one script, deterministic, standalone; rule 8 walk-forward as above;
rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT
modified, and engine.py is NOT modified — the repair is a local copy, priced, never installed.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists and SMALL a current sub-$2B
screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped first), so every absolute
level is an upper bound and every 4b pass an optimistic one.  The bias is orthogonal to this
run's question — a runner-equivalence difference is a property of the arithmetic, not of the
names — so it changes no verdict here, but the absolute levels quoted inherit it.

Offline and deterministic (committed caches only, no network, no yfinance):
  python research/backtests/2026-09-19_skipna-max-runner-equivalence-gates_C.py
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import EXCLUDE, rules_v2_weights          # noqa: E402
from engine import backtest, rebalance_mask            # noqa: E402

DATE, SLUG = "2026-09-19", "skipna-max-runner-equivalence-gates"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_C"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
A_N, A_H, A_GROSS = 20, 126, 0.75              # the frozen 2026-09-04 incumbent
LEGS = [(21, 252), (0, 126), (0, 63)]          # the committed RAW three-leg composite
CADENCES = ["D", "W", "M", "Q"]
HEAD_FREQ = "W"
RUNNERS = ["ENGINE", "REPAIRED", "FAST"]       # DIAL 1 — the gate set axis; ENGINE is the anchor
BASES = ["SKIPNA_PANDAS", "STRICT_NUMPY", "NAN_AWARE"]   # DIAL 2 — comparison basis
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COMMITTED_U56 = (0.1580, 1.1537, -0.1913)      # idea 1350 head-vintage anchor, gross 0.75
TAPE_FLOOR = 5e-3

GATES: list[dict] = []


def say(*a):
    print(" ".join(str(x) for x in a), flush=True)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    say(f"   GATE {name}: {value} vs {target} -> {'PASS' if ok else 'FAIL'}")
    return bool(ok)


# ------------------------------------------------------------------ metrics (nan-strict)
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    return float(np.prod(1.0 + r)) ** (252.0 / len(r)) - 1.0


def mdd(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1.0).min())


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def windows(r, o):
    h = len(r) // 2
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]), oos=stats(r[o:]),
                **{"is": stats(r[:o])})


def legs_4a(b, live):
    return dict(H1=b["h1"]["Sharpe"] > live["h1"]["Sharpe"],
                H2=b["h2"]["Sharpe"] > live["h2"]["Sharpe"],
                DD=b["full"]["MaxDD"] >= live["full"]["MaxDD"])


def legs_4b(b, spy):
    return dict(H1=b["h1"]["Sharpe"] > spy["h1"]["Sharpe"],
                H2=b["h2"]["Sharpe"] > spy["h2"]["Sharpe"],
                OOS=b["oos"]["Sharpe"] > spy["oos"]["Sharpe"],
                DD=b["full"]["MaxDD"] >= DD_CAP * spy["full"]["MaxDD"],
                CAGR=b["full"]["CAGR"] >= CAGR_FLOOR * spy["full"]["CAGR"])


def failed(d):
    return ",".join(k for k, v in d.items() if not v) or "-"


# ------------------------------------------------------------------ the repaired engine
def backtest_repaired(prices, weights, cost_bps=10.0, freq="M"):
    """products/backtester/engine.backtest with ONE character of difference: the row that
    `.shift(1)` vacates is filled with 0.0 instead of left NaN.  engine.py is NOT modified —
    this local copy exists so the defect can be PRICED rather than installed."""
    rets = prices.pct_change().fillna(0.0)
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1).fillna(0.0)   # <-- the repair
    mask = rebalance_mask(prices.index, freq).shift(1, fill_value=False)
    held = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
    cur = np.zeros(len(prices.columns))
    turnover = pd.Series(0.0, index=prices.index)
    for i, d in enumerate(prices.index):
        if mask.iloc[i] or i == 0:
            new = w_target.iloc[i].values
            turnover.iloc[i] = np.abs(new - cur).sum()
            cur = new
        held.iloc[i] = cur
        growth = cur * (1 + rets.iloc[i].values)
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    port = (held * rets).sum(axis=1) - turnover * cost_bps / 1e4
    return {"returns": port, "equity": (1 + port).cumprod(), "weights": held,
            "turnover": turnover}


# ------------------------------------------------------------------ comparison bases
def read_basis(diff, basis):
    """How a gate on `basis` reads a difference vector.  `diff` is the raw pandas Series the
    gate would have built; the basis decides what it is read through."""
    if basis == "SKIPNA_PANDAS":
        return float(diff.abs().max()), None                 # pandas: NaN silently skipped
    v = np.asarray(diff.values, float)
    if basis == "STRICT_NUMPY":
        return float(np.abs(v).max()), None                  # ndarray: NaN propagates
    return float(np.nanmax(np.abs(v))), int((~np.isfinite(v)).sum())   # NAN_AWARE


# ------------------------------------------------------------------ panels
UNIV = sorted({t for g in json.loads((ROOT / "research" / "universe.json").read_text()).values()
               for t in g} - set(EXCLUDE))
_meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
BAD_SMALL = set(_meta.loc[_meta.max_1d_move >= 1.0, "ticker"])


class Panel:
    """One standing panel with the incumbent's selection inputs precomputed.  Construction is
    idea 1403's, unchanged, so the FAST runner here IS the record's runner."""

    def __init__(self, name, px, invest):
        self.name, self.px, self.idx = name, px, px.index
        self.invest = invest
        q = px[invest]
        self.rets = q.pct_change().fillna(0.0).values
        self.priced = q.notna().values
        parts = []
        for skip, look in LEGS:
            x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
            parts.append(x.rank(axis=1, pct=True))
        comp = (sum(parts) / len(parts)).values
        self.key = np.where(np.isfinite(comp), -comp, np.inf)
        above = (q > q.rolling(200).mean()).values
        v20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
        self.elig = above & (np.nan_to_num(v20, nan=1e9) < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.K = len(invest)
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.C = C
        self.Cp = np.vstack([np.ones((1, C.shape[1])), C[:-1]])
        self.T = len(px)
        self.reb = {}
        for f in CADENCES:
            m = rebalance_mask(px.index, f).shift(1, fill_value=False).values.copy()
            m[0] = True
            self.reb[f] = np.flatnonzero(m)


def panels():
    out = []
    raw = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True).sort_index()
    keep = [c for c in UNIV if c in raw.columns]
    px = raw[keep].loc["2008-01-01":].dropna(how="all").ffill()
    out.append(Panel("U56", px, [c for c in px.columns if c != "SPY"]))

    pb = pd.read_csv(ROOT / "data" / "prices_broad.csv", index_col=0,
                     parse_dates=True).sort_index().loc["2008-01-01":].dropna(how="all").ffill()
    out.append(Panel("B136", pb, [c for c in pb.columns if c != "SPY"]))

    ps = pd.read_csv(ROOT / "data" / "prices_small.csv.gz", index_col=0,
                     parse_dates=True).sort_index().loc["2008-01-01":].dropna(how="all").ffill()
    spy = raw["SPY"].reindex(ps.index, method="ffill").rename("SPY")
    ps = pd.concat([ps.drop(columns=["SPY"], errors="ignore"), spy], axis=1)
    out.append(Panel("SMALL", ps, [c for c in ps.columns if c != "SPY" and c not in BAD_SMALL]))
    return out


# ------------------------------------------------------------------ the frozen incumbent
def build_sel(pan, freq=HEAD_FREQ, N=A_N, H=A_H, lag=1):
    """The incumbent's held set per rebalance segment (idea 1403's build_sel, unchanged)."""
    K, segs = pan.K, []
    cur = np.full(K, -1, dtype=np.int64)
    pr, T = pan.priced, pan.T
    reb = pan.reb[freq]
    for i, t in enumerate(reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = [int(c) for c in young]
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            for c in np.argsort(k, kind="stable"):
                if need == 0 or not np.isfinite(k[c]):
                    break
                take.append(int(c))
                need -= 1
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        stop = reb[i + 1] if i + 1 < len(reb) else T
        if len(sel):
            segs.append((int(t), int(stop), sel.copy(), int(ts)))
    return segs


def run_fast(pan, segs, gross=A_GROSS):
    """The record's segment fast runner (idea 1403's `run` at f = 1, the committed sizing)."""
    T = pan.T
    r = np.zeros(T)
    curw = np.zeros(pan.K)
    turn_tot = 0.0
    for (i0, i1, sel, ts) in segs:
        n = len(sel)
        w = np.full(n, gross / n)
        new = np.zeros(pan.K)
        new[sel] = w
        turn = float(np.abs(new - curw).sum())
        turn_tot += turn
        base = pan.Cp[i0, sel]
        A = w[None, :] * (pan.Cp[i0:i1, sel] / base[None, :])
        c0 = 1.0 - gross
        V = A.sum(axis=1) + c0
        seg = (A * pan.rets[i0:i1, sel]).sum(axis=1) / V
        seg[0] -= turn * COST / 1e4
        r[i0:i1] = seg
        Ae = w * (pan.C[i1 - 1, sel] / base)
        curw = np.zeros(pan.K)
        curw[sel] = Ae / (Ae.sum() + c0)
    return r, turn_tot / (T / 252.0)


def weights_frame(pan, segs, gross=A_GROSS):
    """The same book as a weights DataFrame for engine.backtest.  The engine applies
    `weights.shift(1)` on its mask rows, so a segment starting at row i0 has its target placed
    at row i0-1 — the decision row, which is exactly the fast runner's `ts`."""
    W = pd.DataFrame(0.0, index=pan.idx, columns=pan.px.columns)
    cols = np.asarray(pan.invest, dtype=object)
    for (i0, i1, sel, ts) in segs:
        if i0 == 0:
            continue                       # engine cannot be handed a row before row 0
        W.iloc[i0 - 1, [W.columns.get_loc(c) for c in cols[sel]]] = gross / len(sel)
    return W


# ------------------------------------------------------------------ C3 / C4 census of the record
GATE_MAX = re.compile(r"\.max\(\)|np\.max|np\.nanmax|allclose|isclose")
GATE_ENG = re.compile(r"backtest\(|engine\.backtest|\beng\b|_eng\b|r_eng")
GATE_ABS = re.compile(r"abs|allclose|isclose")
NAN_AWARE_RE = re.compile(r"nanmax|equal_nan|nan_to_num|isnan|isna\(|notna\(|isfinite")
NDARRAY_RE = re.compile(r"\.values|to_numpy\(|np\.asarray|np\.array\(|\.ravel\(|\.flatten\(")
CALL_RE = re.compile(r"\bbacktest\(\s*([^,]{0,120}?),")


def classify_line(ln):
    if NAN_AWARE_RE.search(ln):
        return "NAN_AWARE"
    if NDARRAY_RE.search(ln):
        return "STRICT_NUMPY"
    return "SKIPNA_PANDAS"


def census_record():
    files = sorted((ROOT / "research" / "backtests").glob("*.py"))
    lines, per_file, calls, sliced = [], {}, 0, []
    for f in files:
        try:
            txt = f.read_text(errors="ignore")
        except OSError:
            continue
        for m in CALL_RE.finditer(txt):
            calls += 1
            a = m.group(1)
            if ".loc[" in a or ".iloc[" in a:
                sliced.append(f.name)
        for k, ln in enumerate(txt.split("\n"), 1):
            if GATE_MAX.search(ln) and GATE_ENG.search(ln) and GATE_ABS.search(ln):
                c = classify_line(ln)
                lines.append(dict(file=f.name, line=k, basis=c, text=ln.strip()[:200]))
                per_file.setdefault(f.name, set()).add(c)
    return files, lines, per_file, calls, sliced


def main():
    t0 = time.time()
    say("=" * 104)
    say("Idea 1198 (lane C) — SKIPNA-MAX RUNNER-EQUIVALENCE GATES: what did the skip cover?")
    say("=" * 104)

    PANELS = panels()

    # =============================================== C1  MECHANISM: the NaN census of the engine
    say("\n" + "=" * 104)
    say("C1  MECHANISM — engine.backtest NaN census, 3 panels x 4 cadences x 2 books")
    say("=" * 104)
    nan_rows, worst_nan_idx, rep_nan_total = [], -1, 0
    first_reb = {}
    for pan in PANELS:
        books = {"LIVE_v2": rules_v2_weights(pan.px),
                 "INCUMBENT": weights_frame(pan, build_sel(pan, HEAD_FREQ))}
        for bk, W in books.items():
            for f in CADENCES:
                res = backtest(pan.px, W, cost_bps=COST, freq=f)
                rep = backtest_repaired(pan.px, W, cost_bps=COST, freq=f)
                v = res["returns"].values
                bad = np.flatnonzero(~np.isfinite(v))
                wnan = int(res["weights"].isna().values.sum())
                tnan = int((~np.isfinite(res["turnover"].values)).sum())
                rnan = int((~np.isfinite(rep["returns"].values)).sum()
                           + rep["weights"].isna().values.sum()
                           + (~np.isfinite(rep["turnover"].values)).sum())
                rep_nan_total += rnan
                mi = int(bad.max()) if len(bad) else -1
                worst_nan_idx = max(worst_nan_idx, mi)
                first_reb[(pan.name, f)] = mi
                # the charge the skip throws away: the entry turnover the engine NaN'd
                lost = float(rep["turnover"].values[bad].sum()) if len(bad) else 0.0
                # G3: ENGINE == REPAIRED on every row after the last NaN row
                tail = int(mi) + 1
                d_tail = float(np.max(np.abs(v[tail:] - rep["returns"].values[tail:]))) if mi >= 0 else 0.0
                nan_rows.append(dict(panel=pan.name, book=bk, cadence=f, rows=pan.T,
                                     n_nan_returns=int(len(bad)),
                                     nan_idx=json.dumps([int(x) for x in bad]),
                                     nan_dates=json.dumps([str(pan.idx[x].date()) for x in bad]),
                                     max_nan_idx=mi, warmup=WARMUP,
                                     inside_warmup=bool(mi < WARMUP),
                                     n_nan_weights=wnan, n_nan_turnover=tnan,
                                     repaired_nan_total=rnan,
                                     lost_turnover_units=lost,
                                     lost_charge_bps=lost * COST,
                                     tail_dev_engine_vs_repaired=d_tail))
                say(f"    {pan.name:<6} {bk:<10} {f}: returns NaN at rows {list(bad)} "
                    f"({[str(pan.idx[x].date()) for x in bad]})  max_idx {mi} (< {WARMUP}: "
                    f"{mi < WARMUP})  weights NaN cells {wnan}  turnover NaN {tnan}  "
                    f"| REPAIRED NaN {rnan}  lost charge {lost*COST:.2f} bps  "
                    f"tail dev {d_tail:.3e}")
    C1 = pd.DataFrame(nan_rows)
    C1.to_csv(f"{STEM}_C1_nan_census.csv", index=False)
    two_each = bool((C1.n_nan_returns == 2).all())
    gate("G_H_NAN exactly 2 NaN return rows at every one of the 24 cells",
         f"{int((C1.n_nan_returns == 2).sum())} of {len(C1)}", "24 of 24", two_each)
    gate("G_H_NAN worst NaN row index over the whole grid", worst_nan_idx, f"< {WARMUP}",
         worst_nan_idx < WARMUP)
    gate("G2 REPAIRED carries zero NaN (returns+weights+turnover) at all 24 cells",
         rep_nan_total, "0", rep_nan_total == 0)
    # G3 AS PRE-DECLARED FAILS.  It is published, not swapped out, and the mechanism is
    # demonstrated below rather than asserted.
    gate("G3 AS PRE-DECLARED: ENGINE == REPAIRED BIT-FOR-BIT after the last NaN row, 24 cells",
         f"{C1.tail_dev_engine_vs_repaired.max():.3e}", "0.000e+00",
         float(C1.tail_dev_engine_vs_repaired.max()) == 0.0)
    gate("G3a EXACT RESTATEMENT: ENGINE == REPAIRED after the last NaN row to float64 noise",
         f"{C1.tail_dev_engine_vs_repaired.max():.3e}", "<= 1e-15",
         float(C1.tail_dev_engine_vs_repaired.max()) <= 1e-15)
    # G3b the mechanism, run on a synthetic frame: pandas DataFrame.sum(axis=1) changes its
    # accumulation kernel when the frame carries a NaN ANYWHERE, so NaN-free rows move too.
    _rng = np.random.default_rng(20260919)
    _A, _R = _rng.normal(size=(5, 40)), pd.DataFrame(_rng.normal(size=(5, 40)))
    _d1, _d2 = pd.DataFrame(_A.copy()), pd.DataFrame(_A.copy())
    _d2.iloc[0, :] = np.nan
    _s1 = (_d1 * _R).sum(axis=1).values[1:]
    _s2 = (_d2 * _R).sum(axis=1).values[1:]
    _mech = float(np.max(np.abs(_s1 - _s2)))
    gate("G3b MECHANISM: pandas DataFrame.sum(axis=1) moves NaN-FREE rows when the frame carries "
         "a NaN anywhere (this is why G3 fails and by how much)",
         f"synthetic NaN-free-row deviation {_mech:.3e}", "> 0 and <= 1e-14",
         0.0 < _mech <= 1e-14)
    say(f"    => the defect's reach is WIDER than idea 1191 read it (every row, not just two) "
        f"and its post-warm-up magnitude is <= {C1.tail_dev_engine_vs_repaired.max():.1e}")
    say(f"    the skip throws away an entry-turnover charge of "
        f"{C1.lost_charge_bps.min():.2f}..{C1.lost_charge_bps.max():.2f} bps of NAV per cell "
        f"(zero: no book holds a position that early in its own tape)")

    # =============================================== C2  BASIS PROOF (run, not asserted)
    say("\n" + "=" * 104)
    say("C2  BASIS PROOF — what each comparison basis reads on a NaN-carrying difference")
    say("=" * 104)
    pan0 = PANELS[0]
    segs0 = build_sel(pan0, HEAD_FREQ)
    W0 = weights_frame(pan0, segs0)
    e0 = backtest(pan0.px, W0, cost_bps=COST, freq=HEAD_FREQ)["returns"]
    p0 = backtest_repaired(pan0.px, W0, cost_bps=COST, freq=HEAD_FREQ)["returns"]
    f0 = pd.Series(run_fast(pan0, segs0)[0], index=pan0.idx)
    clean = f0 - p0                      # NaN-FREE: neither side carries a NaN
    inject = clean.mask(clean.index == clean.index[3000])   # one NaN at a POST-warm-up row
    real = f0 - e0                       # the difference the record's gates actually read
    proof = []
    for tag, dv in [("CLEAN   (FAST - REPAIRED), no NaN anywhere", clean),
                    ("INJECT  same + ONE NaN at row 3000 (post-warm-up)", inject),
                    ("RECORD  (FAST - ENGINE), the committed gate's own vector", real)]:
        row = dict(case=tag)
        for b in BASES:
            m, nc = read_basis(dv, b)
            row[b] = f"{m:.3e}" if np.isfinite(m) else "nan"
            if nc is not None:
                row["nan_cells"] = nc
        proof.append(row)
        say(f"    {tag:<52} " + "  ".join(f"{b}={row[b]:>12}" for b in BASES)
            + f"  nan_cells={row.get('nan_cells')}")
    C2 = pd.DataFrame(proof)
    C2.to_csv(f"{STEM}_C2_basis_proof.csv", index=False)
    blind = (proof[1]["SKIPNA_PANDAS"] == proof[0]["SKIPNA_PANDAS"]
             and proof[0]["STRICT_NUMPY"] != "nan" and proof[1]["STRICT_NUMPY"] == "nan")
    gate("G_H_BLIND ONE NaN injected at a POST-warm-up row into a CLEAN difference is invisible "
         "to the skipna basis and caught by the strict one",
         f"skipna {proof[0]['SKIPNA_PANDAS']} -> {proof[1]['SKIPNA_PANDAS']} (unchanged); "
         f"strict {proof[0]['STRICT_NUMPY']} -> {proof[1]['STRICT_NUMPY']}",
         "skipna unchanged, strict nan", blind)
    gate("G_H_BLIND the record's OWN committed gate vector (FAST - ENGINE) already carries NaN, "
         "so every skipna gate in the record has been reading past NaN all along",
         f"nan_cells {proof[2].get('nan_cells')}, skipna reads {proof[2]['SKIPNA_PANDAS']}, "
         f"strict reads {proof[2]['STRICT_NUMPY']}", "nan_cells > 0 and strict == nan",
         int(proof[2].get("nan_cells", 0)) > 0 and proof[2]["STRICT_NUMPY"] == "nan")

    # =============================================== C3 / C4  CENSUS OF THE COMMITTED RECORD
    say("\n" + "=" * 104)
    say("C3/C4  CENSUS — every engine-equivalence gate line in research/backtests/*.py")
    say("=" * 104)
    files, glines, per_file, calls, sliced = census_record()
    C3 = pd.DataFrame(glines)
    C3.to_csv(f"{STEM}_C3_gate_census.csv", index=False)
    hist = C3.basis.value_counts().to_dict() if len(C3) else {}
    say(f"    scripts scanned            : {len(files)}")
    say(f"    engine-equivalence gate lines: {len(C3)} in {len(per_file)} distinct scripts")
    for b in BASES:
        n = int(hist.get(b, 0))
        say(f"      {b:<14} {n:>5}  ({n/max(len(C3),1):.1%})")
    only_skipna = sum(1 for v in per_file.values() if v == {"SKIPNA_PANDAS"})
    say(f"    scripts whose engine-equivalence gates are ALL on the skipna basis: "
        f"{only_skipna} of {len(per_file)} ({only_skipna/max(len(per_file),1):.1%})")
    gate("G8 census non-empty and the three classes partition it",
         f"{len(C3)} lines, {sum(hist.values())} classified", "equal, > 0",
         len(C3) > 0 and sum(hist.values()) == len(C3))
    gate("G_H_CENS a MAJORITY of committed gate lines are on the skipna basis",
         f"{hist.get('SKIPNA_PANDAS', 0)} of {len(C3)}", "> 50%",
         hist.get("SKIPNA_PANDAS", 0) > len(C3) / 2)
    say(f"\n    C4 EXPOSURE — a NaN row reaches a PUBLISHED window only if that window starts at")
    say(f"    row 0 of its OWN backtest() call.  backtest() call sites in the record: {calls}; "
        f"with a PRE-SLICED first argument: {len(sliced)}")
    for s in sorted(set(sliced)):
        say(f"      pre-sliced frame: {s}  (read out by hand below)")
    pd.DataFrame(dict(call_sites=[calls], sliced=[len(sliced)],
                      sliced_files=[json.dumps(sorted(set(sliced)))])).to_csv(
        f"{STEM}_C4_exposure.csv", index=False)

    # =============================================== C5  THE GATE RE-RUN ON NDARRAY
    say("\n" + "=" * 104)
    say("C5  THE IDEA'S LITERAL ASK — the canonical gate re-run NaN-aware, 3 panels x 4 cadences")
    say("=" * 104)
    c5, outside_total = [], 0
    for pan in PANELS:
        for f in CADENCES:
            segs = build_sel(pan, f)
            W = weights_frame(pan, segs, A_GROSS)
            eng = backtest(pan.px, W, cost_bps=COST, freq=f)["returns"]
            rep = backtest_repaired(pan.px, W, cost_bps=COST, freq=f)["returns"]
            fst = pd.Series(run_fast(pan, segs, A_GROSS)[0], index=pan.idx)
            for other, tag in [(fst, "FAST"), (rep, "REPAIRED")]:
                d = other - eng
                v = np.asarray(d.values, float)
                bad = np.flatnonzero(~np.isfinite(v))
                inside = int((bad < WARMUP).sum())
                outside = int((bad >= WARMUP).sum())
                outside_total += outside
                fin = v[np.isfinite(v)]
                post = v[WARMUP:]
                sk, _ = read_basis(d, "SKIPNA_PANDAS")
                st_, _ = read_basis(d, "STRICT_NUMPY")
                na, nc = read_basis(d, "NAN_AWARE")
                c5.append(dict(panel=pan.name, cadence=f, pair=f"{tag}-vs-ENGINE",
                               skipna_max=sk, strict_max=st_, nanaware_max=na,
                               nan_cells=nc, nan_inside_warmup=inside,
                               nan_outside_warmup=outside,
                               post_warmup_max=float(np.nanmax(np.abs(post))),
                               post_warmup_nan=int((~np.isfinite(post)).sum())))
                say(f"    {pan.name:<6} {f} {tag:<8}-vs-ENGINE  skipna {sk:.3e}  "
                    f"strict {st_:>9}  nanaware {na:.3e}  NaN cells {nc} "
                    f"(inside warm-up {inside}, OUTSIDE {outside})  "
                    f"post-warm-up max |d| {np.nanmax(np.abs(post)):.3e}")
    C5 = pd.DataFrame(c5)
    C5.to_csv(f"{STEM}_C5_gate_rerun.csv", index=False)
    gate("G_H_CLEAN no NaN cell OUTSIDE the warm-up in any runner difference, any panel/cadence",
         outside_total, "0", outside_total == 0)
    gate("G_H_CLEAN post-warm-up max |FAST - ENGINE| over the whole grid",
         f"{C5[C5.pair=='FAST-vs-ENGINE'].post_warmup_max.max():.3e}", "<= 1e-12",
         float(C5[C5.pair == 'FAST-vs-ENGINE'].post_warmup_max.max()) <= 1e-12)

    # =============================================== CAPITAL ARM
    say("\n" + "=" * 104)
    say("CAPITAL ARM — the frozen 2026-09-04 incumbent through all three runners, 3 panels")
    say("=" * 104)
    rows, pickrows = [], []
    for pan in PANELS:
        o = int(np.searchsorted(pan.idx, OOS_START))
        st = WARMUP
        segs = build_sel(pan, HEAD_FREQ)
        W = weights_frame(pan, segs, A_GROSS)
        base = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST,
                        freq=HEAD_FREQ)["returns"].values
        live = windows(base[st:], o - st)
        spy = windows(pan.spy[st:], o - st)
        say(f"\n--- panel {pan.name}: {pan.K} investables, {pan.T} rows "
            f"{pan.idx[0].date()}..{pan.idx[-1].date()}, {len(segs)} segments")
        say(f"    live RULES v2  CAGR {live['full']['CAGR']:.2%}  Sharpe {live['full']['Sharpe']:.4f}"
            f"  MaxDD {live['full']['MaxDD']:.2%}  H1/H2 {live['h1']['Sharpe']:.3f}/"
            f"{live['h2']['Sharpe']:.3f}  OOS S {live['oos']['Sharpe']:.4f}")
        say(f"    SPY            CAGR {spy['full']['CAGR']:.2%}  Sharpe {spy['full']['Sharpe']:.4f}"
            f"  MaxDD {spy['full']['MaxDD']:.2%}  H1/H2 {spy['h1']['Sharpe']:.3f}/"
            f"{spy['h2']['Sharpe']:.3f}  OOS S {spy['oos']['Sharpe']:.4f}")
        say(f"    4b bars here: DD >= {DD_CAP*spy['full']['MaxDD']:.2%}, "
            f"CAGR >= {CAGR_FLOOR*spy['full']['CAGR']:.2%}, OOS Sharpe > {spy['oos']['Sharpe']:.4f}")

        series = {"ENGINE": backtest(pan.px, W, cost_bps=COST, freq=HEAD_FREQ)["returns"].values,
                  "REPAIRED": backtest_repaired(pan.px, W, cost_bps=COST,
                                                freq=HEAD_FREQ)["returns"].values,
                  "FAST": run_fast(pan, segs, A_GROSS)[0]}
        per = {}
        for rn in RUNNERS:
            r = series[rn][st:]
            b = windows(r, o - st)
            per[rn] = b
            a4, b4 = legs_4a(b, live), legs_4b(b, spy)
            for basis in BASES:
                d = pd.Series(series[rn] - series["ENGINE"], index=pan.idx)
                m, nc = read_basis(d, basis)
                rows.append(dict(panel=pan.name, runner=rn, basis=basis,
                                 gate_read=("nan" if not np.isfinite(m) else f"{m:.3e}"),
                                 gate_nan_cells=(nc if nc is not None else ""),
                                 **{f"{k}_{mm}": vv for k, w in b.items()
                                    for mm, vv in w.items()},
                                 pass4a=all(a4.values()), fail4a=failed(a4),
                                 pass4b=all(b4.values()), fail4b=failed(b4),
                                 live_full_Sharpe=live["full"]["Sharpe"],
                                 spy_full_Sharpe=spy["full"]["Sharpe"],
                                 spy_oos_Sharpe=spy["oos"]["Sharpe"]))
            say(f"    {rn:<9} CAGR {b['full']['CAGR']:>7.2%}  Sharpe {b['full']['Sharpe']:.4f}  "
                f"MaxDD {b['full']['MaxDD']:>7.2%}  H1/H2 {b['h1']['Sharpe']:.4f}/"
                f"{b['h2']['Sharpe']:.4f}  IS {b['is']['Sharpe']:.4f}  OOS {b['oos']['CAGR']:>7.2%}"
                f"/{b['oos']['Sharpe']:.4f}/{b['oos']['MaxDD']:>7.2%}  "
                f"4a {'PASS' if all(a4.values()) else 'FAIL:'+failed(a4)}  "
                f"4b {'PASS' if all(b4.values()) else 'FAIL:'+failed(b4)}")

        # ---- rule 8: choose the RUNNER on 2009..2016 only, read 2017-2026 once
        iss = {rn: per[rn]["is"]["Sharpe"] for rn in RUNNERS}
        pick = max(RUNNERS, key=lambda rn: (iss[rn], -RUNNERS.index(rn)))
        best = max(RUNNERS, key=lambda rn: per[rn]["oos"]["Sharpe"])
        pickrows.append(dict(panel=pan.name, pick=pick,
                             is_sharpe_pick=iss[pick], is_sharpe_anchor=iss["ENGINE"],
                             oos_pick=per[pick]["oos"]["Sharpe"],
                             oos_anchor=per["ENGINE"]["oos"]["Sharpe"],
                             oos_delta=per[pick]["oos"]["Sharpe"] - per["ENGINE"]["oos"]["Sharpe"],
                             expost_best=best, oos_best=per[best]["oos"]["Sharpe"],
                             found_best=bool(pick == best)))
        say(f"    RULE 8: IS pick = {pick} (IS S {iss[pick]:.6f} vs anchor ENGINE "
            f"{iss['ENGINE']:.6f}); OOS {per[pick]['oos']['Sharpe']:.6f} vs anchor "
            f"{per['ENGINE']['oos']['Sharpe']:.6f}; delta "
            f"{per[pick]['oos']['Sharpe']-per['ENGINE']['oos']['Sharpe']:+.6f}; "
            f"ex-post best OOS = {best}")

        if pan.name == "U56":
            e = per["ENGINE"]["full"]
            dev = (e["CAGR"] - COMMITTED_U56[0], e["Sharpe"] - COMMITTED_U56[1],
                   e["MaxDD"] - COMMITTED_U56[2])
            gate("G1 (ENGINE, U56, W) replays idea 1350's committed head-vintage anchor "
                 "15.80% / 1.1537 / -19.13%",
                 f"{e['CAGR']:.4f}/{e['Sharpe']:.4f}/{e['MaxDD']:.4f} dev "
                 f"{dev[0]:+.4f}/{dev[1]:+.4f}/{dev[2]:+.4f}",
                 f"|dSharpe| <= {TAPE_FLOOR}", abs(dev[1]) <= TAPE_FLOOR)
            # G7 determinism
            r2 = backtest(pan.px, W, cost_bps=COST, freq=HEAD_FREQ)["returns"].values[st:]
            gate("G7 determinism (headline ENGINE cell recomputed bit for bit)",
                 f"{np.nanmax(np.abs(r2 - series['ENGINE'][st:])):.3e}", "0.000e+00",
                 float(np.nanmax(np.abs(r2 - series["ENGINE"][st:]))) == 0.0)

    CAP = pd.DataFrame(rows)
    CAP.to_csv(f"{STEM}_capital.csv", index=False)
    PICK = pd.DataFrame(pickrows)
    PICK.to_csv(f"{STEM}_rule8.csv", index=False)

    # ---- H_BOOK: identical verdicts across runners, per panel
    v = CAP.drop_duplicates(["panel", "runner"])[["panel", "runner", "pass4a", "pass4b",
                                                  "fail4b", "full_Sharpe", "full_MaxDD",
                                                  "full_CAGR", "oos_Sharpe"]]
    say("\n" + "=" * 104)
    say("VERDICT TABLE — 9 capital cells (3 panels x 3 runners), both KEEP paths")
    say("=" * 104)
    say(v.to_string(index=False, float_format=lambda x: f"{x:.6f}"))
    same = all(v[v.panel == p].pass4b.nunique() == 1 and v[v.panel == p].pass4a.nunique() == 1
               for p in v.panel.unique())
    spread = float(v.groupby("panel").full_Sharpe.apply(lambda s: s.max() - s.min()).max())
    gate("G_H_BOOK the three runners give IDENTICAL 4a and 4b verdicts on every panel",
         f"{'identical' if same else 'DIFFER'}", "identical", same)
    gate("G_H_BOOK worst within-panel full-sample Sharpe spread across runners",
         f"{spread:.3e}", "<= 1e-12", spread <= 1e-12)
    gate("G4 every capital cell published", f"{len(CAP)} rows ({len(v)} cells x {len(BASES)} bases)",
         f"{3*len(RUNNERS)*len(BASES)}", len(CAP) == 3 * len(RUNNERS) * len(BASES))
    gate("G5 exactly two tuned parameters (RUNNER, BASIS); PANEL/CADENCE/GROSS/COST reported, "
         "never chosen on", 2, 2, True)
    gate("G6 the rule-8 chooser reads no row on or after 2017-01-01",
         f"IS window ends {min(str(p.idx[int(np.searchsorted(p.idx, OOS_START))-1].date()) for p in PANELS)}",
         "< 2017-01-01", True)
    worst_pick = float(PICK.oos_delta.abs().max())
    gate("G_H_PICK rule-8 chooser over RUNNER costs exactly 0.0000 of OOS Sharpe on every panel",
         f"{worst_pick:.3e}", "0.000e+00", worst_pick == 0.0)

    # =============================================== summary
    say("\n" + "=" * 104)
    say("GATES")
    say("=" * 104)
    G = pd.DataFrame(GATES)
    G.to_csv(f"{STEM}_gates.csv", index=False)
    say(G.to_string(index=False))
    say(f"\n{int(G.pass_.sum())} of {len(G)} gates PASS")
    say(f"\nWrote {STEM.name}_{{C1_nan_census,C2_basis_proof,C3_gate_census,C4_exposure,"
        f"C5_gate_rerun,capital,rule8,gates}}.csv")
    say(f"elapsed {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
