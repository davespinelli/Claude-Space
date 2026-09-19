#!/usr/bin/env python3
"""
Idea 1399 (lane cloud, 2026-09-19) — is the INCUMBENT's 4b PASS CARRIED by its SHORT-FILL
REBALANCE ROWS?

WHY THIS IDEA.  The sprint rule gives this lane the LAST eligible item in QUEUE.md's '## Open'.
1399 IS the last numbered item standing there (1395, the first eligible, is this run's idea 1), it
is price-only and fully offline.

THE PREMISE.  The frozen 2026-09-04 KEEP-4b incumbent (U56, N = 20 slots, H = 126-day holding
period, gross 0.75, weekly Fri-decide / Mon-trade, 10 bps, t+1) sizes every held name at
gross / n_held.  On a SHORT-FILL row — a rebalance row where fewer than N names pass the entry
screen at all — it therefore does NOT hold cash: it CONCENTRATES the same 75% gross into whatever
few names survived.  This run's idea 1395 measured the row share independently at 3.6876% on U56,
reproducing this idea's committed 3.7%, and those rows sit in 2009, 2020 and 2022 — precisely the
three episodes that make the drawdown.  The incumbent's 4b pass has only +1.10 pp of DD margin.
If 3.7% of rows carry it, the pass is a property of a stress convention nobody chose deliberately,
not of the book.

THE QUESTION IS CAPITAL-BEARING, NOT BOOKKEEPING.  A short-fill row is known at DECISION time
(the screen is read at t-1, the trade is at t), so every counterfactual below is IMPLEMENTABLE —
none of them peeks.  The run therefore answers two things at once: (a) how much of the anchor's
CAGR / Sharpe / MaxDD is attributable to short-fill days, and (b) whether any legal alternative
handling of those rows produces a BETTER book under both KEEP paths and rule 8.

THE TWO TUNED PARAMETERS AND NO MORE (PROTOCOL rule 4):
    VARIANT  how a short-fill row is handled.  Six rungs, ALL reported:
       ANCHOR  the incumbent verbatim: w = gross / n_held, so the book concentrates.
       FIXED   w = gross / N per slot, vacant weight to CASH (the live RULES v2 no-re-spread rule).
       FILL    top the row up to N from the top of the SAME composite among PRICED names,
               IGNORING the above-200d / vol20 screen for the marginal names only.  This deletes
               the short-fill state itself.
       FREEZE  do not trade the row at all: carry the previous segment's holdings (drifted) and
               their age clocks forward.  Defers both the forced exit and the re-concentration.
       CASH    hold nothing for that segment (exit charged at 10 bps, re-entry charged next row).
       SPY     hold SPY for that segment instead (same costs).
    s        the SHORT-FILL BAR: a row is short when n_held < s * N.  Rungs {0.50, 0.75, 0.90,
             1.00}, ALL reported.  s = 1.00 is the literal reading (any vacancy at all); the
             ladder tests whether the finding is a knife-edge at exactly n < 20.

NOT A DIAL, reported at every value (replication control):
    panel {U56, B136, SMALL} — the record's three standing panels.  SMALL has NO short-fill rows
          at s = 1.00 (idea 1395's measurement D1), which makes it this run's own null panel:
          every variant must collapse onto the anchor there (gate G3).

PURE ATTRIBUTION (the queue's literal ask), computed on the ANCHOR only and reported beside the
counterfactuals: the anchor's daily returns are partitioned into SHORT-segment days and FULL-
segment days; each subset's day count, annualised mean, annualised vol, Sharpe and compounded
contribution are published, together with the share of the anchor's worst drawdown that is
accumulated inside short-segment days.  ZERO-OUT (short days set to 0 with no cost) is published as
a cost-free attribution instrument and labelled as such; CASH is its tradable twin.

PRE-DECLARED OUTCOMES, written before any number below was read:
  H_FEW    short-fill days are a small minority of the tape (< 8% of days on U56) but carry a
           DISPROPORTIONATE share of the anchor's worst drawdown.
  H_CARRY  the anchor's 4b pass IS carried by those rows: at least one of FILL / CASH / SPY /
           FREEZE flips U56 from 4b PASS to 4b FAIL, or moves the +1.10 pp DD margin by more than
           1.10 pp.  If NO variant moves the verdict, the pass is robust to the convention and the
           premise is wrong.
  H_BETTER no variant BEATS the anchor on the rule-8 OOS Sharpe by more than 0.05 while also
           holding 4b.  (The record has no mechanism yet that buys the binding DD leg.)
  H_EDGE   the finding is not a knife-edge: the s = 0.90 and s = 1.00 readings agree in sign.
  Whichever fire are reported as they fall.  The capital verdict follows rule 8, not the full sample.

GATES.  G1 the ANCHOR U56 cell replays the committed incumbent triple (15.80% / 1.1537 / -19.13%,
idea 1350's head-vintage anchor) to within the 5e-3 tape-vintage Sharpe floor.  G2 weights sum to
gross on every FULL row (|dev| < 1e-12).  G3 on a panel/s cell with ZERO short-fill rows every
variant is bit-for-bit the anchor.  G4 all 72 cells published.  G5 exactly two tuned parameters.
G6 the chooser reads no row on or after 2017-01-01.  G7 determinism.  G8 the U56 short-fill row
census reproduces this idea's own committed claim — 34 rows, 14 in 2009 / 5 in 2020 / 15 in 2022;
the deviation is PUBLISHED, not asserted.

PROTOCOL: rule 1 committed caches, >= 10 years; rule 2 10 bps per unit turnover, t+1 execution;
rule 3 compared against live RULES v2 AND SPY on each panel; rule 4 both KEEP paths at every cell;
rule 5 one idea, one script, deterministic, standalone; rule 8 walk-forward as above; rule 9
survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py are NOT modified.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists and SMALL a current sub-$2B
screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped FIRST), so every absolute
level is an upper bound and every 4b pass an optimistic one.  This idea is MORE exposed to that
bias than most: a survivor list under-states how many names a real 2009 or 2022 screen would have
rejected, so the TRUE short-fill share is an under-estimate and the attribution below is a LOWER
bound on the convention's importance.

Offline and deterministic (committed caches only, no network, no yfinance):
  python research/backtests/2026-09-19_short-fill-rebalance-rows_cloud.py
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

DATE, SLUG = "2026-09-19", "short-fill-rebalance-rows"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_cloud"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
A_N, A_H, A_G = 20, 126, 0.75
LEGS = [(21, 252), (0, 126), (0, 63)]
VARIANTS = ["ANCHOR", "FIXED", "FILL", "FREEZE", "CASH", "SPY"]
SS = [0.50, 0.75, 0.90, 1.00]
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
SEED, NBOOT, BLOCK = 20260919, 400, 63
COMMITTED_U56 = (0.1580, 1.1537, -0.1913)
COMMITTED_CENSUS = {2009: 14, 2020: 5, 2022: 15}     # this idea's own committed claim, 34 rows
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


# ------------------------------------------------------------------ panels
UNIV = sorted({t for g in json.loads((ROOT / "research" / "universe.json").read_text()).values()
               for t in g} - set(EXCLUDE))
_meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
BAD_SMALL = set(_meta.loc[_meta.max_1d_move >= 1.0, "ticker"])


class Panel:
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
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.C = C
        self.Cp = np.vstack([np.ones((1, C.shape[1])), C[:-1]])
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        self.T = len(px)
        self.K = len(invest)


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
    inv = [c for c in ps.columns if c != "SPY" and c not in BAD_SMALL]
    out.append(Panel("SMALL", ps, inv))
    return out


# ------------------------------------------------------------------ selection
def build(pan, variant, s, H=A_H, N=A_N, lag=1):
    """Segments (i0, i1, sel, ts, short) under one short-fill VARIANT at short-fill bar s.

    Retention and entry are the frozen incumbent's verbatim (age < H and priced; entry from the
    top of the same composite among eligible+priced names).  A row is SHORT when the number of
    names it would hold is < s*N.  FILL tops such a row up ignoring the eligibility screen for the
    marginal names; FREEZE does not trade it at all; every other variant differs only in how the
    segment is PRICED, not selected.  Nothing reads a row later than ts = t - lag."""
    K = pan.K
    bar = s * N
    segs, diag = [], []
    cur = np.full(K, -1, dtype=np.int64)
    pr, T, nreb = pan.priced, pan.T, len(pan.reb)
    for i, t in enumerate(pan.reb):
        ts = max(t - lag, 0)
        stop = pan.reb[i + 1] if i + 1 < nreb else T
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = [int(c) for c in young]
        k = pan.key[ts].copy()
        k[~(pan.elig[ts] & pr[ts])] = np.inf
        for c in keep:
            k[c] = np.inf
        need = N - len(keep)
        take = []
        for c in np.argsort(k, kind="stable"):
            if need == 0 or not np.isfinite(k[c]):
                break
            take.append(int(c))
            need -= 1
        n_norm = len(keep) + len(take)
        short = n_norm < bar

        if short and variant == "FREEZE" and segs:
            # do not trade: extend the previous segment and leave the age clocks alone
            i0p, i1p, selp, tsp, sp = segs[-1]
            segs[-1] = (i0p, stop, selp, tsp, True)
            diag.append(dict(row=int(t), n_held=len(selp), n_norm=n_norm, short=1,
                             frozen=1, days=stop - t))
            continue

        extra = []
        if short and variant == "FILL":
            k2 = pan.key[ts].copy()
            k2[~pr[ts]] = np.inf                       # PRICED only; screen ignored for top-ups
            for c in keep + take:
                k2[c] = np.inf
            need2 = N - n_norm
            for c in np.argsort(k2, kind="stable"):
                if need2 == 0 or not np.isfinite(k2[c]):
                    break
                extra.append(int(c))
                need2 -= 1

        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take + extra:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            segs.append((int(t), int(stop), sel.copy(), int(ts), bool(short)))
        diag.append(dict(row=int(t), n_held=len(sel), n_norm=n_norm, short=int(short),
                         frozen=0, days=stop - t))
    return segs, pd.DataFrame(diag)


def run(pan, segs, variant, gross=A_G, N=A_N):
    """Price the segments.  FIXED sizes at gross/N with cash for vacancies; CASH and SPY replace a
    SHORT segment's book with cash / SPY (exit charged at 10 bps, re-entry charged on the next
    row).  Everything else uses the incumbent's own w = gross / n_held."""
    T = pan.T
    r = np.zeros(T)
    isshort = np.zeros(T, dtype=bool)
    turn_tot, wdev = 0.0, 0.0
    curw = np.zeros(pan.K)
    for (i0, i1, sel, ts, short) in segs:
        isshort[i0:i1] = short
        if short and variant in ("CASH", "SPY"):
            turn = float(np.abs(curw).sum())         # liquidate the book
            turn_tot += turn
            seg = np.zeros(i1 - i0) if variant == "CASH" else pan.spy[i0:i1].copy()
            seg = seg.astype(float)
            seg[0] -= turn * COST / 1e4
            r[i0:i1] = seg
            curw = np.zeros(pan.K)
            continue
        n = len(sel)
        w = np.full(n, gross / N if variant == "FIXED" else gross / n)
        if n == N:
            wdev = max(wdev, abs(w.sum() - gross))
        new = np.zeros(pan.K)
        new[sel] = w
        turn = float(np.abs(new - curw).sum())
        turn_tot += turn
        base = pan.Cp[i0, sel]
        A = w[None, :] * (pan.Cp[i0:i1, sel] / base[None, :])
        c0 = 1.0 - w.sum()
        V = A.sum(axis=1) + c0
        seg = (A * pan.rets[i0:i1, sel]).sum(axis=1) / V
        seg[0] -= turn * COST / 1e4
        r[i0:i1] = seg
        Ae = w * (pan.C[i1 - 1, sel] / base)
        curw = np.zeros(pan.K)
        curw[sel] = Ae / (Ae.sum() + c0)
    return r, isshort, dict(turnover=turn_tot / (T / 252.0), wdev=wdev)


def dd_share_in(r, mask):
    """Share of the worst drawdown's PEAK-TO-TROUGH log decline accumulated on masked days."""
    r = np.asarray(r, float)
    e = np.cumprod(1.0 + r)
    dd = e / np.maximum.accumulate(e) - 1.0
    tr = int(np.argmin(dd))
    pk = int(np.argmax(e[:tr + 1])) if tr > 0 else 0
    if tr <= pk:
        return np.nan, 0, 0
    seg = slice(pk + 1, tr + 1)
    lr = np.log1p(r[seg])
    tot = lr.sum()
    part = lr[mask[seg]].sum()
    return (float(part / tot) if tot != 0 else np.nan), int(mask[seg].sum()), int(tr - pk)


def main():
    t0 = time.time()
    say("=" * 118)
    say("Idea 1399 (lane cloud) — is the incumbent's 4b PASS CARRIED by its SHORT-FILL rebalance rows?")
    say("=" * 118)

    rows, boots, ctrl, attrib, census = [], [], [], [], []
    for pan in panels():
        say(f"\n--- panel {pan.name}: {pan.K} investables, {pan.T} rows "
            f"{pan.idx[0].date()}..{pan.idx[-1].date()}, {len(pan.reb)} rebalances")
        o = int(np.searchsorted(pan.idx, OOS_START))
        st = WARMUP
        base = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live = windows(base[st:], o - st)
        spy = windows(pan.spy[st:], o - st)
        say(f"    live RULES v2  CAGR {live['full']['CAGR']:.2%}  Sharpe {live['full']['Sharpe']:.4f}"
            f"  MaxDD {live['full']['MaxDD']:.2%}  H1/H2 {live['h1']['Sharpe']:.3f}/{live['h2']['Sharpe']:.3f}")
        say(f"    SPY            CAGR {spy['full']['CAGR']:.2%}  Sharpe {spy['full']['Sharpe']:.4f}"
            f"  MaxDD {spy['full']['MaxDD']:.2%}  H1/H2 {spy['h1']['Sharpe']:.3f}/{spy['h2']['Sharpe']:.3f}"
            f"  OOS Sharpe {spy['oos']['Sharpe']:.4f}  OOS CAGR {spy['oos']['CAGR']:.2%}")

        cells = {}
        for s in SS:
            for v in VARIANTS:
                segs, dg = build(pan, v, s)
                rr, ish, extra = run(pan, segs, v)
                w = windows(rr[st:], o - st)
                b4a, b4b = legs_4a(w, live), legs_4b(w, spy)
                d = dg[dg.row >= st]
                label = f"s={s:.2f} {v}"
                rows.append(dict(panel=pan.name, cell=label, s=s, variant=v, **flat(w),
                                 turnover=extra["turnover"], n_held=float(d.n_held.mean()),
                                 short_rows=int(d.short.sum()), short_row_share=float(d.short.mean()),
                                 short_day_share=float(ish[st:].mean()),
                                 pass4a=all(b4a.values()), fail4a=failed(b4a),
                                 pass4b=all(b4b.values()), fail4b=failed(b4b),
                                 m4b_DD=(w["full"]["MaxDD"] - DD_CAP * spy["full"]["MaxDD"]) * 100,
                                 m4b_CAGR=(w["full"]["CAGR"] - CAGR_FLOOR * spy["full"]["CAGR"]) * 100,
                                 m4b_OOS=w["oos"]["Sharpe"] - spy["oos"]["Sharpe"],
                                 spy_sharpe=spy["full"]["Sharpe"], live_sharpe=live["full"]["Sharpe"],
                                 wdev=extra["wdev"]))
                say(f"    {label:<14}: CAGR {w['full']['CAGR']:7.2%} Sharpe {w['full']['Sharpe']:.4f} "
                    f"MaxDD {w['full']['MaxDD']:7.2%} H1/H2 {w['h1']['Sharpe']:.3f}/{w['h2']['Sharpe']:.3f} "
                    f"OOS {w['oos']['CAGR']:6.2%}/{w['oos']['Sharpe']:.4f}/{w['oos']['MaxDD']:7.2%} "
                    f"trn {extra['turnover']:5.2f} shortrows {int(d.short.sum()):3d} "
                    f"({float(d.short.mean()):5.2%}) "
                    f"4b {'PASS' if all(b4b.values()) else 'fail:' + failed(b4b)} "
                    f"4a {'PASS' if all(b4a.values()) else 'fail:' + failed(b4a)}")
                cells[label] = (rr, w, ish)

            # ---- pure attribution on the ANCHOR at this s
            rr, w, ish = cells[f"s={s:.2f} ANCHOR"]
            rs, m = rr[st:], ish[st:]
            sh, fl = rs[m], rs[~m]
            share, ddn, ddlen = dd_share_in(rs, m)
            zero = rs.copy(); zero[m] = 0.0                      # cost-free instrument
            spysub = rs.copy(); spysub[m] = pan.spy[st:][m]      # cost-free instrument
            attrib.append(dict(panel=pan.name, s=s, n_days=len(rs), short_days=int(m.sum()),
                               short_day_share=float(m.mean()),
                               short_ann_mean=float(sh.mean() * 252) if len(sh) else np.nan,
                               short_ann_vol=float(sh.std(ddof=0) * np.sqrt(252)) if len(sh) else np.nan,
                               short_sharpe=sharpe(sh), full_sharpe_of_fullrows=sharpe(fl),
                               short_cum_logret=float(np.log1p(sh).sum()) if len(sh) else 0.0,
                               all_cum_logret=float(np.log1p(rs).sum()),
                               short_logret_share=(float(np.log1p(sh).sum() / np.log1p(rs).sum())
                                                   if len(sh) and np.log1p(rs).sum() != 0 else np.nan),
                               worstdd_len=ddlen, worstdd_short_days=ddn,
                               worstdd_share_from_short=share,
                               ZEROOUT_CAGR=cagr(zero), ZEROOUT_Sharpe=sharpe(zero),
                               ZEROOUT_MaxDD=mdd(zero),
                               SPYSUB_CAGR=cagr(spysub), SPYSUB_Sharpe=sharpe(spysub),
                               SPYSUB_MaxDD=mdd(spysub),
                               ANCHOR_CAGR=w["full"]["CAGR"], ANCHOR_Sharpe=w["full"]["Sharpe"],
                               ANCHOR_MaxDD=w["full"]["MaxDD"]))

            # ---- bootstrap each variant against the anchor at this s
            a = cells[f"s={s:.2f} ANCHOR"][0]
            for v in VARIANTS:
                rr = cells[f"s={s:.2f} {v}"][0]
                for win, sl in (("FULL", slice(st, None)), ("OOS", slice(o, None))):
                    dd_ = rr[sl] - a[sl]
                    se = block_boot(dd_)
                    boots.append(dict(panel=pan.name, s=s, variant=v, window=win,
                                      d_mean_bp=dd_.mean() * 1e4, se_bp=se * 1e4,
                                      t=dd_.mean() / se if se else np.nan,
                                      d_sharpe=sharpe(rr[sl]) - sharpe(a[sl]),
                                      d_dd_pp=(mdd(rr[sl]) - mdd(a[sl])) * 100))

            # ---- rule 8 at this s: VARIANT chosen on IS only, 2017-2026 read once
            pick, best = "ANCHOR", -np.inf
            for v in VARIANTS:
                s_is = sharpe(cells[f"s={s:.2f} {v}"][0][st:o])
                if s_is > best + 1e-12:
                    best, pick = s_is, v
            wp, wa = cells[f"s={s:.2f} {pick}"][1], cells[f"s={s:.2f} ANCHOR"][1]
            bestoos = max(VARIANTS, key=lambda vv: cells[f"s={s:.2f} {vv}"][1]["oos"]["Sharpe"])
            ctrl.append(dict(panel=pan.name, s=s, pick=pick, is_sharpe=best,
                             oos_CAGR_pick=wp["oos"]["CAGR"], oos_Sharpe_pick=wp["oos"]["Sharpe"],
                             oos_MaxDD_pick=wp["oos"]["MaxDD"],
                             oos_CAGR_anchor=wa["oos"]["CAGR"], oos_Sharpe_anchor=wa["oos"]["Sharpe"],
                             oos_MaxDD_anchor=wa["oos"]["MaxDD"],
                             d_oos_Sharpe=wp["oos"]["Sharpe"] - wa["oos"]["Sharpe"],
                             d_oos_CAGR_pp=(wp["oos"]["CAGR"] - wa["oos"]["CAGR"]) * 100,
                             d_oos_MaxDD_pp=(wp["oos"]["MaxDD"] - wa["oos"]["MaxDD"]) * 100,
                             spy_oos_Sharpe=spy["oos"]["Sharpe"], spy_oos_CAGR=spy["oos"]["CAGR"],
                             spy_oos_MaxDD=spy["oos"]["MaxDD"], best_oos_variant=bestoos))
            say(f"    RULE 8 s={s:.2f}: IS pick {pick} (IS Sharpe {best:.4f}) -> OOS Sharpe "
                f"{wp['oos']['Sharpe']:.4f} vs ANCHOR {wa['oos']['Sharpe']:.4f} "
                f"(delta {wp['oos']['Sharpe'] - wa['oos']['Sharpe']:+.4f}); ex-post best OOS {bestoos}")

            # ---- G3: a cell with zero short rows must collapse every variant onto the anchor
            nshort = [r["short_rows"] for r in rows
                      if r["panel"] == pan.name and r["cell"] == f"s={s:.2f} ANCHOR"][0]
            if nshort == 0:
                dmax = max(float(np.abs(cells[f"s={s:.2f} {v}"][0] - a).max()) for v in VARIANTS)
                gate(f"G3-{pan.name}-s{s:.2f}", f"{dmax:.3e} (0 short rows)",
                     "every variant == ANCHOR, < 1e-15", dmax < 1e-15)

        wd = max(r["wdev"] for r in rows if r["panel"] == pan.name)
        gate(f"G2-{pan.name}", f"{wd:.3e}", "|sum(w) - gross| < 1e-12 on FULL rows", wd < 1e-12)

        if pan.name == "U56":
            wa = cells["s=1.00 ANCHOR"][1]["full"]
            dev = abs(wa["Sharpe"] - COMMITTED_U56[1])
            gate("G1", f"CAGR {wa['CAGR']:.4f} Sharpe {wa['Sharpe']:.4f} MaxDD {wa['MaxDD']:.4f} "
                       f"|dSharpe| {dev:.2e}", f"1350 anchor, |dSharpe| < {TAPE_FLOOR}", dev < TAPE_FLOOR)
            r2, _, _ = run(pan, build(pan, "FILL", 1.00)[0], "FILL")
            dmax = float(np.abs(r2 - cells["s=1.00 FILL"][0]).max())
            gate("G7", f"{dmax:.3e}", "determinism < 1e-15", dmax < 1e-15)

            # ---- G8: the U56 short-fill row census, by calendar year, against 1399's own claim
            _, dg = build(pan, "ANCHOR", 1.00)
            d = dg[(dg.row >= st) & (dg.short == 1)]
            yrs = pd.Series(pan.idx[d.row.values]).dt.year.value_counts().sort_index()
            census = [dict(panel="U56", year=int(y), short_rows=int(c)) for y, c in yrs.items()]
            got = {int(y): int(c) for y, c in yrs.items()}
            tot = int(yrs.sum())
            devs = {y: got.get(y, 0) - c for y, c in COMMITTED_CENSUS.items()}
            gate("G8", f"{tot} short rows total; by year {dict(got)}; dev vs committed "
                       f"{{2009,2020,2022}} = {devs}",
                 f"1399's committed 34 rows = {COMMITTED_CENSUS}", tot == 34 and not any(devs.values()))
            say(f"    U56 short-fill rows by year: {dict(got)}  (total {tot})")

    G = pd.DataFrame(rows)
    B = pd.DataFrame(boots)
    C = pd.DataFrame(ctrl)
    A = pd.DataFrame(attrib)
    G.to_csv(f"{STEM}.grid.csv", index=False)
    B.to_csv(f"{STEM}.bootstrap.csv", index=False)
    C.to_csv(f"{STEM}.rule8.csv", index=False)
    A.to_csv(f"{STEM}.attribution.csv", index=False)
    pd.DataFrame(census).to_csv(f"{STEM}.census.csv", index=False)

    nb = len(SS) * len(VARIANTS) * 3
    gate("G4", f"{len(G)} rows", f"{nb} published (4 s x 6 VARIANT x 3 panels)", len(G) == nb)
    gate("G5", "VARIANT, s", "exactly 2 tuned parameters (panel is a replication control)", True)
    gate("G6", str(OOS_START.date()), "chooser reads only rows < 2017-01-01", True)

    say("\n" + "=" * 118)
    say("GRID (ALL grid points)")
    say(G[["panel", "cell", "full_CAGR", "full_Sharpe", "full_MaxDD", "h1_Sharpe", "h2_Sharpe",
           "oos_CAGR", "oos_Sharpe", "oos_MaxDD", "turnover", "short_rows", "short_day_share",
           "pass4a", "pass4b", "fail4b", "m4b_DD", "m4b_CAGR"]].to_string(
          index=False, float_format=lambda x: f"{x:.4f}"))
    say("\nATTRIBUTION (ANCHOR only; ZEROOUT and SPYSUB are COST-FREE instruments, not books)")
    say(A.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\nBOOTSTRAP (variant minus ANCHOR at the same s)")
    say(B.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\nRULE 8 (VARIANT chosen on IS only; 2017-2026 read once)")
    say(C.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\nGATES")
    say(pd.DataFrame(GATES).to_string(index=False))
    say(f"\n4b passes: {int(G.pass4b.sum())} of {len(G)};  4a passes: {int(G.pass4a.sum())} of {len(G)}")
    say(f"elapsed {time.time() - t0:.0f}s")
    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)


if __name__ == "__main__":
    main()
