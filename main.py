"""Главный модуль."""

import arcade

import config
from db.history import history
from db.questions import questions
from sound import SoundManager
from utils import Timer
from views.finish_view import FinishView
from views.history_view import HistoryView
from views.menu_view import MenuView
from views.quiz_view import QuizView
from views.statistics_view import StatisticsView


class App(arcade.Window):
    """Приложение."""

    def __init__(self) -> None:
        """Инициализирует приложение с вопросами, плеером и роутером представлений."""
        super().__init__(title=config.TITLE, fullscreen=True)
        self.questions = questions
        self.slides = history
        self.player = SoundManager()
        self.timer = Timer(config.TIME_LEFT_SEC)  # проксируется в BaseView
        self.texture_cache: dict[str, arcade.Texture] = {}
        self._preload_textures()
        # TODO: прелоад общей статистики чтобы не было тормозов при первом ее открытии
        self.font_cache: dict[str, arcade.Texture] = {}
        self._load_fonts()
        self.show_menu()

    def exit(self) -> None:
        """Выход."""
        arcade.exit()

    def show_menu(self) -> None:
        """Переходит к представлению меню."""
        view = MenuView()
        self.show_view(view)

    def show_quiz(self) -> None:
        """Переходит к представлению викторины."""
        view = QuizView(self.questions)
        self.show_view(view)

    def show_finish(self, statistics: dict) -> None:
        """Переходит к представлению индивидуальной статистики после викторины."""
        view = FinishView(statistics)
        self.show_view(view)

    def show_statistics(self) -> None:
        """Переходит к представлению общей статистики всех пользователей."""
        view = StatisticsView()
        self.show_view(view)

    def show_history(self) -> None:
        """Переходит к представлению истории."""
        view = HistoryView(self.slides)
        self.show_view(view)

    def get_texture(self, filename: str) -> arcade.Texture:
        """Отдает текстуру из кэша, проксируется в BaseView."""
        filename = str(filename)

        if filename not in self.texture_cache:
            path = config.IMAGE_DIR / filename
            self.texture_cache[filename] = arcade.load_texture(str(path))

        return self.texture_cache[filename]

    def _preload_textures(self) -> None:
        """Кэширует все текстуры."""
        allowed = {".png", ".jpg", ".jpeg"}
        for file in config.IMAGE_DIR.iterdir():
            if file.is_file() and file.suffix.lower() in allowed:  # TODO: лестница
                if file.name not in self.texture_cache:
                    self.texture_cache[file.name] = arcade.load_texture(str(file))

    def _load_fonts(self) -> None:
        """Загружает все шрифты.

        В arcade шрифты загружаются один раз и доступны
        по своему имени внутри файла шрифта.
        """
        for file in config.FONT_DIR.iterdir():
            if file.suffix.lower() == ".ttf":
                arcade.load_font(str(file))


if __name__ == "__main__":
    App()
    arcade.run()
