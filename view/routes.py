import flet as ft
from .pages.home import HomePage
from .pages.validation import ValidationPage

class Routes:
    def __init__(self, page: ft.Page):
        self.page = page
        self.home_page = HomePage(page)
        self.validation_page = ValidationPage(page)
    
    def route_change(self, e):
        self.page.views.clear()

        if self.page.route == "/": self.page.views.append(self.home_page.get_view())
        elif self.page.route == "/validation": self.page.views.append(self.validation_page.get_view())

        self.page.update()
    
    def view_pop(self, e: ft.ViewPopEvent) -> None:
        self.page.views.pop()
        top_view: ft.View = self.page.views[-1]
        self.page.route = top_view.route
    
    def goto(self, page: str = '/') -> None:
        self.page.go({page})