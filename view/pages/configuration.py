import flet as ft
from models.appconfig import AppConfig
from ..controls import *
from services import *
from myapp import MyApp
from ..theme import Theme

class ConfigurationPage(ft.Container):
    def __init__(self, page: ft.Page, app_config: AppConfig) -> None:
        self.page = page
        self.app_config = app_config
        self.set_controls()
        super().__init__(content=self.build())

    def restore_defaults(self) -> None:
        self.app_config.restore_defaults()

    def save_changes(self) -> None:
        self.app_config.language = self.language_dropdown.value
        self.app_config.theme = self.theme_dropdown.value
        self.app_config.client_id = self.client_id_textbox.value
        self.app_config.client_secret = self.client_secret_textbox.value
        self.app_config.redirect_uri = self.redirect_uri_textbox.value

        self.app_config.prefix = self.prefix_textbox.value
        self.app_config.help_word = self.help_word_textbox.value
        self.app_config.enable_word = self.enable_word_textbox.value
        self.app_config.disable_word = self.disable_word_textbox.value
        self.app_config.start_word = self.start_word_textbox.value
        self.app_config.finish_word = self.finish_word_textbox.value

        self.app_config.announce_speaker = self.announce_speaker_checkbox.value
        self.app_config.speak_volume = self.speak_slider.value
        self.app_config.sounds_volume = self.sounds_slider.value
        
        self.app_config.social_media = {
            'facebook': self.facebook_textbox.value,
            'twitter': self.twitter_textbox.value,
            'instagram': self.instagram_textbox.value,
            'tiktok': self.tiktok_textbox.value,
            'youtube': self.youtube_textbox.value,
            'discord': self.discord_textbox.value
        }

        self.app_config.save(MyApp.appconfig_path)
        Theme.apply(self.page, self.app_config.theme)

    def set_controls(self) -> None:
        social_media = self.app_config.social_media

        # General controls
        self.facebook_textbox = TextBox(value=social_media.get('facebook'), height=32, border=0, place_holder='https://facebook.com/username...')
        self.twitter_textbox = TextBox(value=social_media.get('twitter'), height=32, border=0, place_holder='https://twitter.com/username...')
        self.instagram_textbox = TextBox(value=social_media.get('instagram'), height=32, border=0, place_holder='https://instagram.com/username...')
        self.youtube_textbox = TextBox(value=social_media.get('youtube'), height=32, border=0, place_holder='https://youtube.com/username...')
        self.discord_textbox = TextBox(value=social_media.get('discord'), height=32, border=0, place_holder='https://discord.com/invite/...')
        self.tiktok_textbox = TextBox(value=social_media.get('tiktok'), height=32, border=0, place_holder='https://tiktok.com/username...')

        self.theme_dropdown = DropDown(
            value=self.app_config.theme,
            options=[
                ft.DropdownOption(key='light', text='Claro'),
                ft.DropdownOption(key='dark', text='Oscuro')
            ]
        )

        self.language_dropdown = DropDown(
            value=self.app_config.language,
            options=[
                ft.DropdownOption(key='español', text='Español'),
                ft.DropdownOption(key='english', text='English')
            ]
        )

        # Chatbot controls
        self.prefix_textbox = TextBox(value=self.app_config.prefix)
        self.help_word_textbox = TextBox(value=self.app_config.help_word)
        self.enable_word_textbox = TextBox(value=self.app_config.enable_word)
        self.disable_word_textbox = TextBox(value=self.app_config.disable_word)
        self.start_word_textbox = TextBox(value=self.app_config.start_word)
        self.finish_word_textbox = TextBox(value=self.app_config.finish_word)

        self.bot_language_textbox = DropDown(
            value=self.app_config.bot_language,
            options=[
                ft.DropdownOption(key='español', text='Español'),
                ft.DropdownOption(key='english', text='English')
            ]
        )

        # Security controls
        self.client_id_textbox = TextBox(value=self.app_config.client_id, password=True, can_reveal_password=True)
        self.client_secret_textbox = TextBox(value=self.app_config.client_secret, password=True, can_reveal_password=True)
        self.redirect_uri_textbox = TextBox(value=self.app_config.redirect_uri, place_holder='https://localhost:300')

        # Sound controls
        self.announce_speaker_checkbox = CheckBox(text="Mencionar nombre del usuario al leer comentario.", checked=self.app_config.announce_speaker)

        self.speak_slider = ft.Slider(
            value=self.app_config.speak_volume,
            padding=ft.padding.symmetric(horizontal=0, vertical=4),
            #on_change=lambda e: setattr(self.app_config, 'speak_volume', e.control.value)
        )

        self.sounds_slider = ft.Slider(
            value=self.app_config.sounds_volume,
            padding=ft.padding.symmetric(horizontal=0, vertical=4),
        )

    # Build the view UI of configuration page
    def build(self) -> ft.Container:
        return ft.Column(
            expand=True,
            spacing=0,
            controls=[
                ft.Container(
                    expand=True,
                    padding=0,
                    content=TabControl(
                        tabs=[
                            # General settings tab
                            ft.Tab(
                                text="General",
                                content=ft.Container(
                                    padding=32,
                                    content=ft.Column(
                                        scroll=ft.ScrollMode.ADAPTIVE,
                                        spacing=20,
                                        controls=[
                                            ft.Column(
                                                spacing=0,
                                                controls=[
                                                    Label('Tema:'),
                                                    self.theme_dropdown
                                                ]
                                            ),

                                            ft.Column(
                                                spacing=0,
                                                controls=[
                                                    Label('Lenguaje:'),
                                                    self.language_dropdown
                                                ]
                                            ),

                                            Label('Redes sociales:'),
                                            
                                            ft.ResponsiveRow(
                                                spacing=20,
                                                run_spacing=8,
                                                columns=2,
                                                controls=[
                                                    ft.Row(
                                                        col={'sm': 2, 'md': 1 },
                                                        controls=[
                                                            ft.Image(width=32, src='social media/facebook.png'),
                                                            self.facebook_textbox
                                                        ]
                                                    ),

                                                    ft.Row(
                                                        col={'sm': 2, 'md': 1 },
                                                        controls=[
                                                            ft.Image(width=32, src='social media/twitter.png'),
                                                            self.twitter_textbox
                                                        ]
                                                    ),

                                                    ft.Row(
                                                        col={'sm': 2, 'md': 1 },
                                                        controls=[
                                                            ft.Image(width=32, src='social media/instagram.png'),
                                                            self.instagram_textbox
                                                        ]
                                                    ),

                                                    ft.Row(
                                                        col={'sm': 2, 'md': 1 },
                                                        controls=[
                                                            ft.Image(width=32, src='social media/tiktok.png'),
                                                            self.tiktok_textbox
                                                        ]
                                                    ),

                                                    ft.Row(
                                                        col={'sm': 2, 'md': 1 },
                                                        controls=[
                                                            ft.Image(width=32, src='social media/youtube.png'),
                                                            self.youtube_textbox
                                                        ]
                                                    ),

                                                    ft.Row(
                                                        col={'sm': 2, 'md': 1 },
                                                        controls=[
                                                            ft.Image(width=32, src='social media/discord.png'),
                                                            self.discord_textbox
                                                        ]
                                                    ),
                                                ]
                                            )
                                        ]
                                    )
                                )
                            ),

                            # Chatbot settings tab
                            ft.Tab(
                                text='Chatbot',
                                content=ft.Container(
                                    padding=32,
                                    content=ft.Column(
                                        spacing=20,
                                        scroll=ft.ScrollMode.ADAPTIVE,
                                        controls=[
                                            ft.RadioGroup(
                                                content=ft.Column(
                                                    spacing=0,
                                                    controls=[
                                                        ft.Radio(value='1', label='Al iniciar la aplicación'),
                                                        ft.Radio(value='2', label='Al iniciar stream'),
                                                        ft.Radio(value='3', label='Manualmente')
                                                    ]
                                                )
                                            ),

                                            ft.Column(
                                                spacing=0,
                                                controls=[
                                                    Label('Lenguaje del Bot:'),
                                                    self.bot_language_textbox
                                                ]
                                            ),

                                            ft.ResponsiveRow(
                                                spacing=20,
                                                run_spacing=20,
                                                columns=2,
                                                controls=[
                                                    ft.Column(
                                                        spacing=0,
                                                        col={'xs': 2, 'sm': 1},
                                                        controls=[
                                                            Label('Prefijo:'),
                                                            self.prefix_textbox
                                                        ]
                                                    ),

                                                    ft.Column(
                                                        spacing=0,
                                                        col={'xs': 2, 'sm': 1},
                                                        controls=[
                                                            Label('Help word:'),
                                                            self.help_word_textbox
                                                        ]
                                                    ),

                                                    ft.Column(
                                                        spacing=0,
                                                        col={'xs': 2, 'sm': 1},
                                                        controls=[
                                                            Label('Enable word:'),
                                                            self.enable_word_textbox
                                                        ]
                                                    ),

                                                    ft.Column(
                                                        spacing=0,
                                                        col={'xs': 2, 'sm': 1},
                                                        controls=[
                                                            Label('Disable word:'),
                                                            self.disable_word_textbox
                                                        ]
                                                    ),

                                                    ft.Column(
                                                        spacing=0,
                                                        col={'xs': 2, 'sm': 1},
                                                        controls=[
                                                            Label('Start word:'),
                                                            self.start_word_textbox
                                                        ]
                                                    ),

                                                    ft.Column(
                                                        spacing=0,
                                                        col={'xs': 2, 'sm': 1},
                                                        controls=[
                                                            Label('Finish word:'),
                                                            self.finish_word_textbox
                                                        ]
                                                    ),
                                                ]
                                            ),

                                            CheckBox('Permitir a los moderadores apagar/encender comandos'),
                                        ]
                                    )
                                )
                            ),

                            # Security settings tab
                            ft.Tab(
                                text='Seguridad',
                                content=ft.Container(
                                    padding=32,
                                    content=ft.Column(
                                        spacing=16,
                                        controls=[
                                            ft.Column(
                                                spacing=0,
                                                controls=[
                                                    Label('Client ID:'),
                                                    self.client_id_textbox
                                                ]
                                            ),

                                            ft.Column(
                                                spacing=0,
                                                controls=[
                                                    Label('Client secret:'),
                                                    self.client_secret_textbox
                                                ]
                                            ),

                                            ft.Column(
                                                spacing=0,
                                                controls=[
                                                    Label('Dirección de redireccionamiento de OAuth:'),
                                                    self.redirect_uri_textbox
                                                ]
                                            ),
                                        ]
                                    )
                                )
                            ),

                            # Sound settings tab
                            ft.Tab(
                                text='Sonido',
                                content=ft.Container(
                                    padding=32,
                                    content=ft.Column(
                                        spacing=0,
                                        controls=[
                                            ft.ResponsiveRow(
                                                spacing=32,
                                                run_spacing=20,
                                                columns=2,
                                                controls=[
                                                    ft.Column(
                                                        spacing=0,
                                                        col={'sm':2, 'md':1},
                                                        controls=[
                                                            Label('Volumen de narrador:'),
                                                            self.speak_slider
                                                        ]
                                                    ),
                                                    ft.Column(
                                                        spacing=0,
                                                        col={'sm':2, 'md':1},
                                                        controls=[
                                                            Label('Volumen de sonidos:'),
                                                            self.sounds_slider
                                                        ]
                                                    )
                                                ]
                                            ),

                                            ft.Column(
                                                controls=[
                                                    self.announce_speaker_checkbox
                                                ]
                                            )
                                        ]
                                    )
                                )
                            )
                        ]
                    )
                ),

                ft.Container(
                    padding=ft.padding.only(left=32, right=32, top=0, bottom=32),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            Button(text='Restaurar', outlined=True, on_click=lambda e: self.restore_defaults()),
                            Button(text='Guardar', outlined=False, on_click=lambda e: self.save_changes())
                        ]
                    )
                )
            ]
        )