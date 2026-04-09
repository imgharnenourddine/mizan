# Entry point for the Mizan FastAPI application — configures CORS, routers, and health check

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Mizan API",
    version="1.0.0",
    description="Mizan — ميزان · L'agent IA de bien-être étudiant",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0", "project": "Mizan — ميزان"}
