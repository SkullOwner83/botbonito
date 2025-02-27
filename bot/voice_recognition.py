import asyncio
from twitchio.ext import commands
from twitchio import Message
import speech_recognition as sr
from modules.file import File
from myapp import MyApp

class VoiceRecognition(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.r = sr.Recognizer()
        self.wake_word = config['wake_word']
        self.user_alias = File.open(f"{MyApp.config_path}/useralias.json")

    # Create a loop to listen for audio input and recognize the voice
    def capture_voice_commands(self):
        while True:
            with sr.Microphone() as source:
                self.r.adjust_for_ambient_noise(source)
                audio = self.r.listen(source)
            
            command = ""

            try:
                command = self.r.recognize_google(audio, language="es-ES")
                command = command.lower()
            except sr.UnknownValueError:
                print("No se entendió el audio.")

            except sr.RequestError as e:
                print(f"Error con el reconocimiento de voz: {e}")

            # Check if the recognized command is the wake word and excecute the command
            if command and command.startswith(self.wake_word):
                command = command.replace(self.wake_word, "").strip()
                self.handle_voice_command(command)
                print(command)

    # Get a main loop and execute the voice command or send the complete message
    def handle_voice_command(self, command):
        loop = self.bot.loop

        if any(word in command for word in ["saluda", "saludo", "salúdame"]) and len(command) > 1:
            for user, alias in self.user_alias.items():
                if any(name in command for name in alias):
                    message = f"¡Hola! @{user}, ¿Cómo estás?"
                    asyncio.run_coroutine_threadsafe(self.send_message(message), loop)
                    return
        
        # send the complete command to simulate a user message and execute if it's a command
        asyncio.run_coroutine_threadsafe(self.execute_commands(command), loop)

    # Create a fake message to execute the command
    async def execute_commands(self, command):
        fake_message = Message(
            content=f"!{command}",
            author=self.bot.connected_channels[0],
            channel=self.bot.connected_channels[0],
            tags={}, 
            bot=self
        )

        if command in self.bot.social_media:
            await self.send_message(self.bot.social_media[command])
            return
        
        await self.bot.handle_commands(fake_message)

    async def send_message(self, message):
        await self.bot.send_message(message)
