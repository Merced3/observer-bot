# observer_fetchers/reddit_fetcher.py

import os
import time
import asyncio
import asyncpraw
from dotenv import load_dotenv
from observer_discord import send_message
from collections import Counter, defaultdict
from observer_fetchers.language_splitter import split_text
from observer_message_format import format_trending_subreddits, format_reddit_keyword_surges
from shared_state import get_trending_subs, update_trending_subs, get_keyword_memory, update_keyword_memory

load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

DEBUG = False  # Set to False in production

reddit = None

async def setup_reddit():
    global reddit
    if reddit is None:
        reddit = asyncpraw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            username=REDDIT_USERNAME,
            password=REDDIT_PASSWORD,
            user_agent=REDDIT_USER_AGENT,
        )

# -------- Fetchers --------

async def fetch_trending_subreddits(bot):
    await setup_reddit()

    while True:
        if DEBUG: print("[Reddit_fetcher] Fetching trending subreddits...")
        
        trending = []
        async for sub in reddit.subreddits.popular(limit=10):
            trending.append(sub.display_name)
        
        last_trending_subs = get_trending_subs()
        if trending != last_trending_subs or not last_trending_subs:
            message = format_trending_subreddits(trending)
            await send_message(bot, message)
            update_trending_subs(trending) # Save to disk too

        await asyncio.sleep(30)  # check again after 30 seconds

async def detect_keyword_surges(bot):
    await setup_reddit()

    while True:
        start_time = time.time()
        if DEBUG: print("\n[Reddit_fetcher] Starting Cultural Shift Radar...")

        global_nouns = []
        global_proper_nouns = []
        good_subreddits = 0
        weak_subreddits = []

        # Define strategic subreddits by category
        target_subreddits = [
            "AskReddit", "Home", "pics", "NoStupidQuestions",  # General
            "WallStreetBets", "investing", "stocks",           # Finance
            "technology", "Futurology", "programming",         # Tech
            "memes", "dankmemes",                              # Memes
            "worldnews", "news"                                # News
        ]

        for sub_name in target_subreddits:
            try:
                subreddit = await reddit.subreddit(sub_name)
                if DEBUG: print(f"🔍 Scanning r/{sub_name}...")

                post_counter = 0
                async for post in subreddit.hot(limit=200):  # Large batch, we'll filter
                    if not post.is_self or post.num_comments < 30:
                        continue

                    text_blocks = [post.title, post.selftext]

                    # Pull top comments Try to add top 5 if available
                    comments = await post.comments()
                    if hasattr(comments, 'list') and comments.list():
                        for top_comment in comments.list()[:5]:
                            if hasattr(top_comment, 'body'):
                                text_blocks.append(top_comment.body)

                    for block in text_blocks:
                        if not block:
                            continue
                        result = split_text(block)
                        global_nouns.extend(result['nouns'])
                        global_proper_nouns.extend(result['proper_nouns'])
                    
                    post_counter += 1
                    if post_counter >= 100:
                        break

                if post_counter >= 90:
                    good_subreddits += 1
                else:
                    weak_subreddits.append(sub_name)

            except Exception as e:
                print(f"⚠️ Skipping r/{sub_name} due to error: {e}")
                continue

        clean_nouns = simple_clean(global_nouns)
        clean_proper_nouns = simple_clean(global_proper_nouns)
        
        noun_counts = Counter(clean_nouns).most_common(30)
        proper_counts = Counter(clean_proper_nouns).most_common(30)

        keyword_memory = get_keyword_memory()
        previous_noun_counts = keyword_memory.get("nouns", {})
        previous_proper_counts = keyword_memory.get("proper_nouns", {})

        # After `noun_counts`` and `proper_counts`; Compare deltas
        noun_deltas = compare_deltas(noun_counts, previous_noun_counts)
        proper_deltas = compare_deltas(proper_counts, previous_proper_counts)

        # Determine if anything changed
        any_changes = noun_deltas["up"] or noun_deltas["down"] or proper_deltas["up"] or proper_deltas["down"]

        # Send appropriate message
        if any_changes:
            changes = {
                "up": noun_deltas["up"] + proper_deltas["up"],
                "down": noun_deltas["down"] + proper_deltas["down"]
            }
            message = format_reddit_keyword_surges(noun_counts, proper_counts, changes=changes)
            await send_message(bot, message)

            update_keyword_memory( # Only update memory if something really changed
                nouns=dict(Counter(clean_nouns)),
                proper_nouns=dict(Counter(clean_proper_nouns))
            )
        else:
            if DEBUG:
                print("[Reddit_fetcher] No major cultural shift detected. Skipping message send.")

        # End timer
        end_time = time.time()
        elapsed = end_time - start_time
        minutes, seconds = divmod(int(elapsed), 60)

        if DEBUG:
            print(f"[Reddit_fetcher] ✅ Finished scanning in {minutes} min {seconds} sec.")
            print(f"[Reddit_fetcher] Good subs: {good_subreddits}, Weak subs: {weak_subreddits}")
        await asyncio.sleep(3 * 60 * 60) # 3 hours in seconds

# -------- Helper Functions --------

def simple_clean(words):
    cleaned = []
    for word in words:
        if word.isalpha() and len(word) > 2:  # Only real alphabetic words, at least 3 letters
            cleaned.append(word)
    return cleaned

def compare_deltas(current_counts, previous_counts, threshold=10):
    """
    Compare current word counts to previous ones and return significant changes.
    """
    up = []
    down = []
    current_dict = dict(current_counts)

    all_keys = set(current_dict) | set(previous_counts)

    for word in all_keys:
        current = current_dict.get(word, 0)
        previous = previous_counts.get(word, 0)
        delta = current - previous

        if abs(delta) >= threshold:
            if delta > 0:
                up.append((word, delta))
            else:
                down.append((word, abs(delta)))

    # Sort from largest change to smallest
    return {
        "up": sorted(up, key=lambda x: x[1], reverse=True),
        "down": sorted(down, key=lambda x: x[1], reverse=True),
    }

# -------- Master Orchestrator --------

async def observe_reddit(bot):
    # Run both tasks concurrently
    await asyncio.gather(
        fetch_trending_subreddits(bot),   # loops every 30 second
        detect_keyword_surges(bot)        # Loops every 3 hours internally
    )