# Idea 133 — is-the-defensive-class-one-book-in-disguise (lane B, 2026-09-05)

**ANSWERED. KILL of the premise.** The `4b-defensive` class is **not one book in disguise**, and
the construction idea 129 named is not even its best member — it is a mediocre one. PROTOCOL
should keep the class, not name a book. Rules unchanged; no new KEEP candidate.

Script `2026-09-05_defensive-class-census_B.py`; grid `.grid.csv` (2244 rows, every one reported);
walk-forward `.walkforward.csv` (72 rows); console `.console.txt`.

## What was asked

Idea 129 proposed a `4b-defensive` reporting class — an arm clearing 4b's two halves-Sharpe bars,
its OOS-Sharpe bar and its MaxDD cap, failing **only** the CAGR floor — and filed its own caveat:
its 11 Pareto-best members were all `EWall + a slow trend gate, de-grossed` at ~53% gross, so "the
class may be one construction in disguise". Idea 133 asks whether the class has any member that is
not that construction, over the leaderboard's **ranked** and **sleeve** books, **at matched gross**.

Two hypotheses were written down before any number was read, with opposite predictions on the same
table: **H_one** — the class is one construction, so ranked and sleeve books stay out at every
gross level; **H_gross** — the class is a gross level, so at matched gross everything joins.

## Harness and reproduction (four checks before anything new was read, plus a fifth after)

Idea 94's simulator (`H.run`, 17 arms, 5 gates, both conventions) and idea 102's sleeve
(`sleeve_weights`, idea 18 variant B: trend-vote × risk-parity over TLT/GLD/DBC/UUP) are
**imported, not re-implemented**. `book_targets()` generalises `H.targets` to n-ranked and sleeve
books and is asserted identical to it on the three books that function already knows.

| check | result |
|---|---|
| (a) `book_targets` vs `H.targets`, 3 books × 6 gates × 2 conventions | max\|diff\| **0.000e+00** |
| (b) `H.run` (all instruments off) vs `engine.backtest` | max\|diff\| **0.000e+00** |
| (c) idea 94's published `EWall+vol60-dg` u56@10bps | **11.587% / 1.133 / −16.884%** vs 11.6/1.133/−16.9 |
| (d) idea 102 sleeve imported | DBC/GLD/TLT/UUP non-zero, mean gross 0.580 |
| (e) **idea 129's entire 306-row grid re-run** | 306/306 matched; max\|d CAGR\| 9.7e-17, \|d Sharpe\| 2.2e-16, \|d MaxDD\| 9.7e-17, \|d OOS Sharpe\| 2.2e-16, \|d gross\| 5.6e-17; **0/306 `floor_only` mismatches, 0/306 `pass4b` mismatches** |

Corpus: 3 panels (u56 56, broad 136, small 439) × 8 books (V1u, TOP5/10/20/40, EWall, SLV25, SLV50;
sleeve books need TLT/GLD/DBC/UUP and are **not run on the small panel**) × 17 arms × 2 cost rungs ×
3 gross modes = **2244 rows, all reported**. Tuned parameters: exactly two — `n ∈ {5,10,20,40}`
(ranked size) and `f ∈ {0.25,0.50}` (sleeve fraction). Gross mode is a reported convention axis
fixed in advance, not a search: `native` (m=1, idea 129's reading), `m53` (mean gross forced to
0.53, the queue's number for the class), `m75` (forced to 0.75, the nominal). Achieved mean gross is
reported on every row (m53 → 0.529/0.530, m75 → 0.742/0.751).

## (1) The census — H_one is refuted, decisively

**531 of 2244 rows are in the class. 37 are `EWall + slow trend gate + de-gross`. 494 (93.0%) are
not.** The class spans **six of the eight books**; 431 of its 531 members also pass 4a.

Membership by book (rate, count out of 102 rows per book per gross mode):

| book | native | m53 | m75 |
|---|---|---|---|
| V1u | **0.0% (0)** | **0.0% (0)** | **0.0% (0)** |
| TOP5 | **0.0% (0)** | **0.0% (0)** | **0.0% (0)** |
| TOP10 | 0.0% (0) | 10.8% (11) | 0.0% (0) |
| TOP20 | 1.0% (1) | 33.3% (34) | 0.0% (0) |
| TOP40 | 9.8% (10) | 51.0% (52) | 2.0% (2) |
| EWall | 25.5% (26) | 61.8% (63) | 6.9% (7) |
| SLV25 | **73.5% (50)** | **97.1% (66)** | **76.5% (52)** |
| SLV50 | **76.5% (52)** | **76.5% (52)** | **77.9% (53)** |

The two macro-sleeve books are members at *every* gross level, including the one where EWall almost
vanishes (m75: EWall 6.9%, SLV50 77.9%). Membership is therefore a construction property for them,
not a gross artefact.

## (2) The Pareto-best subset — idea 129's actual claim, and it inverts

Idea 129's claim is about the (Sharpe, MaxDD) Pareto front, so the front was taken twice. Within
`(panel, book, cost)`, idea 129's own convention: 138 floor-only Pareto rows, **118 (85.5%) not
EWall+slow-gate**. Across **all books** within `(panel, cost, gross)` — the frontier this question
actually needs, because "is the class one book" is a cross-book question — the front is **47 rows,
of which 2 are `EWall+slow-gate-dg`** and they rank **27th and 28th of 47 by Sharpe**.

The top of that front, all sleeve books, native gross, 10 bps:

| panel | book | arm | gross | CAGR | Sharpe | MaxDD | H1 / H2 | OOS Sharpe | OOS MaxDD | CAGR margin | turnover |
|---|---|---|---|---|---|---|---|---|---|---|---|
| broad | SLV50 | ebud-0.10 | 0.743 | 8.7% | **1.292** | −13.6% | 1.318 / 1.273 | **1.311** | −13.6% | −2.0 pp | 4.2× |
| broad | SLV50 | vol60-dg | 0.735 | 7.6% | 1.277 | −10.6% | 1.262 / 1.293 | **1.338** | −10.6% | −3.0 pp | 4.8× |
| u56 | SLV50 | ebud-0.10 | 0.743 | 8.2% | 1.263 | −12.9% | — | 1.316 | −12.9% | −2.5 pp | 4.2× |
| u56 | SLV25 | band3-dg | 0.586 | 7.2% | 1.253 | −9.6% | — | **1.369** | −9.6% | −3.5 pp | 3.3× |
| u56 | EWall | band3-dg | 0.533 | 8.7% | 1.206 | −12.1% | — | 1.285 | −12.1% | −2.0 pp | 1.8× |

Class means by book at native gross: SLV50 Sharpe 1.171 / OOS 1.255 / OOS MaxDD −11.6%; SLV25
1.118 / 1.164 / −14.0%; EWall 1.054 / 1.112 / −14.4%; TOP40 1.063 / 1.154 / −15.5%; TOP20 0.997 /
1.034 / −16.6%. Corpus-wide, sleeve class members average **OOS Sharpe 1.208 (n=325)** against
EWall's **1.102 (n=96)** and the ranked books' **1.066 (n=110)**. The construction idea 129 named
sits in the **middle** of its own class, not at its top.

## (3) Why the other books are out — and the gross channel, measured

The binding bar is legible book by book. `V1u` is out of the class in **all 276 of its rows**
because it fails the halves and OOS bars as well (its closest arm anywhere misses H1 by 0.206–0.568),
i.e. it is a bad book, not a defensive one; `TOP5` likewise (its closest rows fail the DD cap in 92
of 276). At the other end `SLV50` fails **only** the CAGR floor in 157 rows and floor+H1 in 47,
never the DD cap: it is a defensive book that the floor is the only thing standing between and 4b.

Gross does real work, but only on the ranked books: forcing every arm to 0.53 mean gross moves
TOP20 from 1 member to 34 and TOP40 from 10 to 52, and raises class size 139 → 278 overall. So
**H_gross is partly right** — de-grossing manufactures class membership for ranked books, which is
exactly idea 129's own warning that the floor "cannot distinguish a de-grossed lever from a
better-shaped defensive book". But it cannot be the whole story: V1u and TOP5 join at **no** gross
level (0 of 276 each), and the sleeve books are members at **every** level. Class members average
MaxDD −13.2/−13.7/−13.3% (m53/m75/native) against non-members' −21.3/−27.0/−25.2%, at Sharpe
1.096/1.137/1.121 vs 0.668/0.774/0.760 — the shape difference is not a gross difference.

## (4) Rule 8 walk-forward (parameters on 2009–2016, 2017–2026 read once)

Four selectors were fixed in writing before any OOS number was read; 18 cells pool **all books**
within a (panel, cost, gross) triple, because "which construction gets picked" is the question.
S0 = argmax IS Sharpe, no screen. S1 = idea 129's IS 4b screen with the floor. S2 = the same with
the floor deleted. S3 = **NEW** — argmax IS Sharpe among arms that are IS-window `4b-defensive`
(halves and DD met, floor failed), i.e. select the class deliberately.

| selector | picks | OOS CAGR | OOS Sharpe | OOS MaxDD | beats SPY | beats v1 | beats own control | mean OOS rank (of 136) |
|---|---|---|---|---|---|---|---|---|
| S0 no screen | 18/18 | **12.5%** | 0.958 | −23.7% | 12 | 18 | 9 | 41.6 |
| S1 floor kept | 11/18 | 13.0% | 1.069 | −20.9% | 9 | 11 | 6 | 52.9 |
| S2 floor deleted | 12/18 | 10.3% | 1.192 | −16.6% | 12 | 12 | 8 | 26.0 |
| **S3 select the class** | 12/18 | 9.1% | **1.233** | **−14.3%** | **12** | **12** | **11** | **15.9** |

Reference: SPY OOS 15.45% / 0.882 / −33.72%; RULES v1 OOS 4.86% / 0.451 / −25.30%; ungated EWall
control OOS Sharpe 0.952.

Two things follow. First, the class is **prospectively selectable**: screening for it on the IS
window alone produces the best OOS Sharpe, the shallowest OOS drawdown and the best mean OOS rank
of the four selectors, and beats SPY, RULES v1 and its own control in 12/12/11 of the 12 cells where
it picks — at 9.1% OOS CAGR against SPY's 15.45%, which is precisely the trade the CAGR floor
refuses. Second, and directly on this idea's question, **S3's 12 picks are not one construction**:
SLV50 ×7, SLV25 ×3, TOP20 ×1, TOP40 ×1, and zero EWall. All six small-panel cells are empty for
S1/S2/S3 (the small panel contributes **0 of 531** class members at any gross level).

## (5) Both KEEP paths

4a passes **1053 of 2244**; 4b passes **144 of 2244**. Arms passing 4b in all four (u56/broad ×
10/25 bps) cells at native gross: **`EWall/band3-rw` and `EWall/vol60-dg`** — both already present
in idea 129's grid, so this run **confirms** them and discovers nothing new. The standing candidate
`EWall + vol60-dg` is untouched and reproduces exactly: u56 11.6%/1.133/−16.9% (halves 1.156/1.113,
OOS 1.186, 1.39× turnover), broad 12.4%/1.138/−18.7% (halves 1.255/1.027, OOS 1.122). **No new KEEP
candidate.** The best sleeve arms are *not* candidates: they fail the CAGR floor by 2.0–5.5 pp/yr,
which is what puts them in the class in the first place.

## Verdict

**KILL of the "one construction" premise.** The class has 531 members across six books; 93% are not
`EWall + slow gate + de-gross`; on the cross-book Pareto front that construction holds 2 of 47 seats
and ranks 27th; and a selector aimed at the class picks four different books and no EWall. Idea
129's caveat was an artefact of the three-book corpus it ran on. **PROTOCOL should keep the class
name, and idea 129's memo should drop its "may be one construction" caveat and gain two others:
that class membership is partly manufacturable by de-grossing a ranked book (so the class must
report mean gross, which idea 129 already requires), and that the class's best members on this
corpus are macro-sleeve books whose standing is hostage to open ideas 100/102/105/106.**

## Caveats, carried not buried

- **The sleeve books inherit every open question about the sleeve.** Idea 100's sleeve is a PARK;
  idea 102 found GLD carries 53% of its return and TLT much of the rest; ideas 105 and 106 are open
  on whether the exposure is gold specifically and whether DBC's contribution is a contango
  artefact. Nothing here is a claim that the sleeve is a good book — only that the class is not
  one book, and that the sleeve construction is where its best members currently sit.
- The class's members earn 7–9% CAGR against SPY's 15.4%. They are defensive sleeves, not
  capital-worthy books under 4b, and this run does not propose adopting one.
- **Survivorship** (idea 54): three current-constituent panels. It runs *toward* this finding —
  absent delistings inflate the fully-invested books' CAGR most, so the floor's exclusion of
  defensive arms is if anything understated here.
- **Idea 128**: the IS window (SPY MaxDD −22.1%) is shallower than the OOS window (−33.7%), so every
  IS-window drawdown screen, S1/S2/S3 included, is biased toward over-admission.
- **Idea 38**: u56/broad still carry the calendar-day index; it applies identically to every arm
  inside a cell and cancels in the cross-book comparison this run is about.
- **Idea 126**: every number is at t+1 execution only; no lag band is claimed.
- A matched-gross row is a different instrument from its native row and is never quoted as one.
  MaxDD is one number off one path, and both Pareto fronts inherit that fragility.
