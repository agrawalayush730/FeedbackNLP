from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app=FastAPI()


templates = Jinja2Templates(directory="templates")


@app.get("/feedback", response_class=HTMLResponse)
def serve_feedback_form(request: Request):
    return templates.TemplateResponse("feedback.html", {"request": request})

@app.get("/", response_class=HTMLResponse)
def serve_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/upload-csv", response_class=HTMLResponse)
def serve_form(request: Request):
    return templates.TemplateResponse("upload_csv.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
def serve_form(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})