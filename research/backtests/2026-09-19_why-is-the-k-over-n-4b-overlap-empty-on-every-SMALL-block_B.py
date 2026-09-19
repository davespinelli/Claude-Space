#!/usr/bin/env python3
"""Idea 908 (lane B, 2026-09-19) — WHY IS THE k/n 4b LEG-OVERLAP EMPTY ON EVERY SMALL BLOCK?

THE PREMISE (idea 887, committed 2026-09-15).  On a 1,710-book k/n grid the two LEVEL legs of
PROTOCOL path 4b

    L_CAGR :  CAGR  >= 0.70 x SPY CAGR            (the floor)
    L_DD   :  MaxDD >= 0.60 x SPY MaxDD           (the cap, both negative)

overlap in 7 of 12 (panel, constr) blocks but in 0 of 4 on SMALL, where 174 of 192 cells clear
NEITHER leg.  887 never said WHICH leg SMALL fails, nor whether the failure is a property of
SMALL-CAP NAMES or merely of HOW MANY names the panel carries (U56 holds 56, SMALL 662).  This
run decomposes the failure leg by leg against SIZE-MATCHED RANDOM DRAWS from every panel.

TUNED PARAMETERS (exactly 2, the queue's own): PANEL SIZE m x FAMILY.
REPORTED AXES (not tuned, every point published): panel {U56, B136, SMALL} x q (887's k/n
ladder) x construction {RESPREAD, DEGROSS} x cost rung {10, 25} bps x seed draw.
FROZEN at 887's headline: gross 0.75, cadence W, next-day execution (engine semantics).

PRE-REGISTERED, WRITTEN BEFORE ANY NUMBER IS READ.

 (P1) DECOMPOSITION.  Per (panel, m): the pass rate of L_CAGR, of L_DD and of BOTH, pooled over
      families, q, constr and seeds at the 10 bps headline rung.  Every cell published.

 (P2) SIZE vs PANEL.  H_SIZE: SMALL's empty overlap is a NAME-COUNT fact — at the matched size
      m = 55 the SMALL draws' BOTH-rate comes within 0.10 of the U56 draws'.  H_PANEL: the gap
      survives matching.  Decided by the m = 55 row; the whole size ladder is published beside it
      so the reader can see the trajectory rather than one contrast.

 (P3) MECHANISM (H_CALMAR).  Clearing both LEVEL legs implies, BY ALGEBRA AND NOT BY EVIDENCE,

          Calmar = CAGR / |MaxDD|  >=  (0.70 x SPY CAGR) / (0.60 x |SPY MaxDD|)
                                    =  1.1667 x SPY Calmar

      so the Calmar ceiling is a NECESSARY condition and its recall is 1.0000 by construction; a
      run that published that as a finding would be publishing a tautology, and this one says so
      up front.  The EMPIRICAL content is entirely in (a) the PRECISION of the bar — how often a
      book clears 1.1667 x SPY Calmar and still misses a level leg — and (b) the per-panel MAXIMUM
      Calmar against the bar, which is what decides whether a panel can reach the overlap AT ALL.
      Pre-registered reading: if SMALL's max Calmar sits BELOW the bar while U56's sits above,
      the empty overlap is a CALMAR-CEILING fact about the panel and the leg-by-leg split of P1 is
      a consequence of WHICH SIDE of the ceiling a given construction lands on, not a cause.

 (P4) BOTH KEEP PATHS (rule 4) evaluated at EVERY published cell.  4a is judged against RULES v2
      run on the SAME sub-panel (a matched-universe baseline; the FULL-panel live book is
      reported separately for continuity).  4b is judged against SPY over the common window.

 (P6) THE MISSING RUNG — **ADDED AFTER P1-P5 WERE READ, AND SAID SO RATHER THAN BACK-DATED.**
      P3's SMALL cells that clear the Calmar ceiling split into exactly two kinds: RESPREAD books
      at gross 0.75 with CAGR 13-27% and MaxDD -27% to -54%, and DEGROSS books at a realised mean
      gross of 0.0375-0.15 with MaxDD -1.8% to -9.3% and CAGR 1.1-5.1%.  The k/n family therefore
      offers only TWO exposure regimes and nothing between them, so a book at the exposure that
      would clear both bars at once is not IN 887's grid to be found.  This arm adds it: the same
      selections held at a CONSTANT gross c.  PRE-REGISTERED BEFORE ANY c NUMBER IS READ — if any
      SMALL cell clears BOTH level legs at any c rung, the empty overlap is a GRID ARTEFACT of
      887's two constructions and not a panel property; if none does at any rung, it is the panel.
      c is a REPORTED axis (887's own `gross` axis widened downward), every rung published, and
      nothing is chosen on it except through the rule-8 IS-only chooser of P5.

 (P5) RULE 8.  The two tuned dials (m, FAMILY) are chosen on IS rows ONLY (eval start .. 2016-12-31)
      under three legal IS-only choosers declared here; 2017-2026 is read ONCE.  A chooser's pick
      is realised as the pre-declared SEED-0 draw at that (panel, m, family) so the pick names an
      implementable fixed list of tickers, never a seed average.  OOS CAGR/Sharpe/MaxDD reported
      against the sub-panel RULES v2 baseline and SPY.

COMMON WINDOW.  Every book, every baseline and SPY are scored on ONE calendar — the SMALL cache
starts 2010-01-04, so the evaluation window is SMALL.index[260] .. end, intersected with each
panel's own index.  Without this a "SMALL fails the CAGR floor" reading could be nothing but
U56 carrying the 2008-09 crash and SMALL not.  Rule 8's IS leg therefore begins in 2011, not
2009; that is stated rather than hidden.

SURVIVORSHIP (rule 9): U56 / B136 are current-constituent lists and SMALL is a current sub-$2B
screen, so every LEVEL is an upper bound.  What the run turns on is the GAP between panels at
matched size, and every panel inherits the same direction of bias.

Outputs (all committed):
  *.books.csv.gz      every book x cost rung: CAGR/Sharpe/MaxDD full, halves, IS, OOS, leg flags
  *.rates.csv        P1/P2: per (panel, m, constr) leg pass rates and the BOTH overlap
  *.calmar.csv       P3: the Calmar-ceiling predictor against the observed BOTH flag
  *.walkforward.csv  P5: rule-8 choosers, OOS read once
  *.gates.csv        gates, printed before any hypothesis is read
  *.console.txt      full console transcript
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, rebalance_mask  # noqa

STEM = Path(__file__).with_suffix("")
OUT = lambda ext: Path(str(STEM) + "." + ext)
_console = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s); _console.append(s)

# ---------------------------------------------------------------- fast backtest (887's, gated)
_CTX = {}
def ctx(px, freq):
    key = (id(px), freq)
    if key in _CTX: return _CTX[key]
    idx = px.index
    rets = px.pct_change().fillna(0.0).values
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cm = np.vstack([np.ones((1, N)), C])
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    s_idx = np.maximum.accumulate(np.where(mask, np.arange(T), -1))
    base = Cm[s_idx]
    A = Cm[:T] / base
    A1 = C / base
    _CTX[key] = (idx, T, N, s_idx, np.where(mask)[0], A, A1)
    return _CTX[key]

def fast_run(px, W, freq="W"):
    """Gross (pre-cost) daily returns + turnover; identical semantics to engine.backtest."""
    idx, T, N, s_idx, rb, A, A1 = ctx(px, freq)
    Wt = W.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    Wb = Wt[s_idx]
    E = Wb.sum(axis=1)
    V = (Wb * A).sum(axis=1) + (1.0 - E)
    V1 = (Wb * A1).sum(axis=1) + (1.0 - E)
    port = V1 / V - 1.0
    prev = np.zeros((T, N))
    ent = Wb[rb - 1] * A1[rb - 1] / np.where(V1[rb - 1] > 0, V1[rb - 1], 1.0)[:, None]
    prev[rb] = np.where((rb - 1 >= 0)[:, None], ent, 0.0)
    turn = np.zeros(T)
    turn[rb] = np.abs(Wt[rb] - prev[rb]).sum(axis=1)
    return pd.Series(port, index=idx), pd.Series(turn, index=idx)

def mets(r):
    eq = (1 + r).cumprod(); yrs = len(r) / 252.0
    cagr = eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan
    dd = float((eq / eq.cummax() - 1).min())
    vol = r.std() * np.sqrt(252)
    return cagr, (r.mean() * 252 / vol if vol else np.nan), dd

# ---------------------------------------------------------------- panels
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "max_1d_move" if "max_1d_move" in meta.columns else meta.columns[-1]
    tick = meta.columns[0]
    bad = set(meta.loc[meta[col] >= 1.0, tick].astype(str))
    return px[[c for c in px.columns if c == "SPY" or c not in bad]]

# ---------------------------------------------------------------- families / books
def signals(px):
    ma = px.rolling(200).mean()
    above = (px > ma) & px.notna()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3
    rnd = pd.DataFrame(np.random.default_rng(908).random(px.shape), index=px.index, columns=px.columns)
    return above, dict(MOM=comp, MADIST=px / ma - 1, VOLLO=-vol20, VOLHI=vol20, RAND=rnd)

def fam_ctx(px, above, stat):
    """Per-(sub-panel, family) invariants: eligibility, rank, eligible count."""
    ok = above & stat.notna()
    n_e = ok.sum(axis=1).astype(float)
    rank = stat.where(ok).rank(axis=1, ascending=False, method="first")
    return ok, n_e, rank

def book_weights(px, ok, n_e, rank, q, constr, gross):
    k = np.maximum(1.0, np.round(q * n_e)).where(n_e > 0, 0.0)
    sel = rank.le(k, axis=0) & ok
    kk = sel.sum(axis=1).astype(float)
    w = (gross / kk.replace(0, np.nan)) if constr == "RESPREAD" else (pd.Series(gross, index=px.index) / n_e.replace(0, np.nan))
    return sel.astype(float).mul(w, axis=0).fillna(0.0)

# ---------------------------------------------------------------- grid
QS      = [0.05, 0.10, 0.20, 0.30, 0.50, 1.00]
FAMS    = ["MOM", "MADIST", "VOLLO", "VOLHI", "RAND"]
# (construction, gross).  DEGROSS's realised exposure is already gross*k/n_e, so it needs no
# ladder; RESPREAD is walked DOWN the gross axis to supply the rung the k/n family omits (P6).
CONSTR  = [("RESPREAD", 0.75), ("DEGROSS", 0.75), ("RESPREAD", 0.50), ("RESPREAD", 0.375),
           ("RESPREAD", 0.25), ("RESPREAD", 0.15)]
RUNGS   = [10, 25]
GROSS, CADENCE = 0.75, "W"
SIZES   = {"U56": [14, 28], "B136": [14, 28, 55], "SMALL": [14, 28, 55, 110, 220]}   # + each panel's own FULL size, appended
NSEED   = 8
SPLIT   = pd.Timestamp("2017-01-01")
CALMAR_RATIO = 0.70 / 0.60

def draw(cols, m, panel_i, s):
    rng = np.random.default_rng([908, panel_i, m, s])
    return sorted(rng.choice(np.asarray(cols), size=m, replace=False).tolist())

def legs(cagr, sh, dd, h1, h2, oos_sh, oos_cagr, oos_dd, spy, bse):
    """PROTOCOL rule 4.  spy = dict of SPY stats; bse = dict of the sub-panel baseline's stats."""
    L_CAGR = cagr >= 0.70 * spy["cagr"]
    L_DD   = dd   >= 0.60 * spy["dd"]
    L_H1   = h1 > spy["h1"]; L_H2 = h2 > spy["h2"]; L_OOS = oos_sh > spy["oos_sh"]
    keep4b = bool(L_CAGR and L_DD and L_H1 and L_H2 and L_OOS)
    keep4a = bool(h1 > bse["h1"] and h2 > bse["h2"] and dd >= bse["dd"])
    return dict(L_CAGR=bool(L_CAGR), L_DD=bool(L_DD), L_H1=bool(L_H1), L_H2=bool(L_H2),
                L_OOS=bool(L_OOS), BOTH_LEVEL=bool(L_CAGR and L_DD), keep4b=keep4b, keep4a=keep4a)

def stats_of(r):
    split_i = int(r.index.searchsorted(SPLIT))
    c, s, d = mets(r)
    h = len(r) // 2
    _, h1, _ = mets(r.iloc[:h]); _, h2, _ = mets(r.iloc[h:])
    ci, si, di = mets(r.iloc[:split_i]); co, so, do = mets(r.iloc[split_i:])
    return dict(cagr=c, sh=s, dd=d, h1=h1, h2=h2, is_cagr=ci, is_sh=si, is_dd=di,
                oos_cagr=co, oos_sh=so, oos_dd=do,
                calmar=(c / abs(d) if d else np.nan), is_calmar=(ci / abs(di) if di else np.nan))

def main():
    t0 = time.time()
    say("# Idea 908 (lane B, 2026-09-19) — why is the k/n 4b LEG-OVERLAP empty on every SMALL block?")
    pans = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL": small_panel()}
    EVAL = pans["SMALL"].index[260]
    say(f"# common evaluation window starts {EVAL.date()} (SMALL cache row 260); IS = .. 2016-12-31, OOS = 2017-01-01 ..")

    # ------------------------------------------------- gates, before any hypothesis is read
    gates = []
    gp = pans["U56"]
    ab, sg = signals(gp); ok, n_e, rk = fam_ctx(gp, ab, sg["MOM"])
    Wg = book_weights(gp, ok, n_e, rk, 0.30, "RESPREAD", 0.75)
    ref = backtest(gp, Wg, cost_bps=10, freq="W"); fr, ft = fast_run(gp, Wg, "W")
    fin = np.isfinite(ref["returns"].values)
    d0 = float(np.abs(ref["returns"].values[fin] - (fr - ft * 10 / 1e4).values[fin]).max())
    gates.append(("G0 fast_run vs engine.backtest (MOM q0.30 RESPREAD g0.75 W, 10bps)", d0, "< 1e-12", d0 < 1e-12))
    fint = np.isfinite(ref["turnover"].values)
    d1 = float(np.abs(ref["turnover"].values[fint] - ft.values[fint]).max())
    gates.append(("G1 turnover fast_run vs engine.backtest", d1, "< 1e-12", d1 < 1e-12))
    Wb = rules_v2_weights(gp)
    rb_e = backtest(gp, Wb, cost_bps=10, freq="W")["returns"]; rb_f, rb_t = fast_run(gp, Wb, "W")
    fin2 = np.isfinite(rb_e.values)
    d2 = float(np.abs(rb_e.values[fin2] - (rb_f - rb_t * 10 / 1e4).values[fin2]).max())
    gates.append(("G2 fast_run vs engine.backtest on the LIVE book (RULES v2, U56)", d2, "< 1e-12", d2 < 1e-12))
    w1 = book_weights(gp, ok, n_e, rk, 1.00, "RESPREAD", 0.75)
    w2 = book_weights(gp, ok, n_e, rk, 1.00, "DEGROSS", 0.75)
    d3 = float(np.abs(w1.values - w2.values).max())
    gates.append(("G3 q=1.00 RESPREAD == DEGROSS (k == n_elig)", d3, "< 1e-12", d3 < 1e-12))
    e = w1.sum(axis=1)[ok.sum(axis=1) > 0]
    d4 = float(np.abs(e - GROSS).max())
    gates.append(("G4 RESPREAD realised gross exact on rankable-eligible days", d4, "< 1e-12", d4 < 1e-12))
    wd = book_weights(gp, ok, n_e, rk, 0.30, "DEGROSS", 0.75)
    d5 = float((wd.sum(axis=1) - GROSS).max())
    gates.append(("G5 DEGROSS never exceeds gross (no leverage)", d5, "<= 1e-12", d5 <= 1e-12))
    yrs = len(gp.loc[EVAL:]) / 252.0
    gates.append(("G6 evaluation window length (years, rule 1 min 10)", yrs, ">= 10", yrs >= 10))
    say("\n## GATES")
    for g in gates: say(f"  {'PASS' if g[3] else 'FAIL'}  {g[0]}: {g[1]:.6g}  (bar {g[2]})")
    pd.DataFrame(gates, columns=["gate", "value", "bar", "passed"]).to_csv(OUT("gates.csv"), index=False)
    if not all(g[3] for g in gates):
        say("!! a gate failed — results below are not to be trusted"); 

    # ------------------------------------------------- SPY bars, per panel calendar, common window
    SPYS = {}
    say("\n## SPY bars on the common window, on each panel's own trading calendar")
    for pname, pxf in pans.items():
        sr = pxf["SPY"].pct_change().fillna(0.0).loc[EVAL:]
        st = stats_of(sr)
        SPYS[pname] = dict(cagr=st["cagr"], dd=st["dd"], h1=st["h1"], h2=st["h2"], oos_sh=st["oos_sh"],
                           calmar=st["calmar"], is_calmar=st["is_calmar"], full=st)
        say(f"  {pname:5s} n={len(sr)}  CAGR {st['cagr']:.2%}  Sharpe {st['sh']:.4f}  MaxDD {st['dd']:.2%}  "
            f"halves {st['h1']:.4f}/{st['h2']:.4f}  OOS {st['oos_cagr']:.2%}/{st['oos_sh']:.4f}/{st['oos_dd']:.2%}  "
            f"Calmar {st['calmar']:.4f}")
        say(f"        4b bars: CAGR floor {0.70*st['cagr']:.2%}  DD cap {0.60*st['dd']:.2%}  "
            f"Calmar ceiling bar {CALMAR_RATIO*st['calmar']:.4f} (IS bar {CALMAR_RATIO*st['is_calmar']:.4f})")
    S = SPYS["SMALL"]["full"]

    # ------------------------------------------------- the grid
    rows = []
    for pi, (pname, px_full) in enumerate(pans.items()):
        inv = [c for c in px_full.columns if c != "SPY"]
        combos = [(m, s) for m in SIZES[pname] if m < len(inv) for s in range(NSEED)]
        combos += [(len(inv), 0)]                      # the panel itself, undrawn
        spy = SPYS[pname]
        for (m, s) in combos:
            cols = inv if m == len(inv) else draw(inv, m, pi, s)
            px = px_full[cols].copy()            # SPY is the benchmark only, never investable
            _CTX.clear()
            ab, sg = signals(px)
            # matched-universe baseline: RULES v2 on this same sub-panel
            bw = rules_v2_weights(px)
            br, bt = fast_run(px, bw, CADENCE)
            b10 = stats_of((br - bt * 10 / 1e4).loc[EVAL:])
            bse = dict(h1=b10["h1"], h2=b10["h2"], dd=b10["dd"])
            for fam in FAMS:
                ok, n_e, rk = fam_ctx(px, ab, sg[fam])
                for (constr, cg) in CONSTR:
                    label = constr if cg == 0.75 else f"{constr}@{cg:g}"
                    for q in QS:
                        W = book_weights(px, ok, n_e, rk, q, constr, cg)
                        gr, tu = fast_run(px, W, CADENCE)
                        for rung in RUNGS:
                            r = (gr - tu * rung / 1e4).loc[EVAL:]
                            st = stats_of(r)
                            lg = legs(st["cagr"], st["sh"], st["dd"], st["h1"], st["h2"],
                                      st["oos_sh"], st["oos_cagr"], st["oos_dd"], spy, bse)
                            rows.append(dict(panel=pname, m=m, seed=s, family=fam, constr=label, cg=cg, q=q,
                                             rung=rung, mean_gross=float(W.sum(axis=1).loc[EVAL:].mean()),
                                             **{k: st[k] for k in st}, **lg,
                                             base_sh=b10["sh"], base_dd=b10["dd"], base_h1=b10["h1"],
                                             base_h2=b10["h2"], base_cagr=b10["cagr"],
                                             base_oos_sh=b10["oos_sh"], base_oos_cagr=b10["oos_cagr"],
                                             base_oos_dd=b10["oos_dd"],
                                             calmar_pred=bool(st["calmar"] >= CALMAR_RATIO * spy["calmar"]),
                                             is_calmar_pred=bool(st["is_calmar"] >= CALMAR_RATIO * spy["is_calmar"])))
        say(f"  ... {pname} done ({len(rows)} rows, {time.time()-t0:.0f}s)")
    D = pd.DataFrame(rows)
    D.to_csv(OUT("books.csv.gz"), index=False, compression="gzip")
    say(f"\n## {len(D)} published cells ({D[D.rung==10].shape[0]} at the 10 bps headline rung)")

    H = D[D.rung == 10]

    # ------------------------------------------------- P1 / P2
    say("\n## (P1) LEG DECOMPOSITION — pass rates at 10 bps, pooled over families, q and seeds")
    rate = (H.groupby(["panel", "m", "constr"])
              .agg(n=("L_CAGR", "size"), r_CAGR=("L_CAGR", "mean"), r_DD=("L_DD", "mean"),
                   r_BOTH=("BOTH_LEVEL", "mean"), r_4b=("keep4b", "mean"), r_4a=("keep4a", "mean"),
                   med_calmar=("calmar", "median"))
              .reset_index())
    rate.to_csv(OUT("rates.csv"), index=False)
    say(rate.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n## (P1b) pooled over constr")
    pool = (H.groupby(["panel", "m"])
              .agg(n=("L_CAGR", "size"), r_CAGR=("L_CAGR", "mean"), r_DD=("L_DD", "mean"),
                   r_BOTH=("BOTH_LEVEL", "mean"), r_4b=("keep4b", "mean"), r_4a=("keep4a", "mean"),
                   med_calmar=("calmar", "median"), max_calmar=("calmar", "max")).reset_index())
    say(pool.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n## (P2) SIZE vs PANEL — the matched size m = 55")
    say("  A pass RATE is a fraction over a construction set, so ADDING constructions that rarely pass")
    say("  anywhere shrinks every rate and every DIFFERENCE between rates with it.  P2 was pre-registered")
    say("  on 887's OWN two constructions; it is read there FIRST, and then again over the full set")
    say("  including P6's post-hoc c ladder, so the dilution is visible rather than silently decisive.")
    for tag, sub in (("PRE-REGISTERED (887's two constructions: RESPREAD, DEGROSS)",
                      H[H.constr.isin(["RESPREAD", "DEGROSS"])]),
                     ("DILUTED (all six constructions, incl. P6's post-hoc c ladder)", H)):
        pl = (sub.groupby(["panel", "m"])
                 .agg(r_CAGR=("L_CAGR", "mean"), r_DD=("L_DD", "mean"), r_BOTH=("BOTH_LEVEL", "mean"),
                      med_calmar=("calmar", "median")).reset_index())
        m55 = pl[pl.m == 55].set_index("panel")
        say(f"\n  -- {tag}")
        for a in ("U56", "B136"):
            if a in m55.index and "SMALL" in m55.index:
                g = abs(m55.loc["SMALL", "r_BOTH"] - m55.loc[a, "r_BOTH"])
                say(f"     |BOTH(SMALL,55) - BOTH({a},55)| = |{m55.loc['SMALL','r_BOTH']:.4f} - "
                    f"{m55.loc[a,'r_BOTH']:.4f}| = {g:.4f}   -> "
                    f"{'H_SIZE (matched)' if g <= 0.10 else 'H_PANEL (gap survives matching)'}")
                say(f"        legs at m=55: L_CAGR SMALL {m55.loc['SMALL','r_CAGR']:.4f} vs {a} "
                    f"{m55.loc[a,'r_CAGR']:.4f}; L_DD SMALL {m55.loc['SMALL','r_DD']:.4f} vs {a} "
                    f"{m55.loc[a,'r_DD']:.4f}")
    say("\n  -- the LEVEL statistic, which no construction set can dilute: MEDIAN CALMAR at m = 55")
    for tag, sub in (("887's two", H[H.constr.isin(["RESPREAD", "DEGROSS"])]), ("all six", H)):
        pl = sub[sub.m == 55].groupby("panel").calmar.median()
        say(f"     {tag}: " + "  ".join(f"{k} {v:.4f}" for k, v in pl.items())
            + f"   (SMALL / U56 ratio {pl.get('SMALL', np.nan)/pl.get('U56', np.nan):.3f})")

    # ------------------------------------------------- P3
    say("\n## (P3) MECHANISM — Calmar ceiling vs the observed BOTH_LEVEL flag")
    cal = []
    for rung in RUNGS:
        d = D[D.rung == rung]
        agree = float((d.calmar_pred == d.BOTH_LEVEL).mean())
        tp = int(((d.calmar_pred) & (d.BOTH_LEVEL)).sum()); tn = int(((~d.calmar_pred) & (~d.BOTH_LEVEL)).sum())
        fp = int(((d.calmar_pred) & (~d.BOTH_LEVEL)).sum()); fn = int(((~d.calmar_pred) & (d.BOTH_LEVEL)).sum())
        den = np.sqrt(float((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn)))
        mcc = (tp*tn - fp*fn) / den if den > 0 else np.nan
        prec = tp / (tp + fp) if (tp + fp) else np.nan
        rec = tp / (tp + fn) if (tp + fn) else np.nan
        cal.append(dict(rung=rung, n=len(d), agree=agree, TP=tp, FP=fp, FN=fn, TN=tn, MCC=mcc,
                        precision=prec, recall=rec))
        say(f"  {rung} bps: agreement {agree:.4f}  recall {rec:.4f} (1.0000 expected: the bar is ALGEBRAICALLY "
            f"necessary)  precision {prec:.4f}  (TP {tp} FP {fp} FN {fn} TN {tn}, MCC {mcc:.4f})")
    pd.DataFrame(cal).to_csv(OUT("calmar.csv"), index=False)
    say("\n  (P3 decisive) per-panel MAX Calmar vs the 1.1667 x SPY ceiling — can the panel reach the overlap at all?")
    for p in pans:
        d = H[H.panel == p]
        say(f"    {p}: max Calmar {d.calmar.max():.4f}, share of cells over the bar {float(d.calmar_pred.mean()):.4f} "
            f"(bar {CALMAR_RATIO*SPYS[p]['calmar']:.4f})")

    # ------------------------------------------------- P4
    say("\n## (P4) BOTH KEEP PATHS over every published cell")
    say(f"  path 4a passes: {int(H.keep4a.sum())} of {len(H)} at 10 bps, {int(D[D.rung==25].keep4a.sum())} of "
        f"{len(D[D.rung==25])} at 25 bps")
    say(f"  path 4b passes: {int(H.keep4b.sum())} of {len(H)} at 10 bps, {int(D[D.rung==25].keep4b.sum())} of "
        f"{len(D[D.rung==25])} at 25 bps")
    if H.keep4b.any():
        say("  4b passers at 10 bps:")
        say(H[H.keep4b][["panel","m","seed","family","constr","q","cagr","sh","dd","oos_sh","calmar"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    if H.keep4a.any():
        say(f"  4a passers at 10 bps by panel: {H[H.keep4a].groupby('panel').size().to_dict()}")

    # ------------------------------------------------- P6 the missing rung
    say("\n## (P6) THE MISSING RUNG — the same selections held at a CONSTANT gross c")
    mr = (H.groupby(["panel", "constr"])
            .agg(n=("L_CAGR", "size"), r_CAGR=("L_CAGR", "mean"), r_DD=("L_DD", "mean"),
                 r_BOTH=("BOTH_LEVEL", "mean"), r_4b=("keep4b", "mean"), r_4a=("keep4a", "mean"),
                 med_cagr=("cagr", "median"), med_dd=("dd", "median"), max_calmar=("calmar", "max"))
            .reset_index())
    say(mr.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    sm = H[(H.panel == "SMALL") & (H.BOTH_LEVEL)]
    say(f"\n  SMALL cells clearing BOTH level legs, over the whole c ladder: {len(sm)} of "
        f"{len(H[H.panel=='SMALL'])}  -> "
        f"{'GRID ARTEFACT of 887 two constructions' if len(sm) else 'A PANEL PROPERTY (no rung clears both)'}")
    if len(sm):
        say(sm[["m","seed","family","constr","q","cagr","sh","dd","h1","h2","oos_sh","oos_cagr","oos_dd",
                "calmar","mean_gross","keep4b","keep4a"]]
            .sort_values("sh", ascending=False).to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    sm.to_csv(OUT("small_both.csv"), index=False)
    # the lone SMALL 4b passer: does it survive the cost rung, and can rule 8 REACH it?
    win = H[(H.panel == "SMALL") & (H.keep4b)]
    say(f"\n  SMALL cells clearing the WHOLE of 4b at 10 bps: {len(win)} of {len(H[H.panel=='SMALL'])}")
    for _, w in win.iterrows():
        sp = SPYS["SMALL"]
        say(f"    {w.family} {w.constr} q={w.q:g} m={int(w.m)} seed={int(w.seed)}: margins vs the bars — "
            f"CAGR {w.cagr:.2%} over {0.70*sp['cagr']:.2%} (+{100*(w.cagr-0.70*sp['cagr']):.2f} pp), "
            f"MaxDD {w.dd:.2%} inside {0.60*sp['dd']:.2%} (+{100*(w.dd-0.60*sp['dd']):.2f} pp), "
            f"H1 +{w.h1-sp['h1']:.4f}, H2 +{w.h2-sp['h2']:.4f}, OOS Sharpe +{w.oos_sh-sp['oos_sh']:.4f}")
        tw = D[(D.rung == 25) & (D.panel == w.panel) & (D.m == w.m) & (D.seed == w.seed) &
               (D.family == w.family) & (D.constr == w.constr) & (D.q == w.q)]
        if len(tw):
            u = tw.iloc[0]
            say(f"      at 25 bps: CAGR {u.cagr:.2%} Sharpe {u.sh:.4f} MaxDD {u.dd:.2%} -> 4b "
                f"{'PASS' if u.keep4b else 'FAIL'} (L_CAGR {u.L_CAGR}, L_DD {u.L_DD})")

    # ------------------------------------------------- P5 rule 8
    say("\n## (P5) RULE 8 — (m, FAMILY) chosen on IS rows only, 2017-2026 read ONCE, seed-0 draw realised")
    wf = []
    S0 = H[H.seed == 0]
    for pname in pans:
        for constr in sorted(S0.constr.unique()):
            for qv in QS:
                d = S0[(S0.panel == pname) & (S0.constr == constr) & (S0.q == qv)]
                if d.empty: continue
                picks = {
                    "C_IS_SHARPE": d.loc[d.is_sh.idxmax()],
                    "C_IS_CALMAR": d.loc[d.is_calmar.idxmax()],
                    "C_IS_LEVEL":  d.assign(k=d.is_calmar_pred.astype(int)).sort_values(
                                       ["k", "is_sh"], ascending=False).iloc[0],
                }
                for cname, row in picks.items():
                    wf.append(dict(panel=pname, constr=constr, q=qv, chooser=cname,
                                   m=int(row.m), family=row.family,
                                   oos_cagr=row.oos_cagr, oos_sh=row.oos_sh, oos_dd=row.oos_dd,
                                   base_oos_sh=row.base_oos_sh, base_oos_cagr=row.base_oos_cagr,
                                   spy_oos_sh=SPYS[pname]["oos_sh"],
                                   beats_base=bool(row.oos_sh > row.base_oos_sh),
                                   beats_spy=bool(row.oos_sh > SPYS[pname]["oos_sh"]),
                                   keep4b=bool(row.keep4b), keep4a=bool(row.keep4a),
                                   L_CAGR=bool(row.L_CAGR), L_DD=bool(row.L_DD)))
    W = pd.DataFrame(wf)
    W.to_csv(OUT("walkforward.csv"), index=False)
    say(f"  {len(W)} (panel, constr, q, chooser) picks")
    say(W.groupby(["panel", "chooser"]).agg(n=("m", "size"), mean_m=("m", "mean"),
                                            mean_oos_sh=("oos_sh", "mean"), mean_oos_cagr=("oos_cagr", "mean"),
                                            mean_oos_dd=("oos_dd", "mean"), n4b=("keep4b", "sum"),
                                            n4a=("keep4a", "sum"), n_beat_base=("beats_base", "sum"),
                                            n_beat_spy=("beats_spy", "sum")).to_string(float_format=lambda x: f"{x:.4f}"))
    say(f"  picked m distribution: {W.m.value_counts().sort_index().to_dict()}")
    say(f"  picked family distribution: {W.family.value_counts().to_dict()}")
    ws = W[W.panel == "SMALL"]
    say(f"  REACHABILITY on SMALL: {int(ws.keep4b.sum())} of {len(ws)} IS-only picks clear 4b; "
        f"{int(ws.beats_spy.sum())} of {len(ws)} beat SPY's OOS Sharpe ({SPYS['SMALL']['oos_sh']:.4f}); "
        f"mean OOS Sharpe of the picks {ws.oos_sh.mean():.4f}.")
    for _, w in H[(H.panel == "SMALL") & (H.keep4b)].iterrows():
        hit = ws[(ws.constr == w.constr) & (ws.q == w.q) & (ws.m == w.m) & (ws.family == w.family)]
        say(f"  the 4b cell ({w.family} {w.constr} q={w.q:g} m={int(w.m)}) is reached by "
            f"{len(hit)} of the {len(ws[(ws.constr==w.constr)&(ws.q==w.q)])} choosers that could name it.")

    say(f"\n# done in {time.time()-t0:.0f}s")
    OUT("console.txt").write_text("\n".join(_console) + "\n")

if __name__ == "__main__":
    main()
