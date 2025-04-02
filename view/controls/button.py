import flet as ft
from typing import Callable
from myapp import MyApp

class Button(ft.FilledButton):
    def __init__(self, text: str, style: str = 'Filled', padding: ft.PaddingValue = None, **kwargs) -> None:
        super().__init__(
            text=text,
            height=32,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.PRIMARY,
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.padding.symmetric(horizontal=16) if padding is None else padding,
                text_style=ft.TextStyle(
                    foreground=ft.Paint(color=ft.Colors.WHITE),
                    font_family=MyApp.font_primary,
                    weight=ft.FontWeight.BOLD,
                    size=16
                )
            ) 
            if style == 'Filled' else 
            ft.ButtonStyle(
                bgcolor=ft.Colors.TRANSPARENT,
                side=ft.BorderSide(width=1, color=ft.Colors.GREY_800),
                shape=ft.RoundedRectangleBorder(radius=8),
                text_style=ft.TextStyle(
                    foreground=ft.Paint(color=ft.Colors.GREY_800),
                    font_family=MyApp.font_primary,
                    weight=ft.FontWeight.BOLD,
                    size=16
                )
            ),
            **kwargs
        )