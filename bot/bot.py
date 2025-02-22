import os
import time
import random
import asyncio
import pyperclip
import pygame
import re
from twitchio.ext import commands
from modules.api import Api
from modules.token import Token
from modules import file
from modules.file import File
from gtts import gTTS

pygame.init()
pygame.mixer.init()

class Bot(commands.Bot):
    # Load config and variable values from files
    ProjectPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ConfigPath = f"{ProjectPath}/config/"
    sound_list = file.ReadDictionary(f"{ConfigPath}/soundlist.txt")

    # Variable configuration
    frequency_message_time = 1200
    playsound_command = True
    speak_command = True
    snd_user_register = {}
    spk_user_register = {}
    snd_cooldown = 60
    spk_cooldown = 180
    speak_max_lenght = 200

    give_away_started = False
    send_demo_started = False
    give_away_list = []
    user_demo_list = []
    demos_list = {}

    # Constructor method that receives the bot config
    def __init__(self, config, credentials):
        self.social_media = File.open(f"{self.ConfigPath}/socialmedia.json")

        self.name = config['name']
        self.channels = config['channels']
        self.prefix = config['prefix']
        self.token = credentials['token']
        self.client_id = credentials['client_id']

        self.frequency_message_list = [
            "¿Ya tomaste awua uwu?",
            "Esta bonito tu stream mijito! uwu",
            "¿Se estan pasando un buen rato? :3",
            "Gracias a los que estan viendo el directo :D",
            f"Recuerden entrar a mi discord: {self.social_media['discord']}",
            f"¿Ya te suscribiste a mi canal de youtube? {self.social_media['youtube']}",
            f"¿Ya me seguiste en instagram? {self.social_media['instagram']}",
            "Usa !help para ver la lista de comandos disponibles. :D"
        ]

        super().__init__(
            irc_token=f'oauth:{self.token}',
            client_id=self.client_id,
            nick=self.name,
            prefix=self.prefix,
            initial_channels=self.channels
        )

    # Print a message when the bot is ready and send initial greeting in the specified channels
    async def event_ready(self):
        print("Hi, I'm ready!")
        
        for channel_name in self.initial_channels:
            channel = self.get_channel(channel_name)

            if channel:
                await channel.send("Hola, soy el bot bonito del Skull.")
                asyncio.create_task(self.send_frequent_messages())

    # send random messages Frequently in the first bot Channel
    async def send_frequent_messages(self):
        while True:
            await asyncio.sleep(self.frequency_message_time)
            
            for channel_name in self.initial_channels:
                channel = self.get_channel(channel_name)

                if channel:
                    random.seed(int(time.time()))
                    Message = random.choice(self.frequency_message_list)
                    await channel.send(Message)

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

    @commands.command(name="help")
    async def help(self, ctx):
        await ctx.send("¡Hola! Soy el bot bonito del Skull Owner y estoy aquí para ayudarte. Te envió los comandos que tengo disponibles para todos:")
        await ctx.send("!horario, !discord, !youtube, !instagram, !onlyfans, !gay, !memide, !leentro, !play, !speak, !following")

    @commands.command(name="horario")
    async def schedule(self, ctx):
        await ctx.send(f"Hola @{ctx.author.name}! El horario es: Martes y Jueves a partir de las 8:00pm (Zona Horaria GMT-6). Domingo si hay oportunidad, a partir de la misma hora")
    
    # Another random commands
    @commands.command(name="onlyfans")
    async def onlyfans(ctx):
        await ctx.send(f"{ctx.author.name} se ha suscrito al onlyfans del Skull!")    

    @commands.command(name="gay")
    async def gay(self, ctx):
        print(self.GiveAwayStarted)
        await ctx.send("Quien? El Owl?")  

    @commands.command(name="memide")
    async def memide(ctx):
        size = random.randint(1, 50)
        await ctx.send(f"{ctx.author.name} le mide {size}cm")

     # Check if the user or a specified user follows the channel and since when
    @commands.command(name="following")
    async def follow(self, ctx, *args):
        user_name = ctx.author.name
        channel_name = ctx.channel.name
        api = Api(self.token, self.client_id)

        # Check if there is text next to the comand and get the first word as an argument
        if len(args) > 0:
            user_name = args[0].lower()

        broadcaster_data = api.get_user(channel_name)
        user_data = api.get_user(user_name)

        if broadcaster_data is None:
            await ctx.send("No se ha encontrado el canal")
            return
    
        if user_data is None:
            await ctx.send("No se ha encontrado el usuario")
            return

        idBroadcaster = broadcaster_data['id']
        idUser = user_data['id']
        following_since = api.check_follow(idUser, idBroadcaster)
        
        if following_since != None:
            await ctx.send(f'{user_name} ha seguido a {channel_name} desde {following_since}')
        else:
            await ctx.send(f'{user_name} no sigue este canal :(')
        
    # Play sounds commands
    @commands.command(name="play")
    async def play_sound(self, ctx, *args):
        SoundListCommands = self.sound_list.keys()
        user_cooldown = 0

        # Check if ther is text next to the comand and get the first word as an argument
        if len(args) > 0:
            command = args[0].lower()

        # Activate or desactivate the play sound command
        if self.admin_check(ctx):
            if command == "enable":
                self.playsound_command = True
                await ctx.send(f"Se ha activado el comando play sound.")
                return
            
            if command == "disable":
                self.playsound_command = False
                await ctx.send(f"Se ha desactivado el comando play sound.")
                return
        
        if self.playsound_command == True:
            # Check if the user has used a sound and is still on cooldown. Also, take the current time to set the next cooldown
            user_cooldown = self.snd_user_register.get(ctx.author.name, 0)
            current_time = time.time()

            # Substract the cooldown time minus the time when the user used a sound minus the current time to get the rest time
            rest_time = self.snd_cooldown - (current_time - user_cooldown)

            # Check if the user's cooldown has already passed and the command is in the sound list to play the sound
            if rest_time <= 0 or self.admin_check(ctx):
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
    async def speak(self, ctx, *args):
        user_cooldown = 0

        # Check if there is text next to the comand and get the first word as an argument
        if len(args) > 0:
            command = "".join(args).lower()

        # Check if the user has used a speaker and is still on cooldown. Also, take the current time to set the next cooldown
        user_cooldown = self.spk_user_register.get(ctx.author.name, 0)
        current_time = time.time()

        # Substract the cooldown time minus the time when the user used a speaker minus the current time to get the rest time
        rest_time = self.spk_cooldown - (current_time - user_cooldown)

        # Activate or desactivate the speak command
        if self.admin_check(ctx):
            if command == "enable":
                self.speak_command = True
                await ctx.send(f"Se ha activado el comando speak.")
                return
            
            if command == "disable":
                self.speak_command = False
                await ctx.send(f"Se ha desactivado el comando speak.")
                return

        if self.speak_command == True:
            if len(command) <= self.speak_max_lenght:
                # Check if the user cooldown has already passed to speak the text
                if rest_time <= 0 or self.admin_check(ctx):
                    Speaker = gTTS(text=command, lang="es", slow=False)
                    Speaker.save("LastSpeech.mp3")
                    Sound = pygame.mixer.Sound("LastSpeech.mp3")
                    Sound.play()
                    self.spk_user_register[ctx.author.name] = time.time()
                else: 
                    await ctx.send(f"@{ctx.author.name} Espera un poco más para volver a usar el lector de texto. Tiempo restante ({round(rest_time)}s)")
            else:
                await ctx.send(f"@{ctx.author.name} Has escrito un mensaje demasiado largo. El máximo de caracteres es {self.speak_max_lenght} caracteres")
        else:
            await ctx.send(f"@{ctx.author.name} Lo siento, el comando speak esta desactivado :(")

    # Send demos commands
    @commands.command(name="senddemo")    
    async def send_demo(self, ctx, *args):
        # Check if there is text next to the comand and get the first word as an argument
        if len(args) > 0:
            command = args[0].lower()
        
        if self.admin_check(ctx):
            # Start the demos collection 
            if command == "start":
                if self.send_demo_started == False:
                    self.send_demo_started = True
                    self.demos_list.clear()
                    await ctx.send("Comenzamos con la recopilación de demos. Recuerda seguirme para poder participar, ademas de enviar un enlace de Youtube o Soundcloud. Para enviar tu demo, escribe el comando !demo, seguido del link de tu demo.")

            # Finish the demos collection. Choose a user at random and copy his link to the clipboard
            if command == "finish":
                if self.send_demo_started == True:
                    self.send_demo_started = False
                    await ctx.send("La lista para poder enviar tu demo, ha finalizado! Ahora se escogera un demo de manera aleatoria. Suerte a todos!")
                    await asyncio.sleep(3)
                    user_winner = random.choice(list(self.demos_list.keys()))
                    await ctx.send(f"El usuario elegido fue @{user_winner}. Se ha copiado su link en el portapapeles del streamer.")
                    print(f"Se ha copiado el link del demo al portapapeles.")
                    pyperclip.copy(self.demos_list[user_winner])            

    @commands.command(name="demo")
    async def Demo(self, ctx, *args):
        youtube_patter = re.compile(r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+$")
        soundcloud_patter = re.compile(r'https?://soundcloud\.com/[\w-]+/[\w-]+')

        # Check if there is text next to the comand and get the first word as an argument
        if len(args) > 0:
            Link = args[0].lower()

        # Check if the argument is a linka and is valid
        if self.send_demo_started == True:
            if youtube_patter.match(Link) or soundcloud_patter.match(Link):
                if not ctx.author.name in self.demos_list:
                    self.demos_list[ctx.author.name] = Link
                    print(f"Se añadió el demo de {ctx.author.name} a la lista!")
                else:
                    await ctx.send(f"@{ctx.author.name} solo puedes enviar un demo!")
            else:
                await ctx.send(f"@{ctx.author.name} envia un enlace válido!")
        else:
            await ctx.send(f"@{ctx.author.name} eh perate! Todavía no puedes enviar un demo!")

    # Give away commands
    @commands.command(name="giveaway")
    async def giveawaystart(self, ctx, *args):
        # Check if there is text next to the comand and get the first word as an argument
        if len(args) > 0:
            command = args[0].lower()
        
        if self.add_check(ctx):
            # Start the participant collection 
            if command == "start":
                if self.give_away_started == False:
                    self.give_away_started = True
                    self.give_away_list.clear()
                    await ctx.send("Iniciamos con la recopilación de participantes para el sorteo. Recuerda seguirme para poder participar. Para entrar escribe el comando !leentro")

            # Finish the give away, save the list in a text file and copy it tol the clipboard
            if command == "finish":
                if self.give_away_started == True:
                    await ctx.send("La lista para entrar al sorte, ha finalizado! Suete a todos.")

                    with open(f"{self.ProjectPath}/Lista.txt", "w") as file:
                        for element in self.give_away_list:
                            file.write(f"{element}\n")
                        
                    print(f"Se ha guardado la lista de participantes correctame en la ruta: {self.ProjectPath}")
                    list_string = '\n'.join(map(str, self.give_away_list))
                    pyperclip.copy(list_string)
                    print(f"Se ha copiado la lista de participantes al portapapeles.")
                    self.give_away_started = False
            
            if command == "help":
                await ctx.send("Utiliza el comando !giveaway start, para iniciar una recopilación de participantes que se almacenarán en una lista. Los usuarios pueden entrar a la lista escribiendo el comando !leentro. Los usuarios deben seguir el canal para poder particiar.")
                await ctx.send(f"Utiliza el comando !giveaway finish, para concluir con la recopilación de participantes. Se creará un archivo de texto en la ruta {self.ProjectPath} con la lista de participantes. Adicionalmente se copiará la lista a tu portapapeles para mayor accesibilidad.")
                await ctx.send(f"Utiliza el comando !giveaway copyagain, para volver a copiar la lista de participantes en caso de que no encuentres el fichero o ya no se encuentre en el portapapeles.")

    @commands.command(name="enter")
    async def GiveAway(self, ctx):
        user = ctx.author.name

        if self.give_away_started == True:
            if user not in self.give_away_list:
                self.give_away_list.append(user)
                await ctx.send(f"{user} se unió a la rifa!")
        else:
            await ctx.send(f"{user} eh perate. ¿A dónde le quieres entrar?")