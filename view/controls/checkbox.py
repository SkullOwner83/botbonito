from typing import Optional
import flet as ft
from myapp import MyApp

class CheckBox(ft.Checkbox):
    def __init__(self, text: str, checked: Optional[bool] = False, **kwargs):
        super().__init__(
            label=text,
            value=checked,
            label_style=ft.TextStyle(
                foreground=ft.Paint(color=ft.Colors.GREY_700),
                font_family=MyApp.font_primary,
                weight=ft.FontWeight.BOLD,
                size=16
            )
        )