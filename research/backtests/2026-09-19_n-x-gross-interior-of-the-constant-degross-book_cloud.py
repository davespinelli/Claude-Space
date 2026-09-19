#!/usr/bin/env python3
"""Idea 1582 — does the CONSTANT DE-GROSS BOOK have an (N, GROSS) INTERIOR an IS-ONLY CHOOSER CAN REACH?

THE OBJECT.  Nine 2026-09-19 runs (1429, 1433, 1436, 1454, 1534, 1545, 1562, 1570, 1586) each
found a drawdown-buying DEVICE beaten-or-tied AT MATCHED EXPOSURE by a plain CONSTANT de-gross of
the same anchor.  If the constant book really is the record's efficient frontier, then its two
free coordinates — the holding count N and the constant gross g — deserve the same pricing the
devices have been getting, and the frozen default (N = 20, g = 0.75) deserves to be asked whether
it is an ARGMAX or an INHERITANCE.

WHAT IS PRICED.  The frozen 2026-09-04 incumbent FRAME (momentum legs (21,252)/(0,126)/(0,63),
200d MA gate at band 0.00, MAXVOL 0.60, min-hold H = 126, weekly cadence, t+1 execution) run at
    N     in {10, 15, 20, 30, 40}                       DIAL 1 (tuned)
    gross in {0.40, 0.45, ..., 1.00}  (13 rungs)        DIAL 2 (tuned)
= 65 cells on EACH of three panels (U56, B136, SMALL) = 195 real books, every one published with
BOTH KEEP paths, at the headline 10 bps and on the 0 / 25 / 50 bps robustness ladder (the ladder
is an EXACT identity off one engine run: net(c) = rg - turnover * c / 1e4; it is never selected on).

THE TITLE QUESTION.  Rule 8: choose (N, g) on warm-up..2016-12-31 ONLY, with FOUR legal IS-only
choosers (argmax IS Sharpe; argmax IS Calmar; argmax IS 4b-legs then Sharpe; DD-aware argmax IS
Sharpe subject to IS MaxDD >= 0.60 x IS SPY MaxDD), then read 2017-01-01..end EXACTLY ONCE.
Does ANY of them reach an interior cell the frozen (20, 0.75) default does not — and if it does,
is the cell it reaches BETTER out of sample than changing nothing?

PRE-REGISTERED VERDICT RULE (written before the run, not after).
  H_INTERIOR   TRUE if, on a majority of panels, at least one legal IS-only chooser lands on a
               cell != (20, 0.75) AND that cell's OOS Sharpe EXCEEDS the frozen default's OOS
               Sharpe.  Only then does the constant book have a reachable interior and the record
               may consider re-siting the default.
  H_FROZEN     TRUE if the choosers either return (20, 0.75) or land on cells that LOSE out of
               sample.  Then the default is not an argmax anyone could have found, and the
               honest reading is that the two coordinates are UNTUNABLE at this sample length —
               a KILL of the interior claim, not of the book.
  A KEEP is claimed ONLY through PROTOCOL path 4a or 4b, and only for a cell a rule-8 chooser
  actually reaches (an in-sample-best cell is PARK at most, never KEEP).

PROTOCOL: rule 1 (>= 10y); rule 2 (weights decided at close t-1, applied at t; 10 bps headline;
long-only, gross <= 1.00, never levered); rule 3 (vs live RULES v2 AND SPY); rule 4 (full sample +
both halves, both KEEP paths at EVERY cell); rule 8 (walk-forward, 2017-2026 read once); rule 9
(survivorship stated).  Exactly TWO tuned parameters: N and gross.

GATES.  G0 >= 10 years on every panel.  G1 CROSS-SCRIPT REPLAY of the committed frozen U56 anchor
(15.80% / 1.1537 / -19.13%, OOS Sharpe 1.1857) at (N=20, g=0.75, W, 10 bps).  G2 exactly two tuned
dials.  G3 no chooser touches a row on or after 2017-01-01.  G4 gross in [0, 1] on every book.
G5 the cost ladder is an identity (the 0 bps net path reproduces rg exactly).  G6 all 195 cells
published.  G7 the protocol-mandated SMALL filter (max_1d_move >= 1.0 dropped) is applied.
G8 the frame is N-monotone (a larger N never holds fewer names on average).  G9 realised gross
tracks the target rung.

Runs standalone and offline (committed price caches only; no network):
  python research/backtests/2026-09-19_n-x-gross-interior-of-the-constant-degross-book_cloud.py
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

DATE = "2026-09-19"
SLUG = "n-x-gross-interior-of-the-constant-degross-book"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP = 260
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G, I_V, I_C = 20, 126, 0.75, 0.60, "W"          # the frozen 2026-09-04 incumbent
NS = [10, 15, 20, 30, 40]                                    # DIAL 1 (tuned)
GS = [round(0.40 + 0.05 * k, 2) for k in range(13)]          # DIAL 2 (tuned): 0.40 .. 1.00
COSTS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_COST = 10.0
OOS_START, IS_END = "2017-01-01", "2016-12-31"
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


# ------------------------------------------------------------------ statistics
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
    """4a against the LIVE RULES v2 book; 4b against SPY.  All four 4b legs returned so any
    failure can be attributed to the leg that caused it."""
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(h1 > bm["H1"]), H2=bool(h2 > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


# ------------------------------------------------------------------ the panel
def mech_legs(q: pd.DataFrame):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return (sum(parts) / len(parts)).values


def cadence_rows(idx, cad):
    """Rebalance ROWS, already shifted one day: the decision taken at close t-1 is applied at t."""
    m = rebalance_mask(idx, cad)
    v = m.shift(1, fill_value=False).values.copy()
    v[0] = True
    return np.flatnonzero(v)


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        q = px[invest]
        self.q = q
        self.comp = mech_legs(q)
        self.vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values

    def frame_inputs(self):
        above = (self.q > self.q.rolling(200).mean()).values
        elig = above & (np.nan_to_num(self.vol20, nan=1e9) < I_V)
        sc = self.comp * (0.5 + 0.5 * above.astype(float))
        key = np.where(np.isfinite(sc), -sc, np.inf)
        return elig, key


def build_frame(pan, elig, key, reb, N, H=I_H, lag=1):
    """The frozen incumbent's HOLDINGS frame at unit gross: min-hold H retains a held name that is
    still priced; vacancies are filled from the eligible set by the composite key."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    nheld = np.zeros(T)
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
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
            k[~(elig[ts] & pr[ts])] = np.inf
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
        stop = reb[i + 1] if i + 1 < len(reb) else T
        if len(sel):
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
            nheld[t:stop] = len(sel)
    return W, nheld


def run_const_gross(pan, frame, reb, g):
    """Daily engine at CONSTANT gross g.  De-gross goes to CASH at 0%/yr, never re-spread, never
    levered.  Returns the GROSS return path and the turnover path; the net path at any cost rung
    is then an exact identity."""
    T, M = pan.rets.shape
    isreb = np.zeros(T, bool)
    isreb[reb] = True
    cur = np.zeros(M)
    rg = np.zeros(T)
    turn = np.zeros(T)
    sc = np.zeros(T)
    gmax = 0.0
    for t in range(T):
        if isreb[t]:
            post = g * frame[t]
        else:
            post = cur
        sc[t] = float(post.sum())
        turn[t] = float(np.abs(post - cur).sum())
        gmax = max(gmax, sc[t])
        r = float(post @ pan.rets[t])
        rg[t] = r
        cur = post * (1.0 + pan.rets[t]) / (1.0 + r)
    return dict(rg=rg, turn=turn, gmax=gmax, gbar=float(sc[WARMUP:].mean()))


def net_of(run, cost):
    return run["rg"] - run["turn"] * cost / 1e4


# ------------------------------------------------------------------ choosers
def chooser_is_sharpe(rows):
    return max(rows, key=lambda d: (d["isSharpe"], -d["N"], -d["g"]))


def chooser_is_calmar(rows):
    return max(rows, key=lambda d: (d["isCAGR"] / abs(d["isMaxDD"]) if d["isMaxDD"] < 0 else -9e9,
                                    -d["N"], -d["g"]))


def chooser_is_legs(rows):
    return max(rows, key=lambda d: (d["isLegs"], d["isSharpe"], -d["N"], -d["g"]))


def chooser_is_ddaware(rows, is_spy_mdd):
    ok = [d for d in rows if d["isMaxDD"] >= DD_CAP * is_spy_mdd]
    pool = ok if ok else rows
    return max(pool, key=lambda d: (d["isSharpe"], -d["N"], -d["g"]))


CHOOSERS = ["argmaxISsharpe", "argmaxIScalmar", "argmaxISlegs", "ISsharpe|ISddcap"]


def main():
    t0 = time.time()
    say("=" * 128)
    say("IDEA 1582 — does the CONSTANT DE-GROSS BOOK have an (N, GROSS) INTERIOR an IS-ONLY "
        "CHOOSER CAN REACH?   (lane cloud, idea 1 of 2)")
    say("  PRE-REGISTERED  H_INTERIOR: on a MAJORITY of panels some legal IS-only chooser lands "
        "off (20, 0.75) AND beats the frozen default's OOS Sharpe -> the interior is reachable.")
    say("  PRE-REGISTERED  H_FROZEN:   the choosers return (20, 0.75) or land on OOS LOSERS -> "
        "the two coordinates are UNTUNABLE at this sample length; KILL of the interior claim.")
    say("=" * 128)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    gate("G7 SMALL max_1d_move filter", f"{len(bad)} dropped, {len(inv)} investable",
         "protocol-mandated, applied", len(bad) > 0 and len(inv) > 100)

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"\n  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1} names, "
        f"SMALL {len(inv)} names.")
    say("  SURVIVORSHIP (rule 9): U56 and B136 are CURRENT-constituent lists and SMALL is a "
        "CURRENT sub-$2B screen carried back to 2010, so every ABSOLUTE level below is an UPPER "
        "BOUND.  The headline of this run is a CONTRAST between cells of ONE grid over the SAME "
        "names on the SAME days, differing only in (N, gross); the bias cannot manufacture that "
        "contrast, but the 4a / 4b verdicts against SPY inherit it and are read as upper bounds.")
    say(f"  GRID: N {NS} x gross {GS} = {len(NS)*len(GS)} cells per panel, "
        f"{len(NS)*len(GS)*len(panels)} real books.  TUNED DIALS = 2 (N, gross).")

    gate("G2 tuned parameters", 2, "exactly 2 (N, gross)", True)

    rows = []
    g5_dev, g8_ok, g9_dev = 0.0, True, 0.0
    bench = {}

    for pan in panels:
        T = len(pan.idx)
        yrs = T / 252.0
        gate(f"G0 {pan.name} length", f"{yrs:.1f}y ({T} rows)", ">= 10y", yrs >= 10.0)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        spy_is = bmpack(pan.spy[WARMUP:i_oos])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=HEADLINE_COST,
                      freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
        bench[pan.name] = dict(spy=spy, spyO=spyO, spy_is=spy_is, live=live, liveO=liveO,
                               i_oos=i_oos)

        say(f"\n  [{pan.name}]  SPY  {spy['CAGR']:.2%} / {spy['Sharpe']:.4f} / {spy['MaxDD']:.2%}  "
            f"H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}   |   4b bars: DD cap "
            f"{DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps  {live['CAGR']:.2%} / {live['Sharpe']:.4f} / "
            f"{live['MaxDD']:.2%}  H1/H2 {live['H1']:.3f}/{live['H2']:.3f}")
        say(f"           OOS SPY {spyO['CAGR']:.2%}/{spyO['Sharpe']:.4f}/{spyO['MaxDD']:.2%}   |   "
            f"OOS RULES v2 {liveO['CAGR']:.2%}/{liveO['Sharpe']:.4f}/{liveO['MaxDD']:.2%}")

        elig, key = pan.frame_inputs()
        reb = cadence_rows(pan.idx, I_C)
        frames, meanheld = {}, {}
        for N in NS:
            frames[N], nh = build_frame(pan, elig, key, reb, N)
            meanheld[N] = float(nh[WARMUP:].mean())
        for a, b in zip(NS, NS[1:]):
            if meanheld[b] < meanheld[a] - 1e-9:
                g8_ok = False
        say("           mean names held: " + ", ".join(f"N={N}:{meanheld[N]:.2f}" for N in NS))

        for N in NS:
            for g in GS:
                run = run_const_gross(pan, frames[N], reb, g)
                g5_dev = max(g5_dev, float(np.abs(net_of(run, 0.0) - run["rg"]).max()))
                g9_dev = max(g9_dev, abs(run["gbar"] - g))
                rec = dict(panel=pan.name, N=N, g=g, gmax=run["gmax"], gbar=run["gbar"])
                for c in COSTS:
                    nr = net_of(run, c)
                    r_all, r_is, r_oos = nr[WARMUP:], nr[WARMUP:i_oos], nr[i_oos:]
                    k4a, k4b, m, h1, h2, legs = keep_paths(r_all, spy, live)
                    ko4a, ko4b, mo, _, _, olegs = keep_paths(r_oos, spyO, liveO)
                    tag = f"c{int(c)}"
                    rec.update({
                        f"{tag}_CAGR": m["CAGR"], f"{tag}_Sharpe": m["Sharpe"],
                        f"{tag}_MaxDD": m["MaxDD"], f"{tag}_H1": h1, f"{tag}_H2": h2,
                        f"{tag}_4a": k4a, f"{tag}_4b": k4b,
                        f"{tag}_4blegs": "".join("1" if legs[x] else "0"
                                                 for x in ("H1", "H2", "DD", "CAGR")),
                        f"{tag}_oCAGR": mo["CAGR"], f"{tag}_oSharpe": mo["Sharpe"],
                        f"{tag}_oMaxDD": mo["MaxDD"], f"{tag}_o4a": ko4a, f"{tag}_o4b": ko4b,
                        f"{tag}_isSharpe": sharpe(r_is), f"{tag}_isCAGR": cagr(r_is),
                        f"{tag}_isMaxDD": mdd(r_is),
                        f"{tag}_turnover": float(run["turn"][WARMUP:].sum() / (len(r_all) / 252)),
                    })
                rows.append(rec)

    D = pd.DataFrame(rows)
    D.to_csv(f"{OUT}.grid.csv", index=False)
    gate("G5 cost-ladder identity (0 bps net == rg)", f"max |dev| {g5_dev:.3e}", "== 0", g5_dev == 0.0)
    gate("G8 frame is N-monotone in mean names held", g8_ok, "True", g8_ok)
    gate("G9 realised mean gross tracks target", f"max |gbar - g| {g9_dev:.4f}", "< 0.20",
         g9_dev < 0.20)
    gate("G6 cells published", f"{len(D)} rows -> {OUT.name}.grid.csv",
         f"{len(NS)*len(GS)*len(panels)}", len(D) == len(NS) * len(GS) * len(panels))
    gate("G4 gross in [0,1]", f"max realised gross {D['gmax'].max():.4f}", "<= 1.0",
         D["gmax"].max() <= 1.0 + 1e-9)

    # ---------------------------------------------------------- G1 anchor replay
    a = D[(D.panel == "U56") & (D.N == I_N) & (D.g == I_G)].iloc[0]
    dev = max(abs(a.c10_CAGR - C_U56["CAGR"]), abs(a.c10_Sharpe - C_U56["Sharpe"]),
              abs(a.c10_MaxDD - C_U56["MaxDD"]), abs(a.c10_oSharpe - C_U56["oSharpe"]))
    say(f"\n  G1 REPLAY of the committed frozen U56 anchor (N=20, g=0.75, W, 10 bps):")
    say(f"     this run {a.c10_CAGR:7.2%} / {a.c10_Sharpe:.4f} / {a.c10_MaxDD:7.2%}  OOS Sharpe "
        f"{a.c10_oSharpe:.4f}")
    say(f"     committed {C_U56['CAGR']:7.2%} / {C_U56['Sharpe']:.4f} / {C_U56['MaxDD']:7.2%}  OOS "
        f"Sharpe {C_U56['oSharpe']:.4f}")
    gate("G1 cross-script anchor replay", f"max |dev| {dev:.4f}", "< 0.01", dev < 0.01)

    # ---------------------------------------------------------- the full grid
    say("\n" + "=" * 128)
    say("ALL 195 CELLS AT THE HEADLINE 10 bps  (CAGR / Sharpe / MaxDD | H1 H2 | 4a 4b legs | OOS "
        "CAGR/Sharpe/MaxDD | o4b)")
    say("=" * 128)
    for pan in panels:
        say(f"\n  [{pan.name}]")
        sub = D[D.panel == pan.name]
        for N in NS:
            for g in GS:
                r = sub[(sub.N == N) & (sub.g == g)].iloc[0]
                say(f"    N={N:<3d} g={g:.2f}  {r.c10_CAGR:7.2%} / {r.c10_Sharpe:7.4f} / "
                    f"{r.c10_MaxDD:7.2%} | {r.c10_H1:6.3f} {r.c10_H2:6.3f} | "
                    f"4a {'Y' if r.c10_4a else '.'}  4b {'Y' if r.c10_4b else '.'} "
                    f"[{r.c10_4blegs}] | OOS {r.c10_oCAGR:7.2%} / {r.c10_oSharpe:7.4f} / "
                    f"{r.c10_oMaxDD:7.2%} | o4b {'Y' if r.c10_o4b else '.'} | "
                    f"turn {r.c10_turnover:5.2f}/yr")

    # ---------------------------------------------------------- KEEP-path census
    say("\n" + "=" * 128)
    say("KEEP-PATH CENSUS (both paths, every cost rung, FULL and OOS)")
    say("=" * 128)
    cens = []
    for c in COSTS:
        tag = f"c{int(c)}"
        for pan in panels:
            s = D[D.panel == pan.name]
            cens.append(dict(cost=c, panel=pan.name, n=len(s),
                             p4a=int(s[f"{tag}_4a"].sum()), p4b=int(s[f"{tag}_4b"].sum()),
                             po4a=int(s[f"{tag}_o4a"].sum()), po4b=int(s[f"{tag}_o4b"].sum()),
                             both4b=int((s[f"{tag}_4b"] & s[f"{tag}_o4b"]).sum())))
    C = pd.DataFrame(cens)
    C.to_csv(f"{OUT}.keeppaths.csv", index=False)
    for _, r in C.iterrows():
        say(f"    {int(r.cost):>2d} bps  {r.panel:<6s}  4a {r.p4a:>2d}/{r.n}  4b {r.p4b:>2d}/{r.n}  "
            f"OOS-4a {r.po4a:>2d}/{r.n}  OOS-4b {r.po4b:>2d}/{r.n}  4b FULL+OOS {r.both4b:>2d}/{r.n}")
    tot4a = int(C[C.cost == HEADLINE_COST].p4a.sum())
    tot4b = int(C[C.cost == HEADLINE_COST].both4b.sum())
    say(f"\n    HEADLINE 10 bps:  4a {tot4a} of {len(D)} cells;  4b FULL AND OOS {tot4b} of "
        f"{len(D)} cells.")

    # ---------------------------------------------------------- rule 8
    say("\n" + "=" * 128)
    say("RULE 8 WALK-FORWARD — (N, g) chosen on warm-up..2016-12-31 ONLY; 2017-01-01..end read ONCE")
    say("=" * 128)
    gate("G3 chooser look-ahead", "choosers read only isSharpe/isCAGR/isMaxDD, all computed on "
         "rows strictly before 2017-01-01", "no OOS row read by any chooser", True)

    wf = []
    for pan in panels:
        b = bench[pan.name]
        sub = D[D.panel == pan.name]
        frozen = sub[(sub.N == I_N) & (sub.g == I_G)].iloc[0]
        for c in COSTS:
            tag = f"c{int(c)}"
            rws = []
            for _, r in sub.iterrows():
                legs_is = 0
                # IS 4b legs, computed on IS rows only (the chooser's own information set)
                legs_is += int(r[f"{tag}_isSharpe"] > b["spy_is"]["Sharpe"])
                legs_is += int(r[f"{tag}_isMaxDD"] >= DD_CAP * b["spy_is"]["MaxDD"])
                legs_is += int(r[f"{tag}_isCAGR"] >= CAGR_FLOOR * b["spy_is"]["CAGR"])
                rws.append(dict(N=int(r.N), g=float(r.g), isSharpe=float(r[f"{tag}_isSharpe"]),
                                isCAGR=float(r[f"{tag}_isCAGR"]), isMaxDD=float(r[f"{tag}_isMaxDD"]),
                                isLegs=legs_is, oSharpe=float(r[f"{tag}_oSharpe"]),
                                oCAGR=float(r[f"{tag}_oCAGR"]), oMaxDD=float(r[f"{tag}_oMaxDD"]),
                                o4a=bool(r[f"{tag}_o4a"]), o4b=bool(r[f"{tag}_o4b"])))
            picks = dict(zip(CHOOSERS,
                             [chooser_is_sharpe(rws), chooser_is_calmar(rws), chooser_is_legs(rws),
                              chooser_is_ddaware(rws, b["spy_is"]["MaxDD"])]))
            for cname, p in picks.items():
                wf.append(dict(panel=pan.name, cost=c, chooser=cname, N=p["N"], g=p["g"],
                               moved=bool((p["N"], p["g"]) != (I_N, I_G)),
                               oCAGR=p["oCAGR"], oSharpe=p["oSharpe"], oMaxDD=p["oMaxDD"],
                               o4a=p["o4a"], o4b=p["o4b"],
                               frozen_oSharpe=float(frozen[f"{tag}_oSharpe"]),
                               frozen_oCAGR=float(frozen[f"{tag}_oCAGR"]),
                               frozen_oMaxDD=float(frozen[f"{tag}_oMaxDD"]),
                               d_oSharpe=p["oSharpe"] - float(frozen[f"{tag}_oSharpe"]),
                               spy_oSharpe=b["spyO"]["Sharpe"], spy_oCAGR=b["spyO"]["CAGR"],
                               spy_oMaxDD=b["spyO"]["MaxDD"],
                               live_oSharpe=b["liveO"]["Sharpe"], live_oCAGR=b["liveO"]["CAGR"],
                               live_oMaxDD=b["liveO"]["MaxDD"]))
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    for pan in panels:
        say(f"\n  [{pan.name}]  frozen default = (N={I_N}, g={I_G})")
        for c in COSTS:
            for _, r in W[(W.panel == pan.name) & (W.cost == c)].iterrows():
                say(f"    {int(c):>2d} bps  {r.chooser:<18s} -> (N={int(r.N):<3d} g={r.g:.2f}) "
                    f"{'MOVED  ' if r.moved else 'FROZEN '} OOS {r.oCAGR:7.2%} / {r.oSharpe:.4f} / "
                    f"{r.oMaxDD:7.2%}   vs frozen {r.frozen_oCAGR:7.2%} / {r.frozen_oSharpe:.4f} / "
                    f"{r.frozen_oMaxDD:7.2%}   d_oSharpe {r.d_oSharpe:+.4f}   "
                    f"o4a {'Y' if r.o4a else '.'} o4b {'Y' if r.o4b else '.'}")
        b = bench[pan.name]
        say(f"    OOS reference:  SPY {b['spyO']['CAGR']:.2%}/{b['spyO']['Sharpe']:.4f}/"
            f"{b['spyO']['MaxDD']:.2%}   RULES v2 {b['liveO']['CAGR']:.2%}/"
            f"{b['liveO']['Sharpe']:.4f}/{b['liveO']['MaxDD']:.2%}")

    H = W[W.cost == HEADLINE_COST]
    moved = int(H.moved.sum())
    moved_win = int(((H.moved) & (H.d_oSharpe > 0)).sum())
    panels_ok = sum(1 for p in panels
                    if ((H.panel == p.name) & H.moved & (H.d_oSharpe > 0)).any())
    say(f"\n  RULE 8 SUMMARY @10 bps: {moved} of {len(H)} chooser x panel picks MOVE off "
        f"(20, 0.75); {moved_win} of those BEAT the frozen default OOS.")
    say(f"    mean d_oSharpe (chooser - frozen) = {H.d_oSharpe.mean():+.4f}  "
        f"[tuning's OOS price against changing nothing]")
    say(f"    panels where SOME legal chooser both MOVES and WINS OOS: {panels_ok} of {len(panels)}")

    h_interior = panels_ok > len(panels) / 2
    say(f"\n  H_INTERIOR = {h_interior}   H_FROZEN = {not h_interior}")

    # ---------------------------------------------------------- the interior itself
    say("\n" + "=" * 128)
    say("IS THE FROZEN DEFAULT AN ARGMAX?  (full-sample argmax of the grid, per panel, 10 bps)")
    say("=" * 128)
    for pan in panels:
        s = D[D.panel == pan.name]
        bs = s.loc[s.c10_Sharpe.idxmax()]
        bo = s.loc[s.c10_oSharpe.idxmax()]
        fz = s[(s.N == I_N) & (s.g == I_G)].iloc[0]
        rank_full = int((s.c10_Sharpe > fz.c10_Sharpe).sum()) + 1
        rank_oos = int((s.c10_oSharpe > fz.c10_oSharpe).sum()) + 1
        say(f"  [{pan.name}]  FULL argmax (N={int(bs.N)}, g={bs.g:.2f}) Sharpe {bs.c10_Sharpe:.4f} "
            f"| OOS argmax (N={int(bo.N)}, g={bo.g:.2f}) oSharpe {bo.c10_oSharpe:.4f} | frozen "
            f"(20, 0.75) ranks {rank_full}/{len(s)} full and {rank_oos}/{len(s)} OOS")

    ok = all(g["pass_"] for g in GATES)
    G = pd.DataFrame(GATES)
    G.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n  GATES: {int(G.pass_.sum())} of {len(G)} PASS.")
    say(f"  VERDICT: {'H_INTERIOR (reachable interior)' if h_interior else 'H_FROZEN — KILL of the interior claim'}")
    say(f"  elapsed {time.time()-t0:.1f}s; gates_all_pass={ok}")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
