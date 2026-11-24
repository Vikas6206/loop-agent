from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from starlette.requests import Request
import uvicorn

from backend import run_workflow

BASE_DIR = Path(__file__).resolve().parent

## initialize the fast API

app = FastAPI(title = "Self-Correcting Multi-Agent Demo")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


class RunRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=300)


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.post("/api/run")
def run(payload: RunRequest):
    try:
        return run_workflow(payload.topic.strip())
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Workflow failed: {exc}") from exc


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
