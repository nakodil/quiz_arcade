"""Модуль макета экрана статистики."""

from collections.abc import Callable

import arcade.gui

import config
import utils
from layouts.base_layout import BaseLayout


class StatisticsLayout(BaseLayout):
    """Макет общей статистики."""

    def __init__(
            self,
            size: tuple[int, int],
            callbacks: dict[str, Callable],
    ) -> None:
        """Инициализирует макет статистики."""
        super().__init__(
            size=size,
            propotrions=(0.1, 0.8, 0.1),
            callbacks=callbacks,
        )

    def render_page(
            self,
            records: list,
            page_num: int,
            total_pages: int,
            avg_stats: dict,
    ) -> None:
        """Отрисовывает конкретную страницу данных."""
        self.header_container.clear()
        self.content_container.clear()
        self.footer_container.clear()

        self.make_required_buttons()
        # Вертикальный бокс для заголовка и статистики
        header_vbox = arcade.gui.UIBoxLayout(vertical=True, space_between=5)

        # Главный заголовок
        title = self.create_label(
            "Статистика",
            font="title",
            font_size=config.FS_XL,
        )
        header_vbox.add(title)

        # Строка общей статистики (если есть записи)
        if records:
            avg_time_str = utils.get_formatted_time(int(avg_stats["avg_time"]))
            stats_text = (
                f"В среднем: ✔ {avg_stats["avg_correct"]} | "
                f"❌ {avg_stats["avg_incorrect"]} | "
                f"⏳ {avg_time_str}"
            )
            stats_label = self.create_label(
                stats_text,
                font_size=config.FS_M,
            )
            header_vbox.add(stats_label)

        # Добавляем весь блок заголовков в хедер-контейнер
        self.header_container.add(header_vbox, anchor_x="center", anchor_y="center")

        # Порядковый номер страницы
        page_info = self.create_label(
            f"{page_num + 1} / {total_pages}",
            font_size=config.FS_M,
        )
        self.header_container.add(
            page_info,
            anchor_x="right",
            anchor_y="center",
        )

        # Форматированные элементы статистики
        vbox = arcade.gui.UIBoxLayout(space_between=10, align="left")

        if not records:
            empty_lbl = self.create_label(
                "Статистики пока нет. Пройдите викторину первым;)",
                font_size=config.FS_L,
            )
            vbox.add(empty_lbl)
        else:
            for i, record in enumerate(records, 1):
                row = self._create_record_row(record, i + (page_num * 10))
                vbox.add(row)

        self.content_container.add(vbox, anchor_x="center", anchor_y="center")

        # Контейнер кнопок нижнего ряда
        navigation_container = arcade.gui.UIBoxLayout(vertical=False, space_between=20)

        # Кнопки пагинации
        if total_pages > 1:
            btn_prev = self.create_button(
                on_click=self.callbacks["prev page"],
                text="<",
                width=60,
            )
            navigation_container.add(btn_prev)

        btn_menu = self.create_button(
            on_click=self.callbacks["menu"],
            text="МЕНЮ",
            width=150,
        )
        navigation_container.add(btn_menu)

        if total_pages > 1:
            btn_next = self.create_button(
                on_click=self.callbacks["next page"],
                text=">",
                width=60,
            )
            navigation_container.add(btn_next)

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
        time_spent = utils.get_formatted_time(record.get("потрачено", 0))
        status = record.get("статус", "")
        text = (
            f"{num:02}. | {dt} | ✔{correct} | ❌{incorrect} | "
            f"{time_spent}⏳ | {status}"
        )
        return self.create_label(text=text, font_size=config.FS_M)
