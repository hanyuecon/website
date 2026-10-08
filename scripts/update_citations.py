"""Fetch citation counts from Google Scholar (via SerpApi) and write citations.json.
Runs weekly from GitHub Actions. Needs the SERPAPI_KEY secret."""
import json, os, re, sys, datetime, urllib.parse, urllib.request

AUTHOR_ID = "G29Zjg8AAAAJ"
KEY = os.environ.get("SERPAPI_KEY", "")
if not KEY:
    sys.exit("SERPAPI_KEY is not set")

def norm(t):
    return re.sub(r"[^a-z0-9]", "", t.lower())

papers, start, data0 = {}, 0, None
while True:
    q = urllib.parse.urlencode({"engine": "google_scholar_author", "author_id": AUTHOR_ID,
                                "num": 100, "start": start, "api_key": KEY})
    with urllib.request.urlopen("https://serpapi.com/search.json?" + q, timeout=60) as r:
        data = json.load(r)
    if "error" in data:
        sys.exit("SerpApi error: " + str(data["error"]))
    data0 = data0 or data
    arts = data.get("articles", [])
    for a in arts:
        n = (a.get("cited_by") or {}).get("value") or 0
        k = norm(a.get("title", ""))
        if k:
            papers[k] = max(n, papers.get(k, 0))
    if len(arts) < 100:
        break
    start += 100

if not papers:
    sys.exit("No articles returned; keeping the existing citations.json")

total = h = None
for row in (data0.get("cited_by") or {}).get("table", []):
    if "citations" in row: total = row["citations"].get("all")
    if "h_index" in row: h = row["h_index"].get("all")

out = {"updated": datetime.date.today().isoformat(), "total": total, "h_index": h, "papers": papers}
with open("citations.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1, sort_keys=True)
print("Wrote", len(papers), "papers; total", total, "h", h)
