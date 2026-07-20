import urllib.request
import urllib.parse
import re
import json

queries = [
    "Apple iPhone 16 Pro Max amazon.in",
    "Apple iPhone 16 Pro amazon.in",
    "Apple iPhone 16 Plus amazon.in",
    "Samsung Galaxy S24 Ultra amazon.in",
    "Google Pixel 8 Pro amazon.in",
    "OnePlus 12 amazon.in",
    "Apple MacBook Air M3 amazon.in",
    "Apple MacBook Pro 14-inch M3 amazon.in",
    "Dell XPS 13 amazon.in",
    "HP Spectre x360 amazon.in",
    "Lenovo ThinkPad X1 Carbon amazon.in",
    "ASUS ROG Zephyrus G16 amazon.in",
    "Apple Watch Series 9 amazon.in",
    "Samsung Galaxy Watch 6 amazon.in",
    "Apple AirPods Pro 2nd Gen amazon.in",
    "Sony WH-1000XM5 amazon.in",
    "Nike Air Force 1 amazon.in",
    "Adidas Ultraboost amazon.in"
]

results = {}

for query in queries:
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query + ' images.unsplash.com OR m.media-amazon.com')}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        # Find first m.media-amazon.com or images.unsplash.com url ending in jpg
        match = re.search(r'(https://[a-zA-Z0-9\-\.]+(?:amazon|unsplash)\.com/[^"\']+\.jpg)', html)
        if match:
            results[query] = match.group(1)
        else:
            results[query] = "NOT_FOUND"
    except Exception as e:
        results[query] = str(e)

print(json.dumps(results, indent=2))
