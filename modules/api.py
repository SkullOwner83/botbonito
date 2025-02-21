from datetime import datetime
import requests

class Api():
    def __init__(self, token, client_id):
        self.token = token
        self.client_id = client_id

    # Get information about a specific user
    def get_user(self, user):
        url = 'https://api.twitch.tv/helix/users'

        parameters = {
            'login': user
        }

        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.token}"
        }

        try:
            response = requests.get(url, headers=headers, params=parameters)
            data = response.json()

            if response.status_code == 200:
                if len(data['data']) > 0:
                    return data['data'][0]
                else:
                    print("No se ha encontrado el usuario")
            else:
                print(f"Error {data['status']}: {data['message']}")
        except requests.RequestException as error:
            print(f"Error: {error}")

        return None
    
    # Check if the user follows the channel and return since when
    def check_follow(self, user_id, broadcaster_id):
        url = 'https://api.twitch.tv/helix/channels/followers'

        parameters = {
            'broadcaster_id': broadcaster_id,
            'user_id': user_id
        }

        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.token}"
        }

        try:
            response = requests.get(url, headers=headers, params=parameters)
            data = response.json()

            if response.status_code == 200:
                if len(data['data']) > 0:
                    date_object = datetime.strptime(data["data"][0]["followed_at"], "%Y-%m-%dT%H:%M:%SZ")
                    date = date_object.strftime("%d de %B de %Y")
                    return date
                else:
                    print("El usuario no sigue al canal especificado")
            else:
                print(f"Error {data['status']}: {data['message']}")
        except requests.RequestException as error:
            print(f"Error: {error}")

        return None