from typing import Optional


def get_secret_from_server(key: str, client_id: Optional[str] = None):
    from fused.api.api import FusedAPI

    api = FusedAPI()
    return api.get_secret_value(key=key, client_id=client_id)


def list_secrets_from_server(client_id: Optional[str] = None):
    from fused.api.api import FusedAPI

    api = FusedAPI()
    return api.list_secrets(client_id=client_id)


def set_secret_on_server(key: str, value: str, client_id: Optional[str] = None):
    from fused.api.api import FusedAPI

    api = FusedAPI()
    return api.set_secret_value(key=key, value=value, client_id=client_id)


def delete_secret_on_server(key: str, client_id: Optional[str] = None):
    from fused.api.api import FusedAPI

    api = FusedAPI()
    return api.delete_secret_value(key=key, client_id=client_id)
