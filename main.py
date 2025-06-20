import asyncio
import logging
import random
from typing import List
from llm_clients import LLMManager
from twitter_client import TwitterClient
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class JokeBot:
    def __init__(self):
        self.llm_manager = LLMManager()
        self.twitter_client = TwitterClient()
        
        self.joke_prompts = [
            "Tell me a programming joke",
            "Give me a dad joke",
            "Tell me a joke about technology",
            "Share a funny pun",
            "Tell me a clean joke about animals",
            "Give me a joke about artificial intelligence",
            "Tell me a workplace humor joke",
            "Share a joke about the internet",
            "Tell me a science joke",
            "Give me a joke about everyday life"
        ]
    
    async def run_once(self, custom_prompt=None):
        logger.info("Starting joke generation and posting cycle")
        
        if custom_prompt:
            prompt = custom_prompt
        else:
            prompt = random.choice(self.joke_prompts)
        logger.info(f"Using prompt: {prompt}")
        
        jokes = await self.llm_manager.get_jokes(prompt)
        
        if not jokes:
            logger.warning("No jokes generated")
            return
        
        logger.info(f"Generated {len(jokes)} jokes")
        for i, joke in enumerate(jokes):
            logger.info(f"Joke {i+1}: {joke}...")
        
        posted_tweets = await self.twitter_client.post_jokes(jokes)
        
        if posted_tweets:
            logger.info(f"Successfully posted {len(posted_tweets)} tweets")
        else:
            logger.warning("No tweets were posted")
    
    async def run_continuous(self, interval_minutes: int = 60):
        logger.info(f"Starting continuous mode with {interval_minutes} minute intervals")
        
        while True:
            try:
                await self.run_once()
                logger.info(f"Waiting {interval_minutes} minutes until next cycle")
                await asyncio.sleep(interval_minutes * 60)
            except KeyboardInterrupt:
                logger.info("Bot stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in continuous mode: {e}")
                await asyncio.sleep(300)

async def main():
    bot = JokeBot()
    
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        # Read from stdin if available
        stdin_prompt = None
        if not sys.stdin.isatty():
            stdin_prompt = sys.stdin.read().strip()
        
        await bot.run_once(custom_prompt=stdin_prompt)
    else:
        interval = 60
        if len(sys.argv) > 2:
            try:
                interval = int(sys.argv[2])
            except ValueError:
                logger.warning("Invalid interval, using default 60 minutes")
        
        await bot.run_continuous(interval)

if __name__ == "__main__":
    asyncio.run(main())
