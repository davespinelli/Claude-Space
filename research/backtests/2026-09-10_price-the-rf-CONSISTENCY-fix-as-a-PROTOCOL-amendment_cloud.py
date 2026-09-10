#!/usr/bin/env python3
"""Idea 641 — price the rf-CONSISTENCY fix as a PROTOCOL amendment (cloud, 2026-09-10).

Idea 406 established (a) the record prices every de-grossed book with cash at ZERO, (b) the
queue's literal fix (credit cash at c, leave rf=0) flips 2.83%/5.04% of 26,207 committed 4b
verdicts fail->pass, and (c) the fix REVERSES itself once rf is made consistent (rf=c), because
crediting a risk-free return and then measuring it as excess return counts rf as alpha.

This run does the three things idea 641 asks for:

  PART A  write the three-line amendment (credit rate, rf, both inside engine.metrics);
  PART B  re-price the record's committed KEEP-candidates -- the MEMO corpus, i.e. every
          KEEP-candidate the record filed a memo for and that is reconstructible from price
          data alone -- EXACTLY (re-simulated, not first-order) under all five treatments;
  PART C  the RECORD corpus: a first-order census over every committed CSV that publishes
          (Sharpe, CAGR, MaxDD, gross) in one row, so the amendment can be priced record-wide;
  PART D  rule 8 (PROTOCOL 8) walk-forward on the three dial families the corpus lives in,
          the dial chosen on the FIRST half (<= 2016-12-31) under each treatment and the
          second half read exactly once.

TWO TUNED PARAMETERS, as the queue allows: the credit RATE (0 / 150 / 300 bps) and the CORPUS
(MEMO / RECORD).  Every grid point is reported.

TREATMENTS (these are the object under test, not tuned dials):
  C0   cash 0,   rf 0    -- the record's standing convention, what every published verdict used
  C1   cash c,   rf 0    -- the queue's literal ask (idea 641's "credit rate" line alone)
  C2   cash c,   rf c    -- the internally consistent amendment (both lines)

Costs 10 bps headline (25 bps reported), next-day execution, no shorting, no leverage.
Panels: U56 (research/universe.json) and B136 (research/universe_broad.json).  SURVIVORSHIP:
both are current-constituent lists, so every level here is optimistic; only the DIFFERENCES
between treatments are the object of this run.

Outputs (all committed):
  .txt         full console log
  .corpus.csv  PART B, one row per (book, rung, treatment): full 4b margin vector + verdicts
  .census.csv  PART C, per-file record-wide census
  .wf.csv      PART D, every rule-8 grid point
  .result.md   the answer, incl. the drafted amendment
Nothing outside research/ is written; RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py
are NOT modified by this script.
"""
from __future__ import annotations
import glob, gzip, os, sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score, band_state  # noqa
from engine import backtest, metrics, rebalance_mask                                        # noqa

DATE = "2026-09-10"
SLUG = "price-the-rf-CONSISTENCY-fix-as-a-PROTOCOL-amendment"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

END = "2026-09-04"          # the record's committed vintage; data/prices.csv now runs past it
OOS_START = "2017-01-01"    # PROTOCOL rule 8
IS_END = "2016-12-31"
RATES = [0.0, 150.0, 300.0]         # tuned parameter 1
CORPORA = ["MEMO", "RECORD"]        # tuned parameter 2
RUNGS = [10, 25]
RUNG_HEAD = 10
MAX_VOL = 0.60
LOG = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# =====================================================================================
# the engine: idea 406's run_cash verbatim (cash credited INSIDE the drift renormalisation)
# =====================================================================================
def run_cash(px, W, credit_bps=0.0, freq="W"):
    """Hold W, drifting between rebalances, paying credit_bps/yr on POSITIVE cash.

    credit_bps = 0 reproduces engine.backtest exactly (gate G1).  Returns are cost-free plus
    a turnover series so every cost rung comes off one simulation.
    """
    rets = px.pct_change().fillna(0.0).values
    tgt = W.reindex(px.index).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    crd = credit_bps / 1e4 / 252.0
    nrow, ncol = rets.shape
    cur = np.zeros(ncol)
    r = np.zeros(nrow); turn = np.zeros(nrow); cash_s = np.zeros(nrow)
    for i in range(nrow):
        if mask[i] and i > 0:
            new = tgt[i - 1]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        cash = 1.0 - cur.sum()
        pay = cash * crd if cash > 0.0 else 0.0
        cash_s[i] = max(cash, 0.0)
        growth = cur * (1 + rets[i])
        r[i] = growth.sum() - cur.sum() + pay
        tot = growth.sum() + cash + pay
        cur = growth / tot if tot > 0 else cur
    idx = px.index
    return dict(r=pd.Series(r, index=idx), to=pd.Series(turn, index=idx),
                cash=pd.Series(cash_s, index=idx))


def net(sim, bps, start):
    return (sim["r"] - sim["to"] * bps / 1e4).loc[start:]


def pack(r, rf_annual):
    """CAGR / Sharpe(rf) / MaxDD / vol / half Sharpes / OOS Sharpe, all under one rf."""
    m = metrics(r, rf=rf_annual)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], Vol=m["Vol"],
                H1=metrics(r.iloc[:h], rf=rf_annual)["Sharpe"],
                H2=metrics(r.iloc[h:], rf=rf_annual)["Sharpe"],
                OOS=metrics(r.loc[OOS_START:], rf=rf_annual)["Sharpe"],
                OOS_CAGR=metrics(r.loc[OOS_START:])["CAGR"],
                OOS_MaxDD=metrics(r.loc[OOS_START:])["MaxDD"])


# =====================================================================================
# the books:  every committed KEEP-candidate memo that is reconstructible from prices alone
# =====================================================================================
def comp_rank(px):
    """The record's composite score WITHOUT the vol scaler, and its eligibility mask."""
    s, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < MAX_VOL)
    return s.where(elig), elig


def topn_weights(px, n=20, gross=0.75, m=0, fixed=False):
    """Top-n composite, optional no-trade rank buffer m (a held name is sold only when it
    leaves the eligible set or its rank passes n+m).  fixed=False weights gross/k (memo
    2026-09-07 wording); fixed=True weights gross/n per name, so a short day de-grosses
    (memo 2026-09-06 wording, "20 names at 3.75% of NAV each")."""
    sc, elig = comp_rank(px)
    rank = sc.rank(axis=1, ascending=False)
    if m == 0:
        sel = (rank <= n).fillna(False)
    else:
        R = rank.values; E = elig.values
        held = np.zeros(px.shape[1], bool)
        out = np.zeros(px.shape, bool)
        for i in range(len(px)):
            r_i, e_i = R[i], E[i]
            ok = ~np.isnan(r_i)
            keep = held & e_i & ok & (r_i <= n + m)
            need = n - int(keep.sum())
            if need > 0:
                cand = np.where(e_i & ok & ~keep)[0]
                if len(cand):
                    cand = cand[np.argsort(r_i[cand])][:need]
                    keep[cand] = True
            held = keep
            out[i] = keep
        sel = pd.DataFrame(out, index=px.index, columns=px.columns)
    if fixed:
        return sel.astype(float).mul(gross / n)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.astype(float).div(k, axis=0).mul(gross).fillna(0.0)


def band_ew_respread(px, band, gross):
    """Idea 360's wording: hold every IN name at gross/k_t, k_t = number of IN names that day
    (RESPREAD over the in-band set), not gross/N de-grossed as RULES v2 does."""
    e = band_state(px, band).astype(float).where(px.notna(), 0.0)
    k = e.sum(axis=1).replace(0, np.nan)
    return e.div(k, axis=0).mul(gross).fillna(0.0)


def magate_weights(px, gross=1.00):
    """Every name above its 200d MA, equal weight at `gross`; the rest CASH. No vol filter."""
    above = (px > px.rolling(200).mean()).fillna(False)
    e = above.astype(float).where(px.notna(), 0.0)
    k = e.sum(axis=1).replace(0, np.nan)
    return e.div(k, axis=0).mul(gross).fillna(0.0)


def ewall_weights(px, gross=1.00):
    """Scored-eligible (above 200d MA AND vol20 < 0.60) equal weight at `gross`."""
    _, elig = comp_rank(px)
    e = elig.astype(float).where(px.notna(), 0.0)
    k = e.sum(axis=1).replace(0, np.nan)
    return e.div(k, axis=0).mul(gross).fillna(0.0)


def shy_residual_weights(px, gross=0.375, sleeve="SHY"):
    """ewall at `gross`, the un-invested residual parked in SHY instead of cash (idea 383)."""
    W = ewall_weights(px.drop(columns=[sleeve]), gross).reindex(columns=px.columns).fillna(0.0)
    W[sleeve] = (1.0 - W.sum(axis=1)).clip(lower=0.0)
    return W


def breadth_gate_weights(px, gross=1.00, q=0.17, wroll=1008, depth=1.0, freq="W"):
    """ewall at `gross`, de-grossed by `depth` while panel 200d-MA breadth sits below its own
    trailing `wroll`-day q-quantile (idea 604's QROLL arm, the record's newest 4b candidate)."""
    core = px.drop(columns=["SPY"], errors="ignore")
    above = core > core.rolling(200).mean()
    breadth = above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)
    thr = breadth.rolling(wroll, min_periods=wroll).quantile(q)
    bad = (breadth < thr) & breadth.notna() & thr.notna()
    m = pd.Series(1.0, index=px.index).where(~bad, 1.0 - depth)
    mask = rebalance_mask(px.index, freq)
    m = m.where(mask).ffill().fillna(1.0)
    return ewall_weights(px, gross).mul(m, axis=0)


# (key, label, panel, weights fn, cadence, memo file, published (CAGR, Sharpe, MaxDD))
def build_corpus():
    return [
        ("K1", "u56 top20 composite g0.75 W (memo 2026-09-07_u56-top20-g075-4b_C)",
         "U56", lambda px: topn_weights(px, 20, 0.75, 0), "W", (0.1279, 1.064, -0.1831)),
        ("K2", "u56 top20 composite g0.75 W + rank buffer m=20 (memo 2026-09-07_u56-top20-band-m20)",
         "U56", lambda px: topn_weights(px, 20, 0.75, 20), "W", (None, None, None)),
        ("K3", "u56 top20-200d DAILY + rank buffer m=50 (memo 2026-09-06 KEEP)",
         "U56", lambda px: topn_weights(px, 20, 0.75, 50, fixed=True), "D", (0.1171, 1.1454, -0.1237)),
        ("K4", "u56 EW-all 200d-MA gate (band 0), gross 1.00, MONTHLY (memo 2026-09-08 KEEP)",
         "U56", lambda px: rules_v2_weights(px, 0.0, 1.00), "M", (0.1196, 1.2126, -0.1549)),
        ("K5", "u56 RULES v2 gate at gross 1.00, weekly (memo 2026-09-08 / 2026-09-10)",
         "U56", lambda px: rules_v2_weights(px, 0.03, 1.00), "W", (0.1159, 1.2055, -0.1591)),
        ("K6", "u56 wide-band b=0.12 EW g0.75 weekly (memo 2026-09-07 idea 360 KEEP)",
         "U56", lambda px: band_ew_respread(px, 0.12, 0.75), "W", (0.1402, 1.2264, -0.1942)),
        ("K7", "b136 scored-eligible EW g=0.375, residual in SHY (memo 2026-09-07, path 4a)",
         "B136", lambda px: shy_residual_weights(px, 0.375), "W", (0.0627, 1.1777, -0.1110)),
        ("K8", "u56 EW-all g1.00 weekly, de-gross to ZERO on breadth < trailing-1008d q0.17 "
               "(2026-09-10 leaderboard KEEP-candidate)",
         "U56", lambda px: breadth_gate_weights(px, 1.00, 0.17), "W", (0.1413, 1.2204, -0.1479)),
        ("LIVE", "RULES v2 (the live book, band 3%, gross 0.75, weekly)",
         "U56", lambda px: rules_v2_weights(px, 0.03, 0.75), "W", (None, None, None)),
        ("V1", "RULES v1 (the previous live book)",
         "U56", lambda px: rules_v1_weights(px), "W", (None, None, None)),
    ]


# =====================================================================================
# gates
# =====================================================================================
def gates(pxU, pxB, start_u):
    log("\n" + "=" * 110)
    log("GATES (five, pre-registered, run before any result is read)")
    log("=" * 110)
    res = {}

    # G1: run_cash(c=0) == engine.backtest
    W = rules_v2_weights(pxU, 0.03, 0.75)
    a = run_cash(pxU, W, 0.0, "W")
    b = backtest(pxU, W, cost_bps=0, freq="W")
    fin = b["returns"].notna().values & b["turnover"].notna().values   # engine's own shift-NaN
    d1 = float(np.abs(a["r"].values[fin] - b["returns"].values[fin]).max())
    d1t = float(np.abs(a["to"].values[fin] - b["turnover"].values[fin]).max())
    log(f"      ({int((~fin).sum())} rows excluded: engine.backtest's own w_target.shift(1) NaN "
        f"at the head of the sample, present in the record's every run)")
    res["G1"] = d1 < 1e-12 and d1t < 1e-12
    log(f"  G1  run_cash(c=0) vs engine.backtest, RULES v2 U56: returns {d1:.3e}, "
        f"turnover {d1t:.3e}  (bar 1e-12)  {'PASS' if res['G1'] else 'FAIL'}")

    # G2: RULES v2's own committed headline @10 bps
    m = metrics(net(a, 10, start_u))
    ok = abs(m["Sharpe"] - 1.202) < 6e-3 and abs(m["CAGR"] - 0.0863) < 6e-3 and abs(m["MaxDD"] + 0.1205) < 6e-3
    res["G2"] = ok
    log(f"  G2  RULES v2 U56 @10bps {m['CAGR']:.2%}/{m['Sharpe']:.4f}/{m['MaxDD']:.2%} "
        f"vs committed 8.63%/1.202/-12.05% (bar 6e-3; data/prices.csv is re-downloaded daily with auto-adjusted closes, so u56 rows in this record reproduce to ~3e-3, NOT bit-exact -- idea 406's finding)  {'PASS' if ok else 'FAIL'}")

    # G3: every memo book reproduces its published headline
    log("  G3  memo-headline reproduction (bar |dSharpe| <= 0.02; a miss EXCLUDES the book):")
    keep = []
    for key, label, panel, fn, freq, pub in build_corpus():
        px = pxU if panel == "U56" else pxB
        st = px.index[260]
        sim = run_cash(px, fn(px), 0.0, freq)
        mm = metrics(net(sim, 10, st))
        if pub[1] is None:
            log(f"      {key:<5} {mm['CAGR']:>7.2%} / {mm['Sharpe']:>7.4f} / {mm['MaxDD']:>7.2%}"
                f"   (no published headline to gate against -- carried)")
            keep.append(key); continue
        ds = mm["Sharpe"] - pub[1]; dc = mm["CAGR"] - pub[0]; dd = mm["MaxDD"] - pub[2]
        good = abs(ds) <= 0.02
        log(f"      {key:<5} {mm['CAGR']:>7.2%} / {mm['Sharpe']:>7.4f} / {mm['MaxDD']:>7.2%}"
            f"   published {pub[0]:>7.2%} / {pub[1]:>7.4f} / {pub[2]:>7.2%}"
            f"   d {dc:+.4f} / {ds:+.4f} / {dd:+.4f}   {'ok' if good else 'EXCLUDED'}")
        if good: keep.append(key)
    res["G3"] = len(keep)
    res["G3_keep"] = keep

    # G4: the vol-recovery identity used by PART C's record-wide census
    errs = []
    for key, label, panel, fn, freq, pub in build_corpus():
        px = pxU if panel == "U56" else pxB
        st = px.index[260]
        r = net(run_cash(px, fn(px), 0.0, freq), 10, st)
        mm = metrics(r)
        S, C, V = mm["Sharpe"], mm["CAGR"], mm["Vol"]
        disc = S * S - 2 * C
        vhat = S - np.sqrt(disc) if disc > 0 else np.nan
        errs.append(abs(vhat - V))
    res["G4"] = float(np.nanmax(errs))
    log(f"  G4  vol recovered from (Sharpe, CAGR) vs true vol on the corpus: "
        f"max |err| {res['G4']:.4f}, median {np.nanmedian(errs):.4f}  "
        f"(a TOLERANCE, not an assert; PART C's census is first-order and says so)")

    # G5: the first-order credit (1-gbar)*c against the exact re-simulation
    rows = []
    for key, label, panel, fn, freq, pub in build_corpus():
        px = pxU if panel == "U56" else pxB
        st = px.index[260]
        W = fn(px)
        s0 = run_cash(px, W, 0.0, freq); s3 = run_cash(px, W, 300.0, freq)
        cbar = float(s0["cash"].loc[st:].mean())
        exact = metrics(net(s3, 10, st))["CAGR"] - metrics(net(s0, 10, st))["CAGR"]
        first = cbar * 300.0 / 1e4
        rows.append((key, cbar, first, exact, exact - first))
    res["G5"] = max(abs(x[4]) for x in rows)
    log(f"  G5  first-order credit (1-gbar)*c vs exact re-simulation at 300 bps:")
    for k, cb, f1, ex, d in rows:
        log(f"      {k:<5} mean cash {cb:>6.3f}   first-order {f1*1e4:>6.1f} bps   "
            f"exact {ex*1e4:>6.1f} bps   understatement {d*1e4:>+5.1f} bps")
    log(f"      -> the first-order form understates the credit by at most {res['G5']*1e4:.1f} bps "
        f"of CAGR (compounding); PART C is therefore CONSERVATIVE on the C1 direction.")
    return res


# =====================================================================================
# PART B -- the MEMO corpus, exact re-pricing under all five treatments
# =====================================================================================
def part_b(pxU, pxB, keep_keys):
    log("\n" + "=" * 110)
    log("PART B -- the MEMO corpus: every committed KEEP-candidate the record filed a memo for,")
    log("          re-simulated (not first-order) under C0 / C1@150 / C1@300 / C2@150 / C2@300")
    log("=" * 110)

    panels = {"U56": pxU, "B136": pxB}
    spy_sims, v2_sims, starts = {}, {}, {}
    for pn, px in panels.items():
        st = px.index[260]; starts[pn] = st
        Wspy = pd.DataFrame(0.0, index=px.index, columns=px.columns); Wspy["SPY"] = 1.0
        spy_sims[pn] = {c: run_cash(px, Wspy, c, "W") for c in RATES}
        Wv2 = rules_v2_weights(px, 0.03, 0.75)
        v2_sims[pn] = {c: run_cash(px, Wv2, c, "W") for c in RATES}
        log(f"  panel {pn}: {px.shape[1]} cols, {px.index[0].date()} -> {px.index[-1].date()}, "
            f"eval from {st.date()} ({len(px.loc[st:])} days)")

    rows = []
    for key, label, panel, fn, freq, pub in build_corpus():
        if key not in keep_keys:
            log(f"  {key} EXCLUDED by gate G3 -- not re-priced.")
            continue
        px = panels[panel]; st = starts[panel]
        W = fn(px)
        sims = {c: run_cash(px, W, c, freq) for c in RATES}
        cbar = float(sims[0.0]["cash"].loc[st:].mean())
        for rung in RUNGS:
            for tname, c, rf in (("C0", 0.0, 0.0), ("C1@150", 150.0, 0.0), ("C1@300", 300.0, 0.0),
                                 ("C2@150", 150.0, 150.0), ("C2@300", 300.0, 300.0)):
                rfa = rf / 1e4
                p = pack(net(sims[c], rung, st), rfa)
                s = pack(net(spy_sims[panel][c], rung, st), rfa)
                v = pack(net(v2_sims[panel][c], rung, st), rfa)
                mH1 = p["H1"] - s["H1"]; mH2 = p["H2"] - s["H2"]; mOOS = p["OOS"] - s["OOS"]
                mDD = 0.60 * abs(s["MaxDD"]) - abs(p["MaxDD"])
                mCAGR = p["CAGR"] - 0.70 * s["CAGR"]
                v4b = min(mH1, mH2, mOOS, mDD, mCAGR) > 0
                v4a = (p["H1"] > v["H1"]) and (p["H2"] > v["H2"]) and (p["MaxDD"] >= v["MaxDD"])
                bind = ["H1", "H2", "OOS", "DD", "CAGR"][int(np.argmin([mH1, mH2, mOOS, mDD, mCAGR]))]
                rows.append(dict(book=key, label=label, panel=panel, cadence=freq, rung=rung,
                                 treatment=tname, credit_bps=c, rf_bps=rf, mean_cash=cbar,
                                 CAGR=p["CAGR"], Sharpe=p["Sharpe"], MaxDD=p["MaxDD"], Vol=p["Vol"],
                                 H1=p["H1"], H2=p["H2"], OOS=p["OOS"],
                                 m_H1=mH1, m_H2=mH2, m_OOS=mOOS, m_DD=mDD, m_CAGR=mCAGR,
                                 m_min=min(mH1, mH2, mOOS, mDD, mCAGR), bind=bind,
                                 pass4b=v4b, pass4a=v4a,
                                 spy_H1=s["H1"], spy_H2=s["H2"], spy_OOS=s["OOS"],
                                 spy_CAGR=s["CAGR"], spy_MaxDD=s["MaxDD"],
                                 v2_H1=v["H1"], v2_H2=v["H2"], v2_MaxDD=v["MaxDD"]))
    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}.corpus.csv", index=False)

    for rung in RUNGS:
        log(f"\n  --- cost rung {rung} bps " + "-" * 88)
        log(f"  {'book':<5} {'cash':>5} {'treat':<7} {'CAGR':>7} {'Shrp':>7} {'MaxDD':>7} "
            f"{'m_H1':>7} {'m_H2':>7} {'m_OOS':>7} {'m_DD':>7} {'m_CAGR':>7} {'bind':>5} {'4b':>3} {'4a':>3}")
        for key, label, panel, fn, freq, pub in build_corpus():
            sub = df[(df.book == key) & (df.rung == rung)]
            if sub.empty: continue
            for _, r in sub.iterrows():
                log(f"  {r.book:<5} {r.mean_cash:>5.3f} {r.treatment:<7} {r.CAGR:>7.2%} "
                    f"{r.Sharpe:>7.4f} {r.MaxDD:>7.2%} {r.m_H1:>+7.4f} {r.m_H2:>+7.4f} "
                    f"{r.m_OOS:>+7.4f} {r.m_DD:>+7.4f} {r.m_CAGR:>+7.4f} {r.bind:>5} "
                    f"{'Y' if r.pass4b else '.':>3} {'Y' if r.pass4a else '.':>3}")
            log("")

    # the verdict-transfer table: does the PUBLISHED (C0) verdict survive each treatment?
    log("\n  VERDICT TRANSFER -- does the published (C0) verdict survive the amendment?")
    log(f"  {'book':<5} {'rung':>4} " + " ".join(f"{t:>8}" for t in
        ("C0", "C1@150", "C1@300", "C2@150", "C2@300")) + "   4b carries?   4a carries?")
    safe4b, safe4a, n4b, n4a = [], [], 0, 0
    for key, label, panel, fn, freq, pub in build_corpus():
        for rung in RUNGS:
            sub = df[(df.book == key) & (df.rung == rung)].set_index("treatment")
            if sub.empty: continue
            v4b = {t: bool(sub.loc[t, "pass4b"]) for t in sub.index}
            v4a = {t: bool(sub.loc[t, "pass4a"]) for t in sub.index}
            c4b = all(v4b[t] == v4b["C0"] for t in v4b)
            c4a = all(v4a[t] == v4a["C0"] for t in v4a)
            n4b += 1; n4a += 1
            if c4b: safe4b.append((key, rung))
            if c4a: safe4a.append((key, rung))
            log(f"  {key:<5} {rung:>4} " + " ".join(
                f"{('4b' if v4b[t] else '--') + '/' + ('4a' if v4a[t] else '--'):>8}"
                for t in ("C0", "C1@150", "C1@300", "C2@150", "C2@300")) +
                f"   {'YES' if c4b else 'NO ':>10}   {'YES' if c4a else 'NO ':>10}")
    log(f"\n  -> 4b verdict identical under all five treatments in {len(safe4b)} of {n4b} "
        f"(book x rung) cells; 4a in {len(safe4a)} of {n4a}.")
    return df, safe4b, safe4a


# =====================================================================================
# PART C -- the RECORD corpus, first-order census over every committed CSV
# =====================================================================================
def _num(s):
    return pd.to_numeric(s, errors="coerce")


def part_c(spy_ref):
    log("\n" + "=" * 110)
    log("PART C -- the RECORD corpus: every committed research/backtests CSV that publishes")
    log("          (Sharpe, CAGR, MaxDD, gross) in ONE row, re-priced FIRST-ORDER under C1/C2")
    log("=" * 110)
    log("  METHOD.  For a row publishing (S, CAGR, MaxDD, gross g):")
    log("    dCAGR    = (1-g)*c                       (both C1 and C2; conservative, gate G5)")
    log("    vol_hat  = S - sqrt(S^2 - 2*CAGR)        (Sharpe/CAGR identity, gate G4)")
    log("    dS(C1)   = +(1-g)*c / vol_hat            (the queue's literal fix: cash paid, rf=0)")
    log("    dS(C2)   = -g*c     / vol_hat            (the consistent fix: cash paid AND rf=c)")
    log("  dS(C1) > 0 for every de-grossed row and dS(C2) < 0 for every row with ANY exposure:")
    log("  the two lines of the amendment push the record's Sharpe column in OPPOSITE directions.")

    files = sorted(glob.glob(str(OUT.parent / "*.csv")) + glob.glob(str(OUT.parent / "*.csv.gz")))
    rows, per_file = [], []
    t0 = time.time()
    for f in files:
        base = os.path.basename(f)
        if base.startswith(f"{DATE}_{SLUG}"):
            continue
        try:
            if os.path.getsize(f) > 60e6:
                per_file.append(dict(file=base, status="skipped-too-large", n=0)); continue
            df = pd.read_csv(f, nrows=200000, low_memory=False)
        except Exception as e:
            per_file.append(dict(file=base, status=f"unreadable:{type(e).__name__}", n=0)); continue
        cols = {c.lower().strip(): c for c in df.columns}
        def find(*keys):
            for k in keys:
                for lc, c in cols.items():
                    if lc == k: return c
            for k in keys:
                for lc, c in cols.items():
                    if k in lc: return c
            return None
        cS = find("sharpe", "sharpe_full", "full_sharpe")
        cC = find("cagr", "cagr_full")
        cD = find("maxdd", "max_dd", "dd")
        cG = find("gross", "g_eff", "realised_gross", "mean_gross", "gross_eff")
        if not (cS and cC and cD and cG):
            per_file.append(dict(file=base, status="no-4-column-row", n=0)); continue
        S, C, D, G = _num(df[cS]), _num(df[cC]), _num(df[cD]), _num(df[cG])
        ok = S.notna() & C.notna() & D.notna() & G.notna() & (G > 0) & (G <= 2.5) & (S.abs() < 10)
        if not ok.any():
            per_file.append(dict(file=base, status="no-usable-rows", n=0)); continue
        sub = pd.DataFrame(dict(S=S[ok], C=C[ok], D=D[ok], G=G[ok]))
        panel = ("SMALL" if "small" in base.lower() else
                 "B136" if ("broad" in base.lower() or "b136" in base.lower()) else "U56")
        sub["panel"] = panel
        sub["file"] = base
        rows.append(sub)
        per_file.append(dict(file=base, status="used", n=int(ok.sum()), panel=panel))
    cen = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
    pf = pd.DataFrame(per_file)
    pf.to_csv(f"{OUT}.census.csv", index=False)
    log(f"\n  scanned {len(files)} committed CSVs in {time.time()-t0:.0f}s: "
        f"{(pf.status=='used').sum()} usable, {(pf.status=='no-4-column-row').sum()} lack one of the "
        f"four columns, {(pf.status=='no-usable-rows').sum()} have the columns but no usable row, "
        f"{(pf.status.str.startswith('unreadable')).sum()} unreadable, "
        f"{(pf.status=='skipped-too-large').sum()} too large.")
    if cen.empty:
        log("  NO usable rows -- PART C reports nothing.")
        return cen, {}
    log(f"  -> {len(cen):,} published book-rows across {cen.file.nunique()} files; "
        f"mean gross {cen.G.mean():.3f}, mean cash {1-cen.G.mean():.3f}, "
        f"de-grossed (g<1) {(cen.G<1).mean():.1%}, levered (g>1) {(cen.G>1).mean():.1%}")

    disc = cen.S ** 2 - 2 * cen.C
    cen["vol_hat"] = np.where(disc > 0, cen.S - np.sqrt(disc.clip(lower=0)), np.nan)
    cen = cen[cen.vol_hat.between(0.01, 1.5)]
    log(f"  {len(cen):,} rows survive the vol-recovery domain check (vol_hat in [0.01, 1.5]); "
        f"median vol_hat {cen.vol_hat.median():.3f}")

    out = {}
    log(f"\n  {'rate':>5} {'|dS(C1)| med':>13} {'|dS(C2)| med':>13} {'>0.05 C1':>10} {'>0.05 C2':>10} "
        f"{'S-bar flips C1':>15} {'S-bar flips C2':>15} {'CAGR-floor flips':>17}")
    for c_bps in RATES:
        if c_bps == 0:
            continue
        c = c_bps / 1e4
        dC = (1 - cen.G).clip(lower=0) * c
        dS1 = dC / cen.vol_hat
        dS2 = (dC - c) / cen.vol_hat
        sbar = cen.panel.map({k: v["S"] for k, v in spy_ref.items()})
        cbar = cen.panel.map({k: 0.70 * v["C"] for k, v in spy_ref.items()})
        base_sharpe_pass = cen.S > sbar
        f1 = (((cen.S + dS1) > sbar) != base_sharpe_pass).mean()
        f2 = (((cen.S + dS2) > sbar) != base_sharpe_pass).mean()
        base_cagr_pass = cen.C > cbar
        fc = (((cen.C + dC) > cbar) != base_cagr_pass).mean()
        out[c_bps] = dict(n=len(cen), dS1=dS1.median(), dS2=dS2.median(),
                          big1=(dS1.abs() > 0.05).mean(), big2=(dS2.abs() > 0.05).mean(),
                          flip1=f1, flip2=f2, flipc=fc)
        log(f"  {int(c_bps):>5} {dS1.median():>13.4f} {dS2.median():>13.4f} "
            f"{(dS1.abs()>0.05).mean():>10.2%} {(dS2.abs()>0.05).mean():>10.2%} "
            f"{f1:>15.2%} {f2:>15.2%} {fc:>17.2%}")
    log("\n  (the full-sample Sharpe-vs-SPY bar is NOT a 4b leg -- 4b reads halves + OOS -- so these")
    log("   flip rates are a SIZE statistic for the record's Sharpe column, not a verdict count;")
    log("   PART B counts verdicts exactly. Panel is inferred from the filename, default U56.)")
    return cen, out


# =====================================================================================
# PART D -- rule 8 walk-forward
# =====================================================================================
FAMILIES = [
    ("BAND3-GROSS", "U56", [(g, f) for g in (0.50, 0.625, 0.75, 0.875, 1.00) for f in ("W", "M")],
     lambda px, p: rules_v2_weights(px, 0.03, p[0])),
    ("MAGATE-GROSS", "U56", [(g, f) for g in (0.50, 0.625, 0.75, 0.875, 1.00) for f in ("W", "M")],
     lambda px, p: magate_weights(px, p[0])),
    ("TOPN-GROSS", "U56", [(n, g) for n in (5, 10, 20, 50) for g in (0.50, 0.75, 1.00)],
     lambda px, p: topn_weights(px, p[0], p[1], 0)),
]


def part_d(pxU):
    log("\n" + "=" * 110)
    log("PART D -- PROTOCOL rule 8: the dial chosen on the FIRST half (<= 2016-12-31) by IS")
    log("          Sharpe UNDER EACH TREATMENT, 2017-01-01.. read exactly once.")
    log("=" * 110)
    px = pxU; st = px.index[260]
    Wspy = pd.DataFrame(0.0, index=px.index, columns=px.columns); Wspy["SPY"] = 1.0
    spy_sims = {c: run_cash(px, Wspy, c, "W") for c in RATES}
    v2_sims = {c: run_cash(px, rules_v2_weights(px, 0.03, 0.75), c, "W") for c in RATES}

    rows = []
    for fam, panel, grid, fn in FAMILIES:
        for p in grid:
            freq = p[1] if fam != "TOPN-GROSS" else "W"
            W = fn(px, p)
            for c in RATES:
                sim = run_cash(px, W, c, freq)
                r = net(sim, RUNG_HEAD, st)
                for tname, rf in (("C0", 0.0), ("C1", 0.0), ("C2", c)):
                    if tname == "C0" and c != 0.0: continue
                    if tname != "C0" and c == 0.0: continue
                    rfa = rf / 1e4
                    isr, oosr = r.loc[:IS_END], r.loc[OOS_START:]
                    rows.append(dict(family=fam, dial=str(p), credit_bps=c,
                                     treatment=tname if tname == "C0" else f"{tname}@{int(c)}",
                                     IS_Sharpe=metrics(isr, rf=rfa)["Sharpe"],
                                     OOS_Sharpe=metrics(oosr, rf=rfa)["Sharpe"],
                                     OOS_CAGR=metrics(oosr)["CAGR"], OOS_MaxDD=metrics(oosr)["MaxDD"]))
    wf = pd.DataFrame(rows)
    wf.to_csv(f"{OUT}.wf.csv", index=False)

    log(f"\n  ALL {len(wf)} grid points written to {os.path.basename(OUT)}.wf.csv")
    picks = []
    for fam, panel, grid, fn in FAMILIES:
        log(f"\n  --- family {fam} ({len(grid)} dial cells) " + "-" * 60)
        log(f"  {'treatment':<9} {'IS pick':<14} {'IS Sharpe':>10} {'OOS Sharpe':>11} "
            f"{'OOS CAGR':>9} {'OOS MaxDD':>10} {'vs RULESv2':>11} {'vs SPY':>8}")
        for tname, c, rf in (("C0", 0.0, 0.0), ("C1@150", 150.0, 0.0), ("C1@300", 300.0, 0.0),
                             ("C2@150", 150.0, 150.0), ("C2@300", 300.0, 300.0)):
            sub = wf[(wf.family == fam) & (wf.treatment == tname)]
            if sub.empty: continue
            best = sub.loc[sub.IS_Sharpe.idxmax()]
            rfa = rf / 1e4
            v2o = metrics(net(v2_sims[c], RUNG_HEAD, st).loc[OOS_START:], rf=rfa)
            spo = metrics(net(spy_sims[c], RUNG_HEAD, st).loc[OOS_START:], rf=rfa)
            dv = best.OOS_Sharpe - v2o["Sharpe"]; ds = best.OOS_Sharpe - spo["Sharpe"]
            picks.append(dict(family=fam, treatment=tname, dial=best.dial,
                              OOS_Sharpe=best.OOS_Sharpe, OOS_CAGR=best.OOS_CAGR,
                              OOS_MaxDD=best.OOS_MaxDD, d_v2=dv, d_spy=ds,
                              v2_OOS=v2o["Sharpe"], spy_OOS=spo["Sharpe"]))
            log(f"  {tname:<9} {best.dial:<14} {best.IS_Sharpe:>10.4f} {best.OOS_Sharpe:>11.4f} "
                f"{best.OOS_CAGR:>9.2%} {best.OOS_MaxDD:>10.2%} {dv:>+11.4f} {ds:>+8.4f}")
    pk = pd.DataFrame(picks)
    log(f"\n  the AMENDMENT's effect on rule 8: the IS pick CHANGES under the amendment in "
        f"{sum(1 for f in pk.family.unique() for t in ('C1@150','C1@300','C2@150','C2@300') if not pk[(pk.family==f)&(pk.treatment==t)].empty and pk[(pk.family==f)&(pk.treatment==t)].dial.iloc[0] != pk[(pk.family==f)&(pk.treatment=='C0')].dial.iloc[0])} "
        f"of {len(pk)-len(pk.family.unique())} (family x treatment) cells.")
    log(f"  OOS the pick beats RULES v2 in {int((pk.d_v2>0).sum())} of {len(pk)} cells and "
        f"SPY in {int((pk.d_spy>0).sum())} of {len(pk)}.")
    return wf, pk


# =====================================================================================
def main():
    t0 = time.time()
    log(f"IDEA 641 -- {SLUG}  (cloud, {DATE})")
    log(f"Two tuned parameters: RATE in {RATES} bps x CORPUS in {CORPORA}. Every grid point reported.")
    log("Costs 10 bps headline (25 reported), next-day execution, no shorting, no leverage.")

    pxU = load_universe().loc[:END]
    pxB = load_universe(broad=True).loc[:END]
    start_u = pxU.index[260]

    g = gates(pxU, pxB, start_u)
    assert g["G1"], "G1 FAILED"
    assert g["G2"], "G2 FAILED"

    # ---- PART A -------------------------------------------------------------------
    log("\n" + "=" * 110)
    log("PART A -- the three-line amendment, as idea 641 asks. DRAFT ONLY: this script does NOT")
    log("          edit PROTOCOL.md (rule 6: PROTOCOL/RULES change only at Sunday review).")
    log("=" * 110)
    log(AMENDMENT)

    # ---- PART B -------------------------------------------------------------------
    corpus, safe4b, safe4a = part_b(pxU, pxB, set(g["G3_keep"]))

    # SPY reference per panel, for PART C's bars
    spy_ref = {}
    for pn, px in (("U56", pxU), ("B136", pxB)):
        st = px.index[260]
        W = pd.DataFrame(0.0, index=px.index, columns=px.columns); W["SPY"] = 1.0
        m = metrics(net(run_cash(px, W, 0.0, "W"), RUNG_HEAD, st))
        spy_ref[pn] = dict(S=m["Sharpe"], C=m["CAGR"], D=m["MaxDD"])
    spy_ref["SMALL"] = spy_ref["U56"]      # the small panel joins the same SPY column
    log(f"\n  SPY reference (10 bps, own panel window): " +
        "; ".join(f"{k} {v['C']:.2%}/{v['S']:.4f}/{v['D']:.2%}" for k, v in spy_ref.items()))

    # ---- PART C -------------------------------------------------------------------
    cen, cout = part_c(spy_ref)

    # ---- PART D -------------------------------------------------------------------
    wf, pk = part_d(pxU)

    log(f"\nDONE in {time.time()-t0:.0f}s")
    Path(f"{OUT}.txt").write_text("\n".join(LOG) + "\n")
    return corpus, cen, cout, wf, pk, safe4b, safe4a


AMENDMENT = """
  PROPOSED PROTOCOL clause 10 (DRAFT -- not adopted by this run):

    10. **Cash and the risk-free rate (one convention, three lines).**
        (a) Un-invested NAV earns the credit rate c inside the drift renormalisation, so a
            book at gross g earns (1-g)*c per year on its cash leg;
        (b) every Sharpe and Sortino in the same comparison is computed at rf = c, including
            SPY's and the live book's -- `engine.metrics(r, rf=c)`, never rf=0 beside a
            credited book;
        (c) c is a single number fixed for the whole record and stated in every memo; a run
            may not choose it. Changing c re-prices EVERY committed verdict and is a
            PROTOCOL amendment, not a run-level dial.

  Line (a) alone is what idea 641's parent asked for. Lines (a) and (b) are inseparable:
  (a) without (b) pays a risk-free return and then measures it as excess return.
"""


if __name__ == "__main__":
    main()
