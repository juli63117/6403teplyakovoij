import argparse
import json
import logging
from data_module.data_save import SaveData
from analisys_module.data_analisys import DataAnalyzer
from interface.interface import UserInteraction

class UserDataManager:
    def __init__(self):
        self.savedata = SaveData()
        self.user_interaction = UserInteraction(self.load_data, self.save_data)
        self.data_analyzer = DataAnalyzer(self.user_interaction.data)
        self.logger = logging.getLogger(__name__)

    def load_data(self):
        return self.savedata.data

    def save_data(self, data):
        self.savedata.data = data
        self.savedata.save()

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description="Управление данными пользователей, картами и информацией о расходах.")
        subparsers = parser.add_subparsers(dest='command')

        # Добавить карту
        add_card_parser = subparsers.add_parser('add_card', help='Добавить новую платежную карту для пользователя')
        add_card_parser.add_argument('user_id', type=str, help='Уникальный идентификатор пользователя')
        add_card_parser.add_argument('card_number', type=str, help='Номер карты (например, 1234-5678-9876-5432)')
        add_card_parser.add_argument('expiry_date', type=str, help='Срок действия карты в формате MM/YY (например, 12/24)')
        add_card_parser.add_argument('cvv_code', type=int, help='CVV код (3 цифры с обратной стороны карты)')
        add_card_parser.add_argument('monthly_spending', type=str, help='Данные о ежемесячных расходах в формате JSON')

        # Удалить карту
        delete_card_parser = subparsers.add_parser('delete_card', help='Удалить платежную карту у пользователя')
        delete_card_parser.add_argument('user_id', type=str, help='Уникальный идентификатор пользователя')
        delete_card_parser.add_argument('card_number', type=str, help='Номер карты для удаления')

        # Обновить карту
        update_card_parser = subparsers.add_parser('update_card', help='Обновить информацию о существующей карте')
        update_card_parser.add_argument('user_id', type=str, help='Уникальный идентификатор пользователя')
        update_card_parser.add_argument('card_number', type=str, help='Номер карты для обновления')
        update_card_parser.add_argument('expiry_date', type=str, help='Новая дата истечения (MM/YY)')
        update_card_parser.add_argument('cvv_code', type=int, help='Новый CVV код')
        update_card_parser.add_argument('monthly_spending', type=str, help='Обновленные данные о ежемесячных расходах (формат JSON)')

        # Обновить пользователя
        update_parser = subparsers.add_parser('update_user', help='Обновить информацию о пользователе')
        update_parser.add_argument('user_id', type=str, help='Уникальный идентификатор пользователя')
        update_parser.add_argument('user_data', type=str, help='Обновленные данные о пользователе в формате JSON')

        # Добавить пользователя
        add_user_parser = subparsers.add_parser('add_user', help='Создать новую учетную запись пользователя')
        add_user_parser.add_argument('user_id', type=str, help='Уникальный идентификатор для нового пользователя')
        add_user_parser.add_argument('user_data', type=str, help='Дополнительные данные о пользователе в формате JSON')

        # Общие расходы
        total_spending_parser = subparsers.add_parser('total_spending', help='Рассчитать общие расходы пользователя')
        total_spending_parser.add_argument('user_id', type=str, help='Уникальный идентификатор пользователя')

        # Ежемесячные расходы
        monthly_spending_parser = subparsers.add_parser('monthly_spending', help='Получить данные о ежемесячных расходах пользователя')
        monthly_spending_parser.add_argument('user_id', type=str, help='Уникальный идентификатор пользователя')

        # Минимальные расходы
        get_user_min_parser = subparsers.add_parser('get_user_min', help='Найти минимальные ежемесячные расходы пользователя')
        get_user_min_parser.add_argument('user_id', type=str, help='Уникальный идентификатор пользователя')

        # Максимальные расходы
        get_user_max_parser = subparsers.add_parser('get_user_max', help='Найти максимальные ежемесячные расходы пользователя')
        get_user_max_parser.add_argument('user_id', type=str, help='Уникальный идентификатор пользователя')

        # Средние расходы
        get_user_mean_parser = subparsers.add_parser('get_user_mean', help='Рассчитать средние ежемесячные расходы пользователя')
        get_user_mean_parser.add_argument('user_id', type=str, help='Уникальный идентификатор пользователя')

        # Диапазон расходов
        get_user_range_parser = subparsers.add_parser('get_user_range', help='Рассчитать диапазон расходов пользователя')
        get_user_range_parser.add_argument('user_id', type=str, help='Уникальный идентификатор пользователя')

        # Печать карт пользователя
        print_user_cards_and_spending_parser = subparsers.add_parser('print_user_cards_and_spending', help='Список карт пользователя и их детали расходов')
        print_user_cards_and_spending_parser.add_argument('user_id', type=str, help='Уникальный идентификатор пользователя')

        # Минимальная трата за месяц
        plot_user_min_parser = subparsers.add_parser('plot_user_monthly_min', help='Построить график расходов пользователя за месяцы с выделением минимальных значений')
        plot_user_min_parser.add_argument('user_id', type=str, help='Unique identifier of the user')

        # Максимальная трата за месяц
        plot_user_max_parser = subparsers.add_parser('plot_user_monthly_max',help='Построить график расходов пользователя за месяцы с выделением максимальных значений')
        plot_user_max_parser.add_argument('user_id', type=str, help='Unique identifier of the user')

        return parser.parse_args()

    def execute_command(self, args):
        try:
            if args.command == "add_card":
                monthly_spending = json.loads(args.monthly_spending)
                self.user_interaction.add_card(args.user_id, args.card_number, args.expiry_date, args.cvv_code, monthly_spending)
                self.logger.info(f"Card added for user {args.user_id}")

            elif args.command == "delete_card":
                self.user_interaction.delete_card(args.user_id, args.card_number)
                self.logger.info(f"Card deleted for user {args.user_id}")

            elif args.command == "update_card":
                monthly_spending = json.loads(args.monthly_spending)
                self.user_interaction.update_card(args.user_id, args.card_number, args.expiry_date, args.cvv_code, monthly_spending)
                self.logger.info(f"Card updated for user {args.user_id}")

            elif args.command == "add_user":
                additional_data = json.loads(args.user_data)
                user_data = {"user_id": args.user_id, **additional_data}
                self.user_interaction.add_user(user_data)
                self.logger.info(f"User successfully added.")

            elif args.command == "update_user":
                user_data = json.loads(args.user_data)
                self.user_interaction.update_user(args.user_id, user_data)
                self.logger.info(f"Data for user {args.user_id} updated.")

            elif args.command == "total_spending":
                total = self.data_analyzer.get_user_total_spending(args.user_id)
                self.logger.info(f"Total spending for user {args.user_id}: {total}")

            elif args.command == "monthly_spending":
                monthly = self.data_analyzer.get_user_monthly_spending(args.user_id)
                self.logger.info(f"Monthly spending for user {args.user_id}: {monthly}")

            elif args.command == "get_user_min":
                monthly = self.data_analyzer.get_user_min(args.user_id)
                self.logger.info(f"Minimum monthly spending for user {args.user_id}: {monthly}")

            elif args.command == "get_user_max":
                monthly = self.data_analyzer.get_user_max(args.user_id)
                self.logger.info(f"Maximum monthly spending for user {args.user_id}: {monthly}")

            elif args.command == "get_user_mean":
                monthly = self.data_analyzer.get_user_mean(args.user_id)
                self.logger.info(f"Average monthly spending for user {args.user_id}: {monthly}")

            elif args.command == "get_user_range":
                monthly = self.data_analyzer.get_user_range(args.user_id)
                self.logger.info(f"Range of monthly spending for user {args.user_id}: {monthly}")

            elif args.command == "print_user_cards_and_spending":
                self.data_analyzer.print_user_cards_and_spending(args.user_id)
                self.logger.info(f"Cards and spending for user {args.user_id} printed.")

            elif args.command == "plot_user_monthly_min":
                self.data_analyzer.plot_user_monthly_spending_with_min(args.user_id)
                self.logger.info(f"Spending chart for user {args.user_id} with minimum values created.")

            elif args.command == "plot_user_monthly_max":
                self.data_analyzer.plot_user_monthly_spending_with_max(args.user_id)
                self.logger.info(f"Spending chart for user {args.user_id} with maximum values created.")

            else:
                self.logger.warning("Invalid command.")
        except json.JSONDecodeError:
            self.logger.warning("Invalid JSON format for monthly spending.")
        except Exception as e:
            self.logger.warning(f"An error occurred: {e}")
