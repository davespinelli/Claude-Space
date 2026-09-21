#!/usr/bin/env python3
"""Idea 2060 (lane B, 2026-09-21) — IS THE STANDING KEEP-4b CELL'S CAGR-FLOOR MARGIN
RESOLVABLE, OR IS +1.92 pp A POINT ESTIMATE WITH NO ERROR BAR?

THE QUESTION.  The standing KEEP-candidate (VOLTGT-DRIFT on B136, `t = 0.10`, `h = 0.08`, trade
W, 10 bps, t+1 — memo `research/backtests/2026-09-20_voltgt-drift-b136_KEEP4b_MEMO.md`) passes
PROTOCOL 4b on all five legs.  The memo's own caveat 7 calls the CAGR leg thin: the book's 12.51%
clears `0.70 x SPY` (10.58%) by **+1.92 pp**, and idea 2064's adversarial survivor deletion showed
that is the leg every deletion spends.  That +1.92 pp has never carried a standard error.  This
run resamples the BOOK and SPY on the SAME day blocks and publishes the margin's SE, bootstrap t,
two-sided p and percentile interval, for all five 4b legs and for the JOINT five-leg pass — so the
record stops quoting a CAGR-floor pass without one.

THE TWO TUNED PARAMETERS (PROTOCOL rule 4; every grid point reported, none hidden):
    P1  B      circular-block length, trading days   {5, 10, 21, 63, 126}
    P2  seed   bootstrap seed                        {11, 22, 33}   (a resolution control:
               the spread across seeds bounds how much of any SE is Monte-Carlo noise)
    nboot = 4000 per (B, seed).  Nothing about the BOOK is tuned here: (t, h), panel, cadence,
    cost and the sigma convention are all INHERITED from the standing memo, unchanged.

REPORTED, NOT TUNED: panel {B136 (the cell), U56 (a second read)}, cost {0, 10, 25, 50} bps,
window {FULL, OOS}.

BOOTSTRAP CONVENTION (stated because idea 1511/1537 showed the convention moves the number):
  * PAIRED.  Book and SPY are resampled with the SAME circular-block offsets inside a draw, so
    the difference keeps its day-by-day pairing and the SE is of the CONTRAST, not of two levels.
  * PER-WINDOW.  Each 4b leg is resampled on the calendar window it is READ on (H1 days for L1,
    H2 days for L2, 2017+ days for L3, the whole book window for L4/L5).  A single full-sample
    resample would let H1 days land in the H2 half and destroy what "half" means; this convention
    keeps every leg's window intact and only shuffles blocks inside it.
  * JOINT.  Draw k of every window shares the seed stream, so the five legs can be read together
    for a joint 4b pass rate.  The windows are resampled INDEPENDENTLY of each other (they are
    disjoint day sets), which is an assumption, not a fact — stated, not repaired.
  * CAGR on a resampled path is `prod(1+r)^(252/n) - 1`; MaxDD is of the resampled path.  A
    block bootstrap of a drawdown is conservative-to-noisy by construction (it breaks the single
    longest loss run); L4 is reported for completeness, and the headline claim is L5.

PROTOCOL: rule 2 (10 bps headline, t+1 next-day execution, gross capped at 1.00, no leverage);
rule 3 (live RULES v2 AND SPY); rule 4 (both KEEP paths, <= 2 tuned parameters, all grid points
reported); rule 5 (one idea, deterministic, standalone); rule 8 (walk-forward: (t, h) chosen on
2009-2016 ONLY, 2017-2026 read exactly once, and the pick's OOS margin bootstrapped); rule 9
(survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP.  B136 and U56 are CURRENT-constituent lists.  Every CAGR/MaxDD LEVEL here is
optimistic and both 4b bars are easier than on a point-in-time panel.  The SE is a same-tape,
same-names, paired contrast, so it is first-order immune to that bias; the PASS LEVELS are not.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-21_cagr-floor-margin-paired-block-bootstrap_B.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights                  # noqa: E402
from engine import backtest as engine_backtest, rebalance_mask        # noqa: E402

DATE, SLUG, LANE = "2026-09-21", "cagr-floor-margin-paired-block-bootstrap", "B"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

# ---------------------------------------------------------------- inherited, NOT tuned
WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SIG_L, SIG_D = 20, 0
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST0 = 10
COSTS = [0, 10, 25, 50]
CELL = dict(target=0.10, h=0.08, T_trade="W")        # the standing KEEP-4b cell, verbatim
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]

# ---------------------------------------------------------------- the two tuned parameters
BLOCKS = [5, 10, 21, 63, 126]
SEEDS = [11, 22, 33]
NBOOT = 4000

# rule-8 grid (idea 1799/2022's inherited dials; the chooser walks it, nothing new is invented)
TARGETS = [0.08, 0.10, 0.12, 0.16, 0.20]
THRESH = [0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.16, 0.20, 0.25]

# committed numbers this run must reproduce (the standing memo, points 2/4/5)
PUB = dict(CAGR=0.1251, Sharpe=1.2286, MaxDD=-0.1181, H1=1.3171, H2=1.1415,
           oCAGR=0.1301, oSharpe=1.2928, oMaxDD=-0.1181,
           spy_CAGR=0.1512, spy_Sharpe=0.8844, spy_MaxDD=-0.3372,
           spy_H1=0.9571, spy_H2=0.8249, spy_oCAGR=0.1526, spy_oSharpe=0.8737,
           L1=0.3600, L2=0.3166, L3=0.4191, L4=0.0842, L5=0.0192)

_log: list[str] = []
_gates: list[dict] = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _log.append(s)


def gate(name, value, target, ok):
    _gates.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    log(f"  GATE {'PASS' if ok else 'FAIL'}  {name}: {value}   (target {target})")
    return bool(ok)


# ---------------------------------------------------------------- book machinery (idea 1799/2034 verbatim)
def eq_weight(px, cols):
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.reindex(columns=px.columns).fillna(0.0)


def panel_sigma(px, cols, L=SIG_L, d=SIG_D):
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    pr = (ew.shift(1) * sub.pct_change()).sum(axis=1)
    s = pr.rolling(L).std() * np.sqrt(252.0)
    return s.shift(d) if d else s


def bt_drift(px_ret, W0, g0, mT, h):
    n = len(px_ret)
    cur = np.zeros(px_ret.shape[1])
    held = np.empty_like(px_ret)
    turn = np.zeros(n)
    g_eff = g0[0]
    nref = 0
    for i in range(n):
        trig = abs(g0[i] - cur.sum()) > h
        if trig or i == 0:
            g_eff = g0[i]
            nref += 1
        if mT[i] or i == 0:
            new = W0[i] * g_eff
            turn[i] = np.abs(new - cur).sum()
            cur = new
        elif trig:
            s = cur.sum()
            if s > 0:
                new = cur * (g_eff / s)
                turn[i] = np.abs(new - cur).sum()
                cur = new
        held[i] = cur
        gr = cur * (1.0 + px_ret[i])
        tot = gr.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = gr / tot
    return (held * px_ret).sum(axis=1), turn, held.sum(axis=1), nref


class Book:
    def __init__(self, px, cols):
        self.index = px.index
        self.R = np.nan_to_num(px.pct_change().values, nan=0.0)
        ew = np.nan_to_num(eq_weight(px, cols).values, nan=0.0)
        self.W = np.vstack([np.zeros((1, ew.shape[1])), ew[:-1]])
        self.SIG = panel_sigma(px, cols)
        m = np.asarray(rebalance_mask(px.index, CELL["T_trade"]).values, bool)
        self.mT = np.concatenate([[False], m[:-1]])

    def g_of(self, tgt):
        g = (tgt / self.SIG.replace(0, np.nan)).clip(upper=1.0).fillna(0.0).values
        return np.concatenate([[0.0], g[:-1]])

    def run(self, tgt, h):
        r, t, gs, nref = bt_drift(self.R, self.W, self.g_of(tgt), self.mT, h)
        return (pd.Series(r, index=self.index), pd.Series(t, index=self.index),
                pd.Series(gs, index=self.index), nref)


def net(r0, t0, c):
    return r0 - t0 * c / 1e4


def mets(r):
    r = pd.Series(r).dropna()
    eq = (1 + r).cumprod()
    yrs = len(r) / 252.0
    vol = r.std() * np.sqrt(252.0)
    return dict(CAGR=float(eq.iloc[-1] ** (1 / yrs) - 1) if yrs else np.nan,
                Sharpe=float((r.mean() * 252.0) / vol) if vol else np.nan,
                MaxDD=float((eq / eq.cummax() - 1).min()))


def halves(r):
    h = len(r) // 2
    return mets(r.iloc[:h])["Sharpe"], mets(r.iloc[h:])["Sharpe"]


def legs_of(rb, spy):
    """The five 4b leg MARGINS (all positive == pass), exactly as the memo states them."""
    mb, ms = mets(rb), mets(spy)
    bh1, bh2 = halves(rb)
    sh1, sh2 = halves(spy)
    ob, os_ = mets(rb.loc[OOS_START:]), mets(spy.loc[OOS_START:])
    return dict(L1_H1=bh1 - sh1, L2_H2=bh2 - sh2, L3_OOS=ob["Sharpe"] - os_["Sharpe"],
                L4_DD=mb["MaxDD"] - DD_CAP * ms["MaxDD"],
                L5_CAGR=mb["CAGR"] - CAGR_FLOOR * ms["CAGR"],
                CAGR=mb["CAGR"], Sharpe=mb["Sharpe"], MaxDD=mb["MaxDD"], H1=bh1, H2=bh2,
                oCAGR=ob["CAGR"], oSharpe=ob["Sharpe"], oMaxDD=ob["MaxDD"])


# ---------------------------------------------------------------- vectorised bootstrap kernels
def block_index(n, B, nboot, rng):
    """Circular-block index matrix (nboot x n): ceil(n/B) wrapped blocks, truncated to n."""
    nb = int(np.ceil(n / B))
    starts = rng.integers(0, n, size=(nboot, nb))
    off = np.arange(B)
    return ((starts[:, :, None] + off[None, None, :]).reshape(nboot, nb * B) % n)[:, :n]


def sharpe_rows(X):
    sd = X.std(axis=1, ddof=1)
    return np.where(sd > 0, X.mean(axis=1) * 252.0 / (sd * np.sqrt(252.0)), np.nan)


def cagr_rows(X):
    n = X.shape[1]
    e = np.cumprod(1.0 + X, axis=1)[:, -1]
    return np.where(e > 0, e ** (252.0 / n) - 1.0, np.nan)


def mdd_rows(X):
    e = np.cumprod(1.0 + X, axis=1)
    return (e / np.maximum.accumulate(e, axis=1) - 1.0).min(axis=1)


def boot_row(obs, draws):
    """SE, bootstrap t, two-sided p against the centred null, 95% percentile band and the
    share of draws on the WRONG side of zero (the leg failing)."""
    d = np.asarray(draws, float)
    d = d[np.isfinite(d)]
    if len(d) < 50:
        return dict(SE=np.nan, t=np.nan, p2=np.nan, mean=np.nan, lo=np.nan, hi=np.nan,
                    fail_share=np.nan, n=len(d))
    se = float(d.std(ddof=1))
    centred = d - d.mean()
    p2 = float(2.0 * min((centred >= abs(obs)).mean(), (centred <= -abs(obs)).mean()))
    return dict(SE=se, t=float(obs / se) if se > 0 else np.nan, p2=min(1.0, p2),
                mean=float(d.mean()), lo=float(np.percentile(d, 2.5)),
                hi=float(np.percentile(d, 97.5)),
                fail_share=float((d <= 0).mean()), n=len(d))


def draw_legs(rb, spy, B, seed, nboot=NBOOT):
    """Paired circular-block draws of all five leg margins, each on ITS OWN calendar window.
    Returns a dict leg -> (nboot,) array, plus the book's own resampled CAGR/MaxDD."""
    b, s = rb.values, spy.values
    h = len(b) // 2
    win = {"FULL": (b, s), "H1": (b[:h], s[:h]), "H2": (b[h:], s[h:])}
    oos = rb.index >= pd.Timestamp(OOS_START)
    win["OOS"] = (b[oos], s[oos])
    D = {}
    for k, (bb, ss) in win.items():
        rng = np.random.default_rng(seed + 1000 * (1 + list(win).index(k)))
        idx = block_index(len(bb), B, nboot, rng)
        D[k] = (bb[idx], ss[idx])
    Xb, Xs = D["FULL"]
    out = dict(L1_H1=sharpe_rows(D["H1"][0]) - sharpe_rows(D["H1"][1]),
               L2_H2=sharpe_rows(D["H2"][0]) - sharpe_rows(D["H2"][1]),
               L3_OOS=sharpe_rows(D["OOS"][0]) - sharpe_rows(D["OOS"][1]),
               L4_DD=mdd_rows(Xb) - DD_CAP * mdd_rows(Xs),
               L5_CAGR=cagr_rows(Xb) - CAGR_FLOOR * cagr_rows(Xs))
    out["_bookCAGR"] = cagr_rows(Xb)
    out["_spyCAGR"] = cagr_rows(Xs)
    out["_oosL5"] = cagr_rows(D["OOS"][0]) - CAGR_FLOOR * cagr_rows(D["OOS"][1])
    return out


# ---------------------------------------------------------------- main
def main():
    log(f"# Idea 2060 (lane {LANE}, {DATE}) — is the standing KEEP-4b cell's CAGR-FLOOR MARGIN "
        f"RESOLVABLE against a PAIRED BLOCK BOOTSTRAP of SPY?")
    log(f"# CELL (inherited, nothing tuned): VOLTGT-DRIFT, t={CELL['target']}, h={CELL['h']}, "
        f"trade {CELL['T_trade']}, {COST0} bps, t+1, gross <= 1.00, sigma (L={SIG_L}, d={SIG_D}).")
    log(f"# TUNED (2): block length B {BLOCKS} x seed {SEEDS}; nboot {NBOOT} each. ALL reported.")
    log(f"# REPORTED, not tuned: panel [B136, U56], cost {COSTS} bps, window [FULL, OOS].")
    log(f"# warm-up {WARMUP}; IS <= {IS_END}; OOS >= {OOS_START}.")

    px136 = load_universe(broad=True).dropna(how="all").ffill()
    px56 = load_universe().dropna(how="all").ffill()
    PANELS = [("B136", px136, list(px136.columns)), ("U56", px56, list(px56.columns))]

    STATE = {}
    for pname, px, cols in PANELS:
        st = px.index[WARMUP]
        bk = Book(px, cols)
        r0, t0, gs, nref = bk.run(CELL["target"], CELL["h"])
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        lw = rules_v2_weights(px[cols], 0.03, 0.75).reindex(columns=px.columns).fillna(0.0)
        lb = engine_backtest(px, lw, cost_bps=0.0, freq="W")
        lr, lt = lb["returns"].loc[st:], lb["turnover"].loc[st:]
        STATE[pname] = dict(px=px, cols=cols, bk=bk, st=st, r0=r0.loc[st:], t0=t0.loc[st:],
                            spy=spy, lr=lr, lt=lt, gs=gs.loc[st:], nref=nref)
        rb = net(r0.loc[st:], t0.loc[st:], COST0)
        L = legs_of(rb, spy)
        ms = mets(spy)
        log(f"\n## {pname}: {len(cols)} names, book window {st.date()} -> {px.index[-1].date()} "
            f"({len(rb)} days, {len(rb)/252:.1f}y), turnover {t0.loc[st:].sum()/(len(rb)/252):.2f}/yr, "
            f"{nref/(len(rb)/252):.1f} refreshes/yr, mean gross {gs.loc[st:].mean():.3f}")
        log(f"   BOOK  {L['CAGR']:.2%} / {L['Sharpe']:.4f} / {L['MaxDD']:.2%}  halves "
            f"{L['H1']:.4f} / {L['H2']:.4f}   OOS {L['oCAGR']:.2%} / {L['oSharpe']:.4f} / {L['oMaxDD']:.2%}")
        log(f"   SPY   {ms['CAGR']:.2%} / {ms['Sharpe']:.4f} / {ms['MaxDD']:.2%}  "
            f"-> CAGR floor {CAGR_FLOOR*ms['CAGR']:.2%}, DD cap {DD_CAP*ms['MaxDD']:.2%}")
        log("   LEGS  " + "  ".join(f"{k} {L[k]:+.4f}" for k in LEGS))

    # ------------------------------------------------------------------ GATES
    log("\n## GATES (printed before any new number is read)")
    S = STATE["B136"]
    rb = net(S["r0"], S["t0"], COST0)
    L = legs_of(rb, S["spy"])
    ms = mets(S["spy"])
    g1 = max(abs(L["CAGR"] - PUB["CAGR"]), abs(L["Sharpe"] - PUB["Sharpe"]),
             abs(L["MaxDD"] - PUB["MaxDD"]))
    gate("G1 B136 cell reproduces the standing memo's point 2 (CAGR/Sharpe/MaxDD)",
         f"max|d| {g1:.2e}", "<= 5e-4", g1 <= 5e-4)
    g2 = max(abs(L["H1"] - PUB["H1"]), abs(L["H2"] - PUB["H2"]))
    gate("G2 halves reproduce (1.3171 / 1.1415)", f"max|d| {g2:.2e}", "<= 5e-4", g2 <= 5e-4)
    g3 = max(abs(L["oCAGR"] - PUB["oCAGR"]), abs(L["oSharpe"] - PUB["oSharpe"]))
    gate("G3 memo point 5 OOS reproduces (13.01% / 1.2928)", f"max|d| {g3:.2e}", "<= 5e-4", g3 <= 5e-4)
    g4 = max(abs(ms["CAGR"] - PUB["spy_CAGR"]), abs(ms["Sharpe"] - PUB["spy_Sharpe"]),
             abs(ms["MaxDD"] - PUB["spy_MaxDD"]))
    gate("G4 SPY comparand reproduces (15.12% / 0.8844 / -33.72%)", f"max|d| {g4:.2e}",
         "<= 5e-4", g4 <= 5e-4)
    g5 = max(abs(L[k] - PUB[k.split('_')[0]]) for k in LEGS)
    gate("G5 all five published leg margins reproduce (+.3600/+.3166/+.4191/+.0842/+.0192)",
         f"max|d| {g5:.2e}", "<= 5e-4", g5 <= 5e-4)
    lr10 = net(S["lr"], S["lt"], COST0)
    ml = mets(lr10)
    g6 = max(abs(ml["CAGR"] - 0.0796), abs(ml["Sharpe"] - 1.0972), abs(ml["MaxDD"] + 0.1224))
    gate("G6 live RULES v2 comparand reproduces (7.96% / 1.0972 / -12.24%)", f"max|d| {g6:.2e}",
         "<= 5e-4", g6 <= 5e-4)
    # the bootstrap machinery itself, on a null where the answer is known
    rngc = np.random.default_rng(7)
    xa = pd.Series(rngc.normal(0, 0.01, 3000),
                   index=pd.bdate_range('2009-01-02', periods=3000))
    da = draw_legs(xa, xa, 21, 5, nboot=400)
    gate("G7 paired bootstrap of a series against ITSELF gives exactly zero on every Sharpe leg",
         f"max|d| {np.nanmax(np.abs(np.concatenate([da['L1_H1'], da['L2_H2'], da['L3_OOS']]))):.2e}",
         "== 0", np.nanmax(np.abs(np.concatenate([da["L1_H1"], da["L2_H2"], da["L3_OOS"]]))) == 0.0)
    idxc = block_index(1000, 21, 50, np.random.default_rng(3))
    gate("G8 block index is a proper circular resample (shape, range, contiguity)",
         f"shape {idxc.shape}, max {idxc.max()}, contig {(np.diff(idxc[0][:21]) == 1).all()}",
         "(50,1000), <=999, True",
         idxc.shape == (50, 1000) and idxc.max() <= 999 and bool((np.diff(idxc[0][:21]) == 1).all()))
    npass = sum(g["pass_"] for g in _gates)
    log(f"  -> {npass} of {len(_gates)} gates PASS")

    # ------------------------------------------------------------------ THE GRID
    log("\n## THE GRID — every (panel x B x seed) point, all five legs.  "
        "fail_share = share of draws in which the leg FAILS (margin <= 0).")
    rows = []
    for pname in ("B136", "U56"):
        S = STATE[pname]
        rbk = net(S["r0"], S["t0"], COST0)
        obs = legs_of(rbk, S["spy"])
        obs_oosL5 = mets(rbk.loc[OOS_START:])["CAGR"] - CAGR_FLOOR * mets(S["spy"].loc[OOS_START:])["CAGR"]
        for B in BLOCKS:
            for sd in SEEDS:
                D = draw_legs(rbk, S["spy"], B, sd)
                joint = np.ones(NBOOT, bool)
                for k in LEGS:
                    joint &= (D[k] > 0)
                for k in LEGS:
                    br = boot_row(obs[k], D[k])
                    rows.append(dict(panel=pname, B=B, seed=sd, leg=k, window="FULL",
                                     obs=obs[k], **br, joint4b=float(joint.mean())))
                br = boot_row(obs_oosL5, D["_oosL5"])
                rows.append(dict(panel=pname, B=B, seed=sd, leg="L5_CAGR", window="OOS",
                                 obs=obs_oosL5, **br, joint4b=np.nan))
    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)

    for pname in ("B136", "U56"):
        log(f"\n### {pname}  (obs = the published point estimate; t = obs / SE)")
        sub = G[(G.panel == pname) & (G.window == "FULL")]
        log(f"{'B':>5} {'seed':>5} | " + " | ".join(f"{k:>26}" for k in LEGS) + " | joint4b")
        for B in BLOCKS:
            for sd in SEEDS:
                r = sub[(sub.B == B) & (sub.seed == sd)].set_index("leg")
                cells = " | ".join(
                    f"{r.loc[k,'obs']:+.4f} SE{r.loc[k,'SE']:.4f} t{r.loc[k,'t']:+6.2f}" for k in LEGS)
                log(f"{B:>5} {sd:>5} | {cells} | {r.loc['L5_CAGR','joint4b']:.3f}")
        log(f"{'':>5} {'':>5} |  fail_share (draws in which the leg FAILS):")
        for B in BLOCKS:
            r = sub[(sub.B == B)].groupby("leg").fail_share.mean()
            log(f"{B:>5} {'mean':>5} | " + " | ".join(f"{k}={r[k]:.3f}" for k in LEGS))

    # ------------------------------------------------------------------ THE HEADLINE
    log("\n## HEADLINE — the CAGR-floor margin's error bar (B136, the standing cell, 10 bps)")
    h = G[(G.panel == "B136") & (G.leg == "L5_CAGR") & (G.window == "FULL")]
    obs5 = float(h.obs.iloc[0])
    log(f"  observed margin  {obs5:+.4f}  ({obs5*100:+.2f} pp) — the memo's caveat-7 number")
    log(f"  SE across the grid: min {h.SE.min():.4f} ({h.SE.min()*100:.2f} pp), "
        f"median {h.SE.median():.4f} ({h.SE.median()*100:.2f} pp), max {h.SE.max():.4f} "
        f"({h.SE.max()*100:.2f} pp)")
    log(f"  bootstrap t:        min {h.t.min():+.2f}, median {h.t.median():+.2f}, max {h.t.max():+.2f}")
    log(f"  two-sided p:        min {h.p2.min():.4f}, median {h.p2.median():.4f}, max {h.p2.max():.4f}")
    log(f"  fail_share (margin <= 0): min {h.fail_share.min():.3f}, median "
        f"{h.fail_share.median():.3f}, max {h.fail_share.max():.3f}")
    log(f"  95% percentile band at the longest block (B=126): "
        f"[{h[h.B==126].lo.mean():+.4f}, {h[h.B==126].hi.mean():+.4f}]")
    seedspread = h.groupby("B").SE.agg(lambda s: s.max() - s.min())
    log(f"  MONTE-CARLO share: max SE spread ACROSS SEEDS at a fixed B = "
        f"{seedspread.max():.5f} ({seedspread.max()*100:.3f} pp) — vs an SE of "
        f"{h.SE.median():.4f}; so the SE is a TAPE fact, not a draw-count fact.")
    hj = h.joint4b
    log(f"  JOINT five-leg 4b pass rate across draws: min {hj.min():.3f}, median "
        f"{hj.median():.3f}, max {hj.max():.3f}")

    # ------------------------------------------------------------------ COST LADDER (reported)
    log("\n## THE MARGIN ACROSS THE COST LADDER (reported, not tuned; B=21, seed=11)")
    crows = []
    for pname in ("B136", "U56"):
        S = STATE[pname]
        for c in COSTS:
            rbk = net(S["r0"], S["t0"], c)
            o = legs_of(rbk, S["spy"])
            D = draw_legs(rbk, S["spy"], 21, 11)
            br = boot_row(o["L5_CAGR"], D["L5_CAGR"])
            joint = np.ones(NBOOT, bool)
            for k in LEGS:
                joint &= (D[k] > 0)
            crows.append(dict(panel=pname, cost_bps=c, margin=o["L5_CAGR"], SE=br["SE"],
                              t=br["t"], fail_share=br["fail_share"], joint4b=float(joint.mean()),
                              CAGR=o["CAGR"], Sharpe=o["Sharpe"], MaxDD=o["MaxDD"]))
            log(f"   {pname:5s} {c:3d} bps  margin {o['L5_CAGR']*100:+6.2f} pp  SE "
                f"{br['SE']*100:5.2f} pp  t {br['t']:+6.2f}  fail_share {br['fail_share']:.3f}  "
                f"joint4b {joint.mean():.3f}  (book {o['CAGR']:.2%}/{o['Sharpe']:.4f}/{o['MaxDD']:.2%})")
    pd.DataFrame(crows).to_csv(f"{OUT}.costladder.csv", index=False)

    # ------------------------------------------------------------------ RULE 8
    log("\n## RULE 8 — (t, h) chosen on 2009-2016 ONLY, 2017-2026 read exactly ONCE, then the "
        "PICK's OOS CAGR-floor margin bootstrapped.  Every grid point reported.")
    wf = []
    for pname in ("B136", "U56"):
        S = STATE[pname]
        bk, st, spy = S["bk"], S["st"], S["spy"]
        spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
        sis, soos = mets(spy_is), mets(spy_oos)
        sis_h1, sis_h2 = halves(spy_is)
        for tg in TARGETS:
            for hh in THRESH:
                r0, t0, gs, nref = bk.run(tg, hh)
                rbk = net(r0.loc[st:], t0.loc[st:], COST0)
                ris, roos = rbk.loc[:IS_END], rbk.loc[OOS_START:]
                mi, mo = mets(ris), mets(roos)
                ih1, ih2 = halves(ris)
                # IS-only 4b legs (no post-2016 information anywhere in the chooser)
                sl = dict(L1=ih1 - sis_h1, L2=ih2 - sis_h2,
                          L4=mi["MaxDD"] - DD_CAP * sis["MaxDD"],
                          L5=mi["CAGR"] - CAGR_FLOOR * sis["CAGR"])
                wf.append(dict(panel=pname, target=tg, h=hh,
                               is_CAGR=mi["CAGR"], is_Sharpe=mi["Sharpe"], is_MaxDD=mi["MaxDD"],
                               is_minslack=min(sl.values()), **{f"is_{k}": v for k, v in sl.items()},
                               oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                               oos_L5=mo["CAGR"] - CAGR_FLOOR * soos["CAGR"],
                               oos_L3=mo["Sharpe"] - soos["Sharpe"],
                               oos_L4=mo["MaxDD"] - DD_CAP * soos["MaxDD"]))
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    for pname in ("B136", "U56"):
        sub = W[W.panel == pname]
        log(f"\n### {pname} — all {len(sub)} (t, h) cells: IS min-slack chooser, OOS read once")
        log(f"{'t':>6} " + " ".join(f"{h:>7}" for h in THRESH) + "   <- h;  cell = OOS L5 margin (pp)")
        for tg in TARGETS:
            r = sub[sub.target == tg].set_index("h")
            log(f"{tg:>6} " + " ".join(f"{r.loc[h,'oos_L5']*100:+7.2f}" for h in THRESH))
        pick = sub.loc[sub.is_minslack.idxmax()]
        log(f"  IS PICK (argmax min IS 4b-leg slack, 2009-2016 only): t={pick.target}, h={pick.h} "
            f"[IS min-slack {pick.is_minslack:+.4f}]")
        log(f"  OOS read ONCE: {pick.oos_CAGR:.2%} / {pick.oos_Sharpe:.4f} / {pick.oos_MaxDD:.2%}"
            f"   vs SPY {mets(STATE[pname]['spy'].loc[OOS_START:])['CAGR']:.2%} / "
            f"{mets(STATE[pname]['spy'].loc[OOS_START:])['Sharpe']:.4f} / "
            f"{mets(STATE[pname]['spy'].loc[OOS_START:])['MaxDD']:.2%}"
            f"   vs live v2 {mets(net(STATE[pname]['lr'],STATE[pname]['lt'],COST0).loc[OOS_START:])['CAGR']:.2%} / "
            f"{mets(net(STATE[pname]['lr'],STATE[pname]['lt'],COST0).loc[OOS_START:])['Sharpe']:.4f} / "
            f"{mets(net(STATE[pname]['lr'],STATE[pname]['lt'],COST0).loc[OOS_START:])['MaxDD']:.2%}")
        r0, t0, _, _ = STATE[pname]["bk"].run(float(pick.target), float(pick.h))
        rpk = net(r0.loc[STATE[pname]["st"]:], t0.loc[STATE[pname]["st"]:], COST0)
        prow = []
        for B in BLOCKS:
            for sd in SEEDS:
                D = draw_legs(rpk, STATE[pname]["spy"], B, sd)
                br = boot_row(float(pick.oos_L5), D["_oosL5"])
                prow.append(dict(panel=pname, target=float(pick.target), h=float(pick.h),
                                 B=B, seed=sd, window="OOS", **br))
        P = pd.DataFrame(prow)
        log(f"  OOS CAGR-floor margin {pick.oos_L5*100:+.2f} pp; bootstrap SE "
            f"{P.SE.min()*100:.2f}-{P.SE.max()*100:.2f} pp, t {P.t.min():+.2f} to {P.t.max():+.2f}, "
            f"fail_share {P.fail_share.min():.3f}-{P.fail_share.max():.3f}")
        P.to_csv(f"{OUT}.pick_{pname}.csv", index=False)

    # ------------------------------------------------------------------ BOTH KEEP PATHS
    log("\n## BOTH KEEP PATHS, with the error bar attached (10 bps, t+1)")
    kp = []
    for pname in ("B136", "U56"):
        S = STATE[pname]
        rbk = net(S["r0"], S["t0"], COST0)
        o = legs_of(rbk, S["spy"])
        lrc = net(S["lr"], S["lt"], COST0)
        mlv = mets(lrc)
        lh1, lh2 = halves(lrc)
        p4a = (o["H1"] > lh1) and (o["H2"] > lh2) and (o["MaxDD"] >= mlv["MaxDD"])
        p4b = all(o[k] > 0 for k in LEGS)
        D = draw_legs(rbk, S["spy"], 21, 11)
        joint = np.ones(NBOOT, bool)
        for k in LEGS:
            joint &= (D[k] > 0)
        kp.append(dict(panel=pname, path4a=p4a, path4b=p4b, joint4b_draws=float(joint.mean()),
                       L5=o["L5_CAGR"], L5_fail_share=boot_row(o["L5_CAGR"], D["L5_CAGR"])["fail_share"]))
        log(f"   {pname:5s} 4a {'PASS' if p4a else 'FAIL'} (book halves {o['H1']:.4f}/{o['H2']:.4f} "
            f"vs live {lh1:.4f}/{lh2:.4f}; MaxDD {o['MaxDD']:.2%} vs {mlv['MaxDD']:.2%})   "
            f"4b {'PASS' if p4b else 'FAIL'} at the point estimate, but only "
            f"{joint.mean():.1%} of paired block-bootstrap draws hold all five legs")
    pd.DataFrame(kp).to_csv(f"{OUT}.keeppaths.csv", index=False)

    pd.DataFrame(_gates).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.console.txt").write_text("\n".join(_log) + "\n")
    log(f"\nwrote {OUT}.grid.csv / .walkforward.csv / .costladder.csv / .keeppaths.csv / "
        f".gates.csv / .console.txt")


if __name__ == "__main__":
    main()
