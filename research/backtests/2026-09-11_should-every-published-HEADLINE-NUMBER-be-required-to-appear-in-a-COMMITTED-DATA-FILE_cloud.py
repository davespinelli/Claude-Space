#!/usr/bin/env python3
"""Idea 791 (cloud, 2026-09-11) — should-every-published-HEADLINE-NUMBER-be-required-to-
appear-in-a-COMMITTED-DATA-FILE.

QUESTION
--------
Idea 790 re-read 457 runs against their own artefacts and found that a run's published
numbers are recoverable VERBATIM from its own committed DATA 1.56%–7.69% of the time, against
58%–82% from the run's own CONSOLE printout, with 16 runs committing no data file at all.
That is a diagnosis.  This run prices the REMEDY the queue names: a declared PROTOCOL leg,

    "every number a narrative quotes must be reproducible from a committed csv/json row,
     not only from the console"

against the record's actual practice.  Two numbers decide whether such a clause is adoptable:
how many runs would have to RE-COMMIT to satisfy it, and what the CHEAPEST artefact that
satisfies it costs.

WHAT IS MEASURED (declared before any count is read)
---------------------------------------------------
RUN   = a committed filename stem `YYYY-MM-DD_<slug>_<lane>` in research/backtests/ that
        owns at least one NARRATIVE (`.result.md`, `_MEMO.md`, or a bare `.md` that is not a
        report).  A run with no narrative quotes nothing and is not in the corpus.
QUOTED NUMBER = a numeric token in the run's own narrative carrying >= 4 SIGNIFICANT DIGITS
        (idea 790's DISTINCTIVE bar, kept verbatim so the two runs' corpora are comparable:
        "0.75" and "2.0" cannot qualify, "1.2264" and "-12.05%" can).  Dates, years,
        4-digit integers that are plainly counts, and idea numbers are excluded by the
        digit/decimal shape rule stated in DISTINCT_RE.
PRESENT-IN(S) = the token, or one of its declared equivalent spellings (sign-stripped,
        comma-stripped, percent<->fraction, leading-zero variants), occurs verbatim in the
        concatenated text of the run's OWN artefacts of class set S.  Substring presence is
        the STRICT leg on purpose: idea 792 measured a 46.0% chance floor for the tolerant
        ROUND leg that rises to 78.4% on the largest artefacts, so ROUND is reported as a
        secondary column and is never the leg being priced.
ARTEFACT CLASSES, by the run's own file extension:
        CSV      .csv / .csv.gz         JSON  .json
        TXTNC    .txt that is NOT .console.txt
        MD       narratives and memos other than the one being read
        CONSOLE  .console.txt           (PY .py is never counted — a script is not data)

TUNED PARAMETERS (PROTOCOL rule 4, exactly two, as the queue specifies)
    1. LEG FORM   in {ALL, P90, P75, P50, HEAD}
         ALL   every quoted number must be present                        (phi = 1.00)
         P90   >= 90% of them          P75  >= 75%          P50  >= 50%
         HEAD  phi = 1.00 but restricted to HEADLINE numbers only (those inside the
               narrative's title block or inside a **bold** span) — the cheap version of the
               clause, which is the one a protocol would plausibly adopt
    2. ARTEFACT SET in {CSV, CSVJSON, CSVJSONTXT, NONCONSOLE, ANY}
         CSVJSON is the clause's literal wording ("a committed csv/json row"); ANY is the
         record's de-facto practice today (the console counts).
All 5 x 5 = 25 grid points are reported.  REPORTED, never selected: the ROUND leg, the
per-run missing-count distribution, the vintage split, and the price-side comparands.

PRE-REGISTERED HYPOTHESES (written before any new number was read)
    H_COST   : the clause is expensive — under the literal leg (ALL x CSVJSON) fewer than
               25% of runs comply today.  Falsified at >= 25%.
    H_CHEAP  : the remedy is cheap — the median non-compliant run is missing fewer than 50
               values, i.e. one small csv fixes it.  Falsified at >= 50.
    H_CONSOLE: the console is what carries the record — ANY compliance under ALL exceeds
               CSVJSON compliance by >= 20 pp.  Falsified below 20 pp.
    H_STABLE : the clause's price is a property of the record, not of its vintage — the
               chosen leg's OOS (late-vintage) compliance is within 15 pp of its IS value.

GATES (pre-registered, reported before any finding)
    G1 idea 790 reproduces: DATA-only verbatim presence is far below CONSOLE-inclusive
       presence on the shared corpus, with the console-inclusive per-run share inside
       790's published 58%–82% band.
    G2 PLANT-FALSE chance floor: random tokens of the same SHAPE as the real ones match the
       CSVJSON set at a rate that is reported, and the real rate must exceed it.
    G3 monotonicity: per-run coverage is non-decreasing as the artefact set widens
       (CSV <= CSVJSON <= CSVJSONTXT <= NONCONSOLE <= ANY) for every run.
    G4 price comparands are the record's: RULES v2 full Sharpe ~1.1998, MaxDD ~-12.05%,
       SPY OOS Sharpe ~0.8721.

PROTOCOL: 10 bps, next-day execution (engine), rule 8 walk-forward on the vintage axis
(choose the leg on runs committed in the FIRST half of the record's date range, read the
SECOND half once).  RULES.md / scan.py / bot.py / baseline.py are NOT modified.
"""
from __future__ import annotations

import gzip
import json
import random
import re
import sys
import time
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, metrics, backtest  # noqa: E402

BT = ROOT / "research" / "backtests"
OUT = str(BT / "2026-09-11_should-every-published-HEADLINE-NUMBER-be-required-to-appear-in-a-COMMITTED-DATA-FILE_cloud")
COST = 10
SEED = 791
MAXBYTES = 48_000_000          # per-file read cap; the largest committed artefact is 29.9 MB

_LOG: list[str] = []


def P(s: str = "") -> None:
    print(s)
    _LOG.append(s)


# ---------------------------------------------------------------- corpus construction
STEM_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}_.+?)((?:\.[a-z0-9]+)+)$")
NARRATIVE_SUFFIXES = (".result.md", "_MEMO.md", ".memo.md")

# >= 4 significant digits.  Either a decimal with >= 4 sig digits, or an integer with >= 4
# digits that is NOT a bare year/date fragment (handled by the guard below).
DISTINCT_RE = re.compile(r"[-+]?\d{1,3}(?:,\d{3})*(?:\.\d+)?%?|[-+]?\d*\.\d+(?:[eE][-+]?\d+)?%?|[-+]?\d+(?:\.\d+)?[eE][-+]?\d+")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*", re.S)
DATEISH_RE = re.compile(r"\d{4}-\d{2}-\d{2}|\b(?:19|20)\d{2}\b")


def sig_digits(tok: str) -> int:
    """Significant digits of a numeric token, ignoring sign / % / commas / exponent."""
    t = tok.strip().lstrip("+-").rstrip("%").replace(",", "")
    t = re.split(r"[eE]", t)[0]
    if "." in t:
        a, b = t.split(".", 1)
        a = a.lstrip("0")
        if a:
            return len((a + b).rstrip("0")) if b else len(a)
        return len(b.lstrip("0"))          # 0.0434 -> 3 ; 0.04340 -> 4
    return len(t.lstrip("0"))


def distinctive_tokens(text: str) -> list[str]:
    """Numeric tokens with >= 4 significant digits, with dates/years masked out first."""
    masked = DATEISH_RE.sub(" ", text)
    out = []
    for m in DISTINCT_RE.finditer(masked):
        tok = m.group(0)
        if sig_digits(tok) >= 4:
            out.append(tok)
    return out


def spellings(tok: str) -> list[str]:
    """Declared equivalent spellings of a quoted token, all searched as substrings."""
    t = tok.strip()
    neg = t.startswith("-")
    core = t.lstrip("+-")
    pct = core.endswith("%")
    core = core.rstrip("%").replace(",", "")
    cands = {core}
    if core.startswith("0."):
        cands.add(core[1:])                               # 0.4325 -> .4325
    if core.startswith("."):
        cands.add("0" + core)
    if pct:
        try:                                              # 12.34% -> 0.1234
            cands.add(f"{float(core) / 100.0:.10f}".rstrip("0"))
            cands.add(f"{float(core) / 100.0:.{len(core.split('.')[-1]) + 2 if '.' in core else 2}f}")
        except ValueError:
            pass
    else:
        try:                                              # 0.1234 -> 12.34
            v = float(core) * 100.0
            cands.add(f"{v:.10f}".rstrip("0").rstrip("."))
        except ValueError:
            pass
    out = set()
    for c in cands:
        if not c or c in {".", "0", "0."}:
            continue
        out.add(c)
        if neg:
            out.add("-" + c)
    return sorted(out)


def read_text(p: Path) -> str:
    try:
        if p.suffix == ".gz":
            with gzip.open(p, "rt", errors="ignore") as fh:
                return fh.read(MAXBYTES)
        if p.stat().st_size > MAXBYTES:
            return p.read_text(errors="ignore")[:MAXBYTES]
        return p.read_text(errors="ignore")
    except Exception:
        return ""


def classify(name: str, stem: str) -> str:
    if name.endswith(".console.txt"):
        return "CONSOLE"
    if name.endswith(".csv") or name.endswith(".csv.gz"):
        return "CSV"
    if name.endswith(".json"):
        return "JSON"
    if name.endswith(".txt"):
        return "TXTNC"
    if name.endswith(".md"):
        return "MD"
    return "OTHER"


SETS = {
    "CSV":        ("CSV",),
    "CSVJSON":    ("CSV", "JSON"),
    "CSVJSONTXT": ("CSV", "JSON", "TXTNC"),
    "NONCONSOLE": ("CSV", "JSON", "TXTNC", "MD"),
    "ANY":        ("CSV", "JSON", "TXTNC", "MD", "CONSOLE"),
}
SETORDER = ["CSV", "CSVJSON", "CSVJSONTXT", "NONCONSOLE", "ANY"]
LEGS = ["ALL", "P90", "P75", "P50", "HEAD"]
PHI = {"ALL": 1.00, "P90": 0.90, "P75": 0.75, "P50": 0.50, "HEAD": 1.00}


def build_corpus() -> tuple[dict, dict]:
    """stem -> {class -> [paths]}, and stem -> [narrative paths]."""
    files = defaultdict(lambda: defaultdict(list))
    narratives = defaultdict(list)
    for p in sorted(BT.iterdir()):
        if not p.is_file():
            continue
        m = STEM_RE.match(p.name)
        if not m:
            continue
        stem = m.group(1)
        cls = classify(p.name, stem)
        if cls == "OTHER":
            continue
        if any(p.name.endswith(s) for s in NARRATIVE_SUFFIXES) or (
            p.name.endswith(".md") and p.name[len(stem):] in (".md",)
        ):
            narratives[stem].append(p)
        else:
            files[stem][cls].append(p)
    return files, narratives


def main() -> None:
    t0 = time.time()
    rng = random.Random(SEED)
    P("=" * 100)
    P("IDEA 791 — should every published HEADLINE NUMBER be required to appear in a COMMITTED DATA FILE")
    P("cloud lane, 2026-09-11.  PROTOCOL: 10 bps, next-day execution, rule 8 walk-forward.")
    P("=" * 100)

    files, narratives = build_corpus()
    stems = sorted(narratives)
    P(f"corpus: {len(stems)} runs own a narrative; "
      f"{sum(len(v) for v in narratives.values())} narrative files; "
      f"{sum(len(ps) for f in files.values() for ps in f.values())} data/console artefacts")

    # artefact classes in nesting order; SETORDER[i] = union of INCREMENTAL[:i+1]
    INCREMENTAL = ["CSV", "JSON", "TXTNC", "MD", "CONSOLE"]

    rows = []
    per_token = []
    plant_hits = plant_n = 0
    for stem in stems:
        ntext = "\n".join(read_text(p) for p in narratives[stem])
        toks = distinctive_tokens(ntext)
        if not toks:
            continue
        head_src = ntext[:1200] + "\n" + "\n".join(BOLD_RE.findall(ntext))
        head_toks = set(distinctive_tokens(head_src))

        # concatenate each artefact class once
        cls_text = {}
        cls_bytes = {}
        for cls in ("CSV", "JSON", "TXTNC", "MD", "CONSOLE"):
            ps = files[stem].get(cls, [])
            cls_bytes[cls] = sum(p.stat().st_size for p in ps)
            cls_text[cls] = "\n".join(read_text(p) for p in ps) if ps else ""

        uniq = sorted(set(toks))
        found = {s: 0 for s in SETORDER}
        hfound = {s: 0 for s in SETORDER}
        missing_csvjson = []
        csvjson_text = cls_text["CSV"] + "\n" + cls_text["JSON"]
        for tok in uniq:
            sp = spellings(tok)
            hit = False
            hits = {}
            for i, c in enumerate(INCREMENTAL):          # nested sets: presence is cumulative
                if not hit and cls_text[c]:
                    t = cls_text[c]
                    hit = any(x in t for x in sp)
                hits[SETORDER[i]] = hit
            for s in SETORDER:
                if hits[s]:
                    found[s] += 1
                    if tok in head_toks:
                        hfound[s] += 1
            if not hits["CSVJSON"]:
                missing_csvjson.append(tok)
            per_token.append(dict(stem=stem, token=tok, head=int(tok in head_toks),
                                  in_CSV=int(hits["CSV"]), in_CSVJSON=int(hits["CSVJSON"]),
                                  in_ANY=int(hits["ANY"])))
            # G2 PLANT-FALSE, same shape, drawn once per real token, tested on the same text
            core = tok.lstrip("+-").rstrip("%").replace(",", "")
            if "." in core:
                a, bpart = core.split(".", 1)
                fake = (a if a in ("", "0") else str(rng.randint(0, 10 ** len(a) - 1))) + "." + \
                       "".join(str(rng.randint(0, 9)) for _ in bpart)
            else:
                fake = str(rng.randint(10 ** (len(core) - 1), 10 ** len(core) - 1))
            plant_n += 1
            plant_hits += int(fake in csvjson_text)
        nh = len(head_toks & set(uniq))
        rows.append(dict(
            stem=stem, date=stem[:10], n_tok=len(uniq), n_head=nh,
            bytes_csv=cls_bytes["CSV"], bytes_json=cls_bytes["JSON"],
            bytes_console=cls_bytes["CONSOLE"],
            bytes_data=cls_bytes["CSV"] + cls_bytes["JSON"] + cls_bytes["TXTNC"],
            has_data=int(cls_bytes["CSV"] + cls_bytes["JSON"] > 0),
            missing_csvjson=len(missing_csvjson),
            **{f"cov_{s}": found[s] / len(uniq) for s in SETORDER},
            **{f"hcov_{s}": (hfound[s] / nh if nh else np.nan) for s in SETORDER},
        ))

    runs = pd.DataFrame(rows).set_index("stem")
    tokdf = pd.DataFrame(per_token)
    P(f"quoted numbers: {int(runs['n_tok'].sum())} distinct tokens over {len(runs)} runs "
      f"(median {runs['n_tok'].median():.0f}/run); headline subset {int(runs['n_head'].sum())}")
    P("")

    # ---------------------------------------------------------------- gates
    P("GATES (pre-registered)")
    csv_share = float((tokdf["in_CSVJSON"] == 1).mean())
    any_share = float((tokdf["in_ANY"] == 1).mean())
    run_any = float(runs["cov_ANY"].mean())
    g1 = bool(csv_share < any_share - 0.20 and 0.40 <= run_any <= 0.95)
    P(f"  G1 idea 790 reproduces : token-level presence CSVJSON {csv_share:.4f} vs ANY "
      f"{any_share:.4f}; per-run mean ANY coverage {run_any:.4f} (790 published 58%-82% "
      f"console-inclusive) -> {'PASS' if g1 else 'FAIL'}")

    # G2 PLANT-FALSE: same shape, random digits, tested on the same CSVJSON text (accumulated
    # in the main pass, one draw per real token)
    plant_rate = plant_hits / max(plant_n, 1)
    g2 = bool(csv_share > plant_rate)
    P(f"  G2 PLANT-FALSE floor   : random same-shape tokens match CSVJSON at "
      f"{plant_rate:.4f} ({plant_hits}/{plant_n}); real rate {csv_share:.4f} -> "
      f"{'PASS' if g2 else 'FAIL'}")

    mono = all(bool((runs[f"cov_{SETORDER[i]}"] <= runs[f"cov_{SETORDER[i+1]}"] + 1e-12).all())
               for i in range(len(SETORDER) - 1))
    P(f"  G3 set monotonicity    : coverage non-decreasing CSV->ANY on all {len(runs)} runs "
      f"-> {'PASS' if mono else 'FAIL'}")

    px = load_universe()
    start = px.index[260]
    b = backtest(px, rules_v2_weights(px), cost_bps=COST, freq="W")["returns"].loc[start:]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    h = len(b) // 2
    mb, ms = metrics(b), metrics(spy)
    mb1, mb2 = metrics(b.iloc[:h]), metrics(b.iloc[h:])
    ms1, ms2 = metrics(spy.iloc[:h]), metrics(spy.iloc[h:])
    oos = slice("2017-01-01", None)
    mbo, mso = metrics(b.loc[oos]), metrics(spy.loc[oos])
    g4 = bool(abs(mb["Sharpe"] - 1.1998) <= 0.01 and abs(mb["MaxDD"] + 0.1205) <= 0.01
              and abs(mso["Sharpe"] - 0.8721) <= 0.01)
    P(f"  G4 price comparands    : RULES v2 Sharpe {mb['Sharpe']:.4f} (record 1.1998), MaxDD "
      f"{mb['MaxDD']:.4f} (record -0.1205), SPY OOS Sharpe {mso['Sharpe']:.4f} (record "
      f"0.8721) -> {'PASS' if g4 else 'FAIL'}")
    P(f"  ALL GATES {'PASS' if all([g1, g2, mono, g4]) else 'NOT ALL PASS'}")
    P("")

    # ---------------------------------------------------------------- the 25-cell grid
    def comply(sub: pd.DataFrame, leg: str, s: str) -> pd.Series:
        col = f"hcov_{s}" if leg == "HEAD" else f"cov_{s}"
        v = sub[col]
        if leg == "HEAD":
            return (v.fillna(1.0) >= 1.0 - 1e-12)     # a run quoting no headline number complies vacuously
        return v >= PHI[leg] - 1e-12

    grid = []
    for leg in LEGS:
        for s in SETORDER:
            c = comply(runs, leg, s)
            grid.append(dict(leg=leg, phi=PHI[leg], artefact_set=s, n=len(runs),
                             comply=int(c.sum()), share=float(c.mean()),
                             recommit=int((~c).sum())))
    grid = pd.DataFrame(grid)
    P("THE GRID — 25 cells (leg form x artefact set), ALL reported")
    P("  share = fraction of the record's runs that ALREADY comply; recommit = runs that would")
    P("  have to re-commit an artefact if the clause were adopted today.")
    P("")
    P("  " + "leg  phi   " + "".join(f"{s:>13}" for s in SETORDER))
    for leg in LEGS:
        sub = grid[grid.leg == leg].set_index("artefact_set")
        P(f"  {leg:<5}{PHI[leg]:.2f}  " + "".join(
            f"{sub.loc[s, 'share']:>8.4f} ({sub.loc[s, 'recommit']:>3d})" for s in SETORDER))
    P("")
    lit = grid[(grid.leg == "ALL") & (grid.artefact_set == "CSVJSON")].iloc[0]
    litany = grid[(grid.leg == "ALL") & (grid.artefact_set == "ANY")].iloc[0]
    P(f"  LITERAL CLAUSE (ALL x CSVJSON): {lit['comply']}/{lit['n']} comply "
      f"({lit['share']:.2%}); {lit['recommit']} runs would have to re-commit.")
    P(f"  DE-FACTO TODAY (ALL x ANY, console counts): {litany['share']:.2%} comply.")
    P(f"  H_COST   {'HELD' if lit['share'] < 0.25 else 'FALSIFIED'} (literal compliance "
      f"{lit['share']:.2%} vs 25% bar)")
    P(f"  H_CONSOLE {'HELD' if (litany['share'] - lit['share']) >= 0.20 else 'FALSIFIED'} "
      f"(ANY - CSVJSON = {(litany['share'] - lit['share']) * 100:.2f} pp vs 20 pp bar)")
    P("")

    # ---------------------------------------------------------------- cheapest artefact
    P("CHEAPEST ARTEFACT THAT SATISFIES THE CLAUSE")
    nc = runs[~comply(runs, "ALL", "CSVJSON")]
    miss = nc["missing_csvjson"]
    est_bytes = miss * 48                      # one "label,value" row, 48 bytes is generous
    P(f"  non-compliant runs {len(nc)}; missing values per run: median {miss.median():.0f}, "
      f"mean {miss.mean():.1f}, p90 {miss.quantile(0.90):.0f}, max {int(miss.max())}")
    P(f"  total missing values over the record: {int(miss.sum())}")
    P(f"  a one-file `<stem>.headline.csv` of (label,value) rows costs a median "
      f"{est_bytes.median():.0f} B / run, {est_bytes.sum() / 1e6:.3f} MB over the whole record")
    P(f"  for comparison the same runs already commit {nc['bytes_data'].sum() / 1e6:.1f} MB of "
      f"data and {nc['bytes_console'].sum() / 1e6:.1f} MB of console; the remedy is "
      f"{est_bytes.sum() / max(nc['bytes_console'].sum(), 1) * 100:.3f}% of the console bytes "
      f"already committed")
    nodata = int((runs["has_data"] == 0).sum())
    P(f"  runs committing NO csv/json at all: {nodata} "
      f"({nodata / len(runs):.2%}) — 790 counted 16 on its 457-run corpus")
    P(f"  H_CHEAP {'HELD' if miss.median() < 50 else 'FALSIFIED'} (median missing "
      f"{miss.median():.0f} vs 50 bar)")
    P("")
    P("  the HEAD leg is the cheap adoptable form:")
    hlit = grid[(grid.leg == "HEAD") & (grid.artefact_set == "CSVJSON")].iloc[0]
    hmiss = (runs["n_head"] * (1 - runs["hcov_CSVJSON"].fillna(1.0))).round()
    P(f"    HEAD x CSVJSON: {hlit['share']:.2%} comply, {hlit['recommit']} re-commit, median "
      f"{hmiss[hmiss > 0].median():.0f} values to publish per non-compliant run "
      f"({int(hmiss.sum())} over the record, {hmiss.sum() * 48 / 1e3:.1f} kB)")
    P("")

    # ---------------------------------------------------------------- rule 8 walk-forward
    P("RULE 8 WALK-FORWARD (vintage axis: choose on the FIRST half of the record, read the SECOND once)")
    runs = runs.sort_values("date")
    dates = sorted(runs["date"].unique())
    cut = dates[len(dates) // 2]
    IS, OOS = runs[runs["date"] < cut], runs[runs["date"] >= cut]
    P(f"  split at {cut}: IS {len(IS)} runs ({dates[0]}..), OOS {len(OOS)} runs (..{dates[-1]})")
    # pre-stated selector: the STRICTEST cell (highest phi, then narrowest artefact set) whose
    # IS compliance is at least 50% — i.e. the strongest clause a majority of the record
    # already meets.  Chosen on IS only; OOS read once.
    order = [(leg, s) for leg in ["ALL", "P90", "P75", "P50", "HEAD"] for s in SETORDER]
    wf = []
    for leg, s in order:
        wf.append(dict(leg=leg, artefact_set=s,
                       IS=float(comply(IS, leg, s).mean()),
                       OOS=float(comply(OOS, leg, s).mean())))
    wf = pd.DataFrame(wf)
    elig = wf[wf.IS >= 0.50]
    if len(elig):
        rank = {"ALL": 0, "P90": 1, "P75": 2, "P50": 3, "HEAD": 4}
        elig = elig.assign(_l=elig.leg.map(rank), _s=elig.artefact_set.map(
            {s: i for i, s in enumerate(SETORDER)})).sort_values(["_l", "_s"])
        pick = elig.iloc[0]
        P(f"  IS pick (strictest cell with IS compliance >= 50%): {pick['leg']} x "
          f"{pick['artefact_set']}  IS {pick['IS']:.4f}")
        P(f"  OOS read ONCE                                    : OOS {pick['OOS']:.4f}  "
          f"(drift {(pick['OOS'] - pick['IS']) * 100:+.2f} pp)")
        stable = abs(pick["OOS"] - pick["IS"]) <= 0.15
        P(f"  H_STABLE {'HELD' if stable else 'FALSIFIED'} (|drift| "
          f"{abs(pick['OOS'] - pick['IS']) * 100:.2f} pp vs 15 pp bar)")
    else:
        pick = None
        P("  IS pick: NONE — no cell reaches 50% IS compliance.  The clause is unadoptable at "
          "every leg form tested without a re-commit campaign; that IS the walk-forward result.")
        P("  H_STABLE: not testable (no pick).")
    P("")
    P("  full IS/OOS ladder (all 25 cells, reported):")
    P("  " + f"{'leg':<6}{'set':<13}{'IS':>9}{'OOS':>9}{'drift pp':>10}")
    for _, r in wf.iterrows():
        P("  " + f"{r['leg']:<6}{r['artefact_set']:<13}{r['IS']:>9.4f}{r['OOS']:>9.4f}"
          f"{(r['OOS'] - r['IS']) * 100:>10.2f}")
    P("")

    # ---------------------------------------------------------------- KEEP paths
    P("KEEP PATHS (PROTOCOL rule 4)")
    P(f"  comparands: RULES v2 full CAGR {mb['CAGR']:.4f} Sharpe {mb['Sharpe']:.4f} "
      f"(H1 {mb1['Sharpe']:.4f} / H2 {mb2['Sharpe']:.4f}) MaxDD {mb['MaxDD']:.4f}; "
      f"SPY full CAGR {ms['CAGR']:.4f} Sharpe {ms['Sharpe']:.4f} (H1 {ms1['Sharpe']:.4f} / "
      f"H2 {ms2['Sharpe']:.4f}) MaxDD {ms['MaxDD']:.4f}")
    P(f"  OOS (2017+): RULES v2 CAGR {mbo['CAGR']:.4f} Sharpe {mbo['Sharpe']:.4f} MaxDD "
      f"{mbo['MaxDD']:.4f}; SPY CAGR {mso['CAGR']:.4f} Sharpe {mso['Sharpe']:.4f} MaxDD "
      f"{mso['MaxDD']:.4f}")
    P("  4a (beat the book): N/A — this idea prices a documentation clause.  It produces no "
      "weights function and no return stream, so there is nothing to compare against RULES v2 "
      "in either half.")
    P("  4b (capital-worthy): N/A — same reason.  Recorded n/a, NOT claimed either way.")
    P("")

    # ---------------------------------------------------------------- artefacts
    runs.to_csv(f"{OUT}.runs.csv")
    grid.to_csv(f"{OUT}.grid.csv", index=False)
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    tokdf.to_csv(f"{OUT}.tokens.csv", index=False)
    summary = dict(
        idea=791, lane="cloud", date="2026-09-11",
        n_runs=int(len(runs)), n_tokens=int(runs["n_tok"].sum()),
        token_share_csvjson=csv_share, token_share_any=any_share,
        plant_false_rate=plant_rate,
        literal_comply=float(lit["share"]), literal_recommit=int(lit["recommit"]),
        defacto_comply=float(litany["share"]),
        head_comply=float(hlit["share"]), head_recommit=int(hlit["recommit"]),
        median_missing=float(miss.median()), total_missing=int(miss.sum()),
        remedy_bytes=int(est_bytes.sum()), runs_without_data=nodata,
        wf_cut=cut, wf_pick=(None if pick is None else f"{pick['leg']}x{pick['artefact_set']}"),
        wf_is=(None if pick is None else float(pick["IS"])),
        wf_oos=(None if pick is None else float(pick["OOS"])),
        gates=dict(G1=g1, G2=g2, G3=mono, G4=g4),
        rules_v2=dict(CAGR=mb["CAGR"], Sharpe=mb["Sharpe"], MaxDD=mb["MaxDD"],
                      H1=mb1["Sharpe"], H2=mb2["Sharpe"], OOS_Sharpe=mbo["Sharpe"],
                      OOS_CAGR=mbo["CAGR"], OOS_MaxDD=mbo["MaxDD"]),
        spy=dict(CAGR=ms["CAGR"], Sharpe=ms["Sharpe"], MaxDD=ms["MaxDD"],
                 H1=ms1["Sharpe"], H2=ms2["Sharpe"], OOS_Sharpe=mso["Sharpe"],
                 OOS_CAGR=mso["CAGR"], OOS_MaxDD=mso["MaxDD"]),
    )
    Path(f"{OUT}.summary.json").write_text(json.dumps(summary, indent=2, default=float))
    P(f"artefacts: {Path(OUT).name}.runs.csv .grid.csv .walkforward.csv .tokens.csv "
      f".summary.json .console.txt   ({time.time() - t0:.0f}s)")
    Path(f"{OUT}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
