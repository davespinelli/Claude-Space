"""Fetch the primary 10-Q/10-K document for (a) every filing that mentions "10b5-1" but carries no ecd
XBRL tags (or is missing from the notes data sets), and (b) a validation sample of tagged filings whose
answer is known from XBRL. Cached under cache/docs/. Writes cache/doc_list.csv."""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sec


def url(r):
    cik = int(str(r.ciks).split(";")[0])
    return f"https://www.sec.gov/Archives/edgar/data/{cik}/{r.adsh.replace('-', '')}/{r.file}"


def build_list(seed=7):
    d = pd.read_csv(sec.CACHE / "fts_10b51_docs.csv.gz")
    d = d[d.file_type.isin(["10-Q", "10-K", "10-KT", "10-QT"])]
    f = pd.read_csv(sec.ROOT / "data" / "filings.csv.gz", usecols=["adsh", "ecd_tagged"], low_memory=False)
    d = d.merge(f, on="adsh", how="left")
    d["group"] = None
    d.loc[d.ecd_tagged == False, "group"] = "untagged"
    d.loc[d.ecd_tagged.isna(), "group"] = "not_in_fsn"
    # validation: tagged filings with a known answer
    a = pd.read_csv(sec.ROOT / "data" / "arrangements.csv.gz", low_memory=False)
    pos = a[(a.is_trm == True) & a.person_ok].adsh.unique()
    tagged = d[d.ecd_tagged == True]
    vpos = tagged[tagged.adsh.isin(pos)].drop_duplicates("adsh").sample(200, random_state=seed)
    vneg = tagged[~tagged.adsh.isin(pos)].drop_duplicates("adsh").sample(200, random_state=seed)
    d.loc[d.index.isin(vpos.index), "group"] = "valid_pos"
    d.loc[d.index.isin(vneg.index), "group"] = "valid_neg"
    d = d[d.group.notna()].copy()
    d["url"] = d.apply(url, axis=1)
    d.to_csv(sec.CACHE / "doc_list.csv", index=False)
    return d


if __name__ == "__main__":
    d = build_list()
    print(d.group.value_counts().to_dict(), flush=True)
    order = pd.concat([d[d.group.str.startswith("valid")], d[~d.group.str.startswith("valid")]])
    from concurrent.futures import ThreadPoolExecutor
    urls = list(order.url)
    with ThreadPoolExecutor(6) as ex:  # the shared file-lock limiter still spaces request starts >= 0.55 s
        for i, _ in enumerate(ex.map(lambda u: sec.get(u, "docs", ".htm", ok404=True), urls)):
            if i % 100 == 0:
                print(i, len(urls), sec.STATS, flush=True)
    print("done", sec.STATS)
