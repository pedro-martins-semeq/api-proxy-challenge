import httpx
from time import time
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

from src.api_client.schema import LoginRequest, RefreshTokenRequest, VerifyTokenRequest
from src.screens.modals.login_modal import LoginModal
from src.utils import get_exp_from_token

if TYPE_CHECKING:
    from src.app.proxy_tui import ProxyTUI


class APIClient:
    def __init__(self):
        self.__app: "ProxyTUI"
        self._api_url: str = ""
        self._username: str = ""
        self._access_token: str = ""
        self.__access_token_exp: int = 0
        self._refresh_token: str = ""
        self.__refresh_token_exp: int = 0

    @property
    def api_url(self) -> str:
        return self._api_url

    @api_url.setter
    def api_url(self, url: str) -> None:
        self._api_url = url

    @property
    def app(self) -> "ProxyTUI":
        return self.__app

    @app.setter
    def app(self, app: "ProxyTUI") -> None:
        self.__app = app

    @property
    def access_token(self) -> str:
        return self._access_token

    @access_token.setter
    def access_token(self, token: str) -> None:
        self.__access_token_exp = get_exp_from_token(token)
        self._access_token = token

    @property
    def access_token_exp(self) -> int:
        return self.__access_token_exp

    @property
    def refresh_token(self) -> str:
        return self._refresh_token

    @refresh_token.setter
    def refresh_token(self, token: str) -> None:
        self.__refresh_token_exp = get_exp_from_token(token)
        self._refresh_token = token

    @property
    def refresh_token_exp(self) -> int:
        return self.__refresh_token_exp

    @dataclass(frozen=True)
    class Response:
        state: bool
        body: dict

    class APIClientException(Exception):
        def __init__(self, message: str, code: int = 0):
            super().__init__(message)
            self.code = code

    async def _http_proxy(
        self,
        method: str,
        url: str,
        headers: Optional[dict] = None,
        json: Optional[dict] = None,
        timeout: Optional[int] = None,
    ):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method=method, url=url, headers=headers, json=json, timeout=timeout
                )

            response.raise_for_status()
            return self.Response(True, response.json() if response.content else {})

        except httpx.TimeoutException:
            raise self.APIClientException("Timeout error")

        except httpx.RequestError:
            raise self.APIClientException("Network error: Unreachable host")

        except httpx.HTTPStatusError as e:
            return self.Response(
                False,
                {
                    "error": str(e),
                    "status_code": e.response.status_code,
                    "detail": e.response.text,
                },
            )

    async def _verify_token(self, token: str) -> Response:
        response: APIClient.Response = await self._http_proxy(
            method="POST",
            url=f"{self.api_url}/auth/token/verify",
            json=VerifyTokenRequest(token=token).model_dump(),
        )

        return response

    async def _refresh_new_access_token(self, refresh_token) -> Response:
        response: APIClient.Response = await self._http_proxy(
            method="POST",
            url=f"{self.api_url}/auth/token/refresh",
            json=RefreshTokenRequest(refresh=refresh_token).model_dump(),
        )

        return response

    async def validate_credentials(
        self, password: str, username: Optional[str] = None
    ) -> Response:
        if username is not None:
            self._username = username

        payload = LoginRequest(username=self._username, password=password)

        try:
            response = await self._http_proxy(
                method="POST",
                url=f"{self._api_url}/auth/login",
                json=payload.model_dump(),
            )

            if not response.state:
                self._username = ""
                return self.Response(False, response.body)

            self.access_token = response.body["access"]
            self.refresh_token = response.body["refresh"]
            return self.Response(True, {})

        except self.APIClientException as e:
            return self.Response(False, {"error": str(e)})

    def request_connection(self) -> None:
        self.__app.push_screen("connection_screen")

    async def request_login(
        self, label: Optional[str] = None, username: Optional[str] = None
    ) -> None:
        self.__app.install_screen(
            LoginModal(label=label, username=username), name="login_modal"
        )
        await self.__app.push_screen("login_modal")

    async def validate_token_request(self) -> bool:
        timenow = time()
        if self.access_token_exp > timenow:
            access_verify_response: APIClient.Response = await self._verify_token(
                self.access_token
            )
            is_valid_access_token: bool = access_verify_response.state
            if is_valid_access_token:
                return True

        self.app.notify(
            "Trying refresh token...",
            severity="warning",
            title="Expired Access Token",
        )
        if self.refresh_token_exp > timenow:
            refresh_verify_response: APIClient.Response = await self._verify_token(
                self.refresh_token
            )
            is_valid_refresh_token: bool = refresh_verify_response.state
            if is_valid_refresh_token:
                refresh_token_response: APIClient.Response = (
                    await self._refresh_new_access_token(
                        refresh_token=self.refresh_token
                    )
                )
                is_token_refreshed = refresh_token_response.state
                if is_token_refreshed:
                    self.access_token = refresh_token_response.body["access"]
                    self.app.notify(
                        "Access token is refresh",
                        severity="information",
                        title="Access Token Refresh",
                    )
                    return True

                self.app.notify(
                    "Could not refresh access token",
                    severity="warning",
                    title="Login is required",
                )
                await self.request_login("Login Expired", self._username)
                return False

        self.app.notify(
            "Login is required",
            severity="warning",
            title="Session Expired",
        )
        await self.request_login("Login Expired", self._username)
        return False
