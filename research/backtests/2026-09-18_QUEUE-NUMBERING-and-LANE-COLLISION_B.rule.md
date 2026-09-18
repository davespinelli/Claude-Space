<!-- QUEUE HYGIENE RULE (idea 932, adopted 2026-09-18 lane B).  Two clauses, both mechanical.
  (N) NUMBERING.  A new idea's number is `1 + the maximum number appearing ANYWHERE in this
      file` (Open, In progress and Done alike), read at the moment of filing, PLUS the lane's
      reservation offset: lane A +0, lane B +1, lane C +2, cloud +3, then stride 4 for a lane's
      second and later ideas in the same run (A: m+1, m+5, ...; B: m+2, m+6, ...).  Two lanes
      filing in the same hour therefore cannot collide even before either has pushed, and no
      number is ever reused.  A collision that survives a rebase is resolved by RENUMBERING the
      later-pushed line, never by deleting either.
  (C) CLAIMING.  A claim is only real once it is PUSHED.  A lane claims by moving the idea's
      line to '## In progress' with the date and the lane, pushing that single-file commit
      BEFORE any compute, and re-checking after `git pull --rebase`: if the rebase reveals the
      same idea claimed by another lane, the LATER-pushed claim yields and takes the next
      eligible idea.  An idea standing in '## In progress' or '## Done' is never claimable, and
      an Open line duplicating one is a stale copy to be removed, not re-run.
  (D) DE-DUPLICATION.  An Open line is removable only if its (number, slug) pair already stands
      elsewhere in the file.  No unique idea text is ever deleted by this rule. -->
