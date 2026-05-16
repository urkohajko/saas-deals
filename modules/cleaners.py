# cleaners.py
#
# Limpieza y normalización de texto para SaaS Deals

def clean_text(text: str) -> str:
    if not text:
        return ""
    return (
        text.replace("\n", " ")
            .replace("\t", " ")
            .replace("\r", " ")
            .strip()
    )


def clean_price(text: str) -> str:
    if not text:
        return ""
    t = text.lower().strip()
    t = t.replace("usd", "").replace("$", "").strip()
    return t
