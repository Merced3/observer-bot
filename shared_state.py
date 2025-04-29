# shared_state.py

import os
import json

SEEN_FILE = "seen_sources.json"

current_tasks = []
internet_connected = True

def load_seen_sources():
    if not os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "w") as f:
            json.dump({}, f)

    with open(SEEN_FILE, "r") as f:
        return json.load(f)

def save_seen_source(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(seen, f, indent=4)

def ensure_reddit_memory():
    data = load_seen_sources()
    updated = False

    if "reddit_memory" not in data:
        data["reddit_memory"] = {}
        updated = True

    if "trending_subs" not in data["reddit_memory"]:
        data["reddit_memory"]["trending_subs"] = []
        updated = True

    if "keyword_memory" not in data["reddit_memory"]:
        data["reddit_memory"]["keyword_memory"] = {
            "nouns": {},
            "proper_nouns": {}
        }
        updated = True

    if updated:
        save_seen_source(data)

    return data["reddit_memory"]

def get_reddit_memory():
    return ensure_reddit_memory()

def get_trending_subs():
    return get_reddit_memory()["trending_subs"]

def update_trending_subs(trending):
    data = load_seen_sources()
    data["reddit_memory"]["trending_subs"] = trending
    save_seen_source(data)

def get_keyword_memory():
    return get_reddit_memory()["keyword_memory"]

def update_keyword_memory(nouns, proper_nouns):
    data = load_seen_sources()
    reddit_mem = data.setdefault("reddit_memory", {})
    reddit_mem["keyword_memory"] = {
        "nouns": nouns,
        "proper_nouns": proper_nouns
    }
    save_seen_source(data)