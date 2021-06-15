import os
import json
import requests
import sys

BASE_URL = "https://api.twitch.tv/helix"
CLIENT_ID = "qjxv2zaxmcg3rr08oisc2dvu8r5u5w"
CLIENT_SECRET = os.environ["TWITCH_CLIENT_SECRET"]
TOKEN = os.environ["TWITCH_TOKEN"]

headers = {
    "Client-Id": CLIENT_ID,
    "Authorization": "Bearer " + TOKEN
}


def get_token():
    body = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }

    r = requests.post('https://id.twitch.tv/oauth2/token', body)

    return r.content


def validate_token(token):
    url = "https://id.twitch.tv/oauth2/validate"
    body = {
        "Authorization": "OAuth " + token
    }
    r = requests.get(url, headers=body)

    # returns 200 if token is valid
    return r


def create_stream_online_sub(streamer_user_id):
    url = f"{BASE_URL}/eventsub/subscriptions"

    headers["Content-Type"] = "application/json"

    payload = {
        "type": "stream.online",
        "version": "1",
        "condition": {
            "broadcaster_user_id": streamer_user_id
        },
        "transport": {
            "method": "webhook",
            "callback": "https://n7rqxfes54.execute-api.us-east-1.amazonaws.com/mcd-bot",
            "secret": "i3BAhjxMwta46n"
        }
    }

    r = requests.post(url, headers=headers, data=json.dumps(payload))

    return r


def delete_sub(sub_id):
    url = f"{BASE_URL}/eventsub/subscriptions?id={sub_id}"

    r = requests.delete(url, headers=headers)

    return r


def get_subs():
    url = f"{BASE_URL}/eventsub/subscriptions?status=enabled"

    r = requests.get(url, headers=headers)

    return r


def get_user(search_type, user):

    if str(search_type).lower() == "id":
        url = f"{BASE_URL}/users?id={user}"
    elif str(search_type).lower() == "login":
        url = f"{BASE_URL}/users?login={user}"

    r = requests.get(url, headers=headers)

    return r


def get_stream(login):

    url = f"{BASE_URL}/streams?user_login={login}"
    r = requests.get(url, headers=headers)

    return r


def main():
    # Keeps reading from stdin and quits only if the word 'exit' is there
    # This loop, by default does not terminate, since stdin is open

    menu_options = """
[1] Get Token
[2] Validate Token
[3] List Subscriptions
[4] Create Subscription
[5] Delete Subscription
[6] Get User
[7] Get Stream
Exit
"""
    ans = True
    while ans:
        print(menu_options)
        ans = input("Menu selection: ")

        if ans.strip() == "1":
            print(f"Your token has been generated:\n {get_token()}")
        elif ans.strip() == "2":
            token = input("What token would you like to validate?: ")
            print(validate_token(token).json())
        elif ans.strip() == "3":
            print(get_subs().json())
        elif ans.strip() == "4":
            streamer_id = input(
                "What streamer (streamer id) would you like to add?: ")
            print(create_stream_online_sub(streamer_id).json())
        elif ans.strip() == "5":
            sub_id = input(
                "What stream subscription would you like to delete?: ")
            print(delete_sub(sub_id))
        elif ans.strip() == "6":
            user_type = input("Do you want to look up a login or id?: ")
            while user_type.strip().lower() not in ["login", "id"]:
                user_type = input("Invalid input. Please select login or id: ")
            user_name = input("What user would you like to look up?: ")
            print(get_user(user_type.strip(), user_name).json())
        elif ans.strip() == "7":
            user_name = input("What stream would you like to look up?: ")
            print(get_stream(user_name).json())
        elif ans.strip().upper() == "EXIT":
            print("Exiting")
            exit(0)
        else:
            print("Not a valid selection. Try again.")


if __name__ == "__main__":
    main()
