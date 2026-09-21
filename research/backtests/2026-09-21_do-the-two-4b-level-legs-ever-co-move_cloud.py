#!/usr/bin/env python3
"""Idea 908 (lane cloud, 2026-09-21) — IS THERE ANY DIAL ON WHICH THE TWO 4b *LEVEL* LEGS
MOVE THE SAME WAY, OR IS EVERY PASS BOUGHT BY TRADING ONE LEG FOR THE OTHER?

THE QUESTION.  PROTOCOL path 4b has three RATIO legs (H1 / H2 / OOS Sharpe vs SPY) and two
LEVEL legs: L4_DD (|MaxDD| <= 0.60 x |SPY|) and L5_CAGR (CAGR >= 0.70 x SPY).  Idea 887 turned
one dial, k/n, and found the two level legs EXACTLY anti-monotone (rho +1.000 / -1.000 under
DEGROSS; 0 of 90 slices agreeing in sign), i.e. every 4b pass it found sits where the dial has
already stopped buying.  Today's idea 2042 (lane cloud, same run) independently found the same
two legs are the BINDING ones at 48 of 48 passing-cell readings and that no 4b pass in its grid
survives its own error bar.  So the axis matters: if some dial moves BOTH level legs in the
passing direction, that dial is where a capital-worthy book can live.  This run searches eight
dials on two panels under both weight conventions and reports whether ANY exists.

THE TWO TUNED PARAMETERS (PROTOCOL rule 4; every grid point reported, none hidden):
    P1  dial  which ladder is turned        {GROSS, BAND, COUNT, MAXVOL, VOLTGT, MALEN, QELIG, CADENCE}
    P2  rung  where on that ladder          (4-6 rungs per dial; every rung published)
    These are ALSO the two dials the rule-8 chooser is allowed to pick over, so rule 8 is a test
    of this run's own tuning and not an add-on.  Nothing else is tuned.

REPORTED, NOT TUNED: panel {U56, B136}; weight convention {DEGROSS (gated weight -> cash, the
live book's convention), RESPREAD (gated weight re-spread over survivors, gross held)} wherever
a dial has an eligibility gate; cost {10 bps headline, plus a 0 / 25 / 50 bps ladder derived
exactly from turnover, never re-run}; cadence W (the live book's) except on the CADENCE dial.

PRE-REGISTERED BARS, written before any number below was read:
    B1  CO-MOVE.  A dial co-moves if rho_spearman(rung, L4_DD) and rho_spearman(rung, L5_CAGR)
        share a sign with |rho| >= 0.60 on BOTH, on BOTH panels, under every convention it has.
    B2  STEP AGREEMENT.  Adjacent-rung steps where dL4 and dL5 share a sign, >= 0.75 of steps.
    B3  A dial that clears B1 and B2 is reported as an AXIS WORTH TURNING only if some rung on
        it also clears 4b outright (all five legs) at 10 bps with next-day execution.
    A dial failing B1/B2 is reported as anti-monotone (887's finding replicated on a new axis),
    which is a KILL of that axis, not of the dial's book.

PROTOCOL: rule 2 (10 bps, t+1 via engine.backtest, gross <= 1.00, no shorting/leverage); rule 3
(live RULES v2 AND SPY at every cell); rule 4 (BOTH KEEP paths at every cell, <= 2 tuned
parameters, all grid points reported); rule 5 (one idea, deterministic, standalone); rule 8
(walk-forward: (dial, rung) chosen on 2009-2016 ONLY by pre-registered IS-only choosers,
2017-2026 read exactly once); rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py,
bot.py and baseline.py are NOT modified.

SURVIVORSHIP.  U56 and B136 are CURRENT-constituent lists, so CAGR and MaxDD LEVELS are
optimistic and both 4b level bars are easier than on a point-in-time panel.  The co-movement
question is about the SIGN of a within-panel gradient and is first-order robust to that; the
pass counts are not.

Runs standalone and offline (committed caches only):
  python research/backtests/2026-09-21_do-the-two-4b-level-legs-ever-co-move_cloud.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state     # noqa: E402
from engine import backtest as engine_backtest                        # noqa: E402

DATE, SLUG, LANE = "2026-09-21", "do-the-two-4b-level-legs-ever-co-move", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"
WARMUP, COST_BPS = 260, 10.0
OOS_START, IS_END = "2017-01-01", "2016-12-31"
LINES: list[str] = []


def P(s: str = "") -> None:
    print(s)
    LINES.append(s)


def sharpe(r):
    sd = np.std(r, ddof=1)
    return float(np.mean(r) / sd * np.sqrt(252.0)) if sd > 0 else 0.0


def cagr(r):
    return float(np.exp(np.log1p(r).sum() * (252.0 / len(r))) - 1.0)


def maxdd(r):
    eq = np.cumprod(1.0 + r)
    return float((eq / np.maximum.accumulate(eq) - 1.0).min())


# ------------------------------------------------------------------ weight builders
def _spread(elig: pd.DataFrame, px: pd.DataFrame, gross: float, conv: str) -> pd.DataFrame:
    """elig is a 0/1 frame. DEGROSS: gross/N_priced per held name (rest to cash).
    RESPREAD: gross/N_eligible per held name (gross held constant whenever anything is held)."""
    priced = px.notna().astype(float)
    e = elig.astype(float) * priced
    den = priced.sum(axis=1) if conv == "DEGROSS" else e.sum(axis=1)
    return gross * e.div(den.replace(0, np.nan), axis=0).fillna(0.0)


def _mom(px):      return px.shift(21) / px.shift(252) - 1.0
def _r6(px):       return px / px.shift(126) - 1.0
def _vol20(px):    return px.pct_change().rolling(20).std() * np.sqrt(252.0)


def w_gross(px, g, conv="DEGROSS"):
    return rules_v2_weights(px, band=0.03, gross=g)


def w_band(px, c, conv):
    return _spread(band_state(px, c), px, 0.75, conv)


def w_count(px, n, conv):
    elig = band_state(px, 0.03)
    rank = _mom(px).where(elig).rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    if conv == "DEGROSS":                       # short of n names -> the rest is cash
        return 0.75 * sel / float(n)
    return _spread(sel > 0, px, 0.75, "RESPREAD")


def w_maxvol(px, m, conv):
    return _spread(band_state(px, 0.03) & (_vol20(px) < m), px, 0.75, conv)


def w_qelig(px, q, conv):
    r6 = _r6(px)
    thr = r6.quantile(q / 100.0, axis=1)
    return _spread(band_state(px, 0.03) & r6.ge(thr, axis=0), px, 0.75, conv)


def w_malen(px, L, conv):
    ma = px.rolling(int(L)).mean()
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    raw = raw.mask(px > ma * 1.03, 1.0).mask(px < ma * 0.97, 0.0)
    return _spread(raw.ffill().fillna(0.0) > 0.5, px, 0.75, conv)


def w_voltgt(px, tgt, conv="DEGROSS"):
    """Scale the live book's exposure toward a target volatility, capped at gross 1.00
    (rule 2: no leverage).  sigma is the 20d realised vol of the book's own equal-weight
    eligible basket, known at t and applied to weights decided at t (engine trades t+1)."""
    base = _spread(band_state(px, 0.03), px, 1.0, "DEGROSS")
    br = (base.shift(1) * px.pct_change()).sum(axis=1)
    sig = br.rolling(20).std() * np.sqrt(252.0)
    s = (tgt / sig.replace(0, np.nan)).clip(upper=1.0).fillna(0.0)
    return base.mul(s, axis=0)


DIALS = {
    "GROSS":   dict(fn=w_gross,  rungs=[0.25, 0.50, 0.75, 1.00], conv=["DEGROSS"], freq="W",
                    label="gross of NAV, band 0.03"),
    "BAND":    dict(fn=w_band,   rungs=[0.00, 0.02, 0.04, 0.06, 0.08, 0.12], conv=["DEGROSS", "RESPREAD"],
                    freq="W", label="200d band half-width c, gross 0.75"),
    "COUNT":   dict(fn=w_count,  rungs=[5, 10, 20, 40, 80], conv=["DEGROSS", "RESPREAD"], freq="W",
                    label="top-n by 12-1 momentum inside the band, gross 0.75"),
    "MAXVOL":  dict(fn=w_maxvol, rungs=[0.30, 0.45, 0.60, 0.80, 1.20], conv=["DEGROSS", "RESPREAD"],
                    freq="W", label="vol20 ceiling m, gross 0.75"),
    "VOLTGT":  dict(fn=w_voltgt, rungs=[0.06, 0.08, 0.10, 0.14, 0.20], conv=["DEGROSS"], freq="W",
                    label="book vol target, exposure capped at 1.00"),
    "MALEN":   dict(fn=w_malen,  rungs=[50, 100, 150, 200, 300], conv=["DEGROSS", "RESPREAD"], freq="W",
                    label="trend window length, band 3%, gross 0.75"),
    "QELIG":   dict(fn=w_qelig,  rungs=[0, 25, 50, 75, 90], conv=["DEGROSS", "RESPREAD"], freq="W",
                    label="6m-return percentile floor q, gross 0.75"),
    "CADENCE": dict(fn=None,     rungs=["D", "W", "M", "Q"], conv=["DEGROSS"], freq=None,
                    label="rebalance cadence, band 0.03, gross 0.75"),
}


def main() -> None:
    P(__doc__.strip())
    P("\n" + "=" * 104)
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    idx = panels["U56"].index
    start = idx[WARMUP]
    dates = idx[idx >= start]
    n = len(dates)
    half = n // 2
    W = dict(FULL=np.arange(n), H1=np.arange(half), H2=np.arange(half, n),
             OOS=np.where(dates >= pd.Timestamp(OOS_START))[0],
             IS=np.where(dates <= pd.Timestamp(IS_END))[0])
    spy = panels["U56"]["SPY"].pct_change().fillna(0.0).loc[start:].to_numpy()
    base = {p: engine_backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq="W")["returns"].loc[start:].to_numpy()
            for p, px in panels.items()}
    P(f"Sample {dates[0].date()} .. {dates[-1].date()} ({n} days after {WARMUP}-day warm-up); "
      f"IS <= {IS_END} ({len(W['IS'])}), OOS >= {OOS_START} ({len(W['OOS'])}).")
    P(f"SPY: CAGR {cagr(spy):.2%}  Sharpe {sharpe(spy):.4f}  MaxDD {maxdd(spy):.2%}  "
      f"H1 {sharpe(spy[W['H1']]):.4f}  H2 {sharpe(spy[W['H2']]):.4f}  OOS {sharpe(spy[W['OOS']]):.4f} / "
      f"CAGR {cagr(spy[W['OOS']]):.2%} / MaxDD {maxdd(spy[W['OOS']]):.2%}")
    for p in panels:
        b = base[p]
        P(f"RULES v2 live ({p}): CAGR {cagr(b):.2%}  Sharpe {sharpe(b):.4f}  MaxDD {maxdd(b):.2%}  "
          f"H1 {sharpe(b[W['H1']]):.4f}  H2 {sharpe(b[W['H2']]):.4f}  OOS {sharpe(b[W['OOS']]):.4f} / "
          f"CAGR {cagr(b[W['OOS']]):.2%} / MaxDD {maxdd(b[W['OOS']]):.2%}")

    rows, ret = [], {}
    for pname, px in panels.items():
        for dial, spec in DIALS.items():
            for conv in spec["conv"]:
                for k, rung in enumerate(spec["rungs"]):
                    if dial == "CADENCE":
                        w, freq = rules_v2_weights(px, band=0.03, gross=0.75), rung
                    else:
                        w, freq = spec["fn"](px, rung, conv), spec["freq"]
                    res = engine_backtest(px, w, cost_bps=COST_BPS, freq=freq)
                    r = res["returns"].loc[start:].to_numpy()
                    tno = float(res["turnover"].loc[start:].mean() * 252)
                    key = (pname, dial, conv, str(rung))
                    ret[key] = r
                    b = base[pname]
                    row = dict(panel=pname, dial=dial, conv=conv, rung=str(rung), k=k,
                               CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r),
                               H1=sharpe(r[W["H1"]]), H2=sharpe(r[W["H2"]]),
                               OOS_CAGR=cagr(r[W["OOS"]]), OOS_Sharpe=sharpe(r[W["OOS"]]),
                               OOS_MaxDD=maxdd(r[W["OOS"]]), IS_Sharpe=sharpe(r[W["IS"]]), turn=tno,
                               L1_H1=sharpe(r[W["H1"]]) - sharpe(spy[W["H1"]]),
                               L2_H2=sharpe(r[W["H2"]]) - sharpe(spy[W["H2"]]),
                               L3_OOS=sharpe(r[W["OOS"]]) - sharpe(spy[W["OOS"]]),
                               L4_DD=0.60 * abs(maxdd(spy)) - abs(maxdd(r)),
                               L5_CAGR=cagr(r) - 0.70 * cagr(spy))
                    row["pass4b"] = all(row[x] > 0 for x in ("L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"))
                    row["pass4a"] = (row["H1"] > sharpe(b[W["H1"]]) and row["H2"] > sharpe(b[W["H2"]])
                                     and row["MaxDD"] >= maxdd(b))
                    # exact cost ladder: r_c = r_10 + turnover*(10-c)/1e4 (derived, never re-run)
                    tser = res["turnover"].loc[start:].to_numpy()
                    for c in (0, 25, 50):
                        rc = r + tser * (COST_BPS - c) / 1e4
                        row[f"L4_DD@{c}"] = 0.60 * abs(maxdd(spy)) - abs(maxdd(rc))
                        row[f"L5_CAGR@{c}"] = cagr(rc) - 0.70 * cagr(spy)
                    rows.append(row)
    cells = pd.DataFrame(rows)
    cells.to_csv(f"{OUT}.cells.csv", index=False)

    P("\n" + "-" * 104)
    P(f"SECTION 1 — EVERY RUNG ({len(cells)} books: 2 panels x 8 dials x rungs x conventions), 10 bps, t+1, cadence W "
      "unless the dial IS cadence.")
    for dial, spec in DIALS.items():
        P(f"\n  DIAL {dial} — {spec['label']}")
        s = cells[cells.dial == dial][["panel", "conv", "rung", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                       "OOS_Sharpe", "turn", "L4_DD", "L5_CAGR", "pass4a", "pass4b"]]
        P("    " + s.to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n    "))

    # ------------------------------------------------------------ co-movement
    def spearman(a, b):
        ra, rb = pd.Series(a).rank().to_numpy(), pd.Series(b).rank().to_numpy()
        if np.std(ra) == 0 or np.std(rb) == 0:
            return 0.0
        return float(np.corrcoef(ra, rb)[0, 1])

    P("\n" + "-" * 104)
    P("SECTION 2 — DO THE TWO LEVEL LEGS CO-MOVE?  rho = Spearman(rung index, leg margin); "
      "agree = share of adjacent-rung steps where dL4_DD and dL5_CAGR have the SAME sign.")
    P("  B1 co-move bar: same sign and |rho| >= 0.60 on BOTH legs.   B2: agree >= 0.75.")
    co_rows = []
    for (pn, dial, conv), g in cells.groupby(["panel", "dial", "conv"], sort=False):
        g = g.sort_values("k")
        r4, r5 = spearman(g.k, g.L4_DD), spearman(g.k, g.L5_CAGR)
        d4, d5 = np.diff(g.L4_DD.to_numpy()), np.diff(g.L5_CAGR.to_numpy())
        agree = float(np.mean(np.sign(d4) == np.sign(d5)))
        rec = dict(panel=pn, dial=dial, conv=conv, rho_L4=r4, rho_L5=r5, agree=agree,
                   B1=bool(np.sign(r4) == np.sign(r5) and abs(r4) >= 0.60 and abs(r5) >= 0.60 and r4 != 0),
                   B2=bool(agree >= 0.75), n4b=int(g.pass4b.sum()), nrung=len(g))
        for c in (0, 25, 50):
            rec[f"rho_L4@{c}"] = spearman(g.k, g[f"L4_DD@{c}"])
            rec[f"rho_L5@{c}"] = spearman(g.k, g[f"L5_CAGR@{c}"])
            rec[f"agree@{c}"] = float(np.mean(np.sign(np.diff(g[f"L4_DD@{c}"].to_numpy()))
                                              == np.sign(np.diff(g[f"L5_CAGR@{c}"].to_numpy()))))
        co_rows.append(rec)
    co = pd.DataFrame(co_rows)
    co.to_csv(f"{OUT}.comove.csv", index=False)
    P("\n    " + co[["panel", "dial", "conv", "rho_L4", "rho_L5", "agree", "B1", "B2", "n4b", "nrung"]]
      .to_string(index=False, float_format=lambda x: f"{x:+.3f}").replace("\n", "\n    "))

    P("\n  B1 AND B2 held on EVERY (panel, convention) slice of a dial — the answer to the question:")
    any_dial = False
    for dial in DIALS:
        s = co[co.dial == dial]
        ok = bool(s.B1.all() and s.B2.all())
        any_dial |= ok
        pas = int(cells[(cells.dial == dial)].pass4b.sum())
        P(f"    {dial:<8} co-moves on {int((s.B1 & s.B2).sum())}/{len(s)} slices   "
          f"ALL-SLICE: {'YES' if ok else 'no'}   rungs clearing full 4b: {pas}   "
          f"(rho_L4 {s.rho_L4.min():+.2f}..{s.rho_L4.max():+.2f}, rho_L5 {s.rho_L5.min():+.2f}..{s.rho_L5.max():+.2f})")
    P(f"\n  ANY DIAL CLEARING B1+B2 ON EVERY SLICE: {'YES' if any_dial else 'NO'}")
    P("  Cost-rung robustness of the same reading (0 / 25 / 50 bps, derived exactly from turnover):")
    for c in (0, 25, 50):
        b1 = ((np.sign(co[f"rho_L4@{c}"]) == np.sign(co[f"rho_L5@{c}"]))
              & (co[f"rho_L4@{c}"].abs() >= 0.60) & (co[f"rho_L5@{c}"].abs() >= 0.60))
        P(f"    @{c:>2} bps: slices clearing B1 {int(b1.sum())}/{len(co)}; median agree {co[f'agree@{c}'].median():.3f}")

    # ------------------------------------------------------------ rule 8
    P("\n" + "-" * 104)
    P("SECTION 3 — RULE 8 WALK-FORWARD.  (dial, rung) chosen on 2009-2016 ONLY, 2017-2026 read ONCE.")
    P("  Pre-registered IS-only choosers: C1 = max IS Sharpe; C2 = max IS min-leg margin over the four")
    P("  in-sample-computable 4b legs (IS-half1 Sharpe, IS-half2 Sharpe, IS DD cap, IS CAGR floor).")
    isi = W["IS"]
    ih = len(isi) // 2
    picks_rows = []
    for key, r in ret.items():
        ri, si = r[isi], spy[isi]
        m = [sharpe(ri[:ih]) - sharpe(si[:ih]), sharpe(ri[ih:]) - sharpe(si[ih:]),
             0.60 * abs(maxdd(si)) - abs(maxdd(ri)), cagr(ri) - 0.70 * cagr(si)]
        picks_rows.append(dict(key=key, panel=key[0], dial=key[1], conv=key[2], rung=key[3],
                               IS_Sharpe=sharpe(ri), IS_minleg=min(m)))
    pk = pd.DataFrame(picks_rows)
    oos = W["OOS"]
    P(f"\n    {'chooser / scope':<40}{'pick':<34}{'OOS CAGR':>10}{'OOS Sharpe':>12}{'OOS MaxDD':>11}  4b/4a(full)")
    P(f"    {'SPY':<40}{'':<34}{cagr(spy[oos]):>10.2%}{sharpe(spy[oos]):>12.4f}{maxdd(spy[oos]):>11.2%}")
    for p in panels:
        b = base[p][oos]
        P(f"    {'RULES v2 live (' + p + ')':<40}{'':<34}{cagr(b):>10.2%}{sharpe(b):>12.4f}{maxdd(b):>11.2%}")
    wf = []
    for scope, sub in [("ALL dials", pk)] + [(f"dial={d}", pk[pk.dial == d]) for d in DIALS]:
        for cn, col in (("C1 max IS Sharpe", "IS_Sharpe"), ("C2 max IS min-leg", "IS_minleg")):
            w = sub.loc[sub[col].idxmax()]
            r = ret[w.key][oos]
            row = cells[(cells.panel == w.panel) & (cells.dial == w.dial) & (cells.conv == w.conv)
                        & (cells.rung == w.rung)].iloc[0]
            lab = f"{w.panel}/{w.dial}/{w.conv}/{w.rung}"
            P(f"    {cn + ' | ' + scope:<40}{lab:<34}{cagr(r):>10.2%}{sharpe(r):>12.4f}{maxdd(r):>11.2%}"
              f"  {'PASS' if row.pass4b else 'fail'}/{'PASS' if row.pass4a else 'fail'}")
            wf.append(dict(scope=scope, chooser=cn, pick=lab, OOS_CAGR=cagr(r), OOS_Sharpe=sharpe(r),
                           OOS_MaxDD=maxdd(r), full_pass4b=bool(row.pass4b), full_pass4a=bool(row.pass4a),
                           beats_SPY_OOS_Sharpe=sharpe(r) > sharpe(spy[oos]),
                           beats_base_OOS_Sharpe=sharpe(r) > sharpe(base[w.panel][oos])))
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(f"\n    Of the {len(wfd)} rule-8 picks: {int(wfd.beats_SPY_OOS_Sharpe.sum())} beat SPY's OOS Sharpe, "
      f"{int(wfd.beats_base_OOS_Sharpe.sum())} beat the live book's, "
      f"{int(wfd.full_pass4b.sum())} carry a full-sample 4b pass, {int(wfd.full_pass4a.sum())} a 4a pass.")

    P("\n" + "-" * 104)
    P("SECTION 4 — KEEP PATHS AT EVERY CELL (PROTOCOL rule 4).")
    P(f"  4b passes: {int(cells.pass4b.sum())} of {len(cells)} rungs.  4a passes: {int(cells.pass4a.sum())}.  "
      f"Both: {int((cells.pass4a & cells.pass4b).sum())}.")
    if cells.pass4b.any():
        P("  Rungs clearing 4b:")
        P("    " + cells[cells.pass4b][["panel", "dial", "conv", "rung", "CAGR", "Sharpe", "MaxDD",
                                        "OOS_Sharpe", "L4_DD", "L5_CAGR", "turn"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n    "))
    if cells.pass4a.any():
        P("  Rungs clearing 4a (vs the LIVE book):")
        P("    " + cells[cells.pass4a][["panel", "dial", "conv", "rung", "CAGR", "Sharpe", "MaxDD",
                                        "H1", "H2", "OOS_Sharpe", "turn"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n    "))
    P("\n" + "=" * 104)
    Path(f"{OUT}.txt").write_text("\n".join(LINES) + "\n")
    P("Files: " + ", ".join(Path(f"{OUT}.{x}").name for x in ("cells.csv", "comove.csv", "walkforward.csv", "txt")))


if __name__ == "__main__":
    main()
