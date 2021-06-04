# bot.py
import os
import discord
from discord_slash import SlashCommand
from crypto import get_ada_price

TOKEN = os.environ["BOT_TOKEN"]

client = discord.Client()
slash = SlashCommand(
    client, sync_commands=True
)  # Declares slash commands through the client.


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")


guild_ids = [850148009655795742]


@slash.slash(name="ping", guild_ids=guild_ids)
async def _ping(ctx):  # Defines a new "context" (ctx) command called "ping."
    await ctx.send(f"Pong! ({client.latency*1000}ms)")


@slash.slash(
    name="ada", description="Return the current price of ADA", guild_ids=guild_ids
)
async def _ada(ctx):
    ada_price = str(round(get_ada_price(), 2))
    await ctx.send(f"The current price of ADA is {ada_price}")


client.run(TOKEN)
