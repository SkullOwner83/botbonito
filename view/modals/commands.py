from typing import Callable, Optional
import flet as ft
from services import *
from ..controls import *
from models.commands import CommandConfig
from utilities.enums import UserLevel, ResponseType

class CommandsModal(Modal):
    def __init__(self, command: Optional[CommandConfig] = None, on_save: Optional[Callable] = None) -> None:
        self.commands_manager: CommandsManager = ServiceLocator.get('commands')

        if command is None:
            self.action = 'create'
            self.command = CommandConfig('nombre')
            self.command_type = 'custom'
        else:
            self.action = 'edit'
            self.command = command
            self.command_type = 'default' if command in self.commands_manager.default_commands.values() else 'custom'

        self.alias = self.command.alias.copy()
        self.on_save = on_save
        self.set_controls()

        super().__init__(
            title="Editar comando" if self.action == 'edit' else "Nuevo comando",
            content=self.build(),
            actions=[
                ft.Row(
                    controls=[
                        *self.delete_button,
                        ft.Container(
                            expand=True,
                            alignment=ft.alignment.center_right,
                            content=ft.Row(
                                alignment= ft.MainAxisAlignment.END,
                                controls=[
                                    Button(text="Cancelar", on_click=lambda e: self.on_close(), outlined=True),
                                    Button(text="Guardar", on_click=lambda e: self.save_changes())
                                ]
                            )
                        )
                    ]
                )
            ]
        )

    # Define the controls to save his reference
    def set_controls(self) -> None:
        self.name_textbox = TextBox(value=self.command.name, one_word=True, is_alpha=True)
        self.alias_textbox = TextBox(on_submit=self.add_alias, one_word=True, is_alpha=True)
        self.alias_container = ft.Row(wrap=True)
        self.error_message = Label(text="", color=ft.Colors.RED)
        self.customs_controls = []
        self.delete_button = []
        self.load_alias()
       
        self.user_level_dropdown = DropDown(
            value=self.command.user_level if self.command.user_level else UserLevel.EVERYONE,
            options=[
                ft.DropdownOption(key=user_level.value, text=str.capitalize(user_level.value)) 
                for user_level in UserLevel if user_level != UserLevel.NO_ONE
            ]
        )

        # Define controls only for custom commands
        if self.command_type == 'custom':
            self.response_textbox = TextBox(value=self.command.response)
            self.delete_button.append(ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED))

            self.response_type_dropdown = DropDown(
                value=self.command.response_type if self.command.response_type else ResponseType.SAY,
                options=[
                    ft.DropdownOption(key=response_type.value, text=str.capitalize(response_type.value))
                    for response_type in ResponseType
                ]
            )

            self.customs_controls.extend([
                ft.Column(
                    spacing=0,
                    controls=[
                        Label(text="Respuesta:"),
                        self.response_textbox
                    ]
                ),

                ft.Column(
                    spacing=0,
                    controls=[
                        Label(text="Tipo de respuesta:"),
                        self.response_type_dropdown
                    ]
                )
            ])

    # Build the view UI of commands modal
    def build(self) -> ft.Column:
        return ft.Column(
            expand=True,
            spacing=16,
            scroll=ft.ScrollMode.ADAPTIVE,
            controls=[
                ft.Column(
                    spacing=0,
                    controls=[
                        Label(text="Nombre:"),
                        self.name_textbox,
                    ]
                ),

                ft.Column(
                    spacing=0,
                    controls=[
                        Label(text="Nivel requerido:"),
                        self.user_level_dropdown,
                    ]
                ),

                *self.customs_controls,

                ft.Column(
                    spacing=0,
                    controls=[
                        Label(text="Alias de comando:"),
                        self.alias_textbox,
                    ]
                ),
                
                self.alias_container
            ]
        )

    def load_alias(self):
        self.alias_container.controls.clear()

        for alias in self.alias:
            self.alias_container.controls.append(
                Tag(alias, lambda e, a=alias: self.remove_alias(a))
            )

    def add_alias(self, e: ft.ControlEvent) -> None:
        textbox = e.control
        value = textbox.value.strip()

        if value and not value in self.alias:
            self.alias.append(textbox.value)
            textbox.value = ""
            textbox.focus()
            self.load_alias()
            self.page.update()
    
    def remove_alias(self, alias: str) -> None:
        if alias in self.alias:
            self.alias.remove(alias)
            self.load_alias()
            self.page.update()

    def save_changes(self) -> None:
        self.command.name = self.name_textbox.value
        self.command.user_level = self.user_level_dropdown.value
        self.command.alias = self.alias.copy()

        if self.command_type == 'custom':
            self.command.response = self.response_textbox.value
            self.command.response_type = self.response_type_dropdown.value

        if self.action == 'create':
            self.commands_manager.custom_commands[self.command.name] = self.command

        self.commands_manager.save_commands()
        self.on_save() if self.on_save else None
        self.on_close()

    def on_close(self) -> None:
        self.page.close(self)
        self.page.update()