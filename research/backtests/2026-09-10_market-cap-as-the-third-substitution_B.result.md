# Idea 195 — market-cap-as-the-third-substitution (lane B, 2026-09-10)

**Verdict: SPLIT — the PARK is LIFTED (it was a search error), leg (c) RUNS, and leg (c) is KILLED
as an edge.** No KEEP, no book promoted, no RULES change. `RULES.md`, `PROTOCOL.md`, `scan.py`,
`bot.py` and `baseline.py` untouched.

## 1. The PARK was wrong, and it was wrong for a checkable reason
Idea 193 (2026-09-05) parked leg (c) for want of a shares-outstanding series; a 2026-09-08 lane-B
pass re-affirmed the PARK. **Both searched `data/` only.** The series is in the repo, written by the
filings job rather than the price job: `research/deepvalue/universe_under2b.csv` carries `shares`
and `mktcap` for **716 tickers, covering 430 of the 439 SMALL panel names (97.9%)**. The nine
uncovered names (ALOT, ICHR, III, OLN, PCYO, PLPC, SPWR, TH, TYGO) are dropped, giving SMALL430.

It is runnable in **one form only**, and naming that form is half the answer. The file is a
**snapshot** — one share count, dated today, per name. There is no shares *time series* anywhere in
the repo. So the only market cap constructible offline is

    MCAP_t = px_t * s_T

which by idea 193's own identity is the true cap times **two terminal-known per-name constants**:
`s_T / s_t` (sixteen years of buybacks and dilution) and the panel's dividend-adjustment factor.
**Leg (c) is a leaking key by construction, strictly leakier than PRICE.** Caching a shares
*snapshot* does not unblock the leg in an implementable form; only a shares *history* would.

Idea 565's pinning convention is honoured: the snapshot is committed as `.shares.csv`, because
`universe_under2b.csv` is rewritten nightly and this run is otherwise irreproducible tomorrow.

## 2. Gates (four, all pre-registered, all PASS)
| gate | result |
|---|---|
| G1 `fast_backtest` == `engine.backtest`, control book | **2.776e-17** |
| G4 rung identity `r(c) = r(0) − turnover·c/1e4` vs a live 25 bps engine run | **2.776e-17** |
| G3 snapshot self-consistency `mktcap == price * shares` | **4.367e-16** |
| G2 idea 185's committed small-panel rows (6 keys x 2 dirs x 3 m x 2 rungs) | **72 of 72 at max 5.721e-08** (pre-stated tol 5e-3) |

G2 is the one that matters for comparability: leg (c) is being added to the *same* table, on idea
185's exact 439+SPY panel and construction, before the leg-(c) panel is cut.

## 3. The substitution table (SMALL430, mean NEG dSharpe vs the untilted control, 10 bps)
Two tuned parameters — KEY and tilt strength m ∈ {0.20, 0.50, 1.00} — and **all 193 arms x 3 rungs
are in `.arms.csv`**. Null band = q95 of |dSharpe| over 20 random-walk keys = **0.1796**.

| key | class | mean NEG dSharpe | \|IC vs realised fwd return\| |
|---|---|---|---|
| DVOL | levelproduct | +0.6222 | 0.5998 |
| **MCAP** | **leg (c)** | **+0.6181** | **0.6959** |
| PRICE | pricelevel | +0.4659 | 0.4234 |
| MCAPREB | leg (c) | +0.3555 | 0.4389 |
| VOLSH | levelproduct | +0.3433 | 0.4183 |
| SHARES | leg (c) | +0.2495 | 0.3290 |
| REBASED | leakfree | +0.2407 | 0.1972 |
| MCAPFRZ | leg (c) | +0.2163 | 0.3995 |
| FROZEN | pricelevel | +0.1728 | 0.2247 |
| DDTR | leakfree | **−0.0356** | 0.0780 |

Headline arm: **MCAP/NEG/m=1.00 @10bps — CAGR 20.29%, Sharpe 1.374, MaxDD −24.87%, halves
1.148 / 1.570**, against the untilted control 6.12% / 0.438 / −25.90% (0.628 / 0.281), RULES v2
3.77% / 0.565 / −14.58%, RULES v1 7.41% / 0.554 / −34.92% and SPY 14.13% / 0.862 / −33.72%
(0.891 / 0.858). Turnover 17.53x/yr.

## 4. Why that number is not an edge
**Idea 185's leak law is confirmed and leg (c) lands on it as the leakiest real key in the record.**
Spearman(|IC|, mean NEG dSharpe) = **+0.943** over the record's six keys and **+0.915** with leg
(c)'s four added (idea 185 published +0.881). MCAP outranks PRICE on *both* axes, exactly as the law
predicts for a key that multiplies the price panel by a terminal-dated constant.

**The decomposition says it is a blend, and that both halves leak.** SHARES alone carries **0.404**
of MCAP's tilt; cross-sectionally rho(MCAP, PRICE) = +0.556, rho(MCAP, SHARES) = +0.507,
rho(SHARES, PRICE) = **−0.363**, rho(MCAP, DVOL) = +0.820. Size is genuinely a second axis — but a
terminal-dated share count is itself look-ahead (|IC| 0.3290), so separating the axes does not
separate out a causal signal.

**The placebo halves it again.** `MCAP = PRICE ∘ diag(s)` is exactly idea 197's `px → px·diag(c)`
operator, so the size information has an exact placebo: permute the share counts across names,
keeping the multiplier distribution and destroying the name↔shares link. Over 20 permutations at
10 bps the placebo reproduces **52.2%** of leg (c)'s tilt (+0.3226 of +0.6181), and at m=0.20 the
real key sits **inside** the placebo band (+0.3247 vs a placebo max of +0.3450). A *random* rescale
of the price panel buys most of what "market cap" buys.

## 5. PROTOCOL 4 and PROTOCOL 8
**4a 0/193, 4b 0/193, BOTH 0/193 — at 0, 10 and 25 bps.** The binding leg is the drawdown cap and
nothing else: `MaxDD < 0.60x SPY (−20.23%)` fails **193 of 193**, against H1 189, OOS 176, H2 175,
CAGR 168. **The pure oracle key FWDRET — the rank of the realised forward total return — passes 4b
on 0 of its 6 arms.** On a 20-name small-cap book, 4b's verdict is a verdict on the book's
concentration, not on the tilt (ideas 411 / 527 / 531 again).

**Rule 8 fails to protect, and that is the run's sharpest result.** With (KEY, m) chosen on
2010–2016 IS Sharpe alone and 2017–2026 read once, MCAP/NEG/m=1.00 is the pick at all three rungs
and beats *everything* out of sample: **OOS 26.31% / 1.584 / −24.87%** vs RULES v2 3.77% / 0.558 /
−14.58%, RULES v1 6.66% / 0.499 / −34.92%, the untilted control 6.23% / 0.434 / −25.90% and SPY
15.45% / 0.882 / −33.72%. A key whose |IC| with the realised forward return is 0.6959 *should* win a
walk-forward, because the OOS window sits inside its lookahead. **PROTOCOL 8 splits the sample by
date; it does not detect a key that is terminal-dated rather than window-dated.** The T1 family
(ideas 197 / 426 / 428 / 433) is the instrument that catches this, and it should run *before* rule 8,
not after.

## 6. Pre-registered predictions, scored
P1 gates PASS · P2 HIT (MCAP/NEG +0.6181 vs band 0.1796) · P3 HIT (|IC| 0.6959 > 0.4234 and
dS +0.6181 > +0.4659) · P4 HIT (SHARES 0.404 of MCAP) · P5 HIT (rho +0.915 ≥ +0.70) ·
**P6 MISS** — BOTH = 0 as predicted, but the LEGC rule-8 pick *does* beat RULES v2 OOS. The miss is
reported as the finding in §5.

## 7. Survivorship, stated as PROTOCOL 9 requires
Worse than usual here: the SMALL panel is current constituents of a sub-$2B screen
(`data/SMALL_PANEL_README.md`), and the shares snapshot exists only for names that still file today,
so SMALL430 is a survivor of a survivor. Every number above is biased in the tilt's favour.

## 8. What the record should take from this
1. **Leg (c) is closed as an edge and open as a data question.** The queue asked for a shares
   series; a shares *snapshot* answers the substitution but cannot make it implementable. Re-park
   the *implementable* form ("MCAP with a shares time series") explicitly, so it is not confused
   with the leg run here.
2. **A PARK justified by "no data in `data/`" needs to name the directories it searched.** This one
   was re-affirmed once on the same too-narrow search.
3. **Rule 8 is not a leak detector.** Any key built from a terminal-dated quantity walks forward.

Follow-ups filed: 622 (census the record's PARKs for the same search error), 623 (a T1-style
terminal-dating certificate as a pre-rule-8 gate).

Script: `research/backtests/2026-09-10_market-cap-as-the-third-substitution_B.py`
Artefacts: `.console.txt`, `.arms.csv` (579 rows), `.keyic.csv`, `.placebo.csv`, `.walkforward.csv`,
`.reproduction.csv`, `.shares.csv` (the pinned snapshot).
