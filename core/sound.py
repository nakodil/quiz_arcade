"""Модуль управления звуком и фоновым сопровождением."""

from __future__ import annotations

from typing import TYPE_CHECKING

import arcade

import config

if TYPE_CHECKING:
    import pyglet.media


class SoundManager:
    """Класс для управления аудио-эффектами и фоновой музыкой.

    Запускает одиночные и зацикленные звуки, останавливает все звуки,
    очищает каналы от уже проигранных звуков.
    """

    def __init__(self) -> None:
        """Инициализирует менеджер, загружает звуки."""
        self.is_mute: bool = False

        self.sounds_map: dict[str, str] = {
            "music": "music.mp3",
            "click": "click.mp3",
        }

        self.sounds: dict[str, arcade.Sound] = {
            sound_name: arcade.Sound(config.SOUND_DIR / file_name)
            for sound_name, file_name in self.sounds_map.items()
        }

        self.active_players: list[pyglet.media.Player] = []

    def on_update(self) -> None:
        """Удаляет плееры, которые завершили воспроизведение."""
        self.active_players = [
            player for player in self.active_players if player.playing
        ]

    def play(self, sound_name: str, *, is_loop: bool = False) -> None:
        """Проигрывает звук один раз или циклично.

        Args:
            sound_name: Ключ звука из словаря self.sounds.
            is_loop: Зациклен ли звук.

        """
        if self.is_mute:
            return

        sound: arcade.Sound | None = self.sounds.get(sound_name)
        if not sound:
            return

        player: pyglet.media.Player | None = arcade.play_sound(
            sound,
            loop=is_loop,
            volume=0.5,
        )
        if player:
            self.active_players.append(player)

    def stop_all(self) -> None:
        """Мгновенно останавливает все активные плееры."""
        for player in self.active_players:
            arcade.stop_sound(player)
        self.active_players.clear()

    def toggle_mute(self) -> bool:
        """Переключает состояние звука и возвращает текущее состояние."""
        self.is_mute = not self.is_mute
        if self.is_mute:
            self.stop_all()
        return self.is_mute
