#!/usr/bin/env python3
"""Idea 354 (cloud, 2026-09-07): does-the-ceiling-invert-BECAUSE-of-de-grossing.

QUEUE TEXT: "idea 352 found a turnover ceiling has lift 3.64 within one construction family
and lift <1 pooled over 61,200 committed record rows, with the 10-bps median turnover HIGHER
for 4b passes (9.11x) than fails (4.95x).  Split the census by whether the row's book is
de-grossed/gated (realised gross < 0.9) and test whether the inversion is entirely the
low-gross stratum, i.e. Simpson's paradox with gross as the confounder.  Max 2 params
(gross split point, cost rung)."

TUNED PARAMETERS: exactly 2 -- the gross split point G* and the cost rung c.  Both are swept
and every grid point is reported.  Everything else (panels, books, n, cadence, gate) is the
POPULATION being stratified, not a tuned dial.

THE CLAIM UNDER TEST
--------------------
Idea 352's headline anomaly is an INVERSION: pooled over the record, 4b passes have HIGHER
turnover (9.11x/yr) than 4b failures (4.95x/yr), so a turnover CEILING has lift < 1 -- it
screens out the passes.  Simpson's paradox with gross as the confounder predicts three
things simultaneously, and all three must hold or the explanation fails:

  S1  gross is associated with 4b passing      (low-gross books pass more often), AND
  S2  gross is associated with turnover        (low-gross books trade less), AND
  S3  the inversion is WEAKER OR ABSENT inside each gross stratum than pooled.

S1 and S2 together are what makes gross a confounder; S3 is the paradox itself.  A test that
only looks at S3 cannot distinguish "gross explains it" from "turnover carries no signal at
all anywhere".  So a fourth reading is reported:

  S4  after stratifying, does a turnover ceiling become USEFUL (lift > 1) in either stratum?

PART A  THE RECORD (retrospective, observational).  Re-run idea 352's census, but carry a
        gross column where the committed CSV states one.  Realised-gross columns are
        preferred over nominal ones and the two are reported separately, because a nominal
        `gross=0.75` dial and a gate that de-grosses to 0.75 are different objects.

PART B  THE LIVE GRID (constructive, causal).  180 books = 3 panels x 5 book shapes
        (TOP5/10/20/40 + EWALL) x 3 nominal gross levels x {gated, ungated} x {W, M}.  Here realised gross is MEASURED
        (mean of the held weight row-sums) rather than parsed, and gross is dialled by
        construction, so the stratified comparison is a controlled one instead of an
        observational one.  Every point reported, both KEEP paths.

RULE 8 (walk-forward, required): G* and the turnover ceiling T* are chosen on the IS window
        (<= 2016-12-31) ONLY; the menu each screen admits is then read ONCE on the untouched
        OOS window (2017-01-01 ->).  Reported per panel x rung: the OOS CAGR / Sharpe / MaxDD
        of the book that the unscreened, ceiling-screened and gross-stratified-screened
        menus each pick, against RULES v2 (the live baseline) and SPY.

BOTH KEEP PATHS reported for every live point: 4a vs RULES v2 (Sharpe both halves + MaxDD no
worse), 4b vs that panel's own SPY (halves + OOS Sharpe, DD <= 60% SPY, CAGR >= 70% SPY).

SURVIVORSHIP: the SMALL panel is current constituents of a sub-$2B screen only
(data/SMALL_PANEL_README.md); tickers with max_1d_move >= 1.0 in data/small_meta.csv are
dropped first (44 of 483).  Every small-panel number below is an UPPER BOUND on what was
actually tradeable; the panel cannot support a KEEP on its own.

Deterministic, standalone, offline:
    python3 research/backtests/2026-09-07_does-the-ceiling-invert-BECAUSE-of-de-grossing_cloud.py
"""
import csv
import glob
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, score, rules_v2_weights, band_state  # noqa
from engine import backtest, metrics  # noqa

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 500)

OUT = ROOT / "research" / "backtests" / "2026-09-07_does-the-ceiling-invert-BECAUSE-of-de-grossing_cloud"
IS_END, OOS_START = "2016-12-31", "2017-01-01"

# ---- the two tuned parameters, both swept, every point reported -------------
GSTARS = [0.50, 0.60, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00]   # gross split point
RUNGS = [0, 5, 10, 25]                                            # cost rung
GSTAR_PRE = 0.90                                                  # the queue's pre-registered split
CEILINGS = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0, 12.0, 20.0]

# ---- the population (NOT tuned) --------------------------------------------
NS = [5, 10, 20, 40]
CADENCES = ["W", "M"]
GROSSES = [0.50, 0.75, 1.00]
GATES = [False, True]


# ===================================================================== helpers
def stats(r):
    """CAGR / Sharpe / MaxDD / halves / OOS on one full-sample return series."""
    m = metrics(r)
    h = len(r) // 2
    m1, m2 = metrics(r.iloc[:h]), metrics(r.iloc[h:])
    o = metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=m1["Sharpe"], H2=m2["Sharpe"],
                OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"])


def win_stats(r):
    """CAGR / Sharpe / MaxDD / halves computed WITHIN whatever window r already is."""
    m = metrics(r)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def bars_for(spy):
    """PROTOCOL 4b bars from this panel's own SPY sample."""
    s = stats(spy)
    return dict(H1=s["H1"], H2=s["H2"], OOS=s["OOS_Sharpe"],
                DD=0.60 * abs(s["MaxDD"]), CAGR=0.70 * s["CAGR"], spy=s)


def win_bars(spy_win):
    s = win_stats(spy_win)
    return dict(H1=s["H1"], H2=s["H2"], DD=0.60 * abs(s["MaxDD"]), CAGR=0.70 * s["CAGR"], spy=s)


def pass4b(st, B):
    tests = [("H1", st["H1"] - B["H1"]), ("H2", st["H2"] - B["H2"]), ("OOS", st["OOS_Sharpe"] - B["OOS"]),
             ("DD", B["DD"] - abs(st["MaxDD"])), ("CAGR", st["CAGR"] - B["CAGR"])]
    fails = [k for k, m in tests if m <= 0]
    return (len(fails) == 0), (fails[0] if fails else ""), {k: m for k, m in tests}


def pass4b_win(st, B):
    """4b judged inside one window (no separate OOS leg -- the window IS the test)."""
    tests = [("H1", st["H1"] - B["H1"]), ("H2", st["H2"] - B["H2"]),
             ("DD", B["DD"] - abs(st["MaxDD"])), ("CAGR", st["CAGR"] - B["CAGR"])]
    fails = [k for k, m in tests if m <= 0]
    return (len(fails) == 0), (fails[0] if fails else "")


def pass4a(st, base):
    return st["H1"] > base["H1"] and st["H2"] > base["H2"] and st["MaxDD"] >= base["MaxDD"]


def net(r0, tau, c):
    return r0 - tau * c / 1e4


def spearman(a, b):
    a, b = pd.Series(a).astype(float), pd.Series(b).astype(float)
    ok = a.notna() & b.notna()
    if ok.sum() < 8 or a[ok].nunique() < 2 or b[ok].nunique() < 2:
        return np.nan
    return float(a[ok].rank().corr(b[ok].rank()))


# ============================================================ PART A: the record
TRUEY = {"true", "1", "yes", "y", "pass", "t"}
FALSEY = {"false", "0", "no", "n", "fail", "f", ""}
# realised-gross column names take priority over nominal-dial ones
G_REAL = ["realised_gross", "gross_real", "gross_mean", "mean_gross", "gross_realised",
          "gross_mean_is", "ov_gross", "gross_conv", "gross_min"]
G_NOM = ["gross", "g", "nominal_gross", "ctl_gross"]


def _flag(v):
    s = str(v).strip().lower()
    if s in TRUEY:
        return True
    if s in FALSEY:
        return False
    return None


def _num(v):
    try:
        s = str(v).strip().replace("%", "").replace("x", "")
        if s in ("", "nan", "none", "n/a"):
            return None
        return float(s)
    except Exception:
        return None


def census():
    """Idea 352's census, plus a gross column wherever the committed CSV states one."""
    rows, files, files_g, skipped = [], 0, 0, []
    for f in sorted(glob.glob(str(ROOT / "research" / "backtests" / "*.csv"))):
        # A prior census DUMP is not a record row -- it is a copy of rows already pooled.
        # Idea 352 committed one (183,828 rows) whose header parses as (turnover, 4b), so a
        # naive re-glob double-counts its entire population and lets one script outvote the
        # record.  Exclude every census dump, this script's own outputs included.
        if Path(f).name.endswith(".census.csv") or Path(f).name.startswith(OUT.name):
            skipped.append(Path(f).name)
            continue
        try:
            rd = list(csv.DictReader(open(f, newline="")))
        except Exception:
            continue
        if not rd:
            continue
        hdr = {c.lower(): c for c in rd[0].keys() if c}
        to_c = next((hdr[c] for c in hdr if "turn" in c), None)
        cands = [c for c in hdr if "4b" in c and "fail" not in c and "oos" not in c and c != "is4b"]
        p4_c = hdr[cands[0]] if cands else None
        if not (to_c and p4_c):
            continue
        cost_c = next((hdr[c] for c in hdr if c in ("cost", "bps", "cost_bps", "rung", "cost_rung", "turn_bps")), None)
        sh_c = next((hdr[c] for c in hdr if c in ("sharpe", "full_sharpe", "sharpe_full")), None)
        g_c = next((hdr[c] for c in G_REAL if c in hdr), None)
        g_kind = "realised"
        if g_c is None:
            g_c = next((hdr[c] for c in G_NOM if c in hdr), None)
            g_kind = "nominal"
        used = 0
        for r in rd:
            t, p = _num(r.get(to_c)), _flag(r.get(p4_c))
            if t is None or p is None or t < 0 or t > 200:
                continue
            g = _num(r.get(g_c)) if g_c else None
            if g is not None and not (0.0 < g <= 2.0):    # a column called "gross" that is not a gross
                g = None
            c = _num(r.get(cost_c)) if cost_c else None
            rows.append(dict(file=Path(f).name, turnover=t, pass4b=p,
                             cost=(c if c is not None else np.nan),
                             sharpe=(_num(r.get(sh_c)) if sh_c else np.nan),
                             gross=(g if g is not None else np.nan),
                             gross_kind=(g_kind if g is not None else "none")))
            used += 1
        if used:
            files += 1
            if g_c:
                files_g += 1
    df = pd.DataFrame(rows)
    df["turn_x"] = np.where(df.turnover > 25, df.turnover / 100.0, df.turnover)
    print(f"\nPART A  CENSUS: {files} committed CSVs contributed {len(df)} parseable rows; "
          f"{files_g} of them also state a gross column -> {int(df.gross.notna().sum())} rows "
          f"({df.gross.notna().mean():.1%}) carry gross.")
    print(f"  excluded {len(skipped)} prior census dumps (re-pooling them double-counts): {skipped}")
    print("  gross column kind:", df.loc[df.gross.notna(), "gross_kind"].value_counts().to_dict())
    return df


def inversion(df, label):
    """The idea-352 statistic: median turnover of 4b passes MINUS that of 4b failures.
    Positive = INVERTED (passes trade more), which is what makes a ceiling useless."""
    p, q = df[df.pass4b], df[~df.pass4b]
    if len(p) < 5 or len(q) < 5:
        return dict(slice=label, n=len(df), n_pass=len(p), rate=np.nan,
                    med_pass=np.nan, med_fail=np.nan, delta=np.nan, inverted=np.nan,
                    spearman_turn_pass=np.nan)
    mp, mq = float(p.turn_x.median()), float(q.turn_x.median())
    return dict(slice=label, n=len(df), n_pass=len(p), rate=df.pass4b.mean(),
                med_pass=mp, med_fail=mq, delta=mp - mq, inverted=bool(mp > mq),
                spearman_turn_pass=spearman(df.turn_x, df.pass4b.astype(float)))


def ceiling_curve(df, tag):
    if len(df) < 50 or df.pass4b.mean() in (0.0, 1.0):
        return pd.DataFrame()
    base = df.pass4b.mean()
    out = []
    for T in CEILINGS:
        sub = df[df.turn_x <= T]
        if len(sub) == 0:
            continue
        out.append(dict(slice=tag, ceiling_x_yr=T, admitted=len(sub), admit_share=len(sub) / len(df),
                        precision=sub.pass4b.mean(),
                        recall=sub.pass4b.sum() / max(df.pass4b.sum(), 1),
                        lift=sub.pass4b.mean() / base))
    return pd.DataFrame(out)


def part_a(rec):
    print("\n" + "=" * 100)
    print("PART A1  IS THE INVERSION CONFINED TO THE LOW-GROSS STRATUM?  (record, observational)")
    print("=" * 100)
    have = rec[rec.gross.notna()].copy()
    rows = []
    for c in RUNGS + [None]:
        sub = rec if c is None else rec[rec.cost == c]
        subg = have if c is None else have[have.cost == c]
        clab = "ALL rungs" if c is None else f"{int(c)} bps"
        rows.append({**inversion(sub, f"{clab} | ALL rows (no gross needed)"), "rung": clab, "stratum": "pooled-allrows", "gstar": np.nan})
        rows.append({**inversion(subg, f"{clab} | rows WITH gross, pooled"), "rung": clab, "stratum": "pooled", "gstar": np.nan})
        for G in GSTARS:
            rows.append({**inversion(subg[subg.gross < G], f"{clab} | gross < {G:.2f}"), "rung": clab, "stratum": "low", "gstar": G})
            rows.append({**inversion(subg[subg.gross >= G], f"{clab} | gross >= {G:.2f}"), "rung": clab, "stratum": "high", "gstar": G})
    inv = pd.DataFrame(rows)
    for c in ["ALL rungs", "0 bps", "10 bps", "25 bps"]:
        d = inv[(inv.rung == c) & (inv.gstar.isna() | (inv.gstar == GSTAR_PRE))]
        if d.n.max() > 0:
            print(f"\n--- rung {c}, pre-registered split G*={GSTAR_PRE}")
            print(d[["slice", "n", "n_pass", "rate", "med_pass", "med_fail", "delta", "inverted",
                     "spearman_turn_pass"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\n--- FULL G* SWEEP at the 10-bps rung (every grid point)")
    d = inv[(inv.rung == "10 bps") & inv.gstar.notna()]
    print(d[["gstar", "stratum", "n", "n_pass", "rate", "med_pass", "med_fail", "delta", "inverted"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n" + "=" * 100)
    print("PART A2  IS GROSS ACTUALLY A CONFOUNDER?  (S1: gross -> 4b, S2: gross -> turnover)")
    print("=" * 100)
    conf = []
    for c in RUNGS + [None]:
        sub = have if c is None else have[have.cost == c]
        if len(sub) < 50:
            continue
        clab = "ALL rungs" if c is None else f"{int(c)} bps"
        lo, hi = sub[sub.gross < GSTAR_PRE], sub[sub.gross >= GSTAR_PRE]
        conf.append(dict(rung=clab, n=len(sub),
                         n_low=len(lo), n_high=len(hi),
                         rate_low=lo.pass4b.mean() if len(lo) else np.nan,
                         rate_high=hi.pass4b.mean() if len(hi) else np.nan,
                         S1_rate_gap=(lo.pass4b.mean() - hi.pass4b.mean()) if len(lo) and len(hi) else np.nan,
                         med_turn_low=lo.turn_x.median() if len(lo) else np.nan,
                         med_turn_high=hi.turn_x.median() if len(hi) else np.nan,
                         S2_turn_gap=(lo.turn_x.median() - hi.turn_x.median()) if len(lo) and len(hi) else np.nan,
                         sp_gross_pass=spearman(sub.gross, sub.pass4b.astype(float)),
                         sp_gross_turn=spearman(sub.gross, sub.turn_x)))
    confd = pd.DataFrame(conf)
    print(confd.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n" + "=" * 100)
    print("PART A3  DOES A TURNOVER CEILING BECOME USEFUL INSIDE A STRATUM?  (S4)")
    print("=" * 100)
    cur = []
    for c in [0, 10, 25]:
        sub = have[have.cost == c]
        if len(sub) < 50:
            continue
        cur.append(ceiling_curve(sub, f"{c}bps pooled"))
        cur.append(ceiling_curve(sub[sub.gross < GSTAR_PRE], f"{c}bps gross<{GSTAR_PRE}"))
        cur.append(ceiling_curve(sub[sub.gross >= GSTAR_PRE], f"{c}bps gross>={GSTAR_PRE}"))
    cur = [x for x in cur if len(x)]
    curd = pd.concat(cur, ignore_index=True) if cur else pd.DataFrame()
    if len(curd):
        print(curd.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        best = curd.loc[curd.groupby("slice").lift.idxmax()]
        print("\n  best ceiling per slice (max lift):")
        print(best.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\n" + "=" * 100)
    print("PART A4  IF NOT GROSS, WHAT?  THE INVERSION WITH *FILE* AS THE STRATUM")
    print("=" * 100)
    print("  A committed CSV is one script's own grid: one panel family, one book family, one")
    print("  turnover scale, one 4b base rate.  Pooling them is exactly the setting a Simpson")
    print("  reversal needs.  Below: the same delta computed WITHIN each file, then averaged.")
    wf_rows = []
    for c in [0, 10, 25]:
        sub = rec[rec.cost == c]
        per = []
        for fn, d in sub.groupby("file"):
            if d.pass4b.sum() < 5 or (~d.pass4b).sum() < 5:
                continue
            i = inversion(d, fn)
            per.append(dict(rung=c, file=fn, n=i["n"], rate=i["rate"], delta=i["delta"],
                            inverted=i["inverted"]))
        pf = pd.DataFrame(per)
        pooled = inversion(sub, "pooled")
        if not len(pf):
            continue
        wf_rows.append(pf)
        print(f"\n  rung {c:2d} bps: pooled delta {pooled['delta']:+.3f} (inverted={pooled['inverted']}) "
              f"over n={pooled['n']}")
        print(f"            within-file: {int(pf.inverted.sum())}/{len(pf)} files inverted, "
              f"mean delta {pf.delta.mean():+.3f}, median {pf.delta.median():+.3f}, "
              f"n-weighted {np.average(pf.delta, weights=pf.n):+.3f}")
        print(f"            between-file spread: 4b base rate {pf.rate.min():.3f}-{pf.rate.max():.3f}, "
              f"file sizes {int(pf.n.min())}-{int(pf.n.max())}")
    perfile = pd.concat(wf_rows, ignore_index=True) if wf_rows else pd.DataFrame()
    if len(perfile):
        d10 = perfile[perfile.rung == 10].sort_values("n", ascending=False).head(15)
        print("\n  the 15 largest contributors at 10 bps (n, base rate, own delta):")
        print(d10[["file", "n", "rate", "delta", "inverted"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    return inv, confd, curd, perfile


# ============================================================ PART B: the live grid
def panels():
    u = load_universe()
    b = load_universe(broad=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    s = load_universe(small=True)
    s = s.drop(columns=[c for c in s.columns if c in bad])
    print(f"\nSMALL: dropped {len(bad)} tickers with max_1d_move >= 1.0 -> {s.shape[1]-1} names + SPY "
          f"(SURVIVORSHIP: current constituents only)")
    return {"U56": u, "B136": b, f"SMALL{s.shape[1]-1}": s}


def eligibility(px):
    s, above, vol20 = score(px)
    ok = above & (vol20 < 0.60)
    return s.where(ok), ok


def w_rank(elig, n):
    rank = elig.rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    return sel.div(sel.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def w_ewall(ok):
    sel = ok.astype(float)
    return sel.div(sel.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def part_b():
    P = panels()
    recs, gate_err = [], []
    store = {}
    for pname, px in P.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        B = bars_for(spy)
        base_r = backtest(px, rules_v2_weights(px), cost_bps=10, freq="W")["returns"].loc[start:]
        base = stats(base_r)
        print(f"\n=== {pname}  {px.index[0].date()} -> {px.index[-1].date()}  {px.shape[1]-1} names")
        print(f"    SPY   CAGR {B['spy']['CAGR']:.2%}  Sharpe {B['spy']['Sharpe']:.4f}  MaxDD {B['spy']['MaxDD']:.2%}"
              f"  halves {B['spy']['H1']:.4f}/{B['spy']['H2']:.4f}  OOS {B['spy']['OOS_Sharpe']:.4f}")
        print(f"    4b bars: H1>{B['H1']:.4f} H2>{B['H2']:.4f} OOS>{B['OOS']:.4f} |DD|<={B['DD']:.2%} CAGR>={B['CAGR']:.2%}")
        print(f"    RULES v2 @10bps: CAGR {base['CAGR']:.2%} Sharpe {base['Sharpe']:.4f} MaxDD {base['MaxDD']:.2%}"
              f"  halves {base['H1']:.4f}/{base['H2']:.4f}  OOS {base['OOS_Sharpe']:.4f}")

        elig, ok = eligibility(px)
        shapes = {f"TOP{n}": w_rank(elig, n) for n in NS}
        shapes["EWALL"] = w_ewall(ok)
        gate = band_state(px, 0.03)
        for bname, w1 in shapes.items():
            for g in GROSSES:
                for gated in GATES:
                    w = (w1 * g)
                    if gated:
                        w = w.where(gate, 0.0)          # de-gross to CASH, never re-spread
                    for freq in CADENCES:
                        res = backtest(px, w, cost_bps=0, freq=freq)
                        r0 = res["returns"].loc[start:]
                        tau = res["turnover"].loc[start:]
                        held = res["weights"].loc[start:]
                        greal = float(held.sum(axis=1).mean())      # MEASURED realised gross
                        T = float(tau.sum() / (len(r0) / 252))
                        st = {c: stats(net(r0, tau, c)) for c in RUNGS}
                        p4 = {c: pass4b(st[c], B) for c in RUNGS}
                        key = (pname, bname, g, gated, freq)
                        store[key] = (r0, tau, B, base, spy)
                        recs.append(dict(panel=pname, book=bname, gross_nom=g, gated=gated, cadence=freq,
                                         gross_real=greal, turn_x_yr=T,
                                         **{f"S{c}": st[c]["Sharpe"] for c in RUNGS},
                                         CAGR10=st[10]["CAGR"], MaxDD10=st[10]["MaxDD"],
                                         H1_10=st[10]["H1"], H2_10=st[10]["H2"],
                                         OOS_S10=st[10]["OOS_Sharpe"], OOS_CAGR10=st[10]["OOS_CAGR"],
                                         OOS_MaxDD10=st[10]["OOS_MaxDD"],
                                         **{f"p4b_{c}": p4[c][0] for c in RUNGS},
                                         **{f"fail_{c}": p4[c][1] for c in RUNGS},
                                         **{f"p4a_{c}": pass4a(st[c], base) for c in RUNGS}))
                        if bname == "TOP20" and g == 1.00 and not gated and freq == "W":
                            direct = backtest(px, w, cost_bps=10, freq=freq)["returns"].loc[start:]
                            gate_err.append((pname, float(np.abs(direct - net(r0, tau, 10.0)).max())))
    grid = pd.DataFrame(recs)
    print("\n  cost-identity gate  max|direct - r0 - tau*c/1e4| per panel:",
          {p: f"{e:.2e}" for p, e in gate_err})
    return P, grid, store


def part_b_analysis(grid):
    print("\n" + "=" * 100)
    print("PART B1  THE SAME INVERSION TEST ON A CONSTRUCTED GRID (gross MEASURED, not parsed)")
    print("=" * 100)
    rows = []
    for c in RUNGS:
        d = grid.copy()
        d["pass4b"] = d[f"p4b_{c}"]
        d["turn_x"] = d.turn_x_yr
        rows.append({**inversion(d, f"{c} bps | pooled (all {len(d)})"), "rung": c, "stratum": "pooled", "gstar": np.nan})
        for G in GSTARS:
            rows.append({**inversion(d[d.gross_real < G], f"{c} bps | gross_real < {G:.2f}"), "rung": c, "stratum": "low", "gstar": G})
            rows.append({**inversion(d[d.gross_real >= G], f"{c} bps | gross_real >= {G:.2f}"), "rung": c, "stratum": "high", "gstar": G})
    liveinv = pd.DataFrame(rows)
    print(liveinv[["rung", "stratum", "gstar", "n", "n_pass", "rate", "med_pass", "med_fail", "delta", "inverted"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n  --- the controlled version: hold NOMINAL gross fixed and re-read the sign")
    ctl = []
    for c in RUNGS:
        d = grid.copy()
        d["pass4b"] = d[f"p4b_{c}"]
        d["turn_x"] = d.turn_x_yr
        for g in GROSSES:
            for gated in GATES:
                ctl.append({**inversion(d[(d.gross_nom == g) & (d.gated == gated)],
                                        f"{c} bps | g={g:.2f} gated={gated}"), "rung": c,
                            "gross_nom": g, "gated": gated})
    ctld = pd.DataFrame(ctl)
    print(ctld[["rung", "gross_nom", "gated", "n", "n_pass", "rate", "med_pass", "med_fail", "delta", "inverted"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    return liveinv, ctld


def keep_paths(grid):
    print("\n" + "=" * 100)
    print(f"PART B2  BOTH KEEP PATHS over the {len(grid)}-book population, every rung")
    print("=" * 100)
    rows = []
    for c in RUNGS:
        for pname, d in grid.groupby("panel"):
            rows.append(dict(rung=c, panel=pname, n=len(d),
                             p4a=int(d[f"p4a_{c}"].sum()), p4b=int(d[f"p4b_{c}"].sum())))
    kp = pd.DataFrame(rows)
    print(kp.to_string(index=False))
    print("\n  4b passes at 10 bps (the PROTOCOL rung), listed in full:")
    w = grid[grid.p4b_10]
    if len(w):
        print(w[["panel", "book", "gross_nom", "gated", "cadence", "gross_real", "turn_x_yr",
                 "CAGR10", "S10", "MaxDD10", "H1_10", "H2_10", "OOS_S10"]]
              .sort_values("S10", ascending=False).to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    else:
        print("   (none)")
    print("\n  first failing 4b bar at 10 bps, by gross stratum:")
    for lab, sub in [("gross_real < 0.90", grid[grid.gross_real < 0.90]), ("gross_real >= 0.90", grid[grid.gross_real >= 0.90])]:
        print(f"   {lab:20s} n={len(sub):4d}  {sub.fail_10.value_counts().to_dict()}")
    return kp


# ============================================================ RULE 8 walk-forward
def rule8(P, grid, store):
    print("\n" + "=" * 100)
    print("RULE 8  WALK-FORWARD.  G* and T* chosen on IS (<=2016) only; menus read ONCE on OOS (2017->)")
    print("=" * 100)
    rows = []
    for pname, px in P.items():
        sub = grid[grid.panel == pname]
        for c in [10, 25]:
            # ---- IS: score every book, and choose the two screen parameters on IS ONLY
            isrows = []
            for _, k in sub.iterrows():
                r0, tau, B, base, spy = store[(k.panel, k.book, k.gross_nom, k.gated, k.cadence)]
                r = net(r0, tau, c)
                ris, roos = r.loc[:IS_END], r.loc[OOS_START:]
                tis = float(tau.loc[:IS_END].sum() / (len(ris) / 252))
                isrows.append(dict(book=k.book, gross_nom=k.gross_nom, gated=k.gated, cadence=k.cadence,
                                   gross_real=k.gross_real, turn_is=tis,
                                   IS_S=metrics(ris)["Sharpe"], **{f"OOS_{a}": v for a, v in win_stats(roos).items()},
                                   key=(k.panel, k.book, k.gross_nom, k.gated, k.cadence)))
            D = pd.DataFrame(isrows)
            spy_is = P[pname]["SPY"].pct_change().fillna(0).loc[:IS_END]
            spy_oos = P[pname]["SPY"].pct_change().fillna(0).loc[OOS_START:]
            Bis = win_bars(spy_is)
            D["IS_4b"] = [pass4b_win(win_stats(net(*store[k][:2], c).loc[:IS_END]), Bis)[0] for k in D.key]

            # screen parameters chosen on IS: the (G*, T*) pair with the best IS 4b lift
            baseR = D.IS_4b.mean()
            best = (np.nan, np.nan, -1.0, 0)
            for G in GSTARS:
                for T in CEILINGS:
                    adm = D[(D.gross_real < G) & (D.turn_is <= T)]
                    if len(adm) < 5:
                        continue
                    lift = adm.IS_4b.mean() / baseR if baseR > 0 else np.nan
                    if not np.isnan(lift) and lift > best[2]:
                        best = (G, T, lift, len(adm))
            Gs, Ts, liftIS, nadm = best

            # ---- OOS: read each menu ONCE
            def pick(menu, tag):
                if not len(menu):
                    return dict(panel=pname, rung=c, menu=tag, n_menu=0)
                w = menu.loc[menu.IS_S.idxmax()]
                return dict(panel=pname, rung=c, menu=tag, n_menu=len(menu),
                            pick=f"{w.book} g{w.gross_nom:.2f} {'gate' if w.gated else 'raw'} {w.cadence}",
                            gross_real=w.gross_real, turn_is=w.turn_is, IS_S=w.IS_S,
                            OOS_CAGR=w.OOS_CAGR, OOS_Sharpe=w.OOS_Sharpe, OOS_MaxDD=w.OOS_MaxDD,
                            menu_mean_OOS_S=menu.OOS_Sharpe.mean())

            ceil_only = D[D.turn_is <= (Ts if not np.isnan(Ts) else 1e9)]
            strat = D[(D.gross_real < (Gs if not np.isnan(Gs) else 1e9)) & (D.turn_is <= (Ts if not np.isnan(Ts) else 1e9))]
            rows.append({**pick(D, f"unscreened (all {len(D)})"), "Gstar": np.nan, "Tstar": np.nan, "IS_lift": np.nan})
            rows.append({**pick(ceil_only, "turnover ceiling only"), "Gstar": np.nan, "Tstar": Ts, "IS_lift": np.nan})
            rows.append({**pick(strat, "gross-stratified + ceiling"), "Gstar": Gs, "Tstar": Ts, "IS_lift": liftIS})

            bl = backtest(px, rules_v2_weights(px), cost_bps=c, freq="W")["returns"].loc[px.index[260]:]
            rows.append(dict(panel=pname, rung=c, menu="RULES v2 (live baseline)", n_menu=np.nan,
                             pick="rules_v2", **{f"OOS_{a}": v for a, v in
                                                 {k2: v2 for k2, v2 in win_stats(bl.loc[OOS_START:]).items()
                                                  if k2 in ("CAGR", "Sharpe", "MaxDD")}.items()}))
            rows.append(dict(panel=pname, rung=c, menu="SPY buy-and-hold", n_menu=np.nan, pick="SPY",
                             **{f"OOS_{a}": v for a, v in
                                {k2: v2 for k2, v2 in win_stats(spy_oos).items()
                                 if k2 in ("CAGR", "Sharpe", "MaxDD")}.items()}))
    wf = pd.DataFrame(rows)
    cols = ["panel", "rung", "menu", "n_menu", "Gstar", "Tstar", "IS_lift", "pick",
            "gross_real", "turn_is", "IS_S", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "menu_mean_OOS_S"]
    print(wf.reindex(columns=cols).to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    return wf


# ===================================================================== main
def main():
    rec = census()
    inv, confd, curd, perfile = part_a(rec)
    rec.to_csv(f"{OUT}.census.csv", index=False)
    inv.to_csv(f"{OUT}.inversion.csv", index=False)
    confd.to_csv(f"{OUT}.confounder.csv", index=False)
    curd.to_csv(f"{OUT}.ceiling.csv", index=False)
    perfile.to_csv(f"{OUT}.perfile.csv", index=False)

    P, grid, store = part_b()
    liveinv, ctld = part_b_analysis(grid)
    kp = keep_paths(grid)
    grid.to_csv(f"{OUT}.grid.csv", index=False)
    liveinv.to_csv(f"{OUT}.live_inversion.csv", index=False)
    ctld.to_csv(f"{OUT}.controlled.csv", index=False)
    kp.to_csv(f"{OUT}.keeppaths.csv", index=False)

    wf = rule8(P, grid, store)
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)

    # ------------------------------------------------------------- verdict
    print("\n" + "=" * 100)
    print("VERDICT INPUTS")
    print("=" * 100)
    have = rec[rec.gross.notna()]
    r10 = have[have.cost == 10]
    p_all = inversion(rec[rec.cost == 10], "record 10bps all rows")
    p_g = inversion(r10, "record 10bps rows-with-gross")
    p_lo = inversion(r10[r10.gross < GSTAR_PRE], "record 10bps low gross")
    p_hi = inversion(r10[r10.gross >= GSTAR_PRE], "record 10bps high gross")
    for d in (p_all, p_g, p_lo, p_hi):
        print(f"  {d['slice']:36s} n={d['n']:6d} rate={d['rate']:.4f} "
              f"med pass {d['med_pass']:.2f} vs fail {d['med_fail']:.2f}  delta {d['delta']:+.2f}  inverted={d['inverted']}")
    print(f"\n  S1 (gross->4b) / S2 (gross->turnover) spearman at 10 bps: "
          f"{spearman(r10.gross, r10.pass4b.astype(float)):+.4f} / {spearman(r10.gross, r10.turn_x):+.4f}")
    li = liveinv[(liveinv.rung == 10)]
    print("\n  live grid @10bps: pooled delta "
          f"{li[li.stratum == 'pooled'].delta.iloc[0]:+.4f}; "
          f"low(<0.90) {li[(li.stratum=='low')&(li.gstar==GSTAR_PRE)].delta.iloc[0]:+.4f}; "
          f"high(>=0.90) {li[(li.stratum=='high')&(li.gstar==GSTAR_PRE)].delta.iloc[0]:+.4f}")
    print(f"  live grid 4a passes @10bps: {int(grid.p4a_10.sum())}/{len(grid)}; "
          f"4b passes @10bps: {int(grid.p4b_10.sum())}/{len(grid)}")
    print("\nDone.")


if __name__ == "__main__":
    main()
