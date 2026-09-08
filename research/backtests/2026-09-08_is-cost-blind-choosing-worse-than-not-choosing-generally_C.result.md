# Idea 455 — is cost-blind choosing worse than not choosing, generally? (lane C, 2026-09-08)

**VERDICT: SPLIT — the question is ANSWERED and idea 231's sentence half survives.
"A cost-blind chooser is worse than not choosing" holds in SIGN at every rung, every
weighting and both corpora (9 of 9 readings), but at PROTOCOL's own 10 bps it is
significant on exactly ONE of four readings. "The ladder's whole value is avoiding the
cost-blind pick" is FALSE: costing the choice is worth a NET 3.2 pp of loss rate against a
35-41% loss rate, and 99.0% of the record's selection losses at 10 bps lose whether the
chooser is blind or not. The one robust claim is DELTA > 0 (costing the choice beats not
costing it) — and it is an artefact of concentration: DELTA is IDENTICALLY ZERO in 85.5% of
the record's readings, and live it is one dial.**
No book promoted; no new KEEP proposed. RULES.md, scan.py, bot.py, baseline.py untouched.

Script: `2026-09-08_is-cost-blind-choosing-worse-than-not-choosing-generally_C.py`
Outputs: `.census.csv.gz` (12,539 rung-readings), `.rungcurve.csv`, `.instances.csv`,
`.grid.csv` (896 live points), `.walkforward.csv`, `.keeppaths.csv`, `.console.txt`.

---

## 0. The decomposition, and the two tuned parameters

For a swept dial read at cost rung `c`:

```
L_aware(c) = OOS(argmax_d IS_Sharpe(d, c))   - OOS(default)     the cost-AWARE chooser
L_blind(c) = OOS(argmax_d IS_Sharpe(d, 0))   - OOS(default)     the cost-BLIND chooser
DELTA(c)   = L_aware(c) - L_blind(c)                            what costing the choice buys
```

* **p1 = COMPARAND** (what "not choosing" means): MEDIAN arm, RANDOM (mean over arms), and
  DEFAULT (the live RULES arm, Part B only). All levels reported.
* **p2 = RUNG**: {0, 5, 10, 15, 20, 25, 30} bps live, plus whatever rungs the archive commits.
  All grid points reported.

Nothing else is tuned. ORACLE (the OOS argmax) is printed as a ceiling, never as a comparand.

**Corpus.** PART A: 1,849 committed CSVs scanned, **59 usable, 5,214 cells, 12,539
rung-readings**. PART B: 3 panels x 6 dials x 7 rungs = **896 live points / 18 walk-forward
cells**, IS 2009-2016, OOS 2017-2026 read once.

## 1. Gates passed before any number was read

| gate | result |
|---|---|
| **G0** DELTA == 0 wherever the rung does not move the argmax | max \|DELTA\| = **0.000e+00** over 10,724 non-moving readings — an identity, as claimed |
| **G0b** DELTA_IS >= 0 (in-sample entitlement) | **0 violations of 12,539** |
| **G1** live re-simulation vs idea 235's committed walk-forward, 4 shared dials | 84 of 84 rows joined, max \|d\| = **2.220e-16** on OOS_aware, OOS_blind, OOS_DEFAULT, OOS_MEDIAN, OOS_RANDOM |
| **G1b** idea 235's 10-bps headline re-read from its own file | aware **+0.0156** / blind **-0.0188** (idea 231 quoted +0.0177 / -0.0237 on its own corpus — same shape, different panel) |

## 2. A correction the queue's premise needs first

Idea 235 defined the cost-blind pick as the argmax at the ladder's **lowest committed rung**.
Only **25 of 59 files (3,595 of 12,539 readings, 28.7%)** commit a genuine 0-bps rung; on the
rest the "cost-blind" chooser is a 10- or 25-bps chooser and DELTA is mechanically attenuated
to zero. Every archive number below is therefore reported both over all ladders and over the
**ZERO-ANCHORED** subcorpus. At 10 bps the correction triples the re-rank rate
(**2.4% -> 16.2%**) and the effect (**+0.0021 -> +0.0143**).

## 3. The split, at PROTOCOL's own 10 bps (the rung that decides)

| reading | n | L_aware | p | L_blind | p | DELTA | 95% CI | DELTA_IS | pick moves |
|---|---|---|---|---|---|---|---|---|---|
| ARCHIVE cell-weighted | 5,214 | **-0.0152** | <1e-4 | **-0.0174** | <1e-4 | +0.0021 | [+0.0005, +0.0081] | +0.0007 | 2.4% |
| ARCHIVE zero-anchored | 783 | +0.0061 | 0.402 | **-0.0082** | **0.029** | +0.0143 | [+0.0054, +0.0306] | +0.0045 | 16.2% |
| ARCHIVE file-weighted | 59 | **+0.0046** | **0.025** | -0.0052 | 0.896 | +0.0098 | [+0.0028, +0.0203] | +0.0033 | 33.9% |
| LIVE, 18 cells (vs DEFAULT) | 18 | +0.0087 | 1.000 | -0.0143 | 0.481 | +0.0230 | [+0.0000, +0.0689] | +0.0044 | 16.7% |
| LIVE, idea-235 dials only | 12 | +0.0156 | 1.000 | -0.0188 | 0.388 | +0.0345 | [+0.0000, +0.1034] | +0.0065 | 16.7% |

**H1 (blind loses to the default) is negative in 5 of 5 readings and significant in 1.**
**H2 (aware beats the default) is positive in 4 of 5 and significant in 1 — the one where H1
is not.** The weighting convention decides which half of idea 231's sentence you can publish,
exactly as idea 235 found for the premium itself: on the cell-weighted reading BOTH choosers
lose to the median arm at 10 bps; on the file-weighted reading the aware chooser wins and the
blind one is indistinguishable from zero. The pair of claims is never jointly significant.

## 4. The rung ramp: this is a 30-bps statement, not a 10-bps one

| source | L_aware slope | L_blind slope | DELTA slope |
|---|---|---|---|
| ARCHIVE cell-weighted | +0.002543/bp (R2 0.79) | **-0.000950/bp** (R2 0.79) | +0.003494/bp (R2 0.84) |
| ARCHIVE zero-anchored | +0.002669/bp (R2 0.94) | -0.000930/bp (R2 0.72) | +0.003599/bp (R2 0.90) |
| ARCHIVE file-weighted | +0.001006/bp (R2 0.94) | -0.000271/bp (R2 0.27) | +0.001277/bp (R2 0.82) |

DELTA(0) = 0 by definition, so the whole statement is a ramp anchored at zero. At 50 bps the
archive gives L_aware **+0.1342** / L_blind **-0.0649** / DELTA **+0.1991** (100% win rate) —
a large, obvious effect. At 10 bps it is 1/14th of that. The two halves are asymmetric: the
aware half rises **2.7x faster** than the blind half falls, i.e. most of the rung ramp is the
aware chooser gaining, not the blind one losing.

## 5. DELTA is concentrated, not general

* **85.5% of all readings and 81.1% of zero-anchored readings have DELTA identically 0** —
  the cost rung does not re-rank the dial, so cost-blindness is *free*. All of the effect
  lives in the moving minority, where the conditional gain is large and noisy
  (**D|moved = +0.0879** at 10 bps, +0.1982 at 30 bps).
* **The IS entitlement does not explain it.** DELTA >= 0 is an identity in sample; at 10 bps
  the aware pick's IS margin over the blind pick is **+0.0045** of Sharpe (zero-anchored) while
  its OOS margin is **+0.0143** — a **3.2x transfer ratio**. The chooser switches arms on
  half a hundredth of in-sample Sharpe and collects a ±0.09 out-of-sample swing. The ratio
  falls monotonically to **1.20 at 50 bps**: cost-awareness is a real instrument only where
  the rung makes the IS margin real, and at PROTOCOL's rung it is an amplifier of noise.
* **Live, it is ONE DIAL.** Pooled over rungs and panels: dropping the vol cap `V` takes
  DELTA from **+0.0267 to +0.0084**; every other single-dial deletion moves it by <=0.005.
  Per dial: V **+0.1185**, N +0.0492, L +0.0045, W +0.0006, G **+0.0000** (never re-ranks),
  K **-0.0123** — on the cadence dial, costing the choice makes the OOS result *worse*. This
  reproduces idea 228's reading that the vol-cap dial is discovering "switch the vol20 gate
  off", a result ideas 38/49 found directly.

## 6. The record's "selection loses" instances, split (comparand MEDIAN, 10 bps)

| subcorpus | n | aware loses | blind loses | both | **saved by costing** | **broken by costing** |
|---|---|---|---|---|---|---|
| ALL | 5,214 | 2,204 (42.3%) | 2,229 (42.8%) | 2,181 | 48 (0.9%) | 23 (0.4%) |
| ZERO-ANCHORED | 783 | 274 (35.0%) | 299 (38.2%) | 251 | 48 (6.1%) | 23 (2.9%) |

**This is the answer to the queue's question.** Of the record's 2,204 cost-aware selection
losses at 10 bps, only **23 (1.04%)** are losses the cost-blind chooser would have won — i.e.
**99.0% of the record's selection losses are not about cost-blindness at all**. Costing the
choice fixes 48 readings and breaks 23, a **net 25 of 783 (3.2 pp)** against a **35-41% loss
rate**. Selection loses in this record for reasons the cost rung cannot touch. The
loss is also deep when it happens: mean L_aware among losers **-0.0551** (zero-anchored),
mean L_blind among losers **-0.0747**.

Idea 229's number stands unaltered: the quantity PROTOCOL should quote is the REGRET
(~0.04 OOS Sharpe), and cost-blindness contributes a small, rung-dependent slice of it.

## 7. Rule 8 (PROTOCOL 8), live, at 10 bps — OOS 2017-2026 read once

| book | OOS Sharpe | OOS CAGR | OOS MaxDD |
|---|---|---|---|
| cost-aware chooser | 0.8588 | 16.67% | -31.72% |
| cost-blind chooser | 0.8357 | 15.53% | -30.36% |
| do-nothing (live RULES arm) | 0.8500 | 14.92% | -28.85% |
| random arm | 0.8216 | 13.97% | -28.82% |
| ORACLE (ceiling) | 0.9024 | — | — |
| **SPY** | **0.8820** | **15.45%** | **-33.72%** |
| RULES v1 (panel mean) | 0.6052 | 6.67% | -23.71% |
| RULES v2 (panel mean) | **0.9905** | 7.12% | -12.99% |

Per panel: U56 v1 0.7471 (7.73%, -13.83%) / v2 1.2851 (9.53%, -12.05%); B136 v1 0.5763
(5.94%, -21.19%) / v2 1.1185 (7.98%, -12.24%); SMALL439 v1 0.4923 (6.35%, -36.12%) /
v2 0.5680 (3.85%, -14.68%); SPY 0.8820 (15.45%, -33.72%) on all three.

**Every chooser in this study loses to SPY out of sample, and all of them lose to the live
RULES v2 book.** Even the ORACLE (0.9024) clears SPY by 0.02. The rung curve is monotone:
aware 0.9303 -> 0.7004 and blind 0.9303 -> 0.6463 from 0 to 30 bps, do-nothing 0.9503 ->
0.6491. At 0 bps the aware chooser *loses* to do-nothing by -0.0201 (5/18).

## 8. KEEP paths (both evaluated on all 896 live grid points)

**4a 137/896; 4b 24/896** — U56 22/294, B136 2/301, SMALL439 **0/301** (the 17th reproduction
of idea 136). 4b failing bars: DD 813, H2 542, OOS 508, H1 435, CAGR 303.

The 4b passers at 10 bps are all U56 and all single-panel: `N=40` (12.95%/1.1236/-18.38%,
H1 1.073 / H2 1.172, OOS 1.2656) and `V=0.30` — both **already-PARKed corners** of ideas
228/232/235, reproduced here unchanged — plus two by-products of this script's two new dials,
`L=100` (15.17%/1.0481/-19.72%, OOS 1.1354) and `W=0.75` (12.66%/1.0921/-18.31%, H1 1.088 /
H2 1.102, OOS 1.1680). B136's only 4b passer (`W=0.75`) clears at 0-5 bps and **fails at
PROTOCOL's 10**.

**All four are PARKed, not proposed.** `W` is a gross scalar, so per idea 311 its 4b verdict
is a dial placement rather than an edge, and per idea 144 a re-dialled book is the same book;
`L=100` is a single-panel, in-sample argmax on a dial this script introduced. Of the 18 arms
rule 8 actually picks at 10 bps, exactly one clears 4b (U56 `W=0.75`) and **0 of 18 clear 4a**
— every one fails on drawdown against the live low-vol book.

## 9. What this changes

1. Idea 231's "-0.0237 vs +0.0177" is a **corpus-specific, rung-specific reading**, not a
   general fact. Reproduced exactly on its own corpus (2.2e-16), it survives widening to 18
   live cells only in sign, and neither half is significant at 10 bps on any live reading.
2. **Report DELTA with its re-rank rate.** A DELTA quoted without `P(pick moves)` is
   uninterpretable, because DELTA is identically zero off the moving cells; the honest form is
   `DELTA = P(moves) x E[DELTA | moves]` (10 bps zero-anchored: 0.162 x +0.0879).
3. **Report the transfer ratio.** DELTA >= 0 is an in-sample identity, so DELTA/DELTA_IS is
   the only part that is evidence. At 10 bps it is 3.2; a chooser that swings 0.09 of OOS
   Sharpe off 0.0045 of IS Sharpe is not selecting, it is sampling.
4. **A cost-blind reading requires a 0-bps rung.** 71.3% of the record's rung-readings sit on
   ladders that cannot express one; idea 235's archive pick0 column is attenuated by that
   and should be re-read on the zero-anchored subcorpus.

Offered to Sunday review as reporting clauses (2), (3) and (4). No RULES change.
