#!/usr/bin/env python3
"""Idea 371 -- the-IS-chooser-prefers-SPY-where-OOS-prefers-QQQ: is the rule-8 chooser's
IS->OOS ordering inversion a property of COMPOSITION dials, or was it specific to the
QQQ-vs-SPY core of idea 30?

Background
----------
Idea 30 (research/backtests/2026-09-07_qqq-core-plus-sleeve-h1_B.py) found, on the
`c x q` grid of `c` of NAV in a 200d-gated equity core (q of it QQQ, 1-q SPY) plus
(1-c) in the idea-18 macro sleeve, that at c=0.60 OOS Sharpe rises MONOTONICALLY in q
(1.024 at q=0 -> 1.153 at q=1) while the rule-8 IS-Sharpe chooser, trained on 2009-2016,
picks q=0.50 and lands 0.019 BELOW the pre-registered anchor it was meant to improve.
That is a chooser error on a dial that changes only the COMPOSITION of a fixed exposure,
not its width (n, lookback, band) or its size (gross).  The queue asked whether that
inversion generalises.

What this script does
---------------------
[A] GATE.  Re-runs idea 30's exact cells (c=0.60, gate ON, both panels, 10 and 25 bps) and
    asserts equality against its committed grid CSV.
[B] NINE ONE-PARAMETER DIALS, each swept over 5 points, each classified in advance:
      COMPOSITION (re-allocates a fixed exposure between two components)
        C1 core-QQQ-vs-SPY      idea 30's dial, c=0.60 gated core + 0.40 macro sleeve
        C2 core-QQQ-vs-IWM      same structure, size composition
        C3 core-SPY-vs-EFA      same structure, geography composition
        C4 sleeve-equity-membership   idea-18 sleeve, equity legs scaled by q then the
                                      whole sleeve renormalised to its q=1 gross
        C5 book-blend-v1-vs-v2  q x RULES v1 (n=5, gross 0.75) + (1-q) x RULES v2
        C6 sector-tilt-XLK      gross 0.75 across 11 sector ETFs, q of it in XLK
      CONTROL (the dial classes rule 8 is already known to handle)
        W1 width-n              RULES v1 at n in {3,5,8,12,20}, w = 0.75/n (gross fixed)
        W2 width-band           RULES v2 band in {0.00,0.03,0.06,0.12,0.20}, gross 0.75
        G1 gross                RULES v2 band 0.03, gross in {0.20,0.40,0.60,0.80,1.00}
    Exactly ONE tuned parameter per dial (the dial position).  Panel (U56, B136), cost rung
    (0/10/25 bps) and dial identity are REPORTED axes, not tuned choices: all 270 cells are
    printed.  Both KEEP paths are evaluated at every one of them.
[C] ORDERING.  Per (dial, panel, cost): Spearman rho between IS Sharpe (2009-2016) and OOS
    Sharpe (2017-2026) across the dial's 5 points; the IS-argmax and OOS-argmax positions;
    the signed gap between them; and whether the dial's high-vol end is the one IS
    under-selects (orientation measured from the endpoint books, not assumed).
[D] RULE 8 (required).  Chooser trained on 2009-2016 IS Sharpe, OOS 2017-2026 read once:
    OOS CAGR/Sharpe/MaxDD of the pick vs the OOS-best cell (regret), vs the dial's
    pre-registered anchor, vs RULES v2 (live book) and vs SPY.
[E] THREE-FOLD robustness: the same ordering statistic on expanding train/test folds
    (train<=2013 -> 2014-2016; train<=2016 -> 2017-2020; train<=2020 -> 2021-2026), to
    separate "signed and reproducible" from "one split, one draw".

Conventions: weekly rebalance, weights decided at close t applied at t+1 (engine),
long-only, no leverage, 260-day warm-up skipped, 10 bps is the PROTOCOL rung (0 and 25 are
reported robustness rungs).

CAVEATS: (1) both panels are current-constituent lists -- survivorship flatters levels; the
IS-vs-OOS ORDERING statistics studied here are far less affected, but the OOS window is the
one where survivorship bias is largest.  (2) Five points per dial means the Spearman rho
takes only a few discrete values (|rho| in {0.0,0.1,...,1.0} at steps of 0.1) and a single
rho carries roughly 1.5 effective degrees of freedom; nothing here rests on one dial's rho,
only on the census across dials, panels, rungs and folds.  (3) C1-C4 hold only ETFs present
in both panels, so their panel axis is degenerate by construction (asserted, not assumed).
(4) The dial CLASSIFICATION (composition vs control) is pre-registered in this docstring
before any number was read.

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights   # noqa
from engine import backtest, metrics                                      # noqa

SLUG = "2026-09-07_the-IS-chooser-prefers-SPY-where-OOS-prefers-QQQ_B"
OUT = ROOT / "research" / "backtests"
IDEA30 = OUT / "2026-09-07_qqq-core-plus-sleeve-h1_B.grid.csv"
FREQ = "W"
COSTS = [0, 10, 25]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
FOLDS = [("F1", None, "2013-12-31", "2014-01-01", "2016-12-31"),
         ("F2", None, "2016-12-31", "2017-01-01", "2020-12-31"),
         ("F3", None, "2020-12-31", "2021-01-01", None)]

# ---------------------------------------------------------------- idea-18/24 macro sleeve
MACRO = ["SPY", "QQQ", "IWM", "EFA", "EEM", "TLT", "GLD", "DBC", "UUP"]
SLEEVE_EQ = ["SPY", "QQQ", "IWM", "EFA", "EEM"]
MOM_LAGS = (252, 126, 63)
VOL_WINDOW, MA_WINDOW = 60, 200
SECTORS = ["XLK", "XLF", "XLV", "XLE", "XLI", "XLY", "XLP", "XLU", "XLB", "XLRE", "XLC"]
TILT = "XLK"


def _risk_parity(sub):
    vol = sub.pct_change().rolling(VOL_WINDOW).std()
    inv = 1.0 / vol.replace(0.0, np.nan)
    return inv.div(inv.sum(axis=1), axis=0)


def _vote_mom(sub):
    sig = [sub.shift(21) / sub.shift(MOM_LAGS[0]) - 1,
           sub / sub.shift(MOM_LAGS[1]) - 1,
           sub / sub.shift(MOM_LAGS[2]) - 1]
    return sum((s > 0).astype(float).where(s.notna()) for s in sig) / len(sig)


def sleeve_b_weights(px):
    """idea 18 variant B, copied verbatim through idea 24 and idea 30."""
    sub = px[MACRO]
    w = (_vote_mom(sub) * _risk_parity(sub)).fillna(0.0)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[MACRO] = w
    return out


def sleeve_membership_weights(px, q):
    """C4: idea-18 sleeve with the five EQUITY legs scaled by q, the whole sleeve then
    renormalised back to its q=1 daily gross so the dial changes MEMBERSHIP, not size.
    q=1 is exactly sleeve_b_weights; q=0 drops the equity legs into the macro four."""
    base = sleeve_b_weights(px)[MACRO]
    tilt = base.copy()
    tilt[SLEEVE_EQ] = tilt[SLEEVE_EQ] * q
    g0, g1 = base.sum(axis=1), tilt.sum(axis=1)
    scaled = tilt.mul((g0 / g1.replace(0.0, np.nan)).fillna(0.0), axis=0)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[MACRO] = scaled.fillna(0.0)
    return out


def core_leg(px, ticker, frac, gate=True):
    p = px[ticker]
    if gate:
        ma = p.rolling(MA_WINDOW).mean()
        on = (p > ma).astype(float).where(ma.notna(), 0.0)
    else:
        on = pd.Series(1.0, index=px.index)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[ticker] = frac * on
    return out


def core_blend(px, q, hi, lo, c=0.60, gate=True):
    """C1/C2/C3: c of NAV in a gated two-ETF core (q in `hi`, 1-q in `lo`), 1-c in the sleeve."""
    return (core_leg(px, hi, c * q, gate) + core_leg(px, lo, c * (1.0 - q), gate)
            + (1.0 - c) * sleeve_b_weights(px))


def book_blend(px, q, gross=0.75):
    """C5: q of NAV following RULES v1 (n=5, gross 0.75), 1-q following RULES v2."""
    return q * rules_v1_weights(px, n=5, w=gross / 5.0) + (1.0 - q) * rules_v2_weights(px, gross=gross)


def sector_tilt(px, q, gross=0.75):
    """C6: gross across the 11 sector ETFs, q of it in XLK and 1-q spread equally over the
    other ten (only names priced that day)."""
    cols = [c for c in SECTORS if c in px.columns]
    others = [c for c in cols if c != TILT]
    avail = px[cols].notna()
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    t_ok = avail[TILT].astype(float)
    n_o = avail[others].sum(axis=1).replace(0, np.nan)
    out[TILT] = gross * q * t_ok
    share = gross * (1.0 - q * t_ok) / n_o
    for c in others:
        out[c] = (share * avail[c].astype(float)).fillna(0.0)
    return out.fillna(0.0)


# ---------------------------------------------------------------- dial registry
def _f(fn):
    return fn


DIALS = [
    # (key, class, label, [(native, q_norm, weights_fn)], anchor_native, description)
    ("C1", "composition", "core-QQQ-vs-SPY (c=0.60 gated + 0.40 sleeve)",
     [(q, q, (lambda px, q=q: core_blend(px, q, "QQQ", "SPY"))) for q in (0.0, 0.25, 0.5, 0.75, 1.0)],
     1.0, "q = QQQ share of the core; q=1 is idea 24 variant B (anchor)"),
    ("C2", "composition", "core-QQQ-vs-IWM (c=0.60 gated + 0.40 sleeve)",
     [(q, q, (lambda px, q=q: core_blend(px, q, "QQQ", "IWM"))) for q in (0.0, 0.25, 0.5, 0.75, 1.0)],
     1.0, "q = QQQ share of the core, the rest small caps"),
    ("C3", "composition", "core-SPY-vs-EFA (c=0.60 gated + 0.40 sleeve)",
     [(q, q, (lambda px, q=q: core_blend(px, q, "SPY", "EFA"))) for q in (0.0, 0.25, 0.5, 0.75, 1.0)],
     1.0, "q = US share of the core, the rest developed ex-US"),
    ("C4", "composition", "sleeve-equity-membership (0.60 gated QQQ core + 0.40 sleeve)",
     [(q, q, (lambda px, q=q: core_leg(px, "QQQ", 0.60, True) + 0.40 * sleeve_membership_weights(px, q)))
      for q in (0.0, 0.25, 0.5, 0.75, 1.0)],
     1.0, "q = weight multiplier on the sleeve's five equity legs, gross held at the q=1 level"),
    ("C5", "composition", "book-blend RULES v1 vs RULES v2 (gross 0.75 both)",
     [(q, q, (lambda px, q=q: book_blend(px, q))) for q in (0.0, 0.25, 0.5, 0.75, 1.0)],
     0.0, "q = share of NAV run by RULES v1; q=0 is the live book (anchor)"),
    ("C6", "composition", "sector-tilt XLK vs the other ten (gross 0.75)",
     [(q, i / 4.0, (lambda px, q=q: sector_tilt(px, q)))
      for i, q in enumerate((0.0, 1.0 / 11.0, 0.25, 0.50, 1.00))],
     1.0 / 11.0, "q = XLK's share of gross; q=1/11 is the equal-weight anchor"),
    ("W1", "control-width", "width n (RULES v1, gross 0.75)",
     [(n, i / 4.0, (lambda px, n=n: rules_v1_weights(px, n=n, w=0.75 / n)))
      for i, n in enumerate((3, 5, 8, 12, 20))],
     5, "n = number of ranked positions; n=5 is the RULES v1 anchor"),
    ("W2", "control-width", "width band (RULES v2, gross 0.75)",
     [(b, i / 4.0, (lambda px, b=b: rules_v2_weights(px, band=b, gross=0.75)))
      for i, b in enumerate((0.00, 0.03, 0.06, 0.12, 0.20))],
     0.03, "band = 200d hysteresis half-width; 0.03 is the live RULES v2 anchor"),
    ("G1", "control-gross", "gross (RULES v2, band 0.03)",
     [(g, i / 4.0, (lambda px, g=g: rules_v2_weights(px, band=0.03, gross=g)))
      for i, g in enumerate((0.20, 0.40, 0.60, 0.80, 1.00))],
     0.75, "gross = total NAV deployed; the live book is 0.75, off-grid by construction"),
]


# ---------------------------------------------------------------- metric helpers
def hs(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_4b(r, spy):
    """PROTOCOL 4b: Sharpe > SPY in BOTH halves AND OOS, |MaxDD| <= 60% of SPY's, CAGR >= 70%."""
    m, ms = metrics(r), metrics(spy)
    h1, h2 = hs(r); s1, s2 = hs(spy)
    o = metrics(r.loc[OOS_START:])["Sharpe"] - metrics(spy.loc[OOS_START:])["Sharpe"]
    d = {"H1": h1 - s1, "H2": h2 - s2, "OOS": o,
         "DD": 0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"]),
         "CAGR": m["CAGR"] - 0.70 * ms["CAGR"]}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


def bars_4a(r, base):
    """PROTOCOL 4a: Sharpe > live book in BOTH halves and MaxDD no worse than the live book."""
    m, mb = metrics(r), metrics(base)
    h1, h2 = hs(r); b1, b2 = hs(base)
    d = {"H1": h1 - b1, "H2": h2 - b2, "DD": abs(mb["MaxDD"]) - abs(m["MaxDD"])}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ra = pd.Series(a).rank().values; rb = pd.Series(b).rank().values
    if ra.std() == 0 or rb.std() == 0: return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


def run(px, w, cost, start):
    res = backtest(px, w, cost_bps=cost, freq=FREQ)
    return res["returns"].loc[start:], res["turnover"].loc[start:], res["weights"].loc[start:].sum(axis=1)


def win(r, lo, hi):
    return r.loc[(lo or r.index[0]):(hi or r.index[-1])]


# ---------------------------------------------------------------- main
def main():
    lines = []

    def log(s=""):
        print(s); lines.append(str(s))

    log("#" * 108)
    log("IDEA 371 -- is the rule-8 IS->OOS ordering inversion a COMPOSITION-dial property?")
    log("Pre-registered classification: C1-C6 composition, W1/W2 width, G1 gross.  "
        "One tuned parameter per dial.")
    log("#" * 108)

    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    grid_rows, ord_rows, wf_rows, fold_rows = [], [], [], []

    for pname, px in panels.items():
        wknd = int((px.index.dayofweek >= 5).sum())
        assert wknd == 0, f"{pname}: expected the corrected trading-day tape, {wknd} weekend rows"
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        ms = metrics(spy); s1, s2 = hs(spy); so = metrics(spy.loc[OOS_START:])
        log("\n" + "#" * 108)
        log(f"### PANEL {pname}: {px.shape[1]} cols, {px.index[0].date()} -> {px.index[-1].date()}, "
            f"eval from {start.date()} ({wknd} weekend rows)")
        log(f"    SPY CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%} "
            f"H1/H2 {s1:.3f}/{s2:.3f} | OOS CAGR {so['CAGR']:.2%} Sharpe {so['Sharpe']:.3f} "
            f"MaxDD {so['MaxDD']:.2%}")
        log(f"    4b bars: H1>{s1:.3f} H2>{s2:.3f} OOS>{so['Sharpe']:.3f} "
            f"|MaxDD|<={0.60 * abs(ms['MaxDD']):.2%} CAGR>={0.70 * ms['CAGR']:.2%}")

        for cost in COSTS:
            base, _, _ = run(px, rules_v2_weights(px), cost, start)
            mb = metrics(base); b1, b2 = hs(base); bo = metrics(base.loc[OOS_START:])
            log("\n" + "=" * 108)
            log(f"[B] DIAL GRID -- panel {pname} @ {cost} bps.  RULES v2 (live, 4a comparand): "
                f"CAGR {mb['CAGR']:.2%} Sharpe {mb['Sharpe']:.3f} MaxDD {mb['MaxDD']:.2%} "
                f"H1/H2 {b1:.3f}/{b2:.3f} | OOS Sharpe {bo['Sharpe']:.3f}")

            for key, klass, label, points, anchor, note in DIALS:
                tab, series = [], {}
                for native, qn, fn in points:
                    r, t, g = run(px, fn(px), cost, start)
                    series[native] = r
                    m = metrics(r); h1, h2 = hs(r)
                    mi, mo = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
                    ok4b, d4b, f4b = bars_4b(r, spy)
                    ok4a, d4a, f4a = bars_4a(r, base)
                    rec = dict(panel=pname, cost=cost, dial=key, dial_class=klass, dial_label=label,
                               param=native, q_norm=qn, is_anchor=int(native == anchor),
                               CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], Vol=m["Vol"],
                               H1=h1, H2=h2,
                               IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                               OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                               turnover=t.sum() / (len(r) / 252), gross=g.mean(),
                               pass4a=int(ok4a), fail4a="+".join(f4a) or "-",
                               pass4b=int(ok4b), fail4b="+".join(f4b) or "-",
                               m4b_H1=d4b["H1"], m4b_H2=d4b["H2"], m4b_OOS=d4b["OOS"],
                               m4b_DD=d4b["DD"], m4b_CAGR=d4b["CAGR"])
                    grid_rows.append(rec)
                    tab.append(dict(param=native, q=round(qn, 3), CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                                    MaxDD=m["MaxDD"], H1=h1, H2=h2, IS_Sh=mi["Sharpe"],
                                    OOS_Sh=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_DD=mo["MaxDD"],
                                    turn=t.sum() / (len(r) / 252),
                                    _4a="PASS" if ok4a else "fail:" + "+".join(f4a),
                                    _4b="PASS" if ok4b else "fail:" + "+".join(f4b),
                                    anchor="<-anchor" if native == anchor else ""))
                log(f"\n--- {key} [{klass}] {label}")
                log(f"    {note}")
                log(pd.DataFrame(tab).to_string(index=False, float_format=lambda x: f"{x:.3f}"))

                # ---- [C] ordering + [D] rule 8 for this dial
                sub = [r for r in grid_rows if r["panel"] == pname and r["cost"] == cost
                       and r["dial"] == key]
                iss = [r["IS_Sharpe"] for r in sub]; oos = [r["OOS_Sharpe"] for r in sub]
                qn = [r["q_norm"] for r in sub]
                rho = spearman(iss, oos)
                is_spread = max(iss) - min(iss)
                pick = max(sub, key=lambda r: r["IS_Sharpe"])
                best = max(sub, key=lambda r: r["OOS_Sharpe"])
                anch = [r for r in sub if r["is_anchor"] == 1]
                anch = anch[0] if anch else None
                worst = min(sub, key=lambda r: r["OOS_Sharpe"])
                # orientation: which end carries the higher realised full-sample vol
                vol_lo, vol_hi = sub[0]["Vol"], sub[-1]["Vol"]
                hi_end_is_vol = vol_hi > vol_lo
                regret = pick["OOS_Sharpe"] - best["OOS_Sharpe"]
                spread = best["OOS_Sharpe"] - worst["OOS_Sharpe"]
                orow = dict(panel=pname, cost=cost, dial=key, dial_class=klass, rho_IS_OOS=rho,
                            IS_spread=is_spread, near_tie=int(is_spread < 0.01),
                            q_IS_star=pick["q_norm"], q_OOS_star=best["q_norm"],
                            dq=pick["q_norm"] - best["q_norm"],
                            IS_Sharpe_pick=pick["IS_Sharpe"], OOS_Sharpe_pick=pick["OOS_Sharpe"],
                            OOS_Sharpe_best=best["OOS_Sharpe"], regret=regret,
                            OOS_spread=spread,
                            regret_frac=regret / spread if spread > 0 else np.nan,
                            OOS_CAGR_pick=pick["OOS_CAGR"], OOS_MaxDD_pick=pick["OOS_MaxDD"],
                            OOS_CAGR_best=best["OOS_CAGR"], OOS_MaxDD_best=best["OOS_MaxDD"],
                            vs_anchor=(pick["OOS_Sharpe"] - anch["OOS_Sharpe"]) if anch else np.nan,
                            anchor_param=anch["param"] if anch else np.nan,
                            OOS_Sharpe_anchor=anch["OOS_Sharpe"] if anch else np.nan,
                            OOS_vs_SPY=pick["OOS_Sharpe"] - so["Sharpe"],
                            OOS_vs_v2=pick["OOS_Sharpe"] - bo["Sharpe"],
                            OOS_SPY_Sharpe=so["Sharpe"], OOS_SPY_CAGR=so["CAGR"],
                            OOS_SPY_MaxDD=so["MaxDD"], OOS_v2_Sharpe=bo["Sharpe"],
                            OOS_v2_CAGR=bo["CAGR"], OOS_v2_MaxDD=bo["MaxDD"],
                            hi_end_higher_vol=int(hi_end_is_vol),
                            IS_undersells_vol_end=int((pick["q_norm"] < best["q_norm"]) == hi_end_is_vol
                                                      and pick["q_norm"] != best["q_norm"]),
                            inverted=int(rho < 0) if rho == rho else 0,
                            pass4a_n=sum(r["pass4a"] for r in sub),
                            pass4b_n=sum(r["pass4b"] for r in sub))
                ord_rows.append(orow)
                wf_rows.append(dict(panel=pname, cost=cost, dial=key, dial_class=klass,
                                    role="IS-Sharpe pick", param=pick["param"],
                                    OOS_CAGR=pick["OOS_CAGR"], OOS_Sharpe=pick["OOS_Sharpe"],
                                    OOS_MaxDD=pick["OOS_MaxDD"],
                                    OOS_SPY_Sharpe=so["Sharpe"], OOS_SPY_CAGR=so["CAGR"],
                                    OOS_SPY_MaxDD=so["MaxDD"], OOS_v2_Sharpe=bo["Sharpe"],
                                    OOS_v2_CAGR=bo["CAGR"], OOS_v2_MaxDD=bo["MaxDD"]))
                for lbl, r in (("OOS-best (hindsight)", best), ("anchor", anch)):
                    if r is None: continue
                    wf_rows.append(dict(panel=pname, cost=cost, dial=key, dial_class=klass, role=lbl,
                                        param=r["param"], OOS_CAGR=r["OOS_CAGR"],
                                        OOS_Sharpe=r["OOS_Sharpe"], OOS_MaxDD=r["OOS_MaxDD"],
                                        OOS_SPY_Sharpe=so["Sharpe"], OOS_SPY_CAGR=so["CAGR"],
                                        OOS_SPY_MaxDD=so["MaxDD"], OOS_v2_Sharpe=bo["Sharpe"],
                                        OOS_v2_CAGR=bo["CAGR"], OOS_v2_MaxDD=bo["MaxDD"]))
                log(f"    [C] Spearman rho(IS Sharpe, OOS Sharpe) over the 5 points = "
                    f"{rho:+.3f}{'   <-- INVERTED' if rho == rho and rho < 0 else ''}"
                    f"   [IS Sharpe spread {is_spread:.3f}"
                    f"{', NEAR-TIE: rho ranks noise' if is_spread < 0.01 else ''}, "
                    f"OOS spread {spread:.3f}]")
                log(f"    [D] rule 8: IS pick param={pick['param']} (IS Sharpe {pick['IS_Sharpe']:.3f}) "
                    f"-> OOS CAGR {pick['OOS_CAGR']:.2%} Sharpe {pick['OOS_Sharpe']:.3f} "
                    f"MaxDD {pick['OOS_MaxDD']:.2%}")
                log(f"        OOS-best param={best['param']} Sharpe {best['OOS_Sharpe']:.3f} "
                    f"| regret {regret:+.3f} ({(regret / spread if spread > 0 else float('nan')):+.1%} of the "
                    f"{spread:.3f} OOS spread)"
                    + (f" | vs anchor param={anch['param']} {pick['OOS_Sharpe'] - anch['OOS_Sharpe']:+.3f}"
                       if anch else ""))
                log(f"        pick vs SPY OOS {pick['OOS_Sharpe'] - so['Sharpe']:+.3f} | "
                    f"vs RULES v2 OOS {pick['OOS_Sharpe'] - bo['Sharpe']:+.3f} | "
                    f"KEEP paths on this dial: 4a {sum(r['pass4a'] for r in sub)}/5, "
                    f"4b {sum(r['pass4b'] for r in sub)}/5")

                # ---- [E] folds
                for fname, tr_lo, tr_hi, te_lo, te_hi in FOLDS:
                    tr = [metrics(win(series[n], tr_lo, tr_hi))["Sharpe"] for n, _, _ in points]
                    te = [metrics(win(series[n], te_lo, te_hi))["Sharpe"] for n, _, _ in points]
                    frho = spearman(tr, te)
                    ip = int(np.argmax(tr)); bp = int(np.argmax(te))
                    fold_rows.append(dict(panel=pname, cost=cost, dial=key, dial_class=klass,
                                          fold=fname, rho=frho,
                                          q_tr_star=points[ip][1], q_te_star=points[bp][1],
                                          param_tr_star=points[ip][0], param_te_star=points[bp][0],
                                          test_Sharpe_pick=te[ip], test_Sharpe_best=te[bp],
                                          regret=te[ip] - te[bp], inverted=int(frho < 0) if frho == frho else 0))

    G = pd.DataFrame(grid_rows); O = pd.DataFrame(ord_rows)
    W = pd.DataFrame(wf_rows); F = pd.DataFrame(fold_rows)
    G.to_csv(OUT / f"{SLUG}.grid.csv", index=False)
    O.to_csv(OUT / f"{SLUG}.ordering.csv", index=False)
    W.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    F.to_csv(OUT / f"{SLUG}.folds.csv", index=False)

    # ------------------------------------------------------------ [A] gate vs idea 30
    log("\n" + "=" * 108)
    log("[A] GATE -- idea 30's committed grid, shared cells (C1 == its c=0.60 GATE=ON column)")
    if IDEA30.exists():
        I30 = pd.read_csv(IDEA30)
        i = I30[(I30.gate == 1) & (I30.c == 0.60)].copy()
        i["q"] = i["q"].round(4)
        mine = G[(G.dial == "C1") & (G.cost.isin([10, 25]))].copy()
        mine["q"] = mine["param"].round(4)
        j = mine.merge(i, on=["panel", "cost", "q"], suffixes=("_new", "_30"))
        assert len(j) == 20, f"expected 20 shared cells (2 panels x 2 rungs x 5 q), got {len(j)}"
        d = {c: float((j[f"{c}_new"] - j[f"{c}_30"]).abs().max())
             for c in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "OOS_CAGR", "IS_Sharpe")}
        log(f"    {len(j)} shared cells; max |new - idea30| = "
            + ", ".join(f"{k} {v:.2e}" for k, v in d.items()))
        assert max(d.values()) < 1e-12, f"GATE FAILED: {d}"
        log("    GATE PASSED (reproduction to <1e-12 on every shared metric).")
        i30q = j.sort_values("q")
        log("    idea 30's headline row reproduced (U56 @10 bps, c=0.60, GATE=ON):")
        log(i30q[i30q.panel.eq("U56") & i30q.cost.eq(10)][
            ["q", "IS_Sharpe_new", "OOS_Sharpe_new", "Sharpe_new", "MaxDD_new"]]
            .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    else:
        log("    idea 30 grid CSV not found -- gate SKIPPED (this must not happen in the repo)")

    # ------------------------------------------------------------ [C] census
    log("\n" + "=" * 108)
    log("[C] ORDERING CENSUS -- rho(IS Sharpe, OOS Sharpe) per dial x panel x cost "
        f"({len(O)} cells, all reported)")
    piv = O.pivot_table(index=["dial", "dial_class"], columns=["panel", "cost"], values="rho_IS_OOS")
    log(piv.to_string(float_format=lambda x: f"{x:+.2f}"))
    log("\n    Regret (OOS Sharpe of the IS pick minus OOS best), same layout:")
    log(O.pivot_table(index=["dial", "dial_class"], columns=["panel", "cost"], values="regret")
        .to_string(float_format=lambda x: f"{x:+.3f}"))

    log("\n    By dial CLASS (pooled over panels and rungs):")
    cls = O.groupby("dial_class").agg(cells=("rho_IS_OOS", "size"),
                                      median_rho=("rho_IS_OOS", "median"),
                                      mean_rho=("rho_IS_OOS", "mean"),
                                      inverted=("inverted", "sum"),
                                      median_regret=("regret", "median"),
                                      mean_regret=("regret", "mean"),
                                      worst_regret=("regret", "min"),
                                      median_regret_frac=("regret_frac", "median"))
    log(cls.to_string(float_format=lambda x: f"{x:.3f}"))
    comp = O[O.dial_class == "composition"]; ctrl = O[O.dial_class != "composition"]
    log(f"\n    COMPOSITION: {len(comp)} cells, rho<0 in {int(comp.inverted.sum())}, "
        f"rho median {comp.rho_IS_OOS.median():+.2f}, regret median {comp.regret.median():+.3f}, "
        f"IS pick == OOS best in {int((comp.dq == 0).sum())}/{len(comp)}")
    log(f"    CONTROL:     {len(ctrl)} cells, rho<0 in {int(ctrl.inverted.sum())}, "
        f"rho median {ctrl.rho_IS_OOS.median():+.2f}, regret median {ctrl.regret.median():+.3f}, "
        f"IS pick == OOS best in {int((ctrl.dq == 0).sum())}/{len(ctrl)}")
    log("\n    Per-dial summary (pooled over the 6 panel x rung cells of each dial):")
    per = O.groupby(["dial", "dial_class"]).agg(median_rho=("rho_IS_OOS", "median"),
                                                inverted=("inverted", "sum"),
                                                median_regret=("regret", "median"),
                                                worst_regret=("regret", "min"),
                                                median_dq=("dq", "median"),
                                                exact_hits=("dq", lambda s: int((s == 0).sum())),
                                                median_vs_anchor=("vs_anchor", "median"))
    log(per.to_string(float_format=lambda x: f"{x:.3f}"))

    log("\n    HOW MUCH SIGNAL IS THERE TO INVERT?  rho is scale-free, so a perfect inversion on a "
        "dial whose\n    IS Sharpes are within noise is not the same failure as one on a dial that "
        "spreads.  IS Sharpe spread\n    (max-min over each dial's 5 points) against OOS spread:")
    log(O.pivot_table(index=["dial", "dial_class"], columns=["panel", "cost"], values="IS_spread")
        .to_string(float_format=lambda x: f"{x:.3f}"))
    log(f"\n    near-ties (IS spread < 0.01): composition {int(comp.near_tie.sum())}/{len(comp)}, "
        f"control {int(ctrl.near_tie.sum())}/{len(ctrl)}")
    ns = O[O.near_tie == 0]
    nsc, nsk = ns[ns.dial_class == "composition"], ns[ns.dial_class != "composition"]
    log(f"    EXCLUDING near-ties: composition {len(nsc)} cells, rho<0 in {int(nsc.inverted.sum())}, "
        f"median rho {nsc.rho_IS_OOS.median():+.2f}, median regret {nsc.regret.median():+.3f}")
    log(f"    EXCLUDING near-ties: control     {len(nsk)} cells, rho<0 in {int(nsk.inverted.sum())}, "
        f"median rho {nsk.rho_IS_OOS.median():+.2f}, median regret {nsk.regret.median():+.3f}")

    log("\n    SIGN of the error: is the IS pick on the LOWER-vol side of the OOS best?")
    log(f"      composition: {int(comp.IS_undersells_vol_end.sum())}/{len(comp)} cells "
        f"(of {int((comp.dq != 0).sum())} where the pick and the OOS best differ)")
    log(f"      control:     {int(ctrl.IS_undersells_vol_end.sum())}/{len(ctrl)} cells "
        f"(of {int((ctrl.dq != 0).sum())} where they differ)")
    log("      dq = q(IS pick) - q(OOS best) in normalised dial units, by dial:")
    log(O.pivot_table(index="dial", columns=["panel", "cost"], values="dq")
        .to_string(float_format=lambda x: f"{x:+.2f}"))

    # is the composition/control gap bigger than the panel or rung effect?
    log("\n    Regret by cost rung and class (the rung is a reported axis, not a tuned one):")
    log(O.pivot_table(index="dial_class", columns="cost", values="regret", aggfunc="median")
        .to_string(float_format=lambda x: f"{x:+.3f}"))

    # ------------------------------------------------------------ [E] folds
    log("\n" + "=" * 108)
    log(f"[E] THREE-FOLD robustness ({len(F)} dial x panel x cost x fold cells)")
    log("    F1 train<=2013 -> test 2014-2016 | F2 train<=2016 -> test 2017-2020 | "
        "F3 train<=2020 -> test 2021-2026")
    log(F.pivot_table(index=["dial", "dial_class"], columns="fold", values="rho", aggfunc="median")
        .to_string(float_format=lambda x: f"{x:+.2f}"))
    log("\n    Median regret by fold and class:")
    log(F.pivot_table(index="dial_class", columns="fold", values="regret", aggfunc="median")
        .to_string(float_format=lambda x: f"{x:+.3f}"))
    log("\n    Inversion count (rho<0) by fold and class:")
    log(F.pivot_table(index="dial_class", columns="fold", values="inverted", aggfunc="sum")
        .to_string())
    fc = F[F.dial_class == "composition"]; fk = F[F.dial_class != "composition"]
    log(f"\n    Pooled over all folds: composition rho median {fc.rho.median():+.3f}, "
        f"inverted {int(fc.inverted.sum())}/{len(fc)}, regret median {fc.regret.median():+.3f}")
    log(f"    Pooled over all folds: control     rho median {fk.rho.median():+.3f}, "
        f"inverted {int(fk.inverted.sum())}/{len(fk)}, regret median {fk.regret.median():+.3f}")
    log("\n    Per-dial fold detail (is any single dial's inversion reproducible across folds?):")
    log(F.pivot_table(index=["dial", "panel"], columns=["cost", "fold"], values="rho")
        .to_string(float_format=lambda x: f"{x:+.2f}"))

    # ------------------------------------------------------------ KEEP paths
    log("\n" + "=" * 108)
    log(f"[KEEP] census over all {len(G)} grid points (both paths at every point)")
    log(G.groupby(["panel", "cost"])[["pass4a", "pass4b"]].agg(["sum", "count"]).to_string())
    log("\n    by dial:")
    log(G.groupby(["dial", "dial_class"])[["pass4a", "pass4b"]].sum().to_string())
    log(f"\n    4a passes anywhere: {int(G.pass4a.sum())}/{len(G)};  "
        f"4b passes anywhere: {int(G.pass4b.sum())}/{len(G)}")
    # Two grid points ARE the live book by construction (C5 q=0 and W2 band=0.03, both gross 0.75).
    # They "pass" 4a by tying with themselves; that is an identity check, not a result.
    ident = G[((G.dial == "C5") & (G.param == 0.0)) | ((G.dial == "W2") & (G.param == 0.03))]
    dup = ident.merge(G[["panel", "cost", "dial", "param", "Sharpe"]], on=["panel", "cost"],
                      suffixes=("", "_o"))
    log("\n    IDENTITY CHECK: C5 q=0 and W2 band=0.03 are both rules_v2(band=0.03, gross=0.75), "
        "i.e. the live book.")
    pair = ident.pivot_table(index=["panel", "cost"], columns="dial", values=["Sharpe", "CAGR", "MaxDD"])
    dmax = max(float((pair[m]["C5"] - pair[m]["W2"]).abs().max()) for m in ("Sharpe", "CAGR", "MaxDD"))
    log(f"      max |C5(q=0) - W2(band=0.03)| over Sharpe/CAGR/MaxDD on all 6 panel x rung cells: "
        f"{dmax:.2e}  -> they are the same book")
    log(f"      those {len(ident)} cells 'pass' 4a by tying with the comparand.  "
        f"NON-DEGENERATE 4a passes: {int(G.pass4a.sum()) - int(ident.pass4a.sum())}/"
        f"{len(G) - len(ident)}")
    nd = G[(G.pass4a == 1) & ~G.index.isin(ident.index)]
    if len(nd):
        log(nd[["panel", "cost", "dial", "param", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                "OOS_Sharpe", "fail4b"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    log("\n    First failing 4b bar, census over all failures:")
    log(G[G.pass4b == 0].groupby("fail4b").size().sort_values(ascending=False).to_string())
    if G.pass4b.sum():
        log("\n    Every 4b-passing point:")
        log(G[G.pass4b == 1][["panel", "cost", "dial", "param", "CAGR", "Sharpe", "MaxDD",
                              "H1", "H2", "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "turnover"]]
            .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
        log("\n    Is any 4b passer SELECTABLE by rule 8 (i.e. is it the IS pick of its dial)?")
        sel = []
        for _, r in G[G.pass4b == 1].iterrows():
            o = O[(O.panel == r.panel) & (O.cost == r.cost) & (O.dial == r.dial)].iloc[0]
            pick = G[(G.panel == r.panel) & (G.cost == r.cost) & (G.dial == r.dial)]
            pick = pick.loc[pick.IS_Sharpe.idxmax()]
            sel.append(dict(panel=r.panel, cost=r.cost, dial=r.dial, param=r.param,
                            IS_pick_param=pick.param, selected=int(pick.param == r.param),
                            pick_pass4b=int(pick.pass4b)))
        S = pd.DataFrame(sel)
        log(S.to_string(index=False))
        log(f"    -> rule 8 selects the 4b passer in {int(S.selected.sum())}/{len(S)} cases; "
            f"the IS pick itself clears 4b in {int(S.pick_pass4b.sum())}/{len(S)}")

    # ------------------------------------------------------------ panel degeneracy
    log("\n" + "=" * 108)
    log("[X] Panel-degeneracy check (C1-C4 hold only ETFs present in both panels)")
    a = G[G.panel == "U56"].set_index(["cost", "dial", "param"])[["CAGR", "Sharpe", "MaxDD", "H1", "H2"]]
    b = G[G.panel == "B136"].set_index(["cost", "dial", "param"])[["CAGR", "Sharpe", "MaxDD", "H1", "H2"]]
    d = (a - b).abs().groupby("dial").max()
    log(d.to_string(float_format=lambda x: f"{x:.2e}"))
    log("    C1-C4 and C6 are ETF-only books: their panel axis is price-file rounding, NOT an "
        "independent confirmation.  C5, W1, W2 and G1 are panel-sensitive.")

    (OUT / f"{SLUG}.console.txt").write_text("\n".join(lines) + "\n")
    print(f"\nwrote {SLUG}.grid.csv ({len(G)}), .ordering.csv ({len(O)}), "
          f".walkforward.csv ({len(W)}), .folds.csv ({len(F)}), .console.txt")


if __name__ == "__main__":
    main()
