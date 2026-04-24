"""Модуль настройки."""

import sys
from pathlib import Path

if getattr(sys, "frozen", False):  # PyInstaller ставит автоматически frozen
    BASE_DIR = Path(getattr(sys, "_MEIPASS", sys.executable)).resolve()
    ROOT_DIR = Path(sys.executable).parent.resolve()  # папка, где лежит exe
else:  # Запущен из папки разработки через консоль
    BASE_DIR = Path(__file__).resolve().parent
    ROOT_DIR = BASE_DIR

ASSETS_DIR = BASE_DIR / "assets"
DB_DIR = BASE_DIR / "db"
IMAGE_DIR = ASSETS_DIR / "img"
FONT_DIR = ASSETS_DIR / "font"
SOUND_DIR = ASSETS_DIR / "sound"
STATISTICS_JSON = ROOT_DIR / "statistics.json"

# БД
QUESTIONS_JSON = DB_DIR / "questions.json"
HISTORY_JSON = DB_DIR / "history.json"

# Часовой пояс для записи времени в статистику
TIMEZONE = "Europe/Moscow"

# Название в макете меню
TITLE = "Викторина о космосе"

# Время на викторину в секундах
TIME_LEFT_SEC = 300

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
FS_XL = 30
FS_L = 25
FS_M = 15
FS_S = 10

# Прозрачность оверлея над фоном (0-255)
OVERLAY_ALPHA = 220

# Типы файлов
TEXTURE_FILE_TYPES = {".png", ".jpg", ".jpeg"}
FONT_FILE_TYPES = {".ttf"}
