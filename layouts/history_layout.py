"""Модуль макета истории."""

from collections.abc import Callable

import arcade
import arcade.gui

import utils
from layouts.base_layout import BaseLayout


class HistoryLayout(BaseLayout):
    """Макет для экрана истории."""

    def __init__(
            self,
            width: int,
            height: int,
            on_menu: Callable,
            on_prev: Callable,
            on_next: Callable,
            get_texture_func: Callable,
    ) -> None:
        """Инициализирует макет истории."""
        super().__init__(
            width=width,
            height=height,
            header_ratio=0.1,
            content_ratio=0.8,
            footer_ratio=0.1,
        )
        self.on_menu = on_menu
        self.on_prev = on_prev
        self.on_next = on_next
        self.get_texture: Callable = get_texture_func
        self.lbl_counter: arcade.gui.UILabel | None = None
        self.slide: dict | None = None

    def _make_header_widgets(self, current_idx: int, total: int) -> None:
        """Верхний ряд: заголовок и порядковый номер слада."""
        # Заголовок
        title_lbl = self.create_label(
            text=self.slide["заголовок"],
            font_size=24,
            font="title",
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
            font_size=16,
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
        texture = self.get_texture(self.slide["изображение"])
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
            font_size=24,
            width=text_width,
            multiline=True,
        )
        data_container.add(topic_lbl)

        # Текст
        text_lbl = self.create_label(
            text=self.slide["текст"],
            font_size=24,
            width=text_width,
            multiline=True,
        )
        data_container.add(text_lbl)

    def _make_footer(self, total_pages: int) -> None:
        """Нижний ряд: кнопки пагинации и кнопка меню."""
        navigation_container = arcade.gui.UIBoxLayout(vertical=False, space_between=20)

        btn_prev = self.create_button(on_click=self.on_prev, text="<", width=60)
        btn_menu = self.create_button(on_click=self.on_menu, text="В МЕНЮ")
        btn_next = self.create_button(on_click=self.on_next, text=">", width=60)

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

        # Вешаем фон из слайда
        bg_texture = self.get_texture(slide["фон"])
        self.setup_background(texture=bg_texture)

        # Очищаем контейнеры перед новым вопросом
        self.header_container.clear()
        self.content_container.clear()
        self.footer_container.clear()

        self._make_header_widgets(current_idx, total)
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
