# sources/producthunt.py

import requests
from bs4 import BeautifulSoup
from cleaners import clean_text
from db_saas_deals import search_tools_by_name

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_producthunt(limit=20):
    url = "https://www.producthunt.com/"
    resp = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, "html.parser")

    items = soup.select("div.styles_item__3Y8dW")
    tools = []

    for item in items[:limit]:
        name_el = item.select_one("h3")
        tagline_el = item.select_one("p")
        link_el = item.select_one("a")

        if not name_el or not link_el:
            continue

        name = clean_text(name_el.text)
        if search_tools_by_name(name):
            continue

        tools.append({
            "name": name,
            "url": "https://www.producthunt.com" + link_el.get("href"),
            "tagline": clean_text(tagline_el.text if tagline_el else ""),
            "category": "",
            "pricing": "",
            "features": "",
            "source": "producthunt"
        })

    return tools
