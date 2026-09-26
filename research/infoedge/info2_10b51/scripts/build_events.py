"""Turn the ecd (Item 408(a)) XBRL facts extracted from the SEC notes data sets into one row per
(filing, person, action) and classify each termination.

Inputs : cache/extract/*.{sub,ecdtxt,ecdnum,dei,dim}.parquet   (from extract_fsn.py)
Outputs: data/arrangements.csv.gz   every tagged adoption / termination record, classified
         data/filings.csv.gz        every original 10-Q/10-K with its Item 408 tag status
         data/coverage_by_month.csv share of 10-Q/10-K filings carrying the ecd flags, by month

Classification of a termination (point in time: only the disclosing filing is used):
  expired      the text says the plan expired / ended by its terms / all trades completed, or the
               termination date is on or after the tagged scheduled expiration date
  replacement  the same person also adopted a trading arrangement in the same filing, or the text
               says the plan was modified / amended / replaced / superseded
  early        everything else (the pre-registered event)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sec

EXT = sec.CACHE / "extract"
DATA = sec.ROOT / "data"
DATA.mkdir(exist_ok=True)

TAGS_408 = ["Rule10b51ArrAdoptedFlag", "Rule10b51ArrTrmntdFlag", "NonRule10b51ArrAdoptedFlag",
            "NonRule10b51ArrTrmntdFlag", "TrdArrIndName", "TrdArrIndTitle", "TrdArrAdoptionDate",
            "TrdArrTerminationDate", "TrdArrExpirationDate", "TrdArrDuration", "MtrlTermsOfTrdArrTextBlock"]
ORIG_FORMS = {"10-Q", "10-K", "10-KT", "10-QT"}

# --------------------------------------------------------------------------- text rules
RX_CEO = re.compile(r"\bchief\s+executive\b|\bC\.?E\.?O\.?\b|principal\s+executive\s+officer", re.I)
RX_CFO = re.compile(r"\bchief\s+financial\b|\bC\.?F\.?O\.?\b|principal\s+financial\s+officer", re.I)
RX_DIR = re.compile(r"(?<!managing\s)(?<!senior\s)(?<!associate\s)(?<!regional\s)(?<!medical\s)"
                    r"(?<!technical\s)(?<!creative\s)(?<!art\s)\bdirector\b(?!\s+of\b)(?!\s*,\s*(?:sales|finance|"
                    r"marketing|operations|human|investor|research|engineering|global|corporate|tax))"
                    r"|\bchair(?:man|woman|person)?\b|\bboard\s+member\b|member\s+of\s+the\s+board", re.I)
RX_EARLY = re.compile(
    r"(?:prior\s+to|before)\s+(?:its|the|their|such)\s+(?:(?:scheduled|stated|original|expected|planned)\s+)?"
    r"(?:expiration|expiry|end|termination\s+date|maturity|completion)"
    r"|early\s+terminat|terminated\s+early|would\s+have\s+(?:otherwise\s+)?(?:expired|terminated|ended|remained)"
    r"|(?:was|were|had\s+been)\s+(?:originally\s+)?scheduled\s+to\s+(?:expire|terminate|end|remain)"
    r"|originally\s+scheduled|otherwise\s+(?:would\s+have\s+)?(?:expire|terminate)", re.I)
RX_EXPIRED = re.compile(
    r"\bexpired\b|\bmatured\b|\bexpir(?:ed|ation)\s+(?:by|in\s+accordance\s+with|pursuant\s+to)\s+its"
    r"|terminated\s+(?:automatically|pursuant\s+to\s+its\s+terms|by\s+its\s+(?:own\s+)?terms|in\s+accordance\s+with\s+its"
    r"|upon\s+(?:its\s+)?(?:scheduled\s+)?expiration|upon\s+(?:the\s+)?completion|upon\s+(?:the\s+)?(?:sale|execution))"
    r"|in\s+accordance\s+with\s+(?:its|the\s+plan.?s|the\s+arrangement.?s)\s+terms"
    r"|upon\s+(?:the\s+)?(?:completion|execution|sale)\s+of\s+all"
    r"|all\s+(?:of\s+the\s+)?(?:shares|securities|trades|sales|transactions)[^.]{0,80}(?:sold|executed|completed)"
    r"|completion\s+of\s+(?:all\s+)?(?:the\s+)?(?:sales|trades|transactions)|fully\s+(?:executed|completed|exercised)"
    r"|natural\s+expiration|end\s+of\s+(?:its|the)\s+term", re.I)
RX_MODIFY = re.compile(
    r"terminat\w*[^.]{0,150}(?:in\s+connection\s+with|in\s+order\s+to|so\s+as\s+to|to\s+(?:adopt|enter\s+into)"
    r"|and\s+(?:simultaneously\s+|subsequently\s+|concurrently\s+)?(?:adopted|entered\s+into))[^.]{0,80}"
    r"(?:new|replacement|amended|modified|subsequent|successor|another)"
    r"|\b(?:was|were|has\s+been|have\s+been)\s+(?:modified|amended|replaced|superseded)\b(?!\s+(?:on|in|as\s+of|effective)\b)"
    r"|\bmodification\s+of\s+(?:a|an|the|his|her|their)\b|\b(?:modified|amended)\s+(?:his|her|their|a|an|the)\b[^.]{0,60}"
    r"(?:plan|arrangement)|\breplaced\s+(?:by|with)\b|\bsuperseded\s+by\b|\bconsidered\s+a\s+termination"
    r"|\btreated\s+as\s+(?:a\s+)?termination|\bdeemed\s+(?:a\s+)?termination"
    r"|\b(?:adopted|entered\s+into)\s+(?:a|an)\s+(?:new|replacement|successor|subsequent)\s+(?:rule\s+)?(?:10b5-1\s+)?"
    r"(?:sales\s+|trading\s+|stock\s+)?(?:plan|arrangement|contract)", re.I)
RX_BOILER = re.compile(r"(?:adopt(?:ed|s)?|enter(?:ed)?\s+into)\s*,?\s*(?:(?:modif(?:y|ied)|amend(?:ed)?)\s*,?\s*)?"
                       r"(?:or|and/or|and)\s+(?:modif(?:y|ied)\s+or\s+)?terminat(?:e|ed)", re.I)
RX_SALE = re.compile(r"\bsale\b|\bsales\b|\bsell\b|\bselling\b|\bsold\b|\bdispos", re.I)
RX_BUY = re.compile(r"\bpurchas|\bbuy\b|\bacqui", re.I)
RX_NONE_BOILER = re.compile(r"\b(?:no|none\s+of)\s+(?:our\s+|the\s+company.?s\s+)?(?:directors?|officers?)"
                            r"[^.]{0,120}(?:adopted|terminated)", re.I)


def parse_date(s) -> pd.Timestamp:
    if s is None or (isinstance(s, float) and np.isnan(s)):
        return pd.NaT
    s = str(s).strip()
    s = re.sub(r"\s+", " ", s).replace(" ,", ",")
    s = re.sub(r",(\d)", r", \1", s)
    for fmt in (None, "%B %d, %Y", "%b %d, %Y", "%m/%d/%Y", "%m/%d/%y", "%Y-%m-%d", "%d %B %Y"):
        try:
            d = pd.to_datetime(s, format=fmt) if fmt else pd.to_datetime(s)
            if pd.Timestamp("2015-01-01") <= d <= pd.Timestamp("2035-12-31"):
                return d.normalize()
        except (ValueError, TypeError, OverflowError):
            continue
    return pd.NaT


def parse_duration_days(s):
    """TrdArrDuration is an xs:duration (e.g. P365D, P1Y2M) or free text."""
    if s is None or (isinstance(s, float) and np.isnan(s)):
        return np.nan
    s = str(s).strip()
    m = re.fullmatch(r"P(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)W)?(?:(\d+)D)?", s)
    if m and any(m.groups()):
        y, mo, w, d = (int(x) if x else 0 for x in m.groups())
        return y * 365 + mo * 30.4 + w * 7 + d
    return np.nan


def norm_name(s: str) -> str:
    s = re.sub(r"\b(mr|mrs|ms|dr|jr|sr|ii|iii|iv)\b\.?", " ", str(s).lower())
    s = re.sub(r"[^a-z ]", " ", s)
    toks = [t for t in s.split() if len(t) > 1]
    return " ".join(toks)


def seg_person(seg: str) -> str:
    """Person key from the dimension segments."""
    d = dict(x.split("=", 1) for x in seg.split(";") if "=" in x)
    return d.get("Individual") or d.get("TradingArr") or seg


def title_class(title: str, text: str = "") -> dict:
    t = title or ""
    return {"is_ceo": bool(RX_CEO.search(t)), "is_cfo": bool(RX_CFO.search(t)), "is_dir": bool(RX_DIR.search(t))}


def person_text(text: str, name: str) -> str:
    """Parts of a (possibly multi-person, possibly tabular) text block around this person's last name:
    for each mention, 80 characters before to 450 after."""
    if not text or not name:
        return text or ""
    toks = norm_name(name).split()
    if not toks:
        return text
    last = toks[-1]
    spans = [(max(0, m.start() - 80), m.start() + 450) for m in re.finditer(rf"\b{re.escape(last)}\b", text, re.I)]
    if not spans:
        return ""
    merged = [list(spans[0])]
    for a_, b_ in spans[1:]:
        if a_ <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b_)
        else:
            merged.append([a_, b_])
    return " ... ".join(text[a_:b_] for a_, b_ in merged)


MONTHS = (r"(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan\.?|Feb\.?"
          r"|Mar\.?|Apr\.?|Jun\.?|Jul\.?|Aug\.?|Sept?\.?|Oct\.?|Nov\.?|Dec\.?)")
DATE = rf"(?:{MONTHS}\s*\d{{1,2}}\s*,?\s*\d{{4}}|\d{{1,2}}/\d{{1,2}}/\d{{2,4}})"
RX_SCHED = re.compile(rf"(?:expir\w*|until|through|thru|no\s+later\s+than|earlier\s+of|end\s+date|ending\s+on"
                      rf"|scheduled\s+to\s+(?:terminate|end)|would\s+have\s+(?:otherwise\s+)?(?:terminated|ended|expired))"
                      rf"[^.]{{0,90}}?({DATE})", re.I)
RX_COMPLETED = re.compile(
    r"terminat\w*\s+(?:automatically\s+)?(?:upon|following|after|due\s+to|as\s+a\s+result\s+of)\s+(?:the\s+)?"
    r"(?:completion|execution|sale|exercise)\s+of\s+all"
    r"|all\s+(?:of\s+the\s+)?(?:shares|securities|options|trades|sales|orders)\s+(?:subject\s+to\s+[^.]{0,40})?"
    r"(?:were|had\s+been|have\s+been)\s+(?:sold|executed|exercised|completed)"
    r"|(?:became|was|were|been)\s+fully\s+(?:executed|exercised|completed|sold)"
    r"|terminat\w*\s+(?:automatically|pursuant\s+to\s+its\s+terms|by\s+its\s+(?:own\s+)?terms|in\s+accordance\s+with\s+its"
    r"|upon\s+(?:its\s+)?(?:scheduled\s+)?expiration|upon\s+(?:the\s+)?completion|upon\s+execution)"
    r"|completed\s+all\s+(?:sales|trades|transactions)|\bterminated\s+upon\s+(?:the\s+)?(?:sale|execution)", re.I)
RX_EXPIRED_WEAK = re.compile(
    r"\b(?:plan|arrangement)\s+(?:has\s+|had\s+)?expired\b|\bexpired\s+(?:on|by|in\s+accordance|pursuant|at)"
    r"|natural\s+expiration|upon\s+(?:its\s+)?(?:scheduled\s+)?expiration|\bexpiration\s+of\s+(?:the|its)\s+term", re.I)


def sched_end_from_text(c: str):
    ds = [parse_date(m.group(1)) for m in RX_SCHED.finditer(c or "")]
    ds = [d for d in ds if pd.notna(d)]
    return max(ds) if ds else pd.NaT


# --------------------------------------------------------------------------- load
def load():
    subs, txt, num, dei, dims = [], [], [], [], []
    for p in sorted(EXT.glob("*.sub.parquet")):
        stem = p.name[: -len(".sub.parquet")]
        subs.append(pd.read_parquet(p))
        txt.append(pd.read_parquet(EXT / f"{stem}.ecdtxt.parquet"))
        num.append(pd.read_parquet(EXT / f"{stem}.ecdnum.parquet"))
        dei.append(pd.read_parquet(EXT / f"{stem}.dei.parquet"))
        dims.append(pd.read_parquet(EXT / f"{stem}.dim.parquet"))
    sub = pd.concat(subs, ignore_index=True).drop_duplicates("adsh")
    txt = pd.concat(txt, ignore_index=True)
    num = pd.concat(num, ignore_index=True)
    dei = pd.concat(dei, ignore_index=True)
    dim = pd.concat(dims, ignore_index=True).drop_duplicates("dimh")
    seg = dict(zip(dim.dimh, dim.segments))
    for df in (txt, num, dei):
        df["segments"] = df["dimh"].map(seg).fillna("")
    return sub, txt, num, dei


def build():
    sub, txt, num, dei = load()
    sub["filed"] = pd.to_datetime(sub["filed"], format="%Y%m%d")
    sub["period"] = pd.to_datetime(sub["period"], format="%Y%m%d", errors="coerce")
    sub["cik"] = sub["cik"].astype(int)
    orig = sub[sub.form.isin(ORIG_FORMS)].copy()

    t = txt[txt.tag.isin(TAGS_408) & txt.adsh.isin(set(orig.adsh))].copy()
    t["value"] = t["value"].astype(str)
    t = t[t.value.str.strip() != ""]
    # ---------------- filing-level tag status and coverage
    fl = t[t.tag.isin(TAGS_408[:4])].copy()
    fl["v"] = fl.value.str.strip().str.lower().eq("true")
    fstat = fl.groupby(["adsh", "tag"]).v.max().unstack()
    orig = orig.merge(fstat, left_on="adsh", right_index=True, how="left")
    orig["ecd_tagged"] = orig[TAGS_408[:4]].notna().any(axis=1)
    orig["fm"] = orig.filed.dt.to_period("M").astype(str)
    cov = orig.groupby("fm").agg(filings=("adsh", "size"), tagged=("ecd_tagged", "sum"),
                                 trm_true=("Rule10b51ArrTrmntdFlag", lambda s: int((s == True).sum())),
                                 adopt_true=("Rule10b51ArrAdoptedFlag", lambda s: int((s == True).sum())))
    cov["tagged_share"] = (cov.tagged / cov.filings).round(3)
    cov.to_csv(DATA / "coverage_by_month.csv")

    # ---------------- context records: one per (adsh, dimension context)
    lists = t.groupby(["adsh", "segments", "tag"]).value.agg(lambda s: list(dict.fromkeys(s))).unstack()
    for c in TAGS_408:
        if c not in lists:
            lists[c] = None

    def tf(v):
        if not isinstance(v, list):
            return None
        v = [str(x).strip().lower() for x in v]
        return True if "true" in v else (False if "false" in v else None)

    def first(v):
        return v[0] if isinstance(v, list) and v else None

    rec = pd.DataFrame({
        "rule_adopt": lists.Rule10b51ArrAdoptedFlag.map(tf), "rule_trm": lists.Rule10b51ArrTrmntdFlag.map(tf),
        "nonrule_adopt": lists.NonRule10b51ArrAdoptedFlag.map(tf),
        "nonrule_trm": lists.NonRule10b51ArrTrmntdFlag.map(tf),
        "n_names": lists.TrdArrIndName.map(lambda v: len(v) if isinstance(v, list) else 0),
        "name": lists.TrdArrIndName.map(first), "title": lists.TrdArrIndTitle.map(first),
        "adopt_date_raw": lists.TrdArrAdoptionDate.map(first), "term_date_raw": lists.TrdArrTerminationDate.map(first),
        "exp_date_raw": lists.TrdArrExpirationDate.map(first), "duration_raw": lists.TrdArrDuration.map(first),
        "text": lists.MtrlTermsOfTrdArrTextBlock.map(lambda v: " ".join(v) if isinstance(v, list) else ""),
    }).reset_index()
    rec["has_dim"] = rec.segments != ""
    rec["pkey"] = rec.segments.map(seg_person)
    # numeric: planned shares in the same context
    amt = num[(num.tag == "TrdArrSecuritiesAggAvailAmt") & num.adsh.isin(set(orig.adsh))].copy()
    amt["value"] = pd.to_numeric(amt.value, errors="coerce")
    a = amt.groupby(["adsh", "segments"]).value.max().rename("agg_shares")
    rec = rec.merge(a, left_on=["adsh", "segments"], right_index=True, how="left")
    # a filing with dimensional 408 detail uses its no-dimension flags only as summary flags
    dim_filings = set(rec.loc[rec.has_dim, "adsh"])
    rec["summary_only"] = ~rec.has_dim & rec.adsh.isin(dim_filings)
    # fill name / title / shares from other contexts of the same person in the same filing
    for col in ("name", "title"):
        fill = rec[rec.has_dim & rec[col].notna()].groupby(["adsh", "pkey"])[col].first()
        idx = pd.MultiIndex.from_arrays([rec.adsh, rec.pkey])
        rec[col] = rec[col].where(rec[col].notna() | ~rec.has_dim, pd.Series(fill.reindex(idx).values, index=rec.index))
    ftext = t[(t.tag == "MtrlTermsOfTrdArrTextBlock")].groupby("adsh").value.apply(
        lambda s: " ".join(dict.fromkeys(s)))
    rec["filing_text"] = rec.adsh.map(ftext).fillna("")
    rec = rec.merge(orig[["adsh", "cik", "name", "sic", "form", "period", "filed", "accepted", "fm"]].rename(
        columns={"name": "company"}), on="adsh", how="left")

    rec["adopt_date"] = rec.adopt_date_raw.map(parse_date)
    rec["term_date"] = rec.term_date_raw.map(parse_date)
    rec["exp_date"] = rec.exp_date_raw.map(parse_date)
    rec["duration_days"] = rec.duration_raw.map(parse_duration_days)
    rec["name_norm"] = rec.name.fillna("").map(norm_name)

    def pkey_short(n):  # first initial + last name, robust to middle names / suffixes
        toks = n.split()
        return f"{toks[0][0]} {toks[-1]}" if len(toks) >= 2 else n
    rec["name_short"] = rec.name_norm.map(pkey_short)
    # identity: the Individual dimension member when the filer used one, else the tagged name
    rec["person"] = np.where(rec.has_dim, rec.pkey, rec.name_short)

    # per-context text used for classification (boilerplate "adopted or terminated" removed)
    def ctx(r):
        own = r.text if r.text else ""
        nm = r["name"] if isinstance(r["name"], str) else ""
        if own and (r.has_dim or r.n_names <= 1):
            out = own if not nm else (person_text(own, nm) or own)
        else:
            out = person_text(r.filing_text, nm) if nm else r.filing_text
        return RX_BOILER.sub(" ", out)
    rec["ctx"] = rec.apply(ctx, axis=1)
    def title_eff(r):
        if isinstance(r.title, str) and r.title.strip():
            return r.title
        nm = r["name"] if isinstance(r["name"], str) else ""
        toks = norm_name(nm).split()
        if not toks:
            return ""
        m = re.search(rf"\b{re.escape(toks[-1])}\b", r.ctx or "", re.I)
        return (r.ctx or "")[m.end(): m.end() + 120] if m else ""
    rec["title_eff"] = rec.apply(title_eff, axis=1)
    rec["title_from_text"] = rec.title.isna() & (rec.title_eff != "")
    cls = pd.DataFrame([title_class(x) for x in rec.title_eff], index=rec.index)
    rec = pd.concat([rec, cls], axis=1)
    rec["insider_target"] = rec.is_ceo | rec.is_cfo | rec.is_dir
    rec["sale_text"] = rec.ctx.str.contains(RX_SALE)
    rec["buy_text"] = rec.ctx.str.contains(RX_BUY)
    rec["purchase_only"] = rec.buy_text & ~rec.sale_text

    # ---------------- actions
    lag = pd.Timedelta(days=1)
    # a "termination date" after the filing date is a scheduled end tagged with the wrong element
    rec["trm_future_date"] = (rec.rule_trm == True) & rec.term_date.notna() & (rec.term_date > rec.filed + lag)
    rec["is_trm"] = (rec.rule_trm == True) & ~rec.trm_future_date & ~rec.summary_only
    rec["is_adopt"] = (rec.rule_adopt == True) & ~rec.summary_only & ~(
        rec.adopt_date.notna() & (rec.adopt_date > rec.filed + lag))
    # a context flagged both ways with no usable termination date and an adoption date is an adoption
    both = rec.is_trm & rec.is_adopt
    rec.loc[both & rec.term_date.isna() & rec.adopt_date.notna(), "is_trm"] = False
    rec["any_adopt"] = rec.is_adopt | ((rec.nonrule_adopt == True) & ~rec.summary_only)
    # replacement: the same person (dimension member or tagged name) adopted a plan in the same filing on or
    # after the termination date (an adoption dated before the termination is the terminated plan itself)
    ad = rec[rec.any_adopt]
    adopts = {}
    for ix, a_, p, n, d in zip(ad.index, ad.adsh, ad.person, ad.name_short, ad.adopt_date):
        for k in ((a_, p), (a_, n)):
            if k[1] and len(str(k[1])) > 3:
                adopts.setdefault(k, {})[ix] = d
    D3 = pd.Timedelta(days=3)

    def repl(ix, a_, p, n, td):
        cand = {**adopts.get((a_, p), {}), **adopts.get((a_, n), {})}
        own = cand.pop(ix, None) if ix in cand else None
        if own is not None and pd.notna(own) and pd.notna(td) and own >= td - D3:
            return True  # the context's own adoption is dated on/after the termination: a new plan
        # adoptions in the person's other contexts: dated on/after the termination, or undated
        return any(pd.isna(d) or pd.isna(td) or d >= td - D3 for d in cand.values())
    rec["same_filing_adopt"] = rec.is_trm & pd.Series(
        [repl(ix, a_, p, n, td) for ix, a_, p, n, td in zip(rec.index, rec.adsh, rec.person, rec.name_short, rec.term_date)],
        index=rec.index)
    # a termination dated well before the reporting quarter is a repeated (stale) disclosure
    rec["trm_stale"] = rec.is_trm & rec.term_date.notna() & rec.period.notna() & (
        rec.term_date < rec.period - pd.Timedelta(days=100))
    rec["person_ok"] = rec.name.notna() & ((rec.n_names <= 1) | rec.has_dim)

    rec["sched_end_text"] = [sched_end_from_text(c + " " + (d if isinstance(d, str) else ""))
                             for c, d in zip(rec.ctx, rec.duration_raw)]

    def classify(r):
        if not r.is_trm:
            return None, None
        c = r.ctx or ""
        td = r.term_date
        if r.same_filing_adopt:
            return "replacement", "same person adopted a plan in the same filing"
        if RX_MODIFY.search(c):
            return "replacement", "text: modified / replaced"
        if RX_COMPLETED.search(c):
            return "expired", "text: completed / ended by its terms"
        if pd.notna(td) and pd.notna(r.exp_date):
            return (("early", "tagged expiration date after termination") if td < r.exp_date - pd.Timedelta(days=3)
                    else ("expired", "termination on/after tagged expiration date"))
        if pd.notna(td) and pd.notna(r.sched_end_text) and r.sched_end_text > td + pd.Timedelta(days=3):
            return "early", "text: scheduled end after termination"
        if RX_EXPIRED_WEAK.search(c) and not RX_EARLY.search(c):
            return "expired", "text: expired"
        return "early", "default (no expiry / replacement cue)"
    cl = rec.apply(classify, axis=1, result_type="expand")
    rec["trm_class"], rec["trm_reason"] = cl[0], cl[1]
    keep = [c for c in rec.columns if c not in ("filing_text", "text")]  # ctx keeps the person's own passage
    rec[keep].to_csv(DATA / "arrangements.csv.gz", index=False)
    dei.to_parquet(sec.CACHE / "dei_all.parquet")
    fcols = ["adsh", "cik", "name", "sic", "form", "period", "filed", "accepted", "fm", "ecd_tagged"] + TAGS_408[:4]
    orig[fcols].to_csv(DATA / "filings.csv.gz", index=False)
    return rec, orig, cov


if __name__ == "__main__":
    rec, orig, cov = build()
    print(cov.to_string())
    tr = rec[rec.is_trm]
    print("termination records", len(tr), "by class", tr.trm_class.value_counts().to_dict())
    print("with person", int(tr.person_ok.sum()), "future-dated trm flags", int(rec.trm_future_date.sum()))
