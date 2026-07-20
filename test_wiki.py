import urllib.request
import urllib.parse
import json

products = [
    "IPhone 16 Pro",
    "Samsung Galaxy S24 Ultra",
    "MacBook Pro",
    "Dell XPS",
    "Apple Watch Series 9",
    "AirPods Pro",
    "PlayStation 5"
]

images = {}

for product in products:
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(product)}&prop=pageimages&format=json&pithumbsize=600"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        data = json.loads(html)
        pages = data.get('query', {}).get('pages', {})
        for page_id, page_data in pages.items():
            if 'thumbnail' in page_data:
                images[product] = page_data['thumbnail']['source']
            else:
                images[product] = "NO_IMAGE"
    except Exception as e:
        images[product] = str(e)

print(json.dumps(images, indent=2))
