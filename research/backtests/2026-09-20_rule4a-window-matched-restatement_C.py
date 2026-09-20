#!/usr/bin/env python3
"""Idea 1631 (lane C, 2026-09-20): should PROTOCOL rule 4a be restated as a WINDOW-MATCHED test?

1602 showed path 4a's half-sample legs are fixed by the TAPE, not by the device, so a rule
confined to one monetary regime is unadjudicable by construction.  This prices the three
restatements the idea names, on a corpus of the record's OWN committed book families, and asks
two questions per restatement:

  (a) how many committed 4a VERDICTS does it move (pass->fail, fail->pass)?
  (b) does it let a NULL device (no signal, matched gross) pass?

Restatements
  R0  CURRENT  : Sharpe > baseline in BOTH calendar halves AND MaxDD >= baseline MaxDD (full).
  R1  ACTIVE   : identical test, but both legs are computed on the DEVICE'S OWN ACTIVE WINDOW
                 (the days its realised gross > 0), halves taken of that window.  Window-matched.
  R2  BLOCKS(p): device beats baseline Sharpe in >= p of the rolling 5y blocks (1y step),
                 AND MaxDD >= baseline MaxDD (full).           <-- tuned parameter 1 of 2
  R3  MARGIN(m): Sharpe > baseline + m in BOTH halves, AND MaxDD >= baseline MaxDD (full).
                                                                <-- tuned parameter 2 of 2

Exactly TWO tuned parameters (p, m); every grid point is reported.  Device rungs are the CORPUS
being adjudicated, not tuning knobs.  Rule 8 walk-forward: p and m are fixed on 2009-2016 rows
only, each restatement is then used as a CHOOSER on those IS rows, and the book it picks is read
once on 2017-2026.  Both KEEP paths evaluated for every chosen book.

Price-only.  Cached panels (U56, B136).  No EDGAR / Form 4 / 8-K / options / live data.
Deterministic, offline, standalone:  python3 research/backtests/2026-09-20_rule4a-window-matched-restatement_C.py
"""
import sys, time, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, band_state, score  # noqa
from engine import backtest, metrics, rebalance_mask  # noqa

pd.set_option("display.width", 200)
T0 = time.time()
COST = 10.0                       # protocol rule 2
FREQ = "W"                        # live cadence
GROSS = 0.75                      # live gross
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

# ----------------------------------------------------------------------------- device corpus
def _ew(px, elig, gross=GROSS):
    """Record convention: gross/N over every PRICED name, gated-out weight goes to CASH."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(elig, 0.0)

def _vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)

def _comp(px):
    """Composite rank score WITHOUT the vol scaler (the 2026-09-04 KEEP 4b form)."""
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3

def dev_band(c):    return lambda px: rules_v2_weights(px, band=c, gross=GROSS)
def dev_maxvol(m):  return lambda px: _ew(px, _vol20(px) < m)
def dev_degross(g): return lambda px: _ew(px, px.notna(), gross=g)
def dev_topn(n):
    def f(px):
        s = _comp(px).where(px.notna())
        rank = s.rank(axis=1, ascending=False)
        return (rank <= n).astype(float) * (GROSS / n)
    return f
def dev_spyfilt(L):
    def f(px):
        spy = px["SPY"]
        on = spy > spy.rolling(L).mean()
        elig = pd.DataFrame(np.repeat(np.asarray(on.values, dtype=bool)[:, None], px.shape[1], axis=1),
                            index=px.index, columns=px.columns) & px.notna()
        return _ew(px, elig)
    return f
def dev_madist(q):
    def f(px):
        d = (px / px.rolling(200).mean() - 1).where(px.notna())
        r = d.rank(axis=1, pct=True, ascending=False)
        return _ew(px, r <= q)
    return f
def dev_stop(s):
    def f(px):
        hi = px.rolling(63).max()
        hit = (px / hi - 1) < -s
        out = hit.rolling(21).max().fillna(0) > 0.5          # sidelined 21 days after a hit
        return _ew(px, px.notna() & ~out)
    return f
def dev_voltgt(t):
    def f(px):
        base = _ew(px, px.notna(), gross=1.0)
        pr = (base.shift(1) * px.pct_change()).sum(axis=1)
        rv = pr.rolling(20).std() * np.sqrt(252)
        k = (t / rv.replace(0, np.nan)).clip(upper=1.0).fillna(0.0)
        return base.mul(k, axis=0)
    return f

# --- NULL devices: no forward information at all, matched gross, seeded and deterministic ---
def null_rand(seed, k=20):
    def f(px):
        rng = np.random.default_rng(seed)
        A = px.notna().values
        M = np.zeros(A.shape, dtype=bool)
        for i in range(A.shape[0]):
            idx = np.flatnonzero(A[i])
            if len(idx) == 0: continue
            pick = rng.choice(idx, size=min(k, len(idx)), replace=False)
            M[i, pick] = True
        return _ew(px, pd.DataFrame(M, index=px.index, columns=px.columns))
    return f
def null_parity():
    def f(px):
        wk = np.asarray(px.index.isocalendar().week.values, dtype=np.int64) % 2 == 1
        elig = pd.DataFrame(np.repeat(wk[:, None], px.shape[1], axis=1),
                            index=px.index, columns=px.columns) & px.notna()
        return _ew(px, elig)
    return f
def null_shuffle(seed, n=10):
    def f(px):
        rng = np.random.default_rng(seed)
        s = _comp(px).where(px.notna())
        V = s.values.copy()
        for i in range(V.shape[0]):
            row = V[i]; ok = np.flatnonzero(~np.isnan(row))
            if len(ok) > 1: row[ok] = rng.permutation(row[ok])
        sh = pd.DataFrame(V, index=px.index, columns=px.columns)
        return (sh.rank(axis=1, ascending=False) <= n).astype(float) * (GROSS / n)
    return f
def null_coinflip(seed):
    """Bernoulli band-state at the live band's own marginal in-band rate."""
    def f(px):
        rng = np.random.default_rng(seed)
        bs = band_state(px, 0.03)
        p = float(bs.values.mean())
        M = pd.DataFrame(rng.random(bs.shape) < p, index=px.index, columns=px.columns)
        return _ew(px, M & px.notna())
    return f

CORPUS = (
    [(f"BAND c={c:.2f}",      "BAND",    dev_band(c),    False) for c in (0.00, 0.03, 0.06, 0.10)] +
    [(f"MAXVOL m={m:.2f}",    "MAXVOL",  dev_maxvol(m),  False) for m in (0.45, 0.60, 0.80, 1.00)] +
    [(f"DEGROSS G={g:.2f}",   "DEGROSS", dev_degross(g), False) for g in (0.25, 0.50, 0.75, 1.00)] +
    [(f"TOPN n={n}",          "TOPN",    dev_topn(n),    False) for n in (3, 5, 10, 20)] +
    [(f"SPYFILT L={L}",       "SPYFILT", dev_spyfilt(L), False) for L in (100, 200)] +
    [(f"MADIST q={q:.2f}",    "MADIST",  dev_madist(q),  False) for q in (0.20, 0.50)] +
    [(f"STOP s={s:.2f}",      "STOP",    dev_stop(s),    False) for s in (0.10, 0.20)] +
    [(f"VOLTGT t={t:.2f}",    "VOLTGT",  dev_voltgt(t),  False) for t in (0.08, 0.12, 0.16)] +
    [("RULES v1 (previous)",  "LIVE",    rules_v1_weights, False)] +
    [(f"NULL_RAND s={s}",     "NULL",    null_rand(s),   True)  for s in (0, 1, 2)] +
    [("NULL_PARITY",          "NULL",    null_parity(),  True)] +
    [(f"NULL_SHUFFLE s={s}",  "NULL",    null_shuffle(s), True) for s in (0, 1)] +
    [("NULL_COINFLIP s=0",    "NULL",    null_coinflip(0), True)]
)

# ----------------------------------------------------------------------------- run + costs
def run(px, wf):
    """Run at ZERO cost once; the cost axis is then exact: r(c) = r_gross - turnover*c/1e4."""
    res = backtest(px, wf(px), cost_bps=0.0, freq=FREQ)
    return res["returns"], res["turnover"], res["weights"].sum(axis=1), res["weights"]

def at_cost(r0, to, c):
    return r0 - to * c / 1e4

def sh(r):
    v = r.std() * np.sqrt(252)
    return (r.mean() * 252) / v if v else np.nan

def mdd(r):
    eq = (1 + r).cumprod()
    return float((eq / eq.cummax() - 1).min())

def cagr(r):
    eq = (1 + r).cumprod(); y = len(r) / 252
    return eq.iloc[-1] ** (1 / y) - 1 if y > 0 else np.nan

# ----------------------------------------------------------------------------- restatements
def blocks_5y(idx, step_years=1):
    out = []
    y0, y1 = idx[0].year, idx[-1].year
    for y in range(y0, y1 + 1, step_years):
        a, b = pd.Timestamp(f"{y}-01-01"), pd.Timestamp(f"{y+5}-01-01")
        if b > idx[-1]: break
        m = (idx >= a) & (idx < b)
        if m.sum() > 750: out.append((f"{y}-{y+4}", m))
    return out

def verdicts(r, b, active, diff, blk, P_GRID, M_GRID):
    """Every restatement's pass/fail for one (device, baseline) return pair."""
    h = len(r) // 2
    dd_ok = mdd(r) >= mdd(b)
    out = {}
    L_H1 = bool(sh(r.iloc[:h]) > sh(b.iloc[:h]))
    L_H2 = bool(sh(r.iloc[h:]) > sh(b.iloc[h:]))
    out["leg_H1"], out["leg_H2"], out["leg_DD"] = L_H1, L_H2, dd_ok
    out["_dSh_H1"] = float(sh(r.iloc[:h]) - sh(b.iloc[:h]))
    out["_dSh_H2"] = float(sh(r.iloc[h:]) - sh(b.iloc[h:]))
    out["_dMaxDD_pp"] = float((mdd(r) - mdd(b)) * 100)
    out["R0_CURRENT"] = bool(L_H1 and L_H2 and dd_ok)
    # R1a ACTIVE-GROSS: window-matched to the days the device is DEPLOYED (realised gross > 0)
    # R1b ACTIVE-DIFF : window-matched to the days the device's BOOK DIFFERS from the baseline's
    #                   (on the other days the device IS the baseline, so they only add shared tape)
    for tag, mask in (("R1a_ACTIVE_GROSS", active), ("R1b_ACTIVE_DIFF", diff)):
        ra, ba = r[mask], b[mask]
        out[f"_n_{tag}"] = int(len(ra))
        if len(ra) < 500:
            out[tag] = False                 # too thin a window to adjudicate anything
            continue
        ha = len(ra) // 2
        out[tag] = bool(sh(ra.iloc[:ha]) > sh(ba.iloc[:ha]) and sh(ra.iloc[ha:]) > sh(ba.iloc[ha:])
                        and mdd(ra) >= mdd(ba))
    wins = [sh(r[m]) > sh(b[m]) for _, m in blk]
    share = float(np.mean(wins)) if wins else 0.0
    out["_blockshare"] = share
    for p in P_GRID:
        out[f"R2_BLOCKS p={p:.2f}"] = bool(share >= p - 1e-12 and dd_ok)
    marg = min(sh(r.iloc[:h]) - sh(b.iloc[:h]), sh(r.iloc[h:]) - sh(b.iloc[h:]))
    out["_minmargin"] = float(marg)
    for m in M_GRID:
        out[f"R3_MARGIN m={m:.2f}"] = bool(marg > m and dd_ok)
    return out

# ----------------------------------------------------------------------------- main
P_GRID = (0.50, 0.60, 0.70, 0.80, 0.90, 1.00)
M_GRID = (0.00, 0.05, 0.10, 0.20, 0.30)
PANELS = [("U56", dict()), ("B136", dict(broad=True))]

def main():
    gates = {}
    all_rows, chooser_rows, memo = [], [], []

    for pname, kw in PANELS:
        px = load_universe(**kw)
        start = px.index[260]                       # skip warm-up, as compare() does
        px = px.loc[:]                              # full frame; slice the RETURNS, not the prices
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        b0, bto, bgr, bW = run(px, lambda p: rules_v2_weights(p, band=0.03, gross=GROSS))
        b = at_cost(b0, bto, COST).loc[start:]

        # ---- G1: the cost axis is exact off the zero-cost rung
        chk = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"]
        gates[f"G1 cost-axis exact ({pname})"] = float(np.abs(at_cost(b0, bto, COST) - chk).max())
        # ---- G2: the (band 0.03, G 0.75, W) cell IS the live book
        gates[f"G2 baseline==live rules_v2 ({pname})"] = float(
            np.abs(b - backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]).max())

        blk = blocks_5y(b.index)
        rets = {}
        for name, fam, wf, is_null in CORPUS:
            r0, to, gr, W = run(px, wf)
            r = at_cost(r0, to, COST).loc[start:]
            active = (gr.loc[start:] > 1e-9).values
            diff = ((W - bW).abs().sum(axis=1).loc[start:] > 1e-9).values
            rets[name] = (r, active, diff, fam, is_null, to.loc[start:].sum() / (len(r) / 252))
            v = verdicts(r, b, active, diff, blk, P_GRID, M_GRID)
            row = dict(panel=pname, device=name, family=fam, null=is_null,
                       CAGR=cagr(r), Sharpe=sh(r), MaxDD=mdd(r),
                       H1=sh(r.iloc[:len(r)//2]), H2=sh(r.iloc[len(r)//2:]),
                       act_share=float(np.mean(active)), diff_share=float(np.mean(diff)), **v)
            all_rows.append(row)

        # -------------------------------------------------- rule 8: IS-only parameter choice
        isr = lambda s: s.loc[:IS_END]
        oosr = lambda s: s.loc[OOS_START:]
        b_is, b_oos = isr(b), oosr(b)
        blk_is = blocks_5y(b_is.index)
        is_v = {}
        for name, (r, active, diff, fam, is_null, tpy) in rets.items():
            n_is = len(isr(r))
            is_v[name] = verdicts(isr(r), b_is, active[:n_is], diff[:n_is], blk_is, P_GRID, M_GRID)

        # tuned params picked on IS rows ONLY: the tightest rung that admits no NULL on IS
        def tightest(prefix, grid, key):
            for g in grid:
                k = f"{prefix} {key}={g:.2f}"
                if not any(is_v[n][k] for n, t in rets.items() if t[4]):
                    return g, k
            return grid[-1], f"{prefix} {key}={grid[-1]:.2f}"
        p_star, p_key = tightest("R2_BLOCKS", P_GRID, "p")
        m_star, m_key = tightest("R3_MARGIN", M_GRID, "m")
        memo.append((pname, p_star, m_star))

        ALL_RK = (["R0_CURRENT", "R1a_ACTIVE_GROSS", "R1b_ACTIVE_DIFF"] +
                  [f"R2_BLOCKS p={p:.2f}" for p in P_GRID] +
                  [f"R3_MARGIN m={m:.2f}" for m in M_GRID])
        for rk in ALL_RK:
            cand = [n for n, t in rets.items() if not t[4] and is_v[n][rk]]
            if not cand:
                chooser_rows.append(dict(panel=pname, restatement=rk, picked="(none passes IS)",
                                         n_is_pass=0, n_is_NULL=0, OOS_CAGR=np.nan, OOS_Sharpe=np.nan,
                                         OOS_MaxDD=np.nan, p4a=False, p4b=False))
                continue
            pick = max(cand, key=lambda n: sh(isr(rets[n][0])))     # IS rows only
            ro = oosr(rets[pick][0])
            s_oos, s_spy_oos = spy.loc[OOS_START:], spy.loc[OOS_START:]
            h = len(ro) // 2
            p4a = bool(sh(ro.iloc[:h]) > sh(b_oos.iloc[:h]) and sh(ro.iloc[h:]) > sh(b_oos.iloc[h:])
                       and mdd(ro) >= mdd(b_oos))
            p4b = bool(sh(ro.iloc[:h]) > sh(s_oos.iloc[:h]) and sh(ro.iloc[h:]) > sh(s_oos.iloc[h:])
                       and mdd(ro) >= 0.60 * mdd(s_oos) and cagr(ro) >= 0.70 * cagr(s_oos))
            n_null_is = int(sum(is_v[n][rk] for n, t in rets.items() if t[4]))
            chooser_rows.append(dict(panel=pname, restatement=rk, picked=pick, n_is_pass=len(cand),
                                     n_is_NULL=n_null_is,
                                     OOS_CAGR=cagr(ro), OOS_Sharpe=sh(ro), OOS_MaxDD=mdd(ro),
                                     p4a=p4a, p4b=p4b))
        chooser_rows.append(dict(panel=pname, restatement="-- baseline RULES v2 --", picked="",
                                 n_is_pass=-1, n_is_NULL=-1, OOS_CAGR=cagr(b_oos), OOS_Sharpe=sh(b_oos),
                                 OOS_MaxDD=mdd(b_oos), p4a=False, p4b=False))
        chooser_rows.append(dict(panel=pname, restatement="-- SPY --", picked="", n_is_pass=-1, n_is_NULL=-1,
                                 OOS_CAGR=cagr(spy.loc[OOS_START:]), OOS_Sharpe=sh(spy.loc[OOS_START:]),
                                 OOS_MaxDD=mdd(spy.loc[OOS_START:]), p4a=False, p4b=False))
        # G6: no chooser statistic may read a 2017+ row.  Recompute the IS verdicts on a HARD
        # TRUNCATED frame (rows physically deleted) and require bit-identical results.
        g6 = 0.0
        for name, t in list(rets.items())[:6]:
            r, active, diff, fam, is_null, tpy = t
            n_is = len(isr(r))
            hard = r.iloc[:n_is].copy()
            v_h = verdicts(hard, b_is.iloc[:n_is], active[:n_is], diff[:n_is], blk_is, P_GRID, M_GRID)
            for k in v_h:
                if isinstance(v_h[k], bool):
                    g6 = max(g6, float(v_h[k] != is_v[name][k]))
                else:
                    g6 = max(g6, abs(float(v_h[k]) - float(is_v[name][k])))
        gates[f"G6 chooser reads no 2017+ row ({pname})"] = g6
        gates[f"G5 tuned params ({pname})"] = 2
        gates[f"G3 blocks ({pname})"] = len(blk)
        gates[f"G4 IS blocks ({pname})"] = len(blk_is)

    df = pd.DataFrame(all_rows)
    ch = pd.DataFrame(chooser_rows)
    out = ROOT / "research" / "backtests" / "2026-09-20_rule4a-window-matched-restatement_C.csv"
    df.to_csv(out, index=False)

    # ------------------------------------------------------------------ report: EVERY grid point
    keys = ["R0_CURRENT", "R1a_ACTIVE_GROSS", "R1b_ACTIVE_DIFF"] + [f"R2_BLOCKS p={p:.2f}" for p in P_GRID] + \
           [f"R3_MARGIN m={m:.2f}" for m in M_GRID]
    print("\n" + "=" * 110)
    print("IDEA 1631 - RESTATING PROTOCOL RULE 4a.  Corpus =", len(CORPUS), "books x", len(PANELS),
          "panels =", len(df), "committed cells.  Cost", COST, "bps, freq", FREQ)
    print("=" * 110)

    print("\n--- ALL GRID POINTS: 4a pass counts, verdict moves vs R0, and NULL leakage ---")
    rep = []
    real = df[~df.null]; nul = df[df.null]
    for k in keys:
        mv_up = int(((df[k]) & (~df.R0_CURRENT)).sum())
        mv_dn = int(((~df[k]) & (df.R0_CURRENT)).sum())
        rep.append(dict(restatement=k, pass_real=int(real[k].sum()), of_real=len(real),
                        pass_NULL=int(nul[k].sum()), of_NULL=len(nul),
                        moved_fail_to_pass=mv_up, moved_pass_to_fail=mv_dn,
                        moved_total=mv_up + mv_dn))
    rp = pd.DataFrame(rep)
    print(rp.to_string(index=False))

    print("\n--- per panel ---")
    for pname, _ in PANELS:
        d = df[df.panel == pname]
        sub = pd.DataFrame([dict(restatement=k, pass_real=int(d[~d.null][k].sum()),
                                 pass_NULL=int(d[d.null][k].sum()),
                                 moved=int((d[k] != d.R0_CURRENT).sum())) for k in keys])
        print(f"\n[{pname}]"); print(sub.to_string(index=False))

    print("\n--- NULL devices in full (do any restatement let a no-signal book through?) ---")
    cols = ["panel", "device", "Sharpe", "H1", "H2", "MaxDD", "act_share", "diff_share",
            "_blockshare", "_minmargin"] + keys
    print(nul[cols].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    print("\n--- every REAL book, headline metrics + the two continuous statistics ---")
    print(real[["panel", "device", "family", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                "act_share", "diff_share", "_n_R1b_ACTIVE_DIFF", "_blockshare", "_minmargin",
                "R0_CURRENT", "R1a_ACTIVE_GROSS", "R1b_ACTIVE_DIFF"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    print("\n--- WHICH 4a LEG ACTUALLY BINDS?  (all three restatements rewrite the SHARPE legs;")
    print("    if the binding leg is MaxDD, no Sharpe restatement can move the verdict) ---")
    lg = []
    for pname, _ in PANELS:
        d = real[real.panel == pname]
        f = d[~d.R0_CURRENT]
        lg.append(dict(panel=pname, real_books=len(d), pass_4a=int(d.R0_CURRENT.sum()), fail=len(f),
                       fail_H1_only=int((~f.leg_H1 & f.leg_H2 & f.leg_DD).sum()),
                       fail_H2_only=int((f.leg_H1 & ~f.leg_H2 & f.leg_DD).sum()),
                       fail_DD_only=int((f.leg_H1 & f.leg_H2 & ~f.leg_DD).sum()),
                       fail_both_halves=int((~f.leg_H1 & ~f.leg_H2).sum()),
                       DD_leg_fails=int((~f.leg_DD).sum()),
                       SHARPE_leg_fails=int((~f.leg_H1 | ~f.leg_H2).sum())))
    print(pd.DataFrame(lg).to_string(index=False))
    print("\n  mean min-half Sharpe margin vs baseline, real books: "
          f"{real._minmargin.mean():+.4f}  (median {real._minmargin.median():+.4f}); "
          f"books with a POSITIVE margin: {int((real._minmargin > 0).sum())} of {len(real)}")
    print("  mean dMaxDD vs baseline, real books: "
          f"{real._dMaxDD_pp.mean():+.2f} pp; books SHALLOWER than baseline: "
          f"{int((real._dMaxDD_pp >= 0).sum())} of {len(real)}")

    print("\n--- RULE 8 WALK-FORWARD: (p,m) fixed on 2009-2016 rows, restatement used as CHOOSER,")
    print("    the book it picks read ONCE on 2017-2026.  Both KEEP paths evaluated. ---")
    print("IS-chosen tuned parameters per panel (tightest rung admitting NO null on IS):",
          {p: dict(p=ps, m=ms) for p, ps, ms in memo})
    print(ch.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n--- GATES ---")
    for k, v in gates.items():
        print(f"  {k}: {v:.3e}" if isinstance(v, float) else f"  {k}: {v}")
    print(f"\nwrote {out.relative_to(ROOT)}   elapsed {time.time()-T0:.0f}s")
    return df, ch

if __name__ == "__main__":
    main()
