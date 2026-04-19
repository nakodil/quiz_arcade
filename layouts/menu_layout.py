"""Модуль макета меню."""

import arcade.gui

import config
from layouts.base_layout import BaseLayout


class MenuLayout(BaseLayout):
    """Макет меню."""

    def __init__(
            self,
            width: int,
            height: int,
            callbacks: dict,
    ) -> None:
        """Инициализирует макет меню."""
        super().__init__(
            width=width,
            height=height,
            header_ratio=0.1,
            content_ratio=0.8,
            footer_ratio=0.1,
        )
        self._setup_ui(callbacks)

    def _setup_ui(self, callbacks: dict) -> None:
        """Создание интерфейса."""
        # Название посередине ряда контента
        title = self.create_label(
            text=config.TITLE,
            font_size=54,
            font="main",
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

        # Описываем структуру кнопок
        menu_items = [
            ("ВЫХОД", callbacks["exit"]),
            ("ИСТОРИЯ", callbacks["history"]),
            ("СТАТИСТИКА", callbacks["stats"]),
            ("ВИКТОРИНА", callbacks["quiz"]),
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
