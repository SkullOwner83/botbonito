import flet as ft
from ..controls import NavigationBar

class HomePage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(
            route='/',
            padding=0
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
                        content=ft.Text(value="Página de inicio.")
                    )
                ]
            )
        )