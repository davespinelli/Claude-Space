# Idea 433 — adopt-the-T1-DEGREE-DETECTOR-as-the-PROTOCOL-corpus-gate (cloud, 2026-09-08)

**ANSWERED. The queue's question ("which one should the clause name?") has a false premise: the
two instruments have DISJOINT domains, and the clause needs BOTH, in a fixed order.**

Script: `2026-09-08_adopt-the-T1-DEGREE-DETECTOR-as-the-PROTOCOL-corpus-gate_cloud.py`
(reads idea 428's PART 0 verbatim, sha256[:16] `8dbb98aa47fd80cb`, 307 lines — 428's own book
does not re-run). Outputs: `.console.txt .keys.csv .census.csv .coverage.csv .fnfloor.csv
.verdicts.csv .walkforward.csv`.

## The headline

On a 20-key corpus with hand-derived ground truth, read under the reading a PROTOCOL line
actually gets (ONE instrument policing BOTH usage forms — an absolute cut `key >= L` and a
cross-sectional ranker `rank(key) <= n`):

| clause | clears | FALSE clearances | false rejections |
|---|---|---|---|
| DET (idea 428's degree detector) | 12/20 | **4** — PXDIFF, LOGPX, PXRANK, DVRANK | 1 — REBASED |
| CERT rank-invariance, tol 0 | 5/20 | 1 — MKTLVL | 5 — MOM, R6, PCT, REBASED, DDTR |
| CERT value-invariance, tol 0 | 8/20 | 0 | 1 — VOLAT |
| CERT rank-invariance, 1 rank step | 10/20 | 1 — MKTLVL | 0 |
| **CERT value-invariance, 1 rank step** | **9/20** | **0** | **0** |

So the *value* certificate at a one-rank-step tolerance is the only instrument that is exactly
right on all 20 keys — and it is **not** the instrument idea 426 drafts (that is the *rank*
certificate, which clears `px.mean(axis=1)`: a single-column price aggregate has no cross-section
for a per-name rescale to re-order).

But the certificate has no reach. DET types every file in the corpus with no data and no
execution; CERT needs a runnable key. Of 394 committed files, 335 (85.0%) define a module-level
function taking a price-like argument and 218 (55.3%) define one callable as `fn(px)` — and that
55.3% is an **upper bound**, because "callable as fn(px)" does not mean the function returns a
key (most return weights, tables or None). Everything else needs a hand-written harness before
the certificate can be applied at all.

## Recommendation (the deliverable the queue asked for)

1. **DET is the GATE** — corpus-wide reach, no data, no execution; it reproduced 428's committed
   census exactly (293/293 hits on the 157 files both runs saw, 0 new, 0 missing).
2. **CERT is the ADJUDICATOR, in its VALUE form at a one-rank-step tolerance** — 0 false
   clearances, 0 false rejections. Name the value certificate, not the rank certificate.
3. Two amendments must go in with the clause or it is quoted on wrong numbers:
   * DET's degree tables mis-type `diff` and `rank` as degree-0, `var` as degree-1, leave
     `np.log` untyped, and its `div`/`mul` handling keeps the receiver's degree while ignoring
     the argument's — which false-positives `px.div(px.iloc[0], axis=1)` (REBASED, arithmetically
     degree 0). That is 4 false clearances and 1 false rejection on 20 keys.
   * **The queue's "reads all 379 scripts in ~2 s" is wrong by 45x: measured 89 s** (226 ms/file,
     median 216 ms, p90 365 ms). `run()` walks the AST three times per function and is called once
     per function, so cost is ~O(functions × nodes). Still cheap absolutely, but reach — not
     speed — is the detector's advantage, and the clause must not be sold on the 2 s figure.
4. DET is structurally blind to the RANK family: **0/20 flags in the rank form**, because
   `rank(...) <= n` is degree 0 whatever the key. Ten of DET's fourteen false negatives are of
   that kind. This is why the pair, not the choice.

## Pre-registered predictions

| | prediction | result |
|---|---|---|
| P1 | ≥4 LEVEL-form disagreements AND DET rank-form flag rate 0/20 | **HIT** (6 disagreements; 0/20) |
| P2 | CERT has a false negative of its own (single-column price aggregate) | **HIT** under the one-clause reading (rank certificate clears MKTLVL); **MISS** under the form-matched reading (0) |
| P3 | DET reproduces 428's census exactly | **HIT** (293/293 on the shared file set) |
| P4 | CERT automatic coverage < 25% of files | **MISS** (55.3% upper bound) |
| P5a | no SMALL439 arm clears 4b | **HIT** (0/208) |
| P5b | the T1-unsafe PXQ arm does not beat its no-screen comparand OOS on U56 | **HIT** (+0.0000) |

## Consequence book — the clause costs capital nothing (PROTOCOL 2/3/4/8)

Panels SMALL439 (`max_1d_move >= 1.0` dropped) and U56; books EWALL and MA200; gross 0.75;
weekly, t+1; costs 0/5/10/25 bps; screens NONE / PXABS(level) / PXQ(matched admission) /
VOLQ(matched admission, small panel only). Two tuned parameters — instrument and level. All 352
grid points in `.verdicts.csv`.

* **4a KEEP 4/352, 4b KEEP 14/352.** SMALL439 4a 2/208, 4b **0/208** (0/52 at 10 bps).
  U56 4a 2/144, 4b 14/144 (4/36 at 10 bps).
* The four 10-bps 4b passes are `U56/NONE_0/MA200/rw`, `U56/PXABS_2/MA200/rw`,
  `U56/PXQ_2/MA200/rw`, `U56/PXQ_5/MA200/rw`. The un-screened control is among them, and
  `PXQ_2` on U56 admits 1.000 of the panel — it *is* the control. So the clause deletes nothing
  the un-screened book does not already deliver.
* U56 reference @10 bps: SPY 15.23%/0.889/-33.7% (H1 0.957, H2 0.834, OOS 0.882);
  RULES v2 8.66%/1.206/-12.1%. SMALL439: SPY 14.13%/0.862/-33.7% (OOS 0.882);
  RULES v2 3.80%/0.571/-14.7%.
* **Rule 8** (screen level chosen on ≤2016-12-31, 2017-2026 read once, 40 cells): the chooser
  loses to simply not screening in **0/40** cells, mean **−0.0407** OOS Sharpe (t −6.03);
  vs SPY mean −0.1318, wins 16/40. Oracle headroom over the whole level ladder is **+0.0000** —
  perfect hindsight buys nothing, because every screen is monotonically costly.
  Allowed to abstain the chooser picks no screen in 24/40 cells and still gives up −0.0101.

**Verdict: ANSWERED / report-only. No book, no PROTOCOL edit made here.** The T1 clause is a
reporting clause with no measurable book cost, which is why it is cheap to adopt — and why it
must not be presented as an edge.

## Caveats carried

* **SURVIVORSHIP.** Both panels are current-constituent lists. On SMALL439 the missing delisted
  cohort is exactly the thin, low-priced names a price floor argues about, so only
  screen-minus-screen contrasts are read there; every level is biased upward and no book is
  proposed on it. U56's 4b passes are the same u56 MA200/EWALL books already in the record
  (2026-09-08 KEEP memos) and are not a new signal.
* The ground truth is hand-derived arithmetic stated per key in the script's `KEYS` table, not a
  third instrument. The value certificate agrees with it on 20/20, which is expected — its
  theorem is exact — so the interesting numbers are the disagreements, the domains and the costs,
  not the accuracy score.
* The CERT panel is one deterministic 750×140 SMALL439 slice at sigma 0.25, 8 draws, seed 433.
  U56 has no cached share volume, so the three volume-bearing keys use a deterministic
  price-free surrogate there; that is stated in the script, not hidden.
* The 20-key corpus is chosen to span the hard cases, so it is adversarial by construction and
  its flag RATES are not estimates of the record's own composition. The census (`.census.csv`)
  is what carries the record's composition: B1 4, B2 46, B3 258, Z 11, PARSE_FAIL 1.
