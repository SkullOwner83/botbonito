from datetime import datetime
import requests

# Get information about a specific user
def get_user(User, Token, idClient):
    url = 'https://api.twitch.tv/helix/users'

    parameters = {
        'login': User
    }

    headers = {
        "Client-ID": idClient,
        "Authorization": f"Bearer {Token}"
    }

    try:
        response = requests.get(url, headers=headers, params=parameters)

        if response.status_code == 200:
            data = response.json()["data"]

            if len(data) > 0:
                return data[0]
            else:
                print(response.content)
                return None
    except requests.RequestException as error:
        print(f"Error: {error}")

    return None

# Check if the user follows the channel and return since when
def check_follow(idUser, idBroadcaster, Token, idClient):
    url = 'https://api.twitch.tv/helix/channels/followers'

    parameters = {
        'broadcaster_id': idBroadcaster,
        'user_id': idUser
    }

    headers = {
        "Client-ID": idClient,
        "Authorization": f"Bearer {Token}"
    }

    try:
        response = requests.get(url, headers=headers, params=parameters)

        if response.status_code == 200:
            data = response.json()["data"]

            if len(data) > 0:
                date_object = datetime.strptime(data[0]["followed_at"], "%Y-%m-%dT%H:%M:%SZ")
                date = date_object.strftime("%d de %B de %Y")
                return date
            else:
                print(response.content)
                return None
    except requests.RequestException as error:
        print(f"Error: {error}")

    return None