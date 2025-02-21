import os
from twitchio.ext import commands
from modules import file
from modules.api import Api
from modules.token import Token
from bot.bot import Bot

# Load config and variable values from files
ProjectPath = os.path.dirname(os.path.abspath(__file__))
ConfigPath = f"{ProjectPath}/config/"

Credentials = file.ReadDictionary(f"{ConfigPath}/credentials.txt")
SocialMedia = file.ReadDictionary(f"{ConfigPath}/socialmedia.txt")
SoundList = file.ReadDictionary(f"{ConfigPath}/soundlist.txt")

# Bot configuration with username and his oauth token to get the permissions to send message from the account
# The idClient and ClientSecret are found in the application created on twitch developer        
BotName = Credentials["BOT_NICK"]
idClient = Credentials["CLIENT_ID"] 
ircToken = f'oauth:{Credentials["TOKEN"]}'
Prefix = Credentials["BOT_PREFIX"]
Channel = [Credentials["CHANNEL"]]
ClientSecret = Credentials["CLIENT_SECRET"]
RedirectUri = Credentials["REDIRECT_URI"]
scope = [
    'chat:read',
    'user:read:subscriptions',
    'chat:edit',
    'moderator:read:followers'
]

# Check if the Oauth Token of bot account is valid or hasn't expired yet.
ValidToken = Token.validation(Credentials["TOKEN"])

while ValidToken == False:
    print("Tu token no es valido. Ingresa al siguiente sitio para obtener un nuevo token:")
    token = Token(idClient, ClientSecret, scope, RedirectUri)
    NewToken = token.get_authorization()
    
    if token.validation(NewToken):
        Credentials["TOKEN"] = NewToken
        ircToken = f'oauth:{NewToken}'
        file.WriteDictionary(f"{ConfigPath}/credentials.txt", Credentials)
        print("Token validado")
        ValidToken = True

# Execute bot on loop
if __name__ == '__main__':
    botbonito = Bot(BotName, Prefix, Channel, Credentials)
    botbonito.run()