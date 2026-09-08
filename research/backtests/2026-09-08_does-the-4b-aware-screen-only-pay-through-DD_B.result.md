# Idea 163 — does the 4b-aware screen only pay through DD?  (lane B, 2026-09-08)

**ANSWERED / SPLIT. The queue's intuition is right about the SELECTOR and wrong about the
SCREEN — and the pooled number that made it look right is 95.3% fallback artefact.
No book promoted. PROTOCOL.md, RULES.md, scan.py, bot.py, baseline.py untouched.**

Census of every committed grid in the record carrying a 4b-aware admission mask — 132 (18
cells), 142 (48), 151 (72), 416 (72, zero (panel,book) overlap with 142/151, so an
out-of-corpus replication). **Verdict gate: all 4 files reproduce EVERY deterministic
committed pick arm-for-arm from their own grid (216/216, 576/576, 576/576, 576/576).**
1,104 census rows, 150 distinct (panel,book,cost) cells, 4 panels, 3 cost rungs, 0 tuned
parameters. Everything is IS-chosen (through 2016-12-31) and read once on 2017-01-01..2026,
so every line below is rule 8.

## 1. The pooled reading says the screen COSTS drawdown — the opposite of idea 152's instance

Screened pick minus unscreened pick, same selector, same cell, MOVED cells only (n 363):
**d OOS MaxDD −3.30 pp (t −9.78, 83W/250L), d OOS Sharpe +0.0327 (t +7.05), d OOS CAGR
+2.03 pp (t +12.13)**. Negative DD sign in **4 of 4 files** (−6.30 / −3.93 / −3.91 / −2.73 pp).
S2 (the same screen with the CAGR floor deleted) is larger, not smaller: −4.57 pp — so the
CAGR floor is not the mechanism.

## 2. …but 95.3% of that drawdown move is the EMPTY-POOL FALLBACK, not screening

The screen admits **nothing** in most cells (median 0 of 17 arms admitted; pool empty in
281 of the 363 moved cells). When the pool is empty the "screened pick" *is* the ungated
control, i.e. the cell declines idea 94's whole de-risking menu. Split:

| subset | n | d OOS MaxDD | d OOS Sharpe | d OOS CAGR |
|---|---|---|---|---|
| EMPTY-POOL (fell back to control) | 281 | **−4.06 pp (t −10.19)** | +0.0368 (t +6.57) | +2.33 pp (t +12.01) |
| LIVE-POOL, pick MOVED | 82 | **−0.69 pp (t −1.35, 39W/43L, sign p 0.74)** | +0.0186 (t +2.62) | +0.98 pp (t +3.30) |
| LIVE-POOL, pick UNCHANGED | 198 | 0 | 0 | 0 |

Per file, LIVE-POOL/MOVED d OOS MaxDD: 132 −1.11 (t −0.56), 142 −1.48 (t −2.08),
151 −1.62 (t −2.71), 416 **+0.06 (t +0.07)** — positive in 1 of 4.
**Screening inside a live pool is a NULL on drawdown and a small positive on return.**
Idea 152's instance does not generalise; it is one draw from a distribution centred on zero.

## 3. The reconciliation: rescored on drawdown, EVERY selector beats do-nothing

Selector minus do-nothing (hold the cell's ungated control), pooled distinct cells,
unscreened pool: **OOS MaxDD +0.38 / +1.96 / +8.60 / +1.76 pp (K_CAGR / K_Calmar / K_MaxDD /
K_Sharpe), all t ≥ +2.33**, while on OOS Sharpe the same picks are +0.003 / −0.011 / −0.059 /
−0.014 (three negative). This is exactly idea 163's sentence — but the object it is true of is
the SELECTOR (equivalently idea 418's menu), not the screen. It also reproduces 416's exchange
rate: K_MaxDD pays −4.45 pp OOS CAGR for +8.60 pp of shallower drawdown.

## 4. KEEP paths — the screen buys 4b passes, through CAGR, not through DD

Pooled distinct, S1: 4a(v2) unscreened 31/600 vs screened 32/600 (**net +1**); 4b(full) 86 vs
129 (**net +43**, gains 46 / loses 3); 4b(OOS window) 94/576 vs 131/576 (**net +37**). BOTH
PATHS 8 vs 11 of 816. The screen's 4b gains sit on the CAGR floor, which is the bar its own
picks move (+2.03 pp OOS CAGR), while its OOS drawdown gets **deeper** — consistent with the
record's finding that the CAGR floor and the DD cap are near-disjoint bars (idea 150 census).

## 5. Levels (freshly computed from research/baseline.py, OOS 2017-01-01..)

RULES v2 @10 bps: CAGR 9.53%, Sharpe 1.2851, MaxDD −12.05% (@25 bps 9.24% / 1.2483 / −12.09%).
SPY: CAGR 15.45%, Sharpe 0.8820, MaxDD −33.72% → 4b OOS bars 10.82% / −20.23%.
Census means (600 distinct S1 rows): do-nothing control 13.97% / 0.9328 / −25.63%; unscreened
pick 12.29% / 0.9125 / −22.46%; screened pick 13.52% / 0.9322 / −24.45%.
Survivorship (idea 54) inflates every level here; read the contrasts, not the levels.

## What this changes

PROTOCOL rule 8's IS-4b screen should **not** be described as drawdown insurance. On its own
object it does nothing measurable to OOS drawdown; what it reliably does is push picks toward
return (+0.98 pp OOS CAGR inside a live pool) and, in the majority of cells, refuse the menu
entirely — and refusing the menu costs 4.06 pp of OOS drawdown for 2.33 pp of OOS CAGR.
The drawdown claim belongs to the MENU (idea 418) and to the SELECTOR rescored on drawdown
(§3), which is where idea 163's sentence should be filed. Corroborates idea 140
("abstention is the screen's COST, selection is the only thing it earns") on an independent
corpus and construction.
