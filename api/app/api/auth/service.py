import httpx
from fastapi import HTTPException

from app.core.config import settings
from app.api.auth.schema import LoginRequest, VerifyTokenRequest, RefreshTokenRequest


class AuthService:
    def login_user(self, credentials: LoginRequest):
        try:
            response = httpx.request(
                method="POST",
                url=f"{settings.external_api_url}/token",
                json=credentials.model_dump(),
            )

            response.raise_for_status()
            return response.json()

        except Exception as e:
            raise HTTPException(
                status_code=503, detail="Service Unavailable") from e

    def verify_token(self, token: VerifyTokenRequest):
        try:
            response = httpx.request(
                method="POST",
                url=f"{settings.external_api_url}/token/verify",
                json=token.model_dump(),
            )

            response.raise_for_status()
            return response.json()

        except Exception as e:
            raise HTTPException(
                status_code=503, detail="Service Unavailable") from e
