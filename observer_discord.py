# observer_discord.py

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_INTEL_STREAM_CHANNEL_ID"))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Observer is online as {bot.user}!")
    print(f"Connected Guilds: {[guild.name for guild in bot.guilds]}")

async def send_message(content):
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(content)

async def send_file(file_path):
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        with open(file_path, 'rb') as f:
            discord_file = discord.File(f)
            await channel.send(file=discord_file)

async def fetch_message_content(message_id):
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        message = await channel.fetch_message(message_id)
        return message.content
    return None

async def edit_message(message_id, new_content):
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        message = await channel.fetch_message(message_id)
        await message.edit(content=new_content)

def setup_bot():
    return bot
