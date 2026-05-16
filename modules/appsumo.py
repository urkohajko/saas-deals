# sources/appsumo.py

import requests
from bs4 import BeautifulSoup
from cleaners import clean_text
from db_saas_deals import search_tools_by_name

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_appsumo(limit=20):
    url = "https://appsumo.com/tools/"
    resp = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, "html.parser")

    cards = soup.select("div.css-1o7z2dq")
    tools = []

    for card in cards[:limit]:
        name_el = card.select_one("h3")
        tagline_el = card.select_one("p")
        link_el = card.select_one("a")
        price_el = card.select_one("span.css-1w6xk0c")

        if not name_el or not link_el:
            continue

        name = clean_text(name_el.text)
        if search_tools_by_name(name):
            continue

        tools.append({
            "name": name,
            "url": "https://appsumo.com" + link_el.get("href"),
            "tagline": clean_text(tagline_el.text if tagline_el else ""),
            "category": "",
            "pricing": clean_text(price_el.text if price_el else ""),
            "features": "",
            "source": "appsumo"
        })

    return tools
