# Idea 681 (cloud) — how many of the record's 520 ASSERT CLAUSES are SELF-CONSISTENCY gates?

**Verdict: ANSWERED / THE SHARE IS NOT A SINGLE NUMBER — it spans 6.15% to 62.30% across the
classifier dial and is FLAT across the sample dial.** Headline reading (MID) **191 of 520
(36.73%)**. No KEEP, no book promoted, no memo, no rule change. `RULES.md`, `PROTOCOL.md`,
`scan.py`, `bot.py`, `baseline.py` untouched.

Script: `2026-09-11_how-many-of-the-record-s-520-ASSERT-CLAUSES-are-SELF-CONSISTENCY-gates_cloud.py`
Artefacts: `.clauses.csv` (520 rows, one per clause, all three classifiers), `.grid.csv` (9 grid
points), `.byform.csv`, `.i516.csv`, `.reached.csv`, `.keeppaths.csv` (30 arms), `.walkforward.csv`,
`.vintage.csv`, `.console.txt`.

## Parameters (two, as the queue allows; every grid point reported)

* **P1 classifier**, 3 nested strictnesses for what counts as a COMMITTED CONSTANT (the artefact
  rule is identical at all three; an ordering-comparison numeric operand is a BAR, never a value,
  at all three): **WIDE** (any literal |v| ≥ 1e-2 anywhere in the value-side closure), **MID**
  (headline — such a literal in expected-value position: operand of `-` or `/`, or comparand of
  `==`/`!=`), **NARROW** (MID and the literal is non-integral, i.e. carries hand-copied decimals).
  NARROW ⊆ MID ⊆ WIDE; the nesting is asserted and holds on 0 violations.
* **P2 sample**, 3 nested script subsets ordered by `md5(filename)`: S38 ⊂ S76 ⊂ S151 (S151 = the
  whole census).

Dataflow depth (6), the 1e-2 constant floor and the INPUT/ARTEFACT path rule are FIXED, stated,
and not swept. Nothing is tuned on an outcome. Deterministic: `PYTHONHASHSEED=1` and `=2` give a
byte-identical `.clauses.csv` (`d44b683b…`) — the first draft was **not** deterministic (set
iteration order), which is recorded here rather than quietly fixed.

## Method — why the clause source alone cannot answer this

Most of the record's clauses read `g1 < 1e-09` or `d3b / max(tot3b,1) < 1e-4`: the interesting
side is a local variable. So the classifier is an **AST dataflow closure**. For each clause the
ordering BAR is stripped, every `Name` on the remaining value side is resolved back through the
producing script's own assignments (depth 6, cycle-guarded, deliberately over-approximating by
unioning every assignment to a name anywhere in the file), and the leaves are tagged.

**The correction that matters.** A read call is only a REPRODUCTION leg if it brings in a *prior
run's output*. Reading `data/prices.csv`, `data/small_meta.csv` or `research/universe.json` is an
**INPUT both sides of the gate share** — it moves under both sides identically, so the gate stays
self-consistent. Path expressions are resolved the same way and split INPUT (29 clauses) from
ARTEFACT (174) / ARTEFACT|INPUT (5) / unresolved (4). Treating panel reads as reproduction legs
(the first draft) inflates the artefact class by ~30 clauses; the split is published so the reader
can undo it.

520 of 520 clauses were located in source (488 at the exact recorded expression, 32 at the
enclosing `assert`); 0 unreadable.

## Reproduction gates (recorded, non-raising — the point of this idea is that a raising gate hides what is behind it)

All eight PASS: idea 515's published **520 / 345 tolerance / 87 exact / 46 structural / 40 count /
151 scripts**, and idea 516's **36 re-executed / 35 moved**. These are REPRODUCTION gates by this
script's own definition (one side is a committed artefact), which is the point.

## [A] The answer, all nine grid points

| sample | classifier | SELF | CONST | ARTEFACT | share_self |
|---|---|---|---|---|---|
| S38 (170 clauses) | WIDE | 14 | 98 | 58 | 0.0824 |
| S38 | MID | 63 | 49 | 58 | **0.3706** |
| S38 | NARROW | 103 | 9 | 58 | 0.6059 |
| S76 (305) | WIDE | 19 | 181 | 105 | 0.0623 |
| S76 | MID | 113 | 87 | 105 | **0.3705** |
| S76 | NARROW | 190 | 10 | 105 | 0.6230 |
| S151 (520, full) | WIDE | 32 | 305 | 183 | 0.0615 |
| S151 | MID | **191** | 146 | 183 | **0.3673** |
| S151 | NARROW | 314 | 23 | 183 | 0.6038 |

**The sample dial is flat and the classifier dial is a factor of 9.8.** Across the three nested
samples the share moves by ≤ 0.019 at every classifier; across the three classifiers it moves from
0.0615 to 0.6038 on the same 520 clauses. So the queue's question — "the share of the record's
gating that is structurally blind to vintage" — **has no single answer until the constant rule is
named**, and any future citation of a number from this run must carry its classifier.

By FORM at MID (full census): **count 0/40 self (0.0000)** — every count clause compares against an
artefact's row count and is a genuine reproduction gate; tolerance 127/345 (0.3681); exact 43/87
(0.4943); structural 20/46 (0.4348); floor 1/2. **36 of 151 scripts (23.84%) have EVERY clause
self-consistency** — those are the files whose gates cannot, even in principle, see a panel move.

## [B] The mechanism, tested where idea 516 measured it

Only **13 of idea 516's 36 re-executed scripts carry census clauses at all** (41 clauses) — idea
515's census covers the 158 *gated* scripts and idea 516 sampled the 60 rc=0 files, so the overlap
is thin and this leg is **descriptive, not a test**. On those 41: SELF 13, CONST 7, ARTEFACT 21
(share_self 0.3171), essentially the corpus rate. Cut by idea 516's own `cause`: PANEL DRIFT 40
clauses / 12 scripts / share_self 0.325.

**[B2] is the stronger leg.** Joining this classification onto idea 515's recorded
`(observed, bar, passed)` for the **171 clauses that were actually reached**: pass rate
**SELF 0.9403 (n=67) > CONST 0.9074 (n=54) > ARTEFACT 0.7200 (n=50)**. The ordering is monotone and
in the predicted direction: the gates that can see outside their own run are the gates that fail.
That is the mechanism behind idea 516's "36 of 36 pass while 35 of 36 move" stated as a rate
rather than a count. It is an association on 171 clauses, not a controlled contrast: artefact
gates also tend to be the strictest, and this run does not separate the two.

## [C] PROTOCOL leg — rule 8, both KEEP paths, and what the blindness is worth

U56 (56 instruments, 2008-01-02 → 2026-09-10), 30 band × gross arms, **10 bps, weekly, t+1**,
metrics from 2009-01-13.

* Comparands: **RULES v2** CAGR 8.61%, Sharpe 1.1998, MaxDD −12.05%, H1/H2 1.235/1.172.
  **SPY** CAGR 15.11%, Sharpe 0.8835, MaxDD −33.72%, H1/H2 0.960/0.821; OOS Sharpe 0.8721,
  CAGR 15.24%, MaxDD −33.72%.
* **4a: 0 of 30 arms pass.** Every arm loses the MaxDD leg or a half to RULES v2 (best margin
  −0.0257). **4b: 15 of 30 pass**, all of them at gross ≥ 0.95 — the CAGR floor is what the low
  grosses miss, replicating the record's standing gross-window result.
* **Rule 8** (band chosen on 2009-2016 alone by IS Sharpe, 2017-2026 read once): band **0.08** at
  every gross. OOS Sharpe **1.1611–1.1634 vs SPY 0.8721** at OOS CAGR 6.56%–13.21% vs SPY 15.24%
  and OOS MaxDD −10.71%..−20.85% vs SPY −33.72%. **4b passes at g = 0.95 and 1.00 only; 4a at
  none.** The walk-forward pick is stable in gross, which is the useful part.
* **The vintage step.** Every arm re-run on the panel truncated 2 trading days (2026-09-08, the
  APPEND channel; the restatement channel is not reachable offline): **max |ΔSharpe| 4.51e-03,
  max |ΔCAGR| 5.50e-04, max |ΔMaxDD| exactly 0.00e+00, and 0 of 30 4a and 0 of 30 4b verdicts
  flip.** Every one of those deltas is invisible to a self-consistency gate by construction — the
  gate recomputes *both* of its sides on the moved panel.

**So the blindness is real and, at this step size, cheap.** Two trading days move a published
Sharpe by ~4e-3 and move zero verdicts on these 30 arms; the zero ΔMaxDD replicates idea 518's
vintage-inert DD leg (every arm's worst drawdown sits in 2020/2022). Idea 516's 20 4a and 11 4b
row-level flips came from a corpus 5,000× larger, not from a larger per-arm delta.

## Caveats

Panel reads are classified INPUT by a path regex, not by resolving the file: 4 clauses could not
be resolved either way and are counted ARTEFACT (conservative against the headline). The dataflow
closure over-approximates (every assignment to a name anywhere in the file), which biases toward
REPRODUCTION and therefore *understates* share_self at every classifier. The 1e-2 constant floor
separates published numbers from tolerances by magnitude alone and will misread a hand-copied
number below 1e-2. [B] is an overlap of 13 scripts. SURVIVORSHIP (idea 54) applies to every panel
in the record. No RULES change proposed or taken.
