import asyncio
import os
from typing import List, Dict, Optional
import openai
from anthropic import Anthropic
import logging

logger = logging.getLogger(__name__)

max_token_output = 4*1024

class LLMClient:
    async def get_joke(self, prompt: str) -> Optional[str]:
        raise NotImplementedError

class OpenAIClient(LLMClient):
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
    
    async def get_joke(self, prompt: str) -> Optional[str]:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a comedian. Generate a single, clean, funny joke."},
                    {"role": "user", "content": prompt}
                ],
                #max_tokens=280,
                max_completion_tokens=max_token_output,
                #temperature=0.9
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return None

class AnthropicClient(LLMClient):
    def __init__(self, api_key: str, model: str = "claude-3-haiku-20240307"):
        self.client = Anthropic(api_key=api_key)
        self.model = model
    
    async def get_joke(self, prompt: str) -> Optional[str]:
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_token_output,
                temperature=0.9,
                system="You are a comedian. Generate a single, clean, funny joke.",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            return None

class LLMManager:
    def __init__(self):
        self.clients: List[LLMClient] = []
        self._setup_clients()
    
    def _setup_clients(self):
        if os.getenv("OPENAI_API_KEY"):
            model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
            self.clients.append(OpenAIClient(os.getenv("OPENAI_API_KEY"), model))
        
        if os.getenv("ANTHROPIC_API_KEY"):
            model = os.getenv("ANTHROPIC_MODEL", "claude-3-haiku-20240307")
            self.clients.append(AnthropicClient(os.getenv("ANTHROPIC_API_KEY"), model))
    
    async def get_jokes(self, prompt: str) -> List[str]:
        if not self.clients:
            logger.warning("No LLM clients configured")
            return []
        
        tasks = [client.get_joke(prompt) for client in self.clients]
        jokes = await asyncio.gather(*tasks, return_exceptions=True)
        
        valid_jokes = []
        for joke in jokes:
            if isinstance(joke, str) and joke:
                valid_jokes.append(joke)
            elif isinstance(joke, Exception):
                logger.error(f"Error getting joke: {joke}")
        
        return valid_jokes
