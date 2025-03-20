import flet as ft
from ..controls.menu_button import MenuButton

class NavigationBar(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        self.content = ft.Container(
            bgcolor=ft.Colors.WHITE,
            content=ft.Column(
                width=150,
                spacing=0,
                controls=[
                    MenuButton('Inicio', lambda e: self.page.go('/')),
                    MenuButton('Comandos', lambda e: self.page.go('/commands')),
                    MenuButton('Moderación', lambda e: self.page.go('/moderation')),
                    MenuButton('Configuración', lambda e: self.page.go('/configuration'))
                ]
            )
        )