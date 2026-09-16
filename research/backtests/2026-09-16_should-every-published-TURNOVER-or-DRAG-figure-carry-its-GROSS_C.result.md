# Idea 1076 (lane C, 2026-09-16) — should every published TURNOVER or DRAG figure carry its GROSS?

**ANSWERED = YES, AND ALMOST NOTHING IN THE RECORD DOES.** 57 of 751 committed turnover/drag
figures (**0.076**) state a numeric gross within 200 characters of themselves; **23 of 751
(0.031)** state one in their own clause. Plus a **CORRECTION to this idea's own premise**: gross
does **not** scale turnover exactly linearly. Plus a **CONFIRM** of idea 930's reconciliation,
exact on the ladder medians. **No book proposed, no RULES change, no PROTOCOL edit (rule 6);
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.**

Script `research/backtests/2026-09-16_should-every-published-TURNOVER-or-DRAG-figure-carry-its-GROSS_C.py`,
8 CSVs, console log committed. **Gates 6 of 7. Hypotheses 4 of 6.**

---

## SELECTION

Lane C takes the SECOND open idea. Idea 1075 (first) went to lane A; 1076 is this run. Nothing
in its text touches EDGAR, Form 4, 8-K, options or live data, so it is eligible for the sandbox.

## THE TWO DIALS AND NO MORE (PROTOCOL rule 4)

**TUNED 1 — CLAIM SET**, 2 levels, both reported and never merged:
`STRICT` = a committed unit carrying a turnover/drag token AND a figure in a convertible unit
(`N bp/yr`, `Nx/yr`, "turnover … Nx", "drag … N bp"); `WIDE` = the token and ≥ 1 numeral.
**TUNED 2 — GROSS CONVENTION**, 3 levels, ALL reported: `AT100` (per unit of gross, 930's column),
`AT075` (the live book's gross), `LADMED` (median over the record's own {0.50, 0.75, 1.00}).

**REPORTED AXES, every point published:** stamp window {80 chars, 200 chars, whole unit};
source {LEADERBOARD, CHANGELOG, QUEUE, RESULTMD}; panel {U56, B136}; book {TOP5, TOP10, TOP20,
EWELIG, BAND03} — idea 930's own set, reused verbatim; cadence {D, W, M, Q}; gross ladder
{0.25, 0.50, 0.75, 1.00}, where 0.25 exists only to widen the linearity test and no verdict is
read off it.

## GATES — 6 of 7, printed before any result number

| | | |
|---|---|---|
| G1 | fast runner ≡ `engine.backtest` (returns AND turnover, 2 rungs) | **4.16e-16** PASS |
| G2 | cost linearity `net(c) == gross − turn·c/1e4` at 5 and 25 bps | **2.08e-17** PASS |
| G3 | SPY OOS triple vs committed (0.152102, 0.8711, −0.337173) | **2.98e-05** PASS |
| G4 | live RULES v2 full MaxDD vs committed −12.05% | **4.95e-05** PASS |
| G5 | CROSS-RUN `turn_yr` vs idea 930's committed `dragcurve.csv`, 90 shared cells | **3.55e-15** PASS |
| G6a | DECLARED DIRECTION: `turn(g)/g` decreasing in g | **40 of 40 cells** PASS |
| G6b | DECLARED MAGNITUDE: deviation < 1% | **5.31e-02** — **FAIL, published** |

G6 was declared in full before the numbers were read, including its mechanism: `engine.backtest`
renormalises the drifted row by `V = 1 + g·d`, `d` the drift P&L per unit of gross; `d > 0` on
average on this tape, so a larger `g` deflates the held row more and pulls it back toward target,
making `turn(g)/g` **decreasing** in g. **The direction was right on 40 of 40 cells. The size was
wrong** — the declaration said under 1% and it is 5.31%. Both halves are published as declared.

## THE CENSUS

Corpus **30,542 committed units** over 4 sources (LEADERBOARD.md rows; CHANGELOG.md paragraphs;
QUEUE.md lines; 856 `*.result.md` files, by paragraph). **2,309 carry a turnover-or-drag token;
751 carry a figure in a convertible unit.**

| claim set | window | n | numeric gross | share | (word-only, generous) |
|---|---|---|---|---|---|
| STRICT | 80 chars | 751 | 23 | **0.031** | 65 (0.087) |
| STRICT | 200 chars | 751 | 57 | **0.076** | 143 (0.190) |
| STRICT | whole unit | 751 | 126 | 0.168 | 262 (0.349) |
| WIDE | 80 chars | 2,309 | 214 | 0.093 | 520 (0.225) |
| WIDE | 200 chars | 2,309 | 248 | **0.107** | 598 (0.259) |
| WIDE | whole unit | 2,309 | 317 | 0.137 | 717 (0.311) |

By source (VALUED, 200-char window): LEADERBOARD **28 of 261 = 0.107**, RESULTMD **23 of 341 =
0.067**, QUEUE **6 of 149 = 0.040**. **CHANGELOG.md contributes ZERO** — as committed it is 6,054
bytes / 9 paragraphs (rotated to the latest entries) and carries no turnover figure at all, which
is itself worth knowing before any future run treats it as the record.

The bare word "gross" anywhere in the unit is the most generous reading anyone could defend, and
even it tops out at **0.349**. On the reading that actually pins a figure — a numeric gross in its
own clause — **96.9% of the record's turnover and drag figures are unconvertible as published.**

## THE RE-EXPRESSION

**694 unstamped valued figures** re-expressed under all 3 conventions × the record's own ladder as
the assumed measurement gross (148 in `bp/yr`, 546 in `x`). Medians of the `bp/yr` figures under
`AT100`: **50.00 / 33.33 / 25.00** if they were measured at g = 0.50 / 0.75 / 1.00; the `x`
figures: 9.95 / 6.63 / 4.97. Per-figure rows in `…_C.reexpress.csv`.

**Two things the dials revealed rather than measured, and both are results, not bugs.**
(i) **The WIDE claim set adds nothing to the re-expression**: 1,558 of the 2,309 turnover/drag
units carry the token and a numeral but no figure in a convertible unit, so WIDE's re-expression
rows are identical to STRICT's by construction — you cannot re-express a figure that was never
stated in a unit. (ii) **The record has TWO gross conventions here, not three**: `median{0.50,
0.75, 1.00} == 0.75 ==` the live book's gross, so `LADMED` and `AT075` coincide exactly.

## THE CORRECTION — gross is NOT an exact linear scale on turnover

This idea's own queue text says "gross scales turnover linearly". It does not, exactly.

* `max | (turn(g)/g) / turn(1.00) − 1 |` over 40 (panel × book × cadence) cells × 4 rungs =
  **5.312e-02**. Per rung: **@0.25 5.31%, @0.50 2.87%, @0.75 1.08%, @1.00 0** (H_LINEAR FAIL).
* Converting a figure with `v(g') = v(g)·g'/g` over all 480 ordered ladder pairs is wrong by up to
  **5.31%**; over the record's **own** ladder alone (240 pairs) up to **2.87%**, median **0.69%**
  (H_CONVERT FAIL).
* The worst cells are all `BAND03` **daily** — the lowest-turnover, highest-drift-between-decisions
  book, which is exactly where the `1 + g·d` renormalisation has the most room to bite.

**What the stamp is worth, in one line:** a turnover or drag figure published **without** its gross
is ambiguous by **exactly 2.000×** on the record's own ladder — a mechanical fact, not an estimate.
Published **with** it, the same figure converts to any other rung on that ladder to within
**2.87%** (median 0.69%). **The stamp removes a factor-of-two ambiguity and leaves a few-percent
one.** The few-percent residue is the reason the clause below asks for the gross the figure was
*measured* at rather than a normalised figure.

## H_930 — CONFIRM, and exact on the ladder medians

Read on idea 930's own grid (its 5 books, its W/M/Q cadences, its {0.50, 0.75, 1.00} ladder; the
daily rung this run added is excluded so the comparison is like for like):

| cadence | @1.00 median drag | 926's committed | | ladder median | 930's committed | |
|---|---|---|---|---|---|---|
| W | **168.5 bp/yr** | 161.0 | +4.7% | **109.6** | 109.6 | **−0.0%** |
| M | **74.0 bp/yr** | 73.0 | +1.3% | **48.9** | 48.9 | **+0.0%** |

By gross, W: @0.50 84.6 / @0.75 126.5 / @1.00 168.5 bp/yr. M: 37.3 / 55.7 / 74.0. 930's re-reading
of 926 reproduces **exactly**; 926's own figures reproduce inside the 5% bar (H_930 PASS).

## RULE 8 AND BOTH KEEP PATHS

Gross chosen on IS 2009–2016 by IS Sharpe alone, OOS 2017–2026 read once, 40 (panel × book ×
cadence) picks. Benchmarks — **U56: SPY full 15.10% / 0.8829 / −33.72% (halves 0.9588 / 0.8207),
OOS 15.21% / 0.8711 / −33.72%; RULES v2 live full 8.62% / 1.2007 / −12.05%, OOS 9.45% / 1.2762 /
−12.05%. B136: SPY full 15.16% / 0.8861 / −33.72%, OOS 15.33% / 0.8767 / −33.72%; RULES v2 full
7.98% / 1.0993 / −12.24%, OOS 7.88% / 1.1059 / −12.24%.**

**4b full-sample on the IS pick: 5 of 40. 4b OUT OF SAMPLE on the pick: 4 of 40. 4a: 0 of 40.
Whole ladder 4b: 11 of 160.** The four picks clearing 4b out of sample are U56 TOP20 weekly at
g = 0.75 (OOS 14.35% / 1.1246 / −18.31%) and U56 BAND03 daily / weekly / monthly at g = 1.00
(OOS 12.45% / 1.2868 / −14.77%, 12.67% / 1.2755 / −15.91%, 12.81% / 1.2243 / −18.81%).

**NOTHING IS PROPOSED.** The strongest of them — the live band construction at full gross — is
already committed in LEADERBOARD.md as `BAND03@g1.00`, OOS 12.68% / full 11.54%, a 4b pass
**refused on 4a for drawdown four times over**. This run reads **11.53% full / 12.67% OOS**:
agreement to 0.01 pp, reported as a cross-run check and not as a discovery. The 4b/4a columns
exist here because PROTOCOL rule 4 requires both paths scored on every run, not because this run
found a book.

## THE CLAUSE THIS RUN WOULD PROPOSE (text only — rule 6, not applied)

> Every published TURNOVER or DRAG figure states the GROSS it was measured at, as `@g`
> (e.g. `14.7x/yr @0.75`, `147 bp/yr @0.75`). A figure without one is read as unconvertible, not
> as `@1.00`. Where a figure is a summary over a gross ladder, it states the ladder.

Cost: six characters per figure. Benefit: 2.000× → 1.03× on the record's own ladder. Against 694
figures already in the record it is retrospective only in `…_C.reexpress.csv`, which gives each
one its three readings; no past claim can be repaired without its script.

## SURVIVORSHIP (PROTOCOL rule 9)

U56 and B136 are CURRENT-CONSTITUENT panels. The census half of this run is a statement about
committed text and is unaffected. The tape half — the drag levels, the linearity residual and the
rule-8 numbers — is flattered exactly as every other run on these panels is, and the 4b counts
above are upper bounds.

## FOLLOW-UPS FILED

Filed as 1084-1086, renumbered to **1087-1089** on push: a concurrent lane had
already taken 1084-1086 from idea 1082 (defect 932 again).

1087 (does the 1+g·d renormalisation bias any committed CADENCE claim, since it is largest on the
slowest books), 1088 (is CHANGELOG.md's 6 KB rotation silently shrinking every "the record"
census), 1089 (how many committed figures in units OTHER than turnover are per-unit-of-gross too).
