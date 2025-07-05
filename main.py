import os
import flet as ft
from services.moderation_manager import ModerationManager
from services.service_locator import ServiceLocator
from view.main_window import MainWindow
from view.routes import RouteHandler
from services import *
from view.modals import *
from utilities.file import File
from myapp import MyApp

def startup(page: ft.Page) -> None:
    if os.path.exists(MyApp.config_path):
        botconfig = File.open(MyApp.botconfig_path)
        credentials = File.open(MyApp.credentials_path)
    else:
        os.makedirs(MyApp.config_path)
    
    service_handler()
    route_handler = RouteHandler(page, botconfig)
    main_window = MainWindow(page, route_handler, botconfig, credentials)

# Create the service locator instance and register the services
def service_handler():
    ServiceLocator.register('session', SessionService())
    ServiceLocator.register('bot', BotService())
    ServiceLocator.register('websocket', WebsocketService())
    ServiceLocator.register('commands', CommandsManager())
    ServiceLocator.register('moderation', ModerationManager())

if __name__ == "__main__":
    ft.app(
        target=startup,
        assets_dir='assets'
        #view=ft.WEB_BROWSER,
    )