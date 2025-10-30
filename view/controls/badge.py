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
    UserLevel.EVERYONE: "user levels/everyone.png",
    UserLevel.FOLLOWER: "user levels/follower.png",
    UserLevel.MODERATOR: "user levels/moderator.png",
    UserLevel.SUBSCRIBER: "user levels/subscriber.png",
    UserLevel.BROADCASTER: "user levels/broadcaster.png",
    UserLevel.VIP: "user levels/vip.png",
}