#!/usr/bin/env python3
"""IDEA 1250 (lane cloud, 2026-09-18) — is the L NEIGHBOURHOOD of 63 WIDE ENOUGH to make every
committed L-KEYED claim SAFE?

THE QUESTION.  1242 measured each resample output's L swing against its own 8-seed noise and found
0 of 18 outputs separate between L = 42 and L = 126 while 8 of 18 separate between 21 and 252: the
record's frozen L = 63 is LOCALLY safe and only GLOBALLY fragile.  That was read off two rung PAIRS.
This run maps the neighbourhood DIRECTLY: on a 21-rung L ladder it finds, per output, the WIDEST
[L_lo, L_hi] around 63 inside which the swing never exceeds that output's own seed noise, and then
prices the clause the queue proposes — "an unstated L asserts the claim over a BAND, not at a POINT"
— against the record's own 141 unstated-L bar-side verdict units (1242's census, inherited whole).

TWO DIALS (rule 4), 12 cells, EVERY ONE PUBLISHED:
  dial 1 = NOISE MULTIPLE  {1.0, 1.5, 2.0, 3.0}   a rung is SAFE if its swing from L = 63 is at
           most m x that output's own mean 8-seed swing.  1242 declared 2.0 for its cell-3 bar;
           1.0 is the strictest reading of "inside its own noise" and 3.0 the loosest.
  dial 2 = OUTPUT SET      {OS_CORE (7), OS_WIDE (14), OS_ALL (18)}   1242's own three sets,
           inherited whole, never re-defined here.

WHAT IS NOT A DIAL.  The L ladder itself (it is the object under measurement, never selected on),
the 72 decisions (panel 3 x anchor 2 x ladder 4 x chooser 3), the 18 output definitions, B = 1000
draws, the 8 seed streams, and the ASSERTION BAND the clause is scored against, which is
pre-declared as BAND_REC = [21, 252] — 1242's LP_REC endpoints, i.e. the span of L the record has
actually published at.  BAND_NEAR = [42, 126] is reported beside it as a descriptive control.

EXECUTION (binding, rule 2): weights decided at the rebalance close t, applied at t+1; 10 bps per
unit turnover; no shorting, no leverage.  RULE 8: every band is measured on warm-up..2016-12-31 and
the chosen cell's band is then re-measured ONCE on 2017-2026 book returns, which no band ever saw.

Offline, deterministic, standalone.  Writes .outputs.csv .seedsweep.csv .bands.csv .grid.csv
.census.csv .walkforward.csv .capital.csv .books.csv .gates.csv .console.txt
"""
import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-18"
SLUG = "is-the-L-NEIGHBOURHOOD-of-63-WIDE-ENOUGH-to-make-every-committed-L-KEYED-claim-SAFE"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"
REF_1242 = (Path(__file__).resolve().parent /
            "2026-09-17_is-REACH-the-only-RESAMPLING-OUTPUT-in-the-record-that-is-L-FREE_B")

# ----- 1096/1101/1208/1242's construction, inherited whole --------------------------------------
LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]

LAD_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]
LAD_H = [21, 63, 126, 252]
LAD_G = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]
LAD_C = ["D", "W", "M", "Q"]
LADDERS = {"N": LAD_N, "H": LAD_H, "GROSS": LAD_G, "CADENCE": LAD_C}
LADNAMES = ["N", "H", "GROSS", "CADENCE"]
ANCHORS = {"A": dict(N=20, H=126, GROSS=0.75, CADENCE="W"),
           "B": dict(N=12, H=63, GROSS=0.55, CADENCE="M")}
PANELS = ["U56", "B136", "SMALL"]
CHOOSERS = ["CH_ISSHARPE", "CH_ISCAGR", "CH_ISDD"]

BAR_HI = 0.90
BDRAWS = 1000
SEED_BASE = 12081208                      # 1242/1208's base, so the shared rungs replay bit for bit
L_HEAD = 63
SEED_LADDER = [0, 1, 2, 3, 4, 5, 6, 7]
# the DENSE ladder: 1242's 11 numeric rungs (kept, so its rows can be gated) plus 10 new ones that
# fill the neighbourhood of 63.  Never selected on — this is the object under measurement.
L_1242 = [1, 2, 5, 10, 21, 42, 63, 126, 252, 504, 1008]
L_NEW = [16, 26, 32, 52, 79, 100, 160, 200, 378, 756]
L_NUM = sorted(set(L_1242 + L_NEW))
L_ALL = L_NUM + ["T"]

OUTPUTS = {
    "O_REACH": "OBS", "B_PPICK": "BAR", "B_Q95": "BAR", "B_NULLMED": "BAR", "B_RECRANGE": "BAR",
    "B_BOOT95": "BAR", "B_PCTRANK": "BAR",
    "B_PMAX": "BAR", "B_MODALRUNG": "BAR", "B_MODALMATCH": "BAR", "B_SD": "BAR",
    "B_GAPEXCEEDS": "BAR", "B_RESOLVED": "BAR", "B_Q05": "BAR",
    "O_PICK": "OBS", "O_MARGIN": "OBS", "O_LEVEL": "OBS", "O_GAPRATIO": "OBS",
}
OS_CORE = ["O_REACH", "B_PPICK", "B_Q95", "B_NULLMED", "B_RECRANGE", "B_BOOT95", "B_PCTRANK"]
OS_WIDE = OS_CORE + ["B_PMAX", "B_MODALRUNG", "B_MODALMATCH", "B_SD", "B_GAPEXCEEDS",
                     "B_RESOLVED", "B_Q05"]
OS_ALL = OS_WIDE + ["O_PICK", "O_MARGIN", "O_LEVEL", "O_GAPRATIO"]
OUTPUT_SETS = {"OS_CORE": OS_CORE, "OS_WIDE": OS_WIDE, "OS_ALL": OS_ALL}

# ----- THIS RUN'S DIALS -------------------------------------------------------------------------
NOISE_MULTS = [1.0, 1.5, 2.0, 3.0]
BAND_REC = (21, 252)        # pre-declared assertion band: 1242's LP_REC, the record's published span
BAND_NEAR = (42, 126)       # control, reported not selected on

# ----- committed numbers QUOTED and GATED, never re-derived -------------------------------------
C1242_UNITS_CORE = (1272, 1129, 158, 141)     # units / verdict / verdict+BAR / verdict+BAR+no L
C1242_UNITS_WIDE_NO_L = 700
C1208_REACH = 14
C1208_RATES = {21: 0.1944, 63: 0.2222, 252: 0.3194}
C1242_NEAR_LFREE = 18                          # 0 of 18 separate between 42 and 126
C1242_REC_LDEP = 8                             # 8 of 18 separate between 21 and 252
C1101_TRIPLE = (0.155787, 1.139701, -0.191276)
LIVE_MAXDD_COMMITTED = -0.1205
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
C1246_ANCHOR_OOS = 0.7922

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


GATES: list[dict] = []


def gate(name, what, value, ok):
    GATES.append(dict(gate=name, check=what, value=float(value), pass_=bool(ok)))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name:<8s} {what}  ->  {value:.4e}")
    return bool(ok)


# ================================================================================================
# the runner, metrics and book construction: 1101/1208/1242's, verbatim
# ================================================================================================
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


def windows_of(idx):
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


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep].dropna(how="all").ffill(), len(bad), len(meta)


class Panel:
    def __init__(self, name, px):
        self.name, self.px = name, px
        self.idx, self.K, self.T = px.index, len(px.columns), len(px.index)
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.warm, self.ins, self.oos = windows_of(px.index)
        sc, elig = mech(px)
        spy_i = list(px.columns).index("SPY")
        if name == "SMALL":
            elig = elig.copy()
            elig[:, spy_i] = False
        self.sc, self.elig = sc, elig
        self.reb, self.mkl = {}, {}
        for f in LAD_C:
            mk = rebalance_mask(px.index, f).values
            self.reb[f] = np.flatnonzero(mk)
            m = np.roll(mk, LAG)
            m[:LAG] = False
            self.mkl[f] = m
        self.spy = px["SPY"].pct_change().fillna(0.0).values


def book(pan, N, H, gross, freq):
    W = build(-pan.sc, pan.elig, pan.priced, pan.reb[freq], N, H, pan.T, pan.K, gross)
    Wl = np.zeros_like(W)
    Wl[LAG:] = W[:-LAG]
    r, turn = nrun(pan.rets, Wl, pan.mkl[freq])
    return r - turn * COST / 1e4


def ladder_books(pan, anchor, lad):
    a = ANCHORS[anchor]
    out = {}
    for rung in LADDERS[lad]:
        kw = dict(N=a["N"], H=a["H"], gross=a["GROSS"], freq=a["CADENCE"])
        kw[{"N": "N", "H": "H", "GROSS": "gross", "CADENCE": "freq"}[lad]] = rung
        out[rung] = book(pan, kw["N"], kw["H"], kw["gross"], kw["freq"])
    return out


# ----- 1208/1242's bootstrap and the 18 outputs, verbatim ---------------------------------------
def block_index(rng, T, L, B):
    L = int(min(max(L, 1), T))
    nb = int(np.ceil(T / L))
    starts = rng.integers(0, max(T - L, 1), size=(B, nb))
    off = np.arange(L)[None, None, :]
    idx = (starts[:, :, None] + off).reshape(B, nb * L)[:, :T]
    return np.minimum(idx, T - 1)


def draw_stats(R, stat, L, seed, B=BDRAWS, chunk=100):
    T, k = R.shape
    rng = np.random.default_rng(seed)
    parts, done = [], 0
    while done < B:
        b = min(chunk, B - done)
        idx = block_index(rng, T, L, b)
        X = R[idx]
        if stat == "CH_ISSHARPE":
            v = X.mean(axis=1) * 252.0 / (X.std(axis=1, ddof=1) * np.sqrt(252.0))
        elif stat == "CH_ISCAGR":
            eq = np.cumprod(1.0 + X, axis=1)
            v = eq[:, -1, :] ** (252.0 / T) - 1.0
        elif stat == "CH_ISDD":
            eq = np.cumprod(1.0 + X, axis=1)
            v = (eq / np.maximum.accumulate(eq, axis=1) - 1.0).min(axis=1)
        else:
            raise ValueError(stat)
        parts.append(np.where(np.isfinite(v), v, -np.inf))
        done += b
    return np.vstack(parts)


def is_stat_win(r, win, stat):
    x = r[win]
    n = len(x)
    if stat == "CH_ISSHARPE":
        return fsharpe(x)
    if stat == "CH_ISCAGR":
        eq = np.cumprod(1.0 + x)
        return eq[-1] ** (252.0 / n) - 1.0
    if stat == "CH_ISDD":
        eq = np.cumprod(1.0 + x)
        return float((eq / np.maximum.accumulate(eq) - 1.0).min())
    raise ValueError(stat)


def observed_outputs(obs, rungs, anchor_rung):
    j = int(np.nanargmax(obs))
    sd = np.sort(obs)[::-1]
    margin = float(sd[0] - sd[1]) if len(sd) > 1 else np.nan
    spread = float(sd[0] - sd[-1]) if len(sd) > 1 else np.nan
    return j, dict(O_PICK=float(j), O_REACH=float(rungs[j] == anchor_rung), O_MARGIN=margin,
                   O_LEVEL=float(obs[j]),
                   O_GAPRATIO=float(margin / spread) if spread and np.isfinite(spread) and spread > 0 else np.nan)


def bar_outputs(D, obs, j):
    am = D.argmax(axis=1)
    Pv = np.bincount(am, minlength=D.shape[1]) / D.shape[0]
    col = D[:, j]
    colf = col[np.isfinite(col)]
    if colf.size == 0:
        colf = np.array([np.nan])
    srt = np.sort(D, axis=1)[:, ::-1]
    gaps = srt[:, 0] - srt[:, 1] if D.shape[1] > 1 else np.zeros(D.shape[0])
    gaps = gaps[np.isfinite(gaps)] if np.isfinite(gaps).any() else np.array([np.nan])
    rec = colf - colf.mean()
    obs_margin = float(np.sort(obs)[::-1][0] - np.sort(obs)[::-1][1]) if len(obs) > 1 else np.nan
    b95 = float(np.percentile(gaps, 95))
    return dict(B_PPICK=float(Pv[j]), B_PMAX=float(Pv.max()), B_MODALRUNG=float(int(Pv.argmax())),
                B_MODALMATCH=float(int(Pv.argmax()) == j), B_Q95=float(np.percentile(colf, 95)),
                B_Q05=float(np.percentile(colf, 5)), B_NULLMED=float(np.median(colf)),
                B_RECRANGE=float(np.percentile(rec, 95) - np.percentile(rec, 5)),
                B_SD=float(colf.std(ddof=1) if colf.size > 1 else np.nan),
                B_PCTRANK=float((colf <= obs[j]).mean()), B_BOOT95=b95,
                B_GAPEXCEEDS=float(obs_margin > b95), B_RESOLVED=float(Pv[j] >= BAR_HI))


def widest_band(rungs, safe, centre=L_HEAD):
    """The widest contiguous rung interval containing `centre` on which `safe` holds everywhere."""
    i = rungs.index(centre)
    if not safe[i]:
        return (centre, centre, 1, False)
    lo = i
    while lo - 1 >= 0 and safe[lo - 1]:
        lo -= 1
    hi = i
    while hi + 1 < len(rungs) and safe[hi + 1]:
        hi += 1
    return (rungs[lo], rungs[hi], hi - lo + 1, True)


# ================================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P(f"IDEA 1250 (lane cloud, {DATE}) — is the L NEIGHBOURHOOD of 63 WIDE ENOUGH to make every")
    P("                                 committed L-KEYED claim SAFE?")
    P("=" * 100)
    P("  dial 1 = NOISE MULTIPLE {1.0, 1.5, 2.0, 3.0}   (1242 declared 2.0 for its cell-3 bar)")
    P("  dial 2 = OUTPUT SET     {OS_CORE 7, OS_WIDE 14, OS_ALL 18}   -> 12 cells, ALL PUBLISHED")
    P(f"  L ladder (measured, never selected on): {L_NUM} + T   ({len(L_ALL)} rungs)")
    P("  NOT dials: the 72 decisions, the 18 output definitions, B = 1000, the 8 seed streams, and")
    P(f"  the pre-declared assertion band BAND_REC = {BAND_REC} (1242's LP_REC, the record's own span).")
    P("")
    P("-" * 100)
    P("ARM 0 — WHAT IS DECLARED BEFORE THE TAPE IS TOUCHED")
    P("-" * 100)
    P("  1242 read the neighbourhood off two PAIRS: 0 of 18 outputs separate at (42, 126), 8 of 18")
    P("  separate at (21, 252).  A pair says nothing about where between 126 and 252 safety ends.")
    P("  Pre-declared outcomes:")
    P("    (A) THE NEIGHBOURHOOD IS WIDE ENOUGH — at the declared multiple 2.0 every OS_CORE bar")
    P("        output's band covers BAND_REC, so a neighbourhood clause resolves all 141 units.")
    P("    (B) THE NEIGHBOURHOOD IS REAL BUT NARROWER THAN THE RECORD'S SPAN — bands are wide")
    P("        around 63 but do not reach 21 or 252, so the clause resolves some units and the")
    P("        rest still need their L stated.")
    P("    (C) THERE IS NO NEIGHBOURHOOD — some bar output moves beyond its own noise at a rung")
    P("        adjacent to 63, and the point value is all the record ever had.")
    P("  H_BAND    : at m = 2.0 every OS_CORE bar output has a band strictly wider than {63}.")
    P("  H_COVER   : at m = 2.0 the OS_CORE intersected band covers BAND_REC = (21, 252).")
    P("  H_RESOLVE : a neighbourhood clause at m = 2.0 resolves a MAJORITY of the 141 units.")
    P("  H_TRANSFER: the IS band of the rule-8 chosen cell still holds on 2017-2026, read once.")
    P("  H_CAPITAL : moving L inside the band changes no book choice and no 4b verdict.")
    P("")

    # ---------------------------------------------------------------------------- panels & books
    P("-" * 100)
    P("ARM 1 — PANELS, BENCHMARKS AND THE 162 RUNG BOOKS")
    P("-" * 100)
    u = load_universe()
    b = load_universe(broad=True)
    s, n_bad, n_meta = load_small()
    PAN = {}
    for nm, px in (("U56", u), ("B136", b), ("SMALL", s)):
        PAN[nm] = Panel(nm, px)
        pan = PAN[nm]
        P(f"  {nm:<6s} {px.shape[1]:>4d} cols x {px.shape[0]:>5d} rows  {px.index[0].date()} .. "
          f"{px.index[-1].date()}  IS {pan.ins.sum():>5d}  OOS {pan.oos.sum():>5d}")
    P(f"  SMALL exclusion: {n_bad} of {n_meta} names dropped on max_1d_move >= 1.0 (documented).")
    BM = {}
    for nm, pan in PAN.items():
        spy = blocks_m(pan.spy, pan.warm, pan.ins, pan.oos)
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live = blocks_m(lr, pan.warm, pan.ins, pan.oos)
        BM[nm] = dict(spy=spy, live=live)
        P(f"  {nm:<6s} SPY     full {spy['CAGR']:>7.2%} / {spy['Sharpe']:.4f} / {spy['MaxDD']:>7.2%}"
          f"  halves {spy['H1']:.4f}/{spy['H2']:.4f}  OOS {spy['OOS_CAGR']:>7.2%} / {spy['OOS_Sharpe']:.4f}")
        P(f"  {nm:<6s} LIVE v2 full {live['CAGR']:>7.2%} / {live['Sharpe']:.4f} / {live['MaxDD']:>7.2%}"
          f"  halves {live['H1']:.4f}/{live['H2']:.4f}  OOS {live['OOS_CAGR']:>7.2%} / {live['OOS_Sharpe']:.4f}")
    RB, brows = {}, []
    for pnm in PANELS:
        pan = PAN[pnm]
        for anc in ANCHORS:
            for lad in LADNAMES:
                bks = ladder_books(pan, anc, lad)
                RB[(pnm, anc, lad)] = bks
                a = ANCHORS[anc]
                for rung, r in bks.items():
                    m = blocks_m(r, pan.warm, pan.ins, pan.oos)
                    kw = dict(N=a["N"], H=a["H"], GROSS=a["GROSS"], CADENCE=a["CADENCE"])
                    kw[lad] = rung
                    row = dict(panel=pnm, anchor=anc, ladder=lad, rung=rung, **kw, **m)
                    row.update(legs_4b(m, BM[pnm]["spy"]))
                    row.update(legs_4b_oos(m, BM[pnm]["spy"]))
                    row.update(legs_4a(m, BM[pnm]["live"]))
                    row["pass_4b_full"] = all(row[k] for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                    row["pass_4b_oos"] = all(row[k] for k in ("O_S", "O_DD", "O_CAGR"))
                    row["pass_4a"] = all(row[k] for k in ("A_H1", "A_H2", "A_DD"))
                    brows.append(row)
    books = pd.DataFrame(brows)
    dump(books, "books")
    P(f"  built {len(books)} rung books;  4a {int(books.pass_4a.sum())};  4b full "
      f"{int(books.pass_4b_full.sum())};  4b OOS {int(books.pass_4b_oos.sum())};  "
      f"BOTH {int((books.pass_4b_full & books.pass_4b_oos).sum())}")
    inc = books[(books.panel == "U56") & (books.anchor == "A") & (books.ladder == "N") & (books.rung == 20)].iloc[0]
    e1 = max(abs(inc.CAGR - C1101_TRIPLE[0]), abs(inc.Sharpe - C1101_TRIPLE[1]), abs(inc.MaxDD - C1101_TRIPLE[2]))
    gate("G1", "incumbent U56/A/N=20 triple vs 1101's committed", e1, e1 < 5e-3)
    e2 = abs(BM["U56"]["live"]["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gate("G2", "U56 live RULES v2 MaxDD vs committed -12.05%", e2, e2 < 5e-3)
    e3 = max(abs(BM["U56"]["spy"]["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
             abs(BM["U56"]["spy"]["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(BM["U56"]["spy"]["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gate("G3", "U56 SPY OOS triple vs committed", e3, e3 < 5e-3)
    ov = sum(int((PAN[p].ins & PAN[p].oos).sum()) for p in PANELS)
    gate("G4", "IS n OOS rows (must be 0)", ov, ov == 0)
    pan = PAN["U56"]
    W = build(-pan.sc, pan.elig, pan.priced, pan.reb["W"], 20, 126, pan.T, pan.K, 0.75)
    eng = backtest(pan.px, pd.DataFrame(W, index=pan.idx, columns=pan.px.columns), cost_bps=COST, freq="W")["returns"].values
    e5 = float(np.abs(eng[WARMUP:] - RB[("U56", "A", "N")][20][WARMUP:]).max())
    gate("G5", "fast runner == engine.backtest (U56 A N=20)", e5, e5 < 1e-9)

    # ------------------------------------------------- ARM 2: every output at every rung (IS)
    P("")
    P("-" * 100)
    P(f"ARM 2 — EVERY OUTPUT AT EVERY ONE OF {len(L_ALL)} L RUNGS, ON 1208/1242's SAME 72 DECISIONS")
    P("-" * 100)
    DEC = [(pn, an, lad, ch) for pn in PANELS for an in ANCHORS for lad in LADNAMES for ch in CHOOSERS]
    pre = {}
    for (pn, an, lad, ch) in DEC:
        pan = PAN[pn]
        rungs = LADDERS[lad]
        R = np.column_stack([RB[(pn, an, lad)][rg][pan.ins] for rg in rungs])
        Ro = np.column_stack([RB[(pn, an, lad)][rg][pan.oos] for rg in rungs])
        obs = np.array([is_stat_win(RB[(pn, an, lad)][rg], pan.ins, ch) for rg in rungs])
        obso = np.array([is_stat_win(RB[(pn, an, lad)][rg], pan.oos, ch) for rg in rungs])
        j, oout = observed_outputs(obs, rungs, ANCHORS[an][lad])
        jo, oouto = observed_outputs(obso, rungs, ANCHORS[an][lad])
        pre[(pn, an, lad, ch)] = dict(R=R, obs=obs, j=j, oout=oout, rungs=rungs,
                                      Ro=Ro, obso=obso, jo=jo, oouto=oouto)
    rows = []
    for (pn, an, lad, ch) in DEC:
        d = pre[(pn, an, lad, ch)]
        for L in L_ALL:
            Lv = d["R"].shape[0] if L == "T" else int(L)
            D = draw_stats(d["R"], ch, Lv, seed_of(pn, an, lad, ch, L))
            rows.append(dict(panel=pn, anchor=an, ladder=lad, chooser=ch, k=len(d["rungs"]),
                             L=("T" if L == "T" else L), L_eff=Lv, pick=str(d["rungs"][d["j"]]),
                             **d["oout"], **bar_outputs(D, d["obs"], d["j"])))
    odf = pd.DataFrame(rows)
    dump(odf, "outputs")
    P(f"  {len(odf):,} rows = 72 decisions x {len(L_ALL)} rungs  ({time.time() - t0:.0f}s)")

    # replay 1242's committed artefact on the 12 shared rungs, row by row
    ref_p = Path(f"{REF_1242}.outputs.csv")
    if ref_p.exists():
        ref = pd.read_csv(ref_p)
        ref["L"] = ref.L.astype(str)
        mine = odf.copy()
        mine["L"] = mine.L.astype(str)
        mg = ref.merge(mine, on=["panel", "anchor", "ladder", "chooser", "L"], suffixes=("_r", "_m"))
        cols = [c for c in OUTPUTS if f"{c}_r" in mg.columns]
        dev = max(float(np.nanmax(np.abs(mg[f"{c}_r"] - mg[f"{c}_m"]))) for c in cols)
        gate("G6", f"all {len(cols)} outputs replay 1242's committed rows bit for bit "
                   f"({len(mg)} of {len(ref)} rows)", dev, dev == 0.0 and len(mg) == len(ref))
    else:
        gate("G6", "1242's committed outputs.csv present for the row-by-row replay", 1.0, False)
    reach_by_L = odf.groupby("L", sort=False).O_REACH.sum()
    gate("G7", f"reach = {C1208_REACH} of 72 at EVERY rung incl. the 10 NEW ones",
         float(np.abs(reach_by_L - C1208_REACH).max()), bool((reach_by_L == C1208_REACH).all()))
    rate_by_L = odf.groupby("L", sort=False).B_RESOLVED.mean()
    dev_rates = max(abs(float(rate_by_L.loc[L]) - v) for L, v in C1208_RATES.items())
    gate("G8", "1208's resolution rates at L = 21 / 63 / 252 replay", dev_rates, dev_rates < 1e-6)

    # --------------------------------------------------------- ARM 3: the seed noise yardstick
    P("")
    P("-" * 100)
    P(f"ARM 3 — THE NOISE YARDSTICK: every output at L = {L_HEAD} on {len(SEED_LADDER)} rng streams")
    P("-" * 100)
    srows = []
    for (pn, an, lad, ch) in DEC:
        d = pre[(pn, an, lad, ch)]
        for sd in SEED_LADDER:
            D = draw_stats(d["R"], ch, L_HEAD, seed_of("SEED", sd, pn, an, lad, ch))
            srows.append(dict(panel=pn, anchor=an, ladder=lad, chooser=ch, seed=sd,
                              **d["oout"], **bar_outputs(D, d["obs"], d["j"])))
    sdf = pd.DataFrame(srows)
    dump(sdf, "seedsweep")
    KEY = ["panel", "anchor", "ladder", "chooser"]
    seed_noise = {}
    for o in OUTPUTS:
        g = sdf.groupby(KEY)[o]
        seed_noise[o] = float((g.max() - g.min()).mean())
    P(f"  {'output':<14s} {'class':<4s} {'mean 8-seed swing at L=63':>26s}")
    for o in OUTPUTS:
        P(f"  {o:<14s} {OUTPUTS[o]:<4s} {seed_noise[o]:>26.6f}")

    # --------------------------------------------------- ARM 4: the band map, per output, per m
    P("")
    P("-" * 100)
    P("ARM 4 — THE NEIGHBOURHOOD MAP: THE WIDEST [L_lo, L_hi] AROUND 63 INSIDE THE OUTPUT'S OWN NOISE")
    P("-" * 100)
    base = odf[odf.L == L_HEAD].set_index(KEY)
    swing = {}
    for o in OUTPUTS:
        sw = {}
        for L in L_NUM:
            cur = odf[odf.L == L].set_index(KEY)[o]
            sw[L] = float(np.nanmean(np.abs(cur - base[o])))
        swing[o] = sw
    brows2 = []
    for o in OUTPUTS:
        for m in NOISE_MULTS:
            tol = m * seed_noise[o]
            safe = [swing[o][L] <= tol + 1e-15 for L in L_NUM]
            lo, hi, nr, ok = widest_band(L_NUM, safe)
            brows2.append(dict(output=o, cls=OUTPUTS[o], noise_mult=m, seed_noise=seed_noise[o],
                               tol=tol, L_lo=lo, L_hi=hi, n_rungs=nr, band_ok=ok,
                               wider_than_point=bool(nr > 1),
                               covers_BAND_REC=bool(lo <= BAND_REC[0] and hi >= BAND_REC[1]),
                               covers_BAND_NEAR=bool(lo <= BAND_NEAR[0] and hi >= BAND_NEAR[1]),
                               swing_at_21=swing[o][21], swing_at_42=swing[o][42],
                               swing_at_126=swing[o][126], swing_at_252=swing[o][252],
                               first_unsafe_below=next((L for L in reversed([x for x in L_NUM if x < lo]) if True), np.nan) if lo > L_NUM[0] else np.nan,
                               first_unsafe_above=next((L for L in L_NUM if L > hi), np.nan) if hi < L_NUM[-1] else np.nan))
    bands = pd.DataFrame(brows2)
    dump(bands, "bands")
    for m in NOISE_MULTS:
        P(f"  noise multiple m = {m}")
        for _, r in bands[bands.noise_mult == m].iterrows():
            tagl = "" if np.isnan(r.first_unsafe_below) else f" (breaks below at {int(r.first_unsafe_below)})"
            tagh = "" if np.isnan(r.first_unsafe_above) else f" (breaks above at {int(r.first_unsafe_above)})"
            P(f"    {r.output:<14s} {r.cls:<4s} band [{r.L_lo:>4d}, {r.L_hi:>4d}] "
              f"{r.n_rungs:>2d} rungs  covers REC {str(bool(r.covers_BAND_REC)):<5s} "
              f"NEAR {str(bool(r.covers_BAND_NEAR)):<5s}{tagl}{tagh}")

    # --------------------------------------------------------- ARM 5: the 12-cell dial grid
    P("")
    P("-" * 100)
    P("ARM 5 — THE 12-CELL GRID, AND THE CENSUS THE CLAUSE WOULD RESOLVE")
    P("-" * 100)
    cen_p = Path(f"{REF_1242}.census_units.csv")
    cen = pd.read_csv(cen_p)
    cen["CARRIES_VERDICT"] = cen.CARRIES_VERDICT.astype(bool)
    cen["STATES_L"] = cen.STATES_L.astype(bool)
    P(f"  census inherited whole from 1242 ({cen_p.name}): {len(cen):,} committed text units.")
    core_bar = [o for o in OS_CORE if OUTPUTS[o] == "BAR"]
    def unit_outputs(row, oset):
        return [o for o in oset if bool(row.get(f"h_{o}", False))]
    checks = {}
    for sname, oset in OUTPUT_SETS.items():
        names = [f"h_{o}" for o in oset if f"h_{o}" in cen.columns]
        in_set = cen[names].any(axis=1)
        bar_names = [f"h_{o}" for o in oset if OUTPUTS[o] == "BAR" and f"h_{o}" in cen.columns]
        uses_bar = cen[bar_names].any(axis=1)
        sel = cen[in_set & cen.CARRIES_VERDICT & uses_bar & ~cen.STATES_L].copy()
        checks[sname] = sel
        P(f"  {sname:<8s} units naming the set {int(in_set.sum()):>5d};  verdict-carrying "
          f"{int((in_set & cen.CARRIES_VERDICT).sum()):>5d};  of those BAR-side and stating NO L: "
          f"{len(sel):>5d}")
    gate("G9", "1242's OS_CORE census counts replay (units / verdict / bar / unstated-L)",
         abs(len(checks["OS_CORE"]) - C1242_UNITS_CORE[3]),
         len(checks["OS_CORE"]) == C1242_UNITS_CORE[3])
    gate("G10", "1242's OS_WIDE unstated-L count replays (700)",
         abs(len(checks["OS_WIDE"]) - C1242_UNITS_WIDE_NO_L),
         len(checks["OS_WIDE"]) == C1242_UNITS_WIDE_NO_L)

    P("")
    P(f"  {'m':>4s} {'set':<8s} {'outputs':>7s} {'bar':>4s} {'band(intersect)':>17s} {'covers REC':>10s} "
      f"{'covers NEAR':>11s} {'units':>6s} {'resolvedREC':>12s} {'resolvedNEAR':>13s}")
    grows = []
    for m in NOISE_MULTS:
        bm = bands[bands.noise_mult == m].set_index("output")
        for sname, oset in OUTPUT_SETS.items():
            bar_os = [o for o in oset if OUTPUTS[o] == "BAR"]
            lo = max(int(bm.loc[o, "L_lo"]) for o in oset)
            hi = min(int(bm.loc[o, "L_hi"]) for o in oset)
            sel = checks[sname]
            res_rec = res_near = 0
            for _, r in sel.iterrows():
                used = [o for o in bar_os if bool(r.get(f"h_{o}", False))]
                res_rec += int(all(bool(bm.loc[o, "covers_BAND_REC"]) for o in used))
                res_near += int(all(bool(bm.loc[o, "covers_BAND_NEAR"]) for o in used))
            grows.append(dict(noise_mult=m, output_set=sname, n_outputs=len(oset), n_bar=len(bar_os),
                              band_lo=lo, band_hi=hi, band_rungs=sum(1 for L in L_NUM if lo <= L <= hi),
                              covers_BAND_REC=bool(lo <= BAND_REC[0] and hi >= BAND_REC[1]),
                              covers_BAND_NEAR=bool(lo <= BAND_NEAR[0] and hi >= BAND_NEAR[1]),
                              n_units=len(sel), resolved_REC=res_rec, resolved_NEAR=res_near,
                              frac_REC=res_rec / max(len(sel), 1), frac_NEAR=res_near / max(len(sel), 1),
                              n_outputs_wider_than_point=int(bm.loc[oset, "wider_than_point"].sum())))
            g = grows[-1]
            P(f"  {m:>4.1f} {sname:<8s} {len(oset):>7d} {len(bar_os):>4d} "
              f"{f'[{lo}, {hi}]':>17s} {str(g['covers_BAND_REC']):>10s} {str(g['covers_BAND_NEAR']):>11s} "
              f"{len(sel):>6d} {res_rec:>12d} {res_near:>13d}")
    grid = pd.DataFrame(grows)
    dump(grid, "grid")
    dump(pd.DataFrame([dict(output_set=k, n_unstated_L_verdict_units=len(v)) for k, v in checks.items()]), "census")

    m2 = grid[grid.noise_mult == 2.0]
    core2 = bands[(bands.noise_mult == 2.0) & (bands.output.isin(core_bar))]
    H_BAND = bool((core2.n_rungs > 1).all())
    H_COVER = bool(m2[m2.output_set == "OS_CORE"].covers_BAND_REC.iloc[0])
    row_core2 = m2[m2.output_set == "OS_CORE"].iloc[0]
    H_RESOLVE = bool(row_core2.resolved_REC > row_core2.n_units / 2)

    # ------------------------------------------------- ARM 6: rule 8 — the band, read once on OOS
    P("")
    P("-" * 100)
    P("ARM 6 — RULE 8: THE BAND IS MEASURED IN SAMPLE, THEN RE-MEASURED ONCE ON 2017-2026")
    P("-" * 100)
    P("  Pre-declared choice rule: among the 12 cells take the one resolving the MOST units against")
    P("  BAND_REC; ties broken by the SMALLEST noise multiple, then the SMALLEST output set.  No")
    P("  OOS quantity enters the choice.")
    ordq = {"OS_CORE": 0, "OS_WIDE": 1, "OS_ALL": 2}
    gsort = grid.copy()
    gsort["ord_set"] = gsort.output_set.map(ordq)
    gsort = gsort.sort_values(["resolved_REC", "noise_mult", "ord_set"],
                              ascending=[False, True, True]).reset_index(drop=True)
    pick = gsort.iloc[0]
    P(f"  RULE-8 CHOICE: m = {pick.noise_mult}, set = {pick.output_set}, IS band "
      f"[{int(pick.band_lo)}, {int(pick.band_hi)}], resolves {int(pick.resolved_REC)} of {int(pick.n_units)}")
    orows = []
    for (pn, an, lad, ch) in DEC:
        d = pre[(pn, an, lad, ch)]
        for L in L_NUM:
            D = draw_stats(d["Ro"], ch, L, seed_of("OOS", pn, an, lad, ch, L))
            orows.append(dict(panel=pn, anchor=an, ladder=lad, chooser=ch, L=L,
                              **d["oouto"], **bar_outputs(D, d["obso"], d["jo"])))
        for sd in SEED_LADDER:
            D = draw_stats(d["Ro"], ch, L_HEAD, seed_of("OOSSEED", sd, pn, an, lad, ch))
            orows.append(dict(panel=pn, anchor=an, ladder=lad, chooser=ch, L=-sd - 1,
                              **d["oouto"], **bar_outputs(D, d["obso"], d["jo"])))
    oo = pd.DataFrame(orows)
    oo_L = oo[oo.L > 0]
    oo_S = oo[oo.L < 0]
    obase = oo_L[oo_L.L == L_HEAD].set_index(KEY)
    wrows = []
    for o in OUTPUTS:
        g = oo_S.groupby(KEY)[o]
        noise_o = float((g.max() - g.min()).mean())
        sw = {L: float(np.nanmean(np.abs(oo_L[oo_L.L == L].set_index(KEY)[o] - obase[o]))) for L in L_NUM}
        for m in NOISE_MULTS:
            safe = [sw[L] <= m * noise_o + 1e-15 for L in L_NUM]
            lo, hi, nr, ok = widest_band(L_NUM, safe)
            wrows.append(dict(output=o, cls=OUTPUTS[o], noise_mult=m, oos_seed_noise=noise_o,
                              oos_L_lo=lo, oos_L_hi=hi, oos_n_rungs=nr,
                              oos_covers_BAND_REC=bool(lo <= BAND_REC[0] and hi >= BAND_REC[1]),
                              oos_covers_BAND_NEAR=bool(lo <= BAND_NEAR[0] and hi >= BAND_NEAR[1])))
    wf = pd.DataFrame(wrows)
    dump(wf, "walkforward")
    pm, pset = float(pick.noise_mult), str(pick.output_set)
    sub_is = bands[(bands.noise_mult == pm) & (bands.output.isin(OUTPUT_SETS[pset]))].set_index("output")
    sub_oos = wf[(wf.noise_mult == pm) & (wf.output.isin(OUTPUT_SETS[pset]))].set_index("output")
    is_lo = max(int(sub_is.loc[o, "L_lo"]) for o in OUTPUT_SETS[pset])
    is_hi = min(int(sub_is.loc[o, "L_hi"]) for o in OUTPUT_SETS[pset])
    oos_lo = max(int(sub_oos.loc[o, "oos_L_lo"]) for o in OUTPUT_SETS[pset])
    oos_hi = min(int(sub_oos.loc[o, "oos_L_hi"]) for o in OUTPUT_SETS[pset])
    held = bool(oos_lo <= is_lo and oos_hi >= is_hi)
    P(f"  IS band  [{is_lo}, {is_hi}]   ->   OOS band (read ONCE) [{oos_lo}, {oos_hi}]   "
      f"IS band holds out of sample: {held}")
    P(f"  {'output':<14s} {'IS band':>14s} {'OOS band':>14s}  holds")
    for o in OUTPUT_SETS[pset]:
        a1, a2 = int(sub_is.loc[o, "L_lo"]), int(sub_is.loc[o, "L_hi"])
        b1, b2 = int(sub_oos.loc[o, "oos_L_lo"]), int(sub_oos.loc[o, "oos_L_hi"])
        P(f"  {o:<14s} {f'[{a1}, {a2}]':>14s} {f'[{b1}, {b2}]':>14s}  {b1 <= a1 and b2 >= a2}")
    H_TRANSFER = held
    for m in NOISE_MULTS:
        sub = wf[(wf.noise_mult == m) & (wf.cls == "BAR")]
        P(f"  m = {m}: OOS bands wider than a point at {int((sub.oos_n_rungs > 1).sum())} of "
          f"{len(sub)} bar outputs;  covering BAND_REC at {int(sub.oos_covers_BAND_REC.sum())}")

    # ------------------------------------------- ARM 7: does L inside the band touch capital?
    P("")
    P("-" * 100)
    P("ARM 7 — CAPITAL: WHAT MOVING L INSIDE THE BAND DOES TO REAL BOOKS AND TO 4b")
    P("-" * 100)
    bkey = books.set_index(["panel", "anchor", "ladder", "rung"])
    dec_meta = []
    for (pn, an, lad, ch) in DEC:
        d = pre[(pn, an, lad, ch)]
        pick_rung = d["rungs"][d["j"]]
        anch = ANCHORS[an][lad]
        dec_meta.append(dict(panel=pn, anchor=an, ladder=lad, chooser=ch, pick=pick_rung, anchor_rung=anch,
                             pick_OOS=float(bkey.loc[(pn, an, lad, pick_rung)].OOS_Sharpe),
                             anchor_OOS=float(bkey.loc[(pn, an, lad, anch)].OOS_Sharpe),
                             pick_4b=int(bool(bkey.loc[(pn, an, lad, pick_rung)].pass_4b_full) and
                                         bool(bkey.loc[(pn, an, lad, pick_rung)].pass_4b_oos)),
                             anchor_4b=int(bool(bkey.loc[(pn, an, lad, anch)].pass_4b_full) and
                                           bool(bkey.loc[(pn, an, lad, anch)].pass_4b_oos))))
    dm = pd.DataFrame(dec_meta).set_index(KEY)
    base_oos = float(dm.anchor_OOS.mean())
    base_4b = int(dm.anchor_4b.sum())
    gate("G11", "do-nothing mean OOS Sharpe vs 1246/1260's committed 0.7922",
         abs(base_oos - C1246_ANCHOR_OOS), abs(base_oos - C1246_ANCHOR_OOS) < 5e-3)
    crows = []
    for L in L_NUM:
        sub = odf[odf.L == L].set_index(KEY)
        fire = sub.B_RESOLVED.reindex(dm.index).values > 0.5
        oos = np.where(fire, dm.pick_OOS.values, dm.anchor_OOS.values)
        n4b = int(np.where(fire, dm.pick_4b.values, dm.anchor_4b.values).sum())
        crows.append(dict(L=L, n_fire=int(fire.sum()), sel_mean_OOS_Sharpe=float(oos.mean()),
                          d_sel=float(oos.mean()) - base_oos, n_4b_both=n4b,
                          do_nothing_OOS=base_oos, do_nothing_4b=base_4b))
    cap = pd.DataFrame(crows)
    dump(cap, "capital")
    P(f"  the gated selector (P_boot >= 0.90) at every L rung — picks are L-FREE, only the GATE moves:")
    P(f"  {'L':>5s} {'n_fire':>7s} {'selOOS':>8s} {'d_sel':>8s} {'4b BOTH':>8s}")
    for _, r in cap.iterrows():
        P(f"  {int(r.L):>5d} {int(r.n_fire):>7d} {r.sel_mean_OOS_Sharpe:>8.4f} {r.d_sel:>+8.4f} {int(r.n_4b_both):>8d}")
    in_band = cap[(cap.L >= is_lo) & (cap.L <= is_hi)]
    P(f"  INSIDE the rule-8 band [{is_lo}, {is_hi}]: d_sel spans {in_band.d_sel.min():+.4f} to "
      f"{in_band.d_sel.max():+.4f} ({in_band.d_sel.max() - in_band.d_sel.min():.4f} wide), "
      f"4b BOTH {int(in_band.n_4b_both.min())}-{int(in_band.n_4b_both.max())} vs do-nothing {base_4b}")
    P(f"  OVER THE WHOLE LADDER:                 d_sel spans {cap.d_sel.min():+.4f} to "
      f"{cap.d_sel.max():+.4f} ({cap.d_sel.max() - cap.d_sel.min():.4f} wide), "
      f"4b BOTH {int(cap.n_4b_both.min())}-{int(cap.n_4b_both.max())}")
    picks_move = int((odf.groupby(KEY).pick.nunique() > 1).sum())
    gate("G12", "the book PICK never moves with L (0 of 72 decisions)", picks_move, picks_move == 0)
    H_CAPITAL = bool(picks_move == 0 and int(in_band.n_4b_both.min()) == int(in_band.n_4b_both.max()))

    P("")
    P("-" * 100)
    P("ARM 8 — BOTH KEEP PATHS ON THE 162 RUNG BOOKS")
    P("-" * 100)
    P(f"  4a {int(books.pass_4a.sum())} of {len(books)}  (A_DD fails at {int((~books.A_DD).sum())})")
    P(f"  4b full {int(books.pass_4b_full.sum())};  4b OOS {int(books.pass_4b_oos.sum())};  "
      f"BOTH {int((books.pass_4b_full & books.pass_4b_oos).sum())} rows -> "
      f"{books[books.pass_4b_full & books.pass_4b_oos].drop_duplicates(subset=['panel','N','H','GROSS','CADENCE']).shape[0]} distinct, "
      f"{books[books.pass_4b_full & books.pass_4b_oos].groupby('panel').size().to_dict()}")
    for leg in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"):
        P(f"    4b leg {leg:<7s} fails at {int((~books[leg]).sum()):>3d} of {len(books)}")
    bb = books[books.pass_4b_full & books.pass_4b_oos].drop_duplicates(subset=["panel", "N", "H", "GROSS", "CADENCE"])
    for _, r in bb.sort_values("OOS_Sharpe", ascending=False).head(6).iterrows():
        P(f"    {r.panel:<6s} N={r.N:<3.0f} H={r.H:<4.0f} G={r.GROSS:.2f} {r.CADENCE:<2s}  full "
          f"{r.CAGR:>7.2%} / {r.Sharpe:.4f} / {r.MaxDD:>7.2%}  halves {r.H1:.4f}/{r.H2:.4f}  "
          f"OOS {r.OOS_CAGR:>7.2%} / {r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:>7.2%}")
    P("  Every one is prior art; this run adds no book — the object here is a PUBLISHING clause.")

    P("")
    P("-" * 100)
    P("VERDICT")
    P("-" * 100)
    core_bar_bands = bands[(bands.noise_mult == 2.0) & (bands.output.isin(core_bar))]
    if not H_BAND:
        outcome = "(C) THERE IS NO NEIGHBOURHOOD"
    elif H_COVER:
        outcome = "(A) THE NEIGHBOURHOOD IS WIDE ENOUGH"
    else:
        outcome = "(B) THE NEIGHBOURHOOD IS REAL BUT NARROWER THAN THE RECORD'S SPAN"
    P(f"  OUTCOME: {outcome}")
    P(f"  H_BAND {'SUPPORTED' if H_BAND else 'REFUTED'};  H_COVER {'SUPPORTED' if H_COVER else 'REFUTED'};"
      f"  H_RESOLVE {'SUPPORTED' if H_RESOLVE else 'REFUTED'};  H_TRANSFER "
      f"{'SUPPORTED' if H_TRANSFER else 'REFUTED'};  H_CAPITAL {'SUPPORTED' if H_CAPITAL else 'REFUTED'}")
    P(f"  At m = 2.0 the OS_CORE bar outputs' bands are: " +
      ";  ".join(f"{r.output} [{int(r.L_lo)}, {int(r.L_hi)}]" for _, r in core_bar_bands.iterrows()))
    P(f"  CAPITAL: 4a {int(books.pass_4a.sum())} of 162; no new book; the clause is a PUBLISHING")
    P("  change for the Sunday review (rule 6), nothing enacted here.")

    gate("G13", "determinism / shape: 12 grid rows, 72 outputs-per-rung, 162 books",
         abs(len(grid) - 12) + abs(len(odf) - 72 * len(L_ALL)) + abs(len(books) - 162),
         len(grid) == 12 and len(odf) == 72 * len(L_ALL) and len(books) == 162)
    spy_days = int((PAN["SMALL"].elig[:, list(PAN["SMALL"].px.columns).index("SPY")]).sum())
    gate("G14", "SPY never eligible on SMALL (benchmark, not constituent)", spy_days, spy_days == 0)
    gates = pd.DataFrame(GATES)
    dump(gates, "gates")
    P(f"  GATES {int(gates.pass_.sum())} of {len(gates)}")
    P(f"  elapsed {time.time() - t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
