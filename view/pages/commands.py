import flet as ft
from ..controls.navigation_bar import NavigationBar
from myapp import MyApp


class CommandsPage():
    def __init__(self, page: ft.Page):
        self.page = page
        self.commands = []

    def get_view(self) -> ft.View:
        self.load_data()

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
                                                                    ft.FilledButton(text="Predeterminados"),
                                                                    ft.FilledButton(text="Personalizados"),
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
                                                                border_radius=12,
                                                                on_change=self.search_command
                                                            )
                                                        )
                                                    ]
                                                ),

                                                ft.Row(
                                                    expand=True,
                                                    vertical_alignment= ft.CrossAxisAlignment.START,
                                                    controls=[
                                                        ft.Column(
                                                            expand=True,
                                                            scroll=ft.ScrollMode.ALWAYS,
                                                            controls=[
                                                                ft.Row(
                                                                    controls=[
                                                                        ft.DataTable(
                                                                            expand=True,
                                                                            bgcolor=ft.Colors.WHITE,
                                                                            column_spacing=0,
                                                                            border_radius=8,

                                                                            heading_text_style=ft.TextStyle(
                                                                                font_family=MyApp.font_secondary,
                                                                                weight=ft.FontWeight.BOLD,
                                                                                size=14
                                                                            ),

                                                                            data_text_style=ft.TextStyle(
                                                                                font_family=MyApp.font_secondary,
                                                                                size=14
                                                                            ),

                                                                            columns=[
                                                                                ft.DataColumn(ft.Text("ACTIVO")),
                                                                                ft.DataColumn(ft.Text("COMANDO")),
                                                                                ft.DataColumn(ft.Text("DESCRIPCIÓN")),
                                                                                ft.DataColumn(ft.Text("PERMISOS")),
                                                                            ],

                                                                            rows=self.commands,
                                                                        )
                                                                    ]
                                                                )
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
    
    def load_data(self, filter: str = '') -> None:
        self.commands.clear()

        if MyApp.bot:
            for command in MyApp.bot.default_commands.values():
                if filter == '' or filter in command.name:
                    self.commands.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Switch(
                                    value=command.enable,
                                    width=32)
                                ),

                                ft.DataCell(ft.Text(f"!{command.name}")),
                                ft.DataCell(ft.Text(command.name)),
                                ft.DataCell(ft.Text(command.user_level))
                            ]
                        )
                    )
        
        self.page.update()
    
    def search_command(self, e: ft.ControlEvent):
        filter = e.control.value.lower()

        if not e.control.value == "":
            self.load_data(filter)
        else:
            self.load_data()