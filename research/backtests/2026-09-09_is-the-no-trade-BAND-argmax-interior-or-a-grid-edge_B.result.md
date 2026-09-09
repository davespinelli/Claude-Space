# Idea 328 — is the no-trade BAND's argmax INTERIOR, or a GRID EDGE?

**Lane B, 2026-09-09.** Script `2026-09-09_is-the-no-trade-BAND-argmax-interior-or-a-grid-edge_B.py`.
Two tuned parameters and only two: `n in {10, 20}`, `m in {0, 5, 10, 20, 40, 60, 80, 120, NOSELL}`.
Panels {U56, B136, SMALL439} and cost rungs {0, 10, 25} bps are reported axes, not choices.
54 cells, **all reported**, at all three rungs. Gross 0.75, weekly, NORM weights, vol scaler off.

## Verdict: KILL of the located-optimum reading — AND the queue's proposed replacement is refuted too

**1/6 books has an interior argmax.** H_LOCATED (interior on >= 4 of 6) is NOT SUPPORTED.
**H_CADENCE ("the honest instrument is a cadence dial") is ALSO NOT SUPPORTED** — at matched
turnover the band and the cadence dial are a coin flip. The band is neither located nor dominated.
**No KEEP-candidate: 4a 0/54 at every rung, and every rule-8 pick loses to RULES v2 out of sample.**

## Gates (all pre-registered, all run before any new number was read)

| Gate | Result |
|---|---|
| G1 `fast_backtest` vs `engine.backtest`, returns AND turnover | max\|d\| **0.000e+00** / **0.000e+00** (bar 1e-12) PASS |
| G2 cost-rung identity `r(c) = r(0) - turnover*c/1e4` vs live `cost_bps=10` | **0.000e+00** PASS |
| G3 `sel_band(m=0)` nests `sel_hard(n=20)` on every rebalance day | **0** disagreements PASS |
| G4 (U56, n=20, m=20, g=0.75, W, 10bps) vs idea 384's committed headline | max\|d\| **4.07e-04** (bar 5e-4) PASS |
| G5 `nweek_mask(k=1)` vs `engine.rebalance_mask('W')` | **0** disagreements PASS |

**G4 is a panel-vintage story and it is reported, not hidden.** On today's raw U56 (2026-09-08)
the same cell reads 12.8550% / 1.1107 / -17.2217% / **1.1514** / 1.0853 against the filed
12.87 / 1.112 / -17.22 / **1.144** / 1.093 — max\|d\| **7.70e-03**, which would FAIL the same bar.
MaxDD is identical to 1e-6; the entire drift is the **half split**, which four extra trading days
move (H1 **+0.0075**). B136 and SMALL439 were last cached 2026-09-04, so all three panels are
truncated to that common last date before anything is run. This is idea 514's panel stamp doing
real work: a reproduction gate on a half-split statistic is a gate on the panel's last date.

## [0] The degeneracy the filed sweep did not anticipate — and it decides the question

The band expels a held name when its rank passes `n + m`. Where `n + m` exceeds the panel's
eligible-rank ceiling `K_t` the band **can never expel by rank**: it is not a band, it is
HOLD-UNTIL-INELIGIBLE, i.e. idea 280's already-KILLED `m=999` arm.

| panel | cols | K_min | K_p25 | K_median | K_p75 | K_max |
|---|---|---|---|---|---|---|
| U56 | 56 | 3 | 33 | **41** | 45 | 55 |
| B136 | 136 | 3 | 80 | **99** | 111 | 127 |
| SMALL439 | 440 | 1 | 112 | **147** | 177 | 275 |

`m*` = the smallest tested `m` whose selection frame is **bit-identical** to the NO-SELL-EVER arm:

| panel | n=10 | n=20 |
|---|---|---|
| U56 | **60** | **40** |
| B136 | 120 | 120 |
| SMALL439 | none of the tested rungs | none of the tested rungs |

**The sweep the queue filed — `{40, 60, 80, 120, NOSELL} x {10, 20}` on three panels — is 30
cells but only 21 distinct books.** On U56, the panel that produced idea 325's PARK candidate, its
five rungs are **2 distinct books at n=10 and exactly 1 at n=20**. Nine of the thirty filed cells
are duplicates of a book already in the record under a different name. The wide end of this dial
does not exist on a 56-name panel.

## [1]-[2] The answer: edge, not interior

@10 bps, "genuine" = `m < m*`:

| panel | n | m* | widest genuine | argmax over ALL m | argmax over GENUINE m | Sharpe at m=0 | monotone up over genuine | INTERIOR |
|---|---|---|---|---|---|---|---|---|
| U56 | 10 | 60 | 40 | 60 (1.1101) | **40** (1.0992) | 0.9305 | **True** | No |
| U56 | 20 | 40 | 20 | 40 (1.1269) | **20** (1.1116) | 1.0635 | **True** | No |
| B136 | 10 | 120 | 80 | 20 (1.0622) | **20** (1.0622) | 0.8946 | False | **Yes** |
| B136 | 20 | 120 | 80 | 120 (1.0705) | **80** (1.0383) | 0.9432 | False | No |
| SMALL439 | 10 | — | 120 | 120 (0.7016) | **120** (0.7016) | 0.4773 | False | No |
| SMALL439 | 20 | — | 120 | NOSELL (0.6839) | **120** (0.6388) | 0.4499 | False | No |

**H_LOCATED: 1/6. NOT SUPPORTED.** Five of six books put the genuine argmax at the widest rung the
band can still reach, which is the definition of idea 240/256's grid-edge flag.

**The filed suspicion is confirmed exactly where it was raised.** On U56 — and only on U56 — Sharpe
is **monotone increasing in m across the whole genuine range at both n**. Idea 325's PARK candidate
(U56, n=20, m=20) is therefore **the last genuine rung of its own dial, not an optimum**: the very
next rung, m=40, is already the NO-SELL-EVER book. The curve does not turn over; it hits a wall.
Widening the grid, which is the remedy the filed idea proposed, cannot rescue it — there is nothing
on U56 to widen into.

Where the band *does* have room to run (B136, SMALL439) the curve is **not** monotone (4/6 books),
so "wider is better" is not a property of the band either. It is non-monotone noise on the wide
panels and a wall on the narrow one.

## [3] The matched-turnover cadence control — the queue's alternative, and it fails too

The filed wording proposes that if there is no located optimum "the honest instrument is a cadence
dial, not a band". Tested directly: the same parent book (m=0) at cadence `k x` weekly,
`k in {1,2,3,4,6,8,13,26}` — a **control ladder, never chosen, fully reported** — and each band cell
priced against the cadence arm at its **own realised turnover** (nearest rung and log-turnover
interpolation, both reported).

| set | band > cadence | median dSharpe |
|---|---|---|
| all 48 in-range cells | 27/48 = **56.2%** | **+0.0143** |
| genuine bands only (m < m*) | 18/33 = 54.5% | +0.0089 |
| U56 | 7/16 | **−0.0029** |
| B136 | 9/16 | +0.0187 |
| SMALL439 | 11/16 | +0.0175 |

**H_CADENCE NOT SUPPORTED.** A coin flip with a median edge of under one hundredth of a Sharpe, and
the sign flips panel to panel. Neither instrument dominates at matched turnover, so the queue's
proposed consequence — retire the band, use cadence — is **not earned by this evidence**. What the
run establishes is narrower and firmer: *both* dials are turnover dials, and on this family the
turnover level is doing the work, not which knob sets it.

Note this is a **weaker** result than idea 280's, which found the parent at 6W beat the buffer by
+0.093 Sharpe. That comparison is not reproduced here: at U56 n=10 the k=6 cadence arm reads
Sharpe 1.1312 at 5.37x/yr against the band's 1.0850 at 5.39x/yr — **−0.046 for the band**, the
right sign and half the magnitude. It is one cell of 48, and the pooled statistic does not carry it.

## [4] KEEP paths — all 54 cells, every rung

| rung | 4a | 4b |
|---|---|---|
| 0 bps | **0/54** | 23/54 |
| 10 bps | **0/54** | 16/54 |
| 25 bps | **0/54** | 13/54 |

**All 16 of the 4b passes @10 bps are on U56**, and every one of them is a book idea 384 already
published or a degenerate duplicate of one. Of the 24 cells at the **newly filed** rungs (m >= 60),
14 are degenerate and the 10 genuine ones return **0 4b passes and 0 4a passes**. The widened grid
adds no admissible book on any panel.

4b failure-bar census @10 bps: `H1,H2,OOS,DD,CAGR`:12, `H1,H2,OOS,DD`:6, `H2,OOS,DD`:5, `H2`:5,
`H2,DD`:4, `H1`:2, `DD`:2, `H2,OOS`:2.

## [5] Rule 8 walk-forward — (n, m) on 2008-2016 IS Sharpe @10bps, 2017-2026 read once

| panel | pool | pick | degenerate | OOS CAGR | OOS Sharpe | OOS MaxDD | RULES v2 OOS Sharpe | SPY OOS Sharpe | regret | full-sample 4b |
|---|---|---|---|---|---|---|---|---|---|---|
| U56 | unrestricted | n=20, m=40 | **yes** | 14.34% | 1.1892 | −15.27% | **1.2851** | 0.8820 | 0.0082 | PASS |
| U56 | genuine only | n=20, m=20 | no | 14.67% | 1.1867 | −17.22% | **1.2851** | 0.8820 | 0.0106 | PASS |
| B136 | either | n=10, m=20 | no | 15.63% | 0.9217 | −22.24% | **1.1185** | 0.8820 | 0.0619 | FAIL (H2,DD) |
| SMALL439 | either | n=20, m=120 | no | 8.51% | 0.5656 | −31.31% | **0.5680** | 0.8820 | 0.1849 | FAIL (all five) |

SPY OOS: CAGR 15.45%, Sharpe 0.8820, MaxDD −33.72%.

The unrestricted U56 pick is **again** the degenerate arm — the same trap idea 384 fell into and
flagged — and restricting to genuine bands costs 0.0025 OOS Sharpe. **All three picks lose to
RULES v2 out of sample** (1.2851 / 1.1185 / 0.5680). Under the identical rule-8 procedure the
cadence control picks U56 n=10 k=6 (OOS 1.0868), B136 n=10 k=13 (OOS 0.6805), SMALL439 n=10 k=6
(OOS **0.7401**): the band beats cadence 2/3 OOS, and loses badly on the panel where cadence wins.
That 2–1 split is the same coin flip section [3] measured, not a preference.

## Consequences proposed

1. **Idea 325's U56 top-20 m=20 PARK candidate stays PARKed, and gains a second reason.** It is not
   an interior optimum and cannot be made one: at n=20 on U56 the band has exactly four genuine
   rungs and m=20 is the last of them. The grid-edge flag is **confirmed**, not cleared.
2. **Report `m*` beside every published no-trade-band ladder.** A rung with `n + m >= K_t` is idea
   280's KILLED arm wearing idea 273's name, and both idea 384 and this run's own unrestricted
   rule-8 pick landed on one. `m*` is one line of code and it is a precondition for reading any
   `m` ladder, exactly as idea 359's `names` column is.
3. **Do not adopt the queue's cadence consequence.** It is not supported at matched turnover
   (56.2%, median +0.014, sign flips by panel). The defensible statement is that band and cadence
   are interchangeable turnover dials on this family.

**No RULES change. No book promoted. No KEEP claimed. RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py untouched.**

## Caveats

(1) All three panels are current-constituent lists — **SURVIVORSHIP** — so CAGR levels are
optimistic and 4b's CAGR floor is tested in the book's favour. (2) The 4a comparand RULES v2 runs
at its own live weekly cadence and gross. (3) SMALL439 starts 2010-01-04 and drops the 44 tickers
with `max_1d_move >= 1.0`, so its IS window is 7 years, not 9, and its rule-8 pick is the least
supported of the three. (4) NO-SELL-EVER still expels a name that stops being priced or stops being
eligible; it is "never sell on RANK", not "never sell". (5) The cadence ladder is a control arm, so
its 8 rungs are reported in full and no cadence is chosen anywhere except in the rule-8 mirror,
where it is chosen by the same IS rule as the band.
