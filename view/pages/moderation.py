import flet as ft
from models.appconfig import AppConfig
from models.protection import Protection
from view.modals.protection import ProtectionModal
from services.moderation_manager import ModerationManager
from ..controls import *
from services import *

class ModerationPage(ft.Container):
    def __init__(self, page: ft.Page, app_config: AppConfig) -> None:
        moderation_manager: ModerationManager = ServiceLocator.get('moderation')
        self.protections: dict[str, Protection] = moderation_manager.protections

        self.page = page
        self.botconfig = app_config
        self.set_controls()
        super().__init__(padding=32, content=self.build())

    def set_controls(self):
        self.row = ft.ResponsiveRow(
            columns=6,
            spacing=20,
            run_spacing=20
        )

        for protection in self.protections.values():
            enable_label = Label(text='Habilitado' if protection.enable else 'Deshabilitado', color=ft.Colors.GREY_700)

            self.row.controls.append(
                Card(
                    title=protection.name, 
                    description=protection.description,
                    col={ "sm": 6, "md": 3, "lg": 2 },
                    icon=_PROTECTION_ICONS.get(protection.name),
                    padding=16,
                    footer=ft.Container(
                        padding=ft.padding.only(top=8),
                        alignment=ft.alignment.center_left,
                        content=ft.Row(
                            spacing=8,
                            controls=[
                                ft.Switch(value=protection.enable, width=32, on_change=lambda e, p=protection, l=enable_label: self.toggle_protection(e, p, l),),
                                enable_label,
                                ft.Container(
                                    expand=True,
                                    alignment=ft.alignment.center_right,
                                    content=ft.IconButton(icon=ft.Icons.SETTINGS, on_click=lambda e, p=protection: self.open_settings(p))
                                )
                            ]
                        )
                    )
                )
            )

    def toggle_protection(self, e: ft.ControlEvent, protection: Protection, label: Label) -> None:
        protection.enable = e.control.value
        label.text = 'Habilitado' if protection.enable else 'Deshabilitado'
        label.update()

    def open_settings(self, protection: Protection):
        self.page.open(ProtectionModal(protection))

    # def change_tab(self, e: ft.ControlEvent):
    #     pass

    def build(self) -> ft.Container:
        return ft.Column(
            spacing=20,
            controls=[
                # SegmentedButton(
                #     on_change=self.change_tab,
                #     segments=[
                #         ft.Segment(value='1', label=ft.Text('Protecciones')),
                #         ft.Segment(value='2', label=ft.Text('Palabras prohibidas'))
                #     ]
                # ),

                ft.Column(
                    expand=True,
                    scroll=ft.ScrollMode.ALWAYS,
                    controls=[self.row]
                )
            ]
        )
    
_PROTECTION_ICONS = {
    'links': ft.Icons.ATTACHMENT,
    'repeated_messages': ft.Icons.REPEAT,
    'long_messages': ft.Icons.MESSAGE,
    'excess_caps': ft.Icons.TITLE_ROUNDED,
    'excess_emotes': ft.Icons.EMOJI_EMOTIONS,
    'excess_symbols': ft.Icons.EMOJI_SYMBOLS
}