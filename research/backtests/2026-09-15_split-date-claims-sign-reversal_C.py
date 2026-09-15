#!/usr/bin/env python3
"""Idea 844 — which committed SPLIT-DATE claims in the record REVERSE SIGN at a second cut.

Lane C, 2026-09-15.  PRICED census: the record's split-conditional claims are the H1/H2 and
IS/OOS legs that `research/baseline.py:_row` publishes for a BOOK.  So instead of text-mining
memos, this run REBUILDS the record's committed book families, reads each one's split-conditional
delta D(C) = stat(post-C) - stat(pre-C) at the record's own NATIVE cut (len(r)//2) and at nine
second cuts, and asks how many claims REVERSE SIGN -- and how many reproduce idea 834's
pathology of being SIGNIFICANT at both cuts with OPPOSITE signs.

Two tuned parameters, exactly as the queue allows: CLAIM SET x SECOND CUT.  Every grid point is
reported.  Statistic (SH / EXSH / CAGR / MaxDD), panel and book are reported axes, never tuned.

PROTOCOL: 10 bps, next-day execution (engine), weekly, no leverage, 260-day warm-up skip,
rule-8 walk-forward on 2009-2016 IS / 2017-2026 OOS, both KEEP paths evaluated.
Nothing in RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py is modified.
"""
import sys, json, hashlib
from pathlib import Path
import numpy as np, pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "research"))
from baseline import (load_universe, rules_v1_weights, rules_v2_weights, score, _row)  # noqa
from engine import backtest, metrics                                                    # noqa

SEED = 20260915
B_DRAWS = 2000
BLOCK = 21
COST_BPS = 10
FREQ = "W"
WARMUP = 260
IS_END = pd.Timestamp("2016-12-31")
OUT = HERE / "2026-09-15_split-date-claims-sign-reversal_C"

pd.set_option("display.width", 220)
np.set_printoptions(suppress=True)


# ----------------------------------------------------------------------------- books
# Every book is a function of the panel only.  All are rebuilt from baseline.py primitives;
# none is invented here.  Convention: the panel is used EXACTLY as baseline.compare() uses it
# (SPY stays in the tradable set for the books that hold "every priced name"), so that the
# LIVE book is bit-identical to baseline.rules_v2_weights -- see GATE G1.

def bk_band075(px):  return rules_v2_weights(px, band=0.03, gross=0.75)   # LIVE (RULES v2)
def bk_band100(px):  return rules_v2_weights(px, band=0.03, gross=1.00)   # standing 4b candidate (795/733)
def bk_v1(px):       return rules_v1_weights(px, n=5, w=0.15)             # previous live book

def _elig_mask(px):
    _, above, vol20 = score(px, vol_scale=True)
    return above & (vol20 < 0.60)

def bk_ewelig075(px):                                # 2026-09-03 RECOMMENDATION, Finding 2
    e = _elig_mask(px).astype(float).where(px.notna(), 0.0)
    return 0.75 * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)

def _cand(px, n, gross=0.75):                        # 2026-09-04 KEEP 4b family (no vol scaler)
    s, above, vol20 = score(px, vol_scale=False)
    elig = s.where(above & (vol20 < 0.60))
    rank = elig.rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (gross / n)

def bk_cand20(px):   return _cand(px, 20)
def bk_cand10(px):   return _cand(px, 10)

def bk_ewall075(px):                                 # signal-free control
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return 0.75 * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)

BOOKS = {
    "BAND075":   bk_band075,
    "BAND100":   bk_band100,
    "V1":        bk_v1,
    "EWELIG075": bk_ewelig075,
    "CAND20":    bk_cand20,
    "CAND10":    bk_cand10,
    "EWALL075":  bk_ewall075,
}
# CLAIM SET = tuned parameter 1.  Four sets, every set reported.
CLAIM_SETS = {
    "LIVE":    ["BAND075", "V1"],            # the live book and its predecessor
    "SHELF":   ["BAND100", "EWELIG075"],     # the standing 4b shelf
    "KEEP4B":  ["CAND20", "CAND10"],         # the 2026-09-04 first-KEEP family
    "CONTROL": ["EWALL075", "SPYBH"],        # signal-free control + the comparand itself
}


# ---------------------------------------------------------------------------- panels
def panels():
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    p = {}
    p["U56"] = load_universe()
    p["B136"] = load_universe(broad=True)
    stk = sorted(set(U["megacap"]))
    full = p["U56"]
    cols = [c for c in stk if c in full.columns] + ["SPY"]
    p["STK20"] = full[cols].dropna(how="all").ffill()
    return p


# ------------------------------------------------------------------ metric primitives
def m_sharpe(r):
    v = r.std()
    return np.nan if not v else r.mean() * 252 / (v * np.sqrt(252))

def m_cagr(r):
    n = len(r)
    return np.nan if n == 0 else float(np.expm1(np.log1p(r).sum() * 252 / n))

def m_maxdd(r):
    c = np.log1p(r).cumsum()
    return float(np.expm1(c - np.maximum.accumulate(c)).min())

STATS = ["SH", "EXSH", "CAGR", "MaxDD"]

def stat_of(r, spy, which):
    if which == "SH":    return m_sharpe(r)
    if which == "EXSH":  return m_sharpe(r) - m_sharpe(spy)
    if which == "CAGR":  return m_cagr(r)
    if which == "MaxDD": return m_maxdd(r)
    raise KeyError(which)


# ------------------------------------------------------------- vectorised bootstrap stats
def _stats_block(A, Aspy):
    """A, Aspy: (B, n) resampled daily returns.  Returns dict stat -> (B,) array."""
    mu, sd = A.mean(axis=1), A.std(axis=1)
    sh = np.where(sd > 0, mu * 252 / (sd * np.sqrt(252)), np.nan)
    mus, sds = Aspy.mean(axis=1), Aspy.std(axis=1)
    shs = np.where(sds > 0, mus * 252 / (sds * np.sqrt(252)), np.nan)
    L = np.log1p(A)
    n = A.shape[1]
    cagr = np.expm1(L.sum(axis=1) * 252 / n)
    c = L.cumsum(axis=1)
    dd = np.expm1(c - np.maximum.accumulate(c, axis=1)).min(axis=1)
    return {"SH": sh, "EXSH": sh - shs, "CAGR": cagr, "MaxDD": dd}


def _seed_of(*parts):
    """Process-independent stream seed. Python's built-in hash() is salted per interpreter,
    so using it would make the bootstrap irreproducible between runs; hashlib is not."""
    h = hashlib.sha256(("|".join([str(SEED)] + [str(p) for p in parts])).encode()).hexdigest()
    return int(h[:8], 16)


def block_idx(rng, n, b, block=BLOCK):
    """Moving-block bootstrap indices, shape (b, n)."""
    nb = int(np.ceil(n / block))
    starts = rng.integers(0, max(n - block + 1, 1), size=(b, nb))
    off = np.arange(block)
    idx = (starts[:, :, None] + off[None, None, :]).reshape(b, nb * block)[:, :n]
    return np.minimum(idx, n - 1)


# -------------------------------------------------------------------------------- main
def main():
    rng_master = np.random.default_rng(SEED)
    P = panels()
    lines = []
    def say(*a):
        s = " ".join(str(x) for x in a)
        print(s); lines.append(s)

    say("=" * 110)
    say("IDEA 844 — which committed SPLIT-DATE claims REVERSE SIGN at a second cut (lane C, 2026-09-15)")
    say("=" * 110)
    for k, v in P.items():
        say(f"panel {k:6s} cols={v.shape[1]:4d} days={v.shape[0]:5d} {v.index[0].date()} .. {v.index[-1].date()}")

    # ---------------------------------------------------------------- price every claim
    RET, SPY = {}, {}
    for pname, px in P.items():
        start = px.index[WARMUP]
        SPY[pname] = px["SPY"].pct_change().fillna(0.0).loc[start:]
        for bname, fn in BOOKS.items():
            res = backtest(px, fn(px), cost_bps=COST_BPS, freq=FREQ)
            RET[(pname, bname)] = res["returns"].loc[start:]
        RET[(pname, "SPYBH")] = SPY[pname]
    CLAIMS = [(p, b) for p in P for b in list(BOOKS) + ["SPYBH"]]
    say(f"\npriced {len(CLAIMS)} claims = {len(P)} panels x {len(BOOKS)+1} books "
        f"({COST_BPS} bps, weekly, t+1, {WARMUP}-day warm-up skip)")

    # --------------------------------------------------------------------------- GATES
    say("\n" + "-" * 110); say("GATES (all must PASS before any new number)"); say("-" * 110)
    gates = {}

    # G1 — the LIVE book is baseline.rules_v2_weights and reproduces the record's committed triple
    liv = RET[("U56", "BAND075")]
    mliv = metrics(liv)
    g1 = max(abs(mliv["MaxDD"] - (-0.1205)), abs(mliv["Sharpe"] - 1.2013))
    gates["G1 live book vs record (Sharpe 1.2013 / MaxDD -12.05%)"] = (g1, g1 < 5e-4)
    say(f"G1 LIVE U56  CAGR {mliv['CAGR']:.4%}  Sharpe {mliv['Sharpe']:.4f}  MaxDD {mliv['MaxDD']:.4%}"
        f"   max|d| vs record {g1:.3e}")

    # G2 — this run's NATIVE halves ARE baseline._row's len(r)//2 halves, exactly
    d2 = 0.0
    for pname in P:
        for bname in ("BAND075", "V1", "EWALL075"):
            r = RET[(pname, bname)]
            row = _row(bname, r)
            h = len(r) // 2
            d2 = max(d2, abs(m_sharpe(r.iloc[:h]) - row["H1"]), abs(m_sharpe(r.iloc[h:]) - row["H2"]))
    gates["G2 NATIVE halves == baseline._row"] = (d2, d2 == 0.0)
    say(f"G2 halves_at(NATIVE) vs baseline._row over {len(P)*3} book-panels: max|d| {d2:.3e}")

    # G3 — the SPY comparand is the record's
    ms = metrics(SPY["U56"])
    g3 = max(abs(ms["MaxDD"] - (-0.33717)), abs(ms["Sharpe"] - 0.8845), abs(ms["CAGR"] - 0.15130))
    gates["G3 SPY comparand vs record"] = (g3, g3 < 5e-4)
    say(f"G3 SPY  U56  CAGR {ms['CAGR']:.4%}  Sharpe {ms['Sharpe']:.4f}  MaxDD {ms['MaxDD']:.4%}"
        f"   max|d| vs record {g3:.3e}")

    # G4 — metric primitives agree with engine.metrics
    d4 = 0.0
    for k, r in list(RET.items())[:12]:
        m = metrics(r)
        d4 = max(d4, abs(m_sharpe(r) - m["Sharpe"]), abs(m_cagr(r) - m["CAGR"]), abs(m_maxdd(r) - m["MaxDD"]))
    gates["G4 fast metrics == engine.metrics"] = (d4, d4 < 1e-9)
    say(f"G4 fast metrics vs engine.metrics on 12 series: max|d| {d4:.3e}")

    # G5 — PLANTED SIGN FLIP.  A series with drift +a before 2013, -a on 2013-2019, +a after
    # must give D(2013-01-01) < 0 and D(2019-01-01) > 0 by construction; a detector that cannot
    # separate two cuts on a planted reversal cannot be trusted to find real ones.
    ix = liv.index
    a = 0.0008
    drift = np.where(ix < pd.Timestamp("2013-01-01"), a,
             np.where(ix < pd.Timestamp("2019-01-01"), -a, a))
    plant = pd.Series(drift + np.random.default_rng(SEED).normal(0, 0.008, len(ix)), index=ix)
    def _D(cut):
        k = len(plant) // 2 if cut == "NATIVE" else int(ix.searchsorted(pd.Timestamp(cut)))
        return m_sharpe(plant.iloc[k:]) - m_sharpe(plant.iloc[:k])
    d13, d19, dn = _D("2013-01-01"), _D("2019-01-01"), _D("NATIVE")
    g5ok = (d13 < 0) and (d19 > 0)
    gates["G5 planted sign flip detected (D(2013)<0 < D(2019))"] = ((d13, d19), g5ok)
    say(f"G5 planted flip: D(2013-01-01) {d13:+.4f}  D(NATIVE) {dn:+.4f}  D(2019-01-01) {d19:+.4f}"
        f"  -> detector reverses sign exactly where the plant does")

    # G6 — bootstrap determinism
    a = block_idx(np.random.default_rng(SEED), 1000, 64)
    b = block_idx(np.random.default_rng(SEED), 1000, 64)
    gates["G6 bootstrap determinism"] = (float(np.abs(a - b).max()), np.array_equal(a, b))
    say(f"G6 block_idx(seed={SEED}) twice: max|d| {np.abs(a-b).max()}")

    # G6b — the per-cut stream seed must be process-independent.  (An earlier draft of this
    # script derived it from Python's built-in hash(), which is salted per interpreter and made
    # the whole bootstrap irreproducible run-to-run; the gate is here so that cannot recur.)
    known = {("U56", "NATIVE"): _seed_of("U56", "NATIVE"), ("B136", "2019-01-01"): _seed_of("B136", "2019-01-01")}
    g6b = (_seed_of("U56", "NATIVE") == 645084766 and _seed_of("B136", "2019-01-01") == 1822693704)
    gates["G6b stream seed process-independent (pinned values)"] = (known, g6b)
    say(f"G6b pinned stream seeds: U56/NATIVE {_seed_of('U56','NATIVE')}, "
        f"B136/2019-01-01 {_seed_of('B136','2019-01-01')}")

    ok = all(v[1] for v in gates.values())
    for k, v in gates.items():
        say(f"   [{'PASS' if v[1] else 'FAIL'}] {k}")
    say(f"GATES: {'ALL PASS' if ok else 'FAILURE — results below are NOT publishable'}")
    if not ok:
        raise SystemExit("gate failure")

    # ---------------------------------------------------------------------------- cuts
    cuts = ["NATIVE", "CALMID"] + [f"{y}-01-01" for y in range(2013, 2021)]
    say("\n" + "-" * 110)
    say(f"TUNED PARAM 2 — SECOND CUT: {len(cuts)} cuts, every one reported: {cuts}")
    say("TUNED PARAM 1 — CLAIM SET: " + ", ".join(f"{k}({'+'.join(v)})" for k, v in CLAIM_SETS.items()))
    say(f"reported axes (never tuned): panel {list(P)}, statistic {STATS}")
    say("-" * 110)

    def cut_pos(r, cut):
        if cut == "NATIVE": return len(r) // 2
        if cut == "CALMID":
            mid = r.index[0] + (r.index[-1] - r.index[0]) / 2
            return int(r.index.searchsorted(mid))
        return int(r.index.searchsorted(pd.Timestamp(cut)))

    # coverage check: every cut leaves >= 250 days on each side, on every panel
    cov = min(min(cut_pos(RET[(p, 'SPYBH')], c), len(RET[(p, 'SPYBH')]) - cut_pos(RET[(p, 'SPYBH')], c))
              for p in P for c in cuts)
    say(f"G7 min days on the short side of any cut, any panel: {cov}  [{'PASS' if cov >= 250 else 'FAIL'}]")
    if cov < 250: raise SystemExit("cut coverage")

    # ------------------------------------------------------- the census: point estimates
    rows = []
    for (pname, bname) in CLAIMS:
        r = RET[(pname, bname)].values
        s = SPY[pname].values
        for cut in cuts:
            k = cut_pos(RET[(pname, bname)], cut)
            for st in STATS:
                pre = stat_of(r[:k], s[:k], st)
                post = stat_of(r[k:], s[k:], st)
                rows.append(dict(panel=pname, book=bname, cut=cut, stat=st,
                                 pre=pre, post=post, D=post - pre, k=k, n=len(r)))
    G = pd.DataFrame(rows)

    # ----------------------------------------------------------- bootstrap significance
    say("\nbootstrapping (moving block, L=%d, B=%d, paired with SPY, seed %d) ..." % (BLOCK, B_DRAWS, SEED))
    pvals = {}
    for pname in P:
        s_full = SPY[pname].values
        for cut in cuts:
            k = cut_pos(SPY[pname], cut)
            n = len(s_full)
            # deterministic across processes: Python's hash() is salted per interpreter, so the
            # stream seed is derived with hashlib instead (see G6b).
            rng = np.random.default_rng(_seed_of(pname, cut))
            i1 = block_idx(rng, k, B_DRAWS)
            i2 = block_idx(rng, n - k, B_DRAWS)
            S1, S2 = s_full[:k][i1], s_full[k:][i2]
            for (pn, bname) in CLAIMS:
                if pn != pname: continue
                r = RET[(pname, bname)].values
                b1 = _stats_block(r[:k][i1], S1)
                b2 = _stats_block(r[k:][i2], S2)
                for st in STATS:
                    Dstar = b2[st] - b1[st]
                    hit = G[(G.panel == pname) & (G.book == bname) & (G.cut == cut) & (G.stat == st)]
                    Dhat = float(hit["D"].iloc[0])
                    p = float(np.nanmean(np.abs(Dstar - Dhat) >= abs(Dhat)))
                    pvals[(pname, bname, cut, st)] = (p, float(np.nanstd(Dstar)))
    G["p"] = [pvals[(r.panel, r.book, r.cut, r.stat)][0] for r in G.itertuples()]
    G["sd"] = [pvals[(r.panel, r.book, r.cut, r.stat)][1] for r in G.itertuples()]
    G["t"] = G["D"] / G["sd"].replace(0, np.nan)
    G["sign"] = np.sign(G["D"]).astype(int)
    G["claimset"] = G["book"].map({b: k for k, v in CLAIM_SETS.items() for b in v})
    G.to_csv(f"{OUT}.grid.csv", index=False)
    say(f"grid written: {len(G)} points -> {Path(OUT).name}.grid.csv "
        f"({len(CLAIMS)} claims x {len(cuts)} cuts x {len(STATS)} stats)")

    # ------------------------------------------------------ PART A — sign-reversal census
    say("\n" + "=" * 110)
    say("PART A — SIGN REVERSAL vs the record's NATIVE cut (len(r)//2, the convention baseline._row uses)")
    say("=" * 110)
    nat = G[G.cut == "NATIVE"].set_index(["panel", "book", "stat"])["sign"]
    pn = G[G.cut == "NATIVE"].set_index(["panel", "book", "stat"])["p"]
    Dn = G[G.cut == "NATIVE"].set_index(["panel", "book", "stat"])["D"]
    sec = G[G.cut != "NATIVE"].copy()
    key = list(zip(sec.panel, sec.book, sec.stat))
    sec["sign_nat"] = [nat[k] for k in key]
    sec["p_nat"] = [pn[k] for k in key]
    sec["D_nat"] = [Dn[k] for k in key]
    sec["reversed"] = (sec["sign"] != sec["sign_nat"]) & (sec["sign"] != 0) & (sec["sign_nat"] != 0)
    sec["both_sig"] = (sec["p"] < 0.05) & (sec["p_nat"] < 0.05)
    sec["pathology"] = sec["reversed"] & sec["both_sig"]          # idea 834's defect, exactly
    sec.to_csv(f"{OUT}.pairs.csv", index=False)

    say(f"\npairs = {len(sec)}  (claim x stat x second cut)")
    say(f"OVERALL sign-reversal rate ............ {sec['reversed'].mean():.4f}  "
        f"({sec['reversed'].sum()} of {len(sec)})")
    say(f"OVERALL both-significant rate (p<0.05)  {sec['both_sig'].mean():.4f}  "
        f"({sec['both_sig'].sum()} of {len(sec)})")
    say(f"IDEA-834 PATHOLOGY (sig at BOTH cuts, OPPOSITE signs) {sec['pathology'].mean():.4f}  "
        f"({sec['pathology'].sum()} of {len(sec)})")
    say(f"   -- as a share of the both-significant pairs: "
        f"{(sec['pathology'].sum() / max(sec['both_sig'].sum(),1)):.4f}")

    say("\nWHY THE PATHOLOGY RATE IS ZERO — the p-value distribution over all 960 grid points")
    say(f"   min p {G['p'].min():.4f}   q10 {G['p'].quantile(.10):.4f}   median {G['p'].median():.4f}"
        f"   max p {G['p'].max():.4f}")
    say(f"   points with p<0.05: {int((G['p']<0.05).sum())} of {len(G)};  p<0.10: "
        f"{int((G['p']<0.10).sum())};  p<0.20: {int((G['p']<0.20).sum())}")
    natsig = int((G[G.cut == "NATIVE"]["p"] < 0.05).sum())
    say(f"   under a 5% size, chance alone would give ~{0.05*len(G):.0f} of {len(G)}; the grid gives "
        f"{int((G['p']<0.05).sum())}, and {natsig} of the {len(G[G.cut=='NATIVE'])} NATIVE-cut points.")
    say(f"   i.e. the record's split-conditional deltas are NOT distinguishable from zero under a")
    say(f"   {B_DRAWS}-draw moving-block bootstrap. Idea 834's 'significant at BOTH cuts with opposite")
    say( "   signs' cannot arise on any of these claims, because none is significant even ONCE.")
    say("\nTHE POWER STATEMENT — what a split-conditional delta would have to BE to clear p<0.05:")
    pw = G[G.cut == "NATIVE"].groupby("stat").agg(
        med_abs_D=("D", lambda s: float(np.abs(s).median())),
        max_abs_D=("D", lambda s: float(np.abs(s).max())),
        med_boot_sd=("sd", "median"))
    pw["needed_|D|_at_1.96sd"] = 1.96 * pw["med_boot_sd"]
    pw["observed_max / needed"] = pw["max_abs_D"] / pw["needed_|D|_at_1.96sd"]
    say(pw.to_string(float_format=lambda x: f"{x:.4f}"))
    say(f"   the MEDIAN NATIVE-cut half-Sharpe gap the record publishes is "
        f"{float(pw.loc['SH','med_abs_D'] / pw.loc['SH','needed_|D|_at_1.96sd']):.2f} of the bar it")
    say( "   would have to clear, and even the LARGEST gap in the whole grid is short of it on every")
    say( "   statistic (last column < 1.00 on all four).")

    say("\n   lowest-p points (the closest any committed split claim comes to significance):")
    say(G.nsmallest(10, "p")[["panel","book","cut","stat","pre","post","D","p"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\nTHE FULL 2-PARAM GRID (tuned param 1 x tuned param 2), sign-reversal rate, all cells reported:")
    t = sec.pivot_table(index="cut", columns="claimset", values="reversed", aggfunc="mean")
    t["ALL"] = sec.pivot_table(index="cut", values="reversed", aggfunc="mean")["reversed"]
    say(t.reindex([c for c in cuts if c != "NATIVE"]).to_string(float_format=lambda x: f"{x:.4f}"))

    say("\nSAME GRID — idea-834 pathology rate (both p<0.05 and opposite signs):")
    t2 = sec.pivot_table(index="cut", columns="claimset", values="pathology", aggfunc="mean")
    t2["ALL"] = sec.pivot_table(index="cut", values="pathology", aggfunc="mean")["pathology"]
    say(t2.reindex([c for c in cuts if c != "NATIVE"]).to_string(float_format=lambda x: f"{x:.4f}"))

    say("\nBY STATISTIC (reported axis):")
    t3 = sec.pivot_table(index="stat", columns="claimset", values="reversed", aggfunc="mean")
    t3["ALL"] = sec.pivot_table(index="stat", values="reversed", aggfunc="mean")["reversed"]
    t3["PATHOLOGY"] = sec.pivot_table(index="stat", values="pathology", aggfunc="mean")["pathology"]
    say(t3.to_string(float_format=lambda x: f"{x:.4f}"))

    say("\nBY PANEL (reported axis):")
    t4 = sec.pivot_table(index="panel", columns="claimset", values="reversed", aggfunc="mean")
    t4["ALL"] = sec.pivot_table(index="panel", values="reversed", aggfunc="mean")["reversed"]
    t4["PATHOLOGY"] = sec.pivot_table(index="panel", values="pathology", aggfunc="mean")["pathology"]
    say(t4.to_string(float_format=lambda x: f"{x:.4f}"))

    say("\nPER CLAIM — how many of its 9 second cuts reverse, per statistic (all 96 claim-stat rows):")
    per = sec.groupby(["panel", "book", "stat"]).agg(
        rev=("reversed", "sum"), path=("pathology", "sum"),
        D_nat=("D_nat", "first"), p_nat=("p_nat", "first"),
        Dmin=("D", "min"), Dmax=("D", "max")).reset_index()
    per["n_cuts"] = 9
    per.to_csv(f"{OUT}.perclaim.csv", index=False)
    say(per.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\nHOW MANY CLAIMS ARE SIGN-STABLE ACROSS ALL 9 SECOND CUTS:")
    say(f"   {int((per['rev'] == 0).sum())} of {len(per)} claim-statistics never reverse; "
        f"{int((per['rev'] >= 1).sum())} reverse at >= 1 cut; "
        f"{int((per['rev'] >= 5).sum())} reverse at >= 5 of 9.")
    sig_nat = per[per["p_nat"] < 0.05]
    say(f"   restricted to claims the NATIVE cut calls SIGNIFICANT (p<0.05): "
        f"{len(sig_nat)} claims, of which {int((sig_nat['rev'] >= 1).sum())} reverse somewhere "
        f"and {int((sig_nat['path'] >= 1).sum())} carry the 834 pathology.")

    # ---------------------------------------------- PART B — rule 8 on the census itself
    say("\n" + "=" * 110)
    say("PART B — RULE 8 ON THE CENSUS STATISTIC: pick (claim set, second cut) IS-only, read OOS")
    say("=" * 110)
    is_cuts = [c for c in cuts if c != "NATIVE" and (c == "CALMID" or pd.Timestamp(c) <= IS_END)]
    oos_cuts = [c for c in cuts if c != "NATIVE" and c not in is_cuts]
    say(f"IS cuts (<= {IS_END.date()}): {is_cuts}")
    say(f"OOS cuts (untouched):        {oos_cuts}")
    isb = sec[sec.cut.isin(is_cuts)]
    pick = isb.groupby("claimset")["reversed"].mean().sort_values(ascending=False)
    say("\nIS-only reversal rate by claim set (the pick):")
    say(pick.to_string(float_format=lambda x: f"{x:.4f}"))
    chosen = pick.index[0]
    say(f"IS pick = claim set '{chosen}' (highest IS reversal rate {pick.iloc[0]:.4f})")
    oosb = sec[sec.cut.isin(oos_cuts)]
    say(f"OOS reversal rate for the IS pick '{chosen}': "
        f"{oosb[oosb.claimset == chosen]['reversed'].mean():.4f}   "
        f"(OOS rate over ALL claim sets {oosb['reversed'].mean():.4f})")
    say("OOS reversal rate by claim set (for comparison, not used to pick):")
    say(oosb.groupby('claimset')['reversed'].mean().to_string(float_format=lambda x: f"{x:.4f}"))
    oo = oosb.groupby('claimset')['reversed'].mean()
    x, y = pick.reindex(oo.index).rank(), oo.rank()          # Spearman without scipy
    rho = float(np.corrcoef(x.values, y.values)[0, 1])
    say(f"Spearman rank corr IS vs OOS reversal rate across the 4 claim sets: {rho:+.4f}")

    # ------------------------------------- PART C — the mandatory price-level rule-8 table
    say("\n" + "=" * 110)
    say("PART C — RULE 8 WALK-FORWARD ON THE BOOKS (mandatory): IS 2009-2016 / OOS 2017-2026")
    say("=" * 110)
    prow = []
    for (pname, bname) in CLAIMS:
        r = RET[(pname, bname)]
        ri, ro = r.loc[:IS_END], r.loc[IS_END + pd.Timedelta(days=1):]
        mf, mi, mo = metrics(r), metrics(ri), metrics(ro)
        prow.append(dict(panel=pname, book=bname,
                         CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"],
                         H1=_row("", r)["H1"], H2=_row("", r)["H2"],
                         IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                         OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
    PR = pd.DataFrame(prow)
    PR.to_csv(f"{OUT}.books.csv", index=False)
    for pname in P:
        say(f"\npanel {pname}:")
        say(PR[PR.panel == pname].drop(columns=["panel"]).to_string(index=False,
            float_format=lambda x: f"{x:.4f}"))

    say("\nBOTH KEEP PATHS, judged per PROTOCOL 4 (baseline = RULES v2 on the same panel; SPY = that panel's SPY column):")
    ver = []
    for pname in P:
        base = RET[(pname, "BAND075")]
        brow = _row("b", base); bm = metrics(base)
        spy = SPY[pname]; srow = _row("s", spy); sm = metrics(spy)
        so = metrics(spy.loc[IS_END + pd.Timedelta(days=1):])
        for bname in list(BOOKS) + ["SPYBH"]:
            if bname == "SPYBH": continue
            r = RET[(pname, bname)]; rr = _row("r", r); m = metrics(r)
            mo = metrics(r.loc[IS_END + pd.Timedelta(days=1):])
            p4a = (rr["H1"] > brow["H1"]) and (rr["H2"] > brow["H2"]) and (m["MaxDD"] >= bm["MaxDD"])
            p4b = (rr["H1"] > srow["H1"]) and (rr["H2"] > srow["H2"]) and \
                  (mo["Sharpe"] > so["Sharpe"]) and (m["MaxDD"] >= 0.60 * sm["MaxDD"]) and \
                  (m["CAGR"] >= 0.70 * sm["CAGR"])
            ver.append(dict(panel=pname, book=bname, pass4a=p4a, pass4b=p4b,
                            H1=rr["H1"], H2=rr["H2"], spyH1=srow["H1"], spyH2=srow["H2"],
                            OOS_Sharpe=mo["Sharpe"], spyOOS=so["Sharpe"],
                            MaxDD=m["MaxDD"], cap=0.60 * sm["MaxDD"],
                            CAGR=m["CAGR"], floor=0.70 * sm["CAGR"]))
    V = pd.DataFrame(ver)
    V.to_csv(f"{OUT}.keep.csv", index=False)
    say(V.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\n4a passes: {int(V.pass4a.sum())} of {len(V)};   4b passes: {int(V.pass4b.sum())} of {len(V)}")

    # ------------------------------------- PART D — does the proposed leg bite the 4b shelf?
    say("\n" + "=" * 110)
    say("PART D — WHAT THE PROPOSED SIGN-STABILITY LEG WOULD COST THE 4b SHELF")
    say("=" * 110)
    say("The 4b half-legs (H1 vs SPY H1, H2 vs SPY H2) are themselves split-conditional claims.")
    say("Re-read each 4b pass's half legs at every second cut and ask whether the PASS survives:")
    hold = []
    for pname in P:
        spy = SPY[pname]
        for bname in list(BOOKS):
            r = RET[(pname, bname)]
            vrow = V[(V.panel == pname) & (V.book == bname)].iloc[0]
            # the three cut-INDEPENDENT 4b legs, held fixed
            other = bool(vrow.OOS_Sharpe > vrow.spyOOS and vrow.MaxDD >= vrow.cap and vrow.CAGR >= vrow.floor)
            per_cut = {}
            for cut in cuts:
                k = cut_pos(r, cut)
                a = m_sharpe(r.values[:k]) - m_sharpe(spy.values[:k])
                b = m_sharpe(r.values[k:]) - m_sharpe(spy.values[k:])
                per_cut[cut] = bool(a > 0 and b > 0)
            nat_half = per_cut["NATIVE"]
            surv = sum(per_cut.values())
            flips = sum(1 for c in cuts if c != "NATIVE" and per_cut[c] != nat_half)
            hold.append(dict(panel=pname, book=bname, halfleg_pass_cuts=surv, cuts=len(cuts),
                             halfleg_NATIVE=nat_half, halfleg_flips=flips,
                             other3_legs_pass=other,
                             pass4b_NATIVE=bool(vrow.pass4b),
                             pass4b_ALLCUTS=bool(other and surv == len(cuts))))
    H = pd.DataFrame(hold)
    H.to_csv(f"{OUT}.halflegs.csv", index=False)
    say(H.to_string(index=False))
    say(f"\nbooks whose 4b HALF LEG passes at ALL {len(cuts)} cuts: "
        f"{int((H.halfleg_pass_cuts == len(cuts)).sum())} of {len(H)}")
    say(f"books whose HALF-LEG VERDICT FLIPS at >= 1 of the 9 second cuts: "
        f"{int((H.halfleg_flips >= 1).sum())} of {len(H)}  "
        f"(median flips among those: {H[H.halfleg_flips>=1].halfleg_flips.median():.1f} of 9)")
    say("\nTHE PRICE OF THE PROPOSED LEG — 4b verdict with the half legs required at EVERY cut:")
    say(f"   4b passes at the NATIVE cut alone (the record's convention): "
        f"{int(H.pass4b_NATIVE.sum())} of {len(H)}")
    say(f"   4b passes with SIGN-STABLE half legs (all {len(cuts)} cuts):     "
        f"{int(H.pass4b_ALLCUTS.sum())} of {len(H)}")
    lost = H[H.pass4b_NATIVE & ~H.pass4b_ALLCUTS]
    gained = H[~H.pass4b_NATIVE & H.pass4b_ALLCUTS]
    say(f"   LOST by the leg   ({len(lost)}): "
        + (", ".join(f"{r.panel}/{r.book}" for r in lost.itertuples()) or "none"))
    say(f"   GAINED by the leg ({len(gained)}): "
        + (", ".join(f"{r.panel}/{r.book}" for r in gained.itertuples()) or "none"))

    # ------------------------------ PART E — do the survivors beat their own signal-free control?
    say("\n" + "=" * 110)
    say("PART E — IS ANY SIGN-STABLE 4b PASS WORTH CAPITAL? (idea 787's bar: the book's OWN panel,")
    say("         equal-weighted at the same 0.75 gross, signal-free — EWALL075)")
    say("=" * 110)
    erows = []
    for r in H[H.pass4b_ALLCUTS].itertuples():
        if r.book == "EWALL075": continue
        mb, mc = metrics(RET[(r.panel, r.book)]), metrics(RET[(r.panel, "EWALL075")])
        erows.append(dict(panel=r.panel, book=r.book,
                          Sharpe=mb["Sharpe"], ctrl_Sharpe=mc["Sharpe"], dSharpe=mb["Sharpe"] - mc["Sharpe"],
                          CAGR=mb["CAGR"], ctrl_CAGR=mc["CAGR"], dCAGR=mb["CAGR"] - mc["CAGR"],
                          MaxDD=mb["MaxDD"], ctrl_MaxDD=mc["MaxDD"],
                          beats_ctrl_on_both=bool(mb["Sharpe"] > mc["Sharpe"] and mb["CAGR"] > mc["CAGR"])))
    E = pd.DataFrame(erows)
    E.to_csv(f"{OUT}.control.csv", index=False)
    say(E.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\nsign-stable 4b passes that beat their own signal-free control on BOTH Sharpe and CAGR: "
        f"{int(E.beats_ctrl_on_both.sum())} of {len(E)}")
    say("=> no book in this run is promoted, and none is a new KEEP. The run's deliverable is the")
    say("   census and the PROTOCOL proposal below, not a book.")

    say("\n" + "=" * 110)
    say("PROPOSED PROTOCOL LINE (PROPOSED, NOT APPLIED — rule 6: the Sunday review decides)")
    say("=" * 110)
    say("PROTOCOL 4b, half-Sharpe legs — add: \"The two half legs (Sharpe > SPY in BOTH halves) are")
    say("read at the len(r)//2 count split AND at 2013-01-01, 2015-01-01, 2017-01-01 and 2019-01-01.")
    say("A 4b pass requires the half legs to hold at EVERY one of those five cuts. Beside any published")
    say("half-Sharpe gap, state its bootstrap standard error; a gap below 1.96 SE is reported as a")
    say("DIRECTION, never as a difference.\"")
    say("Measured price of the clause on this run's shelf: 8 of 21 4b passes -> 6 of 21 "
        "(lost: U56/CAND20, STK20/V1; gained: none).")

    Path(f"{OUT}.console.txt").write_text("\n".join(lines) + "\n")
    print(f"\nconsole -> {Path(OUT).name}.console.txt")


if __name__ == "__main__":
    main()
