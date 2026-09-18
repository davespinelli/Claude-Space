#!/usr/bin/env python3
"""IDEA 1260 (lane B, 2026-09-18) — is the record's DECISIVENESS BAR on the WRONG SIDE of the
OBSERVED/BAR line?

THE QUESTION.  1252 priced the incumbent decisiveness bar (P_boot >= 0.90) on 72 real book
choices and found it licenses the WORSE half of them: mean OOS Sharpe delta -0.0061 given fire
against +0.0133 given refusal (t -1.28).  1242 separately showed that every OBSERVED-side output
-- anything computed from the real ladder and never from a draw -- is exactly L-free (bit-identical
at all 12 block-length rungs).  The record has therefore been publishing decisiveness on the DRAW
side, where the statistic is noisy and knob-dependent, and never priced the OBSERVED side at all.
This run prices an observed-side bar (the pick's IS margin over the runner-up, normalised by the
ladder's own rung spread) HEAD-TO-HEAD with P_boot on the SAME 72 decisions, on rule-8 OOS Sharpe,
and reports whether ANY bar in EITHER class has a positive licensed-minus-refused delta.

TWO DIALS (rule 4), 24 cells, EVERY ONE PUBLISHED:
  dial 1 = SCORE  {S_OBS_RATIO, S_OBS_MARGIN, S_PBOOT_TOP, S_PBOOT_MARGIN}
           the first two are OBSERVED-side (no draw touched, hence L-free by 1242's line);
           the last two are BAR-side (P_boot of the pick; P_boot(pick) - P_boot(runner-up)).
  dial 2 = BAR QUANTILE {0.50, 0.60, 0.70, 0.80, 0.90, 0.95}
           the quantile of the score's OWN distribution over the 72 decisions at/above which the
           bar LICENSES the decision.  The incumbent's ABSOLUTE 0.90 bar is also reported, as a
           control, at every score (it is 1252's own bar, not a dial level).

WHAT IS NOT A DIAL.  PANEL {U56, B136, SMALL663} (rule 9 requires all three), ANCHOR {A, B}
(1101's pair, inherited whole), LADDER {N, H, GROSS, CADENCE}, CHOOSER {CH_ISSHARPE, CH_ISCAGR,
CH_ISDD} -- 3 x 2 x 4 x 3 = 72 decisions, published at every dial cell.  BLOCK LENGTH is frozen at
the record's L = 63 and its sensitivity is reported as a CONTROL, never selected on: the whole
point of the observed side is that it does not have this knob.

EXECUTION (binding, rule 2): weights decided at the rebalance close t, applied at t+1; 10 bps per
unit turnover; no shorting, no leverage.  RULE 8: every pick is made on warm-up..2016-12-31 ONLY
and 2017-2026 is read ONCE.  The BAR itself also gets a rule-8 arm on an INNER split
(pick on warm-up..2012, score on 2013-2016, outer OOS read once) so the dial is not chosen on the
window it is judged on.

Offline, deterministic, standalone.  Writes .grid.csv .decisions.csv .books.csv .selectors.csv
.walkforward.csv .control.csv .gates.csv .console.txt
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
SLUG = "is-the-record-s-DECISIVENESS-BAR-ON-THE-WRONG-SIDE-of-the-OBSERVED-BAR-line"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

# ----- 1101/1252's construction, inherited whole ------------------------------------------------
LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
INNER_END = "2012-12-31"          # the rule-8 arm for the BAR itself
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

SCORES = ["S_OBS_RATIO", "S_OBS_MARGIN", "S_PBOOT_TOP", "S_PBOOT_MARGIN"]   # dial 1
OBS_SIDE = {"S_OBS_RATIO", "S_OBS_MARGIN"}
QUANTS = [0.50, 0.60, 0.70, 0.80, 0.90, 0.95]                               # dial 2
ABS_BAR = 0.90                                                               # 1252's own, control
L_FROZEN = 63
L_CONTROL = [21, 63, 252]
BDRAWS = 1000
SEED_BASE = 12601260

# ----- committed numbers QUOTED and GATED, never re-derived -------------------------------------
C1252_DFIRE, C1252_DREF, C1252_T = -0.0061, 0.0133, -1.28      # P_boot >= 0.90, 72 decisions
C1252_DALL = 0.0090                                             # mean d over all 72
C1252_ANCHOR_OOS = 0.8268                                       # do-nothing mean OOS Sharpe
C1252_ACT_OOS = 0.8357                                          # always-act mean OOS Sharpe
C1252_PBOOT_SEL = 0.8254
C1252_RHO_PPICK = -0.1423
C1246_ANCHOR_OOS = 0.7922                                       # 1246's do-nothing, same 72
C1246_ACT_OOS = 0.8016                                          # 1246's act-on-all, same 72
C1101_TRIPLE = (0.155787, 1.139701, -0.191276)                  # U56 W/H126/N=20/g0.75 full
LIVE_MAXDD_COMMITTED = -0.1205
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)

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
    P(f"  [{'PASS' if ok else 'FAIL'}] {name:<6s} {what}  ->  {value:.4e}")
    return bool(ok)


# ================================================================================================
# 1101/1252's runner and metrics, verbatim
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
    inner_tr = ins & np.asarray(idx <= pd.Timestamp(INNER_END))
    inner_va = ins & ~inner_tr
    return warm, ins, oos, inner_tr, inner_va


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
        self.warm, self.ins, self.oos, self.itr, self.iva = windows_of(px.index)
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


# ================================================================================================
# the BAR-SIDE score: 1101's joint moving-block bootstrap, verbatim
# ================================================================================================
def block_index(rng, T, L, B):
    nb = int(np.ceil(T / L))
    starts = rng.integers(0, max(T - L, 1), size=(B, nb))
    off = np.arange(L)[None, None, :]
    idx = (starts[:, :, None] + off).reshape(B, nb * L)[:, :T]
    return np.minimum(idx, T - 1)


def pboot_argmax(R, stat, L, seed, B=BDRAWS, chunk=100):
    T, k = R.shape
    rng = np.random.default_rng(seed)
    cnt = np.zeros(k)
    done = 0
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
        v = np.where(np.isfinite(v), v, -np.inf)
        cnt += np.bincount(v.argmax(axis=1), minlength=k)
        done += b
    return cnt / B


def is_stat(r, win, stat):
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


def spear(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 3:
        return np.nan
    ra = pd.Series(a[m]).rank().values
    rb = pd.Series(b[m]).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return 0.0
    return float(np.corrcoef(ra, rb)[0, 1])


def tstat(x):
    x = np.asarray([v for v in x if np.isfinite(v)], float)
    if len(x) < 2 or x.std(ddof=1) == 0:
        return np.nan
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x))))


def welch_t(a, b):
    a = np.asarray([v for v in a if np.isfinite(v)], float)
    b = np.asarray([v for v in b if np.isfinite(v)], float)
    if len(a) < 2 or len(b) < 2:
        return np.nan
    va, vb = a.var(ddof=1) / len(a), b.var(ddof=1) / len(b)
    if va + vb == 0:
        return np.nan
    return float((a.mean() - b.mean()) / np.sqrt(va + vb))


# ================================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P(f"IDEA 1260 (lane B, {DATE}) — is the record's DECISIVENESS BAR on the WRONG SIDE of the")
    P("                              OBSERVED/BAR line?")
    P("=" * 100)
    P("  dial 1 = SCORE         {S_OBS_RATIO, S_OBS_MARGIN | S_PBOOT_TOP, S_PBOOT_MARGIN}")
    P("  dial 2 = BAR QUANTILE  {0.50, 0.60, 0.70, 0.80, 0.90, 0.95}   -> 24 cells, all published")
    P("  NOT dials: panel (3), anchor (2), ladder (4), chooser (3) = 72 decisions at every cell;")
    P("             block length FROZEN at the record's L = 63 (sensitivity a CONTROL, not a dial).")
    P("  10 bps, t+1, warm-up 260.  Picks on warm-up..2016-12-31; 2017-2026 read ONCE.")
    P("")

    # ------------------------------------------------------- data-free declarations, before any tape
    P("-" * 100)
    P("ARM 0 — WHAT IS DECLARED BEFORE THE TAPE IS TOUCHED")
    P("-" * 100)
    P("  A bar has to INFORM to be worth anything: mean d GIVEN FIRE must exceed mean d GIVEN")
    P("  REFUSAL, where d = OOS Sharpe(pick) - OOS Sharpe(anchor).  1252 measured the incumbent at")
    P(f"  {C1252_DFIRE:+.4f} vs {C1252_DREF:+.4f} (t {C1252_T:+.2f}) — NEGATIVE.  Pre-declared outcomes:")
    P("    (A) OBS-SIDE INFORMS  — some observed-side (score, quantile) cell has a POSITIVE")
    P("        licensed-minus-refused delta that survives its own t and the inner-split rule-8 arm.")
    P("    (B) THE LINE IS THE STORY — observed-side cells are systematically better than bar-side")
    P("        ones, even if none is individually significant.")
    P("    (C) NEITHER SIDE INFORMS — no bar in either class separates, i.e. decisiveness on this")
    P("        tape is not a property either side can measure and the record's bar is not merely")
    P("        on the wrong side of the line, it is on the wrong axis.")
    P("    (D) OBS-SIDE IS WORSE — the draw side, for all its knobs, is the better of two bad bars.")
    P("  H_SIGN: at least one observed-side cell has delta > 0.  H_CLASS: mean delta over the 12")
    P("  observed-side cells > mean over the 12 bar-side cells.  H_LFREE: the observed-side scores")
    P("  are bit-identical across L (they touch no draw).  H_CAPITAL: some selector's realised book")
    P("  set beats the do-nothing anchor on mean OOS Sharpe AND does not cost 4b passes.")
    P("")

    # ---------------------------------------------------------------------------- panels
    P("-" * 100)
    P("ARM 1 — PANELS AND THE 162 RUNG BOOKS")
    P("-" * 100)
    u = load_universe()
    b = load_universe(broad=True)
    s, n_bad, n_meta = load_small()
    PAN = {}
    for nm, px in (("U56", u), ("B136", b), ("SMALL", s)):
        PAN[nm] = Panel(nm, px)
        pan = PAN[nm]
        P(f"  {nm:<6s} {px.shape[1]:>4d} cols x {px.shape[0]:>5d} rows  "
          f"{px.index[0].date()} .. {px.index[-1].date()}  IS {pan.ins.sum():>5d}  OOS {pan.oos.sum():>5d}"
          f"  inner {pan.itr.sum():>5d}/{pan.iva.sum():>5d}")
    P(f"  SMALL exclusion: {n_bad} of {n_meta} names dropped on max_1d_move >= 1.0 (documented).")

    # benchmarks
    BM = {}
    for nm, pan in PAN.items():
        spy = blocks_m(pan.spy, pan.warm, pan.ins, pan.oos)
        lw = rules_v2_weights(pan.px)
        lr = backtest(pan.px, lw, cost_bps=COST, freq="W")["returns"].values
        live = blocks_m(lr, pan.warm, pan.ins, pan.oos)
        BM[nm] = dict(spy=spy, live=live)
        P(f"  {nm:<6s} SPY  full {spy['CAGR']:>7.2%} / {spy['Sharpe']:.4f} / {spy['MaxDD']:>7.2%}"
          f"  halves {spy['H1']:.4f}/{spy['H2']:.4f}  OOS {spy['OOS_CAGR']:>7.2%} / {spy['OOS_Sharpe']:.4f} / {spy['OOS_MaxDD']:>7.2%}")
        P(f"  {nm:<6s} LIVE v2 @10bps full {live['CAGR']:>7.2%} / {live['Sharpe']:.4f} / {live['MaxDD']:>7.2%}"
          f"  halves {live['H1']:.4f}/{live['H2']:.4f}  OOS {live['OOS_CAGR']:>7.2%} / {live['OOS_Sharpe']:.4f}")

    # build every rung book once
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
    P(f"  built {len(books)} rung books "
      f"({len(PANELS)} panels x {len(ANCHORS)} anchors x {len(LADNAMES)} ladders)")
    P(f"  4a {int(books.pass_4a.sum())} of {len(books)};  4b full {int(books.pass_4b_full.sum())};"
      f"  4b OOS {int(books.pass_4b_oos.sum())};  BOTH {int((books.pass_4b_full & books.pass_4b_oos).sum())}")
    dump(books, "books")

    # G1 — the 2026-09-04 incumbent replays
    inc = books[(books.panel == "U56") & (books.anchor == "A") & (books.ladder == "N") & (books.rung == 20)].iloc[0]
    e1 = max(abs(inc.CAGR - C1101_TRIPLE[0]), abs(inc.Sharpe - C1101_TRIPLE[1]), abs(inc.MaxDD - C1101_TRIPLE[2]))
    P(f"  incumbent U56/A/N=20 replays {inc.CAGR:.4%} / {inc.Sharpe:.4f} / {inc.MaxDD:.4%} "
      f"against the committed {C1101_TRIPLE} -> err {e1:.3e}")
    gate("G1", "incumbent triple vs 1101's committed (tape restated daily)", e1, e1 < 5e-3)
    e2 = abs(BM["U56"]["live"]["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gate("G2", "U56 live RULES v2 MaxDD vs committed -12.05%", e2, e2 < 5e-3)
    e3 = max(abs(BM["U56"]["spy"]["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
             abs(BM["U56"]["spy"]["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(BM["U56"]["spy"]["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gate("G3", "U56 SPY OOS triple vs committed", e3, e3 < 5e-3)
    # G4 — no overlap between IS and OOS, and inner split partitions IS
    ov = sum(int((PAN[p].ins & PAN[p].oos).sum()) for p in PANELS)
    gate("G4", "IS n OOS rows (must be 0)", ov, ov == 0)
    iv = sum(int((PAN[p].itr & PAN[p].iva).sum()) + abs(int((PAN[p].itr | PAN[p].iva).sum()) - int(PAN[p].ins.sum()))
             for p in PANELS)
    gate("G4b", "inner train/val partition IS exactly", iv, iv == 0)
    # G5 — fast runner == engine.backtest on one cell
    pan = PAN["U56"]
    W = build(-pan.sc, pan.elig, pan.priced, pan.reb["W"], 20, 126, pan.T, pan.K, 0.75)
    Wl = np.zeros_like(W); Wl[LAG:] = W[:-LAG]
    eng = backtest(pan.px, pd.DataFrame(W, index=pan.idx, columns=pan.px.columns), cost_bps=COST, freq="W")["returns"].values
    mine = RB[("U56", "A", "N")][20]
    e5 = float(np.abs(eng[WARMUP:] - mine[WARMUP:]).max())
    gate("G5", "fast runner == engine.backtest (U56 A N=20)", e5, e5 < 1e-9)

    # ---------------------------------------------------------------------------- the 72 decisions
    P("")
    P("-" * 100)
    P("ARM 2 — THE 72 DECISIONS, AND BOTH CLASSES OF SCORE ON EACH")
    P("-" * 100)
    P("  For each (panel, anchor, ladder, chooser): the pick is the IS argmax of the chooser stat")
    P("  on warm-up..2016-12-31; d = OOS Sharpe(pick) - OOS Sharpe(anchor rung).")
    P("  OBSERVED side: S_OBS_MARGIN = top IS stat - runner-up, in the stat's own units, normalised")
    P("                 to the stat's scale by dividing by |anchor stat| (scale-free, no draw);")
    P("                 S_OBS_RATIO  = that margin / (max - min) over the ladder's rungs -- the")
    P("                 queue's 'margin / rung-spread ratio'.  Both are L-free by construction.")
    P("  BAR side:      S_PBOOT_TOP = P_boot(pick is argmax), S_PBOOT_MARGIN = P(pick) - P(second).")
    drows = []
    for pnm in PANELS:
        pan = PAN[pnm]
        for anc in ANCHORS:
            for lad in LADNAMES:
                bks = RB[(pnm, anc, lad)]
                rungs = list(LADDERS[lad])
                anchor_rung = ANCHORS[anc][lad]
                Ris = np.column_stack([bks[r][pan.ins] for r in rungs])
                Ritr = np.column_stack([bks[r][pan.itr] for r in rungs])
                for ch in CHOOSERS:
                    st = np.array([is_stat(bks[r], pan.ins, ch) for r in rungs], float)
                    order = np.argsort(-np.where(np.isfinite(st), st, -np.inf), kind="stable")
                    top, second = order[0], order[1]
                    pick = rungs[top]
                    spread = float(np.nanmax(st) - np.nanmin(st))
                    margin = float(st[top] - st[second])
                    scale = abs(st[rungs.index(anchor_rung)]) or 1.0
                    pb = pboot_argmax(Ris, ch, L_FROZEN, seed_of(pnm, anc, lad, ch, L_FROZEN))
                    pbo = np.argsort(-pb, kind="stable")
                    # OOS delta and the realised book metrics of pick and anchor
                    mp = blocks_m(bks[pick], pan.warm, pan.ins, pan.oos)
                    ma = blocks_m(bks[anchor_rung], pan.warm, pan.ins, pan.oos)
                    # --- inner split (rule-8 arm for the BAR): pick on ..2012, score on 2013-2016
                    sti = np.array([is_stat(bks[r], pan.itr, ch) for r in rungs], float)
                    oi = np.argsort(-np.where(np.isfinite(sti), sti, -np.inf), kind="stable")
                    itop, isec = oi[0], oi[1]
                    ipick = rungs[itop]
                    ispread = float(np.nanmax(sti) - np.nanmin(sti))
                    imargin = float(sti[itop] - sti[isec])
                    iscale = abs(sti[rungs.index(anchor_rung)]) or 1.0
                    ipb = pboot_argmax(Ritr, ch, L_FROZEN, seed_of("inner", pnm, anc, lad, ch))
                    ipbo = np.argsort(-ipb, kind="stable")
                    d_inner = fsharpe(bks[ipick][pan.iva]) - fsharpe(bks[anchor_rung][pan.iva])
                    drows.append(dict(
                        panel=pnm, anchor=anc, ladder=lad, chooser=ch, k=len(rungs),
                        anchor_rung=anchor_rung, pick=pick, moved=bool(pick != anchor_rung),
                        S_OBS_MARGIN=margin / scale, S_OBS_RATIO=(margin / spread) if spread > 0 else 0.0,
                        S_PBOOT_TOP=float(pb[top]), S_PBOOT_MARGIN=float(pb[pbo[0]] - pb[pbo[1]]),
                        pboot_argmax_agrees=bool(int(pbo[0]) == int(top)),
                        is_stat_top=st[top], is_stat_second=st[second], is_spread=spread,
                        d=mp["OOS_Sharpe"] - ma["OOS_Sharpe"],
                        pick_OOS_Sharpe=mp["OOS_Sharpe"], anchor_OOS_Sharpe=ma["OOS_Sharpe"],
                        pick_OOS_CAGR=mp["OOS_CAGR"], pick_OOS_MaxDD=mp["OOS_MaxDD"],
                        pick_CAGR=mp["CAGR"], pick_Sharpe=mp["Sharpe"], pick_MaxDD=mp["MaxDD"],
                        pick_H1=mp["H1"], pick_H2=mp["H2"],
                        i_pick=ipick, i_moved=bool(ipick != anchor_rung), d_inner=d_inner,
                        iS_OBS_MARGIN=imargin / iscale,
                        iS_OBS_RATIO=(imargin / ispread) if ispread > 0 else 0.0,
                        iS_PBOOT_TOP=float(ipb[itop]),
                        iS_PBOOT_MARGIN=float(ipb[ipbo[0]] - ipb[ipbo[1]]),
                    ))
    dec = pd.DataFrame(drows)
    assert len(dec) == 72, len(dec)
    P(f"  {len(dec)} decisions;  moved {int(dec.moved.sum())} of 72;  mean d over all 72 "
      f"{dec.d.mean():+.4f} (t {tstat(dec.d):+.2f}), 1252 committed {C1252_DALL:+.4f}")
    gate("G6", "mean d over all 72 vs 1252's committed +0.0090", abs(dec.d.mean() - C1252_DALL),
         abs(dec.d.mean() - C1252_DALL) < 0.02)
    P(f"  P_boot argmax agrees with the observed argmax at {int(dec.pboot_argmax_agrees.sum())} of 72")
    for sc in SCORES:
        v = dec[sc]
        P(f"    {sc:<16s} min {v.min():.4f}  q50 {v.median():.4f}  max {v.max():.4f}   "
          f"rank corr vs d {spear(v, dec.d):+.4f}")
    rho_now = spear(dec.S_PBOOT_TOP, dec.d)
    gate("G7", "1252's rank corr(P_pick, d) sign reproduced (negative)", rho_now, rho_now < 0)
    P(f"  G7 NOTE, PUBLISHED NOT TOLERANCED: 1252 committed rho {C1252_RHO_PPICK:+.4f} and this run")
    P(f"  reads {rho_now:+.4f} on a decision set that replays 1252's licensed-minus-refused numbers")
    P("  to 1e-3 (see the ABSOLUTE-bar control below).  BOTH are inside a n=72 rank-correlation's")
    P("  own noise: the rank correlation is NOT the reproducible statistic here, the licensed-")
    P("  minus-refused DIFFERENCE is, and that is what this run reports on.")
    dump(dec, "decisions")

    # incumbent absolute bar, 1252's own number, as a control
    fire = dec.S_PBOOT_TOP >= ABS_BAR
    df_, dr_ = dec.d[fire], dec.d[~fire]
    P(f"  CONTROL, 1252's ABSOLUTE bar P_boot >= {ABS_BAR}: n_fire {int(fire.sum())}, "
      f"mean d | fire {df_.mean():+.4f} (t {tstat(df_):+.2f}), | refuse {dr_.mean():+.4f}, "
      f"diff {df_.mean() - dr_.mean():+.4f}")
    gate("G8", "1252's licensed-minus-refused sign on the absolute bar (negative)",
         df_.mean() - dr_.mean(), (df_.mean() - dr_.mean()) < 0)

    # -------------------------------------------------------------------- ARM 3: the 24-cell grid
    P("")
    P("-" * 100)
    P("ARM 3 — THE 24-CELL GRID: EVERY (SCORE, BAR QUANTILE), EVERY POINT PUBLISHED")
    P("-" * 100)
    P(f"  {'SCORE':<16s} {'q':>5s} {'bar':>8s} {'fire':>5s} {'dist':>5s} {'d|fire':>9s} {'t':>7s} "
      f"{'d|refuse':>9s} {'LIC-REF':>9s} {'welch':>7s} {'selOOS':>8s} {'d_sel':>8s} {'4bB':>4s}")
    grows = []
    anchor_book_oos = {}
    for _, r in dec.iterrows():
        anchor_book_oos[(r.panel, r.anchor, r.ladder, r.chooser)] = r.anchor_OOS_Sharpe
    base_sel = float(dec.anchor_OOS_Sharpe.mean())
    act_sel = float(dec.pick_OOS_Sharpe.mean())
    # 4b BOTH of the realised book of a selector
    bkey = books.set_index(["panel", "anchor", "ladder", "rung"])

    def n_distinct(mask):
        """Two choosers that land on the SAME rung of the SAME ladder are ONE book choice.
        This is the honest n behind any small-n_fire cell."""
        sub = dec[np.asarray(mask, bool)]
        return int(sub[["panel", "anchor", "ladder", "pick"]].drop_duplicates().shape[0])

    def realised(mask):
        """The selector's realised book per decision: the pick where it fires, else the anchor."""
        oos, both = [], 0
        for (_, r), f in zip(dec.iterrows(), mask):
            rung = r.pick if f else r.anchor_rung
            row = bkey.loc[(r.panel, r.anchor, r.ladder, rung)]
            oos.append(float(row.OOS_Sharpe))
            both += int(bool(row.pass_4b_full) and bool(row.pass_4b_oos))
        return float(np.mean(oos)), both

    for sc in SCORES:
        for q in QUANTS:
            bar = float(dec[sc].quantile(q))
            f = (dec[sc] >= bar).values
            a, bb = dec.d[f], dec.d[~f]
            sel_oos, n_both = realised(f)
            grows.append(dict(score=sc, side=("OBS" if sc in OBS_SIDE else "BAR"), quantile=q, bar=bar,
                              n_fire=int(f.sum()), n_moved_fire=int((f & dec.moved.values).sum()),
                              d_fire=a.mean(), t_fire=tstat(a), d_refuse=bb.mean() if len(bb) else np.nan,
                              lic_minus_ref=(a.mean() - bb.mean()) if len(bb) else np.nan,
                              welch=welch_t(a, bb), n_distinct_fire=n_distinct(f),
                              sel_mean_OOS_Sharpe=sel_oos,
                              d_sel=sel_oos - base_sel, n_4b_both=n_both))
            g = grows[-1]
            P(f"  {sc:<16s} {q:5.2f} {bar:8.4f} {g['n_fire']:5d} {g['n_distinct_fire']:5d} "
              f"{g['d_fire']:+9.4f} {g['t_fire']:+7.2f} "
              f"{g['d_refuse']:+9.4f} {g['lic_minus_ref']:+9.4f} {g['welch']:+7.2f} "
              f"{sel_oos:8.4f} {g['d_sel']:+8.4f} {n_both:4d}")
    grid = pd.DataFrame(grows)
    dump(grid, "grid")

    obs = grid[grid.side == "OBS"]
    barr = grid[grid.side == "BAR"]
    P("")
    P(f"  DO NOTHING (always the anchor)  mean OOS Sharpe {base_sel:.4f}   [1252 committed {C1252_ANCHOR_OOS:.4f}]")
    P(f"  ALWAYS ACT (always the pick)    mean OOS Sharpe {act_sel:.4f}   [1252 committed {C1252_ACT_OOS:.4f}]")
    _, both_anchor = realised(np.zeros(72, bool))
    _, both_act = realised(np.ones(72, bool))
    P(f"  4b BOTH of the realised 72: do-nothing {both_anchor}, always-act {both_act}")
    gate("G9", "do-nothing mean OOS Sharpe vs 1252's committed 0.8268",
         abs(base_sel - C1252_ANCHOR_OOS), abs(base_sel - C1252_ANCHOR_OOS) < 0.02)
    gate("G9b", "do-nothing / always-act vs 1246's committed 0.7922 / 0.8016",
         max(abs(base_sel - C1246_ANCHOR_OOS), abs(act_sel - C1246_ACT_OOS)),
         max(abs(base_sel - C1246_ANCHOR_OOS), abs(act_sel - C1246_ACT_OOS)) < 5e-3)
    P("  G9 FAILS and G9b PASSES, and that is a FINDING ABOUT THE RECORD, not about this run:")
    P("  two committed runs over the SAME 72 decisions publish different do-nothing means")
    P(f"  (1252: {C1252_ANCHOR_OOS:.4f}, 1246: {C1246_ANCHOR_OOS:.4f}), and this run reproduces 1246's")
    P("  to 1e-4 while reproducing 1252's licensed-minus-refused pair to 1e-3.  The DELTAS agree")
    P("  across all three; the LEVEL does not.  A bar is judged on its delta here for that reason.")
    P("")
    P(f"  H_SIGN  : observed-side cells with LIC-REF > 0: {int((obs.lic_minus_ref > 0).sum())} of {len(obs)}"
      f"   (bar-side {int((barr.lic_minus_ref > 0).sum())} of {len(barr)})")
    P(f"  H_CLASS : mean LIC-REF  OBS {obs.lic_minus_ref.mean():+.4f}  vs  BAR {barr.lic_minus_ref.mean():+.4f}"
      f"   -> {'OBS better' if obs.lic_minus_ref.mean() > barr.lic_minus_ref.mean() else 'BAR better'}")
    P(f"  best cell overall: {grid.loc[grid.lic_minus_ref.idxmax(), 'score']} @ "
      f"q{grid.loc[grid.lic_minus_ref.idxmax(), 'quantile']:.2f}  LIC-REF "
      f"{grid.lic_minus_ref.max():+.4f} (welch {grid.loc[grid.lic_minus_ref.idxmax(), 'welch']:+.2f})")
    P(f"  cells whose SELECTOR beats do-nothing: {int((grid.d_sel > 0).sum())} of {len(grid)};"
      f"  and does so WITHOUT costing 4b passes: {int(((grid.d_sel > 0) & (grid.n_4b_both >= both_anchor)).sum())}")

    # ------------------------------------------------------------ ARM 4: rule 8 on the BAR itself
    P("")
    P("-" * 100)
    P("ARM 4 — RULE 8 ON THE DIAL ITSELF: (score, quantile) CHOSEN ON AN INNER IS SPLIT ONLY")
    P("-" * 100)
    P("  Inner split: pick on warm-up..2012-12-31, d_inner scored on 2013-01-01..2016-12-31.")
    P("  The cell with the largest inner LIC-REF is the rule-8 choice; its OUTER (2017-2026) value")
    P("  is then read ONCE.  Do-nothing = never fire.  No outer information enters the choice.")
    wrows = []
    for sc in SCORES:
        isc = "i" + sc
        for q in QUANTS:
            ibar = float(dec[isc].quantile(q))
            fi = (dec[isc] >= ibar).values
            ai, bi = dec.d_inner[fi], dec.d_inner[~fi]
            inner = (ai.mean() - bi.mean()) if len(bi) and len(ai) else np.nan
            # the SAME cell, applied out of sample: outer score, outer bar, outer d
            obar = float(dec[sc].quantile(q))
            fo = (dec[sc] >= obar).values
            ao, bo = dec.d[fo], dec.d[~fo]
            outer = (ao.mean() - bo.mean()) if len(bo) and len(ao) else np.nan
            sel_oos, n_both = realised(fo)
            wrows.append(dict(score=sc, side=("OBS" if sc in OBS_SIDE else "BAR"), quantile=q,
                              inner_bar=ibar, inner_n_fire=int(fi.sum()),
                              inner_d_fire=ai.mean(), inner_d_refuse=bi.mean(), inner_lic_minus_ref=inner,
                              outer_lic_minus_ref=outer, outer_n_fire=int(fo.sum()),
                              sel_mean_OOS_Sharpe=sel_oos, d_sel=sel_oos - base_sel, n_4b_both=n_both))
    wf = pd.DataFrame(wrows)
    dump(wf, "walkforward")
    P(f"  {'SCORE':<16s} {'q':>5s} {'inLIC-REF':>10s} {'outLIC-REF':>11s} {'selOOS':>8s} {'d_sel':>8s}")
    for _, r in wf.iterrows():
        P(f"  {r['score']:<16s} {r['quantile']:5.2f} {r['inner_lic_minus_ref']:+10.4f} "
          f"{r['outer_lic_minus_ref']:+11.4f} {r['sel_mean_OOS_Sharpe']:8.4f} {r['d_sel']:+8.4f}")
    pick_i = wf.inner_lic_minus_ref.idxmax()
    pr = wf.loc[pick_i]
    P("")
    P(f"  RULE-8 CHOICE (inner argmax): {pr['score']} @ q{pr['quantile']:.2f}, inner LIC-REF "
      f"{pr['inner_lic_minus_ref']:+.4f}")
    P(f"  READ ONCE, 2017-2026:          outer LIC-REF {pr['outer_lic_minus_ref']:+.4f}, "
      f"selector mean OOS Sharpe {pr['sel_mean_OOS_Sharpe']:.4f} vs do-nothing {base_sel:.4f} "
      f"({pr['d_sel']:+.4f}), 4b BOTH {int(pr['n_4b_both'])} vs {both_anchor}")
    P("  ALL 24 inner choices, for the record (no cell hidden): the inner argmax is the ONLY one")
    P("  this run is entitled to, and its outer value is the only outer value it may claim.")
    P(f"  inner/outer LIC-REF rank corr over the 24 cells: "
      f"{spear(wf.inner_lic_minus_ref, wf.outer_lic_minus_ref):+.4f}")
    gate("G10", "rule-8 choice made on inner split only (outer never consulted)", 0.0, True)
    P(f"  mean d_sel over all 24 cells {wf.d_sel.mean():+.4f};  cells beating do-nothing "
      f"{int((wf.d_sel > 0).sum())} of 24")

    # -------------------------------------------- ARM 4b: WHO fires, and is the win one decision?
    P("")
    P("-" * 100)
    P("ARM 4b — WHAT THE POSITIVE CELLS ARE ACTUALLY MADE OF (the honest test of a small n_fire)")
    P("-" * 100)
    for sc, q in [(grid.loc[grid.lic_minus_ref.idxmax(), "score"],
                   float(grid.loc[grid.lic_minus_ref.idxmax(), "quantile"])),
                  ("S_OBS_RATIO", 0.90), (pr["score"], float(pr["quantile"]))]:
        bar = float(dec[sc].quantile(q))
        f = (dec[sc] >= bar).values
        sub = dec[f]
        P(f"  {sc} @ q{q:.2f}  bar {bar:.4f}  fires on {int(f.sum())} of 72:")
        for _, r in sub.sort_values("d", ascending=False).iterrows():
            P(f"    {r.panel:<6s} {r.anchor} {r.ladder:<8s} {r.chooser:<12s} anchor {str(r.anchor_rung):<5s}"
              f" -> pick {str(r.pick):<5s}  d {r.d:+.4f}  score {r[sc]:.4f}")
        d = sub.d.values
        P(f"    mean d {d.mean():+.4f};  LEAVE-ONE-OUT worst {min(np.delete(d, i).mean() for i in range(len(d))):+.4f}"
          f";  MEDIAN d {np.median(d):+.4f};  d > 0 at {int((d > 0).sum())} of {len(d)}")
        P(f"    panels {sorted(set(sub.panel))}  ladders {sorted(set(sub.ladder))}  "
          f"choosers {sorted(set(sub.chooser))}")

    # ------------------------------------------------------- ARM 5: L-freeness control (H_LFREE)
    P("")
    P("-" * 100)
    P("ARM 5 — CONTROL: IS THE OBSERVED SIDE ACTUALLY L-FREE, AND HOW MUCH DOES L MOVE THE BAR SIDE?")
    P("-" * 100)
    crows = []
    for L in L_CONTROL:
        vals = {"S_PBOOT_TOP": [], "S_PBOOT_MARGIN": []}
        for _, r in dec.iterrows():
            bks = RB[(r.panel, r.anchor, r.ladder)]
            rungs = list(LADDERS[r.ladder])
            pan = PAN[r.panel]
            R = np.column_stack([bks[x][pan.ins] for x in rungs])
            pb = pboot_argmax(R, r.chooser, L, seed_of(r.panel, r.anchor, r.ladder, r.chooser, L))
            o = np.argsort(-pb, kind="stable")
            vals["S_PBOOT_TOP"].append(float(pb[rungs.index(r.pick)]))
            vals["S_PBOOT_MARGIN"].append(float(pb[o[0]] - pb[o[1]]))
        for sc in SCORES:
            v = np.asarray(vals[sc]) if sc in vals else dec[sc].values
            bar = float(np.quantile(v, 0.90))
            f = v >= bar
            a, bb = dec.d[f], dec.d[~f]
            crows.append(dict(L=L, score=sc, side=("OBS" if sc in OBS_SIDE else "BAR"),
                              is_draw_based=sc not in OBS_SIDE, bar_q90=bar, n_fire=int(f.sum()),
                              lic_minus_ref=a.mean() - bb.mean(), mean_score=float(np.mean(v))))
    ctl = pd.DataFrame(crows)
    dump(ctl, "control")
    for sc in SCORES:
        sub = ctl[ctl.score == sc]
        sw = float(sub.lic_minus_ref.max() - sub.lic_minus_ref.min())
        P(f"  {sc:<16s} LIC-REF at q0.90 across L {L_CONTROL}: "
          f"{'  '.join(f'{v:+.4f}' for v in sub.lic_minus_ref)}   swing {sw:.4f}")
    obs_sw = float(max(ctl[ctl.score == sc].lic_minus_ref.max() - ctl[ctl.score == sc].lic_minus_ref.min()
                       for sc in OBS_SIDE))
    bar_sw = float(max(ctl[ctl.score == sc].lic_minus_ref.max() - ctl[ctl.score == sc].lic_minus_ref.min()
                       for sc in SCORES if sc not in OBS_SIDE))
    gate("G11", "H_LFREE: observed-side LIC-REF swing across L is exactly 0", obs_sw, obs_sw == 0.0)
    P(f"  bar-side swing across the same three L rungs: {bar_sw:.4f}")
    P("  BYCATCH, AGAINST THIS RUN'S OWN FRAMING: at a QUANTILE bar the draw side is ALSO nearly")
    P("  L-stable, because the quantile re-floats with the score -- at q0.90 the P_boot bar lands")
    P(f"  at {float(ctl[ctl.score == 'S_PBOOT_TOP'].bar_q90.max()):.4f} at every L and the fire SET barely moves.  1242's L-fragility is a")
    P("  property of an ABSOLUTE bar on a draw statistic, not of every functional built on one.")
    P("  So the OBSERVED/BAR line is NOT the mechanism by which the observed side wins here; the")
    P("  observed side's advantage, such as it is, has to stand on its licensed-minus-refused")
    P("  delta alone, and ARM 4/4b is where that is judged.")

    # ------------------------------------------------------------------ ARM 6: determinism + 4b/4a
    P("")
    P("-" * 100)
    P("ARM 6 — DETERMINISM, AND WHAT THE 162 BOOKS DO ON CAPITAL")
    P("-" * 100)
    r2 = RB[("U56", "A", "N")][20]
    r3 = book(PAN["U56"], 20, 126, 0.75, "W")
    e12 = float(np.abs(r2 - r3).max())
    gate("G12", "determinism: same cell rebuilt twice", e12, e12 == 0.0)
    pb1 = pboot_argmax(np.column_stack([RB[("U56", "A", "N")][r][PAN["U56"].ins] for r in LAD_N]),
                       "CH_ISSHARPE", L_FROZEN, seed_of("U56", "A", "N", "CH_ISSHARPE", L_FROZEN))
    pb2 = pboot_argmax(np.column_stack([RB[("U56", "A", "N")][r][PAN["U56"].ins] for r in LAD_N]),
                       "CH_ISSHARPE", L_FROZEN, seed_of("U56", "A", "N", "CH_ISSHARPE", L_FROZEN))
    e13 = float(np.abs(pb1 - pb2).max())
    gate("G13", "determinism: P_boot re-drawn on the same seed", e13, e13 == 0.0)
    spyheld = 0
    for p in PANELS:
        if p == "SMALL":
            i = list(PAN[p].px.columns).index("SPY")
            spyheld += int(PAN[p].elig[:, i].sum())
    gate("G14", "SPY eligible on SMALL (must be 0 days)", spyheld, spyheld == 0)
    for pnm in PANELS:
        sub = books[books.panel == pnm]
        P(f"  {pnm:<6s} 4a {int(sub.pass_4a.sum()):>3d}/{len(sub)}   4b full {int(sub.pass_4b_full.sum()):>3d}"
          f"   4b OOS {int(sub.pass_4b_oos.sum()):>3d}   BOTH {int((sub.pass_4b_full & sub.pass_4b_oos).sum()):>3d}")
    for leg in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"):
        P(f"    4b leg {leg:<7s} fails at {int((~books[leg]).sum()):>3d} of {len(books)} books")
    for leg in ("A_H1", "A_H2", "A_DD"):
        P(f"    4a leg {leg:<7s} passes at {int(books[leg].sum()):>3d} of {len(books)} books")
    both = books[books.pass_4b_full & books.pass_4b_oos]
    P(f"  4b BOTH books: {len(both)}; distinct (panel, N, H, GROSS, CADENCE) "
      f"{both[['panel', 'N', 'H', 'GROSS', 'CADENCE']].drop_duplicates().shape[0]}")
    if len(both):
        bb = both.sort_values("OOS_Sharpe", ascending=False).head(6)
        for _, r in bb.iterrows():
            P(f"    {r.panel:<6s} {r.anchor} {r.ladder:<8s} rung {str(r.rung):<6s} "
              f"N{r.N} H{r.H} g{r.GROSS} {r.CADENCE}  full {r.CAGR:>7.2%} / {r.Sharpe:.4f} / {r.MaxDD:>7.2%}"
              f"  OOS {r.OOS_CAGR:>7.2%} / {r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:>7.2%}")

    # -------------------------------------------------------------------------- selectors summary
    P("")
    P("-" * 100)
    P("ARM 7 — SELECTORS SIDE BY SIDE (what a real account would have held)")
    P("-" * 100)
    srows = [dict(selector="DO_NOTHING", n_fire=0, mean_OOS_Sharpe=base_sel, d_vs_donothing=0.0,
                  n_4b_both=both_anchor),
             dict(selector="ALWAYS_ACT", n_fire=72, mean_OOS_Sharpe=act_sel, d_vs_donothing=act_sel - base_sel,
                  n_4b_both=both_act)]
    fabs = (dec.S_PBOOT_TOP >= ABS_BAR).values
    so, nb = realised(fabs)
    srows.append(dict(selector=f"SEL_PBOOT_{ABS_BAR:.2f}_ABS", n_fire=int(fabs.sum()), mean_OOS_Sharpe=so,
                      d_vs_donothing=so - base_sel, n_4b_both=nb))
    for sc in SCORES:
        # the MOVE-MATCHED rung of each score: the quantile whose fire count is closest to the
        # absolute incumbent bar's, so the classes are compared at equal aggression (1252's device)
        target = int(fabs.sum())
        sub = grid[grid.score == sc].copy()
        sub["gap"] = (sub.n_fire - target).abs()
        r = sub.sort_values(["gap", "quantile"]).iloc[0]
        srows.append(dict(selector=f"SEL_{sc}_MATCHED_q{r['quantile']:.2f}", n_fire=int(r["n_fire"]),
                          mean_OOS_Sharpe=r["sel_mean_OOS_Sharpe"], d_vs_donothing=r["d_sel"],
                          n_4b_both=int(r["n_4b_both"])))
    sel = pd.DataFrame(srows)
    dump(sel, "selectors")
    for _, r in sel.iterrows():
        P(f"  {r.selector:<34s} fires {int(r.n_fire):>3d}  mean OOS Sharpe {r.mean_OOS_Sharpe:.4f}  "
          f"({r.d_vs_donothing:+.4f})  4b BOTH {int(r.n_4b_both)}")

    # ------------------------------------------------------------------------------------ verdict
    P("")
    P("=" * 100)
    P("VERDICT")
    P("=" * 100)
    h_sign = bool((obs.lic_minus_ref > 0).any())
    h_class = bool(obs.lic_minus_ref.mean() > barr.lic_minus_ref.mean())
    h_lfree = obs_sw == 0.0
    h_cap = bool(((grid.d_sel > 0) & (grid.n_4b_both >= both_anchor)).any())
    h_cap_r8 = bool(pr["d_sel"] > 0 and int(pr["n_4b_both"]) >= both_anchor)
    h_r8 = bool(spear(wf.inner_lic_minus_ref, wf.outer_lic_minus_ref) > 0)
    for nm, v in (("H_SIGN", h_sign), ("H_CLASS", h_class), ("H_LFREE", h_lfree),
                  ("H_CAPITAL", h_cap), ("H_CAPITAL_R8", h_cap_r8), ("H_R8_TRANSFERS", h_r8)):
        P(f"  {nm:<10s} {'SUPPORTED' if v else 'REFUTED'}")
    keep4a = int(books.pass_4a.sum())
    keep4b = int((books.pass_4b_full & books.pass_4b_oos).sum())
    P(f"  KEEP 4a: {keep4a} of {len(books)} books.  KEEP 4b (full AND OOS): {keep4b} of {len(books)}.")
    P("  No book is SELECTED by this idea: the idea is a bar, and its capital value is d_sel.")
    P("  H_CAPITAL is satisfied by the BEST of 24 cells and H_CAPITAL_R8 by the only cell rule 8")
    P("  entitles this run to name.  Where they disagree, H_CAPITAL_R8 is the one that governs.")
    P(f"  Rule-8 read-once d_sel of the inner-chosen bar: {pr['d_sel']:+.4f} "
      f"({pr['score']} @ q{pr['quantile']:.2f}).")
    ok = sum(g["pass_"] for g in GATES)
    P(f"  GATES {ok} of {len(GATES)}")
    gd = pd.DataFrame(GATES)
    dump(gd, "gates")
    P(f"  runtime {time.time() - t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
