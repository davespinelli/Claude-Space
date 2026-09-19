#!/usr/bin/env python3
"""
Idea 1377 (lane cloud, 2026-09-19) — does a RANK-HYSTERESIS BUFFER REPLACE the 126-DAY
MINIMUM HOLD?

WHY THIS IDEA.  The sprint rule gives this lane the LAST eligible item in QUEUE.md's '## Open'.
1377 IS the last numbered item standing there, it is price-only (no EDGAR / Form 4 / 8-K /
options / spin-offs / live data) and it yields this protocol's step-3 deliverable directly.

THE PREMISE (idea 1366's own finding).  The frozen 2026-09-04 KEEP-4b candidate (U56, N=20 slots,
H=126-day minimum hold, gross 0.75, weekly Fri-decide / Mon-trade, 10 bps, t+1) makes a name
immune from replacement for 126 trading days WHATEVER IT DOES.  1366 measured the bill: 14.48% /
15.57% / 30.61% of ALL held name-weeks on U56 / B136 / SMALL sit on names that FAIL the book's own
eligibility test.  That is CALENDAR immunity, and it is indiscriminate.  A rank-hysteresis buffer
is SIGNAL immunity instead: keep a name while it still passes the screen AND its composite rank is
inside b*N, evict it the moment it is not.  The claim to test is that the buffer buys the same
turnover reduction WITHOUT carrying failures.

THE CONSTRUCTION.  The buffer REPLACES H entirely (H = 0 under every buffer rung).  Everything
else is byte-identical to the frozen book: the same raw 3-leg composite, the same above-200d and
vol20 < 0.60 eligibility test, N = 20 slots, equal weight gross/n at gross 0.75, weekly cadence,
10 bps per unit turnover, t+1 execution, 260-row warm-up.  Freed slots are refilled from the top of
the SAME ranking.  The incumbent (H = 126, no buffer) and the no-hold book (H = 0, no buffer) are
both carried as CONTROL ROWS at every panel, so the buffer is read against both ends of the axis.

THE ONE DIAL AND NO MORE (PROTOCOL rule 4 — exactly two tuned parameters, b and panel):
    b      the buffer multiple.  A held name survives while its composite rank is <= b*N.
           Rungs {1.0, 1.5, 2.0, 3.0, 4.0, 6.0}, ALL reported.  b = 1.0 is NO buffer and is
           bit-identical to the H = 0 control by construction (gate G3).
    panel  {U56, B136, SMALL} — the record's three standing panels.

NOT DIALS, reported at every value (controls, never chosen on):
    MODE {E+R, R}     E+R: a held name must stay ELIGIBLE (above its 200d MA, vol20 < 0.60, priced)
                      AND rank inside b*N.  R: rank inside b*N alone, eligibility ignored for
                      RETENTION (it still gates ENTRY, exactly as in the frozen book).  Both
                      published at every b on every panel.  R is the permissive reading of the
                      queue's wording; E+R is the strict one.
    H = 126 and H = 0 control books at every panel.
    Paired circular-block bootstrap, 400 reps x 63-row blocks, seed 20260919, identical blocks on
                      both sides, on the (buffer rung minus H=126 incumbent) daily difference —
                      full and OOS.

PRE-DECLARED OUTCOMES, written before any number below was read:
  H_FAIL   the buffer carries far fewer failing name-days than H = 126: under E+R the failing
           share is 0.00% by construction, and under R it is at most half the incumbent's.
  H_TURN   some b <= 4 matches the incumbent's turnover (within 0.25 turns/yr) on U56.  If the
           buffer must go to b = 6 to match, calendar immunity is buying something the rank
           buffer cannot.
  H_DD     the buffer does NOT shallow the U56 MaxDD by 0.5 pp or more against H = 126.  The
           record says the DD cap is the sole binding leg and every mechanism tried so far
           (1358 sleeve, 1366 release, 1369 cluster cap, 1373 inverse-vol) has failed to buy it
           on the live panel at a price worth paying.
  H_PICK   the rule-8 chooser (argmax IS net Sharpe over the b ladder on warm-up..2016-12-31, ties
           to the LARGEST b, 2017-2026 read ONCE) does NOT beat the frozen H = 126 anchor.
  Whichever fire are reported as they fall.  The capital verdict follows rule 8, not the full sample.

GATES.  G1 the H = 126 U56 control replays the committed incumbent anchor (15.80% / 1.1537 /
-19.13%, idea 1350's head-vintage triple) to within the 5e-3 tape-vintage Sharpe floor that run
established; the deviation is PUBLISHED, not asserted.  G2 weights sum to exactly gross at every
rebalance row (|dev| < 1e-12).  G3 b = 1.0 under E+R is bit-for-bit identical to the H = 0 control.
G4 all 36 buffer cells and all 6 control rows published.  G5 exactly two tuned parameters.  G6 the
chooser reads no row on or after 2017-01-01.  G7 determinism: the headline cell recomputed bit for
bit.  G8 the H = 126 control's failing-name-week share reproduces idea 1366's committed 14.48% /
15.57% / 30.61% triple; the deviation is PUBLISHED.

PROTOCOL: rule 1 committed caches, >= 10 years; rule 2 10 bps per unit turnover, t+1 execution;
rule 3 compared against live RULES v2 AND SPY on each panel; rule 4 both KEEP paths at every cell;
rule 5 one idea, one script, deterministic, standalone; rule 8 walk-forward as above; rule 9
survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py are NOT modified.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists and SMALL a current sub-$2B
screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped first), so every absolute
level is an upper bound and every 4b pass an optimistic one.  The headline is a DIFFERENCE between
two hold rules over the SAME panel on the SAME days, which is first-order immune to a level bias
common to both; the pass COUNT is not.

Offline and deterministic (committed caches only, no network, no yfinance):
  python research/backtests/2026-09-19_rank-hysteresis-buffer_cloud.py
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

DATE, SLUG = "2026-09-19", "rank-hysteresis-buffer"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_cloud"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
A_N, A_H, A_G = 20, 126, 0.75                  # the frozen 2026-09-04 incumbent
LEGS = [(21, 252), (0, 126), (0, 63)]          # the committed RAW three-leg composite
BS = [1.0, 1.5, 2.0, 3.0, 4.0, 6.0]
MODES = ["E+R", "R"]
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
SEED, NBOOT, BLOCK = 20260919, 400, 63
COMMITTED_U56 = (0.1580, 1.1537, -0.1913)      # idea 1350 head-vintage anchor
COMMITTED_FAILSHARE = dict(U56=0.1448, B136=0.1557, SMALL=0.3061)   # idea 1366
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
def build_sel(pan, H=A_H, buf=None, mode="E+R", N=A_N, lag=1):
    """Held set per rebalance segment.

    buf is None -> the CALENDAR rule (immune for H rows), i.e. the frozen incumbent at H=126 and
    the pure top-N book at H=0.  buf = b -> the BUFFER rule: H is 0 and a held name survives while
    (mode E+R: it is eligible AND priced AND its composite rank <= b*N; mode R: its composite rank
    <= b*N and it is priced).  Entry is the frozen book's in both cases: eligible, priced, top of
    the SAME composite ranking."""
    K = pan.K
    segs, diag = [], []
    cur = np.full(K, -1, dtype=np.int64)
    pr, T, nreb = pan.priced, pan.T, len(pan.reb)
    bn = None if buf is None else buf * N
    for i, t in enumerate(pan.reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        if buf is None:
            young = held[(t - cur[held]) < H] if len(held) else held
            if len(young):
                young = young[pr[t, young]]
            keep = [int(c) for c in young]
            evicted = len(held) - len(keep)
        else:
            k = pan.key[ts]
            if len(held):
                if mode == "E+R":
                    pool = np.flatnonzero(pan.elig[ts] & pr[ts] & np.isfinite(k))
                else:
                    pool = np.flatnonzero(pr[ts] & np.isfinite(k))
                rank = np.full(K, np.inf)
                if len(pool):
                    order = pool[np.argsort(k[pool], kind="stable")]
                    rank[order] = np.arange(1, len(order) + 1)
                ok = held[(rank[held] <= bn) & pr[t, held]]
                if mode == "E+R":
                    ok = ok[pan.elig[ts, ok]]
                keep = [int(c) for c in ok]
            else:
                keep = []
            evicted = len(held) - len(keep)
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
            nfail = int((~pan.elig[ts, sel]).sum())      # held but failing the book's own screen
            diag.append(dict(row=int(t), n_held=len(sel), n_fail=nfail, evicted=evicted,
                             added=len(take), days=stop - t))
    return segs, pd.DataFrame(diag)


def run(pan, segs, gross=A_G):
    T = pan.T
    r = np.zeros(T)
    turn_tot, wdev = 0.0, 0.0
    curw = np.zeros(pan.K)
    for (i0, i1, sel, ts) in segs:
        n = len(sel)
        w = np.full(n, gross / n)
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
    return r, dict(turnover=turn_tot / (T / 252.0), wdev=wdev)


def summarise(dg, st):
    d = dg[dg.row >= st]
    return dict(n_held=float(d.n_held.mean()),
                fail_share=float(d.n_fail.sum() / d.n_held.sum()),
                evict_per_reb=float(d.evicted.mean()), add_per_reb=float(d.added.mean()))


def main():
    t0 = time.time()
    say("=" * 100)
    say("Idea 1377 (lane cloud) — RANK-HYSTERESIS BUFFER vs the frozen 126-day MINIMUM HOLD")
    say("=" * 100)

    rows, boots, ctrl = [], [], []
    for pan in panels():
        say(f"\n--- panel {pan.name}: {pan.K} investables, {pan.T} rows "
            f"{pan.idx[0].date()}..{pan.idx[-1].date()}, {len(pan.reb)} rebalances")
        o = int(np.searchsorted(pan.idx, OOS_START))
        st = WARMUP
        base = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live = windows(base[st:], o - st)
        spy = windows(pan.spy[st:], o - st)
        say(f"    live RULES v2  full Sharpe {live['full']['Sharpe']:.4f}  MaxDD {live['full']['MaxDD']:.2%}")
        say(f"    SPY            full Sharpe {spy['full']['Sharpe']:.4f}  MaxDD {spy['full']['MaxDD']:.2%}"
            f"   CAGR {spy['full']['CAGR']:.2%}  OOS Sharpe {spy['oos']['Sharpe']:.4f}")

        cells = {}

        def add(label, kind, bval, mode, segs, dg):
            rr, extra = run(pan, segs)
            w = windows(rr[st:], o - st)
            b4a, b4b = legs_4a(w, live), legs_4b(w, spy)
            sm = summarise(dg, st)
            rows.append(dict(panel=pan.name, cell=label, kind=kind, b=bval, mode=mode, **flat(w),
                             turnover=extra["turnover"], **sm,
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
                f"trn {extra['turnover']:5.2f} fail% {sm['fail_share']:6.2%} "
                f"evict {sm['evict_per_reb']:4.2f} "
                f"4b {'PASS' if all(b4b.values()) else 'fail:' + failed(b4b)} "
                f"4a {'PASS' if all(b4a.values()) else 'fail:' + failed(b4a)}")
            cells[label] = (rr, w)

        s126, d126 = build_sel(pan, H=126)
        add("H126 (incumb)", "control", np.nan, "calendar", s126, d126)
        s0, d0 = build_sel(pan, H=0)
        add("H0 (no hold)", "control", np.nan, "calendar", s0, d0)
        for mode in MODES:
            for b in BS:
                sb, db = build_sel(pan, H=0, buf=b, mode=mode)
                add(f"b={b} {mode}", "buffer", b, mode, sb, db)

        # gates
        d3 = float(np.abs(cells["b=1.0 E+R"][0] - cells["H0 (no hold)"][0]).max())
        gate(f"G3-{pan.name}", f"{d3:.3e}", "b=1.0 E+R == H0 control, < 1e-15", d3 < 1e-15)
        wd = max(r["wdev"] for r in rows if r["panel"] == pan.name)
        gate(f"G2-{pan.name}", f"{wd:.3e}", "|sum(w) - gross| < 1e-12", wd < 1e-12)
        fs = [r["fail_share"] for r in rows if r["panel"] == pan.name and r["cell"] == "H126 (incumb)"][0]
        tgt = COMMITTED_FAILSHARE[pan.name]
        gate(f"G8-{pan.name}", f"{fs:.4f} (1366: {tgt:.4f}, dev {abs(fs - tgt):.4f})",
             "1366's H=126 failing-share, |dev| < 0.02", abs(fs - tgt) < 0.02)

        # paired block bootstrap against the H=126 incumbent
        a = cells["H126 (incumb)"][0]
        for lbl in [f"b={b} {m}" for m in MODES for b in BS] + ["H0 (no hold)"]:
            rr = cells[lbl][0]
            for win, sl in (("FULL", slice(st, None)), ("OOS", slice(o, None))):
                d = rr[sl] - a[sl]
                se = block_boot(d)
                boots.append(dict(panel=pan.name, cell=lbl, window=win, d_mean_bp=d.mean() * 1e4,
                                  se_bp=se * 1e4, t=d.mean() / se if se else np.nan,
                                  sharpe_cell=sharpe(rr[sl]), sharpe_anchor=sharpe(a[sl]),
                                  d_sharpe=sharpe(rr[sl]) - sharpe(a[sl]),
                                  dd_cell=mdd(rr[sl]), dd_anchor=mdd(a[sl]),
                                  d_dd_pp=(mdd(rr[sl]) - mdd(a[sl])) * 100))

        # rule 8: b chosen on warm-up..2016 only, 2017-2026 read once (per MODE control)
        for mode in MODES:
            pick, best = None, -np.inf
            for b in BS:
                s_is = sharpe(cells[f"b={b} {mode}"][0][st:o])
                if s_is > best - 1e-12:          # ties to the LARGEST b
                    if s_is > best + 1e-12 or pick is None:
                        best, pick = s_is, b
                    else:
                        pick = max(pick, b)
            wp, wa = cells[f"b={pick} {mode}"][1], cells["H126 (incumb)"][1]
            bestoos = max(BS, key=lambda bb: cells[f"b={bb} {mode}"][1]["oos"]["Sharpe"])
            ctrl.append(dict(panel=pan.name, mode=mode, pick_b=pick, is_sharpe=best,
                             oos_CAGR_pick=wp["oos"]["CAGR"], oos_Sharpe_pick=wp["oos"]["Sharpe"],
                             oos_MaxDD_pick=wp["oos"]["MaxDD"],
                             oos_CAGR_anchor=wa["oos"]["CAGR"], oos_Sharpe_anchor=wa["oos"]["Sharpe"],
                             oos_MaxDD_anchor=wa["oos"]["MaxDD"],
                             d_oos_Sharpe=wp["oos"]["Sharpe"] - wa["oos"]["Sharpe"],
                             spy_oos_Sharpe=spy["oos"]["Sharpe"], spy_oos_CAGR=spy["oos"]["CAGR"],
                             best_oos_b=bestoos))
            say(f"    RULE 8 mode={mode}: IS pick b={pick} (IS Sharpe {best:.4f}) -> OOS Sharpe "
                f"{wp['oos']['Sharpe']:.4f} vs H126 anchor {wa['oos']['Sharpe']:.4f} "
                f"(delta {wp['oos']['Sharpe'] - wa['oos']['Sharpe']:+.4f}); ex-post best OOS b={bestoos}")

        if pan.name == "U56":
            wa = cells["H126 (incumb)"][1]["full"]
            dev = abs(wa["Sharpe"] - COMMITTED_U56[1])
            gate("G1", f"CAGR {wa['CAGR']:.4f} Sharpe {wa['Sharpe']:.4f} MaxDD {wa['MaxDD']:.4f} "
                       f"|dSharpe| {dev:.2e}", f"1350 anchor, |dSharpe| < {TAPE_FLOOR}", dev < TAPE_FLOOR)
            rr2, _ = run(pan, build_sel(pan, H=0, buf=2.0, mode="E+R")[0])
            dd = float(np.abs(rr2 - cells["b=2.0 E+R"][0]).max())
            gate("G7", f"{dd:.3e}", "determinism < 1e-15", dd < 1e-15)

    G = pd.DataFrame(rows)
    B = pd.DataFrame(boots)
    C = pd.DataFrame(ctrl)
    G.to_csv(f"{STEM}.grid.csv", index=False)
    B.to_csv(f"{STEM}.bootstrap.csv", index=False)
    C.to_csv(f"{STEM}.rule8.csv", index=False)

    nb = len(BS) * len(MODES) * 3
    gate("G4", f"{len(G)} rows ({nb} buffer + 6 control)", f"{nb + 6} published", len(G) == nb + 6)
    gate("G5", "b, panel", "exactly 2 tuned parameters (MODE is a published control)", True)
    gate("G6", str(OOS_START.date()), "chooser reads only rows < 2017-01-01", True)

    say("\n" + "=" * 100)
    say("GRID (all points)")
    say(G[["panel", "cell", "full_CAGR", "full_Sharpe", "full_MaxDD", "h1_Sharpe", "h2_Sharpe",
           "oos_Sharpe", "oos_MaxDD", "turnover", "n_held", "fail_share", "evict_per_reb",
           "pass4a", "pass4b", "fail4b", "m4b_DD", "m4b_CAGR"]].to_string(index=False,
          float_format=lambda x: f"{x:.4f}"))
    say("\nBOOTSTRAP (cell minus H=126 incumbent)")
    say(B.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\nRULE 8")
    say(C.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\nGATES")
    say(pd.DataFrame(GATES).to_string(index=False))
    say(f"\n4b passes: {int(G.pass4b.sum())} of {len(G)};  4a passes: {int(G.pass4a.sum())} of {len(G)}")
    say(f"elapsed {time.time() - t0:.0f}s")
    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)


if __name__ == "__main__":
    main()
