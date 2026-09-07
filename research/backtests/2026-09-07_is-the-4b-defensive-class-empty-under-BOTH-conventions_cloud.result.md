# Idea 397 — is the `4b-defensive` class empty under BOTH conventions?

**Cloud, 2026-09-07.** Script `2026-09-07_is-the-4b-defensive-class-empty-under-BOTH-conventions_cloud.py`,
console `…console.txt`, grid `…grid.csv` (1,632 rows), members `…members.csv` (531),
gap decomposition `…gap_by_factor.csv`, walk-forward `…walkforward.csv` (84 rows),
selectors `…selectors.csv`.

## Verdict — **ANSWERED, and the queue's own deletion trigger does NOT fire: AMEND, do not delete.**
The intersection is **65 of 531 members (12.2%)** — not near-empty — and the reason is the
cleanest possible one: **the matched-GROSS bar is strictly harder than the matched-DRAWDOWN bar,
and its survivors are a perfect subset of the drawdown convention's, 65 of 65, 0 exceptions.**
The two conventions are not two independent tests that happen to disagree; they are one test at
two strictnesses. So the class does not need deleting — it needs PROTOCOL to **name the strict
convention**, at which point the recorded class *is* the intersection.

No RULES change, no book promoted, no KEEP claimed. RULES.md, scan.py, bot.py, baseline.py and
PROTOCOL.md untouched.

## Reproduction (nothing new was read until these passed)
- The whole corpus was rebuilt from source with idea 135 _B2's own harness: **1,632 of 1,632
  rows matched its COMMITTED grid**, max |diff| **3.55e-15** over CAGR / Sharpe / MaxDD / H1 / H2 /
  IS / OOS / gross / m / turnover / every ladder column, and **0 boolean mismatches** across
  `pass4b`, `floor_only`, `IS_floor_only`, `pass4a`, `pass4a_v2`, `D1`, `D2`, `D3`, `D4`,
  `D1_IS`, `D1_OOS`, `D1_raw`, `lad_pass4b`.
- idea 135's published headline rates re-derive on the rebuild: members **531** (published 531),
  **D1 12.2%** (12.2%), **D2 19.8%** (19.8%), **D4 58.9%** (58.9%).
- Self-identity gate: the ungated `control` arm is its own matched-gross ladder point —
  max |dSharpe| **1.12e-14** over 96 control rows.
- LIVE RULES v2 reproduces exactly: u56 @10 bps **8.66% / 1.2056 / −12.05%**.
- One restatement correction, not a mismatch: idea 135's memo publishes the MaxDD clause alone as
  **411 / 77.4%**, which is the `dMaxDD >= 0` form. At this run's 1e-9 tolerance the same clause
  reads **417 / 78.5%**, and the strict `> tol` form (the committed `D3` column, which matched at
  0 mismatches) reads **374 / 70.4%**. Three numbers, three tie conventions, same rows — which is
  idea 135's own point that a bare `>` on a dominance bar is not well posed.

## (1) The deliverable — the 2x2 on the same 531 rows

|  | D4 pass (matched DD) | D4 fail | total |
|---|---|---|---|
| **D1 pass (matched gross)** | **65** | **0** | 65 |
| D1 fail | 248 | 218 | 466 |
| total | 313 | 218 | 531 |

- **BOTH 65/531 = 12.2%**, EITHER 58.9%, NEITHER 41.1%.
- **NESTING IS EXACT: 0 of 65** matched-gross survivors fail the matched-drawdown bar.
- phi(D1, D4) = **0.312**; under independence BOTH would be 38.3 rows, observed 65.
- D4 is **UNDEFINED for 37 of 531 (7.0%)** — the arm's MaxDD falls outside its own ladder's
  drawdown range. Those are scored as D4 failures above; on defined rows only D4 = 313/494 =
  **63.4%**. No row is silently discarded.
- **Materiality of the 65.** Median dSharpe over their matched-gross control **+0.0152**
  (42 rows > 0.01, 9 > 0.05, **0 > 0.10**); median dCAGR at matched drawdown **+1.21 pp/yr**
  (all 65 > 0.10). The intersection is real but thin on the Sharpe axis and thick on the CAGR
  axis — the two conventions are not measuring the same size of effect.

## (2) The 4.8x convention gap: uniform by panel, graded by book, **owned by one arm kind**
The gap is the 248 rows the drawdown convention admits and the gross convention does not (46.7%
of members). Leave-one-level-out on the pooled gap rate, every level reported:

| factor | pooled gap 46.7 pp falls to | worst single deletion removes | levels positive | spread |
|---|---|---|---|---|
| **kind** | **24.5 pp (drop `gate`)** | **22.2 pp** | 3/5 | 61.0 pp |
| cost | 42.0 (drop 10 bps) | 4.7 pp | 2/2 | 8.7 pp |
| book | 42.8 (drop SLV50) | 3.9 pp | 6/6 | 28.8 pp |
| gross_mode | 44.1 (drop native) | 2.6 pp | 3/3 | 11.9 pp |
| **panel** | 46.3 (drop broad) | **0.4 pp** | 2/2 | **1.0 pp** |

- **It is not one book** (all 6 positive, 27.3–56.1 pp) and **not a panel fact** (u56 46.3 vs
  broad 47.3 — a 1.0 pp spread across the axis the record usually finds ordered).
- **It is concentrated in one arm kind.** `gate` carries **197 of 248 gap rows (79.4%)** on 60.8%
  of members (lift **1.31**), and deleting it nearly halves the pooled gap.
- **Two kinds generate no gap at all, for the same reason:** `stop` **0 of 59** and `ctl` 0 of 29
  clear *either* bar. The trailing-stop family fails the matched-gross AND the matched-drawdown
  control — idea 396's premise, confirmed from the second convention as well.

## (3) Mechanism — the conventions pick different points of the *same* ladder
Matched gross puts the control at mean ladder m **0.809**; matched drawdown puts it at
**0.685**, and de-grosses it *further* in **374 of 494 rows (75.7%)**. Members are shallower than
their matched-gross control by **+2.08 pp** of MaxDD while surrendering **−1.03 pp** of CAGR, so
the drawdown convention has to buy that depth back out of the control's exposure, which costs the
control CAGR. **The extra 248 admissions are that de-grossing, not a property of the instruments**
— on the gap rows the mean dSharpe against the matched-gross control is **−0.0511**, i.e. the
rows the weak bar admits are exactly the ones that lose on the strong one.

## (4) Both KEEP paths, all 1,632 rows
- **4a vs the LIVE book (RULES v2): 23 of 1,632 (1.4%)** — all broad, all sleeve books, best
  `broad/SLV50/ddctl-8/.5/recover @10 bps m75` 8.1% / **1.289** / −11.8% (halves 1.316/1.280,
  OOS 1.323). Against RULES v1, for continuity with the pre-v2 record: 784/1,632.
- **4b vs SPY: 144 of 1,632 (8.8%)**; of them D1 **19.4%**, D4 79.2%, BOTH 19.4%.
- **0 rows pass both paths.** No new KEEP from this idea. The standing candidate is untouched.
- SPY: full 15.23% / MaxDD −33.72% / halves 0.957/0.834; OOS 15.45% / 0.882 / −33.72%.
  RULES v2 OOS Sharpe u56 1.267, broad 1.096.

## (5) Rule 8 — the intersection is the best *screen* and still not a *selector*
Parameters chosen on 2009–2016 alone, 2017–2026 read once; 12 cells (2 panels x 2 rungs x 3 gross
modes), each pooling all 8 books.

| selector | cells with a pick | mean OOS Sharpe | mean OOS CAGR | mean OOS MaxDD | beats SPY | beats v2 | mean OOS rank |
|---|---|---|---|---|---|---|---|
| S0 no screen | 12 | 1.109 | 14.4% | −20.8% | 12 | 6 | 48.8 |
| S3 class (idea 133) | 12 | 1.233 | 9.1% | −14.3% | 12 | 8 | 15.9 |
| S5 = S3 + D1_IS | 9 | 1.260 | 8.0% | −12.4% | 9 | 8 | 12.7 |
| S8 = S3 + D4_IS | 12 | 1.218 | 8.7% | −14.0% | 12 | 8 | 19.5 |
| **S9 = S3 + BOTH** | **8** | **1.279** | 8.1% | −12.5% | 8 | 8 | **4.5** |
| S6 D1_IS alone | 12 | 1.115 | 13.4% | −19.5% | 11 | 6 | 49.5 |
| S10 D4_IS alone | 12 | 1.110 | 13.6% | −19.8% | 11 | 6 | 50.3 |

Paired against S3 on the cells where both pick: **S9 moves 1 pick of 8 for +0.0080 mean OOS
Sharpe and abstains in 4 of 12 cells**; S5 moves 2 of 9 for +0.0009; S8 moves 2 of 12 for
−0.0142. **Neither ladder screen is worth anything on its own** — S6 −0.1172 (6 of 12 picks
worse) and S10 −0.1226 (6 worse, 0 better) against S3. The class restriction earns the OOS
Sharpe; the ladder bar, in either convention, only removes rows.

**The IS window breaks the nesting.** On 2009–2016 alone D1_IS admits 32 members and D4_IS 177,
but **5 of those 32 fail D4_IS** — the perfect subset relation is a full-sample fact and does not
hold on the ruler rule 8 actually chooses on (idea 128: the IS window cannot express deep
drawdowns, and the two conventions weight drawdown differently).

## What PROTOCOL should say (proposed, not adopted here)
Record a `4b-defensive` row only if it beats **its own book's matched-MEAN-GROSS ladder point**
on Sharpe at no worse drawdown, at an explicit **1e-9** tolerance. Naming that convention is
sufficient: it is the strict one, its survivors are a subset of the drawdown convention's, and
the class it defines is the 12.2% intersection this run measured. Adopt it as a **recording**
rule, not as a selector — S9's OOS gain over S3 is +0.008 of Sharpe on one moved pick in eight,
bought at 4 abstentions of 12.

## Caveats carried
Survivorship (idea 54) inflates the fully invested ladder control most, so both controls are hard
tests — which runs against this run's finding, not for it. Idea 128: every IS-window drawdown
clause is measured on a ruler that cannot express deep drawdowns, and section (5) shows that
biting. MaxDD is one number off one path; D1 tie-breaks on it and D4 is defined entirely by it.
Matched-gross and matched-drawdown ladder points are not the same instrument as the m=1 book and
are never quoted as one. Idea 38's calendar-day index applies identically to an arm and to both
of its controls. The small panel is excluded because idea 133 (0 floor-only of 612) and idea 136
(0/180) leave no member there to price.
