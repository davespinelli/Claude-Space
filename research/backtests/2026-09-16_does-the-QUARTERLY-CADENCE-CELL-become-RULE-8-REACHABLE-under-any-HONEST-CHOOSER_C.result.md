# Idea 1099 (lane C, 2026-09-16) — does the QUARTERLY CADENCE CELL become RULE-8 REACHABLE under any HONEST CHOOSER?

**ANSWERED = NO AT EVERY HONEST RUNG, BUT THE "NO" IS DECIDED BY 0.0002 OF IS SHARPE — 73x BELOW
877's OWN COMMITTED SEED FLOOR. KILL of "reachable / unreachable" as a publishable binary on this
ladder; the U56 Q cell is PARKED, not proposed.** No RULES change, no book promoted, no PROTOCOL
edit (rule 6); RULES.md, PROTOCOL.md, engine.py, scan.py, bot.py and baseline.py untouched.

SELECTION: lane C takes the SECOND open idea; 1099 was the second line under `## Open` and is not
EDGAR / Form 4 / 8-K / options / live-data. It has a price leg — 18 books over 2 panels x 9 cadence
rungs, 32 rule-8 picks — so it carries this run's mandatory rule-8 walk-forward and both KEEP paths.

## The two dials and no more (PROTOCOL rule 4)

`CHOOSER` {C_ISSHARPE, C_ISDD, C_ISCAGR, C_ISSHARPE_TP} x `CADENCE SET` {C4, C9} = **8 points, all
published, on BOTH panels**. C4 = D/W/M/Q, every cadence `engine.rebalance_mask` serves; C9 =
1118's nine (D, 2D, W, 2W, M, 2M, Q, 2Q, 4Q), built as k-th-bar subsets of engine's own masks
without touching engine.py. The TP chooser carries a **declared penalty ladder LAM = {5, 10, 25,
50, 100} bps, every rung published**; the headline rung is LAM = 10, PROTOCOL rule 2's own cost and
the only non-arbitrary value on the ladder. **Nothing is selected on LAM**: it is reported at every
point, and D1's LAM* — the smallest penalty that reaches Q — is a measurement of how far outside
honesty one would have to go, not a fit. PANEL is not a dial. COST is not a dial (10 bps
everywhere; the 0/25/50 rungs appear once, in D3, only to re-price the queue's own sentence).
TARGET_Q = {Q} and TARGET_SLOW = {Q, 2Q, 4Q} were both fixed before the run, because 1117/1133's
committed walk-forward found the 4b passer on this ladder is 2Q.

FROZEN at 1082/1094/1096/1110/1117/1118's construction: CAND20 legs, cap INF, max_vol 0.60, gross
0.75, min hold 126, N=20, 10 bps, LAG 1, warm-up 260, IS end 2016-12-31.

## Gates: 11 of 12 PASS, printed before any result number — and the one FAIL is my own bar

G1 fast runner == `engine.backtest` 1.39e-17. G2 CROSS-RUN 936/1071/1082/1094/1096's committed U56
W/H126/N=20 triple 3.18e-07. G3 SPY OOS 1.70e-04. G4 live RULES v2 MaxDD -12.05% 4.95e-05.
**G5 `cadence_mask` == `engine.rebalance_mask` on all four cadences engine serves, 0 differing
bars**; G5b every extended rung is a k-th-bar subset of an engine schedule, 0. **G6 CROSS-RUN
1117/1133's committed U56 CADENCE 2Q figures reproduce on all EIGHT numbers (full CAGR/Sharpe/DD,
both halves, OOS CAGR/Sharpe/DD) at 4.96e-05**; **G7 its committed U56 W-book OOS triple at
3.15e-05**. G8 determinism 0.00e+00. G9 C9 nests C4, 0 rungs lost. G10 the cadence ladder is live
(min-over-panels Sharpe spread 0.1745).

**G11 FAILS and is reported as a FAIL rather than loosened: I declared the turnover axis live at
max/min >= 5x and it reads 3.560x** (B136 1.22 -> 4.36x/yr; U56 4.19x, 0.97 -> 4.06). The bar was
set one rung too tight; the axis is plainly live and nothing in the reading below depends on the
threshold. The honest record is 11 of 12, not a re-cut 12 of 12.

## The literal answer

**0 of the 16 HEADLINE picks (4 choosers x 2 cadence sets x 2 panels, TP at LAM = 10) land on Q,
and 0 land anywhere in {Q, 2Q, 4Q}.** Six land on the frozen default W. Over all 32 picks (every
LAM rung included) Q is reached 4 times, all of them on U56 and all of them at LAM >= 25 bps.
Pick census, all 32: W=11, 2M=7, 2W=6, D=4, Q=4 — C4 {W 11, Q 3, D 2}, C9 {2M 7, 2W 6, D 2, Q 1}.

**LAM*, the smallest penalty that reaches Q** (fine ladder 0..500 bps, 1 bp):

| panel | cadence set | pick @ LAM 0 / 10 / 100 / 500 | LAM*(Q) | LAM*(SLOW) | turnover non-increasing in LAM |
|---|---|---|---|---|---|
| U56 | C4 | W / W / Q / Q | **11 bps** | 11 bps | yes |
| U56 | C9 | 2W / 2W / Q / 4Q | **76 bps** | 76 bps | yes |
| B136 | C4 | W / W / W / Q | **107 bps** | 107 bps | yes |
| B136 | C9 | 2M / 2M / 2M / 4Q | **never within 500 bps** | 118 bps | yes |

## The finding that matters: the "NO" is a tie, not a fact

**On U56/C4 the IS-Sharpe-net-of-10-bps chooser prefers W over Q by +0.0002.** That is the entire
margin on which the queue's sentence "no IS-only chooser selects it, so it is not reachable at the
cost the protocol fixes" rests. It is **73x smaller than 877's own committed 0.0145 seed floor**,
which idea 1100 found already decides 8 of 14 committed ladder picks, and far inside any resolution
the record has measured on a Sharpe ladder (1103: U56 S_FULL floor 0.176 over a spread of 0.183).
**LAM*(Q) = 11 bps is ONE basis point above the cost PROTOCOL rule 2 fixes.** So the correct
statement is not "the quarterly cell is unreachable at 10 bps" but "W and Q are indistinguishable
to this chooser at 10 bps, and which one it names is not a resolvable quantity."
H_REACH REFUTED on the letter; the binary it tests is KILLED as a publishable object.

## A correction to the queue's own premise (H_PASS10 PARTLY)

The queue states the Q cell "clears 4b full AND OOS at 25 and 50 bps", implying it does not at 10.
**On U56 it clears 4b FULL and 4b OOS at ALL FOUR rungs — 0, 10, 25 and 50 bps** (Sharpe 1.1511 /
1.1388 / 1.1203 / 1.0891). The cell is a 4b passer at the cost the protocol fixes; unreachability,
not passing, was ever the whole of its problem. **On B136 it fails 4b at all four rungs**, and its
turnover there is 1.97x/yr, not the 1.65x the queue quotes — 1.65x is the U56 number, so the
queue's premise sentence is a U56 fact carrying no panel stamp.

## Reachability is a property of the RUNG SET, not of the rung (new, and it agrees with 1117/1118)

**LAM*(Q) moves 11 -> 76 bps, a factor of 6.9, between C4 and C9 on the same panel and the same
chooser**, and 107 bps -> never on B136. Adding rungs makes Q *harder* to reach, because 2W and 2M
intercept the penalty path before Q does (U56 C9 picks 2W at LAM 0..75). This is 1117's general
statement seen from the chooser's side: a quantity read off a whole ladder — here "the rung a
chooser reaches" — is not comparable across ladders of different rung counts, and any committed
reachability claim should carry the rung set it was measured on.

## What reaching it would buy (H_WORTH REFUTED, and the prize is also below resolution)

**3 of 16 headline picks beat the frozen W rung's OOS Sharpe; median regret +0.0000** (six picks
*are* W). The Q cell itself does beat W out of sample — **OOS Sharpe 1.1726 vs 1.1643, +0.0083, at
1.65x/yr turnover against 2.90x** — but +0.0083 is itself an order of magnitude below the seed
floor, so the ranking of the two books is as unresolved as the chooser's preference between them.
H_MONO_TP SUPPORTED 4 of 4: the penalty behaves as a penalty (pick turnover never rises with LAM),
which is what licenses reading D1 at all. H_TP_ONLY is vacuous (nothing reached Q at the headline).
H_LAMSTAR PARTLY: LAM*(Q) <= 100 bps on 2 of 4 (panel, cadence set) paths.

## Rule 8 and both KEEP paths — nothing proposed as capital

Every chooser reads IS 2009-2016 alone; OOS 2017-2026 read once. **32 picks: 4b full 8, 4b OOS 8,
4a 0; median OOS Sharpe 1.0967, median regret vs the frozen W rung +0.0000.** **Whole grid, 18
books: 4b full 3, 4b OOS 3, 4a 0** — all three on U56 and all three W-family cadences:

| book | full CAGR / Sharpe / MaxDD | halves | OOS CAGR / Sharpe / MaxDD | turnover |
|---|---|---|---|---|
| U56 W (incumbent) | 15.58% / 1.1397 / -19.13% | 1.2037 / 1.0971 | 16.97% / 1.1643 / -19.13% | 2.90x/yr |
| U56 Q | 15.40% / 1.1388 / -19.94% | 1.2214 / 1.0911 | **17.28% / 1.1726 / -19.94%** | **1.65x/yr** |
| U56 2Q | 13.26% / 1.0019 / -17.90% | 1.0667 / 0.9668 | 15.47% / 1.0660 / -17.90% | 1.31x/yr |

Benchmarks: **U56 SPY 15.10% / 0.8829 / -33.72% full (halves 0.9588/0.8207) and 15.21% / 0.8711 /
-33.72% OOS; B136 SPY 15.16% / 0.8861 / -33.72% and 15.33% / 0.8767 / -33.72%; live RULES v2 U56
8.62% / 1.2007 / -12.05% full and 9.45% / 1.2762 / -12.05% OOS, B136 7.98% / 1.0993 / -12.24% and
7.88% / 1.1059 / -12.24%.** `baseline.compare()` on the U56 Q cell at freq='Q' returns **KILL on
path 4a** (Sharpe 1.139 vs the live book's 1.201; MaxDD -19.9% vs -12.1%), as every growth book on
this record does. **4b: the U56 Q cell PASSES full and OOS but is NOT rule-8 reachable at any
honest penalty rung, so PROTOCOL rule 8 makes it PARK, not KEEP. NOTHING PROPOSED AS CAPITAL.**

SURVIVORSHIP (rule 9): U56 and B136 are current-constituent lists, so every 4b figure is an upper
bound. The reachability half is a contrast between two selections over the same inflated tape and
the bias very largely cancels out of it; it does not cancel out of the 4b legs, measured against
SPY, a real index.

Files: `.py`, `.console.txt`, `.gates.csv`, `.grid.csv`, `.benchmarks.csv`, `.picks.csv`,
`.lamstar.csv`, `.hypotheses.csv`, `.memo.md`.
