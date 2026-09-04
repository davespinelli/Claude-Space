# Idea 85 — exit-schedule-vs-entry-schedule (cloud, 2026-09-04)

**Verdict: idea 83's mechanism claim is HALF WRONG, and the remedy it implies works exactly
where the claim is true and nowhere else. PARK for the entry-only budget on the *unranked*
book; KILL on the ranked one.** No new KEEP: no arm passes 4b on both universes at a common
budget.

Script `2026-09-04_exit-schedule-vs-entry-schedule_cloud.py` · console `…console.txt` ·
grid `…grid.csv`. 44 arms + a 16-point gross ladder, **all reported**; 2 tuned parameters
(budget B, mode); weekly, t+1, 10 bps (25 bps also reported), long-only. Harness sanity
before any new number: idea 2's `CAND20` **12.7%/1.093/−18.3%, halves 1.088/1.103** and idea
10/72's `B136/EWall` **10.7%/1.027/−17.7%, halves 1.146/0.917** reproduce exactly.

## (1) The decomposition — "turnover is mostly the gate's exits" is true only unranked

The entry/exit split is **50.0–50.1% / 49.9–50.0% on all four books**, as a self-financing
long-only book that resets to a fixed gross must be. The informative number is what the exit
leg is *made of*:

| book | gate exits | rank displacement | drift trims |
|---|---|---|---|
| u56 `CAND20` | 24.8% | **67.8%** | 7.4% |
| broad `CAND20` | 11.1% | **82.7%** | 6.1% |
| u56 `EWall` | **56.6%** | 0.0% | 43.4% |
| broad `EWall` | **57.0%** | 0.0% | 43.0% |

On the ranked book — the one idea 83's budget was tested on, and the standing 4b candidate —
**8 of every 9 dollars of selling on the broad list is rank rotation, not the 200d gate.**
Idea 83's explanation of its own KILL is therefore wrong for that book and right for `EWall`.

## (2) The remedy — cheap drawdown insurance, on the unranked book only

Honour every exit, cap the buy leg at B per rebalance (unspent proceeds sit in cash):

| arm | turn | gross | CAGR | Sharpe | MaxDD | ΔSharpe | pp CAGR per pp MaxDD |
|---|---|---|---|---|---|---|---|
| u56 `EWall` control | 8.2× | 0.750 | 10.4% | 1.050 | −15.9% | — | lever **−0.68** |
| u56 `EWall` B=0.10 | 6.3× | 0.709 | 10.0% | **1.100** | **−12.9%** | +0.050 | **−0.14** |
| broad `EWall` control | 8.3× | 0.750 | 10.7% | 1.027 | −17.7% | — | lever **−0.64** |
| broad `EWall` B=0.20 | 7.8× | 0.742 | 10.9% | **1.077** | **−16.4%** | +0.050 | **−0.01** |
| u56 `CAND20` B=0.10 | 8.5× | 0.683 | 12.2% | 1.098 | −16.7% | +0.005 | −0.30 |
| broad `CAND20` B=0.10 | 10.1× | 0.633 | 11.2% | 0.942 | −18.2% | −0.016 | −1.00 |

On `EWall` the instrument buys drawdown at **−0.01 to −0.14 pp of CAGR per pp of MaxDD**
against the gross lever's **−0.63 to −0.73** measured on the same days — 5× to 60× cheaper —
and it is not the lever in disguise: at u56 B=0.10 gross falls only 5.5%, which at the
lever's rate would buy 0.9pp of drawdown, and the observed improvement is **3.0pp**. It also
improves with cost (u56 `EWall` Sharpe at 25 bps: 0.925 control → 1.012 at B=0.05). On
`CAND20` there is nothing: ΔSharpe is +0.001..+0.007 on u56 until the budget starts
de-grossing, and **negative at every budget on broad** (−0.002..−0.016, t −1.08..−3.68);
its exchange rate converges on the lever's own (−0.68 at B=0.05, lever −0.72).

## (3) Idea 83's total budget reproduces, sign and size

Pro-rata truncation of the whole delta vector leaves gross untouched (0.739–0.750 at every
B), cuts turnover up to 70%, and **deepens MaxDD in 19 of 20 arms** (mean **−3.0pp**, range
+0.1 to −5.3pp) — idea 83's −2.4pp, confirmed on four books. Its ΔSharpe is positive but
never significant (t +0.17..+1.89), exactly as idea 83 reported.

## (4) Why it is a PARK and not a KEEP

* **No cross-universe 4b pass at a common B.** broad `EWall` B=0.20 turns the control's OOS
  4b CAGR miss into a **PASS** (full-sample 4b PASS, OOS 4b PASS); the same B on u56 `EWall`
  still fails 4b's CAGR floor, as its control does. Across all 44 arms: 4b full 16/44, 4b OOS
  24/44, 4a 17/44 (the 4a passes are broad, where v1 itself draws down −21.2%).
* **Rule 8 picks the wrong end of the grid**, and it is a textbook idea-88 case: on u56
  `EWall` in-sample Sharpe is monotone **down** in the budget (0.970 → 0.934) while OOS
  Sharpe is monotone **up** (1.114 → 1.224), so R0 selects the weakest arm B=0.30 (OOS 1.124
  against the grid's 1.224) and R2 is infeasible. On broad `EWall` R0 picks B=0.20 (OOS
  1.097 vs best 1.113) — the instrument is only half-selectable, and its IS Sharpe spread is
  0.036, just above idea 88's 0.02 floor.
* **The paired return t-test has no power here** and should not be read as evidence against:
  the effect is entirely in drawdown and vol, not in mean return (CAGR moves −0.4pp/+0.2pp),
  so t −0.23..+0.58 at the favourable arms is what a pure risk instrument looks like.

**Survivorship:** both lists are current constituents; absolute CAGRs are optimistic. Every
arm shares the panel and the days, so the control-vs-arm comparisons are far less exposed
than the levels. **Rules unchanged.** For the Sunday review: if a turnover instrument is ever
adopted, it must be an **entry-only** one and only on an **unranked** book — the ranked book's
selling is rank rotation, and constraining it either does nothing or de-grosses.
