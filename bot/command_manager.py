import random
from twitchio.ext import commands
from modules.api import Api
from myapp import MyApp

class CommandManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @MyApp.register_command("help")
    async def help(self, ctx):
        await ctx.send("¡Hola! Soy el bot bonito del Skull Owner y estoy aquí para ayudarte. Te envió los comandos que tengo disponibles para todos:")
        await ctx.send("!horario, !discord, !youtube, !instagram, !onlyfans, !gay, !memide, !leentro, !play, !speak, !following")

    
    @MyApp.register_command("schedule")
    async def schedule(self, ctx):
        await ctx.send(f"Hola @{ctx.author.name}! El horario es: Martes y Jueves a partir de las 8:00pm (Zona Horaria GMT-6). Domingo si hay oportunidad, a partir de la misma hora")
    
    @MyApp.register_command("onlyfans")
    async def onlyfans(ctx):
        await ctx.send(f"{ctx.author.name} se ha suscrito al onlyfans del Skull!")    

    @MyApp.register_command("gay")
    async def gay(self, ctx):
        await ctx.send("Quien? El Owl?")  

    @MyApp.register_command("memide")
    async def memide(ctx):
        size = random.randint(1, 50)
        await ctx.send(f"{ctx.author.name} le mide {size}cm")

    # Check if the user or a specified user follows the channel and since when
    @MyApp.register_command("following")
    async def following(self, ctx, *args):
        user_name = ctx.author.name
        channel_name = ctx.channel.name
        api = Api(self.bot.token, self.bot.client_id)

        # Check if there is text next to the comand and get the first word as an argument
        if len(args) > 0:
            user_name = args[0].lower()

        broadcaster_data = api.get_user(channel_name)
        user_data = api.get_user(user_name)

        if broadcaster_data is None:
            await ctx.send("No se ha encontrado el canal")
            return
    
        if user_data is None:
            await ctx.send("No se ha encontrado el usuario")
            return

        idBroadcaster = broadcaster_data['id']
        idUser = user_data['id']
        following_since = api.check_follow(idUser, idBroadcaster)
        
        if following_since != None:
            await ctx.send(f'{user_name} ha seguido a {channel_name} desde {following_since}')
        else:
            await ctx.send(f'{user_name} no sigue este canal :(')