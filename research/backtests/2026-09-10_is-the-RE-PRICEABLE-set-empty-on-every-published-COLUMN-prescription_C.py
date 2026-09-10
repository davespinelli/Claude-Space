#!/usr/bin/env python3
"""Idea 616 — is the RE-PRICEABLE set empty on every published COLUMN prescription?  (lane C, 2026-09-10)

QUEUE 616: "idea 613 found exactly 1 of 44 strict width-claim files carries both the turnover and
the rung column its own prescription needs, and that file is the one that made the prescription.
Census the record's OTHER 'publish X beside every Y' prescriptions (ideas 239 EWall, 471
matched-gross, 583 gross, 604 placebo, 607 crossing cost) the same way and report each one's
re-priceable share AT THE POINT IT WAS PROPOSED.  Max 2 params (prescription set, validation
strictness)."

WHAT IS ACTUALLY BEING TESTED
  H1 (census)      Every 'publish X beside every Y' prescription in the record was made against a
                   corpus that cannot be re-priced without re-running it: the share of Y-claim
                   files that already carry X is near zero at the moment the prescription is
                   proposed.  FALSIFIABLE: if a prescription's re-priceable share is already
                   high, that prescription is a no-op and 613's finding is special to width.
  H2 (vintage)     The share does not move materially between the proposal date and now, i.e.
                   the record does not back-fill the column after the prescription is published.
                   FALSIFIABLE: a large PRE -> NOW rise on any prescription refutes it.
  H3 (self-site)   613's "the only re-priceable file is the one that made the prescription"
                   generalises: the X column, where it exists at all, is concentrated in the
                   prescribing run's own artefacts and their descendants.
  H4 (live cost)   The columns are not bookkeeping.  On a FRESH grid that carries all five
                   columns by construction, re-reading a clause-vs-control verdict against the
                   MATCHED-GROSS twin (583/471), the UN-RANKED EWall control (239) and the BLOCK
                   PLACEBO (604) flips a materially different set of verdicts, and the crossing
                   cost (607) sits at or below the rung the claim is published at.
                   FALSIFIABLE: if the four re-readings agree with the full-gross reading, the
                   missing column costs nothing and all five prescriptions are cosmetic.

AXES, AND WHAT IS EVER SELECTED ON (PROTOCOL 4, "no more than 2 tuned parameters")
  The queue names the two tuned parameters and both are swept in full, every point reported:
    P1 prescription set : {239 EWall, 471 matched-gross, 583 gross, 604 placebo, 607 crossing
                          cost} — all five, plus 613 WIDTH re-run as the control prescription
                          whose answer is already published (it is the gate, not a new claim).
    P2 strictness       : LOOSE  (header keyword only, the census a naive regex would make)
                          STRICT (keyword AND the column's VALUES in the right physical range,
                          and the claim's own witness column present and numeric).
  VINTAGE (PRE / AT / NOW) is a REPORTED axis, not a tuned one: all three are always printed.
  The fresh leg's dials are BAND (6 points) and GROSS (3 points), fully enumerated, every point
  reported, and never chosen — except in PROTOCOL rule 8, the only place anything is selected.

GATES (run before any new number is read)
  G1 the vectorised runner vs `engine.backtest` on the evaluated slice, returns AND turnover.
  G2 the rung identity r(c) = r(0) - turnover*c/1e4 vs a live `engine.backtest(cost_bps=25)`.
  G3 VINTAGE: a file's run-date stamp (its filename prefix) must never post-date the commit that
     added it.  The repo's history is shallow (50 commits, 2026-09-09 -> 2026-09-10), so this is
     checkable only on files git can still see; it is reported as a share and the stamp is used
     as the vintage because git cannot see further back.
  G4 the census machinery reproduces idea 613's OWN published census off 613's committed
     `.census.csv`: 44 TIER-A width files, 1 re-priceable.

CAVEATS CARRIED
  * The census reads COMMITTED CSVs only.  A claim made in prose and never written to a CSV is
    invisible to it — that is why LOOSE is reported beside STRICT as an upper bound.
  * A header regex cannot tell a claim from a statistic about a claim (ideas 286/523/613): STRICT
    adds a value check, and every count is reported both ways rather than one being chosen.
  * VINTAGE is the filename date stamp, which is the record's own convention; a file re-written
    later under the same name keeps its original stamp, so PRE counts are, if anything, generous
    to the record.
  * SURVIVORSHIP (idea 54): all three panels are current constituents; SMALL439 additionally
    drops the 44 `max_1d_move >= 1.0` tickers from data/small_meta.csv before anything runs.
  * MaxDD is one number off one path (idea 321) and the 4b DD cap turns on exactly that number.
  * Idea 126: t+1 execution, no lag band.  Idea 38: u56/broad carry the calendar-day index.
  * The placebo is a BLOCK shuffle of the gate in time (block 21d, fixed seed): it preserves the
    gate's on-share and its cross-section and destroys only its timing.

Deterministic, standalone.  Modifies nothing.  Writes .console.txt, .census.csv, .presc.csv,
.grid.csv, .reread.csv, .wf.csv next to itself.
"""
from __future__ import annotations

import csv
import glob
import gzip
import importlib.util
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-10_is-the-RE-PRICEABLE-set-empty-on-every-published-COLUMN-prescription_C"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I613_CENSUS = OUT / ("2026-09-10_publish-DRAG-not-TURNOVER-beside-every-window-width-claim_"
                     "cloud.census.csv")


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")                       # idea 94's harness: composite / vol20
FREQ = H.FREQ
IS_END, OOS_START = H.IS_END, H.OOS_START
PHI, DELTA = 0.70, 0.60                     # 4b CAGR floor / DD cap fractions of SPY

PANELS = ["u56", "broad", "small"]
BOOKS = ["TOP20", "EWALL"]                  # ranked book / the record's un-ranked control (239)
BANDS = [0.00, 0.01, 0.02, 0.04, 0.06, 0.08]        # the clause dial, fully enumerated
GROSSES = [0.50, 0.75, 1.00]                        # the exposure dial, fully enumerated
NTOP = 20
RUNGS = [0.0, 5.0, 10.0, 25.0, 50.0]
BARS5 = ["H1", "H2", "OOS", "DD", "CAGR"]
BLOCK = 21                                  # placebo block length in trading days
SEED = 616

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 4000)
LOG: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# =====================================================================================
# vectorised runner (segment-exact reproduction of engine.backtest at zero cost) — idea 613
# =====================================================================================
def fast_bt(px: pd.DataFrame, W: pd.DataFrame, freq=FREQ):
    rets = px.pct_change().fillna(0.0).values
    w_t = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n = len(px)
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
    idx = px.index
    return pd.Series(port, index=idx), pd.Series(turn, index=idx)


# =====================================================================================
# books, gates, controls
# =====================================================================================
def book_weights(px, book, investable, gross):
    """TOP20 = composite top-20 at gross/20 (the record's ranked book).
       EWALL = equal weight over every priced name at gross/N (the record's un-ranked control)."""
    sub = px[investable]
    if book == "EWALL":
        e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
        W = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    else:
        rank = H.composite(sub).rank(axis=1, ascending=False)
        W = (rank <= NTOP).astype(float) * (gross / NTOP)
    return W.reindex(columns=px.columns).fillna(0.0)


def band_gate(px, band):
    """RULES v2 clause 2 verbatim (baseline.band_state): 200d MA with hysteresis.  band=0.0 is
    the plain MA gate.  Gated-out weight goes to CASH — de-gross, never re-spread."""
    ma = px.rolling(200).mean()
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    raw = raw.mask(px > ma * (1 + band), 1.0).mask(px < ma * (1 - band), 0.0)
    return raw.ffill().fillna(0.0) > 0.5


def block_shuffle(mask: pd.DataFrame, seed=SEED, block=BLOCK):
    """BLOCK placebo (idea 602/604's form): permute contiguous `block`-day slabs of the gate in
    TIME with a fixed seed.  Preserves the gate's on-share and its whole cross-section; destroys
    only WHEN it fires.  Deterministic given (n, seed, block)."""
    n = len(mask)
    starts = list(range(0, n, block))
    rng = np.random.default_rng(seed)
    order = rng.permutation(len(starts))
    rows = []
    for k in order:
        s = starts[k]
        rows.append(np.arange(s, min(s + block, n)))
    idx = np.concatenate(rows)[:n]
    out = mask.values[idx]
    return pd.DataFrame(out, index=mask.index, columns=mask.columns)


def mean_gross(W, start):
    return float(W.loc[start:].sum(axis=1).mean())


# =====================================================================================
# metric helpers
# =====================================================================================
def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_of(spy, which="full"):
    s = spy if which == "full" else spy.loc[:IS_END]
    h = len(s) // 2
    m = metrics(s)
    return dict(s1=metrics(s.iloc[:h])["Sharpe"], s2=metrics(s.iloc[h:])["Sharpe"],
                sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=metrics(spy.loc[OOS_START:])["Sharpe"] if which == "full" else np.nan)


def margins(r, b, which="full"):
    s = r if which == "full" else r.loc[:IS_END]
    h = len(s) // 2
    m = metrics(s)
    d = dict(H1=metrics(s.iloc[:h])["Sharpe"] - b["s1"],
             H2=metrics(s.iloc[h:])["Sharpe"] - b["s2"],
             DD=DELTA * abs(b["sdd"]) - abs(m["MaxDD"]),
             CAGR=m["CAGR"] - PHI * b["scagr"])
    if which == "full":
        d["OOS"] = metrics(r.loc[OOS_START:])["Sharpe"] - b["soos"]
    return d


def pass4a(r, base):
    h1, h2 = halves(r)
    b1, b2 = halves(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


# =====================================================================================
# panels
# =====================================================================================
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad & set(px.columns))


def get_panels():
    P = {}
    P["u56"] = (load_universe(), None)
    P["broad"] = (load_universe(broad=True), None)
    sp, ndrop = small_panel()
    P["small"] = (sp, ndrop)
    return P


# =====================================================================================
# LEG 1 — GATES
# =====================================================================================
DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})_")


def vintage_map():
    """file -> (stamp date from the filename, first git-add date if git can still see it)."""
    stamps = {}
    for f in sorted(glob.glob(str(OUT / "*"))):
        b = os.path.basename(f)
        m = DATE_RE.match(b)
        if m:
            stamps[b] = m.group(1)
    gitdate = {}
    try:
        raw = subprocess.run(
            ["git", "log", "--diff-filter=A", "--name-only", "--date=short", "--format=@%ad",
             "--", "research/backtests"],
            cwd=str(ROOT), capture_output=True, text=True, timeout=300).stdout
        cur = None
        for line in raw.splitlines():
            if line.startswith("@"):
                cur = line[1:].strip()
            elif line.strip() and cur:
                # git log is newest-first, so later lines are OLDER commits and the last
                # assignment for a name is its first (oldest) add.
                gitdate[os.path.basename(line.strip())] = cur
    except Exception as e:
        say(f"  (git vintage unavailable: {type(e).__name__})")
    return stamps, gitdate


def gates(panels, stamps, gitdate):
    say("=" * 100)
    say("GATES (run before any new number is read)")
    say("=" * 100)
    ok = True
    for pk, (px, _) in panels.items():
        inv = [c for c in px.columns if not (pk == "small" and c == "SPY")]
        W = book_weights(px, "TOP20", inv, 0.75)
        start = px.index[260]
        r_f, t_f = fast_bt(px, W)
        e0 = backtest(px, W, cost_bps=0.0, freq=FREQ)
        d_r = float((r_f.loc[start:] - e0["returns"].loc[start:]).abs().max())
        d_t = float((t_f.loc[start:] - e0["turnover"].loc[start:]).abs().max())
        e25 = backtest(px, W, cost_bps=25.0, freq=FREQ)
        d_c = float(((r_f - t_f * 25.0 / 1e4).loc[start:] - e25["returns"].loc[start:]).abs().max())
        say(f"  G1 {pk:>5}: fast_bt vs engine.backtest   max|dr| {d_r:.3e}   max|dturnover| {d_t:.3e}")
        say(f"  G2 {pk:>5}: rung identity vs live 25 bps max|dr| {d_c:.3e}")
        ok &= (d_r < 1e-12) and (d_t < 1e-12) and (d_c < 1e-12)

    both = [b for b in stamps if b in gitdate]
    bad = [b for b in both if stamps[b] > gitdate[b]]
    say(f"  G3 VINTAGE: {len(stamps)} stamped artefacts; git can still see the add commit of "
        f"{len(both)} of them ({len(both)/max(len(stamps),1):.1%}); "
        f"stamp AFTER its add commit in {len(bad)} — a stamp must never post-date its commit")
    say(f"     (the repo history is shallow: {sorted(set(gitdate.values()))[:1]} .. "
        f"{sorted(set(gitdate.values()))[-1:]}, so the FILENAME STAMP is the only vintage that "
        f"reaches the whole record, and it is what this run uses.)")
    ok &= (len(bad) == 0)

    if I613_CENSUS.exists():
        c613 = pd.read_csv(I613_CENSUS)
        nA = int((c613.tierA == 1).sum())
        nboth = int(((c613.tierA == 1) & (c613.has_to == 1) & (c613.has_cost == 1)).sum())
        say(f"  G4 idea 613's committed census: TIER-A width files {nA} (published 44); "
            f"re-priceable {nboth} (published 1)")
        ok &= (nA == 44 and nboth == 1)
    else:
        say("  G4 SKIPPED: idea 613 .census.csv not found")
        ok = False
    say(f"  GATES {'PASS' if ok else 'FAIL'}")
    return ok


# =====================================================================================
# LEG 2 — CENSUS of the record's five 'publish X beside every Y' prescriptions
# =====================================================================================
NOT_A_QUANTITY = re.compile(r"(spearman|kendall|pearson|rho|corr|_ok$|^ok_|flag|share|frac|pct|"
                            r"rate|^has_|^n_|count)", re.I)
OUTCOME = re.compile(r"(sharpe|cagr|maxdd|^dd$|_dd$|calmar)", re.I)

# ---- claim (Y) and required-column (X) detectors, one pair per prescription ----------
PANEL_C = re.compile(r"(^panel$|^panels$|^universe$|^panel_id$|^pk$|^panelset$)", re.I)
EWALL_C = re.compile(r"(ewall|ew_all|eq_?all|unrank|un_rank|^ew$|_ew$|^ew_)", re.I)
REGIME_C = re.compile(r"(^regime$|d_on$|d_off$|_on$|_off$|^on_|^off_|on_share|cond_on|cond_off)",
                      re.I)
GROSS_C = re.compile(r"gross", re.I)
CMP_C = re.compile(r"(^d?cagr|^d?maxdd|dCAGR|dMaxDD|excess|^ctrl_|^ctl_|^base_|^control|_ctrl$|"
                   r"_ctl$|vs_)", re.I)
TWIN_C = re.compile(r"(twin|matched|matchedgross|matched_gross|grossmatch|degross|de_gross|"
                    r"^mg_|_mg$|ctrl|ctl_|control)", re.I)
PLACEBO_C = re.compile(r"(placebo|null|shuffl|permut|bootstrap|^rand|_rand|random)", re.I)
COST_C = re.compile(r"(cost_bps|^cost$|^bps$|^rung$|rung|_bps$|^cost_)", re.I)


def _num(v):
    return pd.to_numeric(v, errors="coerce").dropna()


def v_gross(v):
    """A realised/target gross: non-negative, at most 2.5x, and actually invested."""
    v = _num(v)
    return len(v) >= 2 and float(v.min()) >= 0.0 and float(v.max()) <= 2.5 and float(v.max()) > 0.0


def v_outcome(v):
    v = _num(v)
    return len(v) >= 2 and np.isfinite(v).all() and float(v.abs().max()) < 1e4


def v_rung(v):
    """A cost ladder able to price a crossing cost: >=2 distinct rungs in [0, 500] bps."""
    v = _num(v)
    return v.nunique() >= 2 and float(v.min()) >= 0.0 and float(v.max()) <= 500.0 and float(v.max()) > 0.0


def v_multi(v):
    """A witness column that actually varies (>=2 distinct values)."""
    return pd.Series(v).astype(str).nunique() >= 2


def v_placebo(v):
    v = _num(v)
    return len(v) >= 2 and np.isfinite(v).all()


# Each prescription: (id, label, proposal date, Y-detector, X-detector, strict-Y, strict-X)
PRESC = [
    dict(pid="239", label="publish EWall beside every PANEL claim", date="2026-09-06",
         y="a per-panel outcome (panel/universe column + a Sharpe/CAGR/MaxDD column)",
         x="an un-ranked EWall control column"),
    dict(pid="471", label="publish MATCHED GROSS on every d_on/d_off REGIME SPLIT",
         date="2026-09-08",
         y="a regime split (on/off witness + an outcome column)",
         x="BOTH arms' gross (>=2 valid gross columns)"),
    dict(pid="583", label="publish BOTH arms' GROSS beside every CAGR/MaxDD comparison",
         date="2026-09-09",
         y="a clause-vs-control comparison quoted on CAGR or MaxDD",
         x="BOTH arms' gross (>=2 valid gross columns)"),
    dict(pid="604", label="publish a PLACEBO column beside every MATCHED-GROSS TWIN claim",
         date="2026-09-10",
         y="a twin / matched-gross / de-grossed-control site",
         x="a placebo / null column"),
    dict(pid="607", label="publish a CROSSING COST beside every TWIN claim", date="2026-09-10",
         y="a twin / matched-gross / de-grossed-control site",
         x="a cost ladder with >=2 distinct rungs"),
]


def classify(hdr, D, strict):
    """Return {pid: (has_claim, has_column)} for one file's header (and, when strict, values)."""
    def cols(rx):
        return [c for c in hdr if rx.search(c)]

    def valid(cs, fn):
        if not strict:
            return [c for c in cs if not NOT_A_QUANTITY.search(c)] if fn is not v_multi else cs
        keep = []
        for c in cs:
            if fn is not v_multi and NOT_A_QUANTITY.search(c):
                continue
            if D is not None and c in D.columns:
                try:
                    if fn(D[c]):
                        keep.append(c)
                except Exception:
                    pass
        return keep

    out = {}
    panel = valid(cols(PANEL_C), v_multi)
    outc = valid(cols(OUTCOME), v_outcome)
    ew = valid(cols(EWALL_C), v_outcome)
    reg = valid(cols(REGIME_C), v_multi)
    gr = valid(cols(GROSS_C), v_gross)
    cmpc = valid([c for c in hdr if CMP_C.search(c) and OUTCOME.search(c)], v_outcome)
    twin = valid(cols(TWIN_C), v_outcome)
    pl = valid(cols(PLACEBO_C), v_placebo)
    rung = valid(cols(COST_C), v_rung)

    out["239"] = (bool(panel and outc), bool(ew))
    out["471"] = (bool(reg and outc), bool(len(gr) >= 2))
    out["583"] = (bool(cmpc), bool(len(gr) >= 2))
    out["604"] = (bool(twin), bool(pl))
    out["607"] = (bool(twin), bool(rung))
    return out


def census(stamps):
    say()
    say("=" * 100)
    say("LEG 2 — CENSUS: every committed CSV in research/backtests, five prescriptions x two")
    say("         strictness tiers x three vintages")
    say("=" * 100)
    files = [f for f in sorted(glob.glob(str(OUT / "*.csv"))) + sorted(glob.glob(str(OUT / "*.csv.gz")))
             if STEM not in os.path.basename(f)]       # never census this run's own artefacts
    rows = []
    for f in files:
        b = os.path.basename(f)
        try:
            if f.endswith(".gz"):
                with gzip.open(f, "rt", newline="") as fh:
                    hdr = next(csv.reader(fh))
            else:
                with open(f, newline="") as fh:
                    hdr = next(csv.reader(fh))
        except Exception:
            continue
        hdr = [c.strip() for c in hdr]
        wanted = set()
        for rx in (PANEL_C, OUTCOME, EWALL_C, REGIME_C, GROSS_C, CMP_C, TWIN_C, PLACEBO_C, COST_C):
            wanted |= {c for c in hdr if rx.search(c)}
        D = None
        if wanted:
            try:
                D = pd.read_csv(f, usecols=lambda c: c.strip() in wanted, nrows=4000)
                D.columns = [c.strip() for c in D.columns]
            except Exception:
                D = None
        loose = classify(hdr, None, False)
        strict = classify(hdr, D, True)
        r = dict(file=b, stamp=stamps.get(b, ""), n_cols=len(hdr))
        for p in PRESC:
            pid = p["pid"]
            r[f"L{pid}_claim"], r[f"L{pid}_col"] = int(loose[pid][0]), int(loose[pid][1])
            r[f"S{pid}_claim"], r[f"S{pid}_col"] = int(strict[pid][0]), int(strict[pid][1])
        rows.append(r)
    C = pd.DataFrame(rows)
    say(f"committed CSVs scanned: {len(C)} (this run's own artefacts excluded); "
        f"{int((C.stamp != '').sum())} carry a filename date stamp")
    return C


def presc_table(C):
    say()
    say("-" * 100)
    say("H1/H2 — re-priceable share, per prescription x strictness x vintage")
    say("-" * 100)
    say("  PRE = files stamped STRICTLY BEFORE the proposal date (what the prescribing run could")
    say("  actually see).  AT = stamped on or before it.  NOW = the whole committed record.")
    out = []
    for p in PRESC:
        pid, d = p["pid"], p["date"]
        say(f"\n  idea {pid} — {p['label']}   (proposed {d})")
        say(f"      Y = {p['y']}")
        say(f"      X = {p['x']}")
        say(f"      {'tier':>7} {'vintage':>8} {'files':>7} {'Y-claim files':>14} "
            f"{'+X':>6} {'RE-PRICEABLE':>13}")
        for tier, pre in (("LOOSE", "L"), ("STRICT", "S")):
            for vin in ("PRE", "AT", "NOW"):
                if vin == "NOW":
                    sub = C
                else:
                    ok = C.stamp != ""
                    sub = C[ok & ((C.stamp < d) if vin == "PRE" else (C.stamp <= d))]
                cl = sub[sub[f"{pre}{pid}_claim"] == 1]
                n = len(cl)
                k = int((cl[f"{pre}{pid}_col"] == 1).sum())
                shr = k / n if n else np.nan
                say(f"      {tier:>7} {vin:>8} {len(sub):>7} {n:>14} {k:>6} "
                    f"{('%.1f%%' % (100*shr)) if n else 'n/a':>13}")
                out.append(dict(pid=pid, label=p["label"], proposed=d, tier=tier, vintage=vin,
                                files=len(sub), claim_files=n, with_col=k, reprice_share=shr))
    P = pd.DataFrame(out)
    say()
    say("  HEADLINE (STRICT tier, at the point each prescription was proposed):")
    for p in PRESC:
        r = P[(P.pid == p["pid"]) & (P.tier == "STRICT") & (P.vintage == "PRE")].iloc[0]
        rn = P[(P.pid == p["pid"]) & (P.tier == "STRICT") & (P.vintage == "NOW")].iloc[0]
        say(f"    idea {p['pid']:>3}: {int(r.with_col):>4} of {int(r.claim_files):>5} claim files "
            f"re-priceable at proposal ({(100*r.reprice_share if r.claim_files else float('nan')):.1f}%)"
            f"   ->  now {int(rn.with_col):>4} of {int(rn.claim_files):>5} "
            f"({100*rn.reprice_share:.1f}%)")
    say("    idea 613 (published control): 1 of 44 strict width files re-priceable (2.3%)")
    return P


def self_site(C, P):
    """H3 — where does the X column live?  In the prescribing run's own artefacts, or elsewhere?"""
    say()
    say("-" * 100)
    say("H3 — is the re-priceable set just the PRESCRIBING RUN'S OWN artefacts?")
    say("-" * 100)
    say(f"  {'idea':>5} {'re-priceable files (STRICT, NOW)':>34} {'stamped ON/AFTER proposal':>26} "
        f"{'stamped BEFORE':>15}")
    for p in PRESC:
        pid, d = p["pid"], p["date"]
        cl = C[(C[f"S{pid}_claim"] == 1) & (C[f"S{pid}_col"] == 1)]
        after = int(((cl.stamp >= d) & (cl.stamp != "")).sum())
        before = int(((cl.stamp < d) & (cl.stamp != "")).sum())
        say(f"  {pid:>5} {len(cl):>34} {after:>26} {before:>15}")
    say("  (613's own finding was the extreme case: the ONLY re-priceable width file was the one")
    say("   that made the prescription.)")


# =====================================================================================
# LEG 3 — FRESH GRID: a book that carries ALL FIVE prescribed columns by construction
# =====================================================================================
def run_panel(pk, px, ndrop):
    inv = [c for c in px.columns if not (pk == "small" and c == "SPY")]
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    bars_full = bars_of(spy, "full")
    bars_is = bars_of(spy, "IS")
    v2r, v2t = fast_bt(px, rules_v2_weights(px))
    v2 = {c: (v2r - v2t * c / 1e4).loc[start:] for c in RUNGS}
    say(f"\n  panel {pk}: {px.shape[1]} cols ({len(inv)} investable"
        + (f", {ndrop} tickers dropped for max_1d_move>=1.0" if ndrop else "") +
        f"), {px.index[0].date()} -> {px.index[-1].date()}, evaluated from {start.date()}")
    say(f"    SPY bars: H1 {bars_full['s1']:.3f}  H2 {bars_full['s2']:.3f}  "
        f"OOS {bars_full['soos']:.3f}  MaxDD {bars_full['sdd']:.1%}  CAGR {bars_full['scagr']:.2%}")

    gates_ = {b: band_gate(px[inv], b).reindex(columns=px.columns).fillna(False) for b in BANDS}
    placebos = {b: block_shuffle(gates_[b]) for b in BANDS}

    rows, series = [], {}
    for book in BOOKS:
        for g in GROSSES:
            raw = book_weights(px, book, inv, g)
            r_c, t_c = fast_bt(px, raw)
            r_c, t_c = r_c.loc[start:], t_c.loc[start:]
            g_ctrl = mean_gross(raw, start)
            series[(pk, book, g, "na", "CTRL")] = (r_c, t_c)
            for b in BANDS:
                W_arm = raw.where(gates_[b], 0.0)
                W_pla = raw.where(placebos[b], 0.0)
                g_arm = mean_gross(W_arm, start)
                s = g_arm / g_ctrl if g_ctrl > 0 else 0.0
                W_twin = raw * s                       # matched-mean-gross static twin
                forms = {"ARM": W_arm, "CTRL": None, "TWIN": W_twin, "PLACEBO": W_pla}
                for fname, W in forms.items():
                    if fname == "CTRL":
                        r0, t0 = r_c, t_c
                    else:
                        r0, t0 = fast_bt(px, W)
                        r0, t0 = r0.loc[start:], t0.loc[start:]
                    series[(pk, book, g, b, fname)] = (r0, t0)
                    gm = g_arm if fname == "ARM" else (
                        g_ctrl if fname == "CTRL" else mean_gross(W, start))
                    for c in RUNGS:
                        r = r0 - t0 * c / 1e4
                        m = metrics(r)
                        mg = margins(r, bars_full, "full")
                        mgi = margins(r.loc[:IS_END], bars_is, "IS")
                        rows.append(dict(
                            panel=pk, book=book, gross=g, band=b, form=fname, cost=c,
                            mean_gross=gm, on_share=float(gates_[b].loc[start:].mean().mean()),
                            arm_to=float(t0.sum() / (len(t0) / 252)),
                            CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                            H1=halves(r)[0], H2=halves(r)[1],
                            OOSs=metrics(r.loc[OOS_START:])["Sharpe"],
                            **{f"m_{k}": mg[k] for k in BARS5},
                            m_min=min(mg[k] for k in BARS5),
                            pass4b=all(mg[k] > 0 for k in BARS5), pass4a=pass4a(r, v2[c]),
                            IS_pass4b=all(mgi[k] > 0 for k in ("H1", "H2", "DD", "CAGR")),
                            IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                            IS_CAGR=metrics(r.loc[:IS_END])["CAGR"]))
    return pd.DataFrame(rows), series, v2, bars_full


def reread(G):
    """H4 — re-read every clause-vs-control verdict against each prescribed comparand."""
    say()
    say("=" * 100)
    say("LEG 4 — WHAT THE MISSING COLUMN COSTS, measured on a fresh grid that carries all five")
    say("=" * 100)
    say("  The record's usual comparand is the FULL-GROSS control (same book, gate removed, same")
    say("  nominal gross).  Each prescription names a DIFFERENT comparand or column.  For every")
    say("  (panel, book, gross, band, rung) cell the arm's verdict is read five ways.")
    out = []
    idx = ["panel", "book", "gross", "band", "cost"]
    piv = G.pivot_table(index=idx, columns="form",
                        values=["CAGR", "Sharpe", "MaxDD", "mean_gross"], aggfunc="first")
    ew = G[G.book == "EWALL"].set_index(["panel", "gross", "band", "cost", "form"])
    for key, r in piv.iterrows():
        pk, book, g, b, c = key
        try:
            e = ew.loc[(pk, g, b, c, "ARM")]
        except KeyError:
            continue
        row = dict(panel=pk, book=book, gross=g, band=b, cost=c,
                   arm_gross=r[("mean_gross", "ARM")], ctrl_gross=r[("mean_gross", "CTRL")],
                   twin_gross=r[("mean_gross", "TWIN")])
        for stat, sign in (("CAGR", +1), ("Sharpe", +1), ("MaxDD", +1)):
            a = r[(stat, "ARM")]
            row[f"d{stat}_vs_CTRL"] = a - r[(stat, "CTRL")]
            row[f"d{stat}_vs_TWIN"] = a - r[(stat, "TWIN")]
            row[f"d{stat}_vs_PLACEBO"] = a - r[(stat, "PLACEBO")]
            row[f"d{stat}_vs_EWALL"] = a - float(e[stat])
        out.append(row)
    R = pd.DataFrame(out)
    for stat in ("CAGR", "Sharpe", "MaxDD"):
        for comp in ("CTRL", "TWIN", "PLACEBO", "EWALL"):
            R[f"win_{stat}_{comp}"] = R[f"d{stat}_vs_{comp}"] > 0

    say()
    say("  (a) VERDICT FLIPS — of the cells the record would publish as a WIN against the")
    say("      full-gross control, how many survive each prescribed re-reading?")
    say(f"      {'stat':>7} {'wins vs CTRL':>13} {'survive TWIN':>13} {'survive PLACEBO':>16} "
        f"{'survive EWALL':>14}")
    flips = []
    for stat in ("CAGR", "Sharpe", "MaxDD"):
        w = R[R[f"win_{stat}_CTRL"]]
        n = len(w)
        st = int(w[f"win_{stat}_TWIN"].sum())
        sp = int(w[f"win_{stat}_PLACEBO"].sum())
        se = int(w[f"win_{stat}_EWALL"].sum())
        say(f"      {stat:>7} {n:>13} {st:>7} ({st/max(n,1):.0%}) {sp:>9} ({sp/max(n,1):.0%}) "
            f"{se:>7} ({se/max(n,1):.0%})")
        flips.append(dict(stat=stat, wins_vs_CTRL=n, survive_TWIN=st, survive_PLACEBO=sp,
                          survive_EWALL=se))
    say("      A prescription is COSMETIC where the survival share is 100% and BINDING where it")
    say("      is not.  Sharpe is exposure-blind by construction (idea 581), CAGR and MaxDD are")
    say("      not — the gross column is exactly the difference.")

    say()
    say("  (b) the 583/471 GROSS column, quantified: how big is the arm-vs-control gap that is")
    say("      pure exposure?")
    for stat in ("CAGR", "MaxDD"):
        say(f"      {stat}: median |d vs CTRL| {R[f'd{stat}_vs_CTRL'].abs().median():.4f}   "
            f"median |d vs TWIN| {R[f'd{stat}_vs_TWIN'].abs().median():.4f}   "
            f"ratio {R[f'd{stat}_vs_CTRL'].abs().median()/max(R[f'd{stat}_vs_TWIN'].abs().median(),1e-12):.2f}x")
    say(f"      mean realised gross: arm {R.arm_gross.mean():.3f}  control {R.ctrl_gross.mean():.3f}  "
        f"twin {R.twin_gross.mean():.3f}  (twin matches the arm by construction: "
        f"max|gap| {float((R.twin_gross-R.arm_gross).abs().max()):.2e})")

    say()
    say("  (c) the 607 CROSSING COST: the rung at which the arm's win over its matched-gross twin")
    say("      turns into a loss.  A claim published at or above its crossing cost is a coin flip.")
    cs = []
    for (pk, book, g, b), sub in R.groupby(["panel", "book", "gross", "band"]):
        sub = sub.sort_values("cost")
        for stat in ("CAGR", "Sharpe"):
            d = sub[f"d{stat}_vs_TWIN"].values
            rr = sub["cost"].values
            star = np.nan
            for i in range(len(rr)):
                if d[i] <= 0:
                    star = rr[i]
                    break
            cs.append(dict(panel=pk, book=book, gross=g, band=b, stat=stat, cstar=star,
                           d_at_0=d[0], d_at_10=d[list(rr).index(10.0)]))
    CS = pd.DataFrame(cs)
    for stat in ("CAGR", "Sharpe"):
        s = CS[CS.stat == stat]
        say(f"      {stat}: {int(s.cstar.notna().sum())} of {len(s)} cells cross inside the "
            f"[0, 50] bps ladder; median crossing cost "
            f"{s.cstar.median() if s.cstar.notna().any() else float('nan'):.1f} bps; "
            f"{int((s.cstar <= 10).sum())} cross at or below PROTOCOL's own 10 bps rung "
            f"({int((s.d_at_0 <= 0).sum())} are already losing at 0 bps)")
    return R, CS, pd.DataFrame(flips)


def main():
    T0 = time.time()
    say("=" * 100)
    say("IDEA 616 — is the RE-PRICEABLE set empty on every published COLUMN prescription?  (lane C)")
    say("=" * 100)
    say("tuned parameter 1 (prescription set): 239 EWall / 471 matched-gross / 583 gross / "
        "604 placebo / 607 crossing cost — all five reported, 613 WIDTH as the published control")
    say("tuned parameter 2 (strictness): LOOSE (header keyword) / STRICT (keyword + value check) "
        "— both reported")
    say("reported (not tuned): vintage PRE / AT / NOW; panels, books, bands, grosses, rungs")
    say(f"fresh grid dials, fully enumerated, never chosen: bands {BANDS}  grosses {GROSSES}")
    say(f"books {BOOKS}; panels {PANELS}; rungs {RUNGS} bps; weekly, t+1; "
        f"IS <= {IS_END}, OOS >= {OOS_START}; placebo = block-{BLOCK} time shuffle, seed {SEED}")

    stamps, gitdate = vintage_map()
    panels = get_panels()
    if not gates(panels, stamps, gitdate):
        say("\n*** GATES FAILED — no new number is read. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
        return 1

    C = census(stamps)
    C.to_csv(OUT / f"{STEM}.census.csv", index=False)
    P = presc_table(C)
    P.to_csv(OUT / f"{STEM}.presc.csv", index=False)
    self_site(C, P)

    say()
    say("=" * 100)
    say(f"LEG 3 — FRESH GRID ({len(PANELS)} panels x {len(BOOKS)} books x {len(GROSSES)} grosses "
        f"x {len(BANDS)} bands x 4 forms, read at {len(RUNGS)} rungs)")
    say("=" * 100)
    G, SER, V2, BARS = [], {}, {}, {}
    for pk in PANELS:
        px, ndrop = panels[pk]
        g, ser, v2, bars = run_panel(pk, px, ndrop)
        G.append(g)
        SER.update(ser)
        V2[pk] = v2
        BARS[pk] = bars
    G = pd.concat(G, ignore_index=True)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    nsim = G[["panel", "book", "gross", "band", "form"]].drop_duplicates().shape[0]
    say(f"\n  {len(G)} arm-rows written ({nsim} simulations x {len(RUNGS)} rungs).")

    R, CS, FL = reread(G)
    R.to_csv(OUT / f"{STEM}.reread.csv", index=False)
    CS.to_csv(OUT / f"{STEM}.cstar.csv", index=False)

    # --- KEEP paths ----------------------------------------------------------------
    say()
    say("-" * 100)
    say("KEEP PATHS (PROTOCOL 4) — both evaluated on EVERY arm-row")
    say("-" * 100)
    say(f"  4a (vs live RULES v2, cost-matched): {int(G.pass4a.sum())} / {len(G)}")
    say(f"  4b (vs SPY, all five bars)         : {int(G.pass4b.sum())} / {len(G)}")
    say(f"  BOTH                               : {int((G.pass4a & G.pass4b).sum())} / {len(G)}")
    for c in RUNGS:
        s = G[G.cost == c]
        say(f"    @{c:>4.0f} bps: 4a {int(s.pass4a.sum()):>4}  4b {int(s.pass4b.sum()):>4}  "
            f"BOTH {int((s.pass4a & s.pass4b).sum()):>4}   of {len(s)}")
    say("  by (panel, book, form) @10 bps:")
    for (pk, book, fm), s in G[G.cost == 10].groupby(["panel", "book", "form"]):
        say(f"    {pk:>6} {book:>6} {fm:>8}: 4a {int(s.pass4a.sum()):>3}  "
            f"4b {int(s.pass4b.sum()):>3}  BOTH {int((s.pass4a & s.pass4b).sum()):>3}  of {len(s)}")

    # --- rule 8 --------------------------------------------------------------------
    say()
    say("-" * 100)
    say("RULE 8 (PROTOCOL 8) — (band, gross) chosen on 2009-2016 ONLY, 2017-2026 read once")
    say("-" * 100)
    say("  Four pre-registered selectors.  S2 and S3 are the QUESTION as a selector: S2 ranks the")
    say("  arm by its IS margin over the FULL-GROSS control (the comparand the record publishes")
    say("  when the gross column is absent); S3 ranks it by its margin over the MATCHED-GROSS")
    say("  TWIN (the comparand ideas 471/583 prescribe).  If the column is cosmetic they pick the")
    say("  same book.")
    wf = []
    ARM = G[G.form == "ARM"]
    for pk in PANELS:
        px, _ = panels[pk]
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        spy_o = spy.loc[OOS_START:]
        mo = metrics(spy_o)
        bars_o = dict(s1=metrics(spy_o.iloc[:len(spy_o) // 2])["Sharpe"],
                      s2=metrics(spy_o.iloc[len(spy_o) // 2:])["Sharpe"],
                      sdd=mo["MaxDD"], scagr=mo["CAGR"], soos=mo["Sharpe"])
        for book in BOOKS:
            for c in RUNGS:
                sub = ARM[(ARM.panel == pk) & (ARM.book == book) & (ARM.cost == c)].copy()
                ctl = G[(G.panel == pk) & (G.book == book) & (G.cost == c) &
                        (G.form == "CTRL")].set_index(["gross", "band"])
                twn = G[(G.panel == pk) & (G.book == book) & (G.cost == c) &
                        (G.form == "TWIN")].set_index(["gross", "band"])
                sub["dIS_ctrl"] = [r.IS_Sharpe - float(ctl.loc[(r.gross, r.band), "IS_Sharpe"])
                                   for r in sub.itertuples()]
                sub["dIS_twin"] = [r.IS_Sharpe - float(twn.loc[(r.gross, r.band), "IS_Sharpe"])
                                   for r in sub.itertuples()]
                picks = {"S0_ISsharpe": sub.loc[sub.IS_Sharpe.idxmax()]}
                scr = sub[sub.IS_pass4b]
                picks["S1_IS4b"] = (scr.loc[scr.IS_Sharpe.idxmax()] if len(scr)
                                    else sub.loc[sub.IS_Sharpe.idxmax()])
                picks["S2_vsCTRL"] = sub.loc[sub.dIS_ctrl.idxmax()]
                picks["S3_vsTWIN"] = sub.loc[sub.dIS_twin.idxmax()]
                for sname, p in picks.items():
                    r0, t0 = SER[(pk, book, float(p.gross), float(p.band), "ARM")]
                    r = (r0 - t0 * c / 1e4).loc[OOS_START:]
                    m = metrics(r)
                    h = len(r) // 2
                    o4b = dict(H1=metrics(r.iloc[:h])["Sharpe"] - bars_o["s1"],
                               H2=metrics(r.iloc[h:])["Sharpe"] - bars_o["s2"],
                               OOS=m["Sharpe"] - bars_o["soos"],
                               DD=DELTA * abs(bars_o["sdd"]) - abs(m["MaxDD"]),
                               CAGR=m["CAGR"] - PHI * bars_o["scagr"])
                    v2o = V2[pk][c].loc[OOS_START:]
                    mv = metrics(v2o)
                    wf.append(dict(panel=pk, book=book, cost=c, selector=sname,
                                   band=float(p.band), gross=float(p.gross),
                                   OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"],
                                   SPY_CAGR=mo["CAGR"], SPY_Sharpe=mo["Sharpe"],
                                   SPY_MaxDD=mo["MaxDD"], V2_CAGR=mv["CAGR"],
                                   V2_Sharpe=mv["Sharpe"], V2_MaxDD=mv["MaxDD"],
                                   beats_SPY=bool(m["Sharpe"] > mo["Sharpe"]),
                                   beats_V2=bool(m["Sharpe"] > mv["Sharpe"]),
                                   OOS_4b=all(v > 0 for v in o4b.values()),
                                   OOS_4a=pass4a(r, v2o)))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.wf.csv", index=False)
    say(WF.groupby("selector").agg(
        picks=("band", "size"), median_band=("band", "median"), median_gross=("gross", "median"),
        OOS_Sharpe=("OOS_Sharpe", "mean"), OOS_CAGR=("OOS_CAGR", "mean"),
        OOS_MaxDD=("OOS_MaxDD", "mean"), beats_SPY=("beats_SPY", "sum"),
        beats_V2=("beats_V2", "sum"), OOS_4b=("OOS_4b", "sum"), OOS_4a=("OOS_4a", "sum")
    ).to_string(float_format=lambda x: f"{x:.4f}"))
    say()
    for pk in PANELS:
        s = WF[(WF.panel == pk) & (WF.cost == 10)]
        say(f"  {pk:>6} @10 bps  SPY OOS: CAGR {s.SPY_CAGR.iloc[0]:.2%}  Sharpe "
            f"{s.SPY_Sharpe.iloc[0]:.3f}  MaxDD {s.SPY_MaxDD.iloc[0]:.1%}   |   "
            f"RULES v2 OOS: CAGR {s.V2_CAGR.iloc[0]:.2%}  Sharpe {s.V2_Sharpe.iloc[0]:.3f}  "
            f"MaxDD {s.V2_MaxDD.iloc[0]:.1%}")
        for sn, gg in s.groupby("selector"):
            say(f"          {sn:>12}: OOS CAGR {gg.OOS_CAGR.mean():.2%}  Sharpe "
                f"{gg.OOS_Sharpe.mean():.3f}  MaxDD {gg.OOS_MaxDD.mean():.1%}  "
                f"4b {int(gg.OOS_4b.sum())}/{len(gg)}  4a {int(gg.OOS_4a.sum())}/{len(gg)}")
    say()
    d = WF[WF.selector.isin(["S2_vsCTRL", "S3_vsTWIN"])].pivot_table(
        index=["panel", "book", "cost"], columns="selector", values=["band", "gross"])
    agree = ((d[("band", "S2_vsCTRL")] == d[("band", "S3_vsTWIN")]) &
             (d[("gross", "S2_vsCTRL")] == d[("gross", "S3_vsTWIN")]))
    say(f"  S2 (vs full-gross control, the column-BLIND comparand) vs S3 (vs matched-gross twin,")
    say(f"  the PRESCRIBED comparand): identical rule-8 pick in {int(agree.sum())}/{len(d)} cells "
        f"({agree.mean():.1%}).  Where they differ the missing gross column changes the BOOK,")
    say(f"  not just the number.")
    for sn in ("S2_vsCTRL", "S3_vsTWIN"):
        s = WF[WF.selector == sn]
        say(f"    {sn:>10}: OOS Sharpe {s.OOS_Sharpe.mean():.4f}  CAGR {s.OOS_CAGR.mean():.2%}  "
            f"MaxDD {s.OOS_MaxDD.mean():.2%}  beats SPY {int(s.beats_SPY.sum())}/{len(s)}  "
            f"4b {int(s.OOS_4b.sum())}/{len(s)}  4a {int(s.OOS_4a.sum())}/{len(s)}")

    say()
    say("=" * 100)
    say(f"done in {time.time() - T0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
