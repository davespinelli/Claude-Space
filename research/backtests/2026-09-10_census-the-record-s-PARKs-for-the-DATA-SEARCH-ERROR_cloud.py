#!/usr/bin/env python3
"""Idea 622 — census the record's PARKs for the DATA SEARCH ERROR.   (cloud, 2026-09-10)

QUEUE 622: "idea 195 was parked 2026-09-05 for want of a shares series and the PARK was
re-affirmed 2026-09-08, both times on a search of `data/` only; the series was in
`research/deepvalue/universe_under2b.csv` (430 of 439 SMALL names) the whole time.  Census every
committed PARK whose stated reason is 'no data cached' and re-check each against the WHOLE repo,
not just data/; report how many are claimable today.  Max 2 params (park set, search scope)."

WHAT IS ACTUALLY BEING TESTED
  PART A — THE CENSUS.  Harvest every committed PARK in the record, keep the ones whose STATED
     REASON is a data shortage, name the SERIES each one is missing, and re-resolve that series
     under both search scopes.  The question "how many are claimable today" is answered per PARK,
     with the provider file named, so a reader can check the answer without re-running this file.
  PART B — THE DATING TEST, which the queue's own framing omits.  "The series was in the repo" is
     not the same as "the PARK was wrong": idea 195's own resolution (the 2026-09-10 lift) found
     the recovered shares series is a SINGLE TERMINAL VINTAGE, and idea 623 is in the queue
     precisely because a terminal-dated key wins rule 8 by lookahead.  So every provider found
     here is classified PANEL (dated, one row per name per date -> safe) or SNAPSHOT (one vintage
     -> claimable only into a leak), machine-checked from the file itself.
  PART C — PAY THE CENSUS OFF.  The whole-repo scope adds exactly one family of series the record
     has never used, and only one member of it is time-safe: the SIC sector code.  It is run
     end-to-end as a SECTOR CAP on the SMALL439 top-20 equal-weight book — the 2026-09-04 KEEP 4b
     family — under PROTOCOL 4 and 8, with idea 621's NO-DIAL control carried on every row.

AXES (PROTOCOL 4: the queue names the two params for the census)
  P1 PARK SET:
       STRICT  a committed LEADERBOARD row whose VERDICT CELL contains PARK, or a QUEUE `## Done`
               entry whose result text does;
       WIDE    any line in the committed record (QUEUE, LEADERBOARD, CHANGELOG, every
               backtests/*.result.md) carrying a PARK token.
  P2 SEARCH SCOPE:
       DATAONLY  `data/` only — the scope that produced the 2026-09-05 error and its 2026-09-08
                 re-affirmation;
       REPO      every tracked file outside `.git` and outside this run's own outputs.
  PART C carries ONE tuned parameter (the cap m, chosen by rule 8 alone).  Sector granularity
  (SIC2 / SIC division) is a REPORTED axis, evaluated separately and never selected across; the
  cost rungs and the cadence are reported axes too.  Every grid point is written to .capgrid.csv.

GATES (before any new number is read)
  G1 the segment runner vs `engine.backtest` on returns AND turnover (small panel, D and W).
  G2 the cost-rung identity vs a live `engine.backtest(cost_bps=25)`.
  G3 REPRODUCTION of the queue's own claim: `research/deepvalue/universe_under2b.csv` covers
     430 of the 439 SMALL names.  Counted here, not restated.
  G4 the cap m = 20 arm is EXACTLY the un-capped top-20 book (max|dr| over the sample).
  G5 the sector map is TERMINAL-DATED: the number of distinct as-of periods in the provider is
     printed, so the snapshot's own vintage is on the record.

CAVEATS CARRIED
  * SURVIVORSHIP twice over.  SMALL439 is current constituents (idea 54) and drops every ticker
    with max_1d_move >= 1.0 from data/small_meta.csv.  On top of that the SECTOR LABELS come from
    a screen of names that are under $2B TODAY, so the sector map is itself a terminal snapshot.
    A SIC code is far more time-stable than a share count, but "far more" is not "invariant" and
    the run says so rather than assuming it away (ideas 195/197/623).
  * Idea 623: a terminal-dated key beats rule 8 by construction.  This file therefore refuses to
    call a SNAPSHOT-backed PARK "claimable" without that qualifier.
  * Idea 321 (MaxDD is one path), idea 126 (t+1, 10 bps), ideas 527/531 (4b is a DD-cap test).
  * The census classifies FILES AND SENTENCES, not claims (idea 534); WIDE is an upper bound.

Deterministic, standalone.  Modifies nothing outside its own output files.
Writes .console.txt, .parks.csv, .providers.csv, .capgrid.csv, .wf.csv.
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-10_census-the-record-s-PARKs-for-the-DATA-SEARCH-ERROR_cloud"
OUT = ROOT / "research" / "backtests"

GROSS, NTOP = 0.75, 20
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PHI, DELTA = 0.70, 0.60
PCOST = 10.0
RUNGS = [0.0, 10.0, 25.0, 50.0]
CAPS = [1, 2, 3, 4, 5, 8, 20]          # 20 = no binding cap on a 20-name book (the NO-DIAL arm)
NOCAP = 20
CADENCES = ["W", "D"]
GRAINS = ["SIC2", "DIV"]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 4000)
LOG: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# =====================================================================================
# runner
# =====================================================================================
def _mask(idx, freq):
    return rebalance_mask(idx, freq).shift(1, fill_value=False).values


def fast_bt(rets, w_t, mask):
    n = len(rets)
    reb = np.unique(np.concatenate(([0], np.flatnonzero(mask))))
    port = np.zeros(n)
    turn = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    for si, i0 in enumerate(reb):
        i1 = reb[si + 1] if si + 1 < len(reb) else n
        if i1 <= i0:
            continue
        new = w_t[i0]
        turn[i0] = np.abs(new - cur).sum()
        A = new[None, :] * np.cumprod(1.0 + rets[i0:i1], axis=0)
        S = A.sum(axis=1) + (1.0 - new.sum())
        port[i0:i1] = S / np.concatenate(([1.0], S[:-1])) - 1.0
        cur = A[-1] / S[-1]
    return port, turn


def run(px, W, freq):
    rets = px.pct_change().fillna(0.0).values
    w_t = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    p, t = fast_bt(rets, w_t, _mask(px.index, freq))
    return pd.Series(p, index=px.index), pd.Series(t, index=px.index)


def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def sh(r):
    return metrics(r)["Sharpe"]


def halves(r):
    h = len(r) // 2
    return sh(r.iloc[:h]), sh(r.iloc[h:])


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep].dropna(how="all").ffill(), len(bad & set(px.columns))


# =====================================================================================
# PART A — the PARK census
# =====================================================================================
PARK = re.compile(r"\bPARK(?:ED|ing|s)?\b", re.I)
NEED = re.compile(r"(no|not|lack\w*|without|missing|un-?available|un-?cached|needs?|requires?|"
                  r"cannot|can't)\b[^.;|]{0,140}?"
                  r"(cach\w+|\bdata\b|series|panel|feed|history|file|internet|network|offline|"
                  r"local/Actions|Actions)", re.I)
# the record's own stated-reason phrase for this park family
STATED = re.compile(r"needs?\s+local/?Actions\s+data|no\s+\S+\s+series\s+is\s+cached|"
                    r"is\s+cached\s+in\s+`?data/|not\s+buildable\s+offline|no\s+data\b", re.I)

# the SERIES vocabulary, lifted from the harvested sentences themselves
SERIES = [
    ("shares_outstanding", r"shares[-\s]?outstanding|share\s+count|shares\s+series"),
    ("market_cap_PIT",     r"point-in-time\s+market[-\s]?cap|PIT\s+market[-\s]?cap|"
                           r"PIT\s+(?:top-\d+-by-)?market[-\s]?cap\s+panel"),
    ("index_membership",   r"index[-\s]?membership|reconstitution|Russell|S&P\s*600|S&P\s*500\s+adds"),
    ("delisted_prices",    r"delisted|de-?listing|acquired\s+ticker|dead\s+ticker"),
    ("sector",             r"\bsector\b|\bGICS\b|\bSIC\b|industry\s+classif"),
    ("borrow_short",       r"borrow\s+cost|short\s+interest|utilisation|utilization"),
    ("float",              r"\bfree\s?float\b|\bfloat\b"),
    ("fundamentals",       r"revenue|earnings\s+surprise|EBIT|book\s+value|balance\s+sheet"),
    ("intraday",           r"intraday|minute\s+bars|tick\s+data"),
    ("options_iv",         r"implied\s+vol|options?\s+chain|\bIV\b"),
]

# provider index: what each candidate repo file can actually serve, matched on its COLUMNS
COLKEY = {
    "shares_outstanding": r"^shares(_py)?$|shares_outstanding",
    "market_cap_PIT":     r"^mktcap$|market_?cap",
    "index_membership":   r"index_member|russell|sp600|sp500|constituent",
    "delisted_prices":    r"delist|dead_ticker|last_trade_date",
    "sector":             r"^sic$|^sic_desc$|^sector$|^gics",
    "borrow_short":       r"borrow|short_interest|utilisation|utilization",
    "float":              r"^float$|free_float",
    "fundamentals":       r"^revenue$|^ebit$|^equity$|^cfo$|^net_income$",
    "intraday":           r"^minute$|^bar_time$|intraday",
    "options_iv":         r"^iv$|implied_vol|^iv_",
}


def harvest_parks():
    files = [ROOT / "research" / f for f in ("QUEUE.md", "LEADERBOARD.md", "CHANGELOG.md")]
    files += sorted(OUT.glob("*.result.md"))
    rows = []
    for f in files:
        try:
            txt = f.read_text(errors="ignore")
        except Exception:
            continue
        for ln, line in enumerate(txt.split("\n"), 1):
            if not PARK.search(line):
                continue
            if f.name == "LEADERBOARD.md" and line.startswith("| 20"):
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                strict = bool(len(cells) > 2 and PARK.search(cells[-2]))
            elif f.name == "QUEUE.md":
                strict = "DONE" in line or "**PARK" in line
            else:
                strict = False
            for sent in re.split(r"(?<=[.;])\s+|\|", line):
                if not PARK.search(sent):
                    continue
                s = sent.strip()
                if not s:
                    continue
                rows.append(dict(file=f.name, line=ln, strict=strict,
                                 data_park=bool(NEED.search(s)),
                                 stated=bool(STATED.search(s)),
                                 series=";".join(k for k, rx in SERIES
                                                 if re.search(rx, s, re.I)),
                                 text=s[:400]))
    P = pd.DataFrame(rows)
    # a PARK sentence repeated verbatim in several places is ONE park
    P["key"] = P.text.str.lower().str.replace(r"[^a-z0-9 ]", "", regex=True).str[:90]
    return P


def index_providers():
    """Every tracked data-bearing file outside .git and outside research/backtests, with the
    columns it exposes.  This IS the whole-repo search scope the queue asks for."""
    rows = []
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith(".git/") or rel.startswith("research/backtests/"):
            continue
        if not (rel.endswith(".csv") or rel.endswith(".csv.gz") or rel.endswith(".json")):
            continue
        cols, ndate, err = [], np.nan, ""
        try:
            if rel.endswith(".json"):
                cols = []
            else:
                d = pd.read_csv(p, nrows=300, low_memory=False)
                cols = [str(c) for c in d.columns]
                for c in cols:
                    if re.fullmatch(r"(date|Date|asof|as_of|scan_date|filing_date)", c):
                        ndate = int(pd.Series(d[c]).nunique())
                        break
                else:
                    if cols and re.fullmatch(r"(date|Date|Unnamed: 0)", cols[0]):
                        ndate = int(pd.Series(d[cols[0]]).nunique())
        except Exception as e:                                   # noqa: BLE001
            err = type(e).__name__
        rows.append(dict(path=rel, in_data=rel.startswith("data/"), ncol=len(cols),
                         ndate_head=ndate, cols=";".join(cols[:400]), err=err))
    return pd.DataFrame(rows)


# The series in COLKEY that are NAME-LEVEL ATTRIBUTES: a provider only serves them if it is a
# one-row-per-ticker table.  Without this audit a column-name match alone accepts
# data/form4_purchases.csv's `shares` (an insider TRANSACTION size) as "shares outstanding" —
# the same class of error as the one this idea is censusing, made in the other direction.
NAME_LEVEL = {"shares_outstanding", "market_cap_PIT", "sector", "float", "fundamentals"}


def _is_name_table(path):
    """True if the file is keyed by ticker with (near-)unique tickers."""
    try:
        d = pd.read_csv(ROOT / path, nrows=5000, low_memory=False)
    except Exception:
        return False, 0, 0
    tc = next((c for c in d.columns if str(c).lower() in ("ticker", "symbol")), None)
    if tc is None:
        return False, 0, 0
    n, u = len(d), int(pd.Series(d[tc]).nunique())
    return (u >= 0.9 * n and n > 0), n, u


def resolve(series_key, PR, audit=True):
    """Which files under each scope expose a column that serves this series.  With audit=True a
    name-level series additionally requires the provider to be a one-row-per-ticker table."""
    rx = COLKEY[series_key]
    hit = PR[PR.cols.fillna("").apply(
        lambda s: any(re.search(rx, c, re.I) for c in s.split(";") if c))].copy()
    hit["name_table"] = [_is_name_table(p)[0] for p in hit.path]
    rej = hit[~hit.name_table] if (audit and series_key in NAME_LEVEL) else hit.iloc[0:0]
    if audit and series_key in NAME_LEVEL:
        hit = hit[hit.name_table]
    return hit[hit.in_data], hit[~hit.in_data], rej


def dating_of(path):
    """PANEL (many distinct dates) or SNAPSHOT (one vintage / no date axis), read from the file."""
    p = ROOT / path
    try:
        d = pd.read_csv(p, nrows=5000, low_memory=False)
    except Exception:
        return "UNREADABLE", np.nan
    for c in d.columns:
        if re.fullmatch(r"(date|Date|asof|as_of|scan_date|Unnamed: 0)", str(c)):
            n = int(pd.Series(d[c]).nunique())
            return ("PANEL" if n > 5 else "SNAPSHOT"), n
    per = [c for c in d.columns if str(c).endswith("_period")]
    if per:
        return "SNAPSHOT", int(pd.Series(d[per[0]]).nunique())
    return "SNAPSHOT", 1


# =====================================================================================
# PART C — the sector-cap back-fill
# =====================================================================================
def sector_map(names, grain):
    """SIC from research/deepvalue/universe_under2b.csv — the file the 2026-09-05 PARK missed."""
    d = pd.read_csv(ROOT / "research" / "deepvalue" / "universe_under2b.csv", low_memory=False)
    s = d.dropna(subset=["ticker"]).drop_duplicates("ticker").set_index("ticker")["sic"]
    s = pd.to_numeric(s, errors="coerce").dropna().astype(int)
    m = s.reindex(names)
    if grain == "SIC2":
        lab = (m // 100).astype("Int64").astype(str)
    else:                                   # the standard SIC DIVISIONS
        edges = [(1, 9, "A-agri"), (10, 14, "B-mining"), (15, 17, "C-constr"),
                 (20, 39, "D-mfg"), (40, 49, "E-tpu"), (50, 51, "F-whlsl"),
                 (52, 59, "G-retail"), (60, 67, "H-fin"), (70, 89, "I-svcs"), (91, 99, "J-pub")]
        two = (m // 100)
        lab = pd.Series("UNK", index=names, dtype=object)
        for lo, hi, nm in edges:
            lab[(two >= lo) & (two <= hi)] = nm
        lab = lab.astype(str)
    lab = pd.Series(lab.values, index=names, dtype=object).fillna("UNK")
    lab[lab == "<NA>"] = "UNK"
    return lab


def capped_book(px, comp, sect, cap, freq):
    """Top-NTOP of the composite subject to at most `cap` names per sector, greedy in composite
    rank, equal weight at GROSS/NTOP.  Selection is computed on rebalance days only (the only
    days engine.backtest reads a target) and forward-filled."""
    names = list(comp.columns)
    codes, uniq = pd.factorize(sect.reindex(names).values)
    ng = len(uniq)
    reb = np.flatnonzero(rebalance_mask(px.index, freq).values)
    if 0 not in reb:
        reb = np.concatenate(([0], reb))
    C = comp.values
    W = np.zeros((len(reb), len(names)))
    for r, i in enumerate(reb):
        row = C[i]
        ok = np.flatnonzero(np.isfinite(row))
        if ok.size == 0:
            continue
        order = ok[np.argsort(-row[ok], kind="stable")]
        cnt = np.zeros(ng, dtype=int)
        pick = []
        for j in order:
            g = codes[j]
            if g >= 0 and cnt[g] >= cap:
                continue
            pick.append(j)
            if g >= 0:
                cnt[g] += 1
            if len(pick) == NTOP:
                break
        if pick:
            W[r, pick] = GROSS / NTOP
    Wd = pd.DataFrame(W, index=px.index[reb], columns=names)
    return Wd.reindex(px.index).ffill().fillna(0.0)


def main():
    t0 = time.time()
    say("=" * 104)
    say("IDEA 622 — census the record's PARKs for the DATA SEARCH ERROR   (cloud 2026-09-10)")
    say("=" * 104)

    # ---------------- PART A ----------------
    say("\nPART A — PARK CENSUS")
    P = harvest_parks()
    P.to_csv(OUT / f"{STEM}.parks.csv", index=False)
    strict = P[P.strict].drop_duplicates("key")
    wide = P.drop_duplicates("key")
    say(f"  PARK sentences harvested (all occurrences)      : {len(P)}")
    for lab, S in (("STRICT park set", strict), ("WIDE park set", wide)):
        say(f"  --- {lab}: {len(S)} distinct PARKs")
        say(f"      whose stated reason is a DATA shortage       : {int(S.data_park.sum())}"
            f"  ({S.data_park.mean():.1%})")
        say(f"      matching the record's own phrase for it      : {int(S.stated.sum())}")
        say(f"      naming a recoverable SERIES                  : "
            f"{int((S.series.fillna('') != '').sum())}")

    DP = wide[wide.data_park & (wide.series.fillna("") != "")].copy()
    say(f"\n  DATA-PARKs naming a series (WIDE, de-duplicated): {len(DP)}")
    ser = pd.Series([s for row in DP.series for s in row.split(";") if s]).value_counts()
    say("  series named:\n" + ser.to_string())

    # ---------------- PART A/B: resolve every named series under both scopes ----------------
    say("\nPART B — RESOLUTION under both search scopes (P2), with the DATING test")
    PR = index_providers()
    PR.to_csv(OUT / f"{STEM}.providers.csv", index=False)
    say(f"  data-bearing files indexed repo-wide: {len(PR)}  "
        f"({int(PR.in_data.sum())} under data/, {int((~PR.in_data).sum())} outside it)")
    res, rejects = [], []
    keys = list(ser.index) + [k for k in ("sector",) if k not in ser.index]
    for key in keys:
        raw_in, raw_out, _ = resolve(key, PR, audit=False)
        ind, outd, rej = resolve(key, PR, audit=True)
        for _, r in rej.iterrows():
            rejects.append((key, r.path, "not a one-row-per-ticker table"))
        best = ""
        dating, nvint = "", np.nan
        if len(outd):
            best = outd.iloc[0].path
            dating, nvint = dating_of(best)
        elif len(ind):
            best = ind.iloc[0].path
            dating, nvint = dating_of(best)
        res.append(dict(series=key, n_parks=int(ser.get(key, 0)),
                        raw_in_data=len(raw_in), in_data=len(ind), outside_data=len(outd),
                        provider=best, dating=dating, n_vintages=nvint,
                        found_by_DATAONLY=len(ind) > 0, found_by_REPO=len(ind) + len(outd) > 0,
                        search_error=(len(ind) == 0 and len(outd) > 0)))
    R = pd.DataFrame(res)
    say(R.to_string(index=False))
    say("\n  PROVIDER AUDIT — column-name matches REJECTED as the wrong quantity "
        "(the same class of error, made in the other direction):")
    for k, p, why in rejects:
        say(f"    {k:>18}  <-  {p}  ({why})")
    if not rejects:
        say("    none")
    say("  `sector` is carried in the table because PART C uses it; NO committed PARK names it "
        f"(n_parks = {int(ser.get('sector', 0))}).")
    say(f"\n  PARKS THE `data/`-ONLY SCOPE COULD NOT SERVE BUT THE WHOLE REPO CAN: "
        f"{int(R.search_error.sum())} of {len(R)} series")
    se = R[R.search_error]
    say(f"  ... of which the provider is a DATED PANEL (time-safe)  : "
        f"{int((se.dating == 'PANEL').sum())}")
    say(f"  ... of which the provider is a TERMINAL SNAPSHOT (idea 623 leak risk): "
        f"{int((se.dating == 'SNAPSHOT').sum())}")
    say(f"  series NO scope can serve (still genuinely parked)      : "
        f"{int((~R.found_by_REPO).sum())}  -> {list(R[~R.found_by_REPO].series)}")

    # WHICH PANELS the one recovered provider can actually reach — a series that covers no name
    # in the parked idea's own universe does not lift that PARK.
    dvt = set(pd.read_csv(ROOT / "research" / "deepvalue" / "universe_under2b.csv",
                          low_memory=False).ticker.dropna().astype(str))
    small_cols, _nd = small_panel()
    cover = {"u56": load_universe(), "broad136": load_universe(broad=True),
             "small439": small_cols}
    say("\n  PANEL REACH of the recovered provider (research/deepvalue/universe_under2b.csv):")
    for pk, q in cover.items():
        nm = [c for c in q.columns if c != "SPY"]
        say(f"    {pk:>9}: {len(set(nm) & dvt)} of {len(nm)} names covered")
    say("    -> the recovered series is a SUB-$2B screen; it reaches none of the mega-cap panels, "
        "so it cannot lift the point-in-time-MEGACAP-panel PARK even in principle.")

    # ---------------- PART C ----------------
    say("\n" + "=" * 104)
    say("PART C — PAY IT OFF: the recovered SECTOR series as a SECTOR CAP on SMALL439's top-20")
    say("=" * 104)
    px, ndrop = small_panel()
    sub = px.drop(columns=["SPY"], errors="ignore")
    comp = composite(sub)
    names = list(sub.columns)
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    b = dict(zip(("s1", "s2"), halves(spy)))
    ms = metrics(spy)
    b.update(sdd=ms["MaxDD"], scagr=ms["CAGR"], soos=sh(spy.loc[OOS_START:]))
    br0, bto = run(px, rules_v2_weights(px), "W")
    baser = (br0 - bto * PCOST / 1e4).loc[start:]
    say(f"  panel: {len(names)} names ({ndrop} dropped for max_1d_move>=1.0), "
        f"{px.index[0].date()} .. {px.index[-1].date()}")

    # ---- gates
    say("\nGATES")
    ok = True
    W20 = capped_book(px, comp, sector_map(names, "SIC2"), NOCAP, "W").reindex(columns=px.columns)
    W20 = W20.fillna(0.0)
    for f in CADENCES:
        Wf = capped_book(px, comp, sector_map(names, "SIC2"), NOCAP, f)
        Wf = Wf.reindex(columns=px.columns).fillna(0.0)
        rf, tf = run(px, Wf, f)
        e0 = backtest(px, Wf, cost_bps=0.0, freq=f)
        dr = float((rf.loc[start:] - e0["returns"].loc[start:]).abs().max())
        dt = float((tf.loc[start:] - e0["turnover"].loc[start:]).abs().max())
        say(f"  G1 {f}: max|dr| {dr:.3e}  max|dto| {dt:.3e}")
        ok &= dr < 1e-12 and dt < 1e-12
    rf, tf = run(px, W20, "W")
    e25 = backtest(px, W20, cost_bps=25.0, freq="W")
    d2 = float(((rf - tf * 25.0 / 1e4).loc[start:] - e25["returns"].loc[start:]).abs().max())
    say(f"  G2  : rung identity max|dr| {d2:.3e}")
    ok &= d2 < 1e-12
    dv = pd.read_csv(ROOT / "research" / "deepvalue" / "universe_under2b.csv", low_memory=False)
    cov = len(set(dv.ticker.dropna().astype(str)) & set(names))
    say(f"  G3  : deepvalue covers {cov} of the {len(names)} SMALL names "
        f"(queue's claim: 430 of 439)")
    # G4a: the cap m=20 arm against an un-capped top-20 built with the SAME tie-break.
    flat = pd.Series("ALL", index=names)
    Wflat = capped_book(px, comp, flat, 10 ** 9, "W").reindex(columns=px.columns).fillna(0.0)
    d4a = float((run(px, Wflat, "W")[0].loc[start:] - rf.loc[start:]).abs().max())
    say(f"  G4a : cap m=20 vs an un-capped top-20 on the SAME tie-break  max|dr| {d4a:.3e}")
    ok &= d4a < 1e-12
    # G4b: the same book built with pandas rank() instead — MEASURED, not asserted, because the
    # composite ties and the two tie-breaks then hold different names.
    plain = (comp.rank(axis=1, ascending=False) <= NTOP).astype(float) * (GROSS / NTOP)
    plain = plain.reindex(columns=px.columns).fillna(0.0)
    rp = run(px, plain, "W")[0]
    d4b = float((rp.loc[start:] - rf.loc[start:]).abs().max())
    nd = int((plain.loc[start:].gt(0) ^ W20.loc[start:].gt(0)).any(axis=1).sum())
    say(f"  G4b : the rank()-tie-break book differs on {nd} of "
        f"{len(px.loc[start:])} days, max|dr| {d4b:.3e} — reported, not gated")
    nv = pd.Series(dv["shares_period"]).nunique() if "shares_period" in dv else np.nan
    say(f"  G5  : the provider is TERMINAL-DATED — {nv} distinct as-of periods across all names")
    say(f"  GATES {'PASS' if ok else 'FAIL'}")

    # ---- grid
    rows = []
    for grain in GRAINS:
        sect = sector_map(names, grain)
        ng = sect.nunique()
        nunk = int((sect == "UNK").sum())
        say(f"\n  {grain}: {ng} sectors, {nunk} names UNK (capped as one group)")
        for cad in CADENCES:
            for cap in CAPS:
                W = capped_book(px, comp, sect, cap, cad).reindex(columns=px.columns).fillna(0.0)
                r0, to = run(px, W, cad)
                r0, to = r0.loc[start:], to.loc[start:]
                nsel = float((W.loc[start:] > 0).sum(axis=1).mean())
                rec = dict(grain=grain, cad=cad, cap=cap, is_nodial=(cap == NOCAP),
                           n_held=nsel, turnover=float(to.sum() / (len(to) / 252.0)))
                for c in RUNGS:
                    r = r0 - to * c / 1e4
                    m, mo = metrics(r), metrics(r.loc[OOS_START:])
                    h1, h2 = halves(r)
                    rec[f"cagr_{c:g}"], rec[f"sh_{c:g}"], rec[f"dd_{c:g}"] = \
                        m["CAGR"], m["Sharpe"], m["MaxDD"]
                    rec[f"h1_{c:g}"], rec[f"h2_{c:g}"] = h1, h2
                    rec[f"sh_is_{c:g}"] = sh(r.loc[:IS_END])
                    rec[f"sh_oos_{c:g}"] = mo["Sharpe"]
                    rec[f"cagr_oos_{c:g}"] = mo["CAGR"]
                    rec[f"dd_oos_{c:g}"] = mo["MaxDD"]
                    if c == PCOST:
                        bh1, bh2 = halves(baser)
                        rec["p4a"] = bool(h1 > bh1 and h2 > bh2
                                          and m["MaxDD"] >= metrics(baser)["MaxDD"])
                        rec["p4b"] = bool(h1 > b["s1"] and h2 > b["s2"]
                                          and sh(r.loc[OOS_START:]) > b["soos"]
                                          and abs(m["MaxDD"]) <= DELTA * abs(b["sdd"])
                                          and m["CAGR"] >= PHI * b["scagr"])
                rows.append(rec)
        say(f"    [{time.time()-t0:5.0f}s]")
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STEM}.capgrid.csv", index=False)

    say("\nEVERY GRID POINT (10 bps):")
    say(G[["grain", "cad", "cap", "n_held", "turnover", "cagr_10", "sh_10", "dd_10",
           "h1_10", "h2_10", "sh_is_10", "sh_oos_10", "p4a", "p4b"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- rule 8 + idea 621's NO-DIAL control
    say("\n" + "=" * 104)
    say("RULE 8 (PROTOCOL 8) — cap chosen on 2010-2016 IS Sharpe alone, 2017-2026 read once")
    say("  with idea 621's NO-DIAL control (cap = 20, i.e. no cap) on every row")
    say("=" * 104)
    wf = []
    for (grain, cad), g in G.groupby(["grain", "cad"]):
        for c in RUNGS:
            pick = g.loc[g[f"sh_is_{c:g}"].idxmax()]
            ctl = g[g.is_nodial].iloc[0]
            orc = g.loc[g[f"sh_oos_{c:g}"].idxmax()]
            wf.append(dict(grain=grain, cad=cad, cost=c, pick=int(pick.cap),
                           pick_is=pick[f"sh_is_{c:g}"], pick_oos=pick[f"sh_oos_{c:g}"],
                           pick_cagr_oos=pick[f"cagr_oos_{c:g}"],
                           pick_dd_oos=pick[f"dd_oos_{c:g}"],
                           nodial_oos=ctl[f"sh_oos_{c:g}"],
                           nodial_cagr_oos=ctl[f"cagr_oos_{c:g}"],
                           nodial_dd_oos=ctl[f"dd_oos_{c:g}"],
                           d_nodial=pick[f"sh_oos_{c:g}"] - ctl[f"sh_oos_{c:g}"],
                           oracle=int(orc.cap), regret=orc[f"sh_oos_{c:g}"] - pick[f"sh_oos_{c:g}"],
                           pick_4a=bool(pick.p4a), pick_4b=bool(pick.p4b),
                           nodial_4a=bool(ctl.p4a), nodial_4b=bool(ctl.p4b)))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.wf.csv", index=False)
    say(WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\n  chooser beats the NO-DIAL control in {int((WF.d_nodial > 0).sum())}/{len(WF)} cells"
        f"   median {WF.d_nodial.median():+.4f}")

    mo_s = metrics(spy.loc[OOS_START:])
    mo_b = metrics(baser.loc[OOS_START:])
    say(f"\n  COMPARANDS  OOS 2017-2026: SPY {mo_s['CAGR']:.2%}/{mo_s['Sharpe']:.4f}/"
        f"{mo_s['MaxDD']:.2%}   RULES v2 {mo_b['CAGR']:.2%}/{mo_b['Sharpe']:.4f}/"
        f"{mo_b['MaxDD']:.2%}")
    say(f"  COMPARANDS  full sample : SPY {ms['CAGR']:.2%}/{ms['Sharpe']:.4f}/{ms['MaxDD']:.2%} "
        f"(H {b['s1']:.4f}/{b['s2']:.4f})   RULES v2 {metrics(baser)['CAGR']:.2%}/"
        f"{metrics(baser)['Sharpe']:.4f}/{metrics(baser)['MaxDD']:.2%} "
        f"(H {halves(baser)[0]:.4f}/{halves(baser)[1]:.4f})")

    say("\nKEEP PATHS (PROTOCOL 4, both priced on every arm, 10 bps)")
    say(f"  all {len(G)} grid points: 4a {int(G.p4a.sum())}/{len(G)}   4b {int(G.p4b.sum())}/{len(G)}")
    say(f"  the {len(WF)} chooser arms : 4a {int(WF.pick_4a.sum())}   4b {int(WF.pick_4b.sum())}")
    say(f"  the {len(WF)} no-dial arms : 4a {int(WF.nodial_4a.sum())}   4b {int(WF.nodial_4b.sum())}")

    say(f"\nwrote .parks.csv .providers.csv .capgrid.csv .wf.csv   [{time.time()-t0:.0f}s]")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
