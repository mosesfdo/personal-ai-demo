# Personal AI Agent Project

This project was created to understand how AI agents work using the ElevenLabs SDK. The code is based on the ElevenLabs conversational AI SDK examples.

## Purpose

This project serves as a learning tool to explore:
- How AI agents function in real-time conversations
- Voice interaction with AI assistants
- Integration with ElevenLabs API
- Real-time audio processing and response

## Features

- Real-time voice conversation with AI agent
- Weather information retrieval
- Web search capabilities
- File management (save, list, read files)
- Time and date information
- Graceful session management

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   Create a `.env` file in the root directory with:
   ```
   ELEVENLABS_API_KEY=your_api_key_here
   AGENT_ID=your_agent_id_here
   ```

3. **Run the Application**
   ```bash
   python main.py
   ```

## Usage

- Speak to interact with the AI assistant
- The conversation will be displayed in the console
- Press Ctrl+C to end the conversation gracefully
- After 5 minutes, you can type 'exit' to manually end the session

## Requirements

- Python 3.7+
- ElevenLabs API key
- Agent ID from ElevenLabs
- Microphone for voice input
- Speakers for voice output

## Code Structure

- `main.py` - Main application entry point
- `tools.py` - Custom tools and functions for the AI agent
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (not tracked in git)

## Notes

- This is a learning project based on ElevenLabs SDK examples
- The conversation text may not appear in console due to API limitations
- Listen for the AI's voice response and speak when prompted
- The project includes error handling and graceful shutdown capabilities 