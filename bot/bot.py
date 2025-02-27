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
    # Variable configuration
    playsound_command = True
    speak_command = True

    def __init__(self, config, credentials):
        self.voice_recognition_cog = VoiceRecognition(self, config)
        self.sound_manager_cog = SoundManager(self)
        self.command_manager_cog = CommandManager(self)
        self.dynamics_commands_cog = DynamicsCommands(self)
        self.recognition_thread = threading.Thread(target=self.voice_recognition_cog.capture_voice_commands)

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

        # Load social media links, replace the '@' character to make links accessible in twitch, and insert them into frequency messages
        self.social_media = File.open(f"{MyApp.config_path}/socialmedia.json")
        self.social_media = {key: url.replace('@', '%40') for key, url in self.social_media.items()}
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

        self.add_cog(self.sound_manager_cog)
        self.add_cog(self.command_manager_cog)
        self.add_cog(self.dynamics_commands_cog)

    # Print a message when the bot is ready and send initial greeting in the specified channels
    async def event_ready(self):
        print("Hi, I'm ready!")
        await self.send_message("Hola, soy el bot bonito del Skull.")
        asyncio.create_task(self.send_frequent_messages())
        self.recognition_thread.start()

    # Check chat messages event
    async def event_message(self, ctx):
        ctx.content = ctx.content.lower()

        if ctx.author is None or ctx.author.name == self.name:
            return
        
        if ctx.content[0] == self.prefix:
            command = ctx.content[1:]
            
            if command in self.social_media:
                await ctx.channel.send(f"{self.social_media[command]}")
                return

        # Check if the message is a command
        await self.handle_commands(ctx)

    # Check if the user that sent the command, is the admin    
    def admin_check(self, ctx):
        return True if ctx.author.name == ctx.channel.name else False
    
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