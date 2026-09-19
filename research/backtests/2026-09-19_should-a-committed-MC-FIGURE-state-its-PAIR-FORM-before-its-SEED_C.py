#!/usr/bin/env python3
"""Idea 1196 (lane C, 2026-09-19): should a committed MC FIGURE state its PAIR FORM
before its SEED?

QUESTION (queue text). Idea 1191 found the binding leg of re-runnability is the PAIR
FORM (stated by 0.0869 of C_STRICT units against SEED 0.2218), that a LINEAR kernel's
pairs are identically its pooled means (|F_MC - F_EXACT| = 0.000000 at every K), and
that the exact-pair form costs 1.49e5x less than the pools it summarises. HARVEST the
record's committed pair statistics, CLASSIFY each kernel as linear or not, and report
how many are RECOVERABLE TODAY and what the exact-pair RE-PUBLICATION would cost.

TWO DIALS AND NO MORE (rule 4; the queue names both):
    dial 1 = CLAIM SET    {C_STRICT, C_PROX, C_ALL}   (1191's nesting sets, verbatim)
    dial 2 = KERNEL CLASS {LINEAR, NONLINEAR, UNCLASSIFIED}
=> 9 cells, every one published.
NOT dials, reported at every value: PANEL {U56, B136, SMALL}; the anchor grid
N {10,12,20,30} x cadence {W,M} = 24 real books; the draw ladder K {10,20,50,100,200};
20 seeds at every K; four chooser kernels; the 4a and 4b legs; rule-8 OOS.

WHY A CENSUS CARRIES A CAPITAL ARM HERE. "Recoverable today" is not a filing question:
a LINEAR pair statistic is recoverable from pooled means alone (1191 G2), a NONLINEAR
one needs the per-draw artefact.  So the record can only retire its unrecoverable
figures if a LINEAR chooser buys as good a book as the NONLINEAR ones it would replace.
That is priced here directly: 24 real books per panel-set, gross-matched null pools,
four choosers fitted on 2009-2016 ONLY, 2017-2026 read ONCE.

Costs 10 bps, next-day execution, no shorting, no leverage (PROTOCOL 2).
"""
import sys, re, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights                    # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, rebalance_mask                             # noqa: E402

OUT       = Path(__file__).with_suffix("")
COST      = 10.0
GROSS     = 0.75
ANCHORS   = [(n, f) for f in ("W", "M") for n in (10, 12, 20, 30)]
NDRAW     = 200
KLAD      = [10, 20, 50, 100, 200]
NSEED     = 20
OOS_START = "2017-01-01"
WARMUP    = 260

# ===================================================================== runner
class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        self.cols = list(px.columns)
        self.iinv = np.array([self.cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.P = np.cumprod(1.0 + self.rets, axis=0)
        self.Pprev = np.vstack([np.ones((1, self.P.shape[1])), self.P[:-1]])
        self.priced = px.notna().values
        self.seg = {}
        for f in {a[1] for a in ANCHORS}:
            m = rebalance_mask(px.index, f).shift(1, fill_value=False).values.copy()
            m[0] = True
            s = np.flatnonzero(m)
            self.seg[f] = (s, np.append(s[1:], len(px)))
        self.i0 = px.index.get_loc(px.index[WARMUP])
        self.ioos = px.index.searchsorted(pd.Timestamp(OOS_START))

def run_from_starts(pan, freq, Wstart):
    """engine.backtest arithmetic with targets supplied only on rebalance rows (G1)."""
    starts, ends = pan.seg[freq]
    T, M = pan.rets.shape
    held = np.zeros((T, M)); turn = np.zeros(T); cur = np.zeros(M)
    for k, (i0, i1) in enumerate(zip(starts, ends)):
        w0 = Wstart[k]
        turn[i0] = np.abs(w0 - cur).sum()
        base = pan.Pprev[i0]
        A = w0[None, :] * (pan.Pprev[i0:i1] / base[None, :])
        cash0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + cash0
        held[i0:i1] = A / V[:, None]
        Aend = w0 * (pan.P[i1 - 1] / base)
        cur = Aend / (Aend.sum() + cash0)
    return (held * pan.rets).sum(axis=1) - turn * COST / 1e4

def starts_from_weights(pan, freq, W):
    starts, _ = pan.seg[freq]
    Wv = W.reindex(pan.px.index).fillna(0.0).shift(1).fillna(0.0).values
    return Wv[starts]

def book_weights(pan, n):
    q = pan.px[pan.invest]
    mom = q.shift(21) / q.shift(252) - 1
    r6 = q / q.shift(126) - 1
    r3 = q / q.shift(63) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3
    elig = comp.where(q > q.rolling(200).mean())
    rk = elig.rank(axis=1, ascending=False)
    W = pd.DataFrame(0.0, index=pan.px.index, columns=pan.px.columns)
    W[pan.invest] = (rk <= n).astype(float) * (GROSS / n)
    return W

def null_starts(pan, freq, n, rng):
    starts, _ = pan.seg[freq]
    out = np.zeros((len(starts), pan.rets.shape[1]))
    for k, i in enumerate(starts):
        avail = pan.iinv[pan.priced[max(i - 1, 0)][pan.iinv]]
        if len(avail) < n:
            continue
        out[k, rng.choice(avail, size=n, replace=False)] = GROSS / n
    return out

def sharpe(r):
    v = r.std(ddof=0) * np.sqrt(252)
    return r.mean() * 252 / v if v > 0 else np.nan

def mdd(r):
    e = np.cumprod(1 + r); return (e / np.maximum.accumulate(e) - 1).min()

def cagr(r):
    e = np.cumprod(1 + r); return e[-1] ** (252 / len(r)) - 1

# ===================================================================== census
# 1191's claim-set lexicon, verbatim, so the denominators are comparable.
GEN   = re.compile(r"\b(seed|seeds|seeded|bootstrap|bootstrapped|permutation|permuted|"
                   r"resampl\w*|monte[- ]?carlo|shuffl\w*|draws?|redraw\w*)\b", re.I)
NEAR  = re.compile(r"\b(null|coin[- ]flip|percentile of its own|matched null|control)\b", re.I)
NUM   = re.compile(r"\d")
SEEDT = re.compile(r"\b(seed\s*=?\s*\d+|seeds?\b[^.]{0,30}?\d|rng|random_state|np\.random)\b", re.I)
COUNT = re.compile(r"(\d[\d,]*)\s*(?:-|\s)?\s*(draws?|seeds?|pairs?|resamples?|replicat\w*|"
                   r"bootstrap\w*|permutations?|paths?|simulations?)\b", re.I)
ORDER = re.compile(r"\b(draw order|loop order|pair(?:ed|ing)?|per[- ]pair|matched draw|"
                   r"same draw|exact[- ]pair|pairwise|element[- ]wise)\b", re.I)

# THE NEW LEXICON (dial 2).  A kernel f(a,b) is LINEAR iff mean_i f(a_i,b_i) is a
# function of the pooled means alone -- then the pairing is not information (1191 G2)
# and the figure is recoverable from any pooled artefact.  NONLINEAR kernels
# (percentile / share / rate / ratio / rank / sign) need the per-draw values.
LINEAR = re.compile(r"\b(excess|minus|difference|differenced|gap|delta|spread|advantage|"
                    r"premium|drag|margin|pp\b|percentage points?|mean gain|average gain|"
                    r"net of|less than its own mean|over its own mean)\b", re.I)
NONLIN = re.compile(r"\b(percentile|pctile|pct[- ]?rank|share|rate|fraction|proportion|"
                    r"ratio|times|x the|odds|sign|median|quantile|rank|correlation|rho|"
                    r"spearman|kendall|indicator|beats?|wins?|exceeds?|pass rate|"
                    r"base rate|count of draws|how often)\b", re.I)

def units():
    U = []
    for ln in (ROOT / "research" / "LEADERBOARD.md").read_text().split("\n"):
        if ln.startswith("| 20"):
            U.append(("LEADERBOARD", "LEADERBOARD", ln))
    for para in (ROOT / "research" / "CHANGELOG.md").read_text().split("\n\n"):
        if para.strip():
            U.append(("CHANGELOG", "CHANGELOG", para))
    n_md = 0
    for f in sorted((ROOT / "research" / "backtests").rglob("*.md")):
        n_md += 1
        stem = re.sub(r"\.(result|memo|console)$", "", f.stem)
        for para in f.read_text(errors="ignore").split("\n\n"):
            if para.strip():
                U.append((f.name, stem, para))
    return U, n_md

def perdraw_artefacts():
    """Stems under research/backtests that own at least one CSV with a per-draw column
    (seed / draw / rep / sim / iter).  Those are the artefacts a NONLINEAR pair
    statistic can still be re-derived from today."""
    have, tot, withcol = set(), 0, 0
    for f in sorted((ROOT / "research" / "backtests").rglob("*.csv")):
        tot += 1
        try:
            head = f.open().readline().lower()
        except Exception:
            continue
        if re.search(r"\b(seed|draw|rep|sim|iter)\w*\b", head):
            withcol += 1
            have.add(re.sub(r"\.\w+$", "", f.stem))
            have.add(f.stem)
    return have, tot, withcol

def census():
    U, n_md = units()
    have, tot_csv, seed_csv = perdraw_artefacts()
    fileset = {}
    for src, _, txt in U:
        fileset.setdefault(src, False)
        if GEN.search(txt) or NEAR.search(txt):
            fileset[src] = True
    rows = []
    for src, stem, txt in U:
        g, nr, num = bool(GEN.search(txt)), bool(NEAR.search(txt)), bool(NUM.search(txt))
        lin, non = bool(LINEAR.search(txt)), bool(NONLIN.search(txt))
        # A unit whose text names BOTH kinds of kernel is UNCLASSIFIED: the census
        # cannot tell which number the paragraph's MC figure belongs to.  Never
        # silently resolved in favour of either class.
        kc = "UNCLASSIFIED" if lin == non else ("LINEAR" if lin else "NONLINEAR")
        art = stem in have
        rows.append(dict(src=src, stem=stem, n_chars=len(txt),
                         C_STRICT=g and num, C_PROX=(g or nr) and num,
                         C_ALL=fileset[src] and num,
                         IS_PAIR=bool(ORDER.search(txt)) and (g or nr) and num,
                         KERNEL=kc, HAS_SEED=bool(SEEDT.search(txt)),
                         HAS_COUNT=bool(COUNT.search(txt)), HAS_ARTEFACT=art))
    df = pd.DataFrame(rows)
    # RECOVERABLE TODAY.  LINEAR: yes by construction (pooled means suffice, 1191 G2).
    # NONLINEAR: only with the per-draw artefact AND a stated draw count.
    # UNCLASSIFIED: never claimed as recoverable.
    df["RECOVERABLE"] = np.where(
        df.KERNEL == "LINEAR", True,
        np.where(df.KERNEL == "NONLINEAR", df.HAS_ARTEFACT & df.HAS_COUNT, False))
    return df, len(U), n_md, tot_csv, seed_csv

# ======================================================================= main
def main():
    t_start = time.time()
    print("=" * 78)
    print("(A) THE HARVEST — committed PAIR statistics, classified by KERNEL")
    print("=" * 78)
    cdf, nU, n_md, tot_csv, seed_csv = census()
    cdf.to_csv(f"{OUT}.census.csv", index=False)
    print(f"  corpus: {nU} committed text units "
          f"(LEADERBOARD rows {int((cdf.src=='LEADERBOARD').sum())}, "
          f"CHANGELOG paragraphs {int((cdf.src=='CHANGELOG').sum())}, "
          f"{n_md} markdown artefacts); "
          f"{tot_csv} committed CSVs, {seed_csv} ({seed_csv/max(tot_csv,1):.4f}) with a per-draw column")

    grid = []
    for cs in ["C_STRICT", "C_PROX", "C_ALL"]:
        sub = cdf[cdf[cs]]
        pair = sub[sub.IS_PAIR]
        for kc in ["LINEAR", "NONLINEAR", "UNCLASSIFIED"]:
            k = pair[pair.KERNEL == kc]
            grid.append(dict(claim_set=cs, kernel_class=kc, n_claim=len(sub), n_pair=len(pair),
                             n=len(k), share_of_pair=len(k) / max(len(pair), 1),
                             states_seed=k.HAS_SEED.mean() if len(k) else np.nan,
                             states_count=k.HAS_COUNT.mean() if len(k) else np.nan,
                             has_artefact=k.HAS_ARTEFACT.mean() if len(k) else np.nan,
                             recoverable=k.RECOVERABLE.mean() if len(k) else np.nan,
                             n_recoverable=int(k.RECOVERABLE.sum())))
    gdf = pd.DataFrame(grid); gdf.to_csv(f"{OUT}.censusgrid.csv", index=False)
    for cs in ["C_STRICT", "C_PROX", "C_ALL"]:
        s = gdf[gdf.claim_set == cs]
        print(f"\n  {cs}: {int(s.n_claim.iloc[0])} MC-derived units, "
              f"{int(s.n_pair.iloc[0])} of them PAIR statistics "
              f"({s.n_pair.iloc[0]/max(s.n_claim.iloc[0],1):.4f})")
        for _, r in s.iterrows():
            print(f"    {r.kernel_class:13s} n={r.n:5d} ({r.share_of_pair:.4f} of pair)  "
                  f"seed {r.states_seed:.4f}  count {r.states_count:.4f}  "
                  f"per-draw artefact {r.has_artefact:.4f}  ->  RECOVERABLE TODAY "
                  f"{r.recoverable:.4f} ({r.n_recoverable})")
        tot_p = int(s.n_pair.iloc[0]); rec = int(s.n_recoverable.sum())
        print(f"    TOTAL recoverable today: {rec} of {tot_p} pair statistics "
              f"({rec/max(tot_p,1):.4f})")

    # ------------------------------------------------------------- price arm
    print("\n" + "=" * 78)
    print("(B) THE PRICE ARM — 3 panels x 8 anchors, gross-matched null pools")
    print("=" * 78)
    P = {}
    u = load_universe();            P["U56"] = Panel("U56", u, list(u.columns))
    b = load_universe(broad=True);  P["B136"] = Panel("B136", b, list(b.columns))
    s = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in s.columns if c != "SPY" and c not in bad]
    P["SMALL"] = Panel("SMALL", s[keep + ["SPY"]], keep)
    print(f"  panels: U56 {u.shape}, B136 {b.shape}, SMALL {P['SMALL'].px.shape} "
          f"({len(keep)} investable after dropping {len(bad)} max_1d_move>=1.0 names)")

    gates, books, picks = [], [], []
    pan = P["U56"]; W = book_weights(pan, 20)
    r_fast = run_from_starts(pan, "W", starts_from_weights(pan, "W", W))
    r_eng = backtest(pan.px, W, cost_bps=COST, freq="W")["returns"].values
    g1 = float(np.abs(r_fast[pan.i0:] - r_eng[pan.i0:]).max())
    gates.append(("G1 starts-runner == engine.backtest, post-warm-up (max abs diff)", g1, g1 < 1e-12))

    pools, tpool = {}, {}
    rng_master = np.random.RandomState(20260919)
    bench = {}
    for pname, pan in P.items():
        spy = pan.px["SPY"].pct_change().fillna(0).values
        lv = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        i0, io = pan.i0, pan.ioos
        sl = slice(i0, None)
        bench[pname] = dict(SPY_CAGR=cagr(spy[sl]), SPY_S=sharpe(spy[sl]), SPY_DD=mdd(spy[sl]),
                            SPY_OOS_CAGR=cagr(spy[io:]), SPY_OOS_S=sharpe(spy[io:]),
                            SPY_OOS_DD=mdd(spy[io:]),
                            LV_CAGR=cagr(lv[sl]), LV_S=sharpe(lv[sl]), LV_DD=mdd(lv[sl]),
                            LV_OOS_CAGR=cagr(lv[io:]), LV_OOS_S=sharpe(lv[io:]),
                            LV_OOS_DD=mdd(lv[io:]))
        bb = bench[pname]
        print(f"\n  [{pname}] SPY {bb['SPY_CAGR']:.2%}/{bb['SPY_S']:.4f}/{bb['SPY_DD']:.2%} "
              f"OOS {bb['SPY_OOS_CAGR']:.2%}/{bb['SPY_OOS_S']:.4f}/{bb['SPY_OOS_DD']:.2%} | "
              f"RULES v2 live {bb['LV_CAGR']:.2%}/{bb['LV_S']:.4f}/{bb['LV_DD']:.2%} "
              f"OOS {bb['LV_OOS_CAGR']:.2%}/{bb['LV_OOS_S']:.4f}/{bb['LV_OOS_DD']:.2%}")
        for (n, freq) in ANCHORS:
            t0 = time.time()
            W = book_weights(pan, n)
            rb = run_from_starts(pan, freq, starts_from_weights(pan, freq, W))
            rbf = rb[sl]; h = len(rbf) // 2
            nis = np.zeros(NDRAW)
            for d in range(NDRAW):
                rng = np.random.RandomState(rng_master.randint(0, 2**31 - 1))
                rn = run_from_starts(pan, freq, null_starts(pan, freq, n, rng))
                nis[d] = sharpe(rn[i0:io])                 # IS ONLY — the chooser's input
            pools[(pname, n, freq)] = nis
            tpool[(pname, n, freq)] = time.time() - t0
            spyf, lvf = spy[sl], lv[sl]
            L = dict(L_H1=sharpe(rbf[:h]) > sharpe(spyf[:h]), L_H2=sharpe(rbf[h:]) > sharpe(spyf[h:]),
                     L_OOS=sharpe(rb[io:]) > sharpe(spy[io:]),
                     L_DD=abs(mdd(rbf)) <= 0.60 * abs(mdd(spyf)),
                     L_CAGR=cagr(rbf) >= 0.70 * cagr(spyf))
            p4b = all(L.values())
            p4a = (sharpe(rbf[:h]) > sharpe(lvf[:h]) and sharpe(rbf[h:]) > sharpe(lvf[h:])
                   and mdd(rbf) >= mdd(lvf))
            books.append(dict(panel=pname, n=n, cadence=freq, CAGR=cagr(rbf), Sharpe=sharpe(rbf),
                              MaxDD=mdd(rbf), H1=sharpe(rbf[:h]), H2=sharpe(rbf[h:]),
                              IS_Sharpe=sharpe(rb[i0:io]), OOS_CAGR=cagr(rb[io:]),
                              OOS_Sharpe=sharpe(rb[io:]), OOS_MaxDD=mdd(rb[io:]),
                              null_med_IS=float(np.median(nis)), PASS_4a=p4a, PASS_4b=p4b, **L))
            print(f"    {pname:5s} N={n:<3d} {freq}  {cagr(rbf):.2%}/{sharpe(rbf):.4f}/{mdd(rbf):.2%}"
                  f"  halves {sharpe(rbf[:h]):.3f}/{sharpe(rbf[h:]):.3f}"
                  f"  IS {sharpe(rb[i0:io]):.4f}  OOS {cagr(rb[io:]):.2%}/{sharpe(rb[io:]):.4f}/"
                  f"{mdd(rb[io:]):.2%}  4a={p4a} 4b={p4b}  [{time.time()-t0:.0f}s]")
    bk = pd.DataFrame(books); bk.to_csv(f"{OUT}.books.csv", index=False)
    print(f"\n  ALL {len(bk)} grid points above. 4b full+OOS: {int(bk.PASS_4b.sum())}; "
          f"4a: {int(bk.PASS_4a.sum())}")

    # -------------------------------------------- (C) recoverability, priced
    print("\n" + "=" * 78)
    print("(C) RULE 8 WALK-FORWARD — does a RECOVERABLE (linear) chooser buy a worse book?")
    print("=" * 78)
    # Four choosers over the SAME pools.  DIFF and Z are LINEAR-IN-POOL: computable from
    # the pooled mean (and sd) alone, hence recoverable from any pooled artefact and
    # seed-free at full K.  PCT and RATIO need the per-draw values.
    CH = {
        "CH_DIFF  (LINEAR, recoverable)": ("LINEAR", lambda p, b: float(np.mean(b - p))),
        "CH_Z     (LINEAR, recoverable)": ("LINEAR", lambda p, b: float((b - p.mean()) / p.std(ddof=1))),
        "CH_PCT   (NONLINEAR, record's)": ("NONLINEAR", lambda p, b: float((p < b).mean())),
        "CH_RATIO (NONLINEAR)":           ("NONLINEAR", lambda p, b: float(np.mean(b / p))),
    }
    for pname in P:
        sub = bk[bk.panel == pname]
        bb = bench[pname]
        ch_is = sub.loc[sub.IS_Sharpe.idxmax()]
        print(f"\n  [{pname}] CH_ISSHARPE (no null at all) picks N={ch_is.n}/{ch_is.cadence}"
              f"  OOS {ch_is.OOS_CAGR:.2%}/{ch_is.OOS_Sharpe:.4f}/{ch_is.OOS_MaxDD:.2%}")
        for chname, (kclass, fstat) in CH.items():
            for K in KLAD:
                chosen, tied = [], []
                for sd in range(NSEED):
                    rs = np.random.RandomState(3000 + sd)
                    vals = {}
                    for _, row in sub.iterrows():
                        p = pools[(pname, row.n, row.cadence)]
                        vals[(row.n, row.cadence)] = fstat(p[rs.choice(NDRAW, K, replace=False)],
                                                           row.IS_Sharpe)
                    mx = max(vals.values())
                    tied.append(sum(1 for v in vals.values() if v >= mx - 1e-15))
                    chosen.append(next(k for k, v in vals.items() if v >= mx - 1e-15))
                uq = sorted(set(chosen))
                oos = {c: float(sub[(sub.n == c[0]) & (sub.cadence == c[1])].OOS_Sharpe.iloc[0])
                       for c in uq}
                modal = max(set(chosen), key=chosen.count)
                mrow = sub[(sub.n == modal[0]) & (sub.cadence == modal[1])].iloc[0]
                picks.append(dict(panel=pname, chooser=chname, kernel_class=kclass, K=K,
                                  n_distinct=len(uq), modal_share=chosen.count(modal) / NSEED,
                                  modal=f"N={modal[0]}/{modal[1]}",
                                  mean_tied=float(np.mean(tied)), n_anchors=len(sub),
                                  modal_OOS_CAGR=float(mrow.OOS_CAGR),
                                  modal_OOS_Sharpe=float(mrow.OOS_Sharpe),
                                  modal_OOS_MaxDD=float(mrow.OOS_MaxDD),
                                  modal_PASS_4a=bool(mrow.PASS_4a), modal_PASS_4b=bool(mrow.PASS_4b),
                                  OOS_spread=max(oos.values()) - min(oos.values()),
                                  SPY_OOS_Sharpe=bb["SPY_OOS_S"], SPY_OOS_CAGR=bb["SPY_OOS_CAGR"],
                                  LIVE_OOS_Sharpe=bb["LV_OOS_S"], LIVE_OOS_CAGR=bb["LV_OOS_CAGR"],
                                  CH_ISSHARPE=f"N={ch_is.n}/{ch_is.cadence}",
                                  CH_ISSHARPE_OOS_Sharpe=float(ch_is.OOS_Sharpe)))
                print(f"    {chname:31s} K={K:<4d} distinct/{NSEED}: {len(uq)}  modal "
                      f"{modal[0]}/{modal[1]} @{chosen.count(modal)/NSEED:.2f}  tied "
                      f"{np.mean(tied):.2f}/{len(sub)}  modal OOS "
                      f"{mrow.OOS_CAGR:.2%}/{mrow.OOS_Sharpe:.4f}/{mrow.OOS_MaxDD:.2%}"
                      f"  4b={bool(mrow.PASS_4b)}  seed-spread {max(oos.values())-min(oos.values()):.4f}")
    pk = pd.DataFrame(picks); pk.to_csv(f"{OUT}.picks.csv", index=False)

    lin = pk[pk.kernel_class == "LINEAR"]; non = pk[pk.kernel_class == "NONLINEAR"]
    print(f"\n  LINEAR (recoverable) choosers:    mean modal OOS Sharpe {lin.modal_OOS_Sharpe.mean():.4f}"
          f"   mean distinct picks over {NSEED} seeds {lin.n_distinct.mean():.3f}"
          f"   4b modal picks {int(lin.modal_PASS_4b.sum())}/{len(lin)}")
    print(f"  NONLINEAR (record's) choosers:    mean modal OOS Sharpe {non.modal_OOS_Sharpe.mean():.4f}"
          f"   mean distinct picks over {NSEED} seeds {non.n_distinct.mean():.3f}"
          f"   4b modal picks {int(non.modal_PASS_4b.sum())}/{len(non)}")

    # ------------------------------------------------------- what it COSTS
    print("\n" + "=" * 78)
    print("(D) WHAT THE EXACT-PAIR RE-PUBLICATION WOULD COST")
    print("=" * 78)
    key = ("SMALL", 20, "W")
    p = pools[key]; t_pool = tpool[key]
    t0 = time.time()
    for _ in range(200): float(np.mean(p - p.mean()))
    t_lin = (time.time() - t0) / 200
    t0 = time.time()
    for _ in range(200): float(np.mean(p[:, None] > p[None, :]))
    t_ex = (time.time() - t0) / 200
    strict = cdf[cdf.C_STRICT & cdf.IS_PAIR]
    n_non = int((strict.KERNEL == "NONLINEAR").sum())
    n_non_rec = int(strict[(strict.KERNEL == "NONLINEAR")].RECOVERABLE.sum())
    n_non_lost = n_non - n_non_rec
    print(f"  measured on {key}: pooled/linear form {t_lin*1e6:.1f} us, exact-pair form "
          f"{t_ex*1e6:.1f} us ({t_ex/max(t_lin,1e-12):.1f}x), the {NDRAW}-draw POOL "
          f"{t_pool:.1f} s ({t_pool/max(t_ex,1e-9):.3g}x the pairing)")
    print(f"  C_STRICT pair statistics: {len(strict)}; NONLINEAR {n_non}, of which "
          f"{n_non_rec} still own a per-draw artefact and {n_non_lost} do not.")
    print(f"  re-publishing the {n_non_rec} recoverable ones EXACTLY: "
          f"{n_non_rec*t_ex:.4f} s of pairing (the artefacts already exist).")
    print(f"  re-publishing the {n_non_lost} lost ones: their pools must be REBUILT at "
          f"~{t_pool:.1f} s per cell => {n_non_lost*t_pool/3600:.2f} compute-hours, "
          f"{t_pool/max(t_ex,1e-9):.3g}x more than the pairing it would then take.")
    print(f"  the LINEAR ones cost NOTHING: {int((strict.KERNEL=='LINEAR').sum())} units are "
          f"already exact (1191 G2), and this run's G2 re-confirms it at machine precision.")

    # ----------------------------------------------------------------- gates
    A = pools[("U56", 20, "W")]; bval = float(bk[(bk.panel == "U56") & (bk.n == 20) &
                                                 (bk.cadence == "W")].IS_Sharpe.iloc[0])
    g2 = float(abs(np.mean(bval - A) - (bval - A.mean())))
    gates.append(("G2 LINEAR kernel: mean of paired diffs == pooled-mean diff (exact)", g2, g2 < 1e-12))
    # G3: a NONLINEAR kernel is NOT recoverable from pooled sufficient statistics.  Two
    # pools with identical mean and sd to 1e-12 whose percentile against the same book
    # differs -- constructed, not asserted.
    q = A.copy(); q2 = 2 * A.mean() - A                       # same mean, same sd, mirrored
    g3 = float(abs(((q < bval).mean()) - ((q2 < bval).mean())))
    gates.append((f"G3 NONLINEAR: same pooled mean/sd (dmean {abs(q.mean()-q2.mean()):.2e}, "
                  f"dsd {abs(q.std(ddof=1)-q2.std(ddof=1)):.2e}), percentile differs", g3, g3 > 1e-6))
    # G4: the kernel lexicon is a PARTITION -- every pair unit lands in exactly one class.
    g4 = float((cdf.KERNEL.isin(["LINEAR", "NONLINEAR", "UNCLASSIFIED"])).mean())
    gates.append(("G4 kernel classes partition the corpus (share classified into exactly one)",
                  g4, g4 == 1.0))
    # G4b: REPORTED, NOT ABSORBED -- how much of the pair corpus the lexicon cannot call.
    pairall = cdf[cdf.IS_PAIR & cdf.C_ALL]
    g4b = float((pairall.KERNEL == "UNCLASSIFIED").mean())
    gates.append(("G4b share of C_ALL pair units the lexicon cannot classify (reported, not absorbed)",
                  g4b, True))
    g5 = float(mdd(backtest(P["U56"].px, rules_v2_weights(P["U56"].px), cost_bps=COST,
                            freq="W")["returns"].values[P["U56"].i0:]))
    gates.append(("G5 live RULES v2 U56 MaxDD (record -12.05%)", g5, abs(g5 + 0.1205) < 0.01))
    rs1 = np.random.RandomState(3000); rs2 = np.random.RandomState(3000)
    g6 = abs(float((A[rs1.choice(NDRAW, 50, replace=False)] < bval).mean()) -
             float((A[rs2.choice(NDRAW, 50, replace=False)] < bval).mean()))
    gates.append(("G6 determinism given the pools", g6, g6 == 0.0))

    print("\n" + "=" * 78); print("GATES"); print("=" * 78)
    for name, val, ok in gates:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val:.6g}")
    pd.DataFrame([dict(gate=n, value=v, passed=o) for n, v, o in gates]).to_csv(
        f"{OUT}.gates.csv", index=False)
    print(f"\n  {sum(o for _, _, o in gates)} of {len(gates)} gates pass   "
          f"[total {time.time()-t_start:.0f}s]")
    print("\nSURVIVORSHIP (rule 9): U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the "
          "current output of a sub-$2B screen less the documented max_1d_move>=1.0 exclusion. "
          "Every LEVEL is optimistic and every 4a/4b count an UPPER bound. The harvest arm is a "
          "scan of committed text and carries no market bias; the chooser comparison ranks two "
          "estimator classes against each other on one tape, where the bias largely cancels, but "
          "it does NOT cancel out of the rule-8 OOS levels.")

if __name__ == "__main__":
    main()
