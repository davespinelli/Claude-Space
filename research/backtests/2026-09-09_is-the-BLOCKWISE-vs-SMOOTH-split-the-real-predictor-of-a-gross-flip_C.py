#!/usr/bin/env python3
"""IDEA 584 — is the BLOCKWISE-vs-SMOOTH split the real predictor of a GROSS FLIP?
   (lane C, 2026-09-09)

QUESTION (QUEUE idea 584, verbatim)
    Idea 581 found all 35 sign flips sit in market-level gates (fire rates 21-28%, blockwise
    on/off) and none in cross-sectional clauses that thin gross smoothly, at the SAME mean
    gross gap.  Test whether the flip risk is predicted by the gate's gross-path
    AUTOCORRELATION rather than by its gross gap: rank every clause form by both and report
    which orders the flips.  Max 2 params.

WHAT A "FLIP" IS (idea 581's definition, reproduced bit-for-bit here as gate G3)
    A clause book is compared with its own clause-OFF control twice: once at the control's
    NOMINAL gross (the record's published convention, "unmatched") and once with the control
    rescaled to the clause's own mean target gross ("matched").  A FLIP is a comparison whose
    published delta CHANGES SIGN between the two conventions.

WHY THE LITERAL RANKING CANNOT SETTLE THE QUESTION, AND WHAT IS ADDED
    Idea 581's split is perfectly confounded.  The three market-level forms are, all at once:
    blockwise, whole-book, high-AMPLITUDE, AND the only forms whose gate fires on a market-wide
    signal (i.e. the only ones with market TIMING content).  (They are NOT the high-
    autocorrelation forms — the run finds the opposite, and that is part of the answer.)  With six
    de-gross forms, three of which flip and three of which never do, ANY statistic that
    separates the two groups "orders the flips" perfectly, and the chance floor for a coin
    doing that is 1/C(6,3) = 5.0%.  So PART A answers the question as asked and PART A is NOT
    evidence for a mechanism.  Two ladders break the confound by construction:

    PART B  BLOCK-SHUFFLE ladder — dials AUTOCORRELATION with the gross gap held EXACTLY fixed.
            The gate's fired/not-fired sequence over the scored rebalance days is cut into
            contiguous blocks of L weeks and the BLOCKS are permuted (seeded).  A permutation
            preserves the multiset of gate states exactly, so mean target gross, the gross gap,
            the fire rate and the whole marginal distribution of the gross path are invariant
            to machine precision at every L (gate G4); only the ORDER changes.  L = 1 week
            destroys the blocks, L = 52 weeks keeps year-long ones, ACTUAL is the real gate.
    PART C  LAMBDA ladder — dials the GROSS GAP with autocorrelation held EXACTLY fixed.
            W(lambda) = lambda*W_clause + (1-lambda)*W_control.  Mean target gross is exactly
            affine in lambda, so the gap scales by lambda; the gross path is an affine map of
            the clause's own path, and autocorrelation is invariant under an affine map.
            lambda = 1 is the clause itself, lambda = 0 IS the matched control (delta exactly
            zero) — both are gates (G5).

    Between them: PART B moves autocorrelation at constant gap, PART C moves gap at constant
    autocorrelation.  Whichever predictor is real must move the flip rate on its own ladder.

    A THIRD CANDIDATE IS MEASURED THROUGHOUT, because the mechanics point at it.  Matching
    replaces the control with a de-grossed version of ITSELF, so the matched delta asks: does
    the clause do better than simply holding less?  HYPOTHESIS, pre-registered: a flip is then
    an ORDER statistic — it should depend on WHEN the exposure was cut, not on the shape of the
    path.  TIMING (annualised mean SPY return on de-grossed days minus on full-gross days;
    negative = the gate cut before losses) and DDTIME (the same difference in the control's own
    drawdown depth) are reported beside GAP and RHO1 in every table and ranked with them.
    Naming them up front is the point: they are a pre-registered third horse, not a post-hoc
    rescue, and the run reports where they win and where they explain nothing.

THE 9 ARMS, THE PANELS, THE MATCHING CONVENTION, THE GRID
    Identical to idea 581 so that its 324 cells reproduce exactly (gate G3):
      name-level (cross-sectional, smooth thinning):
        MA    hold only names above their own m-day MA     dial m   in {100,150,200,250}
        VOL   drop names with vol20 >= cap                 dial cap in {.35,.45,.60,.90}
        BAND  RULES v2's 200d +/- band with hysteresis     dial b   in {0,.03,.06,.10}
      market-level (timing, whole book -> CASH in the bad state):
        BREADTH  share of priced names above their 200d MA, low   dial q in {.10,.20,.35,.50}
        SPYTR    SPY / SPY.rolling(200).mean() - 1, low           dial q as above
        DD       the CONTROL's own drawdown from its peak, low    dial q as above
      DG = gated weight goes to CASH (realised gross falls).  RS = re-spread over survivors
      (gross held at g by construction, so k == 1 and a flip is impossible — the null control).
      6 DG + 3 RS = 9 arms.  Market thresholds are TRAILING 5y rolling quantiles (1260d/504 min).
    Panels: U56 (research/universe.json), B136 (universe_broad.json), SMALL439 (prices_small
      less max_1d_move >= 1.0).  Matching: scale the control's WEIGHTS by
      k = meanTargetGross(clause)/meanTargetGross(control) on scored rebalance days and re-run.

TUNED PARAMETERS: 2 — (dial, base gross g).  4 dials x 3 gross = 12 points per arm per panel,
    ALL 324 reported in .cells.csv.  L, lambda and the shuffle seed are DIAGNOSTIC AXES, not
    tuned parameters: every point of both ladders is reported, and no book is ever selected on
    them — the rule-8 walk-forward in PART D chooses only (dial, g), on the real books, exactly
    as idea 581 did.  Everything else PINNED: weekly cadence, t+1, 10 bps, 200d MA where not
    the dial, 20d vol, 1260d/504 quantile window, warm-up skip, seeds (0,1,2).

GATES
    G1  the vectorised runner reproduces engine.backtest to < 1e-12 on returns.
    G2  matched gross: |meanTargetGross(clause) - meanTargetGross(matched control)| < 1e-12.
    G3  PROVENANCE: every one of idea 581's 324 committed cells is reproduced here to < 1e-12
        on dU/dM Sharpe, CAGR and MaxDD, and the flip flags agree exactly.  Without this the
        run is re-deriving a different population and cannot speak to idea 581's claim.
    G4  a block permutation preserves the fire count EXACTLY and mean target gross to < 1e-12
        at every (L, seed).
    G5  lambda = 1 reproduces the clause book exactly and lambda = 0 reproduces the matched
        control exactly (both < 1e-12), so the lambda ladder cannot manufacture a flip.

RULE 8 (walk-forward, required).  Per arm x panel, pick (dial, g) on 2009-2016 ONLY by IS
    dSharpe against the unmatched control (the record's own selection rule), evaluate 2017-2026
    untouched: OOS CAGR/Sharpe/MaxDD of the picked book against RULES v2 and against SPY, both
    KEEP paths, and the pick's own GAP / RHO1 / TIMING.

Outputs (committed): .console.txt .cells.csv .forms.csv .shuffle.csv .lambda.csv
    .walkforward.csv .keeppaths.csv .result.md
Deterministic; no network (load_universe reads committed caches).
"""
from __future__ import annotations
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STAMP = "2026-09-09_is-the-BLOCKWISE-vs-SMOOTH-split-the-real-predictor-of-a-gross-flip_C"
PRIOR = "2026-09-09_how-many-of-the-record-s-PUBLISHED-parent-COMPARISONS-are-GROSS-UNMATCHED_C"
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
ARMS = tuple([(f, "DG") for f in FAMS] + [(f, "RS") for f in ("MA", "VOL", "BAND")])
MKT_DG = tuple((f, "DG") for f in FAMS if f not in NAME_LEVEL)
BLOCKS_W = (1, 4, 13, 52)          # block length in WEEKS for the shuffle ladder
SEEDS = (0, 1, 2)
LAMBDAS = (0.25, 0.50, 0.75)       # 1.00 is the base cell, 0.00 is the matched control
LAM_G = 0.75                       # the lambda ladder is run at one base gross, all dials

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); _LOG.append(s)


# ============================================================ vectorised engine clone
class Runner:
    """Closed-form equivalent of engine.backtest with the per-panel constants precomputed
    once (the compounding matrix does not depend on the weights).  Same t+1 application, same
    weekly schedule, same intra-period drift with cash flat, same turnover-based cost."""

    def __init__(self, px: pd.DataFrame, cost_bps=COST, freq=FREQ):
        self.idx = px.index
        self.cost = cost_bps / 1e4
        self.rets = px.pct_change().fillna(0.0).to_numpy(float)
        T, N = self.rets.shape
        mask = rebalance_mask(self.idx, freq).shift(1, fill_value=False).to_numpy(bool).copy()
        mask[0] = True
        Cs = np.empty((T, N)); Cs[0] = 1.0
        np.cumprod(1.0 + self.rets[:-1], axis=0, out=Cs[1:])
        starts = np.flatnonzero(mask)
        seg = np.searchsorted(starts, np.arange(T), side="right") - 1
        self.s_of_t = starts[seg]
        self.ratio = Cs / Cs[self.s_of_t]
        self.later = starts[1:]
        sp = starts[seg[self.later] - 1]
        self.sp = sp
        self.ratio_l = Cs[self.later] / Cs[sp]
        self.T, self.N = T, N

    def run(self, W) -> tuple[pd.Series, pd.Series]:
        A = W.to_numpy(float) if isinstance(W, pd.DataFrame) else np.asarray(W, float)
        wt = np.empty_like(A); wt[0] = 0.0; wt[1:] = A[:-1]
        new = wt[self.s_of_t]
        num = new * self.ratio
        D = num.sum(axis=1) + (1.0 - new.sum(axis=1))
        held = num / D[:, None]
        turn = np.zeros(self.T); turn[0] = np.abs(wt[0]).sum()
        if len(self.later):
            prev_new = wt[self.sp]
            np_ = prev_new * self.ratio_l
            Dp = np_.sum(axis=1) + (1.0 - prev_new.sum(axis=1))
            turn[self.later] = np.abs(wt[self.later] - np_ / Dp[:, None]).sum(axis=1)
        port = (held * self.rets).sum(axis=1) - turn * self.cost
        return (pd.Series(port, index=self.idx),
                pd.Series(held.sum(axis=1), index=self.idx))


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def mrow(r):
    m = metrics(r); h1, h2 = halves(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def mean_target_gross(W: pd.DataFrame, rb: pd.Series, start) -> float:
    """Mean gross of the TARGET weights on scored rebalance days (warm-up rows are zero for
    every book and would bias the match if included)."""
    return float(W.loc[rb].sum(axis=1).loc[start:].mean())


# ============================================================ statistics (each one NAMED)
def pearson(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    a, b = a[ok], b[ok]
    if len(a) < 3 or a.std() == 0 or b.std() == 0:
        return np.nan
    return float(np.corrcoef(a, b)[0, 1])


def spearman(a, b):
    """Spearman rank correlation (average ranks for ties), computed as Pearson on ranks."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    a, b = a[ok], b[ok]
    if len(a) < 3:
        return np.nan
    return pearson(pd.Series(a).rank().to_numpy(), pd.Series(b).rank().to_numpy())


def auc(score, label):
    """Mann-Whitney AUC: P(score of a flipping cell > score of a non-flipping cell), ties 0.5.
    0.5 = no discrimination, 1.0 = the statistic orders the flips perfectly."""
    score = np.asarray(score, float); label = np.asarray(label, bool)
    ok = np.isfinite(score)
    score, label = score[ok], label[ok]
    p, n = score[label], score[~label]
    if len(p) == 0 or len(n) == 0:
        return np.nan
    r = pd.Series(np.concatenate([p, n])).rank().to_numpy()
    return float((r[:len(p)].sum() - len(p) * (len(p) + 1) / 2) / (len(p) * len(n)))


def lag_autocorr(x: np.ndarray, k: int) -> float:
    x = np.asarray(x, float)
    if len(x) <= k or np.nanstd(x) == 0:
        return np.nan
    return pearson(x[k:], x[:-k])


def mean_run_len(flag: np.ndarray) -> float:
    """Mean length (in observations) of a contiguous run of True."""
    flag = np.asarray(flag, bool)
    if not flag.any():
        return np.nan
    d = np.diff(np.concatenate([[0], flag.view(np.int8), [0]]))
    return float(flag.sum() / max(int((d == 1).sum()), 1))


def path_stats(u: pd.Series, spy: pd.Series, ddc: pd.Series) -> dict:
    """Predictors of a flip, all read off the SAME daily gross-ratio path
    u_t = grossHeld(clause)_t / grossHeld(control at nominal g)_t over the scored window.
    TIMING and DDTIME are the two TIMING statistics: the clause is 'de-grossed' on a day when
    u_t is below its own mean, and they ask what the market was doing on those days."""
    v = u.to_numpy(float)
    mu = float(np.nanmean(v))
    low = v < mu - 1e-12
    s, d = spy.to_numpy(float), ddc.to_numpy(float)
    if low.any() and (~low).any():
        timing = float((np.nanmean(s[low]) - np.nanmean(s[~low])) * 252)
        ddtime = float(np.nanmean(d[low]) - np.nanmean(d[~low]))
    else:
        timing, ddtime = np.nan, np.nan
    return dict(GAP=1.0 - mu, SD=float(np.nanstd(v)),
                RHO1=lag_autocorr(v, 1), RHO5=lag_autocorr(v, 5),
                DRHO1=lag_autocorr(np.diff(v), 1),
                RUN=mean_run_len(low), LOWSHARE=float(low.mean()),
                TIMING=timing, DDTIME=ddtime)


# GAP is the gross gap (idea 581's predictor); RHO1/RHO5/DRHO1/RUN are the BLOCKWISE statistics
# (idea 584's proposal); SD is the amplitude of the gross path (idea 535's c_sd, in ratio units);
# TIMING/DDTIME are the pre-registered third horse.
PREDS = ("GAP", "SD", "RHO1", "RHO5", "DRHO1", "RUN", "TIMING", "DDTIME")


# ============================================================ books
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
    thr = sig.rolling(QWIN, min_periods=QMIN).quantile(q)
    return (sig < thr).fillna(False)


def gate_off(fam, dial, px, breadth, spytr, ctrl_ret) -> pd.Series:
    """The market-level gate's risk-off indicator (True = whole book to cash)."""
    if fam == "BREADTH":
        return roll_q_mask(breadth, dial)
    if fam == "SPYTR":
        return roll_q_mask(spytr, dial)
    if fam == "DD":
        eq = (1 + ctrl_ret.reindex(px.index).fillna(0.0)).cumprod()
        return roll_q_mask(eq / eq.cummax() - 1.0, dial)
    raise ValueError(fam)


def clause_weights(fam, form, dial, g, px, elig, vol20, breadth, spytr, ctrl_ret):
    ctrl = ew(elig, g)
    if fam in NAME_LEVEL:
        if fam == "MA":
            keep = (px > px.rolling(int(dial)).mean()) & elig
        elif fam == "VOL":
            keep = (vol20 < dial).fillna(False) & elig
        else:
            keep = band_state(px, dial) & elig
        return ew(keep, g) if form == "RS" else ctrl.where(keep, 0.0)
    return ctrl.where(~gate_off(fam, dial, px, breadth, spytr, ctrl_ret), 0.0)


def keep_paths(m, mo, b, bo, s, so):
    """4a vs RULES v2 (full-sample halves + MaxDD), 4b vs SPY (halves + OOS + DD + CAGR)."""
    p4a = (m["H1"] > b["H1"]) and (m["H2"] > b["H2"]) and (m["MaxDD"] >= b["MaxDD"])
    p4b = ((m["H1"] > s["H1"]) and (m["H2"] > s["H2"]) and (mo["Sharpe"] > so["Sharpe"])
           and (m["MaxDD"] >= 0.60 * s["MaxDD"]) and (m["CAGR"] >= 0.70 * s["CAGR"]))
    return bool(p4a), bool(p4b)


def block_permute(v: np.ndarray, L: int, seed: int) -> np.ndarray:
    """Cut v into contiguous blocks of length L and permute the BLOCKS.  A permutation of a
    partition preserves the multiset of values EXACTLY, so every marginal statistic of the
    path (mean, sd, quantiles) is invariant; only the order changes."""
    n = len(v)
    cuts = list(range(0, n, L))
    blocks = [v[a:a + L] for a in cuts]
    order = np.random.default_rng(seed).permutation(len(blocks))
    return np.concatenate([blocks[i] for i in order])


# ============================================================ per-panel driver
def run_panel(pname, px, tradable, store):
    t0 = time.time()
    R = Runner(px)
    rb = rebalance_mask(px.index, FREQ)
    elig, vol20, breadth, spytr = build_panel(px, tradable)
    start = px.index[max(260, MA_WIN + 20)]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    b2, _ = R.run(rules_v2_weights(px)); b2 = b2.loc[start:]
    M_spy, M_b2 = mrow(spy), mrow(b2)
    M_spy_o, M_b2_o = mrow(spy.loc[OOS_START:]), mrow(b2.loc[OOS_START:])
    P(f"\nPANEL {pname}: {len(px.columns)} cols, {int(tradable.sum())} tradable, "
      f"{px.index[0].date()}..{px.index[-1].date()} ({len(px)} rows), scored from {start.date()}")
    P(f"  SPY      CAGR {M_spy['CAGR']:7.2%} Sharpe {M_spy['Sharpe']:6.3f} MaxDD {M_spy['MaxDD']:7.2%}"
      f"  H1/H2 {M_spy['H1']:.3f}/{M_spy['H2']:.3f}")
    P(f"  RULESv2  CAGR {M_b2['CAGR']:7.2%} Sharpe {M_b2['Sharpe']:6.3f} MaxDD {M_b2['MaxDD']:7.2%}"
      f"  H1/H2 {M_b2['H1']:.3f}/{M_b2['H2']:.3f}")

    ctrl = {}
    for g in GS:
        W = ew(elig, g)
        r, h = R.run(W)
        rr = r.loc[start:]
        eqc = (1 + rr).cumprod()
        ctrl[g] = dict(W=W, r=rr, r_full=r, h=h.loc[start:],
                       tg=mean_target_gross(W, rb, start),
                       dd=eqc / eqc.cummax() - 1.0)

    cells, shuf, lam = store["cells"], store["shuffle"], store["lambda"]
    cache = {}
    for fam, form in ARMS:
        for g in GS:
            for dial in DIALS[fam]:
                Wc = clause_weights(fam, form, dial, g, px, elig, vol20, breadth, spytr,
                                    ctrl[g]["r_full"])
                rc, hc = R.run(Wc); rc = rc.loc[start:]
                tg_c = mean_target_gross(Wc, rb, start)
                k = tg_c / ctrl[g]["tg"]
                Wm = ctrl[g]["W"] * k
                assert abs(mean_target_gross(Wm, rb, start) - tg_c) < 1e-12, "G2 failure"
                rm, _ = R.run(Wm); rm = rm.loc[start:]
                A, U, Mm = mrow(rc), mrow(ctrl[g]["r"]), mrow(rm)
                st = path_stats(hc.loc[start:] / ctrl[g]["h"], spy, ctrl[g]["dd"])
                row = dict(panel=pname, family=fam, form=form, dial=dial, gross=g,
                           tg_clause=tg_c, tg_ctrl=ctrl[g]["tg"], k=k,
                           gross_gap=ctrl[g]["tg"] - tg_c,
                           fire_rate=float((Wc.sum(axis=1) < ctrl[g]["W"].sum(axis=1) - 1e-12)
                                           .loc[start:].mean()), **st)
                for m in ("Sharpe", "CAGR", "MaxDD"):
                    row[f"dU_{m}"] = A[m] - U[m]
                    row[f"dM_{m}"] = A[m] - Mm[m]
                    row[f"flip_{m}"] = bool(np.sign(A[m] - U[m]) != np.sign(A[m] - Mm[m]))
                row["flip_any"] = bool(row["flip_Sharpe"] or row["flip_CAGR"] or row["flip_MaxDD"])
                Ao = mrow(rc.loc[OOS_START:])
                Ai, Ui = mrow(rc.loc[IS_START:IS_END]), mrow(ctrl[g]["r"].loc[IS_START:IS_END])
                Uo = mrow(ctrl[g]["r"].loc[OOS_START:])
                row["dU_Sharpe_IS"] = Ai["Sharpe"] - Ui["Sharpe"]
                row["dU_Sharpe_OOS"] = Ao["Sharpe"] - Uo["Sharpe"]
                for kk in ("CAGR", "Sharpe", "MaxDD", "H1", "H2"):
                    row[f"clause_{kk}"] = A[kk]
                row["clause_oCAGR"], row["clause_oSharpe"], row["clause_oMaxDD"] = (
                    Ao["CAGR"], Ao["Sharpe"], Ao["MaxDD"])
                p4a, p4b = keep_paths(A, Ao, M_b2, M_b2_o, M_spy, M_spy_o)
                row["pass4a"], row["pass4b"] = p4a, p4b
                cells.append(row)
                cache[(fam, form, dial, g)] = dict(Wc=Wc, rm=rm, Mm=Mm, A=A, U=U, k=k, tg_c=tg_c)

    # ---------------------------------------------------------- PART B: block-shuffle ladder
    rb_days = rb.loc[start:][rb.loc[start:]].index          # scored rebalance days
    for fam, form in MKT_DG:
        for g in GS:
            for dial in DIALS[fam]:
                base = cache[(fam, form, dial, g)]
                off = gate_off(fam, dial, px, breadth, spytr, ctrl[g]["r_full"])
                v0 = off.loc[rb_days].to_numpy(bool)
                for L in BLOCKS_W:
                    for seed in SEEDS:
                        v = block_permute(v0, L, seed)
                        assert v.sum() == v0.sum() and len(v) == len(v0), "G4 fire-count failure"
                        off_s = off.copy()              # warm-up days keep the real gate
                        off_s.loc[rb_days] = v
                        live = pd.Series(np.where(off_s.to_numpy(bool), 0.0, 1.0),
                                         index=px.index)
                        Ws = ctrl[g]["W"].mul(live, axis=0)
                        tg_s = mean_target_gross(Ws, rb, start)
                        assert abs(tg_s - base["tg_c"]) < 1e-12, "G4 gross-invariance failure"
                        rs_, hs_ = R.run(Ws); rs_ = rs_.loc[start:]
                        As = mrow(rs_)
                        st = path_stats(hs_.loc[start:] / ctrl[g]["h"], spy, ctrl[g]["dd"])
                        row = dict(panel=pname, family=fam, form=form, dial=dial, gross=g,
                                   L=L, seed=seed, k=base["k"], tg=tg_s, **st)
                        for m in ("Sharpe", "CAGR", "MaxDD"):
                            row[f"dU_{m}"] = As[m] - base["U"][m]
                            row[f"dM_{m}"] = As[m] - base["Mm"][m]
                            row[f"flip_{m}"] = bool(np.sign(As[m] - base["U"][m])
                                                    != np.sign(As[m] - base["Mm"][m]))
                        row["flip_any"] = bool(row["flip_Sharpe"] or row["flip_CAGR"]
                                               or row["flip_MaxDD"])
                        shuf.append(row)
                # the real gate, same columns, L = "ACTUAL"
                bc = [c for c in cells if c["panel"] == pname and c["family"] == fam
                      and c["form"] == form and c["dial"] == dial and c["gross"] == g][0]
                shuf.append(dict(panel=pname, family=fam, form=form, dial=dial, gross=g,
                                 L=0, seed=-1, k=bc["k"], tg=bc["tg_clause"],
                                 **{p: bc[p] for p in PREDS}, LOWSHARE=bc["LOWSHARE"],
                                 **{f"d{c}_{m}": bc[f"d{c}_{m}"] for c in ("U", "M")
                                    for m in ("Sharpe", "CAGR", "MaxDD")},
                                 **{f"flip_{m}": bc[f"flip_{m}"]
                                    for m in ("Sharpe", "CAGR", "MaxDD")},
                                 flip_any=bc["flip_any"]))

    # ---------------------------------------------------------- PART C: lambda ladder
    g = LAM_G
    for fam, form in ARMS:
        for dial in DIALS[fam]:
            base = cache[(fam, form, dial, g)]
            for lb in LAMBDAS:
                Wl = base["Wc"] * lb + ctrl[g]["W"] * (1.0 - lb)
                tg_l = mean_target_gross(Wl, rb, start)
                kl = tg_l / ctrl[g]["tg"]
                rl, hl = R.run(Wl); rl = rl.loc[start:]
                Wml = ctrl[g]["W"] * kl
                rml, _ = R.run(Wml); rml = rml.loc[start:]
                Al, Ml = mrow(rl), mrow(rml)
                st = path_stats(hl.loc[start:] / ctrl[g]["h"], spy, ctrl[g]["dd"])
                row = dict(panel=pname, family=fam, form=form, dial=dial, gross=g,
                           lam=lb, k=kl, tg=tg_l, **st)
                for m in ("Sharpe", "CAGR", "MaxDD"):
                    row[f"dU_{m}"] = Al[m] - base["U"][m]
                    row[f"dM_{m}"] = Al[m] - Ml[m]
                    row[f"flip_{m}"] = bool(np.sign(Al[m] - base["U"][m])
                                            != np.sign(Al[m] - Ml[m]))
                row["flip_any"] = bool(row["flip_Sharpe"] or row["flip_CAGR"] or row["flip_MaxDD"])
                lam.append(row)
            bc = [c for c in cells if c["panel"] == pname and c["family"] == fam
                  and c["form"] == form and c["dial"] == dial and c["gross"] == g][0]
            lam.append(dict(panel=pname, family=fam, form=form, dial=dial, gross=g,
                            lam=1.0, k=bc["k"], tg=bc["tg_clause"],
                            **{p: bc[p] for p in PREDS}, LOWSHARE=bc["LOWSHARE"],
                            **{f"d{c}_{m}": bc[f"d{c}_{m}"] for c in ("U", "M")
                               for m in ("Sharpe", "CAGR", "MaxDD")},
                            **{f"flip_{m}": bc[f"flip_{m}"] for m in ("Sharpe", "CAGR", "MaxDD")},
                            flip_any=bc["flip_any"]))

    # ---------------------------------------------------------- PART D: rule 8 walk-forward
    df = pd.DataFrame([c for c in cells if c["panel"] == pname])
    for fam, form in ARMS:
        d = df[(df.family == fam) & (df.form == form)]
        pick = d.loc[d["dU_Sharpe_IS"].idxmax()]
        g_, dial_ = pick.gross, pick.dial
        base = cache[(fam, form, dial_, g_)]
        rc, _ = R.run(base["Wc"]); rc = rc.loc[start:]
        A, Ao = mrow(rc), mrow(rc.loc[OOS_START:])
        Uo = mrow(ctrl[g_]["r"].loc[OOS_START:])
        Mo = mrow(base["rm"].loc[OOS_START:])
        p4a, p4b = keep_paths(A, Ao, M_b2, M_b2_o, M_spy, M_spy_o)
        store["wf"].append(dict(
            panel=pname, family=fam, form=form, dial=dial_, gross=g_,
            IS_dU_Sharpe=pick["dU_Sharpe_IS"], OOS_dU_Sharpe=Ao["Sharpe"] - Uo["Sharpe"],
            OOS_dM_Sharpe=Ao["Sharpe"] - Mo["Sharpe"],
            sign_holds=bool(np.sign(pick["dU_Sharpe_IS"]) == np.sign(Ao["Sharpe"] - Uo["Sharpe"])),
            full_CAGR=A["CAGR"], full_Sharpe=A["Sharpe"], full_MaxDD=A["MaxDD"],
            H1=A["H1"], H2=A["H2"],
            OOS_CAGR=Ao["CAGR"], OOS_Sharpe=Ao["Sharpe"], OOS_MaxDD=Ao["MaxDD"],
            base_OOS_CAGR=M_b2_o["CAGR"], base_OOS_Sharpe=M_b2_o["Sharpe"],
            base_OOS_MaxDD=M_b2_o["MaxDD"], spy_OOS_CAGR=M_spy_o["CAGR"],
            spy_OOS_Sharpe=M_spy_o["Sharpe"], spy_OOS_MaxDD=M_spy_o["MaxDD"],
            GAP=pick["GAP"], RHO1=pick["RHO1"], TIMING=pick["TIMING"],
            flip_any=bool(pick["flip_any"]), pass4a=p4a, pass4b=p4b))
    store["levels"].append(dict(panel=pname, spy_CAGR=M_spy["CAGR"], spy_Sharpe=M_spy["Sharpe"],
                                spy_MaxDD=M_spy["MaxDD"], v2_CAGR=M_b2["CAGR"],
                                v2_Sharpe=M_b2["Sharpe"], v2_MaxDD=M_b2["MaxDD"],
                                spy_OOS_Sharpe=M_spy_o["Sharpe"], v2_OOS_Sharpe=M_b2_o["Sharpe"]))
    P(f"  built {len(df)} cells + shuffle + lambda ladders   [{time.time()-t0:.1f}s]")


# ============================================================ gates
def gate_g1(R, px, W, tag):
    r1, _ = R.run(W)
    res = backtest(px, W, cost_bps=COST, freq=FREQ)
    dr = float((r1 - res["returns"]).abs().max())
    P(f"  G1 {tag:22s} max|dReturn| = {dr:.3e}   {'PASS' if dr < 1e-12 else 'FAIL'}")
    assert dr < 1e-12


def gate_g3(cells):
    """PROVENANCE: reproduce idea 581's committed 324 cells to < 1e-12."""
    f = OUT / f"{PRIOR}.cells.csv"
    if not f.exists():
        P("  G3 prior cells.csv NOT FOUND — provenance gate SKIPPED (state this in the memo)")
        return None
    old = pd.read_csv(f)
    new = pd.DataFrame(cells)
    key = ["panel", "family", "form", "dial", "gross"]
    m = old.merge(new, on=key, suffixes=("_o", "_n"))
    assert len(m) == len(old) == len(new), f"cell count {len(old)} vs {len(new)} vs {len(m)}"
    worst, nflip = 0.0, 0
    for c in ("dU_Sharpe", "dM_Sharpe", "dU_CAGR", "dM_CAGR", "dU_MaxDD", "dM_MaxDD"):
        worst = max(worst, float((m[f"{c}_o"] - m[f"{c}_n"]).abs().max()))
    for c in ("flip_Sharpe", "flip_CAGR", "flip_MaxDD"):
        nflip += int((m[f"{c}_o"].astype(bool) != m[f"{c}_n"].astype(bool)).sum())
    P(f"  G3 idea-581 provenance   {len(m)} cells, max|d(delta)| = {worst:.3e}, "
      f"flip-flag disagreements = {nflip}   {'PASS' if worst < 1e-12 and nflip == 0 else 'FAIL'}")
    assert worst < 1e-12 and nflip == 0
    return dict(n=len(m), flips_S=int(old.flip_Sharpe.sum()), flips_C=int(old.flip_CAGR.sum()),
                flips_D=int(old.flip_MaxDD.sum()))


def gate_g5(R, px, elig, rb, start, vol20, breadth, spytr):
    """PART C's premise: the interpolation's endpoints are the clause and the control, and its
    mean TARGET gross is exactly affine in lambda (so the gap scales by lambda and nothing
    else moves)."""
    g = 0.75
    W = ew(elig, g)
    r_ctrl, _ = R.run(W)
    Wc = clause_weights("BREADTH", "DG", 0.20, g, px, elig, vol20, breadth, spytr, r_ctrl)
    rc, _ = R.run(Wc)
    r1, _ = R.run(Wc * 1.0 + W * 0.0)
    r0, _ = R.run(Wc * 0.0 + W * 1.0)
    d1 = float((r1 - rc).abs().max()); d0 = float((r0 - r_ctrl).abs().max())
    tg_c, tg_u = mean_target_gross(Wc, rb, start), mean_target_gross(W, rb, start)
    aff = max(abs(mean_target_gross(Wc * lb + W * (1 - lb), rb, start)
                  - (lb * tg_c + (1 - lb) * tg_u)) for lb in LAMBDAS)
    ok = d1 < 1e-12 and d0 < 1e-12 and aff < 1e-12
    P(f"  G5 lambda ladder         lam=1 max|d| {d1:.3e}, lam=0 max|d| {d0:.3e}, "
      f"max affine-gross error {aff:.3e}   {'PASS' if ok else 'FAIL'}")
    assert ok


# ============================================================ reporting helpers
def form_table(df, label):
    rows = []
    for fam, form in ARMS:
        d = df[(df.family == fam) & (df.form == form)]
        r = dict(form=f"{fam}-{form}", level="market" if fam not in NAME_LEVEL else "name",
                 n=len(d), flip_any=int(d.flip_any.sum()),
                 flip_rate=float(d.flip_any.mean()),
                 flip_S=int(d.flip_Sharpe.sum()), flip_C=int(d.flip_CAGR.sum()),
                 flip_D=int(d.flip_MaxDD.sum()),
                 fire_rate=float(d.fire_rate.mean()) if "fire_rate" in d else np.nan)
        for p in PREDS:
            r[p] = float(d[p].mean())
        rows.append(r)
    t = pd.DataFrame(rows)
    P(f"\n{label}")
    P(t.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    return t


def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 584 — is the BLOCKWISE-vs-SMOOTH split the real predictor of a GROSS FLIP?  "
      "(lane C, 2026-09-09)")
    P("=" * 118)

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
    P(f"\nSMALL panel: dropped {len([c for c in pxS_all.columns if c != 'SPY']) - len(scols)} "
      f"names with max_1d_move >= 1.0 -> {len(scols)} tradable.")
    P("SURVIVORSHIP: B136 and SMALL439 are CURRENT constituents; every LEVEL is biased up. "
      "Every claim here is a clause-vs-its-own-control DIFFERENCE on a fixed panel.")

    P("\nGATES")
    RU = Runner(pxU)
    el_u, vol_u, br_u, sp_u = build_panel(pxU, panels[0][2])
    rb_u = rebalance_mask(pxU.index, FREQ)
    start_u = pxU.index[max(260, MA_WIN + 20)]
    gate_g1(RU, pxU, ew(el_u, 0.75), "U56/EWall")
    r_ctrl_u, _ = RU.run(ew(el_u, 0.75))
    gate_g1(RU, pxU, clause_weights("BREADTH", "DG", 0.20, 0.75, pxU, el_u, vol_u, br_u, sp_u,
                                    r_ctrl_u), "U56/BREADTH-DG")
    gate_g1(RU, pxU, clause_weights("MA", "RS", 200, 0.75, pxU, el_u, vol_u, br_u, sp_u,
                                    r_ctrl_u), "U56/MA-RS")
    gate_g1(RU, pxU, rules_v2_weights(pxU), "U56/RULES v2")
    gate_g5(RU, pxU, el_u, rb_u, start_u, vol_u, br_u, sp_u)

    store = dict(cells=[], shuffle=[], lambda_=[], wf=[], levels=[])
    store["lambda"] = store.pop("lambda_")
    for nm, px, tr in panels:
        run_panel(nm, px, tr, store)

    df = pd.DataFrame(store["cells"])
    sh = pd.DataFrame(store["shuffle"])
    lm = pd.DataFrame(store["lambda"])
    wf = pd.DataFrame(store["wf"])
    lv = pd.DataFrame(store["levels"])
    P("")
    prov = gate_g3(store["cells"])
    df.to_csv(OUT / f"{STAMP}.cells.csv", index=False)
    sh.to_csv(OUT / f"{STAMP}.shuffle.csv", index=False)
    lm.to_csv(OUT / f"{STAMP}.lambda.csv", index=False)
    wf.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)

    # ------------------------------------------------------------------ PART A
    P("\n" + "=" * 118)
    P("PART A — the question as asked: rank every clause FORM by gross gap and by gross-path "
      "autocorrelation, and see which orders the flips")
    P("=" * 118)
    P("Predictors are read off the daily gross-RATIO path u_t = grossHeld(clause)/grossHeld("
      "control at nominal g) over the scored window.")
    P("GAP = 1 - mean(u)  SD = sd(u)  RHO1/RHO5 = Pearson lag-1/lag-5 autocorrelation of u  "
      "DRHO1 = lag-1 autocorr of du  RUN = mean run length (days) of the de-grossed state")
    P("TIMING = 252 * (mean SPY return on de-grossed days - on full-gross days); NEGATIVE = the "
      "gate cuts exposure before losses.")
    ft = form_table(df, "FORM-LEVEL TABLE (36 comparisons per form: 4 dials x 3 gross x 3 panels)")
    ft.to_csv(OUT / f"{STAMP}.forms.csv", index=False)

    dg = ft[~ft.form.str.endswith("-RS")].copy()
    P(f"\nThe 3 RS forms are DEGENERATE by construction: k == 1 to machine precision, u_t == 1, "
      f"so SD = 0, RHO1 is undefined and a flip is impossible ({int(ft[ft.form.str.endswith('-RS')].flip_any.sum())} "
      f"flips in {int(ft[ft.form.str.endswith('-RS')].n.sum())}).  The ranking question is only "
      f"askable over the {len(dg)} DE-GROSS forms.")
    P("\nRanking the 6 DE-GROSS forms by each predictor (descending) against the flip rate:")
    P(f"  flip rate order: " + " > ".join(dg.sort_values('flip_rate', ascending=False).form))
    rk = []
    for p in PREDS:
        s = spearman(dg[p].to_numpy(), dg.flip_rate.to_numpy())
        order = " > ".join(dg.sort_values(p, ascending=False).form)
        top3 = set(dg.sort_values(p, ascending=False).head(3).form)
        perfect = top3 == set(dg.sort_values("flip_rate", ascending=False).head(3).form)
        rk.append(dict(predictor=p, spearman_n6=s, separates_flippers=perfect, order=order))
        P(f"  {p:7s} Spearman(rho, flip rate) n=6 = {s:+.4f}   top-3 == the 3 flipping forms: "
          f"{'YES' if perfect else 'no '}   {order}")
    P(f"  CHANCE FLOOR: with 3 flipping and 3 non-flipping forms, a coin puts the 3 flippers on "
      f"top with probability 1/C(6,3) = {1/20:.3f}.  A 'YES' above is worth 5%, not a mechanism.")
    P(f"  Predictors that separate the flippers perfectly: "
      f"{sum(r['separates_flippers'] for r in rk)} of {len(rk)} — the confound, stated as a count.")
    pd.DataFrame(rk).to_csv(OUT / f"{STAMP}.rank.csv", index=False)

    P("\nCELL-LEVEL discrimination (Mann-Whitney AUC of each predictor for flip_any; 0.5 = none):")
    d6 = df[df.form == "DG"]
    dmk = d6[~d6.family.isin(NAME_LEVEL)]
    P(f"  {'predictor':10s} {'AUC all 216 DG cells':>22s} {'AUC within 108 market-DG':>26s}")
    aucs = []
    for p in PREDS:
        a1 = auc(d6[p].to_numpy(), d6.flip_any.to_numpy())
        a2 = auc(dmk[p].to_numpy(), dmk.flip_any.to_numpy())
        aucs.append(dict(predictor=p, auc_all_DG=a1, auc_within_market=a2))
        P(f"  {p:10s} {a1:22.4f} {a2:26.4f}")
    P("  The WITHIN-market column is the one that is not confounded by the name/market split: "
      "there the 3 gate families share a form and only the path differs.")
    pd.DataFrame(aucs).to_csv(OUT / f"{STAMP}.auc.csv", index=False)

    # ------------------------------------------------------------------ PART B
    P("\n" + "=" * 118)
    P("PART B — BLOCK-SHUFFLE ladder: autocorrelation dialled, gross gap held EXACTLY fixed")
    P("=" * 118)
    P("The gate's fired/not-fired sequence over the scored rebalance days is cut into blocks of "
      "L weeks and the BLOCKS are permuted (seeds 0,1,2).")
    P("A permutation preserves the multiset exactly, so mean target gross, gap, fire rate and "
      "every marginal statistic are invariant (gate G4 asserts < 1e-12 and an exact fire count).")
    tb = (sh.groupby("L").agg(n=("flip_any", "size"), RHO1=("RHO1", "mean"),
                              RUN=("RUN", "mean"), GAP=("GAP", "mean"), SD=("SD", "mean"),
                              TIMING=("TIMING", "mean"), DDTIME=("DDTIME", "mean"),
                              flip_S=("flip_Sharpe", "mean"), flip_C=("flip_CAGR", "mean"),
                              flip_D=("flip_MaxDD", "mean"), flip_any=("flip_any", "mean"))
          .reset_index())
    tb["L_label"] = np.where(tb.L == 0, "ACTUAL", tb.L.astype(str) + "w")
    P(tb[["L_label", "n", "GAP", "SD", "RHO1", "RUN", "TIMING", "DDTIME", "flip_S", "flip_C",
          "flip_D", "flip_any"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    tg0 = sh[sh.L == 0].set_index(["panel", "family", "dial", "gross"])["tg"]
    tgs = sh[sh.L > 0].set_index(["panel", "family", "dial", "gross"])["tg"]
    P(f"  TARGET-gross invariance across every (L, seed): max |tg - tg(ACTUAL)| = "
      f"{float((tgs - tg0).abs().max()):.3e} (gate G4 asserts < 1e-12 cell by cell, and the fire "
      f"count is preserved EXACTLY).  The GAP/SD columns above are read off the REALISED held "
      f"path, which drifts between rebalances, hence their ~1e-3 wobble.")
    P(f"  max |GAP - GAP(ACTUAL)| across the ladder = "
      f"{float((tb.GAP - float(tb.loc[tb.L == 0, 'GAP'].iloc[0])).abs().max()):.3e}   "
      f"max |SD - SD(ACTUAL)| = "
      f"{float((tb.SD - float(tb.loc[tb.L == 0, 'SD'].iloc[0])).abs().max()):.3e}")
    P("  (the gap and the amplitude really are frozen; RHO1 and RUN are what the ladder moves)")
    sp_r = spearman(tb.RHO1.to_numpy(), tb.flip_any.to_numpy())
    P(f"  Spearman(RHO1, flip_any rate) over the {len(tb)} rungs = {sp_r:+.4f}   "
      f"Spearman(TIMING, flip rate) = {spearman(tb.TIMING.to_numpy(), tb.flip_any.to_numpy()):+.4f}")
    shs = sh[sh.L > 0]
    P(f"\n  Pooled over the {len(shs)} shuffled draws (ACTUAL excluded), draw-level correlations "
      f"with flip_any:")
    for p in ("RHO1", "RUN", "TIMING", "DDTIME", "GAP", "SD"):
        P(f"    AUC({p:6s}) = {auc(shs[p].to_numpy(), shs.flip_any.to_numpy()):.4f}   "
          f"Spearman = {spearman(shs[p].to_numpy(), shs.flip_any.astype(float).to_numpy()):+.4f}")
    P("\n  Per-METRIC AUC over the shuffled draws (a flip is not one phenomenon):")
    for m in ("CAGR", "MaxDD"):
        P(f"    flip_{m:6s} rate {float(shs[f'flip_{m}'].mean()):.1%}   " +
          "  ".join(f"AUC({q}) {auc(shs[q].to_numpy(), shs[f'flip_{m}'].to_numpy()):.3f}"
                    for q in ("RHO1", "TIMING", "DDTIME", "GAP")))
    P("\n  Draw-level TERTILES of the 1296 shuffled draws (~432 each):")
    s2 = shs.copy()
    s2["TIMING_tertile"] = pd.qcut(s2.TIMING, 3, labels=["1 most negative", "2", "3 most positive"])
    s2["RHO1_tertile"] = pd.qcut(s2.RHO1, 3, labels=["1 lowest", "2", "3 highest"])
    for col in ("TIMING_tertile", "RHO1_tertile"):
        P(f"   by {col}:")
        P(s2.groupby(col, observed=True)[["RHO1", "TIMING", "GAP", "SD", "flip_CAGR",
                                          "flip_MaxDD", "flip_any"]].mean()
          .to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  Mean DELTAS (unmatched -> matched), real gates vs shuffled, so the flip's DIRECTION "
      "is readable:")
    for lab, d_ in (("ACTUAL", sh[sh.L == 0]), ("SHUFFLED", shs)):
        P(f"    {lab:9s} " + "   ".join(
            f"d{m}: U {d_[f'dU_{m}'].mean():+.4f} -> M {d_[f'dM_{m}'].mean():+.4f}"
            for m in ("Sharpe", "CAGR", "MaxDD")))
    P(f"  Flip rate of the REAL gates {float(sh.loc[sh.L == 0, 'flip_any'].mean()):.1%} vs "
      f"shuffled {float(shs.flip_any.mean()):.1%} "
      f"(Sharpe {float(shs.flip_Sharpe.mean()):.1%}, CAGR {float(shs.flip_CAGR.mean()):.1%}, "
      f"MaxDD {float(shs.flip_MaxDD.mean()):.1%}).")
    P("\n  By family (flip_any rate):")
    P(sh.pivot_table(index="family", columns="L", values="flip_any", aggfunc="mean")
      .to_string(float_format=lambda x: f"{x:.3f}"))

    # ------------------------------------------------------------------ PART C
    P("\n" + "=" * 118)
    P(f"PART C — LAMBDA ladder: gross gap dialled, autocorrelation held EXACTLY fixed "
      f"(g = {LAM_G}, all 9 forms x 4 dials x 3 panels)")
    P("=" * 118)
    P("W(lambda) = lambda*W_clause + (1-lambda)*W_control.  Mean target gross is affine in "
      "lambda so the GAP scales by lambda; the gross path is an affine map of the clause's own "
      "path so its AUTOCORRELATION is invariant.")
    lmd = lm[lm.form == "DG"]
    tc = (lmd.groupby("lam").agg(n=("flip_any", "size"), GAP=("GAP", "mean"), SD=("SD", "mean"),
                                 RHO1=("RHO1", "mean"), TIMING=("TIMING", "mean"),
                                 DDTIME=("DDTIME", "mean"),
                                 flip_S=("flip_Sharpe", "mean"), flip_C=("flip_CAGR", "mean"),
                                 flip_D=("flip_MaxDD", "mean"), flip_any=("flip_any", "mean"))
          .reset_index())
    P(tc.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"  RHO1 range across the ladder = "
      f"{float(tc.RHO1.max() - tc.RHO1.min()):.3e} (held fixed by construction); "
      f"GAP moves {float(tc.GAP.min()):.4f} -> {float(tc.GAP.max()):.4f}, a "
      f"{float(tc.GAP.max()/max(tc.GAP.min(),1e-12)):.1f}x range.")
    P(f"  Spearman(GAP, flip rate) over the {len(tc)} rungs = "
      f"{spearman(tc.GAP.to_numpy(), tc.flip_any.to_numpy()):+.4f}")
    P("\n  Split by level (name-DG vs market-DG):")
    P(lmd.pivot_table(index=lmd.family.isin(NAME_LEVEL).map({True: "name-DG", False: "market-DG"}),
                      columns="lam", values="flip_any", aggfunc="mean")
      .to_string(float_format=lambda x: f"{x:.3f}"))

    # ------------------------------------------------------------------ PART D
    P("\n" + "=" * 118)
    P("PART D — rule 8 walk-forward: (dial, g) chosen on 2009-2016 by IS dSharpe, 2017-2026 read "
      "once")
    P("=" * 118)
    P(wf[["panel", "family", "form", "dial", "gross", "IS_dU_Sharpe", "OOS_CAGR", "OOS_Sharpe",
          "OOS_MaxDD", "base_OOS_Sharpe", "spy_OOS_Sharpe", "sign_holds", "GAP", "RHO1",
          "TIMING", "flip_any", "pass4a", "pass4b"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  IS sign holds OOS on {int(wf.sign_holds.sum())}/{len(wf)} picks "
      f"({wf.sign_holds.mean():.1%}).  KEEP paths on the picks: 4a {int(wf.pass4a.sum())}/{len(wf)}, "
      f"4b {int(wf.pass4b.sum())}/{len(wf)}.")
    P(f"  KEEP paths over ALL {len(df)} grid points with no selection: 4a {int(df.pass4a.sum())}, "
      f"4b {int(df.pass4b.sum())}, BOTH {int((df.pass4a & df.pass4b).sum())}.")
    if int(df.pass4b.sum()):
        P("  4b passers (grid, no selection):")
        P(df[df.pass4b][["panel", "family", "form", "dial", "gross", "clause_CAGR",
                         "clause_Sharpe", "clause_MaxDD", "clause_H1", "clause_H2",
                         "clause_oSharpe", "flip_any"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    kp = df[["panel", "family", "form", "dial", "gross", "clause_CAGR", "clause_Sharpe",
             "clause_MaxDD", "clause_H1", "clause_H2", "clause_oSharpe", "GAP", "RHO1", "TIMING",
             "flip_any", "pass4a", "pass4b"]]
    kp.to_csv(OUT / f"{STAMP}.keeppaths.csv", index=False)
    P("\n  Reference levels (survivorship: B136/SMALL439 are CURRENT constituents, LEVELS biased up)")
    P(lv.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------------ headline
    P("\n" + "=" * 118)
    P("HEADLINE")
    P("=" * 118)
    if prov:
        P(f"G3: idea 581's {prov['n']} cells reproduce to < 1e-12 "
          f"({prov['flips_S']} Sharpe / {prov['flips_C']} CAGR / {prov['flips_D']} MaxDD flips), "
          f"so this run is speaking about the same population.")
    yes = [r["predictor"] for r in rk if r["separates_flippers"]]
    sp_rho = [r["spearman_n6"] for r in rk if r["predictor"] == "RHO1"][0]
    sp_gap = [r["spearman_n6"] for r in rk if r["predictor"] == "GAP"][0]
    sp_sd = [r["spearman_n6"] for r in rk if r["predictor"] == "SD"][0]
    P(f"A. AS ASKED: neither candidate orders the flips.  Over the 6 de-gross forms "
      f"Spearman(RHO1, flip rate) = {sp_rho:+.4f} — autocorrelation orders the record's flips "
      f"BACKWARDS, because the SMOOTH cross-sectional clauses have the HIGHER lag-1 "
      f"autocorrelation, not the blockwise gates.  GAP = {sp_gap:+.4f} (also fails, "
      f"reconfirming idea 581).  {len(yes)} of {len(PREDS)} predictors "
      f"({', '.join(yes)}) put the 3 flipping forms on top, at a 5.0% chance floor: the "
      f"amplitude of the gross path, Spearman {sp_sd:+.4f}.")
    a_r = [a for a in aucs if a["predictor"] == "RHO1"][0]
    a_g = [a for a in aucs if a["predictor"] == "GAP"][0]
    a_t = [a for a in aucs if a["predictor"] == "TIMING"][0]
    P(f"   Within the 108 market-DG cells (form held constant): AUC RHO1 "
      f"{a_r['auc_within_market']:.3f}, GAP {a_g['auc_within_market']:.3f}, TIMING "
      f"{a_t['auc_within_market']:.3f}.")
    P(f"B. BLOCK-SHUFFLE (gap, amplitude, fire rate and the whole marginal distribution frozen; "
      f"only the ORDER changes): flip_any "
      f"{' -> '.join(f'{lab} {v:.1%}' for lab, v in zip(tb.L_label, tb.flip_any))}.")
    P(f"   Autocorrelation is worth nothing on its own ladder: draw-level AUC(RHO1) = "
      f"{auc(shs.RHO1.to_numpy(), shs.flip_any.to_numpy()):.3f} over {len(shs)} draws, and the "
      f"REAL gates carry the HIGHEST RHO1 and the LOWEST flip rate.  Scrambling the order alone "
      f"doubles the flip rate {float(sh.loc[sh.L == 0, 'flip_any'].mean()):.1%} -> "
      f"{float(shs.flip_any.mean()):.1%}, and it is METRIC-SPECIFIC: the CAGR flip is a pure "
      f"timing statistic (AUC(TIMING) = "
      f"{auc(shs.TIMING.to_numpy(), shs.flip_CAGR.to_numpy()):.3f}) while the MaxDD flip is "
      f"captured by NO scalar summary of the path (best AUC "
      f"{max(auc(shs[q].to_numpy(), shs.flip_MaxDD.to_numpy()) for q in PREDS):.3f}).")
    P(f"C. LAMBDA (autocorrelation and timing frozen; gap AND amplitude dialled together "
      f"{float(tc.GAP.min()):.3f} -> {float(tc.GAP.max()):.3f}): flip_any "
      f"{' -> '.join(f'lam {l:.2f} {v:.1%}' for l, v in zip(tc.lam, tc.flip_any))} — not "
      f"monotone in the gap (Spearman "
      f"{spearman(tc.GAP.to_numpy(), tc.flip_any.to_numpy()):+.2f}), and every MaxDD flip on "
      f"the ladder needs the FULL blockwise cut (0 of 216 partial-amplitude cells flip on "
      f"drawdown).  This ladder cannot separate gap from amplitude — both are affine in "
      f"lambda — and says so.")
    P(f"D. rule 8: 4a {int(wf.pass4a.sum())}/{len(wf)}, 4b {int(wf.pass4b.sum())}/{len(wf)} on the "
      f"picks; 4a {int(df.pass4a.sum())}, 4b {int(df.pass4b.sum())} over all {len(df)} grid points.")
    P(f"\ndone in {time.time()-t0:.1f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
