# Idea 881 — is the ONE-SIDED DISPERSION defect a MAX-RUN-LENGTH fact or a TAIL-MASS fact?

**Lane B, 2026-09-15. ANSWERED: IT IS A MAX-RUN-LENGTH FACT, and the deciding pair holds the
illegal tail mass FIXED to 0.002 while changing only the maximum. Splitting the SAME over-long days
into two runs instead of one removes 82% of idea 875's −0.0046. At a legal maximum a 3.07×
dispersion difference moves the statistic by 0.00044, half the measured noise band.
BUT BOTH PRE-REGISTERED HYPOTHESES PRINT REFUTED ON THEIR OWN BARS, and 875's stated MECHANISM is
FALSIFIED. KILL for capital — nothing here is a book. A PROTOCOL amendment is PROPOSED, NOT APPLIED
(rule 6). RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched.**

Script: `2026-09-15_is-the-ONE-SIDED-DISPERSION-defect-a-MAX-RUN-LENGTH-fact-or-a-TAIL-MASS-fact_B.py`
Outputs: `.arms.csv` (1,152) `.excess.csv` (11,520) `.gap.csv` `.contrast.csv` `.mechanism.csv`
`.walkforward.csv` `.books.csv` `.console.txt`

## What was run

1,152 real gate arms (8 families × q{0.07,0.12,0.17} × w{252,1008} × depth{0.50,1.00} ×
cadence{D,W} × gross{0.75,1.00} × panels U56 / B136 / SMALL-664) × **10 nulls** × **20 md5 seeds** ×
3 cost rungs = 691,200 placebo cells, every grid point printed and written to the CSVs. The axis set
is idea 875's verbatim so G3 is an agreement bar. Seed budget raised 10 → 20 because 875 measured
its own per-arm resolution limit at 10 seeds to be ≈0.02 of Sharpe, 4× the effect being split here.

Six nulls are new. All preserve the real arm's firing-day count *k* and run count *m* **exactly**, so
the switch count and the entire switch-cost term are identical to BLOCK's, and they share 871's gap
draw, so the fire-run **shape** is the only manipulated axis. Two tuned parameters, as the queue
names them: **cap rule** and **cost rung**.

| null | max run ÷ L\* | disp ÷ real | days in runs > L\* | switch ratio | placebo vol |
|---|---|---|---|---|---|
| RAND | 0.06 | 0.03 | 0.000 | **13.23** | 0.1185 |
| BLOCK *(reference)* | 1.00 | 1.00 | 0.000 | 1.00 | 0.1183 |
| BLOCK2 *(seed calibration, NEW)* | 1.00 | 1.00 | 0.000 | 1.00 | 0.1183 |
| SM_DOM *(875)* | **8.86** | 5.87 | **0.925** | 1.00 | 0.1184 |
| SM_SPLIT2 *(NEW)* | 4.44 | 4.09 | **0.927** | 1.00 | 0.1184 |
| SM_SPLIT4 *(NEW)* | 2.24 | 2.81 | 0.843 | 1.00 | 0.1183 |
| SM_SPLIT8 *(NEW)* | 1.13 | 1.86 | 0.583 | 1.00 | 0.1183 |
| SM_LONE *(NEW)* | **1.00** | 0.56 | 0.000 | 1.00 | 0.1184 |
| SM_FILL *(NEW)* | **1.00** | 1.73 | 0.000 | 1.00 | 0.1183 |
| SM_UNIF *(875)* | 0.24 | 0.03 | 0.000 | 1.00 | 0.1184 |

L\* = the real arm's own longest fire run (median 64 days over 41 runs).

## Gates (printed before any hypothesis was read)

G1 **0.000e+00** · G2 **0.000e+00** · G4 **0.000e+00** · G6 **0.000e+00** — PASS.
G5a *k* and *m* preserved: **0 violations of 161,280** real cells (0 of 2,100 synthetic).
G5b SM_LONE and SM_FILL have max run **exactly L\***: **0 violations of 46,080**.
G5c SPLIT ladder max-run ratio monotone down in *j* (13.65 > 6.86 > 3.46 > 1.76 synthetic) — PASS.
**G5d FAILS AS PRINTED.** Its bar was "SM_FILL's long-day share exceeds SM_LONE's", and on the
synthetic paths it reads 0.961 < 1.000. The bar was the wrong statistic, not the construction:
"days in runs ≥ 2" saturates at 1.000 for SM_LONE because its m−1 non-dominant runs are all ≥ 2. The
contrast it was meant to certify is settled on the real arms by the right statistic — at the same
maximum SM_FILL's run-length **dispersion is 1.73×** the real arm's against SM_LONE's **0.56×**, i.e.
**3.07× each other** — and that is the number Contrast B is read on.
**G7 CALIBRATION PASS.** BLOCK2 (BLOCK from an independent seed stream, true gap exactly zero by
construction) reads signed **−0.00015**, mean +0.00001, SE 0.00088, share below BLOCK 50.3%,
sign-test **z +0.24**. Band for everything below: |signed| ≤ 0.0010 and |z| < 2.0.
**G3 REPRODUCTION OF 875 PASS 4 of 4.** SM_DOM signed @10 bps **−0.00348** (875: −0.0046, bar
0.0020), sign-test **z +3.83** (875: +3.8), dispersion **5.87×** (875: 5.87×), SM_UNIF inside the
band (+0.00023, z −0.41). The rule-8 book table below also reproduces 875's three IS-picks and their
metrics **identically**.

## 1. CONTRAST A — the deciding pair: same illegal days, different maximum

| null | j | max ÷ L\* | days > L\* | signed @0 | @10 | @25 | sign z | mean ÷ SE |
|---|---|---|---|---|---|---|---|---|
| SM_DOM | 1 | 8.86 | **0.925** | −0.00384 | **−0.00348** | −0.00306 | **+3.83** | **−5.17** |
| SM_SPLIT2 | 2 | 4.44 | **0.927** | −0.00064 | **−0.00063** | −0.00055 | +0.94 | −1.64 |
| SM_SPLIT4 | 4 | 2.24 | 0.843 | +0.00044 | +0.00042 | +0.00066 | −0.53 | +0.73 |
| SM_SPLIT8 | 8 | 1.13 | 0.583 | +0.00139 | +0.00130 | +0.00126 | −1.65 | +2.02 |

**SM_DOM and SM_SPLIT2 hold the over-long day mass at 0.925 vs 0.927 — the same days — and differ
only in whether those days sit in one run or two. The bias falls from −0.00348 (z +3.83, 5.2 SE) to
−0.00063 (z +0.94, 1.6 SE): 82% of it is gone.** Nothing about the tail mass changed. Spearman(max ÷
L\*, signed gap) over the four ladder points = **−1.000**.

## 2. CONTRAST B — same maximum, 3.07× the dispersion

| null | max ÷ L\* | days > L\* | disp | signed @0 | @10 | @25 | sign z |
|---|---|---|---|---|---|---|---|
| SM_LONE | 1.00 | 0.000 | 0.56 | +0.00130 | +0.00101 | +0.00100 | −1.18 |
| SM_FILL | 1.00 | 0.000 | **1.73** | +0.00159 | **+0.00144** | +0.00130 | −1.77 |

Both obey 875's proposed clause. **|SM_FILL − SM_LONE| = 0.00044 at 10 bps — half the BLOCK2 band —
across a 3.07× dispersion difference, and both |z| < 2.** Tail shape at a legal maximum buys nothing.

## 3. Why H_MAX and H_TAIL still print REFUTED (reported as they came)

The signed gap does not decay to zero. It crosses zero between max ÷ L\* of 4.44 and 2.24 and settles
at **+0.0010 to +0.0014** for every capped null (SPLIT8 +0.00130 z −1.65, LONE +0.00101 z −1.18,
FILL +0.00144 z −1.77). No one of those is resolvable — all ≤ 2.0 SE, all |z| < 2 — but all three sit
on the **same** side, and my pre-registered bars required |signed| ≤ 0.0010. H_MAX also required
|signed| monotone *decreasing*; the sequence is 0.00348 / 0.00063 / 0.00042 / 0.00130, monotone in
the **signed** value at ρ = −1.000 but not in |·| once it crosses. So:

* **H_MAX REFUTED as printed** — the literal bar. The channel question it was built to settle is
  nonetheless answered by §1, on a contrast the bar did not depend on.
* **H_TAIL REFUTED as printed** — the two capped nulls are 0.00044 apart (its second leg passes) but
  both sit ~0.0012 outside the ±0.0010 band (its first leg fails).
* The honest statement of the residual: capping at L\* does not merely neutralise the −0.0035, it
  appears to **overshoot to ≈ +0.0012**, at 1.2–2.0 SE. That is below this grid's resolution and is
  named here as an open quantity, not a finding.

## 4. H_MECH REFUTED — 875's stated mechanism is FALSIFIED

875 proposed: *"a single giant de-grossed run is a long cash holiday that lowers the placebo's vol,
raising its Sharpe and shrinking the measured excess."* Priced as a prediction, it fails:

* **Placebo annualised vol is 0.1183–0.1185 across all ten nulls** — a spread of 0.0002, 0.2%
  relative — and is flat along the ladder (0.1184 / 0.1184 / 0.1183 / 0.1183).
* Spearman(max ÷ L\*, placebo vol) = **+0.396**, the **wrong sign** for the proposed mechanism.

With vol equal to 0.2%, the whole signed gap is a **mean-return** difference: SM_DOM's placebo earns
**+4.1 bps/yr** more than BLOCK's (SPLIT2 +0.7, SPLIT4 −0.5, SPLIT8 −1.5, LONE −1.2, FILL −1.7,
UNIF −0.3, BLOCK2 +0.2). The effect is real and it is in the mean, not the vol.

**Where it lives — DEPTH, and nothing else** (`.mechanism.csv`, all cuts printed):

| cut | n | median | mean | SE | sign z |
|---|---|---|---|---|---|
| **depth 1.00** | 576 | **−0.00590** | −0.00623 | 0.00137 | **+3.67** |
| **depth 0.50** | 576 | **−0.00184** | −0.00172 | 0.00069 | +1.75 |
| cadence D / W | 576 / 576 | −0.00350 / −0.00324 | | | +3.17 / +2.25 |
| gross 0.75 / 1.00 | 576 / 576 | −0.00352 / −0.00342 | | | +3.25 / +2.17 |
| panel U56 / B136 / SMALL | 384 each | −0.00357 / −0.00422 / −0.00255 | | | +2.04 / +2.35 / +2.25 |

2× the de-grossing amplitude, **3.2× the bias**; at depth 0.50 it is not resolvable at all. No other
cut changes the reading, and per-arm Spearman against the arm's own firing rate, run count and L\*
are all |ρ| ≤ 0.05 — it is not a property of which arm you picked.

## 5. H_COSTINV CONFIRMED, H_WF REFUTED

Worst switch-matched range across 0/10/25 bps = **0.00078** (bar 0.005); RAND's is **0.69105** at a
13.23× switch ratio. So none of this is a cost story, and RAND's entire gap still is.
Rule 8 on the statistic: Spearman(IS gap, OOS gap) ≥ +0.30 in **0 of 8 families for every null** —
identical to 875, and expected for a quantity that is 85–98% of its own seed-noise prediction
(obs ÷ pred at 20 seeds: SM_DOM 0.96, SPLIT2 0.98, SPLIT4 0.94, SPLIT8 0.95, LONE 0.91, FILL 0.91,
UNIF 0.85, BLOCK2 0.94; RAND **16.07**). The *level* persists in sign for SM_DOM alone: IS −0.0112,
OOS −0.0147 (875: −0.0096 / −0.0163).

## 6. Rule 8 on the books, and both KEEP paths (10 bps, next-day, weekly)

Declared IS-only selector: highest 2009–2016 Sharpe over every arm of the panel; OOS read once.
Same grid and same selector as 875, and the picks and their metrics reproduce it exactly.

| panel | IS pick | CAGR | Sharpe | MaxDD | H1/H2 | OOS CAGR | OOS Sh | OOS DD | 4a | 4b |
|---|---|---|---|---|---|---|---|---|---|---|
| U56 | CORR-HI q0.07 w1008 d1.00 W g1.00 | 12.73% | 1.034 | −22.93% | 1.160/0.915 | 12.41% | 1.016 | −22.93% | ✗ | ✗ (DD) |
| B136 | CORR-HI q0.12 w252 d1.00 W g1.00 | 13.91% | 1.166 | −16.63% | 1.289/1.037 | 12.97% | 1.154 | −16.63% | ✗ | **✓** |
| SMALL | VOL20-LO q0.17 w252 d1.00 D g1.00 | 5.04% | 0.404 | −48.52% | 0.736/0.201 | 2.00% | 0.203 | −48.52% | ✗ | ✗ |
| — | RULES v2 live (U56) | 8.64% | 1.208 | −11.90% | 1.237/1.186 | 9.49% | 1.286 | −11.90% | — | — |
| — | SPY (U56 window) | 15.13% | 0.885 | −33.72% | 0.959/0.824 | 15.27% | 0.874 | −33.72% | — | — |

4b bars on the U56 window: DD ≥ −20.23%, CAGR ≥ 10.59%, OOS Sharpe > 0.874.
Unselected base rates over all 1,152 arms: **4a 0 (0.0%)**, 4b 105 (U56 61/384 = 15.9%,
B136 44/384 = 11.5%, SMALL **0**/384). The B136 pass is the same by-product 875 already memo'd and
declined to propose — inside the CORR family idea 815 flagged as the one whose placebo excess walks
forward while buying no capital (idea 870, still open). **Nothing here is promoted.**

## PROPOSED PROTOCOL amendment (rule 6: PROPOSED, NOT APPLIED; PROTOCOL.md untouched)

> Amend 875's proposed clause by **deleting its parenthetical**. It reads *"its longest run must not
> exceed the real arm's longest run (equivalently, its run-length dispersion must not exceed the real
> arm's)"*. **The two are not equivalent and the clause should name the maximum only:** at a maximum
> fixed at the real arm's own, a 3.07× difference in run-length dispersion moves the statistic by
> 0.00044 — half the measured seed band — and SM_FILL at 1.73× dispersion is as clean as SM_LONE at
> 0.56×. Conversely, holding the over-long day mass fixed at 0.925 and splitting it from one run into
> two removes 82% of the bias. Record alongside it that the cap as written is **conservative**: no
> resolvable bias survives at max ÷ L\* ≤ 4.4 at 20 seeds, and the bias is a **full-de-grossing**
> effect (−0.0059 at depth 1.00, unresolvable at depth 0.50). Delete 875's vol rationale: placebo vol
> is flat to 0.2% across every null priced here and the effect is entirely in the mean return
> (≈ 4 bps/yr).

## Honest limits

1. The residual +0.0012 offset shared by every capped null is unexplained and below this grid's
   resolution; it is named, not claimed. Resolving it needs ≈ 200 seeds by 875's own budget arithmetic.
2. The SPLIT ladder's over-long day mass is only held tightly for j = 1 and 2 (0.925 / 0.927); by
   j = 8 it has fallen to 0.583, because the runs themselves shrink below L\*. The decisive comparison
   is therefore the j = 1 vs j = 2 pair, and that is the one the conclusion rests on.
3. All nulls share 871's gap draw, so the fire-run *placement* is uniform while BLOCK's preserves the
   real arm's ordering. That difference is common to every switch-matched null and cancels in the
   between-null contrasts, but it is not zero against BLOCK, and it is the most likely home of (1).
4. SURVIVORSHIP: U56 and B136 are current-constituent lists; SMALL is the sub-$2B panel with every
   ticker whose `max_1d_move` ≥ 1.0 dropped (716 → 664 columns) and holds current constituents only,
   so its levels are the most optimistic in the run and its 0-of-384 4b rate is an upper bound that
   still reads zero. The headline quantity is a **difference between two nulls on the same arm** and
   is far less exposed to that bias than any level. Binding drawdown is 2020.
5. Deterministic (md5-seeded); the run was executed twice and reproduced bit-for-bit.

**Verdict: ANSWERED = MAX-RUN-LENGTH FACT (82% of the bias removed by splitting the same illegal days
in two; 0.00044 bought by 3.07× dispersion at a legal maximum) / H_MAX and H_TAIL REFUTED on their
own pre-registered bars / 875's VOL MECHANISM FALSIFIED, the effect is +4.1 bps/yr of mean return and
lives at depth 1.00 / KILL for capital.**
