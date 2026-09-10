# Idea 620 — is lambda INERT on every LOW-TURNOVER book, or only on EWALL? (lane C, 2026-09-10)

**VERDICT: SPLIT. The queue's question is ANSWERED and its own framing is REFUTED. Lambda is
inert on EXACTLY ONE book in the whole run — the fully un-ranked one at coverage `c = 1.00` — and
the inertness is a KNIFE-EDGE, not a property of low-turnover books. The mechanism is named,
measured and LINEAR. Nothing promoted, no RULES change, no memo: the run's one 4b passer is
killed as an idea-311 g-band artefact by this file's own gross ladder. RULES.md, PROTOCOL.md,
scan.py, bot.py and baseline.py untouched.**

Script: `2026-09-10_is-lambda-INERT-on-every-low-turnover-book-or-only-on-EWALL_C.py`.
Outputs: `.console.txt`, `.grid.csv` (6,000 rows), `.reach.csv`, `.thresholds.csv`,
`.driver.csv`, `.walkforward.csv`, `.gross.csv`. Runtime 346 s, deterministic.

Two tuned parameters as PROTOCOL rule 4 allows, exactly the two the queue names: **n** (book
concentration, run in BOTH of its natural units — absolute `n` and coverage `c = n/n_scored`,
idea 590's point) and **lambda** (idea 137's ladder, verbatim). Panels (u56 / broad136 /
small439), the three un-ranked control books, cadence (D, W) and the five cost rungs are
REPORTED axes, never selected on. Every grid point is reported. The only selection in the file
is PROTOCOL rule 8.

## Gates — all pass, before any new number was read
* **G1** the vectorised segment runner vs `engine.backtest` on returns AND turnover at D and W,
  all three panels: max |dr| **6.4e-16**, max |dturnover| **3.3e-16**.
* **G2** the rung identity `r(c) = r(0) − turnover·c/1e4` vs a live `engine.backtest(25)`:
  **6.4e-16 / 6.3e-16 / 6.1e-16**.
* **G3** the n-ladder's ALL endpoint (equal weight over SCORED names) vs idea 412's own EWALL
  (equal weight over PRICED names), REPORTED rather than asserted: turnover 0.8248 vs 0.8288
  (u56), 0.8620 vs 0.8657 (broad), 1.7289 vs 1.7409 (small); max |dr| ≤ **3.8e-03**. The two
  definitions differ only on names that are priced but not yet scorable, and the difference is
  far too small to touch any finding below.
* **G4 REPRODUCTION** — idea 412's committed `.grid.csv` EWALL and TOP20 turnovers re-derived
  from its own book definitions on its own k=5/phase=0 grid, 48 cells, all three panels, all
  eight lambdas: worst |d turnover| **1.776e-15 x/yr**. Idea 412's numbers are reproduced
  exactly; everything below is built on top of them, not against them.
* **G5** monotone down in width: **1 of 96** cells, worst wrong-way step 9.2e-04. Monotone down
  in lambda: **5 exception cells, every one listed** — and all five are DE-GROSSED control cells
  (see FINDING 4), not noise.

## FINDING 1 — the inertness is a knife-edge at c = 1.00, not a low-turnover effect
Absolute `n` cannot answer the queue's question, because a ladder in absolute n stops short of
the panel by construction (its widest rung on u56 is 40 of ~54 scored names). Run in the second
unit of the same dial, coverage `c`, the ladder reaches the un-ranked book **continuously** — and
the collapse turns out to occupy the last one percent of it:

| panel | cad | rung | base turnover | raw-target churn | lambda reach | drag saved @10bps |
|---|---|---|---|---|---|---|
| u56 | D | c0.99 | 2.7327 | 1.0880 | **0.9088** | **9.09 bps/yr** |
| u56 | D | c1.00 | 1.7647 | 0.0113 | **0.0053** | **0.05 bps/yr** |
| broad | D | c0.99 | 2.2768 | 0.5084 | **0.4184** | **4.18 bps/yr** |
| broad | D | c1.00 | 1.8335 | 0.0093 | **0.0029** | **0.03 bps/yr** |
| small | D | c0.99 | 4.1351 | 0.5935 | **0.4913** | **4.91 bps/yr** |
| small | D | c1.00 | 3.6592 | 0.0583 | **0.0145** | **0.14 bps/yr** |

**Dropping the worst 1 % of names multiplies the dial's reach by 33x–171x** while base turnover
moves by less than 1.6x. The pre-registered threshold ladder puts the crossings at (widest
coverage still meeting the bar, all 6 panel x cadence cells): **≥ 1 bps/yr at c = 0.99
everywhere**; ≥ 5 bps/yr at c = 0.95–0.99; ≥ 10 bps/yr at c = 0.90–0.98; ≥ 25 bps/yr at
c = 0.65–0.95. There is no gradual "usable threshold" in n to report — the honest answer to the
queue is that **the dial is usable on every book the record actually trades and dead on exactly
one degenerate book.**

## FINDING 2 — the mechanism, and it is linear
Lambda is an EWMA of the raw target. What it can remove is therefore a fixed fraction of what the
raw target does — not of what the book trades. Define `rawchg` = annualised L1 churn of the raw
target and `eff = reach / rawchg`:

* **eff = 0.8358 ± 0.0311 at cadence D and 0.2653 ± 0.0153 at cadence W**, over all 36 coverage
  cells from c = 0.02 to c = 0.99 (12 rungs x 3 panels). A near-constant, cadence-specific
  coefficient across a ladder on which base turnover itself moves by more than 15x.
* The partial correlations say the same thing. On the coverage ladder, `rho(reach, base
  turnover) = +0.987` and `rho(reach, rawchg) = +0.998`, but controlling for churn the base-
  turnover partial collapses to **−0.002 (D) / +0.346 (W)** while the churn partial holds at
  **+0.918 (D) / +0.931 (W)**.
* At **matched base turnover** (~7 x/yr, cadence D) reach still splits by churn, not by turnover:
  u56 COVER c0.90 (base 6.71) reaches 4.46, u56 MA (base 6.91) reaches 1.60.

**EWALL is not inert because it is diversified, un-ranked, or low-turnover. It is inert because
an equal weight over a near-constant membership is a near-constant matrix, and the EWMA of a
near-constant matrix is that matrix.** `rawchg` on the un-ranked books is 0.0093–0.0583 x/yr.

## FINDING 3 — the decisive control: an UN-RANKED book with the LARGEST reach in the run
`MARS` is equal weight over every scored name above its own 200d MA, **re-spread to a constant
gross of 0.75**. It is maximally un-concentrated (n = ALL, zero ranking) and its gross never
moves; only its membership churns. It is the cell that separates the queue's two candidate
explanations, and it separates them completely:

| book (all n = ALL) | gross | base turnover | rawchg | reach | drag @10bps |
|---|---|---|---|---|---|
| RANKN ALL (= EWALL) | 0.750 | 1.76 | 0.011 | **0.005** | 0.05 bps/yr |
| BAND (de-grossed) | 0.535 | 2.48 | 1.384 | **0.000** | 0.00 bps/yr |
| MA (de-grossed) | 0.536 | 6.91 | 5.885 | **1.596** | 16.0 bps/yr |
| **MARS (constant gross)** | 0.750 | 18.11 | 17.538 | **14.656** | **146.6 bps/yr** |

(u56, cadence D; broad and small give 14.45 / 18.50 for MARS.) **The book with zero
concentration has the biggest lambda reach in the entire 6,000-row grid** — larger than any
top-n book on any panel. Both of the queue title's candidate explanations are refuted by this
one row.

## FINDING 4 — a CORRECTION the record needs: on a de-grossed book the dial can RAISE turnover
Idea 137's `smooth` restores the raw target's gross after the EWMA, so on a book whose gross
itself swings the smoother fights its own rescaling. All five monotonicity exceptions are
de-grossed control cells, and two of them are not marginal:

| panel | book | cad | worst wrong-way step | total rise above base |
|---|---|---|---|---|
| u56 | BAND | D | +0.1813 | **+0.4739 x/yr** |
| u56 | BAND | W | +0.0537 | +0.1538 x/yr |
| broad | BAND | D | +0.1154 | +0.2466 x/yr |
| broad | BAND | W | +0.0333 | +0.0635 x/yr |
| u56 | MA | W | +0.0270 | +0.0392 x/yr |

On u56 BAND the dial's downward reach is **exactly 0.0000** at both cadences: every lambda < 1
trades MORE than lambda = 1. **"Lambda lowers turnover" is false on a de-grossed book**, which is
the book form RULES v2 itself uses. Any future use of the dial on a cash-sleeve book must state
its direction rather than assume it.

## Idea 621's NO-DIAL column, back-filled
| menu | median OOS Sharpe | median OOS CAGR | median OOS MaxDD | beats RULES v2 | beats SPY |
|---|---|---|---|---|---|
| JOINT (n, lambda) | 0.9258 | 20.89% | −30.56% | 20/60 | 35/60 |
| NONLY (lambda = 1) | 0.9417 | 13.81% | −28.90% | 26/60 | 36/60 |
| **LAMONLY (n = 20)** | **0.9766** | 15.95% | −26.42% | 20/60 | 36/60 |
| **NODIAL control** | **0.8079** | 12.78% | −26.98% | 14/60 | 25/60 |

SPY OOS Sharpe 0.876–0.882 / CAGR 15.32–15.45% / MaxDD −33.72%; RULES v2 OOS Sharpe 0.406–1.303
/ CAGR 2.66–9.68%. **LAMONLY beats the no-dial control in 47 of 60 cells, median dSharpe
+0.0764** — the opposite of idea 412's 15/36 and median −0.0001, and FINDING 2 says why: idea
412's LAMONLY anchor was EWALL in half its cells, where the dial has no instrument at all. Once
the anchor is a ranked book in every cell, the dial earns its keep against no dial.

**It does not earn a SECOND parameter.** JOINT beats LAMONLY in only **18 of 60** cells (median
−0.0380) and NONLY in 28 of 60 (median −0.0264). Rule 8's answer is one dial, and lambda is a
defensible choice of the one — a strictly stronger statement than idea 412 could make, and
consistent with it rather than against it. The two units of the concentration dial agree on
lambda in 21 of 30 cells (median |d lambda| 0.000), so idea 590's unit worry does not bite here.

## KEEP paths — both, priced on all 6,000 rows
* **4a: 5 / 6,000.** Three are u56 BAND at lambda = 1, i.e. very nearly `rules_v2_weights`
  compared against itself (they differ only in excluding unscored names) — idea 582's degenerate
  control, reported as such and not counted as a result. The other two are small MA at
  lambda = 0.06 and 0/5 bps only.
* **4b: 79 / 6,000, and every single one is the MARS control at 0–10 bps on u56 (43) and broad
  (22 at 0–25 bps).** Lambda = 1.00 passes alongside every lambda < 1, so **not one of the 79 is
  attributable to this run's dial.**
* **BOTH: 0 / 6,000.** By rung: 0 bps 4a 2 / 4b 22; 5 bps 1 / 22; 10 bps 0 / 21; 25 bps 1 / 11;
  50 bps 1 / 3. Binding 4b bar over all rows: DD 3,095, H2 1,116, OOS 1,102, CAGR 349, H1 338.

### The one 4b passer is KILLED by this file's own gross ladder (idea 311)
MARS at gross 0.75, weekly, 10 bps reads u56 CAGR 11.50% / Sharpe 1.088 / MaxDD −18.65% /
H1 1.170 / H2 1.028 / OOS 1.107, against 4b bars of CAGR ≥ 10.61%, MaxDD ≤ 20.23% and SPY
H1 0.959 / H2 0.826 / OOS 0.876. It passes — on margins of **0.0089 (u56, CAGR bar)** and
**0.0011 (broad, DD bar)**. Idea 311 found 98.1 % of the record's committed 4b passes were never
run at a second gross, and 97.6 % of those that were flip. So this run swept it, 17 rungs from
0.50 to 1.30, every point in `.gross.csv`:

* **5 of 68 (panel x cadence x gross) cells pass at 10 bps.**
* u56 W: admissible band **[0.70, 0.80]** — 3 of 17 rungs. broad W: **[0.70, 0.75]** — 2 of 17.
* **u56 D and broad D: the admissible band is EMPTY.** The same book at the same gross fails at
  daily cadence.

The margin peaks at g ≈ 0.70–0.75 and falls away in both directions because the CAGR floor pushes
gross up and the DD cap pushes it down. **This is exactly idea 311's g-band loophole and idea
138's narrow window, so the passer is recorded as an ARTEFACT, not a KEEP-candidate. No memo is
written and nothing is PARKed.** MARS is in any case the record's existing MA-RS book form, not a
new one, and it is a control introduced by this file rather than the idea's own dial.

## Caveats carried
SURVIVORSHIP (idea 54): current constituents on all three panels; SMALL439 drops the 44 tickers
with `max_1d_move >= 1.0`. Idea 126: t+1 execution, no lag band. Idea 38: u56/broad carry the
calendar-day index. Idea 321: MaxDD is one number off one path and the 4b DD cap turns on exactly
that number. Cadence is CLOSED at the record's own D and W conventions so that idea 412's phase
nuisance cannot enter a run about a different dial; the reach numbers are therefore
cadence-conditional, and the D/W gap in `eff` (0.836 vs 0.265) is itself reported rather than
averaged away.

## What the record should take from this
1. **Lambda's reach is `eff x rawchg`, not a book-quality statistic.** Any file proposing the
   dial should publish the book's raw-target churn beside it; a book with churn under ~0.1 x/yr
   has no dial and a rule-8 pick of lambda there is a no-op.
2. **Idea 412's "lambda is inert on the un-ranked book" is correct and mis-generalised.** It is
   inert on the un-ranked CONSTANT-MEMBERSHIP book. An un-ranked book with churn (MARS) carries
   the largest reach in this run.
3. **On a de-grossed book the dial can be turnover-increasing** — direction must be stated.
4. **Idea 621's no-dial control changes the reading**: lambda beats it 47/60 once the anchor book
   has reach, but the joint two-parameter chooser still loses to both singles 18/60.
