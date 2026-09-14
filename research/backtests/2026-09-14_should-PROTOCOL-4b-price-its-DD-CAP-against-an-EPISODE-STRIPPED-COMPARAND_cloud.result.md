# Idea 861 — should PROTOCOL 4b price its DD CAP against an EPISODE-STRIPPED COMPARAND?

**2026-09-14, cloud lane, idea 1 of 2.**
Script `2026-09-14_should-PROTOCOL-4b-price-its-DD-CAP-against-an-EPISODE-STRIPPED-COMPARAND_cloud.py`
(9.1 s, deterministic, seed 861, no network).
Outputs: `.console.txt`, `.margins.csv` (792 rows), `.clause.csv` (264 rows), `.shuffle.csv`, `.walkforward.csv`.

## VERDICT: **YES — ADOPT as a reporting/verdict leg. But it is a ONE-EPISODE clause, and it buys ZERO alpha.**

The clause is cheap, well-calibrated and removes a real defect in how the record publishes 4b.
It is **not** a selection edge: at the rule-8 pick it changes nothing, on either panel, at every
episode set. Adopt it for honesty, not for return.

## GATES — 5 of 5 PASS (printed before any new number)
- **G1** empty splice == unspliced, max|d| `0.000e+00`.
- **G2** 8 of 8 committed 4b memos rebuild inside tolerance (max dSharpe 0.0202, max dMaxDD 0.0109).
  `b136-corr-hi-q017-w252-d050-D-g100` — **idea 814's own book, the one the queue's question is
  about** — still does not rebuild from its memo's wording, so its +5.12 pp → −0.41 pp margin is
  quoted from 814's committed file and is **not** re-derived here. Named, not silently re-specified.
- **G3** SPY reproduces the committed comparand 15.1631% / 0.8861 / −33.7172%, max|d| 4.56e−05.
- **G4** **851 replication**: SPY MaxDD ex-COVID_TIGHT −24.4964% (851: −24.50%), re-priced cap
  −14.6978% (851: −14.70%). The two runs are on the same numbers.
- **G5** the clause is a conjunction on 264 of 264 rows.

## PART A — THE MARGIN CENSUS (new: the record publishes PASS/FAIL, never the margin)
Unstripped, 10 bps, cap −20.23%:

| set | 4b passes | median DD margin | min | max | clearing by < 1.00 pp |
|---|---|---|---|---|---|
| SHELF | 8 of 8 | **+1.75 pp** | +0.48 | +5.44 | **2 of 8** |
| GRID | 19 of 36 | +4.09 pp | +0.73 | +5.44 | 1 of 19 |

**H_MARGIN FAILS** (predicted median > 2.00 pp; got **+1.75 pp**). The shelf — the books a Sunday
review would actually pick from — sits *closer* to the cap than the mechanical grid does. The
tightest committed 4b pass on the record, `u56-quantile50-respread-M`, clears the drawdown cap by
**48 basis points**.

## PART B — THE CLAUSE
**4b-DD-STRIP:** *the DD leg must clear at every single-episode strip in the declared set, with the
cap re-priced (60% of SPY) on that same stripped leg.* Statistic `MINMARGIN = min over strips`.

| book set | rung | base 4b | QUEUE2 keeps | REAL5 keeps | PLACEBO3 keeps |
|---|---|---|---|---|---|
| SHELF | 10 bps | 8 | **5** (kills 3) | 5 (kills 3) | **8 (kills 0)** |
| SHELF | 25 bps | 7 | 4 (kills 3) | 4 (kills 3) | 7 (kills 0) |
| GRID | 10 bps | 19 | **6** (kills 13) | 6 (kills 13) | **19 (kills 0)** |
| GRID | 25 bps | 14 | 3 (kills 11) | 3 (kills 11) | 14 (kills 0) |

SHELF book by book, QUEUE2, 10 bps (margins in pp):

| book | base margin | MINMARGIN | binds at | clause |
|---|---|---|---|---|
| b136-qroll-q012-w1008-d050-g100 | +2.92 | **−0.37** | COVID_TIGHT | DROP |
| u56-k8-qroll-q017-w1008-d100-g100 | +5.44 | **−0.09** | COVID_TIGHT | DROP |
| u56-marsrespread-gross075 | +1.58 | **−0.06** | COVID_TIGHT | DROP |
| b136-r620-gross065-W | +0.80 | +0.28 | COVID_TIGHT | KEEP |
| u56-quantile50-respread-M | +0.48 | +0.37 | COVID_TIGHT | KEEP |
| u56-band008-gross100 | +1.18 | +1.18 | BEAR2022 | KEEP |
| u56-top20-band-m20 | +1.92 | +1.69 | COVID_TIGHT | KEEP |
| u56-v2band-gross100 | +4.32 | +4.25 | COVID_TIGHT | KEEP |

- **H_CLAUSE PASS** (3 of 8 ≥ ⅓).
- **H_PLACEBO PASS** (placebo kills 0 vs real kills 3).
- Note the **rank inversion**: the three books the clause drops are the three with the *largest*
  unstripped margins among the QROLL/respread family (+2.92, +5.44, +1.58), while the tightest
  book on the record (+0.48) survives. The unstripped margin does not predict the stripped one,
  which is exactly the defect the clause is for.

### The clause is a ONE-EPISODE clause
**COVID_TIGHT binds 16 of 16 kills** (SHELF 3 of 3, GRID 13 of 13). BEAR2022 — the queue's second
episode — kills **nothing**, on either book set, at either rung. REAL5 (five real episodes) gives
exactly the same counts as QUEUE2 (two). Adding episodes buys no discrimination: the entire clause
is "delete 2020-02-19..2020-04-07".

## PART B2 — THE CLAUSE'S FALSE-REJECTION RATE
20 random 35-day strips, seed 861. **0 kills on 20 of 20 draws**, SPY MaxDD unchanged at −33.72% on
every one. **H_SHUFFLE PASS (3 vs p90 0.0)** — but the null is **inert by construction, and that is
the finding**: SPY's binding MaxDD runs 2020-02-19 → 2020-03-23, so the cap can only move when a
strip intersects those 24 days, and 0 of 20 draws did. Combined false-rejection evidence: **0 kills
across 23 non-intersecting strips** (3 placebo + 20 shuffle). The clause never fires spuriously; it
also never fires for any reason other than 2020.

## PART C — RULE 8, the clause as a SELECTOR (dial chosen on 2009–2016 alone, OOS 2017–2026 read once)
Screened pool = GRID books whose DD leg clears at every strip, everything computed on the IS window.

| panel | chooser | elig/pool | pick | OOS CAGR / Sharpe / MaxDD | RULES v2 OOS | SPY OOS | 4b | 4a |
|---|---|---|---|---|---|---|---|---|
| U56 | UNSCREENED | 18/18 | U56-band0.08-g1.00 | **12.04% / 1.1654 / −19.05%** | 9.47% / 1.2782 / −12.05% | 15.33% / 0.8767 / −33.72% | PASS | FAIL |
| U56 | SCREENED | 6/18 | U56-band0.08-g1.00 | **12.04% / 1.1654 / −19.05%** | same | same | PASS | FAIL |
| B136 | UNSCREENED | 18/18 | B136-band0.08-g1.00 | **11.05% / 1.0974 / −19.50%** | 7.88% / 1.1059 / −12.24% | same | PASS | FAIL |
| B136 | SCREENED | 7/18 | B136-band0.08-g1.00 | **11.05% / 1.0974 / −19.50%** | same | same | PASS | FAIL |

Full sample, 10 bps: U56-band0.08-g1.00 11.39% / 1.1461 / −19.05% (H1 1.244 / H2 1.066);
B136-band0.08-g1.00 11.39% / 1.1179 / −19.50% (H1 1.278 / H2 0.964). Both are 4b PASS, 4a FAIL.

**SCREENED − UNSCREENED OOS Sharpe = +0.0000 in all 6 (panel × episode set) cells. H_R8 PASS
(0 of 6 improved).** The screen throws away two thirds of the pool and the IS-Sharpe argmax was
already inside the survivors, on both panels, at every episode set. The clause is **free** — and
worth exactly what it costs.

Both picks also satisfy the clause **out of sample** (MINMARGIN +1.18 pp U56, +0.73 pp B136).

## PROPOSED PROTOCOL LINE (not applied — rule 6, Sunday review only)
> **4b DD leg, addendum.** Publish the DD-leg **margin in pp** beside every 4b verdict, and a
> second **MINMARGIN** figure: the smallest (book MaxDD − 0.60 × SPY MaxDD) over a declared strip
> set, each leg spliced from **both** sides. Today's declared set is `{2020-02-19..2020-04-07}` —
> the only strip on this corpus that moves the cap at all. A 4b pass whose MINMARGIN is negative
> is reported as **"passes on the unstripped comparand only"**, not as a plain 4b pass.

Costs nothing at the pick (Part C), fires on 3 of 8 committed candidates, and has a 0-of-23
false-rejection rate. Cheap honesty, not edge.

## CAVEATS
- **SURVIVORSHIP**: U56 and B136 are current-constituent lists. Every CAGR and drawdown **level**
  is optimistic; the strip-to-strip **difference** is the durable part.
- Idea 814's `b136-corr-hi` book is the one candidate the clause was motivated by and the one this
  run cannot rebuild. Its numbers here are quoted, not verified.
- The whole clause rests on one 35-day window. On a corpus with a second crash of comparable depth
  it would need re-calibrating; on this one, "episode-stripped comparand" means "ex-COVID".
- Nothing promoted; RULES.md, scan.py, bot.py and baseline.py untouched.
