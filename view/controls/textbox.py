from typing import Callable, Optional
import flet as ft
from myapp import MyApp

class TextBox(ft.TextField):
    def __init__(
            self, 
            value: Optional[str] = '', 
            place_holder: Optional[str] = None,
            height: Optional[int] = 40,
            border: Optional[int] = 1,
            on_submit: Optional[Callable] = None,
            one_word: Optional[bool] = False,
            is_alpha: Optional[bool] = False,
            is_numeric: Optional[bool] = False,
            **kwargs
        ) -> None:

        self.one_word = one_word
        self.is_alpha = is_alpha
        self.is_numeric = is_numeric

        super().__init__(
            value=value,
            expand=True,
            hint_text=place_holder,
            height=height,
            bgcolor=ft.Colors.WHITE,
            hover_color=ft.Colors.TRANSPARENT,
            text_vertical_align=ft.VerticalAlignment.CENTER,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=0),
            on_submit=on_submit,
            border_width=border,
            border_radius=8,
            on_blur=self.handle_blur,
            input_filter=self.build_filter(),

            border_color={
                ft.ControlState.DEFAULT: ft.Colors.GREY_300,
                ft.ControlState.HOVERED: ft.Colors.PRIMARY
            },

            text_style=ft.TextStyle(
                color=ft.Colors.BLACK,
                font_family=MyApp.font_secondary,
                size=16,
            ),

            hint_style=ft.TextStyle(
                color=ft.Colors.GREY,
                font_family=MyApp.font_secondary,
                size=16,
            ),
            **kwargs
        )

    def build_filter(self):
        patterns = []

        if self.is_numeric: patterns.append(r'0-9')
        if self.is_alpha: patterns.append(r'a-zA-Z')
        if not self.one_word and len(patterns) > 0: patterns[-1] += r' '
        if not patterns: return None

        regex = f"^[{''.join(patterns)}]*$"
        print(regex)

        return ft.InputFilter(
            allow=True,
            regex_string=regex,
            replacement_string=""
        )


    def handle_blur(self, e: ft.ControlEvent):
        if self.is_numeric and e.control.value == '':
            e.control.value = '0'
            e.control.update()