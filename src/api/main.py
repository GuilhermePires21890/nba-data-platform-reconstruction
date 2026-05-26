from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routers import players

app = FastAPI(
    title="NBA Data Platform API",
    description="REST API for historical NBA player statistics - 1996 to 2021",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(players.router)


@app.get("/")
def root():
    return {
        "name": "NBA Data Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "seasons": "25 seasons — 1996 to 2021",
        "records": 11460,
    }


@app.get("/health")
def health():
    return {"status": "ok"}