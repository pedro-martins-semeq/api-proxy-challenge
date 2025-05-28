import re
import base64
import json
from typing import Optional


def is_valid_url(url: str) -> bool:
    return re.match(r"^https?://[^\s]+$", url) is not None


def get_exp_from_token(token: str) -> int:
    payload = _get_token_payload(token)
    exp = _extract_exp_from_token_payload(payload)

    return 0 if exp is None else exp


def _get_token_payload(token: str) -> dict:
    try:
        payload_b64 = token.split(".")[1]
        padding = "=" * (len(payload_b64) % 4)

        payload_b64 += padding

        payload = base64.urlsafe_b64decode(payload_b64)

        return json.loads(payload)

    except Exception as e:
        raise ValueError("Invalid jwt token format") from e


def _extract_exp_from_token_payload(payload: dict) -> Optional[int]:
    return payload.get("exp", None)

