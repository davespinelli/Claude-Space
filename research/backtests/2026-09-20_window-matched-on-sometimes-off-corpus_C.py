#!/usr/bin/env python3
"""Idea 1738 (lane C, 2026-09-20): is the WINDOW-MATCHED 4a test TESTABLE on a SOMETIMES-OFF corpus?

Idea 1631 priced three restatements of PROTOCOL rule 4a and could not adjudicate restatement (i)
-- the WINDOW-MATCHED one -- because its corpus had no variance on the only axis that matters:
every committed book differs from the incumbent on ~100% of days (diff-share 1.000 on 44 of 52
cells; act-share 1.000 on 50 of 52, the two SPYFILT rungs aside).  A window-matched test can only
differ from a full-window test when the window is genuinely SHORTER, so 1631's verdict on (i) was
a statement about its corpus, not about the restatement.

This run builds the corpus 1631 lacked and re-runs the same two tests on it.

  CORPUS.  Four SWITCH families -- SPYFILT / STOP / BREADTH / VOLTGT, the four the idea names --
  each a causal market-state statistic x_t.  A switch is ON when x_t > q, where q is the quantile
  of x on the IS window (2009-2016) that puts the ON-share at a TARGET s.  Sweeping
  s = 0.30 .. 0.90 dials the deployed share directly, which is the whole point of the run.
  Two ARMS turn a switch into a book:
     CASH    : hold the incumbent's book when ON, sit in CASH when OFF
               -> act-share  = s   (deployed on s of days), diff-share = 1 - s
     OVER(f) : BE the incumbent when OFF, hold f x the incumbent's book when ON
               -> diff-share = s   (differs from the incumbent on s of days), act-share = 1
  So act-share and diff-share each span 0.3-0.9 by construction, complementarily, which is the
  variance 1631's corpus did not have.  A NULL switch (seeded uniform noise, same share, no
  information) is carried at every share on both arms.

  TESTS (identical arithmetic to 1631's, only the corpus changes)
    R0  CURRENT       : Sharpe > RULES v2 in BOTH calendar halves AND MaxDD >= baseline (full).
    R1a ACTIVE_GROSS  : the same three legs, computed on the days the device is DEPLOYED.
    R1b ACTIVE_DIFF   : the same three legs, computed on the days the device's BOOK DIFFERS
                        from the incumbent's (elsewhere it IS the incumbent, so those days add
                        only shared tape).
  A window is declared UNADJUDICABLE, and the test FAILS, when it holds fewer than MINN days.

  EXACTLY TWO TUNED PARAMETERS, every grid point reported:
    MINN  in {250, 500, 750, 1000, 1500}   the minimum adjudicable window length
    f     in {0.25, 0.50, 0.75}            the OVER arm's overlay strength
  The share ladder s is the idea's own x-AXIS (the corpus being adjudicated), not a knob; f=1.00
  is carried as a CONTROL rung (it must reproduce the incumbent exactly -- gate G5).

  RULE 8.  (MINN, f) are fixed on 2009-2016 rows alone; each test is then used as a CHOOSER on
  those IS rows (argmax IS Sharpe among the books it passes) and the book it picks is read ONCE
  on 2017-2026, against RULES v2 OOS and SPY OOS, on BOTH KEEP paths.

Protocol: 10 bps (rule 2), next-day execution (engine), weekly cadence, no leverage, no shorting.
Panels U56 / B136 / SMALL.  SURVIVORSHIP (rule 9): all three are CURRENT constituents, so levels
are upper bounds; every claim here is a CONTRAST between books on the same tape.
Price-only.  No EDGAR / Form 4 / 8-K / options / live data.  Deterministic, offline, standalone:
    python3 research/backtests/2026-09-20_window-matched-on-sometimes-off-corpus_C.py
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa
from engine import backtest  # noqa

pd.set_option("display.width", 230)
pd.set_option("display.max_rows", 400)
T0 = time.time()

COST = 10.0                 # protocol rule 2
FREQ = "W"                  # live cadence
GROSS = 0.75                # live gross
BAND = 0.03                 # live band
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SHARES = (0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90)      # the idea's x-axis (corpus)
MINN_GRID = (250, 500, 750, 1000, 1500)                  # tuned parameter 1 of 2
PHI_GRID = (0.25, 0.50, 0.75)                            # tuned parameter 2 of 2
PHI_CTRL = 1.00                                          # control rung, gate G5
NULL_SEEDS = (0, 1)

OUT = []
def say(s=""):
    print(s); OUT.append(str(s))

GATES = []
def gate(name, got, want, ok):
    GATES.append((name, str(got), str(want), bool(ok)))

# ------------------------------------------------------------------ metric helpers
def sh(r):
    v = r.std() * np.sqrt(252)
    return float((r.mean() * 252) / v) if v else np.nan

def mdd(r):
    eq = (1 + r).cumprod()
    return float((eq / eq.cummax() - 1).min())

def cagr(r):
    eq = (1 + r).cumprod(); y = len(r) / 252.0
    return float(eq.iloc[-1] ** (1 / y) - 1) if y > 0 else np.nan

def at_cost(r0, to, c):
    return r0 - to * c / 1e4

# ------------------------------------------------------------------ switch statistics
def stat_spyfilt(px, b0):
    s = px["SPY"]
    return s / s.rolling(200).mean() - 1.0                    # ON when SPY is far above its MA

def stat_stop(px, b0):
    eq = (1 + b0).cumprod()
    return eq / eq.rolling(63, min_periods=1).max() - 1.0     # ON when the book is NOT in drawdown

def stat_breadth(px, b0):
    bs = band_state(px, BAND) & px.notna()
    n = px.notna().sum(axis=1).replace(0, np.nan)
    return (bs.sum(axis=1) / n).fillna(0.0)                   # ON when breadth is wide

def stat_voltgt(px, b0):
    rp = px.pct_change().mean(axis=1)
    return -(rp.rolling(20).std() * np.sqrt(252))             # ON when panel vol is LOW

def stat_null(seed):
    def f(px, b0):
        rng = np.random.default_rng(seed)
        return pd.Series(rng.random(len(px.index)), index=px.index)   # no information at all
    return f

FAMILIES = [("SPYFILT", stat_spyfilt, False), ("STOP", stat_stop, False),
            ("BREADTH", stat_breadth, False), ("VOLTGT", stat_voltgt, False)] + \
           [(f"NULLSW s={s}", stat_null(s), True) for s in NULL_SEEDS]

def on_state(x, s, is_mask):
    """ON when x > q, q = the IS-window quantile of x putting the ON-share at s.  NaN -> OFF."""
    xi = x[is_mask].dropna()
    q = float(np.nanquantile(xi.values, 1.0 - s)) if len(xi) else np.inf
    return (x > q).fillna(False), q

# ------------------------------------------------------------------ the two window-matched tests
def legs(r, b):
    h = len(r) // 2
    return (sh(r.iloc[:h]) > sh(b.iloc[:h]), sh(r.iloc[h:]) > sh(b.iloc[h:]), mdd(r) >= mdd(b))

def test_4a(r, b, mask=None, minn=0):
    """rule 4a on a window.  mask=None -> the FULL window (R0)."""
    if mask is not None:
        r, b = r[mask], b[mask]
        if len(r) < minn:
            return False, len(r)
    h1, h2, dd = legs(r, b)
    return bool(h1 and h2 and dd), len(r)

BLOCK, NDRAW, BSEED = 63, 400, 20260920      # inherited conventions (idea 1511 LB=65, 1709 2 SE)

def paired_block_t(e):
    """t of the mean of a paired difference stream under a circular block bootstrap.
    Block length and draw count are the record's INHERITED conventions, not tuned parameters."""
    n = len(e)
    if n < 2 * BLOCK or e.std() == 0:
        return np.nan
    v = e.values if hasattr(e, "values") else np.asarray(e)
    rng = np.random.default_rng(BSEED)
    nb = int(np.ceil(n / BLOCK))
    st = rng.integers(0, n, size=(NDRAW, nb))
    idx = (st[:, :, None] + np.arange(BLOCK)[None, None, :]).reshape(NDRAW, nb * BLOCK)[:, :n] % n
    se = float(v[idx].mean(axis=1).std(ddof=1))
    return float(v.mean() / se) if se > 0 else np.nan

def window_diag(r, b, mask, tag):
    """Everything the window-matched test sees on ITS OWN window, so the verdict is explainable."""
    rw, bw = r[mask], b[mask]
    d = {f"{tag}_n": int(len(rw))}
    if len(rw) < 2:
        return {**d, f"{tag}_S_dev": np.nan, f"{tag}_S_base": np.nan, f"{tag}_dS": np.nan,
                f"{tag}_zerovar": True, f"{tag}_dMaxDD_pp": np.nan, f"{tag}_legH1": False,
                f"{tag}_legH2": False, f"{tag}_legDD": False, f"{tag}_t_excess": np.nan}
    h = len(rw) // 2
    zv = bool(rw.std() == 0)
    d.update({f"{tag}_S_dev": sh(rw), f"{tag}_S_base": sh(bw), f"{tag}_dS": sh(rw) - sh(bw),
              f"{tag}_zerovar": zv, f"{tag}_dMaxDD_pp": (mdd(rw) - mdd(bw)) * 100,
              f"{tag}_legH1": bool(sh(rw.iloc[:h]) > sh(bw.iloc[:h])),
              f"{tag}_legH2": bool(sh(rw.iloc[h:]) > sh(bw.iloc[h:])),
              f"{tag}_legDD": bool(mdd(rw) >= mdd(bw)),
              f"{tag}_t_excess": paired_block_t(rw - bw)})
    return d

def keep4b(r, spy):
    h = len(r) // 2
    return bool(sh(r.iloc[:h]) > sh(spy.iloc[:h]) and sh(r.iloc[h:]) > sh(spy.iloc[h:])
                and mdd(r) >= 0.60 * mdd(spy) and cagr(r) >= 0.70 * cagr(spy))

# ------------------------------------------------------------------ main
def main():
    # ---- panels (SMALL built exactly as the record's committed convention)
    panels = [("U56", load_universe()), ("B136", load_universe(broad=True))]
    px_s = load_universe(small=True)
    meta_path = ROOT / "data" / "small_meta.csv"
    dropped_meta = []
    if meta_path.exists():
        meta = pd.read_csv(meta_path); tcol = meta.columns[0]
        if "max_1d_move" in meta.columns:
            dropped_meta = [t for t in meta.loc[meta["max_1d_move"] >= 1.0, tcol].astype(str)
                            if t in px_s.columns and t != "SPY"]
    mx = px_s.pct_change().abs().max()
    dropped_px = [c for c in px_s.columns if c != "SPY" and mx[c] >= 1.0]
    px_s = px_s.drop(columns=sorted(set(dropped_meta) | set(dropped_px)))
    panels.append(("SMALL", px_s))

    say("=" * 118)
    say("IDEA 1738 (lane C, 2026-09-20) - IS THE WINDOW-MATCHED 4a TEST TESTABLE ON A SOMETIMES-OFF CORPUS?")
    say("=" * 118)
    say(f"  cost {COST:.0f} bps, cadence {FREQ}, gross {GROSS}, band {BAND}, t+1 execution, long-only, no leverage.")
    say(f"  share ladder (corpus x-axis) {SHARES}")
    say(f"  TUNED 1/2  MINN {MINN_GRID}      TUNED 2/2  f {PHI_GRID}   (control rung f={PHI_CTRL:.2f})")
    say(f"  IS 2009-{IS_END[:4]} chooses; OOS {OOS_START[:4]}-2026 read once.")
    for nm, p in panels:
        say(f"  PANEL {nm:6s} {p.shape[1]:4d} cols incl. SPY  {p.index[0].date()}..{p.index[-1].date()}  "
            f"{len(p)} rows ({len(p)/252:.1f}y)")
        gate(f"G0 {nm} sample >= 10y (rule 1)", f"{len(p)/252:.1f}y", ">= 10.0y", len(p) / 252.0 >= 10.0)
    say("  SURVIVORSHIP (rule 9): current-constituent panels; absolute levels are UPPER BOUNDS, "
        "every claim below is a CONTRAST on one tape.")

    rows, chooser_rows = [], []
    picks_store = {}

    for pname, px in panels:
        start = px.index[260]                                     # warm-up, as baseline.compare()
        spy_full = px["SPY"].pct_change().fillna(0.0)
        Btgt = rules_v2_weights(px, band=BAND, gross=GROSS)
        bres = backtest(px, Btgt, cost_bps=0.0, freq=FREQ)
        b0, bto, bW = bres["returns"], bres["turnover"], bres["weights"]
        b = at_cost(b0, bto, COST).loc[start:]
        spy = spy_full.loc[start:]

        # ---- G1 the cost axis is exact off the zero-cost rung;  G2 baseline IS the live book
        chk = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"]
        gate(f"G1 cost axis exact ({pname})", f"{float(np.abs(at_cost(b0, bto, COST) - chk).max()):.2e}",
             "< 1e-12", float(np.abs(at_cost(b0, bto, COST) - chk).max()) < 1e-12)
        gate(f"G2 baseline == live rules_v2 ({pname})",
             f"{float(np.abs(b - chk.loc[start:]).max()):.2e}", "< 1e-12",
             float(np.abs(b - chk.loc[start:]).max()) < 1e-12)

        is_mask_full = px.index <= pd.Timestamp(IS_END)
        is_mask_full = pd.Series(is_mask_full & (px.index >= start), index=px.index)

        # ---------------------------------------------------- build + run the corpus
        books = []            # (name, family, is_null, arm, target_s, phi, weights)
        for fam, statf, is_null in FAMILIES:
            x = statf(px, b0)
            for s in SHARES:
                ON, q = on_state(x, s, is_mask_full)
                ONd = pd.DataFrame(np.repeat(ON.values[:, None], px.shape[1], axis=1),
                                   index=px.index, columns=px.columns)
                arms = [("CASH", np.nan, Btgt.where(ONd, 0.0))]
                phis = list(PHI_GRID) + ([PHI_CTRL] if (fam == "SPYFILT" and abs(s - 0.50) < 1e-9) else [])
                if is_null: phis = [0.50]
                for f_ in phis:
                    arms.append((f"OVER f={f_:.2f}", f_, Btgt.where(~ONd, Btgt * f_)))
                if is_null: arms = [arms[0], arms[1]]
                for arm, f_, W in arms:
                    books.append((f"{fam} | {arm} | s={s:.2f}", fam, is_null, arm, s, f_, W, q))

        say(f"\n[{pname}] running {len(books)} books ... ({time.time()-T0:.0f}s elapsed)")
        rets = {}
        for name, fam, is_null, arm, s, f_, W, q in books:
            res = backtest(px, W, cost_bps=0.0, freq=FREQ)
            r = at_cost(res["returns"], res["turnover"], COST).loc[start:]
            gr = res["weights"].sum(axis=1).loc[start:]
            dif = (res["weights"] - bW).abs().sum(axis=1).loc[start:]
            act = pd.Series(gr.values > 1e-9, index=r.index)
            dff = pd.Series(dif.values > 1e-9, index=r.index)
            rets[name] = dict(r=r, act=act, dff=dff, fam=fam, null=is_null, arm=arm, s=s, phi=f_,
                              maxgross=float(gr.max()), q=q,
                              tpy=float(res["turnover"].loc[start:].sum() / (len(r) / 252.0)))

        # ---- G3 the corpus really is SOMETIMES OFF on both axes
        A = np.array([v["act"].mean() for v in rets.values()])
        D = np.array([v["dff"].mean() for v in rets.values()])
        gate(f"G3a act-share spans 0.3-0.9 ({pname})", f"[{A.min():.3f}, {A.max():.3f}]",
             "min<=0.35 and max>=0.85", A.min() <= 0.35 and A.max() >= 0.85)
        gate(f"G3b diff-share spans 0.3-0.9 ({pname})", f"[{D.min():.3f}, {D.max():.3f}]",
             "min<=0.35 and max>=0.85", D.min() <= 0.35 and D.max() >= 0.85)
        gate(f"G4 no leverage ({pname})", f"{max(v['maxgross'] for v in rets.values()):.4f}",
             "<= 1.0", max(v["maxgross"] for v in rets.values()) <= 1.0 + 1e-9)
        ctrl = [k for k in rets if k.startswith("SPYFILT | OVER f=1.00")]
        if ctrl:
            d = float(np.abs(rets[ctrl[0]]["r"] - b).max())
            gate(f"G5 OVER f=1.00 reproduces the incumbent ({pname})", f"{d:.2e}", "< 1e-12", d < 1e-12)

        # ---------------------------------------------------- score every book, every grid point
        for name, v in rets.items():
            r = v["r"]
            row = dict(panel=pname, book=name, family=v["fam"], null=v["null"], arm=v["arm"],
                       target_s=v["s"], phi=v["phi"], act_share=float(v["act"].mean()),
                       diff_share=float(v["dff"].mean()), turnover_pa=v["tpy"],
                       CAGR=cagr(r), Sharpe=sh(r), MaxDD=mdd(r),
                       H1=sh(r.iloc[:len(r)//2]), H2=sh(r.iloc[len(r)//2:]),
                       n_act=int(v["act"].sum()), n_diff=int(v["dff"].sum()))
            row["R0_CURRENT"], _ = test_4a(r, b)
            for mn in MINN_GRID:
                row[f"R1a_MINN={mn}"], _ = test_4a(r, b, v["act"].values, mn)
                row[f"R1b_MINN={mn}"], _ = test_4a(r, b, v["dff"].values, mn)
            row.update(window_diag(r, b, v["act"].values, "W_ACT"))
            row.update(window_diag(r, b, v["dff"].values, "W_DIFF"))
            row["R0_legH1"] = bool(sh(r.iloc[:len(r)//2]) > sh(b.iloc[:len(b)//2]))
            row["R0_legH2"] = bool(sh(r.iloc[len(r)//2:]) > sh(b.iloc[len(b)//2:]))
            row["R0_legDD"] = bool(mdd(r) >= mdd(b))
            row["KEEP4b_FULL"] = keep4b(r, spy)
            ro, bo, so = r.loc[OOS_START:], b.loc[OOS_START:], spy.loc[OOS_START:]
            row["R0_OOS"], _ = test_4a(ro, bo)
            row["KEEP4b_OOS"] = keep4b(ro, so)
            row["OOS_CAGR"], row["OOS_Sharpe"], row["OOS_MaxDD"] = cagr(ro), sh(ro), mdd(ro)
            rows.append(row)

        # ---------------------------------------------------- rule 8: IS-only choice of (MINN, f)
        isr = lambda x: x.loc[:IS_END]
        b_is, b_oos = isr(b), b.loc[OOS_START:]
        spy_is, spy_oos = isr(spy), spy.loc[OOS_START:]
        n_is = len(b_is)
        is_v = {}
        for name, v in rets.items():
            r_is = isr(v["r"]); a_is = v["act"].values[:n_is]; d_is = v["dff"].values[:n_is]
            e = dict(IS_Sharpe=sh(r_is))
            e["R0"], _ = test_4a(r_is, b_is)
            for mn in MINN_GRID:
                e[f"R1a_{mn}"], e[f"n_a_{mn}"] = test_4a(r_is, b_is, a_is, mn)
                e[f"R1b_{mn}"], e[f"n_d_{mn}"] = test_4a(r_is, b_is, d_is, mn)
            is_v[name] = e

        # G6: no chooser statistic may read a 2017+ row (hard-truncated replay must be identical)
        g6 = 0.0
        for name in list(rets)[:8]:
            v = rets[name]
            hard_r = v["r"].iloc[:n_is].copy()
            e2 = dict(IS_Sharpe=sh(hard_r))
            e2["R0"], _ = test_4a(hard_r, b_is.iloc[:n_is])
            for mn in MINN_GRID:
                e2[f"R1a_{mn}"], _ = test_4a(hard_r, b_is.iloc[:n_is], v["act"].values[:n_is], mn)
                e2[f"R1b_{mn}"], _ = test_4a(hard_r, b_is.iloc[:n_is], v["dff"].values[:n_is], mn)
            for k in e2:
                g6 = max(g6, abs(float(e2[k]) - float(is_v[name][k])))
        gate(f"G6 chooser reads no 2017+ row ({pname})", f"{g6:.2e}", "== 0", g6 == 0.0)

        # MINN* : the TIGHTEST (largest) MINN that is still not needed -- chosen IS-only as the
        #         SMALLEST rung admitting NO NULL book under R1b on IS rows.
        real_is = [n for n, v in rets.items() if not v["null"] and v["phi"] != PHI_CTRL]
        null_is = [n for n, v in rets.items() if v["null"]]
        MINN_STAR = MINN_GRID[-1]
        for mn in MINN_GRID:
            if not any(is_v[n][f"R1b_{mn}"] for n in null_is):
                MINN_STAR = mn; break
        # f* : the overlay rung whose R1b-chosen book has the highest IS Sharpe (IS rows only)
        def pick(names, key):
            c = [n for n in names if is_v[n][key]]
            return max(c, key=lambda n: is_v[n]["IS_Sharpe"]) if c else None
        best_f, best_v, rule_used = PHI_GRID[0], -np.inf, "R1b"
        for f_ in PHI_GRID:
            sub = [n for n in real_is if (rets[n]["phi"] == f_ or rets[n]["arm"] == "CASH")]
            p = pick(sub, f"R1b_{MINN_STAR}")
            val = is_v[p]["IS_Sharpe"] if p else -np.inf
            if val > best_v: best_v, best_f = val, f_
        if not np.isfinite(best_v):
            # R1b identifies NO book on IS at any f, so it cannot choose f either.  Documented
            # IS-only fallback: choose f by the CURRENT rule (R0) instead, and say so.
            rule_used = "R0 (R1b unidentified)"
            for f_ in PHI_GRID:
                sub = [n for n in real_is if (rets[n]["phi"] == f_ or rets[n]["arm"] == "CASH")]
                p = pick(sub, "R0")
                val = is_v[p]["IS_Sharpe"] if p else -np.inf
                if val > best_v: best_v, best_f = val, f_
        PHI_STAR = best_f
        say(f"[{pname}] rule-8 IS-only tuned params: MINN* = {MINN_STAR}, f* = {PHI_STAR:.2f} "
            f"(chosen by {rule_used}; IS Sharpe of its pick {best_v:.4f})")

        # every grid point as a chooser (all MINN x f x test), the (MINN*, f*) row is the deliverable
        for mn in MINN_GRID:
            for f_ in PHI_GRID:
                sub = [n for n in real_is if (rets[n]["phi"] == f_ or rets[n]["arm"] == "CASH")]
                for tag, key in (("R0_CURRENT", "R0"), ("R1a_ACTIVE_GROSS", f"R1a_{mn}"),
                                 ("R1b_ACTIVE_DIFF", f"R1b_{mn}")):
                    p = pick(sub, key)
                    n_null = int(sum(is_v[n][key] for n in null_is))
                    if p is None:
                        chooser_rows.append(dict(panel=pname, MINN=mn, phi=f_, test=tag,
                                                 picked="(none passes IS)", n_is_pass=0, n_is_NULL=n_null,
                                                 OOS_CAGR=np.nan, OOS_Sharpe=np.nan, OOS_MaxDD=np.nan,
                                                 OOS_4a=False, OOS_4b=False,
                                                 star=(mn == MINN_STAR and abs(f_ - PHI_STAR) < 1e-9)))
                        continue
                    ro = rets[p]["r"].loc[OOS_START:]
                    p4a, _ = test_4a(ro, b_oos)
                    chooser_rows.append(dict(panel=pname, MINN=mn, phi=f_, test=tag, picked=p,
                                             n_is_pass=int(sum(is_v[n][key] for n in sub)),
                                             n_is_NULL=n_null, OOS_CAGR=cagr(ro), OOS_Sharpe=sh(ro),
                                             OOS_MaxDD=mdd(ro), OOS_4a=p4a, OOS_4b=keep4b(ro, spy_oos),
                                             star=(mn == MINN_STAR and abs(f_ - PHI_STAR) < 1e-9)))
        for tag, rr in (("-- RULES v2 baseline --", b_oos), ("-- SPY --", spy_oos)):
            chooser_rows.append(dict(panel=pname, MINN=-1, phi=np.nan, test=tag, picked="",
                                     n_is_pass=-1, n_is_NULL=-1, OOS_CAGR=cagr(rr), OOS_Sharpe=sh(rr),
                                     OOS_MaxDD=mdd(rr), OOS_4a=False, OOS_4b=False, star=False))
        picks_store[pname] = dict(MINN=MINN_STAR, phi=PHI_STAR,
                                  b_oos=(cagr(b_oos), sh(b_oos), mdd(b_oos)),
                                  spy_oos=(cagr(spy_oos), sh(spy_oos), mdd(spy_oos)),
                                  b_full=(cagr(b), sh(b), mdd(b)), spy_full=(cagr(spy), sh(spy), mdd(spy)))

    df = pd.DataFrame(rows); ch = pd.DataFrame(chooser_rows)
    csv = ROOT / "research" / "backtests" / "2026-09-20_window-matched-on-sometimes-off-corpus_C.csv"
    df.to_csv(csv, index=False)
    ch.to_csv(str(csv).replace(".csv", "_choosers.csv"), index=False)

    real = df[(~df.null) & (df.phi != PHI_CTRL)]
    nul = df[df.null]

    # ---------------------------------------------------------------- 1. the corpus has variance
    say("\n" + "=" * 118)
    say("1. THE CORPUS 1631 DID NOT HAVE.  Realised deployed shares (1631: act 1.000 on 50/52, diff 1.000 on 44/52)")
    say("=" * 118)
    piv = real.pivot_table(index=["arm"], columns="target_s", values=["act_share", "diff_share"], aggfunc="mean")
    say(piv.to_string(float_format=lambda x: f"{x:.3f}"))
    say(f"\n  act-share  range over all {len(df)} cells: {df.act_share.min():.3f} .. {df.act_share.max():.3f}"
        f"   (cells strictly inside (0.05,0.95): {int(((df.act_share>0.05)&(df.act_share<0.95)).sum())})")
    say(f"  diff-share range over all {len(df)} cells: {df.diff_share.min():.3f} .. {df.diff_share.max():.3f}"
        f"   (cells strictly inside (0.05,0.95): {int(((df.diff_share>0.05)&(df.diff_share<0.95)).sum())})")

    # ---------------------------------------------------------------- 2. every grid point
    say("\n" + "=" * 118)
    say("2. ALL GRID POINTS.  4a pass counts and verdict MOVES vs R0, real books and NULLs.")
    say("=" * 118)
    rep = []
    for tag, keyf in (("R0_CURRENT", lambda mn: "R0_CURRENT"),
                      ("R1a_ACTIVE_GROSS", lambda mn: f"R1a_MINN={mn}"),
                      ("R1b_ACTIVE_DIFF", lambda mn: f"R1b_MINN={mn}")):
        for mn in (MINN_GRID if tag != "R0_CURRENT" else (MINN_GRID[0],)):
            k = keyf(mn)
            rep.append(dict(test=tag, MINN=(mn if tag != "R0_CURRENT" else "-"),
                            pass_real=int(real[k].sum()), of_real=len(real),
                            pass_NULL=int(nul[k].sum()), of_NULL=len(nul),
                            moved_fail_to_pass=int((real[k] & ~real.R0_CURRENT).sum()),
                            moved_pass_to_fail=int((~real[k] & real.R0_CURRENT).sum()),
                            moved_total=int((real[k] != real.R0_CURRENT).sum())))
    say(pd.DataFrame(rep).to_string(index=False))

    # ---------------------------------------------------------------- 3. divergence vs share
    say("\n" + "=" * 118)
    say("3. WHERE DO THE TWO VERDICTS FIRST DIVERGE, AS A FUNCTION OF DEPLOYED SHARE?  (the idea's question)")
    say("   R1a is read against ACT-share (its own window), R1b against DIFF-share.")
    say("=" * 118)
    for tag, col, keyf in (("R1a_ACTIVE_GROSS", "act_share", lambda mn: f"R1a_MINN={mn}"),
                           ("R1b_ACTIVE_DIFF", "diff_share", lambda mn: f"R1b_MINN={mn}")):
        say(f"\n  [{tag}]  rows = realised {col} bucket, cols = MINN")
        bk = pd.cut(real[col], [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0001], right=False)
        tab = []
        for b_, g in real.groupby(bk, observed=True):
            d = dict(bucket=str(b_), n=len(g), R0_pass=int(g.R0_CURRENT.sum()),
                     mean_window_days=int(g[("n_act" if col == "act_share" else "n_diff")].mean()))
            for mn in MINN_GRID:
                d[f"move@{mn}"] = int((g[keyf(mn)] != g.R0_CURRENT).sum())
                d[f"pass@{mn}"] = int(g[keyf(mn)].sum())
            tab.append(d)
        t = pd.DataFrame(tab)
        say(t.to_string(index=False))
        for mn in MINN_GRID:
            mv = t[t[f"move@{mn}"] > 0]
            say(f"    MINN={mn:5d}: total moves {int(t[f'move@{mn}'].sum()):4d}; "
                f"LOWEST share bucket with a move: {mv.bucket.iloc[0] if len(mv) else 'NONE — no divergence at any share'}")

    # ---------------------------------------------------------------- 4. null leakage vs share
    say("\n" + "=" * 118)
    say("4. NULL LEAKAGE.  Does window-matching let a NO-INFORMATION switch through at some share?")
    say("=" * 118)
    ncols = ["panel", "book", "act_share", "diff_share", "Sharpe", "H1", "H2", "MaxDD", "R0_CURRENT"] + \
            [f"R1a_MINN={mn}" for mn in MINN_GRID] + [f"R1b_MINN={mn}" for mn in MINN_GRID]
    nn = nul[ncols]
    say(f"  NULL books: {len(nn)}.  R0 passes {int(nn.R0_CURRENT.sum())}.  "
        + "  ".join(f"R1a@{mn} {int(nn[f'R1a_MINN={mn}'].sum())}" for mn in MINN_GRID) + "  |  "
        + "  ".join(f"R1b@{mn} {int(nn[f'R1b_MINN={mn}'].sum())}" for mn in MINN_GRID))
    leak = nn[(nn[[f"R1a_MINN={mn}" for mn in MINN_GRID] + [f"R1b_MINN={mn}" for mn in MINN_GRID]].any(axis=1))
              | nn.R0_CURRENT]
    say("  NULL cells passing ANY test:" + (" none" if not len(leak) else ""))
    if len(leak): say(leak.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---------------------------------------------------------------- 4b. THE MECHANISM
    say("\n" + "=" * 118)
    say("4b. WHY DOES THE DIFF-WINDOW TEST MOVE EVERY VERDICT?  Leg-level decomposition on each window.")
    say("=" * 118)
    flip = real[real.R0_CURRENT]
    say(f"  books passing R0 (full-window 4a vs RULES v2): {len(flip)} of {len(real)}.")
    for tag, lbl in (("W_ACT", "R1a ACTIVE-GROSS window"), ("W_DIFF", "R1b ACTIVE-DIFF window")):
        f_ = flip
        say(f"\n  [{lbl}]  of those {len(f_)} R0 passes, on this window:")
        say(f"     leg H1 holds {int(f_[tag+'_legH1'].sum()):3d}   leg H2 holds {int(f_[tag+'_legH2'].sum()):3d}   "
            f"leg DD holds {int(f_[tag+'_legDD'].sum()):3d}   all three {int((f_[tag+'_legH1']&f_[tag+'_legH2']&f_[tag+'_legDD']).sum()):3d}")
        say(f"     zero-variance windows (device is FLAT on every day of its own window, Sharpe undefined): "
            f"{int(f_[tag+'_zerovar'].sum())} of {len(f_)}")
        say(f"     mean dSharpe (device - incumbent) ON THIS WINDOW: {f_[tag+'_dS'].mean():+.4f}  "
            f"(median {f_[tag+'_dS'].median():+.4f}, min {f_[tag+'_dS'].min():+.4f}, max {f_[tag+'_dS'].max():+.4f})")
        say(f"     mean dMaxDD: {f_[tag+'_dMaxDD_pp'].mean():+.2f} pp")
    say("\n  THE SAME TWO STATISTICS OVER THE WHOLE REAL CORPUS, SPLIT BY ARM "
        "(this is the mechanism, not a property of the tape):")
    for arm, g in real.groupby("arm"):
        say(f"    {arm:14s} n={len(g):3d}  FULL dS {g.Sharpe.mean()-0:.4f}"
            f"   W_DIFF: zero-var {int(g.W_DIFF_zerovar.sum()):3d}/{len(g):3d}, "
            f"mean dS {g.W_DIFF_dS.mean():+.4f} (|dS| median {g.W_DIFF_dS.abs().median():.4f}), "
            f"mean dMaxDD {g.W_DIFF_dMaxDD_pp.mean():+.2f} pp")
    say("\n  IS ANY WINDOW-MATCHED CONTRAST ADJUDICABLE AT ALL?  Paired circular-block bootstrap t of the")
    say(f"  MEAN EXCESS return on each window (block {BLOCK}d, {NDRAW} draws, seed {BSEED}; INHERITED")
    say("  conventions, not tuned parameters).  |t| > 2 = the window can tell the two books apart.")
    for tag, lbl in (("W_ACT", "ACTIVE-GROSS"), ("W_DIFF", "ACTIVE-DIFF")):
        t = real[tag + "_t_excess"].dropna()
        say(f"    {lbl:13s} n={len(t):3d}  |t|>2: {int((t.abs()>2).sum()):3d}  "
            f"median t {t.median():+.3f}  mean |t| {t.abs().mean():.3f}  max |t| {t.abs().max():.3f}")
    say("    (a window on which no book is distinguishable from the incumbent cannot adjudicate 4a either way)")

    # ---------------------------------------------------------------- 5. both KEEP paths
    say("\n" + "=" * 118)
    say("5. BOTH KEEP PATHS over the whole corpus (4a judged vs RULES v2, 4b vs SPY).")
    say("=" * 118)
    kp = []
    for pname in [p for p, _ in [("U56", 0), ("B136", 0), ("SMALL", 0)]]:
        d = real[real.panel == pname]; n = nul[nul.panel == pname]
        kp.append(dict(panel=pname, real_books=len(d), pass_4a_FULL=int(d.R0_CURRENT.sum()),
                       pass_4a_OOS=int(d.R0_OOS.sum()), pass_4b_FULL=int(d.KEEP4b_FULL.sum()),
                       pass_4b_OOS=int(d.KEEP4b_OOS.sum()),
                       BOTH_4b_FULL_and_OOS=int((d.KEEP4b_FULL & d.KEEP4b_OOS).sum()),
                       NULL_4b_OOS=int(n.KEEP4b_OOS.sum()), of_NULL=len(n)))
    say(pd.DataFrame(kp).to_string(index=False))
    for pname, st in picks_store.items():
        say(f"  [{pname}] FULL bars  RULES v2 {st['b_full'][0]:.2%} / {st['b_full'][1]:.4f} / {st['b_full'][2]:.2%}"
            f"   SPY {st['spy_full'][0]:.2%} / {st['spy_full'][1]:.4f} / {st['spy_full'][2]:.2%}")
        say(f"  [{pname}] OOS  bars  RULES v2 {st['b_oos'][0]:.2%} / {st['b_oos'][1]:.4f} / {st['b_oos'][2]:.2%}"
            f"   SPY {st['spy_oos'][0]:.2%} / {st['spy_oos'][1]:.4f} / {st['spy_oos'][2]:.2%}")
    kb = real[real.KEEP4b_FULL & real.KEEP4b_OOS]
    say(f"\n  books clearing 4b on FULL *and* OOS: {len(kb)}")
    if len(kb):
        say(kb[["panel", "book", "act_share", "diff_share", "CAGR", "Sharpe", "MaxDD",
                "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "turnover_pa"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- 6. rule 8
    say("\n" + "=" * 118)
    say("6. RULE 8 WALK-FORWARD.  (MINN, f) fixed on 2009-2016; each test used as an IS-ONLY chooser;")
    say("   the book it picks read ONCE on 2017-2026.  ALL grid points shown; (*) marks the IS-chosen cell.")
    say("=" * 118)
    ch2 = ch.copy(); ch2["*"] = np.where(ch2.star, "*", "")
    say(ch2[["panel", "MINN", "phi", "test", "*", "picked", "n_is_pass", "n_is_NULL",
             "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "OOS_4a", "OOS_4b"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\n  THE DELIVERABLE ROWS (IS-chosen MINN*, f*):")
    say(ch2[ch2.star][["panel", "MINN", "phi", "test", "picked", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
                       "OOS_4a", "OOS_4b"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- 7. full corpus dump
    say("\n" + "=" * 118)
    say("7. EVERY REAL BOOK (full corpus, all rungs).")
    say("=" * 118)
    cols = ["panel", "family", "arm", "target_s", "act_share", "diff_share", "CAGR", "Sharpe", "MaxDD",
            "H1", "H2", "n_act", "n_diff", "R0_CURRENT", f"R1a_MINN={MINN_GRID[1]}",
            f"R1b_MINN={MINN_GRID[1]}", "KEEP4b_FULL", "KEEP4b_OOS", "OOS_Sharpe"]
    say(real[cols].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---------------------------------------------------------------- gates
    say("\n" + "=" * 118)
    say("GATES")
    say("=" * 118)
    for n, g_, w, ok in GATES:
        say(f"  [{'PASS' if ok else 'FAIL'}] {n:52s} got {g_:>14s}  want {w}")
    say(f"\n  {sum(1 for *_, ok in GATES if ok)} of {len(GATES)} gates pass.")
    say(f"\nwrote {csv.relative_to(ROOT)}   elapsed {time.time()-T0:.0f}s")
    (ROOT / "research" / "backtests" / "2026-09-20_window-matched-on-sometimes-off-corpus_C.txt").write_text("\n".join(OUT) + "\n")
    return df, ch

if __name__ == "__main__":
    main()
