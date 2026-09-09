#!/usr/bin/env python3
"""Idea 482 — restate every published 4a count against the LIVE book (RULES v2).

PROTOCOL 4a is "Sharpe > current live rules in BOTH halves AND MaxDD no worse than the
live rules".  Every 4a count committed before 2026-09-06 was scored against RULES v1.
On 2026-09-06 the live book became RULES v2, which is a much stronger comparand.  Idea
252 showed one corpus (300 CAND books on B136) collapse 178/300 -> 3/300 under the swap.
This script does the same restatement over the WHOLE committed record.

Two tuned parameters, as the queue allows: baseline version in {v1, v2} and panel in
{u56, broad136, small439}.  Every grid point is reported.

Method
  A. Recompute the RULES v1 and RULES v2 baselines on each panel, at 10 and 25 bps,
     weekly, next-day execution, under baseline.compare()'s exact convention
     (start = px.index[260]; halves at len(r)//2), plus SPY, plus an OOS (2017-) leg.
  B. Harvest every committed research/backtests/*.csv[.gz] carrying H1, H2, MaxDD and a
     published 4a column, map its panel label, and re-score 4a against v1 and against v2.
     The v1 re-score is the REPRODUCTION CONTROL: if it does not reproduce the published
     column, that file's restatement is not trusted and is reported separately.
  C. Rule 8 (walk-forward).  The restatement is a SELECTOR: "pass 4a against the live
     book" is a filter over each committed menu.  On every menu that publishes an IS
     column and OOS columns, pick the best-IS_Sharpe arm inside the 4a-v1 survivors, the
     4a-v2 survivors, and the whole menu, and report OOS CAGR/Sharpe/MaxDD of each
     against the v2 baseline OOS and SPY OOS.  Choice on the first half only; evaluated
     on the untouched second half.
  D. Both KEEP paths evaluated for anything the census promotes.

SURVIVORSHIP: broad136 and small439 are current-constituent screens (PROTOCOL 9,
data/SMALL_PANEL_README.md); small439 = the 483-name sub-$2B panel with the 44 tickers
whose max_1d_move >= 1.0 dropped.  Absolute levels are optimistic; the v1-vs-v2 margin is
a same-names same-days difference and is much less exposed.

Deterministic, offline, no network.  Run: python research/backtests/2026-09-09_restate-*.py
"""
import sys, os, glob, gzip, json, math, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights          # noqa
from engine import backtest, metrics                                            # noqa

STEM = Path(__file__).with_suffix("")
OUT = lambda ext: Path(str(STEM) + ext)
COSTS = (10, 25)
OOS_START = "2017-01-01"                                                        # PROTOCOL 8


# ------------------------------------------------------------------ A. baselines
def panels():
    u56 = load_universe()
    b136 = load_universe(broad=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    drop = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"].astype(str))       # protocol-mandated
    s = load_universe(small=True)
    s439 = s.drop(columns=[c for c in s.columns if c in drop])
    return {"u56": u56, "broad136": b136, "small439": s439}


def legs(r, spy):
    """compare()'s convention: full, halves at len//2, plus the rule-8 OOS leg."""
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    o = metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"],
                H2=m2["Sharpe"], OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"])


def build_baselines(P):
    rows = []
    for pname, px in P.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        rows.append(dict(panel=pname, book="SPY", cost=np.nan, **legs(spy, spy)))
        for cost in COSTS:
            for bname, fn in (("v1", rules_v1_weights), ("v2", rules_v2_weights)):
                r = backtest(px, fn(px), cost_bps=cost, freq="W")["returns"].loc[start:]
                rows.append(dict(panel=pname, book=bname, cost=cost, **legs(r, spy)))
                print(f"  baseline {pname:9s} {bname} {cost}bps  "
                      f"CAGR {rows[-1]['CAGR']:7.2%} Sh {rows[-1]['Sharpe']:.3f} "
                      f"DD {rows[-1]['MaxDD']:7.2%} H1/H2 {rows[-1]['H1']:.3f}/{rows[-1]['H2']:.3f} "
                      f"OOS Sh {rows[-1]['OOS_Sharpe']:.3f}")
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ B. census
PANEL_MAP = {                                                                   # committed labels -> panel
    "u56": "u56", "U56": "u56", "universe.json": "u56", "universe.json(56)": "u56",
    "universe.json (56)": "u56", "universe.json (56, control)": "u56", "56": "u56",
    "broad": "broad136", "B136": "broad136", "BROAD136": "broad136", "broad136": "broad136",
    "universe_broad.json": "broad136", "universe_broad(136)": "broad136",
    "universe_broad.json (136, PRIMARY)": "broad136",
    "universe_broad.json (136, the H2-bound cell)": "broad136", "136": "broad136",
    "small": "small439", "SMALL": "small439", "SMALL439": "small439", "small439": "small439",
    "SMALL484": "small439", "small484": "small439", "SMALL439+SPY": "small439",
}
PANEL_COLS = ("panel", "universe", "uni")
FOURA_COLS = ("p4a", "pass4a", "4a", "f4a")
IS_COLS = ("IS_Sharpe", "IS_Sh", "IS_sharpe", "is_sharpe")
COST_COLS = ("cost", "bps", "cost_bps", "cost_rung")


def header(f):
    op = gzip.open if f.endswith(".gz") else open
    with op(f, "rt", errors="replace") as fh:
        return [c.strip().strip('"') for c in fh.readline().strip().split(",")]


def pick(cols, names):
    low = {c.lower(): c for c in cols}
    for n in names:
        if n.lower() in low:
            return low[n.lower()]
    return None


def as_bool(s):
    """Published 4a columns are True/False, 1/0, 'PASS'/'FAIL', or a fail-string ('' = pass)."""
    if s.dtype == bool:
        return s
    if pd.api.types.is_bool_dtype(s):
        return s.astype(bool)
    if pd.api.types.is_numeric_dtype(s):
        return s.astype(float) > 0.5
    t = s.astype(str).str.strip().str.lower()
    yes = t.isin(["true", "1", "1.0", "yes", "y", "pass", "keep", "ok"])
    no = t.isin(["false", "0", "0.0", "no", "n", "fail", "kill", "nan", ""])
    if (yes | no).mean() > 0.95:
        return yes
    return pd.Series(np.nan, index=s.index)                                     # not a boolean verdict


def to_frac(x):
    """MaxDD is committed as a fraction (-0.12) in some files and as pct (-12.05) in others."""
    v = pd.to_numeric(x, errors="coerce")
    med = v.abs().median()
    return v / 100.0 if (pd.notna(med) and med > 1.5) else v


def census(B):
    files = sorted(glob.glob(str(ROOT / "research/backtests/*.csv"))) + \
            sorted(glob.glob(str(ROOT / "research/backtests/*.csv.gz")))
    me = os.path.basename(str(STEM))
    bidx = {(r.panel, r.book, r.cost): r for r in B.itertuples()}
    rows, menus = [], []
    for f in files:
        base = os.path.basename(f)
        if base.startswith(me):
            continue
        try:
            cols = header(f)
        except Exception:
            continue
        c4a = pick(cols, FOURA_COLS); cp = pick(cols, PANEL_COLS)
        ch1, ch2, cdd = pick(cols, ("H1",)), pick(cols, ("H2",)), pick(cols, ("MaxDD", "DD"))
        if not (c4a and cp and ch1 and ch2 and cdd):
            continue
        try:
            df = pd.read_csv(f)
        except Exception:
            continue
        if len(df) == 0:
            continue
        pan = df[cp].astype(str).str.strip().map(PANEL_MAP)
        pub = as_bool(df[c4a])
        if pub.isna().all():
            continue
        h1 = pd.to_numeric(df[ch1], errors="coerce")
        h2 = pd.to_numeric(df[ch2], errors="coerce")
        dd = to_frac(df[cdd])
        cc = pick(cols, COST_COLS)
        # cost rung: a candidate priced at 5/50 bps cannot be judged against a 10 bps baseline,
        # so those rows are dropped rather than silently mis-matched.
        cost = pd.to_numeric(df[cc], errors="coerce").fillna(10.0) if cc else pd.Series(10.0, index=df.index)
        cost = cost.where(cost.isin(COSTS))
        cis = pick(cols, IS_COLS)
        isv = pd.to_numeric(df[cis], errors="coerce") if cis else pd.Series(np.nan, index=df.index)
        oc = {k: pick(cols, (k,)) for k in ("OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "OOS_Sh", "OOS_DD")}
        o_cagr = pd.to_numeric(df[oc["OOS_CAGR"]], errors="coerce") if oc["OOS_CAGR"] else pd.Series(np.nan, index=df.index)
        o_sh = pd.to_numeric(df[oc["OOS_Sharpe"] or oc["OOS_Sh"]], errors="coerce") if (oc["OOS_Sharpe"] or oc["OOS_Sh"]) else pd.Series(np.nan, index=df.index)
        o_dd = to_frac(df[oc["OOS_MaxDD"] or oc["OOS_DD"]]) if (oc["OOS_MaxDD"] or oc["OOS_DD"]) else pd.Series(np.nan, index=df.index)

        sub = pd.DataFrame(dict(file=base, panel=pan, pub=pub, H1=h1, H2=h2, MaxDD=dd,
                                cost=cost, IS=isv, OOS_CAGR=o_cagr, OOS_Sharpe=o_sh, OOS_MaxDD=o_dd))
        sub = sub.dropna(subset=["panel", "pub", "H1", "H2", "MaxDD", "cost"])
        sub["pub"] = sub["pub"].astype(bool)
        if len(sub) == 0:
            continue
        key = list(zip(sub.panel, sub.cost))
        for v in ("v1", "v2"):
            bh1 = np.array([bidx[(p, v, c)].H1 for p, c in key])
            bh2 = np.array([bidx[(p, v, c)].H2 for p, c in key])
            bdd = np.array([bidx[(p, v, c)].MaxDD for p, c in key])
            sub[f"{v}_H1"] = sub.H1.values > bh1
            sub[f"{v}_H2"] = sub.H2.values > bh2
            sub[f"{v}_DD"] = sub.MaxDD.values >= bdd
            sub[f"pass_{v}"] = sub[f"{v}_H1"] & sub[f"{v}_H2"] & sub[f"{v}_DD"]
        rows.append(sub)
        menus.append(base)
    C = pd.concat(rows, ignore_index=True)
    return C


# ------------------------------------------------------------------ C. rule 8
def walkforward(C, B):
    """Selector test: choose on IS (first half), evaluate on the untouched OOS leg."""
    out = []
    ok = C.dropna(subset=["IS", "OOS_Sharpe"])
    for (f, p), g in ok.groupby(["file", "panel"]):
        if len(g) < 3:
            continue
        def pick_best(gg):
            if len(gg) == 0:
                return None
            return gg.loc[gg.IS.idxmax()]
        rec = dict(file=f, panel=p, n=len(g))
        for arm, gg in (("all", g), ("4a_v1", g[g.pass_v1]), ("4a_v2", g[g.pass_v2])):
            b = pick_best(gg)
            rec[f"{arm}_n"] = len(gg)
            rec[f"{arm}_OOS_Sharpe"] = np.nan if b is None else b.OOS_Sharpe
            rec[f"{arm}_OOS_CAGR"] = np.nan if b is None else b.OOS_CAGR
            rec[f"{arm}_OOS_MaxDD"] = np.nan if b is None else b.OOS_MaxDD
        out.append(rec)
    return pd.DataFrame(out)


# ------------------------------------------------------------------ main
def main():
    print("=" * 100)
    print("IDEA 482 — restate every published 4a count against the LIVE book (RULES v2)")
    print("=" * 100)
    print("\n[A] Panel baselines (weekly, next-day execution, compare() convention)\n")
    if OUT(".baselines.csv").exists():
        B = pd.read_csv(OUT(".baselines.csv"))
        print("  (re-using committed .baselines.csv; delete it to recompute)")
        print(B.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    else:
        P = panels()
        for k, v in P.items():
            print(f"  panel {k:9s} {v.shape[1]:4d} cols  {v.index[0].date()} .. {v.index[-1].date()}")
        B = build_baselines(P)
        B.to_csv(OUT(".baselines.csv"), index=False)

    print("\n[B] Census of committed grid CSVs\n")
    C = census(B)
    # commit the verdict columns only; the float legs are re-derivable from the parent CSVs
    C[["file", "panel", "cost", "pub", "pass_v1", "pass_v2", "v2_H1", "v2_H2", "v2_DD"]] \
        .to_csv(OUT(".census.csv.gz"), index=False, compression="gzip")
    nf = C.file.nunique()
    print(f"  files harvested: {nf}   rows: {len(C):,}   panels: {sorted(C.panel.unique())}")

    # reproduction control: does the recomputed 4a-vs-v1 reproduce the published column?
    rep = C.groupby("file").apply(lambda g: (g.pub == g.pass_v1).mean(), include_groups=False)
    good = set(rep[rep >= 0.95].index)
    print(f"  files whose published 4a column is reproduced by 4a-vs-v1 at >=95%: "
          f"{len(good)}/{nf}  (median agreement {rep.median():.3f})")
    rep.sort_values().to_frame("agree_v1").to_csv(OUT(".reproduction.csv"))
    bins = [(0.999, 1.01, "exact"), (0.95, 0.999, "[0.95,1)"), (0.8, 0.95, "[0.80,0.95)"),
            (0.5, 0.8, "[0.50,0.80)"), (-1, 0.5, "<0.50")]
    print("  reproduction distribution: " + "  ".join(
        f"{lbl} {int(((rep >= lo) & (rep < hi)).sum())}" for lo, hi, lbl in bins))
    print("  (files below 0.95 used a different window, cost rung or half-split than compare();")
    print("   they are EXCLUDED from every count below rather than restated on a mismatched bar.)")

    G = C[C.file.isin(good)]
    print(f"  trusted subset: {len(G):,} rows in {G.file.nunique()} files")

    print("\n[B1] Published 4a passes, restated — ALL grid points, by panel x baseline version\n")
    tbl = []
    for pan, g in G.groupby("panel"):
        tbl.append(dict(panel=pan, rows=len(g), published_pass=int(g.pub.sum()),
                        pass_v1=int(g.pass_v1.sum()), pass_v2=int(g.pass_v2.sum()),
                        survive=int((g.pub & g.pass_v2).sum()),
                        survive_rate=(g.pub & g.pass_v2).sum() / max(g.pub.sum(), 1)))
    T = pd.DataFrame(tbl)
    tot = dict(panel="ALL", rows=len(G), published_pass=int(G.pub.sum()),
               pass_v1=int(G.pass_v1.sum()), pass_v2=int(G.pass_v2.sum()),
               survive=int((G.pub & G.pass_v2).sum()),
               survive_rate=(G.pub & G.pass_v2).sum() / max(G.pub.sum(), 1))
    T = pd.concat([T, pd.DataFrame([tot])], ignore_index=True)
    print(T.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    T.to_csv(OUT(".restated.csv"), index=False)

    print("\n[B2] Which bar kills the published passes (census over pub & ~pass_v2)\n")
    lost = G[G.pub & ~G.pass_v2]
    bars = pd.DataFrame([dict(panel=pan, lost=len(g), fail_H1=int((~g.v2_H1).sum()),
                              fail_H2=int((~g.v2_H2).sum()), fail_DD=int((~g.v2_DD).sum()))
                         for pan, g in lost.groupby("panel")] +
                        [dict(panel="ALL", lost=len(lost), fail_H1=int((~lost.v2_H1).sum()),
                              fail_H2=int((~lost.v2_H2).sum()), fail_DD=int((~lost.v2_DD).sum()))])
    print(bars.to_string(index=False))
    bars.to_csv(OUT(".failbars.csv"), index=False)

    print("\n[B2b] Cost rung: why the old bar was so easy to clear\n")
    ct = G.groupby("cost").agg(rows=("pub", "size"), published_pass=("pub", "sum"),
                               pass_v1=("pass_v1", "sum"), pass_v2=("pass_v2", "sum")).reset_index()
    ct["pub_rate"] = ct.published_pass / ct.rows
    ct["v2_rate"] = ct.pass_v2 / ct.rows
    print(ct.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    dec = B[B.book.isin(["v1", "v2"])].pivot_table(index=["panel", "book"], columns="cost", values="Sharpe")
    dec["decay_10_to_25"] = dec[25.0] - dec[10.0]
    print("\n  Baseline Sharpe by cost rung (the reason):")
    print(dec.to_string(float_format=lambda x: f"{x:+.4f}"))

    print("\n[B3] Verdict flips: files whose 4a support vanishes entirely under the live book\n")
    per = G.groupby("file").agg(rows=("pub", "size"), pub=("pub", "sum"),
                                v1=("pass_v1", "sum"), v2=("pass_v2", "sum")).reset_index()
    per["flip"] = (per.pub > 0) & (per.v2 == 0)
    per = per.sort_values(["flip", "pub"], ascending=[False, False])
    per.to_csv(OUT(".perfile.csv"), index=False)
    fl = per[per.flip]
    print(f"  files with >=1 published 4a pass: {(per.pub > 0).sum()}")
    print(f"  files where ALL published 4a passes die against RULES v2: {len(fl)}")
    print(f"  files retaining >=1 4a pass against RULES v2: {(per.v2 > 0).sum()}")
    print("\n  Largest 4a counts that go to zero:")
    print(fl.head(15).to_string(index=False))
    print("\n  Files that KEEP 4a support under the live book:")
    print(per[per.v2 > 0].head(15).to_string(index=False))

    print("\n[C] Rule 8 walk-forward — is 'passes 4a vs the live book' a better SELECTOR?\n")
    W = walkforward(G, B)
    W.to_csv(OUT(".walkforward.csv"), index=False)
    if len(W):
        print(f"  menus with an IS column and OOS columns: {len(W)} (over {W.file.nunique()} files)")
        for pan, g in list(W.groupby("panel")) + [("ALL", W)]:
            r = dict(panel=pan, menus=len(g))
            for arm in ("all", "4a_v1", "4a_v2"):
                s = g[f"{arm}_OOS_Sharpe"].dropna()
                r[f"{arm}_n"] = len(s)
                r[f"{arm}_Sh"] = s.mean() if len(s) else np.nan
                r[f"{arm}_CAGR"] = g[f"{arm}_OOS_CAGR"].dropna().mean()
                r[f"{arm}_DD"] = g[f"{arm}_OOS_MaxDD"].dropna().mean()
            print("  " + " ".join(f"{k}={v:.4f}" if isinstance(v, float) else f"{k}={v}"
                                  for k, v in r.items()))
        # paired: only menus where both arms produce a pick
        both = W.dropna(subset=["4a_v1_OOS_Sharpe", "4a_v2_OOS_Sharpe"])
        if len(both):
            d = both["4a_v2_OOS_Sharpe"] - both["4a_v1_OOS_Sharpe"]
            t = d.mean() / (d.std(ddof=1) / math.sqrt(len(d))) if d.std(ddof=1) > 0 else np.nan
            print(f"\n  paired menus (both arms pick): {len(d)}  mean OOS Sharpe delta v2-v1 "
                  f"{d.mean():+.4f}  t {t:+.2f}  wins {int((d > 0).sum())}/{len(d)}")
        bothall = W.dropna(subset=["all_OOS_Sharpe", "4a_v2_OOS_Sharpe"])
        if len(bothall):
            d2 = bothall["4a_v2_OOS_Sharpe"] - bothall["all_OOS_Sharpe"]
            t2 = d2.mean() / (d2.std(ddof=1) / math.sqrt(len(d2))) if d2.std(ddof=1) > 0 else np.nan
            print(f"  paired vs unfiltered menu: {len(d2)}  mean OOS Sharpe delta 4a_v2-all "
                  f"{d2.mean():+.4f}  t {t2:+.2f}  wins {int((d2 > 0).sum())}/{len(d2)}")

    print("\n[D] Reference legs the OOS numbers above are judged against (10 bps)\n")
    ref = B[(B.cost == 10) | (B.book == "SPY")][
        ["panel", "book", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]]
    print(ref.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n[E] Both KEEP paths\n")
    print("  No new book is introduced: idea 482 is a restatement of the committed record, so")
    print("  there is nothing to promote.  4a and 4b are reported as COUNTS over the record.")
    n4a_v2 = int(G.pass_v2.sum())
    print(f"  4a (vs the live RULES v2): {n4a_v2}/{len(G)} committed grid points")
    print(f"  4a (vs the superseded v1): {int(G.pass_v1.sum())}/{len(G)}")
    print("  4b is not restated here: 4b is judged against SPY, which did not change on")
    print("  2026-09-06, so no published 4b count moves.  (Ideas 481/253 own the 4b re-scoring.)")
    print("\nDone.  Artefacts: " + ", ".join(os.path.basename(str(OUT(e))) for e in
          (".baselines.csv", ".census.csv.gz", ".reproduction.csv", ".restated.csv",
           ".failbars.csv", ".perfile.csv", ".walkforward.csv")))


if __name__ == "__main__":
    main()
