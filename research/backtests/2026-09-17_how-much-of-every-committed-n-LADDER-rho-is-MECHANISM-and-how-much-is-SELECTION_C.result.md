# Idea 1176 (lane C, 2026-09-17) — how much of every committed n-LADDER rho is MECHANISM and how much is SELECTION?

**ANSWERED = THE MEDIAN n-LADDER rho RETAINS 0.3674 OF ITS MECHANISM, 29 of 56 resolvable cells retain less than half, and 10 REVERSE — but the headline correction is to 1171 itself: on the record's OWN TAPE the N→|MaxDD| "diversification mechanism" is ≈ ZERO (−0.0269 U56, +0.1408 B136), so 1171's 0.582 attenuation was almost entirely TAPE STRUCTURE, not selection. The one place selection ADDS instead of cancelling is N→CAGR, which sign-flips at 8 of 11 cells.** No RULES change, no book promoted, no PROTOCOL edit (rule 6). SELECTION: lane C takes the SECOND open idea; 1176 was second in `## Open` and is not EDGAR / Form 4 / 8-K / options / live-data.

## The two dials and no more (PROTOCOL rule 4, and the queue names both)
`CLAIM SET` {C_VALUED, C_SIGNED, C_ALL} × `TAPE` {T_REALRAND, T_IID, T_BLOCK, T_FACTOR} = **12 cells, every one published** in `.grid.csv`. NOT dials, all reported at every value: PANEL {U56, B136, SMALL}; the six n-ladder OUTCOMES; the 88-book population per panel (9 N × 4 H × 2 cadences at gross 0.75, plus an 8-rung gross ladder) = **264 real books and 5,280 mechanism books**; SEED (five at every controlled cell, spread published); the reading-change BAR (published on a 0.00/0.25/0.50/0.75/1.00 ladder, headline 0.50, so any bar can be read off the file); the four rule-8 choosers. Frozen at 1082/1086/1093/1094/1151/1164/1171's construction.

## What this run adds that 1171 did not have, and why it was needed
1171's `attenuation` = |rho_obs| / |rho_synth| compares a REAL-tape/score-selected rho against an EXCHANGEABLE-tape/score-selected one, so **two** things differ at once. This run adds one control and separates them **at fixed tape**:

`T_REALRAND` — the REAL panel, the REAL eligibility gate, the REAL cadence / min-hold / gross / lag / cost machinery, with the rank key replaced by exchangeable noise: a **random N of the eligible names**. Then

    SELECTION      = rho_obs  − rho_realrand   (identified at FIXED TAPE — the queue's term)
    TAPE STRUCTURE = rho_realrand − rho_synth  (what 1171's attenuation folded into "selection")
    retention      = rho_obs / rho_mech

## Gates 10 of 10 PASS
G1/G2/G3 the committed incumbent anchor (0.155520 / 1.138079 / −0.191276). **G4/G5 this run reproduces from 1171's own committed `.drivers.csv` the two attenuations it exists to decompose: median rho_obs D_N_SH +0.1659, D_N −0.4980.** G6 T_REALRAND is seed-exchangeable (two independent random keys, incumbent cell: Sharpe 1.1334 vs 1.0049). **G7 the composite score BEATS a random book at the incumbent cell (1.1381 vs 1.1016) — so "selection" is a real term and not a mislabel.** G8 `rand_key()` deterministic (0.00e+00). G9 `synth()` deterministic (0.00e+00). G10 the harvest's claim sets partition it (508 = 349 + 159).

## (A) The harvest — 1,058 committed files, 122,864 sentences
**508 sentences name BOOK SIZE and an ordering/correlation token. 349 (0.6870) QUOTE A MAGNITUDE (C_VALUED), 159 (0.3130) are directional only (C_SIGNED); 120 carry an explicit rho token and only 68 (0.1339) name a control of any kind.** By outcome: O_OOSSH 90 sentences (81 valued), O_SHARPE 84 (71), O_DD 46 (40), O_CAGR 34 (26), O_TURN 23 (17), O_CSTAR 7 (6). **324 of 508 touch none of the six priced outcomes and are declared UNSCORABLE rather than quietly counted as "no change".**

## (B) The decomposition — 56 of 72 cells resolvable, 16 DEGENERATE and published as such
| outcome | med rho_obs | med rho_mech | med SELECTION | med retention | sign flips |
|---|---|---|---|---|---|
| O_SHARPE (N→Sharpe) | +0.1659 | +0.8484 | −0.6181 | **+0.2334** | 0/11 |
| O_DD (N→\|MaxDD\|) | −0.4980 | −0.9168 | +0.3238 | +0.6432 | 1/11 |
| O_CAGR (N→CAGR) | −0.7242 | +0.1900 | −0.4840 | **−1.7344** | **8/11** |
| O_TURN (N→turnover) | −0.1556 | −0.1499 | −0.0246 | +1.2251 | 0/11 |
| O_OOSSH (N→OOS Sharpe) | +0.3269 | +0.8094 | −0.6302 | +0.3406 | 0/11 |
| O_CSTAR (N→c\*) | −0.1912 | +0.3569 | −0.5481 | −0.5356 | 1/1 (**11 of 12 DEGENERATE**) |

**MEDIAN retention over all 56 resolvable cells = 0.3674; median |selection| share of |mech|+|sel| = 0.3976; SIGN CHANGES 10 of 56.** Retention < 0.25 at 18 of 56 (0.3214), **< 0.50 at 29 of 56 (0.5179)**, < 0.75 at 40 of 56 (0.7143).

**THE FOUR THINGS WORTH READING:**

1. **THE DIVERSIFICATION MECHANISM IS NOT ON THIS TAPE, and that corrects 1171.** On an exchangeable tape N→|MaxDD| is −0.9491 (T_IID) / −0.9634 (T_BLOCK) — book size orders drawdown almost perfectly, because a small book is a noisy average of i.i.d. columns. **On the record's OWN tape with selection removed it is −0.0269 (U56) and +0.1408 (B136) — indistinguishable from nothing, and the wrong sign on B136.** The TAPE-STRUCTURE term is +0.9222 / +1.0954 / +0.5896 and the SELECTION term −0.4711 / −0.3901 / −0.2658. So 1171's reading — "selection cancels four-fifths of the diversification mechanism" — is the wrong attribution: **real cross-sectional correlation, not selection, destroys the mechanism, and what is left of the observed −0.4980 is supplied BY selection.** Every n-ladder claim that argues from diversification is arguing from a mechanism its own panel does not have.
2. **N→CAGR is PURE SELECTION and it REVERSES: 8 of 11 resolvable cells.** The record's concentration premium reads −0.8570 (U56) / −0.7242 (B136) / −0.1928 (SMALL) — smaller books earn more. With the same tape, same gate, same machinery and the score removed it reads **+0.4941 / +0.2449 / +0.2912**: a random small book earns LESS. |selection| share 0.7322 / 0.7983 / 0.6244. **This is the one outcome where the composite is carrying the whole relation rather than cancelling it — and the only outcome whose rho a mechanism argument may not be used to support.**
3. **The EDGE-ladder premise keeps its sign and loses its size, on every tape.** O_SHARPE retention 0.5556 / 0.3522 / 0.1921 at T_REALRAND and 0.1198–0.3652 on the exchangeable tapes; O_OOSSH the same picture (0.3406 median). **Both contrasts point the same way here** (SELECTION −0.28/−0.31/−0.43, TAPE-STRUCT −0.32/−0.49/−0.32), so unlike O_DD the attenuation really is part selection — it is just never the four-fifths 1171 quoted on one panel.
4. **1175's structural problem is confirmed from the other side: O_CSTAR is DEGENERATE at 11 of 12 cells**, the single resolvable one (U56, T_REALRAND) sign-flipping. A 4b-conditional outcome cannot be decomposed either, for the reason 1171 gave: no control book passes 4b, and a column of tied zeros is not a measurement.

**A ratio caveat this run states rather than hides.** `retention` is unstable where the mechanism is near zero — exactly the O_DD/T_REALRAND cells, which read +18.5000 (U56) and +1.8125 (SMALL). Those are NOT counted as magnitude changes (the ladder is one-sided), which biases the 29-of-56 count DOWNWARD. The additive `selection` term and `|sel| share` (0.9459 and 0.4483 at those two cells) are published beside every ratio so the reading does not depend on the ratio.

## (C) The two dials — how many CLAIMS change reading, all 12 cells
| claimset | T_REALRAND | T_IID | T_BLOCK | T_FACTOR |
|---|---|---|---|---|
| C_VALUED (349 claims, 150-151 scorable) | **0.5497** | 0.8467 | 0.7067 | 0.1733 |
| C_SIGNED (159 claims, 32-33 scorable) | **0.3939** | 0.2500 | 0.0000 | 0.2500 |
| C_ALL (508 claims, 182-184 scorable) | **0.5217** | 0.7418 | 0.5824 | 0.1868 |

**On the record's own tape 96 of 184 scorable n-ladder claims (0.5217) change reading — 68 on a SIGN flip, 54 on a magnitude that is majority-selection.** 324 of 508 are UNSCORABLE and reported as such. **The dial that matters is the TAPE, not the claim set:** the share runs 0.1868 (T_FACTOR) to 0.7418 (T_IID) at C_ALL, a 4× range, because a one-factor tape produces books too alike to rank (it carries 5 of the 16 degenerate cells and the largest seed spread, 1.0697) and an i.i.d. tape produces the maximal mechanism. **T_REALRAND is the one construction that holds the record's own tape fixed, and it is the number a future run should quote.**

## (D) Rule 8 and both KEEP paths — 264 real books, all published
Benchmarks: **U56 SPY 15.06% / 0.8814 / −33.72% (halves 0.9598/0.8170), OOS 15.15% / 0.8684; U56 LIVE RULES v2 @10 bps 8.60% / 1.1980 / −12.05%, OOS 9.42% / 1.2714. B136 SPY 15.16% / 0.8861 / −33.72%, OOS 15.33% / 0.8767; B136 LIVE 7.98% / 1.0993 / −12.24%. SMALL SPY 14.06% / 0.8581 / −33.72%, OOS 15.33% / 0.8767; SMALL LIVE 4.30% / 0.6637 / −13.89%.**

Base rates at 10 bps: **4b full 19 of 264 (U56 16, B136 3, SMALL 0), 4b OOS 20, BOTH 19, 4a 0 of 264** — identical to 1171's independently built grid, as it must be.

| chooser | med OOS Sharpe | mean OOS Sharpe | > SPY OOS | 4b full | 4b OOS | 4a | med N | med OOS CAGR |
|---|---|---|---|---|---|---|---|---|
| CH_ISSHARPE (record's habit) | 0.8940 | 0.8880 | 4/6 | **1/6** | **1/6** | 0/6 | 8.5 | 17.18% |
| CH_NSMALL (act on the n-ladder claim) | 0.9052 | **0.8928** | 5/6 | 0/6 | 0/6 | 0/6 | 5.0 | 19.18% |
| CH_NMECH (act only where the mechanism survives) | 0.8836 | **0.8473** | 4/6 | 0/6 | 0/6 | 0/6 | 5.0 | 17.38% |
| CH_NBIG (falsification control) | **0.9813** | 0.8620 | 4/6 | 0/6 | 0/6 | 0/6 | 17.5 | 14.63% |

**ACTING ON THE n-LADDER CLAIM BUYS +0.0048 OF MEAN OOS SHARPE AND COSTS THE ONLY 4b PASS.** CH_NSMALL and CH_ISSHARPE differ at only 3 of 6 picks (U56/W, SMALL/W, SMALL/M); the edge that buys is inside its own falsification control's range — **CH_NBIG, the deliberate opposite, has the HIGHEST median OOS Sharpe of the four at 0.9813** — and the one 4b pass the record's habit finds (U56/W N=12/H=21) is lost because CH_NSMALL swaps it for N=5/H=63, whose −26.26% drawdown blows the DD cap's −20.2%. **Filtering by the mechanism is worse still: CH_NMECH is LAST on mean OOS Sharpe at 0.8473.** Its filter (O_SHARPE retention ≥ 0.50 with no sign flip on T_REALRAND) passes on U56 (0.5556) and refuses on B136 (0.3522) and SMALL (0.1921), so its only two decisions distinct from CH_NSMALL are the two SMALL picks — **and both refusals were wrong out of sample** (SMALL/W OOS Sharpe 0.8429 against the acted pick's 1.0499, SMALL/M 0.4526 against 0.5183). **A decomposition that is true of the record is not thereby a selection device, and this run priced that rather than assuming it.**

**THE CONTEXT NUMBER THIS RUN DID NOT EXPECT.** The RANDOM-SELECTION books on the REAL tape, scored against the REAL SPY, clear 4b at **133 of 440 (0.3023) on U56 and 20 of 440 (0.0455) on B136, 0 of 440 on SMALL** — against the scored books' **16 of 88 (0.1818) and 3 of 88 (0.0341)**. **On U56 a random book passing the same gate clears 4b more often than the composite's book does**, because the score buys CAGR at the cost of the DD cap. It is a base rate over 5 seeds of the same 88-cell grid, not a claim that random beats the score (G7 shows the score wins on Sharpe at the incumbent cell) — but any future 4b pass on this panel quoted without that 0.3023 beside it is quoted against nothing.

**NO NEW KEEP CANDIDATE AND NO MEMO.** 4a is 0 of 264. The 19 books clearing 4b full AND OOS are exactly 1171's list, built by an independent grid the same day — **confirmatory, not generative** — and the best of them (U56/W/N=12/H=126: 17.65% / 1.1658 / −20.17%, OOS 18.78% / 1.1701, c\* = 64.2) is already on the record.

## Survivorship (rule 9)
U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the current constituents of a sub-$2B screen less 52 tickers with `max_1d_move >= 1.0` (664 names plus SPY as benchmark), dropped before anything else is computed. Every LEVEL is optimistic and the bias does NOT cancel out of the 4b legs — including the 0.3023 random base rate above, which is the shallowest a random book could have drawn on a survivor panel. It cancels far better out of a rho. **T_REALRAND is built from the SAME surviving names as rho_obs, which is exactly what makes the SELECTION contrast the cleaner of the two; T_IID / T_BLOCK / T_FACTOR inherit the panel's optimistic marginals and T_IID only its pooled mean and sd.**

## Verdict
**KILL as a capital finding** (acting on the n-ladder claim loses its only 4b pass and its edge sits inside its own falsification control; mechanism-filtering is worse; nothing enacted). **Answered as a record finding: 0.5217 of the record's scorable n-ladder claims change reading on its own tape, the median rho retains 0.3674 of its mechanism, N→CAGR is pure selection and reverses, and the N→|MaxDD| diversification mechanism 1171 credited to the tape does not exist on the panel the record trades.**

Script `research/backtests/2026-09-17_how-much-of-every-committed-n-LADDER-rho-is-MECHANISM-and-how-much-is-SELECTION_C.py`, 7 CSVs, console log, 3 LEADERBOARD rows.
