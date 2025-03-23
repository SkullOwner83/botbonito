import flet as ft
from models.commands import CommandConfig
from ..controls.navigation_bar import NavigationBar
from ..controls.header import Header
from ..controls.data_table import DataTable
from myapp import MyApp


class CommandsPage():
    def __init__(self, page: ft.Page):
        self.page = page
        self.filter = ''
        
        self.default_commands = DataTable(
            visible=True,
            columns=[
                ft.DataColumn(ft.Text("ACTIVO")),
                ft.DataColumn(ft.Text("COMANDO")),
                ft.DataColumn(ft.Text("DESCRIPCIÓN")),
                ft.DataColumn(ft.Text("PERMISOS"))
            ]
        )

        self.custom_commands = DataTable(
            visible=False,
            columns=[
                ft.DataColumn(ft.Text("ACTIVO")),
                ft.DataColumn(ft.Text("COMANDO")),
                ft.DataColumn(ft.Text("DESCRIPCIÓN")),
                ft.DataColumn(ft.Text("PERMISOS"))
            ]
        )

        self.target_table = self.default_commands

    def load_data(self, table: DataTable, filter: str = '') -> None:
        if MyApp.bot:
            target_commands = MyApp.bot.default_commands.values() if table == self.default_commands else MyApp.bot.custom_commands.values()
            table.rows.clear()

            for command in target_commands:
                if filter == '' or filter in command.name:
                    table.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Switch(
                                    on_change=lambda e, c = command: self.disble_command(e, c),
                                    value=command.enable, 
                                    width=32)
                                ),

                                ft.DataCell(ft.Text(f"!{command.name}")),
                                ft.DataCell(ft.Text(command.name)),
                                ft.DataCell(ft.Text(command.user_level))
                            ]
                        )
                    )
    
    def disble_command(self, e: ft.ControlEvent, command: CommandConfig) -> None:
        command.enable = e.control.value
    
    # Apply the filter and refresh the data in the corresponding table
    def search_command(self, e: ft.ControlEvent) -> None:
        self.filter = e.control.value.lower()
        self.load_data(self.target_table, self.filter)
        self.target_table.update()

    # Change the view to display the corresponding table for the selected tab
    def change_tab(self, e: ft.ControlEvent) -> None:
        if e.control.selected == {"1"}:
            self.default_commands.visible = True
            self.custom_commands.visible = False
            self.target_table = self.default_commands

        elif e.control.selected == {"2"}:
            self.custom_commands.visible = True
            self.default_commands.visible = False
            self.target_table = self.custom_commands

        self.load_data(self.target_table, self.filter)
        self.page.update()

    def get_view(self) -> ft.View:
        self.load_data(self.default_commands)
        self.load_data(self.custom_commands)

        return ft.View(
            route = '/commands',
            padding=0,
            controls = [
                ft.Container(
                    expand=True,
                    content=ft.Row(
                        expand=True,
                        spacing=0,
                        controls =[
                            NavigationBar(self.page),
                            
                            ft.Column(
                                expand=True,
                                spacing=0,
                                controls = [
                                    Header("Comandos"),
                                    
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
                                                                            shape= ft.RoundedRectangleBorder(radius=8),
                                                                            side=ft.BorderSide(width=0),
                                                                            
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
                                                            content= ft.TextField(
                                                                width=350,
                                                                height=32,
                                                                text_style= ft.TextStyle(font_family=MyApp.font_secondary, size=14),
                                                                text_vertical_align=ft.VerticalAlignment.CENTER,
                                                                hint_text="Buscar comando...",
                                                                bgcolor=ft.Colors.WHITE,
                                                                prefix_icon= ft.Icons.SEARCH,
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
                                                    vertical_alignment= ft.CrossAxisAlignment.START,
                                                    controls=[
                                                        ft.Stack(
                                                            expand=True,
                                                            controls=[
                                                                self.default_commands,
                                                                self.custom_commands
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
    
    