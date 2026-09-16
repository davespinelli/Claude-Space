# Idea 1002 — should a ROTATING NULL be PINNED to a PRICE VINTAGE?

**cloud lane, 2026-09-16.** Script `2026-09-16_should-a-ROTATING-NULL-be-PINNED-to-a-PRICE-VINTAGE_cloud.py`.
**GATES 10 of 10. HYPOTHESES 7 of 11** — and the four failures are the answer.
Runtime 186 s.

## ANSWER = NO. PINNING BUYS NOTHING MEASURABLE, AND 971's HEADLINE DOES NOT REPRODUCE

On the only restatement pair that exists in this repository's history — `data/prices.csv` at
git shas **78761a0 (V0)** and **868b5c3 (V1)** — a rotating `ROTP` null drawn at **identical
seeds** on both tapes moves by:

| | U56 | B136 (one committed revision) |
|---|---|---|
| RMS restatement effect on OOS Sharpe | **0.000098** | 0.000000 |
| max \|dSharpe\|, 27 cells × 100 seeds | **0.000269** | 0.000000 |
| sampling sd of the same statistic | **0.0703** | 0.0534 |
| **restatement / sampling VARIANCE share** | **3.53e-06** | 0.00e+00 |
| REC 4b verdict flips on identical seeds | **0.0000** | 0.0000 |

`H_SHARE` **PASS at 3.5e-06**: the restatement channel is **0.19% of one sampling standard
deviation**. The answer to the queue's question — *how much of the record's committed null
variance is tape restatement rather than sampling* — is **essentially none of it**, and the
drawdown-leg share is exactly 0.000000. `H_REC` **PASS at 100%**: `RMS_REST` sits below idea
999's own committed per-cell null sd on **27 of 27** shared cells (0.0001 vs 0.0703).

**`H_MOVE` FAILS**, and it is a real failure: the restatement does not move the null by even
0.01 of Sharpe. **`H_254` FAILS** — 971's published U56 headline of **max \|dSharpe\| 0.254**
reads **0.0003** here, three orders of magnitude smaller. **`H_FLIP` FAILS** — its published
**7.4% REC-4b flip rate on identical seeds** reads **0.0%**, 0 flips of 2,700 paired draws.
971's artefacts are not in this tree, so these are tests of published claims and not bit-level
cross-run gates; said plainly, and the gap is far too large to be a convention difference.

**`H_PIN` FAILS with the sign against it**: pooling over (draw × vintage) makes the sd of OOS
Sharpe **−0.25%** *smaller*, not ≥5% larger. There is nothing for a pin to remove.

## THE TAPE DID MOVE — THE NULL JUST DOES NOT CARE

This is not a null result because nothing was restated. On the 4,704 × 58 common block
(gate G6, published before any draw), V0 and V1 disagree on **26,807 of 272,832 cells
(9.8%)** in **48 of 58 columns**, max relative move **0.62%**. The restatement is
**concentrated**: `UNH` moves on **4,703 of 4,704 days** (a whole-history adjustment-factor
restatement), then DIA 1,924 / SPY 1,370 / COST 1,290.

The ablation arms partition that exactly (gate G7, 0.0):

| arm | what it isolates | RMS on OOS Sharpe | share of the full effect |
|---|---|---|---|
| `REST_UNH_ONLY` | the one column `UNH` | 0.000098 | **0.9996** |
| `REST_EX_UNH` | the other 47 restated columns | 0.000001 | 0.0054 |
| `REST_COMMON` | both | 0.000098 | 1.0000 |

`H_ONENAME` **PASS at 0.9996**. **A 9.8% cell-level restatement of the tape reaches the null
through a single name, and even that is 0.19% of a sampling sd.** The reason is structural:
`ROTP` matches the book's holding COUNT and per-name weight and only re-rolls *which* names
are drawn, and a sub-1% adjustment-factor move reorders the eligibility pool almost nowhere.

## THE LENGTH CHANNEL IS 20× BIGGER — AND STILL IRRELEVANT

Read at each sha's **own natural length** (V1 carries one extra trading day), which is what a
reader who simply reloads the file sees: RMS **0.001976**, max \|dSharpe\| **0.004834**, share
**6.6e-04**, flips **0.0000**. `H_LENGTH` **PASS**. So the larger of the two channels available
here is *when the tape ends*, not *what it says* — 20× the restatement effect and still four
orders of magnitude inside the sampling noise.

`H_CAD` **PASS**: the share's ordering is **W > M > Q at every cost rung**, i.e. the faster the
cadence the more restatement leaks in, as more rebalance decisions are exposed to it. The
ordering is stable; the magnitudes are not material at any of them.

## RULE 8 — the vintage swap changes no verdict at all

(book, cadence) chosen on **2009–2016 using V0 ALONE** by three IS-only choosers, 2017–2026
read **once**, on V0 and again on the restated V1, three cost rungs, both KEEP paths:

- **18 of 18 picks keep their 4b verdict and 18 of 18 keep their 4a verdict.** Max
  \|dOOS Sharpe\| across the swap: **0.000120**. `H_RULE8` **PASS**.
- **OOS 4b 0 of 18, OOS 4a 0 of 18.** The picks are `U56/EWELIG/Q` (binds `L4_DD` at
  −22.21% against the −20.23% cap), `U56/BAND03/W` = the live book (binds `L5_CAGR`),
  `B136/TOP20/M` (`L4_DD`) and `B136/BAND03/W` (`L5_CAGR`).
- Comparands, same OOS window: SPY **15.27% / 0.8741 / −33.72%**; RULES v2 (live)
  **9.47% / 1.2776 / −12.05%** (U56) and **7.88% / 1.1061 / −12.24%** (B136).

No KEEP candidate on either path, so no memo.

## VERDICT — KILL the proposal, keep one reporting line

Pinning a rotating null to a committed price sha is **not worth the machinery**: on this tape
it changes the fourth decimal place of a Sharpe and no verdict anywhere. The only defensible
residue is a one-line disclosure, offered for Sunday review and **not written into
PROTOCOL.md** (rule 6): *"a null quoted across runs states the price sha it was drawn on, so
that a future disagreement can be attributed rather than argued."* That is bookkeeping, not a
correction.

## GATES, 10 of 10

G0 masks ≡ `engine.rebalance_mask` (0 rows). G1 fast `Ctx` ≡ `engine.backtest` (2.08e-17 /
4.44e-16). G2 `band_book(0.03,0.75)` ≡ `baseline.rules_v2_weights` (0.0). **G3 LIVE working
tree ≡ PIN_V1 byte for byte.** G4 determinism (0.0). G5 null gross/count match on **every**
vintage (0 / 1.11e-16). **G6 the tape-delta census published before any null was drawn.**
**G7 the two ablation arms rebuild V0 and V1 exactly (0.0).** **G8 B136's seven vintage arms
are the same tape (0.0)** — 971's "bit-for-bit" finding, reproduced structurally. G9 idea
999's committed U56 nulls read for their own per-cell sd, 27 shared cells.

## THE RESOLUTION LIMIT, STATED BEFORE THE RESULT AND AGAIN HERE

This sandbox has no network, so the only honest vintages are this repository's own git blobs,
and there is **exactly one restatement pair** in the history of `data/prices.csv`
(`prices_broad.csv` and `prices_small.csv` have one revision each — which is why B136 is a
structural zero arm rather than a measured one). Everything above is a **one-pair point
estimate with no sampling distribution over vintages**. What it establishes is the DIRECTION
and the DECOMPOSITION, not a confidence interval on the channel's size.

## SURVIVORSHIP (PROTOCOL rule 9)

U56 and B136 are current-constituent lists, so every level is optimistic. The measured object
is a difference between two vintages of the SAME survivor list, so the bias is common to both
arms and cancels in `SHARE` and `FLIP` almost exactly. What does **not** cancel: a restatement
that **delists or adds a name** would be the largest vintage channel there is, and a
current-constituent panel cannot contain one by construction. **This run therefore measures
only the adjustment-factor half of the restatement channel and is a LOWER bound on the
real-time one.** Said once, and not worked around.

**NOT MODIFIED (rule 6):** RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py.
