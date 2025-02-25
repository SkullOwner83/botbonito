import os
from twitchio.ext import commands
from modules import file
from modules.token import Token
from modules.file import File
from bot.bot import Bot
import config

# Load config and variable values from files
project_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(project_path, "config")
credentials_path = os.path.join(config_path, "credentials.json")
botconfig_path = os.path.join(config_path, "botconfig.json")
credentials = File.open(credentials_path)
botconfig = File.open(botconfig_path)


token = credentials['token']
client_id = credentials['client_id']
client_secret = credentials['client_secret']
redirect_uri = botconfig['redirect_uri']
scope = botconfig['scope']

# Check if the Oauth Token of bot account is valid or hasn't expired yet.
ValidToken = Token.validation(token)

while ValidToken == False:
    print("Tu token no es valido. Ingresa al siguiente sitio para obtener un nuevo token:")
    token = Token(client_id, client_secret, scope, redirect_uri)
    NewToken = token.get_authorization()
    
    if token.validation(NewToken):
        credentials['token'] = NewToken
        File.save(credentials_path, credentials)
        print("Token validado")
        ValidToken = True

# Execute bot on loop
if __name__ == '__main__':
    botbonito = Bot(botconfig, credentials)
    botbonito.run()