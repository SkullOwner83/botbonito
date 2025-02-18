import requests

# Check if the oauth token is valid
def TokenValidattion(Token):
    Url = 'https://id.twitch.tv/oauth2/validate'

    Headers = {
        'Authorization': f'OAuth {Token}'
    }

    try:
        response = requests.get(Url, headers=Headers)

        if response.status_code == 200:
            return True
    except requests.exceptions as error:
        print(f"Error: {error}")
    
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