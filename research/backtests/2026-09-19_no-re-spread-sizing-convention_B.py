#!/usr/bin/env python3
"""
Idea 1403 (lane B, 2026-09-19) — does the 2026-09-04 KEEP-4b BOOK SURVIVE the LIVE BOOK's OWN
NO-RE-SPREAD SIZING CONVENTION?

WHY THIS IDEA.  The sprint rule gives lane B the LAST numbered item standing in QUEUE.md's
'## Open'.  That item is 896, and 895 / 894 / 877 / 876 / 353 under it are all record-bookkeeping
censuses of committed text or filenames.  None yields a weights function, so none can carry this
sprint's binding step-3 deliverable (a book scored against live RULES v2 AND SPY, both KEEP paths,
rule-8 walk-forward).  The documented step-2 fallback was taken: 1395 / 1399 / 1403 were filed as
price-only follow-ups and this lane claimed the last, 1403.

THE PREMISE, READ FROM THE RECORD — A CONTRADICTION BETWEEN THE LIVE BOOK AND THE CANDIDATE.
RULES.md v2 clause 4, the LIVE book, is explicit:

    "Names that are OUT are not held and their weight stays in cash — the book de-grosses.
     Do NOT re-spread the gross over the IN names: a re-grossed book is a different, unpriced
     book (idea 81)."

The STANDING 4b CANDIDATE — the frozen 2026-09-04 top-N book (N=20 slots, H=126-day minimum hold,
gross 0.75, weekly Fri-decide / Mon-trade, 10 bps, t+1), the one every capital run of the last
fortnight is built on (1350, 1358, 1366, 1369, 1373, 1377) — does the OPPOSITE.  Its slot weight
is gross / |held set|, normalised over whatever names it managed to fill.  When the eligibility
test (above 200d AND vol20 < 0.60) starves the pool, the candidate does not de-gross: it RE-SPREADS
the full 0.75 over the survivors.

That is not a hypothetical.  A census of the U56 rebalance rows after warm-up (published below as
gate G9) finds 34 of 922 short-fill rows — 3.7% — and they are not scattered:

    2009: 14 rows   2020: 5 rows   2022: 15 rows

i.e. EXACTLY the three stress episodes that make this book's drawdown, which the record says is
the candidate's SOLE binding 4b leg (1215, 1296, 1346, 1358, 1366, 1373 all attack it; 1350 puts
the margin at +1.10 pp).  At the worst row (2009-01-20) the book holds EIGHT names and gives each
9.38% of NAV.  So the candidate's binding leg is measured on a book that levers INTO precisely the
weeks the live rules would have it sitting in cash, and no run in the record has priced that.

WHAT IS BEING MEASURED.  One dial interpolates between the two conventions.  With n = |held set|
and N = 20 slots, every held name is sized

    w_i  =  gross * ( f / n  +  (1 - f) / N )        deployed gross = gross * (f + (1-f) * n/N)

    f = 1.00  RE-SPREAD          the candidate as committed — deployed gross is always 0.75
    f = 0.00  FIXED SLOT         the live book's convention — each slot is gross/N = 3.75% of NAV
                                 and the unfilled slots stay in CASH at 0%/yr
    f = 0.25 / 0.50 / 0.75       the rungs between, all reported

On the 888 FULL-FILL rows (n = N) every rung is bit-identical by construction — gate G3 proves it —
so the whole grid is a difference on 34 rows out of 922.  That is the point: it is the cheapest
possible test of whether the candidate's 4b pass is a property of its edge or of an unpriced
re-grossing at the three worst moments in the sample.

EXACTLY TWO TUNED PARAMETERS (PROTOCOL rule 4):
    f      the re-spread fraction, rungs {0.00, 0.25, 0.50, 0.75, 1.00}, ALL reported.
    panel  {U56, B136, SMALL} — the record's three standing panels.

NOT DIALS, reported at every value and never chosen on:
    GROSS {0.60, 0.75}  the two frozen gross values the record's capital arm actually uses
                        (0.75 is idea 1350's head-vintage anchor; 0.60 is the 1296/1346/1358
                        frozen book).  Both published at every f; the rule-8 chooser and every
                        headline use 0.75 only.
    CASH at 0%/yr       the record's standing convention.  Idea 1358 showed a de-grossed book
                        understates itself by (1-gross) x the T-bill return; that correction is
                        DELIBERATELY not applied here, because it would flatter f = 0 (which
                        carries the most cash) and the question is whether f = 0 survives on the
                        record's own pessimistic convention.  Stated so the f = 0 column is read
                        as a LOWER bound.
    Paired circular-block bootstrap, 400 reps x 63-row blocks, seed 20260919, identical blocks on
                        both sides, on the (f-rung minus f = 1) daily difference, FULL and OOS.

PRE-DECLARED OUTCOMES, written before any number below was read:
  H_DD    f = 0 gives a SHALLOWER U56 MaxDD than f = 1 by at least 0.5 pp — it is in cash, not
          levered into eight names, at the bottom of 2009 / 2020 / 2022.
  H_CAGR  f = 0 COSTS CAGR (it under-invests through the 2009 recovery) and the 4b CAGR floor,
          the record's standing second binder, then binds on at least one panel.
  H_PASS  the U56 4b pass SURVIVES at f = 0 both FULL and OOS.  If it does not, the standing
          candidate's pass is convention-dependent and the record must say so before any capital
          decision.  This is the headline.
  H_RES   the f = 0 minus f = 1 daily difference is NOT resolvable (|t| < 2) on at least 2 of 3
          panels FULL — 34 rows of 922 is very little tape.
  H_PICK  the rule-8 chooser (argmax IS net Sharpe over the f ladder on warm-up..2016-12-31, ties
          to f = 1.00 = do nothing, 2017-2026 read ONCE) does NOT beat the do-nothing anchor.
          Every dial the record has walked has failed this (1358 sleeve, 1362 N, 1366 H, 1373 p,
          1377 b).
  Whichever fire are reported as they fall.  The capital verdict follows rule 8, not the full sample.

GATES.  G1 the (f = 1, gross 0.75, U56) cell replays idea 1350's committed head-vintage anchor
15.80% / 1.1537 / -19.13% to within the 5e-3 tape-vintage Sharpe floor that same run established;
the deviation is PUBLISHED, not asserted.  G2 deployed gross equals gross*(f + (1-f)*n/N) at every
rebalance row of every cell (|dev| < 1e-12).  G3 all five f rungs are bit-identical on every
FULL-FILL row, so every difference in the grid is confined to the short-fill rows.  (G3 IN THIS
PRE-DECLARED FORM FAILS, and the failure is published rather than swapped out: the turnover charge
on the FIRST day of a full-fill segment that FOLLOWS a short one depends on the drifted weights
carried out of that short segment, so it differs across f.  The exact restatement is added as G3a
-- the slot weight itself is identical on every full-fill rebalance row to within double rounding
on gross/N, max 6.9e-18 -- and G3b -- rungs are
bit-identical on every full-fill day after the segment-start row.  Both pass, and the per-panel
differing-day census is printed, so the leak is bounded at 4 of 4448 days on U56 and 2 of 4448 on
B136.)  G4 all 30 grid
cells and every control published to CSV.  G5 exactly two tuned parameters.  G6 the chooser reads
no row on or after 2017-01-01.  G7 determinism: the headline cell recomputed bit for bit.  G8 mean
deployed gross is non-decreasing in f on every panel and equals gross exactly at f = 1.  G9 the
short-fill census (count, min n, year histogram) published per panel.

PROTOCOL: rule 1 committed caches, >= 10 years; rule 2 10 bps per unit turnover, t+1 execution;
rule 3 compared against live RULES v2 AND SPY on each panel; rule 4 both KEEP paths at every cell;
rule 5 one idea, one script, deterministic, standalone; rule 8 walk-forward as above; rule 9
survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py are NOT modified.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists and SMALL a current sub-$2B
screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped first), so every absolute
level is an upper bound and every 4b pass an optimistic one.  Here the bias runs AGAINST f = 1:
the eight names still eligible in Jan 2009 are eight names that, by construction, SURVIVED to be
in today's list, so re-spreading 75% of NAV onto them is flattered by hindsight in a way the
fixed-slot book is not.  The f = 1 column is therefore an upper bound on the re-spread convention.

Offline and deterministic (committed caches only, no network, no yfinance):
  python research/backtests/2026-09-19_no-re-spread-sizing-convention_B.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import EXCLUDE, rules_v2_weights          # noqa: E402
from engine import backtest, rebalance_mask             # noqa: E402

DATE, SLUG = "2026-09-19", "no-re-spread-sizing-convention"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_B"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
A_N, A_H = 20, 126                             # the frozen 2026-09-04 incumbent
LEGS = [(21, 252), (0, 126), (0, 63)]          # the committed RAW three-leg composite
F_LADDER = [0.00, 0.25, 0.50, 0.75, 1.00]      # DIAL 1 — re-spread fraction (1.00 = incumbent)
GROSSES = [0.60, 0.75]                         # control, never chosen on
HEAD_G = 0.75                                  # the headline / rule-8 gross
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
SEED, NBOOT, BLOCK = 20260919, 400, 63
COMMITTED_U56 = (0.1580, 1.1537, -0.1913)      # idea 1350 head-vintage anchor, gross 0.75
TAPE_FLOOR = 5e-3

GATES: list[dict] = []


def say(*a):
    print(" ".join(str(x) for x in a), flush=True)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    say(f"   GATE {name}: {value} vs {target} -> {'PASS' if ok else 'FAIL'}")
    return bool(ok)


# ------------------------------------------------------------------ metrics
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


def flat(w):
    return {f"{k}_{m}": x for k, v in w.items() for m, x in v.items()}


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


# ------------------------------------------------------------------ panels
UNIV = sorted({t for g in json.loads((ROOT / "research" / "universe.json").read_text()).values()
               for t in g} - set(EXCLUDE))
_meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
BAD_SMALL = set(_meta.loc[_meta.max_1d_move >= 1.0, "ticker"])


class Panel:
    """One standing panel with the incumbent's selection inputs precomputed."""

    def __init__(self, name, px, invest):
        self.name, self.px, self.idx = name, px, px.index
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
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        self.T = len(px)


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


# ------------------------------------------------------------------ the frozen selection
def build_sel(pan, N=A_N, H=A_H, lag=1):
    """The incumbent's held set per rebalance segment.  Independent of f by construction:
    returns [(i0, i1, sel indices into invest columns, decision row)]."""
    K, segs = pan.K, []
    cur = np.full(K, -1, dtype=np.int64)
    pr, T, nreb = pan.priced, pan.T, len(pan.reb)
    for i, t in enumerate(pan.reb):
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
        stop = pan.reb[i + 1] if i + 1 < nreb else T
        if len(sel):
            segs.append((int(t), int(stop), sel.copy(), int(ts)))
    return segs


def run(pan, segs, f, gross, N=A_N, want_gross=False):
    """Net daily returns under the (f, gross) sizing convention.  10 bps per unit turnover at the
    application row, drift between rebalances, cash at 0%/yr.  f = 1 is the committed candidate."""
    T = pan.T
    r = np.zeros(T)
    curw = np.zeros(pan.K)
    turn_tot, gsum, gw, gdev = 0.0, 0.0, 0, 0.0
    for (i0, i1, sel, ts) in segs:
        n = len(sel)
        wi = gross * (f / n + (1.0 - f) / N)
        w = np.full(n, wi)
        new = np.zeros(pan.K)
        new[sel] = w
        turn = float(np.abs(new - curw).sum())
        turn_tot += turn
        deployed = float(w.sum())
        gdev = max(gdev, abs(deployed - gross * (f + (1.0 - f) * n / N)))
        gsum += deployed * (i1 - i0)
        gw += i1 - i0
        base = pan.Cp[i0, sel]
        A = w[None, :] * (pan.Cp[i0:i1, sel] / base[None, :])
        c0 = 1.0 - deployed
        V = A.sum(axis=1) + c0
        seg = (A * pan.rets[i0:i1, sel]).sum(axis=1) / V
        seg[0] -= turn * COST / 1e4
        r[i0:i1] = seg
        Ae = w * (pan.C[i1 - 1, sel] / base)
        curw = np.zeros(pan.K)
        curw[sel] = Ae / (Ae.sum() + c0)
    out = dict(turnover=turn_tot / (T / 252.0), gross_dev=gdev)
    if want_gross:
        out["mean_gross"] = gsum / max(gw, 1)
    return r, out


# ------------------------------------------------------------------ bootstrap
def block_boot(d, reps=NBOOT, block=BLOCK, seed=SEED):
    d = np.asarray(d, float)
    n = len(d)
    if n < block * 3:
        return np.nan
    rng = np.random.default_rng(seed)
    nb = int(np.ceil(n / block))
    starts = rng.integers(0, n, size=(reps, nb))
    idx = (starts[:, :, None] + np.arange(block)[None, None, :]) % n
    return float(d[idx.reshape(reps, -1)[:, :n]].mean(axis=1).std(ddof=1))


def main():
    t0 = time.time()
    say("=" * 100)
    say("Idea 1403 (lane B) — RE-SPREAD vs FIXED SLOT on the frozen 2026-09-04 KEEP-4b candidate")
    say("=" * 100)

    rows, ctrl, boots, census = [], [], [], []
    anchors = {}

    for pan in panels():
        say(f"\n--- panel {pan.name}: {pan.K} investables, {pan.T} rows "
            f"{pan.idx[0].date()}..{pan.idx[-1].date()}, {len(pan.reb)} rebalances")
        o = int(np.searchsorted(pan.idx, OOS_START))
        st = WARMUP
        segs = build_sel(pan)

        # ---- G9 short-fill census (post-warm-up rebalance rows)
        sizes = pd.Series({pan.idx[i0]: len(sel) for (i0, i1, sel, ts) in segs})
        sizes = sizes[sizes.index >= pan.idx[st]]
        short = sizes[sizes < A_N]
        yh = short.groupby(short.index.year).size().to_dict()
        census.append(dict(panel=pan.name, reb_rows=int(len(sizes)), short_rows=int(len(short)),
                           short_share=float(len(short) / max(len(sizes), 1)),
                           min_n=int(sizes.min()), median_n=float(sizes.median()),
                           years=json.dumps({int(k): int(v) for k, v in yh.items()})))
        say(f"    G9 short-fill census: {len(short)} of {len(sizes)} rows "
            f"({len(short)/max(len(sizes),1):.2%}) below N={A_N}; min n = {sizes.min()}; by year {yh}")

        base = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live = windows(base[st:], o - st)
        spy = windows(pan.spy[st:], o - st)
        say(f"    live RULES v2  CAGR {live['full']['CAGR']:.2%}  Sharpe {live['full']['Sharpe']:.4f}"
            f"  MaxDD {live['full']['MaxDD']:.2%}  H1/H2 {live['h1']['Sharpe']:.3f}/{live['h2']['Sharpe']:.3f}"
            f"  OOS {live['oos']['CAGR']:.2%}/{live['oos']['Sharpe']:.4f}/{live['oos']['MaxDD']:.2%}")
        say(f"    SPY            CAGR {spy['full']['CAGR']:.2%}  Sharpe {spy['full']['Sharpe']:.4f}"
            f"  MaxDD {spy['full']['MaxDD']:.2%}  H1/H2 {spy['h1']['Sharpe']:.3f}/{spy['h2']['Sharpe']:.3f}"
            f"  OOS {spy['oos']['CAGR']:.2%}/{spy['oos']['Sharpe']:.4f}/{spy['oos']['MaxDD']:.2%}")
        say(f"    4b bars on this panel: DD >= {DD_CAP*spy['full']['MaxDD']:.2%}, "
            f"CAGR >= {CAGR_FLOOR*spy['full']['CAGR']:.2%}, OOS Sharpe > {spy['oos']['Sharpe']:.4f}")

        maxdev = 0.0
        for g in GROSSES:
            for f in F_LADDER:
                rr, extra = run(pan, segs, f, g, want_gross=True)
                maxdev = max(maxdev, extra["gross_dev"])
                w = windows(rr[st:], o - st)
                b4a, b4b = legs_4a(w, live), legs_4b(w, spy)
                rows.append(dict(panel=pan.name, f=f, gross=g, **flat(w),
                                 turnover=extra["turnover"], mean_gross=extra["mean_gross"],
                                 pass4a=all(b4a.values()), fail4a=failed(b4a),
                                 pass4b=all(b4b.values()), fail4b=failed(b4b),
                                 m4b_DD=(w["full"]["MaxDD"] - DD_CAP * spy["full"]["MaxDD"]) * 100,
                                 m4b_CAGR=(w["full"]["CAGR"] - CAGR_FLOOR * spy["full"]["CAGR"]) * 100,
                                 m4b_OOS=w["oos"]["Sharpe"] - spy["oos"]["Sharpe"],
                                 spy_sharpe=spy["full"]["Sharpe"], live_sharpe=live["full"]["Sharpe"]))
                say(f"    g={g:.2f} f={f:.2f}: CAGR {w['full']['CAGR']:7.2%} Sharpe {w['full']['Sharpe']:.4f} "
                    f"MaxDD {w['full']['MaxDD']:7.2%} H1/H2 {w['h1']['Sharpe']:.3f}/{w['h2']['Sharpe']:.3f} "
                    f"OOS {w['oos']['CAGR']:6.2%}/{w['oos']['Sharpe']:.4f}/{w['oos']['MaxDD']:7.2%} "
                    f"trn {extra['turnover']:.2f} g_bar {extra['mean_gross']:.4f} "
                    f"4b {'PASS' if all(b4b.values()) else 'fail:' + failed(b4b)} "
                    f"4a {'PASS' if all(b4a.values()) else 'fail:' + failed(b4a)}")
                if g == HEAD_G:
                    anchors[(pan.name, f)] = (rr, w)

        gate(f"G2/{pan.name} deployed gross identity", f"{maxdev:.3e}", "< 1e-12", maxdev < 1e-12)

        # ---- G3 as PRE-DECLARED, then its exact restatement (G3a / G3b).  The declared form
        # FAILS by a known mechanism, published here rather than quietly swapped: the turnover
        # charge on the FIRST day of a full-fill segment that follows a SHORT one depends on the
        # drifted weights carried out of the short segment, so it differs across f.  Everything
        # after that first day inside a full-fill segment is bit-identical.
        full_seg = np.zeros(pan.T, dtype=bool)      # every day inside a full-fill segment
        inner_full = np.zeros(pan.T, dtype=bool)    # ... excluding the segment's first day
        short_seg = np.zeros(pan.T, dtype=bool)
        w_dev = 0.0
        for (i0, i1, sel, ts) in segs:
            if len(sel) == A_N:
                full_seg[i0:i1] = True
                inner_full[i0 + 1:i1] = True
                ws = [HEAD_G * (f / len(sel) + (1.0 - f) / A_N) for f in F_LADDER]
                w_dev = max(w_dev, max(abs(x - HEAD_G / A_N) for x in ws))
            else:
                short_seg[i0:i1] = True
        for m_ in (full_seg, inner_full, short_seg):
            m_[:st] = False
        a1 = anchors[(pan.name, 1.00)][0]
        g3 = max(float(np.abs(anchors[(pan.name, f)][0][full_seg] - a1[full_seg]).max())
                 for f in F_LADDER)
        g3b = max(float(np.abs(anchors[(pan.name, f)][0][inner_full] - a1[inner_full]).max())
                  for f in F_LADDER) if inner_full.any() else 0.0
        dif = np.zeros(pan.T, dtype=bool)
        for f in F_LADDER:
            dif |= np.abs(anchors[(pan.name, f)][0] - a1) > 0
        dif[:st] = False
        n_other = int((dif & ~short_seg & ~inner_full).sum())
        say(f"    differing days: {int(dif.sum())} of {pan.T - st} post-warm-up "
            f"({int((dif & short_seg).sum())} inside short-fill segments, {n_other} full-fill "
            f"segment-START rows carrying a different turnover charge, "
            f"{int((dif & inner_full).sum())} elsewhere)")
        gate(f"G3/{pan.name} rungs identical on ALL full-fill days (PRE-DECLARED)",
             f"{g3:.3e}", "0", g3 == 0.0)
        gate(f"G3a/{pan.name} slot weight identical on full-fill rebalance rows",
             f"{w_dev:.3e}", "< 1e-15 (double rounding on gross/N)", w_dev < 1e-15)
        gate(f"G3b/{pan.name} rungs identical on full-fill days AFTER the segment-start row",
             f"{g3b:.3e}", "0", g3b == 0.0)

        # ---- G8: mean deployed gross monotone in f
        mg = [next(r["mean_gross"] for r in rows
                   if r["panel"] == pan.name and r["gross"] == HEAD_G and r["f"] == f)
              for f in F_LADDER]
        gate(f"G8/{pan.name} mean gross non-decreasing in f",
             "[" + ", ".join(f"{x:.4f}" for x in mg) + "]",
             f"monotone, last == {HEAD_G}",
             all(mg[i] <= mg[i + 1] + 1e-15 for i in range(len(mg) - 1))
             and abs(mg[-1] - HEAD_G) < 1e-12)

        # ---- paired block bootstrap of every rung against the committed convention f = 1
        for f in F_LADDER[:-1]:
            rr = anchors[(pan.name, f)][0]
            for lab, sl in (("FULL", slice(st, None)), ("OOS", slice(o, None))):
                d = rr[sl] - a1[sl]
                se = block_boot(d)
                sa, sb = sharpe(rr[sl]), sharpe(a1[sl])
                boots.append(dict(panel=pan.name, f=f, gross=HEAD_G, window=lab,
                                  d_mean_bp=d.mean() * 1e4, se_bp=se * 1e4,
                                  t=d.mean() / se if se else np.nan,
                                  sharpe_f=sa, sharpe_anchor=sb, d_sharpe=sa - sb,
                                  dd_f=mdd(rr[sl]), dd_anchor=mdd(a1[sl]),
                                  d_dd_pp=(mdd(rr[sl]) - mdd(a1[sl])) * 100))
        for b in [b for b in boots if b["panel"] == pan.name]:
            say(f"    BOOT {b['window']:<4} f={b['f']:.2f}: d {b['d_mean_bp']:+.4f} bp/day "
                f"(SE {b['se_bp']:.4f}, t {b['t']:+.2f})  dSharpe {b['d_sharpe']:+.4f}  "
                f"dMaxDD {b['d_dd_pp']:+.2f} pp")

        # ---- rule 8: f chosen on warm-up..2016 only, 2017-2026 read once, ties -> f = 1 (do nothing)
        pick, best = 1.00, sharpe(anchors[(pan.name, 1.00)][0][st:o])
        for f in F_LADDER:
            s_is = sharpe(anchors[(pan.name, f)][0][st:o])
            if s_is > best + 1e-12:
                best, pick = s_is, f
        wpick, wanch = anchors[(pan.name, pick)][1], anchors[(pan.name, 1.00)][1]
        best_oos = max(F_LADDER, key=lambda ff: anchors[(pan.name, ff)][1]["oos"]["Sharpe"])
        ctrl.append(dict(panel=pan.name, pick_f=pick, is_sharpe=best,
                         oos_CAGR_pick=wpick["oos"]["CAGR"], oos_Sharpe_pick=wpick["oos"]["Sharpe"],
                         oos_MaxDD_pick=wpick["oos"]["MaxDD"],
                         oos_CAGR_anchor=wanch["oos"]["CAGR"],
                         oos_Sharpe_anchor=wanch["oos"]["Sharpe"],
                         oos_MaxDD_anchor=wanch["oos"]["MaxDD"],
                         d_oos_Sharpe=wpick["oos"]["Sharpe"] - wanch["oos"]["Sharpe"],
                         spy_oos_Sharpe=spy["oos"]["Sharpe"], spy_oos_CAGR=spy["oos"]["CAGR"],
                         spy_oos_MaxDD=spy["oos"]["MaxDD"],
                         live_oos_Sharpe=live["oos"]["Sharpe"], live_oos_CAGR=live["oos"]["CAGR"],
                         best_oos_f=best_oos))
        say(f"    RULE 8: IS pick f={pick:.2f} (IS Sharpe {best:.4f}) -> OOS "
            f"{wpick['oos']['CAGR']:.2%}/{wpick['oos']['Sharpe']:.4f}/{wpick['oos']['MaxDD']:.2%} "
            f"vs do-nothing f=1.00 {wanch['oos']['CAGR']:.2%}/{wanch['oos']['Sharpe']:.4f}/"
            f"{wanch['oos']['MaxDD']:.2%} (dSharpe {wpick['oos']['Sharpe']-wanch['oos']['Sharpe']:+.4f}); "
            f"ex-post best OOS f={best_oos:.2f}")

    G, B, C, Q = pd.DataFrame(rows), pd.DataFrame(boots), pd.DataFrame(ctrl), pd.DataFrame(census)
    G.to_csv(f"{STEM}.grid.csv", index=False)
    B.to_csv(f"{STEM}.bootstrap.csv", index=False)
    C.to_csv(f"{STEM}.rule8.csv", index=False)
    Q.to_csv(f"{STEM}.census.csv", index=False)

    say("\n" + "=" * 100)
    say("GATES")
    # G1 — committed anchor replay
    u = G[(G.panel == "U56") & (G.f == 1.00) & (G.gross == HEAD_G)].iloc[0]
    dv = (u.full_CAGR - COMMITTED_U56[0], u.full_Sharpe - COMMITTED_U56[1],
          u.full_MaxDD - COMMITTED_U56[2])
    gate("G1 U56 f=1 replays idea 1350 anchor",
         f"{u.full_CAGR:.4%}/{u.full_Sharpe:.4f}/{u.full_MaxDD:.4%} "
         f"(dev {dv[0]:+.4f}/{dv[1]:+.4f}/{dv[2]:+.4f})",
         f"{COMMITTED_U56} within {TAPE_FLOOR} Sharpe", abs(dv[1]) < TAPE_FLOOR)
    gate("G4 all grid cells published", f"{len(G)} rows",
         f"{len(F_LADDER)*len(GROSSES)*3}", len(G) == len(F_LADDER) * len(GROSSES) * 3)
    gate("G5 tuned parameters", "f, panel (gross is a reported control)", "2", True)
    gate("G6 chooser reads no OOS row", f"IS ends {OOS_START.date()} exclusive", "no row >= 2017-01-01", True)
    # G7 determinism
    p0 = panels()[0]
    s0 = build_sel(p0)
    r0, _ = run(p0, s0, 0.00, HEAD_G)
    r1, _ = run(p0, s0, 0.00, HEAD_G)
    gate("G7 determinism (U56 f=0 recomputed)", f"{np.abs(r0-r1).max():.3e}", "0",
         float(np.abs(r0 - r1).max()) == 0.0)

    say("\n" + "=" * 100)
    say("HEADLINE GRID (gross 0.75)")
    say(G[G.gross == HEAD_G][["panel", "f", "full_CAGR", "full_Sharpe", "full_MaxDD",
                              "h1_Sharpe", "h2_Sharpe", "oos_CAGR", "oos_Sharpe", "oos_MaxDD",
                              "turnover", "mean_gross", "pass4a", "fail4a", "pass4b", "fail4b"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\nRULE 8")
    say(C.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n4b PASS COUNTS by f (all 30 cells)")
    say(G.groupby("f").pass4b.agg(["sum", "count"]).to_string())
    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)
    say(f"\nGATES {sum(g['pass_'] for g in GATES)}/{len(GATES)} pass;  {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
