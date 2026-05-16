from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from app.database import engine, create_db_and_tables
from app.models import Deal
from app.seo_utils import slugify, generate_meta_title, generate_meta_description, generate_schema
import json

app = FastAPI()

create_db_and_tables()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def index(request: Request):
    with Session(engine) as session:
        deals = session.exec(select(Deal)).all()
        return templates.TemplateResponse("index.html", {"request": request, "deals": deals})

@app.get("/deal/{deal_id}/{slug}")
def deal_page(request: Request, deal_id: int, slug: str):
    with Session(engine) as session:
        deal = session.exec(select(Deal).where(Deal.id == deal_id)).first()
        if not deal:
            return {"error": "Deal not found"}

        canonical_url = f"https://saasdeals.com/deal/{deal.id}/{slugify(deal.title)}"

        # Obtener otros deals para interlinking
        others = session.exec(select(Deal).where(Deal.id != deal_id)).all()

        return templates.TemplateResponse("deal_page.html", {
            "request": request,
            "deal": deal,
            "others": others,
            "meta_title": generate_meta_title(deal),
            "meta_description": generate_meta_description(deal),
            "schema_json": json.dumps(generate_schema(deal, canonical_url)),
            "canonical_url": canonical_url
        })

@app.get("/click/{deal_id}")
def click_and_redirect(deal_id: int):
    with Session(engine) as session:
        deal = session.exec(select(Deal).where(Deal.id == deal_id)).first()
        if not deal:
            return {"error": "Deal not found"}

        deal.clicks += 1
        session.add(deal)
        session.commit()

        return RedirectResponse(deal.url)

@app.get("/sitemap.xml")
def sitemap():
    with Session(engine) as session:
        deals = session.exec(select(Deal)).all()

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for d in deals:
        slug = slugify(d.title)
        xml += f"""
    <url>
        <loc>https://saasdeals.com/deal/{d.id}/{slug}</loc>
        <changefreq>daily</changefreq>
        <priority>0.8</priority>
    </url>
"""

    xml += "</urlset>"

    return Response(content=xml, media_type="application/xml")
