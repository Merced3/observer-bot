# main.py
import os
import json
import asyncio
from dotenv import load_dotenv
from observer_discord import setup_bot
from observer_source_modal import setup_modals
from observer_source_watcher import check_all_sources
from observer_message_format import SourceRemoved, SourceNameNotFound, SourceListEmpty, SourceList

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
INTEL_STREAM_CHANNEL_ID = int(os.getenv("DISCORD_INTEL_STREAM_CHANNEL_ID"))
APPLICATION_ID = int(os.getenv("DISCORD_APPLICATION_ID"))
bot = setup_bot(application_id=APPLICATION_ID)

# Sources file path
SOURCES_FILE = "sources.json"

# Ensure sources.json exists
if not os.path.exists(SOURCES_FILE):
    with open(SOURCES_FILE, "w") as f:
        json.dump({"sources": []}, f, indent=4)

def has_sources():
    if not os.path.exists(SOURCES_FILE):
        return False

    with open(SOURCES_FILE, "r") as f:
        data = json.load(f)

    return bool(data.get("sources"))


async def background_news_loop():
    await bot.wait_until_ready()
    while not bot.is_closed():
        # Check if sources exist
        if has_sources():
            await check_all_sources(bot)
        else:
            print("[Observer] No sources to check, sleeping...")
        
        await asyncio.sleep(60)

@bot.event
async def on_ready():
    print(f"Observer is online as {bot.user}!")
    print(f"Guilds connected: {[guild.name for guild in bot.guilds]}")
    
    # Setup Modals and Slash Commands AFTER bot is ready
    await setup_modals(bot)

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

@bot.command(name="listsources")
async def list_sources(ctx):
    with open(SOURCES_FILE, "r") as f:
        data = json.load(f)

    if not data["sources"]:
        await ctx.send(SourceListEmpty())
        return

    message = SourceList(data)
    await ctx.send(message)

@bot.command(name="removesource")
async def remove_source(ctx, *, name: str):
    name = name.strip()

    with open(SOURCES_FILE, "r") as f:
        data = json.load(f)

    original_count = len(data["sources"])
    data["sources"] = [src for src in data["sources"] if src.get("name", "").lower() != name.lower()]

    if len(data["sources"]) == original_count:
        await ctx.send(SourceNameNotFound(name))
        return

    with open(SOURCES_FILE, "w") as f:
        json.dump(data, f, indent=4)

    await ctx.send(SourceRemoved())

async def main():
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
