# Idea 1162 (lane B, 2026-09-17) — why does an IID resample produce DEEPER drawdowns than a BLOCK one?

**ANSWERED = BECAUSE THE BLOCK NULL INTERPOLATES BETWEEN THE IID NULL AND THE OBSERVED PATH,
SO "IID DEEPER THAN BLOCK" IS NOT A FACT ABOUT BOOTSTRAPS AT ALL — IT IS THE STATEMENT THAT
THE OBSERVED DRAWDOWN IS SHALLOWER THAN ITS OWN IID NULL, WHICH IS IDEA 1161's FACT. The two
follow-ups 1159 filed as siblings are ONE question, and the ordering REVERSES on the first
control whose observed drawdown is deeper than its null.**

`sign(BLOCK − IID) == sign(OBS − IID)` at **15 of 15** cells, BLOCK lies strictly between the
two at **14 of 15**, `spearman(BLOCK/IID − 1, OBS/IID − 1) = 0.8286`. **ALL THREE CARRIERS THE
QUEUE NAMED ARE DEAD: H_GATE 0 of 3, H_CADENCE 0 of 3, H_MEANREV 0 of 3.** The textbook
variance story is dead too (H_VR 9 of 15 while VR(63) < 1 at 14 of 15). **AND A CORRECTION TO
THE PARENT: on SMALL, 84.1% of 1159's effect is BOOTSTRAP MACHINERY, not the book's order.**

13 of 13 gates pass. 1 of 8 hypotheses supported — the structural one. Nothing proposed, no
RULES change, no PROTOCOL edit (rule 6). `RULES.md`, `PROTOCOL.md`, `engine.py`, `scan.py`,
`bot.py` and `baseline.py` untouched.

SELECTION: this lane takes the LAST open idea; 1162 ended `## Open` and is not EDGAR / Form 4
/ 8-K / options / spin-off / live-data. Pure price run — 180 books, 45 null cells, 180 ladder
rungs — so it carries this run's mandatory rule-8 walk-forward and both KEEP paths.

---

## The two dials and no more (PROTOCOL rule 4; the queue names both)

`NULL TYPE` {N_IID, N_BLOCK, N_STAT} × `CONTROL` {C_BOOK, C_GATEOFF, C_NOREBAL, C_SHUFFLE,
C_SPY} = **15 per panel, 45 in all, EVERY ONE PUBLISHED** in `.dialgrid.csv`.

The controls are a **one-factor-at-a-time ladder off the anchor book**, one per carrier the
queue names, plus one falsification control: `C_GATEOFF` removes the eligibility gate (the
queue's "gate's own exit timing"), `C_NOREBAL` buys once at the first post-warm-up rebalance
and never trades again (the queue's "rebalance cadence"), `C_SHUFFLE` permutes the book's own
realised returns (the queue's "randomly-ordered control"), and `C_SPY` is SPY alone — the most
mean-reverting series on this tape, `ac1 −0.0991` against the book's `−0.0501`, so it is the
sharp test of the queue's "short-horizon mean reversion".

PANEL {U56, B136, SMALL} is not a dial. **The BLOCK-LENGTH LADDER L ∈ {1, 2, 5, 10, 21, 42,
63, 126, 252, 504, 1008, T} is not a dial** — it is the one-parameter family under measurement,
every rung is in `.ladder.csv`, nothing is ever selected on it, and the headline uses the
record's frozen L = 63 and no other. The GROSS ladder (15 rungs) is not a dial. q is not a
dial (0.90 headline, 0.80 / 0.95 beside). SEED is not a dial — three are run at every headline
cell and the spread is published, which is what gives "materially weakens" a scale.

Frozen at 1082/1094/1098/1102/1108/1110/1116/1117/1118/1122/1131/1140/1148/**1159**'s
construction: CAND20 legs, cap INF, max_vol 0.60, gross 0.75, min hold 126, N = 20, cadence W,
10 bps (rule 2), LAG 1, warm-up 260, IS end 2016-12-31, block L = 63, 1000 draws, crc32 seeds.

**PRICE VINTAGE (draft rule 12, proposed by 1163, complied with although NOT enacted).**
`data/prices.csv` @HEAD **crc32 = 85eebc60**, 4,706 rows to 2026-09-16 — which **is** 1159's
tape, since no daily close has landed since `6f1fcb1`. That is deliberate: 1159's cell-level
numbers are this run's cross-run gate and can only be replayed on 1159's own tape. The
2026-09-15 vintage 1154/1160/1161 pinned (**crc32 = 5f9b8015**, 4,705 rows) is recovered from
git and every headline re-read on it in Arm C.

---

## Gates — 13 of 13 PASS, printed before any result number

G1 fast runner ≡ `engine.backtest` 1.39e-17. G2 the control constructor ≡ the anchor book
2.78e-17. **G3 the committed U56 W/H126/N=20 triple on the HEAD tape reads 1.62e-03 — 1163's
defect carried and published, not absorbed; G12 reads 3.18e-07 on the PINNED vintage.** G4
**cross-run, at full precision from 1159's own `.walkforward.csv` rather than from rounded
prose**: SPY and live OOS Sharpe 0.00e+00. G5 live RULES v2 MaxDD ≡ −12.05% 4.95e-05.
**G6 is the gate this run turns on — `N_BLOCK` at L = 1 IS `N_IID`, bit for bit on the same
seed, 0.00e+00; the block family provably contains the iid null as an endpoint.** G7 N_STAT's
realised mean block length 4.31 off 63. G8 all three nulls share the observed marginal mean
(1.15e-02 relative), so ORDER is the only thing that differs between them. **G9 replays 1159's
committed U56 OBJ_MAXDD observed level at 7.11e-15 and G10 re-reads its "12 of 12" ordering
out of its own committed file at 12 of 12** — the premise is verified from the record, not
recalled. G11 SMALL determinism with the weight cache dropped and rebuilt, 0.00e+00. G13 the
gross ladder's scaling shortcut `W(g) ≡ g·W(1)` is exact, 6.94e-18.

---

## (A) The answer — the 15 cells

Median |MaxDD| %, 1000 draws, seed 0. `phi = (BLOCK − IID)/(OBS − IID)`: 0 is the iid null, 1
is the observed path. `epi` is the observed max-drawdown episode's length in bars.

| panel | control | OBS | N_IID | N_BLOCK | N_STAT | BLK/IID | OBS/IID | phi | epi |
|---|---|---|---|---|---|---|---|---|---|
| U56 | C_BOOK | 19.128 | 22.572 | 19.880 | 19.519 | 0.8807 | 0.8474 | 0.781 | 18 |
| U56 | C_GATEOFF | 20.107 | 22.426 | 20.121 | 20.107 | 0.8972 | 0.8966 | 0.994 | 58 |
| U56 | C_NOREBAL | 71.945 | 57.115 | 62.246 | 66.419 | **1.0898** | **1.2597** | 0.346 | 120 |
| U56 | C_SHUFFLE | 23.161 | 22.386 | 22.648 | 22.810 | 1.0117 | 1.0346 | 0.338 | 148 |
| U56 | C_SPY | 26.197 | 24.790 | 26.197 | 26.197 | **1.0568** | **1.0568** | **1.000** | 23 |
| B136 | C_BOOK | 20.740 | 25.765 | 22.451 | 21.337 | 0.8714 | 0.8050 | 0.660 | 23 |
| B136 | C_GATEOFF | 22.306 | 26.588 | 23.781 | 22.417 | 0.8944 | 0.8390 | 0.656 | 23 |
| B136 | C_NOREBAL | 60.004 | 45.332 | 49.359 | 52.013 | **1.0889** | **1.3237** | 0.275 | 143 |
| B136 | C_SHUFFLE | 25.717 | 25.977 | 25.257 | 24.948 | 0.9723 | 0.9900 | 2.773 | 155 |
| B136 | C_SPY | 26.196 | 25.017 | 26.196 | 26.196 | **1.0471** | **1.0471** | **1.000** | 23 |
| SMALL | C_BOOK | 35.814 | 40.246 | 37.830 | 37.692 | 0.9400 | 0.8899 | 0.545 | 39 |
| SMALL | C_GATEOFF | 33.143 | 41.643 | 38.461 | 37.120 | 0.9236 | 0.7959 | 0.374 | 23 |
| SMALL | C_NOREBAL | 38.937 | 50.631 | 49.341 | 48.664 | 0.9745 | 0.7690 | 0.110 | 1439 |
| SMALL | C_SHUFFLE | 46.781 | 40.104 | 40.705 | 39.960 | 1.0150 | 1.1665 | 0.090 | 1006 |
| SMALL | C_SPY | 26.197 | 24.184 | 26.197 | 26.197 | **1.0832** | **1.0832** | **1.000** | 23 |

**H_INTERP SUPPORTED: sign 15 of 15, betweenness 14 of 15, spearman 0.8286.** The one
non-between cell is B136 / C_SHUFFLE, where the OBS−IID gap is 0.26 pp of pure sampling noise
and phi is therefore meaningless (2.773) — reported, not dropped.

**THE FALSIFICATION LANDS.** 1159's "12 of 12" ordering **REVERSES at 7 of 15 cells** here — 5
of the 12 non-shuffle ones — and the reversals are exactly the controls whose observed drawdown
is DEEPER than their own iid null: **all three C_SPY cells, C_NOREBAL on U56 and B136, and two
of the three C_SHUFFLE cells.** SMALL / C_NOREBAL does NOT reverse, and that is the identity
working correctly rather than an exception: its 1,439-bar drawdown is still shallower than its
own iid null (OBS/IID 0.7690), so BLK/IID stays below 1 at 0.9745. `C_SPY` is the cleanest —
`BLOCK = STAT = OBS` to 1e-3 on every panel, phi exactly 1.000, and a cross-seed spread of
**0.00e+00**, because SPY's worst drawdown is a 23-bar episode that a 63-bar block carries
intact in essentially every draw. There is no clustering story and no mean-reversion story
that produces that; it is the interpolation, and nothing else.

**THE L LADDER TRACES IT END TO END** (`.ladder.csv`, 180 rungs). At L = 1 the block null
equals the iid null by construction (G6); at L = T it equals the observed value at
**15 of 15 cells to 1.8e-13**, because a single wrapped block is a rotation and a rotation splits an
18-to-155-bar episode in under 4% of draws. The declared monotonicity bar **REFUTES H_MONO at
13 of 15 sign / 11 of 15 |rho| ≥ 0.80 — and the verdict stands as declared, not re-cut.**
Reported beside it, not in place of it: dropping the two C_SHUFFLE cells, whose "want sign" is
a coin flip because their OBS−IID gap is noise, the reading is **12 of 12 sign and 11 of 12
|rho| ≥ 0.80**.

---

## (B) All three of the queue's carriers are dead

- **H_MEANREV REFUTED 0 of 3, and it is the decisive one.** `C_SPY` is MORE negatively
  autocorrelated than the book (`ac1 −0.0991` vs `−0.0501`) and its ordering is the OPPOSITE
  sign on every panel (BLK/IID 1.0568 / 1.0471 / 1.0832 against the book's 0.8807 / 0.8714 /
  0.9400). More mean reversion, opposite sign: mean reversion does not carry it.
- **H_GATE REFUTED 0 of 3.** Removing the eligibility gate shrinks |OBS/IID − 1| on U56
  (0.1526 → 0.1034) and B136 (0.1950 → 0.1610) but nowhere near halves it, and on SMALL it
  makes it LARGER (0.1101 → 0.2041). The gate contributes; it does not carry.
- **H_CADENCE REFUTED 0 of 3, and it goes the wrong way on every panel.** Removing rebalancing
  RAISES |OBS/IID − 1| (0.1526 → 0.2597, 0.1950 → 0.3237, 0.1101 → 0.2310) — and flips the
  ordering's sign on U56 and B136, because a never-rebalanced book concentrates into its
  winners and then takes a 72% / 60% drawdown over 120–143 bars.
- **H_VR REFUTED 9 of 15 — the textbook story fails as an explanation even where it holds as
  an arithmetic fact.** VR(63) < 1 at 14 of 15 cells (range 0.458 .. 1.126), so the long-horizon
  variance argument predicts BLOCK shallower everywhere; the sign actually agrees at 9 of 15. A
  |MaxDD| is an episode statistic, not a variance functional, and averaging over the whole tape
  cannot see which single episode a block preserves.

---

## (C) The correction to 1159 — how much of its effect is the BOOK and how much is the BOOTSTRAP

The pre-registered falsification bar for `C_SHUFFLE` (BLOCK ≡ IID once order is destroyed)
**FAILED at 1 of 3, and the bar was wrong, not the measurement**: the interpolation identity
forbids what it demanded, because a shuffled path still HAS an observed drawdown that differs
from the iid median by sampling noise. The verdict is recorded REFUTED as declared and is not
re-cut. The corrected sub-arm runs **5 independent permutations per panel** — and it does not
say what this run expected either. **With order destroyed the block null is not centred on the
iid null; it sits systematically BELOW it: pooled mean BLOCK/IID = 0.9696 over 15 permutations
(U56 0.9804, B136 0.9789, SMALL 0.9495).**

That is a MACHINERY effect with a mechanism: a moving block is a contiguous slice of a fixed
array and cannot contain the same bar twice, while an iid draw can stack the tape's worst days
on top of each other. Block sampling shallows drawdowns even on a series with no order at all.
Since the shuffled series carries C_BOOK's exact marginal distribution, its mean is that
panel's machinery baseline, and 1159's effect decomposes:

| panel | total BLK/IID − 1 | machinery | ORDER | machinery share |
|---|---|---|---|---|
| U56 | −0.1193 | −0.0196 | **−0.0996** | 16.5% |
| B136 | −0.1286 | −0.0211 | **−0.1076** | 16.4% |
| SMALL | −0.0600 | −0.0505 | **−0.0095** | **84.1%** |

**1159's ordering is real on U56 and B136 and mostly an artefact of the bootstrap on SMALL** —
a correction no amount of re-running 1159's own grid could find, because its grid never
contained a series with the order taken out.

---

## (D) The mechanism — H_EPISODE, declared **POST HOC** and flagged as exploratory

With the queue's three carriers dead, what sets `phi` was still open, so this was declared
AFTER seeing Arm A and is exploratory wherever it is quoted. Candidate: a block of length L can
carry the observed worst episode intact only if L exceeds that episode's length, so `L*` (the
block length at which the null median has covered 95% of the way to the observed value) should
sit near the episode's own length. **BAR: 0.25 ≤ L*/episode ≤ 4 at ≥ 8 of 12 non-shuffle cells.
MEASURED 7 of 12, spearman(L*, episode) 0.5547 — REFUTED.** What the same table does show, and
it is the honest residual: **L* ≥ the episode length at 12 of 12 non-shuffle cells**, with
L*/episode running 1.09 to 21.91. The episode's length is a **lower bound** on L*, not a
predictor of it — a block must be at least as long as the episode to carry it, and being long
enough is not sufficient, because the block must also START early enough. Filed, not resolved.

---

## (E) Vintage invariance (1163's defect, checked rather than assured)

Re-read on the pinned 2026-09-15 tape (crc32 5f9b8015, 4,705 rows) against HEAD (85eebc60,
4,706): **the sign of (BLOCK − IID) is unchanged at 4 of 5 controls and max |delta BLOCK/IID|
is 0.0357.** The one flip is **C_SHUFFLE**, whose sign is noise by construction and whose
observed value moves 23.161 → 18.474 because the permutation is re-drawn on a different-length
tape. Every substantive cell is vintage-invariant.

---

## (F) Rule 8 and both KEEP paths

4 tradable controls × 15 gross rungs × 3 panels = **180 books, all published** in
`.walkforward.csv`. C_SHUFFLE is excluded because a permuted return stream is not a book; it is
a falsification control and is said so rather than scored as capital.

Benchmarks: **U56 SPY 15.06% / 0.8814 / −33.72% (H 0.9598/0.8170), OOS 15.15% / 0.8684; U56
RULES v2 (live) 8.60% / 1.1980 / −12.05%, OOS 9.42% / 1.2714. B136 SPY 15.16% / 0.8861 /
−33.72%, OOS 15.33% / 0.8767; B136 RULES v2 7.98% / 1.0993 / −12.24%, OOS 7.88% / 1.1059.
SMALL SPY 14.06% / 0.8581 / −33.72%, OOS 15.33% / 0.8767; SMALL RULES v2 4.30% / 0.6637 /
−13.89%, OOS 3.75% / 0.5600.**

Base rates: **4b full 19 of 180, 4b OOS 21 of 180, 4a 2 of 180** (U56 10/12/0, B136 9/9/0,
SMALL 0/0/2). The two 4a passes are SMALL / C_SPY at gross 0.30 and 0.35 — de-grossed SPY
beating a live book whose SMALL Sharpe is 0.6637, which is a statement about the live rules on
a small-cap panel and not a proposal.

**RULE 8: 9 IS-only picks, and NOT ONE clears 4b.** C_ISSHARPE / C_ISCAGR / C_ISDD choosing on
2009–2016 alone pick C_GATEOFF 0.95, C_NOREBAL 1.00, C_GATEOFF 0.30 (U56); C_BOOK 1.00, 1.00,
0.30 (B136); C_SPY 1.00, 1.00, 0.30 (SMALL). **0 of 9 pass 4b full, 0 of 9 pass 4b OOS, 1 of 9
passes 4a** (SMALL C_ISDD → C_SPY 0.30).

**Best book clearing 4b FULL and 4b OOS: U56 / C_BOOK / gross 0.75 — full 15.55% / 1.1381 /
−19.13% (H 1.2049/1.0932), OOS 16.92% / 1.1615 / −19.13%. This is the INCUMBENT DEFAULT and
not a discovery** (1159 committed the same cell at the same numbers), **and it is not reachable
by any IS-only chooser here.**

The one 4b-passing band that is not the incumbent is **U56 / C_GATEOFF at gross 0.55–0.75**
(OOS Sharpe 1.1461, MaxDD −20.11%) and **B136 / C_GATEOFF at 0.50–0.65**. A memo is written
because path 4b passes, and it **recommends PARK**: the band is strictly dominated by the
incumbent on Sharpe, CAGR and drawdown, rule 8 does not reach it, 4a is 0 of 180, and
C_GATEOFF was built as a mechanism control, not proposed as a book. See `.memo.md`.

---

## Survivorship (PROTOCOL rule 9)

U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the CURRENT constituents of a sub-$2B
screen (`data/SMALL_PANEL_README.md`), less the documented `max_1d_move >= 1.0` exclusion (52
of 715 dropped; 663 names served plus SPY as benchmark). Every LEVEL here — CAGR, |MaxDD|, and
every null median built on top of them — is optimistic, and a resample null prices SAMPLING
error on the tape it is handed and cannot correct that. The bias does **not** cancel out of the
4b legs. It very largely **does** cancel out of every headline claim in (A)–(D), which are all
ratios of one construction against itself on the same tape: BLOCK/IID, OBS/IID, phi, the L
ladder and the machinery decomposition.

---

## Files

`2026-09-17_why-does-an-IID-RESAMPLE-produce-DEEPER-drawdowns-than-a-BLOCK-one_B.py`, 13 CSVs
(`gates`, `hypotheses`, `dialgrid`, `cells`, `diagnostics`, `ladder`, `monotonicity`, `lstar`,
`shuffle`, `decomposition`, `vintage`, `walkforward`, `picks`), console log, memo, 5
LEADERBOARD rows.

**Follow-up filed:** 1164 — what sets `phi` once the episode length is only a lower bound on
`L*`; and 1165 — whether the record's other committed block-bootstrap bands carry the same
16%/84% machinery share that the shuffle control exposes here.
