# Idea 706 — is the SELECTION-RATIO SIGN FLIP a BREADTH EFFECT in disguise?

**cloud lane, 2026-09-16.** Script
`2026-09-16_is-the-SELECTION-RATIO-sign-flip-a-BREADTH-effect-in-disguise_cloud.py`.
Two tuned dials: **e = n/n_elig {0.05, 0.10, 0.25, 0.50} × cap mix q {0.00, 0.50, 1.00}** — all 12
cells reported. Reported, not tuned: k ∈ {40, 60, 80, 100, 200, 400}, 8 seeded draws per (q, k),
idea 694's n/k arm at the same four rungs (the reproduction), two implementations of e (E_STAT =
fixed n from the **IS-only** mean eligible count; E_DYN = idea 157's ADAPT, n_t = round(e·E_t)),
and EWall (e = 1.000). 1,469 book rows over 113 panels + a 192-book vintage arm.
**Gates 6 of 8 — and the two failures are the headline.**

## (0) THE REPRODUCTION FAILS AT q = 1.00, AND THE REASON IS THE DATA, NOT THE CODE

| q | this run, 694's own k range | 694's committed `partial_ratio_given_k` |
|---|---|---|
| 0.00 | **+0.7988** | +0.8044 ✔ |
| 0.50 | **+0.6817** | +0.6808 ✔ |
| 1.00 | **+0.0471** | **−0.5022** ✘ |

`data/prices_small` was **rebuilt on 2026-09-11** from 720 screened tickers. Idea 694 (run
2026-09-11, calendar to 09-04) drew from a **439-name** pool; today's usable pool is **663**
(+51%), and the repo's squashed history cannot check the old one out. So "the pure small pool"
694 measured no longer exists.

**Which half of the change carries it (PART A2b, seeded 439-name subpool of today's names —
694's pool SIZE, different NAMES):** ρ = **−0.1101** full-k, **+0.0355** on k ≤ 100. Pool size
closes **0.157 of the 0.549 gap (29%)**; the remaining **71% is the identity of the names**.
**H_KBLOCK FAIL** too: the k ≤ 100 block (the only widths all three cap mixes share) reads
**+0.1481**, also positive, so the published negative is not a wide-panel artefact either.

## (1) THE QUEUE'S TEST — there is no sign flip left to explain

ρ(dial, OOS Sharpe | k), k ≤ 100 matched block:

| q | n/k (694's cut) | e, E_STAT | e, E_DYN |
|---|---|---|---|
| 0.00 | +0.7988 | +0.6469 | +0.4882 |
| 0.50 | +0.6520 | +0.5834 | +0.5029 |
| 1.00 | **+0.1481** | **+0.1329** | **+0.2137** |

**H_FLIP FAIL** — but it fails *upstream*: on today's data the n/k cut itself is positive at all
three q, so the re-cut cannot be scored against a flip that is not there. What the run can still
say, and does:

- **H_GEOM PASS.** The two ratios really are different objects: at a fixed n/k the small-cap book
  holds **1.751×** the share of its eligible set that the large-cap book holds (realised e at
  n/k = 0.25: **0.3976 / 0.5017 / 0.6815** across q; breadth **0.684 / 0.536 / 0.380**, which
  reproduces 694's committed 0.68 / 0.50 / 0.33 to 0.05, gate G5).
- **H_MATCHED PASS, weakly.** Over the shared realised-e window the three ladders agree in sign
  (**+0.7382 / +0.6424 / +0.0967**, 78 / 99 / 114 rows) — but they already agreed on the n/k cut,
  so the matched-e test has no discriminating power on this vintage. It is reported as a PASS with
  that caveat stated, not as evidence.
- **The cap axis still modulates the STRENGTH.** q = 1.00's slope is about **one eighth** of
  q = 0.00's on both cuts. Concentration pays everywhere now; it just pays ~8× less in small caps.
- **H_EDOM FAIL.** Pooled on the matched block, **|ρ(n/k, OOS S | k)| 0.3004 > |ρ(e, OOS S | k)|
  0.2174** — the queue's proposed dial explains *less*, not more. Re-cutting on n/n_elig is not an
  improvement to the record's ratio ladder.
- **H_DYN PASS.** E_STAT and E_DYN agree in sign at all three q, so nothing here depends on
  whether e is held on average or day by day.

## (2) RULE 8 (walk-forward) and both KEEP paths

e chosen on 2009–2016 IS Sharpe inside each (q, draw) choice set, 2017– read once, against the
choice set's own mean OOS (the do-nothing anchor), RULES v2 on the same panel, and SPY.

- Best cell, **RATIO q = 0.00 DIAL-MAX**: OOS CAGR **11.85%**, OOS Sharpe **1.0415**, OOS MaxDD
  −18.61%, against **SPY OOS 15.33% / 0.8767** and **RULES v2 OOS 8.69% / 1.1158** on the same
  panels — it beats SPY's Sharpe in 8 of 8 draws and RULES v2's in 0 of 8.
- At q = 1.00 every selector loses to SPY on Sharpe (beats_spy 0.000) and the IS chooser hits the
  OOS-best rung 0 of 8 on the n/k cut.
- `DIAL-MAX` (concentrate) beats the anchor 0.625–1.000 everywhere, which is the same finding as
  the positive slopes, taken at the selector level.
- **KEEP paths: 4a 0 of 1,469. 4b 49 of 1,469**, and the footprint is entirely the cap axis —
  **q = 0.00 44, q = 0.50 5, q = 1.00 0 of 368**. Every passer is a committed CAND-n / EWall book
  on a random sub-panel of BSTK100: a statement about the draw, not a rule. **No KEEP candidate,
  no memo, RULES.md untouched.**

## VERDICT — **KILL the premise.** The flip is not a breadth effect; it is not there any more

**ANSWERED, and the answer is not the one the queue asked for.** On today's data ρ(n/k, OOS
Sharpe | k) is **positive at all three cap mixes** (+0.80 / +0.68 / +0.05), so the −0.37/−0.50
small-cap negative the queue set out to explain **does not reproduce**. It is neither a
wide-panel artefact (k ≤ 100 reads +0.15) nor a pool-size artefact (a 439-name subpool recovers
only 29% of the gap): **71% of it belongs to the 439 particular names the small pool used to
contain**, and that pool was replaced on 2026-09-11. **KILL** idea 694's headline #4 ("concentrate
in small caps, spread in large ones") as a standing fact. **CONFIRM** the weaker claim it sits on:
concentration pays on every cap mix, about 8× more strongly on large caps than small.
**KILL H_EDOM** — n/n_elig is a worse predictor than n/k, so the re-cut is not an upgrade.
Gates 6 of 8, hypotheses 3 of 8, nothing promoted.

**SURVIVORSHIP.** SMALL439 and BSTK100 are **current** constituents of their screens
(`data/SMALL_PANEL_README.md`): every name survived the whole sample by construction, every CAGR
here is optimistic, and q — the axis this run is about — is precisely the axis that bias hits
hardest, because the small screen is the one rebuilt from today's names. This run is itself a
demonstration of the cost: the screen was rebuilt five days after 694 ran and took its headline
with it.

**Naming defect, reported:** the record's `SMALL439` label now denotes a **663**-name pool. Any
committed claim citing "SMALL439" is a claim about whichever pool existed when it ran.
