# Idea 655 — put a ROW ID on every artefact that RE-READS another artefact

**lane C, 2026-09-10 · KILL for capital, ANSWERED for the record · premise HALF falsified, HALF confirmed and WORSE**

Script: `2026-09-10_put-a-ROW-ID-on-every-artefact-that-RE-READS-another-artefact_C.py` (344.9 s, deterministic, no network).
Artefacts: `.pointers.csv` (246) `.join.csv` (246) `.censusgrid.csv` (9) `.pricing.csv` `.grid.csv` (126) `.walkforward.csv` (6) `.keeppaths.csv` (6) `.console.txt`.
**No RULES change, no book promoted, no KEEP claimed, no memo.** RULES.md, scan.py, bot.py, baseline.py and PROTOCOL.md untouched.

## Gates (all PASS, run before any new number was read)

| gate | result |
|---|---|
| G1 ROW-resolution book == `baseline.rules_v2_weights` | max&#124;dW&#124; **0.000e+00**, max&#124;dR&#124; **0.000e+00** |
| G2 cost-rung identity `r(25) = r(0) − turn·25/1e4` vs a live `engine.backtest(25)` | max&#124;d&#124; **0.000e+00** |
| G3 idea 653's ladder off its OWN committed artefacts | 96 blocks, 107,816 unstated at L0 → **105,303** at L4 (share **0.9767**), **1** survivor; that CSV independently recounted at **105,504** rows |
| G4 P1 ladder nested (STRICT ⊆ LOOSE ⊆ VALUE) on addressable rows | PASS |

## (1) The population — the record re-reads itself a million times

3,030 committed CSVs scanned against an index of 5,499 unique artefact basenames (473 ambiguous names dropped rather than guessed). A pointer instance must clear a **value** bar, not just a header regex — `parent_gross` is a number, not a pointer.

- **246 pointer instances** over **236 distinct files**, **1,088,554 pointer rows**, of which **1,088,251 (99.97%)** resolve to a committed artefact.
- Cumulative by form: STRICT 193 instances / 962,203 rows; +LOOSE 35 / 122,498; +VALUE 18 / 3,853.
- Targets: **88.07%** a committed `.csv`, **10.99%** a `.py`, **0.58%** a `.md`.

## (2) H2 — the queue's diagnosis of its own block is WRONG

QUEUE 655 asserts idea 653's dark block is unrecoverable "because 99.7% of its rows point at a MULTI-panel source through a `file` column with no ROW ID". Re-read row-wise against the sources as committed:

`2026-09-10_re-cut-…-STEP-NORMALISED-argmin_cloud.cells.csv` — 105,504 pointer rows:

| outcome | rows | share |
|---|---|---|
| **KEY-UNIQUE** (shared-column key tuple hits exactly one source row) | **66,762** | **0.6328** |
| key misses the source entirely | 29,127 | 0.2761 |
| ambiguous (key hits >1 source row) | 9,279 | 0.0879 |
| no shared key column at all | 336 | 0.0032 |

**63.28% of that block is already row-addressable with no row id at all.** The missing field is not what makes those 66,762 rows dark, because they are not dark.

## (3) …but at record scale the problem is far WORSE than one block

| | rows | share of pointer rows |
|---|---|---|
| J0 resolve to a committed artefact | 1,088,251 | 0.9997 |
| target is not row-shaped (`.py`/`.md`: a LINE is its row id) | 129,577 | 0.1190 |
| target CSV has exactly 1 row (trivially addressable) | 88 | 0.0001 |
| **target CSV has MANY rows — the population at risk** | **958,586** | **0.8806** |
| **J1 KEY-UNIQUE** | **198,353** | **0.1822** |
| ambiguous (key hits >1 source row) | 287,534 | 0.2641 |
| no shared key column at all | 326,856 | 0.3003 |
| key misses the source | 145,931 | 0.1341 |
| J2 explicit row-id column | 112,906 | 0.1037 |

Of the 958,586 at-risk rows, **198,265 (20.68%) are already key-unique** and **760,321 (79.32%) are genuinely dark** — 7.2× the block idea 653 flagged. The 3×3 grid (`.censusgrid.csv`) reports every point; the key-unique share is 0.1218 / 0.1829 / 0.1822 at STRICT / LOOSE / VALUE.

## (4) H3 — the convention is cheap, and half of it already exists

- Cost: 6 bytes/row × 1,088,554 rows = **6.53 MB** on a **599.36 MB** CSV corpus → **+1.090%**, i.e. **116,411 dark rows recovered per MB**.
- **41 of 246 instances already carry a row-id-shaped column** (112,906 rows, 10.37%) — but **94.94% of those rows point at a `.py`/`.md`**. The record already stamps a `line` on SOURCE-CODE pointers and stamps nothing on CSV pointers. The proposal is not a new convention; it is the existing one, applied to the other 88% of targets.

## (5) H4 — what ROW-LEVEL resolution is worth in a book

The artefact question ("do you know WHICH row, or only HOW MANY?") priced exactly: **ROW** holds every name whose own 200d ±3% band state is IN (= RULES v2); **AGG** knows only the breadth share and holds the whole priced panel at gross when breadth ≥ θ, else cash; **HYB** has both. 126 grid points, all reported; rule 8 fits (θ, gross) on 2009–2016 only.

Rule-8 picks, scored on 2017–2026 untouched:

| panel | mode | pick | OOS CAGR | OOS Sharpe | OOS MaxDD | 4b @ 0/10/25 bps |
|---|---|---|---|---|---|---|
| U56 | **ROW** | θ=0.00 g=1.00 | 12.71% | **1.278** | **−15.91%** | **1/1/1** |
| U56 | AGG | θ=0.20 g=1.00 | 16.48% | 1.079 | −29.18% | 0/0/0 |
| U56 | HYB | θ=0.30 g=1.00 | 12.66% | **1.285** | −15.91% | **1/1/1** |
| B136 | **ROW** | θ=0.00 g=1.00 | 10.66% | 1.117 | −16.16% | 1/1/0 |
| B136 | AGG | θ=0.20 g=1.00 | 16.05% | 1.069 | −25.59% | 0/0/0 |
| B136 | HYB | θ=0.20 g=1.00 | 10.46% | 1.101 | −16.16% | 1/0/0 |

References — U56: SPY OOS Sharpe 0.876 / CAGR 15.32% / MaxDD −33.72%, RULES v2 1.279 / 9.48% / −12.05%. B136: SPY 0.882 / 15.45% / −33.72%, v2 1.119 / 7.98% / −12.24%.

**Row resolution beats aggregate-only, and the whole gap is drawdown.** AGG buys *more* CAGR on both panels (+3.77 pp and +5.39 pp OOS) and pays for it with 13.3 and 9.4 pp of extra MaxDD, which is what fails 4b's cap (60% of SPY's −33.72% = −20.23%). Every mode beats SPY's OOS Sharpe; only the modes that know WHICH names clear the drawdown cap.

**But the passing arm is NOT promotable, and the reason is in the record already.** ROW's Sharpe is **flat in gross to 4 dp** — U56 1.2022 / 1.2021 / 1.2020 and B136 1.1057 / 1.1058 / 1.1057 at g = 0.50 / 0.75 / 1.00 — so the 4b pass at g=1.00 and the 4b failure at g=0.75 differ only through the CAGR floor. That is idea 311's gross-band loophole and open idea 657's exact question: this pass is a **pure exposure fact**, not a new book. ROW@g=1.00 *is* the live book with one dial moved.

Full-sample KEEP paths: **4a 3/126, 4b 14/126, BOTH 0/126.** No rule-8 pick clears 4a at any rung (0/6). The three 4a passers (U56 HYB θ=0.30 at g=0.50 and g=0.75, B136 AGG θ=0.60 at g=0.50) all fail 4b.

## Verdict

**KILL for capital. ANSWERED for the record.** Nothing is promoted: the only 4b-passing rule-8 arms are the live book at full gross, and their pass is decided by the gross dial alone. The infrastructure claim, however, survives in a stronger form than the queue stated it — the darkness is not the one block idea 653 named (63.28% of it is already joinable) but the other 760,321 rows the record never counted, and the fix is a convention the record already applies to source-code pointers, at +1.09% of corpus bytes.

Recommended follow-ups are filed to QUEUE as ideas 660–662.
