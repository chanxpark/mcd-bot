import os
import requests
import json
from twitch import get_user
from discord import Webhook, RequestsWebhookAdapter

webhook_url = os.environ["DEV_WEBHOOK"]


def lambda_handler(event, context):

    payload = event["body"]

    try:
        if "broadcaster_user_id" in payload["subscription"]["condition"]:
            user_id = payload["subscription"]["condition"]["broadcaster_user_id"]
            user = get_user("id", user_id).json()
            print(user)
            user_name = user['data'][0]["login"]
            webhook = Webhook.from_url(
                webhook_url, adapter=RequestsWebhookAdapter())
            webhook.send(
                f"{user_name} is live!\nhttps://www.twitch.tv/{user_name}")

        print("success")
        return 200

    except:
        return "error"
