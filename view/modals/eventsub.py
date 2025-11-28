import flet as ft
from models.eventsub import EventSub
from myapp import MyApp
from services.event_service import EventService
from services.service_locator import ServiceLocator
from view.controls.checkbox import CheckBox
from view.controls.modal import Modal
from view.controls import TextBox, Label, Button

class EventSubModal(Modal):
    def __init__(self, event: EventSub):
        self.event = event
        self.events_manager: EventService = ServiceLocator.get('events')
        self.set_controls()

        super().__init__(
            title='Editar evento',
            content=self.build(),
            actions=[ft.Container(
                expand=True,
                alignment=ft.alignment.center_right,
                content=ft.Row(
                    alignment= ft.MainAxisAlignment.END,
                    controls=[
                        Button(text="Cancelar", on_click=lambda e: self.on_close(), outlined=True),
                        Button(text="Guardar", on_click=lambda e: self.save_changes())
                    ]
                )
            )]
        )

    def save_changes(self):
        self.event.response = self.response_textbox.value
        self.event.announce_response = self.announce_checkbox.value
        self.events_manager.save_events()
        self.on_close()

    def on_close(self) -> None:
        self.page.close(self)
        self.page.update()

    def set_controls(self) -> None:
        self.response_textbox = TextBox(value=self.event.response)
        self.announce_checkbox = CheckBox('Anunciar evento.', self.event.announce_response)
        params = ", ".join(f"{{{p}}}" for p in self.event.params)
        self.params_label = ft.Text(
            value=f'Parametros: {params}' if len(params) > 0 else '',
            color=ft.Colors.GREY_700,
            font_family=MyApp.font_secondary,
            size=16
        )

    def build(self) -> ft.Column:
        return ft.Column(
            spacing=16,
            scroll=ft.ScrollMode.ADAPTIVE,
            controls=[
                ft.Column(
                    spacing=0,
                    controls=[
                        Label('Respuesta del evento:'),
                        self.response_textbox,
                        self.params_label
                    ]
                ),

                self.announce_checkbox
            ]
        )