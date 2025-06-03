import requests
from typing import Optional, Union
from datetime import datetime   

class Api():
    def __init__(self, token: str, client_id: str) -> None:
        self.token = token
        self.client_id = client_id

    # Get general information about a specific user.
    def get_user(self, user: Optional[str] = None) -> Optional[dict]:
        url = 'https://api.twitch.tv/helix/users'

        parameters = {
            'login': user
        }

        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.token}"
        }

        try:
            response = requests.get(url, headers=headers, params=parameters if user else None)

            if response.status_code == 200:
                data = response.json()

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
    def check_follow(self, user_id: Union[int, str], broadcaster_id: Union[int, str]) -> Optional[str]:
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

            if response.status_code == 200:
                data = response.json()

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
    
    # Get goals from a specific user
    def get_goals(self, user_id: Union[int, str]) -> Optional[dict]:
        url = 'https://api.twitch.tv/helix/goals'

        params = {
            'broadcaster_id': user_id,
        }

        headers = {
            'Authorization': f'Bearer {self.token}',
            'Client-ID': self.client_id
        }

        try:
            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()
                return data['data']
            else:
                print(f"Error {data['status']}: {data['message']}")
        except requests.RequestException as error:
            print(f"Error: {error}")
        
        return None
    
    # Send a request to delete a specific message from the chat
    def delete_message(self, broadcaster_id: Union[int, str], moderator_id: Union[int, str], message_id: Union[int, str]) -> bool:
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
    
    def set_ban(self, broadcaster_id: Union[int, str], moderator_id: Union[int, str], user_id: Union[int, str], reason: str = None) -> bool:
        return self._penalty_request(broadcaster_id, moderator_id, user_id, reason=reason)

    def set_timeout(self, broadcaster_id: Union[int, str], moderator_id: Union[int, str], user_id: Union[int, str], duration: int = 300, reason: str = None) -> bool:
        return self._penalty_request(broadcaster_id, moderator_id, user_id, duration=duration, reason=reason)
    
    def _penalty_request(self, broadcaster_id: Union[int, str], moderator_id: Union[int, str], user_id: Union[int, str], *, duration: int = 0, reason: str = None) -> bool:
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
                'user_id': user_id,
                'reason': reason
            }
        }

        if duration is not None:
            data['data']['duration'] = duration

        try:
            response = requests.post(url, headers=headers, params=params, json=data)

            if response.status_code == 200:
                return True
            else:
                print(f"Error {response.status_code}: {response.content}")
        except requests.RequestException as error:
            print(f"Error: {error}")

    def get_subscriptions(self) -> Optional[dict]:
        url = 'https://api.twitch.tv/helix/eventsub/subscriptions'

        headers = {
            'Authorization': f'Bearer {self.token}',
            'Client-ID': self.client_id
        }

        try:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                return data['data']
            else:
                print(f"Error {response.status_code}: {response.content}")
        except requests.RequestException as error:
            print(f"Error: {error}")
        
        return None

    def create_subscription(self, broadcaster_id: str, session_id: str, subscription_type: str, *, version: Optional[int] = 1 ) -> bool:
        url = 'https://api.twitch.tv/helix/eventsub/subscriptions'

        headers = {
            'Authorization' : f'Bearer {self.token}',
            'Client-ID' : self.client_id,
            'Content-Type': 'application/json'
        }

        payload = {
            'type': subscription_type,
            'version': version,
            'condition': {
                'broadcaster_user_id': broadcaster_id,
            },
            'transport': {
                'method': 'websocket',
                'session_id': session_id
            }
        }

        if subscription_type in ['channel.follow']:
            payload['condition']['moderator_user_id'] = broadcaster_id

        try:
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 202:
                return True
            else:
                print(f"Error {response.status_code}: {response.content}")
        except requests.RequestException as error:
            print(f"Error: {error}")
        
        return False
    
    def delete_subscription(self, subscription_id) -> bool:
        url = 'https://api.twitch.tv/helix/eventsub/subscriptions'

        paramas = {
            'id': subscription_id
        }

        headers = {
            'Authorization': f'Bearer {self.token}',
            'Client-ID': self.client_id
        }

        try:
            response = requests.delete(url, headers=headers, params=paramas)

            if response.status_code == 204:
                return True
            else:
                print(f"Error {response.status_code}: {response.content}")
        except requests.RequestException as error:
            print(f"Error: {error}")

        return False