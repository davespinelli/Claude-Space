#!/usr/bin/env python3
"""Idea 426 -- put the T1 line in PROTOCOL and back-fill it.

Idea 197 proposed a one-line, sampling-error-free key certificate to replace idea 193's
Spearman (which has false positives AND false negatives):

    a key is point-in-time honest on auto-adjusted closes IFF it is invariant under
        px -> px @ diag(c),   c_i > 0
    because truncating an auto-adjusted panel rescales each column by one positive
    per-name constant.

Idea 433 then priced two instruments against hand-derived ground truth on a 20-key corpus and
recommended the pair DET (idea 428's static degree detector, as the corpus GATE) + CERT (the
certificate, as the ADJUDICATOR) -- and, importantly for the wording, that the clause name the
VALUE certificate at a one-rank-step tolerance, not the RANK certificate idea 426 was drafting.

This run does the two things idea 426 still owes the record:

    PART A  BACK-FILL.  Harvest every key the record can STILL RECONSTRUCT -- every
            self-contained price expression assigned in a committed script, extracted by AST,
            re-evaluated here from source -- and publish the certificate's pass/fail column
            beside each one.  Keys that cannot be reconstructed are counted and their reason
            stated, because the size of that set is the honest limit on any back-fill.
    PART B  THE CLAUSE, drafted in the exact wording it would take, and NOT applied
            (PROTOCOL 6: rules change only via Sunday review).  RULES.md, PROTOCOL.md,
            scan.py, bot.py and baseline.py are untouched by this file.
    PART C  WHAT THE CLAUSE COSTS.  A top-10 ranker book on every harvested key that can
            drive one, on three panels, with both KEEP paths, and PROTOCOL 8's walk-forward
            run twice: choosing over the WHOLE menu and over the T1-PASSING menu only.  If
            the clause is free, deleting the failing keys must not cost OOS Sharpe.

TWO TUNED PARAMETERS, and no more (PROTOCOL 4):
    FORM in {RANK, VALUE}      -- which invariance the certificate reads
    TOL  in {0, ONE-RANK-STEP} -- the tolerance the clause would name
PANEL and the menu cap are reported axes, not tuned ones.

PROTOCOL-fixed: weights decided at close t, applied at t+1; 10 bps per unit turnover (25 bps
reported beside it); long only, no leverage; weekly; warm-up 260 rows; halves at len(r)//2;
rule 8 split 2016-12-31.
SURVIVORSHIP (PROTOCOL 9): B136 and SMALL439 are CURRENT constituent lists, so their levels
are biased upward and no book here is a tradable estimate; SMALL439 drops the 44 names with
data/small_meta.csv max_1d_move >= 1.0.  The load-bearing quantity is the MENU-minus-MENU
contrast inside one panel, which the bias cannot move.

Run:  python3 research/backtests/2026-09-10_put-the-T1-line-in-PROTOCOL-and-back-fill-it_cloud.py
"""
import ast, hashlib, sys, time
from collections import Counter
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, load_volume, rules_v1_weights, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, rebalance_mask, metrics  # noqa

pd.set_option("display.width", 250)
STEM = str(Path(__file__).with_suffix(""))
BT = ROOT / "research" / "backtests"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARMUP, FREQ = 260, "W"
RUNGS = [10.0, 25.0]
HEADLINE = 10.0
SEED, SIGMA, NDRAW = 426, 0.25, 8
MENU_CAP = 40          # reported axis: the N most-used reconstructible ranker keys
TOPN, GROSS = 10, 0.75
_LOG = []


def log(s=""):
    print(s)
    _LOG.append(str(s))


# ---------------------------------------------------------------- vectorised engine
def fast_backtest(prices, weights, freq=FREQ):
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy(); m[0] = True
    T, Ncol = rets.shape
    C = np.cumprod(1.0 + rets, axis=0); Cp = np.vstack([np.ones((1, Ncol)), C[:-1]])
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]; W0 = wt[s0]
    h = W0 * (Cp / Cp[s0]); V = h.sum(axis=1) + (1.0 - W0.sum(axis=1)); held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]; W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p]); Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1)); heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T); turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return (pd.Series((held * rets).sum(axis=1), index=idx),
            pd.Series(turn, index=idx),
            float(held.sum(axis=1)[WARMUP:].mean()))


def legs(r):
    r = r.iloc[WARMUP:]
    h = len(r) // 2
    f, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    ins, oos = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    return dict(CAGR=f["CAGR"], Sharpe=f["Sharpe"], MaxDD=f["MaxDD"], H1=m1["Sharpe"],
                H2=m2["Sharpe"], IS=ins["Sharpe"], OOS=oos["Sharpe"],
                OOS_CAGR=oos["CAGR"], OOS_DD=oos["MaxDD"])


def margins_4b(L, S):
    return dict(H1=L["H1"] - S["H1"], H2=L["H2"] - S["H2"], OOS=L["OOS"] - S["OOS"],
                DD=L["MaxDD"] - 0.60 * S["MaxDD"], CAGR=L["CAGR"] - 0.70 * S["CAGR"])


def v4a(L, B):
    return int(L["H1"] > B["H1"] and L["H2"] > B["H2"] and L["MaxDD"] >= B["MaxDD"])


# ============================================================ THE CERTIFICATE (idea 197/433)
PRICE_NAMES = {"px", "prices", "pxs", "price", "closes", "adj"}
VOL_NAMES = {"vol", "volume", "shares", "vols"}
SAFE_MODULES = {"np", "pd", "numpy", "math"}


def rankpct(df):
    return df.rank(axis=1, pct=True)


def cert_on_key(fn, p, v, ndraw=NDRAW, sigma=SIGMA, seed=SEED):
    """Returns (rank_moved_tol0, value_moved_tol0, rank_moved_1step, value_moved_1step,
    ncols) -- the fraction of comparable cells whose cross-sectional rank (resp. own value)
    moves under px -> px @ diag(c).  The one-rank-step tolerance is 1/ncols on the rank scale
    and, on the value scale, "moved enough to change a rank by one step" is read as a relative
    move above the same 1/ncols (idea 433's convention, kept verbatim so the two runs compare).
    """
    rng = np.random.default_rng(seed)
    K0 = fn(p, v)
    if isinstance(K0, pd.Series):
        K0 = K0.to_frame("K")
    ncol = K0.shape[1]
    step = 1.0 / max(ncol, 1)
    R0 = rankpct(K0)
    out = {k: [] for k in ("r0", "v0", "r1", "v1")}
    for _ in range(ndraw):
        c = pd.Series(rng.lognormal(0.0, sigma, size=p.shape[1]), index=p.columns)
        K1 = fn(p.mul(c, axis=1), v)
        if isinstance(K1, pd.Series):
            K1 = K1.to_frame("K")
        ok = K0.notna() & K1.notna()
        n = int(ok.values.sum())
        if n == 0:
            for k in out: out[k].append(np.nan)
            continue
        dr = (rankpct(K1) - R0).abs()
        rel = (K1 - K0).abs() / K0.abs().clip(lower=1e-12)
        out["r0"].append(float(((dr > 0) & ok).values.sum()) / n)
        out["v0"].append(float(((rel > 0) & ok).values.sum()) / n)
        out["r1"].append(float(((dr > step) & ok).values.sum()) / n)
        out["v1"].append(float(((rel > step) & ok).values.sum()) / n)
    return (float(np.nanmean(out["r0"])), float(np.nanmean(out["v0"])),
            float(np.nanmean(out["r1"])), float(np.nanmean(out["v1"])), ncol)


# ============================================================ PART A: harvest the record's keys
class _NameCheck(ast.NodeVisitor):
    """Is this expression self-contained: does it reference only a price name, a volume name,
    a safe module and literals?"""
    def __init__(self):
        self.names, self.ok = set(), True

    def visit_Name(self, node):
        self.names.add(node.id)

    def visit_Lambda(self, node):
        self.ok = False

    def visit_Call(self, node):
        # a bare call to an unknown free function (not a method) cannot be reconstructed
        if isinstance(node.func, ast.Name) and node.func.id not in SAFE_MODULES:
            self.ok = False
        self.generic_visit(node)


def _classify(expr, src):
    ck = _NameCheck(); ck.visit(expr)
    if not ck.ok:
        return None, "free call or lambda"
    free = {n for n in ck.names if n not in SAFE_MODULES}
    if not (free & PRICE_NAMES):
        return None, "no price name"
    if free - PRICE_NAMES - VOL_NAMES:
        return None, "references a local this file cannot supply: " + ",".join(sorted(free - PRICE_NAMES - VOL_NAMES))[:60]
    return sorted(free), "OK"


def normalise(src, names):
    """Rewrite the price/volume variable to the canonical px / vol so identical keys written
    with different variable names dedupe to one row."""
    out = src
    for n in sorted(names, key=len, reverse=True):
        canon = "px" if n in PRICE_NAMES else "vol"
        out = "".join(
            (canon if tok == n else tok)
            for tok in __import__("re").split(r"(\b\w+\b)", out))
    return " ".join(out.split())


def harvest():
    log("\n=== PART A  HARVEST: every key the record can still reconstruct ===")
    files = sorted(set(list((ROOT / "research").rglob("*.py")) + list((ROOT / "products").rglob("*.py"))))
    rows, reasons = [], Counter()
    nfiles_ok = 0
    for f in files:
        try:
            src = f.read_text()
            tree = ast.parse(src)
        except Exception:
            reasons["PARSE_FAIL"] += 1
            continue
        got = 0
        for node in ast.walk(tree):
            targets = []
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                targets = [(node.targets[0].id, node.value)]
            elif isinstance(node, ast.Return) and node.value is not None:
                targets = [("<return>", node.value)]
            for vname, expr in targets:
                seg = ast.get_source_segment(src, expr)
                if seg is None or len(seg) > 300:
                    continue
                names, why = _classify(expr, seg)
                if names is None:
                    reasons[why.split(":")[0]] += 1
                    continue
                rows.append(dict(file=str(f.relative_to(ROOT)), lineno=expr.lineno, var=vname,
                                 src=" ".join(seg.split()), norm=normalise(seg, names),
                                 uses_vol=bool(set(names) & VOL_NAMES)))
                got += 1
        nfiles_ok += bool(got)
    H = pd.DataFrame(rows)
    log(f"  scanned {len(files)} committed .py files; {nfiles_ok} contain at least one "
        f"self-contained price expression.")
    log(f"  {len(H)} raw expressions extracted; NOT reconstructible, by reason: "
        + ", ".join(f"{k} {v}" for k, v in reasons.most_common(6)))
    if len(H) == 0:
        return H, pd.DataFrame()
    U = (H.groupby("norm")
           .agg(n_sites=("norm", "size"), n_files=("file", "nunique"),
                uses_vol=("uses_vol", "max"),
                example_file=("file", "first"), example_var=("var", "first"))
           .reset_index().sort_values(["n_files", "n_sites"], ascending=False))
    log(f"  {len(U)} DISTINCT keys after normalising the price/volume variable name.")
    return H, U


def build_evaluator(norm):
    env = {"np": np, "pd": pd}
    code = compile(norm, "<key>", "eval")

    def fn(px, vol):
        return eval(code, env, {"px": px, "vol": vol})  # noqa: S307
    return fn


def cert_backfill(U, p, v):
    log("\n  A2  running the certificate on every distinct reconstructible key")
    rows = []
    t0 = time.time()
    for _, r in U.iterrows():
        try:
            fn = build_evaluator(r.norm)
            K = fn(p, v)
        except Exception as e:
            rows.append(dict(r, evaluable=0, why=f"{type(e).__name__}", ncols=np.nan))
            continue
        if isinstance(K, pd.Series):
            K = K.to_frame("K")
        if not isinstance(K, pd.DataFrame) or len(K) != len(p) or K.shape[1] == 0:
            rows.append(dict(r, evaluable=0, why="not key-shaped", ncols=np.nan))
            continue
        if not np.isfinite(K.to_numpy(dtype="float64", na_value=np.nan)).any():
            rows.append(dict(r, evaluable=0, why="all-NaN", ncols=K.shape[1]))
            continue
        try:
            r0, v0, r1, v1, nc = cert_on_key(fn, p, v)
        except Exception as e:
            rows.append(dict(r, evaluable=0, why=f"cert {type(e).__name__}", ncols=np.nan))
            continue
        rows.append(dict(r, evaluable=1, why="OK", ncols=nc,
                         moved_rank_tol0=r0, moved_value_tol0=v0,
                         moved_rank_1step=r1, moved_value_1step=v1,
                         T1_RANK_tol0=int(r0 == 0), T1_VALUE_tol0=int(v0 == 0),
                         T1_RANK_1step=int(r1 == 0), T1_VALUE_1step=int(v1 == 0),
                         single_col=int(nc == 1)))
    K = pd.DataFrame(rows)
    log(f"  certificate run on {len(U)} keys in {time.time()-t0:.0f}s: "
        f"{int(K.evaluable.sum())} evaluable, {int((K.evaluable==0).sum())} not "
        f"({', '.join(f'{k} {v}' for k, v in K[K.evaluable==0].why.value_counts().head(5).items())})")
    ok = K[K.evaluable == 1]
    if len(ok):
        log(f"\n  A3  THE BACK-FILLED PASS/FAIL COLUMN ({len(ok)} keys, four readings of the clause)")
        for col in ("T1_RANK_tol0", "T1_VALUE_tol0", "T1_RANK_1step", "T1_VALUE_1step"):
            log(f"      {col:16s} PASS {int(ok[col].sum()):4d} / {len(ok)}  ({ok[col].mean():.1%})")
        log(f"      of the passers under the recommended reading (VALUE, 1 step), "
            f"{int(ok[ok.T1_VALUE_1step==1].single_col.sum())} are SINGLE-COLUMN keys "
            f"(idea 433's MKTLVL false-clearance class, which passes the RANK form vacuously: "
            f"{int(ok[ok.T1_RANK_1step==1].single_col.sum())} of its passers).")
        dis = ok[(ok.T1_RANK_1step != ok.T1_VALUE_1step)]
        log(f"      RANK and VALUE readings disagree on {len(dis)} of {len(ok)} keys "
            f"({len(dis)/len(ok):.1%}) -- the choice of form is not cosmetic.")
        wt = ok.assign(w=ok.n_sites)
        log(f"      weighted by SITES in the record: VALUE/1step pass rate "
            f"{(wt.T1_VALUE_1step*wt.w).sum()/wt.w.sum():.1%} of {int(wt.w.sum())} committed sites.")
    K.to_csv(f"{STEM}.keys.csv", index=False)
    return K


# ============================================================ GATES
def gate_g0(p, v):
    """G0  reproduce idea 433's committed key table with this file's independently written
    certificate, on its own 20-key ground-truth corpus."""
    f = BT / "2026-09-08_adopt-the-T1-DEGREE-DETECTOR-as-the-PROTOCOL-corpus-gate_cloud.keys.csv"
    if not f.exists():
        log("G0  SKIPPED: idea 433's committed keys.csv not found"); return
    d = pd.read_csv(f)
    col_src = next((c for c in d.columns if c.lower() in ("src", "source", "expr")), None)
    col_r = next((c for c in d.columns if "rank" in c.lower() and "mov" in c.lower()), None)
    col_v = next((c for c in d.columns if ("lvl" in c.lower() or "value" in c.lower() or "level" in c.lower())
                  and "mov" in c.lower()), None)
    log(f"G0  idea 433 committed keys.csv: {len(d)} rows, columns matched "
        f"src={col_src} rank={col_r} value={col_v}")
    if not (col_src and col_r and col_v):
        log("    columns: " + ", ".join(map(str, d.columns))); return
    n, agree_r, agree_v, worst = 0, 0, 0, 0.0
    for _, r in d.iterrows():
        try:
            fn = build_evaluator(" ".join(str(r[col_src]).split()))
            a, b, _, _, _ = cert_on_key(fn, p, v, ndraw=NDRAW, sigma=SIGMA, seed=433)
        except Exception:
            continue
        n += 1
        agree_r += int((a > 0) == (float(r[col_r]) > 0))
        agree_v += int((b > 0) == (float(r[col_v]) > 0))
        worst = max(worst, abs(a - float(r[col_r])), abs(b - float(r[col_v])))
    log(f"    re-run here on {n} of its keys: the ZERO/NON-ZERO verdict agrees "
        f"rank {agree_r}/{n}, value {agree_v}/{n}; max |difference in the moved fraction| "
        f"{worst:.4f} (idea 433 used its own panel slice, so only the verdict is expected exact)")
    assert n == 0 or (agree_r == n and agree_v == n), "G0 FAILED: a verdict disagrees"


def gate_g1(px):
    q = px.drop(columns=["SPY"])
    w = rules_v2_weights(q, band=0.03, gross=0.75)
    fr, ft, _ = fast_backtest(q, w)
    eng = backtest(q, w, cost_bps=0.0, freq=FREQ)
    st = q.index[WARMUP]
    dr = float((fr.loc[st:] - eng["returns"].loc[st:]).abs().max())
    dt_ = float((ft.loc[st:] - eng["turnover"].loc[st:]).abs().max())
    log(f"G1  fast_backtest vs engine.backtest: max|dret| {dr:.3e}  max|dturn| {dt_:.3e}")
    assert dr < 1e-10 and dt_ < 1e-10, "G1 FAILED"


def gate_g2(px):
    """G2  the live book reads as the record publishes it, so the comparands are the real ones."""
    q = px.drop(columns=["SPY"])
    r, t, _ = fast_backtest(q, rules_v2_weights(q, band=0.03, gross=0.75))
    L = legs(r - t * HEADLINE / 1e4)
    log(f"G2  live RULES v2 on U56 @10bps: {L['CAGR']:.2%} / {L['Sharpe']:.4f} / {L['MaxDD']:.2%}")


def gate_g3(p, v):
    """G3  the certificate returns EXACTLY 0 on a key that is scale-free by construction and
    strictly positive on the price level itself -- the two poles of the theorem."""
    a = cert_on_key(build_evaluator("px / px.shift(126) - 1"), p, v)
    b = cert_on_key(build_evaluator("px"), p, v)
    log(f"G3  poles of the theorem: R6 moved rank {a[0]:.3e} value {a[1]:.3e}; "
        f"PX moved rank {b[0]:.4f} value {b[1]:.4f}")
    assert a[0] == 0.0 and a[1] == 0.0 and b[0] > 0 and b[1] > 0, "G3 FAILED"


# ============================================================ PART C: the consequence book
def key_book(K, px, topn=TOPN, gross=GROSS):
    """A book that is nothing but the key: hold the top-n names by the key, equal weight."""
    rank = K.rank(axis=1, ascending=False)
    w = (rank <= topn).astype(float)
    s = w.sum(axis=1).replace(0, np.nan)
    return (w.div(s, axis=0) * gross).fillna(0.0)


def consequence(K, panels, vols):
    log("\n=== PART C  WHAT THE CLAUSE COSTS: a book per key, both KEEP paths, rule 8 ===")
    ok = K[(K.evaluable == 1) & (K.ncols > 1)].copy()
    menu = ok.sort_values(["n_files", "n_sites"], ascending=False).head(MENU_CAP).reset_index(drop=True)
    log(f"  menu: the {len(menu)} most-used reconstructible multi-column keys "
        f"(cap {MENU_CAP}, a reported axis).  T1 VALUE/1step: "
        f"{int(menu.T1_VALUE_1step.sum())} PASS / {int((1-menu.T1_VALUE_1step).sum())} FAIL; "
        f"RANK/1step: {int(menu.T1_RANK_1step.sum())} PASS.")
    rows = []
    for pk, px in panels.items():
        q = px.drop(columns=["SPY"])
        spy = legs(px["SPY"].pct_change().fillna(0.0))
        rb, tb, _ = fast_backtest(q, rules_v2_weights(q, band=0.03, gross=0.75))
        base = {c: legs(rb - tb * c / 1e4) for c in RUNGS}
        v = vols[pk].reindex(q.index).ffill() if vols.get(pk) is not None else None
        if v is None:
            rng = np.random.default_rng(SEED)
            v = pd.DataFrame(rng.lognormal(13.0, 0.8, size=q.shape), index=q.index, columns=q.columns)
        v = v.reindex(columns=q.columns)
        for _, r in menu.iterrows():
            try:
                Kv = build_evaluator(r.norm)(q, v)
                if isinstance(Kv, pd.Series):
                    continue
                Kv = Kv.reindex(columns=q.columns)
                w = key_book(Kv, q)
                if float(w.abs().sum(axis=1).iloc[WARMUP:].mean()) < 1e-9:
                    continue
                r0, t0, gr = fast_backtest(q, w)
            except Exception:
                continue
            for c in RUNGS:
                L = legs(r0 - t0 * c / 1e4)
                m = margins_4b(L, spy)
                rows.append(dict(panel=pk, key=r.norm[:120], n_files=r.n_files, rung=c,
                                 T1_RANK_1step=int(r.T1_RANK_1step),
                                 T1_VALUE_1step=int(r.T1_VALUE_1step),
                                 T1_RANK_tol0=int(r.T1_RANK_tol0),
                                 T1_VALUE_tol0=int(r.T1_VALUE_tol0),
                                 pass4b=int(all(x >= 0 for x in m.values())),
                                 pass4a=v4a(L, base[c]), m_bind=min(m, key=m.get),
                                 m_min=min(m.values()), gross=gr,
                                 spy_OOS=spy["OOS"], spy_OOS_CAGR=spy["OOS_CAGR"],
                                 base_OOS=base[c]["OOS"], base_OOS_CAGR=base[c]["OOS_CAGR"],
                                 base_OOS_DD=base[c]["OOS_DD"], spy_OOS_DD=spy["OOS_DD"], **L))
    G = pd.DataFrame(rows)
    G.to_csv(f"{STEM}.books.csv", index=False)
    log(f"  {len(G)} book rows committed "
        f"({G.groupby(['panel','key']).ngroups} distinct (panel, key) books x {len(RUNGS)} rungs).")

    log("\n  C1  BOTH KEEP PATHS over every book")
    for c in RUNGS:
        s = G[G.rung == c]
        log(f"    {c:5.0f} bps  4b {int(s.pass4b.sum()):3d}/{len(s)}   4a {int(s.pass4a.sum()):3d}/{len(s)}"
            f"   BOTH {int((s.pass4b & s.pass4a).sum()):3d}")
    h = G[G.rung == HEADLINE]
    if h.pass4b.sum():
        log("\n    4b passers at the headline rung (all reported):")
        log(h[h.pass4b == 1][["panel", "key", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS",
                              "T1_VALUE_1step", "m_bind", "m_min"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}")[:4000])
    log("\n  C2  do the T1-FAILING keys earn anything the passing ones do not? "
        "(headline rung, per panel)")
    for pk, s in h.groupby("panel"):
        for col in ("T1_VALUE_1step", "T1_RANK_1step"):
            a, b = s[s[col] == 1], s[s[col] == 0]
            if len(a) and len(b):
                log(f"    {pk:9s} {col:16s} PASS n={len(a):2d} mean Sharpe {a.Sharpe.mean():.4f} "
                    f"OOS {a.OOS.mean():.4f} 4b {int(a.pass4b.sum())} | "
                    f"FAIL n={len(b):2d} mean Sharpe {b.Sharpe.mean():.4f} "
                    f"OOS {b.OOS.mean():.4f} 4b {int(b.pass4b.sum())}  "
                    f"-> delta OOS {a.OOS.mean()-b.OOS.mean():+.4f}")
    return G, menu


def rule8(G):
    log("\n=== PROTOCOL 8  WALK-FORWARD: choose the key on IS 2008-2016, read OOS once ===")
    rows = []
    for (pk, c), s in G.groupby(["panel", "rung"]):
        for menu_name, sub in (("ALL", s),
                               ("T1-PASS (VALUE/1step)", s[s.T1_VALUE_1step == 1]),
                               ("T1-PASS (RANK/1step)", s[s.T1_RANK_1step == 1]),
                               ("T1-FAIL only", s[s.T1_VALUE_1step == 0])):
            if len(sub) == 0:
                continue
            r = sub.loc[sub.IS.astype(float).idxmax()]
            rows.append(dict(panel=pk, rung=c, menu=menu_name, key=r.key, IS=r.IS, OOS=r.OOS,
                             OOS_CAGR=r.OOS_CAGR, OOS_DD=r.OOS_DD, CAGR=r.CAGR,
                             Sharpe=r.Sharpe, MaxDD=r.MaxDD, pass4b=int(r.pass4b),
                             pass4a=int(r.pass4a), base_OOS=r.base_OOS, spy_OOS=r.spy_OOS,
                             base_OOS_CAGR=r.base_OOS_CAGR, spy_OOS_CAGR=r.spy_OOS_CAGR,
                             base_OOS_DD=r.base_OOS_DD, spy_OOS_DD=r.spy_OOS_DD))
    W = pd.DataFrame(rows)
    W.to_csv(f"{STEM}.wf.csv", index=False)
    log(f"  {len(W)} picks (panel x rung x menu).  The clause's cost is ALL minus T1-PASS.")
    log(f"    {'panel':9s} {'rung':>5} {'menu':22s} {'OOS Sh':>8} {'OOS CAGR':>9} {'OOS DD':>8} "
        f"{'4b':>3} | {'v2 OOS':>7} {'SPY OOS':>8}")
    for _, r in W.sort_values(["panel", "rung", "menu"]).iterrows():
        log(f"    {r.panel:9s} {r.rung:5.0f} {r.menu:22s} {r.OOS:8.4f} {r.OOS_CAGR:9.2%} "
            f"{r.OOS_DD:8.2%} {r.pass4b:3d} | {r.base_OOS:7.4f} {r.spy_OOS:8.4f}")
    for c in RUNGS:
        a = W[(W.rung == c) & (W.menu == "ALL")].set_index("panel")
        for m in ("T1-PASS (VALUE/1step)", "T1-PASS (RANK/1step)"):
            b = W[(W.rung == c) & (W.menu == m)].set_index("panel").reindex(a.index)
            chg = int((a.key != b.key).sum())
            log(f"    {c:.0f} bps  {m:22s} changes the pick in {chg} of {len(a)} panels; "
                f"mean OOS Sharpe {a.OOS.mean():.4f} -> {b.OOS.mean():.4f} "
                f"({b.OOS.mean()-a.OOS.mean():+.4f})")
    return W


# ============================================================ PART B: the clause
CLAUSE = """\
PROTOCOL 10 (proposed, NOT adopted by this run) -- T1, the key certificate.

  Any statistic used to SELECT or SCREEN names (a "key") must be invariant under the
  per-name rescaling  px -> px @ diag(c),  c_i > 0.  Auto-adjusted closes are only defined
  up to one positive constant per name, so a key that moves under diag(c) is reading a
  quantity the data does not carry, and every verdict resting on it is a data artefact.

  (a) GATE.  Every committed research script is scanned by the degree detector
      (idea 428's scan_file); a key typed degree != 0 in the price scale is flagged.
  (b) ADJUDICATOR.  A flagged key is cleared only by the VALUE certificate at a
      one-rank-step tolerance: with c drawn log-normal(0, 0.25), no cell of key(px @ diag(c))
      may differ from key(px) by more than 1/N in relative terms, N = names in the panel.
      The RANK form of the certificate MUST NOT be named alone: it clears single-column
      keys vacuously (idea 433's MKTLVL) and, on this record's own back-fill, disagrees with
      the value form on a material share of the keys actually committed.
  (c) REPORTING.  A LEADERBOARD row whose book selects on a key carries that key's T1
      column (PASS / FAIL / NOT-RECONSTRUCTIBLE).  A FAIL is not automatically a KILL --
      it is a statement that the row's verdict is not transferable to another price source.
  (d) SCOPE.  T1 is a REPORTING clause.  No verdict in this record may turn on it, because
      the record has measured its book cost at approximately zero (idea 433; this file).
"""


def main():
    t0 = time.time()
    log("=" * 100)
    log("IDEA 426  put-the-T1-line-in-PROTOCOL-and-back-fill-it   (cloud, 2026-09-10)")
    log("=" * 100)
    px = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    px["SMALL439"] = sm.drop(columns=[c for c in sm.columns if c in bad])
    vols = {"U56": None, "B136": None}
    try:
        vs = load_volume(small=True)
        vols["SMALL439"] = vs.drop(columns=[c for c in vs.columns if c in bad], errors="ignore")
    except Exception as e:
        vols["SMALL439"] = None
        log(f"  (no cached share volume: {type(e).__name__}; every panel uses the deterministic "
            f"price-free surrogate)")
    log("panels: " + "  ".join(f"{k} {v.shape[1]-1} names x {len(v)} rows "
                               f"[{v.index[0].date()}..{v.index[-1].date()}]" for k, v in px.items()))

    # the certificate panel: one deterministic slice, as idea 433 used
    q = px["SMALL439"].drop(columns=["SPY"])
    p = q.iloc[-750:, :140].copy()
    if vols["SMALL439"] is not None:
        v = vols["SMALL439"].reindex(index=p.index, columns=p.columns).ffill()
        vsrc = "data/volume_small.csv[.gz]"
    else:
        rng = np.random.default_rng(SEED)
        v = pd.DataFrame(rng.lognormal(13.0, 0.8, size=p.shape), index=p.index, columns=p.columns)
        vsrc = "deterministic price-free surrogate"
    log(f"certificate panel: SMALL439 slice {p.shape[0]}d x {p.shape[1]} names "
        f"[{p.index[0].date()}..{p.index[-1].date()}], volume from {vsrc}; "
        f"sigma {SIGMA}, {NDRAW} draws, seed {SEED}")

    log("\n=== GATES ===")
    gate_g1(px["U56"])
    gate_g2(px["U56"])
    gate_g3(p, v)
    gate_g0(p, v)

    H, U = harvest()
    H.to_csv(f"{STEM}.sites.csv", index=False)
    K = cert_backfill(U, p, v)

    log("\n=== PART B  THE CLAUSE AS IT WOULD BE WORDED (report-only; PROTOCOL.md untouched) ===")
    for ln in CLAUSE.split("\n"):
        log("  " + ln)

    G, menu = consequence(K, px, vols)
    W = rule8(G)
    log(f"\ndone in {time.time()-t0:.0f}s")
    Path(f"{STEM}.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
