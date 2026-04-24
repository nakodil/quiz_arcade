"""Модуль базового макета."""

from collections.abc import Callable
from typing import Any

import arcade
import arcade.gui

import config
from core import utils

BUTTON_STYLE = {
    "normal": arcade.gui.UIFlatButton.UIStyle(
        font_size=config.FS_S,
        font_name=(config.FONTS["button"], "arial"),
        font_color=arcade.color.WHITE,
        bg=arcade.types.Color(0, 0, 100, 100),
        border=arcade.color.WHITE,
        border_width=1,
    ),
    "press": arcade.gui.UIFlatButton.UIStyle(
        font_size=config.FS_S,
        font_name=(config.FONTS["button"], "arial"),
        font_color=arcade.color.WHITE,
        bg=arcade.types.Color(0, 0, 100, 100),
        border=arcade.color.WHITE,
        border_width=1,
    ),
    "hover": arcade.gui.UIFlatButton.UIStyle(
        font_size=config.FS_S,
        font_name=(config.FONTS["button"], "arial"),
        font_color=arcade.color.WHITE,
        bg=arcade.types.Color(128, 128, 128, 150),
        border=arcade.color.WHITE,
        border_width=2,
    ),
    "disabled": arcade.gui.UIFlatButton.UIStyle(
        font_size=config.FS_S,
        font_name=(config.FONTS["button"], "arial"),
        font_color=arcade.color.WHITE,
        bg=arcade.types.Color(128, 128, 128, 100),
        border=arcade.color.WHITE,
        border_width=0,
    ),
}


class BaseLayout(arcade.gui.UIAnchorLayout):
    """Базовый макет."""

    def __init__(
            self,
            size: tuple[int, int] = (1920, 1080),
            propotrions: tuple[float, float, float] = (0.05, 0.9, 0.05),
            callbacks: dict[str, Callable] | None = None,
    ) -> None:
        """Инициализирует базовый макет.

        Слои:
            Контейнер фона
            Обертка по размеру корневого контейнера (элементы - вертикально)
                Верний ряд (5% высоты)
                Средний ряд (90% высоты)
                Нижний ряд (5% высоты)
        """
        super().__init__(size_hint=(1, 1))
        if callbacks:
            self.callbacks = callbacks
        else:
            self.callbacks = {}
        self.sound_btn: arcade.gui.UIFlatButton | None = None
        self.exit_btn: arcade.gui.UIFlatButton | None = None

        # Контейнер фона
        self.bg_container = arcade.gui.UIAnchorLayout()
        self.add(self.bg_container)

        # Размер ?корневого? контейнера
        self.width = size[0]
        self.height = size[1]

        # Пропорции высоты рядов
        self.header_ratio = propotrions[0]
        self.content_ratio = propotrions[1]
        self.footer_ratio = propotrions[2]

        # Отступы
        self.padding_hor = round(self.width * 0.01)
        self.padding_ver = self.padding_hor

        # Обертка рядов
        self.body_container = arcade.gui.UIBoxLayout(
            size_hint=(1, 1), vertical=True,
        )

        # Верхний ряд обертки (хэдер)
        self.header_container = arcade.gui.UIAnchorLayout(
            size_hint=(1, self.header_ratio),
        ).with_padding(
            top=self.padding_ver,
            bottom=self.padding_ver,
            left=self.padding_hor,
            right=self.padding_hor,
        )

        # Средний ряд обертки (контент)
        self.content_container = arcade.gui.UIAnchorLayout(
            size_hint=(1, self.content_ratio),
        ).with_padding(
            top=0,  # этот отступ сделает хэдер
            bottom=0,  # этот отступ сделает хэдер
            left=self.padding_hor,
            right=self.padding_hor,
        )

        # Нижний ряд обертки (футер)
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

        # Добавляем обертку в корневой контейнер
        self.add(self.body_container)

    def create_label(
            self,
            text: str = "",
            font_size: int = config.FS_M,
            font: str = "text",
            **kwargs: Any,  # noqa: ANN401
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
            style=BUTTON_STYLE,
        )

        @btn.event("on_click")
        def _handler(_: arcade.gui.UIEvent) -> None:
            """Не пускаем событие дальше, вместо него коллбэки."""
            on_click()

        return btn

    def setup_background(
            self,
            texture: arcade.Texture,
    ) -> None:
        """Создает фон из слоев.

        Каждый слой - контейнер:
            1. Слой заливки цветом - оверлей
            2. Слой изображения
        """
        self.bg_container.clear()

        # Изображение
        scale = utils.get_image_scale(
            texture.width,
            texture.height,
            self.width,
            self.height,
        )
        bg_img = arcade.gui.UIImage(
            texture=texture,
            width=self.width,
            height=self.height,
            scale=scale,
        )
        self.bg_container.add(bg_img)

        # Оверлей (заливка поверх изображения фона)
        overlay_color = arcade.color.BLACK.replace(a=config.OVERLAY_ALPHA)
        overlay = arcade.gui.UIWidget(
            width=self.width,
            height=self.height,
        ).with_background(color=overlay_color)
        self.bg_container.add(overlay)

    def make_required_buttons(self) -> None:
        """Создает обязательные кнопки по бокам футера.

        Кнопки:
            ВКЛ/ОТКЛ звука справа
            ВЫХОД слева
        """
        # Выход
        self.exit_btn = self.create_button(
            self.callbacks["exit"],
            "ВЫХОД",
        )
        self.footer_container.add(
            self.exit_btn,
            anchor_x="left",
            anchor_y="center",
        )

        # ВКЛ/ОТКЛ звука
        self.sound_btn = self.create_button(
            self.callbacks["sound"],
            "ВЫКЛ ЗВУК",
        )
        self.footer_container.add(
            self.sound_btn,
            anchor_x="right",
            anchor_y="center",
        )

    def debug_layout(self) -> None:
        """Заливает ряды обертки прозрачным цветом."""
        self.header_container = self.header_container.with_background(
            color=arcade.color.RED.replace(a=100),
        )
        self.content_container = self.content_container.with_background(
            color=arcade.color.GREEN.replace(a=100),
        )
        self.footer_container = self.footer_container.with_background(
            color=arcade.color.BLUE.replace(a=100),
        )
