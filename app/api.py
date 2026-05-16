from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from app.database import engine
from app.models import Deal, Favorite

api = APIRouter(prefix="/api", tags=["api"])


@api.get("/deals")
def api_deals(category: str | None = None):
    with Session(engine) as session:
        query = select(Deal)
        if category:
            query = query.where(Deal.category == category)
        deals = session.exec(query).all()
    return deals


@api.post("/deals/{deal_id}/like")
def api_like_deal(deal_id: int):
    with Session(engine) as session:
        deal = session.get(Deal, deal_id)
        if not deal:
            raise HTTPException(status_code=404, detail="Deal not found")
        deal.popularity += 1
        session.add(deal)
        session.commit()
    return {"status": "ok", "popularity": deal.popularity}
