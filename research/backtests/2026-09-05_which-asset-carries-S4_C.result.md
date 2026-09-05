# Idea 102 — which-asset-carries-S4 (lane C, 2026-09-05) — **KILL of the TLT hypothesis / PARK on the pruned sleeve**

**Script:** `research/backtests/2026-09-05_which-asset-carries-S4_C.py`
**Artefacts:** `.console.txt`, `.grid.csv`, `.standalone.csv`, `.correlation.csv`, `.deletion.csv`,
`.regime.csv`, `.attribution.csv`, `.walkforward.csv`, `.costladder.csv`, memo `.memo.md`

## What was run

240 grid points, all reported: 6 sleeve compositions × 5 fractions f ∈ {0, 0.25, 0.50, 0.75, 1.00}
× 2 books (`top20`, `ewall`) × 2 universes (u56, broad) × 2 gross conventions (natural, g=1.00).
**Tuned parameters: exactly 2** — sleeve composition and f. Books, universes, conventions and the
5/10/15/20/25 bps cost ladder are reported controls, never selected on. `S4` is the control arm and
reproduces idea 100 exactly (u56 `top20 + 50% S4` at g=1.00: 11.8%/1.149/−14.2%, OOS 1.236).

The engine applies costs as `gross − turnover × bps/1e4` with a bps-independent holdings path, so
each weight matrix is run once at 0 bps and every rung of the ladder derived exactly; asserted
against a direct 10 bps run at start-up (max error 0.0).

## Results

**(1) The sleeve is not TLT. TLT is a passenger.** Run alone as the whole sleeve, TLT is
0.7% CAGR / **0.114** Sharpe / **−30.7%** MaxDD against S4's 2.6% / 0.616 / −8.7%; in the
rising-rate regime it is **−4.8% CAGR / −0.802 Sharpe**. As an overlay at the pre-registered
f = 0.50, `TLTonly` has a **negative** dSharpe against the bare book in **8 of 8** cells
(mean **−0.118**) and passes 4b in **0 of 48** points. Deleting TLT from S4 costs almost nothing:
`noTLT` retains **81–103%** of S4's dSharpe (mean +0.109 vs S4's +0.122), is positive in 8/8, and
is the **only** variant whose cross-universe 4b pass survives to 20 bps in any cell.

**(2) The load-bearing asset is GLD, and DBC is a drag.** Deleting gold is what breaks the sleeve —
`noGLD` retains only **25–54%** of S4's dSharpe (mean +0.049) and is the first variant to lose the
cross-universe 4b pass on the cost ladder (dead by 15 bps where S4 and `noTLT` hold). Deleting DBC
**improves** the sleeve in **8 of 8** cells (retention 1.08–1.54×, mean dSharpe **+0.163**, the
highest of the six). Full-sample additive attribution inside S4: GLD **+33.2pp** of the sleeve's
+62.1pp total (53%), UUP +12.9, DBC +10.4, **TLT +5.6 (9.1%)**.

**(3) The queue's 2022 premise is factually wrong, in the direction that helps.** The duration vote
was indeed flat: mean 0.09, **187 of 251 days at zero**. But TLT's 2022 contribution was
**−1.86%**, not positive — the sleeve's +4.34% in 2022 came from **UUP +4.81%** and **DBC +2.28%**.
2022 was a dollar/commodity year for this sleeve, not a duration year, so the falling-rate sample
is not what is holding idea 100's result up.

**(4) The regime split says the same thing louder.** dSharpe vs the bare book, mean over the 8
cells: falling-rate 2009-2021 — S4 +0.079, `noTLT` +0.010, `TLTonly` +0.058; rising-rate 2022-2026 —
S4 +0.249, **`noTLT` +0.418**, **`TLTonly` −0.548**. Dropping TLT is worth *more* in the regime the
queue was worried about, which is the opposite of a duration artefact.

**(5) Rule 8 (2009-2016 IS → 2017-2026 OOS, joint over sleeve × f).** The walk-forward picks
`noDBC` at f = 0.50 in **6 of 8** cells and `TLTonly` at f = 0.25 in the other 2; it never picks S4
and never picks f = 0. The picks beat SPY's OOS Sharpe **8/8** (0.882), beat RULES v1 **8/8**
(0.747 u56 / 0.576 broad) and beat their own no-sleeve anchor **6/8**; mean regret −0.134. The two
cells where IS selection reached for TLT are the run's **two worst regrets** (−0.223, −0.262) —
in-sample duration is a trap that rule 8 priced.

**(6) The best book this run produced: `top20 + 50% (TLT,GLD,UUP)` at g = 1.00** (i.e. S4 with DBC
deleted), the rule-8 pick in 6/8 cells:

| | CAGR | Sharpe | MaxDD | H1 / H2 | OOS CAGR/Sharpe/MaxDD | Turn/yr | 4a | 4b |
|---|---|---|---|---|---|---|---|---|
| u56 | 11.5% | **1.167** | **−13.3%** | 1.169 / 1.167 | 12.3% / 1.215 / −13.3% | 12.4× | ✅ | ✅ |
| broad | 12.0% | 1.073 | −14.6% | 1.245 / 0.917 | 11.1% / 0.985 / −14.6% | 15.2× | ✅ | ✅ |
| *SPY* | 15.2% | 0.889 | −33.7% | 0.957 / 0.834 | 15.5% / 0.882 / −33.7% | — | | |
| *RULES v1* | 6.5% / 6.4% | 0.664 / 0.635 | −13.8% / −21.2% | 0.641/0.688, 0.756/0.532 | 0.747 / 0.576 | — | | |

It clears 4a **8/8 cells** (both books × conventions × universes) and holds cross-universe 4b to
**15 bps**. It beats the S4 control on Sharpe and MaxDD in 8/8 cells at strictly lower turnover.

## Verdict

**KILL** the "S4 is a falling-rate duration bet" hypothesis — decisively, on five independent
measures. **PARK** the pruned sleeve. `top20 + 50% (TLT,GLD,UUP)` at g=1.00 is the strongest book
the project has on Sharpe-and-drawdown terms, but it inherits idea 100's un-pre-registered gross
dial *and* adds a composition chosen across six variants; adopting it off this run would be exactly
the "tune until it works" that PROTOCOL rule 7 forbids. Proposed RULES wording is in `.memo.md`,
explicitly marked **not adoptable this week**. Rules unchanged.

Follow-ups queued: **104** (fold the drop-DBC composition into idea 101's pre-registered fixed-g
run rather than running a third one), **105** (is it gold or is it any non-dollar real asset — GLD
alone, GLD+UUP, and GLD swapped for SLV/IAU), **106** (DBC is a drag in 8/8 cells at f=0.50 —
check whether that is the 2009-2013 contango era or the whole sample before pruning it for good).

## Caveats

- SURVIVORSHIP: both equity panels are current constituents; equity levels biased upward. The
  sleeve's assets are ETFs and are not exposed.
- **GLD carries its own regime problem, one this run does not solve.** Gold's +33.2pp is
  concentrated in 2010-11, 2019-20 and 2024-25; a sleeve whose edge is gold is a bet that the
  2009-2026 gold sample is representative, which is a strictly weaker claim than "multi-asset
  diversification". Idea 105 exists to test whether the exposure generalises.
- The rising-rate regime is **4.7 years**, of which 2022 is one. Every `dS_rise` number here rests
  on a short window; the sign is consistent across 8 cells but the magnitudes are not tradeable.
- `noDBC` beating S4 in 8/8 is a 6-way selection. Rule 8 independently reaching the same
  composition in 6/8 cells is supporting evidence, not a pre-registration.
- Queue idea 38 (calendar-day index) applies: post-2014 weekends are zero-return rows, hitting
  every arm, baseline and SPY identically. Cross-arm comparisons are apples-to-apples; absolute
  Sharpe levels wait on idea 38.
