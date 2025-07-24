import os
import re
import time
import random
import asyncio
import threading

from twitchio import Message
from twitchio.ext import commands
from twitchio.ext.commands import Context

from bot.voice_recognition import VoiceRecognition
from bot.sound_manager import SoundManager
from bot.command_manager import CommandManager
from bot.dynamics_commands import DynamicsCommands
from bot.moderation import Moderation
from models.appconfig import AppConfig
from utilities.enums import UserLevel
from services.service_locator import ServiceLocator
from services.commands_manager import CommandsManager
from utilities import *
from myapp import MyApp

class Bot(commands.Bot):
    def __init__(self, app_config: AppConfig, credentials: dict) -> None:
        # Create an  instance of the bot Cogs to handle commands
        self.command_manager_cog = CommandManager(self)
        self.dynamics_commands_cog = DynamicsCommands(self)
        self.sound_manager_cog = SoundManager(self, app_config)
        self.voice_recognition_cog = VoiceRecognition(self, app_config)
        self.moderation_cog = Moderation(self)
        self.recognition_thread = threading.Thread(target=self.voice_recognition_cog.capture_voice_commands)

        # load variables from the config files
        self.app_config = app_config
        self.token = credentials['access_token']
        self.client_id = app_config.client_id
        self.client_secret = app_config.client_secret
        self.name = app_config.name
        self.channels = app_config.channels
        self.prefix = app_config.prefix
        # self.frequency_message_time = config['frequency_message_time']
        # self.__frequency_messages = config['frecuency_messages']

        # Load social media links, replace the '@' character to make links accessible in twitch, and insert them into frequency messages
        # self.social_media = File.open(os.path.join(MyApp.config_path, "socialmedia.json"))
        # self.social_media = { key: url.replace('@', '%40') for key, url in self.social_media.items( )}
        # self.frequency_messages = [
        #     message.format(**self.social_media) for message in self.__frequency_messages
        # ]

        # Get the config manager instance to load the commands
        commands_manager: CommandsManager = ServiceLocator.get('commands')
        self.default_commands = commands_manager.default_commands
        self.custom_commands = commands_manager.custom_commands
        self.custom_alias = commands_manager.custom_alias

        # Initialize the bot with the received config
        super().__init__( 
            token=f'oauth:{self.token}',
            client_secret=self.client_secret,
            prefix=self.prefix,
            initial_channels=self.channels
        )

        # Bind the cogs to the bot and create the commands
        self.add_cog(self.sound_manager_cog)
        self.add_cog(self.command_manager_cog)
        self.add_cog(self.dynamics_commands_cog)
        self.create_commands()

    # Create commands from 
    def create_commands(self) -> None:
        for command_name, config in self.default_commands.items():
            if command_name in MyApp.command_registry:
                name = config.name
                alias = config.alias
                callable_function = MyApp.command_registry[command_name]
                new_command = commands.Command(name=name, func=callable_function, aliases=alias)
                self.add_command(new_command)

    # Print a message when the bot is ready and send initial greeting in the specified channels
    async def event_ready(self) -> None:
        print("Hi, I'm ready!")
        await self.send_message("Hola, soy el bot bonito del Skull.")
        
        #asyncio.create_task(self.send_frequent_messages())
        #self.recognition_thread.start()

    # Check chat messages event
    async def event_message(self, message: Message) -> None:
        if not message.author or message.author.name.lower() == self.name.lower():
            return
        
        context = Context(bot=self, message=message, prefix=self.prefix, command=None)
        await self.moderation_cog.message_filter(context)
        
        # Check if the message is a custom command or a social media link request, before sending the message, handle it as a command
        if message.content.startswith(self.prefix):  
            parts = message.content[1:].split()
            command = parts[0]
            message.content = re.sub(r'^(\s*\S+)', lambda m: m.group(0).lower(), message.content, count=1)


            # if command in self.social_media:
            #     await message.channel.send(f"{self.social_media[command]}")
            #     return
            
            if command in self.custom_commands or command in self.custom_alias:
                await self.command_manager_cog.custom_command(context)
                return

        # Check if the message is a command
        await self.handle_commands(message)
    
    # send random messages Frequently in the first bot Channel
    async def send_frequent_messages(self) -> None:
        while True:
            await asyncio.sleep(self.frequency_message_time)
            random.seed(int(time.time()))
            message = random.choice(self.frequency_messages)
            await self.send_message(message)
    
    # Find the current channel when doesn't have the context and send a message from the bot
    async def send_message(self, message: str) -> None:
        for channel_name in self.channels:
            channel = self.get_channel(channel_name)

            if channel:
                await channel.send(message)

    # Check if the user has a specific role in the channel
    def level_check(self, ctx: Context, level: str) -> bool:
        user = ctx.author
        user_badges = list(user.badges.keys())

        if level == UserLevel.FOLLOWER:
            api = Api(self.token, self.client_id)
            user_id = (api.get_user(user.name) or {}).get('id')
            broadcaster_id = (api.get_user(ctx.channel.name) or {}).get('id')

            if user_id and broadcaster_id:
                if api.check_follow(user_id, broadcaster_id): 
                    return True

        if level in user_badges or level == UserLevel.EVERYONE:
            return True
    
        return False

    # Activate or desactivate a command
    async def toggle_command(self, ctx: Context, command: str, value: bool) -> None:
        target_command = self.default_commands.get(command) or self.custom_commands.get(command)
        enable_word = self.app_config.enable_word
        disable_word = self.app_config.disable_word
        
        if value == enable_word or value == disable_word:
            if self.level_check(ctx, UserLevel.BROADCASTER):
                if value == enable_word:
                    if target_command.enable == False:
                        target_command.enable = True
                        await ctx.send(f"Se ha activado el comando {command}.")
                    else:
                        await ctx.send(f"El comando {command} ya esta activado.") 
                
                if value == disable_word:
                    if target_command.enable == True:
                        target_command.enable = False
                        await ctx.send(f"Se ha desactivado el comando {command}.")
                    else:
                        await ctx.send(f"El comando {command} ya esta desactivado.")
            else:
                await ctx.send("No tienes permisos para realizar esta acción.")
            
            return True
        return False

    # Check if the is enable and user has the permission to excecute the command
    async def check_command_access(self, ctx: Context, command_name: str) -> bool:
        user = ctx.author.name
        message_parts = ctx.message.content[1:].split()
        parameter =  message_parts[1] if len(message_parts) > 1 else ""
        command_config = self.default_commands.get(command_name) or self.custom_commands.get(command_name)
        required_level = command_config.user_level
        enable_command = command_config.enable

        if await self.toggle_command(ctx, command_name, parameter):
            return False
        
        if not enable_command:
            return False

        if not self.level_check(ctx, required_level):
            await ctx.send(f"@{user}, no tienes el permiso para realizar la acción.")
            return False

        return True