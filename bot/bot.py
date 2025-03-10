import os
import time
import random
import asyncio
import threading
from twitchio.ext import commands
from modules.file import File
from bot.voice_recognition import VoiceRecognition
from bot.sound_manager import SoundManager
from bot.command_manager import CommandManager
from bot.dynamics_commands import DynamicsCommands
from myapp import MyApp

class Bot(commands.Bot):
    command_registry = {}

    def __init__(self, config, credentials):
        # Create an  instance of the bot Cogs to handle commands
        self.command_manager_cog = CommandManager(self)
        self.dynamics_commands_cog = DynamicsCommands(self)
        self.sound_manager_cog = SoundManager(self)
        self.voice_recognition_cog = VoiceRecognition(self, config)
        self.recognition_thread = threading.Thread(target=self.voice_recognition_cog.capture_voice_commands)

        # load variables from the config files
        self.config = config
        self.token = credentials['token']
        self.client_id = credentials['client_id']
        self.client_secret = credentials['client_secret']
        self.name = config['name']
        self.channels = config['channels']
        self.prefix = config['prefix']
        self.frequency_message_time = config['frequency_message_time']
        self.snd_cooldown = config['snd_cooldown']
        self.spk_cooldown = config['spk_cooldown']
        self.speak_max_lenght = config['speak_max_lenght']
        self.__frequency_messages = config['frecuency_messages']
        self.__commands_config = File.open(os.path.join(MyApp.config_path, "commands.json"))
        self.default_commands = self.__commands_config.get("default_commands", {})
        self.custom_commands = self.__commands_config.get("custom_commands", {})
        self.custom_alias = {alias: key for key, value in self.custom_commands.items() for alias in value.get("alias", [])}

        # Load social media links, replace the '@' character to make links accessible in twitch, and insert them into frequency messages
        self.social_media = File.open(os.path.join(MyApp.config_path, "socialmedia.json"))
        self.social_media = { key: url.replace('@', '%40') for key, url in self.social_media.items( )}
        self.frequency_messages = [
            message.format(**self.social_media) for message in self.__frequency_messages
        ]

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
    def create_commands(self):
        for command_name, config in self.default_commands.items():
            if command_name in MyApp.command_registry:
                name = config['name']
                alias = config['alias']
                callable_function = MyApp.command_registry[command_name]
                new_command = commands.Command(name=name, func=callable_function, aliases=alias)
                self.add_command(new_command)

    # Print a message when the bot is ready and send initial greeting in the specified channels
    async def event_ready(self):
        print("Hi, I'm ready!")
        await self.send_message("Hola, soy el bot bonito del Skull.")
        asyncio.create_task(self.send_frequent_messages())
        self.recognition_thread.start()

    # Check chat messages event
    async def event_message(self, message):
        if message.echo:
            return
        
        message.content = message.content.lower()
        
        # Check if the message request a social media to repsonse with their link
        if message.content.startswith(self.prefix):  
            parts = message.content[1:].split(" ", 1)
            command = parts[0]
            
            if command in self.social_media:
                await message.channel.send(f"{self.social_media[command]}")
                return
            
            if command in self.custom_commands or command in self.custom_alias:
                context = commands.Context(bot=self, message=message, prefix=self.prefix, command=None)
                await self.command_manager_cog.custom_command(context)
                return

        # Check if the message is a command
        await self.handle_commands(message)

    # Check if the user that sent the command, is the admin    
    def level_check(self, ctx, rol):
        user = ctx.author
        user_badges = list(user.badges.keys())

        if rol in user_badges or rol == 'everyone':
            return True
    
        return False
    
    # send random messages Frequently in the first bot Channel
    async def send_frequent_messages(self):
        while True:
            await asyncio.sleep(self.frequency_message_time)
            random.seed(int(time.time()))
            message = random.choice(self.frequency_messages)
            await self.send_message(message)
    
    # Find the current channel when doesn't have the context and send a message from the bot
    async def send_message(self, message):
        for channel_name in self.channels:
            channel = self.get_channel(channel_name)

            if channel:
                await channel.send(message)

    # Activate or desactivate a command
    async def toggle_command(self, ctx, command, value):
        target_command = None
        
        if self.default_commands.get(command):
            target_command = self.default_commands[command]
        elif self.custom_commands.get(command):
            target_command = self.custom_commands[command]

        if self.level_check(ctx, 'broadcaster'):
            if value == self.config.get('enable_word', 'enable'):
                if target_command["enable"] == False:
                    target_command["enable"] = True
                    await ctx.send(f"Se ha activado el comando {command}.")
                else:
                    await ctx.send(f"El comando {command} ya esta activado.") 
                
                return True
            
            if value == self.config.get('disable_word', 'disable'):
                if target_command['enable'] == True:
                    target_command['enable'] = False
                    await ctx.send(f"Se ha desactivado el comando {command}.")
                else:
                    await ctx.send(f"El comando {command} ya esta desactivado.")
                return True
        else:
            await ctx.send("No tienes permisos para realizar esta acción.")
        
        return False
