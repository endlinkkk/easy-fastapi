from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from src.microblog_api.router import router as microblog_router
from src.database import create_db, check_content, add_fake_user
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from loguru import logger
import uvicorn
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Start lifespan")
    create_db()
    if not check_content():
        add_fake_user()
    yield


app = FastAPI(title="microBlog", lifespan=lifespan)


@app.get("/status", include_in_schema=False)
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.exception_handler(HTTPException)
def error_handler(request: Request, exc: HTTPException):
    error_message = {
        "result": False,
        "error_type": type(exc).__name__,
        "error_message": str(exc),
    }
    return JSONResponse(status_code=500, content=error_message)


app.include_router(microblog_router, prefix="/api")
