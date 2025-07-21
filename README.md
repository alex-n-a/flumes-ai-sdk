# Flumes AI – Python SDK
![PyPI](https://img.shields.io/pypi/v/flumes-ai?logo=pypi) ![License](https://img.shields.io/github/license/alex-n-a/flumes-ai-sdk)

Flumes AI is a **unified memory infrastructure** for LLM-powered agents and applications. This SDK lets any Python or LangChain stack plug into the [Flumes Memory API](https://docs.flumes.ai/) in **three lines of code**.

👉 Learn more at <https://www.flumes.ai/> – full docs at <https://docs.flumes.ai/>.

---

## 🚀 Installation

```bash
pip install flumes-ai  # includes the OpenAI client by default
```

Python ≥3.8.  No system packages or C-extensions required.

---

## 🔑 Configuration

Environment variables (preferred):

| Service | Variable | Example |
|---------|----------|---------|
| **Flumes** | `FLUMES_API_KEY` | `export FLUMES_API_KEY=sk_live_…` |
| **OpenAI** | `OPENAI_API_KEY` | `export OPENAI_API_KEY=sk-…` |

You can also pass `api_key="…"` directly to `MemoryClient`.

---

## ⚡ Quick-start

```python
from flumes.agent import Agent

agent = Agent(agent_id="sales_assistant")

agent.remember("We're targeting $1 M ARR by Q4.")
print(agent.chat("What's our current goal?"))
```

Behind the scenes Flumes:
1. Adds the fact to long-term memory (summarised + deduplicated).
2. Retrieves relevant memories with semantic search.
3. Injects them into the LLM prompt (OpenAI by default).
4. Stores the assistant response for future context.

---

## 🛠️ Low-level CRUD

```python
from flumes import MemoryClient

mc = MemoryClient(timeout=120)                # 2-minute timeout for cold starts

mc.add(
    messages=[{"role": "user", "content": "Buy milk"}],
    agent_id="shopping_bot"
)

hits = mc.search(agent_id="shopping_bot", query="milk")
print(hits)
```

All endpoints map 1-to-1 with the [REST reference](https://docs.flumes.ai/api-reference/).

---

## ✨ Key features

* **Semantic search** & vector similarity out-of-the-box.
* **Automatic summarisation & deduplication** (`infer=True` by default).
* **Pluggable LLM backend** – OpenAI today, Claude/Mistral coming.
* **Structured logging** – JSON events (`memory.add.request`, `llm.called`) for easy observability.
* **Timeout & retry helpers** – avoid first-call latency issues.

---

## 🗺 Roadmap

* Async transport with `httpx.AsyncClient`
* CLI: `flumes chat`, `flumes memories list`
* Policy plug-ins: custom summariser / retention strategies
* Local in-process transport (`flumes-core`) for offline testing

---

## 🤝 Contributing

1. Fork the repo and create a feature branch.
2. `make install && make test`
3. Open a PR – we ❤️ community help!

Please see [`LICENSE`](LICENSE) (MIT).

---

Made with 🧠 by the Flumes team – join us on the journey to give every agent a memory!
