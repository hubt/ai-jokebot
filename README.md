# AI Joke Bot

A Python bot that queries multiple AI LLMs for jokes and posts them to Twitter.

## Features

- Supports multiple AI providers (OpenAI, Anthropic)
- Automatically posts jokes to Twitter
- Configurable joke prompts
- Continuous or one-time execution modes
- Comprehensive logging

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy the example environment file and configure your API keys:
```bash
cp .env.example .env
```

3. Edit `.env` with your API keys:
   - OpenAI API key (optional)
   - Anthropic API key (optional)
   - Twitter API credentials (required)

## Usage

Run once:
```bash
python main.py --once
```

Run continuously (default 60 minutes interval):
```bash
python main.py
```

Run continuously with custom interval (in minutes):
```bash
python main.py continuous 30
```

## API Keys Required

### Twitter API
- Bearer Token
- Consumer Key & Secret
- Access Token & Secret

### AI Providers (at least one required)
- OpenAI API Key
- Anthropic API Key

## File Structure

- `main.py` - Main bot logic and entry point
- `llm_clients.py` - AI LLM integrations
- `twitter_client.py` - Twitter API integration
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables template