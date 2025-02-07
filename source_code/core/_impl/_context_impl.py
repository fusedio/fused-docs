from __future__ import annotations

from typing import Dict, Optional


def context_get_user_email() -> str:
    from fused.api.api import FusedAPI

    api = FusedAPI()
    return api._whoami()["email"]


def context_get_auth_header(*, missing_ok: bool = False) -> Dict[str, str]:
    from fused._auth import AUTHORIZATION

    if AUTHORIZATION.is_configured() or not missing_ok:
        return {"Authorization": f"Bearer {AUTHORIZATION.credentials.access_token}"}
    else:
        # Not logged in and that's OK
        return {}


def context_get_auth_scheme_and_token() -> Optional[tuple[str, str]]:
    return None


def context_in_realtime():
    return False


def context_in_batch():
    return False
