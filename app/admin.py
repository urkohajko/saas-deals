from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlmodel import Session, select
from app.models import Deal
from app.database import engine
from app.auth import is_logged, require_login
import shutil

router = APIRouter(prefix="/admin")

CATEGORIES = [
    "Hosting",
    "SEO",
    "Marketing",
    "IA",
    "Productividad",
    "General"
]


@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return request.app.templates.TemplateResponse(
        "admin/login.html",
        {"request": request}
    )


@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "admin123":
        request.session["logged_in"] = True
        return RedirectResponse("/admin/dashboard", status_code=303)
    return RedirectResponse("/admin/login", status_code=303)


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/admin/login", status_code=303)


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    if not is_logged(request):
        return require_login(request)

    with Session(engine) as session:
        deals = session.exec(select(Deal)).all()

    total_deals = len(deals)
    avg_price = sum([d.price for d in deals]) / total_deals if total_deals > 0 else 0
    last_deals = sorted(deals, key=lambda d: d.created_at, reverse=True)[:5]
    high_discount = [d for d in deals if d.discount_percent and d.discount_percent >= 30]

    return request.app.templates.TemplateResponse(
        "admin/dashboard.html",
        {
            "request": request,
            "total_deals": total_deals,
            "avg_price": avg_price,
            "last_deals": last_deals,
            "high_discount": high_discount
        }
    )


@router.get("/deals", response_class=HTMLResponse)
def deals_list(request: Request):
    if not is_logged(request):
        return require_login(request)

    with Session(engine) as session:
        deals = session.exec(select(Deal)).all()

    return request.app.templates.TemplateResponse(
        "admin/deals_list.html",
        {"request": request, "deals": deals}
    )


@router.get("/deals/new", response_class=HTMLResponse)
def new_deal(request: Request):
    if not is_logged(request):
        return require_login(request)

    return request.app.templates.TemplateResponse(
        "admin/deal_form.html",
        {"request": request, "deal": None, "categories": CATEGORIES}
    )


@router.post("/deals/new")
def create_deal(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    url: str = Form(...),
    category: str = Form(...),
    discount_percent: int = Form(None),
    coupon_code: str = Form(None),
    image: UploadFile = File(None),
):
    if not is_logged(request):
        return require_login(request)

    image_url = None
    if image and image.filename:
        path = f"static/uploads/{image.filename}"
        with open(path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = f"/{path}"

    deal = Deal(
        title=title,
        description=description,
        price=price,
        url=url,
        category=category,
        discount_percent=discount_percent,
        coupon_code=coupon_code,
        image_url=image_url,
    )

    with Session(engine) as session:
        session.add(deal)
        session.commit()

    return RedirectResponse("/admin/deals", status_code=303)


@router.get("/deals/edit/{deal_id}", response_class=HTMLResponse)
def edit_deal(request: Request, deal_id: int):
    if not is_logged(request):
        return require_login(request)

    with Session(engine) as session:
        deal = session.get(Deal, deal_id)

    return request.app.templates.TemplateResponse(
        "admin/deal_form.html",
        {"request": request, "deal": deal, "categories": CATEGORIES}
    )


@router.post("/deals/edit/{deal_id}")
def update_deal(
    request: Request,
    deal_id: int,
    title: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    url: str = Form(...),
    category: str = Form(...),
    discount_percent: int = Form(None),
    coupon_code: str = Form(None),
    image: UploadFile = File(None),
):
    if not is_logged(request):
        return require_login(request)

    with Session(engine) as session:
        deal = session.get(Deal, deal_id)

        deal.title = title
        deal.description = description
        deal.price = price
        deal.url = url
        deal.category = category
        deal.discount_percent = discount_percent
        deal.coupon_code = coupon_code

        if image and image.filename:
            path = f"static/uploads/{image.filename}"
            with open(path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            deal.image_url = f"/{path}"

        session.add(deal)
        session.commit()

    return RedirectResponse("/admin/deals", status_code=303)


@router.get("/deals/delete/{deal_id}")
def delete_deal(request: Request, deal_id: int):
    if not is_logged(request):
        return require_login(request)

    with Session(engine) as session:
        deal = session.get(Deal, deal_id)
        session.delete(deal)
        session.commit()

    return RedirectResponse("/admin/deals", status_code=303)
