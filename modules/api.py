from datetime import datetime
import requests

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
        else:
            print(Response.content)
    except requests.exceptions as error:
        print(f"Error: {error}")

    return False

# Get an App Token. This token only works to fetch public data from the api endpoints, not to join chat or streams
def GetAppToken(idClient, secretClient):
    Url = 'https://id.twitch.tv/oauth2/token'

    Parameters = {
        'client_id' : idClient,
        'client_secret' : secretClient,
        'grant_type': 'client_credentials'
    }

    Header = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        Response = requests.post(Url, headers=Header, data=Parameters)

        if Response.status_code == 200:
            Data = Response.json()
            return Data['access_token']
        else:
            print(Response.content)
    except requests.exceptions as error:
        print(f"Error: {error}")
    
    return None

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
                print(Response.content)
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
                print(Response.content)
                return None
    except requests.RequestException as error:
        print(f"Error: {error}")

    return None