import flet as ft
from models.enums import UserLevel
from myapp import MyApp

class Badge(ft.Container):
    def __init__(self, name: UserLevel):
        super().__init__(
            content=ft.Row(
                spacing=4,
                controls=[
                    ft.Image(
                        src=BADGE_IMAGES.get(name),
                        width=20,
                        height=20,
                    ),

                    ft.Text(
                        value=name,
                        font_family=MyApp.font_secondary,
                        weight=ft.FontWeight.BOLD,
                        #color=TEXT_COLOR.get(name)
                    )
                ]
            )
        )

BADGE_IMAGES = {
    UserLevel.EVERYONE: "assets/icons/everyone.png",
    UserLevel.FOLLOWER: "assets/icons/follower.png",
    UserLevel.MODERATOR: "assets/icons/moderator.png",
    UserLevel.SUBSCRIBER: "assets/icons/subscriber.png",
    UserLevel.BROADCASTER: "assets/icons/broadcaster.png",
    UserLevel.VIP: "assets/icons/vip.png",
}

TEXT_COLOR = {
    UserLevel.EVERYONE: ft.Colors.BLUE,
    UserLevel.FOLLOWER: ft.Colors.ORANGE,
    UserLevel.MODERATOR: ft.Colors.GREEN,
    UserLevel.SUBSCRIBER: ft.Colors.PURPLE,
    UserLevel.BROADCASTER: ft.Colors.RED,
    UserLevel.VIP: ft.Colors.PINK,
}