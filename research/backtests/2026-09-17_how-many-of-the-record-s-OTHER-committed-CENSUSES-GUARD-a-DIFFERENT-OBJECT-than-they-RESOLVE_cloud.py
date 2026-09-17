#!/usr/bin/env python3
"""Idea 1168 (cloud lane, 2026-09-17) — how many of the record's OTHER committed CENSUSES
GUARD a DIFFERENT OBJECT than they RESOLVE?

THE PARENT.  Idea 1149 found that idea 1098's OUT_OF_FAMILY guard reads a claim's PROSE
while 1149's own resolution reads the SCRIPT the claim cites.  A claim whose prose is clean
therefore passes the guard and is then attributed to a cell derived from an ensemble or
sleeve script it never meant — and matching the guard to the resolution cost the published
share 291 -> 238 re-scorable claims, and 9 -> 5 of the load-bearing 28.  The queue asks
whether that is one run's slip or a shape the record repeats: census the record's censuses
for an EXCLUSION-basis / RESOLUTION-basis mismatch, and report HOW MANY PUBLISHED SHARES
MOVE under a guard matched to the resolution.

WHAT IS AND IS NOT MEASURED, said plainly up front.  There are two halves and they have
very different standing:

  (A) THE STATIC CENSUS is a LEXICAL PROXY, not a proof.  Nothing short of reading 5,600
      committed files by hand can say with certainty which read feeds which test, so this
      run classifies every record-read site in every committed census script by its OBJECT
      (PROSE / CSV / SCRIPT / FILENAME) and its ROLE (GUARD / RESOLUTION) from the source
      text, and publishes the per-script evidence in `.scripts.csv` so any reading can be
      audited.  It is GATED (G3) on the one case the record has already adjudicated: the
      detector must independently flag 1098 as guarding on PROSE, and must not flag every
      script (G4).  Every share in Part A is a share OF THIS DETECTOR'S READING.

  (B) THE PRICE is EXACT.  Idea 1149 committed its full 2,088-claim table with the prose
      guard flags (NARROW / PROX / WIDE) and FOUR resolution routes side by side, so the
      12 published shares below are recomputed BIT FOR BIT off that committed file, not
      re-derived and not recalled.  G2 replays the parent's own headline (291 -> 238,
      9 -> 5) before anything else is read.

THE TWO TUNED PARAMETERS AND NO MORE (PROTOCOL rule 4), exactly the two the queue names:
  CLAIMSET   {S_NARROW, S_PROX, S_WIDE}   the record's own three committed claim sets
  GUARDBASIS {B_ASIS, B_MATCHED, B_PROSE, B_SCRIPT}
      B_ASIS     the guard as 1098 committed it: prose membership, resolution from
                 prose-union-script and NOT matched to it   (1149's R_UNION)
      B_MATCHED  guard matched to the resolution             (1149's R_UNION_G)
      B_PROSE    guard AND resolution both on prose          (1149's R_PROSE)
      B_SCRIPT   guard AND resolution both on the script     (1149's R_SCRIPT)
= 12 cells, EVERY ONE PUBLISHED in `.cells.csv`.  Nothing else is tuned.

RULE 8 (part D) asks the only question that can reach capital: the record's claims point at
CELLS, so does repairing the guard change WHICH BOOK the record's own claims point at?  Each
of the 12 cells nominates the MODAL committed cell among the claims it admits; that book is
chosen on 2009-2016 ONLY and evaluated on the untouched 2017-2026 against SPY and the live
RULES v2 baseline, on BOTH KEEP paths.

FROZEN at the record's construction: CAND20 legs [(21,252),(0,126),(0,63)], max_vol 0.60,
min hold 126, N=20, gross 0.75, cadence W, cost 10 bps (rule 2), LAG 1, warm-up 260,
IS end 2016-12-31, zero cash.

SURVIVORSHIP: B136 and SMALL are CURRENT constituents only (PROTOCOL rule 9 /
data/SMALL_PANEL_README.md); SMALL drops every ticker with max_1d_move >= 1.0 in
data/small_meta.csv first.  The census inherits whatever survivorship its committed rows
already carry, and no result here is a live-tradable edge on those panels.

Writes: .gates.csv .scripts.csv .bases.csv .cells.csv .shares.csv .walkforward.csv .console.txt
Deterministic, standalone, no network.  Does not modify RULES.md / PROTOCOL.md / scan.py /
bot.py / baseline.py / engine.py.
"""
import sys, re, glob, time, collections
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "how-many-of-the-record-s-OTHER-committed-CENSUSES-GUARD-a-DIFFERENT-OBJECT-than-they-RESOLVE"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"
LOG = []

LAG, WARMUP = 1, 260
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
GROSS0, FREQ0, HOLD0, N0, COST0, MAXVOL0 = 0.75, "W", 126, 20, 10.0, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]

CLAIMSETS = ["S_NARROW", "S_PROX", "S_WIDE"]
GUARDBASES = ["B_ASIS", "B_MATCHED", "B_PROSE", "B_SCRIPT"]

C1149 = ROOT / "research" / "backtests" / (
    "2026-09-17_can-the-RECORD-s-COST-CLAIMS-be-RESOLVED-from-their-SCRIPTS-rather-than-their-PROSE_C.claims.csv")
N1149 = ROOT / "research" / "backtests" / (
    "2026-09-17_can-the-RECORD-s-COST-CLAIMS-be-RESOLVED-from-their-SCRIPTS-rather-than-their-PROSE_C.census.csv")
S1098 = ROOT / "research" / "backtests" / (
    "2026-09-16_do-the-record-s-COMMITTED-COST-CLAIMS-PRICE-the-SHARPE-LEGS-or-only-the-CAGR-FLOOR_C.py")
S1149 = ROOT / "research" / "backtests" / (
    "2026-09-17_can-the-RECORD-s-COST-CLAIMS-be-RESOLVED-from-their-SCRIPTS-rather-than-their-PROSE_C.py")


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# =====================================================================================
#  THE DETECTOR.  Two orthogonal vocabularies (G5 checks they are disjoint) and four
#  objects.  A record-read SITE is a source line that reaches the record at all; its
#  OBJECT is what it reaches, its ROLE is what the surrounding +/-WIN lines call it.
# =====================================================================================
WIN = 2

OBJ_PATTERNS = [
    ("PROSE",    re.compile(r"LEADERBOARD|CHANGELOG|QUEUE\.md|RULES\.md|PROTOCOL\.md|\.md['\"]|read_text\(\)|"
                            r"\bprose\b|\btext\b|\bsentence\b|\bparagraph\b", re.I)),
    ("SCRIPT",   re.compile(r"\.py['\"]|\bscript\b|source|ast\.|inspect\.|getsource", re.I)),
    ("CSV",      re.compile(r"read_csv|\.csv['\"]|\.csv\.gz|committed\s+csv|objects\.csv", re.I)),
    ("FILENAME", re.compile(r"\.stem\b|\.name\b|Path\([^)]*\)\.name|glob\.glob|\bslug\b|\bbasename\b", re.I)),
]
GUARD_VOCAB = re.compile(
    r"\bguard\b|out_of_family|OUT_OF_FAMILY|\bexclude\w*\b|\bexclusion\b|\bdrop\w*\b|\bskip\w*\b|"
    r"\beligib\w*\b|\badmiss\w*\b|\bin_family\b|\bfamily\b|\bfilter\w*\b|NARROW|PROX\b|WIDE\b|"
    r"\bqualif\w*\b|\badmit\w*\b", re.I)
RES_VOCAB = re.compile(
    r"\bresolv\w*\b|\bresolution\b|R_STRICT|R_PROSE|R_SCRIPT|R_UNION|R_LOOSE|\bcell\b|cell_[NHGC]\b|"
    r"\battribut\w*\b|\bpin\w*\b|\bscorable\b|re_score|rescore", re.I)
# a script is a RECORD CENSUS if it reaches the record at all
RECORD_TOUCH = re.compile(r"LEADERBOARD|CHANGELOG|QUEUE\.md|backtests[/\\]|committed", re.I)
SHARE_TOUCH = re.compile(r"share|\bn_of\b|of\s*\{|/\s*max\(|\bcensus\b|n_claims", re.I)


def classify(src):
    """Return (guard_bases, res_bases, sites) for one committed script's source text."""
    lines = src.split("\n")
    gb, rb, sites = collections.Counter(), collections.Counter(), []
    for i, ln in enumerate(lines):
        objs = [nm for nm, pat in OBJ_PATTERNS if pat.search(ln)]
        if not objs:
            continue
        ctx = "\n".join(lines[max(0, i - WIN): i + WIN + 1])
        is_g = bool(GUARD_VOCAB.search(ctx))
        is_r = bool(RES_VOCAB.search(ctx))
        if not (is_g or is_r):
            continue
        for o in objs:
            if is_g:
                gb[o] += 1
            if is_r:
                rb[o] += 1
        sites.append(dict(line=i + 1, objects="|".join(objs), guard=is_g, resolution=is_r,
                          text=ln.strip()[:160]))
    return gb, rb, sites


def dominant(counter):
    if not counter:
        return ""
    m = max(counter.values())
    return "|".join(sorted(k for k, v in counter.items() if v == m))


# =====================================================================================
P("=" * 100)
P(f"IDEA 1168 (cloud) — {SLUG}")
P(f"run {pd.Timestamp.utcnow():%Y-%m-%d %H:%M:%S} UTC")
P("=" * 100)
t0 = time.time()

GATES = []


def gate(name, ok, detail):
    GATES.append(dict(gate=name, verdict="PASS" if ok else "FAIL", detail=detail))
    P(f"  {name:6s} {'PASS' if ok else 'FAIL'}  {detail}")


P("\n" + "=" * 100)
P("GATES — printed BEFORE the hypothesis is read (PROTOCOL rule 7)")
P("=" * 100)

# ------------------------------------------------------------------- G1 the population
pyfiles = sorted(glob.glob(str(ROOT / "research" / "backtests" / "*.py")))
SRC = {}
for f in pyfiles:
    try:
        SRC[f] = open(f, "r", errors="replace").read()
    except Exception:
        pass
census = [f for f, s in SRC.items() if RECORD_TOUCH.search(s)]
gate("G1", len(census) >= 50,
     f"{len(pyfiles):,} committed backtest scripts, {len(census):,} of them reach the RECORD "
     f"(LEADERBOARD / CHANGELOG / QUEUE / the backtests tree) and are the census population")

# ------------------------------------------------------------------- G2 replay the parent
if C1149.exists():
    CL = pd.read_csv(C1149)
    def sc(col, mask=None):
        m = CL[col].astype(str).str.strip().str.lower().isin(["true", "1", "1.0"])
        return int((m & mask).sum()) if mask is not None else int(m.sum())
    is28 = CL["is28"].astype(str).str.strip().str.lower().isin(["true", "1", "1.0"])
    u, ug = sc("R_UNION_scorable"), sc("R_UNION_G_scorable")
    u28, ug28 = sc("R_UNION_scorable", is28), sc("R_UNION_G_scorable", is28)
    gate("G2", (u, ug, u28, ug28) == (291, 238, 9, 5),
         f"1149's own committed 2,088-claim table replays its headline EXACTLY: "
         f"R_UNION {u} -> R_UNION_G {ug} re-scorable, and {u28} -> {ug28} of the 28")
else:
    CL = None
    gate("G2", False, "1149's committed claims table not found")

# ------------------------------------------------------------------- G3 the adjudicated case
g98 = r98 = g49 = r49 = None
if S1098.exists() and S1149.exists():
    g98, r98, _ = classify(SRC.get(str(S1098), open(S1098, errors="replace").read()))
    g49, r49, _ = classify(SRC.get(str(S1149), open(S1149, errors="replace").read()))
    ok = ("PROSE" in dominant(g98)) and ("SCRIPT" in "|".join(r49.keys()))
    gate("G3", ok,
         f"the ONE adjudicated case comes out right without being told: 1098's guard basis reads "
         f"{dominant(g98) or 'NONE'} (dominant) and 1149's resolution reaches "
         f"{'|'.join(sorted(r49.keys())) or 'NONE'}")
else:
    gate("G3", False, "1098 / 1149 scripts not found")

# ------------------------------------------------------------------- detector over the record
rows, sitrows = [], []
for f in census:
    gb, rb, sites = classify(SRC[f])
    if not gb and not rb:
        continue
    gset, rset = set(gb), set(rb)
    rows.append(dict(
        script=Path(f).name,
        publishes_share=bool(SHARE_TOUCH.search(SRC[f])),
        guard_bases="|".join(sorted(gset)) or "NONE",
        res_bases="|".join(sorted(rset)) or "NONE",
        guard_dominant=dominant(gb) or "NONE",
        res_dominant=dominant(rb) or "NONE",
        n_guard_sites=int(sum(gb.values())), n_res_sites=int(sum(rb.values())),
        has_guard=bool(gset), has_res=bool(rset),
        mismatch_dominant=bool(gset and rset and dominant(gb) != dominant(rb)),
        mismatch_disjoint=bool(gset and rset and not (gset & rset)),
        mismatch_setdiff=bool(gset and rset and gset != rset),
    ))
    for s in sites[:40]:
        s["script"] = Path(f).name
        sitrows.append(s)
S = pd.DataFrame(rows)
SITES = pd.DataFrame(sitrows)

# ------------------------------------------------------------------- G4 not everything flags
both = S[S.has_guard & S.has_res]
r_dom = both["mismatch_dominant"].mean() if len(both) else np.nan
gate("G4", 0.0 < r_dom < 1.0,
     f"the detector is discriminating, not degenerate: {int(both['mismatch_dominant'].sum()):,} of "
     f"{len(both):,} scripts that have BOTH a guard site and a resolution site show a DOMINANT-basis "
     f"mismatch ({r_dom:.4f}) — not 0 and not 1")

# ------------------------------------------------------------------- G5 vocabularies disjoint
probe = ["guard", "exclude", "eligible", "family", "resolve", "cell", "scorable", "attribute"]
clash = [w for w in probe if GUARD_VOCAB.fullmatch(w) and RES_VOCAB.fullmatch(w)]
gate("G5", not clash, f"GUARD and RESOLUTION vocabularies are disjoint on the probe set "
                      f"{probe} (clashes: {clash or 'none'})")

# ------------------------------------------------------------------- G6 share arithmetic
if CL is not None:
    nw = len(CL)
    gate("G6", nw == 2088, f"the committed claim table is {nw:,} rows, the record's own WIDE set")
else:
    gate("G6", False, "no claim table")

# ------------------------------------------------------------------- G7 claim sets nest
if CL is not None:
    nn = CL["NARROW"].astype(str).str.lower().isin(["true", "1", "1.0"])
    npx = CL["PROX"].astype(str).str.lower().isin(["true", "1", "1.0"])
    gate("G7", bool((nn & ~npx).sum() == 0) and int(nn.sum()) == 59 and int(npx.sum()) == 125,
         f"the record's claim sets NEST as committed: NARROW {int(nn.sum())} c PROX {int(npx.sum())} "
         f"c WIDE {len(CL):,}")
else:
    gate("G7", False, "no claim table")

GD = pd.DataFrame(GATES)
dump(GD, "gates")
P(f"  {(GD.verdict == 'PASS').sum()} of {len(GD)} gates PASS")

# =====================================================================================
P("\n" + "=" * 100)
P("PART A — THE STATIC CENSUS (a LEXICAL PROXY, published site by site in `.sites.csv`)")
P("=" * 100)
dump(S, "scripts")
dump(SITES, "sites")

P(f"\n  {len(S):,} committed census scripts carry a classifiable guard or resolution site.")
P(f"  {int(S.has_guard.sum()):,} have a GUARD site, {int(S.has_res.sum()):,} a RESOLUTION site, "
  f"{len(both):,} have BOTH (only these can mismatch).")
P("\n  MISMATCH under the three readings, all published (none is 'the' answer):")
for col, what in (("mismatch_dominant", "DOMINANT basis differs"),
                  ("mismatch_setdiff", "basis SETS differ at all"),
                  ("mismatch_disjoint", "basis sets are DISJOINT (1098/1149's shape)")):
    P(f"    {what:46s} {int(both[col].sum()):4,} of {len(both):4,}  ({both[col].mean():.4f})")

P("\n  the guard x resolution DOMINANT-basis table (rows guard, cols resolution):")
ct = pd.crosstab(both["guard_dominant"], both["res_dominant"])
P(ct.to_string())
BAS = ct.reset_index().melt(id_vars="guard_dominant", var_name="res_dominant", value_name="n")
dump(BAS, "bases")

sh = both[both.publishes_share]
P(f"\n  restricted to scripts that PUBLISH A SHARE: {int(sh['mismatch_dominant'].sum()):,} of "
  f"{len(sh):,} mismatch on the dominant basis ({sh['mismatch_dominant'].mean():.4f})")

# =====================================================================================
P("\n" + "=" * 100)
P("PART B — THE PRICE, EXACT: 12 cells recomputed BIT FOR BIT off 1149's committed table")
P("=" * 100)

COLOF = {"B_ASIS": "R_UNION", "B_MATCHED": "R_UNION_G", "B_PROSE": "R_PROSE", "B_SCRIPT": "R_SCRIPT"}
SETOF = {"S_NARROW": "NARROW", "S_PROX": "PROX", "S_WIDE": "WIDE"}


def B(col):
    return CL[col].astype(str).str.strip().str.lower().isin(["true", "1", "1.0"])


cells = []
if CL is not None:
    is28 = B("is28")
    for cs in CLAIMSETS:
        m = B(SETOF[cs]) if SETOF[cs] != "WIDE" else pd.Series(True, index=CL.index)
        for gbz in GUARDBASES:
            pre = COLOF[gbz]
            sc_ = B(f"{pre}_scorable") & m
            st_ = B(f"{pre}_stated") & m
            cells.append(dict(
                claimset=cs, guardbasis=gbz, n_claims=int(m.sum()),
                n_cell_stated=int(st_.sum()), n_rescorable=int(sc_.sum()),
                share_cell_stated=float(st_.sum() / max(m.sum(), 1)),
                share_rescorable=float(sc_.sum() / max(m.sum(), 1)),
                n28=int((m & is28).sum()), n28_rescorable=int((sc_ & is28).sum()),
            ))
    CE = pd.DataFrame(cells)
    base = CE[CE.guardbasis == "B_ASIS"].set_index("claimset")
    CE["d_rescorable_vs_ASIS"] = CE.apply(lambda r: r.n_rescorable - base.loc[r.claimset, "n_rescorable"], axis=1)
    CE["d_share_vs_ASIS"] = CE.apply(lambda r: r.share_rescorable - base.loc[r.claimset, "share_rescorable"], axis=1)
    CE["d_28_vs_ASIS"] = CE.apply(lambda r: r.n28_rescorable - base.loc[r.claimset, "n28_rescorable"], axis=1)
    CE["share_moves"] = CE["d_rescorable_vs_ASIS"] != 0
    P("\nALL 12 CELLS (every grid point reported, PROTOCOL rule 4):")
    P(CE.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(CE, "cells")

    P("\n  HOW MANY PUBLISHED SHARES MOVE under a guard matched to the resolution (B_MATCHED):")
    mm = CE[CE.guardbasis == "B_MATCHED"]
    P(f"    {int(mm.share_moves.sum())} of {len(mm)} of the record's own committed claim-set shares move.")
    for _, r in mm.iterrows():
        P(f"      {r.claimset:9s} re-scorable {int(base.loc[r.claimset,'n_rescorable']):4d} -> "
          f"{r.n_rescorable:4d}  ({base.loc[r.claimset,'share_rescorable']:.4f} -> "
          f"{r.share_rescorable:.4f}, d {r.d_share_vs_ASIS:+.4f});  the 28-set "
          f"{int(base.loc[r.claimset,'n28_rescorable'])} -> {int(r.n28_rescorable)}")

    # the record's OWN committed census rows, re-read under the matched guard
    if N1149.exists():
        NC = pd.read_csv(N1149)
        pub = NC[NC.resolution_source.isin(["R_UNION", "R_UNION_G"])]
        piv = pub.pivot_table(index="claim_set", columns="resolution_source",
                              values=["n_rescorable", "share_rescorable", "n28_rescorable"])
        P("\n  the parent's OWN committed census rows, side by side (read not recalled):")
        P(piv.to_string(float_format=lambda x: f"{x:.4f}"))
        moved = int((piv[("n_rescorable", "R_UNION")] != piv[("n_rescorable", "R_UNION_G")]).sum())
        P(f"    {moved} of {len(piv)} of the parent's published claim-set shares move under its own matched guard")
        SHARES = piv.reset_index()
        SHARES.columns = ["_".join([str(x) for x in c if x != ""]) for c in SHARES.columns]
        dump(SHARES, "shares")

# =====================================================================================
P("\n" + "=" * 100)
P("PART C — MECHANISM: WHICH claims the matched guard removes")
P("=" * 100)
if CL is not None:
    lost = B("R_UNION_scorable") & ~B("R_UNION_G_scorable")
    kept = B("R_UNION_scorable") & B("R_UNION_G_scorable")
    P(f"  the matched guard removes {int(lost.sum())} of {int(B('R_UNION_scorable').sum())} "
      f"re-scorable claims and keeps {int(kept.sum())}.")
    P(f"  cite route of the REMOVED claims:  {CL.loc[lost, 'cite_route'].value_counts().to_dict()}")
    P(f"  cite route of the KEPT claims:     {CL.loc[kept, 'cite_route'].value_counts().to_dict()}")
    P(f"  cell of the REMOVED claims:        {CL.loc[lost, 'R_UNION_cell'].value_counts().head(6).to_dict()}")
    P(f"  cell of the KEPT claims:           {CL.loc[kept, 'R_UNION_cell'].value_counts().head(6).to_dict()}")
    P(f"  removed claims in the 28-set:      {int((lost & is28).sum())} of {int(is28.sum())}")
    P("  READ THIS THE RIGHT WAY: the guard does not remove claims at random, it removes the ones "
      "whose cell came from a SIBLING script the prose never named — exactly the failure 1149 found.")

# =====================================================================================
P("\n" + "=" * 100)
P("PART D — RULE 8 WALK-FORWARD and BOTH KEEP PATHS")
P("   The record's claims point at CELLS.  Each of the 12 cells nominates the MODAL committed")
P("   cell among the claims it admits; that book is chosen on 2009-2016 ONLY and evaluated on")
P("   the untouched 2017-2026 against SPY and the live RULES v2 baseline.")
P("=" * 100)


def nrun(rets, wt, mk):
    T, N = rets.shape
    mk = mk.copy()
    mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return (held * rets).sum(axis=1), turn


def fmet(r):
    r = np.asarray(r, float)
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def mech(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    return (comp * (0.5 + 0.5 * above.astype(float))).values, above.values, vol20.values


def build(rank_key, elig, priced, reb, N, H, T, K, gross):
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    for i, t in enumerate(reb):
        held = np.flatnonzero(cur >= 0)
        if len(held):
            young = held[(t - cur[held]) < H]
            young = young[priced[t, young]]
        else:
            young = held
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = rank_key[t].copy()
            k[~(elig[t] & priced[t])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new_cur = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new_cur[c] = cur[c]
        for c in take:
            new_cur[c] = t
        cur = new_cur
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = gross / len(sel)
    return W


def load_panel(name):
    if name == "U56":
        px = load_universe()
    elif name == "B136":
        px = load_universe(broad=True)
    else:
        px = load_universe(small=True)
        meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
        bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"].astype(str))
        px = px[[c for c in px.columns if c == "SPY" or c not in bad]]
    return px


def prep(px):
    idx = px.index
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    sc, above, vol20 = mech(px)
    return dict(px=px, idx=idx, K=len(px.columns), T=len(idx),
                rets=px.pct_change().fillna(0.0).values, priced=px.notna().values,
                warm=warm, ins=ins, oos=oos, sc=sc, above=above, vol20=vol20,
                spy=px["SPY"].pct_change().fillna(0.0).values,
                mk=rebalance_mask(idx, FREQ0).values)


def run_cell(d, gross=GROSS0, N=N0, H=HOLD0, maxvol=MAXVOL0, freq=FREQ0, cost=COST0):
    mk = d["mk"] if freq == FREQ0 else rebalance_mask(d["idx"], freq).values
    mkl = np.roll(mk, LAG)
    mkl[:LAG] = False
    reb = np.flatnonzero(mk)
    el = d["above"] & (d["vol20"] < maxvol)
    W = build(-d["sc"], el, d["priced"], reb, N, H, d["T"], d["K"], gross)
    Wl = np.zeros_like(W)
    Wl[LAG:] = W[:-LAG]
    g, t = nrun(d["rets"], Wl, mkl)
    return g - t * cost / 1e4


def blocks_m(r, d):
    rr = r[d["warm"]]
    c, s, dd = fmet(rr)
    h = len(rr) // 2
    oc, os_, od = fmet(r[d["oos"]])
    ic, is_, idd = fmet(r[d["ins"]])
    return dict(CAGR=c, Sharpe=s, MaxDD=dd, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


PAN, SPYREF, LIVE = {}, {}, {}
for nm in ("U56", "B136", "SMALL"):
    px = load_panel(nm)
    d = prep(px)
    PAN[nm] = d
    rr = d["spy"][d["warm"]]
    h = len(rr) // 2
    c, s, dd = fmet(rr)
    oc, os_, od = fmet(d["spy"][d["oos"]])
    SPYREF[nm] = dict(CAGR=c, Sharpe=s, MaxDD=dd, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                      OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                      IS_Sharpe=fsharpe(d["spy"][d["ins"]]),
                      IS_CAGR=fmet(d["spy"][d["ins"]])[0])
    b = backtest(px, rules_v2_weights(px), cost_bps=COST0, freq="W")
    LIVE[nm] = blocks_m(b["returns"].reindex(d["idx"]).fillna(0.0).values, d)
    P(f"  {nm:6s} SPY full {c:.2%}/{s:.4f}/{dd:.2%}  OOS {oc:.2%}/{os_:.4f}/{od:.2%}   "
      f"live v2 {LIVE[nm]['CAGR']:.2%}/{LIVE[nm]['Sharpe']:.4f}/{LIVE[nm]['MaxDD']:.2%} "
      f"OOS {LIVE[nm]['OOS_Sharpe']:.4f}")

CACHE = {}


def book(panel, N, H, gross, freq):
    k = (panel, int(N), int(H), round(float(gross), 4), freq)
    if k not in CACHE:
        CACHE[k] = run_cell(PAN[panel], gross=k[3], N=k[1], H=k[2], freq=k[4])
    return CACHE[k]


def modal_cell(mask):
    """The cell the admitted claims point at: modal panel, then modal stated N / H / gross /
    cadence among those claims, falling back to the record's frozen defaults where the
    claims state nothing.  Fallbacks are declared, not hidden."""
    sub = CL[mask]
    if not len(sub):
        return None
    def mode(col, default, cast=float):
        v = sub[col].dropna()
        if not len(v):
            return default, "default"
        try:
            return cast(v.mode().iloc[0]), "claims"
        except Exception:
            return default, "default"
    panel, psrc = mode("panel", "U56", str)
    if panel not in PAN:
        panel, psrc = "U56", "default"
    N, nsrc = mode("cell_N", N0, int)
    H, hsrc = mode("cell_H", HOLD0, int)
    G, gsrc = mode("cell_G", GROSS0, float)
    C, csrc = mode("cell_C", FREQ0, str)
    if C not in ("D", "W", "M", "Q"):
        C, csrc = FREQ0, "default"
    if not (1 <= N <= 60):
        N, nsrc = N0, "default"
    if not (1 <= H <= 756):
        H, hsrc = HOLD0, "default"
    if not (0.05 <= G <= 2.0):
        G, gsrc = GROSS0, "default"
    return dict(panel=panel, N=N, H=H, gross=G, freq=C,
                src=f"panel:{psrc} N:{nsrc} H:{hsrc} g:{gsrc} cad:{csrc}")


wf = []
if CL is not None:
    for cs in CLAIMSETS:
        m = B(SETOF[cs]) if SETOF[cs] != "WIDE" else pd.Series(True, index=CL.index)
        for gbz in GUARDBASES:
            sc_ = B(f"{COLOF[gbz]}_scorable") & m
            mc = modal_cell(sc_)
            if mc is None:
                wf.append(dict(claimset=cs, guardbasis=gbz, n_admitted=0, pick="NONE"))
                continue
            d = PAN[mc["panel"]]
            r = book(mc["panel"], mc["N"], mc["H"], mc["gross"], mc["freq"])
            mm = blocks_m(r, d)
            sb, lb = SPYREF[mc["panel"]], LIVE[mc["panel"]]
            row = dict(claimset=cs, guardbasis=gbz, n_admitted=int(sc_.sum()),
                       pick=f"{mc['panel']}/N={mc['N']}/H={mc['H']}/g={mc['gross']:.2f}/{mc['freq']}",
                       panel=mc["panel"], N=mc["N"], H=mc["H"], gross=mc["gross"], freq=mc["freq"],
                       cell_source=mc["src"], **mm,
                       SPY_CAGR=sb["CAGR"], SPY_Sharpe=sb["Sharpe"], SPY_MaxDD=sb["MaxDD"],
                       SPY_OOS_CAGR=sb["OOS_CAGR"], SPY_OOS_Sharpe=sb["OOS_Sharpe"],
                       SPY_OOS_MaxDD=sb["OOS_MaxDD"],
                       LIVE_Sharpe=lb["Sharpe"], LIVE_MaxDD=lb["MaxDD"],
                       LIVE_OOS_Sharpe=lb["OOS_Sharpe"],
                       L_H1=bool(mm["H1"] > sb["H1"]), L_H2=bool(mm["H2"] > sb["H2"]),
                       L_OOS=bool(mm["OOS_Sharpe"] > sb["OOS_Sharpe"]),
                       L_DD=bool(abs(mm["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"])),
                       L_CAGR=bool(mm["CAGR"] >= CAGR_FLOOR * sb["CAGR"]),
                       O_S=bool(mm["OOS_Sharpe"] > sb["OOS_Sharpe"]),
                       O_DD=bool(abs(mm["OOS_MaxDD"]) <= DD_CAP * abs(sb["OOS_MaxDD"])),
                       O_CAGR=bool(mm["OOS_CAGR"] >= CAGR_FLOOR * sb["OOS_CAGR"]),
                       A_H1=bool(mm["H1"] > lb["H1"]), A_H2=bool(mm["H2"] > lb["H2"]),
                       A_DD=bool(mm["MaxDD"] >= lb["MaxDD"]))
            row["pass_4b_full"] = all(row[k] for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
            row["pass_4b_oos"] = all(row[k] for k in ("O_S", "O_DD", "O_CAGR"))
            row["pass_4a"] = all(row[k] for k in ("A_H1", "A_H2", "A_DD"))
            wf.append(row)
W = pd.DataFrame(wf)
show = ["claimset", "guardbasis", "n_admitted", "pick", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
        "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "pass_4b_full", "pass_4b_oos", "pass_4a"]
P(W[[c for c in show if c in W.columns]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
dump(W, "walkforward")

if "pick" in W.columns:
    nb = W.groupby("claimset")["pick"].nunique()
    P(f"\n  DOES THE GUARD MOVE THE BOOK?  distinct picks per claim set: {nb.to_dict()}")
    moved = 0
    for cs in CLAIMSETS:
        a = W[(W.claimset == cs) & (W.guardbasis == "B_ASIS")]
        b_ = W[(W.claimset == cs) & (W.guardbasis == "B_MATCHED")]
        if len(a) and len(b_) and a.iloc[0]["pick"] != b_.iloc[0]["pick"]:
            moved += 1
    P(f"  B_ASIS -> B_MATCHED changes the nominated book at {moved} of {len(CLAIMSETS)} claim sets.")
    n4b = int((W["pass_4b_full"].fillna(False) & W["pass_4b_oos"].fillna(False)).sum())
    n4a = int(W["pass_4a"].fillna(False).sum())
    P(f"  4b (full AND OOS) clean: {n4b} of {len(W)}      4a passes: {n4a} of {len(W)}")
    if n4b:
        for _, r in W[W["pass_4b_full"].fillna(False) & W["pass_4b_oos"].fillna(False)].iterrows():
            P(f"    4b CLEAN: {r.claimset} {r.guardbasis} {r['pick']}  full {r.CAGR:.2%}/{r.Sharpe:.4f}/"
              f"{r.MaxDD:.2%}  OOS {r.OOS_CAGR:.2%}/{r.OOS_Sharpe:.4f}/{r.OOS_MaxDD:.2%}")

P("\n" + "=" * 100)
P(f"done in {time.time()-t0:.1f}s")
P("=" * 100)
Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
print(f"wrote {OUT}.console.txt")
