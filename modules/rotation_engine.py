import random

_last_id = None

def get_next_deal():
    from db import get_all_deals
    global _last_id

    deals = get_all_deals()
    if not deals:
        return None

    filtered = [d for d in deals if d["id"] != _last_id]
    deal = random.choice(filtered)
    _last_id = deal["id"]
    return deal
