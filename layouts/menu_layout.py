"""Модуль макета меню."""

from collections.abc import Callable

import arcade.gui

import config
from layouts.base_layout import BaseLayout


class MenuLayout(BaseLayout):
    """Макет меню."""

    def __init__(
            self,
            size: tuple[int, int],
            callbacks: dict[str, Callable] | None = None,
    ) -> None:
        """Инициализирует макет меню."""
        super().__init__(
            size=size,
            propotrions=(0.1, 0.8, 0.1),
            callbacks=callbacks,
        )
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Создание интерфейса."""
        # Название посередине ряда контента
        title = self.create_label(
            text=config.TITLE,
            font="main",
            font_size=config.FS_LARGE,
        )
        self.content_container.add(
            title,
            anchor_x="center",
            anchor_y="center",
        )

        # Создаем контейнер для кнопок
        buttons_container = arcade.gui.UIBoxLayout(
            vertical=False,
            space_between=20,
        )

        # Названия кнопок и их коллбэки
        menu_items = [
            ("ИСТОРИЯ", self.callbacks["history"]),
            ("СТАТИСТИКА", self.callbacks["statistics"]),
            ("ВИКТОРИНА", self.callbacks["quiz"]),
        ]

        # Создаем кнопки и кладем их в свой контейнер
        for text, callback in menu_items:
            btn = self.create_button(text=text, on_click=callback)
            buttons_container.add(btn)

        # 3. Размещаем контейнер кнопок в нижнем ряду
        self.footer_container.add(
            buttons_container,
            anchor_x="center",
            anchor_y="center",
        )
