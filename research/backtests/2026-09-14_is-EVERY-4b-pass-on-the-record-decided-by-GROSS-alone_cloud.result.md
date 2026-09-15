# Idea 657 — is EVERY 4b pass on the record decided by GROSS alone?

**2026-09-14, cloud lane, idea 2 of 2.** Script
`2026-09-14_is-EVERY-4b-pass-on-the-record-decided-by-GROSS-alone_cloud.py` (94 s, deterministic,
no network). Outputs: `.console.txt`, `.ladder.csv` (680 rows), `.windows.csv`, `.walkforward.csv`.

## VERDICT: **NO — but every 4b *verdict* is. The Sharpe legs decide nothing; the CAGR floor and the DD cap decide everything.**
**PROTOCOL 4b DOES need a matched-gross leg — and it must be a DRAWDOWN leg, not a Sharpe one.**
Not a KEEP-candidate: this is a bar-design result. Nothing promoted.

## GATES — 5 of 5 PASS
- **G1** k = 1.00 reproduces the unscaled book, max|d| `0.000e+00`.
- **G2** 8 of 8 committed 4b memos rebuild (max dSharpe 0.0202, max dMaxDD 0.0109).
- **G3** U56's SPY == the committed comparand (max|d| 4.56e−05). Per-panel bars printed; **SMALL483
  starts 2011 and its bars are re-priced on its own calendar** (SPY 14.06%/0.8581, floor 9.84%).
- **G4** no leverage, **zero** clipped days.
- **G5** de-grossing is near-affine: corr(r at k=0.20, r at k=1.00) = 0.99957..0.99996 over 20 books.

### A failed first parameterisation, recorded not deleted
The ladder was first written as a **target mean gross** g\* ∈ {0.20..1.00} with a no-leverage clip.
It failed its own gates — clipped-day share at g\*=1.00 ran **12.7%..100.0%** (band books hold cash
on gated days, so pinning their *mean* gross to 1.00 pins their *daily* gross at the ceiling and
stops being a scale), G5 affinity fell to 0.9865. **You cannot up-gross these books without
leverage**, so the only clip-free ladder is a de-gross ladder. No number was read off the failed
parameterisation.

## PART A — Sharpe is invariant; the exposure-sensitive legs are not
Over 17 rungs (k = 0.20…1.00), 10 bps, 20 books:

| statistic | within-book range over the ladder |
|---|---|
| **Sharpe** | median **0.0010**, max **0.0079** — *20 of 20 books under 0.10* |
| CAGR | median **9.70 pp** |
| MaxDD | median **14.75 pp** |

**H_FLAT PASS (20 of 20).** This confirms 653's 0.0052 at 5× the resolution and on the record's own
committed books. The two 4b Sharpe legs (H1 > SPY, H2 > SPY) are **constant down the entire
ladder**: they cannot be what decides a 4b verdict. Only the CAGR floor and the DD cap move.

## PART B — every 4b pass has a narrow, ONE-SIDED gross window
**H_WINDOW PASS: 0 of 20 books pass 4b at all 17 rungs** (653 found 0 of 13 at 3 rungs; it holds at
17). 4 of 20 pass at **no** rung — all four are SMALL483. Windows are contiguous 20 of 20; median
width **0.12** of a 0.80-wide ladder, **11 of 16 are ≤ 0.20 wide**. At 25 bps: 14 windows,
median width 0.075, still 0 of 20 passing everywhere.

4b passes by rung, 10 bps, all 20 books — **monotone in gross**:

| k | 0.20–0.45 | 0.50 | 0.55–0.65 | 0.70 | 0.75 | 0.80 | 0.85 | 0.90 | 0.95 | 1.00 |
|---|---|---|---|---|---|---|---|---|---|---|
| passes | **0** | 1 | 2 | 1 | 5 | 6 | 7 | 7 | **13** | **14** |

**H_LEGS FAILS, and the failure is the finding.** The bottom of every window is closed by
**CAGRFLOOR — 16 of 16**, as predicted. But the top is closed by DDCAP in only **2 of 16**: **14
windows run OPEN to the top of the no-leverage ladder.** The window is *one-sided*. PROTOCOL 4b as
written therefore rewards being **as grossed-up as the rules allow** — the entire 4b population
lives in the top quarter of the ladder, and de-grossing a passing book by two rungs (10% of NAV)
is usually enough to fail it. The only two books closed above are the concentrated `r6top20`
forms, which run at gross 1.00 natively and breach the cap.

## PART C — THE MATCHED-GROSS TWIN: selection is NOT vacuous, and the reason is drawdown
Twin = same panel, same weekly cadence, **every priced name equal-weight, scaled to the same
realised mean gross**. Only the choice of names differs.

**H_TWIN FAILS — in the record's favour. 5 of 8** committed 4b passers beat their matched-gross
twin on full-sample Sharpe at native gross (median delta **+0.0179**, range −0.0328…+0.1065). Best:
`u56-quantile50-respread-M` +0.1065, `u56-k8-qroll-q017-w1008-d100-g100` +0.1015,
`u56-v2band-gross100` +0.0813. Worst: `u56-marsrespread-gross075` −0.0328.

The decisive number is elsewhere:

> **The matched-gross twin fails 4b in 20 of 20 native cells — 18 on DDCAP alone, 2 on
> DDCAP + CAGRFLOOR.** Across the whole ladder only **7 of 60** 4b-passing rows (11.7%) have a twin
> that also passes at the same gross.

Twin MaxDD at k=1.00: U56 −22.06%, B136 −27.75%, SMALL483 −34.64%, against a −20.23% cap. The
equal-weight twin holds everything, including names below their 200d MA, so it takes the full
crash. **The selection and the gates buy essentially nothing in Sharpe and a great deal in
drawdown** — which is exactly the leg 4b prices, and exactly the leg de-grossing also moves. That
is why the two are confounded today.

## PART D — RULE 8 (book × gross chosen on the first half alone, OOS 2017–2026 read once)

| panel | chooser | pool/elig | pick | full CAGR/Sharpe/MaxDD (H1/H2) | **OOS** | RULES v2 OOS | SPY OOS | 4b | 4a |
|---|---|---|---|---|---|---|---|---|---|
| U56 | PLAIN | 170/170 | `u56-quantile50-respread-M @k1.00` | 15.41% / 1.2270 / −19.75% (1.330/1.148) | **16.10% / 1.2209 / −19.75%** | 9.47% / 1.2782 / −12.05% | 15.33% / 0.8767 / −33.72% | **PASS** | FAIL |
| U56 | MATCHED | 170/68 | *same pick* | same | **16.10% / 1.2209 / −19.75%** | same | same | **PASS** | FAIL |
| B136 | PLAIN | 102/102 | `B136:r6top20 @k1.00` | 23.18% / 1.1296 / −28.75% (1.345/0.960) | 22.33% / 1.0439 / −28.75% | 7.88% / 1.1059 / −12.24% | same | FAIL DDCAP | FAIL |
| B136 | MATCHED | 102/34 | *same pick* | same | 22.33% / 1.0439 / −28.75% | same | same | FAIL DDCAP | FAIL |
| SMALL483 | PLAIN | 68/68 | `SMALL483:band008 @k1.00` | 6.38% / 0.7210 / −18.75% (0.918/0.566) | 5.44% / 0.5996 / −18.75% | 3.75% / 0.5600 / −13.89% | same | FAIL H2+CAGRFLOOR | FAIL |
| SMALL483 | MATCHED | 68/**0** | **NONE ELIGIBLE** | — | — | — | — | — | — |

**H_R8 PASS where it can be applied** (MATCHED − PLAIN OOS Sharpe = **+0.0000** on both non-empty
panels: the IS argmax was already inside the matched survivors) **— but the leg VETOES the entire
pool on SMALL483: 0 of 68 (book × rung) cells beat their matched-gross twin in sample.** On small
caps the selection genuinely does nothing the exposure does not, and a matched-gross leg would
correctly refuse every candidate. That veto is a cost the Sharpe delta cannot show.

Out of sample, the picks beat their own twin in **2 of 5** rows (U56 +0.0914 twice, B136 −0.0468,
SMALL483 −0.0102). **4a passes 20 of 340 rows** across the whole ladder.

## ANSWER TO THE QUEUE, AND THE PROPOSED PROTOCOL LEG (rule 6 — not applied)
Every 4b **verdict** on the record is decided by gross, because the only two legs that move with
gross are the only two legs that ever bind. Every 4b **pass** is not: at matched gross the twin
fails 20 of 20, so the selection is earning the DD cap. The bar cannot tell these apart today.

> **PROTOCOL 4b, proposed addendum.** Report, beside every 4b verdict: (i) the book's **realised
> mean gross**; (ii) the **gross window** — the set of de-gross rungs over which the verdict holds,
> and which leg closes each end; and (iii) a **MATCHED-GROSS TWIN** row — the same panel and
> cadence, every priced name equal-weight at the same mean gross — with its **MaxDD and CAGR**, not
> only its Sharpe. A 4b pass whose twin also clears the DD cap at the same gross is an **exposure
> pass** and is reported as such.

The Sharpe form of the leg is worthless (it moves nothing: +0.0000 on 2 of 3 panels and vetoes the
third). The **drawdown** form is the one with content.

## CAVEATS
- **SURVIVORSHIP**: U56/B136 are current-constituent lists; **SMALL483 is a current-constituent
  screen and is worse** — its levels are the least trustworthy here, and its 0-of-68 veto is a
  statement about an optimistic panel, so the true veto is at least that strong.
- SMALL483 drops the 52 tickers with `max_1d_move >= 1.0` per `data/small_meta.csv` before use
  (663 names + SPY) and starts 2011-01-13, so its bars are re-priced and are **not** the record's.
- The ladder is de-gross only. These books cannot be up-grossed without leverage, so "the top of
  the window" means "the top of what PROTOCOL rule 2 permits", not an unbounded maximum.
- Nothing promoted; RULES.md, scan.py, bot.py and baseline.py untouched.
