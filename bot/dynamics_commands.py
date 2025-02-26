import re
import random
import asyncio
import pyperclip
from twitchio.ext import commands

class DynamicsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.give_away_started = False
        self.send_demo_started = False
        self.give_away_list = []
        self.user_demo_list = []
        self.demos_list = {}

    # Give away commands
    @commands.command(name="giveaway")
    async def giveawaystart(self, ctx, *args):
        # Check if there is text next to the comand and get the first word as an argument
        if len(args) > 0:
            command = args[0].lower()
        
        if self.bot.admin_check(ctx):
            # Start the participant collection 
            if command == "start":
                if self.give_away_started == False:
                    self.give_away_started = True
                    self.give_away_list.clear()
                    await ctx.send("Iniciamos con la recopilación de participantes para el sorteo. Recuerda seguirme para poder participar. Para entrar escribe el comando !leentro")

            # Finish the give away, save the list in a text file and copy it tol the clipboard
            if command == "finish":
                if self.give_away_started == True:
                    await ctx.send("La lista para entrar al sorte, ha finalizado! Suerte a todos.")

                    with open(f"{self.ProjectPath}/Lista.txt", "w") as file:
                        for element in self.give_away_list:
                            file.write(f"{element}\n")
                        
                    print(f"Se ha guardado la lista de participantes correctame en la ruta: {self.ProjectPath}")
                    list_string = '\n'.join(map(str, self.give_away_list))
                    pyperclip.copy(list_string)
                    print(f"Se ha copiado la lista de participantes al portapapeles.")
                    self.give_away_started = False
            
        if command == "help":
            await ctx.send("Utiliza el comando !giveaway start, para iniciar una recopilación de participantes que se almacenarán en una lista. Los usuarios pueden entrar a la lista escribiendo el comando !leentro. Los usuarios deben seguir el canal para poder particiar.")
            await ctx.send(f"Utiliza el comando !giveaway finish, para concluir con la recopilación de participantes. Se creará un archivo de texto en la ruta {self.ProjectPath} con la lista de participantes. Adicionalmente se copiará la lista a tu portapapeles para mayor accesibilidad.")
            await ctx.send(f"Utiliza el comando !giveaway copyagain, para volver a copiar la lista de participantes en caso de que no encuentres el fichero o ya no se encuentre en el portapapeles.")

    @commands.command(name="enter")
    async def GiveAway(self, ctx):
        user = ctx.author.name

        if self.give_away_started == True:
            if user not in self.give_away_list:
                self.give_away_list.append(user)
                await ctx.send(f"{user} se unió a la rifa!")
        else:
            await ctx.send(f"{user} eh perate. ¿A dónde le quieres entrar?")

    # Send demos commands
    @commands.command(name="senddemo")    
    async def send_demo(self, ctx, *args):
        # Check if there is text next to the comand and get the first word as an argument
        if len(args) > 0:
            command = args[0].lower()
        
        if self.bot.admin_check(ctx):
            # Start the demos collection 
            if command == "start":
                if self.send_demo_started == False:
                    self.send_demo_started = True
                    self.demos_list.clear()
                    await ctx.send("Comenzamos con la recopilación de demos. Recuerda seguir el canal para poder participar, ademas de enviar un enlace de Youtube o Soundcloud. Para enviar tu demo, escribe el comando !demo, seguido del link de tu demo.")

            # Finish the demos collection. Choose a user at random and copy his link to the clipboard
            if command == "finish":
                if self.send_demo_started == True:
                    self.send_demo_started = False
                    await ctx.send("La lista para poder enviar tu demo, ha finalizado! Ahora se escogera un demo de manera aleatoria. Suerte a todos!")
                    await asyncio.sleep(3)
                    user_winner = random.choice(list(self.demos_list.keys()))
                    await ctx.send(f"El usuario elegido fue @{user_winner}. Se ha copiado su link en el portapapeles del streamer.")
                    print(f"Se ha copiado el link del demo al portapapeles.")
                    pyperclip.copy(self.demos_list[user_winner])            

    @commands.command(name="demo")
    async def Demo(self, ctx, *args):
        youtube_patter = re.compile(r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+$")
        soundcloud_patter = re.compile(r'https?://soundcloud\.com/[\w-]+/[\w-]+')

        # Check if there is text next to the comand and get the first word as an argument
        if len(args) > 0:
            Link = args[0].lower()

        # Check if the argument is a linka and is valid
        if self.send_demo_started == True:
            if youtube_patter.match(Link) or soundcloud_patter.match(Link):
                if not ctx.author.name in self.demos_list:
                    self.demos_list[ctx.author.name] = Link
                    print(f"Se añadió el demo de {ctx.author.name} a la lista!")
                else:
                    await ctx.send(f"@{ctx.author.name} solo puedes enviar un demo!")
            else:
                await ctx.send(f"@{ctx.author.name} envia un enlace válido!")
        else:
            await ctx.send(f"@{ctx.author.name} eh perate! Todavía no puedes enviar un demo!")