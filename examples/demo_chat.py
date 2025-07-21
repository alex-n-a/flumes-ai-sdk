import os, sys

from flumes import MemoryClient, Agent


def main():
    """End-to-end demo talking to the live Flumes API."""

    api_key = os.getenv("FLUMES_API_KEY")
    if not api_key:
        sys.stderr.write("\n⚠️  Please `export FLUMES_API_KEY=sk_...` before running this script.\n")
        sys.exit(1)

    # --------------- Low-level CRUD -----------------
    agent_id = "demo_sales_assistant"
    mc = MemoryClient(api_key=api_key)

    print("Adding a memory …")
    mc.add(
        messages=[{"role": "user", "content": "We will launch on July 31."}],
        agent_id=agent_id,
    )

    print("Searching memories …")
    hits = mc.search(agent_id=agent_id, query="launch")
    print("Search results:", hits)

    # --------------- High-level Agent chat ---------
    # Requires OPENAI_API_KEY (or uses env var if already set)
    agent = Agent(agent_id=agent_id)

    print("Storing agent memory …")
    agent.remember("Our designer's name is Alice.")

    print("Asking agent …")
    reply = agent.chat("Who is our designer?")
    print("Agent replied:", reply)


if __name__ == "__main__":
    main()
