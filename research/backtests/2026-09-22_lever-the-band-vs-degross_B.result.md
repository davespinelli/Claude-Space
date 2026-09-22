# Idea 2085 (lane B, 2026-09-22) — does LEVERAGE clear the 4b CAGR floor where DE-GROSS cannot?

**VERDICT: KILL for a rules change. Leverage is Sharpe-neutral, so it cannot lift the 4b
margin; it trades CAGR for MaxDD ~1:1 and the 4b DD cap binds at gross ~1.25–1.5, before
leverage buys anything the CAGR floor needs — the floor is already cleared at unlevered
gross 1.00. No new KEEP.**

## Grounding (CHANGELOG diagnosis)
The standing 4b candidate's SOLE binding leg is the CAGR floor (>=70% of SPY's CAGR), and
every drawdown-buying device the record has priced is beaten at matched exposure by a plain
DE-GROSS — i.e. every device REMOVES exposure. LEVERAGE (gross>1.0) is the one direction the
record had never priced, and the one that lifts CAGR directly. This run prices it.

## Design
Book = live band book `baseline.rules_v2_weights(px, band, gross)`, gross allowed above 1.0
(leverage stated, PROTOCOL rule 2). Two tuned params: BAND c in {0.03, 0.08}, GROSS in
{0.75, 1.00, 1.25, 1.50, 1.75, 2.00}. All 12 cells x 2 panels (U56, B136) reported. Weekly,
t+1, 10 bps headline; costs {0,10,25,50} bps and financing {0,3,6}%/yr on borrowed gross
reported, tuned nowhere. Rule-8 walk-forward: choose on 2009-2016 only by the memo's
pre-stated 4b IS screen (max IS Sharpe among IS-4b-legal cells), read 2017-2026 once.

## Result — leverage is motion along a fixed Sharpe ray
Sharpe is **constant to 3 dp across the entire gross ladder** (U56 band 0.03: 1.201 at every
gross 0.75->2.00; band 0.08: 1.144/1.145; B136: 1.097 / 1.115). Leverage scales CAGR and MaxDD
together and leaves risk-adjusted return unchanged, so it cannot improve any 4b margin.

U56, band 0.03, 10 bps (CAGR / MaxDD; 4b bars CAGR>=10.60%, MaxDD>=-20.23%):
- gross 0.75: 8.62% / -12.05% — fails 4b (CAGR floor)
- gross 1.00: 11.53% / -15.91% — **passes 4b**
- gross 1.25: 14.46% / -19.69% — **passes 4b**
- gross 1.50: 17.39% / -23.38% — fails 4b (DD cap)
- gross 1.75/2.00: fail (DD cap)

The CAGR floor is already cleared at UNLEVERED gross 1.00; the DD cap breaks at gross ~1.25–1.5.
So leverage never operates in the regime the diagnosis pointed at (it does not rescue a
CAGR-floor failure — that failure is at gross 0.75, below 1.0, and is fixed by grossing UP to
1.0, not by borrowing). 4b full-sample passes: **3 of 12 cells each panel** (gross 1.00 both
bands + gross 1.25 band 0.03); only 1 of the 3 is a leverage rung, and it adds no Sharpe.

## Rule-8 walk-forward (2017-2026 read once)
The legal IS chooser lands on **band 0.08 / gross 1.00 (UNLEVERED)** on both panels:
- U56 OOS 12.00% / 1.163 / -19.05% (halves 1.267 / 1.048) — clears 4b OOS
- B136 OOS 10.98% / 1.092 / -19.50% (halves 1.230 / 0.934) — clears 4b OOS
vs RULES v2 OOS (U56 9.46% / 1.277 / -12.05%; B136 7.85% / 1.102 / -12.24%) and
SPY OOS 15.29% / 0.875 / -33.72%. **This reproduces the standing 2026-09-04 candidate
(band 0.08 / gross 1.00) — a cross-check, not a discovery — and the chooser rejects leverage.**

4a fails 0 of 2 panels at the pick (DD worse than the live book). Costs: U56 pick clears
4b at 0/10/25/50 bps (Sharpe 1.160 -> 1.084). Financing bites only levered cells: at
gross 1.25 band 0.08, fin 3%/6% shave ~0.07/0.14 pp/yr, and that cell already fails 4b OOS
on the DD cap regardless.

## Why KILL
1. Leverage is Sharpe-neutral — it cannot improve the risk-adjusted return or widen any 4b margin.
2. It trades CAGR for MaxDD ~1:1; the 4b DD cap (-20.23%) binds at gross ~1.25–1.5, before
   leverage adds anything the (already-cleared-at-gross-1.0) CAGR floor needs.
3. The only 4b passes it touches reproduce the incumbent band book at gross 1.00 (unlevered).
4. Financing (a real borrow cost the record's 0%-cash convention ignores) only worsens levered cells.

**Closes off "just lever the book" as a route past the CAGR floor.** No RULES.md / scan.py /
bot.py / baseline.py touched. Follow-ups filed as 2077 / 2081 (Open).

## Caveats
Current-constituent survivorship on both panels (flatters the trend book). Financing modelled
as a flat annual rate on borrowed gross; real leverage adds margin mechanics and path risk not
captured here. Sharpe-invariance to gross is exact only under the engine's 0%-cash / no-borrow-
cost convention; the financing arm is the first-order correction and it is negative.

Script: `2026-09-22_lever-the-band-vs-degross_B.py`; grid: `.grid.csv`.
