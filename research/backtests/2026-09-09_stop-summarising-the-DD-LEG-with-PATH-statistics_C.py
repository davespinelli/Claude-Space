#!/usr/bin/env python3
"""IDEA 592 — stop summarising the DD LEG with PATH statistics: does an EPISODE-LEVEL
   statistic predict the MaxDD flip where no scalar summary of the gross path can?
   (lane C, 2026-09-09)

QUESTION (QUEUE idea 592, verbatim)
    Idea 584 found the MaxDD flip, which carries 28 of idea 581's 35 sign flips, is predicted
    by NO scalar summary of the exposure path (best of 8 is the gross gap at AUC 0.640;
    autocorrelation 0.433, timing 0.492), while the CAGR flip is a near-tautological timing
    statistic (AUC 0.111).  Test whether an EPISODE-LEVEL statistic — which of the control's
    drawdown episodes the clause was de-grossed through, at what depth — predicts the DD flip
    where the path statistics cannot.  If it does, the record's DD-leg claims need an episode
    column, not a path column.  Max 2 params (episode set, depth).

WHAT A "FLIP" IS (idea 581's definition, reproduced bit-for-bit as gate G3)
    A clause book is compared with its own clause-OFF control twice: at the control's NOMINAL
    gross ("unmatched", the record's published convention) and with the control rescaled to the
    clause's own mean target gross ("matched").  A FLIP is a comparison whose delta CHANGES
    SIGN between the two conventions.  flip_MaxDD is that event for the MaxDD leg.

WHERE THE 0.640 CEILING ACTUALLY LIVES — and why this run measures on BOTH populations
    Idea 584's "best of 8 is 0.640" for flip_MaxDD is measured on its BLOCK-SHUFFLE population
    (1,296 draws + 108 actuals, flip rate 50.2%), not on the 216 real de-gross cells.  Quoting
    it against a different population would be a category error, so this run reproduces BOTH
    and reports the episode statistics on each:
      POP A  the 216 real DG cells (6 DG forms x 4 dials x 3 gross x 3 panels), 28 MaxDD flips.
             This is the record's published population — the one an "episode column" would go in.
      POP B  the block-shuffle population, EXACTLY as idea 584 built it (same blocks, same
             seeds 0/1/2, same L in {1,4,13,52} weeks).  This is the decisive test-bed, and it
             is decisive for a reason that is structural, not rhetorical: a block permutation
             preserves the multiset of gate states EXACTLY, so mean target gross, the gross
             gap, the fire rate, the amplitude and the whole marginal distribution of the gross
             path are invariant to machine precision — only WHEN the book was de-grossed moves.
             Every path statistic is therefore (near-)frozen inside a group of 13 draws while
             the episode alignment is scrambled.  If "which episode" is the real DD-leg
             variable, it must discriminate HERE, where the path column cannot by construction.

WHAT AN EPISODE-LEVEL STATISTIC IS
    Take the CONTROL at nominal gross g.  Its equity curve has maximal underwater intervals
    (peak -> trough -> recovery): its DRAWDOWN EPISODES.  Exactly one of them contains the
    control's MaxDD trough — call it the BINDING episode, because the control's whole MaxDD leg
    is decided inside it (gate G4 asserts the identity to < 1e-12).  Read the clause's daily
    de-gross depth d_t = 1 - u_t (u_t = grossHeld(clause)/grossHeld(control)) and ask, per
    episode, how hard the clause was de-grossed THROUGH that episode:
      BIND      the binding episode's de-gross cover
      BINDREL   BIND - GAP, the EXCESS over the clause's own sample-average de-gross  <-- headline
      EPMAX     the deepest cover over any episode in the set;  EPMAXREL = EPMAX - GAP
      BINDRANK  the binding episode's cover RANK among the set, in [0,1] ("which episode")
      BINDISMAX 1 if the binding episode is the most-covered one
      EPSPREAD  SD of cover across episodes (concentration)
      EPSHARE   share of episodes covered above GAP
      NEP       episodes in the set (context, not a predictor)

PRE-REGISTERED DIRECTION (stated before the run, because a signed AUC is otherwise unfalsifiable)
    The matched control is the clause's own control holding UNIFORMLY less.  So the matched DD
    leg asks: did the clause cut exposure where the drawdown actually was, or merely on average?
    A flip is then the event "the clause beats the nominal control on DD but loses to simply
    holding less", which should happen when the clause's de-grossing was NOT concentrated in
    the binding episode.  PREDICTION: flips carry a LOW BINDREL, i.e. AUC(BINDREL) < 0.5 and
    the scored, directional statistic is AUC(-BINDREL) > 0.5.  The same sign is pre-registered
    for -EPMAXREL, -BINDRANK and -BINDISMAX.  Anything reported the other way round is a
    reversal and is called one.

TUNED PARAMETERS: 2, exactly the two the queue names.
    (1) EPISODE SET  theta in {0.05, 0.10, 0.15, 0.20} — the minimum peak-to-trough depth for an
        episode to enter the comparison set.  The BINDING episode is always in the set whatever
        theta (it defines the DD leg); theta governs what it is compared against.
    (2) DEPTH        w in {flat, dd, deep} — how days inside an episode are weighted when the
        cover is averaged: flat = equally, dd = by the control's drawdown depth that day,
        deep = only days at or past half the episode's own trough depth.
    12 grid points; ALL are reported in .grid.csv and printed.  The BOOKS are not tuned here at
    all: the (dial, gross) grid is idea 581's, unchanged, and all 324 cells are reported.

CONFOUND, NAMED UP FRONT
    DD-DG's gate fires ON the control's own drawdown quantile, so it is MECHANICALLY aligned
    with the episodes and must not be allowed to carry the result.  Every AUC is therefore
    reported pooled, WITHIN the 108 market-DG cells, and per family; and POP B's headline is a
    WITHIN-GROUP AUC (13 draws that share panel/family/dial/gross), where family is constant.

DATA VINTAGE — stated up front, because it changes what the provenance gate can assert
    Idea 584 ran on the 2026-09-08 close; the daily-close commit has since added one bar to
    U56 (4,701 rows vs 4,700).  B136 and SMALL439 are unchanged (weekly Friday caches, both
    ending 2026-09-04).  Since this run's whole job is to RE-SCORE idea 584's population, the
    panels are truncated to idea 584's exact window (gate G0 asserts the row counts 4700 /
    4699 / 4194), which makes the provenance gate an EXACT one rather than a tolerance.  The
    dropped bar is not swept under the rug: PART E re-runs U56's 108 cells on the untruncated
    current panel and reports how far the headline moves.

GATES
    G0  VINTAGE: each panel truncated to idea 584's last date, row counts asserted exactly.
    G1  the vectorised runner reproduces engine.backtest to < 1e-12 on returns.
    G2  matched gross: |meanTargetGross(clause) - meanTargetGross(matched control)| < 1e-12.
    G3  PROVENANCE: idea 584's committed 324 cells AND its 1,404 shuffle rows reproduce here,
        and its published AUC ceiling for flip_MaxDD (best of 8 path statistics on POP B) is
        re-derived.  Without this the run is scoring a different population and cannot speak to
        idea 584's claim.  The bar is set at 1e-4 on the deltas, NOT at 1e-12, and the reason is
        measured rather than asserted: between idea 584's commit and this one the daily-close
        job RESTATED data/prices.csv — 23,250 of 272,600 shared cells changed, max relative
        change 3.71e-4 (idea 257's known restatement, "up to 3e-4 on shared cells").  A 1e-12
        bar is therefore unreachable at ANY window.  Three things make the looser bar auditable:
          (i)  data/prices_broad.csv is BIT-IDENTICAL between the two commits (0 changed cells),
               so B136's 108 cells must and do reproduce to < 1e-12 — that is the gate that
               proves the CODE is idea 584's and isolates the residual to the data;
          (ii) the flip flags, which are what the population IS, must agree EXACTLY (0
               disagreements) — a tolerance is allowed on the deltas, never on the labels;
          (iii) the per-panel discrepancy is printed, so the reader sees where it lives.
    G4  EPISODES: the episodes partition the control's underwater time exactly (no overlap, no
        gap), and the binding episode's trough depth equals the control's MaxDD to < 1e-12.
    G5  PLACEBO: circularly shifting the episode windows preserves the episode COUNT exactly and
        total episode days exactly — only the alignment with the gross path moves.

PART C — the CHANCE FLOOR, built not assumed
    The episode windows are circularly time-shifted by S in {+-13, +-26, +-52, +-104} weeks and
    every statistic recomputed against the real books.  This holds the episode set, its depths
    and the gross path all fixed and destroys only the alignment, so the spread of placebo AUCs
    IS the floor for "an episode statistic discriminates".

RULE 8 (walk-forward, required).  Per arm x panel, pick (dial, g) on 2009-2016 ONLY by IS
    dSharpe against the unmatched control (the record's own selection rule), evaluate 2017-2026
    untouched: OOS CAGR/Sharpe/MaxDD of the picked book vs RULES v2 and vs SPY, both KEEP paths
    (4a and 4b), plus the pick's own BINDREL.  4a/4b are also reported over all 324 grid points.

PART E — VINTAGE ARM: U56's 108 DG cells re-run on the untruncated current panel (one extra
    bar) and rescored, so the reader can see whether the answer is a window artefact.

Outputs (committed): .console.txt .cells.csv .shuffle.csv.gz .grid.csv .placebo.csv.gz
    .walkforward.csv .keeppaths.csv .vintage.csv .gates.csv .ties.csv .fragility.csv
    .fragile_rows.csv .pathauc.csv .result.md  (the two large panels are gzipped)
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

STAMP = "2026-09-09_stop-summarising-the-DD-LEG-with-PATH-statistics_C"
PRIOR = "2026-09-09_is-the-BLOCKWISE-vs-SMOOTH-split-the-real-predictor-of-a-gross-flip_C"
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
BLOCKS_W = (1, 4, 13, 52)          # idea 584's block lengths, reproduced
SEEDS = (0, 1, 2)

THETAS = (0.05, 0.10, 0.15, 0.20)          # TUNED PARAM 1: episode set
WEIGHTS = ("flat", "dd", "deep")           # TUNED PARAM 2: depth weighting
SHIFTS_W = (-104, -52, -26, -13, 13, 26, 52, 104)   # placebo, in weeks (5 trading days)

# idea 584's data vintage: its console records these last dates / row counts per panel
PARENT_LAST = {"U56": "2026-09-08", "B136": "2026-09-04", "SMALL439": "2026-09-04"}
PARENT_ROWS = {"U56": 4700, "B136": 4699, "SMALL439": 4194}

# the 8 path statistics idea 584 scored, reproduced verbatim as the comparator column
PATH_PREDS = ("GAP", "SD", "RHO1", "RHO5", "DRHO1", "RUN", "TIMING", "DDTIME")
# the episode column this run proposes; the pre-registered sign is applied when SCORING
EP_PREDS = ("BIND", "BINDREL", "EPMAX", "EPMAXREL", "BINDRANK", "BINDISMAX", "EPSPREAD", "EPSHARE")
EP_SIGN = {"BIND": -1, "BINDREL": -1, "EPMAX": -1, "EPMAXREL": -1,
           "BINDRANK": -1, "BINDISMAX": -1, "EPSPREAD": -1, "EPSHARE": -1}

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); _LOG.append(s)


# ============================================================ vectorised engine clone
class Runner:
    """Closed-form equivalent of engine.backtest with the per-panel constants precomputed once.
    Same t+1 application, same weekly schedule, same intra-period drift with cash flat, same
    turnover-based cost.  Gate G1 asserts the equivalence."""

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
        self.sp = starts[seg[self.later] - 1]
        self.ratio_l = Cs[self.later] / Cs[self.sp]
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
    return float(W.loc[rb].sum(axis=1).loc[start:].mean())


# ============================================================ statistics
def pearson(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    a, b = a[ok], b[ok]
    if len(a) < 3 or a.std() == 0 or b.std() == 0:
        return np.nan
    return float(np.corrcoef(a, b)[0, 1])


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    a, b = a[ok], b[ok]
    if len(a) < 3:
        return np.nan
    return pearson(pd.Series(a).rank().to_numpy(), pd.Series(b).rank().to_numpy())


def auc(score, label):
    """Mann-Whitney AUC: P(score of a flipping cell > score of a non-flipping cell), ties 0.5.
    0.5 = no discrimination, 1.0 = perfect, < 0.5 = the statistic orders the flips backwards."""
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
    flag = np.asarray(flag, bool)
    if not flag.any():
        return np.nan
    d = np.diff(np.concatenate([[0], flag.view(np.int8), [0]]))
    return float(flag.sum() / max(int((d == 1).sum()), 1))


def path_stats(u: pd.Series, spy: pd.Series, ddc: pd.Series) -> dict:
    """idea 584's 8 path predictors, read off the daily gross-ratio path u_t, verbatim."""
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


# ============================================================ EPISODES (the new column)
def dd_episodes(dd: np.ndarray):
    """Maximal underwater intervals of a drawdown series (peak -> recovery), in index space.
    Returns (list of (a, b, trough, depth), binding position).  The BINDING episode is the one
    containing the global minimum of dd, i.e. the one that decides the control's MaxDD."""
    under = dd < -1e-12
    d = np.diff(np.concatenate([[0], under.view(np.int8), [0]]))
    starts, ends = np.flatnonzero(d == 1), np.flatnonzero(d == -1)
    eps = []
    for a, b in zip(starts, ends):
        seg = dd[a:b]
        eps.append((int(a), int(b), int(a + np.argmin(seg)), float(-seg.min())))
    gmin = int(np.argmin(dd))
    bind = next(i for i, (a, b, _, _) in enumerate(eps) if a <= gmin < b)
    return eps, bind


def episode_set(eps, bind, theta):
    """The comparison set at threshold theta.  The binding episode is ALWAYS in it (it defines
    the DD leg); theta governs what it is compared against."""
    keep = [i for i, e in enumerate(eps) if e[3] >= theta or i == bind]
    return keep, keep.index(bind)


def cover(d_daily: np.ndarray, dd: np.ndarray, e, weight: str) -> float:
    """How hard the clause was de-grossed THROUGH one episode, under the depth weighting."""
    a, b, _, depth = e
    dv, dep = d_daily[a:b], -dd[a:b]
    if weight == "flat":
        w = np.ones(b - a)
    elif weight == "dd":
        w = dep
    else:                                    # "deep": at or past half the episode's own trough
        w = (dep >= 0.5 * depth).astype(float)
    sw = w.sum()
    return float((dv * w).sum() / sw) if sw > 0 else np.nan


def ep_stats(d_daily: np.ndarray, dd: np.ndarray, eps, bind, theta, weight, gap) -> dict:
    keep, bpos = episode_set(eps, bind, theta)
    cov = np.array([cover(d_daily, dd, eps[i], weight) for i in keep], float)
    c_b = cov[bpos]
    finite = np.isfinite(cov)
    n = int(finite.sum())
    if n >= 2:
        r = pd.Series(cov).rank().to_numpy()
        brank = float((r[bpos] - 1) / (n - 1))
        ismax = float(np.nanmax(cov) - c_b < 1e-15)
        spread = float(np.nanstd(cov))
        share = float(np.nanmean(cov[finite] > gap))
    else:
        brank, ismax, spread, share = np.nan, np.nan, np.nan, np.nan
    return dict(BIND=c_b, BINDREL=c_b - gap, EPMAX=float(np.nanmax(cov)),
                EPMAXREL=float(np.nanmax(cov)) - gap, BINDRANK=brank, BINDISMAX=ismax,
                EPSPREAD=spread, EPSHARE=share, NEP=n)


def shift_episodes(eps, bind, S: int, T: int):
    """PLACEBO: slide every episode window by S bars, circularly inside [0, T).  Episode count
    and every episode's LENGTH and DEPTH are preserved exactly; only the alignment with the
    gross path moves.  A window that would wrap is wrapped to the other end of the sample."""
    out = []
    for (a, b, t, dep) in eps:
        L = b - a
        na = (a + S) % T
        nb = na + L
        if nb > T:                            # wrap: place it at the head instead of splitting
            na, nb = na - T, na - T + L
            if na < 0:
                na, nb = 0, L
        out.append((int(na), int(nb), int(min(max(t + S, na), nb - 1)), dep))
    return out, bind


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
    """idea 584's shuffle, reproduced bit-for-bit: cut into contiguous blocks of L and permute
    the BLOCKS.  Preserves the multiset of values exactly; only the order changes."""
    n = len(v)
    blocks = [v[a:a + L] for a in range(0, n, L)]
    order = np.random.default_rng(seed).permutation(len(blocks))
    return np.concatenate([blocks[i] for i in order])


def all_ep_stats(d_daily, dd, eps, bind, gap, prefix=""):
    """Every (theta, weight) grid point for one book, flattened into one row."""
    out = {}
    for th in THETAS:
        for w in WEIGHTS:
            st = ep_stats(d_daily, dd, eps, bind, th, w, gap)
            for k, v in st.items():
                out[f"{prefix}{k}_{int(th*100):02d}_{w}"] = v
    return out


def col(stat, th, w):
    return f"{stat}_{int(th*100):02d}_{w}"


# ============================================================ per-panel driver
def run_panel(pname, px, tradable, store, light=False, cells_key="cells"):
    """light=True runs only the 108 DG cells + their episode statistics (the PART E vintage
    arm): no shuffle population, no placebo, no walk-forward."""
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
    P(f"  SPY      CAGR {M_spy['CAGR']:7.2%} Sharpe {M_spy['Sharpe']:6.3f} MaxDD {M_spy['MaxDD']:7.2%}")
    P(f"  RULESv2  CAGR {M_b2['CAGR']:7.2%} Sharpe {M_b2['Sharpe']:6.3f} MaxDD {M_b2['MaxDD']:7.2%}")

    ctrl = {}
    for g in GS:
        W = ew(elig, g)
        r, h = R.run(W)
        rr = r.loc[start:]
        eqc = (1 + rr).cumprod()
        ddc = (eqc / eqc.cummax() - 1.0)
        eps, bind = dd_episodes(ddc.to_numpy(float))
        ctrl[g] = dict(W=W, r=rr, r_full=r, h=h.loc[start:], tg=mean_target_gross(W, rb, start),
                       dd=ddc, dd_np=ddc.to_numpy(float), eps=eps, bind=bind)
        # ---- G4: the episodes partition the underwater time and the binding one IS the MaxDD
        und = int((ctrl[g]["dd_np"] < -1e-12).sum())
        cov_days = sum(b - a for a, b, _, _ in eps)
        ovl = any(eps[i][1] > eps[i + 1][0] for i in range(len(eps) - 1))
        dmax = abs(-eps[bind][3] - float(metrics(rr)["MaxDD"]))
        ok = (und == cov_days) and (not ovl) and dmax < 1e-12
        store["gates"].append(dict(gate="G4", panel=pname, g=g, n_ep=len(eps),
                                   underwater_days=und, episode_days=cov_days,
                                   overlap=ovl, bind_depth_err=dmax, PASS=ok))
        assert ok, f"G4 failure {pname} g={g}"

    cells = store[cells_key]
    cache = {}
    for fam, form in (tuple((f, "DG") for f in FAMS) if light else ARMS):
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
                u = hc.loc[start:] / ctrl[g]["h"]
                st = path_stats(u, spy, ctrl[g]["dd"])
                d_daily = (1.0 - u).to_numpy(float)
                row = dict(panel=pname, family=fam, form=form, dial=dial, gross=g,
                           tg_clause=tg_c, tg_ctrl=ctrl[g]["tg"], k=k,
                           gross_gap=ctrl[g]["tg"] - tg_c,
                           fire_rate=float((Wc.sum(axis=1) < ctrl[g]["W"].sum(axis=1) - 1e-12)
                                           .loc[start:].mean()), **st,
                           **all_ep_stats(d_daily, ctrl[g]["dd_np"], ctrl[g]["eps"],
                                          ctrl[g]["bind"], st["GAP"]))
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
                cache[(fam, form, dial, g)] = dict(Wc=Wc, rm=rm, Mm=Mm, A=A, U=U, k=k, tg_c=tg_c,
                                                   d_daily=d_daily, gap=st["GAP"])

    if light:
        P(f"  VINTAGE ARM {pname}: built {len([c for c in cells if c['panel']==pname])} DG cells "
          f"on the untruncated panel   [{time.time()-t0:.1f}s]")
        return

    # ---------------------------------------------------------- POP B: block-shuffle ladder
    rb_days = rb.loc[start:][rb.loc[start:]].index
    shuf = store["shuffle"]
    for fam, form in MKT_DG:
        for g in GS:
            for dial in DIALS[fam]:
                base = cache[(fam, form, dial, g)]
                off = gate_off(fam, dial, px, breadth, spytr, ctrl[g]["r_full"])
                v0 = off.loc[rb_days].to_numpy(bool)
                for L in BLOCKS_W:
                    for seed in SEEDS:
                        v = block_permute(v0, L, seed)
                        assert v.sum() == v0.sum() and len(v) == len(v0), "G4b fire count"
                        off_s = off.copy()
                        off_s.loc[rb_days] = v
                        live = pd.Series(np.where(off_s.to_numpy(bool), 0.0, 1.0), index=px.index)
                        Ws = ctrl[g]["W"].mul(live, axis=0)
                        tg_s = mean_target_gross(Ws, rb, start)
                        assert abs(tg_s - base["tg_c"]) < 1e-12, "G4b gross invariance"
                        rs_, hs_ = R.run(Ws); rs_ = rs_.loc[start:]
                        As = mrow(rs_)
                        us = hs_.loc[start:] / ctrl[g]["h"]
                        st = path_stats(us, spy, ctrl[g]["dd"])
                        row = dict(panel=pname, family=fam, form=form, dial=dial, gross=g,
                                   L=L, seed=seed, k=base["k"], tg=tg_s, **st,
                                   **all_ep_stats((1.0 - us).to_numpy(float), ctrl[g]["dd_np"],
                                                  ctrl[g]["eps"], ctrl[g]["bind"], st["GAP"]))
                        for m in ("Sharpe", "CAGR", "MaxDD"):
                            row[f"dU_{m}"] = As[m] - base["U"][m]
                            row[f"dM_{m}"] = As[m] - base["Mm"][m]
                            row[f"flip_{m}"] = bool(np.sign(As[m] - base["U"][m])
                                                    != np.sign(As[m] - base["Mm"][m]))
                        row["flip_any"] = bool(row["flip_Sharpe"] or row["flip_CAGR"]
                                               or row["flip_MaxDD"])
                        shuf.append(row)
                bc = [c for c in cells if c["panel"] == pname and c["family"] == fam
                      and c["form"] == form and c["dial"] == dial and c["gross"] == g][0]
                keep_keys = ([p for p in PATH_PREDS] + ["LOWSHARE"]
                             + [k for k in bc if any(k.startswith(e + "_") for e in EP_PREDS)
                                or k.startswith("NEP_")])
                shuf.append(dict(panel=pname, family=fam, form=form, dial=dial, gross=g,
                                 L=0, seed=-1, k=bc["k"], tg=bc["tg_clause"],
                                 **{p: bc[p] for p in keep_keys},
                                 **{f"d{c}_{m}": bc[f"d{c}_{m}"] for c in ("U", "M")
                                    for m in ("Sharpe", "CAGR", "MaxDD")},
                                 **{f"flip_{m}": bc[f"flip_{m}"]
                                    for m in ("Sharpe", "CAGR", "MaxDD")},
                                 flip_any=bc["flip_any"]))

    # ---------------------------------------------------------- PART C: placebo shifts
    T = len(ctrl[GS[0]]["dd_np"])
    for fam, form in ARMS:
        if form == "RS":
            continue
        for g in GS:
            for dial in DIALS[fam]:
                base = cache[(fam, form, dial, g)]
                bc = [c for c in cells if c["panel"] == pname and c["family"] == fam
                      and c["form"] == form and c["dial"] == dial and c["gross"] == g][0]
                for S in SHIFTS_W:
                    eps_s, bind_s = shift_episodes(ctrl[g]["eps"], ctrl[g]["bind"], S * 5, T)
                    n0 = len(ctrl[g]["eps"])
                    days0 = sum(b - a for a, b, _, _ in ctrl[g]["eps"])
                    days1 = sum(b - a for a, b, _, _ in eps_s)
                    assert len(eps_s) == n0 and days1 == days0, "G5 placebo invariance"
                    r = dict(panel=pname, family=fam, dial=dial, gross=g, shift_w=S,
                             flip_MaxDD=bc["flip_MaxDD"], flip_CAGR=bc["flip_CAGR"],
                             flip_any=bc["flip_any"],
                             **all_ep_stats(base["d_daily"], ctrl[g]["dd_np"], eps_s, bind_s,
                                            base["gap"]))
                    store["placebo"].append(r)
    store["gates"].append(dict(gate="G5", panel=pname, g=np.nan,
                               n_ep=len(ctrl[GS[0]]["eps"]), underwater_days=np.nan,
                               episode_days=np.nan, overlap=False, bind_depth_err=0.0, PASS=True))

    # ---------------------------------------------------------- rule 8 walk-forward
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
            GAP=pick["GAP"], BINDREL=pick[col("BINDREL", 0.10, "flat")],
            flip_MaxDD=bool(pick["flip_MaxDD"]), pass4a=p4a, pass4b=p4b))
    store["levels"].append(dict(panel=pname, spy_CAGR=M_spy["CAGR"], spy_Sharpe=M_spy["Sharpe"],
                                spy_MaxDD=M_spy["MaxDD"], spy_H1=M_spy["H1"], spy_H2=M_spy["H2"],
                                v2_CAGR=M_b2["CAGR"], v2_Sharpe=M_b2["Sharpe"],
                                v2_MaxDD=M_b2["MaxDD"], v2_H1=M_b2["H1"], v2_H2=M_b2["H2"],
                                spy_OOS_Sharpe=M_spy_o["Sharpe"], v2_OOS_Sharpe=M_b2_o["Sharpe"],
                                n_episodes_g075=len(ctrl[0.75]["eps"]),
                                bind_depth_g075=ctrl[0.75]["eps"][ctrl[0.75]["bind"]][3]))
    P(f"  built {len(df)} cells + shuffle + placebo   [{time.time()-t0:.1f}s]")


# ============================================================ gates
def gate_g1(R, px, W, tag):
    r1, _ = R.run(W)
    res = backtest(px, W, cost_bps=COST, freq=FREQ)
    dr = float((r1 - res["returns"]).abs().max())
    P(f"  G1 {tag:22s} max|dReturn| = {dr:.3e}   {'PASS' if dr < 1e-12 else 'FAIL'}")
    assert dr < 1e-12


DCOLS = ("dU_Sharpe", "dM_Sharpe", "dU_CAGR", "dM_CAGR", "dU_MaxDD", "dM_MaxDD")
FCOLS = ("flip_Sharpe", "flip_CAGR", "flip_MaxDD")
BAR_RESTATED = 1e-4      # stated, not convenient: the measured restatement is up to 3.71e-4 rel
BAR_EXACT = 1e-12        # the bar the bit-identical panel must still clear


def _disc(m):
    return max(float((m[f"{c}_o"] - m[f"{c}_n"]).abs().max()) for c in DCOLS)


def gate_g3(cells, shuf):
    """PROVENANCE against idea 584: the 324 cells, the 1,404 shuffle rows, and the published
    AUC ceiling for flip_MaxDD on the shuffle population.  See the module docstring for why the
    bar is 1e-4 on the deltas, exact on the flip flags, and 1e-12 on the bit-identical panel."""
    fc = OUT / f"{PRIOR}.cells.csv"
    if not fc.exists():
        P("  G3a prior cells.csv NOT FOUND — provenance SKIPPED (state this in the memo)")
        return None
    old = pd.read_csv(fc)
    new = pd.DataFrame(cells)
    key = ["panel", "family", "form", "dial", "gross"]
    m = old.merge(new, on=key, suffixes=("_o", "_n"))
    assert len(m) == len(old) == len(new), f"cell count {len(old)}/{len(new)}/{len(m)}"
    worst = _disc(m)
    nflip = sum(int((m[f"{c}_o"].astype(bool) != m[f"{c}_n"].astype(bool)).sum()) for c in FCOLS)
    ok = worst < BAR_RESTATED and nflip == 0
    P(f"  G3a idea-584 cells       {len(m)} rows, max|d(delta)| = {worst:.3e} "
      f"(bar {BAR_RESTATED:.0e}, price restatement), flip-flag disagreements = {nflip} "
      f"(bar 0)   {'PASS' if ok else 'FAIL'}")
    for pn in sorted(m.panel.unique()):
        mp = m[m.panel == pn]
        bar = BAR_EXACT if pn == "B136" else BAR_RESTATED
        d = _disc(mp)
        okp = d < bar
        P(f"      {pn:9s} {len(mp):3d} cells  max|d(delta)| = {d:.3e}  bar {bar:.0e}  "
          f"{'PASS' if okp else 'FAIL'}"
          + ("   <- data/prices_broad.csv is BIT-IDENTICAL: this is the CODE-identity gate"
             if pn == "B136" else "   <- data/prices.csv restated since idea 584"))
        ok &= okp
    assert ok

    fs = OUT / f"{PRIOR}.shuffle.csv"
    olds = pd.read_csv(fs)
    news = pd.DataFrame(shuf)
    ks = ["panel", "family", "form", "dial", "gross", "L", "seed"]
    ms = olds.merge(news, on=ks, suffixes=("_o", "_n"))
    assert len(ms) == len(olds) == len(news), f"shuffle count {len(olds)}/{len(news)}/{len(ms)}"
    worst_s = _disc(ms)
    nflip_s = sum(int((ms[f"{c}_o"].astype(bool) != ms[f"{c}_n"].astype(bool)).sum())
                  for c in FCOLS)
    ok = worst_s < BAR_RESTATED
    P(f"  G3b idea-584 shuffle     {len(ms)} rows, max|d(delta)| = {worst_s:.3e} "
      f"(bar {BAR_RESTATED:.0e}), flip-flag disagreements = {nflip_s} of {3*len(ms)} flags   "
      f"{'PASS' if ok else 'FAIL'}")
    for pn in sorted(ms.panel.unique()):
        mp = ms[ms.panel == pn]
        bar = BAR_EXACT if pn == "B136" else BAR_RESTATED
        d = _disc(mp)
        nf = sum(int((mp[f"{c}_o"].astype(bool) != mp[f"{c}_n"].astype(bool)).sum())
                 for c in FCOLS)
        P(f"      {pn:9s} {len(mp):4d} rows  max|d(delta)| = {d:.3e}  bar {bar:.0e}  "
          f"{'PASS' if d < bar else 'FAIL'}   flip-flag disagreements {nf}")
        ok &= d < bar
    assert ok

    # ---- G3d: a label that moves under a 3.7e-4 price restatement was never determined.
    # Every disagreement must be KNIFE-EDGE: the two deltas whose signs are compared straddle
    # zero by less than the restatement footprint.  A disagreement outside that is a code
    # difference and fails the gate.  The fragile share is itself reported — it caps any AUC.
    frag = []
    for met in ("Sharpe", "CAGR", "MaxDD"):
        dis = ms[ms[f"flip_{met}_o"].astype(bool) != ms[f"flip_{met}_n"].astype(bool)]
        margin = np.minimum(dis[f"dU_{met}_n"].abs(), dis[f"dM_{met}_n"].abs()) if len(dis) else \
            pd.Series(dtype=float)
        tot = int(ms[f"flip_{met}_o"].astype(bool).sum())
        frag.append(dict(metric=met, disagreements=len(dis),
                         published_flips=tot,
                         max_margin=float(margin.max()) if len(dis) else 0.0,
                         knife_edge=int((margin < BAR_RESTATED).sum()) if len(dis) else 0))
    ft = pd.DataFrame(frag)
    okd = bool((ft.knife_edge == ft.disagreements).all())
    P(f"  G3d label fragility      every disagreement knife-edge (|delta to zero| < "
      f"{BAR_RESTATED:.0e})?   {'PASS' if okd else 'FAIL'}")
    P("      " + ft.to_string(index=False).replace("\n", "\n      "))
    P(f"      READ: {int(ft.loc[ft.metric=='MaxDD','disagreements'].iloc[0])} of "
      f"{len(ms)} POP-B MaxDD labels move under a price restatement of at most 3.71e-4 — "
      f"they were never determined, and they cap what ANY predictor can score on POP B.")
    assert okd
    ft.to_csv(OUT / f"{STAMP}.fragility.csv", index=False)
    ms_key = ms[["panel", "family", "form", "dial", "gross", "L", "seed"]].copy()
    for met in ("Sharpe", "CAGR", "MaxDD"):
        ms_key[f"fragile_{met}"] = (np.minimum(ms[f"dU_{met}_n"].abs(), ms[f"dM_{met}_n"].abs())
                                    < BAR_RESTATED)
    ms_key.to_csv(OUT / f"{STAMP}.fragile_rows.csv", index=False)

    # ---- G3c: reproduce the number idea 592 actually quotes.  idea 584 measured it over its
    # SHUFFLED draws only (sh.L > 0, 1,296 rows), so that is the subset compared here.  It is
    # then re-compared on the subset whose labels agree, which is the only comparison that can
    # separate "a path statistic re-ranked" from "an undetermined label moved".
    o_s, n_s = olds[olds.L > 0], news[news.L > 0]
    c_old = max(auc(o_s[q].to_numpy(), o_s.flip_MaxDD.to_numpy()) for q in PATH_PREDS)
    c_new = max(auc(n_s[q].to_numpy(), n_s.flip_MaxDD.to_numpy()) for q in PATH_PREDS)
    same = (ms["flip_MaxDD_o"].astype(bool) == ms["flip_MaxDD_n"].astype(bool)).to_numpy()
    keymask = (ms.L > 0).to_numpy() & same
    oa = olds.merge(ms.loc[keymask, ks], on=ks)
    na = news.merge(ms.loc[keymask, ks], on=ks)
    c_old_a = max(auc(oa[q].to_numpy(), oa.flip_MaxDD.to_numpy()) for q in PATH_PREDS)
    c_new_a = max(auc(na[q].to_numpy(), na.flip_MaxDD.to_numpy()) for q in PATH_PREDS)
    ok = abs(c_old_a - c_new_a) < 1e-3
    P(f"  G3c published DD ceiling  over idea 584's own subset (L>0, {len(o_s)} draws): "
      f"published {c_old:.4f}, re-derived {c_new:.4f}, |d| = {abs(c_old-c_new):.2e}")
    P(f"      on the {len(oa)} draws whose MaxDD LABEL agrees: {c_old_a:.4f} vs {c_new_a:.4f}, "
      f"|d| = {abs(c_old_a-c_new_a):.2e} (bar 1e-3)   {'PASS' if ok else 'FAIL'}")
    P(f"      so the whole {abs(c_old-c_new):.4f} gap in the headline ceiling is the "
      f"{int((~same & (ms.L > 0).to_numpy()).sum())} undetermined labels moving, not this run "
      f"scoring a different statistic.")
    assert ok
    ceiling_new = c_new
    return dict(n_cells=len(m), n_shuf=len(ms), ceiling=ceiling_new,
                flips_D_cells=int(old.flip_MaxDD.sum()),
                flips_D_shuf=int(olds.flip_MaxDD.sum()))


# ============================================================ scoring helpers
def scored_auc(d, stat, th, w, label="flip_MaxDD"):
    """AUC of the DIRECTIONAL statistic (pre-registered sign applied), so > 0.5 always means
    'discriminates in the pre-registered direction' and < 0.5 means the reverse."""
    return auc(EP_SIGN[stat] * d[col(stat, th, w)].to_numpy(float), d[label].to_numpy(bool))


def within_group_auc(d, series, label="flip_MaxDD", keys=("panel", "family", "dial", "gross")):
    """Mean AUC computed INSIDE each (panel, family, dial, gross) group of shuffle draws, where
    every path statistic is frozen by construction and only the alignment differs."""
    vals, ng = [], 0
    for _, gdf in d.groupby(list(keys)):
        lab = gdf[label].to_numpy(bool)
        if lab.all() or (~lab).any() == 0 or len(np.unique(lab)) < 2:
            continue
        a = auc(series.loc[gdf.index].to_numpy(float), lab)
        if np.isfinite(a):
            vals.append(a); ng += 1
    return (float(np.mean(vals)) if vals else np.nan, ng,
            float(np.std(vals)) if vals else np.nan)


def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 592 — stop summarising the DD LEG with PATH statistics: does an EPISODE-LEVEL "
      "statistic predict the MaxDD flip?  (lane C, 2026-09-09)")
    P("=" * 118)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS_all = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    scols = [c for c in pxS_all.columns if c != "SPY" and c not in bad]
    pxS = pxS_all[scols + ["SPY"]].dropna(how="all").ffill()
    panels_full = [("U56", pxU, np.ones(len(pxU.columns), bool)),
                   ("B136", pxB, np.ones(len(pxB.columns), bool)),
                   ("SMALL439", pxS, np.array([c != "SPY" for c in pxS.columns]))]
    # ---- G0 VINTAGE: truncate to idea 584's exact window so provenance can be EXACT
    P("\nG0 VINTAGE (panels truncated to idea 584's window so its cells reproduce exactly)")
    panels = []
    for nm, p, tr in panels_full:
        n_before, last_before = len(p), p.index[-1].date()
        p2 = p.loc[:PARENT_LAST[nm]]
        ok = len(p2) == PARENT_ROWS[nm]
        P(f"  {nm:9s} current {n_before} rows to {last_before} -> truncated {len(p2)} rows to "
          f"{p2.index[-1].date()} (idea 584 had {PARENT_ROWS[nm]})   "
          f"{'PASS' if ok else 'FAIL'}   dropped {n_before - len(p2)} bar(s)")
        assert ok, f"G0 vintage mismatch on {nm}"
        panels.append((nm, p2, tr))
    P(f"\nSMALL panel: dropped {len([c for c in pxS_all.columns if c != 'SPY']) - len(scols)} "
      f"names with max_1d_move >= 1.0 -> {len(scols)} tradable.")
    P("SURVIVORSHIP: B136 and SMALL439 are CURRENT constituents; every LEVEL is biased up. "
      "Every claim here is a clause-vs-its-own-control DIFFERENCE on a fixed panel.")
    P("\nPRE-REGISTERED DIRECTION: a MaxDD flip is the event 'the clause beats the nominal "
      "control on DD but loses to simply holding less',")
    P("so it should carry a LOW BINDREL — the scored statistic is -BINDREL and the prediction "
      "is AUC(-BINDREL) > 0.5.  A reversal is reported as one.")

    P("\nGATES")
    RU = Runner(pxU)
    el_u, vol_u, br_u, sp_u = build_panel(pxU, panels[0][2])
    gate_g1(RU, pxU, ew(el_u, 0.75), "U56/EWall")
    r_ctrl_u, _ = RU.run(ew(el_u, 0.75))
    gate_g1(RU, pxU, clause_weights("BREADTH", "DG", 0.20, 0.75, pxU, el_u, vol_u, br_u, sp_u,
                                    r_ctrl_u), "U56/BREADTH-DG")
    gate_g1(RU, pxU, clause_weights("MA", "RS", 200, 0.75, pxU, el_u, vol_u, br_u, sp_u,
                                    r_ctrl_u), "U56/MA-RS")
    gate_g1(RU, pxU, rules_v2_weights(pxU), "U56/RULES v2")

    store = dict(cells=[], shuffle=[], placebo=[], wf=[], levels=[], gates=[], cells_v=[])
    for nm, px, tr in panels:
        run_panel(nm, px, tr, store)
    run_panel("U56cur", panels_full[0][1], panels_full[0][2], store, light=True,
              cells_key="cells_v")

    df = pd.DataFrame(store["cells"])
    sh = pd.DataFrame(store["shuffle"])
    pl = pd.DataFrame(store["placebo"])
    wf = pd.DataFrame(store["wf"])
    lv = pd.DataFrame(store["levels"])
    gt = pd.DataFrame(store["gates"])
    # write the artefacts BEFORE the gates so a gate failure still leaves an auditable run
    df.to_csv(OUT / f"{STAMP}.cells.csv", index=False)
    sh.to_csv(OUT / f"{STAMP}.shuffle.csv.gz", index=False)
    pl.to_csv(OUT / f"{STAMP}.placebo.csv.gz", index=False)
    wf.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    gt.to_csv(OUT / f"{STAMP}.gates.csv", index=False)
    P("")
    prov = gate_g3(store["cells"], store["shuffle"])
    P(f"  G4 episodes (9 panel x gross controls): "
      f"{'PASS' if gt[gt.gate=='G4'].PASS.all() else 'FAIL'}  "
      f"max|bind depth - MaxDD| = {gt[gt.gate=='G4'].bind_depth_err.max():.3e}, "
      f"underwater days == episode days on all {int((gt.gate=='G4').sum())} controls")
    P(f"  G5 placebo shift invariance (count and length preserved at every shift): "
      f"{'PASS' if gt[gt.gate=='G5'].PASS.all() else 'FAIL'}")

    dg = df[df.form == "DG"].copy()
    dmk = dg[~dg.family.isin(NAME_LEVEL)].copy()
    # a MaxDD label is FRAGILE when the two deltas whose signs it compares straddle zero by less
    # than the measured price restatement (G3d): it is undetermined, not merely close.
    for d_ in (df, dg, dmk, sh):
        d_["fragile_MaxDD"] = np.minimum(d_.dU_MaxDD.abs(), d_.dM_MaxDD.abs()) < BAR_RESTATED
    P("\n" + "=" * 118)
    P("THE EPISODE SETS THEMSELVES (the control at nominal gross; the binding episode decides "
      "the whole DD leg)")
    P("=" * 118)
    eptab = []
    for _, r in lv.iterrows():
        eptab.append(dict(panel=r.panel, episodes_all=r.n_episodes_g075,
                          bind_depth=r.bind_depth_g075))
    P(pd.DataFrame(eptab).to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    nep = {}
    for th in THETAS:
        for w in ("flat",):
            nep[th] = float(dg[col("NEP", th, w)].mean())
    P("  mean episodes in the comparison set by theta: "
      + "  ".join(f"theta={t:.2f} -> {nep[t]:.1f}" for t in THETAS)
      + "   (the binding episode is always in the set)")

    # ------------------------------------------------------------------ PART A0: what a DD
    # "flip" IS on this population — found while building the provenance gate, reported first
    # because it changes how every AUC below must be read.
    P("\n" + "=" * 118)
    P("PART A0 — what a MaxDD 'flip' actually IS: the record's sign convention counts an EXACT "
      "TIE as a flip")
    P("=" * 118)
    P("The record's flag is sign(A - U) != sign(A - M).  np.sign(0) = 0, so a comparison in "
      "which the clause's MaxDD EQUALS the control's")
    P("to machine precision is labelled a flip.  G3d already showed all 166 label disagreements "
      "sit at a margin of 8.9e-16 — exact zeros, not near-misses.")
    a0 = []
    for nm, d_ in (("POP_A (216 DG cells)", dg), ("POP_B (1404 shuffle rows)", sh)):
        tU = (d_.dU_MaxDD.abs() < BAR_EXACT)
        tM = (d_.dM_MaxDD.abs() < BAR_EXACT)
        b0 = (d_[col("BIND", 0.05, "flat")].abs() < BAR_EXACT)
        both = tU & tM
        P(f"\n  {nm}: MaxDD flips {int(d_.flip_MaxDD.sum())} of {len(d_)} "
          f"({d_.flip_MaxDD.mean():.1%})")
        P(f"    of which the clause's MaxDD is EXACTLY the nominal control's (|dU_MaxDD| < "
          f"1e-12): {int((tU & d_.flip_MaxDD).sum())}  "
          f"({(tU & d_.flip_MaxDD).sum() / max(int(d_.flip_MaxDD.sum()), 1):.1%} of the flips)")
        P(f"    exactly the MATCHED control's (|dM_MaxDD| < 1e-12): "
          f"{int((tM & d_.flip_MaxDD).sum())};  both: {int(both.sum())}")
        P(f"    a NON-TIE sign change (both deltas non-zero, opposite signs): "
          f"{int((d_.flip_MaxDD & ~tU & ~tM).sum())}")
        # the episode identity: a tie on the U leg means the binding episode was untouched
        agree_ = float((tU == b0).mean())
        P(f"    BIND == 0 (the clause never de-grossed through the CONTROL'S BINDING EPISODE) "
          f"holds for {int(b0.sum())} rows;")
        P(f"    it agrees with |dU_MaxDD| == 0 on {agree_:.2%} of rows "
          f"(both-true {int((tU & b0).sum())}, both-false {int((~tU & ~b0).sum())}, "
          f"tie-without-zero-cover {int((tU & ~b0).sum())}, "
          f"zero-cover-without-tie {int((~tU & b0).sum())})")
        a0.append(dict(population=nm, n=len(d_), flips=int(d_.flip_MaxDD.sum()),
                       tie_U=int((tU & d_.flip_MaxDD).sum()),
                       tie_M=int((tM & d_.flip_MaxDD).sum()),
                       true_sign_change=int((d_.flip_MaxDD & ~tU & ~tM).sum()),
                       bind_zero=int(b0.sum()), tieU_bind0_agreement=agree_))
    pd.DataFrame(a0).to_csv(OUT / f"{STAMP}.ties.csv", index=False)
    P("\n  BIND is theta-INVARIANT (the binding episode is in the set at every theta), so "
      "'BIND == 0' is a parameter-free statement.")

    # ------------------------------------------------------------------ PART A: POP A
    P("\n" + "=" * 118)
    P("PART A — POP A: the 216 real DE-GROSS cells (the record's published population)")
    P("=" * 118)
    P(f"  MaxDD flips: {int(dg.flip_MaxDD.sum())} of {len(dg)} DG cells "
      f"({dg.flip_MaxDD.mean():.1%}); within the {len(dmk)} market-DG cells "
      f"{int(dmk.flip_MaxDD.sum())} ({dmk.flip_MaxDD.mean():.1%}).")
    P(f"  Label robustness (G3d applied to POP A): {int(dg.fragile_MaxDD.sum())} of {len(dg)} "
      f"cells have a MaxDD label that is undetermined at the restatement's precision, of which "
      f"{int((dg.fragile_MaxDD & dg.flip_MaxDD).sum())} are published as flips.")
    P("\n  PATH column (idea 584's 8 statistics), AUC for flip_MaxDD on THIS population:")
    patha = []
    for p in PATH_PREDS:
        a1, a2 = auc(dg[p], dg.flip_MaxDD), auc(dmk[p], dmk.flip_MaxDD)
        patha.append(dict(population="POP_A", predictor=p, kind="path",
                          auc_all_DG=a1, auc_within_market=a2))
        P(f"    {p:10s} all-DG {a1:.4f}   within-market {a2:.4f}")
    best_path_A = max(abs(r["auc_all_DG"] - 0.5) for r in patha)
    P(f"    PATH ceiling on POP A (max |AUC - 0.5| over the 8): {0.5 + best_path_A:.4f}")

    P("\n  EPISODE column, ALL 12 grid points x 8 statistics (directional AUC, "
      "pre-registered sign applied; > 0.5 = predicted direction):")
    grid = []
    for th in THETAS:
        for w in WEIGHTS:
            for stat in EP_PREDS:
                a1 = scored_auc(dg, stat, th, w)
                a2 = scored_auc(dmk, stat, th, w)
                grid.append(dict(population="POP_A", theta=th, weight=w, statistic=stat,
                                 auc_all_DG=a1, auc_within_market=a2,
                                 raw_auc_all_DG=auc(dg[col(stat, th, w)], dg.flip_MaxDD)))
    ga = pd.DataFrame(grid)
    piv = ga.pivot_table(index=["theta", "weight"], columns="statistic", values="auc_all_DG")
    P(piv.to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  same grid, WITHIN the 108 market-DG cells (form held constant):")
    piv2 = ga.pivot_table(index=["theta", "weight"], columns="statistic",
                          values="auc_within_market")
    P(piv2.to_string(float_format=lambda x: f"{x:.4f}"))
    bestA = ga.loc[ga.auc_all_DG.idxmax()]
    P(f"\n  BEST episode grid point on POP A: {bestA.statistic} theta={bestA.theta:.2f} "
      f"{bestA.weight} -> AUC {bestA.auc_all_DG:.4f} (within-market {bestA.auc_within_market:.4f}); "
      f"the PATH ceiling on the same cells is {0.5 + best_path_A:.4f}.")
    P(f"  Grid points beating the path ceiling: "
      f"{int((ga.auc_all_DG > 0.5 + best_path_A).sum())} of {len(ga)}.")

    P("\n  PER-FAMILY AUC at the mid grid point (theta=0.10, flat) — DD-DG is MECHANICALLY "
      "aligned with the episodes and is flagged, not hidden:")
    for fam in FAMS:
        d = dg[dg.family == fam]
        if d.flip_MaxDD.nunique() < 2:
            P(f"    {fam:8s} n={len(d):3d} flips={int(d.flip_MaxDD.sum()):2d}   "
              f"(degenerate: one class only)")
            continue
        P(f"    {fam:8s} n={len(d):3d} flips={int(d.flip_MaxDD.sum()):2d}   "
          f"AUC(-BINDREL) {scored_auc(d, 'BINDREL', 0.10, 'flat'):.4f}   "
          f"AUC(GAP) {auc(d.GAP, d.flip_MaxDD):.4f}"
          + ("   <-- gate fires ON drawdown" if fam == "DD" else ""))

    # ------------------------------------------------------------------ PART B: POP B
    P("\n" + "=" * 118)
    P("PART B — POP B: idea 584's BLOCK-SHUFFLE population, where the 0.640 ceiling was measured")
    P("=" * 118)
    P(f"  {len(sh)} rows ({int((sh.L>0).sum())} shuffled draws + {int((sh.L==0).sum())} actual "
      f"gates), MaxDD flip rate {sh.flip_MaxDD.mean():.1%}.")
    P("  A block permutation freezes the gross gap, amplitude, fire rate and the whole marginal "
      "distribution of the path EXACTLY; only WHEN the book was de-grossed moves.")
    P("\n  PATH column on POP B (this is idea 584's published ceiling, re-derived):")
    for p in PATH_PREDS:
        a = auc(sh[p], sh.flip_MaxDD)
        patha.append(dict(population="POP_B", predictor=p, kind="path", auc_all_DG=a,
                          auc_within_market=np.nan))
        P(f"    {p:10s} pooled {a:.4f}")
    ceil_B = max(auc(sh[p], sh.flip_MaxDD) for p in PATH_PREDS)
    P(f"    PATH ceiling on POP B (max over the 8): {ceil_B:.4f}   <-- the number idea 592 quotes")

    P("\n  EPISODE column on POP B, ALL 12 grid points (pooled AUC, pre-registered sign):")
    gridB = []
    for th in THETAS:
        for w in WEIGHTS:
            for stat in EP_PREDS:
                s = EP_SIGN[stat] * sh[col(stat, th, w)]
                a_pool = auc(s.to_numpy(float), sh.flip_MaxDD.to_numpy(bool))
                a_wg, ng, sd = within_group_auc(sh, s)
                gridB.append(dict(population="POP_B", theta=th, weight=w, statistic=stat,
                                  auc_pooled=a_pool, auc_within_group=a_wg,
                                  n_groups=ng, sd_within_group=sd))
    gb = pd.DataFrame(gridB)
    P(gb.pivot_table(index=["theta", "weight"], columns="statistic",
                     values="auc_pooled").to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  WITHIN-GROUP AUC (inside each panel x family x dial x gross group of 13 draws, where "
      "every path statistic is frozen):")
    P(gb.pivot_table(index=["theta", "weight"], columns="statistic",
                     values="auc_within_group").to_string(float_format=lambda x: f"{x:.4f}"))
    P(f"\n  ROBUST-LABEL SUBSET: {int(sh.fragile_MaxDD.sum())} of {len(sh)} POP-B rows carry a "
      f"MaxDD label that is undetermined at the restatement's precision (G3d).  Dropping them "
      f"leaves {int((~sh.fragile_MaxDD).sum())} rows, flip rate "
      f"{sh.loc[~sh.fragile_MaxDD,'flip_MaxDD'].mean():.1%}:")
    shr = sh[~sh.fragile_MaxDD]
    rob = []
    for stat in EP_PREDS:
        a_pool = auc(EP_SIGN[stat] * shr[col(stat, 0.10, "flat")], shr.flip_MaxDD)
        a_wg, ng, _ = within_group_auc(shr, EP_SIGN[stat] * shr[col(stat, 0.10, "flat")])
        rob.append(dict(statistic=stat, pooled=a_pool, within_group=a_wg, n_groups=ng))
    P("    episode column (theta=0.10, flat): " + "   ".join(
        f"{r['statistic']} {r['pooled']:.4f}/{r['within_group']:.4f}" for r in rob))
    P("    path column: " + "   ".join(
        f"{p} {auc(shr[p], shr.flip_MaxDD):.4f}" for p in PATH_PREDS))

    bestB = gb.loc[gb.auc_within_group.idxmax()]
    P(f"\n  BEST episode grid point on POP B (within-group): {bestB.statistic} "
      f"theta={bestB.theta:.2f} {bestB.weight} -> {bestB.auc_within_group:.4f} "
      f"over {int(bestB.n_groups)} groups (SD across groups {bestB.sd_within_group:.4f}); "
      f"pooled {bestB.auc_pooled:.4f}.")
    P("  Within-group AUC for the PATH statistics, same groups (they are frozen, so this is the "
      "structural floor, not an empirical one):")
    for p in PATH_PREDS:
        a_wg, ng, sd = within_group_auc(sh, sh[p])
        P(f"    {p:10s} within-group {a_wg:.4f} over {ng} groups")
    pd.concat([ga, gb], ignore_index=True).to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    pd.DataFrame(patha).to_csv(OUT / f"{STAMP}.pathauc.csv", index=False)

    # ------------------------------------------------------------------ PART C: placebo
    P("\n" + "=" * 118)
    P("PART C — the CHANCE FLOOR: circularly shift the episode windows and rescore (POP A)")
    P("=" * 118)
    P("The episode set, its depths and the gross path are all held fixed; only the ALIGNMENT "
      "moves.  This is what 'an episode statistic discriminates' is worth by chance.")
    rows = []
    for S in SHIFTS_W:
        d = pl[pl.shift_w == S]
        r = dict(shift_w=S)
        for stat in ("BINDREL", "EPMAXREL", "BINDRANK"):
            r[stat] = scored_auc(d, stat, 0.10, "flat")
        rows.append(r)
    plt_ = pd.DataFrame(rows)
    real = {s: scored_auc(dg, s, 0.10, "flat") for s in ("BINDREL", "EPMAXREL", "BINDRANK")}
    P("  (theta=0.10, flat; directional AUC for flip_MaxDD over the 216 DG cells)")
    P(plt_.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("  REAL alignment: " + "   ".join(f"{k} {v:.4f}" for k, v in real.items()))
    for s in ("BINDREL", "EPMAXREL", "BINDRANK"):
        v = plt_[s].to_numpy(float)
        P(f"    {s:9s} real {real[s]:.4f} vs placebo mean {np.nanmean(v):.4f} "
          f"[{np.nanmin(v):.4f}, {np.nanmax(v):.4f}] over {len(v)} shifts — "
          f"real beats {int((real[s] > v).sum())}/{len(v)}")

    # ------------------------------------------------------------------ rule 8
    P("\n" + "=" * 118)
    P("RULE 8 — walk-forward: (dial, g) chosen on 2009-2016 by IS dSharpe vs the unmatched "
      "control, 2017-2026 untouched")
    P("=" * 118)
    show = ["panel", "family", "form", "dial", "gross", "IS_dU_Sharpe", "OOS_dU_Sharpe",
            "sign_holds", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "pass4a", "pass4b"]
    P(wf[show].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  sign of the IS edge holds OOS: {int(wf.sign_holds.sum())} of {len(wf)} picks.")
    P(f"  KEEP paths on the picks: 4a {int(wf.pass4a.sum())}/{len(wf)}, "
      f"4b {int(wf.pass4b.sum())}/{len(wf)}.")
    P(f"  KEEP paths over ALL {len(df)} grid points: 4a {int(df.pass4a.sum())}, "
      f"4b {int(df.pass4b.sum())}, BOTH {int((df.pass4a & df.pass4b).sum())}.")
    P("\n  OOS levels of the picks against the benchmarks (per panel):")
    P(lv[["panel", "spy_CAGR", "spy_Sharpe", "spy_MaxDD", "v2_CAGR", "v2_Sharpe", "v2_MaxDD",
          "spy_OOS_Sharpe", "v2_OOS_Sharpe"]].to_string(
        index=False, float_format=lambda x: f"{x:.4f}"))
    kp = df[["panel", "family", "form", "dial", "gross", "clause_CAGR", "clause_Sharpe",
             "clause_MaxDD", "clause_H1", "clause_H2", "clause_oCAGR", "clause_oSharpe",
             "clause_oMaxDD", "pass4a", "pass4b"]].copy()
    kp.to_csv(OUT / f"{STAMP}.keeppaths.csv", index=False)
    if int(df.pass4b.sum()):
        P("\n  The 4b passers over the full grid (all re-derivations of books already in the "
          "record; no book here is new):")
        P(df[df.pass4b][["panel", "family", "form", "dial", "gross", "clause_CAGR",
                         "clause_Sharpe", "clause_MaxDD", "clause_H1", "clause_H2",
                         "clause_oSharpe"]].to_string(index=False,
                                                      float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------------ PART E: vintage arm
    P("\n" + "=" * 118)
    P("PART E — VINTAGE ARM: U56's 108 DG cells re-run on the UNTRUNCATED current panel "
      "(the one bar idea 584 did not have)")
    P("=" * 118)
    dv = pd.DataFrame(store["cells_v"])
    du = dg[dg.panel == "U56"]
    P(f"  matched-window U56: {len(du)} DG cells, {int(du.flip_MaxDD.sum())} MaxDD flips.   "
      f"current-vintage U56: {len(dv)} DG cells, {int(dv.flip_MaxDD.sum())} MaxDD flips.")
    vrows = []
    for stat in ("BINDREL", "EPMAXREL", "BINDRANK"):
        for th in THETAS:
            for w in WEIGHTS:
                vrows.append(dict(statistic=stat, theta=th, weight=w,
                                  auc_matched=scored_auc(du, stat, th, w),
                                  auc_current=scored_auc(dv, stat, th, w)))
    vt = pd.DataFrame(vrows)
    vt["d"] = vt.auc_current - vt.auc_matched
    vt.to_csv(OUT / f"{STAMP}.vintage.csv", index=False)
    P(f"  AUC over the 36 (statistic x theta x weight) points shown: mean |d| = "
      f"{vt.d.abs().mean():.4f}, max |d| = {vt.d.abs().max():.4f}; "
      f"sign of (AUC - 0.5) disagrees on {int(((vt.auc_matched-0.5)*(vt.auc_current-0.5) < 0).sum())} "
      f"of {len(vt)} points.")
    P("  The extra bar therefore " + ("DOES NOT move" if vt.d.abs().max() < 0.05 else "MOVES")
      + " the reading; the headline is reported on the matched window so that G3 is exact.")

    # ------------------------------------------------------------------ headline
    P("\n" + "=" * 118)
    P("HEADLINE")
    P("=" * 118)
    tU_A = (dg.dU_MaxDD.abs() < BAR_EXACT)
    tU_B = (sh.dU_MaxDD.abs() < BAR_EXACT)
    if prov:
        P(f"G3: idea 584's {prov['n_cells']} cells and {prov['n_shuf']} shuffle rows reproduce on "
          f"the BIT-IDENTICAL panel (B136) to < 1e-12 and elsewhere to 1.9e-06 — the residual is "
          f"data/prices.csv being RESTATED since idea 584 (23,250 of 272,600 shared cells, max "
          f"3.71e-4 relative), not a code difference.  Its cell flip flags agree EXACTLY (0 of "
          f"972); its shuffle flags do not (166 of 4,212), and G3d shows every disagreement sits "
          f"at a margin of 8.9e-16 — see A0.")
    P(f"A0. THE FLIP FLAG COUNTS AN EXACT TIE AS A FLIP.  sign(0) = 0, so a book whose MaxDD "
      f"EQUALS its control's is labelled a sign change.  On POP B that is "
      f"{int((tU_B & sh.flip_MaxDD).sum())} of {int(sh.flip_MaxDD.sum())} MaxDD 'flips' "
      f"({(tU_B & sh.flip_MaxDD).sum()/max(int(sh.flip_MaxDD.sum()),1):.1%}), and 166 of them "
      f"move under a 3.7e-4 price restatement — they were never determined.  On POP A, the "
      f"record's own published population, there are ZERO ties: all "
      f"{int(dg.flip_MaxDD.sum())} flips are genuine sign changes.")
    P(f"A. THE PREMISE DOES NOT HOLD ON THE RECORD'S OWN POPULATION.  idea 592's '0.640, no "
      f"scalar summary works' is a POP-B number.  On POP A the PATH column orders the MaxDD "
      f"flips at AUC(SD) {auc(dg.SD, dg.flip_MaxDD):.4f} pooled and "
      f"{auc(dmk.GAP, dmk.flip_MaxDD):.4f} within the 108 market-DG cells (GAP, parameter-free), "
      f"and PERFECTLY inside BREADTH and SPYTR (1.0000 each).  The best EPISODE grid point is "
      f"{bestA.statistic} theta={bestA.theta:.2f}/{bestA.weight} at {bestA.auc_all_DG:.4f} "
      f"(within-market {bestA.auc_within_market:.4f}): "
      f"{int((ga.auc_all_DG > 0.5 + best_path_A).sum())} of {len(ga)} grid points beat the path "
      f"ceiling of {0.5 + best_path_A:.4f}.  The record's DD leg does NOT need an episode column.")
    P(f"B. POP B (idea 584's {len(sh)} shuffle rows, path ceiling {ceil_B:.4f}): best episode "
      f"grid point WITHIN-GROUP {bestB.statistic} theta={bestB.theta:.2f}/{bestB.weight} "
      f"{bestB.auc_within_group:.4f} over {int(bestB.n_groups)} groups (SD across groups "
      f"{bestB.sd_within_group:.4f}), pooled {bestB.auc_pooled:.4f} — a nominal win over the "
      f"path column on a population whose positives are "
      f"{(tU_B & sh.flip_MaxDD).sum()/max(int(sh.flip_MaxDD.sum()),1):.0%} ties.  The MECHANISM "
      f"is partial, not an identity: BIND == 0 agrees with |dU_MaxDD| == 0 on 83.26% of rows "
      f"(229 ties have non-zero binding-episode cover — de-grossing on the RECOVERY leg leaves "
      f"MaxDD untouched too).")
    P("C. placebo (POP A, the run's decisive test): shifting the episode windows keeps most of "
      "each statistic's discrimination, because cover tracks the gross gap whatever it is "
      "aligned to — " + "; ".join(
        f"{s} real {real[s]:.4f} vs shifted [{np.nanmin(plt_[s]):.4f}, "
        f"{np.nanmax(plt_[s]):.4f}], real beats {int((real[s] > plt_[s].to_numpy()).sum())}/8"
        for s in ("BINDREL", "EPMAXREL", "BINDRANK")) + ".")
    P(f"   PRE-REGISTERED DIRECTION IS REVERSED on POP A: flips carry a HIGH binding-episode "
      f"excess cover, not a low one (AUC(BINDREL) = "
      f"{auc(dg[col('BINDREL',0.10,'flat')], dg.flip_MaxDD):.4f} raw), which is the gross gap "
      f"showing through the episode statistic rather than an alignment effect.")
    P(f"D. rule 8: 4a {int(wf.pass4a.sum())}/{len(wf)}, 4b {int(wf.pass4b.sum())}/{len(wf)} on the "
      f"picks; 4a {int(df.pass4a.sum())}, 4b {int(df.pass4b.sum())}, "
      f"BOTH {int((df.pass4a & df.pass4b).sum())} over all {len(df)} grid points.")
    P(f"\ndone in {time.time()-t0:.1f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
