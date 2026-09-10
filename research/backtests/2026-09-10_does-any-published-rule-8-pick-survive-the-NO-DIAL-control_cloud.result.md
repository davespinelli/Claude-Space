# Idea 621 — does ANY published rule-8 pick survive the NO-DIAL control?  (cloud, 2026-09-10)

**Verdict: SPLIT — the census says the column is missing (2.3 % of the record's rule-8 files
carry it); the back-fill says the missing column would have KILLED four of the record's six dial
families and spared two.**  No KEEP.  Script:
`2026-09-10_does-any-published-rule-8-pick-survive-the-NO-DIAL-control_cloud.py`.

Params (PROTOCOL 4, the two the queue names): **P1 claim set** (six dial families), **P2 control
form** (DEFAULT / MEDIAN-rung).  Everything else — panel, book, cadence, cost rung — is a
reported axis; all 288 grid points are in `.grid.csv`, all 192 rule-8 cells in `.cells.csv`.

## GATES — all pass
| gate | result |
|---|---|
| G1 segment runner vs `engine.backtest`, D and W, 3 panels | max\|dr\| **7.8e-16**, max\|dto\| **4.4e-16** |
| G2 cost-rung identity vs live `engine.backtest(25)` | max\|dr\| **7.8e-16** |
| G3 the DEFAULT control is inside its own ladder, 6/6 dials | True |
| G4 IS ≤ 2016-12-31, OOS ≥ 2017-01-01, disjoint and exhaustive | True |
| **G5 REPRODUCTION** of idea 412's headline from its own `.walkforward.csv` | **LAMONLY beats NONE 15/36, median −0.0001**; CADONLY **19/36, +0.0062** — both exact against 412's prose |

## PART A — the census (624 artefact stems in `research/backtests/`)

| population | n | NO-DIAL, STRICT (machine-readable arm) | prose only | either | a control of ANY kind |
|---|---|---|---|---|---|
| text states a rule-8 chooser | 576 | **13 (2.3 %)** | 20 | 33 (5.7 %) | 487 (84.5 %) |
| carries a committed WF/chooser CSV | 478 | **11 (2.3 %)** | 17 | 28 (5.9 %) | 419 (87.7 %) |

STRICT = a committed CSV exposes the no-dial arm as a whole-token column name or arm value, i.e.
a later run can re-read the number without re-running the file — which is exactly what "back-fill
it where absent" requires.  The **84.5 % / 2.3 % gap is the finding**: the record is saturated
with *controls* (placebo, matched-gross, depth-matched) and almost empty of the *cheapest* one,
the arm where the dial is simply left at its default.  Per ideas 534/612 the LOOSE column is an
upper bound on files, not on claims; only STRICT is quoted as the headline.

## PART B — the back-fill (rule 8, 6 dials × 3 panels × 2 books × 2 cadences × 4 rungs)

Dial chosen on 2009–2016 IS Sharpe alone; 2017–2026 read once.  DEFAULT control spends **no**
parameter (n = 20, λ = 1.00, cadence W, gross 0.75, band 0.03, volcap 0.60).

### At PROTOCOL's 10 bps rung — chooser OOS Sharpe minus NO-DIAL OOS Sharpe

| dial | cells | chooser beats DEFAULT | median Δ | beats MEDIAN-rung | median Δ | median regret vs oracle |
|---|---|---|---|---|---|---|
| **n** (selection) | 6 | **5/6** | **+0.0980** | 5/6 | +0.0980 | +0.0065 |
| **volcap** (selection) | 6 | **6/6** | **+0.0763** | 4/6 | +0.0411 | +0.0084 |
| lambda (trading) | 12 | 7/12 | +0.0256 | 8/12 | +0.0052 | +0.0054 |
| cadence (trading) | 6 | 3/6 | +0.0166 | 0/6 | 0.0000 | +0.0238 |
| gross (exposure) | 12 | 8/12 | **+0.0002** | 8/12 | +0.0002 | 0.0000 |
| band (gate width) | 6 | **2/6** | **−0.0214** | 2/6 | −0.0214 | +0.0361 |
| **pooled** | **48** | **31/48** (p = 0.030 one-sided) | **+0.0014** | 27/48 | +0.0002 | 0.0000 |

* **The pooled win is real and worthless.** 31/48 clears a coin flip at p = 0.030, but the median
  gain is **+0.0014 of Sharpe** and **19 of 48 cells sit inside idea 412's own phase-noise SD of
  0.0150** — i.e. for 40 % of the record's dials, whether the chooser "beat" no-dial is decided by
  which weekday the book rebalances on.  Mean +0.0515, sd 0.1090: the average is two cells
  (volcap on small439 +0.3695, n on broad136 +0.2611), not a tendency.
* **The split is SELECTION vs everything else.** The two dials that change *which names are
  held* win **11 of 12** cells at a median +0.08.  The four that change *trading, exposure or
  gate width* win **20 of 36** — a coin flip — and the band dial is a **net loss** (2/6, median
  −0.0214, worst −0.0980).  Idea 412's LAMONLY result generalises to λ, gross, cadence and band;
  it does **not** generalise to n or the vol cap.
* **Most of what remains is cost avoidance, not signal.** Pooled win rate rises monotonically
  with the rung — **27/48 at 0 bps → 31/48 at 10 → 34/48 at 25 → 38/48 at 50**, median Δ
  0.0000 → +0.0014 → +0.0383 → +0.0757.  At zero cost the chooser is exactly a coin flip.
* **The chooser picks the default in only 3 of 48 cells** yet its median regret against the OOS
  oracle is 0.0000 (pick = oracle in 25/48): the ladders are flat enough that the pick barely
  matters either way.

### Levels, 10 bps, OOS 2017–2026 (medians over each panel's cells)

| panel | chooser | NO-DIAL | RULES v2 (live) | SPY |
|---|---|---|---|---|
| u56 | 1.1968 / 12.88 % / −16.34 % | 1.1599 / 13.43 % / −18.42 % | **1.2788** / 9.48 % / −12.05 % | 0.8758 / 15.32 % / −33.72 % |
| broad136 | 1.0465 / 11.24 % / −18.20 % | 0.8779 / 8.93 % / −20.70 % | **1.1185** / 7.98 % / −12.24 % | 0.8820 / 15.45 % / −33.72 % |
| small439 | 0.5483 / 5.01 % / −31.93 % | 0.4573 / 3.90 % / −31.04 % | **0.5680** / 3.85 % / −14.68 % | 0.8820 / 15.45 % / −33.72 % |

**The chooser loses to RULES v2 on all three panels** and beats SPY's Sharpe on two.  Full sample
(10 bps, grid medians): u56 BAND 8.55 %/1.199/−11.90 % (H 1.214/1.190), u56 TOP20
13.80 %/1.113/−18.42 % (H 1.151/1.089); broad136 BAND 8.01 %/1.108/−12.28 %, TOP20
12.52 %/0.928/−21.75 %; small439 BAND 3.91 %/0.564/−15.51 %, TOP20 6.04 %/0.448/−32.72 %.
Comparands, same window: SPY 15.15 %/0.886/−33.72 % (H 0.959/0.826), RULES v2 u56
8.63 %/1.202/−12.05 % (H 1.231/1.180), broad136 8.03 %/1.106/−12.24 %, small439
3.81 %/0.572/−14.68 %.

## KEEP paths (PROTOCOL 4, both priced on every arm, 10 bps)

| | 4a | 4b |
|---|---|---|
| all 288 grid points, full sample | 10/288 | 38/288 |
| all 288 grid points, OOS window | 19/288 | 41/288 |
| **the 48 CHOOSER arms** | **1/48** | **8/48** |
| **the 48 NO-DIAL arms** | **4/48** | **9/48** |

Passing 4b on the full sample **and** on the OOS window read separately: **chooser 7, no-dial 9.**
Spending the parameter does not buy KEEPs — it loses them.  And the nine no-dial passers are not
nine books: **five** are the *same* u56 TOP20 default weekly book (n = 20, gross 0.75,
volcap 0.60, λ = 1 — OOS 14.86 % / 1.160 / −18.45 %) counted once per dial family, and the other
**four** are its daily twin (13.43 % / 1.074 / −18.42 %).  Two books, both of them the book you
get by turning no dial at all.

## The answer to the queue's question

**Almost none of the record publishes the column (2.3 %), and where this run supplies it the
answer depends entirely on what the dial does.**  A rule-8 pick survives the NO-DIAL control when
the dial *selects the holdings* (n, vol cap: 11/12, +0.08) and does not survive it when the dial
only changes *trading, exposure or gate width* (λ, cadence, gross, band: 20/36, and band is
negative).  Idea 412's LAMONLY finding was not a fact about λ; it was a fact about the class λ
belongs to.  The narrow PROTOCOL amendment this supports is: **a file that reports a rule-8 pick
must report the same book with the dial at its default**, because it costs one extra arm and, on
this evidence, it reverses the reading of four dial families out of six.

## Caveats carried
* SURVIVORSHIP (idea 54) on all three panels; SMALL439 drops 44 tickers with
  `max_1d_move >= 1.0` from `data/small_meta.csv` and is a since-2010 panel of names that exist
  **today** under $2B — only its within-panel arm-minus-arm contrasts are read here.
* Cadence rungs are phase-0 calendar D/W/M/Q; idea 412 measured phase SD 0.0461 at Q, so the
  cadence family's six cells carry a nuisance of the size of its own effect.
* Six cells per single-book dial is a small denominator: n's 5/6 and volcap's 6/6 are p = 0.109
  and p = 0.016 against a coin, and the pooled 31/48 is the only number here with a p under 0.05.
* Idea 321 (MaxDD is one path), idea 126 (t+1), ideas 527/531 (4b is in practice a DD-cap test).
* The census classifies FILES, not CLAIMS (idea 534); LOOSE is an upper bound by construction.
