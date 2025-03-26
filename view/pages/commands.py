from typing import Callable
import flet as ft
from models.commands import CommandConfig
from ..controls.navigation_bar import NavigationBar
from ..controls.data_table import DataTable
from ..controls.tag import Tag
from models.config import ConfigManager
from myapp import MyApp

class CommandsPage():
    def __init__(self, page: ft.Page):
        self.page = page
        self.filter = ''
        self.config_manager = ConfigManager()
        self.default_commands = self.config_manager.default_commands
        self.custom_commands = self.config_manager.custom_commands
        
        self.default_commands_table = DataTable(
            visible=True,
            columns=[
                ft.DataColumn(ft.Text("ACTIVO")),
                ft.DataColumn(ft.Text("COMANDO")),
                ft.DataColumn(ft.Text("DESCRIPCIÓN")),
                ft.DataColumn(ft.Text("PERMISOS"))
            ]
        )

        self.custom_commands_table = DataTable(
            visible=False,
            columns=[
                ft.DataColumn(ft.Text("ACTIVO")),
                ft.DataColumn(ft.Text("COMANDO")),
                ft.DataColumn(ft.Text("DESCRIPCIÓN")),
                ft.DataColumn(ft.Text("PERMISOS"))
            ]
        )

        self.target_table = self.default_commands_table

    def load_data(self, table: DataTable, filter: str = '') -> None:
            target_commands = self.default_commands.values() if table == self.default_commands_table else self.custom_commands.values()
            table.rows.clear()

            for command in target_commands:
                if filter == '' or filter in command.name.lower():
                    table.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Switch(
                                    on_change=lambda e, c=command: self.disable_command(e, c),
                                    value=command.enable, 
                                    width=32,)
                                ),

                                ft.DataCell(ft.Text(f"!{command.name}"), on_tap=lambda e, c=command: self.page.open(DefaultCommandModel(c))),
                                ft.DataCell(ft.Text(command.name)),
                                ft.DataCell(ft.Text(command.user_level))
                            ]
                        )
                    )

    def disable_command(self, e: ft.ControlEvent, command: CommandConfig) -> None:
        command.enable = e.control.value
    
    # Apply the filter and refresh the data in the corresponding table
    def search_command(self, e: ft.ControlEvent) -> None:
        self.filter = e.control.value.lower()
        self.load_data(self.target_table, self.filter)
        self.target_table.update()

    # Change the view to display the corresponding table for the selected tab
    def change_tab(self, e: ft.ControlEvent) -> None:
        if e.control.selected == {"1"}:
            self.default_commands_table.visible = True
            self.custom_commands_table.visible = False
            self.target_table = self.default_commands_table

        elif e.control.selected == {"2"}:
            self.custom_commands_table.visible = True
            self.default_commands_table.visible = False
            self.target_table = self.custom_commands_table

        self.load_data(self.target_table, self.filter)
        self.page.update()

    # Build the view UI and load the data into the tables
    def get_view(self) -> ft.View:
        self.load_data(self.default_commands_table)
        self.load_data(self.custom_commands_table)

        return ft.View(
            route = '/commands',
            padding=0,
            controls = [
                ft.Container(
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
                                controls = [
                                    ft.Container(
                                        expand=True,
                                        padding=32,
                                        alignment=ft.alignment.top_center,
                                        content=ft.Column(
                                            spacing=32,
                                            controls=[
                                                ft.Row(
                                                    spacing=32,
                                                    controls=[
                                                        ft.Container(
                                                            content=ft.Row(
                                                                controls=[
                                                                    ft.SegmentedButton(
                                                                        height=32,
                                                                        allow_multiple_selection=False,
                                                                        allow_empty_selection=False,
                                                                        show_selected_icon=False,
                                                                        selected={"1"},
                                                                        on_change=self.change_tab,

                                                                        style=ft.ButtonStyle(
                                                                            shape=ft.RoundedRectangleBorder(radius=8),
                                                                            side=ft.BorderSide(width=0, color=ft.Colors.TRANSPARENT),
                                                                            bgcolor={
                                                                                ft.ControlState.DEFAULT: ft.Colors.WHITE,
                                                                                ft.ControlState.SELECTED: ft.Colors.PRIMARY
                                                                            },
                                                                            
                                                                            text_style=ft.TextStyle(
                                                                                font_family=MyApp.font_secondary,
                                                                                weight=ft.FontWeight.BOLD,
                                                                                size=14
                                                                            )
                                                                        ),

                                                                        segments=[
                                                                            ft.Segment(value="1", label=ft.Text("Predeterminados")),
                                                                            ft.Segment(value="2", label=ft.Text("Personalizados")),
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ),

                                                        ft.Container(
                                                            expand=True,
                                                            alignment=ft.alignment.center_right,
                                                            content=ft.TextField(
                                                                width=350,
                                                                height=32,
                                                                text_style=ft.TextStyle(font_family=MyApp.font_secondary, size=14),
                                                                text_vertical_align=ft.VerticalAlignment.CENTER,
                                                                hint_text="Buscar comando...",
                                                                bgcolor=ft.Colors.WHITE,
                                                                hover_color=ft.Colors.TRANSPARENT,
                                                                selection_color=ft.Colors.LIGHT_BLUE_100,
                                                                prefix_icon=ft.Icons.SEARCH,
                                                                content_padding=ft.padding.symmetric(horizontal=16),
                                                                border_width=0,
                                                                border_radius=8,
                                                                on_change=self.search_command
                                                            )
                                                        )
                                                    ]
                                                ),

                                                ft.Row(
                                                    expand=True,
                                                    vertical_alignment=ft.CrossAxisAlignment.START,
                                                    controls=[
                                                        ft.Stack(
                                                            expand=True,
                                                            controls=[
                                                                self.default_commands_table,
                                                                self.custom_commands_table
                                                            ]
                                                        )
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
            ]
        )
    

import copy

class DefaultCommandModel(ft.AlertDialog):
    def __init__(self, command: CommandConfig) -> None:
        self.alias = copy.copy(command.alias)

        self.name_textbox = ft.TextField(value=command.name)
        self.alias_textbox = ft.TextField(on_submit=self.add_alias)
        self.alias_container = ft.Row(wrap=True)
        self.load_alias()
       
        self.user_level_dropdown = ft.Dropdown(
            value=command.user_level or "everyone",
            expand=True,
            options=[
                ft.DropdownOption(key="everyone", content=ft.Text("Everyone")),
                ft.DropdownOption(key="moderator", content=ft.Text("Moderator")),
                ft.DropdownOption(key="suscriptor", content=ft.Text("Suscriptor")),
            ]
        )

        super().__init__(
            title_padding=ft.padding.only(left=32, right=32, top=32, bottom=0),
            content_padding=32,
            action_button_padding=16,
            inset_padding=32,
            shape=ft.RoundedRectangleBorder(radius=16),
            modal=False,
            bgcolor=ft.Colors.WHITE,
            title=ft.Text("Editar comando predeterminado"),
            actions_alignment=ft.MainAxisAlignment.END,
            content=ft.Column(
                spacing=8,
                scroll=ft.ScrollMode.ADAPTIVE,
                controls=[
                    ft.Text("Nombre"),
                    self.name_textbox,
                    ft.Text("Nivel requerido"),
                    self.user_level_dropdown,
                    ft.Text("Alias de comando"),
                    self.alias_textbox,
                    self.alias_container
                ]
            ),

            actions=[
                ft.FilledButton(text="Guardar", on_click=lambda e, c=command: self.save_command(e, c)),
                ft.FilledButton(text="Cancelar", on_click=self.on_modal)
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

        if not textbox.value in self.alias:
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

    def save_command(self, e: ft.ControlEvent, command: CommandConfig) -> None:
        command.name = self.name_textbox.value
        command.user_level = self.user_level_dropdown.value
        command.alias = copy.copy(self.alias)
        self.page.close(self)

    def on_modal(self, e: ft.ControlEvent) -> None:
        self.page.close(self)