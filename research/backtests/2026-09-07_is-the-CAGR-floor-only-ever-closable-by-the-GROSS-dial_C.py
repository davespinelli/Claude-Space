#!/usr/bin/env python3
"""Idea 334 — "is-the-CAGR-floor-only-ever-closable-by-the-GROSS-dial" (lane C, 2026-09-07).

QUESTION (from QUEUE.md).  Idea 42 measured that a de-grossing breadth overlay closes a
4b CAGR-floor miss in 0 of 486 points, and that the only thing that ever closed idea 28's
miss was raising gross.  Census every 4b near-miss in the record whose SOLE failing bar is
CAGR, and ask which of the record's instruments has EVER closed one.  If the answer is
"only the gross dial", PROTOCOL's CAGR floor is a statement about LEVERAGE, not about book
construction, and the leaderboard should carry a `closable-by` column.

WHY THE OBVIOUS METHOD IS NOT USED.  Ideas 387/391 established that mining the record's
PROSE mis-attributes ~7% of the rows it attributes at all.  So the census here is run on
COMMITTED NUMBERS, not sentences: 149 committed grid CSVs carry a machine-written
comma-joined failing-bar column (`fail4b`, `first_fail4b`, `fail4b_10`, ...), whose value
is exactly the bar list this run needs.  A row is a CAGR-ONLY near-miss iff that column
reads exactly `CAGR`.

FOUR LEGS.

  L1  ARCHIVE CENSUS.  Every committed CSV with a failing-bar column.  How many rows are
      CAGR-only near-misses, in how many files, and what is the whole failing-bar
      distribution (so the near-miss class can be sized against its alternatives).

  L2  ARCHIVE SIBLING TEST — has any dial EVER closed one, in the record's own numbers?
      Inside each file, rows that differ in EXACTLY ONE key column are siblings on that
      dial.  For every CAGR-only parent, every sibling on every dial is read: does the
      sibling pass 4b outright?  `bps` is a grouping key, never a dial (comparing a book
      to itself at a different cost rung would be cheating).  Dial column NAMES are mapped
      to instrument families; unmapped names are REPORTED, never guessed at.  The
      DENOMINATOR is reported per family — a dial no script ever swept beside a CAGR-only
      parent cannot close one, and that is a gap in the record, not evidence about the
      instrument.

  L3  FRESH MEASUREMENT (the causal test).  L2 can only see dials the record happened to
      sweep.  So build a controlled corpus of CAGR-only near-miss PARENTS and turn every
      instrument on each of them, one dial at a time, everything else frozen:

        parents   3 panels x 2 book-forms x gross {0.35, 0.50, 0.75}   (18 books)
        arms      GROSS g in {0.85, 1.00}            (no leverage — PROTOCOL rule 2)
                  CONC  n in {5, 10} (+20 for EWALL)
                  CADENCE freq in {D, M, Q}
                  NTBAND m in {20, 40}               (rank-space no-trade band)
                  MABAND b in {0.06, 0.12}
                  VOLSCALE vol_scale=True            (the 1/sqrt(vol20) scaler)
                  VOLCAP max_vol in {0.40, 1.00}     (idea 314's eligibility leg)
                  BREADTH B in {0.30, 0.50} depth 0.50  (idea 42's overlay — the control)

      For every arm: does it close the CAGR floor (CAGR >= 0.70 x SPY CAGR), and does the
      cell become a FULL 4b pass (nothing else broken in the process)?  Both are reported,
      because an instrument that buys CAGR by breaking the drawdown cap has not closed
      anything.

  L4  RULE 8 walk-forward.  For every (parent x instrument), the dial is chosen on
      2008/2010-2016 only and 2017-2026 is read once.  Both choosers are reported (IS
      Sharpe, the record's convention, and IS CAGR, the statistic the question is about).
      OOS CAGR/Sharpe/MaxDD against the parent anchor, RULES v2 and SPY.

TUNED PARAMETERS (max 2, PROTOCOL rule 4): (1) the instrument's dial value, (2) the
parent's gross rung.  Panel, book-form and instrument identity are CENSUS axes — every
level of each is reported, nothing is selected on outcome.  All grid points -> grid.csv.

KEEP PATHS.  Both evaluated on every cell at 0, 10 and 25 bps: 4a against RULES v2 on that
panel; 4b against SPY (Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >=
70% of SPY's).

GATES (asserted and printed).  G1/G2 fast_backtest == engine.backtest on returns AND
turnover at 0 and 25 bps.  G3 band_state(b=0) == px > ma200 where the MA is defined.
G4 NTBAND at m=0 == the plain top-n book on every rebalance day.  G5 the BREADTH overlay
at depth=0 == its own parent to machine precision.  G6 the L1 census reproduces on a
re-read of the same files (determinism of the scan).

CAVEATS.  (1) Every panel is a CURRENT-CONSTITUENT list — SURVIVORSHIP; SMALL439's CAGR
is biased UP, i.e. its CAGR floor is tested in the book's favour.  (2) U56 is 36/56 ETFs
and B136 contains U56, so three panels is not three independent samples.  (3) The gross
dial is capped at 1.00: PROTOCOL rule 2 forbids leverage unless the idea says so, and this
idea does not.  A miss that only 1.5x gross would close is reported as NOT closed.
(4) L2 can only speak about dials the record actually swept beside a CAGR-only parent.
"""
import sys, json, re, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, score, rules_v2_weights, band_state          # noqa
from engine import backtest, metrics, rebalance_mask                             # noqa

SLUG = "2026-09-07_is-the-CAGR-floor-only-ever-closable-by-the-GROSS-dial_C"
OUT = ROOT / "research" / "backtests"
COSTS = [0, 10, 25]
IS_END, OOS_START, WARMUP = "2016-12-31", "2017-01-01", 260
DD_CAP, CAGR_FLOOR = 0.60, 0.70          # PROTOCOL 4b
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); LOG.append(s)


# ============================================================ L1/L2 archive scan helpers
FAILCOL = re.compile(r"^(first_)?fail_?4b(_\d+|_full|_oos)?$", re.I)
METRIC = re.compile(r"cagr|sharpe|maxdd|dd|vol|sortino|calmar|turnover|names|elig|"
                    r"total|years|winrate|ret|regret|share|pval|p_val|corr|mae|"
                    r"median|mean|std|count|frac|pct|breakeven|c_star|equity|"
                    r"^h1$|^h2$|^is_|^oos_|^spy|^v2_|^base", re.I)
NOTDIAL = {"bps", "cost_bps", "cost", "panel", "universe"}   # grouping keys, not dials
# OUTCOME columns must never be treated as a dial: grouping on a verdict and calling the
# other side of the group a "sibling" compares a book to a DIFFERENT book by construction.
OUTCOME = re.compile(r"^(pass|fail|keep|verdict|closes|converts|beats|result|ok|"
                     r"flag|winner|survives|passes|status|decision|reject)", re.I)

FAMILY = [
    ("GROSS",    r"^(g|gross|lev|exposure|scale|gross_rung|g_rung)$"),
    ("CONC",     r"^(n|nfix|n_names|top_?n|k|nn|n_hold|count)$"),
    ("CADENCE",  r"^(freq|cadence|rebal|rebalance|period|f)$"),
    ("NTBAND",   r"^(m|band_m|buffer|x|exit_buffer|e|entry_buffer)$"),
    ("MABAND",   r"^(b|band|half_?width|collar)$"),
    ("VOLSCALE", r"^(vol_?scale|kexp|k_exp|scaler|vs)$"),
    ("VOLCAP",   r"^(max_?vol|volcap|vol_?cap|cap)$"),
    ("BREADTH",  r"^(B|thr|threshold|depth|breadth|q|quantile|gate)$"),
    ("SIGNAL",   r"^(signal|sig|form|book|arm|construction|rule|variant|family|mode)$"),
    ("PANEL",    r"^(panel|universe|sub_?panel)$"),
    # a dial whose VALUE is in this column but whose INSTRUMENT is named elsewhere in the
    # file; it cannot be attributed to a family from the column name alone, so it gets its
    # own bucket rather than being folded into any instrument's count.
    ("DIAL-UNNAMED", r"^(dial|rung|point|value|level|setting|step|idx|index)$"),
]


CADENCE_TOK = {"D", "W", "M", "Q", "A", "B", "2W", "SM", "DAILY", "WEEKLY", "MONTHLY",
               "QUARTERLY", "ANNUAL", "YEARLY"}


def _numvals(vals):
    out = []
    for v in vals:
        try:
            out.append(float(v))
        except (TypeError, ValueError):
            return None
    return out


def family_of(col, vals):
    """Attribute a dial column to an instrument family by NAME, then GATE ON ITS VALUES.

    The name alone is not enough in this record: ideas 359/384 showed `m` and the band
    vocabulary are overloaded across files, and a bare `f` holding {0.5, 0.2, 0.1} is a
    FRACTION, not a rebalance frequency.  A name match whose values are the wrong KIND is
    returned as REJECTED:<family> and counted separately — never folded into the family.
    """
    for fam, rx in FAMILY:
        if not re.match(rx, col, re.I):
            continue
        nv = _numvals(vals)
        if fam == "CADENCE":
            ok = all(str(v).strip().upper() in CADENCE_TOK for v in vals)
        elif fam == "GROSS":
            ok = nv is not None and all(0.05 <= x <= 3.0 for x in nv)
        elif fam == "CONC":
            ok = nv is not None and all(x >= 1 and float(x).is_integer() for x in nv)
        elif fam == "MABAND":
            ok = nv is not None and all(0.0 <= x <= 0.5 for x in nv)
        elif fam in ("NTBAND", "VOLCAP", "BREADTH"):
            ok = nv is not None
        else:
            ok = True
        return fam if ok else f"REJECTED:{fam}"
    return None


def scan_archive():
    """L1 + L2: read every committed CSV, find failing-bar columns, census + sibling test."""
    files = sorted(OUT.glob("*.csv"))
    l1, pairs, unmapped, margins = [], [], {}, []
    for f in files:
        try:
            D = pd.read_csv(f, low_memory=False)
        except Exception:
            continue
        fcols = [c for c in D.columns if FAILCOL.match(str(c))]
        if not fcols:
            continue
        for fc in fcols:
            v = D[fc].fillna("").astype(str).str.strip()
            # normalise: a pass is written "-" or "" by every writer in the record
            is_pass = v.isin(["-", "", "nan", "none", "None", "PASS", "pass"])
            is_cagr_only = v.str.upper() == "CAGR"
            l1.append(dict(file=f.name, col=fc, rows=len(D),
                           cagr_only=int(is_cagr_only.sum()), passes=int(is_pass.sum())))
            if not is_cagr_only.any():
                continue
            # --- L2 sibling test on this file/column.
            # IDENTITY = every column that is not a metric, not an outcome and not a
            # fail-bar list: two rows sharing all of these except ONE are siblings on that
            # one column.  Grouping on the FULL identity (high-cardinality columns
            # included) is what makes "one dial" mean one dial; restricting the group key
            # to low-cardinality columns would let everything else vary inside a group.
            ident = [str(c) for c in D.columns
                     if not (str(c) == fc or FAILCOL.match(str(c))
                             or METRIC.search(str(c)) or OUTCOME.match(str(c)))]
            # DIAL CANDIDATES: identity columns with a small, sweepable set of values.
            keys = [c for c in ident if 2 <= D[c].nunique(dropna=False) <= 12]
            if not keys:
                continue
            cagr_col = next((str(c) for c in D.columns if str(c).upper() == "CAGR"), None)
            # attribute each candidate dial ONCE, on its name AND its value set
            fam_by_col = {c: family_of(c, sorted(D[c].dropna().unique().tolist()))
                          for c in keys}
            W = D.copy()
            W["_fail"] = v; W["_pass"] = is_pass; W["_cagr"] = is_cagr_only
            for c in ident:
                W[c] = W[c].astype(str)
            for dial in keys:
                if dial.lower() in NOTDIAL:
                    continue
                others = [c for c in ident if c != dial]
                if not others:
                    continue
                for _, grp in W.groupby(others, dropna=False, sort=False):
                    par = grp[grp["_cagr"]]
                    if par.empty:
                        continue
                    sib = grp[~grp["_cagr"]]
                    fam = fam_by_col[dial]
                    if fam is None:
                        unmapped[dial] = unmapped.get(dial, 0) + len(par)
                    closed = int(sib["_pass"].sum())
                    # L2b: how BIG a CAGR gap did the archive's closures actually close?
                    if cagr_col is not None and closed:
                        pc = pd.to_numeric(par[cagr_col], errors="coerce").dropna()
                        sc = pd.to_numeric(sib.loc[sib["_pass"], cagr_col],
                                           errors="coerce").dropna()
                        if len(pc) and len(sc):
                            best = sib.loc[sib["_pass"]].assign(
                                _c=pd.to_numeric(sib.loc[sib["_pass"], cagr_col],
                                                 errors="coerce"))
                            margins.append(dict(
                                file=f.name, dial=dial, family=fam or "UNMAPPED",
                                # WHICH dial values: the parent's, and the closing
                                # sibling's.  Needed to tell "the instrument has CAGR
                                # authority" from "the parent sat at a punitive setting".
                                par_val=str(par[dial].mode().iloc[0]),
                                sib_val=str(best.loc[best._c.idxmax(), dial]),
                                par_CAGR=float(pc.median()), sib_CAGR=float(sc.max()),
                                dCAGR=float(sc.max() - pc.median())))
                    pairs.append(dict(file=f.name, col=fc, dial=dial,
                                      family=fam or "UNMAPPED",
                                      parents=len(par), siblings=len(sib),
                                      closing_siblings=closed,
                                      # per-PARENT view: how many CAGR-only parents in
                                      # this group had at least one sibling that passes
                                      parents_with_sib=len(par) if len(sib) else 0,
                                      parents_closed=len(par) if closed else 0))
    return pd.DataFrame(l1), pd.DataFrame(pairs), unmapped, pd.DataFrame(margins)


# ==================================================================== panels & the books
def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    return px[[c for c in px.columns if c not in bad]]


def build_panels():
    return [("U56", load_universe()), ("B136", load_universe(broad=True)),
            ("SMALL439", small_panel())]


_RK = {}


def rank_frame(px, key, b, vol_scale, max_vol):
    """Composite rank inside the 200d MA collar and the vol cap.  Cached per panel/dial."""
    ck = (key, b, vol_scale, max_vol)
    if ck not in _RK:
        s = score(px, vol_scale=vol_scale)[0]
        vol20 = score(px)[2]
        _RK[ck] = s.where(band_state(px, b) & (vol20 < max_vol) & px.notna()).rank(
            axis=1, ascending=False)
    return _RK[ck]


def sel_hard(rk, n):
    return (rk <= n).fillna(False)


def sel_band(rk, n, m, freq):
    """Rank-space no-trade band: enter at rank<=n, hold while rank<=n+m.  m=0 nests
    sel_hard on every rebalance day (gate G4).  State advances on rebalance days only."""
    if m <= 0:
        return sel_hard(rk, n)
    enter, hold = (rk <= n).fillna(False).values, (rk <= n + m).fillna(False).values
    reb = rebalance_mask(rk.index, freq).values
    out = np.zeros(enter.shape, dtype=bool)
    cur = np.zeros(enter.shape[1], dtype=bool)
    for i in range(enter.shape[0]):
        if reb[i] or i == 0:
            cur = (cur & hold[i]) | enter[i]
        out[i] = cur
    return pd.DataFrame(out, index=rk.index, columns=rk.columns)


def w_topn(px, key, n, gross, b, vol_scale, max_vol, m, freq):
    rk = rank_frame(px, key, b, vol_scale, max_vol)
    s = sel_band(rk, n, m, freq).astype(float)
    k = s.sum(axis=1).replace(0, np.nan)
    return gross * s.div(k, axis=0).fillna(0.0)


def w_ewall(px, key, n, gross, b, vol_scale, max_vol, m, freq):
    """RULES v2 form: hold every name inside the collar (and vol cap) at gross/N, gated
    weight -> CASH.  n=None means no top-n cap; n set applies the CONC dial."""
    rk = rank_frame(px, key, b, vol_scale, max_vol)
    elig = rk.notna()
    sel = elig if n is None else sel_band(rk, n, m, freq)
    s = sel.astype(float)
    denom = px.notna().sum(axis=1).replace(0, np.nan)      # N = instruments PRICED (v2)
    if n is None:
        return gross * s.div(denom, axis=0).fillna(0.0)
    k = s.sum(axis=1).replace(0, np.nan)
    return gross * s.div(k, axis=0).fillna(0.0)


def breadth_series(px):
    """CAUSAL cross-sectional breadth: share of PRICED names above their own 200d MA."""
    above = (px > px.rolling(200).mean()) & px.notna()
    return (above.sum(axis=1) / px.notna().sum(axis=1).replace(0, np.nan)).fillna(0.0)


def apply_breadth(w, px, B, depth):
    if B is None:
        return w
    fire = breadth_series(px) < B
    return w.mul(np.where(fire, 1.0 - depth, 1.0), axis=0)


# ========================================================================== the machinery
def fast_backtest(px, w, freq):
    """Clone of engine.backtest returning GROSS returns + turnover + held-name count."""
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    nT, nC = rets.shape
    held = np.empty((nT, nC)); turn = np.zeros(nT); cur = np.zeros(nC)
    for i in range(nT):
        if mask[i] or i == 0:
            new = wt[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        growth = cur * (1 + rets[i]); tot = growth.sum() + (1 - cur.sum())
        if tot > 0: cur = growth / tot
    idx = px.index
    return (pd.Series(np.nansum(held * rets, axis=1), index=idx),
            pd.Series(turn, index=idx), pd.Series((held > 0).sum(axis=1), index=idx))


def stats(gross_r, turn, bps, start):
    r = (gross_r - turn * bps / 1e4).loc[start:]
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    mo, mi = metrics(r.loc[OOS_START:]), metrics(r.loc[:IS_END])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"],
                H2=m2["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                OOS_MaxDD=mo["MaxDD"], IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"])


def keeps(s, v2, spy):
    a = (s["H1"] > v2["H1"]) and (s["H2"] > v2["H2"]) and (s["MaxDD"] >= v2["MaxDD"])
    fb = []
    if not s["H1"] > spy["H1"]: fb.append("H1")
    if not s["H2"] > spy["H2"]: fb.append("H2")
    if not s["OOS_Sharpe"] > spy["OOS_Sharpe"]: fb.append("OOS")
    if not s["MaxDD"] >= -DD_CAP * abs(spy["MaxDD"]): fb.append("DD")
    if not s["CAGR"] >= CAGR_FLOOR * spy["CAGR"]: fb.append("CAGR")
    return a, len(fb) == 0, ",".join(fb) if fb else "-"


# ---------------------------------------------------------------- the arm specification
GROSSES = [0.35, 0.50, 0.75]
BASE = dict(b=0.03, vol_scale=False, max_vol=0.60, m=0, freq="W", B=None, depth=0.0)


def arms_for(form):
    """One dial off the parent per arm.  (family, label, override-dict)."""
    A = [("GROSS", "g=0.85", dict(gross=0.85)), ("GROSS", "g=1.00", dict(gross=1.00))]
    A += [("CONC", "n=5", dict(n=5)), ("CONC", "n=10", dict(n=10))]
    if form == "EWALL":
        A += [("CONC", "n=20", dict(n=20))]
    A += [("CADENCE", f"freq={f}", dict(freq=f)) for f in ("D", "M", "Q")]
    if form == "MARS20":
        A += [("NTBAND", "m=20", dict(m=20)), ("NTBAND", "m=40", dict(m=40))]
    A += [("MABAND", "b=0.06", dict(b=0.06)), ("MABAND", "b=0.12", dict(b=0.12))]
    A += [("VOLSCALE", "volscale=on", dict(vol_scale=True))]
    A += [("VOLCAP", "maxvol=0.40", dict(max_vol=0.40)),
          ("VOLCAP", "maxvol=1.00", dict(max_vol=1.00))]
    A += [("BREADTH", "B=0.30,d=0.50", dict(B=0.30, depth=0.50)),
          ("BREADTH", "B=0.50,d=0.50", dict(B=0.50, depth=0.50))]
    return A


def run_book(px, key, form, gross, cfg):
    n = cfg.get("n", 20 if form == "MARS20" else None)
    kw = dict(key=key, n=n, gross=gross, b=cfg["b"], vol_scale=cfg["vol_scale"],
              max_vol=cfg["max_vol"], m=cfg["m"], freq=cfg["freq"])
    w = (w_topn if form == "MARS20" else w_ewall)(px, **kw)
    w = apply_breadth(w, px, cfg["B"], cfg["depth"])
    return fast_backtest(px, w, cfg["freq"])


# ==================================================================================== main
def main():
    t0 = time.time()
    P(f"=== idea 334 — is the CAGR floor only ever closable by the GROSS dial?  ({SLUG}) ===")
    P("Census on COMMITTED NUMBERS (machine-written fail-bar columns), not prose —")
    P("        ideas 387/391 showed the record's prose mis-attributes ~7% of what it attributes.")
    P("Tuned params (2): the instrument's dial value, and the parent's gross rung.")
    P("        Panel / book-form / instrument identity are census axes, fully reported.")
    P(f"4b bars: Sharpe > SPY in H1, H2 and OOS; MaxDD >= -{DD_CAP:.2f}x|SPY DD|; "
      f"CAGR >= {CAGR_FLOOR:.2f}x SPY CAGR.")

    # ------------------------------------------------------------------ L1 + L2
    P("\n[L1] ARCHIVE CENSUS — every committed CSV carrying a machine-written fail-bar column")
    L1, PR, unmapped, MG = scan_archive()
    L1b, PRb, _, MGb = scan_archive()                                # G6 determinism
    g6 = (L1.equals(L1b) and PR.equals(PRb) and MG.equals(MGb))
    P(f"    G6 scan is deterministic on a re-read: {g6}")
    assert g6
    L1.to_csv(OUT / f"{SLUG}.census.csv", index=False)
    tot_rows, tot_cagr = int(L1["rows"].sum()), int(L1["cagr_only"].sum())
    P(f"    {len(L1)} (file, column) fail-bar sources in {L1.file.nunique()} files, "
      f"{tot_rows} rows")
    P(f"    CAGR-ONLY near-misses: {tot_cagr} rows ({tot_cagr/max(tot_rows,1):.2%}) "
      f"in {int((L1.cagr_only > 0).sum())} sources / "
      f"{L1[L1.cagr_only > 0].file.nunique()} files")
    P(f"    outright 4b passes in the same corpus: {int(L1['passes'].sum())} rows "
      f"({L1['passes'].sum()/max(tot_rows,1):.2%})")
    P("    top files by CAGR-only count:")
    P(L1[L1.cagr_only > 0].sort_values("cagr_only", ascending=False)
      .head(12)[["file", "col", "rows", "cagr_only", "passes"]].to_string(index=False))

    P("\n[L2] ARCHIVE SIBLING TEST — for a CAGR-only parent, does a one-dial sibling PASS 4b?")
    if PR.empty:
        P("    no sibling structure recoverable — SKIPPED")
    else:
        PR.to_csv(OUT / f"{SLUG}.siblings.csv", index=False)
        fam = PR.groupby("family").agg(
            files=("file", "nunique"), dials=("dial", "nunique"),
            parent_rows=("parents", "sum"), sibling_rows=("siblings", "sum"),
            closing=("closing_siblings", "sum"),
            par_with_sib=("parents_with_sib", "sum"),
            par_closed=("parents_closed", "sum")).reset_index()
        fam["close_rate"] = fam["closing"] / fam["sibling_rows"].replace(0, np.nan)
        fam["parent_close_rate"] = fam["par_closed"] / fam["par_with_sib"].replace(0, np.nan)
        fam = fam.sort_values("par_closed", ascending=False)
        P(fam.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        P("    parent_close_rate = share of CAGR-only parents that HAVE a one-dial sibling")
        P("    on that family and whose sibling passes 4b — the 'has it EVER closed one'")
        P("    statistic.  DIAL-UNNAMED = the dial value is in the file but the instrument")
        P("    is named in another column, so it cannot be attributed from the name alone.")
        P(f"    UNMAPPED dial names (reported, not guessed): "
          f"{dict(sorted(unmapped.items(), key=lambda kv: -kv[1])[:12]) if unmapped else '{}'}")
        P("    NOTE the denominator: a family with sibling_rows=0 was never swept beside a")
        P("    CAGR-only parent in this record — that is a gap in the archive, not a")
        P("    measurement about the instrument.  L3 closes exactly that gap.")

    P("\n[L2b] HOW BIG A GAP DID THE ARCHIVE'S CLOSURES ACTUALLY CLOSE?")
    P("      (closing sibling's CAGR minus its CAGR-only parent's, where the file writes a")
    P("      CAGR column — the size of the miss each instrument was asked to cover)")
    if MG.empty:
        P("      no closure carried a readable CAGR column — SKIPPED")
    else:
        MG.to_csv(OUT / f"{SLUG}.margins.csv", index=False)
        a = MG.groupby("family").agg(
            closures=("dCAGR", "size"), med_dCAGR=("dCAGR", "median"),
            p90_dCAGR=("dCAGR", lambda s: float(np.percentile(s, 90))),
            max_dCAGR=("dCAGR", "max")).reset_index()
        P(a.sort_values("med_dCAGR", ascending=False)
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        P("\n      WHICH dial values the archive's closures move BETWEEN (top families):")
        for famname in ("CADENCE", "CONC", "GROSS", "MABAND", "NTBAND", "VOLSCALE"):
            sub = MG[MG.family == famname]
            if sub.empty:
                continue
            mv = (sub.groupby(["par_val", "sib_val"]).dCAGR
                  .agg(["size", "median"]).sort_values("size", ascending=False).head(4))
            P(f"        {famname:9s} " + "; ".join(
                f"{p}->{s} (n={int(r['size'])}, med {r['median']*100:+.2f}pp)"
                for (p, s), r in mv.iterrows()))

    # ------------------------------------------------------------------ panels
    P("\n[0] PANELS")
    panels = build_panels()
    for nm, px in panels:
        P(f"    {nm:9s} {px.shape[1]:>4d} cols  {px.index[0].date()} -> "
          f"{px.index[-1].date()}  ({len(px)} rows)")

    # ------------------------------------------------------------------ gates
    P("\n[0b] GATES")
    u = dict(panels)["U56"]
    wg = w_topn(u, "U56", 20, 0.75, 0.03, False, 0.60, 0, "W")
    gr, tn, _ = fast_backtest(u, wg, "W")
    for bps in (0, 25):
        eng = backtest(u, wg, cost_bps=bps, freq="W")
        d1 = float((eng["returns"] - (gr - tn * bps / 1e4)).abs().max())
        d2 = float((eng["turnover"] - tn).abs().max())
        P(f"    G1/G2 cost_bps={bps:>2}: |d returns| {d1:.3e}  |d turnover| {d2:.3e}")
        assert d1 < 1e-12 and d2 < 1e-12
    ma = u.rolling(200).mean(); defined = ma.notna() & u.notna()
    d3 = int(((band_state(u, 0.0) != (u > ma)) & defined).values.sum())
    P(f"    G3 band_state(b=0) vs px>ma200 where defined: {d3}/{int(defined.values.sum())}")
    assert d3 / max(int(defined.values.sum()), 1) < 1e-4
    rk = rank_frame(u, "U56", 0.03, False, 0.60)
    reb = rebalance_mask(u.index, "W").values
    d4 = int((sel_band(rk, 20, 0, "W").values[reb] != sel_hard(rk, 20).values[reb]).sum())
    P(f"    G4 sel_band(m=0) vs sel_hard on rebalance days: {d4} disagreements")
    assert d4 == 0
    d5 = float((apply_breadth(wg, u, 0.30, 0.0) - wg).abs().values.max())
    P(f"    G5 breadth overlay at depth=0 vs parent: |dw| {d5:.3e}")
    assert d5 < 1e-15

    # ------------------------------------------------------------------ comparands
    P("\n[1] COMPARANDS per panel @10 bps (SPY and RULES v2 live)")
    comp = {}
    for nm, px in panels:
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        h = len(spy) // 2
        sp = dict(CAGR=metrics(spy)["CAGR"], Sharpe=metrics(spy)["Sharpe"],
                  MaxDD=metrics(spy)["MaxDD"], H1=metrics(spy.iloc[:h])["Sharpe"],
                  H2=metrics(spy.iloc[h:])["Sharpe"],
                  OOS_Sharpe=metrics(spy.loc[OOS_START:])["Sharpe"],
                  OOS_CAGR=metrics(spy.loc[OOS_START:])["CAGR"],
                  OOS_MaxDD=metrics(spy.loc[OOS_START:])["MaxDD"])
        v2r = backtest(px, rules_v2_weights(px), cost_bps=10, freq="W")["returns"]
        v2 = stats(v2r, pd.Series(0.0, index=px.index), 0, start)
        comp[nm] = (sp, v2, start)
        P(f"    {nm:9s} SPY CAGR {sp['CAGR']:7.2%} Sharpe {sp['Sharpe']:.3f} "
          f"DD {sp['MaxDD']:7.2%} H1/H2 {sp['H1']:.3f}/{sp['H2']:.3f} "
          f"OOS {sp['OOS_Sharpe']:.3f} | 4b bars: CAGR>={CAGR_FLOOR*sp['CAGR']:.2%}, "
          f"DD>={-DD_CAP*abs(sp['MaxDD']):.2%}")
        P(f"    {'':9s} v2  CAGR {v2['CAGR']:7.2%} Sharpe {v2['Sharpe']:.3f} "
          f"DD {v2['MaxDD']:7.2%} H1/H2 {v2['H1']:.3f}/{v2['H2']:.3f} "
          f"OOS {v2['OOS_Sharpe']:.3f}")

    # ------------------------------------------------------------------ L3 the grid
    P("\n[L3] FRESH MEASUREMENT — parents, then one dial at a time")
    rows = []
    for nm, px in panels:
        sp, v2, start = comp[nm]
        yrs_den = None
        for form in ("MARS20", "EWALL"):
            for g in GROSSES:
                specs = [("PARENT", "parent", {})] + arms_for(form)
                for family, label, ov in specs:
                    cfg = dict(BASE); cfg.update({k: v for k, v in ov.items() if k != "gross"})
                    gg = ov.get("gross", g)
                    if "n" in ov: cfg["n"] = ov["n"]
                    g_r, t_r, nn = run_book(px, nm, form, gg, cfg)
                    yrs = len(t_r.loc[start:]) / 252.0
                    for bps in COSTS:
                        s = stats(g_r, t_r, bps, start)
                        a, b4, fb = keeps(s, v2, sp)
                        rows.append(dict(
                            panel=nm, form=form, parent_gross=g, family=family,
                            arm=label, bps=bps, **s,
                            names=float(nn.loc[start:].mean()),
                            cash_days=float((nn.loc[start:] == 0).mean()),
                            turnover=float(t_r.loc[start:].sum() / yrs),
                            spy_CAGR=sp["CAGR"], spy_Sharpe=sp["Sharpe"],
                            spy_MaxDD=sp["MaxDD"], spy_OOS_CAGR=sp["OOS_CAGR"],
                            spy_OOS_Sharpe=sp["OOS_Sharpe"],
                            cagr_floor=CAGR_FLOOR * sp["CAGR"],
                            oos_cagr_floor=CAGR_FLOOR * sp["OOS_CAGR"],
                            pass4a=a, pass4b=b4, fail4b=fb))
        P(f"    {nm} done  ({time.time()-t0:.0f}s)")
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{SLUG}.grid.csv", index=False)
    P(f"    grid: {len(G)} rows -> {SLUG}.grid.csv")

    # ------------------------------------------------------------- the parent population
    P("\n[L3a] THE PARENT POPULATION @10 bps — which parents are CAGR-ONLY near-misses?")
    par = G[(G.family == "PARENT") & (G.bps == 10)].copy()
    par["cagr_only"] = par.fail4b == "CAGR"
    P(par[["panel", "form", "parent_gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
           "OOS_Sharpe", "cagr_floor", "fail4b", "pass4b"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n    CAGR-only near-miss parents: {int(par.cagr_only.sum())} of {len(par)}")
    P("    parent fail-bar distribution: " +
      str(par.fail4b.value_counts().to_dict()))

    keyset = par[par.cagr_only][["panel", "form", "parent_gross"]]
    if keyset.empty:
        P("\n    !! NO CAGR-only parents at 10 bps — the causal leg has no population.")
    ks = set(map(tuple, keyset.values))

    # ------------------------------------------------------------- THE HEADLINE
    P("\n[L3b] THE QUESTION — for each CAGR-only parent, does the instrument close the floor?")
    P("      'closes' = CAGR >= 0.70 x SPY CAGR.  'converts' = the whole 4b passes.")
    head = []
    for bps in COSTS:
        sub = G[(G.bps == bps) & G.apply(
            lambda r: (r.panel, r.form, r.parent_gross) in ks, axis=1)]
        pars = sub[sub.family == "PARENT"].set_index(["panel", "form", "parent_gross"])
        arms = sub[sub.family != "PARENT"]
        for _, r in arms.iterrows():
            p = pars.loc[(r.panel, r.form, r.parent_gross)]
            head.append(dict(bps=bps, panel=r.panel, form=r.form,
                             parent_gross=r.parent_gross, family=r.family, arm=r.arm,
                             parent_CAGR=p.CAGR, CAGR=r.CAGR, dCAGR=r.CAGR - p.CAGR,
                             floor=r.cagr_floor,
                             closes=bool(r.CAGR >= r.cagr_floor),
                             converts=bool(r.pass4b), fail4b=r.fail4b,
                             dSharpe=r.Sharpe - p.Sharpe, dMaxDD=r.MaxDD - p.MaxDD))
    H = pd.DataFrame(head)
    H.to_csv(OUT / f"{SLUG}.headline.csv", index=False)
    if not H.empty:
        for bps in COSTS:
            hh = H[H.bps == bps]
            agg = hh.groupby("family").agg(
                points=("closes", "size"), closes=("closes", "sum"),
                converts=("converts", "sum"),
                med_dCAGR=("dCAGR", "median"), best_dCAGR=("dCAGR", "max"),
                med_dSharpe=("dSharpe", "median"),
                med_dMaxDD=("dMaxDD", "median")).reset_index()
            agg["close_rate"] = agg["closes"] / agg["points"]
            P(f"\n    @{bps} bps  ({len(hh)} instrument points over "
              f"{hh.groupby(['panel','form','parent_gross']).ngroups} CAGR-only parents)")
            P(agg.sort_values("closes", ascending=False)
              .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        P("\n    [L3c] CAGR AUTHORITY — the largest CAGR move each instrument can produce")
        P("          off these parents, against the gap it is being asked to cover.")
        gap = (par[par.cagr_only].cagr_floor - par[par.cagr_only].CAGR)
        P(f"          parent gaps to the floor (pp/yr): min {gap.min()*100:.2f}  "
          f"median {gap.median()*100:.2f}  max {gap.max()*100:.2f}")
        for bps in COSTS:
            au = H[H.bps == bps].groupby("family").dCAGR.max().sort_values(ascending=False)
            P(f"          @{bps:>2} bps authority (max dCAGR, pp/yr): " +
              str({k: round(v * 100, 2) for k, v in au.items()}))
        P("\n    Every arm at 10 bps (ALL grid points, per parent):")
        P(H[H.bps == 10][["panel", "form", "parent_gross", "family", "arm", "parent_CAGR",
                          "CAGR", "dCAGR", "floor", "closes", "converts", "fail4b"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------------ 4a / 4b tallies
    P("\n[2] BOTH KEEP PATHS over the whole grid")
    for bps in COSTS:
        gg = G[G.bps == bps]
        P(f"    @{bps:>2} bps: 4a {int(gg.pass4a.sum())}/{len(gg)}   "
          f"4b {int(gg.pass4b.sum())}/{len(gg)}")
    g10 = G[G.bps == 10]
    bars = {}
    for v in g10[~g10.pass4b].fail4b:
        for b in v.split(","):
            bars[b] = bars.get(b, 0) + 1
    P(f"    failing bars @10 bps (all cells): "
      f"{dict(sorted(bars.items(), key=lambda kv: -kv[1]))}")
    if g10.pass4b.any():
        best = g10[g10.pass4b].sort_values("Sharpe", ascending=False).iloc[0]
        P(f"    best 4b cell @10 bps: {best.panel}/{best.form}/g={best.parent_gross}/"
          f"{best.arm}  CAGR {best.CAGR:.2%} Sharpe {best.Sharpe:.3f} "
          f"DD {best.MaxDD:.2%} H1/H2 {best.H1:.3f}/{best.H2:.3f} OOS {best.OOS_Sharpe:.3f}")

    # ------------------------------------------------------------------ L4 rule 8
    P("\n[L4] RULE 8 WALK-FORWARD — dial chosen on <=2016 only, 2017-2026 read once")
    P("     Two choosers reported: IS Sharpe (record convention) and IS CAGR (the")
    P("     statistic this question is about).  Anchor = the parent, same window.")
    wf = []
    for (pnl, form, g), _ in G[G.bps == 10].groupby(["panel", "form", "parent_gross"]):
        sp, v2, _ = comp[pnl]
        sub = G[(G.bps == 10) & (G.panel == pnl) & (G.form == form) &
                (G.parent_gross == g)]
        anch = sub[sub.family == "PARENT"].iloc[0]
        for fam, arms in sub[sub.family != "PARENT"].groupby("family"):
            for chooser in ("IS_Sharpe", "IS_CAGR"):
                pick = arms.loc[arms[chooser].idxmax()]
                wf.append(dict(panel=pnl, form=form, parent_gross=g, family=fam,
                               chooser=chooser, pick=pick.arm,
                               OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                               OOS_MaxDD=pick.OOS_MaxDD,
                               anchor_OOS_CAGR=anch.OOS_CAGR,
                               anchor_OOS_Sharpe=anch.OOS_Sharpe,
                               anchor_OOS_MaxDD=anch.OOS_MaxDD,
                               v2_OOS_Sharpe=v2["OOS_Sharpe"], v2_OOS_CAGR=v2["OOS_CAGR"],
                               spy_OOS_Sharpe=sp["OOS_Sharpe"], spy_OOS_CAGR=sp["OOS_CAGR"],
                               best_OOS_Sharpe=arms.OOS_Sharpe.max(),
                               oos_floor=CAGR_FLOOR * sp["OOS_CAGR"],
                               oos_closes=bool(pick.OOS_CAGR >=
                                               CAGR_FLOOR * sp["OOS_CAGR"]),
                               parent_cagr_only=(pnl, form, g) in ks))
    WF = pd.DataFrame(wf)
    WF["regret"] = WF.best_OOS_Sharpe - WF.OOS_Sharpe
    WF["beats_anchor"] = WF.OOS_Sharpe > WF.anchor_OOS_Sharpe
    WF["beats_spy"] = WF.OOS_Sharpe > WF.spy_OOS_Sharpe
    WF["beats_v2"] = WF.OOS_Sharpe > WF.v2_OOS_Sharpe
    WF.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    for chooser in ("IS_Sharpe", "IS_CAGR"):
        w = WF[WF.chooser == chooser]
        P(f"\n    chooser = {chooser}  ({len(w)} parent x family cells)")
        P(f"      beats own parent anchor OOS Sharpe {int(w.beats_anchor.sum())}/{len(w)}"
          f" | beats SPY {int(w.beats_spy.sum())}/{len(w)}"
          f" | beats RULES v2 {int(w.beats_v2.sum())}/{len(w)}"
          f" | mean regret {w.regret.mean():+.4f}")
        a = w.groupby("family").agg(
            cells=("pick", "size"), oos_closes=("oos_closes", "sum"),
            med_OOS_CAGR=("OOS_CAGR", "median"), med_OOS_Sharpe=("OOS_Sharpe", "median"),
            med_regret=("regret", "median")).reset_index()
        P(a.sort_values("oos_closes", ascending=False)
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    wcag = WF[WF.parent_cagr_only]
    if not wcag.empty:
        P("\n    restricted to the CAGR-ONLY parents (the population the question is about):")
        for chooser in ("IS_Sharpe", "IS_CAGR"):
            w = wcag[wcag.chooser == chooser]
            a = w.groupby("family").agg(
                cells=("pick", "size"), oos_closes=("oos_closes", "sum"),
                med_OOS_CAGR=("OOS_CAGR", "median"),
                med_OOS_Sharpe=("OOS_Sharpe", "median")).reset_index()
            P(f"      chooser={chooser}: OOS CAGR floor closed by family -> " +
              str({r.family: f"{int(r.oos_closes)}/{int(r.cells)}"
                   for _, r in a.iterrows()}))

    P(f"\n[done] {time.time()-t0:.0f}s")
    (OUT / f"{SLUG}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
