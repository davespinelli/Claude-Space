# Idea 2064 (lane B, 2026-09-20) — DOES THE STANDING KEEP-4b CELL SURVIVE *ADVERSARIAL* (BEST-NAME) DELETION?

**ANSWERED — SPLIT, AND THE SPLIT IS THE POINT. (1) IDEA 2050'S RANDOM-DELETION NULL IS THE WRONG
NULL FOR SURVIVORSHIP: THE ADVERSARIAL RUNG SITS *BELOW THE RANDOM BAND'S MINIMUM* AT 0 OF 8
(panel, k) RUNGS. (2) THE B136 CANDIDATE STILL CLEARS 4b TO k = 10 BUT BREAKS AT k = 20, AND
EVERY BREAK IS THE *CAGR FLOOR*. (3) U56's 4b PASS IS KILLED AT k = 5, BY 0.04 pp. (4) 4a DIES A
THIRD TIME, 0 OF 8 ON BOTH BARS.**

Script `research/backtests/2026-09-20_adversarial-survivor-deletion_B.py`; artifacts `.books.csv.gz`
(266 books) / `.walkforward.csv` (90 rule-8 picks) / `.summary.csv` / `.asymmetry.csv` /
`.wf_summary.csv` / `.gates.csv` / `.log.txt` / `.console.txt`. **Gates 10 of 10**, including an
exact reproduction of idea 2034's published candidate (max abs d = **4.441e-16**) and of idea
1799's verbatim drift loop (5.551e-15 on returns, turnover and gross).

## The defect this closes

Idea 2050 deleted `k` names **uniformly at random** from the candidate's panel, found the 4b leg
survives **800 of 800** draws, and stated its own limit verbatim: *"random deletion is NOT a
point-in-time correction — it removes survivors at random where history removes losers — so it
bounds the verdict's SENSITIVITY to the name set and does not de-bias the LEVELS."* B136 and U56
are CURRENT-constituent lists, so their bias is **directional**: the list over-includes names that
went on to win. Nobody had run that direction. This does.

## Construction

The standing cell (`VOLTGT t = 0.10, DRIFT h = 0.08, trade W, ENGINE phase, t+1, 10 bps`) is
re-scored on deleted panels with the whole book rebuilt on what is left (equal-weight basket,
realised panel vol driving the gross scalar, drift trigger, turnover). Two dials, both REPORTED at
every rung rather than argmaxed: `k` in {5, 10, 20, 40} x RULE in {**BEST** (delete the k highest
full-sample annualised returns), **BEST_IS** (the same, ranked on 2009-2016 only — ex-ante
readable), **WORST** (the opposite direction), **RANDOM** (30 seeded draws — 2050's own null,
re-run in this script as the control band)}. Nothing is tuned. Path 4a is scored against BOTH a
FIXED bar (live RULES v2 on the full panel) and a MATCHED bar (live RULES v2 rebuilt on the same
deleted names); path 4b's SPY bar is deletion-invariant by construction.

The deleted names are exactly the survivorship poster children: B136 BEST-5 = PLTR, AVGO, TSLA,
ANET, NVDA; B136 BEST_IS-5 = NFLX, TSLA, AVGO, REGN, BKNG.

## (A) THE RANDOM NULL NEVER COVERS THE SURVIVORSHIP DIRECTION — 0 OF 8

| panel | k | BEST Sharpe | BEST_IS | WORST | RANDOM mean | RANDOM min | RANDOM max | BEST inside band |
|---|---|---|---|---|---|---|---|---|
| U56 | 5 | 1.0932 | 1.1265 | 1.2715 | 1.2363 | 1.1830 | 1.2860 | **no** |
| U56 | 10 | 1.0021 | 1.0162 | 1.2529 | 1.2234 | 1.1377 | 1.3121 | **no** |
| U56 | 20 | 0.8021 | 0.9171 | 1.3578 | 1.2297 | 1.1105 | 1.3474 | **no** |
| U56 | 40 | 0.4457 | 0.4629 | 1.5266 | 1.1463 | 0.9233 | 1.4035 | **no** |
| B136 | 5 | 1.1603 | 1.1793 | 1.2403 | 1.2225 | 1.1827 | 1.2420 | **no** |
| B136 | 10 | 1.1266 | 1.1559 | 1.2210 | 1.2126 | 1.1867 | 1.2358 | **no** |
| B136 | 20 | 1.0662 | 1.1100 | 1.2396 | 1.2110 | 1.1735 | 1.2641 | **no** |
| B136 | 40 | 0.9832 | 1.0458 | 1.2980 | 1.2113 | 1.1767 | 1.2626 | **no** |

At **every** rung the adversarial book reads below the *minimum* of 30 random draws at the same
`k`. A 800-of-800 random-deletion record is therefore **not** evidence about survivorship: it is
evidence about a null whose support does not reach the survivorship direction at all. This is the
general lesson, and it applies to every name-set robustness claim in the record.

## (B) B136: THE CANDIDATE HOLDS TO k = 10 AND BREAKS AT k = 20 — ALWAYS THROUGH THE CAGR FLOOR

| rule | k | frac | CAGR | Sharpe | MaxDD | OOS CAGR / Sharpe / MaxDD | L5_CAGR | L4_DD | 4b |
|---|---|---|---|---|---|---|---|---|---|
| — | 0 | 0% | 12.51% | 1.2286 | -11.81% | 13.01% / 1.2928 / -11.81% | +0.0192 | +0.0842 | PASS |
| BEST | 5 | 3.7% | 11.62% | 1.1603 | -12.76% | 11.81% / 1.2019 / -12.76% | +0.0103 | +0.0747 | PASS |
| BEST | 10 | 7.4% | 11.14% | 1.1266 | -12.79% | 11.43% / 1.1722 / -12.79% | +0.0056 | +0.0744 | PASS |
| BEST | 20 | 14.7% | 10.38% | 1.0662 | -12.95% | 10.64% / 1.1103 / -12.95% | **-0.0021** | +0.0728 | **FAIL** |
| BEST | 40 | 29.4% | 9.35% | 0.9832 | -13.27% | 9.54% / 1.0192 / -13.27% | **-0.0123** | +0.0696 | **FAIL** |
| BEST_IS | 5 | 3.7% | 11.86% | 1.1793 | -12.89% | 12.67% / 1.2687 / -12.89% | +0.0127 | +0.0734 | PASS |
| BEST_IS | 10 | 7.4% | 11.58% | 1.1559 | -12.90% | 12.44% / 1.2502 / -12.90% | +0.0099 | +0.0733 | PASS |
| BEST_IS | 20 | 14.7% | 11.08% | 1.1100 | -12.94% | 12.18% / 1.2201 / -12.94% | +0.0050 | +0.0729 | PASS |
| BEST_IS | 40 | 29.4% | 10.30% | 1.0458 | -13.53% | 11.62% / 1.1762 / -13.53% | **-0.0028** | +0.0670 | **FAIL** |

**5 of 8 adversarial rungs keep 4b; all 4 rungs at k <= 10 keep it.** Every one of the three
failures is `L5_CAGR` — the `0.70 x SPY` CAGR floor of 10.59% — and **not one is drawdown**: the
`L4_DD` margin never falls below +6.70 pp, and both Sharpe halves and the OOS Sharpe leg stay
positive at every rung (worst `L1_H1` +0.0606, worst `L3_OOS` +0.1455). The memo's own caveat 7
called the CAGR leg's +1.92 pp the thin margin; this is the axis that spends it.

## (C) U56 IS KILLED AT k = 5, BY 0.04 pp

BEST-5 on U56 reads **10.55% / 1.0932 / -13.01%** against a CAGR floor of 10.59%: `L5_CAGR`
**-0.0004**, a **0.04 pp** miss, with every other leg still clearing (the OOS legs all pass).
BEST-10 misses by 1.29 pp, BEST-20 by 3.41 pp and BEST-40 by 7.11 pp (and at k = 40 all five legs
fail, MaxDD -26.39%). Deleting **five names of fifty-six** ends U56's 4b pass. Published with the
margin, per the record's own standing residue: this is a verdict 0.04 pp wide, not a fact.

## (D) 4a DIES A THIRD TIME — 0 OF 8, BOTH BARS

On B136 the 4a leg fails at **every** adversarial rung on the FIXED bar and on the MATCHED bar
alike (0 of 8 / 0 of 8), where the RANDOM control at the same `k` still passes 0.800 / 0.667 /
0.500 / 0.233. After latency-cost-phase (idea 2054) and random deletion (idea 2050), this is the
third independent axis to kill it, and it fails on the **same leg as the other two plus one
more**: **MaxDD is implicated in 8 of 8** (the candidate's drawdown deepens -11.81% -> -12.76% at
k = 5 and -13.53% at k = 40, through the live book's -12.24% each time, exactly the 0.43 pp margin
ideas 2050 and 2054 both spent), and the **H1 Sharpe leg joins at 6 of 8** (H2 at 1 of 8) because
deleting the winners removes return the live book keeps. The MATCHED bar moves the live book's own
drawdown the other way (-12.24% -> -10.53% at k = 40), so the matched reading is not a rescue.

## (E) RULE 8 — IS 2009-2016 CHOOSES, 2017-2026 READ ONCE, ON THE ADVERSARIAL PANELS

The legal IS-only chooser (argmax min IS 4b-leg slack, idea 2034's own) re-picks `t` and `h` over
the inherited 5 x 10 ladder at every deleted panel. On B136 it reaches a 4b-clearing book at only
**4 of 8** adversarial panels (undeleted reference 1 of 1; the RANDOM control 32 of 32), mean OOS
**13.22% / 1.1539 / -17.93%** against **SPY OOS 15.26% / 0.8737 / -33.72%** and **live RULES v2
OOS 7.85% / 1.1017 / -12.24%**. So the reached book still beats both OOS Sharpe bars on average,
and the reach halves. **All four rule-8 failures are `L4_DD`** — the IS window, stripped of its
winners, pushes the chooser to aggressive cells (`t = 0.16/0.20`, `h = 0.25`) whose OOS drawdown
breaches the -20.23% cap, at -20.40% to -22.68%. The candidate's own `t = 0.10` is picked at 2 of
8 and its `h = 0.08` at **0 of 8**, against 1.000 / 0.375 on the random control: adversarial
deletion moves the TARGET dial that random deletion left stable at 57 of 60.

U56: the chooser reaches 4b at 2 of 8 adversarial panels (BEST-5 and BEST_IS-5 only).

## Verdicts (pre-stated, not adjusted after)

* **V1 PARTIAL on B136 / KILL on U56.** B136 keeps 4b at 4 of 4 rungs with k <= 10 and breaks at
  k = 20 (BEST) and k = 40 (both rules). U56 breaks at k = 5. The standing candidate is **not
  withdrawn** — it is **qualified**: its 4b pass tolerates deleting the 10 best names of 136
  (7.4%) and not the 20 best (14.7%).
* **V2 KILL, third axis.** 4a 0 of 8 on both bars.
* **V3** every candidate-cell failure is `L5_CAGR`; every rule-8 failure is `L4_DD`.
* **V4** reach 4 of 8 on B136, 2 of 8 on U56.
* **V5 KILL of the generalisation.** 0 of 8 rungs put BEST inside the RANDOM band. Idea 2050's
  800-of-800 answers "is this cell a *particular* name-set accident" and must not be quoted as
  "this cell is survivorship-robust".

## What this run cannot do (stated, not repaired)

Deleting winners **bounds** survivorship bias; it does not correct it. History does not delete the
biggest winners — it fails to list the losers that were there at the time and are absent today,
and nothing offline can put a delisted 2011 name back. `BEST` also chooses its deletion with the
whole tape in hand (look-ahead in the STRESS, never in the book), so its levels are pessimistic by
construction; `BEST_IS` is the ex-ante readable version and both are published side by side. The
`k` ladder is ABSOLUTE, so k = 40 is 71.4% of U56 and 29.4% of B136 — the per-panel shares are NOT
deletion-matched and must not be compared across panels. SMALL665 is not run (six committed
confirmations that this family clears 4b 0 of N on small caps).

**SURVIVORSHIP.** U56 and B136 are CURRENT-constituent lists; every LEVEL here is optimistic and
both 4b bars are easier than on a point-in-time panel. That is precisely what this run bounds, and
the bound is one-sided.

**NO NEW KEEP IS FILED and no rules change** (rule 6; RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py untouched). This run prices an existing candidate; the standing memo
`2026-09-20_voltgt-drift-b136_KEEP4b_MEMO.md` gains a third addendum.
