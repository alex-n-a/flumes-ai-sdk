from __future__ import annotations

from typing import Any, Dict, List, Optional

import httpx

from flumes.logger import emit
from flumes.exceptions import AuthenticationError, NotFoundError, RateLimitError, TransportError
from flumes.exceptions import FlumesError

# ---------------------------------------------------------------------------
# Response handling helper
# ---------------------------------------------------------------------------

def _handle_response(resp: httpx.Response) -> dict:  # noqa: D401
    if resp.status_code < 300:
        return resp.json()
    if resp.status_code == 401:
        raise AuthenticationError(resp.text)
    if resp.status_code == 404:
        raise NotFoundError(resp.text)
    if resp.status_code == 429:
        raise RateLimitError(resp.text)
    raise TransportError(f"{resp.status_code}: {resp.text}")


# ---------------------------------------------------------------------------
# Abstract transport class
# ---------------------------------------------------------------------------

class BaseTransport:
    """Abstract transport providing CRUD helpers."""

    def add(self, payload: dict) -> dict:  # noqa: D401
        raise NotImplementedError

    def get(self, memory_id: str) -> dict:  # noqa: D401
        raise NotImplementedError

    def search(self, params: dict) -> dict:  # noqa: D401
        raise NotImplementedError

    def delete(self, memory_id: str) -> dict:  # noqa: D401
        raise NotImplementedError

    def update(self, memory_id: str, payload: dict) -> dict:  # noqa: D401
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Remote HTTP transport
# ---------------------------------------------------------------------------

class RemoteTransport(BaseTransport):
    def __init__(self, base_url: str, api_key: str, timeout: int = 10, *, client: Optional[httpx.Client] = None):
        default_headers = {
            "Authorization": f"Bearer {api_key}"
        }

        self.client = client or httpx.Client(
            base_url=base_url,
            headers=default_headers,
            timeout=timeout,
        )

    # ------------------------ CRUD ------------------------
    def add(self, payload: dict) -> dict:  # noqa: D401
        emit("memory.add.request", **payload)
        resp = self.client.post("/v1/memories/", json=payload)
        data = _handle_response(resp)
        emit("memory.stored", **data)
        return data

    def get(self, memory_id: str) -> dict:  # noqa: D401
        resp = self.client.get(f"/v1/memories/{memory_id}")
        return _handle_response(resp)

    def search(self, params: dict) -> dict:  # noqa: D401
        resp = self.client.get("/v1/memories/", params=params)
        return _handle_response(resp)

    def delete(self, memory_id: str) -> dict:  # noqa: D401
        resp = self.client.delete(f"/v1/memories/{memory_id}")
        return _handle_response(resp)

    def update(self, memory_id: str, payload: dict) -> dict:  # noqa: D401
        resp = self.client.patch(f"/v1/memories/{memory_id}", json=payload)
        return _handle_response(resp)


# ---- LocalTransport has been removed from the public SDK to avoid
# heavy backend dependencies.  Kept here as a private stub so imports
# in legacy code fail clearly.


class LocalTransport(BaseTransport):
    def __init__(self):  # noqa: D401
        raise FlumesError(
            "Local transport is not available in the public SDK. "
            "Clone the Flumes monorepo and run from source if you need in-process mode."
        )

    # Dummy implementations (never reached)
    def add(self, payload: dict) -> dict:  # noqa: D401
        raise NotImplementedError

    def get(self, memory_id: str) -> dict:  # noqa: D401
        raise NotImplementedError

    def search(self, params: dict) -> dict:  # noqa: D401
        raise NotImplementedError

    def delete(self, memory_id: str) -> dict:  # noqa: D401
        raise NotImplementedError

    def update(self, memory_id: str, payload: dict) -> dict:  # noqa: D401
        raise NotImplementedError
