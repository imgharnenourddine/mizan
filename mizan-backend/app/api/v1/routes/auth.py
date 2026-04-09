# app/api/v1/routes/auth.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.auth import (
    LoginSchema,
    RefreshTokenSchema,
    RequestActivationSchema,
    SetPasswordSchema,
    TokenResponse,
    VerifyOtpSchema,
)
from app.services.auth_service import (
    login,
    refresh_access_token,
    request_activation,
    set_password,
    verify_otp,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/request-activation")
async def handle_request_activation(
    payload: RequestActivationSchema, db: AsyncSession = Depends(get_db)
):
    await request_activation(db, payload.email)
    return {"message": "OTP sent to your email"}


@router.post("/verify-otp")
async def handle_verify_otp(
    payload: VerifyOtpSchema, db: AsyncSession = Depends(get_db)
):
    token = await verify_otp(db, payload.email, payload.otp)
    return {"temp_token": token}


@router.post("/set-password", response_model=TokenResponse)
async def handle_set_password(
    payload: SetPasswordSchema, db: AsyncSession = Depends(get_db)
):
    return await set_password(db, payload.token, payload.new_password)


@router.post("/login", response_model=TokenResponse)
async def handle_login(
    payload: LoginSchema, db: AsyncSession = Depends(get_db)
):
    return await login(db, payload.email, payload.password)


@router.post("/refresh")
async def handle_refresh(
    payload: RefreshTokenSchema, db: AsyncSession = Depends(get_db)
):
    token = await refresh_access_token(db, payload.refresh_token)
    return {"access_token": token, "token_type": "bearer"}