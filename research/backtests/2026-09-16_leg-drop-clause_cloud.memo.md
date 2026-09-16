# MEMO — PROTOCOL rule 4 LEG-DROP clause (PROPOSED, NOT APPLIED — rule 6)

Source: idea 1018 (cloud lane, 2026-09-16),
`2026-09-16_is-L3_OOS-the-leg-4b-could-ACTUALLY-DROP_cloud.py`. This is a REPORTING clause. It
changes no bar, promotes no book, and does not touch `RULES.md`, `PROTOCOL.md`, `scan.py`,
`bot.py` or `baseline.py`.

## Exact RULES wording (to be added to PROTOCOL.md rule 4 at a Sunday review, not before)

> **4c (leg drop, added 2026-09-16).** No leg is removed from the 4b conjunction on a
> SOLE-BINDER rate alone. A proposed drop is published with, at every cost rung the record
> carries: (i) the leg's **CO-FAIL DEPTH** distribution — among rows where the leg fails, the
> total number of failing legs — measured on the book population **and** on a gross-matched
> null; and (ii) the leg's **DISCRIMINATION LIFT**, the real pass rate minus the gross-matched
> null pass rate for that leg alone. A leg whose minimum co-fail depth is **2 or less** on any
> published population is **NOT droppable**, whatever its sole-binder rate. A drop that clears
> both is reported with the widening it produces on the book population and on the null; a drop
> that widens the null by more than the books is reported as PARK, not KEEP.

## Why

1014 established `L3_OOS`'s sole-binder rate at 0.00013 record-wide and the queue read that as
grounds for a drop. A sole rate is a census of a population already filtered by the other four
legs and cannot distinguish a leg that is **redundant** from one that is **one co-binder away
from deciding**. 1018 separates them: on 13,500 gross-matched null draws `L3_OOS`'s minimum
co-fail depth is **3** — never 1, never 2 — and its discrimination lift is **+0.0687**, the
smallest of the five legs and 4.8x below `L4_DD`'s +0.3271. Both readings agree, and only
together do they license the drop.

The same run shows why the clause is not redundant with the sole rate: at 25 bps `L3_OOS` fails
on **86.30%** of null FAIL rows while deciding **0.00%** of them. A leg can be near-universally
failing and still never decisive; a leg can be rarely failing and be decisive. The sole rate
sees neither.

## What it re-labels on the record as it stands

Nothing is re-labelled. The clause CLEARS the one drop the record has proposed (`L3_OOS`: min
depth 3, lift +0.0687, d_real = d_null = +0.0000 in all 9 cells) and would have REFUSED it on
the evidence 1014 alone supplied. Its effect is prospective: it names the two statistics a
future drop must publish.
