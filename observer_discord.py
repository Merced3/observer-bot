# observer_discord.py

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

def setup_bot(application_id=None):
    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents, application_id=application_id)

    # Load channel ID inside setup
    bot.channel_id = int(os.getenv("DISCORD_INTEL_STREAM_CHANNEL_ID"))

    @bot.event
    async def on_ready():
        print(f"Observer is online as {bot.user}!")
        print(f"Connected Guilds: {[guild.name for guild in bot.guilds]}\n")

    return bot

async def send_message(bot, content):
    channel = bot.get_channel(bot.channel_id)
    if channel:
        await channel.send(content)

async def send_file(bot, file_path):
    channel = bot.get_channel(bot.channel_id)
    if channel:
        with open(file_path, 'rb') as f:
            discord_file = discord.File(f)
            await channel.send(file=discord_file)

async def fetch_message_content(bot, message_id):
    channel = bot.get_channel(bot.channel_id)
    if channel:
        message = await channel.fetch_message(message_id)
        return message.content
    return None

async def edit_message(bot, message_id, new_content):
    channel = bot.get_channel(bot.channel_id)
    if channel:
        message = await channel.fetch_message(message_id)
        await message.edit(content=new_content)
