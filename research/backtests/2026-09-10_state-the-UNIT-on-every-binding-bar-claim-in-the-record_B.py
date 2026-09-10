#!/usr/bin/env python3
"""IDEA 480 — state the UNIT on every binding-bar claim in the record.  (lane B, 2026-09-10)

PRE-REGISTERED QUESTION (QUEUE.md, written before any number in this file was read)
    Idea 253 found the closest-to-binding bar is CAGR in RAW units (67.2% of 25,028
    published 4b passes) but DD in PANEL-NOISE units (47.6%), the two argmins disagreeing
    on 26.1% of rows.  Re-read every published "the DD cap is what cuts" / "CAGR floor
    binds" claim (idea 150 first) under BOTH units and report which flip.
    Max 2 params (unit, panel).

WHAT IS ALREADY ANSWERED, AND WHAT IS NOT (idea 632, 2026-09-10, cloud)
    Idea 632 re-cut the record's binding-bar CELLS under RAW/SD/IQR/RANK/SENS and found
    44% of claims do not survive.  It got 58 prose sentences over 47 files but could link
    only 16 (prose, file) pairs to a five-margin block, because it rebuilt those blocks
    itself from 83 file x family blocks.  So 42 of the record's 58 PROSE claims — the
    claims idea 480 actually names — were left unaudited, and idea 632 chose IQR on a
    DENSITY-INVARIANCE argument, i.e. on taste, with no external criterion saying which
    unit is RIGHT.  This run does the two things that leaves open:

    PART A  LINK THE PROSE.  Idea 253's committed census
            (`2026-09-09_does-a-random-sub-panel-pass-4b-because-the-CAGR-floor-moves_B
            .census.csv`, 25,153 rows over 238 source files) already carries BOTH units
            per row (`binding_raw`, `binding`).  Linking the prose to THAT, by file stem,
            audits far more of the record than rebuilding blocks does.  Idea 150 first,
            as the queue asks.  CHANGELOG.md prose is scanned too.

    PART B  DECIDE THE UNIT WITH A COUNTERFACTUAL, not with taste.  A binding-bar claim
            is a PREDICTIVE claim: on a passer it says "this is the bar you lose first",
            on a failure "this is the bar you must move to turn it into a pass".  Both are
            directly falsifiable by moving the dial and watching which bar actually breaks
            first / clears last.  That is ground truth BY CONSTRUCTION, not another
            normalisation.  Score RAW and NOISE (and IQR, RANK) on how often each names
            it, and a units debate becomes an accuracy number.

DEFINITIONS, fixed in advance
    Five 4b margins of an arm against SPY on the identical sample:
        m_H1   = Sharpe_arm(H1)  - Sharpe_SPY(H1)          [Sharpe units]
        m_H2   = Sharpe_arm(H2)  - Sharpe_SPY(H2)          [Sharpe units]
        m_OOS  = Sharpe_arm(OOS) - Sharpe_SPY(OOS)         [Sharpe units]
        m_DD   = 0.60*|MaxDD_SPY| - |MaxDD_arm|            [MaxDD fraction]
        m_CAGR = CAGR_arm - 0.70*CAGR_SPY                  [CAGR fraction]
    4b passes iff min of the five >= 0.  PROTOCOL 4b verbatim.
    RAW   argmin over the five margins as published (three different units).
    NOISE argmin over m_b / sd_null(b | panel), sd_null = sd of that bar's slack over
          random sub-panel draws on the SAME panel — idea 253's construction, reproduced
          here, and the literal "panel-noise units" the queue names.
    IQR / RANK  idea 632's other two normalisers, carried as robustness, not as headline.

GROUND TRUTH (PART B), pre-registered before it was run.  Distances below are |index
distance| in GRID STEPS along the arm's own dial, direction-agnostic, +inf when the event
never happens on the grid.  Two regimes, because the record publishes in both:
    PASS  (idea 253's census is 25,028 published 4b PASSES, so this regime carries the
          record's "the DD cap is what cuts" claims).  d_b = distance to the nearest dial
          value where bar b goes NEGATIVE; TRUE = argMIN_b d_b, the bar lost FIRST.
    FAIL  d_b = distance to the nearest value where bar b CLEARS (0 if already clear, so a
          satisfied bar can never be TRUE); TRUE = argMAX_b d_b, the bar that clears LAST.
    A UNIQUE extremum is the ground truth even at +inf; those rows are flagged
    `unreachable` and accuracy is reported with and without them.  TIES are EXCLUDED from
    the denominator rather than broken by a rule.
    Accuracy(unit) = P(unit's argmin here == TRUE bar) over the scorable arms.
    Rows with exactly ONE negative bar are agreement BY CONSTRUCTION (every positive
    rescaling shares that argmin) and are reported separately, not hidden in a pooled rate.

TUNED PARAMETERS: exactly two.
    UNIT  in {RAW, NOISE, IQR, RANK}          PANEL in {U56, B136, SMALL439}
    Every grid point of every dial on every panel is written to the .grid.csv, and every
    (UNIT x PANEL) cell is printed.  Nothing else is chosen by looking at an outcome.

RULE 8 (PROTOCOL 8, required): sd_null AND the ground truth are recomputed on
    IS <= 2016-12-31 alone; the unit is CHOSEN there; OOS >= 2017-01-01 is read ONCE.
    Reported OOS: (a) each unit's out-of-sample naming accuracy, and (b) the book you land
    on if you ACT on the named bar — DEFEND IT, i.e. move the dial to the IS value buying
    the most slack on it, among IS 4b passers where any exist — against the c0 control,
    the LIVE RULES v2 book cost-matched, RULES v1, and SPY.
    Both KEEP paths are evaluated on EVERY grid point, and neither is assumed.

CAVEATS, stated not buried
  - SURVIVORSHIP (PROTOCOL 9): all three panels are CURRENT-constituent lists; SMALL439
    additionally drops data/small_meta.csv max_1d_move >= 1.0 (idea 118, a terminal-dated
    screen per idea 627).  Absolute CAGR/Sharpe levels are biased up and none is a
    tradable estimate.  Only within-panel contrasts — which bar is the argmin, and
    RAW-vs-NOISE — are meant to survive that bias; both units are read off the IDENTICAL
    books, so the bias is common to them.
  - Idea 38: u56/broad still carry the calendar-day index (BTC-driven weekend rows).
  - Idea 126: t+1 execution only, no lag band.
  - PART A audits the record's PROSE against the record's OWN committed census.  Where a
    prose file committed no census rows it is reported as UNLINKED, never imputed.
"""
import sys, re, json, time, zlib
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, band_state  # noqa
from engine import backtest, metrics, rebalance_mask                                # noqa

OUT = Path(__file__).with_suffix("")
BT = ROOT / "research" / "backtests"
CENSUS = BT / "2026-09-09_does-a-random-sub-panel-pass-4b-because-the-CAGR-floor-moves_B.census.csv"

FREQ, COST = "W", 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
BARS = ["H1", "H2", "OOS", "DD", "CAGR"]
UNITS = ["RAW", "NOISE", "IQR", "RANK"]
NDRAW, KFRAC = 150, 0.5          # random sub-panel null: 150 draws of half the panel
SEED = 4800

_LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); _LOG.append(s)


# ============================================================ harness
def fast_backtest(prices, weights, freq=FREQ):
    """Vectorised equivalent of engine.backtest (asserted against it in GATE 1)."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy(); m[0] = True
    T, Ncol = rets.shape
    C = np.cumprod(1.0 + rets, axis=0); Cp = np.vstack([np.ones((1, Ncol)), C[:-1]])
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]; W0 = wt[s0]
    h = W0 * (Cp / Cp[s0]); V = h.sum(axis=1) + (1.0 - W0.sum(axis=1)); held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]; W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p]); Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1)); heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T); turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    net = (held * rets).sum(axis=1) - turn * COST / 1e4
    return pd.Series(net, index=idx)


def _m(r):
    eq = (1 + r).cumprod(); yrs = len(r) / 252
    vol = r.std() * np.sqrt(252)
    return (eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan,
            (r.mean() * 252) / vol if vol else np.nan,
            (eq / eq.cummax() - 1).min())


def margins(r, spy, window="FULL"):
    """The five 4b margins of return series r against SPY, PROTOCOL 4b verbatim."""
    if window == "IS":   r, spy = r.loc[:IS_END], spy.loc[:IS_END]
    elif window == "OOS": r, spy = r.loc[OOS_START:], spy.loc[OOS_START:]
    h = len(r) // 2
    _, sH1, _ = _m(r.iloc[:h]);  _, bH1, _ = _m(spy.iloc[:h])
    _, sH2, _ = _m(r.iloc[h:]);  _, bH2, _ = _m(spy.iloc[h:])
    ro, so = r.loc[OOS_START:], spy.loc[OOS_START:]
    if len(ro) > 260:
        _, sO, _ = _m(ro); _, bO, _ = _m(so)
    else:                      # IS window contains no OOS leg; carry H2 as the third Sharpe
        sO, bO = sH2, bH2
    cg, sh, dd = _m(r); bcg, bsh, bdd = _m(spy)
    return dict(m_H1=sH1 - bH1, m_H2=sH2 - bH2, m_OOS=sO - bO,
                m_DD=0.60 * abs(bdd) - abs(dd), m_CAGR=cg - 0.70 * bcg,
                CAGR=cg, Sharpe=sh, MaxDD=dd)


def argmin_bar(row, scale=None):
    v = {b: row[f"m_{b}"] / (1.0 if scale is None else scale[b]) for b in BARS}
    return min(v, key=v.get), min(v.values())


# ============================================================ panels and dials
class Panel:
    def __init__(self, name, px):
        self.name, self.px = name, px
        self.q = px.drop(columns=["SPY"])
        self.spy = px["SPY"].pct_change().fillna(0.0)
        mom = self.q.shift(21) / self.q.shift(252) - 1
        r6 = self.q / self.q.shift(126) - 1
        r3 = self.q / self.q.shift(63) - 1
        self.comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True)
                     + r3.rank(axis=1, pct=True)) / 3
        self.vol20 = self.q.pct_change().rolling(20).std() * np.sqrt(252)
        self.above200 = self.q > self.q.rolling(200).mean()
        self._band, self._run = {}, {}
        self.start = px.index[260]

    def bandst(self, b):
        k = round(float(b), 8)
        if k not in self._band: self._band[k] = band_state(self.q, k)
        return self._band[k]

    def book(self, dial, c):
        """V2 host for band/gross (the live rules' shape); V1 host for n."""
        if dial == "band":
            e = self.q.notna().astype(float)
            ew = 0.75 * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
            w = ew.where(self.bandst(c), 0.0)
        elif dial == "gross":
            e = self.q.notna().astype(float)
            ew = float(c) * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
            w = ew.where(self.bandst(0.03), 0.0)
        elif dial == "n":
            s = self.comp * (0.5 + 0.5 * self.above200.astype(float))
            s = s / self.vol20.clip(lower=0.08) ** 0.5
            elig = s.where(self.above200 & (self.vol20 < 0.60))
            w = (elig.rank(axis=1, ascending=False) <= int(c)).astype(float) * (0.75 / int(c))
        else: raise ValueError(dial)
        return w.reindex(columns=self.px.columns).fillna(0.0)

    def run(self, dial, c):
        """Deterministic; memoised so the same arm is never priced twice in one run."""
        k = (dial, round(float(c), 8))
        if k not in self._run:
            self._run[k] = fast_backtest(self.px, self.book(dial, c)).loc[self.start:]
        return self._run[k]


DIALS = {                                    # c0 = the record's adopted value
    "band":  dict(c0=0.03, vals=[round(0.00 + 0.01 * i, 4) for i in range(13)]),
    "gross": dict(c0=0.75, vals=[round(0.30 + 0.05 * i, 4) for i in range(19)]),
    "n":     dict(c0=5,    vals=[1, 3, 5, 7, 9, 11, 15, 19, 23, 29]),
}


# ============================================================ GATES
def gates(panels):
    P("\n=== GATES (all pre-registered; a failure here stops the run) ===")
    p = panels["U56"]
    w = p.book("gross", 0.75)
    ref = backtest(p.px, w, cost_bps=COST, freq=FREQ)["returns"]
    got = fast_backtest(p.px, w)
    d_ev = float(np.abs(ref.loc[p.start:].values - got.loc[p.start:].values).max())
    nan_ref = int(ref.isna().sum())
    d_all = float(np.nanmax(np.abs(ref.values - got.values)))
    P(f"G1  fast_backtest vs engine.backtest, U56 gross=0.75 : max|diff| on the EVALUATION "
      f"window (>= px.index[260], the only window this run reads) {d_ev:.3e}")
    P(f"    whole sample, finite rows only: {d_all:.3e}.  engine.backtest returns NaN on "
      f"{nan_ref} rows (its row-0 turnover is NaN because w_target.shift(1) is NaN there); "
      f"both rows are 2008 warm-up and are dropped by every arm in this run.")
    assert d_ev < 1e-12 and d_all < 1e-12, "G1 FAILED"

    lv = backtest(p.px, rules_v2_weights(p.px), cost_bps=COST, freq=FREQ)["returns"].loc[p.start:]
    cg, sh, dd = _m(lv)
    P(f"G2  LIVE RULES v2, U56 @10bps : CAGR {cg:.2%}  Sharpe {sh:.4f}  MaxDD {dd:.2%}")

    C = pd.read_csv(CENSUS)
    dis = float((C.binding != C.binding_raw).mean())
    raw = C.binding_raw.value_counts(); nz = C.binding.value_counts()
    P(f"G3  idea 253's committed census re-read: {len(C):,} rows over {C.file.nunique()} files")
    P(f"    RAW modal  {raw.index[0]} {raw.iloc[0]:,}/{len(C):,} = {raw.iloc[0]/len(C):.3f}"
      f"   (queue says CAGR 0.672)")
    P(f"    NOISE modal {nz.index[0]} {nz.iloc[0]:,}/{len(C):,} = {nz.iloc[0]/len(C):.3f}"
      f"   (queue says DD 0.476)")
    P(f"    disagreement {dis:.4f}   (queue says 0.261)")
    assert abs(dis - 0.261) < 0.01, "G3 FAILED: census does not reproduce the queue's premise"
    # G4: the census's own z columns are its m columns divided by a per-panel constant
    ok = []
    for pan, g in C.groupby("panel"):
        if len(g) < 50: continue
        for b in BARS:
            rr = g[f"m_{b}"] / g[f"z_{b}"]
            ok.append(float(rr.std() / abs(rr.mean())) if abs(rr.mean()) > 0 else 1.0)
    P(f"G4  census z == m / per-panel constant : max relative sd over bars {max(ok):.3e}")
    assert max(ok) < 1e-9, "G4 FAILED: z is not a per-panel rescaling of m"
    return C


# ============================================================ PART A — the prose audit
BARWORD = {"CAGR": r"CAGR", "DD": r"(?:MaxDD|DD cap|drawdown cap|DD leg)",
           "H1": r"\bH1\b", "H2": r"\bH2\b", "OOS": r"\bOOS\b"}
BINDSENT = re.compile(r"[^.\n]*\b(?:binding bar|bar that (?:binds|cuts)|what (?:binds|cuts)|"
                      r"sole (?:bar|cut)|binds\b|is the binding)\b[^.\n]*", re.I)


def part_a(C):
    P("\n=== PART A — every published binding-bar claim, re-read under BOTH units ===")
    files = sorted(list(BT.glob("*.result.md")) + list(BT.glob("*.memo.md")))
    prose = []
    for f in files:
        for s in BINDSENT.findall(f.read_text(errors="ignore")):
            named = [b for b, p in BARWORD.items() if re.search(p, s)]
            if len(named) == 1:
                prose.append(dict(src=f.name, stem=f.name.split(".")[0], kind="result/memo",
                                  bar=named[0], sentence=" ".join(s.split())[:240]))
    nres = len(prose)
    for s in BINDSENT.findall((ROOT / "research" / "CHANGELOG.md").read_text(errors="ignore")):
        named = [b for b, p in BARWORD.items() if re.search(p, s)]
        if len(named) == 1:
            prose.append(dict(src="CHANGELOG.md", stem="CHANGELOG", kind="changelog",
                              bar=named[0], sentence=" ".join(s.split())[:240]))
    PR = pd.DataFrame(prose)
    P(f"  files scanned: {len(files)} result/memo + CHANGELOG.md")
    P(f"  sentences naming EXACTLY ONE bar : {nres} in result/memo over "
      f"{PR[PR.kind=='result/memo'].src.nunique()} files (idea 632 reports 58 over 47) "
      f"+ {len(PR)-nres} in CHANGELOG.md")
    P("  bar named (all sources): " + "  ".join(f"{k}={v}" for k, v in PR.bar.value_counts().items()))

    # link each prose stem to idea 253's census rows produced by the SAME run
    C = C.copy(); C["stem"] = C.file.str.split(".").str[0]
    agg = {}
    for stem, g in C.groupby("stem"):
        row = dict(n_rows=len(g),
                   raw_modal=g.binding_raw.value_counts().index[0],
                   raw_share=g.binding_raw.value_counts(normalize=True).iloc[0],
                   noise_modal=g.binding.value_counts().index[0],
                   noise_share=g.binding.value_counts(normalize=True).iloc[0],
                   disagree=float((g.binding != g.binding_raw).mean()),
                   panel="|".join(sorted(g.panel.dropna().unique())))
        agg[stem] = row
    PR["linked"] = PR.stem.isin(agg)
    for k in ("n_rows", "raw_modal", "noise_modal", "disagree", "panel", "raw_share", "noise_share"):
        PR[k] = PR.stem.map(lambda s: agg.get(s, {}).get(k))
    PR["match_raw"] = np.where(PR.linked, PR.bar == PR.raw_modal, None)
    PR["match_noise"] = np.where(PR.linked, PR.bar == PR.noise_modal, None)
    PR["FLIPS"] = np.where(PR.linked, PR.raw_modal != PR.noise_modal, None)
    PR.to_csv(OUT.with_suffix(".prose.csv"), index=False)

    L = PR[PR.linked]
    P(f"\n  LINKED to idea 253's census by run stem: {len(L)}/{len(PR)} claims "
      f"over {L.stem.nunique()} runs   (idea 632 could link 16)")
    if len(L):
        P(f"    prose bar == the run's own RAW   modal bar : {int(L.match_raw.sum())}/{len(L)}"
          f" = {L.match_raw.mean():.3f}")
        P(f"    prose bar == the run's own NOISE modal bar : {int(L.match_noise.sum())}/{len(L)}"
          f" = {L.match_noise.mean():.3f}")
        P(f"    runs whose modal bar FLIPS between the units: "
          f"{int(L.FLIPS.sum())}/{len(L)} claims = {L.FLIPS.mean():.3f}")
        P("\n    per claim (the audit idea 480 asks for):")
        P(f"    {'prose':>5s} {'RAW':>5s} {'NOISE':>5s} {'dis':>6s} {'panel':>10s}  source")
        for _, r in L.sort_values(["FLIPS", "src"], ascending=[False, True]).iterrows():
            flag = "FLIP" if r.FLIPS else "    "
            P(f"    {r.bar:>5s} {r.raw_modal:>5s} {r.noise_modal:>5s} {r.disagree:6.3f} "
              f"{str(r.panel):>10s}  {flag} {r.src}")
    U = PR[~PR.linked]
    P(f"\n  UNLINKED (the run committed no census rows; NOT imputed): {len(U)} claims "
      f"over {U.src.nunique()} sources")
    P("    unlinked bars: " + "  ".join(f"{k}={v}" for k, v in U.bar.value_counts().items()))

    # idea 150 first, as the queue asks
    P("\n  IDEA 150 (the queue names it first):")
    h150 = PR[PR.src.str.contains("150", na=False) | PR.sentence.str.contains("idea 150", case=False)]
    if len(h150):
        for _, r in h150.iterrows():
            P(f"    [{r.bar}] {r.src}: {r.sentence[:150]}")
    else:
        P("    no sentence in any committed result/memo/CHANGELOG names a single binding bar")
        P("    AND is attributable to idea 150 by filename or by an in-text 'idea 150' reference.")
    c150 = C[C.stem.str.contains("150", na=False)]
    P(f"    idea-150-stemmed census rows: {len(c150)}")

    # per-panel disagreement — the second tuned parameter, on the record's own census
    P("\n  DISAGREEMENT BY PANEL (the record's own census, all 25,153 rows):")
    for pan, g in C.groupby("panel"):
        P(f"    {pan:8s} N={len(g):6,d}  RAW modal {g.binding_raw.value_counts().index[0]:>4s} "
          f"({g.binding_raw.value_counts(normalize=True).iloc[0]:.3f})  "
          f"NOISE modal {g.binding.value_counts().index[0]:>4s} "
          f"({g.binding.value_counts(normalize=True).iloc[0]:.3f})  "
          f"disagree {float((g.binding != g.binding_raw).mean()):.4f}")
    return PR


def part_a2(C, SD):
    """"Panel-noise units" is not ONE unit.  The record's committed z uses idea 253's null;
    this run's uses its own.  Recover idea 253's implied scale from its own committed
    columns (sd_b = mean(m_b / z_b), exact by G4) and re-score all 25,153 rows under both."""
    P("\n=== PART A2 — the UNIT ITSELF is a construction choice, and it is the whole story ===")
    PMAP = {"U56": "U56", "B136": "B136", "SMALL": "SMALL439"}
    rows = []
    for pan, g in C.groupby("panel"):
        if len(g) < 50 or pan not in PMAP: continue
        sd253 = {b: float((g[f"m_{b}"] / g[f"z_{b}"]).mean()) for b in BARS}
        sdB = SD.loc[PMAP[pan]].to_dict()
        rows.append(dict(panel=pan, N=len(g),
                         **{f"sd253_{b}": sd253[b] for b in BARS},
                         **{f"sdB_{b}": sdB[b] for b in BARS},
                         ratio253=sd253["DD"] / sd253["CAGR"], ratioB=sdB["DD"] / sdB["CAGR"]))
    S = pd.DataFrame(rows)
    P("  sd_null(DD) / sd_null(CAGR) — the single ratio that decides DD-vs-CAGR, because")
    P("  binding = argmin_b m_b/sd_b and those two are the contest:")
    P(f"    {'panel':<8s}{'idea 253 null':>16s}{'this run null':>16s}{'x':>8s}")
    for _, r in S.iterrows():
        P(f"    {r.panel:<8s}{r.ratio253:16.3f}{r.ratioB:16.3f}{r.ratio253/r.ratioB:8.2f}")
    P("  idea 253's null: random SUB-PANELS at the panel's own k; this run's: equal-weight")
    P("  random half-panels inside the live 200d band.  Both are defensible 'panel noise'.")

    # re-score the record's own rows under this run's null
    D = C[C.panel.isin(PMAP)].copy()
    scal = {pan: SD.loc[PMAP[pan]].to_dict() for pan in D.panel.unique()}
    zb = pd.DataFrame({b: D.apply(lambda r, b=b: r[f"m_{b}"] / scal[r.panel][b], axis=1)
                       for b in BARS})
    D["binding_B"] = [BARS[i] for i in zb.values.argmin(axis=1)]
    P(f"\n  the record's own {len(D):,} rows, re-scored under this run's null:")
    for nm, col in (("RAW (published m)", "binding_raw"),
                    ("NOISE, idea 253's null (the committed z)", "binding"),
                    ("NOISE, this run's null", "binding_B")):
        vc = D[col].value_counts(normalize=True)
        P(f"    {nm:<42s} " + "  ".join(f"{k} {v:.3f}" for k, v in vc.items()))
    P(f"    rows whose NOISE bar MOVES when only the null changes: "
      f"{float((D.binding != D.binding_B).mean()):.4f} "
      f"({int((D.binding != D.binding_B).sum()):,}/{len(D):,})")
    P(f"    for comparison, RAW vs the committed NOISE: {float((D.binding_raw != D.binding).mean()):.4f}")
    P("    per panel:")
    for pan, g in D.groupby("panel"):
        P(f"      {pan:<6s} N={len(g):6,d}  RAW {g.binding_raw.value_counts().index[0]:>4s}"
          f"  NOISE-253 {g.binding.value_counts().index[0]:>4s}"
          f"  NOISE-B {g.binding_B.value_counts().index[0]:>4s}"
          f"   null-change flip {float((g.binding != g.binding_B).mean()):.4f}")
    D[["panel", "file", "binding_raw", "binding", "binding_B"]].to_csv(
        OUT.with_suffix(".rescored.csv"), index=False)
    S.to_csv(OUT.with_suffix(".scales.csv"), index=False)
    return D, S


PANEL_ALIAS = {"u56": "U56", "universe.json(56)": "U56", "universe.json": "U56",
               "broad": "B136", "broad136": "B136", "universe_broad.json": "B136",
               "universe_broad(136)": "B136",
               "small": "SMALL439", "small439": "SMALL439"}


def part_a3(C, SD, PR):
    """The queue names idea 150 FIRST.  Its own committed grid carries the five margins
    (suffixed `m_*_`), so it — and every other committed CSV with a complete five-margin
    block — can be re-read under both units DIRECTLY, without idea 253's census.  This is
    the audit the queue asked for, on 98 files rather than the 13 the census reaches."""
    P("\n=== PART A3 — every committed FIVE-MARGIN block re-read under both units ===")
    sd253 = {}
    for pan, g in C.groupby("panel"):
        if len(g) < 50: continue
        key = {"U56": "U56", "B136": "B136", "SMALL": "SMALL439"}.get(pan)
        if key: sd253[key] = {b: float((g[f"m_{b}"] / g[f"z_{b}"]).mean()) for b in BARS}
    P(f"  idea 253's implied scales recovered for: {sorted(sd253)}  (SMALL has only "
      f"{int((C.panel=='SMALL').sum())} census rows, so it has no recoverable scale)")

    recs, files = [], sorted(BT.glob("*.csv"))
    for f in files:
        try: hdr = pd.read_csv(f, nrows=0).columns.tolist()
        except Exception: continue
        cols = set(hdr)
        suf = ("" if {f"m_{b}" for b in BARS} <= cols else
               ("_" if {f"m_{b}_" for b in BARS} <= cols else None))
        if suf is None: continue
        pc = [c for c in hdr if c.lower().strip("_") in ("panel", "universe", "uni")]
        use = [f"m_{b}{suf}" for b in BARS] + pc[:1]
        try: d = pd.read_csv(f, usecols=use)
        except Exception: continue
        d = d.dropna(subset=[f"m_{b}{suf}" for b in BARS])
        if len(d) < 8: continue
        M = d[[f"m_{b}{suf}" for b in BARS]].values
        raw = np.array(BARS)[M.argmin(axis=1)]
        if pc:
            pan = d[pc[0]].astype(str).str.strip().map(
                lambda v: PANEL_ALIAS.get(v.lower(), v if v in ("U56", "B136", "SMALL439") else None))
        else:
            pan = pd.Series([None] * len(d))
        n_unstated = int(pan.isna().sum())
        z253 = np.full(M.shape, np.nan); zB = np.full(M.shape, np.nan)
        for i, pv in enumerate(pan.values):
            if pv in sd253: z253[i] = M[i] / np.array([sd253[pv][b] for b in BARS])
            if pv in SD.index: zB[i] = M[i] / SD.loc[pv, BARS].values
        ok253 = ~np.isnan(z253).any(axis=1); okB = ~np.isnan(zB).any(axis=1)
        n253 = (np.array(BARS)[np.where(ok253[:, None], z253, 0).argmin(axis=1)]
                if ok253.any() else None)
        nB = (np.array(BARS)[np.where(okB[:, None], zB, 0).argmin(axis=1)]
              if okB.any() else None)
        mode = lambda a, m: (pd.Series(a[m]).value_counts().index[0] if m.any() else None)
        recs.append(dict(file=f.name, stem=f.name.split(".")[0], n=len(d),
                         panels="|".join(sorted({p for p in pan.dropna().unique()})),
                         n_panel_unstated=n_unstated,
                         raw_modal=pd.Series(raw).value_counts().index[0],
                         noise253_modal=mode(n253, ok253) if n253 is not None else None,
                         noiseB_modal=mode(nB, okB) if nB is not None else None,
                         flip253=(float((raw[ok253] != n253[ok253]).mean()) if n253 is not None else np.nan),
                         flipnull=(float((n253[ok253 & okB] != nB[ok253 & okB]).mean())
                                   if (n253 is not None and nB is not None and (ok253 & okB).any()) else np.nan)))
    A3 = pd.DataFrame(recs)
    A3.to_csv(OUT.with_suffix(".blocks.csv"), index=False)
    P(f"  committed CSVs carrying a COMPLETE five-margin block and >= 8 rows: {len(A3)} "
      f"(idea 632 found 81 claim-making blocks; this reaches them without rebuilding)")
    P(f"    total rows re-read: {int(A3.n.sum()):,}")
    unst = A3[A3.n_panel_unstated > 0]
    P(f"    files where at least one row's PANEL is unstated or unmappable: {len(unst)} "
      f"({int(A3.n_panel_unstated.sum()):,} rows) — these CANNOT be put in panel-noise")
    P("    units at all, which is itself the answer to 'state the unit': the conversion")
    P("    needs a panel the file never printed.")
    cv = A3.dropna(subset=["flip253"])
    P(f"\n  modal binding bar of each block, {len(cv)} convertible files:")
    for nm, col in (("RAW", "raw_modal"), ("NOISE, idea 253's null", "noise253_modal"),
                    ("NOISE, this run's null", "noiseB_modal")):
        vc = cv[col].value_counts()
        P(f"    {nm:<26s} " + "  ".join(f"{k} {v}" for k, v in vc.items()))
    P(f"    files whose modal bar FLIPS RAW -> NOISE-253 : "
      f"{int((cv.raw_modal != cv.noise253_modal).sum())}/{len(cv)} "
      f"= {float((cv.raw_modal != cv.noise253_modal).mean()):.3f}")
    cv2 = cv.dropna(subset=["flipnull"])
    P(f"    files whose modal bar MOVES when ONLY THE NULL changes: "
      f"{int((cv2.noise253_modal != cv2.noiseB_modal).sum())}/{len(cv2)} "
      f"= {float((cv2.noise253_modal != cv2.noiseB_modal).mean()):.3f}   "
      f"(cell-level median {cv2.flipnull.median():.3f})")

    P("\n  IDEA 150 — the claim the queue names FIRST — audited directly:")
    i150 = A3[A3.stem.str.contains("the-DD-cap-is-what-cuts", na=False)]
    if len(i150):
        for _, r in i150.iterrows():
            P(f"    {r.file}  ({int(r.n):,} rows, panels {r.panels or 'UNSTATED'})")
            P(f"      title claim   : DD")
            P(f"      RAW modal     : {r.raw_modal}")
            P(f"      NOISE-253     : {r.noise253_modal}   (cell flip vs RAW {r.flip253:.3f})"
              if pd.notna(r.flip253) else "      NOISE-253     : not convertible")
            P(f"      NOISE-this run: {r.noiseB_modal}")
            P(f"      VERDICT on the title: "
              + ("HOLDS under " + " and ".join(
                  [n for n, v in (("RAW", r.raw_modal), ("NOISE-253", r.noise253_modal),
                                  ("NOISE-B", r.noiseB_modal)) if v == "DD"])
                 if "DD" in (r.raw_modal, r.noise253_modal, r.noiseB_modal)
                 else "FAILS under every unit this run can form"))
    else:
        P("    no committed CSV from that run carries a complete five-margin block")

    # prose linked to a five-margin block (a much wider net than the census stems)
    # a run can commit several blocks; represent each stem by its LARGEST one
    B = A3.sort_values("n", ascending=False).drop_duplicates("stem").set_index("stem")
    PR = PR.copy()
    PR["blk"] = PR.stem.isin(B.index)
    L = PR[PR.blk]
    if len(L):
        for k in ("raw_modal", "noise253_modal", "noiseB_modal"):
            PR.loc[PR.blk, k] = PR.loc[PR.blk, "stem"].map(B[k])
        L = PR[PR.blk]
        P(f"\n  PROSE claims now auditable via a five-margin block: {len(L)}/{len(PR)} "
          f"over {L.stem.nunique()} runs (the census alone reached "
          f"{int(PR.linked.sum())})")
        for nm, col in (("RAW", "raw_modal"), ("NOISE-253", "noise253_modal"),
                        ("NOISE-this run", "noiseB_modal")):
            m = L[L[col].notna()]
            P(f"    prose bar == the block's own {nm:<14s} modal bar : "
              f"{int((m.bar == m[col]).sum())}/{len(m)}"
              + (f" = {float((m.bar == m[col]).mean()):.3f}" if len(m) else ""))
    PR.to_csv(OUT.with_suffix(".prose.csv"), index=False)
    return A3, PR


# ============================================================ PART B — noise units + ground truth
def null_returns(panels):
    """Price the random sub-panel null ONCE (seeded); every window reads the same draws.
    Idea 253's construction: equal-weight a random half of the panel inside the live band."""
    NR = {}
    for nm, p in panels.items():
        rng = np.random.default_rng(SEED + zlib.crc32(nm.encode()) % 100000)  # stable across processes
        cols = list(p.q.columns); k = max(5, int(round(KFRAC * len(cols))))
        series = []
        for _ in range(NDRAW):
            sub = [cols[j] for j in rng.choice(len(cols), size=k, replace=False)]
            e = p.q[sub].notna().astype(float)
            ew = 0.75 * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
            w = ew.where(p.bandst(0.03)[sub], 0.0).reindex(columns=p.px.columns).fillna(0.0)
            series.append(fast_backtest(p.px, w).loc[p.start:])
        NR[nm] = series
    return NR


def null_scales(panels, NR, window="FULL"):
    """sd_null / IQR_null (bar | panel) over those draws, on the requested window."""
    rows = []
    for nm, p in panels.items():
        spy = p.spy.loc[p.start:]
        for i, r in enumerate(NR[nm]):
            m = margins(r, spy, window)
            rows.append(dict(panel=nm, window=window, draw=i,
                             **{f"m_{b}": m[f"m_{b}"] for b in BARS}))
    N = pd.DataFrame(rows)
    cols = [f"m_{b}" for b in BARS]
    SD = N.groupby("panel")[cols].std(); SD.columns = BARS
    IQ = (N.groupby("panel")[cols].quantile(0.75) - N.groupby("panel")[cols].quantile(0.25))
    IQ.columns = BARS
    return N, SD, IQ


def build_grid(panels, window="FULL"):
    rows = []
    for nm, p in panels.items():
        for dial, cfg in DIALS.items():
            for c in cfg["vals"]:
                r = p.run(dial, c)
                m = margins(r, p.spy.loc[p.start:], window)
                rows.append(dict(panel=nm, dial=dial, c=c, is_c0=(c == cfg["c0"]), **m))
    G = pd.DataFrame(rows)
    G["m_min_raw"] = G[[f"m_{b}" for b in BARS]].min(axis=1)
    G["pass4b"] = G.m_min_raw >= 0
    return G


def label_units(G, SD, IQ):
    """Attach each unit's argmin bar to every grid row."""
    G = G.copy()
    G["bar_RAW"] = [argmin_bar(r, None)[0] for _, r in G.iterrows()]
    G["bar_NOISE"] = [argmin_bar(r, SD.loc[r.panel].to_dict())[0] for _, r in G.iterrows()]
    G["bar_IQR"] = [argmin_bar(r, IQ.loc[r.panel].to_dict())[0] for _, r in G.iterrows()]
    # RANK is a within-column percentile, so it needs the whole (panel,dial) block at once
    rk = []
    for _, g in G.groupby(["panel", "dial"], sort=False):
        R = g[[f"m_{b}" for b in BARS]].rank(pct=True)
        rk.append(pd.Series([BARS[i] for i in R.values.argmin(axis=1)], index=g.index))
    G["bar_RANK"] = pd.concat(rk).sort_index()
    return G


def ground_truth(G):
    """The counterfactual definition of "the bar that binds", in the two regimes the
    record actually publishes in.  Distances are |index distance| in GRID STEPS along the
    arm's own dial, direction-agnostic, +inf when the event never happens on the grid.

    PASS regime (idea 253's census is 25,028 published 4b PASSES, so this is the one that
        carries the record's "the DD cap is what cuts" claims).  For a passing arm,
            d_b = distance to the nearest dial value where bar b goes NEGATIVE.
        TRUE = argMIN_b d_b — the bar you lose FIRST, i.e. the one closest to binding.
    FAIL regime.  For a failing arm,
            d_b = distance to the nearest dial value where bar b CLEARS (0 if already
                  clear, so a satisfied bar can never be the TRUE bar).
        TRUE = argMAX_b d_b — the bar that clears LAST, i.e. the one that gates the pass.

    A UNIQUE argmin/argmax is the ground truth even at +inf; those rows are flagged
    `unreachable` and accuracy is reported with and without them.  Ties are EXCLUDED from
    the denominator rather than broken by a rule.  `n_neg` (how many of the five bars are
    negative here) is carried because with n_neg == 1 every positive rescaling has the
    same argmin: those rows are agreement by construction and are reported separately.
    """
    out = []
    for (pan, dial), g in G.groupby(["panel", "dial"], sort=False):
        g = g.sort_values("c").reset_index(drop=True)
        clr = {b: np.flatnonzero(g[f"m_{b}"].values >= 0) for b in BARS}
        brk = {b: np.flatnonzero(g[f"m_{b}"].values < 0) for b in BARS}
        for i, row in g.iterrows():
            n_neg = int(sum(row[f"m_{b}"] < 0 for b in BARS))
            if row.pass4b:
                regime, src, pick = "PASS", brk, min
            else:
                regime, src, pick = "FAIL", clr, max
            d = {b: (float(np.abs(src[b] - i).min()) if len(src[b]) else np.inf) for b in BARS}
            ext = pick(d.values()); tie = sum(1 for v in d.values() if v == ext)
            true = (min(d, key=d.get) if regime == "PASS" else max(d, key=d.get))
            out.append(dict(panel=pan, dial=dial, c=row.c, is_c0=row.is_c0, regime=regime,
                            n_neg=n_neg, **{f"d_{b}": d[b] for b in BARS},
                            unreachable=bool(not np.isfinite(ext)),
                            TRUE=(true if tie == 1 else "TIE"),
                            **{f"bar_{u}": row[f"bar_{u}"] for u in UNITS}))
    return pd.DataFrame(out)


def part_b(G, T):
    P("\n=== PART B — which unit NAMES THE BAR THAT ACTUALLY GATES THE PASS ===")
    P(f"  fresh grid: {len(G)} points ({G.panel.nunique()} panels x {G.dial.nunique()} dials), "
      f"all written to .grid.csv;  4b passes {int(G.pass4b.sum())}/{len(G)}")
    P(f"  arms with a ground-truth bar: {len(T)} rows "
      f"(PASS {int((T.regime=='PASS').sum())} / FAIL {int((T.regime=='FAIL').sum())})")
    P(f"    scorable {int((T.TRUE!='TIE').sum())}   TIE {int((T.TRUE=='TIE').sum())} (EXCLUDED)"
      f"   of the scorable, {int(T[T.TRUE!='TIE'].unreachable.sum())} name a bar whose "
      f"counterfactual never happens on the dial")
    S = T[T.TRUE != "TIE"]
    if not len(S):
        P("  no scorable rows — accuracy undefined; reported as such."); return None
    P("  TRUE bar distribution: " + "  ".join(f"{k}={v}" for k, v in S.TRUE.value_counts().items()))

    def block(title, D):
        if not len(D): P(f"\n  {title}: no rows"); return []
        P(f"\n  {title}")
        P(f"    {'PANEL':<10s}" + "".join(f"{u:>9s}" for u in UNITS) + f"{'N':>7s}")
        rr = []
        for pan in list(G.panel.unique()) + ["ALL"]:
            g = D if pan == "ALL" else D[D.panel == pan]
            if not len(g): continue
            acc = {u: float((g[f"bar_{u}"] == g.TRUE).mean()) for u in UNITS}
            rr.append(dict(subset=title, panel=pan, N=len(g), **acc))
            P(f"    {pan:<10s}" + "".join(f"{acc[u]:9.3f}" for u in UNITS) + f"{len(g):7d}")
        return rr

    rows = []
    rows += block("ACCURACY, ALL scorable rows (2-param grid, every cell printed)", S)
    rows += block("PASS regime — 'which bar do I lose FIRST' (the record's census is PASSES)",
                  S[S.regime == "PASS"])
    rows += block("FAIL regime — 'which bar clears LAST'", S[S.regime == "FAIL"])
    DIS = S[S.bar_RAW != S.bar_NOISE]
    rows += block("THE ROWS THAT DECIDE IT — RAW and NOISE name DIFFERENT bars", DIS)
    A = pd.DataFrame(rows)

    P("\n  by DIAL (reported, not tuned):")
    P(f"    {'DIAL':<10s}" + "".join(f"{u:>9s}" for u in UNITS) + f"{'N':>7s}")
    for dial, g in S.groupby("dial"):
        P(f"    {dial:<10s}" + "".join(f"{float((g[f'bar_{u}']==g.TRUE).mean()):9.3f}" for u in UNITS)
          + f"{len(g):7d}")
    P("\n  by n_neg (how many of the five bars are negative at the point):")
    P(f"    {'n_neg':<10s}" + "".join(f"{u:>9s}" for u in UNITS) + f"{'N':>7s}"
      + "   RAW==NOISE")
    for k, g in S.groupby("n_neg"):
        P(f"    {k:<10d}" + "".join(f"{float((g[f'bar_{u}']==g.TRUE).mean()):9.3f}" for u in UNITS)
          + f"{len(g):7d}" + f"{float((g.bar_RAW==g.bar_NOISE).mean()):13.3f}")
    P("    (with exactly one negative bar every positive rescaling has the same argmin, so")
    P("     those rows are agreement BY CONSTRUCTION and carry no information about units.)")

    P("\n  THE DEGENERACY THAT LIMITS THIS TEST, stated before the scores are read:")
    vc = S.TRUE.value_counts(normalize=True)
    P("    TRUE bar shares: " + "  ".join(f"{k} {v:.3f}" for k, v in vc.items()))
    P(f"    a CONSTANT predictor that always says '{vc.index[0]}' scores {vc.iloc[0]:.3f} — "
      f"{'ABOVE' if vc.iloc[0] > max(float((S[f'bar_{u}']==S.TRUE).mean()) for u in UNITS) else 'below'}"
      f" every unit.  On the record's own panels and dials the bar that actually gates is")
    P("    almost always the same one, so this experiment can rank the units but cannot")
    P("    credit any of them with information the constant does not already have.")
    best = A[(A.subset.str.startswith("ACCURACY")) & (A.panel == "ALL")][UNITS].iloc[0]
    P(f"\n  chance = {1.0/len(BARS):.3f}.  Pooled: " + "  ".join(f"{u} {best[u]:.3f}" for u in UNITS))
    P(f"  RAW - NOISE = {best['RAW']-best['NOISE']:+.3f} "
      f"({int(S.eval('bar_RAW==TRUE').sum())} vs {int(S.eval('bar_NOISE==TRUE').sum())} of {len(S)})")
    P(f"  units DISAGREE on {float((S.bar_RAW != S.bar_NOISE).mean()):.3f} of scorable rows "
      f"(N={len(DIS)}); there RAW right {float((DIS.bar_RAW==DIS.TRUE).mean()) if len(DIS) else float('nan'):.3f}, "
      f"NOISE right {float((DIS.bar_NOISE==DIS.TRUE).mean()) if len(DIS) else float('nan'):.3f}, "
      f"neither {float(((DIS.bar_RAW!=DIS.TRUE)&(DIS.bar_NOISE!=DIS.TRUE)).mean()) if len(DIS) else float('nan'):.3f}")
    R = S[~S.unreachable]
    if len(R):
        P(f"  rows whose counterfactual is REACHABLE on the dial (N={len(R)}): "
          + "  ".join(f"{u} {float((R[f'bar_{u}']==R.TRUE).mean()):.3f}" for u in UNITS))
    return A


# ============================================================ PART C — rule 8
def act_on_claim(p, dial, c0, bar, G):
    """The decision a binding-bar claim implies, and the only one that works in BOTH
    regimes: DEFEND THE NAMED BAR — move the dial to the value that buys the most slack on
    it.  Among the grid values that pass 4b if any do, else among all of them.  Everything
    here is read off the IS grid only.  Returns (picked value, moved?)."""
    g = G[(G.panel == p) & (G.dial == dial)].sort_values("c").reset_index(drop=True)
    cand = g[g.pass4b] if bool(g.pass4b.any()) else g
    c = float(cand.loc[cand[f"m_{bar}"].idxmax(), "c"])
    return c, not np.isclose(c, float(c0))


def part_c(panels, NR, G_full, SDf, IQf):
    P("\n=== PART C — RULE 8: unit chosen on 2009-2016 ONLY, 2017-2026 read ONCE ===")
    _, SDi, IQi = null_scales(panels, NR, "IS")
    P("  sd_null re-estimated on IS alone (per panel, per bar):")
    P("    " + SDi.to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n    "))
    G_is = build_grid(panels, "IS")
    G_is = label_units(G_is, SDi, IQi)
    T_is = ground_truth(G_is)
    S_is = T_is[T_is.TRUE != "TIE"]
    accIS = {u: float((S_is[f"bar_{u}"] == S_is.TRUE).mean()) for u in UNITS} if len(S_is) else {}
    P(f"  IS accuracy (N={len(S_is)}): " + "  ".join(f"{u} {accIS.get(u, float('nan')):.3f}" for u in UNITS))
    CHOSEN = max(accIS, key=accIS.get) if accIS else "RAW"
    P(f"  ==> UNIT CHOSEN ON IS ALONE: {CHOSEN}")

    G_oos = build_grid(panels, "OOS")
    _, SDo, IQo = null_scales(panels, NR, "OOS")
    G_oos = label_units(G_oos, SDo, IQo)
    T_oos = ground_truth(G_oos)
    S_oos = T_oos[T_oos.TRUE != "TIE"]
    accOOS = {u: float((S_oos[f"bar_{u}"] == S_oos.TRUE).mean()) for u in UNITS} if len(S_oos) else {}
    P(f"  OOS accuracy (N={len(S_oos)}), read once: "
      + "  ".join(f"{u} {accOOS.get(u, float('nan')):.3f}" for u in UNITS))
    P(f"  the IS-chosen unit {CHOSEN} scores {accOOS.get(CHOSEN, float('nan')):.3f} OOS; "
      f"the OOS-best unit is {max(accOOS, key=accOOS.get) if accOOS else 'n/a'}")

    # ---- the BOOK side: act on the IS-named bar, evaluate the resulting book OOS
    P("\n  ACTING ON THE CLAIM — DEFEND THE NAMED BAR: dial moved to the IS value buying the")
    P("  most slack on it (among IS 4b passers where any exist), then the resulting book read")
    P("  out of sample 2017-2026, a window never used to choose anything above:")
    recs = []
    for pan, p in panels.items():
        spy_o = p.spy.loc[OOS_START:]
        cg_s, sh_s, dd_s = _m(spy_o)
        v2f = fast_backtest(p.px, rules_v2_weights(p.px)).loc[p.start:]
        v1f = fast_backtest(p.px, rules_v1_weights(p.px)).loc[p.start:]
        cg_2, sh_2, dd_2 = _m(v2f.loc[OOS_START:]); cg_1, sh_1, dd_1 = _m(v1f.loc[OOS_START:])
        H = len(v2f) // 2
        f2cg, f2sh, f2dd = _m(v2f); _, f2H1, _ = _m(v2f.iloc[:H]); _, f2H2, _ = _m(v2f.iloc[H:])
        f1cg, f1sh, f1dd = _m(v1f); _, f1H1, _ = _m(v1f.iloc[:H]); _, f1H2, _ = _m(v1f.iloc[H:])
        spy_f = p.spy.loc[p.start:]
        fscg, fssh, fsdd = _m(spy_f); _, fsH1, _ = _m(spy_f.iloc[:H]); _, fsH2, _ = _m(spy_f.iloc[H:])
        for dial, cfg in DIALS.items():
            c0 = cfg["c0"]
            base = G_is[(G_is.panel == pan) & (G_is.dial == dial) & (G_is.is_c0)]
            if not len(base): continue
            row0 = base.iloc[0]
            for u in UNITS + ["CONTROL"]:
                if u == "CONTROL": c_pick, moved = float(c0), False
                else: c_pick, moved = act_on_claim(pan, dial, c0, row0[f"bar_{u}"], G_is)
                rf = p.run(dial, c_pick)
                cg, sh, dd = _m(rf.loc[OOS_START:])
                mo = margins(rf, p.spy.loc[p.start:], "FULL")
                hh = len(rf) // 2
                _, fH1, _ = _m(rf.iloc[:hh]); _, fH2, _ = _m(rf.iloc[hh:])
                fcg, fsh, fdd = _m(rf)
                recs.append(dict(panel=pan, dial=dial, unit=u,
                                 IS_bar=(row0[f"bar_{u}"] if u != "CONTROL" else "-"),
                                 c0=c0, c_pick=c_pick, moved=moved,
                                 FULL_CAGR=fcg, FULL_Sharpe=fsh, FULL_MaxDD=fdd,
                                 FULL_H1=fH1, FULL_H2=fH2,
                                 OOS_CAGR=cg, OOS_Sharpe=sh, OOS_MaxDD=dd,
                                 SPY_Sharpe=sh_s, SPY_CAGR=cg_s, SPY_MaxDD=dd_s,
                                 V2_Sharpe=sh_2, V2_CAGR=cg_2, V2_MaxDD=dd_2,
                                 V1_Sharpe=sh_1, V1_CAGR=cg_1, V1_MaxDD=dd_1,
                                 V2f_CAGR=f2cg, V2f_Sharpe=f2sh, V2f_MaxDD=f2dd, V2f_H1=f2H1, V2f_H2=f2H2,
                                 V1f_CAGR=f1cg, V1f_Sharpe=f1sh, V1f_MaxDD=f1dd, V1f_H1=f1H1, V1f_H2=f1H2,
                                 SPYf_CAGR=fscg, SPYf_Sharpe=fssh, SPYf_MaxDD=fsdd, SPYf_H1=fsH1, SPYf_H2=fsH2,
                                 full_pass4b=bool(min(mo[f"m_{b}"] for b in BARS) >= 0)))
    W = pd.DataFrame(recs)
    W.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)
    P(f"    {'unit':<9s}{'OOS Sh':>9s}{'d SPY':>9s}{'d v2':>9s}{'OOS CAGR':>10s}"
      f"{'OOS MaxDD':>11s}{'moved':>8s}")
    for u in UNITS + ["CONTROL"]:
        g = W[W.unit == u]
        P(f"    {u:<9s}{g.OOS_Sharpe.mean():9.4f}{(g.OOS_Sharpe-g.SPY_Sharpe).mean():+9.4f}"
          f"{(g.OOS_Sharpe-g.V2_Sharpe).mean():+9.4f}{g.OOS_CAGR.mean():10.2%}"
          f"{g.OOS_MaxDD.mean():11.2%}{int(g.moved.sum()):5d}/{len(g):<3d}")
    P("\n    FULL SAMPLE and HALVES (PROTOCOL 4), mean over panels x dials:")
    P(f"    {'row':<26s}{'CAGR':>9s}{'Sharpe':>9s}{'MaxDD':>10s}{'H1':>8s}{'H2':>8s}")
    for u in UNITS + ["CONTROL"]:
        g = W[W.unit == u]
        P(f"    {u+' pick':<26s}{g.FULL_CAGR.mean():9.2%}{g.FULL_Sharpe.mean():9.4f}"
          f"{g.FULL_MaxDD.mean():10.2%}{g.FULL_H1.mean():8.3f}{g.FULL_H2.mean():8.3f}")
    for nm, pre in (("RULES v2 baseline (live)", "V2f"), ("RULES v1 (previous)", "V1f"), ("SPY", "SPYf")):
        g = W.drop_duplicates("panel")
        P(f"    {nm:<26s}{g[pre+'_CAGR'].mean():9.2%}{g[pre+'_Sharpe'].mean():9.4f}"
          f"{g[pre+'_MaxDD'].mean():10.2%}{g[pre+'_H1'].mean():8.3f}{g[pre+'_H2'].mean():8.3f}")
    P("    (each baseline row is the mean over the three panels, one value per panel.)")
    P("\n    per panel, OOS 2017-2026 (mean over dials x units):")
    for pan, g in W.groupby("panel"):
        P(f"      {pan:<10s} pick Sh {g.OOS_Sharpe.mean():.4f}  RULES v2 {g.V2_Sharpe.mean():.4f}  "
          f"SPY {g.SPY_Sharpe.mean():.4f}   pick CAGR {g.OOS_CAGR.mean():.2%}  v2 {g.V2_CAGR.mean():.2%}  "
          f"SPY {g.SPY_CAGR.mean():.2%}   pick MaxDD {g.OOS_MaxDD.mean():.2%}  v2 {g.V2_MaxDD.mean():.2%}  "
          f"SPY {g.SPY_MaxDD.mean():.2%}")
    return CHOSEN, accIS, accOOS, W, G_is, G_oos


# ============================================================ KEEP paths
def keep_paths(panels, G):
    P("\n=== KEEP PATHS — both, on EVERY grid point (PROTOCOL 4a and 4b) ===")
    out = []
    for pan, p in panels.items():
        bl = fast_backtest(p.px, rules_v2_weights(p.px)).loc[p.start:]
        h = len(bl) // 2
        _, bH1, _ = _m(bl.iloc[:h]); _, bH2, _ = _m(bl.iloc[h:]); _, _, bdd = _m(bl)
        for dial, cfg in DIALS.items():
            for c in cfg["vals"]:
                r = p.run(dial, c); hh = len(r) // 2
                _, aH1, _ = _m(r.iloc[:hh]); _, aH2, _ = _m(r.iloc[hh:]); _, _, add = _m(r)
                g = G[(G.panel == pan) & (G.dial == dial) & (np.isclose(G.c.astype(float), float(c)))]
                out.append(dict(panel=pan, dial=dial, c=c,
                                pass4a=bool(aH1 > bH1 and aH2 > bH2 and add >= bdd),
                                pass4b=bool(g.pass4b.iloc[0]) if len(g) else None))
    K = pd.DataFrame(out)
    K.to_csv(OUT.with_suffix(".keeppaths.csv"), index=False)
    P(f"  {len(K)} grid points: 4b {int(K.pass4b.sum())}   4a {int(K.pass4a.sum())}   "
      f"BOTH {int((K.pass4a & K.pass4b.astype(bool)).sum())}")
    for pan, g in K.groupby("panel"):
        P(f"    {pan:<10s} 4b {int(g.pass4b.sum()):3d}/{len(g)}   4a {int(g.pass4a.sum()):3d}/{len(g)}")
    P("  Every 4b passer here is a point on an already-committed dial ladder "
      "(gross/band/n on the record's own panels); this run claims NO KEEP.")
    return K


# ============================================================ main
def main():
    t0 = time.time()
    P("IDEA 480 — state the UNIT on every binding-bar claim in the record (lane B, 2026-09-10)")
    P(f"cost {COST:.0f} bps, freq {FREQ}, t+1 execution (PROTOCOL 2)")

    small = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    drop = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])          # idea 118
    small = small.drop(columns=[c for c in small.columns if c in drop])
    panels = {"U56": Panel("U56", load_universe()),
              "B136": Panel("B136", load_universe(broad=True)),
              "SMALL439": Panel("SMALL439", small)}
    for k, v in panels.items(): P(f"  panel {k}: {v.q.shape[1]} names, {len(v.px)} days")

    C = gates(panels)
    PR = part_a(C)

    P("\n  building panel-noise units (idea 253's random sub-panel null, "
      f"{NDRAW} draws of {int(KFRAC*100)}% of each panel) ...")
    NR = null_returns(panels)
    N, SD, IQ = null_scales(panels, NR, "FULL")
    N.to_csv(OUT.with_suffix(".null.csv"), index=False)
    P("  sd_null(bar | panel), FULL sample:")
    P("    " + SD.to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n    "))

    D253, SCAL = part_a2(C, SD)
    A3, PR = part_a3(C, SD, PR)

    G = build_grid(panels, "FULL")
    G = label_units(G, SD, IQ)
    G.to_csv(OUT.with_suffix(".grid.csv"), index=False)
    T = ground_truth(G)
    T.to_csv(OUT.with_suffix(".truth.csv"), index=False)
    A = part_b(G, T)
    if A is not None: A.to_csv(OUT.with_suffix(".accuracy.csv"), index=False)

    CHOSEN, accIS, accOOS, W, G_is, G_oos = part_c(panels, NR, G, SD, IQ)
    K = keep_paths(panels, G)

    P(f"\nVERDICT: see .result.md.  runtime {time.time()-t0:.0f}s")
    OUT.with_suffix(".console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
