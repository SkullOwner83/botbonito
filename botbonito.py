from twitchio.ext import commands
from playsound import playsound
import requests
import random
import time
import os
import asyncio

# Variables definition
ProjectPath= os.path.dirname(os.path.abspath(__file__))
SaveFilesPath = "D:/Desktop"

FrequencyMessagesTime = 300
DiscordLink = "https://discord.gg/prWCuWU5JM"
YoutubeLink = "https://www.youtube.com/@SkullOwnerGaming"
InstagramLink = "https://www.instagram.com/skullowner83/"
GiveAwayStarted = False
GiveAwayList = []

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

    while True:
        await FrequentMessage()
        await asyncio.sleep(FrequencyMessagesTime)

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
    await ctx.send("!horario, !discord, !onlyfans, !gay, !leentro")

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

# Start, finish and Save username in a list for the raffle when it starts
@bot.command(name="giveawaystart")
async def giveawaystart(ctx):
    global GiveAwayStarted

    if GiveAwayStarted == False and AdminCheck(ctx):
        GiveAwayStarted = True
        await ctx.send("Iniciamos con la recopilación de participantes para el sorteo. Recuerda seguirme para poder participar. Para entrar escribe el comando !leentro")

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
        else:
            await ctx.send(f"{User}, debes seguir al skull para poder participar.")
    else:
        await ctx.send(f"{User} eh perate. ¿A dónde le quieres entrar?")

@bot.command(name="giveawayfinish")
async def giveawayfinish(ctx):
    global GiveAwayStarted
    global GiveAwayList

    # Check if the admin sent the command to finish the giveaway and save the list in one file text
    if GiveAwayStarted == True and AdminCheck(ctx):
        await ctx.send("La lista para entrar al sorte, ha finalizado! Suete a todos.")

        with open(f"{SaveFilesPath}/Lista.txt", "w") as File:
            for Element in GiveAwayList:
                File.write(f"{Element}\n")
            
        print(f"Se ha guardado la lista de participantes correctame en la ruta: {SaveFilesPath}")
        GiveAwayStarted = False

# Execute bot on loop
if __name__ == '__main__':
    bot.run()