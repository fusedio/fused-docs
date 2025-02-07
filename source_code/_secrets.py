from typing import Any, Iterable, Iterator, Optional, Union

from fused.core._impl._secret_ops_impl import (
    delete_secret_on_server,
    get_secret_from_server,
    list_secrets_from_server,
    set_secret_on_server,
)


class SecretsManager:
    """Access secrets stored in the Fused backend for the current kernel."""

    _client_id: Optional[str] = None
    """Which instance (kernel) to retrieve and set secrets on."""

    def __init__(self, client_id: Optional[str] = None):
        """ """
        self._client_id = client_id

    def __getattribute__(self, key: str) -> Union[Any, str]:
        try:
            return super().__getattribute__(key)
        except AttributeError:
            try:
                return self[key]
            # Note that we need to raise an AttributeError, **not a KeyError** so that
            # IPython's _repr_html_ works here
            except KeyError:
                raise AttributeError(
                    f"object of type {type(self).__name__} has no attribute {key}"
                ) from None

    def __getitem__(self, key: str) -> str:
        return get_secret_from_server(key=key, client_id=self._client_id)

    def __dir__(self) -> Iterable[str]:
        return list_secrets_from_server(client_id=self._client_id)

    def __iter__(self) -> Iterator[str]:
        for key in dir(self):
            yield key

    def __len__(self) -> int:
        return len(dir(self))

    def __setitem__(self, key: str, value: str):
        return set_secret_on_server(key=key, value=value, client_id=self._client_id)

    def __delitem__(self, key: str):
        return delete_secret_on_server(key=key, client_id=self._client_id)


secrets = SecretsManager()
"""
Access secrets stored in the Fused backend for the current kernel.

Examples:

    Retrieve a secret value:
    ```py
    my_secret_value = fused.secrets["my_secret_key"]
    ```

    or:
    ```py
    my_secret_value = fused.secrets.my_secret_key
    ```

    List all secret keys:
    ```py
    print(dir(fused.secrets))
    ```
"""
