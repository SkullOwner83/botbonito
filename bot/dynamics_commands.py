import re
import random
import asyncio
import pyperclip
from typing import Optional
from twitchio.ext import commands
from twitchio.ext.commands import Context
from models.appconfig import AppConfig
from models.commands import CommandConfig
from services.service_locator import ServiceLocator
from services.commands_manager import CommandsManager
from myapp import MyApp

class DynamicsCommands(commands.Cog):
    def __init__(self, bot: commands.Bot, app_config: AppConfig) -> None:
        self.bot = bot
        self.app_config = app_config
        commands_manager: CommandsManager = ServiceLocator.get('commands')
        self.default_commands = commands_manager.default_commands
        self.giveaway_started = False
        self.feedback_started = False
        self.giveaway_list: list[str] = []
        self.feedback_user_register: list[str] = []
        self.feedback_list: dict[str, str] = {}
        MyApp.bind_commands(self)

    @MyApp.register_command("giveaway")
    async def giveaway_start(self, ctx: Context, parameter: str) -> None:
        parameter = parameter.lower() if parameter else None
        command_config: CommandConfig = self.default_commands.get('giveaway')
        entry_command: CommandConfig = self.default_commands.get('giveaway_entry')

        if await self.bot.check_command_access(ctx, 'giveaway'):
            if parameter == self.app_config.help_word:
                await ctx.send(f"Utiliza el comando !{command_config.name} start, para iniciar una recopilación de participantes que se almacenarán en una lista. Los usuarios pueden entrar a la lista escribiendo el comando !leentro. Los usuarios deben seguir el canal para poder particiar.")
                await ctx.send(f"Utiliza el comando !{command_config.name} finish, para concluir con la recopilación de participantes. Se creará un archivo de texto en la ruta {self.ProjectPath} con la lista de participantes. Adicionalmente se copiará la lista a tu portapapeles para mayor accesibilidad.")
                await ctx.send(f"Utiliza el comando !{command_config.name} copyagain, para volver a copiar la lista de participantes en caso de que no encuentres el fichero o ya no se encuentre en el portapapeles.")
                return

            # Start the participant collection
            if parameter == self.app_config.start_word:
                if not self.giveaway_started:
                    self.giveaway_started = True
                    self.giveaway_list.clear()
                    await ctx.send(f"Iniciamos con la recopilación de participantes para el sorteo. Recuerda seguir el canal para poder participar. Para entrar escribe el comando !{entry_command.name}")

            # Finish the give away, save the list in a text file and copy it tol the clipboard
            if parameter == self.app_config.finish_word:
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

    @MyApp.register_command("giveaway_entry")
    async def giveaway_entry(self, ctx: Context, parameter: Optional[str] = None) -> None:
        user = ctx.author.name  
        parameter = parameter.lower() if parameter else None

        if await self.bot.check_command_access(ctx, 'giveaway_entry'):
            if self.giveaway_started:
                if user not in self.giveaway_list:
                    self.giveaway_list.append(user)
                    await ctx.send(f"{user} se unió a la rifa!")

    @MyApp.register_command("feedback")
    async def feedback(self, ctx: Context, parameter: str) -> None:
        parameter = parameter.lower() if parameter else None

        if await self.bot.check_command_access(ctx, 'feedback'): 
            # Start the demos collection 
            if parameter == self.app_config.start_word:
                if self.feedback_started == False:
                    self.feedback_started = True
                    self.feedback_list.clear()
                    await ctx.send("Comenzamos con la recopilación de demos. Recuerda seguir el canal para poder participar, ademas de enviar un enlace de Youtube o Soundcloud. Para enviar tu demo, escribe el comando !demo, seguido del link de tu demo.")

            # Finish the demos collection. Choose a user at random and copy his link to the clipboard
            if parameter == self.app_config.finish_word:
                if self.feedback_started == True:
                    self.feedback_started = False
                    await ctx.send("La lista para poder enviar tu demo, ha finalizado! Ahora se escogera un demo de manera aleatoria. Suerte a todos!")
                    await asyncio.sleep(3)
                    user_winner = random.choice(list(self.feedback_list.keys()))
                    await ctx.send(f"El usuario elegido fue @{user_winner}. Se ha copiado su link en el portapapeles del streamer.")
                    print(f"Se ha copiado el link del demo al portapapeles.")
                    pyperclip.copy(self.feedback_list[user_winner])

    @MyApp.register_command("send")
    async def send(self, ctx: Context, parameter: str) -> None:
        user = ctx.author.name
        parameter = parameter.lower() if parameter else None
        youtube_patter = re.compile(r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+$")
        soundcloud_patter = re.compile(r'https?://soundcloud\.com/[\w-]+/[\w-]+')

        if await self.bot.check_command_access(ctx, 'send'):
            if self.feedback_started:
                if youtube_patter.match(parameter) or soundcloud_patter.match(parameter):
                    if not user in self.feedback_list:
                        self.feedback_list[user] = parameter
                        await ctx.send(f"@{user} se añadió tu link a la lista.")
                    else:
                        await ctx.send(f"@{user} solo puedes enviar un demo!")
                else:
                    await ctx.send(f"@{user} envia un enlace válido!")