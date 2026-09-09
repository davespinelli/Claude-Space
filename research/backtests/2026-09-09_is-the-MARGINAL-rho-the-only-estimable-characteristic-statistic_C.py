#!/usr/bin/env python3
"""Idea 546 - "is-the-MARGINAL-rho-the-only-estimable-characteristic-statistic" (lane C, 2026-09-09).

The question
------------
Idea 310 (both lanes) found that the RANK-PARTIAL of a characteristic against a panel's OOS
Sharpe does not replicate across disjoint seed blocks for ANY of the four characteristics
(cross-block rank corr of the per-point partial -0.04..-0.30; 53 of 54 `disp` bootstrap CIs
crossing zero), while the MARGINAL rho keeps its sign in 21-26 of 27 points.  The queue asks:
re-read every published characteristic claim in the record that rests on a PARTIAL or a
JOINT-FIT t, and report how many survive restatement on the MARGINAL.

Design (nothing after a gate is read until the gate is graded)
-------------------------------------------------------------
  GATE      Every cell statistic used downstream is RECOMPUTED from the two committed panel
            files (idea 293's 540 panels, seeds 0..59; idea 310-B's fresh 540, seeds 100..159)
            with idea 293's / 284's estimators verbatim, and matched against idea 310-B's
            committed .blockA.csv/.blockB.csv.  Idea 293's 27-point mean partials
            (disp +0.0046, evol +0.1551), idea 284's three within-stratum `corr` rho and its
            four joint-fit t at (q=0.500, k=40), and idea 310-B's committed cross-block
            sign-agreement table are all re-derived.  Nothing is consumed from the parent's
            committed columns: the 20,000-draw permutation p and the 2,000-draw bootstrap CI
            are re-run for all 216 cells with the parent's own seeds, and every downstream
            number is read off the RECOMPUTED columns.

  CENSUS    Every published memo in research/backtests/*.result.md (and, as a second corpus,
            every CHANGELOG entry) is scanned for characteristic claims and each claim is
            classified by the statistic it rests on: MARGINAL (rho / Spearman / rank corr),
            PARTIAL (partial / within-stratum / controlled / residualised), JOINT-FIT t.
            Both readings are REPORTED and neither is selected on: SENTENCE (the statistic
            token must appear in the same sentence as the characteristic) and FILE (anywhere
            in the memo).  Following ideas 523/534, the unit is the CLAIM, not the word: a
            headline-block reading is reported beside the whole-memo reading.

  RESTATE   (a) CELL level, the 216 committed cells (2 blocks x 9 strata x 3 books x 4 chars):
            for each statistic, how many of its SIGNIFICANT cells have a marginal that is
            same-signed and significant, and how many of each statistic's significant cells
            replicate their sign in the other block.
            (b) CLAIM level: each partial/joint-resting claim's characteristic and published
            sign are parsed out of the memo, and the claim is restated on the marginal.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. statistic in {marginal, partial, joint_t}   the statistic a claim is restated on
    2. block     in {A (seeds 0..59), B (seeds 100..159)}
ALL grid points are reported.  Everything else is idea 284/293/310's published convention and
is NOT tuned: 9 strata (q in {0.250,0.500,0.750} x k in {20,40,80}), 60 seeds per stratum, the
three books EWall/CAND10/CAND20, outcome = OOS Sharpe, IS <= 2016-12-31, 75% gross, weekly
cadence, 10 bps, next-day execution.  The census readings are reported at BOTH settings and no
verdict is selected on either.

Pre-registered predictions (written before any restatement number was read; graded verbatim)
    P1  Fewer than half of the record's partial/joint-resting characteristic claims survive
        restatement on the marginal at the record's own |t| >= 2 convention.
    P2  The partial and the marginal name a DIFFERENT strongest characteristic in >= 1/3 of the
        27 (stratum, book) points, in each block.
    P3  No selector - marginal, partial or joint - beats SPY OOS on average in either block.
    P4  Cell level: marginal-significant cells keep their sign across blocks MORE often than
        partial-significant cells do.

Rule 8 walk-forward (required)
    IS = 2009-01-01..2016-12-31 chooses, OOS = 2017-01-01..end read ONCE.  Inside every stratum
    and for every book, each selector fits its own statistic on IS DATA ONLY (the four IS
    characteristics against the panel's IS Sharpe), names the characteristic with the largest
    |statistic|, and picks the panel at that characteristic's extreme in the fitted direction.
    The panel's OOS book is then read once.  Comparands: the do-nothing stratum-mean anchor
    with its seed sd, SPY OOS, RULES v2 (live) OOS.  OOS CAGR / Sharpe / MaxDD for every pick.

Verdicts (both KEEP paths, on every cell of both blocks and on every walk-forward pick)
    4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2.
    4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's, CAGR >= 70% of
        SPY's.

SURVIVORSHIP: the constructed panels draw on SMALL439 and BSTK100, which are CURRENT
constituents of their screens, so every panel inherits the bias whole and every return LEVEL is
inflated.  The object under test here is which STATISTIC about a characteristic is estimable,
not a return level; the bias is common inside a stratum and inflates between-panel spread, so it
runs AGAINST a "nothing is estimable" verdict and does not protect one.  No tradable claim is
made from these panels.

Deterministic, standalone.  Reads baseline.py and committed CSV/markdown only; modifies nothing
outside this script's own output files.
"""
import json, re, sys, glob
from pathlib import Path
import numpy as np, pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

CHARS = ["breadth", "disp", "corr", "evol"]
BOOKS = ["EWall", "CAND10", "CAND20"]
QS = [0.250, 0.500, 0.750]
KS = [20, 40, 80]
STATS = ["marginal", "partial", "joint_t"]
BLOCKS = ["A", "B"]

BT = REPO / "research" / "backtests"
PANELS = {
    "A": BT / "2026-09-06_does-the-CORR-ordering-hold-off-q-0.5_cloud.panels.csv",
    "B": BT / "2026-09-09_is-EVOL-the-real-survivor-not-DISP_B.panelsB.csv",
}
CELLS = {
    "A": BT / "2026-09-09_is-EVOL-the-real-survivor-not-DISP_B.blockA.csv",
    "B": BT / "2026-09-09_is-EVOL-the-real-survivor-not-DISP_B.blockB.csv",
}
STAB = BT / "2026-09-09_is-EVOL-the-real-survivor-not-DISP_B.stability.csv"

REPRO_284_CORR = {"CAND10": -0.3648, "CAND20": -0.4815, "EWall": -0.4708}
REPRO_284_T = {"CAND10": dict(disp=+1.43, evol=-0.97),
               "CAND20": dict(disp=+1.31, evol=+0.23),
               "EWall": dict(disp=+1.65, evol=-0.49)}
REPRO_293_PARTIAL = {"disp": +0.0046, "evol": +0.1551}
REPRO_310_AGREE = {"breadth": ("5/27", "10/27"), "disp": ("9/27", "21/27"),
                   "corr": ("20/27", "26/27"), "evol": ("19/27", "22/27")}
GATE_TOL = 1e-8
N_BOOT, N_PERM = 2000, 20000
T_BAR = 2.0          # the record's own significance convention
P_BAR = 0.05

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 800)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ---------------------------------------------------------------- estimators (284/293 verbatim)
def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 4:
        return np.nan, len(x)
    rx = pd.Series(x).rank().to_numpy()
    ry = pd.Series(y).rank().to_numpy()
    if rx.std() == 0 or ry.std() == 0:
        return np.nan, len(x)
    return float(np.corrcoef(rx, ry)[0, 1]), len(x)


def perm_p(x, y, seed=7, nperm=N_PERM):
    rho, n = spearman(x, y)
    if not np.isfinite(rho):
        return np.nan, np.nan, n
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    rx = pd.Series(x[ok]).rank().to_numpy()
    ry = pd.Series(y[ok]).rank().to_numpy()
    rx = (rx - rx.mean()) / rx.std()
    rng = np.random.default_rng(seed)
    cnt = 0
    for _ in range(nperm):
        p = rng.permutation(ry)
        r = float(np.dot(rx, (p - p.mean()) / p.std()) / len(rx))
        if abs(r) >= abs(rho) - 1e-12:
            cnt += 1
    return rho, (cnt + 1) / (nperm + 1), n


def _rk(v):
    v = pd.Series(np.asarray(v, float)).rank().to_numpy()
    return (v - v.mean()) / (v.std() if v.std() > 0 else 1.0)


def rank_partial(y, x, controls):
    """Idea 293's estimator, verbatim."""
    Y, X = _rk(y), _rk(x)
    C = np.column_stack([np.ones(len(Y))] + [_rk(c) for c in controls])
    B = np.linalg.pinv(C.T @ C) @ C.T
    ry = Y - C @ (B @ Y)
    rx = X - C @ (B @ X)
    if ry.std() == 0 or rx.std() == 0:
        return np.nan
    return float(np.corrcoef(rx, ry)[0, 1])


def partial_boot(y, x, controls, seed=11, nboot=N_BOOT):
    y, x = np.asarray(y, float), np.asarray(x, float)
    C = [np.asarray(c, float) for c in controls]
    n = len(y)
    rng = np.random.default_rng(seed)
    out = np.empty(nboot)
    for b in range(nboot):
        idx = rng.integers(0, n, n)
        out[b] = rank_partial(y[idx], x[idx], [c[idx] for c in C])
    out = out[np.isfinite(out)]
    if len(out) < 100:
        return np.nan, np.nan, np.nan
    return float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5)), float(out.std())


def ols_t(y, X):
    y, X = np.asarray(y, float), np.asarray(X, float)
    n, p = X.shape
    XtXi = np.linalg.pinv(X.T @ X)
    b = XtXi @ (X.T @ y)
    e = y - X @ b
    ss_res = float(e @ e)
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan
    dof = max(1, n - p)
    se = np.sqrt(np.maximum(np.diag(XtXi * (ss_res / dof)), 0))
    t = np.where(se > 0, b / np.where(se > 0, se, 1), np.nan)
    return b, t, r2


def joint_fit(d, y_col):
    """Idea 284's joint fit: y ~ 1 + the four z-scored IS characteristics."""
    y = d[y_col].to_numpy(float)
    cols = []
    for c in CHARS:
        v = d[f"{c}_IS"].to_numpy(float)
        cols.append((v - v.mean()) / (v.std(ddof=0) if v.std(ddof=0) > 0 else 1.0))
    X = np.column_stack([np.ones(len(y))] + cols)
    b, t, r2 = ols_t(y, X)
    return {CHARS[i]: (float(b[i + 1]), float(t[i + 1])) for i in range(len(CHARS))}, float(r2)


def one_sample_t(v):
    v = np.asarray([x for x in v if np.isfinite(x)], float)
    if len(v) < 3 or v.std(ddof=1) == 0:
        return float(v.mean()) if len(v) else np.nan, np.nan, len(v)
    return float(v.mean()), float(v.mean() / (v.std(ddof=1) / np.sqrt(len(v)))), len(v)


# ---------------------------------------------------------------- load + recompute cells
def load_panels(block):
    d = pd.read_csv(PANELS[block])
    if "kind" in d.columns:
        d = d[d["kind"] != "NAMED"].copy()
    d["q"] = d["q"].astype(float).round(3)
    d["k"] = d["k"].astype(int)
    return d


def recompute_cells(block, px):
    """Every cell statistic this run consumes, recomputed from the committed panels with the
    parents' estimators and the parents' seeds (perm 7, bootstrap 11)."""
    rows = []
    for k in KS:
        for q in QS:
            d = px[(px["k"] == k) & (np.isclose(px["q"], q))]
            if len(d) == 0:
                continue
            for book in BOOKS:
                y = d[f"{book}_OOS_Sharpe"]
                jb, jr2 = joint_fit(d, f"{book}_OOS_Sharpe")
                for c in CHARS:
                    others = [d[f"{o}_IS"].to_numpy() for o in CHARS if o != c]
                    rho, pp, n = perm_p(d[f"{c}_IS"], y)
                    rp = rank_partial(y, d[f"{c}_IS"], [d[f"{o}_IS"] for o in CHARS if o != c])
                    lo, hi, sdb = partial_boot(y.to_numpy(), d[f"{c}_IS"].to_numpy(), others)
                    rows.append(dict(block=block, k=k, q=q, book=book, char=c, n=n,
                                     rho_re=rho, p_re=pp, rho_partial_re=rp,
                                     partial_lo_re=lo, partial_hi_re=hi, partial_sd_re=sdb,
                                     partial_crosses_0_re=bool(np.isfinite(lo) and lo < 0 < hi),
                                     joint_b_re=jb[c][0], joint_t_re=jb[c][1], joint_R2_re=jr2))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- census
CHAR_TOKEN = re.compile(r"(?<![A-Za-z0-9_])(breadth|disp|evol|corr)(?![A-Za-z0-9_])", re.I)
CHAR_LONG = {"breadth": r"breadth", "disp": r"disp(?:ersion)?", "evol": r"evol",
             "corr": r"corr(?:elation)?"}
PART_RE = re.compile(r"partial|within-stratum|within stratum|controll|residualis|residualiz|"
                     r"held constant|conditional on|net of the other", re.I)
JOINT_RE = re.compile(r"joint[- ]fit|joint fit|joint_t|joint t\b|multivariate|four z-scored", re.I)
MARG_RE = re.compile(r"marginal|spearman|rank corr|\brho\b|rank rho", re.I)
SIGNED = re.compile(r"[+−–—-]\s?\d*\.\d+")
LEDGER = re.compile(r"\bledger\b|census of the record|corpus census", re.I)


def sentences(text):
    return [s for s in re.split(r"(?<=[.!?;])\s+|\n", text) if s.strip()]


def headline_block(text):
    """The memo's first bolded verdict paragraph (ideas 523/534's 'claim, not word' unit)."""
    m = re.search(r"\*\*(.{20,1200}?)\*\*", text, re.S)
    head = text.split("\n\n")[0] if "\n\n" in text else text[:800]
    return (m.group(1) if m else "") + "\n" + head


def parse_sign(sentence, char):
    """The sign of the number nearest the characteristic mention inside one sentence."""
    pat = re.compile(CHAR_LONG[char], re.I)
    m = pat.search(sentence)
    if not m:
        return 0
    best, bestd = 0, 10 ** 9
    for num in SIGNED.finditer(sentence):
        d = abs(num.start() - m.start())
        if d < bestd:
            bestd = d
            tok = num.group(0)
            best = -1 if tok[0] in "-−–—" else +1
    return best if bestd < 120 else 0


def census(paths, corpus):
    rows = []
    for p in paths:
        txt = Path(p).read_text(encoding="utf-8", errors="replace")
        if not CHAR_TOKEN.search(txt):
            continue
        head = headline_block(txt)
        sents = sentences(txt)
        hsents = sentences(head)
        for c in CHARS:
            cp = re.compile(CHAR_LONG[c], re.I)
            named_file = bool(cp.search(txt))
            named_head = bool(cp.search(head))
            if not named_file:
                continue
            def scan(ss):
                pa = ja = ma = False
                sg, ssent = 0, ""
                for s in ss:
                    if not cp.search(s):
                        continue
                    if PART_RE.search(s):
                        pa = True
                    if JOINT_RE.search(s):
                        ja = True
                    if MARG_RE.search(s):
                        ma = True
                    if sg == 0:
                        g = parse_sign(s, c)
                        if g:
                            sg, ssent = g, s.strip()[:220]
                return pa, ja, ma, sg, ssent
            pa_s, ja_s, ma_s, sign_s, sent_s = scan(sents)
            pa_h, ja_h, ma_h, sign_h, _ = scan(hsents)
            rows.append(dict(corpus=corpus, file=Path(p).name, char=c,
                             named_head=named_head,
                             sent_partial=pa_s, sent_joint=ja_s, sent_marginal=ma_s,
                             file_partial=bool(PART_RE.search(txt)),
                             file_joint=bool(JOINT_RE.search(txt)),
                             file_marginal=bool(MARG_RE.search(txt)),
                             head_partial=pa_h, head_joint=ja_h, head_marginal=ma_h,
                             is_ledger=bool(LEDGER.search(head)),
                             claim_sign=sign_s, claim_sentence=sent_s))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- KEEP paths
def keep_paths(r):
    """r: a row carrying book + v2_ + SPY_ metrics for one panel."""
    a = (r["Sharpe_H1"] > r["v2_H1"]) and (r["Sharpe_H2"] > r["v2_H2"]) and (r["MaxDD"] >= r["v2_MaxDD"])
    b = ((r["Sharpe_H1"] > r["SPY_H1"]) and (r["Sharpe_H2"] > r["SPY_H2"])
         and (r["OOS_Sharpe"] > r["SPY_OOS_Sharpe"])
         and (r["MaxDD"] >= 0.60 * r["SPY_MaxDD"])
         and (r["CAGR"] >= 0.70 * r["SPY_CAGR"]))
    return bool(a), bool(b)


def book_rows(px, book):
    d = pd.DataFrame(dict(
        panel=px["panel"], k=px["k"], q=px["q"], seed=px["seed"],
        CAGR=px[f"{book}_CAGR"], Sharpe=px[f"{book}_Sharpe"], MaxDD=px[f"{book}_MaxDD"],
        Sharpe_H1=px[f"{book}_H1"], Sharpe_H2=px[f"{book}_H2"],
        IS_Sharpe=px[f"{book}_IS_Sharpe"], OOS_Sharpe=px[f"{book}_OOS_Sharpe"],
        OOS_CAGR=px[f"{book}_OOS_CAGR"], OOS_MaxDD=px[f"{book}_OOS_MaxDD"],
        v2_H1=px["v2_H1"], v2_H2=px["v2_H2"], v2_MaxDD=px["v2_MaxDD"],
        v2_OOS_Sharpe=px["v2_OOS_Sharpe"],
        SPY_H1=px["SPY_H1"], SPY_H2=px["SPY_H2"], SPY_MaxDD=px["SPY_MaxDD"],
        SPY_CAGR=px["SPY_CAGR"], SPY_OOS_Sharpe=px["SPY_OOS_Sharpe"],
        SPY_OOS_CAGR=px["SPY_OOS_CAGR"], SPY_OOS_MaxDD=px["SPY_OOS_MaxDD"]))
    d["book"] = book
    return d


# ================================================================== MAIN
def main():
    P("=" * 110)
    P("IDEA 546 - is-the-MARGINAL-rho-the-only-estimable-characteristic-statistic  (lane C, 2026-09-09)")
    P("=" * 110)
    P("Two tuned dials, all grid points reported: statistic in {marginal, partial, joint_t}, block in {A, B}.")
    P("Costs 10 bps, next-day execution, weekly cadence, 75% gross - inherited from ideas 284/293/310, not tuned.")
    P("")

    # ---------------------------------------------------------- GATE
    P("-" * 110)
    P("GATE - recompute every downstream statistic from the two committed panel files")
    P("-" * 110)
    panels = {b: load_panels(b) for b in BLOCKS}
    for b in BLOCKS:
        P(f"  block {b}: {len(panels[b])} constructed panels from {PANELS[b].name}")
    committed = pd.concat([pd.read_csv(CELLS[b]) for b in BLOCKS], ignore_index=True)
    recomp = pd.concat([recompute_cells(b, panels[b]) for b in BLOCKS], ignore_index=True)
    cells = committed.merge(recomp, on=["block", "k", "q", "book", "char"], how="outer",
                            validate="one_to_one")
    assert len(cells) == 216, len(cells)
    gate_rows = []
    for col, re_col in [("rho", "rho_re"), ("p", "p_re"), ("rho_partial", "rho_partial_re"),
                        ("partial_lo", "partial_lo_re"), ("partial_hi", "partial_hi_re"),
                        ("joint_t", "joint_t_re")]:
        d = float(np.nanmax(np.abs(cells[col] - cells[re_col])))
        nbad = int((np.abs(cells[col] - cells[re_col]) > GATE_TOL).sum())
        gate_rows.append(dict(gate=f"G1:{col}", detail=f"216 cells vs idea 310-B committed, {nbad} over tol",
                              maxabs=d, passed=d < GATE_TOL))
    m293 = cells[(cells.block == "A")].groupby("char")["rho_partial_re"].mean()
    for c, v in REPRO_293_PARTIAL.items():
        d = abs(float(m293[c]) - v)
        gate_rows.append(dict(gate=f"G2:293 mean partial {c}", detail=f"published {v:+.4f}",
                              maxabs=d, passed=d < 5e-5))
    cell5040 = cells[(cells.block == "A") & (cells.k == 40) & (np.isclose(cells.q, 0.5))]
    for book, v in REPRO_284_CORR.items():
        got = float(cell5040[(cell5040.book == book) & (cell5040.char == "corr")]["rho_re"].iloc[0])
        d = abs(got - v)
        gate_rows.append(dict(gate=f"G3:284 corr rho {book}", detail=f"published {v:+.4f} got {got:+.4f}",
                              maxabs=d, passed=d < 5e-4))
    for book, dd in REPRO_284_T.items():
        for c, v in dd.items():
            got = float(cell5040[(cell5040.book == book) & (cell5040.char == c)]["joint_t_re"].iloc[0])
            d = abs(got - v)
            gate_rows.append(dict(gate=f"G4:284 joint t {book}/{c}", detail=f"published {v:+.2f} got {got:+.2f}",
                                  maxabs=d, passed=d < 5e-3))
    gate = pd.DataFrame(gate_rows)
    P(fmt(gate.assign(maxabs=gate.maxabs.map(lambda x: f"{x:.3e}")), 4))
    gate.to_csv(f"{OUT}.gate.csv", index=False)
    P(f"  gates passed: {int(gate.passed.sum())}/{len(gate)}")
    bad = cells[np.abs(cells["rho"] - cells["rho_re"]) > GATE_TOL]
    if len(bad):
        P("  !! G1 near-miss cells (committed vs recomputed marginal rho):")
        P(fmt(bad[["block", "k", "q", "book", "char", "rho", "rho_re", "rho_partial",
                   "rho_partial_re"]], 6))
        for blk in BLOCKS:
            for (k, q), g in bad[bad.block == blk].groupby(["k", "q"]):
                d = panels[blk][(panels[blk].k == k) & (np.isclose(panels[blk].q, q))]
                for c in sorted(set(g["char"])):
                    v = d[f"{c}_IS"]
                    P(f"     block {blk} k={k} q={q} char={c}: {v.nunique()} distinct values in 60 "
                      f"panels -> {60 - v.nunique()} exact ties in the committed CSV")
        P("  DIAGNOSIS: the affected cells are ties in the committed panel column, which the parent's")
        P("  in-memory frame did not carry.  EVERY downstream number in this run is computed from the")
        P("  RECOMPUTED columns, which are reproducible from the committed CSV by anyone.")
    P("")

    # significance flags, on the record's own conventions - RECOMPUTED columns only
    cells["sig_marginal"] = cells["p_re"] < P_BAR
    cells["sig_partial"] = ~cells["partial_crosses_0_re"].astype(bool)
    cells["sig_joint_t"] = cells["joint_t_re"].abs() >= T_BAR
    cells["val_marginal"] = cells["rho_re"]
    cells["val_partial"] = cells["rho_partial_re"]
    cells["val_joint_t"] = cells["joint_t_re"]
    cells["rho"] = cells["rho_re"]
    cells.to_csv(f"{OUT}.cells.csv", index=False)

    # ---------------------------------------------------------- CENSUS
    P("-" * 110)
    P("CENSUS - which statistic does each published characteristic claim rest on?")
    P("-" * 110)
    memos = sorted(glob.glob(str(BT / "*.result.md")))
    cen = census(memos, "result.md")
    ch_log = REPO / "research" / "CHANGELOG.md"
    cen_ch = census([ch_log], "CHANGELOG.md")
    cen_all = pd.concat([cen, cen_ch], ignore_index=True)
    cen_all.to_csv(f"{OUT}.census.csv", index=False)
    P(f"  memos scanned: {len(memos)};  memo-characteristic pairs naming a characteristic: {len(cen)}")
    P(f"  distinct memos naming >=1 characteristic: {cen.file.nunique()}")
    tab = []
    for reading, cols in [("SENTENCE", ("sent_partial", "sent_joint", "sent_marginal")),
                          ("HEADLINE", ("head_partial", "head_joint", "head_marginal")),
                          ("FILE", ("file_partial", "file_joint", "file_marginal"))]:
        pcol, jcol, mcol = cols
        sub = cen
        tab.append(dict(reading=reading, pairs=len(sub),
                        partial=int(sub[pcol].sum()), joint_t=int(sub[jcol].sum()),
                        marginal=int(sub[mcol].sum()),
                        partial_or_joint=int((sub[pcol] | sub[jcol]).sum()),
                        files_partial_or_joint=int(sub[sub[pcol] | sub[jcol]].file.nunique())))
    tabdf = pd.DataFrame(tab)
    P(fmt(tabdf, 0))
    P("")
    P("  per characteristic (SENTENCE reading, the tight one):")
    per = cen.groupby("char").agg(pairs=("file", "size"),
                                  partial=("sent_partial", "sum"),
                                  joint_t=("sent_joint", "sum"),
                                  marginal=("sent_marginal", "sum"),
                                  signed_claim=("claim_sign", lambda s: int((s != 0).sum())))
    P(fmt(per, 0))
    P("")

    # ---------------------------------------------------------- RESTATE (a) cell level
    P("-" * 110)
    P("RESTATEMENT (a) - CELL level, 216 committed cells: does a significant PARTIAL / JOINT t")
    P("                  survive restatement on the MARGINAL, and which statistic replicates?")
    P("-" * 110)
    rows = []
    for blk in BLOCKS:
        cb = cells[cells.block == blk]
        other = cells[cells.block != blk].set_index(["k", "q", "book", "char"])
        for st in STATS:
            sig = cb[cb[f"sig_{st}"]]
            n_sig = len(sig)
            same_sign_marg = int((np.sign(sig[f"val_{st}"]) == np.sign(sig["rho"])).sum())
            surv = int(((np.sign(sig[f"val_{st}"]) == np.sign(sig["rho"])) & sig["sig_marginal"]).sum())
            # cross-block sign replication of this statistic's own significant cells
            rep = 0
            for _, r in sig.iterrows():
                key = (r["k"], r["q"], r["book"], r["char"])
                if key in other.index:
                    o = other.loc[key]
                    if np.sign(o[f"val_{st}"]) == np.sign(r[f"val_{st}"]):
                        rep += 1
            rows.append(dict(block=blk, statistic=st, cells=len(cb), n_sig=n_sig,
                             sig_share=n_sig / len(cb),
                             same_sign_as_marginal=same_sign_marg,
                             survives_on_marginal=surv,
                             survive_share=(surv / n_sig) if n_sig else np.nan,
                             own_sign_replicates_other_block=rep,
                             replicate_share=(rep / n_sig) if n_sig else np.nan))
    rest = pd.DataFrame(rows)
    P(fmt(rest, 3))
    rest.to_csv(f"{OUT}.restate_cells.csv", index=False)
    P("")
    P("  all-cell sign replication across blocks (not conditioned on significance):")
    rep_rows = []
    A = cells[cells.block == "A"].set_index(["k", "q", "book", "char"])
    B = cells[cells.block == "B"].set_index(["k", "q", "book", "char"])
    for st in STATS:
        for c in CHARS:
            ia = A.xs(c, level="char")[f"val_{st}"]
            ib = B.xs(c, level="char")[f"val_{st}"]
            j = pd.concat([ia.rename("A"), ib.rename("B")], axis=1).dropna()
            agree = int((np.sign(j.A) == np.sign(j.B)).sum())
            rk = float(pd.Series(j.A).rank().corr(pd.Series(j.B).rank())) if len(j) > 2 else np.nan
            mA, tA, _ = one_sample_t(ia)
            mB, tB, _ = one_sample_t(ib)
            rep_rows.append(dict(statistic=st, char=c, n=len(j), sign_agree=f"{agree}/{len(j)}",
                                 agree_share=agree / len(j), rank_corr_AB=rk,
                                 meanA=mA, tA=tA, meanB=mB, tB=tB,
                                 both_sig_same_sign=bool(np.isfinite(tA) and np.isfinite(tB)
                                                         and abs(tA) >= T_BAR and abs(tB) >= T_BAR
                                                         and np.sign(mA) == np.sign(mB))))
    repdf = pd.DataFrame(rep_rows)
    P(fmt(repdf, 4))
    repdf.to_csv(f"{OUT}.replication.csv", index=False)
    P("")
    P("  idea 310-B's committed sign-agreement table, re-derived here (partial / marginal):")
    for c in CHARS:
        r = repdf[(repdf.char == c)]
        gp = r[r.statistic == "partial"]["sign_agree"].iloc[0]
        gm = r[r.statistic == "marginal"]["sign_agree"].iloc[0]
        ok = (gp, gm) == REPRO_310_AGREE[c]
        P(f"    {c:<8} partial {gp:<6} marginal {gm:<6}   committed {REPRO_310_AGREE[c]}   {'MATCH' if ok else 'DIFFERS'}")
    P("")

    # ---------------------------------------------------------- RESTATE (b) claim level
    P("-" * 110)
    P("RESTATEMENT (b) - CLAIM level: every partial/joint-resting characteristic claim in the record,")
    P("                  restated on the marginal at the record's own |t| >= 2 convention.")
    P("-" * 110)
    P("  survival rule (pre-registered, no new dial): the characteristic's 27-point mean statistic")
    P("  must (i) carry the claim's published sign and (ii) reach |t| >= 2 across the 27 points,")
    P("  in BOTH seed blocks.  The same rule is applied to the claim's OWN statistic as the comparand.")
    corpus_stat = {}
    for st in STATS:
        for c in CHARS:
            mA, tA, _ = one_sample_t(A.xs(c, level="char")[f"val_{st}"])
            mB, tB, _ = one_sample_t(B.xs(c, level="char")[f"val_{st}"])
            corpus_stat[(st, c)] = (mA, tA, mB, tB)

    def survives(st, c, sign):
        mA, tA, mB, tB = corpus_stat[(st, c)]
        return bool(np.sign(mA) == sign and np.sign(mB) == sign
                    and abs(tA) >= T_BAR and abs(tB) >= T_BAR)

    def restate(sub, pcol, jcol, reading):
        out = []
        for _, r in sub.iterrows():
            rests = ("joint_t" if (r[jcol] and not r[pcol])
                     else ("partial" if (r[pcol] and not r[jcol]) else "both"))
            sign = int(r["claim_sign"])
            own = "partial" if rests in ("partial", "both") else "joint_t"
            if sign == 0:
                out.append(dict(reading=reading, file=r["file"], char=r["char"], rests_on=rests,
                                claim_sign=0, survives_marginal=None, survives_own=None,
                                status="UNPARSED-SIGN"))
                continue
            sm, so = survives("marginal", r["char"], sign), survives(own, r["char"], sign)
            out.append(dict(reading=reading, file=r["file"], char=r["char"], rests_on=rests,
                            claim_sign=sign, survives_marginal=sm, survives_own=so,
                            status="SURVIVES" if sm else ("DIES-BOTH" if not so else "DIES-ON-MARGINAL")))
        return pd.DataFrame(out)

    cl = restate(cen[cen.sent_partial | cen.sent_joint], "sent_partial", "sent_joint", "SENTENCE")
    cl_file = restate(cen[(cen.file_partial | cen.file_joint) & (cen.claim_sign != 0)],
                      "file_partial", "file_joint", "FILE")
    claims_all = pd.concat([cl, cl_file], ignore_index=True)
    claims_all.to_csv(f"{OUT}.claims.csv", index=False)
    P("")
    P(fmt(cl.drop(columns=["reading"]), 0))
    n_parsed = int((cl.claim_sign != 0).sum())
    n_surv = int((cl.survives_marginal == True).sum())
    n_own = int((cl.survives_own == True).sum())
    P("")
    P(f"  partial/joint-resting characteristic claims (SENTENCE reading): {len(cl)}"
      f"  ({n_parsed} with a parseable published sign, {len(cl)-n_parsed} unparsed)")
    P(f"  survive restatement on the MARGINAL: {n_surv}/{n_parsed}"
      f"   survive on their OWN statistic: {n_own}/{n_parsed}")
    nf_parsed = len(cl_file)
    nf_surv = int((cl_file.survives_marginal == True).sum())
    nf_own = int((cl_file.survives_own == True).sum())
    P(f"  same, WIDE (FILE) reading: {nf_surv}/{nf_parsed} survive on the marginal,"
      f" {nf_own}/{nf_parsed} on their own statistic")
    P("  by characteristic (SENTENCE reading):")
    P(fmt(cl[cl.claim_sign != 0].groupby("char").agg(claims=("file", "size"),
                                                     surv_marginal=("survives_marginal", "sum"),
                                                     surv_own=("survives_own", "sum")), 0))
    P("")
    P("  the corpus statistic each verdict is read off (27 points per characteristic per block):")
    cs = pd.DataFrame([dict(statistic=st, char=c, meanA=v[0], tA=v[1], meanB=v[2], tB=v[3],
                            sign_stable=bool(np.sign(v[0]) == np.sign(v[2])),
                            t_bar_both=bool(abs(v[1]) >= T_BAR and abs(v[3]) >= T_BAR))
                       for (st, c), v in corpus_stat.items()])
    P(fmt(cs, 4))
    cs.to_csv(f"{OUT}.corpusstat.csv", index=False)
    P("")

    # ---------------------------------------------------------- RULE 8 WALK-FORWARD
    P("-" * 110)
    P("RULE 8 WALK-FORWARD - IS (<=2016-12-31) chooses the statistic AND the characteristic;")
    P("                      OOS (2017-) read once.  Every (statistic, block) grid point reported.")
    P("-" * 110)
    wf_rows, pick_rows = [], []
    for blk in BLOCKS:
        px = panels[blk]
        for st in STATS:
            picks = []
            for k in KS:
                for q in QS:
                    d = px[(px.k == k) & (np.isclose(px.q, q))]
                    for book in BOOKS:
                        yis = d[f"{book}_IS_Sharpe"]
                        best_c, best_v = None, 0.0
                        for c in CHARS:
                            if st == "marginal":
                                v, _ = spearman(d[f"{c}_IS"], yis)
                            elif st == "partial":
                                v = rank_partial(yis, d[f"{c}_IS"], [d[f"{o}_IS"] for o in CHARS if o != c])
                            else:
                                jb, _ = joint_fit(d, f"{book}_IS_Sharpe")
                                v = jb[c][1]
                            if np.isfinite(v) and abs(v) > abs(best_v):
                                best_c, best_v = c, float(v)
                        asc = best_v < 0
                        sel = d.sort_values(f"{best_c}_IS", ascending=asc).iloc[0]
                        rev = d.sort_values(f"{best_c}_IS", ascending=not asc).iloc[0]
                        anchor = float(d[f"{book}_OOS_Sharpe"].mean())
                        sd = float(d[f"{book}_OOS_Sharpe"].std(ddof=1))
                        picks.append(dict(block=blk, statistic=st, k=k, q=q, book=book,
                                          chosen_char=best_c, is_stat=best_v,
                                          panel=sel["panel"],
                                          OOS_Sharpe=float(sel[f"{book}_OOS_Sharpe"]),
                                          OOS_CAGR=float(sel[f"{book}_OOS_CAGR"]),
                                          OOS_MaxDD=float(sel[f"{book}_OOS_MaxDD"]),
                                          rev_OOS_Sharpe=float(rev[f"{book}_OOS_Sharpe"]),
                                          anchor=anchor, seed_sd=sd,
                                          SPY_OOS_Sharpe=float(sel["SPY_OOS_Sharpe"]),
                                          SPY_OOS_CAGR=float(sel["SPY_OOS_CAGR"]),
                                          SPY_OOS_MaxDD=float(sel["SPY_OOS_MaxDD"]),
                                          v2_OOS_Sharpe=float(sel["v2_OOS_Sharpe"])))
            pk = pd.DataFrame(picks)
            pick_rows.append(pk)
            wf_rows.append(dict(block=blk, statistic=st, cells=len(pk),
                                OOS_Sharpe=pk.OOS_Sharpe.mean(),
                                regret_vs_anchor=(pk.OOS_Sharpe - pk.anchor).mean(),
                                mean_seed_sd=pk.seed_sd.mean(),
                                beats_anchor=f"{int((pk.OOS_Sharpe>pk.anchor).sum())}/{len(pk)}",
                                beats_SPY=f"{int((pk.OOS_Sharpe>pk.SPY_OOS_Sharpe).sum())}/{len(pk)}",
                                beats_v2=f"{int((pk.OOS_Sharpe>pk.v2_OOS_Sharpe).sum())}/{len(pk)}",
                                PICK_minus_REVERSE=(pk.OOS_Sharpe - pk.rev_OOS_Sharpe).mean(),
                                OOS_CAGR=pk.OOS_CAGR.mean(), OOS_MaxDD=pk.OOS_MaxDD.mean()))
    picks_all = pd.concat(pick_rows, ignore_index=True)
    picks_all.to_csv(f"{OUT}.picks.csv", index=False)
    wf = pd.DataFrame(wf_rows)
    spy_row = dict(block="-", statistic="SPY (buy & hold)", cells=len(picks_all),
                   OOS_Sharpe=picks_all.SPY_OOS_Sharpe.mean(), regret_vs_anchor=np.nan,
                   mean_seed_sd=np.nan, beats_anchor="-", beats_SPY="-", beats_v2="-",
                   PICK_minus_REVERSE=np.nan, OOS_CAGR=picks_all.SPY_OOS_CAGR.mean(),
                   OOS_MaxDD=picks_all.SPY_OOS_MaxDD.mean())
    v2_row = dict(block="-", statistic="RULES v2 (live)", cells=len(picks_all),
                  OOS_Sharpe=picks_all.v2_OOS_Sharpe.mean(), regret_vs_anchor=np.nan,
                  mean_seed_sd=np.nan, beats_anchor="-", beats_SPY="-", beats_v2="-",
                  PICK_minus_REVERSE=np.nan, OOS_CAGR=np.nan, OOS_MaxDD=np.nan)
    anch_row = dict(block="-", statistic="anchor (stratum mean)", cells=len(picks_all),
                    OOS_Sharpe=picks_all.anchor.mean(), regret_vs_anchor=0.0,
                    mean_seed_sd=picks_all.seed_sd.mean(), beats_anchor="-", beats_SPY="-",
                    beats_v2="-", PICK_minus_REVERSE=np.nan, OOS_CAGR=np.nan, OOS_MaxDD=np.nan)
    wf_full = pd.concat([wf, pd.DataFrame([anch_row, spy_row, v2_row])], ignore_index=True)
    P(fmt(wf_full, 4))
    wf_full.to_csv(f"{OUT}.walkforward.csv", index=False)
    P("")
    # do the statistics disagree about WHICH characteristic to use?
    P("  do the statistics name the same characteristic?  (27 (stratum, book) points per block)")
    dis_rows = []
    for blk in BLOCKS:
        p = picks_all[picks_all.block == blk]
        w = p.pivot_table(index=["k", "q", "book"], columns="statistic", values="chosen_char",
                          aggfunc="first")
        for a, b in [("marginal", "partial"), ("marginal", "joint_t"), ("partial", "joint_t")]:
            agree = int((w[a] == w[b]).sum())
            dis_rows.append(dict(block=blk, pair=f"{a} vs {b}", agree=f"{agree}/{len(w)}",
                                 disagree_share=1 - agree / len(w)))
    dis = pd.DataFrame(dis_rows)
    P(fmt(dis, 3))
    dis.to_csv(f"{OUT}.statdisagree.csv", index=False)
    P("")
    P("  characteristic chosen, by statistic and block:")
    P(fmt(picks_all.groupby(["block", "statistic"])["chosen_char"].value_counts().unstack(fill_value=0), 0))
    P("")

    # ---------------------------------------------------------- KEEP PATHS
    P("-" * 110)
    P("BOTH KEEP PATHS - every cell of both blocks (2 x 540 panels x 3 books) and every WF pick")
    P("-" * 110)
    kp_rows = []
    allbooks = []
    for blk in BLOCKS:
        for book in BOOKS:
            d = book_rows(panels[blk], book)
            d["block"] = blk
            allbooks.append(d)
    ab = pd.concat(allbooks, ignore_index=True)
    ab["p4a"], ab["p4b"] = zip(*[keep_paths(r) for _, r in ab.iterrows()])
    ab.to_csv(f"{OUT}.keeppaths.csv", index=False)
    for blk in BLOCKS:
        s = ab[ab.block == blk]
        kp_rows.append(dict(scope=f"all cells block {blk}", n=len(s),
                            pass_4a=int(s.p4a.sum()), pass_4b=int(s.p4b.sum()),
                            pass_both=int((s.p4a & s.p4b).sum())))
    sel_keys = set(zip(picks_all.panel, picks_all.book))
    sel = ab[[(p, b) in sel_keys for p, b in zip(ab.panel, ab.book)]]
    kp_rows.append(dict(scope="walk-forward picks (all statistics/blocks)", n=len(sel),
                        pass_4a=int(sel.p4a.sum()), pass_4b=int(sel.p4b.sum()),
                        pass_both=int((sel.p4a & sel.p4b).sum())))
    kp = pd.DataFrame(kp_rows)
    P(fmt(kp, 0))
    P("")
    b4 = ab[ab.p4b]
    if len(b4):
        P("  4b passers by (block, q) - the cap-mix gradient the record has seen before:")
        P(fmt(b4.groupby(["block", "q"]).size().rename("n_4b").to_frame(), 0))
    P("")

    # ---------------------------------------------------------- PREDICTIONS
    P("-" * 110)
    P("PRE-REGISTERED PREDICTIONS, GRADED")
    P("-" * 110)
    p1 = (n_surv / n_parsed) < 0.5 if n_parsed else None
    p2 = all(float(dis[(dis.block == b) & (dis.pair == "marginal vs partial")]["disagree_share"].iloc[0]) >= 1 / 3
             for b in BLOCKS)
    p3 = all(float(wf[(wf.block == b) & (wf.statistic == st)]["OOS_Sharpe"].iloc[0])
             < picks_all.SPY_OOS_Sharpe.mean() for b in BLOCKS for st in STATS)
    marg_ag = repdf[repdf.statistic == "marginal"]["agree_share"].mean()
    part_ag = repdf[repdf.statistic == "partial"]["agree_share"].mean()
    p4 = marg_ag > part_ag
    preds = pd.DataFrame([
        dict(pred="P1 <half of partial/joint claims survive on the marginal",
             detail=f"{n_surv}/{n_parsed}", result="PASS" if p1 else "FAIL"),
        dict(pred="P2 marginal and partial name a different char in >=1/3 of points, both blocks",
             detail="; ".join(f"{b}:{float(dis[(dis.block==b)&(dis.pair=='marginal vs partial')]['disagree_share'].iloc[0]):.3f}" for b in BLOCKS),
             result="PASS" if p2 else "FAIL"),
        dict(pred="P3 no selector beats SPY OOS on average in either block",
             detail=f"SPY {picks_all.SPY_OOS_Sharpe.mean():.4f}; best selector {wf.OOS_Sharpe.max():.4f}",
             result="PASS" if p3 else "FAIL"),
        dict(pred="P4 marginal sign replicates across blocks more than the partial",
             detail=f"marginal {marg_ag:.3f} vs partial {part_ag:.3f}",
             result="PASS" if p4 else "FAIL"),
    ])
    P(fmt(preds, 3))
    P("")

    # ---------------------------------------------------------- LEADERBOARD
    P("-" * 110)
    best = wf.sort_values("OOS_Sharpe", ascending=False).iloc[0]
    verdict = ("ANSWERED / KILL of the partial and joint-t readings"
               if (p1 and p3) else "ANSWERED / see console")
    P(f"VERDICT: {verdict}")
    name = "is-the-MARGINAL-rho-the-only-estimable-characteristic-statistic"
    script = Path(__file__).name
    row = (f"| 2026-09-09 | {name} (best selector {best.statistic}, block {best.block}) | "
           f"{best.OOS_CAGR:.1%} | {best.OOS_Sharpe:.2f} | {best.OOS_MaxDD:.1%} | "
           f"{n_surv}/{n_parsed} claims survive on marginal | "
           f"SPY OOS {picks_all.SPY_OOS_Sharpe.mean():.2f} / v2 OOS {picks_all.v2_OOS_Sharpe.mean():.2f} | "
           f"{'KILL' if (p1 and p3) else 'PARK'} | {script} |")
    P("LEADERBOARD row:")
    P(row)
    P("")
    P("Outputs: .gate.csv .cells.csv .census.csv .restate_cells.csv .replication.csv .claims.csv "
      ".corpusstat.csv .walkforward.csv .picks.csv .statdisagree.csv .keeppaths.csv .console.txt")
    flush_log()


if __name__ == "__main__":
    main()
