# observer_annotation/load_reddit_posts.py

import os
import json
import asyncio
import asyncpraw
from dotenv import load_dotenv

load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

target_subreddits = [
    "AskReddit", "Home", "pics", "NoStupidQuestions",  # General
    "WallStreetBets", "investing", "stocks",           # Finance
    "technology", "Futurology", "programming",         # Tech
    "memes", "dankmemes",                              # Memes
    "worldnews", "news"                                # News
]

async def get_reddit_posts(limit_per_sub=5, comments_per_post=10):
    
    reddit = asyncpraw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        username=REDDIT_USERNAME,
        password=REDDIT_PASSWORD,
        user_agent=REDDIT_USER_AGENT,
    )

    all_posts = []
    
    for sub in target_subreddits:
        subreddit = await reddit.subreddit(sub)
        async for post in subreddit.hot(limit=limit_per_sub):
            if not post.is_self or post.num_comments < 5:
                continue

            await post.load()
            await post.comments.replace_more(limit=0)
            top_comments = [
                comment.body for comment in post.comments[:comments_per_post]
                if hasattr(comment, 'body')
            ]

            all_posts.append({
                "subreddit": sub,
                "title": post.title,
                "body": post.selftext,
                "comments": top_comments
            })

    # Save to data.json
    with open("observer_annotation/data.json", "w") as f:
        json.dump(all_posts, f, indent=2)

    print(f"✅ Saved {len(all_posts)} Reddit posts to data.json")

if __name__ == "__main__":
    asyncio.run(get_reddit_posts())
