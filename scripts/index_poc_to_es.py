#!/usr/bin/env python3
"""
scripts/index_poc_to_es.py
Indexe les JSON POC présents dans data/justice_gov_ma/ vers Elasticsearch.
Usage:
  .venv/bin/python3 scripts/index_poc_to_es.py --dir data/justice_gov_ma --index justice_poc --es http://localhost:9200
"""
import argparse
import glob
import hashlib
import json
import os
from datetime import datetime

from elasticsearch import Elasticsearch, helpers


def doc_id_from_url(url: str) -> str:
    return hashlib.md5(url.encode("utf-8")).hexdigest()


def load_json_files(path_pattern, limit=0):
    files = sorted(glob.glob(path_pattern))
    if limit and limit > 0:
        files = files[:limit]
    for f in files:
        try:
            with open(f, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            yield f, data
        except Exception as e:
            print(f"skip {f}: {e}")


def to_es_doc(json_obj):
    # Adaptation minimale : map fields we expect (fallbacks)
    title = json_obj.get("title") or json_obj.get("titre") or ""
    text = json_obj.get("content") or json_obj.get("content_snippet") or json_obj.get("text") or ""
    url = json_obj.get("url") or json_obj.get("source_url") or ""
    date = json_obj.get("date")
    # Normalize date if possible
    if date:
        try:
            # Accept basic ISO formats
            parsed = datetime.fromisoformat(date)
            date = parsed.isoformat()
        except Exception:
            date = None
    return {
        "_id": doc_id_from_url(url) if url else None,
        "_source": {
            "title": title,
            "text": text,
            "url": url,
            "date": date,
            "raw": json_obj,
        },
    }


def ensure_index(es, index_name):
    if es.indices.exists(index=index_name):
        print(f"Index {index_name} already exists.")
        return
    mapping = {
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "text": {"type": "text"},
                "url": {"type": "keyword"},
                "date": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
            }
        }
    }
    es.indices.create(index=index_name, body=mapping)
    print(f"Created index {index_name}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dir", default="data/justice_gov_ma", help="Directory with JSON files")
    p.add_argument("--index", default="justice_poc", help="Elasticsearch index name")
    p.add_argument("--es", default="http://localhost:9200", help="Elasticsearch URL")
    p.add_argument("--limit", type=int, default=0, help="Limit number of files (0 = all)")
    p.add_argument("--http_auth", default=None, help="Optional http auth user:pass")
    args = p.parse_args()

    es_kwargs = {}
    if args.http_auth:
        user, pw = args.http_auth.split(":", 1)
        es_kwargs["http_auth"] = (user, pw)
    es = Elasticsearch(args.es, **es_kwargs)

    try:
        es.info()
    except Exception as e:
        print("Cannot connect to Elasticsearch:", e)
        return

    ensure_index(es, args.index)
    pattern = os.path.join(args.dir, "*.json")
    docs = []
    for filename, obj in load_json_files(pattern, limit=args.limit):
        doc = to_es_doc(obj)
        action = {"_index": args.index}
        if doc["_id"]:
            action["_id"] = doc["_id"]
        action["_source"] = doc["_source"]
        docs.append(action)

    if not docs:
        print("No documents to index.")
        return

    print(f"Indexing {len(docs)} documents into {args.index} ...")
    helpers.bulk(es, docs)
    print("Indexing done.")
    # quick count
    res = es.count(index=args.index)
    print("Index contains", res.get("count"))


if __name__ == "__main__":
    main()
