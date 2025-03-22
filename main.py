import sys
sys.path.append(r'D:\Desktop\Proyectos\Visual Studio Code\botbonito')
import flet as ft
import asyncio
import threading
from modules.token import Token
from modules.file import File
from bot.bot import Bot
from myapp import MyApp
from view.routes import Routes

class BotUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.title = "Botbonito"
        self.page.title = self.title
        self.page.window.width = 720
        self.page.window.height = 480
        self.page.window.always_on_top = True
        self.page.update()
        
        page.theme = ft.Theme(
            page_transitions=ft.PageTransitionsTheme(
                windows=ft.PageTransitionTheme.NONE
            )
        )

        self.bot = None

        self.routes = Routes(self.page)
        self.page.on_route_change = self.routes.route_change
        self.page.on_view_pop = self.routes.view_pop
        self.page.go(page.route)

        # Cargar configuración  
        self.credentials = File.open(MyApp.credentials_path)
        self.botconfig = File.open(MyApp.botconfig_path)
        self.token = self.credentials['token']

        self.load_page()
    
    def load_page(self):
        ValidToken = Token.validation(self.token)

        if ValidToken:
            self.run_bot()  
            self.page.go('/')
        else:
            pass
            self.page.go('/validation')

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
        MyApp.bot = bot
        await bot.start()

ft.app(target=lambda page: BotUI(page), assets_dir='assets')