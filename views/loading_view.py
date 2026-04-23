"""Модуль представления загрузки."""

from typing import TYPE_CHECKING

import arcade

import config

if TYPE_CHECKING:
    from main import App


class LoadingView(arcade.View):
    """Представление загрузки: макет реализован прямо в предстявлени."""

    window: "App"

    def __init__(self) -> None:
        """Инициализация представления загруки."""
        super().__init__()
        self.progress = 0.0
        self.loader = self.window.preload_assets_gen()
        self.loading_lbl: arcade.Text
        self.setup()

    def setup(self) -> None:
        """Создает элементы интерфейса."""
        self.loading_lbl = arcade.Text(
            text=f"загрузка: {int(self.progress * 100)}%",
            x=self.window.width // 2,
            y=self.window.height // 2,
            color=arcade.color.WHITE,
            font_size=config.FS_XXL,
            anchor_x="center",
            anchor_y="center",
        )

    def on_update(self, _: float) -> None:
        """Обновление текста загрузки."""
        try:
            self.progress = next(self.loader)
            self.loading_lbl.text = f"загрузка: {int(self.progress * 100)}%"
        except StopIteration:
            self.window.on_loading_finish()

    def on_draw(self) -> None:
        """Очищает окно и рисует текст посередине."""
        self.clear()
        self.loading_lbl.draw()
