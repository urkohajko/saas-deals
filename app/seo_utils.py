import re
from datetime import datetime

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")

def generate_meta_title(deal):
    return f"{deal.title} – Oferta {deal.discount_percent}% | SaaS Deals"

def generate_meta_description(deal):
    return f"{deal.title}: {deal.description}. Precio: ${deal.price}. Descuento: {deal.discount_percent}%. Cupón: {deal.coupon_code or 'N/A'}."

def generate_schema(deal, url):
    return {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": deal.title,
        "description": deal.description,
        "image": deal.image_url,
        "offers": {
            "@type": "Offer",
            "price": str(deal.price),
            "priceCurrency": "USD",
            "url": url,
            "availability": "https://schema.org/InStock",
            "validFrom": datetime.now().isoformat()
        }
    }
