#!/usr/bin/env python3
"""Idea 688 - "is-WIDTH-MAXIMISATION-a-general-rule-8-selector-pathology" (lane C, 2026-09-11).

The question
------------
Idea 685 (lane C, committed) extended idea 525's (q, k) panel ladder from 2.5x of width to
10.0x and found exactly one rule-8 selector that the extension moved:

    EBAR-MAX takes the widest panel on 5 of 5 book sizes (k: 100 -> 400) and pays
    -0.1685 of OOS Sharpe and +3.24pp of OOS MaxDD for it; EBAR-MIN, BREADTH-MAX,
    BREADTH-MIN and IS-SHARPE-MAX are unmoved (0.0000 on all five book sizes).

Its stated mechanism was mechanical, not empirical: Ebar (the mean count of eligible names)
is an **extensive** statistic - it is a SUM over panel members - so on a choice set whose
members differ in width, argmax Ebar is argmax k up to a breadth factor that barely moves.
Nothing in that argument is about Ebar.  It applies to ANY criterion that counts instead of
averaging.  Idea 688 asks whether the record's other MAX-form selectors carry the same
defect, i.e. **which of them are extensive statistics in disguise.**

The design - matched normalisation pairs on a single-pool width ladder
---------------------------------------------------------------------
The test has to separate "this criterion tracks width because width is genuinely better"
from "this criterion tracks width because it forgot to divide by k".  Two devices do that:

1.  **A NULL ladder.**  Cap mix is held at q = 1.00, so every panel at every width is an
    i.i.d. uniform draw of columns from ONE pool (SMALL439).  No width level is genuinely
    better than another: the panels are exchangeable up to their size.  A selector whose
    argmax concentrates on one end of the width axis under this null is pinning on width
    mechanically.  (q = 1.00 is FORCED, not tuned: only q >= 0.75 can reach k = 400 at all
    - see idea 685's envelope - and q = 1.00 is the single case in which every panel comes
    from one pool, which is what makes the exchangeability null exact.)

2.  **MATCHED PAIRS.**  Five criteria are tested against their own k-normalised twin, where
    the twin is *literally the same number divided by k*:

        C_Ebar   = mean_t  n_elig(t)          I_breadth  = C_Ebar  / k
        C_Emed   = med_t   n_elig(t)          I_bmed     = C_Emed  / k
        C_Emax   = max_t   n_elig(t)          I_bmax     = C_Emax  / k
        C_Esd    = sd_t    n_elig(t)          I_bsd      = C_Esd   / k
        C_cover  = # names EVER eligible      I_cover    = C_cover / k

    Within a pair the two selectors see the same information and differ ONLY by the
    normalisation.  If the extensive member pins to a width end and the intensive twin does
    not, the pathology IS the missing division - there is no other candidate explanation
    left standing.

    Plus, from the record's own selector population: IS-SHARPE-MAX (the record's dominant
    pick criterion, 1100 idxmax/idxmin sites, overwhelmingly IS_Sharpe), EWSHARPE-MAX,
    SELECTIVITY-MAX (20/Ebar_IS - INVERSE-extensive, predicted to pin to the NARROW end),
    the MIN forms EBAR-MIN / BREADTH-MIN (idea 685's own pair), and two calibration
    controls: **K-MAX** (criterion = k itself; must pin at 1.000 by construction - a
    positive control that proves the measurement works) and **RANDOM** (a seeded uniform
    criterion; a negative control that measures the test's own false-positive rate).

Tuned parameters (PROTOCOL rule 4: at most two) - ALL grid points reported
    1. SELECTOR SET:  16 selectors, listed above and in SELECTORS below.  Every one is
       reported on every ceiling; none is dropped after the fact.
    2. CHOICE-SET WIDTH: the ceiling C, choice set = {k in KS : k <= C}, for
       C in {60, 80, 100, 200, 400} = {1.5x, 2.0x, 2.5x, 5.0x, 10.0x} of width.
       C = 100 is lane B's published ceiling; C = 400 is idea 685's.
    Everything else is inherited from the record and not chosen here: the RULES v1 gate
    (idea 276), CAND-n / EWall / ADAPT books (idea 286), GROSS = 0.75, weekly cadence,
    10 bps, next-day execution, the 260-day warm-up skip, NS_LAD = {5,10,15,20,30},
    IS = ..2016-12-31, OOS = 2017-01-01.. .  N_DRAWS is raised from lane B's 3 to 8 purely
    for the resolution of a rate statistic (8 independent draws per width instead of 3);
    no verdict is a function of that choice and the per-draw picks are all published.

PRE-REGISTERED BARS (fixed here before any number in this run was read)
----------------------------------------------------------------------
    EXTENSIVITY EXPONENT b = OLS slope of log|C| on log k over all panels.
        b >= +0.70              -> EXTENSIVE      (criterion scales with width)
        |b| <= 0.15             -> INTENSIVE      (criterion is width-free)
        b <= -0.70              -> INVERSE-EXTENSIVE
        otherwise               -> MIXED
    WIDTH-PIN RATE p = share of independent draws on which the selector's pick sits at the
    CEILING (for MAX forms) or at the FLOOR (for MIN forms) of the choice set, at C = 400.
        p >= 0.80               -> WIDTH-PINNED
        p inside the two-sided 95% exact-binomial band of 1/|K|  -> WIDTH-NEUTRAL
        otherwise               -> WIDTH-LEANING
    A selector is **EXTENSIVE IN DISGUISE** iff it is WIDTH-PINNED and |b| >= 0.70 and it is
    not the K-MAX positive control.  The PRICE of the pathology is the pre-registered
    quantity  dOOS = OOS Sharpe(pick | C = 400) - OOS Sharpe(pick | C = 100), averaged over
    draws and book sizes, reported for every selector whether or not it is pinned.

Gates, asserted before any new number is read
    G0  REPRODUCTION.  The k <= 100 draws replay lane B's rng sequence (seed 2026, its full
        QS x KS x N_DRAWS loop in its own order, so the generator state matches at every
        cell) and the k in {200, 400} draws replay idea 685's second generator (seed 685,
        its own loop order including the cells skipped by the envelope test, which consume
        nothing).  The q = 1.00 subset is re-measured from scratch and asserted against BOTH
        committed .panels.csv / .stats.csv files at 1e-9 on Ebar, breadth, Emed, Ebar_IS,
        breadth_IS and on S1..S5, EW_Sharpe, EW_OOS_Sharpe, ADAPT_Sharpe, best_prem.
    G1  k-IDENTITY: max |k * breadth - Ebar| over all panels, asserted < 1e-9.
    G2  PAIR IDENTITY: every intensive twin equals its extensive partner / k, asserted
        < 1e-12.  This is what makes "the pair differs only by the normalisation" a checked
        fact rather than a claim about the source code.
    G3  ENVELOPE: exact width, exact cap mix, no duplicate columns, inside the pool bounds.

Rule 8 walk-forward (PROTOCOL rule 8, required)
    Every criterion is measured on the IS window (..2016-12-31) ONLY - the panel measures
    from the IS slice of the weekly gate matrix, the book criteria from full_row's IS_Sharpe.
    Each selector picks one panel per (book size n, ceiling C); that pick is then read once
    on 2017-01-01.. untouched, and reported as OOS CAGR / Sharpe / MaxDD against the
    do-nothing anchor (the choice-set mean), against RULES v2 on the same panel, and against
    SPY.  Both KEEP paths are evaluated on every book row in .books.csv.

CENSUS (what the tested set is drawn from)
    The record's committed backtests are scanned for MAX-form rule-8 selector sites and each
    distinct criterion token is classified by a DECLARED lexicon (count-form vs rate-form vs
    unclassified).  The census is descriptive - it says how much of the record's selector
    population sits in the family this run prices - and no verdict is taken from it.

SURVIVORSHIP (idea 54, data/SMALL_PANEL_README.md): SMALL439 is CURRENT constituents of its
screen, so every level here is optimistic.  q = 1.00 makes this ladder entirely small-cap,
which is the most exposed corner of the record's panels.  The object under test is whether a
SELECTOR pins on a panel COORDINATE; survivorship moves the level of every panel in the
choice set together and so cannot manufacture or hide an argmax concentration.  No arm here
is a new BOOK - CAND-n and EWall are the record's existing books re-run on re-drawn panels -
so a 4a/4b pass would be a statement about the panel, not a capital candidate.

Outputs: .panels.csv .stats.csv .books.csv .census.csv .extensivity.csv .picks.csv
         .walkforward.csv .console.txt .result.md
"""
import importlib.util, math, re, sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import rebalance_mask              # noqa

OUT = Path(__file__).with_suffix("")
BT = ROOT / "research" / "backtests"
LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)

COST, FREQ, GROSS = 10, "W", 0.75
IS_END, OOS_START = "2016-12-31", "2017-01-01"

# ---- this run's grid (2 tuned params) -------------------------------------------------
Q_FIXED = 1.00                                  # FORCED by the envelope, not tuned
KS      = [40, 60, 80, 100, 200, 400]
CEILS   = [60, 80, 100, 200, 400]               # param 2: choice-set width
NS_LAD  = [5, 10, 15, 20, 30]
N_DRAWS = 8
SEED_B, SEED_685, SEED_NEW = 2026, 685, 688
BAR_EXT, BAR_INT, BAR_PIN = 0.70, 0.15, 0.80    # pre-registered

# ---------------------------------------------------------------- import the record
def _load(p, name):
    spec = importlib.util.spec_from_file_location(name, str(p))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

M276 = _load(BT / "2026-09-06_is-breadth-a-small-cap-dummy-everywhere-in-the-record_cloud.py", "idea276")
M286 = _load(BT / "2026-09-09_price-the-14-breadth-files-on-their-own-books_B.py", "idea286")
P525 = BT / "2026-09-11_is-n_elig-the-variable-the-record-keeps-mislabelling_B"
M525 = _load(f"{P525}.py", "idea525")
P685 = BT / "2026-09-11_extend-the-q-x-k-ladder-past-k-EQUALS-100_C"
M685 = _load(f"{P685}.py", "idea685")

spearman = M286.spearman
panel_measures, do_panel = M525.panel_measures, M525.do_panel
SCOLS = M525.SCOLS
QS_B, KS_B, NDRAWS_B = M525.QS, M525.KS, M525.N_DRAWS
QS_685, KS_685, ND_685 = M685.QS, M685.KS, M685.N_DRAWS


# ---------------------------------------------------------------- the selector set (param 1)
# (criterion column, MAX?, declared family, matched twin)
SELECTORS = {
    "EBAR-MAX":        ("C_Ebar",    True,  "extensive",  "BREADTH-MAX"),
    "BREADTH-MAX":     ("I_breadth", True,  "intensive",  "EBAR-MAX"),
    "EMED-MAX":        ("C_Emed",    True,  "extensive",  "BMED-MAX"),
    "BMED-MAX":        ("I_bmed",    True,  "intensive",  "EMED-MAX"),
    "EMAX-MAX":        ("C_Emax",    True,  "extensive",  "BMAX-MAX"),
    "BMAX-MAX":        ("I_bmax",    True,  "intensive",  "EMAX-MAX"),
    "ESD-MAX":         ("C_Esd",     True,  "extensive",  "BSD-MAX"),
    "BSD-MAX":         ("I_bsd",     True,  "intensive",  "ESD-MAX"),
    "COVER-MAX":       ("C_cover",   True,  "extensive",  "COVERSHARE-MAX"),
    "COVERSHARE-MAX":  ("I_cover",   True,  "intensive",  "COVER-MAX"),
    "SELECTIVITY-MAX": ("X_select",  True,  "inverse",    ""),
    "IS-SHARPE-MAX":   ("IS_Sharpe", True,  "intensive",  ""),
    "EWSHARPE-MAX":    ("EW_IS_S",   True,  "intensive",  ""),
    "EBAR-MIN":        ("C_Ebar",    False, "extensive",  "BREADTH-MIN"),
    "BREADTH-MIN":     ("I_breadth", False, "intensive",  "EBAR-MIN"),
    "K-MAX":           ("k",         True,  "control+",   ""),
    "RANDOM":          ("R_rand",    True,  "control-",   ""),
}
PAIRS = [("EBAR-MAX", "BREADTH-MAX"), ("EMED-MAX", "BMED-MAX"), ("EMAX-MAX", "BMAX-MAX"),
         ("ESD-MAX", "BSD-MAX"), ("COVER-MAX", "COVERSHARE-MAX"), ("EBAR-MIN", "BREADTH-MIN")]
BOOKLEVEL = {"IS-SHARPE-MAX"}          # criterion depends on the book size n


def extra_measures(px, cols, rng_rand):
    """IS-WINDOW-ONLY panel criteria, from ONE weekly gate matrix so each intensive twin is
    EXACTLY its extensive partner divided by k (gate G2 checks that)."""
    sub = px[cols]
    g = M276.gate(sub)
    mask = rebalance_mask(sub.index, FREQ)
    w = g.loc[mask.values].iloc[40:].loc[:IS_END]
    cnt = w.sum(axis=1).astype(float)
    k = float(len(cols))
    cover = float((w.sum(axis=0) > 0).sum())
    d = dict(k=k,
             C_Ebar=float(cnt.mean()), C_Emed=float(cnt.median()), C_Emax=float(cnt.max()),
             C_Esd=float(cnt.std()), C_cover=cover)
    d.update(I_breadth=d["C_Ebar"] / k, I_bmed=d["C_Emed"] / k, I_bmax=d["C_Emax"] / k,
             I_bsd=d["C_Esd"] / k, I_cover=d["C_cover"] / k)
    d["X_select"] = 20.0 / max(d["C_Ebar"], 1e-9)
    d["R_rand"] = float(rng_rand.random())
    d["n_is_days"] = int(len(cnt))
    return d


# ---------------------------------------------------------------- panel construction
def build_ladder(s_stk, b_stk):
    """[(k, draw, cols, provenance)] at q = 1.00.

    draws 0..2 at k <= 100 replay lane B's generator; draws 0..2 at k in {200,400} replay
    idea 685's second generator; draws 3..7 are NEW (seed 688).  The replays reproduce the
    committed panels exactly (GATE 0), so this ladder is a strict extension of the record's.
    """
    built, seen, prov = [], set(), {}
    # --- lane B's loop, replayed in its own order so the rng state matches at every cell
    rng = np.random.default_rng(SEED_B)
    for q in QS_B:
        for k in KS_B:
            ns_ = int(round(q * k)); nl_ = k - ns_
            for d in range(NDRAWS_B):
                sc = sorted(rng.choice(s_stk, size=ns_, replace=False)) if ns_ else []
                lc = sorted(rng.choice(b_stk, size=nl_, replace=False)) if nl_ else []
                key = (tuple(sc), tuple(lc))
                if key in seen: continue
                seen.add(key)
                if abs(q - Q_FIXED) < 1e-12 and k in KS:
                    built.append((k, d, sc + lc)); prov[(k, d)] = "laneB"
    # --- idea 685's second generator, replayed in its own order (skips consume nothing)
    rng2 = np.random.default_rng(SEED_685)
    for q in QS_685:
        for k in KS_685:
            if k <= 100: continue
            ns_ = int(round(q * k)); nl_ = k - ns_
            if ns_ > len(s_stk) or nl_ > len(b_stk): continue
            for d in range(ND_685):
                sc = sorted(rng2.choice(s_stk, size=ns_, replace=False)) if ns_ else []
                lc = sorted(rng2.choice(b_stk, size=nl_, replace=False)) if nl_ else []
                key = (tuple(sc), tuple(lc))
                if key in seen: continue
                seen.add(key)
                if abs(q - Q_FIXED) < 1e-12 and k in KS:
                    built.append((k, d, sc + lc)); prov[(k, d)] = "idea685"
    # --- this run's own draws, from a separate generator
    rng3 = np.random.default_rng(SEED_NEW)
    have = {(k, d) for k, d, _ in built}
    for k in KS:
        for d in range(N_DRAWS):
            if (k, d) in have: continue
            sc = sorted(rng3.choice(s_stk, size=k, replace=False))
            key = (tuple(sc), ())
            if key in seen:
                P(f"  dedupe: k={k} draw {d} is an exact repeat - redrawn"); continue
            seen.add(key)
            built.append((k, d, sc)); prov[(k, d)] = "new"
    built.sort(key=lambda t: (t[0], t[1]))
    return built, prov


# ---------------------------------------------------------------- statistics
def ols1(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 3 or np.std(x) == 0: return np.nan, np.nan
    b = np.cov(x, y, ddof=1)[0, 1] / np.var(x, ddof=1)
    a = y.mean() - b * x.mean()
    yhat = a + b * x
    ss = float(np.sum((y - y.mean()) ** 2))
    r2 = 1.0 - float(np.sum((y - yhat) ** 2)) / ss if ss > 0 else np.nan
    return float(b), r2


def binom_band(n, p, alpha=0.05):
    """Two-sided 95% acceptance band for a Binomial(n,p) count, as rates."""
    if n == 0: return (np.nan, np.nan)
    pmf = [math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(n + 1)]
    cdf = np.cumsum(pmf)
    lo = next((i for i in range(n + 1) if cdf[i] > alpha / 2), 0)
    hi = next((i for i in range(n + 1) if cdf[i] >= 1 - alpha / 2), n)
    return lo / n, hi / n


def binom_p_ge(n, x, p):
    """Exact one-sided P(X >= x) under Binomial(n, p)."""
    if n == 0: return np.nan
    return float(sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(x, n + 1)))


def classify_exponent(b):
    if not np.isfinite(b): return "NA"
    if b >= BAR_EXT: return "EXTENSIVE"
    if b <= -BAR_EXT: return "INVERSE-EXTENSIVE"
    if abs(b) <= BAR_INT: return "INTENSIVE"
    return "MIXED"


# ---------------------------------------------------------------- the record's census
COUNT_TOK = re.compile(r"(ebar|emed|emax|n_?elig|nelig|count|_cnt|cnt_|ndays|n_days|"
                       r"bought|nnames|n_names|width|^k$|_k$)", re.I)
RATE_TOK = re.compile(r"(sharpe|cagr|maxdd|_dd$|dd_|rho|corr|breadth|share|frac|pct|"
                      r"ratio|rate|overlap|margin|gap|prem|vol|disp|beta|auc|sortino|"
                      r"calmar|turnover|slope|score|mean|med_|avg)", re.I)
IDXPAT = re.compile(r"(?:([A-Za-z_][A-Za-z0-9_]*)\.([A-Za-z_][A-Za-z0-9_]*)|"
                    r"[A-Za-z_][A-Za-z0-9_]*\[[\"']([A-Za-z0-9_]+)[\"']\])\.(idxmax|idxmin)\(\)")
SELPAT = re.compile(r"[\"']([A-Za-z0-9_.:+-]{2,32})[\"']\s*:\s*\(\s*[\"']([A-Za-z0-9_]+)[\"']\s*,"
                    r"\s*(True|False)\s*\)")


def census():
    """Descriptive census of MAX-form rule-8 selector sites in the committed record."""
    rows = []
    for p in sorted(BT.glob("*.py")):
        if p.name == Path(__file__).name: continue
        try: txt = p.read_text(errors="ignore")
        except Exception: continue
        for m in IDXPAT.finditer(txt):
            col = m.group(2) or m.group(3)
            rows.append(dict(file=p.name, site="idxmax/idxmin", selector="",
                             criterion=col, form="MAX" if m.group(4) == "idxmax" else "MIN"))
        for m in SELPAT.finditer(txt):
            rows.append(dict(file=p.name, site="SELECTORS-dict", selector=m.group(1),
                             criterion=m.group(2), form="MAX" if m.group(3) == "True" else "MIN"))
    df = pd.DataFrame(rows)
    if df.empty: return df, pd.DataFrame()
    def fam(c):
        cnt, rate = bool(COUNT_TOK.search(c)), bool(RATE_TOK.search(c))
        if cnt and not rate: return "count-form"
        if rate and not cnt: return "rate-form"
        if cnt and rate: return "ambiguous"
        return "unclassified"
    df["family"] = df.criterion.map(fam)
    agg = (df.groupby(["criterion", "family"])
             .agg(sites=("file", "size"), files=("file", "nunique"),
                  max_sites=("form", lambda s: int((s == "MAX").sum())))
             .reset_index().sort_values("sites", ascending=False))
    return df, agg


def main():
    t0all = time.time()
    P("=" * 100)
    P("IDEA 688 - is-WIDTH-MAXIMISATION-a-general-rule-8-selector-pathology (lane C, 2026-09-11)")
    P("=" * 100)
    P("PRE-REGISTERED BARS (docstring, fixed before any number below was read):")
    P(f"  extensivity exponent b = d log|C| / d log k :  b >= +{BAR_EXT:.2f} EXTENSIVE | "
      f"|b| <= {BAR_INT:.2f} INTENSIVE | b <= -{BAR_EXT:.2f} INVERSE | else MIXED")
    P(f"  width-pin rate p at the widest ceiling    :  p >= {BAR_PIN:.2f} WIDTH-PINNED | "
      "inside the 95% exact-binomial band of 1/|K| WIDTH-NEUTRAL | else WIDTH-LEANING")
    P("  EXTENSIVE IN DISGUISE = WIDTH-PINNED and |b| >= 0.70 and not the K-MAX control.")
    P(f"  PRICE dOOS = OOS Sharpe(pick | C=400) - OOS Sharpe(pick | C=100), all selectors.")
    P(f"  Ladder: q = {Q_FIXED:.2f} (FORCED - single pool, exchangeable draws), "
      f"k in {KS} ({max(KS)//min(KS)}.0x), {N_DRAWS} draws, {len(SELECTORS)} selectors, "
      f"ceilings {CEILS}.")

    # ------------------------------------------------------------ census
    P("\n" + "=" * 100)
    P("CENSUS - MAX-form rule-8 selector sites in the committed record (descriptive)")
    P("=" * 100)
    craw, cagg = census()
    craw.to_csv(f"{OUT}.census.csv", index=False)
    if not cagg.empty:
        tot, nmax = len(craw), int((craw.form == "MAX").sum())
        P(f"  {tot} selector sites in {craw.file.nunique()} committed scripts "
          f"({nmax} MAX form, {tot - nmax} MIN form); {cagg.criterion.nunique()} distinct criteria.")
        fam = craw.groupby("family").size().sort_values(ascending=False)
        for f_, c_ in fam.items():
            P(f"    {f_:14s} {c_:5d} sites ({c_ / tot:6.1%})   "
              f"{craw[craw.family == f_].criterion.nunique():3d} distinct criteria")
        P("  top 15 criteria by site count:")
        P("    " + cagg.head(15).to_string(index=False).replace("\n", "\n    "))
        P("  count-form criteria found in the record (the family this run prices):")
        cf = cagg[cagg.family == "count-form"]
        P("    " + (cf.to_string(index=False).replace("\n", "\n    ") if len(cf) else "(none)"))

    # ------------------------------------------------------------ sources + ladder
    src = M276.build_sources()
    pxs, pxb = src["pxs"], src["pxb"]
    idx = pxs.index.intersection(pxb.index)
    pxs_c, pxb_c = pxs.reindex(idx).ffill(), pxb.reindex(idx).ffill()
    spy = pxb_c["SPY"]
    s_stk, b_stk = src["s_stk"], src["b_stk"]
    P(f"\ncommon calendar {idx[0].date()} .. {idx[-1].date()}  ({len(idx)} days); "
      f"pools: SMALL {len(s_stk)}, BSTK {len(b_stk)}")

    built, prov = build_ladder(s_stk, b_stk)
    nrep = sum(1 for v in prov.values() if v != "new")
    P(f"\n{len(built)} panels built at q={Q_FIXED:.2f} "
      f"({nrep} replayed from the record, {len(built) - nrep} new)")

    P("\n--- GATE 3: envelope ---")
    bad = []
    for k, d, cols in built:
        if len(cols) != k: bad.append((k, d, "width"))
        if len(set(cols)) != len(cols): bad.append((k, d, "dup"))
        if any(c not in s_stk for c in cols): bad.append((k, d, "cap mix"))
    assert not bad, f"GATE 3 FAILED: {bad[:5]}"
    P(f"  GATE 3 PASS - all {len(built)} panels: exact width, pure SMALL pool "
      f"(q={Q_FIXED:.2f}), no duplicate columns, inside the pool bound ({len(s_stk)}).")

    # ------------------------------------------------------------ run every panel
    P("\n" + "=" * 100)
    P("RUNNING THE LADDER")
    P("=" * 100)
    rng_rand = np.random.default_rng(SEED_NEW + 1)
    brows, srows, xrows = [], [], []
    for i, (k, d, cols) in enumerate(built):
        px = pd.concat([pxs_c[cols], spy.rename("SPY")], axis=1).dropna(how="all").ffill()
        px = px[cols + ["SPY"]]
        tag = f"MIX q={Q_FIXED:.2f} k={k} d{d}"
        t0 = time.time()
        do_panel(tag, "mix", Q_FIXED, d, px, cols, brows, srows, NS_LAD, {"lad": NS_LAD})
        xm = extra_measures(px, cols, rng_rand)
        xrows.append(dict(panel=tag, draw=d, prov=prov[(k, d)], **xm))   # xm carries k
        P(f"  [{i + 1:3d}/{len(built)}] k={k:3d} d{d}  {time.time() - t0:5.1f}s "
          f"(elapsed {time.time() - t0all:6.1f}s)  [{prov[(k, d)]}]")

    stats = pd.DataFrame(srows); books = pd.DataFrame(brows); ext = pd.DataFrame(xrows)
    mix = stats[stats.ladder == "lad"].copy()
    stats.to_csv(f"{OUT}.stats.csv", index=False)
    books.to_csv(f"{OUT}.books.csv", index=False)
    mix[["panel", "q", "k", "draw", "Ebar", "Emed", "breadth", "Ebar_IS", "breadth_IS",
         "selectivity20"]].merge(ext.drop(columns=["k", "draw"]), on="panel") \
        .to_csv(f"{OUT}.panels.csv", index=False)

    # ------------------------------------------------------------ GATE 0
    P("\n" + "=" * 100)
    P("GATE 0 - REPRODUCTION of the committed record from the replayed draws")
    P("=" * 100)
    EXACT = ["Ebar", "breadth", "Emed", "Ebar_IS", "breadth_IS"]
    SGATE = SCOLS + ["EW_Sharpe", "EW_OOS_Sharpe", "ADAPT_Sharpe", "best_prem"]
    mine_p = mix.set_index("panel"); mine_s = mix.set_index("panel")
    worst_all, tot_over = {}, 0
    for label, base in (("lane B (idea 525)", P525), ("idea 685 (lane C)", P685)):
        refp = pd.read_csv(f"{base}.panels.csv"); refp = refp[refp.kind == "mix"] if "kind" in refp else refp
        refp = refp.set_index("panel")
        refs = pd.read_csv(f"{base}.stats.csv")
        refs = refs[(refs.kind == "mix") & (refs.ladder == "lad")].set_index("panel")
        over = [p for p in mine_p.index if p in refp.index and p in refs.index]
        P(f"  {label}: {len(over)} overlapping panels")
        if not over: continue
        tot_over += len(over)
        for c in EXACT:
            dd = (refp.loc[over, c] - mine_p.loc[over, c]).abs()
            worst_all[f"{label}:{c}"] = float(dd.max())
            P(f"    panel measure {c:12s} max |delta| {dd.max():.3e}  >1e-9: "
              f"{int((dd > 1e-9).sum())}/{len(dd)}")
        for c in SGATE:
            dd = (refs.loc[over, c] - mine_s.loc[over, c]).abs()
            worst_all[f"{label}:{c}"] = float(dd.max())
            P(f"    statistic     {c:12s} max |delta| {dd.max():.3e}  >1e-9: "
              f"{int((dd > 1e-9).sum())}/{len(dd)}")
    for kk, vv in worst_all.items():
        assert vv < 1e-9, f"GATE 0 FAILED on {kk}: {vv:.3e}"
    P(f"  GATE 0 PASS - {tot_over} panel-overlaps x {len(EXACT + SGATE)} quantities reproduce "
      f"at MACHINE PRECISION (worst {max(worst_all.values()):.3e}).")

    P("\n--- GATE 1: the k-IDENTITY ---")
    dident = (mix.k * mix.breadth - mix.Ebar).abs()
    P(f"  max |k * breadth - Ebar| over {len(mix)} panels: {dident.max():.3e}")
    assert float(dident.max()) < 1e-9, f"GATE 1 FAILED: {dident.max():.3e}"
    P("  GATE 1 PASS.")

    P("\n--- GATE 2: PAIR IDENTITY (each intensive twin == its extensive partner / k) ---")
    worst2 = 0.0
    for ce, ci in (("C_Ebar", "I_breadth"), ("C_Emed", "I_bmed"), ("C_Emax", "I_bmax"),
                   ("C_Esd", "I_bsd"), ("C_cover", "I_cover")):
        dd = (ext[ce] / ext.k - ext[ci]).abs()
        worst2 = max(worst2, float(dd.max()))
        P(f"  {ce:8s} / k  vs  {ci:10s}  max |delta| {dd.max():.3e}")
    assert worst2 < 1e-12, f"GATE 2 FAILED: {worst2:.3e}"
    P(f"  GATE 2 PASS (worst {worst2:.3e}) - within a pair the two selectors differ ONLY by "
      "the division by k.")

    # ------------------------------------------------------------ extensivity exponents
    P("\n" + "=" * 100)
    P("EXTENSIVITY - b = OLS slope of log|criterion| on log k, over all panels")
    P("=" * 100)
    erows = []
    logk = np.log(ext.k.values)
    for sel, (col, hi, famdecl, twin) in SELECTORS.items():
        if sel in BOOKLEVEL or col == "EW_IS_S":
            continue                              # book-level criteria handled below
        v = ext[col].values.astype(float)
        b, r2 = ols1(logk, np.log(np.abs(v) + 1e-12))
        # within-draw slope: removes any draw-level level effect
        wsl = []
        for d, sub in ext.groupby("draw"):
            bb, _ = ols1(np.log(sub.k.values), np.log(np.abs(sub[col].values) + 1e-12))
            if np.isfinite(bb): wsl.append(bb)
        erows.append(dict(selector=sel, criterion=col, declared=famdecl, twin=twin,
                          beta_logk=b, R2=r2, within_draw_beta=float(np.mean(wsl)) if wsl else np.nan,
                          rho_k=spearman(ext[col], ext.k),
                          lo=float(np.nanmin(v)), hi=float(np.nanmax(v)),
                          span=float(np.nanmax(v) / np.nanmin(v)) if np.nanmin(v) > 0 else np.nan,
                          measured=classify_exponent(b)))
    # book-level criteria, measured on the CAND-n / EWall IS Sharpes
    bk = books.merge(ext[["panel", "prov"]], on="panel")
    for sel, col in (("IS-SHARPE-MAX", "IS_Sharpe"), ("EWSHARPE-MAX", "EW_IS_S")):
        sub = bk[bk.arm != "EWall"] if sel == "IS-SHARPE-MAX" else bk[bk.arm == "EWall"]
        b, r2 = ols1(np.log(sub.k.values), np.log(np.abs(sub.IS_Sharpe.values) + 1e-12))
        erows.append(dict(selector=sel, criterion=col, declared="intensive", twin="",
                          beta_logk=b, R2=r2, within_draw_beta=np.nan,
                          rho_k=spearman(sub.IS_Sharpe, sub.k),
                          lo=float(sub.IS_Sharpe.min()), hi=float(sub.IS_Sharpe.max()),
                          span=np.nan, measured=classify_exponent(b)))
    edf = pd.DataFrame(erows)
    edf.to_csv(f"{OUT}.extensivity.csv", index=False)
    P(edf[["selector", "criterion", "declared", "beta_logk", "within_draw_beta", "R2",
           "rho_k", "span", "measured"]].to_string(index=False,
           float_format=lambda x: f"{x:8.4f}"))
    agree = int((edf.declared.str.startswith("ext") & (edf.measured == "EXTENSIVE")).sum()
                + (edf.declared.str.startswith("int") & (edf.measured == "INTENSIVE")).sum()
                + (edf.declared.str.startswith("inv") & (edf.measured == "INVERSE-EXTENSIVE")).sum())
    decl = edf[edf.declared.isin(["extensive", "intensive", "inverse"])]
    P(f"\n  declared family confirmed by the measured exponent on {agree} of {len(decl)} "
      "non-control selectors.")

    # ------------------------------------------------------------ the picks (rule 8)
    P("\n" + "=" * 100)
    P("RULE 8 - IS-only criteria pick a panel; the pick is read ONCE on 2017-01-01..")
    P("=" * 100)
    bb = books[books.arm != "EWall"].copy()
    ewis = books[books.arm == "EWall"].set_index("panel").IS_Sharpe
    bb = bb.merge(ext.drop(columns=["k", "draw"]), on="panel", how="left")
    bb["EW_IS_S"] = bb.panel.map(ewis)
    smeta = mix.set_index("panel")[["spy_OOS_CAGR", "spy_OOS_DD", "v2_OOS_CAGR", "v2_OOS_DD"]]
    bb = bb.join(smeta, on="panel")

    prows = []
    for ceil in CEILS:
        cs = bb[bb.k <= ceil]
        klev = sorted(cs.k.unique()); nk = len(klev)
        for n, subn in cs.groupby("n"):
            for d, sub in subn.groupby("draw"):
                if sub.k.nunique() != nk: continue          # incomplete choice set, skipped
                anchor = float(sub.OOS_Sharpe.mean())
                for sel, (col, hi, famdecl, twin) in SELECTORS.items():
                    i = sub[col].idxmax() if hi else sub[col].idxmin()
                    pk = sub.loc[i]
                    prows.append(dict(ceiling=ceil, n_levels=nk, n=int(n), draw=int(d),
                                      selector=sel, criterion=col, form="MAX" if hi else "MIN",
                                      declared=famdecl, panel=pk.panel, k_pick=float(pk.k),
                                      at_ceiling=bool(pk.k == max(klev)),
                                      at_floor=bool(pk.k == min(klev)),
                                      pinned=bool(pk.k == (max(klev) if hi else min(klev))),
                                      crit=float(pk[col]),
                                      OOS_CAGR=float(pk.OOS_CAGR), OOS_Sharpe=float(pk.OOS_Sharpe),
                                      OOS_MaxDD=float(pk.OOS_MaxDD), IS_Sharpe=float(pk.IS_Sharpe),
                                      anchor_OOS_S=anchor,
                                      v2_OOS_S=float(pk.v2_OOS_S), v2_OOS_CAGR=float(pk.v2_OOS_CAGR),
                                      v2_OOS_DD=float(pk.v2_OOS_DD),
                                      spy_OOS_S=float(pk.spy_OOS_S), spy_OOS_CAGR=float(pk.spy_OOS_CAGR),
                                      spy_OOS_DD=float(pk.spy_OOS_DD),
                                      beats_anchor=bool(pk.OOS_Sharpe > anchor),
                                      beats_v2=bool(pk.OOS_Sharpe > pk.v2_OOS_S),
                                      beats_spy=bool(pk.OOS_Sharpe > pk.spy_OOS_S)))
    picks = pd.DataFrame(prows)
    picks.to_csv(f"{OUT}.picks.csv", index=False)

    # -------- width-pin rates, per selector x ceiling; independence handled explicitly
    P("\nWIDTH-PIN RATE  (share of picks at the extreme END the selector's form points at)")
    P("  n_ind = independent draws (panel-level criteria give the SAME pick at every book")
    P("  size, so the draw is the independent unit; book-level criteria are flagged).")
    wrows = []
    for ceil in CEILS:
        sub0 = picks[picks.ceiling == ceil]
        if sub0.empty: continue
        nk = int(sub0.n_levels.iloc[0]); unif = 1.0 / nk
        lo, hi_ = binom_band(N_DRAWS, unif)
        for sel in SELECTORS:
            s = sub0[sub0.selector == sel]
            if s.empty: continue
            rate = float(s.pinned.mean())
            # independent unit = draw (panel-level) or draw x n (book-level, correlated)
            per_draw = s.groupby("draw").pinned.mean()
            ind_rate = float((per_draw > 0.5).mean()); nind = int(len(per_draw))
            x = int(round(ind_rate * nind))
            pval = binom_p_ge(nind, x, unif)
            verdict = ("WIDTH-PINNED" if ind_rate >= BAR_PIN else
                       "WIDTH-NEUTRAL" if lo <= ind_rate <= hi_ else "WIDTH-LEANING")
            wrows.append(dict(ceiling=ceil, n_levels=nk, selector=sel,
                              declared=SELECTORS[sel][2], form=s.form.iloc[0],
                              book_level=sel in BOOKLEVEL, uniform=unif,
                              pin_rate_all=rate, pin_rate_draws=ind_rate, n_ind=nind,
                              binom_p=pval, band_lo=lo, band_hi=hi_,
                              mean_k_pick=float(s.k_pick.mean()),
                              mean_OOS_S=float(s.OOS_Sharpe.mean()),
                              mean_OOS_CAGR=float(s.OOS_CAGR.mean()),
                              mean_OOS_DD=float(s.OOS_MaxDD.mean()),
                              anchor_OOS_S=float(s.anchor_OOS_S.mean()),
                              beats_anchor=float(s.beats_anchor.mean()),
                              beats_v2=float(s.beats_v2.mean()),
                              beats_spy=float(s.beats_spy.mean()), verdict=verdict))
    wf = pd.DataFrame(wrows)
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    for ceil in CEILS:
        s = wf[wf.ceiling == ceil]
        if s.empty: continue
        P(f"\n  ceiling C = {ceil:3d}  ({int(s.n_levels.iloc[0])} width levels, uniform "
          f"{s.uniform.iloc[0]:.3f}, 95% band [{s.band_lo.iloc[0]:.3f}, {s.band_hi.iloc[0]:.3f}])")
        P("    " + s[["selector", "declared", "form", "pin_rate_draws", "binom_p",
                      "mean_k_pick", "mean_OOS_S", "anchor_OOS_S", "verdict"]]
          .to_string(index=False, float_format=lambda x: f"{x:8.4f}").replace("\n", "\n    "))

    # -------- the headline table: exponent x pin x price
    P("\n" + "=" * 100)
    P("THE ANSWER - which MAX-form selectors are EXTENSIVE STATISTICS IN DISGUISE")
    P("=" * 100)
    w400 = wf[wf.ceiling == max(CEILS)].set_index("selector")
    w100 = wf[wf.ceiling == 100].set_index("selector")
    e = edf.set_index("selector")
    hrows = []
    for sel in SELECTORS:
        if sel not in w400.index or sel not in e.index: continue
        b = float(e.loc[sel, "beta_logk"])
        pin = float(w400.loc[sel, "pin_rate_draws"])
        dOOS = float(w400.loc[sel, "mean_OOS_S"] - w100.loc[sel, "mean_OOS_S"]) if sel in w100.index else np.nan
        dDD = float(w400.loc[sel, "mean_OOS_DD"] - w100.loc[sel, "mean_OOS_DD"]) if sel in w100.index else np.nan
        dCAGR = float(w400.loc[sel, "mean_OOS_CAGR"] - w100.loc[sel, "mean_OOS_CAGR"]) if sel in w100.index else np.nan
        disguise = bool(pin >= BAR_PIN and abs(b) >= BAR_EXT and SELECTORS[sel][2] != "control+")
        hrows.append(dict(selector=sel, declared=SELECTORS[sel][2], beta_logk=b,
                          exponent_class=e.loc[sel, "measured"], pin_rate_C400=pin,
                          pin_verdict=w400.loc[sel, "verdict"],
                          k_pick_C100=float(w100.loc[sel, "mean_k_pick"]) if sel in w100.index else np.nan,
                          k_pick_C400=float(w400.loc[sel, "mean_k_pick"]),
                          OOS_S_C100=float(w100.loc[sel, "mean_OOS_S"]) if sel in w100.index else np.nan,
                          OOS_S_C400=float(w400.loc[sel, "mean_OOS_S"]),
                          dOOS_S=dOOS, dOOS_CAGR=dCAGR, dOOS_MaxDD=dDD,
                          EXTENSIVE_IN_DISGUISE=disguise))
    H = pd.DataFrame(hrows)
    P(H.to_string(index=False, float_format=lambda x: f"{x:8.4f}"))
    nd = int(H.EXTENSIVE_IN_DISGUISE.sum())
    P(f"\n  EXTENSIVE IN DISGUISE: {nd} of {len(H)} tested selectors "
      f"({', '.join(H[H.EXTENSIVE_IN_DISGUISE].selector)})")
    P(f"  mean dOOS Sharpe, disguised selectors : "
      f"{H[H.EXTENSIVE_IN_DISGUISE].dOOS_S.mean():+.4f}")
    P(f"  mean dOOS Sharpe, everything else     : "
      f"{H[~H.EXTENSIVE_IN_DISGUISE].dOOS_S.mean():+.4f}")

    P("\n  MATCHED PAIRS (the two members differ ONLY by the division by k):")
    for a, bsel in PAIRS:
        if a not in H.selector.values or bsel not in H.selector.values: continue
        ra = H[H.selector == a].iloc[0]; rb = H[H.selector == bsel].iloc[0]
        P(f"    {a:16s} b={ra.beta_logk:+.3f} pin={ra.pin_rate_C400:.3f} "
          f"dOOS={ra.dOOS_S:+.4f}   |   {bsel:16s} b={rb.beta_logk:+.3f} "
          f"pin={rb.pin_rate_C400:.3f} dOOS={rb.dOOS_S:+.4f}   "
          f"-> pin gap {ra.pin_rate_C400 - rb.pin_rate_C400:+.3f}, "
          f"OOS gap {ra.dOOS_S - rb.dOOS_S:+.4f}")

    # -------- how the pathology scales with the choice set
    P("\n  PIN RATE vs CHOICE-SET WIDTH (all ceilings, all selectors reported):")
    piv = wf.pivot_table(index="selector", columns="ceiling", values="pin_rate_draws")
    P("    " + piv.to_string(float_format=lambda x: f"{x:6.3f}").replace("\n", "\n    "))
    P("\n  MEAN OOS SHARPE OF THE PICK vs CHOICE-SET WIDTH:")
    piv2 = wf.pivot_table(index="selector", columns="ceiling", values="mean_OOS_S")
    P("    " + piv2.to_string(float_format=lambda x: f"{x:6.3f}").replace("\n", "\n    "))

    # ------------------------------------------------------------ benchmarks + KEEP paths
    P("\n" + "=" * 100)
    P("BENCHMARKS AND PROTOCOL 4a / 4b (10 bps, every book row)")
    P("=" * 100)
    P(f"  SPY      OOS Sharpe {mix.spy_OOS_S.mean():.4f}  CAGR {mix.spy_OOS_CAGR.mean():.2%}  "
      f"MaxDD {mix.spy_OOS_DD.mean():.2%}")
    P(f"  RULES v2 OOS Sharpe {mix.v2_OOS_S.mean():.4f}  CAGR {mix.v2_OOS_CAGR.mean():.2%}  "
      f"MaxDD {mix.v2_OOS_DD.mean():.2%}   (per-panel means)")
    P(f"  choice-set anchor (mean OOS Sharpe over all {len(books)} book rows): "
      f"{books.OOS_Sharpe.mean():.4f}")
    P(f"\n  4a passes: {int(books.pass4a.sum())} / {len(books)}      "
      f"4b passes: {int(books.pass4b.sum())} / {len(books)}")
    for kk, sub in books.groupby("k"):
        P(f"    k={int(kk):3d}: 4a {int(sub.pass4a.sum()):3d}/{len(sub):3d}   "
          f"4b {int(sub.pass4b.sum()):3d}/{len(sub):3d}")
    P("\n  full-sample / halves / OOS of the book arms (mean over panels, by n):")
    g = books.groupby("arm").agg(CAGR=("CAGR", "mean"), Sharpe=("Sharpe", "mean"),
                                 MaxDD=("MaxDD", "mean"), H1=("H1", "mean"), H2=("H2", "mean"),
                                 OOS_S=("OOS_Sharpe", "mean"), OOS_CAGR=("OOS_CAGR", "mean"),
                                 OOS_DD=("OOS_MaxDD", "mean"))
    P("    " + g.to_string(float_format=lambda x: f"{x:8.4f}").replace("\n", "\n    "))
    P("\n  selector picks vs the benchmarks, at C = 400 (share of picks that beat):")
    P("    " + w400[["beats_anchor", "beats_v2", "beats_spy", "mean_OOS_S", "mean_OOS_CAGR",
                     "mean_OOS_DD"]].to_string(float_format=lambda x: f"{x:8.4f}")
      .replace("\n", "\n    "))

    P("\n" + "=" * 100)
    P(f"done in {time.time() - t0all:.1f}s")
    P("=" * 100)
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
