#!/usr/bin/env python3
"""QUEUE 1111 — is-the-lam-LINEARITY-of-TURNOVER-assumed-anywhere-ELSE-in-the-record

PREMISE (idea 1106, committed 2026-09-16).  Under the REBUILT DD-match the rebuilt book's
cost term is

    tr(lam) = lam * | W_r - A_p / V_p(lam) |_1 ,     V_p(lam) = 1 + lam * (S_p - W_sp)

so `tr(lam) / lam` is NOT `tr(1)` unless the cash sleeve `S_p - W_sp` is identically zero.
1106 recovered a null's raw turnover as `matched / lam`, its declared gate G1d FAILED, and it
measured the error at 1.75% of peak rebalance turnover.  1111 asks whether that shortcut is
assumed ANYWHERE ELSE in the committed record, and re-prices the exposure.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4)
  D1  CLAIM SET   {STRICT, WIDE}
        STRICT — a committed script whose SOURCE performs arithmetic joining a DD-match
                 lambda variable to a turnover / cost / drag quantity (`turn/lam`, `lam*turn`,
                 `turn*lam`, `cost/lam`, ...), i.e. the shortcut is written down.
        WIDE   — STRICT plus every committed script that BUILDS a DD-match lambda AND commits
                 a turnover / cost / drag figure.  These do not write `/lam`, but a reader who
                 wants the raw turnover behind a matched figure has no other route, and the
                 record's own `gross_rescaler` docstring TELLS them the route is exact.
  D2  TOLERANCE  {0.5%, 1%, 2%, 5%} of peak rebalance turnover — the bar above which a
                 linearity-recovered figure counts as MATERIALLY wrong.
  All 2 x 4 = 8 grid points are reported.  PANEL, N and the lam ladder are COORDINATE SETS,
  not dials: every rung is published, none is chosen.

WHAT IS MEASURED, AND HOW
  NTURN_raw       annualised one-way turnover of the book evaluated DIRECTLY at lam = 1.
  NTURN_matched   the turnover actually charged after the DD-match rebuild at lam.
  NTURN_recov     NTURN_matched / lam — what the shortcut would report.
  ERR             NTURN_recov - NTURN_raw, in turns/yr, as a fraction of NTURN_raw, and as a
                  fraction of PEAK REBALANCE turnover (1106's unit, kept for comparability).
  The closed form above says ERR is driven by the CASH SLEEVE, so the run also reports the
  realised sleeve per cell and the rank correlation of |ERR| against it.

HYPOTHESES, DECLARED BEFORE ANY NUMBER
  H_EXPOSED   the STRICT claim set is NON-EMPTY beyond 1106 itself (i.e. the shortcut is
              written down somewhere else in the record).
  H_WIDE      the WIDE claim set covers >= 10 committed scripts.
  H_SIZE      the error is of 1106's order: median |ERR| / peak rebalance turnover within
              [0.5%, 5%] across the re-priced grid.
  H_SLEEVE    Spearman(|ERR|, cash sleeve) >= +0.5 — the closed form's named mechanism.
  H_SIGN      ERR has a CONSTANT sign across the grid (so the shortcut is a bias, not noise).
  H_MATERIAL  at the 1% tolerance rung, a MAJORITY of re-priced cells are flagged.

GATES print before any result number.  RULE 8 walk-forward and both KEEP paths are run on the
books themselves.  RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py are NOT touched.

SURVIVORSHIP (rule 9): U56 and B136 are CURRENT-CONSTITUENT panels; every CAGR/Sharpe level
below is optimistic and every 4a/4b count is an UPPER bound.  The ERR/sleeve measurements are
within-book on one tape and the bias very largely cancels out of them.
"""
import hashlib
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa: E402

SLUG = "2026-09-16_is-the-lam-LINEARITY-of-TURNOVER-assumed-anywhere-ELSE-in-the-record_cloud"
OUT = ROOT / "research" / "backtests"
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ---------------------------------------------------------------- frozen construction
COST = 10.0          # bps, PROTOCOL rule 2
GROSS = 0.75         # incumbent book gross
MAXVOL = 0.60
FREQ = "W"
SEEDS = 20           # 1071's committed seed count
BISECT = 34
WARM = 260           # baseline.compare()'s warm-up skip: no metric is read before this
N_LADDER = [5, 10, 20, 40]
LAM_LADDER = [0.25, 0.50, 0.75, 1.25, 1.50, 2.00]   # coordinate set, published in full
TOLS = [0.005, 0.010, 0.020, 0.050]                 # D2
IS_END, OOS_START = "2016-12-31", "2017-01-01"      # PROTOCOL rule 8


def W(name, df):
    p = OUT / f"{SLUG}.{name}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def mdseed(*parts):
    return int(hashlib.md5("|".join(str(x) for x in parts).encode()).hexdigest()[:8], 16)


# ---------------------------------------------------------------- fast runner (1097/1106 verbatim)
def nrun(rets, wt, mk):
    T, N = rets.shape
    mk = mk.copy(); mk[0] = True
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
    return (held * rets).sum(axis=1), turn


def gross_rescaler(rets, wt, mk):
    """f(lam) -> NET returns of the book REBUILT at gross lam*g, and the realised turnover
    path.  NOTE (1106, and the object of this run): that path is NOT exactly lam * the lam=1
    path — the cash sleeve inside V_p does not scale.  Also returns the per-rebalance cash
    sleeve (S_p - W_sp), which the closed form names as the driver of the error."""
    T, N = rets.shape
    mk = mk.copy(); mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    A = wt[s0] * (Cp / Cp[s0])
    AR = (A * rets).sum(axis=1)
    S = A.sum(axis=1)
    Wsum = wt[s0].sum(axis=1)
    s0p = reb[np.maximum(seg - 1, 0)]
    Ap = (wt[s0p] * (Cp / Cp[s0p]))[reb]
    Sp = Ap.sum(axis=1)
    Wsp = wt[s0p].sum(axis=1)[reb]
    Ap[0] = 0.0; Sp[0] = 0.0; Wsp[0] = 0.0
    Wr = wt[reb]
    c = COST / 1e4
    sleeve = Sp - Wsp                     # the term that does NOT scale with lam

    def f(lam, want_turn=False):
        V = 1.0 + lam * (S - Wsum)
        g = lam * AR / V
        Vp = 1.0 + lam * sleeve
        tr = lam * np.abs(Wr - Ap / Vp[:, None]).sum(axis=1)
        out = g.copy()
        out[reb] -= tr * c
        if want_turn:
            tpath = np.zeros(T)
            tpath[reb] = tr
            return out, tpath
        return out

    return f, reb, sleeve


def fmet(r):
    r = np.asarray(r, float)
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def lam_rebuilt(f, sl, target_dd, it=BISECT):
    """Smallest lam in (0, 4] whose REBUILT book matches target_dd on slice sl."""
    lo, hi = 1e-6, 4.0

    def dd_at(l):
        return fmet(f(l)[sl])[2]

    if dd_at(hi) > target_dd:
        return None
    for _ in range(it):
        mid = 0.5 * (lo + hi)
        if dd_at(mid) > target_dd:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------- books
LAG = 1


def lagmat(a):
    """Weights decided at close t are applied at t+1 (PROTOCOL rule 2)."""
    out = np.zeros_like(a)
    out[LAG:] = a[:-LAG]
    return out


def _topn(key, n, gross):
    """Exactly n names, ties broken by column order ('first'), equal weight gross/n."""
    rank = key.rank(axis=1, ascending=False, method="first")
    return (rank <= n).astype(float) * (gross / n)


def book_weights(px, n, gross=GROSS, max_vol=MAXVOL):
    """The incumbent composite, equal-weighted at gross/n over the top n (CAND20 legs)."""
    s, above, vol20 = score(px, vol_scale=True)
    return _topn(s.where(above & (vol20 < max_vol)), n, gross)


def null_weights(px, n, seed, gate, gross=GROSS, max_vol=MAXVOL):
    """RANDOM ordering of the SAME eligibility set.  gate='OPEN' -> all priced names eligible
    (1071/1082/1086's convention); gate='ELIG' -> the book's own 200d/vol gate."""
    _, above, vol20 = score(px, vol_scale=True)
    rng = np.random.default_rng(seed)
    R = pd.DataFrame(rng.random(px.shape), index=px.index, columns=px.columns)
    ok = px.notna() if gate == "OPEN" else (above & (vol20 < max_vol) & px.notna())
    return _topn(R.where(ok), n, gross)


def prep(px):
    """Returns, and the LAGGED weekly rebalance mask the engine uses."""
    rets = px.pct_change().fillna(0.0)
    key = pd.Series(px.index.to_period("W"), index=px.index)
    mk = (key != key.shift(-1)).values
    return rets, np.roll(mk, LAG)


# ================================================================= PART A — CENSUS
LAM_TOKEN = re.compile(r"\blam(?:_[a-z0-9_]+)?\b")
TCD = r"(?:turn(?:over)?|nturn|tover|cost|drag|tpath|tr)"
SHORTCUT = [
    re.compile(rf"[A-Za-z_]*{TCD}[A-Za-z_0-9]*\s*/\s*lam\b", re.I),
    re.compile(rf"\blam(?:_[a-z0-9_]+)?\s*\*\s*[A-Za-z_]*{TCD}[A-Za-z_0-9]*", re.I),
    re.compile(rf"[A-Za-z_]*{TCD}[A-Za-z_0-9]*\s*\*\s*lam\b", re.I),
    re.compile(rf"\blam(?:_[a-z0-9_]+)?\s*/\s*[A-Za-z_]*{TCD}[A-Za-z_0-9]*", re.I),
]
BUILDS_LAM = [
    re.compile(r"def\s+lam_[a-z_]+", re.I),
    re.compile(r"\blam\s*=\s*lam_[a-z_]+\s*\(", re.I),
    re.compile(r"gross_rescaler", re.I),
    re.compile(r"DD[- _]?match", re.I),
]
REPORTS_TCD = re.compile(rf"\b{TCD}\b", re.I)
LINEARITY_ASSERTION = re.compile(
    r"exactly\s+lam\s*\*|is\s+exactly\s+`?lam|linear\s+in\s+lam", re.I)


def census():
    P("\n" + "=" * 96)
    P("PART A — CENSUS of the committed record (D1: CLAIM SET)")
    P("=" * 96)
    # THIS script is excluded from its own census: it quotes the shortcut in its regexes and
    # its docstring, so including it would count the auditor as a member of the audited set.
    files = [f for f in sorted((ROOT / "research" / "backtests").glob("*.py"))
             if f.stem != SLUG]
    P(f"  (self-excluded from the census: {SLUG}.py)")
    rows = []
    for f in files:
        try:
            src = f.read_text(errors="replace")
        except Exception:
            continue
        # strip python's own `lambda` keyword so it cannot masquerade as the DD-match lam
        src_nl = re.sub(r"\blambda\b", "__PYLAMBDA__", src)
        builds = any(p.search(src_nl) for p in BUILDS_LAM)
        hits = []
        for p in SHORTCUT:
            for m in p.finditer(src_nl):
                hits.append(m.group(0).strip())
        reports = bool(REPORTS_TCD.search(src_nl))
        asserts_lin = bool(LINEARITY_ASSERTION.search(src_nl))
        strict = bool(hits) and builds
        wide = strict or (builds and reports)
        rows.append(dict(file=f.name, mentions_lam=bool(LAM_TOKEN.search(src_nl)),
                         builds_lam=builds, reports_tcd=reports,
                         n_shortcut_hits=len(hits), asserts_linearity=asserts_lin,
                         STRICT=strict, WIDE=wide,
                         example_hit=(hits[0][:60] if hits else "")))
    df = pd.DataFrame(rows)
    P(f"  committed scripts scanned                     : {len(df):,}")
    P(f"  mention a bare DD-match `lam` token           : {int(df.mentions_lam.sum()):,}")
    P(f"  BUILD a DD-match lambda                       : {int(df.builds_lam.sum()):,}")
    P(f"  build a lambda AND report turnover/cost/drag  : {int((df.builds_lam & df.reports_tcd).sum()):,}")
    P(f"  D1 = STRICT  (shortcut arithmetic written)    : {int(df.STRICT.sum()):,}")
    P(f"  D1 = WIDE    (STRICT + exposed-by-assumption) : {int(df.WIDE.sum()):,}")
    P(f"  assert lam-LINEARITY in prose/docstring       : {int(df.asserts_linearity.sum()):,}")
    P("\n  STRICT members (every one, with the first matching expression):")
    for _, r in df[df.STRICT].iterrows():
        P(f"    - {r.file}")
        P(f"        hits={r.n_shortcut_hits}  e.g. `{r.example_hit}`  asserts_linearity={r.asserts_linearity}")
    P("\n  WIDE-but-not-STRICT members (exposed only if a reader divides):")
    wn = df[df.WIDE & ~df.STRICT]
    for _, r in wn.iterrows():
        P(f"    - {r.file}  (asserts_linearity={r.asserts_linearity})")
    W("census", df)
    return df


# ================================================================= PART B — RE-PRICE
def reprice():
    P("\n" + "=" * 96)
    P("PART B — RE-PRICE: how big is the lam-linearity error, and what drives it")
    P("=" * 96)
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    rows, wf_rows = [], []
    sl = slice(WARM, None)
    for pname, px in panels.items():
        rets_df, mk = prep(px)
        rets = rets_df.values
        idx = px.index
        yrs = (len(idx) - WARM) / 252.0
        for n in N_LADDER:
            bw = lagmat(book_weights(px, n).reindex(
                index=idx, columns=px.columns).fillna(0.0).values)
            br_g, bt = nrun(rets, bw, mk)
            br = br_g - bt * COST / 1e4                       # NET, as the engine charges it
            b_cagr, b_sh, b_dd = fmet(br[sl])
            fb, reb_b, sleeve_b = gross_rescaler(rets, bw, mk)

            # --- B1: the BOOK itself down a published lam ladder (no choosing, all rungs)
            _, t1 = fb(1.0, want_turn=True)
            raw_book = t1[sl].sum() / yrs
            peak_book = float(t1[sl].max())
            for lam in LAM_LADDER:
                _, tl = fb(lam, want_turn=True)
                recov = (tl[sl].sum() / lam) / yrs
                err = recov - raw_book
                rows.append(dict(arm="BOOK_LADDER", panel=pname, n=n, gate="", seed=-1,
                                 lam=lam, NTURN_raw=raw_book, NTURN_matched=tl[sl].sum() / yrs,
                                 NTURN_recov=recov, ERR=err,
                                 ERR_rel_raw=err / raw_book if raw_book else np.nan,
                                 ERR_rel_peak=err / peak_book if peak_book else np.nan,
                                 sleeve_mean=float(sleeve_b.mean()),
                                 sleeve_absmax=float(np.abs(sleeve_b).max()),
                                 peak_reb_turn=peak_book))

            # --- B2: the DD-MATCHED NULLS, the object 1106 actually mis-recovered
            for gate in ("OPEN", "ELIG"):
                for s in range(SEEDS):
                    sd = mdseed(pname, n, gate, s, "1111")
                    nw = lagmat(null_weights(px, n, sd, gate).reindex(
                        index=idx, columns=px.columns).fillna(0.0).values)
                    fn, reb_n, sleeve_n = gross_rescaler(rets, nw, mk)
                    lam = lam_rebuilt(fn, sl, b_dd)
                    if lam is None:
                        lam = 1.0
                    _, tm = fn(lam, want_turn=True)
                    _, tr1 = fn(1.0, want_turn=True)
                    raw = tr1[sl].sum() / yrs
                    matched = tm[sl].sum() / yrs
                    recov = matched / lam
                    err = recov - raw
                    peak = float(tr1[sl].max())
                    rows.append(dict(arm="NULL_DDMATCH", panel=pname, n=n, gate=gate, seed=s,
                                     lam=lam, NTURN_raw=raw, NTURN_matched=matched,
                                     NTURN_recov=recov, ERR=err,
                                     ERR_rel_raw=err / raw if raw else np.nan,
                                     ERR_rel_peak=err / peak if peak else np.nan,
                                     sleeve_mean=float(sleeve_n.mean()),
                                     sleeve_absmax=float(np.abs(sleeve_n).max()),
                                     peak_reb_turn=peak))

            # --- rule-8 legs for this cell, IS / OOS / halves (post-warm-up, as compare() does)
            sr = pd.Series(br, index=idx).iloc[WARM:]
            is_m = fmet(sr.loc[:IS_END].values)
            oos_m = fmet(sr.loc[OOS_START:].values)
            h = len(sr) // 2
            h1, h2 = fmet(sr.iloc[:h].values), fmet(sr.iloc[h:].values)
            wf_rows.append(dict(panel=pname, n=n, full_CAGR=b_cagr, full_Sharpe=b_sh,
                                full_MaxDD=b_dd, H1_Sharpe=h1[1], H2_Sharpe=h2[1],
                                IS_CAGR=is_m[0], IS_Sharpe=is_m[1], IS_MaxDD=is_m[2],
                                OOS_CAGR=oos_m[0], OOS_Sharpe=oos_m[1], OOS_MaxDD=oos_m[2],
                                NTURN=bt.sum() / yrs))
            P(f"  {pname:5s} n={n:<3d} book CAGR {b_cagr:7.2%} Sharpe {b_sh:6.4f} "
              f"MaxDD {b_dd:7.2%}  turn {bt.sum()/yrs:6.2f}/yr")
    df = pd.DataFrame(rows)
    W("reprice", df)
    return df, pd.DataFrame(wf_rows), panels


# ================================================================= PART C — GATES
def gates(panels):
    P("\n" + "=" * 96)
    P("GATES (printed BEFORE any result number)")
    P("=" * 96)
    g = {}
    px = panels["U56"]
    rets_df, mk = prep(px)
    rets = rets_df.values
    bw_raw = book_weights(px, 20)
    bw = lagmat(bw_raw.reindex(index=px.index, columns=px.columns).fillna(0.0).values)

    # G1 fast runner == engine.backtest (the engine applies the same LAG internally)
    sys.path.insert(0, str(ROOT / "products" / "backtester"))
    from engine import backtest  # noqa: E402
    eng = backtest(px, bw_raw, cost_bps=COST, freq=FREQ)
    r_fast, t_fast = nrun(rets, bw, mk)
    r_net = r_fast - t_fast * COST / 1e4
    # engine.backtest emits NaN on its opening rows (weights are fillna'd BEFORE .shift(1), so
    # row 0's target is NaN and the seeding turnover is NaN with it).  Every metric in this run
    # is read post-warm-up, so the reproduction gate is read there too; the NaN count is
    # published rather than skipped past.
    nan_eng = int(eng["returns"].isna().sum())
    d1 = float(np.abs(r_net[WARM:] - eng["returns"].values[WARM:]).max())
    g["G1 fast runner NET returns == engine.backtest (post-warm-up)"] = (d1, d1 < 1e-12)
    d1b = float(np.abs(t_fast[WARM:] - eng["turnover"].values[WARM:]).max())
    g["G1b fast runner turnover == engine.backtest (post-warm-up)"] = (d1b, d1b < 1e-12)
    g["G1e engine.backtest NaN rows, all inside the warm-up (MEASURED)"] = (
        nan_eng, nan_eng < WARM)

    # G1c rescaler at lam=1 == fast runner (both NET)
    f, reb, sleeve = gross_rescaler(rets, bw, mk)
    r1, t1 = f(1.0, want_turn=True)
    d1c = float(np.abs(r1 - r_net).max())
    g["G1c rescaler(lam=1) NET returns == fast runner"] = (d1c, d1c < 1e-12)
    d1d = float(np.abs(t1 - t_fast).max())
    g["G1d rescaler(lam=1) turnover == fast runner"] = (d1d, d1d < 1e-12)

    # G2 the linearity DEFECT is REAL and is exactly the cash sleeve (closed form)
    lam = 1.7
    _, tl = f(lam, want_turn=True)
    err_path = np.abs(tl[reb] / lam - t1[reb])
    g["G2 turnover is NOT exactly linear in lam (defect reproduced)"] = (
        float(err_path.max()), float(err_path.max()) > 1e-10)
    # closed form: error vanishes iff sleeve == 0
    zero_sleeve = float(np.abs(sleeve).max())
    g["G2b the non-scaling term is the cash sleeve (|S_p - W_sp|_max > 0)"] = (
        zero_sleeve, zero_sleeve > 1e-10)

    # G3 SPY benchmark, post-warm-up (the window every metric below is read on)
    spy = px["SPY"].pct_change().fillna(0.0)
    sm = fmet(spy.values[WARM:])
    g["G3 SPY post-warm-up CAGR (context, not a pass/fail)"] = (sm[0], True)

    # G4 live RULES v2 MaxDD reproduces the record's -12.05%
    v2 = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)
    v2m = fmet(v2["returns"].iloc[WARM:].values)
    g["G4 live RULES v2 MaxDD == record's -12.05%"] = (v2m[2], abs(v2m[2] + 0.1205) < 5e-4)

    # G5 every book runs at gross 0.75 exactly (method='first' ranking, no tie inflation)
    gm = float(bw.sum(axis=1).max())
    g["G5 book gross == 0.75"] = (gm, abs(gm - GROSS) < 1e-12)

    npass = 0
    for k, (v, ok) in g.items():
        P(f"  [{'PASS' if ok else 'FAIL'}] {k}: {v:.6g}")
        npass += bool(ok)
    P(f"  GATES {npass} of {len(g)} PASS")
    return g, v2m, sm


# ================================================================= PART D — ANSWER
def answer(cen, rep, wf, panels, v2m, spym):
    P("\n" + "=" * 96)
    P("PART D — THE ANSWER (all 8 D1 x D2 grid points)")
    P("=" * 96)
    nulls = rep[rep.arm == "NULL_DDMATCH"]
    ladder = rep[rep.arm == "BOOK_LADDER"]

    P(f"\n  RE-PRICED CELLS: {len(nulls):,} DD-matched nulls + {len(ladder):,} book-ladder points")
    for lab, sub in (("DD-MATCHED NULLS", nulls), ("BOOK lam LADDER", ladder)):
        e = sub.ERR_rel_peak.dropna()
        er = sub.ERR_rel_raw.dropna()
        P(f"\n  {lab}")
        P(f"    ERR (turns/yr)          median {sub.ERR.median():+.6f}  "
          f"range [{sub.ERR.min():+.6f}, {sub.ERR.max():+.6f}]")
        P(f"    ERR / NTURN_raw         median {er.median():+.4%}  "
          f"range [{er.min():+.4%}, {er.max():+.4%}]")
        P(f"    |ERR| / PEAK reb turn   median {e.abs().median():.4%}  max {e.abs().max():.4%}")
        P(f"    sign: {int((sub.ERR > 0).sum())} positive / {int((sub.ERR < 0).sum())} negative "
          f"of {len(sub)}")
        P(f"    lam range               [{sub.lam.min():.4f}, {sub.lam.max():.4f}]")

    # D2 tolerance grid, both claim sets
    P("\n  D1 x D2 GRID — cells flagged MATERIALLY WRONG (|ERR| / peak reb turnover > tol):")
    P(f"    {'claim set':<10s} {'tol':>6s} {'n_scripts':>10s} {'n_cells':>9s} {'flagged':>9s} {'share':>8s}")
    grid = []
    for cs in ("STRICT", "WIDE"):
        nsc = int(cen[cs].sum())
        for tol in TOLS:
            fl = int((nulls.ERR_rel_peak.abs() > tol).sum())
            grid.append(dict(claim_set=cs, tolerance=tol, n_scripts=nsc, n_cells=len(nulls),
                             n_flagged=fl, share_flagged=fl / len(nulls),
                             scripts_at_risk=nsc if fl else 0))
            P(f"    {cs:<10s} {tol:>6.1%} {nsc:>10d} {len(nulls):>9d} {fl:>9d} "
              f"{fl/len(nulls):>8.1%}")
    W("grid", pd.DataFrame(grid))

    # mechanism
    rho = nulls[["ERR", "sleeve_absmax"]].assign(a=nulls.ERR.abs()).corr(method="spearman").loc["a", "sleeve_absmax"]
    rho_lam = nulls.assign(a=nulls.ERR.abs())[["a", "lam"]].corr(method="spearman").loc["a", "lam"]
    P(f"\n  MECHANISM  Spearman(|ERR|, |cash sleeve|_max) = {rho:+.4f}")
    P(f"             Spearman(|ERR|, lam)                = {rho_lam:+.4f}")
    P(f"             mean |1 - lam| over the matched nulls = {float((1-nulls.lam).abs().mean()):.4f}")

    # cost translation
    P("\n  WHAT THE ERROR IS WORTH, in bps/yr of charged cost:")
    for bps in (10, 25, 50):
        v = nulls.ERR.abs().median() * bps
        vm = nulls.ERR.abs().max() * bps
        P(f"    at {bps:>2d} bps: median {v:7.3f} bps/yr, max {vm:7.3f} bps/yr")

    # hypotheses
    P("\n  HYPOTHESES (declared before any number):")
    H = {}
    strict_other = [f for f in cen[cen.STRICT].file if "U56-H21-SIGN-FLIP" not in f]
    H["H_EXPOSED  STRICT non-empty beyond 1106 itself"] = len(strict_other) > 0
    H["H_WIDE     WIDE covers >= 10 committed scripts"] = int(cen.WIDE.sum()) >= 10
    med = float(nulls.ERR_rel_peak.abs().median())
    H["H_SIZE     median |ERR|/peak in [0.5%, 5%]"] = 0.005 <= med <= 0.05
    H["H_SLEEVE   Spearman(|ERR|, sleeve) >= +0.5"] = bool(rho >= 0.5)
    H["H_SIGN     ERR has a constant sign across the grid"] = bool(
        (nulls.ERR > 0).all() or (nulls.ERR < 0).all())
    H["H_MATERIAL majority of cells flagged at tol = 1%"] = bool(
        (nulls.ERR_rel_peak.abs() > 0.01).mean() > 0.5)
    for k, v in H.items():
        P(f"    [{'PASS' if v else 'FAIL'}] {k}")
    P(f"    HYPOTHESES {sum(H.values())} of {len(H)} PASS")
    W("hypotheses", pd.DataFrame([dict(hypothesis=k, verdict="PASS" if v else "FAIL")
                                  for k, v in H.items()]))
    return H, med, rho


# ================================================================= PART E — RULE 8 + KEEP
def rule8(wf, panels, v2m, spym):
    P("\n" + "=" * 96)
    P("PART E — RULE 8 WALK-FORWARD and BOTH KEEP PATHS")
    P("=" * 96)
    bench = {}
    for pname, px in panels.items():
        spy = px["SPY"].pct_change().fillna(0.0).iloc[WARM:]
        h = len(spy) // 2
        bench[pname] = dict(
            full=fmet(spy.values), IS=fmet(spy.loc[:IS_END].values),
            OOS=fmet(spy.loc[OOS_START:].values),
            H1=fmet(spy.iloc[:h].values), H2=fmet(spy.iloc[h:].values))
        b = bench[pname]
        P(f"  SPY on {pname:5s}: full {b['full'][0]:7.2%} / {b['full'][1]:.4f} / {b['full'][2]:7.2%}"
          f"   OOS {b['OOS'][0]:7.2%} / {b['OOS'][1]:.4f} / {b['OOS'][2]:7.2%}"
          f"   halves {b['H1'][1]:.4f} / {b['H2'][1]:.4f}")
    P(f"  RULES v2 (live baseline, U56, post-warmup): CAGR {v2m[0]:.2%} Sharpe {v2m[1]:.4f} "
      f"MaxDD {v2m[2]:.2%}")

    rows = []
    for _, r in wf.iterrows():
        b = bench[r.panel]
        # 4b legs, full sample and OOS, judged against SPY on the SAME panel
        L_H1 = r.H1_Sharpe > b["H1"][1]
        L_H2 = r.H2_Sharpe > b["H2"][1]
        L_OOS = r.OOS_Sharpe > b["OOS"][1]
        L_DD = r.full_MaxDD >= 0.60 * b["full"][2]          # both negative: >= is "shallower"
        L_CAGR = r.full_CAGR >= 0.70 * b["full"][0]
        p4b = bool(L_H1 and L_H2 and L_OOS and L_DD and L_CAGR)
        L_DD_o = r.OOS_MaxDD >= 0.60 * b["OOS"][2]
        L_CAGR_o = r.OOS_CAGR >= 0.70 * b["OOS"][0]
        p4b_oos = bool(L_OOS and L_DD_o and L_CAGR_o)
        # 4a, judged against the LIVE book
        p4a = bool(r.H1_Sharpe > v2m[1] and r.H2_Sharpe > v2m[1] and r.full_MaxDD >= v2m[2])
        rows.append(dict(panel=r.panel, n=int(r.n), full_CAGR=r.full_CAGR,
                         full_Sharpe=r.full_Sharpe, full_MaxDD=r.full_MaxDD,
                         H1=r.H1_Sharpe, H2=r.H2_Sharpe, IS_Sharpe=r.IS_Sharpe,
                         OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                         L_H1=L_H1, L_H2=L_H2, L_OOS=L_OOS, L_DD=L_DD, L_CAGR=L_CAGR,
                         PASS_4b=p4b, PASS_4b_OOS=p4b_oos, PASS_4a=p4a))
    wfd = pd.DataFrame(rows)
    P("\n  ALL GRID POINTS (no cell hidden):")
    P(f"    {'panel':<6s}{'n':>4s} {'fullCAGR':>9s} {'fullShp':>8s} {'fullDD':>8s} "
      f"{'H1':>7s} {'H2':>7s} {'oosCAGR':>9s} {'oosShp':>7s} {'oosDD':>8s} {'4a':>4s} {'4b':>4s} {'4bOOS':>6s}")
    for _, r in wfd.iterrows():
        P(f"    {r.panel:<6s}{r.n:>4d} {r.full_CAGR:>9.2%} {r.full_Sharpe:>8.4f} "
          f"{r.full_MaxDD:>8.2%} {r.H1:>7.4f} {r.H2:>7.4f} {r.OOS_CAGR:>9.2%} "
          f"{r.OOS_Sharpe:>7.4f} {r.OOS_MaxDD:>8.2%} {str(r.PASS_4a):>4s} "
          f"{str(r.PASS_4b):>4s} {str(r.PASS_4b_OOS):>6s}")

    P("\n  RULE 8 CHOOSERS (declared in advance; choose on IS 2009-2016, read OOS ONCE):")
    for pname in wfd.panel.unique():
        sub = wfd[wfd.panel == pname]
        b = bench[pname]
        for cname, col in (("C_SHARPE", "IS_Sharpe"), ("C_CAGR", "full_CAGR")):
            pick = sub.loc[sub[col].idxmax()]
            P(f"    {pname:5s} {cname:9s} picks n={int(pick.n):<3d} -> OOS "
              f"{pick.OOS_CAGR:7.2%} / {pick.OOS_Sharpe:.4f} / {pick.OOS_MaxDD:7.2%}  "
              f"vs SPY OOS {b['OOS'][0]:7.2%} / {b['OOS'][1]:.4f} / {b['OOS'][2]:7.2%}  "
              f"-> 4b OOS {'PASS' if pick.PASS_4b_OOS else 'FAIL'}")
    P(f"\n  4a: {int(wfd.PASS_4a.sum())} of {len(wfd)}   "
      f"4b full: {int(wfd.PASS_4b.sum())} of {len(wfd)}   "
      f"4b OOS: {int(wfd.PASS_4b_OOS.sum())} of {len(wfd)}")
    for leg in ("L_CAGR", "L_H1", "L_H2", "L_OOS", "L_DD"):
        P(f"    {leg:7s} {int(wfd[leg].sum()):>2d} of {len(wfd)}")
    W("walkforward", wfd)
    return wfd


def main():
    pd.set_option("display.width", 200)
    P(f"# {SLUG}")
    P(f"# COST {COST} bps | GROSS {GROSS} | FREQ {FREQ} | SEEDS {SEEDS} | BISECT {BISECT}")
    P(f"# N ladder {N_LADDER} | lam ladder {LAM_LADDER} | tolerances {TOLS}")
    panels_probe = {"U56": load_universe(), "B136": load_universe(broad=True)}
    g, v2m, spym = gates(panels_probe)
    cen = census()
    rep, wf, panels = reprice()
    H, med, rho = answer(cen, rep, wf, panels, v2m, spym)
    wfd = rule8(wf, panels, v2m, spym)
    (OUT / f"{SLUG}.console.txt").write_text("\n".join(LOG))
    P(f"\nwrote {SLUG}.console.txt")


if __name__ == "__main__":
    main()
