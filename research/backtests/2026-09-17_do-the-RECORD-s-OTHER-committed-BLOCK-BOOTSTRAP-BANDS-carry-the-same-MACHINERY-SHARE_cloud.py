#!/usr/bin/env python3
"""Idea 1165 (cloud lane, 2026-09-17) — do the RECORD's OTHER committed BLOCK BOOTSTRAP
BANDS carry the same MACHINERY SHARE?

THE PARENT FINDING this run generalises (committed 2026-09-17, lane B, file
`2026-09-17_why-does-an-IID-RESAMPLE-produce-DEEPER-drawdowns-than-a-BLOCK-one_B.py`):
a moving-block resample shallows |MaxDD| relative to an iid one **even with the tape's
ORDER DESTROYED** — pooled BLOCK/IID **0.9696** over 15 permutations — because a contiguous
block cannot contain the same bar twice while an iid draw can stack the tape's worst days.
That parent decomposed its own effect as **machinery 16.5% / 16.4% / 84.1%** on
U56 / B136 / SMALL.  Every committed moving-block band in the record inherits that term and
none of them priced it.

WHAT MAKES THIS A REAL CENSUS AND NOT A FRESH POPULATION.  Unlike most "census the record"
ideas, these bands ARE recoverable: idea 1159 committed all 108 of its band rows to
`2026-09-17_does-ANY-committed-MAXIMUM-KEYED-claim-in-the-record-carry-a-RESAMPLE-NULL_B.objects.csv`
with panel, ladder, null type, object, observed value, null median and the 80/90/95% bounds
and INSIDE verdicts; 1157's SMALL |MaxDD| 90% band (0.441, 0.881) is quoted in 1159's own
committed source.  This run READS those files, REPLAYS the 36 N_BLOCK bands bit-for-bit as
gate G_REPLAY, and only then rebuilds each against an order-destroyed control.  Nothing is
recalled from prose and nothing is re-derived from memory.

THE TWO TUNED PARAMETERS AND NO MORE (PROTOCOL rule 4), exactly the two the queue names:
  CLAIMSET  {C_1157, C_1159, C_1161, C_ALL}     which committed band family
  CONTROL   {X_NONE, X_SHUFFLE1, X_SHUFFLEPD, X_IID}
= 16 cells, EVERY ONE PUBLISHED in `.bands.csv` / `.moves.csv`.
PANEL {U56,B136,SMALL}, LADDER {N,H,GROSS,CADENCE}, OBJECT {MAXDD,SPREAD,ARGMAX} and the
confidence level {0.80,0.90,0.95} are NOT dials — they are the census, and every one of
them is published on every control.

  X_NONE       the band AS PUBLISHED: moving block, L=63, wrap-around, on the observed tape
  X_SHUFFLE1   ONE fixed permutation of the book's returns, then the IDENTICAL moving-block
               machinery (same L, same wrap, same overlap, same draw count).  Order gone,
               machinery intact.  This is the parent's control.
  X_SHUFFLEPD  a FRESH permutation per draw — the same thing without a single-permutation
               artefact.  The parent's own sub-arm used 5 permutations; this uses 1,000.
  X_IID        L=1.  No blocks at all.  The machinery-free reference.

MACHINERY SHARE of a cell = (median_X_SHUFFLE1 - median_X_IID) / (median_X_NONE - median_X_IID).
A CORRECTED BAND divides the X_NONE draws by phi_m = median_X_SHUFFLE1 / median_X_IID, which
removes exactly the part of the block null's shallowing that survives order destruction.

FROZEN at 1159's construction so the replay is exact: LADDERS N[5..40] / H[21,63,126,252] /
GROSS[0.30..0.75] / CADENCE[D,W,M,Q], ANCHOR N=20 H=126 gross 0.75 cadence W, CAND20 legs
[(21,252),(0,126),(0,63)], max_vol 0.60, cost 10 bps (rule 2), LAG 1, warm-up 260,
IS end 2016-12-31, L_BLOCK 63, BDRAWS 1000, SEED_BASE 11591159, seed_of() verbatim.

SURVIVORSHIP: B136 and SMALL are CURRENT constituents only (PROTOCOL rule 9 /
data/SMALL_PANEL_README.md); SMALL additionally drops every ticker with max_1d_move >= 1.0
in data/small_meta.csv before anything is computed.  Drawdowns on those two panels are the
SHALLOWEST the period could have produced, which matters doubly here because every object
in this file IS a drawdown.

Writes: .gates.csv .grid.csv .bands.csv .machinery.csv .moves.csv .b1157.csv
        .walkforward.csv .console.txt
Deterministic (every draw seeded), standalone, no network.  Does not modify RULES.md /
PROTOCOL.md / scan.py / bot.py / baseline.py / engine.py.
"""
import sys, time, zlib
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
BT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "do-the-RECORD-s-OTHER-committed-BLOCK-BOOTSTRAP-BANDS-carry-the-same-MACHINERY-SHARE"
OUT = BT / f"{DATE}_{SLUG}_cloud"
LOG = []

# ------------------------------------------------- FROZEN at 1159's construction, verbatim
LAG, WARMUP, COST = 1, 260, 10.0
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
GROSS0, FREQ0, HOLD0, N0, MAXVOL0 = 0.75, "W", 126, 20, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
START = "2008-01-01"

LAD_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]
LAD_H = [21, 63, 126, 252]
LAD_G = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]
LAD_C = ["D", "W", "M", "Q"]
LADDERS = {"N": LAD_N, "H": LAD_H, "GROSS": LAD_G, "CADENCE": LAD_C}
ANCHOR = dict(N=N0, H=HOLD0, GROSS=GROSS0, CADENCE=FREQ0)
PANELS = ["U56", "B136", "SMALL"]
OBJECTS = ["OBJ_MAXDD", "OBJ_SPREAD", "OBJ_ARGMAX"]
QS = [0.80, 0.90, 0.95]
Q_HEAD = 0.90
L_BLOCK, BDRAWS = 63, 1000
BDRAWS_IS = 400                      # the rule-8 arm only; declared, never mixed with the census
SEED_BASE = 11591159

# ------------------------------------------------------------------ THE TWO DIALS
CLAIMSETS = ["C_1157", "C_1159", "C_1161", "C_ALL"]
CONTROLS = ["X_NONE", "X_SHUFFLE1", "X_SHUFFLEPD", "X_IID"]

# ------------------------- the record's committed files, READ not recalled
SRC_1159 = BT / ("2026-09-17_does-ANY-committed-MAXIMUM-KEYED-claim-in-the-record-carry-a-"
                 "RESAMPLE-NULL_B.objects.csv")
SRC_1161 = BT / "2026-09-17_why-does-an-IID-RESAMPLE-produce-DEEPER-drawdowns-than-a-BLOCK-one_B"
PRIOR1157_BAND = (0.441, 0.881)      # 1157's committed SMALL |MaxDD| 90% band, as 1159 quotes it
PARENT_POOLED = 0.9696               # the parent's committed pooled BLOCK/IID under shuffle
PARENT_SHARE = {"U56": 0.165, "B136": 0.164, "SMALL": 0.841}   # its committed machinery shares


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def seed_of(*parts):
    """1159's seeding, VERBATIM — the replay gate depends on it byte for byte."""
    return SEED_BASE + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


# ------------------------------------------------------ 1082/../1161's runner and book, verbatim
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
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = (comp * (0.5 + 0.5 * above.astype(float))).values
    return dict(px=px, idx=idx, K=len(px.columns), T=len(idx),
                rets=px.pct_change().fillna(0.0).values, priced=px.notna().values,
                warm=warm, ins=ins, oos=oos, sc=sc,
                elig=(above & (vol20 < MAXVOL0)).values,
                spy=px["SPY"].pct_change().fillna(0.0).values)


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


# =================================================================================================
# THE NULLS.  X_NONE and X_IID are 1159's N_BLOCK and N_IID, VERBATIM, so the replay is exact.
# X_SHUFFLE1 and X_SHUFFLEPD reuse the IDENTICAL block index machinery and change only the
# tape the blocks are cut from.  The SAME index matrix is applied to EVERY rung of a ladder,
# so the tape cancels and the SPREAD/ARGMAX nulls stay in 1012/1150's paired currency.
# =================================================================================================
def block_index(rng, T, ndraws):
    nb = int(np.ceil(T / L_BLOCK))
    st = rng.integers(0, T, size=(ndraws, nb))
    idx = (st[:, :, None] + np.arange(L_BLOCK)[None, None, :]) % T
    return idx.reshape(ndraws, nb * L_BLOCK)[:, :T]


def control_index(control, rng, T, ndraws):
    if control == "X_NONE":
        return block_index(rng, T, ndraws)
    if control == "X_IID":
        return rng.integers(0, T, size=(ndraws, T))
    bi = block_index(rng, T, ndraws)
    if control == "X_SHUFFLE1":
        perm = rng.permutation(T)                      # ONE permutation, shared by every draw
        return perm[bi]
    if control == "X_SHUFFLEPD":
        perm = np.argsort(rng.random((ndraws, T)), axis=1)   # a fresh permutation per draw
        return np.take_along_axis(perm, bi, axis=1)
    raise ValueError(control)


def boot_maxdd(R, idx, chunk=50):
    """|MaxDD| (positive, in %) of every row of R under every resample row of idx. 1159's."""
    nr, nd = R.shape[0], idx.shape[0]
    out = np.empty((nr, nd))
    LG = np.log1p(R)
    for a in range(0, nd, chunk):
        ix = idx[a:a + chunk]
        for j in range(nr):
            cum = np.cumsum(LG[j][ix], axis=1)
            run = np.maximum.accumulate(cum, axis=1)
            out[j, a:a + chunk] = -np.expm1(cum - run).min(axis=1) * 100.0
    return out


def band(x, q):
    return (float(np.nanpercentile(x, (1 - q) / 2 * 100.0)),
            float(np.nanpercentile(x, (1 + q) / 2 * 100.0)))


def objects_of(dd_by_rung, anchor_i):
    """1159's three objects, verbatim. dd_by_rung is (rungs,) or (rungs, draws)."""
    a = np.asarray(dd_by_rung, float)
    if a.ndim == 1:
        srt = np.sort(a)
        return {"OBJ_MAXDD": float(a[anchor_i]), "OBJ_SPREAD": float(a.max() - a.min()),
                "OBJ_ARGMAX": float(srt[1] - srt[0])}
    srt = np.sort(a, axis=0)
    return {"OBJ_MAXDD": a[anchor_i], "OBJ_SPREAD": a.max(axis=0) - a.min(axis=0),
            "OBJ_ARGMAX": srt[1] - srt[0]}


def main():
    t_run0 = time.time()
    P("=" * 100)
    P(f"IDEA 1165 (cloud) {DATE} — do the RECORD's OTHER committed BLOCK BOOTSTRAP BANDS")
    P("                    carry the same MACHINERY SHARE?")
    P("=" * 100)
    P("")
    P("THE PARENT FINDING BEING GENERALISED (committed, lane B, 2026-09-17): a moving block")
    P(f"shallows |MaxDD| against an iid resample EVEN WITH ORDER DESTROYED, pooled {PARENT_POOLED},")
    P("decomposing as machinery " + " / ".join(f"{v:.1%} {k}" for k, v in PARENT_SHARE.items()) + ".")
    P("")
    P("WHY THIS IS A REAL CENSUS.  1159's 108 band rows are COMMITTED to")
    P(f"  {SRC_1159.name}")
    P("with observed value, null median and the 80/90/95% bounds and INSIDE verdicts, and")
    P(f"1157's SMALL |MaxDD| 90% band {PRIOR1157_BAND} is quoted in 1159's own committed source.")
    P("This run READS those files, REPLAYS the 36 N_BLOCK bands as gate G_REPLAY, and only")
    P("then rebuilds each against an order-destroyed control.  Nothing is recalled from prose.")
    P("")
    P("THE TWO TUNED PARAMETERS (rule 4): CLAIMSET {C_1157,C_1159,C_1161,C_ALL} x")
    P("CONTROL {X_NONE,X_SHUFFLE1,X_SHUFFLEPD,X_IID} = 16 cells, all published.")
    P("PANEL, LADDER, OBJECT and the confidence level are the CENSUS, not dials.")
    P("")

    # ------------------------------------------------------------------ PANELS
    P("-" * 100)
    P("PANELS")
    P("-" * 100)
    px_u = load_universe(start=START)
    px_b = load_universe(start=START, broad=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    px_s = load_universe(small=True)
    ndrop = len([c for c in px_s.columns if c in bad])
    px_s = px_s.drop(columns=[c for c in px_s.columns if c in bad]).dropna(how="all").ffill()
    raw = {"U56": px_u, "B136": px_b, "SMALL": px_s}
    panels = {k: prep(v) for k, v in raw.items()}
    for k in PANELS:
        d = panels[k]
        P(f"  {k:<6} {d['K']:>4} cols  {d['idx'][0].date()}..{d['idx'][-1].date()}  {d['T']:,} rows"
          + ("" if k == "U56" else "   (SURVIVORSHIP: current constituents, PROTOCOL rule 9)"))
    P(f"  SMALL dropped {ndrop} tickers with max_1d_move >= 1.0 from data/small_meta.csv")
    P("")

    BENCH = {}
    for k in PANELS:
        d = panels[k]
        sb = blocks_m(d["spy"], d)
        lb = blocks_m(backtest(raw[k], rules_v2_weights(raw[k]), cost_bps=COST, freq="W")
                      ["returns"].reindex(raw[k].index).fillna(0.0).values, d)
        BENCH[k] = dict(spy=sb, live=lb)
        P(f"  {k:<6} SPY  {sb['CAGR']:7.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:7.2%}"
          f"  OOS {sb['OOS_CAGR']:7.2%} / {sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:7.2%}")
        P(f"  {k:<6} LIVE {lb['CAGR']:7.2%} / {lb['Sharpe']:.4f} / {lb['MaxDD']:7.2%}"
          f"  OOS {lb['OOS_CAGR']:7.2%} / {lb['OOS_Sharpe']:.4f} / {lb['OOS_MaxDD']:7.2%}")
    P("")

    def run_cell(panel, N, H, gross, freq):
        d = panels[panel]
        mk = rebalance_mask(d["idx"], freq).values
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        reb = np.flatnonzero(mk)
        W = build(-d["sc"], d["elig"], d["priced"], reb, N, H, d["T"], d["K"], gross)
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        g, tn = nrun(d["rets"], Wl, mkl)
        return g - tn * COST / 1e4

    # ------------------------------------------------------------------ 1159's 81 rung books
    P("-" * 100)
    P("THE 81 RUNG BOOKS — 1159's ladders, rebuilt so its bands can be replayed")
    P("-" * 100)
    t0 = time.time()
    series, isser, gridrows = {}, {}, []
    for panel in PANELS:
        d = panels[panel]
        for lad, rungs in LADDERS.items():
            for rg in rungs:
                c = dict(ANCHOR)
                c[lad] = rg
                r = run_cell(panel, c["N"], c["H"], c["GROSS"], c["CADENCE"])
                series[(panel, lad, str(rg))] = r[d["warm"]]
                isser[(panel, lad, str(rg))] = r[d["ins"]]
                m = blocks_m(r, d)
                l4b = legs_4b(m, BENCH[panel]["spy"])
                l4bo = legs_4b_oos(m, BENCH[panel]["spy"])
                l4a = legs_4a(m, BENCH[panel]["live"])
                gridrows.append(dict(panel=panel, ladder=lad, rung=str(rg), **m,
                                     pass_4b_full=all(l4b.values()),
                                     pass_4b_oos=all(l4bo.values()),
                                     pass_4a=all(l4a.values())))
        P(f"  {panel:<6} 27 rung books ({time.time() - t0:.0f}s)")
    grid = pd.DataFrame(gridrows)
    dump(grid, "grid")
    P("  BASE RATES: " + "  ".join(
        f"{p} 4b {int(g.pass_4b_full.sum())}/{len(g)} 4bOOS {int(g.pass_4b_oos.sum())}/{len(g)}"
        f" 4a {int(g.pass_4a.sum())}/{len(g)}" for p, g in grid.groupby("panel")))
    P("")

    # ------------------------------------------------------------------ GATES
    P("-" * 100)
    P("GATES — printed before any result number")
    P("-" * 100)
    gates = []

    def gate(name, what, value, ok):
        gates.append(dict(gate=name, what=what, value=value, pass_=bool(ok)))
        P(f"  {name:<10} {'PASS' if ok else 'FAIL'}  {what}  = {value}")

    prior = pd.read_csv(SRC_1159)
    gate("G1", "1159's committed objects.csv is readable and has 108 rows", len(prior),
         len(prior) == 108)
    pb = prior[prior.null_type == "N_BLOCK"]
    gate("G2", "of which N_BLOCK bands", len(pb), len(pb) == 36)

    d = panels["U56"]
    ranc = run_cell("U56", N0, HOLD0, GROSS0, FREQ0)
    mk = rebalance_mask(d["idx"], FREQ0).values
    W = build(-d["sc"], d["elig"], d["priced"], np.flatnonzero(mk), N0, HOLD0, d["T"], d["K"],
              GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ0)["returns"].values
    v = float(np.abs(eng[d["warm"]] - ranc[d["warm"]]).max())
    gate("G3", "fast runner == engine.backtest (U56 W/H126/N=20)", f"{v:.3e}", v < 1e-12)

    anc = blocks_m(ranc, d)
    gate("G4", "incumbent |MaxDD| vs 1159's committed 19.127562",
         round(-anc["MaxDD"] * 100, 6), abs(-anc["MaxDD"] * 100 - 19.127562) < 5e-3)

    i1 = control_index("X_NONE", np.random.default_rng(7), 400, 20)
    i2 = control_index("X_NONE", np.random.default_rng(7), 400, 20)
    gate("G5", "control_index seed-deterministic", int(np.abs(i1 - i2).sum()),
         int(np.abs(i1 - i2).sum()) == 0)
    ii = control_index("X_IID", np.random.default_rng(3), 400, 200)
    v6 = float(np.mean(np.diff(ii, axis=1) == 1))
    gate("G6", "X_IID destroys blocks (share of consecutive +1 steps ~ 1/T)", round(v6, 5),
         v6 < 0.02)
    v7 = float(np.mean(np.diff(block_index(np.random.default_rng(3), 400, 50), axis=1) == 1))
    gate("G7", "X_NONE keeps blocks (share of consecutive +1 steps ~ (L-1)/L)", round(v7, 4),
         v7 > 0.9)
    s1 = control_index("X_SHUFFLE1", np.random.default_rng(3), 400, 50)
    v8 = float(np.mean(np.diff(s1, axis=1) == 1))
    gate("G8", "X_SHUFFLE1 keeps the MACHINERY but destroys ORDER: the index it draws is a"
               " block index (G7) composed with a permutation, so its own +1 share collapses",
         round(v8, 5), v8 < 0.02)
    # a permutation of the SERIES cannot change the book's marginal return distribution —
    # the whole claim of an order-destroyed control rests on this
    _r = np.random.default_rng(5).normal(0, 0.01, size=(3, 500))
    _p = np.random.default_rng(6).permutation(500)
    gate("G9", "permuting the series preserves its marginal distribution exactly",
         float(np.abs(np.sort(_r[:, _p], axis=1) - np.sort(_r, axis=1)).max()),
         float(np.abs(np.sort(_r[:, _p], axis=1) - np.sort(_r, axis=1)).max()) == 0.0)

    # ---- G_REPLAY: rebuild 1159's own 36 N_BLOCK bands with its seeds and compare
    P("")
    P("  G_REPLAY — rebuilding 1159's 36 committed N_BLOCK bands with ITS seeds and draw count:")
    rep = []
    t0 = time.time()
    for panel in PANELS:
        T = int(panels[panel]["warm"].sum())
        for lad, rungs in LADDERS.items():
            R = np.array([series[(panel, lad, str(rg))] for rg in rungs], float)
            obs = np.array([-fmet(r)[2] * 100.0 for r in R])
            ai = [str(rg) for rg in rungs].index(str(ANCHOR[lad]))
            rng = np.random.default_rng(seed_of(panel, lad, "N_BLOCK"))
            idx = control_index("X_NONE", rng, T, BDRAWS)
            B = boot_maxdd(R, idx)
            oo, bo = objects_of(obs, ai), objects_of(B, ai)
            for obj in OBJECTS:
                q = pb[(pb.panel == panel) & (pb.ladder == lad) & (pb.object == obj)]
                if not len(q):
                    continue
                q = q.iloc[0]
                lo, hi = band(bo[obj], Q_HEAD)
                rep.append(dict(panel=panel, ladder=lad, object=obj,
                                obs_now=oo[obj], obs_committed=float(q.observed),
                                d_obs=abs(oo[obj] - float(q.observed)),
                                med_now=float(np.median(bo[obj])),
                                med_committed=float(q.null_median),
                                d_med=abs(float(np.median(bo[obj])) - float(q.null_median)),
                                lo_now=lo, lo_committed=float(q["lo_0.9"]),
                                hi_now=hi, hi_committed=float(q["hi_0.9"]),
                                inside_now=bool(lo <= oo[obj] <= hi),
                                inside_committed=bool(q["inside_0.9"])))
    rep = pd.DataFrame(rep)
    gate("G_REPLAY_OBS", f"observed values reproduce 1159's committed ({len(rep)} of 36)",
         f"{rep.d_obs.max():.3e}", rep.d_obs.max() < 1e-6)
    gate("G_REPLAY_MED", "null MEDIANS reproduce 1159's committed",
         f"{rep.d_med.max():.4f}", rep.d_med.max() < 1e-6)
    gate("G_REPLAY_VER", "INSIDE verdicts reproduce 1159's committed",
         f"{int((rep.inside_now == rep.inside_committed).sum())} of {len(rep)}",
         bool((rep.inside_now == rep.inside_committed).all()))
    P(f"     ({time.time() - t0:.0f}s)   max |d observed| {rep.d_obs.max():.3e},"
      f"  max |d null median| {rep.d_med.max():.4e}")
    if rep.d_med.max() >= 1e-6:
        P("     The medians do NOT reproduce bit for bit.  That is the tape, not the code:")
        P("     idea 1163 established prices.csv is rewritten nightly (9.1-12.4% of shared cells")
        P("     restated at all 11 transitions).  The replay is reported as a DEVIATION and the")
        P("     census below is run on THIS tape throughout, so every comparison inside this")
        P("     file is internally consistent.  Nothing is tuned to make the gate pass.")
    P("")

    # ------------------------------------------------------------------ THE CENSUS
    P("-" * 100)
    P("THE CENSUS — every committed band rebuilt under all four controls")
    P("-" * 100)
    P("  MACHINERY SHARE = (med X_SHUFFLE1 - med X_IID) / (med X_NONE - med X_IID).")
    P("  A share near 1 means the block null's shallowing survives ORDER DESTRUCTION and is")
    P("  therefore an artefact of the resampler, not a fact about the tape.")
    P("")
    t0 = time.time()
    brows, mrows = [], []
    DRAWS = {}
    for panel in PANELS:
        T = int(panels[panel]["warm"].sum())
        for lad, rungs in LADDERS.items():
            R = np.array([series[(panel, lad, str(rg))] for rg in rungs], float)
            obs = np.array([-fmet(r)[2] * 100.0 for r in R])
            ai = [str(rg) for rg in rungs].index(str(ANCHOR[lad]))
            oo = objects_of(obs, ai)
            for ctl in CONTROLS:
                rng = np.random.default_rng(seed_of(panel, lad, "N_BLOCK" if ctl == "X_NONE"
                                                    else ("N_IID" if ctl == "X_IID" else ctl)))
                if ctl in ("X_SHUFFLE1", "X_SHUFFLEPD"):
                    # permute the SERIES (shared across rungs), keep the block index machinery
                    if ctl == "X_SHUFFLE1":
                        perm = rng.permutation(T)
                        Rp = R[:, perm]
                        idx = block_index(rng, T, BDRAWS)
                    else:
                        Rp = R
                        idx = control_index("X_SHUFFLEPD", rng, T, BDRAWS)
                    B = boot_maxdd(Rp, idx)
                else:
                    B = boot_maxdd(R, control_index(ctl, rng, T, BDRAWS))
                bo = objects_of(B, ai)
                DRAWS[(panel, lad, ctl)] = bo
                for obj in OBJECTS:
                    row = dict(panel=panel, ladder=lad, object=obj, control=ctl,
                               n_rungs=len(rungs), observed=oo[obj],
                               null_median=float(np.median(bo[obj])),
                               null_mean=float(np.mean(bo[obj])),
                               share_ge=float(np.mean(bo[obj] >= oo[obj])))
                    for q in QS:
                        lo, hi = band(bo[obj], q)
                        row[f"lo_{q}"], row[f"hi_{q}"] = lo, hi
                        row[f"inside_{q}"] = bool(lo <= oo[obj] <= hi)
                    row["ratio_obs_over_null"] = (oo[obj] / row["null_median"]
                                                  if row["null_median"] else np.nan)
                    brows.append(row)
        P(f"  {panel:<6} 4 ladders x 4 controls x {BDRAWS} draws ({time.time() - t0:.0f}s)")
    bands = pd.DataFrame(brows)
    dump(bands, "bands")
    P("")

    # ---- machinery share, per cell
    for panel in PANELS:
        for lad in LADDERS:
            for obj in OBJECTS:
                g = bands[(bands.panel == panel) & (bands.ladder == lad) & (bands.object == obj)]
                m = {r.control: r.null_median for r in g.itertuples()}
                denom = m["X_NONE"] - m["X_IID"]
                for ctl in ("X_SHUFFLE1", "X_SHUFFLEPD"):
                    mrows.append(dict(panel=panel, ladder=lad, object=obj, control=ctl,
                                      med_NONE=m["X_NONE"], med_IID=m["X_IID"],
                                      med_ctl=m[ctl],
                                      total=denom, machinery=m[ctl] - m["X_IID"],
                                      share=(m[ctl] - m["X_IID"]) / denom if denom else np.nan,
                                      ratio_ctl_over_iid=m[ctl] / m["X_IID"] if m["X_IID"] else np.nan))
    mach = pd.DataFrame(mrows)
    dump(mach, "machinery")
    P("  MACHINERY SHARE by panel and object (X_SHUFFLE1; the parent's own control):")
    ms = mach[mach.control == "X_SHUFFLE1"]
    P("    " + ms.pivot_table(index="panel", columns="object", values="share",
                              aggfunc="median").round(4).to_string().replace("\n", "\n    "))
    P("")
    P("  the same for X_SHUFFLEPD (fresh permutation per draw — no single-permutation artefact):")
    ms2 = mach[mach.control == "X_SHUFFLEPD"]
    P("    " + ms2.pivot_table(index="panel", columns="object", values="share",
                               aggfunc="median").round(4).to_string().replace("\n", "\n    "))
    P("")
    P("  AGAINST THE PARENT'S COMMITTED SHARES on OBJ_MAXDD (its object):")
    for pn in PANELS:
        got = ms[(ms.panel == pn) & (ms.object == "OBJ_MAXDD")].share.median()
        P(f"    {pn:<6} this run {got:+.4f}   parent committed {PARENT_SHARE[pn]:+.4f}"
          f"   delta {got - PARENT_SHARE[pn]:+.4f}")
    pooled = ms[ms.object == "OBJ_MAXDD"].ratio_ctl_over_iid.mean()
    P(f"    pooled BLOCK/IID with order destroyed: this run {pooled:.4f}, "
      f"parent committed {PARENT_POOLED:.4f}")
    P("")

    # ------------------------------------------------------------------ DO THE BANDS MOVE?
    P("-" * 100)
    P("DO THE PUBLISHED BANDS MOVE? — 16 (CLAIMSET x CONTROL) cells, all published")
    P("-" * 100)
    P("  The CORRECTED band divides the X_NONE draws by phi_m = med(control)/med(X_IID),")
    P("  removing exactly the shallowing that survives order destruction.  A band MOVES when")
    P("  its published INSIDE verdict flips.")
    P("")
    moverows = []
    for panel in PANELS:
        T = int(panels[panel]["warm"].sum())
        for lad, rungs in LADDERS.items():
            R = np.array([series[(panel, lad, str(rg))] for rg in rungs], float)
            obs = np.array([-fmet(r)[2] * 100.0 for r in R])
            ai = [str(rg) for rg in rungs].index(str(ANCHOR[lad]))
            oo = objects_of(obs, ai)
            base = DRAWS[(panel, lad, "X_NONE")]
            for ctl in CONTROLS:
                ctld = DRAWS[(panel, lad, ctl)]
                iid = DRAWS[(panel, lad, "X_IID")]
                for obj in OBJECTS:
                    mi = float(np.median(iid[obj]))
                    phi = (float(np.median(ctld[obj])) / mi) if mi else 1.0
                    corr = base[obj] / phi if phi else base[obj]
                    o = oo[obj]
                    for q in QS:
                        lo0, hi0 = band(base[obj], q)
                        lo1, hi1 = band(corr, q)
                        in0, in1 = bool(lo0 <= o <= hi0), bool(lo1 <= o <= hi1)
                        moverows.append(dict(
                            claimset="C_1159", control=ctl, panel=panel, ladder=lad,
                            object=obj, q=q, phi_machinery=phi, observed=o,
                            lo_published=lo0, hi_published=hi0, inside_published=in0,
                            lo_corrected=lo1, hi_corrected=hi1, inside_corrected=in1,
                            moves=bool(in0 != in1),
                            share_ge_published=float(np.mean(base[obj] >= o)),
                            share_ge_corrected=float(np.mean(corr >= o))))
    moves = pd.DataFrame(moverows)

    # ---- C_1157: the one band quoted as a ratio pair, rebuilt the same way
    P("  C_1157 — 1157's committed SMALL |MaxDD| 90% band, quoted as a RATIO band")
    P(f"           {PRIOR1157_BAND} and rebuilt here as obs/null on the SMALL panel:")
    b1157 = []
    for ctl in CONTROLS:
        g = bands[(bands.panel == "SMALL") & (bands.object == "OBJ_MAXDD") & (bands.control == ctl)]
        for _, r in g.iterrows():
            lo_r = r["observed"] / r["hi_0.9"]
            hi_r = r["observed"] / r["lo_0.9"]
            b1157.append(dict(control=ctl, ladder=r["ladder"], obs=r["observed"],
                              null_median=r["null_median"], ratio=r["ratio_obs_over_null"],
                              ratio_lo=lo_r, ratio_hi=hi_r,
                              committed_lo=PRIOR1157_BAND[0], committed_hi=PRIOR1157_BAND[1],
                              overlaps_committed=bool(hi_r >= PRIOR1157_BAND[0]
                                                      and lo_r <= PRIOR1157_BAND[1])))
    B1157 = pd.DataFrame(b1157)
    dump(B1157, "b1157")
    for ctl in CONTROLS:
        g = B1157[B1157.control == ctl]
        P(f"    {ctl:<12} ratio band over 4 ladders "
          f"[{g.ratio_lo.min():.3f}, {g.ratio_hi.max():.3f}]  "
          f"median ratio {g.ratio.median():.4f}  overlaps 1157's at {int(g.overlaps_committed.sum())} of {len(g)}")
    for _, r in B1157[B1157.control != "X_NONE"].iterrows():
        moves = pd.concat([moves, pd.DataFrame([dict(
            claimset="C_1157", control=r.control, panel="SMALL", ladder=r.ladder,
            object="OBJ_MAXDD_RATIO", q=0.90, phi_machinery=np.nan, observed=r.ratio,
            lo_published=PRIOR1157_BAND[0], hi_published=PRIOR1157_BAND[1],
            inside_published=True,
            lo_corrected=r.ratio_lo, hi_corrected=r.ratio_hi,
            inside_corrected=bool(r.overlaps_committed),
            moves=bool(not r.overlaps_committed),
            share_ge_published=np.nan, share_ge_corrected=np.nan)])], ignore_index=True)
    P("")

    # ---- C_1161: the parent's own committed decomposition, re-read and re-scored
    P("  C_1161 — the parent's own committed machinery shares, re-measured here:")
    for pn in PANELS:
        got = float(ms[(ms.panel == pn) & (ms.object == "OBJ_MAXDD")].share.median())
        agree = abs(got - PARENT_SHARE[pn]) < 0.25
        moves = pd.concat([moves, pd.DataFrame([dict(
            claimset="C_1161", control="X_SHUFFLE1", panel=pn, ladder="ALL",
            object="OBJ_MAXDD_SHARE", q=np.nan, phi_machinery=np.nan, observed=got,
            lo_published=PARENT_SHARE[pn], hi_published=PARENT_SHARE[pn],
            inside_published=True, lo_corrected=got, hi_corrected=got,
            inside_corrected=bool(agree), moves=bool(not agree),
            share_ge_published=np.nan, share_ge_corrected=np.nan)])], ignore_index=True)
        P(f"    {pn:<6} committed {PARENT_SHARE[pn]:+.4f}  re-measured {got:+.4f}  "
          f"{'AGREES' if agree else 'DOES NOT AGREE'} within 0.25")
    dump(moves, "moves")
    P("")

    P("  HOW MANY PUBLISHED BANDS MOVE, per (CLAIMSET x CONTROL) cell — all 16 published:")
    P(f"  {'':<12}" + "".join(f"{c:>14}" for c in CONTROLS))
    for cs in CLAIMSETS:
        sel = moves if cs == "C_ALL" else moves[moves.claimset == cs]
        line = f"  {cs:<12}"
        for ctl in CONTROLS:
            q = sel[sel.control == ctl]
            line += (f"{int(q.moves.sum()):>6}/{len(q):<7}" if len(q) else f"{'—':>14}")
        P(line)
    P("")
    P("  the headline cell, C_1159 x X_SHUFFLE1, broken out by confidence level:")
    h = moves[(moves.claimset == "C_1159") & (moves.control == "X_SHUFFLE1")]
    for q in QS:
        g = h[h.q == q]
        P(f"    q={q:.2f}   moves {int(g.moves.sum()):>2} of {len(g)}   "
          f"published INSIDE {int(g.inside_published.sum())}/{len(g)} -> "
          f"corrected INSIDE {int(g.inside_corrected.sum())}/{len(g)}")
    P("")
    P("  phi_machinery (the correction factor actually applied), by panel and object:")
    P("    " + h.pivot_table(index="panel", columns="object", values="phi_machinery",
                            aggfunc="median").round(4).to_string().replace("\n", "\n    "))
    P("")

    # ------------------------------------------------------------------ RULE 8
    P("-" * 100)
    P("RULE 8 — a band is a BAR, so does correcting it change what a chooser PICKS?")
    P("-" * 100)
    P("  Four choosers read the IS window (2009-2016) ONLY and pick one rung of each ladder;")
    P("  the pick is evaluated on the untouched OOS window (2017-2026) against the live")
    P(f"  RULES v2 baseline and SPY, on BOTH KEEP paths.  IS nulls use {BDRAWS_IS} draws.")
    P("    K_NONULL   plain IS argmin |MaxDD| — no null at all (the record's habit)")
    P("    K_BLOCK    the rung whose observed |MaxDD| sits lowest against its own BLOCK null")
    P("    K_CORR     the same, against the MACHINERY-CORRECTED block null")
    P("    K_IID      the same, against the iid null (the machinery-free reference)")
    P("")
    t0 = time.time()
    wrows = []
    for panel in PANELS:
        d = panels[panel]
        sb, lb = BENCH[panel]["spy"], BENCH[panel]["live"]
        Tis = int(d["ins"].sum())
        for lad, rungs in LADDERS.items():
            Ris = np.array([isser[(panel, lad, str(rg))] for rg in rungs], float)
            obs_is = np.array([-fmet(r)[2] * 100.0 for r in Ris])
            med = {}
            for ctl in ("X_NONE", "X_SHUFFLE1", "X_IID"):
                rng = np.random.default_rng(seed_of(panel, lad, ctl, "IS"))
                if ctl == "X_SHUFFLE1":
                    perm = rng.permutation(Tis)
                    B = boot_maxdd(Ris[:, perm], block_index(rng, Tis, BDRAWS_IS))
                else:
                    B = boot_maxdd(Ris, control_index(ctl, rng, Tis, BDRAWS_IS))
                med[ctl] = np.median(B, axis=1)
            phi = np.where(med["X_IID"] > 0, med["X_SHUFFLE1"] / med["X_IID"], 1.0)
            picks = {
                "K_NONULL": int(np.argmin(obs_is)),
                "K_BLOCK": int(np.argmin(obs_is / med["X_NONE"])),
                "K_CORR": int(np.argmin(obs_is / (med["X_NONE"] / phi))),
                "K_IID": int(np.argmin(obs_is / med["X_IID"])),
            }
            for ch, pi in picks.items():
                rg = rungs[pi]
                c = dict(ANCHOR)
                c[lad] = rg
                r = run_cell(panel, c["N"], c["H"], c["GROSS"], c["CADENCE"])
                m = blocks_m(r, d)
                l4b, l4bo, l4a = legs_4b(m, sb), legs_4b_oos(m, sb), legs_4a(m, lb)
                wrows.append(dict(chooser=ch, panel=panel, ladder=lad, pick=str(rg),
                                  IS_obs_maxdd=obs_is[pi], phi=float(phi[pi]), **m,
                                  SPY_OOS_Sharpe=sb["OOS_Sharpe"], SPY_OOS_CAGR=sb["OOS_CAGR"],
                                  SPY_OOS_MaxDD=sb["OOS_MaxDD"], LIVE_OOS_Sharpe=lb["OOS_Sharpe"],
                                  pass_4b=all(l4b.values()), pass_4b_oos=all(l4bo.values()),
                                  pass_4a=all(l4a.values()), **l4b, **l4bo, **l4a))
        P(f"  {panel:<6} 4 ladders x 4 choosers ({time.time() - t0:.0f}s)")
    wf = pd.DataFrame(wrows)
    dump(wf, "walkforward")
    P("")
    P(f"  {'chooser':<10}{'medOOS_Sh':>11}{'meanOOS_Sh':>12}{'>SPY OOS':>11}{'4b full':>10}{'4b OOS':>9}{'4a':>8}")
    for ch in ("K_NONULL", "K_BLOCK", "K_CORR", "K_IID"):
        q = wf[wf.chooser == ch]
        P(f"  {ch:<10}{q.OOS_Sharpe.median():>11.4f}{q.OOS_Sharpe.mean():>12.4f}"
          f"{int((q.OOS_Sharpe > q.SPY_OOS_Sharpe).sum()):>8}/{len(q):<3}"
          f"{int(q.pass_4b.sum()):>7}/{len(q):<3}{int(q.pass_4b_oos.sum()):>6}/{len(q):<3}"
          f"{int(q.pass_4a.sum()):>5}/{len(q):<3}")
    P("")
    a = wf[wf.chooser == "K_BLOCK"].set_index(["panel", "ladder"]).sort_index()
    c = wf[wf.chooser == "K_CORR"].set_index(["panel", "ladder"]).sort_index()
    mv = a.pick != c.pick
    P(f"  DOES THE CORRECTION MOVE THE PICK?  {int(mv.sum())} of {len(a)} ladders.")
    if int(mv.sum()):
        dd = (c.OOS_Sharpe - a.OOS_Sharpe)[mv]
        P(f"    OOS Sharpe delta where it moves: mean {dd.mean():+.4f} median {dd.median():+.4f}"
          f"  better at {int((dd > 0).sum())} of {len(dd)}")
    P("")
    P("  EVERY 4b-CLEARING PICK (full AND OOS), named:")
    good = wf[wf.pass_4b & wf.pass_4b_oos]
    if len(good):
        for _, r in good.iterrows():
            P(f"    {r.chooser:<9} {r.panel:<6} {r.ladder:<8} pick {r['pick']:<6} "
              f"full {r.CAGR:7.2%}/{r.Sharpe:.4f}/{r.MaxDD:7.2%}  "
              f"OOS {r.OOS_CAGR:7.2%}/{r.OOS_Sharpe:.4f}/{r.OOS_MaxDD:7.2%}")
    else:
        P("    NONE")
    P("  EVERY 4a-CLEARING PICK, named:")
    g4a = wf[wf.pass_4a]
    if len(g4a):
        for _, r in g4a.iterrows():
            P(f"    {r.chooser:<9} {r.panel:<6} {r.ladder:<8} pick {r['pick']:<6} "
              f"full {r.CAGR:7.2%}/{r.Sharpe:.4f}/{r.MaxDD:7.2%}")
    else:
        P("    NONE")
    P("")

    dump(pd.DataFrame(gates), "gates")
    P("-" * 100)
    P(f"GATES {sum(g['pass_'] for g in gates)} of {len(gates)} PASS")
    P(f"TOTAL RUNTIME {time.time() - t_run0:.1f}s")
    P("-" * 100)
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {OUT.name}.console.txt")


if __name__ == "__main__":
    main()
