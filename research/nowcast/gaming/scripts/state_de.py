"""Delaware (Delaware Lottery) monthly video lottery + table games net proceeds by agent -> data/state_de.csv.gz

Usage:  python3 scripts/state_de.py [download]      (DE_REFRESH=1 re-fetches the current fiscal-year pages; all
        other pages are read from cache/de/)

SOURCES (HTML tables, no PDFs)
  Video lottery (VL):
    https://www.delottery.com/More/Video-Lottery/Monthly-Net-Proceeds/Monthly-Proceeds-And-Track-Data/<YYYY>
      (calendar-year pages 2011..2022; the 2022 page stops at June 2022)
    https://www.delottery.com/More/Video-Lottery/Monthly-Net-Proceeds/Monthly-Proceeds-And-Distribution-Financial-Year/<FY>
      (FY2023 = Jul 2022-Jun 2023 .. FY2027)
  Table games (TG):
    https://www.delottery.com/More/Table-Games/Revenue-Distribution/Monthly-Data-Summary/<YYYY>   (2011..2022-06)
    https://www.delottery.com/More/Table-Games/Revenue-Distribution/Monthly-Proceeds-And-Distribution-Financial-Year/<FY>

MEASURE  ggr = slots + tables where slots = VL "NET PROCEEDS" (amount played - amount won, before the statutory
  split to state/vendors/purses/track) and tables = TG "NET PROCEEDS"/"Net Proceeds (Win)" (incl. poker).
  Sports lottery, iGaming and traditional lottery are excluded. __STATE_TOTAL__ = the pages' TOTAL column
  (VL + TG). "FISCAL YEAR TOTALS" blocks and '$' placeholder blocks for future periods are skipped.

ACCOUNTING PERIODS -> CALENDAR MONTHS (important)
  The Lottery reports by accounting month: 4- or 5-week periods ending on a Sunday; since 2018 the fiscal year
  closes on June 30, so June ends on Jun 30 and July starts Jul 1 (e.g. 2021-07-01..2021-07-25 = 25 days). Page
  labels are unreliable (VL 2020-2022 are labelled with calendar month-ends although the 5-week pattern shows Sunday
  periods; TG FY2025 labels are off by 1-2 days), so each period's true end = explicit range if printed (FY2025+
  "07/01/25 - 07/27/25"), else a Sunday label from either page, else June 30 (2018+), else the last Sunday on/before
  the label; start = previous end + 1. Each period's net proceeds are then allocated to calendar months PRO RATA BY
  DAYS (uniform daily revenue assumed; annual totals preserved). A calendar month therefore partly depends on the
  next accounting period; only months fully covered by published periods are output.

MONTHS  2012-01 .. 2026-08 (period ending 2026-08-31 is the latest published on 2026-09-23).

UNITS  3 racetrack casinos (unit_level=property): DE_DELAWARE_PARK (Delaware Park), DE_DOVER_DOWNS (DOVER DOWNS ->
  BALLY'S DOVER on the VL pages from 2021, TG pages from FY2023; Dover Downs Gaming & Entertainment, acquired by
  Twin River/Bally's 2019), DE_HARRINGTON (Harrington Raceway & Casino). `unit` = VL-page column name of the
  accounting period contributing most days to that month.
  COVID: casinos closed Mar 16 - Jun 8 2020; VL April/May periods are 0 and TG has "No monthly proceeds reports for
  April and May" -> 0 (calendar Apr and May 2020 = 0).

PUBLICATION DATES  none: the pages are overwritten in place, carry no posting date, and Lottery press releases do
  not cover monthly proceeds. pub_date/pub_source are blank. (Observed: the period ending 2026-08-31 was online by
  2026-09-23, i.e. within ~3 weeks.)

SPOT CHECKS (data/state_de_checks.csv.gz): one row per ACCOUNTING period (month = label month, note gives the true
  period dates): sum of the three agents vs the TOTAL column, VL and TG separately and combined, all 176 periods
  2012-01..2026-08: max |diff| 0.0003 % (rounding; VL is published rounded to $100 in 2011-2017 and 2020-2021). After pro-rating
  the monthly sum of units differs from the pro-rated total by <= $97. Dollars. No month/month jumps >3x or <1/3
  outside Mar-Jul 2020.
"""
import os, re, sys, time, html
import requests
import pandas as pd
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, 'cache', 'de')
DATA = os.path.join(ROOT, 'data')
BASE = 'https://www.delottery.com'
UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
os.makedirs(CACHE, exist_ok=True)
os.makedirs(DATA, exist_ok=True)
REFRESH = os.environ.get('DE_REFRESH') == '1'
_last = [0.0]


def fetch(url, fname, refresh=False):
    path = os.path.join(CACHE, fname)
    if os.path.exists(path) and os.path.getsize(path) > 0 and not refresh:
        return path
    for attempt in range(4):
        wait = 1.0 - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        try:
            r = requests.get(url, headers={'User-Agent': UA}, timeout=60)
            if r.status_code == 200 and 'NotFound' not in r.url:
                with open(path, 'wb') as f:
                    f.write(r.content)
                return path
            print('HTTP', r.status_code, url, file=sys.stderr)
            if r.status_code == 404 or 'NotFound' in r.url:
                return None
        except Exception as e:  # noqa
            print('ERR', e, url, file=sys.stderr)
        time.sleep(2 ** attempt)
    return None


VL = '/More/Video-Lottery/Monthly-Net-Proceeds/'
TG = '/More/Table-Games/Revenue-Distribution/'
CURRENT_FY = 2027


def sources():
    """(kind, url, cache name). Calendar-year pages up to 2022, fiscal-year pages from FY2023."""
    out = []
    for y in range(2011, 2023):
        out.append(('vl', BASE + VL + 'Monthly-Proceeds-And-Track-Data/%d' % y, 'vl_track_%d.html' % y))
        out.append(('tg', BASE + TG + 'Monthly-Data-Summary/%d' % y, 'tg_summary_%d.html' % y))
    for fy in range(2023, CURRENT_FY + 1):
        out.append(('vl', BASE + VL + 'Monthly-Proceeds-And-Distribution-Financial-Year/%d' % fy, 'vl_fy%d.html' % fy))
        out.append(('tg', BASE + TG + 'Monthly-Proceeds-And-Distribution-Financial-Year/%d' % fy, 'tg_fy%d.html' % fy))
    return out


if __name__ == '__main__' and 'download' in sys.argv:
    for kind, url, fn in sources():
        p = fetch(url, fn, refresh=REFRESH and str(CURRENT_FY) in fn)
        print(fn, p is not None, os.path.getsize(p) if p else 0)


# ----------------------------------------------------------------------------------------------
# Parsing: HTML tables, one block per Lottery accounting period
# ----------------------------------------------------------------------------------------------
import datetime as dt

UNIT_IDS = {'delawarepark': 'DE_DELAWARE_PARK', 'doverdowns': 'DE_DOVER_DOWNS', 'ballysdover': 'DE_DOVER_DOWNS',
            'harrington': 'DE_HARRINGTON', 'total': '__STATE_TOTAL__'}


def norm(s):
    return re.sub(r'[^a-z]', '', s.lower())


def _cells(r):
    return [re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', c))).strip().replace('’', "'")
            for c in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', r, re.S)]


def _date(s):
    for fmt in ('%m/%d/%Y', '%m/%d/%y'):
        try:
            return dt.datetime.strptime(s.strip(), fmt).date()
        except ValueError:
            pass
    return None


def _num(s):
    s = s.replace('$', '').replace(',', '').strip()
    if not re.fullmatch(r'\(?-?[\d.]+\)?', s):
        return None
    neg = s.startswith('(') or s.startswith('-')
    v = float(s.strip('()-'))
    return -v if neg else v


def parse_page(path):
    """-> list of {'label_end', 'start' (or None), 'end_explicit', 'values': {header name: net proceeds}}"""
    s = open(path, encoding='utf-8', errors='ignore').read()
    rows = [_cells(r) for tb in re.findall(r'<table.*?</table>', s, re.S) for r in re.findall(r'<tr.*?</tr>', tb, re.S)]
    hdr = rows[0]
    cols = {j: h for j, h in enumerate(hdr) if j >= 2 and h and h != '%'}
    out, cur = [], None
    for r in rows[1:]:
        if any('fiscal year total' in c.lower() for c in r):
            break
        if r and re.search(r'\d+/\d+/\d+', r[0]):
            ds = re.findall(r'\d+/\d+/\d+', r[0])
            cur = {'label_end': _date(ds[-1]), 'start': _date(ds[0]) if len(ds) == 2 else None,
                   'end_explicit': len(ds) == 2, 'label': r[0], 'values': None}
        if cur is None or len(r) < 3 or not r[1].upper().startswith('NET PROCEEDS'):
            continue
        if len(r) == len(hdr):
            vals = {h: _num(r[j]) for j, h in cols.items()}
        else:  # fall back to order of the non-empty, non-% cells
            nums = [c for c in r[2:] if c and not c.endswith('%')]
            vals = {h: _num(v) for h, v in zip(cols.values(), nums)}
            print('DE %s %s: row length %d != header %d, used order' % (os.path.basename(path), cur['label'],
                                                                        len(r), len(hdr)), file=sys.stderr)
        if all(v is None for v in vals.values()):
            continue  # template block for a future period ('$' placeholders)
        if cur['values'] is None:
            cur['values'] = vals
            out.append(cur)
    return out


def is_sunday(d):
    return d.weekday() == 6


def true_end(cands, explicit):
    """Accounting periods end on Sundays (fiscal year ends June 30 from 2018). Page labels are sometimes
    calendar month-ends or off by a day or two; pick the credible date."""
    if explicit:
        return explicit[0]
    sund = [d for d in cands if is_sunday(d)]
    if sund:
        return max(set(sund), key=sund.count)
    j30 = [d for d in cands if d.month == 6 and d.day == 30 and d.year >= 2018]
    if j30:
        return j30[0]
    d = min(cands)
    return d - dt.timedelta(days=(d.weekday() + 1) % 7)  # last Sunday on or before


def build_periods():
    """Accounting periods keyed by the calendar month of their end label, with VL and TG net proceeds."""
    per = {}
    for kind, url, fn in sources():
        path = fetch(url, fn, refresh=REFRESH and str(CURRENT_FY) in fn)
        if path is None:
            print('DE missing page', fn, file=sys.stderr)
            continue
        for p in parse_page(path):
            key = (p['label_end'].year, p['label_end'].month)
            d = per.setdefault(key, {'cands': [], 'explicit': [], 'starts': [], 'vl': None, 'tg': None,
                                     'names': {}, 'files': []})
            if d[kind] is not None:
                raise ValueError('DE duplicate period %s %s (%s)' % (key, kind, fn))
            vals = {}
            for h, v in p['values'].items():
                uid = UNIT_IDS.get(norm(h))
                if uid is None:
                    raise KeyError('DE unknown column %r in %s' % (h, fn))
                vals[uid] = v
                if kind == 'vl' or uid not in d['names']:
                    d['names'][uid] = h
            d[kind] = vals
            d['files'].append(fn)
            (d['explicit'] if p['end_explicit'] else d['cands']).append(p['label_end'])
            if p['start']:
                d['starts'].append(p['start'])
    keys = sorted(per)
    prev_end = None
    for k in keys:
        d = per[k]
        d['end'] = true_end(d['cands'] + d['explicit'], d['explicit'])
        d['start'] = prev_end + dt.timedelta(days=1) if prev_end else None
        if d['starts'] and d['start'] and d['starts'][0] != d['start']:
            print('DE period %s: explicit start %s != previous end + 1 %s' % (k, d['starts'][0], d['start']),
                  file=sys.stderr)
        n = (d['end'] - d['start']).days + 1 if d['start'] else None
        if n is not None and not (26 <= n <= 37):
            print('DE period %s has %d days (%s - %s)' % (k, n, d['start'], d['end']), file=sys.stderr)
        if d['tg'] is None:  # table games closed Mar 16 - Jun 8 2020: 'No monthly proceeds reports for April and May'
            if k in ((2020, 4), (2020, 5)):
                d['tg'] = {u: 0.0 for u in d['vl']}
            else:
                raise ValueError('DE missing table games for %s' % (k,))
        if d['vl'] is None:
            raise ValueError('DE missing video lottery for %s' % (k,))
        prev_end = d['end']
    return per


def prorate(per):
    """Allocate each accounting period's net proceeds to calendar months pro rata by days."""
    acc = {}
    cover = {}
    for k in sorted(per):
        d = per[k]
        if d['start'] is None:
            continue  # first period (Jan 2011) only anchors the calendar
        n = (d['end'] - d['start']).days + 1
        day = d['start']
        while day <= d['end']:
            m = '%04d-%02d' % (day.year, day.month)
            nxt = (pd.Timestamp(day) + pd.offsets.MonthBegin(1)).date()
            seg_end = min(d['end'], nxt - dt.timedelta(days=1))
            w = ((seg_end - day).days + 1) / n
            cover[m] = cover.get(m, 0) + (seg_end - day).days + 1
            for kind in ('vl', 'tg'):
                for uid, v in d[kind].items():
                    a = acc.setdefault((m, uid), {'vl': 0.0, 'tg': 0.0, 'w': {}, 'files': set()})
                    a[kind] += (v or 0.0) * w
                    a['w'][k] = a['w'].get(k, 0) + w / 2
                    a['files'].update(d['files'])
            day = seg_end + dt.timedelta(days=1)
    rows = []
    for (m, uid), a in acc.items():
        per_m = pd.Period(m, 'M')
        if cover.get(m, 0) != per_m.days_in_month or m < '2012-01':
            continue  # month not fully covered by published periods
        main = max(a['w'], key=a['w'].get)  # accounting period contributing most days -> name as published
        name = per[main]['names'][uid] if uid != '__STATE_TOTAL__' else '__STATE_TOTAL__'
        rows.append({'state': 'DE', 'unit': name, 'unit_id': uid,
                     'unit_level': 'state_total' if uid == '__STATE_TOTAL__' else 'property', 'month': m,
                     'ggr': a['vl'] + a['tg'], 'slots': a['vl'], 'tables': a['tg'], 'n_casinos': np.nan,
                     'measure': 'VL net proceeds + table games net proceeds (win); accounting periods pro-rated to calendar months',
                     'pub_date': '', 'pub_source': '', 'source_file': ';'.join(sorted(a['files']))})
    return pd.DataFrame(rows).sort_values(['unit_level', 'unit_id', 'month']).reset_index(drop=True)


def checks(per):
    rows = []
    for k in sorted(per):
        d = per[k]
        if k < (2012, 1):
            continue
        su = sum(v or 0 for u, v in d['vl'].items() if u != '__STATE_TOTAL__') + \
            sum(v or 0 for u, v in d['tg'].items() if u != '__STATE_TOTAL__')
        reg = (d['vl'].get('__STATE_TOTAL__') or 0) + (d['tg'].get('__STATE_TOTAL__') or 0)
        vl_d = sum(v or 0 for u, v in d['vl'].items() if u != '__STATE_TOTAL__') - (d['vl'].get('__STATE_TOTAL__') or 0)
        tg_d = sum(v or 0 for u, v in d['tg'].items() if u != '__STATE_TOTAL__') - (d['tg'].get('__STATE_TOTAL__') or 0)
        rows.append({'month': '%04d-%02d' % k, 'sum_of_units': su, 'regulator_total': reg,
                     'diff_pct': 100 * (su - reg) / reg if reg else (0.0 if su == 0 else np.nan),
                     'note': 'accounting period %s..%s (label month); VL diff %.0f, TG diff %.0f' % (
                         d['start'], d['end'], vl_d, tg_d)})
    return pd.DataFrame(rows)


def jump_scan(df):
    out = []
    for uid, g in df[df.unit_level == 'property'].groupby('unit_id'):
        g = g.sort_values('month')
        r = g.ggr / g.ggr.shift(1)
        for m, x, v in zip(g.month, r, g.ggr):
            if '2020-03' <= m <= '2020-07':
                continue
            if pd.notna(x) and (x > 3 or x < 1 / 3):
                out.append((uid, m, round(x, 3), v))
    return out


if __name__ == '__main__' and 'download' not in sys.argv:
    per = build_periods()
    df = prorate(per)
    chk = checks(per)
    cols = ['state', 'unit', 'unit_id', 'unit_level', 'month', 'ggr', 'slots', 'tables', 'n_casinos', 'measure',
            'pub_date', 'pub_source', 'source_file']
    df = df[cols]
    assert not df.duplicated(['unit_id', 'month']).any()
    df.to_csv(os.path.join(DATA, 'state_de.csv.gz'), index=False, compression='gzip')
    chk.to_csv(os.path.join(DATA, 'state_de_checks.csv.gz'), index=False, compression='gzip')
    print('rows', len(df), 'units', df[df.unit_level == 'property'].unit_id.nunique(), 'months',
          df.month.min(), df.month.max(), df.month.nunique())
    print('max |diff_pct| (accounting periods)', chk.diff_pct.abs().max())
    t = df[df.unit_level == 'state_total'].set_index('month').ggr
    s = df[df.unit_level == 'property'].groupby('month').ggr.sum()
    print('max |diff| pro-rated months', (s - t).abs().max())
    print('jumps:', jump_scan(df))
