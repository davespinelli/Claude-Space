# Idea 572 — does mrho's GAP SHRINKAGE survive a WIDER overlap?

**cloud lane, 2026-09-11.** Script `2026-09-11_does-mrho-s-GAP-SHRINKAGE-survive-a-WIDER-overlap_cloud.py`, console `…console.txt`, artefacts `.grid.csv` (9,936) `.rungs.csv` (138) `.origin.csv` (30) `.overlap.csv` (12) `.feas.csv` (162) `.walkforward.csv` (12) `.keeppaths.csv` (9,936) `.chars.csv` (828). 519 s, deterministic, no network.

## ANSWER — NO. H_ARTEFACT CONFIRMED, and the artefact is the LEVEL SET, not k

Idea 569's **+0.0801 (0.41× idea 568's 0.1961)** is a **rung-selection artefact**. The 3-rung overlap a k=36 draw allows omits exactly the high-mrho rungs where the B−S gap is large (+0.2417 at L=0.2100, +0.2118 at L=0.2509). Add those rungs back and **the gap is 0.1017–0.1092 (0.52–0.56×), and it sits 1.14–1.41× ABOVE its own seed floor at every k and every level set** — never inside it. **mrho is not the carrier** by idea 569's own test.

**KILL of the absorption reading. KILL for capital.** No RULES change, no book promoted, no KEEP claimed, no memo, no PROTOCOL edit; RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py untouched.

## GATES — four, pre-registered, printed before any new number was read. ALL PASS

| gate | result | bar |
|---|---|---|
| G0 draw determinism at every K | **0 of 828** differ on rebuild | 0 |
| G1 `fast_backtest` vs `engine.backtest` | **1.388e-17** | 1e-9 |
| G2 idea 569's committed `.rungs.csv` mrho, all **13 rows × 5 cols**, rebuilt from prices | **9.714e-17** | 1e-9 |
| G3 idea 569's committed `.origin.csv` mrho, all **3 rows × 8 cols**; mean gap here **+0.0801** vs committed **+0.0801** | **2.220e-16** | 1e-9 |
| G4 idea 569's committed k=36 mrho reach bands, BONLY [0.1251, 0.3367] / SONLY [0.0787, 0.2735] | **2.410e-05** | 1e-4 |

## H_WIDER — PASS. The premise is right: a smaller draw reaches further

| char | K | BONLY reach | SONLY reach | feasible Q9 B/S | overlap Q5 | overlap Q9 |
|---|---|---|---|---|---|---|
| mrho | 20 | [0.0827, 0.3622] | [0.0665, 0.2825] | 9/9, 9/9 | **5** | **9** |
| mrho | 28 | [0.1075, 0.3480] | [0.0729, 0.2775] | 9/9, 8/9 | **4** | **8** |
| mrho | 36 | [0.1251, 0.3367] | [0.0787, 0.2735] | 8/9, 8/9 | **3** *(569's cell)* | 7 |

## THE ANSWER — the gap is FLAT in k and rises with the level set

All 6 tuned points × 2 characteristics (every one committed in `.overlap.csv`):

| char | K | levelset | overlap | mean gap | **\|gap\|** | sd_pair | **\|gap\|/floor** | \|resid\| | \|gap\|/568 | within floor |
|---|---|---|---|---|---|---|---|---|---|---|
| mrho | 20 | Q5 | 5 | +0.0361 | 0.1074 | 0.0837 | 1.28 | 0.0990 | 0.55 | 2/5 |
| mrho | 20 | Q9 | 9 | +0.0621 | **0.1017** | 0.0891 | **1.14** | 0.0990 | 0.52 | 4/9 |
| mrho | 28 | Q5 | 4 | +0.0136 | 0.0904 | 0.0782 | 1.16 | 0.1054 | 0.46 | 2/4 |
| mrho | 28 | Q9 | 8 | +0.0566 | 0.1092 | 0.0804 | 1.36 | 0.1022 | 0.56 | 4/8 |
| mrho | 36 | Q5 | 3 | **+0.0801** | **0.0801** | 0.0661 | 1.21 | 0.0971 | **0.41** | 2/3 |
| mrho | 36 | Q9 | 7 | +0.0932 | 0.1080 | 0.0767 | 1.41 | 0.0998 | 0.55 | 4/7 |

**The decisive comparison is the last two rows.** Holding k at 36 — idea 569's own draw size — and only widening the level set from Q5 to Q9 moves |gap| from **0.0801 to 0.1080** and the ratio from **0.41× to 0.55×** of idea 568. Shrinking k, which the queue proposed as the fix, moves almost nothing: at Q9 the gap reads **0.1017 / 0.1092 / 0.1080** at k = 20 / 28 / 36. So the queue's diagnosis ("short overlap") is **confirmed**, but its proposed instrument is not the one that matters: the truth was already recoverable at k=36 by using all nine rungs. k buys rungs; it does not move the gap.

- **H_SHRINK FAIL** — 0.1017 at K=20/Q9 is above the 0.0981 carrier bar (idea 569's own 0.5 × 0.1961).
- **H_FLOOR PASS**, and it cuts against absorption: |gap|/floor is **1.14–1.41 at every mrho cell**, i.e. the gap never falls inside the seed noise floor. Idea 569's 2-of-3 "within floor" becomes **4 of 9** once the omitted rungs are restored, and the 5 that fail are the 5 highest-mrho rungs.
- **H_MATCH FAIL** — mean |achieved_B − achieved_S| is **0.0990 at K=20 vs 0.0971 at K=36**: shrinking k does *not* fix the match. At every k and every rung BONLY lands 0.09–0.13 of mrho **above** SONLY, because B136 simply has no low-mrho names for the kernel to find. **mrho was never matched, at any k** — so "matched-level absorption" was not a licensed reading of this ladder in the first place.

**CONTROL (cvol, idea 568/569's reference).** |gap| 0.1131–0.1438 on Q9, |gap|/floor **1.76–2.00**, within floor **0 of 6**, |resid| 0.1187–0.1233. mrho's gap *is* genuinely smaller than cvol's in floor units (1.14–1.41 vs 1.76–2.11) — so mrho absorbs **part** of the origin effect — but partial absorption above the floor is not the collapse idea 569's number implied.

## RULE 8

**WF-A — the gap recomputed separately on IS and OOS (OOS read once).**

| char | K | overlap | gap FULL | gap IS | gap OOS | IS/568 | OOS/568 | shrink IS | shrink OOS |
|---|---|---|---|---|---|---|---|---|---|
| mrho | 20 | 9 | +0.0621 | +0.1442 | +0.0222 | 0.74 | 0.66 | **False** | **False** |
| mrho | 28 | 8 | +0.0566 | +0.1156 | +0.0275 | 0.65 | 0.80 | **False** | **False** |
| mrho | 36 | 7 | +0.0932 | +0.1283 | +0.0778 | 0.72 | 0.66 | **False** | **False** |

The shrinkage verdict fails in **both** windows at every k — it is not an in-sample-only result that OOS rescues, and not an OOS-only one either.

**WF-B — the absorption claim as a trading instruction, OOS read ONCE.** Among the overlapping rungs only, (flavour, level, seed, gross, cadence) chosen by IS Sharpe alone. Comparands OOS: **RULES v2 on U56 9.53% / 1.2851 / −12.05%; SPY 15.45% / 0.8820 / −33.72%.**

| char | K | held | IS Sharpe | OOS CAGR | OOS Sharpe | OOS MaxDD | >v2 | >SPY | hh BONLY | hh SONLY |
|---|---|---|---|---|---|---|---|---|---|---|
| mrho | 20 | BONLY L0.195 s1 g1.00 M | 1.4128 | 22.03% | 1.1534 | −26.07% | False | True | **1.0378** | **0.3299** |
| mrho | 28 | BONLY L0.148 s0 g1.00 M | 1.4260 | 21.96% | **1.3146** | −25.94% | **True** | True | **1.1174** | **0.4035** |
| mrho | 36 | BONLY L0.195 s1 g1.00 M | 1.3882 | 21.95% | 1.1801 | −28.49% | False | True | **1.1428** | **0.3548** |
| cvol | 20/28/36 | BONLY L0.378 s2 g1.00 M | 1.19–1.40 | 15.78–17.15% | 0.91–0.97 | −29.4 to −30.8% | False | True | 0.95–0.97 | 0.32–0.34 |

**beat RULES v2 on OOS Sharpe 1/6; beat SPY on OOS Sharpe 6/6.** The head-to-head is the finding: at matched mrho the **BONLY arm out-Sharpes the SONLY arm out of sample by ~0.70–0.78 (1.04–1.14 vs 0.33–0.40) at every k**. The IS selector picks a BONLY book in all six cells without being told to. Whatever mrho matching does to the *premium* gap, it leaves the origin effect fully intact in OOS Sharpe — the strongest single reason to call this a KILL rather than a PARK.

## KEEP PATHS — all 9,936 books

4a **81**, 4b **391**, BOTH **4**. By K: 4a 50 / 20 / 11 and 4b 147 / 131 / 113 at K = 20 / 28 / 36 — both monotone **decreasing** in draw size, i.e. the bars are easier to clear on narrower books, a resolution effect and not an edge. By flavour: **4b BONLY 386, SONLY 1, POOL 4** — 98.7% of all 4b passes are B-sourced, which reproduces idea 573's origin-in-the-KEEP-counts finding on a completely different ladder. Binding 4b legs: DD 8,692, H2 7,300, OOS 7,286, H1 6,343, CAGR 5,762. **Every panel here is a kernel-weighted seeded draw, not a tradable rule: no 4b pass on this ladder is a capital candidate and none is claimed.**

## SURVIVORSHIP

The pool is B136 (current constituents of `universe_broad.json`, 134 names on the common index) plus the sub-$2B panel (current constituents, all 44 tickers with `max_1d_move ≥ 1.0` dropped first) — 573 names on 2010-01-04..2026-09-04. Dead SMALL names are absent, so the S-sourced premium is biased **upward**, which **shrinks** the B−S gap measured here. The bias therefore works **in favour of** H_SHRINK and **against** the artefact verdict this run reaches — the gap is larger than 0.10 in truth, not smaller.

## HYPOTHESES

H_REPRO **PASS** · H_WIDER **PASS** · H_MATCH **FAIL** · H_SHRINK **FAIL** · H_FLOOR **PASS** · **H_ARTEFACT CONFIRMED**.
