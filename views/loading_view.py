"""Модуль представления загрузки."""

from typing import TYPE_CHECKING

import arcade

if TYPE_CHECKING:
    from main import App

class LoadingView(arcade.View):
    """Экран загрузки с использованием одного объекта текста."""

    window: "App"

    def __init__(self) -> None:
        """Инициализация представления загруки."""
        super().__init__()
        self.progress = 0.0
        self.loader = self.window.preload_assets_gen()

        # Создаем один объект текста раз и навсегда
        self.label = arcade.Text(
            text="ЗАГРУЗКА: 0%",
            x=self.window.width // 2,
            y=self.window.height // 2,
            color=arcade.color.WHITE,
            font_size=30,
            anchor_x="center",
            anchor_y="center",
        )

    def on_update(self, _: float) -> None:
        """Обновляем только текст объекта."""
        try:
            self.progress = next(self.loader)
            # Просто меняем атрибут
            self.label.text = f"ЗАГРУЗКА: {int(self.progress * 100)}%"
        except StopIteration:
            self.window.show_menu()

    def on_draw(self) -> None:
        """Рендер."""
        self.clear()
        self.label.draw()
