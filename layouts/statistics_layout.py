"""Модуль макета экрана статистики."""

from collections.abc import Callable

import arcade.gui

from layouts.base_layout import BaseLayout


class StatisticsLayout(BaseLayout):
    """Макет общей статистики."""

    def __init__(
            self,
            width: int,
            height: int,
            on_menu: Callable,
            on_prev: Callable,
            on_next: Callable,
    ) -> None:
        """Инициализирует макет с пагинацией."""
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

    def render_page(self, records: list, page_num: int, total_pages: int):
        """Отрисовывает конкретную страницу данных."""
        self.header_container.clear()
        self.content_container.clear()
        self.footer_container.clear()

        # Заголовок
        title = self.create_label("Статистика", font_size=40, font="title")
        self.header_container.add(title, anchor_x="center", anchor_y="center")

        # Форматированные элементы статистики
        vbox = arcade.gui.UIBoxLayout(space_between=10, align="left")

        if not records:
            vbox.add(self.create_label("История игр пока пуста", font_size=24))
        else:
            for i, record in enumerate(records, 1):
                vbox.add(self._create_record_row(record, i + (page_num * 10)))

        self.content_container.add(vbox, anchor_x="center", anchor_y="center")

        # Контейнер кнопок нижнего ряда
        navigation_container = arcade.gui.UIBoxLayout(vertical=False, space_between=20)

        # Кнопки пагинации
        if total_pages > 1:
            btn_prev = self.create_button(
                on_click=self.on_prev,
                text="<",
                width=60,
            )
            btn_next = self.create_button(
                on_click=self.on_next,
                text=">",
                width=60,
            )

            page_info = self.create_label(
                f"{page_num + 1} / {total_pages}",
                font_size=18,
            )

            navigation_container.add(btn_prev)
            navigation_container.add(page_info)
            navigation_container.add(btn_next)

        # Кнопка меню
        btn_menu = self.create_button(
            on_click=self.on_menu,
            text="МЕНЮ",
            width=150,
        )
        navigation_container.add(btn_menu)
        self.footer_container.add(
            navigation_container,
            anchor_x="center",
            anchor_y="center",
        )

    def _create_record_row(
            self,
            record: dict,
            num: int,
    ) -> arcade.gui.UILabel:
        """Отдает форматированную строку статистики лейблом."""
        dt = record.get("дата", "")
        correct = record.get("верно", 0)
        incorrect = record.get("ошибки", 0)
        status = record.get("статус", "")
        text = f"{num:02}. {dt} | ✔{correct} | ✖{incorrect} | {status}"

        return self.create_label(text=text, font_size=18)
