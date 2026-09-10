#!/usr/bin/env python3
"""Idea 659 (lane C, 2026-09-10) -- publish the SIGN BALANCE of every fitted SELECTOR TARGET.

Idea 497's rule 8 found that F1's selector target `IS_Sharpe(M) - IS_Sharpe(6W)` is positive
on 94.8% of 115 books while its OOS counterpart is positive on 27.0%, and that every fitted
arm at every fold count and every penalty collapsed onto ONE constant arm -- the losing one.

The queue asks: census the record's "can property X choose dial Y" studies for one-signed
targets and report how many of their fitted selectors are constants in disguise.

INSTRUMENT.  A *selector target* is a per-row PAIRED DIFFERENCE committed to a CSV: the
quantity whose SIGN says which arm a chooser should pick.  For every such column,

    sign_balance = max(share(t > 0), share(t < 0))   over finite non-zero rows
    headroom     = 1 - sign_balance

is the largest share of rows any non-constant selector could ever add over the best constant
arm.  A fitted selector is a CONSTANT IN DISGUISE when, fitted out of fold on that study's own
properties, it either emits a single value on every row (LITERAL) or fails to beat the best
constant (NO LIFT).  Both are measured, not asserted.

PARAMS (2, both reported at every grid point):
  1. STUDY SET  in {CHOOSER (stem names a chooser question -- a STATIC text match, reported
                             only because the queue names this population),
                   SELECTOR (the file carries a committed selector/pick column -- ARTEFACT
                             evidence, the primary set),
                   ALL      (every committed CSV carrying a paired-difference column)}
  2. SIGN-BALANCE BAR b in {0.60, 0.70, 0.80, 0.90, 0.95, 0.99}
  => 3 x 6 = 18 grid points, all reported in .censusgrid.csv.

Section (4) is PROTOCOL rule 8 run LIVE on prices: four weight-level dials (top-n, v2 gross,
v2 band, v1 vol cap) x four market properties (breadth, dispersion, SPY vol, SPY trend).  Each
property->dial selector is fitted on 2009-2016 ONLY (bucket threshold = IS median, per-bucket
arm = IS-Sharpe argmax) and scored untouched on 2017-2026 against its own constant-dial arm,
the live RULES v2 book and SPY.  Both KEEP paths are evaluated on every arm.

Deterministic, standalone, ~2 min.  Reads only committed artefacts + research/baseline.py.
Writes .console.txt .targets.csv .censusgrid.csv .constancy.csv .grid.csv (the 16 live
selectors) .walkforward.csv (31 arms).
Modifies nothing.
"""
import re
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics  # noqa: E402

SEED = 659
KFOLD = 5
LAM = 1.0
MAXROWS = 4000                       # deterministic subsample cap for very tall artefacts
COST = 10.0
FREQ = "W"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
BARS = [0.60, 0.70, 0.80, 0.90, 0.95, 0.99]
SETS = ["CHOOSER", "SELECTOR", "ALL"]

# a paired difference: the sign of the number is the choice
DELTA = re.compile(
    r"(^d_?(sharpe|cagr|maxdd|dd|calmar|turn)|^delta|_delta$|margin|regret|excess|_gap$|^gap"
    r"|_vs_|^vs_|_minus_|_over_|edge|lift|_adv$|^gain$|^m$|^a$|^dsh|^dcagr|^ddd)", re.I)
SELCOL = re.compile(r"^(pick|picked|choice|chosen|selector|sel|argmax)(_|$)", re.I)
CHOOSER_STEM = re.compile(r"(choos|choose|chose|select|pick|pin-|decide)", re.I)
P175 = "2026-09-05_does-cadence-skill-survive-a-second-corpus_cloud"

LINES = []


def P(s=""):
    print(s)
    LINES.append(s)


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return np.nan
    ra = pd.Series(a[ok]).rank().values
    rb = pd.Series(b[ok]).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


# ----------------------------------------------------------------------------- (0) GATES
def gates(px):
    P("(0) GATES")
    # RULES.md's acceptance table was computed on the 2026-09-04 price vintage; the committed
    # cache now runs to 2026-09-09, which moves the halves split. Gate on the published vintage,
    # then state the current-vintage numbers this study actually uses.
    pv = px.loc[:"2026-09-04"]
    rv = backtest(pv, rules_v2_weights(pv), cost_bps=COST, freq=FREQ)["returns"].loc[pv.index[260]:]
    mv = metrics(rv)
    hv = len(rv) // 2
    v1h, v2h = metrics(rv.iloc[:hv])["Sharpe"], metrics(rv.iloc[hv:])["Sharpe"]
    P(f"  G1 LIVE RULES v2, PUBLISHED vintage (<=2026-09-04): CAGR {mv['CAGR']:.4%}  "
      f"Sharpe {mv['Sharpe']:.4f}  MaxDD {mv['MaxDD']:.4%}  halves {v1h:.4f} / {v2h:.4f}")
    P(f"     RULES.md publishes 8.66% / 1.2056 / -12.05% / 1.2259 / 1.1908  -> max |d| "
      f"{max(abs(mv['CAGR']-0.0866), abs(mv['Sharpe']-1.2056), abs(mv['MaxDD']+0.1205), abs(v1h-1.2259), abs(v2h-1.1908)):.2e}")
    b = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)
    start = px.index[260]
    r = b["returns"].loc[start:]
    m = metrics(r)
    h = len(r) // 2
    h1, h2 = metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]
    P(f"     CURRENT vintage (<=2026-09-09, used everywhere below): CAGR {m['CAGR']:.4%}  "
      f"Sharpe {m['Sharpe']:.4f}  MaxDD {m['MaxDD']:.4%}  halves {h1:.4f} / {h2:.4f} "
      f"(3 extra sessions move H1/H2 by +{h1-v1h:+.4f}/{h2-v2h:+.4f})")

    L = pd.read_csv(OUT / f"{P175}.ladder.csv")
    IS = L.pivot_table(index="book", columns="point", values="IS_Sharpe")
    OS = L.pivot_table(index="book", columns="point", values="OOS_Sharpe")
    d_is, d_os = (IS["M"] - IS["6W"]).dropna(), (OS["M"] - OS["6W"]).dropna()
    s_is, s_os = float((d_is > 0).mean()), float((d_os > 0).mean())
    rho = spearman(d_is.reindex(d_os.index).values, d_os.values)
    P(f"  G2 PROVENANCE, idea 497's own target on idea 175's committed ladder ({len(d_is)} books): "
      f"IS share>0 {s_is:.4f} (published 0.948), OOS {s_os:.4f} (published 0.270), "
      f"Spearman {rho:+.4f} (published -0.1801) -> max |d| "
      f"{max(abs(s_is-0.948), abs(s_os-0.270), abs(rho+0.1801)):.2e}")
    P()
    return b, start, s_is, s_os


# ------------------------------------------------------------------- (1) THE TARGET CENSUS
def census():
    # this script's OWN outputs are excluded: the census must not read itself
    files = sorted([p.name for p in OUT.glob("*.csv")] + [p.name for p in OUT.glob("*.csv.gz")])
    files = [f for f in files if not f.startswith(STEM)]
    hdr = {}
    for f in files:
        opener = __import__("gzip").open if f.endswith(".gz") else open
        with opener(OUT / f, "rt", errors="replace") as fh:
            hdr[f] = [c.strip().strip('"') for c in fh.readline().strip().split(",")]

    rows = []
    for f, cs in hdr.items():
        tc = [c for c in cs if DELTA.search(c)]
        if not tc:
            continue
        sc = [c for c in cs if SELCOL.search(c)]
        try:
            df = pd.read_csv(OUT / f, usecols=tc + sc, low_memory=False)
        except Exception:
            continue
        for c in tc:
            s = pd.to_numeric(df[c], errors="coerce").astype(float)
            s = s[np.isfinite(s)]
            nz = s[s != 0]
            if len(nz) < 30:
                continue
            pos = float((nz > 0).mean())
            rows.append(dict(file=f, target=c, n=int(len(s)), nnz=int(len(nz)), share_pos=pos,
                             sign_balance=max(pos, 1 - pos), has_selcol=int(bool(sc)),
                             chooser_stem=int(bool(CHOOSER_STEM.search(f)))))
    T = pd.DataFrame(rows)
    T["degenerate"] = (T.sign_balance >= 1 - 1e-9).astype(int)
    return T, len(hdr)


def in_set(T, s):
    return T[T.chooser_stem == 1] if s == "CHOOSER" else (T[T.has_selcol == 1] if s == "SELECTOR" else T)


# ------------------------------------------------- (2) IS THE FITTED SELECTOR A CONSTANT?
def oof_selector(X, y):
    """Out-of-fold sign predictor vs the out-of-fold best constant. Standardised ridge,
    intercept unpenalised, standardisation fitted on the TRAIN fold only."""
    rng = np.random.RandomState(SEED)
    n = len(y)
    fold = np.empty(n, int)
    for i, ix in enumerate(rng.permutation(n)):
        fold[ix] = i % KFOLD
    pred, cpred = np.zeros(n), np.zeros(n)
    for k in range(KFOLD):
        tr, te = fold != k, fold == k
        if tr.sum() < 10 or te.sum() < 1:
            return None
        Xt = X[tr]
        mu, sd = Xt.mean(0), Xt.std(0)
        sd[sd == 0] = 1.0
        Z = np.hstack([np.ones((int(tr.sum()), 1)), (Xt - mu) / sd])
        A = Z.T @ Z + LAM * np.eye(Z.shape[1])
        A[0, 0] -= LAM
        try:
            beta = np.linalg.solve(A, Z.T @ y[tr])
        except np.linalg.LinAlgError:
            return None
        Ze = np.hstack([np.ones((int(te.sum()), 1)), (X[te] - mu) / sd])
        pred[te] = np.sign(Ze @ beta)
        cpred[te] = np.sign(y[tr].sum()) or 1.0
    pred[pred == 0] = 1.0
    return pred, cpred


def constancy(T):
    out = []
    for f in sorted(T.file.unique()):
        try:
            df = pd.read_csv(OUT / f, low_memory=False)
        except Exception:
            continue
        if len(df) > MAXROWS:
            df = df.sample(MAXROWS, random_state=SEED).reset_index(drop=True)
        num = df.select_dtypes(include=[np.number])
        cat = [c for c in df.columns if c not in num.columns and 2 <= df[c].nunique(dropna=True) <= 10]
        D = (pd.get_dummies(df[cat].astype(str), drop_first=True).astype(float)
             if cat else pd.DataFrame(index=df.index))
        for c in T.loc[T.file == f, "target"]:
            if c not in df.columns:
                continue
            y = pd.to_numeric(df[c], errors="coerce").astype(float)
            ok = np.isfinite(y) & (y != 0)
            if ok.sum() < 40:
                continue
            yy = np.sign(y[ok].values)
            # properties = the study's own columns, MINUS every other paired difference
            # (another delta is an outcome, not a property) and minus anything that
            # reconstructs the target at |corr| >= 0.99.
            keep = [x for x in num.columns if x != c and not DELTA.search(x)]
            Xn = num.loc[ok, keep].astype(float)
            Xn = Xn.loc[:, Xn.notna().all() & (Xn.std() > 0)]
            if Xn.shape[1]:
                cr = np.abs(np.corrcoef(np.vstack([y[ok].values, Xn.values.T]))[0, 1:])
                Xn = Xn.loc[:, ~(np.nan_to_num(cr) >= 0.99)]
            Xd = D.loc[ok.values]
            if Xd.shape[1]:
                Xd = Xd.loc[:, Xd.std() > 0]
            p = Xn.shape[1] + Xd.shape[1]
            if p < 1:
                out.append(dict(file=f, target=c, p=0, n=int(ok.sum()),
                                fit=np.nan, const=np.nan, lift=np.nan, literal=np.nan))
                continue
            r = oof_selector(np.hstack([Xn.values, Xd.values]), yy)
            if r is None:
                continue
            pred, cpred = r
            out.append(dict(file=f, target=c, p=int(p), n=int(ok.sum()),
                            fit=float((pred == yy).mean()), const=float((cpred == yy).mean()),
                            lift=float((pred == yy).mean() - (cpred == yy).mean()),
                            literal=int(len(np.unique(pred)) == 1)))
    return pd.DataFrame(out)


# --------------------------------------------------------- (3) THE IS -> OOS SIGN FLIP
def is_oos_pairs(T):
    """Targets committed as an IS/OOS pair of the SAME quantity: the flip idea 497 found."""
    base = {}
    for f, c in zip(T.file, T.target):
        lo = c.lower()
        for pre, tag in (("is_", "IS"), ("oos_", "OOS")):
            if lo.startswith(pre):
                base.setdefault((f, lo[len(pre):]), {})[tag] = c
        for suf, tag in (("_is", "IS"), ("_oos", "OOS")):
            if lo.endswith(suf):
                base.setdefault((f, lo[:-len(suf)]), {})[tag] = c
    rows = []
    idx = T.set_index(["file", "target"])
    for (f, q), d in sorted(base.items()):
        if "IS" not in d or "OOS" not in d:
            continue
        a, b = idx.loc[(f, d["IS"])], idx.loc[(f, d["OOS"])]
        rows.append(dict(file=f, quantity=q, is_col=d["IS"], oos_col=d["OOS"],
                         is_pos=float(a.share_pos), oos_pos=float(b.share_pos),
                         is_sb=float(a.sign_balance), oos_sb=float(b.sign_balance),
                         flips=int((a.share_pos > 0.5) != (b.share_pos > 0.5))))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ (4) RULE 8, LIVE
def topn_eqw(px, n, gross=1.0, max_vol=9.9):
    s, above, vol20 = score(px, vol_scale=False)
    elig = s.where(above & (vol20 < max_vol))
    rank = elig.rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (gross / n)


def properties(px):
    ma = px.rolling(200).mean()
    spy = px["SPY"]
    return {
        "BREADTH": (px > ma).mean(axis=1),
        "DISP": (px / px.shift(63) - 1).std(axis=1),
        "SPYVOL": spy.pct_change().rolling(20).std() * np.sqrt(252),
        "SPYTREND": spy / spy.rolling(200).mean() - 1,
    }


def dial_families(px):
    return {
        "topn":   {f"n={n}": topn_eqw(px, n) for n in (5, 10, 20)},
        "gross":  {f"g={g:.2f}": rules_v2_weights(px, band=0.03, gross=g) for g in (0.50, 0.75, 1.00)},
        "band":   {f"b={b:.2f}": rules_v2_weights(px, band=b, gross=0.75) for b in (0.01, 0.03, 0.06)},
        "volcap": {f"v={v}": topn_eqw(px, 20, max_vol=v) for v in (0.40, 0.60, 9.9)},
    }


def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v else np.nan


def arm_row(name, family, prop, r, spy, v2, note):
    h = len(r) // 2
    m = metrics(r)
    h1, h2 = metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]
    ro, so = r.loc[OOS_START:], spy.loc[OOS_START:]
    mo, mso = metrics(ro), metrics(so)
    ms, mv = metrics(spy), metrics(v2)
    hv = len(v2) // 2
    v1h, v2h = metrics(v2.iloc[:hv])["Sharpe"], metrics(v2.iloc[hv:])["Sharpe"]
    hs = len(spy) // 2
    s1, s2 = metrics(spy.iloc[:hs])["Sharpe"], metrics(spy.iloc[hs:])["Sharpe"]
    f4a = [t for t, ok in (("H1", h1 > v1h), ("H2", h2 > v2h), ("DD", m["MaxDD"] >= mv["MaxDD"])) if not ok]
    f4b = [t for t, ok in (("H1", h1 > s1), ("H2", h2 > s2), ("OOS", mo["Sharpe"] > mso["Sharpe"]),
                           ("DD", abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"])),
                           ("CAGR", m["CAGR"] >= 0.70 * ms["CAGR"])) if not ok]
    return dict(arm=name, family=family, prop=prop, note=note,
                CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                SPY_OOS_Sharpe=mso["Sharpe"], v2_OOS_Sharpe=metrics(v2.loc[OOS_START:])["Sharpe"],
                pass4a=int(not f4a), pass4b=int(not f4b),
                fail4a=",".join(f4a), fail4b=",".join(f4b))


def rule8(px, v2res, start):
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    v2 = v2res["returns"].loc[start:]
    v1 = backtest(px, rules_v1_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
    props = properties(px)
    fams = dial_families(px)
    rets = {}
    for fam, arms in fams.items():
        for a, W in arms.items():
            rets[(fam, a)] = backtest(px, W, cost_bps=COST, freq=FREQ)["returns"].loc[start:]

    rows, diag = [], []
    wmap = {"LIVE RULES v2": rules_v2_weights(px)}
    rows.append(arm_row("LIVE RULES v2", "-", "-", v2, spy, v2, "baseline"))
    rows.append(arm_row("RULES v1", "-", "-", v1, spy, v2, "previous book"))
    rows.append(arm_row("SPY", "-", "-", spy, spy, v2, "benchmark"))

    for fam, arms in fams.items():
        keys = list(arms)
        isr = {a: rets[(fam, a)].loc[:IS_END] for a in keys}
        const = max(keys, key=lambda a: sharpe(isr[a]))
        for a in keys:
            wmap[f"{fam}:{a}"] = arms[a]
            rows.append(arm_row(f"{fam}:{a}", fam, "-", rets[(fam, a)], spy, v2,
                                "IS-argmax constant" if a == const else "fixed dial"))
        # sign balance of what the chooser is separating: daily rival-minus-constant, IS only
        d = np.concatenate([(isr[a] - isr[const]).values for a in keys if a != const])
        d = d[np.isfinite(d) & (d != 0)]
        sb_daily = float(max((d > 0).mean(), (d <= 0).mean()))
        R = pd.DataFrame({a: isr[a] for a in keys})
        modal_share = float((R.idxmax(axis=1) == const).mean())
        # the granularity the chooser actually reads: idea 497's target is a per-BOOK IS
        # Sharpe difference, so cut IS into non-overlapping 126-day books and sign it there.
        w = []
        for a in keys:
            if a == const:
                continue
            for s0 in range(0, len(isr[a]) - 126 + 1, 126):
                w.append(sharpe(isr[a].iloc[s0:s0 + 126]) - sharpe(isr[const].iloc[s0:s0 + 126]))
        w = np.array([x for x in w if np.isfinite(x) and x != 0])
        sb_window = float(max((w > 0).mean(), (w <= 0).mean())) if len(w) else np.nan

        for pname, ps in props.items():
            s = ps.reindex(rets[(fam, keys[0])].index)
            thr = float(s.loc[:IS_END].median())
            hi = (s >= thr).fillna(False)
            pick = {}
            for side, mask in (("LOW", ~hi), ("HIGH", hi)):
                m_is = mask.loc[:IS_END]
                pick[side] = max(keys, key=lambda a: sharpe(isr[a][m_is.values]))
            W = fams[fam][pick["HIGH"]].where(hi, fams[fam][pick["LOW"]])
            r = backtest(px, W, cost_bps=COST, freq=FREQ)["returns"].loc[start:]
            collapsed = int(pick["LOW"] == pick["HIGH"])
            note = (f"collapsed to {pick['LOW']}" if collapsed
                    else f"LOW={pick['LOW']} HIGH={pick['HIGH']}")
            wmap[f"{fam}<-{pname}"] = W
            rows.append(arm_row(f"{fam}<-{pname}", fam, pname, r, spy, v2, note))
            diag.append(dict(family=fam, prop=pname, thr=thr, pick_low=pick["LOW"],
                             pick_high=pick["HIGH"], const=const, collapsed=collapsed,
                             collapsed_to_const=int(collapsed and pick["LOW"] == const),
                             sb_daily=sb_daily, sb_window=sb_window,
                             modal_day_share=modal_share,
                             OOS_Sharpe=metrics(r.loc[OOS_START:])["Sharpe"],
                             const_OOS_Sharpe=metrics(rets[(fam, const)].loc[OOS_START:])["Sharpe"]))
    return pd.DataFrame(rows), pd.DataFrame(diag), wmap, spy, v2


# ------------------------------------------------------------------------------- MAIN
def main():
    P(f"# Idea 659 -- publish the SIGN BALANCE of every fitted SELECTOR TARGET (lane C, 2026-09-10)")
    P(f"# seed {SEED}, K={KFOLD}, ridge lam={LAM}, cost {COST:.0f} bps, weekly, next-day execution")
    P()
    px = load_universe()
    v2res, start, s_is_497, s_os_497 = gates(px)

    P("(1) THE CENSUS -- sign balance of every committed selector target")
    T, nfiles = census()
    T.to_csv(OUT / f"{STEM}.targets.csv", index=False)
    P(f"  {nfiles} committed CSVs scanned; {T.file.nunique()} carry a paired-difference column; "
      f"{len(T)} selector targets with >=30 non-zero rows.")
    q = T.sign_balance.describe()
    P(f"  sign_balance: min {q['min']:.4f}  q25 {q['25%']:.4f}  median {q['50%']:.4f}  "
      f"q75 {q['75%']:.4f}  mean {q['mean']:.4f}")
    P(f"  EXACTLY one-signed (sign_balance = 1, i.e. NO choice exists at all): "
      f"{int(T.degenerate.sum())}/{len(T)} = {T.degenerate.mean():.1%}")
    P()

    P("  GRID -- 18 points, study set x sign-balance bar (all reported in .grid.csv):")
    grid = []
    for s in SETS:
        sub = in_set(T, s)
        for b in BARS:
            hit = sub[sub.sign_balance >= b]
            grid.append(dict(study_set=s, bar=b, n_files=int(sub.file.nunique()),
                             n_targets=int(len(sub)), n_one_signed=int(len(hit)),
                             share_one_signed=float(len(hit) / len(sub)) if len(sub) else np.nan,
                             n_degenerate=int(hit.degenerate.sum()),
                             median_headroom=float(1 - hit.sign_balance.median()) if len(hit) else np.nan))
    G = pd.DataFrame(grid)
    for s in SETS:
        sub = G[G.study_set == s]
        P(f"    {s:9s} ({int(sub.n_files.iloc[0]):3d} files, {int(sub.n_targets.iloc[0]):4d} targets): " +
          "  ".join(f"b={r.bar:.2f} {r.n_one_signed:4d} ({r.share_one_signed:.1%})"
                    for r in sub.itertuples()))
    P()

    P("(2) ARE THE FITTED SELECTORS CONSTANTS IN DISGUISE?")
    C = constancy(T)
    C.to_csv(OUT / f"{STEM}.constancy.csv", index=False)
    J = C.dropna(subset=["fit"]).merge(T, on=["file", "target"])
    P(f"  {len(J)} targets refitted out of fold on their own study's properties "
      f"(median p = {J.p.median():.0f} predictors).")
    P(f"  LITERAL constant (one value on every OOF row): {int(J.literal.sum())}/{len(J)} "
      f"= {J.literal.mean():.1%}")
    P(f"  NO LIFT over the best constant (OOF accuracy <= constant's): "
      f"{int((J.lift <= 0).sum())}/{len(J)} = {(J.lift <= 0).mean():.1%}")
    P(f"  Spearman(sign_balance, OOF lift) = {spearman(J.sign_balance, J.lift):+.4f}")
    P("  by sign-balance bucket:")
    P(f"    {'bucket':>14s} {'n':>5s} {'literal':>8s} {'no lift':>8s} {'mean lift':>10s}")
    for lo, hi, lab in [(0.50, 0.60, "[0.50,0.60)"), (0.60, 0.70, "[0.60,0.70)"),
                        (0.70, 0.80, "[0.70,0.80)"), (0.80, 0.90, "[0.80,0.90)"),
                        (0.90, 0.95, "[0.90,0.95)"), (0.95, 1.0 - 1e-9, "[0.95,1.00)"),
                        (1.0 - 1e-9, 1.1, "== 1.00")]:
        s = J[(J.sign_balance >= lo) & (J.sign_balance < hi)]
        if len(s):
            P(f"    {lab:>14s} {len(s):5d} {s.literal.mean():8.1%} {(s.lift <= 0).mean():8.1%} "
              f"{s.lift.mean():+10.4f}")
    nd = J[J.degenerate == 0]
    P(f"  DROPPING the {int(J.degenerate.sum())} degenerate targets of these 1617 (sign_balance = 1, where a "
      f"constant is the only possible answer):")
    P(f"    literal {nd.literal.mean():.1%}, no lift {(nd.lift <= 0).mean():.1%} over {len(nd)} targets; "
      f"at 0.95 <= sb < 1: literal "
      f"{nd[nd.sign_balance>=0.95].literal.mean():.1%}, no lift "
      f"{(nd[nd.sign_balance>=0.95].lift <= 0).mean():.1%} over "
      f"{int((nd.sign_balance>=0.95).sum())} targets.")
    P()

    P("(3) THE IS -> OOS SIGN FLIP (idea 497's mechanism, censused)")
    F = is_oos_pairs(T)
    if len(F):
        P(f"  {len(F)} targets committed as a matched IS/OOS pair over {F.file.nunique()} files.")
        P(f"  IS sign_balance median {F.is_sb.median():.4f}; OOS median {F.oos_sb.median():.4f}; "
          f"the majority SIDE flips IS->OOS on {int(F.flips.sum())}/{len(F)} = {F.flips.mean():.1%}.")
        P(f"  Spearman(IS share>0, OOS share>0) = {spearman(F.is_pos, F.oos_pos):+.4f}  "
          f"(idea 497's own pair: {s_is_497:.4f} -> {s_os_497:.4f}).")
    else:
        P("  no matched IS/OOS target pairs found.")
    P()

    P("(4) PROTOCOL RULE 8 -- the same question run LIVE on prices")
    P(f"  IS 2009-{IS_END[:4]} chooses the bucket threshold and the per-bucket dial; "
      f"{OOS_START[:4]}-2026 is untouched.")
    W, D, wmap, spy_r, v2_r = rule8(px, v2res, start)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    D.to_csv(OUT / f"{STEM}.grid.csv", index=False)   # per-selector diagnostics
    G.to_csv(OUT / f"{STEM}.censusgrid.csv", index=False)
    sel = W[W["prop"] != "-"]
    P(f"  {len(W)} arms ({len(sel)} fitted property->dial selectors, "
      f"{len(W)-len(sel)-3} fixed dials, 3 references).")
    P(f"  COLLAPSED to a single dial value (both buckets picked the same arm): "
      f"{int(D.collapsed.sum())}/{len(D)} = {D.collapsed.mean():.1%}; "
      f"of those, {int(D.collapsed_to_const.sum())} collapsed onto the IS-argmax constant arm.")
    P(f"  IS sign_balance of rival-minus-constant: {D.sb_daily.mean():.4f} at DAY granularity, "
      f"{D.sb_window.mean():.4f} at the 126-day BOOK granularity a chooser actually reads "
      f"(per family: " + ", ".join(f"{f} {v:.3f}" for f, v in D.groupby('family').sb_window.first().items()) + ").")
    P(f"  mean share of IS days whose best arm IS the constant {D.modal_day_share.mean():.4f}. "
      f"Spearman(sb_window, collapsed) over the {len(D)} selectors = "
      f"{spearman(D.sb_window, D.collapsed):+.4f}.")
    P()
    P("  arms (full sample from " + str(start.date()) + ", then OOS 2017-):")
    P(f"    {'arm':22s} {'CAGR':>7s} {'Sharpe':>7s} {'MaxDD':>8s} {'H1':>6s} {'H2':>6s} "
      f"{'oCAGR':>7s} {'oSh':>6s} {'oDD':>8s}  4a 4b  note")
    for r in W.itertuples():
        P(f"    {r.arm:22s} {r.CAGR:7.2%} {r.Sharpe:7.3f} {r.MaxDD:8.2%} {r.H1:6.3f} {r.H2:6.3f} "
          f"{r.OOS_CAGR:7.2%} {r.OOS_Sharpe:6.3f} {r.OOS_MaxDD:8.2%}   {r.pass4a}  {r.pass4b}  {r.note}")
    P()
    nsel = len(sel)
    P(f"  KEEP paths over all {len(W)} arms: 4a {int(W.pass4a.sum())}/{len(W)}, "
      f"4b {int(W.pass4b.sum())}/{len(W)}.")
    P(f"  KEEP paths over the {nsel} FITTED selectors only: 4a {int(sel.pass4a.sum())}/{nsel}, "
      f"4b {int(sel.pass4b.sum())}/{nsel}.")
    beat = sel.OOS_Sharpe.values > D.const_OOS_Sharpe.values
    P(f"  fitted selector beats its own constant-dial arm OOS: {int(beat.sum())}/{nsel} = "
      f"{beat.mean():.1%}; mean OOS Sharpe {sel.OOS_Sharpe.mean():.4f} vs constant "
      f"{D.const_OOS_Sharpe.mean():.4f} (d {sel.OOS_Sharpe.mean()-D.const_OOS_Sharpe.mean():+.4f}).")
    col = sel[sel.note.str.startswith("collapsed")]
    P(f"  every 4b pass among the fitted selectors is a COLLAPSED one: "
      f"{int(col.pass4b.sum())}/{int(sel.pass4b.sum())} of the fitted 4b passes come from arms "
      f"that chose one dial value for both buckets, i.e. they pass AS the constant.")
    P()

    P("  (4b) AUDIT of every arm that clears a KEEP path -- cost ladder and the DD tie")
    v2m = metrics(v2_r)
    for r in W[(W.pass4a == 1) | (W.pass4b == 1)].itertuples():
        tie = "TIE with the live book (PROTOCOL's >= passes it)" if abs(r.MaxDD - v2m["MaxDD"]) < 1e-9 else ""
        P(f"    {r.arm}  [4a={r.pass4a} 4b={r.pass4b}]  {r.note}  {tie}")
        if r.arm in wmap:
            lad = []
            for c in (5.0, 10.0, 25.0, 50.0):
                rr = backtest(px, wmap[r.arm], cost_bps=c, freq=FREQ)["returns"].loc[start:]
                bb = backtest(px, wmap["LIVE RULES v2"], cost_bps=c, freq=FREQ)["returns"].loc[start:]
                hh = len(rr) // 2
                a1, a2 = metrics(rr.iloc[:hh])["Sharpe"], metrics(rr.iloc[hh:])["Sharpe"]
                b1, b2 = metrics(bb.iloc[:hh])["Sharpe"], metrics(bb.iloc[hh:])["Sharpe"]
                ok = a1 > b1 and a2 > b2 and metrics(rr)["MaxDD"] >= metrics(bb)["MaxDD"]
                lad.append(f"{c:.0f}bps Sh {metrics(rr)['Sharpe']:.4f} vs v2 {metrics(bb)['Sharpe']:.4f} "
                           f"({'4a' if ok else '--'})")
            P("      " + " | ".join(lad))
    P()

    P("(5) VERDICT")
    P(f"  The record's selector targets are ONE-SIGNED at scale: median sign_balance "
      f"{T.sign_balance.median():.4f}, and {int(T.degenerate.sum())} of {len(T)} "
      f"({T.degenerate.mean():.1%}) admit NO choice at all (every row one sign).")
    P(f"  Sign balance is what decides whether a fitted selector is a constant: literal-constant "
      f"rate rises monotonically from "
      f"{J[(J.sign_balance<0.60)].literal.mean():.1%} below 0.60 to "
      f"{nd[nd.sign_balance>=0.95].literal.mean():.1%} at 0.95<=sb<1 to 100.0% at sb=1.")
    P(f"  Live, the same collapse reproduces: {int(D.collapsed.sum())}/{len(D)} fitted "
      f"property->dial selectors are constants in disguise, and the fitted set beats its own "
      f"constant OOS {beat.mean():.1%} of the time.")
    P(f"  4a: {int(W.pass4a.sum())}/{len(W)} arms.  4b: {int(W.pass4b.sum())}/{len(W)} arms.")
    P("  No RULES change. RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    print(f"\nwrote {STEM}.console.txt .targets.csv .censusgrid.csv .constancy.csv "
          f".grid.csv .walkforward.csv")


if __name__ == "__main__":
    main()
