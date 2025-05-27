from fastapi import APIRouter

from app.api.auth.schema import LoginRequest, RefreshTokenRequest, VerifyTokenRequest
from app.api.auth.service import AuthService

router = APIRouter()
auth_service = AuthService()


@router.post("/login")
def login(data: LoginRequest):
    return auth_service.login_user(data)


@router.post("/token/verify")
def verify_token(data: VerifyTokenRequest):
    return auth_service.verify_token(data)


@router.post("/token/refresh")
def refresh_token(data: RefreshTokenRequest):
    return {"TokenRefresh": "Placeholder"}
