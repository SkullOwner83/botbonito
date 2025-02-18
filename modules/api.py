from datetime import datetime
import requests
import asyncio

# Check if the token is valid
def TokenValidattion(Token):
    Url = 'https://id.twitch.tv/oauth2/validate'

    Headers = {
        'Authorization': f'OAuth {Token}'
    }

    try:
        Response = requests.get(Url, headers=Headers)

        if Response.status_code == 200:
            return True
    except requests.exceptions as error:
        print(f"Error: {error}")

    return False

# Get information about a specific user
def GetUser(User, Token, idClient):
    Url = 'https://api.twitch.tv/helix/users'

    Parameters = {
        'login': User
    }

    Headers = {
        "Client-ID": idClient,
        "Authorization": f"Bearer {Token}"
    }

    try:
        Response = requests.get(Url, headers=Headers, params=Parameters)

        if Response.status_code == 200:
            Data = Response.json()["data"]

            if len(Data) > 0:
                return Data[0]
            else:
                return None
    except requests.RequestException as error:
        print(f"Error: {error}")

    return None

# Check if the user follows the channel and return since when
def CheckFollow(idUser, idBroadcaster, Token, idClient):
    Url = 'https://api.twitch.tv/helix/channels/followers'

    Parameters = {
        'broadcaster_id': idBroadcaster,
        'user_id': idUser
    }

    Headers = {
        "Client-ID": idClient,
        "Authorization": f"Bearer {Token}"
    }

    try:
        Response = requests.get(Url, headers=Headers, params=Parameters)

        if Response.status_code == 200:
            Data = Response.json()["data"]

            if len(Data) > 0:
                DateObject = datetime.strptime(Data[0]["followed_at"], "%Y-%m-%dT%H:%M:%SZ")
                Date = DateObject.strftime("%d de %B de %Y")
                return Date
            else:
                return None
    except requests.RequestException as error:
        #print(f"Error: {error}")
        print("")

    return None