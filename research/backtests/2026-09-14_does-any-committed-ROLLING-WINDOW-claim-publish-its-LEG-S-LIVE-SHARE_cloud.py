#!/usr/bin/env python3
"""Idea 845 (cloud lane, 2026-09-14) — does any committed ROLLING-WINDOW claim in the
record PUBLISH its leg's LIVE SHARE?

QUESTION (QUEUE idea 845, verbatim)
    idea 843 found that at the record's 2016 split a w2016 QROLL arm is the ungated book on
    87.5% of its PRE leg (100% on SMALL663), and proved it bit-identically (max|d| 0.000e+00),
    yet no committed file prints the share of a leg on which the rolling threshold exists.
    Census every committed rolling-window claim for that column, re-read the ones below a
    liveness bar, and propose a PROTOCOL line requiring LIVE SHARE beside any window-length
    verdict.  Max 2 params (claim set, liveness bar).

WHY IT IS A CAPITAL QUESTION, NOT HYGIENE.  Two of the record's standing 4b KEEP-candidates
    are w=1008 breadth-QROLL books (B136 q0.12 depth0.50 gross1.00, memo 2026-09-12; U56 "K8"
    q0.17 depth1.00 gross1.00).  A w=1008 rolling threshold does not exist until 1008 trading
    days of breadth have accrued, and `gate_series` sets the multiplier to 1.0 while it is NaN,
    so on those days the arm IS the ungated equal-weight book — bit-identically (G3 re-proves
    it here).  Every full-sample headline for such a book therefore averages a gated book with
    an ungated one.  This run prices that: the two candidates are re-read on the leg that
    starts the day their own threshold exists, and both KEEP paths are re-evaluated there.

TUNED PARAMETERS: exactly TWO, the two the queue names.
    (1) CLAIM SET reading in {TIGHT, LOOSE}.  TIGHT = a single line carries BOTH a
        rolling/window token AND a verdict word.  LOOSE = the file carries both anywhere.
        Neither is a headline; both are reported at every bar.
    (2) LIVENESS BAR in {0.50, 0.80, 0.90, 0.95, 1.00}.  A claim file is BELOW the bar when the
        longest window it names has a FULL-leg live share under the bar on the headline panel.
        All 2 x 5 = 10 cells are reported.

REPORTED AXES (computed at every tuned point, none of them a tune)
    PANEL   U56 (live), B136 (broad), SMALL (sub-$2B, max_1d_move >= 1.0 dropped).
    LEG     FULL (the record's scored sample), PRE (<=2016-12-31), POST (>=2017-01-01),
            LIVE (starts on the arm's own first live day).
    WINDOW  w in {252, 504, 756, 1008, 2016}.
    COST    0 / 10 / 25 bps; headline 10 = PROTOCOL rule 2's.

PRE-REGISTERED HYPOTHESES (declared before any number is read)
    H_NONE      no committed rolling-window claim file publishes a LIVE SHARE column
                (idea 845's premise).  Any file that does falsifies it and is named.
    H_ATRISK    at the 0.90 bar, a MAJORITY of TIGHT claim files are below it.
    H_CANDLIVE  the two standing w1008 4b candidates keep their 4b PASS when the leg is
                restricted to live days (if they do not, the record's 4b shelf shrinks).
    H_GATEDEAD  on the dead region the gated arm is bit-identical to the ungated book
                (843's G6, re-proved: max|d| must be exactly 0.0).
    H_PICKMOVE  the rule-8 (q, w, depth) pick moves when the chooser is restricted to arms
                live over >= 50% of the IS window (a warm-up-blind chooser can pick a w that
                did not exist for most of the window it was chosen on).
    H_R8CLAIM   RULE 8 ON THE CLAIM: the reading chosen on the earlier half of the dated
                corpus reproduces its publish-share on the later half, |OOS - IS| <= 0.10.

GATES (printed before any new number; every one must pass)
    G1  fast_run reproduces products/backtester/engine.backtest on a real GATED book
        (returns and turnover) to < 1e-12.
    G2  the committed B136 QROLL 4b candidate reproduces its memo headline
        (14.30% / 1.1121 / -17.31%) and the U56 K8 candidate reproduces 14.16% / 1.2226 /
        -14.79%.
    G3  INERTNESS: on every day before its threshold exists, the QROLL arm's return is
        BIT-identical to the ungated book at the same gross.  max|d| must be exactly 0.0.
    G4  SPY full-sample reproduces the record's 4b comparand 15.16% / 0.8861 / -33.72%.

PROTOCOL: 10 bps per unit turnover (0/25 reported), weekly cadence, weights decided at close
    t applied at t+1, no shorting, no leverage.  Both KEEP paths evaluated on every book row.
    Rule 8 walk-forward is run on the books ((q, w, depth) chosen on 2009-2016 IS Sharpe only,
    2017-2026 read exactly once, three choosers) and on the claim census.

SURVIVORSHIP, up front: all three panels are CURRENT-constituent lists, so every CAGR and
    drawdown LEVEL here is optimistic, SMALL worst (a sub-$2B screen read today cannot see the
    names that fell out of it — data/SMALL_PANEL_README.md).  Tickers with max_1d_move >= 1.0
    in data/small_meta.csv are dropped before anything is computed.  Nothing printed here is a
    capital claim on its own.

Outputs (all committed under research/backtests/):
    .console.txt      full log
    .liveness.csv     per (panel, w, leg): first live day, live share, dead-day count
    .census.csv       per claim file: reading, windows named, live share, publishes-live-share
    .cells.csv        the 10 tuned cells (reading x liveness bar)
    .books.csv        every arm x panel x leg x cost rung, with 4a/4b verdicts
    .walkforward.csv  the rule-8 picks under three choosers and their OOS reads

Run: python research/backtests/2026-09-14_does-any-committed-ROLLING-WINDOW-claim-publish-its-LEG-S-LIVE-SHARE_cloud.py
Deterministic; no network (reads the committed price caches only).
"""
import re
import sys
import time
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, score, rules_v2_weights, rules_v1_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

DATE = "2026-09-14"
SLUG = "does-any-committed-ROLLING-WINDOW-claim-publish-its-LEG-S-LIVE-SHARE"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

# ---- the record's constants, copied so G2 is a real reproduction -----------------------
FREQ = "W"
LAG = 1
MAX_VOL = 0.60
WARMUP = 260
GROSS = 1.00
QS = [0.07, 0.12, 0.17]
WS = [252, 504, 756, 1008, 2016]
DEPTHS = [0.50, 1.00]
RUNGS = [0.0, 10.0, 25.0]
RUNG_HEAD = 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SMALL_MAXMOVE = 1.0
PANELS = ["U56", "B136", "SMALL"]
HEAD_PANEL = "U56"                      # the panel the census's live share is read on

# ---- tuned dial 1 and 2 ----------------------------------------------------------------
READINGS = ["TIGHT", "LOOSE"]
BARS = [0.50, 0.80, 0.90, 0.95, 1.00]

# ---- the two standing w1008 4b candidates (memo 2026-09-12) ----------------------------
CANDIDATES = {
    "B136_QROLL_q012_w1008_d050_g100": dict(panel="B136", q=0.12, w=1008, depth=0.50,
                                            memo=(0.1430, 1.1121, -0.1731)),
    "U56_K8_QROLL_q017_w1008_d100_g100": dict(panel="U56", q=0.17, w=1008, depth=1.00,
                                              memo=(0.1416, 1.2226, -0.1479)),
}

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ------------------------------------------------------------------ runner (825's/834's)
def fast_run(prices, weights, mask, lag=LAG):
    """Vectorised replica of engine.backtest. Returns (gross returns, turnover); the net
    return at cost c bps is r - turnover * c / 1e4, exactly as the engine computes it."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(lag).fillna(0.0).values
    mk = mask.shift(lag, fill_value=False).values.copy()
    mk[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
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
    return pd.Series((held * rets).sum(axis=1), index=idx), pd.Series(turn, index=idx)


def fmet(r):
    r = np.asarray(r, float)
    n = len(r)
    if n < 2:
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / n) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    if len(r) < 2:
        return np.nan
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def pack(r):
    c, s, d = fmet(r)
    h = len(r) // 2
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(r[:h]), H2=fsharpe(r[h:]))


def keep_paths(s, base, spy):
    """PROTOCOL rule 4. 4a vs the live book (RULES v2); 4b vs SPY on the same leg."""
    p4a = (s["H1"] > base["H1"]) and (s["H2"] > base["H2"]) and (s["MaxDD"] >= base["MaxDD"])
    p4b = (s["H1"] > spy["H1"]) and (s["H2"] > spy["H2"]) and \
          (s["MaxDD"] >= 0.60 * spy["MaxDD"]) and (s["CAGR"] >= 0.70 * spy["CAGR"])
    return bool(p4a), bool(p4b)


def fail4b(s, spy):
    f = []
    if not s["H1"] > spy["H1"]:
        f.append("H1")
    if not s["H2"] > spy["H2"]:
        f.append("H2")
    if not s["MaxDD"] >= 0.60 * spy["MaxDD"]:
        f.append("DDCAP")
    if not s["CAGR"] >= 0.70 * spy["CAGR"]:
        f.append("CAGRFLOOR")
    return "+".join(f) if f else "-"


# ------------------------------------------------------------------ primitives (825's/834's)
def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def ewall_weights(px, gross, elig):
    e = elig.astype(float)
    n = e.sum(axis=1).replace(0, np.nan)
    return e.div(n, axis=0).mul(gross).fillna(0.0)


def breadth(px):
    above = px > px.rolling(200).mean()
    return above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)


def gate_series(br, thr, depth, idx):
    """The record's gate: multiplier 1-depth while breadth is below the threshold, 1.0
    whenever the threshold does not exist (THIS is the warm-up blindness), held between
    weekly rebalances."""
    below = (br < thr)
    m = pd.Series(1.0, index=idx).where(~below, 1.0 - depth)
    ok = br.notna() & (thr.notna() if isinstance(thr, pd.Series) else True)
    m = m.where(ok, 1.0)
    return m.where(rebalance_mask(idx, FREQ)).ffill().fillna(1.0)


def load_panel(name):
    if name == "U56":
        px = load_universe()
    elif name == "B136":
        px = load_universe(broad=True)
    else:
        px = load_universe(small=True)
        meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
        bad = set(meta.loc[meta.max_1d_move >= SMALL_MAXMOVE, "ticker"])
        drop = [c for c in px.columns if c in bad and c != "SPY"]
        px = px.drop(columns=drop)
        P(f"   SMALL panel: dropped {len(drop)} tickers with max_1d_move >= {SMALL_MAXMOVE} "
          f"(data/small_meta.csv); {len([c for c in px.columns if c != 'SPY'])} names left")
    return px.dropna(how="all").ffill()


# =======================================================================================
# PANEL BUILD
# =======================================================================================
def build(name):
    px = load_panel(name)
    idx = px.index
    elig = eligible_mask(px)
    base_w = ewall_weights(px, GROSS, elig)
    mask = rebalance_mask(idx, FREQ)
    br = breadth(px)
    thr = {(q, w): br.rolling(w, min_periods=w).quantile(q) for q in QS for w in WS}
    start = idx[WARMUP]
    eidx = idx[idx >= start]
    r0, t0 = fast_run(px, base_w, mask)
    spy = px["SPY"].pct_change().fillna(0.0)
    return dict(name=name, px=px, idx=idx, elig=elig, base_w=base_w, mask=mask, br=br,
                thr=thr, start=start, eidx=eidx, r0=r0, t0=t0, spy=spy)


def arm_returns(B, q, w, depth):
    """Gross returns and turnover of one gated arm, on the panel's full index."""
    m = gate_series(B["br"], B["thr"][(q, w)], depth, B["idx"])
    W = B["base_w"].mul(m, axis=0)
    return fast_run(B["px"], W, B["mask"])


def live_index(B, w):
    """First position in the SCORED index on which the gate can act (the threshold, lagged
    by the engine's one-day application lag, exists)."""
    v = B["thr"][(QS[0], w)].reindex(B["eidx"]).shift(1).notna().values
    nz = np.flatnonzero(v)
    return int(nz[0]) if len(nz) else len(B["eidx"])


# =======================================================================================
# MAIN
# =======================================================================================
def main():
    t_start = time.time()
    P(f"# Idea 845 — LIVE SHARE beside every rolling-window claim ({DATE}, cloud lane)")
    P(f"# {len(READINGS)} readings x {len(BARS)} liveness bars = {len(READINGS) * len(BARS)} "
      f"tuned cells; books at {len(QS)}x{len(WS)}x{len(DEPTHS)} = "
      f"{len(QS) * len(WS) * len(DEPTHS)} arms x {len(PANELS)} panels x {len(RUNGS)} rungs, "
      f"ALL reported.")
    P("# SURVIVORSHIP: all three panels are current-constituent lists; every level is optimistic.")

    Bs = {}
    for name in PANELS:
        P(f"\n## panel {name}")
        Bs[name] = build(name)
        B = Bs[name]
        P(f"   {B['px'].shape[1]} columns, {len(B['idx'])} rows "
          f"{B['idx'][0].date()}..{B['idx'][-1].date()}; scored from {B['start'].date()} "
          f"({len(B['eidx'])} days)")

    # ----------------------------------------------------------------- GATES
    P("\n### GATES (printed before any new number)")
    gate_ok = True

    # G1 — fast_run vs engine.backtest on a real GATED book.
    B = Bs["B136"]
    m = gate_series(B["br"], B["thr"][(0.12, 1008)], 0.50, B["idx"])
    Wg = B["base_w"].mul(m, axis=0)
    eng = backtest(B["px"], Wg, cost_bps=0.0, freq=FREQ)
    fr, ft = fast_run(B["px"], Wg, B["mask"])
    fin = eng["returns"].notna().values
    n_nan = int((~fin).sum())
    g1r = float(np.abs(eng["returns"].values[fin] - fr.values[fin]).max())
    g1t = float(np.abs(eng["turnover"].values[fin] - ft.values[fin]).max())
    P(f"   G1 fast_run vs engine.backtest on the gated B136 book over {int(fin.sum())} finite "
      f"rows ({n_nan} engine NaN warm-up rows excluded, all before the {WARMUP}-day skip): "
      f"max|dr| {g1r:.3e}  max|dturn| {g1t:.3e}  {'PASS' if max(g1r, g1t) < 1e-12 else 'FAIL'}")
    assert n_nan == 0 or eng["returns"].index[~fin].max() < B["idx"][WARMUP]
    gate_ok &= max(g1r, g1t) < 1e-12

    # G2 — the two committed candidates reproduce their memo headlines.
    for cname, c in CANDIDATES.items():
        Bc = Bs[c["panel"]]
        r, t = arm_returns(Bc, c["q"], c["w"], c["depth"])
        net = (r - t * RUNG_HEAD / 1e4).loc[Bc["start"]:].values
        got = fmet(net)
        d = max(abs(got[0] - c["memo"][0]), abs(got[1] - c["memo"][1]), abs(got[2] - c["memo"][2]))
        # EXACT = inside the memo's own rounding; NEAR = reproduces the book but not the digit
        # (stated, never hidden — the residual is reported and is smaller than every verdict
        # margin read below).
        tag = "PASS (EXACT)" if d < 5e-5 else ("PASS (NEAR, residual stated)" if d < 1e-3 else "FAIL")
        P(f"   G2 {cname}: {got[0]:.4%} / {got[1]:.4f} / {got[2]:.4%}  vs committed memo "
          f"{c['memo'][0]:.2%} / {c['memo'][1]:.4f} / {c['memo'][2]:.2%}  max|d| {d:.2e} {tag}")
        gate_ok &= d < 1e-3

    # G3 — INERTNESS on the dead region (843's G6, re-proved here).
    g3max = 0.0
    g3cells = 0
    for pname in PANELS:
        Bp = Bs[pname]
        base_net = (Bp["r0"] - Bp["t0"] * RUNG_HEAD / 1e4).loc[Bp["start"]:].values
        for w in WS:
            li = live_index(Bp, w)
            if li <= 0:
                continue
            for q, dep in ((0.12, 0.50), (0.17, 1.00)):
                r, t = arm_returns(Bp, q, w, dep)
                net = (r - t * RUNG_HEAD / 1e4).loc[Bp["start"]:].values
                g3max = max(g3max, float(np.abs(net[:li] - base_net[:li]).max()))
                g3cells += 1
    P(f"   G3 INERTNESS: over {g3cells} (panel, w, arm) dead regions the gated arm is identical "
      f"to the ungated book: max|d| {g3max:.3e} {'PASS' if g3max == 0.0 else 'FAIL'}")
    gate_ok &= g3max == 0.0

    # G4 — SPY, the 4b comparand.
    Bu = Bs["U56"]
    spy_full = Bu["spy"].loc[Bu["start"]:].values
    sc, ss, sd = fmet(spy_full)
    g4 = max(abs(sc - 0.1516), abs(ss - 0.8861), abs(sd + 0.3372))
    P(f"   G4 SPY full {sc:.4%} / {ss:.4f} / {sd:.4%} vs committed 15.16% / 0.8861 / -33.72%: "
      f"max|d| {g4:.2e} {'PASS' if g4 < 1e-3 else 'FAIL'}")
    gate_ok &= g4 < 1e-3
    P(f"   GATES: {'ALL PASS' if gate_ok else 'FAILURE — nothing below is read'}")
    assert gate_ok

    # ----------------------------------------------------------------- PART A: LIVE SHARE
    P("\n### PART A — the LIVE SHARE table (the column the record never prints)")
    rows = []
    for pname in PANELS:
        Bp = Bs[pname]
        eidx = Bp["eidx"]
        legs = {"FULL": np.ones(len(eidx), bool),
                "PRE": np.asarray(eidx <= pd.Timestamp(IS_END)),
                "POST": np.asarray(eidx >= pd.Timestamp(OOS_START))}
        for w in WS:
            liveflag = Bp["thr"][(QS[0], w)].reindex(eidx).shift(1).notna().values
            li = live_index(Bp, w)
            first = eidx[li].date() if li < len(eidx) else None
            for lname, sel in legs.items():
                n = int(sel.sum())
                live = int((liveflag & sel).sum())
                rows.append(dict(panel=pname, w=w, leg=lname, days=n, live_days=live,
                                 dead_days=n - live,
                                 live_share=(live / n if n else np.nan),
                                 first_live=first))
    LIVE = pd.DataFrame(rows)
    LIVE.to_csv(f"{OUT}.liveness.csv", index=False)
    piv = LIVE.pivot_table(index=["panel", "w"], columns="leg", values="live_share")
    P(piv.reindex(columns=["FULL", "PRE", "POST"]).to_string(float_format=lambda x: f"{x:.4f}"))
    for pname in PANELS:
        s = LIVE[(LIVE.panel == pname) & (LIVE.leg == "FULL")]
        P("   " + pname + " first live day: " + ", ".join(
            f"w{int(r.w)} {r.first_live}" for r in s.itertuples()))
    head_share = {int(r.w): float(r.live_share) for r in
                  LIVE[(LIVE.panel == HEAD_PANEL) & (LIVE.leg == "FULL")].itertuples()}
    P(f"   HEADLINE (panel {HEAD_PANEL}, FULL leg) live shares: " +
      ", ".join(f"w{w} {head_share[w]:.4f}" for w in WS))

    # ----------------------------------------------------------------- PART B: the CENSUS
    P("\n### PART B — the CENSUS: every committed rolling-window claim, does it publish LIVE SHARE?")
    files = sorted([p for p in (ROOT / "research").rglob("*.py")] +
                   [p for p in (ROOT / "research").rglob("*.md")])
    me = Path(__file__).resolve()
    files = [p for p in files if p.resolve() != me and p.name != "QUEUE.md"]
    P(f"   corpus: {len(files)} committed .py/.md files under research/ "
      f"(QUEUE.md and this script excluded)")

    RE_ROLL = re.compile(r"QROLL|rolling\s*\(|\brolling\b|ROLLING", re.I)
    RE_W = re.compile(r"(?:\bw[\s_=]*|\bwindow[\s_=]*|rolling\s*\(\s*|\blookback[\s_=]*)"
                      r"(252|504|756|1008|2016)\b"
                      r"|\b(252|504|756|1008|2016)[- ]?trading[- ]?day", re.I)

    def wins(text):
        """Every window length the text NAMES as a window (not as a bare integer)."""
        return sorted({int(m.group(1) or m.group(2)) for m in RE_W.finditer(text)})

    RE_VERD = re.compile(r"KEEP|KILL|PARK|\bPASS\b|\bFAIL\b|beats?\b|wins?\b|monoton|better|"
                         r"worse|verdict|ordering|\b4a\b|\b4b\b", re.I)
    RE_LIVE = re.compile(r"live[\s_-]?share|liveness|live[\s_-]?index|dead[\s_-]?day|"
                         r"warm-?up share|live[\s_-]?leg|share of (?:the )?leg", re.I)
    RE_WARM = re.compile(r"warm-?up|min_periods", re.I)
    RE_DATE = re.compile(r"(20\d\d)-(\d\d)-(\d\d)")

    crows = []
    skipped = 0
    for p in files:
        try:
            if p.stat().st_size > 8_000_000:
                skipped += 1
                continue
            txt = p.read_text(errors="replace")
        except Exception:
            skipped += 1
            continue
        ws = wins(txt)
        if not ws or not RE_ROLL.search(txt):
            continue
        loose = bool(RE_VERD.search(txt))
        tight = any(RE_W.search(ln) and RE_VERD.search(ln) and RE_ROLL.search(ln)
                    for ln in txt.split("\n"))
        if not loose:
            continue
        mdate = RE_DATE.match(p.name)
        crows.append(dict(
            file=str(p.relative_to(ROOT)), TIGHT=tight, LOOSE=loose,
            windows=";".join(str(x) for x in ws), max_w=max(ws),
            live_share_max_w=head_share.get(max(ws), np.nan),
            publishes_live_share=bool(RE_LIVE.search(txt)),
            live_sites=len(RE_LIVE.findall(txt)),
            mentions_warmup=bool(RE_WARM.search(txt)),
            date=(f"{mdate.group(0)}" if mdate else "")))
    CEN = pd.DataFrame(crows)
    CEN.to_csv(f"{OUT}.census.csv", index=False)
    P(f"   {skipped} files skipped (unreadable or > 8 MB); {len(CEN)} rolling-window claim files "
      f"found under LOOSE, {int(CEN.TIGHT.sum())} under TIGHT")

    cells = []
    for reading, bar in product(READINGS, BARS):
        sub = CEN[CEN[reading]]
        n = len(sub)
        pub = int(sub.publishes_live_share.sum())
        below = sub[sub.live_share_max_w < bar]
        below_pub = int(below.publishes_live_share.sum())
        cells.append(dict(reading=reading, bar=bar, n_claim_files=n,
                          n_publish=pub, publish_share=(pub / n if n else np.nan),
                          n_below_bar=len(below),
                          below_share=(len(below) / n if n else np.nan),
                          n_below_and_publish=below_pub,
                          n_mention_warmup=int(sub.mentions_warmup.sum())))
    CELLS = pd.DataFrame(cells)
    CELLS.to_csv(f"{OUT}.cells.csv", index=False)
    P(CELLS.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    pubs = CEN[CEN.publishes_live_share]
    P(f"   H_NONE: {len(pubs)} of {len(CEN)} LOOSE claim files publish a LIVE-SHARE token "
      f"({'FALSIFIED' if len(pubs) else 'HOLDS'}).")
    if len(pubs):
        for r in pubs.sort_values("live_sites", ascending=False).head(12).itertuples():
            P(f"      {r.live_sites:>4} sites  w[{r.windows}]  {r.file}")
        P(f"      ... {len(pubs)} files total; the rest are in .census.csv")
    # The premise is about the RECORD, not about the run that discovered the problem: idea 843's
    # own script, its result memo, and the two ledgers that quote it are one lineage.
    LINEAGE = "is-the-QROLL-LOOKBACK-MONOTONICITY-a-WINDOW-fact-or-a-WARM-UP-fact"
    out = CEN[~(CEN.file.str.contains(LINEAGE) |
                CEN.file.str.endswith("LEADERBOARD.md") |
                CEN.file.str.endswith("CHANGELOG.md"))]
    P(f"   OUTSIDE idea 843's own lineage (its script + result memo) and the two ledgers that "
      f"quote it: {int(out.publishes_live_share.sum())} of {len(out)} claim files publish a "
      f"LIVE-SHARE column.")
    P("   the TIGHT claim files, in full:")
    for r in CEN[CEN.TIGHT].sort_values("file").itertuples():
        P(f"      publishes={str(r.publishes_live_share):<5} w[{r.windows}] "
          f"live_share(max w)={r.live_share_max_w:.4f}  {r.file}")
    tight_pub = CEN[CEN.TIGHT & CEN.publishes_live_share]
    P(f"   TIGHT reading: {len(tight_pub)} of {int(CEN.TIGHT.sum())} publish "
      f"({len(tight_pub) / max(int(CEN.TIGHT.sum()), 1):.4f})")
    b90 = CELLS[(CELLS.reading == "TIGHT") & (CELLS.bar == 0.90)].iloc[0]
    P(f"   H_ATRISK (TIGHT, bar 0.90): {b90.n_below_bar} of {b90.n_claim_files} below "
      f"({b90.below_share:.4f}) — {'PASS' if b90.below_share > 0.50 else 'FAIL'}")

    # ----------------------------------------------------------------- PART B2: rule 8 on the claim
    P("\n### PART B2 — RULE 8 ON THE CLAIM (reading chosen on the earlier corpus half, later read once)")
    dated = CEN[CEN.date != ""].copy()
    if len(dated) >= 8:
        dated = dated.sort_values("date").reset_index(drop=True)
        med = dated.date.iloc[len(dated) // 2]           # string dates sort lexicographically
        IS = dated[dated.date <= med]
        OOS = dated[dated.date > med]
        if len(OOS) == 0:                       # median lands on the corpus's last date
            k = len(dated) // 2
            IS, OOS = dated.iloc[:k], dated.iloc[k:]
            P(f"   date median {med} cannot split the corpus; falling back to the index midpoint")
        pick = max(READINGS, key=lambda r: (IS[IS[r]].publishes_live_share.mean()
                                            if len(IS[IS[r]]) else -1))
        is_share = float(IS[IS[pick]].publishes_live_share.mean()) if len(IS[IS[pick]]) else np.nan
        oos_share = float(OOS[OOS[pick]].publishes_live_share.mean()) if len(OOS[OOS[pick]]) else np.nan
        gap = abs(oos_share - is_share)
        P(f"   split at {med}: IS {len(IS)} files, OOS {len(OOS)} files; pick = {pick} "
          f"(IS publish-share {is_share:.4f})")
        P(f"   H_R8CLAIM: OOS publish-share {oos_share:.4f}, |OOS - IS| {gap:.4f} against a 0.10 "
          f"bar — {'PASS' if gap <= 0.10 else 'FAIL'}")
    else:
        P(f"   only {len(dated)} dated claim files — rule 8 on the claim is INFEASIBLE, stated as such")

    # ----------------------------------------------------------------- PART C: the BOOK leg
    P("\n### PART C — the BOOK leg: every arm on RAW and LIVE legs, both KEEP paths, 3 rungs")
    brows = []
    for pname in PANELS:
        Bp = Bs[pname]
        eidx = Bp["eidx"]
        spy_e = Bp["spy"].loc[Bp["start"]:].values
        v2r, v2t = fast_run(Bp["px"], rules_v2_weights(Bp["px"]), Bp["mask"])
        v1r, v1t = fast_run(Bp["px"], rules_v1_weights(Bp["px"]), Bp["mask"])
        base_r, base_t = Bp["r0"], Bp["t0"]
        oos0 = int(np.searchsorted(eidx.values, np.datetime64(OOS_START)))
        for q, w, dep in product(QS, WS, DEPTHS):
            r, t = arm_returns(Bp, q, w, dep)
            rr = r.loc[Bp["start"]:].values
            tt = t.loc[Bp["start"]:].values
            li = live_index(Bp, w)
            for rung in RUNGS:
                net = rr - tt * rung / 1e4
                v2 = (v2r - v2t * rung / 1e4).loc[Bp["start"]:].values
                ung = (base_r - base_t * rung / 1e4).loc[Bp["start"]:].values
                for leg, a, b in (("RAW", 0, len(eidx)), ("LIVE", li, len(eidx)),
                                  ("OOS", oos0, len(eidx))):
                    if b - a < 252:
                        continue
                    s = pack(net[a:b])
                    bs = pack(v2[a:b])
                    sp = pack(spy_e[a:b])
                    u = pack(ung[a:b])
                    p4a, p4b = keep_paths(s, bs, sp)
                    brows.append(dict(
                        panel=pname, q=q, w=w, depth=dep, gross=GROSS, rung=rung, leg=leg,
                        start=str(eidx[a].date()), days=b - a,
                        live_share=float(LIVE[(LIVE.panel == pname) & (LIVE.w == w) &
                                              (LIVE.leg == "FULL")].live_share.iloc[0])
                        if leg == "RAW" else 1.0,
                        CAGR=s["CAGR"], Sharpe=s["Sharpe"], MaxDD=s["MaxDD"],
                        H1=s["H1"], H2=s["H2"],
                        UNGATED_CAGR=u["CAGR"], UNGATED_Sharpe=u["Sharpe"], UNGATED_MaxDD=u["MaxDD"],
                        V2_Sharpe=bs["Sharpe"], V2_CAGR=bs["CAGR"], V2_MaxDD=bs["MaxDD"],
                        SPY_CAGR=sp["CAGR"], SPY_Sharpe=sp["Sharpe"], SPY_MaxDD=sp["MaxDD"],
                        SPY_H1=sp["H1"], SPY_H2=sp["H2"],
                        pass4a=p4a, pass4b=p4b, fail4b=fail4b(s, sp)))
    BK = pd.DataFrame(brows)
    BK.to_csv(f"{OUT}.books.csv", index=False)
    hd = BK[BK.rung == RUNG_HEAD]
    P(f"   {len(BK)} book rows ({len(hd)} at the 10-bps rung), ALL in .books.csv")
    for leg in ("RAW", "LIVE", "OOS"):
        s = hd[hd.leg == leg]
        P(f"   leg {leg:>4}: 4b {int(s.pass4b.sum())}/{len(s)}   4a {int(s.pass4a.sum())}/{len(s)}")
    P("   4b pass counts by (panel, leg) at 10 bps:")
    P(hd.pivot_table(index="panel", columns="leg", values="pass4b", aggfunc="sum")
      .reindex(columns=["RAW", "LIVE", "OOS"]).to_string())

    # The two standing candidates, leg by leg.
    P("\n   THE TWO STANDING w1008 4b CANDIDATES, re-read on their own LIVE leg (10 bps):")
    for cname, c in CANDIDATES.items():
        for leg in ("RAW", "LIVE", "OOS"):
            r = hd[(hd.panel == c["panel"]) & (hd.q == c["q"]) & (hd.w == c["w"]) &
                   (hd.depth == c["depth"]) & (hd.leg == leg)]
            if not len(r):
                continue
            r = r.iloc[0]
            P(f"      {cname:<34} {leg:>4} from {r.start} ({r.days} d, live share "
              f"{r.live_share:.4f}): CAGR {r.CAGR:.2%} Sharpe {r.Sharpe:.4f} MaxDD {r.MaxDD:.2%} "
              f"halves {r.H1:.3f}/{r.H2:.3f} | ungated {r.UNGATED_CAGR:.2%}/{r.UNGATED_Sharpe:.4f}/"
              f"{r.UNGATED_MaxDD:.2%} | SPY {r.SPY_CAGR:.2%}/{r.SPY_Sharpe:.4f}/{r.SPY_MaxDD:.2%} "
              f"| 4b {'PASS' if r.pass4b else 'FAIL ' + r.fail4b}  4a {'PASS' if r.pass4a else 'FAIL'}")
    # How big is the dilution, over the whole grid rather than the two headline arms?
    key = ["panel", "q", "w", "depth"]
    raw = hd[hd.leg == "RAW"].set_index(key)
    liv = hd[hd.leg == "LIVE"].set_index(key)
    j = raw[["Sharpe", "CAGR", "MaxDD", "live_share"]].join(
        liv[["Sharpe", "CAGR", "MaxDD"]], lsuffix="_RAW", rsuffix="_LIVE").dropna()
    d_sh = j.Sharpe_LIVE - j.Sharpe_RAW
    P(f"\n   DILUTION over all {len(j)} (panel, q, w, depth) arms at 10 bps: LIVE - RAW Sharpe "
      f"mean {d_sh.mean():+.4f}, median {d_sh.median():+.4f}, "
      f"{int((d_sh > 0).sum())}/{len(j)} positive; "
      f"rho(live share, dSharpe) {j.live_share.rank().corr(d_sh.rank()):+.4f} (Spearman)")
    for w in WS:
        s = j[j.index.get_level_values("w") == w]
        P(f"      w{w:<5} live share {s.live_share.iloc[0]:.4f}..{s.live_share.iloc[-1]:.4f}  "
          f"dSharpe mean {(s.Sharpe_LIVE - s.Sharpe_RAW).mean():+.4f}  "
          f"dCAGR mean {(s.CAGR_LIVE - s.CAGR_RAW).mean():+.2%}  "
          f"dMaxDD mean {(s.MaxDD_LIVE - s.MaxDD_RAW).mean():+.2%}")

    cand_live = all(
        bool(hd[(hd.panel == c["panel"]) & (hd.q == c["q"]) & (hd.w == c["w"]) &
                (hd.depth == c["depth"]) & (hd.leg == "LIVE")].pass4b.iloc[0])
        for c in CANDIDATES.values())
    P(f"   H_CANDLIVE: {'PASS — both keep 4b on the live leg' if cand_live else 'FAIL — at least one 4b pass does not survive its own live leg'}")

    # ----------------------------------------------------------------- PART D: rule 8 on the books
    P("\n### PART D — RULE 8 ON THE BOOKS: (q, w, depth) chosen on 2009-2016 IS Sharpe only, "
      "OOS 2017-2026 read ONCE, three choosers")
    wrows = []
    for pname in PANELS:
        Bp = Bs[pname]
        eidx = Bp["eidx"]
        oos0 = int(np.searchsorted(eidx.values, np.datetime64(OOS_START)))
        is_end = oos0
        spy_e = Bp["spy"].loc[Bp["start"]:].values
        v2r, v2t = fast_run(Bp["px"], rules_v2_weights(Bp["px"]), Bp["mask"])
        v1r, v1t = fast_run(Bp["px"], rules_v1_weights(Bp["px"]), Bp["mask"])
        cand = []
        for q, w, dep in product(QS, WS, DEPTHS):
            r, t = arm_returns(Bp, q, w, dep)
            net = (r - t * RUNG_HEAD / 1e4).loc[Bp["start"]:].values
            li = live_index(Bp, w)
            is_share = float(((np.arange(is_end) >= li)).mean()) if is_end else np.nan
            cand.append(dict(q=q, w=w, depth=dep, net=net, li=li, is_share=is_share,
                             is_sharpe=fsharpe(net[:is_end]),
                             is_sharpe_liveleg=(fsharpe(net[li:is_end]) if is_end - li >= 252
                                                else np.nan)))
        for chooser in ("BLIND", "LIVE50", "LIVELEG"):
            pool = [c for c in cand if (chooser != "LIVE50" or c["is_share"] >= 0.50)]
            keyf = (lambda c: c["is_sharpe_liveleg"]) if chooser == "LIVELEG" else (lambda c: c["is_sharpe"])
            pool = [c for c in pool if np.isfinite(keyf(c))]
            if not pool:
                P(f"   {pname} {chooser}: no feasible candidate — stated, no pick")
                continue
            best = max(pool, key=keyf)
            net = best["net"]
            s = pack(net[oos0:])
            bs = pack((v2r - v2t * RUNG_HEAD / 1e4).loc[Bp["start"]:].values[oos0:])
            v1 = pack((v1r - v1t * RUNG_HEAD / 1e4).loc[Bp["start"]:].values[oos0:])
            sp = pack(spy_e[oos0:])
            p4a, p4b = keep_paths(s, bs, sp)
            P(f"   {pname} {chooser:<7} pick q={best['q']} w={best['w']} depth={best['depth']} "
              f"(IS Sharpe {best['is_sharpe']:.4f}, IS live share {best['is_share']:.4f})  "
              f"OOS {s['CAGR']:.2%} / {s['Sharpe']:.4f} / {s['MaxDD']:.2%} halves "
              f"{s['H1']:.3f}/{s['H2']:.3f}  | RULES v2 {bs['CAGR']:.2%}/{bs['Sharpe']:.4f}/"
              f"{bs['MaxDD']:.2%} | v1 {v1['CAGR']:.2%}/{v1['Sharpe']:.4f} | SPY {sp['CAGR']:.2%}/"
              f"{sp['Sharpe']:.4f}/{sp['MaxDD']:.2%} | 4b {'PASS' if p4b else 'FAIL ' + fail4b(s, sp)}"
              f"  4a {'PASS' if p4a else 'FAIL'}")
            wrows.append(dict(panel=pname, chooser=chooser, q=best["q"], w=best["w"],
                              depth=best["depth"], IS_Sharpe=best["is_sharpe"],
                              IS_live_share=best["is_share"],
                              OOS_CAGR=s["CAGR"], OOS_Sharpe=s["Sharpe"], OOS_MaxDD=s["MaxDD"],
                              OOS_H1=s["H1"], OOS_H2=s["H2"],
                              V2_OOS_CAGR=bs["CAGR"], V2_OOS_Sharpe=bs["Sharpe"],
                              V2_OOS_MaxDD=bs["MaxDD"],
                              SPY_OOS_CAGR=sp["CAGR"], SPY_OOS_Sharpe=sp["Sharpe"],
                              SPY_OOS_MaxDD=sp["MaxDD"],
                              pass4a=p4a, pass4b=p4b, fail4b=fail4b(s, sp)))
    WF = pd.DataFrame(wrows)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    moved = []
    for pname in PANELS:
        s = WF[WF.panel == pname].set_index("chooser")
        if "BLIND" in s.index and "LIVE50" in s.index:
            a = tuple(s.loc["BLIND", ["q", "w", "depth"]])
            b = tuple(s.loc["LIVE50", ["q", "w", "depth"]])
            moved.append((pname, a, b, a != b))
    P("   H_PICKMOVE: " + "; ".join(
        f"{p} BLIND {a} vs LIVE50 {b} -> {'MOVES' if mv else 'same'}" for p, a, b, mv in moved))
    P(f"   H_PICKMOVE verdict: {'PASS' if any(m[3] for m in moved) else 'FAIL'} "
      f"({sum(m[3] for m in moved)} of {len(moved)} panels move)")

    # ----------------------------------------------------------------- PART E: the proposed line
    P("\n### PART E — the PROTOCOL line this run proposes (PROPOSAL ONLY; PROTOCOL.md is NOT edited "
      "— rule 6 puts every protocol change through Sunday review)")
    P("   Proposed PROTOCOL rule 10 (exact wording):")
    P('   10. **Live share (rolling windows):** any verdict that turns on a rolling-window LENGTH')
    P('       must print, beside it, the LIVE SHARE of each leg it is read on — the fraction of')
    P('       scored days on which that window\'s statistic actually exists. A rolling statistic')
    P('       with `min_periods = w` is NaN for its first w-1 days and every gate built on it is')
    P('       inert there, so the arm IS its own ungated control on those days. A leg with live')
    P('       share below 0.90 may not carry a window-length verdict on its own; report the')
    P('       LIVE-leg reading beside the RAW one.')

    # ----------------------------------------------------------------- close
    P(f"\n### done in {time.time() - t_start:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
