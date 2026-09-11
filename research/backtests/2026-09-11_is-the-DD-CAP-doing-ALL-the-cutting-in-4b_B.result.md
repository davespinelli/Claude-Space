# Idea 530 — is the DD CAP doing ALL the cutting in 4b?

**Verdict: ANSWERED / the queue's premise is CONFIRMED as a verdict-count statement and
REFUTED as a redundancy statement. No KEEP, no memo, no RULES or PROTOCOL change.**
Script: `2026-09-11_is-the-DD-CAP-doing-ALL-the-cutting-in-4b_B.py`
Artefacts: `.books.csv` `.lattice.csv` `.corpus.csv` `.walkforward.csv` `.headline.csv` `.console.txt`

## 1. The answer

Delete H1/H2/OOS entirely and score 4b on the DD cap and the CAGR floor alone:

| sample | n | pass 5-bar | pass {DD,CAGR} | verdicts CHANGED | of all | of the 2-bar passers |
|---|---|---|---|---|---|---|
| FRESH price family (this run) | 84 | 7 | 9 | **2** | 2.38% | 22.2% |
| RUN-POOLED corpus | 6,184 | 322 | 465 | **143** | 2.31% | 30.8% |
| **RUN-POOLED, duplicates removed** | **4,114** | **274** | **368** | **94** | **2.28%** | **25.5%** |
| rule-8 PICKS of the fresh family | 9 | 3 | 3 | **0** | 0.00% | 0.0% |
| zero-signal CONTROL (SPY at gross g) | 12 | 0 | 0 | **0** | 0.00% | — |

So the premise holds on the denominator the queue implies — **97.7% of 4b verdicts are decided
by the two constants alone**, and on the books an honest rule-8 selector actually reaches the
three Sharpe legs change **nothing at all (0 of 9)**. It fails on the denominator that matters
for a KEEP: of the 368 distinct books that clear {DD, CAGR}, the Sharpe legs cut **94, or one
in four**. "4b is a two-bar rule" is true of the corpus and false of the shortlist.

Both readings are printed side by side in PART G(1) because quoting either alone is misleading.
The 94 changed decisions are spread over **12 of the 21 source artefacts** (top three: the WIDTH
cloud run 22, idea 286's breadth books 16, idea `is-n_elig` 14), so this is not one run's
pathology.

## 2. The DD cap is *not* the bar doing the cutting — and which bar is, depends on the family

Sole-cut counts (books admitted when exactly one bar is deleted):

| sample | −H1 | −H2 | −OOS | −DD | −CAGR |
|---|---|---|---|---|---|
| FRESH family (84, gross-spanning) | 1 | 1 | 0 | **4** | **33** |
| RUN-POOLED distinct (4,114) | 16 | 37 | 1 | **430** | **382** |

Idea 527's live leg said the DD cap fails 36 of 39 and is sole 22 times; idea 531 said the CAGR
floor is sole 22 times against the cap's 4. **Both are right.** On a family that spans gross
(this run's and 531's), de-grossing slides a book down its Calmar ray until the floor catches
it, so the floor binds; on the record's run-pooled books — which are mostly full-gross selection
studies — the two bars are a near-tie (430 vs 382). The record should stop quoting either number
without naming the gross ladder it was measured on.

The OOS leg is once again almost never decisive: **1 sole-OOS of 4,114 (0.00024)**, recomputed
here from raw numbers rather than from a `fail4b` column. Idea 527 measured 46 of 399,086
(0.00012) by parsing fail-set columns on a disjoint corpus. Same order of magnitude, independent
method — 527's headline replicates.

## 3. The correction this run owes idea 531 (and the reason the two bars are not redundant)

Idea 531's committed CONTROL leaderboard row says of its zero-signal SPY-at-gross-g book: *"What
stops it is the three **Sharpe legs** … plus the Calmar structure — not either constant."*

**The Sharpe legs are not needed.** {DD, CAGR} admits **0 of 12** control rows on its own, and so
does every one of the 31 bar sets of size ≥ 2. Only the two single-bar rules let a de-levered
index through, and they do it on exactly complementary halves of the gross ladder:

| control gross | DD_ratio | CAGR_ratio | Calmar_ratio | passes DD alone | passes CAGR alone |
|---|---|---|---|---|---|
| 0.25 | 0.278 | 0.254 | 0.915 | ✓ | ✗ |
| 0.50 | 0.537 | 0.506 | 0.944 | ✓ | ✗ |
| 0.75 | 0.777 | 0.755 | 0.972 | ✗ | ✓ |
| 1.00 | 1.000 | 1.000 | 1.000 | ✗ | ✓ |

Every control row has Calmar_ratio ≤ **1.0000 < φ_CAGR/φ_DD = 1.1667**, so the pair blocks it
unaided — idea 333's Calmar ray, not the Sharpe legs, is the base-rate defence. This is the
sense in which the two-bar rule is *not* a weakened 4b: it is exactly the bar that a zero-signal
book cannot buy with leverage.

## 4. Live leg, both KEEP paths, PROTOCOL rule 8

Pre-registered family (declared in the script docstring before any number was read): 3 panels
(U56 55 names, B136 135, SMALL439 439) × [BAND b∈{0.00,0.03,0.08} + TOPN n∈{10,20,50} + EWALL]
× gross {0.25,0.50,0.75,1.00} = **84 real books**, + SPYG control × 12. 10 bps, weekly, next-day
execution, 260-day warm-up.

Per-leg fails over the 84: **CAGR 67 / H2 36 / H1 32 / OOS 32 / DD 18**. Sole bar CAGR 33, DD 4,
H1 1, H2 1. **4a 4 of 84, 4b 7 of 84.**

Rule 8 — dial *and* gross chosen on 2009-2016 IS Sharpe only, read once on 2017-01-01– :

| panel | family | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | vs RULES v2 OOS | vs SPY OOS |
|---|---|---|---|---|---|---|---|
| U56 | BAND | BAND0.08 g=1.00 | 11.87% | 1.1739 | −18.58% | 9.30% / 1.2835 / −11.69% | 15.24% / 0.8721 / −33.72% |
| U56 | TOPN | TOPN20 g=0.75 | 14.30% | 1.1648 | −18.15% | " | " |
| U56 | EWALL | EWALL g=1.00 | 15.08% | 1.1090 | −20.84% | " | " |
| B136 | BAND | BAND0.08 g=1.00 | 11.12% | 1.1125 | −19.31% | 7.92% / 1.1206 / −12.09% | 15.45% / 0.8820 / −33.72% |
| B136 | EWALL | EWALL g=1.00 | 14.11% | 1.0187 | −23.08% | " | " |
| B136 | TOPN | TOPN10 g=1.00 | 17.02% | 0.8007 | −27.95% | " | " |
| SMALL439 | BAND | BAND0.08 g=1.00 | 5.74% | 0.6265 | −19.43% | 3.83% / 0.5665 / −14.66% | " |
| SMALL439 | TOPN | TOPN20 g=1.00 | 9.39% | 0.5018 | −36.39% | " | " |
| SMALL439 | EWALL | EWALL g=1.00 | 3.75% | 0.2909 | −50.11% | " | " |

Picks beat RULES v2 OOS Sharpe **1 of 9**, beat SPY OOS Sharpe **5 of 9**; mean pick OOS CAGR
**11.37% vs SPY 15.38%** — no pick reaches SPY's OOS CAGR. Mean IS-selection regret vs the OOS
oracle **−0.0561**. **Picks: 4a 0/9, 4b 3/9.**

**No KEEP.** The 7 full-sample 4b passers all sit at gross ≥ 0.75 and are inside idea 531's
committed 63-book family — every one a re-measurement of a book the record already holds
(`2026-09-08_u56-band3-fullgross_KEEP_MEMO.md`, `2026-09-07_u56-top20-g075-4b_C_MEMO.md`). The
4 new 4a passers sit at g=0.25/0.50, and the IS-only picker takes g=1.00 in every BAND family,
so **not one 4a book here is rule-8 reachable**. Nothing is promoted.

## 5. Gates (all pre-registered, all printed before any new number)

* **G1** `fast_bt` vs `engine.backtest` on SMALL439: returns **6.939e-18**, turnover **0.000e+00**.
* **G2** live leg RULES v2 on U56 @10 bps **8.47% / 1.2070 / −11.69%** vs committed 8.66% /
  1.2056 / −12.05% (bar |ΔSharpe| ≤ 0.02; `data/prices.csv` re-downloads daily, idea 641 G2).
* **G3** the g∈{0.50,0.75,1.00} slice reproduces idea 531's committed `.legs.csv` **exactly** —
  72 rows × 5 leg booleans + `n_fail`, **0 disagreements**.
* **G4** lattice monotonicity (S ⊂ S′ ⟹ pass(S) ≥ pass(S′)): **0 violations over 961 ordered
  subset pairs on each of the four samples**.
* **G5** this run's 5-bar verdict equals idea 286's committed `keep_paths` 4b on **96/96 rows**.

## 6. Record discrepancy found (artefact vs headline, not a computation error)

Idea 531's QUEUE entry and commit message say **"4a 0/63"**. Its own committed `.books.csv`
contains **2** 4a passes among those 63 rows — `B136 BAND0.08 g=0.50` (H1 1.2730 > 1.2313,
H2 0.9871 > 0.9861, MaxDD −9.90% vs −12.09%) and `SMALL439 BAND0.08 g=0.50` (0.6526 > 0.5683,
0.6085 > 0.5757, −10.10% vs −14.66%). Its console reports 4a only on the 9 rule-8 **picks**
(0/9, which reproduces here exactly). The artefact is correct; the "0/63" is an
over-generalisation of the "0/9" and should be read as such wherever the record quotes it.
Both rows are low-return de-grossed band books and neither is rule-8 reachable, so nothing
about idea 531's conclusions changes.

## 7. Caveats

* The run-pooled corpus is the 21 committed `research/backtests/*.csv` artefacts that publish
  all five legs' **raw inputs**, so every verdict is recomputed; no `fail4b`/`f4b` column is
  read anywhere (idea 527 showed that column carries two incompatible semantics). 2,070 of the
  6,184 rows are exact duplicates of an earlier row — the same book published by two artefacts —
  and the headline uses the **4,114 distinct** decisions.
* Corpus rows are heterogeneous in panel, width, cap mix and gross, and each row's legs are
  scored against **its own** `spy_*` comparand. That is the right per-row comparison but it
  means the pooled counts weight whichever ideas happened to publish the most books.
* SURVIVORSHIP: all three panels are current constituents of their screens (`universe.json`,
  `universe_broad.json`, `data/SMALL_PANEL_README.md`), so every CAGR level is optimistic and
  the CAGR floor is tested in the books' favour.
* Nothing is proposed for adoption. `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` and
  `baseline.py` are untouched (PROTOCOL rule 6). One zero-parameter hygiene ask is *recorded,
  not applied*: any claim about which 4b bar binds should name the **gross ladder** it was
  measured on, since §2 shows that alone flips the answer.
