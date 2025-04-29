# observer_source_watcher.py

import asyncio
from shared_state import current_tasks
from observer_fetchers import reddit_fetcher
from news_publications_handler import handle_news

DEBUG = False

async def run_safely(name, coro):
    try:
        await coro
    except Exception as e:
        print(f"[Observer] ⚠️ Source '{name}' failed: {e}")

async def concurrent_sources_loop(bot):
    current_tasks.clear() # Clear any leftover tasks
    
    tasks = [
        asyncio.create_task(run_safely("handle_news()", handle_news(bot))),
        asyncio.create_task(run_safely("observe_reddit()", reddit_fetcher.observe_reddit(bot))),
        # (future) asyncio.create_task(observe_twitter(bot)),
        # (future) asyncio.create_task(observe_youtube(bot)),
    ]
    current_tasks.extend(tasks)

    await asyncio.gather(*tasks)
