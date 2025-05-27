from app.core.config import settings
from app.core.http_proxy import handle_http_request


class UsercorpService:
    RETRIEVE_USERCORP_SERVICE_TIMEOUT: float = 5.0

    def retrieve_usercorp_data(self, token: str):
        headers = {"Authorization": f"Bearer {token}"}

        return handle_http_request(
            method="GET",
            url=f"{settings.external_api_url}/usercorp",
            headers=headers,
            timeout=UsercorpService.RETRIEVE_USERCORP_SERVICE_TIMEOUT,
        )
