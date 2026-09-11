#!/usr/bin/env python3
"""Idea 740 — is the SPY-IN-THE-COMPARAND convention worth a PROTOCOL clause of its own?

`baseline.load_universe()` returns SPY *inside* the price frame, so every comparand built by
`baseline.compare()` (RULES v2 today, RULES v1 before 2026-09-06) holds SPY as an INVESTABLE
NAME, while idea 538's panels() and several later scripts drop it.  Two readings of the same
sentence in PROTOCOL rule 3.  This script prices the difference.

Three treatments of the comparand's investable frame (the question axis, not a tuned dial):
  INCL  — px as returned by load_universe(): SPY is a constituent      (the live convention)
  ZERO  — SPY's weight forced to 0, denominator N unchanged            (position removed only)
  DROP  — SPY removed from the frame before weighting                  (the "noSPY" reading)
ZERO decomposes DROP-INCL into "lose the SPY position" and "re-spread over N-1".

TUNED PARAMETERS (max 2 per PROTOCOL rule 4): gross g and book n/form.  Everything else is
held at the live RULES v2 setting (band 0.03, weekly, 10 bps, next-day execution).

PART A  the comparand as a book: 3 panels x 3 treatments x {v2 @ g in 0.50/0.75/1.00, v1}
PART B  the record: identify which comparand each canonically-formatted LEADERBOARD row quotes,
        and re-adjudicate its 4a verdict under the SPY-free comparand
PART C  PROTOCOL rule 8 walk-forward: g fixed on IS <= 2016 only, 2017-2026 read once
Both KEEP paths (4a vs live RULES v2, 4b vs SPY) evaluated at every grid point.
"""
import json, re, sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, band_state  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics  # noqa

STEM = Path(__file__).with_suffix("").name
OUT = Path(__file__).resolve().parent
COST = 10.0          # PROTOCOL rule 2
FREQ = "W"           # live cadence
BAND = 0.03          # live RULES v2 band
IS_END, OOS_START = "2016-12-31", "2017-01-01"
GROSSES = [0.50, 0.75, 1.00]
TREATS = ["INCL", "ZERO", "DROP"]
pd.set_option("display.width", 200)


# ---------------------------------------------------------------- panels
def panels():
    out = {}
    out["U56"] = load_universe()
    out["B136"] = load_universe(broad=True)
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, meta.columns[0]]) if "max_1d_move" in meta else set()
    keep = [c for c in sm.columns if c == "SPY" or c not in bad]
    out[f"SMALL{len(keep)-1}"] = sm[keep]
    return out


def frame(px, treat):
    """The investable frame the comparand's weights are computed on."""
    return px.drop(columns=["SPY"]) if treat == "DROP" else px


def v2_weights(px, treat, g):
    w = rules_v2_weights(frame(px, treat), band=BAND, gross=g)
    if treat == "ZERO":
        w = w.copy(); w["SPY"] = 0.0          # position dropped, N (hence per-name weight) unchanged
    return w.reindex(columns=px.columns).fillna(0.0)


def v1_weights(px, treat, g=None):
    w = rules_v1_weights(frame(px, treat))
    if treat == "ZERO":
        w = w.copy(); w["SPY"] = 0.0          # SPY may win a top-5 slot; ZERO forfeits that slot to cash
    return w.reindex(columns=px.columns).fillna(0.0)


def run(px, w, start):
    res = backtest(px, w, cost_bps=COST, freq=FREQ)
    return res["returns"].loc[start:], res


def stats(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def keep4a(d, b):
    """PROTOCOL 4a: Sharpe > live rules in BOTH halves and MaxDD no worse."""
    return bool(d["H1"] > b["H1"] and d["H2"] > b["H2"] and d["MaxDD"] >= b["MaxDD"])


def keep4b(d, s, oos_ok=None):
    """PROTOCOL 4b: Sharpe > SPY in BOTH halves (and OOS), MaxDD <= 60% of SPY's, CAGR >= 70%."""
    legs = dict(H1=d["H1"] > s["H1"], H2=d["H2"] > s["H2"],
                DD=d["MaxDD"] >= 0.60 * s["MaxDD"], CAGR=d["CAGR"] >= 0.70 * s["CAGR"])
    if oos_ok is not None: legs["OOS"] = bool(oos_ok)
    return all(legs.values()), legs


# ---------------------------------------------------------------- gates
def gates(P):
    print("\n=== GATES (pre-registered) ===")
    px = P["U56"]; start = px.index[260]
    g1a, _ = run(px, rules_v2_weights(px, band=BAND, gross=0.75), start)
    g1b, _ = run(px, v2_weights(px, "INCL", 0.75), start)
    d1 = float(np.abs(g1a - g1b).max())
    print(f"G1 v2_weights(INCL) == baseline.rules_v2_weights: max|dr| {d1:.3e}   {'PASS' if d1 < 1e-15 else 'FAIL'}")

    m = stats(g1a)
    ok2 = abs(m["CAGR"] - 0.0866) < 5e-3 and abs(m["Sharpe"] - 1.2056) < 0.02 and abs(m["MaxDD"] + 0.1205) < 5e-3
    vintage = abs(m["Sharpe"] - 1.2056)          # prices.csv is re-downloaded daily (idea 641 G2)
    print(f"G2 live RULES v2 U56 @10bps  {m['CAGR']:.2%} / {m['Sharpe']:.4f} / {m['MaxDD']:.2%} "
          f"vs committed 8.66% / 1.2056 / -12.05%   {'PASS' if ok2 else 'FAIL'}  "
          f"(vintage gap {vintage:.4f} of Sharpe — the identification bar for PART B)")

    _, res = run(px, v2_weights(px, "INCL", 0.75), start)
    held = res["weights"].loc[start:]
    spy_share = (held["SPY"] / held.sum(axis=1).replace(0, np.nan)).mean()
    print(f"G3 SPY is a real POSITION in the live comparand, not just a denominator: mean share of "
          f"book {spy_share:.4%}, days held {(held['SPY'] > 0).mean():.1%}   "
          f"{'PASS' if spy_share > 0 else 'FAIL'}")

    z, _ = run(px, v2_weights(px, "ZERO", 0.75), start)
    dd, _ = run(px, v2_weights(px, "DROP", 0.75), start)
    print(f"G4 the three treatments are distinct books: max|r_INCL-r_ZERO| {float(np.abs(g1a-z).max()):.3e}, "
          f"max|r_ZERO-r_DROP| {float(np.abs(z-dd).max()):.3e}   "
          f"{'PASS' if float(np.abs(g1a-z).max()) > 0 and float(np.abs(z-dd).max()) > 0 else 'FAIL'}")
    return dict(G1=d1, G2=ok2, G3=float(spy_share), vintage=float(vintage))


# ---------------------------------------------------------------- part A
def part_a(P):
    print("\n=== PART A — the comparand as a book (all grid points reported) ===")
    rows = []
    for pname, px in P.items():
        start = px.index[260]
        spy_full = px["SPY"].pct_change().fillna(0).loc[start:]
        s_full = stats(spy_full)
        s_oos = stats(spy_full.loc[OOS_START:])
        for book, gs in (("v2band", GROSSES), ("v1rules", [np.nan])):
            for g in gs:
                for t in TREATS:
                    w = v2_weights(px, t, g) if book == "v2band" else v1_weights(px, t)
                    r, _ = run(px, w, start)
                    d = stats(r); o = stats(r.loc[OOS_START:])
                    p4b, legs = keep4b(d, s_full, oos_ok=o["Sharpe"] > s_oos["Sharpe"])
                    rows.append(dict(panel=pname, book=book, gross=g, treat=t, **d,
                                     OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"],
                                     SPY_CAGR=s_full["CAGR"], SPY_Sharpe=s_full["Sharpe"],
                                     SPY_MaxDD=s_full["MaxDD"], SPY_OOS_Sharpe=s_oos["Sharpe"],
                                     keep4b=p4b, **{f"leg_{k}": v for k, v in legs.items()}))
    df = pd.DataFrame(rows)
    # 4a is judged against the LIVE comparand: v2band, g=0.75, INCL, same panel
    live = {p: df[(df.panel == p) & (df.book == "v2band") & (df.gross == 0.75) & (df.treat == "INCL")].iloc[0]
            for p in P}
    df["keep4a"] = [keep4a(r, live[r["panel"]]) for _, r in df.iterrows()]
    df.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    show = df[["panel", "book", "gross", "treat", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
               "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "keep4a", "keep4b"]]
    print(show.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n--- the convention's size, per panel/book/gross: DROP - INCL and ZERO - INCL ---")
    deltas = []
    for (p, b, g), grp in df.groupby(["panel", "book", "gross"], dropna=False):
        gi = grp[grp.treat == "INCL"].iloc[0]
        for t in ("ZERO", "DROP"):
            gt = grp[grp.treat == t].iloc[0]
            deltas.append(dict(panel=p, book=b, gross=g, vs=f"{t}-INCL",
                               dCAGR_pp=100 * (gt.CAGR - gi.CAGR), dSharpe=gt.Sharpe - gi.Sharpe,
                               dH1=gt.H1 - gi.H1, dH2=gt.H2 - gi.H2,
                               dMaxDD_pp=100 * (gt.MaxDD - gi.MaxDD),
                               dOOS_Sharpe=gt.OOS_Sharpe - gi.OOS_Sharpe,
                               verdict_flip4b=bool(gt.keep4b != gi.keep4b)))
    dd = pd.DataFrame(deltas)
    dd.to_csv(OUT / f"{STEM}.deltas.csv", index=False)
    print(dd.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    return df, dd


# ---------------------------------------------------------------- part B
CANON = re.compile(
    r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*(.*?)\s*\|\s*(-?\d+\.\d)%\s*\|\s*(-?\d+\.\d\d)\s*\|\s*(-?\d+\.\d)%\s*\|"
    r"\s*(-?\d+\.\d\d)\s*/\s*(-?\d+\.\d\d)\s*\|\s*(-?\d+\.\d\d)\s*\(\s*(-?\d+\.\d\d)\s*/\s*(-?\d+\.\d\d)\s*\)\s*\|"
    r"\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*$")


def part_b0(df, vintage_gap):
    """Is the convention RESOLVABLE at the record's own reporting precision (2dp) at all?"""
    print("\n=== PART B0 — resolvability of the convention at published precision ===")
    print(f"the record publishes Sharpe at 2 dp -> rounding bin +/- 0.005; today's prices.csv vintage "
          f"moves the live comparand's Sharpe by {vintage_gap:.4f} (GATE G2)")
    rows = []
    for (p, b, g), grp in df.groupby(["panel", "book", "gross"], dropna=False):
        gi = grp[grp.treat == "INCL"].iloc[0]; gd = grp[grp.treat == "DROP"].iloc[0]
        d = abs(gd.Sharpe - gi.Sharpe); dh = max(abs(gd.H1 - gi.H1), abs(gd.H2 - gi.H2))
        rows.append(dict(panel=p, book=b, gross=g, dSharpe=d, dHalf_max=dh,
                         gt_2dp_bin=bool(max(d, dh) > 0.005),
                         gt_vintage=bool(max(d, dh) > vintage_gap)))
    r = pd.DataFrame(rows)
    print(r.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    r.to_csv(OUT / f"{STEM}.resolvability.csv", index=False)
    return r


def part_b2():
    """Source census: which reading does each committed backtest script actually run on?"""
    print("\n=== PART B2 — source census of the committed scripts (the code fact) ===")
    files = sorted((ROOT / "research" / "backtests").glob("*.py"))
    drop_pat = re.compile(r"drop\(\s*columns\s*=\s*\[?\s*[\"']SPY[\"']|columns\s*!=\s*[\"']SPY[\"']|"
                          r"c\s*!=\s*[\"']SPY[\"']|with_spy\s*=\s*False|\.remove\(\s*[\"']SPY[\"']")
    rows = []
    for f in files:
        s = f.read_text(errors="ignore")
        rows.append(dict(file=f.name, imports_baseline=bool(re.search(r"from baseline import|import baseline", s)),
                         calls_compare=bool(re.search(r"(?<!def )compare\(", s)),
                         drops_spy=bool(drop_pat.search(s))))
    c = pd.DataFrame(rows)
    n = len(c)
    print(f"committed backtest scripts: {n}")
    print(f"  import baseline                : {c.imports_baseline.sum()} ({c.imports_baseline.mean():.1%})")
    print(f"  call compare()  -> INCL by construction : {c.calls_compare.sum()} ({c.calls_compare.mean():.1%})")
    print(f"  build a SPY-free frame -> DROP reading  : {c.drops_spy.sum()} ({c.drops_spy.mean():.1%})")
    print(f"  BOTH readings in one file      : {int((c.calls_compare & c.drops_spy).sum())}")
    print(f"  neither (own book, SPY in frame): {int((~c.calls_compare & ~c.drops_spy).sum())}")
    c.to_csv(OUT / f"{STEM}.source_census.csv", index=False)
    return c


def part_b(df):
    print("\n=== PART B — the record: which comparand do the committed rows quote? ===")
    lb = (ROOT / "research" / "LEADERBOARD.md").read_text().split("\n")
    rows = []
    for ln in lb:
        m = CANON.match(ln)
        if m:
            rows.append(dict(date=m.group(1), idea=m.group(2)[:60], CAGR=float(m.group(3)) / 100,
                             Sharpe=float(m.group(4)), MaxDD=float(m.group(5)) / 100,
                             H1=float(m.group(6)), H2=float(m.group(7)),
                             bS=float(m.group(8)), bH1=float(m.group(9)), bH2=float(m.group(10)),
                             verdict=m.group(11)[:40], script=m.group(12)[:80]))
    rec = pd.DataFrame(rows)
    print(f"canonically-formatted rows in LEADERBOARD.md: {len(rec)} of {len(lb)} lines "
          f"({len(rec)/max(len(lb),1):.1%}) — the row set this part can adjudicate at all")
    if rec.empty:
        return rec, pd.DataFrame()

    # candidate comparands: every (panel, book, gross, treat) cell of PART A, at 2dp as published
    cand = df[["panel", "book", "gross", "treat", "Sharpe", "H1", "H2", "MaxDD"]].copy()
    cand["key"] = cand.apply(lambda r: f"{r.panel}/{r.book}/{r.gross}/{r.treat}", axis=1)

    def match(r):
        hits = cand[(cand.Sharpe.round(2) == r.bS) & (cand.H1.round(2) == r.bH1) & (cand.H2.round(2) == r.bH2)]
        return list(hits.key)

    rec["matches"] = rec.apply(match, axis=1)
    rec["n_match"] = rec.matches.str.len()
    rec["treats"] = rec.matches.apply(lambda ms: sorted({m.split("/")[-1] for m in ms}))
    rec["identified"] = rec.treats.apply(lambda t: t[0] if len(t) == 1 else ("ambiguous" if t else "none"))
    print("\nidentification of the quoted baseline triple (Sharpe, H1, H2) at published 2dp:")
    print(rec.identified.value_counts().to_string())
    for t in TREATS:
        n = int((rec.identified == t).sum())
        print(f"  uniquely {t}: {n} rows ({n/len(rec):.2%})")

    # re-adjudicate 4a: every canonical row against one panel's comparand under INCL and under DROP.
    # Sensitivity census (the row's own panel is not recoverable from the table), both comparand
    # versions: v2band g0.75 = the live rule, v1rules = the pre-2026-09-06 comparand ~3/4 of the
    # canonical rows actually quote.
    flips = []
    for p in df.panel.unique():
        for book, g in (("v2band", 0.75), ("v1rules", np.nan)):
            sel = (df.panel == p) & (df.book == book) & (df.gross.isna() if book == "v1rules" else df.gross == g)
            gi = df[sel & (df.treat == "INCL")].iloc[0]; gd = df[sel & (df.treat == "DROP")].iloc[0]
            a_i = rec.apply(lambda r: r.H1 > gi.H1 and r.H2 > gi.H2 and r.MaxDD >= gi.MaxDD, axis=1)
            a_d = rec.apply(lambda r: r.H1 > gd.H1 and r.H2 > gd.H2 and r.MaxDD >= gd.MaxDD, axis=1)
            flips.append(dict(panel=p, comparand=book, n_rows=len(rec), pass_INCL=int(a_i.sum()),
                              pass_DROP=int(a_d.sum()), flips=int((a_i != a_d).sum()),
                              flip_FAIL_to_PASS=int((~a_i & a_d).sum()),
                              flip_PASS_to_FAIL=int((a_i & ~a_d).sum())))
    fl = pd.DataFrame(flips)
    print("\n4a re-adjudication of every canonical row against the live-gross comparand, INCL vs DROP:")
    print(fl.to_string(index=False))
    rec.drop(columns=["matches"]).to_csv(OUT / f"{STEM}.census.csv", index=False)
    fl.to_csv(OUT / f"{STEM}.flips.csv", index=False)
    return rec, fl


# ---------------------------------------------------------------- part C
def part_c(P):
    print("\n=== PART C — PROTOCOL rule 8 walk-forward (g fixed on IS <= 2016, 2017-2026 read once) ===")
    rows = []
    for pname, px in P.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        s_oos, s_full = stats(spy.loc[OOS_START:]), stats(spy)
        base_is, base_oos = {}, {}
        b, _ = run(px, v2_weights(px, "INCL", 0.75), start)
        base_is, base_oos = stats(b.loc[:IS_END]), stats(b.loc[OOS_START:])
        for t in TREATS:
            cells = {}
            for g in GROSSES:
                r, _ = run(px, v2_weights(px, t, g), start)
                cells[g] = (stats(r.loc[:IS_END]), stats(r.loc[OOS_START:]), r)
            pick = max(GROSSES, key=lambda g: cells[g][0]["Sharpe"])          # selector: max IS Sharpe
            i, o, r = cells[pick]
            ok4b, legs = keep4b(o, s_oos)
            rows.append(dict(panel=pname, treat=t, pick_gross=pick,
                             IS_Sharpe=i["Sharpe"], IS_spread=max(c[0]["Sharpe"] for c in cells.values())
                             - min(c[0]["Sharpe"] for c in cells.values()),
                             OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"],
                             OOS_H1=o["H1"], OOS_H2=o["H2"],
                             base_OOS_Sharpe=base_oos["Sharpe"], base_OOS_CAGR=base_oos["CAGR"],
                             base_OOS_MaxDD=base_oos["MaxDD"],
                             SPY_OOS_CAGR=s_oos["CAGR"], SPY_OOS_Sharpe=s_oos["Sharpe"],
                             SPY_OOS_MaxDD=s_oos["MaxDD"],
                             OOS_4b=ok4b, **{f"oosleg_{k}": v for k, v in legs.items()},
                             OOS_4a=keep4a(o, base_oos)))
    wf = pd.DataFrame(rows)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    print(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\nOOS effect of the convention (DROP - INCL) on the walk-forward pick:")
    for p in wf.panel.unique():
        a = wf[(wf.panel == p) & (wf.treat == "INCL")].iloc[0]
        b = wf[(wf.panel == p) & (wf.treat == "DROP")].iloc[0]
        print(f"  {p:9s} pick {a.pick_gross}->{b.pick_gross}  dOOS_Sharpe {b.OOS_Sharpe-a.OOS_Sharpe:+.4f}  "
              f"dOOS_CAGR {100*(b.OOS_CAGR-a.OOS_CAGR):+.2f} pp  dOOS_MaxDD {100*(b.OOS_MaxDD-a.OOS_MaxDD):+.2f} pp  "
              f"4b {a.OOS_4b}->{b.OOS_4b}")
    return wf


if __name__ == "__main__":
    P = panels()
    for k, v in P.items(): print(f"panel {k}: {v.shape[1]} cols, {v.index[0].date()}..{v.index[-1].date()}")
    g = gates(P)
    A, D = part_a(P)
    RES = part_b0(A, g["vintage"])
    SRC = part_b2()
    rec, fl = part_b(A)
    wf = part_c(P)
    summ = dict(gates=g, n_grid=len(A), max_abs_dSharpe_DROP=float(D[D.vs == "DROP-INCL"].dSharpe.abs().max()),
                max_abs_dMaxDD_pp_DROP=float(D[D.vs == "DROP-INCL"].dMaxDD_pp.abs().max()),
                n_4b_flips=int(D.verdict_flip4b.sum()), n_canon_rows=int(len(rec)),
                identified=rec.identified.value_counts().to_dict() if len(rec) else {},
                rec_4a_flips=fl.to_dict("records") if len(fl) else [],
                resolvable_cells=int(RES.gt_2dp_bin.sum()), n_cells=int(len(RES)),
                src_compare=int(SRC.calls_compare.sum()), src_drops_spy=int(SRC.drops_spy.sum()),
                src_n=int(len(SRC)), vintage_gap=g["vintage"],
                wf_4b=wf[["panel", "treat", "pick_gross", "OOS_Sharpe", "OOS_4b"]].to_dict("records"))
    (OUT / f"{STEM}.summary.json").write_text(json.dumps(summ, indent=1, default=str))
    print("\nwrote", STEM + ".{grid,deltas,census,flips,walkforward}.csv + .summary.json")
