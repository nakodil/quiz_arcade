"""Модуль представления индивидуальной статистики."""

from layouts.finish_layout import FinishLayout
from views.base_view import BaseView


class FinishView(BaseView):
    """Представление финального экрана (+ логика сохранения и навигации)."""

    def __init__(self, statistics: dict) -> None:
        """Инициализирует представление индивидуальной статистики."""
        super().__init__("finish_bg.jpg")

        self.window.save_new_result(statistics)

        # Инициализируем макет и передаем данные
        self.layout = FinishLayout(
            width=self.window.width,
            height=self.window.height,
            statistics=statistics,
            on_menu=self.on_menu,
        )
        self.setup_layout(self.layout)
        self.ui.add(self.layout)

    def on_menu(self) -> None:
        """Коллбэк кнопки меню."""
        self.window.show_menu()
