# Memo — the CAGR FLOOR SE clause (idea 1025, cloud lane, 2026-09-16)
Proposed as a PROTOCOL rule 4b reporting clause. **NOT applied** (rule 6: rules change only at
Sunday review). Nothing in `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` or `baseline.py` was
touched by this run, and no book was promoted.

**Exact wording, to be added to PROTOCOL.md rule 4b if the Sunday review adopts it:**

> *A 4b `CAGR >= 70% of SPY's` pass is published with the distance from the book's OOS CAGR to
> the floor expressed in units of that book's OWN OOS-CAGR standard error (stationary block
> bootstrap, 21-day blocks, B >= 1,000). A pass inside 1 SE is reported as NOT CERTIFYING and
> cannot be the leg on which a KEEP turns: at PROTOCOL's own split the median book sits
> **0.97 SE** from the floor, **52.9%** of (book, end) cells are inside 1 SE and **91.7%** inside
> 2 SE, and **49 of the 78** OOS 4b passes in this run clear the floor by less than one SE of
> their own OOS CAGR. The null base rate quoted alongside such a pass names its NULL
> CONSTRUCTION, because the three legal constructions do not agree: at the 0.70 floor a
> gross-matched name-randomisation clears it **0.0000** of the time while a block or iid
> bootstrap of the same book's own path clears it **0.2911** and **0.2976** — a spread of 0.30 on
> a quantity the record publishes as one number.*

**Why.** Idea 1025 was filed on 1022's reading that the split-point sensitivity the record blames
on the drawdown cap is really a CAGR-floor object. **That reading is confirmed, and it is not
confined to the illegal window.** On 1022's post-2020 grid `L5_CAGR` flips on **43.2%** of the 44
books against **13.6%** for `L4_DD` (**H_CARRY PASS**), and on the RULE-8-LEGAL grid — where rule
8 actually permits a split — `L5_CAGR` still flips on **11.4%** of books while `L4_DD` flips on
**0.00%** and is constant on **all 44** (**H_LEGAL PASS**). The DD cap has no split-point band on
any legal end; the CAGR floor has one everywhere.

**But the floor is not a test the record can run.** `H_DECIDE` **FAILS**: the median distance to
0.70 × SPY is **0.0382** of CAGR against a median bootstrap SE of **0.0366**, i.e. **0.969 SE**.
Raising the floor makes it worse, not better (1.63 / 1.36 / **0.97** / 0.72 / 0.45 SE at 0.50 /
0.60 / **0.70** / 0.80 / 0.90), so there is no floor level on the grid at which the leg separates
from its own noise. The split-point band `L5_CAGR` exhibits is therefore the leg being re-read
across overlapping windows that cannot resolve it — which is why the clause asks for the SE and
not for a different floor.

**Two further failures, reported as loudly.** `H_NULLKIND` **FAILS** (spread **0.2976** at the
headline floor): the gross-matched null never clears 0.70 × SPY at any end, because random name
selection at the live book's 0.75 gross gives up too much return, while bootstraps of a real
book's own path clear it ~29% of the time. "The base rate" is not one number. `H_BASIS` **FAILS**
and reverses 1022's finding on the legal grid: there the comparand BASIS moves `L5_CAGR`'s binding
rate by **0.0043** while sliding the split moves it by **0.0909** — the opposite ordering to the
post-2020 grid, where 1022 found the basis dominant. `H_FLOORMONO` PASSES on all three nulls.

**Evidence.** `2026-09-16_does-L5_CAGR-carry-the-SPLIT-POINT-EFFECT_cloud.py`, a 4,224-row ladder
(44 books × 3 rungs × 32 ends), a 42,240-row decidability table (1,000 block-bootstrap draws per
book × end × rung), and 500 draws of each of three nulls per panel — **15 dial points (5 floors ×
3 nulls) all reported at every panel × cost × end grid × basis, none selected**. Gates **8 of 8**:
G1 fast runner vs `engine.backtest` (6.9e-18 / 1.7e-16), G3 SPY's committed OOS triple (1.7e-04),
G4 1013's four published picks (4 of 4, 4.6e-04), G5 bit-level determinism, **G6 the gross match
itself (2.2e-16)**, G7 bootstrap consistency (44 of 44), G8 the 2026-09-04 KEEP-4b candidate's own
legs. Hypotheses **3 of 7**. `H_1022` fails on the letter (`L4_DD` binds 0.0341 on the full
2019Q1– band against 1022's 0.0000) and **reconciles exactly** on the POSTCRASH sub-grid that
1022's number is actually conditioned on — 11 ends from 2020-06-30, where `L4_DD` binds **0.0000**
and is constant on **44 of 44** while `L5_CAGR` binds **0.2521**. The two CAGR shares reproduce to
**0.0096**.

**Rule 8.** All 44 books at PROTOCOL's declared split, 2009–2016 in sample, 2017–2026 read once:
**OOS 4b 78 of 132, OOS 4a 2 of 132**. Best `U56-qroll-q0.12-w1008-d1.00` at 10 bps, OOS **16.59%
/ 1.404 / −13.03%**, against SPY OOS 15.21% / 0.8711 / −33.72% and RULES v2 live 8.62% / 1.2007 /
−12.05% — and it clears the CAGR floor by **1.55 SE**, one of the minority that would survive the
proposed clause. **No book KEEP is claimed.** The two 4a passes are the same de-grossed band book
(`B136-band0.08-g0.50`, 10 and 25 bps) at full-sample CAGR **5.67%**, which beats RULES v2's
second-half Sharpe by **0.0009** — inside any reading of noise — and fails 4b on the CAGR floor by
a wide margin. It is a lower-return book than the live rules and is not capital-worthy.

**Survivorship (rule 9).** U56 and B136 are current-constituent panels, so every CAGR level here
is optimistic and every 4b count an upper bound. The bias runs AGAINST this memo's conclusion
rather than for it: an inflated book CAGR pushes books further above the floor and makes
`L5_CAGR` look MORE decidable than it is, while SPY is a real index series and is not inflated. A
`H_DECIDE` failure at **0.97 SE** on survivor panels is therefore a lower bound on the problem.
