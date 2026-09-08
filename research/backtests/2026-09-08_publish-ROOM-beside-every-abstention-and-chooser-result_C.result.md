# Idea 457 — publish ROOM beside every abstention (and chooser) result (lane C, 2026-09-08)

**Verdict: ANSWERED / clause DRAFTED, and the abstention rule KILLED again on its own terms.
The queue's premise is CONFIRMED and made quantitative: 277 of the 425 auditable positive
abstention verdicts in the record (65.2%) flip to ≤ 0 once ROOM is netted out. No KEEP
(4a 0 of 24 books, 4b 0 of 24 for every book under test).** RULES.md, scan.py, bot.py,
baseline.py and PROTOCOL.md untouched; the clause below is a DRAFT for the Sunday review.

Script `2026-09-08_publish-ROOM-beside-every-abstention-and-chooser-result_C.py`
(deterministic, seed 457000, no network, ~4 min). Artefacts alongside: `.console.txt`,
`.room.csv`, `.taugrid.csv`, `.verdicts.csv`, `.ledger.csv`, `.arms.csv`, `.livecells.csv`,
`.calgrid.csv`, `.livegrid.csv`, `.keeppaths.csv`, `.walkforward.csv`.

## The algebra (this is the whole idea)

For a cell with an IS argmax `star`, a labelled control `ctl` and a menu OOS mean, an
abstention rule that falls back to the control when its gate fires earns

```
D = mean[ OOS(pick) − OOS(star) ] = f · ( ROOM_fired − LIFT_fired )
ROOM = OOS_ctl  − OOS_mean     (a verdict on the CONTROL vs a random menu arm)
LIFT = OOS_star − OOS_mean     (what the ARGMAX buys vs a random menu arm)
```

so a gate with **no information** firing at the same rate `f` on random cells earns
`f·(ROOM_bar − LIFT_bar)` in expectation. Two nettings are published at every point and
neither is selected: **ROOM-ONLY** (`D − f·ROOM_bar`, the queue's literal wording, and the
right null when the verdict is quoted against the menu mean) and **FULL-NULL**
(`D − f·(ROOM_bar − LIFT_bar)`, the right null when the verdict is quoted against the raw
argmax, as idea 241's is). The exact within-file permutation null (2,000 draws, per-file
fire count held fixed) is carried beside them as the non-parametric reference.

**Identity check `D = f·(ROOM_fired − LIFT_fired)`: max error 5.20e-18 over all grid points.**

## Gates (passed before any new number was read)

| gate | requirement | result |
|---|---|---|
| G1 | cost-rung identity `net(c) = gross − TO·c/1e4` | **0.000e+00** |
| G2 | idea 241 lane B's four published decomposition numbers, re-read off its committed census | ROOM +0.02583 (t +22.21) vs published +0.0258 (+22.2); LIFT +0.02008 (+11.76) vs +0.0201 (+11.8); star−ctl −0.00575 (−3.19) vs −0.0058 (−3.2); regret +0.04780 (+26.94) vs +0.0478 (+26.9). **max \|Δmean\| 4.98e-05, max \|Δt\| 4.0e-02** |

## A. The back-fill — ROOM over the 1,834 control-carrying census cells

1,834 Sharpe cells over **45 files**; the argmax **is** the control in 631 (34.4%), where
abstention is a no-op by construction. Pooled **ROOM +0.02583, LIFT +0.02008, ROOM−LIFT
+0.00575**. ROOM > 0 in **75.5%** of cells but exceeds LIFT in only **34.5%**.

**ROOM is not a constant** — the same objection idea 445 raised against quoting a single
REGRET. Per-file ROOM runs **−0.0206 … +0.1487** and is *negative* in 7 of 45 files (the
control is a worse-than-average arm there), and on this run's own live panels it is
**−0.0837 (u56), +0.0013 (broad136), +0.0442 (small439)**. A netting constant imported from
another corpus is not evidence; ROOM has to be published per result.

Tuned parameters: exactly 2, **q** (threshold as a quantile of the corpus's own top-2 gap
distribution, 10 levels) × **norm** ∈ {raw, z, rng} — idea 241 lane B's ladder imported
verbatim, not re-fitted. All 30 points are in `.taugrid.csv` and printed in the console; the
ROOM-estimator (POOLED | PERFILE) × netting-basis (ROOM-ONLY | FULL-NULL) matrix is a
reporting axis published at all 4 levels with no point selected.

Of the **24 non-degenerate grid points with D > 0** (median raw D +0.00450):

| netting | still > 0 | median netted D |
|---|---|---|
| POOLED ROOM-ONLY | **0 of 24** | −0.00940 |
| PERFILE ROOM-ONLY | **0 of 24** | −0.01184 |
| POOLED FULL-NULL | 16 of 24 | +0.00071 |
| PERFILE FULL-NULL | 12 of 24 | +0.00077 |
| exact permutation null | 5 of 24 | −0.00434 |

Against the matched-rate random gate the record's abstention ladder is **significantly ABOVE
it at 3 of 24 points, significantly BELOW it at 18, indistinguishable at 3**. The three that
beat a random gate keep 11–15% of their published D: `raw/q0.9` +0.00901 → **+0.00111**,
`rng/q0.8` +0.01180 → **+0.00175**, `rng/q0.9` +0.00794 → **+0.00085**. The queue's own
pre-registered anchor τ = 0.013 raw: D +0.00300, ROOM-netted **−0.00964**, permutation-netted
**−0.00490**.

## B. The published-verdict census — how many verdicts flip

2,018 committed CSVs re-read (this run's own artefacts excluded, so the census is idempotent).
A row is an ABSTENTION VERDICT if its file publishes **both** a fire-rate column and a
delta-vs-pick column; the column actually used is published per file, and every rejection is
counted (1,997 no fire-rate column, 7 no delta column, 1 non-numeric).

**13 files admitted, 1,276 verdict rows** (RECORD 730, LIVE 210, UNKNOWN 336). Anchor
certificate — the file's own `f = 0` row publishes delta exactly 0 — holds in **6 of the 9
files that carry such a row**; 4 files carry none. Signs as published: **607 POSITIVE, 606
NEGATIVE, 63 NEUTRAL**.

**Of the 607 positive verdicts, 425 are auditable (all RECORD-scope; the 182 UNKNOWN-scope
rows have no reconstructable ROOM and are counted as UNAUDITED, never as a pass):**

| netting | flip to ≤ 0 | share of the 425 auditable | survive |
|---|---|---|---|
| **ROOM-ONLY** | **277** | **65.2%** | 148 |
| FULL-NULL | 67 | 15.8% | 358 |

By file (positive rows only): `the-mid-tercile-band_cloud.walkforward` 133 of 229 flip,
`the-mid-tercile-band_cloud.bandgrid` 112 of 284, `the-013-margin-rule_B.taugrid` **26 of 26**,
`the-013-margin-rule_cloud.tau` **5 of 5**. Netted under *every* ROOM estimate this run
measured, 0 of 607 flip under all of them and 53 survive all of them — the remaining 554 are
estimator-dependent, which is the same finding as part A: the netting constant is a property
of the corpus, so it must be published with the result rather than imported.

## C. Rule 8 on live prices, out of corpus

Fresh 31-arm menu (band × gross × cadence + an ungated control) × 3 panels × 2 cost rungs,
**300 seeded sub-menus per (panel, cost) = 1,800 live cells**, arms read on 2010–2016, τ
chosen on **2014–2016 only**, 2017–2026 read once, t+1 execution, 260-bar warm-up skip.

**Coverage limit, reported not buried:** the ungated control is the IS argmax in **100% of
broad136 and small439 cells**, so the gate is a strict no-op on two of three panels. The live
evidence is **u56-only** (600 cells, 24.3% of them with a non-control argmax). Live ROOM:
u56 **−0.0837**, broad136 +0.0013, small439 +0.0442.

Calibration picked `raw/q0.9` (τ 0.0465, calibration D **+0.0757** at a 90% fire rate). Read
once OOS: **D −0.03226 (t −24.5)**, ROOM-netted −0.02089, FULL-NULL −0.00348,
**permutation-netted −0.00016 (p 0.015)**. The entire live effect — all of it, and it is
negative — is what a random gate firing at the same rate would have produced.

| panel/cost | book | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR | OOS Sharpe | OOS MaxDD | 4a | 4b | 4b OOS |
|---|---|---|---|---|---|---|---|---|---|---|---|
| u56 10bps | **ABSTAIN** | 17.74% | 1.1245 | −29.18% | 1.192 / 1.072 | 18.47% | **1.1353** | −29.18% | False | **False** | False |
| u56 10bps | ARGMAX | 11.00% | 1.2255 | −15.46% | 1.273 / 1.184 | 11.66% | 1.2731 | −15.46% | False | True | True |
| u56 10bps | INCUMBENT | 17.74% | 1.1245 | −29.18% | 1.192 / 1.072 | 18.47% | 1.1353 | −29.18% | False | False | False |
| u56 10bps | **RANDGATE** | 17.72% | 1.1248 | −29.14% | 1.192 / 1.072 | 18.46% | **1.1356** | −29.14% | False | False | False |
| u56 10bps | RULES v2 (live) | 8.66% | 1.2056 | −12.05% | 1.226 / 1.191 | 9.53% | 1.2851 | −12.05% | — | — | — |
| u56 10bps | SPY | 15.23% | 0.8890 | −33.72% | 0.957 / 0.834 | 15.45% | 0.8820 | −33.72% | — | — | — |

(the 25 bps rung and both degenerate panels are in `.keeppaths.csv`; RULES v2 OOS Sharpe
1.1185 on broad136 and 0.5680 on small439.)

**The headline of part C, on the 2 of 6 books where the gate moves at all:
ABSTAIN − ARGMAX = −0.1221 of OOS Sharpe, ABSTAIN − RANDGATE = −0.0005.** The abstention book
is the random-gate book to within half a thousandth of Sharpe, and both give up 0.12 of Sharpe
and double the drawdown (−15.5% → −29.2%) against simply keeping the argmax.

**KEEP paths: 4a 0 of 24 books, 4a(OOS) 0 of 24, 4b 2 of 24, 4b(OOS) 2 of 24 — and both 4b
passes are the ARGMAX book on u56 (10 and 25 bps), not the object under test. ABSTAIN 0/6 and
RANDGATE 0/6 on every path.** The ARGMAX pass is idea 439's known gross-1.00 family, already
in the record; no memo, nothing promoted.

## D. The drafted clause (extends idea 445's proposal to abstention; PROTOCOL.md NOT edited)

```
10b. Abstention results publish ROOM and the matched-rate null, not the raw delta
     (proposed, idea 457; extends the idea-445 clause from SELECTION to ABSTENTION).
     A rule that hands a cell back to a control (an abstention, fallback, veto or
     "do-nothing-unless" gate) may not claim it helps from its delta alone.  With
     f the fire rate,

         D = mean[ OOS(pick) - OOS(argmax) ] = f * ( ROOM_fired - LIFT_fired )
         ROOM = OOS(control) - OOS(menu mean)   LIFT = OOS(argmax) - OOS(menu mean)

     the result must publish f, ROOM measured on ITS OWN corpus (never imported: ROOM
     runs -0.084 to +0.149 across the corpora measured here, and is negative in 7 of the
     record's 45 control-carrying files), and D net of the matched-rate null
     f*(ROOM_bar - LIFT_bar) -- or, preferably, net of an explicit permutation null that
     re-draws WHICH cells fire while holding the per-corpus fire count fixed.  A gate whose
     netted D is not distinguishable from that null has not been shown to carry information,
     however large and however significant its raw D.  A verdict quoted against the menu
     mean or a random arm nets ROOM in full; one quoted against the raw argmax nets
     ROOM - LIFT.  The control's identity and the menu length are named in both cases.
```

## Predictions vs outcomes

| | prediction | outcome |
|---|---|---|
| R1 | the record's positive abstention verdicts are mostly ROOM | **CONFIRMED** — 65.2% of the 425 auditable flip under ROOM-ONLY; 15.8% under the stricter FULL-NULL |
| R2 | ROOM is not a constant | **CONFIRMED** — per-file −0.0206…+0.1487, negative in 7 of 45 files, −0.0837 on live u56 |
| R3 | the live abstention effect is the random-gate null | **CONFIRMED** — OOS D −0.03226, permutation-netted −0.00016; ABSTAIN − RANDGATE −0.0005 of OOS Sharpe |
| R4 | no KEEP | **CONFIRMED** — 4a 0/24, 4b 0/24 for ABSTAIN/RANDGATE/INCUMBENT; the 2 ARGMAX 4b passes are a known family |

## Caveats

* Parts A and B are a re-reading of committed artefacts. The 1,834-cell census is idea 241
  lane B's, taken as given after its four published numbers reproduce to 5e-05 (G2); a
  defect in that census propagates here.
* 182 of the 607 positive verdicts (30%) are UNKNOWN-scope and cannot be netted; they are
  reported as unaudited, never as passes. The published bound over every ROOM estimate this
  run measured is deliberately wide because ROOM itself is not a constant.
* The verdict census is mechanical: a file is admitted on the presence of a fire-rate and a
  delta column, and 4 of 13 admitted files publish no `f = 0` anchor row to certify the
  delta's sign convention. Column choice per file is published in `.ledger.csv`.
* Cells and files are not independent (shared panels, prices, dials); the permutation null
  blocks within file, and file counts are published beside every pooled number.
* SMALL439 is a **current-constituents** panel (`data/SMALL_PANEL_README.md`) with
  `max_1d_move >= 1.0` tickers dropped: **survivorship bias**, a shape check only, never a
  tradable return. It is also one of the two degenerate panels here.
* 10 bps is the protocol rung; 25 bps is carried as a robustness axis.
