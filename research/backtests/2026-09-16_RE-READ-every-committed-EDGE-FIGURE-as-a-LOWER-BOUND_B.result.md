# Idea 1097 (lane B, 2026-09-16) — RE-READ every committed EDGE FIGURE as a LOWER BOUND

**ANSWERED = MOSTLY, BUT "LOWER BOUND" IS NOT A PROPERTY OF THE RECORD — IT IS A PROPERTY OF 81 OF
ITS 94 COMMITTED EDGE FIGURES.** Re-priced against the rank-matched ELIG null at its own cell,
`GATE = EDGE_OPEN − EDGE_ELIG` is **≤ 0 at 81 of 94** (0.862), mean **−0.791 pp**, median −0.679,
range **[−2.728, +1.104] pp**. So the re-read is a **KILL of the universal claim** 1097's own queue
text makes ("all UNDER-state rank skill"), a **CONFIRM of the direction** for the large majority,
and a **CORRECTION of its quoted envelope**: `H_MAGNITUDE` FAILS, max |GATE| **2.728 pp** against
the 0.03–2.47 pp the queue quotes from 1085 as if it were record-wide.

**THE 13 EXCEPTIONS ARE NOT SCATTERED — 6 of 9 sit in one slice, U56 at H = 21**, the shortest hold,
where the mean GATE is **+0.216 pp** and the ELIG null is the EASIER comparand. Every other
(panel, H) slice is 8/9 or 9/9 negative. So the sign of the "lower bound" re-read is a **HOLD** fact
on U56 and a flat fact on B136 (−1.902 / −1.815 / −0.869 pp at H = 21 / 63 / 126).

**WHAT ACTUALLY CHANGES.** `H_SIGN` **PASSES: 0 of 94** committed figures change sign — no published
EDGE reading is reversed by the re-read. `H_VERDICT` fails on **3 of 94** and all three go the same
way (not-decisive → decisive; decisive count 91 → 94). **`H_RANK` FAILS hardest and is the finding
that matters: 13 of 34 committed LADDERS change their argmax**, far beyond the single U56 H = 126
case 1085 already published. **Twelve of the thirteen sit on axes the record has never scored
against this null at all** — the H axis (7 of 18 move) and 1071's cap axis (5 of 8). The N axis,
the one the record has walked most, is the stable one (1 of 8).

**A CORRECTION TO 1071's OWN HEADLINE, AND TO `H_CONV`.** At the doubly-committed U56/N=20/H=126/
cap INF cell — 1071's committed **+5.07 pp** — GATE reads **+0.271 pp under CASH** and **−0.027 pp
under REBUILT**. The two DD-match conventions **disagree on the sign** (`H_CONV` FAIL, 7 of 8 agree,
max gap 0.386 pp). At the record's single most-cited EDGE figure, "is it a lower bound?" is **not a
tape question at this resolution — it is a convention question**.

**No RULES change, no book promoted, no PROTOCOL edit (rule 6); RULES.md, PROTOCOL.md, scan.py,
bot.py and baseline.py untouched.** Script
`research/backtests/2026-09-16_RE-READ-every-committed-EDGE-FIGURE-as-a-LOWER-BOUND_B.py`,
8 CSVs, console log. **Gates 13 of 13 PASS. Hypotheses 2 of 7.**

---

## SELECTION

Lane B takes the LAST open idea. 1097 was the last line under `## Open` and names no EDGAR / Form 4
/ 8-K / options / live-data source, so it runs in the sandbox. Unlike most record-census ideas in
the queue, 1097 **has a price leg**: re-pricing a committed EDGE figure means rebuilding its book
and its null on the tape, so it carries this lane's mandatory rule-8 walk-forward and both KEEP
paths.

## THE TWO DIALS AND NO MORE (PROTOCOL rule 4)

**CLAIM SET** {STRICT, WIDE} × **NULL GATE** {OPEN, ELIG}.

- **STRICT** — a committed EDGE figure that is (i) a book-minus-null CAGR advantage and (ii)
  machine-readable in a committed CSV with a fully determined cell, so it can be rebuilt
  byte-for-byte. **94 figures, 188 prices, all published.** This is the arm every number is read
  off.
- **WIDE** — STRICT plus every committed prose unit carrying an `edge` token, a figure in pp AND a
  null/comparand token. Its deliverable is a census, not a second set of prices.
- **OPEN** — random ranks, `elig` = all priced. 1071's / 1082's / 1086's convention, i.e. the one
  every committed EDGE figure in the record was measured under. It is the **control**, reproduced
  under each committing run's exact seed recipe (gates G5–G9), not a new measurement.
- **ELIG** — random ranks, `elig` = the book's own gate (px > 200d MA AND 20d annualised vol <
  0.60). The null gets the gate for free and differs from the book **only in how it orders the
  survivors**. 1085's rank-matched null.

**THE CELL COORDINATES ARE NOT DIALS.** `(panel, N, H, cap, seeds, DD-match convention)` are taken
exactly as the record committed them. This run walks no new rung and tunes nothing over them.
Everything else is frozen at 936/1071/1082/1085/1086's construction: CAND20 legs
[(21,252),(0,126),(0,63)], max_vol 0.60, gross 0.75, W cadence, 10 bps, LAG 1.

## THE HARVEST

| family | committer | coordinates | seeds | DD match | figures |
|---|---|---|---|---|---|
| A | 1082 / 1085 / 1086 | 2 panels × 9 N × 3 H, cap INF | 40 | REBUILT | **54** |
| B | 1071 | 2 panels × 4 N × 5 caps, H = 126 | 20 | CASH | **40** |

**94 committed EDGE figures. The record has scored exactly 18 of them against the ELIG null (1085,
H = 126, cap INF, family A only). 76 had never been re-priced** — the whole H = 21 and H = 63
slices, and the entire cap ladder, where the null gate had never been crossed with the cap dial at
all. The 8 doubly-committed (panel, N, H=126, cap INF, N ∈ {20,25,30,40}) cells appear in **both**
families because the record committed them twice under different conventions and seed counts; both
readings are re-priced and neither is dropped.

## THE CLAIM-SET CENSUS (dial 1, WIDE arm)

Corpus **31,030 committed units** (LEADERBOARD and QUEUE by line, CHANGELOG and 863 `*.result.md`
by paragraph). **1,019 carry an `edge` token; 1,001 of those carry a numeral; 215 carry a figure in
pp; 161 carry a null/comparand token; only 52 carry BOTH a pp figure and a null token, and 35 of
those also carry a cell key.** By source: LEADERBOARD 19, QUEUE 19, CHANGELOG 3, result.md 11.

**The WIDE arm's result is that WIDE adds no prices.** The record's `edge` vocabulary is
overwhelmingly *not* the null contrast — "grid edge", "knife-edge", "ladder edge", "Sharpe edge"
dominate the 1,019 — and of the 52 units that are, essentially all trace back to the same four runs
whose CSVs STRICT already harvests at full precision. Re-pricing a prose figure adds a rounding
error, not a measurement. That is a claim-set fact, and it is why every number below is STRICT.

## GATES — 13 of 13 PASS, printed before any result number

| gate | value | |
|---|---|---|
| G1 fast runner ≡ `engine.backtest` (U56, N=20, H=126, cap INF) | 1.39e-17 | PASS |
| G1b `gross_rescaler(1.0)` ≡ `nrun` (the bisection kernel is the same book) | 1.39e-17 | PASS |
| G1c **capped** build ≡ `engine.backtest` (U56, N=20, cap 2.00) — 1071's arm | 1.39e-17 | PASS |
| G2 CROSS-RUN 936/1071/1082 committed W/H126 N=20 triple | 3.18e-07 | PASS |
| G3 CROSS-RUN SPY OOS triple (U56 / B136) | 1.70e-04 / 4.05e-05 | PASS |
| G4 live RULES v2 MaxDD ≡ committed (U56 −12.05%, B136 −12.24%) | 4.95e-05 / 9.85e-06 | PASS |
| **G5 CROSS-RUN reproduce 1086's 54 committed `EDGE_pp`** | **8.88e-16** | PASS |
| **G6 CROSS-RUN reproduce 1085's 18 committed `EDGE_ELIG_pp` and `EDGE_OPEN_pp`** | **8.88e-16** | PASS |
| **G7 CROSS-RUN reproduce 1071's 40 committed null medians and book CAGRs (CASH/20)** | **8.33e-17** | PASS |
| G8 CROSS-RUN reproduce 1082's 18 committed `EDGE_pp` | 8.88e-16 | PASS |
| G9 every harvested figure reproduced from its own committer | 8.44e-15 | PASS |

G5–G9 are the point of the gate suite: **all 94 harvested figures reproduce from their committing
run to machine precision**, so the OPEN column is literally the record's own numbers and every GATE
below is a difference of two measurements made the same way.

## A RECORD-HYGIENE DEFECT THIS RUN HIT AND PAID FOR

1071's `cap` column is a **string key** (`"INF"`, `"1.00"`, `"1.25"`, `"1.50"`, `"2.00"`) that enters
its md5 null-seed recipe **verbatim**. Reading that CSV with pandas' default dtype silently converts
it to `inf / 1.0 / 1.25 / 1.5 / 2.0`; re-formatting those draws **different nulls**, and the first
run of this script reproduced 1071 at 8 of 40 cells (only the `1.25` rung, whose string round-trips)
and failed G7 at 8.98e-03. The column is now read as text and never converted. **This is open idea
979's `unit` / `cell_key` proposal arriving as a concrete cost**: a committed CSV whose key column
does not survive `pd.read_csv` is not self-describing, and the failure is silent — it produces
plausible numbers, not an error. Filed as a follow-up.

## THE ANSWER — `H_LOWER`, 94 cells

`GATE ≤ 0` at **81 of 94** (0.862). Mean **−0.791 pp**, median **−0.679**, range **[−2.728,
+1.104]**.

| slice | negative | mean GATE | range |
|---|---|---|---|
| FAMILY A (all) | 47/54 | −0.951 | [−2.728, +1.104] |
| FAMILY B (all) | 34/40 | −0.574 | [−1.697, +0.349] |
| A U56 H=21 | **3/9** | **+0.216** | [−1.154, +1.104] |
| A U56 H=63 | 9/9 | −0.872 | [−1.947, −0.182] |
| A U56 H=126 | 9/9 | −0.465 | [−1.436, −0.027] |
| A B136 H=21 | 9/9 | −1.902 | [−2.728, −1.158] |
| A B136 H=63 | 9/9 | −1.815 | [−2.487, −1.205] |
| A B136 H=126 | 8/9 | −0.869 | [−2.471, +0.123] |

`H_LOWER` **FAILS**, and it fails in one place: **U56 at the 21-day hold**, where 6 of 9 rungs run
positive (N = 8/10/12/15/20/40, GATE +0.876 / +0.982 / +1.104 / +0.640 / +0.151 / +0.136). Against
the seed SE of the difference, **50 of 94 cells are decisively negative and 2 decisively positive**
at 2 SE; the other 42 are inside the noise. So the honest statement is: *most committed EDGE
figures are lower bounds, decisively so; a minority are upper bounds; and roughly 45% of the record
cannot tell.*

## `H_MAGNITUDE` — the queue's quoted envelope is too narrow

1097's queue text quotes 1085's **0.03–2.47 pp** as the size of the understatement. Three cells fall
outside it, all on B136: **N=15/H=21 −2.728**, **N=12/H=63 −2.487**, **N=5/H=126 −2.471 pp**.
`H_MAGNITUDE` **FAILS**. The envelope was a property of the 18 cells 1085 happened to measure, not
of the record.

## WHAT CHANGES — sign, rank, verdict

- **SIGN — `H_SIGN` PASSES, 0 of 94.** Every committed EDGE figure keeps its sign. No published
  reading is reversed.
- **VERDICT — 3 of 94 change**, all not-decisive → decisive, all at **N = 40** (U56 H=63 cap INF
  0.147→0.836 pp; U56 H=126 cap 1.00 0.128→0.875; cap 1.50 0.167→0.889). Decisive count 91 → 94.
  The record's *weakest* EDGE figures are the ones the re-read rescues.
- **RANK — `H_RANK` FAILS, 13 of 34 committed ladders move their argmax.** Declared in advance as
  expected to fail once (1085's U56 H=126, 12 → 5); it fails thirteen times.

| ladder | axis | argmax OPEN → ELIG | ρ |
|---|---|---|---|
| A/U56/H=126/N | N | 12 → **5** | +0.93 |
| A/U56/N=10/H | H | 21 → **63** | −0.50 |
| A/U56/N=12/H | H | 21 → **126** | +0.50 |
| A/U56/N=15/H | H | 21 → **126** | −0.50 |
| A/B136/N=10/H | H | 126 → **63** | +0.50 |
| A/B136/N=12/H | H | 126 → **63** | +0.50 |
| A/B136/N=20/H | H | 126 → **21** | +0.50 |
| A/B136/N=40/H | H | 126 → **21** | +0.50 |
| B/U56/N=20/cap | cap | INF → **1.50** | −0.80 |
| B/U56/N=25/cap | cap | 1.50 → **1.00** | −0.60 |
| B/U56/N=30/cap | cap | INF → **1.25** | −0.60 |
| B/B136/N=20/cap | cap | 1.00 → **1.25** | +0.80 |
| B/B136/N=40/cap | cap | 1.00 → **1.50** | +0.20 |

**The N ladders are the stable ones** (7 of 8 hold their argmax, ρ **+0.867 to +1.000**, none
negative); **the H and cap ladders are not** — **7 of 18** and **5 of 8** move, with ρ down to
−0.500 and −0.800 and **three cap ladders at *negative* rank correlation**.
This dovetails with idea 1098's independent finding that an argmax over a 9-rung ladder sits below
its own resolution floor: 1098 showed the argmax is not stable to the DRAW, and 1097 shows it is not
stable to the CHOICE OF NULL either. **A published argmax over an H or cap ladder should not be
quoted without its null gate.**

## `H_CONV` — the doubly-committed cells, and a correction to 1071's +5.07

| cell | GATE (CASH) | GATE (REBUILT) | |
|---|---|---|---|
| U56 N=20 | **+0.271** | **−0.027** | **DISAGREE** |
| U56 N=25 | −0.416 | −0.546 | agree |
| U56 N=30 | −0.240 | −0.360 | agree |
| U56 N=40 | −0.571 | −0.496 | agree |
| B136 N=20 | −0.315 | −0.669 | agree |
| B136 N=25 | −0.489 | −0.875 | agree |
| B136 N=30 | −1.159 | −0.977 | agree |
| B136 N=40 | −0.887 | −1.067 | agree |

`H_CONV` **FAILS 7 of 8**, max |CASH − REBUILT| **0.386 pp**. The one disagreement is at the cell the
record cites most: **1071's committed +5.07 pp on U56/N=20**. Reproduced exactly (`EDGE_OPEN`
5.0719 vs committed 5.0719), it is a lower bound under REBUILT (−0.027 pp, itself inside the noise)
and an **upper** bound under CASH (+0.271 pp). Neither reading is wrong; the quantity is smaller
than the gap between two defensible conventions. **1071's +5.07 should be quoted as ±0.4 pp for
convention alone**, before any sampling error.

## POST-RUN DIAGNOSTIC, LABELLED AS POST-RUN — the λ clip runs AGAINST this run's own headline

λ is constrained to (0, 1], so a null draw already drier than the book enters unmatched at λ = 1
with its CAGR understated, which **inflates** EDGE. **The ELIG null is drier far more often than the
OPEN null: clip share 0.609 vs 0.344 on average, and ELIG clips more at 80 of 94 cells.** That
inflates `EDGE_ELIG` more than `EDGE_OPEN` and therefore pushes GATE **negative** — i.e. toward the
"every figure is a lower bound" conclusion this run is testing. **`H_LOWER` fails anyway, at 13
cells, several with the bias at its strongest** (U56 N=15/H=21: clip 0.000 OPEN vs 0.925 ELIG, GATE
still **+0.640 pp**). The bias is conservative for the failure and the failure survives it. It is
*not* conservative for the 81 negative cells, whose magnitudes are upper bounds on the true
understatement.

## RULE 8 AND BOTH KEEP PATHS

**EDGE is not a KEEP path, and this run's dial 2 cannot move one.** The book at every cell is
byte-identical across the two gates — only the comparand changes — so 4a and 4b are mathematically
invariant to the re-read. Both paths are scored at all 94 cells anyway because rule 4 requires it.

**Rule 8** — the cell chosen on IS 2009–2016 alone by four choosers, OOS 2017–2026 read once, 8
picks:

| panel | chooser | pick | OOS CAGR / Sharpe / MaxDD | 4b OOS |
|---|---|---|---|---|
| U56 | C_ISEDGE_ELIG | N=5 H=63 | 18.02% / 0.8998 / −26.26% | FAIL (O_DD) |
| U56 | C_ISEDGE_OPEN | N=5 H=63 | 18.02% / 0.8998 / −26.26% | FAIL (O_DD) |
| U56 | **C_ISSHARPE** | **N=12 H=21** | **17.57% / 1.1426 / −19.48%** | **PASS** |
| U56 | **C_ISDD** | **N=40 H=21** | **13.01% / 1.1286 / −19.27%** | **PASS** |
| B136 | C_ISEDGE_ELIG | N=5 H=63 | 20.46% / 0.9156 / −28.62% | FAIL (O_DD) |
| B136 | C_ISEDGE_OPEN | N=5 H=63 | 20.46% / 0.9156 / −28.62% | FAIL (O_DD) |
| B136 | C_ISSHARPE | N=5 H=63 | 20.46% / 0.9156 / −28.62% | FAIL (O_DD) |
| B136 | C_ISDD | N=40 H=63 | 13.89% / 0.9641 / −28.28% | FAIL (O_DD) |

`H_WF` **PASSES 2 of 8** — and note **both EDGE choosers, under either gate, pick the same losing
cell (N=5/H=63) on both panels and fail on the drawdown leg.** This reproduces 1082's and 1084's
reading from a third direction: **the EDGE ladder carries no out-of-sample selection information
that a plain IS Sharpe does not carry better.** Re-pricing it against the right null does not change
that.

Benchmarks: U56 SPY full 15.10% / 0.8829 / −33.72% (halves 0.9588 / 0.8207), OOS 15.21% / 0.8711 /
−33.72%; RULES v2 live full 8.62% / 1.2007 / −12.05% (halves 1.2322 / 1.1760), OOS 9.45% / 1.2762 /
−12.05%. B136 SPY full 15.16% / 0.8861 / −33.72% (halves 0.9596 / 0.8259), OOS 15.33% / 0.8767 /
−33.72%; RULES v2 7.98% / 1.0993 / −12.24% (halves 1.2348 / 0.9658), OOS 7.88% / 1.1059 / −12.24%.

**4a 0 of 94.** No cell clears the live book's drawdown — a book fact, not a null fact.
**4b full-sample 18 of 94, 4b out of sample 19 of 94, both 18 of 94.** **Nothing is proposed and no
memo is written.** Every one of the 18 is a cell the record already committed and already parked:
**8 are family A** (7 on U56 — including N=12/H=21, which 1086 published as the first
rule-8-reachable 4b pass in this family and parked on stated grounds, reproduced here at 8.88e-16,
and N=12/H=126 and N=20/H=126, which are 1082's own two parked passes — and 1 on B136, N=15/H=126,
1082's third); **10 are 1071's cap rungs** (5 on U56 at N=20, which are the same book to 0.01 pp,
and 5 on B136 at N=20/25). **They bind on drawdown by 0.01–1.45 pp against the 20.23% cap, and idea
1083 measured the 90% width of exactly that quantity at 4.1–7.2 pp on this tape.** This run
inherited those books; it did not find them, and re-pricing their nulls tells you nothing about
whether they are capital. They stay **PARKED**.

## SURVIVORSHIP (PROTOCOL rule 9)

U56 and B136 are CURRENT-CONSTITUENT panels. Every level here is optimistic and every 4a/4b count
is an UPPER bound. `EDGE_OPEN`, `EDGE_ELIG` and `GATE` are within-pool contrasts over the same tape
and the bias very largely cancels out of them; it does **not** cancel out of the 4b legs, which are
measured against SPY, a real index, so the 18 parked passes are flattered by it.

## ARTIFACTS

`...B.py`, `...B.console.txt`, and 8 CSVs: `.grid.csv` (94 × 57, every cell both gates),
`.ladders.csv` (34 committed ladders), `.census.csv` (1,019 `edge`-token units classified),
`.wide.csv` (the 52 WIDE units), `.rule8.csv`, `.gates.csv`, `.benchmarks.csv`, `.hypotheses.csv`.

**Follow-ups filed:** 1105 (a committed CSV key column that does not survive `pd.read_csv` — cost
this run a full re-run; idea 979's schema proposal with a price attached), 1106 (is the U56 H=21
sign flip a turnover fact — the gate's value to a random ordering should fall as the hold shortens),
1107 (re-price the record's committed ARGMAX claims on H and cap ladders, which 1097 shows are not
stable to the null gate).
