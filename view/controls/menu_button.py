import flet as ft
from typing import Callable

class MenuButton(ft.Container):
    def __init__(self, text: str, onclick: Callable = None, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.bgcolor = '#fff'
        self.padding = ft.padding.symmetric(horizontal=16, vertical=8)
        self.on_hover = self.hover_event
        self.on_click = onclick
        
        self.content = ft.Row (
            controls = [
                ft.Text(
                    value=text,
                    font_family='Arial',
                    size=16
                ),
            ]
        )
    
    def hover_event(self, e: ft.ControlEvent):
            self.bgcolor = "#e9e9e9" if e.data == "true" else "#fff" 
            self.update()