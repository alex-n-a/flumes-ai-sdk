from __future__ import annotations

from typing import List, Optional, Dict

from flumes.client import MemoryClient
from flumes.models import Message
from flumes.utils.openai_wrapper import LLMBackend, OpenAIBackend
from flumes.logger import emit


class Agent:
    """Opinionated high-level interface for chat with memory support."""

    def __init__(
        self,
        *,
        agent_id: str,
        user_id: Optional[str] = None,
        run_id: Optional[str] = None,
        memory_client: Optional[MemoryClient] = None,
        llm_backend: Optional[LLMBackend] = None,
    ):
        self.agent_id = agent_id
        self.user_id = user_id
        self.run_id = run_id
        self._mem = memory_client or MemoryClient()
        self._llm = llm_backend or OpenAIBackend()

    # --------------------------------------------------------
    # Memory helpers
    # --------------------------------------------------------

    def remember(self, memory: str, *, metadata: Optional[Dict] = None) -> dict:
        """Persist *memory* as an assistant message."""
        return self._mem.add(
            messages=[Message(role="assistant", content=memory)],
            agent_id=self.agent_id,
            user_id=self.user_id,
            run_id=self.run_id,
            metadata=metadata,
            infer=True,
        )

    # --------------------------------------------------------
    # Chat API
    # --------------------------------------------------------

    def chat(self, prompt: str, *, limit: int = 20) -> str:  # noqa: D401
        """Chat with the agent – simple MVP workflow."""
        # 1. Store the user prompt as a memory
        self._mem.add(
            messages=[Message(role="user", content=prompt)],
            agent_id=self.agent_id,
            user_id=self.user_id,
            run_id=self.run_id,
            infer=True,
        )

        # 2. Fetch relevant memories
        mems = self._mem.search(
            agent_id=self.agent_id,
            user_id=self.user_id,
            query=prompt,
            limit=limit,
        )

        # 3. Build LLM context
        mem_items = mems.get("results", mems.get("memories", []))
        context_lines = [m.get("memory", "") for m in mem_items]
        system_msg = (
            "You are an AI assistant equipped with long-term memory. "
            "Relevant stored memories will be provided as context."
        )
        memory_block = "\n".join(f"- {m}" for m in context_lines)

        messages = [
            {"role": "system", "content": system_msg},
            {
                "role": "system",
                "content": (
                    "Relevant memories:\n" + memory_block +
                    "\nWhen answering, rely on these memories if they are pertinent."
                ),
            },
            {"role": "user", "content": prompt},
        ]

        # 4. Call LLM
        emit("llm.called", backend=self._llm.__class__.__name__, prompt=prompt)
        reply = self._llm.complete(messages)

        # 5. Store assistant reply
        self._mem.add(
            messages=[Message(role="assistant", content=reply)],
            agent_id=self.agent_id,
            user_id=self.user_id,
            run_id=self.run_id,
            infer=True,
        )
        return reply
