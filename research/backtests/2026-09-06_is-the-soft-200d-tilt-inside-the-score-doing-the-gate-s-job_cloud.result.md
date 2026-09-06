# Idea 289 — is-the-soft-200d-tilt-inside-the-score-doing-the-gate-s-job

**Run:** cloud, 2026-09-06. Script `2026-09-06_is-the-soft-200d-tilt-inside-the-score-doing-the-gate-s-job_cloud.py`.
**Verdict: ANSWERED — the tilt IS the gate (exactly, at t=1), and NEITHER form is load-bearing.
KILL of both the soft trend tilt and the hard 200d gate as RETURN instruments on the large-cap
panels; the entire eligibility effect idea 56 measured is the `vol20 < 0.60` clause. No RULES
change, no KEEP; `RULES.md`, `scan.py`, `bot.py` and `baseline.py` untouched.**

## What was swept

`s(t) = comp * (1 - t + t*above200)` — t=0.00 no trend information, **t=0.50 the live scan.py
form**, t=1.00 a hard multiplicative gate. Tuned: t ∈ {0.00, 0.25, 0.50, 0.75, 1.00} × n ∈ {5,10,20}
(2 parameters, PROTOCOL rule 4). Reported never-selected axes: universe (U56, B136) × convention
(dg de-gross to cash, rw re-spread 75%) × hard gate (OFF / **MA** = the 200d gate alone / V1 =
RULES v1's full `above200 & vol20<0.60`). **180 cells, all printed** (`.grid.csv`). Construction
fixed at idea 2's: rank composite, no vol scaler, top-n EW at 75% gross, weekly, 10 bps, t+1
execution. The MA level is the correction that makes the question answerable — pricing OFF against
V1 attributes the vol clause's damage to the 200d gate.

## The three answers

**1. At t=1.00 the tilt reproduces the hard gate BIT-IDENTICALLY.** Selections differ on **0 of
4439 days** in all 6 (universe, n) cells, and every MA−OFF metric delta at t=1 is exactly +0.000.
The tie-handling loophole (below-MA names all score 0 and could enter when fewer than n names are
above their average) never binds, even though the MA gate is short of n names on 0.06/0.14/0.76 of
days at n=5/10/20 on U56. Idea 56's "bit-identical" claim is confirmed and now has its mechanism.

**2. At the LIVE t=0.50 the hard gate is nearly inert, and inert BECAUSE of the tilt.** Selections
differ on **0.05% / 2.2% / 9.9%** of days (U56 n=5/10/20) and **0.0% / 0.4% / 1.8%** (B136), and
the mean count of below-MA names held with no gate at all falls from 0.021→0.000 (n=5),
0.162→0.057 (n=10), 0.907→0.670 (n=20) as t goes 0→0.5. Idea 56's "the 200d clause is INERT"
reading is correct, and the reason is the tilt, not the irrelevance of trend.

**3. Neither form is load-bearing on RETURN; the vol clause is the whole effect.**

| contrast | dSharpe range over its cells | mean |
|---|---|---|
| tilt t>0 vs t=0 (gate OFF), 48 cells | −0.0494 .. +0.0164 | **−0.0046** |
| hard MA200 gate vs no gate, 60 cells | −0.0494 .. +0.0164 | **−0.0063** |
| RULES v1 full filter vs no gate, 60 cells | −0.2147 .. **−0.0232** | **−0.1070** |

The V1 filter costs **−1.62 to −7.41 pp/yr of CAGR (mean −3.81)** in 60 of 60 cells and buys
+0.94 to +7.60 pp of drawdown. The tilt and the 200d gate are the same instrument and it is worth
roughly nothing either way; the destruction is entirely the vol clause, reproducing idea 56.

Headline cell (U56, dg, t=0.50, n=20): OFF 15.40%/1.177/−21.27%, MA 14.40%/1.158/−19.09%,
V1 12.74%/1.098/−18.15%. The trend information buys ~2.2 pp of drawdown for ~1.0 pp of CAGR; the
vol clause buys a further 0.9 pp of drawdown for 1.7 pp of CAGR.

## Rule 8 walk-forward (12 cells; (t, n) chosen on ≤2016 by IS Sharpe, 2017–2026 read once)

The IS chooser **never picks the live t=0.50** — picks are t=0.00 (9 of 12) and t=0.25 (3 of 12) —
and it **loses to the pre-registered anchor (t=0.50, n=20) in 12 of 12 cells**: mean OOS Sharpe
**0.9539 vs 1.0389 (−0.0850)**, mean regret vs the best OOS cell 0.0867. This is another instance
of the record's do-nothing streak: fitting the tilt on the first half is worse than leaving it at
the live value. SPY OOS Sharpe 0.882 on both panels; RULES v2 OOS 1.294 (U56) / 1.121 (B136).

## KEEP paths

**4a: 0 / 180.** Nothing beats RULES v2 in both halves with no worse drawdown.
**4b: 16 / 180, every one on U56, none on B136 (0/90).** First failing bar over the 180: DD 94,
H2 50, H1 20. All 16 passers are n=20; 5 of them are U56/MA/dg at *every* tilt (identical book:
14.40%/1.158/−19.09%, H1/H2 1.222/1.118, OOS 15.85%/1.181/−19.09%), which beats idea 2's V1-gated
candidate on CAGR (+1.66 pp) and Sharpe (+0.060) for 0.94 pp more drawdown.

**That passer is NOT proposed.** It fails on two counts: (i) it is U56-only — 0/90 on B136, the
same list-specificity idea 53 found for idea 2's candidate; (ii) it is **not reachable by the
pre-registered selector** — inside U56/MA/dg rule 8 picks (t=0.00, n=5) and lands at OOS 1.044,
0.137 of Sharpe short of it. A cell that only a hindsight chooser finds is not a candidate.

## Caveats

B136 is current-constituent (survivorship, PROTOCOL rule 9). U56 excludes BTC/ETH. All numbers at
10 bps per unit turnover with t+1 execution; costs were not swept here.
