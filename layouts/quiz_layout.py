"""Модуль макета викторины."""

from collections.abc import Callable

import arcade
import arcade.gui

import config
from core import utils
from layouts.base_layout import BaseLayout


class QuizLayout(BaseLayout):
    """Макет для экрана викторины."""

    def __init__(
            self,
            size: tuple[int, int],
            callbacks: dict[str, Callable] | None = None,
    ) -> None:
        """Инициализирует макет викторины."""
        super().__init__(
            size=size,
            propotrions=(0.1, 0.8, 0.1),
            callbacks=callbacks,
        )
        self.lbl_timer: arcade.gui.UILabel | None = None
        self.lbl_counter: arcade.gui.UILabel | None = None
        self.question = {}
        self.answer_map = {}

    def update_timer(self, time_str: str, color_type: str) -> None:
        """Обновляет текст и цвет таймера."""
        if not self.lbl_timer:
            return

        self.lbl_timer.text = time_str
        if color_type == "warning":
            self.lbl_timer.update_font(font_color=arcade.color.RED)

    def _make_header_widgets(self, current_idx: int, total: int) -> None:
        """Верхний ряд: порядковый номер вопроса и таймер."""
        # Порядковый номер вопроса
        self.lbl_counter = self.create_label(
            f"{current_idx + 1} / {total}",
            font="mono",
            font_size=config.FS_L,
        )
        self.header_container.add(
            self.lbl_counter,
            anchor_x="right",
            anchor_y="center",
        )

        # Таймер
        self.lbl_timer = self.create_label(
            "",
            font="mono",
            font_size=config.FS_L,
        )
        self.header_container.add(
            self.lbl_timer,
            anchor_x="center",
            anchor_y="center",
        )

    def _make_image(self) -> None:
        """Создает контейнер и изображение в нем."""
        # Контейнер для изображения
        img_container = arcade.gui.UIBoxLayout(
            size_hint=(0.5, 1),
            align="right",
        ).with_padding(
            top=0,
            bottom=self.padding_ver,
            left=0,
            right=self.padding_hor,
        )
        self.content_container.add(
            img_container,
            anchor_x="left",
            anchor_y="top",
        )

        # Изображение
        image_filename = self.question["изображение"]
        texture_getter = self.callbacks["get texture"]
        texture = texture_getter(image_filename)
        image_max_w = round(self.width * 0.5 - self.padding_hor * 2)
        image_max_h = round(self.height * self.content_ratio - self.padding_ver)
        scale = utils.get_image_scale(
            texture.width,
            texture.height,
            image_max_w,
            image_max_h,
            mode="contain",
        )
        img = arcade.gui.UIImage(
            texture=texture,
            width=round(texture.width * scale),
            height=round(texture.height * scale),
        )
        img_container.add(img)

    def _make_question_content(
            self,
            width_hint: float,
            padding_left: int,
    ) -> None:
        """Создает контейнер и лейблы для вопроса."""
        question_container = arcade.gui.UIBoxLayout(
            size_hint=(width_hint, 1),
            align="left",
            space_between=10,
        ).with_padding(
            top=0,
            bottom=0,
            left=padding_left,
            right=0,
        )

        self.content_container.add(
            question_container,
            anchor_x="right",
            anchor_y="top",
        )

        available_width = self.width * width_hint
        text_width = round(available_width - self.padding_hor - padding_left)
        text_lbl = self.create_label(
            text=self.question["текст"],
            width=text_width,
            multiline=True,
            font_size=config.FS_M,
        )
        question_container.add(text_lbl)

        for letter, text in self.answer_map.items():
            option_lbl = self.create_label(
                text=f"{letter}. {text}",
                width=text_width,
                multiline=True,
                font_size=config.FS_M,
            )
            question_container.add(option_lbl)

    def _make_footer(self) -> None:
        """Нижний ряд: кнопки с ответами."""
        btn_box = arcade.gui.UIBoxLayout(vertical=False, space_between=20)
        for letter in self.answer_map:
            btn = self.create_button(
                on_click=lambda l=letter: self.callbacks["on answer"](l),
                text=letter,
                width=100,
            )
            btn_box.add(btn)

        self.footer_container.add(
            btn_box,
            anchor_x="center",
            anchor_y="center",
        )

    def render_question(
            self,
            question: dict,
            answer_map: dict,
            current_idx: int,
            total: int,
    ) -> None:
        """Полная сборка/перерисовка экрана вопроса."""
        self.question = question
        self.answer_map = answer_map

        # Очищаем контейнеры перед новым вопросом
        self.header_container.clear()
        self.content_container.clear()
        self.footer_container.clear()

        self._make_header_widgets(current_idx, total)
        if question.get("изображение"):
            self._make_image()
            self._make_question_content(
                width_hint=0.5, padding_left=self.padding_hor,
            )
        else:
            self._make_question_content(
                width_hint=1, padding_left=self.padding_hor,
            )

        self._make_footer()
