# generator_threads.py
#
# Generador de hilos premium para SaaS Deals
# - Usa la DB real
# - Crea hilos de 4–8 tweets
# - Formato profesional
# - Listo para enchufar al bot

from typing import List, Dict
from db_saas_deals import get_random_tool, get_random_tools


# =========================
# PLANTILLAS BASE
# =========================

INTRO_TEMPLATES = [
    "🚀 {name}: {tagline}",
    "🔥 Herramienta SaaS que deberías conocer: {name}",
    "⚡ {name} — {tagline}",
    "💡 Si no conoces {name}, estás perdiendo tiempo.",
]

VALUE_TEMPLATES = [
    "👉 ¿Qué hace?\n{features}",
    "👉 ¿Por qué importa?\n{tagline}",
    "👉 ¿Para quién es?\nIdeal para equipos que necesitan {category}.",
]

BENEFIT_TEMPLATES = [
    "✨ Beneficios clave:\n- Ahorra tiempo\n- Reduce fricción\n- Mejora tu workflow",
    "✨ Lo mejor:\n- Fácil de usar\n- Rápido de implementar\n- Resultados inmediatos",
]

CTA_TEMPLATES = [
    "🔗 Más info: {url}",
    "🔗 Descúbrelo aquí: {url}",
    "🔗 Pruébalo: {url}",
]

OUTRO_TEMPLATES = [
    "Si quieres más herramientas como esta, sigue @SaaSDealsHQ.",
    "Comparto herramientas SaaS cada día. Sígueme para más.",
    "Más herramientas, más productividad. @SaaSDealsHQ.",
]


# =========================
# GENERADOR DE HILOS
# =========================

def generar_hilo() -> List[str]:
    """
    Genera un hilo completo usando una herramienta aleatoria de la DB.
    Devuelve una lista de tweets (partes del hilo).
    """

    tool = get_random_tool()
    if not tool:
        return ["No hay herramientas en la base de datos todavía."]

    name = tool["name"]
    tagline = tool["tagline"] or "SaaS tool worth checking"
    url = tool["url"]
    category = tool["category"] or "productivity"
    features = tool["features"] or "Características no disponibles."

    partes = []

    # INTRO
    intro = random_choice(INTRO_TEMPLATES).format(
        name=name,
        tagline=tagline
    )
    partes.append(intro)

    # VALUE
    value = random_choice(VALUE_TEMPLATES).format(
        tagline=tagline,
        features=features,
        category=category
    )
    partes.append(value)

    # BENEFITS
    partes.append(random_choice(BENEFIT_TEMPLATES))

    # CTA
    cta = random_choice(CTA_TEMPLATES).format(url=url)
    partes.append(cta)

    # OUTRO
    partes.append(random_choice(OUTRO_TEMPLATES))

    return partes


# =========================
# UTILIDAD
# =========================

import random

def random_choice(arr: List[str]) -> str:
    return random.choice(arr)
