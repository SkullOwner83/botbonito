from typing import Callable
import flet as ft
from myapp import MyApp

class Tag(ft.Container):
    def __init__(self, text: str, on_remove: Callable) -> None:
        self.text = text
        self.on_remove = on_remove

        super().__init__(
            height=32,
            bgcolor=ft.Colors.GREY_300,
            border_radius=20,
            padding=ft.padding.only(left=16),
            content=self.build()
        )

    def build(self) -> ft.Column:
        return ft.Row(
            tight=True,
            spacing=0,
            controls=[
                ft.Text(
                    value=self.text,
                    size=16,
                    font_family=MyApp.font_secondary,
                ),

                ft.IconButton(ft.Icons.CLOSE, 
                    icon_size=16, 
                    width=32, 
                    height=32,
                    on_click=lambda e, a=self.text: self.on_remove(e, a)
                )
            ]
        )