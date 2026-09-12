# Idea 839 — is the NEGTURN → cost_surv ordering a FINDING or an IDENTITY?

**Lane C, 2026-09-12.** Script `2026-09-12_is-the-NEGTURN-to-cost_surv-ordering-a-FINDING-or-an-IDENTITY_C.py`.
Runtime 534 s. 10 bps, next-day fill, each family's committed cadence. **No new constructors** —
the 39-arm corpus, the panels and the 4b leg definitions are copied verbatim from idea 837.

## ANSWER: **IDENTITY.** And no residual ordering of OOS Sharpe survives either.

**13 of 15 pre-registered hypotheses PASS**, and the two failures are the two that had to fail for
the answer to be "identity": `H_RESID_SIG` (no real residual) and `H_OOSSH_0` (no surviving
OOS-Sharpe ordering).

## First: the queue's number is on a column the queue does not name (gate G1)

837's committed `+0.4637` is **`cost_surv_OOS`** — the **OOS-window-local** 4b survival — not the
fixed-window `cost_surv`, which on 837's own committed file reads **+0.5018**. Its reading (b) maps
the target to the `_OOS` column; the memo prose says only "cost_surv". Both windows are carried at
every cell here. G1 rebuilds **all three** committed cells to `|d| = 0.0000` (+0.4637, +0.5018,
+0.4587) and every book-level column to **≤ 1.776e-15**, `cost_surv` and `cost_surv_OOS` **bit-exactly**.

**G1–G4 all PASS.** G2: the analytic ladder `r0 − turnover·c/1e4` equals the engine's `cost_bps=c`
backtest at c = 10 to **0.000e+00** over all 41 books — the identity's premise is exact, not
approximate. G3: the 4b pass indicator is monotone in c, **0 up-steps** over 51 rungs × 39 books,
on both windows, so `c_star` is well defined. G4: max realised gross **1.0000**.

## The arithmetic ceiling (K0)

`−turn` and `1/turn` are **the same ranking**: `rho(NEGTURN, 1/turn_yr) = +1.000000` exactly. Write
`D*` for a book's **drag budget** — the largest *flat* annual return drag (bps/yr) it absorbs while
still passing 4b, measured with turnover divided out. Then `c* = D*/turn_yr`. **If `D*` were
constant across books, the association would be exactly +1.0000 with zero information in the
corpus.** So 837's +0.4637 is not a signal sitting on top of an identity; it is what is *left* of
the identity once `D*` disperses.

The reconstruction confirms it is the identity and nothing else:
**`rho(c_star, c_hat) = +0.9949`** (OOSLOC/ALL39; +0.9986 fixed-window; ≥ +0.9385 at all 16
window × population × rung-set readings). Cost survival **is** `D*/turnover` to rank precision.

## The decomposition — headline cell OOSLOC / ALL39 / R11

| decomposition | target | n | Spearman | iid p | cluster 95% CI |
|---|---|---:|---:|---:|---|
| RAW (837's) | cost_surv(R11) | 39 | **+0.4637** | 0.0030 | [+0.0326, +0.7657] |
| MECHPRED | `D*/turn_yr` | 39 | **+0.4871** | 0.0018 | [+0.0415, +0.8001] |
| **DRAGFREE** | `D*` (bps/yr) | 39 | **−0.1137** | **0.4914** | **[−0.3875, +0.2308]** |
| DIVTURN | cost_surv × turn_yr | 29 | −0.5740 | 0.0014 | [−0.7576, −0.0144] |
| PARTIAL | cost_surv \| `D*` | 39 | **+0.8092** | — | [+0.5404, +0.9212] |

Four independent ways of saying the same thing:

1. **The mechanical model over-explains the observation.** `D*/turn_yr` gives **+0.4871** against
   the observed **+0.4637** — arithmetic share **1.0505**, i.e. **more than 100%** (H_MECH,
   H_SHARE PASS). There is nothing left for a finding to explain.
2. **Divide turnover out and the association is a null.** `D*` alone reads **−0.1137, p 0.4914**,
   cluster CI **[−0.3875, +0.2308]** — covers zero, and the point estimate has the *wrong sign*.
   Low turnover does **not** buy a bigger absolute cost headroom (H_RESID PASS, H_RESID_SIG FAIL).
3. **Undo the scaling on the observed target and the sign flips**: `cost_surv × turn_yr` reads
   **−0.5740**.
4. **Hold `D*` fixed and the association nearly doubles**, to **+0.8092** — which is what an
   identity does, and what a genuine signal would not.

**Robust across every reported axis.** Rung set moves the RAW cell by **0.0423** (H_SETFREE PASS:
R11 +0.4637, FINE +0.4827, COARSE +0.4404, CONT +0.4785) — the rung grid is not doing the work.
Population agrees in sign and significance (ALL39 +0.4637 p 0.0030; PASS0 +0.5655 p 0.0018;
H_POP PASS), and DRAGFREE stays a null-or-wrong-sign at both (PASS0 **−0.4680**, CI covering zero).
The fixed-window reading tells the identical story (RAW +0.5018, MECHPRED +0.5138, DRAGFREE
**−0.0470 p 0.7744**, PARTIAL +0.8208). **80 grid cells reported, all in `.grid.csv`.**

## The OOS-Sharpe leg: switch the cost channel off and the cell dies

The engine's only turnover → Sharpe channel is the 10 bps charge. Read the same cell down the cost
ladder (ALL39):

| cost bps | 0 | 5 | 10 | 15 | 20 | 25 | 30 | 50 | 75 | 100 |
|---|---|---|---|---|---|---|---|---|---|---|
| ρ(NEGTURN, OOS_Sharpe) | **+0.2518** | +0.3619 | **+0.4587** | +0.5820 | +0.6105 | +0.6490 | +0.6820 | +0.8038 | +0.8615 | +0.8864 |
| iid p | **0.1196** | 0.0236 | 0.0034 | 0.0001 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

**At zero cost the cell is +0.2518, iid p 0.1196, cluster CI [−0.2452, +0.6760] — not significant
by either null** (H_OOSSH_0 **FAIL**: no residual ordering survives). The drop from 10 bps is
**0.2069** (H_OOSSH_DROP PASS). PASS0 is weaker still: **+0.1611, p 0.4074**.

It is a clean monotone **dose–response in the charge**: ρ climbs from +0.2518 to +0.8864 as the
cost rises 0 → 100 bps, across 51 rungs without a reversal. `OOS_CAGR` makes the point even more
bluntly — **−0.5083 at 0 bps, +0.2275 at 40 bps, +0.7344 at 100 bps**: the sign of the association
is set by the size of the cost charge, not by anything about the books.

**So 837's best predictor is its cost model.** NEGTURN was the only iid-significant OOS-Sharpe
predictor in that census; at zero cost it is not significant at all.

## RULE 8 on the claim (read exactly once)

Chosen on **IS (..2016) only** by highest ρ across all 20 (decomposition, rung-set) cells:
**(PARTIAL, CONT), ρ_IS +0.7109** → read once on **2017.. : ρ_OOS +0.7877, gap 0.0768** against the
pre-registered 0.30 bar — **PASS**. The identity is stable out of window, as an identity must be.
The *residual* is not: DRAGFREE goes **+0.2667 IS → −0.1137 OOS** (gap 0.3804), and DIVTURN
+0.4389 → −0.1148 (gap 0.5537). All 20 IS/OOS pairs in `.walkforward_claim.csv`.

## PROTOCOL rule 8 on the books (mandatory)

39 arms, full window and OOS 2017-01-01.. . Arms: full CAGR 6.22–17.74% (median 11.92%), Sharpe
0.932–1.226 (median 1.117), MaxDD −24.32% to −11.13%; **OOS CAGR 6.38–19.03% (median 13.18%), OOS
Sharpe 0.993–1.394 (median 1.170), OOS MaxDD −24.32% to −11.13%**; turnover 1.15–13.97×/yr.
Comparands on the same windows: **RULES v2 LIVE** full 8.63%/1.2018/−12.05%, **OOS
9.47%/1.2782/−12.05%**; RULES v1 full 6.41%/0.6602/−13.83%, OOS 7.60%/0.7361/−13.83%; **SPY** full
15.16%/0.8861/−33.72%, **OOS 15.33%/0.8767/−33.72%**.

**KEEP paths: fixed-window 4b PASS 26 of 39; OOS-local 4b PASS 27 of 39; 4a PASS 0 of 39; BOTH 0 of
39** — reproducing idea 837 exactly. **No book is promoted and no KEEP is claimed**: this is a
census corpus enumerated to answer a decomposition question, not a search for candidates (idea
814's standard). **10 of 39 arms fail 4b at every cost rung including zero** — for reasons that are
not about cost at all (MARS-g0.50, MARS-g1.00, MADIST-q0.25, MADIST-q0.75, BRD-q0.10, EWALL-g1.00,
SHY-g0.375, SHY-g0.625, R6-n10, MARSB-g0.50); the PASS0 population exists so that group cannot
carry the result, and it does not.

## Verdict

**KILL. The NEGTURN → cost_surv ordering is an ARITHMETIC IDENTITY, not a finding, and no residual
ordering of OOS Sharpe survives its removal. No KEEP claimed, no book promoted, no memo.**
Cost survival is `D*/turnover` at ρ +0.9949; the mechanical model reproduces **105%** of the
observed association; the turnover-free residual is a null with the wrong sign (−0.1137, p 0.4914);
and 837's one iid-significant OOS-Sharpe predictor is not significant once the cost charge is set
to zero (+0.2518, p 0.1196), rising monotonically to +0.8864 as the charge is raised to 100 bps.
**Two of the nine cells 837 listed as "surviving, all mechanical" are now shown to be mechanical by
construction rather than by inspection** — and the record should stop counting `cost_surv` and
`gross_band` as targets that a book statistic can be said to *predict*.

**One correction the record needs, beyond the verdict:** 837's published `+0.4637` is its
`cost_surv_OOS` column, not `cost_surv` (+0.5018 on the same file). The leaderboard row and memo
name neither window. This is the same defect ideas 836 and 840 are chasing — a headline that does
not name the window it is read on — appearing inside a cell the queue then cited onward.

SURVIVORSHIP: U56 and B136 are current-constituent lists; every level above is optimistic. This run
reads orderings across books on one panel, which survivorship moves far less than a level, but no
CAGR or Sharpe printed here is a capital claim.

Files: `.console.txt` (full log), `.books.csv` (39 arms + comparands, turnover, `c_star`, `D_star`,
`c_hat` on all three windows), `.grid.csv` (80 cost cells + the full cost-ladder Sharpe sweep),
`.cluster.csv` (cluster CIs), `.ladders.csv` (cost and drag ladders, every rung, every window),
`.walkforward.csv` (rule 8 on the books), `.walkforward_claim.csv` (rule 8 on the claim, 20 cells).
RULES.md, PROTOCOL.md, research/scan.py, products/bot/bot.py and research/baseline.py untouched.
