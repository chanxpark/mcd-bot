import os
import logging
import interactions
from interactions.api.models.misc import Image
from utils.tools import load_json, sanitize_str

from riotgames.requests import TFT, TFT_API
from crypto import get_crypto

logging.getLogger().setLevel(logging.INFO)

DISCORD_TOKEN = os.environ["BOT_TOKEN"]
bot = interactions.Client(token=DISCORD_TOKEN)

# Initialize TFT object
RG_API_KEY = os.environ["rg_api_key"]
TFT_API.initialize(RG_API_KEY)

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
    name="setup",
    description="sets up assets for TFT bot",
    scope=dev
)
async def setup(ctx):
    await ctx.defer()
    _guild = await ctx.get_guild()

    try:
        # get assets to load
        assets = load_json('riotgames/assets/assets_list.json')

        _counter = 0
        for asset_class in assets:
            for asset in assets[asset_class]:
                logging.info(f"creating emoji for TFT_{asset_class}_{asset}")
                created = await _guild.create_emoji(
                    Image(f"riotgames/assets/{asset_class}/{asset}.png"),
                    name=f"TFT_{asset_class}_{asset}"
                )
                print(created)
                _counter += 1

        logging.info(f"Successfully loaded {_counter} assets")
        await ctx.send(f"Successfully loaded {_counter} assets")

    except Exception as e:
        logging.error(f"Error: {e}")
        await ctx.send("Error in set up")


@bot.command(
    name="cutoff",
    description="get challenger and grandmaster LP cutoffs",
    scope=guilds
)
async def cutoff(ctx):
    await ctx.defer()
    try:
        cutoffs = TFT_API.get_ranked_cutoff()
        message = f"""**Challenger:** {cutoffs['challenger']}
**Grandmaster:** {cutoffs['grandmaster']}
"""
        await ctx.send(message)

    except Exception as e:
        logging.error(f"Error: {e}")
        await ctx.send("There was an error")


@bot.command(
    name="rank",
    description="get rank of a player",
    scope=guilds,
    options=[
        interactions.Option(
            name="summoner",
            description="summoner name to search",
            type=interactions.OptionType.STRING,
            required=True,
        )
    ]
)
async def rank(ctx, summoner: str):
    stats = TFT_API.get_ranked_stats(summoner)
    ranked_info_embed = interactions.Embed(title=stats['name'])

    _full_rank = stats['tier'].capitalize()
    if stats['tier'] not in ['Master', 'Grandmaster', 'Challenger']:
        _full_rank += f" {stats['rank']}"

    ranked_info_embed.add_field(
        name="Rank",
        value=f"{_full_rank} - {stats['lp']}LP",
        inline=False
    )

    ranked_info_embed.add_field(
        name="Wins",
        value=stats['wins'],
        inline=True
    )

    ranked_info_embed.add_field(
        name="Win Rate",
        value=round(stats['win_rate'], 1),
        inline=True
    )

    ranked_info_embed.add_field(
        name="Total Played",
        value=stats['played'],
        inline=True
    )

    message = f"""**{stats['name']}**
**Rank:** {_full_rank} - {stats['lp']}
**Wins:** {stats['wins']}
**Win Rate:** {round(stats['win_rate'], 1)}
**Total Played:** {stats['played']}
"""

    # embeds not working properly -> wait til next release for interactions
    # await ctx.send(embeds=ranked_info_embed)
    await ctx.send(message)


bot.start()
