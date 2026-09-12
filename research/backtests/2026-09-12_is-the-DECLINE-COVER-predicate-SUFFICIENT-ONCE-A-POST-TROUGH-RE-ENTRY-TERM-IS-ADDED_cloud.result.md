# Idea 817 — is the DECLINE COVER predicate SUFFICIENT once a POST-TROUGH RE-ENTRY term is added?
**cloud lane, 2026-09-12. ANSWERED = NO — SUFFICIENCY RETURNS, BUT ONLY BY SPENDING NECESSITY, SO THE TERM IS EXACTLY THE SECOND TUNE THE QUEUE FORBADE. The predicate is never two-directional at any rung of the ladder. KILL for capital; no KEEP, no memo, no RULES/PROTOCOL edit (rule 6).**

Script `2026-09-12_is-the-DECLINE-COVER-predicate-SUFFICIENT-ONCE-A-POST-TROUGH-RE-ENTRY-TERM-IS-ADDED_cloud.py`.
RULES.md, PROTOCOL.md, research/scan.py, products/bot/bot.py and research/baseline.py untouched.

## The bar, declared before the grid was read
Adding a conjunct can only shrink the predicate population, so sufficiency `P(tie|pred)` is
purchasable at will — take k large enough and #pred collapses onto arms that never de-gross, which
*are* the control and tie trivially. So four bars were pre-registered, all at the **same** rung:
(1) sufficiency 1.0000; (2) #pred ≥ 30 (the queue's own power bar); (3) **necessity 1.0000 — the
term throws away NO true tie** (LOAD-BEARING: a tie whose arm de-grosses after the trough is a
*true* tie the POST clause discards, and discarding it is fitting to the counterexamples, not
completing the predicate); (4) #pred strictly exceeds the zero-cover-all-window count.
The headline rung was chosen by a **stated rule**, not by looking: smallest k meeting (1) and (2).

## Reproduction gates — all PASS, so this stands on 813's corpus, not a new one
G1 never-firing arm ≡ CONTROL-U 0.000e+00 · G2 vectorised runner ≡ `engine.backtest` · G3 every
(panel×gross×window) binding episode reproduces its MaxDD 0.000e+00 · G4 CONTROL-M mean gross ≡
arm's 1.478e-04 · **G5a** the 596/811 sub-corpus on FULL: 141 arms / 45 ties / 1.0000 / 1.0000,
ties SPYTR 0, BREADTH 12, VOL 18, SPYDD 15 — field for field · **G5b** 813's qualifying corpus:
**14 long-decline cells, 897 scored arms, 111 ties, 114 predicate arms, sufficiency 0.9737, 3 false
positives**, and **15 false positives over all windows split CORR 9 / VOL 3 / SPYDD 3** — field for
field · **G6** POST_REC nests 813's RECOVERY leg exactly (0.000e+00).

## The answer — qualifying corpus (897 arms, 111 ties), ALL families, eps = 0
| leg | #pred | necessity P(pred\|tie) | sufficiency P(tie\|pred) | ties LOST | FP left | two-directional? |
|---|---|---|---|---|---|---|
| DECLINE (813's) | 114 | **1.0000** | 0.9737 | 0 | 3 | no |
| +POST k=5 | 99 | 0.8919 | **1.0000** | 12 | 0 | **no** |
| +POST k=10 | 96 | 0.8649 | 1.0000 | 15 | 0 | no |
| +POST k=21 / 42 / 63 | 93 | 0.8378 | 1.0000 | 18 | 0 | no |
| +POST k=126 | 84 | 0.7568 | 1.0000 | 27 | 0 | no |
| +POST k=252 | 81 | 0.7297 | 1.0000 | 30 | 0 | no |
| +POST k=REC | 82 | 0.7387 | 1.0000 | 29 | 0 | no |
| +POST k=ALL | 60 | 0.5405 | 1.0000 | 51 | 0 | no |

Sufficiency reaches 1.0000 at **every** rung, and necessity is **below 1.0000 at every rung**. The
trade is one-for-one and visible: the term removes the 3 false positives on this corpus and, at the
cheapest rung, **12 true ties with them**. `both = 1` is never reached. With SPYDD dropped the
picture is identical (necessity 1.0000 → 0.9000 at k=5, sufficiency 0.9677 → 1.0000).
**#pred at k=5 is 99 against a zero-cover-all-window count of 18, so the term is not trivialised
(H_NONTRIV PASS) — the predicate is genuinely non-vacuous and still not two-directional.**

## Where the term does not reach — the 3 unremovable false positives
12 of 813's 15 false positives are removable by some rung; **3 are removable by none**, and they
name their own reason: **U56 POST20 SPYDD 0.20 at all three gross levels, arm trough 2023-03-10
against a control trough of 2025-04-08** — the arm's own MaxDD sits **before the control's peak**
(`arm_dd_before_ctl_peak` True in 3 of 3, `cover_RECOVERY` exactly 0). The offending de-gross
happened before the episode began, so no post-trough clause can see it. On POST20 with all families
the term makes sufficiency **worse** (0.9167 → 0.9000 at k=5): it discards 6 true ties while
leaving those 3 in place. 813's diagnosis of the counterexamples' *shape* is therefore correct for
12 of 15 and wrong for 3, and the 3 are precisely the SPYDD cells 811 built its confound story on.

## Reported axes, none of them a tune
Cover-bar ladder {0, 1e-12, 1e-6, 1e-4, 1e-3}: **flat at every rung**, #pred identical at all five.
`POST_k` ≡ `POST_k+COST` — **0 disagreements** at all 9 rungs over all 1,404 scored cells (811/813
read the same for DECLINE). Pre-peak cover is published as a diagnostic column only, never a
conjunct.

## Pre-registered hypotheses — 7 of 10 pass
PASS: H_REPRO, H_SUFF1, H_POWER, H_PLATEAU, H_NONTRIV, H_NOSPYDD, H_COST.
**FAIL: H_NEC1 (the load-bearing one) — necessity 0.8919 at the headline rung, so the POST term is
a filter fitted to the counterexamples, not a missing term in the predicate.**
FAIL: H_ALLFP — 6 of 15 false positives survive k=5 across all windows; 3 survive every rung.
FAIL: H_MONO — and the failure is **explained, not a defect**: #pred is monotone non-increasing
over the seven fixed-length rungs (99/96/93/93/93/84/81) and breaks only at REC, which is not a
fixed length (median recovery 195 trading days, 71% of cells under 252), so REC and 252 are not
nested — 6 arms are in REC's predicate and not 252's, 2 the other way.

## PROTOCOL rule 8 + both KEEP paths (mandatory; dial chosen on IS by IS Sharpe alone, OOS read once)
Standing 2016/2017 split on FULL; window-local half split on the six short windows, a stated
departure reported beside it. **Rule-8 picks passing 4b OOS 20 of 375; 4a OOS 11 of 375.**
FULL-window picks (54), median OOS CAGR / Sharpe / MaxDD by panel — U56 **9.08% / 1.271 / −9.98%**,
B136 **7.51% / 1.100 / −10.94%**, SMALL **3.09% / 0.512 / −12.44%** — against
**SPY OOS 15.33% / 0.877 / −33.72%** and **RULES v2 OOS 9.47%/1.278/−12.05% (U56), 7.88%/1.106/
−12.24% (B136), 3.75%/0.560/−13.89% (SMALL)**. 4b OOS 6 of 54, 4a OOS 2 of 54 on FULL.
Per window (scored / 4a / 4b / 4a-OOS / 4b-OOS / BOTH / 4b∧4b-OOS / **beats CONTROL-M**):
FULL 246/6/16/15/17/0/11/**0** · PRE20 219/8/9/1/24/0/8/1 · E2011 213/6/0/3/0/0/0/**0** ·
E2015 168/0/19/3/4/0/4/**0** · E2018 168/5/2/8/0/0/0/**0** · POST20 204/2/15/1/5/0/5/**0** ·
BEAR22 186/20/0/13/0/0/0/**0**.
**15 of the 16 FULL 4b passers are matched by their own gross-matched CONTROL-M** — the pass is
exposure, not the clause. Exactly **one** row anywhere beats its own control (B136 DISP ≤ 0.15
g=1.00, PRE20, 10.95%/1.173/−10.46% vs ctlM 9.56%/1.142/−9.12%), and PRE20 ends in 2019, wholly
in-sample under the record's own convention. **Nothing is promoted.**

## Caveats
SURVIVORSHIP: all three panels are current-constituent lists, so every level is optimistic and the
SMALL panel worst (a sub-$2B screen read today cannot see the names that fell out of it —
`data/SMALL_PANEL_README.md`); 52 tickers with `max_1d_move ≥ 1.0` were dropped first, 663 left.
The pooled corpus re-uses arms across overlapping windows — stated, not netted. Several windows are
3–5 years and sit wholly inside a bull leg, so no Sharpe or CAGR read off them is a capital claim.
486 of 1,890 rows are degenerate (gate never fires) and 33 of the 1,404 scored rows are all-cash;
both disclosed, neither netted.

## Correction to the record this run publishes
Idea 813 reported the false-positive mechanism as "the gate sits out the control's decline, fires
AFTER the trough". That is right for **12 of 15**. For the **3 U56 POST20 SPYDD 0.20 cells** the
de-gross is **before the control's peak** and the arm's binding episode is 2023, two years earlier
than the control's — no post-trough term can reach them, which is why idea 817's proposed clause
cannot restore sufficiency on POST20 at any k.

## Follow-ups filed
820 (price the PRE-PEAK leg the 3 unremovable counterexamples name, as its own one-parameter
predicate, and report what it costs necessity), 821 (restate the DECLINE predicate in the record as
a NECESSARY-ONLY condition and census which committed headlines change), 822 (does any
two-directional MaxDD-tie predicate exist on this corpus at all, or is exactness only ever
purchasable in one direction?).
