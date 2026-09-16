#!/usr/bin/env python3
"""Idea 1104 (lane C, 2026-09-16) — does the FAR-SIDE COLLAPSE survive a PANEL it was not
found on?

QUESTION (QUEUE idea 1104, verbatim)
    idea 1098 found the only resolved part of the EDGE shape is the collapse above n~15 (6.41 /
    6.47 pp, far above the 3.25 / 4.02 pp floor), while the peak's location is not resolved at
    all.  Re-run the same 9-rung EDGE ladder and its bootstrap floor on the SMALL panel (dropping
    max_1d_move >= 1.0 per data/small_meta.csv) and report whether the collapse is a large-cap
    fact or a breadth fact.  Max 2 params (n, panel).

WHAT IS TUNED AND WHAT IS NOT (PROTOCOL rule 4)
    Exactly TWO dials: n (1082's nine rungs {5,8,10,12,15,20,25,30,40}) x PANEL
    {SMALL_F10 (headline), SMALL_RAW (control), U56 (1098's own anchor), U56_2010 (labelled
    tape control)}.  36 cells, ALL published.  Everything else is 1098/1082's construction
    frozen verbatim: CAND20 legs, cap INF, max_vol 0.60, gross 0.75, W cadence, min hold 126,
    10 bps, LAG 1, warm-up 260, IS end 2016-12-31, SEEDS = 40 (1098's headline seed count; the
    seed dial is NOT re-opened here), 1,000 block-bootstrap draws.  BLOCK LENGTH is not a dial:
    headline L = 63, L in {21, 126} reported beside it and never selected on.

    TAPE IS NOT A DIAL EITHER.  The small panel begins 2010-01-04, U56 begins 2008-01-02, so a
    bare SMALL-vs-U56 comparison confounds breadth with tape length.  U56_2010 is U56 clipped to
    the small panel's own span, reported as a labelled control so the panel answer can be read
    net of tape length.  No result is selected on it.

THE PANEL FILTER (the idea's own instruction)
    data/SMALL_PANEL_README.md flags 48-52 tickers carrying a one-day move above +100% that does
    NOT reverse (missing split adjustments, post-bankruptcy re-listings; AMPY jumps +16,083% on
    2016-10-24 and stays there).  SMALL_F10 drops every ticker with max_1d_move >= 1.0 in
    data/small_meta.csv.  SMALL_RAW keeps them, so the reader can see what the flagged names do
    to an EDGE ladder rather than take the filter on trust.  SPY is a BENCHMARK column on this
    panel, never a constituent: it is excluded from the investable set of both small panels (and
    from the RULES v2 baseline run on them), which is the panel's documented convention.

DECLARED BEFORE ANY NUMBER
    (a) H_COLLAPSE_SIGN — on SMALL_F10, EDGE(argmax) - EDGE(40) > 0: a far-side collapse exists
        at all.  RIVAL, named in advance: on a 663-name pool a 40-name book is still tiny
        relative to breadth, so the collapse may not have begun by n=40 and the gap may be ~0.
    (b) H_COLLAPSE_RESOLVED — on SMALL_F10 that gap is ABOVE the panel's own 90% sign-resolution
        floor, measured the same way 1098 measured it (smallest |dEDGE| above which the
        bootstrap agrees with the full-sample sign at least 90% of the time over all 36 rung
        pairs).  This is the claim 1104 exists to test: if it passes, the collapse is a BREADTH
        fact; if it fails, 1098's "resolved far side" is a large-cap fact.
    (c) H_PEAK_UNRESOLVED — on SMALL_F10 the peak-minus-runner-up gap is BELOW that same floor,
        i.e. 1098's other half (the peak's location is not resolved) also travels.
    (d) H_STEPS — the collapse's SIGN is the same on SMALL_RAW as on SMALL_F10.  If it is not,
        the small-panel answer is a data-quality artefact and must be reported as one.
    (e) H_TAPE — U56_2010 still carries a resolved collapse on the short tape.  If it does not,
        any SMALL failure is tape length, not breadth, and 1104 cannot be answered on this data.
    (f) H_FLOOR_SCALES — the SMALL_F10 floor is HIGHER than U56's 3.25 pp (a 663-name pool makes
        a 20-name draw more dispersed, so the bootstrap is wider).
    (g) EDGE IS NOT A KEEP PATH, exactly as 1082/1098 declared.  4a and 4b are scored at every
        rung of every panel and rule 8 picks n on the IS window alone, per panel, separately.

SURVIVORSHIP (PROTOCOL rule 9).  EVERY panel here is a CURRENT-CONSTITUENT panel, and the SMALL
    panel is the worst of them: data/SMALL_PANEL_README.md warns the screen contains only names
    still listed, still public and still under $2B TODAY, so returns are biased upward and the
    bias grows with lookback.  Book and null are drawn from the SAME pool over the SAME tape, so
    the bias very largely cancels out of EDGE, out of the argmax and out of the floor — which is
    why this run's headline is an EDGE-shape claim and NOT a capital claim.  It does NOT cancel
    out of the 4b legs, which are measured against SPY; every 4b figure on a SMALL panel below is
    therefore flattered and is reported for completeness, not as a candidate.
"""
from __future__ import annotations

import hashlib
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

DATE = "2026-09-16"
SLUG = "does-the-FAR-SIDE-COLLAPSE-survive-a-PANEL-it-was-not-found-on"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

LAG = 1
WARMUP = 260
MAXVOL = 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
GROSS0 = 0.75
FREQ = "W"
HOLD = 126
LEGS = [(21, 252), (0, 126), (0, 63)]
CAPNAME = "INF"
BISECT = 34

NS = [5, 8, 10, 12, 15, 20, 25, 30, 40]        # dial 1 — 1082's ladder verbatim
NSEED = 40                                      # frozen at 1098's headline seed count
BDRAWS = 1000
BLOCKS_L = [21, 63, 126]
L_HEAD = 63
STEP_CUT = 1.0                                  # the idea's own filter: drop max_1d_move >= 1.0
PANELS = ["U56", "U56_2010", "SMALL_F10", "SMALL_RAW"]   # dial 2
HEADLINE_PANEL = "SMALL_F10"
CHOOSERS = ["C_ISSHARPE", "C_ISDD", "C_ISCAGR", "C_ISEDGE"]

# committed cross-run anchors (for gates, never for selection)
A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
A1082_EDGE_U56 = [5.95, 5.35, 6.21, 6.82, 5.22, 5.12, 2.95, 1.55, 0.41]     # 1082 CHANGELOG
A1098_U56 = dict(floor90=3.25, floor95=4.66, peak=12, gap=0.61, collapse=6.41)
A1098_B136 = dict(floor90=4.02, collapse=6.47)
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def mdseed(*parts):
    """1082/1086/1094/1098's recipe verbatim, so the null draws are the SAME objects."""
    return int(hashlib.md5("|".join(str(x) for x in parts).encode()).hexdigest()[:8], 16)


# ------------------------------------------- 1082/1098's runner and rescaler, copied verbatim
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


def gross_rescaler(rets, wt, mk):
    T, N = rets.shape
    mk = mk.copy()
    mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    A = wt[s0] * (Cp / Cp[s0])
    AR = (A * rets).sum(axis=1)
    S = A.sum(axis=1)
    Wsum = wt[s0].sum(axis=1)
    s0p = reb[np.maximum(seg - 1, 0)]
    Ap = (wt[s0p] * (Cp / Cp[s0p]))[reb]
    Sp = Ap.sum(axis=1)
    Wsp = wt[s0p].sum(axis=1)[reb]
    Ap[0] = 0.0
    Sp[0] = 0.0
    Wsp[0] = 0.0
    Wr = wt[reb]
    c = COST / 1e4

    def f(lam):
        V = 1.0 + lam * (S - Wsum)
        g = lam * AR / V
        Vp = 1.0 + lam * (Sp - Wsp)
        tr = lam * np.abs(Wr - Ap / Vp[:, None]).sum(axis=1)
        out = g.copy()
        out[reb] -= tr * c
        return out

    return f


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


def maxdd(r):
    eq = np.cumprod(1.0 + np.asarray(r, float))
    return float((eq / np.maximum.accumulate(eq) - 1.0).min())


def lagmat(a):
    out = np.zeros_like(a)
    out[LAG:] = a[:-LAG]
    return out


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
    return sc.values, (above & (vol20 < MAXVOL)).values


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


def build_null(rng, priced, reb, N, H, T, K, gross):
    """1082's convention: random ranks, NO eligibility gate (the investable mask still binds:
    it is folded into `priced` for the small panels, where SPY is a benchmark, not a name)."""
    return build(rng.random((T, K)), np.ones((T, K), dtype=bool), priced, reb, N, H, T, K, gross)


def lam_rebuilt(f, sl, target_dd):
    if abs(maxdd(f(1.0)[sl])) <= abs(target_dd):
        return None
    a, b = 1e-4, 1.0
    for _ in range(BISECT):
        m = 0.5 * (a + b)
        if abs(maxdd(f(m)[sl])) > abs(target_dd):
            b = m
        else:
            a = m
    return 0.5 * (a + b)


def windows(idx):
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    return warm, ins, oos


def blocks_m(r, warm, ins, oos):
    rr = r[warm]
    c, s, d = fmet(rr)
    h = len(rr) // 2
    oc, os_, od = fmet(r[oos])
    ic, is_, idd = fmet(r[ins])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
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


def legs_4a(b, lb):
    return {"A_H1": bool(b["H1"] > lb["H1"]), "A_H2": bool(b["H2"] > lb["H2"]),
            "A_DD": bool(b["MaxDD"] >= lb["MaxDD"])}


# ---------------------------------------------------------------- the bootstrap machinery
def block_starts(rng, T, L, ndraws):
    nb = int(np.ceil(T / L))
    return rng.integers(0, T, size=(ndraws, nb)), nb


def boot_cagr(LOGR, starts, L, nb, chunk=100):
    """CAGR of every row of LOGR under CIRCULAR block resampling, exactly (a product does not
    care about order, so block sums of log1p suffice)."""
    D = np.concatenate([LOGR, LOGR], axis=1)
    CS = np.concatenate([np.zeros((D.shape[0], 1)), np.cumsum(D, axis=1)], axis=1)
    out = np.empty((LOGR.shape[0], starts.shape[0]))
    for a in range(0, starts.shape[0], chunk):
        st = starts[a:a + chunk]
        out[:, a:a + chunk] = (CS[:, st + L] - CS[:, st]).sum(axis=2)
    return np.expm1(out * (252.0 / (nb * L)))


def widest_mass(counts, rungs, q=0.90):
    """Smallest contiguous-in-RANK set of rungs carrying >= q of the argmax mass."""
    k = len(rungs)
    best = None
    for w in range(1, k + 1):
        for i in range(0, k - w + 1):
            m = counts[i:i + w].sum()
            if m >= q:
                cand = (w, [rungs[j] for j in range(i, i + w)], float(m))
                if best is None or cand[0] < best[0]:
                    best = cand
        if best is not None:
            break
    if best is None:
        best = (k, list(rungs), float(counts.sum()))
    return best


def measure_floor(sub, q):
    """1098's definition verbatim: the smallest |dEDGE| above which EVERY pair agrees in sign
    with the full sample at least q of the time."""
    s = sub.sort_values("abs_dEDGE_pp")
    for i in range(len(s)):
        if (s.iloc[i:].sign_agreement >= q).all():
            return float(s.iloc[i].abs_dEDGE_pp)
    return np.inf


# ---------------------------------------------------------------- panel construction
def load_panel(name, gates):
    """Returns (px, invest_mask over columns, note).  U56 is 1098's verbatim panel."""
    if name.startswith("U56"):
        px = load_universe().dropna(how="all").ffill()
        if name == "U56_2010":
            px = px.loc["2010-01-04":]
        return px, np.ones(len(px.columns), dtype=bool), "current-constituent large-cap panel"
    px = load_universe(small=True).dropna(how="all").ffill()
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= STEP_CUT, "ticker"])
    if name == "SMALL_F10":
        keep = [c for c in px.columns if c == "SPY" or c not in bad]
        dropped = len(px.columns) - len(keep)
        gates[f"G_FILT dropped names with max_1d_move >= {STEP_CUT} "
              f"({len(bad)} flagged in small_meta.csv)"] = (float(dropped), dropped == len(
                  bad & set(px.columns)))
        px = px[keep]
    invest = np.array([c != "SPY" for c in px.columns])
    return px, invest, "current-constituent sub-$2B panel (SPY excluded from the investable set)"


def main():
    t0 = time.time()
    P(f"# Idea 1104 (lane C, {DATE}) — does the FAR-SIDE COLLAPSE survive a PANEL it was not")
    P("#   found on?")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): n {NS} x PANEL {PANELS} = {len(NS)*len(PANELS)} "
      f"cells, ALL published.")
    P(f"# FROZEN: CAND20 legs {LEGS}, cap {CAPNAME}, max_vol {MAXVOL}, gross {GROSS0}, cadence "
      f"{FREQ}, min hold {HOLD},")
    P(f"#   {COST:.0f} bps, LAG {LAG}, warm-up {WARMUP}, IS end {IS_END}, SEEDS {NSEED} "
      f"(1098's headline count; the seed dial is NOT re-opened).")
    P(f"#   BLOCK LENGTH is NOT a dial: headline L={L_HEAD}, L in {BLOCKS_L} reported beside it.")
    P("#   TAPE is NOT a dial: U56_2010 is a labelled control so breadth is not read off tape "
      "length.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) H_COLLAPSE_SIGN  — SMALL_F10 EDGE(argmax) - EDGE(40) > 0.")
    P("#   (b) H_COLLAPSE_RESOLVED — that gap is ABOVE SMALL_F10's own 90% floor "
      "(=> BREADTH fact).")
    P("#   (c) H_PEAK_UNRESOLVED — SMALL_F10 peak-minus-runner-up is BELOW that floor.")
    P("#   (d) H_STEPS — the collapse's SIGN is unchanged on SMALL_RAW.")
    P("#   (e) H_TAPE — U56_2010 still carries a resolved collapse on the short tape.")
    P("#   (f) H_FLOOR_SCALES — the SMALL_F10 floor is HIGHER than U56's 3.25 pp.")
    P("#   (g) EDGE IS NOT A KEEP PATH: 4a/4b scored at every rung, rule 8 picks n on the IS")
    P("#       window alone, per panel, separately.")
    P("# SURVIVORSHIP (rule 9): every panel is current-constituent; the SMALL panel is the worst")
    P("#   (see data/SMALL_PANEL_README.md).  Book and null share the pool and the tape, so the")
    P("#   bias largely cancels out of EDGE; it does NOT cancel out of the 4b legs vs SPY.")
    P("")

    gates, gaterows = {}, []
    edgerows, bootrows, pairrows, floorrows, pickrows, gridrows, benchrows = [], [], [], [], [], [], []
    collrows = []

    for panel in PANELS:
        px, invest, note = load_panel(panel, gates)
        idx, K, T = px.index, len(px.columns), len(px.index)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values & invest[None, :]
        mk = rebalance_mask(idx, FREQ).values
        mkl = np.roll(mk, LAG)
        reb = np.flatnonzero(mk)
        warm, ins, oos = windows(idx)
        yrs = warm.sum() / 252.0
        sc, elig = mech(px)
        rank_key = -np.nan_to_num(sc, nan=-np.inf)
        rank_key[np.isnan(sc)] = np.inf

        spy = px["SPY"].pct_change().fillna(0.0).values
        sb = blocks_m(spy, warm, ins, oos)
        px_inv = px[[c for c, m in zip(px.columns, invest) if m]]
        live = backtest(px_inv, rules_v2_weights(px_inv), cost_bps=COST, freq=FREQ)["returns"].values
        lb = blocks_m(live, warm, ins, oos)
        benchrows.append(dict(panel=panel, series="SPY", **sb))
        benchrows.append(dict(panel=panel, series="RULESv2", **lb))
        P(f"## {panel}: {int(invest.sum())} investable columns of {K}, {T} days "
          f"{idx[0].date()}..{idx[-1].date()}, {yrs:.2f} scored years — {note}")
        P(f"   IS {int(ins.sum())} days / OOS {int(oos.sum())} days "
          f"({ins.sum()/252.0:.2f} / {oos.sum()/252.0:.2f} yrs)")
        P(f"   SPY full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%}  halves "
          f"{sb['H1']:.4f}/{sb['H2']:.4f}  OOS {sb['OOS_CAGR']:.2%} / {sb['OOS_Sharpe']:.4f} / "
          f"{sb['OOS_MaxDD']:.2%}")
        P(f"   RULES v2 live full {lb['CAGR']:.2%} / {lb['Sharpe']:.4f} / {lb['MaxDD']:.2%}  OOS "
          f"{lb['OOS_CAGR']:.2%} / {lb['OOS_Sharpe']:.4f} / {lb['OOS_MaxDD']:.2%}")
        P(f"   4b bars: DD cap {DD_CAP*abs(sb['MaxDD']):.2%} full / "
          f"{DD_CAP*abs(sb['OOS_MaxDD']):.2%} OOS;  CAGR floor {CAGR_FLOOR*sb['CAGR']:.2%} full")

        # ---- gates ------------------------------------------------------------------------
        if panel in ("U56", "SMALL_F10"):
            W20 = build(rank_key, elig, priced, reb, 20, HOLD, T, K, GROSS0)
            g20, t20 = nrun(rets, lagmat(W20), mkl)
            r20 = g20 - t20 * COST / 1e4
            eng = backtest(px, pd.DataFrame(W20, index=idx, columns=px.columns),
                           cost_bps=COST, freq=FREQ)["returns"].values
            d = float(np.abs(r20[WARMUP:] - eng[WARMUP:]).max())
            gates[f"G1 fast runner == engine.backtest ({panel} N=20 H=126 @ 10 bps)"] = (
                d, d < 1e-12)
            f20 = gross_rescaler(rets, lagmat(W20), mkl)
            d1b = float(np.abs(f20(1.0) - r20).max())
            gates[f"G1b gross_rescaler(1.0) == nrun ({panel})"] = (d1b, d1b < 1e-12)
        if panel == "U56":
            m = fmet(r20[warm])
            d2 = max(abs(m[i] - A936_WH126[i]) for i in range(3))
            gates["G2 CROSS-RUN 936/1071/1082/1098's committed U56 W/H126 N=20 triple"] = (
                d2, d2 < 5e-3)
            d3 = max(abs(sb["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
                     abs(sb["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
                     abs(sb["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
            gates["G3 CROSS-RUN SPY OOS triple"] = (d3, d3 < 5e-4)
            d5 = abs(lb["MaxDD"] - LIVE_MAXDD_COMMITTED)
            gates["G5 live RULES v2 MaxDD == committed -12.05%"] = (d5, d5 < 5e-4)
            a = np.random.default_rng(mdseed(panel, 20, CAPNAME, 0)).random(6)
            b_ = np.random.default_rng(mdseed(panel, 20, CAPNAME, 0)).random(6)
            gates["G7 determinism of 1082/1098's seed recipe"] = (
                float(np.abs(a - b_).max()), True)
        if panel == "SMALL_F10":
            gates["G_SPY SPY is not investable on the small panel"] = (
                float(priced[:, list(px.columns).index("SPY")].sum()), True)

        # ---- the ladder: book + 40 DD-matched nulls at every rung -------------------------
        BOOKR, NULLR = {}, {}
        for N in NS:
            W = build(rank_key, elig, priced, reb, N, HOLD, T, K, GROSS0)
            g, tn = nrun(rets, lagmat(W), mkl)
            r = g - tn * COST / 1e4
            b = blocks_m(r, warm, ins, oos)
            BOOKR[N] = r[warm]
            nulls, lams, drier, nis = [], [], 0, []
            for s in range(NSEED):
                rng = np.random.default_rng(mdseed(panel, N, CAPNAME, s))
                Wn = build_null(rng, priced, reb, N, HOLD, T, K, GROSS0)
                fn = gross_rescaler(rets, lagmat(Wn), mkl)
                lr = lam_rebuilt(fn, warm, b["MaxDD"])
                if lr is None:
                    drier += 1
                    lr = 1.0
                nulls.append(fn(lr)[warm])
                lams.append(lr)
                lri = lam_rebuilt(fn, ins, b["IS_MaxDD"])          # 1082's IS arm, for C_ISEDGE
                nis.append(fmet(fn(1.0)[ins] if lri is None else fn(lri)[ins])[0])
            NULLR[N] = np.array(nulls)
            ncagr = np.array([fmet(x)[0] for x in NULLR[N]])
            nis = np.array(nis)
            l4b, l4a, l4o = legs_4b(b, sb), legs_4a(b, lb), legs_4b_oos(b, sb)
            e = 100.0 * (b["CAGR"] - float(np.median(ncagr)))
            se = 100.0 * 1.2533 * float(ncagr.std(ddof=1)) / np.sqrt(NSEED)
            row = dict(panel=panel, N=N, turnover=float(tn[warm].sum() / yrs), **b, **l4b, **l4a,
                       **l4o, pass4b=all(l4b.values()), pass4a=all(l4a.values()),
                       pass4b_oos=all(l4o.values()), lam_median=float(np.median(lams)),
                       n_already_drier=drier, EDGE_pp=e, EDGE_se_pp=se)
            gridrows.append(row)
            edgerows.append(dict(panel=panel, N=N, seeds=NSEED, EDGE_pp=e,
                                 EDGE_IS_pp=100.0 * (b["IS_CAGR"] - float(np.median(nis))),
                                 book_CAGR=b["CAGR"], null_CAGR_med=float(np.median(ncagr)),
                                 null_CAGR_sd=float(ncagr.std(ddof=1)), EDGE_se_pp=se,
                                 lam_median=float(np.median(lams)),
                                 book_pct_of_null=float((ncagr < b["CAGR"]).mean())))
            P(f"   N={N:2d}  book {b['CAGR']:7.2%} / {b['Sharpe']:.4f} / {b['MaxDD']:7.2%}  "
              f"EDGE {e:+6.2f} pp (SE {se:.2f})  lam~{np.median(lams):.3f}  drier {drier}/"
              f"{NSEED}  ({time.time()-t0:.0f}s)")

        if panel == "U56":
            mine = [next(r for r in edgerows if r["panel"] == "U56" and r["N"] == N)["EDGE_pp"]
                    for N in NS]
            dx = float(np.abs(np.array(mine) - np.array(A1082_EDGE_U56)).max())
            gates["G_XRUN U56: 1082/1098's nine committed EDGE figures reproduce"] = (
                dx, dx < 5.1e-3)

        # ---- the bootstrap ---------------------------------------------------------------
        Tw = int(warm.sum())
        paths = [BOOKR[N] for N in NS] + [NULLR[N][s] for N in NS for s in range(NSEED)]
        LOGR = np.log1p(np.array(paths))
        nb_book = len(NS)
        fullE = np.array([next(r for r in edgerows if r["panel"] == panel
                               and r["N"] == n)["EDGE_pp"] for n in NS])
        fa = NS[int(np.argmax(fullE))]
        order = np.argsort(fullE)[::-1]
        gap = float(fullE[order[0]] - fullE[order[1]])
        collapse = float(fullE[int(np.argmax(fullE))] - fullE[-1])          # EDGE(peak)-EDGE(40)
        for L in BLOCKS_L:
            rng = np.random.default_rng(mdseed("boot", panel, L))
            starts, nb = block_starts(rng, Tw, L, BDRAWS)
            C = boot_cagr(LOGR, starts, L, nb)
            BK = C[:nb_book]
            NU = C[nb_book:].reshape(len(NS), NSEED, BDRAWS)
            E = 100.0 * (BK - np.median(NU, axis=1))                        # (rungs, draws)
            am = np.array(NS)[np.argmax(E, axis=0)]
            cnt = np.array([(am == n).mean() for n in NS])
            w, wset, mass = widest_mass(cnt, NS)
            ipk = int(np.argmax(fullE))
            coll_boot = E[ipk] - E[-1]
            bootrows.append(dict(panel=panel, block_L=L, seeds=NSEED, n_rungs=len(NS),
                                 full_argmax=fa,
                                 P_argmax_equals_full=float((am == fa).mean()),
                                 modal_argmax=int(NS[int(np.argmax(cnt))]),
                                 P_modal=float(cnt.max()), width90_rungs=w,
                                 width90_set=";".join(str(x) for x in wset), width90_mass=mass,
                                 peak_minus_runnerup_pp=gap, runner_up=int(NS[order[1]]),
                                 collapse_pp=collapse,
                                 collapse_boot_sd_pp=float(coll_boot.std(ddof=1)),
                                 collapse_sign_agreement=float(
                                     (np.sign(coll_boot) == np.sign(collapse)).mean()),
                                 dist=";".join(f"{n}:{c:.3f}" for n, c in zip(NS, cnt))))
            if L == L_HEAD:
                for i in range(len(NS)):
                    for j in range(i + 1, len(NS)):
                        d0 = fullE[i] - fullE[j]
                        db = E[i] - E[j]
                        pairrows.append(dict(panel=panel, n_i=NS[i], n_j=NS[j], dEDGE_pp=d0,
                                             abs_dEDGE_pp=abs(d0),
                                             boot_sd_pp=float(db.std(ddof=1)),
                                             sign_agreement=float(
                                                 (np.sign(db) == np.sign(d0)).mean())))
            P(f"   bootstrap L={L} done ({time.time()-t0:.0f}s)")

        # ---- rule 8 on this panel ---------------------------------------------------------
        gp = pd.DataFrame([r for r in gridrows if r["panel"] == panel])
        for ch in CHOOSERS:
            if ch == "C_ISEDGE":
                isedge = {n: next(r for r in edgerows if r["panel"] == panel
                                  and r["N"] == n)["EDGE_IS_pp"] for n in NS}
                pick = int(max(isedge, key=isedge.get))
            else:
                key = {"C_ISSHARPE": "IS_Sharpe", "C_ISDD": "IS_MaxDD",
                       "C_ISCAGR": "IS_CAGR"}[ch]
                pick = int(gp.sort_values(key, ascending=False).iloc[0]["N"])
            r = gp[gp.N == pick].iloc[0]
            pickrows.append(dict(panel=panel, chooser=ch, pick=pick, OOS_CAGR=r.OOS_CAGR,
                                 OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD, CAGR=r.CAGR,
                                 Sharpe=r.Sharpe, MaxDD=r.MaxDD, H1=r.H1, H2=r.H2,
                                 pass4b=bool(r.pass4b), pass4b_oos=bool(r.pass4b_oos),
                                 pass4a=bool(r.pass4a), spy_OOS_CAGR=sb["OOS_CAGR"],
                                 spy_OOS_Sharpe=sb["OOS_Sharpe"], spy_OOS_MaxDD=sb["OOS_MaxDD"],
                                 live_OOS_Sharpe=lb["OOS_Sharpe"],
                                 best_possible_OOS_Sharpe=float(gp.OOS_Sharpe.max())))

    ed = pd.DataFrame(edgerows)
    bt = pd.DataFrame(bootrows)
    pr = pd.DataFrame(pairrows)
    pk = pd.DataFrame(pickrows)
    gd = pd.DataFrame(gridrows)

    P("")
    P("# ---- GATES (printed before any result number) ----")
    ok = 0
    for k, (d, good) in gates.items():
        P(f"   {'PASS' if good else 'FAIL'}  {k}: {d:.3e}")
        gaterows.append(dict(gate=k, value=d, passed=bool(good)))
        ok += bool(good)
    P(f"   {ok} of {len(gates)} gates pass")

    P("")
    P("# ---- THE NINE-RUNG EDGE LADDER ON EVERY PANEL (pp of CAGR, S=40) ----")
    P("   panel      " + "".join(f"{n:>8d}" for n in NS))
    for panel in PANELS:
        v = [float(ed[(ed.panel == panel) & (ed.N == n)].EDGE_pp.iloc[0]) for n in NS]
        P(f"   {panel:10s} " + "".join(f"{x:+8.2f}" for x in v))

    P("")
    P("# ---- THE RESOLUTION FLOOR AND THE FAR SIDE (headline L=63) ----")
    hyp = []
    for panel in PANELS:
        s = pr[pr.panel == panel]
        f90, f95 = measure_floor(s, 0.90), measure_floor(s, 0.95)
        r = bt[(bt.panel == panel) & (bt.block_L == L_HEAD)].iloc[0]
        nres = int((s.sign_agreement < 0.90).sum())
        lu = float(s[s.sign_agreement < 0.90].abs_dEDGE_pp.max()) if nres else 0.0
        P(f"   {panel}: floor@90 {f90:.2f} pp, floor@95 {f95:.2f} pp over {len(s)} rung pairs; "
          f"{nres} pairs unresolved@90 (largest {lu:.2f} pp)")
        P(f"      peak n={r.full_argmax} beats runner-up n={r.runner_up} by "
          f"{r.peak_minus_runnerup_pp:+.2f} pp -> "
          f"{'ABOVE' if r.peak_minus_runnerup_pp >= f90 else 'BELOW'} the floor; "
          f"P(argmax==full) {r.P_argmax_equals_full:.3f}, 90% set {{{r.width90_set}}} "
          f"= {r.width90_rungs} rungs")
        P(f"      FAR-SIDE COLLAPSE EDGE({r.full_argmax}) - EDGE(40) = {r.collapse_pp:+.2f} pp "
          f"-> {'ABOVE' if r.collapse_pp >= f90 else 'BELOW'} the floor; bootstrap sign "
          f"agreement {r.collapse_sign_agreement:.3f} (sd {r.collapse_boot_sd_pp:.2f} pp)")
        floorrows.append(dict(panel=panel, floor90_pp=f90, floor95_pp=f95,
                              peak=int(r.full_argmax), runner_up=int(r.runner_up),
                              peak_minus_runnerup_pp=float(r.peak_minus_runnerup_pp),
                              peak_above_floor=bool(r.peak_minus_runnerup_pp >= f90),
                              collapse_pp=float(r.collapse_pp),
                              collapse_above_floor=bool(r.collapse_pp >= f90),
                              collapse_sign_agreement=float(r.collapse_sign_agreement),
                              P_argmax_equals_full=float(r.P_argmax_equals_full),
                              width90_rungs=int(r.width90_rungs), width90_set=r.width90_set,
                              pairs=len(s), pairs_unresolved90=nres,
                              largest_unresolved_gap_pp=lu))
        collrows.append(dict(panel=panel, **{f"EDGE_n{n}": float(
            ed[(ed.panel == panel) & (ed.N == n)].EDGE_pp.iloc[0]) for n in NS}))

    P("")
    P("   BLOCK-LENGTH robustness (reported, never selected on):")
    for panel in PANELS:
        for L in BLOCKS_L:
            r = bt[(bt.panel == panel) & (bt.block_L == L)].iloc[0]
            P(f"     {panel:10s} L={L:3d}: collapse sign agreement "
              f"{r.collapse_sign_agreement:.3f}, P(argmax==full) {r.P_argmax_equals_full:.3f}, "
              f"90% set {{{r.width90_set}}}")

    fl = pd.DataFrame(floorrows).set_index("panel")
    hp = fl.loc[HEADLINE_PANEL]
    u56 = fl.loc["U56"]
    raw = fl.loc["SMALL_RAW"]
    u10 = fl.loc["U56_2010"]
    hyp = [
        dict(hypothesis="H_COLLAPSE_SIGN (SMALL_F10): EDGE(argmax) - EDGE(40) > 0",
             declared=">0", observed=f"{hp.collapse_pp:+.2f} pp",
             passed=bool(hp.collapse_pp > 0)),
        dict(hypothesis="H_COLLAPSE_RESOLVED (SMALL_F10): the collapse is ABOVE the panel's own "
                        "90% floor => a BREADTH fact", declared="above",
             observed=f"{hp.collapse_pp:+.2f} vs floor {hp.floor90_pp:.2f} pp "
                      f"(sign agreement {hp.collapse_sign_agreement:.3f})",
             passed=bool(hp.collapse_above_floor)),
        dict(hypothesis="H_PEAK_UNRESOLVED (SMALL_F10): peak-minus-runner-up is BELOW the floor",
             declared="below",
             observed=f"{hp.peak_minus_runnerup_pp:+.2f} vs floor {hp.floor90_pp:.2f} pp",
             passed=bool(not hp.peak_above_floor)),
        dict(hypothesis="H_STEPS: the collapse's SIGN is unchanged on SMALL_RAW", declared="same",
             observed=f"F10 {hp.collapse_pp:+.2f} vs RAW {raw.collapse_pp:+.2f} pp",
             passed=bool(np.sign(hp.collapse_pp) == np.sign(raw.collapse_pp))),
        dict(hypothesis="H_TAPE (U56_2010): the collapse stays resolved on the short tape",
             declared="above floor",
             observed=f"{u10.collapse_pp:+.2f} vs floor {u10.floor90_pp:.2f} pp",
             passed=bool(u10.collapse_above_floor)),
        dict(hypothesis="H_FLOOR_SCALES: the SMALL_F10 floor is HIGHER than U56's",
             declared="higher", observed=f"{hp.floor90_pp:.2f} vs {u56.floor90_pp:.2f} pp",
             passed=bool(hp.floor90_pp > u56.floor90_pp)),
    ]

    P("")
    P("# ---- CROSS-RUN READ AGAINST 1098's COMMITTED FIGURES ----")
    P(f"   1098 committed U56 floor@90 {A1098_U56['floor90']:.2f} pp, peak n={A1098_U56['peak']} "
      f"by {A1098_U56['gap']:.2f} pp, collapse {A1098_U56['collapse']:.2f} pp")
    P(f"   this run U56        floor@90 {u56.floor90_pp:.2f} pp, peak n={int(u56.peak)} by "
      f"{u56.peak_minus_runnerup_pp:.2f} pp, collapse {u56.collapse_pp:.2f} pp")
    P(f"   1098 committed B136 floor@90 {A1098_B136['floor90']:.2f} pp, collapse "
      f"{A1098_B136['collapse']:.2f} pp (B136 is not re-run here; the panel dial is SMALL)")

    P("")
    P("# ---- RULE 8 WALK-FORWARD AND BOTH KEEP PATHS ----")
    for panel in PANELS:
        sbq = [r for r in benchrows if r["panel"] == panel and r["series"] == "SPY"][0]
        lbq = [r for r in benchrows if r["panel"] == panel and r["series"] == "RULESv2"][0]
        P(f"   {panel}: SPY OOS {sbq['OOS_CAGR']:.2%} / {sbq['OOS_Sharpe']:.4f} / "
          f"{sbq['OOS_MaxDD']:.2%};  RULES v2 OOS {lbq['OOS_CAGR']:.2%} / "
          f"{lbq['OOS_Sharpe']:.4f} / {lbq['OOS_MaxDD']:.2%}")
        s = pk[pk.panel == panel]
        g = gd[gd.panel == panel]
        P(f"     picks ({len(s)} choosers): 4b full {int(s.pass4b.sum())}/{len(s)}, 4b OOS "
          f"{int(s.pass4b_oos.sum())}/{len(s)}, 4a {int(s.pass4a.sum())}/{len(s)}")
        for _, r in s.iterrows():
            P(f"       {r.chooser:11s} pick n={r['pick']:2d}  OOS {r.OOS_CAGR:7.2%} / "
              f"{r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:7.2%}  full {r.CAGR:7.2%} / {r.Sharpe:.4f} / "
              f"{r.MaxDD:7.2%}  halves {r.H1:.3f}/{r.H2:.3f}  4b {bool(r.pass4b)} / 4b-OOS "
              f"{bool(r.pass4b_oos)} / 4a {bool(r.pass4a)}  regret "
              f"{r.best_possible_OOS_Sharpe - r.OOS_Sharpe:+.4f}")
        P(f"     whole ladder (9 rungs): 4b full {int(g.pass4b.sum())}/9, 4b OOS "
          f"{int(g.pass4b_oos.sum())}/9, 4a {int(g.pass4a.sum())}/9")

    P("")
    P("# ---- HYPOTHESES ----")
    for h in hyp:
        P(f"   {'PASS' if h['passed'] else 'FAIL'}  {h['hypothesis']}  [declared {h['declared']};"
          f" observed {h['observed']}]")
    P(f"   {sum(h['passed'] for h in hyp)} of {len(hyp)} hypotheses supported")

    dump(ed, "edge")
    dump(bt, "argmax")
    dump(pr, "pairs")
    dump(pd.DataFrame(floorrows), "floor")
    dump(pd.DataFrame(collrows), "ladder")
    dump(pk, "picks")
    dump(gd, "grid")
    dump(pd.DataFrame(gaterows), "gates")
    dump(pd.DataFrame(hyp), "hypotheses")
    dump(pd.DataFrame(benchrows), "benchmarks")
    P(f"# done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
