#!/usr/bin/env python3
"""
Idea 1358 (lane cloud, 2026-09-19) — does routing the incumbent's UNINVESTED GROSS into a BOND
SLEEVE buy the BINDING 4b DD LEG?

THE PREMISE.  Every de-grossing arm the record has priced — idea 1296's drawdown brake, idea
1346's flat gross ladder, ideas 794/1297's vol-target overlay — parks the uninvested gross in
CASH AT 0%.  That is both unrealistic (no implementer holds 40% of NAV in a mattress for 17
years) and the mechanical reason de-grossing always trades CAGR for drawdown one-for-one: the
residual earns nothing, so lowering gross scales the whole book toward a zero-return asset.
Idea 383 already found a SHY residual STRICTLY DOMINATES cash cell-for-cell — but on the RULES v2
BAND book at gross 0.375 on B136, NOT on the frozen 2026-09-04 KEEP-4b incumbent, whose SOLE
binding leg is the 4b MaxDD cap with 1.10 pp of room (idea 1298).  This run asks the incumbent's
own question: is the DD leg buyable by paying the residual a coupon instead of nothing?

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  SLEEVE {CASH, SHY, IEF, TLT}   DIAL 1 — CASH is the incumbent's residual (0%/yr)
  GROSS  {0.50, 0.60, 0.75}      DIAL 2 — 0.60 is the frozen incumbent's value

  12 cells per panel, 36 in all, EVERY ONE published in `.grid.csv`.

THE BOOK, OTHERWISE FROZEN.  The record's certified 2026-09-04 incumbent as the cloud lane has
carried it since idea 1296: 3-leg rank composite ((21,252), (0,126), (0,63)) x the
`0.5 + 0.5*above-200d` tilt, eligibility = above the 200d MA AND vol20 < 0.60, N = 15 names at
equal weight, minimum hold H = 126 trading days, decisions lagged one row and applied at t+1
(rule 2), 10 bps per unit turnover.  The sleeve leg PAYS THE SAME 10 bps on its own turnover —
the bond ETF is traded, not conjured.  No leverage, no shorting: weights sum to exactly 1.0 and
the sleeve is long-only.

WHAT IS BEING ASKED, PRECISELY.  Not "does a bond sleeve raise CAGR" — of course a positive-carry
residual raises CAGR over a 17-year sample that contains the largest bond bull market on record.
The question is whether it does so WITHOUT giving the drawdown back, so every cell publishes the
DD MARGIN (MaxDD - 0.60 x SPY's) and the CAGR MARGIN (CAGR - 0.70 x SPY's) side by side, plus its
own realised vol.  And because a sleeve that merely re-levers the book is not a finding, every
sleeve cell is ALSO scored against a VOL-MATCHED CASH TWIN: the cash-residual book on a fine
gross ladder (0.35..1.00 by 0.05, CONTROLS, not dials) whose realised vol is nearest that cell's.
If the sleeve's edge disappears at matched vol, the sleeve is an exposure dial wearing a costume.

THE HONEST CAVEAT, STATED BEFORE THE NUMBERS.  2009-2026 is the wrong sample to learn the value
of duration from: it holds a 13-year bond bull market followed by 2022, the worst Treasury year
in modern history.  The halves are therefore reported for the SLEEVE ITSELF as well as for the
book, and the rule-8 OOS window (2017-2026) is the one that contains 2022.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); both KEEP paths at every
cell; the halves; IS and OOS windows; turnover and its 10 bps drag in bp/yr; realised vol.

COMPARANDS (rule 3): the live RULES v2 baseline at 10 bps weekly, SPY buy-and-hold, and the
FROZEN (CASH, gross 0.60) incumbent.

PROTOCOL: rule 1 (>= 10 years); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3 (RULES v2
AND SPY); rule 4 (both KEEP paths, 2 tuned parameters); rule 8 (walk-forward: the (SLEEVE, GROSS)
PAIR chosen on warm-up..2016-12-31 by argmax IS Sharpe, 2017-2026 read ONCE, scored against the
frozen (CASH, 0.60) incumbent); rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py,
bot.py and baseline.py are NOT modified.

RESOLVABILITY, not just sign.  Every sleeve-minus-vol-matched-twin Sharpe gap is scored by a
PAIRED circular-block bootstrap (400 reps x 63-row blocks, seed 20260919, both books resampled on
IDENTICAL blocks so the pairing survives), full sample and OOS.  |t| > 2 is the record's bar.  A
gap inside its own SE is reported as UNRESOLVED, not as a finding.

GATES.  G1 is a CROSS-SCRIPT replay: the (CASH, 0.60) cell must reproduce, on ALL THREE panels to
< 5e-6, the anchor row committed by this lane's idea-1296 and idea-1346 scripts — same tape, a
different machinery path (the sleeve-augmented runner must collapse EXACTLY onto the cash runner
when the sleeve is CASH).  G2a asserts the joined sleeve series is EXACTLY U56's own column;
G2b bounds (never zeroes) the B136 difference, which is idea 353's standing open finding about
`data/prices_broad.csv` being a raw yf.download at a different decimal precision.  G3 asserts no
leverage: the weight sum never exceeds 1.0.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-19_does-routing-the-incumbent-s-UNINVESTED-GROSS-into-a-BOND-SLEEVE-buy-the-BINDING-4b-DD-LEG_cloud.py
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
SLUG = "does-routing-the-incumbent-s-UNINVESTED-GROSS-into-a-BOND-SLEEVE-buy-the-BINDING-4b-DD-LEG"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H = 15, 126                                 # frozen: width, minimum hold
COST = 10.0                                        # PROTOCOL rule 2
CADENCE = "W"                                      # frozen
SLEEVES = ["CASH", "SHY", "IEF", "TLT"]            # DIAL 1
GROSSES = [0.50, 0.60, 0.75]                       # DIAL 2
ANCHOR_SLV, ANCHOR_G = "CASH", 0.60                # the frozen incumbent
CTRL_GROSSES = [round(0.35 + 0.05 * i, 2) for i in range(14)]   # 0.35..1.00 CASH controls
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
# Committed by this lane's idea-1296 (.grid.csv BASIS=NONE depth 1.00) and re-read bit-identically
# by idea 1346's (gross 0.60, W) cell.  Cross-script gate G1.
C_ANCHOR = {
    "U56": dict(CAGR=0.1367020011892825, Sharpe=1.17166235540161, MaxDD=-0.163814812515476,
                H1=1.2526855979053693, H2=1.121880836109541, turn=2.463043347965852),
    "B136": dict(CAGR=0.1343474037905223, Sharpe=1.0630027470342966, MaxDD=-0.1597051532314095,
                 H1=1.2318389322712402, H2=0.9406397253110836, turn=2.6461090252500337),
    "SMALL": dict(CAGR=0.0753535266944089, Sharpe=0.5569518940285322, MaxDD=-0.3263346826561878,
                  H1=0.8125393414921002, H2=0.358407645038224, turn=3.407055866031751),
}

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=value, target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


def publish(name, value):
    GATES.append(dict(gate=name, value=value, target="published, not asserted", pass_=True))


def mech(q):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = (q > q.rolling(200).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    sc = (comp * (0.5 + 0.5 * above.astype(float))).values
    return sc, above, np.nan_to_num(vol20, nan=1e9)


def cadence_rows(idx, cad):
    m = rebalance_mask(idx, cad).shift(1, fill_value=False).values.copy()
    m[0] = True
    return np.flatnonzero(m)


class Panel:
    def __init__(self, name, px, invest, sleeve_px):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        self.reb = cadence_rows(px.index, CADENCE)
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        # sleeve daily returns, reindexed onto THIS panel's trading days (same device
        # baseline.load_universe uses to join SPY onto the small panel)
        s = sleeve_px.reindex(px.index, method="ffill")
        self.sret = {c: s[c].pct_change().fillna(0.0).values for c in s.columns}


def build1(pan, N, H, lag=1):
    """The record's min-hold selection frame at GROSS = 1.0; lag = 1 is rule 2.  The frame does
    not depend on the gross or on the sleeve, so it is built ONCE and scaled — which is exactly
    why (sleeve, gross) is a clean pair of dials here."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    reb = pan.reb
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
            k = pan.rank_key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
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
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def run(pan, frame, gross, sret=None):
    """Residual (1 - gross) goes to CASH at 0% when sret is None, otherwise to the SLEEVE, which
    is an ordinary long asset: it drifts, it is rebalanced on the same weekly grid, and it pays
    the same 10 bps on its own turnover.  Weights never sum above 1.0 (no leverage, no shorting).
    With sret=None this is bit-identical to the cash runner idea 1296/1346 committed."""
    rets = pan.rets
    T, M = rets.shape
    if sret is None:
        aug = rets
        extra = 0
    else:
        aug = np.hstack([rets, np.asarray(sret, float).reshape(-1, 1)])
        extra = 1
    C = np.cumprod(1.0 + aug, axis=0)
    Cp = np.vstack([np.ones((1, M + extra)), C[:-1]])
    turn = np.zeros(T)
    out = np.zeros(T)
    wsum = np.zeros(T)
    curw = np.zeros(M + extra)
    reb = np.asarray(pan.reb, dtype=np.int64)
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
        w0 = np.zeros(M + extra)
        w0[:M] = gross * frame[i0]
        if extra:
            w0[M] = 1.0 - gross
        wsum[i0] = w0.sum()
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        out[i0:i1] = ((A / V[:, None]) * aug[i0:i1]).sum(axis=1)
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return out, turn, wsum


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


def annvol(r):
    return float(np.std(np.asarray(r, float), ddof=0) * np.sqrt(252))


def annturn(tu, lo, hi):
    n = hi - lo
    return float(np.sum(tu[lo:hi]) * 252.0 / n) if n > 0 else np.nan


BOOT_REPS, BOOT_BLOCK, BOOT_SEED = 400, 63, 20260919


def paired_block_dsharpe(a, b, reps=BOOT_REPS, L=BOOT_BLOCK, seed=BOOT_SEED):
    """SE of (Sharpe(a) - Sharpe(b)) under a PAIRED circular block bootstrap: both series are
    resampled on IDENTICAL block starts, so the pairing (and hence the very high correlation
    between a book and its own vol-matched twin) is preserved and the SE is of the DIFFERENCE,
    not of either level.  Returns (observed d, SE, t)."""
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    nb = int(np.ceil(n / L))
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n, size=(reps, nb))
    off = np.arange(L)
    idx = (starts[:, :, None] + off[None, None, :]).reshape(reps, nb * L)[:, :n] % n
    A, B = a[idx], b[idx]

    def sh(X):
        v = X.std(axis=1, ddof=0) * np.sqrt(252)
        return np.where(v > 0, X.mean(axis=1) * 252 / v, np.nan)

    d = sh(A) - sh(B)
    obs = float(sharpe(a) - sharpe(b))
    se = float(np.nanstd(d, ddof=1))
    return obs, se, (obs / se if se > 0 else np.nan)


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


def main():
    t0 = time.time()
    say("=" * 124)
    say("IDEA 1358 (lane cloud, 2026-09-19) — does routing the incumbent's UNINVESTED GROSS into "
        "a BOND SLEEVE buy the BINDING 4b DD LEG?")
    say("DIALS: SLEEVE {CASH,SHY,IEF,TLT} x GROSS {0.50,0.60,0.75} at the frozen incumbent "
        "(N=15, H=126, MAXVOL 0.60, MA gate ON, weekly, 10 bps on EVERY leg incl. the sleeve, "
        "t+1).")
    say("=" * 124)

    raw = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True).sort_index()
    sleeve_px = raw[["SHY", "IEF", "TLT"]].ffill()

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    meta = ROOT / "data" / "small_meta.csv"
    if meta.exists():
        md = pd.read_csv(meta)
        col = "ticker" if "ticker" in md.columns else md.columns[0]
        bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
        say(f"  SMALL filter: data/small_meta.csv drops {len(bad)} tickers with "
            f"max_1d_move >= 1.0 (protocol-mandated).")
    else:
        bad = set()
        say("  SMALL filter: data/small_meta.csv absent; in-panel max |1d move| >= 1.0 screen.")
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"], sleeve_px),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"], sleeve_px),
              Panel("SMALL", pxS, inv, sleeve_px)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, "
        f"SMALL {len(inv)} (of {len(pxS.columns)-1} priced).")
    say("  SURVIVORSHIP (rule 9): U56 / B136 / SMALL are CURRENT-constituent lists; SMALL is a "
        "sub-$2B screen carried back to 2010, so its LEVELS are an upper bound and only its "
        "CONTRASTS across sleeve and gross are read here.  The SLEEVE tickers (SHY/IEF/TLT) are "
        "survivorship-free: they are three specific ETFs that existed throughout.")
    say("  NOTE, not a defect: on U56 and B136 the sleeve tickers are ALSO selectable by the "
        "scorer, so a sleeve cell can hold the same ETF twice (once by rank, once as residual). "
        "That is what an implementer would actually experience and it is left in.")
    say("  TAPE STAMP:")
    for p in panels:
        say(f"    {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y);  {len(p.reb)} weekly rebalances")
        publish(f"TAPE STAMP {p.name}",
                f"{len(p.idx)} rows, {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)

    # G2: the joined sleeve series IS the panel's own series where the panel prices it.
    # One convention throughout: the sleeve ALWAYS comes from data/prices.csv.  On U56 (built
    # from that same file) the match must be exact.  On B136 it is NOT exact, and that is idea
    # 353's standing open finding, not a defect of this run: data/prices_broad.csv is written by
    # a raw yf.download at a different decimal precision, so the same three ETFs differ at the
    # 1e-4 level daily.  Published with its magnitude and bounded, never asserted to zero.
    devs = {}
    for pn in panels:
        d = [float(np.nanmax(np.abs(pn.px[c].pct_change().fillna(0.0).values - pn.sret[c])))
             for c in ["SHY", "IEF", "TLT"] if c in pn.px.columns]
        devs[pn.name] = max(d) if d else None
    gate("G2a joined sleeve returns == U56's own columns (same source file, must be exact)",
         f"{devs['U56']:.3e}", "< 1e-12", devs["U56"] < 1e-12)
    gate("G2b B136's own sleeve columns are the SAME INSTRUMENTS at a different cache vintage "
         "(idea 353's open finding: data/prices_broad.csv is a raw yf.download)",
         f"{devs['B136']:.3e}", "< 1e-3 (bounded, not zero)", devs["B136"] < 1e-3)
    publish("G2c SMALL panel prices no sleeve ticker (no overlap to check)",
            str(devs["SMALL"]))

    say("\n  WHAT THE SLEEVES THEMSELVES DID (buy-and-hold, each panel's own window, post-warm-up)")
    for p in panels:
        for c in ["SHY", "IEF", "TLT"]:
            r = p.sret[c][WARMUP:]
            m = triple(r)
            h1, h2 = halves(r)
            i_oos = int(np.searchsorted(p.idx.values, np.datetime64(OOS_START)))
            mo = triple(p.sret[c][i_oos:])
            say(f"    {p.name:>6} {c}: CAGR {m['CAGR']:6.2%} Sharpe {m['Sharpe']:7.4f} MaxDD "
                f"{m['MaxDD']:7.2%} vol {annvol(r):5.2%} H1/H2 {h1:6.3f}/{h2:6.3f}  |  OOS "
                f"(2017+, contains 2022) {mo['CAGR']:6.2%}/{mo['Sharpe']:7.4f}/{mo['MaxDD']:7.2%}")
            publish(f"SLEEVE STANDALONE {p.name} {c}",
                    f"CAGR {m['CAGR']:.4f} Sharpe {m['Sharpe']:.4f} MaxDD {m['MaxDD']:.4f} "
                    f"OOS {mo['CAGR']:.4f}/{mo['Sharpe']:.4f}/{mo['MaxDD']:.4f}")

    grid, ctrl_rows, wf_rows, bench = [], [], [], {}
    max_wsum, n_empty_reb = 0.0, 0

    for pan in panels:
        n = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
        frame = build1(pan, I_N, I_H)

        say(f"\n  [{pan.name}]  SPY: CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.4f} MaxDD "
            f"{spy['MaxDD']:.2%} H1/H2 {spy['H1']:.4f}/{spy['H2']:.4f}  |  4b bars: DD cap "
            f"{DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps: CAGR {live['CAGR']:.2%} Sharpe "
            f"{live['Sharpe']:.4f} MaxDD {live['MaxDD']:.2%} H1/H2 {live['H1']:.4f}/"
            f"{live['H2']:.4f}")
        say(f"           OOS SPY {spyO['CAGR']:.2%}/{spyO['Sharpe']:.4f}/{spyO['MaxDD']:.2%}  |  "
            f"OOS RULES v2 {liveO['CAGR']:.2%}/{liveO['Sharpe']:.4f}/{liveO['MaxDD']:.2%}")

        # ---- CASH CONTROL LADDER (not a dial: the vol-matched twin for every sleeve cell) -----
        ctrl, ctrl_rr = [], {}
        for g_ in CTRL_GROSSES:
            gg, tu, _ = run(pan, frame, g_, None)
            rr = gg - tu * COST / 1e4
            r = rr[WARMUP:]
            m = triple(r)
            h1, h2 = halves(r)
            mo = triple(rr[i_oos:])
            d = dict(panel=pan.name, gross=g_, vol=annvol(r), CAGR=m["CAGR"],
                     Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                     OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                     turn=annturn(tu, WARMUP, n))
            ctrl.append(d)
            ctrl_rr[g_] = rr
            ctrl_rows.append(d)
        ctrl_vol = np.array([c["vol"] for c in ctrl])

        say(f"    {'sleeve':>6} {'gross':>5} | {'CAGR':>7} {'Sharpe':>7} {'MaxDD':>8} {'H1':>6} "
            f"{'H2':>6} | {'DDmargin':>8} {'CGmargin':>8} | {'vol':>6} {'turn':>5} {'drag':>6} | "
            f"{'OOSCAGR':>8} {'OOSShrp':>7} {'OOSMaxDD':>8} | {'ISShrp':>7} | {'vs CASH same-g':>15}"
            f" {'vs VOLMATCH':>12} | 4a 4b  fail-legs")
        runs = {}
        for slv in SLEEVES:
            for g_ in GROSSES:
                sret = None if slv == "CASH" else pan.sret[slv]
                gg, tu, wsum = run(pan, frame, g_, sret)
                if sret is not None:
                    act = wsum[np.asarray(pan.reb, dtype=np.int64)]
                    max_wsum = max(max_wsum, float(np.max(act)))
                    # frame rows are 1/len(sel) so they sum to EXACTLY 1 when any name is
                    # selected and to 0 when none is (early warm-up / nothing eligible); the
                    # latter leaves (1-gross) in the sleeve and gross in cash, which is the
                    # correct analogue of the cash book holding everything in cash.
                    full = act[np.abs(act - 1.0) < 1e-12]
                    n_empty_reb = max(n_empty_reb, int(len(act) - len(full)))
                rr = gg - tu * COST / 1e4
                r = rr[WARMUP:]
                turn = annturn(tu, WARMUP, n)
                ka, kb, m, h1, h2, legs = keep_paths(r, spy, live)
                mo = triple(rr[i_oos:])
                kb_oos = bool(mo["Sharpe"] > spyO["Sharpe"])
                runs[(slv, g_)] = rr
                ddm = m["MaxDD"] - DD_CAP * spy["MaxDD"]
                cgm = m["CAGR"] - CAGR_FLOOR * spy["CAGR"]
                v = annvol(r)
                same = [c for c in ctrl if abs(c["gross"] - g_) < 1e-9][0]
                j = int(np.argmin(np.abs(ctrl_vol - v)))
                vm = ctrl[j]
                row = dict(panel=pan.name, sleeve=slv, gross=g_,
                           CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                           DD_margin_pp=ddm, CAGR_margin_pp=cgm,
                           vol_real=v, turn=turn, cost_drag_bp=turn * COST, n_rebal=len(pan.reb),
                           OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                           IS_Sharpe=sharpe(rr[WARMUP:i_oos]),
                           dS_vs_cash_same_gross=m["Sharpe"] - same["Sharpe"],
                           dCAGR_vs_cash_same_gross=m["CAGR"] - same["CAGR"],
                           dDD_vs_cash_same_gross=m["MaxDD"] - same["MaxDD"],
                           volmatch_gross=vm["gross"], volmatch_vol=vm["vol"],
                           dS_vs_volmatch=m["Sharpe"] - vm["Sharpe"],
                           dCAGR_vs_volmatch=m["CAGR"] - vm["CAGR"],
                           dDD_vs_volmatch=m["MaxDD"] - vm["MaxDD"],
                           dOOS_S_vs_volmatch=mo["Sharpe"] - vm["OOS_Sharpe"],
                           SPY_Sharpe=spy["Sharpe"], SPY_CAGR=spy["CAGR"],
                           SPY_MaxDD=spy["MaxDD"], LIVE_Sharpe=live["Sharpe"],
                           LIVE_MaxDD=live["MaxDD"], OOS_SPY_Sharpe=spyO["Sharpe"],
                           OOS_SPY_CAGR=spyO["CAGR"], OOS_SPY_MaxDD=spyO["MaxDD"],
                           OOS_LIVE_Sharpe=liveO["Sharpe"],
                           keep4a=ka, keep4b=kb, keep4b_oos_sharpe=kb_oos,
                           keep4b_and_oos=bool(kb and kb_oos),
                           leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"],
                           leg_CAGR=legs["CAGR"])
                grid.append(row)
                say(f"    {slv:>6} {g_:5.2f} | {m['CAGR']:7.2%} {m['Sharpe']:7.4f} "
                    f"{m['MaxDD']:8.2%} {h1:6.3f} {h2:6.3f} | {ddm:+8.2%} {cgm:+8.2%} | "
                    f"{v:6.2%} {turn:5.2f} {turn*COST:6.1f} | {mo['CAGR']:8.2%} "
                    f"{mo['Sharpe']:7.4f} {mo['MaxDD']:8.2%} | {row['IS_Sharpe']:7.4f} | "
                    f"{row['dS_vs_cash_same_gross']:+15.4f} "
                    f"{row['dS_vs_volmatch']:+7.4f}@g{vm['gross']:.2f} | "
                    f"{int(ka)}  {int(kb)}   "
                    + (",".join(k for k, v_ in legs.items() if not v_) or "-"))
        bench[pan.name] = dict(spy=spy, spyO=spyO, live=live, liveO=liveO, runs=runs,
                               i_oos=i_oos, n=n, ctrl=ctrl, ctrl_rr=ctrl_rr)

        a = [r for r in grid if r["panel"] == pan.name and r["sleeve"] == ANCHOR_SLV
             and r["gross"] == ANCHOR_G][0]
        c = C_ANCHOR[pan.name]
        dev = max(abs(a[k] - v) for k, v in c.items())
        gate(f"G1 cross-script replay of idea 1296/1346's {pan.name} anchor (CASH, gross 0.60) "
             f"on CAGR/Sharpe/MaxDD/H1/H2/turn", f"{dev:.3e}", "< 5e-6", dev < 5e-6)

    gate("G3 NO LEVERAGE (rule 2): max weight sum over every sleeve cell and rebalance",
         f"{max_wsum:.12f}", "<= 1.0 + 1e-12", max_wsum <= 1.0 + 1e-12)
    publish("G3b rebalances where NO name was selected (sleeve held alone, rest in cash) — "
            "worst cell", str(n_empty_reb))

    G = pd.DataFrame(grid)
    CTRL = pd.DataFrame(ctrl_rows)

    say("\n" + "=" * 124)
    say("1. DOES THE SLEEVE BUY THE DD LEG?  (DD margin = MaxDD - 0.60 x SPY MaxDD; CAGR margin = "
        "CAGR - 0.70 x SPY CAGR.  BOTH must be >= 0 for 4b.)")
    say("=" * 124)
    for p in G.panel.unique():
        for slv in SLEEVES:
            sub = G[(G.panel == p) & (G.sleeve == slv)].sort_values("gross")
            say(f"    {p:>6} {slv:>4}: " + "  ".join(
                f"g{r.gross:.2f}[DD {r.DD_margin_pp:+.2%} / CG {r.CAGR_margin_pp:+.2%} / "
                f"S {r.Sharpe:.4f} / 4b {int(r.keep4b)}]" for r in sub.itertuples()))
        anc = G[(G.panel == p) & (G.sleeve == ANCHOR_SLV) & (G.gross == ANCHOR_G)].iloc[0]
        better = G[(G.panel == p) & (G.sleeve != "CASH")
                   & (G.MaxDD > anc.MaxDD) & (G.CAGR > anc.CAGR)]
        say(f"      -> {p}: sleeve cells with BOTH a shallower MaxDD AND a higher CAGR than the "
            f"frozen (CASH, 0.60) anchor: "
            + (", ".join(f"{r.sleeve}@g{r.gross:.2f}" for r in better.itertuples())
               if len(better) else "NONE"))

    say("\n2. IS THE SLEEVE AN EDGE OR AN EXPOSURE DIAL?  (every sleeve cell vs the CASH book on "
        "the 0.35-1.00 control ladder whose REALISED VOL is nearest)")
    for p in G.panel.unique():
        for slv in [s for s in SLEEVES if s != "CASH"]:
            sub = G[(G.panel == p) & (G.sleeve == slv)].sort_values("gross")
            say(f"    {p:>6} {slv:>4}: " + "  ".join(
                f"g{r.gross:.2f}[dS {r.dS_vs_volmatch:+.4f} dCAGR {r.dCAGR_vs_volmatch:+.2%} "
                f"dDD {r.dDD_vs_volmatch:+.2%} dOOSs {r.dOOS_S_vs_volmatch:+.4f} "
                f"(twin g{r.volmatch_gross:.2f} vol {r.volmatch_vol:.2%} vs {r.vol_real:.2%})]"
                for r in sub.itertuples()))
    ns = G[G.sleeve != "CASH"]
    say(f"    POOLED over all {len(ns)} sleeve cells vs their vol-matched CASH twins: mean dSharpe "
        f"{ns.dS_vs_volmatch.mean():+.4f} (positive in {int((ns.dS_vs_volmatch>0).sum())} of "
        f"{len(ns)}), mean dCAGR {ns.dCAGR_vs_volmatch.mean():+.2%}, mean dMaxDD "
        f"{ns.dDD_vs_volmatch.mean():+.2%} (positive = SHALLOWER), mean dOOS Sharpe "
        f"{ns.dOOS_S_vs_volmatch.mean():+.4f} (positive in "
        f"{int((ns.dOOS_S_vs_volmatch>0).sum())} of {len(ns)}).")
    say(f"    And vs the CASH book at the SAME gross (the un-matched, flattering comparison): mean "
        f"dSharpe {ns.dS_vs_cash_same_gross.mean():+.4f} (positive in "
        f"{int((ns.dS_vs_cash_same_gross>0).sum())} of {len(ns)}), mean dCAGR "
        f"{ns.dCAGR_vs_cash_same_gross.mean():+.2%}, mean dMaxDD "
        f"{ns.dDD_vs_cash_same_gross.mean():+.2%}.")

    say("\n2b. IS THAT GAIN RESOLVABLE AT ALL?  Paired circular-block bootstrap of "
        f"(sleeve Sharpe - vol-matched CASH twin Sharpe): {BOOT_REPS} reps x {BOOT_BLOCK}-row "
        f"blocks, seed {BOOT_SEED}, BOTH books resampled on IDENTICAL blocks.  |t| > 2 = "
        "resolvable.")
    boot_rows = []
    for p in G.panel.unique():
        b = bench[p]
        for slv in [x for x in SLEEVES if x != "CASH"]:
            outs = []
            for g_ in GROSSES:
                r = b["runs"][(slv, g_)]
                cell = G[(G.panel == p) & (G.sleeve == slv) & (G.gross == g_)].iloc[0]
                tw = b["ctrl_rr"][float(cell.volmatch_gross)]
                o, se, t = paired_block_dsharpe(r[WARMUP:], tw[WARMUP:])
                oo, seo, to = paired_block_dsharpe(r[b["i_oos"]:], tw[b["i_oos"]:])
                boot_rows.append(dict(panel=p, sleeve=slv, gross=g_,
                                      volmatch_gross=float(cell.volmatch_gross),
                                      full_dS=o, full_SE=se, full_t=t,
                                      oos_dS=oo, oos_SE=seo, oos_t=to,
                                      full_resolvable=bool(abs(t) > 2),
                                      oos_resolvable=bool(abs(to) > 2)))
                outs.append(f"g{g_:.2f}[full {o:+.4f} +-{se:.4f} t{t:+.2f} | OOS {oo:+.4f} "
                            f"+-{seo:.4f} t{to:+.2f}]")
            say(f"    {p:>6} {slv:>4}: " + "  ".join(outs))
    BOOT = pd.DataFrame(boot_rows)
    say(f"    RESOLVABLE (|t| > 2) on the FULL sample: {int(BOOT.full_resolvable.sum())} of "
        f"{len(BOOT)} sleeve cells;  OOS: {int(BOOT.oos_resolvable.sum())} of {len(BOOT)}.")
    for slv in [x for x in SLEEVES if x != "CASH"]:
        sb = BOOT[BOOT.sleeve == slv]
        say(f"      {slv:>4}: full mean t {sb.full_t.mean():+.2f} (resolvable "
            f"{int(sb.full_resolvable.sum())}/{len(sb)}), OOS mean t {sb.oos_t.mean():+.2f} "
            f"(resolvable {int(sb.oos_resolvable.sum())}/{len(sb)}); OOS dS positive in "
            f"{int((sb.oos_dS > 0).sum())}/{len(sb)}, median SE {sb.oos_SE.median():.4f}")

    say("\n3. KEEP PATHS OVER ALL 36 CELLS")
    say(f"    4a (beat the live book): {int(G.keep4a.sum())} of {len(G)}")
    say(f"    4b full-sample: {int(G.keep4b.sum())} of {len(G)};  4b full AND OOS Sharpe > SPY: "
        f"{int(G.keep4b_and_oos.sum())} of {len(G)}")
    for p in G.panel.unique():
        s = G[G.panel == p]
        say(f"      {p:>6}: 4a {int(s.keep4a.sum())}/{len(s)}   4b {int(s.keep4b.sum())}/{len(s)}"
            f"   4b+OOS {int(s.keep4b_and_oos.sum())}/{len(s)}")
    for slv in SLEEVES:
        s = G[G.sleeve == slv]
        say(f"      {slv:>6}: 4a {int(s.keep4a.sum())}/{len(s)}   4b {int(s.keep4b.sum())}/"
            f"{len(s)}   4b+OOS {int(s.keep4b_and_oos.sum())}/{len(s)}")
    for g_ in GROSSES:
        s = G[G.gross == g_]
        say(f"      g{g_:.2f}: 4a {int(s.keep4a.sum())}/{len(s)}   4b {int(s.keep4b.sum())}/"
            f"{len(s)}   4b+OOS {int(s.keep4b_and_oos.sum())}/{len(s)}")
    fails = dict(H1=int((~G.leg_H1).sum()), H2=int((~G.leg_H2).sum()),
                 DD=int((~G.leg_DD).sum()), CAGR=int((~G.leg_CAGR).sum()))
    say(f"    4b binding legs across all {len(G)} cells: " + ", ".join(
        f"{k} fails {v}" for k, v in sorted(fails.items(), key=lambda kv: -kv[1])))
    say("    Cells that BEAT the frozen (CASH, 0.60) incumbent on full-sample Sharpe AND pass 4b "
        "full+OOS:")
    any_dom = False
    for p in G.panel.unique():
        anc = G[(G.panel == p) & (G.sleeve == ANCHOR_SLV) & (G.gross == ANCHOR_G)].iloc[0]
        d = G[(G.panel == p) & (G.Sharpe > anc.Sharpe) & G.keep4b_and_oos]
        for r in d.itertuples():
            any_dom = True
            say(f"      {p} {r.sleeve}@g{r.gross:.2f}: {r.Sharpe:.4f} vs anchor {anc.Sharpe:.4f} "
                f"(+{r.Sharpe-anc.Sharpe:.4f}), OOS {r.OOS_Sharpe:.4f} vs {anc.OOS_Sharpe:.4f}, "
                f"MaxDD {r.MaxDD:.2%} vs {anc.MaxDD:.2%}, CAGR {r.CAGR:.2%} vs {anc.CAGR:.2%}, "
                f"vs vol-matched CASH twin dS {r.dS_vs_volmatch:+.4f}")
    if not any_dom:
        say("      NONE on any panel.")

    # ---- rule 8 ---------------------------------------------------------------------------
    say("\n4. RULE 8 WALK-FORWARD — the (SLEEVE, GROSS) PAIR chosen on warm-up..2016-12-31 by "
        "argmax IS Sharpe; 2017-2026 read ONCE")
    say("=" * 124)
    for p in G.panel.unique():
        b = bench[p]
        sub = G[G.panel == p]
        pick = sub.loc[sub.IS_Sharpe.idxmax()]
        anc = sub[(sub.sleeve == ANCHOR_SLV) & (sub.gross == ANCHOR_G)].iloc[0]
        ro = b["runs"][(pick.sleeve, float(pick.gross))][b["i_oos"]:]
        h1o, h2o = halves(ro)
        legs_oos = dict(OOS_Sharpe_vs_SPY=bool(pick.OOS_Sharpe > b["spyO"]["Sharpe"]),
                        DD=bool(pick.OOS_MaxDD >= DD_CAP * b["spyO"]["MaxDD"]),
                        CAGR=bool(pick.OOS_CAGR >= CAGR_FLOOR * b["spyO"]["CAGR"]))
        anc_legs_oos = dict(OOS_Sharpe_vs_SPY=bool(anc.OOS_Sharpe > b["spyO"]["Sharpe"]),
                            DD=bool(anc.OOS_MaxDD >= DD_CAP * b["spyO"]["MaxDD"]),
                            CAGR=bool(anc.OOS_CAGR >= CAGR_FLOOR * b["spyO"]["CAGR"]))
        best_oos = sub.loc[sub.OOS_Sharpe.idxmax()]
        wf = dict(panel=p, IS_pick_sleeve=pick.sleeve, IS_pick_gross=float(pick.gross),
                  IS_Sharpe=pick.IS_Sharpe, ANCHOR_IS_Sharpe=anc.IS_Sharpe,
                  IS_margin_over_anchor=pick.IS_Sharpe - anc.IS_Sharpe,
                  is_the_incumbent=bool(pick.sleeve == ANCHOR_SLV and pick.gross == ANCHOR_G),
                  OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                  OOS_H1=h1o, OOS_H2=h2o,
                  ANCHOR_OOS_CAGR=anc.OOS_CAGR, ANCHOR_OOS_Sharpe=anc.OOS_Sharpe,
                  ANCHOR_OOS_MaxDD=anc.OOS_MaxDD,
                  dOOS_Sharpe_vs_anchor=pick.OOS_Sharpe - anc.OOS_Sharpe,
                  dOOS_CAGR_vs_anchor=pick.OOS_CAGR - anc.OOS_CAGR,
                  dOOS_MaxDD_vs_anchor=pick.OOS_MaxDD - anc.OOS_MaxDD,
                  SPY_OOS_CAGR=b["spyO"]["CAGR"], SPY_OOS_Sharpe=b["spyO"]["Sharpe"],
                  SPY_OOS_MaxDD=b["spyO"]["MaxDD"],
                  LIVE_OOS_CAGR=b["liveO"]["CAGR"], LIVE_OOS_Sharpe=b["liveO"]["Sharpe"],
                  LIVE_OOS_MaxDD=b["liveO"]["MaxDD"],
                  keep4b_oos_all=bool(all(legs_oos.values())),
                  anchor_keep4b_oos_all=bool(all(anc_legs_oos.values())),
                  oos_fail_legs=",".join(k for k, v in legs_oos.items() if not v) or "-",
                  best_OOS_sleeve=best_oos.sleeve, best_OOS_gross=float(best_oos.gross),
                  best_OOS_Sharpe=best_oos.OOS_Sharpe)
        wf_rows.append(wf)
        say(f"    {p:>6}: IS pick ({pick.sleeve}, g{pick.gross:.2f}) IS Sharpe "
            f"{pick.IS_Sharpe:.4f} (anchor {anc.IS_Sharpe:.4f}, margin "
            f"{pick.IS_Sharpe-anc.IS_Sharpe:+.5f}) -> OOS {pick.OOS_CAGR:7.2%}/"
            f"{pick.OOS_Sharpe:.4f}/{pick.OOS_MaxDD:7.2%}")
        say(f"            vs FROZEN (CASH, 0.60) {anc.OOS_CAGR:7.2%}/{anc.OOS_Sharpe:.4f}/"
            f"{anc.OOS_MaxDD:7.2%}   d Sharpe {pick.OOS_Sharpe-anc.OOS_Sharpe:+.4f}, d CAGR "
            f"{pick.OOS_CAGR-anc.OOS_CAGR:+.2%}, d MaxDD {pick.OOS_MaxDD-anc.OOS_MaxDD:+.2%}")
        say(f"            vs SPY {b['spyO']['CAGR']:7.2%}/{b['spyO']['Sharpe']:.4f}/"
            f"{b['spyO']['MaxDD']:7.2%}   vs RULES v2 {b['liveO']['CAGR']:7.2%}/"
            f"{b['liveO']['Sharpe']:.4f}/{b['liveO']['MaxDD']:7.2%}")
        say(f"            4b on every OOS leg: pick {int(wf['keep4b_oos_all'])} "
            f"[{wf['oos_fail_legs']}]  anchor {int(wf['anchor_keep4b_oos_all'])}   | ex-post best "
            f"OOS cell ({wf['best_OOS_sleeve']}, g{wf['best_OOS_gross']:.2f}) "
            f"{wf['best_OOS_Sharpe']:.4f}")

    WF = pd.DataFrame(wf_rows)
    say(f"\n    The IS chooser lands on the frozen incumbent (CASH, 0.60) in "
        f"{int(WF.is_the_incumbent.sum())} of {len(WF)} panels.")
    say(f"    Mean OOS Sharpe of the IS-chosen PAIR minus the frozen incumbent: "
        f"{WF.dOOS_Sharpe_vs_anchor.mean():+.4f} (min {WF.dOOS_Sharpe_vs_anchor.min():+.4f}, "
        f"max {WF.dOOS_Sharpe_vs_anchor.max():+.4f}); it beats the incumbent in "
        f"{int((WF.dOOS_Sharpe_vs_anchor > 0).sum())} of {len(WF)}.")
    say(f"    Mean OOS CAGR difference: {WF.dOOS_CAGR_vs_anchor.mean():+.2%};  mean OOS MaxDD "
        f"difference: {WF.dOOS_MaxDD_vs_anchor.mean():+.2%} (positive = SHALLOWER).")
    say(f"    4b on every OOS leg after rule 8: pick {int(WF.keep4b_oos_all.sum())} of {len(WF)}, "
        f"anchor {int(WF.anchor_keep4b_oos_all.sum())} of {len(WF)}.")
    hind = int(((WF.best_OOS_sleeve != WF.IS_pick_sleeve)
                | (WF.best_OOS_gross != WF.IS_pick_gross)).sum())
    say(f"    H_HINDSIGHT: the ex-post best OOS cell differs from the IS pick on {hind} of "
        f"{len(WF)} panels.")

    say("\n5. THE 2022 QUESTION — the sleeve's own worst year inside the book (calendar-year "
        "returns of each cell, U56 only, the panel the incumbent is carried on)")
    b = bench["U56"]
    idx = panels[0].idx
    for slv in SLEEVES:
        for g_ in [ANCHOR_G]:
            rr = pd.Series(b["runs"][(slv, g_)], index=idx)
            yr = (1 + rr).groupby(rr.index.year).prod() - 1
            say(f"    {slv:>4} g{g_:.2f}: " + "  ".join(
                f"{y}:{v:+6.1%}" for y, v in yr.items() if y >= 2018))

    say("\n6. THE FULL CASH CONTROL LADDER (0.35-1.00), for the reader who wants the raw exposure "
        "shape the sleeve is being scored against")
    for p in CTRL.panel.unique():
        sub = CTRL[CTRL.panel == p].sort_values("gross")
        say(f"    {p:>6}: " + "  ".join(
            f"g{r.gross:.2f}({r.Sharpe:.3f}/{r.CAGR:.1%}/{r.MaxDD:.1%}/v{r.vol:.1%})"
            for r in sub.itertuples()))

    G.to_csv(f"{OUT}.grid.csv", index=False)
    CTRL.to_csv(f"{OUT}.controls.csv", index=False)
    BOOT.to_csv(f"{OUT}.bootstrap.csv", index=False)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n  wrote {Path(OUT).name}.grid.csv ({len(G)} cells), .controls.csv ({len(CTRL)}), "
        f".bootstrap.csv ({len(BOOT)}), .walkforward.csv ({len(WF)}), .gates.csv")
    asserted = [g for g in GATES if g["target"] != "published, not asserted"]
    say(f"  GATES: {sum(g['pass_'] for g in asserted)}/{len(asserted)} asserted pass "
        f"(plus {len(GATES)-len(asserted)} published stamps)")
    say(f"  elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
