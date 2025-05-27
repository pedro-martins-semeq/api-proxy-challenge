from app.core.config import settings
from app.core.http_proxy import handle_http_request


class ImplantationService:
    GET_TREE_BY_ID_SERVICE_TIMEOUT: float = 30.0
    GET_INFO_BY_ID_SERVICE_TIMEOUT: float = 15.0
    GET_STATIC_ASSET_SERVICE_TIMEOUT: float = 5.0
    GET_LUBRICANTS_SERVICE_TIMEOUT: float = 30.0

    def get_tree_by_id(self, id: str, token: str):
        url = f"{settings.external_api_url}/implantation/mobile/tree?site={id}"

        return handle_http_request(
            method="GET",
            url=url,
            headers={"Authorization": f"Bearer {token}"},
            timeout=ImplantationService.GET_TREE_BY_ID_SERVICE_TIMEOUT,
        )

    def get_asset_info_by_id(self, id: str, token: str):
        url = f"{settings.external_api_url}/implantation/mobile/info?site={id}"

        return handle_http_request(
            method="GET",
            url=url,
            headers={"Authorization": f"Bearer {token}"},
            timeout=ImplantationService.GET_INFO_BY_ID_SERVICE_TIMEOUT,
        )

    def get_static_asset(self, token: str):
        url = f"{settings.external_api_url}/implantation/mobile/static"

        return handle_http_request(
            method="GET",
            url=url,
            headers={"Authorization": f"Bearer {token}"},
            timeout=ImplantationService.GET_STATIC_ASSET_SERVICE_TIMEOUT,
        )

    def get_lubricants(self, token: str):
        url = f"{settings.external_api_url}/implantation/mobile/static/get_lubricants"

        return handle_http_request(
            method="GET",
            url=url,
            headers={"Authorization": f"Bearer {token}"},
            timeout=ImplantationService.GET_LUBRICANTS_SERVICE_TIMEOUT,
        )
