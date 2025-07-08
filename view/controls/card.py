from typing import Optional
import flet as ft
from myapp import MyApp

class Card(ft.Container):
    def __init__(
        self, 
        title: Optional[str] = None,
        title_alignment: Optional[ft.TextAlign] = ft.TextAlign.CENTER,
        description: Optional[str] = None,
        header: Optional[ft.Control] = None,
        footer: Optional[ft.Control] = None,
        icon: Optional[ft.IconValue] = None,
        value: Optional[int] = None,
        padding: Optional[int] = 8,
        **kwargs
    ) -> None:
        self.title = title
        self.text_alignment = title_alignment
        self.description = description
        self.header = header
        self.footer = footer
        self.icon = icon
        self.value = value
        self.set_controls()

        super().__init__(
            expand=True,
            bgcolor=ft.Colors.WHITE,
            border_radius=8,
            padding=padding,
            content=self.build(),
            **kwargs
        )

    def set_controls(self):
        self.icon_control = [ft.Icon(name=self.icon)] if self.icon else []
        self.value_control = [
            ft.Text(
                value=self.value,
                font_family=MyApp.font_secondary,
                weight=ft.FontWeight.BOLD,
                size=24
            )
        ] if self.value else []

    def build(self):
        return ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            controls=[
                *self.icon_control,
                ft.Container(self.header),
                *self.value_control,

                ft.Text(
                    value=self.title,
                    font_family=MyApp.font_secondary,
                    weight=ft.FontWeight.BOLD,
                    text_align=self.text_alignment,
                    size=16),
                
                ft.Text(
                    value=self.description,
                    color=ft.Colors.GREY_700,
                    font_family=MyApp.font_secondary,
                    size=16
                ),

                ft.Container(self.footer)
            ]
        )