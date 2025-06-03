import flet as ft
from ..controls import *
from services import *

class ModerationPage(ft.View):
    def __init__(self, page: ft.Page, botconfig: dict, session_service: SessionService, websocket_service: WebsocketService):
        super().__init__(
            route='/validation',
            padding=0
        )

        self.page = page
        self.botconfig = botconfig
        self.session_service = session_service
        self.websocket_service = websocket_service
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
                            Header("Moderación", self.botconfig, self.session_service, self.websocket_service),

                            ft.Container(
                                expand=True,
                                bgcolor=ft.Colors.GREY_100,
                                alignment=ft.alignment.center,
                                content=ft.Text(value="Página de moderación.")
                            )
                        ]
                    )
                ]
            )
        )