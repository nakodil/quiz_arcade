"""Модуль представления меню."""

import random

import arcade

from layouts import MenuLayout
from views import BaseView


class MenuView(BaseView):
    """Представление меню."""

    layout: MenuLayout

    def __init__(self) -> None:
        """Инициализирует представление меню."""
        super().__init__(bg_filename="menu_bg.jpg")
        self.layout = MenuLayout(
            size=(self.window.width, self.window.height),
            callbacks=self.callbacks,
        )
        self.setup_layout(self.layout)
        self.ui.add(self.layout)

        self.mks = arcade.Sprite(
            self.window.get_texture("mks.png"),
            0.5,
            center_x=self.window.width / 2,
            center_y=self.window.height / 2,
        )
        self.sprites.insert(1, self.mks)  # между фоном и оверлеем

    def on_update(self, _: float) -> bool | None:
        """Обновление спрайтов."""
        self.mks.center_x += random.randint(-1, 1)
        self.mks.center_y += random.randint(-1, 1)
