"""Модуль утилит."""

import json
from pathlib import Path


def get_image_scale(
        source_w: float,
        source_h: float,
        target_w: float,
        target_h: float,
        mode: str = "cover",
) -> float:
    """Возвращает масштаб для изображения."""
    scale_x = target_w / source_w
    scale_y = target_h / source_h
    if mode == "cover":
        return max(scale_x, scale_y)
    if mode == "contain":
        return min(scale_x, scale_y)
    return -1


def get_formatted_time(time: float, sep: str = ":") -> str:
    """Возвращает время строкой в формате ЧЧ:ММ:СС."""
    time_total = round(time)
    hours = time_total // (60 * 60)
    minutes = time_total // 60 % 60
    seconds = time_total % 60
    return f"{hours:02}{sep}{minutes:02}{sep}{seconds:02}"


def load_json(path: Path) -> list:
    """Безопасно загружает JSON как список."""
    if not path.exists() or path.stat().st_size == 0:
        return []

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)

            if isinstance(data, list):
                return data
            return []

    except json.JSONDecodeError:
        return []


def write_json(path: Path, data: list | dict) -> None:
    """Записывает данные в JSON."""
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


class Timer:
    """Таймер обратного отсчета."""

    def __init__(self, time_left: int = 300) -> None:
        """Инициализирует таймер."""
        self.total_time = time_left
        self.time_left = self.total_time
        self.color = "normal"
        self.is_over = False

    def setup(self) -> None:
        """Исходное состояние."""
        self.is_over = False
        self.time_left = self.total_time

    def on_update(self, delta_time: float) -> None:
        """Отнимает время и задает цвет цифр."""
        self.time_left -= delta_time
        if self.time_left <= self.total_time * 0.1:
            self.color = "warning"
        if self.time_left <= 0:
            self.is_over = True

    def get_time_str(self) -> str:
        """Отдает время в формате ЧЧ:ММ:СС."""
        return get_formatted_time(self.time_left)
