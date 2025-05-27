import httpx
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.app.proxy_tui import ProxyTUI


class APIClient:
    def __init__(self):
        self.__app: "ProxyTUI"
        self._api_url: str = ""
        self._username: str = ""
        self._access_token: str = ""
        self._refresh_token: str = ""

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
        self._access_token = token

    @property
    def refresh_token(self) -> str:
        return self._refresh_token

    @refresh_token.setter
    def refresh_token(self, token: str) -> None:
        self._refresh_token = token

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
