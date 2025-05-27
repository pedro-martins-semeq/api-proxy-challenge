from fastapi import APIRouter

from app.api.auth.schema import LoginRequest, RefreshTokenRequest, VerifyTokenRequest


router = APIRouter()


@router.post("/login")
def login(data: LoginRequest):
    return {"Login": "Placeholder"}


@router.post("/token/verify")
def verify_token(data: VerifyTokenRequest):
    return {"TokenVerify": "Placeholder"}


@router.post("/token/refresh")
def refresh_token(data: RefreshTokenRequest):
    return {"TokenRefresh": "Placeholder"}
