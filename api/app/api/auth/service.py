from app.core.http_proxy import handle_http_request
from app.core.config import settings
from app.api.auth.schema import LoginRequest, VerifyTokenRequest, RefreshTokenRequest


class AuthService:
    def login_user(self, credentials: LoginRequest):
        return handle_http_request(
            method="POST",
            url=f"{settings.external_api_url}/token",
            json=credentials.model_dump(),
        )

    def verify_token(self, token: VerifyTokenRequest):
        return handle_http_request(
            method="POST",
            url=f"{settings.external_api_url}/token/verify",
            json=token.model_dump(),
        )

    def refresh_token(self, token: RefreshTokenRequest):
        return handle_http_request(
            method="POST",
            url=f"{settings.external_api_url}/token/refresh",
            json=token.model_dump(),
        )
