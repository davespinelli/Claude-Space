# Idea 1317 (lane C, 2026-09-18) — can a RESIDUAL-TARGETED SCREEN reach an IDIOSYNCRATIC drawdown where a VOL SCREEN cannot?

**VERDICT: KILL.** The hypothesis is refuted on its own terms and on both of its clauses.
No RULES change, no PROTOCOL edit (rule 6). RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py untouched. Offline, deterministic, 14 of 14 gates, 13.1s, 57 real books.

## What was run
The incumbent's only risk screen is `vol20 < 0.60`, a TOTAL-vol bar. Idea 1301 found SMALL's
worst episode is **21.2% systematic / 78.8% residual** and that the residual stream's
standalone MaxDD (-44.68%) is nearly twice beta*SPY's (-23.18%), so the queue's hypothesis was
that a screen pricing IDIOSYNCRATIC risk is the one that moves the 4b drawdown leg. The screen
was replaced with `RESID_VOL = sd(r - beta*SPY)` over a trailing window (beta by OLS on that
same window; `resid_var = var(r) - cov(r,spy)^2/var(spy)`, verified against a direct
`np.polyfit` residual to 5.6e-17, gate G6).

Two dials, all 9 grid points published on all three panels: **WINDOW {63, 126, 252} x
RESID_MAX {0.5, 0.7, 0.9}**. Everything else is the frozen incumbent (N=15, H=126, gross 0.60,
weekly, 10 bps, decide-at-t / apply-at-t+1, warm-up 260).

**The control arm, which is the point.** Every RESID cell is run beside a TOTAL cell ranking
total vol over the SAME window at the SAME percentile, built as "admit the k lowest,
k = floor(p * n_candidates(t))" over the above-200d priced measurable set, so the two arms
admit **exactly the same number of names on every single day** (gate G1, max |difference| = 0
over 27 cells x ~4,200 days). The only thing that differs between the two books is WHICH
names. A `pct_rank <= p` BAR does not do this — resid_var is clipped at zero and ties at the
floor differ between the two statistics, admitting up to **18** more eligible names on one arm
than the other; that first-pass defect is why the screen is written in the count form.

## Finding 1 — the residual screen does NOT reach the cap (the queue's question, answered NO)
SMALL663, 9 RESID cells at the frozen gross: MaxDD **-31.52% .. -24.50%** against a **-20.23%**
cap. **0 of 9 clear the cap. 0 of 9 clear the cap AND the 9.84% CAGR floor.** The shallowest
cell (w=126, p=0.5) misses the cap by **4.27 pp** and earns 6.19% against the 9.84% floor.
For comparison on the same leg: 1301's best SELECTION cell -28.69%, 1297's best EXPOSURE cell
-22.43%. The residual screen is the best of the three instruments on drawdown alone and still
short, and it buys nothing the CAGR floor can pay for.

## Finding 2 — at MATCHED admission the residual screen is indistinguishable from the total-vol one
Pooled over 27 matched pairs (3 panels x 9 cells): RESID is shallower than TOTAL in **14 of
27**, median dMaxDD **+0.000 pp**, mean **-0.158 pp**, **paired t = -0.62**. Per panel the
median dMaxDD is U56 -0.44 pp, B136 +0.21 pp, SMALL663 -0.62 pp — no consistent sign. RESID
has the higher Sharpe in 10 of 27 (median dSharpe -0.0152) and the higher OOS Sharpe in 12 of
27. **The statistic that prices idiosyncratic risk is not the one that moves the leg.**

## Finding 3 — the mechanism, which explains Finding 2: both screens are DE-BETAERS
On SMALL the RESID screen does cut the incumbent's drawdown by **+8.85 pp** (-33.35% ->
-24.50%), but the exact additive split of each book's own worst episode shows how: beta falls
**0.658 -> 0.528** and the episode flips from **21.2% systematic / 78.8% residual** to
**72.4% / 27.6%**, while the residual stream's standalone MaxDD only falls -44.68% -> -37.23%.
The TOTAL control does the same thing (beta 0.506, 69.5% / 30.5%, residual stream -35.41%) —
slightly better on the residual stream than the "residual-targeted" screen. Low residual vol
and low total vol select nearly the same defensive names, so both instruments act on the
systematic part, which is exactly the part 1301 showed is not SMALL's binder.

## Finding 4 — on the large panels the swap is strictly worse than the incumbent
U56: incumbent 13.66% / 1.1706 / -16.38% (4b full AND OOS pass). Best RESID cell by Sharpe
10.55% / 1.0021 / -15.79% — **-3.10 pp of CAGR and -0.1684 of Sharpe**; **0 of 9 RESID cells
pass 4b full, 0 of 9 pass 4b BOTH.** B136: incumbent 13.48% / 1.0670 / -15.97% (4b BOTH pass);
best RESID 9.67% / 0.9822 / -17.43%, **-3.81 pp / -0.0848**; 0 of 9 pass 4b full or BOTH.
**4a is 0 of 57 books** — RULES v2's -12.05% MaxDD at 1.20 Sharpe keeps path 4a out of reach
for any growth book, as the record has found repeatedly.

## Rule 8 (2017-2026 read ONCE), run for BOTH arms on all three panels
(WINDOW, RESID_MAX) by argmax IS Sharpe on warm-up..2016-12-31.

| panel | arm | pick | OOS CAGR / Sharpe / MaxDD | vs FROZEN anchor | 4b BOTH |
|---|---|---|---|---|---|
| U56 | RESID | w=252 p=0.9 | 11.13% / 0.9808 / -15.92% | **-0.2139** | no |
| U56 | TOTAL | w=252 p=0.9 | 11.68% / 1.0578 / -16.23% | -0.1369 | yes |
| B136 | RESID | w=252 p=0.9 | 11.11% / 0.9006 / -19.44% | **-0.1448** | no |
| B136 | TOTAL | w=252 p=0.9 | 10.52% / 0.8982 / -19.64% | -0.1472 | no |
| SMALL663 | RESID | w=63 p=0.5 | 3.87% / 0.3506 / -26.09% | **-0.1147** | no |
| SMALL663 | TOTAL | w=63 p=0.5 | 4.43% / 0.3941 / -25.11% | -0.0712 | no |

OOS SPY 15.28% / 0.8747 / -33.72% (U56) and 15.33% / 0.8769 / -33.72% (B136, SMALL663); OOS
RULES v2 9.47% / 1.2781 / -12.05%, 7.88% / 1.1061 / -12.24%, 4.47% / 0.6518 / -12.18%. **Every
rule-8 pick, in both arms and on all three panels, lands BELOW the frozen incumbent anchor
out of sample.** The single 4b-BOTH pass among the 54 screen-swap books is the TOTAL control
on U56, not the residual screen it was built to control for — and it still gives up 2.18 pp of
CAGR and 0.056 of Sharpe against the frozen incumbent, so it is not a candidate either.

## KEEP-4b re-confirmation (not a new claim)
The frozen incumbent re-confirms KEEP-4b on U56 (13.66% / 1.1706 / -16.38%, full sample AND
rule-8 OOS 15.12% / 1.1947 / -16.38%) and on B136 (13.48% / 1.0670 / -15.97%, OOS 14.11% /
1.0454 / -15.97%), and fails on SMALL663 as the record says. Replay gates G2/G3 match
1215/1297/1301's committed numbers to 3.3e-05 and 5.0e-05.

## NOT CLAIMED
That residual risk is irrelevant to SMALL's drawdown (1301's decomposition stands; what is
killed is that a residual-vol SCREEN is the instrument that reaches it); that some other
residual construction — a multi-factor residual, a downside-only residual, a shorter or
event-triggered window — must fail; that any cell here is a new candidate book; that anything
in RULES.md changes (rule 6).

## SURVIVORSHIP (rule 9)
Current constituents only on all three panels; SMALL additionally drops 52 tickers with
max_1d_move >= 1.0 from data/small_meta.csv, leaving 663. The bias is worst on SMALL and
flatters every absolute level and the drawdown leg specifically, so the SMALL KILL is the
STRONGER reading, not the weaker one. The RESID-vs-TOTAL difference is read on the SAME names
and days under a matched admission count, so a common level bias moves both arms together and
cannot manufacture the null result in Finding 2.

Script: `research/backtests/2026-09-18_can-a-RESIDUAL-TARGETED-SCREEN-reach-an-IDIOSYNCRATIC-drawdown_C.py`
Artifacts: `.grid.csv` (57 books), `.headtohead.csv` (27 matched pairs), `.admissions.csv`,
`.decomp.csv`, `.walkforward.csv`, `.gates.csv`, `.console.txt`
