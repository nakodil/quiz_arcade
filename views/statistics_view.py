"""Модуль представления общей статистики."""

import math

from layouts.statistics_layout import StatisticsLayout
from views.base_view import BaseView


class StatisticsView(BaseView):
    """Логика пагинации и загрузки данных статистики."""

    def __init__(self, data: list) -> None:
        super().__init__("statistics_bg.jpg")

        # Разворачиваем данные (свежие сверху)
        self.data = list(reversed(data))

        # Настройки пагинации
        self.current_page = 0
        self.items_per_page = 10
        self.total_pages = math.ceil(len(self.data) / self.items_per_page)

        # Создаем макет
        self.layout = StatisticsLayout(
            width=self.window.width,
            height=self.window.height,
            on_menu=self.on_menu,
            on_prev=self.on_prev,
            on_next=self.on_next,
        )
        self.setup_layout(self.layout)
        self._update_display()

    def _update_display(self) -> None:
        """Вычисляет срез данных и просит макет их отрисовать."""
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        page_data = self.data[start:end]

        self.layout.render_page(
            records=page_data,
            page_num=self.current_page,
            total_pages=self.total_pages
        )

    def on_next(self) -> None:
        """Коллбэк кнопки следующего слайда."""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self._update_display()

    def on_prev(self) -> None:
        """Коллбэк кнопки предыдущего слайда."""
        if self.current_page > 0:
            self.current_page -= 1
            self._update_display()

    def on_menu(self) -> None:
        """Коллбэк кнопки следующего меню."""
        self.window.show_menu()
