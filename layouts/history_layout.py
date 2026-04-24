"""Модуль макета истории."""

from collections.abc import Callable

import arcade
import arcade.gui

import config
from core import utils
from layouts.base_layout import BaseLayout


class HistoryLayout(BaseLayout):
    """Макет для экрана истории."""

    def __init__(
            self,
            size: tuple[int, int],
            callbacks: dict[str, Callable] | None = None,
    ) -> None:
        """Инициализирует макет истории."""
        super().__init__(
            size=size,
            propotrions=(0.1, 0.8, 0.1),
            callbacks=callbacks,
        )
        self.lbl_counter: arcade.gui.UILabel | None = None
        self.slide = {}

    def _make_content_widgets(self, current_idx: int, total: int) -> None:
        """Верхний ряд: заголовок и порядковый номер слада."""
        # Заголовок
        title_lbl = self.create_label(
            text=self.slide["заголовок"],
            font="title",
            font_size=config.FS_XL,
        )
        self.header_container.add(
            title_lbl,
            anchor_x="center",
            anchor_y="center",
        )

        # Порядковый номер
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
        imgage_filename = self.slide["изображение"]  # DRY: все как в QuizView
        texture_getter = self.callbacks["get texture"]
        texture = texture_getter(imgage_filename)
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

    def _make_slide_content(
            self,
            width_hint: float,
            padding_left: int,
    ) -> None:
        """Создает контейнер и лейблы для слайда."""
        data_container = arcade.gui.UIBoxLayout(
            size_hint=(width_hint, 1),
            align="left",
            space_between=self.padding_ver,
        ).with_padding(
            top=0,
            bottom=0,
            left=padding_left,
            right=0,
        )

        self.content_container.add(
            data_container,
            anchor_x="right",
            anchor_y="top",
        )

        available_width = self.width * width_hint
        text_width = round(available_width - self.padding_hor - padding_left)

        # Тема
        topic_lbl = self.create_label(
            text=self.slide["тема"],
            width=text_width,
            multiline=True,
            font_size=config.FS_L,
        )
        data_container.add(topic_lbl)

        # Текст
        text_lbl = self.create_label(
            text=self.slide["текст"],
            width=text_width,
            multiline=True,
            font_size=config.FS_M,
        )
        data_container.add(text_lbl)

    def _make_footer(self, total_pages: int) -> None:
        """Нижний ряд: кнопки пагинации и кнопка меню."""
        self.make_required_buttons()
        navigation_container = arcade.gui.UIBoxLayout(
            vertical=False,
            space_between=20,
        )

        btn_prev = self.create_button(
            on_click=self.callbacks["on prev"],
            text="<",
            width=60,
        )
        btn_menu = self.create_button(
            on_click=self.callbacks["menu"],
            text="В МЕНЮ",
        )
        btn_next = self.create_button(
            on_click=self.callbacks["on next"],
            text=">",
            width=60,
        )

        # Добавляем кнопку "назад", если страниц больше одной
        if total_pages > 1:
            navigation_container.add(btn_prev)

        # Кнопка меню всегда по центру
        navigation_container.add(btn_menu)

        # Добавляем кнопку "вперед", если страниц больше одной
        if total_pages > 1:
            navigation_container.add(btn_next)

        # Теперь добавляем весь ряд с кнопками в футер
        self.footer_container.add(
            navigation_container, anchor_x="center", anchor_y="center",
        )

    def render_slide(
            self,
            slide: dict,
            current_idx: int,
            total: int,
    ) -> None:
        """Полная сборка/перерисовка слайда."""
        self.slide = slide

        # Очищаем контейнеры перед новым вопросом
        self.header_container.clear()
        self.content_container.clear()
        self.footer_container.clear()

        self._make_content_widgets(current_idx, total)
        if slide.get("изображение"):
            self._make_image()
            self._make_slide_content(
                width_hint=0.5, padding_left=self.padding_hor,
            )
        else:
            self._make_slide_content(
                width_hint=1, padding_left=0,
            )

        self._make_footer(total)
