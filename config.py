"""Модуль настройки."""

from pathlib import Path

TITLE = "Викторина о космосе"

TIME_LEFT_SEC = 20

STATUS =  {
    "interrupted": "прервано",
    "completed": "викторина окончена",
    "time_is_over": "время вышло",
}

# Не имя файла, открой файл шрифта - посмотри правильное имя
FONTS = {
    "main": "Space Age Cyrillic",
    "title": "PT Sans",
    "topic": "PT Sans",
    "text": "PT Serif",
    "mono": "IBM Plex Mono",
    "button": "Space Age Cyrillic",
}

TIMEZONE = "Europe/Moscow"

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
IMAGE_DIR = ASSETS_DIR / "img"
FONT_DIR = ASSETS_DIR / "font"
SOUND_DIR = ASSETS_DIR / "sound"
STATISTICS_JSON = "statistics.json"
