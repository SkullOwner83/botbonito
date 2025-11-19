import os
import flet as ft
from models.appconfig import AppConfig
from services.event_service import EventService
from services.moderation_manager import ModerationManager
from services.service_locator import ServiceLocator
from view.main_window import MainWindow
from view.routes import RouteHandler
from services import *
from utilities.file import File
from myapp import MyApp

def startup(page: ft.Page) -> None:
    os.makedirs(MyApp.config_path, exist_ok=True)
    app_config = AppConfig()

    try:
        app_config.open(MyApp.appconfig_path)
    except FileNotFoundError:
        app_config.save(MyApp.appconfig_path)

    try:
        credentials = File.open(MyApp.credentials_path)
    except FileNotFoundError:
        credentials = {
            "bot": { "access_token": "", "refresh_token": "" },
            "user": { "access_token": "", "refresh_token": "" }
        }

        File.save(MyApp.credentials_path, credentials)
    
    service_handler()
    route_handler = RouteHandler(page, app_config)
    main_window = MainWindow(page, route_handler, app_config, credentials)
        
# Create the service locator instance and register the services
def service_handler():
    ServiceLocator.register('bot', BotService())
    ServiceLocator.register('session', SessionService())
    ServiceLocator.register('websocket', WebsocketService())
    ServiceLocator.register('commands', CommandsManager())
    ServiceLocator.register('events', EventService())
    ServiceLocator.register('moderation', ModerationManager())

if __name__ == "__main__":
    ft.app(
        target=startup,
        assets_dir='assets'
        # ,view=ft.WEB_BROWSER,
    )