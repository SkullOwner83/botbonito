from twitchio.ext import commands
from playsound import playsound
import requests
import random

#Variables definition
List = []
Saved = False
DiscordLink = ""

#Bot configuration
BotName = "botbonito_"

bot = commands.Bot(
    irc_token = "",
    client_id = "",
    nick = BotName,
    prefix = "!",
    initial_channels = ["#"]
)

#Print message when the bot is ready
@bot.event
async def event_ready():
    print("Hi, I'm ready!")
    
#Check chat messages event
@bot.event
async def event_message(ctx):
    if ctx.author.name.lower() == BotName:
        return
    
    #Check if the message is a command
    await bot.handle_commands(ctx)

@bot.command(name="horario")
async def horario(ctx):
    await ctx.send(f"Hola @{ctx.author.name}! El horario es: Martes y Jueves a partir de las 8:00pm (Zona Horaria GMT-6). Domingo si hay oportunidad, a partir de la misma hora")     

@bot.command(name="discord")
async def discord(ctx):
    await ctx.send(f"{DiscordLink}")     
    

#Execute bot on loop
if __name__ == '__main__':
    bot.run()