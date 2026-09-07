#!/usr/bin/env python3
"""QUEUE idea 105 — is-it-gold-or-any-real-asset (cloud, 2026-09-07).

Question (QUEUE.md wording)
---------------------------
"idea 102 found GLD carries 53% of S4's return and deleting it retains only 25-54% of the
sleeve's dSharpe, so the 'multi-asset diversifier' claim is really a gold claim.  Test
GLD-only, GLD+UUP, and GLD swapped for SLV/IAU at f=0.50 on both universes: is the exposure
gold specifically, a precious-metals factor, or any non-dollar real asset?  Max 2 params.
Blocks any RULES wording that says 'macro sleeve'."

DATA DEVIATION, STATED UP FRONT: **IAU is not in either cached panel** (research/universe.json
or research/universe_broad.json) and the cloud sandbox has no network, so it cannot be added.
IAU is a same-underlying gold ETF, so its arm would have been a redundancy check rather than a
discriminating one.  The precious-metals question is instead carried by SLV (silver, in both
panels) and GDX (gold miners, in both panels) — one non-gold precious metal and one levered
gold-equity proxy, which is a STRONGER test of "precious-metals factor" than IAU would have
been.  The broad-real-asset question is carried by DBC, USO, XLE and TIP.

The three hypotheses, pre-registered
------------------------------------
H_GOLD    the exposure is GLD specifically: swapping GLD out for anything collapses the sleeve.
H_METALS  it is a precious-metals factor: GLD, SLV (and GDX) all work, broad real assets do not.
H_REAL    it is any non-dollar real asset: DBC / USO / XLE / TIP swaps work about as well.
A fourth null must be excluded before any of them can be believed:
H_DOLLAR  it is UUP, and GLD is the passenger (idea 102 found UUP carried 2022, +4.81%).

Design (PROTOCOL rules 1-9)
---------------------------
Panels      : load_universe() (u56) and load_universe(broad=True) (136).  SURVIVORSHIP: both
              are current constituents, so equity levels are biased up; every sleeve asset is
              an ETF and is not exposed to it, and the bias hits all arms identically.
TUNED (2)   : sleeve composition (15 arms below) x f in {0, .25, .50, .75, 1.00}.  f=0.50 is
              the queue's pre-registered headline; the whole f-grid is reported so nothing is
              hidden, and rule 8 selects over the joint 15x5 surface.  ALL 600 points written.
CONTROLS    : book in {top20, ewall}, universe in {u56, broad}, gross convention in
              {natural, g1.00}, cost in {0,5,10,15,20,25} bps.  Reported, never selected on.
              Held at incumbent values: GROSS 0.75, cadence W, 60d vol window, (252,126,63)
              momentum lags, 10 bps headline, next-day execution (engine shifts weights).
Sleeve      : idea 18 variant B verbatim (trend vote in {0,1/3,2/3,1} x inverse-60d-vol risk
              parity, row-normalised), restricted to each arm's assets — identical machinery to
              ideas 100/102/103, so arms differ ONLY in which assets they may hold.
Rule 8      : (arm, f) chosen on 2009-2016 by IS Sharpe, 2017-2026 evaluated untouched, per
              (universe, book, convention).  OOS CAGR/Sharpe/MaxDD vs no-sleeve control,
              RULES v2 (live), RULES v1 and SPY.
Mechanism   : per-asset standalone stats + correlation to book, and a regression of each
              single-asset arm's f=0.50 dSharpe on (asset standalone Sharpe, asset-book
              correlation) — the two candidate explanations for why gold and not oil.

COST NOTE: engine.backtest applies costs as gross_returns - turnover * bps/1e4 with a
bps-independent holdings path, so each weight matrix is run ONCE at 0 bps and every rung of
the ladder derived exactly.  Asserted against a direct 10 bps run at start-up.

KNOWN DATA CAVEAT (queue idea 38): data/prices*.csv are indexed on CALENDAR days after
2014-09-17 because BTC-USD is in the download, so post-2014 weekends are zero-return rows.
It hits every arm, the baseline and SPY identically — cross-arm comparisons are
apples-to-apples; absolute Sharpe levels wait on idea 38.

Deterministic, standalone:
    python research/backtests/2026-09-07_is-it-gold-or-any-real-asset_cloud.py
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd

from baseline import load_universe, rules_v1_weights, rules_v2_weights, score
from engine import backtest, metrics  # noqa

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 900)

COST_BPS, FREQ, GROSS = 10, "W", 0.75
COST_LADDER = (0, 5, 10, 15, 20, 25)
MOM_LAGS, VOL_WINDOW = (252, 126, 63), 60
FGRID = [0.00, 0.25, 0.50, 0.75, 1.00]
F_STAR = 0.50
SPLIT, IS_END = "2017-01-01", "2016-12-31"
REGIME_SPLIT = "2022-01-01"
OUT = Path(__file__).with_suffix("")

# The arms.  Group A reproduces idea 102 (controls).  Group B isolates gold.  Group C swaps
# gold out of idea 102's best arm one asset at a time — this is the discriminating group.
SLEEVES = {
    # A — controls, reproducing idea 100 / idea 102
    "S4":          ["TLT", "GLD", "DBC", "UUP"],     # idea 100's sleeve
    "noDBC":       ["TLT", "GLD", "UUP"],            # idea 102's best arm (the PARK candidate)
    "noGLD":       ["TLT", "DBC", "UUP"],            # idea 102's gold-deletion control
    # B — is it gold on its own, or gold plus the dollar?
    "GLDonly":     ["GLD"],
    "GLD_UUP":     ["GLD", "UUP"],
    "UUPonly":     ["UUP"],                          # H_DOLLAR null
    "TLTonly":     ["TLT"],                          # idea 102's passenger, re-run as anchor
    # B2 — the precious-metals question (IAU unavailable; SLV and GDX carry it)
    "SLVonly":     ["SLV"],
    "SLV_UUP":     ["SLV", "UUP"],
    "GDXonly":     ["GDX"],
    # C — GLD swapped out of idea 102's best arm, one substitute at a time
    "sub_SLV":     ["TLT", "SLV", "UUP"],
    "sub_GDX":     ["TLT", "GDX", "UUP"],
    "sub_DBC":     ["TLT", "DBC", "UUP"],            # == noGLD; kept as the named substitution
    "sub_USO":     ["TLT", "USO", "UUP"],
    "sub_XLE":     ["TLT", "XLE", "UUP"],
    "sub_TIP":     ["TLT", "TIP", "UUP"],
}
GROUP = {"S4": "A", "noDBC": "A", "noGLD": "A",
         "GLDonly": "B", "GLD_UUP": "B", "UUPonly": "B", "TLTonly": "B",
         "SLVonly": "B2", "SLV_UUP": "B2", "GDXonly": "B2",
         "sub_SLV": "C", "sub_GDX": "C", "sub_DBC": "C", "sub_USO": "C",
         "sub_XLE": "C", "sub_TIP": "C"}
SINGLES = ["GLDonly", "SLVonly", "GDXonly", "UUPonly", "TLTonly"]
ASSETS = sorted({a for v in SLEEVES.values() for a in v})


# ---------------------------------------------------------------- sleeve / books
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
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    sub = px[assets]
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
    """natural = (1-f)E + fS as-is; g1.00 = the same rescaled per row to 1.0 gross
    (fully invested, NOT leverage — the convention under which idea 100/102's arm passes 4b)."""
    w = (1 - f) * E + f * S
    if conv == "natural":
        return w
    g = w.sum(axis=1)
    return w.mul((1.0 / g.where(g > 1e-12)).fillna(0.0), axis=0)


# ---------------------------------------------------------------- helpers
def run0(px, w, start):
    res = backtest(px, w, cost_bps=0.0, freq=FREQ)
    return res["returns"].loc[start:], res["turnover"].loc[start:]


def net(gr, to, bps=COST_BPS):
    return gr - to * bps / 1e4


def stats(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def full_row(r):
    h = len(r) // 2
    c, s, d = stats(r)
    _, h1, _ = stats(r.iloc[:h])
    _, h2, _ = stats(r.iloc[h:])
    _, is_, _ = stats(r.loc[:IS_END])
    oc, os_, od = stats(r.loc[SPLIT:])
    fc, fs, _ = stats(r.loc[:"2021-12-31"])
    rc, rs, _ = stats(r.loc[REGIME_SPLIT:])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=h1, H2=h2, IS_Sharpe=is_,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                FALL_CAGR=fc, FALL_Sharpe=fs, RISE_CAGR=rc, RISE_Sharpe=rs)


def keep_4a(row, base):
    return bool(row["H1"] > base["H1"] and row["H2"] > base["H2"] and row["MaxDD"] >= base["MaxDD"])


def keep_4b(row, spy):
    return bool(row["H1"] > spy["H1"] and row["H2"] > spy["H2"] and row["OOS_Sharpe"] > spy["OOS_Sharpe"]
                and row["MaxDD"] >= 0.60 * spy["MaxDD"] and row["CAGR"] >= 0.70 * spy["CAGR"])


def ols(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 3:
        return np.nan, np.nan, np.nan, 0
    b = np.polyfit(x, y, 1)
    ss = ((y - y.mean()) ** 2).sum()
    return float(b[0]), float(b[1]), float(1 - ((y - np.polyval(b, x)) ** 2).sum() / ss if ss > 0 else np.nan), len(x)


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.4f}")


# ---------------------------------------------------------------- main
def main():
    universes = {"u56": load_universe(), "broad": load_universe(broad=True)}

    px0 = universes["u56"]
    st0 = px0.index[260]
    w0 = book_top20(px0)
    gr0, to0 = run0(px0, w0, st0)
    direct = backtest(px0, w0, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[st0:]
    err = float((net(gr0, to0) - direct).abs().max())
    print(f"[gate] cost linearity max |derived - direct| at {COST_BPS} bps = {err:.3e}")
    assert err < 1e-12, "cost is not linear in this engine — ladder derivation invalid"

    print(f"[gate] IAU present in u56? {'IAU' in universes['u56'].columns} | "
          f"in broad? {'IAU' in universes['broad'].columns}  "
          "-> the queue's IAU arm cannot be run; SLV and GDX carry the metals question.")
    for tag, px in universes.items():
        miss = [a for a in ASSETS if a not in px.columns]
        print(f"[gate] {tag}: missing sleeve assets {miss if miss else 'none'}")
        if miss:
            raise SystemExit(f"cannot run: {tag} lacks {miss}")

    print(f"[grid] {len(SLEEVES)} arms x {len(FGRID)} f x {len(BOOKS)} books x 2 conventions x "
          f"2 universes = {len(SLEEVES)*len(FGRID)*len(BOOKS)*2*2} points")
    for k, v in SLEEVES.items():
        print(f"   [{GROUP[k]}] {k:10s} {' '.join(v)}")

    records, refs, cache = [], {}, {}
    for tag, px in universes.items():
        start = px.index[260]
        print("\n" + "=" * 122)
        print(f"### UNIVERSE {tag}: {px.shape[1]} tickers, {px.index[0].date()} -> "
              f"{px.index[-1].date()} | eval from {start.date()}")
        bgr, bto = run0(px, rules_v2_weights(px), start)
        base = full_row(net(bgr, bto))
        v1gr, v1to = run0(px, rules_v1_weights(px), start)
        v1 = full_row(net(v1gr, v1to))
        spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
        spy = full_row(spy_r)
        refs[tag] = (base, v1, spy)
        print("\nReference rows (same days, same 10 bps):")
        print(fmt(pd.DataFrame({"RULES v2 (live baseline)": base, "RULES v1": v1, "SPY": spy}).T))
        print(f"4b bars: Sharpe > SPY H1 {spy['H1']:.3f} / H2 {spy['H2']:.3f} / OOS "
              f"{spy['OOS_Sharpe']:.3f} · MaxDD >= {0.60*spy['MaxDD']:.1%} · "
              f"CAGR >= {0.70*spy['CAGR']:.2%}")

        S_w = {s: sleeve_weights(px, a) for s, a in SLEEVES.items()}
        for bname, bfn in BOOKS.items():
            E = bfn(px)
            for conv in ("natural", "g1.00"):
                for sname in SLEEVES:
                    for f in FGRID:
                        w = blend(E, S_w[sname], f, conv)
                        gr, to = run0(px, w, start)
                        cache[(tag, bname, conv, sname, f)] = (gr, to)
                        r = net(gr, to)
                        row = full_row(r)
                        row["Turn_yr"] = to.sum() / (len(r) / 252)
                        row["Gross"] = w.loc[start:].sum(axis=1).mean()
                        row["p4a"] = keep_4a(row, base)
                        row["p4b"] = keep_4b(row, spy)
                        records.append(dict(universe=tag, book=bname, conv=conv, sleeve=sname,
                                            group=GROUP[sname], f=f, **row))
        print(f"    grid done: {len([r for r in records if r['universe']==tag])} points")

    G = pd.DataFrame(records)
    G.to_csv(f"{OUT}.grid.csv", index=False)

    # ---------------------------------------------------------- reproduction gates
    print("\n" + "=" * 122)
    print("### REPRODUCTION GATES (idea 100 / idea 102 published numbers, recomputed here)")
    for (u, b, cv, s, f), label in [
            (("u56", "top20", "g1.00", "S4", 0.50), "idea 100 u56 top20+50% S4 @ g=1.00"),
            (("broad", "top20", "g1.00", "S4", 0.50), "idea 100 broad top20+50% S4 @ g=1.00"),
            (("u56", "top20", "g1.00", "noDBC", 0.50), "idea 102 u56 top20+50% (TLT,GLD,UUP) g=1.00"),
            (("broad", "top20", "g1.00", "noDBC", 0.50), "idea 102 broad same")]:
        r = G[(G.universe == u) & (G.book == b) & (G.conv == cv) & (G.sleeve == s) & (G.f == f)].iloc[0]
        print(f"  {label:46s} {r.CAGR:6.1%} / {r.Sharpe:.3f} / {r.MaxDD:6.1%} / "
              f"H {r.H1:.3f}/{r.H2:.3f} / OOS {r.OOS_CAGR:5.1%} {r.OOS_Sharpe:.3f} {r.OOS_MaxDD:6.1%} "
              f"/ {r.Turn_yr:.1f}x / 4a {bool(r.p4a)} 4b {bool(r.p4b)}")

    # ---------------------------------------------------------- (1) the assets themselves
    print("\n" + "=" * 122)
    print("### (1) THE CANDIDATE ASSETS, BUY-AND-HOLD, AND THEIR CORRELATION TO THE BOOK")
    print("  Before any sleeve machinery: what are these things on their own?\n")
    ar = []
    for tag, px in universes.items():
        start = px.index[260]
        bk = net(*run0(px, book_top20(px), start))
        for a in ASSETS:
            r = px[a].pct_change().fillna(0).loc[start:]
            c, s, d = stats(r)
            fc, fs, _ = stats(r.loc[:"2021-12-31"])
            rc, rs, _ = stats(r.loc[REGIME_SPLIT:])
            ar.append(dict(universe=tag, asset=a, CAGR=c, Sharpe=s, MaxDD=d,
                           FALL_CAGR=fc, RISE_CAGR=rc, RISE_Sharpe=rs,
                           corr_book=float(np.corrcoef(r, bk)[0, 1]),
                           corr_spy=float(np.corrcoef(r, px["SPY"].pct_change().fillna(0).loc[start:])[0, 1])))
    A = pd.DataFrame(ar)
    A.to_csv(f"{OUT}.assets.csv", index=False)
    print(fmt(A.set_index(["universe", "asset"])[
        ["CAGR", "Sharpe", "MaxDD", "FALL_CAGR", "RISE_CAGR", "RISE_Sharpe", "corr_book", "corr_spy"]]))

    # ---------------------------------------------------------- (2) the substitution test
    print("\n" + "=" * 122)
    print(f"### (2) THE SUBSTITUTION TEST at the pre-registered f={F_STAR:.2f}")
    print("  dSharpe = Sharpe(blend) - Sharpe(the same book alone, same convention), 8 cells")
    print("  (2 universes x 2 books x 2 conventions).  Retention is against noDBC = idea 102's")
    print("  best arm, the arm each 'sub_*' row substitutes gold out of.\n")
    dl = []
    for (u, b, cv), sub in G[G.f == F_STAR].groupby(["universe", "book", "conv"]):
        b0 = G[(G.universe == u) & (G.book == b) & (G.conv == cv) & (G.f == 0.0)].iloc[0]
        for r in sub.itertuples():
            dl.append(dict(universe=u, book=b, conv=cv, sleeve=r.sleeve, group=GROUP[r.sleeve],
                           dSharpe=r.Sharpe - b0.Sharpe, dCAGR=r.CAGR - b0.CAGR,
                           dMaxDD=r.MaxDD - b0.MaxDD, Sharpe=r.Sharpe, CAGR=r.CAGR,
                           MaxDD=r.MaxDD, OOS_Sharpe=r.OOS_Sharpe, p4a=r.p4a, p4b=r.p4b))
    DL = pd.DataFrame(dl)
    ref = DL[DL.sleeve == "noDBC"].set_index(["universe", "book", "conv"]).dSharpe
    DL["ref_dSharpe"] = [ref.loc[(r.universe, r.book, r.conv)] for r in DL.itertuples()]
    DL["retention"] = DL.dSharpe / DL.ref_dSharpe
    DL.to_csv(f"{OUT}.substitution.csv", index=False)
    S = DL.groupby(["group", "sleeve"]).agg(
        dSharpe_mean=("dSharpe", "mean"), dSharpe_min=("dSharpe", "min"), dSharpe_max=("dSharpe", "max"),
        pos=("dSharpe", lambda v: int((v > 0).sum())), n=("dSharpe", "size"),
        retention_mean=("retention", "mean"), dCAGR_mean=("dCAGR", "mean"),
        dMaxDD_mean=("dMaxDD", "mean"), p4a=("p4a", "sum"), p4b=("p4b", "sum")
    ).sort_values(["group", "dSharpe_mean"], ascending=[True, False])
    print(fmt(S))

    print("\n  THE DISCRIMINATING ROWS — group C, gold swapped out of (TLT,?,UUP):")
    Cg = S.loc["C"].copy()
    gold = S.loc[("A", "noDBC")]
    print(f"    gold arm  noDBC (TLT,GLD,UUP): dSharpe {gold.dSharpe_mean:+.4f}, "
          f"positive {int(gold.pos)}/{int(gold.n)}, 4b {int(gold.p4b)}/8")
    for s, r in Cg.iterrows():
        print(f"    {s:10s} dSharpe {r.dSharpe_mean:+.4f}  retains {r.retention_mean:6.1%}  "
              f"positive {int(r.pos)}/{int(r.n)}  4b {int(r.p4b)}/8")
    print("\n  VERDICT ARITHMETIC (mean dSharpe at f=0.50, all 8 cells):")
    print(f"    H_GOLD   gold arms  : GLDonly {S.loc[('B','GLDonly')].dSharpe_mean:+.4f}, "
          f"GLD_UUP {S.loc[('B','GLD_UUP')].dSharpe_mean:+.4f}, noDBC {gold.dSharpe_mean:+.4f}")
    print(f"    H_METALS metal arms : SLVonly {S.loc[('B2','SLVonly')].dSharpe_mean:+.4f}, "
          f"SLV_UUP {S.loc[('B2','SLV_UUP')].dSharpe_mean:+.4f}, "
          f"GDXonly {S.loc[('B2','GDXonly')].dSharpe_mean:+.4f}, "
          f"sub_SLV {S.loc[('C','sub_SLV')].dSharpe_mean:+.4f}, "
          f"sub_GDX {S.loc[('C','sub_GDX')].dSharpe_mean:+.4f}")
    print(f"    H_REAL   broad real : sub_DBC {S.loc[('C','sub_DBC')].dSharpe_mean:+.4f}, "
          f"sub_USO {S.loc[('C','sub_USO')].dSharpe_mean:+.4f}, "
          f"sub_XLE {S.loc[('C','sub_XLE')].dSharpe_mean:+.4f}, "
          f"sub_TIP {S.loc[('C','sub_TIP')].dSharpe_mean:+.4f}")
    print(f"    H_DOLLAR null       : UUPonly {S.loc[('B','UUPonly')].dSharpe_mean:+.4f}  "
          f"(TLTonly {S.loc[('B','TLTonly')].dSharpe_mean:+.4f}, idea 102's passenger)")

    # ---------------------------------------------------------- (3) mechanism
    print("\n" + "=" * 122)
    print("### (3) MECHANISM — is it the asset's own Sharpe, or its correlation to the book?")
    print("  Regress each single-asset arm's f=0.50 dSharpe on the asset's own standalone Sharpe")
    print("  and on its correlation to the book.  If gold is special, neither should explain it.\n")
    mech = []
    for r in DL[DL.sleeve.isin(SINGLES)].itertuples():
        a = SLEEVES[r.sleeve][0]
        arow = A[(A.universe == r.universe) & (A.asset == a)].iloc[0]
        mech.append(dict(universe=r.universe, book=r.book, conv=r.conv, asset=a,
                         dSharpe=r.dSharpe, asset_Sharpe=arow.Sharpe, corr_book=arow.corr_book,
                         asset_CAGR=arow.CAGR))
    MECH = pd.DataFrame(mech)
    MECH.to_csv(f"{OUT}.mechanism.csv", index=False)
    print(fmt(MECH.groupby("asset").agg(dSharpe=("dSharpe", "mean"),
                                        asset_Sharpe=("asset_Sharpe", "mean"),
                                        corr_book=("corr_book", "mean"),
                                        asset_CAGR=("asset_CAGR", "mean"))))
    for xv in ("asset_Sharpe", "corr_book"):
        sl, ic, r2, n = ols(MECH[xv], MECH.dSharpe)
        print(f"  dSharpe ~ {xv:12s}: slope {sl:+.4f}, intercept {ic:+.4f}, R2 {r2:.4f}, n={n}")
    resid = MECH.dSharpe - np.polyval(np.polyfit(MECH.asset_Sharpe, MECH.dSharpe, 1), MECH.asset_Sharpe)
    print("  residual dSharpe after removing the asset's own Sharpe, by asset "
          "(a positive residual = the asset does more than its Sharpe explains):")
    print(fmt(pd.Series(resid.values, index=MECH.asset).groupby(level=0).mean().to_frame("resid")))

    # ---------------------------------------------------------- (4) rule 8
    print("\n" + "=" * 122)
    print("### (4) RULE 8 — (arm, f) chosen on 2009-2016 by IS Sharpe, 2017-2026 untouched")
    wf = []
    for (u, b, cv), sub in G.groupby(["universe", "book", "conv"]):
        base, v1, spy = refs[u]
        ctrl = sub[(sub.f == 0.0) & (sub.sleeve == "S4")].iloc[0]
        pick = sub[sub.f > 0].iloc[int(np.argmax(sub[sub.f > 0].IS_Sharpe.values))]
        # pre-registered f=0.50 headline arm, chosen among arms on IS Sharpe only
        p50 = sub[sub.f == F_STAR]
        pick50 = p50.iloc[int(np.argmax(p50.IS_Sharpe.values))]
        for nm, p in (("joint(arm,f)", pick), (f"arm@f={F_STAR}", pick50)):
            wf.append(dict(universe=u, book=b, conv=cv, chooser=nm, sleeve=p.sleeve, f=p.f,
                           IS_Sharpe=p.IS_Sharpe, CAGR=p.CAGR, Sharpe=p.Sharpe, MaxDD=p.MaxDD,
                           H1=p.H1, H2=p.H2, OOS_CAGR=p.OOS_CAGR, OOS_Sharpe=p.OOS_Sharpe,
                           OOS_MaxDD=p.OOS_MaxDD, Turn_yr=p.Turn_yr, p4a=p.p4a, p4b=p.p4b,
                           ctrl_OOS_Sharpe=ctrl.OOS_Sharpe, ctrl_OOS_CAGR=ctrl.OOS_CAGR,
                           spy_OOS_Sharpe=spy["OOS_Sharpe"], spy_OOS_CAGR=spy["OOS_CAGR"],
                           spy_OOS_MaxDD=spy["OOS_MaxDD"], v2_OOS_Sharpe=base["OOS_Sharpe"],
                           v1_OOS_Sharpe=v1["OOS_Sharpe"],
                           best_OOS_in_cell=sub[sub.f > 0].OOS_Sharpe.max()))
    W = pd.DataFrame(wf)
    W["regret"] = W.OOS_Sharpe - W.best_OOS_in_cell
    W["vs_ctrl"] = W.OOS_Sharpe - W.ctrl_OOS_Sharpe
    W["vs_spy"] = W.OOS_Sharpe - W.spy_OOS_Sharpe
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    print(fmt(W.set_index(["chooser", "universe", "book", "conv"])[
        ["sleeve", "f", "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "ctrl_OOS_Sharpe",
         "spy_OOS_Sharpe", "v2_OOS_Sharpe", "vs_ctrl", "vs_spy", "regret", "p4b"]]))
    print("\n  Which arm does IS selection reach for?")
    print(fmt(W.groupby(["chooser", "sleeve"]).size().to_frame("cells")))
    print("\n  Chooser summary:")
    print(fmt(W.groupby("chooser").agg(
        n=("OOS_Sharpe", "size"), mean_OOS_Sharpe=("OOS_Sharpe", "mean"),
        mean_OOS_CAGR=("OOS_CAGR", "mean"), mean_OOS_MaxDD=("OOS_MaxDD", "mean"),
        beats_ctrl=("vs_ctrl", lambda v: int((v > 0).sum())),
        beats_spy=("vs_spy", lambda v: int((v > 0).sum())),
        mean_regret=("regret", "mean"), p4a=("p4a", "sum"), p4b=("p4b", "sum"))))

    print("\n  OOS Sharpe of every arm at the pre-registered f=0.50 (NOT selected on — reported):")
    print(fmt(G[G.f == F_STAR].groupby(["group", "sleeve"]).agg(
        OOS_Sharpe=("OOS_Sharpe", "mean"), OOS_CAGR=("OOS_CAGR", "mean"),
        OOS_MaxDD=("OOS_MaxDD", "mean"), full_Sharpe=("Sharpe", "mean"),
        beats_spy_OOS=("OOS_Sharpe", lambda v: int(sum(
            x > refs[u][2]["OOS_Sharpe"] for x, u in zip(v, G[G.f == F_STAR].universe))))
    ).sort_values("OOS_Sharpe", ascending=False)))

    # ---------------------------------------------------------- (5) KEEP paths + cost
    print("\n" + "=" * 122)
    print(f"### (5) KEEP PATHS over all {len(G)} grid points (both reported, neither selected on)")
    kp = G.groupby(["universe", "conv"]).agg(n=("p4b", "size"), p4a=("p4a", "sum"), p4b=("p4b", "sum"))
    print(fmt(kp))
    kp.to_csv(f"{OUT}.keeppaths.csv")
    p4b = G[G.p4b]
    if len(p4b):
        print(f"\n  {len(p4b)} points clear 4b, by arm:")
        print(fmt(p4b.groupby(["group", "sleeve"]).agg(
            n_4b=("f", "size"), fs=("f", lambda v: sorted(set(v))),
            universes=("universe", lambda v: sorted(set(v))))))
        print("\n  CROSS-UNIVERSE 4b (an arm/f/book/conv that passes on BOTH panels):")
        xu = p4b.groupby(["sleeve", "f", "book", "conv"]).universe.nunique()
        xu = xu[xu == 2]
        if len(xu):
            for (s, f, b, cv) in xu.index:
                rows = G[(G.sleeve == s) & (G.f == f) & (G.book == b) & (G.conv == cv)]
                print(f"    {s} f={f} {b} {cv}:")
                print(fmt(rows.set_index("universe")[["CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                                      "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "Turn_yr"]]))
        else:
            print("    none.")
    else:
        print("  no point clears 4b.")

    print("\n  COST LADDER on every f=0.50 arm (cross-universe 4b pass count by bps, top20+g1.00):")
    cl = []
    for r in G[(G.f == F_STAR)].itertuples():
        base, v1, spy = refs[r.universe]
        gr, to = cache[(r.universe, r.book, r.conv, r.sleeve, r.f)]
        for bps in COST_LADDER:
            row = full_row(net(gr, to, bps))
            cl.append(dict(universe=r.universe, book=r.book, conv=r.conv, sleeve=r.sleeve,
                           group=GROUP[r.sleeve], bps=bps, Sharpe=row["Sharpe"],
                           OOS_Sharpe=row["OOS_Sharpe"], CAGR=row["CAGR"],
                           p4b=keep_4b(row, spy), p4a=keep_4a(row, base)))
    CL = pd.DataFrame(cl)
    CL.to_csv(f"{OUT}.costladder.csv", index=False)
    sel = CL[(CL.book == "top20") & (CL.conv == "g1.00")]
    piv = sel.pivot_table(index=["group", "sleeve"], columns="bps", values="p4b", aggfunc="sum")
    print(fmt(piv))
    print("  (values are 4b passes out of 2 universes at that cost rung)")

    print("\n" + "=" * 122)
    print("### ARTEFACTS")
    for s in (".grid.csv", ".assets.csv", ".substitution.csv", ".mechanism.csv",
              ".walkforward.csv", ".keeppaths.csv", ".costladder.csv"):
        print(f"   {OUT.name}{s}")


if __name__ == "__main__":
    main()
