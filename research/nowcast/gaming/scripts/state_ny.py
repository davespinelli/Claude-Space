"""New York monthly casino / video-gaming revenue by facility (2012-01 .. 2025-09).

Sources
-------
The NY State Gaming Commission (gaming.ny.gov, "Revenue Reports") posts cumulative Excel/PDF reports:
  * VGM (video lottery / video gaming machine) facilities: "Web Site Report - <facility>.xls"
    (monthly, one sheet per state fiscal year Apr-Mar, back to each facility's opening) and
    "Web Site Report - Statewide Totals.xls".
  * Commercial casinos (Upstate Gaming Economic Development Act): "<casino> Monthly Commercial Gaming
    Report.xlsx" (del Lago, Rivers Schenectady, Tioga Downs, Resorts World Catskills) and
    "Statewide Monthly Commercial Gaming Report.xlsx".
gaming.ny.gov sits behind a Cloudflare browser challenge that returns HTTP 403 to every scripted
request (pages and files alike). We do NOT try to get around it. Instead all files are taken from the
Internet Archive's Wayback Machine copies of those exact URLs:
    CDX index : http://web.archive.org/cdx/search/cdx?url=<prefix>&matchType=prefix
    file      : http://web.archive.org/web/<timestamp>id_/<original url>
  prefixes: gaming.ny.gov/system/files/documents/ (site since 2024), www.gaming.ny.gov/pdf/finance/
  and gaming.ny.gov/pdf/finance/ (old site). The newest capture of each report is used; because the
  files are cumulative, one capture carries the whole history. Cached in cache/ny/ as
  <report-key>__<wayback timestamp>.<ext>; CDX listings cached as cache/ny/cdx_*.txt.

Coverage limit: the Wayback Machine has usable captures of the facility files only up to
2025-10-11 (from Nov 2025 its crawler is also served 403 by Cloudflare). So the panel ends at
2025-09 for VGM facilities and 2025-08 for commercial casinos (Sep 2025 commercial files not
archived). Later months are NOT available per facility from any scripted source; fill them later
from a browser download if needed. Statewide-only PDFs were archived later (VGM statewide through
2026-04, commercial statewide through ~2025-11) but are not used beyond the unit panel.
Note for the study: per an archived RWNYC weekly report, Resorts World NYC "ceased operations as a
VLT facility on 4/27/2026" and began operating as a commercial casino (not covered here).

Measure
-------
* VGM facilities: "Net Win" (= net terminal income, credits played - credits won, after free play,
  before distribution) -> measure "NTI"; ggr = slots = Net Win; tables blank (VGM only).
* Commercial casinos: ggr = Slot & ETG GGR + Table Game GGR + Poker Table GGR; measure "GGR";
  `tables` includes poker. Sports wagering GGR (in the files' "Total GGR" since 2019) is excluded.
* Monthly figures are published directly, so no weekly -> monthly aggregation was needed.
* Months are rebuilt from the fiscal-year sheet name (FY yy-yy, Apr..Mar) plus the month number,
  because the statewide commercial file mislabels Jan-Mar with the wrong year.
* __STATE_TOTAL__ = regulator VGM statewide Net Win ("Statewide Totals" file) + regulator commercial
  statewide slot+table+poker GGR ("Statewide Monthly Commercial" file); measure "NTI+GGR". The
  archived statewide commercial .xlsx ends 2025-04; 2025-05..08 come from the newest archived
  statewide commercial PDF (Jan 2026 capture; slot + table + poker GGR columns; equals the .xlsx to
  within $1.10 where both exist). For 2025-09 the total includes commercial casinos but the unit rows
  do not (commercial facility files end 2025-08), so that month's check shows -22% by construction.

Units / unit_id (renames linked; `unit` = facility name printed on that fiscal-year sheet)
----------------------------------------------------------------------------------------
NY_BATAVIA_DOWNS        "Batavia Downs Casino" (FY11-12) -> "Batavia Downs Gaming"   (Western OTB)
NY_EMPIRE_CITY          "Empire City Casino at Yonkers Raceway"                      (MGM from Jan 2019)
NY_FINGER_LAKES         "Finger Lakes Casino and Racetrack" -> "Finger Lakes Gaming and Racetrack"
NY_HAMBURG              "Hamburg Casino at the Fairgrounds" -> "Hamburg Gaming"
NY_JAKES_58             "Jake's 58 Hotel & Casino" (Suffolk OTB, opened Feb 2017)
NY_MONTICELLO           "Monticello Casino & Raceway" (Empire Resorts; most VGMs moved to Resorts
                        World Catskills in Feb 2018, a small VGM floor ran until 2019-04)
NY_NASSAU_OTB_RWNYC     "Nassau OTB at Resorts World Casino New York City" (Nassau OTB's VGMs run by
                        Genting inside RWNYC, from 2016-10)
NY_RW_NYC               "Resorts World Casino New York City" (Genting, Aqueduct, opened Oct 2011)
NY_RW_HUDSON_VALLEY     "Resorts World Hudson Valley" (Newburgh, opened Dec 2022)
NY_SARATOGA             "Saratoga Casino & Raceway" -> "Saratoga Casino - Hotel" -> "Saratoga Casino
                        Hotel" (Churchill Downs from Feb 2022 via P2E)
NY_VERNON_DOWNS         "Vernon Downs Casino + Hotel"
NY_TIOGA_DOWNS          "Tioga Downs Casino": VGM (NTI) through 2016-11, commercial casino (GGR)
                        from 2016-12 - same unit_id, measure column changes.
NY_DEL_LAGO             "del Lago Resort and Casino" (opened Feb 2017)
NY_RIVERS_SCHENECTADY   "Rivers Casino and Resort" (opened Feb 2017)
NY_RW_CATSKILLS         "Resorts World Catskills" (Empire Resorts, opened 2018-02-08)

Publication date
----------------
Not printed in the reports. The Commission re-saves every file each time it is updated, so every
archived version of the statewide files (VGM "Statewide Totals" .xls/.pdf, and del Lago's monthly
commercial .xlsx/.pdf which is saved together with the other commercial files) was downloaded and its
internal document metadata read (Excel "last saved" property / PDF CreationDate). When a version whose
newest month is M was saved <= 25 days after the end of M, that save date is taken as the publication
date of month M for every facility of that type (pub_source = "pdf_metadata", i.e. file-internal
metadata). Months without such a version keep pub_date blank (about 80% of rows: the archive has
only ~60 versions since 2017). Typical lag observed: median ~7 days after month-end for VGM, ~9 days
for commercial (e.g. Sep 2025 VGM files saved 2025-10-07; Aug 2025 commercial saved 2025-09-04).

Quirks
------
* COVID-19: all VGM facilities and commercial casinos closed 2020-03-16 and reopened from
  2020-09-09; the reports show 0 for the closed months, kept as 0.
* Leading months before opening and trailing months after closure (zeros/blank in the sheets) are
  dropped; the future months of the current fiscal year are blank (or 0 in the statewide
  commercial file) and dropped.

Spot checks (run 2026-09-23): data/state_ny_checks.csv.gz, every month 2012-01..2025-08 (VGM units
vs VGM statewide; commercial units vs commercial statewide; combined vs __STATE_TOTAL__): max |diff|
= 0.000%. Month/month jumps > 3x are openings only: del Lago 2017-02 (opened 2017-02-01, Jan =
preview), Jake's 58 2017-03 (opened late Feb 2017), RW Hudson Valley 2023-01 (opened 2022-12-28).
COVID closures show 0 for 2020-04..2020-08 at every facility. Units are dollars.
"""
import os, re, io, sys, json, time, glob, zipfile, collections
from datetime import date, datetime, timedelta
import requests
import pandas as pd
import numpy as np

ROOT = '/Users/davidspinelli/Documents/Claude Space/research/nowcast/gaming'
CACHE = os.path.join(ROOT, 'cache', 'ny')
DATA = os.path.join(ROOT, 'data')
S = requests.Session()
S.headers['User-Agent'] = 'Mozilla/5.0 (research data collection; casino revenue study)'
PREFIXES = ['gaming.ny.gov/system/files/documents/', 'www.gaming.ny.gov/pdf/finance/', 'gaming.ny.gov/pdf/finance/']

VGM_KEYS = {
    'web-site-report-batavia-downs-casino': 'NY_BATAVIA_DOWNS',
    'web-site-report-empire-city-casino-at-yonkers-raceway': 'NY_EMPIRE_CITY',
    'web-site-report-finger-lakes-casino-racetrack': 'NY_FINGER_LAKES',
    'web-site-report-hamburg-casino-at-the-fairgrounds': 'NY_HAMBURG',
    'web-site-report-jakes-58-suffolk-otb': 'NY_JAKES_58',
    'web-site-report-monticello-casino-raceway': 'NY_MONTICELLO',
    'web-site-report-nassau-at-resorts-world': 'NY_NASSAU_OTB_RWNYC',
    'web-site-report-resorts-world-casino': 'NY_RW_NYC',
    'web-site-report-resorts-world-hudson-valley': 'NY_RW_HUDSON_VALLEY',
    'web-site-report-saratoga-casino-hotel': 'NY_SARATOGA',
    'web-site-report-tioga-downs-casino': 'NY_TIOGA_DOWNS',
    'web-site-report-vernon-downs-casino': 'NY_VERNON_DOWNS',
}
COM_KEYS = {
    'del-lago-monthly-commercial-gaming-report': 'NY_DEL_LAGO',
    'rivers-monthly-commercial-gaming-report': 'NY_RIVERS_SCHENECTADY',
    'tioga-monthly-commercial-gaming-report': 'NY_TIOGA_DOWNS',
    'resorts-world-catskills-casino-monthly-commercial-gaming-report': 'NY_RW_CATSKILLS',
}
VGM_STATE = 'web-site-report-statewide-totals'
COM_STATE = 'statewide-monthly-commercial-gaming-report'
# reports whose every archived version is downloaded for publication dating
DATING = {'vgm': ['web-site-report-statewide-totals'],
          'com': ['del-lago-monthly-commercial-gaming-report', 'del-lago-casino-monthly-website-report']}


def report_key(u):
    b = u.split('?')[0].split('/')[-1].lower().replace('%20', '-').replace(' ', '-')
    b = re.sub(r'(_\d+)?\.(xlsx?|pdf)$', r'.\2', b)
    b = b.replace('---', '-').replace('-&-', '-').replace('&', '')
    b = re.sub(r'\.xlsx?$', '.xls', b)
    return b


def wb_get(url, tries=5):
    for a in range(tries):
        try:
            time.sleep(1.0)
            r = S.get(url, timeout=180)
            if r.status_code == 200:
                return r
            print('HTTP', r.status_code, url[:150])
            if r.status_code in (403, 404):
                return None
        except Exception as e:
            print('err', e)
        time.sleep(10 * (a + 1))
    return None


def cdx_rows(refresh=False):
    rows = []
    for i, pre in enumerate(PREFIXES):
        p = os.path.join(CACHE, f'cdx_{i}.txt')
        if refresh or not os.path.exists(p):
            r = wb_get('http://web.archive.org/cdx/search/cdx?' + '&'.join([
                f'url={pre}', 'matchType=prefix', 'fl=original,timestamp,statuscode,mimetype,digest',
                'filter=statuscode:200', 'limit=300000']))
            open(p, 'w').write(r.text)
        rows += [l.split() for l in open(p).read().splitlines() if len(l.split()) == 5]
    return rows


def download(refresh=False):
    os.makedirs(CACHE, exist_ok=True)
    rows = cdx_rows(refresh)
    by = collections.defaultdict(list)
    for u, ts, st, mt, dg in rows:
        by[report_key(u)].append((ts, u, mt, dg))
    got = {}

    def fetch(key, ts, u, mt):
        ext = 'pdf' if u.lower().endswith('.pdf') else ('xlsx' if 'openxml' in mt or u.lower().endswith('.xlsx') else 'xls')
        fn = f'{key[:-4]}__{ts}.{ext}'
        p = os.path.join(CACHE, fn)
        if not os.path.exists(p):
            r = wb_get(f'http://web.archive.org/web/{ts}id_/{u}')
            if r is None:
                return None
            open(p, 'wb').write(r.content)
        return fn

    # newest excel capture of each report
    for k in list(VGM_KEYS) + list(COM_KEYS) + [VGM_STATE, COM_STATE]:
        caps = sorted(by.get(k + '.xls', []))
        for ts, u, mt, dg in reversed(caps):
            fn = fetch(k + '.xls', ts, u, mt)
            if fn:
                got[k] = fn
                break
    # newest PDF capture of the statewide commercial report (runs later than the archived .xlsx)
    caps = sorted(by.get(COM_STATE + '.pdf', []))
    for ts, u, mt, dg in reversed(caps):
        fn = fetch(COM_STATE + '.pdf', ts, u, mt)
        if fn:
            got[COM_STATE + '_pdf'] = fn
            break
    # every distinct version of the dating reports (xls + pdf)
    versions = {'vgm': [], 'com': []}
    for kind, keys in DATING.items():
        for k in keys:
            for ext in ('.xls', '.pdf'):
                seen = set()
                for ts, u, mt, dg in sorted(by.get(k + ext, [])):
                    if dg in seen:
                        continue
                    seen.add(dg)
                    fn = fetch(k + ext, ts, u, mt)
                    if fn:
                        versions[kind].append(fn)
    return got, versions


MONTHS3 = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']


def fy_start(sheet):
    m = re.search(r'(\d\d)\s*-\s*(\d\d)', sheet)
    return 2000 + int(m.group(1))


def month_num(v):
    if isinstance(v, (datetime, pd.Timestamp)):
        return v.month
    s = str(v).strip().lower()
    for i, m in enumerate(MONTHS3):
        if s.startswith(m):
            return i + 1
    return None


def header_map(sh, hrow, nup=4):
    cols = {}
    for c in range(sh.shape[1]):
        parts = [str(sh.iat[r, c]).strip() for r in range(max(0, hrow - nup), hrow + 1)
                 if pd.notna(sh.iat[r, c]) and str(sh.iat[r, c]).strip()]
        cols[c] = re.sub(r'\s+', ' ', ' '.join(parts))
    return cols


def parse_sheets(path, kind):
    """Yield dicts(month, name, values...) from every FY sheet of a cumulative report."""
    xl = pd.read_excel(os.path.join(CACHE, path), sheet_name=None, header=None)
    out = []
    for sname, sh in xl.items():
        if not re.search(r'\d\d\s*-\s*\d\d', sname):
            continue
        fy = fy_start(sname)
        name = re.sub(r'\s+', ' ', str(sh.iat[0, 0])).strip()
        hrow = next(r for r in range(sh.shape[0]) if str(sh.iat[r, 0]).strip() == 'Month')
        cols = header_map(sh, hrow)
        if kind == 'vgm':
            nw = [c for c, h in cols.items() if re.fullmatch(r'Net Win', h)]
            assert nw, (path, sname, cols)
            want = {'net_win': nw[0]}
        else:
            def find(pat):
                cs = [c for c, h in cols.items() if re.search(pat, h, re.I)]
                return cs[0] if cs else None
            want = {'slots': find(r'Slot.*GGR$'), 'tables': find(r'^Table Games?.*Table Game GGR$|Table Game GGR$'),
                    'poker': find(r'Poker.*GGR$'), 'sports': find(r'Sports.*GGR$'), 'total': find(r'^Total GGR$')}
            assert want['slots'] is not None and want['tables'] is not None, (path, sname, cols)
        for r in range(hrow + 1, min(hrow + 16, sh.shape[0])):
            mn = month_num(sh.iat[r, 0])
            if mn is None:
                if str(sh.iat[r, 0]).strip().lower().startswith('total'):
                    break
                continue
            y = fy if mn >= 4 else fy + 1
            rec = {'month': f'{y:04d}-{mn:02d}', 'name': name, 'sheet': sname}
            for k, c in want.items():
                v = sh.iat[r, c] if c is not None else np.nan
                try:
                    rec[k] = float(v) if pd.notna(v) and str(v).strip() != '' else np.nan
                except ValueError:
                    rec[k] = np.nan
            out.append(rec)
    return pd.DataFrame(out)


def trim(df, col):
    """drop months before first and after last non-zero value (keeps interior zeros e.g. COVID)."""
    df = df.sort_values('month')
    nz = df[col].fillna(0) != 0
    if not nz.any():
        return df.iloc[0:0]
    first, last = df.month[nz].min(), df.month[nz].max()
    d = df[(df.month >= first) & (df.month <= last)].copy()
    d[col] = d[col].fillna(0.0)
    return d


def file_saved(fn):
    p = os.path.join(CACHE, fn)
    try:
        if fn.endswith('.xls'):
            import olefile
            m = olefile.OleFileIO(p).get_metadata()
            return m.last_saved_time
        if fn.endswith('.xlsx'):
            c = zipfile.ZipFile(p).read('docProps/core.xml').decode()
            m = re.search(r'<dcterms:modified[^>]*>([^<]+)<', c)
            return datetime.fromisoformat(m.group(1).replace('Z', ''))
        if fn.endswith('.pdf'):
            import pymupdf
            d = pymupdf.open(p)
            s = d.metadata.get('creationDate') or d.metadata.get('modDate')
            m = re.search(r'D:(\d{8})', s or '')
            return datetime.strptime(m.group(1), '%Y%m%d') if m else None
    except Exception as e:
        print('meta err', fn, e)
    return None


def latest_month_in(fn, kind):
    p = os.path.join(CACHE, fn)
    try:
        if fn.endswith('.pdf'):
            import pymupdf
            t = ' '.join(pg.get_text() for pg in pymupdf.open(p))
            fym = re.search(r'Fiscal Year\s+(\d{4})\s*/\s*(\d{4})', t) or re.search(r'FY\s*(\d\d)\s*-\s*(\d\d)', t)
            if not fym:
                return None
            fy = int(fym.group(1)) if len(fym.group(1)) == 4 else 2000 + int(fym.group(1))
            # monthly rows look like "April 2025 <numbers>" or "Apr-25 ..." ; take the last month label followed by a number > 0
            last = None
            for m in re.finditer(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\b[^\n]{0,12}\n?\s*\$?\s*([\d,]{5,}\.?\d*)', t):
                mn = MONTHS3.index(m.group(1)[:3].lower()) + 1
                if float(m.group(2).replace(',', '')) > 0:
                    y = fy if mn >= 4 else fy + 1
                    ym = f'{y:04d}-{mn:02d}'
                    last = max(last, ym) if last else ym
            return last
        df = parse_sheets(fn, 'vgm' if kind == 'vgm' else 'com')
        col = 'net_win' if kind == 'vgm' else 'slots'
        df = df[df[col].fillna(0) != 0]
        return df.month.max() if len(df) else None
    except Exception as e:
        print('latest err', fn, e)
        return None


def pub_dates(versions):
    res = {}
    for kind, fns in versions.items():
        best = {}
        for fn in fns:
            saved = file_saved(fn)
            lm = latest_month_in(fn, kind)
            if saved is None or lm is None:
                continue
            me = (pd.Timestamp(lm + '-01') + pd.offsets.MonthEnd(0)).date()
            lag = (saved.date() - me).days
            if 0 <= lag <= 25:
                if lm not in best or saved.date() < best[lm]:
                    best[lm] = saved.date()
        res[kind] = best
    return res


def parse_state_com_pdf(fn):
    """Statewide Monthly Commercial Gaming Report PDF: month rows 'Apr-25 $credits $promo $won $slotGGR ETGs
    $win/unit tables $drop $promo $tableGGR pokertables $pokerGGR $handle $sportsGGR $totalGGR ...'."""
    import pymupdf
    out = {}
    for page in pymupdf.open(os.path.join(CACHE, fn)):
        tk = [x.strip() for x in page.get_text().split('\n') if x.strip()]
        for i, t in enumerate(tk):
            m = re.fullmatch(r'([A-Z][a-z]{2})-(\d\d)', t)
            if not m or m.group(1).lower() not in MONTHS3:
                continue
            vals = tk[i + 1:i + 16]
            if len(vals) < 15 or any(re.fullmatch(r'[A-Z][a-z]{2}-\d\d', v) for v in vals):
                continue
            def mon(v):
                v = v.replace('$', '').replace(',', '').strip()
                neg = v.startswith('(')
                v = float(v.strip('()')) if v not in ('', '-') else 0.0
                return -v if neg else v
            mo = f'20{m.group(2)}-{MONTHS3.index(m.group(1).lower()) + 1:02d}'
            if mo not in out:
                out[mo] = mon(vals[3]) + mon(vals[9]) + mon(vals[11])
    return pd.Series(out, dtype=float)


def main(refresh=False):
    got, versions = download(refresh)
    rows = []
    vgm_units = []
    for k, uid in VGM_KEYS.items():
        df = parse_sheets(got[k], 'vgm')
        df = trim(df, 'net_win')
        df['unit_id'] = uid
        df['src'] = got[k]
        vgm_units.append(df)
    vgm = pd.concat(vgm_units)
    # Tioga Downs: VGM months end when the commercial casino starts (2016-12)
    com_units = []
    for k, uid in COM_KEYS.items():
        df = parse_sheets(got[k], 'com')
        for c in ('slots', 'tables', 'poker'):
            df[c] = df[c].fillna(0.0) if c in df else 0.0
        df['ggr'] = df.slots + df.tables + df.poker
        df = trim(df, 'ggr')
        df['unit_id'] = uid
        df['src'] = got[k]
        com_units.append(df)
    com = pd.concat(com_units)
    tioga_start = com[com.unit_id == 'NY_TIOGA_DOWNS'].month.min()
    vgm = vgm[~((vgm.unit_id == 'NY_TIOGA_DOWNS') & (vgm.month >= tioga_start))]

    pdts = pub_dates(versions)
    for _, r in vgm.iterrows():
        pdv = pdts['vgm'].get(r.month)
        rows.append(dict(state='NY', unit=r['name'], unit_id=r.unit_id, unit_level='property', month=r.month,
                         ggr=r.net_win, slots=r.net_win, tables=np.nan, n_casinos=np.nan, measure='NTI',
                         pub_date=pdv.isoformat() if pdv else '', pub_source='pdf_metadata' if pdv else '',
                         source_file=r.src))
    for _, r in com.iterrows():
        pdv = pdts['com'].get(r.month)
        rows.append(dict(state='NY', unit=r['name'], unit_id=r.unit_id, unit_level='property', month=r.month,
                         ggr=round(r.ggr, 2), slots=r.slots, tables=round(r.tables + r.poker, 2), n_casinos=np.nan,
                         measure='GGR', pub_date=pdv.isoformat() if pdv else '',
                         pub_source='pdf_metadata' if pdv else '', source_file=r.src))
    # regulator statewide totals
    sv = parse_sheets(got[VGM_STATE], 'vgm')
    sv = sv[sv.net_win.notna()]
    sv = sv.groupby('month').net_win.sum()
    sc = parse_sheets(got[COM_STATE], 'com')
    for c in ('slots', 'tables', 'poker'):
        sc[c] = sc[c].fillna(0.0)
    sc['ggr'] = sc.slots + sc.tables + sc.poker
    sc = sc.groupby('month')[['ggr', 'slots', 'tables', 'poker']].sum()
    sc = sc[sc.index <= sc.index[sc.ggr != 0].max()]   # drop future (zero) months, keep COVID zeros
    if COM_STATE + '_pdf' in got:
        extra = parse_state_com_pdf(got[COM_STATE + '_pdf'])
        both = [m for m in extra.index if m in sc.index]
        if both:
            print('statewide commercial pdf vs xlsx, max abs diff $', max(abs(extra[m] - sc.ggr[m]) for m in both))
        for m in extra.index:
            if m not in sc.index and extra[m] != 0:
                sc.loc[m, 'ggr'] = extra[m]
        sc = sc.sort_index()
    df = pd.DataFrame(rows)
    df = df[(df.month >= '2012-01')]
    months = sorted(df.month.unique())
    checks = []
    last_com_state = sc.index[(sc.ggr != 0)].max()
    last_vgm_state = sv.index[sv != 0].max()
    tot_rows = []
    for m in months:
        d = df[df.month == m]
        vs = d[d.measure == 'NTI'].ggr.sum()
        cs = d[d.measure == 'GGR'].ggr.sum()
        v_reg = sv.get(m, np.nan) if m <= last_vgm_state else np.nan
        c_reg = sc.ggr.get(m, np.nan) if m <= last_com_state else np.nan
        if m < '2016-12':
            c_reg = 0.0  # no commercial casinos before Tioga Downs converted in Dec 2016
        tot = v_reg + c_reg if pd.notna(v_reg) and pd.notna(c_reg) else np.nan
        pdv = pdts['vgm'].get(m)
        tot_rows.append(dict(state='NY', unit='__STATE_TOTAL__', unit_id='NY__STATE_TOTAL__', unit_level='state_total',
                             month=m, ggr=tot, slots=np.nan, tables=np.nan,
                             n_casinos=len(d), measure='NTI+GGR', pub_date=pdv.isoformat() if pdv else '',
                             pub_source='pdf_metadata' if pdv else '',
                             source_file=f'{got[VGM_STATE]} + ' + (got[COM_STATE] if m <= '2025-04' else got.get(COM_STATE + '_pdf', ''))))
        note = []
        if pd.notna(v_reg) and v_reg:
            note.append(f'VGM units vs VGM statewide {(vs - v_reg) / v_reg * 100:+.4f}%')
        if pd.notna(c_reg) and c_reg:
            note.append(f'commercial units vs commercial statewide {(cs - c_reg) / c_reg * 100:+.4f}%')
        if pd.isna(tot):
            note.append('regulator statewide total not archived for this month')
        if cs == 0 and pd.notna(c_reg) and c_reg > 0:
            note.append('commercial casino facility files for this month not archived (only the statewide '
                        'commercial PDF): sum of units covers VGM facilities only')
        checks.append(dict(month=m, sum_of_units=round(vs + cs, 2), regulator_total=tot,
                           diff_pct=round((vs + cs - tot) / tot * 100, 4) if pd.notna(tot) and tot else (0.0 if tot == 0 else np.nan),
                           note='; '.join(note)))
    df = pd.concat([df, pd.DataFrame(tot_rows)], ignore_index=True)
    ck = pd.DataFrame(checks)
    assert not df.duplicated(['unit_id', 'month']).any()
    prop = df[df.unit_level == 'property'].sort_values(['unit_id', 'month']).copy()
    prop['prev'] = prop.groupby('unit_id').ggr.shift()
    prop['ratio'] = prop.ggr / prop.prev
    odd = prop[((prop.ratio > 3) | (prop.ratio < 1 / 3)) & ~prop.month.between('2020-03', '2020-10')]
    print('jumps >3x or <1/3 outside COVID:')
    print(odd[['unit_id', 'month', 'prev', 'ggr']].to_string())
    print('checks n', ck.diff_pct.notna().sum(), 'max |diff| %', ck.diff_pct.abs().max())
    print(ck[ck.diff_pct.abs() > 0.01].to_string())
    print('months', df.month.min(), df.month.max(), 'pub_date filled', (prop.pub_date != '').mean().round(3))
    df = df.sort_values(['month', 'unit_level', 'unit_id'])
    df.to_csv(os.path.join(DATA, 'state_ny.csv.gz'), index=False, compression='gzip')
    ck.to_csv(os.path.join(DATA, 'state_ny_checks.csv.gz'), index=False, compression='gzip')
    return df, ck, pdts


if __name__ == '__main__':
    main(refresh='--refresh' in sys.argv)
