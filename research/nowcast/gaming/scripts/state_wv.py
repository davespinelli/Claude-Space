"""West Virginia racetrack casinos + The Greenbrier: monthly revenue by property
-> data/state_wv.csv.gz

Sources (West Virginia Lottery; everything is WEEKLY, by fiscal year July-June):
  * business.wvlottery.com "Resources & Payments" page (https://business.wvlottery.com/resourcesPayments),
    Contentful-hosted zips, re-published every week:
      Video_Lottery_Summary.zip -> "<yy>FY RVL Video Lottery Summary.xlsx" (FY2021-FY2027)
      Table_Games.zip -> "<yy>FY Table Games Weekly Summary.xlsx", "<yy>FY Greenbrier Weekly Summary.xlsx"
                          (FY2021-FY2027)
  * Older fiscal years only survive in the Internet Archive copies of the former wvlottery.com site:
      https://web.archive.org/web/20220816065255id_/https://wvlottery.com/assets/pdf/secure-login/vidsum/VidSum.ZIP
          (RVL FY2019-FY2023)
      https://web.archive.org/web/20220816065301id_/https://wvlottery.com/assets/pdf/secure-login/reports/tablegames.zip
          (table games + Greenbrier FY2019-FY2023)
      https://web.archive.org/web/20130725124758id_/http://wvlottery.com/pdf/tablegames.zip
          (table games + Greenbrier FY2012-FY2013)
    No archived copy of the racetrack video-lottery summaries before FY2019 (July 2018) was found
    (Wayback CDX searched for vidsum/RVL/racetrack/video files on wvlottery.com, 2005-2026), and the
    Legislature's monthly Lottery reports only give statewide totals in $000s. Hence racetrack rows
    start 2018-07. The Greenbrier (which reports tables AND video in one file) also has FY2012-FY2013.
    Racetrack table-games data for FY2012-13 exist but are NOT emitted (VLT half missing).
Measures (both net of promotional credits / as taxed):
  slots  = racetrack video lottery "ADJ GROSS TERMINAL REVENUE" (amount played - won - promo) per track;
           Greenbrier: "Video Gross Terminal Revenue" (FY2012-13 files: "Adjusted Gross Terminal Income").
  tables = racetrack table games weekly "Total" (adjusted gross receipts across all games incl.
           poker); Greenbrier: "Table Games Gross Receipts" (FY2012-13: "Total Gross Receipts").
  ggr    = slots + tables; measure = "AGR" (adjusted gross receipts / adjusted gross terminal revenue).
  Excluded: limited video lottery (bars), sports wagering, iGaming.
Weekly -> monthly: each row is a week ending Saturday; weeks are cut at fiscal-year boundaries
  (rows marked "*" / "**" cover only the days inside the FY). Each row covers the days from the day
  after the previous row's end date (first row: July 1) through its end date; its amount is allocated
  to calendar months PRO-RATA BY DAYS. A month is emitted only when every day of it is covered
  (so the current partial month is dropped). This smooths revenue across month ends: a monthly
  figure here is an estimate, not a regulator-published month.
Units (unit_level = property; names = the regulator's sheet names):
  WV_MOUNTAINEER      "Mountaineer"  (Mountaineer Casino, Racetrack & Resort, New Cumberland)
  WV_WHEELING_ISLAND  "Wheeling"     (Wheeling Island Hotel-Casino-Racetrack)
  WV_MARDI_GRAS       "Mardi Gras"   (Mardi Gras Casino & Resort, Cross Lanes; ex Tri-State)
  WV_CHARLES_TOWN     "Charles Town" (Hollywood Casino at Charles Town Races)
  WV_GREENBRIER       "Greenbrier"   (The Casino Club at The Greenbrier, historic resort)
State total (unit_id WV_STATE_TOTAL): regulator totals allocated the same way = RVL "Total" sheet
  + table games "Summary"/"Weekly Summary" total + Greenbrier -- only for months with racetrack data.
  n_casinos = number of properties.
Publication dates: the files are cumulative fiscal-year workbooks re-posted every week, so a
  month's first publication date is not recoverable. pub_date is set only where the workbook's own
  metadata dates it: for June of each FY, the XLSX "modified" timestamp of that FY's final file when
  it is within 20 days of June 30 (the file is then the FY-closing post), and for the latest complete
  month of the current FY file (2026-08: file modified 2026-09-17, data through week ending
  2026-09-12). pub_source = pdf_metadata (document metadata of the XLSX). June months: published
  1-11 days after June 30. Weekly data are posted about 5-6 days after the week ends, so a month is
  fully public ~1-2 weeks after month end.
COVID: all WV casinos closed 2020-03-17 .. 2020-06-05; closed weeks are 0 in the files.
Spot checks (run 2026-09-23, data/state_wv_checks.csv.gz): sum of 5 properties vs regulator totals,
  all 98 months 2018-07..2026-08: max |diff| 0.0000%. Fiscal-year sums of the pro-rated monthly
  VLT figures reproduce the published FY totals exactly (e.g. Mountaineer FY2025 76,848,325.40,
  Wheeling FY2025 85,481,970.47). Units are dollars.
  Jump scan (m/m >3x or <1/3 outside Mar-Jul 2020): only The Greenbrier (tiny, ~$0.4-1.5m/month,
  volatile table hold: 2020-09 tables -$0.12m -> ggr x0.23; 2022-05 x3.1 after a weak April). Real.
Coverage: racetracks 2018-07 .. 2026-08 (98 months); Greenbrier 2012-01 .. 2013-06 and
  2018-07 .. 2026-08 (116 months). Rows: 606. Gap 2012-2018 for racetracks: source not archived.
"""
from __future__ import annotations

import datetime as dt
import io
import re
import sys
import time
import zipfile
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "cache" / "wv"
DATA = ROOT / "data"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
LISTING = "https://business.wvlottery.com/resourcesPayments"
WAYBACK = {
    "VidSum_20220816.zip": "https://web.archive.org/web/20220816065255id_/https://wvlottery.com/assets/pdf/secure-login/vidsum/VidSum.ZIP",
    "tablegames_20220816.zip": "https://web.archive.org/web/20220816065301id_/https://wvlottery.com/assets/pdf/secure-login/reports/tablegames.zip",
    "tablegames_20130725.zip": "https://web.archive.org/web/20130725124758id_/http://wvlottery.com/pdf/tablegames.zip",
}
TRACKS = {"Mountaineer": "WV_MOUNTAINEER", "Wheeling": "WV_WHEELING_ISLAND",
          "Mardi Gras": "WV_MARDI_GRAS", "Charles Town": "WV_CHARLES_TOWN"}
_last = [0.0]


def get(url):
    for attempt in range(4):
        w = 1.0 - (time.time() - _last[0])
        if w > 0:
            time.sleep(w)
        _last[0] = time.time()
        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=180)
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            print(f"  retry {attempt + 1} {url}: {e}", file=sys.stderr)
            time.sleep(2 ** attempt * 3)
    raise RuntimeError(url)


def download(refresh: bool) -> dict[str, Path]:
    CACHE.mkdir(parents=True, exist_ok=True)
    lst = CACHE / "_listing_resourcesPayments.html"
    if refresh or not lst.exists():
        lst.write_bytes(get(LISTING).content)
    html = lst.read_text(errors="ignore")
    zips = {}
    for name in ("Video_Lottery_Summary", "Table_Games"):
        m = re.search(r"https://assets\.ctfassets\.net/[^\"\\]*/([0-9a-f]{32})/" + name + r"\.zip", html)
        if not m:
            raise RuntimeError(f"{name}.zip not on listing page")
        # the content hash is in the URL -> a new weekly version gets a new cache file
        dest = CACHE / f"{name}_{m.group(1)[:8]}.zip"
        if not dest.exists():
            legacy = CACHE / f"{name}.zip"   # first download (2026-09-23) was saved without hash
            if legacy.exists():
                legacy.rename(dest)
            else:
                dest.write_bytes(get(m.group(0)).content)
        zips[name] = dest
    for fn, url in WAYBACK.items():
        dest = CACHE / "wayback" / fn
        if not dest.exists():
            dest.parent.mkdir(exist_ok=True)
            dest.write_bytes(get(url).content)
        zips[fn] = dest
    return zips


def members(zpath: Path, pattern: str) -> dict[int, tuple[str, bytes, dt.datetime]]:
    """{fiscal_year: (member name, bytes, zip mtime)} for members matching pattern."""
    out = {}
    with zipfile.ZipFile(zpath) as z:
        for info in z.infolist():
            m = re.match(r"(\d\d)FY " + pattern, info.filename)
            if m:
                out[2000 + int(m.group(1))] = (info.filename, z.read(info), dt.datetime(*info.date_time))
    return out


def parse_date(v) -> dt.date | None:
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, str):
        m = re.match(r"\s*(\d{1,2})/(\d{1,2})/(\d{4})", v)
        if m:
            return dt.date(int(m.group(3)), int(m.group(1)), int(m.group(2)))
    return None


def weekly_series(ws, col_pred) -> list[tuple[dt.date, float]]:
    """rows (week_end, value) from a sheet; value column = first header cell satisfying col_pred.
    Header is re-detected (sheets can repeat headers)."""
    col = None
    out = []
    for r in ws.iter_rows(values_only=True):
        for j, v in enumerate(r):
            if isinstance(v, str) and col_pred(re.sub(r"\s+", " ", v).strip()):
                col = j
                break
        if col is None:
            continue
        d = parse_date(r[0]) if r else None
        if d is None:
            continue
        v = r[col] if col < len(r) else None
        out.append((d, float(v) if isinstance(v, (int, float)) else 0.0))
    # a sheet may print the same table twice (print areas) -> dedupe by date keeping first
    seen, uniq = set(), []
    for d, v in out:
        if d not in seen:
            seen.add(d)
            uniq.append((d, v))
    return sorted(uniq)


def to_days(fy: int, rows: list[tuple[dt.date, float]]) -> pd.Series:
    """expand weekly rows of a fiscal year into a daily series (pro-rata)."""
    start = dt.date(fy - 1, 7, 1)
    fy_end = dt.date(fy, 6, 30)
    vals = {}
    prev_end = start - dt.timedelta(days=1)
    for end, v in rows:
        s = max(prev_end + dt.timedelta(days=1), start)
        e = min(end, fy_end)
        n = (e - s).days + 1
        if n <= 0:
            continue
        for k in range(n):
            vals[s + dt.timedelta(days=k)] = v / n
        prev_end = e
    return pd.Series(vals, dtype=float)


def monthly(daily: pd.Series) -> pd.Series:
    if daily.empty:
        return pd.Series(dtype=float)
    idx = pd.to_datetime(pd.Series(daily.index))
    s = pd.Series(daily.values, index=idx)
    g = s.groupby(s.index.to_period("M"))
    full = g.size() == g.apply(lambda x: x.index[0].days_in_month)
    m = g.sum()[full]
    m.index = m.index.astype(str)
    return m


def load_book(data: bytes):
    import openpyxl
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return openpyxl.load_workbook(io.BytesIO(data), data_only=True)


def main(refresh=False):
    zips = download(refresh)
    # fiscal-year -> member, current zips override wayback for overlapping FYs
    rvl = {**members(zips["VidSum_20220816.zip"], r"RVL Video Lottery Summary\.xlsx"),
           **members(zips["Video_Lottery_Summary"], r"RVL Video Lottery Summary\.xlsx")}
    tg = {**members(zips["tablegames_20130725.zip"], r"Table Games Weekly Summary(-Final)?\.xlsx"),
          **members(zips["tablegames_20220816.zip"], r"Table Games Weekly Summary\.xlsx"),
          **members(zips["Table_Games"], r"Table Games Weekly Summary\.xlsx")}
    gb = {**members(zips["tablegames_20130725.zip"], r"Greenbrier Weekly Summary(-Final)?\.xlsx"),
          **members(zips["tablegames_20220816.zip"], r"Greenbrier Weekly Summary\.xlsx"),
          **members(zips["Table_Games"], r"Greenbrier Weekly Summary\.xlsx")}
    src_zip = {}
    for fy in rvl:
        src_zip[("rvl", fy)] = "Video_Lottery_Summary" if fy >= 2021 else "VidSum_20220816.zip"
    for fy in tg:
        src_zip[("tg", fy)] = ("Table_Games" if fy >= 2021 else
                               "tablegames_20220816.zip" if fy >= 2019 else "tablegames_20130725.zip")

    daily = {}   # (unit_id, component) -> list of daily series
    fyinfo = []  # for pub dates
    is_rvl_total = lambda h: bool(re.match(r"ADJ GROSS TERMINAL REV", h, re.I))
    for fy, (fn, data, mtime) in sorted(rvl.items()):
        if fy < 2019:
            continue
        wb = load_book(data)
        for sheet, uid in list(TRACKS.items()) + [("Total", "WV_STATE_TOTAL")]:
            rows = weekly_series(wb[sheet], is_rvl_total)
            daily.setdefault((uid, "slots"), []).append(to_days(fy, rows))
        fyinfo.append(("rvl", fy, fn, wb.properties.modified, rows[-1][0] if rows else None))
    for fy, (fn, data, mtime) in sorted(tg.items()):
        if fy < 2019:
            continue  # FY2012-13 racetrack tables exist but VLT half is missing -> not emitted
        wb = load_book(data)
        tot_sheet = "Summary" if "Summary" in wb.sheetnames else "Weekly Summary"
        for sheet, uid in list(TRACKS.items()) + [(tot_sheet, "WV_STATE_TOTAL")]:
            rows = weekly_series(wb[sheet], lambda h: h == "Total")
            daily.setdefault((uid, "tables"), []).append(to_days(fy, rows))
        fyinfo.append(("tg", fy, fn, wb.properties.modified, rows[-1][0] if rows else None))
    for fy, (fn, data, mtime) in sorted(gb.items()):
        wb = load_book(data)
        ws = wb["Weekly Summary"]
        # FY2019+: "Table Games Gross Receipts" / "Video Gross Terminal Revenue";
        # FY2012-13: "Total Gross Receipts" / "Adjusted Gross Terminal Income"
        t = weekly_series(ws, lambda h: bool(re.fullmatch(r"(Table Games|Total) Gross Receipts", h, re.I)))
        v = weekly_series(ws, lambda h: bool(re.fullmatch(r"Video Gross Terminal Revenue|Adjusted Gross Terminal Income", h, re.I)))
        daily.setdefault(("WV_GREENBRIER", "tables"), []).append(to_days(fy, t))
        daily.setdefault(("WV_GREENBRIER", "slots"), []).append(to_days(fy, v))
        fyinfo.append(("gb", fy, fn, wb.properties.modified, t[-1][0] if t else None))

    mon = {}
    for key, parts in daily.items():
        s = pd.concat(parts)
        s = s[~s.index.duplicated(keep="last")].sort_index()
        mon[key] = monthly(s)
    names = {v: k for k, v in TRACKS.items()} | {"WV_GREENBRIER": "Greenbrier", "WV_STATE_TOTAL": "__STATE_TOTAL__"}
    rows = []
    for uid in list(TRACKS.values()) + ["WV_GREENBRIER", "WV_STATE_TOTAL"]:
        sl, tb = mon.get((uid, "slots")), mon.get((uid, "tables"))
        if sl is None or tb is None:
            continue
        months = sorted(set(sl.index) & set(tb.index))
        for m in months:
            if m < "2012-01":
                continue
            rows.append(dict(state="WV", unit=names[uid], unit_id=uid,
                             unit_level="state_total" if uid == "WV_STATE_TOTAL" else "property",
                             month=m, ggr=sl[m] + tb[m] + (0.0 if uid != "WV_STATE_TOTAL" else 0.0),
                             slots=sl[m], tables=tb[m], n_casinos=None, measure="AGR",
                             pub_date="", pub_source="", source_file=""))
    out = pd.DataFrame(rows)
    # state total must include the Greenbrier (regulator totals are racetrack-only)
    gbm = out[out.unit_id == "WV_GREENBRIER"].set_index("month")
    st = out.unit_id == "WV_STATE_TOTAL"
    out.loc[st, "slots"] = out.loc[st].apply(lambda r: r.slots + gbm.slots.get(r.month, 0.0), axis=1)
    out.loc[st, "tables"] = out.loc[st].apply(lambda r: r.tables + gbm.tables.get(r.month, 0.0), axis=1)
    out.loc[st, "ggr"] = out.loc[st, "slots"] + out.loc[st, "tables"]
    out.loc[st, "n_casinos"] = 5
    # source files
    def srcs(m):
        y, mo = map(int, m.split("-"))
        fy = y + 1 if mo >= 7 else y
        s = []
        if (("rvl", fy)) in src_zip:
            s.append(f"{src_zip[('rvl', fy)]}::{rvl[fy][0]}")
        if (("tg", fy)) in src_zip:
            s.append(f"{src_zip[('tg', fy)]}::{tg[fy][0]}")
        if fy in gb:
            s.append(f"{src_zip.get(('tg', fy), 'Table_Games')}::{gb[fy][0]}")
        return " + ".join(s)
    out["source_file"] = out.month.map(srcs)
    gb_only = out.unit_id == "WV_GREENBRIER"
    out.loc[gb_only, "source_file"] = out.loc[gb_only, "month"].map(
        lambda m: next(x for x in srcs(m).split(" + ") if "Greenbrier" in x))

    # pub dates: June of each FY from FY-final file metadata; latest complete month of current FY
    pubs = {}
    last_month = out.month.max()
    for kind, fy, fn, modified, last_week in fyinfo:
        if kind != "rvl" or modified is None:
            continue
        june = f"{fy}-06"
        if dt.date(fy, 6, 30) <= modified.date() <= dt.date(fy, 7, 20):
            pubs[june] = modified.date().isoformat()
        if last_week and last_week < dt.date(fy, 6, 30) and last_month <= f"{fy}-06":
            pubs[last_month] = modified.date().isoformat()
    out["pub_date"] = out.month.map(pubs).fillna("")
    out["pub_source"] = out.pub_date.map(lambda x: "pdf_metadata" if x else "")
    out = out.sort_values(["month", "unit_level", "unit_id"])
    assert not out.duplicated(["unit_id", "month"]).any()
    DATA.mkdir(exist_ok=True)
    out.to_csv(DATA / "state_wv.csv.gz", index=False)

    # checks: sum of units vs regulator totals (allocated identically) + weekly sum vs FY total rows
    u = out[out.unit_level == "property"].groupby("month").ggr.sum()
    t = out[out.unit_level == "state_total"].set_index("month").ggr
    chk = pd.DataFrame({"sum_of_units": u, "regulator_total": t}).dropna()
    chk["diff_pct"] = (chk.sum_of_units - chk.regulator_total) / chk.regulator_total.where(chk.regulator_total != 0) * 100
    chk["note"] = ("4 racetracks + Greenbrier vs RVL 'Total' sheet + table-games 'Summary' + Greenbrier "
                   "(weekly, pro-rated to months identically)")
    chk.index.name = "month"
    chk = chk.reset_index()
    chk.to_csv(DATA / "state_wv_checks.csv.gz", index=False)

    jumps = []
    for uid, g in out[out.unit_level == "property"].groupby("unit_id"):
        v = g.set_index("month").ggr
        rat = v / v.shift(1)
        for m, x in rat.items():
            if pd.notna(x) and (x > 3 or x < 1 / 3) and not ("2020-03" <= m <= "2020-07"):
                jumps.append((uid, m, round(x, 2)))
    neg = out[out.ggr < 0][["unit_id", "month", "ggr"]].values.tolist()
    print(f"rows={len(out)} months {out.month.min()}..{out.month.max()} "
          f"racetrack months {out[out.unit_id == 'WV_CHARLES_TOWN'].month.min()}..")
    print(f"check max|diff%|={chk.diff_pct.abs().max():.4f} n={len(chk)}")
    print("jumps:", jumps, "negative:", neg)
    print("pub dates:", pubs)
    return out


if __name__ == "__main__":
    main("--refresh" in sys.argv)
