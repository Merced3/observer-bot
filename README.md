# Observer – News Intelligence Bot for Discord

**Observer** is a custom-built Discord bot that logs real-time news, market headlines, social media signals, and raw intel directly into a private Discord server. The purpose of this system is to build a long-term dataset of market-affecting information for future analysis, machine learning, and autonomous trading logic.

---

## 🚀 Project Goals

- Track headlines and links from manually added sources (websites, RSS feeds, social media, etc.)
- Store news events in Discord with message ID references and attached `.txt` or `.html` files
- Maintain a clean, queryable local archive of all posted data
- Allow dynamic updates to source lists via Discord messages
- Train local LLMs to observe news, link them to price moves, and eventually act as a real-time trading indicator

---

## 🗂️ File Structure

```bash
observer-bot/
├── main.py                        # Core bot logic and startup
├── observer_discord.py             # Bot setup and basic Discord interaction helpers
├── observer_source_watcher.py      # Handles source polling, checking, and posting
├── observer_message_format.py      # Modular formatting system for clean message outputs
├── observer_source_modal.py        # Slash command modal for adding sources via UI
├── observer_fetchers/
│   ├── rss_fetcher.py              # RSS pulling logic
│   ├── fmp_fetcher.py              # Financial Modeling Prep fetcher
│   ├── finnhub_fetcher.py          # Finnhub fetcher
├── .env.example                    # Environment variable example (API keys, bot token)
├── requirements.txt                # Python package list
├── sources.json                    # List of tracked source URLs (dynamic, gitignored)
├── README.md                       # You're reading it!
├── .gitignore                      # Ignore sensitive/configuration files
```

### ℹ️ Recommended: Use a virtual environment (venv) for all Python dependencies:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🧪 Setup Checklist

> ⚠️ Copy `.env.example` → `.env` and fill in your actual token and API keys before running the bot.

### 1️⃣ Bot Setup:
- Add your Discord bot token and IDs to `.env`
- Create a private Discord server and invite the bot
- Ensure bot permissions include sending messages, embedding links, attaching files, and reading message history

### 2️⃣ Adding News/Data Sources:
- Use the `/addsource` slash command inside Discord to register a new source
- Provide URL, Name, and Type (Data/News) via the modal popup
- Observer will begin polling sources and logging live data automatically

---

## 🔒 Git Ignore Notes

The following are excluded from version control:

- `.env` – for secrets and API tokens
- `sources.json` – dynamically updated during runtime
- `venv/` – local Python environment

---

## ⚙️ Future Plans

- Add archiving (Wayback Machine snapshots)
- Summarization via lightweight helper LLMs
- Self-updating source discovery based on past news lead time
- Offline training using local LLMs (Mistral/MythoMax) with sentiment and price correlation
- Real-time Webhook Receivers (Finnhub, MarketAux) for instant low-latency updates

---

## 🧠 Philosophy

This project doesn’t aim to *predict* the market—it aims to **see it more clearly**. News and misinformation move markets, and this system will log everything as it came in—raw and unfiltered—so that future analysis (machine or human) can make sense of it in hindsight and action.
