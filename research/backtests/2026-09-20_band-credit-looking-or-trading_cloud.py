#!/usr/bin/env python3
"""Idea 1761 (lane cloud, 2026-09-20): does the BAND'S DRAWDOWN CREDIT come from LOOKING or
from TRADING?

Idea 1741 (this run, earlier) showed the 200d band's MaxDD advantage over its realised-gross-
matched de-gross twin is a TRADE-CADENCE object -- +4.34 / +6.28 / +6.37 pp weekly, +1.75 /
+2.38 / +2.18 monthly and -4.51 / -4.67 / -7.06 QUARTERLY at the live construction -- even
though the gate itself was evaluated DAILY at every rung.  The credit is therefore bought with
TURNOVER, not with information.

The capital question: can the WEEKLY credit be bought at a fraction of the weekly turnover by
trading only when a name's gate actually FLIPS?  Build an EVENT-DRIVEN book (rebalance on day t
iff at least k names crossed the band since the last trade, with an optional forced fallback
cadence), score it against the calendar D / W / M / Q books and against realised-gross-matched
de-gross twins, and publish the CREDIT PER UNIT OF TURNOVER at every rung.

TUNED PARAMETERS (max 2, per PROTOCOL rule 4): EVENT THRESHOLD k and PANEL AXIS.  The fallback
cadence, gross and cost rungs are reported grid axes, every point published.

Protocol: 10 bps headline costs (25 / 50 also published), next-day execution (engine), both KEEP
paths at every cell, rule-8 walk-forward with 2017-2026 read ONCE.  Offline, deterministic.

SURVIVORSHIP: U56 / B136 are CURRENT constituents; SMALL is a CURRENT sub-$2B screen with the
house filter (data/small_meta.csv max_1d_move >= 1.0 dropped, 665 names remain).  Every headline
here is a WITHIN-PANEL contrast between cadences on the SAME names and is first-order immune;
the 4a / 4b pass counts and the rule-8 picks are NOT.
"""
import sys, itertools
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state          # noqa: E402
from engine import backtest as engine_backtest, rebalance_mask           # noqa: E402

BAND      = 0.03
WARMUP    = 260
IS_END    = "2016-12-31"
OOS_START = "2017-01-01"
COSTS     = [0, 10, 25, 50]
GROSSES   = [0.75, 1.00]
KS        = [1, 2, 4, 8, 16]        # tuned parameter 1
FALLBACKS = [None, "Q"]
CALENDARS = ["D", "W", "M", "Q"]
OUT = Path(__file__).with_suffix(".txt")
_log = []
def log(*a):
    s = " ".join(str(x) for x in a); print(s); _log.append(s)

# ---------------------------------------------------------------- panels (tuned parameter 2)
def small_panel():
    px = load_universe(small=True)
    bad = set(pd.read_csv(ROOT / "data" / "small_meta.csv").query("max_1d_move >= 1.0").ticker)
    return px[[c for c in px.columns if c not in bad]]

# ---------------------------------------------------------------- engine replay, arbitrary mask
def bt_mask(px, w, mask_dec):
    """numpy replay of engine.backtest at cost 0 with an ARBITRARY decision-day mask
    (shifted t -> t+1 exactly as the engine does).  Gated against engine.backtest in G1."""
    R = np.nan_to_num(px.pct_change().values, nan=0.0)
    W = np.nan_to_num(w.reindex(px.index).values, nan=0.0)
    W = np.vstack([np.zeros((1, W.shape[1])), W[:-1]])
    m = np.concatenate([[False], np.asarray(mask_dec, bool)[:-1]])
    n = len(R); cur = np.zeros(R.shape[1]); held = np.empty_like(R); turn = np.zeros(n)
    for i in range(n):
        if m[i] or i == 0:
            new = W[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        g = cur * (1.0 + R[i]); tot = g.sum() + (1.0 - cur.sum())
        if tot > 0: cur = g / tot
    return (pd.Series((held * R).sum(axis=1), index=px.index),
            pd.Series(turn, index=px.index), pd.Series(held.sum(axis=1), index=px.index))

def event_mask(state, k):
    """True on day t iff >= k names' band state differs from the state at the last trade."""
    S = np.asarray(state, bool); n = len(S)
    m = np.zeros(n, bool); m[0] = True; last = S[0].copy()
    for i in range(1, n):
        if (S[i] != last).sum() >= k:
            m[i] = True; last = S[i].copy()
    return m

def net(r0, t0, c): return r0 - t0 * c / 1e4
def mets(r):
    eq = (1 + r).cumprod(); yrs = len(r) / 252
    vol = r.std() * np.sqrt(252)
    return dict(CAGR=eq.iloc[-1] ** (1 / yrs) - 1, Sharpe=(r.mean() * 252) / vol if vol else np.nan,
                MaxDD=(eq / eq.cummax() - 1).min(), Vol=vol, Years=yrs)
def halves(r):
    h = len(r) // 2
    return mets(r.iloc[:h])["Sharpe"], mets(r.iloc[h:])["Sharpe"]

def eq_w(px, cols, gross):
    e = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    e[cols] = px[cols].notna().astype(float)
    return gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)

def twin(px, cols, mask, target, tol=1e-6):
    """Plain de-gross twin (no band, SAME trade days) re-scaled to the band book's realised
    mean gross by secant on nominal gross."""
    def run(g):
        r0, t0, gs = bt_mask(px, eq_w(px, cols, g), mask)
        return r0, t0, gs, gs.iloc[WARMUP:].mean()
    g0 = target; r0, t0, s0, m0 = run(g0)
    if abs(m0 - target) < tol: return r0, t0, g0, abs(m0 - target)
    g1 = g0 * (target / m0); r1, t1, s1, m1 = run(g1)
    for _ in range(4):
        if abs(m1 - target) < tol: break
        den = m1 - m0
        g2 = g1 - (m1 - target) * (g1 - g0) / den if den else g1
        g0, m0 = g1, m1; g1 = float(np.clip(g2, 1e-4, 2.0)); r1, t1, s1, m1 = run(g1)
    return r1, t1, g1, abs(m1 - target)

# ---------------------------------------------------------------- run
def main():
    PX = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL": small_panel()}
    log("# Idea 1761 — does the band's drawdown credit come from LOOKING or from TRADING?")
    log(f"# band c={BAND} | warm-up {WARMUP} rows | IS<= {IS_END} | OOS>= {OOS_START} | k ladder {KS}")
    for k, v in PX.items():
        log(f"# panel {k}: {v.shape[1]} columns, {v.index[0].date()} -> {v.index[-1].date()}")

    # ---- G1: bt_mask replays engine.backtest on a calendar mask -----------------------
    g1 = 0.0
    for name in ("U56", "B136"):
        px = PX[name]; w = rules_v2_weights(px, BAND, 0.75); st = px.index[WARMUP]
        a = bt_mask(px, w, rebalance_mask(px.index, "W").values)[0].loc[st:]
        b = engine_backtest(px, w, cost_bps=0.0, freq="W")["returns"].loc[st:]
        g1 = max(g1, float(np.abs(a.values - b.values).max()))
    log(f"G1  bt_mask(calendar) vs engine.backtest max|d| = {g1:.3e} -> {'PASS' if g1 < 1e-12 else 'FAIL'}")

    base, BS = {}, {}
    for name, px in PX.items():
        BS[name] = band_state(px, BAND)
        st = px.index[WARMUP]
        r0, t0, _ = bt_mask(px, rules_v2_weights(px, BAND, 0.75), rebalance_mask(px.index, "W").values)
        spy = px["SPY"].pct_change().fillna(0.0)
        b = dict(start=st, r0=r0.loc[st:], t0=t0.loc[st:], spy=spy.loc[st:])
        for c in COSTS:
            b[f"live{c}"] = mets(net(b["r0"], b["t0"], c)); b[f"lh{c}"] = halves(net(b["r0"], b["t0"], c))
        b["live10_oos"] = mets(net(b["r0"], b["t0"], 10).loc[OOS_START:])
        b["spym"], b["sh"] = mets(b["spy"]), halves(b["spy"])
        b["spym_oos"] = mets(b["spy"].loc[OOS_START:])
        base[name] = b
        log(f"# {name}: RULES v2 (live, 10bps) {b['live10']['CAGR']:.2%}/{b['live10']['Sharpe']:.4f}/"
            f"{b['live10']['MaxDD']:.2%} (OOS {b['live10_oos']['CAGR']:.2%}/{b['live10_oos']['Sharpe']:.4f}/"
            f"{b['live10_oos']['MaxDD']:.2%}) | SPY {b['spym']['CAGR']:.2%}/{b['spym']['Sharpe']:.4f}/"
            f"{b['spym']['MaxDD']:.2%} (OOS {b['spym_oos']['CAGR']:.2%}/{b['spym_oos']['Sharpe']:.4f}/"
            f"{b['spym_oos']['MaxDD']:.2%})")

    # ---- G3: a huge-k event book with a calendar fallback IS the calendar book --------
    px = PX["U56"]; cols = list(px.columns); st = px.index[WARMUP]
    cal = rebalance_mask(px.index, "W").values
    big = event_mask((BS["U56"][cols] & px[cols].notna()).values, 10 ** 6) | cal
    g3 = float(np.abs(bt_mask(px, eq_w(px, cols, 0.75).where(BS["U56"], 0.0), big)[0].loc[st:].values
                      - bt_mask(px, eq_w(px, cols, 0.75).where(BS["U56"], 0.0), cal)[0].loc[st:].values).max())
    log(f"G3  event(k=1e6)|calendar(W) == calendar(W) max|d| = {g3:.3e} -> {'PASS' if g3 < 1e-15 else 'FAIL'}")

    # ---- the grid ---------------------------------------------------------------------
    rows = []
    for pname, px in PX.items():
        cols = [c for c in px.columns if not (pname == "SMALL" and c == "SPY")]
        st = base[pname]["start"]; bs = BS[pname]
        state = (bs[cols] & px[cols].notna()).values
        books = [("CAL", f, None, rebalance_mask(px.index, f).values) for f in CALENDARS]
        for k, fb in itertools.product(KS, FALLBACKS):
            m = event_mask(state, k)
            if fb: m = m | rebalance_mask(px.index, fb).values
            books.append(("EVT", fb or "NONE", k, m))
        for kind, lbl, k, m in books:
            for gross in GROSSES:
                br0, bt_, bg = bt_mask(px, eq_w(px, cols, gross).where(bs, 0.0), m)
                gb = bg.loc[st:].mean()
                tr0, tt_, gnom, gap = twin(px, cols, m, gb)
                br0, bt_, tr0, tt_ = br0.loc[st:], bt_.loc[st:], tr0.loc[st:], tt_.loc[st:]
                yrs = len(br0) / 252
                tpy = float(bt_.sum() / yrs)
                trades = int(m[WARMUP:].sum())
                for c in COSTS:
                    rb, rt = net(br0, bt_, c), net(tr0, tt_, c)
                    mb, mt = mets(rb), mets(rt)
                    b1, b2 = halves(rb)
                    mb_is, mb_oos = mets(rb.loc[:IS_END]), mets(rb.loc[OOS_START:])
                    mt_oos = mets(rt.loc[OOS_START:])
                    B, S, So = base[pname], base[pname]["spym"], base[pname]["spym_oos"]
                    credit = 100 * (mb["MaxDD"] - mt["MaxDD"])
                    rows.append(dict(
                        panel=pname, kind=kind, label=lbl, k=k, gross=gross, cost=c,
                        trades=trades, turn_py=tpy, gross_real=gb, gross_gap=gap, g_twin=gnom,
                        CAGR=mb["CAGR"], Sharpe=mb["Sharpe"], MaxDD=mb["MaxDD"], H1=b1, H2=b2,
                        twin_Sharpe=mt["Sharpe"], twin_MaxDD=mt["MaxDD"],
                        credit_pp=credit, credit_per_turn=credit / tpy if tpy else np.nan,
                        dSharpe=mb["Sharpe"] - mt["Sharpe"], dCAGR_pp=100 * (mb["CAGR"] - mt["CAGR"]),
                        is_Sharpe=mb_is["Sharpe"], is_CAGR=mb_is["CAGR"], is_MaxDD=mb_is["MaxDD"],
                        is_credit_pp=100 * (mb_is["MaxDD"] - mets(rt.loc[:IS_END])["MaxDD"]),
                        oos_CAGR=mb_oos["CAGR"], oos_Sharpe=mb_oos["Sharpe"], oos_MaxDD=mb_oos["MaxDD"],
                        oos_credit_pp=100 * (mb_oos["MaxDD"] - mt_oos["MaxDD"]),
                        keep4a=(b1 > B[f"lh{c}"][0] and b2 > B[f"lh{c}"][1] and mb["MaxDD"] >= B[f"live{c}"]["MaxDD"]),
                        keep4b_full=(b1 > B["sh"][0] and b2 > B["sh"][1] and mb["MaxDD"] >= 0.60 * S["MaxDD"]
                                     and mb["CAGR"] >= 0.70 * S["CAGR"]),
                        keep4b_oos=(mb_oos["Sharpe"] > So["Sharpe"] and mb_oos["MaxDD"] >= 0.60 * So["MaxDD"]
                                    and mb_oos["CAGR"] >= 0.70 * So["CAGR"])))
        log(f"# grid done: {pname} ({len(rows)} rows so far)")

    df = pd.DataFrame(rows)
    df.to_csv(Path(__file__).with_name(Path(__file__).stem + "_grid.csv"), index=False)
    log(f"G2  realised-gross match band vs twin: max gap = {df.gross_gap.max():.3e} -> "
        f"{'PASS' if df.gross_gap.max() < 1e-4 else 'FAIL'}")
    log(f"G4  grid rows = {len(df)} (3 panels x 14 books x 2 gross x 4 cost)")

    # ---- 1741 replication: the calendar credit ladder -----------------------------------
    log("\n## REPLICATION — the calendar credit ladder at the live construction (gross 0.75, 10 bps)")
    cal = df[(df.kind == "CAL") & (df.gross == 0.75) & (df.cost == 10)]
    for p in ("U56", "B136", "SMALL"):
        s = cal[cal.panel == p].set_index("label")
        log("  " + p.ljust(6) + "  " + "  ".join(
            f"{f}: {s.loc[f,'credit_pp']:+.2f} pp @ {s.loc[f,'turn_py']:.1f}x/yr" for f in CALENDARS))
    log("  (1741 published W +4.34 / +6.28 / +6.37, M +1.75 / +2.38 / +2.18, Q -4.51 / -4.67 / -7.06)")

    # ---- THE HEADLINE: credit per unit of turnover -------------------------------------
    log("\n## LOOKING vs TRADING — credit, turnover, and CREDIT PER UNIT OF TURNOVER (gross 0.75, 10 bps)")
    d = df[(df.gross == 0.75) & (df.cost == 10)]
    for p in ("U56", "B136", "SMALL"):
        log(f"  {p}:")
        s = d[d.panel == p].sort_values("turn_py")
        for _, r in s.iterrows():
            tag = f"CAL {r.label}" if r.kind == "CAL" else f"EVT k={int(r.k):<2d} fb={r.label}"
            log(f"     {tag:18s} trades {int(r.trades):5d}  turn {r.turn_py:5.2f}x/yr  credit {r.credit_pp:+6.2f} pp"
                f"  credit/turn {r.credit_per_turn:+6.2f}  Sharpe {r.Sharpe:.4f}  MaxDD {r.MaxDD:.2%}"
                f"  CAGR {r.CAGR:.2%}  dSharpe vs twin {r.dSharpe:+.4f}")
    w = d[(d.kind == "CAL") & (d.label == "W")].set_index("panel")
    log("  >> best EVENT book per panel by credit/turn vs the WEEKLY calendar book:")
    for p in ("U56", "B136", "SMALL"):
        e = d[(d.panel == p) & (d.kind == "EVT")]
        b = e.loc[e.credit_per_turn.idxmax()]
        log(f"     {p:6s} EVT k={int(b.k)} fb={b.label}: credit {b.credit_pp:+.2f} pp at {b.turn_py:.2f}x/yr "
            f"({b.credit_per_turn:+.2f} per turn) vs WEEKLY {w.loc[p,'credit_pp']:+.2f} pp at "
            f"{w.loc[p,'turn_py']:.2f}x/yr ({w.loc[p,'credit_per_turn']:+.2f} per turn) -> "
            f"{'EVENT WINS per unit of turnover' if b.credit_per_turn > w.loc[p,'credit_per_turn'] else 'WEEKLY WINS'}"
            f"; credit RETAINED {b.credit_pp / w.loc[p,'credit_pp']:.1%} at "
            f"{b.turn_py / w.loc[p,'turn_py']:.1%} of the turnover")

    # ---- is the credit a pure function of turnover? -------------------------------------
    log("\n## IS THE CREDIT A PURE FUNCTION OF TURNOVER?  (all 84 books at 10 bps, both gross)")
    def ols(X, y):
        cs = [np.asarray(c, float) for c in X]
        A = np.column_stack([np.ones(len(cs[0]))] + cs)
        beta, *_ = np.linalg.lstsq(A, np.asarray(y, float), rcond=None)
        pred = A @ beta
        return beta, 1 - ((y - pred) ** 2).sum() / ((y - y.mean()) ** 2).sum()
    s = df[df.cost == 10]
    for lab, X in [("turnover/yr alone", [s.turn_py]), ("log turnover/yr", [np.log(s.turn_py)]),
                   ("turnover + panel dummies", [s.turn_py, (s.panel == "B136").astype(float),
                                                 (s.panel == "SMALL").astype(float)]),
                   ("turnover + gross", [s.turn_py, s.gross])]:
        beta, r2 = ols(X, s.credit_pp.values)
        log(f"  {lab:26s} R2 = {r2:+.4f}  beta = {np.round(beta,3).tolist()}")
    for p in ("U56", "B136", "SMALL"):
        t = s[s.panel == p]
        _, r2 = ols([np.log(t.turn_py)], t.credit_pp.values)
        rho = float(np.corrcoef(t.turn_py, t.credit_pp)[0, 1])
        log(f"     within {p:6s}: R2(log turnover) = {r2:+.4f}, rho(turnover, credit) = {rho:+.4f}")

    # ---- both KEEP paths -----------------------------------------------------------------
    log("\n## BOTH KEEP PATHS, EVERY CELL (4a vs live RULES v2, 4b vs SPY)")
    log(f"  4a FULL {int(df.keep4a.sum())} | 4b FULL {int(df.keep4b_full.sum())} | 4b OOS "
        f"{int(df.keep4b_oos.sum())} | 4b FULL-and-OOS {int((df.keep4b_full & df.keep4b_oos).sum())}  of {len(df)}")
    for key in ("panel", "cost", "gross", "kind"):
        for v, g in df.groupby(key):
            log(f"     {key}={v!s:>6s}: 4a {int(g.keep4a.sum()):3d} | 4b FULL {int(g.keep4b_full.sum()):3d} | "
                f"4b OOS {int(g.keep4b_oos.sum()):3d} | BOTH {int((g.keep4b_full & g.keep4b_oos).sum()):3d}  (of {len(g)})")
    both = df[df.keep4b_full & df.keep4b_oos]
    log("  4b FULL-and-OOS passers:")
    for _, r in both.iterrows():
        tag = f"CAL {r.label}" if r.kind == "CAL" else f"EVT k={int(r.k)} fb={r.label}"
        log(f"     {r.panel:6s} {tag:16s} g={r.gross} c={int(r.cost):2d}bps turn {r.turn_py:4.2f}x  FULL "
            f"{r.CAGR:.2%}/{r.Sharpe:.4f}/{r.MaxDD:.2%}  OOS {r.oos_CAGR:.2%}/{r.oos_Sharpe:.4f}/{r.oos_MaxDD:.2%}"
            f"  4a {'PASS' if r.keep4a else 'fail'}")
    if len(both) == 0: log("     (none)")

    # ---- rule 8 ---------------------------------------------------------------------------
    log("\n## RULE 8 — k (and book kind) chosen on warm-up..2016-12-31 ONLY; 2017-2026 read ONCE")
    picks = []
    d10 = df[df.cost == 10]
    for p in ("U56", "B136", "SMALL"):
        for gross in GROSSES:
            s = d10[(d10.panel == p) & (d10.gross == gross)]
            for cname, key in [("C_SHARPE", lambda x: x.is_Sharpe),
                               ("C_CALMAR", lambda x: x.is_CAGR / x.is_MaxDD.abs()),
                               ("C_CREDIT", lambda x: x.is_credit_pp),
                               ("C_CREDPERTURN", lambda x: x.is_credit_pp / x.turn_py)]:
                pick = s.loc[key(s).idxmax()]
                So, Lo = base[p]["spym_oos"], base[p]["live10_oos"]
                ok4b = (pick.oos_Sharpe > So["Sharpe"] and pick.oos_MaxDD >= 0.60 * So["MaxDD"]
                        and pick.oos_CAGR >= 0.70 * So["CAGR"])
                ok4a = pick.oos_Sharpe > Lo["Sharpe"] and pick.oos_MaxDD >= Lo["MaxDD"]
                tag = f"CAL {pick.label}" if pick.kind == "CAL" else f"EVT k={int(pick.k)} fb={pick.label}"
                picks.append(dict(panel=p, gross=gross, chooser=cname, pick=tag, turn_py=pick.turn_py,
                                  oos_CAGR=pick.oos_CAGR, oos_Sharpe=pick.oos_Sharpe, oos_MaxDD=pick.oos_MaxDD,
                                  oos_credit=pick.oos_credit_pp, keep4a_oos=ok4a, keep4b_oos=ok4b))
                log(f"  {p:6s} g={gross} {cname:14s} -> {tag:16s} turn {pick.turn_py:4.2f}x | OOS "
                    f"{pick.oos_CAGR:.2%}/{pick.oos_Sharpe:.4f}/{pick.oos_MaxDD:.2%} | credit OOS "
                    f"{pick.oos_credit_pp:+.2f} pp | 4a {'PASS' if ok4a else 'fail'} 4b {'PASS' if ok4b else 'fail'}")
    pk = pd.DataFrame(picks)
    pk.to_csv(Path(__file__).with_name(Path(__file__).stem + "_choosers.csv"), index=False)
    log(f"  >> picks clearing 4a OOS: {int(pk.keep4a_oos.sum())} of {len(pk)}; 4b OOS: "
        f"{int(pk.keep4b_oos.sum())} of {len(pk)}")
    log(f"  >> EVENT books chosen: {int((pk['pick'].str.startswith('EVT')).sum())} of {len(pk)}")
    r_io = float(np.corrcoef(d10.is_credit_pp, d10.oos_credit_pp)[0, 1])
    log(f"  IS->OOS correlation of the credit across {len(d10)} cells: rho = {r_io:+.4f}")

    log("\n## SURVIVORSHIP CAVEAT")
    log("  U56 / B136 are CURRENT constituents; SMALL is a CURRENT sub-$2B screen (54 names dropped at")
    log("  max_1d_move >= 1.0, 665 remain).  Every cadence contrast is WITHIN a panel on the SAME names")
    log("  and first-order immune; the 4a / 4b pass counts and the rule-8 picks are NOT.")
    OUT.write_text("\n".join(_log) + "\n")

if __name__ == "__main__":
    main()
