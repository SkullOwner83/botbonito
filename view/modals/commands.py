from typing import Callable, Optional
import flet as ft
from ..controls import *
from models.commands import CommandConfig
from models.config import ConfigManager

class CommandsModal(Modal):
    def __init__(self, command: Optional[CommandConfig] = None, on_save: Optional[Callable] = None) -> None:
        self.commands_config = ConfigManager()

        if command is None:
            self.action = 'create'
            self.command = CommandConfig('nombre')
            self.command_type = 'custom'
        else:
            self.action = 'edit'
            self.command = command
            self.command_type = 'default' if command in self.commands_config.default_commands.values() else 'custom'

        self.alias = self.command.alias.copy()
        self.on_save = on_save
        self.set_controls()

        super().__init__(
            title="Editar comando" if self.action == 'edit' else "Nuevo comando",
            content=self.build(),
            actions=[
                Button(text="Cancelar", style="Outlined", on_click=self.on_close),
                Button(text="Guardar", style="Filled", on_click=lambda e: self.save_command(e))
            ]
        )

    def set_controls(self) -> None:
        self.name_textbox = TextBox(value=self.command.name)
        self.alias_textbox = TextBox(on_submit=self.add_alias)
        self.alias_container = ft.Row(wrap=True)
        self.customs_controls = []
        self.load_alias()
       
        self.user_level_dropdown = DropDown(
            value=self.command.user_level or "everyone",
            options=[
                ft.DropdownOption(key="everyone", content=ft.Text("Everyone")),
                ft.DropdownOption(key="moderator", content=ft.Text("Moderator")),
                ft.DropdownOption(key="suscriptor", content=ft.Text("Suscriptor")),
                ft.DropdownOption(key="broadcaster", content=ft.Text("Broadcaster")),
            ]
        )

        if self.command_type == 'custom':
            self.response_textbox = TextBox(value=self.command.response)

            self.response_type_dropdown = DropDown(
                value=self.command.response_type or "say",
                options=[
                    ft.DropdownOption(key="say", content=ft.Text("Decir")),
                    ft.DropdownOption(key="mention", content=ft.Text("Mencionar")),
                    ft.DropdownOption(key="reply", content=ft.Text("Responder")),
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

    def build(self) -> ft.Column:
        return ft.Column(
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
                        Label(text="Nivel requerido"),
                        self.user_level_dropdown,
                    ]
                ),

                *self.customs_controls,

                ft.Column(
                    spacing=0,
                    controls=[
                        Label(text="Alias de comando"),
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
                Tag(alias, lambda e, a=alias: self.remove_alias(e, a))
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
    
    def remove_alias(self, e: ft.ControlEvent, alias: str) -> None:
        if alias in self.alias:
            self.alias.remove(alias)
            self.load_alias()
            self.page.update()

    def save_command(self, e: ft.ControlEvent) -> None:
        self.command.name = self.name_textbox.value
        self.command.user_level = self.user_level_dropdown.value
        self.command.alias = self.alias.copy()

        if self.command_type == 'custom':
            self.command.response = self.response_textbox.value
            self.command.response_type = self.response_type_dropdown.value

        if self.action == 'create':
            self.commands_config.custom_commands[self.command.name] = self.command

        self.commands_config.save_commands()
        self.on_save() if self.on_save else None
        self.page.close(self)

    def on_close(self, e: ft.ControlEvent) -> None:
        self.page.close(self)
        self.page.update()