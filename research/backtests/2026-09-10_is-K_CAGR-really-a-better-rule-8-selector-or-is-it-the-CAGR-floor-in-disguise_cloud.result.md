# Idea 415 — is K_CAGR really a better rule-8 selector, or is it the CAGR floor in disguise?
(cloud, 2026-09-10)

**ANSWERED — BOTH, and then the whole gap dies out of corpus. KILL of K_CAGR as a rule-8
selector, and a KILL of the record's habit of ORDERING selectors at all. No RULES change, no new
KEEP, no memo; `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched.**

Script `research/backtests/2026-09-10_is-K_CAGR-really-a-better-rule-8-selector-or-is-it-the-CAGR-floor-in-disguise_cloud.py`
Artefacts `.txt` `.rescore.csv` (360 re-scored picks) `.grid.csv` (264 fresh arm-rows)
`.picks.csv` (475 fresh picks) `.wf.csv`.

Two tuned parameters, as the queue allows and identical to idea 142's: **SELECTOR** (5, incl. a
seeded K_Random control) × **SCREEN** (S0 none / S1 IS-4b with the CAGR floor φ=0.70 / S2 the
same with the floor deleted). Panel, book variant, dial family, cost rung and scoring metric are
reported axes, never selected on. 10 and 25 bps, next-day execution.

---

## GATES — six, pre-registered, all pass

* **G1** `fast_run` vs `engine.backtest`: returns **2.572e-16**, turnover **0.000e+00** (bar 1e-12).
* **G2** live RULES v2 u56 @10 bps **8.66% / 1.2056 / −12.05%**, the record's number.
* **G3** derived cost rung `r(c) = r(0) − turnover·c/1e4` vs a live 25-bps engine run **2.572e-16**.
* **G4** idea 142's committed grid: 816 rows / 48 cells, KEEP paths **4b 88 / 4a_v2 5 / BOTH 2** —
  its published counts, exactly.
* **G5a** its picks **re-derived** from its own grid: **565 of 576** exact. The 11 misses are all
  **exact float-equal ties in the committed CSV** and they are **not immaterial** —
  max |ΔOOS_Sharpe| over them **4.746e-02**, and re-deriving moves the published 48-cell gap by
  **+0.0006**. Pandas round-trips a 1e-17 inequality to an exact tie and the tie-break is then
  arbitrary. **Consequence adopted here: PARTS A and B score idea 142's OWN COMMITTED PICKS**,
  joined to its grid for the columns `picks.csv` does not carry; the re-derivation is the gate only.
* **G6** those committed picks reproduce the headline under test: 48-cell K_CAGR − K_Sharpe =
  **+0.0415 (t 3.34)** against published +0.0415 (t 3.34). **Exact.**

---

## PART A — the queue's test, run on both channels the floor can act through

360 (selector × screen × cell) picks, five scoring metrics. Paired within cell.

| screen | n | metric | K_Sharpe | K_Calmar | K_MaxDD | K_CAGR | K_CAGR−K_Sharpe | t |
|---|---|---|---|---|---|---|---|---|
| S0 | 48 | OOS Sharpe | 0.8414 | 0.8502 | 0.7980 | **0.8829** | **+0.0415** | +3.34 |
| S0 | 48 | OOS MaxDD pp | −22.60 | −23.20 | −16.90 | **−24.50** | **−1.90** | −3.29 |
| S0 | 48 | OOS CAGR pp | 11.56 | 11.70 | 8.72 | 12.99 | +1.43 | +5.60 |
| S0 | 48 | **4b pass φ=0.70** | 0.125 | 0.125 | 0.042 | 0.146 | **+0.021** | +0.37 |
| S0 | 48 | **4b pass φ=0.00** | 0.250 | 0.250 | 0.333 | 0.208 | **−0.042** | −1.00 |
| S1 | 19 | OOS Sharpe | 1.0404 | 1.0440 | 1.0418 | 1.0535 | +0.0131 | +1.83 |
| S1 | 19 | 4b pass φ=0.70 → φ=0.00 | 0.474 | 0.474 | 0.632 | 0.421 | **−0.053 → −0.053** | |
| S2 | 23 | OOS Sharpe | 1.0445 | 1.0456 | 1.0562 | 1.0614 | +0.0169 | +2.41 |
| S2 | 23 | **4b pass φ=0.70** | 0.261 | 0.261 | 0.130 | **0.391** | **+0.130** | +1.37 |
| S2 | 23 | **4b pass φ=0.00** | 0.522 | 0.522 | 0.652 | 0.522 | **+0.000** | 0.00 |

**(1) ON THE BAR THAT ACTUALLY DECIDES A KEEP, THE QUEUE IS RIGHT AND THE ANSWER IS CLEAN.**
Re-scored on the 4b verdict, K_CAGR's advantage over the incumbent is **+0.021 → −0.042** when
the floor is deleted (S0) and **+0.130 → exactly +0.000** (S2). On S1 it is negative at both φ.
There is no reading of the 4b pass rate on which K_CAGR beats IS-Sharpe once φ=0. **K_CAGR is
the CAGR floor, not a selector, exactly as idea 415 predicted.**

**(2) ON OOS SHARPE THE GAP SURVIVES THE FLOOR — because OOS Sharpe contains no floor.** It is
still +0.0415 / +0.0131 / +0.0169 across the three screens. That half of the question is answered
by PART B and PART C, not by φ.

**(3) THE QUEUE'S SECOND ASK — OOS DRAWDOWN — REVERSES THE VERDICT ON ITS OWN.** On every screen
K_CAGR has the **deepest** OOS drawdown of the four selectors (−24.50 pp vs the incumbent's
−22.60 and K_MaxDD's −16.90 at S0). Whatever the OOS-Sharpe gap is, it is not free.

---

## PART B — where the surviving OOS-Sharpe gap lives (idea 142's corpus, S0, 48 cells)

* **It is an exposure trade.** K_CAGR − K_Sharpe: realised gross **+0.0724**, OOS MaxDD
  **−1.90 pp**, OOS Sharpe +0.0415. K_CAGR picks the higher-gross arm in **29 of 48** cells and
  the deeper-drawdown arm in 18 of 48.
* **It rests on 30 cells, not 48.** The two selectors pick the **same arm in 18 of 48** cells
  (gap identically 0 there). On the 30 disagreeing cells the gap is **+0.0664 (t +3.58), 25W/5L**.
* **By panel:** broad **+0.0430** (t +3.21, 16 disagreeing), small **+0.0605** (t +1.38, 5),
  u56 **+0.0274** (t +2.66, 9).
* **By the picked arm's own binding 4b bar** (the queue's hypothesis read directly): where the
  binding bar includes the CAGR floor the gap is **+0.0883 (n 18, t +3.02)**; where it does not,
  **+0.0135 (n 30, t +2.53)** — a 6.5× concentration in exactly the cells the queue named. This
  is correlational (OOS Sharpe contains no floor); the causal tests are PART A's φ re-scoring and
  PART C's replication.

---

## PART C — the out-of-corpus replication idea 142 itself asked for

A fresh corpus sharing **zero arms** with idea 142's overlay corpus: one parametric book
(200d-MA band gate with hysteresis, optional vol20 < 0.60 eligibility, optionally ranked to the
top-n by the record's composite without the vol scaler, equal weight at gross/k, remainder cash)
swept over four **dial** families — gross (7), band width (6), cadence (4), top-n (5) —
× 3 panels × 2 book variants × 2 rungs = **48 cells, 264 arm-rows, every point committed**.
Clean PROTOCOL rule 8: selectors and screens read ≤ 2016-12-31 only, 2017-01-01.. read once.

KEEP paths on all 264 arms: **4b(φ=0.70) 64, 4b(φ=0.00) 111**; binding 4b bar CAGR 95 / DD 66 /
H2 55 / H1 33 / OOS 15. The IS screen S1 admits 56 of 264 arms and **admits nothing in 26 of 48
cells**.

| screen | n | metric | K_Sharpe | K_Calmar | K_MaxDD | K_CAGR | K_Random | K_CAGR−K_Sharpe | t |
|---|---|---|---|---|---|---|---|---|---|
| S0 | 48 | OOS Sharpe | 0.8723 | 0.8890 | **0.8921** | 0.8521 | 0.8505 | **−0.0201** | **−1.78** |
| S0 | 48 | OOS MaxDD pp | −28.25 | −24.59 | −20.57 | **−29.26** | −25.68 | −1.01 | −3.38 |
| S0 | 48 | 4b pass φ=0.70 | 0.188 | 0.333 | **0.417** | **0.083** | 0.312 | **−0.104** | −2.34 |
| S0 | 48 | 4b pass φ=0.00 | 0.229 | 0.375 | **0.667** | **0.083** | 0.438 | **−0.146** | −2.83 |
| S1 | 22 | OOS Sharpe | 1.1063 | 1.1124 | 1.1133 | 1.1151 | 1.1103 | +0.0087 | +1.81 |
| S2 | 25 | OOS Sharpe | 1.1178 | 1.1249 | 1.1269 | 1.1255 | 1.1199 | +0.0077 | +1.80 |

**(1) THE GAP DOES NOT REPLICATE. IT REVERSES.** Unscreened, K_CAGR − K_Sharpe is **−0.0201
(t −1.78)** against idea 142's **+0.0415 (t +3.34)** — same statistic, same construction, a
corpus that shares no arms.

**(2) K_CAGR IS INDISTINGUISHABLE FROM A COIN FLIP.** Its 0.8521 sits **0.0016** above the
seeded K_Random control (0.8505) and **last of the five** selectors. On the 4b pass rate it is
last at both φ (0.083 against K_Random's 0.312/0.438), and on OOS drawdown it is last as well.

**(3) THE WHOLE ORDERING INVERTS.** K_MaxDD, which idea 142 killed at **−0.0434** on its corpus
(0.7980, last of four), is **first here** (0.8921), with the shallowest OOS drawdown and the best
4b pass rate at both φ (0.417 / 0.667). K_CAGR goes first → last, K_MaxDD last → first. **No
selector ordering in this record has been shown to transfer between corpora, and this run is the
counter-example.**

**(4) UNDER EITHER IS SCREEN NOTHING SEPARATES THE SELECTORS.** The S1/S2 gaps are +0.0087 and
+0.0077 with the 4b pass rates **identical at φ=0.70 and φ=0.00 (gap exactly 0.000)** — the
screen has already spent whatever information the floor carried.

**Rule 8 read once** (S0 picks, means over 16 cells per panel), against RULES v2 and SPY:

| panel | RULES v2 OOS | SPY OOS | best selector OOS | K_CAGR OOS | beats v2 | beats SPY |
|---|---|---|---|---|---|---|
| u56 | 9.53% / 1.2851 / −12.05% | 15.45% / 0.8820 / −33.72% | K_MaxDD 10.57% / **1.1782** / −14.33% | 15.82% / **1.0812** / −22.66% | **0 of 16 for every selector** | 15–16 of 16 |
| broad | 7.98% / 1.1185 / −12.24% | same | K_Calmar 12.90% / **1.0426** / −21.40% | 14.31% / 0.9971 / −23.71% | 0–2 of 16 | 13–16 of 16 |
| small | 3.85% / 0.5680 / −14.68% | same | K_Sharpe 7.58% / 0.4832 / −41.30% | 7.48% / 0.4780 / −41.41% | 5–7 of 16 | **0 of 16** |

**No selector's picks beat the live book out of sample on u56 (0 of 16, all five).** On small,
every selector loses to SPY in 16 of 16 cells with drawdowns of −32 to −41%.

**By-product cross-check (unplanned, and worth the record's attention):** the highest-OOS-Sharpe
arm in the entire fresh corpus is **u56, band = 0.12, gross 0.75, weekly, 10 bps — 14.02% /
1.2264 / −19.42%**, which is idea 360's committed KEEP memo to four decimals, reproduced here
from an independently written book function. Every one of the 64 fresh 4b passers sits inside a
family the record has already filed a memo for (idea 360's band ladder, idea 420/423's gross
ladder), so **there is no new KEEP-candidate and no memo is filed.**

---

## The answer

**Is K_CAGR a better rule-8 selector, or the CAGR floor in disguise? On the 4b verdict it is the
floor (the advantage is exactly 0.000 once φ=0 and negative unscreened). On OOS Sharpe it is
neither — it is the gross dial, bought with 1.90 pp of drawdown — and out of corpus that gap
reverses to −0.0201 and lands K_CAGR below a seeded coin flip.**

**KILL.** The incumbent IS-Sharpe stands; no change to PROTOCOL rule 8 is warranted by idea 142's
gap, and idea 142's own caution ("a hypothesis for a pre-registered test, not a rule-8 change")
was correct.

**Bears on ideas 151 and 163, as the queue said.** Idea 163's "every selector wins on OOS
drawdown" is corpus-specific: on this fresh corpus K_CAGR loses on drawdown to every other
selector and to the random control. Any published selector claim in the record should carry the
corpus it was measured on, because this run shows the ordering can invert completely across two
corpora of the same size, panels, rungs and protocol.

**LIMITS.** 48 cells per corpus is small; the fresh corpus is one parametric book family, so
"out of corpus" means out of idea 142's ARM set, not out of the record's book universe; the
tie-break defect in G5a means published grids cannot always be re-derived to the pick, which
touches every re-analysis in the record that reads a committed CSV.

**SURVIVORSHIP:** broad136 and the small panel are current-constituent lists, the small panel
additionally carrying the record's terminal-dated `max_1d_move ≥ 1.0` screen (44 of 483 names
dropped, 439 kept), so no LEVEL above is achievable. The object of this run is the DIFFERENCE
BETWEEN SELECTORS inside a panel, which that bias does not move.
