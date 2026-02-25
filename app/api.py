from pathlib import Path
from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.counter import Counter
from app.database import DB_PATH
from app.visuals import build_svg


app = FastAPI()
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


def get_db():
    return DB_PATH


@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: str = Depends(get_db)):
    counter = Counter("default", db)
    return templates.TemplateResponse(
        request,
        "index.html",
        {"value": counter.value, "svg": build_svg(counter.value)},
    )


@app.post("/increment", response_class=HTMLResponse)
def increment(request: Request, db: str = Depends(get_db)):
    counter = Counter("default", db)
    counter.increment()
    return templates.TemplateResponse(
        request,
        "counter.html",
        {"value": counter.value, "svg": build_svg(counter.value)},
    )


@app.post("/decrement", response_class=HTMLResponse)
def decrement(request: Request, db: str = Depends(get_db)):
    counter = Counter("default", db)
    try:
        counter.decrement()
        return templates.TemplateResponse(
            request,
            "counter.html",
            {"value": counter.value, "svg": build_svg(counter.value)},
        )
    except ValueError as e:
        return templates.TemplateResponse(
            request,
            "counter.html",
            {
                "value": counter.value,
                "error": str(e),
                "svg": build_svg(counter.value),
            },
        )


@app.post("/reset", response_class=HTMLResponse)
def reset(request: Request, db: str = Depends(get_db)):
    counter = Counter("default", db)
    counter.reset()
    return templates.TemplateResponse(
        request,
        "counter.html",
        {"value": counter.value, "svg": build_svg(counter.value)},
    )
