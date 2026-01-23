import flet as ft

class Theme:
    themes = {
        'light': ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=ft.Colors.DEEP_PURPLE,
                on_primary=ft.Colors.WHITE,
                background=ft.Colors.GREY_100,
                on_background=ft.Colors.BLACK,
                surface=ft.Colors.WHITE,
                on_surface=ft.Colors.BLACK
            ),
            page_transitions=ft.PageTransitionsTheme(
                windows=ft.PageTransitionTheme.NONE
            )
        ),

        'dark': ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=ft.Colors.DEEP_PURPLE,
                on_primary=ft.Colors.WHITE,
                background=ft.Colors.GREY_900,
                on_background=ft.Colors.WHITE,
                surface=ft.Colors.GREY_800,
                on_surface=ft.Colors.WHITE
            ),
            page_transitions=ft.PageTransitionsTheme(
                windows=ft.PageTransitionTheme.NONE
            )
        )
    }

    @staticmethod
    def apply(page: ft.Page, theme: str):
        new_theme = Theme.themes.get(theme)

        if not new_theme: raise ValueError("Does not exists the specified theme.")
        
        Theme.colors = new_theme.color_scheme
        page.theme = new_theme
        page.update()