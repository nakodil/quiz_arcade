"""Модуль приложения."""

from collections.abc import Generator

import arcade

import config
from views import (
    FinishView,
    HistoryView,
    LoadingView,
    MenuView,
    QuizView,
    StatisticsView,
)

from . import utils
from .sound import SoundManager


class App(arcade.Window):
    """Приложение."""

    def __init__(self) -> None:
        """Инициализирует приложение с вопросами, плеером и роутером представлений."""
        super().__init__(title=config.TITLE, fullscreen=True)
        self.questions = utils.load_json(config.QUESTIONS_JSON)
        self.slides = utils.load_json(config.HISTORY_JSON)
        self.player = SoundManager()
        self.timer = utils.Timer(config.TIME_LEFT_SEC)  # проксируется в BaseView
        self.texture_cache: dict[str, arcade.Texture] = {}
        self.font_cache: dict[str, arcade.Texture] = {}
        self.stats_cache: list[dict] = []  # Кэш для общей статистики
        self.show_loading()

    def exit(self) -> None:
        """Выход."""
        arcade.exit()

    def show_loading(self) -> None:
        """Переходит к представлению загрузки."""
        view = LoadingView()
        self.show_view(view)

    def on_loading_finish(self) -> None:
        """Включает музыку и показывает представление меню."""
        if not self.player.is_mute:
            self.player.play("music", is_loop=True)
        self.show_menu()

    def on_sound_toggle(self) -> None:
        """Коллбэк кнопки ВКЛ/ОТКЛ звука."""
        is_mute = self.player.toggle_mute()
        if is_mute:
            self.player.stop_all()
        else:
            self.player.play("music", is_loop=True)

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
        view = StatisticsView(data=self.stats_cache)
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

    def save_new_result(self, result: dict) -> None:
        """Обновляет и синхронизирует кэш."""
        # 1. Обновляем кэш статистики
        self.stats_cache.append(result)

        # 2. Перезаписываем статистику кэшем
        utils.write_json(config.STATISTICS_JSON, self.stats_cache)

    def preload_assets_gen(self) -> Generator[float]:
        """Генератор для поочередной загрузки шрифтов и текстур.

        Yields:
            float: Прогресс загрузки от 0.0 до 1.0.

        """
        # Загрузка шрифтов
        font_files = [
            f for f in config.FONT_DIR.iterdir()
            if f.suffix.lower() in config.FONT_FILE_TYPES
        ]
        for file in font_files:
            arcade.load_font(str(file))
            yield 0.05

        # 2. Загрузка текстур
        allowed = config.TEXTURE_FILE_TYPES
        image_files = [
            f for f in config.IMAGE_DIR.iterdir()
            if f.is_file() and f.suffix.lower() in allowed
        ]

        total = len(image_files)
        for i, file in enumerate(image_files):
            if file.name not in self.texture_cache:
                self.texture_cache[file.name] = arcade.load_texture(str(file))

            # Рассчитываем прогресс (от 0.1 до 1.0)
            progress = 0.1 + (i + 1) / total * 0.9
            yield min(progress, 1.0)

        # Загрузка статистики (JSON)
        self.stats_cache = utils.load_json(config.STATISTICS_JSON)
        yield 1.0
