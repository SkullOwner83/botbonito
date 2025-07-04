import flet as ft
from ..controls import *
from services import *


class HomePage(ft.View):
    def __init__(self, page: ft.Page, botconfig: dict) -> None:
        super().__init__(
            route='/',
            padding=0
        )

        self.page = page
        self.botconfig = botconfig
        self.controls.append(self.build())

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
                            Header("Dashboard", self.botconfig),

                            ft.Container(
                                padding=32,
                                content=ft.Column(
                                    spacing=20,
                                    controls=[
                                        ft.Row(
                                            height=32,
                                            controls=[
                                                ft.IconButton(width=32, icon=ft.Icons.ARROW_BACK_IOS_ROUNDED),

                                                ft.Container(
                                                    expand=True,
                                                    bgcolor=ft.Colors.WHITE,
                                                    alignment=ft.alignment.center,
                                                    border_radius=8,
                                                    content=ft.Text(
                                                        value="jueves, 22 de mayo",
                                                        color=ft.Colors.PRIMARY,
                                                        weight=ft.FontWeight.BOLD,
                                                        size=16
                                                    )
                                                ),

                                                ft.IconButton(width=32, icon=ft.Icons.ARROW_FORWARD_IOS_ROUNDED)
                                            ]
                                        ),

                                        ft.ResponsiveRow(
                                            columns=4,
                                            spacing=20,
                                            run_spacing=20,
                                            controls=[
                                                Card(text="Seguidores", icon=ft.Icons.FAVORITE, col={ "xs": 4, "sm": 2, "md": 1 }),
                                                Card(text="Suscriptores", icon=ft.Icons.STAR, col={ "xs": 4, "sm": 2, "md": 1 }),
                                                Card(text="Vistas", icon=ft.Icons.REMOVE_RED_EYE, col={ "xs": 4, "sm": 2, "md": 1 }),
                                                Card(text="Bits", icon=ft.Icons.PAYMENTS, col={ "xs": 4, "sm": 2, "md": 1 })
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