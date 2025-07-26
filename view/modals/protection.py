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

    # Define the controls to save his reference
    def set_controls(self) -> None:
        self.reason_textbox = TextBox(value=self.protection.reason)
        self.duration_textbox = TextBox(value=self.protection.duration)
        self.strikes_textbox = TextBox(value=self.protection.strikes)
        self.announce_checkbox = CheckBox(text='Anunciar penalización', checked=self.protection.announce_penalty)

        self.penalty_dropdown = DropDown(
            value=self.protection.penalty if self.protection.penalty else PenaltyType.DELETE_MESSAGE.value,
            options=[
                ft.DropdownOption(key=penalty_type.value, text=str.capitalize(penalty_type.value))
                for penalty_type in PenaltyType
            ]
        )

        self.exclude_dropdown = DropDown(
            value=self.protection.exclude if self.protection.exclude else UserLevel.NO_ONE,
            options=[
                ft.DropdownOption(key=user_level.value, text=str.capitalize(user_level.value))
                for user_level in UserLevel if not user_level in [UserLevel.EVERYONE, UserLevel.BROADCASTER]
            ]
        )

    # Build the view UI of protection modal
    def build(self) -> ft.Column:
        return ft.Column(
            spacing=20,
            scroll=ft.ScrollMode.ADAPTIVE,
            controls=[
                ft.ResponsiveRow(
                    spacing=20,
                    run_spacing=20,
                    columns=2,
                    controls=[
                        ft.Column(
                            col=2,
                            spacing=0,
                            controls=[
                                Label('Penalización:'),
                                self.penalty_dropdown
                            ]
                        ),

                        ft.Column(
                            col=1,
                            spacing=0,
                            controls=[
                                Label('Duración:'),
                                self.duration_textbox
                            ]
                        ),

                        ft.Column(
                            col=1,
                            spacing=0,
                            controls=[
                                Label('Strikes:'),
                                self.strikes_textbox
                            ]
                        ),

                        ft.Column(
                            col=2,
                            spacing=0,
                            controls=[
                                Label('Excluir:'),
                                self.exclude_dropdown
                            ]
                        ),

                        ft.Column(
                            col=2,
                            spacing=0,
                            controls=[
                                Label('Razón de penalización:'),
                                self.reason_textbox
                            ]
                        ),

                        self.announce_checkbox
                    ]
                )
            ]
        )
    
    # Update the values of protection instance and close the modal
    def save_changes(self) -> None:
        self.protection.reason = self.reason_textbox.value
        self.protection.penalty = self.penalty_dropdown.value
        self.protection.exclude = self.exclude_dropdown.value
        self.protection.duration = self.duration_textbox.value
        self.protection.strikes = self.strikes_textbox.value
        self.protection.announce_penalty = self.announce_checkbox.value
        self.moderation_manager.save_protections()
        self.on_close()
    
    # Close the protection modal
    def on_close(self) -> None:
        self.page.close(self)
        self.page.update()