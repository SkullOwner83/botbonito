import flet as ft
from models.eventsub import EventSub
from services.event_service import EventService
from services.service_locator import ServiceLocator
from models.appconfig import AppConfig
from view.modals.eventsub import EventSubModal
from view.controls import *
from myapp import MyApp

class EventsPage(ft.Container):
    def __init__(self, page: ft.Page, app_config: AppConfig) -> None:
        self.page = page
        self.app_config = app_config

        self.events_manager: EventService = ServiceLocator.get('events')
        self.event_subs: dict[str, EventSub] = self.events_manager.events
        self.set_controls()

        super().__init__(padding=32, content=self.build())

    def set_controls(self):
        self.event_list = []

        for event in self.event_subs.values():
            self.event_list.append(
                ft.Container(
                    bgcolor=ft.Colors.WHITE,
                    padding=8,
                    on_click=lambda e, es=event: self.handle_click(es),
                    on_hover=self.handle_hover,
                    content=ft.Row(
                        spacing=8,
                        controls=[
                            ft.Switch(value=event.enable, width=32),
                            ft.Text(value=event.name, font_family=MyApp.font_secondary, size=16)
                        ]
                    )
                )
            )

    def handle_click(self, event: EventSub) -> None:
        self.page.open(EventSubModal(event))

    def handle_hover(self, e: ft.ControlEvent) -> None:
        e.control.bgcolor = ft.Colors.GREY_100 if e.data == 'true' else ft.Colors.WHITE
        e.control.update()

    def build(self) -> ft.Container:
        return ft.Row(
            spacing=24,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Container(
                    expand=True,
                    #width=200,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=8,
                    content=ft.ListView(
                        expand=1,
                        controls=self.event_list
                    )
                ),

                # ft.Container(
                #     expand=True,
                #     bgcolor=ft.Colors.WHITE,
                #     border_radius=8,
                #     content=ft.Text("Hola")
                # )
            ]
        )