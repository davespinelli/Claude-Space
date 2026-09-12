# Idea 831 (lane B, 2026-09-12) — how many of the record's committed 4b passes survive their own entry-date census?

**ANSWERED = NONE OF THEM, AND THE RECORD'S OWN HEADLINE DOES NOT EVEN ORDER THEM.**
Script: `2026-09-12_how-many-of-the-record-s-committed-4b-PASSES-survive-their-OWN-ENTRY-DATE-CENSUS_B.py`

## What was scored
The record's committed, reconstructible 4b/KEEP memo corpus — **12 books**: `K1..K8`, the
gate-verified corpus of ideas 641/574, each at its **own memo gross**, plus `R1..R4`, the four
further 4b memos filed 2026-09-11/12 (u56 band 0.08 g1.00, u56 MA-RESPREAD g0.75, u56
MA-DISTANCE top-half M g0.75, b136 R6-top20 g0.65) — against the LIVE RULES v2 book and retired
RULES v1 as comparands. **2 tuned parameters, the queue's own:** claim set (MEMO8 / MEMO12) and
horizon H (756d / 1260d). Entry spacing s ∈ {21, 63} is reported, not selected. 6,132
(book, H, s, entry) rows; every cell printed.

**Gates, before any new number: 12 of 12 PASS.** G1 — every book with a published triple
reproduces its own memo's (CAGR, Sharpe, MaxDD) inside the declared vintage tolerance (K2 and
V1 have no published triple and are marked so, not counted). G2 — LIVE reproduces RULES v2's
committed 8.63% / 1.202 / −12.05%. **G3 — this run's census machinery reproduces idea 828/829's
committed entry-date share for the standing candidate (K5 g=1.00, H=756, s=21) at 0.3977 on 176
windows, |d| = 0.0000.**

## The answer

| bar | MEMO8 @ H=756 | MEMO12 @ H=756 | MEMO8 @ H=1260 | MEMO12 @ H=1260 |
|---|---|---|---|---|
| share ≥ 0.80 | **0 of 8** | **0 of 12** | **0 of 8** | **0 of 12** |
| share ≥ 0.50 | **0 of 8** | **0 of 12** | 5 of 8 | 7 of 12 |
| median share | 0.3210 | 0.2869 | 0.5526 | 0.5296 |

**Zero of the record's committed 4b passes clears 0.80 at a 3-year horizon, and zero clears even
0.50.** Identical at s=63 (0 / 0, median 0.3136 / 0.2797). The best book in the whole corpus is
**K4** (u56 EW-all 200d-MA gate, band 0, monthly, g=1.00) at **0.4432** of 176 windows; the worst
is K7 at 0.0057. Restricting to OOS entries (≥2017-01-01) — the most favourable window the
sample contains — the maximum is still only **0.6875** (K8), 0 of 12 at 0.80 and 5 of 12 at 0.50.

## The pass share beside the claim (H=756d, s=21d, n=176 windows each)

| book | what it is | fixed-window claim (CAGR/Sharpe/MaxDD) | 4b / 4a | **3y entry share** | binding leg |
|---|---|---|---|---|---|
| K4 | u56 EW-all MA gate b=0, M, g1.00 | 11.92% / 1.2095 / −15.49% | PASS / FAIL | **0.4432** | halves (80 of 98) |
| K8 | u56 EW-all, breadth de-gross, W, g1.00 | 14.16% / 1.2226 / −14.79% | PASS / FAIL | **0.4148** | halves 83, dd 72 |
| K5 | u56 RULES v2 b=0.03, W, g1.00 *(standing candidate)* | 11.54% / 1.2017 / −15.91% | PASS / FAIL | **0.3977** | halves 85, cagr 48 |
| K3 | u56 top20 DAILY + buffer m=50, D, g0.75 | 11.78% / 1.1582 / −12.37% | PASS / FAIL | **0.3636** | halves 94, dd 79 |
| R1 | u56 band 0.08, W, g1.00 | 11.39% / 1.1461 / −19.05% | PASS / FAIL | **0.3295** | halves 78, dd 74, cagr 70 |
| R3 | u56 MA-DISTANCE top-half, M, g0.75 | 15.38% / 1.2260 / −19.98% | PASS / FAIL | **0.2955** | dd 85, halves 59 |
| K6 | u56 band 0.12 EW respread, W, g0.75 | 13.97% / 1.2233 / −19.42% | PASS / FAIL | **0.2784** | dd 115 |
| R2 | u56 MA-RESPREAD, W, g0.75 | 11.51% / 1.0877 / −18.65% | PASS / FAIL | **0.1705** | dd 95, halves 82 |
| R4 | b136 R6-top20, W, g0.65 | 14.99% / 1.1264 / −19.43% | PASS / FAIL | **0.1364** | halves 106, dd 83 |
| K1 | u56 top20 composite, W, g0.75 | 12.78% / 1.0632 / −18.31% | PASS / FAIL | **0.1136** | dd 137, halves 114 |
| K2 | u56 top20 + buffer m=20, W, g0.75 | 12.82% / 1.1168 / −17.24% | PASS / FAIL | **0.1080** | dd 110, halves 93 |
| K7 | b136 EW + SHY residual, W, g0.375 | 6.22% / 1.1687 / −11.13% | **FAIL** / FAIL | **0.0057** | cagr (175 of 175) |
| *LIVE* | *RULES v2, W, g0.75 (comparand)* | *8.63% / 1.2018 / −12.05%* | *FAIL / —* | *0.1875* | *cagr 133* |
| *V1* | *RULES v1 (comparand)* | *6.41% / 0.6602 / −13.83%* | *FAIL / —* | *0.0114* | *halves 174* |

Honesty note on the denominator: **K7's memo is a 4a memo** (`…_4a_cloud_MEMO.md`), and on the
2026-09-12 vintage it fails 4b on the CAGR floor full **and** OOS. So the corpus carries **11**
fixed-window 4b passes, not 12 — and 11 of 11 re-derive their published 4b PASS here. **0 of 11
clears 0.80 or 0.50 on entry dates.** All 12 fail 4a against the live book, which is the
record's standing position.

## Why (the mechanism, measured not asserted)

1. **The binding leg is not the one the record worries about.** Summed over the 12 books'
   **1,574** failing windows at the headline cell, the window-local **halves** leg fails **975**
   times and the **DD** leg **898**, against **550** for CAGR and **211** for Sharpe. The fixed-window 4b verdict
   is dominated by the CAGR floor and the DD cap; the *entry-date* verdict is dominated by the
   requirement that the book beat SPY in **both halves of a short window**, which no book in the
   corpus does reliably. Two books bracket the point: K7's CAGR leg fails in
   **every one** of its 175 failing windows (a 6.2%/yr book never clears 70% of SPY's), while R3
   fails on *neither* Sharpe nor CAGR (leg shares 1.0000 / 1.0000) — only on DD (85) and halves
   (59).
2. **The record's published number does not order the entry-date share.** Spearman(full-sample
   Sharpe, 3-year entry share) = **+0.5385** (n = 12; Pearson +0.6384) against a pre-registered
   bar of +0.70 → **H_RANK FAILS**. Rank 1 by published Sharpe (R3, 1.2260) is rank **6** by entry
   share; rank 1 by entry share (K4) is rank 4 by published Sharpe; K7 is rank 6 by Sharpe and
   **last** by entry share.
3. **Horizon, not book, is the axis that moves the number** — idea 828's finding reproduces on a
   12-book corpus: share(1260) > share(756) at **12 of 12** books (H_HORIZON PASS), median
   0.3210 → 0.5526 on MEMO8. Nothing in the corpus buys the 0.80 bar; five years buys the 0.50
   one for 5 of 8.
4. **Gross is not the lever either.** The LIVE book (the same form as K5 at g=0.75) scores
   0.1875 against K5's 0.3977 — but its failures are 133 CAGR-leg failures against K5's 48, and
   its DD leg is 0.9545 against K5's 0.8636 (LIVE fails 143 of 176 windows: 133 CAGR, 85 halves,
   15 Sharpe, 8 DD). Raising gross trades one leg for the other exactly
   as idea 828 found; neither end of the dial approaches 0.80.

## Rule 8

**(a) On this run's own tuned axes — FAILS.** Picking (book, H) on IS entries alone (windows
closing ≤ 2016-12-31, 36–60 windows per cell) selects **(R3, 1260)** at IS share 0.8611 → OOS
share 1.0000, gap **0.1389** against the 0.10 bar, and the IS pick is **not** the OOS best
(K3 at 1260 reads 1.0000 on 56 OOS windows). Every book's IS share is far below its OOS share
(K3: 0.0000 → 0.6750 at H=756; K8: 0.0500 → 0.6875), i.e. **the entry-date pass share is a
property of the WINDOW, not of the book** — the same conclusion idea 828 reached at gap 0.1625.

**(b) Mandated book leg, OOS 2017-01-01 → 2026-09-11, read once** (full table in `.books.csv`):

| | K4 | K5 | K8 | R3 | LIVE (RULES v2) | SPY |
|---|---|---|---|---|---|---|
| OOS CAGR | 12.65% | 12.70% | 16.04% | 16.00% | 9.47% | 15.33% |
| OOS Sharpe | 1.2693 | 1.2775 | 1.3937 | 1.2154 | 1.2782 | 0.8767 |
| OOS MaxDD | −15.49% | −15.91% | −12.72% | −19.98% | −12.05% | −33.72% |

Every candidate beats SPY's OOS Sharpe and drawdown. Only **two** beat the live book's OOS
Sharpe of 1.2782 — K8 (1.3937) and K3 (1.2864) — and both still fail 4a, on the full-sample
drawdown leg (−14.79% and −12.37% against the live −12.05%) and, for K3, in both halves.

## Verdict — **KILL for capital. No KEEP claimed, no book promoted, no memo filed.**

4a: **0 of 12** books pass (every one is worse than the live book on drawdown, Sharpe or both).
4b on the fixed window: 11 of 12 pass, exactly as the record says. 4b on an entry-date census:
**0 of 12 at 0.80, 0 of 12 at 0.50, best 0.4432.** The record's 4b column is a one-window
statement, and this run prices what that costs: an entrant picking any committed 4b pass at a
uniformly random date and holding three years would have seen the claim hold **between 0.6% and
44% of the time**.

**PROTOCOL line PROPOSED, not applied** (rule 6 — Sunday review only; `PROTOCOL.md` untouched):
*"Every 4b verdict must be published beside its entry-date pass share at H = 756d, s = 21d, or
be marked ONE-WINDOW."*

Follow-ups filed: 832, 833.

**Files not modified:** `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py`.
**Survivorship:** `universe.json` and `universe_broad.json` are current-constituent lists, so
every LEVEL here is optimistic; the object of the run is a within-corpus contrast.
