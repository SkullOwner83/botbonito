import flet as ft
from view.controls import *
from models.appconfig import AppConfig

class EventsPage(ft.Container):
    def __init__(self, page: ft.Page, app_config: AppConfig) -> None:
        self.page = page
        self.theme = page.theme.color_scheme
        self.app_config = app_config
        super().__init__(padding=32, content=self.build())

    def build(self) -> ft.Container:
        return ft.Container(
            expand=True,
            content=ft.Text('Sorteos')
        )