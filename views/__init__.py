"""Импорт представлений."""

from .base_view import BaseView
from .finish_view import FinishView
from .history_view import HistoryView
from .loading_view import LoadingView
from .menu_view import MenuView
from .quiz_view import QuizView
from .statistics_view import StatisticsView

__all__ = [
    "BaseView",
    "FinishView",
    "HistoryView",
    "LoadingView",
    "MenuView",
    "QuizView",
    "StatisticsView",
]
