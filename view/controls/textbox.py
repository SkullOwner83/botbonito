from typing import Callable, Optional
import flet as ft
from myapp import MyApp

class TextBox(ft.TextField):
    def __init__(
            self, 
            value: Optional[str] = '', 
            place_holder: Optional[str] = None,
            height: Optional[int] = 40,
            border: Optional[int] = 1,
            on_submit: Optional[Callable] = None,
            **kwargs
        ) -> None:
        super().__init__(
            value=value,
            expand=True,
            hint_text=place_holder,
            height=height,
            bgcolor=ft.Colors.WHITE,
            hover_color=ft.Colors.TRANSPARENT,
            text_vertical_align=ft.VerticalAlignment.CENTER,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=0),
            on_submit=on_submit,
            border_width=border,
            border_radius=8,

            border_color={
                ft.ControlState.DEFAULT: ft.Colors.GREY_300,
                ft.ControlState.HOVERED: ft.Colors.PRIMARY
            },

            text_style=ft.TextStyle(
                color=ft.Colors.BLACK,
                font_family=MyApp.font_secondary,
                size=16,
            ),

            hint_style=ft.TextStyle(
                color=ft.Colors.GREY,
                font_family=MyApp.font_secondary,
                size=16,
            ),
            **kwargs
        )