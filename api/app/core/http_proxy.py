from fastapi import HTTPException
import httpx

from typing import Optional


def handle_http_request(
    method: str,
    url: str,
    *,
    headers: Optional[dict] = None,
    json: Optional[dict] = None,
    timeout: float = 5.0,
):
    try:
        response = httpx.request(
            method=method, url=url, headers=headers, json=json, timeout=timeout
        )

        response.raise_for_status()
        return response.json()

    except httpx.HTTPStatusError as e:
        try:
            detail = e.response.json().get("detail", e.response.text)
        except Exception:
            detail = e.response.text

        raise HTTPException(status_code=e.response.status_code, detail=detail)

    except httpx.TimeoutException as e:
        raise HTTPException(status_code=408, detail="Request timeout") from e

    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail="Service unavailable") from e
