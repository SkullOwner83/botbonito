import requests

def UserToken(idClient, ClientSecret, RedirectUri, Code):
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        'client_id': idClient,
        'client_secret': ClientSecret,
        'code': Code,
        'grant_type': 'authorization_code',
        'redirect_uri': RedirectUri,
    }

    response = requests.post(url, params=params)
    return response.json().get('access_token')

# Check if the oauth token is still valid
def TokenValidattion(OAuth):
    Url = 'https://id.twitch.tv/oauth2/validate'

    Headers = {
        'Authorization': 'OAuth ' + OAuth.replace("oauth:","")
    }

    try:
        Response = requests.get(Url, headers=Headers)
        Response.raise_for_status()
        Data = Response.json
        return Data
    except requests.exceptions.HTTPError as errh:
        print(f"Error HTTP: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error de conexión: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Error de tiempo de espera: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Error general: {err}")

    return False

# Get the app token by his client id and secret of the aplication 
def AppToken(idClient, ClientSecret):
    Url = 'https://id.twitch.tv/oauth2/token'

    params = {
        'client_id': idClient,
        'client_secret': ClientSecret,
        'grant_type': 'client_credentials',
    }

    response = requests.post(Url, params=params)
    data = response.json()
    return data['access_token']

# Get the broadcasterr id by his username and the client id and apptoken of the aplication
def BroadcasterId(UserName, idClient, AccessToken):
    Url = f'https://api.twitch.tv/helix/users?login={UserName}'

    headers = {
        'Client-Id': idClient,
        'Authorization': f'Bearer {AccessToken}'
    }

    response = requests.get(Url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        if data['data']:
            return data['data'][0]['id']
        else:
            print(f"No se encontró el usuario con el nombre {UserName}.")
            return None
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Get the user id by his username and the client id and apptoken of the aplication
def UserId(UserName, idClient, AccessToken):
    url = f'https://api.twitch.tv/helix/users'
    params = {'login': UserName}
    
    headers = {
        'Authorization': f'Bearer {AccessToken}',
        'Client-Id': idClient
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()

        if data.get('data'):
            user_id = data['data'][0]['id']
            return user_id
        else:
            print(f'No se encontró el usuario: {UserName}')
            return None
    else:
        print(f'Error en la solicitud: {response.status_code}')
        print(response.text)
        return None