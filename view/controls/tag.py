from typing import Callable
import flet as ft

class Tag(ft.Container):
    def __init__(self, text: str, on_remove: Callable) -> None:
        super().__init__(
            height=32,
            bgcolor=ft.Colors.GREY_300,
            border_radius=20,
            padding=ft.padding.only(left=16),
            content=ft.Row(
                tight=True,
                spacing=0,
                controls=[
                    ft.Text(text),
                    ft.IconButton(ft.Icons.CLOSE, 
                        icon_size=16, 
                        width=32, 
                        height=32,
                        on_click=lambda e, a=text: on_remove(e, a)
                    )
                ]
            )
        )