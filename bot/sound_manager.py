import os
import time
import pygame
from twitchio.ext import commands
from twitchio.ext.commands import Context
from gtts import gTTS
from modules.file import File
from myapp import MyApp

class SoundManager(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.sound_list = File.open(os.path.join(MyApp.config_path, "soundlist.json"))
        self.snd_user_register: dict[str, float] = {}
        self.spk_user_register: dict[str, float] = {}
        pygame.init()
        pygame.mixer.init()
        MyApp.bind_commands(self)

    @MyApp.register_command("playsound")
    async def play_sound(self, ctx: Context, parameter: str) -> None:
        user = ctx.author.name
        parameter = parameter.lower() if parameter else None
        command_config = self.bot.default_commands.get('playsound')
        sound_commands = self.sound_list.keys()
        user_cooldown = 0

        if await self.bot.check_command_access(ctx, "giveaway_entry"):
            if parameter == self.bot.config.get('help_word', 'help'):
                await ctx.send(f"Para reproducir un sonido, escribe el comando !{command_config['name']}, seguido del nombre de uno de los siguientes sonidos (!{command_config['name']} holi):")
                await ctx.send(f"!{', !'.join(sound_commands)}")
                return
                
            current_time = time.time()
            user_cooldown = self.snd_user_register.get(user, 0)
            rest_time = command_config.cooldown - (current_time - user_cooldown)

            # Check if the user's cooldown has already passed and the command is in the sound list to play the sound
            if rest_time <= 0 or self.bot.level_check(ctx, 'broadcaster'):
                if parameter in self.sound_list:
                    sound = pygame.mixer.Sound(self.sound_list[parameter])
                    sound.play()
                    self.snd_user_register[user] = time.time()
            else:
                await ctx.send(f"@{user} Espera un poco más para volver a usar un sonido. Tiempo restante ({round(rest_time)}s)")

    @MyApp.register_command("speak")
    async def speak(self, ctx: Context, parameter: str) -> None:
        user = ctx.author.name
        parameter = parameter.lower() if parameter else None
        command_config = self.bot.default_commands.get('speak')
        user_cooldown = 0

        if await self.bot.check_command_access(ctx, "giveaway_entry"):
            if parameter == self.bot.config.get('help_word', 'help'):
                await ctx.send(f"Escribe el comando !{command_config.name}, seguido de un mensaje no mayor a {command_config.max_length} caracteres, para que pueda ser leido.")
                return
                
            current_time = time.time()
            user_cooldown = self.spk_user_register.get(user, 0)
            rest_time = command_config.cooldown - (current_time - user_cooldown)

            if len(parameter) <= command_config.max_length:
                # Check if the user cooldown has already passed to speak the text
                if rest_time <= 0 or self.bot.level_check(ctx, 'broadcaster'):
                    message = str.join(" ", ctx.message.content.split()[1:])
                    Speaker = gTTS(text=message, lang="es", slow=False)
                    Speaker.save("last_speech.mp3")
                    Sound = pygame.mixer.Sound("last_speech.mp3")
                    Sound.play()
                    os.remove("last_speech.mp3")
                    self.spk_user_register[user] = time.time()
                else: 
                    await ctx.send(f"@{user} Espera un poco más para volver a usar el lector de texto. Tiempo restante ({round(rest_time)}s)")
            else:
                await ctx.send(f"@{user} Has escrito un mensaje demasiado largo. El máximo de caracteres es {command_config.max_length} caracteres")