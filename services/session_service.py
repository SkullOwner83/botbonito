from typing import Callable, List
import webbrowser
from utilities.enums import AccountType
from models.appconfig import AppConfig
from models.user import User
from utilities import *

class SessionService:
    def __init__(self):
        self.user_account = None
        self.bot_account = None
        self.is_logged_in = False
        self.on_login_callback: List[Callable] = []
        self.on_logout_callback: List[Callable] = []

    # Validate if the token is valid or refresh it if it's expired
    def validation(self, credentials: dict, app_config: AppConfig, account_type: AccountType) -> bool:
        if Token.validation(credentials['access_token']):        
            if self.load_account(credentials, app_config, account_type): return True
        else:
            if credentials['refresh_token']:
                token = Token(app_config.client_id, app_config.client_secret, Constants.BOT_SCOPES, app_config.redirect_uri)
                token_refreshed = token.refresh_access_token(credentials['refresh_token'])
                
                if token_refreshed:
                    new_token = token_refreshed.get('access_token')
                    new_refresh_token = token_refreshed.get('refresh_token')

                    if Token.validation(new_token):
                        credentials['access_token'] = new_token
                        credentials['refresh_token'] = new_refresh_token
                        self.load_account(credentials, app_config, account_type)
                        print("Token has been refreshed.")
                        return True

        return False

    # Login the twitch account using the credentials
    def login(self, app_config: AppConfig, account_type: str) -> bool:
        scope = Constants.USER_SCOPES if account_type == AccountType.USER else Constants.BOT_SCOPES
        token = Token(app_config.client_id, app_config.client_secret, scope, app_config.redirect_uri)
        auth_url = token.generate_auth_url()
        webbrowser.open(auth_url)
        token_data = token.get_authorization()

        if token_data and token.validation(token_data.get('access_token')):
            credentials = {
                'access_token': token_data['access_token'],
                'refresh_token': token_data['refresh_token']
            }
        
            if self.load_account(credentials, app_config, account_type):
                self.on_login(self.user_account if account_type == AccountType.USER else self.bot_account)
                return True
    
        return False
    
    # Logout the specified account
    def logout(self, account_type: str) -> None:
        if account_type == AccountType.USER:
            self.user_account = None
            self.is_logged_in = False
        elif account_type == AccountType.BOT:
            self.bot_account = None

    # Fetch the account data from the twitch API to load the account
    def load_account(self, credentials: dict, app_config: AppConfig, account_type: str) -> bool:
        api = Api(credentials['access_token'], app_config.client_id)
        account_data= api.get_user()

        if account_data:
            account = User(
                id=account_data.get('id'), 
                email=account_data.get('email'),
                username=account_data.get('login'),
                display_name=account_data.get('display_name'),
                broadcaster_type=account_data.get('broadcaster_type'),
                profile_image=account_data.get('profile_image_url'),
                credentials=credentials
            )

            if account_type == AccountType.USER: 
                self.user_account = account
                self.is_logged_in = True
            elif account_type == AccountType.BOT: self.bot_account = account
            return True

        return False

    # Create a dictionary of the accounts to can be saved to a json file
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

    def on_login(self, account: User) -> None:
        for callback in self.on_login_callback:
            callback(account)
    
    def on_logout(self) -> None:
        for callback in self.on_logout_callback:
            callback()