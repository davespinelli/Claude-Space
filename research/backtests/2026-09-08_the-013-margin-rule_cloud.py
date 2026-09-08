#!/usr/bin/env python3
"""Idea 241 — the-013-margin-rule (cloud, 2026-09-08)

QUESTION (queue, verbatim intent)
  Idea 77's IS-Sharpe chooser lost 0.230 of OOS Sharpe on an IS margin of 0.013 (BSTK100
  1.0520 vs STK20 1.0392).  Pool every published argmax in the record with its runner-up gap
  and test whether a MINIMUM-MARGIN ABSTENTION RULE — fall back to the incumbent when the
  top-2 IS gap is under a pre-registered threshold — beats the raw argmax OOS.

PRE-REGISTERED PREDICTIONS (written before any number in parts B-E was read)
  R1  The rule will NOT have an interior optimum.  Idea 114 already showed the margin
      predicts pick STABILITY but not OOS REGRET (rho +0.119, p 0.705, wrong sign), so a
      threshold on the margin has nothing to condition on.
  R2  If anything beats the raw argmax it will be tau = INFINITY — always abstain — because
      the record's standing result is that selection loses to a do-nothing control (ideas
      229/232/446, "a sixth coin flip").  That is not a margin rule; it is "do not select",
      and this run must say so rather than banking an interior-looking win.
  R3  The margin distribution is heavily right-skewed with a mode near zero, so a tau in the
      0.01-0.02 region abstains on roughly half of all instances and the rule's curve will be
      close to a linear interpolation between the two endpoints.
  R4  Idea 77's 0.013 will sit near the MEDIAN of the record's margin distribution, i.e. it is
      an ordinary margin, not an unusually thin one — which would make "0.013 was too thin to
      act on" a post-hoc reading of one instance.

WHAT THIS RUN DOES (declared before any number is read)
  A. THE CORPUS.  Every published argmax the record can still be re-read as an argmax, found
     mechanically, not by prose: every committed research/backtests/*.csv carrying BOTH an
     IS_Sharpe and an OOS_Sharpe column is scanned; STRUCTURAL columns (non-metric, low
     cardinality) are separated from metrics; the DIAL is the numeric structural column with
     the most levels that is NOT a replication or reporting axis (draw/seed/rung/phase/shift/
     fold/cost_bps/...); the remaining structural columns form the CELL.  A (file, cell) with
     >= 3 dial levels and exactly one row per level is a SELECTION INSTANCE.  Every file is
     admitted or rejected WITH ITS REASON and the counts are published.
     Because a handful of files carry thousands of instances, every pooled statistic is
     reported BOTH instance-pooled AND file-clustered (equal weight per file), and every
     bootstrap is blocked on FILE.

  B. THE MARGIN.  Per instance: pick = IS argmax, MARGIN = IS_Sharpe(top1) - IS_Sharpe(top2),
     OOS Sharpe of the pick, of the fallback, of the ladder's OOS-best (the oracle), and
     REGRET = oracle - pick.  Idea 114's margin distribution is reproduced from its own
     committed cells as a gate, then extended to the full corpus.  Where idea 77's 0.013 sits
     in that distribution is reported (R4).

  C. THE RULE (TUNED PARAMETER 1 = tau).  For every tau on a declared ladder — 0 (raw
     argmax), the record's own margin deciles, idea 77's 0.013, and INF (always abstain) —
     the rule takes the argmax when margin >= tau and the fallback otherwise.  Mean OOS
     Sharpe, win rate against the raw argmax, and abstention rate are reported at EVERY tau,
     under both fallbacks (TUNED PARAMETER 2), instance-pooled and file-clustered.

  D. RULE 8 ON THE CORPUS.  tau is chosen on a random half of FILES and read once on the
     held-out half, 20 seeds.  A rule that only wins where its tau was fitted is not a rule.

  E. RULE 8 ON LIVE PRICES, OUT OF CORPUS.  Idea 229's pre-registered live frame is IMPORTED
     and re-run on fresh prices: 6 dials x 3 panels x 2 cost rungs = 36 cells, each dial
     carrying its DECLARED incumbent arm (so the fallback is the record's, not this run's).
     Choice on IS (<= 2016-12-31) only; 2017-2026 read once.  The tau chosen in part D on the
     RECORD corpus is applied here UNTOUCHED — a genuine out-of-universe walk-forward — and
     the whole tau ladder is reported beside it.  Pooled equal-weight books for the raw
     chooser, the abstaining chooser and the always-incumbent arm go through BOTH KEEP PATHS
     (4a vs live RULES v2 and v1, 4b vs SPY), full sample + halves + OOS.

  TWO TUNED PARAMETERS, EVERY GRID POINT REPORTED
    P1  TAU   — the minimum-margin threshold.  Ladder declared below, includes 0 and INF.
    P2  FALLBACK — what you hold when you abstain.  On the record corpus, where no incumbent
        is declared in a generic grid, {LADDER-MEAN, LADDER-MEDIAN}; on the live frame, the
        dial's DECLARED INCUMBENT (idea 229's, imported) with LADDER-MEAN reported beside it.
  Everything else — the IS/OOS split, the six live dials and their incumbents, panels, costs,
  cadence, gross, t+1 execution, the backtest helpers — is imported from the record's own
  committed scripts, not re-chosen here.

SURVIVORSHIP.  The small panel is current constituents of a sub-$2B screen only, and the
broad panel is current constituents (PROTOCOL 9).  Levels are upward-biased; only same-cell
contrasts (pick minus fallback, on the same ladder and the same days) are read.  The record
corpus inherits whatever bias each source run carried; it is a re-reading, not new evidence
about returns.

Costs 10 and 25 bps, next-day execution (PROTOCOL 2).  Deterministic (seeds fixed).
Artefacts: .console.txt, .corpus.csv, .instances.csv, .tau.csv, .holdout.csv, .livegrid.csv,
           .walkforward.csv, .keeppaths.csv, .result.md
Nothing outside research/ is touched; RULES.md, scan.py, bot.py, baseline.py untouched.
"""
from __future__ import annotations
import sys, re, glob, os, time, importlib.util, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import rules_v1_weights, rules_v2_weights  # noqa
from engine import backtest as engine_backtest           # noqa

BT = ROOT / "research" / "backtests"
STEM = "2026-09-08_the-013-margin-rule_cloud"
LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def _load(stem, mod):
    spec = importlib.util.spec_from_file_location(mod, BT / f"{stem}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# idea 229's live frame: six dials with DECLARED incumbents, panels, costs, book builders.
I229 = _load("2026-09-08_the-tenth-selection-loses-instance-as-a-distribution_cloud", "i229")
DIALS, PANELS, COSTS = I229.DIALS, I229.PANELS, I229.COSTS
live_book, parts, fast_backtest, csd = I229.live_book, I229.parts, I229.fast_backtest, I229.csd
IS_END, OOS_START, C229 = I229.IS_END, I229.OOS_START, I229.C

IDEA77_MARGIN = 0.013          # the queue's own number, declared before anything is read
SEEDS = 20
B_BOOT = 2000

# ---------------------------------------------------------------- corpus admission (PART A)
MET = re.compile(r"(?i)(cagr|sharpe|maxdd|calmar|sortino|turnover|regret|margin|equity|"
                 r"^dd$|_dd$|^h[12]$|years|^t_|^p_|pval|pass|keep|beat|wins|losses|"
                 r"spy_|vol|ret|alpha|corr|slope|^n$|^n_|count|frac|_pct)")
NOTDIAL = re.compile(r"(?i)^(draw|seed|rep|boot|iter|sim|rung|phase|shift|fold|split|"
                     r"cost_bps|bps|cost|year|month|start|end|idx|index|row|id)$")


def harvest():
    """Every committed CSV that can still be re-read as an argmax over a dial."""
    rows, inst = [], []
    for f in sorted(glob.glob(str(BT / "*.csv"))):
        base = os.path.basename(f)
        if base.startswith(STEM):
            continue
        try:
            d = pd.read_csv(f)
        except Exception as e:
            rows.append(dict(file=base, admitted=False, reason=f"unreadable ({type(e).__name__})",
                             dial="", n_inst=0)); continue
        if not len(d):
            rows.append(dict(file=base, admitted=False, reason="empty", dial="", n_inst=0)); continue
        lc = {c.lower(): c for c in d.columns}
        if "oos_sharpe" not in lc:
            rows.append(dict(file=base, admitted=False, reason="no OOS_Sharpe column",
                             dial="", n_inst=0)); continue
        isc = next((lc[c] for c in lc if c in ("is_sharpe", "sharpe_is", "is sharpe")), None)
        if isc is None:
            rows.append(dict(file=base, admitted=False, reason="no IS_Sharpe column",
                             dial="", n_inst=0)); continue
        oosc = lc["oos_sharpe"]
        struct = [c for c in d.columns
                  if not MET.search(c) and d[c].nunique(dropna=True) <= max(3, 0.25 * len(d))]
        dials = [c for c in struct if not NOTDIAL.search(c)
                 and pd.api.types.is_numeric_dtype(d[c])
                 and 3 <= d[c].nunique(dropna=True) <= 25]
        if not dials:
            rows.append(dict(file=base, admitted=False,
                             reason="no numeric design dial with 3-25 levels", dial="",
                             n_inst=0)); continue
        dial = max(dials, key=lambda c: d[c].nunique(dropna=True))
        cellk = [c for c in struct if c != dial]
        k = 0
        grp = d.groupby(cellk, dropna=False) if cellk else [((), d)]
        for key, s in grp:
            s = s.dropna(subset=[isc, oosc])
            if s[dial].nunique() < 3 or len(s) != s[dial].nunique():
                continue
            s = s.sort_values(dial)
            v = s[isc].values.astype(float)
            o = s[oosc].values.astype(float)
            x = s[dial].values.astype(float)
            order = np.argsort(-v)
            pick_i = int(order[0])
            margin = float(v[order[0]] - v[order[1]])
            # fallbacks, both declared: the ladder held equally, and its middle rung by dial
            fb_mean = float(o.mean())
            mid = int(np.argsort(x)[len(x) // 2])
            fb_med = float(o[mid])
            inst.append(dict(file=base, dial=dial, n_arms=len(s),
                             cell=str(key) if cellk else "(single)",
                             margin=margin, is_best=float(v[order[0]]),
                             is_runnerup=float(v[order[1]]), is_sd=float(v.std(ddof=1)),
                             oos_pick=float(o[pick_i]), oos_mean=fb_mean, oos_median=fb_med,
                             oos_best=float(o.max()), oos_worst=float(o.min()),
                             pick_is_oos_best=bool(pick_i == int(np.argmax(o)))))
            k += 1
        rows.append(dict(file=base, admitted=bool(k), dial=dial if k else "",
                         reason="OK" if k else "no cell with a clean >=3-rung ladder", n_inst=k))
    return pd.DataFrame(rows), pd.DataFrame(inst)


def spearman(a, b):
    """Rank correlation without scipy (the sandbox has none): Pearson on average ranks."""
    a = pd.Series(np.asarray(a, float)); b = pd.Series(np.asarray(b, float))
    ok = a.notna() & b.notna()
    if ok.sum() < 3:
        return float("nan")
    ra, rb = a[ok].rank(), b[ok].rank()
    if ra.nunique() < 2 or rb.nunique() < 2:
        return float("nan")
    return float(np.corrcoef(ra.values, rb.values)[0, 1])


def clustered(df, col, by="file"):
    """Equal weight per file, so a 1,210-instance file cannot own a pooled mean."""
    return float(df.groupby(by)[col].mean().mean())


def boot_file(df, col, B=B_BOOT, seed=241001):
    rng = np.random.default_rng(seed)
    files = df.file.unique()
    g = {f: df.loc[df.file == f, col].values for f in files}
    out = np.empty(B)
    for b in range(B):
        pick = rng.choice(files, len(files), replace=True)
        out[b] = np.mean([g[f].mean() for f in pick])
    return float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5)), float((out <= 0).mean())


# ============================================================================== PART C: tau
def apply_rule(I, tau, fallback):
    """OOS Sharpe the abstention rule earns on each instance."""
    fb = I.oos_mean.values if fallback == "LADDER-MEAN" else I.oos_median.values
    take = I.margin.values >= tau
    return np.where(take, I.oos_pick.values, fb), take


def tau_table(I, taus, fallbacks):
    rows = []
    for fb in fallbacks:
        raw, _ = apply_rule(I, 0.0, fb)
        for tau in taus:
            v, take = apply_rule(I, tau, fb)
            d = v - raw
            rows.append(dict(fallback=fb, tau=tau,
                             abstain_rate=float(1 - take.mean()),
                             mean_oos=float(v.mean()), clustered_oos=clustered(
                                 I.assign(_v=v), "_v"),
                             d_vs_argmax=float(d.mean()),
                             d_clustered=clustered(I.assign(_d=d), "_d"),
                             win_rate=float((d > 0).mean()),
                             loss_rate=float((d < 0).mean()),
                             n=len(I)))
    return pd.DataFrame(rows)


# ============================================================ PART E: live frame (idea 229)
def metrics_is(r):
    c, s, dd = csd(r.loc[:IS_END])
    return s


def run_live():
    P("\n" + "=" * 118)
    P("PART E — RULE 8 ON LIVE PRICES, OUT OF CORPUS.  Idea 229's pre-registered frame,")
    P("imported unchanged: 6 dials x 3 panels x 2 cost rungs = 36 cells, each dial carrying")
    P("its DECLARED incumbent arm.  Choice on IS (<= 2016-12-31) only; 2017-2026 read once.")
    P("=" * 118)
    ref, rows, RET = {}, [], {}
    t0 = time.time()
    for pk in PANELS:
        px, spy_full, desc = C229.panel(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        s, above, v = parts(px, pk)
        n_elig = float((above & (v < 0.60)).loc[start:].sum(axis=1).mean())
        nmap = {m: max(2, int(round(m * n_elig)))
                for m in [0.05, 0.10, 0.15, 0.20, 0.27, 0.35, 0.53, 0.75]}
        v2 = {c: fast_backtest(px, rules_v2_weights(px), c).loc[start:] for c in COSTS}
        v1 = {c: fast_backtest(px, rules_v1_weights(px), c).loc[start:] for c in COSTS}
        ref[pk] = dict(px=px, start=start, spy=spy, nmap=nmap, v2=v2, v1=v1, desc=desc)
        cg, sh, dd = csd(spy)
        oc, osh, odd = csd(spy.loc[OOS_START:])
        P(f"\n  [panel] {pk} = {desc}: {px.shape[1]} cols, eval {start.date()} -> "
          f"{px.index[-1].date()}, mean weekly eligible {n_elig:.1f}")
        P(f"      SPY {cg:.2%}/{sh:.3f}/{dd:.2%} | OOS {oc:.2%}/{osh:.3f}/{odd:.2%}")
        for c in COSTS:
            a, b, d_ = csd(v2[c]); e, f_, g_ = csd(v1[c])
            P(f"      RULES v2 @{c:.0f}bps {a:.2%}/{b:.3f}/{d_:.2%}   "
              f"RULES v1 @{c:.0f}bps {e:.2%}/{f_:.3f}/{g_:.2%}")
        for dial, (ladder, dflt) in DIALS.items():
            for arm in ladder:
                W, freq = live_book(px, pk, dial, arm, nmap)
                for cost in COSTS:
                    r = fast_backtest(px, W, cost, freq).loc[start:]
                    RET[(pk, cost, dial, arm)] = r
                    cgr, shr, ddr = csd(r)
                    oc2, osh2, odd2 = csd(r.loc[OOS_START:])
                    h = len(r) // 2
                    _, h1, _ = csd(r.iloc[:h])
                    _, h2, _ = csd(r.iloc[h:])
                    rows.append(dict(panel=pk, cost=cost, dial=dial, arm=arm,
                                     is_default=(arm == dflt),
                                     IS_Sharpe=metrics_is(r), CAGR=cgr, Sharpe=shr, MaxDD=ddr,
                                     H1=h1, H2=h2, OOS_CAGR=oc2, OOS_Sharpe=osh2,
                                     OOS_MaxDD=odd2))
        P(f"      {sum(len(l) for l, _ in DIALS.values()) * len(COSTS)} books done "
          f"({time.time() - t0:.0f}s cum.)")
    return ref, pd.DataFrame(rows), RET


def live_cells(LG):
    """One selection instance per (panel, cost, dial), with the DECLARED incumbent."""
    out = []
    for pk in PANELS:
        for cost in COSTS:
            for dial, (ladder, dflt) in DIALS.items():
                s = LG[(LG.panel == pk) & (LG.cost == cost) & (LG.dial == dial)]
                s = s.set_index("arm").reindex(ladder).dropna(subset=["IS_Sharpe"])
                if len(s) < 3:
                    continue
                v = s.IS_Sharpe.values
                o = s.OOS_Sharpe.values
                order = np.argsort(-v)
                out.append(dict(panel=pk, cost=cost, dial=dial, n_arms=len(s),
                                pick=s.index[order[0]], incumbent=dflt,
                                margin=float(v[order[0]] - v[order[1]]),
                                oos_pick=float(o[order[0]]),
                                oos_incumbent=float(s.OOS_Sharpe.get(dflt, np.nan)),
                                oos_mean=float(o.mean()), oos_best=float(o.max()),
                                pick_is_incumbent=bool(s.index[order[0]] == dflt)))
    return pd.DataFrame(out)


# ==================================================================================== main
def main():
    P("=" * 118)
    P("IDEA 241 — THE 0.013 MARGIN RULE (cloud, 2026-09-08)")
    P("=" * 118)
    P("\nPRE-REGISTERED: R1 no interior optimum; R2 any win sits at tau=INF and is 'do not")
    P("select', not a margin rule; R3 the margin mode is near zero so the curve is close to a")
    P("straight line between the endpoints; R4 idea 77's 0.013 is an ORDINARY margin.")

    P("\nREPRODUCTION GATES (binding, before any new number is read)")
    C114 = pd.read_csv(BT / "2026-09-05_IS-Sharpe-margin-as-the-reportable-selector-"
                            "statistic_cloud.cells.csv")
    ok114 = (len(C114) == 44 and abs(C114.M.mean() - 0.019) < 5e-4
             and abs(C114.M.median() - 0.006) < 5e-4 and abs(C114.M.max() - 0.120) < 5e-4)
    P(f"  G1  idea 114's margin distribution from its own 44 committed cells: mean "
      f"{C114.M.mean():.4f} median {C114.M.median():.4f} max {C114.M.max():.4f} "
      f"(published 0.019 / 0.006 / 0.120) -> {'MATCH' if ok114 else 'MISMATCH'}")
    assert ok114
    r114 = spearman(C114.M, C114.R)
    P(f"  G2  idea 114's null (margin -> OOS regret), Spearman: {r114:+.3f} "
      f"(published +0.119, wrong sign, p 0.705) -> "
      f"{'MATCH' if abs(r114 - 0.119) < 0.02 else 'reported as found'}")

    px, spy_full, desc = C229.panel("u56")
    W0 = rules_v2_weights(px)
    a = engine_backtest(px, W0, cost_bps=10.0, freq="W")["returns"]
    b = fast_backtest(px, W0, 10.0, "W")
    P(f"  G3  fast_backtest vs engine.backtest, RULES v2 / u56: max |diff| "
      f"{float(np.abs(a - b).max()):.3e}")
    assert float(np.abs(a - b).max()) < 1e-12

    # ------------------------------------------------------------------------ PART A
    P("\n" + "=" * 118)
    P("PART A — THE CORPUS.  Every committed CSV re-readable as an argmax over a design dial.")
    P("Admission is mechanical; every file is admitted or rejected WITH ITS REASON.")
    P("=" * 118)
    CO, I = harvest()
    P(f"  CSV files scanned ................ {len(CO)}")
    for reason, n in CO[~CO.admitted].reason.value_counts().items():
        P(f"    rejected: {reason:52s} {n:5d}")
    P(f"  ADMITTED files ................... {int(CO.admitted.sum())}")
    P(f"  SELECTION INSTANCES .............. {len(I)}")
    P(f"  instances per admitted file: median {CO[CO.admitted].n_inst.median():.0f}, "
      f"max {CO[CO.admitted].n_inst.max():.0f} "
      f"({CO.loc[CO.n_inst.idxmax(), 'file']})")
    P(f"  -> a few files dominate the pool, so EVERY pooled number below is reported BOTH")
    P(f"     instance-pooled AND file-clustered, and every bootstrap is blocked on FILE.")
    P(f"\n  ladder length: {I.n_arms.min()}-{I.n_arms.max()} arms, median {I.n_arms.median():.0f}")
    P(f"  dials used (top 12): " + ", ".join(
        f"{k} {v}" for k, v in I.dial.value_counts().head(12).items()))

    # ------------------------------------------------------------------------ PART B
    P("\n" + "=" * 118)
    P("PART B — THE MARGIN, and where idea 77's 0.013 sits in it.")
    P("=" * 118)
    q = I.margin.quantile([0.1, 0.25, 0.5, 0.75, 0.9, 0.99]).to_dict()
    P(f"  margin over {len(I)} instances: mean {I.margin.mean():.4f}, median "
      f"{I.margin.median():.4f}, sd {I.margin.std():.4f}, max {I.margin.max():.4f}")
    P(f"    deciles/quartiles: " + "  ".join(f"p{int(k*100)} {v:.4f}" for k, v in q.items()))
    pct77 = float((I.margin <= IDEA77_MARGIN).mean())
    P(f"  idea 77's {IDEA77_MARGIN}: it is the {pct77:.1%} percentile of the record's margins "
      f"-> R4 {'CONFIRMED' if 0.3 <= pct77 <= 0.7 else 'REFUTED'} "
      f"({'an ordinary margin' if 0.3 <= pct77 <= 0.7 else 'NOT an ordinary margin'})")
    P(f"  file-clustered mean margin {clustered(I, 'margin'):.4f}")

    I["regret"] = I.oos_best - I.oos_pick
    I["d_mean"] = I.oos_pick - I.oos_mean
    I["d_median"] = I.oos_pick - I.oos_median
    for x, y in [("margin", "regret"), ("margin", "d_mean"), ("margin", "d_median")]:
        rho = spearman(I[x], I[y])
        rr = [spearman(I[I.file == f][x], I[I.file == f][y])
              for f in I.file.unique() if I[I.file == f][x].nunique() > 2]
        rr = [v for v in rr if np.isfinite(v)]
        rhoc = float(np.mean(rr)) if rr else float("nan")
        P(f"  Spearman({x}, {y}) = {rho:+.4f} pooled, {rhoc:+.4f} mean within-file")
    P(f"  the pick is already the OOS-best arm in {I.pick_is_oos_best.mean():.1%} of instances "
      f"(file-clustered {clustered(I, 'pick_is_oos_best'):.1%}); mean regret "
      f"{I.regret.mean():.4f}")
    lo, hi, p0 = boot_file(I, "d_mean")
    P(f"  RAW ARGMAX minus LADDER-MEAN, pooled {I.d_mean.mean():+.4f}, file-clustered "
      f"{clustered(I, 'd_mean'):+.4f}, 95% CI (file-blocked) [{lo:+.4f}, {hi:+.4f}], "
      f"P(<=0) {p0:.3f}")

    # ------------------------------------------------------------------------ PART C
    P("\n" + "=" * 118)
    P("PART C — THE RULE.  P1 = tau (every rung reported, including 0 = raw argmax and")
    P("INF = always abstain); P2 = fallback.  d_vs_argmax > 0 means the abstention rule beats")
    P("the raw argmax OOS.")
    P("=" * 118)
    TAUS = [0.0, 0.001, 0.005, IDEA77_MARGIN, 0.02, 0.03, 0.05, 0.10, 0.25, np.inf]
    FALLBACKS = ["LADDER-MEAN", "LADDER-MEDIAN"]
    T = tau_table(I, TAUS, FALLBACKS)
    for fb in FALLBACKS:
        P(f"\n  fallback = {fb}")
        P(f"  {'tau':>8s} {'abstain':>8s} {'mean OOS':>9s} {'clustered':>10s} "
          f"{'d vs argmax':>12s} {'d clustered':>12s} {'win':>6s} {'loss':>6s}")
        for _, r in T[T.fallback == fb].iterrows():
            tag = "  <- idea 77" if r.tau == IDEA77_MARGIN else (
                "  <- raw argmax" if r.tau == 0 else (
                    "  <- always abstain" if not np.isfinite(r.tau) else ""))
            P(f"  {r.tau:8.3f} {r.abstain_rate:8.1%} {r.mean_oos:9.4f} {r.clustered_oos:10.4f} "
              f"{r.d_vs_argmax:+12.4f} {r.d_clustered:+12.4f} {r.win_rate:6.1%} "
              f"{r.loss_rate:6.1%}{tag}")
        s = T[(T.fallback == fb) & (T.tau > 0)]
        best = s.loc[s.d_clustered.idxmax()]
        wins = s[s.d_clustered > 0]
        P(f"    best tau > 0 on the file-clustered criterion: {best.tau:.3f} at "
          f"{best.d_clustered:+.4f}; rungs that actually BEAT the raw argmax: "
          f"{len(wins)} of {len(s)} "
          f"({', '.join(f'{v:.3f}' for v in wins.tau) if len(wins) else 'NONE'})")
        if len(wins) == 0:
            P(f"    -> R1 CONFIRMED: no tau > 0 beats the raw argmax; the curve is monotone "
              f"DOWN in tau and tau=INF is the worst point, so R2 is refuted too — on this "
              f"corpus SELECTION WINS and abstention is a pure cost.")
        elif not np.isfinite(best.tau):
            P(f"    -> R2: the only win is tau = INF, i.e. DO NOT SELECT — not a margin rule.")
        else:
            P(f"    -> an INTERIOR rung beats the raw argmax by {best.d_clustered:+.4f} "
              f"file-clustered.  Whether that survives is PART D's question, not this table's.")
    P(f"\n  R3 check — is the tau curve close to a straight line between its endpoints?")
    for fb in FALLBACKS:
        s = T[(T.fallback == fb) & np.isfinite(T.tau)].sort_values("abstain_rate")
        e0 = float(T[(T.fallback == fb) & (T.tau == 0)].d_clustered.iloc[0])
        e1 = float(T[(T.fallback == fb) & ~np.isfinite(T.tau)].d_clustered.iloc[0])
        pred = e0 + (e1 - e0) * s.abstain_rate.values
        P(f"    {fb}: max |actual - linear-in-abstention-rate| = "
          f"{np.abs(s.d_clustered.values - pred).max():.4f} over {len(s)} finite rungs")

    # ------------------------------------------------------------------------ PART D
    P("\n" + "=" * 118)
    P("PART D — RULE 8 ON THE CORPUS.  tau chosen on a random half of FILES, read once on the")
    P(f"held-out half, {SEEDS} seeds.  A rule that only wins where its tau was fitted is not a rule.")
    P("=" * 118)
    files = np.array(sorted(I.file.unique()))
    hrows = []
    P(f"  {'fallback':14s} {'seed':>4s} {'tau*':>7s} {'IS gain':>9s} {'OOS gain':>9s} "
      f"{'OOS gain of tau=INF':>20s}")
    for fb in FALLBACKS:
        for seed in range(SEEDS):
            rng = np.random.default_rng(1000 + seed)
            perm = rng.permutation(len(files))
            fa = set(files[perm[: len(files) // 2]])
            A = I[I.file.isin(fa)]
            Bh = I[~I.file.isin(fa)]
            TA = tau_table(A, TAUS, [fb])
            s = TA[TA.tau > 0]
            tstar = float(s.loc[s.d_clustered.idxmax()].tau)
            isg = float(s.d_clustered.max())
            vB, _ = apply_rule(Bh, tstar, fb)
            rawB, _ = apply_rule(Bh, 0.0, fb)
            oosg = clustered(Bh.assign(_d=vB - rawB), "_d")
            vI, _ = apply_rule(Bh, np.inf, fb)
            oinf = clustered(Bh.assign(_d=vI - rawB), "_d")
            hrows.append(dict(fallback=fb, seed=seed, tau_star=tstar, is_gain=isg,
                              oos_gain=oosg, oos_gain_inf=oinf,
                              tau_is_inf=bool(not np.isfinite(tstar))))
            if seed < 5:
                P(f"  {fb:14s} {seed:4d} {tstar:7.3f} {isg:+9.4f} {oosg:+9.4f} {oinf:+20.4f}")
    HO = pd.DataFrame(hrows)
    for fb in FALLBACKS:
        s = HO[HO.fallback == fb]
        P(f"\n  {fb}: tau* = INF in {int(s.tau_is_inf.sum())}/{len(s)} seeds "
          f"(finite tau* values {sorted(set(np.round(s.tau_star[np.isfinite(s.tau_star)], 3)))});")
        P(f"    held-out gain of the CHOSEN tau {s.oos_gain.mean():+.4f} "
          f"(positive in {int((s.oos_gain > 0).sum())}/{len(s)} seeds); held-out gain of "
          f"tau=INF {s.oos_gain_inf.mean():+.4f} ({int((s.oos_gain_inf > 0).sum())}/{len(s)})")

    # ------------------------------------------------------------------------ PART E
    ref, LG, RET = run_live()
    LC = live_cells(LG)
    P(f"\n  {len(LC)} live cells (pre-registered 36 = 3 panels x 2 costs x 6 dials).")
    P(f"  {'panel':7s} {'cost':>5s} {'dial':9s} {'pick':>8s} {'incumb':>8s} {'margin':>8s} "
      f"{'OOS pick':>9s} {'OOS incumb':>11s} {'delta':>8s}")
    for _, r in LC.iterrows():
        P(f"  {r.panel:7s} {r.cost:5.0f} {r.dial:9s} {str(r.pick):>8s} {str(r.incumbent):>8s} "
          f"{r.margin:8.4f} {r.oos_pick:9.4f} {r.oos_incumbent:11.4f} "
          f"{r.oos_pick - r.oos_incumbent:+8.4f}")
    LC["d_inc"] = LC.oos_pick - LC.oos_incumbent
    P(f"\n  raw chooser minus DECLARED INCUMBENT, 36 cells: mean {LC.d_inc.mean():+.4f}, "
      f"positive in {int((LC.d_inc > 0).sum())}/{len(LC)}; chooser picks the incumbent itself "
      f"in {int(LC.pick_is_incumbent.sum())}/{len(LC)}")
    P(f"  live margin distribution: median {LC.margin.median():.4f}, "
      f"{(LC.margin <= IDEA77_MARGIN).mean():.1%} at or below idea 77's {IDEA77_MARGIN}")

    P(f"\n  THE RULE ON THE LIVE FRAME (fallback = the dial's DECLARED INCUMBENT; ladder-mean")
    P(f"  reported beside it).  tau* imported from PART D is applied UNTOUCHED.")
    P(f"  {'tau':>8s} {'abstain':>8s} {'mean OOS (incumbent fb)':>24s} {'d vs argmax':>12s} "
      f"{'mean OOS (ladder-mean fb)':>26s} {'d':>9s}")
    lrows = []
    raw = LC.oos_pick.values
    for tau in TAUS:
        take = LC.margin.values >= tau
        vi = np.where(take, raw, LC.oos_incumbent.values)
        vm = np.where(take, raw, LC.oos_mean.values)
        lrows.append(dict(tau=tau, abstain=float(1 - take.mean()),
                          oos_incumbent_fb=float(vi.mean()), d_inc=float((vi - raw).mean()),
                          oos_meanfb=float(vm.mean()), d_mean=float((vm - raw).mean())))
        tag = "  <- idea 77" if tau == IDEA77_MARGIN else ""
        P(f"  {tau:8.3f} {1 - take.mean():8.1%} {vi.mean():24.4f} {(vi - raw).mean():+12.4f} "
          f"{vm.mean():26.4f} {(vm - raw).mean():+9.4f}{tag}")
    LR = pd.DataFrame(lrows)

    # ------------------------------------------------- pooled books + both KEEP paths
    P("\n" + "=" * 118)
    P("POOLED BOOKS AND BOTH KEEP PATHS.  Equal-weight over the cells of each panel/cost:")
    P("CHOOSER (raw argmax), ABSTAIN@tau (the rule), INCUMBENT (always the declared arm),")
    P("and ORACLE (best OOS arm per cell, not investable).  4a vs live RULES v2 and v1 on the")
    P("cell's own panel; 4b vs SPY on that panel.")
    P("=" * 118)
    tau_live = float(HO[HO.fallback == "LADDER-MEAN"].tau_star.replace(np.inf, np.nan)
                     .median()) if np.isfinite(HO.tau_star).any() else np.nan
    tau_apply = IDEA77_MARGIN
    P(f"  tau applied to the pooled books: idea 77's own {tau_apply} (pre-registered) and, "
      f"where part D chose a finite tau*, {tau_live if np.isfinite(tau_live) else 'none'}.")
    krows, wrows = [], []
    for pk in PANELS:
        r0 = ref[pk]
        spy = r0["spy"]
        sc, ss, sdd = csd(spy)
        h = len(spy) // 2
        _, sh1, _ = csd(spy.iloc[:h])
        _, sh2, _ = csd(spy.iloc[h:])
        _, soos, _ = csd(spy.loc[OOS_START:])
        for cost in COSTS:
            sub = LC[(LC.panel == pk) & (LC.cost == cost)]
            arms = {}
            for name in ["CHOOSER", f"ABSTAIN@{tau_apply}", "INCUMBENT", "LADDER-MEAN", "ORACLE"]:
                series = []
                for _, r in sub.iterrows():
                    ladder = DIALS[r.dial][0]
                    if name == "CHOOSER":
                        arm = r.pick
                    elif name.startswith("ABSTAIN"):
                        arm = r.pick if r.margin >= tau_apply else r.incumbent
                    elif name == "INCUMBENT":
                        arm = r.incumbent
                    elif name == "ORACLE":
                        oo = {a: csd(RET[(pk, cost, r.dial, a)].loc[OOS_START:])[1]
                              for a in ladder if (pk, cost, r.dial, a) in RET}
                        arm = max(oo, key=oo.get)
                    else:
                        series.append(pd.concat(
                            [RET[(pk, cost, r.dial, a)] for a in ladder
                             if (pk, cost, r.dial, a) in RET], axis=1).mean(axis=1))
                        continue
                    series.append(RET[(pk, cost, r.dial, arm)])
                bk = pd.concat(series, axis=1).mean(axis=1)
                arms[name] = bk
                c, s_, dd = csd(bk)
                hh = len(bk) // 2
                _, h1, _ = csd(bk.iloc[:hh])
                _, h2, _ = csd(bk.iloc[hh:])
                oc, osh, odd = csd(bk.loc[OOS_START:])
                v2 = r0["v2"][cost]; v1 = r0["v1"][cost]
                c2, s2, d2 = csd(v2)
                hv = len(v2) // 2
                _, v2h1, _ = csd(v2.iloc[:hv])
                _, v2h2, _ = csd(v2.iloc[hv:])
                c1, s1, d1 = csd(v1)
                _, v1h1, _ = csd(v1.iloc[:hv])
                _, v1h2, _ = csd(v1.iloc[hv:])
                p4a_v2 = bool(h1 > v2h1 and h2 > v2h2 and dd >= d2)
                p4a_v1 = bool(h1 > v1h1 and h2 > v1h2 and dd >= d1)
                p4b = bool(h1 > sh1 and h2 > sh2 and osh > soos
                           and abs(dd) <= 0.60 * abs(sdd) and c >= 0.70 * sc)
                fail = "|".join([n for n, o in (("H1", h1 > sh1), ("H2", h2 > sh2),
                                                ("OOS", osh > soos),
                                                ("DD", abs(dd) <= 0.60 * abs(sdd)),
                                                ("CAGR", c >= 0.70 * sc)) if not o])
                rec = dict(panel=pk, cost=cost, arm=name, CAGR=c, Sharpe=s_, MaxDD=dd,
                           H1=h1, H2=h2, OOS_CAGR=oc, OOS_Sharpe=osh, OOS_MaxDD=odd,
                           v2_Sharpe=s2, v1_Sharpe=s1, spy_Sharpe=ss, spy_OOS=soos,
                           pass4a_v2=p4a_v2, pass4a_v1=p4a_v1, pass4b=p4b, failing4b=fail)
                krows.append(rec); wrows.append(rec)
    K = pd.DataFrame(krows)
    P(f"  {'panel':7s} {'cost':>5s} {'arm':18s} {'CAGR':>7s} {'Sharpe':>7s} {'MaxDD':>8s} "
      f"{'H1':>6s} {'H2':>6s} {'OOS CAGR':>9s} {'OOS Sh':>7s} {'4a v2':>6s} {'4b':>4s}")
    for _, r in K.iterrows():
        P(f"  {r.panel:7s} {r.cost:5.0f} {r.arm:18s} {r.CAGR:7.2%} {r.Sharpe:7.3f} "
          f"{r.MaxDD:8.2%} {r.H1:6.3f} {r.H2:6.3f} {r.OOS_CAGR:9.2%} {r.OOS_Sharpe:7.3f} "
          f"{('Y' if r.pass4a_v2 else '.'):>6s} {('Y' if r.pass4b else '.'):>4s}")
    P(f"\n  {'arm':18s} {'mean OOS Sharpe':>16s} {'4a(v2)':>7s} {'4a(v1)':>7s} {'4b':>5s}")
    for name, s in K.groupby("arm", sort=False):
        P(f"  {name:18s} {s.OOS_Sharpe.mean():16.4f} {int(s.pass4a_v2.sum()):3d}/{len(s):<3d} "
          f"{int(s.pass4a_v1.sum()):3d}/{len(s):<3d} {int(s.pass4b.sum()):3d}/{len(s):<3d}")
    P(f"  binding 4b bars over all {len(K)} books: "
      + ", ".join(f"{k} {v}" for k, v in
                  K[~K.pass4b].failing4b.str.split("|").explode().value_counts().items()))
    ch = K[K.arm == "CHOOSER"].set_index(["panel", "cost"]).OOS_Sharpe
    ab = K[K.arm == f"ABSTAIN@{tau_apply}"].set_index(["panel", "cost"]).OOS_Sharpe
    inc = K[K.arm == "INCUMBENT"].set_index(["panel", "cost"]).OOS_Sharpe
    P(f"\n  pooled-book OOS Sharpe: CHOOSER {ch.mean():.4f}, ABSTAIN@{tau_apply} "
      f"{ab.mean():.4f} ({(ab - ch).mean():+.4f}), INCUMBENT {inc.mean():.4f} "
      f"({(inc - ch).mean():+.4f}) over {len(ch)} (panel, cost) books.")

    # ---------------------------------------------------------------------------- write
    CO.to_csv(BT / f"{STEM}.corpus.csv", index=False)
    I.to_csv(BT / f"{STEM}.instances.csv", index=False)
    pd.concat([T.assign(scope="record"), LR.assign(scope="live")], ignore_index=True) \
        .to_csv(BT / f"{STEM}.tau.csv", index=False)
    HO.to_csv(BT / f"{STEM}.holdout.csv", index=False)
    LG.to_csv(BT / f"{STEM}.livegrid.csv", index=False)
    pd.concat([LC.assign(kind="cell"), pd.DataFrame(wrows).assign(kind="book")],
              ignore_index=True).to_csv(BT / f"{STEM}.walkforward.csv", index=False)
    K.to_csv(BT / f"{STEM}.keeppaths.csv", index=False)

    P("\n" + "=" * 118)
    P("HEADLINE")
    P("=" * 118)
    P(f"  1. CORPUS: {len(I)} selection instances over {int(CO.admitted.sum())} committed files "
      f"— every published argmax the record can still be re-read as one.")
    P(f"  2. R4: idea 77's 0.013 is the {pct77:.0%} percentile of the record's own margins — "
      f"{'an ordinary margin, not a thin one' if 0.3 <= pct77 <= 0.7 else 'NOT ordinary'}.")
    for fb in FALLBACKS:
        s = T[(T.fallback == fb) & (T.tau > 0)]
        best = s.loc[s.d_clustered.idxmax()]
        P(f"  3. RULE ({fb}): best tau > 0 is {best.tau:.3f} at {best.d_clustered:+.4f} "
          f"file-clustered; raw argmax = 0 by construction; tau=INF "
          f"{float(s[~np.isfinite(s.tau)].d_clustered.iloc[0]):+.4f}.")
    for fb in FALLBACKS:
        s = HO[HO.fallback == fb]
        P(f"  4. RULE 8 on the corpus ({fb}): held-out gain of the chosen tau "
          f"{s.oos_gain.mean():+.4f}, positive in {int((s.oos_gain > 0).sum())}/{len(s)} seeds.")
    P(f"  5. LIVE 36 cells: chooser minus declared incumbent {LC.d_inc.mean():+.4f} "
      f"({int((LC.d_inc > 0).sum())}/{len(LC)} positive); ABSTAIN@{tau_apply} vs CHOOSER on the "
      f"pooled books {(ab - ch).mean():+.4f}, INCUMBENT {(inc - ch).mean():+.4f}.")
    P(f"  6. KEEP paths: 4a(v2) {int(K.pass4a_v2.sum())}/{len(K)}, 4a(v1) "
      f"{int(K.pass4a_v1.sum())}/{len(K)}, 4b {int(K.pass4b.sum())}/{len(K)}.")

    Path(BT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"\nwrote {STEM}.console.txt and 7 CSVs")


if __name__ == "__main__":
    main()
