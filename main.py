import os
import tweepy
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Keys from grok-install.yaml
X_API_KEY = os.getenv("X_API_KEY")
GROK_API_KEY = os.getenv("GROK_API_KEY")

# Grok client (xAI)
client = OpenAI(
    api_key=GROK_API_KEY,
    base_url="https://api.x.ai/v1"
)

# Twitter (X) client
auth = tweepy.OAuth1UserHandler(
    consumer_key=os.getenv("X_CONSUMER_KEY", X_API_KEY),
    consumer_secret=os.getenv("X_CONSUMER_SECRET"),
    access_token=os.getenv("X_ACCESS_TOKEN"),
    access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET")
)
api = tweepy.API(auth)

class MyStream(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        if tweet.in_reply_to_user_id is None:  # Only reply to mentions
            try:
                response = client.chat.completions.create(
                    model="grok-beta",
                    messages=[{"role": "user", "content": tweet.text}],
                    temperature=0.7
                )
                reply_text = response.choices[0].message.content[:280]
                api.update_status(status=f"@{tweet.author_id} {reply_text}", in_reply_to_status_id=tweet.id)
                print(f"Replied to tweet {tweet.id}")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    print("Twitter Reply Bot powered by Grok is running...")
    stream = MyStream(bearer_token=os.getenv("X_BEARER_TOKEN"))
    stream.filter(track=["@yourbotusername"])  # Change to your bot's @username
