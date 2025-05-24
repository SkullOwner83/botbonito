from typing import List, Callable
import flet as ft
from myapp import MyApp

class SegmentedButton(ft.SegmentedButton):
    def __init__(self, *, segments: List[ft.Segment], on_change: Callable = None) -> None:
        super().__init__(
            height=32,
            allow_multiple_selection=False,
            allow_empty_selection=False,
            show_selected_icon=False,
            selected={"1"},
            segments=segments,
            on_change=on_change,
            
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.padding.symmetric(horizontal=16),
                side=ft.BorderSide(width=0, color=ft.Colors.TRANSPARENT),
                bgcolor={
                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                    ft.ControlState.SELECTED: ft.Colors.PRIMARY
                },
                
                text_style={
                    ft.ControlState.DEFAULT: ft.TextStyle(
                        foreground=ft.Paint(color=ft.Colors.BLACK),
                        font_family=MyApp.font_primary,
                        weight=ft.FontWeight.BOLD,
                        size=16
                    ),

                    ft.ControlState.SELECTED: ft.TextStyle(
                        foreground=ft.Paint(color=ft.Colors.ON_PRIMARY),
                        font_family=MyApp.font_primary,
                        weight=ft.FontWeight.BOLD,
                        size=16
                    ),
                }
            ),
        )