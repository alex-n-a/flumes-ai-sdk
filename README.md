# Flumes Python SDK

Flumes is the unified memory infrastructure for AI agents.

```bash
# Install the SDK (includes OpenAI client by default)
pip install flumes-ai
```

## Quickstart

```python
from flumes.agent import Agent

agent = Agent(agent_id="sales_assistant")

agent.remember("We're targeting $1 M ARR by Q4.")
print(agent.chat("What's our current goal?"))
```

## Low-level CRUD

```python
from flumes import MemoryClient

mc = MemoryClient()
mc.add(messages=[{"role": "user", "content": "buy milk"}], user_id="u_1")
results = mc.search(user_id="u_1", query="milk")
```

## API keys

| Service | Env var | Example |
|---------|---------|---------|
| Flumes  | `FLUMES_API_KEY` | `export FLUMES_API_KEY=sk_live_...` |
| OpenAI  | `OPENAI_API_KEY` | `export OPENAI_API_KEY=sk-...` |

Pass `api_key="..."` to `MemoryClient` if you prefer not to use environment variables.

---

*Built with ❤️ by the Flumes team – join us on the journey to make agents truly memory-aware.*
