# Idea 1174 (lane C, 2026-09-17) — how many committed H-AXIS claims rest on the THREE-POINT LADDER {21, 63, 126}?

**ANSWERED = 15 of 60 C_STRICT claims are measured at EXACTLY {21, 63, 126} (0.250), but that
is the wrong number to worry about: 28 of 60 (0.467) have never been off the three-point ladder
at all, and on the cheapest of them the three-point reading is OVERTURNED at 14 of 18 families
once the rungs are filled in. AND THE FINER LADDER LOSES MONEY: an honest IS-only chooser
allowed the full 16-rung ladder returns 0.0559 LESS OOS Sharpe than one restricted to
{21, 63, 126}, and it loses the run's only 4b-clearing rule-8 pick.**

No RULES change, no book promoted, no PROTOCOL edit (rule 6); RULES.md, PROTOCOL.md, engine.py,
scan.py, bot.py and baseline.py untouched. SELECTION: this lane takes the SECOND open idea; 1174
was second among the LIVE entries of '## Open' (the two ahead of it, 1177 and 1172, are stale
duplicates of entries already in '## Done') and is not EDGAR / Form 4 / 8-K / options / live-data.
Price leg of 288 real books and 10 rule-8 picks, so it carries this run's mandatory rule-8
walk-forward and both KEEP paths.

## THE TWO DIALS AND NO MORE (PROTOCOL rule 4, and the queue names both)

`CLAIM SET` {C_STRICT, C_PROX, C_ALL} x `LADDER SPACING` {L3, L7, LFINE} = **9 cells, EVERY ONE
PUBLISHED** in `.census.csv` and `.ladder.csv`. The three ladders are **STRICTLY NESTED and span
the SAME range [21, 126]** (gates G7, G8), so a moved reading is attributable to RESOLUTION and
never to RANGE:

    L3    ( 3 rungs)  [21, 63, 126]                                          — the record's
    L7    ( 7 rungs)  [21, 42, 52, 63, 76, 90, 126]                          — 1093's, unchanged
    LFINE (16 rungs)  L7 + [26, 32, 37, 47, 57, 69, 83, 105, 115]

NOT dials, reported at every value: PANEL {U56, B136}; N in {5, 8, 10, 12, 15, 20, 25, 30, 40}
(1082/1086/1093's committed ladder); the four statistics {Sharpe, CAGR, MaxDD, turnover}; the
4a/4b legs; the five rule-8 choosers. 2 x 9 x 16 = **288 books, all published** in `.grid.csv`.
Everything else FROZEN at 936/1071/1082/1086/1093's construction: cap INF, CAND20 legs
(21/252, 0/126, 0/63), max_vol 0.60, gross 0.75, W cadence, 10 bps, LAG 1, warm-up 260.

## A DEFECT THIS RUN FOUND IN ITSELF, PRICED AND NOT HIDDEN

The first cut matched the bare-letter H forms (`H=63`, `H in {...}`) CASE-INSENSITIVELY and swept
in **`h=1` — idea 125's event-study forward horizon — and `h=8%/yr` — idea 54's delisting
HAZARD** — different objects that happen to share a letter. The bare-letter forms are now
case-SENSITIVE; the WORD forms ("hold", "min hold", "holding period") stay case-insensitive.
**The repair removes 57 of 299 units (0.191) and adds none** (G11 proves the strict population is
a strict subset). Every number below is post-repair; the pre-repair count is printed in the
console so it is recoverable.

## GATES — 12 of 13 PASS, AND THE ONE FAILURE IS DIAGNOSED RATHER THAN ABSORBED

G1 fast runner == `engine.backtest` 1.39e-17. G2 the committed W/H126 N=20 triple 1.62e-03.
**G3 FAILS: the committed SPY OOS triple is out by 2.894e-03, entirely in the Sharpe term
(0.8684 measured against the committed 0.8713); CAGR is out by 6e-04 and MaxDD by 0.**
**G3b DIAGNOSES IT: this run reproduces 1093's SAME-DAY committed benchmarks — 4 series x 11
statistics, both panels — at 1.11e-16.** So the drift is against the OLDER anchor only: it is
idea 1163's nightly-rewrite vintage effect arriving from the benchmark side, not a construction
error here. **G5 reproduces 1093's WHOLE committed grid cell-for-cell — 126 shared (panel, N, H)
cells x 4 statistics — at 1.78e-15**, which is the premise of the whole re-pricing arm.
G4 live RULES v2 MaxDD 4.95e-05. G6 determinism 0.00e+00. G7/G8 the nesting and the fixed range.
G9 the H dial is live (B136 turnover spread 6.47x/yr). G10 the census partitions. G11 the repair.

## (A) THE CENSUS — THE QUEUE'S NUMBER, AND THE NUMBER THAT ACTUALLY MATTERS

Corpus = **31,582 committed text units** (LEADERBOARD rows + CHANGELOG paragraphs + **909**
`*.result.md` files). **242 carry an H-AXIS token AND name at least one H rung.** A rung is only
ever counted when it is ATTACHED to an H token — never a bare integer — which is deliberately
conservative and understates the population.

    claim set   claims    EXACT {21,63,126}   share    CONFINED to it   share    SUPERSET    OFF
    C_STRICT        60                  15   0.250                28   0.467           6     26
    C_PROX         124                  15   0.121                75   0.605           4     45
    C_ALL          242                  18   0.074               155   0.640           9     78

**EXACT and CONFINED are published side by side and never merged.** EXACT is the queue's literal
ask. CONFINED — the unit names only rungs drawn FROM {21, 63, 126}, one, two or all three — is
the reading that carries the queue's worry, because **a claim measured at H=63 alone is exactly
as unable to see a finer rung as one measured at all three.** On that reading **0.467 of the
record's strict H-ladder claims, and 0.640 of all its H-axis claims, have never been off the
three-point ladder.**

**THE RUNG HISTOGRAM IS THE BLUNTEST STATEMENT OF THE PROBLEM.** Across all 242 units the record
has measured **H=126 in 116, H=21 in 90, H=63 in 63** — and the four rungs 1086/1093 added
(42, 52, 76, 90) in **8 to 10 units each**, essentially those two runs and 1095's proposal.
**H = 26, 32, 37, 47, 57, 69, 83, 105 and 115 appear in ZERO committed units.** Nine of the
sixteen rungs on this run's ladder are rungs the record has never priced.

**THE 'CHEAPEST OF THEM' IS A MEASUREMENT HERE, NOT A CONVENIENCE.** Every claim carries a
re-pricing COST CLASS read off its own text and published as a census column. Among C_STRICT:
**P_BOOK 8, P_NULL 36, P_BOOT 11, P_TAPE 0, P_OTHER 5.** The cheapest class is P_BOOK — a book
metric on the H axis, one build per rung — and Arm B re-prices that family and only that family.
Worth stating plainly: **the record's strict H-ladder claims are MOSTLY the expensive
null-based (EDGE) kind, 36 of 60**, so the cheap arm re-priced here is not the typical one.

## (B) THE RE-PRICING — THE THREE-POINT READING IS OVERTURNED AT 14 OF 18 FAMILIES

A READING of a family is the pair (argmax rung, monotone verdict). It is OVERTURNED when either
component moves between L3 and LFINE. Scored, as pre-declared, on Sharpe over the 18 (panel, N)
families:

    stat        families   overturned   argmax moved   monotone flipped   unconverged (L7 vs LFINE)
    Sharpe            18           14             14                  5            10
    CAGR              18           15             14                  7             9
    MaxDD             18           12             10                  4             9
    turnover          18           14              2                 14             2

**PRE-DECLARED OUTCOME (A): THE 3-POINT LADDER IS LOAD-BEARING** (overturned 14 of 18, against
the pre-registered bar of 9; outcome (D) was checked first and not reached, 10 unconverged
against its bar of 12).

**THE INTERIOR-PEAK QUESTION HAS AN EXACT ANSWER.** On a three-point ladder the only interior
rung is 63, so every 'interior peak' the record has read off it is the claim "H=63 is best".
**Ten of 18 families read an interior Sharpe peak on L3; LFINE keeps the peak at 63 in only 3 of
those 10** — the other seven move to 57, 76, 83, 90 or 115. On CAGR it is 3 of 11.

**TURNOVER IS THE CONTROL THAT MAKES THE POINT.** Its argmax moves at only 2 of 18 families — a
longer min hold trades less, and no amount of resolution changes that. Its MONOTONE verdict
flips at 14 of 18, because L3 cannot see the local reversals. **So the coarse ladder is reliable
for the mechanical statistic and unreliable for every statistic that carries return.**

**THE HONEST CAVEAT, STATED AT FULL STRENGTH: LFINE HAS NOT CONVERGED EITHER.** The Sharpe
argmax still moves between L7 and LFINE at 10 of 18 families. This run does NOT claim LFINE's
argmax is the true one; it claims the three-point one is not a measurement — and by the same
evidence, neither is the sixteen-point one. That is a statement about the tape's resolution on
this axis, not about where the optimum sits.

## RULE 8 AND BOTH KEEP PATHS — THE FINER LADDER LOSES MONEY

Benchmarks: **U56 SPY 15.06% / 0.8814 / -33.72% (halves 0.9598/0.8170), OOS 15.15% / 0.8684 /
-33.72%; U56 RULES v2 (live) @10 bps 8.60% / 1.1980 / -12.05%, OOS 9.42% / 1.2714 / -12.05%;
B136 SPY 15.16% / 0.8861 / -33.72% (halves 0.9596/0.8259), OOS 15.33% / 0.8767 / -33.72%;
B136 RULES v2 7.98% / 1.0993 / -12.24%, OOS 7.88% / 1.1059 / -12.24%.**

Base rates at 10 bps over 288 books: **4b full 17, 4b OOS 18, 4b full AND OOS 17 (U56 16, B136 1),
4a 0 of 288.** By ladder membership: **L3 reaches 8 of them from 54 cells, L7 9 from 126, LFINE
all 17 from 288.**

**RULE 8 — (N, H) chosen on 2009-2016 ONLY, 2017-2026 read ONCE, with the LADDER as the chooser's
constraint.** This is the capital question the idea actually poses.

    ladder   IS-Sharpe chooser   mean OOS Sharpe   mean OOS CAGR   beats SPY   4b full   picks
    L3                              1.0273             18.98%        2 of 2     1 of 2   U56 N=12 H=21,  B136 N=5 H=63
    L7                              1.0095             19.25%        2 of 2     0 of 2   U56 N=15 H=90,  B136 N=5 H=63
    LFINE                           0.9713             18.28%        1 of 2     0 of 2   U56 N=15 H=90,  B136 N=5 H=69

**LFINE - L3 on mean OOS Sharpe: -0.0559.** Buying resolution on the hold axis costs OOS Sharpe:
the extra rungs give the IS argmax more places to overfit (U56's IS-Sharpe optimum moves from
H=21 to H=90 and gives back 0.036 of OOS Sharpe; B136's moves 63 -> 69 and gives back 0.076, and
that pick is the only one of the six that fails to beat SPY out of sample).

**THE ONE RULE-8-REACHABLE 4b BOOK IS REACHED FROM THE COARSE LADDER AND IS ALREADY COMMITTED.**
C_L3's U56 pick, **N=12 / H=21 — 16.76% / 1.1603 / -19.48%, halves 1.246/1.099, OOS 17.50% /
1.1389 / -19.48%** — clears 4b full AND OOS. Idea 1151's committed run already lists U56 N=12
among the books clearing 4b full and OOS at 10 bps, so **this is CONFIRMATORY, not generative,
and no new incumbent is proposed.**

**THE NINE NEW 4b CELLS ARE A SELECTION ARTEFACT AND THE IS RANKS PROVE IT.** Nine of the 17 4b
passes sit at rungs off L3, and seven of those at rungs the record has never measured at all
(H=26 carries five, H=37, 83 and 115 one each). **But not one of them is reachable by any
IS-only chooser: their IS-Sharpe ranks run 64th to 138th of 144 U56 cells.** The best,
**U56 N=20 / H=26 — 14.96% / 1.1560 / -19.95%, OOS 16.95% / 1.2192 / -19.95%** — is 105th on IS
Sharpe. A memo is written for it and **recommends PARK**: a book selected with full-sample
knowledge is not a rule-8 candidate, and the honest measurement of how much of the finer
ladder's "discovery" is selection is exactly that rank.

## SURVIVORSHIP (PROTOCOL rule 9)

U56 (`research/universe.json`) and B136 (`research/universe_broad.json`) are CURRENT-CONSTITUENT
lists. Every CAGR and drawdown LEVEL above is optimistic and every 4a/4b count is an UPPER bound,
including the 17. The census arm is a scan of committed text and carries no market bias at all.
The bias very largely cancels out of a ladder READING, which ranks one construction against
itself on one tape, but it does NOT cancel out of the rule-8 OOS levels.

## VERDICT

**KILL as a capital finding.** 4a is 0 of 288; the run promotes nothing; the finer ladder's
honest chooser LOSES 0.0559 of OOS Sharpe to the coarse one. **The census result stands on its
own: 15 of 60 strict H-axis claims are measured at exactly {21, 63, 126} and 28 of 60 have never
left it, nine of this run's sixteen rungs have never been measured by the record at all, and on
the cheapest family the three-point reading is overturned at 14 of 18 families — while the
sixteen-point reading is not yet a measurement either.**

Script `research/backtests/2026-09-17_how-many-committed-H-AXIS-claims-rest-on-the-THREE-POINT-LADDER-21-63-126_C.py`,
9 CSVs, console log, memo, 6 LEADERBOARD rows. Follow-ups filed 1181 (is the H axis resolvable at
all on this tape, or is every argmax on it a sampling artefact), 1182 (how many committed ladder
claims in the record name a rung the record has measured in fewer than 10 units) and 1183 (does
the coarse-ladder OOS advantage survive on a rolling IS window and on the small panel).
