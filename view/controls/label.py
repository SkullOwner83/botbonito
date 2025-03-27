import flet as ft
from myapp import MyApp

class Label(ft.Text):
    def __init__(self, text:str):
        super().__init__(
            value=text,
            font_family=MyApp.font_primary,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK,
            size=16,
        )