import os
import discord
import logging
from discord import app_commands

from crypto import get_crypto

logging.getLogger().setLevel(logging.INFO)

TOKEN = os.environ["BOT_TOKEN"]

guilds = [
    discord.Object(id=849687400988409876),  # k3MCD
    discord.Object(id=850148009655795742)   # reboob-dev
]

# CRYTPO COMMANDS


class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            for guild in guilds:
                await tree.sync(guild=guild)
                self.synced = True
        logging.INFO(f"Logged in as {self.user}")


client = aclient()
tree = app_commands.CommandTree(client)


@tree.command(
    name="ada",
    description="Return the current price of ADA",
    guilds=guilds
)
async def ada(interaction: discord.Interaction):
    info = get_crypto("ADA")
    price = round(info["quote"]["USD"]["price"], 4)
    percent_change_24 = round(info["quote"]["USD"]["percent_change_24h"], 2)
    await interaction.response.send_message(f"The current price of ADA is **{price}**. 24 Hour % Change: **{percent_change_24}%**")


"""
@bot.command(
    name="crypto",
    description="Return the current price of a crypto",
    options=[
        interactions.Option(
            name="symbol",
            description="Symbol of the crypto you want to search",
            option_type=interactions.OptionType.STRING,
            required=True,
        )
    ],
    guild_ids=guild_ids,
)
async def _crypto(ctx, symbol: str):
    info = get_crypto(symbol.strip().upper())
    if info == "error":
        await ctx.send(f"{symbol.strip().upper()} does not exist")
    else:
        price = round(info["quote"]["USD"]["price"], 4)
        percent_change_24 = round(info["quote"]["USD"]["percent_change_24h"], 2)
        await ctx.send(
            f"The current price of {symbol.strip().upper()} is **{price}**. 24 Hour % Change: **{percent_change_24}%**"
        )
"""


client.run(TOKEN)
