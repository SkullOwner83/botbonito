import flet as ft

class HomePage:
    def __init__(self, page: ft.Page):
        self.page = page

    def get_view(self) -> ft.Page:
        return ft.View(
            route = '/',
            controls = [
                ft.Text(value="¡Hola! Soy el bot bonito. yo tambien"),
                ft.Stack(
                    
                )
            ]
        )