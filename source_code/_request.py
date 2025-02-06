from __future__ import annotations

from http import HTTPStatus

from requests import HTTPError, Response


def raise_for_status(r: Response):
    """
    A wrapper around Response.raise_for_status to give more information on 422.
    """
    # Look for an error message from model parsing
    if r.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        error_msg = r.json()
        raise HTTPError(error_msg, response=r)

    # Look for a Fused error message
    if 400 <= r.status_code < 600:
        to_raise: Exception | None = None
        try:
            if r.headers["Content-Type"] == "application/json":
                error_msg = r.json()
                if "message" in error_msg:
                    error_msg = error_msg["message"]
                to_raise = HTTPError(error_msg, response=r)
        except:  # noqa: E722
            # Fall through to raise_for_status, below
            pass
        if to_raise is not None:
            raise to_raise

    r.raise_for_status()
