#!/usr/bin/env python3
"""Idea 1457 (lane cloud, 2026-09-22): how many committed NEUTRALITY / MATCH claims in the
record are scored against a MARGINAL SE when the contrast is PAIRED?

Idea 1444 found the anchor's marginal block-bootstrap CAGR SE is 9.1x / 10.8x / 11.6x wider
than the PAIRED SE of the very same difference on U56 / B136 / SMALL, and that the U56
CAGR-neutral frontier is non-empty under the first ruler and empty under the second.  Every
"matched to within its own SE" / "indistinguishable from" verdict in the record is exposed.

This run does not census prose.  It rebuilds a REAL book grid (RULES v2's band book over a
band x gross ladder) on three panels, forms every pairwise contrast, and scores each
contrast's MATCHED / DISTINGUISHABLE verdict under BOTH rulers FROM THE SAME BOOTSTRAP
DRAWS, so the two rulers differ only in whether the draw is shared.  A marginal ruler that
is merely WIDER changes nothing; only a ruler that moves a VERDICT, and above all one that
moves the rule-8 PICK, reaches capital.

CAPITAL ARM (rule 8): the ruler is turned into a real chooser.  Parameters are chosen on
2009-2016 ONLY; 2017-2026 is read ONCE.  Among the books whose IS Sharpe is inside 2*SE of
the IS leader (the "matched set" -- wide under the marginal ruler, narrow under the paired
one) the chooser takes the shallowest IS MaxDD.  Both picks are scored OOS against the live
RULES v2 baseline and against SPY, on BOTH KEEP paths, at every cost rung.

EXACT COST LADDER.  `engine.backtest` builds `held` and `turnover` independently of
cost_bps and then subtracts `turnover * cost_bps / 1e4`, so ONE zero-cost run per book
yields every rung exactly: r(c) = r(0) - turnover * c / 1e4.

Two tuned dials and no more: the SE RULER (marginal vs paired) and the BLOCK LENGTH L.
Panel, cost rung, band and gross are REPORTED at every grid point, never selected on.

SURVIVORSHIP (rule 9): U56 / B136 are current-constituent lists held from 2008 and SMALL is
a current sub-$2B screen held from 2010, so every absolute level is optimistic.  The
RULER CONTRAST is same-tape, same-book and first-order immune; the pass counts are not.

Usage (the sandbox throttles background work, so panels run one per invocation):
    python <this> U56 | B136 | SMALL      -> compute and cache that panel
    python <this> REPORT                  -> aggregate and print every table
Deterministic: fixed seed, no network.
"""
import sys, itertools, pickle
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa
from engine import backtest  # noqa

SLUG = "2026-09-22_paired-vs-marginal-se-ruler_cloud"
CACHE = ROOT / "research" / "backtests" / ".cache_1457"
SEED = 20260922
NBOOT = 1000
BLOCKS = [5, 10, 21, 63, 126]          # tuned dial 2
RULERS = ["marginal", "paired"]        # tuned dial 1
BANDS = [0.01, 0.02, 0.03, 0.05, 0.08]
GROSS = [0.50, 0.75, 1.00]
COSTS = [0, 10, 25, 50]                # reported, never selected on
LIVE = (0.03, 0.75)                    # the live RULES v2 book
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
pd.set_option("display.width", 240)


def cagr(r):
    eq = float(np.prod(1.0 + r)); yrs = len(r) / 252.0
    return eq ** (1.0 / yrs) - 1.0 if eq > 0 else -1.0


def sharpe(r):
    sd = r.std()
    return float(r.mean() * 252.0 / (sd * np.sqrt(252.0))) if sd > 0 else np.nan


def maxdd(r):
    eq = np.cumprod(1.0 + r)
    return float((eq / np.maximum.accumulate(eq) - 1.0).min())


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    print(f"SMALL: dropped {len(px.columns)-len(keep)} tickers with max_1d_move >= 1.0; "
          f"{len(keep)-1} names + SPY.  SURVIVORSHIP: current constituents of the screen only.")
    return px[keep]


PANELS = {"U56": lambda: load_universe(),
          "B136": lambda: load_universe(broad=True),
          "SMALL": small_panel}
BOOKS = [(b, g) for b in BANDS for g in GROSS]


def build(name):
    px = PANELS[name]()
    print(f"PANEL {name}: {px.shape[0]} x {px.shape[1]}  {px.index[0].date()} -> {px.index[-1].date()}")
    start = px.index[260]
    out = {}
    for (b, g) in BOOKS:
        res = backtest(px, rules_v2_weights(px, band=b, gross=g), cost_bps=0.0, freq="W")
        out[(b, g)] = (res["returns"].loc[start:].astype(float),
                       res["turnover"].loc[start:].astype(float))
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    CACHE.mkdir(exist_ok=True)
    with open(CACHE / f"{name}.pkl", "wb") as f:
        pickle.dump(dict(books=out, spy=spy), f)
    print(f"cached {name}: {len(out)} books")


def at_cost(pair, c, sl=None):
    r = pair[0] - pair[1] * c / 1e4
    return (r.loc[sl] if sl is not None else r).values


def boot_index(T, L, nboot, rng):
    """Circular moving-block bootstrap index matrix, shape (nboot, T)."""
    nblk = int(np.ceil(T / L))
    starts = rng.integers(0, T, size=(nboot, nblk))
    idx = (starts[:, :, None] + np.arange(L)[None, None, :]) % T
    return idx.reshape(nboot, nblk * L)[:, :T]


def boot_stats(r, idx):
    x = r[idx]
    yrs = x.shape[1] / 252.0
    eq = np.exp(np.log1p(x).sum(axis=1))
    cg = np.where(eq > 0, eq ** (1.0 / yrs) - 1.0, -1.0)
    sd = x.std(axis=1)
    sh = np.where(sd > 0, x.mean(axis=1) * np.sqrt(252.0) / sd, np.nan)
    return cg, sh


def keep_paths(r, base, spy):
    h, hb, hs = len(r) // 2, len(base) // 2, len(spy) // 2
    s1, s2 = sharpe(r[:h]), sharpe(r[h:])
    a = (s1 > sharpe(base[:hb])) and (s2 > sharpe(base[hb:])) and (maxdd(r) >= maxdd(base))
    b = ((s1 > sharpe(spy[:hs])) and (s2 > sharpe(spy[hs:]))
         and (maxdd(r) >= 0.60 * maxdd(spy)) and (cagr(r) >= 0.70 * cagr(spy)))
    return a, b, dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), H1=s1, H2=s2)


def ruler_table(P, panel, cost=10):
    R = {k: at_cost(P["books"][k], cost) for k in BOOKS}
    T = len(R[LIVE]); rng = np.random.default_rng(SEED); rows = []
    for L in BLOCKS:
        idx = boot_index(T, L, NBOOT, rng)
        bs = {k: boot_stats(R[k], idx) for k in BOOKS}
        obs = {k: (cagr(R[k]), sharpe(R[k])) for k in BOOKS}
        for a, b in itertools.combinations(BOOKS, 2):
            for si, sname in ((0, "CAGR"), (1, "Sharpe")):
                xa, xb = bs[a][si], bs[b][si]
                d = obs[a][si] - obs[b][si]
                sm = float(np.sqrt(np.nanvar(xa, ddof=1) + np.nanvar(xb, ddof=1)))
                sp = float(np.nanstd(xa - xb, ddof=1))
                rows.append(dict(panel=panel, L=L, stat=sname,
                                 A=f"b{a[0]:.2f}g{a[1]:.2f}", B=f"b{b[0]:.2f}g{b[1]:.2f}",
                                 d=d, se_marginal=sm, se_paired=sp,
                                 ratio=sm / sp if sp > 0 else np.nan,
                                 matched_marginal=abs(d) < 2 * sm,
                                 matched_paired=abs(d) < 2 * sp))
    return pd.DataFrame(rows)


def rule8(P, panel, cost=10):
    out = []
    IS = {k: at_cost(P["books"][k], cost, slice(None, IS_END)) for k in BOOKS}
    T = len(IS[LIVE])
    is_sh = {k: sharpe(IS[k]) for k in BOOKS}
    is_dd = {k: maxdd(IS[k]) for k in BOOKS}
    lead = max(BOOKS, key=lambda k: is_sh[k])
    for L in BLOCKS:
        rng = np.random.default_rng(SEED + L)
        idx = boot_index(T, L, NBOOT, rng)
        bs = {k: boot_stats(IS[k], idx)[1] for k in BOOKS}
        for ruler in RULERS:
            if ruler == "paired":
                se = {k: float(np.nanstd(bs[lead] - bs[k], ddof=1)) for k in BOOKS}
            else:
                vl = np.nanvar(bs[lead], ddof=1)
                se = {k: float(np.sqrt(vl + np.nanvar(bs[k], ddof=1))) for k in BOOKS}
            mset = [k for k in BOOKS if is_sh[lead] - is_sh[k] < 2 * se[k]]
            pick = max(mset, key=lambda k: is_dd[k])
            oos = at_cost(P["books"][pick], cost, slice(OOS_START, None))
            out.append(dict(panel=panel, L=L, ruler=ruler, n_matched=len(mset),
                            se_med=float(np.median(list(se.values()))),
                            lead=f"b{lead[0]:.2f}g{lead[1]:.2f}",
                            pick=f"b{pick[0]:.2f}g{pick[1]:.2f}", pick_tuple=pick,
                            oos_CAGR=cagr(oos), oos_Sharpe=sharpe(oos), oos_MaxDD=maxdd(oos)))
    return pd.DataFrame(out)


def report():
    panels = {}
    for n in PANELS:
        with open(CACHE / f"{n}.pkl", "rb") as f:
            panels[n] = pickle.load(f)
    RU = pd.concat([ruler_table(panels[n], n) for n in PANELS], ignore_index=True)
    R8 = pd.concat([rule8(panels[n], n) for n in PANELS], ignore_index=True)

    print("\n" + "#" * 108)
    print("# A.  RULER WIDTH.  marginal / paired SE of the SAME contrast, SAME draws. 10 bps, weekly.")
    print("#" * 108)
    print(RU.groupby(["panel", "L", "stat"]).agg(
        n_pairs=("ratio", "size"), ratio_med=("ratio", "median"), ratio_min=("ratio", "min"),
        ratio_max=("ratio", "max"), se_marg_med=("se_marginal", "median"),
        se_pair_med=("se_paired", "median")).reset_index().to_string(
        index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n" + "#" * 108)
    print("# B.  VERDICT FLIPS.  MATCHED under the marginal ruler, DISTINGUISHABLE under the")
    print("#     paired one (and the reverse).  ALL grid points reported.")
    print("#" * 108)
    RU["flip"] = RU["matched_marginal"] & ~RU["matched_paired"]
    RU["flip_back"] = ~RU["matched_marginal"] & RU["matched_paired"]
    f = RU.groupby(["panel", "L", "stat"]).agg(
        n=("flip", "size"), matched_marginal=("matched_marginal", "sum"),
        matched_paired=("matched_paired", "sum"), flips_M_to_D=("flip", "sum"),
        flips_D_to_M=("flip_back", "sum")).reset_index()
    f["flip_share_of_matched"] = f["flips_M_to_D"] / f["matched_marginal"].replace(0, np.nan)
    print(f.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"\nPOOLED over all {len(RU)} contrast-rows: matched_marginal "
          f"{int(RU.matched_marginal.sum())}, matched_paired {int(RU.matched_paired.sum())}, "
          f"M->D flips {int(RU.flip.sum())} ({RU.flip.sum()/max(1,RU.matched_marginal.sum()):.1%} "
          f"of marginal-matched), D->M flips {int(RU.flip_back.sum())}.")

    print("\n" + "#" * 108)
    print("# C.  RULE 8 CAPITAL ARM.  Chosen on 2009-2016 ONLY; 2017-2026 read ONCE.")
    print("#     Chooser: shallowest IS MaxDD among books inside 2*SE of the IS Sharpe leader.")
    print("#" * 108)
    print(R8.drop(columns=["pick_tuple"]).to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\n--- comparands on the SAME OOS window, 10 bps ---")
    for n, P in panels.items():
        bo = at_cost(P["books"][LIVE], 10, slice(OOS_START, None))
        so = P["spy"].loc[OOS_START:].values
        print(f"{n:6s} live RULES v2 OOS {cagr(bo):7.2%} / {sharpe(bo):6.4f} / {maxdd(bo):7.2%}"
              f"   SPY OOS {cagr(so):7.2%} / {sharpe(so):6.4f} / {maxdd(so):7.2%}")

    print("\n" + "#" * 108)
    print("# D.  BOTH KEEP PATHS for every ruler pick, EVERY cost rung, FULL sample.")
    print("#" * 108)
    rows = []
    for _, r in R8.iterrows():
        P = panels[r["panel"]]
        for c in COSTS:
            rr = at_cost(P["books"][r["pick_tuple"]], c)
            a, b, m = keep_paths(rr, at_cost(P["books"][LIVE], c), P["spy"].values)
            rows.append(dict(panel=r["panel"], L=r["L"], ruler=r["ruler"], pick=r["pick"],
                             cost=c, **m, KEEP_4a=a, KEEP_4b=b))
    K = pd.DataFrame(rows)
    print(K.drop_duplicates(subset=["panel", "ruler", "pick", "cost"]).to_string(
        index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"\n4a passes {int(K.KEEP_4a.sum())} of {len(K)};  4b passes {int(K.KEEP_4b.sum())} of {len(K)}")

    print("\n" + "#" * 108)
    print("# E.  OOS-ONLY KEEP paths for the two rulers' picks (rule-8 window, every cost rung).")
    print("#" * 108)
    rows = []
    for _, r in R8.iterrows():
        P = panels[r["panel"]]
        for c in COSTS:
            rr = at_cost(P["books"][r["pick_tuple"]], c, slice(OOS_START, None))
            a, b, m = keep_paths(rr, at_cost(P["books"][LIVE], c, slice(OOS_START, None)),
                                 P["spy"].loc[OOS_START:].values)
            rows.append(dict(panel=r["panel"], L=r["L"], ruler=r["ruler"], pick=r["pick"],
                             cost=c, **m, KEEP_4a_oos=a, KEEP_4b_oos=b))
    E = pd.DataFrame(rows)
    print(E.drop_duplicates(subset=["panel", "ruler", "pick", "cost"]).to_string(
        index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"\nOOS 4a passes {int(E.KEEP_4a_oos.sum())} of {len(E)};  "
          f"OOS 4b passes {int(E.KEEP_4b_oos.sum())} of {len(E)}")

    print("\n" + "#" * 108)
    print("# F.  DOES THE RULER CHANGE THE PICK?  (the only thing that reaches capital)")
    print("#" * 108)
    for (p, L), g in R8.groupby(["panel", "L"]):
        gi = g.set_index("ruler")
        same = gi.loc["marginal", "pick"] == gi.loc["paired", "pick"]
        print(f"  {p:6s} L={L:4d}  marginal: n={gi.loc['marginal','n_matched']:2d} pick "
              f"{gi.loc['marginal','pick']} OOS {gi.loc['marginal','oos_Sharpe']:.4f}   |   "
              f"paired: n={gi.loc['paired','n_matched']:2d} pick {gi.loc['paired','pick']} "
              f"OOS {gi.loc['paired','oos_Sharpe']:.4f}   -> "
              f"{'SAME PICK' if same else 'PICK MOVES'}")
    ncell = R8.groupby(['panel', 'L']).ngroups
    same = sum(1 for _, g in R8.groupby(["panel", "L"]) if g["pick"].nunique() == 1)
    print(f"\nPICK IDENTICAL under both rulers at {same} of {ncell} (panel, L) cells; "
          f"the ruler moves the pick at {ncell - same}.")

    out = ROOT / "research" / "backtests" / f"{SLUG}.contrasts.csv"
    RU.to_csv(out, index=False)
    R8.drop(columns=["pick_tuple"]).to_csv(str(out).replace(".contrasts", ".rule8"), index=False)
    K.to_csv(str(out).replace(".contrasts", ".keep_full"), index=False)
    E.to_csv(str(out).replace(".contrasts", ".keep_oos"), index=False)
    print(f"\nwrote {out.name} ({len(RU)} rows), .rule8.csv, .keep_full.csv, .keep_oos.csv")


if __name__ == "__main__":
    a = sys.argv[1] if len(sys.argv) > 1 else "REPORT"
    if a == "REPORT":
        report()
    elif a == "ALL":
        for n in PANELS:
            build(n)
        report()
    else:
        build(a)
