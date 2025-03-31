import sys
sys.path.append(r'D:\Desktop\Proyectos\Visual Studio Code\botbonito')
import asyncio
import threading
from flet import Page, Theme, app
from flet import PageTransitionsTheme, PageTransitionTheme
from view.routes import Routes
from modules.token import Token
from modules.file import File
from bot.bot import Bot
from myapp import MyApp

class BotUI:
    def __init__(self, page: Page):
        self.page = page
        self.title = "Botbonito"
        self.page.title = self.title
        self.page.window.width = 800
        self.page.window.height = 600
        self.page.window.always_on_top = True #This property is temporary, used only to maintain the app on top while it is beign designed
        self.page.update()

        self.routes = Routes(self.page)
        self.page.on_route_change = self.routes.route_change
        self.page.on_view_pop = self.routes.view_pop
        self.page.go(page.route)

        page.theme = Theme(
            page_transitions=PageTransitionsTheme(
                windows=PageTransitionTheme.NONE
            )
        )

        self.credentials = File.open(MyApp.credentials_path)
        self.botconfig = File.open(MyApp.botconfig_path)
        self.token = self.credentials['token']
        self.bot = None

        self.load_page()
    
    def load_page(self) -> None:
        ValidToken = Token.validation(self.token)

        if ValidToken:
            self.run_bot()
            self.page.go('/')
        else:
            pass
            self.page.go('/validation')

    def run_bot(self) -> None:
        thread = threading.Thread(target=self.run_bot_in_thread)
        thread.start()
        thread.join() 

    def run_bot_in_thread(self) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.main())

    async def main(self) -> None:
        bot = Bot(self.botconfig, self.credentials)
        MyApp.bot = bot
        await bot.start()

if __name__ == "__main__":
    app(
        target=lambda page: BotUI(page),
        assets_dir='assets'
        #view=ft.WEB_BROWSER,
    )