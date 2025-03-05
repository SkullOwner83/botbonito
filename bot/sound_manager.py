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

    # Play sounds commands
    async def play_sound(self, ctx, command):
        command = command.lower()
        SoundListCommands = self.sound_list.keys()
        user = ctx.author.name
        user_cooldown = 0

        # Activate or desactivate the play sound command
        if await self.bot.toggle_command(ctx, "playsound", command): return

        if self.bot.commands_config["playsound"]["enable"] == True:
            # Check if the user has used a sound and is still on cooldown. Also, take the current time to set the next cooldown
            current_time = time.time()
            user_cooldown = self.snd_user_register.get(user, 0)
            rest_time = self.bot.snd_cooldown - (current_time - user_cooldown)

            if command == "help":
                await ctx.send(f"Para reproducir un sonido, escribe el comando !play, seguido del nombre de uno de los siguientes sonidos (!play holi): {list(SoundListCommands)}")
                return

            # Check if the user's cooldown has already passed and the command is in the sound list to play the sound
            if rest_time <= 0 or self.bot.level_check(ctx, 'broadcaster'):
                if command in self.sound_list:
                    sound = pygame.mixer.Sound(self.sound_list[command])
                    sound.play()
                    self.snd_user_register[user] = time.time()
            else:
                await ctx.send(f"@{user} Espera un poco más para volver a usar un sonido. Tiempo restante ({round(rest_time)})")
        else:
            await ctx.send(f"@{user} Lo siento, el comando play sound esta desactivado :(")

    # Speak text commands
    async def speak(self, ctx, command):
        command = command.lower()
        user = ctx.author.name
        user_cooldown = 0

        # Check if the user has used a speaker and is still on cooldown. Also, take the current time to set the next cooldown
        current_time = time.time()
        user_cooldown = self.spk_user_register.get(user, 0)
        rest_time = self.bot.spk_cooldown - (current_time - user_cooldown)

        # Activate or desactivate the play sound command
        if await self.bot.toggle_command(ctx, "speak", command): return
        
        if command == "help":
            await ctx.send(f"Escribe el comando !speak, seguido de un mensaje no mayor a 200 caracteres, para que pueda ser leido.")
            return

        if self.bot.commands_config["speak"]["enable"] == True:
            if len(command) <= self.bot.speak_max_lenght:
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
            await ctx.send(f"@{user} Lo siento, el comando speak esta desactivado :(")