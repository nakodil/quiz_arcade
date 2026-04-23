"""Модуль представления индивидуальной статистики."""

from layouts import FinishLayout
from views import BaseView


class FinishView(BaseView):
    """Представление финального экрана (+ логика сохранения и навигации)."""

    layout: FinishLayout

    def __init__(self, statistics: dict) -> None:
        """Инициализирует представление индивидуальной статистики."""
        super().__init__("finish_bg.jpg")

        self.window.save_new_result(statistics)

        # Инициализируем макет и передаем данные
        self.layout = FinishLayout(
            size=(self.window.width, self.window.height),
            callbacks=self.callbacks,
            statistics=statistics,
        )
        self.setup_layout(self.layout)
        self.ui.add(self.layout)

    def on_menu(self) -> None:
        """Коллбэк кнопки меню."""
        self.window.show_menu()
