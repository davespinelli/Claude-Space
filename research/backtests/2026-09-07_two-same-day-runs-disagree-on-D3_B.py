#!/usr/bin/env python3
"""Idea 382 — two same-day runs disagree on D3 for PATH-DEPENDENT arms by exactly one draw.

THE FILED PREMISE (research/QUEUE.md, idea 382)
-----------------------------------------------
    "idea 124's `_B` and `_B2` runs SHARE SEED, q order and NDRAW and agree to the last
     digit on every GATE arm, but on ebud-0.10 / ebud-0.20 / stop15 their D3 frac_pos
     differs by EXACTLY 0.025 (one draw of forty): `_B2` reproduces idea 122's COMMITTED
     d3.csv at 0.000e+00, `_B` does not.  Find the difference (cost accrual inside the
     state machine? sub-panel column order? pending-exit handling?) and make the record
     carry one number for stateful instruments.  INFRASTRUCTURE."

Three factual claims are load-bearing and all three are checked here BEFORE anything is
recomputed, directly off the committed artefacts:

    P1  the two runs share a seed.
    P2  they agree to the last digit on every gate arm.
    P3  the disagreement is exactly one draw of forty (0.025) on three stateful arms.

PRE-REGISTRATION (written before the measurement section runs)
-------------------------------------------------------------
H0 (the queue's hypothesis)  the disagreement is a PATH-DEPENDENCE defect: something in
    the stateful machine (cost accrual, pending exits, sub-panel column order) makes a
    stateful arm's return depend on run identity.  Signature: stateless (gate) arms agree
    exactly; stateful arms do not.

H1 (the alternative tested here)  the disagreement is DRAW NOISE from two different draw
    sets.  Signature: every arm disagrees, stateful and stateless alike, by an amount
    whose distribution is reproduced by re-drawing the sub-panels.

"Stateful arms disagree more" does NOT by itself separate the two: a state machine
amplifies whatever the panel does, so pure re-drawing can produce exactly that signature
with no defect at all.  The permutation test below therefore measures AMPLIFICATION
(H_amp: draw noise is larger on stateful arms) and is reported as a descriptive fact, not
as evidence for H0.

The DECISIVE test is a per-cell CALIBRATION.  Draw M independent sub-panels from one
master stream and cut them into disjoint blocks of N (statistically identical to
independent seeds, since each draw is an independent uniform sample of columns).  For each
(book, arm) cell this yields a null distribution of block-to-block |frac_pos| gaps that is
SPECIFIC TO THAT CELL, so an arm's own amplification is already inside the null.  Locate
the actually-observed `_B` vs `_B2` gap for that cell inside its own null and record the
percentile.  Under H1 those percentiles are Uniform(0,1); under H0 the stateful cells sit
systematically high.

Decision rule, fixed in advance:
  * H1 is sufficient (H0 unnecessary) if the mean cell percentile does not exceed 0.5 at
    a one-sided p < 0.05 (10,000 permutations of the sign of the deviation), tested on
    ALL cells and on the STATEFUL cells alone.
  * H0 is retained only if the stateful cells' percentiles are significantly high.
  * The deliverable "one number for stateful instruments" is then answered by asking what
    NDRAW makes the statistic reproducible to a stated tolerance, and, if no feasible
    NDRAW does, by proposing that the draw SET be fixed instead of the draw COUNT.

TWO TUNED PARAMETERS (PROTOCOL rule 4): N (draws per replicate) and tau (the D3 bar).
q is held at idea 119/122's pre-registered headline 0.10 and is not tuned.  ALL grid
points are reported.

CONSTRUCTION.  Nothing here is re-derived: the panel, book targets, arm specs, state
machine and dpair() are imported from the committed `_B2` script (which itself imports
idea 94's harness), so the sub-panel construction is byte-identical to the run that
reproduces idea 122 at 0.000e+00.  Books are restricted to TOP20 (idea 94's published
rung) and TOPALL (the deepest rung) to buy draws with the compute; both universes'
committed d3 files are still used in full for the forensic section.

PROTOCOL: 10 bps (rule 2), next-day execution (engine), rule-8 walk-forward, both KEEP
paths 4a and 4b.  Deterministic, standalone, modifies nothing outside research/.
"""
import importlib.util
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))

from baseline import rules_v2_weights  # noqa: E402  (also puts engine on sys.path)
from engine import backtest, metrics  # noqa: E402

BT = ROOT / "research" / "backtests"
STEM = Path(__file__).stem
OUT = BT / STEM


def _load(stem, mod):
    spec = importlib.util.spec_from_file_location(mod, BT / f"{stem}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


B2 = _load("2026-09-07_book-size-floor-for-any-quoted-price_B2", "i124b2")
H = B2.H

# ---- committed artefacts under audit
F_B = BT / "2026-09-07_book-size-floor-for-any-quoted-price_B"
F_B2 = BT / "2026-09-07_book-size-floor-for-any-quoted-price_B2"
F_122 = BT / "2026-09-05_price-denominator-sign-test_C"

# ---- constants (idea 122/124's, unchanged)
PCOST = 10.0
Q_STAR = 0.10                               # idea 119/122's headline, NOT tuned here
TAUS = (0.80, 0.90, 0.95, 1.00)             # tuned dial 2; 0.90 is the record's headline
NGRID = (10, 20, 40, 80)                    # tuned dial 1; 40 is the record's NDRAW
M_DRAWS = 480                               # master stream length (lcm-friendly for NGRID)
MASTER_SEED = 20260907382
BOOKS = ["TOP20", "TOPALL"]
ARMS = B2.ARMS
STATEFUL = {"stop15", "stop25", "ddctl-8/.5/recover", "ddctl-8/.5/high",
            "ebud-0.10", "ebud-0.20"}
IS_END, OOS_START = H.IS_END, H.OOS_START
NPERM = 10000

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 3000)


def fmt(df, nd=4):
    return df.to_string(index=False, float_format=lambda x: f"{x:.{nd}f}")


def rule(c="="):
    print(c * 118)


# =============================================================== 0. FORENSICS
def const_of(path, name):
    """Read a module-level constant assignment out of a committed script's SOURCE."""
    src = path.read_text()
    m = re.search(rf"^NDRAW, DROP_FRACS, TAUS, SEED\s*=\s*(.+)$", src, re.M)
    if m:
        vals = eval("(" + m.group(1) + ")")                      # noqa: S307 (own repo)
        return dict(NDRAW=vals[0], DROP_FRACS=vals[1], TAUS=vals[2], SEED=vals[3])[name]
    raise KeyError(name)


def bootstrap_src(path):
    """The bootstrap() PRICING LOOP, whitespace/comment/local-name normalised.

    Everything from `rng = np.random.default_rng(SEED)` down to the progress print is the
    part that decides the numbers; what each script does with the frame afterwards (`_B`
    aggregates in a separate d3_table(), `_B2` inline) cannot change a draw's price."""
    src = path.read_text().split("\n")
    i = next(k for k, l in enumerate(src) if l.startswith("def bootstrap("))
    body, j = [], i + 1
    while j < len(src) and not (src[j] and not src[j][0].isspace()):
        body.append(src[j])
        j += 1
    txt = "\n".join(body)
    txt = re.sub(r'""".*?"""', "", txt, flags=re.S)              # drop docstring
    txt = re.sub(r"#.*", "", txt)                                # drop comments
    txt = txt.split("        print(")[0]                         # stop at the progress print
    txt = re.sub(r"\bsignals\b|\bpanel\b", "PANELFN", txt)       # the two names differ
    txt = re.sub(r"\btargets_n\b|\btargets\b", "TARGETFN", txt)
    txt = re.sub(r"\bgt\b|\bg\b", "GATEVAR", txt)
    txt = re.sub(r"nkeep=k,\s*", "", txt)                        # _B carries an extra column
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt


def forensics():
    rule()
    print("[0] FORENSICS — the three filed claims, checked against the committed artefacts")
    rule()

    s_b, s_b2 = const_of(F_B.with_suffix(".py"), "SEED"), const_of(F_B2.with_suffix(".py"), "SEED")
    n_b, n_b2 = const_of(F_B.with_suffix(".py"), "NDRAW"), const_of(F_B2.with_suffix(".py"), "NDRAW")
    q_b, q_b2 = (const_of(F_B.with_suffix(".py"), "DROP_FRACS"),
                 const_of(F_B2.with_suffix(".py"), "DROP_FRACS"))
    print(f"  _B  : SEED={s_b}  NDRAW={n_b}  DROP_FRACS={q_b}")
    print(f"  _B2 : SEED={s_b2}  NDRAW={n_b2}  DROP_FRACS={q_b2}")
    p1 = (s_b == s_b2)
    print(f"  [P1] 'the two runs share seed'                       -> "
          f"{'CONFIRMED' if p1 else 'REFUTED'}  "
          f"(seeds differ by {abs(s_b - s_b2)}; q order and NDRAW DO match)")

    same_struct = bootstrap_src(F_B.with_suffix(".py")) == bootstrap_src(F_B2.with_suffix(".py"))
    print(f"  [struct] bootstrap() bodies, normalised, are IDENTICAL -> {same_struct}  "
          f"(same loop nesting, same rng call, same order of rng consumption)")

    d = {}
    for k, f in (("B", F_B), ("B2", F_B2), ("C122", F_122)):
        t = pd.read_csv(f.with_suffix("").as_posix() + ".d3.csv")
        t["book"] = t["book"].str.upper()                        # _B writes TOPall, _B2 TOPALL
        d[k] = t
    key = ["uni", "q", "book", "arm"]
    cols = ["frac_pos_full", "frac_pos_IS", "frac_pos_OOS", "frac_priceable"]

    print("\n  reproduction of idea 122's COMMITTED d3.csv (192 shared rows: TOP20/V1u x 16 arms x 3q x 2uni)")
    gates = {}
    for k in ("B", "B2"):
        mm = d["C122"].merge(d[k], on=key, suffixes=("_C", "_x"))
        w = {c: float((mm[c + "_C"] - mm[c + "_x"]).abs().max()) for c in cols}
        gates[k] = max(w.values())
        print(f"    _{k:<3s} n={len(mm):3d}  max|diff| " +
              "  ".join(f"{c}={w[c]:.3e}" for c in cols) +
              f"   -> {'EXACT' if gates[k] < 1e-12 else 'NOT EXACT'}")
    print(f"  [G1] _B2 reproduces idea 122 at {gates['B2']:.3e}  "
          f"({'PASS — this run inherits _B2 construction' if gates['B2'] < 1e-12 else 'FAIL'})")

    m = d["B"].merge(d["B2"], on=key, suffixes=("_B", "_B2"))
    print(f"\n  _B vs _B2 across ALL {len(m)} shared rows (7 books x 16 arms x 3 q x 2 uni):")
    for c in cols:
        dd = (m[c + "_B"] - m[c + "_B2"]).abs()
        print(f"    {c:<16s} rows differing {int((dd > 1e-12).sum()):3d}/{len(dd)}  "
              f"max {dd.max():.4f}  mean {dd.mean():.4f}  "
              f"(max is {dd.max() * 40:.0f} draws of 40)")
    m["ad"] = (m.frac_pos_full_B - m.frac_pos_full_B2).abs()
    m["stateful"] = m.arm.isin(STATEFUL)
    by = (m.groupby("arm")
            .agg(n=("ad", "size"), rows_differ=("ad", lambda s: int((s > 1e-12).sum())),
                 max_ad=("ad", "max"), mean_ad=("ad", "mean"))
            .reset_index())
    by["stateful"] = by.arm.isin(STATEFUL)
    print("\n  per-arm |frac_pos_full(_B) - frac_pos_full(_B2)|, "
          "42 rows per arm (7 books x 3 q x 2 universes):")
    print(fmt(by.sort_values("max_ad", ascending=False)))
    gate_rows = m[~m.stateful]
    p2 = float(gate_rows.ad.abs().max()) < 1e-12
    print(f"\n  [P2] 'agree to the last digit on every GATE arm'     -> "
          f"{'CONFIRMED' if p2 else 'REFUTED'}  "
          f"(stateless arms: {int((gate_rows.ad > 1e-12).sum())}/{len(gate_rows)} rows differ, "
          f"max {gate_rows.ad.max():.4f})")
    three = m[m.arm.isin(["ebud-0.10", "ebud-0.20", "stop15"])]
    p3 = np.allclose(three.ad[three.ad > 1e-12], 0.025, atol=1e-9)
    print(f"  [P3] 'differs by exactly 0.025 on ebud/stop15'       -> "
          f"{'CONFIRMED' if p3 else 'REFUTED'}  "
          f"(those 3 arms: {int((three.ad > 1e-12).sum())}/{len(three)} rows differ, "
          f"spread {three.ad.min():.4f}..{three.ad.max():.4f}, "
          f"{int(round(three.ad.max() * 40))} draws of 40)")
    print(f"  [note] mean |diff| stateful {m[m.stateful].ad.mean():.4f} "
          f"vs stateless {m[~m.stateful].ad.mean():.4f} — the raw contrast the queue read")
    by.to_csv(f"{OUT}.forensics_by_arm.csv", index=False)
    m[key + ["ad", "stateful"]].to_csv(f"{OUT}.forensics_rows.csv", index=False)

    # the matched subset this run will calibrate against
    sub = m[(m.uni == "universe.json(56)") & (m.q == Q_STAR) & (m.book.isin(BOOKS))]
    obs = float(sub.ad.max())
    print(f"\n  MATCHED SUBSET for calibration (u56, q={Q_STAR}, books {BOOKS}, 16 arms): "
          f"n={len(sub)}, max|diff| {obs:.4f}, mean {sub.ad.mean():.4f}, "
          f"{int((sub.ad > 1e-12).sum())} rows differ")
    return dict(p1=p1, p2=p2, p3=p3, same_struct=same_struct, g1=gates["B2"], g2=gates["B"],
                obs_matched_max=obs, obs_matched_mean=float(sub.ad.mean()),
                obs_matched_n=len(sub), matched=sub)


# =============================================================== 1. MASTER DRAW STREAM
def master_stream(px, start):
    """M independent sub-panel draws at q=Q_STAR, priced on BOOKS x ARMS.

    Exactly `_B2`'s bootstrap() inner body — same panel(), targets(), H.run(), dpair() —
    with the draw index carried so the stream can be cut into disjoint replicate blocks."""
    rng = np.random.default_rng(MASTER_SEED)
    ncol = px.shape[1]
    k = int(round(ncol * (1 - Q_STAR)))
    out, t0 = [], time.time()
    for dix in range(M_DRAWS):
        keep = sorted(rng.choice(ncol, size=k, replace=False))
        sub = px.iloc[:, keep]
        Ss = B2.panel(sub)
        for b in BOOKS:
            rc = H.run(sub, B2.targets(sub, b, Ss), bps=PCOST)["r"].loc[start:]
            for name, kind, kwargs, (g, conv) in ARMS:
                ra = H.run(sub, B2.targets(sub, b, Ss, g, conv), bps=PCOST,
                           **kwargs)["r"].loc[start:]
                rec = dict(draw=dix, book=b, arm=name, kind=kind)
                for w in ("full", "IS", "OOS"):
                    dc, dd, rt = B2.dpair(B2.win(rc, w), B2.win(ra, w))
                    rec[f"dCAGR_{w}"], rec[f"dMaxDD_{w}"], rec[f"rate_{w}"] = dc, dd, rt
                out.append(rec)
        if (dix + 1) % 40 == 0:
            print(f"    draws {dix + 1:4d}/{M_DRAWS}  ({time.time() - t0:.0f}s elapsed)",
                  flush=True)
    return pd.DataFrame(out)


def frac_table(D, ndraw, block):
    """frac_pos over one block of `ndraw` draws."""
    lo, hi = block * ndraw, (block + 1) * ndraw
    d = D[(D.draw >= lo) & (D.draw < hi)]
    g = d.groupby(["book", "arm"])
    return pd.DataFrame(dict(
        frac_pos_full=g.dMaxDD_full.apply(lambda s: float((s > 0).mean())),
        frac_pos_IS=g.dMaxDD_IS.apply(lambda s: float((s > 0).mean())),
        frac_pos_OOS=g.dMaxDD_OOS.apply(lambda s: float((s > 0).mean())),
    )).reset_index().assign(N=ndraw, block=block)


# =============================================================== 2. REPLICATE SPREAD
def spread_analysis(D, fx):
    rule()
    print(f"[2] REPLICATE SPREAD — {M_DRAWS} draws cut into disjoint blocks of N "
          f"(u56, q={Q_STAR}, {len(BOOKS)} books x {len(ARMS)} arms = "
          f"{len(BOOKS) * len(ARMS)} cells)")
    rule()
    reps = pd.concat([frac_table(D, N, b) for N in NGRID for b in range(M_DRAWS // N)],
                     ignore_index=True)
    reps["stateful"] = reps.arm.isin(STATEFUL)
    reps.to_csv(f"{OUT}.replicates.csv", index=False)

    rows = []
    for N in NGRID:
        r = reps[reps.N == N]
        nb = M_DRAWS // N
        for col in ("frac_pos_full", "frac_pos_IS", "frac_pos_OOS"):
            g = r.groupby(["book", "arm"])[col]
            sd, rng_ = g.std(ddof=1), g.max() - g.min()
            rows.append(dict(N=N, blocks=nb, stat=col, mean_sd=float(sd.mean()),
                             max_sd=float(sd.max()), mean_range=float(rng_.mean()),
                             max_range=float(rng_.max()),
                             binom_sd=float(np.sqrt(0.25 / N))))
    SP = pd.DataFrame(rows)
    print("\n  block-to-block dispersion of frac_pos by N (binom_sd = sqrt(.25/N), the "
          "independent-Bernoulli ceiling at p=0.5):")
    print(fmt(SP))
    SP.to_csv(f"{OUT}.spread_by_N.csv", index=False)

    print("\n  H_amp — stateful vs stateless replicate SD of frac_pos_full.  This is "
          "DESCRIPTIVE:\n  a state machine amplifies panel composition, so a high `diff` "
          "is what pure draw noise\n  looks like on these arms, NOT evidence of a "
          "run-identity defect:")
    perm_rows = []
    rs = np.random.default_rng(11)
    for N in NGRID:
        r = reps[reps.N == N]
        sd = (r.groupby(["book", "arm", "stateful"])["frac_pos_full"].std(ddof=1)
                .reset_index())
        a = sd[sd.stateful].frac_pos_full.values
        b = sd[~sd.stateful].frac_pos_full.values
        obs = float(a.mean() - b.mean())
        pool = np.concatenate([a, b])
        na = len(a)
        cnt = 0
        for _ in range(NPERM):
            p = rs.permutation(pool)
            if (p[:na].mean() - p[na:].mean()) >= obs:
                cnt += 1
        pval = (cnt + 1) / (NPERM + 1)
        perm_rows.append(dict(N=N, n_stateful=na, n_stateless=len(b),
                              sd_stateful=float(a.mean()), sd_stateless=float(b.mean()),
                              diff=obs, p_one_sided=pval,
                              amp_significant=bool(pval < 0.05)))
    PERM = pd.DataFrame(perm_rows)
    print(fmt(PERM, 4))
    PERM.to_csv(f"{OUT}.stateful_permutation.csv", index=False)

    # ---- CALIBRATION: per-cell, does draw noise alone reproduce the _B vs _B2 gap?
    CAL_N = 40 if 40 in NGRID else max(NGRID)
    tag = " (the record's NDRAW)" if CAL_N == 40 else ""
    print(f"\n  CALIBRATION at N={CAL_N}{tag} — for EACH (book, arm) cell, the null\n"
          f"  distribution of |frac_pos_full| gaps between disjoint blocks, and where the\n"
          f"  actually observed _B vs _B2 gap for that same cell sits inside it:")
    rN = reps[reps.N == CAL_N]
    gaps, cells = [], []
    obs_map = {(r.book, r.arm): float(r.ad) for r in fx["matched"].itertuples()}
    for (bk, ar), g in rN.groupby(["book", "arm"]):
        v = g.frac_pos_full.values
        null = np.array([abs(v[i] - v[j]) for i in range(len(v))
                         for j in range(i + 1, len(v))])
        for x in null:
            gaps.append(dict(book=bk, arm=ar, stateful=ar in STATEFUL, gap=float(x)))
        o = obs_map.get((bk, ar))
        if o is None:
            continue
        cells.append(dict(book=bk, arm=ar, stateful=ar in STATEFUL, obs_gap=o,
                          null_n=len(null), null_mean=float(null.mean()),
                          null_max=float(null.max()),
                          pct=float((null < o).mean() + 0.5 * (null == o).mean())))
    GAP = pd.DataFrame(gaps)
    CELL = pd.DataFrame(cells)
    GAP.to_csv(f"{OUT}.calibration_gaps.csv", index=False)
    CELL.to_csv(f"{OUT}.calibration_cells.csv", index=False)
    print("\n" + fmt(CELL.sort_values("pct", ascending=False)))

    rs2 = np.random.default_rng(23)

    def sign_perm(x):
        """One-sided permutation test that mean(pct) <= 0.5, flipping deviation signs."""
        dv = np.asarray(x) - 0.5
        obs = dv.mean()
        cnt = sum(1 for _ in range(NPERM)
                  if (dv * rs2.choice([-1.0, 1.0], size=len(dv))).mean() >= obs)
        return float(obs + 0.5), float((cnt + 1) / (NPERM + 1))

    print("\n  [CAL] mean cell percentile of the observed gap inside its own null "
          "(0.50 = pure draw noise):")
    cal_rows = []
    for lab, sel in (("ALL cells", CELL), ("STATEFUL only", CELL[CELL.stateful]),
                     ("STATELESS only", CELL[~CELL.stateful])):
        if len(sel) < 3:
            continue
        mp, pv = sign_perm(sel.pct.values)
        cal_rows.append(dict(subset=lab, n=len(sel), mean_pct=mp, p_one_sided=pv,
                             exceeds_noise=bool(pv < 0.05),
                             obs_mean_gap=float(sel.obs_gap.mean()),
                             null_mean_gap=float(sel.null_mean.mean())))
    CAL = pd.DataFrame(cal_rows)
    print(fmt(CAL, 4))
    CAL.to_csv(f"{OUT}.calibration_test.csv", index=False)

    obs_max = fx["obs_matched_max"]
    q = {p: float(np.quantile(GAP.gap, p)) for p in (0.5, 0.9, 0.95, 0.99, 1.0)}
    contained = obs_max <= q[1.0]
    pct = float((GAP.gap >= obs_max).mean())
    print(f"\n    pooled null ({len(GAP)} block pairs): mean {GAP.gap.mean():.4f}, "
          f"median {q[0.5]:.4f}, p90 {q[0.9]:.4f}, p95 {q[0.95]:.4f}, "
          f"p99 {q[0.99]:.4f}, max {q[1.0]:.4f}")
    print(f"    observed _B vs _B2 on the SAME {fx['obs_matched_n']} cells: "
          f"mean {fx['obs_matched_mean']:.4f}, max {obs_max:.4f}")
    print(f"    draw noise alone {'CONTAINS' if contained else 'DOES NOT CONTAIN'} the "
          f"observed max ({100 * pct:.2f}% of noise gaps are at least as large)")
    h0 = bool(CAL[CAL.subset == "STATEFUL only"].exceeds_noise.any()) if len(CAL) else False
    return reps, SP, PERM, GAP, dict(contained=contained, pct=pct, q=q, CELL=CELL, CAL=CAL,
                                     h0_retained=h0,
                                     ratio=float(fx["obs_matched_mean"] / GAP.gap.mean()))


# =============================================================== 3. VERDICT STABILITY
def verdict_stability(reps):
    rule()
    print("[3] WHAT THE NOISE COSTS THE RECORD — D3 admissibility flips across replicates")
    print("    (full grid: N x tau; a cell is UNSTABLE if the tau verdict is not unanimous "
          "over the disjoint blocks)")
    rule()
    rows = []
    for N in NGRID:
        r = reps[reps.N == N]
        nb = M_DRAWS // N
        for tau in TAUS:
            v = r.assign(adm=(r.frac_pos_full >= tau))
            g = v.groupby(["book", "arm"])["adm"]
            unan = g.nunique()
            share = g.mean()
            rows.append(dict(N=N, blocks=nb, tau=tau, cells=len(unan),
                             unstable=int((unan > 1).sum()),
                             unstable_frac=float((unan > 1).mean()),
                             mean_adm_share=float(share.mean()),
                             flip_prob=float((2 * share * (1 - share)).mean())))
    V = pd.DataFrame(rows)
    print(fmt(V))
    V.to_csv(f"{OUT}.verdict_stability.csv", index=False)
    HN = 40 if 40 in NGRID else max(NGRID)
    hl = V[(V.N == HN) & (V.tau == 0.90)].iloc[0]
    print(f"\n  HEADLINE cell (N={HN}, tau=0.90 — the record's own setting): "
          f"{hl.unstable}/{hl.cells} cells ({hl.unstable_frac:.1%}) get a DIFFERENT "
          f"admissibility verdict depending only on the seed; "
          f"P(two runs disagree) = {hl.flip_prob:.3f}")

    print("\n  N needed for a stated tolerance (extrapolating the measured mean SD as "
          "c/sqrt(N), c fitted on NGRID):")
    fitrows = []
    for col in ("frac_pos_full", "frac_pos_IS", "frac_pos_OOS"):
        xs, ys = [], []
        for N in NGRID:
            r = reps[reps.N == N]
            ys.append(float(r.groupby(["book", "arm"])[col].std(ddof=1).mean()))
            xs.append(1.0 / np.sqrt(N))
        c = float(np.polyfit(xs, ys, 1)[0] + 0.0) if len(xs) > 1 else np.nan
        c = float(np.sum(np.array(xs) * np.array(ys)) / np.sum(np.array(xs) ** 2))
        for tol in (0.05, 0.025, 0.01):
            fitrows.append(dict(stat=col, c=c, tol=tol, N_needed=int(np.ceil((c / tol) ** 2))))
    F = pd.DataFrame(fitrows)
    print(fmt(F, 4))
    F.to_csv(f"{OUT}.n_needed.csv", index=False)
    return V, F


# =============================================================== 4. RULE 8 WALK-FORWARD
def walk_forward(D, reps, px, start, bars, v2_net, spy):
    rule()
    print("[4] RULE 8 WALK-FORWARD — parameters (N, tau) chosen on 2009-2016 ONLY, "
          "2017-2026 untouched")
    print("    Selector: among cells whose IS-window D3 fraction clears tau, take the one "
          "with the best IS Sharpe; report its OOS.")
    rule()
    # deterministic full-panel returns for every (book, arm), the object actually selected
    S = B2.panel(px)
    rets = {}
    for b in BOOKS:
        for name, kind, kwargs, (g, conv) in H.arm_specs():
            rets[(b, name)] = H.run(px, B2.targets(px, b, S, g, conv), bps=PCOST,
                                    **kwargs)["r"].loc[start:]
    m_is = {k: metrics(B2.win(r, "IS")) for k, r in rets.items()}
    m_oos = {k: metrics(B2.win(r, "OOS")) for k, r in rets.items()}

    v2_oos = metrics(B2.win(v2_net, "OOS"))
    spy_oos = metrics(B2.win(spy, "OOS"))
    print(f"  OOS bars: SPY {spy_oos['CAGR']:.2%}/{spy_oos['Sharpe']:.3f}/"
          f"{spy_oos['MaxDD']:.2%}   RULES v2 {v2_oos['CAGR']:.2%}/"
          f"{v2_oos['Sharpe']:.3f}/{v2_oos['MaxDD']:.2%}")

    rows = []
    for N in NGRID:
        r = reps[reps.N == N]
        for tau in TAUS:
            for blk, g in r.groupby("block"):
                adm = g[g.frac_pos_IS >= tau]
                if len(adm) == 0:
                    rows.append(dict(N=N, tau=tau, block=int(blk), pick="(none admissible)",
                                     n_adm=0, IS_Sharpe=np.nan, OOS_CAGR=np.nan,
                                     OOS_Sharpe=np.nan, OOS_MaxDD=np.nan,
                                     vs_SPY=np.nan, vs_v2=np.nan))
                    continue
                cand = [((b, a), m_is[(b, a)]["Sharpe"])
                        for b, a in zip(adm.book, adm.arm)]
                pick = max(cand, key=lambda t: t[1])[0]
                mo = m_oos[pick]
                rows.append(dict(N=N, tau=tau, block=int(blk),
                                 pick=f"{pick[0]}/{pick[1]}", n_adm=len(adm),
                                 IS_Sharpe=m_is[pick]["Sharpe"], OOS_CAGR=mo["CAGR"],
                                 OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                 vs_SPY=mo["Sharpe"] - spy_oos["Sharpe"],
                                 vs_v2=mo["Sharpe"] - v2_oos["Sharpe"]))
    W = pd.DataFrame(rows)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)

    agg = (W.groupby(["N", "tau"])
             .agg(blocks=("block", "size"), n_distinct_picks=("pick", "nunique"),
                  modal_share=("pick", lambda s: float(s.value_counts(normalize=True).iloc[0])),
                  mean_OOS_Sharpe=("OOS_Sharpe", "mean"),
                  sd_OOS_Sharpe=("OOS_Sharpe", "std"),
                  min_OOS_Sharpe=("OOS_Sharpe", "min"),
                  max_OOS_Sharpe=("OOS_Sharpe", "max"),
                  mean_OOS_CAGR=("OOS_CAGR", "mean"),
                  mean_OOS_MaxDD=("OOS_MaxDD", "mean"),
                  beats_SPY=("vs_SPY", lambda s: float((s > 0).mean())),
                  beats_v2=("vs_v2", lambda s: float((s > 0).mean())))
             .reset_index())
    print("\n  ALL GRID POINTS (selection instability across seeds is the whole point of "
          "the column `n_distinct_picks`):")
    print(fmt(agg))
    agg.to_csv(f"{OUT}.walkforward_agg.csv", index=False)

    HN = 40 if 40 in NGRID else max(NGRID)
    hl = agg[(agg.N == HN) & (agg.tau == 0.90)]
    if len(hl):
        h = hl.iloc[0]
        print(f"\n  HEADLINE (N={HN}, tau=0.90): {int(h.n_distinct_picks)} distinct picks over "
              f"{int(h.blocks)} seeds, modal pick chosen {h.modal_share:.0%} of the time; "
              f"OOS Sharpe {h.mean_OOS_Sharpe:.3f} +/- {h.sd_OOS_Sharpe:.3f} "
              f"(range {h.min_OOS_Sharpe:.3f}..{h.max_OOS_Sharpe:.3f}); "
              f"beats SPY {h.beats_SPY:.0%}, beats RULES v2 {h.beats_v2:.0%} of seeds")
    return W, agg, rets, m_oos, v2_oos, spy_oos


# =============================================================== 5. KEEP PATHS 4a / 4b
def keep_paths(rets, px, start, bars, v2_net):
    rule()
    print("[5] KEEP PATHS — every cell this run prices, both paths, @10 bps "
          "(full sample, halves, OOS)")
    rule()
    rows = []
    for (b, a), r in sorted(rets.items()):
        m = metrics(r)
        h1, h2 = H.halves(r)
        mo = metrics(B2.win(r, "OOS"))
        mg = H.margins(r, bars)
        rows.append(dict(book=b, arm=a, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                         MaxDD=m["MaxDD"], H1=h1, H2=h2, OOS_Sharpe=mo["Sharpe"],
                         OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                         p4a=H.pass4a(r, v2_net),
                         p4b=all(v > 0 for v in mg.values()),
                         f4b=",".join([k for k, v in mg.items() if not v > 0]) or "-"))
    K = pd.DataFrame(rows)
    print(fmt(K))
    K.to_csv(f"{OUT}.keeppaths.csv", index=False)
    print(f"\n  4a vs live RULES v2: {int(K.p4a.sum())}/{len(K)}    "
          f"4b vs SPY: {int(K.p4b.sum())}/{len(K)}")
    return K


# =============================================================== main
def main():
    t0 = time.time()
    print(__doc__)
    fx = forensics()

    rule()
    print("[1] MASTER DRAW STREAM — the calibration instrument")
    rule()
    px = H.load_universe()
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    bars = H.bars_of(spy)
    ms = metrics(spy)
    v2_net = backtest(px, rules_v2_weights(px), cost_bps=PCOST,
                      freq=H.FREQ)["returns"].loc[start:]
    mv2 = metrics(v2_net)
    print(f"  panel {px.shape[1]} names, eval {start.date()} -> {px.index[-1].date()}, "
          f"IS <= {IS_END}, OOS >= {OOS_START}")
    print(f"  SPY      {ms['CAGR']:.2%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.2%}  "
          f"halves {bars['s1']:.3f}/{bars['s2']:.3f}  OOS {bars['soos']:.3f}")
    print(f"  RULES v2 {mv2['CAGR']:.2%} / {mv2['Sharpe']:.3f} / {mv2['MaxDD']:.2%}  "
          f"halves {H.halves(v2_net)[0]:.3f}/{H.halves(v2_net)[1]:.3f}  "
          f"OOS {metrics(B2.win(v2_net, 'OOS'))['Sharpe']:.3f}")
    print(f"  drawing {M_DRAWS} sub-panels at q={Q_STAR} (master seed {MASTER_SEED}), "
          f"pricing {len(BOOKS)} books x {len(ARMS)} arms each", flush=True)
    D = master_stream(px, start)
    D.to_csv(f"{OUT}.draws.csv.gz", index=False, compression="gzip")
    print(f"  stream done: {len(D)} arm-draw rows in {time.time() - t0:.0f}s")

    reps, SP, PERM, GAP, cal = spread_analysis(D, fx)
    V, F = verdict_stability(reps)
    W, agg, rets, m_oos, v2_oos, spy_oos = walk_forward(D, reps, px, start, bars,
                                                        v2_net, spy)
    K = keep_paths(rets, px, start, bars, v2_net)

    rule()
    print("[6] VERDICT")
    rule()
    print(f"  P1 (same seed)                : {'CONFIRMED' if fx['p1'] else 'REFUTED'}")
    print(f"  P2 (gate arms agree exactly)  : {'CONFIRMED' if fx['p2'] else 'REFUTED'}")
    print(f"  P3 (exactly 0.025, 3 arms)    : {'CONFIRMED' if fx['p3'] else 'REFUTED'}")
    print(f"  H0 (path-dependence defect)   : "
          f"{'RETAINED' if cal['h0_retained'] else 'NOT RETAINED'} "
          f"(stateful cells' observed gaps do "
          f"{'' if cal['h0_retained'] else 'NOT '}exceed their own draw-noise nulls)")
    print(f"  H1 (draw noise sufficient)    : "
          f"{'SUPPORTED' if cal['contained'] and not cal['h0_retained'] else 'NOT SUFFICIENT'} "
          f"(observed max inside the null: {cal['contained']}; "
          f"mean-gap ratio observed/noise {cal['ratio']:.3f})")
    print(f"  H_amp (stateful arms noisier) : "
          f"{'YES at ' + str(list(PERM[PERM.amp_significant].N)) if PERM.amp_significant.any() else 'not significant at any N'}"
          f"  — descriptive, and the reason the queue read a path-dependence signature")
    print(f"  4a {int(K.p4a.sum())}/{len(K)}   4b {int(K.p4b.sum())}/{len(K)}")
    print(f"\n  elapsed {time.time() - t0:.0f}s")
    print(f"  wrote {STEM}.{{forensics_by_arm,forensics_rows,draws,replicates,spread_by_N,"
          f"stateful_permutation,calibration_gaps,verdict_stability,n_needed,walkforward,"
          f"walkforward_agg,keeppaths}}")


if __name__ == "__main__":
    main()
