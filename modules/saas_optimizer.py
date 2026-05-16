import random
import saas_data
import saas_brain
from datetime import datetime, timedelta

# ============================================================
# CONFIGURACIÓN BASE
# ============================================================

DEFAULT_FREQ = 6 * 60 * 60  # 6 horas
MIN_FREQ = 3 * 60 * 60      # 3 horas
MAX_FREQ = 24 * 60 * 60     # 24 horas

TONES = ["simple", "balanced", "expert"]
DEPTHS = ["light", "medium", "high"]

# ============================================================
# FRECUENCIA DINÁMICA
# ============================================================

def compute_frequency(history):
    """
    Ajusta frecuencia según:
    - antigüedad del último hilo
    - rendimiento (si existiera)
    - ruido controlado
    """

    if not history:
        return DEFAULT_FREQ

    last = history[-1]
    ts = datetime.fromisoformat(last["timestamp"])
    hours = (datetime.utcnow() - ts).total_seconds() / 3600

    # Si hace mucho que no se publica → aumentar prioridad
    if hours > 48:
        return MIN_FREQ

    # Si se publicó hace poco → bajar prioridad
    if hours < 12:
        return DEFAULT_FREQ * 1.5

    # Ruido controlado
    noise = random.uniform(0.8, 1.2)
    freq = DEFAULT_FREQ * noise

    return max(MIN_FREQ, min(MAX_FREQ, freq))

# ============================================================
# TONO DINÁMICO
# ============================================================

def compute_tone(history):
    """
    Ajusta tono según:
    - variedad
    - recencia
    """

    if not history:
        return "balanced"

    last = history[-1]["thread_type"]

    if last == "pro":
        # alternar
        return random.choice(["simple", "balanced"])

    return random.choice(TONES)

# ============================================================
# PROFUNDIDAD DINÁMICA
# ============================================================

def compute_depth(history):
    """
    Ajusta profundidad según:
    - variedad
    - recencia
    """

    if not history:
        return "medium"

    last = history[-1]["thread_type"]

    if last == "pro":
        return random.choice(["light", "medium"])

    return random.choice(DEPTHS)

# ============================================================
# OPTIMIZACIÓN GLOBAL DEL SISTEMA
# ============================================================

def optimize_system():
    """
    Devuelve un dict:
    {
        slug: {
            "frequency": X,
            "structure": {
                "tone": "...",
                "depth": "..."
            }
        }
    }
    """

    config = {}
    all_saas = saas_data.get_all_saas()

    for tool in all_saas:
        slug = tool["slug"]
        history = saas_data.get_thread_history(slug)

        freq = compute_frequency(history)
        tone = compute_tone(history)
        depth = compute_depth(history)

        config[slug] = {
            "frequency": freq,
            "structure": {
                "tone": tone,
                "depth": depth
            }
        }

    return config

# ============================================================
# ELECCIÓN DEL SAAS A PUBLICAR
# ============================================================

def optimize_saas_priority():
    """
    Usa el cerebro (saas_brain) para elegir el SaaS.
    """
    return saas_brain.get_next_saas()
