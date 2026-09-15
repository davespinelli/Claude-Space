#!/usr/bin/env python3
"""QUEUE idea 867 — is-the-4b-DD-CAP-just-a-BETA-CAP   (cloud lane, 2026-09-15).

QUESTION (pre-registered, verbatim from QUEUE.md idea 867)
    "ideas 662, 866 and 676 each found de-grossing buys drawdown and pays CAGR, so the DD leg may
     be a monotone read of realised beta and nothing else; regress every shelf book's MaxDD on
     its own SPY beta and report the residual.  Max 2 params (beta estimator, panel)."

WHY IT MATTERS FOR CAPITAL.  PROTOCOL 4b's drawdown leg (MaxDD <= 60% of SPY's) is meant to be a
risk test a book has to EARN.  If MaxDD is an affine function of realised SPY beta with a small
residual, then the leg is satisfied by holding less of the market, nothing more — any book can
clear it by de-grossing, and the leg is carrying no information about the book's construction.
That is exactly the shape ideas 662/866/676 kept running into.  The question this run answers is
NOT "is MaxDD correlated with beta" (it obviously is) but "is the RESIDUAL big enough for the DD
cap to separate books at MATCHED beta" — and, for capital, "does a pure beta cap, fitted in
sample, reach a book that clears 4b out of sample".

THE SHELF (built mechanically; no book is hand-picked)
    Every book is: top-k of the eligible names by a family statistic, equal weight gross/k,
    shortfall to CASH and NEVER respread, monthly rebalance, fills t+1, 10 bps.
      family  MOM     baseline.score(px, vol_scale=False) — the 2026-09-04 shelf KEEP's signal
              MOMVS   baseline.score(px, vol_scale=True)  — RULES v1's signal
              MADIST  px / 200d MA - 1
              LOWVOL  -vol20  (the family a priori expected to sit at low beta)
      width   k in {5, 10, 20, 40, ALL}  (ALL = every eligible name that day)
      gross   g in {0.25, 0.50, 0.75, 1.00}   <- the de-grossing axis the idea names
      gate    close > 200d MA AND vol20 < 0.60, AND a non-NaN family statistic
    plus two REFERENCE books that are not on the grid: RULES v1 (baseline.rules_v1_weights,
    weekly) and RULES v2 (baseline.rules_v2_weights, weekly — the LIVE book).
    Shelf size per panel: 4 x 5 x 4 = 80 grid books + 2 reference books = 82.

THE TWO TUNED PARAMETERS (the only two; EVERY value of both is reported)
    P1  BETA ESTIMATOR   OLSD    daily OLS beta, cov(r, spy) / var(spy), full window
                         OLSM    the same on 21-day NON-OVERLAPPING compounded returns
                                 (a lower-frequency beta; immune to the daily-fill artefact)
                         DOWN    downside beta: the same daily OLS restricted to days on which
                                 SPY's return is negative.  Drawdown is a downside object, so
                                 this is the estimator most favourable to the idea's hypothesis.
    P2  PANEL            U56 (research/universe.json), B136 (broad=True),
                         SMALL (small=True, max_1d_move >= 1.0 dropped FIRST)

THE HYPOTHESES, written out in full BEFORE any number below was read
    H_AFFINE   MaxDD is an affine read of beta: OLS of MaxDD on beta across the shelf gives
               R^2 >= 0.90 on at least one (estimator, panel) block.
    H_CAP      the 4b DD cap IS a beta cap: there is a beta threshold b* whose pass/fail
               classification of the shelf agrees with the DD cap's on >= 95% of books, in
               every block.  (If the DD leg is nothing but a beta cap, agreement is ~100%.)
    H_RESID    the residual is immaterial for capital: no book clears the DD cap while carrying
               a beta ABOVE the median beta of the books that fail it (i.e. no book buys the DD
               cap with construction rather than with de-grossing).
    H_REACH    (the capital question, rule 8)  a pure IS-fitted BETA CAP selector — pick the
               highest IS-Sharpe book whose IS beta is under b*_IS — reaches a book that clears
               4b OUT OF SAMPLE.
    Declared before running: H_REACH decides the verdict.  H_CAP decides whether the record's
    DD leg should be restated.

PROTOCOL rule 8 walk-forward (required, read ONCE)
    IS = start-of-sample .. 2016-12-31, OOS = 2017-01-01 .. end, on every panel.
    Betas, the regression, and b* are fitted on IS ONLY.  THREE IS-only selectors:
        PICK-BETA     highest IS Sharpe among books whose IS beta <= b*_IS, where b*_IS is the
                      beta threshold that best reproduces the IS DD cap (the beta-cap idea,
                      taken at its word).
        PICK-DDIS     highest IS Sharpe among books that clear the IS DD cap directly
                      (the control: the leg itself, not its beta proxy).
        PICK-SHARPE   highest IS Sharpe, unconstrained (the do-nothing control).
    Each pick is read ONCE on OOS against SPY (4b) and RULES v2 live (4a).

BOTH KEEP PATHS are evaluated on every shelf book, full sample, both halves, and again on OOS:
    4a  Sharpe > RULES v2 live in BOTH halves AND MaxDD no worse than v2's.
    4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

GATES, printed before any hypothesis is read
    G1  beta is monotone in gross at fixed (family, k): halving gross must not raise beta.
        This is the mechanical check that the de-grossing axis does what the idea assumes.
    G2  a 100% SPY book priced through the same engine reads beta 1.000 +/- 0.01 on all three
        estimators and reproduces SPY's own MaxDD to within 0.5 pp (the estimator calibration).
    G3  the U56 MOM k=20 g=0.65 book reproduces the record's committed shelf triple
        (12.69% / 1.201 / -17.11%, idea 879's memo) to 0.05 pp / 0.02, using the record's own
        rank(ascending=False) <= k cut.  This pins this run's book construction to the record's.
    G4  the three beta estimators are not the same number: max |OLSD - DOWN| across the shelf
        is reported, so no claim below can be read as estimator-free.

CAVEATS carried, not buried
    * SURVIVORSHIP.  U56 / B136 / SMALL are CURRENT-constituent lists (SMALL additionally drops
      the 52 tickers with max_1d_move >= 1.0 per data/small_meta.csv), so every CAGR and every
      MaxDD LEVEL below is optimistic and both 4b level bars are easier here than on a
      point-in-time panel.  This run's headline is a REGRESSION ACROSS BOOKS measured on the
      same days and the same names, which is far less exposed than any level — but the 4b
      pass/fail counts and the OOS triples ARE levels and must be read as upper bounds.
    * beta and MaxDD are both realised, full-window statistics of the SAME return series, so the
      regression is descriptive, not predictive.  The rule-8 section is the only place anything
      is asked to walk forward, and it is read once.
    * 2020 and 2022 are the only real stress episodes in the sample, so MaxDD here is close to a
      two-event statistic and the DD cap is close to a statement about those two episodes.
    * SMALL starts 2010-01-04; its IS window is one year shorter than U56/B136's.
    * Rule 6: nothing here is a rules change.  A rules change is a Sunday-review decision.

Deterministic, standalone, no network.  Writes only its own CSVs under research/backtests/out/.
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v1_weights, rules_v2_weights   # noqa: E402
from engine import backtest, metrics                                            # noqa: E402

SLUG = "2026-09-15_is-the-4b-DD-CAP-just-a-BETA-CAP_cloud"
OUTDIR = ROOT / "research" / "backtests" / "out"
OUTDIR.mkdir(exist_ok=True)
pd.set_option("display.width", 250)
pd.set_option("display.max_rows", 500)

FAMILIES = ["MOM", "MOMVS", "MADIST", "LOWVOL"]
WIDTHS = [5, 10, 20, 40, "ALL"]
GROSSES = [0.25, 0.50, 0.75, 1.00]
ESTIMATORS = ["OLSD", "OLSM", "DOWN"]
PANELS = ["U56", "B136", "SMALL"]
COST, MAX_VOL, WARMUP = 10, 0.60, 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"


def log(*a):
    print(*a, flush=True)


# ---------------------------------------------------------------- panel / signals
def panel(name):
    if name == "U56":
        return load_universe()
    if name == "B136":
        return load_universe(broad=True)
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    log(f"  SMALL: {px.shape[1]} columns -> {len(keep)} kept "
        f"({px.shape[1] - len(keep)} dropped for max_1d_move >= 1.0)")
    return px[keep]


def candidates(pname, px):
    """SPY is a listed constituent of universe.json and universe_broad.json (so the record's
    books can hold it) but on SMALL it is a joined benchmark column only."""
    return list(px.columns) if pname in ("U56", "B136") else [c for c in px.columns if c != "SPY"]


def signals(px, cols):
    p = px[cols]
    comp_ns, above, vol20 = score(p, vol_scale=False)
    comp_vs, _, _ = score(p, vol_scale=True)
    gate = above & (vol20 < MAX_VOL) & p.notna()
    sig = dict(MOM=comp_ns, MOMVS=comp_vs, MADIST=p / p.rolling(200).mean() - 1.0, LOWVOL=-vol20)
    return sig, {f: gate & sig[f].notna() for f in sig}


def month_end(idx):
    s = pd.Series(idx.to_period("M"), index=idx)
    return idx[(s != s.shift(-1)).values]


def book(sig, elig, rebal, k, gross, index, cols, rank_cut=False):
    """Top-k of the eligible names, gross/k each, shortfall to CASH, never respread.

    rank_cut=True uses the record's own pandas rank(ascending=False) <= k cut (gate G3);
    otherwise a strict descending sort, which is what a width ladder needs.
    """
    e = sig.where(elig)
    if k == "ALL":
        n = elig.sum(axis=1).replace(0, np.nan)
        W = elig.astype(float).div(n, axis=0).fillna(0.0) * gross
        return W.reindex(rebal).reindex(index).ffill().fillna(0.0)
    if rank_cut:
        W = (e.rank(axis=1, ascending=False) <= k).astype(float) * (gross / k)
        return W.reindex(rebal).reindex(index).ffill().fillna(0.0)
    W = pd.DataFrame(0.0, index=rebal, columns=cols)
    er = e.reindex(rebal)
    for d in rebal:
        row = er.loc[d].dropna()
        if len(row):
            W.loc[d, row.sort_values(ascending=False).index[:k]] = gross / k
    return W.reindex(index).ffill().fillna(0.0)


# ---------------------------------------------------------------- beta estimators
def beta(r, spy, kind):
    if kind == "DOWN":
        m = spy < 0
        r, spy = r[m], spy[m]
    elif kind == "OLSM":
        g = np.arange(len(r)) // 21
        r = (1 + r).groupby(g).prod() - 1
        spy = (1 + spy).groupby(g).prod() - 1
    v = float(spy.var())
    return float(np.cov(r, spy)[0, 1] / v) if v > 0 else np.nan


# ---------------------------------------------------------------- 4b / 4a
def legs(r, spy):
    a, s = metrics(r), metrics(spy)
    h = len(r) // 2
    a1, a2 = metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]
    s1, s2 = metrics(spy.iloc[:h])["Sharpe"], metrics(spy.iloc[h:])["Sharpe"]
    return dict(CAGR=a["CAGR"], Sharpe=a["Sharpe"], MaxDD=a["MaxDD"], H1=a1, H2=a2,
                spyCAGR=s["CAGR"], spyMaxDD=s["MaxDD"],
                h1_ok=bool(a1 > s1), h2_ok=bool(a2 > s2),
                dd_ok=bool(a["MaxDD"] >= 0.60 * s["MaxDD"]),
                cagr_ok=bool(a["CAGR"] >= 0.70 * s["CAGR"]))


def four_b(L):
    return L["h1_ok"] and L["h2_ok"] and L["dd_ok"] and L["cagr_ok"]


def four_a(r, base):
    h = len(r) // 2
    return bool(metrics(r.iloc[:h])["Sharpe"] > metrics(base.iloc[:h])["Sharpe"]
                and metrics(r.iloc[h:])["Sharpe"] > metrics(base.iloc[h:])["Sharpe"]
                and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def best_threshold(betas, dd_ok):
    """The beta threshold b* whose 'beta <= b*' rule best reproduces the DD-cap labels.

    Reported with its agreement rate; ties broken by the smaller threshold.
    """
    cand = sorted(set(np.round(betas, 4)))
    best = (None, -1.0)
    for b in cand:
        agree = float(((np.asarray(betas) <= b) == np.asarray(dd_ok)).mean())
        if agree > best[1]:
            best = (b, agree)
    return best


# ================================================================ build the shelf
log("=" * 112)
log("GATES (printed before any hypothesis is read)")
log("=" * 112)

SHELF, DATA = [], {}
for pname in PANELS:
    px = panel(pname)
    cols = candidates(pname, px)
    sig, elig = signals(px, cols)
    rebal = month_end(px.index)
    start = px.index[WARMUP]
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    base = backtest(px, rules_v2_weights(px[cols]).reindex(columns=px.columns).fillna(0.0),
                    cost_bps=COST, freq="W")["returns"].loc[start:]
    v1 = backtest(px, rules_v1_weights(px[cols]).reindex(columns=px.columns).fillna(0.0),
                  cost_bps=COST, freq="W")["returns"].loc[start:]
    DATA[pname] = dict(px=px, cols=cols, sig=sig, elig=elig, rebal=rebal, start=start,
                       spy=spy, base=base, v1=v1)
    log(f"\n[{pname}] {px.shape[0]} days x {len(cols)} candidates "
        f"(SPY {'IS' if 'SPY' in cols else 'is NOT'} a candidate), "
        f"{px.index[0].date()}..{px.index[-1].date()}, {len(rebal)} monthly rebalances, "
        f"metrics from {start.date()}")

    for fam in FAMILIES:
        for k in WIDTHS:
            W = book(sig[fam], elig[fam], rebal, k, 1.0, px.index, cols)
            W = W.reindex(columns=px.columns).fillna(0.0)
            for g in GROSSES:
                r = backtest(px, W * g, cost_bps=COST, freq="M")["returns"].loc[start:]
                SHELF.append(dict(panel=pname, book=f"{fam}/k={k}/g={g}", family=fam,
                                  k=str(k), gross=g, r=r))
    for nm, r in (("RULES v1", DATA[pname]["v1"]), ("RULES v2 (live)", base)):
        SHELF.append(dict(panel=pname, book=nm, family="REFERENCE", k="-", gross=np.nan, r=r))
    log(f"  shelf: {len([s for s in SHELF if s['panel']==pname])} books priced")

# ---------------------------------------------------------------- gates
rows = []
for s in SHELF:
    d = DATA[s["panel"]]
    r, spy = s["r"], d["spy"]
    L = legs(r, spy)
    Lis, Loos = legs(r.loc[:IS_END], spy.loc[:IS_END]), legs(r.loc[OOS_START:], spy.loc[OOS_START:])
    row = dict(panel=s["panel"], book=s["book"], family=s["family"], k=s["k"], gross=s["gross"],
               CAGR=L["CAGR"], Sharpe=L["Sharpe"], MaxDD=L["MaxDD"], H1=L["H1"], H2=L["H2"],
               dd_ok=L["dd_ok"], cagr_ok=L["cagr_ok"], h1=L["h1_ok"], h2=L["h2_ok"],
               KEEP4b=four_b(L), KEEP4a=four_a(r, d["base"]),
               is_Sharpe=Lis["Sharpe"], is_MaxDD=Lis["MaxDD"], is_dd_ok=Lis["dd_ok"],
               oos_CAGR=Loos["CAGR"], oos_Sharpe=Loos["Sharpe"], oos_MaxDD=Loos["MaxDD"],
               oos_dd=Loos["dd_ok"], oos_cagr=Loos["cagr_ok"], oos_h1=Loos["h1_ok"],
               oos_h2=Loos["h2_ok"], oos_4b=four_b(Loos))
    for e in ESTIMATORS:
        row[f"beta_{e}"] = beta(r, spy, e)
        row[f"isbeta_{e}"] = beta(r.loc[:IS_END], spy.loc[:IS_END], e)
    rows.append(row)
SH = pd.DataFrame(rows)
SH.to_csv(OUTDIR / f"{SLUG}.shelf.csv", index=False)

# G1 beta monotone in gross
GRID = SH[SH.family != "REFERENCE"]
g1_bad, g1_tot = 0, 0
for (pn, fam, k), b in GRID.groupby(["panel", "family", "k"]):
    b = b.sort_values("gross")
    for e in ESTIMATORS:
        g1_tot += 1
        if not (b[f"beta_{e}"].diff().dropna() >= -1e-9).all():
            g1_bad += 1
log(f"\n  G1 beta non-decreasing in gross at fixed (family, k), all estimators: "
    f"{'PASS' if g1_bad == 0 else 'FAIL'} ({g1_tot - g1_bad} of {g1_tot} blocks monotone)")

# G2 SPY-through-the-engine calibration
d = DATA["U56"]
Wspy = pd.DataFrame(0.0, index=d["px"].index, columns=d["px"].columns)
Wspy["SPY"] = 1.0
r_spy_book = backtest(d["px"], Wspy, cost_bps=0, freq="M")["returns"].loc[d["start"]:]
bs = {e: beta(r_spy_book, d["spy"], e) for e in ESTIMATORS}
dd_gap = abs(metrics(r_spy_book)["MaxDD"] - metrics(d["spy"])["MaxDD"])
g2 = all(abs(v - 1.0) < 0.01 for v in bs.values()) and dd_gap < 0.005
log(f"  G2 100% SPY book through the engine: beta " +
    ", ".join(f"{e} {bs[e]:.4f}" for e in ESTIMATORS) +
    f"; MaxDD gap {100*dd_gap:.3f} pp  -> {'PASS' if g2 else 'FAIL'}")

# G3 record reproduction
W65 = book(d["sig"]["MOM"], d["elig"]["MOM"], d["rebal"], 20, 0.65, d["px"].index, d["cols"],
           rank_cut=True).reindex(columns=d["px"].columns).fillna(0.0)
m3 = metrics(backtest(d["px"], W65, cost_bps=10, freq="M")["returns"].loc[d["start"]:])
g3 = abs(m3["CAGR"] - 0.1269) < 5e-4 and abs(m3["Sharpe"] - 1.201) < 0.02 and abs(m3["MaxDD"] + 0.1711) < 5e-4
log(f"  G3 U56 MOM k=20 g=0.65 vs idea 879 memo (12.69% / 1.201 / -17.11%): "
    f"{m3['CAGR']:.2%} / {m3['Sharpe']:.3f} / {m3['MaxDD']:.2%}  -> {'PASS' if g3 else 'FAIL'}")

gap = float((SH.beta_OLSD - SH.beta_DOWN).abs().max())
log(f"  G4 the estimators are different numbers: max |OLSD - DOWN| over the shelf = {gap:.4f}, "
    f"max |OLSD - OLSM| = {float((SH.beta_OLSD - SH.beta_OLSM).abs().max()):.4f}  -> "
    f"{'PASS' if gap > 0.01 else 'FAIL (estimator choice is vacuous)'}")

log(f"\n  shelf: {len(SH)} books ({len(SH[SH.family!='REFERENCE'])} grid + "
    f"{len(SH[SH.family=='REFERENCE'])} reference) over {len(PANELS)} panels")

# ================================================================ H_AFFINE
log("\n" + "=" * 112)
log("H_AFFINE — regress each shelf book's MaxDD on its own SPY beta.  Every block reported.")
log("=" * 112)
aff = []
for pn in PANELS:
    b = SH[SH.panel == pn]
    for e in ESTIMATORS:
        x, y = b[f"beta_{e}"].to_numpy(), b["MaxDD"].to_numpy()
        ok = np.isfinite(x) & np.isfinite(y)
        x, y = x[ok], y[ok]
        sl, ic = np.polyfit(x, y, 1)
        res = y - (sl * x + ic)
        r2 = 1 - res.var() / y.var()
        aff.append(dict(panel=pn, est=e, n=len(x), slope=sl, intercept=ic, R2=r2,
                        resid_sd_pp=100 * res.std(), resid_max_pp=100 * np.abs(res).max(),
                        spyMaxDD=b["MaxDD"].iloc[0] * 0 + metrics(DATA[pn]["spy"])["MaxDD"],
                        dd_cap=0.60 * metrics(DATA[pn]["spy"])["MaxDD"]))
AF = pd.DataFrame(aff)
log(AF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
h_affine = bool((AF.R2 >= 0.90).any())
log(f"\nH_AFFINE (R2 >= 0.90 somewhere): {'CONFIRMED' if h_affine else 'REFUTED'} — "
    f"max R2 {AF.R2.max():.4f} ({AF.loc[AF.R2.idxmax(),'panel']}/{AF.loc[AF.R2.idxmax(),'est']}), "
    f"min {AF.R2.min():.4f}; residual SD {AF.resid_sd_pp.min():.2f}-{AF.resid_sd_pp.max():.2f} pp "
    f"of drawdown against DD caps of " +
    ", ".join(f"{pn} {100*0.60*metrics(DATA[pn]['spy'])['MaxDD']:.1f} pp" for pn in PANELS))

# ================================================================ H_CAP
log("\n" + "=" * 112)
log("H_CAP — is the DD cap reproducible as a BETA CAP?  (best threshold b*, and where it errs)")
log("=" * 112)
cap = []
for pn in PANELS:
    b = SH[SH.panel == pn]
    for e in ESTIMATORS:
        bb, agree = best_threshold(b[f"beta_{e}"].to_numpy(), b["dd_ok"].to_numpy())
        pred = b[f"beta_{e}"] <= bb
        cap.append(dict(panel=pn, est=e, n=len(b), b_star=bb, agreement=agree,
                        n_dd_ok=int(b.dd_ok.sum()),
                        false_pass=int((pred & ~b.dd_ok).sum()),     # low beta, fails DD cap
                        false_fail=int((~pred & b.dd_ok).sum()),     # high beta, clears DD cap
                        rho_spearman=float(b[[f"beta_{e}", "MaxDD"]].corr(method="spearman").iloc[0, 1])))
CP = pd.DataFrame(cap)
log(CP.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
h_cap = bool((CP.agreement >= 0.95).all())
log(f"\nH_CAP (>= 95% agreement in EVERY block): {'CONFIRMED' if h_cap else 'REFUTED'} — "
    f"agreement {CP.agreement.min():.4f}-{CP.agreement.max():.4f}, "
    f"{int((CP.agreement >= 0.95).sum())} of {len(CP)} blocks at or above 0.95")

# ================================================================ H_RESID
log("\n" + "=" * 112)
log("H_RESID — does any book buy the DD cap with CONSTRUCTION rather than with de-grossing?")
log("=" * 112)
res_rows = []
for pn in PANELS:
    b = SH[SH.panel == pn]
    for e in ESTIMATORS:
        fail_med = float(b.loc[~b.dd_ok, f"beta_{e}"].median())
        winners = b[b.dd_ok & (b[f"beta_{e}"] > fail_med)]
        res_rows.append(dict(panel=pn, est=e, fail_median_beta=fail_med,
                             n_dd_ok_above=len(winners),
                             books=", ".join(winners.book.head(4))))
RS = pd.DataFrame(res_rows)
log(RS.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
h_resid = bool((RS.n_dd_ok_above == 0).all())
log(f"\nH_RESID (no book clears the DD cap above the failers' median beta): "
    f"{'CONFIRMED — the cap is bought with beta and nothing else' if h_resid else 'REFUTED'} — "
    f"{int(RS.n_dd_ok_above.sum())} such books across {len(RS)} blocks")

# per-gross view: the de-grossing story, stated as numbers
log("\n  DD-cap pass rate by gross (grid books only, all panels pooled):")
gg = GRID.groupby("gross").agg(
    books=("book", "size"), dd_ok=("dd_ok", "sum"), cagr_ok=("cagr_ok", "sum"),
    CAGR=("CAGR", "mean"), MaxDD=("MaxDD", "mean"), beta=("beta_OLSD", "mean"))
gg["both"] = GRID.assign(_b=GRID.dd_ok & GRID.cagr_ok).groupby("gross")["_b"].sum()
log(gg.to_string(float_format=lambda x: f"{x:.4f}"))

# ================================================================ rule 8 / H_REACH
log("\n" + "=" * 112)
log("PROTOCOL RULE 8 WALK-FORWARD — b*, betas and the pick all fitted on IS only; OOS read once")
log("=" * 112)
sel_rows = []
for pn in PANELS:
    b = SH[SH.panel == pn].copy()
    for e in ESTIMATORS:
        b_is, agree_is = best_threshold(b[f"isbeta_{e}"].to_numpy(), b["is_dd_ok"].to_numpy())
        for selname in ["PICK-BETA", "PICK-DDIS", "PICK-SHARPE"]:
            if selname == "PICK-BETA":
                cand = b[b[f"isbeta_{e}"] <= b_is]
            elif selname == "PICK-DDIS":
                cand = b[b.is_dd_ok]
            else:
                cand = b
            if len(cand) == 0:
                sel_rows.append(dict(panel=pn, est=e, selector=selname, b_star_IS=b_is,
                                     picked="NONE"))
                continue
            c0 = cand.sort_values("is_Sharpe", ascending=False).iloc[0]
            sel_rows.append(dict(panel=pn, est=e, selector=selname, b_star_IS=b_is,
                                 is_agree=agree_is, picked=c0.book,
                                 is_Sharpe=c0.is_Sharpe, oos_CAGR=c0.oos_CAGR,
                                 oos_Sharpe=c0.oos_Sharpe, oos_MaxDD=c0.oos_MaxDD,
                                 oos_dd=c0.oos_dd, oos_cagr=c0.oos_cagr, oos_h1=c0.oos_h1,
                                 oos_h2=c0.oos_h2, oos_4b=c0.oos_4b,
                                 full_4b=c0.KEEP4b, full_4a=c0.KEEP4a))
SEL = pd.DataFrame(sel_rows)
SEL.to_csv(OUTDIR / f"{SLUG}.selectors.csv", index=False)
log(SEL.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

reach = SEL[SEL.get("oos_4b", False) == True] if "oos_4b" in SEL else pd.DataFrame()   # noqa: E712
log(f"\nH_REACH: {len(reach)} of {len(SEL)} IS-only selector picks clear 4b OUT OF SAMPLE "
    f"({len(SEL[(SEL.selector=='PICK-BETA')])} of them are the beta-cap selector's).")
if len(reach):
    log(reach.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

log("\nOOS comparands (2017-01-01..), per panel:")
for pn in PANELS:
    s, bb = DATA[pn]["spy"].loc[OOS_START:], DATA[pn]["base"].loc[OOS_START:]
    ms, mb = metrics(s), metrics(bb)
    log(f"  {pn}: SPY CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%}  |  "
        f"RULES v2 live CAGR {mb['CAGR']:.2%} Sharpe {mb['Sharpe']:.3f} MaxDD {mb['MaxDD']:.2%}  |  "
        f"OOS 4b bars: DD cap {0.60*ms['MaxDD']:.2%}, CAGR floor {0.70*ms['CAGR']:.2%}")

# ================================================================ verdict
log("\n" + "=" * 112)
log("VERDICT")
log("=" * 112)
log(f"  shelf books priced                    {len(SH)}")
log(f"  clear the 4b DD cap (full sample)     {int(SH.dd_ok.sum())}")
log(f"  clear the 4b CAGR floor               {int(SH.cagr_ok.sum())}")
log(f"  clear BOTH                            {int((SH.dd_ok & SH.cagr_ok).sum())}")
log(f"  clear all four 4b legs (full sample)  {int(SH.KEEP4b.sum())}")
log(f"  clear all four 4b legs (OOS window)   {int(SH.oos_4b.sum())}")
log(f"  clear 4a vs RULES v2 live             {int(SH.KEEP4a.sum())}")
log(f"  reached by an IS-only selector OOS    {len(reach)}")
log(f"\n  H_AFFINE {'CONFIRMED' if h_affine else 'REFUTED'} | H_CAP "
    f"{'CONFIRMED' if h_cap else 'REFUTED'} | H_RESID {'CONFIRMED' if h_resid else 'REFUTED'} | "
    f"H_REACH {'CONFIRMED' if len(reach) else 'REFUTED'}")
verdict = "KEEP-candidate" if len(reach) else ("PARK" if int(SH.KEEP4b.sum()) else "KILL")
log(f"\n  VERDICT: {verdict}")
log("  (KEEP-candidate requires an IS-only selector to land on a book that clears 4b OOS.)")
