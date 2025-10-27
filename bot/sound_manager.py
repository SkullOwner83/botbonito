import os
import time
import pygame
import asyncio
from gtts import gTTS
from twitchio.ext import commands
from twitchio.ext.commands import Context
from services.commands_manager import CommandsManager
from services.service_locator import ServiceLocator
from models.appconfig import AppConfig
from utilities.enums import UserLevel
from utilities.file import File
from myapp import MyApp

class SoundManager(commands.Cog):
    def __init__(self, bot: commands.bot, app_config: AppConfig) -> None:
        self.bot: commands.bot = bot
        self.app_config = app_config
        commands_manager: CommandsManager = ServiceLocator.get('commands')
        self.default_commands = commands_manager.default_commands
        self.sound_list = File.open(os.path.join(MyApp.config_path, "soundlist.json"))
        self.snd_user_register: dict[str, float] = {}
        self.spk_user_register: dict[str, float] = {}
        self.audio_queue = asyncio.Queue()

        pygame.init()
        pygame.mixer.init()
        MyApp.bind_commands(self)

    @commands.Cog.event()
    async def event_ready(self):
        print(f"[{self.__class__.__name__}] Bot listo. Iniciando la tarea de reproducción de audio.")
        self.bot.loop.create_task(self.audio_player_task())

    # Asynchronous loop that consumes the audio queue and plays each file sequentially
    async def audio_player_task(self):
        while True:
            # Waits until there is an audio file in the queue
            audio_data = await self.audio_queue.get() 
            filepath = audio_data.get('filepath')
            volume = audio_data.get('volume', self.app_config.speak_volume)
            
            if not filepath:
                self.audio_queue.task_done()
                continue

            try:
                # Load and play the current file in the queue
                sound = pygame.mixer.Sound(filepath)
                sound.set_volume(volume)
                sound.play()
                
                # Wait asynchronously until the sound finishes playing
                while pygame.mixer.get_busy():
                    await asyncio.sleep(0.1)

                await asyncio.sleep(self.app_config.speak_cooldown)
            except Exception as e:
                print(f"Error reproduciendo el audio: {e}")
            finally:
                # Release the queue and clean up the resource
                self.audio_queue.task_done()
                if audio_data.get('should_delete', False) and os.path.exists(filepath):
                    os.remove(filepath)

    @MyApp.register_command("playsound")
    async def play_sound(self, ctx: Context, parameter: str) -> None:
        user = ctx.author.name
        parameter = parameter.lower() if parameter else None
        command_config = self.default_commands.get('playsound')
        sound_commands = self.sound_list.keys()
        user_cooldown = 0

        if await self.bot.check_command_access(ctx, 'playsound'):
            if parameter == self.app_config.help_word:
                await ctx.send(f"Para reproducir un sonido, escribe el comando !{command_config.name}, seguido del nombre de uno de los siguientes sonidos (!{command_config.name} holi):")
                await ctx.send(f"!{', !'.join(sound_commands)}")
                return
                
            current_time = time.time()
            user_cooldown = self.snd_user_register.get(user, 0)
            rest_time = command_config.cooldown - (current_time - user_cooldown)

            # Check if the user's cooldown has already passed and the command is in the sound list to play the sound
            if rest_time <= 0 or self.bot.level_check(ctx, UserLevel.BROADCASTER):
                if parameter in self.sound_list:
                    sound = pygame.mixer.Sound(self.sound_list[parameter])
                    sound.set_volume(self.app_config.sounds_volume)
                    sound.play()
                    self.snd_user_register[user] = time.time()
            else:
                await ctx.send(f"@{user} Espera un poco más para volver a usar un sonido. Tiempo restante ({round(rest_time)}s)")

    @MyApp.register_command("speak")
    async def speak(self, ctx: Context, parameter: str) -> None:
        user = ctx.author.name
        message = str.join(" ", ctx.message.content.split()[1:])
        parameter = parameter.lower() if parameter else None
        command_config = self.default_commands.get('speak')
        user_cooldown = 0

        if await self.bot.check_command_access(ctx, 'speak'):
            if parameter == self.app_config.help_word:
                await ctx.send(f"Escribe el comando !{command_config.name}, seguido de un mensaje no mayor a {command_config.max_length} caracteres, para que pueda ser leido.")
                return
                
            current_time = time.time()
            user_cooldown = self.spk_user_register.get(user, 0)
            rest_time = command_config.cooldown - (current_time - user_cooldown)

            if len(message) <= command_config.max_length:
                # Check if the user cooldown has already passed to speak the text
                if rest_time <= 0 or self.bot.level_check(ctx, UserLevel.BROADCASTER):
                    temp_filename = f"tts_{ctx.author.name}_{time.time()}.mp3"
            
                    try:
                        tts_message = f"{ctx.author.name} dice: {message}"
                        engine = gTTS(text=tts_message, lang="es", slow=False)
                        engine.save(temp_filename)
                        
                        # Put generated audio into the queue
                        await self.audio_queue.put({
                            'filepath': temp_filename,
                            'volume': self.app_config.speak_volume,
                            'should_delete': True
                        })
                    except Exception as e:
                        print(f"Error al generar el audio: {e}")
                        await ctx.send(f"@{user} Hubo un problema al generar el audio.")
                else: 
                    await ctx.send(f"@{user} Espera un poco más para volver a usar el lector de texto. Tiempo restante ({round(rest_time)}s)")
            else:
                await ctx.send(f"@{user} Has escrito un mensaje demasiado largo. El máximo de caracteres es {command_config.max_length} caracteres")