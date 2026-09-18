# Idea 1279 (lane C, 2026-09-18) — does the GROSS LADDER belong in the record's COMPARISON SET AT ALL?

**ANSWER: NO. IT IS A RULER WITH NO MARKS ON IT, AND SEVEN TENTHS OF THE RECORD'S DECISIVE
LADDER CALLS ARE MEASUREMENTS OF THAT FACT. VERDICT: KILL (capital), NO NEW BOOK, SCHEMA
OFFERED.**

Script `2026-09-18_does-the-GROSS-LADDER-belong-in-the-record-s-COMPARISON-SET-AT-ALL_C.py`,
19/19 gates PASS (G1 vintage-pinned anchor replay residual 5.965e-05; G2 determinism; G3 folds
partition; G4 IS/OOS disjoint; G5 the IS argmax reads no OOS row, 20/20 cells; G6 NO_GROSS's
cells a strict subset of ALL4's; G7/G7b SEs and shares in range; G8 D_TIGHT ⊂ D_LOOSE; G9
denominator stamped at tree `eac846f`; G10 MAXVOL monotone; G11 1101 replayed exactly — U56
GROSS IS-Sharpe argmax at the TOP rung 0.75, IS-DD argmax at the BOTTOM rung 0.30).

## The two dials, every cell published
`LADDER_SET {ALL4, NO_GROSS}` × `DECISIVE_BAR {D_TIGHT 2.160, D_LOOSE 1.771}`. Controls at every
value: PANEL {U56, B135, SMALL663}, LADDER {GROSS, N, H, MAXVOL} at the record's committed BASE
rungs, IS_STAT {IS_SHARPE, IS_CAGR, IS_DD}, N_FOLDS = 14 (idea 1276's count, copied not chosen).

## ARM A — the ladder widths, and what the four-ladder set was buying
Fold-mean width (max − min of the ladder's rungs' fold Sharpe, 14 folds, ± SE):

| panel | GROSS | MAXVOL | N | H |
|---|---|---|---|---|
| U56 | **0.0032** ± 0.0008 | 0.2376 ± 0.0277 | 0.3808 ± 0.0801 | 0.4921 ± 0.0557 |
| B135 | **0.0055** ± 0.0016 | 0.3084 ± 0.0305 | 0.3753 ± 0.0782 | 0.5236 ± 0.0556 |
| SMALL663 | **0.0080** ± 0.0021 | 0.4763 ± 0.0528 | 0.4721 ± 0.0463 | 0.9500 ± 0.0958 |

**H_DEGENERATE HELD** — GROSS is the narrowest ladder on 3 of 3 panels, by 59x to 74x against
the next-narrowest. Whole-span widths 0.0017 / 0.0040 / 0.0021 against 0.0247–0.2772.

**H_MANUFACTURED HELD** — 9 of 13 ALL4 decisive pair calls (69.2%) involve GROSS, at BOTH bars.
Every GROSS pair is decisive on every panel (|t| 4.72–9.96, 9 of 9); of the 9 non-GROSS pairs
only 4 are (|t| 3.68–5.61), and the other 5 sit at |t| 0.06–1.56.

**H_SURVIVE HELD** — headline counts across both bars: ALL4 publishes **34**, NO_GROSS **10**
(29.4%). By form: H_ANY 13/18 (72.2%) → 4/9 (44.4%); **H_NARROWEST 3/3 → 0/3** — all three
"narrowest dial" headlines were the statement that GROSS is flat; H_WIDEST 1/3 → 1/3, the only
form GROSS never touched.

**The decisiveness bar is not load-bearing.** D_TIGHT and D_LOOSE give IDENTICAL counts in all
four cells, because no pair's |t| falls in the 1.56–3.68 gap. The comparison SET is the whole
dial; the significance threshold the record argues about is inert here.

## ARM B — capital (rule 8, 2017-2026 read ONCE)
- Every grid point on both KEEP paths: **4a 0 of 60**. **4b 13 of 60 rows = 10 distinct books**
  (U56 6, B135 4, SMALL663 0) under 1194's gross-free key — all prior art, no new book.
  Binding 4b leg: DD 42, CAGR 22, H2 20, OOS 20, H1 18.
- **CROSS-LADDER chooser (the object the queue asks to price):** dropping GROSS moves the pick
  in **3 of 9** (panel, IS_STAT) cells and costs **−0.0115 of OOS Sharpe (SE 0.0133, t −0.86,
  n = 9)** — indistinguishable from zero. **H_CAPITAL HELD.**
- And the four-ladder set was buying nothing on the other side either: ALL4's chooser lands
  **+0.0001** of OOS Sharpe against the anchor, NO_GROSS **−0.0113**; NEITHER reaches the anchor
  in any of 9 cells. The gross rungs' entire capital contribution is to hand the IS_DD chooser a
  low-gross cell — GROSS = 0.30 wins IS_DD on 3 of 3 panels — which is the anchor with a cash
  sleeve, not a different book (d OOS Sharpe −0.0021 / −0.0045 / −0.0020).
- WITHIN-LADDER chooser, 36 decisions, continuity with 1152 ARM C: mean d(OOS Sharpe) pick minus
  anchor **−0.0280** (SE 0.0126, positive 4/36), reach 9/36 — **6 of those 9 reaches are the
  GROSS ladder**, where "reached" means only that the chooser could not leave a flat rung.

## ARM C — what the record committed (tree `eac846f`)
1501 of 6813 committed csv/csv.gz artefacts carry a ladder/axis/pair column: 28,027 of 373,817
rows (7.5%) name GROSS and **467 of 1501 artefacts (31.1%)** carry at least one GROSS row.
876 committed decisive / widest-dial prose sentences, 38 (4.3%) name GROSS.

## Recommendation (Sunday review; PROTOCOL.md NOT edited here)
Drop GROSS from the committed four-ladder comparison set and re-key the affected artefacts.
Exact wording offered: *"A ladder whose fold-mean width is below one tenth of the narrowest
other ladder in the same comparison set is DEGENERATE and must not be scored as a comparand; it
may be published as an ATTRIBUTE of the cells it spans, never as a dial."* On this tape that
clause fires on GROSS and on nothing else.

## Survivorship (PROTOCOL rule 9)
U56 and B135 are CURRENT-constituent lists; SMALL663 is a current sub-$2B screen. Every absolute
level is optimistic and every 4b pass is an UPPER bound. ARM A's headline is a DIFFERENCE
between ladders measured on the SAME names in the SAME folds, so it is first-order immune.
