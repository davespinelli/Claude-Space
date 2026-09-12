# Idea 842 - do the record's permutation/bootstrap p-values NAME THEIR POOL?  (2026-09-12, cloud)

## The answer, in two numbers
**CENSUS (headline claim set NEAR: 201 numeric p-value sites tied to a
resampling null, in 24 committed files of 2827 scanned):
the pool is named at 0.8308 under the LOOSE reading and 0.4776 under the STRICT one**
(STRICT = a pool word AND the unit permuted AND a count, all within 400 characters of the p-value).
So the record mostly gestures at its pool and states it properly slightly less than half the time.
H_NAMED PASS, H_STRICT FAIL.

**RE-PRICING: the pool is worth up to 17x in p on an observed statistic that
does not move at all.** ABS's delta is +0.1481 at all
7 pools (H_DIR exact: max spread 0.0e+00) and its p runs
0.0010..0.0170 (z +2.17..+4.22),
crossing the conventional bars 0.01;0.001 - i.e. a reader who quotes
"p 0.001" and a reader who quotes "p 0.017" can both be right about the same data and disagree at
alpha 0.01.  At alpha 0.05, 7 of 324 re-priced cells flip outright,
all of them QROLL - the family whose own
membership the pool changes - so on THIS leg pair the flip needs a membership change and the bar
level does the rest.

## Where the queue's own example stands
H_QUEUE **FAIL**: ABS reads p 0.0010 (z +4.22) at pool ALL
and p 0.0010 (z +4.21) at pool LONGW.  Idea 834's ABS-turns-significant flip does
NOT reproduce here, and the reason is stated rather than buried: this file's leg pair is FULL -> OOS
read from 834's committed .arms.csv, not 834's PRE/POST split, and ABS is already significant at
pool ALL on it.  The MECHANISM the queue names reproduces exactly - the null's location is a pool
property (0.0414 -> 0.0618 -> 0.0861 -> 0.0567 -> 0.0485 -> 0.0374 -> 0.0705
across pools) while the observed delta is fixed.

## Rule 8 (both legs run)
* ON THE CENSUS, declared cut 2026-09-05: **unresolvable** - only 2
  of the 57 date-stamped sites predate it, so the IS leg cannot resolve a 0.10 bar; both
  readings FAIL as declared.  On the MEDIAN cut the same statistic PASSES both readings
  (LOOSE gap 0.0199,
  STRICT gap 0.0847).
* ON THE CLAIM: pool chosen on the FULL leg (ALL), OOS leg read once -> p 0.0010
  (PASS).

## Book leg (computed from prices in this file; nothing tuned, nothing promoted)
4a passes **0** and 4b passes **3** of 12 book-rung rows.  At 10 bps: LIVE RULES v2
8.63% /
1.2018 /
-12.05%; the standing 4b candidate
11.54% /
1.2017 /
-15.91% (OOS
12.70% /
1.2775 /
-15.91%); SPY
15.16% / 0.8861 / -33.72% (OOS 15.33% /
0.8767 / -33.72%).  The candidate's 4b pass and 4a failure reproduce
at every cost rung; no book's parameter was chosen here.

## Verdict
**ANSWERED - 6 of 9 pre-registered hypotheses PASS.**  A committed
permutation/bootstrap p-value in this record is not interpretable without its pool: the same
unchanged statistic is worth 17x in p across four pools of the same corpus,
and slightly over half the record's own p-value sites fail to state the pool to the STRICT standard.
**PROPOSED, not applied (PROTOCOL rule 6, Sunday review only):** every committed permutation or
bootstrap p-value states (i) what was permuted or resampled, (ii) the pool it was drawn from and
(iii) that pool's unit count - and any cross-artefact citation of such a p-value repeats the pool.
No RULES change, no KEEP claimed, no memo, no book promoted.

## Caveats
Current-constituent survivorship in all three panels.  The FULL leg contains the OOS leg, so the
leg-to-leg delta is not a disjoint contrast (its LEVEL is an in-window identity - ideas 833/836);
this run's object is the p-value of a FIXED delta under differently pooled nulls, which that nesting
does not touch.  The census is a TEXT detector: its 12 controls are printed in the console, it was
repaired against those controls BEFORE any census number was read, and the per-site table is
committed so any other reading can be re-scored without re-running anything.
