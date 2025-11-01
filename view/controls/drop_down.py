import flet as ft
from myapp import MyApp

class DropDown(ft.Stack):
    def __init__(self, value, options, icon=None, on_change=None) -> None:
        self._icon_container = ft.Container(
            content=icon,
            padding=8
        ) if icon else None

        self._dropdown = ft.Dropdown(
            expand=True,
            value=value,
            options=options,
            color=ft.Colors.BLACK,
            bgcolor=ft.Colors.WHITE,
            filled=False,
            border_width=0,  # Desactivamos borde interno
            border_radius=8,
            content_padding=ft.padding.symmetric(horizontal=16),
            leading_icon=self._icon_container,
            on_change=on_change,
            trailing_icon=ft.Container(
                content=ft.Icon(name=ft.Icons.KEYBOARD_ARROW_DOWN_ROUNDED, size=32),
                padding=ft.padding.only(top=-8, left=-4, right=-4),
            ),
            selected_trailing_icon=ft.Container(
                content=ft.Icon(name=ft.Icons.KEYBOARD_ARROW_UP_ROUNDED, size=32),
                padding=ft.padding.only(top=-8, left=-4, right=-4)
            ),
            text_style=ft.TextStyle(
                font_family=MyApp.font_secondary,
                size=16,
            )
        )

        self._container = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=8,
            border=ft.border.all(1, ft.Colors.GREY_500),
            content=self._dropdown
        )

        super().__init__(
            expand=True,
            height=40,
            controls=[self._container]
        )

    @property
    def value(self):
        return self._dropdown.value

    @value.setter
    def value(self, val):
        self._dropdown.value = val

    @property
    def options(self):
        return self._dropdown.options

    @options.setter
    def options(self, opts):
        self._dropdown.options = opts

    @property
    def icon(self):
        return self._icon_container.content if self._icon_container else None
    
    @icon.setter
    def icon(self, new_icon):
        if not new_icon:
            self._icon_container = None
            self._dropdown.update()
        else:    
            if not self._icon_container:
                self._icon_container = ft.Container(padding=8)

            self._icon_container.content = new_icon
            self._icon_container.update()