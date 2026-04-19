"""Модуль представления меню."""

from layouts.menu_layout import MenuLayout
from views.base_view import BaseView


class MenuView(BaseView):
    def __init__(self) -> None:
        super().__init__(bg_filename="menu_bg.jpg")

        callbacks = {
            "quiz": self._go_quiz,
            "history": self._go_history,
            "stats": self._go_stats,
            "exit": self._exit,
        }

        self.layout = MenuLayout(
            width=self.window.width,
            height=self.window.height,
            callbacks=callbacks,
        )

        self.setup_layout(self.layout)

        self.ui.add(self.layout)

    def _go_quiz(self):
        self.window.show_quiz()

    def _go_history(self):
        self.window.show_history()

    def _go_stats(self):
        self.window.show_statistics()

    def _exit(self):
        self.window.exit()
