"""Модуль базового представления, родительского для всех остальных."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import App

import arcade
import arcade.gui

from layouts.base_layout import BaseLayout


class BaseView(arcade.View):
    """Базовое представление."""

    window: "App"

    def __init__(self, bg_filename: str | None = None) -> None:
        """Инициализирует базовое представление."""
        super().__init__()
        self.bg_filename = bg_filename
        self.ui = arcade.gui.UIManager()
        self.layout: arcade.gui.UIAnchorLayout | None = None

    def setup_layout(self, layout: BaseLayout) -> None:
        """Настраивает макет и вешает на него фон."""
        self.layout = layout
        self.ui.add(self.layout)

        if not self.bg_filename:
            return
        texture = self.get_texture(self.bg_filename)
        self.layout.setup_background(texture=texture)

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
        """Очищает окно и рисует весь интерфейс."""
        self.clear()
        self.ui.draw()

    def on_key_press(self, symbol: int, _: int) -> None:
        """Выход клавишей ESC."""
        if symbol == arcade.key.ESCAPE:
            self.window.exit()
