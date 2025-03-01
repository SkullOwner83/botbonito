import time
import pygame
from twitchio.ext import commands
from gtts import gTTS
from modules.file import File
from myapp import MyApp

class SoundManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sound_list = File.open(f"{MyApp.config_path}/soundlist.json")
        self.snd_user_register = {}
        self.spk_user_register = {}
        pygame.init()
        pygame.mixer.init()

    # Play sounds commands
    @commands.command(name="play")
    async def play_sound(self, ctx, command):
        SoundListCommands = self.sound_list.keys()
        user_cooldown = 0

        # Activate or desactivate the play sound command
        if command in ["enable", "disable"]:
            await self.bot.toggle_command(ctx, "playsound", command)
            return

        if self.bot.commands_config["playsound"]["enable"] == True:
            # Check if the user has used a sound and is still on cooldown. Also, take the current time to set the next cooldown
            current_time = time.time()
            user_cooldown = self.snd_user_register.get(ctx.author.name, 0)
            rest_time = self.bot.snd_cooldown - (current_time - user_cooldown)

            # Check if the user's cooldown has already passed and the command is in the sound list to play the sound
            if rest_time <= 0 or self.bot.admin_check(ctx):
                if command in self.sound_list:
                    sound = pygame.mixer.Sound(self.sound_list[command])
                    sound.play()
                    self.snd_user_register[ctx.author.name] = time.time()
                else:
                    if command == "help":
                        await ctx.send(f"Para reproducir un sonido, escribe el comando !play, seguido del nombre de uno de los siguientes sonidos (!play holi): {list(SoundListCommands)}")
            else:
                await ctx.send(f"@{ctx.author.name} Espera un poco más para volver a usar un sonido. Tiempo restante ({round(rest_time)})")
        else:
            await ctx.send(f"@{ctx.author.name} Lo siento, el comando play sound esta desactivado :(")

    # Speak text commands
    @commands.command(name="speak")
    async def speak(self, ctx, command):
        command = command.lower()
        user_cooldown = 0

        # Check if the user has used a speaker and is still on cooldown. Also, take the current time to set the next cooldown
        current_time = time.time()
        user_cooldown = self.spk_user_register.get(ctx.author.name, 0)
        rest_time = self.bot.spk_cooldown - (current_time - user_cooldown)

        # Activate or desactivate the speak command
        if command in ["enable", "disable"]:
            await self.bot.toggle_command(ctx, "speak", command)
            return

        if self.bot.commands_config["speak"]["enable"] == True:
            if len(command) <= self.bot.speak_max_lenght:
                # Check if the user cooldown has already passed to speak the text
                if rest_time <= 0 or self.bot.admin_check(ctx):
                    message = "".join(ctx.message.content.split()[1:])
                    Speaker = gTTS(text=message, lang="es", slow=False)
                    Speaker.save("LastSpeech.mp3")
                    Sound = pygame.mixer.Sound("LastSpeech.mp3")
                    Sound.play()
                    self.spk_user_register[ctx.author.name] = time.time()
                else: 
                    await ctx.send(f"@{ctx.author.name} Espera un poco más para volver a usar el lector de texto. Tiempo restante ({round(rest_time)}s)")
            else:
                await ctx.send(f"@{ctx.author.name} Has escrito un mensaje demasiado largo. El máximo de caracteres es {self.bot.speak_max_lenght} caracteres")
        else:
            await ctx.send(f"@{ctx.author.name} Lo siento, el comando speak esta desactivado :(")