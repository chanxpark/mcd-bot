# bot.py
import io
import os
import json
import aiohttp
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
from crypto import get_crypto
from twitch import get_stream, get_subs, get_user, create_stream_online_sub, delete_sub
from janet import get_random_image

TOKEN = os.environ["BOT_TOKEN"]

bot = commands.Bot(command_prefix="!")
slash = SlashCommand(bot)
print("MCD Bot successfully connected")

guild_ids = [850148009655795742, 849687400988409876]


# for maintaining user names and user id mappings for Twitch
with open("./user_mapping.json", "r+") as f:
    file_contents = f.read()
    try:
        user_mapping = json.loads(file_contents)
    except:
        user_mapping = {}
        f.write(json.dumps(user_mapping))


# JANET COMMAND
# Returns a photo of xchocobars
@slash.slash(name="janet", description="Get a photo of xChocoBars", guild_ids=guild_ids)
async def _janet(ctx):
    img_url = get_random_image()
    async with aiohttp.ClientSession() as session:
        async with session.get(img_url) as resp:
            if resp.status != 200:
                await ctx.send(f"Something broke. This bot sucks.")
            else:
                data = io.BytesIO(await resp.read())
                await ctx.send(file=discord.File(data, "xChocoBars.jpg"))


# CRYTPO COMMANDS


@slash.slash(
    name="ada", description="Return the current price of ADA", guild_ids=guild_ids
)
async def _ada(ctx):
    info = get_crypto("ADA")
    price = round(info["quote"]["USD"]["price"], 4)
    percent_change_24 = round(info["quote"]["USD"]["percent_change_24h"], 2)
    await ctx.send(
        f"The current price of ADA is **{price}**. 24 Hour % Change: **{percent_change_24}%**"
    )


@slash.slash(
    name="crypto",
    description="Return the current price of a crypto",
    options=[
        create_option(
            name="symbol",
            description="Symbol of the crypto you want to search",
            option_type=3,
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


# TWITCH COMMANDS


def save_user_mapping(file):
    # save changes to Twitch user name and user id mapping
    with open("./user_mapping.json", "w") as f:
        f.write(json.dumps(file))


@slash.subcommand(
    base="twitch",
    name="online",
    description="Gets random info on Twitch Streams",
    options=[
        create_option(
            name="stream",
            description="Looks up if a stream is online and provides link to stream",
            option_type=3,
            required=True,
        )
    ],
    guild_ids=guild_ids,
)
async def _twitch_stream(ctx, stream: str):
    stream_info = get_stream(stream.strip()).json()

    if "error" in stream_info:
        message = f"That is not a valid stream. Please try again."
    elif not stream_info["data"]:
        message = f"The stream is not online."
    else:
        user = stream_info["data"][0]["user_name"]
        message = f"{user} is oneline!\nhttps://www.twitch.tv/{user}"

    await ctx.send(message)


@slash.subcommand(
    base="twitch",
    subcommand_group="notification",
    name="list",
    description="List active notifications",
    guild_ids=guild_ids,
)
async def _twitch_notification_list(ctx):
    sub_list = get_subs().json()
    list_of_stream = []
    for sub in sub_list["data"]:
        # add subs that have been verified and enabled by Twitch
        if sub["status"] == "enabled":
            user_id = sub["condition"]["broadcaster_user_id"]

            if user_id not in user_mapping:
                user_info = get_user("id", user_id).json()
                user_mapping[user_id] = {
                    "login": user_info["data"][0]["login"],
                    "display_name": user_info["data"][0]["display_name"],
                }
                save_user_mapping(user_mapping)

            list_of_stream.append(user_mapping[user_id]["display_name"])

    list_of_stream_string = "".join(["\n" + str(stream) for stream in list_of_stream])

    message = (
        f"You will be notified for the following streamers: {list_of_stream_string}"
    )
    await ctx.send(message)


@slash.subcommand(
    base="twitch",
    subcommand_group="notification",
    name="add",
    description="Add a channel notification for when a streamer comes online",
    options=[
        create_option(
            name="twitch", description="Twitch user name", option_type=3, required=True
        )
    ],
    guild_ids=guild_ids,
)
async def _twitch_notification_add(ctx, twitch_user_name: str):
    # create the subscription
    twitch_user_info = get_user("login", twitch_user_name).json()
    if not twitch_user_info["data"]:
        message = f"{twitch_user_name} is not a valid user. Please try again."
    else:
        twitch_user_id = twitch_user_info["data"][0]["id"]
        result = create_stream_online_sub(twitch_user_id)
        # check to make sure the subscription was successful
        data = result.json()
        if result.ok:
            message = (
                f"Notification for {twitch_user_name} has been successfully added."
            )
        else:
            message = f"{data['message']}. Please try again."

    await ctx.send(message)


@slash.subcommand(
    base="twitch",
    subcommand_group="notification",
    name="delete",
    description="Delete a channel notification for when a streamer comes online",
    options=[
        create_option(
            name="twitch", description="Twitch user name", option_type=3, required=True
        )
    ],
    guild_ids=guild_ids,
)
async def _twitch_notification_delete(ctx, twitch_user_name: str):
    twitch_user_info = get_user("login", twitch_user_name).json()
    if not twitch_user_info["data"]:
        message = f"{twitch_user_name} is not a valid user. Please try again."
    else:
        twitch_user_id = twitch_user_info["data"][0]["id"]
        sub_list = get_subs().json()
        for sub in sub_list["data"]:
            if sub["condition"]["broadcaster_user_id"] == twitch_user_id:
                r = delete_sub(sub["id"])
                if r.ok:
                    message = f"Notification for {twitch_user_name} has been deleted."
                else:
                    message = f"Something went wrong. Please try again."
                break
            message = f"Invalid request. There is no existing notifications for {twitch_user_name}."

    await ctx.send(message)


# MUSIC


@slash.slash(name="music")
async def music(ctx):
    print(ctx.author_id)


bot.run(TOKEN)
