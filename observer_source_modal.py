# observer_source_modal.py
import discord
import json
import os
from discord import app_commands
from discord.ext import commands
from observer_message_format import SourceAdded, SourceAlreadyExists

# Path to your sources file
SOURCES_FILE = "sources.json"

class SourceModal(discord.ui.Modal, title="Add a New Source"):
    def __init__(self):
        super().__init__(timeout=None)

        # URL input field
        self.url = discord.ui.TextInput(
            label="Source URL",
            placeholder="Enter the full RSS/API URL",
            required=True,
            max_length=300
        )
        self.add_item(self.url)

        # Name input field
        self.name = discord.ui.TextInput(
            label="Source Name",
            placeholder="Enter a human-readable source name",
            required=True,
            max_length=100
        )
        self.add_item(self.name)

        # Source type input field
        self.source_type = discord.ui.TextInput(
            label="Source Type",
            placeholder="Examples: News, Data, Blog, API, Government",
            required=True,  # You can set to False if you want it optional later
            max_length=50
        )
        self.add_item(self.source_type)

    async def on_submit(self, interaction: discord.Interaction):
        # Build the source dictionary
        new_source = {
            "url": self.url.value.strip(),
            "name": self.name.value.strip(),
            "type": self.source_type.value.strip(),
            "added_by": str(interaction.user),
            "message_id": interaction.message.id if interaction.message else 0
        }

        # Ensure sources.json exists
        if not os.path.exists(SOURCES_FILE):
            with open(SOURCES_FILE, "w") as f:
                json.dump({"sources": []}, f, indent=4)

        # Load and update sources.json
        with open(SOURCES_FILE, "r") as f:
            data = json.load(f)

        # Prevent duplicates
        if any(source["url"] == new_source["url"] for source in data["sources"]):
            await interaction.response.send_message(SourceAlreadyExists(), ephemeral=True)
            return

        data["sources"].append(new_source)

        with open(SOURCES_FILE, "w") as f:
            json.dump(data, f, indent=4)

        await interaction.response.send_message(SourceAdded(), ephemeral=True)

class SourceTypeSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="News", description="News-based sources"),
            discord.SelectOption(label="Data", description="Raw data feeds"),
            discord.SelectOption(label="Blog", description="Blog or opinion sources"),
            discord.SelectOption(label="Other", description="Anything else")
        ]
        super().__init__(
            placeholder="Select Source Type",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        # Optional if you want to react when selection is made immediately
        pass

# This is how you would add the slash command into your bot setup (in main.py)
async def setup_modals(bot: commands.Bot):
    @bot.tree.command(name="addsource", description="Add a new source using a modal form")
    async def addsource_slash(interaction: discord.Interaction):
        try:
            await interaction.response.send_modal(SourceModal())
        except Exception as e:
            await interaction.response.send_message(f"⚠️ Failed to send modal: {e}", ephemeral=True)

    await bot.tree.sync()  # Sync the slash commands to Discord
