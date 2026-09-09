#!/usr/bin/env python3
"""Idea 290 (lane B) — how many published panel shares are 7-cell binomials?

Idea 277 found the within-rung seed sd of the matched-ratio reversal share is 0.2641
against a mechanical 7-cell floor of 0.5/sqrt(7) = 0.1890, and that ETF36's published
2/7 is an ordinary draw from the k-matched STOCK band.  The queue asks:

  A. CENSUS.  Every published claim in the record that ranks or contrasts PANELS on a
     share computed from <= N_MAX cells.  Attach each share's binomial sd and test each
     ORDERING (an ordered pair of shares on the same published line, carrying two
     distinct panel labels) against its own sampling noise with a two-sided Fisher
     exact test.  Report how many orderings survive.

  B. DOES THE NOISE BAR PAY?  The census is only worth a rule if acting on it beats
     acting on the raw share.  On three real panels, build a 10-arm dial book, score
     each arm by the SHARE OF m IN-SAMPLE SUB-WINDOWS in which it beats the live
     baseline (a k/m share with m <= 10 — exactly the published statistic), and compare
     three selectors out of sample: S_NAIVE (argmax share), S_NOISE (argmax only if its
     lead clears Fisher-exact alpha, else the live constant), S_CONST (always the live
     constant).  Rule 8: everything is chosen on 2009-2016 and evaluated on 2017-2026,
     untouched.

Exactly two tuned parameters, shared by both halves: the cell cap / cell count (N_MAX
in the census, m in the live test) and the noise bar alpha.  ALL grid points reported.
Both KEEP paths are evaluated for every arm book (4a vs live RULES v2, 4b vs SPY).

Costs 10 bps per unit turnover, weekly, weights decided at close t applied at t+1
(engine).  Deterministic, no network.  SURVIVORSHIP: B136 and the sub-$2B panel are
current constituents only (research/PROTOCOL.md rule 9).

Reproduction gate (must pass before any new number): idea 277's published 0.2641 /
0.1419 / ETF36 2/7 are recomputed from its own committed panelshare.csv.
"""
from __future__ import annotations
import math, re, sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa
from engine import backtest, metrics  # noqa

STAMP = "2026-09-09_how-many-published-panel-shares-are-7-cell-binomials_B"
OUT = ROOT / "research" / "backtests"
COST, FREQ = 10, "W"

# ---- the two tuned parameters, and only these two -------------------------------
NMAX_GRID = [5, 7, 8, 10, 12, 15]          # param 1: cell cap (census) / cell count m (live)
ALPHA_GRID = [0.01, 0.05, 0.10, 0.20, 0.32, 0.50]   # param 2: noise bar
M_GRID = [3, 5, 7, 10]                     # live-test cell counts (subset of param 1's role)

_console: list[str] = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); _console.append(s)


# =================================================================== Fisher exact
def _hyper(a, b, c, d):
    """P(this exact 2x2 table | margins) under the hypergeometric null."""
    n = a + b + c + d
    return (math.comb(a + b, a) * math.comb(c + d, c)) / math.comb(n, a + c)


def fisher_two_sided(k1, n1, k2, n2):
    """Two-sided Fisher exact p for shares k1/n1 vs k2/n2 (small cells: exact, no normal
    approximation, which is the whole point of the idea)."""
    a, b, c, d = k1, n1 - k1, k2, n2 - k2
    p_obs = _hyper(a, b, c, d)
    r1, r2, c1 = a + b, c + d, a + c
    lo, hi = max(0, c1 - r2), min(r1, c1)
    tot = 0.0
    for x in range(lo, hi + 1):
        p = _hyper(x, r1 - x, c1 - x, r2 - (c1 - x))
        if p <= p_obs * (1 + 1e-9):
            tot += p
    return min(1.0, tot)


def binom_sd(k, n):
    p = k / n
    return math.sqrt(p * (1 - p) / n)


# =================================================================== reproduction gate
def gate():
    f = OUT / "2026-09-06_is-ETF36-a-third-cluster-or-just-a-small-sample_C.panelshare.csv"
    p = pd.read_csv(f)
    mix = p[p["kind"] == "MIX"]
    within = mix.groupby("etf_share")["rev"].std(ddof=1).mean()
    m = p[(p["kind"] == "MIX") | (p["panel"] == "ETF36")].copy()
    m["etf_share"] = m["etf_share"].fillna(1.0)
    between = m.groupby("etf_share")["rev"].mean().std(ddof=1)
    etf = float(p.loc[p.panel == "ETF36", "rev"].iloc[0])
    floor7 = 0.5 / math.sqrt(7)
    say("REPRODUCTION GATE (idea 277's own committed panelshare.csv)")
    say(f"  within-rung seed sd   {within:.4f}   [published 0.2641]  {'OK' if abs(within-0.2641)<5e-5 else 'FAIL'}")
    say(f"  between-rung sd       {between:.4f}   [published 0.1419]  {'OK' if abs(between-0.1419)<5e-5 else 'FAIL'}")
    say(f"  ETF36 share           {etf:.4f} = {round(etf*7)}/7   [published 2/7]  {'OK' if round(etf*7)==2 else 'FAIL'}")
    say(f"  7-cell binomial floor {floor7:.4f}   [published 0.1890]  {'OK' if abs(floor7-0.1890)<5e-5 else 'FAIL'}")
    ok = abs(within - 0.2641) < 5e-5 and abs(between - 0.1419) < 5e-5 and round(etf * 7) == 2
    assert ok, "idea 277 reproduction FAILED — stop, do not publish new numbers"
    say("  gate 4/4 PASS")
    say("")
    # the sd the queue contrasts: 0.2641 seed sd vs the 0.1890 mechanical floor
    say(f"  seed sd / mechanical floor = {within/floor7:.3f}x  (the seed sd is {within/floor7:.2f}x the "
        f"most a 7-cell binomial can be)")
    say("")
    return dict(within=within, between=between, etf=etf, floor7=floor7)


# =================================================================== A. the census
SHARE_RE = re.compile(r"(?<![\w./%-])(\d{1,3})\s*(?:/|\s+of\s+)\s*(\d{1,3})(?![\w./%])")
PANEL_TOKENS = {
    "u56": "U56", "b136": "B136", "broad136": "B136", "broad": "B136", "bstk100": "BSTK100",
    "small439": "SMALL", "small484": "SMALL", "small": "SMALL", "etf36": "ETF36",
    "etf": "ETF36", "stock": "STOCK", "u56/broad": "U56",
}
PANEL_RE = re.compile(r"\b(U56|B136|broad136|BSTK100|SMALL439|small439|ETF36|broad|small|stock)\b", re.I)
DATEISH = re.compile(r"\b20\d\d-\d\d-\d\d\b")


def _sources():
    s = sorted((ROOT / "research" / "backtests").glob("*.result.md"))
    s += sorted((ROOT / "research" / "backtests").glob("*.console.txt"))
    s += [ROOT / "research" / "CHANGELOG.md", ROOT / "research" / "LEADERBOARD.md",
          ROOT / "research" / "QUEUE.md"]
    return [p for p in s if p.exists() and STAMP not in p.name]


SENT_SPLIT = re.compile(r"(?<=[.;:!?])\s+(?=[A-Z(*`\d])")


def segments(line):
    """A published CLAIM is a sentence, not a physical line: CHANGELOG entries are one
    multi-kilobyte line, so pairing every share on the line would invent contrasts that
    were never made.  Short lines (console tables) stay whole."""
    if len(line) <= 200:
        return [line]
    out = []
    for s in SENT_SPLIT.split(line):
        while len(s) > 400:
            out.append(s[:400]); s = s[400:]
        out.append(s)
    return out


def _shares_on(line, nmax):
    out = []
    for m in SHARE_RE.finditer(line):
        k, n = int(m.group(1)), int(m.group(2))
        if n == 0 or k > n or n > nmax:
            continue
        out.append((k, n, m.start()))
    return out


def census(nmax):
    """Every k/n with n <= nmax in the published prose record, plus the subset that sits on
    a line naming >= 2 distinct panels (a PANEL ORDERING claim)."""
    all_rows, ord_rows = [], []
    for p in _sources():
        try:
            txt = p.read_text(errors="ignore")
        except Exception:
            continue
        rel = str(p.relative_to(ROOT))
        for ln_no, raw in enumerate(txt.splitlines(), 1):
            if DATEISH.search(raw):
                raw = DATEISH.sub(" ", raw)
            for line in segments(raw):
                sh = _shares_on(line, nmax)
                if not sh:
                    continue
                panels = sorted({PANEL_TOKENS.get(t.group(1).lower(), t.group(1).upper())
                                 for t in PANEL_RE.finditer(line)})
                for k, n, _ in sh:
                    all_rows.append(dict(file=rel, line=ln_no, k=k, n=n, share=k / n,
                                         sd=binom_sd(k, n), floor=0.5 / math.sqrt(n),
                                         n_panels=len(panels)))
                if len(panels) >= 2 and len(sh) >= 2:
                    for i in range(len(sh)):
                        for j in range(i + 1, len(sh)):
                            k1, n1, _ = sh[i]; k2, n2, _ = sh[j]
                            if k1 / n1 == k2 / n2:
                                continue                   # not an ordering claim
                            pv = fisher_two_sided(k1, n1, k2, n2)
                            hi, lo = (((k1, n1), (k2, n2)) if k1 / n1 > k2 / n2
                                      else ((k2, n2), (k1, n1)))
                            ord_rows.append(dict(
                                file=rel, line=ln_no, panels="|".join(panels),
                                k_hi=hi[0], n_hi=hi[1], k_lo=lo[0], n_lo=lo[1],
                                share_hi=hi[0] / hi[1], share_lo=lo[0] / lo[1],
                                gap=hi[0] / hi[1] - lo[0] / lo[1],
                                sd_hi=binom_sd(*hi), sd_lo=binom_sd(*lo), fisher_p=pv,
                                text=line.strip()[:200]))
    A = pd.DataFrame(all_rows)
    O = pd.DataFrame(ord_rows)
    if len(O):
        O["claim_id"] = (O.k_hi.astype(str) + "/" + O.n_hi.astype(str) + " vs "
                         + O.k_lo.astype(str) + "/" + O.n_lo.astype(str) + " :: "
                         + O.panels + " :: " + O.text)
    return A, O


def min_detectable(n, alpha):
    """Smallest share gap between two n-cell shares that a two-sided Fisher exact can
    call at alpha.  inf when no split of n vs n is callable at all."""
    best = math.inf
    for k1 in range(n + 1):
        for k2 in range(k1 + 1, n + 1):
            if fisher_two_sided(k2, n, k1, n) < alpha:
                best = min(best, (k2 - k1) / n)
    return best


# =================================================================== B. the live test
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"]) if "max_1d_move" in meta else set()
    keep = [c for c in px.columns if c not in bad]
    return px[keep]


def panels():
    return {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL": small_panel()}


BANDS = [0.00, 0.02, 0.03, 0.05, 0.08, 0.12]
NRANK = [3, 5, 8, 12]
DEFAULT_ARM = "band0.03"                                   # the live RULES v2 constant


def arm_fns():
    d = {}
    for b in BANDS:
        d[f"band{b:.2f}"] = (lambda px, b=b: rules_v2_weights(px, band=b))
    for n in NRANK:
        d[f"rank{n}"] = (lambda px, n=n: rules_v1_weights(px, n=n, w=0.75 / n))
    return d


def dd_max(r):
    e = (1 + r).cumprod()
    return float((e / e.cummax() - 1).min())


def met(r):
    if len(r) < 60 or r.std() == 0:
        return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    m = metrics(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"])


IS_END = pd.Timestamp("2016-12-31")


def run_panel(name, px):
    fns = arm_fns()
    rets = {}
    for a, f in fns.items():
        rets[a] = backtest(px, f(px), cost_bps=COST, freq=FREQ)["returns"]
    start = px.index[260]
    rets = {a: r.loc[start:] for a, r in rets.items()}
    base = rets[DEFAULT_ARM]                                # live RULES v2 on this panel
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    return rets, base, spy


def keep_paths(r, base, spy, live=None):
    """PROTOCOL rule 4 on the full common sample.  4a vs live RULES v2 (Sharpe in BOTH
    halves and MaxDD no worse), 4b vs SPY (Sharpe both halves AND OOS, |MaxDD| <= 60% of
    SPY's, CAGR >= 70% of SPY's)."""
    h = len(r) // 2
    R, B, S = met(r), met(base), met(spy)
    r1, r2 = met(r.iloc[:h]), met(r.iloc[h:])
    b1, b2 = met(base.iloc[:h]), met(base.iloc[h:])
    s1, s2 = met(spy.iloc[:h]), met(spy.iloc[h:])
    oos = slice(IS_END + pd.Timedelta(days=1), None)
    ro, so = met(r.loc[oos]), met(spy.loc[oos])
    p4a = (r1["Sharpe"] > b1["Sharpe"] and r2["Sharpe"] > b2["Sharpe"]
           and abs(R["MaxDD"]) <= abs(B["MaxDD"]))
    p4b = (r1["Sharpe"] > s1["Sharpe"] and r2["Sharpe"] > s2["Sharpe"]
           and ro["Sharpe"] > so["Sharpe"] and abs(R["MaxDD"]) <= 0.60 * abs(S["MaxDD"])
           and R["CAGR"] >= 0.70 * S["CAGR"])
    # PROTOCOL rule 4a names the LIVE book, which is RULES v2 on U56 — not a per-panel
    # restatement of it.  Report both, and let the live-book column be the binding one.
    p4a_live = np.nan
    if live is not None:
        lv = live.reindex(r.index).fillna(0.0)
        l1, l2, L = met(lv.iloc[:h]), met(lv.iloc[h:]), met(lv)
        p4a_live = (r1["Sharpe"] > l1["Sharpe"] and r2["Sharpe"] > l2["Sharpe"]
                    and abs(R["MaxDD"]) <= abs(L["MaxDD"]))
    return dict(CAGR=R["CAGR"], Sharpe=R["Sharpe"], MaxDD=R["MaxDD"], H1=r1["Sharpe"],
                H2=r2["Sharpe"], OOS_CAGR=ro["CAGR"], OOS_Sharpe=ro["Sharpe"],
                OOS_MaxDD=ro["MaxDD"], pass4a=p4a, pass4a_live=p4a_live, pass4b=p4b)


def cell_shares(rets, base, m):
    """Share of m equal-length IN-SAMPLE sub-windows in which each arm's Sharpe beats the
    baseline's.  A k/m share with m <= 10 — the published statistic under audit."""
    idx = base.loc[:IS_END].index
    edges = np.linspace(0, len(idx), m + 1).astype(int)
    out = {}
    for a, r in rets.items():
        k = 0
        for i in range(m):
            sl = idx[edges[i]:edges[i + 1]]
            ra, rb = r.loc[sl], base.loc[sl]
            sa = ra.mean() / ra.std() if ra.std() else 0.0
            sb = rb.mean() / rb.std() if rb.std() else 0.0
            k += int(sa > sb)
        out[a] = k
    return out


def select(shares, m, alpha):
    """S_NAIVE = argmax share (deterministic tie-break by arm name).  S_NOISE = S_NAIVE
    only if its Fisher-exact lead over the runner-up clears alpha, else the live constant."""
    order = sorted(shares.items(), key=lambda kv: (-kv[1], kv[0]))
    top, ktop = order[0]
    run, krun = order[1]
    pv = fisher_two_sided(ktop, m, krun, m)
    return top, (top if pv < alpha else DEFAULT_ARM), pv, ktop, krun


# =================================================================== main
def main():
    anchors = gate()

    # ---------------------------------------------------------------- A
    say("=" * 78)
    say("A. CENSUS — published panel orderings on shares of <= N_MAX cells")
    say("=" * 78)
    all_big, ord_big = census(max(NMAX_GRID))
    say(f"sources scanned: {len(_sources())} files "
        f"({len(all_big):,} share tokens at n <= {max(NMAX_GRID)})")
    say("")
    ord_uni = ord_big.drop_duplicates("claim_id")
    say(f"panel orderings: {len(ord_big):,} occurrences, {len(ord_uni):,} DISTINCT claims "
        f"(the record restates the same claim in console.txt, result.md and CHANGELOG.md); "
        f"every count below is on DISTINCT claims.")
    say("")
    grid = []
    for nmax in NMAX_GRID:
        A = all_big[all_big.n <= nmax]
        O = ord_uni[(ord_uni.n_hi <= nmax) & (ord_uni.n_lo <= nmax)]
        for alpha in ALPHA_GRID:
            surv = int((O.fisher_p < alpha).sum())
            grid.append(dict(nmax=nmax, alpha=alpha, shares=len(A), orderings=len(O),
                             survive=surv, survive_share=surv / len(O) if len(O) else np.nan,
                             excess_over_null=(surv / len(O) - alpha) if len(O) else np.nan,
                             median_sd=float(A.sd.median()) if len(A) else np.nan,
                             median_gap=float(O.gap.median()) if len(O) else np.nan,
                             median_p=float(O.fisher_p.median()) if len(O) else np.nan))
    G = pd.DataFrame(grid)
    say(G.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("  (excess_over_null = survive_share - alpha: how far the record's orderings sit above "
        "what pure noise would deliver at that bar)")
    say("")
    n7 = all_big[all_big.n == 7]
    say(f"exactly-7-cell shares in the record: {len(n7):,}  "
        f"(median sd {n7.sd.median():.4f}, mechanical floor {0.5/math.sqrt(7):.4f})")
    say(f"share of all n <= 10 tokens that are 7-cell: "
        f"{len(n7)/max(1,len(all_big[all_big.n<=10])):.1%}")
    say("")
    say("minimum DETECTABLE share gap between two n-cell shares (two-sided Fisher):")
    md = pd.DataFrame([{**{"n": n}, **{f"a={a}": min_detectable(n, a) for a in ALPHA_GRID}}
                       for n in NMAX_GRID]).set_index("n")
    say(md.to_string(float_format=lambda x: "----" if not np.isfinite(x) else f"{x:.3f}"))
    say("")
    O10 = ord_uni[(ord_uni.n_hi <= 10) & (ord_uni.n_lo <= 10)]
    if len(O10):
        say(f"HEADLINE at the queue's own cap (n <= 10) and the conventional bar (alpha 0.05): "
            f"{int((O10.fisher_p<0.05).sum())} of {len(O10)} DISTINCT published panel orderings "
            f"survive their own sampling noise ({(O10.fisher_p<0.05).mean():.1%}); "
            f"{int((O10.fisher_p>=0.05).sum())} ({(O10.fisher_p>=0.05).mean():.1%}) do not. "
            f"Median Fisher p {O10.fisher_p.median():.3f}, median published gap {O10.gap.median():.3f}.")
        say(f"  a claim needs a gap of at least {min_detectable(7,0.05):.3f} to be callable at all "
            f"on 7 cells, and {min_detectable(10,0.05):.3f} on 10; the record's median 7-cell "
            f"gap is {O10[(O10.n_hi==7)&(O10.n_lo==7)].gap.median() if len(O10[(O10.n_hi==7)&(O10.n_lo==7)]) else float('nan'):.3f}")
        say("")
        say("the 10 widest published gaps that STILL fail at alpha 0.05:")
        f = O10[O10.fisher_p >= 0.05].nlargest(10, "gap")
        for _, r in f.iterrows():
            say(f"  {r.k_hi}/{r.n_hi} vs {r.k_lo}/{r.n_lo}  gap {r.gap:+.3f}  p {r.fisher_p:.3f}  "
                f"[{r.panels}]  {Path(r.file).name}:{r.line}")
            say(f"      \"{r.text[:150]}\"")
        say("")
        say("distribution of the cell count n over distinct orderings (n <= 10):")
        say(pd.concat([O10.n_hi, O10.n_lo]).value_counts().sort_index().to_string())
    say("")
    all_big.to_csv(OUT / f"{STAMP}.shares.csv.gz", index=False, compression="gzip")
    ord_uni.to_csv(OUT / f"{STAMP}.orderings.csv", index=False)
    G.to_csv(OUT / f"{STAMP}.census_grid.csv", index=False)

    # ---------------------------------------------------------------- B
    say("=" * 78)
    say("B. DOES THE NOISE BAR PAY?  (rule 8: chosen on 2009-2016, judged on 2017-2026)")
    say("=" * 78)
    arms_rows, sel_rows = [], []
    P = panels()
    live_u56 = run_panel("U56", P["U56"])[1]           # the actual live book: RULES v2 on U56
    for pname, px in P.items():
        rets, base, spy = run_panel(pname, px)
        say(f"\n--- {pname}: {px.shape[1]} cols, {rets[DEFAULT_ARM].index[0].date()} -> "
            f"{rets[DEFAULT_ARM].index[-1].date()}")
        for a, r in rets.items():
            row = dict(panel=pname, arm=a, **keep_paths(r, base, spy, live=live_u56))
            arms_rows.append(row)
        A = pd.DataFrame([r for r in arms_rows if r["panel"] == pname]).set_index("arm")
        b = A.loc[DEFAULT_ARM]
        S = met(spy); Soos = met(spy.loc[IS_END + pd.Timedelta(days=1):])
        say(A[["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
               "pass4a", "pass4a_live", "pass4b"]].to_string(float_format=lambda x: f"{x:.3f}"))
        say(f"  SPY full {S['CAGR']:.3f}/{S['Sharpe']:.3f}/{S['MaxDD']:.3f}   "
            f"SPY OOS {Soos['CAGR']:.3f}/{Soos['Sharpe']:.3f}/{Soos['MaxDD']:.3f}")

        for m in M_GRID:
            sh = cell_shares(rets, base, m)
            for alpha in ALPHA_GRID:
                naive, noise, pv, ktop, krun = select(sh, m, alpha)
                oos = slice(IS_END + pd.Timedelta(days=1), None)
                mn, mz, mc = met(rets[naive].loc[oos]), met(rets[noise].loc[oos]), met(base.loc[oos])
                sel_rows.append(dict(
                    panel=pname, m=m, alpha=alpha, k_top=ktop, k_run=krun, fisher_p=pv,
                    S_NAIVE=naive, S_NOISE=noise, fired=int(noise != DEFAULT_ARM),
                    naive_OOS_CAGR=mn["CAGR"], naive_OOS_Sharpe=mn["Sharpe"], naive_OOS_MaxDD=mn["MaxDD"],
                    noise_OOS_CAGR=mz["CAGR"], noise_OOS_Sharpe=mz["Sharpe"], noise_OOS_MaxDD=mz["MaxDD"],
                    const_OOS_CAGR=mc["CAGR"], const_OOS_Sharpe=mc["Sharpe"], const_OOS_MaxDD=mc["MaxDD"],
                    spy_OOS_CAGR=Soos["CAGR"], spy_OOS_Sharpe=Soos["Sharpe"], spy_OOS_MaxDD=Soos["MaxDD"]))
        SS = pd.DataFrame([r for r in sel_rows if r["panel"] == pname])
        say("  IS cell shares k/m by arm:")
        for m in M_GRID:
            sh = cell_shares(rets, base, m)
            say(f"    m={m:<3} " + "  ".join(f"{a}:{k}/{m}" for a, k in sh.items()))

    ARMS = pd.DataFrame(arms_rows)
    SEL = pd.DataFrame(sel_rows)
    ARMS.to_csv(OUT / f"{STAMP}.arms.csv", index=False)
    SEL.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)

    say("")
    say("KEEP paths over all arm books (PROTOCOL rule 4, full sample; 4b's OOS leg = rule 8):")
    say(f"  4a (per-panel restatement of RULES v2): {int(ARMS.pass4a.sum())} / {len(ARMS)}")
    say(f"  4a (the ACTUAL live book, RULES v2 on U56 — the binding comparand): "
        f"{int(ARMS.pass4a_live.sum())} / {len(ARMS)}")
    say(f"  4b (vs SPY, incl. the rule-8 OOS Sharpe leg): {int(ARMS.pass4b.sum())} / {len(ARMS)}"
        f"     both paths: {int((ARMS.pass4a_live & ARMS.pass4b).sum())} / {len(ARMS)}")
    for _, r in ARMS[ARMS.pass4a | ARMS.pass4a_live | ARMS.pass4b].iterrows():
        say(f"    {r.panel:<6} {r.arm:<10} 4a={r.pass4a} 4a_live={r.pass4a_live} 4b={r.pass4b}  "
            f"{r.CAGR:.3f}/{r.Sharpe:.3f}/{r.MaxDD:.3f}  halves {r.H1:.3f}/{r.H2:.3f}  "
            f"OOS {r.OOS_CAGR:.3f}/{r.OOS_Sharpe:.3f}/{r.OOS_MaxDD:.3f}")
    say("")
    say("SELECTOR GRID (all 3 x 4 x 6 = 72 points; OOS = 2017-01-01 onward, untouched):")
    say(SEL[["panel", "m", "alpha", "k_top", "k_run", "fisher_p", "S_NAIVE", "S_NOISE", "fired",
             "naive_OOS_Sharpe", "noise_OOS_Sharpe", "const_OOS_Sharpe", "spy_OOS_Sharpe",
             "naive_OOS_CAGR", "noise_OOS_CAGR", "const_OOS_CAGR"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("")
    for lab, col in [("Sharpe", "OOS_Sharpe"), ("CAGR", "OOS_CAGR"), ("MaxDD", "OOS_MaxDD")]:
        say(f"mean OOS {lab}:  NAIVE {SEL['naive_'+col].mean():+.4f}   "
            f"NOISE {SEL['noise_'+col].mean():+.4f}   CONST {SEL['const_'+col].mean():+.4f}   "
            f"SPY {SEL['spy_'+col].mean():+.4f}")
    d_nc = SEL.naive_OOS_Sharpe - SEL.const_OOS_Sharpe
    d_zc = SEL.noise_OOS_Sharpe - SEL.const_OOS_Sharpe
    d_zn = SEL.noise_OOS_Sharpe - SEL.naive_OOS_Sharpe
    for lab, d in [("NAIVE - CONST", d_nc), ("NOISE - CONST", d_zc), ("NOISE - NAIVE", d_zn)]:
        t = d.mean() / (d.std(ddof=1) / math.sqrt(len(d))) if d.std(ddof=1) else np.nan
        say(f"OOS Sharpe {lab}: mean {d.mean():+.4f}  sd {d.std(ddof=1):.4f}  t {t:+.2f}  "
            f"wins {int((d>0).sum())}/{len(d)}")
    say("  CAVEAT ON THOSE t's: the 72 cells are 3 PANELS x 4 m x 6 alpha and the m/alpha "
        "cells are near-duplicates, so the effective sample is 3, not 72.  Per panel:")
    for p in SEL.panel.unique():
        s = SEL[SEL.panel == p]
        say(f"    {p:<6} NAIVE-CONST {(s.naive_OOS_Sharpe-s.const_OOS_Sharpe).mean():+.4f}   "
            f"NOISE-CONST {(s.noise_OOS_Sharpe-s.const_OOS_Sharpe).mean():+.4f}   "
            f"NAIVE picks {sorted(set(s.S_NAIVE))}   fired {int(s.fired.sum())}/{len(s)}")
    say("")
    say(f"the bar FIRED (picked something other than the live constant) in "
        f"{int(SEL.fired.sum())} of {len(SEL)} cells; NAIVE differed from the constant in "
        f"{int((SEL.S_NAIVE != DEFAULT_ARM).sum())} of {len(SEL)}")
    say("")
    A = ARMS.set_index(["panel", "arm"])
    for lab, col in [("S_NAIVE", "S_NAIVE"), ("S_NOISE", "S_NOISE")]:
        sub = A.loc[list(zip(SEL.panel, SEL[col]))]
        say(f"KEEP paths for the {lab} books (72 selector cells, resolved to arm books): "
            f"4a(per-panel) {int(sub.pass4a.sum())}/{len(sub)}   "
            f"4a(live book) {int(sub.pass4a_live.sum())}/{len(sub)}   "
            f"4b {int(sub.pass4b.sum())}/{len(sub)}   "
            f"both {int((sub.pass4a_live & sub.pass4b).sum())}/{len(sub)}")

    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_console) + "\n")
    say(f"\nwrote {STAMP}.{{console.txt,shares.csv.gz,orderings.csv,census_grid.csv,arms.csv,walkforward.csv}}")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_console) + "\n")


if __name__ == "__main__":
    main()
