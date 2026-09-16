# Idea 993 (lane C, 2026-09-16) — price the EMPTIED-SLOT COST: is DECLINING TO PICK better than the UNSCREENED PICK?

**ANSWER = NOT BY ITSELF. "DECLINING IS BETTER" IS A STATEMENT ABOUT THE FALLBACK, NOT ABOUT THE
SCREEN — the sign flips with what you hold instead (mean ΔSharpe on the emptied slots is **−0.4703
/ +0.4066 / +0.0899** for cash / SPY / the live book), and the one convention the record actually
uses — a declined slot costs nothing — is the only one that is never true.** Idea 980's headline
survives being made to pay, but smaller: median OOS Sharpe **0.8312 → 1.0590 unpaid → 1.0011 paid**
(**25.4% of the published gain is the accounting**) and on the mean **0.7523 → 1.0829 → 0.9087**
(**52.7% is the accounting**). And the screen loses to a strictly simpler rule: **refuse every slot
and just hold the live book — median OOS Sharpe 1.1061, median OOS MaxDD −12.24% — beats the best
screened point (1.0011 / −20.00%) on both.** **KILL for "a declined slot is free."** **KEEP as a
PROTOCOL rule 4 reporting clause (proposed, not applied — rule 6).** 980's PARK stands: **OOS 4a is
0 at 28 of 28 MQ18 points.** Nothing promoted; `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`,
`baseline.py` untouched.

## The grid

The ladder ideas 976 / 981 / 984 / 986 / 980 built, **rebuilt here from scratch**: 3 panels {U56,
B136, SMALL} × 5 books × 2 gross × D/W/M/Q at matched gross × every phase (1/5/21/63) = **2,700
phase-books × 5 cost rungs = 13,500 rows**, plus **18 rule-8 slots per grid half** (3 panels × 2
cadences × 3 IS-only choosers). M/Q is 980's pre-declared headline; D/W is published beside it.
Two tuned axes only — **fallback {FB_NONE, FB_CASH, FB_SPY, FB_LIVE} × floor {0.00 … 0.90}** — all
28 points reported, none selected. The share basis is **fixed** at 980's legal IS-only `S_IS4B`;
`S_ISLEG4` and the leaky `S_FULL4B` are in an appendix with no selection made on them.

## What a declined slot actually holds, 2017–2026

| fallback | U56 | B136 | SMALL | 4b | 4a |
|---|---|---|---|---|---|
| `FB_CASH` (Sharpe **defined** 0.0, DD 0.0) | 0.00% / 0.0000 / 0.00% | same | same | never | never |
| `FB_SPY` (costless) | 15.21% / 0.8713 / −33.72% | 15.33% / 0.8769 / −33.72% | same | never | never |
| `FB_LIVE` (RULES v2, 10 bps) | 9.45% / **1.2765** / −12.05% | 7.88% / 1.1061 / −12.24% | 3.75% / 0.5601 / −13.89% | never | never |

No fallback ever certifies 4b (cash and SPY fail four legs each; the live book fails `L5_CAGR` on
every panel), so **paying for refusals cannot manufacture a 4b pass** — it can only take one away.

## The paid summary, MQ18, 10 bps — all 18 slots scored at every floor

| fallback | floor | declined | OOS 4b | OOS 4a | med Sharpe | **mean** Sharpe | med MaxDD | **mean** MaxDD |
|---|---|---|---|---|---|---|---|---|
| — control | 0.00 | 0 | **0** | 0 | 0.8312 | 0.7523 | −34.14% | −32.35% |
| `FB_NONE` (980's convention) | **0.40** | 6 | **3** | 0 | **1.0590** | **1.0829** | −21.35% | −21.55% |
| `FB_CASH` | 0.40 | 6 | 3 | 0 | 1.0011 | 0.7219 | −20.00% | −14.36% |
| `FB_SPY` | 0.40 | 6 | 3 | 0 | 1.0011 | 1.0142 | −23.32% | −25.60% |
| `FB_LIVE` | 0.40 | 6 | 3 | 0 | **1.0011** | **0.9087** | **−20.00%** | −18.99% |
| `FB_LIVE` | 0.75 | 12 | 0 | 0 | 1.0274 | 0.9547 | −13.89% | −16.14% |
| `FB_LIVE` | **0.90 (all-refuse)** | 18 | 0 | 0 | **1.1061** | 0.9809 | **−12.24%** | −12.73% |

**The median is nearly blind here and that is itself the finding.** Every fallback lands below every
surviving pick, so the median only slides to a different order statistic and reads **1.0011 for all
three** — which is why the mean is carried beside it at every point: it is the mean that prices *how
bad* a refusal is, and it separates cash (0.7219) from SPY (1.0142) by 0.29 of Sharpe at the same
floor with the same picks.

## The three results

**1. The convention is material but does not change what you would ship.** H_CONVENTION **PASS at
0.0579** (median, bar 0.05) and H_CONVENTION_MEAN **PASS at 0.1742**. H_RANK **PASS**: floor 0.40
ranks best under FB_NONE and under FB_LIVE alike. So the free-refusal convention inflates the
*level* of every screened claim in the record and leaves the *ranking* intact — a reporting defect,
not a selection defect.

**2. "Declining beats picking" has no fixed sign.** On the 6 emptied slots at floor 0.40 — which are
the entire SMALL panel — mean ΔSharpe (fallback − the unscreened pick in that same slot) is
**−0.4703 cash (0 of 6 wins) / +0.4066 SPY (6 of 6) / +0.0899 live (4 of 6)**, and mean ΔMaxDD is
**+0.3225 / −0.0147 / +0.1836**. Both H_DECLINE_S and H_DECLINE_DD **FAIL**: no fallback wins on
both statistics, and cash and SPY disagree on the sign of each. **A refusal is worth whatever you
hold instead, and the record has never named that object.**

**3. The screen loses to not screening at all.** H_DECLINE_ALL **FAIL**: the degenerate all-refuse
point (floor 0.90 — every slot on the live book) reads **1.1061 / −12.24%** against the best
eligible screened point's **1.0011 / −20.00%**, better on *both*. The screened point's only
advantage is the one thing the all-refuse point cannot have: **3 OOS 4b passes against 0**, because
the live book's 7.88% OOS CAGR fails 4b's CAGR floor everywhere. So the honest reading is narrow:
the screen buys 4b passes, not risk-adjusted return.

## Where the refusals are NOT free — the D/W half

At D/W the same screen declines **12 of 18 slots at floor 0.10 and 15 of 18 from 0.25 up**, and the
unscreened control there passes **4 OOS 4b**. Every screened floor passes **0**. The paired column
says why: `ctrl_4b_in_emptied` is **2 at floor 0.10 and 4 from 0.25 up** — *all four* of the
control's OOS 4b passes sit in slots the screen empties. On M/Q that column is **0 at every floor**.
**980's refusals looked free only because, on the M/Q half it reported, they happened to be.**

## The null, with the same refusals paid the same way

2,000 size-matched random screens, seed 993, refusals paid identically in the null. At FB_LIVE@0.40
the paid median OOS Sharpe beats **0.9960** of draws (null mean 0.8018) and paid median MaxDD beats
0.9475 — **H_NULL PASS**, so the share still carries information once refusals are charged. On the
OOS 4b count it is 980's knife-edge unchanged: **0.9557 / 0.9547 at floors 0.40 / 0.50 and
0.29 / 0.30 / 0.50 elsewhere.**

## Rule 8, both KEEP paths, and the comparands

The whole experiment is a rule-8 walk-forward: (book, gross) chosen on **2009–2016 alone**,
2017–2026 read once. **KEEP path 4a: 0 of 28 MQ18 points, refused outright** — as in 980, 981, 984
and 986. **KEEP path 4b: 3 of 18 slots at floors 0.40/0.50 under every fallback**, unchanged by the
accounting. Comparands: **SPY OOS 15.21% / 0.8713 / −33.72%**; RULES v2 (live) full-sample Sharpe /
MaxDD **U56 1.2009 / −12.05%**, **B136 1.0994 / −12.24%**, **SMALL 0.6637 / −13.89%**. The six OOS
4b passers anywhere in the run are the record's standing set and **all six are U56**: D/W
`BAND03`@1.00 (12.45% / 1.287 / −14.77%, 12.67% / 1.276 / −15.91%), W `TOP20`@0.75, and M `TOP20`@0.75
(16.68% / 1.283 / −19.51%), `BAND03`@1.00, `EWELIG`@0.75. **None passes 4a. Nothing promoted — this
is the fifth refusal of the same object, not a fifth sighting.**

## Gates — 11 of 11 PASS, printed before any result number

G0 `offset_mask(·,per,0)` ≡ `engine.rebalance_mask` on D/W/M/Q, 0 rows. G1 fast `Ctx` ≡
`engine.backtest` on returns AND turnover, D and M, max|d| **2.498e-16**. G2 `BAND03@0.75` ≡
`baseline.rules_v2_weights` **0.000e+00**. **G2b the FB_LIVE series IS the live book: identical to
the ladder's own (BAND03, CORE, W, phase 0, 10 bps) row on all 8 reported metrics, max|d|
2.220e-16.** **G3a CROSS-RUN: idea 980's committed 13,500-row ladder reproduced on 13,500 of 13,500
rows × 46 numeric columns, max|d| 7.105e-15.** **G3b CROSS-RUN: 980's committed 756 screened picks
(21 floor × basis points × 36 slots) reproduced book-for-book, gross-for-gross and refusal-for-
refusal, 0 disagreements** — the screen here is 980's, not a lookalike. **G3c CROSS-RUN: 980's
published 6 / 12 / 18 emptied slots at floors 0.40 / 0.75 / 0.90 recomputed exactly.** G4 matched
gross, 30 target matrices. G5 determinism 0.000e+00. **G6 ACCOUNTING IDENTITY: at floor 0.00 no slot
is declined and all four fallback conventions give identical numbers, max|d| 0.000e+00** — the
fallback provably touches only emptied slots. G7 IS-purity: screen and picks invariant under
permuted OOS columns, 0 disagreements.

## Limits, stated

Cash and SPY are scored **costless** while the live book pays the full 10 bps, which flatters the
two passive fallbacks — i.e. it works *against* this run's own claim that refusals are expensive.
Cash's Sharpe is a **definition** (0.0 for a zero-variance series), not a measurement; it is the one
number here that is a convention rather than a result, and it is why cash's mean ΔSharpe is the
largest negative in the paired table. The all-refuse point is degenerate by construction and is
excluded from the best-floor rule by 980's own "fills at least half the slots" eligibility, which
this run inherits verbatim rather than re-invents; it is reported as its own hypothesis precisely so
the exclusion is visible. Floors 0.40 and 0.50 are one point, not two — no family's share falls
between them.

## Survivorship (rule 9)

U56 / B136 / SMALL are current-constituent lists (SMALL additionally drops the 52 tickers with
`max_1d_move` >= 1.0 per `data/small_meta.csv`), so every CAGR and drawdown LEVEL is optimistic and
every 4b pass count — screened, unscreened and fallback alike — is an **UPPER bound**. The measured
object is a **difference between two accounting conventions applied to the same picks on the same
tape**, and is very nearly immune. One asymmetry with teeth: `FB_SPY` and `FB_CASH` are **not**
survivorship-inflated at all while the screened picks are, so wherever a passive fallback beats a
screened pick the true gap is **wider** on honest data, not narrower — which strengthens result 3
and weakens nothing above.

## Proposed, not applied (rule 6)

`2026-09-16_declined-slot-clause_C.memo.md` proposes a PROTOCOL rule 4 reporting clause: *a screen
that can decline to pick reports its statistics over ALL slots, with the fallback named; a
screened statistic quoted over surviving picks alone is reported as such and carries no comparison
with an unscreened control.* It contradicts nothing — 980 is reproduced here to the basis point on
every published number.

## Follow-ups filed

995 (the D/W half loses all 4 control OOS 4b passes to refusals while M/Q loses 0 — is refusal cost
a cadence object the way `L4_DD` is?), 996 (census the record's committed screen/eligibility claims
for how many are quoted over surviving picks only), 997 (the all-refuse point beats every screened
point on Sharpe and MaxDD but buys 0 OOS 4b — price the live book as a standing 4b comparand).
