import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

# Multi-LLM Support
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "grok").lower()

if LLM_PROVIDER == "grok":
    from grok import Grok
    client = Grok(api_key=os.getenv("GROK_API_KEY"))
elif LLM_PROVIDER == "openai":
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
elif LLM_PROVIDER == "claude":
    import anthropic
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
else:
    raise ValueError("Invalid LLM_PROVIDER. Use: grok, openai, or claude")

# Twitter credentials
X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")

auth = tweepy.OAuth1UserHandler(
    X_API_KEY,
    X_API_SECRET,
    os.getenv("X_ACCESS_TOKEN"),
    os.getenv("X_ACCESS_TOKEN_SECRET")
)
api = tweepy.API(auth)

def generate_reply(tweet_text: str) -> str:
    """Generate smart reply using chosen LLM"""
    prompt = f"Write a natural, helpful, and engaging reply to this tweet:\n\n{tweet_text}\n\nReply in under 280 characters:"

    if LLM_PROVIDER == "grok":
        response = client.chat.completions.create(
            model="grok-beta",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    
    elif LLM_PROVIDER == "openai":
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    
    elif LLM_PROVIDER == "claude":
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()

# Simple stream listener (for testing)
class ReplyListener(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        if tweet.referenced_tweets is None:  # only reply to mentions
            reply_text = generate_reply(tweet.text)
            api.update_status(
                status=f"@{tweet.author_id} {reply_text}",
                in_reply_to_status_id=tweet.id
            )
            print(f"Replied to tweet {tweet.id}")

# Run the bot
if __name__ == "__main__":
    print(f"🚀 Smart Twitter Reply Bot running with {LLM_PROVIDER.upper()}...")
    stream = ReplyListener(os.getenv("X_BEARER_TOKEN"))
    stream.filter(track=["@yourbotusername"])  # replace with your bot's @username
