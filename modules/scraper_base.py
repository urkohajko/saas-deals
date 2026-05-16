# scraper_base.py
#
# Scraper base para SaaS Deals
# - Descarga HTML
# - Extrae datos
# - Limpia texto
# - Inserta en la DB
# - Evita duplicados
#
# Este archivo es el núcleo del motor de scraping.

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time
import random

from db_saas_deals import insert_tools_bulk, search_tools_by_name


# =========================
# CONFIG
# =========================

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}

TIMEOUT = 12


# =========================
# UTILIDADES
# =========================

def clean_text(text: str) -> str:
    if not text:
        return ""
    return (
        text.replace("\n", " ")
            .replace("\t", " ")
            .strip()
    )


def already_exists(name: str) -> bool:
    """
    Comprueba si una herramienta ya existe en la DB por nombre.
    """
    results = search_tools_by_name(name)
    return len(results) > 0


def fetch_html(url: str) -> BeautifulSoup:
    """
    Descarga HTML y devuelve BeautifulSoup.
    """
    resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


# =========================
# SCRAPER: PRODUCT HUNT (EJEMPLO)
# =========================

def scrape_producthunt(limit: int = 20) -> List[Dict]:
    """
    Scraper simple de Product Hunt (página de hoy).
    Extrae:
    - nombre
    - tagline
    - url
    """
    url = "https://www.producthunt.com/"
    soup = fetch_html(url)

    items = soup.select("div.styles_item__3Y8dW")  # selector estable
    tools = []

    for item in items[:limit]:
        name_el = item.select_one("h3")
        tagline_el = item.select_one("p")
        link_el = item.select_one("a")

        if not name_el or not link_el:
            continue

        name = clean_text(name_el.text)
        tagline = clean_text(tagline_el.text if tagline_el else "")
        url = "https://www.producthunt.com" + link_el.get("href")

        if already_exists(name):
            continue

        tools.append({
            "name": name,
            "url": url,
            "tagline": tagline,
            "category": "",
            "pricing": "",
            "features": "",
            "source": "producthunt"
        })

    return tools


# =========================
# SCRAPER: APPSUMO (EJEMPLO)
# =========================

def scrape_appsumo(limit: int = 20) -> List[Dict]:
    """
    Scraper simple de AppSumo.
    Extrae:
    - nombre
    - tagline
    - url
    - pricing
    """
    url = "https://appsumo.com/tools/"
    soup = fetch_html(url)

    cards = soup.select("div.css-1o7z2dq")  # selector estable
    tools = []

    for card in cards[:limit]:
        name_el = card.select_one("h3")
        tagline_el = card.select_one("p")
        link_el = card.select_one("a")
        price_el = card.select_one("span.css-1w6xk0c")

        if not name_el or not link_el:
            continue

        name = clean_text(name_el.text)
        tagline = clean_text(tagline_el.text if tagline_el else "")
        url = "https://appsumo.com" + link_el.get("href")
        pricing = clean_text(price_el.text if price_el else "")

        if already_exists(name):
            continue

        tools.append({
            "name": name,
            "url": url,
            "tagline": tagline,
            "category": "",
            "pricing": pricing,
            "features": "",
            "source": "appsumo"
        })

    return tools


# =========================
# SCRAPER PRINCIPAL
# =========================

def run_scraper():
    """
    Ejecuta todos los scrapers y guarda en DB.
    """
    print("Scraping Product Hunt…")
    ph_tools = scrape_producthunt(limit=25)
    print(f"PH: {len(ph_tools)} nuevas herramientas")

    time.sleep(random.uniform(1.5, 3.5))

    print("Scraping AppSumo…")
    as_tools = scrape_appsumo(limit=25)
    print(f"AS: {len(as_tools)} nuevas herramientas")

    all_tools = ph_tools + as_tools

    if all_tools:
        inserted = insert_tools_bulk(all_tools)
        print(f"Insertadas en DB: {inserted}")
    else:
        print("No hay herramientas nuevas.")

    print("Scraping completado.")


if __name__ == "__main__":
    run_scraper()
