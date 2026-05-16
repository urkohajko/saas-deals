# generator_tweets.py
#
# Generador de tweets automáticos para SaaS Deals
# - Usa la DB real
# - Produce insights, opiniones, preguntas y CTAs
# - Rotación inteligente
# - Listo para enchufar al scheduler

import random
from typing import Dict
from db_saas_deals import get_random_tool


# =========================
# PLANTILLAS
# =========================

INSIGHTS = [
    "The best SaaS tools remove friction, not add features.",
    "A tool that saves 10 hours/month is cheap.",
    "Most teams don’t need more tools. They need better workflows.",
    "Automation is not about speed. It’s about consistency.",
    "SaaS is leverage. Use it or fall behind.",
]

OPINIONES = [
    "Most AI tools are just UI wrappers.",
    "Simplicity beats features every time.",
    "If a tool needs a tutorial, it’s already too complex.",
    "Good SaaS feels invisible.",
    "The best tools don’t replace people. They amplify them.",
]

PREGUNTAS = [
    "What’s one SaaS tool you can’t live without?",
    "What’s the most overrated SaaS tool?",
    "What’s your current SaaS stack?",
    "What’s the last tool you paid for that was worth it?",
    "What SaaS tool saved you the most time?",
]

CTAS = [
    "Daily SaaS tools & exclusive deals. Follow @SaaSDealsHQ.",
    "Discover new tools daily. Zero noise.",
    "Want better tools? Follow @SaaSDealsHQ.",
    "I share the best SaaS tools daily.",
    "Upgrade your stack. Follow @SaaSDealsHQ.",
]


# =========================
# TWEETS BASADOS EN LA DB
# =========================

def tweet_from_tool() -> str:
    """
    Genera un tweet basado en una herramienta real de la DB.
    """
    tool = get_random_tool()
    if not tool:
        return random.choice(INSIGHTS)

    name = tool["name"]
    tagline = tool["tagline"] or ""
    url = tool["url"]

    templates = [
        "🚀 {name}: {tagline}\n{url}",
        "🔥 Herramienta SaaS recomendada: {name}\n{url}",
        "💡 {name} — {tagline}\n{url}",
        "⚡ Si no conoces {name}, estás perdiendo tiempo.\n{url}",
    ]

    return random.choice(templates).format(
        name=name,
        tagline=tagline,
        url=url
    )


# =========================
# ROTACIÓN INTELIGENTE
# =========================

def generar_tweet(ciclo: int) -> str:
    """
    Rotación:
    0 → insight
    1 → pregunta
    2 → opinión
    3 → herramienta real
    4 → insight
    5 → herramienta real
    6 → opinión
    7 → herramienta real
    (y se repite)
    """

    tipo = ciclo % 8

    if tipo == 0:
        return random.choice(INSIGHTS)
    if tipo == 1:
        return random.choice(PREGUNTAS)
    if tipo == 2:
        return random.choice(OPINIONES)
    if tipo == 3:
        return tweet_from_tool()
    if tipo == 4:
        return random.choice(INSIGHTS)
    if tipo == 5:
        return tweet_from_tool()
    if tipo == 6:
        return random.choice(OPINIONES)
    if tipo == 7:
        return tweet_from_tool()

    return random.choice(INSIGHTS)
