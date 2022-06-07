import os
import logging
import interactions

from crypto import get_crypto

logging.getLogger().setLevel(logging.INFO)

TOKEN = os.environ["BOT_TOKEN"]
bot = interactions.Client(token=TOKEN)

guilds = [
    849687400988409876,  # k3MCD
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
    await ctx.response.send_message(f"The current price of ADA is **{price}**. 24 Hour % Change: **{percent_change_24}%**")


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


bot.start()
