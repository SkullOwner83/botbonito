import flet as ft
from ..controls import NavigationBar

class HomePage:
    def __init__(self, page: ft.Page):
        self.page = page

    def get_view(self) -> ft.View:
        return ft.View(
            route = '/',
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
                                content=ft.Text(value="Página de inicio.")
                            )
                        ]
                    )
                )
            ]
        )