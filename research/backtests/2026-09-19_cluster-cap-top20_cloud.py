#!/usr/bin/env python3
"""
Idea 1369 (lane cloud, 2026-09-19) — does a CLUSTER CAP on the incumbent's TOP-20 buy the
BINDING 4b DD LEG?

WHY THIS IDEA.  The sprint rule gives this lane the FIRST eligible item in QUEUE.md's '## Open'.
1204 and everything under it down to the 3xx-9xx block are record-bookkeeping censuses of
committed text, gates and margins (plus 429, PARKed for want of a share-volume cache, and 353,
which needs a live yf.download the sandbox cannot make).  None yields a weights function, so none
can carry this sprint's binding step-3 deliverable.  The standing eligibility descent was taken
and 1369 is the FIRST numbered item that does yield it.

THE PREMISE.  The frozen 2026-09-04 KEEP-4b candidate (U56, N=20 slots, H=126-day minimum hold,
gross 0.75, weekly Fri-decide / Mon-trade, 10 bps, t+1) ranks names by a raw 3-leg composite and
takes the top 20 with NO diversification constraint at all.  Nothing stops all 20 slots filling
from one co-moving theme, and the record says the MaxDD CAP is this book's SOLE binding 4b leg
(1215, 1296, 1346, 1358, 1366, 1373 all attack it; 1350 measures the U56 margin at +1.10 pp).
Capping how many slots one return-correlation cluster may take is the classic repair.

THE CONSTRUCTION.  N stays 20 and gross stays 0.75 at EVERY rung: a candidate whose cluster is
already full is SKIPPED and the slot goes to the next eligible name down the SAME composite
ranking (convention FILL).  Only when the eligible pool is exhausted does the book hold fewer than
20 names.  So the cap changes WHICH names are held and NOTHING else — not the slot count, not the
exposure, not the eligibility test, not the weighting (equal, gross/n).  The min-hold is part of
the frozen book, so the cap governs ADDITIONS only; a young held name is never evicted to satisfy
it (a cluster can therefore sit over its cap after a relabel, which is measured and published).

THE ONE DIAL AND NO MORE (PROTOCOL rule 4 — exactly two tuned parameters, cap and panel):
    cap    max slots one cluster may take on a rebalance.  Rungs {2, 3, 4, 5, 6, 20}, ALL
           reported.  cap = 20 >= N is the UNCAPPED incumbent by construction (gate G3).
    panel  {U56, B136, SMALL} — the record's three standing panels.

NOT DIALS, reported at every value (controls, never chosen on):
    RHO {0.50, 0.65}  the correlation threshold that defines a cluster.  Both published at every
                      cap on every panel.
    Clustering is CAUSAL and deterministic: on the first rebalance of each calendar year, from the
    trailing 252 trading days of returns ending at the DECISION row (t-1), a leader algorithm
    assigns each name to the first leader it correlates with at >= RHO, leaders taken in order of
    descending centrality (sum of |corr|), ties by column index.  A name with < 200 valid returns
    in the window is its own singleton.  Labels are frozen until the next year-end refresh, so no
    future row is ever read.
    Paired circular-block bootstrap, 400 reps x 63-row blocks, seed 20260919, identical blocks on
                      both sides, on the (cap-rung minus incumbent) daily difference — full and OOS.

PRE-DECLARED OUTCOMES, written before any number below was read:
  H_BIND   the cap actually BINDS: at RHO 0.65 the uncapped U56 book spends >= 20% of held
           name-weeks with some cluster over 5 slots.  If it does not bind, the idea is answered
           NO for a mechanical reason and the rest is a null result, reported as such.
  H_DD     a cap of 5 shallows U56 MaxDD by at least 0.5 pp against the uncapped incumbent.
  H_COST   the cap is not free: it forces the book down the ranking, so full-sample CAGR falls
           monotonically as the cap tightens.
  H_PICK   the rule-8 chooser (argmax IS net Sharpe over the cap ladder on warm-up..2016-12-31,
           ties to the LOOSEST cap, 2017-2026 read ONCE) does NOT beat the uncapped anchor.
           Every dial the record has walked has failed this (1362 N, 1366 H, 1358 sleeve, 1373 p).
  Whichever fire are reported as they fall.  The capital verdict follows rule 8, not the full sample.

GATES.  G1 the cap=20 U56 cell replays the committed incumbent anchor (15.80% / 1.1537 / -19.13%,
idea 1350's head-vintage triple) to within the 5e-3 tape-vintage Sharpe floor that run established;
the deviation is PUBLISHED, not asserted.  G2 weights sum to exactly gross at every rebalance row
(|dev| < 1e-12).  G3 cap=20 is bit-for-bit identical across both RHO values.  G4 all 36 grid cells
and all controls published.  G5 exactly two tuned parameters.  G6 the chooser reads no row on or
after 2017-01-01.  G7 determinism: the headline cell recomputed bit for bit.  G8 the cluster
labeller reads no row at or after the decision row it is called on.

PROTOCOL: rule 1 committed caches, >= 10 years; rule 2 10 bps per unit turnover, t+1 execution;
rule 3 compared against live RULES v2 AND SPY on each panel; rule 4 both KEEP paths at every cell;
rule 5 one idea, one script, deterministic, standalone; rule 8 walk-forward as above; rule 9
survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py are NOT modified.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists and SMALL a current sub-$2B
screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped first), so every absolute
level is an upper bound and every 4b pass an optimistic one.  The headline is a DIFFERENCE between
two selections from the SAME panel on the SAME days, which is first-order immune to a level bias
common to both; the pass COUNT is not.

Offline and deterministic (committed caches only, no network, no yfinance):
  python research/backtests/2026-09-19_cluster-cap-top20_cloud.py
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

DATE, SLUG = "2026-09-19", "cluster-cap-top20"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_cloud"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
A_N, A_H, A_G = 20, 126, 0.75                  # the frozen 2026-09-04 incumbent
LEGS = [(21, 252), (0, 126), (0, 63)]          # the committed RAW three-leg composite
CAPS = [2, 3, 4, 5, 6, 20]                     # 20 >= N == uncapped incumbent
RHOS = [0.50, 0.65]
CORRWIN, MINOBS = 252, 200
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
SEED, NBOOT, BLOCK = 20260919, 400, 63
COMMITTED_U56 = (0.1580, 1.1537, -0.1913)      # idea 1350 head-vintage anchor
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
        self.iinv = np.arange(len(invest))
        self.rets = q.pct_change().fillna(0.0).values
        self.rets_raw = q.pct_change().values                     # NaN preserved, for corr
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


# ------------------------------------------------------------------ causal clustering
def cluster_labels(pan, ts, rho):
    """Leader clustering of the panel's names from the 252 rows STRICTLY BEFORE ts.

    Deterministic; reads no row at or after ts (gate G8)."""
    lo = max(ts - CORRWIN, 0)
    R = pan.rets_raw[lo:ts]                       # rows lo .. ts-1  (exclusive of ts)
    ok = np.isfinite(R).sum(axis=0) >= MINOBS
    lab = np.full(pan.K, -1, dtype=np.int64)
    idx = np.flatnonzero(ok)
    if len(idx) < 2:
        return np.arange(pan.K)                   # all singletons
    X = R[:, idx]
    X = np.where(np.isfinite(X), X, 0.0)
    X = X - X.mean(axis=0, keepdims=True)
    sd = X.std(axis=0, ddof=0)
    sd[sd <= 0] = 1.0
    X = X / sd
    Cm = (X.T @ X) / X.shape[0]
    np.fill_diagonal(Cm, 1.0)
    central = np.abs(Cm).sum(axis=1)
    order = np.lexsort((idx, -central))           # descending centrality, ties by column index
    leaders: list[int] = []
    nxt = 0
    for j in order:
        placed = False
        for li, lj in enumerate(leaders):
            if Cm[j, lj] >= rho:
                lab[idx[j]] = li
                placed = True
                break
        if not placed:
            leaders.append(j)
            lab[idx[j]] = len(leaders) - 1
    nxt = len(leaders)
    for c in np.flatnonzero(lab < 0):             # too little history -> singleton
        lab[c] = nxt
        nxt += 1
    return lab


def label_schedule(pan, rho):
    """{rebalance row -> labels}, refreshed on the first rebalance of each calendar year."""
    sched, cur, cur_year = {}, None, None
    for t in pan.reb:
        y = pan.idx[t].year
        if cur is None or y != cur_year:
            cur = cluster_labels(pan, max(t - 1, 0), rho)
            cur_year = y
        sched[int(t)] = cur
    return sched


# ------------------------------------------------------------------ the selection, capped
def build_sel(pan, cap, sched, N=A_N, H=A_H, lag=1):
    """Held set per rebalance segment under a per-cluster slot cap.

    cap >= N is the uncapped incumbent (the cluster counter can never bind)."""
    K = pan.K
    segs, diag = [], []
    cur = np.full(K, -1, dtype=np.int64)
    pr, T, nreb = pan.priced, pan.T, len(pan.reb)
    for i, t in enumerate(pan.reb):
        ts = max(t - lag, 0)
        lab = sched[int(t)]
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = [int(c) for c in young]
        cnt: dict[int, int] = {}
        for c in keep:
            cnt[lab[c]] = cnt.get(lab[c], 0) + 1
        over = sum(max(0, v - cap) for v in cnt.values())         # inherited excess, never evicted
        need = N - len(keep)
        take, blocked = [], 0
        if need > 0:
            k = pan.key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            for c in np.argsort(k, kind="stable"):
                if need == 0 or not np.isfinite(k[c]):
                    break
                g = lab[c]
                if cnt.get(g, 0) >= cap:
                    blocked += 1
                    continue
                take.append(int(c))
                cnt[g] = cnt.get(g, 0) + 1
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
            mx = 0
            cc: dict[int, int] = {}
            for c in sel:
                cc[lab[c]] = cc.get(lab[c], 0) + 1
            mx = max(cc.values())
            diag.append(dict(row=int(t), n_held=len(sel), max_cluster=mx, n_clusters=len(cc),
                             blocked=blocked, over_cap=over, days=stop - t))
    return segs, pd.DataFrame(diag)


def run(pan, segs, gross=A_G):
    """Net daily returns; equal weight gross/n over the held set; 10 bps per unit turnover."""
    T = pan.T
    r = np.zeros(T)
    turn_tot = 0.0
    curw = np.zeros(pan.K)
    wdev = 0.0
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


def main():
    t0 = time.time()
    say("=" * 100)
    say("Idea 1369 (lane cloud) — CLUSTER CAP on the frozen 2026-09-04 incumbent's top 20")
    say("=" * 100)

    rows, boots, ctrl, diags = [], [], [], []
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

        anchor = {}
        for rho in RHOS:
            sched = label_schedule(pan, rho)
            nclu = np.mean([len(np.unique(sched[int(t)])) for t in pan.reb])
            say(f"    RHO {rho}: mean {nclu:.1f} clusters over {len(pan.reb)} rebalances")
            for cap in CAPS:
                segs, dg = build_sel(pan, cap, sched)
                rr, extra = run(pan, segs)
                w = windows(rr[st:], o - st)
                b4a, b4b = legs_4a(w, live), legs_4b(w, spy)
                dgm = dg[dg.row >= st]
                share_over5 = float((dgm.max_cluster > 5).mul(dgm.days).sum() / dgm.days.sum())
                rows.append(dict(panel=pan.name, cap=cap, rho=rho, **flat(w),
                                 turnover=extra["turnover"], n_held=float(dgm.n_held.mean()),
                                 max_cluster=float(dgm.max_cluster.mean()),
                                 share_days_maxclu_gt5=share_over5,
                                 blocked_per_reb=float(dgm.blocked.mean()),
                                 over_cap_per_reb=float(dgm.over_cap.mean()),
                                 pass4a=all(b4a.values()), fail4a=failed(b4a),
                                 pass4b=all(b4b.values()), fail4b=failed(b4b),
                                 m4b_DD=(w["full"]["MaxDD"] - DD_CAP * spy["full"]["MaxDD"]) * 100,
                                 m4b_CAGR=(w["full"]["CAGR"] - CAGR_FLOOR * spy["full"]["CAGR"]) * 100,
                                 m4b_OOS=w["oos"]["Sharpe"] - spy["oos"]["Sharpe"],
                                 spy_sharpe=spy["full"]["Sharpe"], live_sharpe=live["full"]["Sharpe"],
                                 wdev=extra["wdev"]))
                dg["panel"], dg["cap"], dg["rho"] = pan.name, cap, rho
                diags.append(dg)
                say(f"    cap={cap:<3} rho={rho}: CAGR {w['full']['CAGR']:7.2%} Sharpe {w['full']['Sharpe']:.4f} "
                    f"MaxDD {w['full']['MaxDD']:7.2%} H1/H2 {w['h1']['Sharpe']:.3f}/{w['h2']['Sharpe']:.3f} "
                    f"OOS {w['oos']['CAGR']:6.2%}/{w['oos']['Sharpe']:.4f}/{w['oos']['MaxDD']:7.2%} "
                    f"trn {extra['turnover']:.2f} nheld {dgm.n_held.mean():.1f} maxclu {dgm.max_cluster.mean():.2f} "
                    f"blk {dgm.blocked.mean():.2f} "
                    f"4b {'PASS' if all(b4b.values()) else 'fail:' + failed(b4b)} "
                    f"4a {'PASS' if all(b4a.values()) else 'fail:' + failed(b4a)}")
                anchor[(rho, cap)] = (rr, w)

        # G3: cap=20 identical across both RHO values (the counter cannot bind)
        d3 = float(np.abs(anchor[(RHOS[0], 20)][0] - anchor[(RHOS[1], 20)][0]).max())
        gate(f"G3-{pan.name}", f"{d3:.3e}", "cap=20 identical across RHO, < 1e-15", d3 < 1e-15)
        gate(f"G2-{pan.name}", f"{max(r['wdev'] for r in rows if r['panel'] == pan.name):.3e}",
             "|sum(w) - gross| < 1e-12", max(r["wdev"] for r in rows if r["panel"] == pan.name) < 1e-12)

        # ---- paired block bootstrap of every cap rung against the uncapped incumbent (RHO 0.65)
        a = anchor[(0.65, 20)][0]
        for cap in CAPS[:-1]:
            rr = anchor[(0.65, cap)][0]
            for lab, sl in (("FULL", slice(st, None)), ("OOS", slice(o, None))):
                d = rr[sl] - a[sl]
                se = block_boot(d)
                boots.append(dict(panel=pan.name, cap=cap, rho=0.65, window=lab,
                                  d_mean_bp=d.mean() * 1e4, se_bp=se * 1e4,
                                  t=d.mean() / se if se else np.nan,
                                  sharpe_cap=sharpe(rr[sl]), sharpe_anchor=sharpe(a[sl]),
                                  d_sharpe=sharpe(rr[sl]) - sharpe(a[sl]),
                                  dd_cap=mdd(rr[sl]), dd_anchor=mdd(a[sl]),
                                  d_dd_pp=(mdd(rr[sl]) - mdd(a[sl])) * 100))

        # ---- rule 8: cap chosen on warm-up..2016 only, 2017-2026 read once (RHO 0.65 control)
        for rho in RHOS:
            pick, best = 20, -np.inf
            for cap in CAPS:
                s_is = sharpe(anchor[(rho, cap)][0][st:o])
                if s_is > best + 1e-12:
                    best, pick = s_is, cap
            wp, wa = anchor[(rho, pick)][1], anchor[(rho, 20)][1]
            bestoos = max(CAPS, key=lambda c: anchor[(rho, c)][1]["oos"]["Sharpe"])
            ctrl.append(dict(panel=pan.name, rho=rho, pick_cap=pick, is_sharpe=best,
                             oos_CAGR_pick=wp["oos"]["CAGR"], oos_Sharpe_pick=wp["oos"]["Sharpe"],
                             oos_MaxDD_pick=wp["oos"]["MaxDD"],
                             oos_CAGR_anchor=wa["oos"]["CAGR"], oos_Sharpe_anchor=wa["oos"]["Sharpe"],
                             oos_MaxDD_anchor=wa["oos"]["MaxDD"],
                             d_oos_Sharpe=wp["oos"]["Sharpe"] - wa["oos"]["Sharpe"],
                             spy_oos_Sharpe=spy["oos"]["Sharpe"], spy_oos_CAGR=spy["oos"]["CAGR"],
                             best_oos_cap=bestoos))
            say(f"    RULE 8 rho={rho}: IS pick cap={pick} (IS Sharpe {best:.4f}) -> OOS Sharpe "
                f"{wp['oos']['Sharpe']:.4f} vs uncapped {wa['oos']['Sharpe']:.4f} "
                f"(delta {wp['oos']['Sharpe'] - wa['oos']['Sharpe']:+.4f}); ex-post best OOS cap={bestoos}")

        if pan.name == "U56":
            wa = anchor[(0.65, 20)][1]["full"]
            dev = (abs(wa["CAGR"] - COMMITTED_U56[0]), abs(wa["Sharpe"] - COMMITTED_U56[1]),
                   abs(wa["MaxDD"] - COMMITTED_U56[2]))
            gate("G1", f"CAGR {wa['CAGR']:.4f} Sharpe {wa['Sharpe']:.4f} MaxDD {wa['MaxDD']:.4f} "
                       f"|dSharpe| {dev[1]:.2e}", f"1350 anchor, |dSharpe| < {TAPE_FLOOR}",
                 dev[1] < TAPE_FLOOR)
            rr2, _ = run(pan, build_sel(pan, 4, label_schedule(pan, 0.65))[0])
            gate("G7", f"{np.abs(rr2 - anchor[(0.65, 4)][0]).max():.3e}", "determinism < 1e-15",
                 np.abs(rr2 - anchor[(0.65, 4)][0]).max() < 1e-15)

    G = pd.DataFrame(rows)
    B = pd.DataFrame(boots)
    C = pd.DataFrame(ctrl)
    D = pd.concat(diags, ignore_index=True)
    G.to_csv(f"{STEM}.grid.csv", index=False)
    B.to_csv(f"{STEM}.bootstrap.csv", index=False)
    C.to_csv(f"{STEM}.rule8.csv", index=False)
    D.to_csv(f"{STEM}.diag.csv.gz", index=False, compression="gzip")

    gate("G4", f"{len(G)} cells", f"{len(CAPS) * len(RHOS) * 3} cells published",
         len(G) == len(CAPS) * len(RHOS) * 3)
    gate("G5", "cap, panel", "exactly 2 tuned parameters (RHO is a published control)", True)
    gate("G6", str(OOS_START.date()), "chooser reads only rows < 2017-01-01", True)
    gate("G8", "labels from rows < decision row", "causal clustering", True)

    say("\n" + "=" * 100)
    say("GRID (all points)")
    say(G[["panel", "cap", "rho", "full_CAGR", "full_Sharpe", "full_MaxDD", "h1_Sharpe", "h2_Sharpe",
           "oos_Sharpe", "oos_MaxDD", "turnover", "n_held", "max_cluster", "blocked_per_reb",
           "pass4a", "pass4b", "fail4b", "m4b_DD", "m4b_CAGR"]].to_string(index=False,
          float_format=lambda x: f"{x:.4f}"))
    say("\nBOOTSTRAP (cap rung minus uncapped incumbent, rho 0.65)")
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
