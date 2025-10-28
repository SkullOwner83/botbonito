import flet as ft
from myapp import MyApp

class DropDown(ft.Stack):
    def __init__(self, value, options) -> None:
        self.dropdown = ft.Dropdown(
            expand=True,
            value=value,
            options=options,
            color=ft.Colors.BLACK,
            bgcolor=ft.Colors.WHITE,
            filled=False,
            border_width=1,
            border_radius=8,
            border_color=ft.Colors.GREY_500,
            content_padding=ft.padding.symmetric(horizontal=16),
            text_style=ft.TextStyle(
                font_family=MyApp.font_secondary,
                size=16,
            )
        )

        super().__init__(
            expand=True,
            height=40,
            controls=[
                ft.Container(
                    bgcolor=ft.Colors.WHITE,
                    border_radius=8,
                    content=self.dropdown
                ),

                ft.Container(
                    top=1,
                    right=4,
                    width=40,
                    height=38,
                    border_radius=8,
                    bgcolor=ft.Colors.WHITE,
                    ignore_interactions=True,
                    alignment=ft.alignment.center,
                    content=ft.Icon(name=ft.Icons.KEYBOARD_ARROW_DOWN_ROUNDED, color=ft.Colors.GREY_600, size=32,)
                )
            ]
        )

    @property
    def value(self):
        return self.dropdown.value

    @value.setter
    def value(self, val):
        self.dropdown.value = val

    @property
    def options(self):
        return self.dropdown.options

    @options.setter
    def options(self, opts):
        self.dropdown.options = opts

    def on_change(self, handler):
        self.dropdown.on_change = handler