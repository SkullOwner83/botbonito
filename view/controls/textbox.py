from typing import Callable
import flet as ft
from myapp import MyApp

class TextBox(ft.TextField):
    def __init__(self, value: str = '', on_submit: Callable = None) -> None:
        super().__init__(
            height=40,
            bgcolor=ft.Colors.WHITE,
            value=value,
            content_padding=ft.padding.symmetric(horizontal=16),
            on_submit=on_submit,
            border_width=1,
            border_radius=8,
            border_color=ft.Colors.GREY_300,

            text_style=ft.TextStyle(
                font_family=MyApp.font_secondary,
                size=16,
            )
        )