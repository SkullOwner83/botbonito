import flet as ft
from ..controls.navigation_bar import NavigationBar

class CommandOption(ft.Container):
    def __init__(self, page: ft.Page):
        self.page = page

        self.content = ft.Row(

        )


class CommandsPage():
    def __init__(self, page: ft.Page):
        self.page = page

    def get_view(self) -> ft.View:
        return ft.View(
            route = '/commands',
            padding=0,
            controls = [
                ft.Container(
                    expand=True,
                    content=ft.Row(
                        spacing=0,
                        controls =[
                            NavigationBar(self.page),

                            ft.Container(
                                expand=True,
                                bgcolor=ft.Colors.GREY_100,
                                alignment=ft.alignment.center,
                                content=ft.Column(
                                    spacing=0,
                                )
                            )
                        ]
                    )
                )
            ]
        )