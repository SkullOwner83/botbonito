from typing import Optional
import flet as ft
from myapp import MyApp

class Card(ft.Container):
    def __init__(
        self, 
        text: Optional[str] = None, 
        icon: Optional[ft.IconValue] = None,
        value: Optional[int] = 0,
        **kwargs
    ) -> None:
        self.text = text
        self.icon = icon
        self.value = value

        super().__init__(
            expand=True,
            bgcolor=ft.Colors.WHITE,
            border_radius=8,
            padding=8,
            content=self.build(),
            **kwargs
        )

    def build(self):
        return ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            controls=[
                ft.Icon(name=self.icon),

                ft.Text(
                    value=self.value,
                    font_family=MyApp.font_secondary,
                    weight=ft.FontWeight.BOLD,
                    size=24
                ),

                ft.Text(
                    value=self.text, 
                    font_family=MyApp.font_secondary,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                    size=16),
            ]
        )