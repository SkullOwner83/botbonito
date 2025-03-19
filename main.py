import sys
sys.path.append(r'D:\Desktop\Proyectos\Visual Studio Code\botbonito')
from modules.token import Token
from modules.file import File
from bot.bot import Bot
from myapp import MyApp

import flet as ft
import asyncio
import threading


class BotUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.title = "Botbonito"
        page.title = self.title
        page.window.width = 420
        page.window.height = 420
        page.window.resizable = False
        page.update()
        
        self.bot = None

        page.on_route_change = self.route_change
        page.on_view_pop = self.view_pop
        page.go(page.route)
        
        # Cargar configuración
        self.credentials = File.open(MyApp.credentials_path)
        self.botconfig = File.open(MyApp.botconfig_path)
        self.token = self.credentials['token']
        self.client_id = self.credentials['client_id']
        self.client_secret = self.credentials['client_secret']
        self.redirect_uri = self.botconfig['redirect_uri']
        self.scope = self.botconfig['scope']

        self.load_page()
    
    def load_page(self):
        ValidToken = Token.validation(self.token)

        if ValidToken:
            self.run_bot()
            self.page.go('/')
        else:
            self.page.go('/validation')

    def route_change(self, e: ft.RouteChangeEvent) -> None:
        self.page.views.clear()

        if self.page.route == '/':
            self.page.views.append(
                ft.View(
                    route='/',
                    controls = [
                        ft.Text(value="¡Hola! Soy el bot bonito.")
                    ]
                )
            )

        if self.page.route == '/validation':
            self.page.views.append(
                ft.View(
                    controls=[
                        ft.Row(controls=[ft.Text(value="Tu token no es valido. Ingresa al siguiente sitio para obtener un nuevo token.", )]),
                        ft.Row(
                            controls = [
                                ft.Button(text="Abrir", width=100, on_click=self.token_validation),
                                ft.Button(text="Copiar", width=100)
                            ],
                            alignment = ft.MainAxisAlignment.CENTER 
                        )
                    ]
                )
            )

        self.page.update()

    def view_pop(self, e: ft.ViewPopEvent) -> None:
        self.page.views.pop()
        top_view: ft.View = self.page.views[-1]
        self.page.route = top_view.route

    def token_validation(self, e: ft.ControlEvent):
        token = Token(self.client_id, self.client_secret, self.scope, self.redirect_uri)
        NewToken = token.get_authorization('copy_link')

        if token.validation(NewToken):
            self.credentials['token'] = NewToken
            File.save(MyApp.credentials_path, self.credentials)
            self.page.go('/validation')
            self.run_bot()

        else:
            print("Token invalido")


    def run_bot(self):
        thread = threading.Thread(target=self.run_bot_in_thread)
        thread.start()
        thread.join() 

    def run_bot_in_thread(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.main())

    async def main(self):
        bot = Bot(self.botconfig, self.credentials)
        await bot.start()

def main(page: ft.Page):
    BotUI(page)

ft.app(target=main)


"""
# Load config and variable values from files
credentials = File.open(MyApp.credentials_path)
botconfig = File.open(MyApp.botconfig_path)

token = credentials['token']
client_id = credentials['client_id']
client_secret = credentials['client_secret']
redirect_uri = botconfig['redirect_uri']
scope = botconfig['scope']

# Check if the Oauth Token of bot account is valid or hasn't expired yet.
ValidToken = Token.validation(token)

while ValidToken == False:
    print("Tu token no es valido. Ingresa al siguiente sitio para obtener un nuevo token:")
    token = Token(client_id, client_secret, scope, redirect_uri)
    NewToken = token.get_authorization()
    
    if token.validation(NewToken):
        credentials['token'] = NewToken
        File.save(MyApp.credentials_path, credentials)
        print("Token validado")
        ValidToken = True

# Execute bot on loop
if __name__ == '__main__':
    botbonito = Bot(botconfig, credentials)
    botbonito.run()
"""