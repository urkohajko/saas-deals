# db_saas_deals.py
#
# Módulo de base de datos para SaaS Deals
# - SQLite
# - Tabla: tools
# - Funciones listas para usar desde el bot o el scraper

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

DB_PATH = "saas_deals.db"


# =========================
# CONEXIÓN Y SETUP
# =========================

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tools (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            tagline TEXT,
            category TEXT,
            pricing TEXT,
            features TEXT,
            source TEXT,
            created_at TEXT NOT NULL
        );
        """
    )

    cur.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_tools_created_at
        ON tools (created_at DESC);
        """
    )

    cur.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_tools_name
        ON tools (name);
        """
    )

    conn.commit()
    conn.close()


# =========================
# OPERACIONES BÁSICAS
# =========================

def insert_tool(
    name: str,
    url: str,
    tagline: str = "",
    category: str = "",
    pricing: str = "",
    features: str = "",
    source: str = ""
) -> int:
    """
    Inserta una herramienta y devuelve su ID.
    """
    conn = get_connection()
    cur = conn.cursor()

    created_at = datetime.utcnow().isoformat()

    cur.execute(
        """
        INSERT INTO tools (name, url, tagline, category, pricing, features, source, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """,
        (name, url, tagline, category, pricing, features, source, created_at)
    )

    tool_id = cur.lastrowid
    conn.commit()
    conn.close()
    return tool_id


def insert_tools_bulk(tools: List[Dict]) -> int:
    """
    Inserta múltiples herramientas de una vez.
    Cada dict debe tener al menos: name, url.
    Devuelve cuántas se han insertado.
    """
    if not tools:
        return 0

    conn = get_connection()
    cur = conn.cursor()
    created_at = datetime.utcnow().isoformat()

    rows = []
    for t in tools:
        rows.append((
            t.get("name", "").strip(),
            t.get("url", "").strip(),
            t.get("tagline", "").strip(),
            t.get("category", "").strip(),
            t.get("pricing", "").strip(),
            t.get("features", "").strip(),
            t.get("source", "").strip(),
            created_at
        ))

    cur.executemany(
        """
        INSERT INTO tools (name, url, tagline, category, pricing, features, source, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """,
        rows
    )

    conn.commit()
    count = cur.rowcount
    conn.close()
    return count


# =========================
# LECTURA PARA EL BOT
# =========================

def row_to_dict(row: sqlite3.Row) -> Dict:
    return {
        "id": row["id"],
        "name": row["name"],
        "url": row["url"],
        "tagline": row["tagline"],
        "category": row["category"],
        "pricing": row["pricing"],
        "features": row["features"],
        "source": row["source"],
        "created_at": row["created_at"],
    }


def get_latest_tools(limit: int = 10) -> List[Dict]:
    """
    Devuelve las últimas herramientas insertadas.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM tools
        ORDER BY datetime(created_at) DESC
        LIMIT ?;
        """,
        (limit,)
    )

    rows = cur.fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]


def get_random_tool() -> Optional[Dict]:
    """
    Devuelve una herramienta aleatoria.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM tools
        ORDER BY RANDOM()
        LIMIT 1;
        """
    )

    row = cur.fetchone()
    conn.close()
    if row is None:
        return None
    return row_to_dict(row)


def get_random_tools(limit: int = 5) -> List[Dict]:
    """
    Devuelve varias herramientas aleatorias.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM tools
        ORDER BY RANDOM()
        LIMIT ?;
        """,
        (limit,)
    )

    rows = cur.fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]


def get_tool_by_id(tool_id: int) -> Optional[Dict]:
    """
    Devuelve una herramienta por ID.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM tools
        WHERE id = ?;
        """,
        (tool_id,)
    )

    row = cur.fetchone()
    conn.close()
    if row is None:
        return None
    return row_to_dict(row)


# =========================
# BÚSQUEDA SIMPLE
# =========================

def search_tools_by_name(query: str, limit: int = 20) -> List[Dict]:
    """
    Búsqueda simple por nombre (LIKE).
    """
    conn = get_connection()
    cur = conn.cursor()

    like = f"%{query}%"
    cur.execute(
        """
        SELECT *
        FROM tools
        WHERE name LIKE ?
        ORDER BY datetime(created_at) DESC
        LIMIT ?;
        """,
        (like, limit)
    )

    rows = cur.fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]


def search_tools_by_category(category: str, limit: int = 20) -> List[Dict]:
    """
    Búsqueda simple por categoría exacta.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM tools
        WHERE category = ?
        ORDER BY datetime(created_at) DESC
        LIMIT ?;
        """,
        (category, limit)
    )

    rows = cur.fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]


# =========================
# UTILIDAD
# =========================

def count_tools() -> int:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) AS c FROM tools;")
    row = cur.fetchone()
    conn.close()
    return row["c"] if row else 0


if __name__ == "__main__":
    # Inicializa la DB si no existe
    init_db()
    print(f"DB lista. Total herramientas: {count_tools()}")
