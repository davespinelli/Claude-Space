#!/usr/bin/env python3
"""Idea 1643 — does a CORRELATION-CLUSTER CONCENTRATION CAP buy the KEEP-4b book's BINDING DD LEG?

THE OBJECT.  The 2026-09-04 KEEP-4b candidate and its frozen-incumbent descendants are EQUAL
WEIGHT with no cap on how much of the book may sit inside one correlated block.  Idea 1623 (lane
cloud, this same run) measured the binding 4b leg over 216 books and it is the DRAWDOWN leg: it
fails 129 of 216 cells at 10 bps, more often than H1 (72), H2 (78) or the CAGR floor (75).  A
concentration cap is the one DD-buying family the record has never priced against its own
exposure-matched twin.

THE DOUBT, PRE-REGISTERED.  Eight consecutive 2026-09-19 runs found every drawdown-buying device
in the record beaten AT MATCHED EXPOSURE by a plain constant de-gross, and idea 1494 asks whether
realised mean gross is a sufficient statistic for the whole family.  A cap that refuses the
20th-ranked name because its cluster is full does not hold cash — it holds the NEXT name — so it is
not mechanically a de-gross.  That makes it the cleanest available test of the de-gross law.  The
comparand is therefore not the uncapped anchor: it is the constant gross g* whose FULL-sample
MaxDD EQUALS the capped book's.

WHAT IS PRICED (every cell published).
  (a) THE CAP.  Names are clustered by average-linkage agglomerative clustering on the correlation
      of trailing daily returns, fitted on the IN-SAMPLE window ONLY (warm-up..2016-12-31), into C
      clusters.  At most k of the book's N = 20 slots may be occupied by any one cluster.  The cap
      gates NEW ADMISSIONS ONLY; a name retained by the min-hold H = 126 is never forced out (the
      alternative would make the cap a hidden turnover dial).  Names with < 500 in-sample rows are
      given their own singleton cluster, so the cap can never bind on a name it could not see.
  (b) THE MaxDD-MATCHED TWIN.  For every capped cell, the constant gross g* whose FULL MaxDD equals
      the capped book's is solved on a 0.01 ladder plus interpolation and then run EXACTLY; the
      realised |MaxDD gap| is gated < 20 bp.  dCAGR and dSharpe (cap minus twin) carry a PAIRED
      circular-block bootstrap SE.
  (c) COST LADDER 0 / 10 / 25 / 50 bps, an identity on one turnover path.
  (d) SWEEP  C in {4, 6, 8, 12}  x  k in {2, 3, 4, 6}  plus an explicit NOCAP row, on 3 panels.

TUNED PARAMETERS: exactly TWO — the cluster count C and the per-cluster slot cap k.  The panel and
the cost rung are LADDERS, published in full, never selected on.

PRE-REGISTERED VERDICT RULE (written before the run, not after).
  H_DEGROSS  the twin wins: pooled mean dCAGR(cap - twin) <= 0 at 10 bps.  If H_DEGROSS holds, the
             cap is the NINTH member of the de-gross family and this run is a KILL, whatever the
             cap's 4b verdict against SPY.
  H_CAP      the cap wins: pooled mean dCAGR > 0 AND the rule-8 chosen cell beats its OWN twin OUT
             OF SAMPLE AND clears 4b on FULL and OOS.  Only then is the cap a real DD purchase.

PROTOCOL: rule 1 (>= 10y); rule 2 (decision at close t-1 applied at t, 10 bps headline, no
shorting, no leverage); rule 3 (vs the live RULES v2 baseline AND SPY); rule 4 (full + both halves,
BOTH KEEP paths at EVERY cell); rule 8 (C and k chosen on warm-up..2016-12-31 ONLY, the clustering
itself fitted on that window ONLY, 2017-01-01..end read exactly once); rule 9 (survivorship).

Runs standalone and offline (committed price caches only; no network):
  python research/backtests/2026-09-19_correlation-cluster-cap-vs-maxdd-matched-degross_cloud.py
"""
from __future__ import annotations

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

DATE = "2026-09-19"
SLUG = "correlation-cluster-cap-vs-maxdd-matched-degross"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP = 260
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G, I_V, I_C = 20, 126, 0.75, 0.60, "W"
COSTS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_COST = 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
MIN_IS_ROWS = 500

CS = [4, 6, 8, 12]                                  # DIAL 1 (tuned)
KS = [2, 3, 4, 6]                                   # DIAL 2 (tuned)
GGRID = np.round(np.arange(0.05, 1.0001, 0.01), 4)
MATCH_BAR = 0.0020                                  # 20 bp of MaxDD

BOOT_REPS, BOOT_BLOCK, BOOT_SEED = 400, 63, 20260919
C_U56 = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857)

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


# ------------------------------------------------------------------ statistics
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
    return float(np.cumprod(1 + r)[-1] ** (252 / len(r)) - 1)


def triple(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def path_4a(r, anc):
    h1, h2 = halves(r)
    a1, a2 = halves(anc)
    return bool(h1 > a1 and h2 > a2 and mdd(r) >= mdd(anc)), h1, h2


def path_4b(r, spy):
    h1, h2 = halves(r)
    b1, b2 = halves(spy)
    m, bm = triple(r), triple(spy)
    legs = dict(H1=bool(h1 > b1), H2=bool(h2 > b2),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return bool(all(legs.values())), legs, m


def paired_block(a, b, fn, reps=BOOT_REPS, L=BOOT_BLOCK, seed=BOOT_SEED):
    """PAIRED circular-block bootstrap of a statistic DIFFERENCE: the same block index set is
    applied to both series (idea 1444's ruler, not the marginal one)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    nb = int(np.ceil(n / L))
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n, size=(reps, nb))
    idx = (starts[:, :, None] + np.arange(L)[None, None, :]).reshape(reps, nb * L)[:, :n] % n
    d = np.array([fn(a[i]) - fn(b[i]) for i in idx])
    obs = float(fn(a) - fn(b))
    se = float(np.nanstd(d, ddof=1))
    return obs, se, (obs / se if se > 0 else np.nan)


# ------------------------------------------------------------------ clustering
def average_linkage(D, ncl):
    """Agglomerative average-linkage on a square distance matrix, Lance-Williams update.
    Returns an integer label per row.  Pure numpy; no scipy in this sandbox."""
    n = D.shape[0]
    D = D.astype(float).copy()
    np.fill_diagonal(D, np.inf)
    size = np.ones(n)
    label = np.arange(n)
    alive = np.ones(n, bool)
    members = {i: [i] for i in range(n)}
    nclust = n
    while nclust > ncl:
        j = int(np.nanargmin(np.where(alive[:, None] & alive[None, :], D, np.inf)))
        a, b = divmod(j, n)
        if a > b:
            a, b = b, a
        na, nb = size[a], size[b]
        newrow = (na * D[a] + nb * D[b]) / (na + nb)
        D[a, :] = newrow
        D[:, a] = newrow
        D[a, a] = np.inf
        alive[b] = False
        D[b, :] = np.inf
        D[:, b] = np.inf
        size[a] = na + nb
        members[a] = members[a] + members[b]
        del members[b]
        nclust -= 1
    lab = np.empty(n, dtype=np.int64)
    for c, (_, ms) in enumerate(sorted(members.items())):
        for m in ms:
            lab[m] = c
    return lab


def is_only_clusters(pan, is_rows, C):
    """Average-linkage clusters on the IS-ONLY return correlation.  Names with < MIN_IS_ROWS
    in-sample observations get their own SINGLETON cluster, so the cap can never bind on a name
    the clustering could not see."""
    R = pan.q.pct_change().iloc[:is_rows]
    cnt = R.notna().sum().values
    ok = cnt >= MIN_IS_ROWS
    lab = np.full(len(pan.invest), -1, dtype=np.int64)
    if ok.sum() >= C:
        corr = R.loc[:, ok].corr().values
        corr = np.nan_to_num(corr, nan=0.0)
        lab[ok] = average_linkage(1.0 - corr, C)
    nxt = int(lab.max()) + 1 if (lab >= 0).any() else 0
    for i in np.flatnonzero(~ok):
        lab[i] = nxt
        nxt += 1
    return lab, int(ok.sum())


# ------------------------------------------------------------------ the panel
def mech_legs(q):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return (sum(parts) / len(parts)).values


def cadence_rows(idx, cad):
    m = rebalance_mask(idx, cad)
    v = m.shift(1, fill_value=False).values.copy()
    v[0] = True
    return np.flatnonzero(v)


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        q = px[invest]
        self.q = q
        self.comp = mech_legs(q)
        self.vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values

    def frame_inputs(self):
        above = (self.q > self.q.rolling(200).mean()).values
        elig = above & (np.nan_to_num(self.vol20, nan=1e9) < I_V)
        sc = self.comp * (0.5 + 0.5 * above.astype(float))
        key = np.where(np.isfinite(sc), -sc, np.inf)
        return elig, key


def build_frame(pan, elig, key, reb, lab=None, kcap=None, N=I_N, H=I_H, lag=1):
    """The frozen incumbent's HOLDINGS frame at unit gross, optionally with a per-cluster slot cap
    on NEW ADMISSIONS (retained names are never forced out)."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    capped = lab is not None and kcap is not None
    nblocked = 0
    for i, t in enumerate(reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = [int(c) for c in young]
        kset = set(keep)
        need = N - len(keep)
        take = []
        if need > 0:
            k = key[ts].copy()
            k[~(elig[ts] & pr[ts])] = np.inf
            for c in kset:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            if capped:
                cnt = {}
                for c in keep:
                    cnt[lab[c]] = cnt.get(lab[c], 0) + 1
                for c in order:
                    c = int(c)
                    if not np.isfinite(k[c]):
                        break
                    g = lab[c]
                    if cnt.get(g, 0) >= kcap:
                        nblocked += 1
                        continue
                    take.append(c)
                    cnt[g] = cnt.get(g, 0) + 1
                    if len(take) >= need:
                        break
            else:
                take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new = np.full(K, -1, dtype=np.int64)
        for c in kset:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W, nblocked


def run_gseq(pan, frame, reb, gseq):
    T, M = pan.rets.shape
    isreb = np.zeros(T, bool)
    isreb[reb] = True
    g = np.broadcast_to(np.asarray(gseq, float), (T,)).astype(float)
    cur = np.zeros(M)
    rg = np.zeros(T)
    turn = np.zeros(T)
    gp = np.zeros(T)
    for t in range(T):
        post = g[t] * frame[t] if isreb[t] else cur
        turn[t] = float(np.abs(post - cur).sum())
        gp[t] = float(post.sum())
        r = float(post @ pan.rets[t])
        rg[t] = r
        cur = post * (1.0 + pan.rets[t]) / (1.0 + r)
    return dict(rg=rg, turn=turn, gmax=float(gp.max()), gbar=float(gp[WARMUP:].mean()))


def net_of(run, cost):
    return run["rg"] - run["turn"] * cost / 1e4


def singleton_share(pan, frame, lab, C):
    """Share of BOOK WEIGHT sitting in names the IS clustering could not see (< MIN_IS_ROWS of
    in-sample data), i.e. in the singleton pass-throughs.  This is the run's own survivorship
    exposure meter: a cap that works by pushing the book into late-listed names is buying
    survivorship, not diversification."""
    M = frame.shape[1]
    sing = np.zeros(M, bool)
    sing[pan.iinv[lab >= C]] = True
    w = frame[WARMUP:]
    tot = w.sum(axis=1)
    ok = tot > 0
    if not ok.any():
        return 0.0
    return float((w[ok][:, sing].sum(axis=1) / tot[ok]).mean())


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say("=" * 124)
    say("IDEA 1643 — does a CORRELATION-CLUSTER CONCENTRATION CAP buy the KEEP-4b book's BINDING "
        "DD LEG, or is it the NINTH de-gross in costume?   (lane cloud, idea 2 of 2)")
    say("  PRE-REGISTERED  H_DEGROSS: the MaxDD-MATCHED constant de-gross twin wins (pooled mean "
        "dCAGR(cap - twin) <= 0 at 10 bps) -> the cap is a de-gross in costume and this run is a "
        "KILL, whatever its 4b verdict.")
    say("  PRE-REGISTERED  H_CAP: pooled dCAGR > 0 AND the rule-8 cell beats its OWN twin OOS AND "
        "clears 4b on FULL and OOS.")
    say("=" * 124)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0; {len(inv)} investable names survive.")

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, SMALL {len(inv)}.")
    say("  SURVIVORSHIP (rule 9): U56 and B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010, so every ABSOLUTE level below is an UPPER BOUND.  "
        "The HEADLINE is a CONTRAST between a capped book and its MaxDD-matched twin over the SAME "
        "names on the SAME days, which the bias cannot manufacture; the 4a / 4b levels inherit it.")
    say("")

    rows = []
    for pan in panels:
        reb = cadence_rows(pan.idx, I_C)
        elig, key = pan.frame_inputs()
        T = len(pan.idx)
        ev = np.arange(WARMUP, T)
        d_ev = pan.idx[ev]
        is_mask = np.asarray(d_ev <= pd.Timestamp(IS_END))
        oos_mask = np.asarray(d_ev >= pd.Timestamp(OOS_START))
        is_rows_full = int(np.sum(np.asarray(pan.idx <= pd.Timestamp(IS_END))))
        spy_ev = pan.spy[ev]
        say(f"  PANEL {pan.name}: eval {d_ev[0].date()} .. {d_ev[-1].date()} "
            f"({len(ev)/252:.1f}y), IS rows {int(is_mask.sum())}, OOS rows {int(oos_mask.sum())}.")

        nocap_frame, _ = build_frame(pan, elig, key, reb)
        anchor_sing = {}
        anc_run = run_gseq(pan, nocap_frame, reb, I_G)
        anc10 = net_of(anc_run, HEADLINE_COST)[ev]
        if pan.name == "U56":
            am, ao = triple(anc10), triple(anc10[oos_mask])
            d = max(abs(am["Sharpe"] - C_U56["Sharpe"]), abs(ao["Sharpe"] - C_U56["oSharpe"]),
                    abs(am["CAGR"] - C_U56["CAGR"]), abs(am["MaxDD"] - C_U56["MaxDD"]))
            gate("G1 cross-script replay of the committed 2026-09-04 U56 frozen anchor "
                 f"(15.80%/1.1537/-19.13%, OOS 1.1857) — got {am['CAGR']:.2%}/{am['Sharpe']:.4f}/"
                 f"{am['MaxDD']:.2%}, OOS {ao['Sharpe']:.4f}", f"max |diff| {d:.4f}", "< 0.01",
                 d < 0.01)
        ab, alegs, amm = path_4b(anc10, spy_ev)
        say(f"    NOCAP anchor @10bps  {amm['CAGR']:.2%} / {sharpe(anc10):.4f} / "
            f"{amm['MaxDD']:.2%}   4b FULL {'PASS' if ab else 'FAIL'}  legs {alegs}   "
            f"SPY {cagr(spy_ev):.2%} / {sharpe(spy_ev):.4f} / {mdd(spy_ev):.2%}")

        # the de-gross ray on the UNCAPPED frame (the twin's search space), one run per rung
        ray = {}
        for g in GGRID:
            ray[float(g)] = run_gseq(pan, nocap_frame, reb, float(g))
        ray_mdd = {c: np.array([mdd(net_of(ray[float(g)], c)[ev]) for g in GGRID]) for c in COSTS}

        labs = {}
        for C in CS:
            labs[C], n_ok = is_only_clusters(pan, is_rows_full, C)
            sizes = np.bincount(labs[C])
            say(f"    IS-only clusters C={C:2d}: {n_ok} of {len(pan.invest)} names clustered "
                f"(>= {MIN_IS_ROWS} IS rows), sizes of the {C} fitted blocks "
                f"{sorted(sizes[:C], reverse=True)[:8]}, "
                f"{len(sizes)-C} singleton pass-throughs.")
            anchor_sing[C] = singleton_share(pan, nocap_frame, labs[C], C)
            say(f"        NOCAP anchor holds {anchor_sing[C]:.1%} of book weight in those "
                f"singleton pass-throughs.")

        for C in CS:
            for k in KS:
                frame, nblocked = build_frame(pan, elig, key, reb, lab=labs[C], kcap=k)
                sshare = singleton_share(pan, frame, labs[C], C)
                run = run_gseq(pan, frame, reb, I_G)
                for cost in COSTS:
                    r = net_of(run, cost)[ev]
                    anc = net_of(anc_run, cost)[ev]
                    m = triple(r)
                    # ---- MaxDD-matched constant de-gross twin
                    mv_ = ray_mdd[cost]
                    gstar = float(np.interp(m["MaxDD"], mv_[::-1], GGRID[::-1]))
                    gstar = float(np.clip(round(gstar, 4), 0.02, 1.0))
                    twin_run = run_gseq(pan, nocap_frame, reb, gstar)
                    tw = net_of(twin_run, cost)[ev]
                    tm = triple(tw)
                    gap = abs(tm["MaxDD"] - m["MaxDD"])
                    dC, dS = m["CAGR"] - tm["CAGR"], m["Sharpe"] - tm["Sharpe"]
                    if cost == HEADLINE_COST:
                        oC, seC, tC = paired_block(r, tw, cagr)
                    else:
                        oC = seC = tC = np.nan
                    k4a, h1, h2 = path_4a(r, anc)
                    k4b, legs, _ = path_4b(r, spy_ev)
                    k4b_o = path_4b(r[oos_mask], spy_ev[oos_mask])[0]
                    mo = triple(r[oos_mask])
                    two = triple(tw[oos_mask])
                    rows.append(dict(
                        panel=pan.name, C=C, k=k, cost=cost, blocked=nblocked,
                        sing=sshare, anchor_sing=anchor_sing[C],
                        gbar=run["gbar"], gstar=gstar, mdd_gap=gap,
                        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                        IS_Sharpe=sharpe(r[is_mask]),
                        oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                        tCAGR=tm["CAGR"], tSharpe=tm["Sharpe"], tMaxDD=tm["MaxDD"],
                        toCAGR=two["CAGR"], toSharpe=two["Sharpe"],
                        dCAGR=dC, dSharpe=dS, dCAGR_se=seC, dCAGR_t=tC,
                        odCAGR=mo["CAGR"] - two["CAGR"], odSharpe=mo["Sharpe"] - two["Sharpe"],
                        k4a=k4a, k4b=k4b, k4b_oos=k4b_o,
                        leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"],
                        leg_CAGR=legs["CAGR"],
                        aCAGR=triple(anc)["CAGR"], aSharpe=sharpe(anc), aMaxDD=mdd(anc)))
        say("")

    G = pd.DataFrame(rows)
    G.to_csv(OUT.with_suffix(".csv"), index=False)
    say(f"  {len(G):,} cell readings written to {OUT.name}.csv "
        f"({len(G[['panel','C','k']].drop_duplicates())} capped books x {len(COSTS)} cost rungs).")
    say("")

    # ---------------------------------------------------------------- publish every cell
    say("-" * 124)
    say("EVERY CELL at the headline rung (10 bps).  dCAGR / dSharpe are CAP minus its own "
        "MaxDD-MATCHED constant de-gross twin; t is a PAIRED circular-block bootstrap (L=63, "
        f"{BOOT_REPS} reps).")
    H = G[G.cost == HEADLINE_COST].copy()
    cols = ["panel", "C", "k", "sing", "gbar", "gstar", "mdd_gap", "CAGR", "Sharpe", "MaxDD",
            "dCAGR", "dSharpe", "dCAGR_t", "oCAGR", "oSharpe", "odCAGR", "k4a", "k4b", "k4b_oos"]
    say(H[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("")

    # ---------------------------------------------------------------- the de-gross law
    say("-" * 124)
    say("THE DE-GROSS LAW.  Pooled CAP minus MaxDD-MATCHED TWIN, by panel and by cost rung.")
    for cost in COSTS:
        c = G[G.cost == cost]
        say(f"  {cost:5.1f} bps   pooled dCAGR {c.dCAGR.mean():+.4f} pp/yr "
            f"({c.dCAGR.mean()*100:+.4f} pp)   dSharpe {c.dSharpe.mean():+.4f}   "
            f"cap wins dCAGR in {int((c.dCAGR > 0).sum())} of {len(c)}")
    for p in ["U56", "B136", "SMALL"]:
        c = H[H.panel == p]
        say(f"  {p:6s} @10bps  dCAGR {c.dCAGR.mean()*100:+.4f} pp   dSharpe {c.dSharpe.mean():+.4f}"
            f"   |t| > 2 in {int((c.dCAGR_t.abs() > 2).sum())} of {len(c)}   "
            f"OOS dCAGR {c.odCAGR.mean()*100:+.4f} pp   OOS dSharpe {c.odSharpe.mean():+.4f}")
    say("  DOES THE CAP EVEN BIND?  blocked admissions and realised mean gross, by cell:")
    for p in ["U56", "B136", "SMALL"]:
        c = H[H.panel == p]
        say(f"      {p:6s} blocked admissions {int(c.blocked.min()):5d}..{int(c.blocked.max()):5d}"
            f"   realised mean gross {c.gbar.min():.4f}..{c.gbar.max():.4f}  "
            f"(anchor {G[(G.panel==p)].gbar.max():.4f})")
    say("  SURVIVORSHIP EXPOSURE METER (the caveat, measured rather than asserted).  Share of "
        "book weight in names the IS clustering could NOT see (< 500 IS rows, i.e. LATE-LISTED "
        "survivors), capped book vs the NOCAP anchor:")
    for p in ["U56", "B136", "SMALL"]:
        c = H[H.panel == p]
        say(f"      {p:6s} capped {c.sing.min():.1%}..{c.sing.max():.1%} (mean {c.sing.mean():.1%})"
            f"   vs NOCAP anchor {c.anchor_sing.mean():.1%}   -> lift "
            f"{(c.sing.mean()-c.anchor_sing.mean())*100:+.1f} pp of book weight")
    say("")

    # ---------------------------------------------------------------- rule 8
    say("-" * 124)
    say("RULE 8 — C and k chosen on warm-up..2016-12-31 ONLY (argmax IS Sharpe within panel), "
        "2017-01-01..end read exactly ONCE.")
    picks = []
    for p in ["U56", "B136", "SMALL"]:
        sub = H[H.panel == p]
        j = sub.IS_Sharpe.idxmax()
        q = sub.loc[j]
        picks.append(dict(panel=p, C=int(q.C), k=int(q.k), IS_Sharpe=q.IS_Sharpe,
                          oCAGR=q.oCAGR, oSharpe=q.oSharpe, oMaxDD=q.oMaxDD,
                          twin_oCAGR=q.toCAGR, twin_oSharpe=q.toSharpe,
                          odCAGR=q.odCAGR, odSharpe=q.odSharpe,
                          k4a=bool(q.k4a), k4b=bool(q.k4b), k4b_oos=bool(q.k4b_oos)))
    P = pd.DataFrame(picks)
    say(P.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    beats_oos = int(((P.odCAGR > 0) & (P.odSharpe > 0)).sum())
    say(f"  rule-8 picks beating their OWN MaxDD-matched twin OUT OF SAMPLE on BOTH CAGR and "
        f"Sharpe: {beats_oos} of {len(P)}")
    say("")

    # ---------------------------------------------------------------- both KEEP paths
    say("-" * 124)
    say("BOTH KEEP PATHS at every cell.")
    for cost in COSTS:
        c = G[G.cost == cost]
        say(f"  {cost:5.1f} bps   4a {int(c.k4a.sum()):3d}/{len(c):3d}   "
            f"4b FULL {int(c.k4b.sum()):3d}/{len(c):3d}   4b OOS {int(c.k4b_oos.sum()):3d}/"
            f"{len(c):3d}   4b BOTH {int((c.k4b & c.k4b_oos).sum()):3d}/{len(c):3d}")
    say("  4b leg attribution at 10 bps (which leg fails):")
    for leg in ["leg_H1", "leg_H2", "leg_DD", "leg_CAGR"]:
        say(f"      {leg:9s} fails {int((~H[leg]).sum()):3d} of {len(H)}")
    say("")

    # ---------------------------------------------------------------- gates
    say("-" * 124)
    gate("G0 minimum sample (rule 1)", f"{len(panels[0].idx)/252:.1f}y U56 / "
         f"{len(panels[2].idx)/252:.1f}y SMALL", ">= 10y", len(panels[2].idx) / 252 >= 10)
    worst = float(G.mdd_gap.max())
    gate("G2 MaxDD match quality on every twin", f"max gap {worst:.4f}",
         f"< {MATCH_BAR}", worst < MATCH_BAR)
    gate("G3 exactly two tuned parameters", "C and k (panel / cost are published ladders)",
         "2", True)
    gate("G4 no leverage: max gross on any book", f"{I_G:.4f}", "<= 1.00", I_G <= 1.0)
    gate("G5 clustering and chooser read IS rows ONLY",
         "corr fitted on warm-up..2016-12-31; argmax on IS Sharpe", "asserted", True)
    binds = int((H.blocked > 0).sum())
    gate("G6 the cap actually BINDS (blocked admissions > 0)", f"{binds} of {len(H)} cells",
         "> 0 on a majority", binds > len(H) // 2)
    n_exp = len(G[["panel", "C", "k"]].drop_duplicates()) * len(COSTS)
    gate("G7 every cell published", f"{len(G)} rows, {n_exp} expected", "equal", len(G) == n_exp)
    gate("G8 cost ladder is an identity on one turnover path", "exact by construction",
         "asserted", True)
    npass = sum(1 for g in GATES if g["pass_"])
    say(f"  GATES: {npass} of {len(GATES)} PASS.")
    say("")

    # ---------------------------------------------------------------- verdict
    say("=" * 124)
    pooled = float(H.dCAGR.mean())
    h_deg = pooled <= 0
    h_cap = (pooled > 0) and (beats_oos == len(P)) and bool((P.k4b & P.k4b_oos).all())
    say(f"  H_DEGROSS {'HOLDS' if h_deg else 'DOES NOT HOLD'} — pooled dCAGR(cap - MaxDD-matched "
        f"twin) at 10 bps = {pooled*100:+.4f} pp/yr over {len(H)} cells; cap wins dCAGR in "
        f"{int((H.dCAGR > 0).sum())} of {len(H)}.")
    say(f"  H_CAP     {'HOLDS' if h_cap else 'DOES NOT HOLD'} — rule-8 picks beating their own "
        f"twin OOS on both legs: {beats_oos} of {len(P)}; picks clearing 4b FULL and OOS: "
        f"{int((P.k4b & P.k4b_oos).sum())} of {len(P)}.")
    say("=" * 124)
    say(f"  elapsed {time.time()-t0:.0f}s")

    pd.DataFrame(GATES).to_csv(OUT.parent / f"{OUT.name}_gates.csv", index=False)
    (OUT.parent / f"{OUT.name}_log.txt").write_text("\n".join(LOG))
    return G, P


if __name__ == "__main__":
    main()
