import flet as ft
from utilities.constants import Constants
from myapp import MyApp

class Badge(ft.Container):
    def __init__(self, name: str) -> None:
        super().__init__(
            content=ft.Row(
                spacing=4,
                controls=[
                    ft.Image(
                        src=Constants.USER_LEVEL_ICONS.get(name),
                        width=20,
                        height=20,
                    ),

                    ft.Text(
                        value=name,
                        font_family=MyApp.font_secondary,
                        weight=ft.FontWeight.BOLD
                    )
                ]
            )
        )

