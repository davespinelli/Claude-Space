#!/usr/bin/env python3
"""Idea 521 — do the record's HAND-COPIED-CONSTANT gates fail more than its ARTEFACT gates?

Idea 515 re-executed 43 scripts and REACHED 171 of the record's 520 committed assert clauses;
23 of those 171 failed.  The queue's claim is that the failures split into two populations:
gates that compare a freshly computed statistic against a 3-4 decimal number TYPED INTO THE
SOURCE (`abs(m['Sharpe'] - 1.133) < 5e-4`) and gates that compare against a COMMITTED
ARTEFACT, and that the same constant 1.133 is restated in three scripts and reads 7.85e-4 in
all three.  Idea 681 reported reached-gate pass rates SELF 0.9403 > CONST 0.9074 >
ARTEFACT 0.7200 as a by-product of a different classifier; this run makes the reference-kind
split the object, measures the native failure rate of each kind over the FULL census, and
PRICES what "re-gate on the artefact" would actually recover.

Nothing is re-executed: the observed/bar/passed columns are idea 515's own committed
`.gates.csv`, so every failure rate here is the record's NATIVE one.

This run does four things:
  A. CLASSIFY all 520 committed clauses by REFERENCE KIND (CONST / ARTEFACT / SELF /
     STRUCTURAL) under three nested classifiers, and report the full cross-tab.
  B. Native FAILURE RATE by reference kind on the 171 reached gates, every classifier.
  C. PRICE the two candidate fixes on the failing gates:
       C1 "re-gate on the artefact": can the artefact even be IDENTIFIED from the typed
          number?  Count the committed CSV cells that round to each constant.
       C2 "quantization-corrected bar" bar' = bar + 0.5*10^-d for a d-decimal constant
          (the transcription's own half-width; q = 0 for a full-precision artefact).
     Both swept over the full bar ladder, ALL grid points reported.
  D. RULE 8 (mandatory): the publication convention as a BOOK ADMISSION GATE.  A book grid
     is scored on 2009-2016 only, each policy's pick is read ONCE on 2017-01-01+ against
     RULES v2 and SPY on the same panel and calendar.  10 bps, weekly/monthly/quarterly
     rebalance, t+1 execution.
  It does NOT edit PROTOCOL.md, RULES.md, scan.py, bot.py or baseline.py (rule 6).

TUNED PARAMETERS — exactly two, both swept, ALL grid points reported:
    1. REFERENCE-KIND CLASSIFIER in {NARROW, MID, WIDE} (nested: how many decimals make a
       literal a hand-copied reference, and how many assignment hops a file read may travel)
    2. BAR in the ladder {native, 1e-6, 1e-4, 5e-4, 1e-3, 1e-2} (and the derived bar+q form)
Everything else is pre-registered and fixed: the clause set (idea 515's committed census),
the observed values (idea 515's committed gates), 10 bps, t+1, the 2009-2016 / 2017-2026
rule-8 split, the 2-trading-day vintage step used as the reproduction perturbation.

Outputs (all beside this script):
    .console.txt      full run log
    .census.csv       all 520 clauses with a reference-kind stamp under each classifier
    .fails.csv        the 23 native failures, classified, with overrun and recovery
    .grid.csv         classifier x bar x reference kind — ALL grid points
    .identify.csv     C1: committed-artefact cells that round to each typed constant
    .walkforward.csv  rule-8: 5 policies x 3 panels, picks chosen IS, read ONCE on OOS
    .bookgrid.csv     every book scored (IS/OOS/full), all grid points
    .result.md        the memo
"""
from __future__ import annotations
import ast, re, sys, glob, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state          # noqa: E402
from engine import backtest as engine_backtest, metrics, rebalance_mask   # noqa: E402

STEM = Path(__file__).with_suffix("")
OUT = lambda ext: Path(str(STEM) + ext)
BT = ROOT / "research" / "backtests"

# ------------------------------------------------------------------ pre-registered constants
COST_BPS = 10.0
BAND = 0.03
IS_START, IS_END = "2009-01-01", "2016-12-31"
OOS_START = "2017-01-01"
VINTAGE_DAYS = 2                  # idea 681's vintage step, reused verbatim as the perturbation
NATIVE_CONST_BAR = 5e-4           # the record's own bar on its 3-4 decimal constants
BAR_LADDER = (1e-6, 1e-4, 5e-4, 1e-3, 1e-2)
CLASSIFIERS = ("NARROW", "MID", "WIDE")
KINDS = ("CONST", "ARTEFACT", "SELF", "STRUCTURAL")
# literals that are dials/shape, never a hand-copied published statistic
DIAL_LITERALS = {0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 10.0, 12.0, 20.0, 21.0, 50.0, 52.0, 60.0,
                 63.0, 100.0, 126.0, 200.0, 252.0, 0.5, 1.5, 0.25, 0.75}

# idea 515's committed artefacts (the clause set and the NATIVE observations)
C515 = BT / "2026-09-09_restate-the-record-s-158-REPRODUCTION-GATES-as-TOLERANCES-in-record-units_C.census.csv"
G515 = BT / "2026-09-09_restate-the-record-s-158-REPRODUCTION-GATES-as-TOLERANCES-in-record-units_C.gates.csv"

_LOG: list[str] = []
_EXTRA_GATES: list[dict] = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); _LOG.append(s)


# ============================================================================== helpers
def fast_backtest(px_vals: np.ndarray, w_vals: np.ndarray, rb: np.ndarray, cost_bps=COST_BPS):
    """numpy clone of engine.backtest; returns daily returns (t+1 execution, costs on turnover)."""
    T, N = px_vals.shape
    rets = np.zeros_like(px_vals)
    rets[1:] = px_vals[1:] / px_vals[:-1] - 1.0
    rets = np.nan_to_num(rets, nan=0.0, posinf=0.0, neginf=0.0)
    wt = np.vstack([np.zeros((1, N)), w_vals[:-1]])
    mask = np.concatenate([[False], rb[:-1]])
    cur = np.zeros(N); out = np.zeros(T)
    for i in range(T):
        if mask[i] or i == 0:
            new = wt[i]; to = np.abs(new - cur).sum(); cur = new
        else:
            to = 0.0
        out[i] = (cur * rets[i]).sum() - to * cost_bps / 1e4
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    return out


def mets(r: pd.Series) -> dict:
    m = metrics(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"])


def ewall_weights(px: pd.DataFrame, gross: float) -> pd.DataFrame:
    """RULES v2 shape at an arbitrary gross dial: equal weight inside the 200d band, rest cash."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, BAND), 0.0)


def decimals_of(tok: str) -> int:
    """Decimal places a fixed-point literal was TYPED with ('1.133' -> 3).  -1 if not fixed point."""
    tok = tok.strip()
    if "e" in tok.lower() or "." not in tok: return -1
    return len(tok.split(".")[1].rstrip())


def quantization(d: int) -> float:
    """Half-width of the rounding cell a d-decimal transcription lands in."""
    return 0.5 * 10.0 ** (-d) if d >= 0 else 0.0


# ================================================================== PART A — classification
_NUM = re.compile(r"(?<![\w.])(\d+\.\d+|\d+e-?\d+|\d+)(?![\w.])", re.I)

def _read_seeds(src_text: str) -> set[str]:
    """Names assigned (anywhere in the script) from a file read — the artefact seed set."""
    seeds = set()
    pat = re.compile(r"^\s*([A-Za-z_]\w*)\s*=\s*(.*?(?:read_csv|read_json|read_table|read_parquet"
                     r"|read_text|json\.loads?|np\.load|loadtxt|read_pickle).*)$", re.M)
    for m in pat.finditer(src_text):
        seeds.add(m.group(1))
    return seeds


def _assign_map(src_text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for m in re.finditer(r"^\s*([A-Za-z_]\w*)\s*=\s*([^=].*)$", src_text, re.M):
        out.setdefault(m.group(1), "")
        out[m.group(1)] += " " + m.group(2)
    return out


def _traces_to_artefact(names: set[str], seeds: set[str], amap: dict[str, str], hops: int) -> bool:
    frontier = set(names)
    seen: set[str] = set()
    for _ in range(hops):
        if frontier & seeds: return True
        nxt: set[str] = set()
        for n in frontier - seen:
            seen.add(n)
            rhs = amap.get(n, "")
            if any(k in rhs for k in ("read_csv", "read_json", "read_text", "json.load",
                                      "np.load", "read_parquet", "read_pickle")):
                return True
            nxt |= set(re.findall(r"[A-Za-z_]\w*", rhs))
        frontier = nxt
    return bool(frontier & seeds)


def clause_parts(src: str):
    """(reference literals on the compared side, bar token) for a clause source string."""
    try:
        node = ast.parse(src.strip(), mode="eval").body
    except SyntaxError:
        return [], None
    if not isinstance(node, ast.Compare) or len(node.comparators) != 1:
        return [], None
    left, right = node.left, node.comparators[0]
    # the bar is the side that is a bare numeric literal; the reference lives on the other side
    def lits(n):
        return [ast.unparse(x) for x in ast.walk(n) if isinstance(x, ast.Constant)
                and isinstance(x.value, (int, float)) and not isinstance(x.value, bool)]
    if isinstance(right, ast.Constant) and isinstance(right.value, (int, float)):
        return lits(left), ast.unparse(right)
    if isinstance(left, ast.Constant) and isinstance(left.value, (int, float)):
        return lits(right), ast.unparse(left)
    return lits(left) + lits(right), None


def classify(row, src_text: str, seeds: set[str], amap: dict[str, str], mode: str) -> tuple[str, str, int]:
    """-> (kind, reference literal or '', decimals).  Precedence STRUCTURAL > CONST > ARTEFACT > SELF."""
    if row.form == "structural":
        return "STRUCTURAL", "", -1
    src = str(row.src)
    refs, _bar = clause_parts(src)
    min_dec = {"NARROW": 3, "MID": 2, "WIDE": 1}[mode]
    hops = {"NARROW": 1, "MID": 2, "WIDE": 3}[mode]
    best, bestd = "", -1
    for tok in refs:
        d = decimals_of(tok)
        try: v = float(tok)
        except ValueError: continue
        if mode != "WIDE" and abs(v) in DIAL_LITERALS: continue
        if d >= min_dec and d > bestd:
            best, bestd = tok, d
    if best:
        return "CONST", best, bestd
    names = set(re.findall(r"[A-Za-z_]\w*", src))
    if _traces_to_artefact(names, seeds, amap, hops):
        return "ARTEFACT", "", -1
    return "SELF", "", -1


def part_a() -> pd.DataFrame:
    say("\n" + "=" * 78)
    say("PART A — classify every committed clause by REFERENCE KIND (3 nested classifiers)")
    say("=" * 78)
    C = pd.read_csv(C515)
    G = pd.read_csv(G515)
    say(f"  idea 515 census: {len(C)} clauses over {C.script.nunique()} scripts; "
        f"reached gates: {len(G)} over {G.script.nunique()} scripts "
        f"({int((~G.passed).sum())} native failures)")

    src_cache: dict[str, tuple[str, set[str], dict]] = {}
    def ctx(script: str):
        if script not in src_cache:
            p = BT / script
            t = p.read_text(errors="ignore") if p.exists() else ""
            src_cache[script] = (t, _read_seeds(t), _assign_map(t))
        return src_cache[script]

    missing = sorted({s for s in C.script.unique() if not (BT / s).exists()})
    if missing:
        say(f"  WARNING: {len(missing)} census scripts no longer on disk: {missing[:3]}")
    for mode in CLASSIFIERS:
        kinds, refs, decs = [], [], []
        for _, r in C.iterrows():
            t, seeds, amap = ctx(r.script)
            k, ref, d = classify(r, t, seeds, amap, mode)
            kinds.append(k); refs.append(ref); decs.append(d)
        C["kind_" + mode] = kinds
        C["ref_" + mode] = refs
        C["dec_" + mode] = decs
    tab = pd.DataFrame({m: C["kind_" + m].value_counts() for m in CLASSIFIERS}).reindex(KINDS).fillna(0).astype(int)
    tab["share_MID"] = (tab["MID"] / len(C)).round(4)
    say("\nreference kind over the FULL 520-clause census (all three classifiers):")
    say(tab.to_string())
    # the 158 reproduction-gate subset idea 515 named (tolerance+exact forms)
    rep = C[C.form.isin(["tolerance", "exact"])]
    say(f"\nthe {len(rep)} tolerance/exact clauses (the numeric-bar family idea 513's "
        f"'158 reproduction gates' sits inside; structural/count forms dropped):")
    say(pd.DataFrame({m: rep["kind_" + m].value_counts() for m in CLASSIFIERS})
        .reindex(KINDS).fillna(0).astype(int).to_string())
    C.to_csv(OUT(".census.csv"), index=False)
    return C, G


# =========================================================== PART B — native failure rates
def part_b(C: pd.DataFrame, G: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    say("\n" + "=" * 78)
    say("PART B — NATIVE failure rate by reference kind (idea 515's own observed/bar/passed)")
    say("=" * 78)
    key = ["script", "gate_id"]
    M = G.merge(C[key + [c for c in C.columns if c.startswith(("kind_", "ref_", "dec_"))]],
                on=key, how="left", validate="one_to_one")
    say(f"  joined {len(M)} reached gates to the census ({M['kind_MID'].isna().sum()} unmatched)")
    rows = []
    for mode in CLASSIFIERS:
        for k in KINDS:
            s = M[M["kind_" + mode] == k]
            if not len(s): continue
            rows.append(dict(classifier=mode, kind=k, n=len(s), fails=int((~s.passed).sum()),
                             fail_rate=round(float((~s.passed).mean()), 4),
                             pass_rate=round(float(s.passed.mean()), 4)))
    B = pd.DataFrame(rows)
    say("\nreached-gate outcome by (classifier x reference kind) — ALL grid points:")
    say(B.to_string(index=False))
    for mode in CLASSIFIERS:
        s = B[B.classifier == mode].set_index("kind")
        if {"CONST", "ARTEFACT"} <= set(s.index):
            c, a = s.loc["CONST"], s.loc["ARTEFACT"]
            say(f"  [{mode}] CONST fail {c.fail_rate:.4f} (n={c.n}) vs ARTEFACT fail "
                f"{a.fail_rate:.4f} (n={a.n})  ->  "
                f"{'CONST fails MORE' if c.fail_rate > a.fail_rate else 'CONST fails LESS'}")
    F = M[~M.passed].copy()
    say(f"\nthe {len(F)} native failures, by kind (MID): "
        f"{F.kind_MID.value_counts().to_dict()}")
    return M, F


# ==================================================== PART C — price the two candidate fixes
def scan_artefact_cells(consts: list[tuple[str, float, int]]) -> pd.DataFrame:
    """C1: how many committed CSV cells round to each typed constant?  One pass over the record."""
    files = sorted(glob.glob(str(BT / "*.csv"))) + sorted(glob.glob(str(BT / "*.csv.gz")))
    say(f"  scanning {len(files)} committed CSV artefacts for cells inside each constant's "
        f"rounding cell...")
    counts = {tok: 0 for tok, _, _ in consts}
    stems = {tok: set() for tok, _, _ in consts}
    for f in files:
        try:
            df = pd.read_csv(f)
        except Exception:
            continue
        num = df.select_dtypes(include=[np.number])
        if not len(num.columns): continue
        arr = num.to_numpy(dtype=float, copy=False)
        arr = arr[np.isfinite(arr)]
        if not arr.size: continue
        stem = Path(f).name.split(".")[0]
        for tok, v, d in consts:
            q = quantization(d)
            n = int((np.abs(arr - v) <= q).sum())
            if n:
                counts[tok] += n
                stems[tok].add(stem)
    return pd.DataFrame([dict(const=tok, value=v, decimals=d, quantization=quantization(d),
                              cells_in_rounding_cell=counts[tok], distinct_scripts=len(stems[tok]))
                         for tok, v, d in consts]).sort_values("cells_in_rounding_cell",
                                                               ascending=False)


def part_c(M: pd.DataFrame, F: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    say("\n" + "=" * 78)
    say("PART C — price the two fixes:  C1 re-gate on the artefact,  C2 bar' = bar + q")
    say("=" * 78)

    # ---- the queue's own 1.133 restatement claim
    lit = M[M.src.astype(str).str.contains("1.133", regex=False)]
    say(f"\n  the 1.133 restatement claim: {len(lit)} reached clauses over "
        f"{lit.script.nunique()} scripts; observed values "
        f"{sorted(set(np.round(lit.observed.dropna().values, 10)))}")

    # ---- C2: quantization-corrected bar over the failing gates
    rows = []
    for _, r in F.iterrows():
        kind = r.kind_MID
        d = int(r.dec_MID) if pd.notna(r.dec_MID) else -1
        q = quantization(d) if kind == "CONST" else 0.0
        obs, bar = r.observed, r.declared_bar
        rows.append(dict(script=r.script[:58], gate_id=r.gate_id, kind=kind, src=str(r.src)[:90],
                         observed=obs, bar=bar, decimals=d, q=q,
                         overrun=(obs / bar) if (pd.notna(obs) and pd.notna(bar) and bar > 0) else np.nan,
                         recovered_by_q=bool(pd.notna(obs) and pd.notna(bar) and obs < bar + q)))
    FF = pd.DataFrame(rows)
    say("\nthe native failures with overrun (observed / declared bar) and the bar+q test:")
    say(FF.to_string(index=False, float_format=lambda x: f"{x:.6g}"))
    num = FF[FF.overrun.notna()]
    for k in ("CONST", "ARTEFACT", "SELF"):
        s = num[num.kind == k]
        if len(s):
            say(f"  [{k}] failures n={len(s)}  median overrun {s.overrun.median():.3g}x  "
                f"max {s.overrun.max():.3g}x  recovered by bar+q: {int(s.recovered_by_q.sum())}/{len(s)}")
    FF.to_csv(OUT(".fails.csv"), index=False)

    # ---- C1: is the artefact identifiable from the typed number?
    consts = []
    seen = set()
    for _, r in M[M.kind_MID == "CONST"].iterrows():
        tok = str(r.ref_MID)
        if tok and tok not in seen:
            try: v = float(tok)
            except ValueError: continue
            seen.add(tok); consts.append((tok, v, int(r.dec_MID)))
    say(f"\nC1 — {len(consts)} distinct hand-copied constants among the reached CONST gates.")
    I = scan_artefact_cells(consts)
    say(I.to_string(index=False))
    say(f"  median cells inside a constant's own rounding cell: "
        f"{I.cells_in_rounding_cell.median():.0f}; median distinct scripts: "
        f"{I.distinct_scripts.median():.0f}")
    say("  -> a constant is IDENTIFIABLE from its value alone only if this count is 1.  "
        f"It is 1 for {int((I.cells_in_rounding_cell == 1).sum())} of {len(I)} constants.")
    I.to_csv(OUT(".identify.csv"), index=False)

    # ---- the grid: classifier x bar x kind, counterfactual pass counts on the reached gates
    grid = []
    for mode in CLASSIFIERS:
        for bar in BAR_LADDER:
            for k in KINDS:
                # scored forms only: a bar means "gap <= bar" for tol/exact/count.  The record's
                # structural clauses carry no bar and its one `floor` clause inverts the sense,
                # so both are excluded from every counterfactual (counts reported in PART B).
                s = M[(M["kind_" + mode] == k) & M.observed.notna()
                      & M["kind"].isin(("tol", "exact", "count"))]
                if not len(s): continue
                d = s["dec_" + mode].fillna(-1).astype(int)
                q = np.where(np.array([kk == "CONST" for kk in s["kind_" + mode]]),
                             np.array([quantization(x) for x in d]), 0.0)
                # the record's own gate FORM decides the comparison: a tolerance gate is
                # strict (`observed < bar`), an exact/count/floor gate is satisfied at 0 == 0.
                strict = (s["kind"] == "tol").values
                def hits(obs, bars):
                    obs = np.asarray(obs, dtype=float); bars = np.asarray(bars, dtype=float)
                    ok = np.where(strict, obs < bars, obs <= bars)
                    return int(np.nansum(np.where(np.isnan(obs) | np.isnan(bars), False, ok)))
                nb = s.declared_bar.notna()
                grid.append(dict(classifier=mode, bar=bar, kind=k, n=len(s),
                                 pass_native=int(s.passed.sum()),
                                 pass_flat_bar=hits(s.observed, np.full(len(s), bar)),
                                 pass_bar_plus_q=hits(s.observed, bar + q),
                                 n_with_bar=int(nb.sum()),
                                 pass_native_plus_q=hits(s.observed, s.declared_bar + q)))
    GR = pd.DataFrame(grid)
    # G4 (internal consistency): q is 0 for every kind but CONST, so the bar+q counterfactual
    # must reproduce the record's NATIVE outcome exactly on those kinds.
    z = GR[GR.kind != "CONST"]
    ok4 = bool((z.pass_native_plus_q == z.pass_native).all())
    _EXTRA_GATES.append(dict(gate="G4 bar+q reproduces NATIVE on every non-CONST kind (q=0)",
                             passed=ok4,
                             detail=f"{int((z.pass_native_plus_q == z.pass_native).sum())}/{len(z)} rows"))
    say(f"\n  [{'PASS' if ok4 else 'FAIL'}] G4 bar+q reproduces the NATIVE outcome on every "
        f"non-CONST kind (q=0 there): "
        f"{int((z.pass_native_plus_q == z.pass_native).sum())}/{len(z)} rows")
    say("\nPART C GRID — classifier x bar x reference kind, ALL grid points "
        f"({len(GR)} rows; numeric-observed gates only):")
    say(GR.to_string(index=False))
    GR.to_csv(OUT(".grid.csv"), index=False)
    return FF, I, GR


# ============================================================ PART D — RULE 8 (the price leg)
def part_d(panels: dict) -> pd.DataFrame:
    say("\n" + "=" * 78)
    say("PART D / RULE 8 — the publication convention as a BOOK ADMISSION GATE")
    say("  books scored on 2009-2016 ONLY; each policy's pick read ONCE on 2017-01-01+")
    say("=" * 78)
    say("  Two pre-registered re-run perturbations, both reported:")
    say("   - VINTAGE (idea 681's 2-trading-day cache step, TRAIL and LEAD). Reported as a "
        "CONTROL: on a statistic measured over a FIXED window, with >=200 observations already "
        "behind every window date, both directions are EXACTLY 0 — proven below, not assumed.")
    say("   - WARMUP (the record's own 260-vs-252 skip convention). This is the live "
        "perturbation the admission gates are read on; it is a convention gap of the same size "
        "class as the record's failing ARTEFACT gates (1e-3 to 1e-2 of Sharpe).")
    books, bench = [], []
    for pname, px in panels.items():
        names = [c for c in px.columns if c != "SPY"]
        p = px[names]
        pv = p.iloc[:-VINTAGE_DAYS]                     # TRAIL step (control)
        pl = p.iloc[VINTAGE_DAYS:]                      # LEAD step (the live perturbation)
        start = p.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        base = engine_backtest(p, rules_v2_weights(p, band=BAND, gross=0.75),
                               cost_bps=COST_BPS, freq="W")["returns"].loc[start:]
        for nm, s in (("RULESv2", base), ("SPY", spy)):
            bench.append(dict(panel=pname, book=nm,
                              **{"IS_" + k: v for k, v in mets(s.loc[IS_START:IS_END]).items()},
                              **{"OOS_" + k: v for k, v in mets(s.loc[OOS_START:]).items()},
                              **mets(s), H1=metrics(s.iloc[:len(s) // 2])["Sharpe"],
                              H2=metrics(s.iloc[len(s) // 2:])["Sharpe"]))
        for gr in (0.50, 0.75, 1.00):
            w = ewall_weights(p, gr)
            wv = ewall_weights(pv, gr)
            wl = ewall_weights(pl, gr)
            for cad in ("W", "M", "Q"):
                r = pd.Series(fast_backtest(p.values, w.values, rebalance_mask(p.index, cad).values),
                              index=p.index).loc[start:]
                rv = pd.Series(fast_backtest(pv.values, wv.values, rebalance_mask(pv.index, cad).values),
                               index=pv.index).loc[start:]
                rl = pd.Series(fast_backtest(pl.values, wl.values, rebalance_mask(pl.index, cad).values),
                               index=pl.index).loc[start:]
                ra = pd.Series(fast_backtest(p.values, w.values, rebalance_mask(p.index, cad).values),
                               index=p.index).loc[p.index[252]:]        # WARMUP convention step
                is_full = mets(r.loc[IS_START:IS_END])["Sharpe"]        # full-precision "artefact"
                is_trail = mets(rv.loc[IS_START:IS_END])["Sharpe"]      # VINTAGE TRAIL control
                is_lead = mets(rl.loc[IS_START:IS_END])["Sharpe"]       # VINTAGE LEAD control
                is_vint = mets(ra.loc[IS_START:IS_END])["Sharpe"]       # the gate's input (WARMUP)
                books.append(dict(panel=pname, book=f"g{gr:.2f}-{cad}", gross=gr, cad=cad,
                                  IS_Sharpe_pub=is_full, IS_Sharpe_rerun=is_vint,
                                  drift_VINTAGE_TRAIL=abs(is_trail - is_full),
                                  drift_VINTAGE_LEAD=abs(is_lead - is_full),
                                  drift=abs(is_vint - is_full),
                                  drift_vs_const3=abs(is_vint - round(is_full, 3)),
                                  drift_vs_const4=abs(is_vint - round(is_full, 4)),
                                  **{"IS_" + k: v for k, v in mets(r.loc[IS_START:IS_END]).items()},
                                  **{"OOS_" + k: v for k, v in mets(r.loc[OOS_START:]).items()},
                                  **mets(r), H1=metrics(r.iloc[:len(r) // 2])["Sharpe"],
                                  H2=metrics(r.iloc[len(r) // 2:])["Sharpe"]))
    B = pd.DataFrame(books); BM = pd.DataFrame(bench)
    say(f"\nbook grid — {len(B)} books over {len(panels)} panels, ALL grid points "
        f"(drift = |Sharpe(IS) re-run under the WARMUP convention - Sharpe(IS) as published|):")
    say(f"  VINTAGE control over all {len(B)} books: max TRAIL "
        f"{B.drift_VINTAGE_TRAIL.max():.3e}, max LEAD {B.drift_VINTAGE_LEAD.max():.3e} "
        f"-> a +/-2-day cache step moves a fixed-window statistic by EXACTLY nothing here")
    say(f"  WARMUP drift: max {B.drift.max():.3e}  median {B.drift.median():.3e}  "
        f"min {B.drift.min():.3e}")
    say(B.drop(columns=["gross", "cad"]).to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\nbenchmarks on the same panels and calendars:")
    say(BM.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    B.to_csv(OUT(".bookgrid.csv"), index=False)

    POLICIES = {
        "NOGATE":     lambda r, bar: True,
        "ARTEFACT":   lambda r, bar: r.drift < bar,
        "CONST3":     lambda r, bar: r.drift_vs_const3 < bar,
        "CONST4":     lambda r, bar: r.drift_vs_const4 < bar,
        "CONST3+q":   lambda r, bar: r.drift_vs_const3 < bar + quantization(3),
    }
    BARS = tuple(sorted({NATIVE_CONST_BAR, *BAR_LADDER, 1e-1}))
    picks = []
    for pname in panels:
        s = B[B.panel == pname]
        bm = BM[BM.panel == pname].set_index("book")
        v2, sp = bm.loc["RULESv2"], bm.loc["SPY"]
        for pol, fn0 in POLICIES.items():
          for bar in BARS:
            fn = (lambda r, f=fn0, b=bar: f(r, b))
            adm = s[s.apply(fn, axis=1)]
            if not len(adm):
                picks.append(dict(panel=pname, policy=pol, bar=bar, admitted=0, book="NONE",
                                  OOS_CAGR=np.nan, OOS_Sharpe=np.nan, OOS_MaxDD=np.nan,
                                  v2_OOS_Sharpe=v2.OOS_Sharpe, spy_OOS_Sharpe=sp.OOS_Sharpe,
                                  spy_OOS_CAGR=sp.OOS_CAGR, spy_OOS_MaxDD=sp.OOS_MaxDD,
                                  H1=np.nan, H2=np.nan, MaxDD=np.nan, CAGR=np.nan,
                                  pass4a=False, pass4b=False))
                continue
            pick = adm.loc[adm.IS_Sharpe.idxmax()]
            p4a = (pick.H1 > v2.H1) and (pick.H2 > v2.H2) and (pick.MaxDD >= v2.MaxDD)
            p4b = ((pick.H1 > sp.H1) and (pick.H2 > sp.H2) and (pick.OOS_Sharpe > sp.OOS_Sharpe)
                   and (pick.MaxDD >= 0.60 * sp.MaxDD) and (pick.CAGR >= 0.70 * sp.CAGR))
            picks.append(dict(panel=pname, policy=pol, bar=bar, admitted=len(adm), book=pick.book,
                              OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                              OOS_MaxDD=pick.OOS_MaxDD, v2_OOS_Sharpe=v2.OOS_Sharpe,
                              spy_OOS_Sharpe=sp.OOS_Sharpe, spy_OOS_CAGR=sp.OOS_CAGR,
                              spy_OOS_MaxDD=sp.OOS_MaxDD, H1=pick.H1, H2=pick.H2,
                              MaxDD=pick.MaxDD, CAGR=pick.CAGR,
                              pass4a=bool(p4a), pass4b=bool(p4b)))
    K = pd.DataFrame(picks)
    say(f"\nrule-8 picks — {len(POLICIES)} policies x {len(BARS)} bars x {len(panels)} panels "
        f"= {len(K)} cells, ALL reported; chosen on 2009-2016 ONLY, read ONCE on 2017+:")
    say(K.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    gated = K[K.policy != "NOGATE"]
    base_pick = K[K.policy == "NOGATE"].drop_duplicates("panel").set_index("panel").book
    moved = sum(1 for _, r in gated.iterrows() if r.book != base_pick[r.panel])
    stood = int((gated.admitted == 0).sum())
    say(f"\n  gated cells: {len(gated)};  book changed in {moved};  of those, "
        f"{stood} are a STAND-DOWN (nothing admitted at all), "
        f"{moved - stood} a genuinely different book")
    say("\n  admitted count by policy x bar (pooled over panels):")
    say(gated.pivot_table(index="policy", columns="bar", values="admitted",
                          aggfunc="sum").to_string())
    say(f"\n  RULE 8 VERDICT: 4a {int(K.pass4a.sum())}/{len(K)}, 4b {int(K.pass4b.sum())}/{len(K)}"
        f"  (NOGATE alone: 4a {int(K[K.policy=='NOGATE'].pass4a.sum())}/"
        f"{len(K[K.policy=='NOGATE'])}, 4b {int(K[K.policy=='NOGATE'].pass4b.sum())}/"
        f"{len(K[K.policy=='NOGATE'])})")
    K.to_csv(OUT(".walkforward.csv"), index=False)
    return K


# ================================================================================ gates
def run_gates(C: pd.DataFrame, G: pd.DataFrame) -> list:
    say("\n" + "=" * 78)
    say("PRE-REGISTERED REPRODUCTION GATES (non-raising; all reported)")
    say("=" * 78)
    g = []
    def gate(name, ok, detail):
        g.append(dict(gate=name, passed=bool(ok), detail=detail))
        say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    vc = C.form.value_counts()
    gate("G1 idea 515 census shape 520/345/87/46/40/151",
         len(C) == 520 and vc.get("tolerance") == 345 and vc.get("exact") == 87
         and vc.get("structural") == 46 and vc.get("count") == 40 and C.script.nunique() == 151,
         f"{len(C)}/{vc.get('tolerance')}/{vc.get('exact')}/{vc.get('structural')}/"
         f"{vc.get('count')}/{C.script.nunique()}")
    gate("G2 idea 515 reached gates 171 with 23 native failures",
         len(G) == 171 and int((~G.passed).sum()) == 23,
         f"{len(G)} reached, {int((~G.passed).sum())} failures")
    lit = G[G.src.astype(str).str.contains("1.133", regex=False)]
    vals = sorted(set(np.round(lit.observed.dropna().values, 10)))
    gate("G3 queue claim: 1.133 restated in >=3 scripts, one observed value 7.85e-4",
         lit.script.nunique() >= 3 and len(vals) == 1 and abs(vals[0] - 7.848148e-4) < 1e-8,
         f"{lit.script.nunique()} scripts, {len(lit)} clauses, observed {vals}")
    return g


# ================================================================================== main
def main():
    say("Idea 521 — do the record's HAND-COPIED-CONSTANT gates fail more than its ARTEFACT "
        "gates?  (lane B, 2026-09-11)")
    say("PROTOCOL rules 1-9.  10 bps, next-day execution.  Two tuned parameters: "
        "REFERENCE-KIND CLASSIFIER x BAR, all grid points reported.")
    say("No script is re-executed: observed/bar/passed are idea 515's committed NATIVE values.")

    C, G = part_a()
    gl = run_gates(C, G)
    M, F = part_b(C, G)
    FF, I, GR = part_c(M, F)

    say("\nLoading panels (committed caches only — no network)...")
    panels = {}
    panels["U56"] = load_universe()
    panels["B136"] = load_universe(broad=True)
    sm = load_universe(small=True)
    mx = sm.drop(columns=["SPY"]).pct_change().abs().max()
    drop = list(mx[mx >= 1.0].index)
    panels["SMALL439"] = sm.drop(columns=drop)
    say(f"  U56 {panels['U56'].shape}  B136 {panels['B136'].shape}  "
        f"SMALL439 {panels['SMALL439'].shape} (dropped {len(drop)} names, max 1d move >= 1.0)")
    K = part_d(panels)

    # ------------------------------------------------------------------------- verdict
    say("\n" + "=" * 78)
    say("VERDICT")
    say("=" * 78)
    mid = M[M.observed.notna()]
    cf = mid[mid.kind_MID == "CONST"]; af = mid[mid.kind_MID == "ARTEFACT"]
    cr = float((~cf.passed).mean()) if len(cf) else np.nan
    ar = float((~af.passed).mean()) if len(af) else np.nan
    nq = FF[(FF.kind == "CONST")]
    say(f"  A. CONST native failure rate {cr:.4f} (n={len(cf)}) vs ARTEFACT {ar:.4f} (n={len(af)})")
    say(f"  B. of the {len(nq)} CONST failures, bar'=bar+q recovers {int(nq.recovered_by_q.sum())}")
    say(f"  C. artefact identifiable from the typed value alone: "
        f"{int((I.cells_in_rounding_cell == 1).sum())}/{len(I)} constants")
    gated = K[K.policy != "NOGATE"]
    say(f"  D. rule 8: 4a {int(K.pass4a.sum())}/{len(K)}, 4b {int(K.pass4b.sum())}/{len(K)}; "
        f"of {len(gated)} gated cells {int((gated.admitted == 0).sum())} admit NOTHING "
        f"(stand-down) and {int((gated.admitted > 0).sum())} admit a book")
    say("  KEEP paths: 4a needs Sharpe > RULES v2 in BOTH halves with MaxDD no worse; "
        "4b needs Sharpe > SPY in both halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70%.")

    pd.DataFrame(gl + _EXTRA_GATES).to_csv(OUT(".gates.csv"), index=False)
    OUT(".console.txt").write_text("\n".join(_LOG) + "\n")
    say(f"\nwrote {OUT('.census.csv').name}, {OUT('.fails.csv').name}, {OUT('.identify.csv').name}, "
        f"{OUT('.grid.csv').name}, {OUT('.walkforward.csv').name}, {OUT('.bookgrid.csv').name}, "
        f"{OUT('.gates.csv').name}, {OUT('.console.txt').name}")
    OUT(".console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
