# Idea 1182 (lane C, 2026-09-19) — rung-thinness census + well-measured-rung chooser

**VERDICT: ANSWERED (census) / KILL for capital (chooser). No new book, no RULES change.**

**The question.** Idea 1174 built the measurement histogram for the hold axis H and found the
record's "finer" hold evidence is two runs wearing seven rung labels. The queue asked for the
same histogram on the four axes that actually price a book — N, GROSS, COST, CADENCE — and for
the count of committed claims standing on a single-digit rung.

**The answer.** Over 35,216 committed text units (LEADERBOARD.md + CHANGELOG.md + 1,204
`*.result.md` / `*.memo.md`, 15,178,975 bytes read off HEAD), **204 of 4,614 committed axis
claims (0.0442) name a rung the record has measured fewer than ten times**: N 42 of 776
(0.0541), GROSS 23 of 966 (0.0238), COST 139 of 2,078 (0.0669), CADENCE 0 of 794. Every bar is
published, not tuned: T = 3 / 5 / 10 / 20 / 50 gives 107 / 149 / 204 / 337 / 484 thin-rung
claims. The H axis's alarm does **not** generalise.

**Why it does not, and what the real defect is.** The thin tail is small because the measurement
mass sits on ONE rung per axis. N = 20 holds 0.4568 of all run-mass (51 rungs, HHI 0.2384);
GROSS = 0.75 holds 0.4467, top two 0.7016; COST = 10 bps holds 0.4236, top two 0.6406;
CADENCE = W holds 0.5473, top two 0.7903. A committed ladder claim is rarely standing on a rung
nobody measured — it is usually standing on the same rung everybody measured, and no single-digit
thinness bar can see that. **The record's axis problem is concentration, not thinness.**

**The capital leg.** 126 real books (N {5,10,15,20,25,30,40} x GROSS {0.35,0.45,0.55,0.65,0.75,
1.00} on the frozen 2026-09-04 incumbent frame, three panels, weekly, 10 bps, t+1), every cell
published with both KEEP paths. 4a 0 of 126. 4b 28 of 126 full-sample, 20 OOS, 19 both. The U56
anchor replays to |dSharpe| 3.7e-05.

**Rule 8 (2017–2026 read once).** (N, GROSS) by argmax IS Sharpe on warm-up..2016-12-31, in two
variants: C_ALL over all 42 cells, and C_THICK restricted to cells both of whose rungs the census
measures >= T times, at every T. **14 of 15 (panel x bar) arms pick the identical cell**; mean
OOS dSharpe +0.0052. The one differing arm (SMALL, T = 50, menu 12 of 42) gains +0.0782 OOS
Sharpe on a book whose OOS MaxDD is -49.88% and which fails every 4b leg; against 40 size-matched
random menus it sits at the 0.9625 mid-rank percentile — 1 of 9 arms above the 95th at a draw
resolution of 0.025, median arm 0.425, mean tied share 0.575 (a random menu of the same size
usually picks the SAME cell). **Refusing thin rungs buys nothing.**

**Documented caveat (not a KEEP).** U56 **N15 g0.75** passes 4b full-sample AND OOS and beats the
frozen incumbent on every headline (CAGR 17.14% vs 15.80%, Sharpe 1.1722 vs 1.1537, OOS 1.1971 vs
1.1857) — but its 4b DD margin is **+0.0858 pp against the anchor's +1.1028 pp**, 12.8x thinner,
and its Sharpe edge is **+0.0185, t +0.34** (paired 63-day circular-block bootstrap, 400 reps,
identical block starts). **0 of 27 4b-passing non-anchor cells resolve |t| > 2 on full-sample
Sharpe, 0 on OOS Sharpe.** Rule 8's own chooser never reaches it: the argmax-IS-Sharpe chooser
goes to the gross corner g = 1.00 on all three panels and lands OOS-4b-FAIL on all three, while
19 of 126 cells pass 4b both full-sample and OOS. That is PROTOCOL rule 8's PARK-not-KEEP clause
biting, not a new book.

**Gates.** All PASS — G0 >= 10y (16.68); G1 cross-script replay of the committed anchor
(|dSharpe| 3.7e-05); G2 126 of 126 cells published; G3 corpus stamp; G4 the chooser reads no row
on or after 2017-01-01; G5 no leverage (max realised weight sum 1.000000); G6 every BOOK rung
appears in the census histogram; G7 bit-identical recompute of the anchor cell. Two tuned
parameters per leg and no more.

**Survivorship (rule 9).** U56 / B136 are current-constituent lists and SMALL a current sub-$2B
screen carried back to 2010; every absolute level here is an upper bound and every 4b pass an
optimistic one. What the run reads is a contrast between two choosers on the same names and days.

Artifacts: `.histogram.csv` (260 rung rows), `.concentration.csv`, `.claims.csv` (20 axis x bar
rows), `.claimunits.csv` (4,614 claim units), `.grid.csv` (126 cells), `.rule8.csv` (15 arms),
`.caveat.csv` (27 cells), `.gates.csv`, `.log.txt`.
