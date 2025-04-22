# observer_message_format.py

def format_article_message(article: dict, source_name: str) -> str:
    lines = ["━━━━━━━━━━━━━━━━━━━━"]

    # SOURCE at top
    lines.append(f"**SOURCE:** __{source_name}__")

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

    #lines.append("━━━━━━━━━━━━━━━━━━━━")
    return "\n".join(lines)

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
