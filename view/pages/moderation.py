import flet as ft

from models.protection import Protection
from services.moderation_manager import ModerationManager
from ..controls import *
from services import *

class ModerationPage(ft.View):
    def __init__(self, page: ft.Page, botconfig: dict) -> None:
        super().__init__(
            route='/moderation',
            padding=0
        )

        moderation_manager: ModerationManager = ServiceLocator.get('moderation')
        self.protections: dict[str, Protection] = moderation_manager.protections

        self.page = page
        self.botconfig = botconfig
        self.set_controls()
        self.controls.append(self.build())

    def set_controls(self):
        self.row = ft.ResponsiveRow(controls=[])

        for protection in self.protections.values():
            self.row.controls.append(
                Card(protection.name)
            )


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

                                        self.row
                                    ]
                                )
                            )
                        ]
                    )
                ]
            )
        )