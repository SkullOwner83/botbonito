import flet as ft
from utilities.enums import UserLevel
from myapp import MyApp

class Badge(ft.Container):
    def __init__(self, name: str) -> None:
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
                        weight=ft.FontWeight.BOLD
                    )
                ]
            )
        )

BADGE_IMAGES = {
    UserLevel.EVERYONE: "assets/user levels/everyone.png",
    UserLevel.FOLLOWER: "assets/user levels/follower.png",
    UserLevel.MODERATOR: "assets/user levels/moderator.png",
    UserLevel.SUBSCRIBER: "assets/user levels/subscriber.png",
    UserLevel.BROADCASTER: "assets/user levels/broadcaster.png",
    UserLevel.VIP: "assets/user levels/vip.png",
}