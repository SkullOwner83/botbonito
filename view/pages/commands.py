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

                            ft.Container(
                                expand=True,
                                padding=32,
                                bgcolor=ft.Colors.GREY_100,
                                alignment=ft.alignment.top_center,
                                content=ft.Column(
                                    scroll= ft.ScrollMode.ADAPTIVE,
                                    controls = [
                                        ft.Row(
                                            spacing=0,
                                            controls = [
                                                ft.DataTable(
                                                    expand=True,
                                                    bgcolor=ft.Colors.WHITE,
                                                    column_spacing=0,
                                                    border_radius=8,
                                                    columns=[
                                                        ft.DataColumn(ft.Text("Activo")),
                                                        ft.DataColumn(ft.Text("Comando")),
                                                        ft.DataColumn(ft.Text("Descrición")),
                                                        ft.DataColumn(ft.Text("Nivel de usuario")),
                                                    ],

                                                    rows=self.commands
                                                )
                                            ]
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                )
            ]
        )
    
    def load_data(self) -> None:
        self.commands.clear()

        if MyApp.bot:
            for command in MyApp.bot.default_commands.values():
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
