import flet as ft
from typing import Callable
from myapp import MyApp

class NavigationBar(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.home_icon = "icons/home.svg"
        self.commands_icon = "icons/commands.svg"
        self.moderation_icon = "icons/moderation.svg"
        self.configuration_icon = "icons/configuration.svg"

        super().__init__(
            bgcolor=ft.Colors.WHITE,
            content=self.build()
        )
    
    def build(self):
        return ft.Column(
            width=200,
            spacing=0,
            controls=[
                ft.Container(
                    height=64,
                    padding=16,
                    content=ft.Image(src="icons/botbonito.svg", width=150)
                ),

                MenuButton('Inicio', self.home_icon, lambda e: self.page.go('/')),
                MenuButton('Comandos', self.commands_icon, lambda e: self.page.go('/commands')),
                MenuButton('Moderación', self.moderation_icon, lambda e: self.page.go('/moderation')),
                MenuButton('Configuración', self.configuration_icon, lambda e: self.page.go('/configuration'))
            ]
        )


class MenuButton(ft.Container):
    def __init__(self, text: str, icon: str, onclick: Callable = None) -> None:
        super().__init__(
            height=32,
            bgcolor=ft.Colors.WHITE,
            padding=ft.padding.symmetric(horizontal=16),
            on_hover=self.hover_event
        )

        self.text = text
        self.icon = icon
        self.hover_color = ft.Colors.GREY_300
        self.on_click = onclick
        self.content = self.build()

    def build(self) -> ft.Row:
        return ft.Row(
            spacing=8,
            controls = [
                ft.Container(
                    width=18,
                    height=18,
                    content=ft.Image(src=self.icon),
                ),

                ft.Text(
                    value=self.text,
                    color= ft.Colors.BLACK,
                    font_family=MyApp.font_primary,
                    weight= ft.FontWeight.BOLD,
                    size=16
                ),
            ]
        )
    
    def hover_event(self, e: ft.ControlEvent) -> None:
            self.bgcolor = self.hover_color if e.data == "true" else ft.Colors.WHITE
            self.update()