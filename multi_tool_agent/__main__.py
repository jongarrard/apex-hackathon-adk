"""Entry point for running the multi-tool agent."""

import asyncio
import os
from dotenv import load_dotenv
from google.genai import types
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from .agent import my_agent


async def call_agent_async(runner, app_name, user_id, session_id, user_query):
    """Send a message to the agent and get the response."""
    # Package the user query into ADK Content format
    content = types.Content(role='user', parts=[types.Part(text=user_query)])
    
    # Call the runner with the user message
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    ):
        # Print intermediate events for debugging (optional)
        if hasattr(event, 'content') and event.content and hasattr(event.content, 'parts'):
            if event.content.parts:
                print(f"🤖 Event: {event.content.parts[0].text}")
        
        # Check if this is the final response
        if event.is_final_response():
            if event.content and event.content.parts:
                return event.content.parts[0].text
            elif event.actions and hasattr(event.actions, 'escalate') and event.actions.escalate:
                return f"Agent escalated: {getattr(event, 'error_message', 'No specific message.')}"
            return "No response"
    
    return "No response received"


async def interactive_chat(runner, app_name, user_id, session_id):
    """Run an interactive chat loop with the agent."""
    print("\n💬 Interactive Chat Started!")
    print("Type 'quit', 'exit', or 'bye' to end the conversation.")
    print("-" * 50)
    
    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                print("\n👋 Goodbye! Thanks for chatting!")
                break
            
            if not user_input:
                continue
            
            # Send message to agent and get response
            print("\n🤖 Agent is thinking...")
            response = await call_agent_async(
                runner, app_name, user_id, session_id, user_input
            )
            
            print(f"\n🤖 {my_agent.name}: {response}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Chat interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again or type 'quit' to exit.")


async def main():
    """Main async function to run the agent."""
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
    
    print("🚀 Starting Multi-Tool Agent...")
    print(f"Agent: {my_agent.name}")
    print(f"Description: {my_agent.description}")
    
    # Setup Session Service
    session_service = InMemorySessionService()
    
    # Define constants for identifying the interaction context
    APP_NAME = "apex_hackathon_app"
    USER_ID = "user_1"
    SESSION_ID = "session_001"
    
    # Create the session
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")
    
    # Setup Runner
    runner = Runner(
        agent=my_agent,
        app_name=APP_NAME,
        session_service=session_service
    )
    print(f"Runner created for agent '{runner.agent.name}'.")
    
    print("✅ Agent setup complete!")
    
    # Start interactive chat
    await interactive_chat(runner, APP_NAME, USER_ID, SESSION_ID)


def run_main():
    """Wrapper to run the async main function."""
    asyncio.run(main())


if __name__ == "__main__":
    run_main()
