from modules.file import File
from modules.token import Token
from myapp import MyApp
import flet as ft
from ..controls.navigation_bar import NavigationBar

class ConfigurationPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(
            route='/validation',
            padding=0,
        )

        self.page = page
        self.controls.append(self.build())

    def build(self) -> ft.Container:
        return ft.Container(
            expand=True,
            content=ft.Row(
                spacing=0,
                controls =[
                    NavigationBar(self.page),

                    ft.Container(
                        expand=True,
                        bgcolor=ft.Colors.GREY_100,
                        alignment=ft.alignment.center,
                        content=ft.Text(value="Página de configuración.")
                    )
                ]
            )
        )