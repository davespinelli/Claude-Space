#!/usr/bin/env python3
"""Idea 205 — the POOL MEAN as a required LEADERBOARD column beside every selector claim.

QUESTION (queue 205, following 196 and 204)
    Idea 196 found S2LF beats a RANDOM draw from its own pool by +0.0110 (t +3.78) while STILL
    losing to doing nothing by -0.0032, because the POOL's mean dSharpe is negative.  So "does
    selection help?" conflates two things a reader cannot separate from a published row:
        selector dOOS  =  (pool mean dOOS)   +   (selector's lift over a random pool draw)
                           ^ expectancy of the      ^ actual picking skill
                             instrument itself
    This script (a) states the column, (b) BACK-FILLS it over every selector claim in the record
    whose parent grid CSV survives, and (c) reports how many of the record's selector claims are
    made over a NEGATIVE-expectancy pool.  Idea 204 (the regression form) is still OPEN and unrun;
    its pooled regression falls out of the same table and is reported here as a by-product, flagged
    as such, not as a claim on 204.

THE PROPOSED COLUMN (exact wording proposed for PROTOCOL / LEADERBOARD)
    For any published claim of the form "selector S picked arm a* and its OOS metric beat C":
        pool_mean_dOOS = mean over the pool P that S chose from of (OOS_Sharpe(a) - OOS_Sharpe(C))
        pool_sign      = sign(pool_mean_dOOS)
        lift           = dOOS(a*) - pool_mean_dOOS       (the part that is actually SELECTION)
    Report pool_mean_dOOS and n(P) beside dOOS.  A claim with pool_mean_dOOS < 0 and dOOS < 0 is
    an INSTRUMENT result, not a selector result, and must not be written up as "selection failed".

BACK-FILL MECHANICS (mechanical, no hand-picking)
    A stem qualifies iff it has BOTH
      SELECTOR file  .walkforward.csv / .picks.csv / .choices.csv  — one row per published claim,
                     carrying the pick's own OOS Sharpe AND at least one comparand column, and
      POOL file      .grid.csv / .arms.csv / .ladder.csv / .corpus.csv / .sweep.csv / .cells.csv /
                     .points.csv — the arms the selector chose among, carrying OOS Sharpe.
    Pool membership = pool rows agreeing with the claim row on EVERY shared cell key from a fixed
    allowlist (panel/universe/uni/book/grid/corpus/family/fam/cost/cost_bps/bps/arm/kind/conv/
    dial/gate/mode/gross_mode/cadence/freq/n/g).  Claims with fewer than MIN_POOL pool rows are
    dropped and counted, not silently discarded.

PARAMETERS (2, swept, ALL grid points reported)
    p1  comparand  in {CONTROL, SPY}   — which published comparand the dOOS is taken against
                                          (CONTROL = base_/ctl_/ctrl_/v1_/S0/anchor/incumbent)
    p2  pool_def   in {ALL, LIVE}      — ALL pool rows, vs LIVE only (rows flagged is_null /
                                          apriori / kind in {null,control,ctl} removed)
    MIN_POOL = 3 is a structural admission threshold, pre-set, not swept.

RULE 8 (required) — TWO walk-forwards, both on this run's own new numbers
    W1 CORPUS walk-forward of the PROPOSED SCREEN.  The screen under test is "a selector claim
       whose pool_mean_dOOS < 0 should not be written up as a selector result".  Its content is
       falsifiable: does pool_sign predict claim_sign OUT OF SAMPLE?  Claims are split by parent
       script DATE — IS = the first half of the record's dates, OOS = the second half read once —
       and the IS-fitted sign rule is applied to the OOS claims untouched.
    W2 a LIVE book-level walk-forward that puts the column on a pool built fresh in this run, so
       the proposal is demonstrated on real books and not only on archived CSVs: the KEEP-4b
       candidate's own dial (top-n equal-weight, no vol scaler, weekly, u56) x a gross ladder,
       every arm reported with 4a and 4b, an IS-Sharpe selector picking on 2010-2016 and 2017-2026
       read once against SPY, RULES v2 and the do-nothing control -- reported WITH the new column.

Outputs (committed): .console.txt .claims.csv .stems.csv .census.csv .walkforward.csv
                     .livepool.csv .result.md
Deterministic; no network.
"""
import sys, re, time, glob, gzip, math
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics  # noqa

STAMP = "2026-09-08_the-pool-mean-as-a-leaderboard-column_cloud"
OUT = Path(__file__).resolve().parent
MIN_POOL = 3
IS_END, OOS_START = "2016-12-31", "2017-01-01"

_LOG: list[str] = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); _LOG.append(s)


# ------------------------------------------------------------------ file discovery
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
    return pd.read_csv(p, compression="gzip" if str(p).endswith(".gz") else None,
                       low_memory=False)

def own_oos_col(cols):
    for c in OWN_OOS:
        for k in cols:
            if k == c: return k
    return None

def comparand_cols(cols):
    """{'CONTROL': col, 'SPY': col} — comparand OOS-Sharpe columns published in the sel file."""
    out = {}
    for k in cols:
        kl = k.lower()
        if "sharpe" not in kl or "oos" not in kl: continue
        if k in OWN_OOS: continue
        if SPY_PAT.match(k) and "SPY" not in out: out["SPY"] = k
        elif CTRL_PAT.match(k) and "CONTROL" not in out: out["CONTROL"] = k
    return out

def live_mask(pool):
    """p2 = LIVE: drop pool rows the record itself marks as null / control arms."""
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


# ==================================================================================== census
def build_census():
    stems = {}
    for f in sorted(glob.glob(str(OUT / "*.csv"))) + sorted(glob.glob(str(OUT / "*.csv.gz"))):
        b = Path(f).name
        b = b[:-3] if b.endswith(".gz") else b
        m = re.match(r"(.+?)\.([A-Za-z0-9_]+)\.csv$", b)
        if not m: continue
        stems.setdefault(m.group(1), {})["." + m.group(2) + ".csv"] = f

    claims, stem_rows = [], []
    for stem, d in sorted(stems.items()):
        sel_f = next((d[s] for s in SEL_SUF if s in d), None)
        pool_f = next((d[s] for s in POOL_SUF if s in d), None)
        st = dict(stem=stem, sel=Path(sel_f).name.split(".")[-2] if sel_f else "",
                  pool=Path(pool_f).name.split(".")[-2] if pool_f else "",
                  status="", n_claims=0, n_dropped_thin=0)
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
                if pl is None or len(pl) < MIN_POOL:
                    if pdef == "ALL": nd += 1
                    continue
                pm = float(pl[po].mean()); pmed = float(pl[po].median()); npl = int(len(pl))
                for cname, ccol in comp.items():
                    cv = pd.to_numeric(pd.Series([r[ccol]]), errors="coerce").iloc[0]
                    if not np.isfinite(cv): continue
                    claims.append(dict(
                        stem=stem, comparand=cname, pool_def=pdef, n_pool=npl,
                        sel_OOS_Sharpe=float(own), comparand_OOS_Sharpe=float(cv),
                        sel_dOOS=float(own) - float(cv),
                        pool_mean_dOOS=pm - float(cv), pool_median_dOOS=pmed - float(cv),
                        lift=(float(own) - float(cv)) - (pm - float(cv)),
                        selector=str(r.get("selector", r.get("sel", ""))),
                        date=stem[:10]))
                    nc += 1
        st.update(status="OK" if nc else "no usable claim rows", n_claims=nc, n_dropped_thin=nd)
        stem_rows.append(st)
    return pd.DataFrame(claims), pd.DataFrame(stem_rows)


# ==================================================================================== live pool
def live_pool_demo():
    """W2 — build a pool fresh so the column is demonstrated on real books, with 4a/4b."""
    px = load_universe()
    spy = px["SPY"].pct_change().fillna(0)
    COST, FREQ = 10.0, "W"

    def topn_ew(n, g, vol_scale=False):
        def f(p):
            s, above, vol20 = score(p, vol_scale=vol_scale)
            elig = s.where(above)
            rank = elig.rank(axis=1, ascending=False)
            m = (rank <= n)
            cnt = m.sum(axis=1).replace(0, np.nan)
            return (g * m.astype(float)).div(cnt, axis=0).fillna(0.0)
        return f

    start = px.index[260]
    b2 = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
    v1 = backtest(px, rules_v1_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
    spy = spy.loc[start:]

    def halves(r):
        h = len(r) // 2
        return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]

    rows, rets = [], {}
    NS, GS = [10, 15, 20, 25, 30], [0.50, 0.625, 0.75, 0.875, 1.00]
    for n in NS:
        for g in GS:
            r = backtest(px, topn_ew(n, g)(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
            rets[(n, g)] = r
            m, mi, mo = metrics(r), metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
            h1, h2 = halves(r); s1, s2 = halves(spy)
            ms, mso = metrics(spy), metrics(spy.loc[OOS_START:])
            mb1, mb2 = halves(b2)
            rows.append(dict(
                n=n, g=g, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                IS_Sharpe=mi["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                OOS_MaxDD=mo["MaxDD"],
                keep4a=bool(h1 > mb1 and h2 > mb2 and m["MaxDD"] >= metrics(b2)["MaxDD"]),
                keep4b=bool(h1 > s1 and h2 > s2 and mo["Sharpe"] > mso["Sharpe"]
                            and m["MaxDD"] >= 0.60 * ms["MaxDD"]
                            and m["CAGR"] >= 0.70 * ms["CAGR"])))
    return pd.DataFrame(rows), rets, spy, b2, v1, px, start


# ==================================================================================== run
def main():
    t0 = time.time()
    P("=" * 112)
    P("IDEA 205 — the POOL MEAN as a required LEADERBOARD column beside every selector claim")
    P("  parameters: p1 comparand in {CONTROL, SPY};  p2 pool_def in {ALL, LIVE}. All 4 reported.")
    P(f"  structural: MIN_POOL = {MIN_POOL} pool rows per claim (pre-set, not swept)")
    P("  NOTE idea 204 (the regression form) is still OPEN and UNRUN; its pooled regression is")
    P("       reported below as a BY-PRODUCT of the same table, not as a verdict on 204.")
    P("=" * 112)

    C, S = build_census()
    C.to_csv(OUT / f"{STAMP}.claims.csv", index=False)
    S.to_csv(OUT / f"{STAMP}.stems.csv", index=False)

    P(f"\nCORPUS  {len(S)} script stems in research/backtests/")
    for st, k in S.status.value_counts().items():
        P(f"  {k:5d}  {st}")
    ok = S[S.status == "OK"]
    P(f"  -> {len(ok)} stems yield {len(C)} (claim x comparand x pool_def) rows; "
      f"{int(S.n_dropped_thin.sum())} claim rows dropped for pool < {MIN_POOL}")
    if not len(C):
        P("NO CLAIMS RECOVERED — census aborted."); return
    P(f"  distinct parent dates {C.date.nunique()} ({C.date.min()} .. {C.date.max()})")

    # ---------------------------------------------------------------- Q1 the census
    P("\n" + "=" * 112)
    P("Q1  HOW MANY SELECTOR CLAIMS ARE MADE OVER A NEGATIVE-EXPECTANCY POOL?  (all 4 grid points)")
    P("=" * 112)
    cen = []
    P(f"  {'comparand':10s} {'pool':5s} {'n_claims':>8s} {'n_stems':>7s} "
      f"{'pool<0':>8s} {'share':>7s} {'sel<0':>7s} {'both<0':>7s} "
      f"{'mean pool':>9s} {'mean sel':>9s} {'mean lift':>9s} {'t(lift)':>8s}")
    for comp in ("CONTROL", "SPY"):
        for pdef in ("ALL", "LIVE"):
            s = C[(C.comparand == comp) & (C.pool_def == pdef)]
            if not len(s): continue
            neg = int((s.pool_mean_dOOS < 0).sum()); sneg = int((s.sel_dOOS < 0).sum())
            both = int(((s.pool_mean_dOOS < 0) & (s.sel_dOOS < 0)).sum())
            lf = s.lift.values
            t = float(lf.mean() / (lf.std(ddof=1) / np.sqrt(len(lf)))) if len(lf) > 1 and lf.std() > 0 else 0.0
            cen.append(dict(comparand=comp, pool_def=pdef, n_claims=len(s), n_stems=s.stem.nunique(),
                            n_pool_negative=neg, share_pool_negative=neg / len(s),
                            n_sel_negative=sneg, n_both_negative=both,
                            mean_pool_dOOS=float(s.pool_mean_dOOS.mean()),
                            mean_sel_dOOS=float(s.sel_dOOS.mean()),
                            mean_lift=float(lf.mean()), t_lift=t,
                            median_n_pool=float(s.n_pool.median())))
            P(f"  {comp:10s} {pdef:5s} {len(s):8d} {s.stem.nunique():7d} {neg:8d} "
              f"{neg/len(s):7.1%} {sneg:7d} {both:7d} {s.pool_mean_dOOS.mean():+9.4f} "
              f"{s.sel_dOOS.mean():+9.4f} {lf.mean():+9.4f} {t:+8.2f}")
    CEN = pd.DataFrame(cen)
    CEN.to_csv(OUT / f"{STAMP}.census.csv", index=False)

    P("\n  SIGN AGREEMENT — does the pool's sign predict the claim's sign?")
    P(f"  {'comparand':10s} {'pool':5s} {'agree':>7s} {'rate':>7s} "
      f"{'P(sel<0|pool<0)':>16s} {'P(sel<0|pool>=0)':>17s} {'lift explains':>13s}")
    for comp in ("CONTROL", "SPY"):
        for pdef in ("ALL", "LIVE"):
            s = C[(C.comparand == comp) & (C.pool_def == pdef)]
            if not len(s): continue
            ag = int((np.sign(s.pool_mean_dOOS) == np.sign(s.sel_dOOS)).sum())
            a = s[s.pool_mean_dOOS < 0]; b = s[s.pool_mean_dOOS >= 0]
            pa = (a.sel_dOOS < 0).mean() if len(a) else float("nan")
            pb = (b.sel_dOOS < 0).mean() if len(b) else float("nan")
            share = float(np.abs(s.pool_mean_dOOS).sum() /
                          max(np.abs(s.pool_mean_dOOS).sum() + np.abs(s.lift).sum(), 1e-12))
            P(f"  {comp:10s} {pdef:5s} {ag:7d} {ag/len(s):7.1%} {pa:16.1%} {pb:17.1%} "
              f"{share:13.1%}")
    P("  ('lift explains' = |pool| / (|pool| + |lift|): how much of a claim's magnitude is the")
    P("   instrument's own expectancy rather than picking skill.)")

    # ---------------------------------------------------------------- Q2 204 by-product
    P("\n" + "=" * 112)
    P("Q2  BY-PRODUCT (idea 204's form, reported not adjudicated): sel_dOOS ~ a + b * pool_mean")
    P("=" * 112)
    P(f"  {'comparand':10s} {'pool':5s} {'a':>9s} {'b':>8s} {'t(b)':>7s} {'R2':>7s} "
      f"{'t(a)':>7s}  (a = mean lift at a zero-expectancy pool)")
    for comp in ("CONTROL", "SPY"):
        for pdef in ("ALL", "LIVE"):
            s = C[(C.comparand == comp) & (C.pool_def == pdef)]
            if len(s) < 5: continue
            x, y = s.pool_mean_dOOS.values, s.sel_dOOS.values
            X = np.column_stack([np.ones_like(x), x])
            beta, *_ = np.linalg.lstsq(X, y, rcond=None)
            resid = y - X @ beta
            dof = max(len(y) - 2, 1)
            s2 = float(resid @ resid / dof)
            cov = s2 * np.linalg.pinv(X.T @ X)
            se = np.sqrt(np.diag(cov))
            r2 = 1 - float(resid @ resid) / max(float(((y - y.mean()) ** 2).sum()), 1e-12)
            P(f"  {comp:10s} {pdef:5s} {beta[0]:+9.4f} {beta[1]:+8.4f} "
              f"{beta[1]/max(se[1],1e-12):+7.2f} {r2:7.3f} {beta[0]/max(se[0],1e-12):+7.2f}")
    P("  Books inside one stem are overlapping draws from one pool, so these pooled t-stats")
    P("  OVERSTATE significance; per-stem numbers are in .claims.csv.  This settles nothing on 204.")

    # ---------------------------------------------------------------- Q3 rule 8 W1
    P("\n" + "=" * 112)
    P("Q3  RULE 8 / W1 — corpus walk-forward of the proposed screen (split by parent script DATE)")
    P("    IS = earlier half of dates (rule fitted), OOS = later half read ONCE.")
    P("=" * 112)
    dates = sorted(C.date.unique())
    cut = dates[len(dates) // 2]
    P(f"  {len(dates)} distinct parent dates; IS = dates < {cut}, OOS = dates >= {cut}")
    wf = []
    P(f"  {'comparand':10s} {'pool':5s} {'nIS':>5s} {'nOOS':>5s} | "
      f"{'IS agree':>8s} {'OOS agree':>9s} | {'IS P(sel<0|pool<0)':>18s} {'OOS same':>9s} | "
      f"{'IS b':>7s} {'OOS b':>7s}")
    for comp in ("CONTROL", "SPY"):
        for pdef in ("ALL", "LIVE"):
            s = C[(C.comparand == comp) & (C.pool_def == pdef)]
            a, b = s[s.date < cut], s[s.date >= cut]
            if len(a) < 5 or len(b) < 5: continue
            def agree(z): return float((np.sign(z.pool_mean_dOOS) == np.sign(z.sel_dOOS)).mean())
            def cond(z):
                q = z[z.pool_mean_dOOS < 0]
                return float((q.sel_dOOS < 0).mean()) if len(q) else float("nan")
            def slope(z):
                x, y = z.pool_mean_dOOS.values, z.sel_dOOS.values
                X = np.column_stack([np.ones_like(x), x])
                return float(np.linalg.lstsq(X, y, rcond=None)[0][1])
            wf.append(dict(comparand=comp, pool_def=pdef, n_IS=len(a), n_OOS=len(b),
                           IS_agree=agree(a), OOS_agree=agree(b),
                           IS_cond=cond(a), OOS_cond=cond(b),
                           IS_slope=slope(a), OOS_slope=slope(b)))
            P(f"  {comp:10s} {pdef:5s} {len(a):5d} {len(b):5d} | {agree(a):8.1%} {agree(b):9.1%} "
              f"| {cond(a):18.1%} {cond(b):9.1%} | {slope(a):+7.3f} {slope(b):+7.3f}")
    pd.DataFrame(wf).to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)

    # ---------------------------------------------------------------- Q4 rule 8 W2 live
    P("\n" + "=" * 112)
    P("Q4  RULE 8 / W2 — a LIVE pool built fresh this run (u56, top-n EW no vol scaler, weekly,")
    P("    10 bps, t+1), so the column is demonstrated on real books.  ALL 25 grid points.")
    P("=" * 112)
    G, rets, spy, b2, v1, px, start = live_pool_demo()
    G.to_csv(OUT / f"{STAMP}.livepool.csv", index=False)
    ms, mso = metrics(spy), metrics(spy.loc[OOS_START:])
    mb, mbo = metrics(b2), metrics(b2.loc[OOS_START:])
    mv, mvo = metrics(v1), metrics(v1.loc[OOS_START:])
    P(f"  references (from {start.date()}):")
    for nm, m, mo in (("SPY", ms, mso), ("RULES v2 (live)", mb, mbo), ("RULES v1", mv, mvo)):
        P(f"    {nm:16s} CAGR {m['CAGR']:7.2%} Sharpe {m['Sharpe']:6.3f} MaxDD {m['MaxDD']:7.2%}"
          f" | OOS CAGR {mo['CAGR']:7.2%} Sharpe {mo['Sharpe']:6.3f} MaxDD {mo['MaxDD']:7.2%}")
    P(f"\n  {'n':>3s} {'g':>6s} {'CAGR':>7s} {'Sharpe':>7s} {'MaxDD':>7s} {'H1':>6s} {'H2':>6s} "
      f"{'IS Sh':>6s} {'OOSCAGR':>8s} {'OOS Sh':>7s} {'OOS DD':>7s} {'4a':>5s} {'4b':>5s}")
    for _, r in G.iterrows():
        P(f"  {int(r.n):3d} {r.g:6.3f} {r.CAGR:7.2%} {r.Sharpe:7.3f} {r.MaxDD:7.2%} {r.H1:6.3f} "
          f"{r.H2:6.3f} {r.IS_Sharpe:6.3f} {r.OOS_CAGR:8.2%} {r.OOS_Sharpe:7.3f} "
          f"{r.OOS_MaxDD:7.2%} {str(bool(r.keep4a)):>5s} {str(bool(r.keep4b)):>5s}")
    P(f"\n  KEEP paths over the live pool: 4a {int(G.keep4a.sum())}/{len(G)}, "
      f"4b {int(G.keep4b.sum())}/{len(G)}")

    pick = G.loc[G.IS_Sharpe.idxmax()]
    ctl_key = (20, 0.75)                      # the standing KEEP-4b candidate = do-nothing control
    ctl = G[(G.n == ctl_key[0]) & (G.g == ctl_key[1])].iloc[0]
    for cname, cv, cvc, cvd in (("do-nothing (n=20,g=0.75)", ctl.OOS_Sharpe, ctl.OOS_CAGR, ctl.OOS_MaxDD),
                                ("SPY", mso["Sharpe"], mso["CAGR"], mso["MaxDD"]),
                                ("RULES v2", mbo["Sharpe"], mbo["CAGR"], mbo["MaxDD"])):
        pm = float(G.OOS_Sharpe.mean()) - cv
        P(f"\n  vs {cname}:")
        P(f"    IS-Sharpe pick        n={int(pick.n)} g={pick.g:.3f}  "
          f"OOS CAGR {pick.OOS_CAGR:7.2%}  Sharpe {pick.OOS_Sharpe:6.3f}  MaxDD {pick.OOS_MaxDD:7.2%}")
        P(f"    comparand                         OOS CAGR {cvc:7.2%}  Sharpe {cv:6.3f}  "
          f"MaxDD {cvd:7.2%}")
        P(f"    sel_dOOS        {pick.OOS_Sharpe - cv:+7.4f}")
        P(f"    POOL_MEAN_dOOS  {pm:+7.4f}   (n_pool = {len(G)})   <-- THE PROPOSED COLUMN")
        P(f"    lift            {(pick.OOS_Sharpe - cv) - pm:+7.4f}   "
          f"({'skill' if (pick.OOS_Sharpe-cv)-pm > 0 else 'no skill'} inside a "
          f"{'NEGATIVE' if pm < 0 else 'POSITIVE'}-expectancy pool)")

    P("\n" + "=" * 112)
    P("PROPOSED PROTOCOL CLAUSE (wording; NOT applied — RULES.md/PROTOCOL.md untouched by this run)")
    P("=" * 112)
    P("  PROTOCOL 10.  Any published claim that an IS selector's OOS result beats a comparand C")
    P("  MUST report, in the same row: n(pool), pool_mean_dOOS = mean over the pool of")
    P("  (OOS_Sharpe(arm) - OOS_Sharpe(C)), and lift = dOOS(pick) - pool_mean_dOOS.  A claim with")
    P("  pool_mean_dOOS < 0 is reported as an INSTRUMENT result; only `lift` may be described as")
    P("  selection.  LEADERBOARD gains one column: `pool_mean_dOOS (n_pool)`.")

    P(f"\nDONE in {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
