import flet as ft
from myapp import MyApp

class DropDown(ft.Dropdown):
    def __init__(self, value, options) -> None:
        super().__init__(
            expand=True,
            value=value,
            options=options,
            color=ft.Colors.BLACK,
            bgcolor=ft.Colors.WHITE,
            filled=True,
            fill_color=ft.Colors.WHITE,
            border_width=1,
            border_radius=8,
            border_color=ft.Colors.GREY_500,
            content_padding=ft.padding.symmetric(horizontal=16),
            text_style=ft.TextStyle(
                font_family=MyApp.font_secondary,
                size=16,
            )
        )