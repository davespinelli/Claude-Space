#!/usr/bin/env python3
"""Idea 1221 (lane B, 2026-09-17)
   is-there-ANY-CHOOSER-in-the-record-that-BEATS-DOING-NOTHING-out-of-sample

THE QUEUE'S PREMISE, QUOTED.  Idea 1212's three SE-based choosers returned mean OOS Sharpe
0.8103-0.8202 against the anchor book's 0.8750, and 1206 already found C_ANCHOR wins on U56
and B136 and loses only on SMALL.  The queue asks for EVERY chooser the record has published
(IS Sharpe, IS Calmar, null percentile, null z, the three SE t's, the mono filters) to be run
against the do-nothing anchor on ONE MATCHED GRID, and for the full ranking to be published
with the anchor's row in it.

WHY ONE MATCHED GRID IS THE WHOLE POINT.  The record's chooser comparisons were made in
different runs, on different ladders, in different panels, at different anchors, and each
published only the choosers that run cared about.  Two choosers measured on different grids
cannot be ranked, and a chooser measured on a grid that never contained the anchor rung
cannot be compared with doing nothing at all.  This run fixes ONE grid -- 24 decisions =
3 panels x 2 anchor contexts x 4 candidate ladders, every ladder containing BOTH contexts'
anchor rung (gate G2) -- and makes all 16 choosers, the anchor included, choose on it.
Every chooser sees exactly the same rungs and exactly the same IS window.

TUNED DIALS (2, PROTOCOL rule 4) -- and the queue names both:

  `CHOOSER SET`      16 choosers (below).  `CANDIDATE LADDER`  4 ladders (below).
  = 64 cells, EVERY ONE PUBLISHED in `.dialgrid.csv` and printed in ARM 3.

  NOT dials, reported at every value: PANEL {U56, B136, SMALL}; ANCHOR CONTEXT {CTX_A, CTX_B};
  the rung tables themselves; the 4a and 4b legs; the nominal bar 1.96; the null bank size
  B = 100; the SE bootstrap B = 600; the block length L = 63 and fold length L = 252 (the
  record's own, 1101 and 1208); tie-break = lowest rung index (declared before any number).

  THE 16 CHOOSERS, each picking ONE rung of a ladder from IS DATA ONLY (rule 8):
    C_ANCHOR    DO NOTHING -- always the context's own rung.  The bar every other row is read against.
    C_ISSHARPE  argmax IS Sharpe.                 C_ISCAGR    argmax IS CAGR.
    C_ISCALMAR  argmax IS CAGR / |IS MaxDD|.      C_ISDD      argmax IS MaxDD (shallowest).
    C_NULLPCT   argmax percentile of the rung's IS Sharpe inside its OWN (N, gross, cadence)-
                matched random-book null (B = 100 draws per key).
    C_NULLZ     argmax (IS Sharpe - null mean) / null SD, same bank.
    C_TIID / C_TBLOCK / C_TFOLD     argmax SIGNED IS t of (rung - anchor) under S_IID /
                S_BLOCK(L=63) / S_FOLD(L=252).  These ALWAYS move -- 1212's form.
    C_BARIID / C_BARBLOCK / C_BARFOLD   the same t, but a rung must CLEAR t > 1.96 to be
                taken at all, else the anchor is kept -- 1210-cloud's "beat the anchor by its
                own SE" form.  These CAN decline to move.
    C_MONO      argmax IS Sharpe only if the ladder is EXACTLY monotone in rung order
                (Spearman |rho| = 1.0, no tolerance), else the anchor -- 1209's mono filter.
    C_MEDIAN    the middle rung: a do-something rule that reads no data at all.
    C_RANDOM    a seeded uniform rung: the coin 1210-cloud showed the family was tracking.

DECLARED BEFORE ANY NUMBER (see ARM 0).  1210-cloud found this family's published statistic
is a census of how often a rule declined to move, and 1212 found all three SE choosers lose
to the anchor.  The prediction is therefore H_NONE: NO chooser beats doing nothing by its own
paired 2 SE; H_COIN: the data-reading choosers do not separate from C_RANDOM / C_MEDIAN; and
H_SPREAD: the whole 16-chooser spread in mean OOS Sharpe is smaller than ONE decision's own
SD.  A chooser that beats the anchor resolvably would REFUTE H_NONE and be a real finding.

ONE ARM WAS ADDED AFTER THE FIRST FULL RUN, AND SAYS SO.  ARM 3b (the count-matched
random-chooser null) and the family-wise bar were written after the first full run showed one
chooser clearing the declared paired 2 SE while a single seeded RANDOM chooser gained nearly
as much.  Neither introduces a dial: ARM 3b's bar is the record's own 90th-percentile
non-certifying bar (1154's memo, 1210-cloud) and the family-wise bar follows from the 15
non-anchor choosers fixed in ARM 0 before any number was computed.  ARM 3 is printed exactly
as it was declared, refuted hypothesis and all.

FROZEN at the 2026-09-04 KEEP-4b candidate's construction: composite = mean of the percentile
ranks of (12-1, 6m, 3m), NO VOL SCALER, eligibility = above own 200d MA and vol20 < 0.60,
top-N equal weight at gross/N of NAV, gated-out weight to CASH at 0%, 10 bps per unit turnover
(PROTOCOL rule 2), next-day execution (LAG 1, gate G3), warm-up 260, IS ends 2016-12-31 and
2017-2026 is read ONCE (PROTOCOL rule 8).

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the
current output of a sub-$2B screen (data/SMALL_PANEL_README.md) less the documented
max_1d_move >= 1.0 exclusion.  A chooser-vs-chooser RANKING is a difference of books drawn
from the same biased panel and the bias very largely cancels out of it; it does NOT cancel out
of the OOS LEVELS or the 4a/4b leg counts, which are reported as levels and must be read as
upper bounds.

Standalone, deterministic, offline.  Nothing outside research/ is written or modified.
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
from engine import rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "is-there-ANY-CHOOSER-in-the-record-that-BEATS-DOING-NOTHING-out-of-sample"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

# ---------------------------------------------------------------- frozen construction
LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]
PANELS = ["U56", "B136", "SMALL"]

CONTEXTS = {                       # NOT a dial: both are reported at every chooser x ladder
    "CTX_A": dict(N=20, H=126, g=0.75, freq="W"),   # the record's anchor (1154, 1212)
    "CTX_B": dict(N=10, H=63, g=0.60, freq="M"),
}
LADDERS = {                        # dial 2 -- every rung of every ladder is priced
    "LAD_N":       ("N",    [5, 8, 10, 12, 15, 20, 25, 30, 40]),
    "LAD_H":       ("H",    [21, 42, 63, 126, 189, 252, 378]),
    "LAD_GROSS":   ("g",    [0.30, 0.45, 0.60, 0.75, 0.90, 1.00]),
    "LAD_CADENCE": ("freq", ["W", "M", "Q"]),
}
CHOOSERS = ["C_ANCHOR", "C_ISSHARPE", "C_ISCAGR", "C_ISCALMAR", "C_ISDD",
            "C_NULLPCT", "C_NULLZ", "C_TIID", "C_TBLOCK", "C_TFOLD",
            "C_BARIID", "C_BARBLOCK", "C_BARFOLD", "C_MONO", "C_MEDIAN", "C_RANDOM"]
MOVERS = [c for c in CHOOSERS if c not in ("C_ANCHOR",)]
DATA_CHOOSERS = [c for c in CHOOSERS if c not in ("C_ANCHOR", "C_MEDIAN", "C_RANDOM")]

NULL_B = 100          # null-bank draws per (panel, N, gross, cadence) key
BOOT_B = 600          # bootstrap draws for S_IID / S_BLOCK
L_BLOCK, L_FOLD = 63, 252
TBAR = 1.9600
SEED_BASE = 12211221

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
    GATES.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
    P(f"  {name:<5s} {'PASS' if ok else 'FAIL'}  {what:<66s} {value:.4e}")
    return bool(ok)


HYP: list[dict] = []


def hyp(name, declared, bar, measured, supported):
    HYP.append(dict(hypothesis=name, declared=declared, bar=bar, measured=str(measured),
                    supported=bool(supported)))
    P(f"  {name:<10s} {'SUPPORTED' if supported else 'REFUTED  '}  {measured}")


# ================================================================= the record's runner
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


def sharpe_rows(x):
    mu = x.mean(axis=1) * 252.0
    sg = x.std(axis=1, ddof=1) * np.sqrt(252.0)
    return np.where(sg > 0, mu / sg, np.nan)


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


def blocks_m(r, ins_m, oos_m):
    c, s, d = fmet(r)
    h = len(r) // 2
    oc, os_, od = fmet(r[oos_m])
    ic, is_, idd = fmet(r[ins_m])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(r[:h]), H2=fsharpe(r[h:]),
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


def se_of_diff(ra, rb, basis, L, tag):
    """SE of Sharpe(ra) - Sharpe(rb) on a PAIRED sample; days resampled JOINTLY."""
    ra, rb = np.asarray(ra, float), np.asarray(rb, float)
    T = len(ra)
    if basis == "S_FOLD":
        ds = []
        for a in range(0, T, L):
            b = min(a + L, T)
            if b - a < 20:
                continue
            ds.append(fsharpe(ra[a:b]) - fsharpe(rb[a:b]))
        ds = np.array([x for x in ds if np.isfinite(x)])
        if len(ds) < 2:
            return np.nan
        return float(ds.std(ddof=1) / np.sqrt(len(ds)))
    rng = np.random.default_rng(seed_of("se", basis, L, tag))
    if basis == "S_IID":
        idx = rng.integers(0, T, size=(BOOT_B, T))
    else:
        nb = int(np.ceil(T / L))
        st = rng.integers(0, T, size=(BOOT_B, nb))
        idx = (st[:, :, None] + np.arange(L)[None, None, :]) % T
        idx = idx.reshape(BOOT_B, nb * L)[:, :T]
    d = sharpe_rows(ra[idx]) - sharpe_rows(rb[idx])
    return float(np.nanstd(d, ddof=1))


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep].dropna(how="all").ffill(), len(bad), len(meta)


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ra = pd.Series(a).rank().values
    rb = pd.Series(b).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


# =================================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P(f"IDEA 1221 (lane B, {DATE}) — {SLUG}")
    P("=" * 100)
    P("")

    # ------------------------------------------------------------------ ARM 0: declarations
    P("## ARM 0 — DECLARED BEFORE ANY NUMBER IS COMPUTED")
    P("  H_NONE   : no chooser's paired mean OOS-Sharpe gap vs C_ANCHOR clears +2 of its own SE.")
    P("  H_COIN   : the 13 data-reading choosers do not separate from C_RANDOM/C_MEDIAN — their")
    P("             mean OOS Sharpe lies inside the [min, max] of the two data-free rows +/- 1 SE.")
    P("  H_SPREAD : the whole 16-chooser spread of mean OOS Sharpe is SMALLER than the SD of a")
    P("             single decision's OOS Sharpe across the grid (a chooser family cannot be")
    P("             ranked by a statistic whose one-draw noise exceeds its whole range).")
    P("  TIE-BREAK: lowest rung INDEX wins every argmax tie (stable argmax), declared here.")
    P("  BAR      : the SE choosers' bar is |t| > 1.9600 on the signed IS t vs the anchor rung.")
    P("")

    P("## PANELS")
    raw = {"U56": load_universe(), "B136": load_universe(broad=True)}
    small, ndrop, nmeta = load_small()
    raw["SMALL"] = small
    panels = {}
    for panel in PANELS:
        px = raw[panel]
        idx, K, T = px.index, len(px.columns), len(px.index)
        warm, ins, oos = windows_of(idx)
        sc, elig = mech(px)
        spy_i = list(px.columns).index("SPY")
        elig = elig.copy()
        elig[:, spy_i] = False                     # SPY is the benchmark, never a holding
        nis = int(np.asarray(idx <= pd.Timestamp(IS_END)).sum())
        panels[panel] = dict(px=px, idx=idx, K=K, T=T, spy_i=spy_i, nis=nis,
                             rets=px.pct_change().fillna(0.0).values,
                             priced=px.notna().values, warm=warm,
                             ins_m=ins[warm], oos_m=oos[warm], sc=sc, elig=elig)
        P(f"  {panel:<6s} {K:4d} cols, {T:,} rows {idx[0].date()} -> {idx[-1].date()}  "
          f"warm {warm.sum():,}  IS {ins.sum():,}  OOS {oos.sum():,}")
    P(f"  SMALL STAMP: data/small_meta.csv lists {nmeta} tickers; {ndrop} dropped for "
      f"max_1d_move >= 1.0; pool served = {panels['SMALL']['K'] - 1} names + SPY as benchmark.")
    P("")

    # ---------------------------------------------------------------------- runners
    def run_W(panel, W, mk, upto=None, lag=LAG):
        d = panels[panel]
        n = d["T"] if upto is None else upto
        rets, warm = d["rets"][:n], d["warm"][:n]
        m = np.asarray(mk[:n]).copy()
        ml = np.roll(m, lag)
        ml[:lag] = False
        Wl = np.zeros((n, d["K"]))
        if lag:
            Wl[lag:] = W[:n - lag]
        else:
            Wl[:] = W[:n]
        g, tn = nrun(rets, Wl, ml)
        return (g - tn * COST / 1e4)[warm], g[warm], tn[warm]

    BOOKS: dict = {}

    def book(panel, N, H, g, freq, upto=None, lag=LAG, cached=True):
        key = (panel, N, H, round(float(g), 4), freq, upto, lag)
        if cached and key in BOOKS:
            return BOOKS[key]
        d = panels[panel]
        n = d["T"] if upto is None else upto
        mk = rebalance_mask(d["idx"], freq).values
        reb = np.flatnonzero(mk[:n])
        W = build(-d["sc"], d["elig"], d["priced"], reb, N, H, n, d["K"], g)
        r, _, _ = run_W(panel, W, mk, upto=upto, lag=lag)
        if cached:
            BOOKS[key] = r
        return r

    NULLBANK: dict = {}

    def null_is_sharpes(panel, N, g, freq):
        """IS Sharpes of NULL_B gross-matched RANDOM books at this (N, gross, cadence).
        Built on the IS-truncated arrays only — no OOS row is ever touched (gate G5)."""
        key = (panel, N, round(float(g), 4), freq)
        if key in NULLBANK:
            return NULLBANK[key]
        d = panels[panel]
        n = d["nis"]
        mk = rebalance_mask(d["idx"], freq).values
        reb = np.flatnonzero(mk[:n])
        ok = d["elig"] & d["priced"]
        out = np.empty(NULL_B)
        for b in range(NULL_B):
            rng = np.random.default_rng(seed_of("null", panel, N, g, freq, b))
            W = np.zeros((n, d["K"]))
            for i, t in enumerate(reb):
                cand = np.flatnonzero(ok[t])
                if not len(cand):
                    continue
                sel = rng.choice(cand, size=min(N, len(cand)), replace=False)
                stop = reb[i + 1] if i + 1 < len(reb) else n
                W[t:stop, sel] = g / len(sel)
            r, _, _ = run_W(panel, W, mk, upto=n)
            out[b] = fsharpe(r)
        NULLBANK[key] = out
        return out

    # ------------------------------------------------------- benchmarks, once per panel
    P("## BENCHMARKS (per panel, 10 bps, post warm-up)")
    bench = {}
    for panel in PANELS:
        dd = panels[panel]
        spy = dd["px"]["SPY"].pct_change().fillna(0.0).values[dd["warm"]]
        live, _, _ = run_W(panel, rules_v2_weights(dd["px"]).values,
                           rebalance_mask(dd["idx"], "W").values)
        bench[panel] = dict(SPY=blocks_m(spy, dd["ins_m"], dd["oos_m"]),
                            LIVE=blocks_m(live, dd["ins_m"], dd["oos_m"]), spy_r=spy)
        for k in ("SPY", "LIVE"):
            m = bench[panel][k]
            P(f"  {panel:<6s} {k:<5s} {m['CAGR']:7.2%} / {m['Sharpe']:.4f} / {m['MaxDD']:8.2%}"
              f"  halves {m['H1']:.4f}/{m['H2']:.4f}  OOS {m['OOS_CAGR']:7.2%} / "
              f"{m['OOS_Sharpe']:.4f} / {m['OOS_MaxDD']:8.2%}")
    P("")

    # ================================================= ARM 1: the 24-decision rung grid
    P("## ARM 1 — THE MATCHED GRID: 3 panels x 2 contexts x 4 ladders = 24 decisions")
    decisions = []
    rung_rows = []
    for panel in PANELS:
        for cname, ctx in CONTEXTS.items():
            for lname, (dial, rungs) in LADDERS.items():
                anchor_val = ctx[dial]
                tab = []
                for j, rv in enumerate(rungs):
                    pr = dict(ctx)
                    pr[dial] = rv
                    full = book(panel, pr["N"], pr["H"], pr["g"], pr["freq"])
                    isr = book(panel, pr["N"], pr["H"], pr["g"], pr["freq"], upto=panels[panel]["nis"])
                    m = blocks_m(full, panels[panel]["ins_m"], panels[panel]["oos_m"])
                    nb = null_is_sharpes(panel, pr["N"], pr["g"], pr["freq"])
                    tab.append(dict(rung_i=j, rung=rv, is_anchor=(rv == anchor_val),
                                    is_r=isr, full_r=full, m=m,
                                    null_pct=float((nb < m["IS_Sharpe"]).mean()),
                                    null_z=float((m["IS_Sharpe"] - nb.mean()) / nb.std(ddof=1)),
                                    null_mean=float(nb.mean()), null_sd=float(nb.std(ddof=1))))
                ai = [t["rung_i"] for t in tab if t["is_anchor"]]
                assert len(ai) == 1, (panel, cname, lname, ai)
                ai = ai[0]
                ar = tab[ai]["is_r"]
                for t in tab:
                    tag = f"{panel}|{cname}|{lname}|{t['rung']}"
                    for nm, basis, L in (("t_iid", "S_IID", 1), ("t_block", "S_BLOCK", L_BLOCK),
                                         ("t_fold", "S_FOLD", L_FOLD)):
                        d_ = t["m"]["IS_Sharpe"] - tab[ai]["m"]["IS_Sharpe"]
                        se = np.nan if t["rung_i"] == ai else se_of_diff(t["is_r"], ar, basis, L, tag)
                        t[nm] = 0.0 if t["rung_i"] == ai else (d_ / se if se and np.isfinite(se) else np.nan)
                        t[nm + "_se"] = 0.0 if t["rung_i"] == ai else se
                dec = dict(panel=panel, ctx=cname, ladder=lname, dial=dial,
                           anchor_i=ai, anchor_val=anchor_val, tab=tab,
                           mono=abs(spearman([t["rung_i"] for t in tab],
                                             [t["m"]["IS_Sharpe"] for t in tab])) == 1.0)
                decisions.append(dec)
                for t in tab:
                    rung_rows.append(dict(
                        panel=panel, ctx=cname, ladder=lname, dial=dial, rung=t["rung"],
                        rung_i=t["rung_i"], is_anchor=t["is_anchor"], ladder_mono=dec["mono"],
                        IS_Sharpe=t["m"]["IS_Sharpe"], IS_CAGR=t["m"]["IS_CAGR"],
                        IS_MaxDD=t["m"]["IS_MaxDD"],
                        IS_Calmar=t["m"]["IS_CAGR"] / abs(t["m"]["IS_MaxDD"]),
                        null_pct=t["null_pct"], null_z=t["null_z"], null_mean=t["null_mean"],
                        null_sd=t["null_sd"], t_iid=t["t_iid"], t_block=t["t_block"],
                        t_fold=t["t_fold"], se_iid=t["t_iid_se"], se_block=t["t_block_se"],
                        se_fold=t["t_fold_se"],
                        OOS_Sharpe=t["m"]["OOS_Sharpe"], OOS_CAGR=t["m"]["OOS_CAGR"],
                        OOS_MaxDD=t["m"]["OOS_MaxDD"], CAGR=t["m"]["CAGR"],
                        Sharpe=t["m"]["Sharpe"], MaxDD=t["m"]["MaxDD"],
                        H1=t["m"]["H1"], H2=t["m"]["H2"]))
            P(f"  {panel:<6s} {cname} built ({time.time() - t0:.0f}s elapsed, "
              f"{len(BOOKS)} books, {len(NULLBANK)} null keys)")
    rdf = pd.DataFrame(rung_rows)
    dump(rdf, "rungs")
    P(f"  {len(decisions)} decisions, {len(rdf)} priced rungs, "
      f"{len(NULLBANK) * NULL_B:,} null books, {len(BOOKS)} real book runs.")
    P(f"  Ladders exactly monotone in IS Sharpe: {int(sum(d['mono'] for d in decisions))} of "
      f"{len(decisions)}.")
    P("")

    # ================================================= gates
    P("## GATES")
    g_ok = True
    d0 = decisions[0]
    n_anc = [sum(1 for t in d["tab"] if t["is_anchor"]) for d in decisions]
    g_ok &= gate("G1", "every decision has EXACTLY ONE anchor rung (do-nothing is reachable)",
                 float(min(n_anc)), set(n_anc) == {1})
    miss = 0
    for lname, (dial, rungs) in LADDERS.items():
        for ctx in CONTEXTS.values():
            if ctx[dial] not in rungs:
                miss += 1
    g_ok &= gate("G2", "declared ladder rung sets contain every context anchor value",
                 float(miss), miss == 0)
    # next-day execution is BINDING
    a_lag1 = book("U56", 20, 126, 0.75, "W")
    a_lag0 = book("U56", 20, 126, 0.75, "W", lag=0, cached=False)
    v = abs(fsharpe(a_lag0) - fsharpe(a_lag1))
    g_ok &= gate("G3", "LAG 1 binds: same-day execution scores DIFFERENTLY (no free lag)",
                 v, v > 1e-6)
    # costs bind
    dU = panels["U56"]
    mkU = rebalance_mask(dU["idx"], "W").values
    WU = build(-dU["sc"], dU["elig"], dU["priced"], np.flatnonzero(mkU), 20, 126,
               dU["T"], dU["K"], 0.75)
    net, gross_r, turn = run_W("U56", WU, mkU)
    v = float(gross_r.sum() - net.sum())
    g_ok &= gate("G4", "10 bps costs bind: gross - net > 0 over the sample", v, v > 0)
    # IS statistics use NO out-of-sample row
    full_anchor = book("U56", 20, 126, 0.75, "W")
    is_anchor = book("U56", 20, 126, 0.75, "W", upto=panels["U56"]["nis"])
    v = float(np.abs(full_anchor[panels["U56"]["ins_m"]] - is_anchor).max())
    g_ok &= gate("G5", "IS-truncated run == full run restricted to IS (no OOS leakage)", v, v < 1e-12)
    # null bank is gross-matched
    nb = null_is_sharpes("U56", 20, 0.75, "W")
    g_ok &= gate("G6", "null bank: NULL_B finite, non-degenerate draws (SD > 0)",
                 float(np.isfinite(nb).sum()),
                 (np.isfinite(nb).sum() == NULL_B) and nb.std(ddof=1) > 0)
    v = float(rdf.null_pct.min()), float(rdf.null_pct.max())
    g_ok &= gate("G6b", "every rung's null percentile lies in [0, 1]", float(v[1]),
                 v[0] >= 0.0 and v[1] <= 1.0)
    # SPY never eligible
    v = float(sum(panels[p]["elig"][:, panels[p]["spy_i"]].sum() for p in PANELS))
    g_ok &= gate("G7", "SPY is never eligible in any panel", v, v == 0)
    # determinism
    v = float(np.abs(book("U56", 20, 126, 0.75, "W", cached=False) - full_anchor).max())
    g_ok &= gate("G8", "book() is deterministic on re-run", v, v < 1e-15)
    s1 = se_of_diff(full_anchor, bench["U56"]["spy_r"], "S_IID", 1, "gate")
    s2 = se_of_diff(full_anchor, bench["U56"]["spy_r"], "S_BLOCK", 1, "gate")
    v = abs(s1 - s2) / s1
    g_ok &= gate("G9", "S_BLOCK at L = 1 == S_IID (relative, both 600 draws)", v, v < 0.15)
    v = float(np.abs(np.array([t["t_iid"] for t in d0["tab"]])[d0["anchor_i"]]))
    g_ok &= gate("G10", "the anchor rung's own t vs itself is exactly 0", v, v == 0.0)
    P("")

    # ================================================= ARM 2: the choosers choose
    P("## ARM 2 — EVERY CHOOSER PICKS ON IS DATA ONLY (PROTOCOL rule 8); 2017-2026 read ONCE")

    def argmax_stable(vals):
        v = np.array([x if np.isfinite(x) else -np.inf for x in vals], float)
        return int(np.argmax(v))                     # ties -> lowest rung index (declared)

    def pick(chooser, dec):
        tab, ai = dec["tab"], dec["anchor_i"]
        if chooser == "C_ANCHOR":
            return ai
        if chooser == "C_ISSHARPE":
            return argmax_stable([t["m"]["IS_Sharpe"] for t in tab])
        if chooser == "C_ISCAGR":
            return argmax_stable([t["m"]["IS_CAGR"] for t in tab])
        if chooser == "C_ISCALMAR":
            return argmax_stable([t["m"]["IS_CAGR"] / abs(t["m"]["IS_MaxDD"]) for t in tab])
        if chooser == "C_ISDD":
            return argmax_stable([t["m"]["IS_MaxDD"] for t in tab])
        if chooser == "C_NULLPCT":
            return argmax_stable([t["null_pct"] for t in tab])
        if chooser == "C_NULLZ":
            return argmax_stable([t["null_z"] for t in tab])
        if chooser in ("C_TIID", "C_TBLOCK", "C_TFOLD"):
            k = {"C_TIID": "t_iid", "C_TBLOCK": "t_block", "C_TFOLD": "t_fold"}[chooser]
            return argmax_stable([t[k] for t in tab])
        if chooser in ("C_BARIID", "C_BARBLOCK", "C_BARFOLD"):
            k = {"C_BARIID": "t_iid", "C_BARBLOCK": "t_block", "C_BARFOLD": "t_fold"}[chooser]
            ts = [t[k] if np.isfinite(t[k]) else -np.inf for t in tab]
            best = argmax_stable(ts)
            return best if ts[best] > TBAR else ai
        if chooser == "C_MONO":
            return argmax_stable([t["m"]["IS_Sharpe"] for t in tab]) if dec["mono"] else ai
        if chooser == "C_MEDIAN":
            return len(tab) // 2
        if chooser == "C_RANDOM":
            rng = np.random.default_rng(seed_of("rand", dec["panel"], dec["ctx"], dec["ladder"]))
            return int(rng.integers(0, len(tab)))
        raise KeyError(chooser)

    pick_rows = []
    for chooser in CHOOSERS:
        for dec in decisions:
            j = pick(chooser, dec)
            t = dec["tab"][j]
            m = t["m"]
            sb, lb = bench[dec["panel"]]["SPY"], bench[dec["panel"]]["LIVE"]
            l4b, l4o, l4a = legs_4b(m, sb), legs_4b_oos(m, sb), legs_4a(m, lb)
            anc = dec["tab"][dec["anchor_i"]]["m"]
            pick_rows.append(dict(
                chooser=chooser, panel=dec["panel"], ctx=dec["ctx"], ladder=dec["ladder"],
                rung=t["rung"], rung_i=j, moved=int(j != dec["anchor_i"]),
                IS_Sharpe=m["IS_Sharpe"], OOS_Sharpe=m["OOS_Sharpe"], OOS_CAGR=m["OOS_CAGR"],
                OOS_MaxDD=m["OOS_MaxDD"], CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=m["H1"], H2=m["H2"],
                d_OOS_Sharpe=m["OOS_Sharpe"] - anc["OOS_Sharpe"],
                d_OOS_CAGR=m["OOS_CAGR"] - anc["OOS_CAGR"],
                d_OOS_MaxDD=abs(m["OOS_MaxDD"]) - abs(anc["OOS_MaxDD"]),
                spy_OOS_Sharpe=sb["OOS_Sharpe"], live_OOS_Sharpe=lb["OOS_Sharpe"],
                pass4a=all(l4a.values()), pass4b=all(l4b.values()),
                pass4b_oos=all(l4o.values()), **l4a, **l4b, **l4o))
    pdf = pd.DataFrame(pick_rows)
    dump(pdf, "picks")
    g_ok &= gate("G11", "every chooser makes exactly 24 picks",
                 float(pdf.groupby("chooser").size().nunique()),
                 set(pdf.groupby("chooser").size()) == {len(decisions)})
    g_ok &= gate("G12", "C_ANCHOR moves at 0 of 24 decisions",
                 float(pdf[pdf.chooser == "C_ANCHOR"].moved.sum()),
                 pdf[pdf.chooser == "C_ANCHOR"].moved.sum() == 0)
    P("")

    # ================================================= ARM 3: THE RANKING
    P("## ARM 3 — THE FINDING: the full ranking on OOS Sharpe, with the anchor's row in it")
    anc_by_dec = pdf[pdf.chooser == "C_ANCHOR"].set_index(["panel", "ctx", "ladder"])
    rank_rows = []
    for chooser in CHOOSERS:
        s = pdf[pdf.chooser == chooser].set_index(["panel", "ctx", "ladder"])
        d = (s.OOS_Sharpe - anc_by_dec.OOS_Sharpe).values
        se = float(np.std(d, ddof=1) / np.sqrt(len(d))) if len(d) > 1 else np.nan
        # panel-clustered SE (3 clusters -- reported, and flagged as thin)
        cl = pd.Series(d, index=s.index.get_level_values("panel")).groupby(level=0).mean()
        se_cl = float(cl.std(ddof=1) / np.sqrt(len(cl)))
        rank_rows.append(dict(
            chooser=chooser, moved=int(s.moved.sum()), mean_OOS_Sharpe=float(s.OOS_Sharpe.mean()),
            mean_OOS_CAGR=float(s.OOS_CAGR.mean()), mean_OOS_MaxDD=float(s.OOS_MaxDD.mean()),
            mean_full_Sharpe=float(s.Sharpe.mean()), mean_IS_Sharpe=float(s.IS_Sharpe.mean()),
            wins_vs_anchor=int((d > 0).sum()), ties=int((d == 0).sum()),
            mean_gap=float(np.mean(d)), se_gap=se, t_gap=float(np.mean(d) / se) if se else np.nan,
            se_gap_panelclustered=se_cl,
            t_gap_panelclustered=float(np.mean(d) / se_cl) if se_cl else np.nan,
            n4a=int(s.pass4a.sum()), n4b=int(s.pass4b.sum()), n4b_oos=int(s.pass4b_oos.sum()),
            beats_SPY_OOS=int((s.OOS_Sharpe > s.spy_OOS_Sharpe).sum()),
            beats_LIVE_OOS=int((s.OOS_Sharpe > s.live_OOS_Sharpe).sum())))
    rank = pd.DataFrame(rank_rows).sort_values("mean_OOS_Sharpe", ascending=False)
    dump(rank, "ranking")
    P("  chooser      moved  meanOOS_S  meanOOS_CAGR  meanOOS_DD   gap vs ANCHOR  "
      "SE      t      t_panel  win/tie  4a  4b  4bOOS  >SPY >LIVE")
    for _, r in rank.iterrows():
        star = " <== DOING NOTHING" if r.chooser == "C_ANCHOR" else ""
        P(f"  {r.chooser:<12s} {r.moved:>2d}/24  {r.mean_OOS_Sharpe:9.4f}  "
          f"{r.mean_OOS_CAGR:11.2%}  {r.mean_OOS_MaxDD:9.2%}  {r.mean_gap:+13.4f}  "
          f"{r.se_gap:.4f}  {r.t_gap:+6.2f}  {r.t_gap_panelclustered:+6.2f}  "
          f"{r.wins_vs_anchor:>2d}/{r.ties:<2d}   {r.n4a:>2d}  {r.n4b:>2d}   {r.n4b_oos:>2d}"
          f"     {r.beats_SPY_OOS:>2d}   {r.beats_LIVE_OOS:>2d}{star}")
    P("")

    best = rank.iloc[0]
    anchor_row = rank[rank.chooser == "C_ANCHOR"].iloc[0]
    anchor_rank = int(list(rank.chooser).index("C_ANCHOR")) + 1
    P(f"  C_ANCHOR RANKS {anchor_rank} of {len(rank)} on mean OOS Sharpe "
      f"({anchor_row.mean_OOS_Sharpe:.4f}); the top row is {best.chooser} "
      f"({best.mean_OOS_Sharpe:.4f}).")
    cleared = rank[(rank.chooser != "C_ANCHOR") & (rank.t_gap > 2.0)]
    P(f"  CHOOSERS CLEARING +2 SE OVER DOING NOTHING: {len(cleared)} of {len(CHOOSERS) - 1}"
      + (f" — {', '.join(cleared.chooser)}" if len(cleared) else ""))
    hyp("H_NONE", "no chooser beats doing nothing by its own paired 2 SE",
        "0 choosers with t_gap > 2", f"{len(cleared)} of {len(CHOOSERS) - 1} clear it; "
        f"best t {rank[rank.chooser != 'C_ANCHOR'].t_gap.max():+.2f} "
        f"({rank[rank.chooser != 'C_ANCHOR'].sort_values('t_gap').iloc[-1].chooser})",
        len(cleared) == 0)

    # ---------------------------------------------------------------- ARM 3b
    # DISCLOSURE: ARM 3b was ADDED AFTER the first full run, which showed one chooser
    # (C_NULLZ) clearing the declared +2 SE bar while a single seeded RANDOM chooser gained
    # nearly as much.  A paired t against the anchor cannot tell "this chooser reads the
    # ladder" from "this chooser moved off the anchor 20 times and the average rung happened
    # to beat the anchor".  The count-matched random null separates them.  Its bar is NOT
    # chosen here: it is the record's own non-certifying bar, the 90th percentile of a
    # count-matched null (1154's memo, 1210-cloud).  The test count (15 non-anchor choosers)
    # was fixed in ARM 0 before any number, so the Bonferroni critical value below is
    # determined in advance even though it is only reported now.
    P("## ARM 3b — COUNT-MATCHED RANDOM-CHOOSER NULL (added after the first full run; see")
    P("##          the disclosure in the source).  A chooser that moves m of 24 times is read")
    P("##          against 2,000 random choosers that move the SAME m times on the SAME grid.")
    dec_oos = [np.array([t["m"]["OOS_Sharpe"] for t in d["tab"]]) for d in decisions]
    dec_anc = [d["anchor_i"] for d in decisions]
    NDRAW = 2000
    null_rows = []
    for chooser in CHOOSERS:
        rr = rank[rank.chooser == chooser].iloc[0]
        m, obs = int(rr.moved), float(rr.mean_gap)
        rng = np.random.default_rng(seed_of("cmnull", chooser))
        gaps = np.empty(NDRAW)
        for b in range(NDRAW):
            tot = 0.0
            if m:
                which = rng.choice(len(decisions), size=m, replace=False)
                for i in which:
                    alt = [j for j in range(len(dec_oos[i])) if j != dec_anc[i]]
                    j = alt[int(rng.integers(0, len(alt)))]
                    tot += dec_oos[i][j] - dec_oos[i][dec_anc[i]]
            gaps[b] = tot / len(decisions)
        null_rows.append(dict(chooser=chooser, moved=m, obs_gap=obs,
                              null_mean=float(gaps.mean()), null_sd=float(gaps.std(ddof=1)),
                              null_p90=float(np.percentile(gaps, 90)),
                              pctile=float((gaps < obs).mean())))
    cmn = pd.DataFrame(null_rows)
    dump(cmn, "countmatched")
    P("  chooser      moved   observed gap   null mean   null SD   null p90   PERCENTILE")
    for _, r in cmn.sort_values("pctile", ascending=False).iterrows():
        P(f"  {r.chooser:<12s} {int(r.moved):>2d}/24   {r.obs_gap:+12.4f}   {r.null_mean:+9.4f}  "
          f"{r.null_sd:8.4f}  {r.null_p90:+9.4f}   {r.pctile:.4f}")
    info = cmn[(cmn.chooser != "C_ANCHOR") & (cmn.pctile >= 0.90)]
    P(f"  CHOOSERS CLEARING THE 90th PERCENTILE OF THEIR OWN COUNT-MATCHED NULL: "
      f"{len(info)} of {len(CHOOSERS) - 1}" + (f" — {', '.join(info.chooser)}" if len(info) else ""))
    zbon = 2.9354                                  # two-sided 0.05 / 15 tests, normal approx
    P(f"  MULTIPLICITY: {len(CHOOSERS) - 1} choosers were tested against one anchor, so the "
      f"family-wise 0.05 bar is |t| > {zbon:.4f}, not 1.96.")
    survive = rank[(rank.chooser != "C_ANCHOR") & (rank.t_gap > zbon)]
    P(f"  CHOOSERS CLEARING THE FAMILY-WISE BAR: {len(survive)} of {len(CHOOSERS) - 1}"
      + (f" — {', '.join(survive.chooser)}" if len(survive) else ""))
    P("")

    free = rank[rank.chooser.isin(["C_RANDOM", "C_MEDIAN"])].mean_OOS_Sharpe
    dat = rank[rank.chooser.isin(DATA_CHOOSERS)]
    onese = float(pdf.groupby(["panel", "ctx", "ladder"]).OOS_Sharpe.mean().std(ddof=1))
    inside = int(((dat.mean_OOS_Sharpe >= free.min() - onese) &
                  (dat.mean_OOS_Sharpe <= free.max() + onese)).sum())
    hyp("H_COIN", "the data-reading choosers do not separate from the data-free ones",
        "all 13 inside [min,max] of C_RANDOM/C_MEDIAN +/- one decision SD",
        f"{inside} of {len(dat)} inside [{free.min():.4f}, {free.max():.4f}] +/- {onese:.4f}",
        inside == len(dat))

    spread = float(rank.mean_OOS_Sharpe.max() - rank.mean_OOS_Sharpe.min())
    dec_sd = float(pdf.OOS_Sharpe.std(ddof=1))
    hyp("H_SPREAD", "the 16-chooser spread is smaller than one decision's own SD",
        "spread < SD(OOS Sharpe) over all picks",
        f"spread {spread:.4f} vs per-pick SD {dec_sd:.4f} "
        f"(ratio {spread / dec_sd:.4f})", spread < dec_sd)
    P("")

    # ================================================= ARM 4: the 64-cell dial grid
    P("## ARM 4 — EVERY ONE OF THE 64 DIAL CELLS (CHOOSER x CANDIDATE LADDER), mean OOS Sharpe")
    cell = pdf.groupby(["chooser", "ladder"]).agg(
        mean_OOS_Sharpe=("OOS_Sharpe", "mean"), moved=("moved", "sum"),
        mean_gap=("d_OOS_Sharpe", "mean"), n=("OOS_Sharpe", "size")).reset_index()
    dump(cell, "dialgrid")
    lad = list(LADDERS)
    P("  chooser      " + "".join(f"{l:<14s}" for l in lad) + "  (mean OOS Sharpe; 6 picks each)")
    for chooser in CHOOSERS:
        row = "".join(
            f"{float(cell[(cell.chooser == chooser) & (cell.ladder == l)].mean_OOS_Sharpe.iloc[0]):<14.4f}"
            for l in lad)
        P(f"  {chooser:<12s} {row}")
    P("  gap vs DOING NOTHING in the same cell:")
    P("  chooser      " + "".join(f"{l:<14s}" for l in lad))
    for chooser in CHOOSERS:
        row = "".join(
            f"{float(cell[(cell.chooser == chooser) & (cell.ladder == l)].mean_gap.iloc[0]):<+14.4f}"
            for l in lad)
        P(f"  {chooser:<12s} {row}")
    won = cell[(cell.chooser != "C_ANCHOR") & (cell.mean_gap > 0)]
    P(f"  CELLS WHERE A CHOOSER BEATS DOING NOTHING ON AVERAGE: {len(won)} of "
      f"{(len(CHOOSERS) - 1) * len(lad)}")
    P("")

    # ================================================= ARM 5: what is a pick worth at all
    P("## ARM 5 — HOW MUCH IS THERE TO WIN? the OOS spread of each decision's own ladder")
    sp = []
    for dec in decisions:
        o = np.array([t["m"]["OOS_Sharpe"] for t in dec["tab"]])
        a = dec["tab"][dec["anchor_i"]]["m"]["OOS_Sharpe"]
        sp.append(dict(panel=dec["panel"], ctx=dec["ctx"], ladder=dec["ladder"], k=len(o),
                       oos_min=o.min(), oos_max=o.max(), oos_mean=o.mean(), anchor=a,
                       best_gain=o.max() - a, worst_loss=o.min() - a,
                       anchor_pctile=float((o < a).mean()),
                       is_oos_rho=spearman([t["m"]["IS_Sharpe"] for t in dec["tab"]], o)))
    spd = pd.DataFrame(sp)
    dump(spd, "spread")
    P(f"  mean best-possible gain over the anchor {spd.best_gain.mean():+.4f}  "
      f"(median {spd.best_gain.median():+.4f}, max {spd.best_gain.max():+.4f})")
    P(f"  mean worst-possible loss              {spd.worst_loss.mean():+.4f}  "
      f"(median {spd.worst_loss.median():+.4f}, min {spd.worst_loss.min():+.4f})")
    P(f"  the anchor's own percentile inside its ladder's OOS Sharpes: mean "
      f"{spd.anchor_pctile.mean():.4f} (a do-nothing rule sitting at 0.5 is an AVERAGE rung)")
    P(f"  IS->OOS rank correlation across the ladder: mean {spd.is_oos_rho.mean():+.4f}, "
      f"median {spd.is_oos_rho.median():+.4f}, positive at "
      f"{int((spd.is_oos_rho > 0).sum())} of {len(spd)} decisions")
    P("  by ladder:")
    for l in lad:
        s = spd[spd.ladder == l]
        P(f"    {l:<12s} best gain {s.best_gain.mean():+.4f}  worst loss "
          f"{s.worst_loss.mean():+.4f}  anchor pctile {s.anchor_pctile.mean():.4f}  "
          f"IS->OOS rho {s.is_oos_rho.mean():+.4f}")
    P("  by panel:")
    for p_ in PANELS:
        s = spd[spd.panel == p_]
        P(f"    {p_:<12s} best gain {s.best_gain.mean():+.4f}  worst loss "
          f"{s.worst_loss.mean():+.4f}  anchor pctile {s.anchor_pctile.mean():.4f}  "
          f"IS->OOS rho {s.is_oos_rho.mean():+.4f}")
    P("")

    # ================================================= ARM 6: per-panel ranking (1206's leg)
    P("## ARM 6 — 1206's LEG RE-READ: does the anchor win on U56/B136 and lose on SMALL?")
    P("  panel   anchor    best chooser (mean OOS Sharpe)      anchor's rank")
    for p_ in PANELS:
        s = pdf[pdf.panel == p_].groupby("chooser").OOS_Sharpe.mean().sort_values(ascending=False)
        ar = int(list(s.index).index("C_ANCHOR")) + 1
        P(f"  {p_:<7s} {s['C_ANCHOR']:.4f}    {s.index[0]:<14s} {s.iloc[0]:.4f}"
          f"              {ar} of {len(s)}")
    P("")

    # ================================================= ARM 7: KEEP paths, both, on every pick
    P("## ARM 7 — BOTH KEEP PATHS on all 384 picks (PROTOCOL rule 4)")
    uniq = pdf.drop_duplicates(subset=["panel", "ctx", "ladder", "rung"])
    P(f"  distinct BOOKS behind the 384 picks: {len(uniq)} "
      f"(a chooser that declines to move re-selects the same anchor book — 1211's inflation)")
    P(f"  4a (beat the live book) : {int(pdf.pass4a.sum())} of {len(pdf)} picks, "
      f"{int(uniq.pass4a.sum())} of {len(uniq)} distinct books")
    P(f"  4b full sample vs SPY   : {int(pdf.pass4b.sum())} of {len(pdf)} picks, "
      f"{int(uniq.pass4b.sum())} of {len(uniq)} distinct books")
    P(f"  4b OOS-only vs SPY      : {int(pdf.pass4b_oos.sum())} of {len(pdf)} picks, "
      f"{int(uniq.pass4b_oos.sum())} of {len(uniq)} distinct books")
    both = uniq[(uniq.pass4b) & (uniq.pass4b_oos)]
    P(f"  BOTH 4b full AND 4b OOS : {len(both)} of {len(uniq)} distinct books")
    for leg in ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]:
        P(f"    4b leg {leg:<7s} passes at {int(uniq[leg].sum()):>3d} of {len(uniq)} books")
    for leg in ["A_H1", "A_H2", "A_DD"]:
        P(f"    4a leg {leg:<7s} passes at {int(uniq[leg].sum()):>3d} of {len(uniq)} books")
    if len(both):
        P("  the books passing both, by panel: " +
          ", ".join(f"{k} {v}" for k, v in both.panel.value_counts().items()))
    P("")

    # ================================================= verdict + leaderboard
    P("## VERDICT")
    n_gate = sum(1 for g in GATES if g["pass_"])
    # a chooser's OWN capital record: the 4b passes among the 24 books IT selected,
    # against the 24 the anchor selected.  A chooser that wins OOS Sharpe but books FEWER
    # capital-worthy rules than doing nothing has not earned capital.
    pdf["both4b"] = pdf.pass4b & pdf.pass4b_oos
    own = pdf.groupby("chooser").both4b.sum()
    anc_both = int(own["C_ANCHOR"])
    surv = sorted(set(cleared.chooser) & set(info.chooser) & set(survive.chooser))
    P(f"  LEG 1 (paired 2 SE vs the anchor)      : {len(cleared)} of {len(CHOOSERS) - 1}"
      + (f" — {', '.join(cleared.chooser)}" if len(cleared) else ""))
    P(f"  LEG 2 (own count-matched null, p90)    : {len(info)} of {len(CHOOSERS) - 1}"
      + (f" — {', '.join(info.chooser)}" if len(info) else ""))
    P(f"  LEG 3 (family-wise bar |t| > {zbon:.2f})    : {len(survive)} of {len(CHOOSERS) - 1}"
      + (f" — {', '.join(survive.chooser)}" if len(survive) else ""))
    P(f"  CHOOSERS PASSING ALL THREE             : {len(surv)}"
      + (f" — {', '.join(surv)}" if surv else ""))
    P(f"  4b (full AND OOS) books each chooser actually SELECTED, against DOING NOTHING's "
      f"{anc_both} of 24:")
    for c in CHOOSERS:
        if c != "C_ANCHOR":
            P(f"    {c:<12s} {int(own[c]):>2d} of 24" +
              ("   <-- fewer than doing nothing" if own[c] < anc_both else
               ("   <-- MORE than doing nothing" if own[c] > anc_both else "   == doing nothing")))
    keepers = [c for c in surv if int(own[c]) > anc_both]
    beat = len(cleared) > 0
    if keepers:
        verdict = "KEEP-candidate"
    elif surv:
        verdict = "PARK (wins OOS Sharpe, books no capital)"
    else:
        verdict = "KILL (capital)"
    answered = ("YES, but only on the raw paired bar" if beat and not surv
                else ("YES" if surv else "NO"))
    P(f"  ANSWERED = {answered}.  {len(cleared)} of {len(CHOOSERS) - 1} published choosers beat "
      f"DOING NOTHING by their own paired 2 SE over 24 matched decisions; {len(surv)} survive "
      f"all three legs; {len(keepers)} of those book MORE capital-worthy rules than the anchor.")
    P(f"  Verdict: {verdict}.  Gates {n_gate} of {len(GATES)}.")
    P("")

    ar = anchor_row
    b_ = best
    sb_u, lb_u = bench["U56"]["SPY"], bench["U56"]["LIVE"]
    rows = [
        f"| {DATE} | 1221 B — **THE FULL CHOOSER RANKING ON ONE MATCHED GRID**: all "
        f"{len(CHOOSERS)} published choosers (IS Sharpe / IS CAGR / IS Calmar / IS DD / null "
        f"percentile / null z / 3 signed-t / 3 t>1.96-else-anchor / mono filter / median rung / "
        f"random rung) + DOING NOTHING, 24 decisions each (3 panels x 2 anchor contexts x 4 "
        f"candidate ladders), rule-8 picks on warm-up..{IS_END}, 2017-2026 read ONCE, all 64 "
        f"dial cells published | {b_.mean_OOS_CAGR:.1%} (best chooser mean OOS) | "
        f"{b_.mean_OOS_Sharpe:.2f} | {b_.mean_OOS_MaxDD:.1%} | n/a | "
        f"DOING NOTHING mean OOS Sharpe {ar.mean_OOS_Sharpe:.4f} | "
        f"**{answered}: {len(cleared)} of {len(CHOOSERS) - 1} CHOOSERS CLEAR +2 SE OVER THE "
        f"ANCHOR. C_ANCHOR ranks {anchor_rank} of {len(rank)}; top row {b_.chooser} "
        f"{b_.mean_OOS_Sharpe:.4f} vs anchor {ar.mean_OOS_Sharpe:.4f} "
        f"(gap {b_.mean_gap:+.4f}, t {b_.t_gap:+.2f}); whole-family spread {spread:.4f} against "
        f"a per-pick SD of {dec_sd:.4f}.** | `{OUT.name}.py` |",

        f"| {DATE} | 1221 B — **IS IT INFORMATION OR IS IT MOVING?** each chooser read against "
        f"2,000 RANDOM choosers count-matched to its own move count on the same 24 decisions "
        f"(bar = the record's own 90th-percentile non-certifying bar), plus the family-wise "
        f"|t| > {zbon:.2f} the {len(CHOOSERS) - 1} tests imply (ARM 3b, added after the first "
        f"full run — disclosed in the source) | n/a | n/a | n/a | n/a | a seeded RANDOM chooser "
        f"gains {float(rank[rank.chooser == 'C_RANDOM'].mean_gap.iloc[0]):+.4f} over the anchor "
        f"by itself | **{len(info)} of {len(CHOOSERS) - 1} choosers clear their own "
        f"count-matched null at p90 and {len(survive)} clear the family-wise bar; "
        f"{len(surv)} clear all three legs"
        + (f" ({', '.join(surv)})" if surv else "")
        + f". Every chooser's gap is bought by MOVING: the null of a coin that moves as often "
        f"gains {float(cmn[cmn.chooser == 'C_ISSHARPE'].null_mean.iloc[0]):+.4f} on its own.** "
        f"| `{OUT.name}.py` |",

        f"| {DATE} | 1221 B — **HOW MUCH IS THERE TO WIN AT ALL**: the OOS Sharpe spread of each "
        f"decision's own ladder, 24 decisions, and the IS->OOS rank correlation that a chooser "
        f"would have to exploit | n/a | n/a | n/a | n/a | the anchor rung's own ladder percentile "
        f"{spd.anchor_pctile.mean():.4f} | **best-possible gain over the anchor averages "
        f"{spd.best_gain.mean():+.4f} and the worst-possible loss {spd.worst_loss.mean():+.4f}; "
        f"IS->OOS rank correlation across the ladder averages {spd.is_oos_rho.mean():+.4f} "
        f"(positive at {int((spd.is_oos_rho > 0).sum())} of {len(spd)} decisions) — the ladder "
        f"carries {'some' if spd.is_oos_rho.mean() > 0.2 else 'no usable'} selection signal.** | "
        f"`{OUT.name}.py` |",

        f"| {DATE} | 1221 B — **RULE 8 WALK-FORWARD + BOTH KEEP PATHS**, {len(pdf)} picks over "
        f"{len(uniq)} distinct books, 10 bps, next-day execution | "
        f"{uniq.CAGR.max():.1%} (best book) | {uniq.Sharpe.max():.2f} | "
        f"{uniq[uniq.Sharpe == uniq.Sharpe.max()].MaxDD.iloc[0]:.1%} | "
        f"{uniq[uniq.Sharpe == uniq.Sharpe.max()].H1.iloc[0]:.2f} / "
        f"{uniq[uniq.Sharpe == uniq.Sharpe.max()].H2.iloc[0]:.2f} | "
        f"U56 SPY {sb_u['Sharpe']:.4f} ({sb_u['H1']:.4f}/{sb_u['H2']:.4f}), OOS "
        f"{sb_u['OOS_Sharpe']:.4f}; U56 LIVE {lb_u['Sharpe']:.4f}, OOS {lb_u['OOS_Sharpe']:.4f} | "
        f"**4a {int(uniq.pass4a.sum())} of {len(uniq)} books; 4b full {int(uniq.pass4b.sum())}, "
        f"4b OOS {int(uniq.pass4b_oos.sum())}, BOTH {len(both)}. Verdict {verdict}.** | "
        f"`{OUT.name}.py` |",
    ]
    P("## LEADERBOARD ROWS")
    for r in rows:
        P(r)
    P("")

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    pd.DataFrame(HYP).to_csv(f"{OUT}.hyp.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    Path(f"{OUT}.leaderboard.txt").write_text("\n".join(rows) + "\n")
    P(f"Runtime {time.time() - t0:.0f}s. Gates {n_gate} of {len(GATES)}. "
      f"Offline, deterministic.")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
