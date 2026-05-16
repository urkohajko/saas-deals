from sqlmodel import Session
from datetime import datetime, timedelta
from app.database import engine
from app.models import Deal

IMG = "/static/uploads/placeholder.png"

deals = [
    {"title": "Midjourney", "description": "Generación de imágenes IA.", "price": 10, "url": "https://hostinger.com?utm_source=saasdeals", "category": "IA", "image_url": IMG, "discount_percent": 0, "coupon_code": None, "popularity": 700},
    {"title": "Jasper AI", "description": "Generador de contenido IA.", "price": 39, "url": "https://canva.com?utm_source=saasdeals", "category": "IA", "image_url": IMG, "discount_percent": 25, "coupon_code": "JASPER25", "popularity": 540},
    {"title": "Copy.ai", "description": "Textos automáticos con IA.", "price": 49, "url": "https://brevo.com?utm_source=saasdeals", "category": "IA", "image_url": IMG, "discount_percent": 20, "coupon_code": "COPY20", "popularity": 480},
    {"title": "Rytr", "description": "IA para escribir rápido.", "price": 9, "url": "https://systeme.io?utm_source=saasdeals", "category": "IA", "image_url": IMG, "discount_percent": 10, "coupon_code": "RYTR10", "popularity": 300},
    {"title": "Writesonic", "description": "IA para marketing y blogs.", "price": 16, "url": "https://getresponse.com?utm_source=saasdeals", "category": "IA", "image_url": IMG, "discount_percent": 30, "coupon_code": "WRITE30", "popularity": 420},

    {"title": "Ahrefs", "description": "SEO profesional.", "price": 99, "url": "https://namecheap.com?utm_source=saasdeals", "category": "SEO", "image_url": IMG, "discount_percent": 10, "coupon_code": "AHREFS10", "popularity": 500},
    {"title": "SEMrush", "description": "Suite SEO completa.", "price": 119, "url": "https://pabbly.com?utm_source=saasdeals", "category": "SEO", "image_url": IMG, "discount_percent": 15, "coupon_code": "SEMR15", "popularity": 480},
    {"title": "Surfer SEO", "description": "Optimización de contenido.", "price": 29, "url": "https://surferseo.com?utm_source=saasdeals", "category": "SEO", "image_url": IMG, "discount_percent": 40, "coupon_code": "SURF40", "popularity": 450},
    {"title": "Mangools", "description": "SEO fácil y potente.", "price": 29, "url": "https://mangools.com?utm_source=saasdeals", "category": "SEO", "image_url": IMG, "discount_percent": 35, "coupon_code": "MANGO35", "popularity": 390},
    {"title": "Ubersuggest", "description": "SEO accesible.", "price": 12, "url": "https://neilpatel.com?utm_source=saasdeals", "category": "SEO", "image_url": IMG, "discount_percent": 20, "coupon_code": "UBER20", "popularity": 350},
]

while len(deals) < 50:
    base = deals[len(deals) % len(deals)].copy()
    base["title"] += f" #{len(deals)+1}"
    deals.append(base)

with Session(engine) as session:
    for d in deals:
        deal = Deal(
            **d,
            created_at=datetime.now() - timedelta(days=1)
        )
        session.add(deal)
    session.commit()

print("50 deals insertados correctamente.")
