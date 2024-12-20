from typing import Any, List, Dict, Optional
from collections import defaultdict
import statistics
import logging
import matplotlib.pyplot as plt


class DataAnalyzer:
    def __init__(self, data: List[Dict[str, Any]]):
        """
        Инициализирует экземпляр класса DataAnalyzer.

        :param data: Список словарей, содержащих информацию о пользователях и их расходах.
        """
        self.data = data
        self.logger = logging.getLogger(__name__)

    def get_user_total_spending(self, user_id: str) -> float:
        """
        Вычисляет общую сумму трат пользователя за весь период.

        :param user_id: Идентификатор пользователя.
        :return: Общая сумма трат пользователя или 0, если пользователь не найден.
        """
        user = next((user for user in self.data if user["user_id"] == user_id), None)
        if user:
            total_spending = 0
            for card_data in user["user_cards"]:
                total_spending += sum(card_data["monthly_spending"].values())
            self.logger.info(f"User with ID {user_id} has a total spending over the entire period.")
            return total_spending
        return 0

    def get_user_monthly_spending(self, user_id: str) -> Dict[str, float]:
        """
        Вычисляет расходы пользователя за месяц.

        :param user_id: Идентификатор пользователя.
        :return: Словарь с месяцами и соответствующими расходами.
        """
        user = next((user for user in self.data if user["user_id"] == user_id), None)
        if user:
            all_spending = defaultdict(float)
            for card_data in user["user_cards"]:
                for month, amount in card_data["monthly_spending"].items():
                    all_spending[month] += amount
            self.logger.info(f"User with ID {user_id} has monthly spending.")
            return dict(all_spending)
        return {}

    def get_user_min(self, user_id: str) -> Optional[float]:
        """
        Вычисляет минимальную сумму расходов пользователя.

        :param user_id: Идентификатор пользователя.
        :return: Минимальная сумма расходов или None, если пользователь не найден или у него нет расходов.
        """
        user = next((user for user in self.data if user["user_id"] == user_id), None)
        if user:
            all_spending = []
            for card_data in user["user_cards"]:
                all_spending.extend(card_data["monthly_spending"].values())
            self.logger.info(f"User with ID {user_id} has a minimum spending amount.")
            return min(all_spending) if all_spending else None
        return None

    def get_user_max(self, user_id: str) -> Optional[float]:
        """
        Вычисляет максимальную сумму расходов пользователя.

        :param user_id: Идентификатор пользователя.
        :return: Максимальная сумма расходов или None, если пользователь не найден или у него нет расходов.
        """
        user = next((user for user in self.data if user["user_id"] == user_id), None)
        if user:
            all_spending = []
            for card_data in user["user_cards"]:
                all_spending.extend(card_data["monthly_spending"].values())
            self.logger.info(f"User with ID {user_id} has a maximum spending amount.")
            return max(all_spending) if all_spending else None
        return None

    def get_user_mean(self, user_id: str) -> Optional[float]:
        """
        Возвращает среднюю сумму расходов пользователя.


        :param user_id: Идентификатор пользователя.
        :return: Средняя сумма расходов или None, если пользователь не найден или у него нет расходов.
        """
        user = next((user for user in self.data if user["user_id"] == user_id), None)
        if user:
            all_spending = []
            for card_data in user["user_cards"]:
                all_spending.extend(card_data["monthly_spending"].values())
            self.logger.info(f"User with ID {user_id} has an average spending amount.")
            return statistics.mean(all_spending) if all_spending else None
        return None

    def get_user_range(self, user_id: str) -> Optional[float]:
        """
        Вычисляет диапазон (разницу между максимальными и минимальными) расходов пользователя.

        :param user_id: Идентификатор пользователя.
        :return: Диапазон расходов или None, если пользователь не найден или у него нет расходов.
        """
        user = next((user for user in self.data if user["user_id"] == user_id), None)
        if user:
            all_spending = []
            for card_data in user["user_cards"]:
                all_spending.extend(card_data["monthly_spending"].values())
            if not all_spending:
                return None
            self.logger.info(f"User with ID {user_id} has a spending range.")
            return max(all_spending) - min(all_spending)
        return None

    def print_user_cards_and_spending(self, user_id):
        """
        Печатает информацию о карточках и расходах пользователя.

        :param user_id: Идентификатор пользователя, для которого нужно вывести информацию.
        :return: None. Метод выводит данные на экран, не возвращает значений.
        """
        user = next((user for user in self.data if user["user_id"] == user_id), None)
        if user:
            self.logger.info(f"Карточки и расходы пользователя {user_id}:")
            for card_data in user["user_cards"]:
                print(f" Номер карты: {card_data['card_number']}")
                for month, amount in card_data["monthly_spending"].items():
                    print(f"{month}: {amount}")
        else:
            self.logger.warning(f"Warning: User with ID {user_id} not found.")

    def plot_user_monthly_spending_with_min(self, user_id: str):
        """
        Строит график расходов пользователя за месяцы с выделением минимальных значений.

        :param user_id: Идентификатор пользователя.
        """
        user = next((user for user in self.data if user["user_id"] == user_id), None)
        if not user:
            self.logger.warning(f"Warning: User with ID {user_id} not found.")
            return

        # Получение данных о расходах
        monthly_spending = self.get_user_monthly_spending(user_id)
        if not monthly_spending:
            self.logger.info(f"User with ID {user_id} has no spending data.")
            return

        # Найти месяц с максимальными расходами
        min_value = min(monthly_spending.values())
        min_months = [month for month, value in monthly_spending.items() if value == min_value]

        # Построение графика
        months = list(monthly_spending.keys())
        values = list(monthly_spending.values())

        plt.figure(figsize=(10, 6))
        plt.plot(months, values, marker='o', label='Расходы')
        plt.title(f"Расходы пользователя {user_id} по месяцам")
        plt.xlabel("Месяц")
        plt.ylabel("Сумма расходов")
        plt.grid(True)

        # Выделение максимумов
        for month in min_months:
            plt.annotate(f"Min: {min_value}", (month, min_value), textcoords="offset points", xytext=(0, 10), ha='center')
            plt.scatter([month], [min_value], color='red', zorder=5, label='Максимум')

        plt.legend()
        plt.tight_layout()
        plt.show()

    def plot_user_monthly_spending_with_max(self, user_id: str):
        """
        Строит график расходов пользователя за месяцы с выделением максимальных значений.


        :param user_id: Идентификатор пользователя.
        """
        user = next((user for user in self.data if user["user_id"] == user_id), None)
        if not user:
            self.logger.warning(f"Warning: User with ID {user_id} not found.")
            return

        # Получение данных о расходах
        monthly_spending = self.get_user_monthly_spending(user_id)
        if not monthly_spending:
            self.logger.info(f"User with ID {user_id} has no spending data.")
            return

        # Найти месяц с максимальными расходами
        max_value = max(monthly_spending.values())
        max_months = [month for month, value in monthly_spending.items() if value == max_value]

        # Построение графика
        months = list(monthly_spending.keys())
        values = list(monthly_spending.values())

        plt.figure(figsize=(10, 6))
        plt.plot(months, values, marker='o', label='Расходы')
        plt.title(f"Расходы пользователя {user_id} по месяцам")
        plt.xlabel("Месяц")
        plt.ylabel("Сумма расходов")
        plt.grid(True)

        # Выделение максимумов
        for month in max_months:
            plt.annotate(f"Max: {max_value}", (month, max_value), textcoords="offset points", xytext=(0, 10), ha='center')
            plt.scatter([month], [max_value], color='red', zorder=5, label='Максимум')

        plt.legend()
        plt.tight_layout()
        plt.show()