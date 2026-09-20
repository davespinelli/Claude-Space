# Idea 1703 (lane B, 2026-09-20) — the standing 4b pass is a SURVIVORSHIP pass

**Verdict: KILL of the capital claim, not of the book.** The band book still does what the record
says it does on U56. It does it only on the half of U56 whose names were chosen ex post.

1. `universe.json` = **36 ETFs + 20 mega-caps**. The ETFs are the survivorship-clean leg (no ETF is
   in the file for having won — USO and UNG are in it having lost 80-99%); the 20 mega-caps are in
   the file *because* they became the 20 largest US companies.
2. Same book, same two dials (`c` in {0.00,0.03,0.05,0.10,0.15} x `G` in {0.25,0.50,0.75,1.00}),
   same tape, 10 bps, weekly, t+1. **4b passes on FULL *and* OOS: U56 5/20, STK20 6/20, ETF36 0/20,
   and 0/400 over 20 matched-count random ETF20 draws.**
3. ETF36 is not a near miss. Its **best cell over the whole grid earns 6.33%/yr against a CAGR floor
   of 10.59%**, and its **H1 Sharpe never exceeds 0.839 against SPY's 0.9573 bar** — the CAGR leg
   fails 20/20 and the H1 leg 20/20. The drawdown leg, the one the record has spent nine runs
   defending, passes 20/20 on every panel.
4. Rule 8 (picks fit on <=2016-12-31, 2017-2026 read once): **ETF36 0 of 4 choosers clear 4b OOS**
   (best OOS 0.9109 Sharpe / 5.37% CAGR); U56 3 of 4, STK20 2 of 4. The R20 pool is 0 of 80.
5. The 2026-09-19 CHANGELOG pick replays exactly: U56 c=0.10 G=1.00 FULL 11.72% / 1.1726 / -16.30%,
   OOS 12.14% / 1.1940 / -16.30%. On ETF36 the same cell is 6.33% / 0.7985 / -12.64%.
6. **The sharpest control in the run needs no rule at all.** Plain equal-weight buy-and-hold of the
   20 mega-caps at G = 0.50, no band, no ranking, no rebalance signal, clears 4b on FULL and OOS
   (15.27% / 1.3709 / -16.69%; OOS 1.3227 / -16.69%). It is the only one of 92 no-gate twins that
   does. A bar a survivorship-selected buy-and-hold clears is not, on this panel, measuring a rule.
7. The band is still worth something where it is worth anything: at c=0.03 it buys +0.0821 Sharpe
   and +10.47 pp of drawdown on U56 and +0.0736 / +8.84 pp on STK20 — but **-0.0061 Sharpe on
   ETF36**, for +11.79 pp of depth it could have bought by de-grossing instead.
8. Honest limit: deleting STK20 removes the *largest* survivorship channel, not all of it. The 16
   sector ETFs were still named in 2026. So **STK20 - ETF36 is a lower bound** on how much of the
   pass is selection.
9. All 460 grid cells, 92 no-gate twins and 92 walk-forward rows are published. Gates 7/7 (G1
   replays `baseline.rules_v2_weights` to 1.735e-17 — the U56 c=0.03/G=0.75 cell IS the live book;
   G5 hard-truncation test: 0 chooser picks change). Deterministic, offline, 24s.
10. **PROPOSED, NOT ENACTED (rule 6, Sunday review only).** Add to PROTOCOL rule 9, after the
    existing sentence: *"A 4b pass quoted on U56 or B136 MUST be quoted beside its ETF-only
    replication on the same dials and the same tape. Where the ETF-only leg fails, the pass is
    reported as SURVIVORSHIP-CONDITIONAL and is not a KEEP."* No change to RULES.md, scan.py,
    bot.py or baseline.py; no book promoted, no book demoted, no live rule touched.
