from typing import Optional
import webbrowser
from modules.file import File
from models.credentials import Credentials
from models.user import User
from modules.api import Api
from modules.token import Token

class SessionService:
    def __init__(self):
        self.user_account = None
        self.bot_account = None
        self.is_logged_in = False

    def validation(self, credentials: dict, botconfig: dict) -> bool:
        if Token.validation(credentials['access_token']):
            self.load_account(credentials, botconfig, 'bot')
            return True
        else:
            if credentials['refresh_token']:
                token = Token(botconfig['client_id'], botconfig['client_secret'], botconfig['scope'], botconfig['redirect_uri'])
                token_refreshed = token.refresh_access_token(credentials['refresh_token'])
                
                if token_refreshed:
                    new_token = token_refreshed.get('access_token')
                    new_refresh_token = token_refreshed.get('refresh_token')

                    if Token.validation(new_token):
                        credentials['access_token'] = new_token
                        credentials['refresh_token'] = new_refresh_token
                        self.load_account(credentials, botconfig, 'bot')
                        print("Token has been refreshed.")
                        return True
            
        return False

    def login(self, botconfig: dict) -> bool:
        token = Token(botconfig['client_id'], botconfig['client_secret'], ['user:read:email'], botconfig['redirect_uri'])
        auth_url = token.generate_auth_url()
        webbrowser.open(auth_url)
        token_data = token.get_authorization()
        credentials = {
            'access_token': token_data['access_token'],
            'refresh_token': token_data['refresh_token']
        }
        
        if self.load_account(credentials, botconfig, 'user'):
            self.is_logged_in = True
            return True
    
        return False
    
    def logout(self):
        self.user_account = None
        self.is_logged_in = False

    def load_account(self, credentials, botconfig, account_type) -> bool:
        api = Api(credentials['access_token'], botconfig['client_id'])
        account_data= api.get_user()

        if account_data:
            account = User(
                id=account_data.get('id'), 
                name=account_data.get('display_name'),
                email=account_data.get('email'),
                broadcaster_type=account_data.get('broadcaster_type'),
                profile_image=account_data.get('profile_image_url'),
                credentials=credentials
            )

            if account_type == 'user': self.user_account = account
            elif account_type == 'bot': self.bot_account = account
            return True

        return False

    def serialize(self) -> dict:
        dictionary = {
            "bot": {
                "access_token": self.bot_account.credentials['access_token'] if self.bot_account else "",
                "refresh_token": self.bot_account.credentials['refresh_token'] if self.bot_account else "",
            },
            "user": {
                "access_token": self.user_account.credentials['access_token'] if self.user_account else "",
                "refresh_token": self.user_account.credentials['refresh_token'] if self.user_account else "",
            }
        }

        return dictionary