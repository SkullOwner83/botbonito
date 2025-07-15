import flet as ft
from services.moderation_manager import ModerationManager
from services.service_locator import ServiceLocator
from utilities.enums import PenaltyType, UserLevel
from models.protection import Protection
from view.controls import *

class ProtectionModal(Modal):
    def __init__(self, protection: Protection):
        self.protection = protection
        self.moderation_manager: ModerationManager = ServiceLocator.get('moderation')
        self.set_controls()

        super().__init__(
            title='Editar protección',
            content=self.build(),
            actions=[
                Button(text="Cancelar", on_click=lambda e: self.on_close(), outlined=True),
                Button(text="Guardar", on_click=lambda e: self.save_changes())
            ]
        )

    def set_controls(self) -> None:
        self.reason_textbox = TextBox(value=self.protection.reason)
        self.duration_textbox = TextBox(value=self.protection.duration)
        self.strikes_textbox = TextBox(value=self.protection.strikes)
        self.announce_checkbox = CheckBox(text='Anunciar penalización', checked=self.protection.announce_penalty)

        self.penalty_dropdown = DropDown(
            value=self.protection.penalty or PenaltyType.DELETE_MESSAGE.value,
            options=[
                ft.DropdownOption(key=penalty_type.value, text=str.capitalize(penalty_type.value))
                for penalty_type in PenaltyType
            ]
        )

        self.exclude_dropdown = DropDown(
            value=self.protection.exclude or PenaltyType.DELETE_MESSAGE.value,
            options=[
                ft.DropdownOption(key=user_level.value, text=str.capitalize(user_level.value))
                for user_level in UserLevel if not user_level in [UserLevel.EVERYONE, UserLevel.BROADCASTER]
            ]
        )

    def build(self) -> ft.Column:
        return ft.Column(
            spacing=16,
            scroll=ft.ScrollMode.ADAPTIVE,
            controls=[
                ft.Column(
                    spacing=0,
                    controls=[
                        Label('Penalización:'),
                        self.penalty_dropdown
                    ]
                ),

                ft.Row(
                    spacing=16,
                    controls=[
                        ft.Column(
                            expand=1,
                            controls=[
                                Label('Duración:'),
                                self.duration_textbox
                            ]
                        ),
                        ft.Column(
                            expand=1,
                            controls=[
                                Label('Strikes:'),
                                self.strikes_textbox
                            ]
                        )
                    ]
                ),

                ft.Column(
                    spacing=0,
                    controls=[
                        Label('Excluir:'),
                        self.exclude_dropdown
                    ]
                ),

                ft.Column(
                    spacing=0,
                    controls=[
                        Label('Razón de penalización:'),
                        self.reason_textbox
                    ]
                ),

                self.announce_checkbox
            ]
        )
    
    def save_changes(self) -> None:
        self.protection.reason = self.reason_textbox.value
        self.protection.penalty = self.penalty_dropdown.value
        self.protection.exclude = self.exclude_dropdown.value
        self.protection.duration = self.duration_textbox.value
        self.protection.strikes = self.strikes_textbox.value
        self.protection.announce_penalty = self.announce_checkbox.value
        self.moderation_manager.save_protections()
        self.on_close()
    
    def on_close(self) -> None:
        self.page.close(self)
        self.page.update()