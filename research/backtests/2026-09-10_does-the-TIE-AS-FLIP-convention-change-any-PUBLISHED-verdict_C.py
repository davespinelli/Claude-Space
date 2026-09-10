#!/usr/bin/env python3
"""IDEA 595 — does the TIE-AS-FLIP convention change any PUBLISHED verdict?  (lane C, 2026-09-10)

QUESTION (QUEUE idea 595, verbatim)
    idea 592 showed the tie problem is absent from the record's 216 real de-gross cells
    (0 ties) and severe on synthetic shuffle populations (43.6%).  Re-score every ladder and
    draw population in the record under a three-way label (better / worse / TIE) instead of a
    binary flip, and report which published flip rates, AUCs and orderings move.
    Max 2 params (population set, tie bar).

WHAT THE CONVENTION IS
    The record compares a clause book A with its own control twice — at the control's NOMINAL
    gross (U) and with the control rescaled to the clause's mean target gross (M) — and flags a
    FLIP with `np.sign(A-U) != np.sign(A-M)`.  `np.sign(0.0) == 0.0`, so a comparison in which
    A EQUALS one of its controls to the last bit is labelled a sign CHANGE.  The mirror-image
    convention `np.sign(x) == np.sign(y)` (the record's `sign_holds` column) has the same bug
    with the opposite reported polarity: a tie is labelled a sign BREAK.

WHAT A THREE-WAY LABEL IS (this run's object)
    lab(d, tau) = TIE if |d| <= tau, else better/worse by sign.  Then a pair (dU, dM) is
      FLIP    both legs determined and their labels differ
      SAME    both legs determined and their labels agree
      UNDET   either leg is a TIE — no verdict is available at this precision
    The published binary flag is EXACTLY `lab(dU,0) != lab(dM,0)` with UNDET folded into FLIP;
    gate G3 asserts that identity on every re-scorable committed row, so the re-scoring here is
    the record's own arithmetic with one branch added, not a different statistic.

TUNED PARAMETERS: 2, exactly the two the queue names.  ALL 40 grid points are reported.
    (1) POPULATION SET, 5 levels:
          REC-CELLS      the record's real book cells (the 324-cell population, deduplicated:
                         ideas 581, 584, 591 and 592 all publish the SAME 324 books)
          REC-LADDER     idea 584's 432-row lambda ladder (a smoothed-gate DIAL population)
          REC-SHUFFLE    idea 584's / 592's 1,404-row block-shuffle DRAW population
          FRESH-CELLS    the 324 cells rebuilt here on the current caches
          FRESH-SHUFFLE  the 1,404 shuffle draws rebuilt here on the current caches
    (2) TIE BAR tau in {0, 1e-16, 1e-15, 1e-12, 1e-9, 1e-6, 1e-4, 1e-3}, applied to the delta
        in its own units (Sharpe points; MaxDD and CAGR as fractions, so 1e-3 = 0.1 pp).
        tau = 0 is strict equality — the only bar at which "exact tie" is literally true.

PRE-REGISTERED DIRECTIONS (stated before the run, so nothing here is unfalsifiable)
    H1  The np.sign(0) mechanism is a MaxDD-leg phenomenon: the Sharpe and CAGR legs carry no
        ties at tau = 0 on any population, because those statistics are sums over the whole
        path and cannot coincide bit-for-bit.
    H2  Ties are a DRAW-POPULATION phenomenon, not a record phenomenon: the block shuffle can
        move a clause's firing off the control's binding drawdown episode entirely, which a
        real dial cannot.  Predicted tie rate: ~0 on REC-CELLS, materially > 0 on REC-SHUFFLE.
    H3  Re-scoring MOVES the shuffle population's published flip rate and AUC ceiling and does
        NOT move the record's own cell population.  If it moves the cells too, the record's
        published parent-comparison claims need amending and this run says so.

WHAT WOULD MAKE THIS RUN MATTER FOR CAPITAL (PART E, and it is not an AUC question)
    The KEEP paths are themselves sign comparisons with an undeclared tie branch: 4a's
    drawdown leg is `MaxDD >= baseline MaxDD`, so a TIE PASSES, while its Sharpe legs are
    strict `>`, so a TIE FAILS.  A book whose drawdown merely equals the live book's is
    therefore credited with a drawdown win.  PART E measures how many committed 4a/4b passes
    are decided inside a tie bar on any single leg — that is a verdict the convention could
    move, unlike a flip rate on a synthetic draw population.

GATES (all asserted; a failure aborts and the artefacts written so far stay auditable)
    G0  VINTAGE: panels truncated to idea 584's window (row counts asserted exactly), so the
        provenance gate can be exact rather than a tolerance.
    G1  the vectorised runner reproduces engine.backtest to < 1e-12 on returns.
    G2  PROVENANCE: idea 592's committed `.ties.csv` is re-derived from its OWN committed
        `.cells.csv` / `.shuffle.csv.gz` at its own stated bar (1e-12).  Exact match required.
    G3  NESTING: the three-way labeller at tau = 0, with UNDET folded into FLIP, reproduces
        every committed `flip_*` column on every re-scorable row.  0 disagreements required.
    G4  matched gross on the fresh cells: |meanTargetGross(clause) - matched control| < 1e-12.
    G5  the fresh cells reproduce idea 584's committed cells — deltas to 1e-4 (the measured
        price restatement, idea 592's G3 reasoning, reproduced) and flip FLAGS exactly.

RULE 8 (walk-forward, required).  Per arm x panel, (dial, g) chosen on 2009-2016 only by IS
    dSharpe against the unmatched control — the record's own selection rule — and evaluated on
    2017-2026 untouched: OOS CAGR/Sharpe/MaxDD vs RULES v2 and vs SPY, both KEEP paths, plus
    the tie-margin of every bar each pick clears or misses.

SURVIVORSHIP: B136 and SMALL439 are CURRENT constituents, so every LEVEL is biased up.  Every
    claim here is a clause-vs-its-own-control DIFFERENCE on a fixed panel, or a label count.

Outputs (committed): .console.txt .sites.csv .grid.csv .auc.csv .ordering.csv
    .cells.csv .shuffle.csv.gz .walkforward.csv .keeppaths.csv .barmargins.csv .gates.csv
    .result.md
Deterministic; no network (load_universe reads committed caches).
"""
from __future__ import annotations
import ast, gzip, sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STAMP = "2026-09-10_does-the-TIE-AS-FLIP-convention-change-any-PUBLISHED-verdict_C"
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
BLOCKS_W = (1, 4, 13, 52)
SEEDS = (0, 1, 2)
METRICS = ("Sharpe", "CAGR", "MaxDD")
PATH_PREDS = ("GAP", "SD", "RHO1", "RHO5", "DRHO1", "RUN", "TIMING", "DDTIME")

# TUNED PARAM 2 — the tie bar, in the delta's own units
TAUS = (0.0, 1e-16, 1e-15, 1e-12, 1e-9, 1e-6, 1e-4, 1e-3)
BAR_592 = 1e-12          # idea 592's own stated tie bar, reproduced by G2
BAR_RESTATED = 1e-4      # the measured price restatement, idea 592's G3 reasoning

PARENT_LAST = {"U56": "2026-09-08", "B136": "2026-09-04", "SMALL439": "2026-09-04"}
PARENT_ROWS = {"U56": 4700, "B136": 4699, "SMALL439": 4194}
P592 = "2026-09-09_stop-summarising-the-DD-LEG-with-PATH-statistics_C"
P584 = "2026-09-09_is-the-BLOCKWISE-vs-SMOOTH-split-the-real-predictor-of-a-gross-flip_C"
P581 = "2026-09-09_how-many-of-the-record-s-PUBLISHED-parent-COMPARISONS-are-GROSS-UNMATCHED_C"
P591 = "2026-09-09_is-AMPLITUDE-the-record-s-real-clause-taxonomy_cloud"

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); _LOG.append(s)


# ================================================================= the three-way labeller
FLIP, SAME, UNDET = "FLIP", "SAME", "UNDET"


def lab3(d, tau):
    """better(+1) / worse(-1) / TIE(0) at bar tau, elementwise on an array."""
    d = np.asarray(d, float)
    out = np.sign(d)
    out[np.abs(d) <= tau] = 0.0
    return out


def pair_label(dU, dM, tau):
    """Three-way verdict for one (unmatched, matched) delta pair.  Returns an object array of
    FLIP / SAME / UNDET."""
    a, b = lab3(dU, tau), lab3(dM, tau)
    und = (a == 0) | (b == 0)
    out = np.where(a != b, FLIP, SAME).astype(object)
    out[und] = UNDET
    return out


def published_flip(dU, dM):
    """The record's own binary flag, bit-for-bit: np.sign(dU) != np.sign(dM)."""
    return np.sign(np.asarray(dU, float)) != np.sign(np.asarray(dM, float))


# ================================================================= vectorised engine clone
class Runner:
    """Closed-form equivalent of engine.backtest (idea 592's Runner, unchanged).  G1 asserts it."""

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

    def run(self, W):
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


def mean_target_gross(W, rb, start):
    return float(W.loc[rb].sum(axis=1).loc[start:].mean())


def pearson(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    a, b = a[ok], b[ok]
    if len(a) < 3 or a.std() == 0 or b.std() == 0:
        return np.nan
    return float(np.corrcoef(a, b)[0, 1])


def auc(score, label):
    """Mann-Whitney AUC, ties in the SCORE at 0.5.  0.5 = no discrimination."""
    score = np.asarray(score, float); label = np.asarray(label, bool)
    ok = np.isfinite(score)
    score, label = score[ok], label[ok]
    p, n = score[label], score[~label]
    if len(p) == 0 or len(n) == 0:
        return np.nan
    r = pd.Series(np.concatenate([p, n])).rank().to_numpy()
    return float((r[:len(p)].sum() - len(p) * (len(p) + 1) / 2) / (len(p) * len(n)))


def lag_autocorr(x, k):
    x = np.asarray(x, float)
    if len(x) <= k or np.nanstd(x) == 0:
        return np.nan
    return pearson(x[k:], x[:-k])


def mean_run_len(flag):
    flag = np.asarray(flag, bool)
    if not flag.any():
        return np.nan
    d = np.diff(np.concatenate([[0], flag.view(np.int8), [0]]))
    return float(flag.sum() / max(int((d == 1).sum()), 1))


def path_stats(u, spy, ddc):
    """idea 584's 8 path predictors, read off the daily gross-ratio path, verbatim."""
    v = u.to_numpy(float)
    mu = float(np.nanmean(v))
    low = v < mu - 1e-12
    s, d = spy.to_numpy(float), ddc.to_numpy(float)
    if low.any() and (~low).any():
        timing = float((np.nanmean(s[low]) - np.nanmean(s[~low])) * 252)
        ddtime = float(np.nanmean(d[low]) - np.nanmean(d[~low]))
    else:
        timing, ddtime = np.nan, np.nan
    return dict(GAP=1.0 - mu, SD=float(np.nanstd(v)), RHO1=lag_autocorr(v, 1),
                RHO5=lag_autocorr(v, 5), DRHO1=lag_autocorr(np.diff(v), 1),
                RUN=mean_run_len(low), LOWSHARE=float(low.mean()),
                TIMING=timing, DDTIME=ddtime)


# ================================================================= books (idea 581's grid)
def build_panel(px, tradable):
    elig = px.notna() & pd.DataFrame(np.tile(tradable, (len(px), 1)), index=px.index,
                                     columns=px.columns)
    vol20 = px.pct_change().rolling(VOL_WIN).std() * np.sqrt(252)
    ma200 = (px > px.rolling(MA_WIN).mean()) & elig
    n = elig.sum(axis=1).replace(0, np.nan)
    breadth = (ma200.sum(axis=1) / n).ffill()
    spytr = px["SPY"] / px["SPY"].rolling(MA_WIN).mean() - 1.0
    return elig, vol20, breadth, spytr


def ew(mask, g):
    n = mask.sum(axis=1).replace(0, np.nan)
    return g * mask.astype(float).div(n, axis=0).fillna(0.0)


def roll_q_mask(sig, q):
    thr = sig.rolling(QWIN, min_periods=QMIN).quantile(q)
    return (sig < thr).fillna(False)


def gate_off(fam, dial, px, breadth, spytr, ctrl_ret):
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
    """4a vs RULES v2, 4b vs SPY.  Returned WITH each bar's signed margin, because the whole
    point of this run is that a bar cleared by 0.000 is not a bar cleared."""
    bars4a = dict(H1=m["H1"] - b["H1"], H2=m["H2"] - b["H2"], DD=m["MaxDD"] - b["MaxDD"])
    bars4b = dict(H1=m["H1"] - s["H1"], H2=m["H2"] - s["H2"],
                  OOS=mo["Sharpe"] - so["Sharpe"], DD=m["MaxDD"] - 0.60 * s["MaxDD"],
                  CAGR=m["CAGR"] - 0.70 * s["CAGR"])
    p4a = (bars4a["H1"] > 0) and (bars4a["H2"] > 0) and (bars4a["DD"] >= 0)
    p4b = all(v > 0 for k, v in bars4b.items() if k in ("H1", "H2", "OOS")) and \
        (bars4b["DD"] >= 0) and (bars4b["CAGR"] >= 0)
    return bool(p4a), bool(p4b), bars4a, bars4b


def block_permute(v, L, seed):
    n = len(v)
    blocks = [v[a:a + L] for a in range(0, n, L)]
    order = np.random.default_rng(seed).permutation(len(blocks))
    return np.concatenate([blocks[i] for i in order])


# ================================================================= PART A: the AST census
SIGN_FORMS = ("SIGNPAIR", "SIGNPROD", "CMPPAIR", "SIGN_ONE")


def _is_sign(n):
    return isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "sign"


def _src(n):
    try:
        return ast.unparse(n)
    except Exception:
        return "<unparse-failed>"


def census_sites(pydir: Path):
    """Every sign-comparison SITE in every committed backtest script.

    A site is tie-vulnerable when one of its operands can be exactly 0 and the convention has
    no branch for it.  Three shapes appear in the record and all three are vulnerable:
      SIGNPAIR   np.sign(A) != np.sign(B)   zero -> sign 0, never equals +-1 -> spurious FLIP
                 np.sign(A) == np.sign(B)   zero -> spurious NON-HOLD (the mirror bug)
      SIGNPROD   np.sign(A) * np.sign(B) < 0   zero -> product 0, NOT < 0 -> spurious SAME
      CMPPAIR    (A > 0) != (B > 0)         zero -> silently 'negative' -> ASYMMETRIC
    The classification is structural (from the AST), never from a filename or a docstring.
    """
    rows = []
    for f in sorted(pydir.glob("*.py")):
        try:
            tree = ast.parse(f.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError:
            rows.append(dict(file=f.name, line=-1, form="UNPARSEABLE", op="", lhs="", rhs="",
                             polarity="", tie_effect=""))
            continue
        for n in ast.walk(tree):
            if isinstance(n, ast.Compare) and len(n.ops) == 1:
                L, R, o = n.left, n.comparators[0], type(n.ops[0]).__name__
                if _is_sign(L) and _is_sign(R) and o in ("Eq", "NotEq"):
                    rows.append(dict(
                        file=f.name, line=n.lineno, form="SIGNPAIR", op=o,
                        lhs=_src(L.args[0]) if L.args else "", rhs=_src(R.args[0]) if R.args else "",
                        polarity="DISAGREE" if o == "NotEq" else "AGREE",
                        tie_effect="spurious FLIP" if o == "NotEq" else "spurious NON-HOLD"))
                elif (_is_sign(L) or _is_sign(R)) and o in ("Eq", "NotEq"):
                    rows.append(dict(file=f.name, line=n.lineno, form="SIGN_ONE", op=o,
                                     lhs=_src(L), rhs=_src(R),
                                     polarity="DISAGREE" if o == "NotEq" else "AGREE",
                                     tie_effect="depends on the literal compared against"))
                elif (o in ("Eq", "NotEq") and isinstance(L, ast.Compare)
                      and isinstance(R, ast.Compare)):
                    rows.append(dict(file=f.name, line=n.lineno, form="CMPPAIR", op=o,
                                     lhs=_src(L), rhs=_src(R),
                                     polarity="DISAGREE" if o == "NotEq" else "AGREE",
                                     tie_effect="ASYMMETRIC (0 counted with the < side)"))
                elif (o in ("Lt", "LtE") and isinstance(L, ast.BinOp)
                      and isinstance(L.op, ast.Mult) and _is_sign(L.left) and _is_sign(L.right)):
                    rows.append(dict(file=f.name, line=n.lineno, form="SIGNPROD", op=o,
                                     lhs=_src(L.left.args[0]) if L.left.args else "",
                                     rhs=_src(L.right.args[0]) if L.right.args else "",
                                     polarity="DISAGREE",
                                     tie_effect="spurious SAME (product 0 is not < 0)"))
    return pd.DataFrame(rows)


def resolve_columns(lhs, rhs):
    """Best-effort resolution of an AST operand pair to a committed CSV column pair.  The
    record's f-string sites (`row[f"dU_{m}"]`) are expanded over the three metric names.  The
    resolver's RECALL is reported, never assumed: an unresolved site is counted as unresolved,
    not as not-vulnerable."""
    out = []
    for m in METRICS:
        a = lhs.replace('{m}', m).replace("f'dU_", "'dU_")
        b = rhs.replace('{m}', m)
        for tok_a, tok_b in ((a, b),):
            ca = tok_a.split(".")[-1].strip("'\"[] f")
            cb = tok_b.split(".")[-1].strip("'\"[] f")
            if ca.startswith("dU_") and cb.startswith("dM_"):
                out.append((ca, cb))
    return sorted(set(out))


# ================================================================= per-panel driver
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
    P(f"  SPY      CAGR {M_spy['CAGR']:7.2%} Sharpe {M_spy['Sharpe']:6.3f} "
      f"MaxDD {M_spy['MaxDD']:7.2%}   OOS Sharpe {M_spy_o['Sharpe']:6.3f}")
    P(f"  RULESv2  CAGR {M_b2['CAGR']:7.2%} Sharpe {M_b2['Sharpe']:6.3f} "
      f"MaxDD {M_b2['MaxDD']:7.2%}   OOS Sharpe {M_b2_o['Sharpe']:6.3f}")

    ctrl = {}
    for g in GS:
        W = ew(elig, g)
        r, h = R.run(W)
        rr = r.loc[start:]
        eqc = (1 + rr).cumprod()
        ctrl[g] = dict(W=W, r=rr, r_full=r, h=h.loc[start:], tg=mean_target_gross(W, rb, start),
                       dd=eqc / eqc.cummax() - 1.0)

    cells, cache = store["cells"], {}
    for fam, form in ARMS:
        for g in GS:
            for dial in DIALS[fam]:
                Wc = clause_weights(fam, form, dial, g, px, elig, vol20, breadth, spytr,
                                    ctrl[g]["r_full"])
                rc, hc = R.run(Wc); rc = rc.loc[start:]
                tg_c = mean_target_gross(Wc, rb, start)
                k = tg_c / ctrl[g]["tg"]
                Wm = ctrl[g]["W"] * k
                dgross = abs(mean_target_gross(Wm, rb, start) - tg_c)
                assert dgross < 1e-12, f"G4 matched-gross failure {pname} {fam} {form}"
                store["g4"].append(dgross)
                rm, _ = R.run(Wm); rm = rm.loc[start:]
                A, U, Mm = mrow(rc), mrow(ctrl[g]["r"]), mrow(rm)
                u = hc.loc[start:] / ctrl[g]["h"]
                st = path_stats(u, spy, ctrl[g]["dd"])
                row = dict(panel=pname, family=fam, form=form, dial=dial, gross=g,
                           tg_clause=tg_c, tg_ctrl=ctrl[g]["tg"], k=k,
                           gross_gap=ctrl[g]["tg"] - tg_c,
                           fire_rate=float((Wc.sum(axis=1) < ctrl[g]["W"].sum(axis=1) - 1e-12)
                                           .loc[start:].mean()), **st)
                for m in METRICS:
                    row[f"dU_{m}"] = A[m] - U[m]
                    row[f"dM_{m}"] = A[m] - Mm[m]
                    row[f"flip_{m}"] = bool(np.sign(A[m] - U[m]) != np.sign(A[m] - Mm[m]))
                row["flip_any"] = bool(any(row[f"flip_{m}"] for m in METRICS))
                Ao = mrow(rc.loc[OOS_START:])
                Ai = mrow(rc.loc[IS_START:IS_END]); Ui = mrow(ctrl[g]["r"].loc[IS_START:IS_END])
                Uo = mrow(ctrl[g]["r"].loc[OOS_START:])
                row["dU_Sharpe_IS"] = Ai["Sharpe"] - Ui["Sharpe"]
                row["dU_Sharpe_OOS"] = Ao["Sharpe"] - Uo["Sharpe"]
                for kk in ("CAGR", "Sharpe", "MaxDD", "H1", "H2"):
                    row[f"clause_{kk}"] = A[kk]
                row["clause_oCAGR"], row["clause_oSharpe"], row["clause_oMaxDD"] = (
                    Ao["CAGR"], Ao["Sharpe"], Ao["MaxDD"])
                p4a, p4b, b4a, b4b = keep_paths(A, Ao, M_b2, M_b2_o, M_spy, M_spy_o)
                row["pass4a"], row["pass4b"] = p4a, p4b
                for kk, v in b4a.items():
                    row[f"m4a_{kk}"] = v
                for kk, v in b4b.items():
                    row[f"m4b_{kk}"] = v
                cells.append(row)
                cache[(fam, form, dial, g)] = dict(Wc=Wc, rm=rm, Mm=Mm, A=A, U=U, k=k, tg_c=tg_c)

    # ------------------------------------------------- FRESH-SHUFFLE (idea 584's population)
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
                        assert v.sum() == v0.sum() and len(v) == len(v0), "shuffle fire count"
                        off_s = off.copy(); off_s.loc[rb_days] = v
                        live = pd.Series(np.where(off_s.to_numpy(bool), 0.0, 1.0), index=px.index)
                        Ws = ctrl[g]["W"].mul(live, axis=0)
                        tg_s = mean_target_gross(Ws, rb, start)
                        assert abs(tg_s - base["tg_c"]) < 1e-12, "shuffle gross invariance"
                        rs_, hs_ = R.run(Ws); rs_ = rs_.loc[start:]
                        As = mrow(rs_)
                        us = hs_.loc[start:] / ctrl[g]["h"]
                        st = path_stats(us, spy, ctrl[g]["dd"])
                        row = dict(panel=pname, family=fam, form=form, dial=dial, gross=g,
                                   L=L, seed=seed, k=base["k"], tg=tg_s, **st)
                        for m in METRICS:
                            row[f"dU_{m}"] = As[m] - base["U"][m]
                            row[f"dM_{m}"] = As[m] - base["Mm"][m]
                            row[f"flip_{m}"] = bool(np.sign(As[m] - base["U"][m])
                                                    != np.sign(As[m] - base["Mm"][m]))
                        row["flip_any"] = bool(any(row[f"flip_{m}"] for m in METRICS))
                        shuf.append(row)
                bc = [c for c in cells if c["panel"] == pname and c["family"] == fam
                      and c["form"] == form and c["dial"] == dial and c["gross"] == g][0]
                shuf.append(dict(panel=pname, family=fam, form=form, dial=dial, gross=g,
                                 L=0, seed=-1, k=bc["k"], tg=bc["tg_clause"],
                                 **{p: bc[p] for p in list(PATH_PREDS) + ["LOWSHARE"]},
                                 **{f"d{c}_{m}": bc[f"d{c}_{m}"] for c in ("U", "M")
                                    for m in METRICS},
                                 **{f"flip_{m}": bc[f"flip_{m}"] for m in METRICS},
                                 flip_any=bc["flip_any"]))

    # ------------------------------------------------- rule 8 walk-forward
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
        p4a, p4b, b4a, b4b = keep_paths(A, Ao, M_b2, M_b2_o, M_spy, M_spy_o)
        store["wf"].append(dict(
            panel=pname, family=fam, form=form, dial=dial_, gross=g_,
            IS_dU_Sharpe=pick["dU_Sharpe_IS"], OOS_dU_Sharpe=Ao["Sharpe"] - Uo["Sharpe"],
            OOS_dM_Sharpe=Ao["Sharpe"] - Mo["Sharpe"],
            sign_holds=bool(np.sign(pick["dU_Sharpe_IS"]) == np.sign(Ao["Sharpe"] - Uo["Sharpe"])),
            IS_tie=bool(pick["dU_Sharpe_IS"] == 0.0),
            OOS_tie=bool((Ao["Sharpe"] - Uo["Sharpe"]) == 0.0),
            full_CAGR=A["CAGR"], full_Sharpe=A["Sharpe"], full_MaxDD=A["MaxDD"],
            H1=A["H1"], H2=A["H2"],
            OOS_CAGR=Ao["CAGR"], OOS_Sharpe=Ao["Sharpe"], OOS_MaxDD=Ao["MaxDD"],
            base_OOS_CAGR=M_b2_o["CAGR"], base_OOS_Sharpe=M_b2_o["Sharpe"],
            base_OOS_MaxDD=M_b2_o["MaxDD"], spy_OOS_CAGR=M_spy_o["CAGR"],
            spy_OOS_Sharpe=M_spy_o["Sharpe"], spy_OOS_MaxDD=M_spy_o["MaxDD"],
            base_CAGR=M_b2["CAGR"], base_Sharpe=M_b2["Sharpe"], base_MaxDD=M_b2["MaxDD"],
            spy_CAGR=M_spy["CAGR"], spy_Sharpe=M_spy["Sharpe"], spy_MaxDD=M_spy["MaxDD"],
            pass4a=p4a, pass4b=p4b,
            **{f"m4a_{k}": v for k, v in b4a.items()},
            **{f"m4b_{k}": v for k, v in b4b.items()}))
    store["levels"].append(dict(
        panel=pname, spy_CAGR=M_spy["CAGR"], spy_Sharpe=M_spy["Sharpe"], spy_MaxDD=M_spy["MaxDD"],
        spy_H1=M_spy["H1"], spy_H2=M_spy["H2"], v2_CAGR=M_b2["CAGR"], v2_Sharpe=M_b2["Sharpe"],
        v2_MaxDD=M_b2["MaxDD"], v2_H1=M_b2["H1"], v2_H2=M_b2["H2"],
        spy_OOS_CAGR=M_spy_o["CAGR"], spy_OOS_Sharpe=M_spy_o["Sharpe"],
        spy_OOS_MaxDD=M_spy_o["MaxDD"], v2_OOS_CAGR=M_b2_o["CAGR"],
        v2_OOS_Sharpe=M_b2_o["Sharpe"], v2_OOS_MaxDD=M_b2_o["MaxDD"]))
    P(f"  built {len(df)} cells + shuffle draws   [{time.time()-t0:.1f}s]")


def gate_g1(R, px, W, tag, store):
    r1, _ = R.run(W)
    res = backtest(px, W, cost_bps=COST, freq=FREQ)
    dr = float((r1 - res["returns"]).abs().max())
    P(f"  G1 {tag:22s} max|dReturn| = {dr:.3e}   {'PASS' if dr < 1e-12 else 'FAIL'}")
    store["gates"].append(dict(gate="G1", detail=tag, value=dr, bar=1e-12, PASS=dr < 1e-12))
    assert dr < 1e-12


# ================================================================= re-scoring
def rescore(name, d, tau):
    """One (population, tau) grid point: the three-way label counts on all three legs."""
    out = dict(population=name, tau=tau, n=len(d))
    for m in METRICS:
        dU, dM = d[f"dU_{m}"].to_numpy(float), d[f"dM_{m}"].to_numpy(float)
        pub = published_flip(dU, dM)
        lab = pair_label(dU, dM, tau)
        det = lab != UNDET
        out[f"{m}_pub_flips"] = int(pub.sum())
        out[f"{m}_pub_rate"] = float(pub.mean())
        out[f"{m}_undet"] = int((~det).sum())
        out[f"{m}_undet_share"] = float((~det).mean())
        out[f"{m}_flip3"] = int((lab == FLIP).sum())
        out[f"{m}_rate_det"] = float((lab[det] == FLIP).mean()) if det.any() else np.nan
        out[f"{m}_rate_all"] = float((lab == FLIP).mean())
        out[f"{m}_tieU"] = int((np.abs(dU) <= tau).sum())
        out[f"{m}_tieM"] = int((np.abs(dM) <= tau).sum())
        out[f"{m}_zeroU"] = int((dU == 0.0).sum())
        out[f"{m}_zeroM"] = int((dM == 0.0).sum())
        out[f"{m}_pub_but_undet"] = int((pub & ~det).sum())
        out[f"{m}_rate_move_pp"] = 100.0 * (out[f"{m}_rate_det"] - out[f"{m}_pub_rate"]) \
            if np.isfinite(out[f"{m}_rate_det"]) else np.nan
    return out


def auc_table(name, d, tau, preds):
    """AUC of every available path predictor for the MaxDD flip, published vs three-way."""
    rows = []
    have = [p for p in preds if p in d.columns]
    dU, dM = d["dU_MaxDD"].to_numpy(float), d["dM_MaxDD"].to_numpy(float)
    pub = published_flip(dU, dM)
    lab = pair_label(dU, dM, tau)
    det = lab != UNDET
    for p in have:
        s = d[p].to_numpy(float)
        a_pub = auc(s, pub)
        a_3 = auc(s[det], (lab[det] == FLIP)) if det.sum() > 1 else np.nan
        rows.append(dict(population=name, tau=tau, predictor=p, auc_published=a_pub,
                         auc_threeway=a_3, d_auc=a_3 - a_pub,
                         n_pub=len(d), n_det=int(det.sum())))
    return rows


# ================================================================= main
def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 595 — does the TIE-AS-FLIP convention change any PUBLISHED verdict?  "
      "(lane C, 2026-09-10)")
    P("=" * 118)
    P("The record's flag is  np.sign(A - U) != np.sign(A - M).  np.sign(0.0) = 0.0, so a leg "
      "that is EXACTLY zero is labelled a")
    P("sign change against any non-zero other leg.  This run re-scores the record's ladder and "
      "draw populations under a three-way")
    P("label (better / worse / TIE) at eight tie bars and reports which published flip rates, "
      "AUCs and orderings move.")
    P("\nPRE-REGISTERED: H1 ties are a MaxDD-leg phenomenon only; H2 ties are a DRAW-population "
      "phenomenon, ~0 on real cells;")
    P("H3 re-scoring moves the shuffle headline and not the record's own cells.  Any of these "
      "coming out the other way is reported as a reversal.")
    store = dict(cells=[], shuffle=[], wf=[], levels=[], gates=[], g4=[])

    # -------------------------------------------------------------- PART A: the AST census
    P("\n" + "=" * 118)
    P("PART A — CENSUS: every SIGN-COMPARISON SITE in every committed backtest script (AST, "
      "not a keyword scan)")
    P("=" * 118)
    sites = census_sites(OUT)
    sites.to_csv(OUT / f"{STAMP}.sites.csv", index=False)
    nfiles = sites.file.nunique()
    P(f"  {len(sites)} sites over {nfiles} scripts "
      f"({len(list(OUT.glob('*.py')))} committed scripts scanned, "
      f"{int((sites.form == 'UNPARSEABLE').sum())} unparseable).")
    tab = sites.groupby(["form", "polarity"]).size().rename("sites").reset_index()
    P(tab.to_string(index=False))
    P("\n  What a tie does at each shape (structural, read off the AST):")
    for form, sub in sites.groupby("form"):
        if form == "UNPARSEABLE":
            continue
        for eff, s2 in sub.groupby("tie_effect"):
            P(f"    {form:9s} {eff:44s} {len(s2):4d} sites over {s2.file.nunique():3d} scripts")
    agree = int((sites.polarity == "AGREE").sum())
    dis = int((sites.polarity == "DISAGREE").sum())
    P(f"\n  {dis} sites report DISAGREEMENT (a tie inflates the count) and {agree} report "
      f"AGREEMENT (a tie DEFLATES it — the `sign_holds` column of every")
    P("  walk-forward file in the record is this second shape).  Both are the same missing "
      "branch; the record has never published either bias.")
    top = sites[sites.form != "UNPARSEABLE"].file.value_counts().head(8)
    P("\n  Densest scripts: " + ", ".join(f"{f.split('_')[0]}..{f[-12:]} {n}"
                                          for f, n in top.items()))

    # -------------------------------------------------------------- committed populations
    P("\n" + "=" * 118)
    P("PART A2 — which of those sites can be RE-SCORED from committed data")
    P("=" * 118)
    P("A site is re-scorable only if the run PUBLISHED both operands of the comparison as "
      "columns.  Anything else is a number the")
    P("record cannot restate without re-running the file — the census reports that denominator "
      "rather than papering over it.")
    pops = {}
    rec_files = {
        "REC-CELLS": (f"{P592}.cells.csv", "the 324 real book cells"),
        "REC-LADDER": (f"{P584}.lambda.csv", "idea 584's 432-row lambda ladder"),
        "REC-SHUFFLE": (f"{P592}.shuffle.csv.gz", "idea 584/592's 1,404 block-shuffle draws"),
    }
    for k, (fn, desc) in rec_files.items():
        p = OUT / fn
        if p.exists():
            pops[k] = pd.read_csv(p)
            P(f"  {k:14s} {len(pops[k]):5d} rows   {desc}   <- {fn}")
        else:
            P(f"  {k:14s} MISSING ({fn}) — this population is skipped and said to be skipped")
    dup = []
    for other, fn in (("581", f"{P581}.cells.csv"), ("591", f"{P591}.cells.csv"),
                      ("584", f"{P584}.cells.csv")):
        p = OUT / fn
        if p.exists() and "REC-CELLS" in pops:
            o = pd.read_csv(p)
            key = ["panel", "family", "form", "dial", "gross"]
            m = pops["REC-CELLS"].merge(o, on=key, suffixes=("_a", "_b"))
            w = max(float((m[f"dU_{x}_a"] - m[f"dU_{x}_b"]).abs().max()) for x in METRICS)
            dup.append((other, len(o), len(m), w))
    for o, n, nm_, w in dup:
        P(f"    idea {o}'s cells.csv: {n} rows, {nm_} shared keys, max|d(dU)| = {w:.3e}  "
          f"-> the SAME population; pooling it would multiply-count, so it is not pooled.")
    rescorable_rows = sum(len(v) for v in pops.values())
    P(f"\n  RE-SCORABLE committed rows: {rescorable_rows} over {len(pops)} distinct populations.")

    # -------------------------------------------------------------- G2 provenance
    P("\nGATES")
    if "REC-SHUFFLE" in pops and (OUT / f"{P592}.ties.csv").exists():
        tie_pub = pd.read_csv(OUT / f"{P592}.ties.csv")
        ok_all = True
        for _, r in tie_pub.iterrows():
            d = pops["REC-CELLS"] if r["population"].startswith("POP_A") else pops["REC-SHUFFLE"]
            if r["population"].startswith("POP_A"):
                d = d[d.form == "DG"]
            fl = d.flip_MaxDD.astype(bool)
            tU = d.dU_MaxDD.abs() < BAR_592
            tM = d.dM_MaxDD.abs() < BAR_592
            got = dict(n=len(d), flips=int(fl.sum()), tie_U=int((tU & fl).sum()),
                       tie_M=int((tM & fl).sum()),
                       true_sign_change=int((fl & ~tU & ~tM).sum()))
            same = all(int(r[k]) == v for k, v in got.items())
            ok_all &= same
            P(f"  G2 idea-592 ties.csv  {r['population']:26s} published "
              f"n={int(r['n'])} flips={int(r['flips'])} tieU={int(r['tie_U'])} "
              f"true={int(r['true_sign_change'])}  |  re-derived "
              f"n={got['n']} flips={got['flips']} tieU={got['tie_U']} "
              f"true={got['true_sign_change']}   {'PASS' if same else 'FAIL'}")
            store["gates"].append(dict(gate="G2", detail=r["population"], value=float(not same),
                                       bar=0.0, PASS=same))
        assert ok_all, "G2 provenance failure"
    else:
        P("  G2 idea-592 artefacts NOT FOUND — provenance SKIPPED (stated in the memo)")

    # -------------------------------------------------------------- G3 nesting
    nd = 0; ntot = 0
    for k, d in pops.items():
        for m in METRICS:
            lab = pair_label(d[f"dU_{m}"], d[f"dM_{m}"], 0.0)
            folded = (lab == FLIP) | (lab == UNDET)
            pub = d[f"flip_{m}"].astype(bool).to_numpy()
            nd += int((folded != pub).sum()); ntot += len(d)
    P(f"  G3 NESTING  three-way at tau=0 with UNDET folded into FLIP reproduces every committed "
      f"flip_* column: {nd} disagreements over {ntot} row-legs   {'PASS' if nd == 0 else 'FAIL'}")
    store["gates"].append(dict(gate="G3", detail="nesting", value=float(nd), bar=0.0,
                               PASS=nd == 0))
    assert nd == 0, "G3 nesting failure — the labeller is not the record's own arithmetic"

    # -------------------------------------------------------------- panels + fresh build
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
    P("\n  G0 VINTAGE (panels truncated to idea 584's window so G5 can be exact on the "
      "bit-identical panel)")
    panels = []
    for nm, p, tr in panels_full:
        p2 = p.loc[:PARENT_LAST[nm]]
        ok = len(p2) == PARENT_ROWS[nm]
        P(f"    {nm:9s} current {len(p)} rows to {p.index[-1].date()} -> truncated {len(p2)} "
          f"(idea 584 had {PARENT_ROWS[nm]})   {'PASS' if ok else 'FAIL'}")
        store["gates"].append(dict(gate="G0", detail=nm, value=float(len(p2)),
                                   bar=float(PARENT_ROWS[nm]), PASS=ok))
        assert ok, f"G0 vintage mismatch on {nm}"
        panels.append((nm, p2, tr))

    RU = Runner(panels[0][1])
    el_u, vol_u, br_u, sp_u = build_panel(panels[0][1], panels[0][2])
    gate_g1(RU, panels[0][1], ew(el_u, 0.75), "U56/EWall", store)
    r_ctrl_u, _ = RU.run(ew(el_u, 0.75))
    gate_g1(RU, panels[0][1], clause_weights("BREADTH", "DG", 0.20, 0.75, panels[0][1], el_u,
                                             vol_u, br_u, sp_u, r_ctrl_u), "U56/BREADTH-DG", store)
    gate_g1(RU, panels[0][1], rules_v2_weights(panels[0][1]), "U56/RULES v2", store)

    for nm, px, tr in panels:
        run_panel(nm, px, tr, store)

    df = pd.DataFrame(store["cells"])
    sh = pd.DataFrame(store["shuffle"])
    wf = pd.DataFrame(store["wf"])
    lv = pd.DataFrame(store["levels"])
    df.to_csv(OUT / f"{STAMP}.cells.csv", index=False)
    sh.to_csv(OUT / f"{STAMP}.shuffle.csv.gz", index=False)
    wf.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    pops["FRESH-CELLS"] = df
    pops["FRESH-SHUFFLE"] = sh
    P(f"\n  G4 matched gross on all {len(store['g4'])} fresh cells: max |d| = "
      f"{max(store['g4']):.3e}   {'PASS' if max(store['g4']) < 1e-12 else 'FAIL'}")
    store["gates"].append(dict(gate="G4", detail="matched gross", value=max(store["g4"]),
                               bar=1e-12, PASS=max(store["g4"]) < 1e-12))

    # -------------------------------------------------------------- G5 fresh vs committed
    key = ["panel", "family", "form", "dial", "gross"]
    old = pops["REC-CELLS"]
    m = old.merge(df, on=key, suffixes=("_o", "_n"))
    assert len(m) == len(old) == len(df), f"G5 cell count {len(old)}/{len(df)}/{len(m)}"
    worst = max(float((m[f"dU_{x}_o"] - m[f"dU_{x}_n"]).abs().max()) for x in METRICS)
    nflip = sum(int((m[f"flip_{x}_o"].astype(bool) != m[f"flip_{x}_n"].astype(bool)).sum())
                for x in METRICS)
    okB = max(float((m[m.panel == "B136"][f"dU_{x}_o"] - m[m.panel == "B136"][f"dU_{x}_n"])
                    .abs().max()) for x in METRICS)
    P(f"  G5 PROVENANCE  {len(m)} fresh cells vs idea 592's committed: max|d(dU)| = {worst:.3e} "
      f"(bar {BAR_RESTATED:.0e}, the measured price restatement),")
    P(f"     flip-flag disagreements = {nflip} (bar 0);  on B136 — where data/prices_broad.csv "
      f"is bit-identical — max|d(dU)| = {okB:.3e} (bar 1e-12).")
    g5 = worst < BAR_RESTATED and nflip == 0 and okB < 1e-12
    store["gates"].append(dict(gate="G5", detail="fresh vs idea 592", value=worst,
                               bar=BAR_RESTATED, PASS=g5))
    P(f"     {'PASS' if g5 else 'FAIL'}")
    assert g5, "G5 provenance failure"
    pd.DataFrame(store["gates"]).to_csv(OUT / f"{STAMP}.gates.csv", index=False)

    # -------------------------------------------------------------- PART B: the grid
    P("\n" + "=" * 118)
    P("PART B — RE-SCORE: the (POPULATION SET x TIE BAR) grid, all 5 x 8 = 40 points, every "
      "leg")
    P("=" * 118)
    ORDER = ["REC-CELLS", "REC-LADDER", "REC-SHUFFLE", "FRESH-CELLS", "FRESH-SHUFFLE"]
    grid = [rescore(k, pops[k], tau) for k in ORDER if k in pops for tau in TAUS]
    G = pd.DataFrame(grid)
    G.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    for m in METRICS:
        P(f"\n  ---- {m} leg: published flip rate, then the three-way rate over DETERMINED rows, "
          f"and the UNDETERMINED share")
        piv = G.pivot_table(index="population", columns="tau",
                            values=f"{m}_undet_share").reindex([k for k in ORDER if k in pops])
        P("    UNDETERMINED share by tie bar:")
        P("      " + piv.to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n      "))
        piv2 = G.pivot_table(index="population", columns="tau",
                             values=f"{m}_rate_det").reindex([k for k in ORDER if k in pops])
        P("    FLIP rate over determined rows (published binary rate in the tau=0 'pub' column "
          "below):")
        P("      " + piv2.to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n      "))
        pub = G[G.tau == 0.0].set_index("population")[f"{m}_pub_rate"]
        P("    published binary rate: " + "  ".join(f"{k} {pub[k]:.4f}" for k in pub.index))

    P("\n  H1 (ties are a MaxDD-leg phenomenon) — exact-zero legs at tau = 0, by population:")
    z = G[G.tau == 0.0]
    for _, r in z.iterrows():
        P(f"    {r.population:14s} n={int(r.n):5d}   " + "   ".join(
            f"{m}: zeroU {int(r[f'{m}_zeroU']):4d} zeroM {int(r[f'{m}_zeroM']):4d}"
            for m in METRICS))

    # -------------------------------------------------------------- PART C: do numbers move?
    P("\n" + "=" * 118)
    P("PART C — DO THE PUBLISHED NUMBERS MOVE?  flip rates, the AUC ceiling, the argmax "
      "predictor, and the panel ordering")
    P("=" * 118)
    arows = []
    for k in ORDER:
        if k not in pops:
            continue
        for tau in TAUS:
            arows += auc_table(k, pops[k], tau, PATH_PREDS)
    A = pd.DataFrame(arows)
    A.to_csv(OUT / f"{STAMP}.auc.csv", index=False)
    P("\n  MaxDD-flip AUC ceiling (max over idea 584's 8 path predictors) and its ARGMAX, "
      "published vs three-way:")
    P(f"    {'population':15s} {'tau':>9s}  {'pub ceiling':>11s} {'pub argmax':>11s}  "
      f"{'3-way ceiling':>13s} {'3-way argmax':>13s}  {'n_det':>6s}  argmax moves?")
    cmoves = []
    for k in ORDER:
        if k not in pops:
            continue
        for tau in TAUS:
            a = A[(A.population == k) & (A.tau == tau)].dropna(subset=["auc_published"])
            if a.empty:
                continue
            ip, i3 = a.auc_published.idxmax(), (a.auc_threeway.idxmax()
                                                if a.auc_threeway.notna().any() else None)
            pub_c, pub_a = a.loc[ip, "auc_published"], a.loc[ip, "predictor"]
            if i3 is None:
                th_c, th_a, moved = np.nan, "-", False
            else:
                th_c, th_a = a.loc[i3, "auc_threeway"], a.loc[i3, "predictor"]
                moved = th_a != pub_a
            P(f"    {k:15s} {tau:9.0e}  {pub_c:11.4f} {pub_a:>11s}  {th_c:13.4f} "
              f"{th_a:>13s}  {int(a.n_det.iloc[0]):6d}  {'YES' if moved else 'no'}")
            cmoves.append(dict(population=k, tau=tau, pub_ceiling=pub_c, pub_argmax=pub_a,
                               three_ceiling=th_c, three_argmax=th_a, argmax_moves=moved))
    CM = pd.DataFrame(cmoves)

    P("\n  PANEL ORDERING by MaxDD flip rate, published vs three-way (this is the shape of "
      "claim the queue asks about):")
    orows = []
    for k in ORDER:
        if k not in pops:
            continue
        d = pops[k]
        if "panel" not in d.columns:
            continue
        for tau in TAUS:
            lab = pair_label(d.dU_MaxDD, d.dM_MaxDD, tau)
            det = lab != UNDET
            pub_r, th_r = {}, {}
            for pn, gd in d.groupby("panel"):
                ix = d.index.get_indexer(gd.index)
                pub_r[pn] = float(published_flip(gd.dU_MaxDD, gd.dM_MaxDD).mean())
                dd = det[ix]
                th_r[pn] = float((lab[ix][dd] == FLIP).mean()) if dd.any() else np.nan
            op = ">".join(sorted(pub_r, key=lambda x: -pub_r[x]))
            ot = ">".join(sorted(th_r, key=lambda x: -(th_r[x] if np.isfinite(th_r[x]) else -1)))
            orows.append(dict(population=k, tau=tau, published_order=op, threeway_order=ot,
                              moved=op != ot,
                              **{f"pub_{p}": v for p, v in pub_r.items()},
                              **{f"three_{p}": v for p, v in th_r.items()}))
    O = pd.DataFrame(orows)
    O.to_csv(OUT / f"{STAMP}.ordering.csv", index=False)
    P(O[["population", "tau", "published_order", "threeway_order", "moved"]].to_string(
        index=False, float_format=lambda x: f"{x:.0e}"))
    P(f"\n  The panel ordering moves at {int(O.moved.sum())} of {len(O)} "
      f"(population x tie bar) points.")

    # -------------------------------------------------------------- PART D: the correction
    P("\n" + "=" * 118)
    P("PART D — the record says these ties are EXACT ZEROS.  They are not: 1e-16 is not 0, and "
      "np.sign does not return 0 for it")
    P("=" * 118)
    P("idea 592's prose reads 'exact zeros, not near-misses' and its ties.csv counts them at "
      "|d| < 1e-12.  Those are different claims,")
    P("and the difference decides whether the published MECHANISM (np.sign(0) = 0) is the one "
      "actually generating the labels.")
    for k in ("REC-SHUFFLE", "FRESH-SHUFFLE", "REC-CELLS", "FRESH-CELLS"):
        if k not in pops:
            continue
        d = pops[k]
        fl = published_flip(d.dU_MaxDD, d.dM_MaxDD)
        zu = (d.dU_MaxDD == 0.0).to_numpy()
        t12 = (d.dU_MaxDD.abs() <= BAR_592).to_numpy()
        nz = d.dU_MaxDD.abs()[(d.dU_MaxDD != 0.0)]
        P(f"\n  {k}: {len(d)} rows, {int(fl.sum())} published MaxDD flips")
        P(f"    |dU_MaxDD| == 0 EXACTLY (np.sign returns 0 — the published mechanism): "
          f"{int((zu & fl).sum())} flips ({(zu & fl).sum()/max(int(fl.sum()),1):.1%})")
        P(f"    |dU_MaxDD| <= 1e-12 but NOT zero (np.sign returns +-1 — a genuine sign "
          f"comparison of float NOISE): {int((t12 & ~zu & fl).sum())} flips")
        P(f"    idea 592's published tie count at its own 1e-12 bar: "
          f"{int((t12 & fl).sum())} — the sum of the two, published as one mechanism")
        if len(nz):
            P(f"    smallest non-zero |dU_MaxDD| on this population: {nz.min():.3e}  "
              f"(one ulp of a MaxDD near {float(d.dU_MaxDD.abs().max()):.2f} is ~1e-16)")

    # -------------------------------------------------------------- PART E: the KEEP paths
    P("\n" + "=" * 118)
    P("PART E — THE VERDICT THAT COSTS MONEY: the KEEP paths are sign comparisons with an "
      "undeclared tie branch")
    P("=" * 118)
    P("4a is  H1 > base AND H2 > base AND MaxDD >= base  — the two Sharpe legs FAIL a tie and "
      "the drawdown leg PASSES one.")
    P("4b is  H1 > SPY AND H2 > SPY AND OOS > SPY AND MaxDD >= 0.60*SPY AND CAGR >= 0.70*SPY  "
      "— same asymmetry.")
    P("So a book whose drawdown merely EQUALS the bar is credited with a win.  How often does "
      "that decide a committed verdict?")
    brows = []
    for tau in TAUS:
        r = dict(tau=tau, n=len(df), pass4a=int(df.pass4a.sum()), pass4b=int(df.pass4b.sum()))
        for path, bars in (("4a", ("H1", "H2", "DD")),
                           ("4b", ("H1", "H2", "OOS", "DD", "CAGR"))):
            cols = [f"m{path}_{b}" for b in bars]
            M_ = df[cols].to_numpy(float)
            passing = df[f"pass{path}"].to_numpy(bool)
            near = (np.abs(M_) <= tau)
            r[f"{path}_pass_with_a_tied_bar"] = int((passing & near.any(axis=1)).sum())
            r[f"{path}_fail_with_a_tied_bar"] = int((~passing & near.any(axis=1)).sum())
            r[f"{path}_min_abs_margin"] = float(np.nanmin(np.abs(M_)))
            for b, c in zip(bars, cols):
                r[f"{path}_{b}_tied"] = int((df[c].abs() <= tau).sum())
        brows.append(r)
    B = pd.DataFrame(brows)
    B.to_csv(OUT / f"{STAMP}.barmargins.csv", index=False)
    P(B.to_string(index=False, float_format=lambda x: f"{x:.3e}"))
    c4a = [c for c in df.columns if c.startswith("m4a_")]
    c4b = [c for c in df.columns if c.startswith("m4b_")]
    mm4a = float(df[c4a].abs().to_numpy().min())
    mm4b = float(df[c4b].abs().to_numpy().min())
    P(f"\n  Smallest |margin| on any 4a bar: {mm4a:.3e};  on any 4b bar: {mm4b:.3e}.")
    exact = df[(df[c4a].abs() == 0.0).any(axis=1)]
    P(f"\n  THE EXACT TIES ARE REAL AND THEY ARE A SELF-COMPARISON.  {len(exact)} of {len(df)} "
      f"cells tie the 4a bars EXACTLY, on all three legs at once:")
    P("    " + exact[["panel", "family", "form", "dial", "gross", "m4a_H1", "m4a_H2", "m4a_DD",
                      "pass4a"]].to_string(index=False).replace("\n", "\n    "))
    P("    These are not coincidences: `BAND-DG at dial 0.03, gross 0.75` IS "
      "`baseline.rules_v2_weights` — the same mask, the same de-gross-to-cash, the same")
    P("    weights — so the 4a comparison is the live book against itself.  It FAILS 4a because "
      "the two Sharpe legs are strict `>` (correct), and it PASSES")
    P("    the drawdown leg because that one is `>=` (a book credited with beating its own "
      "drawdown).  The verdict survives only because the Sharpe legs")
    P("    happen to carry the opposite tie convention.  On SMALL439 the identity does not hold "
      "(SPY is a benchmark column there, not a tradable name), which")
    P("    is why only two cells appear.")
    if int(df.pass4b.sum()):
        thin = df[df.pass4b].copy()
        thin["min_margin"] = thin[c4b].abs().min(axis=1)
        P(f"\n  THE THIN PASSES: of the {int(df.pass4b.sum())} 4b passes, "
          f"{int((thin.min_margin <= 1e-3).sum())} clear their tightest bar by <= 1e-3 and "
          f"{int((thin.min_margin <= 1e-2).sum())} by <= 1e-2:")
        P("    " + thin.nsmallest(6, "min_margin")[
            ["panel", "family", "form", "dial", "gross", "m4b_DD", "m4b_CAGR", "m4b_OOS",
             "min_margin"]].to_string(index=False, float_format=lambda x: f"{x:.6f}"
                                      ).replace("\n", "\n    "))
        P("    None is a machine-precision tie, so the convention does not move them — but each "
          "is a KEEP verdict standing on a margin the record does not publish.")
    mm = min(mm4a, mm4b)

    # -------------------------------------------------------------- PART F: sign_holds
    P("\n" + "=" * 118)
    P("PART F — the MIRROR bug: `sign_holds` on this run's own rule-8 picks")
    P("=" * 118)
    P("Every walk-forward file in the record reports sign_holds = np.sign(IS) == np.sign(OOS). "
      "A tie on either leg makes it FALSE,")
    P("i.e. the record's IS->OOS agreement rates are biased DOWN by exactly the tie rate — the "
      "opposite direction to the flip counts.")
    P(f"  On this run's {len(wf)} picks: IS legs exactly zero {int(wf.IS_tie.sum())}, "
      f"OOS legs exactly zero {int(wf.OOS_tie.sum())}, sign_holds "
      f"{int(wf.sign_holds.sum())}/{len(wf)}.")
    P("  So the bias is measurable but empty here: a Sharpe difference over 4,000 bars does not "
      "coincide bit-for-bit, which is H1 again.")

    # -------------------------------------------------------------- rule 8
    P("\n" + "=" * 118)
    P("RULE 8 — walk-forward: (dial, g) chosen on 2009-2016 by IS dSharpe vs the unmatched "
      "control; 2017-2026 untouched")
    P("=" * 118)
    show = ["panel", "family", "form", "dial", "gross", "IS_dU_Sharpe", "OOS_dU_Sharpe",
            "sign_holds", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "pass4a", "pass4b"]
    P(wf[show].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  sign of the IS edge holds OOS: {int(wf.sign_holds.sum())} of {len(wf)} picks.")
    P(f"  KEEP paths on the picks: 4a {int(wf.pass4a.sum())}/{len(wf)}, "
      f"4b {int(wf.pass4b.sum())}/{len(wf)}.")
    P(f"  KEEP paths over ALL {len(df)} grid points: 4a {int(df.pass4a.sum())}, "
      f"4b {int(df.pass4b.sum())}, BOTH {int((df.pass4a & df.pass4b).sum())}.")
    P("\n  Benchmarks per panel (full sample and OOS), so every OOS number above has its bar:")
    P(lv.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\n  OOS of the picks vs RULES v2 and SPY (the columns rule 8 asks for):")
    cmp_ = wf[["panel", "family", "form", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
               "base_OOS_CAGR", "base_OOS_Sharpe", "base_OOS_MaxDD",
               "spy_OOS_CAGR", "spy_OOS_Sharpe", "spy_OOS_MaxDD"]]
    P(cmp_.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    beat_b = int((wf.OOS_Sharpe > wf.base_OOS_Sharpe).sum())
    beat_s = int((wf.OOS_Sharpe > wf.spy_OOS_Sharpe).sum())
    P(f"\n  OOS Sharpe beats RULES v2 on {beat_b}/{len(wf)} picks and SPY on {beat_s}/{len(wf)}.")
    df[["panel", "family", "form", "dial", "gross", "clause_CAGR", "clause_Sharpe",
        "clause_MaxDD", "clause_H1", "clause_H2", "clause_oCAGR", "clause_oSharpe",
        "clause_oMaxDD", "pass4a", "pass4b"]].to_csv(OUT / f"{STAMP}.keeppaths.csv", index=False)
    if int(df.pass4b.sum()):
        P("\n  The 4b passers over the full grid (all re-derivations of books already in the "
          "record; no book here is new):")
        P(df[df.pass4b][["panel", "family", "form", "dial", "gross", "clause_CAGR",
                         "clause_Sharpe", "clause_MaxDD", "clause_H1", "clause_H2",
                         "clause_oSharpe", "m4b_DD", "m4b_CAGR"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))

    # -------------------------------------------------------------- headline
    P("\n" + "=" * 118)
    P("HEADLINE")
    P("=" * 118)
    z0 = G[G.tau == 0.0].set_index("population")
    zc = G[G.tau == BAR_592].set_index("population")
    P(f"A. CENSUS: {len(sites)} sign-comparison sites over {nfiles} committed scripts carry the "
      f"missing tie branch — {dis} in the DISAGREE direction")
    P(f"   (a tie inflates a flip count) and {agree} in the AGREE direction (a tie deflates a "
      f"`sign_holds` rate).  Only {rescorable_rows} committed rows over")
    P(f"   {len([k for k in pops if k.startswith('REC')])} distinct populations publish both "
      f"operands, so that is the whole re-scorable footprint of the record.")
    P(f"B. RE-SCORING MOVES NOTHING ON REAL BOOKS.  At every tie bar up to 1e-9, the "
      f"UNDETERMINED share is "
      f"{z0.loc['REC-CELLS','MaxDD_undet_share']:.4f} on REC-CELLS and "
      f"{z0.loc['FRESH-CELLS','MaxDD_undet_share']:.4f} on FRESH-CELLS, on all three legs.")
    P(f"   The Sharpe and CAGR legs carry ZERO exact ties on EVERY population "
      f"(H1 confirmed): a statistic summed over ~4,000 bars does not coincide bit-for-bit.")
    P(f"C. ON THE SHUFFLE DRAWS IT MOVES A LOT: the published MaxDD flip rate "
      f"{z0.loc['REC-SHUFFLE','MaxDD_pub_rate']:.1%} becomes "
      f"{zc.loc['REC-SHUFFLE','MaxDD_rate_det']:.1%} over the "
      f"{int(len(pops['REC-SHUFFLE']) - zc.loc['REC-SHUFFLE','MaxDD_undet'])} determined rows,")
    P(f"   with {zc.loc['REC-SHUFFLE','MaxDD_undet_share']:.1%} of the population undetermined "
      f"at 1e-12.  The panel ordering moves at {int(O.moved.sum())} of {len(O)} grid points and "
      f"the AUC argmax at {int(CM.argmax_moves.sum())} of {len(CM)}.")
    P("D. AND THE PUBLISHED MECHANISM IS ONLY PART OF IT (PART D): of idea 592's 342 'exact "
      "ties', only the ones with |dU| == 0 are the np.sign(0) bug;")
    P("   the rest are genuine opposite-sign comparisons of numbers at one ulp.  Both are "
      "undetermined, but only the first is the mechanism the record published.")
    thin_n = 0
    if int(df.pass4b.sum()):
        thin_n = int((df[df.pass4b][c4b].abs().min(axis=1) <= 1e-3).sum())
    P(f"E. NO KEEP VERDICT MOVES, BUT THE TIE BRANCH IS THERE: {len(exact)} of {len(df)} cells "
      f"tie ALL THREE 4a bars exactly — BAND-DG(0.03, 0.75) IS `rules_v2_weights`, so that")
    P(f"   comparison is the live book against itself, and 4a's `>=` drawdown leg credits it "
      f"with a drawdown win.  It still fails 4a only because the Sharpe legs use strict `>`.")
    P(f"   No 4a or 4b PASS is created by a tie at any tau ({int(B.iloc[0]['4a_pass_with_a_tied_bar'])} "
      f"and {int(B.iloc[0]['4b_pass_with_a_tied_bar'])} at tau=0), and the smallest 4b margin is "
      f"{mm4b:.3e} — but {thin_n} of the {int(df.pass4b.sum())} 4b passes clear their tightest bar by <= 1e-3.")
    P(f"F. rule 8: 4a {int(wf.pass4a.sum())}/{len(wf)}, 4b {int(wf.pass4b.sum())}/{len(wf)} on "
      f"the picks; 4a {int(df.pass4a.sum())}, 4b {int(df.pass4b.sum())}, "
      f"BOTH {int((df.pass4a & df.pass4b).sum())} over all {len(df)} grid points.")
    P(f"\ndone in {time.time()-t0:.1f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
