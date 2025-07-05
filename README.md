# Personal AI Assistant

A conversational AI assistant using ElevenLabs API for voice interactions.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create environment file:**
   Create a `.env` file in the project root with the following variables:
   ```
   ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
   AGENT_ID=your_agent_id_here
   ```

3. **Get your API credentials:**
   - Sign up at [ElevenLabs](https://elevenlabs.io/) to get your API key
   - Create an agent in the ElevenLabs dashboard to get your Agent ID

## Usage

Run the assistant:
```bash
python main.py
```

The assistant will:
- Start a voice conversation session
- Listen for your voice input
- Respond with voice output
- Support tools like getting time and weather information

## Features

- **Voice Interaction**: Real-time voice conversation
- **Tool Integration**: Built-in tools for time and weather queries
- **Error Handling**: Graceful error handling and shutdown
- **Environment Configuration**: Secure configuration via environment variables

## Tools

The assistant includes the following tools:
- `get_time()`: Returns current date and time
- `get_weather(city)`: Returns weather information for a specified city
- `web_search(query, max_results)`: Performs web search using DuckDuckGo API
- `save_file(content, filename, file_type)`: Saves content to a file in the data directory
- `list_saved_files()`: Lists all saved files with metadata
- `read_saved_file(filename)`: Reads content from a saved file

## Data Storage

The assistant automatically creates a `data/` directory to store saved files. Files are saved with timestamps to avoid conflicts.

## Requirements

- Python 3.7+
- Microphone and speakers for voice interaction
- ElevenLabs API key and Agent ID 