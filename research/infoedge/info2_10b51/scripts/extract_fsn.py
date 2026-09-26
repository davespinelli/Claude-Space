"""Stream each notes zip in cache/fsn/ and keep only what INFO-2 needs:
  sub   : every 10-Q / 10-K (and amendments / transition reports) submission
  ecdtxt: every ecd-taxonomy text fact (Item 408 flags, names, titles, dates, text blocks)
  ecdnum: every ecd-taxonomy numeric fact (TrdArrSecuritiesAggAvailAmt ...)
  dei   : EntityCommonStockSharesOutstanding / EntityPublicFloat (num), TradingSymbol / SecurityExchangeName (txt)
  dim   : segments text for every dimension hash used by the rows above
Writes cache/extract/<zipname>.{sub,ecdtxt,ecdnum,dei,dim}.parquet (idempotent)."""
import csv
import io
import sys
import zipfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sec

FSN = sec.CACHE / "fsn"
OUT = sec.CACHE / "extract"
FORMS = {"10-Q", "10-K", "10-Q/A", "10-K/A", "10-KT", "10-QT", "10-KT/A", "10-QT/A"}
DEI_NUM = {"EntityCommonStockSharesOutstanding", "EntityPublicFloat"}
DEI_TXT = {"TradingSymbol", "SecurityExchangeName", "EntityFilerCategory", "DocumentType"}
csv.field_size_limit(10 ** 9)


def rows(z, name):
    with z.open(name) as f:
        r = csv.reader(io.TextIOWrapper(f, encoding="utf-8", errors="replace", newline=""),
                       delimiter="\t", quoting=csv.QUOTE_NONE)
        hdr = next(r)
        for row in r:
            yield hdr, row


def extract(zp: Path):
    stem = zp.stem
    done = OUT / f"{stem}.dim.parquet"
    if done.exists():
        return
    OUT.mkdir(parents=True, exist_ok=True)
    z = zipfile.ZipFile(zp)
    names = set(z.namelist())
    ext = "tsv" if "sub.tsv" in names else "txt"
    # sub
    sub, hdr = [], None
    for hdr, row in rows(z, f"sub.{ext}"):
        if len(row) == len(hdr) and row[hdr.index("form")] in FORMS:
            sub.append(row)
    sub = pd.DataFrame(sub, columns=hdr)
    keep = set(sub.adsh)
    # txt
    et, dt_, hdr_t = [], [], None
    for hdr_t, row in rows(z, f"txt.{ext}"):
        if len(row) != len(hdr_t) or row[0] not in keep:
            continue
        v, tag = row[2], row[1]
        if v.startswith("ecd/"):
            et.append(row)
        elif v.startswith("dei/") and tag in DEI_TXT:
            dt_.append(row)
    et = pd.DataFrame(et, columns=hdr_t)
    dt_ = pd.DataFrame(dt_, columns=hdr_t)
    # num
    en, dn, hdr_n = [], [], None
    for hdr_n, row in rows(z, f"num.{ext}"):
        if len(row) != len(hdr_n) or row[0] not in keep:
            continue
        v, tag = row[2], row[1]
        if v.startswith("ecd/"):
            en.append(row)
        elif v.startswith("dei/") and tag in DEI_NUM:
            dn.append(row)
    en = pd.DataFrame(en, columns=hdr_n)
    dn = pd.DataFrame(dn, columns=hdr_n)
    hashes = set(et.get("dimh", [])) | set(en.get("dimh", [])) | set(dn.get("dimh", [])) | set(dt_.get("dimh", []))
    dim = []
    for hdr_d, row in rows(z, f"dim.{ext}"):
        if row and row[0] in hashes:
            dim.append(row[:2])
    dim = pd.DataFrame(dim, columns=["dimh", "segments"])
    sub.to_parquet(OUT / f"{stem}.sub.parquet")
    et.to_parquet(OUT / f"{stem}.ecdtxt.parquet")
    en.to_parquet(OUT / f"{stem}.ecdnum.parquet")
    pd.concat([dn.assign(kind="num"), dt_.assign(kind="txt")], ignore_index=True).astype(str).to_parquet(
        OUT / f"{stem}.dei.parquet")
    dim.to_parquet(done)
    print(stem, "subs", len(sub), "ecdtxt", len(et), "ecdnum", len(en), "dei", len(dn) + len(dt_), flush=True)


if __name__ == "__main__":
    for zp in sorted(FSN.glob("*.zip")):
        extract(zp)
