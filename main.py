# main.py
import os
import json
import aiohttp
import asyncio
import datetime
from dotenv import load_dotenv
from shared_state import current_tasks
from observer_discord import setup_bot
from observer_source_modal import setup_modals
from observer_source_watcher import concurrent_sources_loop
from observer_message_format import SourceRemoved, SourceNameNotFound, SourceListEmpty, SourceList, CommandList

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

async def background_news_loop():
    await bot.wait_until_ready()
    internet_connected = await check_internet()
    
    if internet_connected:
        await concurrent_sources_loop(bot)

    while not bot.is_closed():
        current_status = await check_internet()
        
        if not current_status and internet_connected:
            print(f"[Observer] ❌ Internet disconnected at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")
            
            for task in current_tasks: # Cancel all running tasks
                task.cancel()
            current_tasks.clear()
            
            internet_connected = False
        
        elif current_status and not internet_connected:
            print(f"[Observer] ✅ Internet reconnected at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")
            await concurrent_sources_loop(bot)
            internet_connected = True
        
            
        await asyncio.sleep(1)
    
        
async def check_internet():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.google.com', timeout=5) as resp:
                return resp.status == 200
    except Exception:
        return False

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

@bot.command(name="commands")
async def list_commands(ctx):
    await ctx.send(CommandList())

async def main():
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
