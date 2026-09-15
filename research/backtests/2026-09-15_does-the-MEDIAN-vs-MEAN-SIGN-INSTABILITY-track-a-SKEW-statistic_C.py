#!/usr/bin/env python3
"""Idea 887 (lane C, 2026-09-15) - does the MEDIAN-vs-MEAN SIGN INSTABILITY track a SKEW
statistic the record could publish instead?

THE CLAIM UNDER TEST
--------------------
Idea 880 found that 7 of its 23 de-duplicated headline placebo claims (30.4%) - and 26 of its 151
cuts (17.2%) - carry a SIGNED MEDIAN and a SIGNED MEAN of OPPOSITE SIGN, so the sign of a number
the record would quote depends on a pooling rule no memo declares.  The queue's proposal: if that
disagreement is a deterministic function of the per-arm gap distribution's SHAPE (skew, excess
kurtosis, or the share of arms within one seed-SE of zero), then PROTOCOL can require ONE number
instead of a declared convention - publish the shape statistic and the other pooled value is
implied.

THE ALGEBRA THAT HAS TO BE STATED BEFORE ANY REGRESSION IS RUN
--------------------------------------------------------------
Write the per-arm gap vector s = ex_null - ex_BLOCK, and standardise by its own cross-arm sd:

    M    = median(s) / sd(s)          the standardised LOCATION
    LAM  = (mean(s) - median(s)) / sd(s)   the standardised MEDIAN-MEAN GAP
    mean(s)/sd(s) = M + LAM

Sign instability is, exactly,      median * mean < 0  <=>  M * (M + LAM) < 0
                                                      <=>  sign(M) != sign(LAM)  AND  |M| < |LAM|

So instability is a function of the PAIR (location, gap), and the ratio rho = M / LAM decides it
(unstable <=> -1 < rho < 0).  A SHAPE statistic - skew, kurtosis, near-zero mass - is scale-free
and location-free by construction, so it can at most deliver LAM.  It cannot deliver M.  That is
an identity, not a finding, and it is asserted as gate G2 below rather than discovered at the end.

What is therefore genuinely open, and what this run measures:

    Q1  is the GAP itself a shape fact?  i.e. does LAM track the moment skew g1 tightly enough
        (Pearson's mean-median relation predicts LAM ~ g1/3) that a run publishing a median and a
        skew has published its mean?
    Q2  can shape statistics ALONE classify which claims are unstable, out of fold?  (The algebra
        says they should not be able to; the queue's hypothesis says they should.  Measured.)
    Q3  if shape cannot replace the convention, is there ONE number that can?  The pre-registered
        rival is the sign-test |z| the signed estimator already produces: idea 880 observed all 7
        of its unstable headline claims at |z| <= 0.94.  If instability lives entirely below the
        resolvability bar, the PROTOCOL fix is not a shape statistic at all - it is "do not quote
        a sign you cannot resolve", which costs no new number.

TWO TUNED PARAMETERS (the queue's own)
--------------------------------------
    PARAM 1  SHAPE STATISTIC   feature set fed to the classifier / regression:
             SKEW | EXKURT | NEAR | SKEW+EXKURT | SKEW+EXKURT+NEAR | LAMBDA
             plus three declared NON-shape contrasts (|M|, SKEW+|M|, |Z|) which are NOT candidate
             answers to the queue's question - they are there to show what the shape sets are
             missing.
    PARAM 2  CLAIM SET         ALL (151 cuts) | HEADLINE (23, de-duplicated, idea 880's own) |
             HEADLINE_RAW (31, before de-duplication) | COST (the 3 cost rungs, 95) |
             WINDOW (the IS/OOS cuts, 56) | NEARABLE (the 72 cuts whose file committed seed sd)
    EVERY grid point is printed.  Nothing else is tuned; panel, null family, cost rung, window and
    file are reported axes.

PRE-REGISTERED BARS (fixed before any number was read)
------------------------------------------------------
    H_GAP     the standardised gap LAM is a skew fact: OLS LAM ~ a + b*g1 reaches R^2 >= 0.50 on
              ALL and on HEADLINE, and the fitted b brackets Pearson's 1/3 (b in [0.20, 0.47]).
    H_SHAPE   (the queue's hypothesis) shape statistics ALONE classify instability at
              leave-one-FILE-out balanced accuracy >= 0.80 at the best grid point.
    H_SIGN    knowing the median and the skew recovers the MEAN'S SIGN: >= 90% overall AND >= 75%
              on the unstable subset, using the parameter-free Pearson form mean_hat = med +
              sd*g1/3.
    H_UNRES   >= 95% of unstable cuts sit below the signed estimator's own resolvability bar
              (|sign-test z| < 2.0), i.e. instability is confined to claims that should carry no
              sign at all.
    H_WF      (rule 8a) the shape->gap law fitted on the IS-window cuts only holds out of sample:
              OOS-window sign-recovery within 10 pp of the in-sample rate.

GATES (must pass or the run is void)
------------------------------------
    G0  the 151 cuts and their SIGNED_MED / SIGNED_MEAN reproduce idea 880's committed claims.csv
        to < 1e-12 (this run recomputes from the raw per-arm CSVs, it does not read 880's numbers).
    G1  the de-duplication reproduces idea 880's committed 23-claim headline set exactly.
    G2  the identity  unstable <=> sign(M) != sign(LAM) and |M| < |LAM|  holds at 151 of 151.
    G3  the unstable flags reproduce idea 880's committed sign_unstable column exactly.

RULE 8
------
    (a) the shape->gap law is fitted on the IS-window cuts and read once on the OOS-window cuts.
    (b) a book leg is carried anyway - idea 880's declared grid and IS-only selector, verbatim, on
        U56 / B136 / SMALL - so both KEEP paths are evaluated against RULES v2 and SPY.  A census
        has no book of its own; this is the record's standing gate, not a tuned arm.

COSTS 10 bps, next-day execution, weekly cadence (PROTOCOL 2).  Deterministic; the census legs
read committed CSVs read-only and write nothing outside research/backtests.

Outputs: .cuts.csv (151 with shape stats) .grid.csv .regress.csv .walkforward.csv .books.csv
         .keep.csv .console.txt
"""
import sys, time
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
from baseline import load_universe, rules_v2_weights, score            # noqa: E402
from engine import backtest, metrics, rebalance_mask                   # noqa: E402

STEM = Path(__file__).name[:-3]
OUT = REPO / "research" / "backtests"
BT = OUT
LINES: list[str] = []

KEY = ["panel", "family", "q", "w", "depth", "cadence", "gross"]
REF = "BLOCK"
Z_BAR = 2.0                 # |sign-test z| at which a signed reading is resolvable (880's bar)
NSEED = 20                  # every seed-sd-bearing corpus file's budget (880 fn. 4)
GAP_R2_BAR, SHAPE_ACC_BAR = 0.50, 0.80
SIGN_BAR, SIGN_UNSTABLE_BAR, UNRES_BAR, WF_TOL = 0.90, 0.75, 0.95, 0.10
PEARSON = 1.0 / 3.0         # mean - median ~ sd * skew / 3

# rule 8 (b): idea 880's declared book grid, verbatim
FREQ, MAX_VOL, SMOOTH = "W", 0.60, 20
QS, WS = [0.07, 0.12, 0.17], [252, 1008]
DEPTHS, CADENCES, GROSSES = [0.50, 1.00], ["D", "W"], [0.75, 1.00]
STATES = ["BREADTH", "VOL20", "DISP", "CORR"]
SIDES = {"BREADTH": ("LO", "HI"), "VOL20": ("HI", "LO"), "DISP": ("HI", "LO"), "CORR": ("HI", "LO")}
SPLIT = "2017-01-01"

REF880 = "2026-09-15_how-many-committed-PLACEBO-DIFFERENCED-numbers-would-CHANGE-SIGN-under-the-SIGNED-estimator_cloud"


def log(s=""):
    print(s, flush=True)
    LINES.append(str(s))


# ============================================================ the corpus (structure, not a list)
def find_corpus():
    """Same structural test idea 880 used: a committed CSV is re-priceable iff it holds per-arm
    excess for a null AND its BLOCK reference on the same arm keys."""
    out = []
    for f in sorted(BT.glob("*.csv")):
        try:
            head = pd.read_csv(f, nrows=0)
        except Exception:
            continue
        cols = list(head.columns)
        if "kind" not in cols or not set(KEY).issubset(cols):
            continue
        excols = [c for c in cols if c.startswith("excess")]
        if not excols:
            continue
        df = pd.read_csv(f)
        if REF not in set(df["kind"].unique()):
            continue
        sdcols = [c for c in cols if c.startswith("seedsd")]
        out.append((f.name, df, excols, sdcols))
    return out


def cut_label(excol):
    return excol.replace("excess_", "").replace("excess", "10bps") or "10bps"


def shape_stats(s, se_arm):
    """Every statistic this run tests, computed on ONE cut's per-arm gap vector.

    s       per-arm signed gap  ex_null - ex_BLOCK   (each already a median over that run's seeds)
    se_arm  per-arm SEED standard error of that gap, or None if the file committed no dispersion
    """
    v = s.values.astype(float)
    n = len(v)
    med, mean = float(np.median(v)), float(v.mean())
    sd = float(v.std(ddof=1))
    # Fisher g1 / g2, sample-adjusted (same convention pandas uses), guarded at tiny sd
    if sd > 0 and n > 3:
        z = (v - mean) / sd
        m3, m4 = float((z ** 3).mean()), float((z ** 4).mean())
        g1 = m3 * np.sqrt(n * (n - 1)) / (n - 2)
        g2 = ((n - 1) / ((n - 2) * (n - 3))) * ((n + 1) * (m4 - 3) + 6)
    else:
        g1 = g2 = np.nan
    lam = (mean - med) / sd if sd > 0 else np.nan
    m_loc = med / sd if sd > 0 else np.nan
    near = float((np.abs(v) <= se_arm.values).mean()) if se_arm is not None else np.nan
    # sign test, ties excluded (880's fix: an exact-zero null must not be crowned most resolvable)
    nz = v[v != 0]
    if len(nz) == 0:
        below, zsign = np.nan, np.nan
    else:
        below = float((nz < 0).mean())
        zsign = (below - 0.5) / np.sqrt(0.25 / len(nz))
    return dict(n=n, n_ties=n - len(nz), SIGNED_MED=med, SIGNED_MEAN=mean, SD=sd,
                SKEW=g1, EXKURT=g2, LAMBDA=lam, M_LOC=m_loc, NEAR=near, sign_z=zsign,
                share_below=below,
                unstable=bool(med * mean < 0),
                resolvable=(abs(zsign) >= Z_BAR) if zsign == zsign else False)


def build_cuts():
    rows, vecs = [], {}
    for fname, df, excols, sdcols in find_corpus():
        for ex in excols:
            sd_of = {c.replace("seedsd", "excess"): c for c in sdcols}.get(ex)
            piv = df.pivot_table(index=KEY, columns="kind", values=ex)
            if REF not in piv.columns:
                continue
            sdp = df.pivot_table(index=KEY, columns="kind", values=sd_of) if sd_of else None
            for kind in [k for k in piv.columns if k != REF]:
                s = (piv[kind] - piv[REF]).dropna()
                if len(s) < 30:
                    continue
                se = None
                if sdp is not None and kind in sdp.columns and REF in sdp.columns:
                    se = (np.sqrt(sdp[kind] ** 2 + sdp[REF] ** 2) / np.sqrt(NSEED)).reindex(s.index)
                    if se.isna().any():
                        se = None
                r = dict(file=fname, cut=cut_label(ex), kind=kind)
                r.update(shape_stats(s, se))
                rows.append(r)
                vecs[(fname, cut_label(ex), kind)] = s
    return pd.DataFrame(rows), vecs


def dedup_headline(cuts, vecs):
    """Idea 880's finding: four committed files publish BIT-IDENTICAL null columns, so the
    headline rung double-counts.  Recomputed here from the raw vectors, then gated against 880."""
    head = cuts[cuts["cut"] == "10bps"].copy().reset_index(drop=True)
    dup = np.zeros(len(head), bool)
    for i in range(len(head)):
        if dup[i]:
            continue
        a = vecs[(head.at[i, "file"], "10bps", head.at[i, "kind"])]
        for j in range(i + 1, len(head)):
            if dup[j] or head.at[j, "kind"] != head.at[i, "kind"]:
                continue
            b = vecs[(head.at[j, "file"], "10bps", head.at[j, "kind"])]
            sh = a.index.intersection(b.index)
            if len(sh) >= 30 and float((a.loc[sh] - b.loc[sh]).abs().max()) == 0.0:
                dup[j] = True
    head["dup"] = dup
    return head


# ================================================================== regression / classification
def ols_r2(x, y):
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 5 or x.std() == 0:
        return np.nan, np.nan, np.nan, len(x)
    A = np.column_stack([np.ones(len(x)), x])
    beta = np.linalg.lstsq(A, y, rcond=None)[0]
    resid = y - A @ beta
    ss = ((y - y.mean()) ** 2).sum()
    return (1 - (resid ** 2).sum() / ss if ss > 0 else np.nan), float(beta[1]), float(beta[0]), len(x)


def logit_fit(X, y, ridge=1e-4, iters=60):
    """Plain IRLS logistic regression, ridge-stabilised.  Deterministic, no sklearn."""
    X = np.column_stack([np.ones(len(X)), X])
    b = np.zeros(X.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-np.clip(X @ b, -30, 30)))
        W = np.clip(p * (1 - p), 1e-6, None)
        H = X.T @ (X * W[:, None]) + ridge * np.eye(X.shape[1])
        g = X.T @ (y - p) - ridge * b
        step = np.linalg.solve(H, g)
        b = b + step
        if np.max(np.abs(step)) < 1e-9:
            break
    return b


def logit_p(b, X):
    X = np.column_stack([np.ones(len(X)), X])
    return 1 / (1 + np.exp(-np.clip(X @ b, -30, 30)))


def bal_acc(y, p, thr=0.5):
    pred = p >= thr
    pos, neg = y == 1, y == 0
    if pos.sum() == 0 or neg.sum() == 0:
        return np.nan
    return 0.5 * (pred[pos].mean() + (~pred[neg]).mean())


def auc(y, p):
    pos, neg = p[y == 1], p[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return np.nan
    r = pd.Series(np.concatenate([pos, neg])).rank().values
    return float((r[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))


def best_thr(y, p):
    """Threshold maximising balanced accuracy - only ever fitted on a TRAINING fold."""
    cand = np.unique(np.concatenate([p, [0.0, 1.0]]))
    sc = [bal_acc(y, p, t) for t in cand]
    return float(cand[int(np.nanargmax(sc))]) if np.any(np.isfinite(sc)) else 0.5


def lofo(cs, feats):
    """Leave-one-FILE-out: the only honest fold here, because cuts inside one file share arms.

    bal_acc      at the fixed 0.5 cut-off - the pre-registered bar for H_SHAPE.
    bal_acc_trthr at a cut-off chosen on the TRAINING fold only.  Reported because the classes are
                 imbalanced (17-30% positive), so a 0.5 cut-off collapses a weak-but-real signal to
                 the all-negative rule's 0.5000.  It is an extra column, not a moved bar.
    """
    d = cs.dropna(subset=feats + ["unstable"]).copy()
    y = d["unstable"].astype(int).values
    if len(d) < 10 or y.sum() == 0 or y.sum() == len(y):
        return dict(n=len(d), n_unstable=int(y.sum()), bal_acc=np.nan, bal_acc_trthr=np.nan,
                    auc=np.nan, insample=np.nan)
    P, T = np.full(len(d), np.nan), np.full(len(d), 0.5)
    for f in d["file"].unique():
        te = (d["file"] == f).values
        tr = ~te
        if y[tr].sum() == 0 or y[tr].sum() == tr.sum():
            P[te] = y[tr].mean() if tr.sum() else 0.5      # degenerate fold -> base rate, no info
            continue
        Xtr = d.loc[tr, feats].values
        mu, sg = Xtr.mean(0), np.where(Xtr.std(0) > 0, Xtr.std(0), 1.0)
        b = logit_fit((Xtr - mu) / sg, y[tr])
        P[te] = logit_p(b, (d.loc[te, feats].values - mu) / sg)
        T[te] = best_thr(y[tr], logit_p(b, (Xtr - mu) / sg))
    X = d[feats].values
    mu, sg = X.mean(0), np.where(X.std(0) > 0, X.std(0), 1.0)
    bin_ = logit_fit((X - mu) / sg, y)
    return dict(n=len(d), n_unstable=int(y.sum()), bal_acc=bal_acc(y, P),
                bal_acc_trthr=bal_acc(y, (P >= T).astype(float), 0.5), auc=auc(y, P),
                insample=bal_acc(y, logit_p(bin_, (X - mu) / sg)))


# =========================================================== rule 8 (b): idea 880's book grid
def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def ewall_weights(px, gross):
    e = eligible_mask(px).astype(float)
    return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).mul(gross).fillna(0.0)


def fast_sharpe(v):
    v = np.asarray(v, float)
    sd = v.std(ddof=1)
    return v.mean() * 252 / (sd * np.sqrt(252)) if sd > 0 else np.nan


def state_breadth(px):
    a = px > px.rolling(200).mean()
    return a.sum(axis=1) / a.notna().sum(axis=1).replace(0, np.nan)


def state_vol20(px):
    return (px.pct_change().rolling(SMOOTH).std() * np.sqrt(252)).mean(axis=1)


def state_disp(px):
    return px.pct_change().std(axis=1).rolling(SMOOTH).mean()


def state_corr(px):
    rt = px.pct_change()
    sig = rt.rolling(SMOOTH).std()
    s_idx = rt.mean(axis=1).rolling(SMOOTH).std()
    n = sig.notna().sum(axis=1).replace(0, np.nan)
    sbar, s2bar = sig.mean(axis=1), (sig ** 2).mean(axis=1)
    return ((s_idx ** 2 - s2bar / n) / (sbar ** 2 - s2bar / n).replace(0, np.nan)).clip(-1, 1)


STATE_FN = {"BREADTH": state_breadth, "VOL20": state_vol20, "DISP": state_disp, "CORR": state_corr}


def gate_mult(st, thr, side, depth, cadence, idx):
    fire = ((st < thr) if side == "LO" else (st > thr)) & st.notna() & thr.notna()
    m = pd.Series(1.0, index=idx).where(~fire, 1.0 - depth)
    if cadence == "W":
        m = m.where(rebalance_mask(idx, FREQ)).ffill().fillna(1.0)
    return m


def apply_eff(r_base, m_eff, gross, cost_bps):
    switch = np.abs(np.diff(m_eff, prepend=m_eff[0]))
    return m_eff * r_base - switch * gross * cost_bps / 1e4


def pack(r):
    m = metrics(r if isinstance(r, pd.Series) else pd.Series(r))
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def halves(r):
    h = len(r) // 2
    return fast_sharpe(r[:h]), fast_sharpe(r[h:])


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    log(f"  SMALL panel: {px.shape[1]} columns -> {len(keep)} kept "
        f"({px.shape[1] - len(keep)} dropped for max_1d_move >= 1.0)")
    return px[keep]


def book_panel(name, px):
    idx = px.index
    core = px.drop(columns=["SPY"], errors="ignore")
    spy = px["SPY"].pct_change().fillna(0.0)
    states = {s: STATE_FN[s](core) for s in STATES}
    base = {g: backtest(core, ewall_weights(core, g), cost_bps=10, freq=FREQ)["returns"]
            for g in GROSSES}
    ii = idx[idx >= idx[260]]
    oos = np.asarray(ii >= pd.Timestamp(SPLIT))
    RB = {g: v.loc[ii].values for g, v in base.items()}

    spy_v = spy.loc[ii].values
    b = dict(panel=name)
    b["spy_cagr"], b["spy_sh"], b["spy_dd"] = pack(pd.Series(spy_v, index=ii))
    b["spy_h1"], b["spy_h2"] = halves(spy_v)
    b["spy_oos_c"], b["spy_oos_s"], b["spy_oos_d"] = pack(pd.Series(spy_v[oos], index=ii[oos]))
    bl = backtest(core, rules_v2_weights(core), cost_bps=10, freq=FREQ)["returns"].loc[ii]
    b["bl_cagr"], b["bl_sh"], b["bl_dd"] = pack(bl)
    b["bl_h1"], b["bl_h2"] = halves(bl.values)
    b["bl_oos_c"], b["bl_oos_s"], b["bl_oos_d"] = pack(bl.loc[ii[oos]])

    rows = []
    for st_name in STATES:
        st_full = states[st_name]
        for side in SIDES[st_name]:
            for q, w in product(QS, WS):
                thr = st_full.rolling(w, min_periods=max(60, w // 4)).quantile(
                    q if side == "LO" else 1 - q)
                for depth, cad in product(DEPTHS, CADENCES):
                    me = gate_mult(st_full, thr, side, depth, cad, idx
                                   ).shift(1).fillna(1.0).loc[ii].values
                    for g in GROSSES:
                        rr = apply_eff(RB[g], me, g, 10)
                        c_, s_, d_ = pack(pd.Series(rr, index=ii))
                        h1, h2 = halves(rr)
                        oc, os_, od = pack(pd.Series(rr[oos], index=ii[oos]))
                        rows.append(dict(panel=name, family=f"{st_name}-{side}", q=q, w=w,
                                         depth=depth, cadence=cad, gross=g, CAGR=c_, Sharpe=s_,
                                         MaxDD=d_, H1=h1, H2=h2, IS_Sharpe=fast_sharpe(rr[~oos]),
                                         OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od))
    return pd.DataFrame(rows), b


# ==================================================================================== main
def main():
    t0 = time.time()
    log("=" * 100)
    log("IDEA 887 - does the MEDIAN-vs-MEAN SIGN INSTABILITY track a SKEW statistic the record")
    log("           could publish instead?   (lane C, 2026-09-15)")
    log("=" * 100)
    log("PARAM 1 shape statistic {SKEW, EXKURT, NEAR, SKEW+EXKURT, SKEW+EXKURT+NEAR, LAMBDA};")
    log("PARAM 2 claim set {ALL, HEADLINE, HEADLINE_RAW, COST, WINDOW, NEARABLE}. All printed.")
    log("Non-shape contrasts (|M_LOC|, SKEW+|M_LOC|, |z|) are reported but are NOT answers to the")
    log("queue's question - they exist to price what the shape sets are missing.")
    log("Bars fixed before any number was read: H_GAP R2>=0.50 & b in [0.20,0.47]; H_SHAPE LOFO")
    log(f"balanced accuracy >= {SHAPE_ACC_BAR}; H_SIGN >= {SIGN_BAR:.0%} overall and "
        f">= {SIGN_UNSTABLE_BAR:.0%} on the unstable subset; H_UNRES >= {UNRES_BAR:.0%}; "
        f"H_WF within {WF_TOL:.0%}.")

    # ------------------------------------------------------------------ 1. corpus + shape stats
    log("\n" + "-" * 100)
    log("1. THE CUTS - recomputed from the raw per-arm CSVs, with the shape statistics attached")
    log("-" * 100)
    cuts, vecs = build_cuts()
    log(f"  re-priceable files: {cuts['file'].nunique()}   cuts: {len(cuts)}")
    log("\n  cuts per file x window:")
    log(pd.crosstab(cuts["file"].str[11:44], cuts["cut"]).to_string())

    # ---------------------------------------------------------------------------- 2. the gates
    log("\n" + "-" * 100)
    log("2. GATES")
    log("-" * 100)
    ref = pd.read_csv(BT / f"{REF880}.claims.csv")
    j = cuts.merge(ref[["file", "cut", "kind", "SIGNED_MED", "SIGNED_MEAN", "sign_z",
                        "sign_unstable", "n"]],
                   on=["file", "cut", "kind"], suffixes=("", "_880"))
    g0_n = len(j) == len(cuts) == len(ref)
    g0_v = float(np.nanmax(np.abs(
        np.c_[j.SIGNED_MED - j.SIGNED_MED_880, j.SIGNED_MEAN - j.SIGNED_MEAN_880,
              j.sign_z.fillna(0) - j.sign_z_880.fillna(0), j.n - j.n_880])))
    log(f"  G0 reproduce idea 880's 151 cuts: rows {len(cuts)} vs {len(ref)} "
        f"({'match' if g0_n else 'MISMATCH'}); max |diff| over MED/MEAN/z/n = {g0_v:.3e} "
        f"-> {'PASS' if g0_n and g0_v < 1e-12 else 'FAIL'}")

    head_raw = dedup_headline(cuts, vecs)
    head = head_raw[~head_raw["dup"]].reset_index(drop=True)
    ref_h = pd.read_csv(BT / f"{REF880}.headline.csv")
    mine = set(zip(head.file, head.kind))
    theirs = set(zip(ref_h.file, ref_h.kind))
    g1 = (mine == theirs)
    log(f"  G1 de-duplicated headline set: mine {len(head)} of {len(head_raw)}, "
        f"880's {len(ref_h)}; identical sets -> {'PASS' if g1 else 'FAIL'}")

    ident = ((np.sign(cuts.M_LOC) != np.sign(cuts.LAMBDA)) &
             (cuts.M_LOC.abs() < cuts.LAMBDA.abs()))
    g2_n = int((ident == cuts.unstable).sum())
    log(f"  G2 identity  unstable <=> sign(M)!=sign(LAM) and |M|<|LAM| : {g2_n} of {len(cuts)} "
        f"-> {'PASS' if g2_n == len(cuts) else 'FAIL'}")

    g3_n = int((j.unstable == j.sign_unstable).sum())
    log(f"  G3 unstable flags vs idea 880's committed column: {g3_n} of {len(j)} "
        f"-> {'PASS' if g3_n == len(j) else 'FAIL'}")
    gates_ok = g0_n and g0_v < 1e-12 and g1 and g2_n == len(cuts) and g3_n == len(j)
    log(f"  GATES: {'4 of 4 PASS' if gates_ok else 'FAILED - read nothing below'}")

    cuts["headline"] = False
    cuts.loc[cuts.set_index(["file", "cut", "kind"]).index.isin(
        [(f, "10bps", k) for f, k in mine]), "headline"] = True

    SETS = {
        "ALL": cuts,
        "HEADLINE": cuts[cuts.headline],
        "HEADLINE_RAW": cuts[cuts.cut == "10bps"],
        "COST": cuts[cuts.cut.isin(["0bps", "10bps", "25bps", "strip"])],
        "WINDOW": cuts[cuts.cut.isin(["IS", "OOS"])],
        "NEARABLE": cuts[cuts.NEAR.notna()],
    }
    nosh = cuts[cuts.SKEW.isna()]
    log(f"\n  cuts carrying NO shape statistic at all: {len(nosh)} of {len(cuts)} "
        f"(cross-arm sd = 0, so skew/kurtosis/LAMBDA are undefined) -")
    log("  " + "; ".join(f"{r.file[11:40]}|{r.cut}|{r.kind}" for _, r in nosh.iterrows()))
    log("  These are the exactly-zero nulls (idea 882's OP_REAL is BLOCK by construction). They")
    log("  are DROPPED from every regression below, which is why n reads 146 not 151. They are")
    log("  kept in the instability counts, where they read stable (median = mean = 0).")
    log("\n  claim sets (PARAM 2) and their instability base rates:")
    for nm, cs in SETS.items():
        log(f"    {nm:<13} n={len(cs):>4}  unstable {int(cs.unstable.sum()):>3} "
            f"({cs.unstable.mean():.1%})  NEAR computable on {int(cs.NEAR.notna().sum())}")

    # ------------------------------------------------------- 3. Q1  is the GAP a shape fact?
    log("\n" + "-" * 100)
    log("3. Q1 - IS THE STANDARDISED MEDIAN-MEAN GAP A SHAPE FACT?   LAM ~ a + b*<stat>")
    log("-" * 100)
    reg = []
    for nm, cs in SETS.items():
        for stat in ["SKEW", "EXKURT", "NEAR"]:
            r2, b, a, n = ols_r2(cs[stat].values, cs["LAMBDA"].values)
            reg.append(dict(claim_set=nm, stat=stat, n=n, R2=r2, slope=b, intercept=a))
    reg = pd.DataFrame(reg)
    log(reg.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    r_all = reg[(reg.claim_set == "ALL") & (reg.stat == "SKEW")].iloc[0]
    r_hd = reg[(reg.claim_set == "HEADLINE") & (reg.stat == "SKEW")].iloc[0]
    h_gap = (r_all.R2 >= GAP_R2_BAR and r_hd.R2 >= GAP_R2_BAR
             and 0.20 <= r_all.slope <= 0.47 and 0.20 <= r_hd.slope <= 0.47)
    log(f"\n  Pearson's relation predicts slope {PEARSON:.4f}.  Measured ALL {r_all.slope:.4f} "
        f"(R2 {r_all.R2:.4f}), HEADLINE {r_hd.slope:.4f} (R2 {r_hd.R2:.4f})")
    log(f"  H_GAP (R2 >= {GAP_R2_BAR} on ALL and HEADLINE, slope in [0.20, 0.47]): "
        f"{'CONFIRMED' if h_gap else 'REFUTED'}")

    # ------------------------------------ 4. Q2  can SHAPE ALONE classify the instability?
    log("\n" + "-" * 100)
    log("4. Q2 - CAN SHAPE STATISTICS ALONE CLASSIFY THE INSTABILITY?  (leave-one-FILE-out)")
    log("-" * 100)
    FEATS = {
        "SKEW": (["SKEW"], "shape"),
        "EXKURT": (["EXKURT"], "shape"),
        "NEAR": (["NEAR"], "shape"),
        "SKEW+EXKURT": (["SKEW", "EXKURT"], "shape"),
        "SKEW+EXKURT+NEAR": (["SKEW", "EXKURT", "NEAR"], "shape"),
        "LAMBDA": (["LAMBDA"], "shape"),
        "|M_LOC|": (["ABS_M"], "location (NOT a shape statistic)"),
        "SKEW+|M_LOC|": (["SKEW", "ABS_M"], "mixed (NOT a shape statistic)"),
        "|z|": (["ABS_Z"], "the signed estimator's own bar (NOT a shape statistic)"),
    }
    cuts["ABS_M"] = cuts["M_LOC"].abs()
    cuts["ABS_Z"] = cuts["sign_z"].abs()
    for nm in SETS:
        SETS[nm] = cuts.loc[SETS[nm].index]
    grid = []
    for (fname, (feats, cls)), (sname, cs) in product(FEATS.items(), SETS.items()):
        r = lofo(cs, feats)
        grid.append(dict(shape_stat=fname, kind=cls, claim_set=sname, **r))
    grid = pd.DataFrame(grid)
    log(grid.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    shape_grid = grid[(grid.kind == "shape") & grid.bal_acc.notna()]
    best_shape = shape_grid.loc[shape_grid.bal_acc.idxmax()] if len(shape_grid) else None
    h_shape = bool(best_shape is not None and best_shape.bal_acc >= SHAPE_ACC_BAR)
    log(f"\n  best SHAPE-only grid point: {best_shape.shape_stat} on {best_shape.claim_set}, "
        f"LOFO balanced accuracy {best_shape.bal_acc:.4f} (AUC {best_shape.auc:.4f}, "
        f"in-sample {best_shape.insample:.4f})")
    nonshape = grid[(grid.kind != "shape") & grid.bal_acc.notna()]
    bn = nonshape.loc[nonshape.bal_acc.idxmax()]
    log(f"  best NON-shape contrast:     {bn.shape_stat} on {bn.claim_set}, "
        f"LOFO balanced accuracy {bn.bal_acc:.4f} (AUC {bn.auc:.4f})")
    log(f"  H_SHAPE (shape alone >= {SHAPE_ACC_BAR} LOFO balanced accuracy): "
        f"{'CONFIRMED' if h_shape else 'REFUTED'}")

    # --------------------------------- 5. Q1b  does skew RECOVER the mean's sign from the median?
    log("\n" + "-" * 100)
    log("5. THE PRACTICAL FORM OF THE QUEUE'S PROPOSAL - does (median, sd, skew) recover the")
    log("   MEAN'S SIGN, so that one pooled number plus a shape statistic replaces the convention?")
    log("-" * 100)
    rec = []
    for nm, cs in SETS.items():
        d = cs.dropna(subset=["SKEW", "SD", "SIGNED_MED", "SIGNED_MEAN"])
        hat_p = d.SIGNED_MED + d.SD * d.SKEW * PEARSON
        r2, b, a, _ = ols_r2(d.SKEW.values, d.LAMBDA.values)
        hat_f = d.SIGNED_MED + d.SD * (a + b * d.SKEW)
        for lab, hat in (("PEARSON_1/3", hat_p), ("FITTED", hat_f)):
            ok = np.sign(hat) == np.sign(d.SIGNED_MEAN)
            u = d.unstable.values
            rec.append(dict(claim_set=nm, form=lab, n=len(d), sign_recovery=float(ok.mean()),
                            n_unstable=int(u.sum()),
                            sign_recovery_unstable=float(ok[u].mean()) if u.sum() else np.nan,
                            sign_recovery_stable=float(ok[~u].mean()) if (~u).sum() else np.nan))
    rec = pd.DataFrame(rec)
    log(rec.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    pa = rec[(rec.claim_set == "ALL") & (rec.form == "PEARSON_1/3")].iloc[0]
    h_sign = bool(pa.sign_recovery >= SIGN_BAR and pa.sign_recovery_unstable >= SIGN_UNSTABLE_BAR)
    log(f"\n  H_SIGN (PEARSON form on ALL: >= {SIGN_BAR:.0%} overall AND "
        f">= {SIGN_UNSTABLE_BAR:.0%} on the unstable subset): measured "
        f"{pa.sign_recovery:.1%} / {pa.sign_recovery_unstable:.1%} -> "
        f"{'CONFIRMED' if h_sign else 'REFUTED'}")

    # --------------------------------------- 6. Q3  the rival one number: the estimator's own |z|
    log("\n" + "-" * 100)
    log("6. Q3 - THE RIVAL ONE NUMBER: DOES INSTABILITY LIVE ENTIRELY BELOW THE RESOLVABILITY BAR?")
    log("-" * 100)
    unres = []
    for nm, cs in SETS.items():
        u = cs[cs.unstable]
        unres.append(dict(claim_set=nm, n=len(cs), n_unstable=len(u),
                          max_abs_z=float(u.sign_z.abs().max()) if len(u) else np.nan,
                          share_below_bar=float((u.sign_z.abs() < Z_BAR).mean()) if len(u) else np.nan,
                          unstable_rate_unresolvable=float(
                              cs.loc[~cs.resolvable, "unstable"].mean()) if (~cs.resolvable).any() else np.nan,
                          unstable_rate_resolvable=float(
                              cs.loc[cs.resolvable, "unstable"].mean()) if cs.resolvable.any() else np.nan))
    unres = pd.DataFrame(unres)
    log(unres.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    ua = unres[unres.claim_set == "ALL"].iloc[0]
    h_unres = bool(ua.share_below_bar >= UNRES_BAR)
    log(f"\n  H_UNRES (>= {UNRES_BAR:.0%} of unstable cuts sit below |z| = {Z_BAR}): "
        f"{ua.share_below_bar:.1%}, max |z| among unstable = {ua.max_abs_z:.4f} -> "
        f"{'CONFIRMED' if h_unres else 'REFUTED'}")
    log(f"  instability rate among UNRESOLVABLE cuts {ua.unstable_rate_unresolvable:.1%} vs "
        f"among RESOLVABLE cuts {ua.unstable_rate_resolvable:.1%}")
    log("\n  WHAT THE RIVAL RULE WOULD COST - a declared 'quote no sign below |z| = 2' strips the")
    log("  sign from every unresolvable cut, not just the unstable ones:")
    cost = pd.DataFrame([dict(claim_set=nm, n=len(cs),
                              n_unresolvable=int((~cs.resolvable).sum()),
                              share_stripped=float((~cs.resolvable).mean()),
                              unstable_left=int((cs.unstable & cs.resolvable).sum()))
                         for nm, cs in SETS.items()])
    log(cost.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    log("\n  every unstable cut, with its shape statistics (the queue's 7 headline claims are the")
    log("  subset with headline=True):")
    cols = ["file", "cut", "kind", "headline", "SIGNED_MED", "SIGNED_MEAN", "sign_z", "SKEW",
            "EXKURT", "NEAR", "LAMBDA", "M_LOC"]
    uu = cuts[cuts.unstable].copy()
    uu["file"] = uu["file"].str[11:40]
    log(uu[cols].to_string(index=False, float_format=lambda x: f"{x:.5f}"))

    # ----------------------------------------------------------- 7. rule 8 (a): walk-forward
    log("\n" + "-" * 100)
    log("7. RULE 8 (a) - the shape->gap law fitted on the IS-window cuts, read once on OOS")
    log("-" * 100)
    is_c, oos_c = cuts[cuts.cut == "IS"], cuts[cuts.cut == "OOS"]
    r2i, bi, ai, ni = ols_r2(is_c.SKEW.values, is_c.LAMBDA.values)
    r2o, bo, ao, no = ols_r2(oos_c.SKEW.values, oos_c.LAMBDA.values)
    wf = []
    for nm, cs in (("IS(fit)", is_c), ("OOS(read once)", oos_c)):
        d = cs.dropna(subset=["SKEW", "SD"])
        hat = d.SIGNED_MED + d.SD * (ai + bi * d.SKEW)          # IS-fitted coefficients only
        ok = np.sign(hat) == np.sign(d.SIGNED_MEAN)
        u = d.unstable.values
        wf.append(dict(window=nm, n=len(d), R2_own=r2i if nm.startswith("IS") else r2o,
                       slope_own=bi if nm.startswith("IS") else bo,
                       sign_recovery_ISfit=float(ok.mean()), n_unstable=int(u.sum()),
                       sign_recovery_unstable=float(ok[u].mean()) if u.sum() else np.nan,
                       unstable_rate=float(u.mean())))
    wf = pd.DataFrame(wf)
    log(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    gapwf = abs(wf.sign_recovery_ISfit.iloc[0] - wf.sign_recovery_ISfit.iloc[1])
    h_wf = bool(gapwf <= WF_TOL)
    log(f"  IS-fitted law: LAM = {ai:+.4f} {bi:+.4f}*SKEW (R2 {r2i:.4f}); OOS own fit slope "
        f"{bo:+.4f} (R2 {r2o:.4f})")
    log(f"  H_WF (OOS sign-recovery within {WF_TOL:.0%} of IS): |{wf.sign_recovery_ISfit.iloc[0]:.1%}"
        f" - {wf.sign_recovery_ISfit.iloc[1]:.1%}| = {gapwf:.1%} -> "
        f"{'CONFIRMED' if h_wf else 'REFUTED'}")

    # ---------------------------------------------------------- 8. rule 8 (b): the books
    log("\n" + "-" * 100)
    log("8. RULE 8 (b) - THE BOOKS, BOTH KEEP PATHS (10 bps, next-day, weekly). Idea 880's")
    log("   declared grid and IS-only selector, verbatim.  A census has no book of its own.")
    log("-" * 100)
    panels = [("U56", load_universe()), ("B136", load_universe(broad=True)), ("SMALL", small_panel())]
    books, keeps = [], []
    for nm, px in panels:
        bk, b = book_panel(nm, px)
        books.append(bk)
        pick = bk.loc[bk.IS_Sharpe.idxmax()]
        # 4a: Sharpe > RULES v2 in BOTH halves and MaxDD no worse.  4b: Sharpe > SPY in both
        # halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's.
        def verdicts(r):
            a = (r.H1 > b["bl_h1"] and r.H2 > b["bl_h2"] and r.MaxDD >= b["bl_dd"])
            bb = (r.H1 > b["spy_h1"] and r.H2 > b["spy_h2"] and r.OOS_Sharpe > b["spy_oos_s"]
                  and r.MaxDD >= 0.60 * b["spy_dd"] and r.CAGR >= 0.70 * b["spy_cagr"])
            return bool(a), bool(bb)
        pa4, pb4 = verdicts(pick)
        rate_a = float(np.mean([verdicts(r)[0] for _, r in bk.iterrows()]))
        rate_b = float(np.mean([verdicts(r)[1] for _, r in bk.iterrows()]))
        keeps.append(dict(panel=nm, pick=f"{pick.family} q{pick.q} w{int(pick.w)} d{pick.depth} "
                                         f"{pick.cadence} g{pick.gross}",
                          CAGR=pick.CAGR, Sharpe=pick.Sharpe, MaxDD=pick.MaxDD, H1=pick.H1,
                          H2=pick.H2, OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                          OOS_MaxDD=pick.OOS_MaxDD, path_4a=pa4, path_4b=pb4,
                          base_rate_4a=rate_a, base_rate_4b=rate_b,
                          bl_sh=b["bl_sh"], bl_cagr=b["bl_cagr"], bl_dd=b["bl_dd"],
                          bl_h1=b["bl_h1"], bl_h2=b["bl_h2"], bl_oos_s=b["bl_oos_s"],
                          bl_oos_c=b["bl_oos_c"],
                          spy_sh=b["spy_sh"], spy_cagr=b["spy_cagr"], spy_dd=b["spy_dd"],
                          spy_h1=b["spy_h1"], spy_h2=b["spy_h2"], spy_oos_s=b["spy_oos_s"],
                          spy_oos_c=b["spy_oos_c"]))
    keeps = pd.DataFrame(keeps)
    log(keeps[["panel", "pick", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe",
               "OOS_MaxDD", "path_4a", "path_4b", "base_rate_4a", "base_rate_4b"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    log("\n  reference legs on the same windows:")
    log(keeps[["panel", "bl_cagr", "bl_sh", "bl_dd", "bl_h1", "bl_h2", "bl_oos_c", "bl_oos_s",
               "spy_cagr", "spy_sh", "spy_dd", "spy_h1", "spy_h2", "spy_oos_c", "spy_oos_s"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    log(f"\n  IS-only selector 4a passes: {int(keeps.path_4a.sum())} of 3 panels;  "
        f"4b passes: {int(keeps.path_4b.sum())} of 3.")

    # ------------------------------------------------------------------------------- verdict
    log("\n" + "=" * 100)
    log("VERDICT")
    log("=" * 100)
    log(f"  H_GAP    {'CONFIRMED' if h_gap else 'REFUTED'}   the standardised median-mean gap is "
        f"a skew fact (ALL R2 {r_all.R2:.4f}, slope {r_all.slope:.4f} vs Pearson {PEARSON:.4f})")
    log(f"  H_SHAPE  {'CONFIRMED' if h_shape else 'REFUTED'}   shape alone classifies instability "
        f"at LOFO balanced accuracy {best_shape.bal_acc:.4f} (bar {SHAPE_ACC_BAR})")
    log(f"  H_SIGN   {'CONFIRMED' if h_sign else 'REFUTED'}   (median, sd, skew) recovers the "
        f"mean's sign {pa.sign_recovery:.1%} overall / {pa.sign_recovery_unstable:.1%} unstable")
    log(f"  H_UNRES  {'CONFIRMED' if h_unres else 'REFUTED'}   {ua.share_below_bar:.1%} of unstable"
        f" cuts sit below |z| = {Z_BAR} (max |z| {ua.max_abs_z:.4f})")
    log(f"  H_WF     {'CONFIRMED' if h_wf else 'REFUTED'}   IS-fitted law's sign-recovery moves "
        f"{gapwf:.1%} IS -> OOS")
    log(f"  BOOKS    4a {int(keeps.path_4a.sum())}/3, 4b {int(keeps.path_4b.sum())}/3 on the "
        f"IS-only selector - nothing promoted here; KILL for capital.")

    # --------------------------------------------------------------------------------- outputs
    cuts.to_csv(OUT / f"{STEM}.cuts.csv", index=False)
    grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    pd.concat([reg.assign(leg="GAP_REGRESSION"), rec.assign(leg="SIGN_RECOVERY"),
               unres.assign(leg="UNRESOLVABILITY"), cost.assign(leg="RULE_COST")], ignore_index=True
              ).to_csv(OUT / f"{STEM}.regress.csv", index=False)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    pd.concat(books, ignore_index=True).to_csv(OUT / f"{STEM}.books.csv", index=False)
    keeps.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    log(f"\n  wrote {STEM}.[cuts|grid|regress|walkforward|books|keep].csv + .console.txt   "
        f"({time.time() - t0:.1f}s)")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
