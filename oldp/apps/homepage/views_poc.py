# snippet conceptuel (à placer dans oldp/apps/homepage/views_poc.py)
from django.http import JsonResponse
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")
def poc_search_view(request):
    q = request.GET.get("q", "")
    body = {"query": {"match": {"text": q}}} if q else {"query": {"match_all": {}}}
    res = es.search(index="justice_poc", body=body, size=20)
    hits = [h["_source"] for h in res["hits"]["hits"]]
    return JsonResponse({"query": q, "hits": hits})