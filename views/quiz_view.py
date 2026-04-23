"""Модуль представления викторины."""

import random
from datetime import datetime
from zoneinfo import ZoneInfo

import config
from layouts import QuizLayout
from views import BaseView


class QuizView(BaseView):
    """Представление викторины (логика игры)."""

    layout: QuizLayout

    def __init__(self, questions: list[dict]) -> None:
        """Инициализирует представление викторины."""
        super().__init__("quiz_bg.jpg")

        self.questions = questions
        self.question_index = 0
        self.correct_count = 0
        self.incorrect_count = 0
        self.window.timer.setup()  # из APP
        self.start_time = datetime.now(ZoneInfo(config.TIMEZONE))
        self.status = config.STATUS["interrupted"]
        self.timer = self.window.timer

        # Создаем макет
        additional_callbacks = {
            "get texture": self.window.get_texture,
            "on answer": self.on_answer,
        }
        self.callbacks.update(additional_callbacks)
        self.layout: QuizLayout = QuizLayout(
            size=(self.window.width, self.window.height),
            callbacks=self.callbacks,
        )
        self.ui.add(self.layout)
        self.setup_layout(self.layout)
        self.prepare_question()

    def on_update(self, delta_time: float) -> None:
        """Обновление логики таймера и его визуального состояния."""
        self.timer.on_update(delta_time)
        time_str = self.timer.get_time_str()
        self.layout.update_timer(time_str, self.timer.color)
        if self.timer.is_over:
            self.status = config.STATUS["time_is_over"]
            self._finish()

    def prepare_question(self) -> None:
        """Формирование данных для текущего вопроса."""
        question = self.questions[self.question_index]

        # Перемешивание ответов
        answers = question["варианты"].copy()
        random.shuffle(answers)
        letters = ["A", "B", "C", "D", "E"]
        self.answer_map = {letters[i]: answers[i] for i in range(len(answers))}

        # Командуем макету отрисовать вопрос
        self.layout.render_question(
            question=question,
            answer_map=self.answer_map,
            current_idx=self.question_index,
            total=len(self.questions),
        )

    def on_answer(self, letter: str) -> None:
        """Коллбек для кнопок с вариантом ответа."""
        if self.question_index >= len(self.questions):
            return

        question = self.questions[self.question_index]

        if self.answer_map[letter] == question.get("ответ"):
            self.correct_count += 1
        else:
            self.incorrect_count += 1

        self._next_step()

    def _next_step(self) -> None:
        """Переход к следующему вопросу или завершение."""
        self.question_index += 1

        if self.question_index < len(self.questions):
            self.prepare_question()
            return
        self.status = config.STATUS["completed"]
        self._finish()

    def _finish(self) -> None:
        """Сбор статистики и переход на экран финиша."""
        now = datetime.now(ZoneInfo(config.TIMEZONE))
        duration = int((now - self.start_time).total_seconds())

        stats = {
            "дата": now.strftime("%d.%m.%Y %H:%M"),
            "верно": self.correct_count,
            "ошибки": self.incorrect_count,
            "потрачено": duration,
            "статус": self.status,
        }
        self.window.show_finish(stats)
