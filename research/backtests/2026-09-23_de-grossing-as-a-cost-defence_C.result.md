# idea 2443 (lane C, run 51, 2026-09-23) — IS DE-GROSSING A COST DEFENCE FOR THE CAPPED CANDIDATE AT 25 AND 50 bps?

**ANSWERED = NO, AND THE SIGN IS THE OPPOSITE OF THE PREMISE. KILL of de-grossing as a cost
defence. CONFIRM of idea 2431's breakeven measurement and of lane B run 50's "do not adopt"
recommendation on its 4a candidate — with the dominating alternative now priced directly.**

2424 published rows (2 panels x 2 books x 6 gross x 101 rungs), **22 of 22 gate entries pass**
(7 of them are PUBLISHED-not-asserted, i.e. the number IS the finding).

## What was run
`w_i = min(g / N_in, cap)` on names inside the 200d +/- 3% band, idle NAV swept to SHY at
phi = 1.00 — idea 2300's `CAND` (cap INF) and idea 2322's `CAP2` (cap 0.020). **TWO DIALS AND NO
MORE: gross `g` {0.40, 0.55, 0.70, **0.75 = the committed anchor**, 0.85, 1.00} and the cost rung
`c` on a 1-bp ladder 0..100 (101 rungs, containing 10, 25 and 50 exactly).** Reported never
selected on: panels {U56, B136}, books {CAP2, CAND}, weekly cadence, t+1, band 0.03, the SHY
sweep. SMALL is not priced because 2318 / 2322 / 2326 / 2343 each published SMALL's 4b pass count
at 0 of 40-120 — there is no pass there whose death rung could be walked.

Gates: **G1** the linear cost identity `r(c) = r0 - turnover x c/1e4` is `engine.backtest(cost_bps=c)`
to **max|d| 0.000e+00** at 10/25/50/100 bps on four independent books, so the 101-rung ladder is
exact and not an approximation. **G2/G3** reproduce the two committed g=0.75 headlines (CAP2 U56
11.62% / 1.2687 / -14.81%, OOS 12.77% / 1.3318, 3.51x; CAND U56 12.5950% / 1.1934 / -17.3923%) to
max|d| 2.5e-05 and 4.0e-05. **G4** no leverage (peak gross 1.000000000). **G5** every 4a/4b leg is
a DOWN-SET along the cost ladder — 0 violations over 24 cells x 7 legs — so a death rung is well
defined. **G5b** Sharpe and CAGR strictly decreasing in `c` in 24 of 24 cells.

## THE ANSWER — the 4b death rung FALLS as gross falls
Read each ladder from g = 1.00 DOWN to g = 0.40 (`never` = already failing at 0 bps):

| panel / book | g1.00 | g0.85 | g0.75 | g0.70 | g0.55 | g0.40 | rises / falls |
|---|---|---|---|---|---|---|---|
| U56 / CAP2  | 54 | 52 | **34** | 19 | never | never | 0 / 4 |
| U56 / CAND  | never | 49 | **49** | 35 | never | never | 1 / 2 |
| B136 / CAP2 | never | 42 | **33** | 21 | never | never | 1 / 3 |
| B136 / CAND | never | never | **35** | 23 | never | never | 1 / 2 |

**G10: 0 of 4 ladders are non-decreasing as gross falls; 11 falls against 3 rises over 20 steps.**
The defence hypothesis predicted the opposite in every cell. Below g = 0.70 the 4b pass is dead at
**0 bps** in 8 of 8 (panel, book) cells, so there is no cost tolerance left to measure at all:
de-grossing does not buy an operator room to pay a real spread, it **removes the room the book
already had**. At 25 bps the pass survives in 9 of 24 rows and **every one of them sits at
g >= 0.70**; at 50 bps 2 of 24 survive and both sit at **g >= 0.85**.

## The mechanism, measured rather than asserted
De-grossing is a near-exact SCALE dial on the bill and is therefore powerless on a ratio, while
4b's bars are ABSOLUTE:

- **Turnover is proportional to gross.** `turnover / g` spreads only 5.68..6.21 (cv 0.032) on
  U56/CAND, 6.32..6.93 (cv 0.034) on B136/CAND, 5.83..6.84 (cv 0.057) on B136/CAP2 — the widest
  is U56/CAP2 at 3.99..5.79 (cv 0.133), and that is the 2% cap unbinding as gross falls, not an
  efficiency gain. Raw turnover falls 3.99x -> 2.32x on U56/CAP2.
- **CAGR is proportional to gross too.** `CAGR@10 / g` spreads 12.66..17.91% on U56/CAP2 and
  15.06..17.46% on B136/CAP2. Both scale-free ratios are flat; only the LEVELS move.
- **`L_CAGR` is the only non-scale-free bar and it binds first.** The CAGR floor is 0.70 x SPY =
  **10.66%** (U56) / 10.58% (B136). Margin at 10 bps, in pp, U56/CAP2: **+2.00 / +1.75 / +0.96 /
  +0.36 / -1.50 / -3.50** at g = 1.00 / 0.85 / 0.75 / 0.70 / 0.55 / 0.40. The book walks straight
  through the floor between g = 0.70 and g = 0.55, and `L_CAGR` is the binding leg at the death
  rung in **4 of 4 cells at every g <= 0.75**.
- **The absolute cost budget shrinks too.** Annual bill payable at the death rung, U56/CAP2:
  **2.16 / 1.95 / 1.19 / 0.64 pp of NAV per year** at g = 1.00 / 0.85 / 0.75 / 0.70. De-grossing
  loses cost room in BOTH units — the rung and the dollar bill.

## RULE 8 — and the tension it exposes, stated rather than smoothed
`g` fitted on warm-up..2016-12-31 ONLY by two pre-stated IS choosers (C_ISSHARPE, C_ISCALMAR),
2017-2026 read ONCE, 32 picks (2 panels x 2 books x 4 rungs x 2 choosers):

- **32 of 32 picks land on g = 0.40**, the most de-grossed book on the ladder, and **0 of 32 on
  the committed g = 0.75.** The IS operator wants a small book.
- Those picks **beat the live baseline OOS 32 of 32 and SPY OOS 32 of 32**, at mean OOS Sharpe
  **1.2497 against the committed cell's 1.1435 (+0.1063)**. De-grossing is a genuine RISK-ADJUSTED
  improvement out of sample, and this run does not hide that.
- **0 of 32 picks carry a full-sample 4b pass**, and the failure is `L_CAGR` alone in all 32.
  4b is written on absolute bars; the chooser optimises a ratio. **The two objectives disagree
  about the one dial an operator actually controls, and 4b is the path that governs capital.**

**The death rung is itself unstable walked forward (G12):** IS (<= 2016) vs OOS (2017-2026) death
rungs move by **-23 to +70 bps** with median +0 over 24 cells (U56/CAP2 g0.75: IS 3 -> OOS 60;
B136/CAP2 g0.75: IS 40 -> OOS 28). Consistent with 2431's finding; the breakeven is a full-sample
measurement and is documented as such, never as a forward-looking tolerance.

## The structural fact worth carrying forward: 4a and 4b are DISJOINT in gross
Over all 2424 rows, **4a passes 249 and 4b passes 458, and NO row passes both at any rung**:

| gross | 4a / 404 | 4a@base-pinned-10 / 404 | 4b / 404 |
|---|---|---|---|
| 0.40 | **196** | 117 | **0** |
| 0.55 | **53** | 29 | **0** |
| 0.70 | 0 | 0 | 102 |
| 0.75 | 0 | 0 | 155 |
| 0.85 | 0 | 0 | 146 |
| 1.00 | 0 | 0 | 55 |

Every 4a pass sits at g <= 0.55 and every 4b pass at g >= 0.70. 4a's MaxDD clause rewards holding
less; 4b's CAGR floor punishes it. On the one dial the operator controls, the two KEEP paths point
in **opposite directions** and their feasible sets do not intersect. This is the cleanest statement
the record has of why PROTOCOL rule 4 needed two paths, and it is the reason a 4a pass bought by
de-grossing is not progress toward capital.

## ONE 4a KEEP-CANDIDATE, FILED AND NOT ADOPTED
`CAP2 / g = 0.40` on U56 at 10 bps: **7.16% / 1.3375 / -8.15%**, halves **1.3510 / 1.3350** against
live RULES v2's 1.2262 / 1.1897 and MaxDD -12.05%, OOS **7.92% / 1.4072 / -8.15%**, turnover
**2.32x/yr** against the live book's 1.77x. 4a holds to **68 bps** (36 bps with the baseline pinned
at 10), and the same setting is **JOINT both-panel 4a at 0 / 10 / 25 bps on BOTH books** — which
lane B run 50's `FIX w* = 0.0125` candidate was not (U56 only) — and **rule 8 picks it 32 of 32**,
which that candidate was not (0 of 8). It nevertheless **fails 4b on `L_CAGR` alone by -3.50 pp**
(7.16% against the 10.66% floor), a WIDER miss than 2457's -2.26 pp.

**Recommendation: DO NOT ADOPT, and the reason is now a measurement rather than a judgement.** This
is not a new rule; it is the committed rule with `G` turned down, requiring no new clause — exactly
what run 50 said its own 4a candidate was "strictly dominated by". This run prices that dominating
alternative directly and confirms it is both stronger on 4a and further from 4b. Memo with exact
RULES wording: `2026-09-23_de-grossing-as-a-cost-defence_C.memo.md`.

## What did NOT change
No change to `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py` or `baseline.py` (rule 6). The live book
is unchanged. The standing 4b candidate is unchanged, and so are its `L_DD` leg and its 3.51x
turnover blocker: **the adoption bar published by idea 2431 (cut turnover 3.51x -> 2.42x, -31.0%,
at unchanged returns) stands, and this run closes de-grossing as a way to clear it.** A device that
cuts turnover without cutting exposure is still the only thing that would work.

Artefacts: `.grid.csv.gz` (2424 rows, gzipped for repo size; the script writes it uncompressed), `.cells.csv`, `.deathrung.csv`, `.monotonicity.csv`,
`.joint4b.csv`, `.walkforward.csv`, `.deathrung_walkforward.csv`, `.gates.csv`, `.console.txt`.
