#!/usr/bin/env python3
"""QUEUE idea 1213 - do the RECORD's OTHER COUNT-CORRECTIONS STATE THEIR OWN DOMAIN?

Idea 1207 found 78 of 96 of 1155's checkable units (0.8125) carry a harvested count
OUTSIDE d2's tabulated k = 2..12 domain, so their inflation was a CLIPPED CONSTANT.
d2 is not the only correction the record applies.  Every count- or size-correction has
a domain: subsample / size matching, SE / sqrt(n), block-length scaling, multiple-test
widening and sqrt(252) annualisation all do.  This run censuses them for whether ANY
states its own domain, re-reads the out-of-domain units separately, and then PRICES the
question on real books: if an out-of-domain correction is a clipped constant it cannot
reorder a ladder, so a domain-aware chooser and a domain-blind one must make the same
pick -- or the record has been adjudicating on a constant.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
    CORRECTION SET  {C_D2, C_COUNT, C_ALL}
  x DOMAIN RULE     {R_TABULATED, R_STATED, R_LOOSE}
  = 9 cells, EVERY ONE PUBLISHED.

NOT dials, reported at every value: PANEL {U56, B136, SMALL}; the four ladders
LAD_N6 (k=6, in d2 domain) / LAD_N14 (k=14, OUT) / LAD_G8 (k=8, in) / LAD_G16 (k=16, OUT);
the 4a and 4b legs; the rule-8 walk-forward.  10 bps, t+1 execution (engine), weekly
cadence, 260-row warm-up.  Book construction frozen at the 2026-09-04 KEEP-4b candidate's:
composite (12-1 + 6m + 3m percentile ranks), NO vol scaler, above-own-200d-MA eligibility,
top-N equal weight at g/N of NAV, gated-out weight to CASH at 0%.

SURVIVORSHIP: universe.json / universe_broad.json are CURRENT constituents; the small
panel is the current output of a sub-$2B screen (data/SMALL_PANEL_README.md).  Names whose
max_1d_move >= 1.0 are dropped from the small panel before anything is computed.  The
label SMALL439 no longer denotes this pool: the committed file carries 715 rows and 664
survive the move filter (idea 1074's open rename question).

Run:  python3 research/backtests/2026-09-17_do-the-RECORD-s-OTHER-COUNT-CORRECTIONS-STATE-THEIR-OWN-DOMAIN_cloud.py
"""
from __future__ import annotations
import re, sys, json, itertools
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights          # noqa: E402
from engine import backtest, metrics                           # noqa: E402

OUT = Path(__file__).with_suffix("")
SEED = 1213
COST_BPS = 10
FREQ = "W"
WARMUP = 260
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

# ---------------------------------------------------------------------------
# (0) THE ARITHMETIC, PRINTED BEFORE ANY TEXT OR ANY PRICE IS READ.
# ---------------------------------------------------------------------------
# d2(k) is Hartley's constant: E[range of k iid N(0,1) draws].  It is TABULATED for
# k = 2..12.  The record's habit when k > 12 is to CLIP at d2(12) (idea 1207).  Clipping
# makes the correction a CONSTANT in k, so for two ladders of different length both above
# 12 the count correction contributes EXACTLY 1.0 to their ratio and cannot order them.
# That is an arithmetic fact, gated below (G0), not an empirical finding.
D2 = {2: 1.128, 3: 1.693, 4: 2.059, 5: 2.326, 6: 2.534, 7: 2.704,
      8: 2.847, 9: 2.970, 10: 3.078, 11: 3.173, 12: 3.258}
D2_KMIN, D2_KMAX = 2, 12


def d2(k, clip=True):
    """d2(k).  clip=True is the RECORD's practice (constant above the table);
    clip=False returns NaN out of domain, i.e. refuses to correct."""
    k = int(k)
    if k in D2:
        return D2[k]
    if not clip:
        return np.nan
    return D2[D2_KMAX] if k > D2_KMAX else D2[D2_KMIN]


# Pre-declared outcomes for the census leg, written before the corpus was read:
#   (A) MANY  >= 10 corrections state their own domain
#   (B) FEW   1-9 state it
#   (C) NONE  zero state it
#   (D) UNTRACEABLE  the corrections cannot be located in the corpus at all
CENSUS_OUTCOMES = ("A_MANY>=10", "B_FEW_1_9", "C_NONE", "D_UNTRACEABLE")

# ---------------------------------------------------------------------------
# PART A - THE CENSUS
# ---------------------------------------------------------------------------
# Correction families and their domains, each stated from the correction's OWN
# definition, not from the record's usage.
CORRECTIONS = {
    "D2":        dict(domain="k in [2,12] (Hartley table)",  lo=2,  hi=12,
                      pat=r"\bd2\b|\bd_?2\s*\(|count[- ]match|count inflation|hartley"),
    "SUBSAMPLE": dict(domain="matched size m, 1 <= m <= min(pool sizes); both sizes stated",
                      lo=1, hi=10**9,
                      pat=r"subsample|sub-sample|size[- ]match|gross[- ]matched|matched sub|size matched|matched pool"),
    "SE_SQRTN":  dict(domain="n >= 2 exchangeable draws", lo=2, hi=10**9,
                      pat=r"se\s*/\s*sqrt|/\s*sqrt\(\s*n|sqrt\(\s*n\s*\)|standard error of the mean|sem\b"),
    "BLOCK_L":   dict(domain="1 <= L <= T/2 (T = 4198..4706 rows here -> L <= 2099)",
                      lo=1, hi=2099,
                      pat=r"block length|block[- ]bootstrap|moving[- ]block|block permutation|\bL\s*=\s*\d+"),
    "MULTTEST":  dict(domain="m >= 2 simultaneous tests, m stated", lo=2, hi=10**9,
                      pat=r"bonferroni|multiple[- ]test|family[- ]wise|\bfwer\b|\bfdr\b|benjamini"),
    "ANNUAL":    dict(domain="p periods per year, p stated and matching the bar frequency",
                      lo=1, hi=10**9,
                      pat=r"sqrt\(\s*252|annualis|annualiz|\bper[- ]?annum\b|/yr\b"),
}
SETS = {
    "C_D2":    ["D2"],
    "C_COUNT": ["D2", "SUBSAMPLE", "SE_SQRTN"],
    "C_ALL":   ["D2", "SUBSAMPLE", "SE_SQRTN", "BLOCK_L", "MULTTEST", "ANNUAL"],
}
RULES = ("R_TABULATED", "R_STATED", "R_LOOSE")

# Count cue, inherited WHOLE from 1155/1207 so the comparison is like-for-like.
COUNT_NOUNS = (r"rungs?|cells?|points?|books?|rows?|panels?|names?|draws?|seeds?|folds?|"
               r"tests?|blocks?|days?|reps?|replications?|bars?|windows?|arms?|legs?")
COUNT_CUE = re.compile(r"(\d[\d,]*)\s*(?:" + COUNT_NOUNS + r")\b", re.I)

# "States its own domain": the unit names the correction's range of validity.
DOMAIN_TOKEN = re.compile(
    r"\bdomain\b|\btabulat|\bvalid (?:for|range|only)|\bdefined (?:for|only)|"
    r"\bonly valid\b|\bin-domain\b|\bout-of-domain\b|2\s*\.\.\s*12|k\s*=\s*2\s*(?:to|-|\.\.)\s*12|"
    r"\brange of validity\b|\bapplicab\w*\s+(?:for|range|to)\b|\brequires?\s+k\b|\bout of domain\b",
    re.I)

VERDICT_TOKEN = re.compile(r"\b(KEEP|KILL|PARK|PASS(?:ES|ED)?|FAIL(?:S|ED)?)\b")


def corpus_units():
    """One unit = one LEADERBOARD row, one CHANGELOG paragraph, or one paragraph of any
    other committed markdown artefact under research/.  Same unit definition as 1155/1207."""
    units = []
    lb = ROOT / "research" / "LEADERBOARD.md"
    for i, line in enumerate(lb.read_text(errors="replace").split("\n")):
        if line.strip():
            units.append(dict(src="LEADERBOARD.md", loc=str(i + 1), text=line))
    for p in sorted(ROOT.rglob("*.md")):
        if p == lb or ".git" in p.parts:
            continue
        try:
            txt = p.read_text(errors="replace")
        except Exception:
            continue
        rel = str(p.relative_to(ROOT))
        for j, para in enumerate(re.split(r"\n\s*\n", txt)):
            if para.strip():
                units.append(dict(src=rel, loc=f"p{j + 1}", text=para))
    return units


def harvest_count(text, m):
    """The count cue NEAREST the correction token (1155/1207's harvest, unchanged)."""
    best, bestd = None, 10 ** 9
    for c in COUNT_CUE.finditer(text):
        d = min(abs(c.start() - m.start()), abs(c.start() - m.end()))
        if d < bestd:
            bestd, best = d, c
    if best is None:
        return None
    try:
        return int(best.group(1).replace(",", ""))
    except ValueError:
        return None


def run_census():
    units = corpus_units()
    print(f"\n[A] CORPUS: {len(units):,} units "
          f"({sum(u['src'] == 'LEADERBOARD.md' for u in units):,} LEADERBOARD rows, "
          f"{len(set(u['src'] for u in units)):,} distinct files)")

    hits = []   # one row per (unit, correction) invocation
    for u in units:
        t = u["text"]
        for key, spec in CORRECTIONS.items():
            m = re.search(spec["pat"], t, re.I)
            if not m:
                continue
            k = harvest_count(t, m)
            hits.append(dict(src=u["src"], loc=u["loc"], correction=key,
                             k=k, states_domain=bool(DOMAIN_TOKEN.search(t)),
                             has_verdict=bool(VERDICT_TOKEN.search(t)),
                             text=t[:300].replace("\n", " ")))
    H = pd.DataFrame(hits)
    H.to_csv(OUT.with_suffix(".census_hits.csv"), index=False)
    print(f"[A] {len(H):,} correction invocations over {H.src.nunique()} files; "
          f"by family:\n{H.correction.value_counts().to_string()}")

    def in_domain(row, rule):
        spec = CORRECTIONS[row.correction]
        if rule == "R_LOOSE":
            return bool(row.k is not None and not pd.isna(row.k) and row.k > 0)
        if rule == "R_STATED":
            return bool(row.states_domain)
        # R_TABULATED
        if row.k is None or pd.isna(row.k):
            return False
        return bool(spec["lo"] <= row.k <= spec["hi"])

    rows = []
    for sname, fams in SETS.items():
        sub = H[H.correction.isin(fams)]
        for rule in RULES:
            ind = sub.apply(lambda r: in_domain(r, rule), axis=1) if len(sub) else pd.Series(dtype=bool)
            out = sub[~ind] if len(sub) else sub
            rows.append(dict(
                correction_set=sname, domain_rule=rule,
                n_units=len(sub),
                n_states_domain=int(sub.states_domain.sum()) if len(sub) else 0,
                share_states_domain=float(sub.states_domain.mean()) if len(sub) else np.nan,
                n_k_recovered=int(sub.k.notna().sum()) if len(sub) else 0,
                n_in_domain=int(ind.sum()) if len(sub) else 0,
                n_out_of_domain=len(out),
                share_out=len(out) / len(sub) if len(sub) else np.nan,
                out_carrying_verdict=int(out.has_verdict.sum()) if len(out) else 0,
                share_out_carrying_verdict=float(out.has_verdict.mean()) if len(out) else np.nan,
            ))
    C = pd.DataFrame(rows)
    C.to_csv(OUT.with_suffix(".census.csv"), index=False)
    print("\n[A] THE 9 CELLS, EVERY ONE PUBLISHED:")
    print(C.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # per-family detail, reported at every value (not a dial)
    fam = []
    for key, spec in CORRECTIONS.items():
        s = H[H.correction == key]
        if not len(s):
            fam.append(dict(correction=key, domain=spec["domain"], n=0))
            continue
        k = s.k.dropna()
        tab = s.apply(lambda r: (r.k is not None and not pd.isna(r.k)
                                 and spec["lo"] <= r.k <= spec["hi"]), axis=1)
        fam.append(dict(correction=key, domain=spec["domain"], n=len(s),
                        n_states_domain=int(s.states_domain.sum()),
                        share_states_domain=s.states_domain.mean(),
                        n_k_recovered=int(k.size), median_k=float(k.median()) if k.size else np.nan,
                        max_k=float(k.max()) if k.size else np.nan,
                        share_in_domain_tabulated=float(tab.mean()),
                        n_out_with_verdict=int(s[~tab].has_verdict.sum())))
    F = pd.DataFrame(fam)
    F.to_csv(OUT.with_suffix(".census_by_family.csv"), index=False)
    print("\n[A] PER FAMILY (not a dial - every value reported):")
    print(F.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    total_stating = int(H.states_domain.sum())
    outcome = (CENSUS_OUTCOMES[3] if len(H) == 0 else
               CENSUS_OUTCOMES[2] if total_stating == 0 else
               CENSUS_OUTCOMES[1] if total_stating < 10 else CENSUS_OUTCOMES[0])
    print(f"\n[A] PRE-DECLARED OUTCOME REACHED: {outcome} "
          f"({total_stating:,} of {len(H):,} invocations state their own domain)")
    return H, C, F, outcome


# ---------------------------------------------------------------------------
# PART B - THE PRICE LEG (PROTOCOL rules 2, 3, 4, 8)
# ---------------------------------------------------------------------------
def panels():
    P = {}
    P["U56"] = load_universe()
    P["B136"] = load_universe(broad=True)
    ps = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    dropped = [c for c in ps.columns if c in bad]
    ps = ps.drop(columns=dropped)
    print(f"[B] SMALL: dropped {len(dropped)} names with max_1d_move >= 1.0; "
          f"{ps.shape[1] - 1} tradable + SPY benchmark")
    P["SMALL"] = ps
    return P


def book_weights(px, N, g, tradable):
    """2026-09-04 KEEP-4b construction, frozen."""
    q = px[tradable]
    mom = q.shift(21) / q.shift(252) - 1
    r6 = q / q.shift(126) - 1
    r3 = q / q.shift(63) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3
    above = q > q.rolling(200).mean()
    rank = comp.where(above).rank(axis=1, ascending=False)
    w = (rank <= N).astype(float) * (g / N)
    return w.reindex(columns=px.columns).fillna(0.0)


def run_book(px, N, g, tradable):
    r = backtest(px, book_weights(px, N, g, tradable), cost_bps=COST_BPS, freq=FREQ)
    return r["returns"].loc[px.index[WARMUP]:]


def block_se_sharpe(r, L=63, B=400, rng=None):
    """Moving-block bootstrap SE of the annualised Sharpe.  L = 63 is STATED (idea 1208's
    open complaint); it sits inside BLOCK_L's domain 1 <= L <= T/2."""
    rng = rng or np.random.default_rng(SEED)
    x = r.values
    n = len(x)
    nb = int(np.ceil(n / L))
    starts = rng.integers(0, n - L + 1, size=(B, nb))
    idx = (starts[:, :, None] + np.arange(L)[None, None, :]).reshape(B, -1)[:, :n]
    s = x[idx]
    mu, sd = s.mean(axis=1), s.std(axis=1)
    sh = np.where(sd > 0, mu * 252 / (sd * np.sqrt(252)), np.nan)
    return float(np.nanstd(sh))


def iid_se_sharpe(r):
    """SE / sqrt(n): the textbook iid Sharpe SE.  Domain n >= 2."""
    n = len(r)
    if n < 2:
        return np.nan
    S = sharpe(r)
    return float(np.sqrt((1 + 0.5 * S ** 2) / n) * np.sqrt(252) / np.sqrt(252))


def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mstats(r):
    m = metrics(r)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


LADDERS = {
    "LAD_N6":  dict(axis="N", rungs=[5, 10, 20, 30, 40, 60], anchor=20),
    "LAD_N14": dict(axis="N", rungs=[3, 5, 8, 10, 12, 15, 20, 25, 30, 40, 50, 60, 80, 100], anchor=20),
    "LAD_G8":  dict(axis="G", rungs=[0.30, 0.40, 0.50, 0.60, 0.70, 0.75, 0.85, 1.00], anchor=0.75),
    "LAD_G16": dict(axis="G", rungs=[round(0.25 + 0.05 * i, 2) for i in range(16)], anchor=0.75),
}
ANCHOR_N, ANCHOR_G = 20, 0.75


def correction_bar(k, se, fams, rule):
    """The bar the observed IS-Sharpe RANGE across k rungs must clear.

    Returns (bar, applied, why).  applied=False means the correction set is OUT OF ITS
    DOMAIN under this rule and the chooser must DECLINE TO MOVE (stay at the anchor)."""
    bar, notes = se, []
    ok = True
    for fam in fams:
        spec = CORRECTIONS[fam]
        if fam == "D2":
            if rule == "R_LOOSE":
                bar *= d2(k, clip=True); notes.append(f"d2clip({k})={d2(k, True):.3f}")
            else:
                v = d2(k, clip=False)
                if np.isnan(v):
                    ok = False; notes.append(f"d2 UNDEFINED at k={k}")
                else:
                    bar *= v; notes.append(f"d2({k})={v:.3f}")
        elif fam == "SE_SQRTN":
            if k < spec["lo"]:
                ok = False; notes.append("SE_SQRTN out of domain")
            else:
                notes.append("SE/sqrt(n) in domain")
        elif fam == "BLOCK_L":
            notes.append("L=63 in domain")
        elif fam == "SUBSAMPLE":
            notes.append("size-match in domain (rungs share one tape)")
        elif fam == "MULTTEST":
            if k < 2:
                ok = False; notes.append("MULTTEST out of domain")
            else:
                bar *= np.sqrt(2 * np.log(k)); notes.append(f"fwer x{np.sqrt(2 * np.log(k)):.3f}")
        elif fam == "ANNUAL":
            notes.append("p=252 stated")
    if rule == "R_STATED":
        # in-domain only if the ladder states its own k AND the correction's range;
        # our ladders state k, so this reduces to the tabulated test for D2.
        pass
    return bar, ok, "; ".join(notes)


def run_price_leg(P):
    rng = np.random.default_rng(SEED)
    # ---- books -------------------------------------------------------------
    books, bench = {}, {}
    for pname, px in P.items():
        tradable = [c for c in px.columns if c != "SPY"] if pname == "SMALL" else list(px.columns)
        need_N = sorted(set(LADDERS["LAD_N6"]["rungs"]) | set(LADDERS["LAD_N14"]["rungs"]))
        need_G = sorted(set(LADDERS["LAD_G8"]["rungs"]) | set(LADDERS["LAD_G16"]["rungs"]))
        for N in need_N:
            books[(pname, "N", N)] = run_book(px, N, ANCHOR_G, tradable)
        for g in need_G:
            books[(pname, "G", g)] = run_book(px, ANCHOR_N, g, tradable)
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        live = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        bench[pname] = dict(SPY=spy, LIVE=live)
        print(f"[B] {pname}: {len(need_N)} N-rungs + {len(need_G)} G-rungs built")

    # ---- benchmarks --------------------------------------------------------
    brows = []
    for pname, b in bench.items():
        for bn, r in b.items():
            d = mstats(r); d.update(panel=pname, series=bn, window="FULL")
            brows.append(d)
            o = r.loc[OOS_START:]; d2_ = mstats(o); d2_.update(panel=pname, series=bn, window="OOS")
            brows.append(d2_)
            i = r.loc[:IS_END]; d3 = mstats(i); d3.update(panel=pname, series=bn, window="IS")
            brows.append(d3)
    B = pd.DataFrame(brows)[["panel", "series", "window", "CAGR", "Sharpe", "MaxDD", "H1", "H2"]]
    B.to_csv(OUT.with_suffix(".benchmarks.csv"), index=False)
    print("\n[B] BENCHMARKS (10 bps, t+1, weekly baseline):")
    print(B.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- ladder statistics (IS only; OOS is read ONCE, at the end) ---------
    lrows = []
    for pname in P:
        for lname, spec in LADDERS.items():
            ax, rungs = spec["axis"], spec["rungs"]
            iss, ses = [], []
            for v in rungs:
                r = books[(pname, ax, v)].loc[:IS_END]
                iss.append(sharpe(r)); ses.append(block_se_sharpe(r, rng=rng))
            iss, ses = np.array(iss), np.array(ses)
            lrows.append(dict(panel=pname, ladder=lname, axis=ax, k=len(rungs),
                              rung_lo=rungs[0], rung_hi=rungs[-1],
                              is_range=float(iss.max() - iss.min()),
                              is_sd=float(iss.std(ddof=1)),
                              se_mean=float(ses.mean()),
                              is_argmax=rungs[int(np.argmax(iss))],
                              anchor=spec["anchor"],
                              d2_in_domain=bool(D2_KMIN <= len(rungs) <= D2_KMAX),
                              is_sharpes=";".join(f"{x:.4f}" for x in iss)))
    L = pd.DataFrame(lrows)
    L.to_csv(OUT.with_suffix(".ladders.csv"), index=False)
    print("\n[B] LADDERS, IS 2009-2016 ONLY (every rung's IS Sharpe in the CSV):")
    print(L.drop(columns=["is_sharpes"]).to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- G0 GATE: is the clipped correction really a constant? -------------
    g0 = all(d2(k, clip=True) == D2[D2_KMAX] for k in (13, 14, 16, 20, 100))
    print(f"\n[B] GATE G0 (arithmetic, no data): d2 clipped is constant above k=12 -> {g0}; "
          f"ratio d2(14)/d2(16) clipped = {d2(14, True) / d2(16, True):.6f} (exactly 1 => cannot order)")

    # ---- the 9 cells: rule-8 walk-forward ---------------------------------
    prows = []
    for sname, fams in SETS.items():
        for rule in RULES:
            for pname in P:
                for lname, spec in LADDERS.items():
                    ax, rungs, anch = spec["axis"], spec["rungs"], spec["anchor"]
                    row = L[(L.panel == pname) & (L.ladder == lname)].iloc[0]
                    bar, ok, why = correction_bar(len(rungs), row.se_mean, fams, rule)
                    decisive = bool(ok and row.is_range > bar)
                    pick = row.is_argmax if decisive else anch
                    moved = bool(pick != anch)
                    r_full = books[(pname, ax, pick)]
                    r_oos = r_full.loc[OOS_START:]
                    mf, mo = mstats(r_full), mstats(r_oos)
                    spy_f, spy_o = bench[pname]["SPY"], bench[pname]["SPY"].loc[OOS_START:]
                    liv_f = bench[pname]["LIVE"]
                    msf, mso, mlf = mstats(spy_f), mstats(spy_o), mstats(liv_f)
                    keep4a = (mf["H1"] > mlf["H1"] and mf["H2"] > mlf["H2"] and mf["MaxDD"] >= mlf["MaxDD"])
                    keep4b = (mf["H1"] > msf["H1"] and mf["H2"] > msf["H2"] and mo["Sharpe"] > mso["Sharpe"]
                              and mf["MaxDD"] >= 0.60 * msf["MaxDD"] and mf["CAGR"] >= 0.70 * msf["CAGR"])
                    prows.append(dict(correction_set=sname, domain_rule=rule, panel=pname,
                                      ladder=lname, k=len(rungs), applied=ok, decisive=decisive,
                                      bar=bar, is_range=row.is_range, pick=pick, anchor=anch,
                                      moved=moved,
                                      CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"],
                                      H1=mf["H1"], H2=mf["H2"],
                                      oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                                      spy_Sharpe=msf["Sharpe"], spy_oos_Sharpe=mso["Sharpe"],
                                      live_Sharpe=mlf["Sharpe"],
                                      KEEP_4a=keep4a, KEEP_4b=keep4b, why=why))
    W = pd.DataFrame(prows)
    W.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)

    print("\n[B] RULE-8 WALK-FORWARD: 9 cells x 3 panels x 4 ladders = "
          f"{len(W)} decisions, chosen on 2009-2016, 2017-2026 read ONCE.")
    summ = W.groupby(["correction_set", "domain_rule"]).agg(
        decisions=("pick", "size"), applied=("applied", "sum"), decisive=("decisive", "sum"),
        moved=("moved", "sum"), mean_oos_Sharpe=("oos_Sharpe", "mean"),
        mean_oos_CAGR=("oos_CAGR", "mean"), worst_oos_MaxDD=("oos_MaxDD", "min"),
        n_4a=("KEEP_4a", "sum"), n_4b=("KEEP_4b", "sum")).reset_index()
    summ.to_csv(OUT.with_suffix(".cells.csv"), index=False)
    print(summ.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- CONTROL (not a dial): the SAME gate with NO correction at all -----
    # Without this the 9 cells cannot be read: "the correction never moved a pick" is
    # only informative against the counterfactual where the correction is absent.
    crows = []
    for pname in P:
        for lname, spec in LADDERS.items():
            row = L[(L.panel == pname) & (L.ladder == lname)].iloc[0]
            k = len(spec["rungs"])
            bare = bool(row.is_range > row.se_mean)                     # no inflation
            clip = bool(row.is_range > row.se_mean * d2(k, clip=True))  # record's habit
            tabu = (np.nan if np.isnan(d2(k, clip=False))
                    else bool(row.is_range > row.se_mean * d2(k, clip=False)))
            crows.append(dict(panel=pname, ladder=lname, k=k, is_range=row.is_range,
                              se_mean=row.se_mean, ratio_bare=row.is_range / row.se_mean,
                              d2_clipped=d2(k, clip=True),
                              d2_tabulated=d2(k, clip=False),
                              decisive_NO_CORRECTION=bare,
                              decisive_D2_CLIPPED=clip,
                              decisive_D2_TABULATED=tabu,
                              correction_is_load_bearing=bool(bare != clip)))
    K = pd.DataFrame(crows)
    K.to_csv(OUT.with_suffix(".control_nocorrection.csv"), index=False)
    print("\n[B] CONTROL - THE SAME GATE WITH NO CORRECTION AT ALL (this is what makes the "
          "9 cells readable):")
    print(K.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"  the count correction is LOAD-BEARING at {int(K.correction_is_load_bearing.sum())} "
          f"of {len(K)} (panel, ladder) families; "
          f"bare gate fires at {int(K.decisive_NO_CORRECTION.sum())}, "
          f"corrected gate at {int(K.decisive_D2_CLIPPED.sum())}.")

    # do-nothing control: the anchor book at every panel
    arows = []
    for pname in P:
        for ax, anch in (("N", ANCHOR_N), ("G", ANCHOR_G)):
            r = books[(pname, ax, anch)]
            d = mstats(r); o = mstats(r.loc[OOS_START:])
            arows.append(dict(panel=pname, axis=ax, anchor=anch, CAGR=d["CAGR"], Sharpe=d["Sharpe"],
                              MaxDD=d["MaxDD"], H1=d["H1"], H2=d["H2"],
                              oos_CAGR=o["CAGR"], oos_Sharpe=o["Sharpe"], oos_MaxDD=o["MaxDD"]))
    A = pd.DataFrame(arows)
    A.to_csv(OUT.with_suffix(".anchor.csv"), index=False)
    print("\n[B] DO-NOTHING ANCHOR CONTROL (N=20 / g=0.75, weekly, 10 bps):")
    print(A.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # the out-of-domain ladders, re-read SEPARATELY (the queue's second clause)
    print("\n[B] THE OUT-OF-DOMAIN LADDERS RE-READ SEPARATELY (k=14, k=16):")
    ood = W[W.ladder.isin(["LAD_N14", "LAD_G16"])]
    ind = W[W.ladder.isin(["LAD_N6", "LAD_G8"])]
    for nm, s in (("IN-DOMAIN k<=12", ind), ("OUT-OF-DOMAIN k>12", ood)):
        print(f"  {nm:20s} decisions {len(s):3d}  applied {int(s.applied.sum()):3d}  "
              f"decisive {int(s.decisive.sum()):3d}  moved {int(s.moved.sum()):3d}  "
              f"mean OOS Sharpe {s.oos_Sharpe.mean():.4f}  4b passes {int(s.KEEP_4b.sum())}")
    return W, summ, B, A, L, K


def main():
    print(__doc__.split("Run:")[0])
    H, C, F, outcome = run_census()
    P = panels()
    W, summ, B, A, L, K = run_price_leg(P)

    # ---- the joint verdict -------------------------------------------------
    moved_any = int(W.moved.sum())
    n4b = int(W.KEEP_4b.sum())
    n4a = int(W.KEEP_4a.sum())
    stating = int(H.states_domain.sum())
    print("\n" + "=" * 100)
    print(f"CENSUS OUTCOME: {outcome} - {stating:,} of {len(H):,} correction invocations "
          f"state their own domain.")
    print(f"PRICE LEG: {moved_any} of {len(W)} decisions move off the anchor; "
          f"{n4b} clear 4b; {n4a} clear 4a.")
    print(f"CONTROL: the correction is load-bearing at "
          f"{int(K.correction_is_load_bearing.sum())} of {len(K)} (panel, ladder) families - "
          f"everywhere else the ladder fails its bar WITH OR WITHOUT any correction, so the "
          f"domain question cannot be adjudicated on price there.")
    print("=" * 100)
    for f in sorted(OUT.parent.glob(OUT.name + ".*")):
        print("wrote", f.relative_to(ROOT))


if __name__ == "__main__":
    main()
