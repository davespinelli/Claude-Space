#!/usr/bin/env python3
"""Idea 2071 (lane cloud, 2026-09-21) — CAN THE VOL TARGET `t` BE SET WITHOUT READING THE
IS WINDOW, AND DOES ANY SELF-SCALING TARGET REACH THE 4b BAND?

THE QUESTION.  The standing KEEP-4b candidate (VOLTGT-DRIFT on B136, `t = 0.10`, `h = 0.08`,
trade W, 10 bps, t+1 — memo `research/backtests/2026-09-20_voltgt-drift-b136_KEEP4b_MEMO.md`)
sets its gross scalar from a FIXED annualised vol target.  That number came off an IS ladder.
Idea 2026 removed the drift THRESHOLD's dependence on an IS ladder but left `t` INHERITED, and
idea 1771 showed the 4b pass is a two-sided squeeze in `t` (robust band {0.10, 0.12}) — i.e. a
rule that lands one rung off lands outside.  This run prices THREE targets that spend NO
in-sample statistic and reads them against the whole fixed-`t` ladder:

    FIXED(t)      t is a constant                          (the INCUMBENT comparand; needs a chooser)
    SELFQ(q)      t = the q-quantile of the panel's OWN trailing 3-year realised sigma
    MEDMULT(m)    t = m x the EXPANDING (point-in-time) median of the panel's own sigma
    CASHSHARE(c)  no vol target at all: the deployed gross is set directly at g = 1 - c

SELFQ, MEDMULT and CASHSHARE are computed from data available at close `t` only, so each is a
COMPLETE, DEPLOYABLE rule on day one of the sample: no 2009-2016 window is read anywhere.

THE TWO TUNED PARAMETERS (PROTOCOL rule 4; every grid point reported, none hidden):
    P1  the TARGET-RULE FAMILY   {FIXED, SELFQ, MEDMULT, CASHSHARE}
    P2  that family's OWN single dial   FIXED t / SELFQ q / MEDMULT m / CASHSHARE c (5 rungs each)
Nothing else is tuned.  INHERITED AND PRE-STATED, NOT TUNED: drift threshold `h = 0.08`, trade
cadence W, gross cap 1.00, sigma convention (20-day realised vol of the unlevered equal-weight
panel portfolio, no lag), warm-up 260, t+1 execution.
REPORTED, NOT TUNED: panel {B136, U56, SMALL665}, cost {0, 10, 25, 50} bps, window {FULL, IS, OOS}.

THE ZERO-CHOOSER ARM, PRE-STATED BEFORE ANY NUMBER IS READ.  Each self-scaling family has one
a-priori neutral rung, fixed by its own definition and not by a result:
    SELFQ q = 0.50      the median of the panel's own trailing vol distribution (gross centred on 1)
    MEDMULT m = 1.00    the target IS the long-run median sigma (multiple of one)
    CASHSHARE c = 0.25  the live RULES v2 cash share (gross 0.75), inherited from the live book
These three arms are the headline: they involve NO chooser of any kind, so their FULL-sample and
2017-2026 readings are the honest answer to the idea's question.  The per-family rule-8 chooser
(argmax min IS 4b-leg slack on 2009-2016, then OOS read ONCE) is reported beside them as the
comparand — it is what the incumbent procedure would do and it is NOT the zero-IS claim.

PROTOCOL: rule 2 (10 bps headline, t+1 next-day execution, gross <= 1.00, no shorting/leverage);
rule 3 (live RULES v2 AND SPY, via the same machinery as the standing memo); rule 4 (BOTH KEEP
paths at every cell, <= 2 tuned parameters, ALL grid points reported); rule 5 (one idea, one
script, deterministic, standalone); rule 8 (walk-forward: dials chosen on 2009-2016 only,
2017-2026 read exactly once); rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py,
bot.py and baseline.py are NOT modified by this run.

SURVIVORSHIP.  B136 and U56 are CURRENT-constituent lists and SMALL665 is a current screen of
sub-$2B names (tickers with `max_1d_move >= 1.0` in `data/small_meta.csv` dropped first, per the
sprint brief).  Every CAGR / MaxDD LEVEL below is therefore optimistic and both 4b bars are
EASIER than they would be on a point-in-time panel.  What this run measures is a CONTRAST between
target rules on one tape; the contrast is first-order immune to that bias, the levels are not.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-21_target-without-is-window_cloud.py
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

DATE, SLUG, LANE = "2026-09-21", "target-without-is-window", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

# ---------------------------------------------------------------- inherited, NOT tuned
WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SIG_L, SIG_D = 20, 0
SELF_WIN, SELF_MINP = 756, 126      # trailing 3y window for the self-scaling estimators
H_FIXED = 0.08                      # the candidate's drift threshold, pre-stated
T_TRADE = "W"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST0 = 10
COSTS = [0, 10, 25, 50]
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]

# ---------------------------------------------------------------- the two tuned parameters
FAMILIES = {
    "FIXED":     [0.08, 0.10, 0.12, 0.16, 0.20],
    "SELFQ":     [0.10, 0.20, 0.30, 0.40, 0.50],
    "MEDMULT":   [0.50, 0.70, 0.85, 1.00, 1.20],
    "CASHSHARE": [0.10, 0.20, 0.25, 0.30, 0.40],
}
PRESTATED = {"SELFQ": 0.50, "MEDMULT": 1.00, "CASHSHARE": 0.25}   # the zero-chooser arms
CELL = dict(family="FIXED", dial=0.10)                            # the standing KEEP-4b cell

PUB = dict(CAGR=0.1251, Sharpe=1.2286, MaxDD=-0.1181, H1=1.3171, H2=1.1415,
           oCAGR=0.1301, oSharpe=1.2928, spy_CAGR=0.1512, spy_Sharpe=0.8844, spy_MaxDD=-0.3372)

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
    """Equal-weight book, gross scalar refreshed on a DRIFT trigger, traded on mT.  Verbatim
    from idea 1799/2034 — only the g0 SERIES differs between target rules."""
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
        m = np.asarray(rebalance_mask(px.index, T_TRADE).values, bool)
        self.mT = np.concatenate([[False], m[:-1]])

    def target_series(self, family, dial):
        """The TARGET vol as a series, or None for CASHSHARE (which sets gross directly).
        Every estimator is POINT-IN-TIME: it reads closes up to `t` and nothing after."""
        sig = self.SIG
        if family == "FIXED":
            return pd.Series(float(dial), index=sig.index).where(sig.notna())
        if family == "SELFQ":
            return sig.rolling(SELF_WIN, min_periods=SELF_MINP).quantile(float(dial))
        if family == "MEDMULT":
            return float(dial) * sig.expanding(min_periods=SELF_MINP).median()
        if family == "CASHSHARE":
            return None
        raise ValueError(family)

    def g_of(self, family, dial):
        sig = self.SIG
        if family == "CASHSHARE":
            g = pd.Series(1.0 - float(dial), index=sig.index).where(sig.notna())
        else:
            g = (self.target_series(family, dial) / sig.replace(0, np.nan)).clip(upper=1.0)
        g = g.fillna(0.0).values
        return np.concatenate([[0.0], g[:-1]])          # decided at close t, applied at t+1

    def run(self, family, dial, h=H_FIXED):
        r, t, gs, nref = bt_drift(self.R, self.W, self.g_of(family, dial), self.mT, h)
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


def legs_4b(rb, spy):
    """The five 4b leg MARGINS (all positive == PASS), exactly as the standing memo states them."""
    mb, ms = mets(rb), mets(spy)
    bh1, bh2 = halves(rb)
    sh1, sh2 = halves(spy)
    ob, os_ = mets(rb.loc[OOS_START:]), mets(spy.loc[OOS_START:])
    return dict(L1_H1=bh1 - sh1, L2_H2=bh2 - sh2, L3_OOS=ob["Sharpe"] - os_["Sharpe"],
                L4_DD=mb["MaxDD"] - DD_CAP * ms["MaxDD"],
                L5_CAGR=mb["CAGR"] - CAGR_FLOOR * ms["CAGR"],
                CAGR=mb["CAGR"], Sharpe=mb["Sharpe"], MaxDD=mb["MaxDD"], H1=bh1, H2=bh2,
                oCAGR=ob["CAGR"], oSharpe=ob["Sharpe"], oMaxDD=ob["MaxDD"])


def verdict_4b(L):
    binding = [k for k in LEGS if not (L[k] > 0)]
    return (len(binding) == 0), (",".join(binding) if binding else "none")


def verdict_4a(rb, lb):
    """PATH 4a: Sharpe > live RULES v2 in BOTH halves AND MaxDD no worse than the live rules."""
    bh1, bh2 = halves(rb)
    lh1, lh2 = halves(lb)
    mb, ml = mets(rb), mets(lb)
    fails = []
    if not bh1 > lh1: fails.append("H1")
    if not bh2 > lh2: fails.append("H2")
    if not mb["MaxDD"] >= ml["MaxDD"]: fails.append("MaxDD")
    return (len(fails) == 0), (",".join(fails) if fails else "none")


# ---------------------------------------------------------------- panels
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c not in bad]
    px = px[keep].dropna(how="all").ffill()
    cols = [c for c in px.columns if c != "SPY"]     # SPY is a BENCHMARK on this panel, not a holding
    return px, cols, len(bad & set(load_universe(small=True).columns))


def main():
    log(f"# Idea 2071 (lane {LANE}, {DATE}) — CAN THE TARGET `t` BE SET WITHOUT THE IS WINDOW?")
    log(f"# BOOK (inherited, NOT tuned): VOLTGT-DRIFT, h={H_FIXED}, trade {T_TRADE}, {COST0} bps, "
        f"t+1, gross <= 1.00, sigma (L={SIG_L}, d={SIG_D}), warm-up {WARMUP}.")
    log(f"# TUNED (2): TARGET-RULE FAMILY x that family's own dial. ALL {sum(len(v) for v in FAMILIES.values())} "
        f"rungs reported per panel:")
    for f, d in FAMILIES.items():
        log(f"#     {f:<10} {d}")
    log(f"# ZERO-CHOOSER ARMS, PRE-STATED: {PRESTATED}  (no 2009-2016 statistic anywhere in them)")
    log(f"# REPORTED, not tuned: panel [B136, U56, SMALL665], cost {COSTS} bps, window [FULL, IS, OOS].")
    log(f"# Self-scaling estimators: trailing {SELF_WIN}d window, min_periods {SELF_MINP} "
        f"(live before day {WARMUP}, so no rule carries a cash stub inside the scoring window).")

    px136 = load_universe(broad=True).dropna(how="all").ffill()
    px56 = load_universe().dropna(how="all").ffill()
    pxs, cols_s, n_dropped = small_panel()
    PANELS = [("B136", px136, list(px136.columns)),
              ("U56", px56, list(px56.columns)),
              (f"SMALL{len(cols_s)}", pxs, cols_s)]
    log(f"# SMALL panel: {n_dropped} tickers with max_1d_move >= 1.0 dropped per the sprint brief; "
        f"{len(cols_s)} held names + SPY as benchmark only.")

    STATE = {}
    for pname, px, cols in PANELS:
        st = px.index[WARMUP]
        bk = Book(px, cols)
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        lw = rules_v2_weights(px[cols], 0.03, 0.75).reindex(columns=px.columns).fillna(0.0)
        lb = engine_backtest(px, lw, cost_bps=0.0, freq="W")
        STATE[pname] = dict(px=px, cols=cols, bk=bk, st=st, spy=spy,
                            lr=lb["returns"].loc[st:], lt=lb["turnover"].loc[st:])
        ms, mo = mets(spy), mets(spy.loc[OOS_START:])
        log(f"\n## {pname}: {len(cols)} held names, window {st.date()} -> {px.index[-1].date()} "
            f"({len(spy)} days, {len(spy)/252:.1f}y)")
        log(f"   SPY  {ms['CAGR']:.2%} / {ms['Sharpe']:.4f} / {ms['MaxDD']:.2%}  -> 4b bars: "
            f"CAGR floor {CAGR_FLOOR*ms['CAGR']:.2%}, DD cap {DD_CAP*ms['MaxDD']:.2%}; "
            f"OOS SPY {mo['CAGR']:.2%} / {mo['Sharpe']:.4f}")
        lbn = net(STATE[pname]["lr"], STATE[pname]["lt"], COST0)
        ml = mets(lbn)
        log(f"   live RULES v2  {ml['CAGR']:.2%} / {ml['Sharpe']:.4f} / {ml['MaxDD']:.2%}  halves "
            f"{halves(lbn)[0]:.4f} / {halves(lbn)[1]:.4f}")
        # first day each estimator is live (an honesty check on the warm-up claim)
        for f in ("SELFQ", "MEDMULT"):
            ts = bk.target_series(f, FAMILIES[f][-1]).dropna()
            log(f"   {f} estimator live from {ts.index[0].date()} "
                f"(scoring window opens {st.date()})")

    # ------------------------------------------------------------------ GATES
    log("\n## GATES (printed before any new number is read)")
    S = STATE["B136"]
    r0, t0, gs, nref = S["bk"].run(CELL["family"], CELL["dial"])
    rb = net(r0.loc[S["st"]:], t0.loc[S["st"]:], COST0)
    L = legs_4b(rb, S["spy"])
    ms = mets(S["spy"])
    g1 = max(abs(L["CAGR"] - PUB["CAGR"]), abs(L["Sharpe"] - PUB["Sharpe"]), abs(L["MaxDD"] - PUB["MaxDD"]))
    gate("G1 B136 FIXED t=0.10 reproduces the standing memo point 2", f"max|d| {g1:.2e}", "<= 5e-4", g1 <= 5e-4)
    g2 = max(abs(L["H1"] - PUB["H1"]), abs(L["H2"] - PUB["H2"]))
    gate("G2 halves reproduce (1.3171 / 1.1415)", f"max|d| {g2:.2e}", "<= 5e-4", g2 <= 5e-4)
    g3 = max(abs(L["oCAGR"] - PUB["oCAGR"]), abs(L["oSharpe"] - PUB["oSharpe"]))
    gate("G3 memo point 5 OOS reproduces (13.01% / 1.2928)", f"max|d| {g3:.2e}", "<= 5e-4", g3 <= 5e-4)
    g4 = max(abs(ms["CAGR"] - PUB["spy_CAGR"]), abs(ms["Sharpe"] - PUB["spy_Sharpe"]),
             abs(ms["MaxDD"] - PUB["spy_MaxDD"]))
    gate("G4 SPY comparand reproduces (15.12% / 0.8844 / -33.72%)", f"max|d| {g4:.2e}", "<= 5e-4", g4 <= 5e-4)
    ok4b, _ = verdict_4b(L)
    gate("G5 the standing cell still reads 4b PASS on all five legs", ok4b, "True", ok4b)
    # the self-scaling estimators must contain NO future information: a spot check by construction
    bkB = S["bk"]
    tq = bkB.target_series("SELFQ", 0.50)
    half = bkB.SIG.index[len(bkB.SIG) // 2]
    tq_trunc = panel_sigma(S["px"].loc[:half], S["cols"]).rolling(SELF_WIN, min_periods=SELF_MINP).quantile(0.50)
    d6 = float((tq.loc[:half].dropna() - tq_trunc.reindex(tq.loc[:half].dropna().index)).abs().max())
    gate("G6 SELFQ target on the truncated tape equals the full-tape target (no look-ahead)",
         f"max|d| {d6:.2e}", "<= 1e-12", d6 <= 1e-12)

    # ------------------------------------------------------------------ FULL GRID
    log(f"\n## GRID — every (panel x family x dial x cost) cell, BOTH KEEP paths.  "
        f"{len(PANELS)} x {sum(len(v) for v in FAMILIES.values())} x {len(COSTS)} = "
        f"{len(PANELS)*sum(len(v) for v in FAMILIES.values())*len(COSTS)} rows.")
    rows = []
    BOOKS = {}
    for pname, _, _ in PANELS:
        S = STATE[pname]
        for fam, dials in FAMILIES.items():
            for dl in dials:
                r0, t0, gs, nref = S["bk"].run(fam, dl)
                r0, t0, gs = r0.loc[S["st"]:], t0.loc[S["st"]:], gs.loc[S["st"]:]
                BOOKS[(pname, fam, dl)] = (r0, t0)
                yrs = len(r0) / 252.0
                for c in COSTS:
                    rbk = net(r0, t0, c)
                    lbn = net(S["lr"], S["lt"], c)
                    Lg = legs_4b(rbk, S["spy"])
                    p4b, bind4b = verdict_4b(Lg)
                    p4a, bind4a = verdict_4a(rbk, lbn)
                    rows.append(dict(panel=pname, family=fam, dial=dl, cost_bps=c,
                                     zero_IS=(fam != "FIXED"),
                                     prestated=bool(PRESTATED.get(fam, None) == dl),
                                     CAGR=Lg["CAGR"], Sharpe=Lg["Sharpe"], MaxDD=Lg["MaxDD"],
                                     H1=Lg["H1"], H2=Lg["H2"], oCAGR=Lg["oCAGR"],
                                     oSharpe=Lg["oSharpe"], oMaxDD=Lg["oMaxDD"],
                                     **{k: Lg[k] for k in LEGS},
                                     keep4b=p4b, binding4b=bind4b, keep4a=p4a, binding4a=bind4a,
                                     turnover_yr=float(t0.sum() / yrs),
                                     refresh_yr=float(nref / yrs), mean_gross=float(gs.mean())))
    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)

    for pname, _, _ in PANELS:
        sub = G[(G.panel == pname) & (G.cost_bps == COST0)]
        log(f"\n### {pname} @ {COST0} bps — full sample, all {len(sub)} cells")
        log(f"{'family':<10}{'dial':>6}  {'CAGR':>7} {'Sharpe':>7} {'MaxDD':>8} {'H1':>7} {'H2':>7} "
            f"{'OOSShp':>7} {'trn/yr':>7} {'gross':>6}  {'4b':>4} {'4a':>4}  binding4b")
        for fam in FAMILIES:
            for _, r in sub[sub.family == fam].iterrows():
                star = " *" if r.prestated else "  "
                log(f"{fam:<10}{r.dial:>6.2f}{star}{r.CAGR:>7.2%} {r.Sharpe:>7.4f} {r.MaxDD:>8.2%} "
                    f"{r.H1:>7.4f} {r.H2:>7.4f} {r.oSharpe:>7.4f} {r.turnover_yr:>7.2f} "
                    f"{r.mean_gross:>6.3f}  {'PASS' if r.keep4b else 'fail':>4} "
                    f"{'PASS' if r.keep4a else 'fail':>4}  {r.binding4b}")
        log("   (* = the PRE-STATED zero-chooser rung)")

    log("\n### 4b / 4a PASS COUNTS by family x cost (all panels pooled, full sample)")
    log(f"{'family':<10}" + "".join(f"{'4b@'+str(c):>10}" for c in COSTS)
        + "".join(f"{'4a@'+str(c):>10}" for c in COSTS))
    for fam in FAMILIES:
        n = len(FAMILIES[fam]) * len(PANELS)
        log(f"{fam:<10}"
            + "".join(f"{str(int(G[(G.family==fam)&(G.cost_bps==c)].keep4b.sum()))+'/'+str(n):>10}" for c in COSTS)
            + "".join(f"{str(int(G[(G.family==fam)&(G.cost_bps==c)].keep4a.sum()))+'/'+str(n):>10}" for c in COSTS))

    # ------------------------------------------------------------------ THE ZERO-CHOOSER ARMS
    log("\n## THE HEADLINE — the THREE PRE-STATED ZERO-CHOOSER ARMS, which read NO 2009-2016 "
        "statistic at all, beside the standing IS-chosen cell.")
    pre = []
    for pname, _, _ in PANELS:
        S = STATE[pname]
        arms = [("FIXED", CELL["dial"], "IS-CHOSEN (incumbent)")] + \
               [(f, d, "ZERO-IS (pre-stated)") for f, d in PRESTATED.items()]
        for fam, dl, kind in arms:
            r0, t0 = BOOKS[(pname, fam, dl)]
            for c in COSTS:
                rbk = net(r0, t0, c)
                lbn = net(S["lr"], S["lt"], c)
                Lg = legs_4b(rbk, S["spy"])
                p4b, b4b = verdict_4b(Lg)
                p4a, b4a = verdict_4a(rbk, lbn)
                oo = mets(rbk.loc[OOS_START:])
                pre.append(dict(panel=pname, kind=kind, family=fam, dial=dl, cost_bps=c,
                                CAGR=Lg["CAGR"], Sharpe=Lg["Sharpe"], MaxDD=Lg["MaxDD"],
                                H1=Lg["H1"], H2=Lg["H2"],
                                oCAGR=oo["CAGR"], oSharpe=oo["Sharpe"], oMaxDD=oo["MaxDD"],
                                **{k: Lg[k] for k in LEGS},
                                keep4b=p4b, binding4b=b4b, keep4a=p4a, binding4a=b4a))
    P = pd.DataFrame(pre)
    P.to_csv(f"{OUT}.prestated.csv", index=False)
    for pname, _, _ in PANELS:
        log(f"\n### {pname}")
        log(f"{'arm':<26}{'cost':>5} {'CAGR':>7} {'Sharpe':>7} {'MaxDD':>8} "
            f"{'OOS CAGR':>9} {'OOSShp':>7}  {'4b':>4} {'4a':>4}  binding4b")
        for _, r in P[P.panel == pname].iterrows():
            nm = f"{r.family}({r.dial:g}) {'[0-IS]' if r.kind.startswith('ZERO') else '[IS]'}"
            log(f"{nm:<26}{r.cost_bps:>5} {r.CAGR:>7.2%} {r.Sharpe:>7.4f} {r.MaxDD:>8.2%} "
                f"{r.oCAGR:>9.2%} {r.oSharpe:>7.4f}  {'PASS' if r.keep4b else 'fail':>4} "
                f"{'PASS' if r.keep4a else 'fail':>4}  {r.binding4b}")

    # ------------------------------------------------------------------ RULE 8
    log("\n## RULE 8 WALK-FORWARD — each family's dial chosen on 2009-2016 ONLY (argmax min IS "
        "4b-leg slack), 2017-2026 read exactly ONCE.  Every grid point reported.")
    wf = []
    for pname, _, _ in PANELS:
        S = STATE[pname]
        spy_is, spy_oos = S["spy"].loc[:IS_END], S["spy"].loc[OOS_START:]
        sis, soos = mets(spy_is), mets(spy_oos)
        sis_h1, sis_h2 = halves(spy_is)
        soos_h1, soos_h2 = halves(spy_oos)
        for fam, dials in FAMILIES.items():
            for dl in dials:
                r0, t0 = BOOKS[(pname, fam, dl)]
                rbk = net(r0, t0, COST0)
                lbn = net(S["lr"], S["lt"], COST0)
                ris, roos = rbk.loc[:IS_END], rbk.loc[OOS_START:]
                mi, mo = mets(ris), mets(roos)
                ih1, ih2 = halves(ris)
                oh1, oh2 = halves(roos)
                sl = dict(L1=ih1 - sis_h1, L2=ih2 - sis_h2,
                          L4=mi["MaxDD"] - DD_CAP * sis["MaxDD"],
                          L5=mi["CAGR"] - CAGR_FLOOR * sis["CAGR"])
                # OOS 4b judged on the OOS window alone (halves of the OOS window + its own bars)
                oos_ok = (oh1 > soos_h1 and oh2 > soos_h2
                          and mo["Sharpe"] > soos["Sharpe"]
                          and mo["MaxDD"] >= DD_CAP * soos["MaxDD"]
                          and mo["CAGR"] >= CAGR_FLOOR * soos["CAGR"])
                lo = mets(lbn.loc[OOS_START:])
                lh1, lh2 = halves(lbn.loc[OOS_START:])
                oos_4a = (oh1 > lh1 and oh2 > lh2 and mo["MaxDD"] >= lo["MaxDD"])
                wf.append(dict(panel=pname, family=fam, dial=dl, zero_IS=(fam != "FIXED"),
                               prestated=bool(PRESTATED.get(fam, None) == dl),
                               is_CAGR=mi["CAGR"], is_Sharpe=mi["Sharpe"], is_MaxDD=mi["MaxDD"],
                               is_minslack=min(sl.values()),
                               **{f"is_{k}": v for k, v in sl.items()},
                               oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                               oos_H1=oh1, oos_H2=oh2,
                               oos_L3=mo["Sharpe"] - soos["Sharpe"],
                               oos_L4=mo["MaxDD"] - DD_CAP * soos["MaxDD"],
                               oos_L5=mo["CAGR"] - CAGR_FLOOR * soos["CAGR"],
                               oos_keep4b=oos_ok, oos_keep4a=oos_4a))
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    for pname, _, _ in PANELS:
        S = STATE[pname]
        soos = mets(S["spy"].loc[OOS_START:])
        lo = mets(net(S["lr"], S["lt"], COST0).loc[OOS_START:])
        sub = W[W.panel == pname]
        log(f"\n### {pname} — OOS 2017-2026: SPY {soos['CAGR']:.2%} / {soos['Sharpe']:.4f} / "
            f"{soos['MaxDD']:.2%};  live RULES v2 {lo['CAGR']:.2%} / {lo['Sharpe']:.4f} / {lo['MaxDD']:.2%}")
        log(f"{'family':<10}{'dial':>6} {'IS slack':>9}  {'OOS CAGR':>9} {'OOSShp':>7} {'OOS DD':>8} "
            f"{'4bOOS':>6} {'4aOOS':>6}")
        for fam in FAMILIES:
            s = sub[sub.family == fam]
            for _, r in s.iterrows():
                log(f"{fam:<10}{r.dial:>6.2f} {r.is_minslack:>+9.4f}  {r.oos_CAGR:>9.2%} "
                    f"{r.oos_Sharpe:>7.4f} {r.oos_MaxDD:>8.2%} "
                    f"{'PASS' if r.oos_keep4b else 'fail':>6} {'PASS' if r.oos_keep4a else 'fail':>6}")
            pick = s.loc[s.is_minslack.idxmax()]
            pre_row = s[s.prestated]
            extra = ""
            if len(pre_row):
                pr = pre_row.iloc[0]
                extra = (f"   | PRE-STATED dial {pr.dial:g}: OOS {pr.oos_CAGR:.2%} / "
                         f"{pr.oos_Sharpe:.4f} / {pr.oos_MaxDD:.2%}, 4b "
                         f"{'PASS' if pr.oos_keep4b else 'fail'}"
                         f"   [chooser agrees: {bool(pr.dial == pick.dial)}]")
            log(f"  -> IS PICK {fam} dial={pick.dial:g} (min IS slack {pick.is_minslack:+.4f}); "
                f"OOS read ONCE {pick.oos_CAGR:.2%} / {pick.oos_Sharpe:.4f} / {pick.oos_MaxDD:.2%}, "
                f"4b {'PASS' if pick.oos_keep4b else 'fail'}, 4a "
                f"{'PASS' if pick.oos_keep4a else 'fail'}{extra}")

    # ------------------------------------------------------------------ SUMMARY
    log("\n## SUMMARY — does ANY zero-IS target reach the 4b band?")
    hl = P[(P.cost_bps == COST0) & (P.kind.str.startswith("ZERO"))]
    detail = ", ".join(f"{r.panel}/{r.family}=" + ("PASS" if r.keep4b else "fail")
                       for _, r in hl.iterrows())
    log(f"  full-sample 4b at {COST0} bps, zero-IS arms: {int(hl.keep4b.sum())} of {len(hl)} ({detail})")
    wz = W[(W.prestated) & (W.zero_IS)]
    log(f"  OOS-window 4b, zero-IS pre-stated arms: {int(wz.oos_keep4b.sum())} of {len(wz)}")
    log(f"  full-sample 4b, whole grid at {COST0} bps: "
        f"{int(G[G.cost_bps==COST0].keep4b.sum())} of {len(G[G.cost_bps==COST0])}; "
        f"4a: {int(G[G.cost_bps==COST0].keep4a.sum())}")
    b = G[(G.cost_bps == COST0) & (~G.keep4b)].binding4b.value_counts()
    log("  binding 4b legs among full-sample failures @ 10 bps: " + ", ".join(f"{k} x{v}" for k, v in b.items()))

    pd.DataFrame(_gates).to_csv(f"{OUT}.gates.csv", index=False)
    log(f"\nGATES {sum(g['pass_'] for g in _gates)}/{len(_gates)} passed.")
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")
    log(f"wrote {OUT}.grid.csv / .prestated.csv / .walkforward.csv / .gates.csv / .log.txt")
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")


if __name__ == "__main__":
    main()
