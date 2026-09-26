"""Assemble the INFO-2 event files (PREREG D2, D3, D5).

  data/terminations.csv   every Rule 10b5-1 termination (tagged + text), one row per filing x person,
                          with class (early / replacement / expired) and the primary flag
  data/adoptions.csv      tagged Rule 10b5-1 sell-plan adoptions with planned shares / shares outstanding
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sec
from build_events import norm_name

DATA = sec.ROOT / "data"
PRIORITY = {"replacement": 0, "early": 1, "expired": 2}


def shares_outstanding():
    """Cover-page shares outstanding per filing: the undimensioned value if present, else the sum over share
    classes, at the latest date reported on the cover."""
    d = pd.read_parquet(sec.CACHE / "dei_all.parquet")
    d = d[(d.kind == "num") & (d.tag == "EntityCommonStockSharesOutstanding")].copy()
    d["value"] = pd.to_numeric(d.value, errors="coerce")
    d = d[d.value > 0]
    d["ddate"] = d.ddate.astype(str)
    last = d.groupby("adsh").ddate.transform("max")
    d = d[d.ddate == last]
    nodim = d[d.segments == ""].groupby("adsh").value.max()
    dim = d[d.segments != ""].groupby("adsh").value.sum()
    return nodim.combine_first(dim).rename("shares_out")


def tagged_terminations(a):
    t = a[(a.is_trm == True) & a.person_ok].copy()
    t["source"] = "xbrl"
    t["pri"] = t.trm_class.map(PRIORITY)
    t = t.sort_values(["adsh", "person", "pri"])
    g = t.groupby(["adsh", "person"])
    out = g.first().reset_index()
    # a person counts as CEO / CFO / director if any of their contexts says so
    for c in ("is_ceo", "is_cfo", "is_dir", "purchase_only"):
        out[c] = g[c].max().values if c != "purchase_only" else g[c].min().values
    out["last"] = out.name_norm.map(lambda s: s.split()[-1] if isinstance(s, str) and s.split() else "")
    keep = ["adsh", "cik", "company", "form", "period", "filed", "fm", "person", "name", "last", "title_eff",
            "is_ceo", "is_cfo", "is_dir", "term_date", "exp_date", "trm_class", "trm_reason", "trm_stale",
            "purchase_only", "source", "sic"]
    return out[keep].rename(columns={"title_eff": "title"})


def text_terminations():
    e = pd.read_csv(DATA / "text_events_raw.csv.gz", low_memory=False)
    e = e[e.group.isin(["untagged", "not_in_fsn"])].copy()
    fts = pd.read_csv(sec.CACHE / "fts_10b51_docs.csv.gz", usecols=["adsh", "period_ending", "sics", "names", "form"])
    fts = fts.drop_duplicates("adsh").rename(columns={"form": "fts_form"})
    f = pd.read_csv(DATA / "filings.csv.gz", usecols=["adsh", "period", "name", "form", "sic"], low_memory=False)
    f = f.rename(columns={"name": "company"})
    e = e.merge(fts, on="adsh", how="left").merge(f, on="adsh", how="left")
    e["company"] = e.company.fillna(e.names.astype(str).str.split("  \\(").str[0])
    e["form"] = e.form.fillna(e.fts_form)
    e["cik"] = e.ciks.astype(str).str.split(";").str[0].astype(int)
    e["filed"] = pd.to_datetime(e.file_date)
    e["period"] = pd.to_datetime(e.period.astype("string"), format="%Y-%m-%d", errors="coerce").fillna(
        pd.to_datetime(e.period_ending, errors="coerce"))
    e["term_date"] = pd.to_datetime(e.term_date, errors="coerce")
    e["trm_stale"] = e.term_date.notna() & e.period.notna() & (e.term_date < e.period - pd.Timedelta(days=100))
    e["person"] = e["last"]
    e["fm"] = e.filed.dt.to_period("M").astype(str)
    e["source"] = "text"
    e["sic"] = e.sic.fillna(pd.to_numeric(e.sics.astype(str).str.split(";").str[0], errors="coerce"))
    e["exp_date"] = pd.NaT
    return e


def build():
    a = pd.read_csv(DATA / "arrangements.csv.gz", low_memory=False,
                    parse_dates=["filed", "period", "term_date", "exp_date", "adopt_date"])
    tt = tagged_terminations(a)
    te = text_terminations()
    te = te[[c for c in tt.columns if c in te.columns] + []].copy()
    for c in tt.columns:
        if c not in te.columns:
            te[c] = np.nan
    allt = pd.concat([tt, te[tt.columns]], ignore_index=True)
    allt = allt[~allt.form.isin(["10-Q/A", "10-K/A"])]
    # the same company-person-termination disclosed again later: keep the first filing
    allt = allt.sort_values("filed")
    allt["tdk"] = allt.term_date.dt.strftime("%Y-%m-%d").fillna("nodate-" + allt.adsh)
    allt["dup"] = allt.duplicated(["cik", "last", "tdk"])
    allt["insider_target"] = allt[["is_ceo", "is_cfo", "is_dir"]].fillna(False).astype(bool).any(axis=1)
    allt["purchase_only"] = allt.purchase_only.fillna(False).astype(bool)
    allt["trm_stale"] = allt.trm_stale.fillna(False).astype(bool)
    allt["primary"] = ((allt.trm_class == "early") & allt.insider_target & ~allt.purchase_only & ~allt.trm_stale
                       & ~allt.dup)
    allt["early_or_repl"] = (allt.trm_class.isin(["early", "replacement"]) & allt.insider_target & ~allt.purchase_only
                             & ~allt.trm_stale & ~allt.dup)
    allt.drop(columns=["tdk"]).to_csv(DATA / "terminations.csv", index=False)

    # ---------------- adoptions (tagged only)
    ad = a[(a.is_adopt == True) & a.person_ok & ~a.purchase_only.fillna(False)].copy()
    ad = ad[~ad.form.isin(["10-Q/A", "10-K/A"])]
    g = ad.groupby(["adsh", "person"])
    ado = g.agg(cik=("cik", "first"), company=("company", "first"), filed=("filed", "first"), fm=("fm", "first"),
                name=("name", "first"), title=("title_eff", "first"), adopt_date=("adopt_date", "min"),
                agg_shares=("agg_shares", "sum"), n_shares_tagged=("agg_shares", "count"),
                is_ceo=("is_ceo", "max"), is_cfo=("is_cfo", "max"), is_dir=("is_dir", "max"),
                sic=("sic", "first")).reset_index()
    ado["agg_shares"] = ado.agg_shares.where(ado.n_shares_tagged > 0)
    so = shares_outstanding()
    ado = ado.merge(so, left_on="adsh", right_index=True, how="left")
    ado["pct_out"] = ado.agg_shares / ado.shares_out
    ado["ratio_error"] = ado.pct_out > 0.5
    ado.to_csv(DATA / "adoptions.csv.gz", index=False)
    return allt, ado


if __name__ == "__main__":
    t, ad = build()
    print("terminations", len(t), t.groupby(["source", "trm_class"]).size().to_dict())
    print("primary", int(t.primary.sum()), "by source", t[t.primary].source.value_counts().to_dict(),
          "dups", int(t.dup.sum()), "stale", int(t.trm_stale.sum()))
    print("adoptions", len(ad), "with ratio", int(ad.pct_out.notna().sum()), "ratio errors", int(ad.ratio_error.sum()))
