# Idea 1247 (lane C, 2026-09-18) — should the schema clause say DECLARE WHETHER L REACHES THE IDENTITY rather than STATE A LADDER?

**ANSWER = YES, AND IT SHOULD BE A BINARY, NOT A FRACTION. KILL (capital), no new book.**
Pre-declared outcome **(A) THE AMENDMENT DOMINATES** fires; (B) does not. Gates **13 of 13**.
Script: `2026-09-18_should-the-SCHEMA-CLAUSE-say-DECLARE-WHETHER-L-REACHES-THE-IDENTITY-rather-than-STATE-A-LADDER_C.py`

## The arithmetic the whole thing rests on (ARM C, gate G7/G9)
A moving-block draw at `L = T` has exactly one legal start, so every draw returns the original
sample: measured identity share **1.000000**, deviation from 1 **< 1e-12**, and the identity rung
resolves **72 of 72** decisions. Two consequences, both measured, not assumed:
the top rung's detection is **arithmetic, free of draws**, and *"does my verdict survive the reach
to the identity?"* is exactly *"is my verdict RESOLVED at my own L?"* — 55 decisions flagged, which
is precisely the 55 UNRESOLVED at the frozen `L = 63`.

## The two clauses, on 1208/1243's same 72 decisions
| clause | rungs demanded | detects /72 | recall DEP12 | recall DEP11 | extra draws/verdict |
|---|---|---|---|---|---|
| CF_POINT (status quo) | 63 | 0 | 0.0000 | 0.0000 | 0 |
| CF_LADDER4 (the record's habit) | 21\|63\|126\|252 | 6 | 0.0984 | 0.2727 | 3,000 |
| CF_LADDER11 (1208's clause as run) | 1..1008 | 22 | 0.3607 | *1.0000* | 10,000 |
| CF_LADDER12 (its widest form) | 1..1008\|T | 61 | *1.0000* | *1.0000* | 10,000 |
| **CF_IDENTITY (the amendment)** | **63\|T** | **55** | **0.9016** | **0.7273** | **0** |
| CF_FRACTION, f = 0.02 / 0.05 / 0.10 / 0.25 / 0.50 / 1.00 | 42..T down to 63\|T | 55 at all six | 0.9016 | 0.7273 | 5,000 → 0 |

*Italicised recalls are DEFINITIONAL* (DEP11/DEP12 are the sets those ladders' own rungs disagree
on) and are declared in the console as such, so neither is read as evidence for the ladder.

## What this settles
1. **The amendment is free and the ladder is not.** 55 of 61 DEP12 decisions at **0 draws**, against
   1208's ladder at 10,000 draws for 22. Ratio published, not the level alone.
2. **The FRACTION BAR is inert at every one of its six values** — detection is 55 at f = 0.02 through
   f = 1.00 while the draw bill runs 5,000 → 0. Every admitted rung below the identity adds nothing
   the identity had not caught, so the graded form is **strictly dominated** by the binary one.
3. **The queue's literal wording is inert too, and the run says so rather than hiding it:** the
   identity has L/T = 1 and is therefore the *widest* admitted rung at every bar f ≤ 1, so
   "declare whether the WIDEST rung's block is a non-trivial fraction of T" reads YES always.
   That is why the clause below names the identity directly.
4. **What the amendment cannot see: 6 of 72.** Decisions L-dependent among the 11 non-degenerate
   rungs but constant across {63, T}. Real, and below the pre-declared bar of 8 — so (B) does not
   fire and the ladder is **not** separately earned, but the 6 are published, not rounded away.
5. **Cost.** At SC_RESAMPLE (1,450 bound units; drift from 1243's 1,413 is +37 and this file will add
   more) the ladder clause forces a **re-run on 1,408 units at 10,000 draws each = 14,080,000 draws**.
   The amendment forces a re-run on **1,099** — those stating no L at all, 1249's population, which is
   unfixable under *either* clause — and brings **331 more into conformance by EDIT, at 0 draws**.
   Its re-run set is a strict subset of the ladder's (G2).

## Capital (PROTOCOL rule 8 and both KEEP paths) — this is where it dies
No clause form is a book. As a chooser the amendment **costs nothing and buys nothing**: 17 picks,
identical to the point rule, mean OOS Sharpe **0.8278 (+0.0000)**; it is a disclosure, not a filter
(G12). Ladder forms cut to 11–14 picks and **lose** (0.8220). Acting on all 72 gives 0.8016; **doing
nothing** (holding the anchor rung) gives 0.7922 — and doing nothing carries **4b 24 of 72** against
the point rule's **1 of 17**, so the filter that wins on Sharpe loses on the 4b count.
**4a 0 of 162** rung books. **4b BOTH 25 books**, every one already held by the record.
SPY OOS 0.8745 / 0.8767 / 0.8767; live RULES v2 OOS 1.2778 / 1.1059 / 0.5620 (U56 / B136 / SMALL).
Survivorship (rule 9): current-constituent panels; levels optimistic, the 4b passes are upper bounds.

## PROPOSED for the Sunday review (rule 6) — a PROTOCOL schema line, NEVER a chooser. NOT applied here.
> **PROTOCOL 10 (proposed).** Every published verdict that rests on a block resample states the block
> length **L** and the resampled window length **T**, and declares **whether L = T**. A verdict at
> **L = T is not a resample result**: the draw is the identity, so it re-states the observed sample
> and resolves by construction. Where a claim is a rate over block lengths, the ladder is stated in
> full; a ladder that includes **L = T** reports that rung separately and never inside the rate.

Nothing in RULES.md, PROTOCOL.md, scan.py, bot.py or baseline.py was modified by this run.
