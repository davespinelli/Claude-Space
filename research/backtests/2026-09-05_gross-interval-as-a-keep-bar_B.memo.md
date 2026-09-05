> Independent concurrent replication of idea 90; the parallel lane-B run's memo
> (`..._gross-interval-as-a-pre-registered-KEEP-bar_B.memo.md`) reaches the same verdict.
> Points 4, 6, 7 and 8 below are measurements that run did not make.

# Memo — idea 90: the gross interval as a REPORTED object, not as the verdict (Sunday review)

1. **No bar changes, no book, no KEEP.** phi = 0.70 and delta = 0.60 are untouched; 4b passes stay
   at 29 of 306 point / 72 of 306 family. This is a reporting proposal only.
2. **Reject the idea as queued.** Idea 90 asked for the interval WIDTH to replace the pass/fail.
   It cannot: within the 67 books the IS screen already admits, Spearman(IS width, OOS Sharpe) =
   +0.126 and AUC(width -> OOS-4b pass at m=1.00) = **+0.467**, below a coin flip. Plain IS Sharpe
   scores +0.915 / +0.820 / +0.902 on the same three targets. Width is dominated.
3. **Adopt the interval as a descriptor.** Proposed PROTOCOL rule 4b addition, verbatim:
   *"A 4b verdict is reported with the book's admissible gross set: its hull [g_min, g_max] in
   realised mean gross, the bar that fails just below g_min and just above g_max, and a flag if
   either end is set by rule 2's no-leverage ceiling rather than by a bar. The verdict itself
   remains the pass/fail. Measured on the 306-book corpus of ideas 129/131/144 at (phi, delta) =
   (0.70, 0.60): 72 books non-empty, median width 0.0750, lower shoulder = the CAGR floor in
   72 of 72, upper shoulder = the DD cap in 62, the no-leverage ceiling in 9, a Sharpe bar in 1."*
4. **The censoring flag is not optional.** 9 of 72 (12.5%) intervals end at the ceiling, so their
   width measures rule 2, not 4b. This is idea 145's "width alone is not robustness" on the gross
   axis; quote the flag with the number or do not quote the number.
5. **Say "admissible set", not "interval".** Across the 42-point (phi, delta) grid, 52 of 2,707
   non-empty verdicts are gapped (1.92%), every one of them at phi <= 0.50. At the published bars
   0 of 72 are gapped, so the hull is exact where it is used and an approximation elsewhere.
6. **Idea 84's mechanism is confirmed and can be stated as fact.** Restricted to the 55 books whose
   arm is a pure exposure rescale (`ctl`/`gate`/`stop`), no Sharpe bar appears at either shoulder;
   family Sharpe spread is 0.0034-0.0039 there against 0.1928 for `ddctl` and 0.0487 for `ebud`.
   The clause should therefore say it holds for scale-free instruments and name the exceptions.
7. **4a needs different words.** With no CAGR floor, 4a's admissible set is a one-sided CAP: 183 of
   its 184 non-empty sets run to the grid floor. Write 4a's as "g <= g_max", not as an interval.
   On this corpus 4b is a strict subset of 4a (both 72, 4b-only 0), so 4b is the binding path.
8. **Correction to carry: the incumbent's published gross is right; idea 84's alternative is not.**
   `EWall + vol60-dg` at g = 0.75 is interior in 4 of 4 large-cap cells (joint [0.6839, 0.7594]).
   Idea 84's by-product, `ew-band3` at g = 0.85, is inside its interval in **1 of 4** cells; broad
   caps it at 0.7877, three grid steps below 0.85. Idea 84 used a finer ladder and a 5 bps rung —
   **queued as idea 154** to resolve before either number is quoted again.
9. **Rule 8 wording:** *"An interval width may be reported but may not be used to select a book:
   on the 18-cell corpus the widest-interval selector returns OOS 13.10% / 1.049 / -20.52% against
   the incumbent screen's 12.70% / 1.022 / -21.14% and the do-nothing control's 14.18% / 1.051 /
   -24.31% on the 7 cells all three enter."* The screen's value is abstention (11 of 18 cells
   declined), not selection — S1 and S4 pick identically, reproducing idea 132 independently.
10. **Nothing here is a KEEP for capital.** RULES is untouched, no arm is proposed, and the
    standing 4b candidate is unaffected.
