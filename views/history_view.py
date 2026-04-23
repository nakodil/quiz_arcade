"""Модуль представления истории."""

from layouts import HistoryLayout
from views import BaseView


class HistoryView(BaseView):
    """Представление для экрана истории (слайды)."""

    layout: HistoryLayout

    def __init__(
            self,
            slides_data: list[dict],
    ) -> None:
        """Инициализирует представление истории."""
        super().__init__(bg_filename="history_bg.jpg")
        self.slides = slides_data
        self.current_idx = 0

        # Создаем макет
        additional_callbacks = {
            "get texture": self.window.get_texture,
            "on prev": self.on_prev,
            "on next": self.on_next,
        }
        self.callbacks.update(additional_callbacks)
        self.layout: HistoryLayout = HistoryLayout(
            size=(self.window.width, self.window.height),
            callbacks=self.callbacks,
        )
        self.setup_layout(self.layout)
        self.ui.add(self.layout)
        self.setup()

    def setup(self) -> None:
        """Настройка представления перед показом."""
        self.current_idx = 0
        self.update_slide_view()

    def update_slide_view(self) -> None:
        """Вызывает перерисовку макета с текущими данными слайда."""
        if not self.slides:
            return

        # Передаем данные в макет
        self.layout.render_slide(
            slide=self.slides[self.current_idx],
            current_idx=self.current_idx,
            total=len(self.slides),
        )

    def on_prev(self) -> None:
        """Коллбэк кнопки предыдущего слайда."""
        if self.current_idx > 0:
            self.current_idx -= 1
            self.update_slide_view()

    def on_next(self) -> None:
        """Коллбэк кнопки следующего слайда."""
        if self.current_idx < len(self.slides) - 1:
            self.current_idx += 1
            self.update_slide_view()
