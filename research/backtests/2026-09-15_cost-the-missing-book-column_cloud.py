#!/usr/bin/env python3
"""Idea 982 (cloud lane, 2026-09-15):
    cost-the-MISSING-book-COLUMN-on-the-pass4b-CORPUS

Idea 976's census could map only 701 of 7,055 committed M/Q 4b passes strictly (9.9%) and
3,913 widely (55.5%); 3,142 were unmappable, `book` missing on 3,111 of them.  The queue asks:
on THIS corpus, how many of the record's passes would a single required `book` column have
recovered, and what does the back-fill cost?

A column's cost is not a row count.  A label is worth exactly what it is needed to
ADJUDICATE, so this runs two legs:

  (A) SCHEMA AUDIT - scan every committed csv carrying a 4b-pass column, count the PASS rows
      that are already book-attributable, those recoverable from another committed column,
      those recoverable from the artifact's own sibling .py, and those needing hand work.
      Price the back-fill in files-to-touch and rows-to-rewrite.

  (B) PRICE LEG - what a missing book label actually costs is whether the book CHANGES the
      verdict inside its own cell.  Re-run 5 books x 3 panels x 2 gross x 4 cadences fresh at
      the protocol's 10 bps and measure, per (panel, gross, cadence) cell, whether the books
      disagree on 4b/4a.  If they never disagree, the label is cheap; if they usually do, a
      pass published without one is unadjudicable and the column is load-bearing.
      Rule 8 walk-forward included: book x gross chosen on 2009-2016 alone, 2017-2026 read once.

TUNED PARAMETERS: exactly 2, per the queue line - SCHEMA (BOOK_ONLY / BOOK_PLUS_PANEL /
CELL_KEY) and SCOPE (MQ / ALL / NONNULL).  Every level of both is reported; neither is chosen.

PROTOCOL: 10 bps, t -> t+1 execution (engine semantics, gate G1), both KEEP paths, rule 8.
Writes only research/backtests/* artifacts.  RULES.md / scan.py / bot.py / baseline.py
untouched.  No network.
"""
from __future__ import annotations
import sys, json, csv, re, warnings
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
warnings.filterwarnings("ignore")

from baseline import load_universe, rules_v2_weights, score  # noqa: E402
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa: E402

TODAY = "2026-09-15"
SLUG = "cost-the-missing-book-column"
OUT = Path(__file__).resolve().parent
COST_BPS = 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"

# ---------------------------------------------------------------- pre-registered bars
BAR_RECOVER  = 0.50  # H_RECOVER PASSES if a required `book` column would newly attribute
                     # >= 50% of the corpus's currently unattributed 4b PASS rows.
BAR_BACKFILL = 0.50  # H_BACKFILL PASSES if >= 50% of book-less pass-bearing artifacts can be
                     # back-filled AUTOMATICALLY (their own committed sibling .py names
                     # exactly one book), i.e. the back-fill is cheap.
BAR_PRICE    = 0.25  # H_PRICE PASSES if the book label flips the 4b verdict inside >= 25% of
                     # (panel, gross, cadence) cells - i.e. the column is load-bearing.
BAR_RULE8    = 1     # H_RULE8 PASSES if >= 1 rule-8 pick clears 4b out of sample.

# ==================================================================== fast engine-exact core
def fast_backtest(px: pd.DataFrame, w: pd.DataFrame, raw_mask: np.ndarray, cost_bps=COST_BPS):
    """Bit-for-bit reproduction of products/backtester/engine.backtest in numpy (gate G1).
    Row 0 of the shifted target is NaN in the engine too (it fills BEFORE shifting); that is
    reproduced here, and every window below starts at px.index[260], well past it."""
    P = px.to_numpy(dtype=float)
    R = np.zeros_like(P)
    with np.errstate(invalid="ignore", divide="ignore"):
        R[1:] = P[1:] / P[:-1] - 1.0
    R = np.nan_to_num(R, nan=0.0, posinf=0.0, neginf=0.0)
    W = np.nan_to_num(w.reindex(px.index).to_numpy(dtype=float), nan=0.0)
    WT = np.empty_like(W); WT[0] = np.nan; WT[1:] = W[:-1]
    M = np.zeros(len(P), dtype=bool); M[1:] = raw_mask[:-1]
    cur = np.zeros(P.shape[1]); port = np.zeros(len(P)); turn = np.zeros(len(P))
    for i in range(len(P)):
        if M[i] or i == 0:
            new = WT[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        port[i] = (cur * R[i]).sum() - turn[i] * cost_bps / 1e4
        growth = cur * (1.0 + R[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    return pd.Series(port, index=px.index), pd.Series(turn, index=px.index)

# ==================================================================== panels and books
def load_panels():
    u = load_universe(); b = load_universe(broad=True)
    s = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    s = s[[c for c in s.columns if c == "SPY" or c not in bad]]
    return {"U56": u, "B136": b, "SMALL": s}, len(bad)

def _topn(px, gross, n, vol_scale):
    s, above, vol20 = score(px, vol_scale=vol_scale)
    e = s.where(above & (vol20 < 0.60))
    return (e.rank(axis=1, ascending=False) <= n).astype(float) * (gross / n)

BOOKS = {
    "TOP10":    lambda px, g: _topn(px, g, 10, False),
    "TOP20":    lambda px, g: _topn(px, g, 20, False),   # the standing 2026-09-04 4b candidate
    "TOP20VOL": lambda px, g: _topn(px, g, 20, True),    # same book WITH the v1 vol scaler
    "EWELIG":   lambda px, g: (lambda e: g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0)
                               .fillna(0.0))(((lambda t: t[1] & (t[2] < 0.60))(score(px, vol_scale=False)))
                                             & px.notna()).astype(float),
    "BAND03":   lambda px, g: rules_v2_weights(px, band=0.03, gross=g),
}
GROSSES = [0.75, 1.00]
CADENCES = ["D", "W", "M", "Q"]

# ==================================================================== windows / legs
def windows(idx):
    start = idx[260]; full = idx[idx >= start]; h = len(full) // 2
    oos = idx[idx >= pd.Timestamp(OOS_START)]; oh = len(oos) // 2
    return dict(FULL=(full[0], full[-1]), H1=(full[0], full[h - 1]), H2=(full[h], full[-1]),
                IS=(full[0], pd.Timestamp(IS_END)), OOS=(oos[0], oos[-1]),
                OOSH1=(oos[0], oos[oh - 1]), OOSH2=(oos[oh], oos[-1]))

def wmetrics(r, win):
    return {k: (lambda m: (m["CAGR"], m["Sharpe"], m["MaxDD"]))(metrics(r.loc[a:b]))
            for k, (a, b) in win.items()}

def legs_4b(m, spy):
    return dict(L_H1=m["H1"][1] > spy["H1"][1], L_H2=m["H2"][1] > spy["H2"][1],
                L_OOS=m["OOS"][1] > spy["OOS"][1],
                L_DD=abs(m["FULL"][2]) <= 0.60 * abs(spy["FULL"][2]),
                L_CAGR=m["FULL"][0] >= 0.70 * spy["FULL"][0])

def legs_4b_oos(m, spy):
    return dict(L_H1=m["OOSH1"][1] > spy["OOSH1"][1], L_H2=m["OOSH2"][1] > spy["OOSH2"][1],
                L_OOS=m["OOS"][1] > spy["OOS"][1],
                L_DD=abs(m["OOS"][2]) <= 0.60 * abs(spy["OOS"][2]),
                L_CAGR=m["OOS"][0] >= 0.70 * spy["OOS"][0])

def legs_4a(m, base):
    return dict(A_H1=m["H1"][1] > base["H1"][1], A_H2=m["H2"][1] > base["H2"][1],
                A_DD=m["FULL"][2] >= base["FULL"][2])

def gate_g1(panels):
    worst, checks = 0.0, []
    for pname, px in panels.items():
        for bname, g, cad in [("TOP20", 0.75, "M"), ("EWELIG", 1.00, "Q"), ("BAND03", 0.75, "W")]:
            w = BOOKS[bname](px, g)
            mine, _ = fast_backtest(px, w, rebalance_mask(px.index, cad).to_numpy())
            theirs = engine_backtest(px, w, cost_bps=COST_BPS, freq=cad)["returns"]
            a, b = mine.to_numpy()[260:], theirs.to_numpy()[260:]
            d = float("inf") if not (np.isfinite(a).all() and np.isfinite(b).all()) \
                else float(np.abs(a - b).max())
            worst = max(worst, d); checks.append((pname, bname, g, cad, d))
    return worst, checks

# ==================================================================== (B) price leg
def build_grid(panels):
    rows = []
    for pname, px in panels.items():
        win = windows(px.index)
        spy = wmetrics(px["SPY"].pct_change().fillna(0.0), win)
        base_r, _ = fast_backtest(px, rules_v2_weights(px), rebalance_mask(px.index, "W").to_numpy())
        base = wmetrics(base_r, win)
        for bname, bfn in BOOKS.items():
            for g in GROSSES:
                w = bfn(px, g)
                for cad in CADENCES:
                    r, t = fast_backtest(px, w, rebalance_mask(px.index, cad).to_numpy())
                    m = wmetrics(r, win)
                    l4b, l4bo, l4a = legs_4b(m, spy), legs_4b_oos(m, spy), legs_4a(m, base)
                    yrs = len(r.loc[win["FULL"][0]:]) / 252
                    rows.append(dict(
                        panel=pname, book=bname, gross=g, cadence=cad, cost_bps=COST_BPS,
                        CAGR=m["FULL"][0], Sharpe=m["FULL"][1], MaxDD=m["FULL"][2],
                        H1=m["H1"][1], H2=m["H2"][1],
                        IS_CAGR=m["IS"][0], IS_Sharpe=m["IS"][1], IS_MaxDD=m["IS"][2],
                        OOS_CAGR=m["OOS"][0], OOS_Sharpe=m["OOS"][1], OOS_MaxDD=m["OOS"][2],
                        OOS_H1=m["OOSH1"][1], OOS_H2=m["OOSH2"][1],
                        turn_per_yr=float(t.loc[win["FULL"][0]:].sum()) / yrs,
                        spy_CAGR=spy["FULL"][0], spy_Sharpe=spy["FULL"][1], spy_MaxDD=spy["FULL"][2],
                        spy_H1=spy["H1"][1], spy_H2=spy["H2"][1],
                        spy_OOS_CAGR=spy["OOS"][0], spy_OOS_Sharpe=spy["OOS"][1],
                        spy_OOS_MaxDD=spy["OOS"][2],
                        base_Sharpe=base["FULL"][1], base_H1=base["H1"][1], base_H2=base["H2"][1],
                        base_MaxDD=base["FULL"][2], base_OOS_CAGR=base["OOS"][0],
                        base_OOS_Sharpe=base["OOS"][1], base_OOS_MaxDD=base["OOS"][2],
                        **l4b, pass4b=all(l4b.values()),
                        **{f"O{k}": v for k, v in l4bo.items()},
                        pass4b_OOSPURE=all(l4bo.values()),
                        **l4a, pass4a=all(l4a.values())))
        print(f"  grid: {pname} done ({len(rows)} rows)", flush=True)
    return pd.DataFrame(rows)

CHOOSERS = {
    "C_ISSHARPE": lambda d: d.sort_values(["IS_Sharpe", "book"], ascending=[False, True]).index[0],
    "C_ISCAGR":   lambda d: d.sort_values(["IS_CAGR", "book"], ascending=[False, True]).index[0],
    "C_ISCALMAR": lambda d: d.assign(_k=d.IS_CAGR / d.IS_MaxDD.abs().clip(lower=1e-9))
                             .sort_values(["_k", "book"], ascending=[False, True]).index[0],
}

def rule8(grid):
    """BOOK x GROSS chosen on 2009-2016 ALONE inside each (panel, cadence); 2017-2026 read once."""
    out = []
    for (pnl, cad), fam in grid.groupby(["panel", "cadence"]):
        blind = fam.pass4b_OOSPURE.mean()
        for cname, cfn in CHOOSERS.items():
            r = fam.loc[cfn(fam)]
            out.append(dict(panel=pnl, cadence=cad, chooser=cname, book=r.book, gross=r.gross,
                            n_candidates=len(fam), blind_4b_OOS=blind,
                            OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                            spy_OOS_CAGR=r.spy_OOS_CAGR, spy_OOS_Sharpe=r.spy_OOS_Sharpe,
                            spy_OOS_MaxDD=r.spy_OOS_MaxDD, base_OOS_Sharpe=r.base_OOS_Sharpe,
                            base_OOS_CAGR=r.base_OOS_CAGR,
                            pass4b_OOS=bool(r.pass4b_OOSPURE), pass4b_FULL=bool(r.pass4b),
                            pass4a=bool(r.pass4a)))
    return pd.DataFrame(out)

# ==================================================================== (A) schema audit
PASSCOLS = ["pass4b", "keep4b", "pass4b_REC", "pass4b_OOSPURE"]
BOOK_TOKENS = ["TOP5", "TOP10", "TOP20", "TOP30", "TOP40", "EWELIG", "BAND03", "BAND05",
               "BAND", "RULESV1", "RULESV2", "EWALL", "RANDROT", "CORE", "EXT", "MOM",
               "QQQ", "SPYBH", "FPORT", "CANON"]
TOKEN_RE = re.compile("|".join(sorted(BOOK_TOKENS, key=len, reverse=True)), re.I)
OTHER_LABEL_COLS = ["arm", "unit", "cell", "family", "dial", "name", "label", "scheme",
                    "point", "corpus", "variant", "strategy", "rule"]
NULLISH = re.compile(r"null|rand|coin|flip|perm|bootstrap|shuffle", re.I)
SELF = f"{TODAY}_{SLUG}_cloud"

def truthy(v):
    return str(v).strip().lower() in ("true", "1", "1.0", "yes", "y", "t")

def audit():
    rows = []
    files = sorted(OUT.glob("*.csv"))
    for f in files:
        if SELF in f.name:
            continue
        try:
            with open(f, newline="") as fh:
                head = next(csv.reader(fh))
        except Exception:
            continue
        pcs = [c for c in PASSCOLS if c in head]
        if not pcs:
            continue
        pc = pcs[0]
        try:
            df = pd.read_csv(f, low_memory=False)
        except Exception:
            continue
        if pc not in df.columns:
            continue
        p = df[pc].map(truthy)
        n_pass = int(p.sum())
        cad = df["cadence"].astype(str).str.upper() if "cadence" in df.columns else pd.Series(
            ["?"] * len(df), index=df.index)
        mq = cad.str.startswith(("M", "Q"))
        has_book = "book" in df.columns and df["book"].notna().any()
        # can the book be read off some OTHER committed column in this same file?
        other = False
        for c in OTHER_LABEL_COLS:
            if c in df.columns and df[c].astype(str).str.contains(TOKEN_RE).any():
                other = True; break
        # can it be back-filled automatically from the artifact's own committed sibling .py?
        stem = f.name.split(".")[0]
        sib = OUT / f"{stem}.py"
        toks = set()
        if sib.exists():
            try:
                toks = {t.upper() for t in TOKEN_RE.findall(sib.read_text(errors="ignore"))}
            except Exception:
                toks = set()
        has_panel = "panel" in df.columns
        has_cell = has_book and has_panel and "gross" in df.columns and "cadence" in df.columns
        rows.append(dict(file=f.name, passcol=pc, n_rows=len(df), n_pass=n_pass,
                         n_pass_MQ=int((p & mq).sum()), is_nullish=bool(NULLISH.search(f.name)),
                         has_book=bool(has_book), has_panel=bool(has_panel),
                         has_cell_key=bool(has_cell), other_col_has_book=bool(other),
                         sibling_py=sib.exists(), sibling_book_tokens=len(toks),
                         sibling_unique_book=(len(toks) == 1),
                         sibling_tokens=",".join(sorted(toks))[:80]))
    return pd.DataFrame(rows)

def audit_table(a):
    """The two tuned dials: SCHEMA x SCOPE.  Every level printed, none chosen."""
    scopes = {"ALL": a, "MQ": a[a.n_pass_MQ > 0], "NONNULL": a[~a.is_nullish]}
    out = []
    for sname, d in scopes.items():
        col = "n_pass_MQ" if sname == "MQ" else "n_pass"
        tot = int(d[col].sum())
        if tot == 0:
            continue
        for schema, ok in [("BOOK_ONLY", d.has_book),
                           ("BOOK_PLUS_PANEL", d.has_book & d.has_panel),
                           ("CELL_KEY", d.has_cell_key)]:
            ident = int(d.loc[ok, col].sum())
            out.append(dict(scope=sname, schema=schema, files=len(d),
                            pass_rows=tot, identified=ident, share_identified=ident / tot,
                            unidentified=tot - ident,
                            share_unidentified=1 - ident / tot))
    return pd.DataFrame(out)

# ==================================================================== main
def main():
    print("=" * 100)
    print(f"IDEA 982  {SLUG}   (cloud lane, {TODAY})")
    print("Pre-registered bars: RECOVER >= %.2f | BACKFILL >= %.2f | PRICE >= %.2f | RULE8 >= %d"
          % (BAR_RECOVER, BAR_BACKFILL, BAR_PRICE, BAR_RULE8))
    print("=" * 100)

    panels, n_dropped = load_panels()
    for k, v in panels.items():
        print(f"  panel {k:6s}: {v.shape[1]-1} names + SPY, {v.index[0].date()} -> {v.index[-1].date()}")
    print(f"  SMALL: dropped {n_dropped} tickers with max_1d_move >= 1.0 per data/small_meta.csv")

    print("\n--- GATE G1: fast core vs committed engine ---")
    worst, checks = gate_g1(panels)
    for c in checks:
        print(f"    {c[0]:6s} {c[1]:7s} g{c[2]:.2f} {c[3]}  max|diff| = {c[4]:.3e}")
    g1 = worst < 1e-12
    print(f"  G1 {'PASS' if g1 else 'FAIL'}  (worst {worst:.3e})")

    print("\n--- (A) schema audit of the pass4b corpus ---")
    a = audit()
    a.to_csv(OUT / f"{TODAY}_{SLUG}_cloud.audit.csv", index=False)
    print(f"  {len(a)} committed csv artifacts carry a 4b-pass column; "
          f"{int(a.n_pass.sum())} PASS rows ({int(a.n_pass_MQ.sum())} on an M/Q row).")
    print(f"  artifacts WITH a book column: {int(a.has_book.sum())} of {len(a)}; "
          f"with a full cell key: {int(a.has_cell_key.sum())}")
    tab = audit_table(a)
    tab.to_csv(OUT / f"{TODAY}_{SLUG}_cloud.schema.csv", index=False)
    print(tab.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    noident = a[~a.has_book]
    unid_rows = int(noident.n_pass.sum())
    recover = unid_rows / max(int(a.n_pass.sum()), 1)
    auto = noident[noident.sibling_unique_book]
    other = noident[noident.other_col_has_book]
    backfill = len(set(auto.file) | set(other.file)) / max(len(noident), 1)
    print(f"\n  BACK-FILL PRICE: {len(noident)} artifacts lack `book`, carrying "
          f"{unid_rows} PASS rows ({recover:.1%} of all committed PASS rows).")
    print(f"    recoverable from another committed column in the same file : {len(other)}")
    print(f"    recoverable from the artifact's own sibling .py (1 token)   : {len(auto)}")
    print(f"    sibling .py present but naming 0 or >1 book                 : "
          f"{int((noident.sibling_py & ~noident.sibling_unique_book).sum())}")
    print(f"    no sibling .py at all (hand work or re-run)                 : "
          f"{int((~noident.sibling_py).sum())}")
    print(f"    AUTO-BACK-FILLABLE SHARE: {backfill:.3f}")

    print("\n--- (B) price leg: does the BOOK label move the verdict inside its own cell? ---")
    grid = build_grid(panels)
    grid.to_csv(OUT / f"{TODAY}_{SLUG}_cloud.grid.csv", index=False)
    print(f"  {len(grid)} rows -> {TODAY}_{SLUG}_cloud.grid.csv")
    print(f"  full-sample 4b at 10 bps: {int(grid.pass4b.sum())} of {len(grid)}  |  "
          f"4a: {int(grid.pass4a.sum())} of {len(grid)}")
    cells = grid.groupby(["panel", "gross", "cadence"]).agg(
        n_books=("book", "nunique"), n4b=("pass4b", "sum"), n4a=("pass4a", "sum"),
        cagr_spread=("CAGR", lambda s: s.max() - s.min()),
        sharpe_spread=("Sharpe", lambda s: s.max() - s.min())).reset_index()
    cells["book_flips_4b"] = (cells.n4b > 0) & (cells.n4b < cells.n_books)
    cells["book_flips_4a"] = (cells.n4a > 0) & (cells.n4a < cells.n_books)
    cells.to_csv(OUT / f"{TODAY}_{SLUG}_cloud.cells.csv", index=False)
    print(cells.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    price4b = float(cells.book_flips_4b.mean()); price4a = float(cells.book_flips_4a.mean())
    print(f"\n  cells where the BOOK flips the 4b verdict: {int(cells.book_flips_4b.sum())} of "
          f"{len(cells)} ({price4b:.3f});  4a: {int(cells.book_flips_4a.sum())} ({price4a:.3f})")
    print(f"  median within-cell CAGR spread across books: {cells.cagr_spread.median():.2%};  "
          f"Sharpe spread: {cells.sharpe_spread.median():.3f}")

    print("\n--- RULE 8: book x gross chosen on 2009-2016 alone, 2017-2026 read once ---")
    r8 = rule8(grid)
    r8.to_csv(OUT / f"{TODAY}_{SLUG}_cloud.rule8.csv", index=False)
    print(f"  {len(r8)} picks.  OOS 4b: {int(r8.pass4b_OOS.sum())} of {len(r8)} "
          f"(blind within-cell base rate {r8.blind_4b_OOS.mean():.3f});  "
          f"OOS 4a: {int(r8.pass4a.sum())} of {len(r8)}")
    cols = ["panel", "cadence", "chooser", "book", "gross", "OOS_CAGR", "OOS_Sharpe",
            "OOS_MaxDD", "spy_OOS_Sharpe", "base_OOS_Sharpe", "pass4b_OOS", "pass4a"]
    if r8.pass4b_OOS.any():
        print("  OOS 4b passes:")
        print(r8[r8.pass4b_OOS][cols].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print("  best 5 picks by OOS Sharpe:")
    print(r8.sort_values("OOS_Sharpe", ascending=False).head(5)[cols].to_string(
        index=False, float_format=lambda x: f"{x:.3f}"))

    print("\n--- the standing 2026-09-04 KEEP-4b candidate (TOP20 equal weight), all rungs ---")
    cand = grid[(grid.book == "TOP20")][
        ["panel", "gross", "cadence", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR",
         "OOS_Sharpe", "OOS_MaxDD", "spy_CAGR", "spy_Sharpe", "spy_MaxDD", "pass4b",
         "pass4b_OOSPURE", "pass4a"]]
    print(cand.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    h_recover = recover >= BAR_RECOVER
    h_backfill = backfill >= BAR_BACKFILL
    h_price = price4b >= BAR_PRICE
    h_r8 = int(r8.pass4b_OOS.sum()) >= BAR_RULE8
    print("\n" + "=" * 100)
    for nm, ok, val, bar in [("H_RECOVER", h_recover, recover, BAR_RECOVER),
                             ("H_BACKFILL", h_backfill, backfill, BAR_BACKFILL),
                             ("H_PRICE", h_price, price4b, BAR_PRICE),
                             ("H_RULE8", h_r8, float(r8.pass4b_OOS.sum()), float(BAR_RULE8))]:
        print(f"  {nm:11s} {'PASS' if ok else 'FAIL'}   value {val:.3f}   bar {bar}")
    print(f"  GATE G1 {'PASS' if g1 else 'FAIL'}")
    print("=" * 100)

    summary = dict(gate_g1=bool(g1), g1_worst=worst,
                   audit_files=len(a), pass_rows=int(a.n_pass.sum()),
                   pass_rows_MQ=int(a.n_pass_MQ.sum()),
                   files_with_book=int(a.has_book.sum()),
                   unidentified_pass_rows=unid_rows, recover=recover,
                   backfill_auto_share=backfill, grid_rows=len(grid),
                   grid_pass4b=int(grid.pass4b.sum()), grid_pass4a=int(grid.pass4a.sum()),
                   price_book_flips_4b=price4b, price_book_flips_4a=price4a,
                   median_cell_cagr_spread=float(cells.cagr_spread.median()),
                   rule8_pass4b=int(r8.pass4b_OOS.sum()), rule8_pass4a=int(r8.pass4a.sum()),
                   rule8_blind=float(r8.blind_4b_OOS.mean()),
                   H_RECOVER=bool(h_recover), H_BACKFILL=bool(h_backfill),
                   H_PRICE=bool(h_price), H_RULE8=bool(h_r8))
    (OUT / f"{TODAY}_{SLUG}_cloud.summary.json").write_text(json.dumps(summary, indent=2))
    return summary

if __name__ == "__main__":
    main()
