from __future__ import annotations

import os
from typing import List, Optional

from flumes.models import Message, AddMemoryRequest, UpdateMemoryRequest
from flumes.transport import RemoteTransport, LocalTransport, BaseTransport
from flumes.exceptions import FlumesError
from flumes.logger import emit


class MemoryClient:
    """Synchronous Memory CRUD client (MVP)."""

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: str = "https://api.flumes.ai",
        timeout: int = 120,
        local: bool = False,  # deprecated
    ):
        if local:
            raise FlumesError("local=True is not supported in the public SDK distribution.")
        else:
            key = api_key or os.getenv("FLUMES_API_KEY")
            if not key:
                raise FlumesError("API key missing; set FLUMES_API_KEY or pass api_key=")
            self._transport = RemoteTransport(base_url, key, timeout=timeout)

    # ------------------------------------------------------------------
    # Public API (mirrors endpoints)
    # ------------------------------------------------------------------

    def add(
        self,
        messages: List[Message],
        *,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        run_id: Optional[str] = None,
        metadata: Optional[dict] = None,
        infer: bool = True,
    ) -> dict:
        payload = AddMemoryRequest(
            messages=messages,
            user_id=user_id,
            agent_id=agent_id,
            run_id=run_id,
            metadata=metadata,
            infer=infer,
        ).model_dump(mode="json")
        return self._transport.add(payload)

    def get(self, memory_id: str) -> dict:
        return self._transport.get(memory_id)

    def search(
        self,
        *,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        query: Optional[str] = None,
        limit: int = 20,
    ) -> dict:
        if not any([user_id, agent_id]):
            raise ValueError("One of user_id or agent_id is required for search")
        params = {
            "user_id": user_id,
            "agent_id": agent_id,
            "query": query,
            "limit": limit,
        }
        return self._transport.search(params)

    def delete(self, memory_id: str) -> dict:
        return self._transport.delete(memory_id)

    def update(self, memory_id: str, *, memory: str, metadata: Optional[dict] = None) -> dict:
        payload = UpdateMemoryRequest(memory=memory, metadata=metadata).model_dump(mode="json")
        return self._transport.update(memory_id, payload)
