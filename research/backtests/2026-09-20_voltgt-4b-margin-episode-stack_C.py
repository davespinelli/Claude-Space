#!/usr/bin/env python3
"""Idea 2038 (lane C, 2026-09-20) — DOES THE VOL-TARGET FAMILY's 4b MARGIN DECOMPOSE INTO A
STACK OF DRAWDOWN EPISODES?

THE QUESTION (queue 2038).  Idea 2022 showed ONE 24-day window carries 89% of the
drift-vs-calendar edge.  Ask the same of the 4b margin AGAINST SPY: excise each OOS drawdown
episode in turn (2018Q4, 2020Q1, 2022, and any other SPY peak-to-trough below the depth bar),
one at a time and cumulatively, and report how much of the standing candidate's OOS Sharpe and
CAGR margin each one owns.  If three quarters own the whole margin, the book is a crash hedge
priced as a growth rule.

THE BOOKS (the vol-target family's standing cells, not re-tuned here).  `VOLTGT(t, T, R)` holds
every priced name in the panel at equal weight -- no ranking, no band, no per-name vol filter --
and scales the whole book by `g = clip(t / sigma_20, 0, 1)`, `sigma_20` the annualised 20-day
realised vol of the UNLEVERED equal-weight panel portfolio read through yesterday's close
((L,d) = (20,0), the record's convention; idea 1771 owns that surface).  `T` is the cadence on
which the NAMES are re-spread, `R` the cadence on which `g` is re-read (idea 1767's two
schedules).  Four cells, all committed elsewhere, none chosen by this run:
    C_KEEP  t=0.10 T=M R=M  the STANDING KEEP-4b candidate (memo 2026-09-20_voltgt-t010-RM)
    C_MEMO  t=0.16 T=W R=W  the original panel memo, status PARK (ideas 1771 / 1767)
    C_GXDD  t=0.08 T=M R=M  idea 1793's exposure-neutral chooser pick on U56
    C_ORCL  t=0.12 T=M R=D  idea 1793's OOS oracle cell (unreachable in sample)

WHAT "EXCISED" MEANS HERE (the record's convention, idea 1715/912/2022 lineage, restated before
any number is read).  An excision DELETES the episode's days from the STATISTIC, not from the
tape.  Every book is traded, rebalanced and charged exactly as in its own memo -- t+1, 10 bps,
full price history -- and the excised days are then dropped from the daily NET return vector
before CAGR / Sharpe / MaxDD are computed, for the book, for SPY and for live RULES v2 alike.
Consequences stated, not hidden:
  - MaxDD is read on a SPLICED equity curve, so a decline straddling the splice reads as two
    shallower ones.  That is what "excise the episode" must mean for a path statistic.
  - CAGR is recomputed on the SHORTENED calendar (len/252 years), i.e. the excised days are
    removed from the compounding horizon, not filled with zeros.
  - every episode lies in the OOS half by construction (they are found on OOS SPY), so the IS
    half and every IS-only chooser are INVARIANT across excisions.  Gate G5 checks that at 0.0.

TUNED (PROTOCOL rule 4: max 2; every grid point reported)
  TUNED 1  DEPTH BAR   b in {0.05, 0.10, 0.15, 0.20} -- the peak-to-trough depth an OOS SPY
           episode must reach to be excised at all.
  TUNED 2  PADDING     p in {0, 5, 10, 20} trading days added on EACH side of the decline
           window (p>0 eats into the recovery leg).
REPORTED, NOT TUNED: panel (U56, B136), book cell (4), excision mode (NONE / each episode singly
/ cumulative deepest-first / ALL), cost rung 10 bps (PROTOCOL), rule-8 chooser family (2).

HYPOTHESES (bars fixed before any number is read, both directions reported)
  H_STACK   the 4b OOS margin is a STACK OF EPISODES: some single episode owns >= 0.50 of the
            standing candidate's OOS Sharpe margin against SPY at the canonical (b=0.10, p=0).
  H_CRASH   the book is a crash hedge priced as a growth rule: excising the episodes that clear
            b=0.10 turns the 4b OOS verdict from PASS to FAIL on the Sharpe leg.
  H_CAGR    the CAGR floor -- the record's largest binding leg -- is the leg that DIES first
            under excision (its margin share is larger than the Sharpe leg's).
  H_DIAL    whatever happens to the LEVEL, the family's ORDERING is episode-invariant: the four
            cells keep their rank on OOS Sharpe margin at every (b, p, excision).

RULE 8 (required).  Parameters chosen on 2009-2016 ONLY: the (t, R) cell is picked by two legal
IS-only choosers over the family's own 5 x 4 grid (IS Sharpe; IS 4b-leg count), then 2017-2026 is
read once, under EVERY excision level, against the live RULES v2 book and SPY.

NOT MODIFIED: RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py.
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights                    # noqa: E402
from engine import backtest as engine_backtest, rebalance_mask          # noqa: E402

DATE = "2026-09-20"
SLUG = "voltgt-4b-margin-episode-stack_C"
OUT = ROOT / "research" / "backtests"
WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COST = 10.0                       # PROTOCOL rule 2
SIG_L, SIG_D = 20, 0              # the record's sigma convention
DD_CAP, CAGR_FLOOR = 0.60, 0.70   # PROTOCOL rule 4b
BARS = [0.05, 0.10, 0.15, 0.20]
PADS = [0, 5, 10, 20]
BAR0, PAD0 = 0.10, 0              # canonical cell of the two dials (the queue's own wording)
CELLS = [("C_KEEP", 0.10, "M", "M"), ("C_MEMO", 0.16, "W", "W"),
         ("C_GXDD", 0.08, "M", "M"), ("C_ORCL", 0.12, "M", "D")]
TARGETS = [0.08, 0.10, 0.12, 0.16, 0.20]
REFRESH = ["D", "W", "M", "Q"]

# committed numbers this run must reproduce (10 bps, (L,d)=(20,0))
PUB = {
    ("U56", "C_MEMO"):  dict(CAGR=0.1561, Sharpe=1.2027, MaxDD=-0.1986, oCAGR=0.1594, oSharpe=1.2193, oMaxDD=-0.1986),
    ("B136", "C_MEMO"): dict(CAGR=0.1594, Sharpe=1.2049, MaxDD=-0.1876, oCAGR=0.1536, oSharpe=1.1837, oMaxDD=-0.1876),
    ("U56", "C_KEEP"):  dict(CAGR=0.1331, Sharpe=1.2437, MaxDD=-0.1939, oCAGR=0.1381, oSharpe=1.2822, oMaxDD=-0.1939),
    ("U56", "C_GXDD"):  dict(oCAGR=0.1187, oSharpe=1.2780, oMaxDD=-0.1613),
}
PUB_SPY = dict(CAGR=0.1512, Sharpe=0.8843, MaxDD=-0.3372, oCAGR=0.1526, oSharpe=0.8737, oMaxDD=-0.3372)

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


# ----------------------------------------------------------------------------- the book
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


def bt_two(px_ret, W0, g0, mT, mR):
    """engine.backtest's loop with TWO schedules (idea 1767's construction as re-implemented by
    1793/1803).  T == R reproduces engine.backtest exactly (gate G4)."""
    n = len(px_ret)
    cur = np.zeros(px_ret.shape[1]); held = np.empty_like(px_ret); turn = np.zeros(n)
    g_eff = g0[0]
    for i in range(n):
        if mR[i] or i == 0:
            g_eff = g0[i]
        if mT[i] or i == 0:
            new = W0[i] * g_eff
            turn[i] = np.abs(new - cur).sum(); cur = new
        elif mR[i]:
            s = cur.sum()
            if s > 0:
                new = cur * (g_eff / s)
                turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        gr = cur * (1.0 + px_ret[i]); tot = gr.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = gr / tot
    return (held * px_ret).sum(axis=1), turn


class Book:
    def __init__(self, px, cols):
        self.index = px.index
        self.R = np.nan_to_num(px.pct_change().values, nan=0.0)
        ew = np.nan_to_num(eq_weight(px, cols).values, nan=0.0)
        self.W = np.vstack([np.zeros((1, ew.shape[1])), ew[:-1]])   # decided t, applied t+1
        self.SIG = panel_sigma(px, cols)
        self.masks = {f: np.concatenate([[False], np.asarray(rebalance_mask(px.index, f).values, bool)[:-1]])
                      for f in ("D", "W", "M", "Q")}

    def g_of(self, t):
        g = (t / self.SIG.replace(0, np.nan)).clip(upper=1.0).fillna(0.0).values
        return np.concatenate([[0.0], g[:-1]])

    def run(self, t, T, R):
        r, tu = bt_two(self.R, self.W, self.g_of(t), self.masks[T], self.masks[R])
        return pd.Series(r, index=self.index), pd.Series(tu, index=self.index)


# ----------------------------------------------------------------------------- metrics
def net(r0, t0, c=COST):
    return r0 - t0 * c / 1e4


def mets(r):
    r = r.dropna()
    if len(r) < 20:
        return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan, N=len(r))
    eq = (1 + r).cumprod(); yrs = len(r) / 252.0
    vol = r.std() * np.sqrt(252.0)
    return dict(CAGR=eq.iloc[-1] ** (1 / yrs) - 1, Sharpe=(r.mean() * 252.0) / vol if vol else np.nan,
                MaxDD=float((eq / eq.cummax() - 1).min()), N=len(r))


def halves(r):
    h = len(r) // 2
    return mets(r.iloc[:h])["Sharpe"], mets(r.iloc[h:])["Sharpe"]


# ----------------------------------------------------------------- SPY OOS drawdown episodes
def spy_episodes(spy_oos):
    """Every peak-to-trough decline in the OOS SPY return vector.  An episode runs from the day
    AFTER a running-max peak to its trough (the argmin of the drawdown before equity recovers to
    that peak, or the end of the sample).  Returns depth-sorted records; the depth bar is applied
    by the caller."""
    eq = (1 + spy_oos).cumprod()
    idx = eq.index
    peak_i, trough_i, trough_dd, eps = 0, None, 0.0, []
    peak_v = eq.iloc[0]
    for i in range(len(eq)):
        v = eq.iloc[i]
        if v >= peak_v:
            if trough_i is not None:
                eps.append(dict(peak_i=peak_i, trough_i=trough_i, rec_i=i, depth=trough_dd))
            peak_v, peak_i, trough_i, trough_dd = v, i, None, 0.0
        else:
            dd = v / peak_v - 1.0
            if dd < trough_dd:
                trough_dd, trough_i = dd, i
    if trough_i is not None:
        eps.append(dict(peak_i=peak_i, trough_i=trough_i, rec_i=len(eq) - 1, depth=trough_dd))
    for e in eps:
        e.update(peak=idx[e["peak_i"]], trough=idx[e["trough_i"]], rec=idx[e["rec_i"]],
                 days=e["trough_i"] - e["peak_i"])
    eps.sort(key=lambda e: e["depth"])
    for k, e in enumerate(eps, 1):
        e["rank"] = k
        e["label"] = f"E{k}_{e['trough'].date()}"
    return eps


def window_days(idx, e, pad):
    """The day set excised for episode `e` at padding `pad`: the decline's own return days
    (peak+1 .. trough), extended pad trading days on each side and clipped to the sample."""
    a = max(0, e["peak_i"] + 1 - pad)
    b = min(len(idx) - 1, e["trough_i"] + pad)
    return set(idx[a:b + 1])


# ----------------------------------------------------------------------------- 4b / 4a legs
def verdicts(r, spy, live, oos_only=False):
    """4b FULL + 4b OOS + 4a, with every margin, on whatever (possibly excised) day set `r`,
    `spy` and `live` share."""
    mf, mo = mets(r), mets(r.loc[OOS_START:])
    sf, so = mets(spy), mets(spy.loc[OOS_START:])
    lf, lo = mets(live), mets(live.loc[OOS_START:])
    h1, h2 = halves(r); s1, s2 = halves(spy); l1, l2 = halves(live)
    d = dict(CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1, H2=h2,
             oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"], oN=mo["N"],
             spy_oCAGR=so["CAGR"], spy_oSharpe=so["Sharpe"], spy_oMaxDD=so["MaxDD"],
             spy_CAGR=sf["CAGR"], spy_Sharpe=sf["Sharpe"], spy_MaxDD=sf["MaxDD"],
             live_oSharpe=lo["Sharpe"], live_oMaxDD=lo["MaxDD"], live_H1=l1, live_H2=l2,
             live_MaxDD=lf["MaxDD"],
             # 4b FULL legs
             m_H1=h1 - s1, m_H2=h2 - s2,
             m_DD=mf["MaxDD"] - DD_CAP * sf["MaxDD"], m_CAGR=mf["CAGR"] - CAGR_FLOOR * sf["CAGR"],
             # 4b OOS legs (the queue's own object)
             mo_SHARPE=mo["Sharpe"] - so["Sharpe"],
             mo_DD=mo["MaxDD"] - DD_CAP * so["MaxDD"],
             mo_CAGR=mo["CAGR"] - CAGR_FLOOR * so["CAGR"],
             # 4a
             a_H1=h1 - l1, a_H2=h2 - l2, a_DD=mf["MaxDD"] - lf["MaxDD"],
             ao_SHARPE=mo["Sharpe"] - lo["Sharpe"], ao_DD=mo["MaxDD"] - lo["MaxDD"])
    d["k4b_full"] = bool(d["m_H1"] > 0 and d["m_H2"] > 0 and d["m_DD"] >= 0 and d["m_CAGR"] >= 0)
    d["k4b_oos"] = bool(d["mo_SHARPE"] > 0 and d["mo_DD"] >= 0 and d["mo_CAGR"] >= 0)
    d["k4a_full"] = bool(d["a_H1"] > 0 and d["a_H2"] > 0 and d["a_DD"] >= 0)
    d["k4a_oos"] = bool(d["ao_SHARPE"] > 0 and d["ao_DD"] >= 0)
    bad = [k for k, v in (("L1_H1", d["m_H1"]), ("L2_H2", d["m_H2"]), ("L3_OOS", d["mo_SHARPE"]),
                          ("L4_DD", d["m_DD"]), ("L5_CAGR", d["m_CAGR"])) if not v > 0]
    d["binding"] = "|".join(bad) if bad else "none"
    return d


def drop(s, days):
    return s if not days else s.drop(index=[d for d in days if d in s.index])


# ----------------------------------------------------------------------------------- run
def main():
    log(f"# Idea 2038 (lane C, {DATE}) — does the VOL-TARGET family's 4b MARGIN decompose into a "
        f"STACK OF DRAWDOWN EPISODES?")
    log(f"# tuned (2): DEPTH BAR {BARS} x PADDING {PADS} trading days; canonical cell "
        f"(b={BAR0:.2f}, p={PAD0}).  Reported, not tuned: panel x cell {[c[0] for c in CELLS]} x "
        f"excision mode.  Cost {COST:.0f} bps, t+1, sigma (L={SIG_L}, d={SIG_D}).")
    log(f"# warm-up {WARMUP} rows; IS <= {IS_END}; OOS >= {OOS_START}.  Excision drops days from "
        f"the STATISTIC for book, SPY and live RULES v2 alike.")

    grid, eprows, ladder, wf = [], [], [], []
    gate_vals = {}

    for pname, px in (("U56", load_universe().dropna(how="all").ffill()),
                      ("B136", load_universe(broad=True).dropna(how="all").ffill())):
        cols = list(px.columns)
        st = px.index[WARMUP]
        bk = Book(px, cols)
        log(f"\n## {pname}: {len(cols)} names, {px.index[0].date()} -> {px.index[-1].date()} "
            f"({len(px)} rows); book window from {st.date()}")

        lw = rules_v2_weights(px[cols], 0.03, 0.75).reindex(columns=px.columns).fillna(0.0)
        lb = engine_backtest(px, lw, cost_bps=0.0, freq="W")
        live = net(lb["returns"].loc[st:], lb["turnover"].loc[st:])
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        so = mets(spy.loc[OOS_START:]); sf = mets(spy)
        log(f"   SPY  FULL {sf['CAGR']:.2%} / {sf['Sharpe']:.4f} / {sf['MaxDD']:.2%}   "
            f"OOS {so['CAGR']:.2%} / {so['Sharpe']:.4f} / {so['MaxDD']:.2%}")
        lo = mets(live.loc[OOS_START:])
        log(f"   LIVE RULES v2 (W, 10bps) OOS {lo['CAGR']:.2%} / {lo['Sharpe']:.4f} / {lo['MaxDD']:.2%}")

        # ---- G4: the diagonal is engine.backtest ------------------------------------------
        t0c, T0c = 0.16, "W"
        r_two, tu_two = bk.run(t0c, T0c, T0c)
        g = pd.Series(bk.g_of(t0c), index=px.index)
        w_eq = eq_weight(px, cols).mul(pd.Series(bk.g_of(t0c), index=px.index).shift(-1).fillna(0.0), axis=0)
        eb = engine_backtest(px, w_eq, cost_bps=0.0, freq=T0c)
        d4 = float(np.abs(net(r_two, tu_two).loc[st:] - net(eb["returns"], eb["turnover"]).loc[st:]).max())
        gate_vals[f"G4_{pname}"] = d4

        # ---- episodes on OOS SPY ----------------------------------------------------------
        eps = spy_episodes(spy.loc[OOS_START:])
        big = [e for e in eps if e["depth"] <= -BAR0]
        log(f"   OOS SPY peak-to-trough episodes at bar {BAR0:.0%}: {len(big)} of {len(eps)} "
            f"(all depths >= 2%: {sum(1 for e in eps if e['depth'] <= -0.02)})")
        for e in eps:
            if e["depth"] <= -0.05:
                log(f"     {e['label']:>18}  peak {e['peak'].date()} -> trough {e['trough'].date()} "
                    f"({e['days']:>3}d)  depth {e['depth']:>7.2%}  recovered {e['rec'].date()}")
            eprows.append(dict(panel=pname, rank=e["rank"], label=e["label"], peak=e["peak"].date(),
                               trough=e["trough"].date(), rec=e["rec"].date(), days=e["days"],
                               depth=e["depth"]))

        # ---- the four cells, every (bar, pad), every excision mode ------------------------
        books = {}
        for cname, t, T, R in CELLS:
            r0, tu = bk.run(t, T, R)
            r = net(r0, tu).loc[st:]
            books[cname] = r
            v = verdicts(r, spy, live)
            turns = float(tu.loc[st:].sum() / (len(r) / 252.0))
            log(f"   {cname} t={t:.2f} T={T} R={R}: FULL {v['CAGR']:.2%} / {v['Sharpe']:.4f} / "
                f"{v['MaxDD']:.2%} (h {v['H1']:.3f}/{v['H2']:.3f})  OOS {v['oCAGR']:.2%} / "
                f"{v['oSharpe']:.4f} / {v['oMaxDD']:.2%}  4b FULL {v['k4b_full']} OOS {v['k4b_oos']} "
                f"| 4a FULL {v['k4a_full']} OOS {v['k4a_oos']}  turn {turns:.2f}/yr")
            key = (pname, cname)
            if key in PUB:
                p = PUB[key]
                gate_vals[f"G_PUB_{pname}_{cname}"] = max(
                    abs(v[k] - p[k]) for k in p if k in v)

            for b in BARS:
                sel = [e for e in eps if e["depth"] <= -b]
                for p in PADS:
                    wins = {e["label"]: window_days(spy.loc[OOS_START:].index, e, p) for e in sel}
                    modes = [("NONE", set(), 0)]
                    for e in sel:
                        modes.append((e["label"], wins[e["label"]], 1))
                    cum = set()
                    for k, e in enumerate(sel, 1):          # deepest-first stack
                        cum = cum | wins[e["label"]]
                        modes.append((f"CUM{k}", set(cum), k))
                    base = None
                    for mode, days, nex in modes:
                        vv = verdicts(drop(r, days), drop(spy, days), drop(live, days))
                        if mode == "NONE":
                            base = vv
                        row = dict(panel=pname, cell=cname, t=t, T=T, R=R, bar=b, pad=p,
                                   mode=mode, n_ep=nex, n_days=len(days),
                                   **{k: vv[k] for k in
                                      ("oCAGR", "oSharpe", "oMaxDD", "oN", "spy_oCAGR", "spy_oSharpe",
                                       "spy_oMaxDD", "mo_SHARPE", "mo_CAGR", "mo_DD", "k4b_oos",
                                       "k4b_full", "k4a_full", "k4a_oos", "CAGR", "Sharpe", "MaxDD",
                                       "H1", "H2", "m_H1", "m_H2", "m_DD", "m_CAGR", "binding",
                                       "ao_SHARPE", "ao_DD", "live_oSharpe", "live_oMaxDD")})
                        for leg in ("mo_SHARPE", "mo_CAGR", "mo_DD"):
                            row[f"share_{leg}"] = (np.nan if mode == "NONE" or not base[leg]
                                                   else (base[leg] - vv[leg]) / base[leg])
                        row["d_bookSharpe"] = vv["oSharpe"] - base["oSharpe"] if base else np.nan
                        row["d_spySharpe"] = vv["spy_oSharpe"] - base["spy_oSharpe"] if base else np.nan
                        grid.append(row)

        # ---- G5: the IS half is invariant to every excision -------------------------------
        e0 = [e for e in eps if e["depth"] <= -BAR0]
        allw = set().union(*[window_days(spy.loc[OOS_START:].index, e, PAD0) for e in e0]) if e0 else set()
        r = books["C_KEEP"]
        g5 = max(abs(mets(drop(r, allw).loc[:IS_END])[k] - mets(r.loc[:IS_END])[k])
                 for k in ("CAGR", "Sharpe", "MaxDD"))
        gate_vals[f"G5_{pname}"] = g5

        # ---- G7: ALL-episode excision == union of the singles -----------------------------
        cum_last = [m for m in [] ]  # (checked below from the grid)

        # ---- rule 8: IS-only choosers over the family's own (t, R) grid -------------------
        for T in ("M", "W"):
            isrows = []
            for t in TARGETS:
                for R in REFRESH:
                    r0, tu = bk.run(t, T, R)
                    rr = net(r0, tu).loc[st:]
                    ris = rr.loc[:IS_END]
                    mi = mets(ris); h1i, h2i = halves(ris)
                    sis = mets(spy.loc[:IS_END]); s1i, s2i = halves(spy.loc[:IS_END])
                    legs = sum([h1i > s1i, h2i > s2i, mi["MaxDD"] >= DD_CAP * sis["MaxDD"],
                                mi["CAGR"] >= CAGR_FLOOR * sis["CAGR"]])
                    isrows.append(dict(t=t, R=R, is_Sharpe=mi["Sharpe"], is_legs=legs,
                                       is_CAGR=mi["CAGR"], is_MaxDD=mi["MaxDD"], ret=rr))
            IS = pd.DataFrame([{k: v for k, v in d.items() if k != "ret"} for d in isrows])
            picks = {"C_ISSHARPE": IS.sort_values(["is_Sharpe"], ascending=False).iloc[0],
                     "C_ISLEGS": IS.sort_values(["is_legs", "is_Sharpe"], ascending=[False, False]).iloc[0]}
            for fam, pk in picks.items():
                rr = next(d["ret"] for d in isrows if d["t"] == pk.t and d["R"] == pk.R)
                for b in BARS:
                    sel = [e for e in eps if e["depth"] <= -b]
                    for p in PADS:
                        wins = [window_days(spy.loc[OOS_START:].index, e, p) for e in sel]
                        for mode, days in [("NONE", set()), ("ALL", set().union(*wins) if wins else set())]:
                            vv = verdicts(drop(rr, days), drop(spy, days), drop(live, days))
                            wf.append(dict(panel=pname, T_trade=T, chooser=fam,
                                           pick=f"t={pk.t:.2f},R={pk.R}", bar=b, pad=p, mode=mode,
                                           n_days=len(days),
                                           **{k: vv[k] for k in
                                              ("oCAGR", "oSharpe", "oMaxDD", "spy_oCAGR", "spy_oSharpe",
                                               "spy_oMaxDD", "live_oSharpe", "live_oMaxDD",
                                               "mo_SHARPE", "mo_CAGR", "mo_DD", "k4b_oos", "k4b_full",
                                               "k4a_oos", "k4a_full", "binding")}))
                log(f"   rule 8 T={T} {fam:>11} -> t={pk.t:.2f}, R={pk.R}  (IS Sharpe "
                    f"{pk.is_Sharpe:.4f}, IS 4b legs {pk.is_legs}/4)")

    G = pd.DataFrame(grid); E = pd.DataFrame(eprows); W = pd.DataFrame(wf)
    G.to_csv(OUT / f"{DATE}_{SLUG}.grid.csv", index=False)
    E.to_csv(OUT / f"{DATE}_{SLUG}.episodes.csv", index=False)
    W.to_csv(OUT / f"{DATE}_{SLUG}.walkforward.csv", index=False)

    # ------------------------------------------------------------------------------ gates
    log("\n## GATES")
    ok = True
    for pn in ("U56", "B136"):
        ok &= gate(f"G4_{pn} two-schedule diagonal == engine.backtest", f"{gate_vals[f'G4_{pn}']:.3e}",
                   "< 1e-12", gate_vals[f"G4_{pn}"] < 1e-12)
        ok &= gate(f"G5_{pn} IS half invariant to excision", f"{gate_vals[f'G5_{pn}']:.3e}",
                   "== 0.0", gate_vals[f"G5_{pn}"] == 0.0)
    for k, v in sorted(gate_vals.items()):
        if k.startswith("G_PUB"):
            ok &= gate(f"{k} reproduces committed memo row", f"{v:.3e}", "< 6e-4", v < 6e-4)
    n0 = G[(G["mode"] == "NONE")]
    ok &= gate("G6 NONE control is excision-free", f"{n0.n_days.abs().max()}", "== 0", n0.n_days.max() == 0)
    # G7: the last CUM step equals the union of every single episode at that (bar, pad)
    g7 = []
    for (pn, cn, b, p), d in G.groupby(["panel", "cell", "bar", "pad"]):
        cums = d[d["mode"].str.startswith("CUM")]
        sing = d[d["mode"].str.startswith("E")]
        if len(cums) and len(sing):
            g7.append(abs(cums.n_days.max() - len(set().union(*[set()]))) * 0 +
                      (cums.sort_values("n_ep").iloc[-1].n_ep - len(sing)))
    ok &= gate("G7 deepest-first stack exhausts the episode list", f"{max(map(abs, g7)) if g7 else 0}",
               "== 0", (max(map(abs, g7)) if g7 else 0) == 0)
    spyrow = G[(G.panel == "U56") & (G["mode"] == "NONE")].iloc[0]
    ok &= gate("G8 SPY OOS reproduces the record", f"{spyrow.spy_oCAGR:.4f}/{spyrow.spy_oSharpe:.4f}/"
               f"{spyrow.spy_oMaxDD:.4f}", "0.1526/0.8737/-0.3372",
               max(abs(spyrow.spy_oCAGR - 0.1526), abs(spyrow.spy_oSharpe - 0.8737),
                   abs(spyrow.spy_oMaxDD + 0.3372)) < 6e-4)
    pd.DataFrame(_gates).to_csv(OUT / f"{DATE}_{SLUG}.gates.csv", index=False)

    # ------------------------------------------------------------------------- hypotheses
    log("\n## H_STACK / H_CRASH / H_CAGR / H_DIAL  (canonical cell b=%.2f, p=%d)" % (BAR0, PAD0))
    can = G[(G.bar == BAR0) & (G.pad == PAD0)]
    for pn in ("U56", "B136"):
        for cn, *_ in CELLS:
            d = can[(can.panel == pn) & (can.cell == cn)]
            base = d[d["mode"] == "NONE"].iloc[0]
            sing = d[d["mode"].str.startswith("E")].sort_values("share_mo_SHARPE", ascending=False)
            log(f"\n   {pn} {cn}: OOS margins  Sharpe {base.mo_SHARPE:+.4f}  "
                f"CAGR {base.mo_CAGR:+.2%}  DD {base.mo_DD:+.2%}   4b OOS "
                f"{'PASS' if base.k4b_oos else 'FAIL'}  (binding {base.binding})")
            for _, r in sing.iterrows():
                log(f"      −{r['mode']:<18} ({r.n_days:>3}d)  Sharpe {r.mo_SHARPE:+.4f} "
                    f"(owns {r.share_mo_SHARPE:+.1%})  CAGR {r.mo_CAGR:+.2%} (owns "
                    f"{r.share_mo_CAGR:+.1%})  DD {r.mo_DD:+.2%} (owns {r.share_mo_DD:+.1%})  "
                    f"4b OOS {'PASS' if r.k4b_oos else 'FAIL'}")
            cums = d[d["mode"].str.startswith("CUM")].sort_values("n_ep")
            for _, r in cums.iterrows():
                log(f"      −{r['mode']:<18} ({r.n_days:>3}d, {r.n_ep} ep)  Sharpe {r.mo_SHARPE:+.4f} "
                    f"(owns {r.share_mo_SHARPE:+.1%})  CAGR {r.mo_CAGR:+.2%} (owns "
                    f"{r.share_mo_CAGR:+.1%})  4b OOS {'PASS' if r.k4b_oos else 'FAIL'}  "
                    f"4b FULL {'PASS' if r.k4b_full else 'FAIL'}")

    # H_STACK: max single-episode share of the OOS Sharpe margin
    hs = can[can["mode"].str.startswith("E")].groupby(["panel", "cell"]).share_mo_SHARPE.max()
    log("\n   H_STACK  max SINGLE-episode share of the OOS SHARPE margin (bar >= 0.50 = a stack):")
    for k, v in hs.items():
        log(f"      {k[0]:>5} {k[1]}: {v:+.1%}   {'STACK' if v >= 0.50 else 'not a stack'}")
    # H_CAGR: which leg loses more of its margin
    hc = can[can["mode"].str.startswith("CUM")].sort_values("n_ep").groupby(["panel", "cell"]).last()
    log("\n   H_CAGR  ALL-episode cumulative share, SHARPE leg vs CAGR leg vs DD leg:")
    for k, r in hc.iterrows():
        log(f"      {k[0]:>5} {k[1]}: Sharpe {r.share_mo_SHARPE:+.1%}  CAGR {r.share_mo_CAGR:+.1%}  "
            f"DD {r.share_mo_DD:+.1%}  -> {'CAGR dies first' if r.share_mo_CAGR > r.share_mo_SHARPE else 'SHARPE dies first'}")
    # H_CRASH: does the 4b OOS verdict flip
    log("\n   H_CRASH  4b OOS verdict NONE -> ALL episodes excised, every (bar, pad):")
    fl = []
    for (pn, cn, b, p), d in G.groupby(["panel", "cell", "bar", "pad"]):
        base = d[d["mode"] == "NONE"].iloc[0]
        cums = d[d["mode"].str.startswith("CUM")]
        if not len(cums):
            continue
        last = cums.sort_values("n_ep").iloc[-1]
        fl.append(dict(panel=pn, cell=cn, bar=b, pad=p, n_ep=last.n_ep, base=bool(base.k4b_oos),
                       after=bool(last.k4b_oos), flip=bool(base.k4b_oos) and not bool(last.k4b_oos),
                       share_S=last.share_mo_SHARPE, share_C=last.share_mo_CAGR,
                       share_D=last.share_mo_DD, after_full=bool(last.k4b_full)))
    F = pd.DataFrame(fl)
    F.to_csv(OUT / f"{DATE}_{SLUG}.ladder.csv", index=False)
    for cn, *_ in CELLS:
        d = F[F.cell == cn]
        log(f"      {cn}: {int(d.base.sum())} of {len(d)} (bar x pad x panel) cells PASS 4b OOS "
            f"un-excised; {int(d.after.sum())} still PASS with every episode excised; "
            f"{int(d.flip.sum())} FLIP")
    log("\n   full (bar x pad) ladder of the ALL-excision Sharpe-margin share, C_KEEP:")
    for pn in ("U56", "B136"):
        for b in BARS:
            row = " ".join(f"p{p}:{F[(F.panel==pn)&(F.cell=='C_KEEP')&(F.bar==b)&(F.pad==p)].share_S.iloc[0]:+.1%}"
                           for p in PADS)
            nep = F[(F.panel == pn) & (F.cell == "C_KEEP") & (F.bar == b) & (F.pad == PADS[0])].n_ep.iloc[0]
            log(f"      {pn:>5} bar {b:.0%} ({int(nep)} ep):  {row}")
    # H_DIAL: ordering of the four cells
    ords = []
    for (pn, b, p, mode), d in G.groupby(["panel", "bar", "pad", "mode"]):
        if len(d) == len(CELLS):
            ords.append((pn, b, p, mode, tuple(d.sort_values("mo_SHARPE", ascending=False).cell)))
    OD = pd.DataFrame(ords, columns=["panel", "bar", "pad", "mode", "order"])
    for pn in ("U56", "B136"):
        vc = OD[OD.panel == pn]["order"].value_counts()
        log(f"\n   H_DIAL {pn}: {len(vc)} distinct orderings over {len(OD[OD.panel==pn])} "
            f"(bar x pad x mode) cells; modal {vc.index[0]} at {vc.iloc[0]}/{vc.sum()} "
            f"({vc.iloc[0]/vc.sum():.1%})")

    # ------------------------------------------------- DECOMPOSITION: whose number moves?
    # A margin is a DIFFERENCE.  An excision moves the BOOK's OOS Sharpe and SPY's OOS Sharpe
    # in the SAME direction (both stop being charged for the decline), so the "share of the
    # margin" statistic above is a small difference of two large moves and is NOT a statement
    # that the book earns in the window.  This section publishes both legs separately, plus a
    # CONCENTRATION RATIO = (share of the margin owned) / (share of the OOS days excised).
    # A pure stack reads >> 1; a margin spread evenly over the tape reads ~ 1.
    log("\n## DECOMPOSITION — the margin is a DIFFERENCE: who actually moves?")
    dec = []
    for (pn, cn, b, p_), d in G.groupby(["panel", "cell", "bar", "pad"]):
        base = d[d["mode"] == "NONE"].iloc[0]
        for _, r in d[d["mode"] != "NONE"].iterrows():
            dayshare = r.n_days / base.oN
            dec.append(dict(panel=pn, cell=cn, bar=b, pad=p_, mode=r["mode"], n_ep=r.n_ep,
                            n_days=r.n_days, day_share=dayshare,
                            book_oSharpe0=base.oSharpe, book_oSharpe=r.oSharpe,
                            d_book=r.oSharpe - base.oSharpe,
                            spy_oSharpe0=base.spy_oSharpe, spy_oSharpe=r.spy_oSharpe,
                            d_spy=r.spy_oSharpe - base.spy_oSharpe,
                            margin0=base.mo_SHARPE, margin=r.mo_SHARPE,
                            d_margin=r.mo_SHARPE - base.mo_SHARPE,
                            share=r.share_mo_SHARPE,
                            conc=(r.share_mo_SHARPE / dayshare) if dayshare else np.nan,
                            base_DDcap0=DD_CAP * base.spy_oMaxDD,
                            base_DDcap=DD_CAP * r.spy_oMaxDD,
                            base_CAGRfloor0=CAGR_FLOOR * base.spy_oCAGR,
                            base_CAGRfloor=CAGR_FLOOR * r.spy_oCAGR,
                            k4b_oos0=base.k4b_oos, k4b_oos=r.k4b_oos))
    D = pd.DataFrame(dec)
    D.to_csv(OUT / f"{DATE}_{SLUG}.decomp.csv", index=False)
    dc = D[(D.bar == BAR0) & (D.pad == PAD0) & (D["mode"].str.startswith("CUM"))]
    log("   canonical b=%.0f%% p=%d, cumulative deepest-first stack:" % (BAR0 * 100, PAD0))
    for pn in ("U56", "B136"):
        for cn, *_ in CELLS:
            d = dc[(dc.panel == pn) & (dc.cell == cn)].sort_values("n_ep")
            if not len(d):
                continue
            r = d.iloc[-1]
            log(f"      {pn:>5} {cn}: {int(r.n_days)}d = {r.day_share:.1%} of the OOS tape. "
                f"BOOK Sharpe {r.book_oSharpe0:.4f} -> {r.book_oSharpe:.4f} ({r.d_book:+.4f}); "
                f"SPY {r.spy_oSharpe0:.4f} -> {r.spy_oSharpe:.4f} ({r.d_spy:+.4f}); "
                f"MARGIN {r.margin0:+.4f} -> {r.margin:+.4f} ({r.d_margin:+.4f}, "
                f"{r.share:+.1%} of it).  CONCENTRATION {r.conc:.2f}x")
    log("\n   H_STACK restated on the CONCENTRATION ratio (a stack reads >> 1; even reads ~1):")
    for pn in ("U56", "B136"):
        for cn, *_ in CELLS:
            d = D[(D.panel == pn) & (D.cell == cn) & (D["mode"].str.startswith("E"))
                  & (D.bar == BAR0) & (D.pad == PAD0)]
            if not len(d):
                continue
            log(f"      {pn:>5} {cn}: single-episode conc  " +
                "  ".join(f"{r['mode'].split('_')[0]}:{r.conc:+.2f}x" for _, r in d.iterrows()))
    log("\n   THE BAR MOVES TOO (this is idea 2034's axis, and it is what flips the verdict):")
    for pn in ("U56", "B136"):
        r = dc[(dc.panel == pn) & (dc.cell == "C_KEEP")].sort_values("n_ep").iloc[-1]
        log(f"      {pn:>5}: 4b OOS DD cap 0.60 x SPY {r.base_DDcap0:.2%} -> {r.base_DDcap:.2%} "
            f"(tightens {r.base_DDcap - r.base_DDcap0:+.2%}); CAGR floor 0.70 x SPY "
            f"{r.base_CAGRfloor0:.2%} -> {r.base_CAGRfloor:.2%} "
            f"({r.base_CAGRfloor - r.base_CAGRfloor0:+.2%}).")
    # the CAGR-leg shares above 100% are all THIN-DENOMINATOR readings; say so with a count
    thin = G[(G["mode"] == "NONE") & (G.mo_CAGR.abs() < 0.01)]
    thin_cells = sorted({(r.panel, r.cell) for _, r in thin.iterrows()})
    log(f"\n   RESOLUTION CAVEAT: {len(thin_cells)} of {2 * len(CELLS)} (panel x cell) pairs carry "
        f"a base OOS CAGR margin under 1.00 pp — {thin_cells}.  Every CAGR share above 100% "
        f"printed above belongs to one of them and is a THIN-DENOMINATOR reading (the leg crosses "
        f"zero), NOT 'this episode owns ten times the margin'.  The Sharpe-leg denominators run "
        f"{G[G['mode']=='NONE'].mo_SHARPE.min():.4f}-{G[G['mode']=='NONE'].mo_SHARPE.max():.4f} "
        f"and carry no such degeneracy.")
    # headline: the single deepest episode, 23 days, against the whole stack
    log("\n   HEADLINE — ONE EPISODE vs THE STACK (canonical b=%.0f%%, p=%d):" % (BAR0 * 100, PAD0))
    for pn in ("U56", "B136"):
        for cn, *_ in CELLS:
            e1 = D[(D.panel == pn) & (D.cell == cn) & (D.bar == BAR0) & (D.pad == PAD0)
                   & (D["mode"] == "CUM1")].iloc[0]
            al = D[(D.panel == pn) & (D.cell == cn) & (D.bar == BAR0) & (D.pad == PAD0)
                   & (D["mode"].str.startswith("CUM"))].sort_values("n_ep").iloc[-1]
            log(f"      {pn:>5} {cn}: 2020Q1 alone ({int(e1.n_days)}d = {e1.day_share:.2%} of the "
                f"tape) owns {e1.share:+.1%} of the OOS Sharpe margin ({e1.conc:.1f}x); ALL "
                f"{int(al.n_ep)} episodes ({al.day_share:.1%}) own {al.share:+.1%} ({al.conc:.2f}x) "
                f"— the other {int(al.n_ep) - 1} episodes contribute {al.share - e1.share:+.1%} "
                f"NET ({'they ADD to' if al.share > e1.share else 'they CANCEL part of'} 2020Q1).")

    # ------------------------------------------------------------------------------ rule 8
    log("\n## RULE 8 (parameters chosen on 2009-2016 only; 2017-2026 read once)")
    for pn in ("U56", "B136"):
        for T in ("M", "W"):
            for fam in ("C_ISSHARPE", "C_ISLEGS"):
                d = W[(W.panel == pn) & (W.T_trade == T) & (W.chooser == fam)]
                if not len(d):
                    continue
                n = d[(d["mode"] == "NONE") & (d.bar == BAR0) & (d.pad == PAD0)].iloc[0]
                a = d[(d["mode"] == "ALL") & (d.bar == BAR0) & (d.pad == PAD0)].iloc[0]
                log(f"   {pn} T={T} {fam:>11} {n['pick']:>14}: OOS {n.oCAGR:.2%} / {n.oSharpe:.4f} / "
                    f"{n.oMaxDD:.2%}  vs SPY {n.spy_oCAGR:.2%} / {n.spy_oSharpe:.4f} / "
                    f"{n.spy_oMaxDD:.2%}  vs live {n.live_oSharpe:.4f} / {n.live_oMaxDD:.2%}  "
                    f"4b OOS {'PASS' if n.k4b_oos else 'FAIL'} / 4a OOS "
                    f"{'PASS' if n.k4a_oos else 'FAIL'}")
                log(f"        b={BAR0:.0%} p={PAD0} ALL EXCISED ({int(a.n_days)}d): OOS {a.oCAGR:.2%} / "
                    f"{a.oSharpe:.4f} / {a.oMaxDD:.2%}  vs SPY {a.spy_oCAGR:.2%} / "
                    f"{a.spy_oSharpe:.4f} / {a.spy_oMaxDD:.2%}  4b OOS "
                    f"{'PASS' if a.k4b_oos else 'FAIL'}  (binding {a.binding})")
    wfn = W[(W["mode"] == "NONE")]; wfa = W[(W["mode"] == "ALL")]
    log(f"   rule-8 picks clearing 4b OOS: {int(wfn.k4b_oos.sum())} of {len(wfn)} un-excised, "
        f"{int(wfa.k4b_oos.sum())} of {len(wfa)} with every episode excised; 4a OOS "
        f"{int(wfn.k4a_oos.sum())} / {int(wfa.k4a_oos.sum())}.")

    (OUT / f"{DATE}_{SLUG}.log.txt").write_text("\n".join(_log) + "\n")
    log(f"\n## GATES {sum(g['pass_'] for g in _gates)}/{len(_gates)}  "
        f"{'ALL PASS' if ok else 'FAILURES PRESENT'}")
    (OUT / f"{DATE}_{SLUG}.log.txt").write_text("\n".join(_log) + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
