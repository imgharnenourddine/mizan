from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.students import router as students_router
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

app.include_router(auth_router, prefix="/api/v1")
app.include_router(students_router, prefix="/api/v1")
@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0", "project": "Mizan — ميزان"}


