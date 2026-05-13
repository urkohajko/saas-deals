from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import time

app = FastAPI()

# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Datos
DEALS_DATA = [
    {
        "name": "Notion AI",
        "category": "Productividad",
        "description": "Tu segundo cerebro con IA integrada.",
        "tagline": "Ideal para founders que documentan todo.",
        "slug": "notion-ai",
        "clicks": 0,
        "conversions": 0,
        "price": "$9/mes",
        "old_price": "$19",
        "discount": "-53% lifetime deal",
        "badge": "TOP PICK",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/e/e9/Notion-logo.svg",
        "hero": "https://images.unsplash.com/photo-1555066931-4365d14bab8c"
    },
    {
        "name": "Figma Pro",
        "category": "Diseño UI/UX",
        "description": "Diseño colaborativo para equipos serios.",
        "tagline": "Perfecto para sistemas de diseño escalables.",
        "slug": "figma-pro",
        "clicks": 0,
        "conversions": 0,
        "price": "$12/editor",
        "old_price": "$25",
        "discount": "-52% lifetime deal",
        "badge": "TEAM FAVORITE",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/3/33/Figma-logo.svg",
        "hero": "https://images.unsplash.com/photo-1559027615-ce3a9f4d4a2a"
    },
    {
        "name": "Slack Pro",
        "category": "Comunicación",
        "description": "Comunicación estructurada para equipos remotos.",
        "tagline": "Reduce ruido y centraliza decisiones.",
        "slug": "slack-pro",
        "clicks": 0,
        "conversions": 0,
        "price": "$12",
        "old_price": "$25",
        "discount": "-52% lifetime deal",
        "badge": "ESSENTIAL",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/7/76/Slack_Icon.png",
        "hero": "https://images.unsplash.com/photo-1556761175-4b46a572b786"
    }
]

@app.get("/deals", response_class=HTMLResponse)
async def deals_page(request: Request):
    return templates.TemplateResponse(
        "deals.html",
        {
            "request": request,
            "deals": DEALS_DATA,
            "version": int(time.time())  # fuerza recarga del HTML y CSS
        }
    )
