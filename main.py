import os
import signal
import sys
import threading
import time
from dotenv import load_dotenv

from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
from tools import get_time, get_weather, web_search, save_file, list_saved_files, read_saved_file

# Load environment variables from .env file
load_dotenv()


def log_conversation_event(event_type, message):
    """Log conversation events to console."""
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] {event_type}: {message}")


def check_environment_variables():
    """Check if required environment variables are set."""
    agent_id = os.getenv("AGENT_ID")
    api_key = os.getenv("ELEVENLABS_API_KEY")
    
    if not agent_id:
        print("Error: AGENT_ID environment variable is not set.")
        print("Please create a .env file with your AGENT_ID.")
        return False
    
    if not api_key:
        print("Error: ELEVENLABS_API_KEY environment variable is not set.")
        print("Please create a .env file with your ELEVENLABS_API_KEY.")
        return False
    
    return True


def main():
    """Main function to run the conversation."""
    # Check environment variables
    if not check_environment_variables():
        sys.exit(1)
    
    agent_id = os.getenv("AGENT_ID")
    api_key = os.getenv("ELEVENLABS_API_KEY")
    
    try:
        print(f"🔑 Using API key: {api_key[:10]}..." if api_key else "❌ No API key found")
        print(f"🤖 Agent ID: {agent_id}")
        
        elevenlabs = ElevenLabs(api_key=api_key)
        
        conversation = Conversation(
            # API client and agent ID.
            elevenlabs,
            agent_id,

            # Assume auth is required when API_KEY is set.
            requires_auth=bool(api_key),

            # Use the default audio interface.
            audio_interface=DefaultAudioInterface(),
        )
        
        # Test if callbacks are working
        print("✅ Conversation object created successfully")
        print("🔊 Testing audio interface...")

        print("🎤 Starting voice conversation session...")
        print("💡 Speak to interact with the AI assistant!")
        print("📝 Conversation will be displayed below:")
        print("-" * 50)
        
        # Add a test to see if the conversation is working
        print("🔄 Starting conversation...")
        log_conversation_event("INFO", "Starting voice session")
        conversation.start_session()
        print("✅ Session started successfully")
        log_conversation_event("INFO", "Session started successfully")
        
        # Test if we can access conversation properties
        try:
            print(f"🔍 Conversation object type: {type(conversation)}")
            print(f"🔍 Available methods: {[method for method in dir(conversation) if not method.startswith('_')]}")
        except Exception as debug_error:
            print(f"⚠️  Debug info not available: {debug_error}")

        # Handle graceful shutdown
        def signal_handler(sig, frame):
            print("\n🛑 Shutting down gracefully...")
            try:
                conversation.end_session()
            except:
                pass
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        
        # Also handle SIGTERM for better compatibility
        signal.signal(signal.SIGTERM, signal_handler)

        print("⏳ Waiting for conversation to end...")
        print("💬 Note: Conversation text may not appear in console due to API limitations")
        print("🎧 Listen for the AI's voice response and speak when prompted")
        print("🔄 Press Ctrl+C to end the conversation")
        print("⏰ After 5 minutes, you can type 'exit' to manually end the conversation")
        
        # Add periodic status updates and manual exit option
        def status_updater():
            count = 0
            while True:
                time.sleep(30)  # Update every 30 seconds
                count += 1
                log_conversation_event("STATUS", f"Conversation still active - listening for input (run {count})")
                if count >= 10:  # After 5 minutes, offer manual exit
                    print("\n💡 To exit manually, type 'exit' and press Enter:")
                    try:
                        user_input = input().strip().lower()
                        if user_input == 'exit':
                            print("🛑 Manual exit requested...")
                            conversation.end_session()
                            sys.exit(0)
                    except:
                        pass
        
        status_thread = threading.Thread(target=status_updater, daemon=True)
        status_thread.start()
        
        conversation_id = conversation.wait_for_session_end()
        print(f"📋 Conversation ID: {conversation_id}")
        print("🏁 Conversation ended")
        log_conversation_event("INFO", f"Conversation ended with ID: {conversation_id}")
        
        # Try to get conversation history if available
        try:
            print("📖 Attempting to retrieve conversation history...")
            log_conversation_event("INFO", "Checking for conversation history")
            
            # Try to get conversation details from the API
            try:
                # This might work depending on the API version
                conversation_details = elevenlabs.conversational_ai.get_conversation(conversation_id)
                print(f"📋 Conversation details: {conversation_details}")
            except Exception as api_error:
                print(f"⚠️  API method not available: {api_error}")
            
            print("ℹ️  Conversation history retrieval depends on API version")
        except Exception as e:
            print(f"⚠️  Could not retrieve conversation history: {e}")
            log_conversation_event("ERROR", f"Could not retrieve conversation history: {e}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


