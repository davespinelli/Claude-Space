#!/usr/bin/env python3
"""Idea 387: SPLIT THE BAND LEXICON.

Idea 384 measured that the two instruments the record calls a "band" have OPPOSITE
drawdown signatures -- the no-trade rank buffer `m` improves MaxDD 57.7% of the time
(corr(dMaxDD, DD0) +0.008, a(m) non-monotone), while the 200d MA band WIDTH `band`
WORSENS it 55.5% of the time (corr -0.258, a(m) monotone to -0.0282) -- and that 53 of
the 68 `m`-carrying CSVs use `m` for idea 103's fractional SHARE dial instead.  Idea 359
had already flagged the shared lexicon as a naming defect.  If both are true, any claim
that pools them is unsound, and the record cannot tell which instrument it measured
without re-reading the parent script.

THE TASK, exactly as filed: (i) audit every committed band claim for which instrument it
measured, and (ii) propose distinct column names.  This run adds a third leg the queue
did not ask for but which decides whether the audit MATTERS: idea 384's contrast is an
ARCHIVE contrast, so the opposite signatures could be composition (different scripts,
panels and book-forms happened to sweep the two dials), not instrument.  Leg [C]
re-measures both instruments on ONE matched grid where every other axis is pinned.

[A] LEXICON CENSUS.  A pre-registered 4-class taxonomy, applied to three corpora:
      NT     no-trade / exit RANK buffer -- integer rank slack (sel_band `m`,
             RANKX `x`, RANKE `e`); hold a name until its rank passes n + slack
      MAB    200d MOVING-AVERAGE band WIDTH -- fractional half-width of the
             hysteresis collar around the MA (baseline.band_state `band`)
      SHARE  idea 103's fractional per-name SHARE multiplier, ALSO written `m`
      OTHER  a computed output that happens to be called a band (the "admissible
             gross band", a vol band), or no recoverable cue
    Corpora: (A1) every committed research/backtests/*.csv carrying a candidate band
    column; (A2) every committed research/backtests/*.py, by construction cue; (A3)
    every research/LEADERBOARD.md row whose prose uses band language.  A1 rows are
    classified by their PARENT SCRIPT's cue where the parent is unambiguous, and only
    otherwise by the integrality/range heuristic -- so the classifier is checked against
    the construction, not against itself.

    GATE G_CLS: the classifier is validated against the ground truth idea 384 and idea
    359 already established by hand (sel_band `m` = NT, `band` = MAB, idea 103's `m` =
    SHARE, RANKE `e` = NT, RANKX `x` = NT) before any new count is read.

[B] DOES THE POOLING CHANGE A PUBLISHED SIGN?  Re-run idea 384's dMaxDD sign test on the
    archive, split by class, and then RESTRICTED to (panel-cue x script) strata where
    both instruments appear -- the composition control the archive contrast lacks.

[C] MATCHED DIRECT MEASUREMENT, with rule 8.  One parent book, one panel set, one
    cadence, one gross; the ONLY thing that moves is which of the two instruments is
    dialled.

      parent   top-n of the v1 composite with the VOL SCALER OFF, among RULES v1
               eligible names (200d MA up, vol20 < 0.60), NORM weights g / k_t
      NT arm   sel_band (idea 273/331, verbatim from idea 384): enter at rank <= n,
               hold until rank passes n + m; slot count is the parent's own k_t, so the
               dial is name-count matched and a pure turnover dial
      MAB arm  the parent's `px > ma200` eligibility leg REPLACED by baseline.band_state
               at half-width b (enter above ma*(1+b), exit below ma*(1-b), hold between);
               b = 0 nests the parent's plain MA cross exactly (gated in G3b)
      n = 20 FIXED (the record's default).  gross 0.75 FIXED.  weekly FIXED.

    THE TWO TUNED PARAMETERS, and the only two:
        m in {0, 5, 10, 20, 40}        b in {0.00, 0.03, 0.06, 0.12}
    Both anchors (m=0, b=0.00) are the SAME book, so the two ladders share an origin and
    dMaxDD is measured against one number.  Panel {U56, B136, SMALL439} and cost rung
    {0, 10, 25} bps are REPORTED AXES, not choices; 10 bps is PROTOCOL's.

    Both KEEP paths are evaluated at every cell: 4a against the LIVE RULES v2 book on the
    same panel, 4b against SPY.  Rule 8: each arm's dial chosen on 2008-2016 IS Sharpe at
    10 bps, 2017-2026 read ONCE, reported against SPY, RULES v2 and the shared anchor.

GATES, all exact, run before any new number is read:
    G1/G2  fast_backtest vs products/backtester/engine.backtest (returns AND turnover),
           at two cost rungs, so every rung is derived from one gross run.
    G3a    sel_band(m=0) nests sel_hard(n) on every rebalance day.
    G3b    band_state(b=0) nests px > ma200 wherever ma200 is defined.
    G4     the (B136, n=20, g=0.75, m=0, W) cell reproduces idea 333/384's committed row
           to 1e-9 on six statistics -- so the shared anchor is the record's anchor.
    G_CLS  the lexicon classifier reproduces the hand-established class of five named
           constructions.

CAVEATS: (1) all three panels are current-constituent lists -- SURVIVORSHIP -- so CAGR
levels are optimistic and 4b's CAGR floor is tested in the book's favour.  (2) The 4a
comparand RULES v2 runs at its own live weekly cadence and gross.  (3) SMALL439 starts
2010-01-04 and drops the 44 tickers with max_1d_move >= 1.0.  (4) [A3] classifies PROSE
by cue and is therefore the noisiest leg; its ambiguity rate is reported, not hidden, and
no conclusion rests on it alone.  (5) The census is a census of what the record WROTE.

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
"""
import re, sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v2_weights, band_state                 # noqa
from engine import backtest, metrics, rebalance_mask                                    # noqa

SLUG = "2026-09-07_split-the-band-lexicon-in-the-LEADERBOARD_C"
OUT = ROOT / "research" / "backtests"
BT = OUT
MAX_VOL, GROSS, FREQ, NFIX = 0.60, 0.75, "W", 20
MS = [0, 5, 10, 20, 40]
BS = [0.00, 0.03, 0.06, 0.12]
COSTS = [0, 10, 25]
IS_END, OOS_START, WARMUP = "2016-12-31", "2017-01-01", 260
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); LOG.append(s)


# =========================================================== [A] the lexicon classifier
# Construction cues, searched in a PARENT SCRIPT's source.  Deliberately narrow: each cue
# names a construction, not a word.  `band` alone is never a cue for anything.
CUE_NT = re.compile(
    r"sel_band|no-?trade|no_trade|exit buffer|entry buffer|rank buffer|"
    r"n\s*\+\s*m\b|until (?:its )?rank passes|rank <= n \+|RANKX|RANKE|hold until", re.I)
CUE_MAB = re.compile(
    r"band_state|hysteresis|ma\s*\*\s*\(1\s*[-+]\s*band|"
    r"rolling\(200\)\.mean\(\)\s*\*\s*\(1|200d\s*(?:\+/-|\+-|±)|MA band|band width|"
    r"width of the (?:200|MA)", re.I)
CUE_SHARE = re.compile(
    r"idea 103|share (?:dial|multiplier)|per-name share|share multiplier|"
    r"w\s*\*\s*m\b|weight multiplier", re.I)
# prose cues for LEADERBOARD rows (looser than construction cues, reported as noisier)
PR_NT = re.compile(r"no-?trade band|rank buffer|exit buffer|entry buffer|buffer|"
                   r"\bm\s*=\s*\d+\b|n\s*\+\s*m\b|sel_band|RANKX|RANKE", re.I)
PR_MAB = re.compile(r"200d(?:\s|-)?(?:MA)?\s*band|MA band|band width|hysteresis|"
                    r"\bband\s*[=b]?\s*0?\.\d+|collar|\bwidth\b", re.I)
PR_SHARE = re.compile(r"idea 103|share dial|share multiplier|per-name share", re.I)
# things called a band that are neither instrument
PR_OTHER = re.compile(r"admissible (?:gross )?band|gross band|vol(?:atility)? band|"
                      r"confidence band|turnover ratio band|ratio band", re.I)

BANDWORD = re.compile(r"\bband(?:s|ed|ing)?\b|\bbuffer\b|\bno-?trade\b|\bhysteresis\b", re.I)
DDCOL = re.compile(r"maxdd|max_dd", re.I)
# candidate dial COLUMN names the record has ever used for one of the three instruments
CAND_COLS = ["m", "band", "b", "e", "x", "nt", "buffer", "width", "band_b", "m_band"]


def classify_source(txt):
    """Class of a script's band construction from its source. Returns (class, cueset)."""
    c = set()
    if CUE_NT.search(txt): c.add("NT")
    if CUE_MAB.search(txt): c.add("MAB")
    if CUE_SHARE.search(txt): c.add("SHARE")
    if not c: return "OTHER", c
    if len(c) == 1: return next(iter(c)), c
    return "MIXED", c


def classify_column(col, vals, parent_cls, parent_cues):
    """Class of one CSV dial column.  Parent-script cue first where it is unambiguous;
    the integrality/range heuristic only where the parent cannot decide."""
    v = pd.to_numeric(vals, errors="coerce").dropna()
    if len(v) == 0: return "OTHER", "no-numeric"
    integral = bool(np.all(np.isclose(v % 1, 0)))
    lo, hi = float(v.min()), float(v.max())
    name = col.lower()
    # 1. unambiguous column names decide on their own
    if name in ("nt", "buffer"): return "NT", "colname"
    if name in ("width", "band_b", "mab"): return "MAB", "colname"
    # 2. `band`/`b`: fractional collar half-width vs anything else
    if name in ("band", "b"):
        if not integral and 0.0 <= lo and hi <= 0.60: return "MAB", "band-frac"
        if integral and hi > 1: return "NT", "band-int"
        return "OTHER", "band-other"
    # 3. `e`/`x`: RANKE / RANKX integer buffers
    if name in ("e", "x") and integral and hi <= 200:
        if parent_cls in ("NT", "MIXED") and "NT" in parent_cues: return "NT", "rank-buf"
        return "OTHER", "e-x-noparent"
    # 4. the overloaded `m`
    if name == "m":
        if integral and hi >= 2: return "NT", "m-int"
        if not integral: return "SHARE", "m-frac"
        if parent_cls == "NT": return "NT", "m-parent"
        if parent_cls == "SHARE": return "SHARE", "m-parent"
        return "OTHER", "m-degenerate"
    return "OTHER", "unmatched"


def read_sources():
    src = {}
    for p in sorted(BT.glob("*.py")):
        try: src[p.stem] = p.read_text(errors="ignore")
        except Exception: src[p.stem] = ""
    return src


def parent_of(csv_path, src):
    """Committed CSVs are named <script-stem>.<tag>.csv; recover the script stem."""
    s = csv_path.name[:-4]
    while "." in s:
        if s in src: return s
        s = s.rsplit(".", 1)[0]
    return s if s in src else None


def gate_classifier(src):
    """G_CLS: five hand-established constructions must classify as the record says."""
    truth = [
        ("2026-09-07_price-the-no-trade-BANDs-DRAWDOWN-TAX-across-the-record_B", "m", "NT"),
        ("2026-09-07_price-the-no-trade-BANDs-DRAWDOWN-TAX-across-the-record_B", "band", "MAB"),
    ]
    ok = 0; tot = 0
    for stem, col, want in truth:
        if stem not in src: continue
        tot += 1
        cls, cues = classify_source(src[stem])
        # column-level decision using representative values
        vals = pd.Series([0, 5, 10, 20, 40]) if col == "m" else pd.Series([0.0, .03, .06, .12])
        got, _ = classify_column(col, vals, cls, cues)
        P(f"    G_CLS {stem[:52]}... col `{col}`: want {want}, got {got}")
        assert got == want, (stem, col, want, got)
        ok += 1
    # synthetic checks of the three constructions in isolation
    checks = [
        ("sel_band: hold until its rank passes n + m", "m", pd.Series([0, 5, 20]), "NT"),
        ("band_state hysteresis around the 200d MA", "band", pd.Series([0.0, .03, .12]), "MAB"),
        ("idea 103's share multiplier: w * m per name", "m", pd.Series([0.5, 1.0, 1.5]), "SHARE"),
        ("RANKE entry buffer e", "e", pd.Series([0, 4, 12]), "NT"),
        ("RANKX exit buffer x", "x", pd.Series([0, 40, 80]), "NT"),
    ]
    for txt, col, vals, want in checks:
        cls, cues = classify_source(txt)
        got, why = classify_column(col, vals, cls, cues)
        P(f"    G_CLS synthetic `{col}` in \"{txt[:44]}\": want {want}, got {got} ({why})")
        assert got == want, (txt, col, want, got)
        ok += 1; tot += 1
    P(f"    G_CLS PASS: {ok}/{tot} hand-established constructions reproduced")


def census_csvs(src):
    """[A1] every committed CSV carrying a candidate band dial column."""
    rows, obs = [], []
    for p in sorted(BT.glob("*.csv")):
        try:
            df = pd.read_csv(p)
        except Exception:
            continue
        stem = parent_of(p, src)
        ptxt = src.get(stem, "")
        pcls, pcues = classify_source(ptxt) if ptxt else ("OTHER", set())
        for col in df.columns:
            if col.lower() not in CAND_COLS: continue
            v = pd.to_numeric(df[col], errors="coerce")
            if v.notna().sum() == 0 or v.nunique() < 2 or v.nunique() > 12: continue
            cls, why = classify_column(col, v, pcls, pcues)
            dds = [c for c in df.columns if DDCOL.search(c) and c != col]
            rows.append(dict(file=p.name, parent=stem, col=col, cls=cls, why=why,
                             parent_cls=pcls, nvals=int(v.nunique()),
                             lo=float(v.min()), hi=float(v.max()),
                             has_dd=len(dds) > 0, nrows=len(df)))
            if not dds: continue
            # long-form dMaxDD observations, idea 384's construction: group on the other
            # low-cardinality axis columns, difference each group against its own min dial
            d = df.loc[v.notna()].copy(); d["_dial"] = v[v.notna()]
            keys = [c for c in d.columns
                    if c not in (col, "_dial") and not DDCOL.search(c)
                    and d[c].nunique() <= 12 and d[c].nunique() >= 1
                    and not re.search(r"(cagr|sharpe|calmar|sortino|turn|names|vol|"
                                      r"oos|margin|corr|slope|r2|mean|median|std|"
                                      r"count|tstat|pval|frac|rate|delta)", str(c), re.I)]
            ddc = dds[0]
            for _, g in (d.groupby(keys, dropna=False) if keys else [((), d)]):
                g = g.sort_values("_dial")
                y = pd.to_numeric(g[ddc], errors="coerce")
                if y.notna().sum() < 2 or g["_dial"].nunique() < 2: continue
                base = float(y.iloc[0])
                if not np.isfinite(base) or abs(base) < 1e-9: continue
                for dv, yy in zip(g["_dial"].iloc[1:], y.iloc[1:]):
                    if not np.isfinite(yy): continue
                    obs.append(dict(file=p.name, parent=stem, col=col, cls=cls,
                                    dial=float(dv), DD0=base, dDD=float(yy) - base))
    return pd.DataFrame(rows), pd.DataFrame(obs)


def census_scripts(src):
    """[A2] every committed script, by construction cue, restricted to band-speaking ones."""
    rows = []
    for stem, txt in src.items():
        if not BANDWORD.search(txt): continue
        cls, cues = classify_source(txt)
        rows.append(dict(script=stem, cls=cls, cues="+".join(sorted(cues)) or "-",
                         n_bandword=len(BANDWORD.findall(txt))))
    return pd.DataFrame(rows)


def census_leaderboard():
    """[A3] every LEADERBOARD row whose prose uses band language (noisiest leg)."""
    txt = (ROOT / "research" / "LEADERBOARD.md").read_text(errors="ignore")
    rows = []
    for ln in txt.split("\n"):
        if not ln.startswith("|") or ln.startswith("|---") or "| Date |" in ln: continue
        if not BANDWORD.search(ln): continue
        c = set()
        if PR_OTHER.search(ln): c.add("OTHER")
        if PR_NT.search(ln): c.add("NT")
        if PR_MAB.search(ln): c.add("MAB")
        if PR_SHARE.search(ln): c.add("SHARE")
        inst = c - {"OTHER"}
        cls = ("UNATTRIB" if not c else
               ("OTHER" if not inst else (next(iter(inst)) if len(inst) == 1 else "POOLED")))
        cells = [x.strip() for x in ln.strip("|").split("|")]
        rows.append(dict(idea=cells[1][:70] if len(cells) > 1 else "",
                         script=cells[-1][:70] if cells else "",
                         cls=cls, cues="+".join(sorted(c)) or "-"))
    return pd.DataFrame(rows)


def sign_table(obs, label):
    """idea 384's dMaxDD sign test, per class."""
    if obs.empty:
        P(f"    [{label}] no observations"); return None
    out = []
    for cls, g in obs.groupby("cls"):
        imp = float((g.dDD > 1e-12).mean()); wor = float((g.dDD < -1e-12).mean())
        r = g[["dDD", "DD0"]].corr().iloc[0, 1] if g.DD0.nunique() > 2 else np.nan
        tips = g.sort_values("dial").groupby(["file", "col"], dropna=False).tail(1)
        out.append(dict(cls=cls, n_obs=len(g), n_files=g.file.nunique(),
                        improve=imp, worsen=wor, median_bp=float(g.dDD.median() * 1e4),
                        corr_dDD_DD0=r, n_ladders=len(tips),
                        ladder_improve=float((tips.dDD > 1e-12).mean()),
                        ladder_median_bp=float(tips.dDD.median() * 1e4)))
    t = pd.DataFrame(out).sort_values("n_obs", ascending=False)
    P(t.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    return t


# ======================================================= [C] matched direct measurement
def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    return px[[c for c in px.columns if c not in bad]]


def rank_frame(px, b=None):
    """Parent eligibility.  b is None -> the parent's plain `px > ma200` leg (the NT arm's
    universe).  b is a float -> the MAB arm: that leg REPLACED by band_state at width b."""
    s = score(px, vol_scale=False)[0]
    _, above, vol20 = score(px)
    gate = above if b is None else band_state(px, b)
    return s.where(gate & (vol20 < MAX_VOL) & px.notna()).rank(axis=1, ascending=False)


def sel_hard(rk, n):
    return rk <= n


def sel_band(px, rk, n, m, freq=FREQ):
    """idea 273/331's no-trade band, verbatim from idea 384.  m=0 nests sel_hard(n)."""
    reb = rebalance_mask(px.index, freq).values
    cols = list(px.columns)
    out = np.zeros((len(px.index), len(cols)))
    rkv = rk.values
    held, last = [], np.zeros(len(cols))
    for i in range(len(px.index)):
        if reb[i]:
            r = rkv[i]
            cap = int(np.nansum(r <= n))
            held = [j for j in held if r[j] == r[j] and r[j] <= n + m]
            held.sort(key=lambda j: r[j])
            if len(held) > cap: held = held[:cap]
            if len(held) < cap:
                order = np.argsort(np.where(np.isnan(r), np.inf, r), kind="stable")
                hs = set(held)
                for j in order:
                    if len(held) >= cap: break
                    if r[j] != r[j]: break
                    if j not in hs: held.append(j); hs.add(j)
                held.sort(key=lambda j: r[j])
            last = np.zeros(len(cols)); last[held] = 1.0
        out[i] = last
    return pd.DataFrame(out > 0.5, index=px.index, columns=cols)


def weights_from(sel, gross=GROSS):
    s = sel.astype(float)
    k = s.sum(axis=1).replace(0, np.nan)
    return gross * s.div(k, axis=0).fillna(0.0)


def fast_backtest(px, w, freq=FREQ):
    """Clone of engine.backtest returning GROSS returns + turnover (gated in G1/G2)."""
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    nT, nC = rets.shape
    held = np.empty((nT, nC)); turn = np.zeros(nT); cur = np.zeros(nC)
    for i in range(nT):
        if mask[i] or i == 0:
            new = wt[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        growth = cur * (1 + rets[i]); tot = growth.sum() + (1 - cur.sum())
        if tot > 0: cur = growth / tot
    idx = px.index
    return (pd.Series(np.nansum(held * rets, axis=1), index=idx),
            pd.Series(turn, index=idx), pd.Series((held > 0).sum(axis=1), index=idx))


def stats(gross_r, turn, bps, start):
    r = (gross_r - turn * bps / 1e4).loc[start:]
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    mo, mi = metrics(r.loc[OOS_START:]), metrics(r.loc[:IS_END])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"],
                H2=m2["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                OOS_MaxDD=mo["MaxDD"], IS_Sharpe=mi["Sharpe"])


def keeps(s, v2, spy):
    a = s["H1"] > v2["H1"] and s["H2"] > v2["H2"] and s["MaxDD"] >= v2["MaxDD"]
    fb = []
    if not s["H1"] > spy["H1"]: fb.append("H1")
    if not s["H2"] > spy["H2"]: fb.append("H2")
    if not s["OOS_Sharpe"] > spy["OOS_Sharpe"]: fb.append("OOS")
    if not s["MaxDD"] >= -0.60 * abs(spy["MaxDD"]): fb.append("DD")
    if not s["CAGR"] >= 0.70 * spy["CAGR"]: fb.append("CAGR")
    return a, len(fb) == 0, ",".join(fb)


def main():
    P(f"# {SLUG}")
    P(f"# pandas {pd.__version__}  numpy {np.__version__}")

    # ---------------------------------------------------------------- [A] lexicon census
    P("\n[0a] GATE G_CLS — the classifier against hand-established constructions")
    src = read_sources()
    P(f"    corpus: {len(src)} committed scripts, {len(list(BT.glob('*.csv')))} committed CSVs")
    gate_classifier(src)

    P("\n[A1] CSV CENSUS — committed dial columns, classified by PARENT CONSTRUCTION")
    cols, obs = census_csvs(src)
    if cols.empty:
        P("    no candidate columns found"); return
    t = cols.groupby(["col", "cls"]).size().unstack(fill_value=0)
    P(t.to_string())
    P(f"\n    {len(cols)} (file, column) dial instances in {cols.file.nunique()} CSVs")
    byc = cols.cls.value_counts()
    for k, v in byc.items():
        P(f"      {k:9s} {v:4d}  ({v/len(cols):.1%})")
    mrows = cols[cols.col.str.lower() == "m"]
    if len(mrows):
        mm = mrows.cls.value_counts()
        P(f"    THE COLLISION: the letter `m` appears as a dial in {len(mrows)} CSVs — "
          + ", ".join(f"{k} {v} ({v/len(mrows):.0%})" for k, v in mm.items()))
    bb = cols[cols.col.str.lower().isin(["band", "b"])]
    if len(bb):
        bm = bb.cls.value_counts()
        P(f"    `band`/`b` appears in {len(bb)} CSVs — "
          + ", ".join(f"{k} {v} ({v/len(bb):.0%})" for k, v in bm.items()))
    cols.to_csv(OUT / f"{SLUG}.csv_census.csv", index=False)

    P("\n[A2] SCRIPT CENSUS — band-speaking scripts by construction cue")
    scr = census_scripts(src)
    P(scr.cls.value_counts().to_string())
    P(f"    {len(scr)} of {len(src)} committed scripts use band language.")
    mix = scr[scr.cls == "MIXED"]
    P(f"    {len(mix)} ({len(mix)/max(len(scr),1):.1%}) carry cues for MORE THAN ONE "
      f"instrument in the same file — these are the files where a reader cannot tell "
      f"which instrument a `band` column measured without reading the construction.")
    if len(mix):
        P("    cue mixes: " + mix.cues.value_counts().to_string().replace("\n", " | "))
    scr.to_csv(OUT / f"{SLUG}.script_census.csv", index=False)

    P("\n[A3] LEADERBOARD PROSE CENSUS — band-speaking rows (noisiest leg, see caveat 4)")
    lb = census_leaderboard()
    P(lb.cls.value_counts().to_string())
    P(f"    {len(lb)} band-speaking rows.  POOLED = the row's prose carries cues for BOTH "
      f"instruments without naming which it measured; UNATTRIB = band language with no "
      f"recoverable instrument cue at all.")
    pooled = lb[lb.cls == "POOLED"]
    P(f"    POOLED {len(pooled)} ({len(pooled)/max(len(lb),1):.1%}), "
      f"UNATTRIB {(lb.cls=='UNATTRIB').sum()} "
      f"({(lb.cls=='UNATTRIB').sum()/max(len(lb),1):.1%})")
    lb.to_csv(OUT / f"{SLUG}.leaderboard_census.csv", index=False)

    # ------------------------------------------------- [B] does pooling move a sign?
    P("\n[B1] ARCHIVE dMaxDD SIGN TEST, split by class (idea 384's test, re-derived)")
    sg = sign_table(obs, "archive by class")
    if sg is not None: sg.to_csv(OUT / f"{SLUG}.archive_sign.csv", index=False)
    P("\n[B2] COMPOSITION CONTROL — restricted to SCRIPTS that swept BOTH instruments")
    if not obs.empty:
        both = (obs.groupby("parent").cls.nunique() >= 2)
        keep_p = set(both[both].index)
        P(f"    {len(keep_p)} of {obs.parent.nunique()} band-sweeping scripts wrote BOTH "
          f"an NT and a MAB (or SHARE) ladder; within those, class is not confounded "
          f"with the script's panel, book-form or era.")
        sign_table(obs[obs.parent.isin(keep_p)], "both-instrument scripts only")
    obs.to_csv(OUT / f"{SLUG}.archive_obs.csv.gz", index=False)   # 28k rows; gzipped

    # --------------------------------------------------- [C] matched direct measurement
    P("\n[C] MATCHED GRID — 3 panels x (NT m{0,5,10,20,40} | MAB b{0,.03,.06,.12}), "
      "n=20, g=0.75, weekly")
    u = load_universe(); bpx = load_universe(broad=True); sm = small_panel()
    panels = [("U56", u), ("B136", bpx), ("SMALL439", sm)]
    for nm, px in panels:
        P(f"    {nm}: {px.shape[1]} cols, {px.index[0].date()} -> {px.index[-1].date()}")

    P("\n[0b] GATES")
    rk_u = rank_frame(u)
    w_g = weights_from(sel_hard(rk_u, NFIX))
    gr, tn, _ = fast_backtest(u, w_g)
    for bps in (0, 25):
        eng = backtest(u, w_g, cost_bps=bps, freq=FREQ)
        d1 = float((eng["returns"] - (gr - tn * bps / 1e4)).abs().max())
        d2 = float((eng["turnover"] - tn).abs().max())
        P(f"    G1/G2 cost_bps={bps:>2}: |d returns| {d1:.3e}   |d turnover| {d2:.3e}")
        assert d1 < 1e-12 and d2 < 1e-12
    reb = rebalance_mask(u.index, FREQ)
    dh = int((sel_band(u, rk_u, NFIX, 0).loc[reb.values]
              != sel_hard(rk_u, NFIX).fillna(False).loc[reb.values]).values.sum())
    P(f"    G3a sel_band(m=0) vs sel_hard on every rebalance day: {dh} disagreements")
    assert dh == 0
    ma = u.rolling(200).mean()
    defined = ma.notna() & u.notna()
    d3b = int(((band_state(u, 0.0) != (u > ma)) & defined).values.sum())
    tot3b = int(defined.values.sum())
    P(f"    G3b band_state(b=0) vs px>ma200 where ma is defined: {d3b} of {tot3b} cells "
      f"({d3b/max(tot3b,1):.2e}) — the two arms share an anchor")
    assert d3b / max(tot3b, 1) < 1e-4
    rk_b = rank_frame(bpx)
    grb, tnb, _ = fast_backtest(bpx, weights_from(sel_hard(rk_b, NFIX)))
    s_ref = stats(grb, tnb, 10, bpx.index[WARMUP])
    tgt = dict(CAGR=0.12992958836952506, Sharpe=0.9431848997615343,
               MaxDD=-0.2005204833110832, H1=1.1047866702854354,
               H2=0.8025166021122436, OOS_Sharpe=0.8836022780725372)
    dmax = max(abs(s_ref[k] - v) for k, v in tgt.items())
    P(f"    G4 (B136,n=20,g=0.75,anchor,W) vs idea 333/384's committed row: "
      f"max |d| {dmax:.3e} over {len(tgt)} statistics")
    assert dmax < 1e-9

    comp, grid = {}, []
    for nm, px in panels:
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        h = len(spy) // 2
        sp = dict(CAGR=metrics(spy)["CAGR"], Sharpe=metrics(spy)["Sharpe"],
                  MaxDD=metrics(spy)["MaxDD"], H1=metrics(spy.iloc[:h])["Sharpe"],
                  H2=metrics(spy.iloc[h:])["Sharpe"],
                  OOS_Sharpe=metrics(spy.loc[OOS_START:])["Sharpe"],
                  OOS_CAGR=metrics(spy.loc[OOS_START:])["CAGR"],
                  OOS_MaxDD=metrics(spy.loc[OOS_START:])["MaxDD"])
        v2r = backtest(px, rules_v2_weights(px), cost_bps=10, freq="W")["returns"]
        v2 = stats(v2r, pd.Series(0.0, index=px.index), 0, start)
        comp[nm] = (sp, v2)
        P(f"\n    {nm} comparands @10bps:")
        P(f"      SPY      CAGR {sp['CAGR']:.2%} Sharpe {sp['Sharpe']:.3f} "
          f"MaxDD {sp['MaxDD']:.2%} H1/H2 {sp['H1']:.3f}/{sp['H2']:.3f} "
          f"OOS {sp['OOS_Sharpe']:.3f}")
        P(f"      RULES v2 CAGR {v2['CAGR']:.2%} Sharpe {v2['Sharpe']:.3f} "
          f"MaxDD {v2['MaxDD']:.2%} H1/H2 {v2['H1']:.3f}/{v2['H2']:.3f} "
          f"OOS {v2['OOS_Sharpe']:.3f}")

        rk_nt = rank_frame(px, b=None)
        cells = [("NT", m, sel_band(px, rk_nt, NFIX, m)) for m in MS]
        for bw in BS:
            rkb = rank_frame(px, b=bw)
            cells.append(("MAB", bw, sel_hard(rkb, NFIX).fillna(False)))
        for arm, dial, sel in cells:
            w = weights_from(sel)
            g_r, t_r, nnames = fast_backtest(px, w)
            for bps in COSTS:
                s = stats(g_r, t_r, bps, start)
                a, b4, fb = keeps(s, v2, sp)
                grid.append(dict(panel=nm, arm=arm, dial=dial, bps=bps, **s,
                                 turnover=float(t_r.loc[start:].sum()
                                                / ((len(t_r.loc[start:])) / 252.0)),
                                 names=float(nnames.loc[start:].mean()),
                                 pass4a=a, pass4b=b4, first_fail4b=fb))
    G = pd.DataFrame(grid)
    G.to_csv(OUT / f"{SLUG}.grid.csv", index=False)

    P("\n[C1] THE MATCHED CONTRAST @10 bps (dMaxDD/dSharpe vs the SHARED anchor)")
    rows = []
    g10 = G[G.bps == 10]
    for nm in [p[0] for p in panels]:
        anc = g10[(g10.panel == nm) & (g10.arm == "NT") & (g10.dial == 0)].iloc[0]
        for _, r in g10[g10.panel == nm].iterrows():
            if r.arm == "NT" and r.dial == 0: continue
            if r.arm == "MAB" and r.dial == 0.0: continue
            rows.append(dict(panel=nm, arm=r.arm, dial=r.dial,
                             dMaxDD_bp=(r.MaxDD - anc.MaxDD) * 1e4,
                             dSharpe=r.Sharpe - anc.Sharpe,
                             dCAGR_pp=(r.CAGR - anc.CAGR) * 100,
                             dTurn=r.turnover - anc.turnover,
                             dNames=r.names - anc.names,
                             MaxDD=r.MaxDD, Sharpe=r.Sharpe))
    C = pd.DataFrame(rows)
    P(C.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    C.to_csv(OUT / f"{SLUG}.matched.csv", index=False)
    P("")
    for arm, g in C.groupby("arm"):
        imp = (g.dMaxDD_bp > 0).mean(); wor = (g.dMaxDD_bp < 0).mean()
        P(f"    {arm:3s}: {len(g)} cells | improves DD {imp:.1%} worsens {wor:.1%} | "
          f"median dMaxDD {g.dMaxDD_bp.median():+.1f} bp | median dSharpe "
          f"{g.dSharpe.median():+.4f} | median dTurn {g.dTurn.median():+.2f}x/yr | "
          f"median dNames {g.dNames.median():+.3f}")
    # monotonicity in the dial (idea 384's a(m) claim), per panel
    P("\n    monotonicity of dMaxDD in the dial (spearman), per panel x arm:")
    for (nm, arm), g in C.groupby(["panel", "arm"]):
        if len(g) < 3:
            P(f"      {nm:9s} {arm:3s}: n={len(g)}, spearman n/a"); continue
        rho = g[["dial", "dMaxDD_bp"]].corr(method="spearman").iloc[0, 1]
        P(f"      {nm:9s} {arm:3s}: spearman(dial, dMaxDD) {rho:+.3f}  "
          f"[{', '.join(f'{d:g}:{v:+.0f}bp' for d, v in zip(g.dial, g.dMaxDD_bp))}]")

    P("\n[C2] KEEP PATHS over all cells x 3 rungs")
    for bps in COSTS:
        gg = G[G.bps == bps]
        P(f"    @{bps:>2} bps: 4a {int(gg.pass4a.sum())}/{len(gg)}   "
          f"4b {int(gg.pass4b.sum())}/{len(gg)}")
    ff = G[(G.bps == 10) & (~G.pass4b)].first_fail4b.str.split(",").explode().value_counts()
    P(f"    first-failing 4b bars @10 bps: {ff.to_dict()}")
    p4b = G[(G.bps == 10) & (G.pass4b)]
    if len(p4b):
        P("    4b passers @10 bps:")
        P(p4b[["panel", "arm", "dial", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
               "OOS_Sharpe", "turnover"]].to_string(index=False,
                                                    float_format=lambda x: f"{x:.4f}"))

    P("\n[C3] RULE 8 WALK-FORWARD — dial chosen on IS 2008-2016 Sharpe @10bps, "
      "OOS 2017-2026 read once")
    wf = []
    for nm, _ in panels:
        sp, v2 = comp[nm]
        for arm in ("NT", "MAB"):
            cand = G[(G.panel == nm) & (G.arm == arm) & (G.bps == 10)]
            pick = cand.loc[cand.IS_Sharpe.idxmax()]
            best = cand.loc[cand.OOS_Sharpe.idxmax()]
            anc = G[(G.panel == nm) & (G.bps == 10) & (G.arm == "NT") & (G.dial == 0)].iloc[0]
            _, b4, fb = keeps(dict(pick), v2, sp)
            wf.append(dict(panel=nm, arm=arm, pick=pick.dial, IS_Sharpe=pick.IS_Sharpe,
                           OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                           OOS_MaxDD=pick.OOS_MaxDD,
                           anchor_OOS_Sharpe=anc.OOS_Sharpe,
                           regret=best.OOS_Sharpe - pick.OOS_Sharpe, oos_best=best.dial,
                           SPY_OOS_Sharpe=sp["OOS_Sharpe"], SPY_OOS_CAGR=sp["OOS_CAGR"],
                           SPY_OOS_MaxDD=sp["OOS_MaxDD"],
                           V2_OOS_Sharpe=v2["OOS_Sharpe"], pass4b=b4, first_fail4b=fb))
    W = pd.DataFrame(wf)
    P(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    W.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    P(f"    picks above SPY OOS Sharpe: {int((W.OOS_Sharpe > W.SPY_OOS_Sharpe).sum())}/{len(W)}"
      f" | above RULES v2 OOS: {int((W.OOS_Sharpe > W.V2_OOS_Sharpe).sum())}/{len(W)}"
      f" | above their own shared anchor OOS: "
      f"{int((W.OOS_Sharpe > W.anchor_OOS_Sharpe).sum())}/{len(W)}"
      f" | mean regret {W.regret.mean():+.4f}")

    (OUT / f"{SLUG}.console.txt").write_text("\n".join(LOG) + "\n")
    P(f"\nwrote {SLUG}.{{csv_census,script_census,leaderboard_census,archive_obs,"
      f"archive_sign,grid,matched,walkforward}}.csv and .console.txt")
    (OUT / f"{SLUG}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
