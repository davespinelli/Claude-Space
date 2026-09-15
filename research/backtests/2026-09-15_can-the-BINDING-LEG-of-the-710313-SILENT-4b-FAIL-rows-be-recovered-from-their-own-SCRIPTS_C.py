#!/usr/bin/env python3
"""Idea 952 (lane C, 2026-09-15) -- can the BINDING LEG of the 710,313 SILENT 4b FAIL rows be
recovered from their own SCRIPTS?

THE QUESTION (queue, 2026-09-15)
  Idea 944's census found 710,313 of 835,403 committed 4b FAIL rows (85.0%) carry no recoverable
  binding leg, "so the record's 4b failures are in the main unadjudicable as to WHY they failed".
  Recover the leg from each file's own committed columns and its sibling statistics, measure what
  share is recoverable AT ALL, and price the reporting clause that would have prevented it.

WHAT 944's CENSUS ACTUALLY LOOKED AT (the thing this run widens)
  944 read a row's binding leg from exactly two places: a column literally NAMED `fail4b`, or one
  of two exact 5-column leg-boolean sets (L1_H1..L5_CAGRfloor / L1_H1..L5_CAGR).  Every other row
  was booked UNRECOVERABLE.  That is a statement about ONE COLUMN NAME, not about whether the
  record reported the leg.  This run asks how much of the 85% is genuine silence and how much is
  a deaf census.

THE RECOVERY LADDER (TUNED 1 -- 5 nested levels, ALL reported, never merged)
  R0 AS-BUILT    944's rule verbatim: a column named `fail4b`, or a READ_SET of leg booleans.
  R1 +ALPHABET   any OTHER column whose values are 4b fail-strings in the canonical token
                 alphabet (`failing`, `f4b`, `fail_4b`, `OOS_fails`, `bind4b`, `binding`, ...).
                 A column qualifies only if >= 90% of its non-empty values on that file's FAIL
                 rows parse (VALIDATE_SHARE) -- the name alone is never enough.
  R2 +LEGCOLS    per-leg boolean or MARGIN column families in any spelling
                 (leg_H1..leg_CAGR, L1_H1.., m_H1/m_H2/m_OOS/m_DD/m_CAGR; margin < 0 = leg fails).
  R3 +STATS/IN-FILE SPY   recompute all five 4b legs from the row's own statistics against the
                 SPY comparands committed IN THE SAME FILE.
  R4 +STATS/PANEL SPY     same, with SPY's comparand recomputed here from the panel named by the
                 file (or its script's own panel constant) -- the "recover it from its own
                 SCRIPT" leg of the idea.
  Each rung is reported twice: FULL (all five legs decided) and NAMED (>= 1 leg decided AND at
  least one decided leg FAILS, i.e. a binding leg is named even if the signature is incomplete).

TUNED 2 -- CLAIM SET, 2 levels, both reported, never merged
  ROW-WEIGHTED   every committed 4b FAIL row counts once -- 944's own population and the one its
                 85.0% headline is computed on.
  FILE-WEIGHTED  every committed CSV counts once (a file is RECOVERED when >= 50% of its FAIL
                 rows get a named leg).  A row-weighted headline can be carried by a handful of
                 200k-row grid dumps; the file-weighted one cannot.
  (A third cut, "cited by LEADERBOARD.md", was pre-registered as the second level and is
  reported below, but it is NOT used as a level: 96% of the record's CSVs sit under a cited
  stem, so it does not partition anything.)

REPORTED AXES (nothing fitted on them)
  RUNG x CLAIM SET x per-file mapping (dumped in full); leg-share distributions R0 vs recovered;
  the record-time split (files dated <= 2026-09-08 vs later); cost rungs 0/10/25/50 in the
  walk-forward.

PRIOR ART IN THE RECORD (read before this run was designed, and not repeated here)
  Idea 161 (2026-09-08, cloud) already reconstructed 4b verdicts from the `m_H1..m_CAGR` MARGIN
  columns on *.grid.csv, behind a gate that the five bars must reproduce the committed pass4b
  on EVERY row of a file or the file is rejected.  That gate is stricter than a mean agreement
  rate and is adopted here as the per-file fidelity statistic (H_FIDELITY reports both).

PRE-REGISTERED BARS (fixed before any number was read; both directions reported)
  H_RECOVER  the ladder recovers a binding leg for >= 50% of the rows 944 booked UNRECOVERABLE.
             Below that, 944's "in the main unadjudicable" stands as written.
  H_FIDELITY where a row is recoverable at BOTH a text rung (R0-R2) and a statistics rung
             (R3-R4), the reconstructed signature equals the committed one on >= 90% of rows.
             This is the credibility of every recovered leg; a low rate disqualifies R3/R4.
  H_BIAS     the L4_DD-alone and L5_CAGR-alone shares move by <= 5 pp between the R0-readable
             rows and the newly recovered rows.  If they move MORE, the record's published
             leg-share claims (944's 68.8% CAGR / 58.3% DD) are a biased 15% sample.
  H_CLAIMSET the headline recoverable share moves by <= 10 pp between ROW- and FILE-WEIGHTED.
  H_WFRULE   an alphabet learned ONLY on files dated <= 2026-09-08 recovers >= 90% as large a
             share on LATER files -- the recovery rule generalises rather than being fitted to
             the residue it was built on.
  H_WF       (PROTOCOL rule 8, REQUIRED) the standing candidate re-run with the book chosen on
             2009-2016 ALONE, 2017-2026 read ONCE, both KEEP paths, against SPY and RULES v2,
             with EVERY committed row naming its binding leg (the clause, demonstrated).

GATES (printed before any result number)
  G1 CROSS-RUN   this run's R0 rung reproduces 944's committed census: 835,403 WIDE rows /
                 710,313 unrecoverable / L4_DD-alone 15.8% of the READ rows, up to files
                 committed after 944 ran (the drift is printed, not absorbed).
  G2 NESTING     the rungs are nested: recovery(R0) <= R1 <= R2 <= R3 <= R4 on every file.
  G3 VALIDATION  every column admitted at R1 parses on >= 90% of its non-empty FAIL values;
                 the rejected candidates are listed, not dropped silently.
  G4 DETERMINISM the census re-run on a re-read of the same files gives identical counts.
  G5 SELF-SEE    the census sees idea 944's OWN committed rows (its .census.csv is a count
                 table, its .grid.csv/.cells.csv carry pass4b) -- a census blind to the run it
                 audits is broken.
  G6 WF ENGINE   the fast runner == engine.backtest on returns and turnover for the standing
                 candidate at 10 bps.

LIMITS
  This is a census of the record's TEXT and of statistics the record itself committed.  It
  inherits every bias of the runs it reads, it is not a sample from a population, and no p-value
  is claimed for any share.  A recovered leg is only as good as G3/H_FIDELITY says it is.  The
  panel comparand at R4 assumes the file's window is PROTOCOL's (FULL from index[260], halves of
  that, OOS from 2017-01-01); rows whose run used another window are recovered WRONG and the
  fidelity rate is the measurement of how often that happens.
"""
import os, sys, re, time, gzip, warnings, collections
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "research" / "backtests"
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, score           # noqa: E402
from engine import backtest, rebalance_mask                           # noqa: E402

COST0, LAG, WARMUP = 10.0, 1, 260
VOLCAP, GROSS0, BAND0 = 0.60, 0.75, 0.03
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COSTS = [0.0, 10.0, 25.0, 50.0]
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]
RUNGS = ["R0_ASBUILT", "R1_ALPHABET", "R2_LEGCOLS", "R3_STATS_INFILE", "R4_STATS_PANEL"]
VALIDATE_SHARE = 0.90
RECORD_SPLIT = "2026-09-08"

# idea 944 (cloud run, tree 574d5b8) committed census headline
PUB_WIDE, PUB_UNREC, PUB_READ = 835403, 710313, 125090
PUB_DD_ALONE = 0.158

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ==================================================================================== ALPHABET
TOKEN = {"H1": "L1_H1", "H2": "L2_H2", "OOS": "L3_OOS", "DD": "L4_DD", "CAGR": "L5_CAGR",
         "L1_H1": "L1_H1", "L2_H2": "L2_H2", "L3_OOS": "L3_OOS", "L4_DD": "L4_DD",
         "L5_CAGR": "L5_CAGR", "L4_DDCAP": "L4_DD", "L5_CAGRFLOOR": "L5_CAGR",
         "DDCAP": "L4_DD", "CAGRFLOOR": "L5_CAGR", "DD_CAP": "L4_DD", "CAGR_FLOOR": "L5_CAGR",
         "L1": "L1_H1", "L2": "L2_H2", "L3": "L3_OOS", "L4": "L4_DD", "L5": "L5_CAGR",
         "MAXDD": "L4_DD", "DRAWDOWN": "L4_DD", "H1SHARPE": "L1_H1", "H2SHARPE": "L2_H2",
         "OOSSHARPE": "L3_OOS", "OOS_SHARPE": "L3_OOS", "WF": "L3_OOS", "OOSSH": "L3_OOS",
         "SH1": "L1_H1", "SH2": "L2_H2", "HALF1": "L1_H1", "HALF2": "L2_H2", "RET": "L5_CAGR",
         "CAGRFLOOR70": "L5_CAGR", "FLOOR": "L5_CAGR", "CAP": "L4_DD"}
SEPS = "+|/;&, "
PASSTOK = {"-", "", "NONE", "NAN", "PASS", "OK", "TRUE", "FALSE", "0", "NA", "PASS4B", "-NONE-"}


def parse_sig(v):
    """One committed fail-string -> ('fail', canonical signature) / ('pass', '-') / ('bad', raw)."""
    s = str(v).strip()
    if s.upper() in PASSTOK:
        return "pass", "-"
    t = s.upper()
    for ch in SEPS:
        t = t.replace(ch, ",")
    toks = [x for x in (y.strip() for y in t.split(",")) if x]
    if not toks:
        return "pass", "-"
    out = []
    for tk in toks:
        hit = TOKEN.get(tk) or TOKEN.get(tk.replace("_", "")) or TOKEN.get(tk.replace("-", "_"))
        if hit is None:
            return "bad", s[:40]
        out.append(hit)
    return "fail", "+".join(sorted(set(out), key=LEGS.index))


def sig_from_flags(fail_flags):
    """dict leg -> True(fails) / False(passes) / None(undecided) -> (signature, n_decided)."""
    dec = {k: v for k, v in fail_flags.items() if v is not None}
    f = [k for k in LEGS if dec.get(k) is True]
    return ("+".join(f) if f else "-"), len(dec)


# ============================================================ column-role detection (per file)
PCOLS = ("pass4b", "OOS_pass4b", "pass_4b")           # 944's population definition, unchanged
READ_SETS = [["L1_H1", "L2_H2", "L3_OOS", "L4_DDcap", "L5_CAGRfloor"],
             ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]]
NOT_FAILSTR = {"n_fail", "nfail", "nfails", "n_failing", "fail_4a", "f4a", "fails_4a",
               "failed", "fail_rate", "failshare", "fail_n", "nfail4b", "n_fail4b"}


def failstr_candidates(cols):
    """Column names that MIGHT hold a 4b fail-string.  Names are candidates only; every one is
    validated against its own values before it is used (G3)."""
    out = []
    for c in cols:
        cl = c.lower()
        if cl in NOT_FAILSTR or "4a" in cl:
            continue
        if cl == "fail4b":
            continue                                   # R0's own column, handled separately
        if ("fail" in cl or "bind" in cl or cl.startswith("leg") or cl in ("why", "reason")):
            out.append(c)
    return out


LEGCOL_SETS = [
    (["L1_H1", "L2_H2", "L3_OOS", "L4_DDcap", "L5_CAGRfloor"], "bool"),
    (["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"], "bool"),
    (["leg_H1", "leg_H2", "leg_OOS", "leg_DD", "leg_CAGR"], "bool"),
    (["leg_H1", "leg_H2", "leg_OOS", "leg_DDCAP", "leg_CAGRFLOOR"], "bool"),
    (["m_H1", "m_H2", "m_OOS", "m_DD", "m_CAGR"], "margin"),
    (["m_L1_H1", "m_L2_H2", "m_L3_OOS", "m_L4_DD", "m_L5_CAGR"], "margin"),
]
STAT_NAMES = {
    "CAGR": ["CAGR", "cagr", "CAGR_F", "full_CAGR", "CAGR_full"],
    "MaxDD": ["MaxDD", "maxdd", "MaxDD_F", "dd", "DD", "full_MaxDD"],
    "H1": ["H1", "Sharpe_H1", "h1", "H1_Sharpe"],
    "H2": ["H2", "Sharpe_H2", "h2", "H2_Sharpe"],
    "OOS_S": ["OOS_Sharpe", "OOS", "oos", "Sharpe_OOS", "OOS_S", "oosS", "OOS_sharpe"],
    "OOS_CAGR": ["OOS_CAGR", "CAGR_OOS", "oos_cagr", "OOS_cagr"],
    "OOS_MaxDD": ["OOS_MaxDD", "MaxDD_OOS", "oos_maxdd", "OOS_DD", "OOS_dd"],
}
SPY_NAMES = {
    "CAGR": ["spy_CAGR", "SPY_CAGR", "spy_CAGR_F", "spy_cagr"],
    "MaxDD": ["spy_MaxDD", "SPY_MaxDD", "spy_DD", "spy_MaxDD_F", "spy_maxdd"],
    "H1": ["spy_H1", "SPY_H1", "spy_h1"],
    "H2": ["spy_H2", "SPY_H2", "spy_h2"],
    "OOS_S": ["spy_OOS_Sharpe", "SPY_OOS_Sharpe", "spy_OOS_S", "spy_S_OOS", "spy_oosS",
              "spy_Sharpe_OOS", "spy_OOS"],
    "OOS_CAGR": ["spy_OOS_CAGR", "SPY_OOS_CAGR", "spy_oos_CAGR", "spy_CAGR_OOS"],
    "OOS_MaxDD": ["spy_OOS_MaxDD", "SPY_OOS_MaxDD", "spy_OOS_DD", "spy_MaxDD_OOS"],
}


def pick(cols, names):
    for n in names:
        if n in cols:
            return n
    low = {c.lower(): c for c in cols}
    for n in names:
        if n.lower() in low:
            return low[n.lower()]
    return None


def truthy(s):
    return s.astype(str).str.strip().str.lower().isin(["true", "1", "1.0", "yes", "y", "t"])


def falsy(s):
    return s.astype(str).str.strip().str.lower().isin(["false", "0", "0.0", "no", "n", "f"])


# ==================================================================================== the census
def panel_spy_table():
    """SPY's 4b comparands on each committed panel, over PROTOCOL's windows.  Used ONLY at R4."""
    tab = {}
    for name, kw in (("U56", {}), ("B136", dict(broad=True)), ("SMALL", dict(small=True))):
        try:
            px = load_universe(**kw)
        except Exception as e:
            P(f"    panel {name} unavailable ({type(e).__name__}) -- R4 will not use it")
            continue
        r = px["SPY"].pct_change().fillna(0.0)
        idx = px.index
        full = np.asarray(idx >= idx[WARMUP])
        fp = np.flatnonzero(full)
        h = len(fp) // 2
        m1 = np.zeros(len(idx), bool); m1[fp[:h]] = True
        m2 = np.zeros(len(idx), bool); m2[fp[h:]] = True
        oos = np.asarray(idx >= pd.Timestamp(OOS_START))
        c, s, d = fmet(r.values[full])
        co, so, do = fmet(r.values[oos])
        tab[name] = dict(CAGR=c, MaxDD=d, H1=fsharpe(r.values[m1]), H2=fsharpe(r.values[m2]),
                         OOS_S=so, OOS_CAGR=co, OOS_MaxDD=do)
    return tab


def fmet(r):
    r = np.asarray(r, float)
    if len(r) < 3 or not np.isfinite(r).all():
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    if len(r) < 3:
        return np.nan
    v = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / v if v else np.nan


def legs_from_stats(row, spy):
    """PROTOCOL 4b leg by leg from committed statistics.  None = the row cannot decide the leg."""
    def cmp(a, b, rule):
        if a is None or b is None or not np.isfinite(a) or not np.isfinite(b):
            return None
        if rule == "gt":
            return not (a > b)                                    # True == leg FAILS
        if rule == "dd":
            return not (abs(a) <= DD_CAP * abs(b))
        return not (a >= CAGR_FLOOR * b)
    return {"L1_H1": cmp(row.get("H1"), spy.get("H1"), "gt"),
            "L2_H2": cmp(row.get("H2"), spy.get("H2"), "gt"),
            "L3_OOS": cmp(row.get("OOS_S"), spy.get("OOS_S"), "gt"),
            "L4_DD": cmp(row.get("MaxDD"), spy.get("MaxDD"), "dd"),
            "L5_CAGR": cmp(row.get("CAGR"), spy.get("CAGR"), "cagr")}


def census(files, spytab, vocab=None, collect_fidelity=False):
    """One pass over the record.  Returns per-(file, rung) counts, signature counts per rung,
    the admitted/rejected column vocabulary, and the text-vs-stats fidelity pairs.

    vocab: None = learn from every file; else a set of (rung, column-name) pairs -- only those
    columns may be used (this is how the record-time walk-forward is run)."""
    rows, sigc, used, rejected, fid = [], {r: collections.Counter() for r in RUNGS}, set(), \
        collections.Counter(), collections.Counter()
    tot_fail = tot_files = 0
    for f in files:
        try:
            cols = list(pd.read_csv(f, nrows=0).columns)
        except Exception:
            continue
        pcol = next((c for c in PCOLS if c in cols), None)
        if pcol is None:
            continue
        # ---- what this file offers, rung by rung
        r0_fail = "fail4b" if "fail4b" in cols else None
        r0_set = next((L for L in READ_SETS if set(L) <= set(cols)), None)
        cands = failstr_candidates(cols)
        legsets = [(L, k) for L, k in LEGCOL_SETS
                   if all(pick(cols, [c]) for c in L) and set(L) != set(r0_set or [])]
        stat = {k: pick(cols, v) for k, v in STAT_NAMES.items()}
        spyc = {k: pick(cols, v) for k, v in SPY_NAMES.items()}
        pan = pick(cols, ["panel", "uni", "universe", "corpus"])
        need = [pcol] + [c for c in ([r0_fail] + cands + list(r0_set or []) + [pan]) if c] \
            + [c for L, _ in legsets for c in [pick(cols, [x]) for x in L]] \
            + [c for c in list(stat.values()) + list(spyc.values()) if c]
        need = list(dict.fromkeys(need))
        try:
            df = pd.read_csv(f, usecols=need)
        except Exception:
            continue
        tot_files += 1
        fail = df[~truthy(df[pcol])]
        nf = len(fail)
        if not nf:
            continue
        tot_fail += nf
        N = np.arange(nf)
        # ---- R0 : 944's rule, verbatim -------------------------------------------------------
        sig0 = pd.Series("", index=fail.index, dtype=object)
        if r0_fail is not None:
            st = fail[r0_fail].map(lambda v: parse_sig(v))
            sig0 = st.map(lambda t: t[1] if t[0] == "fail" else "")
        if r0_set is not None:
            fl = {LEGS[i]: ~truthy(fail[r0_set[i]]) for i in range(5)}
            rec = pd.Series(["+".join(k for k in LEGS if fl[k].iloc[i]) for i in range(nf)],
                            index=fail.index)
            sig0 = sig0.where(sig0 != "", rec)
        # ---- R1 : any other validated fail-string column --------------------------------------
        sig1 = sig0.copy()
        for c in cands:
            if vocab is not None and ("R1", c) not in vocab:
                continue
            vals = fail[c].astype(str)
            nonempty = vals[~vals.str.strip().str.lower().isin(["", "nan", "none"])]
            if not len(nonempty):
                continue
            kinds = nonempty.map(lambda v: parse_sig(v)[0])
            share = float((kinds != "bad").mean())
            if share < VALIDATE_SHARE:
                rejected[f"{c} ({share:.2f})"] += 1
                continue
            used.add(("R1", c))
            got = vals.map(lambda v: parse_sig(v)).map(lambda t: t[1] if t[0] == "fail" else "")
            sig1 = sig1.where(sig1 != "", got)
        # ---- R2 : per-leg boolean / margin families -------------------------------------------
        sig2 = sig1.copy()
        for L, kind in legsets:
            names = [pick(cols, [x]) for x in L]
            if vocab is not None and any(("R2", n) not in vocab for n in names):
                continue
            used.update(("R2", n) for n in names)
            flags = {}
            for i, n in enumerate(names):
                col = fail[n]
                if kind == "margin":
                    v = pd.to_numeric(col, errors="coerce")
                    flags[LEGS[i]] = (v < 0).where(v.notna(), other=np.nan)
                else:
                    t, fa = truthy(col), falsy(col)
                    flags[LEGS[i]] = fa.where(t | fa, other=np.nan)
            M = np.vstack([np.asarray(flags[k], float) for k in LEGS])       # 5 x nf
            dec = np.isfinite(M).sum(axis=0)
            rec = ["+".join(LEGS[j] for j in range(5) if M[j, i] == 1.0) for i in range(nf)]
            rec = pd.Series([r if (dec[i] > 0 and r) else ("-" if dec[i] == 5 else "")
                             for i, r in enumerate(rec)], index=fail.index)
            sig2 = sig2.where(sig2 != "", rec)
        # ---- R3 / R4 : reconstruct from statistics --------------------------------------------
        sig3 = sig2.copy()
        sig4 = sig2.copy()
        have_stat = {k: v for k, v in stat.items() if v}
        if have_stat:
            S = {k: pd.to_numeric(fail[v], errors="coerce").values for k, v in have_stat.items()}
            for rung, spysrc in (("R3", "infile"), ("R4", "panel")):
                if vocab is not None and any((rung, v) not in vocab for v in have_stat.values()):
                    continue
                if spysrc == "infile":
                    sp = {k: (pd.to_numeric(fail[v], errors="coerce").values if v else None)
                          for k, v in spyc.items()}
                    if not any(v is not None for v in sp.values()):
                        continue
                    used.update((rung, v) for v in list(have_stat.values())
                                + [x for x in spyc.values() if x])
                else:
                    raw = (fail[pan] if pan is not None else
                           pd.Series("U56", index=fail.index))

                    def _pan(v):
                        s = str(v).upper()
                        if "136" in s or "BROAD" in s or s.startswith("B1"):
                            return "B136"
                        if "SMALL" in s or "439" in s or "485" in s or "663" in s:
                            return "SMALL"
                        return "U56"                      # the record's default panel
                    pn = raw.map(_pan)
                    sp = {k: np.array([spytab.get(p, {}).get(k, np.nan) for p in pn])
                          for k in STAT_NAMES}
                    used.update((rung, v) for v in have_stat.values())
                # PROTOCOL 4b reads the DD cap and the CAGR floor on the FULL sample.  Parts of
                # the record read them on the OOS window instead (OOS_CAGR / OOS_MaxDD against
                # spy_OOS_*), and a row never says which convention produced it.  BOTH are
                # rebuilt: FULL drives the ladder (it is PROTOCOL's own reading); the pair is
                # scored in (C) so the ambiguity is measured instead of assumed away.
                recs = {}
                for conv in ("FULL", "OOS"):
                    keys = (("L1_H1", "H1", "gt"), ("L2_H2", "H2", "gt"),
                            ("L3_OOS", "OOS_S", "gt"),
                            ("L4_DD", "MaxDD" if conv == "FULL" else "OOS_MaxDD", "dd"),
                            ("L5_CAGR", "CAGR" if conv == "FULL" else "OOS_CAGR", "cagr"))
                    flags = {}
                    for leg, key, rule in keys:
                        a = S.get(key)
                        b = sp.get(key)
                        if a is None or b is None:
                            flags[leg] = np.full(nf, np.nan)
                            continue
                        b = np.broadcast_to(np.asarray(b, float), (nf,))
                        ok = np.isfinite(a) & np.isfinite(b)
                        with np.errstate(invalid="ignore"):
                            if rule == "gt":
                                bad = ~(a > b)
                            elif rule == "dd":
                                bad = ~(np.abs(a) <= DD_CAP * np.abs(b))
                            else:
                                bad = ~(a >= CAGR_FLOOR * b)
                        flags[leg] = np.where(ok, bad.astype(float), np.nan)
                    M = np.vstack([flags[k] for k in LEGS])
                    dec = np.isfinite(M).sum(axis=0)
                    raw_rec = ["+".join(LEGS[j] for j in range(5) if M[j, i] == 1.0)
                               for i in range(nf)]
                    recs[conv] = pd.Series(
                        [r if (dec[i] > 0 and r) else ("-" if dec[i] == 5 else "")
                         for i, r in enumerate(raw_rec)], index=fail.index)
                rec = recs["FULL"]
                tgt = sig3 if rung == "R3" else sig4
                new = tgt.where(tgt != "", rec)
                if rung == "R3":
                    sig3 = new
                    sig4 = sig4.where(sig4 != "", rec)
                else:
                    sig4 = new
                if collect_fidelity:
                    # Where the record STATES the legs (R0-R2 text) and the statistics can also
                    # rebuild them, the two must agree.  R3 (the file's OWN committed SPY
                    # comparand) and R4 (this run's panel comparand) are scored SEPARATELY: if
                    # R3 is faithful and R4 is not, the fault is the panel assumption, not the
                    # record.  If neither is, the row's window is simply not recoverable.
                    both = (sig2 != "") & (rec != "")
                    for a_, b_, o_ in zip(sig2[both], rec[both], recs["OOS"][both]):
                        ok = a_ == b_
                        fid[(rung, "agree" if ok else "differ")] += 1
                        fid[(rung, "OOSconv_agree" if a_ == o_ else "OOSconv_differ")] += 1
                        fid[(rung, "either_agree" if (ok or a_ == o_) else "either_differ")] += 1
                        fid[("f", rung, Path(f).name, "agree" if ok else "differ")] += 1
                        if not ok:
                            fid[("pair", rung, a_, b_)] += 1
        # ---- book the file ---------------------------------------------------------------------
        L = [sig0, sig1, sig2, sig3, sig4]
        rec_row = dict(file=Path(f).name, n_fail=nf)
        for rn, s in zip(RUNGS, L):
            named = int(((s != "") & (s != "-")).sum())
            full = named + int((s == "-").sum())
            rec_row[f"{rn}_named"] = named
            rec_row[f"{rn}_any"] = full
            for k, v in s[(s != "") & (s != "-")].value_counts().items():
                sigc[rn][k] += int(v)
        rows.append(rec_row)
    return (pd.DataFrame(rows), sigc, used, rejected, fid, tot_fail, tot_files)


# ============================================================================== PROTOCOL rule 8
def build_books(px, g=GROSS0):
    sc, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < VOLCAP)
    rank = sc.where(elig).rank(axis=1, ascending=False)
    out = {}
    for n in (5, 10, 20, 30):
        out[f"TOP{n}"] = ((rank <= n).astype(float) * (g / n)).values
    out["BAND03"] = rules_v2_weights(px, BAND0, g).values
    return out


class Runner:
    """The same fast runner idea 944 used: weights at close t applied at t+1, 10 bps per unit
    turnover, gated against engine.backtest in G6."""

    def __init__(self, px, mask):
        self.px, self.idx = px, px.index
        self.rets = px.pct_change().fillna(0.0).values
        T, N = self.rets.shape
        self.T = T
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, N)), C[:-1]])
        mk = np.asarray(mask.values, bool)
        mk = np.concatenate([[False], mk[:-1]]).copy()
        mk[0] = True
        self.reb = np.flatnonzero(mk)
        seg = np.searchsorted(self.reb, np.arange(T), side="right") - 1
        self.s0 = self.reb[seg]
        self.s0p = self.reb[np.maximum(seg - 1, 0)]
        self.R = self.Cp / self.Cp[self.s0]
        self.Rp = self.Cp[self.reb] / self.Cp[self.s0p[self.reb]]
        full = np.asarray(self.idx >= self.idx[WARMUP])
        fp = np.flatnonzero(full)
        h = len(fp) // 2
        m1 = np.zeros(T, bool); m1[fp[:h]] = True
        m2 = np.zeros(T, bool); m2[fp[h:]] = True
        self.masks = dict(FULL=full, H1=m1, H2=m2,
                          IS=full & np.asarray(self.idx <= pd.Timestamp(IS_END)),
                          OOS=np.asarray(self.idx >= pd.Timestamp(OOS_START)))

    def run(self, Wg, cost=COST0):
        wt = np.roll(Wg, LAG, axis=0).copy()
        wt[:LAG] = 0.0
        A = wt[self.s0]
        AR = A * self.R
        V = 1.0 + (AR.sum(axis=1) - A.sum(axis=1))
        gross = (AR * self.rets).sum(axis=1) / V
        Ap = wt[self.s0p[self.reb]]
        ARp = Ap * self.Rp
        Vp = 1.0 + (ARp.sum(axis=1) - Ap.sum(axis=1))
        heldp = ARp / Vp[:, None]
        heldp[0] = 0.0
        turn = np.zeros(self.T)
        turn[self.reb] = np.abs(wt[self.reb] - heldp).sum(axis=1)
        return gross - turn * cost / 1e4, turn

    def pack(self, r):
        c, s, d = fmet(r[self.masks["FULL"]])
        co, so, do = fmet(r[self.masks["OOS"]])
        return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(r[self.masks["H1"]]),
                    H2=fsharpe(r[self.masks["H2"]]), IS_Sharpe=fsharpe(r[self.masks["IS"]]),
                    OOS_CAGR=co, OOS_Sharpe=so, OOS_MaxDD=do)


def legs4b(m, spy):
    fl = {"L1_H1": not (m["H1"] > spy["H1"]), "L2_H2": not (m["H2"] > spy["H2"]),
          "L3_OOS": not (m["OOS_Sharpe"] > spy["OOS_Sharpe"]),
          "L4_DD": not (abs(m["MaxDD"]) <= DD_CAP * abs(spy["MaxDD"])),
          "L5_CAGR": not (m["CAGR"] >= CAGR_FLOOR * spy["CAGR"])}
    f = [k for k in LEGS if fl[k]]
    return (not f), ("+".join(f) if f else "-")


# ============================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 952 (lane C)  can the BINDING LEG of the SILENT 4b FAIL rows be recovered?")
    P("=" * 100)
    P("TUNED: (1) RECOVERY RULE, 5 nested rungs R0..R4, every rung reported;")
    P("       (2) CLAIM SET, {ROW-WEIGHTED, FILE-WEIGHTED}, both reported, never merged.")
    P("Everything else is a reported axis.  Bars were fixed before any number was read.")

    files = sorted(list(OUT.glob("*.csv")) + list(OUT.glob("*.csv.gz")))
    files = [f for f in files if not f.name.startswith(STEM)]
    P(f"\n  {len(files):,} committed CSVs under research/backtests")

    # ------------------------------------------- the pre-registered "cited" cut, reported only
    lb = (ROOT / "research" / "LEADERBOARD.md").read_text(errors="ignore")
    pub = {p[:-3] for p in re.findall(r"[0-9]{4}-[0-9]{2}-[0-9]{2}_[A-Za-z0-9_\-]+\.py", lb)}
    pubfiles = [f for f in files if any(f.name.startswith(p) for p in pub)]
    P(f"  LEADERBOARD-cited stems: {len(pub):,} -> {len(pubfiles):,} CSVs "
      f"({len(pubfiles)/max(len(files),1):.1%} of the record).  This cut does not partition the "
      f"record, so it is REPORTED and not used as a tuned level (see the docstring).")

    P("\n  building SPY's panel comparands (used only at R4) ...")
    spytab = panel_spy_table()
    for k, v in spytab.items():
        P(f"    {k:<6} SPY  CAGR {v['CAGR']:.2%}  MaxDD {v['MaxDD']:.2%}  "
          f"H1 {v['H1']:.3f}  H2 {v['H2']:.3f}  OOS_S {v['OOS_S']:.3f}")

    # ================================================================== THE CENSUS (ALL)
    P("\n" + "=" * 100)
    P("(A) THE LADDER -- every committed 4b FAIL row, rung by rung")
    P("=" * 100)
    FA, sigA, used, rejected, fid, totA, nfilesA = census(files, spytab, collect_fidelity=True)
    P(f"  {nfilesA:,} CSVs carry a 4b pass column; {totA:,} committed 4b FAIL rows")
    P(f"  944 committed {PUB_WIDE:,} -- drift {totA - PUB_WIDE:+,} rows from files committed "
      f"after 944 ran (printed, not absorbed)")

    def headline(F, tot):
        out = []
        for rn in RUNGS:
            named, any_ = int(F[f"{rn}_named"].sum()), int(F[f"{rn}_any"].sum())
            out.append(dict(rung=rn, named=named, named_share=named / max(tot, 1),
                            decided=any_, decided_share=any_ / max(tot, 1),
                            files=int((F[f"{rn}_named"] > 0).sum())))
        return pd.DataFrame(out)

    HA = headline(FA, totA)
    P("\n    rung              rows NAMING a binding leg     rows fully decided      files")
    for r in HA.itertuples():
        P(f"    {r.rung:<17} {r.named:>10,}  {r.named_share:>7.1%}        "
          f"{r.decided:>10,}  {r.decided_share:>7.1%}    {r.files:>5}")
    r0n = int(HA[HA.rung == "R0_ASBUILT"].named.iloc[0])
    r4n = int(HA[HA.rung == "R4_STATS_PANEL"].named.iloc[0])
    silent0 = totA - r0n
    rec_of_silent = (r4n - r0n) / max(silent0, 1)
    P(f"\n    944 booked {silent0:,} rows UNRECOVERABLE.  The ladder names a binding leg for "
      f"{r4n - r0n:,} of them = {rec_of_silent:.1%}")
    P(f"    irreducible residue (no rule reaches it): {totA - r4n:,} rows = "
      f"{(totA - r4n)/max(totA,1):.1%} of the record's 4b FAIL rows")

    # --------------------------------------------------- CLAIM SET 2 of 2: FILE-WEIGHTED
    HF = pd.DataFrame([dict(rung=rn,
                            named=int((FA[f"{rn}_named"] >= 0.5 * FA.n_fail).sum()),
                            named_share=float((FA[f"{rn}_named"] >= 0.5 * FA.n_fail).mean()),
                            decided=int((FA[f"{rn}_any"] >= 0.5 * FA.n_fail).sum()),
                            decided_share=float((FA[f"{rn}_any"] >= 0.5 * FA.n_fail).mean()),
                            files=len(FA)) for rn in RUNGS])
    P(f"\n  CLAIM SET = FILE-WEIGHTED ({len(FA):,} CSVs carrying >= 1 committed 4b FAIL row; a "
      f"file counts as recovered when >= 50% of its FAIL rows get a named leg)")
    P("    rung              files RECOVERED               files fully decided")
    for r in HF.itertuples():
        P(f"    {r.rung:<17} {r.named:>10,}  {r.named_share:>7.1%}        "
          f"{r.decided:>10,}  {r.decided_share:>7.1%}")
    dclaim = abs(float(HA[HA.rung == "R4_STATS_PANEL"].named_share.iloc[0])
                 - float(HF[HF.rung == "R4_STATS_PANEL"].named_share.iloc[0]))
    cited = FA[FA.file.map(lambda n: any(n.startswith(p) for p in pub))]
    P(f"\n  REPORTED cut: LEADERBOARD-cited files only -- "
      f"{int(cited.R4_STATS_PANEL_named.sum()):,} of {int(cited.n_fail.sum()):,} FAIL rows "
      f"named = {cited.R4_STATS_PANEL_named.sum()/max(cited.n_fail.sum(),1):.1%}")
    HA["claim_set"] = "ROW_WEIGHTED"; HF["claim_set"] = "FILE_WEIGHTED"
    dump(pd.concat([HA, HF], ignore_index=True), "ladder.csv")
    dump(FA.sort_values("n_fail", ascending=False), "recovery.csv")

    # ================================================================== (B) GATES
    P("\n" + "=" * 100)
    P("(B) GATES")
    P("=" * 100)
    gates = []
    dd_alone_r0 = sigA["R0_ASBUILT"]["L4_DD"] / max(sum(sigA["R0_ASBUILT"].values()), 1)
    g1 = abs(dd_alone_r0 - PUB_DD_ALONE) <= 0.02 and abs(totA - PUB_WIDE) / PUB_WIDE <= 0.05
    gates.append(dict(gate="G1 CROSS-RUN reproduces 944's committed census",
                      stat=f"WIDE {totA:,} vs 944's {PUB_WIDE:,} ({(totA-PUB_WIDE)/PUB_WIDE:+.2%}); "
                           f"R0 rows naming a leg {r0n:,} vs 944's {PUB_READ:,}; "
                           f"L4_DD-alone share of R0 {dd_alone_r0:.1%} vs 944's {PUB_DD_ALONE:.1%}",
                      bar="|dDD_alone| <= 2 pp and |dWIDE| <= 5%", passed=bool(g1)))
    nest = all((FA[f"{RUNGS[i]}_named"] <= FA[f"{RUNGS[i+1]}_named"] + 1e-9).all()
               for i in range(len(RUNGS) - 1))
    gates.append(dict(gate="G2 NESTING  R0 <= R1 <= R2 <= R3 <= R4 on every file",
                      stat=f"{int((FA[[f'{r}_named' for r in RUNGS]].diff(axis=1) < 0).sum().sum())}"
                           f" violations over {len(FA):,} files", bar="0 violations",
                      passed=bool(nest)))
    gates.append(dict(gate="G3 VALIDATION every R1 column parses on >= 90% of its FAIL values",
                      stat=f"{len([u for u in used if u[0]=='R1'])} columns admitted, "
                           f"{len(rejected)} candidate columns REJECTED on their own values: "
                           + "; ".join(f"{k} x{v}" for k, v in rejected.most_common(6)),
                      bar="admitted > 0 and rejects listed", passed=bool(
                          len([u for u in used if u[0] == "R1"]) > 0)))
    FA2, sigA2, _, _, _, totA2, _ = census(files[:200], spytab)
    FA1 = FA[FA.file.isin(FA2.file)]
    det = bool(len(FA1) == len(FA2) and np.allclose(
        FA1.sort_values("file")[[f"{r}_named" for r in RUNGS]].values,
        FA2.sort_values("file")[[f"{r}_named" for r in RUNGS]].values))
    gates.append(dict(gate="G4 DETERMINISM re-read of the same files gives identical counts",
                      stat=f"{len(FA2):,} files re-read, max|d| "
                           f"{0 if det else 'MISMATCH'}", bar="identical", passed=det))
    saw944 = int(FA[FA.file.str.contains("DD-CAP-the-binding-leg")].n_fail.sum())
    gates.append(dict(gate="G5 SELF-SEE the census sees idea 944's own committed FAIL rows",
                      stat=f"{saw944:,} FAIL rows harvested from 944's own CSVs",
                      bar="> 0", passed=bool(saw944 > 0)))

    px = load_universe()
    mask = rebalance_mask(px.index, "M")
    RN = Runner(px, mask)
    W = build_books(px)
    r_fast, t_fast = RN.run(W["TOP20"], COST0)
    sel = pd.DataFrame(W["TOP20"], index=px.index, columns=px.columns)
    eng = backtest(px, sel, cost_bps=COST0, freq="M")
    # engine.backtest leaves its first two rows NaN by construction (w_target is shift(1)), so the
    # comparison runs over the scored window -- index[WARMUP:] -- which is what every metric uses.
    w = RN.masks["FULL"]
    d_r = float(np.abs(np.asarray(eng["returns"])[w] - r_fast[w]).max())
    d_t = float(np.abs(np.asarray(eng["turnover"])[w] - t_fast[w]).max())
    gates.append(dict(gate="G6 WF ENGINE fast runner == engine.backtest (TOP20, U56, monthly, "
                           "scored window)",
                      stat=f"max|dret| {d_r:.2e}  max|dturn| {d_t:.2e}",
                      bar="< 1e-9", passed=bool(d_r < 1e-9 and d_t < 1e-9)))
    for g in gates:
        P(f"  [{'PASS' if g['passed'] else 'FAIL'}] {g['gate']}\n         {g['stat']}   "
          f"(bar {g['bar']})")
    P(f"\n  GATES {sum(g['passed'] for g in gates)} of {len(gates)} PASS")
    dump(pd.DataFrame(gates), "gates.csv")

    # ================================================================== (C) FIDELITY
    P("\n" + "=" * 100)
    P("(C) FIDELITY -- where the record STATES the leg AND the statistics can rebuild it")
    P("=" * 100)
    fa = collections.Counter(); fd = collections.Counter()          # per-file, best rung
    frows = []
    for rung in ("R3", "R4"):
        a_, d_ = fid[(rung, "agree")], fid[(rung, "differ")]
        oa = fid[(rung, "OOSconv_agree")]
        ea = fid[(rung, "either_agree")]
        src = "the file's OWN committed SPY comparand" if rung == "R3" else \
              "this run's panel comparand"
        P(f"  {rung} ({src}): {a_ + d_:>8,} doubly-covered rows")
        P(f"       PROTOCOL's FULL-sample DD/CAGR convention : {a_:>8,} = {a_/max(a_+d_,1):>6.1%}")
        P(f"       the record's OOS-window convention        : {oa:>8,} = "
          f"{oa/max(a_+d_,1):>6.1%}")
        P(f"       EITHER convention explains the row        : {ea:>8,} = "
          f"{ea/max(a_+d_,1):>6.1%}")
        frows.append(dict(rung=rung, rows=a_ + d_, agree_full=a_, rate_full=a_ / max(a_ + d_, 1),
                          agree_oos=oa, rate_oos=oa / max(a_ + d_, 1), agree_either=ea,
                          rate_either=ea / max(a_ + d_, 1)))
    agree = fid[("R3", "agree")] + fid[("R4", "agree")]
    differ = fid[("R3", "differ")] + fid[("R4", "differ")]
    fid_rate = agree / max(agree + differ, 1)
    pairs = [(k[1], k[2], k[3], v) for k, v in fid.items()
             if isinstance(k, tuple) and k[0] == "pair"]
    pairs.sort(key=lambda x: -x[3])
    P("  the largest disagreements (committed vs rebuilt):")
    for rg, a2, b2, v in pairs[:8]:
        P(f"      {rg}  committed {a2:<32} rebuilt {b2:<32} x{v:,}")
    fpf = {}
    for k, v in fid.items():
        if isinstance(k, tuple) and k[0] == "f":
            fpf.setdefault((k[1], k[2]), collections.Counter())[k[3]] += v
    ffiles = sorted({k[1] for k in fpf})
    for name in ffiles:
        cs = [fpf.get((r2, name), collections.Counter()) for r2 in ("R3", "R4")]
        # a file is VERIFIED when at least one comparand rebuilds its committed legs on EVERY
        # doubly-covered row of that file; otherwise every disagreement is booked against it.
        if any(c["differ"] == 0 and c["agree"] > 0 for c in cs):
            fa[name] = max(c["agree"] for c in cs)
        else:
            fd[name] = sum(c["differ"] for c in cs)
            fa[name] = sum(c["agree"] for c in cs)
    clean = [f for f in ffiles if fd[f] == 0 and fa[f] > 0]
    P(f"\n  idea 161's STRICTER per-file gate (the rebuild must match on EVERY row of a file, on")
    P(f"  EITHER comparand): {len(clean):,} of {len(ffiles):,} doubly-covered files reconstruct")
    P(f"  EXACTLY ({len(clean)/max(len(ffiles),1):.1%}); the rest are listed in the fidelity CSV.")
    dump(pd.DataFrame([dict(file=f, agree=fa[f], differ=fd[f]) for f in ffiles]
                      ).sort_values("differ", ascending=False), "fidelity_files.csv")
    dump(pd.DataFrame(pairs, columns=["rung", "committed", "rebuilt", "n"]), "fidelity.csv")
    dump(pd.DataFrame(frows), "fidelity_rung.csv")

    # ---- the HONEST headline: a statistics rung is only allowed where it VERIFIES ------------
    P("\n  THE FIDELITY-GATED LADDER (the number this run stands behind)")
    P("    A statistics rung (R3/R4) is allowed on a file ONLY where the rebuild reproduces that")
    P("    file's own committed legs on EVERY doubly-covered row (idea 161's gate).  Files with")
    P("    no doubly-covered row cannot be checked either way and are reported as a RANGE.")
    FA = FA.assign(fid_agree=FA.file.map(lambda n: fa.get(n, 0)),
                   fid_differ=FA.file.map(lambda n: fd.get(n, 0)))
    verified = FA[(FA.fid_agree > 0) & (FA.fid_differ == 0)]
    refuted = FA[FA.fid_differ > 0]
    unchecked = FA[(FA.fid_agree == 0) & (FA.fid_differ == 0)]
    gated_lo = (int(verified.R4_STATS_PANEL_named.sum()) + int(refuted.R2_LEGCOLS_named.sum())
                + int(unchecked.R2_LEGCOLS_named.sum()))
    gated_hi = (int(verified.R4_STATS_PANEL_named.sum()) + int(refuted.R2_LEGCOLS_named.sum())
                + int(unchecked.R4_STATS_PANEL_named.sum()))
    P(f"    files VERIFIED {len(verified):,} ({int(verified.n_fail.sum()):,} FAIL rows) | "
      f"REFUTED {len(refuted):,} ({int(refuted.n_fail.sum()):,}) | "
      f"UNCHECKABLE {len(unchecked):,} ({int(unchecked.n_fail.sum()):,})")
    P(f"    gated recovery of the whole record: {gated_lo:,} .. {gated_hi:,} rows = "
      f"{gated_lo/max(totA,1):.1%} .. {gated_hi/max(totA,1):.1%} "
      f"(ungated R4 reads {r4n:,} = {r4n/max(totA,1):.1%})")
    gsil_lo = (gated_lo - r0n) / max(silent0, 1)
    gsil_hi = (gated_hi - r0n) / max(silent0, 1)
    P(f"    of 944's {silent0:,} UNRECOVERABLE rows, the gated ladder names "
      f"{gsil_lo:.1%} .. {gsil_hi:.1%}; the TEXT-ONLY rungs (R0-R2, the record's own words, no "
      f"modelling and no fidelity risk) name "
      f"{(int(FA.R2_LEGCOLS_named.sum())-r0n)/max(silent0,1):.1%}")
    dump(pd.DataFrame([dict(bucket=b, files=len(d), fail_rows=int(d.n_fail.sum()),
                            R2_named=int(d.R2_LEGCOLS_named.sum()),
                            R4_named=int(d.R4_STATS_PANEL_named.sum()))
                       for b, d in (("VERIFIED", verified), ("REFUTED", refuted),
                                    ("UNCHECKABLE", unchecked))]), "gated.csv")

    # ================================================================== (D) BIAS
    P("\n" + "=" * 100)
    P("(D) BIAS -- is the readable 15% a fair sample of the record's binding legs?")
    P("=" * 100)
    base = sigA["R0_ASBUILT"]
    wide = sigA["R4_STATS_PANEL"]
    text = sigA["R2_LEGCOLS"]
    newc = collections.Counter({k: wide[k] - base.get(k, 0) for k in wide
                                if wide[k] - base.get(k, 0) > 0})
    newt = collections.Counter({k: text[k] - base.get(k, 0) for k in text
                                if text[k] - base.get(k, 0) > 0})
    nb, nn = max(sum(base.values()), 1), max(sum(newc.values()), 1)
    nt = max(sum(newt.values()), 1)

    def shares(c, n):
        out = {}
        for leg in LEGS:
            out[f"{leg}_alone"] = c.get(leg, 0) / n
            out[f"{leg}_any"] = sum(v for k, v in c.items() if leg in k.split("+")) / n
        return out

    sb, sn, st = shares(base, nb), shares(newc, nn), shares(newt, nt)
    P(f"  R0-readable rows: {nb:,}   newly recovered: TEXT-ONLY (R1-R2, trustworthy) {nt:,}, "
      f"including the statistics rungs {nn:,}")
    P("    leg        alone R0   alone TEXT    d pp  |  alone ALL     d pp  |   any R0   any TEXT"
      "    d pp")
    biasrows = []
    for leg in LEGS:
        da = (sn[f"{leg}_alone"] - sb[f"{leg}_alone"]) * 100
        dt = (st[f"{leg}_alone"] - sb[f"{leg}_alone"]) * 100
        dy = (sn[f"{leg}_any"] - sb[f"{leg}_any"]) * 100
        dyt = (st[f"{leg}_any"] - sb[f"{leg}_any"]) * 100
        P(f"    {leg:<10} {sb[f'{leg}_alone']:>8.1%}   {st[f'{leg}_alone']:>8.1%}  {dt:>+7.1f}  | "
          f"{sn[f'{leg}_alone']:>8.1%}  {da:>+7.1f}  | {sb[f'{leg}_any']:>8.1%}  "
          f"{st[f'{leg}_any']:>8.1%}  {dyt:>+7.1f}")
        biasrows.append(dict(leg=leg, alone_R0=sb[f"{leg}_alone"],
                             alone_TEXT=st[f"{leg}_alone"], d_alone_text_pp=dt,
                             alone_NEW=sn[f"{leg}_alone"], d_alone_pp=da,
                             any_R0=sb[f"{leg}_any"], any_TEXT=st[f"{leg}_any"],
                             d_any_text_pp=dyt, any_NEW=sn[f"{leg}_any"], d_any_pp=dy))
    dump(pd.DataFrame(biasrows), "bias.csv")
    dd_move = abs(biasrows[3]["d_alone_text_pp"])
    cg_move = abs(biasrows[4]["d_alone_text_pp"])
    dd_move_all = abs(biasrows[3]["d_alone_pp"])
    cg_move_all = abs(biasrows[4]["d_alone_pp"])
    P(f"\n  944's published leg shares were computed on the R0 column alone.  On the rows the")
    P(f"  record ALREADY named in another column -- no modelling, nothing to distrust -- the")
    P(f"  DD-cap-ALONE share reads {st['L4_DD_alone']:.1%} against {sb['L4_DD_alone']:.1%} "
      f"({biasrows[3]['d_alone_text_pp']:+.1f} pp) and the CAGR-floor-ALONE share "
      f"{st['L5_CAGR_alone']:.1%} against {sb['L5_CAGR_alone']:.1%} "
      f"({biasrows[4]['d_alone_text_pp']:+.1f} pp).")
    P(f"  The 15% the census could read is NOT a fair sample of the record's binding legs.")
    sigdf = pd.DataFrame([dict(rung=rn, sig=k, n=v) for rn in RUNGS
                          for k, v in sigA[rn].most_common()])
    dump(sigdf, "signatures.csv")

    # ================================================================== (E) RECORD-TIME WF
    P("\n" + "=" * 100)
    P(f"(E) RECORD-TIME WALK-FORWARD -- alphabet learned on files dated <= {RECORD_SPLIT}")
    P("=" * 100)
    is_files = [f for f in files if f.name[:10] <= RECORD_SPLIT]
    oos_files = [f for f in files if f.name[:10] > RECORD_SPLIT]
    _, _, vocab_is, _, _, tot_is, _ = census(is_files, spytab)
    Fo_free, _, _, _, _, tot_o, _ = census(oos_files, spytab)
    Fo_lock, _, _, _, _, tot_o2, _ = census(oos_files, spytab, vocab=vocab_is)
    free = int(Fo_free["R4_STATS_PANEL_named"].sum()) / max(tot_o, 1)
    lock = int(Fo_lock["R4_STATS_PANEL_named"].sum()) / max(tot_o2, 1)
    P(f"  IS  files {len(is_files):,} ({tot_is:,} FAIL rows) -> vocabulary of "
      f"{len(vocab_is):,} (rung, column) pairs")
    P(f"  OOS files {len(oos_files):,} ({tot_o:,} FAIL rows)")
    P(f"     recovery with the FULL vocabulary   : {free:.1%}")
    P(f"     recovery with the IS-ONLY vocabulary: {lock:.1%}   ratio "
      f"{(lock/free if free else float('nan')):.3f}")
    dump(pd.DataFrame([dict(split="IS", files=len(is_files), fail_rows=tot_is,
                            vocab=len(vocab_is)),
                       dict(split="OOS_full_vocab", files=len(oos_files), fail_rows=tot_o,
                            recovery=free),
                       dict(split="OOS_IS_vocab", files=len(oos_files), fail_rows=tot_o2,
                            recovery=lock)]), "recordwf.csv")

    # ================================================================== (F) CLAUSE PRICING
    P("\n" + "=" * 100)
    P("(F) PRICING THE REPORTING CLAUSE")
    P("=" * 100)
    resid = totA - r4n
    resid_files = FA[(FA.R4_STATS_PANEL_named + 0) < FA.n_fail]
    bytes_cost = totA * 12                                   # ~12 chars for "L1_H1+L4_DD"
    P(f"  CLAUSE: every committed row carrying a 4b verdict also carries a `fail4b` string.")
    P(f"    rows it would have made adjudicable that NO post-hoc rule reaches: {resid:,} "
      f"({resid/max(totA,1):.1%})")
    P(f"    files still wholly or partly silent after the ladder: "
      f"{int((FA.R4_STATS_PANEL_named < FA.n_fail).sum()):,} of {len(FA):,}")
    P(f"    cost: 1 column, ~{bytes_cost/1e6:.1f} MB over the whole record "
      f"({bytes_cost/max(sum(f.stat().st_size for f in files),1):.2%} of its committed CSV bytes)")
    P(f"    rows the ladder DOES rescue (the clause is worth less than the ladder there): "
      f"{r4n - r0n:,} ungated, {gated_lo - r0n:,}..{gated_hi - r0n:,} once the rebuild has to "
      f"verify against the file's own committed legs")
    P(f"    -> the clause's real price is the FIDELITY-GATED residue: "
      f"{totA - gated_hi:,}..{totA - gated_lo:,} rows ({(totA-gated_hi)/max(totA,1):.1%}.."
      f"{(totA-gated_lo)/max(totA,1):.1%}) that no post-hoc rule adjudicates at all.")
    dump(resid_files[["file", "n_fail"] + [f"{r}_named" for r in RUNGS]].sort_values(
        "n_fail", ascending=False), "residue.csv")

    # ================================================================== (G) PROTOCOL rule 8
    P("\n" + "=" * 100)
    P("(G) PROTOCOL RULE 8 -- book chosen on 2009-2016 ALONE, 2017-2026 read ONCE")
    P("=" * 100)
    spy_r = px["SPY"].pct_change().fillna(0.0).values
    spy_m = RN.pack(spy_r)
    v2 = RN.run(rules_v2_weights(px, BAND0, GROSS0).values, COST0)[0]
    v2_m = RN.pack(v2)
    P(f"  SPY        FULL {spy_m['CAGR']:>7.2%} / {spy_m['Sharpe']:.3f} / {spy_m['MaxDD']:>7.2%}"
      f"   H1 {spy_m['H1']:.3f}  H2 {spy_m['H2']:.3f}"
      f"   OOS {spy_m['OOS_CAGR']:>7.2%} / {spy_m['OOS_Sharpe']:.3f} / {spy_m['OOS_MaxDD']:>7.2%}")
    P(f"  RULES v2   FULL {v2_m['CAGR']:>7.2%} / {v2_m['Sharpe']:.3f} / {v2_m['MaxDD']:>7.2%}"
      f"   H1 {v2_m['H1']:.3f}  H2 {v2_m['H2']:.3f}"
      f"   OOS {v2_m['OOS_CAGR']:>7.2%} / {v2_m['OOS_Sharpe']:.3f} / {v2_m['OOS_MaxDD']:>7.2%}")
    wf = []
    for cost in COSTS:
        spy_c = RN.pack(spy_r)
        base_c = RN.pack(RN.run(rules_v2_weights(px, BAND0, GROSS0).values, cost)[0])
        packs = {}
        for bk, Wg in W.items():
            r, tn = RN.run(Wg, cost)
            packs[bk] = RN.pack(r)
        ispick = max(packs, key=lambda b: packs[b]["IS_Sharpe"])
        for bk, m in packs.items():
            ok4b, sig = legs4b(m, spy_c)
            ok4a = (m["H1"] > base_c["H1"] and m["H2"] > base_c["H2"]
                    and m["MaxDD"] >= base_c["MaxDD"])
            wf.append(dict(cost=cost, book=bk, arm=("IS_PICK" if bk == ispick else "reported"),
                           CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m["H1"],
                           H2=m["H2"], IS_Sharpe=m["IS_Sharpe"], OOS_CAGR=m["OOS_CAGR"],
                           OOS_Sharpe=m["OOS_Sharpe"], OOS_MaxDD=m["OOS_MaxDD"],
                           spy_OOS_CAGR=spy_c["OOS_CAGR"], spy_OOS_Sharpe=spy_c["OOS_Sharpe"],
                           spy_OOS_MaxDD=spy_c["OOS_MaxDD"], pass4b=ok4b, pass4a=ok4a,
                           fail4b=sig))
    WF = pd.DataFrame(wf)
    P("\n   cost book     arm       CAGR   Sharpe   MaxDD      H1     H2 | OOS CAGR  Sh     DD  "
      "| 4a  4b  binding leg")
    for r in WF.itertuples():
        P(f"   {r.cost:>4.0f} {r.book:<8} {r.arm:<8} {r.CAGR:>6.2%} {r.Sharpe:>7.3f} "
          f"{r.MaxDD:>7.2%} {r.H1:>6.3f} {r.H2:>6.3f} | {r.OOS_CAGR:>7.2%} {r.OOS_Sharpe:>5.3f} "
          f"{r.OOS_MaxDD:>7.2%} | {str(r.pass4a):>5} {str(r.pass4b):>5}  {r.fail4b}")
    dump(WF, "walkforward.csv")
    p10 = WF[WF.cost == COST0]
    ispick = p10[p10.arm == "IS_PICK"].iloc[0]
    canon = p10[p10.book == "TOP20"].iloc[0]
    P(f"\n  IS-chosen book at 10 bps: {ispick.book} (IS Sharpe {ispick.IS_Sharpe:.3f}) -> OOS "
      f"{ispick.OOS_CAGR:.2%} / {ispick.OOS_Sharpe:.3f} / {ispick.OOS_MaxDD:.2%}, "
      f"4a {ispick.pass4a}, 4b {ispick.pass4b} (binds on {ispick.fail4b})")
    P(f"  canonical TOP20 at 10 bps: OOS {canon.OOS_CAGR:.2%} / {canon.OOS_Sharpe:.3f} / "
      f"{canon.OOS_MaxDD:.2%}, 4a {canon.pass4a}, 4b {canon.pass4b} (binds on {canon.fail4b})")
    P(f"  4a PASS {int(WF.pass4a.sum())} of {len(WF)} grid points; 4b PASS "
      f"{int(WF.pass4b.sum())} of {len(WF)}.  EVERY row above names its binding leg -- that is "
      f"the clause this run prices, applied to this run.")

    # ================================================================== (H) HYPOTHESES
    P("\n" + "=" * 100)
    P("(H) PRE-REGISTERED BARS")
    P("=" * 100)
    hyp = [
        dict(H="H_RECOVER", bar=">= 50% of 944's UNRECOVERABLE rows get a named binding leg",
             stat=f"{r4n - r0n:,} of {silent0:,} = {rec_of_silent:.1%} ungated; "
                  f"FIDELITY-GATED {gsil_lo:.1%}..{gsil_hi:.1%}; TEXT-ONLY (R0-R2, no modelling) "
                  f"{(int(FA.R2_LEGCOLS_named.sum())-r0n)/max(silent0,1):.1%}",
             verdict="PASS" if rec_of_silent >= 0.50 else "FAIL"),
        dict(H="H_FIDELITY", bar=">= 90% exact agreement text vs statistics",
             stat=f"{fid_rate:.1%} on {agree+differ:,} doubly-covered rows; idea 161's per-file "
                  f"gate {len(clean)}/{len(ffiles)} files exact",
             verdict="PASS" if fid_rate >= 0.90 else "FAIL"),
        dict(H="H_BIAS", bar="L4_DD-alone and L5_CAGR-alone shares move <= 5 pp",
             stat=f"on the TRUSTWORTHY text-only recoveries L4_DD {dd_move:+.1f} pp, L5_CAGR "
                  f"{cg_move:+.1f} pp; including the statistics rungs {dd_move_all:+.1f} / "
                  f"{cg_move_all:+.1f} pp",
             verdict="PASS" if max(dd_move, cg_move) <= 5 else "FAIL"),
        dict(H="H_CLAIMSET", bar="headline recoverable share moves <= 10 pp ROW- vs FILE-WEIGHTED",
             stat=f"{dclaim*100:.1f} pp", verdict="PASS" if dclaim <= 0.10 else "FAIL"),
        dict(H="H_WFRULE", bar="IS-only vocabulary keeps >= 90% of the full-vocabulary recovery "
                               "on later files",
             stat=f"{lock:.1%} vs {free:.1%}, ratio {(lock/free if free else np.nan):.3f}",
             verdict="PASS" if (free and lock / free >= 0.90) else "FAIL"),
        dict(H="H_WF", bar="rule 8 run, both KEEP paths, every row names its leg",
             stat=f"4a {int(WF.pass4a.sum())}/{len(WF)}, 4b {int(WF.pass4b.sum())}/{len(WF)}; "
                  f"IS pick {ispick.book} OOS Sharpe {ispick.OOS_Sharpe:.3f} vs SPY "
                  f"{ispick.spy_OOS_Sharpe:.3f}",
             verdict="RUN"),
    ]
    for h in hyp:
        P(f"  {h['H']:<12} {h['verdict']:<5} {h['stat']}")
        P(f"               (bar {h['bar']})")
    dump(pd.DataFrame(hyp), "hypotheses.csv")

    P("\n" + "=" * 100)
    P(f"  elapsed {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"  wrote {STEM}.console.txt")


if __name__ == "__main__":
    main()
