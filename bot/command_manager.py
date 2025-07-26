from twitchio.ext import commands
from twitchio.ext.commands import Context
from models.appconfig import AppConfig
from services.commands_manager import CommandsManager
from services.service_locator import ServiceLocator
from utilities.api import Api
from utilities.enums import ResponseType
from myapp import MyApp

class CommandManager(commands.Cog):
    def __init__(self, bot: commands.Bot, app_config: AppConfig, credentials: dict[str, str]) -> None:
        self.bot = bot
        self.app_config = app_config
        self.credentials = credentials
        commands_manager: CommandsManager = ServiceLocator.get('commands')
        self.default_commands = commands_manager.default_commands
        self.custom_commands = commands_manager.custom_commands
        self.custom_alias = commands_manager.custom_alias
        MyApp.bind_commands(self)

    @MyApp.register_command("help")
    async def help(self, ctx: Context) -> None:
        if await self.bot.check_command_access(ctx, 'help'):
            await ctx.send("¡Hola! Soy el bot bonito del Skull Owner y estoy aquí para ayudarte. Te envió los comandos que tengo disponibles. Si requieres mayor información, puedes escribir el comando seguido de help (!comando help):")
            await ctx.send(f"!{', !'.join(self.default_commands)}")

    @MyApp.register_command("schedule")
    async def schedule(self, ctx: Context) -> None:
        if await self.bot.check_command_access(ctx, 'schedule'):
            await ctx.send(f"Hola @{ctx.author.name}! El horario es: Martes y Jueves a partir de las 8:00pm (Zona Horaria GMT-6). Domingo si hay oportunidad, a partir de la misma hora")

    # Check if the user or a specified user follows the channel and since when
    @MyApp.register_command("following")
    async def following(self, ctx: Context, target_user: str = None) -> None:
        user = target_user if target_user else ctx.author.name
        channel_name = ctx.channel.name
        api = Api(self.credentials['access_token'], self.app_config.client_id)

        if await self.bot.check_command_access(ctx, 'following'):
            broadcaster_data = api.get_user(channel_name)
            user_data = api.get_user(user)

            if broadcaster_data is None:
                await ctx.send("No se ha encontrado el canal")
                return
        
            if user_data is None:
                await ctx.send("No se ha encontrado el usuario")
                return
            
            broadcaster_id = broadcaster_data['id']
            user_id = user_data['id']
            following_since = api.check_follow(user_id, broadcaster_id)
            
            if following_since != None:
                await ctx.send(f'{user} ha seguido a {channel_name} desde {following_since}')
            else:
                await ctx.send(f'{user} no sigue este canal :(')
    
    async def custom_command(self, ctx: Context) -> None:
        user = ctx.author.name
        message_parts = ctx.message.content[1:].split()
        command = message_parts[0]
        command_config = self.custom_commands.get(self.custom_alias.get(command, command))
        response = command_config.response
        response_type = command_config.response_type

        if await self.bot.check_command_access(ctx, command_config.name) and response:
            match response_type:
                case ResponseType.SAY: await ctx.send(response)
                case ResponseType.REPLY: await ctx.reply(response)
                case ResponseType.MENTION:
                    response = response.replace('@', f' @{user} ') if '@' in response else f'@{user} {response}'
                    await ctx.send(response)
