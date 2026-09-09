#!/usr/bin/env python3
"""IDEA 581 — how many of the record's PUBLISHED parent/clause-vs-control comparisons are
   GROSS-UNMATCHED, and how many of those change SIGN when matched?   (lane C, 2026-09-09)

QUESTION (QUEUE idea 581, verbatim)
    Idea 317 found idea 48's headline '0/16 on drawdown' flips to 51.7% once the parents are
    rescaled to the conditional book's own mean gross, i.e. the claim measured exposure, not
    conditioning.  Census the committed CSVs for every clause-vs-control comparison and report
    how many put the two arms at different mean gross, and how many of those change SIGN when
    matched.  Max 2 params.

TWO PARTS, BECAUSE THE CENSUS ALONE CANNOT ANSWER THE SECOND HALF
    PART A (census, mechanical, over the committed artifacts).  Enumerate every committed CSV
    that publishes a clause-vs-control comparison and ask what the FILE ITSELF lets a reader
    check about the two arms' gross.  Three tiers:
        T1  the file publishes a per-arm gross AND the compared arms carry DIFFERENT values
            -> visibly unmatched, auditable from the CSV alone.
        T2  the file publishes a per-arm gross and the arms AGREE on it, but the clause is a
            DE-GROSS clause (gated weight goes to CASH, never re-spread) -> the arms are
            unmatched in REALISED gross while looking matched in the published column.
        T3  the file publishes no gross column at all -> unauditable from the record.
    The decisive point is that NOMINAL gross equality is not gross matching: a de-gross clause
    holds strictly less exposure than its clause-OFF control at the same nominal gross, by
    construction, on every day the gate fires.  So the census counts de-gross clauses too.

    PART B (the sign test, real backtests).  The census can say a comparison is unmatched; it
    cannot say whether that mattered.  So rebuild the record's own de-gross clause forms
    against their own clause-OFF controls, measure the realised mean-gross gap, and re-price
    every comparison with the control rescaled to the clause book's own mean target gross.
    Report how many published-style deltas CHANGE SIGN.

THE 9 ARMS = 6 CLAUSE FAMILIES x THE GROSS CONVENTION THEY ARE PUBLISHED UNDER
    Each arm is one clause vs its own clause-OFF EWall control at the same nominal gross —
    exactly the comparison the record publishes.  The three name-level families are run under
    BOTH conventions, because the record publishes both and they are not the same test:
      DG  the gated weight goes to CASH (denominator = ALL eligible names), so realised gross
          FALLS with the gate — the RULES v2 form, and the form that makes a comparison
          gross-unmatched by construction.
      RS  the survivors are re-spread (denominator = the KEPT names), which holds gross at g
          and is therefore gross-matched for free.  RS is the control on the whole question:
          if matching changed signs by itself, RS would show it, and it must not.
    The three market-level families have no RS form — re-spreading a whole-book gate returns
    the control exactly — so they are DG only.  6 DG + 3 RS = 9 arms.

    name-level (cross-sectional) clauses:
      MA       hold only names above their own m-day MA           dial m in {100,150,200,250}
      VOL      drop names with vol20 >= cap                       dial cap in {.35,.45,.60,.90}
      BAND     RULES v2's own 200d +/- band state with hysteresis dial band in {0,.03,.06,.10}
    market-level (timing) clauses, whole book -> CASH in the bad state:
      BREADTH  fraction of priced names above their 200d MA, low  dial q in {.10,.20,.35,.50}
      SPYTR    SPY / SPY.rolling(200).mean() - 1, low             dial q as above
      DD       the CONTROL's own drawdown from its running peak   dial q as above
    Market-level thresholds are TRAILING 5y (1260d, min 504) rolling quantiles, not expanding
    ones (idea 399: the expanding estimator under-fires its nominal q by 3-4x).
    The control is ALWAYS the same book with the clause switched off — EWall at the same
    nominal gross — which is exactly the comparison the record publishes.

MATCHING CONVENTION (the same one idea 317 used, so the two runs are comparable)
    Scale the CONTROL's WEIGHTS by k = meanTargetGross(clause) / meanTargetGross(control),
    both measured on rebalance days, and RE-RUN the book.  Scaling the weights (not the return
    series) keeps costs proportional and preserves the engine's drift/normalisation semantics.
    k <= 1 for every de-gross clause, so no scaled book exceeds gross 1.0 (gate G2 asserts it).

TUNED PARAMETERS: 2 — (dial, base gross g).  4 dials x 3 g = 12 grid points per ARM per
    panel -> 9 x 12 x 3 = 324 comparisons, ALL reported in .cells.csv.  The arm's form (DG/RS)
    is not a tuned parameter: it is the published convention under audit.  Everything else PINNED: weekly cadence, t+1, 10 bps,
    MA 200d where not the dial, vol window 20d, quantile window 1260d/504 min, warm-up skip.

PANELS / SURVIVORSHIP
    U56       research/universe.json (56 cols incl. SPY; whole panel tradable, as EWall uses it)
    B136      research/universe_broad.json — CURRENT constituents, survivorship overstates
              every LEVEL.
    SMALL439  data/prices_small.csv.gz less names with max_1d_move >= 1.0 in data/small_meta.csv.
              SPY is a joined BENCHMARK, not a constituent, excluded from the tradable set.
    Every claim is a clause-vs-its-own-control DIFFERENCE on a fixed panel, so the level bias
    cancels; the walk-forward LEVELS on B136/SMALL439 are biased up and are labelled as such.

GATES
    G1  the vectorised runner reproduces engine.backtest to < 1e-12 on returns and turnover.
    G2  matched gross: |meanTargetGross(clause) - meanTargetGross(control_matched)| < 1e-12 and
        max gross <= 1.0.
    G3  a NULL clause (a mask that is always True) must produce k == 1 and a zero delta, so the
        matching machinery cannot manufacture a flip on its own.

RULE 8 (walk-forward, required).  Per arm x panel, pick (dial, g) on 2009-2016 ONLY, twice:
    once by the UNMATCHED dSharpe (the record's own selection rule) and once by the MATCHED
    dSharpe.  Evaluate 2017-2026 untouched: OOS CAGR/Sharpe/MaxDD of the clause book vs RULES
    v2 and vs SPY, whether the delta's SIGN holds OOS under each convention, and both KEEP
    paths (4a vs RULES v2, 4b vs SPY).

Outputs (committed): .console.txt .census.csv .cells.csv .walkforward.csv .keeppaths.csv .result.md
Deterministic; no network (load_universe reads committed caches).
"""
from __future__ import annotations
import gzip, re, sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STAMP = "2026-09-09_how-many-of-the-record-s-PUBLISHED-parent-COMPARISONS-are-GROSS-UNMATCHED_C"
OUT = Path(__file__).resolve().parent
COST, FREQ = 10.0, "W"
MA_WIN, VOL_WIN = 200, 20
QWIN, QMIN = 1260, 504
IS_START, IS_END, OOS_START = "2009-01-01", "2016-12-31", "2017-01-01"
GS = (0.50, 0.75, 1.00)
DIALS = {"MA": (100, 150, 200, 250), "VOL": (0.35, 0.45, 0.60, 0.90),
         "BAND": (0.00, 0.03, 0.06, 0.10), "BREADTH": (0.10, 0.20, 0.35, 0.50),
         "SPYTR": (0.10, 0.20, 0.35, 0.50), "DD": (0.10, 0.20, 0.35, 0.50)}
FAMS = tuple(DIALS)
NAME_LEVEL = {"MA", "VOL", "BAND"}
# arms = (family, gross convention).  DG = gated weight to CASH; RS = re-spread over survivors.
ARMS = tuple([(f, "DG") for f in FAMS] + [(f, "RS") for f in ("MA", "VOL", "BAND")])

_LOG: list[str] = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); _LOG.append(s)


# ============================================================ vectorised engine clone (idea 317)
def fast_bt(px: pd.DataFrame, W: pd.DataFrame, cost_bps=COST, freq=FREQ):
    """Closed-form equivalent of engine.backtest: same t+1 application, same weekly schedule,
    same intra-period drift with cash flat, same turnover-based cost."""
    idx = px.index
    rets = px.pct_change().fillna(0.0).to_numpy(float)
    wt = W.reindex(idx).fillna(0.0).shift(1).fillna(0.0).to_numpy(float)
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).to_numpy(bool).copy()
    mask[0] = True
    T, N = rets.shape
    Cs = np.empty((T, N)); Cs[0] = 1.0
    np.cumprod(1.0 + rets[:-1], axis=0, out=Cs[1:])
    starts = np.flatnonzero(mask)
    seg = np.searchsorted(starts, np.arange(T), side="right") - 1
    s_of_t = starts[seg]
    new = wt[s_of_t]
    num = new * (Cs / Cs[s_of_t])
    D = num.sum(axis=1) + (1.0 - new.sum(axis=1))
    held = num / D[:, None]
    turn = np.zeros(T); turn[0] = np.abs(wt[0]).sum()
    later = starts[1:]
    if len(later):
        sp = starts[seg[later] - 1]
        prev_new = wt[sp]
        np_ = prev_new * (Cs[later] / Cs[sp])
        Dp = np_.sum(axis=1) + (1.0 - prev_new.sum(axis=1))
        turn[later] = np.abs(wt[later] - np_ / Dp[:, None]).sum(axis=1)
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return pd.Series(port, index=idx), pd.Series(held.sum(axis=1), index=idx)


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def mrow(r):
    m = metrics(r); h1, h2 = halves(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def mean_target_gross(W: pd.DataFrame, start=None) -> float:
    """Mean gross of the TARGET weights on rebalance days, over the SCORED window only (the
    warm-up rows are zero for every book and would bias the match if included)."""
    rb = rebalance_mask(W.index, FREQ)
    g = W.loc[rb].sum(axis=1)
    if start is not None:
        g = g.loc[start:]
    return float(g.mean())


# ============================================================ PART A — census of the record
CMP_COLS = {"arm", "book", "control", "leg", "variant", "kind", "flavour", "flavor", "family"}
DELTA_RE = re.compile(r"^(d|delta_?|gap_?)(sharpe|cagr|maxdd|dd)$|"
                      r"^(dsharpe|dcagr|dmaxdd|delta|gap|edge|diff|premium)")
DEGROSS_RE = re.compile(r"\.where\([^\n]{0,140}?,\s*0(\.0+)?\)|to CASH|de-?gross|degross", re.I)
RESPREAD_RE = re.compile(r"re-?spread|renormalis|renormaliz", re.I)
MATCH_RE = re.compile(r"matched[ -]gross|match_gross|matched gross|rescal", re.I)


def _read_head(f: Path):
    op = gzip.open if f.name.endswith(".gz") else open
    with op(f, "rt", errors="replace") as fh:
        return [c.strip().strip('"').lower() for c in fh.readline().split(",")]


def census():
    """Every committed CSV that publishes a clause-vs-control comparison, tiered by what the
    file lets a reader check about the two arms' gross."""
    files = sorted([p for p in OUT.glob("*.csv")] + [p for p in OUT.glob("*.csv.gz")])
    stem_re = re.compile(r"\.[A-Za-z0-9_]+\.csv(\.gz)?$")
    src_cache: dict[str, tuple[bool, bool, bool]] = {}
    rows = []
    for f in files:
        try:
            cols = _read_head(f)
        except Exception:
            continue
        is_cmp = any(c in CMP_COLS for c in cols) or any(DELTA_RE.match(c) for c in cols)
        if not is_cmp:
            continue
        gcols = [c for c in cols if "gross" in c or c in ("exposure", "expo")]
        stem = stem_re.sub("", f.name)
        if stem not in src_cache:
            py = OUT / f"{stem}.py"
            txt = py.read_text(errors="replace") if py.exists() else ""
            src_cache[stem] = (bool(DEGROSS_RE.search(txt)), bool(RESPREAD_RE.search(txt)),
                               bool(MATCH_RE.search(txt)))
        dg, rs, mg = src_cache[stem]
        # does the file itself show the arms at different gross?
        arms_differ = False
        if gcols:
            try:
                op = gzip.open if f.name.endswith(".gz") else open
                with op(f, "rt", errors="replace") as fh:
                    df = pd.read_csv(fh, usecols=lambda c: c.strip().strip('"').lower() in gcols,
                                     nrows=200000)
                df.columns = [c.strip().strip('"').lower() for c in df.columns]
                for c in df.columns:
                    v = pd.to_numeric(df[c], errors="coerce").dropna()
                    if v.nunique() > 1:
                        arms_differ = True
            except Exception:
                pass
        tier = ("T1_visibly_unmatched" if (gcols and arms_differ) else
                "T2_nominal_matched" if gcols else "T3_no_gross_published")
        rows.append(dict(file=f.name, stem=stem, n_cols=len(cols), gross_cols=";".join(gcols),
                         tier=tier, src_degross=dg, src_respread=rs, src_matched_language=mg,
                         realised_unmatched=bool(dg or (bool(gcols) and arms_differ))))
    return pd.DataFrame(rows)


# ============================================================ PART B — books
def build_panel(px: pd.DataFrame, tradable: np.ndarray):
    elig = px.notna() & pd.DataFrame(np.tile(tradable, (len(px), 1)), index=px.index,
                                     columns=px.columns)
    vol20 = px.pct_change().rolling(VOL_WIN).std() * np.sqrt(252)
    ma200 = (px > px.rolling(MA_WIN).mean()) & elig
    n = elig.sum(axis=1).replace(0, np.nan)
    breadth = (ma200.sum(axis=1) / n).ffill()
    spytr = px["SPY"] / px["SPY"].rolling(MA_WIN).mean() - 1.0
    return elig, vol20, breadth, spytr


def ew(mask: pd.DataFrame, g: float) -> pd.DataFrame:
    n = mask.sum(axis=1).replace(0, np.nan)
    return g * mask.astype(float).div(n, axis=0).fillna(0.0)


def roll_q_mask(sig: pd.Series, q: float) -> pd.Series:
    """Risk-off (gate fires) when the signal is below its own trailing 5y q-quantile."""
    thr = sig.rolling(QWIN, min_periods=QMIN).quantile(q)
    return (sig < thr).fillna(False)


def clause_weights(fam, form, dial, g, px, elig, vol20, breadth, spytr, ctrl_ret):
    """The clause book.  form='DG' sends the gated weight to CASH (denominator = ALL eligible
    names, so gross falls with the gate — the RULES v2 form).  form='RS' re-spreads over the
    survivors (denominator = the kept names), which holds gross at g by construction and is
    therefore gross-matched to the control for free."""
    ctrl = ew(elig, g)
    if fam in NAME_LEVEL:
        if fam == "MA":
            keep = (px > px.rolling(int(dial)).mean()) & elig
        elif fam == "VOL":
            keep = (vol20 < dial).fillna(False) & elig
        else:
            keep = band_state(px, dial) & elig
        return ew(keep, g) if form == "RS" else ctrl.where(keep, 0.0)
    if fam == "BREADTH":
        off = roll_q_mask(breadth, dial)
    elif fam == "SPYTR":
        off = roll_q_mask(spytr, dial)
    elif fam == "DD":
        eq = (1 + ctrl_ret.reindex(px.index).fillna(0.0)).cumprod()
        off = roll_q_mask(eq / eq.cummax() - 1.0, dial)
    else:
        raise ValueError(fam)
    return ctrl.where(~off, 0.0)


def keep_paths(m, mo, b, bo, s, so):
    """4a vs RULES v2 (full-sample halves + MaxDD), 4b vs SPY (halves + OOS + DD + CAGR)."""
    p4a = (m["H1"] > b["H1"]) and (m["H2"] > b["H2"]) and (m["MaxDD"] >= b["MaxDD"])
    p4b = ((m["H1"] > s["H1"]) and (m["H2"] > s["H2"]) and (mo["Sharpe"] > so["Sharpe"])
           and (m["MaxDD"] >= 0.60 * s["MaxDD"]) and (m["CAGR"] >= 0.70 * s["CAGR"]))
    return bool(p4a), bool(p4b)


def run_panel(pname, px, tradable, cells, wfrows, kprows):
    t0 = time.time()
    elig, vol20, breadth, spytr = build_panel(px, tradable)
    start = px.index[max(260, MA_WIN + 20)]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    b2, _ = fast_bt(px, rules_v2_weights(px)); b2 = b2.loc[start:]
    P(f"\nPANEL {pname}: {len(px.columns)} cols, {int(tradable.sum())} tradable, "
      f"{px.index[0].date()}..{px.index[-1].date()} ({len(px)} rows), scored from {start.date()}")
    M_spy, M_b2 = mrow(spy), mrow(b2)
    P(f"  SPY      CAGR {M_spy['CAGR']:7.2%} Sharpe {M_spy['Sharpe']:6.3f} MaxDD {M_spy['MaxDD']:7.2%}"
      f"  H1/H2 {M_spy['H1']:.3f}/{M_spy['H2']:.3f}")
    P(f"  RULESv2  CAGR {M_b2['CAGR']:7.2%} Sharpe {M_b2['Sharpe']:6.3f} MaxDD {M_b2['MaxDD']:7.2%}"
      f"  H1/H2 {M_b2['H1']:.3f}/{M_b2['H2']:.3f}")
    M_spy_o, M_b2_o = mrow(spy.loc[OOS_START:]), mrow(b2.loc[OOS_START:])

    # clause-OFF controls, one per base gross
    ctrl = {}
    for g in GS:
        W = ew(elig, g)
        r, h = fast_bt(px, W)
        ctrl[g] = dict(W=W, r=r.loc[start:], r_full=r, tg=mean_target_gross(W, start),
                       held=float(h.loc[start:].mean()))
        P(f"  control EWall g={g:.2f}  meanTargetGross {ctrl[g]['tg']:.4f}  meanHeldGross "
          f"{ctrl[g]['held']:.4f}  Sharpe {metrics(ctrl[g]['r'])['Sharpe']:.3f}")

    for fam, form in ARMS:
        for g in GS:
            for dial in DIALS[fam]:
                Wc = clause_weights(fam, form, dial, g, px, elig, vol20, breadth, spytr,
                                    ctrl[g]["r_full"])
                rc, hc = fast_bt(px, Wc)
                rc = rc.loc[start:]
                tg_c = mean_target_gross(Wc, start)
                k = tg_c / ctrl[g]["tg"]
                Wm = ctrl[g]["W"] * k
                assert float(Wm.sum(axis=1).max()) <= 1.0 + 1e-9, "scaled control exceeds gross 1"
                assert abs(mean_target_gross(Wm, start) - tg_c) < 1e-12, "G2 matched-gross failure"
                rm, hm = fast_bt(px, Wm)
                rm = rm.loc[start:]
                A, U, Mm = mrow(rc), mrow(ctrl[g]["r"]), mrow(rm)
                Ao, Uo, Mo = (mrow(rc.loc[OOS_START:]), mrow(ctrl[g]["r"].loc[OOS_START:]),
                              mrow(rm.loc[OOS_START:]))
                Ai, Ui, Mi = (mrow(rc.loc[IS_START:IS_END]), mrow(ctrl[g]["r"].loc[IS_START:IS_END]),
                              mrow(rm.loc[IS_START:IS_END]))
                row = dict(panel=pname, family=fam, form=form, dial=dial, gross=g,
                           tg_clause=tg_c, tg_ctrl=ctrl[g]["tg"], k=k,
                           held_clause=float(hc.loc[start:].mean()), held_ctrl=ctrl[g]["held"],
                           gross_gap=ctrl[g]["tg"] - tg_c,
                           fire_rate=float((Wc.sum(axis=1) < ctrl[g]["W"].sum(axis=1) - 1e-12)
                                           .loc[start:].mean()))
                for tag, d in (("clause", A), ("ctrlU", U), ("ctrlM", Mm)):
                    for kk, vv in d.items():
                        row[f"{tag}_{kk}"] = vv
                for m in ("Sharpe", "CAGR", "MaxDD"):
                    row[f"dU_{m}"] = A[m] - U[m]
                    row[f"dM_{m}"] = A[m] - Mm[m]
                    row[f"flip_{m}"] = bool(np.sign(row[f"dU_{m}"]) != np.sign(row[f"dM_{m}"]))
                row["clause_oCAGR"], row["clause_oSharpe"], row["clause_oMaxDD"] = (
                    Ao["CAGR"], Ao["Sharpe"], Ao["MaxDD"])
                row["dU_Sharpe_IS"] = Ai["Sharpe"] - Ui["Sharpe"]
                row["dM_Sharpe_IS"] = Ai["Sharpe"] - Mi["Sharpe"]
                row["dU_Sharpe_OOS"] = Ao["Sharpe"] - Uo["Sharpe"]
                row["dM_Sharpe_OOS"] = Ao["Sharpe"] - Mo["Sharpe"]
                cells.append(row)

    df = pd.DataFrame([c for c in cells if c["panel"] == pname])
    P(f"  {len(df)} comparisons on {pname}  "
      f"({len(ARMS)} arms x {len(GS)} gross x 4 dials)   [{time.time()-t0:.1f}s]")
    P("  arm          gross gap  fire rate | dSharpe unmatched -> matched | sign flips S / C / DD")
    for fam, form in ARMS:
        d = df[(df.family == fam) & (df.form == form)]
        P(f"  {fam+'-'+form:11s}  {d.gross_gap.mean():+.4f}     {d.fire_rate.mean():5.1%}   |  "
          f"{d.dU_Sharpe.mean():+.4f} -> {d.dM_Sharpe.mean():+.4f}        |  "
          f"{int(d.flip_Sharpe.sum()):2d} / {int(d.flip_CAGR.sum()):2d} / {int(d.flip_MaxDD.sum()):2d}"
          f"  of {len(d)}")

    # ------------------------------------------------ rule 8 walk-forward, both conventions
    for fam, form in ARMS:
        d = df[(df.family == fam) & (df.form == form)]
        for conv, col in (("UNMATCHED", "dU_Sharpe_IS"), ("MATCHED", "dM_Sharpe_IS")):
            pick = d.loc[d[col].idxmax()]
            g, dial = pick.gross, pick.dial
            Wc = clause_weights(fam, form, dial, g, px, elig, vol20, breadth, spytr,
                                ctrl[g]["r_full"])
            rc, _ = fast_bt(px, Wc); rc = rc.loc[start:]
            tg_c = mean_target_gross(Wc, start)
            Wm = ctrl[g]["W"] * (tg_c / ctrl[g]["tg"])
            rm, _ = fast_bt(px, Wm); rm = rm.loc[start:]
            A, Ao = mrow(rc), mrow(rc.loc[OOS_START:])
            Uo, Mo = mrow(ctrl[g]["r"].loc[OOS_START:]), mrow(rm.loc[OOS_START:])
            p4a, p4b = keep_paths(A, Ao, M_b2, M_b2_o, M_spy, M_spy_o)
            wfrows.append(dict(panel=pname, family=fam, form=form, convention=conv,
                               dial=dial, gross=g,
                               IS_dU=pick.dU_Sharpe_IS, IS_dM=pick.dM_Sharpe_IS,
                               OOS_CAGR=Ao["CAGR"], OOS_Sharpe=Ao["Sharpe"], OOS_MaxDD=Ao["MaxDD"],
                               OOS_dU_Sharpe=Ao["Sharpe"] - Uo["Sharpe"],
                               OOS_dM_Sharpe=Ao["Sharpe"] - Mo["Sharpe"],
                               sign_holds_U=bool(np.sign(pick.dU_Sharpe_IS) ==
                                                 np.sign(Ao["Sharpe"] - Uo["Sharpe"])),
                               sign_holds_M=bool(np.sign(pick.dM_Sharpe_IS) ==
                                                 np.sign(Ao["Sharpe"] - Mo["Sharpe"])),
                               base_OOS_CAGR=M_b2_o["CAGR"], base_OOS_Sharpe=M_b2_o["Sharpe"],
                               base_OOS_MaxDD=M_b2_o["MaxDD"], spy_OOS_CAGR=M_spy_o["CAGR"],
                               spy_OOS_Sharpe=M_spy_o["Sharpe"], spy_OOS_MaxDD=M_spy_o["MaxDD"],
                               full_CAGR=A["CAGR"], full_Sharpe=A["Sharpe"], full_MaxDD=A["MaxDD"],
                               H1=A["H1"], H2=A["H2"], pass4a=p4a, pass4b=p4b))
    # ------------------------------------------------ KEEP paths for every grid point
    for _, r in df.iterrows():
        A = {k: r[f"clause_{k}"] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2")}
        Ao = dict(CAGR=r["clause_oCAGR"], Sharpe=r["clause_oSharpe"], MaxDD=r["clause_oMaxDD"])
        p4a, p4b = keep_paths(A, Ao, M_b2, M_b2_o, M_spy, M_spy_o)
        kprows.append(dict(panel=pname, family=r.family, form=r.form, dial=r.dial,
                           gross=r.gross,
                           Sharpe=A["Sharpe"], H1=A["H1"], H2=A["H2"], CAGR=A["CAGR"],
                           MaxDD=A["MaxDD"], OOS_Sharpe=Ao["Sharpe"],
                           beats_base_halves=bool(A["H1"] > M_b2["H1"] and A["H2"] > M_b2["H2"]),
                           dd_ok_base=bool(A["MaxDD"] >= M_b2["MaxDD"]),
                           beats_spy_halves=bool(A["H1"] > M_spy["H1"] and A["H2"] > M_spy["H2"]),
                           oos_beats_spy=bool(Ao["Sharpe"] > M_spy_o["Sharpe"]),
                           dd_ok_spy=bool(A["MaxDD"] >= 0.60 * M_spy["MaxDD"]),
                           cagr_ok_spy=bool(A["CAGR"] >= 0.70 * M_spy["CAGR"]),
                           pass4a=p4a, pass4b=p4b))


# ============================================================ gates
def gate_g1(px, W, tag):
    r1, _ = fast_bt(px, W)
    res = backtest(px, W, cost_bps=COST, freq=FREQ)
    dr = float((r1 - res["returns"]).abs().max())
    P(f"  G1 {tag:22s} max|dReturn| = {dr:.3e}   {'PASS' if dr < 1e-12 else 'FAIL'}")
    assert dr < 1e-12


def gate_g3(px, elig):
    """A clause that never fires must give k == 1 and a zero delta."""
    g = 0.75
    W = ew(elig, g)
    null = W.where(pd.Series(True, index=px.index), 0.0)
    k = mean_target_gross(null) / mean_target_gross(W)
    r0, _ = fast_bt(px, null); r1, _ = fast_bt(px, W * k)
    d = float((r0 - r1).abs().max())
    P(f"  G3 null clause          k = {k:.12f}, max|dReturn| = {d:.3e}   "
      f"{'PASS' if abs(k - 1) < 1e-12 and d < 1e-12 else 'FAIL'}")
    assert abs(k - 1) < 1e-12 and d < 1e-12


# ============================================================ main
def main():
    t0 = time.time()
    P("=" * 112)
    P("IDEA 581 — how many published clause-vs-control comparisons are GROSS-UNMATCHED, "
      "and how many flip SIGN when matched?  (lane C)")
    P("=" * 112)

    P("\nPART A — census of the committed record")
    cen = census()
    tiers = cen.tier.value_counts()
    P(f"  {len(cen)} committed CSVs publish a clause-vs-control comparison "
      f"({cen.stem.nunique()} distinct scripts)")
    for t in ("T1_visibly_unmatched", "T2_nominal_matched", "T3_no_gross_published"):
        P(f"    {t:24s} {int(tiers.get(t, 0)):5d}  ({tiers.get(t, 0)/max(len(cen),1):5.1%})")
    P(f"  sibling script contains a DE-GROSS clause (gated weight -> cash): "
      f"{int(cen.src_degross.sum())} ({cen.src_degross.mean():.1%})")
    P(f"  sibling script mentions matched-gross / rescaling at all:         "
      f"{int(cen.src_matched_language.sum())} ({cen.src_matched_language.mean():.1%})")
    P(f"  UNMATCHED IN REALISED GROSS (visibly, or by de-gross construction): "
      f"{int(cen.realised_unmatched.sum())} ({cen.realised_unmatched.mean():.1%})")
    unaud = cen[(cen.tier == 'T3_no_gross_published') & (~cen.src_degross)]
    P(f"  neither published nor mechanically classifiable: {len(unaud)} "
      f"({len(unaud)/max(len(cen),1):.1%}) — the census FLOOR, not a claim of matching")
    cen.to_csv(OUT / f"{STAMP}.census.csv", index=False)

    P("\nPART B — the sign test")
    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS_all = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    scols = [c for c in pxS_all.columns if c != "SPY" and c not in bad]
    pxS = pxS_all[scols + ["SPY"]].dropna(how="all").ffill()
    panels = [("U56", pxU, np.ones(len(pxU.columns), bool)),
              ("B136", pxB, np.ones(len(pxB.columns), bool)),
              ("SMALL439", pxS, np.array([c != "SPY" for c in pxS.columns]))]
    P(f"  SMALL panel: dropped {len([c for c in pxS_all.columns if c != 'SPY']) - len(scols)} "
      f"names with max_1d_move >= 1.0 -> {len(scols)} tradable.")
    P("  SURVIVORSHIP: B136 and SMALL439 are CURRENT constituents; every LEVEL is biased up. "
      "All deltas are clause-vs-its-own-control on a fixed panel.")

    P("\nGATES")
    for nm, px, tr in panels:
        el, *_ = build_panel(px, tr)
        gate_g1(px, ew(el, 0.75), f"{nm}/EWall")
    el_u, vol_u, br_u, sp_u = build_panel(pxU, panels[0][2])
    r_ctrl_u, _ = fast_bt(pxU, ew(el_u, 0.75))
    gate_g1(pxU, clause_weights("MA", "DG", 200, 0.75, pxU, el_u, vol_u, br_u, sp_u, r_ctrl_u),
            "U56/MA-DG")
    gate_g1(pxU, clause_weights("MA", "RS", 200, 0.75, pxU, el_u, vol_u, br_u, sp_u, r_ctrl_u),
            "U56/MA-RS")
    gate_g1(pxU, rules_v2_weights(pxU), "U56/RULES v2")
    gate_g3(pxU, el_u)

    cells, wfrows, kprows = [], [], []
    for nm, px, tr in panels:
        run_panel(nm, px, tr, cells, wfrows, kprows)

    df = pd.DataFrame(cells); wf = pd.DataFrame(wfrows); kp = pd.DataFrame(kprows)
    df.to_csv(OUT / f"{STAMP}.cells.csv", index=False)
    wf.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    kp.to_csv(OUT / f"{STAMP}.keeppaths.csv", index=False)

    P("\n" + "=" * 112)
    P("HEADLINE")
    P("=" * 112)
    P(f"A. Of {len(cen)} committed clause-vs-control comparison CSVs, "
      f"{int((cen.tier=='T1_visibly_unmatched').sum())} are VISIBLY unmatched, "
      f"{int((cen.tier=='T2_nominal_matched').sum())} publish a gross the arms agree on, and "
      f"{int((cen.tier=='T3_no_gross_published').sum())} publish no gross at all.")
    P(f"   {cen.realised_unmatched.mean():.1%} are unmatched in REALISED gross once de-gross "
      f"clauses are counted; only {cen.src_matched_language.mean():.1%} of the files come from a "
      f"script that mentions matching at all.")
    n = len(df)
    P(f"B. {n} rebuilt comparisons ({len(ARMS)} arms x 4 dials x 3 gross x 3 panels).  "
      f"Mean gross gap {df.gross_gap.mean():+.4f} of nominal; every family's control holds MORE.")
    for m in ("Sharpe", "CAGR", "MaxDD"):
        f_ = df[f"flip_{m}"].sum()
        P(f"   d{m:6s} unmatched {df[f'dU_{m}'].mean():+.4f} -> matched {df[f'dM_{m}'].mean():+.4f}"
          f"   SIGN FLIPS {int(f_):4d}/{n} = {f_/n:.1%}")
    P(f"   flips on ANY of the three metrics: "
      f"{int((df.flip_Sharpe | df.flip_CAGR | df.flip_MaxDD).sum())}/{n} = "
      f"{(df.flip_Sharpe | df.flip_CAGR | df.flip_MaxDD).mean():.1%}")
    win_u = (df.dU_Sharpe > 0).mean(); win_m = (df.dM_Sharpe > 0).mean()
    P(f"   share of comparisons where the clause WINS on Sharpe: unmatched {win_u:.1%} -> "
      f"matched {win_m:.1%}")
    dd_u = (df.dU_MaxDD > 0).mean(); dd_m = (df.dM_MaxDD > 0).mean()
    P(f"   share where the clause wins on DRAWDOWN (idea 48's metric): unmatched {dd_u:.1%} -> "
      f"matched {dd_m:.1%}")
    P(f"C. rule 8: {len(wf)} walk-forward picks (6 families x 3 panels x 2 conventions).  "
      f"IS sign holds OOS: unmatched {wf.sign_holds_U.mean():.1%}, matched {wf.sign_holds_M.mean():.1%}.")
    P(f"   KEEP paths on the OOS picks: 4a {int(wf.pass4a.sum())}/{len(wf)}, "
      f"4b {int(wf.pass4b.sum())}/{len(wf)}")
    P(f"   KEEP paths over ALL {len(kp)} grid points (no selection): 4a {int(kp.pass4a.sum())}, "
      f"4b {int(kp.pass4b.sum())}")
    if int(kp.pass4b.sum()):
        P(kp[kp.pass4b][["panel", "family", "form", "dial", "gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                         "OOS_Sharpe"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\nWALK-FORWARD (all picks)")
    P(wf[["panel", "family", "form", "convention", "dial", "gross", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
          "spy_OOS_Sharpe", "base_OOS_Sharpe", "OOS_dU_Sharpe", "OOS_dM_Sharpe",
          "pass4a", "pass4b"]].to_string(index=False,
                                         float_format=lambda x: f"{x:.4f}"))
    P(f"\ndone in {time.time()-t0:.1f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
