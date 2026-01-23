import flet as ft
from services.moderation_manager import ModerationManager
from services.service_locator import ServiceLocator
from utilities.constants import Constants
from utilities.enums import PenaltyType, UserLevel
from models.protection import Protection
from view.controls import *

class ProtectionModal(Modal):
    def __init__(self, protection: Protection):
        self.protection = protection
        self.moderation_manager: ModerationManager = ServiceLocator.get('moderation')
        self.min_threshold, self.max_threshold, self.step_threshold = Constants.PROTECTION_THRESHOLD_RANGES.get(self.protection.name)
        self.safe_threshold = max(min(self.protection.threshold, self.max_threshold), self.min_threshold)

        match(self.protection.name):
            case 'repeated_messages': self.treshold_text = ' mensajes'
            case 'long_messages': self.treshold_text = ' caracteres'
            case 'excess_caps': self.treshold_text = ' mayusculas'
            case 'excess_symbols': self.treshold_text = ' simbolos'
            case 'excess_emotes': self.treshold_text = ' emotes'
            case _: self.treshold_text = ''

        self.set_controls()

        super().__init__(
            title='Editar protección',
            content=self.build(),
            actions=[
                Button(text="Cancelar", on_click=lambda e: self.on_close(), outlined=True),
                Button(text="Guardar", on_click=lambda e: self.save_changes())
            ]
        )

    # Show or hide controls depending the selected penalty
    def apply_control_state(self, value: str):
        if value == PenaltyType.TIME_OUT.value:
            self.penalty_column.col = 4
            self.duration_column.visible = True
        else:
            self.penalty_column.col = 6
            self.duration_column.visible = False

        self.mark_strike_checkbox.visible = value != PenaltyType.BAN_USER
        self.threshold_column.visible = self.protection.name != 'links'

    # Update the icon of the penalty dropdown to the selected item
    def on_penalty_change(self, e: ft.ControlEvent):
        self.penalty_dropdown.icon = ft.Icon(name=Constants.PENALTY_ICONS.get(e.control.value), color=ft.Colors.BLACK)
        self.apply_control_state(e.control.value)
        self.update()

    # Round the slider value to safe value to allow stored without exceptions
    def on_slider_change(self, e: ft.ControlEvent):
        raw = e.control.value
        
        if 0 <= raw <= 1:
            self.safe_threshold = round(raw * 10) / 10
        else:
            self.safe_threshold = round(raw / self.step_threshold) * self.step_threshold


        self.threshold_label.value = self.safe_threshold
        self.threshold_label.update()

    # Set the slider value to the safe stored value when the user finishes moving it    
    def on_slider_change_end(self, e: ft.ControlEvent):
        e.control.value = self.safe_threshold
        e.control.update()

    # Update the values of protection instance and close the modal
    def save_changes(self) -> None:
        self.protection.reason = self.reason_textbox.value
        self.protection.penalty = self.penalty_dropdown.value
        self.protection.exclude = self.exclude_dropdown.value
        self.protection.duration = self.duration_textbox.value
        self.protection.announce_penalty = self.announce_checkbox.value
        self.protection.threshold = self.safe_threshold
        self.moderation_manager.save_protections()
        self.on_close()
    
    # Close the protection modal
    def on_close(self) -> None:
        self.page.close(self)
        self.page.update()

    # Define the controls to save his reference
    def set_controls(self) -> None:
        self.reason_textbox = TextBox(value=self.protection.reason)
        self.duration_textbox = TextBox(value=self.protection.duration, one_word=True, is_numeric=True)
        self.announce_checkbox = CheckBox(text='Anunciar penalización en el chat.', checked=self.protection.announce_penalty)
        self.mark_strike_checkbox = CheckBox(text='Marcar strike por penalización.', checked=self.protection.mark_strike)

        self.penalty_dropdown = DropDown(
            value=self.protection.penalty if self.protection.penalty else PenaltyType.DELETE_MESSAGE.value,
            icon=ft.Icon(name=Constants.PENALTY_ICONS.get(self.protection.penalty), color=ft.Colors.BLACK),
            on_change=self.on_penalty_change,
            options=[
                ft.DropdownOption(
                    key=penalty_type.value, 
                    text=str.capitalize(penalty_type.value),
                    leading_icon=ft.Icon(name=Constants.PENALTY_ICONS.get(penalty_type), color=ft.Colors.BLACK)
                )
                for penalty_type in PenaltyType
            ]
        )

        self.penalty_column = ft.Column(
            col=4,
            spacing=0,
            controls=[
                Label('Penalización:'),
                self.penalty_dropdown
            ]
        )

        self.duration_column = ft.Column(
            col=2,
            spacing=0,
            controls=[
                Label('Duración:'),
                self.duration_textbox
            ]
        )

        self.exclude_dropdown = DropDown(
            value=self.protection.exclude if self.protection.exclude else UserLevel.NO_ONE,
            icon=ft.Image(src=Constants.USER_LEVEL_ICONS.get(self.protection.exclude)),
            on_change=lambda e: setattr(self.exclude_dropdown, 'icon', ft.Image(src=Constants.USER_LEVEL_ICONS.get(e.control.value, 'everyone'))),
            options=[
                ft.DropdownOption(
                    key=user_level.value, 
                    text=str.capitalize(user_level.value),
                    leading_icon=ft.Image(src=Constants.USER_LEVEL_ICONS.get(user_level), width=20, height=20)
                    )
                for user_level in UserLevel if not user_level in [UserLevel.EVERYONE, UserLevel.BROADCASTER]
            ]
        )

        self.threshold_slider = ft.Slider(
            min=self.min_threshold,
            max=self.max_threshold,
            value=self.safe_threshold,
            on_change=self.on_slider_change,
            on_change_end=self.on_slider_change_end,
            padding=ft.padding.symmetric(vertical=4)
        )

        self.threshold_label = Label(text=f'{self.threshold_slider.value}', color=ft.Colors.GREY_600, weigth=ft.FontWeight.NORMAL)

        self.threshold_column = ft.Column(
            col=6,
            spacing=0,
            controls=[
                ft.Row(
                    spacing=0,
                    controls=[
                        Label('Umbral: '),
                        self.threshold_label,
                        Label(self.treshold_text, color=ft.Colors.GREY_600, weigth=ft.FontWeight.NORMAL)

                    ]
                ),

                self.threshold_slider
            ]
        )
        
        self.apply_control_state(self.penalty_dropdown.value)

    # Build the view UI of protection modal
    def build(self) -> ft.Column:
        return ft.Column(
            spacing=16,
            scroll=ft.ScrollMode.ADAPTIVE,
            controls=[
                ft.ResponsiveRow(
                    spacing=16,
                    run_spacing=16,
                    columns=6,
                    controls=[
                        self.penalty_column,
                        self.duration_column,

                        ft.Column(
                            col=6,
                            spacing=0,
                            controls=[
                                Label('Excluir:'),
                                self.exclude_dropdown
                            ]
                        ),

                        ft.Column(
                            col=6,
                            spacing=0,
                            controls=[
                                Label('Razón de penalización:'),
                                self.reason_textbox
                            ]
                        ),

                        self.threshold_column,

                        ft.Column(
                            col=6,
                            spacing=0,
                            controls=[
                                self.announce_checkbox,
                                self.mark_strike_checkbox
                            ]
                        )
                    ]
                )
            ]
        )