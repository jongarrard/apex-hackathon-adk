"""Entry point for running the multi-tool agent."""

import os
from dotenv import load_dotenv
from .agent import root_agent


def main():
    """Main function to run the agent."""
    # Load environment variables
    load_dotenv()
    
    # Check for required environment variables
    required_vars = ['GOOGLE_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease copy .env.example to .env and fill in your values.")
        return
    
    print("🚀 Multi-Tool Agent Ready!")
    print(f"Agent: {root_agent.name}")
    print(f"Description: {root_agent.description}")
    print("\n📝 How to run your agent:")
    print("  🌐 Web UI:        adk web")
    print("  💬 Terminal chat: adk run multi_tool_agent")
    print("  🚀 FastAPI server: adk api_server")
    print("\n✅ Agent is configured and ready to use!")


if __name__ == "__main__":
    main()
