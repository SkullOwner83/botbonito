from typing import List
import flet as ft
from myapp import MyApp

class DataTable(ft.Container):
    def __init__(self, *, columns: List[ft.DataColumn], rows: List[ft.DataRow] = None, visible: bool = True) -> None:
        super().__init__()
        self.expand = True
        self.visible = visible
        self.columns = columns
        self.rows = rows or []
        self.bgcolor=ft.Colors.WHITE
        self.border_radius=8

        self.content = ft.Column(
            expand=True,
            spacing=0,
            scroll=ft.ScrollMode.ADAPTIVE,
            controls=[
                ft.Row(
                    controls=[
                        ft.DataTable(
                            expand=True,
                            column_spacing=32,
                            columns=self.columns,
                            rows=self.rows,
                            heading_row_height=32,
                            data_row_max_height=48,

                            heading_text_style=ft.TextStyle(
                                font_family=MyApp.font_primary,
                                weight=ft.FontWeight.BOLD,
                                size=16
                            ),

                            data_text_style=ft.TextStyle(
                                font_family=MyApp.font_secondary,
                                size=16
                            )
                        )
                    ]
                )
            ]
        )