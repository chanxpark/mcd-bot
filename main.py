# bot.py
import os
import discord
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
from crypto import get_crypto

TOKEN = os.environ["BOT_TOKEN"]

client = discord.Client()
slash = SlashCommand(
    client, sync_commands=True
)  # Declares slash commands through the client.


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")


guild_ids = [850148009655795742, 849687400988409876]


@slash.slash(name="ping", guild_ids=guild_ids)
async def _ping(ctx):  # Defines a new "context" (ctx) command called "ping."
    await ctx.send(f"Pong! ({client.latency*1000}ms)")


@slash.slash(
    name="ada", description="Return the current price of ADA", guild_ids=guild_ids
)
async def _ada(ctx):
    info = (get_crypto("ADA"))
    price = round(info["quote"]["USD"]["price"], 4)
    percent_change_24 = round(info["quote"]["USD"]["percent_change_24h"], 2)
    await ctx.send(f"The current price of ADA is **{price}**. 24 Hour % Change: **{percent_change_24}%**")


@slash.slash(
    name="crypto",
    description="Return the current price of a crypto",
    options=[
        create_option(
            name="symbol",
            description="Symbol of the crypto you want to search",
            option_type=3,
            required=True
        )
    ],
    guild_ids=guild_ids
)
async def _crypto(ctx, symbol: str):
    info = (get_crypto(symbol.strip().upper()))
    if info == "error":
        await ctx.send(f"{symbol.strip().upper()} does not exist")
    else:
        price = round(info["quote"]["USD"]["price"], 4)
        percent_change_24 = round(
            info["quote"]["USD"]["percent_change_24h"], 2)
        await ctx.send(f"The current price of {symbol.strip().upper()} is **{price}**. 24 Hour % Change: **{percent_change_24}%**")

client.run(TOKEN)
