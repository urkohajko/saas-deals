import os
import time
import json
import random
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRAPER_DB_PATH = os.path.join(BASE_DIR, "scraper_db.json")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")

# ============================================================
# INIT
# ============================================================

def init_scraper_db():
    if not os.path.exists(SCRAPER_DB_PATH):
        with open(SCRAPER_DB_PATH, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4)

    if not os.path.exists(SCREENSHOTS_DIR):
        os.makedirs(SCREENSHOTS_DIR)

def load_scraper_db():
    if not os.path.exists(SCRAPER_DB_PATH):
        return {}
    with open(SCRAPER_DB_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return {}

def save_scraper_db(db):
    with open(SCRAPER_DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4)

# ============================================================
# SCRAPER PRO
# ============================================================

def scrape_saas(url, slug):
    """
    Scraping PRO:
    - Abre la web del SaaS
    - Captura screenshot
    - Extrae texto visible
    - Genera problem/solution/key_points
    - Devuelve SIEMPRE un dict válido
    """

    db = load_scraper_db()

    # ============================
    # 1) Lanzar navegador aislado
    # ============================

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1400,900")
    options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service(os.path.join(BASE_DIR, "chromedriver.exe"))
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        time.sleep(4)

        # ============================
        # 2) Screenshot
        # ============================

        screenshot_path = os.path.join(
            SCREENSHOTS_DIR,
            f"{slug}_{int(time.time())}.png"
        )
        driver.save_screenshot(screenshot_path)

        # ============================
        # 3) Extraer texto visible
        # ============================

        page_text = driver.find_element(By.TAG_NAME, "body").text
        page_text = page_text[:5000]  # límite de seguridad

        # ============================
        # 4) Generar insights
        # ============================

        problem = extract_problem(page_text)
        solution = extract_solution(page_text)
        key_points = extract_key_points(page_text)

        result = {
            "slug": slug,
            "url": url,
            "timestamp": datetime.utcnow().isoformat(),
            "screenshot_path": screenshot_path,
            "problem": problem,
            "solution": solution,
            "key_points": key_points,
        }

        db[slug] = result
        save_scraper_db(db)

        return result

    except Exception as e:
        # fallback seguro
        fallback = {
            "slug": slug,
            "url": url,
            "timestamp": datetime.utcnow().isoformat(),
            "screenshot_path": "",
            "problem": "Helps you work faster and reduce operational friction.",
            "solution": "Provides a cleaner workflow and better execution loops.",
            "key_points": [
                "Removes manual steps.",
                "Improves clarity.",
                "Integrates well with your stack."
            ],
        }
        return fallback

    finally:
        driver.quit()

# ============================================================
# EXTRACTORS
# ============================================================

def extract_problem(text):
    text = text.lower()

    candidates = [
        "problem",
        "pain",
        "struggle",
        "challenge",
        "issue",
        "slow",
        "manual",
        "complex",
        "hard",
        "friction",
    ]

    for c in candidates:
        if c in text:
            return f"This tool solves a real {c} in modern workflows."

    return "This tool removes friction and simplifies your workflow."

def extract_solution(text):
    text = text.lower()

    candidates = [
        "automate",
        "optimize",
        "improve",
        "faster",
        "simplify",
        "streamline",
        "boost",
        "scale",
        "organize",
        "manage",
    ]

    for c in candidates:
        if c in text:
            return f"It helps you {c} your operations with less effort."

    return "It gives you a cleaner, more reliable way to operate."

def extract_key_points(text):
    text = text.lower()

    points = []

    if "ai" in text:
        points.append("AI-powered features that reduce manual work.")
    if "team" in text:
        points.append("Improves team alignment and execution.")
    if "dashboard" in text:
        points.append("Clear dashboards that show what matters.")
    if "automation" in text:
        points.append("Automation that removes repetitive tasks.")
    if "integrations" in text:
        points.append("Integrates smoothly with your existing tools.")

    if not points:
        points = [
            "Removes manual busywork.",
            "Gives you clearer feedback loops.",
            "Fits into your existing workflow."
        ]

    return points
