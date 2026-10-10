#!/usr/bin/env python3
"""POC standalone importer for justice.gov.ma sitemaps.

This script does not require Django; it fetches sitemap.xml, downloads a few pages
and writes sample JSON files to the given output directory.
"""
import os
import sys
import time
import json
import argparse
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def fetch_sitemap_index(url, headers=None):
    headers = headers or {}
    r = requests.get(url, timeout=15, headers=headers)
    r.raise_for_status()
    # try parsing as XML sitemap first
    soup_xml = BeautifulSoup(r.content, 'xml')
    loc_tags = soup_xml.find_all('loc')
    locs = [tag.text for tag in loc_tags]
    return locs


def fetch_page(url, headers=None):
    headers = headers or {}
    r = requests.get(url, timeout=15, headers=headers)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, 'html.parser')
    title = soup.title.string.strip() if soup.title else ''
    article = soup.find('article')
    if article:
        content = article.get_text(separator=' ', strip=True)
    else:
        divs = soup.find_all('div')
        content = ''
        for d in divs:
            txt = d.get_text(separator=' ', strip=True)
            if len(txt) > 200:
                content = txt
                break
    date = None
    time_tag = soup.find('time')
    if time_tag and time_tag.has_attr('datetime'):
        date = time_tag['datetime']
    if not date and time_tag:
        date = time_tag.get_text(strip=True)
    return {'url': url, 'title': title, 'date': date, 'content_snippet': content[:2000]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sitemap', default='https://justice.gov.ma/sitemap.xml')
    parser.add_argument('--limit', type=int, default=5)
    parser.add_argument('--out', default='data/justice_gov_ma')
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)
    headers = {'User-Agent': 'OLDP-POC/1.0 (+https://openlegaldata.io)'}
    print(f'Fetching sitemap: {args.sitemap}')
    locs = fetch_sitemap_index(args.sitemap, headers=headers)
    # If locs contain sitemap xml links (ending with .xml), treat as index
    sitemap_links = [l for l in locs if l.endswith('.xml')]
    urls = []
    if sitemap_links:
        print(f'Found {len(sitemap_links)} sitemap entries (index).')
        for sm in sitemap_links:
            if len(urls) >= args.limit:
                break
            try:
                print('Reading sitemap', sm)
                sub_locs = fetch_sitemap_index(sm, headers=headers)
                for l in sub_locs:
                    if len(urls) >= args.limit:
                        break
                    urls.append(l)
            except Exception as e:
                print('Failed to read sitemap', sm, 'error', e)
            time.sleep(0.1)
    else:
        # locs directly contain page URLs
        print(f'Found {len(locs)} URLs in sitemap (no sub-sitemaps).')
        urls = locs[: args.limit]

    print('Will fetch', len(urls), 'pages')
    for i, u in enumerate(urls, start=1):
        try:
            print('Fetching', u)
            doc = fetch_page(u, headers=headers)
            out_file = os.path.join(args.out, f'sample_{i}.json')
            with open(out_file, 'w', encoding='utf8') as fh:
                json.dump(doc, fh, ensure_ascii=False, indent=2)
            print('Wrote', out_file)
        except Exception as e:
            print('Failed to fetch', u, 'error', e)
        time.sleep(0.2)


if __name__ == '__main__':
    main()
