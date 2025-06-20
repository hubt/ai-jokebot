import tweepy
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class TwitterClient:
    def __init__(self):
        self.api = None
        self._setup_client()
    
    def _setup_client(self):
        try:
            bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
            consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
            consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
            access_token = os.getenv("TWITTER_ACCESS_TOKEN")
            access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
            
            if not all([bearer_token, consumer_key, consumer_secret, access_token, access_token_secret]):
                logger.error("Missing Twitter API credentials")
                return
            
            self.client = tweepy.Client(
                bearer_token=bearer_token,
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
                wait_on_rate_limit=True
            )
            
            logger.info("Twitter client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Twitter client: {e}")
    
    async def post_tweet(self, text: str) -> Optional[str]:
        if not self.client:
            logger.error("Twitter client not initialized")
            return None
        
        if len(text) > 280:
            text = text[:277] + "..."
        
        if True:
            return None

        try:
            response = self.client.create_tweet(text=text)
            tweet_id = response.data['id']
            logger.info(f"Tweet posted successfully: {tweet_id}")
            return tweet_id
        except Exception as e:
            logger.error(f"Failed to post tweet: {e}")
            return None
    
    async def post_jokes(self, jokes: list) -> list:
        posted_tweets = []
        
        for i, joke in enumerate(jokes):
            if not joke:
                continue
                
            tweet_text = f"🤖 AI Joke #{i+1}:\n\n{joke}"
            tweet_id = await self.post_tweet(tweet_text)
            
            if tweet_id:
                posted_tweets.append({
                    "id": tweet_id,
                    "text": tweet_text,
                    "joke": joke
                })
        
        return posted_tweets
