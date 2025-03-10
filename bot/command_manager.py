import random
from twitchio.ext import commands
from modules.api import Api
from myapp import MyApp

class CommandManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        MyApp.bind_commands(self)

    @MyApp.register_command("help")
    async def help(self, ctx, parameter: str = None):
        user = ctx.author.name
        parameter = parameter.lower() if parameter else None
        command_config = self.bot.default_commands.get('help')
        required_level = command_config['user_level']
        enable_command = command_config['enable']
        
        # Activate or desactivate the command
        if await self.bot.toggle_command(ctx, "help", parameter): return

        if enable_command:
            if self.bot.level_check(ctx, required_level):
                await ctx.send("¡Hola! Soy el bot bonito del Skull Owner y estoy aquí para ayudarte. Te envió los comandos que tengo disponibles. Si requieres mayor información, puedes escribir el comando seguido de help (!comando help):")
                await ctx.send(f"!{', !'.join(self.bot.default_commands)}")
            else:
                await ctx.send(f"@{user}, no tienes el permiso para realizar la acción.")

    @MyApp.register_command("schedule")
    async def schedule(self, ctx, parameter: str = None):
        user = ctx.author.name
        parameter = parameter.lower() if parameter else None
        command_config = self.bot.default_commands.get('help')
        required_level = command_config['user_level']
        enable_command = command_config['enable']
        
        # Activate or desactivate the command
        if await self.bot.toggle_command(ctx, "schedule", parameter): return

        if enable_command:
            if self.bot.level_check(ctx, required_level):
                await ctx.send(f"Hola @{ctx.author.name}! El horario es: Martes y Jueves a partir de las 8:00pm (Zona Horaria GMT-6). Domingo si hay oportunidad, a partir de la misma hora")
            else:
                await ctx.send(f"@{user}, no tienes el permiso para realizar la acción.")

    # Check if the user or a specified user follows the channel and since when
    @MyApp.register_command("following")
    async def following(self, ctx, user_target):
        user = ctx.author.name
        parameter = parameter.lower() if parameter else None
        command_config = self.bot.default_commands.get('help')
        required_level = command_config['user_level']
        enable_command = command_config['enable']
        channel_name = ctx.channel.name
        api = Api(self.bot.token, self.bot.client_id)
        
        # Activate or desactivate the command
        if await self.bot.toggle_command(ctx, "following", parameter): return

        if enable_command:
            if self.bot.level_check(ctx, required_level):
                if user_target: user = user_target

                broadcaster_data = api.get_user(channel_name)
                user_data = api.get_user(user)

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
                    await ctx.send(f'{user} ha seguido a {channel_name} desde {following_since}')
                else:
                    await ctx.send(f'{user} no sigue este canal :(')
            else:
                await ctx.send(f"@{user}, no tienes el permiso para realizar la acción.")
    
    async def custom_command(self, ctx):
        user = ctx.author.name
        message_parts = ctx.message.content[1:].split(" ", 1)
        command = message_parts[0]
        parameter = message_parts[1] if len(message_parts) > 1 else ""
        command_config = self.bot.custom_commands.get(command)
        target_command = None
        response = ""
        
        if command in self.bot.custom_alias:
            original_command = self.bot.custom_alias[command]
            command_config = self.bot.custom_commands.get(original_command)
            target_command = self.bot.custom_commands[original_command]
        elif command in self.bot.custom_commands:
            target_command = self.bot.custom_commands.get(command)

        response = target_command.get('response')
        response_type = target_command.get('response_type', 'say')
        required_level = command_config['user_level']
        enable_command = command_config['enable']

        # Activate or desactivate the command
        if await self.bot.toggle_command(ctx, command_config['name'], parameter): return

        if enable_command:
            if self.bot.level_check(ctx, required_level):
                match response_type:
                    case 'say': await ctx.send(response)
                    case 'repy': await ctx.reply(response)
                    case 'mention': 
                        if '@' in response:
                            response = response.replace('@', f' @{user} ')
                        else:
                            response = f'@{user} {response}'

                        await ctx.send(response)
            else:
                await ctx.send(f"@{user}, no tienes el permiso para realizar la acción.")
