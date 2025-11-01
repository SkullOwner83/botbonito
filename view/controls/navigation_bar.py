import flet as ft
from typing import Callable, Optional
from myapp import MyApp

class NavigationBar(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.current_route = page.route
        self.menu_buttons = []

        self.home_icon = ft.Icons.HOME_FILLED
        self.commands_icon = ft.Icons.TERMINAL_ROUNDED
        self.moderation_icon = ft.Icons.SHIELD_ROUNDED
        self.configuration_icon = ft.Icons.SETTINGS_ROUNDED
        self.set_controls()

        super().__init__(
            bgcolor=ft.Colors.WHITE,
            content=self.build(),
            
        )
        
    # Deselect the currently selected button to allow selecting the newly pressed one
    def select_button(self, route: str):
        for button in self.menu_buttons:
            if button.route == self.current_route:
                button.state = ft.ControlState.DEFAULT
                button.set_colors()
                button.update()
                break

        self.current_route = route

    def set_controls(self):
        self.menu_buttons = [
            MenuButton('Inicio', self.home_icon, '/', self),
            MenuButton('Comandos', self.commands_icon, '/commands', self),
            MenuButton('Moderación', self.moderation_icon, '/moderation', self),
            MenuButton('Configuración', self.configuration_icon, '/configuration', self)
        ]

    def build(self):
        return ft.Column(
            width=200,
            spacing=0,
            controls=[
                ft.Container(
                    height=64,
                    padding=16,
                    content=ft.Image(src="side menu/botbonito.svg", width=150)
                ),

                ft.ListView(
                    expand=True,
                    padding=ft.padding.symmetric(horizontal=8),
                    controls=self.menu_buttons
                )
            ]
        )

class MenuButton(ft.Container):
    def __init__(self, text: str, icon: str, route: str, navigation_bar: NavigationBar) -> None:
        self.text = text
        self.icon = icon
        self.route = route
        self.navigation_bar = navigation_bar
        self.state = ft.ControlState.SELECTED if self.navigation_bar.page.route == self.route else ft.ControlState.DEFAULT

        self.button_icon = ft.Icon(name=self.icon)
        self.button_text = ft.Text(
            value=self.text,
            font_family=MyApp.font_primary,
            weight= ft.FontWeight.BOLD,
            size=16
        )
        
        super().__init__(
            height=32,
            border_radius=8,
            padding=ft.padding.symmetric(horizontal=8),
            on_hover=self.handle_hover,
            on_click = self.handle_click
        )

        self.set_colors()
        self.content = self.build()

    def handle_click(self, e: ft.ControlEvent) -> None:
        if not self.state == ft.ControlState.SELECTED:
            self.navigation_bar.select_button(self.route)
            self.state = ft.ControlState.SELECTED
            self.page.go(self.route)
            self.set_colors()
            self.update()

    def handle_hover(self, e: ft.ControlEvent) -> None:
        if not self.state == ft.ControlState.SELECTED:
            self.state = ft.ControlState.HOVERED if e.data == "true" else ft.ControlState.DEFAULT
            self.set_colors()
            self.update()

    def set_colors(self):
        match(self.state):
            case ft.ControlState.SELECTED:
                foreground = ft.Colors.PRIMARY
                background = ft.Colors.with_opacity(0.2, ft.Colors.PRIMARY)
            case ft.ControlState.HOVERED:
                foreground = ft.Colors.BLACK
                background = ft.Colors.GREY_100
            case _:
                foreground = ft.Colors.BLACK
                background = ft.Colors.WHITE
        
        self.bgcolor = background
        self.button_icon.color = foreground
        self.button_text.color = foreground

    def build(self) -> ft.Row:
        return ft.Row(
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls = [
                self.button_icon,
                self.button_text
            ]
        )