# Idea 576 — PARK memo (NOT a RULES proposal, NOT a KEEP claim)

1. A 300 bps cash credit turns a failing book into a 4b pass on every leg: WF-B MA-DG g=1.00, B136 weekly, CAGR 11.35% / Sharpe 1.186 / MaxDD −16.57%, OOS 11.50% / 1.221 / −16.57% (SPY 15.23% / 0.889 / −33.72%, floor 10.66%, cap −20.23%).
2. The same book fails 4b at 150 bps and has an EMPTY band at 0 bps, so the pass is bought by the credit, not by the book.
3. 4a is False at every rate (MaxDD −16.57% vs RULES v2's −12.16%), so this could only ever be a 4b promotion.
4. The credit is counterfactual where it matters: a flat 300 bps is applied to 2009–2016, when realised T-bill yields were 0–30 bps, and that window sets both the CAGR floor test and the IS band.
5. Across all 612 books per rate, 4b passes go 50 → 69 → 96 and 4a passes 34 → 124 → 142 (baseline credited at the same rate) — the verdict is a function of an undeclared dial.
6. `engine.metrics` scores Sharpe at `rf=0`, so a cash-heavy book is paid a free Sharpe: on excess legs at the same rate for book and benchmark, the ladder's slope is invariant in c (36/36 cells inside 0.0100).
7. BLOCKING TEST before any promotion: a realised short-rate series (3m T-bill or fed funds) replacing the flat rate, then re-run this exact script with c\_t in place of c. The sandbox has no network and `data/` carries no rate file — local/Actions work.
8. SECOND TEST: re-score the survivor on excess Sharpe at the realised rate for both the book and SPY; a pass that survives (5), (7) and (8) is a candidate, nothing before that is.
9. Adopting this without (7) would be adopting idea 642's open question ("is a FLAT cash rate the wrong instrument entirely") as an assumption.
10. No RULES wording is proposed. `RULES.md`, `PROTOCOL.md`, `scan.py`, `bot.py`, `baseline.py` untouched; the Sunday review is asked only for the reporting line in the result file (declare the cash rate beside every 4a/4b verdict on a cash-holding book).
