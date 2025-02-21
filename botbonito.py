import os
import re
import time
import asyncio
import random
import pygame
import pyperclip
from twitchio.ext import commands
from gtts import gTTS
from modules import file
from modules.api import Api
from modules.token import Token

# Load config and variable values from files
ProjectPath = os.path.dirname(os.path.abspath(__file__))
ConfigPath = f"{ProjectPath}/config/"
SaveFilesPath = "D:/Desktop"

Credentials = file.ReadDictionary(f"{ConfigPath}/credentials.txt")
SocialMedia = file.ReadDictionary(f"{ConfigPath}/socialmedia.txt")
SoundList = file.ReadDictionary(f"{ConfigPath}/soundlist.txt")

# Variable configuration
FrequencyMessagesTime = 1200
PlaySoundEnable = True
SpeakEnable = True
SndLastUsage = {}
SpkLastUsage = {}
SndCoolDown = 60
SpkCoolDown = 180
SpkMaxLen = 200

GiveAwayStarted = False
SendDemosStarted = False
GiveAwayList = []
UserDemoSended = []
DemosList = {}

pygame.init()
pygame.mixer.init()

# Bot configuration with username and his oauth token to get the permissions to send message from the account
# The idClient and ClientSecret are found in the application created on twitch developer        
BotName = Credentials["BOT_NICK"]
idClient = Credentials["CLIENT_ID"] 
ircToken = f'oauth:{Credentials["TOKEN"]}'
Prefix = Credentials["BOT_PREFIX"]
Channel = Credentials["CHANNEL"]
ClientSecret = Credentials["CLIENT_SECRET"]
RedirectUri = Credentials["REDIRECT_URI"]
scope = [
    "chat:read",
    "chat:edit",
    "user:read:subscriptions",
    "moderator:read:followers"
]

DiscordLink = SocialMedia["Discord"]
YoutubeLink = SocialMedia["Youtube"]
InstagramLink = SocialMedia["Instagram"]
FacebookLink = SocialMedia["Facebook"]
TikTokLink = SocialMedia["TikTok"]

MessagesList = [
    "¿Ya tomaste awua uwu?",
    "Esta bonito tu stream mijito! uwu",
    "¿Se estan pasando un buen rato? :3",
    "Gracias a los que estan viendo el directo :D",
    f"Recuerden entrar a mi discord: {DiscordLink}",
    f"¿Ya te suscribiste a mi canal de youtube? {YoutubeLink}",
    f"¿Ya me seguiste en instagram? {InstagramLink}",
    "Usa !help para ver la lista de comandos disponibles. :D"
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

# Creation of bot with previous configuration 
bot = commands.Bot(
    irc_token = ircToken,
    client_id = idClient,
    nick = BotName,
    prefix = Prefix,
    initial_channels = [Channel]
)

# Print message when the bot is ready
@bot.event
async def event_ready():
    print("Hi, I'm ready!")
    
    for channel_name in bot.initial_channels:
        channel = bot.get_channel(channel_name)

        if channel:
            await channel.send("Hola, soy el bot bonito del Skull.")

    asyncio.create_task(send_frequent_messages())

# send random messages Frequently in the first bot Channel
async def send_frequent_messages():
    while True:
        await asyncio.sleep(FrequencyMessagesTime)
        Channel = bot.get_channel(bot.initial_channels[0])
        
        if Channel:
            random.seed(int(time.time()))
            Message = random.choice(MessagesList)
            await Channel.send(Message)
 
# Check if the user that sent the command, is the admin    
def AdminCheck(ctx):
    User = ctx.author.name
    return True if User == Channel else False

# Check chat messages event
@bot.event
async def event_message(ctx):
    if ctx.author is None or ctx.author.name == BotName:
        return

    # Check if the message is a command
    ctx.content = ctx.content.lower() 
    await bot.handle_commands(ctx)

@bot.command(name="help")
async def help(ctx):
    await ctx.send("¡Hola! Soy el bot bonito del Skull Owner y estoy aquí para ayudarte. Te envió los comandos que tengo disponibles para todos:")
    await ctx.send("!horario, !discord, !youtube, !instagram, !onlyfans, !gay, !memide, !leentro, !play, !speak, !following")

# Show the stream schedule command
@bot.command(name="horario")
async def schedule(ctx):
    await ctx.send(f"Hola @{ctx.author.name}! El horario es: Martes y Jueves a partir de las 8:00pm (Zona Horaria GMT-6). Domingo si hay oportunidad, a partir de la misma hora")     

# Show social media commads
@bot.command(name="discord")
async def discord(ctx):
    await ctx.send(f"{DiscordLink}")     

@bot.command(name="youtube")
async def discord(ctx):
    await ctx.send(f"{YoutubeLink}")     

@bot.command(name="instagram")
async def discord(ctx):
    await ctx.send(f"{InstagramLink}")

@bot.command(name="facebook")
async def discord(ctx):
    await ctx.send(f"{FacebookLink}")

@bot.command(name="tiktok")
async def discord(ctx):
    await ctx.send(f"{TikTokLink}")

# Another random commands
@bot.command(name="onlyfans")
async def onlyfans(ctx):
    await ctx.send(f"{ctx.author.name} se ha suscrito al onlyfans del Skull!")    

@bot.command(name="gay")
async def gay(ctx):
    print(GiveAwayStarted)
    await ctx.send("Quien? El Owl?")  

@bot.command(name="memide")
async def memide(ctx, *args):
    Size = random.randint(1, 50)
    await ctx.send(f"{ctx.author.name} le mide {Size}cm")

# Check if the user or a specified user follows the channel and since when
@bot.command(name="following")
async def follow(ctx, *args):
    user_name = ctx.author.name
    api = Api(Credentials["TOKEN"], idClient)

    # Check if there is text next to the comand and get the first word as an argument
    if len(args) > 0:
        user_name = args[0].lower()

    broadcaster_data = api.get_user(Channel)
    user_data = api.get_user(user_name)

    if broadcaster_data is None:
        await ctx.send("No se ha encontrado el canal")
        return
 
    if user_data is None:
        await ctx.send("No se ha encontrado el usuario")
        return

    idBroadcaster = broadcaster_data.get("id")
    idUser = user_data.get("id")
    following_since = api.check_follow(idUser, idBroadcaster)
    
    if following_since != None:
        await ctx.send(f'{user_name} ha seguido a {Channel} desde {following_since}')
    else:
        await ctx.send(f'{user_name} no sigue este canal :(')

# Play sounds commands
@bot.command(name="play")
async def PlaySound(ctx, *args):
    global PlaySoundEnable
    global SndLastUsage
    global SndCoolDown
    global SoundList
    UserCoolDown = 0
    SoundListCommands = SoundList.keys()

    # Check if ther is text next to the comand and get the first word as an argument
    if len(args) > 0:
        Command = args[0].lower()

     # Activate or desactivate the play sound command
    if AdminCheck(ctx):
        if Command == "enable":
            PlaySoundEnable = True
            await ctx.send(f"Se ha activado el comando play sound.")
            return
        
        if Command == "disable":
            PlaySoundEnable = False
            await ctx.send(f"Se ha desactivado el comando play sound.")
            return
    
    if PlaySoundEnable == True:
        # Check if the user has used a sound and is still on cooldown. Also, take the current time to set the next cooldown
        UserCoolDown = SndLastUsage.get(ctx.author.name, 0)
        CurrentTime = time.time()

        # Substract the cooldown time minus the time when the user used a sound minus the current time to get the rest time
        RestTime = SndCoolDown - (CurrentTime - UserCoolDown)

        # Check if the user's cooldown has already passed and the command is in the sound list to play the sound
        if RestTime <= 0 or AdminCheck(ctx):
            if Command in SoundList:
                Sound = pygame.mixer.Sound(SoundList[Command])

                # Play the sound specified and update the time on the user cooldown register
                Sound.play()
                SndLastUsage[ctx.author.name] = time.time()
            else:
                if Command == "help":
                    await ctx.send(f"Para reproducir un sonido, escribe el comando !play, seguido del nombre de uno de los siguientes sonidos (!play holi): {list(SoundListCommands)}")
        else:
            await ctx.send(f"@{ctx.author.name} Espera un poco más para volver a usar un sonido. Tiempo restante ({round(RestTime)})")
    else:
        await ctx.send(f"@{ctx.author.name} Lo siento, el comando play sound esta desactivado :(")

# Speak text commands
@bot.command(name="speak")
async def Speak(ctx, *args):
    global SpeakEnable
    global SpkLastUsage
    global SpkCoolDown
    UserCoolDown = 0

     # Check if there is text next to the comand and get the first word as an argument
    if len(args) > 0:
        Command = "".join(args).lower()

    # Check if the user has used a speaker and is still on cooldown. Also, take the current time to set the next cooldown
    UserCoolDown = SpkLastUsage.get(ctx.author.name, 0)
    CurrentTime = time.time()

    # Substract the cooldown time minus the time when the user used a speaker minus the current time to get the rest time
    RestTime = SpkCoolDown - (CurrentTime - UserCoolDown)

    # Activate or desactivate the speak command
    if AdminCheck(ctx):
        if Command == "enable":
            SpeakEnable = True
            await ctx.send(f"Se ha activado el comando speak.")
            return
        
        if Command == "disable":
            SpeakEnable = False
            await ctx.send(f"Se ha desactivado el comando speak.")
            return

    if SpeakEnable == True:
        if len(Command) <= SpkMaxLen:
            # Check if the user cooldown has already passed to speak the text
            if RestTime <= 0 or AdminCheck(ctx):
                Speaker = gTTS(text=Command, lang="es", slow=False)
                Speaker.save("LastSpeech.mp3")
                Sound = pygame.mixer.Sound("LastSpeech.mp3")
                Sound.play()
                SpkLastUsage[ctx.author.name] = time.time()
            else: 
                await ctx.send(f"@{ctx.author.name} Espera un poco más para volver a usar el lector de texto. Tiempo restante ({round(RestTime)}s)")
        else:
            await ctx.send(f"@{ctx.author.name} Has escrito un mensaje demasiado largo. El máximo de caracteres es {SpkMaxLen} caracteres")
    else:
        await ctx.send(f"@{ctx.author.name} Lo siento, el comando speak esta desactivado :(")

# Send demos commands
@bot.command(name="senddemo")    
async def SendDemo(ctx, *args):
    global SendDemosStarted
    global DemosList

    # Check if there is text next to the comand and get the first word as an argument
    if len(args) > 0:
        Command = args[0].lower()
    
    if AdminCheck(ctx):
        # Start the demos collection 
        if Command == "start":
            if SendDemosStarted == False:
                SendDemosStarted = True
                DemosList.clear()
                await ctx.send("Comenzamos con la recopilación de demos. Recuerda seguirme para poder participar, ademas de enviar un enlace de Youtube o Soundcloud. Para enviar tu demo, escribe el comando !demo, seguido del link de tu demo.")

        # Finish the demos collection. Choose a user at random and copy his link to the clipboard
        if Command == "finish":
            if SendDemosStarted == True:
                SendDemosStarted = False
                await ctx.send("La lista para poder enviar tu demo, ha finalizado! Ahora se escogera un demo de manera aleatoria. Suerte a todos!")
                await asyncio.sleep(3)
                UserWinner = random.choice(list(DemosList.keys()))
                await ctx.send(f"El usuario elegido fue @{UserWinner}. Se ha copiado su link en el portapapeles del streamer.")
                print(f"Se ha copiado el link del demo al portapapeles.")
                pyperclip.copy(DemosList[UserWinner])            

@bot.command(name="demo")
async def Demo(ctx, *args):
    YoutubePattern = re.compile(r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+$")
    SouncloudPattern = re.compile(r'https?://soundcloud\.com/[\w-]+/[\w-]+')
    global SendDemosStarted
    global DemosList

    # Check if there is text next to the comand and get the first word as an argument
    if len(args) > 0:
        Link = args[0].lower()

    # Check if the argument is a linka and is valid
    if SendDemosStarted == True:
        if YoutubePattern.match(Link) or SouncloudPattern.match(Link):
            if not ctx.author.name in DemosList:
                DemosList[ctx.author.name] = Link
                print(f"Se añadió el demo de {ctx.author.name} a la lista!")
            else:
                await ctx.send(f"@{ctx.author.name} solo puedes enviar un demo!")
        else:
            await ctx.send(f"@{ctx.author.name} envia un enlace válido!")
    else:
        await ctx.send(f"@{ctx.author.name} eh perate! Todavía no puedes enviar un demo!")

# Give away commands
@bot.command(name="giveaway")
async def giveawaystart(ctx, *args):
    global GiveAwayStarted
    global GiveAwayList

    # Check if there is text next to the comand and get the first word as an argument
    if len(args) > 0:
        Command = args[0].lower()
    
    if AdminCheck(ctx):
        # Start the participant collection 
        if Command == "start":
            if GiveAwayStarted == False:
                GiveAwayStarted = True
                GiveAwayList.clear()
                await ctx.send("Iniciamos con la recopilación de participantes para el sorteo. Recuerda seguirme para poder participar. Para entrar escribe el comando !leentro")

        # Finish the give away, save the list in a text file and copy it tol the clipboard
        if Command == "finish":
            if GiveAwayStarted == True:
                await ctx.send("La lista para entrar al sorte, ha finalizado! Suete a todos.")

                with open(f"{SaveFilesPath}/Lista.txt", "w") as File:
                    for Element in GiveAwayList:
                        File.write(f"{Element}\n")
                    
                print(f"Se ha guardado la lista de participantes correctame en la ruta: {SaveFilesPath}")
                ListString = '\n'.join(map(str, GiveAwayList))
                pyperclip.copy(ListString)
                print(f"Se ha copiado la lista de participantes al portapapeles.")
                GiveAwayStarted = False
        
        if Command == "help":
            await ctx.send("Utiliza el comando !giveaway start, para iniciar una recopilación de participantes que se almacenarán en una lista. Los usuarios pueden entrar a la lista escribiendo el comando !leentro. Los usuarios deben seguir el canal para poder particiar.")
            await ctx.send(f"Utiliza el comando !giveaway finish, para concluir con la recopilación de participantes. Se creará un archivo de texto en la ruta {SaveFilesPath} con la lista de participantes. Adicionalmente se copiará la lista a tu portapapeles para mayor accesibilidad.")
            await ctx.send(f"Utiliza el comando !giveaway copyagain, para volver a copiar la lista de participantes en caso de que no encuentres el fichero o ya no se encuentre en el portapapeles.")

@bot.command(name="enter")
async def GiveAway(ctx):
    User = ctx.author.name
    global GiveAwayStarted
    global GiveAwayList

    if GiveAwayStarted == True:
        if User not in GiveAwayList:
            GiveAwayList.append(User)
            await ctx.send(f"{User} se unió a la rifa!")
    else:
        await ctx.send(f"{User} eh perate. ¿A dónde le quieres entrar?")

# Execute bot on loop
if __name__ == '__main__':
    bot.run()