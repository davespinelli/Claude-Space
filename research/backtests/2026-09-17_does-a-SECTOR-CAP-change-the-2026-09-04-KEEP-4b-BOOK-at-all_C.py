#!/usr/bin/env python3
"""
Idea 1258 (lane C, 2026-09-17) — does a SECTOR CAP change the 2026-09-04 KEEP 4b BOOK at all?

THE PREMISE.  The standing 4b candidate is a top-20 equal-weight momentum book with NO
concentration control of any kind.  Idea 1255 found it is "about six names wide" — deleting the
k ex-post best constituents walks its CAGR from 15.71% to 9.61% by k = 12 — so the record
already knows the pass is carried by few names.  A max-per-group cap is the cheapest risk clause
a RULES line can state (one sentence, one integer).  Nobody has priced it.  This run does, and
asks the question in the literal form the idea states: DOES IT CHANGE THE BOOK AT ALL, i.e. does
a cap ever BIND, and if it binds, what does it cost and what does it buy?

WHAT IS MEASURED, STATED BEFORE ANY NUMBER IS READ.  The frozen 2026-09-04 candidate with a
max-per-group cap imposed on its N = 20 slots, at eight cap rungs under two group definitions,
on three panels.  At every grid point: full-sample CAGR/Sharpe/MaxDD, both halves, OOS
(2017-01-01 onward), annual turnover, mean net exposure, the BIND RATE (share of rebalance dates
at which the cap displaced at least one candidate the uncapped book would have taken), the mean
number of slots displaced, the mean daily NAME OVERLAP with the uncapped anchor book, the
concentration the cap is acting on (mean and max group share of the 20 slots), the 4a verdict
(vs live RULES v2) and the 4b verdict (vs SPY, full AND OOS) with its failing legs named.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
    CAP   {1, 2, 3, 4, 5, 6, 8, 20} — max names per group among the N = 20 slots.  CAP = 20 is
          unreachable at N = 20 and is therefore the UNCAPPED ANCHOR, i.e. the committed book.
    MAP   {PIT, FROZEN} — how a name is assigned to a group.
          PIT    point-in-time: at each rebalance, a name belongs to the sector SPDR whose daily
                 returns it has the highest 252-day trailing correlation with (min_periods 200).
                 Uses only data on or before the decision date.  Below CORR_MIN the name is
                 UNMAPPED and the cap never binds it.
          FROZEN the same argmax computed ONCE on warm-up..2016-12-31 and held fixed for the
                 whole tape — the static sector table an implementer actually has.  A name with
                 no IS-window history is UNMAPPED (this is stated, not patched with full-sample
                 correlation, which would be lookahead).
NOT DIALS, reported at every value: PANEL {U56, B136, SMALL663} (rule 9); the UJSON control arm
(universe.json's own four declared groups, U56 only — the record's only hand-written group map,
run at every cap rung as a validity read on the correlation maps); the 4a/4b legs; the rule-8
halves; the unmapped share of each panel.

FROZEN AT THE RECORD'S CONSTRUCTION, not touched by this run: composite legs (21/252, 0/126,
0/63) with NO vol scaler, eligibility = above own 200d MA AND vol20 < 0.60, N = 20, H = 126
minimum hold, GROSS = 0.75 of NAV, WEEKLY rebalance, 10 bps (rule 2), t+1 execution, 260-row
warm-up.  Gate G1 checks that (CAP = 20) replays the committed U56 triple 15.71% / 1.1480 /
-19.13%.  Ranking is on the RAW composite: scan.py's (0.5 + 0.5*above) multiplier is identically
1.0 on every eligible name under the committed gate, so it is a no-op here, exactly as in the
committed 2026-09-17 runs.

THREE FROZEN CONSTANTS, DECLARED SO THEY ARE NOT MISTAKEN FOR DIALS.  CORR_MIN = 0.50 (below it
a name is UNMAPPED — bonds, gold, currencies and commodities on U56 have no sector and must not
be forced into one).  CORR_LOOK = 252 days.  The sector set is the 11 SPDRs in data/prices.csv;
XLRE and XLC do not exist before 2015-10 / 2018-06, so the PIT map runs on 9 groups early and 11
late, and that is published rather than back-filled.

HOW THE CAP ACTS, DECLARED BEFORE THE RESULT.  The cap binds ONLY on NEW additions.  A name
already held is never force-sold: the incumbent's H = 126 minimum hold is a committed clause of
the book and a cap that overrides it would be a different book, not a cap on this one.  Existing
holdings COUNT toward their group's tally, so a group at the cap takes no new names.  Under PIT
a held name can drift into an over-full group; the resulting VIOLATION RATE (share of rebalance
dates with any group over the cap among the names actually held) is published at every rung.

PRE-DECLARED OUTCOMES, written before the tape is read:
  (A) THE CAP IS INERT — the book's own group concentration sits at or below the cap rungs the
      idea proposes, the bind rate is ~0 at CAP >= 5, the name overlap with the anchor is ~1.0
      and every metric matches the anchor to noise.  The clause would be free but would also be
      a clause about nothing, and the honest RULES wording would say so.
  (B) THE CAP BINDS AND PAYS — at some rung it materially improves MaxDD without giving up the
      4b CAGR floor, and the 4b verdict survives.  That is a KEEP-candidate memo.
  (C) THE CAP BINDS AND COSTS — it displaces the book's best names into worse ones, CAGR falls
      through 4b's floor (70% of SPY) or Sharpe falls below SPY in a half, and the clause is a
      risk story the tape does not pay for.

RULE 8 (walk-forward).  (CAP, MAP) is CHOSEN on warm-up..2016-12-31 by IS Sharpe alone and
2017-2026 is read ONCE, per panel.  Reported against (i) the do-nothing uncapped anchor, (ii)
the mean over all 16 cells, (iii) the WORST cell, with the IS/OOS rank correlation over the 16.

PROTOCOL: rule 2 costs and execution; rule 4 both KEEP paths at every grid point; rule 5 one
idea, one script, deterministic, standalone; rule 8 as above; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-constituent lists and SMALL663 is a
current sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped before
anything is computed).  Every absolute level printed here is optimistic.  The headline is a
DIFFERENCE between a capped and an uncapped book on the same panel, first-order immune to a
common level bias; the levels are not.  A current-constituent panel is KIND TO CONCENTRATION —
the names a momentum screen piles into are disproportionately the ones that survived to be in
the list — so the UNCAPPED arm is the more flattered of the two, and any win the cap posts here
is a LOWER bound on its win while any loss it posts is an UPPER bound.
A SECOND CAVEAT ON THE GROUP MAP ITSELF: a correlation-argmax group is a CO-MOVEMENT group, not
a GICS sector.  It is the only sector-like map derivable from committed data offline, it is what
the risk clause actually wants (do not hold twenty names that move together), and on U56 the
UJSON arm gives an independent hand-written read on the same question.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-17_does-a-SECTOR-CAP-change-the-2026-09-04-KEEP-4b-BOOK-at-all_C.py
"""
from __future__ import annotations

import json
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

DATE = "2026-09-17"
SLUG = "does-a-SECTOR-CAP-change-the-2026-09-04-KEEP-4b-BOOK-at-all"
OUT = ROOT / "research" / "backtests"
STEM = OUT / f"{DATE}_{SLUG}_C"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = pd.Timestamp("2017-01-01")
IS_END = pd.Timestamp("2016-12-31")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_G = 20, 126, 0.75              # the frozen 2026-09-04 book
CAPS = [1, 2, 3, 4, 5, 6, 8, 20]           # DIAL 1  (20 == uncapped at N=20)
MAPS = ["PIT", "FROZEN"]                   # DIAL 2
ANCHOR_CAP = 20
SECTORS = ["XLB", "XLC", "XLE", "XLF", "XLI", "XLK", "XLP", "XLRE", "XLU", "XLV", "XLY"]
CORR_MIN, CORR_LOOK = 0.50, 252            # frozen constants, NOT dials
COMMITTED_U56 = (0.1571, 1.1480, -0.1913)  # the committed anchor triple, for gate G1
GATES: list[dict] = []


def say(*a):
    print(" ".join(str(x) for x in a), flush=True)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    say(f"   GATE {name}: {value} vs {target} -> {'PASS' if ok else 'FAIL'}")
    return bool(ok)


# ------------------------------------------------------------------ metrics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    return float(np.prod(1.0 + r)) ** (252.0 / len(r)) - 1.0


def mdd(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1.0).min())


def rankcorr(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 3:
        return float("nan")
    ra, rb = pd.Series(a).rank().values, pd.Series(b).rank().values
    sa, sb = ra.std(ddof=0), rb.std(ddof=0)
    if sa == 0 or sb == 0:
        return float("nan")
    return float(((ra - ra.mean()) * (rb - rb.mean())).mean() / (sa * sb))


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def windows(idx, r):
    n = len(r)
    h = n // 2
    o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]), oos=stats(r[o:]), is_=stats(r[:o]))


def flat(w):
    return {f"{k}_{m}": x for k, v in w.items() for m, x in v.items()}


# ------------------------------------------------------------------ panel
class Panel:
    def __init__(self, name, px, invest):
        self.name = name
        self.px = px
        self.invest = invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        q = px[invest]
        parts = []
        for skip, look in LEGS:
            x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
            parts.append(x.rank(axis=1, pct=True))
        comp = (sum(parts) / len(parts)).values          # RAW composite (see docstring)
        self.key = np.where(np.isfinite(comp), -comp, np.inf)
        self.above = (q > q.rolling(200).mean()).values
        vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
        self.volok = np.nan_to_num(vol20, nan=1e9) < MAXVOL
        self.elig = self.above & self.volok              # the committed screen, frozen
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        self.qret = q.pct_change()


# ------------------------------------------------------------------ group maps
def sector_returns(idx):
    px = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)
    return px[SECTORS].reindex(idx).pct_change()


def map_pit(pan, sr):
    """Point-in-time group id per (day, name): argmax of the 252d trailing correlation to a
    sector SPDR, -1 (UNMAPPED, never capped) when the best correlation is below CORR_MIN or no
    correlation exists yet."""
    qr = pan.qret
    best = np.full(qr.shape, -np.inf)
    who = np.full(qr.shape, -1, dtype=np.int64)
    for gi, s in enumerate(SECTORS):
        c = qr.rolling(CORR_LOOK, min_periods=200).corr(sr[s]).values
        c = np.nan_to_num(c, nan=-np.inf, posinf=-np.inf, neginf=-np.inf)
        upd = c > best
        best = np.where(upd, c, best)
        who = np.where(upd, gi, who)
    who[best < CORR_MIN] = -1
    return who, best


def map_frozen(pan, sr):
    """One argmax per name computed on warm-up..2016-12-31 ONLY, held fixed for the whole tape.
    A name with no in-sample history is UNMAPPED (never capped) — stated, not back-filled."""
    m = (pan.idx >= pan.idx[WARMUP]) & (pan.idx <= IS_END)
    qr = pan.qret.loc[m]
    lab = np.full(len(pan.invest), -1, dtype=np.int64)
    best = np.full(len(pan.invest), -np.inf)
    for gi, s in enumerate(SECTORS):
        e = sr[s].loc[m]
        c = qr.corrwith(e).values
        c = np.nan_to_num(c, nan=-np.inf)
        upd = c > best
        best = np.where(upd, c, best)
        lab = np.where(upd, gi, lab)
    lab[best < CORR_MIN] = -1
    return np.repeat(lab[None, :], len(pan.idx), axis=0), lab


def map_ujson(pan):
    """universe.json's own four declared groups (U56 only) — the record's hand-written map."""
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    keys = sorted(U.keys())
    lab = np.full(len(pan.invest), -1, dtype=np.int64)
    for j, t in enumerate(pan.invest):
        for gi, k in enumerate(keys):
            if t in U[k]:
                lab[j] = gi
                break
    return np.repeat(lab[None, :], len(pan.idx), axis=0), keys


# ------------------------------------------------------------------ the book
def build(pan, N, grp, cap, H=A_H, lag=1):
    """The frozen book's selection frame at GROSS = 1.0, with a max-per-group CAP on NEW
    additions (held names count toward their group but are never force-sold — see docstring).
    Row t is the APPLICATION-time weight (rule 2: decided at t-lag, applied at t).
    Weights are 1/len(selected), the SPREAD convention every committed script in this record
    uses (published as a defect by idea 1096 and deliberately not changed here)."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    nreb = len(pan.reb)
    disp = np.zeros(nreb)          # slots the cap displaced
    viol = np.zeros(nreb, dtype=bool)   # any held group over the cap
    conc = np.zeros(nreb)          # max group share of the held book
    held_sets = []
    for i, t in enumerate(pan.reb):
        ts = max(t - lag, 0)
        g = grp[ts]
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = [int(c) for c in young]
        counts: dict[int, int] = {}
        for c in keep:
            gc = int(g[c])
            if gc >= 0:
                counts[gc] = counts.get(gc, 0) + 1
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            for c in order:
                if need == 0:
                    break
                if not np.isfinite(k[c]):
                    break
                gc = int(g[c])
                if gc >= 0 and counts.get(gc, 0) >= cap:
                    disp[i] += 1
                    continue
                take.append(int(c))
                if gc >= 0:
                    counts[gc] = counts.get(gc, 0) + 1
                need -= 1
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        held_sets.append(frozenset(int(c) for c in sel))
        if len(sel):
            gs = g[sel]
            gs = gs[gs >= 0]
            mx = int(np.bincount(gs).max()) if len(gs) else 0
            conc[i] = mx / len(sel)
            viol[i] = mx > cap
            stop = pan.reb[i + 1] if i + 1 < nreb else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    w0 = int(np.searchsorted(pan.reb, WARMUP))
    diag = dict(bind_rate=float((disp[w0:] > 0).mean()), disp_mean=float(disp[w0:].mean()),
                viol_rate=float(viol[w0:].mean()), conc_mean=float(conc[w0:].mean()),
                conc_max=float(conc[w0:].max()))
    return W, diag, held_sets


def overlap(a, b, w0):
    """Mean share of the anchor's names the capped book also holds, over post-warm-up rebalances."""
    v = [len(x & y) / max(len(y), 1) for x, y in zip(a[w0:], b[w0:])]
    return float(np.mean(v)) if v else float("nan")


def run(pan, Wt, gross=A_G):
    """Hold gross*Wt from each rebalance date, drift between, 10 bps on traded notional."""
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    ends = np.append(pan.reb[1:], T)
    for i0, i1 in zip(pan.reb, ends):
        w0 = gross * Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    r = (held * rets).sum(axis=1) - turn * COST / 1e4
    return r, float(turn.sum() / (T / 252.0)), float(held[WARMUP:].sum(axis=1).mean())


# ------------------------------------------------------------------ KEEP paths
def legs_4a(book, live):
    return dict(H1=book["h1"]["Sharpe"] > live["h1"]["Sharpe"],
                H2=book["h2"]["Sharpe"] > live["h2"]["Sharpe"],
                DD=book["full"]["MaxDD"] >= live["full"]["MaxDD"])


def legs_4b(book, spy):
    return dict(H1=book["h1"]["Sharpe"] > spy["h1"]["Sharpe"],
                H2=book["h2"]["Sharpe"] > spy["h2"]["Sharpe"],
                OOS=book["oos"]["Sharpe"] > spy["oos"]["Sharpe"],
                DD=book["full"]["MaxDD"] >= DD_CAP * spy["full"]["MaxDD"],
                CAGR=book["full"]["CAGR"] >= CAGR_FLOOR * spy["full"]["CAGR"])


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say(f"# {DATE} idea 1258 lane C — {SLUG}")
    say("# frozen book: composite(21/252,0/126,0/63) RAW, no vol scaler, gate = above 200d MA AND")
    say(f"# vol20 < {MAXVOL}, N={A_N}, H={A_H}, GROSS={A_G}, weekly, {COST:.0f} bps, t+1, warm-up {WARMUP}")
    say(f"# DIAL 1 cap = {CAPS} (20 = UNCAPPED ANCHOR)   DIAL 2 map = {MAPS}")
    say(f"# frozen constants (NOT dials): CORR_MIN={CORR_MIN}, CORR_LOOK={CORR_LOOK}, sectors={len(SECTORS)}")
    say("# cap binds on NEW ADDITIONS ONLY; held names count but are never force-sold (H=126 is committed)")

    panels = []
    px = load_universe()
    panels.append(("U56", px, [c for c in px.columns if c != "SPY"]))
    pb = load_universe(broad=True)
    panels.append(("B136", pb, [c for c in pb.columns if c != "SPY"]))
    psm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv_s = [c for c in psm.columns if c != "SPY" and c not in bad]
    say(f"# SMALL panel: {psm.shape[1]-1} names, {len(bad & set(psm.columns))} dropped for "
        f"max_1d_move >= 1.0 -> {len(inv_s)} investable")
    panels.append((f"SMALL{len(inv_s)}", psm, inv_s))

    rows, r8rows, maprows = [], [], []
    for name, p_px, inv in panels:
        pan = Panel(name, p_px, inv)
        idx = pan.idx[WARMUP:]
        w0 = int(np.searchsorted(pan.reb, WARMUP))
        spy = windows(idx, pan.spy[WARMUP:])
        live_r = backtest(p_px, rules_v2_weights(p_px), cost_bps=COST, freq="W")["returns"].values[WARMUP:]
        live = windows(idx, live_r)
        sr = sector_returns(pan.idx)

        say(f"\n## {name}  n_days={len(pan.idx)}  n_names={len(inv)}  window {idx[0].date()}..{idx[-1].date()}")
        say(f"   SPY     full {spy['full']['CAGR']:7.2%} / {spy['full']['Sharpe']:.4f} / {spy['full']['MaxDD']:7.2%}"
            f"   halves {spy['h1']['Sharpe']:.4f}/{spy['h2']['Sharpe']:.4f}"
            f"   OOS {spy['oos']['CAGR']:7.2%} / {spy['oos']['Sharpe']:.4f} / {spy['oos']['MaxDD']:7.2%}")
        say(f"   LIVE v2 full {live['full']['CAGR']:7.2%} / {live['full']['Sharpe']:.4f} / {live['full']['MaxDD']:7.2%}"
            f"   halves {live['h1']['Sharpe']:.4f}/{live['h2']['Sharpe']:.4f}"
            f"   OOS {live['oos']['CAGR']:7.2%} / {live['oos']['Sharpe']:.4f} / {live['oos']['MaxDD']:7.2%}")
        say(f"   4b bars: DD cap {DD_CAP*spy['full']['MaxDD']:7.2%}, CAGR floor {CAGR_FLOOR*spy['full']['CAGR']:7.2%}, "
            f"Sharpe H1 {spy['h1']['Sharpe']:.4f} / H2 {spy['h2']['Sharpe']:.4f} / OOS {spy['oos']['Sharpe']:.4f}")

        maps = {}
        g_pit, best_pit = map_pit(pan, sr)
        maps["PIT"] = g_pit
        g_fr, lab_fr = map_frozen(pan, sr)
        maps["FROZEN"] = g_fr
        arms = list(MAPS)
        if name == "U56":
            g_uj, ujkeys = map_ujson(pan)
            maps["UJSON"] = g_uj
            arms.append("UJSON")
            say(f"   UJSON control groups: {ujkeys}  unmapped {int((g_uj[0] < 0).sum())} of {len(inv)}")
        um_pit = float((g_pit[WARMUP:] < 0).mean())
        um_fr = float((lab_fr < 0).mean())
        say(f"   UNMAPPED share: PIT {um_pit:.4f} of name-days, FROZEN {um_fr:.4f} of names "
            f"(no IS history or best corr < {CORR_MIN})")
        maprows.append(dict(panel=name, unmapped_pit_namedays=um_pit, unmapped_frozen_names=um_fr,
                            n_names=len(inv)))

        # ---------- anchor first (CAP = 20, identical under every map)
        Wa, da, sets_a = build(pan, A_N, maps["PIT"], ANCHOR_CAP)
        ra, turn_a, ex_a = run(pan, Wa)
        wa = windows(idx, ra[WARMUP:])
        if name == "U56":
            gate("G1 anchor replays committed U56 triple",
                 f"{wa['full']['CAGR']:.4f}/{wa['full']['Sharpe']:.4f}/{wa['full']['MaxDD']:.4f}",
                 f"{COMMITTED_U56[0]:.4f}/{COMMITTED_U56[1]:.4f}/{COMMITTED_U56[2]:.4f}",
                 abs(wa["full"]["Sharpe"] - COMMITTED_U56[1]) < 5e-3
                 and abs(wa["full"]["MaxDD"] - COMMITTED_U56[2]) < 5e-3
                 and abs(wa["full"]["CAGR"] - COMMITTED_U56[0]) < 5e-3)
        say(f"   ANCHOR (uncapped) concentration of the {A_N} slots: mean max-group share "
            f"{da['conc_mean']:.4f}, worst {da['conc_max']:.4f}  (PIT map) — "
            f"i.e. the largest group holds ~{da['conc_mean']*A_N:.1f} of {A_N} slots on an average week")

        cells = {}
        say(f"\n   {'map':>6} {'cap':>3} | {'CAGR':>7} {'Sharpe':>7} {'MaxDD':>8} | {'H1':>6} {'H2':>6} | "
            f"{'oCAGR':>7} {'oSh':>7} {'oDD':>8} | {'turn':>5} | {'bind':>5} {'disp':>5} {'viol':>5} "
            f"{'ovlp':>5} {'conc':>5} | 4a 4b  failing 4b legs")
        for mp in arms:
            for cp in CAPS:
                W, d, sets = build(pan, A_N, maps[mp], cp)
                r, turn, ex = run(pan, W)
                w = windows(idx, r[WARMUP:])
                ov = overlap(sets, sets_a, w0)
                a, b = legs_4a(w, live), legs_4b(w, spy)
                fails = [k for k, v in b.items() if not v]
                if mp in MAPS:
                    cells[(mp, cp)] = w
                rows.append(dict(panel=name, map=mp, cap=cp, turnover=turn, exposure=ex, gross=A_G,
                                 dial=(mp in MAPS), **d, overlap_anchor=ov, **flat(w),
                                 d_cagr_vs_anchor=w["full"]["CAGR"] - wa["full"]["CAGR"],
                                 d_mdd_vs_anchor=w["full"]["MaxDD"] - wa["full"]["MaxDD"],
                                 d_sharpe_vs_anchor=w["full"]["Sharpe"] - wa["full"]["Sharpe"],
                                 d_oos_sharpe_vs_anchor=w["oos"]["Sharpe"] - wa["oos"]["Sharpe"],
                                 **{f"a_{k}": v for k, v in a.items()},
                                 **{f"b_{k}": v for k, v in b.items()},
                                 pass4a=all(a.values()), pass4b=all(b.values()),
                                 fail4b=",".join(fails) or "NONE"))
                mark = " <= UNCAPPED ANCHOR" if cp == ANCHOR_CAP else ""
                if mp == "UJSON":
                    mark += "  [CONTROL, not a dial]"
                say(f"   {mp:>6} {cp:>3} | {w['full']['CAGR']:7.2%} {w['full']['Sharpe']:7.4f} "
                    f"{w['full']['MaxDD']:8.2%} | {w['h1']['Sharpe']:6.4f} {w['h2']['Sharpe']:6.4f} | "
                    f"{w['oos']['CAGR']:7.2%} {w['oos']['Sharpe']:7.4f} {w['oos']['MaxDD']:8.2%} | "
                    f"{turn:5.2f} | {d['bind_rate']:5.3f} {d['disp_mean']:5.2f} {d['viol_rate']:5.3f} "
                    f"{ov:5.3f} {d['conc_mean']:5.3f} | {int(all(a.values()))}  {int(all(b.values()))}   "
                    f"{','.join(fails) or 'NONE':<18}{mark}")

        # ---------- the cap's price, per map
        say(f"\n   THE CAP'S PRICE ON THE BOOK (cap minus uncapped anchor, both at gross {A_G}):")
        say(f"   {'map':>6} {'cap':>3} | {'dCAGR':>8} {'dMaxDD':>8} {'dSharpe':>8} {'dOOSSh':>8} | "
            f"pp of CAGR paid per pp of MaxDD bought (negative = the cap is worth negative)")
        for mp in MAPS:
            for cp in CAPS:
                w = cells[(mp, cp)]
                dc = w["full"]["CAGR"] - wa["full"]["CAGR"]
                dd = w["full"]["MaxDD"] - wa["full"]["MaxDD"]   # > 0 means the cap IMPROVED DD
                price = (-dc * 100.0) / (dd * 100.0) if abs(dd) > 1e-9 else float("nan")
                say(f"   {mp:>6} {cp:>3} | {dc:+8.2%} {dd:+8.2%} "
                    f"{w['full']['Sharpe']-wa['full']['Sharpe']:+8.4f} "
                    f"{w['oos']['Sharpe']-wa['oos']['Sharpe']:+8.4f} | {price:+.3f}")

        # ---------- rule 8
        grid = [(mp, cp) for mp in MAPS for cp in CAPS]
        iss = [cells[c]["is_"]["Sharpe"] for c in grid]
        oss = [cells[c]["oos"]["Sharpe"] for c in grid]
        pick = grid[int(np.nanargmax(iss))]
        anch = cells[("PIT", ANCHOR_CAP)]
        r8 = dict(panel=name, pick_map=pick[0], pick_cap=pick[1],
                  is_sharpe=cells[pick]["is_"]["Sharpe"], oos_sharpe=cells[pick]["oos"]["Sharpe"],
                  oos_cagr=cells[pick]["oos"]["CAGR"], oos_mdd=cells[pick]["oos"]["MaxDD"],
                  anchor_oos=anch["oos"]["Sharpe"], anchor_oos_cagr=anch["oos"]["CAGR"],
                  anchor_oos_mdd=anch["oos"]["MaxDD"], grid_mean_oos=float(np.nanmean(oss)),
                  grid_worst_oos=float(np.nanmin(oss)), spy_oos=spy["oos"]["Sharpe"],
                  spy_oos_cagr=spy["oos"]["CAGR"], spy_oos_mdd=spy["oos"]["MaxDD"],
                  d_vs_anchor=cells[pick]["oos"]["Sharpe"] - anch["oos"]["Sharpe"],
                  d_vs_gridmean=cells[pick]["oos"]["Sharpe"] - float(np.nanmean(oss)),
                  rank_corr_is_oos=rankcorr(iss, oss), n_cells=len(grid))
        r8rows.append(r8)
        say(f"\n   RULE 8 {name}: (map,cap) chosen on warm-up..{IS_END.date()} by IS Sharpe ONLY, "
            f"{OOS_START.date()}-2026 read ONCE over {len(grid)} cells")
        say(f"        pick = {pick[0]}/{pick[1]}  IS {r8['is_sharpe']:.4f} -> OOS {r8['oos_sharpe']:.4f} "
            f"(CAGR {r8['oos_cagr']:.2%}, MaxDD {r8['oos_mdd']:.2%})")
        say(f"        do-nothing uncapped anchor OOS {r8['anchor_oos']:.4f} ({r8['d_vs_anchor']:+.4f}), "
            f"grid mean {r8['grid_mean_oos']:.4f} ({r8['d_vs_gridmean']:+.4f}), worst {r8['grid_worst_oos']:.4f}, "
            f"SPY {r8['spy_oos']:.4f}")
        say(f"        IS/OOS rank corr over the grid: {r8['rank_corr_is_oos']:+.4f}")

        sub = pd.DataFrame([dict(map=mp, cap=cp, p4a=all(legs_4a(cells[(mp, cp)], live).values()),
                                 p4b=all(legs_4b(cells[(mp, cp)], spy).values()))
                            for mp, cp in grid])
        say(f"        GRID {name}: 4b passes {int(sub.p4b.sum())} of {len(sub)}, "
            f"4a passes {int(sub.p4a.sum())} of {len(sub)}")

    # ---------------------------------------------------------------- outputs
    df = pd.DataFrame(rows)
    df.to_csv(f"{STEM}.grid.csv", index=False)
    pd.DataFrame(r8rows).to_csv(f"{STEM}.walkforward.csv", index=False)
    pd.DataFrame(maprows).to_csv(f"{STEM}.maps.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)

    d = df[df.dial]
    say(f"\n# TOTALS over {len(df)} published grid points ({len(d)} dial cells + "
        f"{len(df)-len(d)} UJSON control cells)")
    say(f"# 4a passes {int(df.pass4a.sum())} of {len(df)};  4b passes {int(df.pass4b.sum())} of {len(df)}")
    for p in df.panel.unique():
        s = df[df.panel == p]
        say(f"#   {p}: 4b {int(s.pass4b.sum())} of {len(s)};  bind rate range "
            f"{s.bind_rate.min():.3f}..{s.bind_rate.max():.3f};  overlap with anchor "
            f"{s.overlap_anchor.min():.3f}..{s.overlap_anchor.max():.3f}")
    say(f"# gates: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass")
    say(f"# wrote {STEM.name}.grid.csv / .walkforward.csv / .maps.csv / .gates.csv")
    say(f"# elapsed {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
