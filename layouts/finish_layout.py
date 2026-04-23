"""Модуль макета экрана завершения."""

from collections.abc import Callable

import arcade.gui

import config
import utils
from layouts.base_layout import BaseLayout


class FinishLayout(BaseLayout):
    """Макет для отображения результатов викторины."""

    def __init__(
            self,
            size: tuple[int, int],
            callbacks: dict | None = None,
            statistics: dict | None = None,
    ) -> None:
        """Инициализирует макет."""
        super().__init__(
            size=size,
            propotrions=(0.1, 0.8, 0.1),
            callbacks=callbacks,
        )
        self._setup_ui(statistics)

    def _setup_ui(self, statistics: dict) -> None:
        # Заголовок
        status_formatted = statistics["статус"].capitalize() + "!"
        title = self.create_label(
            status_formatted,
            font="title",
            font_size=config.FS_MEDIUM,
        )
        self.header_container.add(title, anchor_x="center", anchor_y="center")

        # Cтатистика в столбик
        vbox = arcade.gui.UIBoxLayout(space_between=15, align="left")
        for key, value in statistics.items():
            if key == "статус":
                continue   # в послендем - статус, он уже есть в хедере
            if key == "потрачено":
                value = utils.get_formatted_time(value)
            row_text = f"{key}: {value}"
            row = self.create_label(
                row_text,
                font_size=config.FS_SMALL,
            )
            vbox.add(row)
        self.content_container.add(
            vbox,
            anchor_x="center",
            anchor_y="center",
        )

        # Кнопка в нижнем ряду
        btn_menu = self.create_button(
            on_click=self.callbacks["menu"],
            text="В МЕНЮ",
        )
        self.footer_container.add(
            btn_menu,
            anchor_x="center",
            anchor_y="center",
        )
