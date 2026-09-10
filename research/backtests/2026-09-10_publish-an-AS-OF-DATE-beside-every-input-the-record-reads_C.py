#!/usr/bin/env python3
"""Idea 629 - publish an AS-OF DATE beside every input the record reads.  (lane C, 2026-09-10)

THE QUEUE'S QUESTION
    Idea 623 built the DATING certificate (T2: truncation invariance -- key(inputs)[t] must equal
    key(inputs truncated to <= t)[t]) and reported it PERFECT on the terminal-dating axis, TP 10 /
    FP 0 / FN 0 / TN 10.  But T2 could truncate idea 195's shares snapshot only because idea 623
    HANDED it an as-of date (`shares_asof = px.index[-1]`, its own G5 assumption).  The date is not
    in the file.  `research/deepvalue/universe_under2b.csv` carries no date column at all.  The
    queue asks: census every file the record reads for whether its dating is recoverable AT ALL,
    and price an as-of-date field as a required column.

THE CLAIM UNDER TEST
    Without a published as-of date, an exogenous input cannot be truncated, so T2 passes it
    through at every probe date and clears every key built on it.  T1 (the SCALE certificate,
    px -> px x diag(c)) never touches exogenous inputs at all, so it is INVARIANT to the dating
    rule by construction.  If both hold, then for the record's UNDATED files both certificates are
    structurally blind and idea 623's headline is a statement about idea 195's courtesy, not about
    the record.

    The sharper form, which PART B tests directly: T2's reading under NO COLUMN is IDENTICAL to
    its reading under a genuinely EARLY as-of date (a value that really was knowable in 2010).
    The certificate therefore cannot distinguish an honest early-dated input from a terminal
    snapshot.  That is an IDENTIFICATION failure, not a power failure, and a column fixes it.

PARTS
    A  CENSUS.  Every data file under data/, research/deepvalue/, research/tenders/, the two
       universe JSONs and the pinned artefacts in research/backtests/, classified by whether its
       dating is recoverable from the file itself, crossed with how many committed scripts read it
       and how many of those run PROTOCOL 8.
    B  INSTRUMENT.  Idea 623's 20-key corpus, T1 and T2 re-run under three DATING RULES for the
       one exogenous input (the shares snapshot).  Confusion matrices per rule.
    C  CONSEQUENCE + RULE 8.  The certificate priced as a pre-rule-8 gate under each dating rule
       on idea 195's SMALL430 grid: 20 keys x 2 dirs x 3 m x 3 cost rungs = 360 arms, ALL
       reported; PROTOCOL 4a/4b on every one; PROTOCOL 8 picks (KEY, dir, m) on 2010-2016 IS
       Sharpe among the admitted set and 2017-2026 is read exactly once.
    D  PREDICTIONS scored, and a PROTOCOL wording proposal (report-only, NOT applied).

TUNED PARAMETERS: exactly two, as the queue specifies.
    (1) FILE CLASS -- the census dial: STRICT (only an as_of / asof / scan_date / pinned_utc /
        snapshot_date column counts as a knowledge date) vs LOOSE (any date-parsing column
        counts).  Both readings reported for every file in .census.csv.
    (2) DATING RULE -- NONE / ASOF_TRUE / ASOF_EARLY, the gate dial for PARTS B and C.
    The book's (KEY, dir, m) are NOT tuned by this run: every one of the 360 arms is reported and
    the choice among them is made by PROTOCOL 8's own IS-only selector.  Certificate tolerance is
    fixed at idea 433's one rank step (not tuned); the tol-0 reading is printed beside it.

PRE-REGISTERED PREDICTIONS (scored in PART D, before any of them is read)
    P1  Gates G1-G5 pass at their stated tolerances.
    P2  At least one file that is read by a rule-8-running committed script has NO recoverable
        dating under BOTH file-class readings.
    P3  T1's flags are bit-identical across all three dating rules (structural invariance).
    P4  T2 under NONE and T2 under ASOF_EARLY are bit-identical on every key, while their ground
        truths differ -- the identification failure.
    P5  Under NONE the rule-8 pick is a terminal-dated key and beats SPY out of sample; under
        ASOF_TRUE the pick is causal and does not.  Scored on BOTH gate forms and reported per
        form; the headline reading is idea 623's recommended T1&T2 gate.
    P6  4a 0 / 360 and 4b 0 / 360 (idea 195's drawdown-cap result on the same panel).

SURVIVORSHIP, as PROTOCOL 9 requires: PART C runs on idea 195's SMALL430 -- current constituents
    of a sub-$2B screen (data/SMALL_PANEL_README.md), intersected with the names that still file
    today, and carrying idea 623's terminal-dated `max_1d_move` screen (kept to match the
    published convention; idea 627 priced it at a median +0.0496 Sharpe in the other direction).
    A survivor of a survivor: every PART C number is biased in the tilt's favour.  PARTS A, B and
    D do not depend on the panel.

Costs 10 bps (PROTOCOL 2) with 0 and 25 bps reported; weights at close t applied t+1 (engine).
Deterministic, standalone:
    python research/backtests/2026-09-10_publish-an-AS-OF-DATE-beside-every-input-the-record-reads_C.py
Writes .console.txt .census.csv .certs.csv .confusion.csv .arms.csv .gates.csv .walkforward.csv
"""
import gzip
import json
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import (load_universe, load_volume, rules_v1_weights,  # noqa: E402
                      rules_v2_weights)
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-10_publish-an-AS-OF-DATE-beside-every-input-the-record-reads_C"
OUT = ROOT / "research" / "backtests"
PARENT195 = "2026-09-10_market-cap-as-the-third-substitution_B"
PARENT623 = "2026-09-10_does-a-TERMINAL-DATING-certificate-belong-BEFORE-rule-8_B"
SHARES_PIN = OUT / f"{PARENT195}.shares.csv"          # idea 565's pinning convention, read-only

# ---- inherited verbatim from ideas 181/185/193/195/623 so the published cells stay comparable
SEED = 629
N, GROSS, FREQ, MAXVOL = 20, 0.75, "W", 0.60
MS = [0.20, 0.50, 1.00]
DIRS = {"POS": 1.0, "NEG": -1.0}
COSTS = [0.0, 10.0, 25.0]
IS_END = pd.Timestamp("2016-12-31")
OOS_LO = IS_END + pd.Timedelta(days=1)
PHI, DELTA = 0.70, 0.60
REPRO_TOL = 5e-3
TOL_STEPS = 1.0                                       # idea 433's recommended one rank step

N_SCALE_DRAWS = 8
PROBE_FRAC = [0.35, 0.50, 0.65, 0.80, 0.95]

DATING_RULES = ["NONE", "ASOF_TRUE", "ASOF_EARLY"]

_console = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _console.append(s)


def rankpct(df):
    return df.rank(axis=1, pct=True)


# ------------------------------------------------------------------ vectorised engine equivalent
def fast_backtest(prices, weights, freq=FREQ):
    """(gross returns at 0 bps, turnover).  Costs applied through r(c) = r(0) - turnover*c/1e4;
    gate G2 checks that identity against a live engine run."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy()
    m[0] = True
    T, Ncol = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, Ncol)), C[:-1]])
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    port = (held * rets).sum(axis=1)
    return pd.Series(port, index=idx), pd.Series(turn, index=idx)


# ============================================================== PART A: the input-file census
# A KNOWLEDGE date says when a value became knowable.  An EVENT date says when something happened
# (a transaction, an expiry, a name's first/last trading day) and does NOT license reading the
# row's payload at that date.  FILE CLASS is the dial: STRICT counts only knowledge-date names;
# LOOSE counts any column whose values parse as dates.
KNOWLEDGE_NAMES = re.compile(
    r"^(as_?of(_date)?|asof|scan_date|snapshot_date|pinned_utc|pull_date|retrieved(_at)?|"
    r"filing_date|report_date|published(_at)?|fetched(_at)?)$", re.I)
INDEX_NAMES = re.compile(r"^(date|datetime|day|unnamed: 0|)$", re.I)
RULE8_MARKS = [r"IS_END", r"OOS_LO", r"walk[_ ]?forward", r"walkforward", r"\bOOS\b",
               r"2016-12-31", r"2017-01-01", r"rule[_ ]?8"]


def _parses_as_dates(vals):
    """>=95% of the non-null sample parses as a date, and the parsed range is plausible."""
    s = pd.Series([v for v in vals if v is not None and str(v).strip() not in ("", "nan")])
    if len(s) < 3:
        return False
    d = pd.to_datetime(s, errors="coerce", format="mixed", utc=True)
    if d.notna().mean() < 0.95:
        return False
    yr = d.dt.year.dropna()
    return bool(len(yr) and yr.min() >= 1990 and yr.max() <= 2100)


def _sample_table(path, nrows=200):
    """(columns, {col: sample values}) for a csv/csv.gz; (None, None) for anything else."""
    opener = gzip.open if path.name.endswith(".gz") else open
    try:
        with opener(path, "rt", errors="replace") as fh:
            head = [fh.readline() for _ in range(nrows + 1)]
    except Exception:
        return None, None
    head = [h for h in head if h]
    if len(head) < 2:
        return None, None
    from io import StringIO
    try:
        df = pd.read_csv(StringIO("".join(head)), dtype=str, low_memory=False)
    except Exception:
        return None, None
    return list(df.columns), {c: df[c].tolist() for c in df.columns}


def classify_file(path):
    """Dating recoverability of ONE input file, under both FILE CLASS readings."""
    cols, samp = _sample_table(path)
    if cols is None:
        # not a table: JSON name lists, manifests, blobs.  No per-row dating by construction.
        return dict(kind="non-table", n_cols=0, date_cols="", knowledge_cols="",
                    index_dated=False, class_STRICT="UNDATED", class_LOOSE="UNDATED")
    date_cols = [c for c in cols if _parses_as_dates(samp[c])]
    know_cols = [c for c in date_cols if KNOWLEDGE_NAMES.match(str(c).strip())]
    index_dated = bool(cols and INDEX_NAMES.match(str(cols[0]).strip()) and cols[0] in date_cols)
    if index_dated:
        cS = cL = "INDEX_DATE"                      # a dated row index: exact per-row as-of
    else:
        cS = "ROW_KNOWLEDGE" if know_cols else "UNDATED"
        cL = "ROW_KNOWLEDGE" if know_cols else ("ROW_EVENT_ONLY" if date_cols else "UNDATED")
    return dict(kind="table", n_cols=len(cols), date_cols=";".join(map(str, date_cols)),
                knowledge_cols=";".join(map(str, know_cols)), index_dated=index_dated,
                class_STRICT=cS, class_LOOSE=cL)


def git_last_commit(path):
    try:
        r = subprocess.run(["git", "log", "-1", "--format=%cI", "--", str(path)],
                           cwd=ROOT, capture_output=True, text=True, timeout=30)
        return (r.stdout or "").strip()[:10] or "(untracked)"
    except Exception:
        return "(unavailable)"


def input_file_corpus():
    """Every data file the record can read, plus the pinned artefacts."""
    pats = [("data", "data/*.csv"), ("data", "data/*.csv.gz"), ("data", "data/options/*"),
            ("universe", "research/*.json"),
            ("deepvalue", "research/deepvalue/*.csv"), ("deepvalue", "research/deepvalue/data/*"),
            ("deepvalue", "research/deepvalue/filings/*.json"),
            ("tenders", "research/tenders/*.csv"),
            ("pinned", "research/backtests/*.shares.csv")]
    seen, rows = set(), []
    for group, pat in pats:
        for p in sorted(ROOT.glob(pat)):
            if p.is_dir() or p in seen:
                continue
            seen.add(p)
            rows.append((group, p))
    return rows


def script_corpus():
    ps = sorted(list((ROOT / "research").glob("*.py"))
                + list((ROOT / "research" / "backtests").glob("*.py"))
                + list((ROOT / "products").rglob("*.py")))
    out = []
    for p in ps:
        if p.name == Path(__file__).name:
            continue
        src = p.read_text(errors="replace")
        out.append((p, src, any(re.search(m, src) for m in RULE8_MARKS)))
    return out


# ================================================================== PART B: the key corpus (623)
def _entry(px):
    fv = px.apply(lambda s: s.loc[s.first_valid_index()] if s.first_valid_index() is not None
                  else np.nan)
    out = pd.DataFrame(np.tile(fv.values, (len(px), 1)), index=px.index, columns=px.columns)
    return out.where(px.notna())


def _term(px):
    lv = px.apply(lambda s: s.loc[s.last_valid_index()] if s.last_valid_index() is not None
                  else np.nan)
    out = pd.DataFrame(np.tile(lv.values, (len(px), 1)), index=px.index, columns=px.columns)
    return out.where(px.notna())


def _bcast(vec, px):
    return pd.DataFrame(np.tile(np.asarray(vec, float), (len(px), 1)),
                        index=px.index, columns=px.columns).where(px.notna())


def _composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (rankpct(mom) + rankpct(r6) + rankpct(r3)) / 3


# Idea 623's corpus verbatim.  `uses_exog` marks the keys whose inputs include the ONE exogenous
# (non-price-panel) series -- the shares snapshot.  Those are the keys the as-of column decides.
#                     fn(px, vol, shares)                       scale  term  family     uses_exog
KEY_SPECS = {
    "MOM":      (lambda p, v, s: _composite(p),                  False, False, "causal",   False),
    "R6":       (lambda p, v, s: rankpct(p / p.shift(126) - 1),   False, False, "causal",   False),
    "DDTR":     (lambda p, v, s: rankpct(p / p.rolling(252).max() - 1), False, False, "causal", False),
    "REBASED":  (lambda p, v, s: rankpct(p / _entry(p)),          False, False, "causal",   False),
    "VOL20":    (lambda p, v, s: rankpct(p.pct_change().rolling(20).std()), False, False, "causal", False),
    "VOLSH":    (lambda p, v, s: rankpct(v.rolling(20).mean()),   False, False, "causal",   False),
    "PRICE":    (lambda p, v, s: rankpct(p),                      True,  False, "level",    False),
    "FROZEN":   (lambda p, v, s: rankpct(_entry(p)),              True,  False, "level",    False),
    "DVOL":     (lambda p, v, s: rankpct((p * v).rolling(20).mean()), True, False, "level",  False),
    "PXDVOL":   (lambda p, v, s: rankpct(p * v.rolling(20).mean()), True, False, "level",   False),
    "MCAP":     (lambda p, v, s: rankpct(p * _bcast(s, p)),       True,  True,  "both",     True),
    "MCAPFRZ":  (lambda p, v, s: rankpct(_entry(p) * _bcast(s, p)), True, True,  "both",    True),
    "PXTERM":   (lambda p, v, s: rankpct(_term(p)),               True,  True,  "both",     False),
    "FWDRET":   (lambda p, v, s: rankpct(_term(p) / p - 1.0),     False, True,  "termonly", False),
    "TERMREB":  (lambda p, v, s: rankpct(p / _term(p)),           False, True,  "termonly", False),
    "MCAPREB":  (lambda p, v, s: rankpct((p / _entry(p)) * _bcast(s, p)), False, True, "termonly", True),
    "SHARES":   (lambda p, v, s: rankpct(_bcast(s, p)),           False, True,  "termonly", True),
    "FULLVOL":  (lambda p, v, s: rankpct(_bcast(p.pct_change().std(), p)), False, True, "termonly", False),
    "FULLSHRP": (lambda p, v, s: rankpct(_bcast(p.pct_change().mean() / p.pct_change().std(), p)),
                 False, True, "termonly", False),
    "MAXMOVE":  (lambda p, v, s: rankpct(_bcast(p.pct_change().abs().max(), p)),
                 False, True, "termonly", False),
}


def truth_term_dated(key, rule):
    """Ground truth on the dating axis UNDER a dating rule.  The two rules that pass the snapshot
    through differ in WHY: under NONE the value is still a terminal snapshot (the record simply
    cannot see that), while ASOF_EARLY is the counterfactual world in which the same value really
    was knowable from the panel's first day, so a key built on it is causal.  Everything not built
    on the exogenous input has a rule-independent truth."""
    _, _, tdate, _, exog = KEY_SPECS[key]
    if not exog:
        return tdate
    if rule == "ASOF_EARLY":
        # the exogenous leg is honest; the key is terminal-dated only if its PRICE leg is.
        return False
    return True


def _rank_int(k):
    return k.rank(axis=1, method="first")


def _perday_max(d):
    ok = d.notna().sum(axis=1) >= 20
    return d.max(axis=1).where(ok)


def disp_T1(fn, px, vol, shares, rng):
    """Idea 433's SCALE certificate: order-invariance under px -> px x diag(c).  It never touches
    the exogenous input, so it is invariant to the dating rule by construction (P3)."""
    base = _rank_int(fn(px, vol, shares))
    gmax, per = 0.0, None
    for _ in range(N_SCALE_DRAWS):
        c = pd.Series(np.exp(rng.normal(0.0, 1.0, size=px.shape[1])), index=px.columns)
        alt = _rank_int(fn(px.mul(c, axis=1), vol, shares))
        d = (base - alt).abs()
        gmax = max(gmax, float(np.nanmax(d.values)) if d.notna().any().any() else 0.0)
        pm = _perday_max(d)
        per = pm if per is None else pd.concat([per, pm], axis=1).max(axis=1)
    med = float(np.nanmedian(per.values)) if per is not None and per.notna().any() else 0.0
    return gmax, med


def disp_T2(fn, px, vol, shares, exog_asof):
    """Idea 623's DATING certificate.  `exog_asof` is the as-of date the exogenous input PUBLISHES.
    None means the file publishes no date at all: there is nothing to compare t against, so the
    certificate has no licence to withhold the series and passes it through -- which is exactly
    what an UNDATED file forces on any reader."""
    base = _rank_int(fn(px, vol, shares))
    nan_shares = shares * np.nan
    per = []
    for f in PROBE_FRAC:
        t = px.index[int(f * (len(px) - 1))]
        s_t = shares if (exog_asof is None or exog_asof <= t) else nan_shares
        alt = _rank_int(fn(px.loc[:t], vol.loc[:t], s_t))
        b, a = base.loc[t], alt.loc[t]
        if bool((b.notna() & a.isna()).any()):
            return float("inf"), float("inf")
        d = (b - a).abs()
        per.append(float(np.nanmax(d.values)) if d.notna().any() else 0.0)
    return float(max(per)), float(np.median(per))


# --------------------------------------------------------------------------------------- metrics
def win(r, lo=None, hi=None):
    if lo is not None:
        r = r.loc[lo:]
    if hi is not None:
        r = r.loc[:hi]
    return r


def full_row(r):
    h = len(r) // 2
    out = {}
    for tag, x in (("F", r), ("H1", r.iloc[:h]), ("H2", r.iloc[h:]),
                   ("IS", win(r, hi=IS_END)), ("OOS", win(r, lo=OOS_LO))):
        m = metrics(x)
        out[f"CAGR_{tag}"], out[f"Sharpe_{tag}"], out[f"MaxDD_{tag}"] = \
            m["CAGR"], m["Sharpe"], m["MaxDD"]
    return out


def pass4a(row, base):
    return bool(row["Sharpe_H1"] > base["Sharpe_H1"] and row["Sharpe_H2"] > base["Sharpe_H2"]
                and row["MaxDD_F"] >= base["MaxDD_F"])


def pass4b(row, spy):
    return bool(row["Sharpe_H1"] > spy["Sharpe_H1"] and row["Sharpe_H2"] > spy["Sharpe_H2"]
                and row["Sharpe_OOS"] > spy["Sharpe_OOS"]
                and row["MaxDD_F"] >= DELTA * spy["MaxDD_F"]
                and row["CAGR_F"] >= PHI * spy["CAGR_F"])


def confusion(flags, truth):
    tp = sum(1 for k in flags if flags[k] and truth[k])
    fp = sum(1 for k in flags if flags[k] and not truth[k])
    fn = sum(1 for k in flags if not flags[k] and truth[k])
    tn = sum(1 for k in flags if not flags[k] and not truth[k])
    return tp, fp, fn, tn


# ============================================================================================ run
def main():
    t_start = time.time()
    preds = {}

    # ---------------------------------------------------------------------------- panel (as 195)
    pxF = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    pxF = pxF[[c for c in pxF.columns if c == "SPY" or c not in bad]]
    pin = pd.read_csv(SHARES_PIN)
    shares = pin.set_index("ticker")["shares"]
    covered = [c for c in pxF.columns if c != "SPY" and c in shares.index]
    px = pxF[covered]
    spy_px = pxF["SPY"]
    vol = load_volume(small=True).reindex(index=px.index, columns=px.columns)
    sh = shares.reindex(px.columns)
    start = px.index[260]
    ev = px.index[260:]

    ASOF = {"NONE": None, "ASOF_TRUE": px.index[-1], "ASOF_EARLY": px.index[0]}

    say("=" * 112)
    say(f"IDEA 629 - publish an AS-OF DATE beside every input the record reads   (lane C, "
        f"{pd.Timestamp.now('UTC').date()})")
    say("=" * 112)
    say(f"Panel SMALL{len(covered)} (idea 195's leg-(c) panel, reproduced): {px.shape[1]} names, "
        f"{px.index[0].date()}..{px.index[-1].date()}, SPY benchmark only.")
    say(f"Shares snapshot from the PINNED artefact {SHARES_PIN.name} (idea 565), {len(pin)} rows.")
    say("Tuned parameters: FILE CLASS (STRICT/LOOSE) and DATING RULE (NONE/ASOF_TRUE/ASOF_EARLY).")
    say("")

    # ================================================================= GATES (pre-registered)
    say("-" * 112)
    say("GATES (five, pre-registered)")
    gates = []
    comp = _composite(px)
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    elig = (px > px.rolling(200).mean()) & (vol20 < MAXVOL)
    rk = comp.where(elig).rank(axis=1, ascending=False)
    wctl = (rk <= N).astype(float) * (GROSS / N)

    eng0 = backtest(px, wctl, cost_bps=0.0, freq=FREQ)
    g0, t0turn = fast_backtest(px, wctl)
    g1r = float(np.abs(eng0["returns"].loc[ev].values - g0.loc[ev].values).max())
    g1t = float(np.abs(eng0["turnover"].loc[ev].values - t0turn.loc[ev].values).max())
    say(f"  G1  fast_backtest == engine.backtest (control book)      returns {g1r:.3e}  "
        f"turnover {g1t:.3e}   [tol 1e-12, evaluation window]")
    gates.append(dict(gate="G1_fast_vs_engine", value=max(g1r, g1t), tol=1e-12,
                      passed=max(g1r, g1t) < 1e-12))

    eng25 = backtest(px, wctl, cost_bps=25.0, freq=FREQ)
    derived = g0 - t0turn * 25.0 / 1e4
    g2 = float(np.abs(eng25["returns"].loc[ev].values - derived.loc[ev].values).max())
    say(f"  G2  cost-rung identity r(c)=r(0)-turnover*c/1e4 @25bps    {g2:.3e}   [tol 1e-12]")
    gates.append(dict(gate="G2_rung_identity", value=g2, tol=1e-12, passed=g2 < 1e-12))

    # G3: reproduce idea 623's committed certificate readings under ITS dating rule (ASOF_TRUE)
    c623 = pd.read_csv(OUT / f"{PARENT623}.certs.csv").set_index("key")

    # G4: a causal scale-free control clears BOTH certificates at tol 0 under EVERY dating rule
    ident = lambda p, v, s: rankpct(p / p.shift(21) - 1.0)   # noqa: E731
    x1, m1 = disp_T1(ident, px, vol, sh, np.random.default_rng(SEED + 1))
    worst = m1
    for rule in DATING_RULES:
        _, m2 = disp_T2(ident, px, vol, sh, ASOF[rule])
        worst = max(worst, m2)
    say(f"  G4  control key clears T1 and T2 under all 3 dating rules  worst median {worst:.3e}   "
        f"[tol 0 exactly]")
    gates.append(dict(gate="G4_control_key", value=worst, tol=0.0, passed=worst == 0.0))

    # ============================================================ PART A -- THE CENSUS
    say("")
    say("=" * 112)
    say("PART A  CENSUS: is each input file's dating recoverable FROM THE FILE?")
    say("        INDEX_DATE = dated row index (exact per-row as-of).  ROW_KNOWLEDGE = a column "
        "saying when the row")
    say("        became knowable.  ROW_EVENT_ONLY = dates, but only of EVENTS (LOOSE reading "
        "only).  UNDATED = none.")
    say("=" * 112)
    scripts = script_corpus()
    crows = []
    for group, p in input_file_corpus():
        rel = str(p.relative_to(ROOT))
        info = classify_file(p)
        readers = [(sp, r8) for sp, src, r8 in scripts if p.name in src]
        crows.append(dict(group=group, file=rel, size_kb=round(p.stat().st_size / 1024, 1),
                          n_readers=len(readers), n_readers_rule8=sum(1 for _, r8 in readers if r8),
                          git_last_commit=git_last_commit(p), **info))
    cen = pd.DataFrame(crows).sort_values(["group", "file"]).reset_index(drop=True)
    cen.to_csv(OUT / f"{STEM}.census.csv", index=False)

    say(f"  {len(cen)} input files censused across "
        f"{cen['group'].nunique()} groups; {int((cen.n_readers > 0).sum())} are read by at least "
        f"one committed script, {int((cen.n_readers_rule8 > 0).sum())} by a rule-8-running one.")
    say("")
    for dial in ("class_STRICT", "class_LOOSE"):
        vc = cen[dial].value_counts()
        vcr = cen[cen.n_readers_rule8 > 0][dial].value_counts()
        say(f"  FILE CLASS = {dial.split('_')[1]:6s}  all files: " +
            "  ".join(f"{k} {v}" for k, v in vc.items()))
        say(f"  {'':21s}read by rule-8 scripts: " +
            ("  ".join(f"{k} {v}" for k, v in vcr.items()) or "(none)"))
    say("")
    say("  Every file read by a rule-8-running committed script:")
    say(f"    {'file':52s} {'readers':>7s} {'r8':>3s}  {'STRICT':14s} {'LOOSE':14s} "
        f"{'knowledge cols'}")
    for _, r in cen[cen.n_readers_rule8 > 0].sort_values("n_readers_rule8",
                                                         ascending=False).iterrows():
        say(f"    {r.file[:52]:52s} {r.n_readers:7d} {r.n_readers_rule8:3d}  "
            f"{r.class_STRICT:14s} {r.class_LOOSE:14s} {(r.knowledge_cols or '-')[:40]}")
    blind = cen[(cen.n_readers_rule8 > 0) & (cen.class_STRICT == "UNDATED")
                & (cen.class_LOOSE == "UNDATED")]
    say("")
    say(f"  >>> {len(blind)} file(s) read by a rule-8-running script have NO recoverable dating "
        f"under EITHER reading:")
    for _, r in blind.iterrows():
        say(f"        {r.file}  ({r.n_readers} readers, {r.n_readers_rule8} run rule 8; "
            f"only external dating = git {r.git_last_commit})")
    preds["P2"] = len(blind) >= 1

    # ============================================================ PART B -- THE INSTRUMENT
    say("")
    say("=" * 112)
    say("PART B  INSTRUMENT: T1 and T2 under three DATING RULES for the ONE exogenous input")
    say("        NONE      = the file publishes no as-of date (what an UNDATED file forces).")
    say("        ASOF_TRUE = published as-of is the snapshot day (idea 623's G5 courtesy).")
    say("        ASOF_EARLY= published as-of is the panel's first day: the counterfactual in "
        "which the value")
    say("                    really was knowable in 2010, so a key built on it is CAUSAL.")
    say("=" * 112)
    fwd = px.iloc[-1] / px - 1.0                       # idea 623's definition, verbatim
    certs = []
    for i, (name, (fn, sleak, tdate, fam, exog)) in enumerate(KEY_SPECS.items()):
        x1, m1 = disp_T1(fn, px, vol, sh, np.random.default_rng(SEED + 101 * i))
        k = fn(px, vol, sh)
        vals = []
        for t in px.index[260::63]:
            a, b = k.loc[t], fwd.loc[t]
            msk = a.notna() & b.notna()
            if msk.sum() >= 20:
                ra, rb = a[msk].rank(), b[msk].rank()
                if ra.std() > 0 and rb.std() > 0:
                    vals.append(np.corrcoef(ra, rb)[0, 1])
        ic = abs(float(np.mean(vals))) if vals else np.nan
        for rule in DATING_RULES:
            x2, m2 = disp_T2(fn, px, vol, sh, ASOF[rule])
            certs.append(dict(key=name, family=fam, uses_exog=exog, rule=rule,
                              truth_scale_leak=sleak, truth_term_dated=truth_term_dated(name, rule),
                              T1_flag=bool(m1 > TOL_STEPS), T1_med=m1, T1_max=x1,
                              T2_flag=bool(m2 > TOL_STEPS), T2_med=m2, T2_max=x2,
                              BOTH_flag=bool(m1 > TOL_STEPS or m2 > TOL_STEPS),
                              T1_flag_tol0=bool(m1 > 0.0), T2_flag_tol0=bool(m2 > 0.0),
                              absIC_fwd=float(ic)))
    ce = pd.DataFrame(certs)
    ce.to_csv(OUT / f"{STEM}.certs.csv", index=False)

    # G3 against idea 623's committed readings, under ITS rule.  The T2 median is DETERMINISTIC
    # (fixed probe dates) so it must match exactly; T1's median is a MONTE-CARLO statistic over
    # 8 rescale draws, so only its FLAG is comparable across seeds -- both legs are checked.
    mine = ce[ce.rule == "ASOF_TRUE"].set_index("key")
    common = [k for k in mine.index if k in c623.index]

    def _d(a, b):
        a, b = float(a), float(b)
        return 0.0 if (np.isinf(a) and np.isinf(b)) else abs(a - b)

    g3 = max(_d(mine.loc[k, "T2_med"], c623.loc[k, "T2_med"]) for k in common)
    g3f = sum(1 for k in common if bool(mine.loc[k, "T1_flag"]) == bool(c623.loc[k, "T1_flag"]))
    ok3 = (g3 == 0.0) and g3f == len(common)
    say(f"  G3  idea 623's committed .certs.csv reproduced under ASOF_TRUE on {len(common)}/20 "
        f"keys   max|dT2_med| {g3:.3e} [tol 0 exactly]   T1_flag agreement {g3f}/{len(common)}")
    gates.append(dict(gate="G3_repro_623_certs", value=g3, tol=0.0, passed=ok3))

    # G5: idea 623's leak-content column reproduced (same estimator, same probe dates)
    g5 = max(abs(float(mine.loc[k, "absIC_fwd"]) - float(c623.loc[k, "absIC_fwd"]))
             for k in common)
    say(f"  G5  idea 623's |IC vs realised forward return| reproduced on {len(common)}/20 keys"
        f"          max|d| {g5:.3e}   [tol {REPRO_TOL:g}]")
    gates.append(dict(gate="G5_repro_623_absIC", value=g5, tol=REPRO_TOL, passed=g5 < REPRO_TOL))
    pd.DataFrame(gates).to_csv(OUT / f"{STEM}.gates.csv", index=False)
    preds["P1"] = all(g["passed"] for g in gates)
    say("")

    say(f"  {'key':9s} {'family':9s} {'exog':5s} {'|IC|':>6s} | {'T1med':>6s} {'T1?':>4s} | " +
        " | ".join(f"{r[:10]:>10s} T2med/flag/truth" for r in DATING_RULES))
    for name in KEY_SPECS:
        rows = {r: ce[(ce.key == name) & (ce.rule == r)].iloc[0] for r in DATING_RULES}
        a = rows["NONE"]
        seg = " | ".join(
            f"{rows[r].T2_med:10.1f} {'FLAG' if rows[r].T2_flag else ' ok ':>4s} "
            f"{'T' if rows[r].truth_term_dated else 'F'}" for r in DATING_RULES)
        say(f"  {name:9s} {a.family:9s} {str(bool(a.uses_exog)):5s} {a.absIC_fwd:6.4f} | "
            f"{a.T1_med:6.1f} {'FLAG' if a.T1_flag else ' ok ':>4s} | {seg}")

    # P3: T1 invariant across rules (structural)
    t1piv = ce.pivot_table(index="key", columns="rule", values="T1_med")
    preds["P3"] = bool(np.nanmax(np.abs(t1piv.values - t1piv.values[:, [0]])) == 0.0)
    # P4: T2 under NONE == T2 under ASOF_EARLY on every key, truths differ on the exog keys
    t2n = ce[ce.rule == "NONE"].set_index("key")["T2_med"]
    t2e = ce[ce.rule == "ASOF_EARLY"].set_index("key")["T2_med"]
    same = bool((t2n == t2e).all())
    trn = ce[ce.rule == "NONE"].set_index("key")["truth_term_dated"]
    tre = ce[ce.rule == "ASOF_EARLY"].set_index("key")["truth_term_dated"]
    ndiff = int((trn != tre).sum())
    preds["P4"] = same and ndiff > 0
    say("")
    say(f"  P3 check  max|T1_med(rule) - T1_med(NONE)| over rules = "
        f"{np.nanmax(np.abs(t1piv.values - t1piv.values[:, [0]])):.3e}  -> T1 is "
        f"{'INVARIANT' if preds['P3'] else 'NOT invariant'} to the dating rule.")
    say(f"  P4 check  T2(NONE) == T2(ASOF_EARLY) on all 20 keys: {same};  ground truths differ on "
        f"{ndiff} key(s) ({', '.join(sorted(trn.index[trn != tre]))}).")
    say("            -> the certificate's OUTPUT is identical in a world where the snapshot is "
        "terminal and one")
    say("               where the same value was knowable in 2010.  Without the column this is "
        "UNIDENTIFIED.")

    say("")
    say("  CONFUSION vs the dating ground truth (tol = 1 rank step), per rule and certificate:")
    conf = []
    for rule in DATING_RULES:
        sub = ce[ce.rule == rule].set_index("key")
        truth = sub["truth_term_dated"].to_dict()
        for cert in ("T1", "T2", "BOTH"):
            fl = sub[f"{cert}_flag"].to_dict()
            tp, fp, fn_, tn = confusion(fl, truth)
            conf.append(dict(rule=rule, certificate=cert, TP=tp, FP=fp, FN=fn_, TN=tn,
                             detected=f"{tp}/{tp + fn_}"))
            say(f"    {rule:11s} {cert:5s}  TP {tp:2d}  FP {fp:2d}  FN {fn_:2d}  TN {tn:2d}   "
                f"detection {tp}/{tp + fn_}")
    # the exog-only slice: the keys the as-of column actually decides
    for rule in DATING_RULES:
        sub = ce[(ce.rule == rule) & (ce.uses_exog)].set_index("key")
        truth = sub["truth_term_dated"].to_dict()
        for cert in ("T1", "T2", "BOTH"):
            tp, fp, fn_, tn = confusion(sub[f"{cert}_flag"].to_dict(), truth)
            conf.append(dict(rule=rule, certificate=cert + "_exogonly", TP=tp, FP=fp, FN=fn_,
                             TN=tn, detected=f"{tp}/{tp + fn_}"))
    pd.DataFrame(conf).to_csv(OUT / f"{STEM}.confusion.csv", index=False)
    say("")
    say("  EXOG-ONLY slice (MCAP, MCAPFRZ, MCAPREB, SHARES -- the keys the as-of column decides):")
    for rule in DATING_RULES:
        sub = ce[(ce.rule == rule) & (ce.uses_exog)].set_index("key")
        truth = sub["truth_term_dated"].to_dict()
        tp, fp, fn_, tn = confusion(sub["BOTH_flag"].to_dict(), truth)
        say(f"    {rule:11s} T1&T2  TP {tp}  FP {fp}  FN {fn_}  TN {tn}   "
            f"detection {tp}/{tp + fn_ if (tp + fn_) else 0}")

    # ============================================================ PART C -- CONSEQUENCE + RULE 8
    say("")
    say("=" * 112)
    say("PART C  CONSEQUENCE: the certificate as a PRE-rule-8 gate, under each dating rule")
    say("        Book: score = composite + dir*m*(key-0.5), above own 200d MA, vol20 < 0.60, "
        f"top n={N}, gross {GROSS}, {FREQ}.")
    say("        20 keys x 2 dirs x 3 m x 3 cost rungs = 360 arms; every one written to "
        ".arms.csv.")
    say("=" * 112)
    spy_r = spy_px.pct_change().fillna(0.0).loc[start:]
    spy_row = full_row(spy_r)
    b2 = backtest(px, rules_v2_weights(px), cost_bps=10.0, freq=FREQ)
    b1 = backtest(px, rules_v1_weights(px), cost_bps=10.0, freq=FREQ)
    v2_row = full_row(b2["returns"].loc[start:])
    v1_row = full_row(b1["returns"].loc[start:])
    ctl_row = full_row(g0.loc[start:] - t0turn.loc[start:] * 10.0 / 1e4)

    say(f"  {'comparand':28s} {'CAGR_F':>8s} {'Sh_F':>6s} {'DD_F':>8s} {'Sh_H1':>6s} "
        f"{'Sh_H2':>6s} {'CAGR_OOS':>9s} {'Sh_OOS':>7s} {'DD_OOS':>8s}")
    for nm, rr in (("SPY", spy_row), ("RULES v2 (live baseline)", v2_row),
                   ("RULES v1 (previous)", v1_row), ("CONTROL (no tilt)", ctl_row)):
        say(f"  {nm:28s} {rr['CAGR_F']:8.2%} {rr['Sharpe_F']:6.3f} {rr['MaxDD_F']:8.2%} "
            f"{rr['Sharpe_H1']:6.3f} {rr['Sharpe_H2']:6.3f} {rr['CAGR_OOS']:9.2%} "
            f"{rr['Sharpe_OOS']:7.3f} {rr['MaxDD_OOS']:8.2%}")
    say(f"  4b bars: MaxDD >= {DELTA:.2f} x SPY = {DELTA * spy_row['MaxDD_F']:.2%};  "
        f"CAGR >= {PHI:.2f} x SPY = {PHI * spy_row['CAGR_F']:.2%};  "
        f"Sharpe > SPY in H1 {spy_row['Sharpe_H1']:.3f} / H2 {spy_row['Sharpe_H2']:.3f} / "
        f"OOS {spy_row['Sharpe_OOS']:.3f}")
    say("")

    arms = []
    flagmap = {(r["key"], r["rule"]): (r["T1_flag"], r["T2_flag"]) for _, r in ce.iterrows()}
    for name, (fn, _, _, fam, exog) in KEY_SPECS.items():
        k = fn(px, vol, sh)
        for dname, dsign in DIRS.items():
            for m in MS:
                sc = comp + dsign * m * (k - 0.5)
                rkx = sc.where(elig).rank(axis=1, ascending=False)
                w = (rkx <= N).astype(float) * (GROSS / N)
                gr, tu = fast_backtest(px, w)
                gr, tu = gr.loc[start:], tu.loc[start:]
                turn_yr = float(tu.sum() / (len(tu) / 252))
                for c in COSTS:
                    row = full_row(gr - tu * c / 1e4)
                    rec = dict(key=name, family=fam, uses_exog=exog, dir=dname, m=m, cost=c,
                               turnover_yr=turn_yr, **row)
                    rec["pass4a"] = pass4a(row, v2_row)
                    rec["pass4b"] = pass4b(row, spy_row)
                    for rule in DATING_RULES:
                        f1, f2 = flagmap[(name, rule)]
                        rec[f"admit_T2_{rule}"] = not f2
                        rec[f"admit_BOTH_{rule}"] = not (f1 or f2)
                    arms.append(rec)
    A = pd.DataFrame(arms)
    A.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    say(f"  {len(A)} arms computed and written.  PROTOCOL 4a passes {int(A.pass4a.sum())}/{len(A)}"
        f"; 4b passes {int(A.pass4b.sum())}/{len(A)}.")
    preds["P6"] = bool(A.pass4a.sum() == 0 and A.pass4b.sum() == 0)
    fail = {"CAGR": 0, "DD": 0, "H1": 0, "H2": 0, "OOS": 0}
    for _, r in A.iterrows():
        fail["CAGR"] += r["CAGR_F"] < PHI * spy_row["CAGR_F"]
        fail["DD"] += r["MaxDD_F"] < DELTA * spy_row["MaxDD_F"]
        fail["H1"] += r["Sharpe_H1"] <= spy_row["Sharpe_H1"]
        fail["H2"] += r["Sharpe_H2"] <= spy_row["Sharpe_H2"]
        fail["OOS"] += r["Sharpe_OOS"] <= spy_row["Sharpe_OOS"]
    say(f"  4b failing legs over all {len(A)} arms: " +
        "  ".join(f"{k} {int(v)}" for k, v in sorted(fail.items(), key=lambda z: -z[1])))
    say("")

    # ------------------------------------------------------- RULE 8 under each dating rule
    say("  PROTOCOL 8: (KEY, dir, m) chosen on 2010-2016 IS Sharpe ALONE among the keys the gate "
        "admits;")
    say("              2017-2026 read exactly once.  10 bps.  Both gate forms reported.")
    say("")
    wf = []
    A10 = A[A.cost == 10.0]
    for gate in ("T2", "BOTH"):
        for rule in DATING_RULES:
            adm = A10[A10[f"admit_{gate}_{rule}"]]
            nkeys = adm.key.nunique()
            if adm.empty:
                say(f"    gate {gate:4s} / {rule:11s}: admits 0 keys -- no pick.")
                continue
            pick = adm.loc[adm.Sharpe_IS.idxmax()]
            honest = not truth_term_dated(pick.key, rule)
            # BLIND SPOT: arms the gate admits although their truth is terminal-dated, i.e. the
            # leaks the certificate cannot see under THIS dating rule.  If the selector merely
            # happened not to pick one, the margin says how close it came.
            blindk = [k for k in adm.key.unique() if truth_term_dated(k, rule)]
            badm = adm[adm.key.isin(blindk)]
            b_best = float(badm.Sharpe_IS.max()) if len(badm) else float("nan")
            b_arm = (f"{badm.loc[badm.Sharpe_IS.idxmax(), 'key']}/"
                     f"{badm.loc[badm.Sharpe_IS.idxmax(), 'dir']}") if len(badm) else "-"
            b_oos = float(badm.loc[badm.Sharpe_IS.idxmax(), "Sharpe_OOS"]) if len(badm) else np.nan
            wf.append(dict(gate=gate, rule=rule, n_keys_admitted=nkeys, n_arms_admitted=len(adm),
                           pick_key=pick.key, pick_dir=pick["dir"], pick_m=pick.m,
                           pick_is_causal=honest, Sharpe_IS=pick.Sharpe_IS,
                           CAGR_OOS=pick.CAGR_OOS, Sharpe_OOS=pick.Sharpe_OOS,
                           MaxDD_OOS=pick.MaxDD_OOS, CAGR_F=pick.CAGR_F, Sharpe_F=pick.Sharpe_F,
                           MaxDD_F=pick.MaxDD_F, Sharpe_H1=pick.Sharpe_H1,
                           Sharpe_H2=pick.Sharpe_H2, pass4a=pick.pass4a, pass4b=pick.pass4b,
                           beats_SPY_OOS=bool(pick.Sharpe_OOS > spy_row["Sharpe_OOS"]),
                           beats_v2_OOS=bool(pick.Sharpe_OOS > v2_row["Sharpe_OOS"]),
                           spy_Sharpe_OOS=spy_row["Sharpe_OOS"], v2_Sharpe_OOS=v2_row["Sharpe_OOS"],
                           dSharpe_OOS_vs_SPY=pick.Sharpe_OOS - spy_row["Sharpe_OOS"],
                           n_blind_keys=len(blindk), blind_keys=";".join(sorted(blindk)),
                           blind_best_arm=b_arm, blind_best_Sharpe_IS=b_best,
                           blind_best_Sharpe_OOS=b_oos,
                           blind_IS_margin=(pick.Sharpe_IS - b_best) if len(badm) else np.nan))
            say(f"    gate {gate:4s} / {rule:11s}: admits {nkeys:2d}/20 keys ({len(adm):3d} arms) "
                f"-> pick {pick.key}/{pick['dir']}/m={pick.m:.2f}  "
                f"[{'CAUSAL' if honest else 'TERMINAL-DATED'}]")
            say(f"                            IS Sharpe {pick.Sharpe_IS:6.3f} | OOS "
                f"{pick.CAGR_OOS:7.2%} / {pick.Sharpe_OOS:6.3f} / {pick.MaxDD_OOS:7.2%}  "
                f"vs SPY {spy_row['CAGR_OOS']:.2%}/{spy_row['Sharpe_OOS']:.3f}/"
                f"{spy_row['MaxDD_OOS']:.2%}  vs v2 {v2_row['CAGR_OOS']:.2%}/"
                f"{v2_row['Sharpe_OOS']:.3f}/{v2_row['MaxDD_OOS']:.2%}")
            say(f"                            full {pick.CAGR_F:7.2%} / {pick.Sharpe_F:6.3f} / "
                f"{pick.MaxDD_F:7.2%}  halves {pick.Sharpe_H1:.3f}/{pick.Sharpe_H2:.3f}  "
                f"4a {bool(pick.pass4a)}  4b {bool(pick.pass4b)}")
            say(f"                            BLIND SPOT: {len(blindk)} admitted key(s) are "
                f"terminal-dated and unseen [{';'.join(sorted(blindk)) or '-'}]; best of them "
                f"{b_arm} IS {b_best:.3f} (OOS {b_oos:.3f}), "
                f"margin under the pick {pick.Sharpe_IS - b_best:+.3f}"
                if len(badm) else
                "                            BLIND SPOT: none -- the gate admits no "
                "terminal-dated key.")
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    # P5 is scored on BOTH gate forms and reported per form; the headline reading is idea 623's
    # recommended T1&T2 gate.
    p5 = {}
    for gate in ("T2", "BOTH"):
        sub = W[W.gate == gate].set_index("rule")
        try:
            p5[gate] = bool((not sub.loc["NONE", "pick_is_causal"])
                            and sub.loc["NONE", "beats_SPY_OOS"]
                            and sub.loc["ASOF_TRUE", "pick_is_causal"]
                            and not sub.loc["ASOF_TRUE", "beats_SPY_OOS"])
        except Exception:
            p5[gate] = False
    preds["P5"] = p5["BOTH"]
    say("")
    say(f"  P5 by gate form: T2-only {'HIT' if p5['T2'] else 'MISS'}, "
        f"T1&T2 (recommended) {'HIT' if p5['BOTH'] else 'MISS'}.")
    for gate in ("T2", "BOTH"):
        sub = W[W.gate == gate].set_index("rule")
        moved = sub.loc["NONE", "pick_key"] != sub.loc["ASOF_TRUE", "pick_key"]
        say(f"    gate {gate:4s}: the as-of column moves the pick "
            f"{sub.loc['NONE', 'pick_key']}/{sub.loc['NONE', 'pick_dir']} -> "
            f"{sub.loc['ASOF_TRUE', 'pick_key']}/{sub.loc['ASOF_TRUE', 'pick_dir']}  "
            f"({'MOVES' if moved else 'NO MOVE'});  dSharpe_OOS "
            f"{sub.loc['ASOF_TRUE', 'Sharpe_OOS'] - sub.loc['NONE', 'Sharpe_OOS']:+.4f};  "
            f"admitted keys {int(sub.loc['NONE', 'n_keys_admitted'])} -> "
            f"{int(sub.loc['ASOF_TRUE', 'n_keys_admitted'])}")

    # ============================================================ PART D -- predictions + wording
    say("")
    say("=" * 112)
    say("PART D  PRE-REGISTERED PREDICTIONS, scored")
    say("=" * 112)
    text = {
        "P1": "gates G1-G5 pass at their stated tolerances",
        "P2": "at least one file read by a rule-8 script has NO recoverable dating (both readings)",
        "P3": "T1's readings are bit-identical across all three dating rules",
        "P4": "T2(NONE) == T2(ASOF_EARLY) on every key while the ground truths differ",
        "P5": "NONE picks a terminal-dated key that beats SPY OOS; ASOF_TRUE picks a causal one "
              "that does not (headline reading = the recommended T1&T2 gate)",
        "P6": "4a 0/360 and 4b 0/360",
    }
    for k in ("P1", "P2", "P3", "P4", "P5", "P6"):
        say(f"  {k}  {'HIT ' if preds.get(k) else 'MISS'}  {text[k]}")
    say("")
    say("  PROPOSED PROTOCOL WORDING (report-only; PROTOCOL.md is NOT edited by this run):")
    say("    10. Every non-price input a script reads must publish an AS-OF DATE -- a column, or a")
    say("        stated constant in the script beside the read. An input with no as-of date is")
    say("        UNDATED and any key built on it is treated as TERMINAL-DATED until dated: both")
    say("        the T1 and the T2 certificates are structurally blind to it, so the certificate")
    say("        result must not be quoted for that key.")
    say(f"  RUNTIME {time.time() - t_start:.1f}s")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_console) + "\n")
    return dict(cen=cen, ce=ce, A=A, W=W, preds=preds, spy=spy_row, v2=v2_row)


if __name__ == "__main__":
    main()
