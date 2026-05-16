from sqlmodel import Session
from app.database import engine
from app.models import Deal

deals = [
    {
        "title": "Hosting Turbo Pro",
        "description": "Hosting ultrarrápido con CDN global y SSL incluido.",
        "price": 29.99,
        "url": "https://example.com/hosting",
        "category": "Hosting",
        "image_url": "/static/uploads/hosting.jpg"
    },
    {
        "title": "SEO Booster 3000",
        "description": "Herramienta SEO con auditorías automáticas y análisis de keywords.",
        "price": 19.00,
        "url": "https://example.com/seo",
        "category": "SEO",
        "image_url": "/static/uploads/hosting.jpg"
    },
    {
        "title": "AI Writer Pro",
        "description": "Generador de contenido con IA para blogs, emails y redes sociales.",
        "price": 12.50,
        "url": "https://example.com/ai",
        "category": "IA",
        "image_url": "/static/uploads/hosting.jpg"
    },
    {
        "title": "Marketing Suite X",
        "description": "Automatización de marketing con funnels, emails y analíticas.",
        "price": 49.00,
        "url": "https://example.com/marketing",
        "category": "Marketing",
        "image_url": "/static/uploads/hosting.jpg"
    },
    {
        "title": "Productividad Max",
        "description": "Suite de productividad con notas, tareas y calendario inteligente.",
        "price": 9.99,
        "url": "https://example.com/productividad",
        "category": "Productividad",
        "image_url": "/static/uploads/hosting.jpg"
    }
]

with Session(engine) as session:
    for d in deals:
        deal = Deal(**d)
        session.add(deal)
    session.commit()

print("5 deals insertados correctamente.")
