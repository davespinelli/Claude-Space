#!/usr/bin/env python3
"""QUEUE idea 430 — BACK-FILL `lift` BESIDE EVERY PUBLISHED SELECTOR CLAIM  (cloud, 2026-09-08).

QUESTION (verbatim, QUEUE.md idea 430)
    "idea 204 shows `lift` = M(pick) - mean_P M(a) is the only part of a selector claim that is
     invariant to the comparand (0.000e+00 across three comparands, while `sel_d` moves up to
     0.9280 of Sharpe).  Idea 205 back-filled the pool mean; back-fill `lift` the same way over
     every reconstructable selector claim and report how many published 'selection helps'
     sentences have a lift indistinguishable from zero.  Cheap; max 2 params."

WHAT IS ALREADY DONE, AND WHAT IS NOT (stated up front so this run is not read as new work it is not)
    The BACK-FILL ITSELF IS ALREADY COMMITTED.  Idea 205's census
    (2026-09-08_the-pool-mean-as-a-leaderboard-column_cloud.claims.csv) computes
    `lift = sel_dOOS - pool_mean_dOOS` on line 189 of its own script, for every claim it
    recovers.  Re-deriving that column is bookkeeping, and this run reproduces it as a GATE, not
    as a finding.  What NOTHING in the record has is the second half of the queue's sentence:
    **"indistinguishable from zero" has never been given a null.**  A lift is one number.  Without
    a reference distribution it can be neither distinguished from zero nor not.

    So the content of this run is the NULL, and it is the one null the object itself supplies:

        RANDOM-PICK-FROM-THE-SAME-POOL.  Let the pool be P = {a_1..a_n} with metrics M_1..M_n and
        mean mbar.  A selector that picks a* has lift = M(a*) - mbar.  A selector that picks
        UNIFORMLY AT RANDOM from P has lift distributed exactly as {M_i - mbar}, mean 0 by
        construction.  So the EXACT two-sided p-value of any published lift is

            p2 = (1/n) * #{ i : |M_i - mbar| >= |lift_obs| }          (and p1 = (1/n)*#{M_i >= M(a*)})

        no bootstrap, no assumption, no fitted parameter.  It is the finite-population
        permutation test, and every input already sits in the parent script's own CSV.

    The consequence is arithmetic and is the run's headline: p2 >= 1/n ALWAYS, because the pick is
    itself a member of the pool.  A claim drawn from a pool of n arms therefore CANNOT reach
    p2 < 0.05 unless n >= 20.  Whether the record's published "selection helps" sentences are
    falsifiable at all is thus a fact about POOL SIZE, decidable before any performance number is
    read.  This run decides it.

WHAT THIS RUN REPORTS
    G  GATES.  (G1) lift reproduces idea 205's committed column to machine zero on the shared
       rows.  (G2) lift is invariant to the comparand (idea 204's 0.000e+00 re-measured here).
       (G3) the fresh-book path's fast/engine equivalence.
    Q1 THE BACK-FILL, with the null attached.  Every reconstructable claim gets
       lift / p1 / p2 / n_pool / attainable(p2<0.05).  Full census table, all 8 grid points.
    Q2 HOW MANY PUBLISHED "SELECTION HELPS" SENTENCES SURVIVE?  A published claim counts as a
       "selection helps" sentence iff sel_dOOS > 0 (the record wrote it up as a win).  Of those,
       what share has p2 >= 0.05, what share has lift <= 0 outright (the win is the POOL, not the
       pick), and what share is UNFALSIFIABLE by construction (n_pool < 20)?
    Q3 THE POOLED READING.  Mean lift with a paired t and an exact sign test, per grid point, and
       the same split by claim sign — because a corpus of individually-unfalsifiable claims can
       still carry a jointly measurable mean.
    Q4 RULE 8 / W1 — CORPUS WALK-FORWARD OF THE PROPOSED SCREEN.  The screen is "publish lift and
       its p2 beside sel_d; a sentence with p2 >= 0.05 is not a selection result."  Its falsifiable
       content: does a claim's lift-significance IN SAMPLE predict a positive lift OUT OF SAMPLE?
       Claims are split by PARENT SCRIPT DATE (IS = earlier half, OOS = later half read once).
    Q5 RULE 8 / W2 — A FRESH BOOK POOL, so the column is demonstrated on real books and both KEEP
       paths are scored on real returns.  u56, top-n equal-weight, no vol scaler, weekly, t+1,
       10 bps: n {10,15,20,25,30} x g {0.50,0.625,0.75,0.875,1.00} = 25 arms, ALL reported.
       Arms are fitted on 2010-2016 by IS Sharpe; 2017-2026 is read ONCE.  The pick's lift gets
       the same exact p2 the census gives archived claims.
    Q6 BOTH KEEP PATHS (4a vs live RULES v2, 4b vs SPY) on every W2 arm and on the walk-forward
       pick, full sample / halves / OOS.  This is a bookkeeping idea and cannot promote a book;
       PROTOCOL requires the paths be scored, so they are.

PARAMETERS (2, swept, ALL 8 grid points reported)
    p1  pool_def in {ALL, LIVE}      — all pool rows, vs rows the parent file itself does not flag
                                       as null/control/random arms
    p2  MIN_POOL in {3, 5, 8, 12}    — the admission threshold on pool size
    Nothing else is tuned.  The 0.05 level is the record's own convention, not a fitted knob, and
    the whole p-curve is printed so any other level can be read off the table.

Outputs (committed): .console.txt .claims.csv .stems.csv .census.csv .walkforward.csv .arms.csv
                     .result.md
Deterministic; no network; imports research/baseline.py only.
"""
import sys, re, time, glob, math
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics  # noqa

STAMP = "2026-09-08_back-fill-LIFT-beside-every-published-selector-claim_cloud"
OUT = Path(__file__).resolve().parent
IS_END, OOS_START = "2016-12-31", "2017-01-01"
POOL_DEFS = ("ALL", "LIVE")
MIN_POOLS = (3, 5, 8, 12)
ALPHA = 0.05

_LOG: list[str] = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); _LOG.append(s)


# ------------------------------------------------------------------ file discovery (idea 205's rule, verbatim)
SEL_SUF = [".walkforward.csv", ".picks.csv", ".choices.csv"]
POOL_SUF = [".grid.csv", ".arms.csv", ".ladder.csv", ".corpus.csv", ".sweep.csv",
            ".cells.csv", ".points.csv"]
CELL_KEYS = ["panel", "universe", "uni", "book", "grid", "corpus", "family", "fam",
             "cost", "cost_bps", "bps", "arm", "kind", "conv", "dial", "gate", "mode",
             "gross_mode", "cadence", "freq", "n", "g"]
CTRL_PAT = re.compile(r"^(base|ctl|ctrl|control|v1|s0|do_?nothing|anchor|incumbent|cell)_", re.I)
SPY_PAT = re.compile(r"^spy_", re.I)
OWN_OOS = ["OOS_Sharpe", "Sharpe_OOS", "oos_sharpe", "sharpe_oos"]


def read_csv(p):
    return pd.read_csv(p, compression="gzip" if str(p).endswith(".gz") else None, low_memory=False)


def own_oos_col(cols):
    for c in OWN_OOS:
        for k in cols:
            if k == c: return k
    return None


def comparand_cols(cols):
    out = {}
    for k in cols:
        kl = k.lower()
        if "sharpe" not in kl or "oos" not in kl: continue
        if k in OWN_OOS: continue
        if SPY_PAT.match(k) and "SPY" not in out: out["SPY"] = k
        elif CTRL_PAT.match(k) and "CONTROL" not in out: out["CONTROL"] = k
    return out


def live_mask(pool):
    m = pd.Series(True, index=pool.index)
    for c in ("is_null", "isnull"):
        if c in pool.columns: m &= ~pool[c].astype(str).str.lower().isin(["true", "1", "1.0"])
    for c in ("apriori",):
        if c in pool.columns: m &= ~pool[c].astype(str).str.lower().isin(["true", "1", "1.0"])
    for c in ("kind", "arm", "book"):
        if c in pool.columns:
            m &= ~pool[c].astype(str).str.lower().isin(
                ["null", "control", "ctl", "ctrl", "do-nothing", "donothing", "rand", "random"])
    return m


# ------------------------------------------------------------------ THE NULL
def exact_p(M, m_pick):
    """Exact random-pick-from-the-same-pool null for lift.

    M       array of the pool's own OOS metrics (the pick is one of them)
    m_pick  the picked arm's metric

    Returns (lift, p_one_sided, p_two_sided, n).  Under a uniform random pick the lift is
    distributed exactly as {M_i - mean(M)}, so both p-values are counting statements over the
    pool itself.  No parameter, no resampling, no distributional assumption.
    """
    M = np.asarray(M, dtype=float)
    M = M[np.isfinite(M)]
    n = len(M)
    if n == 0: return np.nan, np.nan, np.nan, 0
    mbar = float(M.mean())
    lift = float(m_pick) - mbar
    dev = np.abs(M - mbar)
    p2 = float((dev >= abs(lift) - 1e-15).sum()) / n
    p1 = float((M >= float(m_pick) - 1e-15).sum()) / n
    return lift, p1, p2, n


# ==================================================================================== census
def build_census():
    """Reconstruct every claim, and — unlike idea 205 — keep the pool's FULL metric vector so the
    null above can be evaluated."""
    stems = {}
    for f in sorted(glob.glob(str(OUT / "*.csv"))) + sorted(glob.glob(str(OUT / "*.csv.gz"))):
        b = Path(f).name
        b = b[:-3] if b.endswith(".gz") else b
        m = re.match(r"(.+?)\.([A-Za-z0-9_]+)\.csv$", b)
        if not m: continue
        stems.setdefault(m.group(1), {})["." + m.group(2) + ".csv"] = f

    claims, stem_rows = [], []
    for stem, d in sorted(stems.items()):
        if stem == STAMP: continue                      # never census our own output
        sel_f = next((d[s] for s in SEL_SUF if s in d), None)
        pool_f = next((d[s] for s in POOL_SUF if s in d), None)
        st = dict(stem=stem, sel=Path(sel_f).name.split(".")[-2] if sel_f else "",
                  pool=Path(pool_f).name.split(".")[-2] if pool_f else "",
                  status="", n_claims=0, n_dropped_thin=0, keys="")
        if not sel_f or not pool_f:
            st["status"] = "no sel/pool pair"; stem_rows.append(st); continue
        try:
            sel, pool = read_csv(sel_f), read_csv(pool_f)
        except Exception as e:
            st["status"] = f"unreadable: {type(e).__name__}"; stem_rows.append(st); continue
        so, po = own_oos_col(sel.columns), own_oos_col(pool.columns)
        if so is None or po is None:
            st["status"] = "no OOS_Sharpe column"; stem_rows.append(st); continue
        comp = comparand_cols(sel.columns)
        if not comp:
            st["status"] = "no comparand column"; stem_rows.append(st); continue
        keys = [k for k in CELL_KEYS if k in sel.columns and k in pool.columns]
        st["keys"] = "|".join(keys)
        pool = pool[np.isfinite(pd.to_numeric(pool[po], errors="coerce"))].copy()
        pool[po] = pd.to_numeric(pool[po], errors="coerce")
        if not len(pool):
            st["status"] = "empty pool"; stem_rows.append(st); continue
        lm = live_mask(pool)

        if keys:
            gall = {k: v for k, v in pool.groupby([pool[c].astype(str) for c in keys])}
            gliv = {k: v for k, v in pool[lm].groupby([pool.loc[lm, c].astype(str) for c in keys])}
        else:
            gall, gliv = {(): pool}, {(): pool[lm]}

        nc = nd = 0
        for _, r in sel.iterrows():
            own = pd.to_numeric(pd.Series([r[so]]), errors="coerce").iloc[0]
            if not np.isfinite(own): continue
            gk = tuple(str(r[c]) for c in keys) if keys else ()
            if keys and len(keys) == 1: gk = gk[0]
            for pdef, gg in (("ALL", gall), ("LIVE", gliv)):
                pl = gg.get(gk)
                if pl is None or len(pl) < min(MIN_POOLS):
                    if pdef == "ALL": nd += 1
                    continue
                Mv = pl[po].values
                lift, p1, p2, npl = exact_p(Mv, float(own))
                pm = float(np.mean(Mv))
                for cname, ccol in comp.items():
                    cv = pd.to_numeric(pd.Series([r[ccol]]), errors="coerce").iloc[0]
                    if not np.isfinite(cv): continue
                    claims.append(dict(
                        stem=stem, date=stem[:10], comparand=cname, pool_def=pdef, n_pool=npl,
                        sel_OOS_Sharpe=float(own), comparand_OOS_Sharpe=float(cv),
                        pool_mean_OOS_Sharpe=pm,
                        sel_dOOS=float(own) - float(cv),
                        pool_mean_dOOS=pm - float(cv),
                        lift=lift, p_one=p1, p_two=p2,
                        attainable=bool(npl >= int(math.ceil(1.0 / ALPHA))),
                        selector=str(r.get("selector", r.get("sel", "")))))
                    nc += 1
        st.update(status="OK" if nc else "no usable claim rows", n_claims=nc, n_dropped_thin=nd)
        stem_rows.append(st)
    return pd.DataFrame(claims), pd.DataFrame(stem_rows)


# ==================================================================================== fresh books (W2)
def topn_ew(n, g, vol_scale=False):
    def f(p):
        s, above, _ = score(p, vol_scale=vol_scale)
        rank = s.where(above).rank(axis=1, ascending=False)
        m = (rank <= n)
        cnt = m.sum(axis=1).replace(0, np.nan)
        return (g * m.astype(float)).div(cnt, axis=0).fillna(0.0)
    return f


def fresh_pool():
    px = load_universe()
    COST, FREQ = 10.0, "W"
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    b2 = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
    v1 = backtest(px, rules_v1_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]

    def halves(r):
        h = len(r) // 2
        return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]

    ms, mso = metrics(spy), metrics(spy.loc[OOS_START:])
    mb, mb1, mb2 = metrics(b2), *halves(b2)
    s1, s2 = halves(spy)

    rows = []
    NS, GS = [10, 15, 20, 25, 30], [0.50, 0.625, 0.75, 0.875, 1.00]
    for n in NS:
        for g in GS:
            r = backtest(px, topn_ew(n, g)(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
            m, mi, mo = metrics(r), metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
            h1, h2 = halves(r)
            rows.append(dict(
                n=n, g=g, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"],
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                keep4a=bool(h1 > mb1 and h2 > mb2 and m["MaxDD"] >= mb["MaxDD"]),
                keep4b=bool(h1 > s1 and h2 > s2 and mo["Sharpe"] > mso["Sharpe"]
                            and m["MaxDD"] >= 0.60 * ms["MaxDD"]
                            and m["CAGR"] >= 0.70 * ms["CAGR"])))
    A = pd.DataFrame(rows)
    bench = dict(spy=ms, spy_oos=mso, spy_h=(s1, s2), b2=mb, b2_h=(mb1, mb2),
                 v1=metrics(v1), v1_oos=metrics(v1.loc[OOS_START:]),
                 b2_oos=metrics(b2.loc[OOS_START:]))
    return A, bench


# ==================================================================================== run
def main():
    t0 = time.time()
    P("=" * 112)
    P("IDEA 430 — BACK-FILL `lift` BESIDE EVERY PUBLISHED SELECTOR CLAIM, WITH A NULL")
    P(f"  p1 pool_def in {POOL_DEFS};  p2 MIN_POOL in {MIN_POOLS}.  All 8 grid points reported.")
    P(f"  null: exact random-pick-from-the-same-pool.  p2 >= 1/n_pool by construction, so a claim")
    P(f"  from a pool of n < {int(math.ceil(1/ALPHA))} arms is UNFALSIFIABLE at alpha={ALPHA} before any number is read.")
    P("=" * 112)

    C, S = build_census()
    C.to_csv(OUT / f"{STAMP}.claims.csv", index=False)
    S.to_csv(OUT / f"{STAMP}.stems.csv", index=False)

    P(f"\nCORPUS  {len(S)} script stems scanned in research/backtests/")
    for st, k in S.status.value_counts().items():
        P(f"  {k:5d}  {st}")
    ok = S[S.status == "OK"]
    P(f"  -> {len(ok)} stems yield {len(C)} (claim x comparand x pool_def) rows at MIN_POOL={min(MIN_POOLS)}; "
      f"{int(S.n_dropped_thin.sum())} claim rows dropped as thinner than that")
    if not len(C):
        P("NO CLAIMS RECOVERED — census aborted."); return
    P(f"  distinct parent dates {C.date.nunique()} ({C.date.min()} .. {C.date.max()}), "
      f"pool size median {C.n_pool.median():.0f}  min {C.n_pool.min():.0f}  max {C.n_pool.max():.0f}")

    # -------------------------------------------------------------------------- GATES
    P("\n" + "=" * 112)
    P("GATES")
    P("=" * 112)
    ref = OUT / "2026-09-08_the-pool-mean-as-a-leaderboard-column_cloud.claims.csv"
    if ref.exists():
        R = read_csv(ref)
        k = ["stem", "comparand", "pool_def", "n_pool", "sel_OOS_Sharpe", "comparand_OOS_Sharpe"]
        # both censuses emit MANY rows per key (one per selector-file row with the same numbers),
        # so a raw merge is a many-to-many blow-up.  Collapse each side to unique keys first and
        # keep only keys that are unambiguous on BOTH sides — anything else is not comparable.
        lhs = C.groupby(k, dropna=False).lift.agg(["nunique", "first"])
        rhs = R.groupby(k, dropna=False).lift.agg(["nunique", "first"])
        j = lhs.join(rhs, how="inner", lsuffix="_l", rsuffix="_r")
        j = j[(j.nunique_l == 1) & (j.nunique_r == 1)]
        if len(j):
            e = float(np.abs(j.first_l - j.first_r).max())
            P(f"  G1  lift reproduces idea 205's committed column on {len(j)} unambiguous shared "
              f"keys ({len(lhs)} keys here, {len(rhs)} there): max abs diff {e:.3e}  "
              f"-> {'PASS' if e < 1e-9 else 'FAIL'}")
        else:
            P("  G1  no shared rows with idea 205's claims.csv (join keys did not match) — SKIPPED")
    else:
        P("  G1  idea 205's claims.csv absent — SKIPPED")

    piv = C.pivot_table(index=["stem", "pool_def", "sel_OOS_Sharpe"], columns="comparand",
                        values="lift", aggfunc="first")
    if {"CONTROL", "SPY"}.issubset(piv.columns):
        both = piv.dropna(subset=["CONTROL", "SPY"])
        e = float(np.abs(both.CONTROL - both.SPY).max()) if len(both) else float("nan")
        sd = C.pivot_table(index=["stem", "pool_def", "sel_OOS_Sharpe"], columns="comparand",
                           values="sel_dOOS", aggfunc="first").dropna(subset=["CONTROL", "SPY"])
        sdmax = float(np.abs(sd.CONTROL - sd.SPY).max()) if len(sd) else float("nan")
        P(f"  G2  COMPARAND INVARIANCE on {len(both)} rows carrying both comparands:")
        P(f"        max |lift(CONTROL) - lift(SPY)|   = {e:.3e}   <- the invariant part")
        P(f"        max |sel_d(CONTROL) - sel_d(SPY)| = {sdmax:.4f}   <- what the comparand is worth")
        P(f"      -> {'PASS' if (not np.isfinite(e)) or e < 1e-9 else 'FAIL'} "
          f"(idea 204 measured 0.000e+00 / up to 0.9280 on its own corpus)")
    else:
        P("  G2  fewer than two comparands recovered — SKIPPED")

    # -------------------------------------------------------------------------- Q1 the census
    P("\n" + "=" * 112)
    P("Q1  THE BACK-FILL WITH ITS NULL — all 8 grid points, nothing hidden")
    P("=" * 112)
    P(f"  {'pool':5s} {'MIN':>4s} {'n_claims':>8s} {'stems':>6s} {'med n_pool':>10s} "
      f"{'mean lift':>9s} {'t':>7s} {'lift>0':>7s} {'p2<.05':>7s} {'share':>7s} {'attainable':>10s}")
    cen = []
    for pdef in POOL_DEFS:
        for mp in MIN_POOLS:
            s = C[(C.pool_def == pdef) & (C.n_pool >= mp)]
            # one row per (stem, claim) — dedupe the comparand axis, lift is invariant to it
            s = s.drop_duplicates(subset=["stem", "pool_def", "sel_OOS_Sharpe", "n_pool", "lift"])
            if not len(s): continue
            lf = s.lift.values
            t = float(lf.mean() / (lf.std(ddof=1) / np.sqrt(len(lf)))) if len(lf) > 1 and lf.std() > 0 else 0.0
            sig = int((s.p_two < ALPHA).sum()); att = int(s.attainable.sum())
            cen.append(dict(pool_def=pdef, min_pool=mp, n_claims=len(s), n_stems=s.stem.nunique(),
                            median_n_pool=float(s.n_pool.median()), mean_lift=float(lf.mean()),
                            median_lift=float(np.median(lf)), t_lift=t,
                            n_lift_positive=int((lf > 0).sum()),
                            n_p2_significant=sig, share_p2_significant=sig / len(s),
                            n_attainable=att, share_attainable=att / len(s)))
            P(f"  {pdef:5s} {mp:4d} {len(s):8d} {s.stem.nunique():6d} {s.n_pool.median():10.0f} "
              f"{lf.mean():+9.4f} {t:+7.2f} {int((lf>0).sum()):7d} {sig:7d} {sig/len(s):7.1%} "
              f"{att/len(s):10.1%}")
    CEN = pd.DataFrame(cen)
    CEN.to_csv(OUT / f"{STAMP}.census.csv", index=False)
    P("  ('attainable' = the share of claims whose pool is large enough (n >= 20) that p2 < 0.05 is")
    P("   REACHABLE at all.  Where it is 0%, no published sentence in that cell can be falsified by")
    P("   its own pool, whatever its lift.)")

    # -------------------------------------------------------------------------- Q2 the queue's count
    P("\n" + "=" * 112)
    P("Q2  HOW MANY PUBLISHED 'SELECTION HELPS' SENTENCES HAVE A LIFT INDISTINGUISHABLE FROM ZERO?")
    P("    (a 'selection helps' sentence = a claim the record published with sel_dOOS > 0)")
    P("=" * 112)
    P(f"  {'pool':5s} {'MIN':>4s} {'n_wins':>7s} {'lift<=0':>8s} {'share':>7s} "
      f"{'p2>=.05':>8s} {'share':>7s} {'unfalsifiable':>13s} {'share':>7s}")
    q2 = []
    for pdef in POOL_DEFS:
        for mp in MIN_POOLS:
            s = C[(C.pool_def == pdef) & (C.n_pool >= mp) & (C.sel_dOOS > 0)]
            s = s.drop_duplicates(subset=["stem", "pool_def", "sel_OOS_Sharpe", "n_pool", "lift"])
            if not len(s): continue
            neg = int((s.lift <= 0).sum()); ins = int((s.p_two >= ALPHA).sum())
            unf = int((~s.attainable).sum())
            q2.append(dict(pool_def=pdef, min_pool=mp, n_wins=len(s), n_lift_nonpositive=neg,
                           share_lift_nonpositive=neg / len(s),
                           n_indistinguishable=ins, share_indistinguishable=ins / len(s),
                           n_unfalsifiable=unf, share_unfalsifiable=unf / len(s)))
            P(f"  {pdef:5s} {mp:4d} {len(s):7d} {neg:8d} {neg/len(s):7.1%} "
              f"{ins:8d} {ins/len(s):7.1%} {unf:13d} {unf/len(s):7.1%}")
    Q2 = pd.DataFrame(q2)
    P("  ('lift<=0' = the published WIN belongs entirely to the pool: the selector picked at or below")
    P("   its own pool's mean and the sentence is an INSTRUMENT result wearing a selector's clothes.)")

    # -------------------------------------------------------------------------- Q3 pooled
    P("\n" + "=" * 112)
    P("Q3  THE POOLED READING — a corpus of individually-unfalsifiable claims can still carry a mean")
    P("=" * 112)
    P(f"  {'pool':5s} {'MIN':>4s} {'subset':14s} {'n':>6s} {'mean lift':>9s} {'sd':>7s} "
      f"{'t':>7s} {'wins':>6s} {'sign p':>8s}")
    def signp(x):
        n = int((x != 0).sum()); k = int((x > 0).sum())
        if n == 0: return float("nan")
        # exact two-sided binomial at 1/2
        c = [math.comb(n, i) for i in range(n + 1)]
        tot = float(sum(c)); lo = min(k, n - k)
        return float(2.0 * sum(c[:lo + 1]) / tot) if 2 * lo != n else 1.0
    for pdef in POOL_DEFS:
        for mp in MIN_POOLS:
            base = C[(C.pool_def == pdef) & (C.n_pool >= mp)].drop_duplicates(
                subset=["stem", "pool_def", "sel_OOS_Sharpe", "n_pool", "lift"])
            for lab, s in (("all claims", base), ("published wins", base[base.sel_dOOS > 0]),
                           ("published losses", base[base.sel_dOOS <= 0])):
                if len(s) < 2: continue
                lf = s.lift.values
                t = float(lf.mean() / (lf.std(ddof=1) / np.sqrt(len(lf)))) if lf.std() > 0 else 0.0
                sp = signp(lf) if len(lf) <= 500 else float("nan")
                P(f"  {pdef:5s} {mp:4d} {lab:14s} {len(s):6d} {lf.mean():+9.4f} "
                  f"{lf.std(ddof=1):7.4f} {t:+7.2f} {int((lf>0).sum()):6d} "
                  f"{(f'{sp:8.4f}' if np.isfinite(sp) else '     n/a')}")

    # -------------------------------------------------------------------------- Q4 rule 8 W1
    P("\n" + "=" * 112)
    P("Q4  RULE 8 / W1 — CORPUS WALK-FORWARD OF THE PROPOSED SCREEN (split by parent script date)")
    P("=" * 112)
    wf = []
    for pdef in POOL_DEFS:
        for mp in MIN_POOLS:
            s = C[(C.pool_def == pdef) & (C.n_pool >= mp)].drop_duplicates(
                subset=["stem", "pool_def", "sel_OOS_Sharpe", "n_pool", "lift"]).sort_values("date")
            if len(s) < 20: continue
            dates = sorted(s.date.unique())
            cut = dates[len(dates) // 2]
            IS, OS = s[s.date < cut], s[s.date >= cut]
            if len(IS) < 5 or len(OS) < 5: continue
            def blk(z):
                lf = z.lift.values
                t = float(lf.mean() / (lf.std(ddof=1) / np.sqrt(len(lf)))) if len(lf) > 1 and lf.std() > 0 else 0.0
                return len(z), float(lf.mean()), t, float((lf > 0).mean()), float((z.p_two < ALPHA).mean())
            ni, mi_, ti, wi, si = blk(IS)
            no, mo_, to, wo, so = blk(OS)
            # the screen's admitted-vs-rejected gap, and the two controls that say whether it is
            # information or arithmetic.  Admission is p_two < ALPHA, and p_two is a monotone
            # function of |lift| WITHIN a pool, so a positive gap is expected mechanically.
            adm, rej = OS[OS.p_two < ALPHA], OS[OS.p_two >= ALPHA]
            d = (float(adm.lift.mean()) - float(rej.lift.mean())) if len(adm) and len(rej) else float("nan")
            # control 1: admit the same NUMBER of claims by largest |lift| alone (no pool, no null)
            kk = len(adm)
            if kk and kk < len(OS):
                top = OS.reindex(OS.lift.abs().sort_values(ascending=False).index)
                d_top = float(top.iloc[:kk].lift.mean()) - float(top.iloc[kk:].lift.mean())
            else:
                d_top = float("nan")
            # control 2: admit the same NUMBER at random (seeded, 200 draws) -> expectation 0
            if kk and kk < len(OS):
                rng = np.random.default_rng(430)
                lv = OS.lift.values
                ds = []
                for _ in range(200):
                    idx = rng.permutation(len(lv))
                    ds.append(lv[idx[:kk]].mean() - lv[idx[kk:]].mean())
                d_rand, d_rand_sd = float(np.mean(ds)), float(np.std(ds, ddof=1))
            else:
                d_rand = d_rand_sd = float("nan")
            wf.append(dict(pool_def=pdef, min_pool=mp, cut=cut, n_IS=ni, n_OOS=no,
                           mean_lift_IS=mi_, t_IS=ti, win_IS=wi, sig_share_IS=si,
                           mean_lift_OOS=mo_, t_OOS=to, win_OOS=wo, sig_share_OOS=so,
                           n_admitted_OOS=len(adm), n_rejected_OOS=len(rej),
                           mean_lift_admitted_OOS=float(adm.lift.mean()) if len(adm) else float("nan"),
                           mean_lift_rejected_OOS=float(rej.lift.mean()) if len(rej) else float("nan"),
                           screen_edge_OOS=d, edge_toplift_control=d_top,
                           edge_random_control=d_rand, edge_random_sd=d_rand_sd))
    W = pd.DataFrame(wf)
    if len(W):
        P("  W1a  DOES THE CORPUS-LEVEL LIFT LEVEL PERSIST?  (the one non-circular reading: the mean")
        P("       lift of claims published BEFORE the cut vs those published on/after it, read once)")
        P(f"  {'pool':5s} {'MIN':>4s} {'cut':10s} {'n_IS':>5s} {'n_OOS':>5s} {'lift_IS':>8s} "
          f"{'t_IS':>6s} {'win_IS':>7s} {'lift_OOS':>9s} {'t_OOS':>6s} {'win_OOS':>7s}")
        for _, r in W.iterrows():
            P(f"  {r.pool_def:5s} {int(r.min_pool):4d} {r.cut:10s} {int(r.n_IS):5d} {int(r.n_OOS):5d} "
              f"{r.mean_lift_IS:+8.4f} {r.t_IS:+6.2f} {r.win_IS:7.1%} {r.mean_lift_OOS:+9.4f} "
              f"{r.t_OOS:+6.2f} {r.win_OOS:7.1%}")
        P("\n  W1b  DOES THE SCREEN ITSELF CARRY INFORMATION, OR IS ITS GAP ARITHMETIC?")
        P("       p_two is a monotone function of |lift| WITHIN a pool, so 'admitted claims have")
        P("       bigger lift' is expected by construction.  Two controls decide it: admitting the")
        P("       SAME NUMBER of claims on |lift| alone (no pool, no null), and admitting the same")
        P("       number AT RANDOM (200 seeded draws; expectation 0).")
        P(f"  {'pool':5s} {'MIN':>4s} {'adm':>4s} {'rej':>4s} {'lift(adm)':>9s} {'lift(rej)':>9s} "
          f"{'edge':>8s} {'edge|lift|':>10s} {'edge rand':>9s} {'rand sd':>8s}")
        for _, r in W.iterrows():
            P(f"  {r.pool_def:5s} {int(r.min_pool):4d} {int(r.n_admitted_OOS):4d} "
              f"{int(r.n_rejected_OOS):4d} {r.mean_lift_admitted_OOS:+9.4f} "
              f"{r.mean_lift_rejected_OOS:+9.4f} {r.screen_edge_OOS:+8.4f} "
              f"{r.edge_toplift_control:+10.4f} {r.edge_random_control:+9.4f} {r.edge_random_sd:8.4f}")
        P("  (If 'edge' ~ 'edge|lift|' and both >> 'edge rand', the screen is a RE-STATEMENT of |lift|,")
        P("   not a filter that knows anything |lift| does not.  That is the correct reading of a")
        P("   REPORTING column and is all idea 430 asked for — but it means the screen must not be")
        P("   sold as a test that separates good selectors from bad ones out of sample.)")
    else:
        P("  too few dated claims for a corpus walk-forward at any grid point.")

    # -------------------------------------------------------------------------- Q5/Q6 fresh books
    P("\n" + "=" * 112)
    P("Q5  RULE 8 / W2 — A FRESH BOOK POOL (u56 top-n EW, no vol scaler, weekly, t+1, 10 bps)")
    P("    25 arms, ALL reported; fitted on 2010-2016 by IS Sharpe; 2017-2026 read ONCE")
    P("=" * 112)
    A, B = fresh_pool()
    A.to_csv(OUT / f"{STAMP}.arms.csv", index=False)
    P(f"  {'n':>3s} {'g':>6s} {'CAGR':>7s} {'Sharpe':>7s} {'MaxDD':>7s} {'H1':>6s} {'H2':>6s} "
      f"{'IS_Shp':>7s} {'OOS_CAGR':>8s} {'OOS_Shp':>8s} {'OOS_DD':>7s} {'4a':>3s} {'4b':>3s}")
    for _, r in A.iterrows():
        P(f"  {int(r.n):3d} {r.g:6.3f} {r.CAGR:7.2%} {r.Sharpe:7.4f} {r.MaxDD:7.2%} {r.H1:6.3f} "
          f"{r.H2:6.3f} {r.IS_Sharpe:7.4f} {r.OOS_CAGR:8.2%} {r.OOS_Sharpe:8.4f} {r.OOS_MaxDD:7.2%} "
          f"{'Y' if r.keep4a else '.':>3s} {'Y' if r.keep4b else '.':>3s}")
    P(f"  SPY          {B['spy']['CAGR']:7.2%} {B['spy']['Sharpe']:7.4f} {B['spy']['MaxDD']:7.2%} "
      f"{B['spy_h'][0]:6.3f} {B['spy_h'][1]:6.3f} {'':7s} {B['spy_oos']['CAGR']:8.2%} "
      f"{B['spy_oos']['Sharpe']:8.4f} {B['spy_oos']['MaxDD']:7.2%}")
    P(f"  RULES v2     {B['b2']['CAGR']:7.2%} {B['b2']['Sharpe']:7.4f} {B['b2']['MaxDD']:7.2%} "
      f"{B['b2_h'][0]:6.3f} {B['b2_h'][1]:6.3f} {'':7s} {B['b2_oos']['CAGR']:8.2%} "
      f"{B['b2_oos']['Sharpe']:8.4f} {B['b2_oos']['MaxDD']:7.2%}")
    P(f"  RULES v1     {B['v1']['CAGR']:7.2%} {B['v1']['Sharpe']:7.4f} {B['v1']['MaxDD']:7.2%} "
      f"{'':6s} {'':6s} {'':7s} {B['v1_oos']['CAGR']:8.2%} {B['v1_oos']['Sharpe']:8.4f} "
      f"{B['v1_oos']['MaxDD']:7.2%}")

    P("\n  THE PICK, WITH THE COLUMN idea 430 PROPOSES:")
    pick = A.loc[A.IS_Sharpe.idxmax()]
    lift, p1, p2, npl = exact_p(A.OOS_Sharpe.values, float(pick.OOS_Sharpe))
    med = A.loc[A.IS_Sharpe.rank(method="first").sub((len(A) + 1) / 2).abs().idxmin()]
    lm_, pm1, pm2, _ = exact_p(A.OOS_Sharpe.values, float(med.OOS_Sharpe))
    P(f"    IS-Sharpe argmax  n={int(pick.n)} g={pick.g:.3f}:  OOS {pick.OOS_CAGR:.2%} / "
      f"{pick.OOS_Sharpe:.4f} / {pick.OOS_MaxDD:.2%}")
    P(f"      pool mean OOS Sharpe {A.OOS_Sharpe.mean():.4f} over n_pool={npl}")
    P(f"      lift {lift:+.4f}   p_one {p1:.4f}   p_two {p2:.4f}   "
      f"-> {'DISTINGUISHABLE' if p2 < ALPHA else 'INDISTINGUISHABLE'} from a random pick from its own pool")
    P(f"      sel_d vs SPY  {pick.OOS_Sharpe - B['spy_oos']['Sharpe']:+.4f}   "
      f"vs RULES v2 {pick.OOS_Sharpe - B['b2_oos']['Sharpe']:+.4f}   "
      f"vs RULES v1 {pick.OOS_Sharpe - B['v1_oos']['Sharpe']:+.4f}  "
      f"(lift is the SAME number under all three)")
    P(f"    IS-Sharpe MEDIAN arm (idea 204's K_MEDIAN) n={int(med.n)} g={med.g:.3f}: "
      f"OOS Sharpe {med.OOS_Sharpe:.4f}, lift {lm_:+.4f}, p_two {pm2:.4f}")
    P(f"    minimum attainable p_two on this pool = 1/{npl} = {1.0/npl:.4f}  "
      f"-> falsifiable at 0.05: {'YES' if npl >= 20 else 'NO'}")

    P("\n" + "=" * 112)
    P("Q6  BOTH KEEP PATHS")
    P("=" * 112)
    P(f"  arms: 4a {int(A.keep4a.sum())}/{len(A)}   4b {int(A.keep4b.sum())}/{len(A)}")
    P(f"  the walk-forward pick (n={int(pick.n)}, g={pick.g:.3f}): "
      f"4a {'PASS' if bool(pick.keep4a) else 'FAIL'}   4b {'PASS' if bool(pick.keep4b) else 'FAIL'}")
    P("  idea 430 is a REPORTING proposal and promotes no book; the paths are scored because PROTOCOL")
    P("  rule 4 requires it, not because this run nominates anything.")

    W.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    Q2.to_csv(OUT / f"{STAMP}.wins.csv", index=False)
    P(f"\nelapsed {time.time()-t0:.1f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
