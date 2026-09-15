# Idea 882 — what is the RESIDUAL +0.0012 shared by every CAPPED null?

**Cloud, 2026-09-15. ANSWERED = NEITHER CHANNEL ON ITS OWN. IT IS AN INTERACTION.
881 named the uniform gap draw as "the most likely home" of the residual. That suspect is
FALSIFIED: a null that changes placement and NOTHING ELSE reads −0.00030 (z +0.18), and
−0.00003 (z 0.00) on violation-free arms — dead centre of the calibration band. A null that
caps the run lengths with placement HELD AT THE REAL ARM'S is also inside the band at all three
cap rules. The +0.0012 exists only when BOTH axes move at once: worst interaction 0.00228.
H_LEN0 and H_COSTINV CONFIRMED; H_PLACE, H_ADD and H_MAXSURV REFUTED on their own bars.
881's headline is materially qualified — see §5. KILL for capital, nothing here is a book.
RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched.**

Script: `2026-09-15_what-is-the-RESIDUAL-PLUS-0.0012-shared-by-every-CAPPED-null_cloud.py`
Outputs: `.arms.csv` (1,152) `.excess.csv` (13,824) `.gap.csv` `.factorial.csv` `.mechanism.csv`
`.walkforward.csv` `.books.csv` `.console.txt`

## What was run

1,152 real gate arms (8 families × q{0.07,0.12,0.17} × w{252,1008} × depth{0.50,1.00} ×
cadence{D,W} × gross{0.75,1.00} × panels U56 / B136 / SMALL-664) × **12 nulls** × **20 md5 seeds**
× 3 cost rungs = 829,440 placebo cells, every grid point printed and written to the CSVs.
The axis set is idea 881's verbatim. Two tuned parameters, as the queue names them:
**gap draw** and **cap rule**. 325 s.

Every switch-matched null in the record to date changes BOTH the run lengths and where the runs
sit, because every one of them redraws the gaps. This run un-confounds them with a 2×2:

| | lengths **REAL** | lengths **reshaped** |
|---|---|---|
| gaps **REAL** (the arm's own sequence, in order) | `OP_REAL` **≡ BLOCK** (gate G8) | `OP_DOM` `OP_SPLIT8` `OP_LONE` `OP_FILL` **(NEW)** |
| gaps **UNIF** (871's draw) | `UG_REAL` **(NEW)** | `SM_DOM` `SM_SPLIT8` `SM_LONE` `SM_FILL` (881's) |

`signed(OP_X)` is the pure **LENGTH** channel, `signed(UG_REAL)` the pure **PLACEMENT** channel,
`signed(SM_X)` is both — the only thing the record has ever measured. The OP nulls keep the real
arm's gap sequence and so its run *order*, which would leak information; each is therefore given
the same random circular roll BLOCK gets. That makes `OP_REAL` (real gaps, real lengths, same
roll, handed BLOCK's own seed stream) **identically BLOCK** — a zero this run measures rather
than assumes.

| null | gaps | lengths | max ÷ L\* | disp ÷ real | days in runs > L\* | switch | placebo vol |
|---|---|---|---|---|---|---|---|
| BLOCK *(reference)* | REAL | REAL | 1.00 | 1.00 | 0.000 | 1.00 | 0.1183 |
| BLOCK2 *(seed calibration)* | REAL | REAL | 1.00 | 1.00 | 0.000 | 1.00 | 0.1183 |
| **OP_REAL** *(the 2×2's zero cell)* | REAL | REAL | 1.00 | 1.00 | 0.000 | 1.00 | 0.1183 |
| **UG_REAL** *(placement only)* | **UNIF** | REAL | **1.00** | **1.00** | 0.000 | 1.00 | 0.1183 |
| SM_DOM | UNIF | DOM | 8.86 | 5.86 | 0.925 | 1.00 | 0.1184 |
| SM_SPLIT8 | UNIF | SPLIT8 | 1.13 | 1.86 | 0.583 | 1.00 | 0.1183 |
| SM_LONE | UNIF | LONE | 1.00 | 0.56 | 0.000 | 1.00 | 0.1184 |
| SM_FILL | UNIF | FILL | 1.00 | 1.73 | 0.000 | 1.00 | 0.1183 |
| **OP_DOM** | REAL | DOM | 8.86 | 5.87 | 0.925 | 1.00 | 0.1183 |
| **OP_SPLIT8** | REAL | SPLIT8 | 1.13 | 1.86 | 0.583 | 1.00 | 0.1184 |
| **OP_LONE** | REAL | LONE | 1.00 | 0.56 | 0.000 | 1.00 | 0.1184 |
| **OP_FILL** | REAL | FILL | 1.00 | 1.73 | 0.000 | 1.00 | 0.1183 |

Run statistics are read on the **circular** decomposition, because BLOCK and every OP null are
rotations and a linear reading of a rotation depends on where the array boundary happens to fall.

## Gates (printed before any hypothesis was read)

G1 **0.000e+00** · G2 **0.000e+00** · G4 **0.000e+00** · G6 **0.000e+00** — PASS.
**G8 PASS, and it is the load-bearing one:** `OP_REAL` reads signed **+0.000000000**, with
max |per-arm gap| **0.000e+00** over all three cost rungs on all 1,152 arms. The
order-preserving construction adds *exactly nothing* by itself, so everything `OP_X` reads is the
cap rule and only the cap rule.
G5e OP_\* reuse the real arm's gap multiset: **0 violations**. G5f `UG_REAL` / `OP_REAL` reuse
the real arm's fire-length multiset: **0 violations**. G5g `UG_REAL` changes no run length (circ
max ÷ L\* and disp ÷ real both exactly 1.00) — PASS. G5h the OP nulls' boundary-split rate
matches BLOCK's to 0.060 (BLOCK 0.257, OP 0.240–0.317) — PASS.
**G7 CALIBRATION PASS.** BLOCK2 signed **−0.00015**, mean +0.00001, SE 0.00088, z **+0.24**.
Band for everything below: |signed| ≤ 0.0010 and |z| < 2.0.

**Two gates FAIL and the cause is named, not hidden.** G5a-CIRCULAR reads 1,625 violations of
230,400 (**0.705%**) and G5b 113 of 92,160 (**0.123%**). Both come from **871's own uniform gap
draw**, which may place the leading *and* the trailing gap at 0, circularly merging the first and
last runs. The per-null diagnostic is unambiguous: every circular k/m violation is in the
`SM_*`/`UG_REAL` family and none in `OP_*`. It is a property of the record's inherited gap draw,
not of anything introduced here — **881's own gate, the LINEAR one it published, reads 0 of
92,160 on the same arms.** §6b re-prices every headline on the violation-free arms and the
answers do not move.

**G3 is an IDENTITY, not an agreement.** This run's seed string has the same *form* as 881's, so
the four `SM_*` nulls are handed the same md5 stream and reproduce 881 **bit-for-bit**
(SM_DOM −0.00348 z +3.83, SPLIT8 +0.00130, LONE +0.00101, FILL +0.00144, residual +0.00125).
That certifies the refactor changed nothing; it is **not** a second, independent draw of 881's
residual, and is not read as one. Every new null is on its own fresh stream.

## 1. H_PLACE REFUTED — the residual is NOT a placement effect

`UG_REAL` is the deciding object: 871's gap draw applied to the real arm's **own** fire-run
length multiset. Its maximum is L\* exactly, its dispersion 1.00× exactly, its k, m and switch
count the real arm's. It reshapes nothing. It moves only where the runs sit.

| null | signed @0 | @10 | @25 | mean | SE | mean ÷ SE | sign z | band |
|---|---|---|---|---|---|---|---|---|
| **UG_REAL** | −0.00024 | **−0.00030** | −0.00019 | +0.00033 | 0.00083 | +0.40 | **+0.18** | **INSIDE** |
| SM_SPLIT8 | +0.00139 | +0.00130 | +0.00126 | +0.00169 | 0.00084 | +2.02 | −1.65 | OUTSIDE |
| SM_LONE | +0.00130 | +0.00101 | +0.00100 | +0.00159 | 0.00082 | +1.93 | −1.18 | OUTSIDE |
| SM_FILL | +0.00159 | +0.00144 | +0.00130 | +0.00114 | 0.00082 | +1.40 | −1.77 | OUTSIDE |
| BLOCK2 *(zero)* | −0.00054 | −0.00015 | −0.00007 | +0.00001 | 0.00088 | +0.01 | +0.24 | INSIDE |

`UG_REAL` is **−0.00155 away from the +0.00125 it had to reproduce** and is on the **opposite
side of zero**. All three pre-registered legs fail. **881's named suspect is falsified.**

## 2. H_LEN0 CONFIRMED — with placement preserved, a legal cap costs nothing

| null | max ÷ L\* | days > L\* | signed @0 | @10 | @25 | sign z | band |
|---|---|---|---|---|---|---|---|
| OP_SPLIT8 | 1.13 | 0.583 | +0.00079 | **+0.00044** | +0.00010 | −0.53 | **INSIDE** |
| OP_LONE | 1.00 | 0.000 | −0.00103 | **−0.00097** | −0.00079 | +0.94 | **INSIDE** |
| OP_FILL | 1.00 | 0.000 | +0.00063 | **+0.00042** | +0.00044 | −0.94 | **INSIDE** |
| OP_DOM | 8.86 | 0.925 | −0.00181 | −0.00191 | −0.00110 | +1.89 | OUTSIDE |

## 3. H_ADD REFUTED — the two channels do not decompose

| cap rule | SM_X *(both)* | OP_X *(length)* | UG_REAL *(placement)* | sum | **interaction** |
|---|---|---|---|---|---|
| DOM | −0.00348 | −0.00191 | −0.00030 | −0.00221 | **−0.00127** |
| SPLIT8 | +0.00130 | +0.00044 | −0.00030 | +0.00013 | **+0.00117** |
| LONE | +0.00101 | −0.00097 | −0.00030 | −0.00127 | **+0.00228** |
| FILL | +0.00144 | +0.00042 | −0.00030 | +0.00012 | **+0.00132** |

Worst |interaction| **0.00228** against a 0.0010 bar. The residual is not the length channel and
it is not the placement channel; it appears only when a reshaped length multiset is dropped into
uniformly drawn gaps. The three capped interactions are all **positive and of the same size**
(+0.0012 to +0.0023) — which is the residual itself, now located but still not explained.

## 4. Robustness — every headline on the violation-free arms only

1,110 of 1,152 arms (96.4%) are free of the boundary artefact at every null and every seed.

| null | all arms | z | clean only | z | shift |
|---|---|---|---|---|---|
| **UG_REAL** | −0.00030 | +0.18 | **−0.00003** | **0.00** | +0.00028 |
| SM_DOM | −0.00348 | +3.83 | −0.00369 | +4.02 | −0.00021 |
| OP_DOM | −0.00191 | +1.89 | −0.00199 | +1.98 | −0.00008 |
| SM_SPLIT8 | +0.00130 | −1.65 | +0.00094 | −1.26 | −0.00036 |
| OP_SPLIT8 | +0.00044 | −0.53 | +0.00036 | −0.42 | −0.00007 |
| SM_LONE | +0.00101 | −1.18 | +0.00088 | −0.90 | −0.00013 |
| OP_LONE | −0.00097 | +0.94 | −0.00113 | +1.26 | −0.00015 |
| SM_FILL | +0.00144 | −1.77 | +0.00121 | −1.44 | −0.00023 |
| OP_FILL | +0.00042 | −0.94 | +0.00043 | −1.02 | +0.00001 |
| BLOCK2 | −0.00015 | +0.24 | −0.00013 | +0.18 | +0.00001 |

No shift exceeds 0.00036. `UG_REAL` gets **cleaner**, not dirtier (−0.00003, z 0.00). Every
verdict is unchanged (H_PLACE REFUTED, H_ADD REFUTED, worst interaction 0.00203).

## 5. The consequential by-product: 881's headline is materially qualified

881 concluded the −0.0046 is a MAX-RUN-LENGTH fact, on a ladder every point of which also
redrew the placement. Holding placement at the real arm's own:

**SM_DOM −0.00348 (z +3.83, 5.2 SE) → OP_DOM −0.00191 (z +1.89, 2.9 SE).**

**45% of the bias is placement-dependent, and what survives falls below the record's own
resolution bar** (|z| < 2.0, inside 3 SE). The *direction* survives — OP_DOM is negative on both
the full and clean samples and is the only non-BLOCK2 null outside the band in §2 — so 881's
qualitative answer stands; its **magnitude does not**, and at 20 seeds a placement-controlled
max-run effect is not resolvable at all. By depth, the cut 881 found decisive:

| | depth 0.50 | depth 1.00 |
|---|---|---|
| SM_DOM | −0.00184 (z +1.75) | **−0.00590 (z +3.67)** |
| OP_DOM | −0.00114 (z +1.17) | **−0.00328 (z +1.50)** |

It remains a full-de-grossing effect, roughly halved. Placebo vol is **0.1183–0.1184 across all
twelve nulls**, so 881's finding that the whole gap is a mean-return difference is untouched.

**H_MAXSURV REFUTED as printed** (bar: signed ≤ −0.0020 *and* z ≥ +3.0; OP_DOM −0.00191, z
+1.89). It misses both legs narrowly and is reported as it came.

**H_COSTINV CONFIRMED.** Worst matched range across 0/10/25 bps = **0.00081** (bar 0.005); every
null's switch ratio is 1.00×, so none of this is a cost story.

Rule 8 on the statistic: ρ(IS gap, OOS gap) ≥ +0.30 in **0 of 8 families for every one of the ten
nulls** — identical to 881 and 875, and expected for a quantity at 85–98% of its own seed-noise
prediction. The *level* persists in sign for SM_DOM (IS −0.0112 / OOS −0.0147) and for OP_DOM
(IS −0.0161 / OOS −0.0100).

## 6. Rule 8 on the books, and both KEEP paths (10 bps, next-day, weekly)

Declared IS-only selector: highest 2009–2016 Sharpe over every arm of the panel; OOS read once.

| panel | IS pick | CAGR | Sharpe | MaxDD | H1/H2 | OOS CAGR | OOS Sh | OOS DD | 4a | 4b |
|---|---|---|---|---|---|---|---|---|---|---|
| U56 | CORR-HI q0.07 w1008 d1.00 W g1.00 | 12.73% | 1.034 | −22.93% | 1.160/0.915 | 12.41% | 1.016 | −22.93% | ✗ | ✗ (DD) |
| B136 | CORR-HI q0.12 w252 d1.00 W g1.00 | 13.91% | 1.166 | −16.63% | 1.289/1.037 | 12.97% | 1.154 | −16.63% | ✗ | **✓** |
| SMALL | VOL20-LO q0.17 w252 d1.00 D g1.00 | 5.04% | 0.404 | −48.52% | 0.736/0.201 | 2.00% | 0.203 | −48.52% | ✗ | ✗ |
| — | RULES v2 live (U56) | 8.64% | 1.208 | −11.90% | 1.237/1.186 | 9.49% | 1.286 | −11.90% | — | — |
| — | SPY (U56 window) | 15.13% | 0.885 | −33.72% | 0.959/0.824 | 15.27% | 0.874 | −33.72% | — | — |

4b bars on the U56 window: DD ≥ −20.23%, CAGR ≥ 10.59%, OOS Sharpe > 0.874.
Unselected base rates over all 1,152 arms: **4a 0 (0.0%)**, 4b 105 (U56 61/384 = 15.9%,
B136 44/384 = 11.5%, SMALL **0**/384). The B136 pass is the same CORR-family by-product 875
memo'd and declined and 881 declined again — inside the family idea 815 flagged as the one whose
placebo excess walks forward while buying no capital (idea 870, still open). **It is declined a
third time and nothing here is promoted; no KEEP memo is written.**

## Honest limits

1. The residual is **located, not explained**. "It is an interaction" says where it is not; it
   does not say what about pouring reshaped lengths into uniform gaps costs +0.0012. The three
   capped interactions agree in sign and rough size, which is a fact worth a successor idea, and
   one is queued.
2. Every reading here is at **20 seeds**. The interaction (0.0012–0.0023) sits at 1.4–2.7 SE and
   the OP_DOM level at 2.9 SE. By 875's budget arithmetic ≈200 seeds would resolve them; nothing
   in §3 or §5 should be quoted as resolved at this budget.
3. G3 is an identity reproduction (shared seed stream), so this run does **not** independently
   re-confirm 881's numbers and does not claim to.
4. The two circular gates fail at 0.705% / 0.123% from 871's inherited gap draw. §4 prices the
   consequence at ≤ 0.00036 on every headline, but the draw itself is a defect the record now
   owns in writing.
5. SURVIVORSHIP: U56 and B136 are current-constituent lists; SMALL is the sub-$2B panel with
   every ticker whose `max_1d_move` ≥ 1.0 dropped (716 → 664 columns) and holds current
   constituents only, so its levels are the most optimistic in the run and its 0-of-384 4b rate
   is an upper bound that still reads zero. The headline quantity is a **difference between two
   nulls on the same arm** and is far less exposed to that bias than any level. Binding drawdown
   is 2020.
6. Deterministic (md5-seeded); G4 max|d| = 0.

**Verdict: ANSWERED = NEITHER CHANNEL ALONE — AN INTERACTION. Placement alone −0.00003 (clean
arms, z 0.00); a legal cap alone inside the band at all three rules; worst interaction 0.00228.
881's placement suspect FALSIFIED / H_LEN0 and H_COSTINV CONFIRMED / H_PLACE, H_ADD and H_MAXSURV
REFUTED on their own bars / 881's max-run effect roughly HALVED and no longer resolvable once
placement is held fixed / KILL for capital.**
