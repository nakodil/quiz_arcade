"""Модуль представления индивидуальной статистики."""

import utils
import config
from views.base_view import BaseView
from layouts.finish_layout import FinishLayout


class FinishView(BaseView):
    """Представление финального экрана (логика сохранения и навигации)."""

    def __init__(self, statistics: dict) -> None:
        super().__init__("finish_bg.jpg")

        # Сохраняем персональную статистику в общую
        utils.save_json(config.STATISTICS_JSON, statistics)

        # Инициализируем макет и передаем данные
        self.layout = FinishLayout(
            width=self.window.width,
            height=self.window.height,
            statistics=statistics,
            on_menu=self.on_menu,
        )
        self.ui.add(self.layout)

    def on_menu(self) -> None:
        """Коллбэк кнопки меню."""
        self.window.show_menu()
