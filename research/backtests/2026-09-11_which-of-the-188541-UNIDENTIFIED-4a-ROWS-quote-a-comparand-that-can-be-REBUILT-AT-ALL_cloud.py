#!/usr/bin/env python3
"""Idea 739 - "which-of-the-188541-UNIDENTIFIED-4a-ROWS-quote-a-comparand-that-can-be-REBUILT-AT-ALL"
(cloud lane, 2026-09-11).

The question
------------
Idea 737 rebuilt five candidate 4a comparands (SAMEv2, SAMEv2_noSPY, CROSSv2, SAMEv1,
CROSSv1) and asked which one REPRODUCES each committed block's published 4a column.  It
identified 649 of 1,018 CANON blocks.  The other **369 blocks / 188,541 rows (48.8% of the
CANON 4a corpus)** are reproduced by NONE of the five, so for half the record the 4a column
cannot be reconstructed from PROTOCOL alone.

737's five candidates are all priced at ONE point: 10 bps, weekly, gross 0.75, evaluated
from `px.index[260]`.  This run asks whether the unidentified half is unidentified because
the record quotes an *unrebuildable* comparand - or merely because 737 priced the comparand
at the wrong KNOBS.  Each unidentified block's own script and its own CSV declare a cost
rung, a window, a gross and a cadence; this run rebuilds the comparand AT THOSE KNOBS and
re-asks the identification question.

Recon that motivated the design (printed again below as a census, not taken on faith):
**155 of the 170 unidentified files carry an explicit cost column, and the modal value set
is {10, 25} or {0, 10, 25} - i.e. most unidentified blocks contain rows priced at a rung
737's 10-bps-only library never offered.**

Tuned parameters (PROTOCOL rule 4: at most two).  Every grid point reported; nothing is
selected outside the rule-8 walk-forward.
    1. BLOCK SET - the census tier.  T0 all 369 unidentified CANON blocks; T1 those whose
       source script is on disk; T2 those whose own CSV carries an explicit cost/rung
       column.  Every tier's counts published.
    2. COMPARAND SOURCE - a cumulative REBUILD LADDER, five levels, every level published:
       L0  737's library verbatim: 5 candidates at 10 bps / W / gross 0.75 / px.index[260].
           Identified = 0 by construction; this is the control.
       L1  + the ROW'S OWN COST RUNG, read from the block's own cost/bps/cost_bps/rung
           column (exact, by cost linearity: r(c) = r(0) - turnover * c / 1e4).
       L2  + the SCRIPT'S OWN WINDOW (px.index[260] | the panel's first SPY day | the
           panel's own first priced day), read from the script text.
       L3  + the COMPARAND'S OWN GROSS ladder {0.50, 0.75, 1.00} for the v2 forms.
       L4  + the COMPARAND'S OWN CADENCE {W, M, Q}.

A block is IDENTIFIED at level L iff at least one candidate available at that level
reproduces its published 4a column on EVERY row of the block (match rate exactly 1.0).
Identification is EMPIRICAL - by reproduction, never by reading a code comment.

4a is the record's own predicate, verbatim from `baseline.compare()`:
    H1 > base.H1  AND  H2 > base.H2  AND  MaxDD >= base.MaxDD
4b is scored against SPY on the same panel and window:
    H1 > spy.H1 AND H2 > spy.H2 AND oSharpe > spy.oSharpe
    AND MaxDD >= -0.60*|spy.MaxDD| AND CAGR >= 0.70*spy.CAGR

Pre-registered gates, written before any identification count was read
----------------------------------------------------------------------
G1  COST LINEARITY.  The whole L1 rung is derived, not re-simulated, so the derivation must
    be exact: for probe cells, |r(c) - (r(0) - turnover*c/1e4)| < 1e-12.
G2  737 REPRODUCTION.  This run's comparand library must restate 737's committed
    `.comparands.csv` to < 1e-9 on Sharpe/CAGR/MaxDD/H1/H2 for all 20 (panel x convention)
    cells, AND the L0 re-adjudication must reproduce 737's committed `identified` column on
    all 1,018 CANON blocks.
G3  CONTROL IS EMPTY.  L0 must identify 0 of the 369 unidentified blocks (it is 737's own
    library, so anything else means the census is not being replayed faithfully).
G4  LADDER MONOTONICITY.  The ladder is cumulative, so identified(L0) <= identified(L1)
    <= ... <= identified(L4) must hold on both blocks and rows.
B1  IS THE UNIDENTIFIED HALF REBUILDABLE AT ALL?  PASS iff L4 identifies >= 1 block.
    A FAIL would mean the record's unidentified half quotes something no knob setting of
    the PROTOCOL comparand reaches, and the 4a column there is unreconstructible.
B2  WHICH KNOB DOES THE WORK?  No bar - the per-level increment is the answer, reported as
    blocks and rows gained at each rung.
B3  DOES IDENTIFICATION CHANGE THE PUBLISHED VERDICTS?  For every newly identified block,
    the published 4a column is by definition reproduced, so nothing is restated; what IS
    reported is how far the published rate sits from the canonical 10-bps bar - the size of
    the error 737's library would have made had it assigned those rows anyway.

RULE 8 (mandatory).  A fresh dial grid - the record's BAND book on 3 panels x gross ladder
x cadence ladder - has its (gross, cadence) chosen on IS <= 2016-12-31 ALONE and 2017-01-01+
read ONCE.  Each pick's 4a is then scored under the CANONICAL comparand (10 bps, W, 0.75,
idx260) and under the comparand rebuilt at the ARM'S OWN cost rung and cadence, and 4b is
scored once.  This asks whether the comparand-source convention changes a FRESH decision,
not just a retrospective census.

CAVEATS.  (i) SURVIVORSHIP (idea 54): U56, B136, SMALL439 and SMALL484 are all
current-constituent panels with no delistings, so every CAGR LEVEL is inflated and both
KEEP columns inherit that whole.  SMALL439/484 are the sub-$2B screen; SMALL439 drops the
44 names with max_1d_move >= 1.0 per PROTOCOL.  (ii) Identification by reproduction is
necessary, not sufficient: a block whose published column happens to agree with a candidate
on every row is called identified even if its script computed something else that agrees
everywhere.  The count is therefore an UPPER bound on true identification and is reported
as such.  (iii) A block identified by SEVERAL candidates is identified but not resolved;
uniquely-identified counts are published beside the totals.  (iv) One corpus read five ways
is not five independent pieces of evidence.
"""
import sys, glob, json, time, re
from pathlib import Path
import numpy as np, pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights      # noqa
from engine import metrics, rebalance_mask                                  # noqa

OUT = Path(__file__).with_suffix("")
BT = REPO / "research" / "backtests"
REF737 = BT / ("2026-09-11_should-PROTOCOL-rule-3-state-that-the-4a-COMPARAND-runs-on-"
               "the-IDEA-S-OWN-PANEL_C")
IS_END, OOS_START = "2016-12-31", "2017-01-01"
CANON_COST, CANON_CAD, CANON_GROSS, CANON_WIN = 10.0, "W", 0.75, "IDX260"
CONVENTIONS = ["SAMEv2", "SAMEv2_noSPY", "CROSSv2", "SAMEv1", "CROSSv1"]
COST_COLS = ["cost", "bps", "cost_bps", "rung", "cost_rung"]
CAD_COLS = ["cad", "freq", "cadence", "rebal"]
A4_COLS = ["pass4a", "p4a", "f4a", "pass_4a", "keep4a", "fail4a"]
A4_NEG = {"f4a", "fail4a"}
PANEL_MAP = {
    "u56": "U56", "U56": "U56", "MAIN": "U56", "U55": "U56",
    "broad": "B136", "B136": "B136", "BROAD136": "B136", "broad136": "B136", "BROAD": "B136",
    "SMALL439": "SMALL439", "small439": "SMALL439",
    "small": "SMALL484", "SMALL": "SMALL484", "SMALL484": "SMALL484",
}
GROSS_LADDER = [0.50, 0.75, 1.00]
CAD_LADDER = ["W", "M", "Q"]
WIN_LADDER = ["IDX260", "SPY0", "PX0"]
TOL_LIN, TOL_REPRO = 1e-12, 1e-9

LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)
def flush_log():
    OUT.with_suffix(".console.txt").write_text("\n".join(LOG) + "\n")


# ------------------------------------------------------------------ machinery (record's own)
def fast_backtest(prices, weights, cost_bps=0.0, freq="W"):
    """numpy re-implementation of engine.backtest; returns (net returns, turnover)."""
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(prices.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(prices.index, freq).shift(1, fill_value=False).values
    n = len(prices.index)
    cur = np.zeros(prices.shape[1]); turn = np.zeros(n); pr = np.empty(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        pr[i] = float(cur @ rets[i])
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    idx = prices.index
    return (pd.Series(pr - turn * cost_bps / 1e4, index=idx), pd.Series(turn, index=idx))


def stat(r):
    h = len(r) // 2
    m, mo = metrics(r), metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                isSharpe=metrics(r.loc[:IS_END])["Sharpe"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])


def live_mask(px): return px.notna() & px.shift(1).notna()


def band_book(px, band=0.03, gross=0.75):
    """RULES v2's book at an arbitrary gross - baseline.rules_v2_weights generalised."""
    return rules_v2_weights(px, band=band, gross=gross)


def pass4a(H1, H2, DD, b):
    return (H1 > b["H1"]) & (H2 > b["H2"]) & (DD >= b["MaxDD"])


def pass4b(CAGR, H1, H2, DD, oS, spy):
    return bool(H1 > spy["H1"] and H2 > spy["H2"] and oS > spy["oSharpe"]
                and DD >= -0.60 * abs(spy["MaxDD"]) and CAGR >= 0.70 * spy["CAGR"])


# ------------------------------------------------------------------ panels
def build_panels():
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv439 = [c for c in pxs.columns if c != "SPY" and c not in bad]
    inv484 = [c for c in pxs.columns if c != "SPY"]
    px56, px136 = load_universe(), load_universe(broad=True)
    out = {
        "U56":      (px56[[c for c in px56.columns if c != "SPY"]],   px56["SPY"]),
        "B136":     (px136[[c for c in px136.columns if c != "SPY"]], px136["SPY"]),
        "SMALL439": (pxs[inv439], pxs["SPY"]),
        "SMALL484": (pxs[inv484], pxs["SPY"]),
    }
    P(f"panels: U56 {out['U56'][0].shape[1]} names, B136 {out['B136'][0].shape[1]}, "
      f"SMALL439 {out['SMALL439'][0].shape[1]} ({len(bad)} dropped for max_1d_move >= 1.0), "
      f"SMALL484 {out['SMALL484'][0].shape[1]}")
    return out


# ------------------------------------------------------------------ comparand cache
class Library:
    """Lazily-built comparand cache.

    key  = (panel, version, spy_in, cadence, gross, cross)
    value = (gross-of-cost return series, turnover series) on the panel's full index.
    Any (cost, window) is then derived EXACTLY: r(c) = r(0) - turnover*c/1e4, sliced.
    """
    def __init__(self, panels):
        self.PN = panels
        self.raw = {}
        self.stats = {}
        self.n_sims = 0
        self.u56_px = load_universe()          # U56 WITH SPY, exactly as load_universe returns

    def _frame(self, panel, spy_in):
        px, spy = self.PN[panel]
        return px.join(spy.rename("SPY")) if spy_in else px

    def series(self, panel, version, spy_in, cad, gross, cross):
        k = (panel, version, spy_in, cad, gross, cross)
        if k in self.raw: return self.raw[k]
        if cross:                                     # built on U56, reindexed onto the panel
            pu = self.u56_px
            w = band_book(pu, gross=gross) if version == "v2" else rules_v1_weights(pu)
            r, t = fast_backtest(pu, w, 0.0, cad)
            idx = self.PN[panel][0].index
            r, t = r.reindex(idx).fillna(0.0), t.reindex(idx).fillna(0.0)
        else:
            f = self._frame(panel, spy_in)
            w = band_book(f, gross=gross) if version == "v2" else rules_v1_weights(f)
            r, t = fast_backtest(f, w, 0.0, cad)
        self.n_sims += 1
        self.raw[k] = (r, t)
        return self.raw[k]

    def start(self, panel, win):
        px, spy = self.PN[panel]
        if win == "IDX260": return px.index[260]
        if win == "SPY0":   return spy.dropna().index[0]
        return px.index[0]

    def get(self, panel, version, spy_in, cad, gross, cross, cost, win):
        k = (panel, version, spy_in, cad, gross, cross, round(float(cost), 6), win)
        if k in self.stats: return self.stats[k]
        r0, t = self.series(panel, version, spy_in, cad, gross, cross)
        s = self.start(panel, win)
        net = (r0 - t * float(cost) / 1e4).loc[s:]
        self.stats[k] = stat(net)
        return self.stats[k]

    def spy(self, panel, win):
        k = ("SPY", panel, win)
        if k in self.stats: return self.stats[k]
        px, spy = self.PN[panel]
        self.stats[k] = stat(spy.pct_change().fillna(0.0).loc[self.start(panel, win):])
        return self.stats[k]


def conv_spec(cv, gross, cad, win):
    """(version, spy_in, cross) for each of 737's five convention NAMES, at given knobs."""
    return {
        "SAMEv2":       ("v2", True,  False),
        "SAMEv2_noSPY": ("v2", False, False),
        "CROSSv2":      ("v2", True,  True),
        "SAMEv1":       ("v1", True,  False),
        "CROSSv1":      ("v1", True,  True),
    }[cv]


# ------------------------------------------------------------------ block scanning
def script_for(fname):
    """research/backtests/<stem>.py for a committed artefact filename, or None."""
    s = fname
    for suf in (".csv.gz", ".csv"):
        if s.endswith(suf): s = s[: -len(suf)]
    p = BT / (s.split(".")[0] + ".py")
    return p if p.exists() else None


def window_of(script_path):
    """Which evaluation window does the script declare?  IDX260 unless it says otherwise."""
    if script_path is None: return CANON_WIN, "no-script"
    t = script_path.read_text(errors="ignore")
    if "spy.index[0]" in t or "spy.dropna().index[0]" in t: return "SPY0", "spy.index[0]"
    if "index[260]" in t: return "IDX260", "index[260]"
    return CANON_WIN, "default"


def gross_of(script_path):
    if script_path is None: return None
    m = re.search(r"^GROSS\s*=\s*([0-9.]+)", script_path.read_text(errors="ignore"), re.M)
    return float(m.group(1)) if m else None


def read_block_rows(fname, panel_label):
    """The published rows of one block, with their own cost rung and cadence where declared."""
    df = pd.read_csv(BT / fname)
    df["panel"] = df["panel"].astype(str)
    sub = df[df["panel"] == panel_label]
    cols = set(df.columns)
    a4 = next((c for c in A4_COLS if c in cols), None)
    pub = sub[a4].astype(str).str.strip().str.lower().map(
        {"true": True, "false": False, "1": True, "0": False, "1.0": True, "0.0": False})
    if a4 in A4_NEG: pub = ~pub.astype("boolean")
    cc = next((c for c in COST_COLS if c in cols), None)
    if cc is None:
        cost = np.full(len(sub), CANON_COST)
    else:
        cost = pd.to_numeric(sub[cc], errors="coerce").values.astype(float)
        if np.nanmax(np.abs(cost)) <= 1.0 and np.nanmax(np.abs(cost)) > 0:
            cost = cost * 1e4                       # a fraction, not bps
        cost = np.where(np.isfinite(cost), cost, CANON_COST)
    dc = next((c for c in CAD_COLS if c in cols), None)
    cad = (sub[dc].astype(str).str.strip().str.upper().str[0].values if dc is not None
           else np.full(len(sub), CANON_CAD))
    cad = np.array([c if c in CAD_LADDER else CANON_CAD for c in cad])
    return sub, pub.values, cost, cad, a4, cc, dc


def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 739  which of the 188,541 UNIDENTIFIED 4a rows quote a comparand that can be "
      "REBUILT AT ALL")
    P("cloud lane, 2026-09-11.  next-day execution (engine convention), 4a and 4b verbatim "
      "from baseline.compare().")
    P("two tuned parameters: BLOCK SET (3 census tiers) x COMPARAND SOURCE (5-level rebuild "
      "ladder).  every grid point published; selection only inside the rule-8 walk-forward.")
    P("=" * 100)
    P("pre-registered gates:")
    P(f"  G1 COST LINEARITY   |r(c) - (r(0) - turnover*c/1e4)| < {TOL_LIN} on probe cells")
    P(f"  G2 737 REPRODUCTION comparand library to < {TOL_REPRO} on 20 cells; L0 restates "
      "737's `identified` column on all 1,018 CANON blocks")
    P("  G3 CONTROL EMPTY    L0 identifies 0 of the 369 unidentified blocks")
    P("  G4 MONOTONE         identified(L0) <= L1 <= L2 <= L3 <= L4 on blocks AND rows")
    P("  B1 REBUILDABLE?     PASS iff L4 identifies >= 1 of the 369 blocks")
    P("  B2 WHICH KNOB       no bar - the per-rung increment IS the answer")
    P("  B3 CONSEQUENCE      published-rate vs canonical-bar distance on newly identified blocks")
    flush_log()

    PN = build_panels()
    LIB = Library(PN)

    # ---------------------------------------------------------------- G1 cost linearity
    P("\n" + "=" * 100)
    P("G1 COST LINEARITY (the whole L1 rung is DERIVED, so the derivation is gated first)")
    P("=" * 100)
    g1_max = 0.0
    for pname in ["U56", "B136", "SMALL439"]:
        for cad in ["W", "M"]:
            px, spy = PN[pname]
            f = px.join(spy.rename("SPY"))
            w = band_book(f, gross=0.75)
            r0, t = fast_backtest(f, w, 0.0, cad)
            for c in (10.0, 25.0, 50.0):
                direct, _ = fast_backtest(f, w, c, cad)
                d = float(np.max(np.abs(direct.values - (r0 - t * c / 1e4).values)))
                g1_max = max(g1_max, d)
            P(f"  {pname:9} cad {cad}  max |direct - derived| over c in (10,25,50): {g1_max:.3e}")
    G1 = g1_max < TOL_LIN
    P(f"  G1: max {g1_max:.3e} vs bar {TOL_LIN} -> {'PASS' if G1 else 'FAIL'}")
    flush_log()

    # ---------------------------------------------------------------- G2a comparand library
    P("\n" + "=" * 100)
    P("G2a COMPARAND LIBRARY at the CANONICAL point (10 bps, W, gross 0.75, px.index[260])")
    P("    restated against idea 737's committed .comparands.csv")
    P("=" * 100)
    ref = pd.read_csv(str(REF737) + ".comparands.csv")
    g2a_max, crows = 0.0, []
    P(f"  {'panel':9} {'convention':14} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>9} {'H1':>8} "
      f"{'H2':>8} {'oSharpe':>8} {'max|d| vs 737':>14}")
    for pname in PN:
        for cv in CONVENTIONS:
            ver, spy_in, cross = conv_spec(cv, CANON_GROSS, CANON_CAD, CANON_WIN)
            c = LIB.get(pname, ver, spy_in, CANON_CAD, CANON_GROSS, cross, CANON_COST, CANON_WIN)
            rr = ref[(ref.panel == pname) & (ref.convention == cv)]
            d = (max(abs(c[k] - float(rr[k].iloc[0])) for k in
                     ["CAGR", "Sharpe", "MaxDD", "H1", "H2"]) if len(rr) else np.nan)
            g2a_max = max(g2a_max, d if np.isfinite(d) else 0.0)
            P(f"  {pname:9} {cv:14} {c['CAGR']:8.4f} {c['Sharpe']:8.4f} {c['MaxDD']:9.4f} "
              f"{c['H1']:8.4f} {c['H2']:8.4f} {c['oSharpe']:8.4f} {d:14.3e}")
            crows.append(dict(panel=pname, convention=cv, **c, d_vs_737=d))
    pd.DataFrame(crows).to_csv(OUT.with_suffix(".comparands.csv"), index=False)
    g2a = g2a_max < TOL_REPRO
    P(f"  G2a: max |d| {g2a_max:.3e} vs bar {TOL_REPRO} -> {'PASS' if g2a else 'FAIL'}")
    flush_log()

    # ---------------------------------------------------------------- the block set
    P("\n" + "=" * 100)
    P("THE BLOCK SET (param 1): idea 737's CANON census, replayed")
    P("=" * 100)
    C737 = pd.read_csv(str(REF737) + ".census.csv")
    mapped = C737[C737.mapped == True].copy()                                 # noqa: E712
    mapped["identified"] = mapped["identified"].fillna("")
    unid = mapped[mapped.identified == ""].copy()
    P(f"  737 CANON blocks {len(mapped)} / {int(mapped.n.sum())} rows; "
      f"IDENTIFIED {int((mapped.identified != '').sum())} blocks / "
      f"{int(mapped[mapped.identified != ''].n.sum())} rows")
    P(f"  T0 UNIDENTIFIED blocks {len(unid)} / {int(unid.n.sum())} rows "
      f"({unid.n.sum()/mapped.n.sum():.1%} of CANON) over {unid.file.nunique()} files")
    for p, g in unid.groupby("canon"):
        P(f"     {p:9} {len(g):4d} blocks {int(g.n.sum()):7d} rows")
    flush_log()

    # per-block knob parse (tiers T1, T2)
    blocks, PAY = [], {}
    for _, r in unid.iterrows():
        sp = script_for(r.file)
        win, win_src = window_of(sp)
        try:
            sub, pub, cost, cad, a4, cc, dc = read_block_rows(r.file, r.panel_label)
        except Exception as e:
            blocks.append(dict(file=r.file, panel_label=r.panel_label, canon=r.canon,
                               n=int(r.n), readable=False, err=str(e)[:80]))
            continue
        ok = bool(pd.notna(pub).all()) and len(sub) == int(r.n)
        PAY[(r.file, r.panel_label)] = (sub, pub, cost, cad)
        blocks.append(dict(file=r.file, panel_label=r.panel_label, canon=r.canon, n=int(r.n),
                           readable=ok, has_script=sp is not None, win=win, win_src=win_src,
                           script_gross=gross_of(sp), a4col=a4, cost_col=cc or "", cad_col=dc or "",
                           n_cost_rungs=int(len(set(np.round(cost, 4)))),
                           cost_rungs="|".join(str(x) for x in sorted(set(np.round(cost, 4)))[:6]),
                           n_cad=int(len(set(cad))),
                           pub_rate=float(np.mean(pub.astype(float))) if ok else np.nan))
    B = pd.DataFrame(blocks)
    T1 = B[(B.readable == True) & (B.has_script == True)]                      # noqa: E712
    T2 = T1[T1.cost_col != ""]
    P(f"\n  T1 (script on disk AND rows readable): {len(T1)} blocks / {int(T1.n.sum())} rows")
    P(f"  T2 (T1 AND an explicit cost/rung column): {len(T2)} blocks / {int(T2.n.sum())} rows")
    P(f"  window declared: " + ", ".join(f"{k} {v}" for k, v in
                                         T1.win_src.value_counts().items()))
    P(f"  blocks whose rows span >1 cost rung: {int((T1.n_cost_rungs > 1).sum())} "
      f"({int(T1[T1.n_cost_rungs > 1].n.sum())} rows); >1 cadence: "
      f"{int((T1.n_cad > 1).sum())}")
    P("  cost-rung sets present (top 10): " +
      ", ".join(f"[{k}] x{v}" for k, v in T1.cost_rungs.value_counts().head(10).items()))
    flush_log()

    # ---------------------------------------------------------------- G2b: L0 replays 737
    P("\n" + "=" * 100)
    P("G2b L0 CONTROL - 737's library replayed on ALL 1,018 CANON blocks")
    P("=" * 100)
    def adjudicate(sub_pub, H1, H2, DD, cost, cad, panel, cv, gross, win, per_row):
        """Predicted 4a for a block's rows under one candidate.  per_row=True uses each
        row's own (cost, cadence); otherwise the canonical point."""
        ver, spy_in, cross = conv_spec(cv, gross, cad, win)
        if not per_row:
            b = LIB.get(panel, ver, spy_in, CANON_CAD, gross, cross, CANON_COST, win)
            return pass4a(H1, H2, DD, b)
        out = np.empty(len(H1), dtype=bool)
        for key in set(zip(np.round(cost, 6), cad)):
            c, cd = key
            m = (np.round(cost, 6) == c) & (cad == cd)
            b = LIB.get(panel, ver, spy_in, cd, gross, cross, c, win)
            out[m] = pass4a(H1[m], H2[m], DD[m], b)
        return out

    l0_ident, n_chk = {}, 0
    for _, r in mapped.iterrows():
        try:
            sub, pub, cost, cad, a4, cc, dc = read_block_rows(r.file, r.panel_label)
        except Exception:
            continue
        if not pd.notna(pub).all(): continue
        H1, H2, DD = sub.H1.values, sub.H2.values, sub.MaxDD.values
        hits = [cv for cv in CONVENTIONS
                if bool(np.all(adjudicate(None, H1, H2, DD, None, None, r.canon, cv,
                                          CANON_GROSS, CANON_WIN, False) == pub))]
        l0_ident[(r.file, r.panel_label)] = "|".join(hits)
        n_chk += 1
    agree = sum(1 for _, r in mapped.iterrows()
                if l0_ident.get((r.file, r.panel_label)) == r.identified)
    g2b = agree == n_chk and n_chk > 0
    P(f"  blocks re-adjudicated: {n_chk} of {len(mapped)} ({len(mapped)-n_chk} skipped - their "
      f"published 4a column carries values this run's boolean map leaves NaN, so they cannot be "
      f"scored either way and are counted nowhere); `identified` column reproduced exactly on "
      f"{agree} -> G2b {'PASS' if g2b else 'FAIL'}")
    G2 = g2a and g2b
    P(f"  G2 OVERALL: {'PASS' if G2 else 'FAIL'}")
    flush_log()

    # ---------------------------------------------------------------- THE LADDER (param 2)
    P("\n" + "=" * 100)
    P("THE REBUILD LADDER (param 2): 5 cumulative levels on the T1 block set")
    P("  L0 737's library (10 bps / W / g0.75 / idx260)   L1 + own COST RUNG")
    P("  L2 + own WINDOW   L3 + own GROSS ladder   L4 + own CADENCE ladder")
    P("=" * 100)
    LEVELS = ["L0", "L1", "L2", "L3", "L4"]
    def candidates(level, blk):
        """(cv, gross, win, per_row_cost_cad) tuples available at each ladder level."""
        wins = [CANON_WIN]
        grosses = [CANON_GROSS]
        per_row = False
        if level in ("L1", "L2", "L3", "L4"): per_row = True
        if level in ("L2", "L3", "L4"): wins = [CANON_WIN, blk.win] if blk.win != CANON_WIN else [CANON_WIN]
        if level in ("L3", "L4"):
            grosses = sorted(set(GROSS_LADDER + ([blk.script_gross] if blk.script_gross else [])))
        out = []
        for cv in CONVENTIONS:
            gl = grosses if cv in ("SAMEv2", "SAMEv2_noSPY", "CROSSv2") else [CANON_GROSS]
            for g in gl:
                for w in wins:
                    out.append((cv, g, w, per_row))
        return out

    recs = []
    for i, blk in enumerate(T1.itertuples()):
        sub, pub, cost, cad = PAY[(blk.file, blk.panel_label)]
        H1, H2, DD = sub.H1.values, sub.H2.values, sub.MaxDD.values
        rec = dict(file=blk.file, panel_label=blk.panel_label, canon=blk.canon, n=blk.n,
                   win=blk.win, cost_rungs=blk.cost_rungs, pub_rate=blk.pub_rate,
                   degenerate=bool(pd.Series(pub).nunique() == 1))
        found_at, hits_at = None, {}
        for lvl in LEVELS:
            # cadence candidates: canonical W always, the block's own cadence vector added at L4.
            # ADDITIVE, never a replacement, so the ladder stays cumulative (G4).
            cads = [np.full(len(cad), CANON_CAD)]
            if lvl == "L4" and not np.all(cad == CANON_CAD): cads.append(cad)
            hits = []
            for (cv, g, w, per_row) in candidates(lvl, blk):
              for ci, cad_use in enumerate(cads):
                pred = adjudicate(None, H1, H2, DD,
                                  cost if per_row else None,
                                  cad_use if per_row else None,
                                  blk.canon, cv, g, w, per_row)
                if bool(np.all(pred == pub)):
                    hits.append(f"{cv}@g{g:.2f}@{w}" + ("@owncad" if ci else ""))
            hits_at[lvl] = hits
            rec[f"ident_{lvl}"] = "|".join(hits[:4])
            rec[f"nhit_{lvl}"] = len(hits)
            if hits and found_at is None: found_at = lvl
        rec["first_level"] = found_at or ""
        # how far the published rate sits from the canonical bar (B3)
        bcan = LIB.get(blk.canon, "v2", True, CANON_CAD, CANON_GROSS, False, CANON_COST, CANON_WIN)
        rec["rate_canonical"] = float(np.mean(pass4a(H1, H2, DD, bcan)))
        recs.append(rec)
        if (i + 1) % 40 == 0:
            P(f"    ... {i+1}/{len(T1)} blocks, {LIB.n_sims} comparand simulations, "
              f"{time.time()-t0:.0f}s")
            flush_log()
    R = pd.DataFrame(recs)
    R.to_csv(OUT.with_suffix(".ladder.csv"), index=False)

    P("\n  A block's published 4a column is DEGENERATE if it is constant (all-PASS or all-FAIL):"
      "\n  any comparand strict enough (or loose enough) reproduces it, so a degenerate match is"
      "\n  weak evidence.  The NON-DEGENERATE column is the load-bearing reading and is published"
      "\n  beside the total throughout.")
    P(f"  of the {len(R)} T1 blocks, {int(R.degenerate.sum())} are degenerate "
      f"({int(R[R.degenerate].n.sum())} rows) and {int((~R.degenerate).sum())} are not "
      f"({int(R[~R.degenerate].n.sum())} rows)")
    P(f"\n  {'level':6} {'blocks ident':>13} {'rows ident':>11} {'blocks +':>9} {'rows +':>8} "
      f"{'uniquely':>9} {'NON-DEGEN blk':>14} {'NON-DEGEN rows':>15}")
    cum_b, cum_r, mono = 0, 0, True
    ladder_rows = []
    for lvl in LEVELS:
        hit = R[R[f"nhit_{lvl}"] > 0]
        nb, nr = len(hit), int(hit.n.sum())
        uq = int((R[f"nhit_{lvl}"] == 1).sum())
        nd = hit[~hit.degenerate]
        if nb < cum_b or nr < cum_r: mono = False
        P(f"  {lvl:6} {nb:13d} {nr:11d} {nb-cum_b:9d} {nr-cum_r:8d} {uq:9d} {len(nd):14d} "
          f"{int(nd.n.sum()):15d}")
        ladder_rows.append(dict(level=lvl, blocks=nb, rows=nr, blocks_gained=nb - cum_b,
                                rows_gained=nr - cum_r, uniquely=uq,
                                blocks_nondegen=len(nd), rows_nondegen=int(nd.n.sum())))
        cum_b, cum_r = nb, nr
    pd.DataFrame(ladder_rows).to_csv(OUT.with_suffix(".levels.csv"), index=False)
    G3 = int((R.nhit_L0 > 0).sum()) == 0
    G4 = mono
    B1 = int((R.nhit_L4 > 0).sum()) >= 1
    P(f"  G3 CONTROL EMPTY: L0 identifies {int((R.nhit_L0>0).sum())} -> "
      f"{'PASS' if G3 else 'FAIL'}")
    P(f"  G4 MONOTONE: {'PASS' if G4 else 'FAIL'}")
    P(f"  B1 REBUILDABLE: L4 identifies {int((R.nhit_L4>0).sum())} of {len(R)} blocks -> "
      f"{'PASS' if B1 else 'FAIL'}")
    flush_log()

    P("\n  B2 WHICH KNOB DOES THE WORK (blocks first identified at each rung, by panel):")
    P(f"  {'panel':9} " + " ".join(f"{l:>7}" for l in LEVELS) + f" {'never':>7} {'total':>7}")
    for p, g in R.groupby("canon"):
        vc = g.first_level.value_counts()
        P(f"  {p:9} " + " ".join(f"{int(vc.get(l,0)):7d}" for l in LEVELS) +
          f" {int((g.first_level=='').sum()):7d} {len(g):7d}")
    vc = R.first_level.value_counts()
    P(f"  {'ALL':9} " + " ".join(f"{int(vc.get(l,0)):7d}" for l in LEVELS) +
      f" {int((R.first_level=='').sum()):7d} {len(R):7d}")
    P("  rows, same cut: " + ", ".join(
        f"{l} {int(R[R.first_level==l].n.sum())}" for l in LEVELS) +
      f", never {int(R[R.first_level=='']. n.sum())}")
    ND = R[~R.degenerate]
    vcn = ND.first_level.value_counts()
    P(f"  {'NON-DEGEN':9} " + " ".join(f"{int(vcn.get(l,0)):7d}" for l in LEVELS) +
      f" {int((ND.first_level=='').sum()):7d} {len(ND):7d}"
      f"   <- the load-bearing count")
    P("  NON-DEGEN rows, same cut: " + ", ".join(
        f"{l} {int(ND[ND.first_level==l].n.sum())}" for l in LEVELS) +
      f", never {int(ND[ND.first_level==''].n.sum())}")
    # which convention name carries the identified blocks
    cn = {}
    for s in R[R.first_level != ""].apply(lambda r: r[f"ident_{r.first_level}"], axis=1):
        for h in str(s).split("|"):
            if h: cn[h.split("@")[0]] = cn.get(h.split("@")[0], 0) + 1
    P("  convention name of the identifying candidate (a block may match several): " +
      ", ".join(f"{k} {v}" for k, v in sorted(cn.items(), key=lambda kv: -kv[1])))
    flush_log()

    P("\n  B3 CONSEQUENCE - on the newly identified blocks, how far the published 4a rate sits")
    P("     from the CANONICAL (10 bps / W / g0.75 / idx260) bar that 737 would have applied:")
    new = R[R.first_level.isin(["L1", "L2", "L3", "L4"])]
    if len(new):
        d = (new.pub_rate - new.rate_canonical).abs()
        P(f"     {len(new)} blocks / {int(new.n.sum())} rows;  |published rate - canonical "
          f"rate|  mean {d.mean():.4f}  median {d.median():.4f}  max {d.max():.4f}")
        P(f"     rows the canonical bar would have MIS-ADJUDICATED (rate difference x n): "
          f"~{int((d * new.n).sum())}")
        P("     the 10 largest, by rows:")
        for _, r in new.nlargest(10, "n").iterrows():
            P(f"       {r.file[:70]:70} {r.panel_label:9} n {int(r.n):6d} rungs [{r.cost_rungs}] "
              f"pub {r.pub_rate:.4f} canon {r.rate_canonical:.4f} -> {r.first_level} "
              f"{r[f'ident_{r.first_level}'][:40]}")
    still = R[R.first_level == ""]
    P(f"\n     STILL UNIDENTIFIED after L4: {len(still)} blocks / {int(still.n.sum())} rows "
      f"({still.n.sum()/max(int(R.n.sum()),1):.1%} of the T1 set) - these quote a comparand no "
      f"knob setting of the PROTOCOL book reaches.")
    if len(still):
        P("     the 8 largest:")
        for _, r in still.nlargest(8, "n").iterrows():
            P(f"       {r.file[:70]:70} {r.panel_label:9} n {int(r.n):6d} rungs [{r.cost_rungs}] "
              f"pub {r.pub_rate:.4f} canon {r.rate_canonical:.4f}")
    flush_log()

    # ---------------------------------------------------------------- RULE 8 WALK-FORWARD
    P("\n" + "=" * 100)
    P("RULE 8 WALK-FORWARD - does the comparand SOURCE change a FRESH 4a decision?")
    P("  fresh dial grid: BAND book, 3 panels x gross {0.50,0.75,1.00} x cadence {W,M,Q} x")
    P("  cost rung {10,25} = 54 arms, ALL REPORTED.  (gross, cadence) chosen on IS <= "
      f"{IS_END} ALONE by IS Sharpe; {OOS_START}+ read ONCE.")
    P("=" * 100)
    arms = []
    for pname in ["U56", "B136", "SMALL439"]:
        px, spy = PN[pname]
        f = px.join(spy.rename("SPY"))
        s0 = px.index[260]
        for g in GROSS_LADDER:
            for cad in CAD_LADDER:
                r0, t = fast_backtest(f, band_book(f, gross=g), 0.0, cad)
                yrs = len(r0.loc[s0:]) / 252
                for c in (10.0, 25.0):
                    net = (r0 - t * c / 1e4).loc[s0:]
                    arms.append(dict(panel=pname, gross=g, cad=cad, cost=c,
                                     turn_yr=float(t.loc[s0:].sum() / yrs), **stat(net)))
    A = pd.DataFrame(arms)
    P(f"  {'panel':9} {'g':>5} {'cad':>4} {'c':>5} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} "
      f"{'H1':>7} {'H2':>7} {'isS':>7} {'oCAGR':>8} {'oSharpe':>8} {'oMaxDD':>8} "
      f"{'4a canon':>9} {'4a own':>7} {'4b':>5}")
    for r in A.itertuples():
        b_can = LIB.get(r.panel, "v2", True, CANON_CAD, CANON_GROSS, False, CANON_COST, CANON_WIN)
        b_own = LIB.get(r.panel, "v2", True, r.cad, CANON_GROSS, False, r.cost, CANON_WIN)
        sp = LIB.spy(r.panel, CANON_WIN)
        A.loc[r.Index, "p4a_canon"] = bool(pass4a(r.H1, r.H2, r.MaxDD, b_can))
        A.loc[r.Index, "p4a_own"] = bool(pass4a(r.H1, r.H2, r.MaxDD, b_own))
        A.loc[r.Index, "p4b"] = pass4b(r.CAGR, r.H1, r.H2, r.MaxDD, r.oSharpe, sp)
        P(f"  {r.panel:9} {r.gross:5.2f} {r.cad:>4} {r.cost:5.0f} {r.CAGR:8.4f} {r.Sharpe:8.4f} "
          f"{r.MaxDD:8.4f} {r.H1:7.4f} {r.H2:7.4f} {r.isSharpe:7.4f} {r.oCAGR:8.4f} "
          f"{r.oSharpe:8.4f} {r.oMaxDD:8.4f} {str(A.loc[r.Index,'p4a_canon']):>9} "
          f"{str(A.loc[r.Index,'p4a_own']):>7} {str(A.loc[r.Index,'p4b']):>5}")
    A.to_csv(OUT.with_suffix(".arms.csv"), index=False)
    flush_log()

    P("\n  the picks (IS Sharpe argmax over gross x cadence, per panel x cost rung):")
    P(f"  {'panel':9} {'c':>5} {'pick':>12} {'isS':>7} | {'oCAGR':>8} {'oSharpe':>8} "
      f"{'oMaxDD':>8} | {'4a canon':>9} {'4a own':>7} {'4b':>5} | {'v2 canon oS':>11} "
      f"{'v2 own oS':>10} {'SPY oS':>7}")
    wf = []
    for pname in ["U56", "B136", "SMALL439"]:
        for c in (10.0, 25.0):
            sub = A[(A.panel == pname) & (A.cost == c)]
            pk = sub.loc[sub.isSharpe.idxmax()]
            b_can = LIB.get(pname, "v2", True, CANON_CAD, CANON_GROSS, False, CANON_COST, CANON_WIN)
            b_own = LIB.get(pname, "v2", True, pk.cad, CANON_GROSS, False, c, CANON_WIN)
            sp = LIB.spy(pname, CANON_WIN)
            P(f"  {pname:9} {c:5.0f} {f'g{pk.gross:.2f} {pk.cad}':>12} {pk.isSharpe:7.4f} | "
              f"{pk.oCAGR:8.4f} {pk.oSharpe:8.4f} {pk.oMaxDD:8.4f} | "
              f"{str(bool(pk.p4a_canon)):>9} {str(bool(pk.p4a_own)):>7} {str(bool(pk.p4b)):>5} | "
              f"{b_can['oSharpe']:11.4f} {b_own['oSharpe']:10.4f} {sp['oSharpe']:7.4f}")
            wf.append(dict(panel=pname, cost=c, gross=pk.gross, cad=pk.cad,
                           isSharpe=pk.isSharpe, CAGR=pk.CAGR, Sharpe=pk.Sharpe,
                           MaxDD=pk.MaxDD, H1=pk.H1, H2=pk.H2, oCAGR=pk.oCAGR,
                           oSharpe=pk.oSharpe, oMaxDD=pk.oMaxDD,
                           p4a_canon=bool(pk.p4a_canon), p4a_own=bool(pk.p4a_own),
                           p4b=bool(pk.p4b), comp_canon_oS=b_can["oSharpe"],
                           comp_own_oS=b_own["oSharpe"], spy_oS=sp["oSharpe"],
                           spy_CAGR=sp["CAGR"], spy_MaxDD=sp["MaxDD"],
                           beats_v2_oos=bool(pk.oSharpe > b_can["oSharpe"]),
                           beats_spy_oos=bool(pk.oSharpe > sp["oSharpe"])))
    W = pd.DataFrame(wf)
    W.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)
    n_can, n_own = int(W.p4a_canon.sum()), int(W.p4a_own.sum())
    P(f"\n  4a on the {len(W)} picks: CANONICAL comparand {n_can}/{len(W)}, OWN-RUNG comparand "
      f"{n_own}/{len(W)}  -> the comparand source "
      f"{'CHANGES' if n_can != n_own else 'does NOT change'} the fresh 4a decision")
    P(f"  4b on the picks: {int(W.p4b.sum())}/{len(W)};  beats RULES v2 OOS Sharpe "
      f"{int(W.beats_v2_oos.sum())}/{len(W)};  beats SPY OOS Sharpe "
      f"{int(W.beats_spy_oos.sum())}/{len(W)}")
    flush_log()

    P("\n" + "=" * 100)
    P("BOTH KEEP PATHS on the 54-arm fresh grid (all points already printed above)")
    P("=" * 100)
    P(f"  4a (canonical comparand): {int(A.p4a_canon.sum())}/{len(A)};  "
      f"4a (own-rung comparand): {int(A.p4a_own.sum())}/{len(A)}")
    P(f"  4b: {int(A.p4b.sum())}/{len(A)}  " + " ".join(
        f"{p}={int(A[A.panel==p].p4b.sum())}" for p in ["U56", "B136", "SMALL439"]))
    for p in ["U56", "B136", "SMALL439"]:
        sp = LIB.spy(p, CANON_WIN)
        best = A[A.panel == p].nlargest(1, "Sharpe").iloc[0]
        P(f"  {p:9} best-Sharpe arm g{best.gross:.2f} {best.cad} @{best.cost:.0f}bps "
          f"CAGR {best.CAGR:.2%} Sharpe {best.Sharpe:.4f} MaxDD {best.MaxDD:.2%} "
          f"(OOS {best.oCAGR:.2%}/{best.oSharpe:.4f}/{best.oMaxDD:.2%})  vs SPY "
          f"{sp['CAGR']:.2%}/{sp['Sharpe']:.4f}/{sp['MaxDD']:.2%}")
    P("  NO NEW KEEP-CANDIDATE IS CLAIMED: the 54-arm grid is the record's standing BAND "
      "family, re-priced here only as the rule-8 vehicle for the comparand-source question.")

    P("\nGATES: G1 %s | G2 %s | G3 %s | G4 %s | B1 %s" %
      tuple("PASS" if x else "FAIL" for x in (G1, G2, G3, G4, B1)))
    summ = dict(G1=G1, G2=G2, G2a=g2a, G2b=g2b, G3=G3, G4=G4, B1=B1,
                blocks_T0=len(unid), rows_T0=int(unid.n.sum()),
                blocks_T1=len(T1), rows_T1=int(T1.n.sum()),
                blocks_T2=len(T2), rows_T2=int(T2.n.sum()),
                ladder={l: dict(blocks=int((R[f"nhit_{l}"] > 0).sum()),
                                rows=int(R[R[f"nhit_{l}"] > 0].n.sum()),
                                blocks_nondegen=int(((R[f"nhit_{l}"] > 0) & ~R.degenerate).sum()),
                                rows_nondegen=int(R[(R[f"nhit_{l}"] > 0) & ~R.degenerate].n.sum()))
                         for l in LEVELS},
                first_level={l: int((R.first_level == l).sum()) for l in LEVELS},
                blocks_degenerate=int(R.degenerate.sum()),
                rows_degenerate=int(R[R.degenerate].n.sum()),
                blocks_never=int((R.first_level == "").sum()),
                rows_never=int(R[R.first_level == ""].n.sum()),
                blocks_never_nondegen=int(((R.first_level == "") & ~R.degenerate).sum()),
                rows_never_nondegen=int(R[(R.first_level == "") & ~R.degenerate].n.sum()),
                wf_4a_canon=n_can, wf_4a_own=n_own, wf_4b=int(W.p4b.sum()),
                wf_n=len(W), grid_4a_canon=int(A.p4a_canon.sum()),
                grid_4a_own=int(A.p4a_own.sum()), grid_4b=int(A.p4b.sum()), grid_n=len(A),
                comparand_sims=LIB.n_sims, runtime_s=round(time.time() - t0, 1))
    OUT.with_suffix(".summary.json").write_text(json.dumps(summ, indent=2, default=str))
    P(f"\nruntime {summ['runtime_s']}s, {LIB.n_sims} comparand simulations")
    flush_log()
    return summ


if __name__ == "__main__":
    main()
