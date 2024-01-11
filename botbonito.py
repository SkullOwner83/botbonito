from twitchio.ext import commands
from playsound import playsound
import requests
import random
import time
import os
import asyncio

# Variables definition
ProjectDirectory = os.path.dirname(os.path.abspath(__file__))
FrequencyMessagesTime = 300
DiscordLink = "https://discord.gg/prWCuWU5JM"
YoutubeLink = "https://www.youtube.com/@SkullOwnerGaming"
InstagramLink = "https://www.instagram.com/skullowner83/"
RaffleList = []

#Read the config file lines and split each line to save data in the dictionary
with open(f"{ProjectDirectory}/config.txt", "r") as File:
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
                    "Gracias a los que estan viendo el directo ^_^",
                    f"Recuerden entrar a mi discord: {DiscordLink}",
                    f"Ya te suscribiste a mi canal de youtube? {YoutubeLink}",
                    f"Ya me seguiste en instagram? {InstagramLink}"]

    Channel = bot.get_channel(bot.initial_channels[0])

    if Channel:
        random.seed(int(time.time()))
        Message = random.choice(MessagesList)
        await Channel.send(Message)
    
# Check chat messages event
@bot.event
async def event_message(ctx):
    if ctx.author.name.lower() == BotName:
        return
    
    # Check if the message is a command
    await bot.handle_commands(ctx)

# Show the stream schedule command
@bot.command(name="horario")
async def horario(ctx):
    await ctx.send(f"Hola @{ctx.author.name}! El horario es: Martes y Jueves a partir de las 8:00pm (Zona Horaria GMT-6). Domingo si hay oportunidad, a partir de la misma hora")     

@bot.command(name="discord")
async def discord(ctx):
    await ctx.send(f"{DiscordLink}")     

@bot.command(name="onlyfans")
async def onlyfans(ctx):
    await ctx.send(f"{ctx.author.name} se ha suscrito al onlyfans del Skull!")    

@bot.command(name="gay")
async def gay(ctx):
    await ctx.send("Quien? El Owl?")         

# Execute bot on loop
if __name__ == '__main__':
    bot.run()