#!/usr/bin/env python3
"""Idea 380 — the SCORED vs PRICED denominator is (allegedly) a 5-point sign-stability gap.

THE FILED CLAIM
    idea 124's ALL rung (weight GROSS/k where k = # names with a DEFINED COMPOSITE) and
    idea 94's EWall (weight GROSS/N where N = # names PRICED) differ by max |dw| 0.0150 and
    disagree on 1530 of 4439 u56 eval days, "yet on IDENTICAL bootstrap draws their mean D3
    frac_pos is 0.8133 vs 0.7609".  A 5-point stability gap created purely by which names the
    denominator counts would be a defect.  Audit every committed all-names book for which
    convention it used and propose one.

WHAT THIS SCRIPT DOES
    A. AUDIT.  Classify every committed all-names / equal-weight-everything book in
       research/ (backtests + baseline) into PRICED / SCORED / GATED by a pre-registered
       source classifier, gated 6/6 against hand-established files, and map the classes onto
       the LEADERBOARD rows those scripts back.
    B. THE CAUSAL TEST.  The archived gap is CONFOUNDED: `_B` (PRICED ALL) ran at
       SEED=20260907 and `_B2` (SCORED ALL) at SEED=20260905 (idea 382's finding).  Seed and
       convention move together, so the archive cannot attribute the gap to either.  This
       script breaks the confound with a 2x2 (both conventions x both archived seeds) plus a
       seed panel of NSEED seeds, one pipeline, one arm set, ONE draw index per seed.
       Pre-registered:
         H1 (denominator effect)  matched-seed mean gap SCORED - PRICED != 0 and ~ the
                                  archived +0.038 (u56) / +0.046 (pooled).
         H0 (seed artefact)       matched-seed gap ~ 0, and the archived gap sits inside the
                                  across-seed spread of a SINGLE convention.
       Decision: paired test over seeds on the matched-seed gap, plus |archived gap| vs the
       across-seed SD of each convention's own mean.  Idea 382's amendment is applied as a
       second reading: D3 recomputed over draws clearing idea 94's 0.10 pp floor only.
    C. THE PRICE + KEEP PATHS + RULE 8.  What the convention is worth in return space, on the
       ungated all-names book AND on the LIVE RULES v2 form (band3-gated all-names), at
       gross g in {0.375, 0.50, 0.75, 1.00}, costs {0, 10, 25} bps, on both panels.  4a vs
       RULES v2, 4b vs SPY, every grid point reported.
    D. THE PROPOSAL.

TUNED PARAMETERS (2, as PROTOCOL rule 4 allows)
    convention in {PRICED, SCORED}   and   gross g in {0.375, 0.50, 0.75, 1.00}.
    The gate FORM (ungated / band3, the live clause) is NOT a dial: both are fixed
    pre-specified constructions, reported side by side and never selected between.
    NSEED/NDRAW/q/tau are the record's own constants (idea 119/122/124), not tuned here.

GATES (nothing is reported before these pass)
    G1  H.run == engine.backtest (returns AND turnover) at 0 and 25 bps, both books, both
        panels.
    G2  PRICED book == H.targets(px, "EWall") exactly.
    G3  idea 380's own filed construction facts: max|dw| = 0.0150 and 1530 of 4439 u56 eval
        days disagree.
    G4  reproduce `_B2`'s committed d3.csv ALL rows (q=0.10) at ITS seed 20260905.
    G5  reproduce `_B`'s committed d3.csv TOPall rows (q=0.10) at ITS seed 20260907.
    G4+G5 together are what make the 2x2 exact: the pipeline here IS both archived pipelines.

Deterministic, standalone, modifies nothing outside research/backtests/<stem>.*
"""
import importlib.util
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))

from baseline import rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

BT = ROOT / "research" / "backtests"
_s94 = importlib.util.spec_from_file_location(
    "i94", BT / "2026-09-04_drawdown-insurance-price-list_B.py")
H = importlib.util.module_from_spec(_s94)
_s94.loader.exec_module(H)

STEM = Path(__file__).stem
OUT = BT / STEM
I124_B = BT / "2026-09-07_book-size-floor-for-any-quoted-price_B"
I124_B2 = BT / "2026-09-07_book-size-floor-for-any-quoted-price_B2"

PCOST = 10.0
COST_RUNGS = [0.0, 10.0, 25.0]
IS_END, OOS_START = H.IS_END, H.OOS_START
FLOOR = 0.10                                   # idea 94's absolute floor on |dMaxDD|
Q_STAR, TAU_STAR = 0.10, 0.90                  # idea 119/122's headline, adopted unchanged
DROP_FRACS = (0.05, 0.10, 0.20)                # the rng must be consumed in idea 122's order
NDRAW = 40
SEED_B, SEED_B2 = 20260907, 20260905            # the two archived seeds (idea 382)
SEEDS = [SEED_B2, SEED_B, 20260901, 20260902, 20260903, 20260904, 20260906, 20260908]
CONVS = ["PRICED", "SCORED"]
GROSSES = [0.375, 0.50, 0.75, 1.00]            # tuned dial 2
ARMS = [a for a in H.arm_specs() if a[0] != "control"]
PANELS = [("universe.json(56)", {}), ("universe_broad.json", dict(broad=True))]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 4000)

RULE = "=" * 200
GATE_LOG = []


def gate(label, value, tol, unit=""):
    ok = (value <= tol) if not np.isnan(value) else False
    GATE_LOG.append(dict(gate=label, value=value, tol=tol, passed=bool(ok)))
    print(f"[gate] {label:<64s} {value:.3e}{unit} (tol {tol:.0e}) "
          f"{'PASS' if ok else 'FAIL — UNSAFE'}")
    return ok


def fmt(df):
    return df.to_string(index=False, float_format=lambda x: f"{x:.4f}")


# =====================================================================================
# the two conventions, as ONE function
# =====================================================================================
def allnames_weights(px, conv, gross=H.GROSS, comp=None, gate_mask=None, rw=False):
    """The all-names equal-weight book under one denominator convention.

    PRICED : indicator = px.notna();            weight = gross / #priced      (idea 94 EWall,
             and research/baseline.py rules_v2_weights, i.e. the LIVE book).
    SCORED : indicator = composite.notna();     weight = gross / #scored      (idea 124 _B2's
             TOPALL rung).
    gate_mask, rw=False -> de-gross (gated-out weight to CASH, the live convention).
    gate_mask, rw=True  -> reweight at full gross among gated-in names (idea 94's 'rw').
    """
    if conv == "PRICED":
        ind = px.notna()
    elif conv == "SCORED":
        ind = (H.composite(px) if comp is None else comp).notna()
    else:
        raise ValueError(conv)
    if gate_mask is not None and rw:
        ind = ind & gate_mask
    e = ind.astype(float)
    k = e.sum(axis=1).replace(0, np.nan)
    W = gross * e.div(k, axis=0).fillna(0.0)
    if gate_mask is not None and not rw:
        W = W.where(gate_mask, 0.0)
    return W


def draw_sets(ncol, seed):
    """Idea 122's draw index, consumed in its order.  Returns {q: [keep-sets]}."""
    rng = np.random.default_rng(seed)
    out = {}
    for q in DROP_FRACS:
        k = int(round(ncol * (1 - q)))
        out[q] = [sorted(rng.choice(ncol, size=k, replace=False)) for _ in range(NDRAW)]
    return out


def dpair(rc, ra):
    mc, ma = metrics(rc), metrics(ra)
    dc = (mc["CAGR"] - ma["CAGR"]) * 100.0
    dd = (abs(mc["MaxDD"]) - abs(ma["MaxDD"])) * 100.0
    return dc, dd, (dc / dd if dd > FLOOR else np.nan)


def win(r, w):
    return r if w == "full" else (r.loc[:IS_END] if w == "IS" else r.loc[OOS_START:])


# =====================================================================================
# A.  THE AUDIT — pre-registered, SITE-level (a file may carry more than one book)
# =====================================================================================
PRICE_VARS = {"px", "sub", "prices", "p", "pr", "pxs", "pan", "panel", "close", "cl",
              "pxx", "pp", "pxu", "pxb", "px2", "P", "PX", "spx", "pxi", "u", "pxn"}
SIG_VARS = {"s", "comp", "composite", "score", "sc", "sig", "v1s", "cmp", "sco", "sk",
            "scr", "sr", "ss", "sg", "cscore", "elig", "defined"}

RE_NOTNA = re.compile(r"\b([A-Za-z_][A-Za-z_0-9]*)\s*\.notna\(\)")
RE_ASSIGN = re.compile(r"^\s*(?:[A-Za-z_][A-Za-z_0-9]*\[[^\]]*\]\s*=|"
                       r"([A-Za-z_][A-Za-z_0-9]*)\s*=)\s*(.+)$")
NOT_ALLNAMES = re.compile(r"ceil\(|FRAC|\bf\s*\*|\bq\s*\*|param\s*\*|round\(|int\(")

# the four ALL-NAMES availability idioms present in this repository
P_FRAME = re.compile(r"DataFrame\(\s*1\.0.*?\.where\((?P<expr>[^\n]*?\.notna\(\)[^\n]*?),\s*0")
P_COUNT = re.compile(r"(?P<expr>\b[A-Za-z_][A-Za-z_0-9]*\s*\.notna\(\)"
                     r"(?:\s*&\s*[A-Za-z_][A-Za-z_0-9]*\.notna\(\))*)\s*\.sum\(axis=1\)")
P_RANKLE = re.compile(r"(?P<expr>rank\s*\.le\(\s*(?P<cnt>[A-Za-z_][A-Za-z_0-9]*)\s*,\s*axis=0\))")
P_CONJ = re.compile(r"(?P<expr>\b[A-Za-z_][A-Za-z_0-9]*\.notna\(\)"
                    r"\s*&\s*[A-Za-z_][A-Za-z_0-9]*\.notna\(\))")

HAND = {                       # the 6 hand-established files that gate the classifier
    "2026-09-04_drawdown-insurance-price-list_B.py": "PRICED",
    "2026-09-07_book-size-floor-for-any-quoted-price_B.py": "PRICED",
    "2026-09-07_book-size-floor-for-any-quoted-price_B2.py": "SCORED",
    "2026-09-07_book-size-floor-for-any-quoted-price_cloud.py": "PRICED",
    "2026-09-07_book-size-floor-INSTRUMENT-CLASS-replication_cloud.py": "SCORED",
    "baseline.py": "PRICED",
}


def collect_assigns(text):
    a = {}
    for line in text.splitlines():
        m = RE_ASSIGN.match(line)
        if m and m.group(1):
            a.setdefault(m.group(1), []).append(m.group(2))
    return a


def var_class(v, A, depth=0):
    if v in PRICE_VARS:
        return "PRICED"
    if v in SIG_VARS:
        return "SCORED"
    if depth > 2:
        return None
    for rhs in A.get(v, []):
        if re.search(r"composite\(|\bscore\(|rank\(|\.rank\(|\bcomp\b|_score|"
                     r"/\s*[A-Za-z_]*vol", rhs):
            return "SCORED"
        if re.search(r"load_universe|load_prices|\bprices\b|\bpx\b|read_csv", rhs):
            return "PRICED"
        m = RE_NOTNA.search(rhs)
        if m and m.group(1) != v:
            c = var_class(m.group(1), A, depth + 1)
            if c:
                return c
        m2 = re.match(r"^\s*([A-Za-z_][A-Za-z_0-9]*)\b", rhs)
        if m2 and m2.group(1) != v:
            c = var_class(m2.group(1), A, depth + 1)
            if c:
                return c
    return None


def conj_class(expr, A):
    """An indicator expression.  An INTERSECTION binds on the stricter (scored) set, because
    comp.notna() implies px.notna() on a forward-filled panel."""
    cs = {var_class(v, A) for v in RE_NOTNA.findall(expr)}
    cs.discard(None)
    if "SCORED" in cs:
        return "SCORED"
    if "PRICED" in cs:
        return "PRICED"
    return "UNRESOLVED"


def classify_file(text):
    A = collect_assigns(text)
    out = []
    for m in P_FRAME.finditer(text):
        out.append(("frame", conj_class(m.group("expr"), A)))
    for m in P_COUNT.finditer(text):
        c = conj_class(m.group("expr"), A)
        if c != "UNRESOLVED":       # an unresolvable receiver is not a panel denominator
            out.append(("count", c))
    for m in P_RANKLE.finditer(text):
        cnt = m.group("cnt")
        if any(NOT_ALLNAMES.search(r) for r in A.get(cnt, [])):
            continue                # a fractional / integer top-n book, not all-names
        c = var_class(cnt, A)
        if c is None:               # the count is a parameter: fall back to the file's counts
            cs = {conj_class(x.group("expr"), A) for x in P_COUNT.finditer(text)}
            cs.discard("UNRESOLVED")
            c = ("SCORED" if "SCORED" in cs else "PRICED" if cs == {"PRICED"} else "UNRESOLVED")
        out.append(("rank.le", c))
    for m in P_CONJ.finditer(text):
        out.append(("conj", conj_class(m.group("expr"), A)))
    return out


def file_class(sites):
    cs = {c for _, c in sites}
    if not sites:
        return "no-all-names-book"
    if "SCORED" in cs and "PRICED" in cs:
        return "BOTH"
    if "SCORED" in cs:
        return "SCORED"
    if "PRICED" in cs:
        return "PRICED"
    return "UNRESOLVED"


def audit():
    print("\n" + RULE)
    print("A.  AUDIT — every committed all-names book, by denominator convention")
    print(RULE)
    files = sorted(BT.glob("*.py")) + [ROOT / "research" / "baseline.py"]
    rows = []
    for f in files:
        s = classify_file(f.read_text(errors="ignore"))
        rows.append(dict(file=f.name, sites=len(s),
                         PRICED=sum(1 for _, c in s if c == "PRICED"),
                         SCORED=sum(1 for _, c in s if c == "SCORED"),
                         UNRESOLVED=sum(1 for _, c in s if c == "UNRESOLVED"),
                         klass=file_class(s)))
    A = pd.DataFrame(rows)

    miss = 0
    for fn, want in HAND.items():
        r = A[A.file == fn]
        if len(r) != 1:
            miss += 1
            print(f"  [G_CLS] {fn}: NOT FOUND")
            continue
        r = r.iloc[0]
        ok = (r.klass == want) or (r.klass == "BOTH" and want == "SCORED" and r.SCORED > 0)
        miss += (not ok)
        print(f"  [G_CLS] {fn:<62s} want {want:<7s} got {r.klass:<12s} "
              f"(sites {r.sites}: P{r.PRICED} S{r.SCORED} U{r.UNRESOLVED}) "
              f"{'ok' if ok else 'MISS'}")
    gate("G_CLS classifier vs 6 hand-established files (misses)", float(miss), 0.0)

    wb = A[A.sites > 0]
    print(f"\n  {len(A)} committed python files scanned; {len(wb)} build an all-names book "
          f"({int(A.sites.sum())} construction sites).")
    tab = wb.groupby("klass").agg(files=("file", "size"), sites=("sites", "sum")).reset_index()
    print("\n  BY CONVENTION (files that build an all-names book):")
    print(fmt(tab.sort_values("files", ascending=False)))
    clsd = int(wb.klass.isin(["PRICED", "SCORED", "BOTH"]).sum())
    npriced = int((wb.klass == "PRICED").sum())
    print(f"\n  => of the {clsd} files the classifier resolves, {npriced} "
          f"({100*npriced/clsd:.1f}%) are PRICED and "
          f"{int((wb.klass=='SCORED').sum())} are SCORED "
          f"({int((wb.klass=='BOTH').sum())} carry both).  "
          f"{int((wb.klass=='UNRESOLVED').sum())} files unresolved and reported as such.")
    print("\n  the SCORED / BOTH files (the whole population):")
    print(fmt(wb[wb.klass.isin(["SCORED", "BOTH"])][["file", "sites", "PRICED", "SCORED",
                                                     "klass"]]))
    print("\n  the UNRESOLVED files:")
    print(fmt(wb[wb.klass == "UNRESOLVED"][["file", "sites", "UNRESOLVED"]]))

    # ---- map onto the LEADERBOARD rows those scripts back
    lb = (ROOT / "research" / "LEADERBOARD.md").read_text().splitlines()
    lb_rows = [l for l in lb if l.startswith("|") and l.count("|") >= 9]
    script_of = {}
    for l in lb_rows:
        cells = [c.strip() for c in l.split("|")]
        s = cells[-2] if len(cells) >= 2 else ""
        script_of[s] = script_of.get(s, 0) + 1
    kl = dict(zip(A.file, A.klass))
    L = pd.DataFrame([dict(script=Path(s).name, rows=n,
                           klass=kl.get(Path(s).name if Path(s).name.endswith(".py")
                                        else Path(s).name + ".py", "unmatched"))
                      for s, n in script_of.items()])
    agg = (L.groupby("klass").agg(scripts=("script", "size"), rows=("rows", "sum"))
           .reset_index().sort_values("rows", ascending=False))
    print(f"\n  LEADERBOARD rows ({int(L.rows.sum())} parsed) by the convention of the script "
          f"that produced them:")
    print(fmt(agg))
    sc = int(agg[agg.klass == "SCORED"].rows.sum()) + int(agg[agg.klass == "BOTH"].rows.sum())
    pr = int(agg[agg.klass == "PRICED"].rows.sum())
    print(f"\n  => {pr} committed rows sit on a PRICED all-names book, {sc} on a SCORED or "
          f"mixed one.")
    A.to_csv(f"{OUT}.audit.csv", index=False)
    L.to_csv(f"{OUT}.audit_rows.csv", index=False)
    return A, L


# =====================================================================================
# B.  THE CAUSAL TEST — 2x2 plus a seed panel
# =====================================================================================
def d3_one(uname, px, start, seed, keepsets):
    """One seed: both conventions on the SAME draws, same arms, one pipeline."""
    out = []
    for d, keep in enumerate(keepsets):
        sub = px.iloc[:, keep]
        comp = H.composite(sub)                       # shared: depends on the draw only
        gates = {g: H.gate_mask(sub, g) for g in H.GATES}
        for conv in CONVS:
            Wc = allnames_weights(sub, conv, comp=comp)
            rc = H.run(sub, Wc, bps=PCOST)["r"].loc[start:]
            for name, kind, kwargs, (g, cv) in ARMS:
                Wa = (Wc if g is None
                      else allnames_weights(sub, conv, comp=comp, gate_mask=gates[g],
                                            rw=(cv == "rw")))
                ra = H.run(sub, Wa, bps=PCOST, **kwargs)["r"].loc[start:]
                rec = dict(uni=uname, seed=seed, conv=conv, draw=d, arm=name)
                for w in ("full", "IS", "OOS"):
                    dc, dd, rt = dpair(win(rc, w), win(ra, w))
                    rec[f"dCAGR_{w}"], rec[f"dMaxDD_{w}"], rec[f"rate_{w}"] = dc, dd, rt
                out.append(rec)
    return pd.DataFrame(out)


def d3_agg(B, floored=False):
    """frac_pos per (uni, seed, conv, arm).  floored=True applies idea 382's amendment:
    only draws whose |dMaxDD| clears idea 94's 0.10 pp floor are counted."""
    b = B.copy()
    if floored:
        b = b[b.dMaxDD_full.abs() > FLOOR]
    g = b.groupby(["uni", "seed", "conv", "arm"])
    D = g.agg(frac_pos_full=("dMaxDD_full", lambda s: float((s > 0).mean())),
              frac_pos_IS=("dMaxDD_IS", lambda s: float((s > 0).mean())),
              frac_pos_OOS=("dMaxDD_OOS", lambda s: float((s > 0).mean())),
              ndraw=("dMaxDD_full", "size")).reset_index()
    return D


def repro_gate(D, path, book_label, seed, tag):
    """Compare our frac_pos at (seed, q=0.10) against a committed d3.csv ALL/TOPall row set."""
    f = Path(f"{path}.d3.csv")
    if not f.exists():
        gate(f"{tag} committed d3.csv present", 1.0, 0.0)
        return
    ref = pd.read_csv(f)
    ref = ref[(ref.q == Q_STAR) & (ref.book == book_label)]
    conv = "SCORED" if book_label == "TOPALL" else "PRICED"
    ours = D[(D.seed == seed) & (D.conv == conv)]
    m = ref.merge(ours, on=["uni", "arm"], suffixes=("_ref", "_new"), how="inner")
    if not len(m):
        gate(f"{tag} rows matched", 1.0, 0.0)
        return
    worst = 0.0
    for c in ("frac_pos_full", "frac_pos_IS", "frac_pos_OOS"):
        worst = max(worst, float((m[f"{c}_ref"] - m[f"{c}_new"]).abs().max()))
    gate(f"{tag} ({len(m)} arm-rows, q={Q_STAR}, seed {seed})", worst, 1e-12)


def causal(BIG):
    print("\n" + RULE)
    print("B.  THE CAUSAL TEST — is the archived 5-point gap the DENOMINATOR or the SEED?")
    print(RULE)
    res = {}
    for floored in (False, True):
        lab = "FLOORED (idea 382 amendment)" if floored else "AS THE RECORD COMPUTES IT"
        D = d3_agg(BIG, floored)
        cell = (D.groupby(["uni", "seed", "conv"]).frac_pos_full.mean().rename("mean_fp")
                .reset_index())
        print(f"\n  B1. mean D3 frac_pos_full by (panel, seed, convention) — {lab}")
        piv = cell.pivot_table(index=["uni", "seed"], columns="conv", values="mean_fp")
        piv["gap_S_minus_P"] = piv.SCORED - piv.PRICED
        print(piv.to_string(float_format=lambda x: f"{x:.4f}"))

        gaps = piv.gap_S_minus_P
        pooled = cell.groupby(["seed", "conv"]).mean_fp.mean().unstack()
        pooled["gap"] = pooled.SCORED - pooled.PRICED
        n = len(pooled)
        g_mean, g_sd = float(pooled.gap.mean()), float(pooled.gap.std(ddof=1))
        tstat = g_mean / (g_sd / np.sqrt(n)) if g_sd > 0 else np.inf
        # across-seed spread WITHIN a convention (what a seed alone can move)
        sd_within = {c: float(pooled[c].std(ddof=1)) for c in CONVS}
        # the archived, confounded contrast: SCORED@20260905 vs PRICED@20260907
        arch = float(pooled.loc[SEED_B2, "SCORED"] - pooled.loc[SEED_B, "PRICED"])
        print(f"\n  B2. matched-seed gap (SCORED - PRICED, same draws), {n} seeds, pooled panels:")
        print(f"      mean {g_mean:+.4f}   sd {g_sd:.4f}   t {tstat:+.2f}   "
              f"range [{pooled.gap.min():+.4f}, {pooled.gap.max():+.4f}]   "
              f"sign {int((pooled.gap > 0).sum())}/{n} positive")
        print(f"      across-seed SD WITHIN a convention: PRICED {sd_within['PRICED']:.4f}, "
              f"SCORED {sd_within['SCORED']:.4f}")
        print(f"      the ARCHIVED (confounded) contrast SCORED@{SEED_B2} - PRICED@{SEED_B} "
              f"= {arch:+.4f}")
        print(f"      => of that {arch:+.4f}, the DENOMINATOR explains {g_mean:+.4f} "
              f"({100*g_mean/arch if arch else np.nan:.1f}%) and the SEED the remaining "
              f"{arch - g_mean:+.4f}.")
        res[floored] = dict(piv=piv, pooled=pooled, mean=g_mean, sd=g_sd, t=tstat,
                            arch=arch, sd_within=sd_within, n=n)

    print("\n  B3. PRE-REGISTERED VERDICT")
    r = res[False]
    h1 = abs(r["mean"]) > 2 * r["sd"] / np.sqrt(r["n"]) and abs(r["mean"]) >= 0.5 * abs(r["arch"])
    print(f"      H1 (denominator effect, matched-seed gap != 0 and >= half the archived gap): "
          f"{'RETAINED' if h1 else 'NOT RETAINED'}")
    inside = abs(r["arch"]) <= 3 * max(r["sd_within"].values())
    print(f"      H0 (seed artefact: archived gap inside +/-3 within-convention seed SD "
          f"= +/-{3*max(r['sd_within'].values()):.4f}): {'RETAINED' if inside else 'NOT RETAINED'}")
    return res


# =====================================================================================
# C.  THE PRICE, KEEP PATHS, RULE 8
# =====================================================================================
def m3(r):
    m = metrics(r)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def price_grid(uname, px, start):
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    sm, s1, s2 = m3(spy), None, None
    sm_oos = metrics(spy.loc[OOS_START:])
    v2 = {c: backtest(px, rules_v2_weights(px), cost_bps=c, freq=H.FREQ)["returns"].loc[start:]
          for c in COST_RUNGS}
    v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=H.FREQ)["returns"].loc[start:]
          for c in COST_RUNGS}
    comp = H.composite(px)
    band = H.gate_mask(px, "band3")
    rows, rets = [], {}
    for conv in CONVS:
        for form in ("ungated", "band3-dg(live form)"):
            gm = None if form == "ungated" else band
            for g in GROSSES:
                W = allnames_weights(px, conv, gross=g, comp=comp, gate_mask=gm)
                for c in COST_RUNGS:
                    r = backtest(px, W, cost_bps=c, freq=H.FREQ)["returns"].loc[start:]
                    rets[(conv, form, g, c)] = r
                    d = m3(r)
                    b = m3(v2[c])
                    rows.append(dict(uni=uname, conv=conv, form=form, gross=g, bps=c,
                                     CAGR=d["CAGR"], Sharpe=d["Sharpe"], MaxDD=d["MaxDD"],
                                     H1=d["H1"], H2=d["H2"],
                                     OOS_Sharpe=metrics(r.loc[OOS_START:])["Sharpe"],
                                     IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                                     OOS_CAGR=metrics(r.loc[OOS_START:])["CAGR"],
                                     OOS_MaxDD=metrics(r.loc[OOS_START:])["MaxDD"],
                                     v2_Sharpe=b["Sharpe"],
                                     pass4a=bool(d["H1"] > b["H1"] and d["H2"] > b["H2"]
                                                 and d["MaxDD"] >= b["MaxDD"]),
                                     pass4b=bool(d["H1"] > sm["H1"] and d["H2"] > sm["H2"]
                                                 and metrics(r.loc[OOS_START:])["Sharpe"]
                                                 > sm_oos["Sharpe"]
                                                 and abs(d["MaxDD"]) <= 0.60 * abs(sm["MaxDD"])
                                                 and d["CAGR"] >= 0.70 * sm["CAGR"])))
    G = pd.DataFrame(rows)
    return G, rets, spy, v2, v1, sm, sm_oos


def walk_forward(uname, G, rets, spy, v2):
    """Rule 8: choose (convention, gross) on IS <= 2016 by IS Sharpe, per gate form; evaluate
    OOS >= 2017 untouched.  Reported at every cost rung."""
    out = []
    for form in G.form.unique():
        for c in COST_RUNGS:
            s = G[(G.form == form) & (G.bps == c)]
            pick = s.loc[s.IS_Sharpe.idxmax()]
            r = rets[(pick.conv, form, pick.gross, c)]
            bo = metrics(v2[c].loc[OOS_START:])
            so = metrics(spy.loc[OOS_START:])
            out.append(dict(uni=uname, form=form, bps=c, pick_conv=pick.conv,
                            pick_gross=pick.gross, IS_Sharpe=pick.IS_Sharpe,
                            OOS_CAGR=metrics(r.loc[OOS_START:])["CAGR"],
                            OOS_Sharpe=metrics(r.loc[OOS_START:])["Sharpe"],
                            OOS_MaxDD=metrics(r.loc[OOS_START:])["MaxDD"],
                            v2_OOS_Sharpe=bo["Sharpe"], v2_OOS_CAGR=bo["CAGR"],
                            v2_OOS_MaxDD=bo["MaxDD"],
                            SPY_OOS_Sharpe=so["Sharpe"], SPY_OOS_CAGR=so["CAGR"],
                            SPY_OOS_MaxDD=so["MaxDD"],
                            # what the OTHER convention would have done at the same gross
                            alt_OOS_Sharpe=metrics(
                                rets[("SCORED" if pick.conv == "PRICED" else "PRICED",
                                      form, pick.gross, c)].loc[OOS_START:])["Sharpe"]))
    return pd.DataFrame(out)


# =====================================================================================
def main():
    t00 = time.time()
    print(RULE)
    print("IDEA 380 — the SCORED vs PRICED denominator.  Lane B, 2026-09-07.")
    print(f"Tuned params: convention x gross ({len(CONVS)} x {len(GROSSES)}).  "
          f"D3: q={Q_STAR}, tau={TAU_STAR}, NDRAW={NDRAW}, {len(SEEDS)} seeds, "
          f"{len(ARMS)} arms, both panels.  Costs {COST_RUNGS} bps.  ALL points reported.")
    print(RULE)

    panels = {}
    for uname, kw in PANELS:
        px = H.load_universe(**kw)
        panels[uname] = (px, px.index[260])

    # ---------------- gates -------------------------------------------------------
    print("\nGATES")
    worst_r = worst_t = 0.0
    for uname, (px, start) in panels.items():
        comp = H.composite(px)
        for conv in CONVS:
            W = allnames_weights(px, conv, comp=comp)
            for c in (0.0, 25.0):
                a = H.run(px, W, bps=c)
                b = backtest(px, W, cost_bps=c, freq=H.FREQ)
                worst_r = max(worst_r, float((a["r"].loc[start:]
                                              - b["returns"].loc[start:]).abs().max()))
                worst_t = max(worst_t, float((a["to"].loc[start:]
                                              - b["turnover"].loc[start:]).abs().max()))
    gate("G1a H.run == engine.backtest RETURNS @0/25bps", worst_r, 1e-12)
    gate("G1b H.run == engine.backtest TURNOVER @0/25bps", worst_t, 1e-12)

    px56, st56 = panels["universe.json(56)"]
    wp = allnames_weights(px56, "PRICED")
    gate("G2  PRICED book == idea 94 H.targets(EWall)",
         float((wp - H.targets(px56, "EWall")).abs().to_numpy().max()), 1e-15)

    ws = allnames_weights(px56, "SCORED")
    dw = float((ws - wp).abs().loc[st56:].to_numpy().max())
    ncomp = H.composite(px56).notna().sum(axis=1).loc[st56:]
    npri = px56.notna().sum(axis=1).loc[st56:]
    ndis, ntot = int((ncomp != npri).sum()), len(ncomp)
    gate("G3a idea 380's filed max|dw| = 0.0150", abs(dw - 0.0150), 1e-4)
    gate("G3b idea 380's filed 1530 of 4439 disagreeing u56 eval days",
         float(abs(ndis - 1530) + abs(ntot - 4439)), 0.0)
    print(f"       [construction] max|dw| {dw:.4f}; SCORED holds {ncomp.mean():.1f} names on "
          f"average vs PRICED {npri.mean():.1f} (panel {px56.shape[1]}); disagree "
          f"{ndis}/{ntot} eval days")

    # ---------------- B: the seed x convention panel ------------------------------
    print("\nrunning the D3 panel (both conventions on identical draws, "
          f"{len(SEEDS)} seeds x {len(PANELS)} panels x {NDRAW} draws) ...", flush=True)
    frames = []
    for uname, (px, start) in panels.items():
        ds = {s: draw_sets(px.shape[1], s)[Q_STAR] for s in SEEDS}
        for s in SEEDS:
            t0 = time.time()
            frames.append(d3_one(uname, px, start, s, ds[s]))
            print(f"    [{uname}] seed {s} done ({time.time()-t0:.0f}s, "
                  f"{time.time()-t00:.0f}s elapsed)", flush=True)
    BIG = pd.concat(frames, ignore_index=True)
    BIG.to_csv(f"{OUT}.bootstrap.csv", index=False)
    D = d3_agg(BIG)
    D.to_csv(f"{OUT}.d3.csv", index=False)

    print()
    repro_gate(D, I124_B2, "TOPALL", SEED_B2, "G4  reproduce _B2 committed d3 (SCORED ALL)")
    repro_gate(D, I124_B, "TOPall", SEED_B, "G5  reproduce _B  committed d3 (PRICED ALL)")

    A, L = audit()
    res = causal(BIG)

    # ---------------- C: price, KEEP paths, rule 8 --------------------------------
    print("\n" + RULE)
    print("C.  THE PRICE — what the convention is worth in return space")
    print(RULE)
    Gs, WFs = [], []
    for uname, (px, start) in panels.items():
        G, rets, spy, v2, v1, sm, sm_oos = price_grid(uname, px, start)
        Gs.append(G)
        WFs.append(walk_forward(uname, G, rets, spy, v2))
        print(f"\n  {uname}: SPY CAGR {sm['CAGR']:.2%} Sharpe {sm['Sharpe']:.3f} "
              f"MaxDD {sm['MaxDD']:.2%} halves {sm['H1']:.3f}/{sm['H2']:.3f} "
              f"OOS Sharpe {sm_oos['Sharpe']:.3f} | RULES v2 @10bps Sharpe "
              f"{m3(v2[10.0])['Sharpe']:.3f} MaxDD {m3(v2[10.0])['MaxDD']:.2%}")
        print(f"  ALL {len(G)} grid points ({len(CONVS)} conv x 2 forms x {len(GROSSES)} "
              f"gross x {len(COST_RUNGS)} bps):")
        print(fmt(G.drop(columns=["uni"])))
        # the paired convention delta at matched (form, gross, cost)
        k = ["form", "gross", "bps"]
        p = G.pivot_table(index=k, columns="conv",
                          values=["CAGR", "Sharpe", "MaxDD", "OOS_Sharpe"])
        d = pd.DataFrame({c: p[(c, "SCORED")] - p[(c, "PRICED")]
                          for c in ("CAGR", "Sharpe", "MaxDD", "OOS_Sharpe")}).reset_index()
        print(f"\n  SCORED - PRICED at matched (form, gross, cost), {len(d)} pairs:")
        print(fmt(d))
        print(f"    median |dSharpe| {d.Sharpe.abs().median():.5f}, max "
              f"{d.Sharpe.abs().max():.5f}; median |dCAGR| {d.CAGR.abs().median():.5%}, "
              f"max {d.CAGR.abs().max():.5%}; sign(dSharpe) "
              f"{int((d.Sharpe>0).sum())}+/{int((d.Sharpe<0).sum())}-/"
              f"{int((d.Sharpe==0).sum())}0")

    GG = pd.concat(Gs, ignore_index=True)
    WF = pd.concat(WFs, ignore_index=True)
    GG.to_csv(f"{OUT}.grid.csv", index=False)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)

    print("\n" + RULE)
    print("KEEP PATHS — every one of the "
          f"{len(GG)} priced cells, both paths, all cost rungs")
    print(RULE)
    for c in COST_RUNGS:
        s = GG[GG.bps == c]
        print(f"  @{c:>4.0f} bps:  4a {int(s.pass4a.sum())}/{len(s)}   "
              f"4b {int(s.pass4b.sum())}/{len(s)}")
    if GG.pass4a.any():
        print("\n  4a passers:")
        print(fmt(GG[GG.pass4a]))
    if GG.pass4b.any():
        print("\n  4b passers:")
        print(fmt(GG[GG.pass4b]))
    print(f"\n  4a total {int(GG.pass4a.sum())}/{len(GG)}, "
          f"4b total {int(GG.pass4b.sum())}/{len(GG)} over all cost rungs.")

    print("\n" + RULE)
    print("RULE 8 — (convention, gross) chosen on IS <= 2016 only, evaluated 2017-2026")
    print(RULE)
    print(fmt(WF))
    same = WF.pick_conv.value_counts().to_dict()
    print(f"\n  the IS chooser picks: {same}")
    print(f"  |OOS Sharpe(pick) - OOS Sharpe(other convention, same gross)|: "
          f"median {(WF.OOS_Sharpe - WF.alt_OOS_Sharpe).abs().median():.5f}, "
          f"max {(WF.OOS_Sharpe - WF.alt_OOS_Sharpe).abs().max():.5f}")
    print(f"  picks above SPY OOS Sharpe: "
          f"{int((WF.OOS_Sharpe > WF.SPY_OOS_Sharpe).sum())}/{len(WF)}; "
          f"above RULES v2 OOS Sharpe: "
          f"{int((WF.OOS_Sharpe > WF.v2_OOS_Sharpe).sum())}/{len(WF)}")

    # ---------------- the live book, exactly --------------------------------------
    print("\n" + RULE)
    print("D.  THE LIVE BOOK — what switching RULES v2's denominator would actually do")
    print(RULE)
    live = []
    for uname, (px, start) in panels.items():
        comp = H.composite(px)
        band = H.gate_mask(px, "band3")
        for conv in CONVS:
            W = allnames_weights(px, conv, gross=H.GROSS, comp=comp, gate_mask=band)
            r = backtest(px, W, cost_bps=PCOST, freq=H.FREQ)["returns"].loc[start:]
            d = m3(r)
            live.append(dict(uni=uname, conv=conv, **d,
                             OOS_Sharpe=metrics(r.loc[OOS_START:])["Sharpe"]))
        rv2 = backtest(px, rules_v2_weights(px), cost_bps=PCOST,
                       freq=H.FREQ)["returns"].loc[start:]
        live.append(dict(uni=uname, conv="rules_v2_weights (live, for reference)", **m3(rv2),
                         OOS_Sharpe=metrics(rv2.loc[OOS_START:])["Sharpe"]))
    LV = pd.DataFrame(live)
    print(fmt(LV))
    LV.to_csv(f"{OUT}.live.csv", index=False)
    pd.DataFrame(GATE_LOG).to_csv(f"{OUT}.gates.csv", index=False)

    print("\n" + RULE)
    print(f"gates: {sum(g['passed'] for g in GATE_LOG)}/{len(GATE_LOG)} passed.  "
          f"total {time.time()-t00:.0f}s")
    print(RULE)


if __name__ == "__main__":
    main()
