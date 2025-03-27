import flet as ft
from myapp import MyApp

class Header(ft.Container):
    def __init__(self, tile):
        super().__init__()
        self.title = tile
        self.height = 64
        self.padding = ft.padding.symmetric(horizontal=32, vertical=12)
        self.border = ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.GREY_400))

        self.content = ft.Row(
            spacing=0,
            controls= [
                ft.Container(
                    ft.Text(
                        value=self.title,
                        font_family=MyApp.font_primary,
                        weight=ft.FontWeight.BOLD,
                        size=24
                    )
                ),

                ft.Container(
                    expand=True,
                    alignment=ft.alignment.center_right,
                    content=ft.Row(
                        alignment= ft.MainAxisAlignment.END,
                        controls=[
                            ft.IconButton(
                                width=40,
                                height=40,
                                icon=ft.Icons.NOTIFICATIONS,
                            ),

                            ft.Container(
                                width=40,
                                height=40,
                                aspect_ratio=1/1,
                                bgcolor=ft.Colors.GREY_300,
                                shape=ft.BoxShape.CIRCLE,
                                content=ft.Icon(name=ft.Icons.PERSON, color=ft.Colors.WHITE)
                            )
                        ]
                    )
                )
            ]
        )
