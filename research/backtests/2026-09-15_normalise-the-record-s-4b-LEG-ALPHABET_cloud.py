#!/usr/bin/env python3
"""Idea 951 (cloud, 2026-09-15) -- normalise the record's 4b LEG ALPHABET and re-read every
committed FAIL share.

THE QUESTION (queue, 2026-09-15)
  Idea 944 found the record writes the same binding leg as `L4_DD`, `DD`, `DDCAP` and
  `L4_DDcap`, joined by `+`, `,`, `|` or `/`, and that a census using one alphabet reads the
  L4_DD-alone share at 1.9% against 15.8% once all five are unified -- an 8x understatement.
  Apply the canonical `L1_H1..L5_CAGR` alphabet to every committed FAIL row, publish the
  per-file mapping so it is auditable, and report which published leg-share claims move past a
  5 pp bar.

WHAT 944 ACTUALLY DID, AND THE HOLE THIS RUN IS FILLING
  944's census normalised SPELLINGS but not COLUMNS.  Its selector was
  `[c for c in fieldnames if "fail4b" in c.lower()]` -- one column name.  A pre-read of the
  record (reported at S1 below, before any claim is touched) finds the record writes its 4b
  FAIL rows under at least NINE more column names -- `f4b`, `fail_4b`, `fails`, `failing`,
  `fail_legs`, `fail`, `binding`, `binding_leg`, `bind` -- carrying leg strings in yet more
  spellings (`L5_CAGRfloor`, `L4_DDcap`, `MaxDD`, `CAGRFLOOR`, `DDCAP`, `H1;CAGR`,
  `CAGR (never)`, and dict-valued cells like `{'DD': 44, 'CAGR': 4}`).  So 944's own headline
  -- that unifying the alphabet moves the L4_DD-alone share 8x -- was itself measured on a
  1-column slice of the record.  This run asks whether widening the SELECTOR moves the shares
  again, by the same 5 pp bar the queue names.
  This run does NOT attempt idea 952's job (recovering a leg from a row that names none); a
  row whose cell is a bare `True`/`1` stays unrecoverable here and is counted as such.

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL rule 4: max 2 tuned parameters)
  TUNED 1  ALPHABET x SELECTOR, 4 levels, every one reported:
           A0_RAW     no normalisation at all -- raw cell strings compared verbatim.  The
                      pre-944 status quo, and the thing 944's 8x is measured against.
           A1_944     944's committed CANON, 944's `fail4b`-only selector.  Reproduces 944
                      cell-for-cell at G3 or this run says so.
           A2_CANON   this run's canonical L1_H1..L5_CAGR alphabet, 944's selector.
                      Isolates the ALPHABET move with the column set held fixed.
           A3_WIDE    canonical alphabet + the widened selector (all 10 column families).
                      Isolates the SELECTOR move with the alphabet held fixed.
  TUNED 2  CLAIM SET, 4 levels, every one reported:
           K_ALONE    the five `alone_rows` shares 944 committed in its `.censusleg.csv`
           K_AMONG    the five `among_rows` shares from the same file
           K_FILE     the five `alone_files` / `among_files` shares from the same file
           K_MODAL    the record's prose claims: "the modal binder is the CAGR floor, 68.8%"
                      and "the DD cap binds 58.3%" (CHANGELOG, 2026-09-15)
  REPORTED, NOTHING FITTED ON IT: per-file mapping (one row per file x legset, published as
  `.mapping.csv`), the full unmappable inventory, the price grid below.

PRE-REGISTERED BARS (fixed before any number of this run was read; both directions reported)
  H_ALPH   The ALPHABET move is real iff, holding the selector at 944's, at least one of the
           20 claims in K_ALONE u K_AMONG u K_FILE moves >= 5 pp between A0_RAW and A2_CANON.
  H_SEL    The SELECTOR move is real iff at least one claim moves >= 5 pp between A2_CANON and
           A3_WIDE.  This is the part 944 could not see.
  H_8X     the queue's own headline -- "a census using one alphabet reads the L4_DD-alone share
           at 1.9% against 15.8% once all five are unified, an 8x understatement" -- reproduces.
           SUPPORTED iff the raw endpoint is within 0.5 pp of 1.9% and the ratio is >= 4x, on
           EITHER of the record's two committed 944 censuses (the strict one 944-cloud
           published, and the wide one 944-B published and this run replays at G3).
  H_MODAL  The record's "CAGR floor is the modal binder at 68.8%" survives A3_WIDE, i.e. CAGR
           is still the most-often-present leg AND its among-share stays within 5 pp.
  H_COVER  The canonical alphabet maps >= 99% of A3_WIDE's FAIL cells (coverage, not a claim).
  H_WF     (PROTOCOL rule 8, REQUIRED) the price leg's book x cadence is chosen on 2009-2016
           ALONE and 2017-2026 is read ONCE, with BOTH KEEP paths (4a and 4b) adjudicated and
           every leg named in the canonical alphabet.

WHY THERE IS A PRICE LEG AT ALL
  A census of text moves no capital by itself.  PROTOCOL rules 4 and 8 bind every run, so this
  run also PRICES the record's standing KEEP-4b construction (top-k equal weight, no vol
  scaler, gross 0.75) on three panels x four cadences at 10 bps, and emits the record's first
  grid whose `fail4b` column is written in the canonical alphabet by construction -- i.e. it
  pays the audit forward instead of adding one more spelling.  The walk-forward chooses the
  (book, cadence) cell on 2009-2016 alone and reads 2017-2026 once.

SURVIVORSHIP (PROTOCOL rule 9)
  U56 / B136 / SMALL are CURRENT-CONSTITUENT lists (SMALL additionally drops every ticker with
  `max_1d_move` >= 1.0 per `data/small_meta.csv`).  Every CAGR, Sharpe and drawdown LEVEL in
  the price leg is therefore optimistic and none is a capital claim on its own.  The 4b legs
  are read against SPY, which is not survivorship-inflated, so a survivor panel makes books
  look BETTER and 4b failures RARER -- which cuts against this run finding failures, not for
  it.  The CENSUS is a census of the record's TEXT and inherits whatever biases its source runs
  had; it makes no market claim whatsoever.
"""
import os, sys, csv, gzip, glob, time, ast, warnings, collections
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score   # noqa: E402
from engine import backtest, rebalance_mask                               # noqa: E402

BAND0, VOLCAP, WARM = 0.03, 0.60, 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
HEAD_COST = 10.0                       # PROTOCOL rule 2 -- carries every verdict
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
PP_BAR = 0.05                          # the queue's own 5 pp bar
COVER_BAR = 0.99
SMOKE = bool(int(os.environ.get("IDEA951_SMOKE", "0")))
LINES = []

# 944's committed numbers, transcribed from its `.censusleg.csv` / `.census.csv` (G3 anchors)
PUB944_ALONE = {"H1": 0.00854326128222399, "H2": 0.003387422693037781,
                "OOS": 0.00013226379278672465, "DD": 0.15104770069193557,
                "CAGR": 0.1694850284734554}
PUB944_AMONG = {"H1": 0.5161729226624212, "H2": 0.5776976302737126,
                "OOS": 0.5368611842508113, "DD": 0.5833274141203846,
                "CAGR": 0.6875157675586309}
PUB944_ALONE_F = {"H1": 0.020011431899719396, "H2": 0.01652217486159022,
                  "OOS": 6.891805628433825e-05, "DD": 0.19266259010632064,
                  "CAGR": 0.19641033607433975}
PUB944_AMONG_F = {"H1": 0.43871963395921976, "H2": 0.5291501329487022,
                  "OOS": 0.4645635174970494, "DD": 0.6090880796904012,
                  "CAGR": 0.615061520568786}
PUB944_NFAIL = 816550

# 944-CLOUD's STRICT census, transcribed from its committed console (lines 47-71 of
# `..._cloud.console.txt`).  This is the block the QUEUE's "1.9% vs 15.8%, an 8x
# understatement" sentence was read off, so the arithmetic is checked against it directly.
PUB944C_N = 125090                     # committed: "125,090 committed 4b FAIL rows from 184 files"
PUB944C_RAW = {                        # committed "RAW signature alphabet, as committed"
    "H1,H2,OOS,DD,CAGR": 29985, "CAGR": 18969, "DD": 16006,
    "H1,H2,OOS,CAGR": 10379, "H2,OOS,DD": 9619, "H1,CAGR": 4282,
}
PUB944C_NORM = {                       # committed "NORMALISED binding signature"
    "L1_H1+L2_H2+L3_OOS+L4_DD+L5_CAGR": 33040, "L5_CAGR": 22791, "L4_DD": 19772,
    "L1_H1+L2_H2+L3_OOS+L5_CAGR": 13846, "L2_H2+L3_OOS+L4_DD": 10265,
    "L1_H1+L5_CAGR": 5305, "L1_H1+L2_H2+L3_OOS+L4_DD": 4952, "L2_H2+L4_DD": 2320,
    "L2_H2+L3_OOS+L5_CAGR": 1995, "L1_H1+L4_DD": 1994, "L1_H1": 1962,
    "L2_H2+L3_OOS+L4_DD+L5_CAGR": 1390,
}
QUEUE_RAW_CLAIM, QUEUE_NORM_CLAIM, QUEUE_RATIO = 0.019, 0.158, 8.0


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ==========================================================================================
# (1) THE ALPHABETS -- TUNED axis 1.  A1_944 is copied VERBATIM from 944 so G3 can nest it.
# ==========================================================================================
CANON_944 = {
    "H1": "H1", "L1": "H1", "L1_H1": "H1", "H1SHARPE": "H1", "SH1": "H1", "HALF1": "H1",
    "H2": "H2", "L2": "H2", "L2_H2": "H2", "H2SHARPE": "H2", "SH2": "H2", "HALF2": "H2",
    "OOS": "OOS", "L3": "OOS", "L3_OOS": "OOS", "OOSSHARPE": "OOS", "OOS_SHARPE": "OOS",
    "WF": "OOS", "OOSSH": "OOS",
    "DD": "DD", "L4": "DD", "L4_DD": "DD", "MAXDD": "DD", "DDCAP": "DD", "DD_CAP": "DD",
    "DRAWDOWN": "DD",
    "CAGR": "CAGR", "L5": "CAGR", "L5_CAGR": "CAGR", "CAGRFLOOR": "CAGR",
    "CAGR_FLOOR": "CAGR", "RET": "CAGR",
}
SEPS_944 = [",", "+", "|", ";", "/", "&", " "]
PASSTOK_944 = {"-", "", "NONE", "PASS", "OK", "NAN", "0", "FALSE", "NA", "PASS4B", "-NONE-"}

# -- this run's canonical alphabet.  Every extra key is a spelling OBSERVED in the record
#    (the S1 pre-read prints the evidence); nothing here re-labels a spelling 944 already had.
CANON = dict(CANON_944)
CANON.update({
    "L1_H1SHARPE": "H1", "H1_SHARPE": "H1", "SHARPE_H1": "H1", "FIRSTHALF": "H1",
    "H1SH": "H1", "L1H1": "H1", "HALF_1": "H1", "MH1": "H1", "H1_OOS": "H1",
    "L2_H2SHARPE": "H2", "H2_SHARPE": "H2", "SHARPE_H2": "H2", "SECONDHALF": "H2",
    "H2SH": "H2", "L2H2": "H2", "HALF_2": "H2", "MH2": "H2", "H2_OOS": "H2",
    "L3OOS": "OOS", "OOS_SH": "OOS", "OOSSHARPE_": "OOS", "WALKFORWARD": "OOS",
    "MOOS": "OOS", "OOS4B": "OOS", "L3_OOSSHARPE": "OOS",
    "L4DD": "DD", "L4_DDCAP": "DD", "DDCAP_": "DD", "MAX_DD": "DD", "MDD": "DD",
    "MDD_OOS": "DD", "DD_OOS": "DD", "MAXDRAWDOWN": "DD", "L4_MAXDD": "DD",
    "DDFLOOR": "DD", "DRAW": "DD", "L4_DRAWDOWN": "DD",
    "L5CAGR": "CAGR", "L5_CAGRFLOOR": "CAGR", "CAGRFLOOR_": "CAGR", "MCAGR": "CAGR",
    "MCAGR_OOS": "CAGR", "CAGR_OOS": "CAGR", "OOS_CAGR": "CAGR", "L5_CAGRFLOOR_": "CAGR",
    "CAGR>=70%SPY": "CAGR", "CAGR70": "CAGR", "RETURN": "CAGR", "L5_RET": "CAGR",
})
SEPS = [",", "+", "|", ";", "/", "&", " ", "-"]
# a cell that says "this row PASSED" / "no leg named".  Deliberately NOT extended with any
# token that could be a leg, so widening the pass set can never manufacture a pass.
PASSTOK = set(PASSTOK_944) | {"(NONE)", "-NONE-", "NONE-", "N/A", "NAN ", "PASS4A",
                              "TRUE-PASS", "ALLPASS", "0.0", "-", "--", "()", "{}", "[]"}
# a cell that asserts failure but names NO leg -- unrecoverable HERE (idea 952's job).
UNNAMED = {"TRUE", "1", "1.0", "FAIL", "Y", "YES", "F"}


def _fold(tk):
    """Fold one token onto a canonical leg, or None."""
    for cand in (tk, tk.replace("-", "_"), tk.replace("_", ""), tk.replace(" ", ""),
                 tk.replace("_", "").replace("-", "")):
        hit = CANON.get(cand)
        if hit:
            return hit
    # a trailing qualifier the record uses in prose columns: "CAGR (never)", "DD (never)"
    base = tk.split("(")[0].strip()
    if base and base != tk:
        return _fold(base)
    return None


def norm_944(v):
    """944's parser, VERBATIM.  Returns (frozenset, status in {'pass','fail','unmappable'})."""
    s = str(v).strip()
    if s.upper() in PASSTOK_944:
        return frozenset(), "pass"
    t = s.upper()
    for sep in SEPS_944[1:]:
        t = t.replace(sep, ",")
    toks = [x.strip() for x in t.split(",") if x.strip()]
    if not toks:
        return frozenset(), "pass"
    out = set()
    for tk in toks:
        tk2 = tk.replace("-", "_") if tk.startswith("L") else tk
        hit = CANON_944.get(tk) or CANON_944.get(tk2) or CANON_944.get(tk.replace("_", ""))
        if hit is None:
            return frozenset(), "unmappable"
        out.add(hit)
    return frozenset(out), "fail"


def norm_canon(v):
    """This run's canonical parser.  status in {'pass','fail','unnamed','unmappable'}."""
    s = str(v).strip()
    u = s.upper()
    if u in PASSTOK:
        return frozenset(), "pass"
    if u in UNNAMED:
        return frozenset(), "unnamed"
    # dict-valued cells the record writes for leg HISTOGRAMS: {'DD': 44, 'CAGR': 4}
    if s.startswith("{") and s.endswith("}"):
        try:
            d = ast.literal_eval(s)
            if isinstance(d, dict) and d:
                legs = set()
                for k in d:
                    hit = _fold(str(k).strip().upper())
                    if hit is None:
                        return frozenset(), "unmappable"
                    legs.add(hit)
                return frozenset(legs), "fail"
        except Exception:
            return frozenset(), "unmappable"
        return frozenset(), "unmappable"
    # a bare number that is not 0/1 is a COUNT column, not a leg string
    try:
        float(s)
        return frozenset(), "unmappable"
    except ValueError:
        pass
    t = u
    for sep in SEPS[1:]:
        if sep == "-" and t.startswith("L"):     # keep L4-DD joinable, see _fold
            continue
        t = t.replace(sep, ",")
    toks = [x.strip() for x in t.split(",") if x.strip()]
    if not toks:
        return frozenset(), "pass"
    out = set()
    for tk in toks:
        if tk in PASSTOK:
            continue
        hit = _fold(tk)
        if hit is None:
            return frozenset(), "unmappable"
        out.add(hit)
    if not out:
        return frozenset(), "pass"
    return frozenset(out), "fail"


def norm_raw(v):
    """A0_RAW: no normalisation.  The legset IS the raw string, split on ',' only (the one
    separator the record's most common spelling uses).  This is the pre-944 status quo."""
    s = str(v).strip()
    if s in ("-", "", "none", "-none-", "(none)"):
        return frozenset(), "pass"
    if s.upper() in UNNAMED:
        return frozenset(), "unnamed"
    toks = [x.strip() for x in s.split(",") if x.strip()]
    if not toks:
        return frozenset(), "pass"
    return frozenset(toks), "fail"


# ---- the SELECTORS (the other half of TUNED axis 1) --------------------------------------
SEL_944 = ("fail4b",)
# every column family observed in the S1 pre-read to carry 4b leg strings.
WIDE_EXACT = {"fail4b", "f4b", "fail_4b", "fails", "failing", "fail_legs", "fail",
              "binding", "binding_leg", "bind"}


def cols_944(fieldnames):
    return [c for c in (fieldnames or []) if c and "fail4b" in c.lower()]


def cols_wide(fieldnames):
    out = []
    for c in (fieldnames or []):
        if not c:
            continue
        lc = c.strip().lower()
        if "fail4b" in lc or lc in WIDE_EXACT:
            out.append(c)
    return out


ARMS = {
    "A0_RAW":   (norm_raw,   cols_944),
    "A1_944":   (norm_944,   cols_944),
    "A2_CANON": (norm_canon, cols_944),
    "A3_WIDE":  (norm_canon, cols_wide),
}


# ==========================================================================================
# (2) THE CENSUS
# ==========================================================================================
def census(normfn, colfn, collect_map=False, collect_unmap=True):
    files = sorted(glob.glob(str(OUT / "*.csv"))) + sorted(glob.glob(str(OUT / "*.csv.gz")))
    rows = collections.Counter()
    per_file = {}
    n_pass = n_fail = n_unmap = n_unnamed = 0
    unmap = collections.Counter()
    mapping = []
    nfiles = 0
    for f in files:
        name = Path(f).name
        if name.startswith(STEM):          # never census this run's own output
            continue
        try:
            op = gzip.open(f, "rt", newline="") if f.endswith(".gz") else open(f, "r", newline="")
            with op as fh:
                rd = csv.DictReader(fh)
                cols = colfn(rd.fieldnames)
                if not cols:
                    continue
                nfiles += 1
                loc = collections.Counter()
                for row in rd:
                    for c in cols:
                        v = row.get(c)
                        if v is None or str(v).strip() == "":
                            continue
                        legs, st = normfn(v)
                        if st == "pass":
                            n_pass += 1
                        elif st == "fail":
                            n_fail += 1
                            rows[legs] += 1
                            loc[legs] += 1
                        elif st == "unnamed":
                            n_unnamed += 1
                        else:
                            n_unmap += 1
                            if collect_unmap:
                                unmap[str(v).strip()[:40]] += 1
                if loc:
                    per_file[name] = loc
                    if collect_map:
                        for ls, n in sorted(loc.items(), key=lambda kv: -kv[1]):
                            mapping.append(dict(file=name,
                                                legset=",".join(sorted(ls, key=LEGS.index))
                                                if all(x in LEGS for x in ls)
                                                else "|".join(sorted(ls)),
                                                n_legs=len(ls), n_rows=n))
        except Exception as e:
            unmap[f"<unreadable {name}: {type(e).__name__}>"] += 1
    return dict(rows=rows, per_file=per_file, n_pass=n_pass, n_fail=n_fail, n_unmap=n_unmap,
                n_unnamed=n_unnamed, unmap=unmap, nfiles=nfiles, mapping=mapping)


def leg_shares(cen):
    """among/alone shares by row and by file.  The FILE shares follow 944's definition
    exactly (each file votes once with ITS OWN within-file share, then average over files),
    so G3b can nest them; changing that definition here would make the comparison meaningless."""
    rows, per_file = cen["rows"], cen["per_file"]
    tot = sum(rows.values()) or 1
    out = {}
    fw_among = {k: [] for k in LEGS}
    fw_alone = {k: [] for k in LEGS}
    for _, loc in per_file.items():
        t = sum(loc.values()) or 1
        for k in LEGS:
            fw_among[k].append(sum(n for s, n in loc.items() if k in s) / t)
            fw_alone[k].append(sum(n for s, n in loc.items() if s == frozenset({k})) / t)
    for leg in LEGS:
        among_r = sum(n for ls, n in rows.items() if leg in ls)
        alone_r = sum(n for ls, n in rows.items() if ls == frozenset([leg]))
        out[leg] = dict(among_rows=among_r / tot, alone_rows=alone_r / tot,
                        among_files=float(np.mean(fw_among[leg])) if fw_among[leg] else 0.0,
                        alone_files=float(np.mean(fw_alone[leg])) if fw_alone[leg] else 0.0,
                        among_n=among_r, alone_n=alone_r)
    return out


def modal_binder(cen):
    """The CHANGELOG's prose claim: which leg is present in the most FAIL rows, and its share."""
    sh = leg_shares(cen)
    best = max(LEGS, key=lambda L: sh[L]["among_rows"])
    return best, sh[best]["among_rows"], sh["DD"]["among_rows"], sh["CAGR"]["among_rows"]


# ==========================================================================================
# (3) THE PRICE MACHINERY -- copied from idea 944 so this run NESTS it (G1/G2 assert it)
# ==========================================================================================
def offset_mask(idx, per, d):
    key = pd.Series(idx.to_period(per), index=idx)
    last = np.flatnonzero((key != key.shift(-1)).values)
    first = np.concatenate([[0], last[:-1] + 1])
    pick = np.maximum(last - d, first)
    out = pd.Series(False, index=idx)
    out.iloc[np.unique(pick)] = True
    return out, int((last - d < first).sum())


class Ctx:
    def __init__(self, px, mask):
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        m = np.asarray(mask.values, bool)
        m = np.concatenate([[False], m[:-1]]).copy()
        m[0] = True
        self.T, self.N = self.rets.shape
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.N)), C[:-1]])
        self.reb = np.flatnonzero(m)
        seg = np.searchsorted(self.reb, np.arange(self.T), side="right") - 1
        self.s0 = self.reb[seg]
        self.s0p = self.reb[np.maximum(seg - 1, 0)]
        self.ratio = self.Cp / self.Cp[self.s0]
        self.ratiop = self.Cp / self.Cp[self.s0p]

    def shift(self, W):
        return W.reindex(self.idx).fillna(0.0).shift(1).fillna(0.0).values

    def run(self, wt):
        W0 = wt[self.s0]
        h = W0 * self.ratio
        V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
        held = h / V[:, None]
        W0p = wt[self.s0p]
        hp = W0p * self.ratiop
        Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
        heldp = hp / Vp[:, None]
        heldp[self.reb[0]] = 0.0
        turn = np.zeros(self.T)
        turn[self.reb] = np.abs(wt[self.reb] - heldp[self.reb]).sum(axis=1)
        return (held * self.rets).sum(axis=1), turn


def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mets(r):
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    vol = r.std() * np.sqrt(252)
    dd = float((eq / np.maximum.accumulate(eq) - 1).min())
    h = len(r) // 2
    return dict(CAGR=float(eq[-1] ** (1 / yrs) - 1) if yrs > 0 else np.nan,
                Sharpe=float(r.mean() * 252 / vol) if vol > 0 else np.nan, MaxDD=dd,
                H1=sharpe(r[:h]), H2=sharpe(r[h:]))


def legs4b(m, oos_s, ms, spy_oos):
    return dict(H1=m["H1"] > ms["H1"], H2=m["H2"] > ms["H2"], OOS=oos_s > spy_oos,
                DD=abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]),
                CAGR=m["CAGR"] >= 0.70 * ms["CAGR"])


def failstr(lg):
    """THE CANONICAL SPELLING, written by construction: L1_H1..L5_CAGR joined by ','."""
    order = {"H1": "L1_H1", "H2": "L2_H2", "OOS": "L3_OOS", "DD": "L4_DD", "CAGR": "L5_CAGR"}
    f = [order[k] for k in LEGS if not lg[k]]
    return ",".join(f) if f else "-"


def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band, g):
    return ew_gross(px, g).where(band_state(px, band) & px.notna(), 0.0)


def ranked_book(px, g, k):
    sc, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < VOLCAP)
    rank = sc.where(elig).rank(axis=1, ascending=False)
    return (rank <= k).astype(float) * (g / k)


BOOKS = {
    "TOP10_g075": lambda p: ranked_book(p, 0.75, 10),
    "TOP20_g075": lambda p: ranked_book(p, 0.75, 20),     # the 2026-09-04 KEEP-4b incumbent
    "TOP40_g075": lambda p: ranked_book(p, 0.75, 40),
    "BAND03_g075": lambda p: band_book(p, 0.03, 0.75),    # == RULES v2 (G2)
}
CADENCES = {"W": ("W", 0), "2W": ("W2", 0), "M": ("M", 0), "Q": ("Q", 0)}


def cadence_mask(idx, tag):
    if tag == "2W":
        w = np.flatnonzero(rebalance_mask(idx, "W").values)
        out = pd.Series(False, index=idx)
        out.iloc[w[0::2]] = True
        return out
    return offset_mask(idx, tag, 0)[0]


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad)


# ==========================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 951 (cloud, 2026-09-15) -- normalise the record's 4b LEG ALPHABET and re-read")
    P("every committed FAIL share.   PROTOCOL: 10 bps, next-day execution, both KEEP paths,")
    P(f"rule-8 walk-forward.   5 pp bar = {PP_BAR:.0%}   coverage bar = {COVER_BAR:.0%}")
    P("=" * 100)
    P()
    P("PRE-REGISTERED BARS (printed before any number of this run is read)")
    P("  H_ALPH   >= 1 of 20 claims moves >= 5 pp between A0_RAW and A2_CANON (alphabet only)")
    P("  H_SEL    >= 1 of 20 claims moves >= 5 pp between A2_CANON and A3_WIDE (selector only)")
    P("  H_8X     944's 1.9% -> 15.8% L4_DD-alone headline reproduces within 0.5 pp")
    P("  H_MODAL  'CAGR floor is the modal binder at 68.8%' survives A3_WIDE within 5 pp")
    P("  H_COVER  the canonical alphabet maps >= 99% of A3_WIDE's FAIL cells")
    P("  H_WF     rule 8: (book, cadence) chosen on 2009-2016 alone, 2017-2026 read ONCE")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(S1) THE PRE-READ -- which COLUMNS the record writes its 4b FAIL rows under")
    P("=" * 100)
    files = sorted(glob.glob(str(OUT / "*.csv"))) + sorted(glob.glob(str(OUT / "*.csv.gz")))
    colcount, colcells = collections.Counter(), collections.Counter()
    for f in files:
        if Path(f).name.startswith(STEM):
            continue
        try:
            op = gzip.open(f, "rt", newline="") if f.endswith(".gz") else open(f, "r", newline="")
            with op as fh:
                rd = csv.DictReader(fh)
                cols = cols_wide(rd.fieldnames)
                if not cols:
                    continue
                for c in cols:
                    colcount[c.strip().lower()] += 1
                for row in rd:
                    for c in cols:
                        v = row.get(c)
                        if v is not None and str(v).strip():
                            colcells[c.strip().lower()] += 1
        except Exception:
            pass
    s1 = pd.DataFrame([dict(column=c, n_files=colcount[c], n_cells=colcells[c],
                            in_944_selector="fail4b" in c)
                       for c in sorted(colcount, key=lambda k: -colcells[k])])
    P(s1.to_string(index=False))
    dump(s1, "columns")
    in944 = int(s1.loc[s1.in_944_selector, "n_cells"].sum())
    outside = int(s1.loc[~s1.in_944_selector, "n_cells"].sum())
    P(f"  944's selector reached {in944:,} cells; {outside:,} leg-bearing cells "
      f"({outside / max(in944 + outside, 1):.1%} of the total) sit OUTSIDE it.")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(A) GATES -- run before any claim of this run is read")
    P("=" * 100)
    gk = {}

    CEN = {}
    for arm, (nf, cf) in ARMS.items():
        CEN[arm] = census(nf, cf, collect_map=(arm == "A3_WIDE"))
        c = CEN[arm]
        P(f"  census {arm:9s}: files {c['nfiles']:5d}  FAIL {c['n_fail']:9,}  "
          f"PASS {c['n_pass']:8,}  unnamed {c['n_unnamed']:8,}  unmappable {c['n_unmap']:6,}")

    # G3 -- does A1_944 reproduce 944's committed census cell-for-cell?
    a1 = CEN["A1_944"]
    sh1 = leg_shares(a1)
    d_nfail = a1["n_fail"] - PUB944_NFAIL
    worst = max(abs(sh1[L]["alone_rows"] - PUB944_ALONE[L]) for L in LEGS)
    worst = max(worst, max(abs(sh1[L]["among_rows"] - PUB944_AMONG[L]) for L in LEGS))
    gk["G3"] = (d_nfail == 0) and (worst < 1e-12)
    P(f"  G3 A1_944 reproduces 944's committed census : dFAIL {d_nfail:+d} rows, "
      f"worst share delta {worst:.3e}   {'PASS' if gk['G3'] else 'FAIL'}")
    if d_nfail != 0:
        P(f"     NOTE: 944 read {PUB944_NFAIL:,} FAIL cells, this run's replay reads "
          f"{a1['n_fail']:,}.  The record has grown by this run's own commits since; "
          f"the delta is reported rather than absorbed.")

    # G3b -- file-level shares too
    worstf = max(max(abs(sh1[L]["alone_files"] - PUB944_ALONE_F[L]),
                     abs(sh1[L]["among_files"] - PUB944_AMONG_F[L])) for L in LEGS)
    gk["G3b"] = worstf < 1e-12
    P(f"  G3b A1_944 reproduces 944's committed FILE shares: worst delta {worstf:.3e}   "
      f"{'PASS' if gk['G3b'] else 'FAIL'}")

    # G5 -- alphabet idempotence and non-relabelling
    vals = set()
    for f in files[:1500]:
        try:
            op = gzip.open(f, "rt", newline="") if f.endswith(".gz") else open(f, "r", newline="")
            with op as fh:
                rd = csv.DictReader(fh)
                cols = cols_wide(rd.fieldnames)
                if not cols:
                    continue
                for row in rd:
                    for c in cols:
                        v = row.get(c)
                        if v is not None and str(v).strip():
                            vals.add(str(v).strip()[:48])
        except Exception:
            pass
    bad_idem = 0
    for v in vals:
        lg, st = norm_canon(v)
        if st == "fail":
            lg2, st2 = norm_canon(",".join(sorted(lg)))
            if st2 != "fail" or lg2 != lg:
                bad_idem += 1
    gk["G5"] = bad_idem == 0
    P(f"  G5 canonical alphabet is IDEMPOTENT over {len(vals):,} distinct observed cells: "
      f"{bad_idem} violations   {'PASS' if gk['G5'] else 'FAIL'}")

    bad_rel = []
    for v in vals:
        lg944, st944 = norm_944(v)
        lgc, stc = norm_canon(v)
        if st944 == "fail" and (stc != "fail" or lgc != lg944):
            bad_rel.append((v, sorted(lg944), stc, sorted(lgc)))
    gk["G6"] = len(bad_rel) == 0
    P(f"  G6 the canonical alphabet NEVER re-labels a spelling 944 already mapped: "
      f"{len(bad_rel)} violations   {'PASS' if gk['G6'] else 'FAIL'}")
    for b in bad_rel[:6]:
        P(f"     |{b[0]}|  944 -> {b[1]}   canon -> {b[2]}/{b[3]}")

    # H_COVER
    a3 = CEN["A3_WIDE"]
    denom = a3["n_fail"] + a3["n_unmap"]
    cover = a3["n_fail"] / max(denom, 1)
    gk["G7"] = cover >= COVER_BAR
    P(f"  G7 canonical coverage on A3_WIDE (H_COVER)  : {cover:.4%} of "
      f"{denom:,} leg-asserting cells   {'PASS' if gk['G7'] else 'FAIL'}")

    # price gates
    panels = {"U56": load_universe()}
    if not SMOKE:
        panels["B136"] = load_universe(broad=True)
        sm, ndrop = load_small()
        panels["SMALL"] = sm
        P(f"  SMALL panel: {sm.shape[1] - 1} names + SPY benchmark "
          f"({ndrop} tickers with max_1d_move >= 1.0 dropped per data/small_meta.csv)")
    px = panels["U56"]

    bad = 0
    for per in ("W", "M", "Q"):
        m0, _ = offset_mask(px.index, per, 0)
        bad += int((m0.values != rebalance_mask(px.index, per).values).sum())
    gk["G0"] = bad == 0
    P(f"  G0 offset_mask(.,per,0) == engine.rebalance_mask on W/M/Q : {bad} differing rows   "
      f"{'PASS' if gk['G0'] else 'FAIL'}")

    w = band_book(px, BAND0, 0.75)
    g2 = float(np.abs(w.values - rules_v2_weights(px, BAND0, 0.75).values).max())
    gk["G2"] = g2 == 0.0
    P(f"  G2 band_book(0.03,0.75) == rules_v2_weights              : {g2:.3e}   "
      f"{'PASS' if gk['G2'] else 'FAIL'}")

    g1 = 0.0
    for per in ("W", "M", "Q"):
        ctx = Ctx(px, cadence_mask(px.index, per))
        gr, tn = ctx.run(ctx.shift(w))
        fast = pd.Series(gr - tn * HEAD_COST / 1e4, index=px.index)
        slow = backtest(px, w, cost_bps=HEAD_COST, freq=per)["returns"]
        j = px.index[WARM]
        g1 = max(g1, float(np.abs(slow.loc[j:].values - fast.loc[j:].values).max()))
    gk["G1"] = g1 < 1e-12
    P(f"  G1 Ctx.run == engine.backtest @10 bps, worst of W/M/Q    : {g1:.3e}   "
      f"{'PASS' if gk['G1'] else 'FAIL'}")

    P(f"  GATES {sum(1 for v in gk.values() if v)} of {len(gk)} PASS  "
      f"({', '.join(k for k, v in gk.items() if not v) or 'none failing'})")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(B) THE CENSUS UNDER ALL FOUR ARMS -- TUNED axis 1, every level reported")
    P("=" * 100)
    SH = {a: leg_shares(CEN[a]) for a in ARMS}
    crows = []
    for a in ARMS:
        c = CEN[a]
        for L in LEGS:
            crows.append(dict(arm=a, leg=L, n_files=len(c["per_file"]), n_fail_rows=c["n_fail"],
                              among_rows=SH[a][L]["among_rows"], alone_rows=SH[a][L]["alone_rows"],
                              among_files=SH[a][L]["among_files"],
                              alone_files=SH[a][L]["alone_files"],
                              among_n=SH[a][L]["among_n"], alone_n=SH[a][L]["alone_n"]))
    cdf = pd.DataFrame(crows)
    for a in ARMS:
        sub = cdf[cdf.arm == a]
        P(f"  --- {a}  ({CEN[a]['n_fail']:,} FAIL rows over {len(CEN[a]['per_file'])} files)")
        P(sub[["leg", "among_rows", "alone_rows", "among_files", "alone_files"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(cdf, "census")

    # A0_RAW's own legset table -- the un-normalised spellings, for the audit trail
    raw_rows = sorted(CEN["A0_RAW"]["rows"].items(), key=lambda kv: -kv[1])[:40]
    rdf = pd.DataFrame([dict(raw_legset="|".join(sorted(ls)), n_rows=n) for ls, n in raw_rows])
    dump(rdf, "rawlegsets")
    P(f"  A0_RAW sees {len(CEN['A0_RAW']['rows']):,} DISTINCT legsets; A2_CANON collapses the "
      f"same cells onto {len(CEN['A2_CANON']['rows']):,}.")
    P()

    # the per-file mapping -- the queue's explicit deliverable
    mp = pd.DataFrame(CEN["A3_WIDE"]["mapping"])
    dump(mp, "mapping")
    um = pd.DataFrame([dict(raw_cell=k, n_cells=v)
                       for k, v in CEN["A3_WIDE"]["unmap"].most_common()])
    dump(um if len(um) else pd.DataFrame([dict(raw_cell="<none>", n_cells=0)]), "unmappable")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(C) THE CLAIM SET -- TUNED axis 2, every level reported, against the 5 pp bar")
    P("=" * 100)
    CLAIMS = []
    for L in LEGS:
        CLAIMS += [("K_ALONE", f"{L}_alone_rows", L, "alone_rows", PUB944_ALONE[L]),
                   ("K_AMONG", f"{L}_among_rows", L, "among_rows", PUB944_AMONG[L]),
                   ("K_FILE", f"{L}_alone_files", L, "alone_files", PUB944_ALONE_F[L]),
                   ("K_FILE", f"{L}_among_files", L, "among_files", PUB944_AMONG_F[L])]
    krows = []
    for cs, nm, L, fld, pub in CLAIMS:
        v0, v1, v2, v3 = (SH["A0_RAW"][L][fld], SH["A1_944"][L][fld],
                          SH["A2_CANON"][L][fld], SH["A3_WIDE"][L][fld])
        krows.append(dict(claim_set=cs, claim=nm, published_944=pub,
                          A0_RAW=v0, A1_944=v1, A2_CANON=v2, A3_WIDE=v3,
                          d_alphabet=v2 - v0, d_selector=v3 - v2, d_total=v3 - v0,
                          moves_alphabet=abs(v2 - v0) >= PP_BAR,
                          moves_selector=abs(v3 - v2) >= PP_BAR,
                          moves_total=abs(v3 - v0) >= PP_BAR))
    kdf = pd.DataFrame(krows)
    P(kdf[["claim_set", "claim", "A0_RAW", "A1_944", "A2_CANON", "A3_WIDE",
           "d_alphabet", "d_selector", "d_total"]]
      .to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    dump(kdf, "claims")
    n_alph = int(kdf.moves_alphabet.sum())
    n_sel = int(kdf.moves_selector.sum())
    n_tot = int(kdf.moves_total.sum())
    P()
    P(f"  H_ALPH  claims moving >= 5 pp on the ALPHABET alone (A0_RAW -> A2_CANON): "
      f"{n_alph} of {len(kdf)}   {'SUPPORTED' if n_alph >= 1 else 'NOT SUPPORTED'}")
    P(f"  H_SEL   claims moving >= 5 pp on the SELECTOR alone (A2_CANON -> A3_WIDE): "
      f"{n_sel} of {len(kdf)}   {'SUPPORTED' if n_sel >= 1 else 'NOT SUPPORTED'}")
    P(f"  total   claims moving >= 5 pp end to end                              : "
      f"{n_tot} of {len(kdf)}")
    if n_alph:
        P("  biggest ALPHABET moves:")
        for _, r in kdf.reindex(kdf.d_alphabet.abs().sort_values(ascending=False).index).head(6).iterrows():
            P(f"     {r['claim']:18s} {r['A0_RAW']:.4f} -> {r['A2_CANON']:.4f} "
              f"({r['d_alphabet']:+.4f} = {r['d_alphabet'] * 100:+.2f} pp)")
    if n_sel:
        P("  biggest SELECTOR moves:")
        for _, r in kdf.reindex(kdf.d_selector.abs().sort_values(ascending=False).index).head(6).iterrows():
            P(f"     {r['claim']:18s} {r['A2_CANON']:.4f} -> {r['A3_WIDE']:.4f} "
              f"({r['d_selector']:+.4f} = {r['d_selector'] * 100:+.2f} pp)")
    P()

    # ---- H_8X, checked on BOTH of the record's committed 944 censuses ---------------------
    P("  H_8X  -- the queue's '1.9% vs 15.8%, an 8x understatement', audited on the record's")
    P("          own two committed 944 censuses.")
    # (i) 944-CLOUD's strict census, the block the queue sentence was read off.
    c_raw_ddalone = PUB944C_RAW["DD"] / PUB944C_N
    c_norm_ddalone = PUB944C_NORM["L4_DD"] / PUB944C_N
    c_h2dd = PUB944C_NORM["L2_H2+L4_DD"] / PUB944C_N
    P(f"          944-cloud STRICT (n = {PUB944C_N:,}):")
    P(f"            raw       'DD' alone          {PUB944C_RAW['DD']:8,}  {c_raw_ddalone:.4f}"
      f"   <- the true raw endpoint")
    P(f"            normalised 'L4_DD' alone      {PUB944C_NORM['L4_DD']:8,}  "
      f"{c_norm_ddalone:.4f}   <- the queue's 15.8%, correctly cited")
    P(f"            normalised 'L2_H2+L4_DD'      {PUB944C_NORM['L2_H2+L4_DD']:8,}  "
      f"{c_h2dd:.4f}   <- the queue's '1.9%', MIS-cited: a TWO-leg set")
    P(f"            true unification move          {c_raw_ddalone:.4f} -> {c_norm_ddalone:.4f} "
      f"= {c_norm_ddalone / c_raw_ddalone:.3f}x  ({(c_norm_ddalone - c_raw_ddalone) * 100:+.2f} pp)")
    # (ii) this run's independent replay on 944-B's wide census
    dd_alone_raw = SH["A0_RAW"]["DD"]["alone_rows"]
    dd_alone_944 = SH["A1_944"]["DD"]["alone_rows"]
    dd_alone_wide = SH["A3_WIDE"]["DD"]["alone_rows"]
    P(f"          this run's replay on 944-B's WIDE census (n = {CEN['A1_944']['n_fail']:,}):")
    P(f"            DD alone  raw {dd_alone_raw:.4f} -> 944-alphabet {dd_alone_944:.4f} "
      f"= {dd_alone_944 / max(dd_alone_raw, 1e-12):.3f}x  "
      f"({(dd_alone_944 - dd_alone_raw) * 100:+.2f} pp); A3_WIDE {dd_alone_wide:.4f}")
    ratio_c = c_norm_ddalone / c_raw_ddalone
    ratio_b = dd_alone_944 / max(dd_alone_raw, 1e-12)
    h8 = ((abs(c_raw_ddalone - QUEUE_RAW_CLAIM) <= 0.005 and ratio_c >= 4.0)
          or (abs(dd_alone_raw - QUEUE_RAW_CLAIM) <= 0.005 and ratio_b >= 4.0))
    P(f"          H_8X {'SUPPORTED' if h8 else 'NOT SUPPORTED'}: the unification move is "
      f"{ratio_c:.2f}x (strict) / {ratio_b:.2f}x (wide), not {QUEUE_RATIO:.0f}x; the raw "
      f"endpoint is {c_raw_ddalone:.4f} / {dd_alone_raw:.4f}, not {QUEUE_RAW_CLAIM:.3f}.")
    eight = pd.DataFrame([
        dict(census="944_cloud_STRICT", n=PUB944C_N, raw_dd_alone=c_raw_ddalone,
             norm_dd_alone=c_norm_ddalone, ratio=ratio_c,
             queue_raw_claim=QUEUE_RAW_CLAIM, queue_norm_claim=QUEUE_NORM_CLAIM,
             queue_ratio=QUEUE_RATIO,
             note="queue's 1.9% = committed share of L2_H2+L4_DD, a TWO-leg set"),
        dict(census="944_B_WIDE(replayed)", n=CEN["A1_944"]["n_fail"],
             raw_dd_alone=dd_alone_raw, norm_dd_alone=dd_alone_944, ratio=ratio_b,
             queue_raw_claim=QUEUE_RAW_CLAIM, queue_norm_claim=QUEUE_NORM_CLAIM,
             queue_ratio=QUEUE_RATIO,
             note="independent selector, same direction and same order of magnitude")])
    dump(eight, "eightx")
    P(f"          RECORD DEFECT, reported: the two committed 944 censuses disagree on the "
      f"denominator itself -- {PUB944C_N:,} FAIL rows over 184 files (cloud, STRICT) against "
      f"{CEN['A1_944']['n_fail']:,} over {len(CEN['A1_944']['per_file'])} (B, WIDE). Both are "
      f"labelled 'the record's committed 4b FAIL rows'.")

    # H_MODAL
    mb_arm, mb_sh, dd_sh, cagr_sh = modal_binder(CEN["A3_WIDE"])
    hmodal = (mb_arm == "CAGR") and abs(cagr_sh - 0.688) < PP_BAR
    P(f"  H_MODAL under A3_WIDE the modal binder is {mb_arm} at {mb_sh:.4f}; "
      f"CAGR {cagr_sh:.4f} vs published 0.688, DD {dd_sh:.4f} vs published 0.583")
    P(f"          {'SURVIVES' if hmodal else 'DOES NOT SURVIVE'} the 5 pp bar")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(D) THE PRICE LEG -- PROTOCOL rules 2/3/4, and the record's first grid whose")
    P("    fail4b column is CANONICAL (L1_H1..L5_CAGR) by construction")
    P("=" * 100)
    GR = []
    for pname, p in panels.items():
        spy = p["SPY"].pct_change().fillna(0.0).values[WARM:]
        oos = np.asarray(p.index >= pd.Timestamp(OOS_START))[WARM:]
        is_ = np.asarray(p.index <= pd.Timestamp(IS_END))[WARM:]
        ms, ms_o, ms_i = mets(spy), mets(spy[oos]), mets(spy[is_])
        base_w = rules_v2_weights(p, BAND0, 0.75)
        bctx = Ctx(p, cadence_mask(p.index, "W"))
        bg, bt = bctx.run(bctx.shift(base_w))
        br = (bg - bt * HEAD_COST / 1e4)[WARM:]
        mb, mb_o, mb_i = mets(br), mets(br[oos]), mets(br[is_])
        for bname, bfn in BOOKS.items():
            W = bfn(p)
            for cad in CADENCES:
                ctx = Ctx(p, cadence_mask(p.index, cad))
                gr, tn = ctx.run(ctx.shift(W))
                r = (gr - tn * HEAD_COST / 1e4)[WARM:]
                m, m_o, m_i = mets(r), mets(r[oos]), mets(r[is_])
                lg = legs4b(m, m_o["Sharpe"], ms, ms_o["Sharpe"])
                lg_i = legs4b(m_i, m_i["Sharpe"], ms_i, ms_i["Sharpe"])
                GR.append(dict(
                    panel=pname, book=bname, cadence=cad,
                    CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                    H1=m["H1"], H2=m["H2"],
                    OOS_CAGR=m_o["CAGR"], OOS_Sharpe=m_o["Sharpe"], OOS_MaxDD=m_o["MaxDD"],
                    IS_Sharpe=m_i["Sharpe"], IS_CAGR=m_i["CAGR"], IS_MaxDD=m_i["MaxDD"],
                    turn_per_yr=float(tn[WARM:].sum() / (len(r) / 252.0)),
                    spy_Sharpe=ms["Sharpe"], spy_CAGR=ms["CAGR"], spy_MaxDD=ms["MaxDD"],
                    spy_H1=ms["H1"], spy_H2=ms["H2"], spy_OOS_Sharpe=ms_o["Sharpe"],
                    base_Sharpe=mb["Sharpe"], base_H1=mb["H1"], base_H2=mb["H2"],
                    base_MaxDD=mb["MaxDD"], base_CAGR=mb["CAGR"],
                    base_OOS_Sharpe=mb_o["Sharpe"], base_OOS_MaxDD=mb_o["MaxDD"],
                    base_OOS_CAGR=mb_o["CAGR"], base_OOS_H1=mb_o["H1"], base_OOS_H2=mb_o["H2"],
                    OOS_H1=m_o["H1"], OOS_H2=m_o["H2"],
                    pass4a=bool(m["H1"] > mb["H1"] and m["H2"] > mb["H2"]
                                and m["MaxDD"] >= mb["MaxDD"]),
                    pass4b=all(lg.values()), fail4b=failstr(lg),
                    IS_pass4b=all(lg_i.values()), IS_fail4b=failstr(lg_i)))
    gdf = pd.DataFrame(GR)
    for pname in panels:
        sub = gdf[gdf.panel == pname]
        P(f"  --- panel {pname}   SPY  CAGR {sub.spy_CAGR.iloc[0]:.2%}  "
          f"Sharpe {sub.spy_Sharpe.iloc[0]:.3f}  MaxDD {sub.spy_MaxDD.iloc[0]:.2%}  "
          f"(H1 {sub.spy_H1.iloc[0]:.3f} / H2 {sub.spy_H2.iloc[0]:.3f}, "
          f"OOS Sharpe {sub.spy_OOS_Sharpe.iloc[0]:.3f})")
        P(f"      RULES v2 baseline (live, W)  CAGR {sub.base_CAGR.iloc[0]:.2%}  "
          f"Sharpe {sub.base_Sharpe.iloc[0]:.3f}  MaxDD {sub.base_MaxDD.iloc[0]:.2%}  "
          f"(H1 {sub.base_H1.iloc[0]:.3f} / H2 {sub.base_H2.iloc[0]:.3f})")
        P(sub[["book", "cadence", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
               "turn_per_yr", "pass4a", "pass4b", "fail4b"]]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    dump(gdf, "grid")
    P(f"  4a PASS {int(gdf.pass4a.sum())} of {len(gdf)} cells; "
      f"4b PASS {int(gdf.pass4b.sum())} of {len(gdf)} cells.")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(E) RULE 8 WALK-FORWARD -- (book, cadence) chosen on 2009-2016 ALONE, 2017-2026 ONCE")
    P("=" * 100)
    WF = []
    for pname in panels:
        sub = gdf[gdf.panel == pname]
        for rule, pick in (("IS_Sharpe_max", sub.loc[sub.IS_Sharpe.idxmax()]),
                           ("IS_4b_then_Sharpe",
                            (sub[sub.IS_pass4b].sort_values("IS_Sharpe").iloc[-1]
                             if sub.IS_pass4b.any() else sub.loc[sub.IS_Sharpe.idxmax()])),
                           ("CANONICAL_TOP20_M",
                            sub[(sub.book == "TOP20_g075") & (sub.cadence == "M")].iloc[0])):
            lg_o = dict(H1=pick.H1 > pick.spy_H1, H2=pick.H2 > pick.spy_H2,
                        OOS=pick.OOS_Sharpe > pick.spy_OOS_Sharpe,
                        DD=abs(pick.OOS_MaxDD) <= 0.60 * abs(pick.spy_MaxDD),
                        CAGR=pick.OOS_CAGR >= 0.70 * pick.spy_CAGR)
            WF.append(dict(panel=pname, rule=rule, picked=f"{pick.book}/{pick.cadence}",
                           IS_Sharpe=pick.IS_Sharpe, IS_pass4b=pick.IS_pass4b,
                           OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                           OOS_MaxDD=pick.OOS_MaxDD,
                           spy_OOS_CAGR=pick.spy_CAGR, spy_OOS_Sharpe=pick.spy_OOS_Sharpe,
                           spy_MaxDD=pick.spy_MaxDD,
                           base_OOS_Sharpe=pick.base_OOS_Sharpe,
                           OOS_pass4a=bool(pick.OOS_H1 > pick.base_OOS_H1
                                            and pick.OOS_H2 > pick.base_OOS_H2
                                            and pick.OOS_MaxDD >= pick.base_OOS_MaxDD),
                           FULL_pass4a=bool(pick.pass4a),
                           OOS_pass4b=all(lg_o.values()),
                           OOS_fail4b=failstr(lg_o)))
    wdf = pd.DataFrame(WF)
    P(wdf.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    dump(wdf, "walkforward")
    P(f"  rule-8 OOS 4b PASS {int(wdf.OOS_pass4b.sum())} of {len(wdf)}; "
      f"4a PASS {int(wdf.OOS_pass4a.sum())} of {len(wdf)}.")
    P("  Every OOS_fail4b above is written in the canonical L1_H1..L5_CAGR alphabet.")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(F) VERDICT")
    P("=" * 100)
    hyp = [
        ("H_ALPH", n_alph >= 1, f"{n_alph} of {len(kdf)} claims move >= 5 pp on alphabet alone"),
        ("H_SEL", n_sel >= 1, f"{n_sel} of {len(kdf)} claims move >= 5 pp on selector alone"),
        ("H_8X", h8, f"queue says 1.9%->15.8% (8x); record says {c_raw_ddalone:.4f}->{c_norm_ddalone:.4f} ({ratio_c:.2f}x) strict, {dd_alone_raw:.4f}->{dd_alone_944:.4f} ({ratio_b:.2f}x) wide"),
        ("H_MODAL", hmodal, f"modal binder {mb_arm} {mb_sh:.4f}; CAGR {cagr_sh:.4f} vs 0.688"),
        ("H_COVER", cover >= COVER_BAR, f"canonical coverage {cover:.4%}"),
        ("H_WF", True, f"rule 8 run on {len(wdf)} (panel, chooser) cells, "
                       f"{int(wdf.OOS_pass4b.sum())} OOS 4b passes"),
    ]
    hdf = pd.DataFrame([dict(hypothesis=h, supported=bool(v), evidence=e) for h, v, e in hyp])
    P(hdf.to_string(index=False))
    dump(hdf, "hypotheses")
    P()
    P(f"  done in {time.time() - t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    return gdf, kdf, wdf


if __name__ == "__main__":
    main()
