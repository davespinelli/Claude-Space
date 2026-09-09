#!/usr/bin/env python3
"""QUEUE idea 292 — does-the-suppression-pattern-appear-under-other-panel-dials (cloud, 2026-09-09).

Idea 277 fitted the record's four panel characteristics (breadth, disp, corr, evol) against a
panel outcome and then added the panel set's OWN CONSTRUCTION DIAL (the ETF share `s` that
generated the sweep).  The dial was worth R2 0.0041 on its own and t +3.47 conditional, and
`evol`'s coefficient FLIPPED -0.2058 -> +0.3222.  That is textbook suppression: the published
characteristic coefficient was not an effect, it was a shadow of the dial the panels were built
along.  Idea 292 asks how much of the record's characteristic story is that.

This is a CENSUS, not a book.  It re-fits every published panel-characteristic regression the
record still carries as a committed CSV, once WITHOUT and once WITH the file's own construction
dial, and counts sign changes.

DISCOVERY IS MECHANICAL — no file is hand-picked.  Every *.csv in research/backtests is scanned;
a file enters the corpus iff, after stripping _IS/_OOS suffixes, it carries
  (a) >= 2 characteristic columns from the fixed vocabulary below,
      (an outcome column that is CONSTANT across the file's rows — every panels.csv carries
       the benchmark's own spy_* Sharpe stamped on every row — is dropped as degenerate),
  (b) >= 1 outcome column matching the mechanical outcome rule, and
  (c) >= 1 construction-dial column, and >= 12 rows.
A column may be BOTH a characteristic and a dial (etf_share is exactly that in idea 277); when
it is used as the dial it is dropped from the characteristic block for that fit.

TWO TUNED PARAMETERS, every level reported:
  VOCAB  STRICT = idea 271's four {breadth, disp, corr, evol}
         WIDE   = every numeric column in the file that is neither an outcome nor a dial
  LAM    ridge penalty on the z-scored design (the constant is never penalised),
         {0, 1e-3, 1e-2, 1e-1, 1, 10, 100} — idea 496 showed an unpublished penalty dominates
         the record's residualisation results, so it is a declared dial here, not a default.

REPORTING AXES (not parameters, all reported): the characteristic measurement window (_IS vs
_OOS), the outcome column, which dial is added, and in-sample vs 5-fold out-of-fold R2
(idea 484's ask — an unfolded fit is not evidence).

REPRODUCTION GATE: the run must reproduce idea 277's published table on its own 49 sweep panels
(4 chars R2 0.1956, evol -0.2058; + etf_share R2 0.3717, evol +0.3222, etf_share t +3.4713).
If that does not come back to four decimals the census is not measuring what idea 277 measured.

RULE 8 (PROTOCOL rule 8, in the form a census can carry it): the flip rate is measured on a
random half of the corpus FILES and read once on the held-out half, 20 seeds.  A census statistic
that does not transfer across files is a property of the files, not of the record.

KEEP PATHS 4a/4b: n/a by construction — this run fits no book and trades nothing, so there is no
return series to judge against RULES v2 or SPY.  Stated rather than left blank.

Deterministic, standalone, no network, reads only committed CSVs.
Does not modify RULES.md, PROTOCOL.md, scan.py, bot.py or baseline.py.
"""
import csv
import glob
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
STEM = Path(__file__).stem
ROOT = HERE.parents[1]

CHAR_VOCAB = {"breadth", "disp", "dispersion", "corr", "evol", "xs_mom", "ts_mom",
              "level_s", "level_c", "etf_share", "capq", "advq", "n_elig", "n_names",
              "adv", "dollar_vol", "beta"}
STRICT = ["breadth", "disp", "corr", "evol"]
DIAL_VOCAB = {"k", "k_frac", "seed", "etf_share", "q", "draws", "n_names", "n_elig_grid",
              "s", "width", "q_cap", "n", "gross", "g", "lam", "band", "m", "quantile", "frac"}
OUT_RE = re.compile(r"(oos_sharpe$|^rev$|^rev_oos$|^rev_is$|^rev_eps0$|oossh)", re.I)
LAMS = [0.0, 1e-3, 1e-2, 1e-1, 1.0, 10.0, 100.0]
VOCABS = ["STRICT", "WIDE"]
SEEDS = 20
FOLDS = 5

_LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _LOG.append(s)


def base_name(c):
    c = c.lower()
    for suf in ("_is", "_oos"):
        if c.endswith(suf):
            return c[:-len(suf)]
    return c


# ------------------------------------------------------------------ linear algebra
def fit(y, X, lam=0.0, names=None):
    """Ridge on a design whose first column is the (unpenalised) constant.

    lam = 0 is plain OLS via pinv, so the reproduction gate is exact.  Returns coefficients,
    classical SEs (lam = 0 only; nan otherwise), R2 and n.
    """
    y = np.asarray(y, float)
    X = np.asarray(X, float)
    ok = np.isfinite(X).all(axis=1) & np.isfinite(y)
    X, y = X[ok], y[ok]
    n, p = X.shape
    if lam == 0.0:
        XtXi = np.linalg.pinv(X.T @ X)
    else:
        D = np.eye(p) * lam
        D[0, 0] = 0.0
        XtXi = np.linalg.pinv(X.T @ X + D)
    b = XtXi @ (X.T @ y)
    e = y - X @ b
    ss_res = float(e @ e)
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan
    if lam == 0.0:
        dof = max(1, n - p)
        se = np.sqrt(np.maximum(np.diag(XtXi * (ss_res / dof)), 0))
        t = np.where(se > 0, b / np.where(se > 0, se, 1), np.nan)
    else:
        se = np.full(p, np.nan)
        t = np.full(p, np.nan)
    return dict(b=b, se=se, t=t, r2=r2, n=n, names=names)


def zdesign(df, cols):
    mu = df[cols].mean()
    sd = df[cols].std(ddof=0).replace(0, 1.0)
    Z = (df[cols] - mu) / sd
    return np.column_stack([np.ones(len(df))] + [Z[c].to_numpy(float) for c in cols])


def oof_r2(df, cols, y, lam, folds=FOLDS, seed=0):
    """K-fold out-of-fold R2 (idea 484's bar).  Standardisation is refitted inside each fold."""
    n = len(df)
    if n < folds * 3:
        return np.nan
    rng = np.random.default_rng(seed)
    idx = rng.permutation(n)
    pred = np.full(n, np.nan)
    yv = np.asarray(y, float)
    for f in range(folds):
        te = idx[f::folds]
        tr = np.setdiff1d(idx, te)
        if len(tr) <= len(cols) + 2:
            return np.nan
        d_tr = df.iloc[tr]
        mu = d_tr[cols].mean()
        sd = d_tr[cols].std(ddof=0).replace(0, 1.0)
        Xtr = np.column_stack([np.ones(len(tr))] +
                              [((d_tr[c] - mu[c]) / sd[c]).to_numpy(float) for c in cols])
        d_te = df.iloc[te]
        Xte = np.column_stack([np.ones(len(te))] +
                              [((d_te[c] - mu[c]) / sd[c]).to_numpy(float) for c in cols])
        r = fit(yv[tr], Xtr, lam)
        pred[te] = Xte @ r["b"]
    ss_res = float(((yv - pred) ** 2).sum())
    ss_tot = float(((yv - yv.mean()) ** 2).sum())
    return 1 - ss_res / ss_tot if ss_tot > 0 else np.nan


# ------------------------------------------------------------------ discovery
def discover():
    corpus = []
    for f in sorted(glob.glob(str(HERE / "*.csv"))):
        p = Path(f)
        if p.stem.startswith(STEM):                      # never census this run's own output
            continue
        try:
            with open(f, newline="") as fh:
                head = next(csv.reader(fh))
        except Exception:
            continue
        lo = [c.lower() for c in head]
        bs = [base_name(c) for c in lo]
        chars = {b for b in bs if b in CHAR_VOCAB}
        dials = {c for c in lo if c in DIAL_VOCAB}
        outs = [c for c, b in zip(lo, bs)
                if OUT_RE.search(c) and b not in CHAR_VOCAB and c not in DIAL_VOCAB]
        try:
            df = pd.read_csv(f)
        except Exception:
            continue
        df.columns = [c.lower() for c in df.columns]
        if len(chars) < 2 or not outs or not dials or len(df) < 12:
            continue
        corpus.append(dict(path=p, name=p.name, df=df, chars=sorted(chars),
                           dials=sorted(dials), outs=outs))
    return corpus


def char_cols(df, chars, window, exclude=()):
    """Resolve base characteristic names to actual columns at the requested window."""
    out = []
    for c in chars:
        if c in exclude:
            continue
        cand = [f"{c}_{window}", c] if window else [c]
        for k in cand:
            if k in df.columns and pd.api.types.is_numeric_dtype(df[k]):
                out.append(k)
                break
    return out


def wide_cols(df, outs, dials):
    bad = set(outs) | set(dials)
    keep = []
    for c in df.columns:
        if c in bad or not pd.api.types.is_numeric_dtype(df[c]):
            continue
        if OUT_RE.search(c) or re.search(r"(sharpe|cagr|maxdd|^h1$|^h2$|keep4|fails4)", c, re.I):
            continue
        if df[c].nunique() < 3:
            continue
        keep.append(c)
    return keep[:12]                                     # cap the block; p/n is idea 498's problem


def main():
    print(__doc__)
    _LOG.append(__doc__)

    corpus = discover()
    P("=" * 110)
    P(f"MECHANICAL DISCOVERY — {len(corpus)} committed CSVs qualify as published "
      f"panel-characteristic regressions")
    for c in corpus:
        P(f"  {len(c['df']):5d} rows  {c['name']}")
        P(f"         chars={c['chars']}  dials={c['dials']}  outcomes={c['outs']}")
    files = sorted({c["name"].split(".")[0] for c in corpus})
    P(f"\n  {len(files)} distinct parent SCRIPTS behind them: " + ", ".join(files))
    P("  This is the whole record's stock of panel-characteristic regressions. The queue's")
    P("  phrase 'every published panel-characteristic regression' is a small corpus, and that")
    P("  is itself a finding — idea 295 counted 26 files NAMING a panel property, but only")
    P(f"  {len(files)} commit the panel-level table needed to re-fit one.")

    # ---------------------------------------------------------------- reproduction gate
    P("\n" + "=" * 110)
    P("REPRODUCTION GATE — idea 277's published Q1 table (49 sweep panels, y = rev)")
    gate_ok = False
    swp = HERE / "2026-09-06_is-ETF36-a-third-cluster-or-just-a-small-sample_C.panelshare.csv"
    if swp.exists():
        d = pd.read_csv(swp)
        d.columns = [c.lower() for c in d.columns]
        d = d.dropna(subset=STRICT + ["rev", "etf_share"])   # both fits on the SAME 49 panels
        a = fit(d.rev.to_numpy(), zdesign(d, STRICT), 0.0, ["const"] + STRICT)
        b = fit(d.rev.to_numpy(), zdesign(d, STRICT + ["etf_share"]), 0.0,
                ["const"] + STRICT + ["etf_share"])
        P(f"  n = {a['n']} (published 49)")
        P(f"  [4 chars]              R2 {a['r2']:.4f} (published 0.1956)")
        for nm, bb, tt in zip(a["names"], a["b"], a["t"]):
            P(f"      {nm:10s} coef {bb:+.4f}  t {tt:+.4f}")
        P(f"  [4 chars + etf_share]  R2 {b['r2']:.4f} (published 0.3717)")
        for nm, bb, tt in zip(b["names"], b["b"], b["t"]):
            P(f"      {nm:10s} coef {bb:+.4f}  t {tt:+.4f}")
        ev_a = a["b"][a["names"].index("evol")]
        ev_b = b["b"][b["names"].index("evol")]
        gate_ok = (abs(a["r2"] - 0.1956) < 5e-4 and abs(b["r2"] - 0.3717) < 5e-4
                   and abs(ev_a + 0.2058) < 5e-4 and abs(ev_b - 0.3222) < 5e-4 and a["n"] == 49)
        P(f"  evol {ev_a:+.4f} -> {ev_b:+.4f} (published -0.2058 -> +0.3222)")
        P(f"  GATE {'PASS' if gate_ok else 'FAIL'}")
    else:
        P("  GATE FILE MISSING — census still runs, but the anchor is unverified.")

    # ---------------------------------------------------------------- the census
    P("\n" + "=" * 110)
    P("THE CENSUS — every (file, outcome, window, vocab, lam, dial) cell, all reported")
    rows = []
    for c in corpus:
        df, outs, dials = c["df"], c["outs"], c["dials"]
        for window in ("is", "oos", ""):
            for vocab in VOCABS:
                if vocab == "STRICT":
                    cols_all = char_cols(df, [x for x in c["chars"] if x in STRICT], window)
                    if len(cols_all) < 2:
                        continue
                else:
                    if window != "":
                        continue                          # WIDE has no window: it takes columns as they are
                    cols_all = wide_cols(df, outs, dials)
                    if len(cols_all) < 2:
                        continue
                for y_col in outs:
                    for dial in dials:
                        if dial not in df.columns or not pd.api.types.is_numeric_dtype(df[dial]):
                            continue
                        cols = [x for x in cols_all if base_name(x) != dial and x != dial]
                        if len(cols) < 2:
                            continue
                        d = df.dropna(subset=cols + [y_col, dial]).copy()
                        if len(d) < max(12, 3 * (len(cols) + 2)) or d[dial].nunique() < 2:
                            continue
                        # a DEGENERATE outcome is not an outcome: benchmark columns (spy_*)
                        # are the same number stamped on every row, and come back with an
                        # sd of ~1e-16 of float dust, which makes R2 meaningless.
                        yy = d[y_col].to_numpy(float)
                        if d[y_col].nunique() < 3 or yy.std() <= 1e-9 * max(1.0, abs(yy.mean())):
                            continue
                        y = d[y_col].to_numpy(float)
                        for lam in LAMS:
                            A = fit(y, zdesign(d, cols), lam, ["const"] + cols)
                            B = fit(y, zdesign(d, cols + [dial]), lam, ["const"] + cols + [dial])
                            oa = oof_r2(d, cols, y, lam)
                            ob = oof_r2(d, cols + [dial], y, lam)
                            for j, nm in enumerate(cols, start=1):
                                ba, bb = A["b"][j], B["b"][j]
                                rows.append(dict(
                                    file=c["name"], y=y_col, window=window or "raw", vocab=vocab,
                                    lam=lam, dial=dial, char=nm, n=A["n"], p=len(cols),
                                    coef_base=ba, coef_dial=bb,
                                    t_base=A["t"][j], t_dial=B["t"][j],
                                    flip=bool(np.sign(ba) != np.sign(bb) and ba != 0 and bb != 0),
                                    d_abs=abs(bb - ba),
                                    r2_base=A["r2"], r2_dial=B["r2"],
                                    oof_base=oa, oof_dial=ob,
                                    dial_coef=B["b"][-1], dial_t=B["t"][-1]))
    R = pd.DataFrame(rows)
    R.to_csv(HERE / f"{STEM}.census.csv", index=False)
    P(f"  {len(R)} coefficient pairs over {R.file.nunique()} files, "
      f"{R.y.nunique()} outcomes, {R.char.nunique()} distinct characteristics, "
      f"{R.dial.nunique()} dials, {len(LAMS)} penalties, {len(VOCABS)} vocabularies.")

    # ---------------------------------------------------------------- headline
    P("\n" + "=" * 110)
    P("HEADLINE — how often does adding the panels' OWN construction dial flip a published")
    P("characteristic coefficient's SIGN?")
    P(f"\n  POOLED over every cell: {int(R.flip.sum())} / {len(R)} = {R.flip.mean():.1%}")
    P("\n  by tuned parameter 1 (vocabulary):")
    P(R.groupby("vocab").flip.agg(["mean", "sum", "size"]).to_string(
        float_format=lambda v: f"{v:.4f}"))
    P("\n  by tuned parameter 2 (ridge penalty) — idea 496's dial:")
    P(R.groupby("lam").flip.agg(["mean", "sum", "size"]).to_string(
        float_format=lambda v: f"{v:.4f}"))
    P("\n  by FILE (the unit that matters — pooled shares over-weight the big files):")
    P(R.groupby("file").flip.agg(["mean", "sum", "size"]).to_string(
        float_format=lambda v: f"{v:.4f}"))
    P("\n  by DIAL:")
    P(R.groupby("dial").flip.agg(["mean", "sum", "size"]).to_string(
        float_format=lambda v: f"{v:.4f}"))
    P("\n  by CHARACTERISTIC (the record's own headline names first):")
    P(R.groupby("char").flip.agg(["mean", "sum", "size"]).sort_values("size", ascending=False)
      .head(20).to_string(float_format=lambda v: f"{v:.4f}"))
    P("\n  FILE-CLUSTERED headline: mean of the per-file flip rates "
      f"{R.groupby('file').flip.mean().mean():.4f} "
      f"(sd {R.groupby('file').flip.mean().std(ddof=1):.4f}, {R.file.nunique()} files)")

    P("\n  Is a flip the same thing as a REAL flip?  A coefficient that is indistinguishable")
    P("  from zero in both fits can 'flip' on noise.  Restricting to pairs where the BASE")
    P("  coefficient is itself significant at |t| >= 2 (lam = 0 only, where t is defined):")
    sig = R[(R.lam == 0.0) & (R.t_base.abs() >= 2)]
    P(f"    {int(sig.flip.sum())} / {len(sig)} = {sig.flip.mean():.1%} of SIGNIFICANT published")
    P(f"    coefficients flip sign when the dial enters "
      f"({sig.file.nunique()} files, file-clustered mean "
      f"{sig.groupby('file').flip.mean().mean():.4f})")
    sig2 = R[(R.lam == 0.0) & (R.t_base.abs() >= 2) & (R.t_dial.abs() >= 2)]
    P(f"    of those, {int(sig2.flip.sum())} / {len(sig2)} = "
      f"{sig2.flip.mean() if len(sig2) else float('nan'):.1%} flip to a coefficient that is")
    P("    ALSO significant — a published sign REPLACED by a significant opposite sign.")

    P("\n  Does the dial actually belong in the model?  In-sample R2 always rises when a")
    P("  regressor is added, so the honest test is the 5-fold OUT-OF-FOLD R2 (idea 484):")
    q = R[R.lam == 0.0].groupby("file")[["r2_base", "r2_dial", "oof_base", "oof_dial"]].mean()
    q["d_is"] = q.r2_dial - q.r2_base
    q["d_oof"] = q.oof_dial - q.oof_base
    P(q.to_string(float_format=lambda v: f"{v:+.4f}"))
    ok = R[R.lam == 0.0].dropna(subset=["oof_base", "oof_dial"])
    P(f"    the dial improves OUT-OF-FOLD R2 in {int((ok.oof_dial > ok.oof_base).sum())} / "
      f"{len(ok)} cells ({(ok.oof_dial > ok.oof_base).mean():.1%}); in-sample it improves in "
      f"{int((ok.r2_dial > ok.r2_base).sum())} / {len(ok)} by construction")

    # ---------------------------------------------------------------- rule 8
    P("\n" + "=" * 110)
    P("RULE 8 — the census's own walk-forward: flip rate measured on a random half of the")
    P("corpus FILES, read once on the held-out half, 20 seeds.")
    fl = sorted(R.file.unique())
    wf = []
    for s in range(SEEDS):
        rng = np.random.default_rng(s)
        perm = rng.permutation(len(fl))
        a = {fl[i] for i in perm[:len(fl) // 2]}
        b = {fl[i] for i in perm[len(fl) // 2:]}
        ra = R[R.file.isin(a)].flip.mean()
        rb = R[R.file.isin(b)].flip.mean()
        wf.append(dict(seed=s, n_a=len(a), n_b=len(b), rate_a=ra, rate_b=rb, gap=rb - ra))
    W = pd.DataFrame(wf)
    W.to_csv(HERE / f"{STEM}.walkforward.csv", index=False)
    P(f"  IS half mean flip rate {W.rate_a.mean():.4f} (sd {W.rate_a.sd if False else W.rate_a.std(ddof=1):.4f}), "
      f"held-out half {W.rate_b.mean():.4f} (sd {W.rate_b.std(ddof=1):.4f})")
    P(f"  |held-out - IS| mean {W.gap.abs().mean():.4f}, max {W.gap.abs().max():.4f}; "
      f"the held-out rate is within 10 pp of the IS rate in {int((W.gap.abs() <= 0.10).sum())}/{SEEDS} seeds")

    # ---------------------------------------------------------------- the named claims
    P("\n" + "=" * 110)
    P("THE RECORD'S OWN NAMED COEFFICIENTS — every STRICT characteristic at lam = 0, per file,")
    P("with the dial that moves it most.  This is the table a re-read of the record needs.")
    P(f"  {'file':62s} {'y':18s} {'char':10s} {'dial':10s} {'base':>9s} {'+dial':>9s} "
      f"{'t_base':>8s} {'t_dial':>8s}  flip")
    st = R[(R.lam == 0.0) & (R.vocab == "STRICT")]
    for (f_, y_, ch_), g in st.groupby(["file", "y", "char"]):
        g = g.reindex(g.d_abs.sort_values(ascending=False).index)
        r = g.iloc[0]
        P(f"  {f_[:62]:62s} {y_[:18]:18s} {ch_:10s} {r.dial:10s} {r.coef_base:+9.4f} "
          f"{r.coef_dial:+9.4f} {r.t_base:+8.3f} {r.t_dial:+8.3f}  "
          f"{'FLIP' if r.flip else ''}")
    P(f"\n  STRICT-vocabulary summary at lam = 0: {int(st.flip.sum())}/{len(st)} = "
      f"{st.flip.mean():.1%} of the record's four named characteristics flip; file-clustered "
      f"{st.groupby('file').flip.mean().mean():.4f}")

    P("\n" + "=" * 110)
    P("KEEP PATHS — 4a and 4b are n/a for this run BY CONSTRUCTION: the census fits no book,")
    P("holds no position and produces no return series, so there is nothing to compare against")
    P("RULES v2 or SPY.  Nothing here is promotable to RULES.md; the output is a re-read of")
    P("published coefficients.")

    (HERE / f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")
    P(f"\nwrote {STEM}.census.csv / .walkforward.csv / .console.txt")
    (HERE / f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
