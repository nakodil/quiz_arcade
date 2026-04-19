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


def load_json(file_name: str) -> list:
    """Безопасно загружает JSON как список."""
    file_path = Path(file_name)

    if not file_path.exists() or file_path.stat().st_size == 0:
        return []

    try:
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

            if isinstance(data, list):
                return data
            return []

    except json.JSONDecodeError:
        return []


def write_json(file_name: str, data: list | dict) -> None:
    """Просто записывает данные в файл, без предварительного чтения."""
    file_path = Path(file_name)
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


class Timer:
    """Таймер обратного отсчета."""

    def __init__(self, time_left: int = 300) -> None:
        self.total_time = time_left
        self.time_left = self.total_time
        self.color = "normal"

    def setup(self) -> None:
        self.time_left = self.total_time

    def on_update(self, delta_time: float) -> None:
        self.time_left -= delta_time
        if self.time_left <= self.total_time * 0.1:
            self.color = "warning"

    def get_time_str(self) -> str:
        return get_formatted_time(self.time_left)

    def is_over(self) -> bool:
        return self.time_left <= 0
