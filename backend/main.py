"""
Yojana.AI - Backend Core
Main entry point for the FastAPI application, handling database initialization,
routing, and static file serving.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response
from backend.routes import eligibility, schemes, pdf, monetization, rejection_predictor, dbt
from backend.database import engine, Base
from backend import db_models
from backend.seed import seed_db
import uvicorn
import os

# Database Initialization
Base.metadata.create_all(bind=engine)
seed_db()

app = FastAPI(
    title="Yojana.AI",
    description="Intelligent Government Scheme Discovery Platform",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# No-cache middleware: forces browsers to always fetch fresh HTML
@app.middleware("http")
async def no_cache_middleware(request: Request, call_next):
    response = await call_next(request)
    if request.url.path.endswith(".html") or request.url.path == "/" or not "." in request.url.path.split("/")[-1]:
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response

# Include Routes
app.include_router(eligibility.router, prefix="/api")
app.include_router(schemes.router, prefix="/api")
app.include_router(pdf.router, prefix="/api")
app.include_router(monetization.router, prefix="/api")
app.include_router(rejection_predictor.router, prefix="/api")
app.include_router(dbt.router, prefix="/api")

# Serve Frontend
frontend_path = os.path.join(os.getcwd(), "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
