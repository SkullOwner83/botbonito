import flet as ft
from ..controls import *
from services import *

class ConfigurationPage(ft.View):
    def __init__(self, page: ft.Page, botconfig: dict):
        super().__init__(
            route='/configuration',
            padding=0,
        )

        self.page = page
        self.botconfig = botconfig
        self.controls.append(self.build())

    def build(self) -> ft.Container:
        return ft.Container(
            expand=True,
            bgcolor=ft.Colors.GREY_100,
            content=ft.Row(
                expand=True,
                spacing=0,
                controls =[
                    NavigationBar(self.page),

                    ft.Column(
                        expand=True,
                        spacing=0,
                        controls=[
                            Header("Configuración", self.botconfig),

                            ft.Container(
                                expand=True,
                                bgcolor=ft.Colors.GREY_100,
                                alignment=ft.alignment.center,
                                content=ft.Text(value="Página de configuración.")
                            )
                        ]
                    )
                ]
            )
        )