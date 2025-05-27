from app.core.http_proxy import handle_http_request
from app.core.config import settings
from app.api.auth.schema import LoginRequest, VerifyTokenRequest, RefreshTokenRequest


class AuthService:
    LOGIN_SERVICE_TIMEOUT: float = 5.0
    VERIFY_TOKEN_TIMEOUT: float = 5.0
    REFRESH_TOKEN_TIMEOUT: float = 5.0

    def login_user(self, credentials: LoginRequest):
        return handle_http_request(
            method="POST",
            url=f"{settings.external_api_url}/token",
            json=credentials.model_dump(),
            timeout=self.LOGIN_SERVICE_TIMEOUT,
        )

    def verify_token(self, token: VerifyTokenRequest):
        return handle_http_request(
            method="POST",
            url=f"{settings.external_api_url}/token/verify",
            json=token.model_dump(),
            timeout=self.VERIFY_TOKEN_TIMEOUT,
        )

    def refresh_token(self, token: RefreshTokenRequest):
        return handle_http_request(
            method="POST",
            url=f"{settings.external_api_url}/token/refresh",
            json=token.model_dump(),
            timeout=self.REFRESH_TOKEN_TIMEOUT,
        )
