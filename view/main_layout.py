import flet as ft
from typing import Optional
from models.appconfig import AppConfig
from view.controls import NavigationBar, Header

class MainLayout(ft.View):
    def __init__(self, page: ft.Page, app_config: AppConfig, content: Optional[ft.Control] = None):
        self.page = page
        self.app_config = app_config

        self.content_container = ft.Container(
            expand=True,
            alignment=ft.alignment.top_center,
            content=content
        )

        super().__init__(
            padding=0,
            controls=[
                ft.Container(
                    expand=True,
                    bgcolor=ft.Colors.GREY_100,
                    content=ft.Row(
                        expand=True,
                        spacing=0,
                        controls=[
                            NavigationBar(self.page),
                            ft.Column(
                                expand=True,
                                spacing=0,
                                controls=[
                                    Header("Comandos", app_config),
                                    self.content_container
                                ],
                            ),
                        ],
                    ),
                )
            ]
        )

    def set_content(self, new_content: ft.Control):
        """Actualiza solo el contenido central sin recargar el layout completo."""
        self.content_container.content = new_content
        self.content_container.update()