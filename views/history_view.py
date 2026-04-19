"""Модуль представления истории."""

from layouts.history_layout import HistoryLayout
from views.base_view import BaseView


class HistoryView(BaseView):
    """Представление для экрана истории (слайды)."""

    def __init__(
            self,
            slides_data: list[dict],
    ) -> None:
        """Инициализирует представление истории.

        Args:
            slides_data: Список словарей с данными слайдов.
            menu_view: Коллбэк кнопки меню
        """
        super().__init__(bg_filename="history_bg.jpg")
        self.slides = slides_data
        self.current_idx = 0
        self.layout: HistoryLayout = HistoryLayout(
            width=self.window.width,
            height=self.window.height,
            on_menu=self.on_menu,
            on_prev=self.on_prev,
            on_next=self.on_next,
            get_texture_func=self.get_texture,
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

    def on_menu(self) -> None:
        """Коллбэк кнопки меню."""
        self.window.show_menu()
