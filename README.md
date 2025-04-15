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
├── main.py              # Core bot logic
├── .env                 # Environment variables (bot token, secrets) – excluded from git
├── sources.json         # List of tracked source URLs or accounts – excluded from git
├── .gitignore           # Ignore .env, sources.json, venv, etc.
├── README.md            # You're reading it!
```

## ℹ️ Recommended: Use a virtual environment (venv) for all Python dependencies:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🧪 Setup Checklist

> ⚠️ Copy `.env.example` → `.env` and fill in your actual token and IDs before running the bot.

1. Add your Discord bot token and other variables to `.env`
2. Create a private Discord server and invite the bot
3. Add source URLs using `!addsource` command in a designated channel
4. Observer will begin polling, logging, and storing relevant data automatically

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

---

## 🧠 Philosophy

This project doesn’t aim to *predict* the market—it aims to **see it more clearly**. News and misinformation move markets, and this system will log everything as it came in—raw and unfiltered—so that future analysis (machine or human) can make sense of it in hindsight and action.
