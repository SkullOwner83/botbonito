import flet as ft
from view.main_window import MainWindow
from services.botservice import BotService
from view.routes import RouteHandler
from view.modals import *

def startup(page: ft.Page) -> None:
    bot_services = BotService()
    route_handler = RouteHandler(page, bot_services)
    main_window = MainWindow(page, route_handler, bot_services)

if __name__ == "__main__":
    ft.app(
        target=startup,
        assets_dir='assets'
        #view=ft.WEB_BROWSER,
    )