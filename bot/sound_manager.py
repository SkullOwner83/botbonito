import os
import time
import pygame
from twitchio.ext import commands
from gtts import gTTS
from modules.file import File
from myapp import MyApp

class SoundManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sound_list = File.open(os.path.join(MyApp.config_path, "soundlist.json"))
        self.snd_user_register = {}
        self.spk_user_register = {}
        pygame.init()
        pygame.mixer.init()
        MyApp.bind_commands(self)

    @MyApp.register_command("playsound")
    async def play_sound(self, ctx, parameter):
        user = ctx.author.name
        parameter = parameter.lower() if parameter else None
        command_config = self.bot.default_commands.get('playsound')
        required_level = command_config['user_level']
        enable_command = command_config['enable']
        sound_commands = self.sound_list.keys()
        user_cooldown = 0

        # Activate or desactivate the command
        if await self.bot.toggle_command(ctx, "playsound", parameter): return

        if enable_command:
            if parameter == self.bot.config.get('help_word', 'help'):
                await ctx.send(f"Para reproducir un sonido, escribe el comando !{command_config['name']}, seguido del nombre de uno de los siguientes sonidos (!{command_config['name']} holi):")
                await ctx.send(f"!{', !'.join(sound_commands)}")
                return
            
            if self.bot.level_check(ctx, required_level):
                current_time = time.time()
                user_cooldown = self.snd_user_register.get(user, 0)
                rest_time = self.bot.snd_cooldown - (current_time - user_cooldown)

                # Check if the user's cooldown has already passed and the command is in the sound list to play the sound
                if rest_time <= 0 or self.bot.level_check(ctx, required_level):
                    if parameter in self.sound_list:
                        sound = pygame.mixer.Sound(self.sound_list[parameter])
                        sound.play()
                        self.snd_user_register[user] = time.time()
                else:
                    await ctx.send(f"@{user} Espera un poco más para volver a usar un sonido. Tiempo restante ({round(rest_time)}s)")
            else:
                await ctx.send(f"@{user}, no tienes el permiso para realizar la acción.")

    @MyApp.register_command("speak")
    async def speak(self, ctx, parameter):
        user = ctx.author.name
        parameter = parameter.lower() if parameter else None
        command_config = self.bot.default_commands.get('speak')
        required_level = command_config['user_level']
        enable_command = command_config['enable']
        user_cooldown = 0

        # Activate or desactivate the command
        if await self.bot.toggle_command(ctx, "speak", parameter): return

        if enable_command:
            if parameter == self.bot.config.get('help_word', 'help'):
                await ctx.send(f"Escribe el comando !{command_config['name']}, seguido de un mensaje no mayor a 200 caracteres, para que pueda ser leido.")
                return
            
            if self.bot.level_check(ctx, required_level):
                current_time = time.time()
                user_cooldown = self.spk_user_register.get(user, 0)
                rest_time = self.bot.spk_cooldown - (current_time - user_cooldown)

                if len(parameter) <= self.bot.speak_max_lenght:
                    # Check if the user cooldown has already passed to speak the text
                    if rest_time <= 0 or self.bot.level_check(ctx, 'broadcaster'):
                        message = "".join(ctx.message.content.split()[1:])
                        Speaker = gTTS(text=message, lang="es", slow=False)
                        Speaker.save("last_speech.mp3")
                        Sound = pygame.mixer.Sound("last_speech.mp3")
                        Sound.play()
                        os.remove("last_speech.mp3")
                        self.spk_user_register[user] = time.time()
                    else: 
                        await ctx.send(f"@{user} Espera un poco más para volver a usar el lector de texto. Tiempo restante ({round(rest_time)}s)")
                else:
                    await ctx.send(f"@{user} Has escrito un mensaje demasiado largo. El máximo de caracteres es {self.bot.speak_max_lenght} caracteres")
            else:
                await ctx.send(f"@{user}, no tienes el permiso para realizar la acción.")