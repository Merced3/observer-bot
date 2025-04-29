# observer_message_format.py

# ---NEWS MESSAGE FORMATS---

def format_article_message(article: dict, source_name: str) -> str:
    # SOURCE at top
    lines = [f"**SOURCE:** __{source_name}__"]

    # TITLE
    if "title" in article:
        lines.append(f"📰 **Title:** {article['title']}")

    # LINK
    if "link" in article:
        lines.append(f"> 🔗 **Link:** {article['link']}")

    # DATE
    if "pubdate" in article:
        lines.append(f"> 🕒 **Date:** {article['pubdate']}")

    # DESCRIPTION / SUMMARY
    if "description" in article:
        lines.append(f"> 📝 **Summary:** {article['description']}")

    return "\n".join(lines)

# ---COMMAND MESSAGE FORMATS---

def SourceAlreadyExists():
    return "⚠️ Source already exists."

def SourceAdded():
    return "✅ New source added successfully."

def SourceRemoved():
    return "🗑️ Source removed successfully."

def SourceNameNotFound(name: str):
    return f"⚠️ Source with name '{name}' not found."

def SourceListEmpty():
    return "⚠️ The source list is empty."

def SourceList(data: dict):
    message_lines = ["📚 **Current Sources:**"]
    for source in data["sources"]:
        line = f"- {source.get('name', 'Unnamed')}"
        message_lines.append(line)

    message = "\n".join(message_lines)
    return message

def NoNewArticles():
    return "🔍 No new articles found."

def FetchError(source_url: str):
    return f"⚠️ Failed to fetch articles from: {source_url}"

def CommandList() -> str:
    lines = ["📜 **Observer Command List:**", ""]

    # Slash Commands
    lines.append("🖱️ **Slash Commands (use '/' to trigger):**")
    lines.append("> `/addsource` - Add a new source using a popup modal")
    lines.append("")

    # Bot Commands
    lines.append("⌨️ **Bot Commands (use '!' to trigger):**")
    lines.append("> `!listsources` - List all currently tracked sources")
    lines.append("> `!removesource <name>` - Remove a source by its saved name")
    lines.append("> `!commands` - Show this command list")

    return "\n".join(lines)

# ---REDDIT MESSAGE FORMATS---

def format_trending_subreddits(subreddits: list) -> str:
    lines = ["🌐 **Top Trending Subreddits Today:**\n"]

    for sub in subreddits:
        lines.append(f"• r/{sub}")

    return "\n".join(lines)

def format_reddit_keyword_surges(noun_counts, proper_counts, changes=None) -> str:
    lines = ["📊 **Cultural Radar: Reddit Keyword Surges**\n"]
    #lines = ["📊 Cultural Radar: Reddit Cycle Update (No Major Surges)"]
    #lines = ["📡 Cultural Radar: Major Keyword Surges Spotted!"]
    #lines = ["📡 Cultural Radar: Calm Waters (No Major Surges)"]

    if proper_counts:
        lines.append("🧠 **Proper Nouns:**")
        for word, count in proper_counts[:10]:
            lines.append(f"> • `{word}` — {count}")
        lines.append("")

    if noun_counts:
        lines.append("🗣️ **Nouns:**")
        for word, count in noun_counts[:10]:
            lines.append(f"> • `{word}` — {count}")
        lines.append("")

    if changes:
        up, down = changes.get("up", []), changes.get("down", [])

        if up:
            lines.append("📈 **Surging Terms:**")
            for word, delta in up[:10]:
                lines.append(f"> • `{word}` ↑ {delta}") # Ex. `word` ↑ 5
            lines.append("")

        if down:
            lines.append("📉 **Falling Terms:**")
            for word, delta in down[:10]:
                lines.append(f"> • `{word}` ↓ {delta}") # Ex. `word` ↓ 5
            lines.append("")

    return "\n".join(lines)
