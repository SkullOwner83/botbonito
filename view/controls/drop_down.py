from typing import Optional, List
import flet as ft
from myapp import MyApp

class DropDown(ft.Dropdown):
    def __init__(self, value, options) -> None:
        super().__init__(
            expand=True,
            value=value,
            options=options,
            border_width=1,
            border_radius=8,
            border_color=ft.Colors.GREY_300,
            content_padding=ft.padding.symmetric(horizontal=16),
            text_style=ft.TextStyle(
                font_family=MyApp.font_secondary,
                size=16,
            )
        )