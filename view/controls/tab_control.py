import flet as ft
from myapp import MyApp

class TabControl(ft.Tabs):
    def __init__(self, **kwargs) -> None:
        super().__init__(
            scrollable=True,
            indicator_tab_size=True,
            indicator_thickness=4,
            divider_height=1,
            divider_color=ft.Colors.GREY_300,
            unselected_label_color=ft.Colors.GREY_500,
            label_padding=ft.padding.symmetric(horizontal=16, vertical=0),
            label_text_style=ft.TextStyle(
                font_family=MyApp.font_primary,
                weight=ft.FontWeight.BOLD,
                size=16,
            ),
            **kwargs
        )