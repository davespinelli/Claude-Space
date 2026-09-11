# Idea 791 — should every published HEADLINE NUMBER be required to appear in a COMMITTED DATA FILE?

**cloud lane, 2026-09-11.** Script: `2026-09-11_should-every-published-HEADLINE-NUMBER-be-required-to-appear-in-a-COMMITTED-DATA-FILE_cloud.py`.
PROTOCOL: 10 bps, next-day execution, rule 8 walk-forward on the vintage axis. RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py untouched.

## Verdict — ANSWERED. The clause is worth adopting, but only in its HEAD form, and it is cheap.

The literal clause idea 790's diagnosis implies ("every number a narrative quotes must be
reproducible from a committed csv/json row") is **priced at 617 of 684 runs re-committing
(90.2% of the record)**. The restricted clause that a protocol would plausibly adopt —
headline numbers only — is priced at **503 runs and 102.8 kB of new artefact over the whole
record**, i.e. **0.5% of the console bytes the record already commits**. The cost objection
to the clause does not survive measurement; the *scope* objection does.

## Corpus and gates

691 runs own a narrative; 684 of them quote at least one distinctive number. **23,486 distinct
quoted tokens** (>= 4 significant digits, idea 790's bar kept verbatim), median 28 per run;
**6,162** of them are HEADLINE numbers (title block or a `**bold**` span). 4,474 data/console
artefacts, 544.3 MB of data and 20.2 MB of console.

| Gate | Reading | |
|---|---|---|
| G1 idea 790 reproduces | token presence CSVJSON **0.6964** vs ANY **0.9488**; per-run mean ANY coverage **0.9182** | PASS |
| G2 PLANT-FALSE floor | random same-shape tokens match CSVJSON at **0.2562** (6,018/23,486) vs real 0.6964 | PASS |
| G3 set monotonicity | coverage non-decreasing CSV→ANY on all 684 runs | PASS |
| G4 price comparands | RULES v2 Sharpe **1.1998** (record 1.1998), MaxDD **−12.05%** (record −12.05%), SPY OOS Sharpe **0.8721** (record 0.8721) | PASS |

**G2 is the caveat that governs every token-level number here.** A quarter of same-shape
random tokens already occur somewhere in a run's own csv/json by chance, so the 0.6964
token-level presence is worth 0.5918 after chance correction — and, in the direction that
matters, chance matching makes *compliance look better than it is*. Every compliance share
below is an **upper bound**.

## The grid — 25 cells (leg form × artefact set), all reported

`share` = runs already complying; `(n)` = runs that would have to re-commit.

| leg | φ | CSV | CSVJSON | CSVJSONTXT | NONCONSOLE | ANY |
|---|---|---|---|---|---|---|
| ALL | 1.00 | 0.0980 (617) | **0.0980 (617)** | 0.1111 (608) | 0.1111 (608) | 0.6038 (271) |
| P90 | 0.90 | 0.2251 (530) | 0.2251 (530) | 0.2412 (519) | 0.2412 (519) | 0.8611 (95) |
| P75 | 0.75 | 0.4576 (371) | 0.4591 (370) | 0.4708 (362) | 0.4708 (362) | 0.9298 (48) |
| P50 | 0.50 | 0.7836 (148) | 0.7851 (147) | 0.7924 (142) | 0.7924 (142) | 0.9444 (38) |
| HEAD | 1.00 | 0.2646 (503) | **0.2646 (503)** | 0.2763 (495) | 0.2763 (495) | 0.7939 (141) |

Three readings of the table:

1. **The console is the record.** ALL × ANY 60.38% against ALL × CSVJSON 9.80% — a **50.58 pp**
   gap that is entirely the run's own printout. H_CONSOLE HELD.
2. **JSON and TXT buy nothing.** CSV → CSVJSON moves compliance by 0.15 pp at P75 and 0.00 pp
   at ALL (only 11 committed .json files exist); CSVJSON → CSVJSONTXT moves it 1.2 pp. The
   artefact-set dial is a two-point dial in practice: **csv, or the console**.
3. **The clause is expensive at φ = 1.00 and nearly free at φ = 0.50.** P50 × CSVJSON already
   holds for 78.51% of the record. H_COST HELD (9.80% < 25% bar).

## The cheapest artefact that satisfies it

Over the 617 non-compliant runs under the literal clause:

* missing values per run: **median 9**, mean 11.6, p90 24, max 150; **7,131 total**.
* a one-file `<stem>.headline.csv` of `(label,value)` rows costs a **median 432 B/run** and
  **0.342 MB over the whole record** — **1.693%** of the 20.2 MB of console those same runs
  already commit. H_CHEAP HELD (median 9 < 50 bar).
* under the HEAD leg the bill falls to **2,142 values, 102.8 kB, median 3 per run**.
* **56 runs (8.19%) commit no csv/json at all** — idea 790 counted 16 on its 457-run corpus;
  on the full 684-run corpus the rate is 8.19%, not 3.5%.

So the honest framing is not "the clause is unaffordable". It is: **the clause costs one extra
csv with a median of three rows, and the record has simply never been asked for it.**

## Rule 8 walk-forward (vintage axis)

Split at the record's date median, **2026-09-07**: IS 238 runs (2026-09-03 →), OOS 446 runs
(→ 2026-09-11). Pre-stated selector: *the strictest cell (highest φ, then narrowest artefact
set) whose IS compliance is ≥ 50%*. OOS read once.

* **IS pick: ALL × ANY, IS 0.6639 → OOS 0.5717, drift −9.21 pp.** H_STABLE HELD (< 15 pp bar).
* **No csv/json cell reaches 50% IS at φ ≥ 0.75.** The selector is forced onto the console leg —
  which is exactly the practice the clause exists to end. The walk-forward's real content is
  that *the record's compliance with its own data cannot carry a 50% bar at any strict leg*.
* Drift is negative at every ALL, P90 and HEAD cell (−6.2 to −10.5 pp) and positive at every
  P50 cell (+1.8 to +7.6 pp): **later runs commit more data but quote more numbers**, so the
  loose legs improve with vintage and the strict legs decay.

Full 25-cell IS/OOS ladder: `.walkforward.csv`.

## KEEP paths

| | |
|---|---|
| RULES v2 (live) | full CAGR 8.61% / Sharpe 1.1998 (H1 1.2349 / H2 1.1718) / MaxDD −12.05%; OOS CAGR 9.45% / Sharpe 1.2747 / MaxDD −12.05% |
| SPY | full CAGR 15.11% / Sharpe 0.8835 (H1 0.9595 / H2 0.8211) / MaxDD −33.72%; OOS CAGR 15.24% / Sharpe 0.8721 / MaxDD −33.72% |
| **4a** | **N/A** — this idea prices a documentation clause. No weights function, no return stream, nothing to compare against RULES v2 in either half. |
| **4b** | **N/A** — same reason. Recorded n/a, **not** claimed either way. |

## Recommendation (for the Sunday review; no RULES change is made here)

Adopt the **HEAD form**, not the literal form: *"every number a narrative quotes in its title
block or in a bold span must appear in a committed csv/json row of the same run."* It is the
only form whose price is measured and small (503 runs, 102.8 kB, median 3 values), and it is
the form whose failure mode idea 790 actually found. Do **not** adopt φ = 1.00 over all quoted
numbers: 617 of 684 runs fail it, and G2 says even that 9.80% is an upper bound.

Two caveats that must travel with any adoption: the PLANT-FALSE floor of 0.2562 means verbatim
presence over-reports (idea 792's size effect applies — big artefacts match by chance more
often), and the compliance census is a **substring** test, so a number present in a csv under a
different rounding than the narrative quotes it counts as missing.

## Artefacts

`.runs.csv` (684 runs × coverage on all five sets), `.grid.csv` (25 cells), `.walkforward.csv`
(25 IS/OOS rows), `.tokens.csv` (23,486 token rows), `.summary.json`, `.console.txt`.
