from typing import Optional
import flet as ft
from myapp import MyApp

class Label(ft.Text):
    def __init__(self, text:str, color: ft.Colors = ft.Colors.BLACK, weigth: ft.FontWeight = ft.FontWeight.BOLD, **kwargs) -> None:
        super().__init__(
            value=text,
            font_family=MyApp.font_primary,
            weight=weigth,
            color=color,
            size=16,
            **kwargs
        )

    @property
    def text(self):
        return self.value

    @text.setter
    def text(self, value):
        self.value = value