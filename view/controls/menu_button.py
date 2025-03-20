import flet as ft
from typing import Callable

class MenuButton(ft.Container):
    def __init__(self, text: str, onclick: Callable = None, icon: str = None):
        super().__init__()
        self.text = text
        self.icon = icon

        self.height = 32
        self.bgcolor = ft.Colors.WHITE
        self.padding = ft.padding.symmetric(horizontal=16)
        self.on_hover = self.hover_event
        self.on_click = onclick
        
        self.content = ft.Row (
            spacing=8,
            controls = [
                ft.Container(
                     width=18,
                     height=18,
                     content=ft.Image(src=self.icon),
                ),

                ft.Text(
                    value=text,
                    font_family='Arial Narrow',
                    size=16
                ),
            ]
        )
    
    def hover_event(self, e: ft.ControlEvent):
            self.bgcolor = "#e9e9e9" if e.data == "true" else ft.Colors.WHITE
            self.update()