from twitchio.ext import commands
import speech_recognition as sr

from twitchio import Message, Chatter, Channel
import asyncio

class VoiceRecognition(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.r = sr.Recognizer()
        self.wake_word = config['wake_word']

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

            if command and command.startswith(self.wake_word):
                command = command.replace(self.wake_word, "").strip()

                if command in self.bot.social_media:
                    loop = self.bot.loop
                    social_media = self.bot.social_media[command]
                    asyncio.run_coroutine_threadsafe(self.bot.send_message(social_media), loop)

                if command == "horario":
                    cmd = self.bot.get_command("horario")
                    loop = self.bot.loop
                    asyncio.run_coroutine_threadsafe(self.send_message(cmd), loop)
