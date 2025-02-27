import asyncio
from twitchio.ext import commands
from twitchio import Message
import speech_recognition as sr

class VoiceRecognition(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.r = sr.Recognizer()
        self.wake_word = config['wake_word']

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
                print(command)
            except sr.UnknownValueError:
                print("No se entendió el audio.")

            except sr.RequestError as e:
                print(f"Error con el reconocimiento de voz: {e}")

            # Check if the recognized command is the wake word and excecute the command in the main loop
            if command and command.startswith(self.wake_word):
                command = command.replace(self.wake_word, "").strip()
                loop = self.bot.loop
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
        
        await self.bot.handle_commands(fake_message)
