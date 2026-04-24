"""Модуль представления общей статистики."""

import math

from layouts import StatisticsLayout
from views import BaseView


class StatisticsView(BaseView):
    """Общая статистика."""

    layout: StatisticsLayout

    def __init__(self, data: list) -> None:
        """Инициализирует представление статистики."""
        super().__init__("statistics_bg.jpg")

        # Данные: сортировка от новых к старым
        self.data = list(reversed(data))
        self.avg_stats = {}
        self._set_avg_stats()

        # Настройки пагинации
        self.current_page = 0
        self.items_per_page = 10
        self.total_pages = math.ceil(len(self.data) / self.items_per_page)

        # Создаем макет
        additional_callbacks = {
            "prev page": self.on_prev,
            "next page": self.on_next,
        }
        self.callbacks.update(additional_callbacks)
        self.layout = StatisticsLayout(
            size=(self.window.width, self.window.height),
            callbacks=self.callbacks,
        )
        self.setup_layout(self.layout)
        self._update_display()

    def _set_avg_stats(self) -> None:
        """Записывает средние значения статистики в атрибуты."""
        # Вычисляем средние значения показателей из каждой записи статистики
        total_records = len(self.data)
        if total_records > 0:
            avg_correct = sum(
                row.get("верно", 0) for row in self.data
            ) / total_records
            avg_incorrect = sum(
                row.get("ошибки", 0) for row in self.data
            ) / total_records
            avg_time = sum(
                row.get("потрачено", 0) for row in self.data
            ) / total_records
        else:
            avg_correct = avg_incorrect = avg_time = 0

        self.avg_stats = {
            "avg_correct": round(avg_correct, 1),
            "avg_incorrect": round(avg_incorrect, 1),
            "avg_time": avg_time,
        }

    def _update_display(self) -> None:
        """Вычисляет срез данных и просит макет их отрисовать."""
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        page_data = self.data[start:end]

        self.layout.render_page(
            records=page_data,
            page_num=self.current_page,
            total_pages=self.total_pages,
            avg_stats=self.avg_stats,
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
