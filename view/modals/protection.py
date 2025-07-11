import flet as ft
from services.moderation_manager import ModerationManager
from services.service_locator import ServiceLocator
from models.enums import PenaltyType, UserLevel
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

        self.penalty_dropdown = DropDown(
            value=self.protection.penalty or PenaltyType.DELETE_MESSAGE.value,
            options=[
                ft.DropdownOption(key=PenaltyType.DELETE_MESSAGE.value, text='Delete message'),
                ft.DropdownOption(key=PenaltyType.TIME_OUT.value, text='Time out'),
                ft.DropdownOption(key=PenaltyType.BAN_USER.value, text='Ban user')
            ]
        )

        self.exclude_dropdown = DropDown(
            value=self.protection.exclude or PenaltyType.DELETE_MESSAGE.value,
            options=[
                ft.DropdownOption(key=UserLevel.NO_ONE.value, text='No one'),
                ft.DropdownOption(key=UserLevel.FOLLOWER.value, text='Follower'),
                ft.DropdownOption(key=UserLevel.MODERATOR.value, text='Moderator'),
                ft.DropdownOption(key=UserLevel.SUBSCRIBER.value, text='Admin'),
                ft.DropdownOption(key=UserLevel.VIP.value, text='VIP')
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
                        Label('Razón de penalización:'),
                        self.reason_textbox
                    ]
                ),
                
                ft.Column(
                    spacing=0,
                    controls=[
                        Label('Penalización:'),
                        self.penalty_dropdown
                    ]
                ),

                ft.Column(
                    spacing=0,
                    controls=[
                        Label('Excluir:'),
                        self.exclude_dropdown
                    ]
                )
            ]
        )
    
    def save_changes(self) -> None:
        self.protection.reason = self.reason_textbox.value
        self.protection.penalty = self.penalty_dropdown.value
        self.protection.exclude = self.exclude_dropdown.value
        self.moderation_manager.save_protections()
        self.on_close()
    
    def on_close(self) -> None:
        self.page.close(self)
        self.page.update()