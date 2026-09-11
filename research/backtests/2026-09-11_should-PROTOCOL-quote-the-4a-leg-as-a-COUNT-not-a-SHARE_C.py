#!/usr/bin/env python3
"""Idea 727 — should PROTOCOL quote the 4a leg as a COUNT, not a SHARE?

Idea 721 found that at a ~3% corpus 4a pass rate a 4a pass-SHARE "BELOW" verdict is
unreadable below 180 picks, and that no rule-8 book leg in the record has ever exceeded
96 picks.  It filed the question: should the 4a leg of a rule-8 report be quoted as a
COUNT rather than a SHARE?

This run prices the two FORMS against each other on a FRESH corpus and proposes the
PROTOCOL wording.  It does NOT edit PROTOCOL.md (rule 6: Sunday review only).

TUNED PARAMETERS — exactly two, both swept, ALL grid points reported:
    1. CORPUS in {NARROW (U56 + B136), WIDE (U56 + B136 + SMALL)}
    2. FORM   in {SHARE (the record's practice), COUNT (the proposal)}
Everything else is pre-registered and fixed: panels, families, the n ladder, the gross
ladder, the cadence ladder, 10 bps, t+1 execution, the IS/OOS split, alpha = 0.05.

FRESHNESS.  Idea 721's corpus was families {RANK n in 5/10/20/50, GATE} on the same three
panels.  This corpus is families {CAND n in 10/20/30/40, IVOL n in 10/20/30/40, EWALL} —
a different family set and a different n ladder.  Panels are data, not corpus design.

Outputs (all beside this script):
    .console.txt   full run log
    .corpus.csv    every book, every grid point
    .floors.csv    form x path x direction x m ladder — feasibility and power
    .picks.csv     rule-8 picks, read once on OOS
    .walkforward.csv  the rule-8 leg summary
    .census.csv    every committed pass4a leg in the record, re-read against its own floor
    .result.md     the memo
"""
from __future__ import annotations
import json, sys, math, itertools, hashlib
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
import baseline
from baseline import load_universe, rules_v2_weights, score, band_state
from engine import backtest as engine_backtest, metrics, rebalance_mask

STEM = Path(__file__).with_suffix("")
OUT = lambda ext: Path(str(STEM) + ext)

RNG_SEED = 727
IS_END = "2016-12-31"          # rule 8: fit on <= IS_END
OOS_START = "2017-01-01"       # rule 8: read ONCE on >= OOS_START
COST_BPS = 10.0
ALPHA = 0.05
BAND = 0.03                    # RULES v2 clause 2 hysteresis band, fixed
NS = (10, 20, 30, 40)
GROSSES = (0.50, 0.75, 1.00)
CADENCES = ("W", "M")
FAMILIES = ("CAND", "IVOL", "EWALL")
M_LADDER = (12, 15, 18, 24, 30, 36, 48, 60, 72, 96, 120, 180, 240, 360, 540)
THETAS = (0.0, 0.25, 0.50, 2.0, 3.0, 5.0)   # alternative = theta x corpus base rate

_LOG: list[str] = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); _LOG.append(s)


# ----------------------------------------------------------------------------- harness
def fast_backtest(px_vals: np.ndarray, w_vals: np.ndarray, rb: np.ndarray,
                  cost_bps=COST_BPS) -> np.ndarray:
    """numpy clone of engine.backtest; returns the daily portfolio return series."""
    T, N = px_vals.shape
    rets = np.zeros_like(px_vals)
    rets[1:] = px_vals[1:] / px_vals[:-1] - 1.0
    rets = np.nan_to_num(rets, nan=0.0, posinf=0.0, neginf=0.0)
    wt = np.vstack([np.zeros((1, N)), w_vals[:-1]])      # decided at t, applied at t+1
    mask = np.concatenate([[False], rb[:-1]])            # engine shifts the mask too
    cur = np.zeros(N); out = np.zeros(T)
    for i in range(T):
        if mask[i] or i == 0:
            new = wt[i]
            to = np.abs(new - cur).sum(); cur = new
        else:
            to = 0.0
        out[i] = (cur * rets[i]).sum() - to * cost_bps / 1e4
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    return out


def mets(r: pd.Series) -> dict:
    m = metrics(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"])


def three_windows(r: pd.Series) -> dict:
    """full, the two halves (PROTOCOL rule 4) and the rule-8 IS/OOS split."""
    h = len(r) // 2
    d = {}
    for tag, s in (("full", r), ("H1", r.iloc[:h]), ("H2", r.iloc[h:]),
                   ("IS", r.loc[:IS_END]), ("OOS", r.loc[OOS_START:])):
        m = mets(s)
        d[f"{tag}_CAGR"], d[f"{tag}_Sharpe"], d[f"{tag}_MaxDD"] = m["CAGR"], m["Sharpe"], m["MaxDD"]
        eq = (1 + s).cumprod(); dd = (eq / eq.cummax() - 1).min()
        d[f"{tag}_Calmar"] = (mets(s)["CAGR"] / abs(dd)) if dd < 0 else np.nan
    return d


# ------------------------------------------------------------------------ book families
def cand_weights(px, sc, elig, n, gross):
    s = sc.where(elig)
    rank = s.rank(axis=1, ascending=False)
    pick = (rank <= n) & s.notna()
    k = pick.sum(axis=1).replace(0, np.nan)
    return pick.astype(float).mul(gross, axis=0).div(np.minimum(k, n), axis=0).fillna(0.0)


def ivol_weights(px, sc, elig, vol20, n, gross):
    s = sc.where(elig)
    rank = s.rank(axis=1, ascending=False)
    pick = (rank <= n) & s.notna()
    iv = (1.0 / vol20.clip(lower=0.08)).where(pick, 0.0)
    tot = iv.sum(axis=1).replace(0, np.nan)
    return iv.div(tot, axis=0).mul(gross).fillna(0.0)


def ewall_weights(px, elig, gross):
    """RULES v2's own form: gross/N over every instrument PRICED that day, gated-out weight
    to CASH (de-gross, never re-spread).  N is the priced count, not the eligible count."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(elig, 0.0)


def build_books(panel, px):
    """(book_id, family, n, gross, cadence, weights DataFrame) for one panel."""
    names = [c for c in px.columns if c != "SPY"]
    p = px[names]
    sc, above, vol20 = score(p, vol_scale=True)
    bs = band_state(p, BAND)
    elig = bs & p.notna()
    out = []
    for g in GROSSES:
        w_ew = ewall_weights(p, bs, g)
        for cad in CADENCES:
            out.append((f"{panel}|EWALL|g{g:.2f}|{cad}", "EWALL", np.nan, g, cad, w_ew))
        for n in NS:
            w_c = cand_weights(p, sc, elig, n, g)
            w_i = ivol_weights(p, sc, elig, vol20, n, g)
            for cad in CADENCES:
                out.append((f"{panel}|CAND{n}|g{g:.2f}|{cad}", "CAND", n, g, cad, w_c))
                out.append((f"{panel}|IVOL{n}|g{g:.2f}|{cad}", "IVOL", n, g, cad, w_i))
    return out, p


# ------------------------------------------------------------------------------- gates
def gates(panels):
    say("\n" + "=" * 78)
    say("GATES (pre-registered, printed before any new number is read)")
    say("=" * 78)
    ok = True

    px = panels["U56"]
    names = [c for c in px.columns if c != "SPY"]
    p = px[names]

    # G1 — fast_backtest == engine.backtest
    dev = 0.0
    sc, above, vol20 = score(p, vol_scale=True)
    elig = band_state(p, BAND) & p.notna()
    for (n, g, cad) in ((20, 0.75, "W"), (10, 1.00, "M")):
        w = cand_weights(p, sc, elig, n, g)
        rb = rebalance_mask(p.index, cad).values
        a = fast_backtest(p.values, w.reindex(p.index).fillna(0.0).values, rb)
        b = engine_backtest(p, w, cost_bps=COST_BPS, freq=cad)["returns"].values
        dev = max(dev, float(np.abs(a - b).max()))
    say(f"G1 fast_backtest == engine.backtest, max abs dev = {dev:.3e}  (bar 1e-12) -> "
        f"{'PASS' if dev < 1e-12 else 'FAIL'}")
    ok &= dev < 1e-12

    # G2 — the live book reproduces exactly from baseline
    w_ew = ewall_weights(p, band_state(p, BAND), 0.75)
    w_v2 = rules_v2_weights(p, band=BAND, gross=0.75)
    d2 = float((w_ew - w_v2.reindex_like(w_ew).fillna(0.0)).abs().max().max())
    say(f"G2 EWALL(g=0.75) == baseline.rules_v2_weights on U56, max abs dev = {d2:.3e}  "
        f"(bar 0.0) -> {'PASS' if d2 == 0.0 else 'FAIL'}")
    ok &= d2 == 0.0

    # G3 — idea 721's committed numbers, READ from its own CSVs, never retyped
    g721 = ROOT / "research" / "backtests" / (
        "2026-09-11_publish-a-MINIMUM-CLAIM-COUNT-beside-every-permutation-band-verdict_cloud")
    bg = pd.read_csv(str(g721) + ".bookgrid.csv")
    books721 = bg[bg.fam != "BENCH"]
    n4a, n4b, nbk = int(books721.pass4a.sum()), int(books721.pass4b.sum()), len(books721)
    pf = pd.read_csv(str(g721) + ".pricefloor.csv")
    f4a = pf[(pf.path == "4a") & (pf.band == "5-95") & pf.feasible_below]
    f4b = pf[(pf.path == "4b") & (pf.band == "5-95") & pf.feasible_below]
    m4a = int(f4a.m.min()) if len(f4a) else -1
    m4b = int(f4b.m.min()) if len(f4b) else -1
    say(f"G3 idea 721 corpus re-read from .bookgrid.csv: 4a {n4a}/{nbk} "
        f"({n4a/nbk:.2%}), 4b {n4b}/{nbk} ({n4b/nbk:.2%})  "
        f"-> {'PASS' if (n4a, n4b, nbk) == (4, 18, 126) else 'FAIL'}")
    ok &= (n4a, n4b, nbk) == (4, 18, 126)
    say(f"G3b idea 721 floors re-read from .pricefloor.csv: 4a BELOW readable at m >= {m4a}, "
        f"4b at m >= {m4b}  -> {'PASS' if (m4a, m4b) == (180, 24) else 'FAIL'}")
    ok &= (m4a, m4b) == (180, 24)

    # G4 — SPY comparand finite
    spy = px["SPY"].pct_change().fillna(0.0)
    sm = mets(spy.loc[OOS_START:])
    say(f"G4 SPY OOS from baseline.load_universe: CAGR {sm['CAGR']:.2%} Sharpe "
        f"{sm['Sharpe']:.4f} MaxDD {sm['MaxDD']:.2%} -> "
        f"{'PASS' if np.isfinite(sm['Sharpe']) else 'FAIL'}")
    ok &= bool(np.isfinite(sm["Sharpe"]))

    say(f"\nGATES: {'ALL PASS' if ok else 'FAILURE — run aborted'}")
    assert ok, "pre-registered gate failed"
    return dict(n4a721=n4a, n4b721=n4b, nbk721=nbk, m4a721=m4a, m4b721=m4b)


# ------------------------------------------------------------- Poisson-binomial machinery
def pb_pmf(ps: np.ndarray) -> np.ndarray:
    """Exact pmf of sum of independent Bernoulli(ps)."""
    pmf = np.zeros(len(ps) + 1); pmf[0] = 1.0
    for i, p in enumerate(ps):
        pmf[1:i + 2] = pmf[1:i + 2] * (1 - p) + pmf[0:i + 1] * p
        pmf[0] *= (1 - p)
    return pmf


def cyclic_ps(p_strata: np.ndarray, m: int) -> np.ndarray:
    """Pre-registered extension of a fixed S-stratum leg to an arbitrary leg length m:
    pick j uses stratum (j mod S).  Exact at m = S, preserves the strata's heterogeneity."""
    S = len(p_strata)
    return np.array([p_strata[j % S] for j in range(m)])


def quantile_from_pmf(pmf: np.ndarray, q: float) -> int:
    c = np.cumsum(pmf)
    return int(np.searchsorted(c, q - 1e-12))


def verdict_share(k: int, m: int, pmf: np.ndarray) -> str:
    """The record's practice: position of the realised SHARE against the null share
    band [q05, q95], read as a 3-way trichotomy."""
    lo, hi = quantile_from_pmf(pmf, 0.05), quantile_from_pmf(pmf, 0.95)
    s, slo, shi = k / m, lo / m, hi / m
    if s < slo: return "BELOW"
    if s > shi: return "ABOVE"
    return "INSIDE"


def asl(k: int, pmf: np.ndarray) -> tuple[float, float]:
    """One-sided achieved significance levels P(K<=k) and P(K>=k)."""
    c = np.cumsum(pmf)
    return float(c[k]), float(1.0 - (c[k - 1] if k > 0 else 0.0))


def verdict_count(k: int, pmf: np.ndarray, alpha=ALPHA) -> str:
    lo, hi = asl(k, pmf)
    if lo <= alpha: return "BELOW"
    if hi <= alpha: return "ABOVE"
    return "INSIDE"


def feas(pmf: np.ndarray, m: int, form: str) -> tuple[bool, bool]:
    """Is a BELOW / an ABOVE verdict attainable AT ALL at this m, under this form?"""
    if form == "SHARE":
        lo, hi = quantile_from_pmf(pmf, 0.05), quantile_from_pmf(pmf, 0.95)
        return lo > 0, hi < m
    return verdict_count(0, pmf) == "BELOW", verdict_count(m, pmf) == "ABOVE"


def power(pmf_null: np.ndarray, p_alt: np.ndarray, m: int, form: str, direction: str,
          n_draw=20000, rng=None) -> float:
    """P(reading `direction` | true per-pick pass prob p_alt), exact by convolution."""
    pmf_alt = pb_pmf(p_alt)
    v = [(verdict_share(k, m, pmf_null) if form == "SHARE" else verdict_count(k, pmf_null))
         for k in range(m + 1)]
    return float(sum(pmf_alt[k] for k in range(m + 1) if v[k] == direction))


# ------------------------------------------------------------------------------ the run
def main():
    say(f"Idea 727 — should PROTOCOL quote the 4a leg as a COUNT, not a SHARE?")
    say(f"lane C · {pd.Timestamp.today().date()} · seed {RNG_SEED} · {COST_BPS:.0f} bps · t+1")

    panels = {}
    say("\nLoading panels (committed caches only — no network)...")
    panels["U56"] = load_universe()
    panels["B136"] = load_universe(broad=True)
    sm = load_universe(small=True)
    mx = sm.drop(columns=["SPY"]).pct_change().abs().max()
    drop = list(mx[mx >= 1.0].index)
    panels["SMALL"] = sm.drop(columns=drop)
    say(f"  U56 {panels['U56'].shape}  B136 {panels['B136'].shape}  "
        f"SMALL {panels['SMALL'].shape} (dropped {len(drop)} names with max_1d_move >= 1.0)")

    g = gates(panels)

    # ---------------------------------------------------------------- corpus of books
    say("\n" + "=" * 78)
    say("THE FRESH CORPUS — families {CAND n, IVOL n, EWALL} x gross x cadence x panel")
    say("=" * 78)
    rows = []
    bench = {}
    for panel, px in panels.items():
        books, p = build_books(panel, px)
        spy = px["SPY"].reindex(p.index).ffill().pct_change().fillna(0.0)
        v2 = pd.Series(fast_backtest(p.values,
                                     rules_v2_weights(p, band=BAND, gross=0.75).values,
                                     rebalance_mask(p.index, "W").values), index=p.index)
        start = p.index[260]                       # skip warm-up, as baseline.compare does
        spy, v2 = spy.loc[start:], v2.loc[start:]
        bench[panel] = dict(spy=three_windows(spy), v2=three_windows(v2))
        say(f"\n{panel}: {len(books)} books · sample {start.date()} -> {p.index[-1].date()}")
        say(f"  SPY      full {bench[panel]['spy']['full_CAGR']:7.2%} / "
            f"{bench[panel]['spy']['full_Sharpe']:.4f} / {bench[panel]['spy']['full_MaxDD']:7.2%}"
            f"   OOS {bench[panel]['spy']['OOS_CAGR']:7.2%} / "
            f"{bench[panel]['spy']['OOS_Sharpe']:.4f} / {bench[panel]['spy']['OOS_MaxDD']:7.2%}")
        say(f"  RULES v2 full {bench[panel]['v2']['full_CAGR']:7.2%} / "
            f"{bench[panel]['v2']['full_Sharpe']:.4f} / {bench[panel]['v2']['full_MaxDD']:7.2%}"
            f"   OOS {bench[panel]['v2']['OOS_CAGR']:7.2%} / "
            f"{bench[panel]['v2']['OOS_Sharpe']:.4f} / {bench[panel]['v2']['OOS_MaxDD']:7.2%}")
        S, V = bench[panel]["spy"], bench[panel]["v2"]
        pv = p.values
        for (bid, fam, n, gr, cad, w) in books:
            rb = rebalance_mask(p.index, cad).values
            r = pd.Series(fast_backtest(pv, w.reindex(p.index).fillna(0.0).values, rb),
                          index=p.index).loc[start:]
            d = three_windows(r)
            # PROTOCOL 4a — beat the book
            p4a = (d["H1_Sharpe"] > V["H1_Sharpe"] and d["H2_Sharpe"] > V["H2_Sharpe"]
                   and d["full_MaxDD"] >= V["full_MaxDD"])
            # PROTOCOL 4b — capital-worthy
            p4b = (d["H1_Sharpe"] > S["H1_Sharpe"] and d["H2_Sharpe"] > S["H2_Sharpe"]
                   and d["OOS_Sharpe"] > S["OOS_Sharpe"]
                   and abs(d["full_MaxDD"]) <= 0.60 * abs(S["full_MaxDD"])
                   and d["full_CAGR"] >= 0.70 * S["full_CAGR"])
            rows.append(dict(panel=panel, book=bid, fam=fam, n=n, gross=gr, cadence=cad,
                             pass4a=p4a, pass4b=p4b, **d))
    corpus = pd.DataFrame(rows)
    corpus.to_csv(OUT(".corpus.csv"), index=False)

    say("\nAll grid points (4a / 4b pass counts by panel x family x gross x cadence):")
    piv = corpus.pivot_table(index=["panel", "fam"], columns=["gross", "cadence"],
                             values=["pass4a", "pass4b"], aggfunc="sum")
    say(piv.to_string())

    CORPORA = {"NARROW": ["U56", "B136"], "WIDE": ["U56", "B136", "SMALL"]}
    say("\nCorpus base rates (tuned parameter 1, both cells reported):")
    base_rates = {}
    for cname, pl in CORPORA.items():
        sub = corpus[corpus.panel.isin(pl)]
        r4a, r4b = sub.pass4a.mean(), sub.pass4b.mean()
        base_rates[cname] = (r4a, r4b, len(sub))
        say(f"  {cname:6s} {len(sub):3d} books   4a {int(sub.pass4a.sum()):3d} ({r4a:6.2%})"
            f"   4b {int(sub.pass4b.sum()):3d} ({r4b:6.2%})")

    # ---------------------------------------------------------------- rule 8 / WF-A
    say("\n" + "=" * 78)
    say("RULE 8 (walk-forward) — selector picks on IS ONLY (<= %s), read ONCE on OOS (>= %s)"
        % (IS_END, OOS_START))
    say("=" * 78)
    SELECTORS = {"IS_SHARPE": "IS_Sharpe", "IS_CAGR": "IS_CAGR",
                 "IS_CALMAR": "IS_Calmar", "IS_MINDD": "IS_MaxDD"}
    picks, wf = [], []
    for cname, pl in CORPORA.items():
        sub = corpus[corpus.panel.isin(pl)].copy()
        strata = sorted(sub.groupby(["panel", "gross", "cadence"]).groups.keys())
        for sel, col in SELECTORS.items():
            got = []
            for st in strata:
                cell = sub[(sub.panel == st[0]) & (sub.gross == st[1]) & (sub.cadence == st[2])]
                b = cell.loc[cell[col].idxmax()]
                got.append(b)
                picks.append(dict(corpus=cname, selector=sel, panel=st[0], gross=st[1],
                                  cadence=st[2], n_cand=len(cell), book=b.book,
                                  pass4a=bool(b.pass4a), pass4b=bool(b.pass4b),
                                  OOS_CAGR=b.OOS_CAGR, OOS_Sharpe=b.OOS_Sharpe,
                                  OOS_MaxDD=b.OOS_MaxDD,
                                  v2_OOS_Sharpe=bench[st[0]]["v2"]["OOS_Sharpe"],
                                  spy_OOS_Sharpe=bench[st[0]]["spy"]["OOS_Sharpe"]))
            G = pd.DataFrame(got)
            wf.append(dict(corpus=cname, selector=sel, m=len(G),
                           k4a=int(G.pass4a.sum()), k4b=int(G.pass4b.sum()),
                           OOS_CAGR=G.OOS_CAGR.mean(), OOS_Sharpe=G.OOS_Sharpe.mean(),
                           OOS_MaxDD=G.OOS_MaxDD.mean(),
                           beat_v2=int(sum(G.OOS_Sharpe.values >
                                           [bench[p_]["v2"]["OOS_Sharpe"] for p_ in G.panel])),
                           beat_spy=int(sum(G.OOS_Sharpe.values >
                                            [bench[p_]["spy"]["OOS_Sharpe"] for p_ in G.panel]))))
    picks = pd.DataFrame(picks); picks.to_csv(OUT(".picks.csv"), index=False)
    WF = pd.DataFrame(wf); WF.to_csv(OUT(".walkforward.csv"), index=False)
    say("\n" + WF.to_string(index=False,
        formatters={"OOS_CAGR": "{:.2%}".format, "OOS_Sharpe": "{:.4f}".format,
                    "OOS_MaxDD": "{:.2%}".format}))
    say("\nOOS comparands (mean over the corpus's panels):")
    for cname, pl in CORPORA.items():
        say(f"  {cname:6s} RULES v2 Sharpe {np.mean([bench[p_]['v2']['OOS_Sharpe'] for p_ in pl]):.4f}"
            f"  CAGR {np.mean([bench[p_]['v2']['OOS_CAGR'] for p_ in pl]):.2%}"
            f"  MaxDD {np.mean([bench[p_]['v2']['OOS_MaxDD'] for p_ in pl]):.2%}"
            f"   |   SPY Sharpe {np.mean([bench[p_]['spy']['OOS_Sharpe'] for p_ in pl]):.4f}"
            f"  CAGR {np.mean([bench[p_]['spy']['OOS_CAGR'] for p_ in pl]):.2%}"
            f"  MaxDD {np.mean([bench[p_]['spy']['OOS_MaxDD'] for p_ in pl]):.2%}")

    # ---------------------------------------------------------- FORM head-to-head
    say("\n" + "=" * 78)
    say("THE HEAD-TO-HEAD — SHARE (record practice) vs COUNT (the proposal), matched alpha")
    say("=" * 78)
    say("Null: a uniform random pick inside each stratum.  Per-stratum pass probability")
    say("p_s = (# passers in the stratum) / (# books in the stratum).  A leg of m picks is")
    say("the Poisson-binomial of the cyclically-extended p_s (exact at m = S).")

    frows = []
    for cname, pl in CORPORA.items():
        sub = corpus[corpus.panel.isin(pl)]
        for path in ("4a", "4b"):
            ps_by_stratum = (sub.groupby(["panel", "gross", "cadence"])[f"pass{path}"]
                             .mean().values)
            pbar = float(ps_by_stratum.mean())
            S = len(ps_by_stratum)
            say(f"\n[{cname} / {path}]  S = {S} strata, p_bar = {pbar:.4f}, "
                f"per-stratum p_s = {np.round(ps_by_stratum, 4).tolist()}")
            # Monte-Carlo cross-check of the exact convolution at m = S
            rng = np.random.default_rng(RNG_SEED)
            draws = (rng.random((20000, S)) < ps_by_stratum).sum(axis=1)
            pmf_S = pb_pmf(ps_by_stratum)
            mc = np.bincount(draws, minlength=S + 1)[:S + 1] / 20000
            say(f"  cross-check exact-vs-20k-MC pmf, max abs dev = "
                f"{np.abs(pmf_S - mc).max():.4f}")
            for m in M_LADDER:
                ps_m = cyclic_ps(ps_by_stratum, m)
                pmf = pb_pmf(ps_m)
                for form in ("SHARE", "COUNT"):
                    fb, fa = feas(pmf, m, form)
                    row = dict(corpus=cname, path=path, m=m, form=form, p_bar=pbar,
                               null_lo=quantile_from_pmf(pmf, 0.05),
                               null_hi=quantile_from_pmf(pmf, 0.95),
                               P_K0=float(pmf[0]), feas_below=fb, feas_above=fa)
                    for th in THETAS:
                        p_alt = np.clip(ps_m * th, 0.0, 1.0)
                        d = "BELOW" if th < 1 else "ABOVE"
                        row[f"pow_th{th:g}"] = power(pmf, p_alt, m, form, d)
                    frows.append(row)
    F = pd.DataFrame(frows); F.to_csv(OUT(".floors.csv"), index=False)

    say("\nFEASIBILITY FLOORS — smallest m at which a verdict in that direction is")
    say("attainable AT ALL (alpha = 0.05), by EXACT integer search (not ladder rungs).")
    say("ALL FOUR (corpus x form) cells reported, alongside the homogeneous closed form")
    say("m* = ceil(ln(alpha)/ln(1 - p_bar)), which is what a PROTOCOL clause could quote.")
    hdr = (f"{'corpus':7s} {'path':4s} {'form':6s} {'p_bar':>8s} {'FEAS_below':>10s} "
           f"{'closed':>7s} {'FEAS_above':>10s}")
    say(hdr); say("-" * len(hdr))
    floor_tbl = []
    MMAX = 20000
    for cname, pl in CORPORA.items():
        sub = corpus[corpus.panel.isin(pl)]
        for path in ("4a", "4b"):
            ps = sub.groupby(["panel", "gross", "cadence"])[f"pass{path}"].mean().values
            pbar = float(ps.mean())
            closed = (math.ceil(math.log(ALPHA) / math.log(1 - pbar)) if 0 < pbar < 1
                      else np.inf)
            # Both feasibility questions reduce to two running products, so the exact
            # integer search is O(MMAX) rather than O(MMAX^3) via the pmf:
            #   BELOW readable  <=>  P(K=0) = prod_j (1-p_j)  {<= alpha (COUNT), < alpha (SHARE)}
            #   ABOVE readable  <=>  P(K=m) = prod_j  p_j     {<= alpha, both forms}
            for form in ("SHARE", "COUNT"):
                fb = fa = np.inf
                p0 = p1 = 1.0
                for m in range(1, MMAX + 1):
                    pj = ps[(m - 1) % len(ps)]
                    p0 *= (1 - pj); p1 *= pj
                    b = (p0 <= ALPHA) if form == "COUNT" else (p0 < ALPHA)
                    a = p1 <= ALPHA
                    if b and fb is np.inf: fb = m
                    if a and fa is np.inf: fa = m
                    if fb is not np.inf and fa is not np.inf: break
                floor_tbl.append(dict(corpus=cname, path=path, form=form, p_bar=pbar,
                                      feas_below=fb, closed_form=closed, feas_above=fa))
                say(f"{cname:7s} {path:4s} {form:6s} {pbar:8.4f} {str(fb):>10s} "
                    f"{str(closed):>7s} {str(fa):>10s}")
    FT = pd.DataFrame(floor_tbl); FT.to_csv(OUT(".exactfloors.csv"), index=False)

    say("\nPOWER at the record's actual leg lengths (theta = alternative / base rate):")
    for cname in CORPORA:
        for path in ("4a", "4b"):
            for m in (12, 18, 96, 180):
                sl = F[(F.corpus == cname) & (F.path == path) & (F.m == m)]
                if sl.empty: continue
                s_ = sl[sl.form == "SHARE"].iloc[0]; c_ = sl[sl.form == "COUNT"].iloc[0]
                say(f"  {cname:6s} {path} m={m:4d}  "
                    + "  ".join(f"th{th:g} S{s_[f'pow_th{th:g}']:.3f}/C{c_[f'pow_th{th:g}']:.3f}"
                                for th in THETAS))

    # the head-to-head number the queue actually asked for
    same = 0; tot = 0; diffs = []
    for _, a in F[F.form == "SHARE"].iterrows():
        b = F[(F.corpus == a.corpus) & (F.path == a.path) & (F.m == a.m)
              & (F.form == "COUNT")].iloc[0]
        tot += 2
        same += int(a.feas_below == b.feas_below) + int(a.feas_above == b.feas_above)
        for th in THETAS:
            diffs.append(abs(a[f"pow_th{th:g}"] - b[f"pow_th{th:g}"]))
    say(f"\nFORM AGREEMENT: {same}/{tot} feasibility cells identical across the two forms; "
        f"max |power difference| over {len(diffs)} matched (corpus,path,m,theta) points = "
        f"{max(diffs):.6f}, mean {np.mean(diffs):.6f}")

    # ------------------------------------------------- what the two forms DO differ on
    say("\n" + "=" * 78)
    say("WHAT THE COUNT FORM ACTUALLY BUYS — graded evidence inside the INSIDE verdict")
    say("=" * 78)
    grad = []
    for _, r in picks.groupby(["corpus", "selector"]).agg(
            m=("pass4a", "size"), k4a=("pass4a", "sum"), k4b=("pass4b", "sum")).reset_index().iterrows():
        cname = r.corpus
        sub = corpus[corpus.panel.isin(CORPORA[cname])]
        for path, k in (("4a", int(r.k4a)), ("4b", int(r.k4b))):
            ps = (sub.groupby(["panel", "gross", "cadence"])[f"pass{path}"].mean().values)
            pmf = pb_pmf(cyclic_ps(ps, int(r.m)))
            lo, hi = asl(k, pmf)
            grad.append(dict(corpus=cname, selector=r.selector, path=path, m=int(r.m), k=k,
                             share=k / r.m, null_lo=quantile_from_pmf(pmf, 0.05) / r.m,
                             null_hi=quantile_from_pmf(pmf, 0.95) / r.m,
                             v_share=verdict_share(k, int(r.m), pmf),
                             v_count=verdict_count(k, pmf),
                             ASL_below=lo, ASL_above=hi))
    GR = pd.DataFrame(grad)
    say(GR.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    hidden = GR[(GR.v_share == "INSIDE") & (GR.ASL_above <= 0.20)]
    say(f"\nlegs reading INSIDE under SHARE whose one-sided ASL is nonetheless <= 0.20: "
        f"{len(hidden)} of {len(GR)}")

    # ----------------------------------------------- census of the record's own 4a legs
    say("\n" + "=" * 78)
    say("CENSUS — every committed leg in the record carrying a pass4a column, re-read")
    say("against its OWN separation floor (files enumerated, nothing matched by keyword)")
    say("=" * 78)
    cen = []
    bt = ROOT / "research" / "backtests"
    for f in sorted(bt.glob("*.csv")):
        try:
            d = pd.read_csv(f, low_memory=False)
        except Exception:
            continue
        if "pass4a" not in d.columns: continue
        col = d["pass4a"]
        if col.dtype == object:
            col = col.astype(str).str.strip().str.lower().map({"true": True, "false": False})
        col = col.dropna().astype(bool)
        if len(col) == 0: continue
        m, k = len(col), int(col.sum())
        rate = k / m
        pmf = pb_pmf(np.full(m, rate)) if 0 < rate < 1 else None
        # the floor implied by this file's OWN observed rate
        fl = np.inf
        for mm in range(1, 4001):
            if (1 - rate) ** mm <= ALPHA: fl = mm; break
        cen.append(dict(file=f.name, m=m, k4a=k, rate=rate, feas_below_floor=fl,
                        below_own_floor=bool(m < fl)))
    CEN = pd.DataFrame(cen).sort_values("m", ascending=False)
    CEN["scale"] = pd.cut(CEN.m, [0, 100, 1000, 10 ** 9],
                          labels=["LEG (m<=100)", "MID (101-1000)", "GRID (m>1000)"])
    CEN.to_csv(OUT(".census.csv"), index=False)
    say(f"{len(CEN)} committed tables carry a pass4a column.  Each is read as a claim")
    say("population of size m = its row count; the floor is the m at which a BELOW verdict")
    say("becomes feasible at that table's OWN observed 4a rate.  NOTE: only the LEG bucket")
    say("is rule-8-leg scale; the GRID bucket is whole design grids, not selector legs.")
    say(f"{int(CEN.below_own_floor.sum())} of {len(CEN)} ({CEN.below_own_floor.mean():.1%}) "
        f"sit BELOW their own floor.")
    say("\n" + CEN.groupby("scale", observed=False).agg(
        tables=("m", "size"), med_m=("m", "median"), med_rate=("rate", "median"),
        zero_rate=("rate", lambda s: int((s == 0).sum())),
        below_floor=("below_own_floor", "sum"),
        share=("below_own_floor", "mean")).to_string(float_format=lambda x: f"{x:.4f}"))
    say("\nThe 25 largest tables:")
    say(CEN.head(25).drop(columns=["scale"]).to_string(index=False,
                                                       float_format=lambda x: f"{x:.4f}"))
    leg = CEN[CEN.m <= 100]
    say(f"\nLEG bucket (m <= 100, the scale a rule-8 book leg actually runs at): "
        f"{len(leg)} tables, median m {int(leg.m.median())}, median 4a rate "
        f"{leg.rate.median():.4f}, {int((leg.rate == 0).sum())} with a ZERO 4a rate "
        f"(floor = infinite), {int(leg.below_own_floor.sum())} of {len(leg)} "
        f"({leg.below_own_floor.mean():.1%}) below their own floor.")
    say(f"\nall-table m distribution: min {CEN.m.min()}  median {int(CEN.m.median())}  "
        f"max {CEN.m.max()};  4a rate: min {CEN.rate.min():.4f} median "
        f"{CEN.rate.median():.4f} max {CEN.rate.max():.4f}")

    # ------------------------------------------------------------------ KEEP evaluation
    say("\n" + "=" * 78)
    say("BOTH KEEP PATHS ON THE CORPUS")
    say("=" * 78)
    for cname, (r4a, r4b, nb) in base_rates.items():
        say(f"  {cname}: 4a {int(round(r4a*nb))}/{nb}, 4b {int(round(r4b*nb))}/{nb}")
    best = corpus.loc[corpus.pass4b] if corpus.pass4b.any() else corpus.iloc[0:0]
    if len(best):
        say("\n4b passers (full sample):")
        say(best[["panel", "book", "full_CAGR", "full_Sharpe", "full_MaxDD",
                  "H1_Sharpe", "H2_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\nThis run's object is a REPORTING FORM, not a book.  No KEEP is claimed: no book")
    say("here was selected out of sample by anything other than the rule-8 selectors above,")
    say("and none of those legs separates from its own random-pick null (see the table).")

    OUT(".console.txt").write_text("\n".join(_LOG) + "\n")
    return corpus, F, FT, WF, GR, CEN


if __name__ == "__main__":
    main()
