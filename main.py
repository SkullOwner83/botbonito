import flet as ft
from view.main_window import MainWindow
from view.routes import RouteHandler
from services import *
from view.modals import *
from utilities.file import File
from myapp import MyApp

def startup(page: ft.Page) -> None:
    botconfig = File.open(MyApp.botconfig_path)
    credentials = File.open(MyApp.credentials_path)
    
    bot_services = BotService()
    session_service = SessionService()
    websocket_service = WebsocketService()
    route_handler = RouteHandler(page, botconfig, bot_services, session_service)
    main_window = MainWindow(page, route_handler, botconfig, credentials, bot_services, session_service, websocket_service)

if __name__ == "__main__":
    ft.app(
        target=startup,
        assets_dir='assets'
        #view=ft.WEB_BROWSER,
    )