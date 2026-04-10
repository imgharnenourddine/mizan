# Entry point for the Mizan FastAPI application — configures CORS, routers, and health check

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.institutional import router as institutional_router

app = FastAPI(
    title="Mizan API",
    description="Backend for Mizan - Student Wellbeing AI Platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1")

app.include_router(institutional_router, prefix="/api/v1")

@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok", "version": "1.0.0", "project": "Mizan — ميزان"}
