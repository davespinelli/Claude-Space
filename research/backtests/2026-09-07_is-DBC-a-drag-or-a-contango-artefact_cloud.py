#!/usr/bin/env python3
"""Idea 106 (cloud, 2026-09-07): is-DBC-a-drag-or-a-contango-artefact.

QUEUE TEXT: "idea 102 found deleting DBC improves the sleeve in 8/8 cells (mean dSharpe
+0.163 vs S4's +0.122) at lower turnover, but DBC's +10.4pp contribution is concentrated in
2021/2022/2026 and its dead years are 2009-2013, the severe-contango era.  Split DBC's
contribution by sub-period before pruning it for good; if the drag is 2009-2013 only, the
prune is a sample artefact and idea 104's arm is mis-specified."

WHY THIS MATTERS BEYOND ONE ETF.  Idea 104 already folded `drop DBC` into idea 101's second
arm and idea 102 PARKed `top20 + 50% (TLT,GLD,UUP)` on the strength of the deletion.  Both
rest on a FULL-SAMPLE 8/8 count.  The record's own rule 8 window puts 2009-2016 in-sample:
if DBC's drag lives only in 2009-2013 then the in-sample chooser is being handed the drag and
the out-of-sample window is being handed the payoff, which is the exact shape of a sample
artefact.  This run does not re-litigate whether DBC helps on the full sample; it asks WHEN.

DESIGN (idea 102's construction verbatim -- this run must reproduce its committed numbers to
machine precision before any new claim is made)
-------------------------------------------------------------------------------------------
Sleeve   : idea 18 variant B -- vote in {0,1/3,2/3,1} on the signs of {12-1, 6m, 3m} times
           inverse-60d-vol risk parity, row-normalised, restricted to the arm's assets.
TUNED (2): sleeve arm in {S4, noDBC, noTLT, noGLD, noUUP, DBConly} x f in {0,.25,.50,.75,1}.
           noTLT/noGLD/noUUP are SIBLING CONTROLS: a DBC-specific era story has to look
           different from theirs, or the finding is about the era, not about DBC.
AXES (reported, never selected on): universe {u56, broad} x book {top20, ewall} x gross
           convention {natural, g1.00} x cost {0, 10, 25} bps.  10 bps is PROTOCOL's rung.
ERAS (pre-registered, from the queue's own wording, not fitted):
           CONTANGO = eval start .. 2013-12-31   (the queue's "severe-contango era")
           POST     = 2014-01-01 .. end
           plus finer reads Y1420 (2014-2020) and Y2126 (2021-2026) and a per-year table.

THE THREE TESTS
---------------
(1) ATTRIBUTION.  DBC's own contribution to the S4 sleeve's return, year by year:
    sum_t w_DBC,t * r_DBC,t inside the sleeve.  Reproduces (or refutes) the queue's "+10.4pp,
    concentrated in 2021/2022/2026, dead 2009-2013".
(2) THE EXCISION.  Re-run idea 102's 8/8 deletion count with the CONTANGO era's days deleted
    from the return series.  If the count collapses, the prune was a 2009-2013 artefact; if
    it survives, idea 104's arm is correctly specified and this idea is a KILL.
    (Splicing daily net returns is exact for Sharpe and for the CAGR of the spliced series;
    it is NOT a tradable path, and is used here only as a sub-period statistic.)
(3) RULE 8, twice.  (a) PROTOCOL's window: choose (arm, f) on 2009-2016 by IS Sharpe, read
    2017-2026 ONCE.  (b) The same chooser with the contango era withheld -- IS = 2014-2016.
    If (a) deletes DBC and (b) does not, the record's walk-forward is selecting on the era.

COST NOTE: engine.backtest applies costs as `gross - turnover*bps/1e4` with a holdings path
independent of bps, so each weight matrix is run ONCE at 0 bps and every rung is derived
exactly.  Asserted against a direct 10 bps run at start-up (idea 102's own device).

SURVIVORSHIP: both panels are current constituents (equity levels biased up).  The sleeve
assets are ETFs alive throughout, so the sleeve arm comparison is unaffected; the BOOK the
sleeve is blended into is not, and every number below is a difference between arms sharing
that same book.

Deterministic, standalone, offline:
    python3 research/backtests/2026-09-07_is-DBC-a-drag-or-a-contango-artefact_cloud.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa
from engine import backtest, metrics  # noqa

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 900)

COST_BPS, FREQ, GROSS = 10, "W", 0.75
COST_RUNGS = (0, 10, 25)
MOM_LAGS, VOL_WINDOW = (252, 126, 63), 60
FGRID = [0.00, 0.25, 0.50, 0.75, 1.00]
F_STAR = 0.50                       # idea 102's pre-registered headline f
SPLIT, IS_END = "2017-01-01", "2016-12-31"
CONTANGO_END = "2013-12-31"         # the queue's era boundary, pre-registered
IS2_START = "2014-01-01"            # contango-withheld IS window starts here
S4 = ["TLT", "GLD", "DBC", "UUP"]
ARMS = {
    "S4": S4,
    "noDBC": ["TLT", "GLD", "UUP"],          # idea 102's prune / idea 104's arm
    "noTLT": ["GLD", "DBC", "UUP"],          # sibling controls
    "noGLD": ["TLT", "DBC", "UUP"],
    "noUUP": ["TLT", "GLD", "DBC"],
    "DBConly": ["DBC"],
}
ERAS = {"CONTANGO": (None, CONTANGO_END), "POST": (IS2_START, None),
        "Y1420": ("2014-01-01", "2020-12-31"), "Y2126": ("2021-01-01", None)}
OUT = Path(__file__).with_suffix("")


# ---------------------------------------------------------------- construction (idea 102's)
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
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[assets] = (_vote_mom(sub) * _risk_parity(sub)).fillna(0.0)
    return out


def book_top20(px, n=20):
    s, above, vol20 = score(px, vol_scale=False)
    rank = s.where(above & (vol20 < 0.60)).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (GROSS / n)


def book_ewall(px):
    s, above, vol20 = score(px, vol_scale=False)
    elig = (above & (vol20 < 0.60) & s.notna()).astype(float)
    k = elig.sum(axis=1)
    return elig.div(k.where(k > 0), axis=0).fillna(0.0) * GROSS


BOOKS = {"top20": book_top20, "ewall": book_ewall}


def blend(E, S, f, conv):
    w = (1 - f) * E + f * S
    if conv == "natural":
        return w
    g = w.sum(axis=1)
    return w.mul((1.0 / g.where(g > 1e-12)).fillna(0.0), axis=0)


# ---------------------------------------------------------------- metrics
def stats(r):
    if len(r) < 30:
        return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    m = metrics(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"])


def slc(r, a, b):
    return r.loc[a:b] if (a or b) else r


def full_row(r):
    a = stats(r)
    h = len(r) // 2
    row = dict(CAGR=a["CAGR"], Sharpe=a["Sharpe"], MaxDD=a["MaxDD"],
               H1=stats(r.iloc[:h])["Sharpe"], H2=stats(r.iloc[h:])["Sharpe"],
               IS_Sharpe=stats(r.loc[:IS_END])["Sharpe"],
               IS2_Sharpe=stats(r.loc[IS2_START:IS_END])["Sharpe"],
               OOS_CAGR=stats(r.loc[SPLIT:])["CAGR"], OOS_Sharpe=stats(r.loc[SPLIT:])["Sharpe"],
               OOS_MaxDD=stats(r.loc[SPLIT:])["MaxDD"])
    for name, (a0, b0) in ERAS.items():
        e = stats(slc(r, a0, b0))
        row[f"S_{name}"] = e["Sharpe"]
        row[f"C_{name}"] = e["CAGR"]
        row[f"D_{name}"] = e["MaxDD"]
    ex = r[~((r.index <= pd.Timestamp(CONTANGO_END)))]           # the excision
    e = stats(ex)
    row["EXC_Sharpe"], row["EXC_CAGR"], row["EXC_MaxDD"] = e["Sharpe"], e["CAGR"], e["MaxDD"]
    return row


def keep_4a(row, base):
    return bool(row["H1"] > base["H1"] and row["H2"] > base["H2"] and row["MaxDD"] >= base["MaxDD"])


def keep_4b(row, spy):
    return bool(row["H1"] > spy["H1"] and row["H2"] > spy["H2"] and row["OOS_Sharpe"] > spy["OOS_Sharpe"]
                and row["MaxDD"] >= 0.60 * spy["MaxDD"] and row["CAGR"] >= 0.70 * spy["CAGR"])


# ---------------------------------------------------------------- main
def main():
    universes = {"u56": load_universe(), "broad": load_universe(broad=True)}

    # cost-linearity assertion (idea 102's device; the whole run depends on it)
    pxa = universes["u56"]
    w0 = blend(book_top20(pxa), sleeve_weights(pxa, S4), 0.5, "natural")
    r0 = backtest(pxa, w0, cost_bps=0.0, freq=FREQ)
    r10 = backtest(pxa, w0, cost_bps=10.0, freq=FREQ)
    err = float((r0["returns"] - r0["turnover"] * 10 / 1e4 - r10["returns"]).abs().max())
    print(f"GATE cost linearity (derive any rung from the 0-bps run): max abs err {err:.3e} "
          f"{'PASS' if err < 1e-15 else 'FAIL'}")
    assert err < 1e-12

    records, attrib, refs = [], [], {}

    for tag, px in universes.items():
        start = px.index[260]
        for a in ARMS.values():
            miss = [t for t in a if t not in px.columns]
            if miss:
                raise SystemExit(f"missing {miss} in {tag}")

        b1_r = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        v2_r = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
        b1, v2, spy = full_row(b1_r), full_row(v2_r), full_row(spy_r)
        refs[tag] = (b1, v2, spy)
        print("\n" + "=" * 122)
        print(f"### {tag}: {px.shape[1]} tickers, {px.index[0].date()} -> {px.index[-1].date()}, eval from {start.date()}")
        print(pd.DataFrame({"RULES v1": b1, "RULES v2 (live)": v2, "SPY": spy}).T[
            ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD",
             "S_CONTANGO", "S_POST"]].to_string(float_format=lambda x: f"{x:.4f}"))
        print(f"4b bars: H1>{spy['H1']:.4f} H2>{spy['H2']:.4f} OOS>{spy['OOS_Sharpe']:.4f} "
              f"|MaxDD|<={abs(0.60*spy['MaxDD']):.2%} CAGR>={0.70*spy['CAGR']:.2%}")

        # ---- (1) DBC's contribution inside the S4 sleeve, year by year
        rets = px.pct_change().fillna(0.0)
        sw = sleeve_weights(px, S4)
        held = sw.shift(1).fillna(0.0)                       # decided t, applied t+1 (engine's convention)
        for t in S4:
            contrib = (held[t] * rets[t]).loc[start:]
            wser = held[t].loc[start:]
            for y, g in contrib.groupby(contrib.index.year):
                attrib.append(dict(universe=tag, asset=t, year=int(y),
                                   contrib_pp=100 * g.sum(), mean_w=float(wser[wser.index.year == y].mean()),
                                   asset_ret_pp=100 * rets[t].loc[start:][rets.loc[start:].index.year == y].sum()))

        S_w = {a: sleeve_weights(px, v) for a, v in ARMS.items()}
        B_w = {b: fn(px) for b, fn in BOOKS.items()}
        cache = {}
        for bname in BOOKS:
            cache[(bname, "PURE")] = backtest(px, B_w[bname], cost_bps=0.0, freq=FREQ)

        for aname in ARMS:
            for bname in BOOKS:
                for conv in ("natural", "g1.00"):
                    for f in FGRID:
                        if f == 0.0 and conv == "natural":
                            res, w = cache[(bname, "PURE")], B_w[bname]
                        else:
                            w = blend(B_w[bname], S_w[aname], f, conv)
                            res = backtest(px, w, cost_bps=0.0, freq=FREQ)
                        g_r, to = res["returns"].loc[start:], res["turnover"].loc[start:]
                        for bps in COST_RUNGS:
                            r = g_r - to * bps / 1e4
                            row = full_row(r)
                            row["Turn_yr"] = to.sum() / (len(r) / 252)
                            row["Gross"] = float(w.loc[start:].sum(axis=1).mean())
                            row["p4a"] = keep_4a(row, v2)
                            row["p4a_v1"] = keep_4a(row, b1)
                            row["p4b"] = keep_4b(row, spy)
                            records.append(dict(universe=tag, arm=aname, book=bname, conv=conv,
                                                f=f, bps=bps, **row))
            print(f"  ... {aname} done ({len(records)} rows)")

    G = pd.DataFrame(records)
    A = pd.DataFrame(attrib)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    A.to_csv(f"{OUT}.attribution.csv", index=False)

    # ------------------------------------------------------------ reproduction gate
    print("\n" + "=" * 122)
    print("### REPRODUCTION GATE — idea 102's committed .deletion.csv (f=0.50, 10 bps)")
    dele = pd.read_csv(REPO / "research" / "backtests" / "2026-09-05_which-asset-carries-S4_C.deletion.csv")
    mine = G[(G.f == F_STAR) & (G.bps == COST_BPS)].set_index(["universe", "book", "conv", "arm"])
    errs = []
    for r in dele.itertuples():
        key = (r.universe, r.book, r.conv, r.sleeve)
        if key in mine.index:
            m = mine.loc[key]
            errs.append((abs(m.CAGR - r.CAGR), abs(m.Sharpe - r.Sharpe), abs(m.MaxDD - r.MaxDD)))
    E = np.array(errs)
    print(f"  matched rows: {len(E)} of {len(dele)}   max abs err  CAGR {E[:,0].max():.3e}  "
          f"Sharpe {E[:,1].max():.3e}  MaxDD {E[:,2].max():.3e}  "
          f"{'PASS' if E.max() < 1e-10 else 'FAIL'}")
    print("  (TLTonly is idea 102's sixth arm and is replaced here by DBConly, so 8 of its 48 "
          "rows have no counterpart by design.)")

    # ------------------------------------------------------------ (1) attribution
    print("\n" + "=" * 122)
    print("### (1) ATTRIBUTION — each S4 asset's contribution to the SLEEVE's return, pp per calendar year")
    for tag in universes:
        sub = A[A.universe == tag]
        piv = sub.pivot_table(index="year", columns="asset", values="contrib_pp")
        piv["TOTAL"] = piv.sum(axis=1)
        print(f"\n  --- {tag} (contribution, pp)")
        print(piv.to_string(float_format=lambda x: f"{x:+.2f}"))
        d = piv["DBC"]
        print(f"      DBC total {d.sum():+.2f} pp;  2009-2013 {d[d.index <= 2013].sum():+.2f} pp;  "
              f"2014-2020 {d[(d.index >= 2014) & (d.index <= 2020)].sum():+.2f} pp;  "
              f"2021-2026 {d[d.index >= 2021].sum():+.2f} pp")
        print(f"      DBC positive years: {sorted(d[d > 0].index.tolist())}")
        print(f"      DBC mean weight inside the sleeve: "
              f"{sub[sub.asset=='DBC'].mean_w.mean():.4f} (equal share would be 0.2500)")

    # ------------------------------------------------------------ (2) the deletion, by era
    print("\n" + "=" * 122)
    print("### (2) THE DELETION GAIN BY ERA — Sharpe(arm) - Sharpe(S4) at each f, per era.")
    print("###     Positive = deleting that asset HELPED.  idea 102's claim is the FULL column.")
    base = G[G.arm == "S4"].set_index(["universe", "book", "conv", "f", "bps"])
    cols = ["Sharpe", "EXC_Sharpe"] + [f"S_{e}" for e in ERAS] + ["CAGR", "OOS_Sharpe"]
    d_rows = []
    for r in G[G.arm != "S4"].to_dict("records"):
        key = (r["universe"], r["book"], r["conv"], r["f"], r["bps"])
        b = base.loc[key]
        rec = {k: r[k] for k in ("universe", "arm", "book", "conv", "f", "bps")}
        for c in cols:
            rec["d_" + c] = r[c] - b[c]
        rec["arm_Sharpe"], rec["S4_Sharpe"] = r["Sharpe"], b["Sharpe"]
        rec["d_Turn"] = r["Turn_yr"] - b["Turn_yr"]
        d_rows.append(rec)
    DEL = pd.DataFrame(d_rows)
    DEL.to_csv(f"{OUT}.deletion_by_era.csv", index=False)

    for bps in COST_RUNGS:
        sub = DEL[(DEL.bps == bps) & (DEL.f > 0) & (DEL.f < 1.0)]
        print(f"\n  --- {bps} bps, f in {{0.25,0.50,0.75}}, {len(sub)} points")
        agg = sub.groupby("arm").agg(
            n=("d_Sharpe", "size"),
            FULL=("d_Sharpe", "mean"), FULL_win=("d_Sharpe", lambda x: int((x > 0).sum())),
            CONTANGO=("d_S_CONTANGO", "mean"),
            CONT_win=("d_S_CONTANGO", lambda x: int((x > 0).sum())),
            POST=("d_S_POST", "mean"), POST_win=("d_S_POST", lambda x: int((x > 0).sum())),
            EXCISED=("d_EXC_Sharpe", "mean"), EXC_win=("d_EXC_Sharpe", lambda x: int((x > 0).sum())),
            y1420=("d_S_Y1420", "mean"), y2126=("d_S_Y2126", "mean"),
            OOS=("d_OOS_Sharpe", "mean"), OOS_win=("d_OOS_Sharpe", lambda x: int((x > 0).sum())),
            dTurn=("d_Turn", "mean"))
        print(agg.to_string(float_format=lambda x: f"{x:+.4f}"))

    print("\n  idea 102's headline cell (f=0.50, 10 bps, the 8 (universe x book x conv) cells):")
    h = DEL[(DEL.f == F_STAR) & (DEL.bps == COST_BPS) & (DEL.arm == "noDBC")]
    print(h[["universe", "book", "conv", "d_Sharpe", "d_S_CONTANGO", "d_S_POST",
             "d_EXC_Sharpe", "d_S_Y1420", "d_S_Y2126", "d_OOS_Sharpe", "d_Turn"]].to_string(
        index=False, float_format=lambda x: f"{x:+.4f}"))
    print(f"\n  FULL sample : deleting DBC helps {int((h.d_Sharpe>0).sum())}/8 cells, "
          f"mean {h.d_Sharpe.mean():+.4f}   (idea 102 published 8/8, mean dSharpe +0.163 vs S4 +0.122)")
    print(f"  CONTANGO era: helps {int((h['d_S_CONTANGO']>0).sum())}/8, "
          f"mean {h['d_S_CONTANGO'].mean():+.4f}")
    print(f"  POST era    : helps {int((h['d_S_POST']>0).sum())}/8, "
          f"mean {h['d_S_POST'].mean():+.4f}")
    print(f"  EXCISED     : helps {int((h.d_EXC_Sharpe>0).sum())}/8, mean {h.d_EXC_Sharpe.mean():+.4f}   "
          f"<-- THE TEST: if this collapses, the prune is a 2009-2013 artefact")
    print(f"  2021-2026   : helps {int((h['d_S_Y2126']>0).sum())}/8, mean {h['d_S_Y2126'].mean():+.4f}")

    print("\n  SIBLING CONTROLS at the same cell (does every deletion behave this way?):")
    hc = DEL[(DEL.f == F_STAR) & (DEL.bps == COST_BPS)]
    print(hc.groupby("arm").agg(
        FULL=("d_Sharpe", "mean"), FULL_win=("d_Sharpe", lambda x: f"{int((x>0).sum())}/8"),
        CONTANGO=("d_S_CONTANGO", "mean"),
        CONT_win=("d_S_CONTANGO", lambda x: f"{int((x>0).sum())}/8"),
        POST=("d_S_POST", "mean"), POST_win=("d_S_POST", lambda x: f"{int((x>0).sum())}/8"),
        EXCISED=("d_EXC_Sharpe", "mean"), EXC_win=("d_EXC_Sharpe", lambda x: f"{int((x>0).sum())}/8")
    ).to_string(float_format=lambda x: f"{x:+.4f}"))

    # ------------------------------------------------------------ DBC standalone by era
    print("\n" + "=" * 122)
    print("### DBC's OWN record by era (the sleeve-weighted DBConly arm at f=1.00, and raw DBC)")
    for tag, px in universes.items():
        start = px.index[260]
        raw = px["DBC"].pct_change().fillna(0).loc[start:]
        q = G[(G.universe == tag) & (G.arm == "DBConly") & (G.f == 1.0) & (G.conv == "natural") &
              (G.bps == COST_BPS) & (G.book == "top20")].iloc[0]
        print(f"  {tag}: raw DBC buy-and-hold  CAGR {metrics(raw)['CAGR']:+.2%} Sharpe {metrics(raw)['Sharpe']:+.3f}"
              f" | 2009-2013 {metrics(raw.loc[:CONTANGO_END])['CAGR']:+.2%}"
              f" | 2014-2020 {metrics(raw.loc['2014':'2020'])['CAGR']:+.2%}"
              f" | 2021- {metrics(raw.loc['2021':])['CAGR']:+.2%}")
        print(f"        DBConly sleeve (trend-voted) CAGR {q.CAGR:+.2%} Sharpe {q.Sharpe:+.3f}"
              f" | contango {q['S_CONTANGO']:+.3f} | post {q['S_POST']:+.3f}")

    # ------------------------------------------------------------ KEEP paths
    print("\n" + "=" * 122)
    print(f"### KEEP PATHS over all {len(G)} points (all cost rungs; none selected on)")
    print(G.groupby(["universe", "bps"]).agg(n=("p4b", "size"), p4b=("p4b", "sum"),
                                             p4a_v2=("p4a", "sum"), p4a_v1=("p4a_v1", "sum")).to_string())
    print(f"  TOTAL: 4b {G.p4b.sum()}/{len(G)}; 4a vs RULES v2 {G.p4a.sum()}/{len(G)}; "
          f"4a vs RULES v1 {G.p4a_v1.sum()}/{len(G)}")
    Gd = G.copy()
    Gd["arm_eff"] = np.where(Gd.f == 0.0, "-", Gd.arm)
    Gd["conv_eff"] = np.where((Gd.f == 0.0) & (Gd.conv == "natural"), "-", Gd.conv)
    Dq = Gd.drop_duplicates(subset=["universe", "book", "arm_eff", "conv_eff", "f", "bps"])
    print(f"  DISTINCT books (f=0 natural collapsed across arms): {len(Dq)} rows; "
          f"4b {int(Dq.p4b.sum())}/{len(Dq)}, 4a vs v2 {int(Dq.p4a.sum())}/{len(Dq)}")
    cc = ["universe", "arm", "book", "conv", "f", "bps", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
          "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "Turn_yr", "Gross", "p4a"]
    if Dq.p4b.sum():
        print("\n  4b passes (distinct books), best 25 by Sharpe:")
        print(Dq[Dq.p4b][cc].sort_values("Sharpe", ascending=False).head(25).to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))
    Dq[Dq.p4b].to_csv(f"{OUT}.keeppaths.csv", index=False)

    # ------------------------------------------------------------ (3) rule 8, twice
    print("\n" + "=" * 122)
    print("### (3) RULE 8 — (arm, f) by IS Sharpe, read ONCE on 2017-2026.")
    print("###     IS_full = 2009-2016 (PROTOCOL); IS_post = 2014-2016 (contango era withheld).")
    # the no-sleeve control is the PURE book (f=0, natural); it is the same object for both
    # conventions, so it is looked up from the whole grid rather than from the conv group.
    CTRL = G[(G.f == 0.0) & (G.conv == "natural")]
    wf = []
    for (tag, bname, conv, bps), sub in G.groupby(["universe", "book", "conv", "bps"], sort=False):
        b1, v2, spy = refs[tag]
        pool = sub[sub.f > 0]
        for wname, col in [("IS_full", "IS_Sharpe"), ("IS_post", "IS2_Sharpe")]:
            p = pool.loc[pool[col].idxmax()]
            ctrl = CTRL[(CTRL.universe == tag) & (CTRL.book == bname) & (CTRL.bps == bps)].iloc[0]
            s4b = pool[pool.arm == "S4"]
            s4b = s4b.loc[s4b[col].idxmax()]
            wf.append(dict(universe=tag, book=bname, conv=conv, bps=bps, window=wname,
                           pick=f"{p.arm}@f={p.f:.2f}", drops_DBC=p.arm in ("noDBC",),
                           has_DBC=("DBC" in ARMS[p.arm]),
                           OOS_Sharpe=p.OOS_Sharpe, OOS_CAGR=p.OOS_CAGR, OOS_MaxDD=p.OOS_MaxDD,
                           p4b=bool(p.p4b), p4a=bool(p.p4a),
                           S4_OOS_Sharpe=s4b.OOS_Sharpe, S4_pick=f"S4@f={s4b.f:.2f}",
                           ctrl_OOS_Sharpe=ctrl.OOS_Sharpe, ctrl_OOS_CAGR=ctrl.OOS_CAGR,
                           v2_OOS_Sharpe=v2["OOS_Sharpe"], v1_OOS_Sharpe=b1["OOS_Sharpe"],
                           spy_OOS_Sharpe=spy["OOS_Sharpe"], spy_OOS_CAGR=spy["OOS_CAGR"]))
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    print(W[W.bps == COST_BPS].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\n  SUMMARY by IS window and cost rung:")
    print(W.groupby(["window", "bps"]).apply(lambda g: pd.Series(dict(
        n=len(g),
        picks_with_DBC=int(g.has_DBC.sum()),
        picks_noDBC=int((g.pick.str.startswith("noDBC")).sum()),
        OOS_Sharpe=g.OOS_Sharpe.mean(),
        vs_S4=(g.OOS_Sharpe - g.S4_OOS_Sharpe).mean(),
        beats_S4=int((g.OOS_Sharpe > g.S4_OOS_Sharpe).sum()),
        beats_ctrl=int((g.OOS_Sharpe > g.ctrl_OOS_Sharpe).sum()),
        beats_v2=int((g.OOS_Sharpe > g.v2_OOS_Sharpe).sum()),
        beats_SPY=int((g.OOS_Sharpe > g.spy_OOS_Sharpe).sum()),
        p4b=int(g.p4b.sum()))), include_groups=False).to_string(float_format=lambda x: f"{x:.4f}"))

    print("\n  DOES THE CHOOSER'S DBC DECISION FLIP WITH THE ERA?  (cells where IS_full and "
          "IS_post disagree on holding DBC)")
    pv = W.pivot_table(index=["universe", "book", "conv", "bps"], columns="window",
                       values="has_DBC", aggfunc="first")
    flip = pv[pv["IS_full"] != pv["IS_post"]]
    print(f"    {len(flip)} of {len(pv)} cells flip.")
    if len(flip):
        print(flip.to_string())

    print("\nWritten:", ", ".join(sorted(p.name for p in OUT.parent.glob(OUT.name + ".*"))))


if __name__ == "__main__":
    main()
