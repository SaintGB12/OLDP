import os
import json
import requests
import time
from urllib.parse import urljoin
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '..', '..', '..', 'data', 'justice_gov_ma')

class Command(BaseCommand):
    help = 'Import sample pages from justice.gov.ma sitemap for POC'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=5, help='Number of pages to fetch')
        parser.add_argument('--out', type=str, default='data/justice_gov_ma', help='Output directory')

    def handle(self, *args, **options):
        limit = options['limit']
        out = options['out']
        os.makedirs(out, exist_ok=True)

        sitemap_index = 'https://justice.gov.ma/sitemap.xml'
        self.stdout.write(f'Fetching sitemap index: {sitemap_index}')
        r = requests.get(sitemap_index, timeout=15)
        r.raise_for_status()

        soup = BeautifulSoup(r.content, 'xml')
        sitemap_tags = soup.find_all('loc')
        sitemaps = [tag.text for tag in sitemap_tags if tag.text.endswith('.xml')]
        self.stdout.write(f'Found {len(sitemaps)} sitemaps')

        urls = []
        for sm in sitemaps:
            if len(urls) >= limit:
                break
            try:
                rs = requests.get(sm, timeout=15)
                rs.raise_for_status()
            except Exception as e:
                self.stderr.write(f'Failed to fetch sitemap {sm}: {e}')
                continue
            ss = BeautifulSoup(rs.content, 'xml')
            locs = ss.find_all('loc')
            for l in locs:
                urls.append(l.text)
                if len(urls) >= limit:
                    break
            time.sleep(0.2)

        self.stdout.write(f'Will fetch {len(urls)} pages')

        for i, u in enumerate(urls, start=1):
            try:
                self.stdout.write(f'Fetching {u}')
                ru = requests.get(u, timeout=15)
                ru.raise_for_status()
                page = BeautifulSoup(ru.content, 'html.parser')
                title = page.title.string.strip() if page.title else ''
                # heuristics: main content
                article = page.find('article')
                if article:
                    content = article.get_text(separator=' ', strip=True)
                else:
                    # fallback: first large div
                    divs = page.find_all('div')
                    content = ''
                    for d in divs:
                        txt = d.get_text(separator=' ', strip=True)
                        if len(txt) > 200:
                            content = txt
                            break
                # date extraction naive
                date = None
                time_tag = page.find('time')
                if time_tag and time_tag.has_attr('datetime'):
                    date = time_tag['datetime']
                if not date and time_tag:
                    date = time_tag.get_text(strip=True)

                doc = {
                    'url': u,
                    'title': title,
                    'date': date,
                    'content_snippet': content[:500],
                }
                out_file = os.path.join(out, f'sample_{i}.json')
                with open(out_file, 'w', encoding='utf8') as fh:
                    json.dump(doc, fh, ensure_ascii=False, indent=2)
                self.stdout.write(f'Wrote {out_file}')
            except Exception as e:
                self.stderr.write(f'Failed to fetch page {u}: {e}')

        self.stdout.write(self.style.SUCCESS('Done'))
