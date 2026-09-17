#!/usr/bin/env python3
"""Idea 1161 (cloud lane, 2026-09-17) — does the TENT CHOOSER reach the INTERIOR on a
ROLLING IS WINDOW, or only on the ONE-SHOT SPLIT?

Idea 1154 found C_IS4B — the min of the three IS-only 4b leg margins (M_S, M_DD, M_CAGR) —
is the ONE chooser on the 33-rung gross ladder that is not monotone, because a min of two
oppositely-sloped monotone legs is a TENT, and a tent peaks in the INTERIOR.  It picked
gross 0.625 (U56) / 0.575 (B136) and was the only chooser whose pick cleared 4b full AND
4b OOS.  But it chose ONCE, on 2009-01..2016-12-31, and was then scored on the untouched
remainder.  A single honest choice is still a single draw.

THE QUEUE ASKS THREE THINGS AND THIS RUN ANSWERS ALL THREE:
  (Q1) re-run C_IS4B as a ROLLING, periodically re-chosen rule — does the tent still reach
       the interior once the window moves, or was 0.625 an artefact of that one window?
  (Q2) how often does the PICK MOVE, and what does the moving COST in turnover?
  (Q3) does the 4b OOS pass SURVIVE being re-chosen instead of chosen once?

THE TWO TUNED PARAMETERS AND NO MORE (PROTOCOL rule 4), exactly the two the queue names:
  WINDOW   {W504 (2y), W756 (3y), W1260 (5y), WEXP (expanding since warm-up)}
  CADENCE  {R6M, R1Y, R2Y}   (re-choice cadence)
= 12 (window, cadence) cells per panel, 24 in all, EVERY ONE PUBLISHED in `.cells.csv`.
The RUNG of the gross ladder is NOT a third parameter — it is the object the chooser
selects (1154's framing, kept verbatim), and all 33 rungs of both panels are published in
`.grid.csv` whatever any chooser did with them.  PANEL {U56, B136} is NOT a dial: both are
reported everywhere and nothing is ever selected on the pair.

THE COMMON SPAN, DECLARED BEFORE ANY NUMBER AND THE REASON FOR IT.  A rolling chooser
cannot choose until warm-up plus one window of bars exist, so the four windows would
otherwise be scored on four different tapes and could not be compared.  Every cell, every
control and every benchmark in this run is therefore scored on the SAME span, starting at
bar WARMUP + max(window) = 260 + 1260 = 1520 (2014-01-21), and WEXP is given the same first
choice date so the windows differ in LOOKBACK only, never in scored tape.  All full-sample,
half and OOS figures below are on that common span and are NOT comparable to 1154's
full-tape figures, which start at bar 260; 1154's own numbers are reproduced on 1154's span
in gate G8 and quoted from its file, never re-derived.

CONTROLS, computed at every cell and never selected on:
  K_FROZEN  the incumbent constant gross 0.75 (the live default)
  K_ONESHOT 1154's one-shot C_IS4B pick held constant (0.625 U56 / 0.575 B136) — the object
            the queue is asking whether rolling improves on
  K_ORACLE  the best full-sample-Sharpe constant rung, un-attainable, reported as a ceiling
  SPY and live RULES v2, on the same common span

PRICE VINTAGE, PINNED AND DECLARED (idea 1160's defect, 1163 open on it).  `data/prices.csv`
is rewritten nightly; every tape here is truncated at PIN = 2026-09-15 so 1154's committed
anchors reproduce, and G2 is reported BOTH ways so the vintage is published, not absorbed.

FROZEN at 1082/1094/1098/1102/1108/1110/1116/1117/1118/1150/1154's construction so the
numbers cross-read: CAND20 legs [(21,252),(0,126),(0,63)], cap INF, max_vol 0.60, min hold
126, N=20, cadence W, cost 10 bps (PROTOCOL rule 2 — a book cannot choose its cost rate),
LAG 1, warm-up 260, zero cash, block L=63, 1000 draws, crc32 seeds, q=0.90.

Writes: .gates.csv .grid.csv .cells.csv .picks.csv .moves.csv .hypotheses.csv
        .walkforward.csv .console.txt
Deterministic, standalone, no network.  Does not modify RULES.md / scan.py / bot.py /
baseline.py / PROTOCOL.md.
"""
import sys, time, zlib
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "does-the-TENT-CHOOSER-reach-the-INTERIOR-on-a-ROLLING-IS-WINDOW"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

PIN = "2026-09-15"
LAG, WARMUP, MAXVOL0 = 1, 260, 0.60
IS_END = "2016-12-31"                 # the record's canonical split, kept for continuity
DD_CAP, CAGR_FLOOR = 0.60, 0.70
GROSS0, FREQ0, HOLD0, N0, COST0 = 0.75, "W", 126, 20, 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]
PANELS = ["U56", "B136"]

GROSS_LADDER = [round(0.20 + 0.025 * i, 3) for i in range(33)]   # 1150/1154's ladder, verbatim

# ------------------------------------------------------------------ THE TWO DIALS (and no more)
WINDOWS = {"W504": 504, "W756": 756, "W1260": 1260, "WEXP": -1}   # -1 = expanding
CADENCES = {"R6M": 126, "R1Y": 252, "R2Y": 504}                   # bars between re-choices
MAXWIN = 1260
COMMON_START = WARMUP + MAXWIN                                    # 1520

Q_HEAD, L_HEAD, BDRAWS, SEED_BASE = 0.90, 63, 1000, 11611161

# committed cross-run anchors (quoted from their own files, never re-derived)
A936_WH126 = (0.155787, 1.139701, -0.191276)      # U56 W/H126/N=20, 10 bps, full tape
A1098_U56_N12 = (0.1771, 1.1692, -0.2017)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
A1154_IS4B = {"U56": 0.625, "B136": 0.575}        # the object this run extends (G8)

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def seed_of(*parts):
    return SEED_BASE + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


# ------------------------------------------- 1082/1098/1102/1108/1117/1150/1154's fast runner
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


def legs_composite(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return sum(parts) / len(parts)


def mech(px):
    comp = legs_composite(px)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, above.values, vol20.values


def build(rank_key, elig, priced, reb, N, H, T, K, gross):
    """1154's build, generalised in ONE way: `gross` may be a scalar OR an array of length
    len(reb) giving the gross in force from rebalance date reb[i] forward.  With a constant
    array it is bit-identical to the scalar path (gate G9)."""
    garr = np.full(len(reb), float(gross)) if np.isscalar(gross) else np.asarray(gross, float)
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
            W[t:stop, sel] = garr[i] / len(sel)
    return W


def windows_of(idx):
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    return warm, ins, oos


def span_m(r, mask, oos_mask):
    """Metrics of return stream r restricted to `mask` (the COMMON SPAN), plus halves of that
    span and the record's canonical post-2016 sub-span."""
    rr = r[mask]
    c, s, d = fmet(rr)
    h = len(rr) // 2
    om = oos_mask & mask
    oc, os_, od = fmet(r[om])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


def legs_4b(b, sb):
    return {"L_H1": bool(b["H1"] > sb["H1"]), "L_H2": bool(b["H2"] > sb["H2"]),
            "L_OOS": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "L_DD": bool(abs(b["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"])),
            "L_CAGR": bool(b["CAGR"] >= CAGR_FLOOR * sb["CAGR"])}


def legs_4b_oos(b, sb):
    return {"O_S": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "O_DD": bool(abs(b["OOS_MaxDD"]) <= DD_CAP * abs(sb["OOS_MaxDD"])),
            "O_CAGR": bool(b["OOS_CAGR"] >= CAGR_FLOOR * sb["OOS_CAGR"])}


def legs_4a(b, lbm):
    return {"A_H1": bool(b["H1"] > lbm["H1"]), "A_H2": bool(b["H2"] > lbm["H2"]),
            "A_DD": bool(b["MaxDD"] >= lbm["MaxDD"])}


# ---------------------------------------------------------- THE TENT CHOOSER (1154's C_IS4B)
# On ANY window [a, b) the three legs are the signed fraction of their own 4b bar still in
# hand, computed on that window only, and C_IS4B maximises the MINIMUM of the three.  The
# only change from 1154 is WHICH window — there it was 2009-01..2016-12-31 once.
def tent_score(rb, rs):
    """rb, rs: book and SPY daily returns over the SAME choosing window."""
    bc, bs, bd = fmet(rb)
    sc, ss, sd = fmet(rs)
    cap = DD_CAP * abs(sd)
    flo = CAGR_FLOOR * sc
    m_s = (bs - ss) / abs(ss) if ss else np.nan
    m_dd = (cap - abs(bd)) / cap if cap else np.nan
    m_cagr = (bc - flo) / abs(flo) if flo else np.nan
    return min(m_s, m_dd, m_cagr), m_s, m_dd, m_cagr


def cadence_mask(idx, spec):
    if spec in ("D", "W", "M", "Q"):
        return rebalance_mask(idx, spec).values.copy()
    k, base = int(spec[:-1]), spec[-1]
    hit = np.flatnonzero(rebalance_mask(idx, base).values)
    m = np.zeros(len(idx), dtype=bool)
    m[hit[::k]] = True
    return m


def block_index(rng, T, L, ndraws):
    nb = int(np.ceil(T / L))
    st = rng.integers(0, T, size=(ndraws, nb))
    off = np.arange(L)
    idx = (st[:, :, None] + off[None, None, :]) % T
    return idx.reshape(ndraws, nb * L)


def main():
    t0 = time.time()
    P(f"# Idea 1161 (cloud lane, {DATE}) — does the TENT CHOOSER reach the INTERIOR on a")
    P("#   ROLLING IS WINDOW, or only on the ONE-SHOT SPLIT?")
    P("#")
    P("# 1154: C_IS4B = min(M_S, M_DD, M_CAGR) on the IS window is the ONE non-monotone chooser")
    P("#   on the 33-rung gross ladder (a min of two oppositely-sloped monotone legs is a TENT),")
    P("#   picked 0.625 (U56) / 0.575 (B136) and was the only chooser clearing 4b full AND OOS.")
    P("#   It chose ONCE.  This run re-chooses it on a rolling window and asks whether the")
    P("#   interior pick, and the 4b OOS pass, are properties of the CHOOSER or of THAT WINDOW.")
    P("#")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4, the two the queue names): WINDOW {list(WINDOWS)}")
    P(f"#   x CADENCE {list(CADENCES)} = {len(WINDOWS) * len(CADENCES)} cells per panel, "
      f"{len(WINDOWS) * len(CADENCES) * len(PANELS)} in all, EVERY ONE PUBLISHED.")
    P("#   The gross RUNG is NOT a third parameter: it is the object the chooser selects")
    P(f"#   (1154's framing).  All {len(GROSS_LADDER)} rungs of both panels are in .grid.csv.")
    P("# PANEL {U56, B136} is NOT a dial (both reported everywhere, nothing selected on the pair).")
    P(f"# COMMON SPAN: every cell, control and benchmark scored from bar {COMMON_START} "
      f"(= warm-up {WARMUP} + longest window {MAXWIN}) so the four windows differ in LOOKBACK")
    P("#   only, never in scored tape.  These figures are NOT comparable to 1154's full-tape")
    P("#   ones (which start at bar 260); 1154's own numbers are replayed in G8 on 1154's span.")
    P(f"# FROZEN: CAND20 legs {LEGS}, cap INF, max_vol {MAXVOL0}, min hold {HOLD0}, N {N0},")
    P(f"#   cadence {FREQ0}, cost {COST0} bps (rule 2), LAG {LAG}, warm-up {WARMUP}, zero cash,")
    P(f"#   block L={L_HEAD}, {BDRAWS} draws, crc32 seeds, q={Q_HEAD}.  PRICE VINTAGE PINNED at {PIN}.")
    P("#")
    P("# DEFINITIONS, DECLARED BEFORE ANY NUMBER:")
    P("#   PICK(t) — argmax over the 33 gross rungs of C_IS4B computed on the trailing window")
    P("#     ending at bar t (exclusive).  Applied from the NEXT weekly rebalance forward.")
    P("#   INTERIOR — pick not in {0.200, 1.000}.  ENDPOINT — either of those two rungs.")
    P("#   MOVE — consecutive picks differ.  MOVE RATE = moves / (choices - 1).")
    P("#   SWITCH COST — the rolling cell's turnover per year MINUS the same cell's turnover")
    P("#     with its gross frozen at the cell's own MEDIAN pick, i.e. the turnover the moving")
    P("#     itself adds, in units of NAV per year; times 10 bps it is the drag in bps/yr.")
    P("#")
    P("# HYPOTHESES, DECLARED BEFORE ANY NUMBER:")
    P("#   H_INTERIOR  the rolling tent still reaches the INTERIOR: >= 75% of all choices across")
    P("#               all 24 cells are interior rungs.  If it collapses to an endpoint once the")
    P("#               window moves, 1154's 0.625 was a property of THAT window.")
    P("#   H_STABLE    the pick is UNSTABLE: median move rate >= 0.50 across the 24 cells.  A")
    P("#               tent's peak sits where two noisy legs cross, which is the least resolvable")
    P("#               place on the ladder (1154 measured the ladder's own Sharpe spread at")
    P("#               0.0021 on U56), so the argmax should wander.")
    P("#   H_CHEAP     the SWITCH COST is small: median added turnover < 0.50x NAV/yr, i.e. under")
    P("#               5 bps/yr of drag.  Gross switching trades only the cash leg.")
    P("#   H_OOSPASS   the 4b OOS pass does NOT survive re-choosing at a majority of cells: fewer")
    P("#               than 12 of 24 cells clear 4b OOS on the common span.")
    P("#   H_NOGAIN    rolling does not beat the frozen incumbent: median (rolling Sharpe -")
    P("#               K_FROZEN Sharpe) <= 0 on the common span.")
    P("# DECISION RULE, declared before any number: the queue's question is ANSWERED 'YES, THE")
    P("#   TENT REACHES THE INTERIOR ON A ROLLING WINDOW TOO' iff H_INTERIOR holds.  It is")
    P("#   ANSWERED 'ONLY ON THE ONE-SHOT SPLIT' if H_INTERIOR fails.  Whether that is WORTH")
    P("#   ANYTHING is a separate question answered by H_NOGAIN and H_OOSPASS, and a KEEP is")
    P("#   asked only on PROTOCOL's own two paths, never on the move rate.")
    P("")

    gaterows, gates = [], {}

    def gate(name, what, value, ok):
        gates[name] = bool(ok)
        gaterows.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
        P(f"  {name:<4s} {what:<64s} {value:.2e}   {'PASS' if ok else 'FAIL'}")

    # ------------------------------------------------------------------ PANELS
    P("## PANELS — loaded, PINNED and stamped before any result number")
    panels, raw_unpinned = {}, {}
    for panel in PANELS:
        pxu = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
        raw_unpinned[panel] = pxu
        px = pxu.loc[:PIN]
        idx = px.index
        warm, ins, oos = windows_of(idx)
        sc, above, vol20 = mech(px)
        common = np.zeros(len(idx), dtype=bool)
        common[COMMON_START:] = True
        panels[panel] = dict(px=px, idx=idx, K=len(px.columns), T=len(idx),
                             rets=px.pct_change().fillna(0.0).values, priced=px.notna().values,
                             warm=warm, ins=ins, oos=oos, common=common,
                             sc=sc, above=above, vol20=vol20,
                             spy=px["SPY"].pct_change().fillna(0.0).values)
        P(f"  {panel:<5s} {len(px.columns):4d} names, PINNED {len(idx):,} rows "
          f"{idx[0].date()} -> {idx[-1].date()} (unpinned ends {pxu.index[-1].date()}); "
          f"warm {warm.sum():,}; COMMON SPAN {common.sum():,} bars "
          f"{idx[COMMON_START].date()} -> {idx[-1].date()}; of which post-{IS_END} "
          f"{(oos & common).sum():,}")
    P("")

    def run_cell(panel, gross=GROSS0, N=N0, H=HOLD0, freq=FREQ0, maxvol=MAXVOL0, d=None):
        d = d or panels[panel]
        mk = cadence_mask(d["idx"], freq)
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        reb = np.flatnonzero(mk)
        el = d["above"] & (d["vol20"] < maxvol)
        W = build(-d["sc"], el, d["priced"], reb, N, H, d["T"], d["K"], gross)
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        return nrun(d["rets"], Wl, mkl), reb

    # ------------------------------------------------------------------ GATES
    P("## GATES — printed before any result number")
    d = panels["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    W = build(-d["sc"], d["above"] & (d["vol20"] < MAXVOL0), d["priced"], np.flatnonzero(mk),
              N0, HOLD0, d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST0, freq=FREQ0)["returns"].values
    (gr, tn), _ = run_cell("U56")
    rfast = gr - tn * COST0 / 1e4
    v = float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max())
    gate("G1", "fast runner == engine.backtest", v, v < 1e-12)

    def full_m(r, dp):
        rr = r[dp["warm"]]
        c, s, dd = fmet(rr)
        return c, s, dd

    c, s, dd = full_m(rfast, d)
    g2 = max(abs(c - A936_WH126[0]), abs(s - A936_WH126[1]), abs(dd - A936_WH126[2]))
    gate("G2", f"committed U56 W/H126/N=20 full-tape triple, PINNED at {PIN}", g2, g2 < 5e-5)
    P(f"       ({c:.4%} / {s:.4f} / {dd:.4%})")

    pxu = raw_unpinned["U56"]
    scu, abu, vlu = mech(pxu)
    wu, iu, ou = windows_of(pxu.index)
    du = dict(idx=pxu.index, K=len(pxu.columns), T=len(pxu.index),
              rets=pxu.pct_change().fillna(0.0).values, priced=pxu.notna().values,
              sc=scu, above=abu, vol20=vlu, warm=wu, ins=iu, oos=ou)
    (gru, tnu), _ = run_cell("U56", d=du)
    cu, su, ddu = full_m(gru - tnu * COST0 / 1e4, du)
    g2u = max(abs(cu - A936_WH126[0]), abs(su - A936_WH126[1]), abs(ddu - A936_WH126[2]))
    P(f"       THE VINTAGE, PUBLISHED NOT ABSORBED: the same gate UNPINNED reads {g2u:.2e} "
      f"({g2u / max(g2, 1e-18):.1f}x the pinned reading) from ONE extra bar of {len(pxu):,}.")
    gaterows.append(dict(gate="G2u", what="same gate on the UNPINNED file (reported, not gated)",
                         value=float(g2u), pass_=bool(g2u < 5e-5)))

    spy_full, live_full, live_m, spy_m = {}, {}, {}, {}
    for panel in PANELS:
        dp = panels[panel]
        sr = dp["spy"]
        spy_full[panel] = sr
        srw = sr[dp["warm"]]
        oc, os_, od = fmet(sr[dp["oos"]])
        spy_m[panel] = dict(full=fmet(srw), oos=(oc, os_, od),
                            common=span_m(sr, dp["common"], dp["oos"]))
        lr = backtest(dp["px"], rules_v2_weights(dp["px"]), cost_bps=COST0, freq="W")["returns"].values
        live_full[panel] = lr
        live_m[panel] = span_m(lr, dp["common"], dp["oos"])
        live_m[panel]["_fullMaxDD"] = fmet(lr[dp["warm"]])[2]
    g3 = max(abs(spy_m["U56"]["oos"][0] - SPY_OOS_COMMITTED[0]),
             abs(spy_m["U56"]["oos"][1] - SPY_OOS_COMMITTED[1]),
             abs(spy_m["U56"]["oos"][2] - SPY_OOS_COMMITTED[2]))
    gate("G3", f"SPY OOS triple, PINNED at {PIN}", g3, g3 < 5e-4)

    (g12, t12), _ = run_cell("U56", N=12)
    c12, s12, d12 = full_m(g12 - t12 * COST0 / 1e4, d)
    g4 = max(abs(c12 - A1098_U56_N12[0]), abs(s12 - A1098_U56_N12[1]), abs(d12 - A1098_U56_N12[2]))
    gate("G4", "CROSS-RUN 1098/1102's committed U56 n=12 triple", g4, g4 < 5e-4)

    g5 = abs(live_m["U56"]["_fullMaxDD"] - LIVE_MAXDD_COMMITTED)
    gate("G5", "live RULES v2 full-tape MaxDD == committed -12.05%", g5, g5 < 5e-4)

    (g12b, _t), _ = run_cell("U56", N=12)
    vv = float(np.abs(g12 - g12b).max())
    gate("G6", "determinism (same cell twice)", vv, vv == 0.0)

    g7 = max(int(np.abs(cadence_mask(d["idx"], f).astype(int) - rebalance_mask(d["idx"], f).values.astype(int)).sum())
             for f in ("D", "W", "M", "Q"))
    gate("G7", "cadence_mask == engine.rebalance_mask (D/W/M/Q)", float(g7), g7 == 0)

    # ------------------------------------------------------- THE GROSS LADDER (all 33 rungs)
    P("")
    P("## THE GROSS LADDER — all 33 rungs on both panels, published whatever a chooser did")
    rung_r, rung_t, reb_of, grows = {}, {}, {}, []
    for panel in PANELS:
        dp = panels[panel]
        for j, g in enumerate(GROSS_LADDER):
            (gg, tt), reb = run_cell(panel, gross=g)
            reb_of[panel] = reb
            r = gg - tt * COST0 / 1e4
            rung_r[(panel, j)] = r
            rung_t[(panel, j)] = tt
            mm = span_m(r, dp["common"], dp["oos"])
            l4b, l4bo, l4a = legs_4b(mm, spy_m[panel]["common"]), \
                legs_4b_oos(mm, spy_m[panel]["common"]), legs_4a(mm, live_m[panel])
            grows.append(dict(panel=panel, rung_i=j, gross=g,
                              turn_per_yr=float(tt[dp["common"]].sum() / (dp["common"].sum() / 252.0)),
                              **{k: float(v) for k, v in mm.items()},
                              **{k: bool(v) for k, v in l4b.items()},
                              **{k: bool(v) for k, v in l4bo.items()},
                              **{k: bool(v) for k, v in l4a.items()},
                              pass_4b=bool(all(l4b.values())),
                              pass_4b_oos=bool(all(l4bo.values())),
                              pass_4a=bool(all(l4a.values()))))
        P(f"  {panel}: {len(GROSS_LADDER)} rungs run  ({time.time() - t0:.0f}s)")
    grid = pd.DataFrame(grows)
    dump(grid, "grid")

    # G8 — 1154's ONE-SHOT C_IS4B pick must reproduce, on 1154's OWN window and span
    P("")
    bad8, shot = 0, {}
    for panel in PANELS:
        dp = panels[panel]
        w = dp["ins"]                                    # 1154's IS window, verbatim
        sc_ = [tent_score(rung_r[(panel, j)][w], dp["spy"][w])[0] for j in range(len(GROSS_LADDER))]
        pick = GROSS_LADDER[int(np.nanargmax(sc_))]
        shot[panel] = pick
        if abs(pick - A1154_IS4B[panel]) > 1e-9:
            bad8 += 1
            P(f"       G8 mismatch: {panel} one-shot C_IS4B picks {pick} not 1154's {A1154_IS4B[panel]}")
    gate("G8", "CROSS-RUN 1154's one-shot C_IS4B picks (0.625 U56 / 0.575 B136)", float(bad8), bad8 == 0)

    # G9 — the time-varying-gross build with a CONSTANT vector == the scalar path
    dp = panels["U56"]
    reb = reb_of["U56"]
    el = dp["above"] & (dp["vol20"] < MAXVOL0)
    Wa = build(-dp["sc"], el, dp["priced"], reb, N0, HOLD0, dp["T"], dp["K"], GROSS0)
    Wb = build(-dp["sc"], el, dp["priced"], reb, N0, HOLD0, dp["T"], dp["K"],
               np.full(len(reb), GROSS0))
    v9 = float(np.abs(Wa - Wb).max())
    gate("G9", "time-varying build with a CONSTANT vector == the scalar path", v9, v9 == 0.0)

    # G10 — the ladder nests the record's committed rungs
    need = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.575, 0.625]
    miss = sum(1 for x in need if not any(abs(x - g) < 1e-9 for g in GROSS_LADDER))
    gate("G10", "gross ladder nests the record's committed rungs", float(miss), miss == 0)

    gdf = pd.DataFrame(gaterows)
    dump(gdf, "gates")
    P(f"  GATES {sum(gates.values())} of {len(gates)} PASS")

    # ------------------------------------------------------------- THE ROLLING TENT (24 cells)
    P("")
    P("## THE ROLLING TENT — 12 (window, cadence) cells per panel, all 24 published")
    cellrows, pickrows, moverows = [], [], []
    roll_r = {}
    for panel in PANELS:
        dp = panels[panel]
        reb = reb_of[panel]
        sb_c = spy_m[panel]["common"]
        lbm = live_m[panel]
        el = dp["above"] & (dp["vol20"] < MAXVOL0)
        for wname, wlen in WINDOWS.items():
            for cname, cad in CADENCES.items():
                # choice bars: COMMON_START, then every `cad` bars
                choice_bars = list(range(COMMON_START, dp["T"], cad))
                picks, pick_i, mins = [], [], []
                for cb in choice_bars:
                    a = WARMUP if wlen < 0 else cb - wlen
                    w = slice(a, cb)
                    rs = dp["spy"][w]
                    sc_ = np.array([tent_score(rung_r[(panel, j)][w], rs)[0]
                                    for j in range(len(GROSS_LADDER))])
                    jj = int(np.nanargmax(sc_))
                    pick_i.append(jj)
                    picks.append(GROSS_LADDER[jj])
                    mins.append(float(sc_[jj]))
                # gross in force at each rebalance date: the last pick STRICTLY before it
                garr = np.full(len(reb), GROSS0)
                for i, t in enumerate(reb):
                    prior = [k for k, cb in enumerate(choice_bars) if cb <= t]
                    if prior:
                        garr[i] = picks[prior[-1]]
                Wv = build(-dp["sc"], el, dp["priced"], reb, N0, HOLD0, dp["T"], dp["K"], garr)
                Wl = np.zeros_like(Wv)
                Wl[LAG:] = Wv[:-LAG]
                mkl = np.roll(cadence_mask(dp["idx"], FREQ0), LAG)
                mkl[:LAG] = False
                gg, tt = nrun(dp["rets"], Wl, mkl)
                r = gg - tt * COST0 / 1e4
                roll_r[(panel, wname, cname)] = r
                mm = span_m(r, dp["common"], dp["oos"])

                # the switch-cost control: the SAME cell with gross frozen at its median pick
                medg = float(np.median(picks))
                medj = int(np.argmin([abs(g - medg) for g in GROSS_LADDER]))
                t_med = rung_t[(panel, medj)]
                tpy = float(tt[dp["common"]].sum() / (dp["common"].sum() / 252.0))
                tpy_med = float(t_med[dp["common"]].sum() / (dp["common"].sum() / 252.0))

                nmv = int(sum(1 for i in range(1, len(picks)) if pick_i[i] != pick_i[i - 1]))
                mrate = nmv / max(len(picks) - 1, 1)
                interior = int(sum(1 for j in pick_i if 0 < j < len(GROSS_LADDER) - 1))
                l4b, l4bo, l4a = legs_4b(mm, sb_c), legs_4b_oos(mm, sb_c), legs_4a(mm, lbm)
                cellrows.append(dict(
                    panel=panel, window=wname, win_bars=wlen, cadence=cname, cad_bars=cad,
                    n_choices=len(picks), n_moves=nmv, move_rate=mrate,
                    n_interior=interior, interior_share=interior / len(picks),
                    pick_first=picks[0], pick_last=picks[-1], pick_med=medg,
                    pick_min=float(min(picks)), pick_max=float(max(picks)),
                    pick_sd=float(np.std(picks, ddof=1)) if len(picks) > 1 else 0.0,
                    mean_abs_step=float(np.mean(np.abs(np.diff(picks)))) if len(picks) > 1 else 0.0,
                    turn_per_yr=tpy, turn_per_yr_frozen_at_med=tpy_med,
                    switch_turn_per_yr=tpy - tpy_med,
                    switch_drag_bps_yr=(tpy - tpy_med) * COST0,
                    **{k: float(v) for k, v in mm.items()},
                    **{k: bool(v) for k, v in l4b.items()},
                    **{k: bool(v) for k, v in l4bo.items()},
                    **{k: bool(v) for k, v in l4a.items()},
                    pass_4b=bool(all(l4b.values())), pass_4b_oos=bool(all(l4bo.values())),
                    pass_4a=bool(all(l4a.values()))))
                for k, cb in enumerate(choice_bars):
                    pickrows.append(dict(panel=panel, window=wname, cadence=cname,
                                         choice_bar=int(cb), date=str(dp["idx"][cb].date()),
                                         rung_i=pick_i[k], gross=picks[k], tent_min=mins[k],
                                         interior=bool(0 < pick_i[k] < len(GROSS_LADDER) - 1),
                                         moved=bool(k > 0 and pick_i[k] != pick_i[k - 1])))
                moverows.append(dict(panel=panel, window=wname, cadence=cname,
                                     n_choices=len(picks), n_moves=nmv, move_rate=mrate,
                                     mean_abs_step=float(np.mean(np.abs(np.diff(picks))))
                                     if len(picks) > 1 else 0.0,
                                     switch_turn_per_yr=tpy - tpy_med,
                                     switch_drag_bps_yr=(tpy - tpy_med) * COST0))
        P(f"  {panel}: 12 cells run  ({time.time() - t0:.0f}s)")
    cells = pd.DataFrame(cellrows)
    dump(cells, "cells")
    dump(pd.DataFrame(pickrows), "picks")
    dump(pd.DataFrame(moverows), "moves")

    # ---------------------------------------------------------------------- CONTROLS
    P("")
    P("## CONTROLS on the SAME common span (never selected on)")
    ctrl = {}
    for panel in PANELS:
        dp = panels[panel]
        jf = GROSS_LADDER.index(0.75)
        js = int(np.argmin([abs(g - shot[panel]) for g in GROSS_LADDER]))
        sub = grid[grid.panel == panel]
        jo = int(sub.iloc[int(np.nanargmax(sub["Sharpe"].values))]["rung_i"])
        for nm, j in (("K_FROZEN", jf), ("K_ONESHOT", js), ("K_ORACLE", jo)):
            mm = span_m(rung_r[(panel, j)], dp["common"], dp["oos"])
            ctrl[(panel, nm)] = dict(gross=GROSS_LADDER[j], **mm)
            l4b = legs_4b(mm, spy_m[panel]["common"])
            l4bo = legs_4b_oos(mm, spy_m[panel]["common"])
            P(f"  {panel:<5s} {nm:<10s} gross {GROSS_LADDER[j]:.3f}  "
              f"CAGR {mm['CAGR']:7.2%}  Sharpe {mm['Sharpe']:.4f}  MaxDD {mm['MaxDD']:7.2%}  "
              f"halves {mm['H1']:.4f}/{mm['H2']:.4f}  OOS {mm['OOS_CAGR']:6.2%}/{mm['OOS_Sharpe']:.4f}"
              f"  4b {'PASS' if all(l4b.values()) else 'fail'}"
              f"  4bOOS {'PASS' if all(l4bo.values()) else 'fail'}")
        sm = spy_m[panel]["common"]
        lm = live_m[panel]
        P(f"  {panel:<5s} {'SPY':<10s} {'':<12s}CAGR {sm['CAGR']:7.2%}  Sharpe {sm['Sharpe']:.4f}  "
          f"MaxDD {sm['MaxDD']:7.2%}  halves {sm['H1']:.4f}/{sm['H2']:.4f}  "
          f"OOS {sm['OOS_CAGR']:6.2%}/{sm['OOS_Sharpe']:.4f}")
        P(f"  {panel:<5s} {'RULESv2':<10s} {'':<12s}CAGR {lm['CAGR']:7.2%}  Sharpe {lm['Sharpe']:.4f}  "
          f"MaxDD {lm['MaxDD']:7.2%}  halves {lm['H1']:.4f}/{lm['H2']:.4f}  "
          f"OOS {lm['OOS_CAGR']:6.2%}/{lm['OOS_Sharpe']:.4f}")

    # ---------------------------------------------------------------------- HYPOTHESES
    P("")
    P("## HYPOTHESES — scored against the bars declared above, before any narrative")
    hyp = []
    ish = float(cells["n_interior"].sum() / cells["n_choices"].sum())
    hyp.append(("H_INTERIOR", "interior share of all choices >= 0.75", ish, ish >= 0.75))
    mr = float(cells["move_rate"].median())
    hyp.append(("H_STABLE", "median move rate >= 0.50 (pick is UNSTABLE)", mr, mr >= 0.50))
    sc_ = float(cells["switch_turn_per_yr"].median())
    hyp.append(("H_CHEAP", "median added turnover < 0.50 NAV/yr", sc_, sc_ < 0.50))
    n4bo = int(cells["pass_4b_oos"].sum())
    hyp.append(("H_OOSPASS", "fewer than 12 of 24 cells clear 4b OOS", float(n4bo), n4bo < 12))
    dsh = float(np.median([cells.loc[i, "Sharpe"] - ctrl[(cells.loc[i, "panel"], "K_FROZEN")]["Sharpe"]
                           for i in cells.index]))
    hyp.append(("H_NOGAIN", "median (rolling - K_FROZEN) Sharpe <= 0", dsh, dsh <= 0))
    for n, w, v, ok in hyp:
        P(f"  {n:<11s} {w:<52s} {v: .4f}   {'SUPPORTED' if ok else 'REFUTED'}")
    dump(pd.DataFrame([dict(hypothesis=n, bar=w, value=float(v), supported=bool(o))
                       for n, w, v, o in hyp]), "hypotheses")

    # ---------------------------------------------------------------------- RULE 8
    P("")
    P("## RULE 8 WALK-FORWARD — the (window, cadence) PAIR chosen on the FIRST HALF of the")
    P("##   common span and evaluated on the SECOND HALF untouched.  Three honest choosers.")
    wf = []
    for panel in PANELS:
        dp = panels[panel]
        cm = np.flatnonzero(dp["common"])
        h = len(cm) // 2
        m1 = np.zeros(dp["T"], dtype=bool); m1[cm[:h]] = True
        m2 = np.zeros(dp["T"], dtype=bool); m2[cm[h:]] = True
        spy1, spy2 = dp["spy"][m1], dp["spy"][m2]
        s1c, s1s, s1d = fmet(spy1); s2c, s2s, s2d = fmet(spy2)
        sub = cells[cells.panel == panel]
        stats = {}
        for i in sub.index:
            key = (sub.loc[i, "window"], sub.loc[i, "cadence"])
            r = roll_r[(panel, key[0], key[1])]
            stats[key] = (fmet(r[m1]), fmet(r[m2]))
        for chname, f in (("C_H1SHARPE", lambda a: a[0][1]),
                          ("C_H1CAGR", lambda a: a[0][0]),
                          ("C_H1TENT", lambda a: min((a[0][1] - s1s) / abs(s1s),
                                                     (0.60 * abs(s1d) - abs(a[0][2])) / (0.60 * abs(s1d)),
                                                     (a[0][0] - 0.70 * s1c) / abs(0.70 * s1c)))):
            best = max(stats, key=lambda k: f(stats[k]))
            (c1, sh1, d1), (c2, sh2, d2) = stats[best]
            wf.append(dict(panel=panel, chooser=chname, pick_window=best[0], pick_cadence=best[1],
                           H1_CAGR=c1, H1_Sharpe=sh1, H1_MaxDD=d1,
                           OOS_CAGR=c2, OOS_Sharpe=sh2, OOS_MaxDD=d2,
                           SPY_OOS_CAGR=s2c, SPY_OOS_Sharpe=s2s, SPY_OOS_MaxDD=s2d,
                           beats_SPY=bool(sh2 > s2s),
                           pass_4b_oos=bool(sh2 > s2s and abs(d2) <= DD_CAP * abs(s2d)
                                            and c2 >= CAGR_FLOOR * s2c)))
            P(f"  {panel:<5s} {chname:<11s} picks ({best[0]}, {best[1]})  "
              f"2nd half {c2:7.2%} / {sh2:.4f} / {d2:7.2%}  vs SPY {s2c:7.2%} / {s2s:.4f} / {s2d:7.2%}  "
              f"{'4bOOS PASS' if wf[-1]['pass_4b_oos'] else '4bOOS fail'}")
        # frozen-incumbent comparand on the same split
        jf = GROSS_LADDER.index(0.75)
        (fc1, fs1, fd1), (fc2, fs2, fd2) = fmet(rung_r[(panel, jf)][m1]), fmet(rung_r[(panel, jf)][m2])
        wf.append(dict(panel=panel, chooser="K_FROZEN(0.75)", pick_window="-", pick_cadence="-",
                       H1_CAGR=fc1, H1_Sharpe=fs1, H1_MaxDD=fd1,
                       OOS_CAGR=fc2, OOS_Sharpe=fs2, OOS_MaxDD=fd2,
                       SPY_OOS_CAGR=s2c, SPY_OOS_Sharpe=s2s, SPY_OOS_MaxDD=s2d,
                       beats_SPY=bool(fs2 > s2s),
                       pass_4b_oos=bool(fs2 > s2s and abs(fd2) <= DD_CAP * abs(s2d)
                                        and fc2 >= CAGR_FLOOR * s2c)))
        P(f"  {panel:<5s} {'K_FROZEN':<11s} gross 0.750           "
          f"2nd half {fc2:7.2%} / {fs2:.4f} / {fd2:7.2%}  vs SPY {s2c:7.2%} / {s2s:.4f} / {s2d:7.2%}  "
          f"{'4bOOS PASS' if wf[-1]['pass_4b_oos'] else '4bOOS fail'}")
    dump(pd.DataFrame(wf), "walkforward")

    # ---------------------------------------------------------------------- HEADLINES
    P("")
    P("## BOTH KEEP PATHS on the common span")
    P(f"  ladder base rate: 4b full {int(grid['pass_4b'].sum())} of {len(grid)}, "
      f"4b OOS {int(grid['pass_4b_oos'].sum())} of {len(grid)}, "
      f"4a {int(grid['pass_4a'].sum())} of {len(grid)}")
    P(f"  rolling cells:    4b full {int(cells['pass_4b'].sum())} of {len(cells)}, "
      f"4b OOS {int(cells['pass_4b_oos'].sum())} of {len(cells)}, "
      f"4a {int(cells['pass_4a'].sum())} of {len(cells)}")
    P("")
    P("## THE CELLS")
    show = cells[["panel", "window", "cadence", "n_choices", "n_moves", "move_rate",
                  "interior_share", "pick_med", "pick_min", "pick_max", "switch_turn_per_yr",
                  "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
                  "pass_4b", "pass_4b_oos", "pass_4a"]]
    P(show.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("")
    P(f"## DONE in {time.time() - t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
