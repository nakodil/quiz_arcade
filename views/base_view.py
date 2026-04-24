"""Модуль базового представления, родительского для всех остальных."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import App

import arcade
import arcade.gui

import config
from core import utils
from layouts import BaseLayout


class BaseView(arcade.View):
    """Базовое представление."""

    window: "App"

    def __init__(self, bg_filename: str | None = None) -> None:
        """Инициализирует базовое представление."""
        super().__init__()
        self.bg_filename = bg_filename
        self.sprites = arcade.SpriteList()
        self._make_sprites()
        self.ui = arcade.gui.UIManager()
        self.layout: BaseLayout
        self.callbacks = {
            "exit": self.window.exit,
            "menu": self.window.show_menu,
            "quiz": self.window.show_quiz,
            "statistics": self.window.show_statistics,
            "finish": self.window.show_finish,
            "history": self.window.show_history,
            "sound": self._on_sound_toggle,
        }

    def _make_sprites(self) -> None:
        """Создает все спрайты."""
        if not self.bg_filename:
            return

        # Фоновое изображение
        texture = self.window.get_texture(self.bg_filename)
        scale = utils.get_image_scale(
            texture.width,
            texture.height,
            self.window.width,
            self.window.height,
        )
        coords = (self.window.width / 2, self.window.height / 2)
        sprite = arcade.Sprite(
            texture,
            scale,
            coords[0],
            coords[1],
        )
        self.sprites.append(sprite)

        # Оверлей
        color = arcade.types.Color(0, 0, 0, config.OVERLAY_ALPHA)
        sprite = arcade.SpriteSolidColor(
            self.window.width,
            self.window.height,
            coords[0],
            coords[1],
            color,
        )
        self.sprites.append(sprite)

    def update_background(self, filename: str) -> None:
        """Динамически меняет текстуру фона и пересчитывает масштаб."""
        if not self.sprites:
            return

        self.bg_filename = filename
        texture = self.window.get_texture(filename)

        # Первый спрайт в self.sprites - это фон
        bg_sprite = self.sprites[0]
        bg_sprite.texture = texture
        bg_sprite.scale = utils.get_image_scale(
            texture.width,
            texture.height,
            self.window.width,
            self.window.height,
        )

    def _on_sound_toggle(self) -> None:
        """Коллбэк кнопки звука.

        Вызывает метод изменения текста кнопки в макете.
        Вызывает метод окна для управления плеером.
        """
        self.layout.sound_btn_update(self.window.player.is_mute)
        self.window.on_sound_toggle()

    def setup_layout(self, layout: BaseLayout) -> None:
        """Настраивает макет и вешает на него фон."""
        self.sprites.clear()
        self._make_sprites()
        self.layout = layout
        self.layout.make_required_buttons()
        self.ui.add(self.layout)

    def get_texture(self, filename: str) -> arcade.Texture:
        """Проксирует доступ к кэшу текстур в App."""
        return self.window.get_texture(filename)

    def on_show_view(self) -> None:
        """Запускает менеджер интерфейса."""
        self.ui.enable()

    def on_hide_view(self) -> None:
        """Останавливает менеджер интерфейса."""
        self.ui.disable()

    def on_draw(self) -> None:
        """Отрисовка.

        Порядок:
        1. Очистка окна
        2. Спрайты (последним спрайтом всегда должен быть оверлей)
        3. GUI
        """
        self.clear()
        self.sprites.draw()
        self.ui.draw()

    def on_key_press(self, symbol: int, _: int) -> None:
        """Выход клавишей ESC."""
        if symbol == arcade.key.ESCAPE:
            self.window.exit()
