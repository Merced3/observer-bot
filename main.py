# main.py
import os
import json
import asyncio
from dotenv import load_dotenv
from observer_discord import setup_bot
from observer_source_watcher import check_all_sources
from observer_message_format import SourceAdded, SourceAlreadyExists

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
INTEL_STREAM_CHANNEL_ID = int(os.getenv("DISCORD_INTEL_STREAM_CHANNEL_ID"))

bot = setup_bot()

# Sources file path
SOURCES_FILE = "sources.json"

# Ensure sources.json exists
if not os.path.exists(SOURCES_FILE):
    with open(SOURCES_FILE, "w") as f:
        json.dump({"sources": []}, f, indent=4)

async def background_news_loop():
    await bot.wait_until_ready()
    while not bot.is_closed():
        await check_all_sources()
        await asyncio.sleep(60)  # 1 minute for testing, 300 for 5 minutes

@bot.event
async def on_ready():
    print(f"Observer is online as {bot.user}!")
    print(f"Guilds connected: {[guild.name for guild in bot.guilds]}")
    
    # Start the Observer's News loop
    bot.loop.create_task(background_news_loop())

@bot.event
async def on_message(message):
    # Ignore messages from bots (including itself)
    if message.author.bot:
        return

    # Only listen to the specific intel-stream channel
    if message.channel.id != INTEL_STREAM_CHANNEL_ID:
        return

    # Debug: print any message received
    if False: # Set to True to enable debug messages
        print(f"[DEBUG] Received a message: {message.content}")
        print(f"  - From: {message.author} ({message.author.id})")
        print(f"  - In Channel: {message.channel} ({message.channel.id})")

    await bot.process_commands(message)

@bot.command()
async def addsource(ctx, *, args: str):
    """Command to add a new news source URL and optional Name"""

    # Split arguments manually
    parts = args.split(" Name:")
    url = parts[0].strip()

    if len(parts) > 1:
        name = parts[1].strip()
    else:
        name = "Unknown Source"  # fallback if no Name given

    # Auto-fix empty sources.json if needed
    if os.path.getsize(SOURCES_FILE) == 0:
        with open(SOURCES_FILE, "w") as f:
            json.dump({"sources": []}, f, indent=4)

    # Load existing sources
    with open(SOURCES_FILE, "r") as f:
        data = json.load(f)

    # Check if URL already exists
    if any(source["url"] == url for source in data["sources"]):
        await ctx.send(SourceAlreadyExists())
        return

    # Add new source
    data["sources"].append({
        "url": url,
        "name": name,
        "added_by": str(ctx.author),
        "message_id": ctx.message.id
    })

    # Save back to sources.json
    with open(SOURCES_FILE, "w") as f:
        json.dump(data, f, indent=4)

    await ctx.send(SourceAdded())

# Run the bot
if __name__ == "__main__":
    while True:
        try:
            bot.run(TOKEN)
        except Exception as e:
            print(f"Error: {e}")
            break
