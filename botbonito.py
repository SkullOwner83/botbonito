from modules import get, file
from twitchio.ext import commands
from gtts import gTTS
import pygame
import pyperclip
import requests
import random
import time
import os
import asyncio
import re
import json

# Variables definition
ProjectPath = os.path.dirname(os.path.abspath(__file__))
ConfigPath = f"{ProjectPath}/config/"
SaveFilesPath = "D:/Desktop"
Credentials = {}

FrequencyMessagesTime = 1200
SndLastUsage = {}
SndCoolDown = 60
SpkLastUsage = {}
SpkCoolDown = 300

GiveAwayStarted = False
GiveAwayList = []
SendDemosStarted = False
DemosList = {}
UserDemoSended = []

DiscordLink = "https://discord.gg/prWCuWU5JM"
YoutubeLink = "https://www.youtube.com/@SkullOwnerGaming"
InstagramLink = "https://www.instagram.com/skullowner83/"

pygame.init()
pygame.mixer.init()

#Read the config file lines and get a data dictionary
Credentials = file.ReadDictionary(f"{ConfigPath}/credentials.txt")
SoundList = file.ReadDictionary(f"{ConfigPath}/soundlist.txt")

# Bot configuration with username and his oauth token to get the permissions to send message from the account
# The idClient and ClientSecret are found in the application created on twitch developer        
BotName = Credentials["BOT_NICK"]
idClient = Credentials["CLIENT_ID"] 
ircToken = Credentials["TOKEN"]
Prefix = Credentials["BOT_PREFIX"]
Channel = Credentials["CHANNEL"]
ClientSecret = Credentials["CLIENT_SECRET"]

# Check if the Oauth Token of bot account It hasn't expired yet.
ValidToken = get.TokenValidattion(ircToken)

while ValidToken == False:
    ircToken = input("Tu oauth token no es valido. Ingresa un token nuevo:")
    ValidToken = get.TokenValidattion(ircToken)
    
print(ValidToken)

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
    Channel = bot.get_channel(bot.initial_channels[0])
    await Channel.send("Hola, soy el bot bonito del Skull.")

    while True:
        await asyncio.sleep(FrequencyMessagesTime)
        await FrequentMessage()

# send random messages Frequently in the first bot Channel
async def FrequentMessage():
    MessagesList = ["¿Ya tomaste awua uwu?",
                    "Esta bonito tu stream mijito! uwu",
                    "¿Se estan pasando un buen rato? :3",
                    "Gracias a los que estan viendo el directo :D",
                    f"Recuerden entrar a mi discord: {DiscordLink}",
                    f"¿Ya te suscribiste a mi canal de youtube? {YoutubeLink}",
                    f"¿Ya me seguiste en instagram? {InstagramLink}"]

    Channel = bot.get_channel(bot.initial_channels[0])

    if Channel:
        random.seed(int(time.time()))
        Message = random.choice(MessagesList)
        await Channel.send(Message)

# Check if the user that sent the command, follows the channel
def FollowCheck(ctx):
    Url = "https://api.twitch.tv/helix/channels/followers"
    AppToken =  get.AppToken(idClient, ClientSecret)
    idBroadcaster = get.BroadcasterId(Channel, idClient, AppToken)
    idUser = get.UserId(ctx.author.name, idClient, AppToken)

    UriRedirect = "https:/localhost:300"
    Scope="user:read:follows"
    UserToken = f"https://id.twitch.tv/oauth2/authorize?client_id={idClient}&redirect_uri={UriRedirect}I&response_type=token&scope={Scope}"
    print(UserToken)

    url = 'https://api.twitch.tv/helix/channels/followers'
    params = {'broadcaster_id': {idBroadcaster}}

    headers = {
        'Authorization': 'Bearer ' + AppToken,
        'Client-Id': idClient
    }

    response = requests.get(url, params=params, headers=headers)

    # Imprime el código de estado y la respuesta del servidor
    print(f"Response ({response.status_code}): {response.json()}")
    return True #Para que funcionen las funciones en lo que se arregla esta

    
# Check if the user that sent the command, is the admin    
def AdminCheck(ctx):
    User = ctx.author.name

    if User == Channel:
        return True
    else:
        return False


# Check chat messages event
@bot.event
async def event_message(ctx):
    if ctx.author.name.lower() == BotName:
        return
    
    if "a" == ctx.content.lower():
        print(FollowCheck(ctx))

    # Check if the message is a command
    await bot.handle_commands(ctx)

@bot.command(name="help")
async def help(ctx):
    await ctx.send("¡Hola! Soy el bot bonito del Skull Owner y estoy aquí para ayudarte. Te envió los comandos que tengo disponibles para todos:")
    await ctx.send("!horario, !discord, !youtube, !instagram, !onlyfans, !gay, !memide, !leentro, !play, !speak")

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

# Another random commands
@bot.command(name="onlyfans")
async def onlyfans(ctx):
    await ctx.send(f"{ctx.author.name} se ha suscrito al onlyfans del Skull!")    

@bot.command(name="gay")
async def gay(ctx):
    print(GiveAwayStarted)
    await ctx.send("Quien? El Owl?")  

@bot.command(name="memide")
async def memide(ctx):
    Size = random.randint(1, 50)
    await ctx.send(f"{ctx.author.name} le mide {Size}cm")  

# Play sounds commands
@bot.command(name="play")
async def PlaySound(ctx, *args):
    global SndLastUsage
    global SndCoolDown
    global SoundList
    SoundListCommands = SoundList.keys()

    # Check if ther is text next to the comand and get the first word as an argument
    if len(args) > 0:
        Command = args[0].lower()
    
    # Check if the user has used a sound and is still on cooldown. Also, take the current time to set the next cooldown
    UserCoolDown = SndLastUsage.get(ctx.author.name, 0)
    CurrentTime = time.time()

    # Substract the cooldown time minus the time when the user used a sound minus the current time to get the rest time
    RestTime = SndCoolDown - (CurrentTime - UserCoolDown)

    # Check if the user's cooldown has already passed and the command is in the sound list to play the sound
    if RestTime <= 0:
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

# Speak text commands
@bot.command(name="speak")
async def Speak(ctx, *args):
    global SpkLastUsage
    global SpkCoolDown

     # Check if ther is text next to the comand and get the first word as an argument
    if len(args) > 0:
        Command = "".join(args).lower()

    # Check if the user has used a speaker and is still on cooldown. Also, take the current time to set the next cooldown
    SpkCoolDown = SpkLastUsage.get(ctx.author.name, 0)
    CurrentTime = time.time()

    # Substract the cooldown time minus the time when the user used a speaker minus the current time to get the rest time
    RestTime = SpkCoolDown - (CurrentTime - SpkCoolDown)

    # Check if the user cooldown has already passed to speak the text
    if RestTime <= 0:
        Speaker = gTTS(text=Command, lang="es", slow=False)
        Speaker.save("LastSpeech.mp3")
        Sound = pygame.mixer.Sound("LastSpeech.mp3")
        Sound.play()
        SpkLastUsage[ctx.author.name] = time.time()
    else: 
        await ctx.send(f"@{ctx.author.name} Espera un poco más para volver a usar el lector de texto. Tiempo restante ({round(RestTime)}s)")

# Send demos commands
@bot.command(name="senddemo")    
async def SendDemo(ctx, *args):
    global SendDemosStarted
    global DemosList

    # Check if ther is text next to the comand and get the first word as an argument
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

    # Check if ther is text next to the comand and get the first word as an argument
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

    # Check if ther is text next to the comand and get the first word as an argument
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


@bot.command(name="leentro")
async def GiveAway(ctx):
    User = ctx.author.name
    isFollow = FollowCheck(ctx)
    global GiveAwayStarted
    global GiveAwayList

    if GiveAwayStarted == True:
        if isFollow == True:
            if User not in GiveAwayList:
                GiveAwayList.append(User)
                await ctx.send(f"{User} se unió a la rifa!")            
                print(f"Se añadió el nombre de {ctx.author.name} a la lista!")
        else:
            await ctx.send(f"{User}, debes seguir al skull para poder participar.")
    else:
        await ctx.send(f"{User} eh perate. ¿A dónde le quieres entrar?")

# Execute bot on loop
if __name__ == '__main__':
    bot.run()