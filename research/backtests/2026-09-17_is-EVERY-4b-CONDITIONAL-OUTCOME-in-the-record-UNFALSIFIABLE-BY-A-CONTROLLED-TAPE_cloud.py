#!/usr/bin/env python3
"""Idea 1175 (cloud lane, idea 1 of 2) — 2026-09-17

QUESTION.  Idea 1171 found 1094's turnover->c* relation DEGENERATE at 9 of 9 synthetic
cells: c* is defined only on books that PASS 4b, no exchangeable tape ever produces one,
so the claim is neither confirmed nor refuted but UNFALSIFIABLE by the method the queue
proposed.  This run asks whether that defect is GENERAL -- how much of the record's
committed outcome layer is 4b-CONDITIONAL, i.e. has the 4b-passing set as its DOMAIN --
and prices the cheapest repair.

TWO TUNED DIALS, every grid point reported:
  OUTCOME SET  O_CSTAR / O_MARGIN / O_BINDING / O_SHARE
  REPAIR       R_NONE / R_DEGATE / R_MATCH / R_SOFT / R_REFUSE
Panel (U56 / B136 / SMALL), tape kind (X_PERM / X_ROT) and seed are REPORTED axes,
replicated at every point, not tuned.

PROTOCOL: 10 bps, weights decided at close t applied at t+1 (engine convention,
reproduced to 1e-17 by G1), both KEEP paths, rule-8 walk-forward (IS 2009-2016 only,
OOS 2017-2026 read once).  Nothing is enacted; RULES.md / PROTOCOL.md / scan.py /
bot.py / baseline.py are not touched.

SURVIVORSHIP (rule 9): B136 and SMALL are current-constituent lists.  SMALL is the
current constituents of a sub-$2B screen, 664 columns after dropping the 52 tickers with
max_1d_move >= 1.0 from data/small_meta.csv.  Every name that delisted, went to zero or
fell below the screen is absent, so every drawdown, CAGR and pass rate on those two
panels is the most flattering the period could have produced.  They are breadth
controls, not tradable claims.
"""
import sys, os, re, csv, glob, json, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa

OUT = ROOT / "research" / "backtests"
SLUG = "2026-09-17_4b-conditional-unfalsifiable_cloud"
COST = 10.0
WARM = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SEEDS = [11, 12, 13, 14, 15]
TAPES = ["X_PERM", "X_ROT"]
NS = [5, 10, 20, 40]
GROSSES = [0.60, 0.75, 1.00]
CADENCES = ["W", "M"]
COST_RUNGS = [0.0, 10.0, 25.0, 50.0]
OUTCOME_SETS = ["O_CSTAR", "O_MARGIN", "O_BINDING", "O_SHARE"]
REPAIRS = ["R_NONE", "R_DEGATE", "R_MATCH", "R_SOFT", "R_REFUSE"]
pd.set_option("display.width", 200)


# ----------------------------------------------------------------- fast runner
def run(px_vals, W_vals, mask, freq_turn_only=False):
    """Exact numpy replica of engine.backtest at cost 0, returning (r0, turnover).
    Cost enters only as -turnover*bps/1e4, so every cost rung is analytic from here."""
    R = px_vals
    n, k = R.shape
    held = np.zeros((n, k)); turn = np.zeros(n); cur = np.zeros(k)
    for i in range(n):
        if mask[i] or i == 0:
            new = W_vals[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        g = cur * (1.0 + R[i]); tot = g.sum() + (1.0 - cur.sum())
        if tot > 0: cur = g / tot
    return (held * R).sum(axis=1), turn


def prep(px, freq):
    R = px.pct_change().fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    return R, mask


def book(px, W, freq):
    R, mask = prep(px, freq)
    Wv = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    r0, turn = run(R, Wv, mask)
    return pd.Series(r0, index=px.index), pd.Series(turn, index=px.index)


def met(r0, turn, bps=COST):
    r = r0 - turn * bps / 1e4
    eq = (1 + r).cumprod(); yrs = len(r) / 252.0
    dd = (eq / np.maximum.accumulate(eq) - 1).min()
    vol = r.std() * np.sqrt(252)
    return dict(CAGR=eq[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan,
                Sharpe=(r.mean() * 252) / vol if vol else np.nan, MaxDD=dd,
                Turn=turn.sum() / yrs)


def sharpe_at(r0, turn, bps):
    r = r0 - turn * bps / 1e4
    v = r.std() * np.sqrt(252)
    return (r.mean() * 252) / v if v else np.nan


# ----------------------------------------------------------------- book family
def weights_from_rank(rank, n, gross):
    return (rank <= n).astype(float) * (gross / n)


MAX_VOL = 0.60


def rank_of(px):
    """Top-n eligibility rank of the 2026-09-04 KEEP-4b family: composite momentum,
    NO vol scaler, 200d-MA eligibility AND the vol20 < 0.60 filter (gate G9 shows this
    is the family whose n=20 / gross=0.75 / W cell reproduces the record's committed
    CAND20 MaxDD exactly)."""
    sc, above, vol20 = score(px, vol_scale=False)
    return sc.where(above & (vol20 < MAX_VOL)).rank(axis=1, ascending=False)


# ----------------------------------------------------------------- 4b / 4a
LEGS = ["H1", "H2", "OOS", "MaxDD", "CAGR"]


def legs_4b(b, bench):
    """PROTOCOL 4b: Sharpe > bench in BOTH halves AND OOS, MaxDD <= 60% of bench's,
    CAGR >= 70% of bench's.  Returns per-leg slack (positive = clears)."""
    return {
        "H1": b["H1"] - bench["H1"],
        "H2": b["H2"] - bench["H2"],
        "OOS": b["OOS_Sharpe"] - bench["OOS_Sharpe"],
        "MaxDD": 0.60 * abs(bench["MaxDD"]) - abs(b["MaxDD"]),
        "CAGR": b["CAGR"] - 0.70 * bench["CAGR"],
    }


def pass_4b(b, bench):
    s = legs_4b(b, bench)
    return all(v > 0 for v in s.values()), s


def pass_4a(b, live):
    return (b["H1"] > live["H1"] and b["H2"] > live["H2"]
            and b["MaxDD"] >= live["MaxDD"])


# ----------------------------------------------------------------- the tapes
def tape(px, kind, seed, bench_col="SPY"):
    """A CONTROLLED (exchangeable) tape.  Constituents only; the benchmark column is
    carried through untouched so 4b can still be scored the record's way (R_NONE).

    Listing dates are respected: a name's NaN prefix is preserved exactly, and only its
    OBSERVABLE returns (priced today AND yesterday) are resampled, so the tape has the
    same panel shape as the real one and no fabricated pre-listing history.

    X_PERM: per-day permutation of the cross-section among the names observable that
            day.  Preserves each day's observable-return multiset EXACTLY (so the
            panel-EW return path is bit-identical, gate G4) and therefore the market
            factor, while destroying every name's identity and all selection.
    X_ROT:  per-name independent circular rotation of that name's own observable return
            series.  Preserves each name's serial structure and marginal distribution
            EXACTLY (gate G5), destroys cross-sectional alignment (the record's RANDROT).
    """
    cols = [c for c in px.columns if c != bench_col]
    X = px[cols]
    VP = X.notna().values                       # priced
    VR = VP & np.vstack([np.zeros((1, VP.shape[1]), bool), VP[:-1]])   # return observable
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
        seg = P[v, j].copy(); seg[0] = 0.0      # first priced day carries no return
        out[v, j] = X.values[v[0], j] * np.cumprod(1.0 + seg)
    D = pd.DataFrame(out, index=px.index, columns=cols)
    if bench_col in px.columns:
        D[bench_col] = px[bench_col].values
    return D[list(px.columns)]


# ----------------------------------------------------------------- panels
def panels():
    P = {}
    P["U56"] = load_universe()
    P["B136"] = load_universe(broad=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    drop = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    s = load_universe(small=True)
    P["SMALL"] = s.drop(columns=[c for c in s.columns if c in drop])
    return P, sorted(drop)


# ================================================================== GATES
def gates(P, dropped):
    print("\n" + "=" * 100)
    print("GATES  (printed before any hypothesis is read)")
    print("=" * 100)
    G = []
    px = P["U56"]
    W = rules_v2_weights(px)
    for freq in ("W", "M"):
        r0, tn = book(px, W, freq)
        e = engine_backtest(px, W, cost_bps=COST, freq=freq)
        st = px.index[WARM]
        dr = float(np.abs((r0 - tn * COST / 1e4).loc[st:] - e["returns"].loc[st:]).max())
        dt = float(np.abs(tn.loc[st:] - e["turnover"].loc[st:]).max())
        G.append(("G1_" + freq, dr < 1e-12 and dt < 1e-9,
                  f"fast runner == engine.backtest  dret {dr:.3e} dturn {dt:.3e}"))

    st = px.index[WARM]
    r0, tn = book(px, rules_v2_weights(px), "W")
    m = met(r0.loc[st:].values, tn.loc[st:].values)
    anchor = dict(CAGR=0.0860, Sharpe=1.1980, MaxDD=-0.1205)
    ok = (abs(m["CAGR"] - anchor["CAGR"]) < 5e-4 and abs(m["Sharpe"] - anchor["Sharpe"]) < 3e-3
          and abs(m["MaxDD"] - anchor["MaxDD"]) < 5e-4)
    G.append(("G2_LIVE", ok, f"RULES v2 live {m['CAGR']:.2%}/{m['Sharpe']:.4f}/{m['MaxDD']:.2%} "
                             f"vs committed 8.60%/1.1980/-12.05%"))
    spy = px["SPY"].pct_change().fillna(0.0).loc[st:].values
    ms = met(spy, np.zeros(len(spy)))
    ok = abs(ms["CAGR"] - 0.1506) < 5e-4 and abs(ms["Sharpe"] - 0.8814) < 3e-3
    G.append(("G3_SPY", ok, f"SPY {ms['CAGR']:.2%}/{ms['Sharpe']:.4f}/{ms['MaxDD']:.2%} "
                            f"vs committed 15.06%/0.8814/-33.72%"))

    # G4 the tape really is exchangeable: X_PERM preserves the daily cross-section exactly
    t1 = tape(px, "X_PERM", 11)
    cols = [c for c in px.columns if c != "SPY"]
    a = px[cols].pct_change().fillna(0.0).values
    b = t1[cols].pct_change().fillna(0.0).values
    dew = float(np.abs(a.mean(1) - b.mean(1)).max())
    dsort = float(np.abs(np.sort(a, axis=1) - np.sort(b, axis=1)).max())
    dmask = int((px[cols].notna().values != t1[cols].notna().values).sum())
    G.append(("G4_PERM", dew < 1e-14 and dsort < 1e-14 and dmask == 0,
              f"X_PERM preserves daily EW return ({dew:.3e}), the daily cross-sectional "
              f"multiset ({dsort:.3e}) and the listing mask ({dmask} cells differ)"))

    # G5 X_ROT preserves each name's own marginal distribution exactly
    t2 = tape(px, "X_ROT", 11)
    c2 = t2[cols].pct_change().fillna(0.0).values
    dmar = float(np.abs(np.sort(a, axis=0) - np.sort(c2, axis=0)).max())
    dmask2 = int((px[cols].notna().values != t2[cols].notna().values).sum())
    G.append(("G5_ROT", dmar < 1e-12 and dmask2 == 0,
              f"X_ROT preserves every name's own return multiset ({dmar:.3e}) and the "
              f"listing mask ({dmask2} cells differ)"))

    # G6 determinism
    t3 = tape(px, "X_PERM", 11)
    dd = float(np.nanmax(np.abs(t1.values - t3.values)))
    G.append(("G6_DET", dd == 0.0, f"same seed -> identical tape ({dd:.3e})"))

    # G7 analytic cost ladder == re-running at that cost
    rk = rank_of(px)
    r0, tn = book(px, weights_from_rank(rk, 20, 0.75), "W")
    e50 = engine_backtest(px, weights_from_rank(rk, 20, 0.75), cost_bps=50.0, freq="W")
    d50 = float(np.abs((r0 - tn * 50.0 / 1e4).loc[st:] - e50["returns"].loc[st:]).max())
    G.append(("G7_COST", d50 < 1e-12, f"analytic cost rung == engine at 50 bps ({d50:.3e})"))

    # G8 c* bisection == brute-force grid to < 0.05 bps
    stv = px.index.get_loc(st)
    r0v, tnv = r0.values[stv:], tn.values[stv:]
    sb = met(spy, np.zeros(len(spy)))["Sharpe"]
    cb = cstar(r0v, tnv, sb)
    grid = np.arange(0.0, 400.0, 0.05)
    sh = np.array([sharpe_at(r0v, tnv, c) for c in grid])
    below = np.where(sh < sb)[0]
    cg = grid[below[0]] if len(below) else np.nan
    G.append(("G8_CSTAR", (np.isnan(cb) and np.isnan(cg)) or abs(cb - cg) < 0.06,
              f"c* bisection {cb:.3f} bps == brute force {cg:.3f} bps"))

    # G9 the 2026-09-04 KEEP-4b candidate reproduces (top-20 EW, no vol scaler, gross .75).
    # The record commits TWO different Sharpes for this same book (931's G3 1.0596 and
    # 933's G3 1.0921, a 0.0325 spread it flagged itself), so the gate is on MaxDD and
    # CAGR and on the Sharpe landing INSIDE the record's own two committed values.
    m20 = met(r0.values[stv:], tn.values[stv:])
    ok = (abs(m20["MaxDD"] - (-0.1831)) < 5e-4 and abs(m20["CAGR"] - 0.1266) < 5e-3
          and 1.0596 <= m20["Sharpe"] <= 1.0921)
    G.append(("G9_CAND", ok,
              f"CAND20 U56/W/gross0.75 {m20['CAGR']:.2%}/{m20['Sharpe']:.4f}/{m20['MaxDD']:.2%} "
              f"vs committed 12.66-12.73%/1.0596-1.0921/-18.31%"))

    G.append(("G10_DROP", len(dropped) == 52 and P["SMALL"].shape[1] == 664,
              f"SMALL panel {P['SMALL'].shape[1]} columns after dropping {len(dropped)} "
              f"tickers with max_1d_move >= 1.0"))

    for k, ok, msg in G:
        print(f"  {k:10s} {'PASS' if ok else 'FAIL'}  {msg}")
    print(f"  ---> {sum(1 for _, o, _ in G if o)} of {len(G)} gates PASS")
    return G


def cstar(r0, turn, bench_sharpe, lo=0.0, hi=1000.0):
    """Breakeven cost: the bps rung at which the book's Sharpe falls to the benchmark's.
    NaN when the book is already below the benchmark at 0 bps (the DEGENERATE case)."""
    if not np.isfinite(bench_sharpe): return np.nan
    if sharpe_at(r0, turn, lo) <= bench_sharpe: return np.nan
    if sharpe_at(r0, turn, hi) > bench_sharpe: return np.inf
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if sharpe_at(r0, turn, mid) > bench_sharpe: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)


# ================================================================== PART A census
GATE_TOKENS = ("pass4b", "fail4b", "p4b", "is4b", "pass_4b", "4b_pass", "passes4b")
OUTCOME_TOKENS = {
    "O_CSTAR": ("cstar", "c_star", "cbreak", "breakeven", "c*"),
    "O_MARGIN": ("margin", "slack", "dsharpe", "excess"),
    "O_BINDING": ("binding", "leg", "which_leg", "failleg"),
    "O_SHARE": ("share", "frac", "pct", "rate", "count"),
}
PROSE_RESTRICT = ("among the passes", "of the passes", "among passes", "among the 4b",
                  "among 4b", "of 4b passes", "passers", "conditional on 4b",
                  "among the passers", "of the passers", "restricted to passes",
                  "among the 4b passes")


def census():
    print("\n" + "=" * 100)
    print("PART A — THE CENSUS: how much of the committed outcome layer has the 4b-PASSING")
    print("         SET as its DOMAIN?  Two layers are scanned separately.")
    print("=" * 100)
    rows = []
    files = sorted(glob.glob(str(OUT / "*.csv")))
    n_gate_files = 0
    for f in files:
        try:
            df = pd.read_csv(f, nrows=4000, low_memory=False)
        except Exception:
            continue
        cols = {c.lower().strip(): c for c in df.columns}
        gate = next((cols[t] for t in GATE_TOKENS if t in cols), None)
        if gate is None:
            continue
        g = df[gate]
        if g.dtype == object:
            g = g.astype(str).str.strip().str.lower().isin(("true", "1", "yes", "pass"))
        gb = g.fillna(False).astype(bool)
        if gate.lower().startswith("fail"):
            gb = ~gb
        if gb.sum() == 0 or gb.all():
            pass_only_possible = False
        else:
            pass_only_possible = True
        n_gate_files += 1
        for c in df.columns:
            if c == gate: continue
            s = df[c]
            defined = s.notna() & (s.astype(str).str.strip() != "")
            if defined.sum() == 0: continue
            # 4b-CONDITIONAL (machine layer): the column is defined ONLY on pass rows,
            # and there is at least one fail row it declines to take a value on.
            cond = bool(pass_only_possible and defined[~gb].sum() == 0 and defined[gb].sum() > 0)
            oset = None
            lc = c.lower()
            for k, toks in OUTCOME_TOKENS.items():
                if any(t in lc for t in toks): oset = k; break
            rows.append(dict(file=os.path.basename(f), col=c, n=len(df),
                             n_pass=int(gb.sum()), n_defined=int(defined.sum()),
                             defined_on_fail=int(defined[~gb].sum()),
                             cond4b=cond, outcome_set=oset))
    A = pd.DataFrame(rows)
    A.to_csv(OUT / f"{SLUG}.A_machine_census.csv", index=False)
    print(f"  MACHINE LAYER: {len(files)} committed CSVs scanned, {n_gate_files} carry a 4b gate "
          f"column, {len(A)} (file, column) cells examined.")
    if len(A):
        print(f"    4b-CONDITIONAL (defined ONLY on pass rows): {int(A.cond4b.sum())} "
              f"({A.cond4b.mean():.4f} of examined cells) in "
              f"{A.loc[A.cond4b, 'file'].nunique()} files")
        by = A[A.cond4b].groupby(A.outcome_set.fillna("O_OTHER")).size().sort_values(ascending=False)
        for k, v in by.items(): print(f"      {k:10s} {v}")

    # reader layer
    prose = []
    for f in sorted(glob.glob(str(OUT / "*.md"))) + [str(ROOT / "research" / "LEADERBOARD.md"),
                                                     str(ROOT / "research" / "CHANGELOG.md")]:
        try: txt = Path(f).read_text(errors="ignore")
        except Exception: continue
        for sent in re.split(r"(?<=[.;])\s+|\n", txt):
            s = sent.strip()
            if len(s) < 20 or len(s) > 1200: continue
            ls = s.lower()
            if not any(t in ls for t in PROSE_RESTRICT): continue
            oset = None
            for k, toks in OUTCOME_TOKENS.items():
                if any(t in ls for t in toks): oset = k; break
            has_num = bool(re.search(r"\d", s))
            prose.append(dict(file=os.path.basename(f), outcome_set=oset or "O_OTHER",
                              has_number=has_num, sentence=s[:400]))
    B = pd.DataFrame(prose)
    B.to_csv(OUT / f"{SLUG}.A_prose_census.csv", index=False)
    print(f"  READER LAYER: {len(B)} committed sentences restrict an outcome to the 4b-passing "
          f"set, in {B.file.nunique() if len(B) else 0} files; "
          f"{int(B.has_number.sum()) if len(B) else 0} of them quote a number.")
    if len(B):
        for k, v in B.groupby("outcome_set").size().sort_values(ascending=False).items():
            print(f"      {k:10s} {v}")
    return A, B


# ================================================================== PART B grid
def build_books(px, label, tape_kind, seed):
    """Every book of the KEEP-4b family on this tape.  Returns a list of dicts carrying
    the cost-0 return path and turnover so every cost rung and every c* is analytic."""
    rk = rank_of(px)
    st = px.index[WARM]
    out = []
    for freq in CADENCES:
        R, mask = prep(px, freq)
        for n in NS:
            base = (rk <= n).astype(float).reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
            for g in GROSSES:
                r0, tn = run(R, base * (g / n), mask)
                out.append(dict(panel=label, tape=tape_kind, seed=seed, cadence=freq,
                                n=n, gross=g, r0=pd.Series(r0, index=px.index),
                                turn=pd.Series(tn, index=px.index)))
    return out, st


def score_books(books, px, st):
    """Full / half / OOS metrics at 10 bps for a set of books plus the three benchmarks
    they may be judged against: real SPY, the tape's own SPY-equivalent (panel EW
    buy-and-hold on THIS tape), and the tape's own median book."""
    idx = px.index
    i0 = idx.get_loc(st)
    h = (len(idx) - i0) // 2
    oi = idx.get_indexer([pd.Timestamp(OOS_START)], method="bfill")[0]

    def slice_metrics(r0, tn):
        a0, a1 = r0.values[i0:], tn.values[i0:]
        full = met(a0, a1)
        h1 = met(a0[:h], a1[:h]); h2 = met(a0[h:], a1[h:])
        o0, o1 = r0.values[oi:], tn.values[oi:]
        oo = met(o0, o1)
        i_0, i_1 = r0.values[i0:oi], tn.values[i0:oi]
        iss = met(i_0, i_1)
        return dict(CAGR=full["CAGR"], Sharpe=full["Sharpe"], MaxDD=full["MaxDD"],
                    Turn=full["Turn"], H1=h1["Sharpe"], H2=h2["Sharpe"],
                    OOS_CAGR=oo["CAGR"], OOS_Sharpe=oo["Sharpe"], OOS_MaxDD=oo["MaxDD"],
                    IS_CAGR=iss["CAGR"], IS_Sharpe=iss["Sharpe"], IS_MaxDD=iss["MaxDD"])

    recs = []
    for b in books:
        m = slice_metrics(b["r0"], b["turn"])
        m.update({k: b[k] for k in ("panel", "tape", "seed", "cadence", "n", "gross")})
        m["_r0"] = b["r0"].values[i0:]; m["_tn"] = b["turn"].values[i0:]
        m["_r0o"] = b["r0"].values[oi:]; m["_tno"] = b["turn"].values[oi:]
        recs.append(m)

    # benchmarks
    spy = px["SPY"].pct_change().fillna(0.0)
    z = pd.Series(0.0, index=idx)
    B_SPY = slice_metrics(spy, z)
    cols = [c for c in px.columns if c != "SPY"]
    ew = px[cols].pct_change().fillna(0.0).mean(axis=1)
    B_EW = slice_metrics(ew, z)
    return recs, B_SPY, B_EW


# ================================================================== main
def main():
    t_all = time.time()
    P, dropped = panels()
    for k, v in P.items():
        print(f"panel {k:6s} {v.shape[0]} days x {v.shape[1]} cols  "
              f"{v.index[0].date()} -> {v.index[-1].date()}")
    G = gates(P, dropped)
    A_mach, A_prose = census()

    print("\n" + "=" * 100)
    print("PART B — THE ANSWER: is a 4b-CONDITIONAL outcome DEFINED on a controlled tape?")
    print("=" * 100)
    allrecs = []
    bench = {}
    for pname, px in P.items():
        cells = [("REAL", 0)] + [(t, s) for t in TAPES for s in SEEDS]
        for tk, sd in cells:
            tpx = px if tk == "REAL" else tape(px, tk, sd)
            bks, st = build_books(tpx, pname, tk, sd)
            recs, B_SPY, B_EW = score_books(bks, tpx, st)
            bench[(pname, tk, sd)] = dict(SPY=B_SPY, EW=B_EW)
            allrecs += recs
        print(f"  {pname}: {len(cells)} tape cells x {len(NS)*len(GROSSES)*len(CADENCES)} books "
              f"= {len(cells)*len(NS)*len(GROSSES)*len(CADENCES)} book runs  "
              f"[{time.time()-t_all:.0f}s]")

    # the tape's own MEDIAN book, per (panel, tape) -- the R_SOFT benchmark
    D = pd.DataFrame([{k: v for k, v in r.items() if not k.startswith("_")} for r in allrecs])
    soft = {}
    for (pn, tk), grp in D[D.tape != "REAL"].groupby(["panel", "tape"]):
        soft[(pn, tk)] = {c: float(grp[c].median()) for c in
                          ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD")}
    for pn in P:                                  # real panel judged against the pooled control
        med = [soft[(pn, t)] for t in TAPES]
        soft[(pn, "REAL")] = {c: float(np.median([m[c] for m in med])) for c in med[0]}

    def bench_for(rec, repair):
        key = (rec["panel"], rec["tape"], rec["seed"])
        if repair in ("R_NONE", "R_DEGATE", "R_REFUSE"):
            return bench[key]["SPY"]
        if repair == "R_MATCH":
            return bench[key]["EW"]
        if repair == "R_SOFT":
            return soft[(rec["panel"], rec["tape"])]
        raise ValueError(repair)

    # ---- outcome definedness under every (outcome set, repair) point
    prows = []
    for rec in allrecs:
        for rep in REPAIRS:
            bch = bench_for(rec, rep) if rep != "R_REFUSE" else bench_for(rec, "R_NONE")
            p4b, slack = pass_4b(rec, bch)
            gated = (rep != "R_DEGATE")          # R_DEGATE drops the 4b gate on the DOMAIN
            if rep == "R_REFUSE":
                defined = {o: (rec["tape"] == "REAL") for o in OUTCOME_SETS}
            else:
                dom = p4b or not gated
                cs = cstar(rec["_r0"], rec["_tn"], bch["Sharpe"])
                defined = {
                    "O_CSTAR": bool(dom and np.isfinite(cs)),
                    "O_MARGIN": bool(dom),
                    "O_BINDING": bool(dom),
                    "O_SHARE": bool(p4b or not gated),
                }
            cs = cstar(rec["_r0"], rec["_tn"], bch["Sharpe"])
            bleg = min(slack, key=slack.get)
            prows.append(dict(panel=rec["panel"], tape=rec["tape"], seed=rec["seed"],
                              cadence=rec["cadence"], n=rec["n"], gross=rec["gross"],
                              repair=rep, pass4b=p4b, cstar=cs, margin=rec["Sharpe"] - bch["Sharpe"],
                              binding_leg=bleg, min_slack=slack[bleg],
                              Sharpe=rec["Sharpe"], CAGR=rec["CAGR"], MaxDD=rec["MaxDD"],
                              Turn=rec["Turn"], OOS_Sharpe=rec["OOS_Sharpe"],
                              **{f"def_{o}": defined[o] for o in OUTCOME_SETS}))
    B = pd.DataFrame(prows)
    B.to_csv(OUT / f"{SLUG}.B_definedness.csv", index=False)

    print("\n  B1. 4b PASS RATE on the REAL panel vs the CONTROLLED tapes, by repair")
    print("      (R_NONE is the record's own convention: judged against the REAL SPY)")
    pv = B.pivot_table(index=["repair", "panel"], columns="tape", values="pass4b", aggfunc="mean")
    print(pv.to_string(float_format=lambda x: f"{x:.3f}"))

    print("\n  B1b. MECHANISM: what each tape does to the panel, and what that does to the book.")
    print("       (mean off-diagonal daily-return correlation, one seed per panel; and the")
    print("        MEDIAN book Sharpe / MaxDD over all 24 books on that tape)")
    mrows = []
    for pn, px in P.items():
        cols = [c for c in px.columns if c != "SPY"]
        for tk in ["REAL"] + TAPES:
            tpx = px if tk == "REAL" else tape(px, tk, SEEDS[0])
            cm = tpx[cols].pct_change().iloc[WARM:].corr().values
            iu = np.triu_indices_from(cm, k=1)
            rbar = float(np.nanmean(cm[iu]))
            sub = B[(B.panel == pn) & (B.tape == tk) & (B.repair == "R_NONE")]
            mrows.append(dict(panel=pn, tape=tk, mean_pair_corr=rbar,
                              med_book_Sharpe=sub.Sharpe.median(),
                              med_book_MaxDD=sub.MaxDD.median(),
                              med_book_CAGR=sub.CAGR.median(),
                              pass4b=sub.pass4b.mean()))
    M = pd.DataFrame(mrows)
    M.to_csv(OUT / f"{SLUG}.B_mechanism.csv", index=False)
    print(M.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n  B2. DEFINEDNESS of each OUTCOME SET on the CONTROLLED tapes (all 20 grid points)")
    T = B[B.tape != "REAL"]
    grid = T.groupby("repair")[[f"def_{o}" for o in OUTCOME_SETS]].mean()
    grid.columns = OUTCOME_SETS
    print(grid.to_string(float_format=lambda x: f"{x:.3f}"))
    print("\n      same, on the REAL panel (the record's own domain):")
    Rr = B[B.tape == "REAL"].groupby("repair")[[f"def_{o}" for o in OUTCOME_SETS]].mean()
    Rr.columns = OUTCOME_SETS
    print(Rr.to_string(float_format=lambda x: f"{x:.3f}"))

    # ---- does the repair PRESERVE the record's real-panel reading?
    print("\n  B3. FIDELITY: does the repair reproduce the record's real-panel turnover->c* "
          "relation?\n      (1094 committed -0.65; 1151 -0.6484; 1171 reproduced -0.6154 on U56)")
    frows = []
    for rep in REPAIRS:
        for pn in P:
            sub = B[(B.repair == rep) & (B.panel == pn) & (B.tape == "REAL")]
            dom = sub if rep == "R_DEGATE" else sub[sub.pass4b]
            d = dom.dropna(subset=["cstar"])
            d = d[np.isfinite(d.cstar)]
            rho = d[["Turn", "cstar"]].corr().iloc[0, 1] if len(d) > 2 else np.nan
            frows.append(dict(repair=rep, panel=pn, n_domain=len(d), rho_turn_cstar=rho,
                              median_cstar=d.cstar.median() if len(d) else np.nan))
    F = pd.DataFrame(frows)
    F.to_csv(OUT / f"{SLUG}.B_fidelity.csv", index=False)
    print(F.pivot_table(index="repair", columns="panel",
                        values=["n_domain", "rho_turn_cstar"]).to_string(float_format=lambda x: f"{x:.3f}"))

    # ---- what does each repair COST
    print("\n  B4. PRICE of each repair (extra tape draws needed beyond the record's own run)")
    ndraw = len(TAPES) * len(SEEDS) * len(NS) * len(GROSSES) * len(CADENCES) * len(P)
    price = {"R_NONE": 0, "R_DEGATE": 0, "R_MATCH": 0, "R_SOFT": ndraw, "R_REFUSE": -ndraw}
    for r in REPAIRS:
        print(f"      {r:10s} extra book runs {price[r]:+6d}   "
              f"{'(re-uses the draws already made)' if price[r]==0 else ''}"
              f"{'(needs the control distribution itself)' if price[r]>0 else ''}"
              f"{'(refuses the control: saves every draw, buys no resolution)' if price[r]<0 else ''}")

    # ================================================================ PART C
    print("\n" + "=" * 100)
    print("PART C — RULE 8 WALK-FORWARD + BOTH KEEP PATHS (real panels only, 10 bps)")
    print("         IS 2009-2016 chooses; OOS 2017-2026 read once.")
    print("=" * 100)
    live = {}
    for pn, px in P.items():
        r0, tn = book(px, rules_v2_weights(px), "W")
        st = px.index[WARM]
        recs, _, _ = score_books([dict(panel=pn, tape="REAL", seed=0, cadence="W", n=0,
                                       gross=0.75, r0=r0, turn=tn)], px, st)
        live[pn] = recs[0]
    real = [r for r in allrecs if r["tape"] == "REAL"]
    crows = []
    for rec in real:
        bspy = bench[(rec["panel"], "REAL", 0)]["SPY"]
        bew = bench[(rec["panel"], "REAL", 0)]["EW"]
        p4b, slack = pass_4b(rec, bspy)
        p4b_oos = (rec["OOS_Sharpe"] > bspy["OOS_Sharpe"]
                   and abs(rec["OOS_MaxDD"]) <= 0.60 * abs(bspy["OOS_MaxDD"])
                   and rec["OOS_CAGR"] >= 0.70 * bspy["OOS_CAGR"])
        p4a = pass_4a(rec, live[rec["panel"]])
        crows.append(dict(panel=rec["panel"], cadence=rec["cadence"], n=rec["n"],
                          gross=rec["gross"], CAGR=rec["CAGR"], Sharpe=rec["Sharpe"],
                          MaxDD=rec["MaxDD"], H1=rec["H1"], H2=rec["H2"],
                          IS_Sharpe=rec["IS_Sharpe"], OOS_CAGR=rec["OOS_CAGR"],
                          OOS_Sharpe=rec["OOS_Sharpe"], OOS_MaxDD=rec["OOS_MaxDD"],
                          Turn=rec["Turn"], pass4b=p4b, pass4b_oos=p4b_oos, pass4a=p4a,
                          IS_cstar=cstar(rec["_r0"][:len(rec["_r0"]) - len(rec["_r0o"])],
                                         rec["_tn"][:len(rec["_tn"]) - len(rec["_tno"])],
                                         bspy["IS_Sharpe"]),
                          IS_pass4b_SPY=all(v > 0 for v in legs_4b(rec, bspy).values()),
                          IS_pass4b_EW=all(v > 0 for v in legs_4b(rec, bew).values())))
    C = pd.DataFrame(crows)
    C.to_csv(OUT / f"{SLUG}.C_books.csv", index=False)
    print(f"\n  {len(C)} real books, ALL published to {SLUG}.C_books.csv")
    print(f"  base rates: 4b full {int(C.pass4b.sum())} of {len(C)}, "
          f"4b OOS {int(C.pass4b_oos.sum())} of {len(C)}, 4a {int(C.pass4a.sum())} of {len(C)}")
    print("\n  ALL GRID POINTS (real panels):")
    print(C[["panel", "cadence", "n", "gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
             "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "Turn", "pass4b", "pass4b_oos", "pass4a"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # choosers, IS only
    print("\n  CHOOSERS (IS 2009-2016 only; OOS read once). CH_GATED and CH_MATCH are the")
    print("  4b-CONDITIONAL selection devices; CH_CSTAR is the DE-GATED outcome as a device.")
    prows = []
    for pn, grp in C.groupby("panel"):
        bspy = bench[(pn, "REAL", 0)]["SPY"]
        picks = {}
        picks["CH_ISSHARPE"] = grp.loc[grp.IS_Sharpe.idxmax()]
        g1 = grp[grp.IS_pass4b_SPY]
        picks["CH_GATED"] = (g1.loc[g1.IS_Sharpe.idxmax()] if len(g1)
                             else grp.loc[grp.IS_Sharpe.idxmax()])
        g2 = grp[grp.IS_pass4b_EW]
        picks["CH_MATCH"] = (g2.loc[g2.IS_Sharpe.idxmax()] if len(g2)
                             else grp.loc[grp.IS_Sharpe.idxmax()])
        cc = grp[np.isfinite(grp.IS_cstar)]
        picks["CH_CSTAR"] = (cc.loc[cc.IS_cstar.idxmax()] if len(cc)
                             else grp.loc[grp.IS_Sharpe.idxmax()])
        for ch, row in picks.items():
            prows.append(dict(panel=pn, chooser=ch, cadence=row.cadence, n=int(row.n),
                              gross=row.gross, n_eligible=(len(g1) if ch == "CH_GATED"
                                                           else len(g2) if ch == "CH_MATCH"
                                                           else len(cc) if ch == "CH_CSTAR" else len(grp)),
                              OOS_CAGR=row.OOS_CAGR, OOS_Sharpe=row.OOS_Sharpe,
                              OOS_MaxDD=row.OOS_MaxDD, full_CAGR=row.CAGR, full_Sharpe=row.Sharpe,
                              full_MaxDD=row.MaxDD, H1=row.H1, H2=row.H2,
                              pass4b=bool(row.pass4b), pass4b_oos=bool(row.pass4b_oos),
                              pass4a=bool(row.pass4a),
                              spy_OOS_Sharpe=bspy["OOS_Sharpe"], spy_OOS_CAGR=bspy["OOS_CAGR"],
                              spy_OOS_MaxDD=bspy["OOS_MaxDD"]))
    PK = pd.DataFrame(prows)
    PK.to_csv(OUT / f"{SLUG}.C_picks.csv", index=False)
    print(PK.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print(f"\n  picks: 4b full {int(PK.pass4b.sum())} of {len(PK)}, "
          f"4b OOS {int(PK.pass4b_oos.sum())} of {len(PK)}, 4a {int(PK.pass4a.sum())} of {len(PK)}")
    same = PK.pivot_table(index="panel", columns="chooser",
                          values=["n", "gross"], aggfunc="first")
    print("\n  does the 4b GATE change the pick?  (cell = the chosen (n, gross))")
    print(same.to_string())
    base = PK[PK.chooser == "CH_ISSHARPE"].set_index("panel")
    for ch in ("CH_GATED", "CH_MATCH", "CH_CSTAR"):
        sub = PK[PK.chooser == ch].set_index("panel")
        d = (sub.OOS_Sharpe - base.OOS_Sharpe)
        moved = int(((sub.n != base.n) | (sub.gross != base.gross) |
                     (sub.cadence != base.cadence)).sum())
        print(f"    {ch:12s} pick moves at {moved} of {len(sub)} panels; "
              f"mean OOS Sharpe change {d.mean():+.4f} (min {d.min():+.4f}, max {d.max():+.4f})")

    print("\n  BENCHMARKS on the real panels (post-warm-up, 10 bps where applicable):")
    for pn in P:
        b = bench[(pn, "REAL", 0)]["SPY"]; e = bench[(pn, "REAL", 0)]["EW"]; l = live[pn]
        print(f"    {pn:6s} SPY full {b['CAGR']:.2%}/{b['Sharpe']:.4f}/{b['MaxDD']:.2%} "
              f"OOS {b['OOS_CAGR']:.2%}/{b['OOS_Sharpe']:.4f}/{b['OOS_MaxDD']:.2%} | "
              f"panelEW full {e['CAGR']:.2%}/{e['Sharpe']:.4f}/{e['MaxDD']:.2%} | "
              f"LIVE v2 full {l['CAGR']:.2%}/{l['Sharpe']:.4f}/{l['MaxDD']:.2%} "
              f"OOS {l['OOS_CAGR']:.2%}/{l['OOS_Sharpe']:.4f}/{l['OOS_MaxDD']:.2%}")

    best = C[C.pass4b & C.pass4b_oos]
    if len(best):
        b = best.loc[best.OOS_Sharpe.idxmax()]
        print(f"\n  BEST 4b book (full AND OOS): {b.panel}/{b.cadence}/n={int(b.n)}/gross={b.gross} "
              f"full {b.CAGR:.2%}/{b.Sharpe:.4f}/{b.MaxDD:.2%} (H1 {b.H1:.3f}/H2 {b.H2:.3f}) "
              f"OOS {b.OOS_CAGR:.2%}/{b.OOS_Sharpe:.4f}/{b.OOS_MaxDD:.2%}")
        reach = PK[(PK.panel == b.panel) & (PK.n == b.n) & (PK.gross == b.gross)
                   & (PK.cadence == b.cadence)]
        print(f"  IS-chooser-reachable: {'YES via ' + ', '.join(reach.chooser) if len(reach) else 'NO'}")
    else:
        print("\n  BEST 4b book (full AND OOS): NONE")

    print(f"\n  total runtime {time.time()-t_all:.0f}s")
    print("  NOTHING ENACTED. RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py untouched.")


if __name__ == "__main__":
    main()
