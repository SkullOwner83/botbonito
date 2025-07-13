import flet as ft
from ..controls import *
from ..modals import CommandsModal
from services import *
from models.commands import CommandConfig
from myapp import MyApp

class CommandsPage(ft.View):
    def __init__(self, page: ft.Page, botconfig: dict) -> None:
        super().__init__(
            route='/validation',
            padding=0
        )

        self.page = page
        self.filter = ''
        self.botconfig = botconfig
        self.commands_manager: CommandsManager = ServiceLocator.get('commands')
        self.default_commands = self.commands_manager.default_commands
        self.custom_commands = self.commands_manager.custom_commands
        
        self.set_controls()
        self.controls.append(self.build())
        self.load_data(self.default_commands_table)
        self.load_data(self.custom_commands_table)

    def load_data(self, table: DataTable = None, filter: str = '') -> None:
        table = self.target_table if table is None else table
        target_commands = self.default_commands.values() if table == self.default_commands_table else self.custom_commands.values()
        table.rows.clear()

        for command in target_commands:
            if filter == '' or filter in command.name.lower():
                table.rows.append(
                    ft.DataRow(
                        on_select_changed=lambda e, c=command: self.modify_command(c),
                        cells=[
                            ft.DataCell(
                                ft.Switch(
                                    on_change=lambda e, c=command: self.toggle_command(e, c),
                                    value=command.enable, 
                                    width=32,
                                )
                            ),

                            ft.DataCell(
                                content=ft.Container(
                                    padding=8,
                                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                                    content=ft.Column(
                                        spacing=0,
                                        controls=[
                                            ft.Text(value=f"!{command.name}", weight=ft.FontWeight.BOLD),
                                            ft.Text(
                                                value=command.description if table is self.default_commands_table else command.response,
                                                color=ft.Colors.GREY_700,
                                                style=ft.TextStyle(height=0)
                                            )
                                        ]
                                    )
                                )
                            ),

                            ft.DataCell(Badge(command.user_level))
                        ]
                    )
                )

        self.page.update()

    def create_command(self, e: ft.ControlEvent) -> None:
        self.page.open(CommandsModal(on_save=self.load_data))
        
    def modify_command(self, command: CommandConfig) -> None:
        self.page.open(CommandsModal(command, self.load_data))
    
    # Apply the filter and refresh the data in the corresponding table
    def search_command(self, e: ft.ControlEvent) -> None:
        self.filter = e.control.value.lower().strip()
        self.load_data(self.target_table, self.filter)
        self.target_table.update()

    # Change the view to display the corresponding table for the selected tab
    def change_tab(self, e: ft.ControlEvent) -> None:
        if e.control.selected == {"1"}:
            self.default_commands_table.visible = True
            self.custom_commands_table.visible = False
            self.add_command_button.visible = False
            self.target_table = self.default_commands_table

        elif e.control.selected == {"2"}:
            self.custom_commands_table.visible = True
            self.default_commands_table.visible = False
            self.add_command_button.visible = True
            self.target_table = self.custom_commands_table

        self.load_data(self.target_table, self.filter)
        self.page.update()
    
    def toggle_command(self, e: ft.ControlEvent, command: CommandConfig) -> None:
        command.enable = e.control.value

    def set_controls(self) -> None:
        self.default_commands_table = DataTable(
            visible=True,
            columns=[
                ft.DataColumn(ft.Text("Activo")),
                ft.DataColumn(label=ft.Text("Comando"), heading_row_alignment=ft.MainAxisAlignment.CENTER),
                ft.DataColumn(ft.Text("Permisos"))
            ]
        )

        self.custom_commands_table = DataTable(
            visible=False,
            columns=[
                ft.DataColumn(ft.Text("Activo")),
                ft.DataColumn(ft.Text("Comando")),
                ft.DataColumn(ft.Text("Permisos"))
            ]
        )

        self.add_command_button = Button(
            text="+", 
            width=32, 
            padding=0, 
            visible=False, 
            on_click=self.create_command
        )

        self.target_table = self.default_commands_table

    # Build the view UI and load the data into the tables
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
                        controls = [
                            Header("Comandos", self.botconfig),
                            
                            ft.Container(
                                expand=True,
                                padding=32,
                                alignment=ft.alignment.top_center,
                                content=ft.Column(
                                    spacing=20,
                                    controls=[
                                        ft.Row(
                                            spacing=20,
                                            controls=[
                                                ft.Container(
                                                    content=SegmentedButton(
                                                        on_change=self.change_tab,
                                                        segments=[
                                                            ft.Segment(value="1", label=ft.Text("Predeterminados")),
                                                            ft.Segment(value="2", label=ft.Text("Personalizados")),
                                                        ]
                                                    )
                                                ),

                                                ft.Container(
                                                    expand=True,
                                                    alignment=ft.alignment.center_right,
                                                    content=TextBox(
                                                        width=350,
                                                        height=32,
                                                        border=0,
                                                        prefix_icon=ft.Icons.SEARCH,
                                                        place_holder='Buscar comando...',
                                                        on_change=self.search_command
                                                    )
                                                ),

                                                self.add_command_button
                                            ]
                                        ),

                                        ft.Column(
                                            expand=True,
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