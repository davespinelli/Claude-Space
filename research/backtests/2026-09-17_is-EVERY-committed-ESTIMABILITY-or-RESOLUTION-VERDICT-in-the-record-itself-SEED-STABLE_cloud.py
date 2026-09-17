#!/usr/bin/env python3
"""Idea 1180 (cloud lane, idea 2 of 2) — 2026-09-17

QUESTION.  Idea 1170 found that re-running 1164's OWN 72 books with 5 seeds instead of 3
moves its committed ESTIMABLE count from 56 to 52: a verdict ABOUT noise is itself noisy,
and the record has no seed-count convention.  This run harvests the record's committed
estimability / resolution / "clears its own noise" verdicts, rebuilds the verdict on a
fresh 72-cell grid, re-scores it at 3 / 5 / 9 / 17 / 33 seeds, and reports how many flip
and what seed count fixes the verdict TO WITHIN ONE CELL.

TWO TUNED DIALS, every grid point reported:
  VERDICT SET  V_BAND / V_TSTAT / V_SIGN / V_RESOLVE
  SEED COUNT   3 / 5 / 9 / 17 / 33
Panel (U56 / B136 / SMALL), statistic (Sharpe / MaxDD / CAGR) and replicate index are
REPORTED axes, replicated at every point, not tuned.

METHOD NOTE, stated because it bounds every number below: the S-seed verdicts are scored
on seed SETS DRAWN WITHOUT REPLACEMENT FROM A COMMON POOL of NPOOL independent null
tapes per panel, not on NPOOL x REPL freshly drawn tapes.  Replicates at the same S are
therefore slightly dependent, which makes the flip rates reported here a LOWER bound on
the flip rate of fully independent re-runs.  A verdict that is already unstable under
this construction is unstable a fortiori.

PROTOCOL: 10 bps, weights decided at close t applied at t+1 (engine convention, gate G1),
both KEEP paths, rule-8 walk-forward (IS 2009-2016 chooses, OOS 2017-2026 read once).
Nothing is enacted; RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py untouched.

SURVIVORSHIP (rule 9): B136 and SMALL are current-constituent lists.  SMALL is the
current constituents of a sub-$2B screen, 664 columns after dropping the 52 tickers with
max_1d_move >= 1.0 from data/small_meta.csv.  Every delisted, zeroed or screened-out name
is absent, so every CAGR, drawdown and pass rate on those panels is the most flattering
the period could have produced.  They are breadth controls, not tradable claims.
"""
import sys, os, re, glob, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa

OUT = ROOT / "research" / "backtests"
SLUG = "2026-09-17_estimability-verdict-seed-stable_cloud"
COST, WARM, MAX_VOL = 10.0, 260, 0.60
OOS_START = "2017-01-01"
NS, GROSSES, CADENCES = [5, 10, 20, 40], [0.60, 0.75, 1.00], ["W", "M"]
SEED_COUNTS = [3, 5, 9, 17, 33]
VERDICT_SETS = ["V_BAND", "V_TSTAT", "V_SIGN", "V_RESOLVE"]
STATS = ["Sharpe", "MaxDD", "CAGR"]
NPOOL = 120          # independent null tapes per panel
REPL = 25            # seed-set replicates at each S
BASE_SEED = 7180
pd.set_option("display.width", 220)


# ----------------------------------------------------------------- fast runner
def run(R, W, mask):
    n, k = R.shape
    held = np.zeros((n, k)); turn = np.zeros(n); cur = np.zeros(k)
    for i in range(n):
        if mask[i] or i == 0:
            new = W[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        g = cur * (1.0 + R[i]); tot = g.sum() + (1.0 - cur.sum())
        if tot > 0: cur = g / tot
    return (held * R).sum(axis=1), turn


def prep(px, freq):
    return (px.pct_change().fillna(0.0).values,
            rebalance_mask(px.index, freq).shift(1, fill_value=False).values)


def met(r0, turn, bps=COST):
    r = r0 - turn * bps / 1e4
    eq = (1 + r).cumprod(); yrs = len(r) / 252.0
    dd = (eq / np.maximum.accumulate(eq) - 1).min()
    vol = r.std() * np.sqrt(252)
    return dict(CAGR=eq[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan,
                Sharpe=(r.mean() * 252) / vol if vol else np.nan, MaxDD=dd,
                Turn=turn.sum() / yrs)


def rank_of(px):
    sc, above, vol20 = score(px, vol_scale=False)
    return sc.where(above & (vol20 < MAX_VOL)).rank(axis=1, ascending=False)


def tape(px, kind, seed, bench_col="SPY"):
    """Controlled tape, listing dates respected (see idea 1175's script, same code).
    X_PERM: per-day cross-sectional permutation among names observable that day.
    X_ROT:  per-name circular rotation of that name's own observable return series."""
    cols = [c for c in px.columns if c != bench_col]
    X = px[cols]
    VP = X.notna().values
    VR = VP & np.vstack([np.zeros((1, VP.shape[1]), bool), VP[:-1]])
    U = X.pct_change().values
    U = np.where(VR, np.nan_to_num(U, nan=0.0), np.where(VP, 0.0, np.nan))
    rng = np.random.default_rng(seed)
    P = U.copy()
    if kind == "X_PERM":
        for i in range(U.shape[0]):
            v = np.flatnonzero(VR[i])
            if v.size > 1: P[i, v] = U[i, v][rng.permutation(v.size)]
    elif kind == "X_ROT":
        for j in range(U.shape[1]):
            v = np.flatnonzero(VR[:, j])
            if v.size > 1: P[v, j] = np.roll(U[v, j], int(rng.integers(0, v.size)))
    else:
        raise ValueError(kind)
    out = np.full(U.shape, np.nan)
    for j in range(U.shape[1]):
        v = np.flatnonzero(VP[:, j])
        if not v.size: continue
        seg = P[v, j].copy(); seg[0] = 0.0
        out[v, j] = X.values[v[0], j] * np.cumprod(1.0 + seg)
    D = pd.DataFrame(out, index=px.index, columns=cols)
    if bench_col in px.columns: D[bench_col] = px[bench_col].values
    return D[list(px.columns)]


BOOKS = [(f, n, g) for f in CADENCES for n in NS for g in GROSSES]


def book_stats(px, split=False):
    """All 24 books of the KEEP-4b family on this tape -> array [24, len(STATS)]
    (and, when split=True, the IS/OOS/half metrics needed for rule 8)."""
    rk = rank_of(px)
    i0 = WARM
    oi = px.index.get_indexer([pd.Timestamp(OOS_START)], method="bfill")[0]
    h = (len(px.index) - i0) // 2
    S = np.full((len(BOOKS), len(STATS)), np.nan)
    extra = []
    cache = {}
    for b, (freq, n, g) in enumerate(BOOKS):
        if freq not in cache: cache[freq] = prep(px, freq)
        R, mask = cache[freq]
        W = (rk <= n).astype(float).reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values * (g / n)
        r0, tn = run(R, W, mask)
        m = met(r0[i0:], tn[i0:])
        S[b] = [m[s] for s in STATS]
        if split:
            h1 = met(r0[i0:i0 + h], tn[i0:i0 + h]); h2 = met(r0[i0 + h:], tn[i0 + h:])
            oo = met(r0[oi:], tn[oi:]); iss = met(r0[i0:oi], tn[i0:oi])
            extra.append(dict(cadence=freq, n=n, gross=g, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                              MaxDD=m["MaxDD"], Turn=m["Turn"], H1=h1["Sharpe"], H2=h2["Sharpe"],
                              IS_Sharpe=iss["Sharpe"], IS_CAGR=iss["CAGR"], IS_MaxDD=iss["MaxDD"],
                              OOS_Sharpe=oo["Sharpe"], OOS_CAGR=oo["CAGR"], OOS_MaxDD=oo["MaxDD"]))
    return S, extra


def bench_stats(px):
    """SPY buy-and-hold on this panel's trading days: full, halves, IS and OOS."""
    idx = px.index; i0 = WARM
    oi = idx.get_indexer([pd.Timestamp(OOS_START)], method="bfill")[0]
    h = (len(idx) - i0) // 2
    spy = px["SPY"].pct_change().fillna(0.0).values
    z = lambda a: np.zeros(len(a))
    out = dict(met(spy[i0:], z(spy[i0:])))
    out["H1"] = met(spy[i0:i0 + h], z(spy[i0:i0 + h]))["Sharpe"]
    out["H2"] = met(spy[i0 + h:], z(spy[i0 + h:]))["Sharpe"]
    oo = met(spy[oi:], z(spy[oi:])); iss = met(spy[i0:oi], z(spy[i0:oi]))
    out.update(OOS_Sharpe=oo["Sharpe"], OOS_CAGR=oo["CAGR"], OOS_MaxDD=oo["MaxDD"],
               IS_Sharpe=iss["Sharpe"], IS_CAGR=iss["CAGR"], IS_MaxDD=iss["MaxDD"])
    return out


# ----------------------------------------------------------------- the verdicts
def verdict(obs, null, kind):
    """obs: scalar. null: 1-D array of S null draws of the same statistic.
    Returns True = the record would call this cell ESTIMABLE / RESOLVED."""
    null = np.asarray(null, float); null = null[np.isfinite(null)]
    if null.size < 2 or not np.isfinite(obs): return False
    if kind == "V_BAND":                      # outside the null's own 5-95 band
        lo, hi = np.percentile(null, [5, 95]); return bool(obs < lo or obs > hi)
    if kind == "V_TSTAT":                     # |obs - mean| / sd > 1.645
        sd = null.std(ddof=1)
        return bool(sd > 0 and abs(obs - null.mean()) / sd > 1.645)
    if kind == "V_SIGN":                      # strictly outside the null's full range
        return bool(obs > null.max() or obs < null.min())
    raise ValueError(kind)


def resolve_verdict(gap_obs, gap_null):
    """V_RESOLVE: is the GAP between two adjacent n-rungs larger than the null's own
    gap spread?  Same 5-95 rule, applied to the difference rather than the level."""
    return verdict(gap_obs, gap_null, "V_BAND")


# ================================================================== gates
def gates(P, dropped):
    print("\n" + "=" * 100)
    print("GATES  (printed before any hypothesis is read)")
    print("=" * 100)
    G = []
    px = P["U56"]; st = px.index[WARM]
    W = rules_v2_weights(px)
    for freq in ("W", "M"):
        R, mask = prep(px, freq)
        Wv = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
        r0, tn = run(R, Wv, mask)
        e = engine_backtest(px, W, cost_bps=COST, freq=freq)
        dr = float(np.abs((r0 - tn * COST / 1e4)[WARM:] - e["returns"].values[WARM:]).max())
        dt = float(np.abs(tn[WARM:] - e["turnover"].values[WARM:]).max())
        G.append((f"G1_{freq}", dr < 1e-12 and dt < 1e-9,
                  f"fast runner == engine.backtest  dret {dr:.3e} dturn {dt:.3e}"))
    R, mask = prep(px, "W")
    Wv = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    r0, tn = run(R, Wv, mask); m = met(r0[WARM:], tn[WARM:])
    G.append(("G2_LIVE", abs(m["CAGR"] - .0860) < 5e-4 and abs(m["Sharpe"] - 1.1980) < 3e-3
              and abs(m["MaxDD"] + .1205) < 5e-4,
              f"RULES v2 live {m['CAGR']:.2%}/{m['Sharpe']:.4f}/{m['MaxDD']:.2%} vs committed "
              f"8.60%/1.1980/-12.05%"))
    b = bench_stats(px)
    G.append(("G3_SPY", abs(b["CAGR"] - .1506) < 5e-4 and abs(b["Sharpe"] - .8814) < 3e-3,
              f"SPY {b['CAGR']:.2%}/{b['Sharpe']:.4f}/{b['MaxDD']:.2%} vs committed "
              f"15.06%/0.8814/-33.72%"))
    t1 = tape(px, "X_PERM", 11); cols = [c for c in px.columns if c != "SPY"]
    a = px[cols].pct_change().fillna(0.0).values; bb = t1[cols].pct_change().fillna(0.0).values
    dew = float(np.abs(a.mean(1) - bb.mean(1)).max())
    dmask = int((px[cols].notna().values != t1[cols].notna().values).sum())
    G.append(("G4_PERM", dew < 1e-14 and dmask == 0,
              f"X_PERM preserves the daily EW return ({dew:.3e}) and the listing mask ({dmask})"))
    t2 = tape(px, "X_ROT", 11); c2 = t2[cols].pct_change().fillna(0.0).values
    dmar = float(np.abs(np.sort(a, axis=0) - np.sort(c2, axis=0)).max())
    G.append(("G5_ROT", dmar < 1e-12, f"X_ROT preserves each name's return multiset ({dmar:.3e})"))
    dd = float(np.nanmax(np.abs(t1.values - tape(px, "X_PERM", 11).values)))
    G.append(("G6_DET", dd == 0.0, f"same seed -> identical tape ({dd:.3e})"))
    S1, _ = book_stats(px); S2, _ = book_stats(px)
    G.append(("G7_DET2", float(np.nanmax(np.abs(S1 - S2))) == 0.0,
              f"book grid deterministic ({float(np.nanmax(np.abs(S1-S2))):.3e})"))
    rk = rank_of(px); R, mask = prep(px, "W")
    Wc = (rk <= 20).astype(float).reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values * (0.75 / 20)
    r0, tn = run(R, Wc, mask); mc = met(r0[WARM:], tn[WARM:])
    G.append(("G8_CAND", abs(mc["MaxDD"] + .1831) < 5e-4 and abs(mc["CAGR"] - .1266) < 5e-3
              and 1.0596 <= mc["Sharpe"] <= 1.0921,
              f"CAND20 U56/W/gross0.75 {mc['CAGR']:.2%}/{mc['Sharpe']:.4f}/{mc['MaxDD']:.2%} vs "
              f"committed 12.66-12.73%/1.0596-1.0921/-18.31% (the record commits two Sharpes "
              f"for this book, 0.0325 apart; the gate brackets them)"))
    G.append(("G9_DROP", len(dropped) == 52 and P["SMALL"].shape[1] == 664,
              f"SMALL {P['SMALL'].shape[1]} cols after dropping {len(dropped)} max_1d_move>=1.0"))
    G.append(("G10_POOL", NPOOL >= max(SEED_COUNTS) * 3,
              f"seed pool {NPOOL} >= 3x the largest seed count {max(SEED_COUNTS)}"))
    for k, ok, msg in G:
        print(f"  {k:10s} {'PASS' if ok else 'FAIL'}  {msg}")
    print(f"  ---> {sum(1 for _, o, _ in G if o)} of {len(G)} gates PASS")
    return G


# ================================================================== PART A
VERDICT_COL_TOKENS = ("estimab", "resolv", "resolution", "seed_stab", "seedstab",
                      "clears", "inside", "outside", "own_noise")
PROSE_TOKENS = ("estimable", "not estimable", "unestimable", "resolvable", "unresolved",
                "clears its own noise", "seed-stable", "seed stable", "inside its own",
                "outside its own", "resolution")
SEED_TOKENS = ("seed", "seeds", "n_seed", "nseed", "seed_count")


def harvest():
    print("\n" + "=" * 100)
    print("PART A — THE HARVEST: the record's committed ESTIMABILITY / RESOLUTION verdicts,")
    print("         and whether any of them states the SEED COUNT it was read at.")
    print("=" * 100)
    rows = []
    for f in sorted(glob.glob(str(OUT / "*.csv"))):
        try: df = pd.read_csv(f, nrows=3000, low_memory=False)
        except Exception: continue
        low = {c: c.lower() for c in df.columns}
        vcols = [c for c in df.columns if any(t in low[c] for t in VERDICT_COL_TOKENS)]
        if not vcols: continue
        has_seed = any(any(t == low[c] or t in low[c] for t in SEED_TOKENS) for c in df.columns)
        nseed = np.nan
        for c in df.columns:
            if low[c] in ("seed", "seeds", "n_seeds", "nseed", "seed_count"):
                try: nseed = df[c].nunique()
                except Exception: pass
                break
        for c in vcols:
            s = df[c]
            isbool = s.dropna().astype(str).str.lower().isin(
                ("true", "false", "0", "1", "yes", "no")).all() and s.notna().any()
            rows.append(dict(file=os.path.basename(f), col=c, n_rows=len(df),
                             boolean_verdict=bool(isbool), states_seed_axis=bool(has_seed),
                             n_distinct_seeds=nseed))
    A = pd.DataFrame(rows)
    A.to_csv(OUT / f"{SLUG}.A_verdict_columns.csv", index=False)
    print(f"  MACHINE LAYER: {A.file.nunique() if len(A) else 0} committed CSVs carry a verdict "
          f"column; {len(A)} (file, column) verdict cells.")
    if len(A):
        print(f"    boolean verdicts:            {int(A.boolean_verdict.sum())} "
              f"({A.boolean_verdict.mean():.3f})")
        print(f"    carry a SEED axis at all:    {int(A.states_seed_axis.sum())} "
              f"({A.states_seed_axis.mean():.3f})")
        sd = A.n_distinct_seeds.dropna()
        print(f"    state a seed COUNT:          {len(sd)} ({len(sd)/len(A):.3f})"
              + (f"; counts seen: {sorted(set(int(x) for x in sd))}" if len(sd) else ""))
    prose = []
    for f in sorted(glob.glob(str(OUT / "*.md"))) + [str(ROOT / "research" / "LEADERBOARD.md"),
                                                     str(ROOT / "research" / "CHANGELOG.md")]:
        try: txt = Path(f).read_text(errors="ignore")
        except Exception: continue
        for sent in re.split(r"(?<=[.;])\s+|\n", txt):
            s = sent.strip()
            if not (20 <= len(s) <= 1200): continue
            ls = s.lower()
            if not any(t in ls for t in PROSE_TOKENS): continue
            prose.append(dict(file=os.path.basename(f),
                              names_seed_count=bool(re.search(r"\b\d+\s*seeds?\b", ls)),
                              has_number=bool(re.search(r"\d", s)), sentence=s[:400]))
    B = pd.DataFrame(prose)
    B.to_csv(OUT / f"{SLUG}.A_verdict_prose.csv", index=False)
    print(f"  READER LAYER: {len(B)} committed sentences publish an estimability / resolution "
          f"verdict, in {B.file.nunique() if len(B) else 0} files.")
    if len(B):
        print(f"    name the SEED COUNT they were read at: {int(B.names_seed_count.sum())} "
              f"({B.names_seed_count.mean():.4f})")
    return A, B


# ================================================================== main
def main():
    t0 = time.time()
    P = {"U56": load_universe(), "B136": load_universe(broad=True)}
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    dropped = sorted(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    s = load_universe(small=True)
    P["SMALL"] = s.drop(columns=[c for c in s.columns if c in set(dropped)])
    for k, v in P.items():
        print(f"panel {k:6s} {v.shape[0]} days x {v.shape[1]} cols  "
              f"{v.index[0].date()} -> {v.index[-1].date()}")
    gates(P, dropped)
    harvest()

    print("\n" + "=" * 100)
    print("PART B — THE ANSWER: is the ESTIMABILITY VERDICT itself SEED-STABLE?")
    print(f"         72 cells (3 panels x 24 books) x {NPOOL} null tapes per panel x "
          f"{len(SEED_COUNTS)} seed counts x {REPL} replicates x {len(VERDICT_SETS)} verdict sets")
    print("=" * 100)
    OBS, NUL, REALX, BEN = {}, {}, {}, {}
    for pn, px in P.items():
        obs, extra = book_stats(px, split=True)
        OBS[pn] = obs; REALX[pn] = extra; BEN[pn] = bench_stats(px)
        nul = np.full((NPOOL, len(BOOKS), len(STATS)), np.nan)
        for k in range(NPOOL):
            nul[k], _ = book_stats(tape(px, "X_PERM", BASE_SEED + 1000 * len(pn) + k))
        NUL[pn] = nul
        print(f"  {pn}: {NPOOL} null tapes x {len(BOOKS)} books built  [{time.time()-t0:.0f}s]")

    rng = np.random.default_rng(BASE_SEED)
    rows = []
    for vs in VERDICT_SETS:
        for S in SEED_COUNTS:
            for rep in range(REPL):
                for pn in P:
                    pick = rng.choice(NPOOL, size=S, replace=False)
                    for si, stat in enumerate(STATS):
                        if vs == "V_RESOLVE":
                            # adjacent n-rungs at matched (cadence, gross)
                            for b, (f, n, g) in enumerate(BOOKS):
                                if n == NS[0]: continue
                                b0 = BOOKS.index((f, NS[NS.index(n) - 1], g))
                                gap = OBS[pn][b, si] - OBS[pn][b0, si]
                                gn = NUL[pn][pick, b, si] - NUL[pn][pick, b0, si]
                                rows.append(dict(verdict_set=vs, S=S, rep=rep, panel=pn,
                                                 stat=stat, book=b,
                                                 v=resolve_verdict(gap, gn)))
                        else:
                            for b in range(len(BOOKS)):
                                rows.append(dict(verdict_set=vs, S=S, rep=rep, panel=pn,
                                                 stat=stat, book=b,
                                                 v=verdict(OBS[pn][b, si], NUL[pn][pick, b, si], vs)))
    V = pd.DataFrame(rows)
    V.to_csv(OUT / f"{SLUG}.B_verdicts.csv.gz", index=False, compression="gzip")
    print(f"  {len(V):,} verdict evaluations written  [{time.time()-t0:.0f}s]")

    print("\n  B1. VERDICT COUNT at each (verdict set, seed count) — the record's own headline")
    print("      form ('N of 72 ESTIMABLE'). Cell = mean count over replicates; the spread")
    print("      is what 1170 found moving 56 -> 52.")
    cnt = V.groupby(["verdict_set", "S", "rep", "stat"]).v.sum().reset_index()
    tab = cnt.pivot_table(index=["verdict_set", "stat"], columns="S", values="v",
                          aggfunc=["mean", "min", "max"])
    print(tab.to_string(float_format=lambda x: f"{x:.1f}"))

    print("\n  B2. SPREAD of the published count across replicates at the SAME seed count")
    print("      (max - min). 'Fixed to within one cell' means this is <= 1.")
    spread = cnt.groupby(["verdict_set", "stat", "S"]).v.agg(lambda x: x.max() - x.min()).unstack("S")
    print(spread.to_string())
    print("\n      smallest S that fixes the count to within ONE cell, by (verdict set, stat):")
    fix = {}
    for (vs, stat), row in spread.iterrows():
        ok = [S for S in SEED_COUNTS if row[S] <= 1]
        fix[(vs, stat)] = min(ok) if ok else None
        lo_S, hi_S = SEED_COUNTS[0], SEED_COUNTS[-1]
        print(f"        {vs:10s} {stat:7s} "
              f"{'S = ' + str(min(ok)) if ok else 'NOT FIXED at S <= ' + str(hi_S)}"
              f"   (spread at S={lo_S} {int(row[lo_S])}, S={hi_S} {int(row[hi_S])})")

    print("\n  B3. PER-CELL FLIP RATE: share of the 72 cells whose verdict is NOT unanimous")
    print("      across the replicates at that seed count.")
    flip = (V.groupby(["verdict_set", "S", "stat", "panel", "book"]).v
            .agg(lambda x: 0 < x.mean() < 1).groupby(level=[0, 1, 2]).mean().unstack("S"))
    print(flip.to_string(float_format=lambda x: f"{x:.3f}"))

    print("\n  B4. AGREEMENT with the S=33 full-information reference, per cell")
    ref = (V[V.S == max(SEED_COUNTS)].groupby(["verdict_set", "stat", "panel", "book"]).v
           .mean() > 0.5)
    agr = []
    for (vs, S, stat, pn, b), grp in V.groupby(["verdict_set", "S", "stat", "panel", "book"]):
        agr.append(dict(verdict_set=vs, S=S, stat=stat,
                        agree=float((grp.v == ref.loc[(vs, stat, pn, b)]).mean())))
    AG = pd.DataFrame(agr).groupby(["verdict_set", "stat", "S"]).agree.mean().unstack("S")
    print(AG.to_string(float_format=lambda x: f"{x:.3f}"))
    AG.to_csv(OUT / f"{SLUG}.B_agreement.csv")
    spread.to_csv(OUT / f"{SLUG}.B_count_spread.csv")
    flip.to_csv(OUT / f"{SLUG}.B_flip_rate.csv")

    # ================================================================ PART C
    print("\n" + "=" * 100)
    print("PART C — RULE 8 WALK-FORWARD + BOTH KEEP PATHS, and the PRICE of the verdict")
    print("         as a SELECTION DEVICE. IS 2009-2016 chooses; OOS 2017-2026 read once.")
    print("=" * 100)
    live = {}
    for pn, px in P.items():
        R, mask = prep(px, "W")
        Wv = rules_v2_weights(px).reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
        r0, tn = run(R, Wv, mask)
        i0 = WARM; oi = px.index.get_indexer([pd.Timestamp(OOS_START)], method="bfill")[0]
        h = (len(px.index) - i0) // 2
        live[pn] = dict(CAGR=met(r0[i0:], tn[i0:])["CAGR"], Sharpe=met(r0[i0:], tn[i0:])["Sharpe"],
                        MaxDD=met(r0[i0:], tn[i0:])["MaxDD"],
                        H1=met(r0[i0:i0 + h], tn[i0:i0 + h])["Sharpe"],
                        H2=met(r0[i0 + h:], tn[i0 + h:])["Sharpe"],
                        OOS_Sharpe=met(r0[oi:], tn[oi:])["Sharpe"],
                        OOS_CAGR=met(r0[oi:], tn[oi:])["CAGR"],
                        OOS_MaxDD=met(r0[oi:], tn[oi:])["MaxDD"])
    crows = []
    for pn in P:
        sp = BEN[pn]
        for b, e in enumerate(REALX[pn]):
            p4b = (e["H1"] > sp["H1"] and e["H2"] > sp["H2"] and e["OOS_Sharpe"] > sp["OOS_Sharpe"]
                   and abs(e["MaxDD"]) <= .60 * abs(sp["MaxDD"]) and e["CAGR"] >= .70 * sp["CAGR"])
            p4b_oos = (e["OOS_Sharpe"] > sp["OOS_Sharpe"]
                       and abs(e["OOS_MaxDD"]) <= .60 * abs(sp["OOS_MaxDD"])
                       and e["OOS_CAGR"] >= .70 * sp["OOS_CAGR"])
            p4a = (e["H1"] > live[pn]["H1"] and e["H2"] > live[pn]["H2"]
                   and e["MaxDD"] >= live[pn]["MaxDD"])
            crows.append(dict(panel=pn, book=b, **e, pass4b=p4b, pass4b_oos=p4b_oos, pass4a=p4a))
    C = pd.DataFrame(crows)
    C.to_csv(OUT / f"{SLUG}.C_books.csv", index=False)
    print(f"\n  {len(C)} real books, ALL published. base rates: 4b full {int(C.pass4b.sum())}, "
          f"4b OOS {int(C.pass4b_oos.sum())}, 4a {int(C.pass4a.sum())} of {len(C)}")
    print(C[["panel", "cadence", "n", "gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
             "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "Turn", "pass4b", "pass4b_oos", "pass4a"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # choosers: is a book's IS Sharpe ESTIMABLE against its own null at S seeds?
    print("\n  CHOOSERS. CH_ISSHARPE ignores the verdict; CH_ESTIM<S> restricts to books whose")
    print("  FULL-SAMPLE Sharpe is ESTIMABLE (V_BAND) against its own null at S seeds, the seed")
    print("  set drawn on the IS window's information only. All picks published.")
    prows = []
    rng2 = np.random.default_rng(BASE_SEED + 1)
    for pn in P:
        g = C[C.panel == pn].reset_index(drop=True)
        sp = BEN[pn]
        base = g.loc[g.IS_Sharpe.idxmax()]
        prows.append(dict(panel=pn, chooser="CH_ISSHARPE", S=0, n_eligible=len(g), **_pick(base, sp)))
        for S in SEED_COUNTS:
            for rep in range(REPL):
                pick = rng2.choice(NPOOL, size=S, replace=False)
                est = np.array([verdict(OBS[pn][b, 0], NUL[pn][pick, b, 0], "V_BAND")
                                for b in range(len(BOOKS))])
                sub = g[est] if est.any() else g
                row = sub.loc[sub.IS_Sharpe.idxmax()]
                prows.append(dict(panel=pn, chooser=f"CH_ESTIM", S=S, rep=rep,
                                  n_eligible=int(est.sum()), **_pick(row, sp)))
    PK = pd.DataFrame(prows)
    PK.to_csv(OUT / f"{SLUG}.C_picks.csv", index=False)
    print("\n  CH_ISSHARPE (the reference pick, one per panel):")
    print(PK[PK.chooser == "CH_ISSHARPE"].drop(columns=["rep"], errors="ignore")
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print("\n  CH_ESTIM across seed counts: does the seed count change WHICH BOOK IS PICKED,")
    print("  and what does it cost out of sample?")
    for pn in P:
        b0 = PK[(PK.panel == pn) & (PK.chooser == "CH_ISSHARPE")].iloc[0]
        for S in SEED_COUNTS:
            sub = PK[(PK.panel == pn) & (PK.chooser == "CH_ESTIM") & (PK.S == S)]
            moved = ((sub.n != b0.n) | (sub.gross != b0.gross) | (sub.cadence != b0.cadence))
            npicks = sub.groupby(["cadence", "n", "gross"]).size()
            print(f"    {pn:6s} S={S:<3d} eligible {sub.n_eligible.min()}-{sub.n_eligible.max()} of 24 | "
                  f"distinct picks {len(npicks)} | moves from CH_ISSHARPE at {int(moved.sum())}/{len(sub)} "
                  f"replicates | OOS Sharpe {sub.OOS_Sharpe.mean():.4f} "
                  f"(min {sub.OOS_Sharpe.min():.4f}, max {sub.OOS_Sharpe.max():.4f}) vs "
                  f"{b0.OOS_Sharpe:.4f} | 4b OOS {int(sub.pass4b_oos.sum())}/{len(sub)}")
    print(f"\n  picks overall: 4b full {int(PK.pass4b.sum())} of {len(PK)}, "
          f"4b OOS {int(PK.pass4b_oos.sum())} of {len(PK)}, 4a {int(PK.pass4a.sum())} of {len(PK)}")

    print("\n  BENCHMARKS (post-warm-up, 10 bps where applicable):")
    for pn in P:
        b = BEN[pn]; l = live[pn]
        print(f"    {pn:6s} SPY full {b['CAGR']:.2%}/{b['Sharpe']:.4f}/{b['MaxDD']:.2%} "
              f"OOS {b['OOS_CAGR']:.2%}/{b['OOS_Sharpe']:.4f}/{b['OOS_MaxDD']:.2%} | "
              f"LIVE v2 full {l['CAGR']:.2%}/{l['Sharpe']:.4f}/{l['MaxDD']:.2%} "
              f"OOS {l['OOS_CAGR']:.2%}/{l['OOS_Sharpe']:.4f}/{l['OOS_MaxDD']:.2%}")
    best = C[C.pass4b & C.pass4b_oos]
    if len(best):
        bb = best.loc[best.OOS_Sharpe.idxmax()]
        print(f"\n  BEST 4b book (full AND OOS): {bb.panel}/{bb.cadence}/n={int(bb.n)}/gross={bb.gross} "
              f"full {bb.CAGR:.2%}/{bb.Sharpe:.4f}/{bb.MaxDD:.2%} (H1 {bb.H1:.3f}/H2 {bb.H2:.3f}) "
              f"OOS {bb.OOS_CAGR:.2%}/{bb.OOS_Sharpe:.4f}/{bb.OOS_MaxDD:.2%}")
        r = PK[(PK.panel == bb.panel) & (PK.n == bb.n) & (PK.gross == bb.gross)
               & (PK.cadence == bb.cadence)]
        print(f"  IS-chooser-reachable: {'YES (' + str(len(r)) + ' of ' + str(len(PK)) + ' picks)' if len(r) else 'NO'}")
    else:
        print("\n  BEST 4b book (full AND OOS): NONE")
    print(f"\n  total runtime {time.time()-t0:.0f}s")
    print("  NOTHING ENACTED. RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py untouched.")


def _pick(row, sp):
    return dict(cadence=row.cadence, n=int(row.n), gross=float(row.gross),
                IS_Sharpe=row.IS_Sharpe, full_CAGR=row.CAGR, full_Sharpe=row.Sharpe,
                full_MaxDD=row.MaxDD, H1=row.H1, H2=row.H2, OOS_CAGR=row.OOS_CAGR,
                OOS_Sharpe=row.OOS_Sharpe, OOS_MaxDD=row.OOS_MaxDD,
                pass4b=bool(row.pass4b), pass4b_oos=bool(row.pass4b_oos), pass4a=bool(row.pass4a),
                spy_OOS_Sharpe=sp["OOS_Sharpe"], spy_OOS_CAGR=sp["OOS_CAGR"],
                spy_OOS_MaxDD=sp["OOS_MaxDD"])


if __name__ == "__main__":
    main()
