import random
import saas_data
from datetime import datetime, timedelta

# ============================================================
# CARGA DE SAAS
# ============================================================

SAAS_LIST = saas_data.get_all_saas()

# ============================================================
# PRIORIDAD BASE
# ============================================================

def base_priority(tool):
    """
    Prioridad base según categoría y tipo de SaaS.
    Puedes ajustar estos pesos si quieres empujar más categorías.
    """
    category = tool.get("category", "").lower()

    weights = {
        "ai": 1.4,
        "productivity": 1.3,
        "marketing": 1.2,
        "automation": 1.25,
        "analytics": 1.15,
        "devtools": 1.1,
        "sales": 1.2,
        "finance": 1.1,
        "ops": 1.1,
    }

    for key, w in weights.items():
        if key in category:
            return w

    return 1.0

# ============================================================
# PENALIZACIÓN POR RECIENCIA
# ============================================================

def recency_penalty(tool):
    """
    Penaliza SaaS publicados recientemente.
    Evita repeticiones.
    """
    last = saas_data.get_last_thread(tool["slug"])
    if not last:
        return 1.0  # nunca publicado → prioridad máxima

    ts = datetime.fromisoformat(last["timestamp"])
    days = (datetime.utcnow() - ts).days

    if days >= 14:
        return 1.0
    if days >= 7:
        return 0.8
    if days >= 3:
        return 0.5
    return 0.2  # publicado hace poco → muy penalizado

# ============================================================
# SCORE FINAL
# ============================================================

def compute_score(tool):
    """
    Score final = prioridad base * penalización por recencia * ruido controlado
    """
    base = base_priority(tool)
    rec = recency_penalty(tool)
    noise = random.uniform(0.9, 1.1)

    return base * rec * noise

# ============================================================
# ELECCIÓN DEL SAAS
# ============================================================

def choose_saas():
    scored = []

    for tool in SAAS_LIST:
        score = compute_score(tool)
        scored.append((score, tool))

    scored.sort(reverse=True, key=lambda x: x[0])

    # Top 5 candidatos
    top = scored[:5]

    # Selección ponderada
    weights = [s[0] for s in top]
    tools = [s[1] for s in top]

    chosen = random.choices(tools, weights=weights, k=1)[0]
    return chosen

# ============================================================
# API PRINCIPAL
# ============================================================

def get_next_saas():
    """
    API pública del cerebro.
    """
    return choose_saas()
