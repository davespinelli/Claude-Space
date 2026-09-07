#!/usr/bin/env python3
"""QUEUE idea 106 — is-DBC-a-drag-or-a-contango-artefact (lane B, 2026-09-07).

Question (as worded in QUEUE.md)
--------------------------------
"Idea 102 found deleting DBC improves the sleeve in 8/8 cells (mean dSharpe +0.163 vs S4's
+0.122) at lower turnover, but DBC's +10.4pp contribution is concentrated in 2021/2022/2026
and its dead years are 2009-2013, the severe-contango era.  Split DBC's contribution by
sub-period before pruning it for good; if the drag is 2009-2013 only, the prune is a sample
artefact and idea 104's arm is mis-specified."

What is actually at stake
-------------------------
Idea 104 folded "drop DBC" (S3) into idea 101 as a second arm and it is the arm that beat S4
on 4a in 2/2 universes at all 5 cost rungs.  That verdict rests on a full-sample dSharpe gap.
If the gap is bought entirely in 2009-2013 — the era when front-month commodity futures rolled
in severe contango and DBC bled carry that no longer exists at today's curve shape — then the
prune is a sample artefact and S3 is over-fit to a regime that has ended.  The falsifiable
claim is therefore NOT "does noDBC beat S4 in full sample" (idea 102 already answered yes) but
"does it still beat S4 once 2009-2013 is removed".

DESIGN (PROTOCOL rules 1-9)
---------------------------
Panels      : `load_universe()` (56) and `load_universe(broad=True)` (136).  SURVIVORSHIP:
              current constituents; equity levels biased up.  Sleeve assets are ETFs and are
              not exposed to it.  Both panels carry TLT/GLD/DBC/UUP from 2008-01-02.
TUNED (2)   : sleeve in {S4, noDBC, DBConly} x f in {0.00, 0.25, 0.50, 0.75, 1.00}.
              ALL 120 (universe x book x convention x sleeve x f) 10-bps points are written to
              .grid.csv; nothing is hidden.  The sub-period split is NOT tuned: it is
              pre-registered at 2014-01-01 from the queue's own wording ("dead years are
              2009-2013"), and a sensitivity sweep over alternative boundaries is reported as
              a robustness check, never selected on.
CONTROLS    : book in {top20, ewall} (idea 2 / idea 10), universe in {u56, broad}, gross
              convention in {natural, g=1.00}, cost in {5,10,15,20,25} bps.  Reported only.
SLEEVE      : idea 18 variant B verbatim (idea 100/102's construction, copied unchanged):
              momentum vote in {0,1/3,2/3,1} on the signs of {12-1, 6m, 3m} times
              inverse-60d-vol risk parity, row-normalised.
BASELINE    : RULES v2 (live since 2026-09-06) for 4a; SPY for 4b; RULES v1 kept for continuity
              with the pre-2026-09-06 record.
RULE 8      : (sleeve, f) chosen on 2009-2016 by IS Sharpe, 2017-2026 evaluated untouched, per
              (universe, book, convention).  Note the IS window is 62% contango era, so if the
              drag IS an artefact the pre-registered chooser should mis-pick and pay OOS —
              that is the sharpest form of the question and it is reported either way.

COST NOTE: engine.backtest applies costs as `gross_returns - turnover * bps/1e4` with the
holdings path independent of bps, so every weight matrix is run ONCE at 0 bps and each rung of
the ladder is derived exactly.  Asserted against a direct 10 bps run at start-up.

KNOWN DATA CAVEAT (queue idea 38): data/prices*.csv are indexed on CALENDAR days after
2014-09-17 because BTC-USD is in the download, so post-2014 weekends are zero-return rows.
It hits every arm, the baseline and SPY identically — cross-arm comparisons are
apples-to-apples; absolute Sharpe levels wait on idea 38.  It does bear on THIS run's headline
because the two sub-periods straddle 2014-09-17: the contango era is trading-day-indexed and
the post era is calendar-indexed, which deflates post-era Sharpe levels relative to contango-era
ones.  The statistic this run judges on is a WITHIN-sub-period DIFFERENCE between two arms on
identical days, which is immune; absolute cross-era Sharpe comparisons are flagged where used.

Deterministic, standalone:
    python research/backtests/2026-09-07_is-DBC-a-drag-or-a-contango-artefact_B.py
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd

from baseline import load_universe, rules_v1_weights, rules_v2_weights, score
from engine import backtest, metrics

COST_BPS = 10
COST_LADDER = (5, 10, 15, 20, 25)
FREQ = "W"
GROSS = 0.75
MOM_LAGS = (252, 126, 63)
VOL_WINDOW = 60
FGRID = [0.00, 0.25, 0.50, 0.75, 1.00]
F_STAR = 0.50                       # idea 100/102's pre-registered headline sleeve fraction
IS_END = "2016-12-31"               # rule 8
SPLIT = "2017-01-01"                # rule 8 OOS start
CONTANGO_END = "2013-12-31"         # pre-registered from the queue wording
POST_START = "2014-01-01"
ALT_BOUNDS = ["2012-01-01", "2013-01-01", "2014-01-01", "2015-01-01", "2016-01-01"]

S4 = ["TLT", "GLD", "DBC", "UUP"]
SLEEVES = {
    "S4": S4,                       # idea 100's sleeve, the incumbent PARK
    "noDBC": ["TLT", "GLD", "UUP"],  # idea 104's arm (S3), the prune under test
    "DBConly": ["DBC"],             # isolates what DBC alone brings
}
OUT = Path(__file__).with_suffix("")


# ---------------------------------------------------------------- sleeve construction
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
    """idea 18 variant B, restricted to `assets`; zero everywhere else."""
    sub = px[assets]
    w = (_vote_mom(sub) * _risk_parity(sub)).fillna(0.0)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[assets] = w
    return out


# ---------------------------------------------------------------- equity books
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
CONVS = ["natural", "g1.00"]


def blend(E, S, f, conv):
    w = (1 - f) * E + f * S
    if conv == "natural":
        return w
    g = w.sum(axis=1)
    return w.mul((1.0 / g.where(g > 1e-12)).fillna(0.0), axis=0)


# ---------------------------------------------------------------- run / metrics helpers
def run(px, w, start):
    res = backtest(px, w, cost_bps=0.0, freq=FREQ)
    return res["returns"].loc[start:], res["turnover"].loc[start:]


def net(gr, to, bps=COST_BPS):
    return gr - to * bps / 1e4


def stats(r):
    if len(r) < 60:
        return np.nan, np.nan, np.nan
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def sharpe_on(r, lo=None, hi=None):
    seg = r.loc[lo:hi] if (lo or hi) else r
    return stats(seg)[1]


def full_row(r, to=None):
    h = len(r) // 2
    c, s, d = stats(r)
    _, h1, _ = stats(r.iloc[:h])
    _, h2, _ = stats(r.iloc[h:])
    _, i_s, _ = stats(r.loc[:IS_END])
    oc, os_, od = stats(r.loc[SPLIT:])
    cc, cs, cd = stats(r.loc[:CONTANGO_END])
    pc, ps, pd_ = stats(r.loc[POST_START:])
    out = dict(CAGR=c, Sharpe=s, MaxDD=d, H1=h1, H2=h2, IS_Sharpe=i_s,
               OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
               CON_CAGR=cc, CON_Sharpe=cs, CON_MaxDD=cd,
               POST_CAGR=pc, POST_Sharpe=ps, POST_MaxDD=pd_)
    if to is not None:
        out["turnover_yr"] = float(to.sum() / (len(to) / 252.0))
    return out


def keep_4a(row, base):
    return bool(row["H1"] > base["H1"] and row["H2"] > base["H2"] and row["MaxDD"] >= base["MaxDD"])


def keep_4b(row, spy):
    return bool(row["H1"] > spy["H1"] and row["H2"] > spy["H2"] and row["OOS_Sharpe"] > spy["OOS_Sharpe"]
                and row["MaxDD"] >= 0.60 * spy["MaxDD"] and row["CAGR"] >= 0.70 * spy["CAGR"])


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.3f}")


# ---------------------------------------------------------------- main
def main():
    universes = {"u56": load_universe(), "broad": load_universe(broad=True)}

    px0 = universes["u56"]
    st0 = px0.index[260]
    w0 = book_top20(px0)
    gr0, to0 = run(px0, w0, st0)
    direct = backtest(px0, w0, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[st0:]
    err = float((net(gr0, to0) - direct).abs().max())
    print(f"[check] cost linearity max |derived - direct| at {COST_BPS} bps = {err:.2e}")
    assert err < 1e-12, "cost is not linear in this engine — ladder derivation invalid"

    records, refs, ladder_rows, attrib_rows, alt_rows = [], {}, [], [], []
    raw = {}   # (tag, book, conv, sleeve, f) -> (gross returns, turnover)

    for tag, px in universes.items():
        start = px.index[260]
        print("=" * 118)
        print(f"### UNIVERSE {tag}: {px.shape[1]} tickers, {px.index[0].date()} -> "
              f"{px.index[-1].date()} | eval from {start.date()}")

        bgr, bto = run(px, rules_v2_weights(px), start)
        base_v2 = full_row(net(bgr, bto), bto)
        ogr, oto = run(px, rules_v1_weights(px), start)
        base_v1 = full_row(net(ogr, oto), oto)
        spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
        spy = full_row(spy_r)
        refs[tag] = (base_v2, base_v1, spy)
        print("\nReference rows (same days, same costs):")
        print(fmt(pd.DataFrame({"RULES v2 (live)": base_v2, "RULES v1": base_v1, "SPY": spy}).T))
        print(f"\n4b bars: Sharpe > SPY H1 {spy['H1']:.3f} / H2 {spy['H2']:.3f} / OOS "
              f"{spy['OOS_Sharpe']:.3f} · MaxDD >= {0.60 * spy['MaxDD']:.1%} · "
              f"CAGR >= {0.70 * spy['CAGR']:.2%}")

        # ---- per-year attribution of DBC INSIDE the S4 sleeve (reproduces idea 102's +10.4pp)
        S = sleeve_weights(px, S4)
        rets = px.pct_change().fillna(0.0)
        wl = S.shift(1).fillna(0.0)          # weights decided t, applied t+1
        contrib = (wl * rets)[S4].loc[start:]
        by_year = contrib.groupby(contrib.index.year).sum()
        tot = contrib.sum()
        print(f"\nDBC contribution inside the S4 sleeve ({tag}): sum of w*r by asset, pp of the "
              f"sleeve's cumulative simple return")
        print(fmt((by_year * 100).round(2)))
        share = {a: 100 * tot[a] / tot.sum() for a in S4}
        print("total pp: " + " ".join(f"{a} {100*tot[a]:+.1f}" for a in S4)
              + " | share of sleeve return: " + " ".join(f"{a} {share[a]:.0f}%" for a in S4))
        for a in S4:
            attrib_rows.append(dict(universe=tag, asset=a,
                                    pp_total=100 * tot[a],
                                    pp_contango=100 * contrib.loc[:CONTANGO_END, a].sum(),
                                    pp_post=100 * contrib.loc[POST_START:, a].sum(),
                                    share_pct=share[a],
                                    mean_weight=float(wl.loc[start:, a].mean())))

        for bname, bfn in BOOKS.items():
            E = bfn(px)
            for sname, assets in SLEEVES.items():
                Sw = sleeve_weights(px, assets)
                for conv in CONVS:
                    for f in FGRID:
                        if f == 0.0 and (sname != "S4" or conv != "natural"):
                            pass  # f=0 is the same book for every sleeve; kept for a full grid
                        w = blend(E, Sw, f, conv)
                        gr, to = run(px, w, start)
                        raw[(tag, bname, conv, sname, f)] = (gr, to)
                        row = full_row(net(gr, to), to)
                        row.update(universe=tag, book=bname, conv=conv, sleeve=sname, f=f,
                                   pass_4a=keep_4a(row, base_v2), pass_4b=keep_4b(row, spy))
                        records.append(row)
                        for bps in COST_LADDER:
                            rr = net(gr, to, bps)
                            lr = full_row(rr)
                            lr.update(universe=tag, book=bname, conv=conv, sleeve=sname, f=f,
                                      cost_bps=bps, pass_4a=keep_4a(lr, base_v2),
                                      pass_4b=keep_4b(lr, spy))
                            ladder_rows.append(lr)

    G = pd.DataFrame(records)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    L = pd.DataFrame(ladder_rows)
    L.to_csv(f"{OUT}.ladder.csv", index=False)
    pd.DataFrame(attrib_rows).to_csv(f"{OUT}.attrib.csv", index=False)
    print("\n" + "=" * 118)
    print(f"FULL GRID at {COST_BPS} bps ({len(G)} points, all reported -> {OUT}.grid.csv)")
    print(fmt(G.set_index(["universe", "book", "conv", "sleeve", "f"])
              [["CAGR", "Sharpe", "MaxDD", "H1", "H2", "CON_Sharpe", "POST_Sharpe",
                "OOS_Sharpe", "turnover_yr", "pass_4a", "pass_4b"]]))

    # ================================================================ THE HEADLINE TEST
    # gap = Sharpe(noDBC) - Sharpe(S4) at matched (universe, book, conv, f), by sub-period.
    print("\n" + "=" * 118)
    print("HEADLINE — does deleting DBC still help once the 2009-2013 contango era is removed?")
    key = ["universe", "book", "conv", "f"]
    piv = G.pivot_table(index=key, columns="sleeve",
                        values=["Sharpe", "CON_Sharpe", "POST_Sharpe", "OOS_Sharpe",
                                "CAGR", "MaxDD", "turnover_yr"])
    gaps = pd.DataFrame({
        "gap_full": piv[("Sharpe", "noDBC")] - piv[("Sharpe", "S4")],
        "gap_contango": piv[("CON_Sharpe", "noDBC")] - piv[("CON_Sharpe", "S4")],
        "gap_post": piv[("POST_Sharpe", "noDBC")] - piv[("POST_Sharpe", "S4")],
        "gap_oos": piv[("OOS_Sharpe", "noDBC")] - piv[("OOS_Sharpe", "S4")],
        "dCAGR": piv[("CAGR", "noDBC")] - piv[("CAGR", "S4")],
        "dMaxDD": piv[("MaxDD", "noDBC")] - piv[("MaxDD", "S4")],
        "dTurnover": piv[("turnover_yr", "noDBC")] - piv[("turnover_yr", "S4")],
    })
    gaps = gaps[gaps.index.get_level_values("f") > 0]   # f=0 is the bare book, gap is 0 by construction
    gaps.to_csv(f"{OUT}.gaps.csv")
    print(fmt(gaps))
    n = len(gaps)
    print(f"\nnoDBC beats S4 in: full {int((gaps.gap_full>0).sum())}/{n} cells "
          f"(mean {gaps.gap_full.mean():+.4f}) | contango-era {int((gaps.gap_contango>0).sum())}/{n} "
          f"(mean {gaps.gap_contango.mean():+.4f}) | post-2014 {int((gaps.gap_post>0).sum())}/{n} "
          f"(mean {gaps.gap_post.mean():+.4f}) | OOS 2017+ {int((gaps.gap_oos>0).sum())}/{n} "
          f"(mean {gaps.gap_oos.mean():+.4f})")
    print(f"turnover: noDBC lower in {int((gaps.dTurnover<0).sum())}/{n} cells "
          f"(mean {gaps.dTurnover.mean():+.3f} /yr)")

    # sub-period sensitivity: the boundary is pre-registered, this sweep is reported not selected on
    print("\nBoundary sensitivity (reported, never selected on) — mean gap on [bound, end):")
    for tag, px in universes.items():
        start = px.index[260]
        for b in ALT_BOUNDS:
            vals = []
            for (t, bk, cv, sl, f), (gr, to) in raw.items():
                if t != tag or sl not in ("S4", "noDBC") or f == 0.0:
                    continue
                vals.append(((bk, cv, f), sl, sharpe_on(net(gr, to), b, None)))
            d = {}
            for k, sl, v in vals:
                d.setdefault(k, {})[sl] = v
            g = np.array([d[k]["noDBC"] - d[k]["S4"] for k in d if len(d[k]) == 2])
            alt_rows.append(dict(universe=tag, bound=b, n=len(g), mean_gap=float(g.mean()),
                                 frac_pos=float((g > 0).mean())))
            print(f"  {tag:5s} from {b}: n={len(g):2d} mean gap {g.mean():+.4f} "
                  f"positive {int((g>0).sum())}/{len(g)}")
    pd.DataFrame(alt_rows).to_csv(f"{OUT}.boundary.csv", index=False)

    # ================================================================ RULE 8 WALK-FORWARD
    print("\n" + "=" * 118)
    print("RULE 8 WALK-FORWARD — (sleeve, f) chosen on 2009-2016 IS Sharpe, 2017-2026 untouched")
    wf = []
    for tag, px in universes.items():
        base_v2, base_v1, spy = refs[tag]
        for bname in BOOKS:
            for conv in CONVS:
                cand = G[(G.universe == tag) & (G.book == bname) & (G.conv == conv)
                         & (G.sleeve != "DBConly")]
                pick = cand.loc[cand.IS_Sharpe.idxmax()]
                # counterfactual: the same chooser restricted to each sleeve
                per = {}
                for sl in ("S4", "noDBC"):
                    c2 = cand[cand.sleeve == sl]
                    p2 = c2.loc[c2.IS_Sharpe.idxmax()]
                    per[sl] = p2
                wf.append(dict(
                    universe=tag, book=bname, conv=conv,
                    pick_sleeve=pick.sleeve, pick_f=pick.f, IS_Sharpe=pick.IS_Sharpe,
                    OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                    base_OOS_Sharpe=base_v2["OOS_Sharpe"], base_OOS_CAGR=base_v2["OOS_CAGR"],
                    base_OOS_MaxDD=base_v2["OOS_MaxDD"],
                    spy_OOS_Sharpe=spy["OOS_Sharpe"], spy_OOS_CAGR=spy["OOS_CAGR"],
                    spy_OOS_MaxDD=spy["OOS_MaxDD"],
                    S4_f=per["S4"].f, S4_OOS_Sharpe=per["S4"].OOS_Sharpe,
                    noDBC_f=per["noDBC"].f, noDBC_OOS_Sharpe=per["noDBC"].OOS_Sharpe,
                    oos_gap_noDBC_minus_S4=per["noDBC"].OOS_Sharpe - per["S4"].OOS_Sharpe,
                    beats_base=pick.OOS_Sharpe > base_v2["OOS_Sharpe"],
                    beats_spy=pick.OOS_Sharpe > spy["OOS_Sharpe"],
                    pass_4a=bool(pick.pass_4a), pass_4b=bool(pick.pass_4b)))
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    print(fmt(W.set_index(["universe", "book", "conv"])))
    print(f"\nrule-8 pick is noDBC in {int((W.pick_sleeve=='noDBC').sum())}/{len(W)} cells; "
          f"beats RULES v2 OOS {int(W.beats_base.sum())}/{len(W)}; beats SPY OOS "
          f"{int(W.beats_spy.sum())}/{len(W)}; 4a {int(W.pass_4a.sum())}/{len(W)}; "
          f"4b {int(W.pass_4b.sum())}/{len(W)}")
    print(f"OOS gap noDBC - S4 (each sleeve's own IS-best f): mean "
          f"{W.oos_gap_noDBC_minus_S4.mean():+.4f}, positive "
          f"{int((W.oos_gap_noDBC_minus_S4>0).sum())}/{len(W)}")

    # ================================================================ KEEP PATHS
    print("\n" + "=" * 118)
    print("KEEP PATHS (both, at 10 bps, over the whole reported grid)")
    print(f"4a passes: {int(G.pass_4a.sum())}/{len(G)}   4b passes: {int(G.pass_4b.sum())}/{len(G)}")
    if G.pass_4b.any():
        print("\n4b passers:")
        print(fmt(G[G.pass_4b][["universe", "book", "conv", "sleeve", "f", "CAGR", "Sharpe",
                                "MaxDD", "H1", "H2", "OOS_Sharpe"]]))
    if G.pass_4a.any():
        print("\n4a passers:")
        print(fmt(G[G.pass_4a][["universe", "book", "conv", "sleeve", "f", "CAGR", "Sharpe",
                                "MaxDD", "H1", "H2", "OOS_Sharpe"]]))
    print("\ncost ladder — passes by rung:")
    print(fmt(L.groupby(["cost_bps"])[["pass_4a", "pass_4b"]].sum()))
    print("\ncost ladder — passes by (sleeve, rung):")
    print(fmt(L.groupby(["sleeve", "cost_bps"])[["pass_4a", "pass_4b"]].sum()))

    # headline cell for the memo: idea 101/104's own arm, top20, g1.00, f=0.50
    print("\n" + "=" * 118)
    print(f"IDEA 101/104's OWN CELL (top20, g1.00, f={F_STAR}) — S4 vs noDBC side by side")
    hd = G[(G.book == "top20") & (G.conv == "g1.00") & (G.f == F_STAR)
           & (G.sleeve != "DBConly")]
    print(fmt(hd.set_index(["universe", "sleeve"])
              [["CAGR", "Sharpe", "MaxDD", "H1", "H2", "CON_Sharpe", "POST_Sharpe",
                "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "turnover_yr", "pass_4a", "pass_4b"]]))
    print(f"\nwrote {OUT}.grid.csv / .ladder.csv / .gaps.csv / .boundary.csv / .attrib.csv "
          f"/ .walkforward.csv")


if __name__ == "__main__":
    main()
