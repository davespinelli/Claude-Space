# Idea 1113 (lane C, 2026-09-16) — does the MIN-HOLD dial's L_DD -> L_CAGR leg swap have a CROSSING POINT?

**ANSWERED = NO. KILL of the crossing point, KILL of the interior optimum, KILL of the
monotone gradient, and a CORRECTION to the idea's own "without clearing both" premise.
No RULES change, no book promoted, no PROTOCOL edit (rule 6); RULES.md, PROTOCOL.md,
scan.py, bot.py and baseline.py untouched.**

SELECTION: lane C takes the SECOND open idea; 1112 and 1113 were the two at the head of
`## Open` and neither is EDGAR / Form 4 / 8-K / options / live-data, so 1113 is the claim.

## The two dials and no more (PROTOCOL rule 4)
`H` (min hold, trading days) on a fine ladder **{5, 7, 10, 13, 16, 21, 26, 32, 42, 52, 63}**
x `PANEL` {U56, B136}. **All 22 ladder points and all 198 walked cells published.**
H=126 is carried for cross-run gates only and is never an argmax rung. The N ladder
{5,8,10,12,15,20,25,30,40} is 1082/1086/1106's committed coordinate set, not a dial; every
rung is reported. Frozen at 1106's construction: cap INF, max_vol 0.60, gross 0.75, W
cadence, 10 bps, LAG 1, CAND20 legs [(21,252),(0,126),(0,63)], warm-up 260 rows.

## The statistic, fixed before any number
`DD_HEAD` = 100*(0.60*|SPY MaxDD| − |book MaxDD|), pp **of drawdown**.
`CAGR_HEAD` = 100*(book CAGR − 0.70*SPY CAGR), pp **of annual return**.
`MINHEAD` = min of the two — literally what the idea asks to maximise, and a **mixed-unit**
statistic. `RELMIN` (each leg as a fraction of its own bar) is published beside it at every
rung so no conclusion rests on the unmatched scaling. It picks the same rung.

## Gates: 12 of 12 pass, printed before any result number
G1 fast runner == `engine.backtest` 1.39e-17. G2 committed U56 W/H126/N=20 triple 3.18e-07.
G3 SPY OOS triple 1.70e-04 / 4.05e-05. G4 live RULES v2 MaxDD 4.95e-05 / 9.85e-06.
**G5 reproduces 1106's 90 committed book CAGR/MaxDD/turnover triples to 3.55e-15** (its CSV
re-read with `dtype=str, keep_default_na=False`, idea 1105's fix). **G6 reproduces 1106's own
conditional headroom medians at H=5/10/21/126 to 4.6e-03; G7 its "25 cells pass 4b FULL and
OOS" exactly.** G8 gross 0.75 everywhere. G9 MINHEAD identity. G10 MINHEAD>0 <=> L_DD and
L_CAGR both pass.

## The answer
**The two curves never meet.** `SWAP` = DD_HEAD − CAGR_HEAD is negative at all 11 rungs on
both panels, running −0.97 → −10.81 pp (U56) and −4.12 → −15.90 pp (B136) as H rises 5 → 63.
**Sign changes at NO rung.** L_DD binds at 92/99 (U56) and 99/99 (B136) cells; L_CAGR passes
198/198 and never binds. So "maximise the minimum" is just "maximise drawdown headroom", and
1106's leg swap is a widening gap, not a trade-off with a crossing point.

**The argmax is a grid edge.** Both panels peak at H=5 (U56 +1.415 pp, B136 −0.879 pp), the
ladder's low end — idea 1109's boundary-pick reading. RELMIN picks the same rung.

**And it is not resolved.** Ladder spread 6.170 pp (U56) / 7.329 pp (B136) — inside 1083's
4.1–7.2 pp band at one end. A paired 500-rep moving-block bootstrap (block 63d, the same
block indices applied to every rung *and* to SPY inside each replicate) separates **0 of 10
rungs from the argmax on either panel**: widths 4.28–9.66 pp and 4.61–12.70 pp against a
largest separation of +3.78 pp (H=5 vs H=63). The answer to "by how much does it beat 1083's
resolution" is **it does not beat it at all, on either the record's number or this run's own**.

**H_MONO_DD and H_MONO_CAGR both REFUTED** (2 and 4 DD inversions, 5 and 5 CAGR inversions):
1106's monotone gradient was a three-point reading of an eleven-point ladder.

## Correction to the idea's own premise
"Shortening the hold trades one leg for the other **without clearing both**" is wrong as
written. At the incumbent N=20 on U56, **6 of 11 rungs (H=5,7,10,13,16,26) clear all five
full-sample AND all three OOS 4b legs** — H_CLEARS is the one supported hypothesis of six.
What does not happen is clearing both with *resolved* headroom: the best MINHEAD anywhere on
the grid is +3.11 pp (U56 H=5 N=8), inside every width above.

## Rule 8 and both KEEP paths — nothing proposed
H chosen on IS 2009–2016 by IS MINHEAD at each (panel, N); OOS 2017–2026 read once.
**The IS chooser picks the OOS-best rung 0 of 18 times; median regret +3.10 pp (U56) /
+5.18 pp (B136)** — larger than 49 of the 50 passing cells' own headroom.
**4a 0 of 198** (A_DD 0/198: no rung drew down less than the live book).
**4b full 50 of 198, 4b OOS 53, full AND OOS 50** (48 U56, 2 B136); binding leg L_DD (fails
145/148 failures, sole failure 100), L_CAGR 0/148.
IS-reachable 4b passes: **3 of 9 N rungs on U56** (N=10 H=5, N=12 H=10, N=15 H=10; OOS Sharpe
1.072 / 1.162 / 1.132, OOS CAGR 16.29% / 17.25% / 15.90%, OOS MaxDD −17.5% / −18.2% / −19.1%
against SPY OOS 15.21% / 0.8711 / −33.72%), **0 of 9 on B136**. Unresolved by the bootstrap
above and refuted out of slice: **PARK, not KEEP. Nothing here is proposed as capital.**

## Survivorship (PROTOCOL rule 9)
U56 and B136 are current-constituent lists. Every level is optimistic and every 4a/4b count
is an upper bound. DD_HEAD and CAGR_HEAD are measured against SPY, a real index, so the bias
does **not** cancel out of them — the headrooms above overstate what a tradable book would
have had, in the direction that flatters the answer.
