"""Rhode Island monthly casino revenue by facility (2012-01 .. latest), Rhode Island Lottery.

Sources
-------
Rhode Island Lottery "Financials" page https://www.rilot.com/en-us/about-us/financials.html, which
links one PDF per state fiscal year (July-June):
  * VLT Revenue Information by Facility (monthly Cash In / Cash Out / NTI / machines by facility):
      https://www.rilot.com/content/dam/interactive/ilottery/pdfs/financial/VLTDatabyFacilitybyMonth-20YY.pdf
      (FY2024: VLTDataFacilityMonthYear.pdf; FY2025+: VLTDatabyFacilitybyMonthFY20YY.pdf)
  * Monthly Net Table Games Revenue by facility:
      .../TableGamesSummaryFY20YY.pdf (FY2024: TableGamesWebsite2024.pdf)
Both cached in cache/ri/. For publication dating, every archived version of these PDFs in the
Internet Archive (http://web.archive.org/cdx/search/cdx?url=rilot.com&matchType=domain) is also
downloaded (cache/ri/wb_<timestamp>_<file>.pdf).

Measure
-------
ggr = VLT net terminal income (NTI = cash in - cash out) + "Total Net Table Games Revenue"
(table win before the state/town/operator split; includes poker). measure = "NTI+TG".
slots = NTI, tables = net table games revenue. Dollars. Sports betting (Sportsbook) and iGaming
reports are separate and excluded.
__STATE_TOTAL__ = the "Combined"/"Both" VLT block + the "Combined" table section (FY2013-18 there is
only one table-games section, Twin River, which is then the statewide table total).

Units
-----
RI_TWIN_RIVER_LINCOLN  "Twin River" -> "Bally's Twin River Casino" (Lincoln; Twin River Worldwide,
                       renamed Bally's Corp. Nov 2020). Table games from June 2013.
RI_NEWPORT_GRAND       "Newport Grand" (VLT only; ceased operations 2018-08-28).
RI_TIVERTON            "Tiverton Casino" -> "Bally's Tiverton Casino" (opened 2018-08-29; VLT+tables).
FY2019's second VLT block is "Newport Grand/Tiverton Casino" combined; August 2018 is split with the
footnote in that PDF (Newport Grand NTI Aug 1-28 = $2,947,604; Tiverton Aug 29-31 = $717,690);
July 2018 is Newport Grand, Sep 2018 onward Tiverton.

Publication date
----------------
PDF CreationDate (pub_source = pdf_metadata). Each FY PDF is re-created each month, so a version's
CreationDate dates its newest month. The current and all archived versions are read; when a version
with newest month M was created <= 45 days after the end of M, that date is pub_date for M. Other
months are blank. Typical lag observed ~4 weeks (e.g. July 2026 created 2026-08-28; June 2026
created 2026-07-28).

Quirks
------
* COVID-19: facilities closed 2020-03-14, reopened 2020-06-08; April-May 2020 shown as "-" -> 0.
* FY2013 table games file shows Mar-May 2013 as 0 with negative RI Lottery transfers (pre-opening
  costs); table games revenue starts June 2013.
* The PDFs are "unaudited and unadjusted".

* FY2021 table-games PDF has no text for its "Combined" section, so for 2020-07..2021-06 the table
  part of __STATE_TOTAL__ is Twin River + Tiverton (noted in the checks file).
* Dec 2020: casinos paused 2020-11-29..2020-12-20 by state order (Jan 2021 jump is the reopening).

Spot checks (run 2026-09-23; data/state_ri_checks.csv.gz)
--------------------------------------------------------
Every month 2012-01..2026-07 (175): facilities vs the regulator's Combined VLT block: 173 exact, 2
off by $1 (rounding); Twin River + Tiverton table games vs the Combined table section: exact in all
85 months where both exist. Max |diff| of sum of units vs __STATE_TOTAL__ = 0.000%. Month/month jumps
> 3x: Tiverton 2018-09 (opened 2018-08-29) and both casinos 2021-01 (reopening after the Dec 2020
pause). pub_date found for ~28% of rows (median lag 27 days after month end).
"""
import os, re, sys, time, json, collections
from datetime import datetime, date
import requests
import pandas as pd
import numpy as np
import pymupdf

ROOT = '/Users/davidspinelli/Documents/Claude Space/research/nowcast/gaming'
CACHE = os.path.join(ROOT, 'cache', 'ri')
DATA = os.path.join(ROOT, 'data')
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) Chrome/124.0 Safari/537.36'}
S = requests.Session(); S.headers.update(UA)
BASE = 'https://www.rilot.com'
FIN = BASE + '/en-us/about-us/financials.html'
MON = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']


def get(url, tries=4):
    for a in range(tries):
        try:
            time.sleep(1.0)
            r = S.get(url, timeout=120)
            if r.status_code == 200:
                return r
            print('HTTP', r.status_code, url)
            if r.status_code in (403, 404):
                return None
        except Exception as e:
            print('err', e)
        time.sleep(10 * (a + 1))
    return None


def fy_of(url):
    m = re.search(r'(?:FY|-)(20\d\d)\.pdf$', url, re.I) or re.search(r'(20\d\d)\.pdf$', url)
    if m:
        return int(m.group(1))
    if 'VLTDataFacilityMonthYear' in url:
        return 2024
    return None


def download():
    os.makedirs(CACHE, exist_ok=True)
    r = get(FIN)
    html = r.text
    open(os.path.join(CACHE, 'financials.html'), 'w').write(html)
    files = {'vlt': {}, 'tg': {}}
    for href in re.findall(r'href="([^"]+\.pdf)"', html):
        fn = href.split('/')[-1]
        kind = 'vlt' if fn.startswith('VLTData') else ('tg' if fn.startswith('TableGames') else None)
        if kind is None:
            continue
        fy = fy_of(href)
        if fy is None or fy < 2012:
            continue
        p = os.path.join(CACHE, fn)
        # the current fiscal year's file changes every month: refresh it if older than 7 days
        cur_fy = date.today().year + (1 if date.today().month >= 7 else 0)
        if fy >= cur_fy - 1 and os.path.exists(p) and time.time() - os.path.getmtime(p) > 7 * 86400:
            os.rename(p, p.replace('.pdf', f'__{datetime.fromtimestamp(os.path.getmtime(p)):%Y%m%d}.pdf'))
        if not os.path.exists(p):
            rr = get(BASE + href)
            if rr is None:
                continue
            open(p, 'wb').write(rr.content)
        files[kind][fy] = fn
    # archived versions for publication dating
    cdxp = os.path.join(CACHE, 'cdx_rilot.txt')
    if not os.path.exists(cdxp):
        rr = get('http://web.archive.org/cdx/search/cdx?url=rilot.com&matchType=domain'
                 '&fl=original,timestamp,statuscode,digest&filter=statuscode:200&limit=300000')
        open(cdxp, 'w').write(rr.text)
    seen = set()
    versions = []
    for l in open(cdxp).read().splitlines():
        u, ts, st, dg = l.split()
        b = u.split('/')[-1]
        if not re.search(r'^(vltdatabyfacilitybymonth|vltdatafacilitymonthyear|tablegames)', b, re.I) or not b.lower().endswith('.pdf'):
            continue
        if 'tojune' in b.lower():
            continue
        m = re.search(r'(20\d\d)', b)
        if not m or int(m.group(1)) < 2012:
            continue
        if dg in seen:
            continue
        seen.add(dg)
        fn = f'wb_{ts}_{b}'
        p = os.path.join(CACHE, fn)
        if not os.path.exists(p):
            rr = get(f'http://web.archive.org/web/{ts}id_/{u}')
            if rr is None or not rr.content.startswith(b'%PDF'):
                continue
            open(p, 'wb').write(rr.content)
        versions.append(fn)
    return files, versions


def tokens(path):
    t = pymupdf.open(os.path.join(CACHE, path))[0].get_text()
    return [x.strip() for x in t.split('\n') if x.strip() and x.strip() != '$']


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


def month_label(tok):
    m = re.fullmatch(r'([A-Za-z]{3})[a-z]*,?\s*(\d{2,4})?', tok)
    if m and m.group(1).lower() in MON:
        return MON.index(m.group(1).lower()) + 1
    return None


def ym(fy, mn):
    y = fy - 1 if mn >= 7 else fy
    return f'{y:04d}-{mn:02d}'


def parse_vlt(fn, fy):
    tk = tokens(fn)
    tail = ' | '.join(tk[-8:])
    # block names are the last three tokens after "FY 20xx"
    i = max(j for j, x in enumerate(tk) if re.fullmatch(r'FY\s*20\d\d', x))
    names = [re.sub(r'[∆*]', '', x).strip() for x in tk[i + 1:i + 4]]
    recs = collections.defaultdict(list)  # month -> [nti per block]
    k = 0
    while k < len(tk):
        mn = month_label(tk[k])
        if mn is None or tk[k].lower().startswith('total'):
            k += 1
            continue
        vals = []
        k += 1
        while k < len(tk) and month_label(tk[k]) is None and not tk[k].startswith('Total'):
            vals.append(tk[k])
            k += 1
        nums = [num(v) for v in vals if not v.endswith('%')]
        nums = [v for v in nums if v is not None]
        nti = nums[2] if len(nums) >= 3 else 0.0
        recs[ym(fy, mn)].append(nti)
    out = []
    for m, v in recs.items():
        if len(v) != 3:
            print('WARN vlt blocks', fn, m, v)
        out.append(dict(month=m, b1=v[0], b2=v[1] if len(v) > 1 else np.nan, comb=v[-1]))
    return names, pd.DataFrame(out)


def parse_tg(fn, fy):
    tk = tokens(fn)
    sections = []  # list of (label, {month: value})
    cur = None
    k = 0
    while k < len(tk):
        x = tk[k]
        if re.fullmatch(r'Total\s+Net', x) and k + 1 < len(tk):
            cur = (tk[k + 1], {})
            sections.append(cur)
            k += 2
            continue
        mn = month_label(x)
        if mn is not None and cur is not None and not re.match(r'(?i)total', x):
            k += 1
            vals = []
            while k < len(tk) and month_label(tk[k]) is None and not tk[k].startswith('Total'):
                vals.append(tk[k]); k += 1
            nums = [num(v) for v in vals]
            nums = [v for v in nums if v is not None]
            m = re.search(r'(\d{4})', x)
            cur[1][ym(fy, mn)] = nums[0] if nums else 0.0
            continue
        k += 1
    return sections


def pdf_created(fn):
    md = pymupdf.open(os.path.join(CACHE, fn)).metadata
    m = re.search(r'D:(\d{8})', md.get('creationDate') or md.get('modDate') or '')
    return datetime.strptime(m.group(1), '%Y%m%d').date() if m else None


def newest_month(fn):
    b = fn.split('_')[-1] if fn.startswith('wb_') else fn
    fy = fy_of(b)
    if fy is None:
        m = re.search(r'(20\d\d)', b)
        fy = int(m.group(1)) if m else None
    if fy is None:
        return None
    try:
        if 'vlt' in fn.lower():
            _, df = parse_vlt(fn, fy)
            df = df[df.comb != 0]
            return df.month.max() if len(df) else None
        secs = parse_tg(fn, fy)
        ms = [m for lab, d in secs for m, v in d.items() if v]
        return max(ms) if ms else None
    except Exception as e:
        return None


def main():
    files, versions = download()
    pub = {}
    for fn in versions + list(files['vlt'].values()) + list(files['tg'].values()):
        c = pdf_created(fn); m = newest_month(fn)
        if c is None or m is None:
            continue
        me = (pd.Timestamp(m + '-01') + pd.offsets.MonthEnd(0)).date()
        if 0 <= (c - me).days <= 45:
            key = ('vlt' if 'vlt' in fn.lower() else 'tg', m)
            if key not in pub or c < pub[key]:
                pub[key] = c
    rows, checks = [], []
    vlt = {}
    for fy, fn in sorted(files['vlt'].items()):
        names, df = parse_vlt(fn, fy)
        for _, r in df.iterrows():
            vlt[r.month] = (names, r.b1, r.b2, r.comb, fn)
    tg = {}
    for fy, fn in sorted(files['tg'].items()):
        for lab, d in parse_tg(fn, fy):
            l = lab.lower()
            key = 'comb' if '/' in l else ('tiv' if 'tiverton' in l else ('tr' if 'twin' in l else None))
            if key is None:
                print('WARN unknown tg section', fn, lab); continue
            for m, v in d.items():
                tg.setdefault(m, {})[key] = (v, fn)
    months = sorted(m for m in vlt if '2012-01' <= m)
    last = max(m for m in months if vlt[m][3] != 0)
    months = [m for m in months if m <= last]
    for m in months:
        names, b1, b2, comb, fn = vlt[m]
        t = tg.get(m, {})
        tr_t = t.get('tr', (np.nan, ''))[0]
        tv_t = t.get('tiv', (np.nan, ''))[0]
        cb_t = t.get('comb', (np.nan, ''))[0]
        if m < '2013-06':
            tr_t = np.nan if m < '2013-03' else tr_t
        units = []
        n1 = names[0]
        units.append(('RI_TWIN_RIVER_LINCOLN', n1, b1, tr_t))
        n2 = names[1]
        if m < '2018-08':
            units.append(('RI_NEWPORT_GRAND', n2.split('/')[0].strip(), b2, np.nan))
        elif m == '2018-08':
            assert abs(b2 - (2947604 + 717690)) < 2, b2
            units.append(('RI_NEWPORT_GRAND', 'Newport Grand', 2947604.0, np.nan))
            units.append(('RI_TIVERTON', 'Tiverton Casino', 717690.0, tv_t))
        else:
            units.append(('RI_TIVERTON', n2.replace('Newport Grand/', ''), b2, tv_t))
        pv = pub.get(('vlt', m)); pt = pub.get(('tg', m))
        pdv = max([x for x in (pv, pt) if x] or [None]) if (pv and (pt or m < '2013-06')) else (pv or pt)
        srcs = fn + (' + ' + t.get('tr', (0, ''))[1] if t else '')
        for uid, nm, s, tb in units:
            ggr = (s or 0) + (0 if pd.isna(tb) else tb)
            rows.append(dict(state='RI', unit=nm, unit_id=uid, unit_level='property', month=m, ggr=round(ggr, 2),
                             slots=s, tables=tb, n_casinos=np.nan, measure='NTI+TG',
                             pub_date=pdv.isoformat() if pdv else '', pub_source='pdf_metadata' if pdv else '',
                             source_file=srcs))
        tg_note = ''
        if pd.notna(cb_t):
            st_t = cb_t
        elif pd.notna(tv_t) and m >= '2018-08':
            st_t = (0 if pd.isna(tr_t) else tr_t) + tv_t
            tg_note = 'no Combined table section in PDF text (FY2021): table part of total = Twin River + Tiverton'
        else:
            st_t = tr_t if pd.notna(tr_t) else 0.0
        st = comb + (st_t or 0)
        rows.append(dict(state='RI', unit='__STATE_TOTAL__', unit_id='RI__STATE_TOTAL__', unit_level='state_total',
                         month=m, ggr=round(st, 2), slots=comb, tables=st_t, n_casinos=len(units), measure='NTI+TG',
                         pub_date=pdv.isoformat() if pdv else '', pub_source='pdf_metadata' if pdv else '',
                         source_file=srcs))
        s_units = sum((u[2] or 0) + (0 if pd.isna(u[3]) else u[3]) for u in units)
        note = []
        if pd.notna(cb_t) and pd.notna(tr_t) and pd.notna(tv_t):
            note.append(f'tables TR+Tiv vs Combined {tr_t + tv_t - cb_t:+,.0f}')
        note.append(f'VLT blocks b1+b2 vs combined {b1 + b2 - comb:+,.0f}')
        if tg_note:
            note.append(tg_note)
        checks.append(dict(month=m, sum_of_units=round(s_units, 2), regulator_total=round(st, 2),
                           diff_pct=round((s_units - st) / st * 100, 4) if st else 0.0, note='; '.join(note)))
    df = pd.DataFrame(rows)
    ck = pd.DataFrame(checks)
    assert not df.duplicated(['unit_id', 'month']).any()
    prop = df[df.unit_level == 'property'].sort_values(['unit_id', 'month']).copy()
    prop['prev'] = prop.groupby('unit_id').ggr.shift()
    prop['ratio'] = prop.ggr / prop.prev
    odd = prop[((prop.ratio > 3) | (prop.ratio < 1 / 3)) & ~prop.month.between('2020-03', '2020-07')]
    print('jumps:'); print(odd[['unit_id', 'month', 'prev', 'ggr']].to_string())
    print('checks n', len(ck), 'max |diff| %', ck.diff_pct.abs().max())
    print(ck[ck.diff_pct.abs() > 0.01].to_string())
    print('months', df.month.min(), df.month.max(), 'pub filled', (prop.pub_date != '').mean().round(3))
    df.to_csv(os.path.join(DATA, 'state_ri.csv.gz'), index=False, compression='gzip')
    ck.to_csv(os.path.join(DATA, 'state_ri_checks.csv.gz'), index=False, compression='gzip')
    return df, ck


if __name__ == '__main__':
    main()
