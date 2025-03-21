import flet as ft
from ..controls.menu_button import MenuButton

class NavigationBar(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.home_icon = "assets/icons/home.svg"
        self.commands_icon = "assets/icons/commands.svg"
        self.moderation_icon = "assets/icons/moderation.svg"
        self.configuration_icon = "assets/icons/configuration.svg"
        

        self.content = ft.Container(
            bgcolor=ft.Colors.WHITE,
            content=ft.Column(
                width=200,
                spacing=0,
                controls=[
                    ft.Container(
                        height=80,
                        padding=16,
                        content=ft.Image(src="assets/icons/botbonito.svg")
                    ),

                    MenuButton('Inicio', lambda e: self.page.go('/'), self.home_icon),
                    MenuButton('Comandos', lambda e: self.page.go('/commands'), self.commands_icon),
                    MenuButton('Moderación', lambda e: self.page.go('/moderation'), self.moderation_icon),
                    MenuButton('Configuración', lambda e: self.page.go('/configuration'), self.configuration_icon)
                ]
            )
        )