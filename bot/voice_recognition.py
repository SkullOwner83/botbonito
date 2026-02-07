import asyncio
from threading import Thread
from typing import TYPE_CHECKING
import unicodedata
from twitchio import Message, Chatter
from twitchio.ext import commands
import speech_recognition as sr
from models.appconfig import AppConfig
if TYPE_CHECKING: from bot.bot import Bot

class VoiceRecognition(commands.Cog):
    def __init__(self, bot: commands.Bot, app_config: AppConfig) -> None:
        self.bot: Bot = bot
        self.app_config = app_config
        self.r = sr.Recognizer()
    
    # Create speech recognition loop when the bot is ready
    @commands.Cog.event()
    async def event_ready(self):
        print(f"[{self.__class__.__name__}] Speech recognition started.")
        Thread(target=self.capture_voice_commands, daemon=True).start()

    # Create a loop to listen for audio input and recognize the voice
    def capture_voice_commands(self) -> None:
        while True:
            command: str = ""
            
            with sr.Microphone() as source:
                self.r.adjust_for_ambient_noise(source)
                audio = self.r.listen(source)

            try:
                command = self.r.recognize_google(audio, language="es-ES")
                command = command.lower()
                command = unicodedata.normalize('NFD', command)
                command =  ''.join(c for c in command if unicodedata.category(c) != 'Mn')

            except sr.UnknownValueError:
                pass
                #print("No se entendió el audio.")
            except sr.RequestError as e:
                print(f"Error con el reconocimiento de voz: {e}")

            # Check if the recognized command is the wake word and excecute the command
            if command and command.startswith(self.app_config.wake_word):
                command = command.replace(self.app_config.wake_word, "").strip()
                asyncio.run_coroutine_threadsafe(
                    self.execute_command(command),
                    self.bot.loop
                )

    # Create a fake message to execute the command
    async def execute_command(self, command: str) -> None:
        if not self.bot.connected_channels:
            return
        
        fake_user = Chatter(
            websocket=self.bot._connection, 
            name=self.bot.nick, 
            channel=self.bot.connected_channels[0],
            tags={
                "user-id": "0",
                "display-name": self.bot.nick,
                "color": "#FFFFFF",
                "badges": "broadcaster/1", 
                "subscriber": "0",
                "mod": "1",
                "turbo": "0"
            }
        )

        try:
            fake_message = Message(
                content=f"{self.bot.prefix}{command}",
                author=fake_user,
                channel=self.bot.connected_channels[0],
                bot=self.bot,
                tags={}
            )
            
            print(f"Ejecutando comando de voz: {command}")
            await self.bot.handle_commands(fake_message)
        except Exception as e:
            print(f"Error al procesar handle_commands: {e}")
