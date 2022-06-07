# bot.py
import io
import os
import interactions

from crypto import get_crypto
from janet import get_random_image

TOKEN = os.environ["BOT_TOKEN"]

bot = interactions.Client(token=TOKEN)
print("MCD Bot successfully connected")

guild_ids = [850148009655795742, 849687400988409876]

# CRYTPO COMMANDS


@bot.command(
    name="ada",
    description="Return the current price of ADA",
    guild_ids=guild_ids
)
async def _ada(ctx):
    info = get_crypto("ADA")
    price = round(info["quote"]["USD"]["price"], 4)
    percent_change_24 = round(info["quote"]["USD"]["percent_change_24h"], 2)
    await ctx.send(
        f"The current price of ADA is **{price}**. 24 Hour % Change: **{percent_change_24}%**"
    )


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


bot.start()
