import flet as ft
from ..controls import *
from services import *

class ModerationPage(ft.View):
    def __init__(self, page: ft.Page, botconfig: dict):
        super().__init__(
            route='/moderation',
            padding=0
        )

        self.page = page
        self.botconfig = botconfig
        self.controls.append(self.build())

    def change_tab(self, e: ft.ControlEvent):
        pass

    def build(self) -> ft.Container:
        return ft.Container(
            expand=True,
            bgcolor=ft.Colors.GREY_100,
            content=ft.Row(
                expand=True,
                spacing=0,
                controls =[
                    NavigationBar(self.page),

                    ft.Column(
                        expand=True,
                        spacing=0,
                        controls=[
                            Header("Moderación", self.botconfig),

                            ft.Container(
                                expand=True,
                                padding=32,
                                content=ft.Column(
                                    spacing=20,
                                    controls=[
                                        SegmentedButton(
                                            on_change=self.change_tab,
                                            segments=[
                                                ft.Segment(value='1', label=ft.Text('Protecciones')),
                                                ft.Segment(value='2', label=ft.Text('Palabras prohibidas'))
                                            ]
                                        ),

                                        ft.ResponsiveRow(
                                            controls=[
                                                Card(),
                                                Card(),
                                                Card()
                                            ]
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                ]
            )
        )