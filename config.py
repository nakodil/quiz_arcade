"""Модуль настройки."""

from pathlib import Path

# Часовой пояс для записи времени в статистику
TIMEZONE = "Europe/Moscow"

# Название в макете меню
TITLE = "Викторина о космосе"

# Время на викторину
TIME_LEFT_SEC = 20

# Статус при завершении викторины
STATUS =  {
    "interrupted": "прервано",
    "completed": "викторина окончена",
    "time_is_over": "время вышло",
}

# Семейства шрифтов
# Не имя файла, открой файл шрифта - посмотри правильное имя
FONTS = {
    "main": "Space Age Cyrillic",
    "title": "PT Sans",
    "topic": "WDXL Lubrifont TC",
    "text": "PT Sans",
    "mono": "Martian Mono SemiExpanded Regular",
    "button": "Martian Mono SemiExpanded Regular",
}

# Кегль шрифтов
FS_XXL = 60
FS_LARGE = 60
FS_MEDIUM = 35
FS_SMALL = 25
FS_S = 15

# Пути
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
IMAGE_DIR = ASSETS_DIR / "img"
FONT_DIR = ASSETS_DIR / "font"
SOUND_DIR = ASSETS_DIR / "sound"
STATISTICS_JSON = "statistics.json"

# Прозрачность оверлея над фоном (0-255)
OVERLAY_ALPHA = 200
