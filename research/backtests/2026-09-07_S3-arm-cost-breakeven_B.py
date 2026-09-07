#!/usr/bin/env python3
"""QUEUE idea 108 — S3-arm-cost-breakeven (lane B, 2026-09-07).

Question (as worded in QUEUE.md)
--------------------------------
108: "idea 101's `top20 + 50% (TLT,GLD,UUP)` at g=1.00 holds cross-universe 4b to 15 bps and
dies at 20, with the CAGR floor binding first.  Run idea 82's 0.5 bp breakeven curve on it and
report the walk-forward spread on the breakeven; that number, not the 10 bps assumption, is
what sizing depends on."

So there are exactly three deliverables and one adjudication:
  D1  the 0.5 bp breakeven curve on the S3 arm, both universes, cross-universe breakeven
      (idea 82's definition: min over panels; NaN if either panel never passes).
  D2  WHICH BAR binds at the breakeven — the queue asserts the CAGR floor; that is a claim to
      be tested per rung, not repeated.
  D3  the WALK-FORWARD SPREAD on the breakeven: the breakeven recomputed with the bars
      measured inside rule 8's IS window (2009-2016) and inside its OOS window (2017-2026).
      spread = be_IS - be_OOS.  A positive spread means an IS-fitted cost budget OVERSTATES
      what the arm can actually pay out of sample, and sizing must use be_OOS.
  ADJ the 15/20 bps claim itself, on a 0.5 bp grid instead of idea 101's 5 bps grid.

PRE-REGISTERED, fixed ex ante, NOT selected on any statistic computed here
--------------------------------------------------------------------------
  candidate     `top20 + 50% (TLT,GLD,UUP)` at g = 1.00, weekly, exactly as idea 101 wrote it.
  book          top20 = idea 2's book: equal-weight the top 20 eligible names by the UNSCALED
                composite, gross 0.75 before the g renormalisation (idea 101's `book_top20`).
  sleeve        idea 18 variant B verbatim: trend vote in {0,1/3,2/3,1} on the signs of
                {12-1, 6m, 3m} x inverse-60d-vol risk parity, row-normalised.
  f*            0.50 — the queue's headline fraction, the point under adjudication.
  bars          PROTOCOL 4b as published: phi = 0.70 (CAGR floor), delta = 0.60 (DD cap),
                Sharpe > SPY in H1, H2 and OOS.  4a is judged against RULES v2 (the live book
                since 2026-09-06) at the SAME cost, per PROTOCOL rule 3/4a.
  windows       IS 2009-01-01..2016-12-31, OOS 2017-01-01..end (rule 8, unchanged).

TUNED (2, PROTOCOL rule 4)
--------------------------
  f     in {0.00, 0.25, 0.50, 0.75, 1.00}        (5 points)
  cost  in 0.0 .. 30.0 bps by 0.5                (61 points, idea 82's curve)
ALL 61 x 5 x (2 panels x 2 arms x 2 conventions x 3 cadences) = 36,600 grid points are
computed and written to .grid.csv.gz; every breakeven derived from them is in .breakeven.csv.
Nothing is hidden.

CONTROLS (reported, never selected on): universe in {u56, broad}; arm in {S3 = TLT,GLD,UUP
(pre-registered) and S4 = TLT,GLD,DBC,UUP (idea 100's, carried for continuity)}; gross
convention in {g1.00 (pre-registered), natural}; cadence in {W (pre-registered), M, D}.

COST NOTE (the identity the whole 61-point curve rests on)
----------------------------------------------------------
engine.backtest computes `port = (held*rets).sum(axis=1) - turnover*bps/1e4`, and neither
`held` nor `turnover` depends on bps.  So each weight matrix is run ONCE at 0 bps and every
rung is derived exactly.  Asserted against a direct 10 bps run before any result is read.

REPRODUCTION GATES asserted before any new number is read (a run that cannot reproduce the
committed record has no standing to correct it):
  G1  cost linearity, max |derived - direct| at 10 bps  ->  must be < 1e-12.
  G2  idea 101's committed headline for the S3 arm at g=1.00, W, 10 bps:
      u56 11.5% / 1.167 / -13.3% (OOS Sharpe 1.215 @ 12.3%),
      broad 12.0% / 1.073 / -14.6% (OOS Sharpe 0.985 @ 11.1%).      -> must match to its
      published precision (0.1pp on CAGR/MaxDD, 0.001 on Sharpe).

CAVEATS carried, not buried
---------------------------
  - SURVIVORSHIP (idea 54): u56 and broad are CURRENT-constituent lists, so equity levels are
    biased up.  The bias hits the arm, the f=0 anchor, RULES v2 and the SPY bars unequally
    (SPY is not survivorship-biased), so the ABSOLUTE 4b pass and therefore the absolute
    breakeven are biased UP.  The f-contrast and the IS-vs-OOS spread are much cleaner.
  - Idea 128: the IS window's SPY MaxDD is shallower than the OOS window's, so an IS-measured
    breakeven is biased UP for that reason too.  D3 measures that bias rather than assuming it.
  - Idea 38: data/prices*.csv are on a CALENDAR-day index after 2014-09-17 (BTC-USD in the
    download), so post-2014 weekends are zero-return rows.  Hits every arm identically.
  - A flat bps per unit turnover both ways; no spread/impact/borrow model.  The breakeven is
    therefore an ALL-IN budget, not a commission estimate.

Deterministic, standalone:
    python research/backtests/2026-09-07_S3-arm-cost-breakeven_B.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = Path(__file__).with_suffix("")

# ---- pre-registered constants -------------------------------------------------------------
G_FIXED = 1.00
BOOK_GROSS = 0.75
F_GRID = [0.00, 0.25, 0.50, 0.75, 1.00]
F_STAR = 0.50
COSTS = [round(x, 1) for x in np.arange(0.0, 30.001, 0.5)]      # 61 points, idea 82's curve
COST_HEADLINE = 10.0
ARMS = {"S3": ["TLT", "GLD", "UUP"], "S4": ["TLT", "GLD", "DBC", "UUP"]}
ARM_STAR = "S3"
CONVENTIONS = ("g1.00", "natural")
CADENCES = ("W", "M", "D")
CADENCE_STAR = "W"
PANELS = ("u56", "broad")
PHI0, DELTA0 = 0.70, 0.60
BARS5 = ("H1", "H2", "OOS", "DD", "CAGR")
BARS_W = ("H1", "H2", "DD", "CAGR")                             # inside one window: no OOS bar
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
MOM_LAGS = (252, 126, 63)
VOL_WINDOW = 60

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 4000)

LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ---------------------------------------------------------------- construction (idea 101 verbatim)
def _risk_parity(sub):
    vol = sub.pct_change().rolling(VOL_WINDOW).std()
    inv = 1.0 / vol.replace(0.0, np.nan)
    return inv.div(inv.sum(axis=1), axis=0)


def _vote_mom(sub):
    sig = [sub.shift(21) / sub.shift(MOM_LAGS[0]) - 1,
           sub / sub.shift(MOM_LAGS[1]) - 1,
           sub / sub.shift(MOM_LAGS[2]) - 1]
    return sum((s > 0).astype(float).where(s.notna()) for s in sig) / len(sig)


def sleeve_weights(px, assets):
    sub = px[assets]
    w = (_vote_mom(sub) * _risk_parity(sub)).fillna(0.0)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[assets] = w
    return out


def book_top20(px, n=20):
    s, above, vol20 = score(px, vol_scale=False)
    rank = s.where(above & (vol20 < 0.60)).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (BOOK_GROSS / n)


def blend(E, S, f, conv):
    w = (1 - f) * E + f * S
    if conv == "natural":
        return w
    g = w.sum(axis=1)
    return w.mul((G_FIXED / g.where(g > 1e-12)).fillna(0.0), axis=0)


# ---------------------------------------------------------------- windows / stats
def win(r, which):
    if which == "full":
        return r
    return r.loc[:IS_END] if which == "IS" else r.loc[OOS_START:]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def stats_win(r, which):
    w = win(r, which)
    m = metrics(w)
    h1, h2 = halves(w)
    oos = metrics(r.loc[OOS_START:])["Sharpe"] if which == "full" else m["Sharpe"]
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2, OOS=oos)


def bars_win(spy, which):
    st = stats_win(spy, which)
    return dict(s1=st["H1"], s2=st["H2"], soos=st["OOS"], sdd=st["MaxDD"], scagr=st["CAGR"])


def margins(st, b, phi=PHI0, delta=DELTA0):
    """Positive margin == bar passed.  Same five bars as idea 82."""
    return dict(H1=st["H1"] - b["s1"], H2=st["H2"] - b["s2"], OOS=st["OOS"] - b["soos"],
                DD=delta * abs(b["sdd"]) - abs(st["MaxDD"]),
                CAGR=st["CAGR"] - phi * b["scagr"])


# ---------------------------------------------------------------- grid
def net(gr, to, bps):
    return gr - to * bps / 1e4


def build():
    """One 0-bps backtest per weight matrix; all 61 rungs derived from the cost identity."""
    rows = []
    for pname in PANELS:
        px = load_universe(broad=(pname == "broad"))
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        B = {w: bars_win(spy, w) for w in ("full", "IS", "OOS")}
        say(f"\n--- PANEL {pname}: {px.shape[1]} tickers {px.index[0].date()}->{px.index[-1].date()}"
            f" | eval from {start.date()}")
        say(f"    SPY full {B['full']['scagr']:.2%}/{metrics(spy)['Sharpe']:.3f}/"
            f"{B['full']['sdd']:.2%} halves {B['full']['s1']:.3f}/{B['full']['s2']:.3f} "
            f"OOS {B['full']['soos']:.3f} | IS CAGR {B['IS']['scagr']:.2%} DD {B['IS']['sdd']:.2%}"
            f" | OOS CAGR {B['OOS']['scagr']:.2%} DD {B['OOS']['sdd']:.2%}")

        E = book_top20(px)
        SL = {a: sleeve_weights(px, assets) for a, assets in ARMS.items()}
        for a, assets in ARMS.items():
            miss = [t for t in assets if t not in px.columns]
            if miss:
                raise SystemExit(f"missing sleeve tickers on {pname}: {miss}")

        # baseline: RULES v2 (live), weekly per its definition, and RULES v1 for continuity
        base0 = {}
        for bname, bw in (("v2", rules_v2_weights(px)), ("v1", rules_v1_weights(px))):
            res = backtest(px, bw, cost_bps=0.0, freq="W")
            base0[bname] = (res["returns"].loc[start:], res["turnover"].loc[start:])
        # baseline stats depend only on (panel, cost) — compute the 61 rungs once, not per cell
        V2 = {c: stats_win(net(*base0["v2"], c), "full") for c in COSTS}
        V1 = {c: stats_win(net(*base0["v1"], c), "full") for c in COSTS}

        for arm in ARMS:
            for conv in CONVENTIONS:
                for f in F_GRID:
                    W = blend(E, SL[arm], f, conv)
                    for cad in CADENCES:
                        res = backtest(px, W, cost_bps=0.0, freq=cad)
                        gr, to = res["returns"].loc[start:], res["turnover"].loc[start:]
                        for c in COSTS:
                            r = net(gr, to, c)
                            d = dict(panel=pname, arm=arm, conv=conv, f=f, cad=cad, cost=c,
                                     turnover_yr=float(to.sum() / (len(to) / 252)))
                            for w in ("full", "IS", "OOS"):
                                st = stats_win(r, w)
                                mg = margins(st, B[w])
                                d[f"{w}_CAGR"], d[f"{w}_Sharpe"], d[f"{w}_MaxDD"] = (
                                    st["CAGR"], st["Sharpe"], st["MaxDD"])
                                d[f"{w}_H1"], d[f"{w}_H2"], d[f"{w}_OOSs"] = (
                                    st["H1"], st["H2"], st["OOS"])
                                for k in BARS5:
                                    d[f"{w}_m_{k}"] = mg[k]
                                for k, key in (("s1", "b_s1"), ("s2", "b_s2"), ("soos", "b_soos"),
                                               ("sdd", "b_sdd"), ("scagr", "b_scagr")):
                                    d[f"{w}_{key}"] = B[w][k]
                            # 4a vs RULES v2 at the SAME cost, full sample
                            sv2 = V2[c]
                            d["v2_H1"], d["v2_H2"], d["v2_MaxDD"] = sv2["H1"], sv2["H2"], sv2["MaxDD"]
                            d["v2_Sharpe"], d["v2_CAGR"] = sv2["Sharpe"], sv2["CAGR"]
                            d["pass4a"] = bool(d["full_H1"] > sv2["H1"] and d["full_H2"] > sv2["H2"]
                                               and d["full_MaxDD"] >= sv2["MaxDD"])
                            # 4a against RULES v1 as well — idea 101 predates the v2 switch
                            sv1 = V1[c]
                            d["v1_H1"], d["v1_H2"], d["v1_MaxDD"] = sv1["H1"], sv1["H2"], sv1["MaxDD"]
                            d["pass4a_v1"] = bool(d["full_H1"] > sv1["H1"] and d["full_H2"] > sv1["H2"]
                                                  and d["full_MaxDD"] >= sv1["MaxDD"])
                            rows.append(d)
                say(f"    {pname}/{arm}/{conv}: {len(rows)} rows")
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- breakevens
KEY = ["panel", "arm", "conv", "f", "cad"]


def ok_series(F, w):
    keys = BARS5 if w == "full" else BARS_W
    return pd.DataFrame({k: F[f"{w}_m_{k}"] > 0 for k in keys}).all(axis=1)


def breakevens(F, w="full", label="4b"):
    """Per cell: highest cost on the 0.5 bp grid at which the bar set still passes.

    be = NaN  -> never passes, not even at 0 bps.
    be = 30.0 -> still passing at the top of the grid (right-censored; reported as >=30)."""
    G = F[KEY + ["cost"]].copy()
    G["ok"] = ok_series(F, w).values if w != "4a" else F["pass4a"].values
    rows = []
    for k, d in G.groupby(KEY, sort=False):
        d = d.sort_values("cost")
        o = d.ok.values
        rec = dict(zip(KEY, k), which=label)
        if not o.any():
            rec.update(be=np.nan, n_ok=0, contiguous=np.nan, holes=np.nan, censored=False)
        else:
            idx = np.flatnonzero(o)
            rec.update(be=float(d.cost.values[idx.max()]), n_ok=int(o.sum()),
                       contiguous=bool(idx.max() - idx.min() + 1 == len(idx)),
                       holes=int(idx.max() - idx.min() + 1 - len(idx)),
                       censored=bool(d.cost.values[idx.max()] >= COSTS[-1]))
        rows.append(rec)
    return pd.DataFrame(rows)


def breakevens_4a(F, col="pass4a", label="4a"):
    G = F[KEY + ["cost", col]].copy().rename(columns={col: "ok"})
    rows = []
    for k, d in G.groupby(KEY, sort=False):
        d = d.sort_values("cost")
        o = d.ok.values
        rec = dict(zip(KEY, k), which=label)
        if not o.any():
            rec.update(be=np.nan, n_ok=0, contiguous=np.nan, holes=np.nan, censored=False)
        else:
            idx = np.flatnonzero(o)
            rec.update(be=float(d.cost.values[idx.max()]), n_ok=int(o.sum()),
                       contiguous=bool(idx.max() - idx.min() + 1 == len(idx)),
                       holes=int(idx.max() - idx.min() + 1 - len(idx)),
                       censored=bool(d.cost.values[idx.max()] >= COSTS[-1]))
        rows.append(rec)
    return pd.DataFrame(rows)


def per_bar_breakeven(F, w="full"):
    """For each of the 5 bars separately: the highest cost at which THAT bar alone passes.
    The binding bar at the joint breakeven is the argmin of these."""
    keys = BARS5 if w == "full" else BARS_W
    rows = []
    for k, d in F.groupby(KEY, sort=False):
        d = d.sort_values("cost")
        rec = dict(zip(KEY, k))
        for bar in keys:
            o = (d[f"{w}_m_{bar}"] > 0).values
            rec[f"be_{bar}"] = float(d.cost.values[np.flatnonzero(o).max()]) if o.any() else np.nan
        vals = {b: rec[f"be_{b}"] for b in keys}
        fin = {b: v for b, v in vals.items() if not np.isnan(v)}
        rec["binding"] = (min(fin, key=fin.get) if len(fin) == len(keys)
                          else ("|".join(sorted(b for b in keys if np.isnan(vals[b]))) + " (never)"))
        rec["be_joint"] = (min(vals.values()) if not any(np.isnan(v) for v in vals.values())
                           else np.nan)
        rows.append(rec)
    return pd.DataFrame(rows)


def cross_universe(BE):
    piv = BE.pivot_table(index=["arm", "conv", "f", "cad", "which"], columns="panel",
                         values="be", dropna=False)
    piv["cross"] = piv[list(PANELS)].min(axis=1, skipna=False)
    return piv.reset_index()


# ---------------------------------------------------------------- rule 8
def rule8(F):
    """f chosen on IS Sharpe alone per (panel, arm, conv, cad, cost); OOS evaluated untouched.
    Reports the chosen arm's OOS CAGR/Sharpe/MaxDD against SPY OOS and RULES v2 OOS."""
    rows = []
    for k, d in F.groupby(["panel", "arm", "conv", "cad", "cost"], sort=False):
        pick = d.loc[d["IS_Sharpe"].idxmax()]
        anchor = d[d.f == 0.0].iloc[0]
        star = d[d.f == F_STAR].iloc[0]
        rows.append(dict(panel=k[0], arm=k[1], conv=k[2], cad=k[3], cost=k[4],
                         f_pick=float(pick["f"]), IS_Sharpe=float(pick["IS_Sharpe"]),
                         OOS_CAGR=float(pick["OOS_CAGR"]), OOS_Sharpe=float(pick["OOS_Sharpe"]),
                         OOS_MaxDD=float(pick["OOS_MaxDD"]),
                         spy_OOS_Sharpe=float(pick["OOS_b_soos"]),
                         spy_OOS_CAGR=float(pick["OOS_b_scagr"]),
                         spy_OOS_MaxDD=float(pick["OOS_b_sdd"]),
                         anchor_OOS_Sharpe=float(anchor["OOS_Sharpe"]),
                         star_OOS_Sharpe=float(star["OOS_Sharpe"]),
                         regret=float(star["OOS_Sharpe"] - pick["OOS_Sharpe"]),
                         picks_star=bool(abs(pick["f"] - F_STAR) < 1e-9)))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- main
def main():
    say("=" * 190)
    say("IDEA 108 — S3-arm-cost-breakeven (lane B, 2026-09-07).  Under adjudication: the ALL-IN "
        "cost budget of `top20 + 50% (TLT,GLD,UUP)` at g=1.00, on a 0.5 bp grid, and how much "
        "of that budget survives out of sample.")
    say("=" * 190)

    # ---- G1 cost linearity ----------------------------------------------------------------
    px0 = load_universe()
    st0 = px0.index[260]
    W0 = blend(book_top20(px0), sleeve_weights(px0, ARMS[ARM_STAR]), F_STAR, "g1.00")
    r0 = backtest(px0, W0, cost_bps=0.0, freq="W")
    direct = backtest(px0, W0, cost_bps=COST_HEADLINE, freq="W")["returns"].loc[st0:]
    err = float((net(r0["returns"].loc[st0:], r0["turnover"].loc[st0:], COST_HEADLINE)
                 - direct).abs().max())
    say(f"\n[G1] cost linearity: max |derived - direct| at {COST_HEADLINE} bps = {err:.3e}")
    assert err < 1e-12, "cost is not linear in this engine — the 61-point ladder is invalid"

    say(f"[pre-registered] arm={ARM_STAR} {ARMS[ARM_STAR]} · g={G_FIXED:.2f} · f*={F_STAR} · "
        f"cadence={CADENCE_STAR} · bars phi={PHI0} delta={DELTA0} · grid {COSTS[0]}..{COSTS[-1]}"
        f" bps by 0.5 ({len(COSTS)} rungs) x f {F_GRID}")

    F = build()
    F.to_csv(f"{STEM}.grid.csv.gz", index=False)
    say(f"\n[grid] {len(F)} rows written to {Path(STEM).name}.grid.csv.gz")

    # ---- G2 reproduce idea 101's committed headline ----------------------------------------
    say("\n" + "=" * 190)
    say("G2  REPRODUCTION GATE — idea 101's committed S3 headline (g1.00, W, 10 bps).")
    say("=" * 190)
    claim = {"u56": (0.115, 1.167, -0.133, 1.215, 0.123),
             "broad": (0.120, 1.073, -0.146, 0.985, 0.111)}
    gate_ok = True
    for p, (cc, cs, cd, co, coc) in claim.items():
        row = F[(F.panel == p) & (F.arm == "S3") & (F.conv == "g1.00") & (F.f == F_STAR)
                & (F.cad == "W") & (F.cost == COST_HEADLINE)].iloc[0]
        got = (row.full_CAGR, row.full_Sharpe, row.full_MaxDD, row.OOS_Sharpe, row.OOS_CAGR)
        d = [abs(g - c) for g, c in zip(got, (cc, cs, cd, co, coc))]
        ok = d[0] < 5e-4 and d[1] < 5e-4 and d[2] < 5e-4 and d[3] < 5e-4 and d[4] < 5e-4
        gate_ok &= ok
        say(f"  {p:>5}: committed {cc:.1%}/{cs:.3f}/{cd:.1%} OOS {co:.3f}@{coc:.1%}  |  "
            f"here {got[0]:.1%}/{got[1]:.3f}/{got[2]:.1%} OOS {got[3]:.3f}@{got[4]:.1%}  |  "
            f"max|d| {max(d):.2e}  {'MATCH' if ok else '*** MISMATCH ***'}")
    say(f"  gate: {'PASS' if gate_ok else 'FAIL'} — idea 101 reproduces to its published precision.")
    assert gate_ok, "cannot reproduce idea 101; this run has no standing to correct it"

    # ---- D1 the 0.5 bp breakeven curve ------------------------------------------------------
    say("\n" + "=" * 190)
    say("D1  THE 0.5 bp BREAKEVEN CURVE.  be = highest cost on the 0..30 grid still clearing "
        "all five 4b bars (full sample).  be=30.0 is RIGHT-CENSORED (>=30).  4a is judged vs "
        "RULES v2 at the same cost.")
    say("=" * 190)
    BE4b = breakevens(F, "full", "4b")
    BE4a = breakevens_4a(F)
    BE4a1 = breakevens_4a(F, "pass4a_v1", "4a_v1")
    BEis = breakevens(F, "IS", "4b_IS")
    BEoos = breakevens(F, "OOS", "4b_OOS")
    BE = pd.concat([BE4b, BE4a, BE4a1, BEis, BEoos], ignore_index=True)
    BE.to_csv(f"{STEM}.breakeven.csv", index=False)

    star = ((BE.arm == ARM_STAR) & (BE.conv == "g1.00") & (BE.cad == CADENCE_STAR))
    W3 = ["4b", "4a", "4a_v1"]
    say("\n  [D1a] THE CANDIDATE CELL (S3, g1.00, W) — full-sample 4b and 4a breakeven by f. "
        "4a is judged vs RULES v2 (live since 2026-09-06); 4a_v1 vs RULES v1, the book idea 101 "
        "was written against:")
    t = BE[star & BE.which.isin(W3)].pivot_table(index=["f"], columns=["which", "panel"],
                                                 values="be", dropna=False)
    say(t.to_string(float_format=lambda x: f"{x:.1f}", na_rep="never"))
    X = cross_universe(BE[star & BE.which.isin(W3)])
    say("\n  cross-universe breakeven (min over u56/broad, idea 82's definition):")
    say(X[["which", "f", "u56", "broad", "cross"]].sort_values(["which", "f"])
        .to_string(index=False, float_format=lambda x: f"{x:.1f}", na_rep="never"))

    at_star = BE[star & (BE.f == F_STAR) & (BE.which == "4b")]
    cu = float(at_star[at_star.panel == "u56"].be.iloc[0])
    cb = float(at_star[at_star.panel == "broad"].be.iloc[0])
    cross_be = min(cu, cb)
    say(f"\n  >>> ADJUDICATION of idea 101's '4b to 15 bps, dies at 20': on the 0.5 bp grid the "
        f"S3 arm at f=0.50 breaks at u56 {cu:.1f} bps / broad {cb:.1f} bps, "
        f"cross-universe c* = {cross_be:.1f} bps.")
    say(f"      Idea 101's 5-bps grid could only bracket this to (15, 20]; the true value is "
        f"{cross_be:.1f}.  Contiguity holes at f=0.50: "
        f"{at_star.holes.tolist()} (0 = the pass region is one interval, as a cost curve "
        f"must be if it is monotone).")

    say("\n  [D1b] ALL cells, full-sample 4b breakeven (arm x conv x cad x f x panel) — nothing hidden:")
    full = BE[BE.which == "4b"].pivot_table(index=["arm", "conv", "cad", "f"], columns="panel",
                                            values="be", dropna=False)
    full["cross"] = full[list(PANELS)].min(axis=1, skipna=False)
    say(full.to_string(float_format=lambda x: f"{x:.1f}", na_rep="never"))

    # ---- D2 which bar binds -----------------------------------------------------------------
    say("\n" + "=" * 190)
    say("D2  WHICH BAR BINDS.  Per-bar breakeven = highest cost at which THAT bar alone passes; "
        "the joint breakeven is their min, and the argmin is the binding bar.  The queue asserts "
        "'the CAGR floor binding first'.")
    say("=" * 190)
    PB = per_bar_breakeven(F, "full")
    PB.to_csv(f"{STEM}.binding.csv", index=False)
    sel = PB[(PB.arm == ARM_STAR) & (PB.conv == "g1.00") & (PB.cad == CADENCE_STAR)]
    say("\n  [D2a] candidate cell (S3, g1.00, W):")
    say(sel[["panel", "f", "be_H1", "be_H2", "be_OOS", "be_DD", "be_CAGR", "be_joint", "binding"]]
        .to_string(index=False, float_format=lambda x: f"{x:.1f}", na_rep="never"))
    at = sel[sel.f == F_STAR]
    say(f"\n  >>> at f=0.50 the binding bar is: "
        + ", ".join(f"{r.panel} -> {r.binding}" for r in at.itertuples()))
    say("  identity check: be_joint == min of the five per-bar breakevens == D1's be, "
        f"max |diff| = "
        f"{float((PB.set_index(KEY).be_joint - BE4b.set_index(KEY).be).abs().max()):.3e}")
    cnt = PB.binding.value_counts()
    say(f"\n  [D2b] binding-bar census over all {len(PB)} cells (all arms/convs/cadences/f):")
    say(cnt.to_string())
    fin = PB[PB.be_joint.notna()]
    cnt2 = fin.binding.value_counts()
    say(f"  restricted to the {len(fin)} cells that pass 4b at 0 bps at all:")
    say(cnt2.to_string())

    # ---- D3 the walk-forward spread on the breakeven ----------------------------------------
    say("\n" + "=" * 190)
    say("D3  THE WALK-FORWARD SPREAD ON THE BREAKEVEN (the number the queue asked for).  "
        "be_IS = breakeven with all bars measured inside 2009-2016; be_OOS = the same bars "
        "measured inside 2017-2026.  spread = be_IS - be_OOS.  Positive spread => an IS-fitted "
        "cost budget OVERSTATES what the arm can pay live, and sizing must use be_OOS.")
    say("=" * 190)
    S = BEis.merge(BEoos, on=KEY, suffixes=("_IS", "_OOS"))
    S = S.merge(BE4b[KEY + ["be"]].rename(columns={"be": "be_full"}), on=KEY)
    S["spread"] = S.be_IS - S.be_OOS
    S.to_csv(f"{STEM}.walkforward.csv", index=False)
    sel = S[(S.arm == ARM_STAR) & (S.conv == "g1.00") & (S.cad == CADENCE_STAR)]
    say("\n  [D3a] candidate cell (S3, g1.00, W).  NB in-window bar sets have no OOS-Sharpe bar "
        "(4 bars, not 5) — stated, not hidden:")
    say(sel[["panel", "f", "be_full", "be_IS", "be_OOS", "spread"]]
        .to_string(index=False, float_format=lambda x: f"{x:.1f}", na_rep="never"))
    a = sel[sel.f == F_STAR]
    for r in a.itertuples():
        say(f"  >>> {r.panel}: be_IS {r.be_IS:.1f} vs be_OOS {r.be_OOS:.1f} bps, "
            f"spread {r.spread:+.1f} bps (full-sample be {r.be_full:.1f}).")
    say("\n  [D3a2] WHICH BAR sets be_OOS — the same per-bar decomposition inside each window "
        "(4 bars: no OOS-Sharpe bar inside a single window):")
    for w, lab in (("IS", "2009-2016"), ("OOS", "2017-2026")):
        P = per_bar_breakeven(F, w)
        s = P[(P.arm == ARM_STAR) & (P.conv == "g1.00") & (P.cad == CADENCE_STAR)]
        say(f"    window {w} ({lab}):")
        say("    " + s[["panel", "f", "be_H1", "be_H2", "be_DD", "be_CAGR", "be_joint", "binding"]]
            .to_string(index=False, float_format=lambda x: f"{x:.1f}", na_rep="never")
            .replace("\n", "\n    "))
        P.to_csv(f"{STEM}.binding_{w}.csv", index=False)
    say(f"\n  [D3b] spread census over all {len(S)} cells: "
        f"positive (IS overstates) {int((S.spread > 0).sum())}, "
        f"zero {int((S.spread == 0).sum())}, negative {int((S.spread < 0).sum())}, "
        f"undefined {int(S.spread.isna().sum())}; "
        f"median {S.spread.median():.1f} bps, mean {S.spread.mean():.2f} bps.")
    say("  by panel (median spread, bps):")
    say(S.groupby("panel").spread.describe()[["count", "mean", "50%", "min", "max"]]
        .to_string(float_format=lambda x: f"{x:.2f}"))
    say("  IS-window SPY bars are the mechanism idea 128 predicted — printed above per panel.")

    # ---- rule 8 -----------------------------------------------------------------------------
    say("\n" + "=" * 190)
    say("RULE 8 WALK-FORWARD (required).  f chosen on 2009-2016 IS Sharpe alone, per "
        "(panel, arm, conv, cadence, cost); 2017-2026 read untouched.")
    say("=" * 190)
    R8 = rule8(F)
    R8.to_csv(f"{STEM}.rule8.csv", index=False)
    sel = R8[(R8.arm == ARM_STAR) & (R8.conv == "g1.00") & (R8.cad == CADENCE_STAR)]
    show = sel[sel.cost.isin([0.0, 5.0, 10.0, 12.0, 15.0, 20.0, 25.0, 30.0])]
    say("\n  [R8a] candidate cell at selected rungs (full 61-rung table in .rule8.csv):")
    say(show[["panel", "cost", "f_pick", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
              "spy_OOS_CAGR", "spy_OOS_Sharpe", "spy_OOS_MaxDD", "regret"]]
        .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say(f"\n  [R8b] rule 8 picks f=0.50 in {int(sel.picks_star.sum())}/{len(sel)} rungs of the "
        f"candidate cell; over ALL {len(R8)} cells it picks f=0.50 in "
        f"{int(R8.picks_star.sum())} ({R8.picks_star.mean():.1%}); mean regret vs f=0.50 "
        f"{R8.regret.mean():+.4f} Sharpe.")
    say("  f-pick census by cost band (candidate cell):")
    say(sel.groupby(["panel", "f_pick"]).size().to_string())

    # RULES v2 comparison OOS at the headline cost
    say("\n  [R8c] OOS (2017-2026) at the headline 10 bps, candidate cell, vs SPY and RULES v2:")
    for p in PANELS:
        row = F[(F.panel == p) & (F.arm == "S3") & (F.conv == "g1.00") & (F.f == F_STAR)
                & (F.cad == "W") & (F.cost == COST_HEADLINE)].iloc[0]
        say(f"    {p:>5}: arm OOS {row.OOS_CAGR:.2%}/{row.OOS_Sharpe:.3f}/{row.OOS_MaxDD:.2%}   "
            f"SPY OOS {row.OOS_b_scagr:.2%}/{row.OOS_b_soos:.3f}/{row.OOS_b_sdd:.2%}")
    B2 = []
    for p in PANELS:
        px = load_universe(broad=(p == "broad"))
        s = px.index[260]
        res = backtest(px, rules_v2_weights(px), cost_bps=COST_HEADLINE, freq="W")
        r = res["returns"].loc[s:]
        st = stats_win(r, "OOS")
        B2.append(dict(panel=p, v2_OOS_CAGR=st["CAGR"], v2_OOS_Sharpe=st["Sharpe"],
                       v2_OOS_MaxDD=st["MaxDD"]))
        say(f"    {p:>5}: RULES v2 OOS {st['CAGR']:.2%}/{st['Sharpe']:.3f}/{st['MaxDD']:.2%}")
    pd.DataFrame(B2).to_csv(f"{STEM}.baselines.csv", index=False)

    # ---- verdict ----------------------------------------------------------------------------
    say("\n" + "=" * 190)
    say("VERDICT")
    say("=" * 190)
    is_star = float(a[a.panel == "u56"].be_IS.iloc[0]), float(a[a.panel == "broad"].be_IS.iloc[0])
    oos_star = float(a[a.panel == "u56"].be_OOS.iloc[0]), float(a[a.panel == "broad"].be_OOS.iloc[0])
    n4a = int((BE4a.be.notna()).sum())
    n4a1 = int((BE4a1.be.notna()).sum())
    n4b = int((BE4b.be.notna()).sum())
    say(f"  4a (vs RULES v2, live) passes at some cost in {n4a}/{len(BE4a)} cells; "
        f"4a vs RULES v1 in {n4a1}/{len(BE4a1)}; 4b in {n4b}/{len(BE4b)} cells.")
    def _cand(df):
        return df[(df.arm == ARM_STAR) & (df.conv == "g1.00") & (df.cad == CADENCE_STAR)
                  & (df.f == F_STAR)]
    c4a, c4a1 = _cand(BE4a), _cand(BE4a1)
    say("  candidate 4a breakeven vs RULES v2: "
        + ", ".join(f"{r.panel} {('never' if pd.isna(r.be) else f'{r.be:.1f}')}"
                    for r in c4a.itertuples())
        + "  |  vs RULES v1: "
        + ", ".join(f"{r.panel} {('never' if pd.isna(r.be) else f'{r.be:.1f}')}"
                    for r in c4a1.itertuples()))
    say(f"  Candidate cross-universe c* (full sample) = {cross_be:.1f} bps.")
    say(f"  Candidate be_IS  = u56 {is_star[0]:.1f} / broad {is_star[1]:.1f} bps.")
    say(f"  Candidate be_OOS = u56 {oos_star[0]:.1f} / broad {oos_star[1]:.1f} bps.")
    say(f"  Cross-universe OOS budget = {min(oos_star):.1f} bps.")
    Path(f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"\nwrote {Path(STEM).name}.console.txt")


if __name__ == "__main__":
    main()
