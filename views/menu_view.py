"""Модуль представления меню."""

from layouts import MenuLayout
from views import BaseView


class MenuView(BaseView):
    """Представление меню."""

    layout: MenuLayout

    def __init__(self) -> None:
        """Инициализирует представление меню."""
        super().__init__(bg_filename="menu_bg.jpg")
        self.layout = MenuLayout(
            size=(self.window.width, self.window.height),
            callbacks=self.callbacks,
        )
        self.setup_layout(self.layout)
        self.ui.add(self.layout)
