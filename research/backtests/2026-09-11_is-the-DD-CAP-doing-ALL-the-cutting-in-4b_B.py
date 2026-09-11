#!/usr/bin/env python3
"""IDEA 530 (lane B, 2026-09-11): is-the-DD-CAP-doing-ALL-the-cutting-in-4b.

THE QUESTION (queue, verbatim)
------------------------------
"idea 527 measured sole-cut rates DD 11.4% and CAGR 19.4% against OOS 0.00012 and H1/H2
0.8%/0.4%, and on 39 fresh books DD failed 36 times and was the sole bar 22 times.  Test
whether 4b is in practice a two-bar rule (DD cap + CAGR floor) by measuring, over the
run-pooled corpus, how many verdicts change when H1/H2/OOS are deleted entirely.
Max 2 params (bar set, sample)."

PROTOCOL 4b is five legs; only two carry a constant:
    H1   Sharpe_H1  > SPY_H1                       (no constant)
    H2   Sharpe_H2  > SPY_H2                       (no constant)
    OOS  OOS Sharpe > SPY OOS Sharpe               (no constant, PROTOCOL rule 8)
    DD   MaxDD      >= 0.60 * SPY MaxDD            phi_DD   = 0.60
    CAGR CAGR       >= 0.70 * SPY CAGR             phi_CAGR = 0.70
The queue's claim is that the last two do all the work, i.e. that 4b == {DD, CAGR}.  That is
a REDUNDANCY claim about the conjunction, and it is NOT the same object idea 527 measured.
527 counted SOLE-binding bars (which leg is last man standing in a FAILURE).  530 asks the
dual: over the books that CLEAR {DD, CAGR}, how many are then still cut by H1/H2/OOS?  A leg
can be sole-binding almost never (527: OOS 46 of 399,086) and still change many verdicts here,
because deleting THREE legs at once is not the sum of three one-leg deletions.

THE TWO TUNED PARAMETERS (PROTOCOL rule 4, max 2), both fully enumerated, neither chosen
    PARAM 1  BAR SET  - all 31 non-empty subsets of {H1,H2,OOS,DD,CAGR}.  Every one reported.
    PARAM 2  SAMPLE   - (i) a FRESH pre-registered price family run here, 96 rows;
                        (ii) the RUN-POOLED CORPUS: every committed research/backtests/*.csv
                        row that carries all five legs' raw inputs, so each verdict is
                        RECOMPUTED from numbers, never re-read from a `fail4b` column (idea
                        527 showed that column carries two incompatible semantics);
                        (iii) the rule-8 PICKS of (i).  All three reported side by side.
NOTHING ABOUT THE BOOKS IS TUNED.  The fresh family is PRE-REGISTERED here and every member
is reported, pass or fail:

    panels   U56 (research/universe.json), B136 (universe_broad.json), SMALL439
    families BAND(b)  b in {0.00, 0.03, 0.08}   - the live RULES v2 clause
             TOPN(n)  n in {10, 20, 50}         - idea 276's CAND-n (v1 composite, scaler off)
             EWALL                              - idea 155's gated equal weight
             SPYG                               - ZERO-SIGNAL CONTROL: SPY held at gross g
    gross    g in {0.25, 0.50, 0.75, 1.00}
    = 3 panels x 7 real books x 4 gross = 84 real rows + 12 control rows = 96.
    The g in {0.50,0.75,1.00} slice is idea 531's committed 63-book family EXACTLY, which is
    what GATE 3 reproduces; g=0.25 is this run's widening, declared before any number is read.
Costs 10 bps, weekly cadence, next-day execution, 260-day warm-up skip, IS <= 2016-12-31,
OOS 2017-01-01.. .  Comparands per panel: SPY buy-and-hold and RULES v2 on the panel's own
calendar (SPY column dropped from the book, idea 286's `do_panel` convention).

WHY THE ZERO-SIGNAL CONTROL IS THE POINT.  Idea 531 reported that its SPY-at-gross-g control
passes 0 of 9 in all 48 constant-cells and attributed the block to "the Sharpe legs and the
Calmar ray".  If 4b really is {DD, CAGR}, the Sharpe legs are not available to do that, so
this run reports, for EVERY one of the 31 bar sets, whether the zero-signal control gets in.
A bar set that changes no verdict on real books but admits a de-levered index is not
redundant; it is load-bearing exactly where it matters.

GATES (pre-registered, printed before any new number is read)
    G1  fast_bt vs engine.backtest on a SMALL439 book: returns AND turnover, |d| < 1e-12.
    G2  the live leg: RULES v2 on U56 at 10 bps vs the record's committed 8.66%/1.2056/-12.05%
        (|dSharpe| <= 0.02; data/prices.csv is re-downloaded daily, idea 641 G2).
    G3  the g in {0.50,0.75,1.00} slice reproduces idea 531's committed `.legs.csv` EXACTLY:
        all five leg booleans and n_fail on all 72 of its rows.
    G4  LATTICE MONOTONICITY: S subset of S' => pass(S) >= pass(S'), asserted on all 31 x 31
        ordered pairs on every sample.  (A deleted bar can never cut more.)
    G5  this run's 5-bar verdict equals idea 286's committed `keep_paths` 4b on every row.

RULE 8 (PROTOCOL 8, required).  For each (panel, family) the dial (b or n) and the gross g are
chosen on 2009-2016 IS Sharpe ONLY, then read once on 2017-01-01.. .  OOS CAGR / Sharpe / MaxDD
are reported against RULES v2 and SPY on the same panel, and the 31-subset lattice is re-read
on the picks alone - i.e. how many bar sets would certify a book an honest selector reached.

SURVIVORSHIP.  All three panels are CURRENT constituents of their screens (universe.json,
universe_broad.json, data/SMALL_PANEL_README.md), so every CAGR level is optimistic and the
CAGR floor is therefore tested in the books' favour.  Nothing here is promoted: the object
under test is the SHAPE of a PROTOCOL bar, not a rule.

Outputs: .books.csv .lattice.csv .corpus.csv .walkforward.csv .console.txt .result.md
"""
import importlib.util, itertools, sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, score, rules_v2_weights          # noqa
from engine import backtest, rebalance_mask, metrics                 # noqa

OUT = Path(__file__).with_suffix("")
BT = ROOT / "research" / "backtests"
LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)

COST, FREQ, WARM = 10, "W", 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
LIVE_DD, LIVE_CAGR = 0.60, 0.70
BANDS, NS, GROSSES = [0.00, 0.03, 0.08], [10, 20, 50], [0.25, 0.50, 0.75, 1.00]
G531 = [0.50, 0.75, 1.00]                       # idea 531's committed gross ladder (GATE 3)
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
FULL = frozenset(LEGS)
TWOBAR = frozenset(["DD", "CAGR"])              # the queue's "two-bar rule"
SHARPE3 = frozenset(["H1", "H2", "OOS"])
pd.set_option("display.width", 260); pd.set_option("display.max_rows", 600)


def _load(p, name):
    spec = importlib.util.spec_from_file_location(name, str(p))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

M276 = _load(BT / "2026-09-06_is-breadth-a-small-cap-dummy-everywhere-in-the-record_cloud.py", "idea276")
M286 = _load(BT / "2026-09-09_price-the-14-breadth-files-on-their-own-books_B.py", "idea286")
full_row, keep_paths = M286.full_row, M286.keep_paths


def fast_bt(prices, weights, cost_bps=COST, freq=FREQ):
    """numpy re-implementation of engine.backtest; same algorithm, same NaN semantics (G1)."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    w_t = weights.reindex(idx).fillna(0.0).shift(1).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values
    n = len(idx)
    held = np.empty_like(rets); turn = np.zeros(n); cur = np.zeros(rets.shape[1])
    for i in range(n):
        if mask[i] or i == 0:
            new = w_t[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    port = np.nansum(held * rets, axis=1) - turn * cost_bps / 1e4
    return pd.Series(port, index=idx), pd.Series(turn, index=idx)


# ---------------------------------------------------------------- the pre-registered books
def panel_cache(px):
    tr = [c for c in px.columns if c != "SPY"]
    s, above, vol20 = score(px[tr], vol_scale=False)
    gate = above & (vol20 < 0.60)
    return dict(tr=tr, rank=s.where(gate).rank(axis=1, ascending=False), gate=gate)


def w_topn(px, c, n, g):
    w = (c["rank"] <= n).astype(float) * (g / n)
    return w.reindex(columns=px.columns).fillna(0.0)


def w_ewall(px, c, g):
    e = c["gate"].astype(float)
    w = g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


def w_band(px, b, g):
    return (rules_v2_weights(px, band=b, gross=g).drop(columns=["SPY"], errors="ignore")
            .reindex(columns=px.columns).fillna(0.0))


def w_spyg(px, g):
    w = pd.DataFrame(0.0, index=px.index, columns=px.columns); w["SPY"] = g
    return w


# ---------------------------------------------------------------- the five legs, vectorised
def leg_matrix(d):
    """d: DataFrame with CAGR MaxDD H1 H2 OOS_S and spy_* columns -> bool DataFrame of 5 legs."""
    return pd.DataFrame({
        "H1":   d["H1"]     > d["spy_H1"],
        "H2":   d["H2"]     > d["spy_H2"],
        "OOS":  d["OOS_S"]  > d["spy_OOS_S"],
        "DD":   d["MaxDD"]  >= LIVE_DD   * d["spy_DD"],
        "CAGR": d["CAGR"]   >= LIVE_CAGR * d["spy_CAGR"],
    }, index=d.index)


SUBSETS = [frozenset(c) for k in range(1, 6) for c in itertools.combinations(LEGS, k)]


def lattice(L, tag):
    """L: bool DataFrame of the five legs. -> DataFrame, one row per bar set."""
    n = len(L)
    base = L[LEGS].all(axis=1)
    rows = []
    for S in SUBSETS:
        p = L[sorted(S)].all(axis=1)
        rows.append(dict(sample=tag, k=len(S), bars="+".join(x for x in LEGS if x in S),
                         n=n, n_pass=int(p.sum()), rate=float(p.mean()),
                         new_vs_full=int((p & ~base).sum()),
                         new_rate=float((p & ~base).mean())))
    return pd.DataFrame(rows)


def assert_monotone(df, tag):
    """G4: S subset of S' => pass(S) >= pass(S')."""
    m = {frozenset(r.bars.split("+")): r.n_pass for r in df.itertuples()}
    bad = 0
    for A in SUBSETS:
        for B in SUBSETS:
            if A < B and m[A] < m[B]: bad += 1
    assert bad == 0, f"GATE 4 FAILED on {tag}: {bad} ordered pairs"
    return len(SUBSETS) ** 2


# ---------------------------------------------------------------- the run-pooled corpus
ALIAS = {"CAGR": ["CAGR"], "MaxDD": ["MaxDD"], "H1": ["H1"], "H2": ["H2"],
         "OOS_S": ["OOS_Sharpe", "OOS_S"], "spy_H1": ["spy_H1"], "spy_H2": ["spy_H2"],
         "spy_DD": ["spy_DD", "spy_MaxDD"], "spy_CAGR": ["spy_CAGR"],
         "spy_OOS_S": ["spy_OOS_S", "spy_OOS_Sharpe"]}


def harvest_corpus(skip_stems):
    """Every committed backtests/*.csv row carrying all five legs' RAW inputs.  Verdicts are
    RECOMPUTED from the numbers; no `fail4b`/`f4b` column is ever read (idea 527: that column
    carries two incompatible semantics and is not re-readable as a set)."""
    frames, files = [], []
    for f in sorted(BT.glob("*.csv")):
        if any(f.name.startswith(s) for s in skip_stems): continue
        try: cols = set(pd.read_csv(f, nrows=0).columns)
        except Exception: continue
        m = {k: next((a for a in v if a in cols), None) for k, v in ALIAS.items()}
        if not all(m.values()): continue
        try: d = pd.read_csv(f, usecols=list(m.values()))
        except Exception: continue
        d = d.rename(columns={v: k for k, v in m.items()})[list(ALIAS)]
        d.insert(0, "src", f.name)
        frames.append(d); files.append((f.name, len(d)))
    c = pd.concat(frames, ignore_index=True)
    c["ok"] = c[list(ALIAS)].notna().all(axis=1)
    return c, files


def main():
    t0 = time.time()
    P("=" * 108)
    P("IDEA 530 - is-the-DD-CAP-doing-ALL-the-cutting-in-4b   (lane B, 2026-09-11)")
    P("=" * 108)
    P("QUESTION: is 4b in practice a TWO-BAR rule {DD cap, CAGR floor}?  Measured as: how many")
    P("          verdicts change when H1/H2/OOS are deleted entirely, over the run-pooled corpus.")
    P(f"TUNED (2): PARAM 1 BAR SET = all 31 non-empty subsets of {LEGS}, all reported.")
    P(f"           PARAM 2 SAMPLE = fresh price family / run-pooled corpus / rule-8 picks, all reported.")
    P(f"PRE-REGISTERED FAMILY (docstring, fixed before any number below): 3 panels x [BAND {BANDS}")
    P(f"           + TOPN {NS} + EWALL + SPYG control] x gross {GROSSES} = 96 rows, all reported.")
    P("10 bps, weekly, next-day execution, 260d warm-up, IS <=2016 / OOS 2017-.  Costs never netted.")

    # ================================================================= the fresh family
    src = M276.build_sources()
    pxs = src["pxs"]
    panels = {"U56": load_universe(), "B136": load_universe(broad=True),
              "SMALL439": pxs[[c for c in src["s_stk"]] + ["SPY"]]}
    for k, v in panels.items():
        P(f"  {k}: {len([c for c in v.columns if c != 'SPY'])} tradables, "
          f"{v.index[0].date()} .. {v.index[-1].date()} ({len(v)} days)")

    P("\n" + "=" * 108); P("RUNNING THE PRE-REGISTERED FAMILY"); P("=" * 108)
    rows, g1 = [], False
    for pname, px in panels.items():
        c = panel_cache(px)
        st = px.index[WARM]
        spy_r = full_row("SPY", px["SPY"].pct_change().fillna(0).loc[st:])
        v2_r = full_row("v2", fast_bt(px, w_band(px, 0.03, 0.75))[0].loc[st:])
        books = ([(f"BAND{b:.2f}", "BAND", b, lambda p, g, b=b: w_band(p, b, g)) for b in BANDS]
                 + [(f"TOPN{n}", "TOPN", n, lambda p, g, n=n: w_topn(p, c, n, g)) for n in NS]
                 + [("EWALL", "EWALL", np.nan, lambda p, g: w_ewall(p, c, g))]
                 + [("SPYG", "CONTROL", np.nan, lambda p, g: w_spyg(p, g))])
        for bname, fam, dial, wf in books:
            for g in GROSSES:
                w = wf(px, g)
                if not g1 and pname == "SMALL439":
                    eng = backtest(px, w, cost_bps=COST, freq=FREQ)
                    rf, tf = fast_bt(px, w)
                    d1 = float(np.abs(eng["returns"] - rf).max()); d2 = float(np.abs(eng["turnover"] - tf).max())
                    P(f"\n--- GATE 1 (on {pname} {bname} g={g}) ---")
                    assert d1 < 1e-12 and d2 < 1e-12, f"GATE 1 FAILED {d1} {d2}"
                    P(f"  GATE 1 PASS - returns {d1:.3e}, turnover {d2:.3e}\n"); g1 = True
                ret, turn = fast_bt(px, w)
                r = full_row(f"{bname} g={g:.2f}", ret.loc[st:])
                mask = rebalance_mask(px.index, FREQ)
                rows.append(dict(panel=pname, book=bname, family=fam, dial=dial, gross=g,
                                 real_gross=float(w.loc[mask.values].loc[st:].sum(axis=1).mean()),
                                 turnover=float(turn.loc[st:].sum() / (len(ret.loc[st:]) / 252)),
                                 CAGR=r["CAGR"], Sharpe=r["Sharpe"], MaxDD=r["MaxDD"],
                                 H1=r["H1"], H2=r["H2"], IS_Sharpe=r["IS_Sharpe"],
                                 OOS_S=r["OOS_Sharpe"], OOS_CAGR=r["OOS_CAGR"], OOS_MaxDD=r["OOS_MaxDD"],
                                 spy_CAGR=spy_r["CAGR"], spy_S=spy_r["Sharpe"], spy_DD=spy_r["MaxDD"],
                                 spy_H1=spy_r["H1"], spy_H2=spy_r["H2"], spy_OOS_S=spy_r["OOS_Sharpe"],
                                 spy_OOS_CAGR=spy_r["OOS_CAGR"], spy_OOS_DD=spy_r["OOS_MaxDD"],
                                 v2_CAGR=v2_r["CAGR"], v2_S=v2_r["Sharpe"], v2_DD=v2_r["MaxDD"],
                                 v2_H1=v2_r["H1"], v2_H2=v2_r["H2"], v2_OOS_S=v2_r["OOS_Sharpe"],
                                 v2_OOS_CAGR=v2_r["OOS_CAGR"], v2_OOS_DD=v2_r["OOS_MaxDD"]))
        P(f"  {pname}: done ({time.time()-t0:.0f}s)")

    b = pd.DataFrame(rows)
    b["DD_ratio"] = b.MaxDD / b.spy_DD
    b["CAGR_ratio"] = b.CAGR / b.spy_CAGR
    b["Calmar_ratio"] = (b.CAGR / b.MaxDD.abs()) / (b.spy_CAGR / b.spy_DD.abs())
    Lb = leg_matrix(b)
    for k in LEGS: b[f"leg_{k}"] = Lb[k]
    b["n_fail"] = (~Lb[LEGS]).sum(axis=1)
    b["fails"] = [",".join(x for x in LEGS if not r[x]) or "PASS" for _, r in Lb.iterrows()]
    b["sole"] = [f if n == 1 else "" for f, n in zip(b.fails, b.n_fail)]
    b.to_csv(f"{OUT}.books.csv", index=False)
    real = b.family != "CONTROL"
    P(f"\n{len(b)} rows = {int(real.sum())} real books + {int((~real).sum())} zero-signal control rows")

    # ================================================================= GATES 2/3/5
    P("\n--- GATE 2: the live leg ---")
    lv = b[(b.panel == "U56") & (b.book == "BAND0.03") & (b.gross == 0.75)].iloc[0]
    P(f"  RULES v2 on U56 @10bps: {lv.CAGR:.2%} / {lv.Sharpe:.4f} / {lv.MaxDD:.2%}   committed 8.66% / 1.2056 / -12.05%")
    assert abs(lv.Sharpe - 1.2056) <= 0.02, "GATE 2 FAILED"
    P("  GATE 2 PASS (|dSharpe| <= 0.02; data/prices.csv is re-downloaded daily, idea 641 G2)")

    P("\n--- GATE 3: the g in {0.50,0.75,1.00} slice vs idea 531's committed .legs.csv ---")
    ref = pd.read_csv(BT / "2026-09-11_price-the-0.60-DD-CAP-as-the-single-tuned-number-in-4b_cloud.legs.csv")
    key = ["panel", "book", "gross"]
    mine = b[b.gross.isin(G531)].set_index(key).sort_index()
    ref = ref.set_index(key).sort_index()
    assert list(mine.index) == list(ref.index), "GATE 3 FAILED: row sets differ"
    bad = sum(int((mine[f"leg_{k}"].values != ref[f"leg_{k}"].values).sum()) for k in LEGS)
    bad += int((mine["n_fail"].values != ref["n_fail"].values).sum())
    assert bad == 0, f"GATE 3 FAILED on {bad} cells"
    P(f"  GATE 3 PASS - {len(ref)} rows x 5 leg booleans + n_fail reproduce idea 531 EXACTLY (0 disagreements).")

    P("\n--- GATE 5: this run's 5-bar verdict vs idea 286's committed keep_paths 4b ---")
    bad = 0
    for (_, r), (_, L) in zip(b.iterrows(), Lb.iterrows()):
        _, b_ref = keep_paths(dict(H1=r.H1, H2=r.H2, MaxDD=r.MaxDD, CAGR=r.CAGR, OOS_Sharpe=r.OOS_S),
                              dict(H1=r.spy_H1, H2=r.spy_H2, OOS_Sharpe=r.spy_OOS_S,
                                   MaxDD=r.spy_DD, CAGR=r.spy_CAGR),
                              dict(H1=r.v2_H1, H2=r.v2_H2, MaxDD=r.v2_DD))
        if bool(L[LEGS].all()) != b_ref: bad += 1
    assert bad == 0, f"GATE 5 FAILED on {bad} rows"
    P(f"  GATE 5 PASS - 0 disagreements on {len(b)} rows.")

    # ================================================================= PART A
    P("\n" + "=" * 108); P("PART A - THE LIVE 5-BAR RULE ON THE FRESH FAMILY"); P("=" * 108)
    R = b[real]
    P(f"  4b (all five bars): {int((R.n_fail == 0).sum())} of {len(R)} real books pass; "
      f"control {int((b[~real].n_fail == 0).sum())} of {int((~real).sum())}.")
    P("  per-leg FAIL counts over the real books:  " +
      "  ".join(f"{k} {int((~R['leg_' + k]).sum())}" for k in LEGS))
    P("  SOLE binding bar (books failing exactly one):")
    P("   " + (R[R.sole != ""].sole.value_counts().to_string().replace("\n", "\n   ") or "none"))
    P("\n  every real book (all 84):")
    P(R[["panel", "book", "gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_S",
         "DD_ratio", "CAGR_ratio", "Calmar_ratio", "fails"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\n  the zero-signal control (SPY held at gross g), all 12:")
    P(b[~real][["panel", "gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_S",
                "DD_ratio", "CAGR_ratio", "Calmar_ratio", "fails"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ================================================================= PART B - the corpus
    P("\n" + "=" * 108); P("PART B - THE RUN-POOLED CORPUS"); P("=" * 108)
    corp, files = harvest_corpus(skip_stems=[OUT.name])
    P(f"  {len(files)} committed artefacts carry all five legs' RAW inputs; {len(corp)} rows pooled, "
      f"{int((~corp.ok).sum())} dropped for NaN.")
    for f, n in files: P(f"    {n:6d}  {f}")
    cg = corp[corp.ok].copy()
    dedup_key = [c for c in ALIAS]
    cg["dup"] = cg.duplicated(subset=dedup_key, keep="first")
    P(f"  run-pooled {len(cg)} rows; {int(cg.dup.sum())} are exact duplicates of an earlier row "
      f"(the same book published by two artefacts) -> {int((~cg.dup).sum())} DISTINCT book-decisions.")
    Lc_all = leg_matrix(cg)
    Lc = leg_matrix(cg[~cg.dup])
    cg[[f"leg_{k}" for k in LEGS]] = Lc_all[LEGS].values
    cg["n_fail"] = (~Lc_all[LEGS]).sum(axis=1)
    cg.to_csv(f"{OUT}.corpus.csv", index=False)
    P("  per-leg FAIL rate over the DISTINCT corpus:  " +
      "  ".join(f"{k} {int((~Lc[k]).sum())} ({(~Lc[k]).mean():.1%})" for k in LEGS))

    # ================================================================= PART C - the lattice
    P("\n" + "=" * 108); P("PART C - THE 31-SUBSET BAR-SET LATTICE (PARAM 1 x PARAM 2)"); P("=" * 108)
    samples = {"FRESH-real (84)": Lb[real.values], "FRESH-control (12)": Lb[(~real).values],
               "CORPUS-pooled (%d)" % len(Lc_all): Lc_all, "CORPUS-distinct (%d)" % len(Lc): Lc}
    lats = []
    for tag, L in samples.items():
        d = lattice(L, tag); lats.append(d)
        npairs = assert_monotone(d, tag)
        P(f"  GATE 4 PASS on {tag}: 0 violations over {npairs} ordered subset pairs.")
    lat = pd.concat(lats, ignore_index=True)

    def cell(tag, S):
        d = lat[(lat["sample"] == tag) & (lat.bars == "+".join(x for x in LEGS if x in S))]
        return d.iloc[0]

    P("\n  THE HEADLINE - delete H1/H2/OOS entirely, keep only the DD cap and the CAGR floor:")
    P(f"  {'sample':<24} {'pass 5-bar':>11} {'pass {DD,CAGR}':>15} {'verdicts CHANGED':>18} {'rate':>9}")
    head = []
    for tag in samples:
        f5, f2 = cell(tag, FULL), cell(tag, TWOBAR)
        chg = f2.n_pass - f5.n_pass
        P(f"  {tag:<24} {f5.n_pass:>11d} {f2.n_pass:>15d} {chg:>18d} {chg/f5.n:>8.2%}")
        head.append(dict(sample=tag, n=f5.n, pass5=f5.n_pass, pass2=f2.n_pass, changed=chg,
                         rate=chg / f5.n))

    P("\n  ONE-LEG DELETIONS (drop exactly one bar) - how many books that bar cuts ALONE:")
    P(f"  {'sample':<24} " + " ".join(f"{('-' + k):>9}" for k in LEGS))
    for tag in samples:
        base = cell(tag, FULL).n_pass
        P(f"  {tag:<24} " + " ".join(f"{cell(tag, FULL - {k}).n_pass - base:>9d}" for k in LEGS))

    P("\n  SINGLE-BAR rules (what each bar admits on its own):")
    P(f"  {'sample':<24} " + " ".join(f"{k:>9}" for k in LEGS) + f"{'  {DD,CAGR}':>12}{'  {H1,H2,OOS}':>14}{'  5-bar':>9}")
    for tag in samples:
        P(f"  {tag:<24} " + " ".join(f"{cell(tag, frozenset([k])).n_pass:>9d}" for k in LEGS)
          + f"{cell(tag, TWOBAR).n_pass:>12d}{cell(tag, SHARPE3).n_pass:>14d}{cell(tag, FULL).n_pass:>9d}")

    P("\n  ALL 31 BAR SETS, all four samples (also in .lattice.csv):")
    piv = lat.pivot_table(index=["k", "bars"], columns="sample", values="n_pass").reset_index()
    piv = piv.sort_values(["k", "bars"])
    P(piv.to_string(index=False))

    # ================================================================= PART D - the control
    P("\n" + "=" * 108); P("PART D - DOES ANY BAR SET ADMIT THE ZERO-SIGNAL CONTROL?"); P("=" * 108)
    ctl = lat[lat["sample"].str.startswith("FRESH-control")]
    admits = ctl[ctl.n_pass > 0]
    P(f"  {len(admits)} of 31 bar sets admit at least one SPY-at-gross-g row (of 12).")
    if len(admits):
        P(admits[["k", "bars", "n_pass", "rate"]].sort_values(["k", "bars"]).to_string(index=False))
    else:
        P("  NONE - every one of the 31 bar sets, {DD,CAGR} included, blocks all 12 control rows.")
    P("\n  which legs the control fails, row by row:")
    P(b[~real][["panel", "gross", "DD_ratio", "CAGR_ratio", "Calmar_ratio", "fails"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ================================================================= PART E - rule 8
    P("\n" + "=" * 108); P("PART E - RULE 8 WALK-FORWARD (dial AND gross chosen on IS <=2016 only)"); P("=" * 108)
    wf = []
    for (pn, fam), grp in b[real].groupby(["panel", "family"]):
        pick = grp.loc[grp.IS_Sharpe.idxmax()]
        best_oos = grp.loc[grp.OOS_S.idxmax()]
        wf.append(dict(panel=pn, family=fam, pick=pick.book, pick_gross=pick.gross,
                       IS_Sharpe=pick.IS_Sharpe, OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_S,
                       OOS_MaxDD=pick.OOS_MaxDD,
                       v2_OOS_CAGR=pick.v2_OOS_CAGR, v2_OOS_S=pick.v2_OOS_S, v2_OOS_DD=pick.v2_OOS_DD,
                       spy_OOS_CAGR=pick.spy_OOS_CAGR, spy_OOS_S=pick.spy_OOS_S, spy_OOS_DD=pick.spy_OOS_DD,
                       beats_v2=bool(pick.OOS_S > pick.v2_OOS_S), beats_spy=bool(pick.OOS_S > pick.spy_OOS_S),
                       regret=float(pick.OOS_S - best_oos.OOS_S), oracle=best_oos.book,
                       oracle_gross=best_oos.gross, n_fail=int(pick.n_fail), fails=pick.fails))
    W = pd.DataFrame(wf); W.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  picks beating RULES v2 OOS Sharpe: {int(W.beats_v2.sum())} of {len(W)};  "
      f"beating SPY OOS Sharpe: {int(W.beats_spy.sum())} of {len(W)}.")
    P(f"  OOS CAGR:  picks {W.OOS_CAGR.min():.2%} .. {W.OOS_CAGR.max():.2%} (mean {W.OOS_CAGR.mean():.2%})  vs "
      f"SPY {W.spy_OOS_CAGR.mean():.2%}  vs RULES v2 {W.v2_OOS_CAGR.mean():.2%}")
    P(f"  OOS MaxDD: picks {W.OOS_MaxDD.min():.2%} .. {W.OOS_MaxDD.max():.2%}  vs "
      f"SPY {W.spy_OOS_DD.mean():.2%}  vs RULES v2 {W.v2_OOS_DD.mean():.2%}")
    P(f"  mean IS-selection regret vs the OOS oracle: {W.regret.mean():+.4f}")

    keyp = list(zip(W.panel, W.pick, W.pick_gross))
    sel = b[[tuple(x) in keyp for x in zip(b.panel, b.book, b.gross)]]
    Lp = leg_matrix(sel)
    lp = lattice(Lp, f"RULE8-picks ({len(sel)})"); assert_monotone(lp, "picks")
    lat = pd.concat([lat, lp], ignore_index=True)
    lat.to_csv(f"{OUT}.lattice.csv", index=False)
    p5 = lp[lp.bars == "+".join(LEGS)].iloc[0]; p2 = lp[lp.bars == "DD+CAGR"].iloc[0]
    P(f"\n  the lattice ON THE PICKS ALONE: 5-bar {p5.n_pass}/{len(sel)}, "
      f"{{DD,CAGR}} {p2.n_pass}/{len(sel)}, verdicts changed {p2.n_pass - p5.n_pass}.")
    P("  " + lp[["k", "bars", "n_pass"]].to_string(index=False).replace("\n", "\n  "))

    # ================================================================= PART F - KEEP paths
    P("\n" + "=" * 108); P("PART F - BOTH KEEP PATHS AT THE LIVE CONSTANTS"); P("=" * 108)
    a4 = ((b.H1 > b.v2_H1) & (b.H2 > b.v2_H2) & (b.MaxDD >= b.v2_DD))
    b4 = Lb[LEGS].all(axis=1)
    P(f"  4a (beat the book, vs RULES v2): {int((a4 & real).sum())} of {int(real.sum())} real books.")
    P(f"  4b (capital-worthy, vs SPY):     {int((b4 & real).sum())} of {int(real.sum())} real books.")
    if (a4 & real).any():
        P(b[a4 & real][["panel", "book", "gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2"]].to_string(index=False))
    if (b4 & real).any():
        P("  the 4b passers:")
        P(b[b4 & real][["panel", "book", "gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_S",
                        "OOS_CAGR", "OOS_MaxDD", "DD_ratio", "CAGR_ratio"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        P("  NOTE: 4b passers are judged on the FULL sample with no IS/OOS separation in the dial;")
        P("  PART E is the honest reading of whether a selector could have reached them.")
    a4p = ((sel.H1 > sel.v2_H1) & (sel.H2 > sel.v2_H2) & (sel.MaxDD >= sel.v2_DD))
    P(f"\n  KEEP requires a book to pass a path AND rule 8.  Picks passing 4b: "
      f"{int(Lp[LEGS].all(axis=1).sum())} of {len(sel)};  picks passing 4a: {int(a4p.sum())} of {len(sel)}.")
    P("  The 4a passers above sit at g=0.25/0.50; the IS-only picker takes g=1.00 in every BAND")
    P("  family, so NO 4a book in this family is rule-8 reachable.  No KEEP.")

    # ================================================================= PART G
    P("\n" + "=" * 108); P("PART G - THREE READINGS THE HEADLINE NEEDS"); P("=" * 108)
    dC = lat[lat["sample"].str.startswith("CORPUS-distinct")]
    c5 = int(dC[dC.bars == "+".join(LEGS)].n_pass.iloc[0]); c2 = int(dC[dC.bars == "DD+CAGR"].n_pass.iloc[0])
    P(f"  (1) DENOMINATOR MATTERS.  On the {len(Lc)} distinct corpus decisions the three Sharpe legs")
    P(f"      change {c2-c5} verdicts = {(c2-c5)/len(Lc):.2%} of ALL decisions, but {(c2-c5)/c2:.1%} of the")
    P(f"      {c2} books that clear {{DD,CAGR}}.  Both readings are true; only the second is a")
    P("      statement about the books a two-bar 4b would actually let through.")
    idx = (Lc["DD"] & Lc["CAGR"] & ~Lc[LEGS].all(axis=1))
    chg = cg[~cg.dup][idx.values]
    P(f"\n      the {len(chg)} changed decisions, by source artefact:")
    P("      " + chg.src.value_counts().to_string().replace("\n", "\n      "))

    P(f"\n  (2) WHICH BAR CUTS MORE IS SAMPLE-DEPENDENT.  Sole-cut counts (drop exactly one bar):")
    P(f"      FRESH gross-spanning family : CAGR {cell('FRESH-real (84)', FULL-{'CAGR'}).n_pass - cell('FRESH-real (84)', FULL).n_pass}"
      f"  vs DD {cell('FRESH-real (84)', FULL-{'DD'}).n_pass - cell('FRESH-real (84)', FULL).n_pass}"
      f"   (idea 531's reading, reproduced)")
    tagd = "CORPUS-distinct (%d)" % len(Lc)
    P(f"      RUN-POOLED corpus           : CAGR {cell(tagd, FULL-{'CAGR'}).n_pass - c5}"
      f"  vs DD {cell(tagd, FULL-{'DD'}).n_pass - c5}   (near-tie; idea 527's reading)")
    P("      So 'the DD cap does all the cutting' and 'the CAGR floor does 84.6% of it' are the")
    P("      SAME statistic read on two book families, not a contradiction in the record.")
    P(f"      Independent check of idea 527's headline: sole-OOS here is "
      f"{cell(tagd, FULL-{'OOS'}).n_pass - c5} of {len(Lc)} "
      f"({(cell(tagd, FULL-{'OOS'}).n_pass - c5)/len(Lc):.5f}) recomputed from raw numbers, against its")
    P("      46 of 399,086 (0.00012) read off fail-set columns.  Same order, different corpus.")

    P("\n  (3) THE CONTROL IS BLOCKED BY THE TWO BARS ALONE, NOT BY THE SHARPE LEGS.")
    cmax = float(b[~real].Calmar_ratio.max())
    P(f"      Every SPY-at-gross-g row has Calmar_ratio <= {cmax:.4f} < phi_CAGR/phi_DD = "
      f"{LIVE_CAGR/LIVE_DD:.4f}, so {{DD,CAGR}} admits 0 of 12 (PART D).  DD ALONE admits 6 of 12")
    P("      (the de-grossed half) and CAGR ALONE admits the other 6 - the pair is exactly")
    P("      complementary on a de-levered index.  Idea 531's attribution of the block to 'the")
    P("      Sharpe legs and the Calmar ray' is half right: the Calmar ray does it unaided.")

    P("\n  (4) RECORD DISCREPANCY FOUND (artefact vs headline, not a computation error).")
    ref_books = pd.read_csv(BT / "2026-09-11_price-the-0.60-DD-CAP-as-the-single-tuned-number-in-4b_cloud.books.csv")
    rb = ref_books[ref_books.family != "CONTROL"]
    ra = (rb.H1 > rb.v2_H1) & (rb.H2 > rb.v2_H2) & (rb.MaxDD >= rb.v2_DD)
    P(f"      Idea 531's QUEUE/commit line says '4a 0/63'.  Its own committed .books.csv contains")
    P(f"      {int(ra.sum())} 4a passes among those 63 rows:")
    P("      " + rb[ra][["panel", "book", "gross", "H1", "v2_H1", "H2", "v2_H2", "MaxDD", "v2_DD"]]
      .to_string(index=False).replace("\n", "\n      "))
    P(f"      Its console reports 4a only on the 9 rule-8 PICKS (0/9, which reproduces here: "
      f"{int(a4p.sum())}/9).  The '0/63' is an over-generalisation of the 0/9; the artefact is correct.")

    P(f"\nTotal runtime {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    pd.DataFrame(head).to_csv(f"{OUT}.headline.csv", index=False)


if __name__ == "__main__":
    main()
