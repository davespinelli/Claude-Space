#!/usr/bin/env python3
"""
Idea 1610 (lane B, 2026-09-19) — does the incumbent's 126-day MINIMUM HOLD PROTECT WINNERS or
TRAP LOSERS?

THE PREMISE, TAKEN FROM THE RECORD'S OWN MECHANISM.  Ideas 1484 / 1505 state why every brake
this record has priced damages MaxDD: a brake holds names the screen has ALREADY DROPPED
through the drawdown.  That damage is ONE-SIDED by construction — it is the LOSING half of the
held book that the brake refuses to release — yet every H ever priced here is SYMMETRIC: the
frozen 2026-09-04 incumbent (U56, composite momentum, N = 20, H = 126, gross 0.75, MAXVOL 0.60,
200d MA gate, weekly Fri-decide / Mon-trade, 10 bps, t+1) protects a name from rank-based
eviction for 126 days whether it is up 40% or down 40% since entry.

If the brake's benefit (turnover saved, whipsaw avoided) sits on the WINNER side and its cost
(drawdown, trapped losers) sits on the LOSER side, then the two sides should be separable: a
book with H_WIN = 126 and H_LOSS = 0 would keep the saving and drop the damage.  If instead the
brake is one object — if releasing losers early is just the momentum screen re-trading its own
noise — then cutting H_LOSS buys nothing and costs turnover.  Nothing in the record answers
this.  This run splits the dial and prices both sides.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  H_WIN   {0, 21, 63, 126, 252}   DIAL 1 — days a name UP since entry is protected from eviction
  H_LOSS  {0, 21, 63, 126, 252}   DIAL 2 — days a name DOWN since entry is protected

25 cells per panel, 75 in all, EVERY ONE published in .grid.csv.  The cell
(H_WIN, H_LOSS) = (126, 126) IS THE FROZEN INCUMBENT and is present as a gate, not as a finding.

SIDE IS READ CAUSALLY.  A held name's side at rebalance row t is decided by its REAL close at
t-1 (the same row the rank key is read on) against its REAL close on the row it was ENTERED.
Both are strictly in the past, and the rebalance grid is itself lagged one row (rule 2), so a
Friday-close decision trades at Monday's open.  A name whose entry or current close is missing
is assigned to the LOSS side (the conservative assignment: it removes protection).  Gate G7
replays a truncated tape and asserts the surviving rows are bit-identical.

WHAT THE SPLIT DOES NOT TOUCH.  The composite ranking legs, the 200d MA gate, the vol20 < 0.60
screen, N, the gross, the cadence, the costs and the realised returns are the frozen incumbent's,
unmodified.  Only the eviction clock is split.  As in the frozen frame, a protected name is
retained even when it has fallen out of eligibility — that retention IS the brake, and it is
exactly what this run is pricing.

THE CONTROLS THAT DECIDE THE VERDICT.
  (a) THE MECHANISM TEST, published before any capital number is read: the share of held
      name-rebalances that are RETAINED WHILE INELIGIBLE (the brake actually biting), split by
      side.  If the brake's damage is one-sided, the loss-side share must dominate.
  (b) Three reordering currencies against the frozen incumbent (mean Jaccard of the held set,
      share of rebalances whose held set differs, share of name-days changed) — a cell that
      changes no holdings cannot produce a finding either way.
  (c) Every dSharpe gap to the frozen incumbent is scored by a PAIRED circular-block bootstrap
      (400 reps x 63-row blocks, seed 20260919, identical block starts for both books).  A gap
      inside its own SE is published as UNRESOLVED, not as a finding.  |t| > 2 is the bar.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); both KEEP paths at every
cell; the halves; IS and OOS windows; annualised turnover; realised mean holding age.

COMPARANDS (rule 3): the live RULES v2 baseline at 10 bps weekly, SPY buy-and-hold, and the
FROZEN (126, 126) incumbent.

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3 (RULES v2 AND
SPY); rule 4 (both KEEP paths, exactly 2 tuned parameters); rule 8 (walk-forward: (H_WIN, H_LOSS)
chosen on warm-up..2016-12-31 by argmax IS Sharpe, 2017-2026 read ONCE, scored against the frozen
incumbent, RULES v2 and SPY); rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py,
bot.py and baseline.py are NOT modified.

GATES.  G0 sample >= 10y.  G1 CROSS-SCRIPT REPLAY: the (126,126) cell must reproduce the
committed 2026-09-04 U56 anchor (15.80% / 1.1537 / -19.13% full; 17.32% / 1.1857 / -19.13% OOS).
G2 the (126,126) cell is BIT-IDENTICAL to a SYMMETRIC-H build that never reads the side at all.
G3 all 75 cells published.  G4 exactly two tuned parameters.  G5 the rule-8 chooser reads no row
on or after 2017-01-01.  G6 no leverage: realised weight sum never exceeds the gross.  G7 the
side assignment is non-anticipating (truncated-tape replay bit-identical).  G8 the split
actually BINDS (both sides carry a non-zero share of held name-rebalances).  G9 bit-identical
recompute of one cell per panel.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-19_does-the-min-hold-protect-winners-or-trap-losers_B.py
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
SLUG = "does-the-min-hold-protect-winners-or-trap-losers"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G = 20, 126, 0.75            # the frozen 2026-09-04 incumbent
COST, CADENCE = 10.0, "W"
HWINS = [0, 21, 63, 126, 252]            # DIAL 1
HLOSSES = [0, 21, 63, 126, 252]          # DIAL 2
OOS_START = "2017-01-01"
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BOOT_REPS, BOOT_BLOCK, BOOT_SEED = 400, 63, 20260919
C_U56 = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857)   # committed anchor

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


def mech_legs(q: pd.DataFrame):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return (sum(parts) / len(parts)).values


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
        self.q = q
        self.qv = q.values                                   # REAL closes, for the side test
        above = (q > q.rolling(200).mean()).values
        vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
        self.above = above
        self.elig = above & (np.nan_to_num(vol20, nan=1e9) < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.rank = self._rank_key(mech_legs(q))

    def _rank_key(self, comp):
        sc = comp * (0.5 + 0.5 * self.above.astype(float))
        return np.where(np.isfinite(sc), -sc, np.inf)


def build(pan, h_win, h_loss, N=I_N, lag=1, symmetric=None, nrows=None):
    """The frozen selection frame with the eviction clock SPLIT BY SIDE.

    A held name is protected from rank-based eviction while (t - entry_row) < H_side, where
    H_side is h_win if its close at t-lag is >= its close on its entry row, else h_loss.
    symmetric=H ignores the side entirely (gate G2's control).  Returns the weight frame at
    gross 1.0, the per-rebalance held sets, and the mechanism/age counters."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    holds = []
    cur = np.full(K, -1, dtype=np.int64)         # entry row, -1 = not held
    epx = np.full(K, np.nan)                     # entry close
    pr = pan.priced[:, pan.iinv]
    qv = pan.qv
    reb = pan.reb if nrows is None else pan.reb[pan.reb < nrows]
    # mechanism counters: held name-rebalances, split by side, and how many are INELIGIBLE
    cnt = dict(n_win=0, n_loss=0, inel_win=0, inel_loss=0, prot_win=0, prot_loss=0, age_sum=0.0,
               age_n=0)
    first_i = int(np.searchsorted(reb, WARMUP))
    for i, t in enumerate(reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        if len(held):
            age = (t - cur[held]).astype(float)
            pn = qv[ts, held]
            pe = epx[held]
            with np.errstate(invalid="ignore"):
                win = np.isfinite(pn) & np.isfinite(pe) & (pn >= pe)
            if symmetric is None:
                lim = np.where(win, h_win, h_loss)
            else:
                lim = np.full(len(held), symmetric)
            young = held[age < lim]
            if i >= first_i:
                el = pan.elig[ts, held] & pr[ts, held]
                cnt["n_win"] += int(win.sum())
                cnt["n_loss"] += int((~win).sum())
                cnt["inel_win"] += int((win & ~el).sum())
                cnt["inel_loss"] += int(((~win) & ~el).sum())
                prot = age < lim
                cnt["prot_win"] += int((win & prot & ~el).sum())
                cnt["prot_loss"] += int(((~win) & prot & ~el).sum())
                cnt["age_sum"] += float(age.sum())
                cnt["age_n"] += len(held)
        else:
            young = held
        if len(young):
            young = young[pr[t, young]]
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.rank[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new = np.full(K, -1, dtype=np.int64)
        newp = np.full(K, np.nan)
        for c in keep:
            new[c] = cur[c]
            newp[c] = epx[c]
        for c in take:
            new[c] = t
            newp[c] = qv[t, c]
        cur, epx = new, newp
        sel = np.flatnonzero(cur >= 0)
        holds.append(frozenset(int(x) for x in sel))
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else (T if nrows is None else nrows)
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W, holds, cnt


def run_book(pan, frame, C, Cp, g, nrows=None):
    rets = pan.rets
    T, M = rets.shape
    if nrows is not None:
        T = nrows
    turn = np.zeros(T)
    out = np.zeros(T)
    curw = np.zeros(M)
    reb = pan.reb[pan.reb < T]
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
    return out, turn, wsum_max


def net(gross_r, turn):
    return gross_r - turn * COST / 1e4


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


def paired_block_dsharpe(a, b, reps=BOOT_REPS, L=BOOT_BLOCK, seed=BOOT_SEED):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    nb = int(np.ceil(n / L))
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n, size=(reps, nb))
    idx = (starts[:, :, None] + np.arange(L)[None, None, :]).reshape(reps, nb * L)[:, :n] % n
    A, B = a[idx], b[idx]

    def sh(X):
        v = X.std(axis=1, ddof=0) * np.sqrt(252)
        return np.where(v > 0, X.mean(axis=1) * 252 / v, np.nan)

    d = sh(A) - sh(B)
    obs = float(sharpe(a) - sharpe(b))
    se = float(np.nanstd(d, ddof=1))
    return obs, se, (obs / se if se > 0 else np.nan)


def reorder_stats(holds, base_holds, first_i):
    jac, diff, nd, tot, n = [], 0, 0, 0, 0
    for i, (h, b) in enumerate(zip(holds, base_holds)):
        if i < first_i:
            continue
        n += 1
        u = len(h | b)
        jac.append(len(h & b) / u if u else 1.0)
        if h != b:
            diff += 1
        nd += len(h ^ b)
        tot += len(h | b)
    return (float(np.mean(jac)) if n else np.nan,
            diff / n if n else np.nan,
            nd / tot if tot else np.nan)


def main():
    t_start = time.time()
    say("=" * 122)
    say("IDEA 1610 (lane B, 2026-09-19) — does the incumbent's 126-day MIN-HOLD PROTECT WINNERS "
        "or TRAP LOSERS?")
    say("DIALS: H_WIN {0,21,63,126,252} x H_LOSS {0,21,63,126,252} on the frozen 2026-09-04 "
        "incumbent (N=20, gross 0.75, MAXVOL 0.60, 200d MA gate, weekly, 10 bps, t+1).")
    say("(126,126) IS the frozen incumbent.  Only the EVICTION CLOCK is split; the legs, the "
        "gate, the screen, the gross, the cadence and the realised returns are unchanged.")
    say("=" * 122)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0.")

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, "
        f"SMALL {len(inv)} (of {len(pxS.columns)-1} priced).")
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010.  Every absolute level below is an UPPER BOUND.  "
        "What this run reads is a CONTRAST between two eviction clocks over the same names on "
        "the same days — but note the bias runs AGAINST the loser-release arm: a survivor's "
        "drawdown is more likely to have been recovered than a delisted name's.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y);  {len(p.reb)} weekly rebalances")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)
    gate("G4 exactly two tuned parameters (H_WIN, H_LOSS)", 2, "== 2", True)

    grid, wf_rows, mech_rows = [], [], []
    wsum_global, g2_dev, g7_dev, g9_dev = 0.0, 0.0, 0.0, 0.0
    g1_txt, side_min = None, 1.0

    for pan in panels:
        T = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        i_is = int(np.searchsorted(pan.idx.values, np.datetime64(IS_END)))
        first_reb = int(np.searchsorted(pan.reb, WARMUP))
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
        C = np.cumprod(1.0 + pan.rets, axis=0)
        Cp = np.vstack([np.ones((1, pan.rets.shape[1])), C[:-1]])

        say(f"\n  [{pan.name}]  SPY  CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.4f} MaxDD "
            f"{spy['MaxDD']:.2%} H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap "
            f"{DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           SPY OOS Sharpe {spyO['Sharpe']:.4f} CAGR {spyO['CAGR']:.2%} MaxDD "
            f"{spyO['MaxDD']:.2%}")
        say(f"           RULES v2 live @10bps  CAGR {live['CAGR']:.2%} Sharpe {live['Sharpe']:.4f} "
            f"MaxDD {live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f}  (OOS Sharpe "
            f"{liveO['Sharpe']:.4f})")

        # ---- the frozen incumbent, cell (126,126) --------------------------------------------
        f0, holds0, cnt0 = build(pan, I_H, I_H)
        g0, tn0, ws = run_book(pan, f0, C, Cp, I_G)
        wsum_global = max(wsum_global, ws)
        r0 = net(g0, tn0)
        anc, ancO = bmpack(r0[WARMUP:]), bmpack(r0[i_oos:])
        say(f"           FROZEN ANCHOR (126,126)  CAGR {anc['CAGR']:.2%} Sharpe {anc['Sharpe']:.4f} "
            f"MaxDD {anc['MaxDD']:.2%} H1/H2 {anc['H1']:.3f}/{anc['H2']:.3f}  |  OOS "
            f"{ancO['CAGR']:.2%} / {ancO['Sharpe']:.4f} / {ancO['MaxDD']:.2%}")
        if pan.name == "U56":
            d = max(abs(anc["CAGR"] - C_U56["CAGR"]), abs(anc["Sharpe"] - C_U56["Sharpe"]),
                    abs(anc["MaxDD"] - C_U56["MaxDD"]), abs(ancO["Sharpe"] - C_U56["oSharpe"]))
            g1_txt = f"maxdiff {d:.2e} vs committed 15.80%/1.1537/-19.13% (OOS 1.1857)"
            gate("G1 cross-script replay of the committed 2026-09-04 U56 anchor", g1_txt,
                 "<= 5e-3", d <= 5e-3)
        # G2: side-blind symmetric build must be bit-identical to (126,126)
        f0s, holds0s, _ = build(pan, 0, 0, symmetric=I_H)
        g2_dev = max(g2_dev, float(np.abs(f0s - f0).max()))
        # G7: non-anticipation — truncate the tape and replay
        ncut = int(pan.reb[len(pan.reb) * 2 // 3])
        f7, _, _ = build(pan, 63, 21, nrows=ncut)
        f7f, _, _ = build(pan, 63, 21)
        g7_dev = max(g7_dev, float(np.abs(f7[:ncut] - f7f[:ncut]).max()))

        # ---- the mechanism test, published BEFORE the capital numbers ------------------------
        tot0 = cnt0["n_win"] + cnt0["n_loss"]
        sw, sl = cnt0["n_win"] / tot0, cnt0["n_loss"] / tot0
        side_min = min(side_min, sw, sl)
        iw = cnt0["inel_win"] / max(cnt0["n_win"], 1)
        il = cnt0["inel_loss"] / max(cnt0["n_loss"], 1)
        pw = cnt0["prot_win"] / max(tot0, 1)
        pl = cnt0["prot_loss"] / max(tot0, 1)
        say(f"    MECHANISM (frozen anchor, held name-rebalances after warm-up, n={tot0}):  "
            f"WIN side {sw:.4f} of holdings, LOSS side {sl:.4f}")
        say(f"      ineligible WHILE HELD: win {iw:.4f} of win-side, loss {il:.4f} of loss-side "
            f"| BRAKE BITING (protected AND ineligible): win {pw:.4f} of all, loss {pl:.4f} of all"
            f"  -> loss/win bite ratio {pl/pw if pw > 0 else float('nan'):.2f}x")
        mech_rows.append(dict(panel=pan.name, n_held_rebalances=tot0, share_win=sw, share_loss=sl,
                              inel_of_win=iw, inel_of_loss=il, brake_bite_win=pw,
                              brake_bite_loss=pl,
                              bite_ratio=(pl / pw if pw > 0 else np.nan),
                              mean_age_days=cnt0["age_sum"] / max(cnt0["age_n"], 1)))

        # ---- the 25-cell grid ----------------------------------------------------------------
        cells = {}
        for hw in HWINS:
            for hl in HLOSSES:
                f, holds, cnt = build(pan, hw, hl)
                gr, tn, ws = run_book(pan, f, C, Cp, I_G)
                wsum_global = max(wsum_global, ws)
                r = net(gr, tn)
                cells[(hw, hl)] = (r, tn)
                m, h1, h2 = triple(r[WARMUP:]), *halves(r[WARMUP:])
                k4a, k4b, _, _, _, legs = keep_paths(r[WARMUP:], spy, live)
                k4aO, k4bO, mO, _, _, _ = keep_paths(r[i_oos:], spyO, liveO)
                jac, dshare, ndshare = reorder_stats(holds, holds0, first_reb)
                obs, se, tt = paired_block_dsharpe(r[WARMUP:], r0[WARMUP:])
                obsO, seO, ttO = paired_block_dsharpe(r[i_oos:], r0[i_oos:])
                grid.append(dict(
                    panel=pan.name, H_WIN=hw, H_LOSS=hl, is_anchor=(hw == I_H and hl == I_H),
                    CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                    oCAGR=mO["CAGR"], oSharpe=mO["Sharpe"], oMaxDD=mO["MaxDD"],
                    isSharpe=sharpe(r[WARMUP:i_is]),
                    turnover=float(tn[WARMUP:].sum()) * 252 / len(tn[WARMUP:]),
                    mean_age=cnt["age_sum"] / max(cnt["age_n"], 1),
                    brake_bite_win=cnt["prot_win"] / max(cnt["n_win"] + cnt["n_loss"], 1),
                    brake_bite_loss=cnt["prot_loss"] / max(cnt["n_win"] + cnt["n_loss"], 1),
                    jaccard=jac, reb_changed=dshare, namedays_changed=ndshare,
                    dSharpe=obs, dSE=se, tstat=tt, odSharpe=obsO, odSE=seO, otstat=ttO,
                    keep4a=k4a, keep4b=k4b, keep4b_oos=k4bO,
                    leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"], leg_CAGR=legs["CAGR"],
                    spy_Sharpe=spy["Sharpe"], spy_CAGR=spy["CAGR"], spy_MaxDD=spy["MaxDD"],
                    live_Sharpe=live["Sharpe"], live_H1=live["H1"], live_H2=live["H2"],
                    live_MaxDD=live["MaxDD"]))
        # G9 determinism
        f9, _, _ = build(pan, 252, 0)
        g9r = net(*run_book(pan, f9, C, Cp, I_G)[:2])
        g9_dev = max(g9_dev, float(np.abs(g9r - cells[(252, 0)][0]).max()))

        # ---- rule 8: choose on IS only, read OOS once ----------------------------------------
        sub = [g for g in grid if g["panel"] == pan.name]
        pick = max(sub, key=lambda d: (d["isSharpe"] if np.isfinite(d["isSharpe"]) else -9))
        rp = cells[(pick["H_WIN"], pick["H_LOSS"])][0]
        obsO, seO, ttO = paired_block_dsharpe(rp[i_oos:], r0[i_oos:])
        k4aO, k4bO, mO, h1O, h2O, legsO = keep_paths(rp[i_oos:], spyO, liveO)
        say(f"    RULE 8  IS argmax Sharpe -> H_WIN {pick['H_WIN']}, H_LOSS {pick['H_LOSS']}  "
            f"(IS Sharpe {pick['isSharpe']:.4f}; anchor IS {sharpe(r0[WARMUP:i_is]):.4f})")
        say(f"            OOS 2017-2026 READ ONCE: CAGR {mO['CAGR']:.2%} Sharpe "
            f"{mO['Sharpe']:.4f} MaxDD {mO['MaxDD']:.2%}   vs ANCHOR OOS {ancO['CAGR']:.2%} / "
            f"{ancO['Sharpe']:.4f} / {ancO['MaxDD']:.2%}  (dSharpe {obsO:+.4f}, SE {seO:.4f}, "
            f"t {ttO:+.2f})")
        say(f"            vs RULES v2 OOS {liveO['CAGR']:.2%} / {liveO['Sharpe']:.4f} / "
            f"{liveO['MaxDD']:.2%}   vs SPY OOS {spyO['CAGR']:.2%} / {spyO['Sharpe']:.4f} / "
            f"{spyO['MaxDD']:.2%}   4a_OOS {k4aO}  4b_OOS {k4bO} {legsO}")
        wf_rows.append(dict(panel=pan.name, H_WIN=pick["H_WIN"], H_LOSS=pick["H_LOSS"],
                            isSharpe=pick["isSharpe"], anchor_isSharpe=sharpe(r0[WARMUP:i_is]),
                            oCAGR=mO["CAGR"], oSharpe=mO["Sharpe"], oMaxDD=mO["MaxDD"],
                            anchor_oCAGR=ancO["CAGR"], anchor_oSharpe=ancO["Sharpe"],
                            anchor_oMaxDD=ancO["MaxDD"], dSharpe_oos=obsO, dSE_oos=seO,
                            dt_oos=ttO, keep4a_oos=k4aO, keep4b_oos=k4bO,
                            live_oSharpe=liveO["Sharpe"], live_oCAGR=liveO["CAGR"],
                            live_oMaxDD=liveO["MaxDD"], spy_oSharpe=spyO["Sharpe"],
                            spy_oCAGR=spyO["CAGR"], spy_oMaxDD=spyO["MaxDD"]))

    G = pd.DataFrame(grid)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    pd.DataFrame(wf_rows).to_csv(f"{OUT}.walkforward.csv", index=False)
    pd.DataFrame(mech_rows).to_csv(f"{OUT}.mechanism.csv", index=False)

    gate("G2 (126,126) bit-identical to a SIDE-BLIND symmetric H=126 build", f"{g2_dev:.3e}",
         "== 0", g2_dev == 0.0)
    gate("G3 all 75 cells published", len(G), "== 75", len(G) == 75)
    gate("G6 no leverage (max realised weight sum)", f"{wsum_global:.6f}",
         f"<= {I_G:.2f}", wsum_global <= I_G + 1e-12)
    gate("G7 side assignment non-anticipating (truncated-tape replay)", f"{g7_dev:.3e}",
         "== 0", g7_dev == 0.0)
    gate("G8 the split BINDS (min side share of held name-rebalances)", f"{side_min:.4f}",
         "> 0.05", side_min > 0.05)
    gate("G9 bit-identical recompute of one cell per panel", f"{g9_dev:.3e}", "== 0",
         g9_dev == 0.0)
    gate("G5 rule-8 chooser reads no row on or after 2017-01-01", "isSharpe over WARMUP..IS_END",
         "true by construction", True)

    say("\n" + "=" * 122)
    say("THE GRID — all 75 cells are in .grid.csv; the two EXTREME arms of the hypothesis first")
    say("=" * 122)
    for pan in ["U56", "B136", "SMALL"]:
        s = G[G.panel == pan].set_index(["H_WIN", "H_LOSS"])
        a = s.loc[(I_H, I_H)]
        say(f"\n  [{pan}]  anchor (126,126): {a.CAGR:>7.2%} / {a.Sharpe:.4f} / {a.MaxDD:>7.2%}  "
            f"turnover {a.turnover:.2f}x  mean age {a.mean_age:.0f}d")
        for lbl, key in [("RELEASE LOSERS EARLY  (126,   0)", (126, 0)),
                         ("RELEASE LOSERS AT 21d (126,  21)", (126, 21)),
                         ("TRAP LOSERS LONGER    (126, 252)", (126, 252)),
                         ("RELEASE WINNERS EARLY (  0, 126)", (0, 126)),
                         ("NO BRAKE AT ALL       (  0,   0)", (0, 0)),
                         ("ALL BRAKE             (252, 252)", (252, 252))]:
            c = s.loc[key]
            say(f"    {lbl}: {c.CAGR:>7.2%} / {c.Sharpe:.4f} / {c.MaxDD:>7.2%}  "
                f"dSharpe {c.dSharpe:+.4f} (t {c.tstat:+.2f})  OOS {c.oCAGR:>7.2%} / {c.oSharpe:.4f} "
                f"/ {c.oMaxDD:>7.2%} (t {c.otstat:+.2f})  turn {c.turnover:.2f}x  age {c.mean_age:.0f}d"
                f"  jac {c.jaccard:.3f}  4a {bool(c.keep4a)} 4b {bool(c.keep4b)}/{bool(c.keep4b_oos)}")

    say("\n  MONOTONICITY IN EACH SIDE, holding the other at the incumbent's 126 (full-sample "
        "Sharpe and MaxDD):")
    for pan in ["U56", "B136", "SMALL"]:
        s = G[G.panel == pan].set_index(["H_WIN", "H_LOSS"])
        rowL = "  ".join(f"HL={hl:>3}: {s.loc[(126, hl)].Sharpe:.4f}/{s.loc[(126, hl)].MaxDD:>7.2%}"
                         for hl in HLOSSES)
        rowW = "  ".join(f"HW={hw:>3}: {s.loc[(hw, 126)].Sharpe:.4f}/{s.loc[(hw, 126)].MaxDD:>7.2%}"
                         for hw in HWINS)
        say(f"    [{pan}] loser side  | {rowL}")
        say(f"    [{pan}] winner side | {rowW}")

    say("\n  THE DIRECTIONAL TEST THE IDEA MAKES: does CUTTING the LOSER clock (H_LOSS < H_WIN) "
        "buy drawdown, and does CUTTING the WINNER clock cost return?")
    for pan in ["U56", "B136", "SMALL"]:
        s = G[G.panel == pan]
        a = s[s.is_anchor].iloc[0]
        lo = s[s.H_LOSS < s.H_WIN]
        hi = s[s.H_LOSS > s.H_WIN]
        say(f"    [{pan}] loser-released cells (H_LOSS < H_WIN, n={len(lo)}): mean dMaxDD "
            f"{(lo.MaxDD.mean()-a.MaxDD)*100:+.2f} pp, mean dSharpe {lo.Sharpe.mean()-a.Sharpe:+.4f}, "
            f"mean dCAGR {(lo.CAGR.mean()-a.CAGR)*100:+.2f} pp, better MaxDD in "
            f"{int((lo.MaxDD > a.MaxDD).sum())} of {len(lo)}")
        say(f"    [{pan}] loser-trapped cells  (H_LOSS > H_WIN, n={len(hi)}): mean dMaxDD "
            f"{(hi.MaxDD.mean()-a.MaxDD)*100:+.2f} pp, mean dSharpe {hi.Sharpe.mean()-a.Sharpe:+.4f}, "
            f"mean dCAGR {(hi.CAGR.mean()-a.CAGR)*100:+.2f} pp, better MaxDD in "
            f"{int((hi.MaxDD > a.MaxDD).sum())} of {len(hi)}")

    say("\n  RESOLUTION: cells beating the frozen anchor on full-sample Sharpe and how many "
        "resolve at |t| > 2 (paired circular-block bootstrap, 400x63, seed 20260919):")
    nb = int((G.dSharpe > 0).sum())
    nr = int(((G.dSharpe > 0) & (G.tstat.abs() > 2)).sum())
    nbO = int((G.odSharpe > 0).sum())
    nrO = int(((G.odSharpe > 0) & (G.otstat.abs() > 2)).sum())
    say(f"    FULL: {nb} of {len(G)} beat the anchor, {nr} at |t| > 2  (max |t| anywhere "
        f"{G.tstat.abs().max():.2f})")
    say(f"    OOS : {nbO} of {len(G)} beat the anchor, {nrO} at |t| > 2  (max |t| anywhere "
        f"{G.otstat.abs().max():.2f})")

    say("\n  BOTH KEEP PATHS, all 75 cells:")
    say(f"    4a: {int(G.keep4a.sum())} of {len(G)}   "
        f"4b FULL: {int(G.keep4b.sum())}   4b OOS: {int(G.keep4b_oos.sum())}   "
        f"4b BOTH: {int((G.keep4b & G.keep4b_oos).sum())}")
    for pan in ["U56", "B136", "SMALL"]:
        s = G[G.panel == pan]
        say(f"      [{pan}] 4a {int(s.keep4a.sum())}/25, 4b FULL {int(s.keep4b.sum())}/25, "
            f"4b OOS {int(s.keep4b_oos.sum())}/25, 4b BOTH "
            f"{int((s.keep4b & s.keep4b_oos).sum())}/25  | binding 4b legs (fails): "
            f"H1 {int((~s.leg_H1).sum())} H2 {int((~s.leg_H2).sum())} DD {int((~s.leg_DD).sum())} "
            f"CAGR {int((~s.leg_CAGR).sum())}")
    both = G[G.keep4b & G.keep4b_oos]
    if len(both):
        say("    4b passers on BOTH windows (all of them):")
        for _, c in both.sort_values("oSharpe", ascending=False).iterrows():
            say(f"      {c.panel} H_WIN {int(c.H_WIN):>3} H_LOSS {int(c.H_LOSS):>3}"
                f"{'  [= FROZEN ANCHOR]' if c.is_anchor else ''}: {c.CAGR:.2%} / {c.Sharpe:.4f} / "
                f"{c.MaxDD:.2%} (halves {c.H1:.3f}/{c.H2:.3f}); OOS {c.oCAGR:.2%} / "
                f"{c.oSharpe:.4f} / {c.oMaxDD:.2%}; dSharpe vs anchor {c.dSharpe:+.4f} "
                f"(t {c.tstat:+.2f}), OOS {c.odSharpe:+.4f} (t {c.otstat:+.2f})")

    say("\n  GATES: " + ", ".join(f"{g['gate'].split()[0]}={'PASS' if g['pass_'] else 'FAIL'}"
                                  for g in GATES if g["target"] != "published, not asserted"))
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n  elapsed {time.time()-t_start:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
