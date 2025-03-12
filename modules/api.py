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
    
    def delete_message(self, broadcaster_id, moderator_id, message_id):
        url = 'https://api.twitch.tv/helix/moderation/chat'

        params = {
            'broadcaster_id': broadcaster_id,
            'moderator_id': moderator_id,
            'message_id': message_id
        }

        headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {self.token}'
        }

        try:
            response = requests.delete(url, headers=headers, params=params)

            if response.status_code == 204:
                return True
            else:
                print(f"Error {response.status_code}: {response.content}")
        except requests.RequestException as error:
            print(f"Error: {error}")
        
        return False
    
    def ban_user(self, broadcaster_id, moderator_id, *, user_id, duration=0, timeout=False):
        url = 'https://api.twitch.tv/helix/moderation/bans'

        params = {
            'broadcaster_id': broadcaster_id,
            'moderator_id': moderator_id
        }

        headers = {
            'Authorization': f'Bearer {self.token}',
            'Client-ID': self.client_id,
            'Content-Type': 'application/json'
        }

        data = {
            'data': { 
                'user_id': user_id
            }
        }

        if timeout:
            data.get('data')['duration'] = duration if duration > 0 else 300

        try:
            response = requests.post(url, headers=headers, params=params, json=data)

            if response.status_code == 200:
                return True
            else:
                print(f"Error {response.status_code}: {response.content}")
        except requests.RequestException as error:
            print(f"Error: {error}")