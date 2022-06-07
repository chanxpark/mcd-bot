import os
import logging
import interactions

from riotgames.requests import TFT_API
from crypto import get_crypto

logging.getLogger().setLevel(logging.INFO)

DISCORD_TOKEN = os.environ["BOT_TOKEN"]
bot = interactions.Client(token=DISCORD_TOKEN)

# Initialize TFT object
RG_API_KEY = os.environ["rg_api_key"]
TFT_API.initialize

guilds = [
    849687400988409876,  # k3MCD
    850148009655795742   # reboob-dev
]

dev = [
    850148009655795742   # reboob-dev
]

# CRYTPO COMMANDS


@bot.command(
    name="ada",
    description="Return the current price of ADA",
    scope=guilds
)
async def ada(ctx: interactions.CommandContext):
    info = get_crypto("ADA")
    price = round(info["quote"]["USD"]["price"], 4)
    percent_change_24 = round(info["quote"]["USD"]["percent_change_24h"], 2)
    await ctx.send(f"The current price of ADA is **{price}**. 24 Hour % Change: **{percent_change_24}%**")


@bot.command(
    name="crypto",
    description="Return the current price of a crypto",
    scope=guilds,
    options=[
        interactions.Option(
            name="symbol",
            description="Symbol of the crypto you want to search",
            type=interactions.OptionType.STRING,
            required=True,
        )
    ]
)
async def crypto(ctx, symbol: str):
    info = get_crypto(symbol.strip().upper())
    if info == "error":
        await ctx.send(f"{symbol.strip().upper()} does not exist")
    else:
        price = round(info["quote"]["USD"]["price"], 4)
        percent_change_24 = round(info["quote"]["USD"]["percent_change_24h"], 2)
        await ctx.send(
            f"The current price of {symbol.strip().upper()} is **{price}**. 24 Hour % Change: **{percent_change_24}%**"
        )

# TFT Commands


match_history_next = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label="Next",
    custom_id="match_history_next",
)

match_history_previous = interactions.Button(
    style=interactions.ButtonStyle.DANGER,
    label="Previous",
    custom_id="match_history_previous",
)

row = interactions.ActionRow(
    components=[match_history_previous, match_history_next]
)


@bot.command(
    name="matches",
    description="Get match history ",
    scope=dev
)
async def matches(ctx):
    await ctx.send("rows!", components=row)


@bot.command(
    name="cutoff",
    description="get challenger and grandmaster LP cutoffs",
    scope=guilds
)
async def cutoff(ctx):
    cutoffs = TFT_API.get_ranked_cutoff
    message = f"""**Chalenger:** {cutoffs['challenger']}
**Grandmaster:** {cutoffs['grandmaster']}
"""
    await ctx.send(message)


bot.start()
