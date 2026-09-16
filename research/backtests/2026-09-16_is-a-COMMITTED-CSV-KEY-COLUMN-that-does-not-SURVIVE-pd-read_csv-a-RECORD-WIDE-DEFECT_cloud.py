#!/usr/bin/env python3
"""QUEUE 1105 — is a COMMITTED CSV KEY COLUMN that does not SURVIVE pd.read_csv a RECORD-WIDE
DEFECT?

PREMISE (idea 1097, committed 2026-09-16).  1071's `cap` column is a STRING KEY ("INF", "1.00",
...) that enters its md5 null-seed recipe VERBATIM:

    sd = mdseed(panel, N, capname, s)

`pd.read_csv` with default dtype infers that column to float64, so "INF" comes back as `inf`
and "1.00" as `1.0`.  `str()` of those is "inf" and "1.0" — DIFFERENT seeds, DIFFERENT random
orderings, and therefore plausible wrong numbers rather than an error.  1097's first pass
reproduced 1071 at 8 of 40 cells because of exactly this.  1105 asks whether the record has
more of these, and prices what a re-read gets wrong.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4)
  D1  COLUMN CLASS  {SEED_KEY, ANY_KEY}
        SEED_KEY — a column whose NAME appears as a token in a committed md5 seed recipe
                   (`mdseed(...)` call sites harvested from the record's own scripts).  These
                   are the columns that, misread, draw DIFFERENT NULLS.
        ANY_KEY  — every column in every committed CSV.  The wider class measures how much of
                   the record's text is lossy, not just how much of its randomness is.
  D2  ROUND-TRIP TEST  {LITERAL, SEMANTIC}
        LITERAL  — `str(pd.read_csv(f)[col])` differs from the raw text, cell by cell.  This is
                   the test that matters for a SEED, because md5 sees the literal.
        SEMANTIC — the raw -> re-read map is NOT INJECTIVE within the column, i.e. two distinct
                   committed labels collide on one re-read value.  LITERAL damage can be undone
                   by a format rule; SEMANTIC damage cannot be undone at all.
  All 2 x 2 = 4 grid points are reported.  PANEL, N and the cap ladder in Part B are COORDINATE
  SETS taken from 1071 verbatim, not dials.

HYPOTHESES, DECLARED BEFORE ANY NUMBER
  H_WIDE      the defect is RECORD-WIDE: > 5% of committed CSVs carry at least one LITERAL
              round-trip failure in a SEED_KEY column.
  H_SEED      SEED_KEY columns fail LITERAL at a HIGHER rate than columns at large — the
              defect concentrates where it does damage.
  H_SEMANTIC  at least one SEED_KEY column is SEMANTICALLY lossy (a genuine collision), not
              merely reformatted.
  H_PRICE     re-reading 1071's `cap` column through the default dtype reproduces FEWER than
              half of its committed cells.
  H_CAPONLY   `cap` is the ONLY seed-key column class in the record that fails LITERAL (if it
              passes, 1097's incident is a one-off, not a record-wide defect).

GATES print before any result number.  RULE 8 walk-forward and both KEEP paths are run on the
capped books themselves.  RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py are NOT touched.

SURVIVORSHIP (rule 9): U56 and B136 are CURRENT-CONSTITUENT panels; every CAGR/Sharpe level is
optimistic and every 4a/4b count an UPPER bound.  The reproduction shares in Part B are
within-tape contrasts and the bias very largely cancels out of them.
"""
import hashlib
import io
import re
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.simplefilter("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, score  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

SLUG = ("2026-09-16_is-a-COMMITTED-CSV-KEY-COLUMN-that-does-not-SURVIVE-pd-read_csv-"
        "a-RECORD-WIDE-DEFECT_cloud")
OUT = ROOT / "research" / "backtests"
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def W(name, df):
    p = OUT / f"{SLUG}.{name}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ---------------------------------------------------------------- frozen construction
COST, GROSS, MAXVOL, FREQ, LAG, WARM = 10.0, 0.75, 0.60, "W", 1, 260
SEEDS = 20                                   # 1071's committed seed count
BISECT = 34
N_LADDER = [5, 10, 20]                       # 1071's coordinate set (subset priced here)
CAPS = [("INF", np.inf), ("2.00", 2.00), ("1.50", 1.50), ("1.00", 1.00)]   # 1071's, verbatim
H_HOLD = 126                                 # 1071's committed min hold
IS_END, OOS_START = "2016-12-31", "2017-01-01"


def mdseed(*parts):
    return int(hashlib.md5("|".join(str(x) for x in parts).encode()).hexdigest()[:8], 16)


# ================================================================= PART A — CENSUS
def harvest_seed_tokens():
    """Every identifier that appears inside a committed `mdseed(...)` call site.  These are the
    record's OWN declarations of which columns are keys."""
    toks = set()
    calls = 0
    for f in sorted(OUT.glob("*.py")):
        if f.stem == SLUG:
            continue
        src = f.read_text(errors="replace")
        for m in re.finditer(r"mdseed\(([^)]*)\)", src):
            body = m.group(1)
            if body.strip() == "*parts":
                continue
            calls += 1
            for t in re.findall(r"[A-Za-z_][A-Za-z_0-9]*", body):
                toks.add(t.lower())
    # the column-name forms the record actually writes for those tokens
    alias = {"capname": "cap", "nseed": "seeds", "pan": "panel", "pname": "panel"}
    toks |= {alias[t] for t in list(toks) if t in alias}
    # A seed recipe's SHORT locals (`s`, `t`, `k`, `n`, `p`, `c`, `f`, `r`, `l`) are loop
    # variables, NOT column names; left in, they match unrelated statistic columns (a t-stat,
    # a p-value, a count) and would inflate the SEED_KEY class with things no reader ever keys
    # on.  The class is therefore restricted to tokens of >= 3 characters.  This is part of the
    # D1 definition, declared here and not tuned afterwards.
    toks = {t for t in toks if len(t) >= 3}
    return toks, calls


def _mode(bp):
    """Classify HOW a column fails the literal round trip, on its failing pairs alone.
      FLOAT_REPR — both sides parse as the SAME float; only the printed digits moved
                   (17-sig-fig text vs pandas' 16-sig-fig repr).  Harmless to a VALUE,
                   fatal to a SEED, which hashes the literal.
      EMPTY_NAN  — committed '' comes back as the string 'nan'.
      KEY        — the raw literal is not a number at all, or is a number whose FORMAT
                   carries the key ('INF' -> 'inf', '1.00' -> '1.0').  This is 1071's defect.
    """
    def asf(x):
        try:
            return float(x)
        except Exception:
            return None
    kinds = set()
    for r, v in zip(bp.r.astype(str), bp.v.astype(str)):
        if r == "":
            kinds.add("EMPTY_NAN"); continue
        fr, fv = asf(r), asf(v)
        if fr is None or fv is None:
            kinds.add("KEY")
        elif fr == fv and r.rstrip("0").rstrip(".") != v.rstrip("0").rstrip("."):
            kinds.add("FLOAT_REPR")
        elif fr == fv:
            kinds.add("KEY")            # same value, different format: 'INF'->'inf', '1.00'->'1.0'
        else:
            kinds.add("FLOAT_REPR")
    for k in ("KEY", "EMPTY_NAN", "FLOAT_REPR"):
        if k in kinds:
            return k
    return "OTHER"


def census(seed_toks):
    P("\n" + "=" * 96)
    P("PART A — CENSUS of every committed CSV (D1 x D2)")
    P("=" * 96)
    files = [f for f in sorted(OUT.glob("*.csv")) if not f.name.startswith(SLUG + ".")]
    P(f"  committed CSVs to scan: {len(files):,}  "
      f"(self-excluded: this run's own {SLUG}.*.csv outputs)")
    rows = []
    bad_read = 0
    for i, f in enumerate(files):
        if i and i % 1000 == 0:
            P(f"    ... {i:,} / {len(files):,}")
        try:
            raw = pd.read_csv(f, dtype=str, keep_default_na=False, low_memory=False)
            inf = pd.read_csv(f, low_memory=False)
        except Exception:
            bad_read += 1
            continue
        if len(raw) == 0 or list(raw.columns) != list(inf.columns):
            continue
        for c in raw.columns:
            rs = raw[c].astype(str)
            vs = inf[c].astype(str)
            n = len(rs)
            lit_bad = int((rs.values != vs.values).sum())
            # SEMANTIC: does the raw -> re-read map collide?
            pairs = pd.DataFrame({"r": rs.values, "v": vs.values}).drop_duplicates()
            n_raw_vals = pairs.r.nunique()
            n_map_vals = pairs.v.nunique()
            semantic_bad = n_map_vals < n_raw_vals
            mode, ex_r, ex_v = "", "", ""
            if lit_bad:
                bp = pairs[pairs.r.values != pairs.v.values]
                ex_r, ex_v = str(bp.r.iloc[0]), str(bp.v.iloc[0])
                mode = _mode(bp)
            rows.append(dict(file=f.name, column=c, n_rows=n, fail_mode=mode,
                             is_seed_key=(c.lower() in seed_toks),
                             literal_bad_cells=lit_bad,
                             literal_fail=bool(lit_bad > 0),
                             semantic_fail=bool(semantic_bad),
                             n_raw_vals=n_raw_vals, n_map_vals=n_map_vals,
                             example_raw=ex_r, example_reread=ex_v))
        del raw, inf
    df = pd.DataFrame(rows)
    P(f"  unreadable CSVs (skipped, reported not hidden) : {bad_read}")
    return df


def census_report(df):
    nfiles = df.file.nunique()
    P(f"\n  columns scanned                               : {len(df):,} in {nfiles:,} files")
    P(f"  SEED_KEY columns (named in a committed mdseed): {int(df.is_seed_key.sum()):,}")
    grid = []
    P("\n  D1 x D2 GRID (all four points):")
    P(f"    {'class':<10s} {'test':<9s} {'cols':>8s} {'cols_fail':>10s} {'share':>8s} "
      f"{'files_fail':>11s} {'file_share':>11s}")
    for cls, sub in (("SEED_KEY", df[df.is_seed_key]), ("ANY_KEY", df)):
        for test, col in (("LITERAL", "literal_fail"), ("SEMANTIC", "semantic_fail")):
            cf = int(sub[col].sum())
            ff = sub.loc[sub[col], "file"].nunique()
            grid.append(dict(column_class=cls, round_trip_test=test, n_cols=len(sub),
                             n_cols_fail=cf, col_share=cf / max(len(sub), 1),
                             n_files_fail=ff, file_share=ff / nfiles))
            P(f"    {cls:<10s} {test:<9s} {len(sub):>8,d} {cf:>10,d} "
              f"{cf/max(len(sub),1):>8.2%} {ff:>11,d} {ff/nfiles:>11.2%}")
    W("grid", pd.DataFrame(grid))

    P("\n  HOW the LITERAL failures break down BY MODE (the decomposition that matters):")
    P(f"    {'class':<10s} {'mode':<11s} {'cols':>8s} {'files':>7s} {'cells':>12s}")
    for cls, sub in (("SEED_KEY", df[df.is_seed_key]), ("ANY_KEY", df)):
        fs = sub[sub.literal_fail]
        for m in ("KEY", "EMPTY_NAN", "FLOAT_REPR", "OTHER"):
            gg = fs[fs.fail_mode == m]
            if len(gg) or m != "OTHER":
                P(f"    {cls:<10s} {m:<11s} {len(gg):>8,d} {gg.file.nunique():>7,d} "
                  f"{int(gg.literal_bad_cells.sum()):>12,d}")
    P("\n  WHICH SEED_KEY COLUMN NAMES FAIL LITERAL (every one, with an example):")
    sk = df[df.is_seed_key & df.literal_fail]
    for name, g in sk.groupby("column"):
        ex = g.iloc[0]
        ex = g.sort_values("fail_mode").iloc[0]
        P(f"    {name:<12s} {g.file.nunique():>4d} files  {int(g.literal_bad_cells.sum()):>9,d} cells  "
          f"modes {dict(g.fail_mode.value_counts())}  "
          f"e.g. '{ex.example_raw}' -> '{ex.example_reread}' ({ex.fail_mode})  "
          f"SEMANTIC-lossy in {int(g.semantic_fail.sum())} of {len(g)}")
    if sk.empty:
        P("    (none)")
    P("\n  TOP NON-SEED columns by failing cells (context, not the claim):")
    ns = df[~df.is_seed_key & df.literal_fail].groupby("column").agg(
        files=("file", "nunique"), cells=("literal_bad_cells", "sum"),
        semantic=("semantic_fail", "sum")).sort_values("cells", ascending=False).head(10)
    for name, r in ns.iterrows():
        P(f"    {name:<24s} {int(r.files):>4d} files  {int(r.cells):>9,d} cells  "
          f"SEMANTIC-lossy in {int(r.semantic)}")
    W("census", df)


# ================================================================= PART B — PRICE
def lagmat(a):
    out = np.zeros_like(a)
    out[LAG:] = a[:-LAG]
    return out


def nrun(rets, wt, mk):
    T, K = rets.shape
    mk = mk.copy(); mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, K)), Cc[:-1]])
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
    return (held * rets).sum(axis=1) - turn * COST / 1e4, turn


def fmet(r):
    r = np.asarray(r, float)
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def build(rank_key, ok, reb, N, cap, H, T, K, gross=GROSS):
    """1071's build(), verbatim in semantics: min hold H, N slots, per-name cap multiple
    `cap` (w_i = min(gross/n_sel, cap*gross/N)), residual -> CASH."""
    Wt = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    per_cap = cap * gross / N if np.isfinite(cap) else np.inf
    for t in reb:
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        young = young[ok[t, young]] if len(young) else young
        keep = list(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = rank_key[t].copy()
            k[~ok[t]] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        sel = keep + take
        new_cur = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new_cur[c] = cur[c]
        for c in take:
            new_cur[c] = t
        cur = new_cur
        if sel:
            w = min(gross / len(sel), per_cap)
            Wt[t, sel] = w
    return _ffill_rows(Wt, reb)


def _ffill_rows(Wt, reb):
    """Hold the last rebalance's targets between rebalances (the engine drifts them)."""
    out = np.zeros_like(Wt)
    last = np.zeros(Wt.shape[1])
    j = 0
    rebset = set(int(x) for x in reb)
    for t in range(Wt.shape[0]):
        if t in rebset:
            last = Wt[t]
        out[t] = last
    return out


def price(seed_toks):
    P("\n" + "=" * 96)
    P("PART B — PRICE: what a default-dtype RE-READ of 1071's `cap` column gets wrong")
    P("=" * 96)
    P("  The re-read map, taken from pandas itself (not asserted):")
    probe = pd.read_csv(
        io.StringIO("cap\n" + "\n".join(c for c, _ in CAPS) + "\n"))
    for (cname, _), v in zip(CAPS, probe["cap"].astype(str)):
        P(f"    committed '{cname}'  ->  re-read '{v}'   "
          f"seed {mdseed('U56', 20, cname, 0)} -> {mdseed('U56', 20, v, 0)}"
          f"   {'SAME' if cname == v else 'DIFFERENT'}")

    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    rows, wf_rows = [], []
    sl = slice(WARM, None)
    for pname, px in panels.items():
        idx = px.index
        T, K = px.shape
        rets = px.pct_change().fillna(0.0).values
        mk = np.roll(rebalance_mask(idx, FREQ).values, LAG)
        reb = np.flatnonzero(mk)
        yrs = (T - WARM) / 252.0
        s, above, vol20 = score(px, vol_scale=True)
        ok_book = (above & (vol20 < MAXVOL) & px.notna()).values
        rk_book = -np.nan_to_num(s.values, nan=-np.inf)
        rk_book[np.isnan(s.values)] = np.inf
        ok_open = px.notna().values
        for cname, cap in CAPS:
            reread = str(pd.read_csv(io.StringIO(f"cap\n{cname}\n"))["cap"].iloc[0])
            for N in N_LADDER:
                bw = lagmat(build(rk_book, ok_book, reb, N, cap, H_HOLD, T, K))
                br, bt = nrun(rets, bw, mk)
                b_cagr, b_sh, b_dd = fmet(br[sl])
                # the two null families: seeded from the COMMITTED literal vs the RE-READ value
                fam = {}
                for tag, key in (("RAW", cname), ("REREAD", reread)):
                    cs = []
                    for sd_i in range(SEEDS):
                        sd = mdseed(pname, N, key, sd_i)
                        rng = np.random.default_rng(sd)
                        rk = rng.random((T, K))
                        nw = lagmat(build(rk, ok_open, reb, N, cap, H_HOLD, T, K))
                        nr, _ = nrun(rets, nw, mk)
                        cs.append(fmet(nr[sl])[0])
                    fam[tag] = np.array(cs)
                med_raw, med_rr = float(np.median(fam["RAW"])), float(np.median(fam["REREAD"]))
                edge_raw = (b_cagr - med_raw) * 100
                edge_rr = (b_cagr - med_rr) * 100
                se = float(np.std(fam["RAW"], ddof=1) / np.sqrt(SEEDS)) * 100
                rows.append(dict(panel=pname, N=N, cap_committed=cname, cap_reread=reread,
                                 seeds_identical=(cname == reread),
                                 book_CAGR=b_cagr, null_med_RAW=med_raw,
                                 null_med_REREAD=med_rr,
                                 EDGE_RAW_pp=edge_raw, EDGE_REREAD_pp=edge_rr,
                                 DELTA_pp=edge_rr - edge_raw, seed_SE_pp=se,
                                 reproduces=bool(abs(edge_rr - edge_raw) < 1e-12),
                                 within_1SE=bool(abs(edge_rr - edge_raw) <= se),
                                 book_Sharpe=b_sh, book_MaxDD=b_dd, NTURN=bt[sl].sum() / yrs))
                P(f"  {pname:5s} N={N:<3d} cap={cname:<4s} book {b_cagr:7.2%}  "
                  f"EDGE raw {edge_raw:+7.4f} pp  re-read {edge_rr:+7.4f} pp  "
                  f"delta {edge_rr-edge_raw:+7.4f} pp (seed SE {se:.4f})")
                sr = pd.Series(br, index=idx).iloc[WARM:]
                h = len(sr) // 2
                is_m, oos_m = fmet(sr.loc[:IS_END].values), fmet(sr.loc[OOS_START:].values)
                h1, h2 = fmet(sr.iloc[:h].values), fmet(sr.iloc[h:].values)
                wf_rows.append(dict(panel=pname, N=N, cap=cname, full_CAGR=b_cagr,
                                    full_Sharpe=b_sh, full_MaxDD=b_dd, H1_Sharpe=h1[1],
                                    H2_Sharpe=h2[1], IS_Sharpe=is_m[1], IS_CAGR=is_m[0],
                                    OOS_CAGR=oos_m[0], OOS_Sharpe=oos_m[1],
                                    OOS_MaxDD=oos_m[2]))
    df = pd.DataFrame(rows)
    W("reprice", df)
    return df, pd.DataFrame(wf_rows), panels


# ================================================================= GATES
def gates(panels):
    P("\n" + "=" * 96)
    P("GATES (printed BEFORE any result number)")
    P("=" * 96)
    g = {}
    px = panels["U56"]
    idx = px.index
    T, K = px.shape
    rets = px.pct_change().fillna(0.0).values
    mk = np.roll(rebalance_mask(idx, FREQ).values, LAG)
    reb = np.flatnonzero(mk)
    s, above, vol20 = score(px, vol_scale=True)
    ok = (above & (vol20 < MAXVOL) & px.notna()).values
    rk = -np.nan_to_num(s.values, nan=-np.inf)
    rk[np.isnan(s.values)] = np.inf
    Wt = build(rk, ok, reb, 20, np.inf, H_HOLD, T, K)
    wdf = pd.DataFrame(lagmat(Wt), index=idx, columns=px.columns)

    r_fast, t_fast = nrun(rets, lagmat(Wt), mk)
    eng = backtest(px, pd.DataFrame(Wt, index=idx, columns=px.columns),
                   cost_bps=COST, freq=FREQ)
    d = float(np.abs(r_fast[WARM:] - eng["returns"].values[WARM:]).max())
    g["G1 fast runner NET returns == engine.backtest (post-warm-up)"] = (d, d < 1e-12)
    db = float(np.abs(t_fast[WARM:] - eng["turnover"].values[WARM:]).max())
    g["G1b fast runner turnover == engine.backtest (post-warm-up)"] = (db, db < 1e-12)

    g["G2 cap=INF book holds exactly N=20 slots at gross 0.75"] = (
        float(Wt[reb].sum(axis=1).max()), abs(Wt[reb].sum(axis=1).max() - GROSS) < 1e-12)
    W1 = build(rk, ok, reb, 20, 1.00, H_HOLD, T, K)
    mxc = float(W1[reb].max())
    g["G2b cap=1.00 BINDS: per-name weight <= 1.00*gross/N on the capped book"] = (
        mxc, mxc <= GROSS / 20 + 1e-12)
    dcap = float(W1[reb].sum(axis=1).max() - Wt[reb].sum(axis=1).max())
    g["G2c the cap DE-GROSSES (capped book's gross <= uncapped's)"] = (dcap, dcap <= 1e-12)

    # G3 the DEFECT itself, from pandas, not asserted
    rr = pd.read_csv(io.StringIO("cap\nINF\n1.00\n"))["cap"].astype(str).tolist()
    g["G3 pandas re-reads 'INF'/'1.00' as something else (defect reproduced)"] = (
        float(rr != ["INF", "1.00"]), rr != ["INF", "1.00"])
    sd_a, sd_b = mdseed("U56", 20, "INF", 0), mdseed("U56", 20, "inf", 0)
    g["G3b the two literals give DIFFERENT md5 seeds"] = (
        float(sd_a != sd_b), sd_a != sd_b)

    # G6 — the CONTROL the priced grid cannot supply (all four committed cap literals fail to
    # survive, so there is no naturally-surviving cell).  Drawing the SAME key twice must give
    # a bit-identical null family; only then is a non-zero RAW-vs-REREAD delta attributable to
    # the key and not to the machinery.
    ok_open = px.notna().values
    def _fam(key):
        out = []
        for i in range(3):
            rng = np.random.default_rng(mdseed("U56", 20, key, i))
            nw = lagmat(build(rng.random((T, K)), ok_open, reb, 20, np.inf, H_HOLD, T, K))
            out.append(fmet(nrun(rets, nw, mk)[0][WARM:])[0])
        return np.array(out)
    d6 = float(np.abs(_fam("INF") - _fam("INF")).max())
    g["G6 same key -> bit-identical null family (reproduction control)"] = (d6, d6 == 0.0)
    d6b = float(np.abs(_fam("INF") - _fam("inf")).max())
    g["G6b 'INF' vs 'inf' -> a DIFFERENT null family (the defect, priced)"] = (d6b, d6b > 0.0)

    v2 = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)
    v2m = fmet(v2["returns"].iloc[WARM:].values)
    g["G4 live RULES v2 MaxDD == record's -12.05%"] = (v2m[2], abs(v2m[2] + 0.1205) < 5e-4)

    spy = px["SPY"].pct_change().fillna(0.0).values[WARM:]
    g["G5 SPY post-warm-up CAGR (context, not a pass/fail)"] = (fmet(spy)[0], True)

    npass = sum(1 for _, (v, okk) in g.items() if okk)
    for k, (v, okk) in g.items():
        P(f"  [{'PASS' if okk else 'FAIL'}] {k}: {v:.6g}")
    P(f"  GATES {npass} of {len(g)} PASS")
    return g, v2m


# ================================================================= PART C — ANSWER
def answer(cen, rep):
    P("\n" + "=" * 96)
    P("PART C — THE ANSWER")
    P("=" * 96)
    nfiles = cen.file.nunique()
    sk = cen[cen.is_seed_key]
    sk_lit_files = sk.loc[sk.literal_fail, "file"].nunique()
    P(f"  SEED_KEY columns failing LITERAL: {int(sk.literal_fail.sum()):,} of {len(sk):,} "
      f"({sk.literal_fail.mean():.2%}) across {sk_lit_files:,} of {nfiles:,} files "
      f"({sk_lit_files/nfiles:.2%})")
    P(f"  ANY_KEY  columns failing LITERAL: {int(cen.literal_fail.sum()):,} of {len(cen):,} "
      f"({cen.literal_fail.mean():.2%})")
    P(f"  SEED_KEY columns SEMANTICALLY lossy: {int(sk.semantic_fail.sum()):,}")
    P(f"  ANY_KEY  columns SEMANTICALLY lossy: {int(cen.semantic_fail.sum()):,}")

    bad = rep[~rep.seeds_identical]
    P(f"\n  PRICED CELLS: {len(rep)} ({len(bad)} whose committed cap literal does NOT survive)")
    if len(bad):
        P(f"    EDGE shift |delta| median {bad.DELTA_pp.abs().median():.4f} pp, "
          f"max {bad.DELTA_pp.abs().max():.4f} pp; seed SE median {bad.seed_SE_pp.median():.4f} pp")
        P(f"    cells reproducing the committed EDGE exactly : "
          f"{int(bad.reproduces.sum())} of {len(bad)}")
        P(f"    cells inside 1 seed SE of it                 : "
          f"{int(bad.within_1SE.sum())} of {len(bad)} ({bad.within_1SE.mean():.1%})")
    good = rep[rep.seeds_identical]
    P(f"    CONTROL — cells whose literal DOES survive: {int(good.reproduces.sum())} of "
      f"{len(good)} reproduce exactly (must be all of them)")

    H = {}
    H["H_WIDE      >5% of committed CSVs carry a SEED_KEY LITERAL failure"] = (
        sk_lit_files / nfiles > 0.05)
    H["H_SEED      SEED_KEY LITERAL rate > ANY_KEY LITERAL rate"] = bool(
        sk.literal_fail.mean() > cen.literal_fail.mean())
    H["H_SEMANTIC  at least one SEED_KEY column is SEMANTICALLY lossy"] = bool(
        sk.semantic_fail.sum() > 0)
    H["H_PRICE     re-read reproduces < half of the affected cells"] = bool(
        len(bad) > 0 and bad.reproduces.mean() < 0.5)
    H["H_CAPONLY   `cap` is the ONLY seed-key column failing LITERAL"] = bool(
        set(sk.loc[sk.literal_fail, "column"].str.lower()) <= {"cap"})
    P("\n  HYPOTHESES (declared before any number):")
    for k, v in H.items():
        P(f"    [{'PASS' if v else 'FAIL'}] {k}")
    P(f"    HYPOTHESES {sum(H.values())} of {len(H)} PASS")
    W("hypotheses", pd.DataFrame([dict(hypothesis=k, verdict="PASS" if v else "FAIL")
                                  for k, v in H.items()]))
    return H


# ================================================================= PART D — RULE 8
def rule8(wf, panels, v2m):
    P("\n" + "=" * 96)
    P("PART D — RULE 8 WALK-FORWARD and BOTH KEEP PATHS")
    P("=" * 96)
    bench = {}
    for pname, px in panels.items():
        spy = px["SPY"].pct_change().fillna(0.0).iloc[WARM:]
        h = len(spy) // 2
        bench[pname] = dict(full=fmet(spy.values), OOS=fmet(spy.loc[OOS_START:].values),
                            H1=fmet(spy.iloc[:h].values), H2=fmet(spy.iloc[h:].values))
        b = bench[pname]
        P(f"  SPY on {pname:5s}: full {b['full'][0]:7.2%} / {b['full'][1]:.4f} / "
          f"{b['full'][2]:7.2%}   OOS {b['OOS'][0]:7.2%} / {b['OOS'][1]:.4f} / "
          f"{b['OOS'][2]:7.2%}   halves {b['H1'][1]:.4f} / {b['H2'][1]:.4f}")
    P(f"  RULES v2 (live, U56, post-warm-up): {v2m[0]:.2%} / {v2m[1]:.4f} / {v2m[2]:.2%}")

    rows = []
    for _, r in wf.iterrows():
        b = bench[r.panel]
        L_H1 = r.H1_Sharpe > b["H1"][1]
        L_H2 = r.H2_Sharpe > b["H2"][1]
        L_OOS = r.OOS_Sharpe > b["OOS"][1]
        L_DD = r.full_MaxDD >= 0.60 * b["full"][2]
        L_CAGR = r.full_CAGR >= 0.70 * b["full"][0]
        rows.append(dict(panel=r.panel, N=int(r.N), cap=r.cap, full_CAGR=r.full_CAGR,
                         full_Sharpe=r.full_Sharpe, full_MaxDD=r.full_MaxDD,
                         H1=r.H1_Sharpe, H2=r.H2_Sharpe, IS_Sharpe=r.IS_Sharpe,
                         OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe,
                         OOS_MaxDD=r.OOS_MaxDD, L_H1=L_H1, L_H2=L_H2, L_OOS=L_OOS,
                         L_DD=L_DD, L_CAGR=L_CAGR,
                         PASS_4b=bool(L_H1 and L_H2 and L_OOS and L_DD and L_CAGR),
                         PASS_4b_OOS=bool(L_OOS and r.OOS_MaxDD >= 0.60 * b["OOS"][2]
                                          and r.OOS_CAGR >= 0.70 * b["OOS"][0]),
                         PASS_4a=bool(r.H1_Sharpe > v2m[1] and r.H2_Sharpe > v2m[1]
                                      and r.full_MaxDD >= v2m[2])))
    wfd = pd.DataFrame(rows)
    P("\n  ALL GRID POINTS (no cell hidden):")
    P(f"    {'panel':<6s}{'N':>3s} {'cap':>5s} {'fullCAGR':>9s} {'fullShp':>8s} {'fullDD':>8s} "
      f"{'H1':>7s} {'H2':>7s} {'oosCAGR':>9s} {'oosShp':>7s} {'oosDD':>8s} {'4a':>5s} "
      f"{'4b':>5s} {'4bOOS':>6s}")
    for _, r in wfd.iterrows():
        P(f"    {r.panel:<6s}{r.N:>3d} {r.cap:>5s} {r.full_CAGR:>9.2%} {r.full_Sharpe:>8.4f} "
          f"{r.full_MaxDD:>8.2%} {r.H1:>7.4f} {r.H2:>7.4f} {r.OOS_CAGR:>9.2%} "
          f"{r.OOS_Sharpe:>7.4f} {r.OOS_MaxDD:>8.2%} {str(r.PASS_4a):>5s} "
          f"{str(r.PASS_4b):>5s} {str(r.PASS_4b_OOS):>6s}")
    P("\n  RULE 8 CHOOSERS (choose on IS 2009-2016, read OOS ONCE):")
    for pname in wfd.panel.unique():
        sub = wfd[wfd.panel == pname]
        b = bench[pname]
        for cn, col in (("C_SHARPE", "IS_Sharpe"), ("C_CAGR", "full_CAGR")):
            pk = sub.loc[sub[col].idxmax()]
            P(f"    {pname:5s} {cn:9s} picks N={pk.N} cap={pk.cap:<4s} -> OOS "
              f"{pk.OOS_CAGR:7.2%} / {pk.OOS_Sharpe:.4f} / {pk.OOS_MaxDD:7.2%}  "
              f"vs SPY OOS {b['OOS'][0]:7.2%} / {b['OOS'][1]:.4f} / {b['OOS'][2]:7.2%}  "
              f"-> 4b OOS {'PASS' if pk.PASS_4b_OOS else 'FAIL'}")
    P(f"\n  4a: {int(wfd.PASS_4a.sum())} of {len(wfd)}   "
      f"4b full: {int(wfd.PASS_4b.sum())} of {len(wfd)}   "
      f"4b OOS: {int(wfd.PASS_4b_OOS.sum())} of {len(wfd)}")
    for leg in ("L_CAGR", "L_H1", "L_H2", "L_OOS", "L_DD"):
        P(f"    {leg:7s} {int(wfd[leg].sum()):>2d} of {len(wfd)}")
    W("walkforward", wfd)
    return wfd


def main():
    P(f"# {SLUG}")
    P(f"# COST {COST} bps | GROSS {GROSS} | FREQ {FREQ} | LAG {LAG} | WARM {WARM} | "
      f"SEEDS {SEEDS} | H {H_HOLD}")
    P(f"# N ladder {N_LADDER} | caps {[c for c,_ in CAPS]}")
    toks, calls = harvest_seed_tokens()
    P(f"# seed-key tokens harvested from {calls} committed mdseed() call sites: "
      f"{sorted(toks)}")
    panels0 = {"U56": load_universe(), "B136": load_universe(broad=True)}
    g, v2m = gates(panels0)
    cen = census(toks)
    census_report(cen)
    rep, wf, panels = price(toks)
    answer(cen, rep)
    rule8(wf, panels, v2m)
    (OUT / f"{SLUG}.console.txt").write_text("\n".join(LOG))
    P(f"\nwrote {SLUG}.console.txt")


if __name__ == "__main__":
    main()
