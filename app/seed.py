from sqlmodel import Session
from app.database import engine
from app.models import Deal

def seed():
    with Session(engine) as session:
        if session.query(Deal).count() == 0:
            deal = Deal(
                title="Super Oferta en Hosting Premium",
                description="Plan de hosting SSD ultrarrápido con dominio gratis el primer año, SSL incluido y migración asistida. Ideal para proyectos SaaS o landing pages de alto rendimiento.",
                price=29.99,
                url="https://saasstarter.io/deal-premium",
                image_url="/static/uploads/hosting.jpg",
            )
            session.add(deal)
            session.commit()

if __name__ == "__main__":
    seed()
