"""Модуль базового представления, родительского для всех остальных."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import App

import arcade
import arcade.gui

import utils
from layouts.base_layout import BaseLayout


class BaseView(arcade.View):
    """Базовое представление."""

    window: "App"

    def __init__(self, bg_filename: str | None = None) -> None:
        super().__init__()
        self.ui = arcade.gui.UIManager()
        self.layout: arcade.gui.UIAnchorLayout | None = None
        self.sprites = arcade.SpriteList()  # Заменить компонентом UI или свойством контейнера

        if bg_filename:
            self.sprites.append(self._get_bg_sprite(bg_filename))

    def _get_bg_sprite(self, bg_filename: str) -> arcade.Sprite:
        """Отдает спрайт фона."""
        texture = self.get_texture(bg_filename)
        scale = utils.get_image_scale(
            texture.width,
            texture.height,
            self.window.width,
            self.window.height,
        )
        sprite = arcade.Sprite(texture, scale)
        sprite.center_x, sprite.center_y = self.window.width // 2, self.window.height // 2
        return sprite

    def get_texture(self, filename: str) -> arcade.Texture:
        """Проксирует доступ к кэшу текстур в App."""
        return self.window.get_texture(filename)

    def on_show_view(self):
        self.ui.enable()

    def on_hide_view(self):
        self.ui.disable()

    def on_draw(self):
        self.clear()
        self.sprites.draw()

        # Рисуем оверлей над фоном
        arcade.draw_lrbt_rectangle_filled(
            0, self.window.width, 0, self.window.height, (0, 0, 0, 200),
        )

        self.ui.draw()

    def on_key_press(self, symbol: int, _: int) -> None:
        """Выход клавишей ESC."""
        if symbol == arcade.key.ESCAPE:
            self.window.exit()
