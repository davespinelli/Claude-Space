# Memo — idea 190. Two PROTOCOL amendments, no RULES change

Not a KEEP candidate: the static sleeve is a KILL as an asset choice (see `.result.md`).
RULES.md, scan.py, bot.py and baseline.py are untouched; rule 6 means any PROTOCOL edit is a
Sunday-review decision, so this memo proposes wording and changes nothing.

**11c (replaces the clause-11/11b statistic).** An instrument's null clause is read on the
**SIGNED** effect, not on |dSharpe|: publish the real point's signed percentile in its null
population and the population's mean. A two-sided bar credits null draws that are large and
*harmful*, and this run has the exact counter-example — the static sleeve clears the published
two-sided bar in 21 of 72 points (29.2%) while being the **strict signed argmax of the whole
enumerated population in 72 of 72**, because the null mean dSharpe is negative in 100% of points.
Where the null population is enumerable, **enumerate it** (84 and 70 draws here) and publish an
exact percentile rather than a band — idea 208's proposal 11b, applied.

**11d (new).** Any instrument whose ASSET IDENTITIES were chosen by a person — a sleeve, a hedge
basket, a named pair — must publish an **IS-chosen-substitute arm**: apply the run's own IS
selector to the enumerated substitution population and read the result out of sample. Without it,
"the named assets beat their substitutes" is undated hindsight. The price of omitting it, measured
here: the named sleeve is the full-sample argmax in 72/72 but the IS argmax in only **8/72**, and
the triple an IS rule actually picks loses do-nothing by **−0.2509 OOS Sharpe, 0 wins in 12**,
against the named sleeve's **+0.0699, 12 wins in 12**. The gap, **−0.3208 (t −19.09)**, is the
whole value of being told the answer.

**Reporting note for the 527 sleeve rows in the LEADERBOARD.** A static sleeve's drawdown
improvement is **98.4%** reproduced by holding cash at the same f (median over 72 points), so any
sleeve row quoting MaxDD must quote the cash carve-out beside it or it is quoting de-grossing.
