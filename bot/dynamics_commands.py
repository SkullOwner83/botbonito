import re
import random
import asyncio
import pyperclip
from twitchio.ext import commands
from myapp import MyApp

class DynamicsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.giveaway_started = False
        self.feedback_started = False
        self.giveaway_list = []
        self.feedback_user_register = []
        self.feedback_list = {}
        MyApp.bind_commands(self)

    @MyApp.register_command("giveaway")
    async def giveaway_start(self, ctx, parameter):
        user = ctx.author.name
        parameter = parameter.lower() if parameter else None
        command_config = self.bot.default_commands.get('giveaway')
        entry_command_config = self.bot.default_commands.get('giveaway_entry')
        required_level = command_config['user_level']
        enable_command = command_config['enable']

        # Activate or desactivate the command
        if await self.bot.toggle_command(ctx, "giveaway", parameter): return

        if enable_command:
            if parameter == self.bot.config.get('help_word', 'help'):
                await ctx.send(f"Utiliza el comando !{command_config['name']} start, para iniciar una recopilación de participantes que se almacenarán en una lista. Los usuarios pueden entrar a la lista escribiendo el comando !leentro. Los usuarios deben seguir el canal para poder particiar.")
                await ctx.send(f"Utiliza el comando !{command_config['name']} finish, para concluir con la recopilación de participantes. Se creará un archivo de texto en la ruta {self.ProjectPath} con la lista de participantes. Adicionalmente se copiará la lista a tu portapapeles para mayor accesibilidad.")
                await ctx.send(f"Utiliza el comando !{command_config['name']} copyagain, para volver a copiar la lista de participantes en caso de que no encuentres el fichero o ya no se encuentre en el portapapeles.")
                return

            if self.bot.level_check(ctx, required_level):
                # Start the participant collection
                if parameter == "start":
                    if not self.giveaway_started:
                        self.giveaway_started = True
                        self.giveaway_list.clear()
                        await ctx.send(f"Iniciamos con la recopilación de participantes para el sorteo. Recuerda seguir el canal para poder participar. Para entrar escribe el comando !{entry_command_config['name']}")

                # Finish the give away, save the list in a text file and copy it tol the clipboard
                if parameter == "finish":
                    if self.giveaway_started:
                        await ctx.send("La lista para entrar al sorte, ha finalizado! Suerte a todos.")

                        with open(f"{self.ProjectPath}/Lista.txt", "w") as file:
                            for element in self.giveaway_list:
                                file.write(f"{element}\n")
                            
                        print(f"Se ha guardado la lista de participantes correctame en la ruta: {self.ProjectPath}")
                        list_string = '\n'.join(map(str, self.giveaway_list))
                        pyperclip.copy(list_string)
                        print(f"Se ha copiado la lista de participantes al portapapeles.")
                        self.giveaway_started = False
            else:
                await ctx.send(f"@{user}, no tienes el permiso para realizar la acción.")

    @MyApp.register_command("giveaway_entry")
    async def giveaway_entry(self, ctx, parameter: str = None):
        user = ctx.author.name
        parameter = parameter.lower() if parameter else None
        command_config = self.bot.default_commands.get('giveaway_entry')
        required_level = command_config['user_level']
        enable_command = command_config['enable']

        # Activate or desactivate the command
        if await self.bot.toggle_command(ctx, "giveaway_entry", parameter): return

        if enable_command:
            if self.bot.level_check(ctx, required_level):
                if self.giveaway_started == True:
                    if user not in self.giveaway_list:
                        self.giveaway_list.append(user)
                        await ctx.send(f"{user} se unió a la rifa!")
            else:
                await ctx.send(f"@{user}, no tienes el permiso para realizar la acción.")

    @MyApp.register_command("feedback")
    async def feedback(self, ctx, parameter):
        user = ctx.author.name
        parameter = parameter.lower() if parameter else None
        command_config = self.bot.default_commands.get('feedback')
        required_level = command_config['user_level']
        enable_command = command_config['enable']

        # Activate or desactivate the command
        if await self.bot.toggle_command(ctx, "feedback", parameter): return
        
        if enable_command:
            if self.bot.level_check(ctx, required_level):
                # Start the demos collection 
                if parameter == "start":
                    if self.feedback_started == False:
                        self.feedback_started = True
                        self.feedback_list.clear()
                        await ctx.send("Comenzamos con la recopilación de demos. Recuerda seguir el canal para poder participar, ademas de enviar un enlace de Youtube o Soundcloud. Para enviar tu demo, escribe el comando !demo, seguido del link de tu demo.")
                        return

                # Finish the demos collection. Choose a user at random and copy his link to the clipboard
                if parameter == "finish":
                    if self.feedback_started == True:
                        self.feedback_started = False
                        await ctx.send("La lista para poder enviar tu demo, ha finalizado! Ahora se escogera un demo de manera aleatoria. Suerte a todos!")
                        await asyncio.sleep(3)
                        user_winner = random.choice(list(self.feedback_list.keys()))
                        await ctx.send(f"El usuario elegido fue @{user_winner}. Se ha copiado su link en el portapapeles del streamer.")
                        print(f"Se ha copiado el link del demo al portapapeles.")
                        pyperclip.copy(self.feedback_list[user_winner])
                        return
            else:
                await ctx.send(f"@{user}, no tienes el permiso para realizar la acción.")

    @MyApp.register_command("send")
    async def send(self, ctx, parameter):
        user = ctx.author.name
        parameter = parameter.lower() if parameter else None
        command_config = self.bot.default_commands.get('send')
        required_level = command_config['user_level']
        enable_command = command_config['enable']
        youtube_patter = re.compile(r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+$")
        soundcloud_patter = re.compile(r'https?://soundcloud\.com/[\w-]+/[\w-]+')

        # Activate or desactivate the command
        if await self.bot.toggle_command(ctx, "send", parameter): return

        if enable_command:
            if self.bot.level_check(ctx, required_level):
                if self.feedback_started:
                    if youtube_patter.match(parameter) or soundcloud_patter.match(parameter):
                        if not user in self.feedback_list:
                            self.feedback_list[user] = parameter
                            await ctx.send(f"@{user} se añadió tu link a la lista.")
                        else:
                            await ctx.send(f"@{user} solo puedes enviar un demo!")
                    else:
                        await ctx.send(f"@{user} envia un enlace válido!")
            else:
                await ctx.send(f"@{user}, no tienes el permiso para realizar la acción.")