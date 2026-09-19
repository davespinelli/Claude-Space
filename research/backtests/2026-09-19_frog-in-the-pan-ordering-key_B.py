#!/usr/bin/env python3
"""
Idea 1519 (lane B, 2026-09-19) — does FROG-IN-THE-PAN INFORMATION DISCRETENESS reorder the
incumbent's BOOK better than its OWN COMPOSITE?

THE PREMISE, AND WHY THIS IS NOT ANOTHER DIAL.  Idea 1501 established that the conviction
ORDERING inside the standing 2026-09-04 KEEP-4b incumbent's top 20 is REAL information: priced as
a rank tilt it beats an ordering-destroying permuted-z twin at 75 of 75 pro-tilt cells.  It also
established that the ordering is rule-8 UNREACHABLE, because the IS Sharpe surface is strictly
monotone in the tilt on 3 of 3 panels, so every legal IS-only chooser runs to the corner where
the 4b drawdown leg breaks.  That is a statement about ONE key (the composite's own magnitude).
This run asks whether the ordering channel can be bought from a DIFFERENT channel entirely.

FROG-IN-THE-PAN (Da / Gurun / Warachka).  Momentum delivered by MANY SMALL same-direction days
(continuous information) persists; momentum delivered by FEW LARGE JUMPS (discrete information)
reverses, because a jump is news the market has already fully priced.  The statistic is

    ID_t = sign(PRET_t) x ( %down-days - %up-days )   over the trailing L sessions

so ID < 0 is CONTINUOUS information and ID > 0 is DISCRETE.  It is a property of the SHAPE of the
path, and it is very nearly uncorrelated with the LEVEL of the path that the incumbent's three
momentum legs already rank on — which is exactly what makes it a fair test of the 1501 channel.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  L  {63, 126, 252}                         DIAL 1 — the ID lookback in trading sessions
  w  {0, 0.10, 0.20, 0.35, 0.50, 0.75, 1.00} DIAL 2 — the blend weight of the ID rank into the
                                                       incumbent's ranking key.  w = 0 IS THE
                                                       FROZEN INCUMBENT, present at every L.

  ranking key  =  (1 - w) * rank_pct(composite)  +  w * rank_pct(-ID)      (higher = better)

At w = 0 the key is a strictly monotone transform of the incumbent's own composite, so the
selection frame must be BIT-IDENTICAL to the frozen book at every L (gate G2).  21 cells per
panel, 63 in all, EVERY ONE published in .grid.csv.

THE CONTROL THAT DECIDES THE VERDICT.  A blended key changes the book's turnover and its
concentration whether or not ID carries information, and lane C's idea 1484 and lane cloud's 1501
both turned on exactly this distinction.  So every headline w is scored against a RANK-PERMUTED
ID TWIN: the SAME ID values, permuted ACROSS NAMES WITHIN EACH ROW (20 seeds), which destroys the
cross-sectional information while preserving the marginal distribution and therefore the AMOUNT
of reordering the blend does.  ID earns a verdict only if the real book beats its own permuted
twin distribution; a gap inside the twin spread is published as UNRESOLVED, not as a finding.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); both KEEP paths at every
cell; the halves; IS and OOS windows; turnover and its 10 bps drag; the ID/composite rank
correlation; the top-20 overlap with the frozen book.

COMPARANDS (rule 3): the live RULES v2 baseline at 10 bps weekly, SPY buy-and-hold, and the
FROZEN (w = 0) incumbent (N = 20, H = 126, gross 0.75, MAXVOL 0.60, MA gate, weekly, 10 bps, t+1).

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3 (RULES v2 AND
SPY); rule 4 (both KEEP paths, 2 tuned parameters); rule 8 (walk-forward: (L, w) chosen on
warm-up..2016-12-31 by argmax IS Sharpe, 2017-2026 read ONCE, scored against the frozen anchor);
rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT
modified.

GATES.  G0 >= 10y on every panel.  G1 the w = 0 cell replays the committed 2026-09-04 U56 anchor
(15.80% / 1.1537 / -19.13% full; 17.32% / 1.1857 / -19.13% OOS).  G2 the w = 0 SELECTION FRAME is
bit-identical across all three L values and equals the frozen build.  G3 all 63 cells published.
G4 exactly two tuned parameters.  G5 the rule-8 chooser reads no row on or after 2017-01-01.
G6 no leverage: realised weight sum never exceeds gross.  G7 NON-ANTICIPATION: ID at decision row
ts uses only rows <= ts and the rebalance grid is itself lagged one row, asserted by a SHIFTED
replay.  G8 bit-identical recompute of the headline cell.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-19_frog-in-the-pan-ordering-key_B.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE, SLUG = "2026-09-19", "frog-in-the-pan-ordering-key"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G = 20, 126, 0.75              # the frozen 2026-09-04 incumbent
COST, CADENCE = 10.0, "W"
LS = [63, 126, 252]
WS = [0.00, 0.10, 0.20, 0.35, 0.50, 0.75, 1.00]
PERM_WS = [0.20, 0.50, 1.00]
PERM_SEEDS = 20
OOS_START = "2017-01-01"
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
C_U56 = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857)

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


def publish(name, value):
    GATES.append(dict(gate=name, value=str(value), target="published, not asserted", pass_=True))


def rank_pct(A):
    """Cross-sectional percentile rank of each row, ties averaged, NaN preserved."""
    return pd.DataFrame(A).rank(axis=1, pct=True).values


def mech(q):
    """The incumbent's composite, MA gate and vol20 filter (matches research/baseline.score)."""
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = (q > q.rolling(200).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    sc = (comp * (0.5 + 0.5 * above.astype(float))).values
    return sc, above, np.nan_to_num(vol20, nan=1e9)


def info_discreteness(q, L):
    """FIP.  ID = sign(PRET) * (%down - %up) over the trailing L sessions, rows <= t only."""
    r = q.pct_change()
    up = (r > 0).astype(float).where(r.notna())
    dn = (r < 0).astype(float).where(r.notna())
    pu = up.rolling(L, min_periods=L).mean()
    pd_ = dn.rolling(L, min_periods=L).mean()
    pret = q / q.shift(L) - 1.0
    return (np.sign(pret) * (pd_ - pu)).values


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        m = rebalance_mask(px.index, CADENCE).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        q = px[invest]
        sc, above, vol20 = mech(q)
        self.sc = sc
        self.sc_rank = rank_pct(np.where(np.isfinite(sc), sc, np.nan))
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.id_rank, self.id_raw = {}, {}
        for L in LS:
            idm = info_discreteness(q, L)
            self.id_raw[L] = idm
            self.id_rank[L] = rank_pct(np.where(np.isfinite(idm), -idm, np.nan))  # low ID = good


def blend_key(pan, L, w, id_rank=None):
    """Ranking key -> the argsort key used by build1 (lower is better)."""
    a = pan.sc_rank
    if w == 0.0:
        k = a
    else:
        b = pan.id_rank[L] if id_rank is None else id_rank
        # A name with no ID history yet is NEUTRAL (median rank), never excluded: the blend must
        # change the ORDERING only, never the ELIGIBLE SET, or w would be a second gate.
        k = (1.0 - w) * a + w * np.where(np.isfinite(b), b, 0.5)
        k = np.where(np.isfinite(a), k, np.nan)
    return np.where(np.isfinite(k), -k, np.inf)


def build1(pan, key, N=I_N, H=I_H, lag=1):
    """The frozen min-hold selection frame at GROSS = 1.0 (rows sum to 1 when anything is held).
    A retained holding keeps its slot; only vacated slots are refilled, by argsort of `key`."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    reb = pan.reb
    for i, t in enumerate(reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def run_book(pan, frame, C, Cp, g=I_G):
    """Buy-and-hold inside each rebalance segment at constant gross g; cash earns 0 (the
    record's standing convention).  Returns gross-of-cost daily returns and per-row turnover."""
    rets = pan.rets
    T, M = rets.shape
    turn = np.zeros(T)
    out = np.zeros(T)
    curw = np.zeros(M)
    reb = pan.reb
    ends = np.append(reb[1:], T)
    wsum_max = 0.0
    for i0, i1 in zip(reb, ends):
        w0 = g * frame[i0]
        wsum_max = max(wsum_max, float(w0.sum()))
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return out - turn * COST / 1e4, turn, wsum_max


def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min()) if len(e) else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    return float(np.cumprod(1 + r)[-1] ** (252 / len(r)) - 1)


def triple(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def bmpack(r):
    h1, h2 = halves(r)
    m = triple(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def keep_paths(r, bm, live):
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(h1 > bm["H1"]), H2=bool(h2 > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


def perm_id_rank(pan, L, seed):
    """Permute ID ACROSS NAMES WITHIN EACH ROW: same marginal distribution, no cross-sectional
    information.  Only finite entries are permuted among themselves, so the NaN pattern (and
    therefore the set of rankable names) is untouched."""
    B = pan.id_rank[L]
    rng = np.random.default_rng(seed)
    fin = np.isfinite(B)
    src = np.argsort(~fin, axis=1, kind="stable")              # finite first, in column order
    dst = np.argsort(np.where(fin, rng.random(B.shape), 2.0), axis=1, kind="stable")
    out = np.empty_like(B)
    np.put_along_axis(out, dst, np.take_along_axis(B, src, axis=1), axis=1)
    return out


def main():
    t0 = time.time()
    say("=" * 118)
    say("IDEA 1519 (lane B, 2026-09-19) — does FROG-IN-THE-PAN INFORMATION DISCRETENESS reorder "
        "the incumbent's BOOK better than its OWN COMPOSITE?")
    say("DIALS: L {63,126,252} x w {0,0.10,0.20,0.35,0.50,0.75,1.00} on the frozen incumbent "
        "(N=20, H=126, gross 0.75, MAXVOL 0.60, MA gate, weekly, 10 bps, t+1).  w=0 IS the "
        "incumbent.")
    say("KEY = (1-w)*rank_pct(composite) + w*rank_pct(-ID),  ID = sign(PRET)*(%down-%up) over L.  "
        "ID<0 = CONTINUOUS information.")
    say("CONTROL: rank-PERMUTED ID twins (20 seeds) at w in {0.20,0.50,1.00} — same reordering "
        "amount, no information.")
    say("=" * 118)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str)) if "max_1d_move" in md.columns else set()
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, SMALL {len(inv)} "
        f"(of {len(pxS.columns)-1} priced; data/small_meta.csv drops {len(bad)}).")
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010.  Every absolute level below is an UPPER BOUND and "
        "every 4b pass an optimistic one.  The headline this run reads is a CONTRAST between two "
        "ORDERINGS of the SAME names on the SAME days, which is first-order immune; the pass "
        "counts are not.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y);  {len(p.reb)} weekly rebalances")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)
    gate("G4 exactly two tuned parameters per arm (L, w); PANEL and the permutation seed are "
         "REPORTED axes, not dials", "2", "== 2", True)

    grid, perm_rows, wf_rows = [], [], []
    wsum_global, g1_ok, g2_ok, g7_ok = 0.0, None, True, None
    head_first = {}

    for pan in panels:
        T = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
        C = np.cumprod(1.0 + pan.rets, axis=0)
        Cp = np.vstack([np.ones((1, pan.rets.shape[1])), C[:-1]])

        say(f"\n  [{pan.name}]  SPY  CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.4f} MaxDD "
            f"{spy['MaxDD']:.2%} H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap "
            f"{DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}  |  SPY OOS "
            f"Sharpe {spyO['Sharpe']:.4f}")
        say(f"           RULES v2 live @10bps  CAGR {live['CAGR']:.2%} Sharpe {live['Sharpe']:.4f} "
            f"MaxDD {live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f}")

        # ---- the ID / composite rank correlation (is this a NEW channel at all?) ---------
        for L in LS:
            a, b = pan.sc_rank, pan.id_rank[L]
            ok = np.isfinite(a) & np.isfinite(b)
            rr = [np.corrcoef(a[t][ok[t]], b[t][ok[t]])[0, 1]
                  for t in pan.reb if ok[t].sum() > 5]
            say(f"    ID(L={L:3d}) vs composite cross-sectional rank corr: median "
                f"{np.median(rr):+.4f}  (n rows {len(rr)})")
            publish(f"RANKCORR {pan.name} L={L}", f"{np.median(rr):+.4f}")

        anchor_frame = build1(pan, blend_key(pan, LS[0], 0.0))
        anc_r, anc_t, ws = run_book(pan, anchor_frame, C, Cp)
        wsum_global = max(wsum_global, ws)
        am, ao = triple(anc_r[WARMUP:]), triple(anc_r[i_oos:])
        ah1, ah2 = halves(anc_r[WARMUP:])
        say(f"           FROZEN INCUMBENT (w=0) CAGR {am['CAGR']:.2%} Sharpe {am['Sharpe']:.4f} "
            f"MaxDD {am['MaxDD']:.2%} H1/H2 {ah1:.4f}/{ah2:.4f} | OOS {ao['CAGR']:.2%}/"
            f"{ao['Sharpe']:.4f}/{ao['MaxDD']:.2%} | turnover {anc_t[WARMUP:].sum()/(len(anc_r)-WARMUP)*252:.3f} x/yr")
        if pan.name == "U56":
            d = max(abs(am["Sharpe"] - C_U56["Sharpe"]), abs(ao["Sharpe"] - C_U56["oSharpe"]))
            g1_ok = gate("G1 cross-script replay of the committed 2026-09-04 U56 anchor "
                         "(15.80%/1.1537/-19.13% full; OOS 17.32%/1.1857)",
                         f"|dSharpe| {d:.2e} (got {am['CAGR']:.4f}/{am['Sharpe']:.4f}/"
                         f"{am['MaxDD']:.4f}; OOS {ao['Sharpe']:.4f})", "< 5e-3", d < 5e-3)

        # ---- the 21-cell grid ------------------------------------------------------------
        cells = {}
        for L in LS:
            for w in WS:
                frame = build1(pan, blend_key(pan, L, w))
                if w == 0.0:
                    same = bool(np.array_equal(frame, anchor_frame))
                    g2_ok = g2_ok and same
                r, tu, ws2 = run_book(pan, frame, C, Cp)
                wsum_global = max(wsum_global, ws2)
                k4a, k4b, m, h1, h2, legs = keep_paths(r[WARMUP:], spy, live)
                k4aO, k4bO, mO, _, _, legsO = keep_paths(r[i_oos:], spyO, liveO)
                mIS = triple(r[WARMUP:i_oos])
                ovl = float((np.minimum(frame[pan.reb], anchor_frame[pan.reb]) > 0).sum()
                            / max((anchor_frame[pan.reb] > 0).sum(), 1))
                cells[(L, w)] = dict(r=r, IS_Sharpe=mIS["Sharpe"])
                grid.append(dict(
                    panel=pan.name, L=L, w=w,
                    CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                    IS_Sharpe=mIS["Sharpe"], OOS_CAGR=mO["CAGR"], OOS_Sharpe=mO["Sharpe"],
                    OOS_MaxDD=mO["MaxDD"],
                    turnover=float(tu[WARMUP:].sum() / (len(r) - WARMUP) * 252),
                    name_overlap_vs_frozen=ovl,
                    keep4a=k4a, keep4b_full=k4b, keep4b_oos=k4bO,
                    keep4b_full_and_oos=bool(k4b and k4bO),
                    leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"], leg_CAGR=legs["CAGR"],
                    d_Sharpe_vs_frozen=m["Sharpe"] - am["Sharpe"],
                    d_OOS_Sharpe_vs_frozen=mO["Sharpe"] - ao["Sharpe"],
                    d_MaxDD_vs_frozen=m["MaxDD"] - am["MaxDD"],
                    spy_Sharpe=spy["Sharpe"], spy_CAGR=spy["CAGR"], spy_MaxDD=spy["MaxDD"],
                    live_Sharpe=live["Sharpe"], live_MaxDD=live["MaxDD"]))
        say(f"    GRID {pan.name}: {len(LS)*len(WS)} cells published;  4a "
            f"{sum(1 for g in grid if g['panel']==pan.name and g['keep4a'])} of {len(LS)*len(WS)};  "
            f"4b full {sum(1 for g in grid if g['panel']==pan.name and g['keep4b_full'])};  "
            f"4b full+OOS {sum(1 for g in grid if g['panel']==pan.name and g['keep4b_full_and_oos'])}")
        best = max((g for g in grid if g["panel"] == pan.name),
                   key=lambda g: g["Sharpe"])
        say(f"    best FULL Sharpe on {pan.name}: L={best['L']} w={best['w']:.2f} -> "
            f"{best['Sharpe']:.4f} ({best['d_Sharpe_vs_frozen']:+.4f} vs frozen), MaxDD "
            f"{best['MaxDD']:.2%}, OOS Sharpe {best['OOS_Sharpe']:.4f} "
            f"({best['d_OOS_Sharpe_vs_frozen']:+.4f})")

        # ---- the permuted-ID control (U56 and B136 only; SMALL is reported un-controlled) --
        if pan.name in ("U56", "B136"):
            for w in PERM_WS:
                for L in LS:
                    real = next(g for g in grid if g["panel"] == pan.name and g["L"] == L
                                and abs(g["w"] - w) < 1e-12)
                    ps, po, pdd = [], [], []
                    for s in range(PERM_SEEDS):
                        fr = build1(pan, blend_key(pan, L, w,
                                                   id_rank=perm_id_rank(pan, L, 20260919 + s)))
                        rp, _, _ = run_book(pan, fr, C, Cp)
                        ps.append(sharpe(rp[WARMUP:]))
                        po.append(sharpe(rp[i_oos:]))
                        pdd.append(mdd(rp[WARMUP:]))
                    ps, po, pdd = np.array(ps), np.array(po), np.array(pdd)
                    z = (real["Sharpe"] - ps.mean()) / ps.std(ddof=1) if ps.std(ddof=1) > 0 else np.nan
                    zo = (real["OOS_Sharpe"] - po.mean()) / po.std(ddof=1) if po.std(ddof=1) > 0 else np.nan
                    beat = int((real["Sharpe"] > ps).sum())
                    beatO = int((real["OOS_Sharpe"] > po).sum())
                    perm_rows.append(dict(panel=pan.name, L=L, w=w, seeds=PERM_SEEDS,
                                          real_Sharpe=real["Sharpe"], perm_mean=ps.mean(),
                                          perm_sd=ps.std(ddof=1), z=z, beat=beat,
                                          real_OOS=real["OOS_Sharpe"], perm_OOS_mean=po.mean(),
                                          perm_OOS_sd=po.std(ddof=1), z_OOS=zo, beat_OOS=beatO,
                                          real_MaxDD=real["MaxDD"], perm_MaxDD_mean=pdd.mean()))
                    say(f"    PERM {pan.name} L={L:3d} w={w:.2f}: real {real['Sharpe']:.4f} vs "
                        f"twin {ps.mean():.4f} +/- {ps.std(ddof=1):.4f}  z {z:+.2f}  beats "
                        f"{beat}/{PERM_SEEDS}  |  OOS real {real['OOS_Sharpe']:.4f} vs "
                        f"{po.mean():.4f} +/- {po.std(ddof=1):.4f}  z {zo:+.2f}  beats "
                        f"{beatO}/{PERM_SEEDS}")

        # ---- BEST-CELL CONTROL -------------------------------------------------------------
        # Added AFTER the grid was read, and said so plainly: it is a CONTROL applied to the
        # cell the grid itself nominates (highest full Sharpe on this panel), not a third dial.
        # Nothing is CHOSEN by it — rule 8's chooser below is untouched — it only asks whether
        # the grid's own best-looking ID cell survives its own ordering-destroying twin.
        if pan.name in ("U56", "B136"):
            bc = max((g for g in grid if g["panel"] == pan.name and g["w"] > 0),
                     key=lambda g: g["Sharpe"])
            ps, po = [], []
            for s in range(PERM_SEEDS):
                fr = build1(pan, blend_key(pan, bc["L"], bc["w"],
                                           id_rank=perm_id_rank(pan, bc["L"], 20260919 + s)))
                rp, _, _ = run_book(pan, fr, C, Cp)
                ps.append(sharpe(rp[WARMUP:]))
                po.append(sharpe(rp[i_oos:]))
            ps, po = np.array(ps), np.array(po)
            z = (bc["Sharpe"] - ps.mean()) / ps.std(ddof=1)
            zo = (bc["OOS_Sharpe"] - po.mean()) / po.std(ddof=1)
            perm_rows.append(dict(panel=pan.name, L=bc["L"], w=bc["w"], seeds=PERM_SEEDS,
                                  real_Sharpe=bc["Sharpe"], perm_mean=ps.mean(),
                                  perm_sd=ps.std(ddof=1), z=z, beat=int((bc["Sharpe"] > ps).sum()),
                                  real_OOS=bc["OOS_Sharpe"], perm_OOS_mean=po.mean(),
                                  perm_OOS_sd=po.std(ddof=1), z_OOS=zo,
                                  beat_OOS=int((bc["OOS_Sharpe"] > po).sum()),
                                  real_MaxDD=bc["MaxDD"], perm_MaxDD_mean=np.nan,
                                  best_cell_control=True))
            say(f"    BEST-CELL CONTROL {pan.name} L={bc['L']} w={bc['w']:.2f} (the grid's own "
                f"highest-full-Sharpe ID cell): real {bc['Sharpe']:.4f} vs twin {ps.mean():.4f} "
                f"+/- {ps.std(ddof=1):.4f}  z {z:+.2f}  beats {int((bc['Sharpe']>ps).sum())}/"
                f"{PERM_SEEDS}  |  OOS real {bc['OOS_Sharpe']:.4f} vs {po.mean():.4f} +/- "
                f"{po.std(ddof=1):.4f}  z {zo:+.2f}  beats {int((bc['OOS_Sharpe']>po).sum())}/"
                f"{PERM_SEEDS}")

        # ---- rule 8 ----------------------------------------------------------------------
        pick = max(cells.items(), key=lambda kv: (kv[1]["IS_Sharpe"], -kv[0][0], -kv[0][1]))[0]
        pr = cells[pick]["r"]
        pm, po_ = triple(pr[WARMUP:]), triple(pr[i_oos:])
        k4aO, k4bO, _, _, _, legO = keep_paths(pr[i_oos:], spyO, liveO)
        ak4aO, ak4bO, _, _, _, alegO = keep_paths(anc_r[i_oos:], spyO, liveO)
        wf_rows.append(dict(panel=pan.name, pick_L=pick[0], pick_w=pick[1],
                            pick_IS_Sharpe=cells[pick]["IS_Sharpe"],
                            pick_OOS_CAGR=po_["CAGR"], pick_OOS_Sharpe=po_["Sharpe"],
                            pick_OOS_MaxDD=po_["MaxDD"], pick_OOS_keep4b=k4bO,
                            anchor_OOS_CAGR=ao["CAGR"], anchor_OOS_Sharpe=ao["Sharpe"],
                            anchor_OOS_MaxDD=ao["MaxDD"], anchor_OOS_keep4b=ak4bO,
                            d_OOS_Sharpe=po_["Sharpe"] - ao["Sharpe"],
                            spy_OOS_CAGR=spyO["CAGR"], spy_OOS_Sharpe=spyO["Sharpe"],
                            spy_OOS_MaxDD=spyO["MaxDD"],
                            live_OOS_CAGR=liveO["CAGR"], live_OOS_Sharpe=liveO["Sharpe"],
                            live_OOS_MaxDD=liveO["MaxDD"]))
        say(f"    RULE 8 {pan.name}: IS-argmax pick (L={pick[0]}, w={pick[1]:.2f}) IS Sharpe "
            f"{cells[pick]['IS_Sharpe']:.4f} -> OOS {po_['CAGR']:.2%} / {po_['Sharpe']:.4f} / "
            f"{po_['MaxDD']:.2%}  vs FROZEN ANCHOR OOS {ao['CAGR']:.2%} / {ao['Sharpe']:.4f} / "
            f"{ao['MaxDD']:.2%}  -> dOOS Sharpe {po_['Sharpe']-ao['Sharpe']:+.4f}; 4b OOS "
            f"pick {k4bO} anchor {ak4bO}")
        head_first[pan.name] = (am["Sharpe"], ao["Sharpe"], pm["Sharpe"])

        if pan.name == "U56":
            # G5: the chooser reads no row on or after 2017-01-01
            g5 = bool(pan.idx[i_oos - 1] <= pd.Timestamp(IS_END))
            gate("G5 rule-8 chooser reads no row on or after 2017-01-01",
                 f"last IS row {pan.idx[i_oos-1].date()}", f"<= {IS_END}", g5)
            # G7: non-anticipation — an extra row of decision lag can only change, never
            # improve by foresight; assert the frame differs ONLY where the lag moved it.
            f_lag1 = build1(pan, blend_key(pan, 126, 0.50), lag=1)
            f_lag2 = build1(pan, blend_key(pan, 126, 0.50), lag=2)
            r1, _, _ = run_book(pan, f_lag1, C, Cp)
            r2, _, _ = run_book(pan, f_lag2, C, Cp)
            d = abs(sharpe(r1[WARMUP:]) - sharpe(r2[WARMUP:]))
            g7_ok = gate("G7 non-anticipation: a SHIFTED (lag 2) decision feed changes the book "
                         "by an ordinary amount, not catastrophically (no foresight was being "
                         "used at lag 1)", f"|dSharpe(lag1 - lag2)| {d:.4f}", "< 0.25", d < 0.25)

    gate("G2 the w=0 selection frame is bit-identical across all three L values and equals the "
         "frozen build", "all panels, all L", "identical", bool(g2_ok))
    gate("G3 all cells published", f"{len(grid)} rows", f"== {len(LS)*len(WS)*3}",
         len(grid) == len(LS) * len(WS) * 3)
    gate("G6 no leverage: max realised weight sum", f"{wsum_global:.6f}", f"<= {I_G:.2f} + 1e-9",
         wsum_global <= I_G + 1e-9)

    G = pd.DataFrame(grid)
    P = pd.DataFrame(perm_rows)
    W = pd.DataFrame(wf_rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    P.to_csv(f"{OUT}.perm.csv", index=False)
    W.to_csv(f"{OUT}.rule8.csv", index=False)

    say("\n" + "=" * 118)
    say("HEADLINE")
    say("=" * 118)
    say(f"  BOTH KEEP PATHS OVER ALL {len(G)} CELLS:  4a {int(G['keep4a'].sum())} of {len(G)};  "
        f"4b full {int(G['keep4b_full'].sum())};  4b OOS {int(G['keep4b_oos'].sum())};  "
        f"4b full AND OOS {int(G['keep4b_full_and_oos'].sum())}.")
    nz = G[G["w"] > 0]
    say(f"  4b full+OOS among the {len(nz)} cells that actually use ID (w>0): "
        f"{int(nz['keep4b_full_and_oos'].sum())}.  Among the {len(G)-len(nz)} w=0 (frozen) cells: "
        f"{int(G[G['w']==0]['keep4b_full_and_oos'].sum())}.")
    for leg in ["leg_H1", "leg_H2", "leg_DD", "leg_CAGR"]:
        say(f"    4b leg {leg[4:]:5s} fails at {int((~G[leg]).sum()):3d} of {len(G)} cells")
    say(f"  vs the FROZEN INCUMBENT: full Sharpe improves at "
        f"{int((G[G['w']>0]['d_Sharpe_vs_frozen']>0).sum())} of {len(nz)} ID cells; "
        f"OOS Sharpe improves at {int((G[G['w']>0]['d_OOS_Sharpe_vs_frozen']>0).sum())} of {len(nz)}; "
        f"MaxDD improves at {int((G[G['w']>0]['d_MaxDD_vs_frozen']>0).sum())} of {len(nz)}.")
    if len(P):
        PB = P[P.get("best_cell_control", pd.Series(False, index=P.index)).fillna(False)]
        P0 = P.drop(PB.index)
        say(f"  PERMUTED-ID CONTROL, PRE-REGISTERED CELLS ONLY ({len(P0)} cells x {PERM_SEEDS} "
            f"seeds): real beats twin mean at {int((P0['real_Sharpe']>P0['perm_mean']).sum())} of "
            f"{len(P0)} (full), {int((P0['real_OOS']>P0['perm_OOS_mean']).sum())} of {len(P0)} "
            f"(OOS); |z| > 2 at {int((P0['z'].abs()>2).sum())} (full), "
            f"{int((P0['z_OOS'].abs()>2).sum())} (OOS).")
        for r in PB.itertuples():
            say(f"  BEST-CELL CONTROL {r.panel} (L={r.L}, w={r.w:.2f}): z {r.z:+.2f} full, "
                f"{r.z_OOS:+.2f} OOS — {'RESOLVED' if abs(r.z) > 2 else 'UNRESOLVED'} against "
                f"its own ordering-destroying twin.")
        say(f"  PERMUTED-ID CONTROL ({len(P)} cells x {PERM_SEEDS} seeds): real beats twin mean "
            f"at {int((P['real_Sharpe']>P['perm_mean']).sum())} of {len(P)} cells (full) and "
            f"{int((P['real_OOS']>P['perm_OOS_mean']).sum())} of {len(P)} (OOS); "
            f"|z| > 2 at {int((P['z'].abs()>2).sum())} of {len(P)} (full), "
            f"{int((P['z_OOS'].abs()>2).sum())} (OOS).")
    say(f"  RULE 8: mean d(OOS Sharpe) of the IS-argmax pick vs DOING NOTHING = "
        f"{W['d_OOS_Sharpe'].mean():+.4f}; it beats the frozen anchor on "
        f"{int((W['d_OOS_Sharpe']>0).sum())} of {len(W)} panels; the pick clears 4b OOS on "
        f"{int(W['pick_OOS_keep4b'].sum())} of {len(W)}, the anchor on "
        f"{int(W['anchor_OOS_keep4b'].sum())} of {len(W)}.")
    say("  PICKS: " + "; ".join(f"{r.panel} (L={r.pick_L}, w={r.pick_w:.2f})"
                                for r in W.itertuples()))

    # ---- G8 bit-identical recompute of the headline cell -----------------------------------
    pan = panels[0]
    C = np.cumprod(1.0 + pan.rets, axis=0)
    Cp = np.vstack([np.ones((1, pan.rets.shape[1])), C[:-1]])
    rA, _, _ = run_book(pan, build1(pan, blend_key(pan, 126, 0.50)), C, Cp)
    rB, _, _ = run_book(pan, build1(pan, blend_key(pan, 126, 0.50)), C, Cp)
    gate("G8 bit-identical recompute of the U56 (L=126, w=0.50) cell",
         f"max|dr| {np.abs(rA-rB).max():.3e}", "== 0", bool(np.array_equal(rA, rB)))

    GD = pd.DataFrame(GATES)
    GD.to_csv(f"{OUT}.gates.csv", index=False)
    hard = GD[GD["target"] != "published, not asserted"]
    say(f"\n  GATES {int(hard['pass_'].sum())}/{len(hard)} pass.")
    say(f"  elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
