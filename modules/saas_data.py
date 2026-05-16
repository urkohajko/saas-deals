import os
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SAAS_LIST_PATH = os.path.join(BASE_DIR, "saas_list.json")
THREAD_DB_PATH = os.path.join(BASE_DIR, "threads_db.json")

# ============================================================
# CARGA DE LISTA DE SAAS
# ============================================================

def load_saas_list():
    if not os.path.exists(SAAS_LIST_PATH):
        raise FileNotFoundError(f"saas_list.json no encontrado en {SAAS_LIST_PATH}")

    with open(SAAS_LIST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

SAAS_LIST = load_saas_list()

# ============================================================
# BASE DE DATOS DE HILOS PUBLICADOS
# ============================================================

def init_saas_system():
    if not os.path.exists(THREAD_DB_PATH):
        with open(THREAD_DB_PATH, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)

def load_thread_db():
    if not os.path.exists(THREAD_DB_PATH):
        return []

    with open(THREAD_DB_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []

def save_thread_db(db):
    with open(THREAD_DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4)

# ============================================================
# REGISTRO DE HILOS
# ============================================================

def add_thread_record(slug, thread_type, tweet_count, url, performance):
    db = load_thread_db()

    entry = {
        "slug": slug,
        "thread_type": thread_type,
        "tweet_count": tweet_count,
        "url": url,
        "performance": performance,
        "timestamp": datetime.utcnow().isoformat()
    }

    db.append(entry)
    save_thread_db(db)

# ============================================================
# CONSULTAS
# ============================================================

def get_last_thread(slug):
    db = load_thread_db()
    filtered = [t for t in db if t["slug"] == slug]
    if not filtered:
        return None
    return filtered[-1]

def get_thread_history(slug):
    db = load_thread_db()
    return [t for t in db if t["slug"] == slug]

def get_global_history():
    return load_thread_db()

def get_saas_by_slug(slug):
    for s in SAAS_LIST:
        if s["slug"] == slug:
            return s
    return None

def get_all_saas():
    return SAAS_LIST
