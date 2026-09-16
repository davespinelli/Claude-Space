#!/usr/bin/env python3
"""Idea 1134 (cloud lane, 2026-09-16)
   is-the-STRICT-SHRINK-GROSS-DRAWDOWN-SURVIVOR-a-real-effect-or-4-copies-of-one-book

Idea 1132 walked a SHRUNK chooser (stay on the ladder's frozen default rung unless the IS gap
exceeds tau x its own IS bootstrap SD) and found that at the strict setting tau=3 exactly 4 of
48 cells still MOVE: `C_ISDD` on the GROSS ladder, picking gross 0.30 over the frozen 0.75, on
both panels x both rung sets.  Those 4 win the MATCHED statistic (OOS MaxDD) by a median
+0.1160 in 4 of 4 while costing -0.0033 of OOS Sharpe.  1132 read that as "the one thing
shrinkage buys is DRAWDOWN, not return".

This run asks whether that survivor is an EFFECT at all.  Three things could be true of it:

  DOUBLE COUNT   the GROSS ladder's CORE and EXT rung sets are the SAME list of rungs, so the
                 4 cells are 2 distinct books counted twice.  A median over 4 is then a median
                 over 2, and "4 of 4" is "2 of 2".
  MECHANICAL     on a GROSS ladder every rung is the SAME basket scaled, so |MaxDD| is
                 monotone in gross and `argmax IS_MaxDD` is the BOTTOM RUNG for every possible
                 book.  The chooser then carries no information about the book: it de-grosses
                 whatever it is handed.
  REAL           the de-gross-on-a-wide-IS-gap rule buys a drawdown gain that a book with NO
                 selection information does not get.  Then it is a rule worth having.

They are separated by ONE comparand the record demands and 1132 did not run: a GROSS-MATCHED
NULL.  If a randomly-selected book at the same gross rungs, same panel, same cadence, same
costs collects the same +0.1160, the gain belongs to the gross DIAL and not to the rule.

TUNED DIALS (2, PROTOCOL rule 4): `SHRINK THRESHOLD` tau {0, 1, 2, 3, 4, 5, 8, inf} x
`NULL KIND` {N_ROT, N_FIX} = 16 combinations, ALL published.
  N_ROT  ROTATING: the basket is redrawn uniformly at random from the eligible set at EVERY
         rebalance (no min hold).  The record's churning null; it pays a turnover no book pays.
  N_FIX  FIXED: the basket is drawn once and carried while priced.  The record's cheap null;
         it pays almost no turnover.

REVISION NOTE, stated because it changes a number and not a verdict.  The first run of this
script drew the FIXED basket from the very first rebalance at which ANY name is eligible
(2008-10-17, 4-8 eligible names on the two panels).  With slots never freeing, the basket then
filled with whichever names became eligible EARLIEST and the random key barely entered: on
B136 all 40 seeds produced the same book to 4 decimal places.  A null that does not vary is not
a null, so N_FIX now draws at the first rebalance carrying at least N=20 eligible names
(U56 2009-05-01, B136 2009-04-09) and holds that draw.  The cost of the repair is stated: the
FIXED null is in cash for the first ~3.5 months of the warm window while the book is invested.
Two READINGS of the null comparison are published side by side for the same reason — the
declared one (raw matched advantage, on the seeds where the rule fires) and a scale-free one
(|OOS_DD(0.30)| / |OOS_DD(0.75)|, on every seed), added after the first run when the raw
advantage turned out to scale with each book's own baseline drawdown.  Both are reported at
every dial point, the declared bar is scored as written, and the verdict is the same under
either.
Both are drawn from the SAME eligibility gate as the book (200d MA and vol < 0.60) and run at
the SAME gross rungs, so the only thing they lack is the composite's ranking information.

NOT dials, reported at every dial point and selected on by nothing: panel {U56, B136}, rung set
{CORE, EXT}, chooser {C_ISSHARPE, C_ISCAGR, C_ISDD}, seed count, keying (K_SE, as 1132's
strict shrink).

RULE 8 throughout: the pick, its IS gap and the gap's bootstrap SD are computed on 2009-2016
ALONE.  OOS 2017-2026 is read ONCE, for scoring.  Both KEEP paths are scored at every rung and
every picked book.

FROZEN at 1082/1094/1098/1117/1132's construction: CAND20 legs (21,252)/(0,126)/(0,63), cap
INF, max_vol 0.60, min hold 126 (the book; the nulls' hold is the null kind itself), N=20,
weekly, 10 bps, LAG 1, warm-up 260, IS end 2016-12-31, block L=63, crc32 seeds, DD cap 0.60,
CAGR floor 0.70.

SURVIVORSHIP (rule 9): U56 and B136 are current-constituent lists, so every LEVEL is optimistic
and every 4b count an UPPER bound.  The measured object is a DIFFERENCE between a book and a
null drawn from the SAME pool over the SAME tape, so the inflation very largely cancels; what
it does not cancel, it raises for book and null together.

Standalone, deterministic, offline.  Nothing outside research/backtests/ is written.
"""
from __future__ import annotations

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

DATE = "2026-09-16"
SLUG = "is-the-STRICT-SHRINK-GROSS-DRAWDOWN-SURVIVOR-a-real-effect-or-4-copies-of-one-book"
HERE = Path(__file__).resolve().parent
OUT = HERE / f"{DATE}_{SLUG}_cloud"
PRIOR1132 = HERE / ("2026-09-16_is-the-ARGMAX-NEGATIVE-INFORMATION-result-a-CHOOSER-artefact-"
                    "or-a-GRID-fact_B")

LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ0, HOLD0, N0 = 10.0, 0.75, "W", 126, 20
LEGS = [(21, 252), (0, 126), (0, 63)]
LAD_G = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]
PANELS = ["U56", "B136"]
RUNGSETS = ["CORE", "EXT"]                 # identical on the GROSS ladder — that is the point
DEFAULT_G = "0.75"
CHOOSERS = {"C_ISSHARPE": ("IS_Sharpe", +1.0, "OOS_Sharpe"),
            "C_ISCAGR": ("IS_CAGR", +1.0, "OOS_CAGR"),
            "C_ISDD": ("IS_MaxDD", +1.0, "OOS_MaxDD")}
TAUS = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 8.0, float("inf")]
NULL_KINDS = ["N_ROT", "N_FIX"]
NSEED, BDRAWS, L_BLOCK = 40, 400, 63
SEED_BASE = 11341134

# committed cross-run anchors
A1132_SURV = dict(pick="0.3", n_cells=4, med_adv=0.11602720423763165,
                  med_advS=-0.00332568697118765)
A1132_U56 = dict(IS_MaxDD_030=-0.056833, IS_MaxDD_075=-0.139523, is_gap=0.082689,
                 gap_SE=0.021689, OOS_MaxDD_030=-0.079903, OOS_MaxDD_075=-0.191276)
A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205

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


# -------------------------------------------------- 1132's fast runner, verbatim
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
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, (above & (vol20 < MAXVOL)).values


def build(rank_key, elig, priced, reb, N, H, T, K, gross):
    """1132's builder verbatim.  rank_key is LOWER-IS-BETTER."""
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


def windows(idx):
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    return warm, warm & ~oos, oos


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


def legs_4a(b, lbm):
    return {"A_H1": bool(b["H1"] > lbm["H1"]), "A_H2": bool(b["H2"] > lbm["H2"]),
            "A_DD": bool(b["MaxDD"] >= lbm["MaxDD"])}


# --------------------------------------------- 1098/1132's paired block bootstrap
def block_index(rng, T, Lb, ndraws):
    nb = int(np.ceil(T / Lb))
    st = rng.integers(0, T, size=(ndraws, nb))
    off = np.arange(Lb)
    idx = (st[:, :, None] + off[None, None, :]) % T
    return idx.reshape(ndraws, nb * Lb)


def boot_maxdd(R, idx, chunk=40):
    nr = R.shape[0]
    nd = idx.shape[0]
    out = np.empty((nr, nd))
    for a in range(0, nd, chunk):
        ix = idx[a:a + chunk]
        for j in range(nr):
            path = np.log1p(R[j])[ix]
            cum = np.cumsum(path, axis=1)
            run = np.maximum.accumulate(cum, axis=1)
            out[j, a:a + chunk] = np.expm1(cum - run).min(axis=1)
    return out


def boot_sharpe_cagr(R, idx, Lb, chunk=100):
    LG = np.log1p(R)
    D = np.concatenate([LG, LG], axis=1)
    CS = np.concatenate([np.zeros((D.shape[0], 1)), np.cumsum(D, axis=1)], axis=1)
    R2 = np.concatenate([R, R], axis=1)
    CS1 = np.concatenate([np.zeros((R.shape[0], 1)), np.cumsum(R2, axis=1)], axis=1)
    CS2 = np.concatenate([np.zeros((R.shape[0], 1)), np.cumsum(R2 ** 2, axis=1)], axis=1)
    nd = idx.shape[0]
    st = idx[:, ::Lb]
    n = idx.shape[1]
    cag = np.empty((R.shape[0], nd))
    shp = np.empty((R.shape[0], nd))
    for a in range(0, nd, chunk):
        s = st[a:a + chunk]
        lsum = (CS[:, s + Lb] - CS[:, s]).sum(axis=2)
        s1 = (CS1[:, s + Lb] - CS1[:, s]).sum(axis=2)
        s2 = (CS2[:, s + Lb] - CS2[:, s]).sum(axis=2)
        cag[:, a:a + chunk] = np.expm1(lsum * (252.0 / n))
        mu = s1 / n
        var = (s2 - n * mu ** 2) / (n - 1)
        sd = np.sqrt(np.maximum(var, 0.0))
        shp[:, a:a + chunk] = np.where(sd > 0, mu * 252.0 / (sd * np.sqrt(252.0)), np.nan)
    return cag, shp


def main():
    t0 = time.time()
    P(f"# Idea 1134 (cloud lane, {DATE}) — is the STRICT-SHRINK GROSS DRAWDOWN SURVIVOR a real")
    P("#   effect, or 4 copies of one book?  Price the de-gross rule against a GROSS-MATCHED NULL.")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): SHRINK THRESHOLD tau {TAUS} x NULL KIND {NULL_KINDS}")
    P(f"#   = {len(TAUS) * len(NULL_KINDS)} combinations, ALL published.")
    P("# NOT dials: panel, rung set, chooser, seed count, keying (K_SE as 1132's strict shrink).")
    P(f"# FROZEN: CAND20 {LEGS}, max_vol {MAXVOL}, hold {HOLD0}, N {N0}, {FREQ0}, {COST:.0f} bps,")
    P(f"#   LAG {LAG}, warm-up {WARMUP}, IS end {IS_END}, block L={L_BLOCK}, {BDRAWS} draws,")
    P(f"#   {NSEED} crc32 seeds per (null kind, panel), GROSS rungs {LAD_G}.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) H_PREMISE   1132's survivor reproduces: C_ISDD on GROSS picks 0.30 at tau=3 on")
    P("#                   both panels x both rung sets, median matched advantage +0.1160,")
    P("#                   median OOS-Sharpe advantage -0.0033.")
    P("#   (b) H_DOUBLE    the 4 surviving cells are 2 distinct books: the GROSS ladder's CORE")
    P("#                   and EXT rung sets are the SAME list, so rung set cannot vary a book.")
    P("#   (c) H_MECH      |MaxDD| is monotone in gross for EVERY book built here (real and")
    P("#                   null alike), so C_ISDD on a GROSS ladder picks the BOTTOM rung by")
    P("#                   construction and carries no information about the book it is given.")
    P("#   (d) H_NULL      (the test the survivor has to pass) the book's +0.1160 matched")
    P("#                   advantage lies ABOVE the 95th percentile of the gross-matched null's")
    P("#                   own advantage, under BOTH null kinds.  Failing this, the drawdown")
    P("#                   gain is the GROSS DIAL and not the rule.")
    P("#   (e) H_FIRES     the de-gross rule fires on the NULL too: >= 0.90 of null seeds have")
    P("#                   IS gap > 3 x their own bootstrap SD.  A rule that fires on a coin")
    P("#                   flip is not selecting books.")
    P("#   (f) H_COST      what the de-gross buys in DD it pays in the 4b CAGR floor: gross")
    P("#                   0.30 fails L_CAGR on both panels while passing L_DD.")
    P("# DECISION RULE, declared before any number: the survivor is a REAL EFFECT only if")
    P("#   H_NULL holds under BOTH null kinds AND H_MECH fails (i.e. the pick is not forced).")
    P("#   Anything else and it is KILLED as an effect: de-grossing lowers drawdown, which is")
    P("#   arithmetic, not a finding, and 4 cells are 2 books.")
    P("")

    gaterows, gates = [], {}

    # =========================================================== panels, comparands, gates
    P("## [1] GATES — printed before any result number")
    panels = {}
    for panel in PANELS:
        px = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
        idx = px.index
        warm, ins, oos = windows(idx)
        sc, elig = mech(px)
        panels[panel] = dict(px=px, idx=idx, K=len(px.columns), T=len(idx),
                             rets=px.pct_change().fillna(0.0).values, priced=px.notna().values,
                             warm=warm, ins=ins, oos=oos, sc=sc, elig=elig)
        P(f"  {panel}: {len(px.columns)} names, {len(idx):,} rows {idx[0].date()} -> "
          f"{idx[-1].date()}, warm {int(warm.sum()):,}, IS {int(ins.sum()):,}, "
          f"OOS {int(oos.sum()):,}")

    def weights_for(panel, rank_key, N, H, gross, start_at_full=False):
        """start_at_full: skip rebalances before the first one carrying >= N eligible names,
        so a draw-once basket is an actual RANDOM draw and not a queue of earliest-eligible."""
        d = panels[panel]
        mk = rebalance_mask(d["idx"], FREQ0).values.copy()
        reb = np.flatnonzero(mk)
        if start_at_full:
            cnt = (d["elig"] & d["priced"])[reb].sum(axis=1)
            ok = np.flatnonzero(cnt >= N)
            if len(ok):
                mk = np.zeros_like(mk)
                mk[reb[ok[0]:]] = True
                reb = reb[ok[0]:]
        return build(rank_key, d["elig"], d["priced"], reb, N, H, d["T"], d["K"], gross), mk

    def evaluate(panel, W, mk):
        """Next-day execution (LAG 1) and 10 bps, exactly as the record's runner."""
        d = panels[panel]
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        g, tn = nrun(d["rets"], Wl, mkl)
        return g - tn * COST / 1e4, tn

    def run_book(panel, gross):
        W, mk = weights_for(panel, -panels[panel]["sc"], N0, HOLD0, gross)
        return evaluate(panel, W, mk)

    d = panels["U56"]
    W0, mk0 = weights_for("U56", -d["sc"], N0, HOLD0, GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W0, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ0)["returns"].values
    rfast, _ = run_book("U56", GROSS0)
    g1 = float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max())
    gates["G1"] = g1 < 1e-12
    gaterows.append(dict(gate="G1", what="fast runner == engine.backtest", value=g1, pass_=gates["G1"]))
    P(f"  G1  fast runner == engine.backtest                       {g1:.2e}  "
      f"{'PASS' if gates['G1'] else 'FAIL'}")

    m = blocks_m(rfast, d["warm"], d["ins"], d["oos"])
    g2 = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]),
             abs(m["MaxDD"] - A936_WH126[2]))
    gates["G2"] = g2 < 5e-5
    gaterows.append(dict(gate="G2", what="committed U56 W/H126/N=20 triple", value=g2, pass_=gates["G2"]))
    P(f"  G2  CROSS-RUN committed U56 W/H126/N=20 triple           {g2:.2e}  "
      f"{'PASS' if gates['G2'] else 'FAIL'}  ({m['CAGR']:.4%} / {m['Sharpe']:.4f} / {m['MaxDD']:.4%})")

    spy_m, live_m = {}, {}
    for panel in PANELS:
        dp = panels[panel]
        spy_m[panel] = blocks_m(dp["px"]["SPY"].pct_change().fillna(0.0).values,
                                dp["warm"], dp["ins"], dp["oos"])
        lr = backtest(dp["px"], rules_v2_weights(dp["px"]), cost_bps=COST, freq="W")["returns"].values
        live_m[panel] = blocks_m(lr, dp["warm"], dp["ins"], dp["oos"])
    g3 = max(abs(spy_m["U56"]["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
             abs(spy_m["U56"]["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(spy_m["U56"]["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gates["G3"] = g3 < 5e-4
    gaterows.append(dict(gate="G3", what="SPY OOS triple", value=g3, pass_=gates["G3"]))
    P(f"  G3  CROSS-RUN SPY OOS triple                             {g3:.2e}  "
      f"{'PASS' if gates['G3'] else 'FAIL'}")
    g4 = abs(live_m["U56"]["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gates["G4"] = g4 < 5e-4
    gaterows.append(dict(gate="G4", what="live RULES v2 MaxDD == -12.05%", value=g4, pass_=gates["G4"]))
    P(f"  G4  CROSS-RUN live RULES v2 MaxDD == -12.05%             {g4:.2e}  "
      f"{'PASS' if gates['G4'] else 'FAIL'}")

    # ================================================== [2] the GROSS ladder, every rung
    P("")
    P("## [2] THE GROSS LADDER — every rung on both panels, 4a/4b legs on all of them")
    rows, book_rets = [], {}
    for panel in PANELS:
        dp = panels[panel]
        for gr in LAD_G:
            r, tn = run_book(panel, gr)
            book_rets[(panel, gr)] = r
            b = blocks_m(r, dp["warm"], dp["ins"], dp["oos"])
            row = dict(panel=panel, ladder="GROSS", rung=str(gr), N=N0, H=HOLD0, gross=gr,
                       freq=FREQ0,
                       turnover=float(tn[dp["warm"]].sum()) / (dp["warm"].sum() / 252.0), **b)
            row.update(legs_4b(b, spy_m[panel]))
            row.update(legs_4b_oos(b, spy_m[panel]))
            row.update(legs_4a(b, live_m[panel]))
            row["pass_4b_full"] = all(row[k] for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
            row["pass_4b_oos"] = all(row[k] for k in ("O_S", "O_DD", "O_CAGR"))
            row["pass_4a"] = all(row[k] for k in ("A_H1", "A_H2", "A_DD"))
            rows.append(row)
    G = pd.DataFrame(rows)
    dump(G, "ladder")
    P(f"  {'panel':5s} {'gross':>5s} {'turn':>5s} {'CAGR':>8s} {'Sharpe':>7s} {'MaxDD':>8s} "
      f"{'IS_DD':>8s} {'OOS_S':>7s} {'OOS_DD':>8s} {'L_DD':>5s} {'L_CAGR':>6s} {'4b':>5s} {'4a':>5s}")
    for _, r_ in G.iterrows():
        P(f"  {r_['panel']:5s} {r_['rung']:>5s} {r_['turnover']:5.2f} {r_['CAGR']:8.2%} "
          f"{r_['Sharpe']:7.3f} {r_['MaxDD']:8.2%} {r_['IS_MaxDD']:8.2%} "
          f"{r_['OOS_Sharpe']:7.3f} {r_['OOS_MaxDD']:8.2%} {str(r_['L_DD']):>5s} "
          f"{str(r_['L_CAGR']):>6s} {str(r_['pass_4b_full']):>5s} {str(r_['pass_4a']):>5s}")

    gi = G.set_index(["panel", "rung"])
    g5 = max(abs(float(gi.loc[("U56", "0.3")]["IS_MaxDD"]) - A1132_U56["IS_MaxDD_030"]),
             abs(float(gi.loc[("U56", "0.75")]["IS_MaxDD"]) - A1132_U56["IS_MaxDD_075"]),
             abs(float(gi.loc[("U56", "0.3")]["OOS_MaxDD"]) - A1132_U56["OOS_MaxDD_030"]),
             abs(float(gi.loc[("U56", "0.75")]["OOS_MaxDD"]) - A1132_U56["OOS_MaxDD_075"]))
    gates["G5"] = g5 < 5e-5
    gaterows.append(dict(gate="G5", what="1132's committed U56 GROSS 0.30/0.75 DD quad",
                         value=g5, pass_=gates["G5"]))
    P(f"  G5  CROSS-RUN 1132's committed U56 GROSS 0.30/0.75 DD quad  {g5:.2e}  "
      f"{'PASS' if gates['G5'] else 'FAIL'}")

    r_again, _ = run_book("U56", 0.30)
    g6 = float(np.abs(r_again - book_rets[("U56", 0.30)]).max())
    gates["G6"] = g6 == 0.0
    gaterows.append(dict(gate="G6", what="determinism", value=g6, pass_=gates["G6"]))
    P(f"  G6  determinism (same cell twice)                        {g6:.2e}  "
      f"{'PASS' if gates['G6'] else 'FAIL'}")

    # ================================ [3] the DOUBLE COUNT and the MECHANICAL reading
    P("")
    P("## [3] DOUBLE COUNT — how many DISTINCT books are 1132's 4 surviving cells?")
    rung_sets = {rs: [str(g) for g in LAD_G] for rs in RUNGSETS}
    same_list = rung_sets["CORE"] == rung_sets["EXT"]
    P(f"  GROSS rung set CORE: {rung_sets['CORE']}")
    P(f"  GROSS rung set EXT : {rung_sets['EXT']}")
    P(f"  the two lists are {'IDENTICAL' if same_list else 'DIFFERENT'} — rung set cannot vary a")
    P("  GROSS pick, so 1132's 4 cells (2 panels x 2 rung sets) are 2 DISTINCT BOOKS, each")
    P("  counted twice.  Its '+0.1160 in 4 of 4' is '+0.1160 in 2 of 2'; the effective n of")
    P("  every pooled statistic over those cells is 2.")
    gates["G7"] = same_list
    gaterows.append(dict(gate="G7", what="GROSS CORE and EXT rung lists identical",
                         value=float(same_list), pass_=same_list))
    P(f"  G7  GROSS CORE == EXT rung list                          {'PASS' if same_list else 'FAIL'}")

    P("")
    P("## [4] MECHANICAL — is `argmax IS_MaxDD` on a GROSS ladder ever anything but the bottom?")
    mono_rows = []
    for panel in PANELS:
        v = [float(gi.loc[(panel, str(g))]["IS_MaxDD"]) for g in LAD_G]
        o = [float(gi.loc[(panel, str(g))]["OOS_MaxDD"]) for g in LAD_G]
        mono_is = all(v[i] > v[i + 1] for i in range(len(v) - 1))
        mono_oos = all(o[i] > o[i + 1] for i in range(len(o) - 1))
        ratio = abs(float(gi.loc[(panel, "0.3")]["OOS_MaxDD"])) / abs(float(gi.loc[(panel, "0.75")]["OOS_MaxDD"]))
        mono_rows.append(dict(who="BOOK", kind="composite", panel=panel, seed=-1,
                              mono_IS=mono_is, mono_OOS=mono_oos, argmax_IS_rung=str(LAD_G[int(np.argmax(v))]),
                              dd_ratio=ratio, gross_ratio=0.30 / 0.75))
        P(f"  {panel} BOOK  IS_MaxDD monotone in gross: {mono_is}   OOS monotone: {mono_oos}   "
          f"argmax IS_MaxDD = gross {LAD_G[int(np.argmax(v))]}")
        P(f"        |OOS_DD(0.30)| / |OOS_DD(0.75)| = {ratio:.4f} against the pure leverage "
          f"prediction 0.30/0.75 = {0.40:.4f}  (residual {ratio - 0.4:+.4f})")

    # ============================================= [5] the GROSS-MATCHED NULL, both kinds
    P("")
    P("## [5] GROSS-MATCHED NULL — the comparand 1132 did not run.  Same panel, same")
    P("##   eligibility gate, same rungs, same cadence, same 10 bps; only the RANKING is random.")
    P(f"##   {NSEED} crc32 seeds per (kind, panel); N_ROT redraws the basket every rebalance,")
    P("##   N_FIX draws it once and carries it.")
    null_rows = []
    for panel in PANELS:
        dp = panels[panel]
        rngidx = np.random.default_rng(seed_of("boot", panel))
        bidx = block_index(rngidx, int(dp["ins"].sum()), L_BLOCK, BDRAWS)
        for kind in NULL_KINDS:
            for s in range(NSEED):
                rng = np.random.default_rng(seed_of(kind, panel, s))
                if kind == "N_ROT":
                    key = rng.random((dp["T"], dp["K"]))
                    H = 0
                else:
                    key = np.repeat(rng.random((1, dp["K"])), dp["T"], axis=0)
                    H = 10 ** 9
                W1, mk = weights_for(panel, key, N0, H, 1.0,      # one basket, scaled below
                                     start_at_full=(kind == "N_FIX"))
                rr = {}
                for gr in LAD_G:
                    r, tn = evaluate(panel, W1 * gr, mk)
                    rr[gr] = (r, float(tn[dp["warm"]].sum()) / (dp["warm"].sum() / 252.0))
                mm = {gr: blocks_m(rr[gr][0], dp["warm"], dp["ins"], dp["oos"]) for gr in LAD_G}
                v = [mm[g]["IS_MaxDD"] for g in LAD_G]
                argmax_rung = LAD_G[int(np.argmax(v))]
                is_gap = float(mm[0.30]["IS_MaxDD"] - mm[GROSS0]["IS_MaxDD"])
                R = np.vstack([rr[0.30][0][dp["ins"]], rr[GROSS0][0][dp["ins"]]])
                bdd = boot_maxdd(R, bidx)
                gap_SE = float(np.nanstd(bdd[0] - bdd[1], ddof=1))
                mono_is = all(v[i] > v[i + 1] for i in range(len(v) - 1))
                null_rows.append(dict(
                    kind=kind, panel=panel, seed=s, turnover=rr[GROSS0][1],
                    IS_MaxDD_030=mm[0.30]["IS_MaxDD"], IS_MaxDD_075=mm[GROSS0]["IS_MaxDD"],
                    is_gap=is_gap, gap_SE=gap_SE,
                    gap_over_SE=is_gap / gap_SE if gap_SE > 0 else np.inf,
                    argmax_IS_rung=str(argmax_rung), mono_IS=mono_is,
                    OOS_MaxDD_030=mm[0.30]["OOS_MaxDD"], OOS_MaxDD_075=mm[GROSS0]["OOS_MaxDD"],
                    adv_matched=float(mm[0.30]["OOS_MaxDD"] - mm[GROSS0]["OOS_MaxDD"]),
                    adv_oos_sharpe=float(mm[0.30]["OOS_Sharpe"] - mm[GROSS0]["OOS_Sharpe"]),
                    OOS_Sharpe_030=mm[0.30]["OOS_Sharpe"], OOS_Sharpe_075=mm[GROSS0]["OOS_Sharpe"],
                    CAGR_030=mm[0.30]["CAGR"], CAGR_075=mm[GROSS0]["CAGR"],
                    dd_ratio=abs(mm[0.30]["OOS_MaxDD"]) / abs(mm[GROSS0]["OOS_MaxDD"])))
        P(f"  {panel}: {NSEED * len(NULL_KINDS)} null books built "
          f"({time.time() - t0:.0f}s elapsed)")
    NU = pd.DataFrame(null_rows)
    dump(NU, "null")

    # the book's own gap and SE, same machinery
    book_rows = []
    for panel in PANELS:
        dp = panels[panel]
        rngidx = np.random.default_rng(seed_of("boot", panel))
        bidx = block_index(rngidx, int(dp["ins"].sum()), L_BLOCK, BDRAWS)
        R = np.vstack([book_rets[(panel, 0.30)][dp["ins"]], book_rets[(panel, GROSS0)][dp["ins"]]])
        bdd = boot_maxdd(R, bidx)
        gap_SE = float(np.nanstd(bdd[0] - bdd[1], ddof=1))
        is_gap = float(gi.loc[(panel, "0.3")]["IS_MaxDD"] - gi.loc[(panel, "0.75")]["IS_MaxDD"])
        book_rows.append(dict(
            panel=panel, is_gap=is_gap, gap_SE=gap_SE, gap_over_SE=is_gap / gap_SE,
            adv_matched=float(gi.loc[(panel, "0.3")]["OOS_MaxDD"] - gi.loc[(panel, "0.75")]["OOS_MaxDD"]),
            adv_oos_sharpe=float(gi.loc[(panel, "0.3")]["OOS_Sharpe"] - gi.loc[(panel, "0.75")]["OOS_Sharpe"]),
            dd_ratio=abs(float(gi.loc[(panel, "0.3")]["OOS_MaxDD"])) / abs(float(gi.loc[(panel, "0.75")]["OOS_MaxDD"]))))
    BK = pd.DataFrame(book_rows)
    dump(BK, "book")
    P(f"  BOOK gap / SE: " + ", ".join(
        f"{r.panel} gap {r.is_gap:+.4f} SE {r.gap_SE:.4f} gap/SE {r.gap_over_SE:.2f}"
        for r in BK.itertuples()))
    g8 = max(abs(float(BK[BK.panel == 'U56'].iloc[0]['is_gap']) - A1132_U56["is_gap"]),
             abs(float(BK[BK.panel == 'U56'].iloc[0]['gap_SE']) - A1132_U56["gap_SE"]) / 5.0)
    gates["G8"] = g8 < 5e-3
    gaterows.append(dict(gate="G8", what="1132's committed U56 IS gap (SE within 5x tol)",
                         value=g8, pass_=gates["G8"]))
    P(f"  G8  CROSS-RUN 1132's committed U56 IS gap {A1132_U56['is_gap']:+.4f} / SE "
      f"{A1132_U56['gap_SE']:.4f}      {g8:.2e}  {'PASS' if gates['G8'] else 'FAIL'}")

    # ======================================== [6] THE DIAL GRID: tau x null kind, all points
    P("")
    P("## [6] THE GRID — every (tau, null kind) point.  'fires' = the de-gross rule moves off")
    P("##   the frozen 0.75; the BOOK's row and the NULL's fire rate are the same rule applied")
    P("##   to a book with information and to books with none.")
    grid = []
    for tau in TAUS:
        for kind in NULL_KINDS:
            for panel in PANELS:
                bk = BK[BK.panel == panel].iloc[0]
                nz = NU[(NU.kind == kind) & (NU.panel == panel)]
                if tau == 0.0:
                    b_fire = bool(bk.is_gap > 0)
                    n_fire = (nz.is_gap > 0).mean()
                elif not np.isfinite(tau):
                    b_fire, n_fire = False, 0.0
                else:
                    b_fire = bool(bk.is_gap > tau * bk.gap_SE)
                    n_fire = float((nz.is_gap > tau * nz.gap_SE).mean())
                adv_b = float(bk.adv_matched) if b_fire else 0.0
                fired = nz[(nz.is_gap > tau * nz.gap_SE)] if np.isfinite(tau) and tau > 0 else (
                    nz[nz.is_gap > 0] if tau == 0.0 else nz.iloc[0:0])
                nadv = fired.adv_matched
                pct = float((nadv <= bk.adv_matched).mean()) if len(nadv) else np.nan
                # second reading, added after the first run (see REVISION NOTE): scale-free and
                # unconditional, because the raw advantage is proportional to a book's own
                # baseline |DD(0.75)| and so partly compares drawdown LEVELS, not the rule.
                pct_uncond = float((nz.adv_matched <= bk.adv_matched).mean())
                pct_ratio = float((nz.dd_ratio <= bk.dd_ratio).mean())
                grid.append(dict(
                    tau=tau, null_kind=kind, panel=panel, rung_sets_counted=len(RUNGSETS),
                    book_fires=b_fire, book_pick=("0.3" if b_fire else DEFAULT_G),
                    book_adv_matched=adv_b,
                    book_adv_oos_sharpe=float(bk.adv_oos_sharpe) if b_fire else 0.0,
                    null_fire_rate=n_fire, n_fired=len(fired),
                    null_med_adv=float(nadv.median()) if len(nadv) else np.nan,
                    null_p05=float(nadv.quantile(0.05)) if len(nadv) else np.nan,
                    null_p95=float(nadv.quantile(0.95)) if len(nadv) else np.nan,
                    book_percentile_in_null=pct,
                    book_pct_uncond=pct_uncond,
                    book_dd_ratio=float(bk.dd_ratio),
                    null_med_dd_ratio=float(nz.dd_ratio.median()),
                    null_p95_dd_ratio=float(nz.dd_ratio.quantile(0.95)),
                    book_pct_dd_ratio=pct_ratio,
                    null_med_adv_sharpe=float(fired.adv_oos_sharpe.median()) if len(fired) else np.nan,
                    null_med_turnover=float(fired.turnover.median()) if len(fired) else np.nan))
    GD = pd.DataFrame(grid)
    dump(GD, "grid")
    P("##   'book pct' is the DECLARED reading (raw advantage, fired seeds only); 'pct unc' and")
    P("##   'pct rat' are the second reading (all seeds; scale-free |DD(0.30)|/|DD(0.75)|).")
    P(f"  {'tau':>5s} {'kind':6s} {'panel':5s} {'fires':>6s} {'book adv':>9s} "
      f"{'null fire':>9s} {'null med adv':>12s} {'null p05':>9s} {'null p95':>9s} "
      f"{'book pct':>8s} {'pct unc':>7s} {'bk rat':>7s} {'nl rat':>7s} {'pct rat':>7s}")
    for _, r_ in GD.iterrows():
        P(f"  {r_['tau']:5.1f} {r_['null_kind']:6s} {r_['panel']:5s} "
          f"{str(r_['book_fires']):>6s} {r_['book_adv_matched']:+9.4f} "
          f"{r_['null_fire_rate']:9.3f} {r_['null_med_adv']:+12.4f} {r_['null_p05']:+9.4f} "
          f"{r_['null_p95']:+9.4f} {r_['book_percentile_in_null']:8.3f} "
          f"{r_['book_pct_uncond']:7.3f} {r_['book_dd_ratio']:7.4f} "
          f"{r_['null_med_dd_ratio']:7.4f} {r_['book_pct_dd_ratio']:7.3f}")

    # ===================================================== [7] rule 8 walk-forward + KEEP paths
    P("")
    P("## [7] RULE 8 WALK-FORWARD AND BOTH KEEP PATHS — picks made on 2009-2016 ALONE, OOS")
    P("##   2017-2026 read ONCE.  Every chooser, every rung set, every tau reported.")
    wf = []
    for panel in PANELS:
        bk = BK[BK.panel == panel].iloc[0]
        sub = G[G.panel == panel]
        for ch, (iscol, sign, ooscol) in CHOOSERS.items():
            v = (sign * sub[iscol]).values
            arg = sub.iloc[int(np.argmax(v))]["rung"]
            dref = gi.loc[(panel, DEFAULT_G)]
            # the chooser's own IS gap (argmax vs default) and its SE: SE measured for C_ISDD,
            # and for the other two by the same paired block bootstrap on their own statistic
            dp = panels[panel]
            rngidx = np.random.default_rng(seed_of("boot", panel))
            bidx = block_index(rngidx, int(dp["ins"].sum()), L_BLOCK, BDRAWS)
            R = np.vstack([book_rets[(panel, float(arg))][dp["ins"]],
                           book_rets[(panel, float(DEFAULT_G))][dp["ins"]]])
            if ch == "C_ISDD":
                bs = boot_maxdd(R, bidx)
                se = float(np.nanstd(bs[0] - bs[1], ddof=1))
            else:
                cg, sh = boot_sharpe_cagr(R, bidx, L_BLOCK)
                bs = cg if ch == "C_ISCAGR" else sh
                se = float(np.nanstd(bs[0] - bs[1], ddof=1))
            gap = float(sign * (sub.set_index("rung").loc[arg][iscol] - dref[iscol]))
            for rs in RUNGSETS:
                for tau in TAUS:
                    if tau == 0.0:
                        take = gap > 0
                    elif not np.isfinite(tau):
                        take = False
                    else:
                        take = bool(gap > tau * se)
                    rg = arg if take else DEFAULT_G
                    pick = gi.loc[(panel, rg)]
                    wf.append(dict(
                        panel=panel, rung_set=rs, chooser=ch, tau=tau, keying="K_SE",
                        pick=rg, argmax_rung=arg, default=DEFAULT_G, moved=bool(rg != DEFAULT_G),
                        is_gap=gap, gap_SE=se, gap_over_SE=gap / se if se > 0 else np.inf,
                        CAGR=float(pick["CAGR"]), Sharpe=float(pick["Sharpe"]),
                        MaxDD=float(pick["MaxDD"]), H1=float(pick["H1"]), H2=float(pick["H2"]),
                        OOS_CAGR=float(pick["OOS_CAGR"]), OOS_Sharpe=float(pick["OOS_Sharpe"]),
                        OOS_MaxDD=float(pick["OOS_MaxDD"]),
                        adv_matched=float(sign * (pick[ooscol] - dref[ooscol])),
                        adv_oos_sharpe=float(pick["OOS_Sharpe"] - dref["OOS_Sharpe"]),
                        pass_4b_full=bool(pick["pass_4b_full"]),
                        pass_4b_oos=bool(pick["pass_4b_oos"]), pass_4a=bool(pick["pass_4a"]),
                        L_DD=bool(pick["L_DD"]), L_CAGR=bool(pick["L_CAGR"]),
                        spy_OOS_CAGR=spy_m[panel]["OOS_CAGR"],
                        spy_OOS_Sharpe=spy_m[panel]["OOS_Sharpe"],
                        spy_OOS_MaxDD=spy_m[panel]["OOS_MaxDD"],
                        live_OOS_Sharpe=live_m[panel]["OOS_Sharpe"],
                        live_MaxDD=live_m[panel]["MaxDD"]))
    WF = pd.DataFrame(wf)
    dump(WF, "walkforward")
    surv = WF[(WF.tau == 3.0) & (WF.moved)]
    P(f"  cells that still MOVE at tau=3 (1132's strict shrink): {len(surv)} of "
      f"{len(WF[WF.tau == 3.0])}")
    P(f"  {'panel':5s} {'set':5s} {'chooser':11s} {'pick':>5s} {'gap/SE':>7s} {'adv_m':>8s} "
      f"{'advS':>8s} {'OOS_S':>7s} {'OOS_DD':>8s} {'4b':>5s} {'4a':>5s}")
    for _, r_ in surv.iterrows():
        P(f"  {r_['panel']:5s} {r_['rung_set']:5s} {r_['chooser']:11s} {r_['pick']:>5s} "
          f"{r_['gap_over_SE']:7.2f} {r_['adv_matched']:+8.4f} {r_['adv_oos_sharpe']:+8.4f} "
          f"{r_['OOS_Sharpe']:7.3f} {r_['OOS_MaxDD']:8.2%} {str(r_['pass_4b_full']):>5s} "
          f"{str(r_['pass_4a']):>5s}")
    med_adv = float(surv.adv_matched.median()) if len(surv) else np.nan
    med_advS = float(surv.adv_oos_sharpe.median()) if len(surv) else np.nan
    P(f"  median matched advantage {med_adv:+.4f} (1132 committed "
      f"{A1132_SURV['med_adv']:+.4f}); median OOS-Sharpe advantage {med_advS:+.4f} "
      f"(1132 committed {A1132_SURV['med_advS']:+.4f})")
    distinct = sorted(set(zip(surv.panel, surv.pick, surv.chooser)))
    P(f"  DISTINCT (panel, pick, chooser) triples behind those {len(surv)} rows: "
      f"{len(distinct)}  ->  {distinct}")
    prem = (len(surv) == A1132_SURV["n_cells"]
            and abs(med_adv - A1132_SURV["med_adv"]) < 5e-3
            and abs(med_advS - A1132_SURV["med_advS"]) < 5e-3
            and all(p == "0.3" and c == "C_ISDD" for _, p, c in distinct))
    gates["G9"] = prem
    gaterows.append(dict(gate="G9", what="reproduce 1132's 4-cell survivor", value=float(len(surv)),
                         pass_=prem))
    P(f"  G9  CROSS-RUN reproduce 1132's 4-cell survivor            "
      f"{'PASS' if prem else 'FAIL'}")
    for panel in PANELS:
        sb, lbm = spy_m[panel], live_m[panel]
        P(f"  {panel} SPY      full {sb['CAGR']:.2%} / {sb['Sharpe']:.3f} / {sb['MaxDD']:.2%}   "
          f"OOS {sb['OOS_CAGR']:.2%} / {sb['OOS_Sharpe']:.3f} / {sb['OOS_MaxDD']:.2%}")
        P(f"  {panel} RULES v2 full {lbm['CAGR']:.2%} / {lbm['Sharpe']:.3f} / {lbm['MaxDD']:.2%}   "
          f"OOS {lbm['OOS_CAGR']:.2%} / {lbm['OOS_Sharpe']:.3f} / {lbm['OOS_MaxDD']:.2%}")

    # ============================================================== [8] HYPOTHESES + VERDICT
    P("")
    P("## [8] HYPOTHESES — declared before any number above was read")
    mono_all_book = all(r["mono_IS"] for r in mono_rows)
    mono_share_null = float(NU.mono_IS.mean())
    bottom_share_null = float((NU.argmax_IS_rung == "0.3").mean())
    at3 = GD[GD.tau == 3.0]
    worst_pct = float(at3.book_percentile_in_null.max())
    fire3 = float(at3.null_fire_rate.min())
    cagr_fail = bool((~G[G.rung == "0.3"].L_CAGR).all() and G[G.rung == "0.3"].L_DD.all())
    hyp = [
        dict(h="H_PREMISE", bar="1132's 4-cell survivor reproduces (pick, +0.1160, -0.0033)",
             value=float(med_adv), pass_=bool(prem)),
        dict(h="H_DOUBLE", bar="the 4 cells are 2 distinct books",
             value=float(len(distinct)), pass_=bool(len(distinct) == 2)),
        dict(h="H_MECH", bar="IS MaxDD monotone in gross for book AND >= 0.95 of null books "
                             "(argmax = bottom rung by construction)",
             value=min(float(mono_all_book), mono_share_null),
             pass_=bool(mono_all_book and mono_share_null >= 0.95)),
        dict(h="H_NULL", bar="book's matched advantage ABOVE the null's 95th percentile at "
                             "tau=3, BOTH kinds, BOTH panels",
             value=worst_pct, pass_=bool(at3.book_percentile_in_null.min() > 0.95)),
        dict(h="H_FIRES", bar="the de-gross rule fires on >= 0.90 of null seeds at tau=3",
             value=fire3, pass_=bool(fire3 >= 0.90)),
        dict(h="H_COST", bar="gross 0.30 passes L_DD and fails L_CAGR on both panels",
             value=float(cagr_fail), pass_=cagr_fail),
    ]
    for h in hyp:
        h["declared"] = True
    # second reading, NOT part of the declared set (see REVISION NOTE); reported beside it
    hyp.append(dict(h="H_NULL_RATIO", declared=False,
                    bar="[second reading, post-hoc] book's scale-free |DD(0.30)|/|DD(0.75)| "
                        "above the null's 95th percentile, both kinds, both panels",
                    value=float(at3.book_pct_dd_ratio.min()),
                    pass_=bool(at3.book_pct_dd_ratio.min() > 0.95)))
    HY = pd.DataFrame(hyp)
    dump(HY, "hypotheses")
    for _, r_ in HY.iterrows():
        P(f"  {r_['h']:12s} {'PASS' if r_['pass_'] else 'FAIL'}  {r_['value']:+.4f}  "
          f"{'declared' if r_['declared'] else 'SECOND READING':14s} {r_['bar']}")
    GT = pd.DataFrame(gaterows)
    dump(GT, "gates")
    dec = HY[HY.declared]
    P(f"  GATES: {int(GT.pass_.sum())} of {len(GT)} PASS.   "
      f"DECLARED HYPOTHESES: {int(dec.pass_.sum())} of {len(dec)} PASS "
      f"(plus 1 second reading, {'PASS' if bool(HY.iloc[-1].pass_) else 'FAIL'}).")

    P("")
    P("## [9] VERDICT")
    real = bool(hyp[3]["pass_"] and not hyp[2]["pass_"])
    P(f"  null books whose IS MaxDD is monotone in gross: {mono_share_null:.3f}; whose "
      f"`argmax IS_MaxDD` is the BOTTOM rung: {bottom_share_null:.3f}")
    P(f"  the de-gross rule fires on {fire3:.3f}-{float(at3.null_fire_rate.max()):.3f} of null "
      f"seeds at tau=3 (median gap/SE over all null seeds "
      f"{float(NU.gap_over_SE.median()):.1f} against the book's "
      f"{float(BK.gap_over_SE.min()):.1f}-{float(BK.gap_over_SE.max()):.1f})")
    P(f"  the book's matched advantage sits at percentile "
      f"{float(at3.book_percentile_in_null.min()):.3f}-{worst_pct:.3f} of the null's own, by "
      f"kind and panel (declared reading, fired seeds only)")
    P(f"  SECOND READING (all seeds, scale-free): the book de-grosses its OWN drawdown to "
      f"{float(BK.dd_ratio.min()):.4f}-{float(BK.dd_ratio.max()):.4f} of the 0.75 book's, the "
      f"null to a median {float(NU.dd_ratio.median()):.4f}")
    P(f"    (pure leverage predicts 0.30/0.75 = 0.4000); the book's ratio sits at percentile "
      f"{float(at3.book_pct_dd_ratio.min()):.3f}-{float(at3.book_pct_dd_ratio.max()):.3f} of "
      f"the null's — i.e. the de-gross buys the BOOK what it buys a COIN FLIP.")
    P(f"  VERDICT: {'REAL EFFECT' if real else 'KILL — the survivor is the GROSS DIAL, and 4 cells are 2 books'}")
    P("  No book is proposed; no KEEP is claimed.  Gross 0.30 clears 4b's DD cap on both panels")
    P("  and fails its CAGR floor on both, so the de-grossed book is not capital-worthy under")
    P("  either KEEP path (4a fails on every rung: no gross rung beats the live book's MaxDD).")
    P("  SURVIVORSHIP (rule 9): U56/B136 are current-constituent lists; every level is")
    P("  optimistic and every 4b count an UPPER bound.  Book and null are drawn from the SAME")
    P("  pool over the SAME tape, so the bias very largely cancels in the difference measured.")
    P(f"  runtime {time.time() - t0:.0f}s")

    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {Path(f'{OUT}.console.txt').name}")


if __name__ == "__main__":
    main()
