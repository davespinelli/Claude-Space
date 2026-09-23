"""Maine monthly casino revenue by casino (2012-01 .. latest), Maine Gambling Control Unit (GCU).

Sources
-------
* 2018 .. current year: GCU "Casino Revenue Distribution" page
    https://www.maine.gov/dps/gcu/casino-gaming/casino-revenue-distribution
  links one PDF per casino per calendar year ("<year> Monthly Revenue"), e.g.
    https://www.maine.gov/dps/sites/maine.gov.dps/files/inline-files/WE%2012-31-25%20Hollywood%20Hollywood_2.pdf
    https://www.maine.gov/dps/sites/maine.gov.dps/files/inline-files/Website%20_WE%2012.31.2025%20Oxford_1.pdf
  Each PDF has a slot block (Funds In/Out, "Net Slot Revenue" by month plus weekly columns of the
  latest month, YTD) and a table block ("Net Revenue"; 2018: "Win"). Parsed with word coordinates:
  every number is assigned to the nearest column header, only month columns are kept.
* 2012 .. 2017: the old Gambling Control Board site (maine.gov/dps/GambBoard/Financials/...), no longer
  online, taken from the Internet Archive (http://web.archive.org/web/<ts>id_/<url>):
    2012  Revised Website figures/2012 Monthly Hollywood and Oxford Website totals.xlsx
    2013  Financials/2013/2013 Hollywood and Oxford Year End.xlsx
    2014  Financials/2014/2014 Year End.xlsx
    2015  Financials/2015/2015 Year-End.xlsx
    2016  financials/2016/2016 Year End.xlsx
    2017  documents/October2017Monthly{Hollywood,Oxford}Website...xlsx (Jan-Oct 2017)
  Columns used: slots "Net Revenue", tables "Win".
* Publication dating: the GCU re-posts each casino's PDF weekly under names like
  "WE 08-31-25 Hollywood Hollywood.pdf"; older versions are still served by maine.gov at their
  original inline-files URLs (names taken from the Wayback CDX index of
  maine.gov/dps/sites/maine.gov.dps/files/inline-files/, then downloaded from maine.gov itself).
All files cached in cache/me/.

Measure
-------
ggr = Net Slot Revenue (funds in - funds out, i.e. slot win; "Net Revenue" in the old files) + table
games net revenue/win (incl. poker). measure "GGR". Dollars. Sports wagering, iGaming, ADW,
fantasy and charitable gaming are separate reports and excluded.

Units
-----
ME_HOLLYWOOD_BANGOR  "Hollywood Casino" (Hollywood Casino Hotel & Raceway Bangor, Penn/PENN)
ME_OXFORD            "Oxford Casino" (opened 2012-06-05; Churchill Downs from 2019-07)

State total
-----------
The GCU publishes no combined monthly statewide figure, so __STATE_TOTAL__ rows have ggr blank. The
checks file instead compares, for every casino-year, the sum of the parsed months with the
regulator's own YTD / "YTD TOTAL" column (month field = last month of that year; note says so).

Publication date
----------------
PDF CreationDate (pub_source = pdf_metadata) of the earliest weekly version (still served by
maine.gov, ~260 versions) whose "as of" date (end date of the last weekly column with slot activity)
is the last day of month M and which was created within 45 days after M; each casino's own version
preferred, else the other casino's. Found for 2018-01..2025-12 for almost all months (~51% of all
rows); 2012-2017 and 2026 blank. Typical lag: median 6 days after month end (range 1-39).

Gaps / quirks
-------------
* 2017-11 and 2017-12 are missing for both casinos: the Nov/Dec 2017 and 2017 year-end files were
  never archived and the 2017 annual report (scanned) has annual totals only.
* The current-year PDFs carry a partial month (e.g. "as of Sept. 1, 2026"); a trailing month that is
  not complete at the as-of date is dropped (the checks add it back to match the YTD column).
* 2019 PDFs are rotated pages; 2018 table row is labelled "Win"; header dashes vary (U+2010).
* COVID-19: both casinos closed mid-March 2020 and reopened in July 2020; April-June 2020 are 0.
* Oxford: first month 2012-06 (opened 2012-06-05), slots and tables.
* The 2012 file used is the "Revised Website figures" version; it equals the original 2012 year-end
  file in every month.

Spot checks (run 2026-09-23; data/state_me_checks.csv.gz)
--------------------------------------------------------
No statewide monthly total is published. For every year 2012-2026 the sum of the parsed months
(both casinos, slots + tables) equals the regulator's own YTD / "YTD TOTAL" columns: max |diff| =
0.000% (largest absolute gap $0.01). No month/month jumps > 3x outside COVID. Dollars.
"""
import os, re, sys, time, json, urllib.parse, calendar
from datetime import datetime, date
import requests
import pandas as pd
import numpy as np
import pymupdf

ROOT = '/Users/davidspinelli/Documents/Claude Space/research/nowcast/gaming'
CACHE = os.path.join(ROOT, 'cache', 'me')
DATA = os.path.join(ROOT, 'data')
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) Chrome/124.0 Safari/537.36'}
S = requests.Session(); S.headers.update(UA)
PAGE = 'https://www.maine.gov/dps/gcu/casino-gaming/casino-revenue-distribution'
INLINE = 'https://www.maine.gov/dps/sites/maine.gov.dps/files/inline-files/'
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september',
          'october', 'november', 'december']
WB_OLD = [
    ('20160406154345', 'http://www.maine.gov/dps/GambBoard/Financials/Revised%20Website%20figures/2012%20Monthly%20Hollywood%20and%20Oxford%20Website%20totals.xlsx', 2012),
    ('20160406154343', 'http://www.maine.gov/dps/GambBoard/Financials/2013/2013%20Hollywood%20and%20Oxford%20Year%20End.xlsx', 2013),
    ('20170224213916', 'http://www.maine.gov/dps/GambBoard/Financials/2014/2014%20Year%20End.xlsx', 2014),
    ('20170208113415', 'http://www.maine.gov/dps/GambBoard/Financials/2015/2015%20Year-End.xlsx', 2015),
    ('20171124060437', 'http://www.maine.gov:80/dps/GambBoard/financials/2016/2016%20Year%20End.xlsx', 2016),
    ('20171124054147', 'http://www.maine.gov:80/dps/GambBoard/documents/October2017MonthlyHollywoodWebsitewithdistribution.xlsx', 2017),
    ('20171124060517', 'http://www.maine.gov:80/dps/GambBoard/documents/October2017MonthlyOxfordWebsitewithdistributiontotalsinclgross.xlsx', 2017),
]
UNITS = {'ME_HOLLYWOOD_BANGOR': 'Hollywood Casino', 'ME_OXFORD': 'Oxford Casino'}


def get(url, tries=5, ok404=True):
    for a in range(tries):
        try:
            time.sleep(1.0)
            r = S.get(url, timeout=120)
            if r.status_code == 200:
                return r
            print('HTTP', r.status_code, url[:140])
            if r.status_code in (403, 404) and ok404:
                return None
        except Exception as e:
            print('err', type(e).__name__, url[:100])
        time.sleep(15 * (a + 1))
    return None


def local_name(url):
    return urllib.parse.unquote(url.split('/')[-1]).replace(' ', '_')


def download():
    os.makedirs(CACHE, exist_ok=True)
    r = get(PAGE)
    open(os.path.join(CACHE, 'casino-revenue-distribution.html'), 'w').write(r.text)
    current = []
    for href, txt in re.findall(r'href="([^"]+\.pdf)"[^>]*>(.*?)</a>', r.text, re.S):
        txt = re.sub(r'<[^>]+>', '', txt)
        m = re.search(r'(20\d\d) Monthly Revenue', txt)
        if not m:
            continue
        yr = int(m.group(1))
        casino = 'ME_OXFORD' if 'oxford' in href.lower() else 'ME_HOLLYWOOD_BANGOR'
        fn = local_name(href)
        p = os.path.join(CACHE, fn)
        if not os.path.exists(p):
            rr = get('https://www.maine.gov' + href)
            if rr is None:
                continue
            open(p, 'wb').write(rr.content)
        current.append((yr, casino, fn))
    old = []
    for ts, u, yr in WB_OLD:
        fn = f'wb_{ts}_{local_name(u)}'
        p = os.path.join(CACHE, fn)
        if not os.path.exists(p):
            rr = get(f'http://web.archive.org/web/{ts}id_/{u}', ok404=False)
            if rr is None:
                print('MISSING old file', u)
                continue
            open(p, 'wb').write(rr.content)
        old.append((yr, fn))
    # weekly/monthly versions for publication dating (names from the Wayback CDX index, files from maine.gov)
    cdxp = os.path.join(CACHE, 'cdx_inline_files.txt')
    if not os.path.exists(cdxp):
        rr = get('http://web.archive.org/cdx/search/cdx?url=www.maine.gov/dps/sites/maine.gov.dps/files/inline-files/'
                 '&matchType=prefix&fl=original&filter=statuscode:200&collapse=urlkey&limit=100000', ok404=False)
        open(cdxp, 'w').write(rr.text if rr is not None else '')
    versions = []
    for u in sorted(set(open(cdxp).read().split())):
        b = u.split('/')[-1]
        if not b.lower().endswith('.pdf') or not re.search(r'(hollywood|oxford)', b, re.I):
            continue
        if re.search(r'(sportsbook|work%20order|daily|chapter|rules|flush|exclusion|slot%20machine|mgcb|adw|fantasy|charit)', b, re.I):
            continue
        fn = 'v_' + local_name(u)
        p = os.path.join(CACHE, fn)
        if not os.path.exists(p):
            if os.path.exists(p + '.missing'):
                continue
            rr = get(INLINE + b)
            if rr is None or not rr.content.startswith(b'%PDF'):
                open(p + '.missing', 'w').write('')
                continue
            open(p, 'wb').write(rr.content)
        versions.append(fn)
    return current, old, versions


def num(s):
    s = s.replace('$', '').replace(',', '').strip()
    if s in ('-', ''):
        return 0.0
    neg = s.startswith('(') and s.endswith(')')
    s = s.strip('()')
    try:
        v = float(s)
    except ValueError:
        return None
    return -v if neg else v


MON_HDR = re.compile(r'^(january|february|march|april|may|june|july|august|september|october|november|december|'
                     r'jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec)(?:[-\u2010\u2011\u2013](\d{4}|\d\d))?$', re.I)


def parse_pdf(fn, year=None):
    """Return dict: {'slots': {month: v}, 'tables': {month: v}, 'ytd': {'slots': v, 'tables': v}, 'asof': date}"""
    page = pymupdf.open(os.path.join(CACHE, fn))[0]
    W = page.get_text('words')
    if page.rotation:   # e.g. the 2019 files: map word boxes to the displayed (rotated) page
        rm = page.rotation_matrix
        W = [tuple(pymupdf.Rect(w[:4]) * rm) + tuple(w[4:]) for w in W]
    txt = page.get_text()
    if year is None:
        m = re.search(r'\b(?:Jan|Feb|Mar)-(20\d\d)\b', txt) or re.search(r'(20\d\d)', txt)
        year = int(m.group(1))
    # column headers: month names / Mon-YYYY, weekly date ranges (first date word), YTD
    hdrs = []
    for w in W:
        t = w[4].strip().replace('\u2010', '-').replace('\u2011', '-').replace('\xa0', ' ')
        m = MON_HDR.match(t)
        if m:
            mn = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'].index(m.group(1).lower()[:3]) + 1
            y = (int(m.group(2)) + (2000 if len(m.group(2)) == 2 else 0)) if m.group(2) else year
            hdrs.append(dict(kind='month', m=f'{y:04d}-{mn:02d}', x=(w[0] + w[2]) / 2, y=(w[1] + w[3]) / 2))
        elif re.fullmatch(r'\d\d?/\d\d?/\d{4}', t):
            hdrs.append(dict(kind='week', m=t, x=(w[0] + w[2]) / 2, y=(w[1] + w[3]) / 2))
        elif t.upper().startswith(('Y-T-D', 'YTD')):
            hdrs.append(dict(kind='ytd', m='ytd', x=(w[0] + w[2]) / 2, y=(w[1] + w[3]) / 2))
    # the two header bands (slot block, table block): cluster header y's
    ys = sorted(set(round(h['y']) for h in hdrs if h['kind'] == 'month'))
    bands = []
    for y in ys:
        if not bands or y - bands[-1][-1] > 20:
            bands.append([y])
        else:
            bands[-1].append(y)
    bands = [(min(b) - 12, max(b) + 12) for b in bands]
    # weekly headers have two date lines ("12/01/2025 to" / "12/02/2025"): keep one per column (by x)

    def band_headers(bi):
        lo, hi = bands[bi]
        hs = [h for h in hdrs if lo <= h['y'] <= hi]
        if bi > 0:   # a month/YTD header missing in a lower block: borrow the column from the top block
            have = {h['m'] for h in hs}
            lo0, hi0 = bands[0]
            hs += [h for h in hdrs if lo0 <= h['y'] <= hi0 and h['kind'] in ('month', 'ytd') and h['m'] not in have]
        out = []
        for h in sorted(hs, key=lambda h: h['x']):
            if out and abs(out[-1]['x'] - h['x']) < 8:
                if h['kind'] == 'week' and out[-1]['kind'] == 'week':   # keep the END date of a week column
                    d0 = datetime.strptime(out[-1]['m'], '%m/%d/%Y')
                    d1 = datetime.strptime(h['m'], '%m/%d/%Y')
                    out[-1] = dict(out[-1], m=max(d0, d1).strftime('%m/%d/%Y'))
                continue
            out.append(h)
        return out

    lines = {}
    for w in W:
        key = (w[5], w[6])
        lines.setdefault(key, []).append(w)
    rows = []
    for key, ws in lines.items():
        ws = sorted(ws, key=lambda w: w[0])
        label = ' '.join(w[4] for w in ws if not re.search(r'\d', w[4]) and w[4] not in ('$', '-', '(', ')'))
        rows.append((label, ws))

    def row_values(label_pat, bi):
        lo = bands[bi][1]
        hi = bands[bi + 1][0] if bi + 1 < len(bands) else 1e9
        hs = band_headers(bi)
        xs = [h['x'] for h in hs]
        cw = float(np.median(np.diff(xs))) if len(xs) > 1 else 50.0
        left = xs[0] - 0.55 * cw          # label area is left of the first column
        labels = {}
        for w in W:
            if lo < w[1] < hi and w[2] <= left:
                labels.setdefault(round((w[1] + w[3]) / 2), []).append(w)
        target = None
        for yc, ws in sorted(labels.items()):
            s = ' '.join(x[4] for x in sorted(ws, key=lambda x: x[0]))
            if re.match(label_pat, s, re.I):
                target = yc
                break
        if target is None:
            return None, None, {}
        vals = {}
        for w in W:
            yc = (w[1] + w[3]) / 2
            if abs(yc - target) > 0.45 * (w[3] - w[1]) + 1.5 or w[2] <= left:
                continue
            if not re.search(r'\d', w[4]) and w[4] != '-':
                continue
            v = num(w[4])
            if v is None:
                continue
            xc = (w[0] + w[2]) / 2
            h = min(hs, key=lambda h: abs(h['x'] - xc))
            if abs(h['x'] - xc) > 0.6 * cw:
                continue
            if h['m'] in vals and w[4] == '-':
                continue
            vals[h['m']] = v
        months = {k: v for k, v in vals.items() if re.fullmatch(r'\d{4}-\d\d', k)}
        weeks = {k: v for k, v in vals.items() if '/' in k}
        return months, vals.get('ytd'), weeks

    out = {'year': year}
    s, sy, sw = row_values(r'^Net Slot (Revenue|Win)', 0)
    out['slots'], out['ytd_slots'] = s or {}, sy
    if len(bands) > 1:
        t, ty, _ = row_values(r'^(Net Revenue|Win|Net Table)', 1)
        out['tables'], out['ytd_tables'] = t or {}, ty
    else:
        out['tables'], out['ytd_tables'] = {}, None
    # "as of" = end date of the last weekly column with slot activity
    wk = [datetime.strptime(k, '%m/%d/%Y').date() for k, v in sw.items() if v]
    out['asof'] = max(wk) if wk else None
    # drop a trailing month that is not complete at the as-of date
    if out['asof'] is not None:
        a = out['asof']
        if a.day != calendar.monthrange(a.year, a.month)[1]:
            part = f'{a.year:04d}-{a.month:02d}'
            out['partial_slots'] = out['slots'].pop(part, 0.0)
            out['partial_tables'] = out['tables'].pop(part, 0.0)
            out['partial'] = part
    return out


def parse_old_xlsx(fn, year):
    x = pd.read_excel(os.path.join(CACHE, fn), sheet_name=None, header=None)
    res = {}
    for sname, sh in x.items():
        n = sname.lower()
        if 'oxford' in n:
            casino = 'ME_OXFORD'
        elif 'hollywood' in n:
            casino = 'ME_HOLLYWOOD_BANGOR'
        else:
            casino = 'ME_OXFORD' if 'oxford' in fn.lower() else 'ME_HOLLYWOOD_BANGOR'
        kind = 'tables' if 'table' in n else ('slots' if 'slot' in n else None)
        hrow = next((r for r in range(sh.shape[0]) if str(sh.iat[r, 0]).strip() == 'Month'), None)
        if hrow is None:
            continue
        hdr = {c: str(sh.iat[hrow, c]).strip() for c in range(sh.shape[1])}
        if kind is None:
            kind = 'tables' if any(h == 'Win' for h in hdr.values()) else 'slots'
        col = next((c for c, h in hdr.items() if (h.startswith('Net Revenue') if kind == 'slots' else h.startswith('Win'))), None)
        if col is None:
            continue
        d, ytd = {}, None
        for r in range(hrow + 1, sh.shape[0]):
            lab = str(sh.iat[r, 0]).strip().lower()
            if lab in MONTHS:
                v = sh.iat[r, col]
                d[f'{year:04d}-{MONTHS.index(lab) + 1:02d}'] = float(v) if pd.notna(v) else np.nan
            elif lab.startswith('ytd'):
                v = sh.iat[r, col]
                ytd = float(v) if pd.notna(v) else None
        res[(casino, kind)] = (d, ytd)
    return res


def trim(d):
    ms = sorted(m for m, v in d.items() if v and not pd.isna(v))
    if not ms:
        return {}
    return {m: (0.0 if pd.isna(v) else v) for m, v in d.items() if ms[0] <= m <= ms[-1]}


def main():
    current, old, versions = download()
    rec = {}   # (uid, month) -> dict
    ytd_checks = []
    for yr, fn in old:
        res = parse_old_xlsx(fn, yr)
        for uid in UNITS:
            if (uid, 'slots') not in res:
                continue
            sl = trim(res[(uid, 'slots')][0])          # months the casino operated (and that are reported)
            tb = res.get((uid, 'tables'), ({}, None))[0]
            for m in sl:
                r = rec.setdefault((uid, m), dict(src=fn))
                r['slots'] = sl[m]
                t = tb.get(m, np.nan)
                r['tables'] = t
            for kind in ('slots', 'tables'):
                if (uid, kind) in res:
                    d, ytd = res[(uid, kind)]
                    ytd_checks.append((uid, yr, kind, sum(v for v in d.values() if not pd.isna(v)), ytd, fn))
    for yr, uid, fn in sorted(current):
        if yr < 2018:
            continue
        o = parse_pdf(fn, yr)
        sl = trim({m: v for m, v in o['slots'].items() if m.startswith(str(yr))})
        tb = {m: v for m, v in o['tables'].items() if m in sl}
        for m in sl:
            r = rec.setdefault((uid, m), {})
            r.update(src=fn, slots=sl[m], tables=tb.get(m, np.nan))
        # the regulator's YTD column includes a trailing partial month, which is dropped from the panel
        ytd_checks.append((uid, yr, 'slots', sum(sl.values()) + o.get('partial_slots', 0.0), o['ytd_slots'], fn))
        ytd_checks.append((uid, yr, 'tables', sum(v for v in tb.values() if not pd.isna(v)) + o.get('partial_tables', 0.0),
                           o['ytd_tables'], fn))
    # publication dates from versions
    pub = {}
    for fn in versions:
        try:
            o = parse_pdf(fn)
        except Exception as e:
            continue
        a = o.get('asof')
        if a is None or a.day != calendar.monthrange(a.year, a.month)[1]:
            continue
        md = pymupdf.open(os.path.join(CACHE, fn)).metadata
        mm = re.search(r'D:(\d{8})', md.get('creationDate') or '')
        if not mm:
            continue
        c = datetime.strptime(mm.group(1), '%Y%m%d').date()
        lag = (c - a).days
        if not 0 <= lag <= 45:
            continue
        uid = 'ME_OXFORD' if 'oxford' in fn.lower() else 'ME_HOLLYWOOD_BANGOR'
        m = f'{a.year:04d}-{a.month:02d}'
        if (uid, m) not in pub or c < pub[(uid, m)]:
            pub[(uid, m)] = c
    rows = []
    for (uid, m), r in sorted(rec.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        if m < '2012-01':
            continue
        s = r.get('slots', np.nan)
        t = r.get('tables', np.nan)
        ggr = (0 if pd.isna(s) else s) + (0 if pd.isna(t) else t)
        pdv = pub.get((uid, m)) or pub.get(('ME_OXFORD' if uid == 'ME_HOLLYWOOD_BANGOR' else 'ME_HOLLYWOOD_BANGOR', m))
        rows.append(dict(state='ME', unit=UNITS[uid], unit_id=uid, unit_level='property', month=m, ggr=round(ggr, 2),
                         slots=s, tables=t, n_casinos=np.nan, measure='GGR',
                         pub_date=pdv.isoformat() if pdv else '', pub_source='pdf_metadata' if pdv else '',
                         source_file=r['src']))
    df = pd.DataFrame(rows)
    months = sorted(df.month.unique())
    tot = []
    for m in months:
        d = df[df.month == m]
        tot.append(dict(state='ME', unit='__STATE_TOTAL__', unit_id='ME__STATE_TOTAL__', unit_level='state_total', month=m,
                        ggr=np.nan, slots=np.nan, tables=np.nan, n_casinos=len(d), measure='GGR',
                        pub_date=d.pub_date.max() if (d.pub_date != '').any() else '',
                        pub_source='pdf_metadata' if (d.pub_date != '').any() else '',
                        source_file='not published (no monthly statewide total)'))
    df = pd.concat([df, pd.DataFrame(tot)], ignore_index=True)
    # checks: per year, both casinos, sum of months vs regulator YTD columns
    ck = []
    yc = pd.DataFrame(ytd_checks, columns=['uid', 'year', 'kind', 'sum', 'ytd', 'fn'])
    for yr, g in yc.groupby('year'):
        if g.ytd.isna().any():
            note = 'some YTD cells missing'
        else:
            note = ''
        su, rt = g['sum'].sum(), g.ytd.fillna(0).sum()
        last = df[(df.month.str[:4] == str(yr)) & (df.unit_level == 'property')].month.max()
        det = '; '.join(f"{r.uid} {r.kind}: {(r['sum'] - (r.ytd or 0)):+,.2f}" for _, r in g.iterrows())
        ck.append(dict(month=last, sum_of_units=round(su, 2), regulator_total=round(rt, 2),
                       diff_pct=round((su - rt) / rt * 100, 4) if rt else np.nan,
                       note=f'YTD check {yr}: sum of parsed months (both casinos, slots+tables) vs regulator YTD columns '
                            f'({", ".join(sorted(set(g.fn)))}); per part diff $: {det}. {note}'.strip()))
    ck = pd.DataFrame(ck)
    assert not df.duplicated(['unit_id', 'month']).any()
    prop = df[df.unit_level == 'property'].sort_values(['unit_id', 'month']).copy()
    prop['prev'] = prop.groupby('unit_id').ggr.shift()
    prop['ratio'] = prop.ggr / prop.prev
    odd = prop[((prop.ratio > 3) | (prop.ratio < 1 / 3)) & ~prop.month.between('2020-03', '2020-08')]
    print('jumps:'); print(odd[['unit_id', 'month', 'prev', 'ggr']].to_string())
    print(ck[['month', 'sum_of_units', 'regulator_total', 'diff_pct']].to_string())
    allm = pd.period_range(prop.month.min(), prop.month.max(), freq='M').astype(str)
    for u in UNITS:
        have = set(prop[prop.unit_id == u].month)
        miss = [m for m in allm if m not in have and not (u == 'ME_OXFORD' and m < '2012-06')]
        print(u, 'missing months', miss)
    print('months', prop.month.min(), prop.month.max(), 'pub filled', (prop.pub_date != '').mean().round(3))
    df.to_csv(os.path.join(DATA, 'state_me.csv.gz'), index=False, compression='gzip')
    ck.to_csv(os.path.join(DATA, 'state_me_checks.csv.gz'), index=False, compression='gzip')
    return df, ck


if __name__ == '__main__':
    main()
