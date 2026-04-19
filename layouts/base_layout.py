"""Модуль базового макета."""

from collections.abc import Callable

import arcade
import arcade.gui

import config


class BaseLayout(arcade.gui.UIAnchorLayout):
    """Базовый макет."""

    def __init__(
            self,
            width: int = 1920,
            height: int = 1080,
            header_ratio: float | None = 0.05,
            content_ratio: float | None = 0.9,
            footer_ratio: float | None = 0.05,
            **kwargs,
    ) -> None:
        """Инициализирует базовый макет.

        Обертка по размеру корневого контейнера (элементы - вертикально)
            Верний ряд (5% высоты)
            Средний ряд (90% высоты)
            Нижний ряд (5% высоты)
        """
        super().__init__(size_hint=(1, 1), **kwargs)

        # Размер корневого контейнера
        self.width = width
        self.height = height

        # Пропорции высоты рядов
        self.header_ratio = header_ratio
        self.content_ratio = content_ratio
        self.footer_ratio = footer_ratio

        # Отступы
        self.padding_hor = round(self.width * 0.01)
        self.padding_ver = self.padding_hor

        # Обертка
        self.body_container = arcade.gui.UIBoxLayout(
            size_hint=(1, 1), vertical=True,
        )

        # Верхний ряд обертки
        self.header_container = arcade.gui.UIAnchorLayout(
            size_hint=(1, self.header_ratio),
        ).with_padding(
            top=self.padding_ver,
            bottom=self.padding_ver,
            left=self.padding_hor,
            right=self.padding_hor,
        )

        # Средний ряд обертки
        self.content_container = arcade.gui.UIAnchorLayout(
            size_hint=(1, self.content_ratio),
        ).with_padding(
            top=0,  # этот отступ сделает хэдер
            bottom=0,  # этот отступ сделает хэдер
            left=self.padding_hor,
            right=self.padding_hor,
        )

        # Нижний ряд обертки
        self.footer_container = arcade.gui.UIAnchorLayout(
            size_hint=(1, self.footer_ratio),
        ).with_padding(
            top=self.padding_ver,
            bottom=self.padding_ver,
            left=self.padding_hor,
            right=self.padding_hor,
        )

        # Добавляем контейнеры в обертку
        self.body_container.add(self.header_container)
        self.body_container.add(self.content_container)
        self.body_container.add(self.footer_container)

        # Добавляем обертку
        self.add(self.body_container)

    def create_label(
            self,
            text: str = "",
            font_size: int = 20,
            font: str = "text",
            **kwargs,
    ) -> arcade.gui.UILabel:
        """Фабрика создания текстов для всех макетов."""
        return arcade.gui.UILabel(
            text=text,
            font_size=font_size,
            font_name=config.FONTS[font],
            text_color=arcade.color.WHITE,
            **kwargs,
        )

    def create_button(
            self,
            on_click: Callable,
            text: str = "",
            width: int = 200,
            height: int = 60,
    ) -> arcade.gui.UIFlatButton:
        """Фабрика создания кнопок для всех макетов."""
        btn = arcade.gui.UIFlatButton(
            text=text,
            width=width,
            height=height,
        )

        @btn.event("on_click")
        def _handler(_: arcade.gui.UIEvent) -> None:
            """Не пускаем событие дальше, вместо него коллбэки."""
            on_click()

        return btn

    def debug_layout(self) -> None:
        """Заливает контейнеры прозрачным цветом."""
        self.header_container = self.header_container.with_background(
            color=arcade.color.RED.replace(a=100),
        )
        self.content_container = self.content_container.with_background(
            color=arcade.color.GREEN.replace(a=100),
        )
        self.footer_container = self.footer_container.with_background(
            color=arcade.color.BLUE.replace(a=100),
        )
