# Idea 952 (lane C, 2026-09-15) — can the binding leg of the 710,313 SILENT 4b FAIL rows be recovered?

**ANSWERED = PARTLY. KILL for recovering the leg from a row's STATISTICS. KEEP the finding that
944's "85.0% silent" is 13.3 pp CENSUS ARTEFACT and that its published leg shares rest on a
non-representative 15% sample.**

Script: `2026-09-15_can-the-BINDING-LEG-of-the-710313-SILENT-4b-FAIL-rows-be-recovered-from-their-own-SCRIPTS_C.py`
Population: 837,860 committed 4b FAIL rows in 692 CSVs (944 committed 835,403; the +2,457 drift is
files committed after 944 ran, printed and not absorbed). **GATES 6 of 6 PASS.**

## The ladder (TUNED 1 — 5 nested rungs, every rung reported)

| rung | what it reads | rows naming a binding leg | files |
|---|---|---|---|
| R0_ASBUILT | 944's rule: a column *named* `fail4b`, or 2 exact leg-boolean sets | 127,261 — **15.2%** | 185 |
| R1_ALPHABET | any OTHER validated fail-string column (`failing`, `f4b`, `fail_4b`, `OOS_fails`, …) | 177,061 — **21.1%** | 286 |
| R2_LEGCOLS | per-leg boolean / margin families (`leg_*`, `m_H1..m_CAGR`, `L1_H1..`) | 238,811 — **28.5%** | 312 |
| R3_STATS_INFILE | the five legs rebuilt from row statistics vs the file's own SPY comparand | 282,508 — 33.7% | 435 |
| R4_STATS_PANEL | same, vs SPY recomputed here on the file's panel | 567,526 — 67.7% | 595 |

**R0 → R2 is free.** 111,550 of the rows 944 booked UNRECOVERABLE (**15.7%**) already carry their
binding leg, in a column the census did not read. No modelling, no assumption, nothing to distrust:
the record's real silence is **71.5%** of committed 4b FAIL rows, not 85.0%. Of the 81 rejected
candidate columns, every rejection is on its own values (G3), e.g. `leg_sharpe` parses 0.00.

**R3/R4 do not survive their own check.** Where a row is covered by BOTH text and statistics
(262,392 rows), the rebuild agrees with the committed legs on 87.1% (panel comparand) and only
48.3% (the file's OWN committed SPY comparand). Under idea 161's stricter per-file gate — the
rebuild must match on *every* doubly-covered row — **42 of 296 checkable files (14.2%) reconstruct
exactly**. A second convention was tested and does not rescue it: reading the DD cap and CAGR floor
on the OOS window instead of the full sample explains 55.0% (panel) / 14.3% (in-file), and
*either* convention lifts the panel rate from 87.1% only to 87.2%. The window a committed row was
scored on is simply not in the row. **H_FIDELITY FAIL.**

Fidelity-gated, the honest recovery of the whole record is **28.5% .. 67.7%** (VERIFIED 42 files /
12,335 rows, REFUTED 254 / 220,874, UNCHECKABLE 388 / 604,651). The bottom of that range is the
text rungs; the top requires trusting a rebuild that fails on 86% of the files where it can be
checked. This run stands behind the bottom.

## The payload: the readable 15% is not a fair sample (H_BIAS **FAIL**)

On the rows the record already named in another column — the trustworthy recoveries, R1–R2 only:

| leg | DD/CAGR-ALONE share, R0-readable | same, newly recovered | move |
|---|---|---|---|
| L4_DD | 16.0% | **30.7%** | **+14.7 pp** |
| L5_CAGR | 18.2% | **25.1%** | **+6.9 pp** |

944 published "the record's modal binder is the CAGR floor (68.8%), the DD cap 58.3%" from the R0
column alone. Those shares are computed on a sample that under-represents single-leg failures by
double digits. The direction of 944's headline is not overturned here — this run does not re-rank
the legs, it prices the sampling error in the claim (the 'any' shares fall 6–24 pp across all five
legs on the recovered rows, i.e. the readable rows skew heavily toward all-five-legs signatures).

## The other bars

- **H_RECOVER PASS** (pre-registered, ungated): 440,265 of 710,599 = 62.0%. Gated: 15.7%..62.0%.
- **H_CLAIMSET FAIL**: row-weighted 67.7% vs file-weighted 80.6% = 12.8 pp apart (bar 10 pp). A
  row-weighted census of this record is carried by a handful of very large grid dumps; both are
  reported, never merged.
- **H_WFRULE PASS**: an alphabet learned only on files dated ≤ 2026-09-08 recovers 92.0% against
  the full vocabulary's 95.0% on later files (ratio 0.968). The recovery rule is not fitted to the
  residue it was built on.

## Pricing the clause

Clause: *every committed row carrying a 4b verdict also carries a `fail4b` string.*
Cost ≈ 1 column, ~10.1 MB over the record = **0.83% of its committed CSV bytes**. It buys the
270,334 rows (32.3%) no post-hoc rule reaches at all, and — the larger part — it removes the
window ambiguity that makes 86% of checkable files un-rebuildable. It is **not** proposed as a
PROTOCOL edit here (rule 6: Sunday review only); proposed wording for that review:
*"10. Any committed row carrying a 4b pass/fail verdict MUST carry a `fail4b` column holding the
canonical `L1_H1+L2_H2+L3_OOS+L4_DD+L5_CAGR` binding signature, `-` when it passes."*

## PROTOCOL rule 8 (required; `.walkforward.csv`, 20 grid points, every row names its leg)

Book chosen on 2009–2016 ALONE by IS Sharpe, 2017–2026 read ONCE, 4 cost rungs reported.

| | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR / Sharpe / MaxDD | 4a | 4b |
|---|---|---|---|---|---|---|---|
| IS pick @10 bps (TOP5) | 18.59% | 1.008 | −27.24% | 1.257 / 0.813 | 15.56% / 0.824 / −27.24% | ✗ | ✗ (L2_H2+L3_OOS+L4_DD) |
| canonical TOP20 @10 bps | 14.69% | 1.202 | −19.51% | 1.216 / 1.198 | 16.67% / 1.282 / −19.51% | ✗ | ✓ |
| RULES v2 (live) @10 bps | 8.88% | 1.172 | −14.38% | 1.217 / 1.135 | 9.56% / 1.224 / −14.38% | — | — |
| SPY | 15.13% | 0.885 | −33.72% | 0.959 / 0.824 | 15.27% / 0.874 / −33.72% | — | — |

**4a: 0 of 20** grid points (no book beats RULES v2's −14.38% MaxDD). **4b: 8 of 20** — TOP20 and
TOP30 at all four rungs, i.e. the standing candidate, re-derived, not a new one. The IS chooser
lands on TOP5 and loses to the canonical book by 0.458 of OOS Sharpe: the free parameter is again
worth less than its default. **Nothing is promoted; RULES.md / PROTOCOL.md / scan.py / bot.py /
baseline.py untouched.**

## Limits

A census of the record's TEXT and of statistics the record committed. It inherits the biases of the
runs it reads, it is not a sample from a population, and no p-value is claimed for any share. The
R4 comparand assumes PROTOCOL's windows; how often that assumption is wrong is exactly what the
fidelity rate measures, and it is why the statistics rungs are rejected rather than published.
