import flet as ft
from myapp import MyApp

class Modal(ft.AlertDialog):
    def __init__(
            self, 
            title: str ='', 
            content = None, 
            actions = None,
            bgcolor = ft.Colors.WHITE,
            title_alignment: ft.TextAlign = ft.TextAlign.CENTER,
            actions_alignment: ft.MainAxisAlignment = ft.MainAxisAlignment.END,
    ) -> None:
        super().__init__(
            title=ft.Text(title, text_align=title_alignment, font_family=MyApp.font_primary, weight=ft.FontWeight.BOLD),
            title_padding=ft.padding.only(left=32, right=32, top=32, bottom=0),
            content_padding=32,
            action_button_padding=16,
            inset_padding=32,
            shape=ft.RoundedRectangleBorder(radius=16),
            modal=False,
            bgcolor=bgcolor,
            actions_alignment=actions_alignment,
            content=ft.Container(
                width=400,
                content=content,
            ),
            actions=actions
        )