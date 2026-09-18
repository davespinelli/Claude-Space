#!/usr/bin/env python3
"""Idea 1286 (lane cloud, 2026-09-18): is the STANDING G = 0.60 BOOK's 4b PASS PAID FOR BY
SELECTION, or BOUGHT BY EXPOSURE?

THE PREMISE, FROM THE RECORD'S OWN TWO MOST RECENT FINDINGS.  Idea 1282 and idea 1281 (this
lane, earlier today) both land on the same book: the U56 gross rung **G = 0.60** is the ONE
book on the record's four ladders that passes PROTOCOL 4b under EVERY drawdown key tried --
MaxDD, the K_k trailing-window family, and all seven quantile rungs Q_0.90..Q_1.00.  It is
currently the record's only undisputed capital-worthy book.  The CHANGELOG's own standing
diagnosis is that "the DD cap is the only binding 4b leg and every exposure mechanism is
reproduced by a flat gross cut".  Put those two together and an uncomfortable question follows
that nobody has run: **if the binding leg is drawdown and drawdown is bought by cutting gross,
what exactly is the three-leg composite SELECTION contributing to that pass?**

THE TEST.  Hold N, H, cadence, gross, costs and execution IDENTICAL and remove ONLY the ranking.
Four arms, on three panels:
    RANK      the standing book -- top N = 20 by the frozen 21/252 + 0/126 + 0/63 composite
              among eligible names, min-hold H = 126, equal weight.  The thing being defended.
    RAND      IDENTICAL mechanics, N = 20 slots, min-hold H = 126, equal weight, drawing
              uniformly at random from the SAME eligible set.  12 seeds; median and full spread
              reported.  This is the decisive control: it matches breadth, holding period,
              turnover shape and exposure, and removes ONLY the ranking.
    BREADTH   equal weight over EVERY eligible name, no N, no ranking (the 2026-09-03
              recommendation memo's Finding 2 mechanism) -- selection-free, breadth-maximal.
    SPYONLY   g of NAV in SPY, the rest cash.  Exposure with no stock selection at all, and the
              floor any "book" must clear to be worth its own operational cost.
"Eligible" is frozen at the record's definition: above own 200d MA AND vol20 < 0.60.

THE TWO DIALS (PROTOCOL rule 4), chosen to be the two things that actually kill live books:
    DIAL 1  COST RUNG  {0, 10, 25, 50} bps per unit turnover.  10 is PROTOCOL's assumption;
            it is an ASSUMPTION and not a measurement, and RAND / BREADTH / RANK do not carry
            the same turnover, so a cost rung can reorder them.
    DIAL 2  FILL DELAY {t+1, t+2}.  t+1 is PROTOCOL rule 2; t+2 is one extra day between the
            decision close and the fill -- the realistic slippage for a book a human trades.
GROSS is NOT a dial: all five rungs {0.50, 0.60, 0.75, 0.85, 1.00} are reported at every grid
point, and the rule-8 arm CHOOSES it in sample so it is never tuned on the evaluation window.
Panel is reported at every value.

PRE-DECLARED OUTCOMES, written before any number was read:
  (A) SELECTION IS PAID FOR -- RANK passes 4b at cells where RAND's MEDIAN does not, and
      RANK - RAND(median) is positive on Sharpe out of sample.  The standing book is a book.
  (B) BOUGHT BY EXPOSURE -- RAND's median passes 4b wherever RANK does.  The composite is
      decoration on a gross cut, and the record should say so.
  (C) PAID FOR BUT NOT AT COST -- RANK separates at 0 and 10 bps and is caught by RAND or
      BREADTH at 25 or 50, i.e. the edge is smaller than the record's own cost uncertainty.
  (D) NOT EVEN AN EXPOSURE STORY -- SPYONLY at matched gross clears 4b too.
Only (A), holding at 25 bps and at t+2, would leave the standing book where the record has it.

THE RULE-8 ARM (PROTOCOL rule 8, required).  Every (panel, arm, cost, delay) cell chooses its
GROSS on warm-up..2016-12-31 ONLY -- highest IS Sharpe among grosses passing all four
IS-computable 4b legs, fallback (declared in advance) highest IS Sharpe -- and 2017-2026 is read
ONCE.  The money question is asked directly: does the RANK chooser beat the RAND chooser OOS,
and by more than the seed spread?

FROZEN, not touched here: the composite and its three legs, eligibility, equal 1/len(held)
slots, weekly decide-Friday cadence, 260-row warm-up.  SPY is the BENCHMARK and is NEVER a
constituent of any panel (gate G5); SPYONLY holds it deliberately and is labelled as a control,
not a book drawn from the panel.

SURVIVORSHIP (rule 9).  U56 and B135 are CURRENT-constituent lists; SMALL663 is a current
sub-$2B screen with the house `max_1d_move >= 1.0` filter applied FIRST.  This matters MORE than
usual here and in a known direction: a current-constituent list is a list of SURVIVORS, so a
RANDOM draw from it is a draw from winners and RAND is FLATTERED relative to a true random pick.
That biases the run AGAINST outcome (A) -- if RANK still separates from RAND, the separation is
conservative; if it does not, the result is not yet proof that selection is worthless, only that
it is not visible above a survivor-flattered control.  Both directions are stated with the
result.  The absolute 4b / 4a verdicts and OOS triples are upper bounds throughout.

Deterministic (fixed seeds), offline, no network.  Run: python3 <this file>
"""
import sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights          # noqa: E402
from engine import backtest, rebalance_mask                   # noqa: E402

DATE = "2026-09-18"
SLUG = "is-the-STANDING-G-0.60-BOOK-s-4b-PASS-PAID-FOR-BY-SELECTION-or-BOUGHT-BY-EXPOSURE"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
A_N, A_H, A_C = 20, 126, "W"
STAND_G = 0.60                                   # the standing rung under defence
LEGS = [(21, 252), (0, 126), (0, 63)]
GROSSES = [0.50, 0.60, 0.75, 0.85, 1.00]         # reported at every grid point, never tuned
COSTS = [0.0, 10.0, 25.0, 50.0]                  # DIAL 1
DELAYS = [1, 2]                                  # DIAL 2  (t+1, t+2)
NSEED, SEED0 = 12, 20260918
_LOG, GATES = [], []


def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); _LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    say(f"   GATE {name}: {value} vs {target} -> {'PASS' if ok else 'FAIL'}")
    return bool(ok)


# ---------------------------------------------------------------- metrics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 20: return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 20: return np.nan
    return float(np.prod(1.0 + r) ** (252.0 / len(r)) - 1.0)


def mdd(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1.0).min())


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def windows(idx, r):
    n = len(r); h = n // 2
    o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]),
                is_=stats(r[:o]), oos=stats(r[o:]),
                is_h1=sharpe(r[:o][:o // 2]), is_h2=sharpe(r[:o][o // 2:]))


def flat(w):
    out = {}
    for k, v in w.items():
        if isinstance(v, dict):
            for m, x in v.items(): out[f"{k}_{m}"] = x
        else: out[k] = v
    return out


# ---------------------------------------------------------------- panel
class Panel:
    def __init__(self, name, px, invest):
        assert "SPY" not in invest, "G5: SPY must never be a constituent"
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.ispy = cols.index("SPY")
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        q = px[invest]
        parts = []
        for skip, look in LEGS:
            x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
            parts.append(x.rank(axis=1, pct=True))
        comp = (sum(parts) / len(parts)).values
        self.key = np.where(np.isfinite(comp), -comp, np.inf)
        above = (q > q.rolling(200).mean()).values
        vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
        self.elig = above & (np.nan_to_num(vol20, nan=1e9) < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        m = rebalance_mask(px.index, A_C).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)


def _slots(pan, keyfn, N, H):
    """Shared N-slot / min-hold-H machinery. keyfn(ts) -> per-name sort key (lower is better,
    np.inf = ineligible). RANK and RAND differ ONLY in keyfn -- that is the whole experiment."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    nreb = len(pan.reb)
    for i, t in enumerate(pan.reb):
        ts = max(t - 1, 0)
        held = np.flatnonzero(cur >= 0)
        if len(held): held = held[pr[t, held]]
        keep = [int(c) for c in (held[(t - cur[held]) < H] if len(held) else held)]
        k = keyfn(ts).copy()
        k[~(pan.elig[ts] & pr[ts])] = np.inf
        for c in keep: k[c] = np.inf
        need, take = N - len(keep), []
        for c in np.argsort(k, kind="stable"):
            if need <= 0 or not np.isfinite(k[int(c)]): break
            take.append(int(c)); need -= 1
        new = np.full(K, -1, dtype=np.int64)
        for c in keep: new[c] = cur[c]
        for c in take: new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if not len(sel): continue
        stop = pan.reb[i + 1] if i + 1 < nreb else T
        W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def w_rank(pan):
    return _slots(pan, lambda ts: pan.key[ts], A_N, A_H)


def w_rand(pan, seed):
    rng = np.random.default_rng(seed)
    K = len(pan.iinv)
    draw = rng.random((len(pan.idx), K))          # pre-drawn so the arm is reproducible
    return _slots(pan, lambda ts: draw[ts], A_N, A_H)


def w_breadth(pan):
    """Equal weight over EVERY eligible name, no N and no ranking."""
    T, M = pan.rets.shape
    W = np.zeros((T, M))
    pr = pan.priced[:, pan.iinv]
    nreb = len(pan.reb)
    for i, t in enumerate(pan.reb):
        ts = max(t - 1, 0)
        sel = np.flatnonzero(pan.elig[ts] & pr[ts])
        if not len(sel): continue
        stop = pan.reb[i + 1] if i + 1 < nreb else T
        W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def w_spy(pan):
    T, M = pan.rets.shape
    W = np.zeros((T, M))
    W[:, pan.ispy] = 1.0
    return W


def run_raw(pan, Wt, gross, delay):
    """Gross-of-cost return path and turnover. Costs are applied OUTSIDE so all four cost
    rungs of DIAL 1 come from one run (the cost term is exactly linear in turnover)."""
    if delay > 1:
        Wt = np.vstack([np.repeat(Wt[:1], delay - 1, axis=0), Wt[:-(delay - 1)]])
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M)); turn = np.zeros(T); curw = np.zeros(M)
    ends = np.append(pan.reb[1:], T)
    for i0, i1 in zip(pan.reb, ends):
        w0 = gross * Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return (held * rets).sum(axis=1), turn


# ---------------------------------------------------------------- KEEP paths
def legs_4a(bk, live):
    return dict(H1=bk["h1"]["Sharpe"] > live["h1"]["Sharpe"],
                H2=bk["h2"]["Sharpe"] > live["h2"]["Sharpe"],
                DD=bk["full"]["MaxDD"] >= live["full"]["MaxDD"])


def legs_4b(bk, spy):
    return dict(H1=bk["h1"]["Sharpe"] > spy["h1"]["Sharpe"],
                H2=bk["h2"]["Sharpe"] > spy["h2"]["Sharpe"],
                OOS=bk["oos"]["Sharpe"] > spy["oos"]["Sharpe"],
                DD=bk["full"]["MaxDD"] >= DD_CAP * spy["full"]["MaxDD"],
                CAGR=bk["full"]["CAGR"] >= CAGR_FLOOR * spy["full"]["CAGR"])


def legs_4b_is(bk, spy):
    """The four legs computable IN SAMPLE -- all a rule-8 chooser may see."""
    return dict(H1=bk["is_h1"] > spy["is_h1"], H2=bk["is_h2"] > spy["is_h2"],
                DD=bk["is_"]["MaxDD"] >= DD_CAP * spy["is_"]["MaxDD"],
                CAGR=bk["is_"]["CAGR"] >= CAGR_FLOOR * spy["is_"]["CAGR"])


def failed(d):
    return ",".join(k for k, v in d.items() if not v) or "-"


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    say(f"# {DATE} idea 1286 lane cloud -- {SLUG}")
    say(f"# ARMS: RANK (the standing book) / RAND ({NSEED} seeds, ranking removed, everything "
        f"else held) / BREADTH (no N, no ranking) / SPYONLY (exposure alone)")
    say(f"# DIAL 1 COST = {COSTS} bps;  DIAL 2 FILL DELAY = {['t+%d' % d for d in DELAYS]}")
    say(f"# GROSS reported at every grid point (never tuned): {GROSSES}; standing rung "
        f"G = {STAND_G}")
    say(f"# frozen: N={A_N} H={A_H} cadence={A_C} warm-up={WARMUP} elig=above200d & vol20<{MAXVOL}")

    panels = []
    px = load_universe()
    panels.append(("U56", px, [c for c in px.columns if c != "SPY"]))
    pb = load_universe(broad=True)
    panels.append((f"B{pb.shape[1]-1}", pb, [c for c in pb.columns if c != "SPY"]))
    psm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv_s = [c for c in psm.columns if c != "SPY" and c not in bad]
    say(f"# SMALL panel: {psm.shape[1]-1} names, {len(bad & set(psm.columns))} dropped for "
        f"max_1d_move >= 1.0 -> {len(inv_s)} investable")
    panels.append((f"SMALL{len(inv_s)}", psm, inv_s))

    rows, r8rows = [], []
    SPYSH = {}
    g1_done = False
    for pname, p_px, inv in panels:
        pan = Panel(pname, p_px, inv)
        idx = pan.idx[WARMUP:]
        spy = windows(idx, pan.spy[WARMUP:])
        live_r = backtest(p_px, rules_v2_weights(p_px), cost_bps=10.0,
                          freq="W")["returns"].fillna(0.0).values[WARMUP:]
        live = windows(idx, live_r)
        SPYSH[pname] = spy["full"]["Sharpe"]
        say(f"\n## {pname}  n_names={len(inv)}  {idx[0].date()}..{idx[-1].date()}")
        say(f"   SPY      full {spy['full']['CAGR']:7.2%} / {spy['full']['Sharpe']:.4f} / "
            f"{spy['full']['MaxDD']:7.2%}   OOS Sh {spy['oos']['Sharpe']:.4f}")
        say(f"   LIVE v2  full {live['full']['CAGR']:7.2%} / {live['full']['Sharpe']:.4f} / "
            f"{live['full']['MaxDD']:7.2%}   OOS Sh {live['oos']['Sharpe']:.4f}")

        WS = [("RANK", -1, w_rank(pan)), ("BREADTH", -1, w_breadth(pan)),
              ("SPYONLY", -1, w_spy(pan))]
        WS += [("RAND", s, w_rand(pan, SEED0 + s)) for s in range(NSEED)]

        if not g1_done:
            # G1: the fast runner reproduces engine.backtest on the standing book
            wdf = pd.DataFrame(np.roll(STAND_G * WS[0][2], -1, axis=0),
                               index=pan.idx, columns=pan.px.columns)
            eng = backtest(pan.px, wdf, cost_bps=10.0, freq=A_C)["returns"].fillna(0.0).values
            gr, tn = run_raw(pan, WS[0][2], STAND_G, 1)
            d = float(np.abs((gr - tn * 10.0 / 1e4)[WARMUP:] - eng[WARMUP:]).max())
            gate("G1 fast runner == engine.backtest (standing book)", f"{d:.3e}", "< 1e-12",
                 d < 1e-12)
            g1_done = True

        cache = {}
        for arm, seed, Wt in WS:
            for g in GROSSES:
                for dl in DELAYS:
                    gr, tn = run_raw(pan, Wt, g, dl)
                    cache[(arm, seed, g, dl)] = (gr[WARMUP:], tn[WARMUP:])
                    for c in COSTS:
                        r = gr[WARMUP:] - tn[WARMUP:] * c / 1e4
                        w = windows(idx, r)
                        a4, b4 = legs_4a(w, live), legs_4b(w, spy)
                        rows.append(dict(panel=pname, arm=arm, seed=seed, gross=g, cost=c,
                                         delay=dl, turnover_yr=tn[WARMUP:].sum() / (len(r) / 252),
                                         keep4a=all(a4.values()), keep4b=all(b4.values()),
                                         fail4a=failed(a4), fail4b=failed(b4), **flat(w)))

        # ---- rule 8: choose GROSS in sample, per (arm, seed, cost, delay); OOS read ONCE
        for arm, seed, _ in WS:
            for c in COSTS:
                for dl in DELAYS:
                    cand = {}
                    for g in GROSSES:
                        gr, tn = cache[(arm, seed, g, dl)]
                        cand[g] = windows(idx, gr - tn * c / 1e4)
                    ok = [g for g in GROSSES if all(legs_4b_is(cand[g], spy).values())]
                    pool = ok if ok else GROSSES
                    pick = max(pool, key=lambda g: (cand[g]["is_"]["Sharpe"], g))
                    w = cand[pick]
                    a4, b4 = legs_4a(w, live), legs_4b(w, spy)
                    r8rows.append(dict(panel=pname, arm=arm, seed=seed, cost=c, delay=dl,
                                       pick_gross=pick, n_eligible=len(ok), fallback=not bool(ok),
                                       is_Sharpe=w["is_"]["Sharpe"],
                                       oos_CAGR=w["oos"]["CAGR"], oos_Sharpe=w["oos"]["Sharpe"],
                                       oos_MaxDD=w["oos"]["MaxDD"],
                                       full_CAGR=w["full"]["CAGR"],
                                       full_Sharpe=w["full"]["Sharpe"],
                                       full_MaxDD=w["full"]["MaxDD"],
                                       h1=w["h1"]["Sharpe"], h2=w["h2"]["Sharpe"],
                                       keep4a=all(a4.values()), keep4b=all(b4.values()),
                                       fail4a=failed(a4), fail4b=failed(b4),
                                       spy_oos_Sharpe=spy["oos"]["Sharpe"],
                                       spy_oos_CAGR=spy["oos"]["CAGR"],
                                       spy_oos_MaxDD=spy["oos"]["MaxDD"],
                                       live_oos_Sharpe=live["oos"]["Sharpe"]))

    D = pd.DataFrame(rows); R8 = pd.DataFrame(r8rows)

    # ---- gates
    sp = D[(D.arm == "SPYONLY") & (D.cost == 0.0) & (D.delay == 1) & (D.gross == 1.00)]
    g2 = float(max(abs(r.full_Sharpe - SPYSH[r.panel]) for _, r in sp.iterrows()))
    gate("G2 SPYONLY at gross 1.00, 0 bps reproduces that panel's OWN SPY Sharpe",
         f"{g2:.3e}", "< 1e-9", g2 < 1e-9)
    mono = D.groupby(["panel", "arm", "seed", "gross", "delay"]).apply(
        lambda d: bool(d.sort_values("cost").full_CAGR.is_monotonic_decreasing),
        include_groups=False)
    gate("G3 CAGR non-increasing in the cost rung", f"{int((~mono).sum())} violations",
         "0", int((~mono).sum()) == 0)
    ident = D[(D.arm == "SPYONLY")].groupby(["panel", "gross", "cost"])["full_Sharpe"].nunique()
    gate("G4 SPYONLY Sharpe invariant to fill delay (it never trades intra-week)",
         f"max distinct = {int(ident.max())}", "1", int(ident.max()) == 1)
    gate("G5 SPY never a panel constituent", "asserted in Panel.__init__", "true", True)
    gate("G6 gross chosen on IS rows only", "structural (legs_4b_is / is_ windows)", "true", True)

    # ================================================================ HEADLINE
    say("\n### THE STANDING RUNG UNDER DEFENCE: G = 0.60, all four arms, all 8 grid points")
    st = D[(D.gross == STAND_G)]
    for pname in st.panel.unique():
        say(f"\n   -- {pname} --")
        for dl in DELAYS:
            for c in COSTS:
                d = st[(st.panel == pname) & (st.cost == c) & (st.delay == dl)]
                rk = d[d.arm == "RANK"].iloc[0]
                rd = d[d.arm == "RAND"]
                br = d[d.arm == "BREADTH"].iloc[0]
                sy = d[d.arm == "SPYONLY"].iloc[0]
                say(f"   t+{dl} {c:5.1f}bps | RANK {rk.full_CAGR:6.2%}/{rk.full_Sharpe:.3f}/"
                    f"{rk.full_MaxDD:7.2%} 4b={'Y' if rk.keep4b else 'n'}({rk.fail4b})"
                    f" | RAND med {rd.full_CAGR.median():6.2%}/{rd.full_Sharpe.median():.3f}/"
                    f"{rd.full_MaxDD.median():7.2%} 4b={int(rd.keep4b.sum())}/{len(rd)}"
                    f" | BREADTH {br.full_Sharpe:.3f} 4b={'Y' if br.keep4b else 'n'}"
                    f" | SPY{STAND_G:.2f} {sy.full_Sharpe:.3f} 4b={'Y' if sy.keep4b else 'n'}")

    say("\n### RANK minus RAND, full-sample Sharpe, at G = 0.60 "
        "(positive = the ranking is paid for)")
    piv = []
    for pname in st.panel.unique():
        for dl in DELAYS:
            for c in COSTS:
                d = st[(st.panel == pname) & (st.cost == c) & (st.delay == dl)]
                rk = d[d.arm == "RANK"].iloc[0].full_Sharpe
                rd = d[d.arm == "RAND"].full_Sharpe
                piv.append(dict(panel=pname, delay=f"t+{dl}", cost=c, RANK=rk,
                                RAND_med=rd.median(), RAND_sd=rd.std(ddof=1),
                                diff=rk - rd.median(),
                                pctile=float((rd < rk).mean()),
                                z=(rk - rd.mean()) / rd.std(ddof=1) if rd.std(ddof=1) > 0 else np.nan))
    P = pd.DataFrame(piv)
    say(P.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    say("\n### 4b PASS COUNTS over the whole grid (5 grosses x 4 costs x 2 delays x 3 panels)")
    cnt = D.groupby("arm").agg(n=("keep4b", "size"), pass4b=("keep4b", "sum"),
                               pass4a=("keep4a", "sum"))
    cnt["rate4b"] = cnt.pass4b / cnt.n
    say(cnt.to_string(float_format=lambda x: f"{x:.4f}"))
    say("\n   4b pass rate by arm x cost rung (all grosses, delays, panels):")
    bc = D.pivot_table(index="arm", columns="cost", values="keep4b", aggfunc="mean")
    say(bc.to_string(float_format=lambda x: f"{x:.4f}"))
    say("\n   4b pass rate by arm x fill delay:")
    bd = D.pivot_table(index="arm", columns="delay", values="keep4b", aggfunc="mean")
    say(bd.to_string(float_format=lambda x: f"{x:.4f}"))
    say("\n   binding 4b leg, share of FAILING cells naming each leg, by arm:")
    fl = []
    for arm in D.arm.unique():
        d = D[(D.arm == arm) & (~D.keep4b)]
        row = {"arm": arm, "n_fail": len(d)}
        for leg in ("H1", "H2", "OOS", "DD", "CAGR"):
            row[leg] = float(d.fail4b.str.contains(leg).mean()) if len(d) else np.nan
        fl.append(row)
    say(pd.DataFrame(fl).to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n### TURNOVER per year at G = 0.60 (why a cost rung can reorder the arms)")
    tv = st.pivot_table(index="arm", columns="panel", values="turnover_yr", aggfunc="median")
    say(tv.to_string(float_format=lambda x: f"{x:.2f}"))

    # ================================================================ RULE 8
    say("\n### RULE 8 -- GROSS CHOSEN ON warm-up..2016, OOS 2017-2026 READ ONCE")
    say("   OOS Sharpe by arm x cost x delay (RAND = median over 12 seeds):")
    agg = R8.groupby(["panel", "arm", "cost", "delay"]).agg(
        oos_Sharpe=("oos_Sharpe", "median"), pick=("pick_gross", "median"),
        keep4b=("keep4b", "mean")).reset_index()
    for pname in agg.panel.unique():
        say(f"\n   -- {pname} --")
        sub = agg[agg.panel == pname].pivot_table(index=["cost", "delay"], columns="arm",
                                                  values="oos_Sharpe")
        say(sub.to_string(float_format=lambda x: f"{x:.4f}"))
    say("\n   RANK minus RAND(median) OOS Sharpe, over all 24 (panel, cost, delay) cells:")
    m = agg.pivot_table(index=["panel", "cost", "delay"], columns="arm", values="oos_Sharpe")
    m["RANK-RAND"] = m["RANK"] - m["RAND"]
    m["RANK-BREADTH"] = m["RANK"] - m["BREADTH"]
    m["RANK-SPYONLY"] = m["RANK"] - m["SPYONLY"]
    say(m.to_string(float_format=lambda x: f"{x:+.4f}"))
    for col in ("RANK-RAND", "RANK-BREADTH", "RANK-SPYONLY"):
        v = m[col].dropna()
        say(f"   {col:14s}: mean {v.mean():+.4f}  SE {v.std(ddof=1)/np.sqrt(len(v)):.4f}  "
            f"t {v.mean()/(v.std(ddof=1)/np.sqrt(len(v))):+.2f}  positive at "
            f"{int((v>0).sum())} of {len(v)}")
    say(f"\n   rule-8 4b passes: " + ", ".join(
        f"{a} {int(R8[R8.arm==a].keep4b.sum())}/{len(R8[R8.arm==a])}" for a in R8.arm.unique()))
    say(f"   rule-8 4a passes: " + ", ".join(
        f"{a} {int(R8[R8.arm==a].keep4a.sum())}/{len(R8[R8.arm==a])}" for a in R8.arm.unique()))

    say("\n### THE STANDING BOOK AT THE HARSHEST GRID POINT IT IS ASKED TO SURVIVE")
    for pname in st.panel.unique():
        d = st[(st.panel == pname) & (st.arm == "RANK") & (st.cost == 25.0) & (st.delay == 2)]
        if not len(d): continue
        r = d.iloc[0]
        say(f"   {pname} RANK G=0.60 @ 25 bps, t+2: full {r.full_CAGR:7.2%} / "
            f"{r.full_Sharpe:.4f} / {r.full_MaxDD:7.2%}  halves {r.h1_Sharpe:.4f} / "
            f"{r.h2_Sharpe:.4f}  OOS {r.oos_CAGR:7.2%} / {r.oos_Sharpe:.4f} / "
            f"{r.oos_MaxDD:7.2%}  4b={'PASS' if r.keep4b else 'FAIL'} ({r.fail4b})  "
            f"4a={'PASS' if r.keep4a else 'FAIL'} ({r.fail4a})")

    D.to_csv(f"{STEM}.grid.csv", index=False)
    R8.to_csv(f"{STEM}.walkforward.csv", index=False)
    P.to_csv(f"{STEM}.rankvsrand.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)
    say(f"\n# gates {sum(g['pass_'] for g in GATES)}/{len(GATES)}  "
        f"elapsed {time.time()-t0:.0f}s")
    Path(f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
