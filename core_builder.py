import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool

# 1. Load environment variables
script_dir = Path(__file__).resolve().parent
env_path = script_dir / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Gemini API key not found in environment variables.")

# 2. Initialize the Gemini Model
model = init_chat_model(
    model="gemini-2.5-flash",
    model_provider="google_genai",
    api_key=api_key,
)


from langchain_mcp_adapters.client import MultiServerMCPClient


async def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.join(current_dir, "math_mcp.py")

    client = MultiServerMCPClient(
        {
            "Math": {
                "url": "http://localhost:8000/mcp",
                "transport": "http",
            }
        }
    )

    tools = await client.get_tools()

    print("=" * 55)
    for t in tools:
        print(f"🔧 {t.name}: {t.description[:60]}...")
    print()
    agent = create_agent(model, tools)

    user_prompt = "what is 1 added with 3 and multiplyed with 6"
    result = agent.invoke({"messages": [("user", user_prompt)]})

    final_answer = result["messages"][-1].content
    print("=== FINAL ANSWER ===")
    print(final_answer)

    print("\n" + "=" * 30 + "\n")

    print("=== EXECUTION STEP-BY-STEP ===")
    for msg in result["messages"]:
        if msg.type == "human":
            print(f"\nUser: {msg.content}")
        elif msg.type == "ai":
            if msg.tool_calls:
                for call in msg.tool_calls:
                    print(
                        f"Agent Calling Tool: {call['name']} with args {call['args']}"
                    )
            elif msg.content:
                print(f"Agent Final Response: {msg.content}")
        elif msg.type == "tool":
            print(f"Tool Output ({msg.name}): {msg.content}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())