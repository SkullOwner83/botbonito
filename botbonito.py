from twitchio.ext import commands
from playsound import playsound
import pyperclip
import requests
import random
import time
import os
import asyncio
import re

# Variables definition
ProjectPath= os.path.dirname(os.path.abspath(__file__))
SaveFilesPath = "D:/Desktop"
GiveAwayStarted = False
GiveAwayList = []
SendDemosStarted = False
DemosList = {}
UserDemoSended = []

FrequencyMessagesTime = 1200
DiscordLink = "https://discord.gg/prWCuWU5JM"
YoutubeLink = "https://www.youtube.com/@SkullOwnerGaming"
InstagramLink = "https://www.instagram.com/skullowner83/"

#Read the config file lines and split each line to save data in the dictionary
with open(f"{ProjectPath}/config.txt", "r") as File:
    Lines = File.readlines()
    Config = {}

    for Line in Lines:
        Parts = Line.replace("\n","").split("=")
        Config[Parts[0]] = Parts[1]

# Bot configuration
BotName = Config["BOT_NICK"]
idClient = Config["CLIENT_ID"]
ircToken = Config["TOKEN"]
Prefix = Config["BOT_PREFIX"]
Channel = Config["CHANNEL"]

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
    MessagesList = ["Ya tomaste awua uwu?",
                    "Esta bonito tu stream mijito! uwu",
                    "Se estan pasando un buen rato? :3",
                    "Gracias a los que estan viendo el directo :D",
                    f"Recuerden entrar a mi discord: {DiscordLink}",
                    f"Ya te suscribiste a mi canal de youtube? {YoutubeLink}",
                    f"Ya me seguiste en instagram? {InstagramLink}"]

    Channel = bot.get_channel(bot.initial_channels[0])

    if Channel:
        random.seed(int(time.time()))
        Message = random.choice(MessagesList)
        await Channel.send(Message)

# Check if the user that sent the command, follows the channel
def FollowCheck(ctx):
     # Call twitch API to get the user data
    ChannelName = ctx.channel.name
    Url = f"https://api.twitch.tv/helix/users/follows?from_id={ctx.author.id}&to_name={ChannelName}"

    Headers = {
        "Client-ID": idClient,
        "Authorization": "Bearer " + ircToken
    }

    Response = requests.get(Url, headers=Headers)

    # if the response was successful (code: 200), check if the user that send the command, is follower
    if Response.status_code == 200:
        Data = Response.json()
        Follows = Data.get("total", 0)

        if Follows > 0:
            return True
        else:
            return False
    else:
        print(f"Error: {Response}! Algo salio mal.")
        return False
    
# Check if the user that sent the command, is the admin    
def AdminCheck(ctx):
    User = ctx.author.name

    if User == "skull_owner":
        return True
    else:
        return False


# Check chat messages event
@bot.event
async def event_message(ctx):
    if ctx.author.name.lower() == BotName:
        return
    
    # Check if the message is a command
    await bot.handle_commands(ctx)

@bot.command(name="help")
async def help(ctx):
    await ctx.send("!horario, !discord, !onlyfans, !gay, !memide, !leentro")

# Show the stream schedule command
@bot.command(name="horario")
async def horario(ctx):
    await ctx.send(f"Hola @{ctx.author.name}! El horario es: Martes y Jueves a partir de las 8:00pm (Zona Horaria GMT-6). Domingo si hay oportunidad, a partir de la misma hora")     

# Show social media commads
@bot.command(name="discord")
async def discord(ctx):
    await ctx.send(f"{DiscordLink}")     

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
    Size = random.randint(1, 100)
    await ctx.send(f"{ctx.author.name} le mide {Size}cm")  

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

@bot.command(name="leentro")
async def GiveAway(ctx):
    User = ctx.author.name
    isFollow = FollowCheck(ctx)
    global GiveAwayStarted
    global GiveAwayList

    if GiveAwayStarted == True:
        if isFollow == False:
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