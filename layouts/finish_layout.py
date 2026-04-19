"""Модуль макета экрана завершения."""

from collections.abc import Callable

import arcade.gui

import utils
from layouts.base_layout import BaseLayout


class FinishLayout(BaseLayout):
    """Макет для отображения результатов викторины."""

    def __init__(
            self,
            width: int,
            height: int,
            statistics: dict,
            on_menu: Callable,
    ) -> None:
        """Инициализирует макет."""
        super().__init__(
            width=width,
            height=height,
            header_ratio=0.1,
            content_ratio=0.9,
            footer_ratio=0.1,
        )
        self._setup_ui(statistics, on_menu)

    def _setup_ui(self, statistics: dict, on_menu: Callable) -> None:
        # Заголовок
        status_formatted = statistics["статус"].capitalize() + "!"
        title = self.create_label(status_formatted, font_size=50, font="title")
        self.header_container.add(title, anchor_x="center", anchor_y="center")

        # Cтатистика в столбик
        vbox = arcade.gui.UIBoxLayout(space_between=15, align="left")
        for key, value in statistics.items():
            if key == "статус":
                continue   # в послендем - статус, он и так в тайтле
            if key == "потрачено":
                value = utils.get_formatted_time(value)
            row_text = f"{key}: {value}"
            row = self.create_label(row_text, font_size=22)
            vbox.add(row)
        self.content_container.add(vbox, anchor_x="center", anchor_y="center")

        # Кнопка в нижнем ряду
        btn_menu = self.create_button(on_click=on_menu, text="В МЕНЮ")
        self.footer_container.add(btn_menu, anchor_x="center", anchor_y="center")
