#!/usr/bin/env python3
"""Idea 1191 (cloud lane, 2026-09-17, idea 2 of 2): how many committed MONTE-CARLO
STATISTICS in the record are REPRODUCIBLE FROM THEIR ARTEFACT?

QUESTION. Idea 1188 found 1148's per-rung R_MATCHED replays at 6 of 1,458 because a
200-pair Monte-Carlo statistic published without its draw order is not recoverable,
while the same statistic's POOLED cell replays bit for bit. Census every committed
figure computed from a seeded resample or MC pair draw, report how many state enough
(seed, draw count, pair form) to be re-run, and price what the EXACT-PAIR form costs.

TWO DIALS AND NO MORE (rule 4, and the queue names both):
    dial 1 = CLAIM SET       {C_STRICT, C_PROX, C_ALL}
    dial 2 = STATISTIC FORM  {F_MC (K sampled pairs), F_EXACT (all KxK pairs), F_POOLED}
=> 9 cells, every one published.
NOT dials, reported at every value: PANEL {U56, B136, SMALL}; ANCHOR (N, cadence) in
{(20,W),(12,W),(20,M),(10,M)}; the K ladder {10,20,50,100,200,400}; 20 seeds at every K;
the three pair kernels {DIFF, RATIO, IND}; the 4a/4b legs; the rule-8 choosers.

PRICE ARM. Pool B = 400 gross-matched null books per (panel, anchor) — at every
rebalance date, N names drawn uniformly from those priced that day, weight 0.75/N,
10 bps, next-day execution. Pool A = 400 63-day moving-block bootstrap resamples of the
REAL book's own daily net returns. The published statistic is a pair statistic over
(A, B), exactly the shape 1148 published and 1188 could not replay.
"""
import sys, re, time, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights                    # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, rebalance_mask, metrics                    # noqa: E402

OUT     = Path(__file__).with_suffix("")
COST    = 10.0
GROSS   = 0.75
ANCHORS = [(20, "W"), (12, "W"), (20, "M"), (10, "M")]
NDRAW   = 400
KLAD    = [10, 20, 50, 100, 200, 400]
NSEED   = 20
BLOCK   = 63
OOS_START = "2017-01-01"
WARMUP  = 260

# ======================================================================= runner
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
    """fast_backtest, but target weights are supplied ONLY on rebalance rows (Wstart[k]
    is the target set at segment k). Identical arithmetic to engine.backtest (G1)."""
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

# ======================================================================= book
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
    """gross-matched null: at each rebalance date draw n names uniformly from those
    priced that day, weight GROSS/n. Same target gross, same holding count, no score."""
    starts, _ = pan.seg[freq]
    M = pan.rets.shape[1]
    out = np.zeros((len(starts), M))
    for k, i in enumerate(starts):
        avail = pan.iinv[pan.priced[max(i - 1, 0)][pan.iinv]]
        if len(avail) < n:
            continue
        pick = rng.choice(avail, size=n, replace=False)
        out[k, pick] = GROSS / n
    return out

def sharpe(r):
    v = r.std(ddof=0) * np.sqrt(252)
    return r.mean() * 252 / v if v > 0 else np.nan

def mdd(r):
    e = np.cumprod(1 + r); return (e / np.maximum.accumulate(e) - 1).min()

def cagr(r):
    e = np.cumprod(1 + r); return e[-1] ** (252 / len(r)) - 1

# ======================================================================= census
GEN = re.compile(r"\b(seed|seeds|seeded|bootstrap|bootstrapped|permutation|permuted|"
                 r"resampl\w*|monte[- ]?carlo|shuffl\w*|draws?|redraw\w*)\b", re.I)
NEAR = re.compile(r"\b(null|coin[- ]flip|percentile of its own|matched null|control)\b", re.I)
NUM = re.compile(r"\d")
SEEDT = re.compile(r"\b(seed\s*=?\s*\d+|seeds?\b[^.]{0,30}?\d|rng|random_state|np\.random)\b", re.I)
COUNT = re.compile(r"(\d[\d,]*)\s*(?:-|\s)?\s*(draws?|seeds?|pairs?|resamples?|replicat\w*|"
                   r"bootstrap\w*|permutations?|paths?|simulations?)\b", re.I)
ORDER = re.compile(r"\b(draw order|loop order|pair(?:ed|ing)?|per[- ]pair|matched draw|"
                   r"same draw|exact[- ]pair|pairwise|element[- ]wise)\b", re.I)

def units():
    """Committed text units: LEADERBOARD rows, CHANGELOG paragraphs, *.result.md and
    any backtest report .md. One unit = one row / one paragraph."""
    U = []
    lb = (ROOT / "research" / "LEADERBOARD.md").read_text().split("\n")
    for ln in lb:
        if ln.startswith("| 20"):
            U.append(("LEADERBOARD", ln))
    cl = (ROOT / "research" / "CHANGELOG.md").read_text().split("\n\n")
    for para in cl:
        if para.strip():
            U.append(("CHANGELOG", para))
    n_md = 0
    for f in sorted((ROOT / "research" / "backtests").rglob("*.md")):
        n_md += 1
        for para in f.read_text(errors="ignore").split("\n\n"):
            if para.strip():
                U.append((f.name, para))
    return U, n_md

def census():
    U, n_md = units()
    fileset = {}
    for src, txt in U:
        fileset.setdefault(src, False)
        if GEN.search(txt) or NEAR.search(txt):
            fileset[src] = True
    rows = []
    for src, txt in U:
        g, nr, num = bool(GEN.search(txt)), bool(NEAR.search(txt)), bool(NUM.search(txt))
        rows.append(dict(
            src=src, n_chars=len(txt),
            C_STRICT=g and num,
            C_PROX=(g or nr) and num,
            C_ALL=fileset[src] and num,
            HAS_SEED=bool(SEEDT.search(txt)),
            HAS_COUNT=bool(COUNT.search(txt)),
            HAS_ORDER=bool(ORDER.search(txt))))
    df = pd.DataFrame(rows)
    df["RERUNNABLE"] = df.HAS_SEED & df.HAS_COUNT & df.HAS_ORDER
    return df, len(U), n_md

def csv_seed_stamps():
    """How many committed backtest CSVs carry a seed / draw-index column at all."""
    tot = withseed = 0
    for f in sorted((ROOT / "research" / "backtests").rglob("*.csv")):
        tot += 1
        try:
            head = f.open().readline().lower()
        except Exception:
            continue
        if re.search(r"\b(seed|draw|rep|sim|iter)\w*\b", head):
            withseed += 1
    return tot, withseed

# ======================================================================= main
def main():
    print("=" * 78); print("(A) THE CENSUS — committed text units carrying an MC-derived figure"); print("=" * 78)
    cdf, nU, n_md = census()
    cdf.to_csv(f"{OUT}.census.csv", index=False)
    tot_csv, seed_csv = csv_seed_stamps()
    print(f"  corpus: {nU} committed text units "
          f"(LEADERBOARD rows {int((cdf.src=='LEADERBOARD').sum())}, "
          f"CHANGELOG paragraphs {int((cdf.src=='CHANGELOG').sum())}, "
          f"{n_md} markdown artefacts)")
    cen = []
    for cs in ["C_STRICT", "C_PROX", "C_ALL"]:
        s = cdf[cdf[cs]]
        r = dict(claim_set=cs, n=len(s),
                 seed=s.HAS_SEED.mean(), count=s.HAS_COUNT.mean(),
                 order=s.HAS_ORDER.mean(), rerunnable=s.RERUNNABLE.mean(),
                 n_rerunnable=int(s.RERUNNABLE.sum()))
        cen.append(r)
        print(f"  {cs:9s} n={len(s):6d}   states SEED {r['seed']:.4f}   COUNT {r['count']:.4f}   "
              f"PAIR FORM {r['order']:.4f}   ALL THREE {r['rerunnable']:.4f} ({r['n_rerunnable']})")
    pd.DataFrame(cen).to_csv(f"{OUT}.censusgrid.csv", index=False)
    print(f"  committed CSV artefacts under research/backtests: {tot_csv}; "
          f"carrying a seed/draw/rep column: {seed_csv} ({seed_csv/max(tot_csv,1):.4f})")

    # ------------------------------------------------------------- price arm
    print("\n" + "=" * 78); print("(B) THE PRICE ARM — real pools, 3 panels x 4 anchors x 400 draws"); print("=" * 78)
    P = {}
    u = load_universe();               P["U56"] = Panel("U56", u, list(u.columns))
    b = load_universe(broad=True);     P["B136"] = Panel("B136", b, list(b.columns))
    s = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in s.columns if c != "SPY" and c not in bad]
    P["SMALL"] = Panel("SMALL", s[keep + ["SPY"]], keep)
    print(f"  panels: U56 {u.shape}, B136 {b.shape}, SMALL {P['SMALL'].px.shape} "
          f"(dropped {len(bad)} max_1d_move>=1.0 names, {len(keep)} investable)")

    gates, books, forms, picks = [], [], [], []
    pools, tcost = {}, {}

    # G1: the starts-runner == engine.backtest on a live cell, post-warm-up
    pan = P["U56"]; W = book_weights(pan, 20)
    r_fast = run_from_starts(pan, "W", starts_from_weights(pan, "W", W))
    r_eng = backtest(pan.px, W, cost_bps=COST, freq="W")["returns"].values
    g = float(np.abs(r_fast[pan.i0:] - r_eng[pan.i0:]).max())
    gates.append(("G1 starts-runner == engine.backtest, post-warm-up (max abs diff)", g, g < 1e-12))
    # G1b: A DEFECT THIS RUN FOUND AND PRICED RATHER THAN HID. engine.backtest does
    # `weights.shift(1)` WITHOUT filling, so row 0's target is NaN; turnover is then NaN
    # at row 0 and again at the first rebalance-application row, and the NaN propagates
    # into `returns` at exactly those two rows. Every committed "fast runner ==
    # engine.backtest" gate in the record compared pandas SERIES, whose .max() is
    # skipna, so those two rows have never been checked by any of them. Both rows sit
    # inside the 260-day warm-up every metric discards, so NO committed figure moves —
    # but the gate that was supposed to catch it could not.
    nan_rows = np.flatnonzero(np.isnan(r_eng))
    g1b = int(len(nan_rows))
    gates.append((f"G1b engine.backtest emits NaN at rows {list(nan_rows)} "
                  f"({[str(pan.px.index[k].date()) for k in nan_rows]}), all inside warm-up "
                  f"(warm-up ends {pan.px.index[pan.i0].date()}) — reported, not absorbed",
                  g1b, bool((nan_rows < pan.i0).all())))

    rng_master = np.random.RandomState(20260917)
    for pname, pan in P.items():
        spy = pan.px["SPY"].pct_change().fillna(0).values
        lv = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        i0, io = pan.i0, pan.ioos
        sl = slice(i0, None)
        S = lambda x: sharpe(x[sl])
        print(f"\n  [{pname}] SPY {cagr(spy[sl]):.2%}/{S(spy):.4f}/{mdd(spy[sl]):.2%} "
              f"OOS {sharpe(spy[io:]):.4f} | RULES v2 live {cagr(lv[sl]):.2%}/{S(lv):.4f}/"
              f"{mdd(lv[sl]):.2%} OOS {sharpe(lv[io:]):.4f}")
        for (n, freq) in ANCHORS:
            t0 = time.time()
            W = book_weights(pan, n)
            rb = run_from_starts(pan, freq, starts_from_weights(pan, freq, W))
            rbf = rb[sl]
            h = len(rbf) // 2
            # ---- pool B: 400 gross-matched nulls
            nullS = np.zeros(NDRAW); nullS_is = np.zeros(NDRAW); nullS_oos = np.zeros(NDRAW)
            for d in range(NDRAW):
                rng = np.random.RandomState(rng_master.randint(0, 2**31 - 1))
                rn = run_from_starts(pan, freq, null_starts(pan, freq, n, rng))
                nullS[d] = sharpe(rn[sl]); nullS_is[d] = sharpe(rn[i0:io]); nullS_oos[d] = sharpe(rn[io:])
            # ---- pool A: 400 block-bootstrap resamples of the book's own returns
            bs = np.zeros(NDRAW)
            nb = int(np.ceil(len(rbf) / BLOCK))
            brng = np.random.RandomState(rng_master.randint(0, 2**31 - 1))
            for d in range(NDRAW):
                st = brng.randint(0, len(rbf) - BLOCK, size=nb)
                path = np.concatenate([rbf[t:t + BLOCK] for t in st])[:len(rbf)]
                bs[d] = sharpe(path)
            pools[(pname, n, freq)] = (bs, nullS, nullS_is, nullS_oos)
            tcost[(pname, n, freq)] = time.time() - t0
            # ---- 4a / 4b on the real book
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
                              null_med_Sharpe=float(np.median(nullS)),
                              pct_in_null=float((nullS < sharpe(rbf)).mean()),
                              PASS_4b=p4b, PASS_4a=p4a, **L))
            print(f"    {pname:5s} N={n:<3d} {freq}  book {cagr(rbf):.2%}/{sharpe(rbf):.4f}/{mdd(rbf):.2%}"
                  f"  null median Sharpe {np.median(nullS):.4f}  book pct {100*(nullS<sharpe(rbf)).mean():.1f}"
                  f"  4b={p4b} 4a={p4a}  [{time.time()-t0:.0f}s]")
    bk = pd.DataFrame(books); bk.to_csv(f"{OUT}.books.csv", index=False)

    # ---------------------------------------------------------- the 3 forms
    print("\n" + "=" * 78)
    print("(C) THE THREE STATISTIC FORMS — F_MC (K sampled pairs) / F_EXACT (all KxK) / F_POOLED")
    print("=" * 78)
    KER = dict(DIFF=lambda a, b: a - b,
               RATIO=lambda a, b: a / b,
               IND=lambda a, b: (a > b).astype(float))
    for key, (A, B, _, _) in pools.items():
        pname, n, freq = key
        for kname, f in KER.items():
            for K in KLAD:
                mc, ex, po = [], [], []
                for sd in range(NSEED):
                    rs = np.random.RandomState(1000 + sd)
                    ia = rs.choice(NDRAW, K, replace=False)
                    ib = rs.choice(NDRAW, K, replace=False)
                    a, b = A[ia], B[ib]
                    mc.append(float(np.mean(f(a, b))))                        # i-th with i-th
                    ex.append(float(np.mean(f(a[:, None], b[None, :]))))      # all K x K
                    po.append(float(f(np.mean(a), np.mean(b))))
                mc, ex, po = np.array(mc), np.array(ex), np.array(po)
                forms.append(dict(panel=pname, n=n, cadence=freq, kernel=kname, K=K,
                                  F_MC=mc.mean(), F_MC_sd=mc.std(ddof=1),
                                  F_EXACT=ex.mean(), F_EXACT_sd=ex.std(ddof=1),
                                  F_POOLED=po.mean(), F_POOLED_sd=po.std(ddof=1),
                                  mean_abs_MC_minus_EXACT=float(np.abs(mc - ex).mean()),
                                  exact_minus_pooled=float(np.abs(ex - po).max()),
                                  replay_1e6=float((np.abs(mc - mc[0]) < 1e-6).mean()),
                                  replay_5e3=float((np.abs(mc - mc[0]) < 5e-3).mean())))
    fm = pd.DataFrame(forms); fm.to_csv(f"{OUT}.forms.csv", index=False)

    for kname in KER:
        sub = fm[fm.kernel == kname]
        print(f"\n  kernel {kname}:")
        for K in KLAD:
            s = sub[sub.K == K]
            print(f"    K={K:<4d} cross-seed SD  F_MC {s.F_MC_sd.median():.6f}  "
                  f"F_EXACT {s.F_EXACT_sd.median():.6f}  F_POOLED {s.F_POOLED_sd.median():.6f}   "
                  f"|MC-EXACT| {s.mean_abs_MC_minus_EXACT.median():.6f}   "
                  f"|EXACT-POOLED| max {s.exact_minus_pooled.max():.3e}   "
                  f"replay@5e-3 {s.replay_5e3.median():.3f}")

    # G2: for a LINEAR kernel the exact-pair form IS the pooled form, exactly
    g2 = float(fm[fm.kernel == "DIFF"].exact_minus_pooled.max())
    gates.append(("G2 DIFF kernel: F_EXACT == F_POOLED (max abs dev)", g2, g2 < 1e-10))
    # G3: for the NONLINEAR kernels it is not
    g3 = float(fm[fm.kernel != "DIFF"].exact_minus_pooled.max())
    gates.append(("G3 RATIO/IND kernels: F_EXACT != F_POOLED (max abs dev, >0 expected)", g3, g3 > 1e-6))
    # G4: F_EXACT is the less seed-dependent form — TRUE for DIFF and IND, and the first
    # cut of this run gated it over ALL kernels and FAILED at 0.8936. The failures are
    # every one of them RATIO cells, and they are a finding, not a bug: enumerating all
    # KxK pairs gives the near-zero-Sharpe null draws in the DENOMINATOR more weight, so
    # the exact-pair form of a RATIO is MORE seed-dependent than the sampled one. The
    # gate is restated to what is actually true and the RATIO share is published beside it.
    lin = fm[fm.kernel != "RATIO"]
    g4 = float((lin.F_EXACT_sd <= lin.F_MC_sd + 1e-15).mean())
    gates.append(("G4 F_EXACT cross-seed SD <= F_MC's on DIFF+IND (share of cells)", g4, g4 == 1.0))
    rat = fm[fm.kernel == "RATIO"]
    g4b = float((rat.F_EXACT_sd <= rat.F_MC_sd + 1e-15).mean())
    gates.append(("G4b same on RATIO (share of cells; < 1 expected, REPORTED not absorbed)",
                  g4b, g4b < 1.0))
    # G5: live RULES v2 anchor reproduces
    g5 = float(mdd(backtest(P["U56"].px, rules_v2_weights(P["U56"].px), cost_bps=COST,
                            freq="W")["returns"].values[P["U56"].i0:]))
    gates.append(("G5 live RULES v2 U56 MaxDD (record -12.05%)", g5, abs(g5 + 0.1205) < 0.01))
    # G6: determinism of the whole form table given the pools
    chk = []
    A, B, _, _ = pools[("U56", 20, "W")]
    for _ in range(2):
        rs = np.random.RandomState(1000)
        ia, ib = rs.choice(NDRAW, 200, replace=False), rs.choice(NDRAW, 200, replace=False)
        chk.append(float(np.mean(A[ia] > B[ib])))
    g6 = abs(chk[0] - chk[1]); gates.append(("G6 determinism given the pools", g6, g6 == 0.0))

    # ---- what the exact-pair form COSTS -------------------------------------
    A, B, _, _ = pools[("SMALL", 20, "W")]
    t_pool = tcost[("SMALL", 20, "W")]
    t0 = time.time()
    for _ in range(200): np.mean(A - B)
    t_mc = (time.time() - t0) / 200
    t0 = time.time()
    for _ in range(200): np.mean(A[:, None] - B[None, :])
    t_ex = (time.time() - t0) / 200
    print(f"\n  COST of the exact-pair form at K={NDRAW}: F_MC {t_mc*1e6:.1f} us, "
          f"F_EXACT {t_ex*1e6:.1f} us ({t_ex/t_mc:.1f}x) — against the {NDRAW} BACKTESTS both "
          f"forms share ({t_pool:.1f}s for this cell, {t_pool/max(t_ex,1e-9):.3g}x the exact "
          f"pairing). The pools are the cost; the pairing is free.")
    rw = int((fm[fm.kernel == "RATIO"].F_EXACT_sd
              > fm[fm.kernel == "RATIO"].F_MC_sd + 1e-15).sum())
    print(f"  RATIO is the kernel where the exact form does NOT help: F_EXACT cross-seed SD "
          f"exceeds F_MC's at {rw} "
          f"of {int((fm.kernel=='RATIO').sum())} RATIO cells, and |F_EXACT - F_POOLED| reaches "
          f"{fm[fm.kernel=='RATIO'].exact_minus_pooled.max():.3g} — a near-zero null Sharpe in the "
          f"denominator, which all-pairs enumeration weights MORE heavily than random pairing.")

    # ---------------------------------------------------------- rule 8
    print("\n" + "=" * 78)
    print("(D) RULE 8 WALK-FORWARD — does the SEED of an MC null change the pick?")
    print("=" * 78)
    for pname in P:
        pan = P[pname]
        spy_oos = sharpe(pan.px["SPY"].pct_change().fillna(0).values[pan.ioos:])
        lv_oos = sharpe(backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST,
                                 freq="W")["returns"].values[pan.ioos:])
        sub = bk[bk.panel == pname]
        ch_is = sub.loc[sub.IS_Sharpe.idxmax()]
        # Two choosers on the SAME MC pool. CH_PCT is the record's form (the book's IS
        # percentile inside its own null) and it SATURATES — a book that beats every
        # draw reads 1.000 whatever the seed, so the statistic carries no ranking
        # information and the seed CANNOT move the pick. CH_Z is the same comparison
        # standardised by the pool's own mean and sd, which never saturates. Ties are
        # broken first-wins and DETERMINISTICALLY; the tied count is published, because
        # a random tie-break would manufacture the very instability being measured.
        for chname, fstat in [("CH_PCT (record's form)", lambda nis, b: float((nis < b).mean())),
                              ("CH_Z   (null-standardised)",
                               lambda nis, b: float((b - nis.mean()) / nis.std(ddof=1)))]:
            for K in KLAD:
                chosen, satur, tied = [], [], []
                for sd in range(NSEED):
                    rs = np.random.RandomState(2000 + sd)
                    vals = {}
                    for _, row in sub.iterrows():
                        _, _, nis, _ = pools[(pname, row.n, row.cadence)]
                        idx = rs.choice(NDRAW, K, replace=False)
                        vals[(row.n, row.cadence)] = fstat(nis[idx], row.IS_Sharpe)
                    mx = max(vals.values())
                    tied.append(sum(1 for v in vals.values() if v >= mx - 1e-15))
                    satur.append(sum(1 for v in vals.values() if v >= 1.0 - 1e-15))
                    chosen.append(next(k for k, v in vals.items() if v >= mx - 1e-15))
                uq = sorted(set(chosen))
                oos = {c: float(sub[(sub.n == c[0]) & (sub.cadence == c[1])].OOS_Sharpe.iloc[0])
                       for c in uq}
                modal = max(set(chosen), key=chosen.count)
                picks.append(dict(panel=pname, chooser=chname, K=K, n_distinct_picks=len(uq),
                                  modal_share=chosen.count(modal) / NSEED,
                                  modal=f"N={modal[0]}/{modal[1]}",
                                  mean_tied_at_max=float(np.mean(tied)),
                                  mean_saturated=float(np.mean(satur)), n_anchors=len(sub),
                                  OOS_min=min(oos.values()), OOS_max=max(oos.values()),
                                  OOS_spread=max(oos.values()) - min(oos.values()),
                                  modal_OOS=float(sub[(sub.n == modal[0]) &
                                                      (sub.cadence == modal[1])].OOS_Sharpe.iloc[0]),
                                  SPY_OOS=spy_oos, LIVE_OOS=lv_oos,
                                  CH_ISSHARPE=f"N={ch_is.n}/{ch_is.cadence}",
                                  CH_ISSHARPE_OOS=float(ch_is.OOS_Sharpe)))
                print(f"  {pname:5s} {chname:27s} K={K:<4d} distinct picks/{NSEED} seeds: {len(uq)}"
                      f"  modal {modal[0]}/{modal[1]} at {chosen.count(modal)/NSEED:.2f}"
                      f"  tied-at-max {np.mean(tied):.2f}/{len(sub)}  saturated {np.mean(satur):.2f}"
                      f"  OOS spread {max(oos.values())-min(oos.values()):.4f}")
        print(f"    [{pname}] SPY OOS {spy_oos:.4f}, LIVE OOS {lv_oos:.4f}, "
              f"CH_ISSHARPE (no null at all) picks N={ch_is.n}/{ch_is.cadence} "
              f"OOS {ch_is.OOS_Sharpe:.4f}")
    pk = pd.DataFrame(picks); pk.to_csv(f"{OUT}.picks.csv", index=False)

    print(f"\n  books clearing 4b full+OOS: {int(bk.PASS_4b.sum())} of {len(bk)};  "
          f"4a: {int(bk.PASS_4a.sum())} of {len(bk)}")
    if bk.PASS_4b.any():
        for _, r in bk[bk.PASS_4b].iterrows():
            print(f"    {r.panel:5s} N={r.n:<3d} {r.cadence}  {r.CAGR:.2%}/{r.Sharpe:.4f}/{r.MaxDD:.2%}"
                  f"  halves {r.H1:.3f}/{r.H2:.3f}  OOS {r.OOS_CAGR:.2%}/{r.OOS_Sharpe:.4f}"
                  f"  null pct {100*r.pct_in_null:.1f}")

    # ---------------------------------------------------------- gates
    print("\n" + "=" * 78); print("GATES"); print("=" * 78)
    for name, val, ok in gates:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val:.6g}")
    pd.DataFrame([dict(gate=n, value=v, passed=o) for n, v, o in gates]).to_csv(
        f"{OUT}.gates.csv", index=False)
    print(f"\n  {sum(o for _, _, o in gates)} of {len(gates)} gates pass")
    print("\nSURVIVORSHIP (rule 9): U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the "
          "current output of a sub-$2B screen less the documented max_1d_move>=1.0 exclusion. "
          "Every LEVEL is optimistic and every 4a/4b count an UPPER bound. The census arm is a "
          "scan of committed text and carries no market bias; the reproducibility statistics "
          "compare one construction against itself on one tape and the bias largely cancels, but "
          "it does NOT cancel out of the rule-8 OOS levels.")

if __name__ == "__main__":
    main()
