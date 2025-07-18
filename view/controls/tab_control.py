import flet as ft
from myapp import MyApp

class TabControl(ft.Tabs):
    def __init__(self, **kwargs):
        super().__init__(
            indicator_thickness=3,
            divider_height=1,
            divider_color=ft.Colors.GREY_300,
            label_padding=ft.padding.symmetric(horizontal=8, vertical=0),
            indicator_tab_size=True,
            label_text_style=ft.TextStyle(
                font_family=MyApp.font_primary,
                weight=ft.FontWeight.BOLD,
                size=16,
            ),
            **kwargs
        )