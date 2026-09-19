#!/usr/bin/env python3
"""
Idea 1566 (lane C, 2026-09-19) — is MIN-HOLD RETENTION SILENTLY DISARMING every ELIGIBILITY
DEVICE in the record?

THE DEFECT THIS RUN PRICES.  Idea 1538 carried a MAXVOL ladder down to m = 0.06 and could not
empty the book at ANY ceiling (mean flat_one 0.0017-0.0101).  The reason it gave: the incumbent's
min-hold clause H = 126 RETAINS a held name regardless of its eligibility, so on U56 the ELIGIBLE
SET is empty on 2.5% of days at m = 0.10 while the BOOK is flat on 0.00%.  If that mechanism is
general, then EVERY eligibility device the record owns — the MAXVOL ceiling, the per-name 200d MA
gate, the +/-3% band — is filtered through the same retention clause, and each one's measured
effect is an effect on ENTRY ONLY.  That would make the live rules' MAXVOL 0.60 inheritance a rule
that does close to nothing, and it would mean every eligibility result in the record was read at
one particular H without that H being named as the thing doing the work.

WHAT IS MEASURED, AND IT IS TWO THINGS, NOT ONE.

  (A) THE DISARMAMENT ITSELF, directly.  For each device and each H, the share of BOOK-DAYS on
      which the device's own verdict is OVERRIDDEN by retention — i.e. the book holds a name the
      device says is INELIGIBLE, purely because that name is younger than H.  Three readings, all
      published.  The HEADLINE reading is OVRC_W: the mean share of BOOK WEIGHT sitting in names
      RETAINED BY AGE although THAT DEVICE'S OWN CLAUSE (its vol ceiling, its MA gate, its band —
      not whatever else the config it sits in also filters on) says INELIGIBLE, so the number is
      attributable to the device.  OVRC_DAY is the share of book-days carrying at least one such
      name.  Beside them, the CONFIG-level readings OVR_W and OVR_SEL (weight share, and share of
      selection slots, failing the ON config's FULL eligibility) are published for continuity with
      how the record has been reading eligibility to date; note that two devices sharing an ON
      config necessarily share those, which is exactly why the clause-level reading exists.

  (B) THE PRICE.  The device's Sharpe and MaxDD CONTRAST against its own device-OFF twin, re-cut
      at H {0, 21, 63, 126, 252} on three panels, with a paired circular-block bootstrap SE on the
      dSharpe so a null contrast can be told from a small one.  Both KEEP paths are evaluated at
      every one of the 75 cells against live RULES v2 AND SPY, full sample and 2017-2026, and the
      rule-8 chooser over the (device, H) grid reads 2017-2026 ONCE.

THE FOUR DEVICES (each an ON book and an OFF twin differing in ONE eligibility clause and nothing
else — the SCORE KEY is held bit-identical across all five configs, built from the band-0 200d MA
tilt, so the contrast isolates the ELIGIBILITY clause and never the ranking):

  config  A INCUMBENT   MA gate band 0.00   MAXVOL 0.60     (the frozen incumbent, N=20, g=0.75, W)
          B NOVOL       MA gate band 0.00   MAXVOL none
          C VOL035      MA gate band 0.00   MAXVOL 0.35
          D NOMA        no MA gate          MAXVOL 0.60
          E BAND03      MA gate band 0.03   MAXVOL 0.60

  DEV_MAXVOL060  A vs B   the LIVE inheritance — the device idea 1566 names explicitly
  DEV_MAXVOL035  C vs B   the same device at a rung tight enough to bite
  DEV_MA200      A vs D   the per-name 200d MA gate
  DEV_BAND03     E vs A   the +/-3% hysteresis band on top of that gate

THE TWO DIALS AND NO MORE (PROTOCOL rule 4), and they are the idea's own two:
  DIAL 1  DEVICE   {DEV_MAXVOL060, DEV_MAXVOL035, DEV_MA200, DEV_BAND03}
  DIAL 2  H        {0, 21, 63, 126, 252}
5 configs x 5 H x 3 panels = 75 books, EVERY ONE published in .grid.csv; 4 devices x 5 H x 3
panels = 60 contrasts, every one published in .contrast.csv.

PRE-REGISTERED BARS — written here BEFORE any number of this run was read, so the idea can fail:

  (T1) DISARMAMENT EXISTS.  At the incumbent H = 126, at least one device carries OVRC_W >= 0.10
       on EVERY panel.  (Below that bar, retention is a rounding error and the idea is wrong.)
  (T2) DISARMAMENT IS MONOTONE IN H.  OVRC_W is non-decreasing across the five H rungs for every
       device x panel ladder (12 ladders).  A device disarmed by retention must be disarmed MORE
       by more retention.
  (T3) THE HEADLINE — IS THE LIVE MAXVOL 0.60 INHERITANCE INERT AT H = 126?  It is called INERT
       iff |dSharpe(A - B)| at H = 126 is inside ONE paired-bootstrap SE on all three panels.
       Reported beside the same contrast at H = 0, which is the device with retention switched
       off entirely.
  (T4) RETENTION SHRINKS THE MEASURED EFFECT.  For each of the four devices, |dSharpe| at H = 0
       exceeds |dSharpe| at H = 126 on at least 2 of 3 panels.  This is the idea's general claim;
       T3 is the one live special case.
  (T5) CAPITAL.  The rule-8 chooser over the 25-cell (config, H) grid, fitted on IS rows only,
       beats DOING NOTHING (the frozen incumbent) on mean OOS Sharpe across the three panels.

THE IDEA IS UPHELD iff T1 & T2 & T4.  T3 answers the live-rule sub-question and T5 is the capital
arm; either can go the other way without touching the mechanism verdict, and is reported as it
falls.

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1 execution, 10 bps, no leverage, no shorting — every device
DE-GROSSES the book toward cash by shrinking the eligible set and never levers); rule 3 (live
RULES v2 AND SPY); rule 4 (both KEEP paths, exactly 2 tuned parameters); rule 8 (walk-forward,
2017-2026 read ONCE); rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py are NOT modified.

GATES.  G0 sample >= 10y on every panel.  G1 CROSS-SCRIPT REPLAY of the committed 2026-09-04 U56
anchor (15.80% / 1.1537 / -19.13% full; 1.1857 OOS) by config A at H = 126.  G2 all 75 cells
published.  G3 exactly two tuned parameters.  G4 the rule-8 chooser reads no row on or after
2017-01-01.  G5 NO LEVERAGE: max DRIFTED book gross <= 1.0 at every row of every cell (the
target gross is 0.75 at each rebalance; between weekly rebalances the equity sleeve drifts against
a fixed cash sleeve, so gross rises above 0.75 with no borrowing — 1.0 is the borrowing line).  G6
deterministic recompute of one cell per panel, bit-identical.  G7 NON-ANTICIPATION: a truncated-
tape replay of one cell per panel is bit-identical on the truncated prefix.  G8 the override
census is INTERNALLY CONSISTENT: both override readings are exactly 0 at H = 0 on every device and
panel (with no retention there is nothing to override) — if this fails the instrument is measuring something
other than retention.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-19_min-hold-retention-disarms-eligibility-devices_C.py
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
SLUG = "min-hold-retention-disarms-eligibility-devices"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP = 260
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_G, I_H = 20, 0.75, 126                      # the frozen incumbent's non-eligibility dials
COST = 10.0
OOS_START, IS_END = "2017-01-01", "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BOOT_REPS, BOOT_BLOCK, BOOT_SEED = 400, 63, 20260919
C_U56 = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857)

H_LADDER = [0, 21, 63, 126, 252]                   # DIAL 2
CONFIGS = {                                        # band, maxvol (np.inf = no ceiling), ma_gate
    "A_INCUMBENT": dict(band=0.00, maxvol=0.60, ma=True),
    "B_NOVOL":     dict(band=0.00, maxvol=np.inf, ma=True),
    "C_VOL035":    dict(band=0.00, maxvol=0.35, ma=True),
    "D_NOMA":      dict(band=0.00, maxvol=0.60, ma=False),
    "E_BAND03":    dict(band=0.03, maxvol=0.60, ma=True),
}
DEVICES = {                                        # DIAL 1: (ON config, OFF config, description)
    "DEV_MAXVOL060": ("A_INCUMBENT", "B_NOVOL",     "the LIVE MAXVOL 0.60 inheritance"),
    "DEV_MAXVOL035": ("C_VOL035",    "B_NOVOL",     "MAXVOL at a rung tight enough to bite"),
    "DEV_MA200":     ("A_INCUMBENT", "D_NOMA",      "the per-name 200d MA eligibility gate"),
    "DEV_BAND03":    ("E_BAND03",    "A_INCUMBENT", "the +/-3% hysteresis band on that gate"),
}
OVR_BAR = 0.10          # T1
ANCHOR = ("A_INCUMBENT", 126)

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


# ---------------------------------------------------------------------------------------------
# statistics
# ---------------------------------------------------------------------------------------------
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
    """4a against the LIVE book (rule 4a), 4b against SPY (rule 4b, the capital path)."""
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(h1 > bm["H1"]), H2=bool(h2 > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


def paired_block_dsharpe(a, b, reps=BOOT_REPS, L=BOOT_BLOCK, seed=BOOT_SEED):
    """Paired circular-block bootstrap of Sharpe(a) - Sharpe(b): the SAME block draw is applied to
    both legs, so the market factor they share cancels instead of inflating the SE."""
    a, b = np.asarray(a, float), np.asarray(b, float)
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


def paired_block_dmdd(a, b, reps=BOOT_REPS, L=BOOT_BLOCK, seed=BOOT_SEED):
    a, b = np.asarray(a, float), np.asarray(b, float)
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    nb = int(np.ceil(n / L))
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n, size=(reps, nb))
    idx = (starts[:, :, None] + np.arange(L)[None, None, :]).reshape(reps, nb * L)[:, :n] % n

    def md(X):
        e = np.cumprod(1 + X, axis=1)
        return (e / np.maximum.accumulate(e, axis=1) - 1).min(axis=1)

    d = md(a[idx]) - md(b[idx])
    obs = float(mdd(a) - mdd(b))
    se = float(np.nanstd(d, ddof=1))
    return obs, se, (obs / se if se > 0 else np.nan)


# ---------------------------------------------------------------------------------------------
# the panel and the selection frame
# ---------------------------------------------------------------------------------------------
def mech_legs(q: pd.DataFrame):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return (sum(parts) / len(parts)).values


def band_gate(q: pd.DataFrame, band: float):
    ma = q.rolling(200).mean()
    if band <= 0.0:
        return (q > ma).values
    raw = pd.DataFrame(np.nan, index=q.index, columns=q.columns)
    raw = raw.mask(q > ma * (1 + band), 1.0).mask(q < ma * (1 - band), 0.0)
    return (raw.ffill().fillna(0.0) > 0.5).values


def cadence_rows(idx, cad="W"):
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
        self._gate = {}
        self.reb = cadence_rows(px.index, "W")
        # THE SCORE KEY IS ONE OBJECT FOR ALL FIVE CONFIGS (band-0 MA tilt), so a device contrast
        # is a contrast in ELIGIBILITY and never in RANKING.
        above0 = self.gate_of(0.00)
        sc = self.comp * (0.5 + 0.5 * above0.astype(float))
        self.key = np.where(np.isfinite(sc), -sc, np.inf)

    def gate_of(self, band):
        if band not in self._gate:
            self._gate[band] = band_gate(self.q, band)
        return self._gate[band]

    def clause_of(self, device):
        """The SINGLE clause a device switches on, as a (T, K) mask, True = the clause says the
        name is ELIGIBLE.  This is what the device's own verdict IS, independent of whatever else
        the ON config also filters on — so the override census below attributes to the DEVICE and
        not to the config it happens to sit in."""
        if device == "DEV_MAXVOL060":
            return np.nan_to_num(self.vol20, nan=1e9) < 0.60
        if device == "DEV_MAXVOL035":
            return np.nan_to_num(self.vol20, nan=1e9) < 0.35
        if device == "DEV_MA200":
            return self.gate_of(0.00)
        if device == "DEV_BAND03":
            return self.gate_of(0.03)
        raise KeyError(device)

    def elig_of(self, cfg, nrows=None):
        T = len(self.idx) if nrows is None else nrows
        ok = np.ones((T, len(self.iinv)), bool)
        if cfg["ma"]:
            ok &= self.gate_of(cfg["band"])[:T]
        if np.isfinite(cfg["maxvol"]):
            ok &= np.nan_to_num(self.vol20[:T], nan=1e9) < cfg["maxvol"]
        return ok


def build_frame(pan, elig, N, H, nrows=None, lag=1):
    """The incumbent's selection frame, INSTRUMENTED.  Retention clause verbatim: a held name
    younger than H is kept REGARDLESS of its eligibility; free slots go to the best eligible
    names by the frozen key.  Returns the daily target frame plus the override census."""
    T = pan.rets.shape[0] if nrows is None else nrows
    M = pan.rets.shape[1]
    K = len(pan.iinv)
    W = np.zeros((T, M))
    ovr_w = np.zeros(T)            # share of BOOK WEIGHT in names the CONFIG calls ineligible
    ovr_any = np.zeros(T, bool)    # book-day carries >= 1 overridden name
    held_n = np.zeros(T)
    retained = np.zeros((T, K), bool)   # names held ONLY because they are younger than H
    dec = np.zeros(T, np.int64)         # the decision row ts governing each day
    n_sel_slots = 0
    n_sel_ovr = 0
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    reb = pan.reb[pan.reb < T]
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
            k = pan.key[ts].copy()
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
        dec[t:stop] = ts
        if len(keep):
            retained[t:stop, np.array(sorted(keep), dtype=np.int64)] = True
        if len(sel):
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
            bad = [c for c in keep if not (elig[ts][c] and pr[ts][c])]
            ovr_w[t:stop] = len(bad) / len(sel)
            ovr_any[t:stop] = len(bad) > 0
            held_n[t:stop] = len(sel)
            n_sel_slots += len(sel)
            n_sel_ovr += len(bad)
    diag = dict(ovr_w=ovr_w, ovr_any=ovr_any, held_n=held_n, retained=retained, dec=dec,
                sel_slots=n_sel_slots, sel_ovr=n_sel_ovr)
    return W, diag


def run_book(pan, frame, g=I_G, nrows=None):
    """Daily engine: weights decided at the rebalance row (which already carries the t-1 decision,
    see cadence_rows) and held between; 10 bps on realised turnover; never levers."""
    T = pan.rets.shape[0] if nrows is None else nrows
    M = pan.rets.shape[1]
    rets = pan.rets
    isreb = np.zeros(T, bool)
    isreb[pan.reb[pan.reb < T]] = True
    rnet = np.zeros(T)
    turn = np.zeros(T)
    cur = np.zeros(M)
    wsum = 0.0
    for t in range(T):
        post = g * frame[t] if isreb[t] else cur
        tr = float(np.abs(post - cur).sum())
        r = float(post @ rets[t])
        rnet[t] = r - tr * COST / 1e4
        turn[t] = tr
        wsum = max(wsum, float(post.sum()))
        cur = post * (1.0 + rets[t]) / (1.0 + r)
    return dict(rnet=rnet, turn=turn, wsum=wsum)


# ---------------------------------------------------------------------------------------------
def main():
    t0 = time.time()
    say("=" * 124)
    say("IDEA 1566 (lane C, 2026-09-19) — IS MIN-HOLD RETENTION SILENTLY DISARMING EVERY "
        "ELIGIBILITY DEVICE IN THE RECORD?")
    say("=" * 124)
    say("5 configs x 5 H rungs x 3 panels = 75 books, every one published; 4 devices x 5 H x 3 "
        "panels = 60 contrasts.")
    say("DIAL 1 device {DEV_MAXVOL060, DEV_MAXVOL035, DEV_MA200, DEV_BAND03};  "
        "DIAL 2 H {0, 21, 63, 126, 252}.")
    say(f"PRE-REGISTERED: T1 some device OVRC_W >= {OVR_BAR} at H=126 on every panel; T2 OVRC_W "
        "non-decreasing in H on all 12 ladders; T3 |dSharpe| of the LIVE MAXVOL 0.60 inside 1 SE "
        "at H=126 on all 3 panels (= INERT); T4 |dSharpe| at H=0 > at H=126 on >= 2 of 3 panels "
        "for each device; T5 rule-8 chooser beats doing nothing on mean OOS Sharpe.")
    say("UPHELD iff T1 & T2 & T4.")
    say("=" * 124)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0; {len(inv)} investable names survive.")

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, SMALL {len(inv)}.")
    say("  SURVIVORSHIP (rule 9): U56 and B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010, so every ABSOLUTE level below is an UPPER BOUND.  "
        "What this run reads is a CONTRAST between two books over the SAME names on the SAME days "
        "differing in ONE eligibility clause, which the bias cannot manufacture.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y)")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)", round(min(len(p.idx) for p in panels) / 252.0, 2),
         ">= 10.0", min(len(p.idx) for p in panels) / 252.0 >= 10.0)
    gate("G3 exactly two tuned parameters (device, H)", 2, "== 2", True)

    grid, contrasts, wf_rows = [], [], []
    wsum_global, g1_ok = 0.0, None
    g6_dev, g7_dev = 0.0, 0.0

    for pan in panels:
        T = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        i_is = int(np.searchsorted(pan.idx.values, np.datetime64(IS_END)))
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])

        say(f"\n  [{pan.name}]  SPY CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.4f} MaxDD "
            f"{spy['MaxDD']:.2%} H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap "
            f"{DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps CAGR {live['CAGR']:.2%} Sharpe {live['Sharpe']:.4f} "
            f"MaxDD {live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f}")
        say(f"           OOS SPY {spyO['CAGR']:.2%}/{spyO['Sharpe']:.4f}/{spyO['MaxDD']:.2%}  |  "
            f"OOS RULES v2 {liveO['CAGR']:.2%}/{liveO['Sharpe']:.4f}/{liveO['MaxDD']:.2%}")

        books = {}
        elig_cache = {c: pan.elig_of(CONFIGS[c]) for c in CONFIGS}
        for cname, cfg in CONFIGS.items():
            for H in H_LADDER:
                frame, diag = build_frame(pan, elig_cache[cname], I_N, H)
                bk = run_book(pan, frame)
                wsum_global = max(wsum_global, bk["wsum"])
                books[(cname, H)] = dict(
                    rnet=bk["rnet"], turn=bk["turn"],
                    held=(frame > 0)[:, pan.iinv].copy(),
                    ovr_w=diag["ovr_w"], ovr_any=diag["ovr_any"], held_n=diag["held_n"],
                    retained=diag["retained"], dec=diag["dec"],
                    sel_slots=diag["sel_slots"], sel_ovr=diag["sel_ovr"])
                del frame

        anch = books[ANCHOR]["rnet"]
        am, ao = triple(anch[WARMUP:]), triple(anch[i_oos:])
        ah1, ah2 = halves(anch[WARMUP:])
        say(f"           FROZEN INCUMBENT (A_INCUMBENT, H=126)  CAGR {am['CAGR']:.2%} Sharpe "
            f"{am['Sharpe']:.4f} MaxDD {am['MaxDD']:.2%} H1/H2 {ah1:.4f}/{ah2:.4f} | OOS "
            f"{ao['CAGR']:.2%}/{ao['Sharpe']:.4f}/{ao['MaxDD']:.2%}")
        if pan.name == "U56":
            d = max(abs(am["Sharpe"] - C_U56["Sharpe"]), abs(ao["Sharpe"] - C_U56["oSharpe"]),
                    abs(am["CAGR"] - C_U56["CAGR"]), abs(am["MaxDD"] - C_U56["MaxDD"]))
            g1_ok = gate("G1 cross-script replay of the committed 2026-09-04 U56 anchor "
                         "(15.80%/1.1537/-19.13% full; 1.1857 OOS)",
                         f"max |dev| {d:.2e} (got {am['CAGR']:.4f}/{am['Sharpe']:.4f}/"
                         f"{am['MaxDD']:.4f}; OOS {ao['Sharpe']:.4f})", "< 5e-3", d < 5e-3)

        # ---- the 25 cells of this panel -------------------------------------------------------
        for (cname, H), bk in books.items():
            r = bk["rnet"]
            k4a, k4b, m, h1, h2, legs = keep_paths(r[WARMUP:], spy, live)
            k4aO, k4bO, mo, _, _, legsO = keep_paths(r[i_oos:], spyO, liveO)
            dsh, se, tt = paired_block_dsharpe(r[WARMUP:], anch[WARMUP:])
            dshO, seO, tO = paired_block_dsharpe(r[i_oos:], anch[i_oos:])
            row = dict(panel=pan.name, config=cname, H=H,
                       CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                       OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                       IS_Sharpe=sharpe(r[WARMUP:i_is]),
                       turn_yr=float(bk["turn"][WARMUP:].mean() * 252),
                       OVR_W=float(bk["ovr_w"][WARMUP:].mean()),
                       OVR_DAY=float(bk["ovr_any"][WARMUP:].mean()),
                       OVR_SEL=float(bk["sel_ovr"] / max(bk["sel_slots"], 1)),
                       mean_held=float(bk["held_n"][WARMUP:].mean()),
                       dSharpe_vs_anchor=dsh, dSharpe_se=se, dSharpe_t=tt,
                       OOS_dSharpe_vs_anchor=dshO, OOS_dSharpe_t=tO,
                       keep4a=k4a, keep4b=k4b, keep4a_OOS=k4aO, keep4b_OOS=k4bO,
                       **{f"leg_{k}": v for k, v in legs.items()},
                       **{f"legO_{k}": v for k, v in legsO.items()})
            grid.append(row)

        # ---- the 20 device contrasts of this panel --------------------------------------------
        for dname, (on, off, desc) in DEVICES.items():
            for H in H_LADDER:
                A, B = books[(on, H)], books[(off, H)]
                ds, ses, ts_ = paired_block_dsharpe(A["rnet"][WARMUP:], B["rnet"][WARMUP:])
                dd, sed, td = paired_block_dmdd(A["rnet"][WARMUP:], B["rnet"][WARMUP:])
                dsO, seO, tO = paired_block_dsharpe(A["rnet"][i_oos:], B["rnet"][i_oos:])
                cl = pan.clause_of(dname)
                bad = A["retained"] & ~cl[A["dec"]]          # retained though the CLAUSE says no
                nbad = bad.sum(axis=1)[WARMUP:].astype(float)
                den = np.maximum(A["held_n"][WARMUP:], 1.0)
                ovrc_w = float(np.mean(nbad / den))
                ovrc_day = float(np.mean(nbad > 0))
                ha, hb = A["held"][WARMUP:], B["held"][WARMUP:]
                ident = float((ha == hb).all(axis=1).mean())
                jac_num = (ha & hb).sum(axis=1)
                jac_den = (ha | hb).sum(axis=1)
                jac = float(np.mean(np.where(jac_den > 0, jac_num / np.maximum(jac_den, 1), 1.0)))
                contrasts.append(dict(
                    panel=pan.name, device=dname, H=H, on=on, off=off, desc=desc,
                    OVRC_W=ovrc_w, OVRC_DAY=ovrc_day,
                    OVR_W_on=float(A["ovr_w"][WARMUP:].mean()),
                    OVR_DAY_on=float(A["ovr_any"][WARMUP:].mean()),
                    OVR_SEL_on=float(A["sel_ovr"] / max(A["sel_slots"], 1)),
                    dSharpe=ds, dSharpe_se=ses, dSharpe_t=ts_,
                    dMaxDD=dd, dMaxDD_se=sed, dMaxDD_t=td,
                    dCAGR=cagr(A["rnet"][WARMUP:]) - cagr(B["rnet"][WARMUP:]),
                    OOS_dSharpe=dsO, OOS_dSharpe_t=tO,
                    ident_share=ident, jaccard=jac,
                    Sharpe_on=sharpe(A["rnet"][WARMUP:]), Sharpe_off=sharpe(B["rnet"][WARMUP:]),
                    MaxDD_on=mdd(A["rnet"][WARMUP:]), MaxDD_off=mdd(B["rnet"][WARMUP:])))

        # ---- rule 8: the chooser over the 25-cell (config, H) grid -----------------------------
        cells = list(books.keys())
        is_sh = {c: sharpe(books[c]["rnet"][WARMUP:i_is]) for c in cells}
        pick = max(cells, key=lambda c: (-1e9 if not np.isfinite(is_sh[c]) else is_sh[c]))
        for label, cell in [("ARGMAX-IS (all 25 cells)", pick), ("DO NOTHING (frozen incumbent)",
                                                                ANCHOR)]:
            r = books[cell]["rnet"]
            k4aO, k4bO, mo, _, _, legsO = keep_paths(r[i_oos:], spyO, liveO)
            dsO, seO, tO = paired_block_dsharpe(r[i_oos:], anch[i_oos:])
            wf_rows.append(dict(panel=pan.name, chooser=label, cell=f"{cell[0]}|H{cell[1]}",
                                IS_Sharpe=is_sh[cell], OOS_CAGR=mo["CAGR"],
                                OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                anchor_OOS_CAGR=ao["CAGR"], anchor_OOS_Sharpe=ao["Sharpe"],
                                anchor_OOS_MaxDD=ao["MaxDD"],
                                spy_OOS_CAGR=spyO["CAGR"], spy_OOS_Sharpe=spyO["Sharpe"],
                                spy_OOS_MaxDD=spyO["MaxDD"],
                                live_OOS_CAGR=liveO["CAGR"], live_OOS_Sharpe=liveO["Sharpe"],
                                live_OOS_MaxDD=liveO["MaxDD"],
                                odSharpe=dsO, odSharpe_t=tO, keep4a_OOS=k4aO, keep4b_OOS=k4bO))
        # per-device rule-8 H pick, so the record can see which H an IS-only chooser would set
        for dname, (on, off, desc) in DEVICES.items():
            hh = max(H_LADDER, key=lambda H: (-1e9 if not np.isfinite(is_sh[(on, H)])
                                              else is_sh[(on, H)]))
            r = books[(on, hh)]["rnet"]
            k4aO, k4bO, mo, _, _, _ = keep_paths(r[i_oos:], spyO, liveO)
            wf_rows.append(dict(panel=pan.name, chooser=f"ARGMAX-IS within {dname}",
                                cell=f"{on}|H{hh}", IS_Sharpe=is_sh[(on, hh)],
                                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                OOS_MaxDD=mo["MaxDD"],
                                anchor_OOS_CAGR=ao["CAGR"], anchor_OOS_Sharpe=ao["Sharpe"],
                                anchor_OOS_MaxDD=ao["MaxDD"],
                                spy_OOS_CAGR=spyO["CAGR"], spy_OOS_Sharpe=spyO["Sharpe"],
                                spy_OOS_MaxDD=spyO["MaxDD"],
                                live_OOS_CAGR=liveO["CAGR"], live_OOS_Sharpe=liveO["Sharpe"],
                                live_OOS_MaxDD=liveO["MaxDD"],
                                odSharpe=np.nan, odSharpe_t=np.nan,
                                keep4a_OOS=k4aO, keep4b_OOS=k4bO))

        # ---- G6 determinism and G7 non-anticipation -------------------------------------------
        f2, _ = build_frame(pan, elig_cache["A_INCUMBENT"], I_N, I_H)
        r2 = run_book(pan, f2)["rnet"]
        g6_dev = max(g6_dev, float(np.abs(r2 - anch).max()))
        ncut = int(0.7 * T)
        ec = pan.elig_of(CONFIGS["A_INCUMBENT"], nrows=ncut)
        f3, _ = build_frame(pan, ec, I_N, I_H, nrows=ncut)
        r3 = run_book(pan, f3, nrows=ncut)["rnet"]
        g7_dev = max(g7_dev, float(np.abs(r3 - anch[:ncut]).max()))
        del books, f2, f3

    G = pd.DataFrame(grid)
    P = pd.DataFrame(contrasts)
    W = pd.DataFrame(wf_rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    P.to_csv(f"{OUT}.contrast.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    gate("G2 all 75 cells published (5 configs x 5 H x 3 panels)", len(G), "== 75", len(G) == 75)
    gate("G5 no leverage: max DRIFTED book gross over every cell and row (target gross is "
         f"{I_G:.2f} at each rebalance; between weekly rebalances the equity sleeve drifts against "
         "a FIXED cash sleeve, which raises gross without borrowing — the no-leverage condition is "
         "gross <= 1)", f"{wsum_global:.6f}", "<= 1.0", wsum_global <= 1.0 + 1e-12)
    gate("G6 deterministic recompute of the incumbent cell (max |dev| over 3 panels)",
         f"{g6_dev:.2e}", "== 0", g6_dev == 0.0)
    gate("G7 non-anticipation: truncated-tape replay of the incumbent cell on its prefix "
         "(max |dev| over 3 panels)", f"{g7_dev:.2e}", "== 0", g7_dev == 0.0)
    return G, P, W, t0


# ---------------------------------------------------------------------------------------------
def analyse(G, P, W, t0):
    say("\n" + "=" * 124)
    say("(1) THE DISARMAMENT CENSUS — share of the book the device's OWN CLAUSE says is INELIGIBLE "
        "and retention holds anyway.")
    say("    OVRC_W / OVRC_DAY = weight share / day share overridden against THAT DEVICE'S OWN "
        "clause (the attributable reading).")
    say("    OVR_W / OVR_SEL = the same against the ON config's FULL eligibility (the reading the "
        "record has used to date; two devices sharing an ON config necessarily share it).")
    say("=" * 124)
    for pan in ["U56", "B136", "SMALL"]:
        say(f"\n    [{pan}]  " + "  ".join(f"H={H:<4}" for H in H_LADDER))
        for dname, (on, off, desc) in DEVICES.items():
            s = P[(P.panel == pan) & (P.device == dname)].set_index("H")
            say(f"      {dname:<14} OVRC_W  " +
                "  ".join(f"{s.loc[H,'OVRC_W']:.4f}" for H in H_LADDER) + f"   ({desc})")
            say(f"      {'':<14} OVRC_DAY" +
                "  ".join(f"{s.loc[H,'OVRC_DAY']:.4f}" for H in H_LADDER))
            say(f"      {'':<14} OVR_W   " +
                "  ".join(f"{s.loc[H,'OVR_W_on']:.4f}" for H in H_LADDER) + "   [config-level]")
            say(f"      {'':<14} OVR_SEL " +
                "  ".join(f"{s.loc[H,'OVR_SEL_on']:.4f}" for H in H_LADDER) + "   [config-level]")

    t1_ok = True
    for pan in ["U56", "B136", "SMALL"]:
        s = P[(P.panel == pan) & (P.H == I_H)]
        best = s.loc[s.OVRC_W.idxmax()]
        ok = best.OVRC_W >= OVR_BAR
        t1_ok &= bool(ok)
        say(f"    T1 [{pan}] max OVRC_W at H={I_H} is {best.OVRC_W:.4f} ({best.device}); per "
            f"device " + ", ".join(f"{r.device.replace('DEV_',''):s} {r.OVRC_W:.4f}"
                                   for _, r in s.iterrows())
            + f" vs bar {OVR_BAR}: {'PASS' if ok else 'FAIL'}")
    gate("T1 DISARMAMENT EXISTS (some device's OWN-CLAUSE OVRC_W >= 0.10 at H=126 on every panel)",
         t1_ok, "True", t1_ok)

    viol = []
    for pan in ["U56", "B136", "SMALL"]:
        for dname in DEVICES:
            s = P[(P.panel == pan) & (P.device == dname)].sort_values("H")
            v = np.diff(s.OVRC_W.values)
            if (v < -1e-12).any():
                viol.append(f"{pan}/{dname} (min step {v.min():+.5f})")
    gate("T2 OVRC_W NON-DECREASING IN H on all 12 device x panel ladders",
         f"{12 - len(viol)}/12 monotone" + (f"; violations: {', '.join(viol)}" if viol else ""),
         "12/12", len(viol) == 0)

    g8 = float(max(P[P.H == 0].OVRC_W.abs().max(), P[P.H == 0].OVR_W_on.abs().max()))
    gate("G8 override census internally consistent (OVRC_W and OVR_W exactly 0 at H = 0)",
         f"{g8:.2e}", "== 0", g8 == 0.0)

    say("\n" + "=" * 124)
    say("(2) THE PRICE — the device's Sharpe and MaxDD contrast against its OWN device-OFF twin, "
        "re-cut at every H.")
    say("    dSharpe / dMaxDD = ON minus OFF, paired circular-block bootstrap (L=63, 400 reps).  "
        "ident = share of book-days the two books hold the IDENTICAL set.")
    say("=" * 124)
    for pan in ["U56", "B136", "SMALL"]:
        say(f"\n    [{pan}]")
        say(f"      {'device':<15}{'H':>5}{'OVRC_W':>8}{'dSharpe':>10}{'SE':>8}{'t':>7}"
            f"{'dMaxDD':>9}{'SE':>7}{'dCAGR':>9}{'ident':>8}{'jacc':>7}{'OOS dS':>9}")
        for dname in DEVICES:
            for H in H_LADDER:
                r = P[(P.panel == pan) & (P.device == dname) & (P.H == H)].iloc[0]
                say(f"      {dname:<15}{H:>5}{r.OVRC_W:>8.4f}{r.dSharpe:>+10.4f}"
                    f"{r.dSharpe_se:>8.4f}"
                    f"{r.dSharpe_t:>+7.2f}{r.dMaxDD:>+9.2%}{r.dMaxDD_se:>7.2%}"
                    f"{r.dCAGR:>+9.2%}{r.ident_share:>8.3f}{r.jaccard:>7.3f}"
                    f"{r.OOS_dSharpe:>+9.4f}")

    say("\n" + "-" * 124)
    say("    T3 — IS THE LIVE MAXVOL 0.60 INHERITANCE INERT AT H = 126?")
    inert = True
    for pan in ["U56", "B136", "SMALL"]:
        a = P[(P.panel == pan) & (P.device == "DEV_MAXVOL060") & (P.H == I_H)].iloc[0]
        z = P[(P.panel == pan) & (P.device == "DEV_MAXVOL060") & (P.H == 0)].iloc[0]
        ok = abs(a.dSharpe) < a.dSharpe_se
        inert &= bool(ok)
        say(f"      [{pan}] H=126 dSharpe {a.dSharpe:+.4f} (SE {a.dSharpe_se:.4f}, |t| "
            f"{abs(a.dSharpe_t):.2f}) -> {'INSIDE 1 SE' if ok else 'OUTSIDE 1 SE'};  "
            f"H=0 dSharpe {z.dSharpe:+.4f} (SE {z.dSharpe_se:.4f}), dCAGR {z.dCAGR:+.2%} vs "
            f"{a.dCAGR:+.2%}, OVR_W {a.OVR_W_on:.4f}")
    gate("T3 LIVE MAXVOL 0.60 INERT AT H = 126 (|dSharpe| inside 1 paired SE on all 3 panels)",
         inert, "True", inert)

    say("\n    T4 — DOES RETENTION SHRINK THE MEASURED EFFECT?  |dSharpe| at H=0 vs at H=126.")
    t4_rows, t4_ok = [], True
    for dname in DEVICES:
        wins = 0
        parts = []
        for pan in ["U56", "B136", "SMALL"]:
            z = abs(P[(P.panel == pan) & (P.device == dname) & (P.H == 0)].iloc[0].dSharpe)
            a = abs(P[(P.panel == pan) & (P.device == dname) & (P.H == I_H)].iloc[0].dSharpe)
            wins += int(z > a)
            parts.append(f"{pan} {z:.4f} vs {a:.4f}")
        ok = wins >= 2
        t4_ok &= bool(ok)
        t4_rows.append(dict(device=dname, panels_shrunk=wins, pass_=ok))
        say(f"      {dname:<15} shrinks on {wins}/3 panels {'PASS' if ok else 'FAIL'}   "
            f"({'; '.join(parts)})")
    gate("T4 RETENTION SHRINKS THE MEASURED EFFECT (|dSharpe| H=0 > H=126 on >= 2 of 3 panels, "
         "every device)", t4_ok, "True", t4_ok)

    say("\n" + "=" * 124)
    say(f"(3) BOTH KEEP PATHS AT ALL {len(G)} CELLS (4a vs live RULES v2; 4b vs SPY, DD cap "
        f"{DD_CAP:.2f}x, CAGR floor {CAGR_FLOOR:.2f}x).")
    say("=" * 124)
    for pan in ["U56", "B136", "SMALL"]:
        s = G[G.panel == pan]
        say(f"    [{pan}] 4a {int(s.keep4a.sum())}/{len(s)} full, {int(s.keep4a_OOS.sum())}/{len(s)}"
            f" OOS  |  4b {int(s.keep4b.sum())}/{len(s)} full, {int(s.keep4b_OOS.sum())}/{len(s)} "
            f"OOS, {int((s.keep4b & s.keep4b_OOS).sum())}/{len(s)} BOTH")
        for leg in ["H1", "H2", "DD", "CAGR"]:
            say(f"           4b leg {leg:<4} passes {int(s['leg_'+leg].sum()):>3}/{len(s)} full, "
                f"{int(s['legO_'+leg].sum()):>3}/{len(s)} OOS")
    say(f"    TOTAL 4a {int(G.keep4a.sum())}/{len(G)} full, {int(G.keep4a_OOS.sum())}/{len(G)} OOS;"
        f" 4b {int(G.keep4b.sum())}/{len(G)} full, {int(G.keep4b_OOS.sum())}/{len(G)} OOS, "
        f"{int((G.keep4b & G.keep4b_OOS).sum())}/{len(G)} BOTH")
    both = G[G.keep4b & G.keep4b_OOS]
    if len(both):
        say("    4b BOTH cells:")
        for _, r in both.iterrows():
            say(f"      [{r.panel}] {r.config}|H{r.H}  FULL {r.CAGR:7.2%}/{r.Sharpe:.4f}/"
                f"{r.MaxDD:7.2%}  OOS {r.OOS_CAGR:7.2%}/{r.OOS_Sharpe:.4f}/{r.OOS_MaxDD:7.2%}  "
                f"dSharpe vs anchor {r.dSharpe_vs_anchor:+.4f} (t {r.dSharpe_t:+.2f}), OOS "
                f"{r.OOS_dSharpe_vs_anchor:+.4f}")

    say("\n    IS-REACHABILITY OF EVERY 4b-BOTH CELL (a cell no LEGAL IS-only chooser reaches is "
        "HINDSIGHT and is recorded as such, never as an enactable book):")
    for _, r in both.iterrows():
        col = G[(G.panel == r.panel) & (G.config == r.config)]
        row = G[(G.panel == r.panel) & (G.H == r.H)]
        pan_all = G[G.panel == r.panel]
        by_H = bool(col.loc[col.IS_Sharpe.idxmax(), "H"] == r.H)
        by_cfg = bool(row.loc[row.IS_Sharpe.idxmax(), "config"] == r.config)
        glob = bool(pan_all.loc[pan_all.IS_Sharpe.idxmax(), "config"] == r.config
                    and pan_all.loc[pan_all.IS_Sharpe.idxmax(), "H"] == r.H)
        is_anchor = (r.config, r.H) == ANCHOR
        tag = ("INCUMBENT (no choice needed)" if is_anchor
               else "REACHABLE" if (by_H or by_cfg or glob) else "HINDSIGHT")
        say(f"      [{r.panel}] {r.config}|H{r.H:<3} IS {r.IS_Sharpe:.4f}  argmax-IS within its "
            f"OWN H ladder {by_H}, within its OWN H column {by_cfg}, GLOBAL argmax {glob}  -> "
            f"{tag}   (full Sharpe {r.Sharpe:.4f} / OOS {r.OOS_Sharpe:.4f} vs anchor)")

    say("\n    FULL 75-CELL TABLE (every cell, no selection):")
    say(f"      {'panel':<7}{'config':<14}{'H':>5}{'CAGR':>9}{'Sharpe':>9}{'MaxDD':>9}"
        f"{'OOS CAGR':>10}{'OOS Sh':>9}{'OOS DD':>9}{'turn/yr':>9}{'OVR_W':>8}{'4a':>4}{'4b':>4}"
        f"{'4bO':>5}")
    for _, r in G.iterrows():
        say(f"      {r.panel:<7}{r.config:<14}{r.H:>5}{r.CAGR:>9.2%}{r.Sharpe:>9.4f}"
            f"{r.MaxDD:>9.2%}{r.OOS_CAGR:>10.2%}{r.OOS_Sharpe:>9.4f}{r.OOS_MaxDD:>9.2%}"
            f"{r.turn_yr:>9.2f}{r.OVR_W:>8.4f}{str(r.keep4a):>4}{str(r.keep4b):>4}"
            f"{str(r.keep4b_OOS):>5}")

    say("\n" + "=" * 124)
    say("(4) RULE 8 CAPITAL ARM.  Cell chosen by argmax IS Sharpe on warm-up..2016-12-31 ONLY; "
        "2017-2026 read once.")
    say("=" * 124)
    for _, r in W.iterrows():
        say(f"    [{r.panel}] {r.chooser:<32} -> {r.cell:<20} IS {r.IS_Sharpe:.4f} | OOS "
            f"{r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:7.2%}  "
            f"(anchor {r.anchor_OOS_CAGR:.2%}/{r.anchor_OOS_Sharpe:.4f}/{r.anchor_OOS_MaxDD:.2%}; "
            f"SPY {r.spy_OOS_CAGR:.2%}/{r.spy_OOS_Sharpe:.4f}/{r.spy_OOS_MaxDD:.2%}; "
            f"v2 {r.live_OOS_CAGR:.2%}/{r.live_OOS_Sharpe:.4f}/{r.live_OOS_MaxDD:.2%})  "
            f"4a {r.keep4a_OOS} 4b {r.keep4b_OOS}")
    mix = W[W.chooser.str.startswith("ARGMAX-IS (all")]
    non = W[W.chooser.str.startswith("DO NOTHING")]
    t5 = bool(mix.OOS_Sharpe.mean() > non.OOS_Sharpe.mean())
    say(f"\n    MEAN OOS SHARPE: chooser {mix.OOS_Sharpe.mean():.4f}  vs  do-nothing "
        f"{non.OOS_Sharpe.mean():.4f}  ({'CHOOSER WINS' if t5 else 'DOING NOTHING WINS'})")
    gate("T5 rule-8 chooser beats doing nothing on mean OOS Sharpe", t5, "True", t5)
    gate("G4 the rule-8 chooser reads no row on or after 2017-01-01",
         "IS window = warm-up..2016-12-31 by construction", "True", True)

    say("\n" + "=" * 124)
    say("VERDICT")
    say("=" * 124)
    gd = {g["gate"].split()[0]: g["pass_"] for g in GATES}
    upheld = bool(gd.get("T1") and gd.get("T2") and gd.get("T4"))
    say(f"    T1 {gd.get('T1')}  T2 {gd.get('T2')}  T3 {gd.get('T3')}  T4 {gd.get('T4')}  "
        f"T5 {gd.get('T5')}")
    say(f"    IDEA 1566 UPHELD (T1 & T2 & T4): {upheld}")
    say(f"    LIVE MAXVOL 0.60 INERT AT H = 126 (T3): {gd.get('T3')}")
    say(f"    CAPITAL: 4a {int(G.keep4a.sum())}/{len(G)} full and {int(G.keep4a_OOS.sum())}/{len(G)}"
        f" OOS; 4b {int(G.keep4b.sum())}/{len(G)} full, {int(G.keep4b_OOS.sum())}/{len(G)} OOS, "
        f"{int((G.keep4b & G.keep4b_OOS).sum())}/{len(G)} BOTH.")

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    allpass = all(g["pass_"] for g in GATES)
    say(f"\n    ALL GATES AND TESTS PASS: {allpass}   ({time.time()-t0:.0f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    G, P, W, t0 = main()
    analyse(G, P, W, t0)
