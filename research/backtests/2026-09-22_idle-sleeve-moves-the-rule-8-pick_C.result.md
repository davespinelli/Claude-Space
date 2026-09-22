# Idea 2217 (lane C, 2026-09-22) — does an IDLE SLEEVE move *which cell* rule 8 reaches on the 2119 band x gross ladder?

**ANSWERED — YES ON THE MECHANISM, NO WHERE IT COUNTS.** A sleeve that pays the idle NAV makes
the in-sample surface see exposure for the first time — the IS Sharpe spread across the gross
dial goes from **0.0010 to 0.1068** on U56 (0.0022 → 0.1034 on B136) and the sign of
d(IS Sharpe)/d(gross) **inverts**, from +0.0021 unsleeved to **−0.2105** at phi = 0.00 — and the
rule-8 pick duly **moves in 8 of 16 arm x panel x chooser instances**, always down the gross dial
and never off band c = 0.08. But the moved pick is better only on the axis that does not decide:
**OOS Sharpe rises in 7 of 8 moves (mean +0.0459) while OOS CAGR falls 2.55 pp**, and CAGR is the
binding 4b leg in every window on both panels. 4b OOS passes among the 16 fitted picks: **5**,
and the only *moved* one is a bit-exact re-derivation of the candidate lane B already recorded
under idea 2221. The one genuinely new object is a **4a** passer (below), and it does not survive
an idle-NAV-matched comparand on one of two panels.

Script `research/backtests/2026-09-22_idle-sleeve-moves-the-rule-8-pick_C.py`, addendum
`..._C.addendum.py`, log `..._C.log.txt`, grid `..._C.grid.csv.gz` (18,018 rows), picks
`..._C.picks.csv`, IS surface `..._C.is_surface.csv`, addendum output `..._C.addendum.txt`.

**8 of 8 gates PASS on both panels.** G1 runner vs `engine.backtest` @10 bps max|d| **6.9e-18**
(U56) / 1.4e-17 (B136); G4 exact cost reconstruction @25 bps same; G2 **0** differing mask rows vs
`engine.rebalance_mask(idx,'W')`; G3 the ladder's centre cell **IS** `baseline.rules_v2_weights`,
max|d| **0.000e+00**; G6 sleeved total weight deviates from 1.0 by ≤ **1.6e-15**; G7 the fast
in-loop book build reproduces the reference constructor exactly (0.000e+00); G5 0 clipped weeks at
d ≤ 2, 175 at d = 4 (so d ≤ 2 is the clip-free noise region).

**Anchors reproduce the record.** SPY U56 FULL **15.14% / 0.8851 / −33.72%** (halves
0.9570/0.8264), OOS 15.29% / 0.8751 / −33.72%. Live RULES v2 @10 bps U56 FULL **8.62% / 1.2010 /
−12.05%** (1.2276/1.1806), OOS 9.46% / 1.2767 / −12.05%; B136 FULL 7.96% / 1.0972 / −12.24%, OOS
7.85% / 1.1017 / −12.24%. 4b bars: DD cap −20.23%, CAGR floor 10.60% FULL / 10.70% OOS (U56).

## The grid
2 panels x **6 sleeve arms** x 25 cells (band {0, 0.02, 0.03, 0.05, 0.08} x gross {0.50, 0.625,
0.75, 0.875, 1.00}) x 5 weekday offsets x 4 cost rungs x 3 windows = **18,018 published rows**.
Arms: `NOSLV` (the live 0%-cash form) and phi ∈ {0.00, 0.25, 0.50, 0.75, 1.00}, where the idle NAV
`1 − Σw` is held in `phi*SPY + (1−phi)*SHY` (construction identical to idea 2221, so the two runs
are directly comparable). **Tuned dials: exactly two — BAND and GROSS**, chosen by rule 8 *inside*
each arm. **phi is a published arm, never selected.** Offsets are a noise measurement (the
reported book is always d = 0); 0 bps is a mechanism read and carries no verdict.

## A — the sleeve makes the IS surface see exposure (this part is unambiguous)
| panel / arm | IS Sharpe spread across gross (mean over 5 bands) | mean d(IS Sharpe)/d(gross) | argmax gross | monotone |
|---|---|---|---|---|
| U56 NOSLV | 0.0010 | +0.0021 | 1.000 at 5/5 bands | UP 5/5 |
| U56 phi 0.00 | **0.1068** | **−0.2105** | **0.500 at 5/5 bands** | **DOWN 5/5** |
| U56 phi 0.25 | 0.0163 | −0.0328 | 0.500 at 4/5 | DOWN 4/5 |
| U56 phi 0.50 | 0.0508 | +0.1012 | 1.000 at 5/5 | UP 5/5 |
| U56 phi 1.00 | 0.0794 | +0.1588 | 1.000 at 5/5 | UP 5/5 |
| B136 NOSLV | 0.0022 | +0.0043 | 1.000 at 5/5 | UP 5/5 |
| B136 phi 0.00 | **0.1034** | **−0.2037** | **0.500 at 5/5** | **DOWN 5/5** |
| B136 phi 0.25 | 0.0122 | −0.0229 | 0.500 at 4/5 | DOWN 4/5 |
| B136 phi 1.00 | 0.0709 | +0.1418 | 1.000 at 5/5 | UP 5/5 |

The filed premise (2119(D): "IS Sharpe moves 0.0013 across the whole gross dial") is confirmed for
the unsleeved ladder and **destroyed by the sleeve**: a 100x (U56) / 47x (B136) amplification, with
the slope changing sign between **phi = 0.25 and phi = 0.50 on both panels** (U56 −0.033 → +0.101).
The mechanism is exactly the one filed — the credit scales with `1 − realised gross`, so it is
largest where the book is smallest — and it is quantitatively identical on the two panels, which
is what one expects of an accounting term rather than a tape fact.

## B — 4a / 4b pass counts per arm, of 25 cells (d = 0, 10 bps)
| panel / window | NOSLV | phi 0.00 | phi 0.25 | phi 0.50 | phi 0.75 | phi 1.00 |
|---|---|---|---|---|---|---|
| U56 FULL | 4a 0 / 4b 5 | **4a 13** / 4b 5 | 4a 0 / **4b 14** | 0 / 6 | 0 / 0 | 0 / 0 |
| U56 OOS | 4a 0 / 4b 7 | **4a 12** / 4b 10 | 4a 0 / **4b 19** | 0 / 6 | 0 / 0 | 0 / 0 |
| B136 FULL | 4a 0 / 4b 4 | **4a 13** / 4b 4 | 4a 0 / 4b 10 | 0 / 3 | 0 / 0 | 0 / 0 |
| B136 OOS | 4a 2 / 4b 1 | **4a 13** / 4b 4 | 4a 0 / 4b 10 | 0 / 3 | 0 / 0 | 0 / 0 |

The CAGR leg binds in 39–65 of the fails in every panel x window and the DD leg in 50–73; **the
two Sharpe legs never bind at all (0 of 150 fails in every cell of the table)**, reproducing
1093/2119's finding that 4b is decided by its level legs on this ladder.

## C — rule 8 (parameters on 2009–2016 only, 2017–2026 read once): does the pick move?
| panel / chooser | arm | pick | moved? | OOS CAGR / Sharpe / MaxDD | 4b | 4a | OOS rank |
|---|---|---|---|---|---|---|---|
| U56 C1 | NOSLV | c0.08_g1.000 | — | 12.00% / 1.1625 / −19.05% | ✔ | ✘ | 25/25 |
| U56 C1 | phi 0.00 | **c0.08_g0.500** | **yes** | 7.12% / **1.3576** / **−8.92%** | ✘ (CAGR) | **✔** | 8/25 |
| U56 C1 | phi 0.25 | c0.08_g0.625 | yes | 10.77% / 1.2099 / −15.65% | ✔ | ✘ | 22/25 |
| U56 C1 | phi 0.50–1.00 | c0.08_g1.000 | no | 15.63–18.56% / 1.169–1.090 / −23.7 to −30.5% | ✘ (DD) | ✘ | 8, 4, 3 /25 |
| U56 C2 | phi 0.25 | c0.08_g0.875 | yes | 12.99% / 1.2043 / −18.64% | ✔ | ✘ | 24/25 |
| B136 C1 | NOSLV | c0.08_g1.000 | — | 10.98% / 1.0921 / −19.50% | ✔ | ✘ | 20/25 |
| B136 C1 | phi 0.00 | **c0.08_g0.500** | **yes** | 6.60% / **1.2912** / **−9.17%** | ✘ (CAGR) | **✔** | 4/25 |
| B136 C1/C2 | phi 0.25 | c0.08_g0.750 | yes | **11.01% / 1.1399 / −17.34%** | ✔ | ✘ | 12/25 |
| B136 C2 | phi 0.00 | c0.08_g0.875 | yes | 10.24% / 1.1581 / −16.84% | ✘ (CAGR) | ✘ | 19/25 |
| B136 C2 | phi 0.50 | c0.08_g0.875 | yes | 13.66% / 1.0877 / −23.32% | ✘ (DD) | ✘ | 4/25 |

C1 = argmax IS Sharpe; C2 = argmax IS Sharpe among the cells that pass 4b **in sample**. The band
resolves to **c = 0.08 in 16 of 16 instances** — the sleeve moves *gross only*, exactly the dial
2119 said the verdict turns on.

**Is the moved pick better OOS?** Against the no-sleeve-picked cell priced *inside the same arm*
(so only the move is being scored): **7 of 8 moves raise OOS Sharpe, mean +0.0459**, but mean OOS
**CAGR −2.55 pp** and mean OOS MaxDD **+4.51 pp** (shallower). Since the CAGR floor is 4b's sole
binder here, the move trades away the one thing 4b wants. Fitted-pick OOS rank within its own arm
averages **9.75 of 25** against a coin-flip null of 13.0 — a mild real edge for the IS chooser,
smaller than the arm-to-arm spread it sits inside. 4b OOS 5 of 16, 4b FULL 4 of 16, **4a OOS 2 of
16** (both of them the phi = 0.00 / c0.08 / g0.50 cell).

**Cross-lane replication.** `B136 / phi 0.25 / c 0.08 / g 0.750` reproduces idea 2221's recorded
candidate to four decimals in every published number (OOS 11.01% / 1.1399 / −17.34%; FULL 11.06% /
1.1520 / −17.34%). 2221 pinned gross at the live 0.75; **this run shows that pin was not binding —
a free gross dial lands on 0.75 anyway on that panel.** Its 4b holds at 5 of 5 offsets and at
0/10/25 bps and fails at 50 bps, as 2221 reported.

## D — the one new object, and why it is not recommended
Chooser C1 reaches **phi = 0.00 / c = 0.08 / g = 0.50** — the band book at half gross with its idle
NAV swept into SHY — on **both panels**, and it is the record's first robust **4a** passer on this
ladder: U56 FULL 6.51% / **1.3084** / **−8.92%** (halves 1.3619/1.2719), OOS 7.12% / 1.3576 /
−8.92%; B136 FULL 6.49% / 1.2761 / −9.17% (1.3908/1.1708), OOS 6.60% / 1.2912 / −9.17%, against a
live book at 1.2010 / −12.05% (U56) and 1.0972 / −12.24% (B136). It holds 4a at **15 of 15**
offset x cost cells at 0/10/25 bps on U56 FULL/IS and **20 of 20 including 50 bps** on B136. Its DD
margin over the 4b cap is +11.31 pp against an offset spread of 1.25 pp (9x outside its own
scheduling noise).

**It is still not a book fact.** PROTOCOL 4a scores against the live book, whose idle NAV earns
**0%**, so a swept candidate collects a credit its comparand is denied. Re-scored against the
**same cell of its own arm** (c0.03 / g0.75 / phi = 0.00 — the live book *with* the sweep), so that
only the band x gross choice is priced:

| panel | FULL | IS | OOS |
|---|---|---|---|
| U56 | matched-4a **17/20** | 19/20 | **0 / 20** (dH1 −0.0441) |
| B136 | 20/20 | 20/20 | 16/20 |

**U56 OOS gives it up entirely** — the candidate's first-half OOS Sharpe falls below the swept
incumbent's — while B136 keeps it. One panel passes, one fails: the same coin-flip failure mode
2221 hit on the other dial. And the sweep applied to the **live cell itself** (the thing a Sunday
review would actually adopt) passes 4a at d = 0 but flickers across weekday offsets at 10 bps
(U56 FULL 1,0,1,1,0) and **dies completely at 25 bps on both panels** — it is worth
**+0.50 pp CAGR and +0.067 Sharpe** on U56 FULL, inside its own scheduling noise.

## Verdict
**PARK** the phi = 0.00 T-bill sweep (a real, implementable cash-accounting fix that produces the
record's first 4a passes but fails an idle-NAV-matched comparand on 1 of 2 panels, and at the live
cell dies at 25 bps). **KILL** the filed hope that the sleeve improves *which cell rule 8 reaches*
for real capital: the pick moves, the movement is systematic and mechanically understood, and it
buys Sharpe with the exact currency — CAGR — that PROTOCOL 4b is short of. No new 4b candidate
beyond the one 2221 already recorded.

**NO RULES CHANGE.** RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py untouched.
**Survivorship (rule 9):** U56 and B136 are current-constituent panels; every level here is
optimistic and this is a within-tape contrast only. The sleeve additionally assumes SHY and SPY are
tradable at the panel's adjusted closes with the same 10 bps and the same weekly cadence as the
book, and that the idle NAV is genuinely sweepable — a brokerage fact this sandbox cannot check.
