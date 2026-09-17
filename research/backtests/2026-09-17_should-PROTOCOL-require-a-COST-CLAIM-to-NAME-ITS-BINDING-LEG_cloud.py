#!/usr/bin/env python3
"""Idea 1151 (cloud lane, 2026-09-17) — should PROTOCOL require a COST CLAIM to NAME ITS
BINDING LEG?

Idea 1098 found 1,876 of 2,088 committed cost-and-verdict sentences (0.8985) name no leg
at all, so "it dies at 25 bps" is unfalsifiable without re-running the book, and 1094 found
the leg that dies predicts c* far better than turnover does (rho -0.65).  The queue asks
for a PRICE on a one-clause stamp ("name the binding leg and its c*") against the record:
how many committed cost claims would CHANGE READING, and what does the stamp COST A RUN
THAT DOES NOT ALREADY COMPUTE A LADDER.

THE SECOND HALF IS THE ONE WITH A REAL ANSWER, AND IT IS AN IDENTITY, NOT AN ESTIMATE.
`engine.backtest` charges cost as `r_t(c) = g_t - tn_t * c/1e4` with g and tn both
INDEPENDENT OF c (weights are decided before costs are charged; the turnover series is a
property of the weight path, not of the fill price).  So the entire cost ladder of a book
is an AFFINE function of two arrays ONE run already holds, and c* for every 4b leg is a
root-find on those arrays with ZERO extra BOOK builds.  "A run that does not already
compute a ladder" does not have to compute one.  G1/G2 below prove the identity against
`engine.backtest` at four cost rungs rather than asserting it, and (B) MEASURES the
wall-clock of both routes on this run's own 216 books.

THE CENSUS HALF IS READ OUT OF 1098's OWN COMMITTED FILE, never re-harvested (1149's
lesson: today's corpus is a DIFFERENT and LARGER population, so no number would be
comparable to the 1,876 and the 212 the queue asks about).  All 2,088 rows come verbatim
from `2026-09-16_..._C.claims.csv`, with its NARROW / PROX / WIDE / names_* / leg_kinds /
has_bindverb columns carried along as the thing to be re-read.

THE TWO TUNED PARAMETERS AND NO MORE (PROTOCOL rule 4, and the queue names both):
  STAMP FORM  {S_NONE, S_LEG, S_CSTAR, S_BOTH}
  CLAIM SET   {NARROW, PROX, WIDE}
= 12 cells, EVERY ONE PUBLISHED in `.stampgrid.csv`.
NOT dials, all reported at every value: PANEL {U56, B136, SMALL}; the book population
N in {5,8,10,12,15,20,25,30,40} x H in {21,63,126,252} x CADENCE {W, M} = 72 per panel,
216 books, every one published; the four cost rungs {0, 10, 25, 50} bps; the 1-bp
measurement ladder 0..300 (a MEASUREMENT AXIS, not a dial); the four rule-8 choosers.
Frozen at 1082/1094/1098/1102/1110/1149/1159/1161's construction: CAND20 legs
[(21,252),(0,126),(0,63)], max_vol 0.60, gross 0.75, cost 10 bps headline (rule 2), LAG 1,
warm-up 260, IS end 2016-12-31, zero cash, DD cap 0.60, CAGR floor 0.70.

SURVIVORSHIP (rule 9): U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the current
constituents of a sub-$2B screen LESS every ticker with max_1d_move >= 1.0 in
data/small_meta.csv, dropped before anything else is computed.  Every CAGR and drawdown
LEVEL is optimistic and every c* is therefore an UPPER BOUND; the bias does NOT cancel out
of the 4b legs.  It does not touch the census arm at all (scans of committed text).

Writes: .gates.csv .claims.csv .stampgrid.csv .books.csv .cstar.csv .cost.csv
        .walkforward.csv .console.txt
Deterministic, standalone, no network.  Does not modify RULES.md / PROTOCOL.md / scan.py /
bot.py / baseline.py / engine.py.
"""
import sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "should-PROTOCOL-require-a-COST-CLAIM-to-NAME-ITS-BINDING-LEG"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"
LOG = []

LAG, WARMUP = 1, 260
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
GROSS0, COST0, MAXVOL0 = 0.75, 10.0, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
START = "2008-01-01"

N_LADDER = [5, 8, 10, 12, 15, 20, 25, 30, 40]
H_LADDER = [21, 63, 126, 252]
CADENCES = ["W", "M"]
COST_RUNGS = [0.0, 10.0, 25.0, 50.0]
CSTAR_HI = 300.0            # bps; the measurement ladder's ceiling, NOT a dial
CSTAR_TOL = 1e-4

STAMPS = ["S_NONE", "S_LEG", "S_CSTAR", "S_BOTH"]
CLAIMSETS = ["NARROW", "PROX", "WIDE"]
CLAIMS_SRC = (ROOT / "research" / "backtests" /
              "2026-09-16_do-the-record-s-COMMITTED-COST-CLAIMS-PRICE-the-SHARPE-LEGS-"
              "or-only-the-CAGR-FLOOR_C.claims.csv")

LEG_NAMES = ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]
LEG_KIND = {"L_H1": "SHARPE", "L_H2": "SHARPE", "L_OOS": "SHARPE",
            "L_DD": "DD", "L_CAGR": "CAGR"}


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ------------------------------------- 1082/../1161's fast runner and book, VERBATIM
def nrun(rets, wt, mk):
    T, N = rets.shape
    mk = mk.copy()
    mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return (held * rets).sum(axis=1), turn


def fmet(r):
    r = np.asarray(r, float)
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def mech(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    return (comp * (0.5 + 0.5 * above.astype(float))).values, above.values, vol20.values


def build(rank_key, elig, priced, reb, N, H, T, K, gross):
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    for i, t in enumerate(reb):
        held = np.flatnonzero(cur >= 0)
        if len(held):
            young = held[(t - cur[held]) < H]
            young = young[priced[t, young]]
        else:
            young = held
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = rank_key[t].copy()
            k[~(elig[t] & priced[t])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new_cur = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new_cur[c] = cur[c]
        for c in take:
            new_cur[c] = t
        cur = new_cur
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = gross / len(sel)
    return W


def prep(px):
    idx = px.index
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    sc, above, vol20 = mech(px)
    return dict(px=px, idx=idx, K=len(px.columns), T=len(idx),
                rets=px.pct_change().fillna(0.0).values, priced=px.notna().values,
                warm=warm, ins=ins, oos=oos, sc=sc, above=above, vol20=vol20,
                spy=px["SPY"].pct_change().fillna(0.0).values,
                mk={f: rebalance_mask(idx, f).values for f in CADENCES})


def run_gt(d, N, H, freq, gross=GROSS0, maxvol=MAXVOL0):
    """Return (gross return series, turnover series) — the TWO ARRAYS the whole cost
    ladder is an affine function of.  Neither depends on c."""
    mk = d["mk"][freq]
    mkl = np.roll(mk, LAG)
    mkl[:LAG] = False
    reb = np.flatnonzero(mk)
    el = d["above"] & (d["vol20"] < maxvol)
    W = build(-d["sc"], el, d["priced"], reb, N, H, d["T"], d["K"], gross)
    Wl = np.zeros_like(W)
    Wl[LAG:] = W[:-LAG]
    return nrun(d["rets"], Wl, mkl)


def net(g, tn, c):
    return g - tn * c / 1e4


def blocks_m(r, d):
    rr = r[d["warm"]]
    c, s, dd = fmet(rr)
    h = len(rr) // 2
    oc, os_, od = fmet(r[d["oos"]])
    ic, is_, idd = fmet(r[d["ins"]])
    return dict(CAGR=c, Sharpe=s, MaxDD=dd, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


def legs_4b(b, sb):
    return dict(L_H1=b["H1"] > sb["H1"], L_H2=b["H2"] > sb["H2"],
                L_OOS=b["OOS_Sharpe"] > sb["OOS_Sharpe"],
                L_DD=abs(b["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"]),
                L_CAGR=b["CAGR"] >= CAGR_FLOOR * sb["CAGR"])


def legs_4b_oos(b, sb):
    return dict(O_S=b["OOS_Sharpe"] > sb["OOS_Sharpe"],
                O_DD=abs(b["OOS_MaxDD"]) <= DD_CAP * abs(sb["OOS_MaxDD"]),
                O_CAGR=b["OOS_CAGR"] >= CAGR_FLOOR * sb["OOS_CAGR"])


def legs_4a(b, lbm):
    return dict(A_H1=b["H1"] > lbm["H1"], A_H2=b["H2"] > lbm["H2"],
                A_DD=b["MaxDD"] >= lbm["MaxDD"])


# --------------------------------------------------------------- THE STAMP ITSELF
def leg_margins(g, tn, c, d, sb, window="full"):
    """Every 4b leg's margin in its own sign convention: >0 means the leg PASSES.
    A leg's margin is a continuous function of c and (empirically, gated below) monotone
    decreasing, so its c* is a bisection root."""
    r = net(g, tn, c)
    m = blocks_m(r, d)
    if window == "IS":
        rr = r[d["ins"]]
        h = len(rr) // 2
        return {"L_H1": fsharpe(rr[:h]) - sb["IS_H1"],
                "L_H2": fsharpe(rr[h:]) - sb["IS_H2"],
                "L_OOS": np.nan,
                "L_DD": DD_CAP * abs(sb["IS_MaxDD"]) - abs(m["IS_MaxDD"]),
                "L_CAGR": m["IS_CAGR"] - CAGR_FLOOR * sb["IS_CAGR"]}
    return {"L_H1": m["H1"] - sb["H1"], "L_H2": m["H2"] - sb["H2"],
            "L_OOS": m["OOS_Sharpe"] - sb["OOS_Sharpe"],
            "L_DD": DD_CAP * abs(sb["MaxDD"]) - abs(m["MaxDD"]),
            "L_CAGR": m["CAGR"] - CAGR_FLOOR * sb["CAGR"]}


def cstar_leg(g, tn, d, sb, leg, window="full", lo=0.0, hi=CSTAR_HI):
    """The cost at which ONE leg flips PASS -> FAIL.  Returns 0.0 if it already fails at
    c=0 and hi (censored) if it still passes at the ceiling.  Pure arithmetic on (g, tn):
    ZERO extra book builds."""
    f = lambda c: leg_margins(g, tn, c, d, sb, window)[leg]  # noqa: E731
    if not np.isfinite(f(lo)) or f(lo) <= 0:
        return 0.0
    if f(hi) > 0:
        return hi
    a, b = lo, hi
    while b - a > CSTAR_TOL:
        m = 0.5 * (a + b)
        if f(m) > 0:
            a = m
        else:
            b = m
    return 0.5 * (a + b)


def stamp_of(g, tn, d, sb, window="full"):
    """THE ONE-CLAUSE STAMP: (binding leg, c*).  c* = min over legs; binding leg = the
    argmin.  Also returns the full per-leg c* vector, which is what makes a claim
    falsifiable without re-running the book."""
    legs = [l for l in LEG_NAMES if not (window == "IS" and l == "L_OOS")]
    cs = {l: cstar_leg(g, tn, d, sb, l, window) for l in legs}
    bind = min(cs, key=lambda l: cs[l])
    return dict(cstar=cs[bind], binding=bind, binding_kind=LEG_KIND[bind],
                **{f"cstar_{l}": cs[l] for l in legs})


def main():
    t_start = time.time()
    P("=" * 100)
    P(f"IDEA 1151 (cloud) — {SLUG}")
    P("=" * 100)
    P("TWO TUNED PARAMETERS (rule 4): STAMP FORM {S_NONE,S_LEG,S_CSTAR,S_BOTH} x")
    P("CLAIM SET {NARROW,PROX,WIDE} = 12 cells, all published in .stampgrid.csv.")
    P("PANEL, the 72-book N x H x cadence population, the 4 cost rungs and the 4 rule-8")
    P("choosers are NOT dials — all values reported everywhere.")
    P("")

    # ------------------------------------------------------------------ PANELS
    P("-" * 100)
    P("PANELS")
    P("-" * 100)
    panels = {}
    panels["U56"] = load_universe(start=START)
    panels["B136"] = load_universe(start=START, broad=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    sm = load_universe(small=True)
    dropped = [c for c in sm.columns if c in bad]
    panels["SMALL"] = sm.drop(columns=dropped)
    for pn, px in panels.items():
        P(f"  {pn:<6} {px.shape[1]:>4} cols  {px.index[0].date()}..{px.index[-1].date()}  "
          f"{len(px):,} rows")
    P(f"  SMALL dropped {len(dropped)} tickers with max_1d_move >= 1.0 (data/small_meta.csv)")
    P("  SURVIVORSHIP (rule 9): all three are CURRENT-CONSTITUENT lists; every LEVEL is")
    P("  optimistic and every c* below is an UPPER BOUND.")
    P("")

    D, BENCH = {}, {}
    for pn, px in panels.items():
        d = prep(px)
        D[pn] = d
        sb = blocks_m(d["spy"], d)
        srr = d["spy"][d["warm"]]
        sh = len(srr) // 2
        sis = d["spy"][d["ins"]]
        ish = len(sis) // 2
        sb["IS_H1"], sb["IS_H2"] = fsharpe(sis[:ish]), fsharpe(sis[ish:])
        lbm = blocks_m(backtest(px, rules_v2_weights(px), cost_bps=COST0, freq="W")["returns"]
                       .reindex(px.index).fillna(0.0).values, d)
        BENCH[pn] = dict(spy=sb, live=lbm)
        P(f"  {pn:<6} SPY   {sb['CAGR']:7.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:7.2%}"
          f"  halves {sb['H1']:.4f}/{sb['H2']:.4f}"
          f"  | OOS {sb['OOS_CAGR']:7.2%} / {sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:7.2%}")
        P(f"  {pn:<6} LIVE  {lbm['CAGR']:7.2%} / {lbm['Sharpe']:.4f} / {lbm['MaxDD']:7.2%}"
          f"  halves {lbm['H1']:.4f}/{lbm['H2']:.4f}"
          f"  | OOS {lbm['OOS_CAGR']:7.2%} / {lbm['OOS_Sharpe']:.4f} / {lbm['OOS_MaxDD']:7.2%}")
    P("")

    # ------------------------------------------------------------------ GATES
    P("-" * 100)
    P("GATES — the identity the whole 'price' answer rests on is PROVED, not asserted")
    P("-" * 100)
    gates = []

    def gate(name, what, value, ok):
        gates.append(dict(gate=name, what=what, value=value, pass_=bool(ok)))
        P(f"  {name:<5} {'PASS' if ok else 'FAIL'}  {what}  = {value}")

    d0 = D["U56"]
    px0 = panels["U56"]
    g0, tn0 = run_gt(d0, 20, 126, "W")

    # G1/G2: r(c) = g - tn*c/1e4 reproduces engine.backtest at EVERY cost rung.
    mk = d0["mk"]["W"]
    reb = np.flatnonzero(mk)
    el = d0["above"] & (d0["vol20"] < MAXVOL0)
    Wm = build(-d0["sc"], el, d0["priced"], reb, 20, 126, d0["T"], d0["K"], GROSS0)
    Wdf = pd.DataFrame(Wm, index=px0.index, columns=px0.columns)
    worst = 0.0
    for c in COST_RUNGS:
        eng = backtest(px0, Wdf, cost_bps=c, freq="W")["returns"].reindex(px0.index).fillna(0.0).values
        ours = net(g0, tn0, c)
        worst = max(worst, float(np.abs(eng[WARMUP:] - ours[WARMUP:]).max()))
    gate("G1", "r(c)=g-tn*c/1e4 == engine.backtest at 0/10/25/50 bps (max abs dev)",
         f"{worst:.3e}", worst < 5e-15)
    # G2: g and tn do NOT depend on c at all (the affine claim's premise)
    g1, tn1 = run_gt(d0, 20, 126, "W")
    gate("G2", "(g, tn) deterministic and c-free across calls",
         f"{float(np.abs(g1-g0).max()):.3e}", np.abs(g1 - g0).max() == 0.0)
    # G3: the incumbent anchor
    m_inc = blocks_m(net(g0, tn0, COST0), d0)
    P(f"  incumbent U56 W/H126/N=20/gross 0.75 @10bps: CAGR {m_inc['CAGR']:.6f} "
      f"Sharpe {m_inc['Sharpe']:.6f} MaxDD {m_inc['MaxDD']:.6f}")
    for nm, got, want in (("G3", m_inc["CAGR"], 0.155787), ("G4", m_inc["Sharpe"], 1.139701),
                          ("G5", m_inc["MaxDD"], -0.191276)):
        gate(nm, f"incumbent anchor vs committed {want}", round(float(got), 6),
             abs(got - want) <= 5e-3)
    # G6: every 4b leg margin is MONOTONE DECREASING in c (bisection is legal)
    grid = np.linspace(0, CSTAR_HI, 61)
    mono_bad = 0
    mono_tested = 0
    for (N, H, f) in ((20, 126, "W"), (12, 21, "W"), (40, 252, "M"), (5, 63, "M")):
        gg, tt = run_gt(d0, N, H, f)
        for leg in LEG_NAMES:
            v = [leg_margins(gg, tt, c, d0, BENCH["U56"]["spy"])[leg] for c in grid]
            mono_tested += 1
            if np.nanmax(np.diff(v)) > 1e-9:
                mono_bad += 1
    gate("G6", f"4b leg margin monotone decreasing in c ({mono_tested} book-legs)",
         f"{mono_tested - mono_bad}/{mono_tested}", mono_bad == 0)
    # G7: the bisection recovers a leg's flip to within tolerance of a 1-bp scan
    st = stamp_of(g0, tn0, d0, BENCH["U56"]["spy"])
    scan = np.arange(0.0, CSTAR_HI + 1e-9, 1.0)
    passes = [all(legs_4b(blocks_m(net(g0, tn0, c), d0), BENCH["U56"]["spy"]).values()) for c in scan]
    if all(passes):
        c_scan = CSTAR_HI
    elif not passes[0]:
        c_scan = 0.0
    else:
        c_scan = scan[int(np.argmin(passes)) - 1]
    gate("G7", "bisection c* within 1 bp of a 1-bp brute-force scan",
         f"{st['cstar']:.4f} vs {c_scan:.1f}", abs(st["cstar"] - c_scan) <= 1.0 + 1e-6)
    # G8: the committed claims population is read verbatim from 1098's own file
    cl = pd.read_csv(CLAIMS_SRC)
    gate("G8", "1098's committed claims file: 2,088 rows", len(cl), len(cl) == 2088)
    gate("G9", "1098's headline reproduced: leg_kinds==NONE",
         int((cl.leg_kinds == "NONE").sum()), int((cl.leg_kinds == "NONE").sum()) == 1876)
    gate("G10", "1098's committed resolved / resolved_loose",
         f"{int(cl.resolved.sum())} / {int(cl.resolved_loose.sum())}",
         int(cl.resolved.sum()) == 82 and int(cl.resolved_loose.sum()) == 425)
    P("")

    # ------------------------------------------------------- (A) THE CENSUS / READING
    P("-" * 100)
    P("(A) HOW MANY COMMITTED COST CLAIMS CHANGE READING — 1098's own 2,088 rows")
    P("-" * 100)
    cl["names_leg"] = cl.leg_kinds != "NONE"
    cl["names_one_leg"] = cl.leg_kind_n == 1
    cl["names_cstar"] = cl.NUMERIC.astype(bool)
    cl["bind_no_leg"] = cl.has_bindverb & ~cl.names_leg
    P(f"  names a leg at all           {int(cl.names_leg.sum()):>5} / 2088  "
      f"({cl.names_leg.mean():.4f})")
    P(f"  names EXACTLY ONE leg        {int(cl.names_one_leg.sum()):>5} / 2088  "
      f"({cl.names_one_leg.mean():.4f})   <- the only shape a 'binding leg' reading needs")
    P(f"  names a NUMERIC c*           {int(cl.names_cstar.sum()):>5} / 2088  "
      f"({cl.names_cstar.mean():.4f})")
    P(f"  uses a BINDING VERB          {int(cl.has_bindverb.sum()):>5} / 2088")
    P(f"  BINDING VERB and NO LEG      {int(cl.bind_no_leg.sum()):>5} / 2088  "
      f"({cl.bind_no_leg.mean():.4f})   <- 1151's unfalsifiable sentence, exactly")
    P(f"  names a leg AND a c*         {int((cl.names_leg & cl.names_cstar).sum()):>5} / 2088")
    P("")

    rows = []
    for cs in CLAIMSETS:
        sub = cl[cl[cs].astype(bool)]
        n = len(sub)
        for s in STAMPS:
            if s == "S_NONE":
                supplied = pd.Series(False, index=sub.index)
            elif s == "S_LEG":
                supplied = ~sub.names_one_leg
            elif s == "S_CSTAR":
                supplied = ~sub.names_cstar
            else:
                supplied = ~(sub.names_one_leg & sub.names_cstar)
            rows.append(dict(
                stamp=s, claimset=cs, n_claims=n,
                n_changes_reading=int(supplied.sum()),
                share_changes=float(supplied.mean()) if n else np.nan,
                n_already_complete=int((~supplied).sum()),
                n_bind_no_leg=int(sub.bind_no_leg.sum()),
                n_names_leg=int(sub.names_leg.sum()),
                n_names_cstar=int(sub.names_cstar.sum()),
                n_multi_leg=int((sub.leg_kind_n > 1).sum()),
                n_rescorable=int(sub.resolved.sum())))
    sg = pd.DataFrame(rows)
    dump(sg, "stampgrid")
    P("  SHARE OF CLAIMS WHOSE READING THE STAMP CHANGES (all 12 cells):")
    P("  " + sg.pivot(index="stamp", columns="claimset",
                      values="share_changes").loc[STAMPS, CLAIMSETS].round(4)
      .to_string().replace("\n", "\n  "))
    P("")
    P("  COUNTS:")
    P("  " + sg.pivot(index="stamp", columns="claimset",
                      values="n_changes_reading").loc[STAMPS, CLAIMSETS]
      .to_string().replace("\n", "\n  "))
    P("")
    cl_out = cl[["NARROW", "PROX", "WIDE", "NUMERIC", "leg_kinds", "leg_kind_n",
                 "has_bindverb", "names_leg", "names_one_leg", "names_cstar",
                 "bind_no_leg", "resolved", "resolved_loose", "src", "line"]].copy()
    dump(cl_out, "claims")

    # ------------------------------------------------- THE BOOK POPULATION + c* CENSUS
    P("-" * 100)
    P("(B) THE BOOK POPULATION — 3 panels x 9 N x 4 H x 2 cadences = 216 books")
    P("-" * 100)
    t_books0 = time.time()
    GT, brows = {}, []
    nbooks = 0
    for pn in ("U56", "B136", "SMALL"):
        d, sb, lbm = D[pn], BENCH[pn]["spy"], BENCH[pn]["live"]
        for f in CADENCES:
            for N in N_LADDER:
                for H in H_LADDER:
                    g, tn = run_gt(d, N, H, f)
                    GT[(pn, f, N, H)] = (g, tn)
                    nbooks += 1
                    row = dict(panel=pn, cadence=f, N=N, H=H)
                    for c in COST_RUNGS:
                        m = blocks_m(net(g, tn, c), d)
                        l4b = legs_4b(m, sb)
                        l4bo = legs_4b_oos(m, sb)
                        l4a = legs_4a(m, lbm)
                        tag = f"c{int(c)}"
                        row[f"{tag}_CAGR"] = m["CAGR"]
                        row[f"{tag}_Sharpe"] = m["Sharpe"]
                        row[f"{tag}_MaxDD"] = m["MaxDD"]
                        row[f"{tag}_H1"], row[f"{tag}_H2"] = m["H1"], m["H2"]
                        row[f"{tag}_OOS_CAGR"] = m["OOS_CAGR"]
                        row[f"{tag}_OOS_Sharpe"] = m["OOS_Sharpe"]
                        row[f"{tag}_OOS_MaxDD"] = m["OOS_MaxDD"]
                        row[f"{tag}_pass4b"] = bool(all(l4b.values()))
                        row[f"{tag}_pass4b_oos"] = bool(all(l4bo.values()))
                        row[f"{tag}_pass4a"] = bool(all(l4a.values()))
                    row["ann_turnover"] = float(tn.sum() / (len(tn) / 252.0))
                    brows.append(row)
            P(f"  {pn:<6} {f}  {len(N_LADDER)*len(H_LADDER)} books built")
    t_books = time.time() - t_books0
    books = pd.DataFrame(brows)
    dump(books, "books")
    P(f"  {nbooks} books in {t_books:.1f}s ({t_books/nbooks:.2f}s per book)")
    P("")
    P("  BASE RATES at each cost rung (context for every share above):")
    P(f"  {'panel':<7}{'rung':>6}{'4b full':>10}{'4b OOS':>10}{'4a':>8}")
    for pn in ("U56", "B136", "SMALL"):
        s = books[books.panel == pn]
        for c in COST_RUNGS:
            t = f"c{int(c)}"
            P(f"  {pn:<7}{int(c):>6}{int(s[t+'_pass4b'].sum()):>6}/{len(s):<3}"
              f"{int(s[t+'_pass4b_oos'].sum()):>6}/{len(s):<3}{int(s[t+'_pass4a'].sum()):>4}/{len(s):<3}")
    P("")

    # the c* stamp for every book — ZERO extra book builds
    P("-" * 100)
    P("THE STAMP, COMPUTED FOR ALL 216 BOOKS — per-leg c* by bisection on (g, tn)")
    P("-" * 100)
    t_st0 = time.time()
    srows = []
    for (pn, f, N, H), (g, tn) in GT.items():
        d, sb = D[pn], BENCH[pn]["spy"]
        stf = stamp_of(g, tn, d, sb, "full")
        sti = stamp_of(g, tn, d, sb, "IS")
        srows.append(dict(panel=pn, cadence=f, N=N, H=H,
                          **{f"full_{k}": v for k, v in stf.items()},
                          **{f"IS_{k}": v for k, v in sti.items()},
                          ann_turnover=float(tn.sum() / (len(tn) / 252.0))))
    t_stamp = time.time() - t_st0
    cst = pd.DataFrame(srows)
    dump(cst, "cstar")
    P(f"  216 stamps in {t_stamp:.1f}s, ZERO extra book builds")
    P("")
    P("  BINDING LEG distribution over the 216 books (full sample):")
    for k, v in cst.full_binding.value_counts().items():
        P(f"    {k:<8} {v:>4}  ({v/len(cst):.4f})")
    P("  by KIND:")
    for k, v in cst.full_binding_kind.value_counts().items():
        P(f"    {k:<8} {v:>4}  ({v/len(cst):.4f})")
    P("")
    live = cst[cst.full_cstar > 0]
    P(f"  books alive at 0 bps: {len(live)} of {len(cst)}; among them median c* "
      f"{live.full_cstar.median():.2f} bps, IQR "
      f"{live.full_cstar.quantile(.25):.2f}..{live.full_cstar.quantile(.75):.2f}")
    P("")
    P("  1094's CHECK — does the BINDING LEG order c* better than TURNOVER does?")

    def spearman(x, y):
        x, y = np.asarray(x, float), np.asarray(y, float)
        ok = np.isfinite(x) & np.isfinite(y)
        if ok.sum() < 3:
            return np.nan
        rx, ry = pd.Series(x[ok]).rank().values, pd.Series(y[ok]).rank().values
        if rx.std() == 0 or ry.std() == 0:
            return 0.0
        return float(np.corrcoef(rx, ry)[0, 1])

    rho_turn = spearman(live.ann_turnover, live.full_cstar)
    P(f"    spearman(annual turnover, c*) over the {len(live)} live books = {rho_turn:+.4f}")
    grp = live.groupby("full_binding").full_cstar.agg(["count", "median"])
    P("    c* by binding leg:")
    for leg, r in grp.iterrows():
        P(f"      {leg:<8} n={int(r['count']):>4}  median c* {r['median']:.2f} bps")
    # between-group share of variance in rank(c*) explained by the binding leg
    rk = pd.Series(live.full_cstar).rank().values
    gidx = pd.Categorical(live.full_binding).codes
    tot = float(rk.var())
    within = float(sum(rk[gidx == k].var() * (gidx == k).sum()
                       for k in np.unique(gidx)) / len(rk)) if tot else np.nan
    eta2 = (1.0 - within / tot) if tot else np.nan
    P(f"    eta^2 of rank(c*) explained by the BINDING LEG = {eta2:.4f}, "
      f"against rho^2 for turnover = {rho_turn**2:.4f}")
    P("")

    # ------------------------------------------------------------------ THE PRICE
    P("-" * 100)
    P("THE PRICE — what the stamp asks of A RUN THAT DOES NOT ALREADY COMPUTE A LADDER")
    P("-" * 100)
    # route 1: the naive ladder — re-run the book at every cost rung through engine.backtest
    t0 = time.time()
    for c in COST_RUNGS:
        backtest(px0, Wdf, cost_bps=c, freq="W")
    t_engine_ladder = time.time() - t0
    t0 = time.time()
    backtest(px0, Wdf, cost_bps=COST0, freq="W")
    t_engine_one = time.time() - t0
    # route 2: the stamp — bisection on (g, tn) the run already holds
    t0 = time.time()
    stamp_of(g0, tn0, d0, BENCH["U56"]["spy"], "full")
    t_one_stamp = time.time() - t0
    t0 = time.time()
    _ = run_gt(d0, 20, 126, "W")
    t_one_book = time.time() - t0
    crows = [
        dict(route="S_NONE (status quo)", extra_book_builds=0, extra_engine_calls=0,
             seconds_per_claim=0.0, note="one book at one cost rung; the record's habit"),
        dict(route="S_CSTAR / S_LEG / S_BOTH via (g,tn)", extra_book_builds=0,
             extra_engine_calls=0, seconds_per_claim=round(t_one_stamp, 4),
             note="bisection on two arrays the run ALREADY holds; 5 legs, 1e-4 bp tol"),
        dict(route="a 4-rung cost LADDER via engine.backtest", extra_book_builds=0,
             extra_engine_calls=len(COST_RUNGS) - 1,
             seconds_per_claim=round(t_engine_ladder - t_engine_one, 4),
             note="what a run without a ladder would naively pay; still 0 extra BOOK builds"),
        dict(route="a 4-rung ladder re-BUILDING the book each rung", extra_book_builds=3,
             extra_engine_calls=0, seconds_per_claim=round(3 * t_one_book, 4),
             note="the worst case the queue has in mind; unnecessary — see G1/G2"),
    ]
    cost = pd.DataFrame(crows)
    cost["pct_of_one_book"] = (cost.seconds_per_claim / t_one_book * 100).round(2)
    dump(cost, "cost")
    P("  " + cost.to_string(index=False).replace("\n", "\n  "))
    P("")
    P(f"  ONE BOOK BUILD = {t_one_book:.3f}s.  THE WHOLE STAMP = {t_one_stamp:.3f}s "
      f"({t_one_stamp/t_one_book*100:.1f}% of one book) and ZERO extra book builds,")
    P(f"  because G1 proves r(c) is AFFINE in c on arrays the run already holds.  All 216")
    P(f"  stamps together cost {t_stamp:.1f}s against {t_books:.1f}s to build the books "
      f"({t_stamp/t_books*100:.1f}%).")
    P("")

    # ------------------------------------------------------------------ (C) RULE 8
    P("-" * 100)
    P("(C) RULE 8 — choosers read 2009-2016 ONLY; picks evaluated on untouched 2017-2026")
    P("-" * 100)
    P("  CH_ISSHARPE  plain IS Sharpe argmax at 10 bps                  (the record's habit)")
    P("  CH_CSTAR     argmax of IS c* — the STAMP-AWARE chooser, maximum cost headroom")
    P("  CH_LEGFILT   IS Sharpe argmax among books whose IS binding leg is NOT the CAGR")
    P("               floor (1094 found that leg decorative for selection)")
    P("  CH_TENT      argmax of the IS 4b margin (1150/1154's object)             (control)")
    P("")
    wrows = []
    for pn in ("U56", "B136", "SMALL"):
        d, sb, lbm = D[pn], BENCH[pn]["spy"], BENCH[pn]["live"]
        for f in CADENCES:
            cand = cst[(cst.panel == pn) & (cst.cadence == f)].copy()
            key = []
            for _, r in cand.iterrows():
                g, tn = GT[(pn, f, int(r.N), int(r.H))]
                m = blocks_m(net(g, tn, COST0), d)
                cap = DD_CAP * abs(sb["IS_MaxDD"])
                flo = CAGR_FLOOR * sb["IS_CAGR"]
                key.append(dict(IS_Sharpe=m["IS_Sharpe"],
                                tent_IS=min((m["IS_Sharpe"] - sb["IS_Sharpe"]) / abs(sb["IS_Sharpe"]),
                                            (cap - abs(m["IS_MaxDD"])) / cap,
                                            (m["IS_CAGR"] - flo) / abs(flo))))
            cand = pd.concat([cand.reset_index(drop=True),
                              pd.DataFrame(key)], axis=1)
            nocagr = cand[cand.IS_binding != "L_CAGR"]
            picks = {
                "CH_ISSHARPE": cand.loc[cand.IS_Sharpe.idxmax()],
                "CH_CSTAR": cand.loc[cand.IS_cstar.idxmax()],
                "CH_LEGFILT": (nocagr.loc[nocagr.IS_Sharpe.idxmax()] if len(nocagr)
                               else cand.loc[cand.IS_Sharpe.idxmax()]),
                "CH_TENT": cand.loc[cand.tent_IS.idxmax()],
            }
            for ch, pr in picks.items():
                N, H = int(pr.N), int(pr.H)
                g, tn = GT[(pn, f, N, H)]
                m = blocks_m(net(g, tn, COST0), d)
                l4b, l4bo, l4a = legs_4b(m, sb), legs_4b_oos(m, sb), legs_4a(m, lbm)
                stf = stamp_of(g, tn, d, sb, "full")
                wrows.append(dict(
                    chooser=ch, panel=pn, cadence=f, N=N, H=H,
                    IS_Sharpe=pr.IS_Sharpe, IS_cstar=pr.IS_cstar, IS_binding=pr.IS_binding,
                    FULL_CAGR=m["CAGR"], FULL_Sharpe=m["Sharpe"], FULL_MaxDD=m["MaxDD"],
                    H1=m["H1"], H2=m["H2"],
                    OOS_CAGR=m["OOS_CAGR"], OOS_Sharpe=m["OOS_Sharpe"], OOS_MaxDD=m["OOS_MaxDD"],
                    full_cstar=stf["cstar"], full_binding=stf["binding"],
                    SPY_Sharpe=sb["Sharpe"], SPY_H1=sb["H1"], SPY_H2=sb["H2"],
                    SPY_CAGR=sb["CAGR"], SPY_MaxDD=sb["MaxDD"],
                    SPY_OOS_Sharpe=sb["OOS_Sharpe"], SPY_OOS_CAGR=sb["OOS_CAGR"],
                    SPY_OOS_MaxDD=sb["OOS_MaxDD"], LIVE_OOS_Sharpe=lbm["OOS_Sharpe"],
                    pass_4b=bool(all(l4b.values())), pass_4b_oos=bool(all(l4bo.values())),
                    pass_4a=bool(all(l4a.values())),
                    **{f"leg_{k}": bool(v) for k, v in l4b.items()},
                    **{f"legO_{k}": bool(v) for k, v in l4bo.items()}))
    wf = pd.DataFrame(wrows)
    dump(wf, "walkforward")
    CH = ("CH_ISSHARPE", "CH_CSTAR", "CH_LEGFILT", "CH_TENT")
    P("  CHOOSER SCOREBOARD (6 picks each; OOS 2017-2026 never read by any chooser):")
    P(f"  {'chooser':<13}{'medOOS_Sh':>11}{'meanOOS_Sh':>12}{'>SPY OOS':>10}"
      f"{'4b full':>9}{'4b OOS':>9}{'4a':>6}{'med c*':>9}")
    for ch in CH:
        q = wf[wf.chooser == ch]
        P(f"  {ch:<13}{q.OOS_Sharpe.median():>11.4f}{q.OOS_Sharpe.mean():>12.4f}"
          f"{int((q.OOS_Sharpe > q.SPY_OOS_Sharpe).sum()):>7}/{len(q):<2}"
          f"{int(q.pass_4b.sum()):>6}/{len(q):<2}{int(q.pass_4b_oos.sum()):>6}/{len(q):<2}"
          f"{int(q.pass_4a.sum()):>3}/{len(q):<2}{q.full_cstar.median():>9.1f}")
    P("")
    P("  EVERY PICK (chooser, panel, cadence) -> full and OOS, against SPY:")
    for _, r in wf.iterrows():
        P(f"    {r.chooser:<12}{r.panel:<6}{r.cadence}  N={r.N:<3}H={r.H:<4} "
          f"full {r.FULL_CAGR:7.2%}/{r.FULL_Sharpe:.4f}/{r.FULL_MaxDD:7.2%} "
          f"halves {r.H1:.3f}/{r.H2:.3f} | OOS {r.OOS_CAGR:7.2%}/{r.OOS_Sharpe:.4f}/"
          f"{r.OOS_MaxDD:7.2%} | c* {r.full_cstar:6.1f} bind {r.full_binding:<7} "
          f"4b {'Y' if r.pass_4b else 'n'}{'Y' if r.pass_4b_oos else 'n'} "
          f"4a {'Y' if r.pass_4a else 'n'}")
    P("")
    best = books.copy()
    okf = best[best.c10_pass4b & best.c10_pass4b_oos]
    P(f"  ACROSS ALL 216 BOOKS at 10 bps: 4b full {int(best.c10_pass4b.sum())}, "
      f"4b OOS {int(best.c10_pass4b_oos.sum())}, BOTH {len(okf)}, 4a {int(best.c10_pass4a.sum())}.")
    if len(okf):
        P("  the books clearing 4b FULL AND OOS at 10 bps:")
        for _, r in okf.sort_values("c10_Sharpe", ascending=False).iterrows():
            cc = cst[(cst.panel == r.panel) & (cst.cadence == r.cadence) &
                     (cst.N == r.N) & (cst.H == r.H)].iloc[0]
            P(f"    {r.panel:<6}{r.cadence} N={int(r.N):<3}H={int(r.H):<4} "
              f"{r.c10_CAGR:7.2%}/{r.c10_Sharpe:.4f}/{r.c10_MaxDD:7.2%} "
              f"halves {r.c10_H1:.3f}/{r.c10_H2:.3f} | OOS {r.c10_OOS_CAGR:7.2%}/"
              f"{r.c10_OOS_Sharpe:.4f}/{r.c10_OOS_MaxDD:7.2%} | c* {cc.full_cstar:6.1f} "
              f"bind {cc.full_binding}")
    P("")

    gdf = pd.DataFrame(gates)
    dump(gdf, "gates")
    P(f"GATES {int(gdf.pass_.sum())} of {len(gdf)} PASS")
    P(f"TOTAL RUNTIME {time.time()-t_start:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
